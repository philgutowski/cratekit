"""``label.judge``: judge the label releases already waiting in review (R-815).

WHAT THIS VERB IS FOR. The genre gate of R-798 judges a release when a sweep is
about to file it. A release already in the review queue takes a place in its
label's offer window and is skipped before the gate is asked, so the 2,755
releases a sweep filed before the gate had a genre to read were never judged,
and a later sweep of 4 hours 42 minutes filed nothing and held nothing. This
verb judges the pending releases themselves, with no sweep, and moves the ones
the gate would not have filed out of review and into a hold.

ONE RULE, THE SWEEP'S. A release is judged by
:meth:`cratekit.label.gate.SweepGate.judge_as`, the body the sweep's own
``judge`` runs, against the kind its label is followed as. This module owns no
rule and no sentence about a verdict. It owns the walk over the queue, what is
written for each release, and when the run stops.

WHAT THE ITEM RECORDS IS USED FIRST, because asking costs two provider reads
before the general catalogue is asked anything. See :func:`_judged` for the
order and what each branch costs.

A HELD RELEASE LEAVES THE QUEUE. :func:`cratekit.core.review.withhold` deletes
the open item and writes the hold in one transaction. It is not rejected and no
tombstone is written: ``crate label held`` lists it with its reason and
``crate label held return`` files it again. A release the gate passes, or
cannot judge, stays in review and its item says what the gate said.

IT DECIDES NOTHING AND DOWNLOADS NOTHING. An item a person has decided is never
touched, and neither is a release a person returned to review.

IT IS A JOB, ONE ITEM PER PENDING RELEASE, so a pass over thousands of releases
picks up where it stopped. A finished item is never claimed again, and the one
in flight when a run died is redone safely: a release this job already held is
found as its hold, and a stamped one is judged from its record.

A CATALOGUE THAT REFUSES PARKS THE RUN. One refusal is enough, and an outage
is given the gate's own bound, three releases in a row unread. Nothing here
retries, waits out or goes round an answer. The same holds for the provider.
See :func:`_asked`.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, artifacts, config, jobs, review, routing
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Queue
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import Taxonomy
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.tagging import published, searchers, shell

ORIGIN = ("label", "judge_cli")

#: Where one release's report is staged and committed, under the queue root.
ARTIFACTS = artifacts.Location(final="label-judge-artifacts", staging="label-judge-staging")

#: What happened to one release, as its report says it. The first three are the
#: gate's verdicts in the gate's own words. The last three are releases the gate
#: was not asked about: one a person returned to review, one a person has
#: decided, and one that was no longer in review when its turn came.
HELD = KindVerdict.HOLD.value
PASSED = KindVerdict.PASS.value
NOT_JUDGED = KindVerdict.NOT_JUDGED.value
RETURNED = genre_gate.RETURNED
DECIDED = "decided"
GONE = "gone"
OUTCOMES: tuple[str, ...] = (HELD, PASSED, NOT_JUDGED, RETURNED, DECIDED, GONE)

#: The warning codes a finished run can carry. Warnings and not causes: the run
#: did what it could, and each names what a person may still want to do.
NOT_JUDGED_LEFT = "label-judge-not-judged"
CATALOGUE_UNREAD = "label-judge-catalogue-unread"
NOTHING_PENDING = "label-judge-nothing-pending"


def build_judge(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the judging job already queued under this identifier",
    )
    parser.add_argument(
        "--label",
        action="append",
        dest="labels",
        default=None,
        metavar="NAME",
        help=(
            "judge only the pending releases of this followed label; repeat it "
            "for several. Without it every pending label release is judged"
        ),
    )
    parser.set_defaults(_handler=label_judge)


def label_judge_argv(job) -> list[str]:
    """The command line that continues one queued judging job."""
    return ["label", "judge", "--job", job.job_id]


# ---------------------------------------------------------------------------
# Queueing
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Scope:
    """The followed labels a run is narrowed to, and the registry that names them."""

    label_ids: tuple[str, ...]
    followed: labels.Registry

    def holds(self, label_id: str) -> bool:
        """Whether a release filed under ``label_id`` is one of the labels named.

        THROUGH THE REGISTRY, not by comparing the text. An item filed before
        a label's identifier moved carries the old one, and the worker reads
        it through ``by_id``, which follows the move. Compared as text, the
        label's own releases would be left out of a run scoped to it.
        """
        entry = self.followed.by_id(label_id) if label_id else None
        return entry is not None and entry.label_id in self.label_ids


def _scope(names: Sequence[str] | None) -> _Scope | None:
    """The followed labels ``--label`` names, or None when it names none.

    EVERY NAME IS RESOLVED BEFORE ANYTHING IS QUEUED, so a mistyped label
    refuses the run and is not read as "that label has nothing pending".
    """
    wanted = [str(name).strip() for name in names or () if str(name).strip()]
    if not wanted:
        return None
    followed = labels.RegistryStore().load()
    found: dict[str, None] = {}
    unknown: list[str] = []
    for name in wanted:
        entry = followed.resolve(name)
        if entry is None:
            unknown.append(name)
        else:
            found.setdefault(entry.label_id, None)
    if unknown:
        raise refuse(
            "label-unknown",
            f"no followed label is named {', '.join(repr(one) for one in unknown)}, "
            f"so there is nothing of it to judge; nothing was queued",
            steps=("take the name from: crate label registry list",),
            origin=ORIGIN,
            detail={"unknown": unknown},
        )
    return _Scope(tuple(found), followed)


def pending(store: review.ReviewStore, scope: _Scope | None = None) -> tuple[str, ...]:
    """The review items a judging job is made of: every open label release.

    READ OFF THE REVIEW QUEUE AND NOTHING ELSE. No provider is asked, so
    queueing cannot refuse where the work would have run once claimed.
    ``scope`` narrows it to the labels named.
    """
    page = review.list_items(
        store, queue=str(Queue.LABEL_RELEASE), kinds=(sweep.KIND,), limit=None
    )
    return tuple(
        item.item_id
        for item in page.items
        if scope is None or scope.holds(str(item.payload.get("label_id") or ""))
    )


def label_judge(ctx) -> Envelope:
    """Queue one judging job over the pending label releases, or drive one."""
    cfg = label_cli._load()
    if ctx.args.job:
        return _resume(ctx, cfg)
    scope = _scope(ctx.args.labels)
    # THE DECLARATION BEFORE ANYTHING IS QUEUED, as the sweep reads it before
    # its first login. A taxonomy that cannot be read refuses here, with its
    # own remedy, and not once per release in a detached child.
    active_taxonomy.load(cfg)
    with review.open_store(cfg) as queue:
        items = pending(queue, scope)
    if not items:
        # THE HONEST ZERO. A job with no items drives straight to succeeded, so
        # queueing one would report a judging pass over a queue nothing read.
        return ctx.envelope(
            data=shell.no_op("no-op"),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": NOTHING_PENDING,
                    "message": (
                        "no label release is waiting in review"
                        + (" for the labels named" if scope is not None else "")
                        + ", so there is nothing to judge"
                    ),
                },
            ),
        )
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"labels": list(scope.label_ids) if scope is not None else []},
            item_ids=items,
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job), warnings=label_cli.queue_warnings())


# ---------------------------------------------------------------------------
# The summary, read from what ran
# ---------------------------------------------------------------------------


def _counts() -> dict[str, int]:
    return {"judged": 0, **dict.fromkeys(OUTCOMES, 0), "asked": 0, "unread": 0}


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this job's committed reports say happened, per label and in total.

    DERIVED FROM WHAT RAN, never from what was queued, so it is true across a
    resume: the reports a previous process committed are counted with this
    one's.

    ``judged`` IS HELD PLUS PASSED, the releases the gate gave a verdict on.
    ``asked`` counts the releases THE PROVIDER WAS ASKED FOR, whether or not
    it answered: a read that failed spent its calls like one that did not, so
    this is the number a run's provider cost is sized from. ``unread`` counts
    the ones the general catalogue could not be read for. ZEROES INCLUDED for
    every outcome, because the set is closed and "none of those" is a fact
    worth a number.
    """
    totals = _counts()
    rows: dict[str, dict[str, Any]] = {}
    for report in artifacts.committed(ARTIFACTS, cfg, job_id):
        outcome = str(report.get("outcome") or "")
        if outcome not in OUTCOMES:
            continue
        label_id = str(report.get("label_id") or "")
        row = rows.setdefault(
            label_id,
            {"label_id": label_id, "label_name": str(report.get("label_name") or ""), **_counts()},
        )
        for counted in (totals, row):
            counted[outcome] += 1
            if outcome in (HELD, PASSED):
                counted["judged"] += 1
            if report.get("asked"):
                counted["asked"] += 1
            if report.get("answer") in published.UNREAD:
                counted["unread"] += 1
    return {
        **totals,
        "labels": sorted(
            rows.values(), key=lambda row: str(row["label_name"] or row["label_id"]).casefold()
        ),
    }


def _warnings(counted: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    found: list[dict[str, str]] = []
    if counted["unread"]:
        found.append(
            {
                "code": CATALOGUE_UNREAD,
                "message": (
                    f"the general catalogue could not be read for {counted['unread']} "
                    f"release(s); they stay in review marked not judged, and another "
                    f"run of crate label judge asks about them again"
                ),
            }
        )
    if counted[NOT_JUDGED]:
        found.append(
            {
                "code": NOT_JUDGED_LEFT,
                "message": (
                    f"{counted[NOT_JUDGED]} release(s) stay in review not judged; "
                    f"each says why in: crate review list --queue {Queue.LABEL_RELEASE}"
                ),
            }
        )
    return tuple(found)


def _left(store, job_id: str) -> int:
    """How many of the job's releases no run has finished."""
    counts = jobs.progress(store, job_id)["counts"]
    settled = (str(jobs.ItemState.DONE), str(jobs.ItemState.SKIPPED))
    return sum(n for state, n in counts.items() if state not in settled)


def _with_summary(error: CratekitError, cfg: config.Config, store, job_id: str) -> CratekitError:
    """The same refusal, carrying what the run did and how much it left.

    A QUEUED VERB HAS TWO EXITS AND THE ENVELOPE IS ONLY ONE OF THEM. A run
    that parked, failed or was stopped leaves through its cause, and that is
    the run a person most needs the counts from: releases were held before it
    stopped. The cause is extended and never rebuilt, so its trail, its remedy
    and its type come through unchanged.
    """
    left = _left(store, job_id)
    cause = error.cause
    # A PARKED JOB IS OPEN and this verb drives it. One that failed or was
    # stopped is closed, and only ``job resume`` re-arms a closed job.
    how = (
        f"crate label judge --job {job_id}"
        if jobs.get(store, job_id).is_open()
        else f"crate job resume {job_id}, then read what it did with: "
        f"crate label judge --job {job_id}"
    )
    step = f"{left} release(s) of this job are not judged yet; continue with: {how}"
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(cause.remediation, steps=(*cause.remediation.steps, step)),
            detail={**cause.detail, "judging": summary(cfg, job_id), "left": left},
        ),
    )


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Continue the judging job named on ``--job``, and report what it did."""
    with jobs.open_store() as store:
        queued = jobs.get(store, ctx.args.job)
        # THE JOB HAS TO BE THIS VERB'S. The worker is resolved from the job row
        # and not from this verb, so without this line the verb would drive any
        # queued job of any verb, under this verb's envelope and without that
        # verb's own resume time checks.
        if queued.handler_key != ctx.entry.handler_key:
            raise refuse(
                "job-unknown",
                f"job {queued.job_id} was queued for {queued.handler_key!r}, which "
                f"is not a judging job, so this verb will not drive it",
                steps=(
                    f"resume it through its own verb, or with: crate job resume "
                    f"{queued.job_id}",
                ),
                origin=ORIGIN,
                detail={"job_id": queued.job_id, "handler": queued.handler_key},
            )
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=ORIGIN,
                nothing_to_run="report a judging pass over releases it never read",
            )
        except CratekitError as failed:
            if not jobs.items(store, queued.job_id):
                raise
            raise _with_summary(failed, cfg, store, queued.job_id) from failed
        counted = summary(cfg, job.job_id)
        return ctx.envelope(
            data=shell.reported(store, job, {"judging": counted}),
            warnings=(*warnings, *_warnings(counted)),
        )


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


@dataclass
class _Tools:
    """What one job's items share, each made on first use and kept for the job.

    ``asking`` and ``reader`` carry the two counts of failures in a row, which
    are counts across releases and would start at zero for every release if
    they were built per item. ``refused`` is the general catalogue's refusal,
    once it has given one. ``declared`` and ``followed`` are the library's
    taxonomy and the label registry, read once for the job and not once for
    each of thousands of releases, most of which are judged from their own
    record with nothing else read at all.
    """

    asking: genre_gate.Asking
    reader: catalogue.ReleaseTracks | None = None
    refused: str | None = None
    declared: Taxonomy | None = None
    followed: labels.Registry | None = None


#: The tools of the one job being driven, keyed by the job, on the reasoning
#: ``label.cli._JOB_ASKING`` gives. NOT THAT HOLDER, which keeps an asking and
#: nothing else and is never dropped: this one is dropped when the run parks.
_JOB_TOOLS: dict[str, _Tools] = {}


def _tools(job) -> _Tools:
    key = str(job.job_id)
    held = _JOB_TOOLS.get(key)
    if held is None:
        _JOB_TOOLS.clear()
        held = _JOB_TOOLS[key] = _Tools(genre_gate.Asking())
    return held


def _parked(job, error: CratekitError) -> jobs.Parked:
    """``error`` as the park that stops the run, with this job's tools dropped.

    EVERY REFUSAL THIS WORKER MEETS STOPS THE RUN, and none fails the item. A
    refusal here is never about one release: it is a catalogue that stopped
    answering, a provider session that expired, a taxonomy or a registry or a
    review database that cannot be read. Every later release would meet the
    same one, and failing each in turn would walk a queue of thousands marking
    every release failed over one cause. Parked, the release in flight goes
    back to pending and the job waits for a person.

    DROPPED, so a resume asks afresh. A resume is a person's act, taken after
    whatever refused has had time to stop refusing, and a count of unread
    answers carried into it would park the run again without asking anybody.
    """
    _JOB_TOOLS.pop(str(job.job_id), None)
    if isinstance(error, jobs.Parked):
        return error
    return jobs.Parked(error.cause)


@dataclass(frozen=True, slots=True)
class _Subject:
    """One release as its review item names it."""

    release_id: str
    label_id: str
    label_name: str
    title: str
    artist: str


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _subject(
    store: review.ReviewStore, item: review.Item, entry: labels.LabelEntry | None
) -> _Subject:
    """The release an item names, and the label it is counted and held under.

    The release through the one reader ``label approved`` reads an item by.

    THE LABEL IS THE REGISTRY'S WHEN THE REGISTRY HOLDS IT. An item filed
    before a label's identifier moved carries the old one, and a hold written
    under that would be one no sweep of the label ever looks at, since a sweep
    asks for the holds under the identifier the label has now. A label nobody
    follows any more keeps what the item says.
    """
    return _Subject(
        release_id=genre_gate.release_id_of(store, item),
        label_id=entry.label_id if entry is not None else _text(item.payload.get("label_id")),
        label_name=entry.name if entry is not None else _text(item.payload.get("label_name")),
        title=_text(item.payload.get("title")),
        artist=_text(item.payload.get("artist")),
    )


def _not_judged(declared: Taxonomy, kind: str | None, why: str, answer: str) -> genre_gate.Judged:
    return genre_gate.Judged(
        KindVerdict.NOT_JUDGED, routing.label_kind(declared, kind), (), why, answer
    )


def _asked(
    job, cfg: config.Config, declared: Taxonomy, kind: str | None, release_id: str
) -> genre_gate.Judged:
    """Read the release's rows and ask the general catalogue. The one costly branch.

    THE RUN STOPS BEFORE A READ IT ALREADY KNOWS IS WASTED, and this refuses
    so the worker parks the run. See :func:`_parked`. Three things end it:

    * THE GENERAL CATALOGUE REFUSED, once. The lookup remembers a refusal for
      the rest of the process and answers every later release from memory, so
      the release after a refusal is not read from the provider to be told
      the same thing. The refused release itself was asked about and stays in
      review saying so.
    * THE GENERAL CATALOGUE WENT UNREAD for the gate's own bound of releases
      in a row, which is how an outage ends: an outage is not remembered, so
      it is given the bound a sweep gives it.
    * THE PROVIDER FAILED its own bound of reads in a row, or refused, an
      expired session or a cooldown.

    NOTHING HERE RETRIES OR WAITS. The lookup paces its own requests and the
    provider's reads go through its gate. This function only decides when to
    stop asking.

    THE READER FORGETS EACH RELEASE ONCE IT IS JUDGED. Nothing asks for one
    release twice in this job, and its count of failures in a row is all the
    next release needs from it.
    """
    tools = _tools(job)
    if tools.refused is not None:
        raise refuse(
            "catalogue-unreachable",
            f"the general catalogue refused ({tools.refused}), so the run stopped "
            f"asking it. The release it refused stays in review marked not "
            f"judged, and the next one was not read from the provider",
            steps=(
                "wait before continuing: nothing here tries to get past a "
                "catalogue that refuses",
            ),
            origin=ORIGIN,
            detail={"job_id": str(job.job_id), "refused": tools.refused},
        )
    if tools.asking.given_up:
        raise refuse(
            "catalogue-unreachable",
            f"the general catalogue could not be read for "
            f"{genre_gate.UNREAD_IN_A_ROW} releases in a row, so the run stopped "
            f"asking it. Those releases stay in review marked not judged, and "
            f"the next one was not read from the provider",
            steps=(
                "wait before continuing: nothing here tries to get past a "
                "catalogue that refuses",
            ),
            origin=ORIGIN,
            detail={"job_id": str(job.job_id), "unread_in_a_row": genre_gate.UNREAD_IN_A_ROW},
        )
    if tools.reader is None:
        tools.reader = catalogue.ReleaseTracks(catalogue.resolve(cfg))
    if tools.reader.given_up:
        raise refuse(
            "unavailable-transient",
            f"the provider failed {catalogue.READS_FAILED_IN_A_ROW} release reads "
            f"in a row, so the run stopped reading. Those releases stay in "
            f"review marked not judged",
            remedy=Remedy.RESUME_JOB,
            origin=ORIGIN,
            detail={"job_id": str(job.job_id)},
        )
    gate = genre_gate.SweepGate(declared, tracks=tools.reader.release_tracks, asking=tools.asking)
    try:
        judged = gate.judge_as(kind, release_id)
    finally:
        tools.reader.forget()
    if judged.answer == searchers.Answer.BLOCKED.value:
        tools.refused = judged.reason
    return judged


def _judged(
    job,
    cfg: config.Config,
    declared: Taxonomy,
    kind: str | None,
    item: review.Item,
    subject: _Subject,
) -> tuple[genre_gate.Judged, bool]:
    """The gate's verdict on one pending release, and whether the provider was read.

    WHAT THE ITEM RECORDS IS USED FIRST, in this order, and only the last
    branch costs a call:

    1. A label that is settled before a word is read, followed for any kind, or
       judged by a taxonomy with no rule for it. Nothing is read.
    2. Words the item recorded, judged against the label's kind as it is now,
       WHEN THEY PASS OR CANNOT BE JUDGED. See below for when they would hold.
    3. A recorded answer that the catalogue had no word for the release. It
       stays not judged, on the reason it was filed with.
    4. Otherwise the release's rows are read, two provider reads, and the
       general catalogue is asked about at most three of its tracks.

    RECORDED WORDS NEVER HOLD A RELEASE ON THEIR OWN. A sweep stops asking at
    the first track whose album is the label's kind and records the words read
    so far, so a passed release's record can be one track's album. Judged
    against a kind the label was given since, that record would hold the
    release on the one track, which is the hold on a guess the gate asks up to
    three tracks to avoid. So a record that would hold sends the release to
    the fourth branch, and it is held only on what the catalogue says now.

    A RELEASE THE ITEM DOES NOT NAME is not judged and nothing is read: with no
    identifier there is nothing to read, and one that does not address this
    item would be judged on another release's tracks.
    """
    recorded = genre_gate.judge_recorded(
        declared, kind, genre_gate.recorded_genres(item.payload, genre_gate.GENRES_FIELD)
    )
    if recorded is not None and not recorded.held:
        return recorded, False
    said = item.payload.get(genre_gate.GATE_ANSWER_FIELD)
    if recorded is None and isinstance(said, str) and said in genre_gate.NO_WORD_ANSWERS:
        why = _text(item.payload.get(genre_gate.GATE_NOTE_FIELD)) or (
            genre_gate.Words((), said).why_none
        )
        return _not_judged(declared, kind, why, said), False
    if not subject.release_id:
        return _not_judged(
            declared,
            kind,
            "its review item names no release, so its tracks could not be read",
            searchers.NOT_ASKED,
        ), False
    if genre_gate.release_item_id(subject.release_id) != item.item_id:
        return _not_judged(
            declared,
            kind,
            f"its review item is not the one release {subject.release_id} is "
            f"addressed by, so it was not read",
            searchers.NOT_ASKED,
        ), False
    return _asked(job, cfg, declared, kind, subject.release_id), True


#: The payload fields that together are the gate's statement about a release.
_STAMP_FIELDS: tuple[str, ...] = (
    genre_gate.GATE_FIELD,
    genre_gate.GATE_NOTE_FIELD,
    genre_gate.GATE_ANSWER_FIELD,
    genre_gate.GENRES_FIELD,
)


def _stamp(
    store: review.ReviewStore, item: review.Item, judged: genre_gate.Judged, run_id: str
) -> None:
    """Write what the gate said onto a release that stays, when it says something new.

    ONLY ONTO AN ITEM THAT IS STILL OPEN AND STILL THERE, which
    :func:`cratekit.core.review.redescribe` checks inside its write. A release
    a person decided while this was asking keeps the payload they decided on.
    And one that left review meanwhile, withheld by another judging job, is
    not filed again beside its own hold, which is what writing through the
    sweep's ``offer_release`` did: that inserts when the row is gone.

    NOT WRITTEN WHEN NOTHING CHANGED. A release judged from its own record
    usually gets the verdict it already carries, and rewriting it would only
    move the stamp's judging job onto a release this job learned nothing about.

    THE STAMP IS ONE STATEMENT AND IS REPLACED WHOLE. A verdict with no words
    takes the old words off the item with it. Merged over them, a release
    whose record would have held it, asked about and answered with nothing,
    read not judged beside the very words the gate had just declined to hold
    it on: every later run asked about it again, and ``label approved`` held
    it on them.
    """
    said = judged.stamp()
    if all(item.payload.get(field) == said.get(field) for field in _STAMP_FIELDS):
        return
    kept = {field: value for field, value in item.payload.items() if field not in _STAMP_FIELDS}
    review.redescribe(
        store, item.item_id, {**kept, **said, genre_gate.GATE_RUN_FIELD: run_id}
    )


def _report(
    item_id: str,
    outcome: str,
    subject: _Subject,
    *,
    reason: str,
    judged: genre_gate.Judged | None = None,
    asked: bool = False,
) -> dict[str, Any]:
    return {
        "item": item_id,
        "release_id": subject.release_id,
        "label_id": subject.label_id,
        "label_name": subject.label_name,
        "title": subject.title,
        "artist": subject.artist,
        "outcome": outcome,
        "reason": reason,
        "kind": judged.kind if judged is not None else None,
        "genres": list(judged.genres) if judged is not None else [],
        "answer": judged.answer if judged is not None else None,
        "asked": asked,
    }


def _held_already(hold: review.Hold) -> _Subject:
    return _Subject(
        release_id=genre_gate.hold_release_id(hold),
        label_id=hold.group,
        label_name=hold.name,
        title=_text(hold.payload.get("title")),
        artist=_text(hold.payload.get("artist")),
    )


def _judge_one(job, item_id: str, cfg: config.Config) -> dict[str, Any]:
    run_id = str(job.job_id)
    queue = str(Queue.LABEL_RELEASE)
    # WHAT THE JOB SHARES IS READ BEFORE THE ITEM IS, so a taxonomy or a
    # registry that cannot be read stops the run on its first release whatever
    # that release turns out to be.
    tools = _tools(job)
    if tools.declared is None:
        tools.declared = active_taxonomy.load(cfg)
    if tools.followed is None:
        tools.followed = labels.RegistryStore().load()
    declared = tools.declared
    with review.open_store(cfg) as store:
        found = review.find(store, item_id)
        standing = review.find_hold(store, queue=queue, item_id=item_id)
        if found is None:
            return _left_review(item_id, standing)
        # A LABEL THE REGISTRY NO LONGER HOLDS IS THE DEFAULT KIND, which is
        # what ``label approved`` judges it as.
        entry = tools.followed.by_id(_text(found.payload.get("label_id")))
        kind = entry.kind if entry is not None else None
        subject = _subject(store, found, entry)
        if found.stored_verdict is not None:
            return _report(
                item_id, DECIDED, subject, reason="a person has decided it, so it was not judged"
            )
        if genre_gate.returned_by(standing, found.payload):
            return _report(
                item_id,
                RETURNED,
                subject,
                reason="a person returned it to review, so it was not judged again",
            )
        judged, asked = _judged(job, cfg, declared, kind, found, subject)
        if not judged.held:
            _stamp(store, found, judged, run_id)
            # IN REVIEW AND STILL HELD is a state two writes of an earlier
            # build can leave. The queue is the truth, as the sweep reads it:
            # the release is in review and the gate does not hold it, so the
            # hold goes, and ``label held`` stops listing a release a person
            # can already decide.
            if standing is not None and standing.state == review.HOLD_HELD:
                review.release_hold(store, queue=queue, item_id=item_id)
            return _report(
                item_id, judged.verdict.value, subject, reason=judged.reason, judged=judged, asked=asked
            )
        hold = review.withhold(
            store,
            item_id,
            group=subject.label_id,
            name=subject.label_name,
            reason=judged.reason,
            detail=judged.detail(),
            run_id=run_id,
        )
        if hold is not None:
            return _report(item_id, HELD, subject, reason=judged.reason, judged=judged, asked=asked)
        # NOTHING WAS MOVED, because the release changed while it was being
        # judged. It is reported as what it is NOW, read again, and never as
        # what this run meant to make of it.
        again = review.find(store, item_id)
        if again is None:
            report = _left_review(
                item_id, review.find_hold(store, queue=queue, item_id=item_id)
            )
        elif again.stored_verdict is not None:
            report = _report(
                item_id,
                DECIDED,
                subject,
                reason="a person decided it while it was being judged, so it was not held",
            )
        else:
            report = _report(
                item_id,
                RETURNED,
                subject,
                reason="a person returned it to review while it was being judged",
            )
        return {**report, "asked": asked}


def _left_review(item_id: str, standing: review.Hold | None) -> dict[str, Any]:
    """The report for a release that is not in review when it is looked for.

    HELD WHEN A HOLD IS IN FORCE ON IT, whoever made the hold. The usual way
    here is this job's own, made by a run that died before the item was marked
    done and is being redone. Another judging job's hold reads the same, and
    so does one made in the moment this job was asking about the release. NOT
    KEYED ON THE HOLD'S RUN, which is the run that FIRST held the release and
    is an earlier one's when a hold already stood beside the item.

    GONE otherwise: the release left review some other way.
    """
    if standing is not None and standing.state == review.HOLD_HELD:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
    gone = _held_already(standing) if standing is not None else _Subject("", "", "", "", "")
    return _report(item_id, GONE, gone, reason="it was no longer in review when its turn came")


def handle(job, item, cfg) -> jobs.Produced:
    """Judge ONE pending release. The per item worker behind ``label.judge``.

    THE ITEM NAMES THE REVIEW ITEM, never the payload, on the rule every worker
    in this package keeps. THE CONFIGURATION IS THE FROZEN ONE and is not
    loaded here.

    EVERY RELEASE REPORTS, whatever happened to it, because the summary is read
    from the reports and a release with none would be missing from every count.
    """
    try:
        report = _judge_one(job, str(item.item_id or ""), cfg)
    except CratekitError as exc:
        raise _parked(job, exc) from exc
    return artifacts.produced(ARTIFACTS, cfg, job, item, report)


__all__ = [
    "ARTIFACTS",
    "CATALOGUE_UNREAD",
    "DECIDED",
    "GONE",
    "HELD",
    "NOTHING_PENDING",
    "NOT_JUDGED",
    "NOT_JUDGED_LEFT",
    "OUTCOMES",
    "PASSED",
    "RETURNED",
    "build_judge",
    "handle",
    "label_judge",
    "label_judge_argv",
    "pending",
    "summary",
]
