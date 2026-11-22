"""``label.judge``: judge the label releases already waiting in review (R-815).

A release in review holds a place in its label's offer window, so a sweep
never asks the gate about it. This verb judges the pending releases with the
sweep's own rule, :meth:`cratekit.label.gate.SweepGate.judge_as`, using what
the item records before asking (:func:`_judged`), and moves the ones the gate
would not have filed into a hold in one transaction, not rejected:
``crate label held return`` files one again. A release passed or not judged
stays in review saying so. A decided or returned release is never touched.

IT IS A JOB, ONE ITEM PER PENDING RELEASE, so a long pass resumes where it
stopped and the item in flight when a run died is redone safely. A catalogue
that refuses, or an outage at the gate's bound, parks the run (:func:`_asked`).

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config, jobs, review, routing
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Queue
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import Taxonomy
from cratekit.label import catalogue, review_common, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.tagging import published, searchers, shell

ORIGIN = ("label", "judge_cli")

#: Where one release's report is staged and committed, under the queue root.
ARTIFACTS = jobs.Artifacts(final="label-judge-artifacts", staging="label-judge-staging")

#: What happened to one release: the gate's three verdicts in its own words, then
#: three releases the gate was not asked about (returned, decided, gone).
HELD = KindVerdict.HOLD.value
PASSED = KindVerdict.PASS.value
NOT_JUDGED = KindVerdict.NOT_JUDGED.value
RETURNED = genre_gate.RETURNED
DECIDED = "decided"
GONE = "gone"
OUTCOMES: tuple[str, ...] = (HELD, PASSED, NOT_JUDGED, RETURNED, DECIDED, GONE)

#: The warning codes a finished run can carry: it did what it could.
NOT_JUDGED_LEFT = "label-judge-not-judged"
CATALOGUE_UNREAD = "label-judge-catalogue-unread"
NOTHING_PENDING = "label-judge-nothing-pending"


def build_judge(parser, entry) -> None:
    parser.add_argument(
        "--job", default=None, metavar="JOB_ID",
        help="continue the judging job already queued under this identifier",
    )
    parser.add_argument(
        "--label", action="append", dest="labels", default=None, metavar="NAME",
        help=(
            "judge only the pending releases of this followed label; repeat it "
            "for several. Without it every pending label release is judged"
        ),
    )
    parser.set_defaults(_handler=label_judge)


def label_judge_argv(job) -> list[str]:
    """The command line that continues one queued judging job."""
    return ["label", "judge", "--job", job.job_id]


@dataclass(frozen=True, slots=True)
class _Scope:
    """The followed labels a run is narrowed to, and the registry that names them."""

    label_ids: tuple[str, ...]
    followed: labels.Registry

    def holds(self, label_id: str) -> bool:
        """Whether a release filed under ``label_id`` is one of the labels named.

        Through the registry, whose ``by_id`` follows a moved identifier, so a
        release filed under a label's old one stays in a run scoped to it.
        """
        entry = self.followed.by_id(label_id) if label_id else None
        return entry is not None and entry.label_id in self.label_ids


def _scope(names: Sequence[str] | None) -> _Scope | None:
    """The followed labels ``--label`` names, or None when it names none.

    Every name is resolved before anything is queued, so a mistyped label
    refuses rather than reading as "that label has nothing pending".
    """
    wanted = review_common.wanted(names)
    if not wanted:
        return None
    followed = labels.RegistryStore().load()
    resolved = [(name, followed.resolve(name)) for name in wanted]
    unknown = [name for name, entry in resolved if entry is None]
    if unknown:
        raise refuse(
            "label-unknown",
            f"no followed label is named {review_common.quoted(unknown)}, "
            f"so there is nothing of it to judge; nothing was queued",
            steps=("take the name from: crate label registry list",),
            origin=ORIGIN,
            detail={"unknown": unknown},
        )
    return _Scope(tuple(dict.fromkeys(entry.label_id for _name, entry in resolved)), followed)


def pending(store: review.ReviewStore, scope: _Scope | None = None) -> tuple[str, ...]:
    """The review items a judging job is made of: every open label release.

    Read off the review queue alone, so queueing asks no provider. ``scope``
    narrows it to the labels named.
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
    # The declaration before anything is queued: an unreadable taxonomy
    # refuses here, not once per release in a detached child.
    active_taxonomy.load(cfg)
    with review.open_store(cfg) as queue:
        items = pending(queue, scope)
    if not items:
        # The honest zero: a job with no items drives straight to succeeded.
        named = " for the labels named" if scope is not None else ""
        return ctx.envelope(
            data=shell.no_op("no-op"),
            outcome=Outcome.NO_OP,
            warnings=({"code": NOTHING_PENDING, "message": (
                f"no label release is waiting in review{named}, so there is nothing to judge"
            )},),
        )
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=ctx.entry.handler_key, item_ids=items, cfg=cfg,
            payload={"labels": list(scope.label_ids) if scope is not None else []},
        )
        return ctx.envelope(data=shell.reported(store, job), warnings=label_cli.queue_warnings())


def _counts() -> dict[str, int]:
    return {"judged": 0, **dict.fromkeys(OUTCOMES, 0), "asked": 0, "unread": 0}


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this job's committed reports say happened, per label and in total.

    Derived from what ran, so true across a resume. ``judged`` is held plus
    passed, ``asked`` the releases the provider was asked for, answered or
    not, ``unread`` the ones the general catalogue could not be read for.
    """
    totals = _counts()
    rows: dict[str, dict[str, Any]] = {}
    for report in ARTIFACTS.committed(cfg, job_id):
        outcome = str(report.get("outcome") or "")
        if outcome not in OUTCOMES:
            continue
        label_id = str(report.get("label_id") or "")
        name = str(report.get("label_name") or "")
        row = rows.setdefault(label_id, {"label_id": label_id, "label_name": name, **_counts()})
        for counted in (totals, row):
            counted[outcome] += 1
            if outcome in (HELD, PASSED):
                counted["judged"] += 1
            if report.get("asked"):
                counted["asked"] += 1
            if report.get("answer") in published.UNREAD:
                counted["unread"] += 1
    by_name = sorted(
        rows.values(), key=lambda row: str(row["label_name"] or row["label_id"]).casefold()
    )
    return {**totals, "labels": by_name}


def _warnings(counted: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    found: list[dict[str, str]] = []
    if counted["unread"]:
        found.append({"code": CATALOGUE_UNREAD, "message": (
            f"the general catalogue could not be read for {counted['unread']} "
            f"release(s); they stay in review marked not judged, and another "
            f"run of crate label judge asks about them again"
        )})
    if counted[NOT_JUDGED]:
        found.append({"code": NOT_JUDGED_LEFT, "message": (
            f"{counted[NOT_JUDGED]} release(s) stay in review not judged; "
            f"each says why in: crate review list --queue {Queue.LABEL_RELEASE}"
        )})
    return tuple(found)


def _left(store, job_id: str) -> int:
    """How many of the job's releases no run has finished."""
    counts = jobs.progress(store, job_id)["counts"]
    settled = (str(jobs.ItemState.DONE), str(jobs.ItemState.SKIPPED))
    return sum(n for state, n in counts.items() if state not in settled)


def _with_summary(error: CratekitError, cfg: config.Config, store, job_id: str) -> CratekitError:
    """The same refusal, carrying what the run did and how much it left.

    A run that parked, failed or was stopped leaves through its cause, and is
    the run a person most needs the counts from.
    """
    left = _left(store, job_id)
    # A parked job is open and this verb drives it; only ``job resume``
    # re-arms one that failed or was stopped.
    how = (
        f"crate label judge --job {job_id}"
        if jobs.get(store, job_id).is_open()
        else f"crate job resume {job_id}, then read what it did with: "
        f"crate label judge --job {job_id}"
    )
    step = f"{left} release(s) of this job are not judged yet; continue with: {how}"
    return review_common.extended(error, step, judging=summary(cfg, job_id), left=left)


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Continue the judging job named on ``--job``, and report what it did."""
    with jobs.open_store() as store:
        queued = jobs.get(store, ctx.args.job)
        # The job has to be this verb's: the worker is resolved from the job
        # row, so any other verb's job would run under this verb's envelope.
        if queued.handler_key != ctx.entry.handler_key:
            raise refuse(
                "job-unknown",
                f"job {queued.job_id} was queued for {queued.handler_key!r}, which "
                f"is not a judging job, so this verb will not drive it",
                steps=(
                    f"resume it through its own verb, or with: crate job resume {queued.job_id}",
                ),
                origin=ORIGIN,
                detail={"job_id": queued.job_id, "handler": queued.handler_key},
            )
        try:
            job, warnings = shell.advance(
                ctx, store, queued, origin=ORIGIN,
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


@dataclass
class _Tools:
    """What one job's items share, each made on first use and kept for the job.

    ``asking`` and ``reader`` carry counts of failures in a row across releases;
    ``refused`` is the catalogue's refusal once given.
    """

    asking: genre_gate.Asking
    reader: catalogue.ReleaseTracks | None = None
    refused: str | None = None
    declared: Taxonomy | None = None
    followed: labels.Registry | None = None


#: The tools of the one job being driven, keyed by the job, on the reasoning
#: ``label.cli._JOB_ASKING`` gives; unlike that holder, dropped when the run parks.
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

    Every refusal here stops the run and none fails the item, since every later
    release would meet it too. The tools are dropped so a resume asks afresh.
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


_text = review_common.text


def _subject(
    store: review.ReviewStore, item: review.Item, entry: labels.LabelEntry | None
) -> _Subject:
    """The release an item names, and the label it is counted and held under.

    The label is the registry's when the registry holds it, since a sweep asks
    for holds under the identifier a label has now; a label nobody follows any
    more keeps what the item says.
    """
    label_id, name = _text(item.payload.get("label_id")), _text(item.payload.get("label_name"))
    if entry is not None:
        label_id, name = entry.label_id, entry.name
    return _Subject(genre_gate.release_id_of(store, item), label_id, name, *_titled(item.payload))


def _titled(payload: Mapping[str, Any]) -> tuple[str, str]:
    return _text(payload.get("title")), _text(payload.get("artist"))


def _not_judged(declared: Taxonomy, kind: str | None, why: str, answer: str) -> genre_gate.Judged:
    return genre_gate.Judged(
        KindVerdict.NOT_JUDGED, routing.label_kind(declared, kind), (), why, answer
    )


_WAIT = ("wait before continuing: nothing here tries to get past a catalogue that refuses",)


def _asked(
    job, cfg: config.Config, declared: Taxonomy, kind: str | None, release_id: str
) -> genre_gate.Judged:
    """Read the release's rows and ask the general catalogue. The one costly branch.

    It refuses, parking the run, before a read it knows is wasted: the catalogue
    refused once, went unread for the gate's bound in a row, or the provider
    failed its own bound. Nothing here retries or waits.
    """
    tools = _tools(job)
    if tools.refused is not None:
        raise refuse(
            "catalogue-unreachable",
            f"the general catalogue refused ({tools.refused}), so the run stopped "
            f"asking it. The release it refused stays in review marked not "
            f"judged, and the next one was not read from the provider",
            steps=_WAIT,
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
            steps=_WAIT,
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
    job, cfg: config.Config, declared: Taxonomy, kind: str | None, item: review.Item,
    subject: _Subject,
) -> tuple[genre_gate.Judged, bool]:
    """The gate's verdict on one pending release, and whether the provider was read.

    What the item records is used first, and only the last branch costs a call:
    a label settled before a word is read; recorded words, when they pass or
    cannot be judged; a recorded answer that the catalogue had no word; else
    the release's rows are read and the general catalogue asked.

    RECORDED WORDS NEVER HOLD A RELEASE ON THEIR OWN: a passed release's record
    can be one track's album, so a record that would hold is asked about again
    and held only on what the catalogue says now. A release the item does not
    name, or names another item's, is not judged and nothing is read.
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
        why = "its review item names no release, so its tracks could not be read"
    elif genre_gate.release_item_id(subject.release_id) != item.item_id:
        why = (
            f"its review item is not the one release {subject.release_id} is "
            f"addressed by, so it was not read"
        )
    else:
        return _asked(job, cfg, declared, kind, subject.release_id), True
    return _not_judged(declared, kind, why, searchers.NOT_ASKED), False


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

    Only onto an item still open, on its payload as it stands at the write
    (:func:`cratekit.core.review.redescribe`), so another writer's field is kept
    (R-840). The stamp is replaced whole: no words takes the old words off.
    """
    said = judged.stamp()

    def stamped(current: dict[str, Any]) -> dict[str, Any] | None:
        if all(current.get(field) == said.get(field) for field in _STAMP_FIELDS):
            return None
        kept = {field: value for field, value in current.items() if field not in _STAMP_FIELDS}
        return {**kept, **said, genre_gate.GATE_RUN_FIELD: run_id}

    review.redescribe(store, item.item_id, stamped)


def _report(
    item_id: str, outcome: str, subject: _Subject, *, reason: str,
    judged: genre_gate.Judged | None = None, asked: bool = False,
) -> dict[str, Any]:
    return {
        "item": item_id,
        **asdict(subject),
        "outcome": outcome,
        "reason": reason,
        "kind": judged.kind if judged is not None else None,
        "genres": list(judged.genres) if judged is not None else [],
        "answer": judged.answer if judged is not None else None,
        "asked": asked,
    }


def _held_already(hold: review.Hold) -> _Subject:
    return _Subject(genre_gate.hold_release_id(hold), hold.group, hold.name, *_titled(hold.payload))


def _judge_one(job, item_id: str, cfg: config.Config) -> dict[str, Any]:
    run_id = str(job.job_id)
    queue = str(Queue.LABEL_RELEASE)
    # What the job shares is read before the item, so an unreadable taxonomy
    # or registry stops the run on its first release.
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
        # A label the registry no longer holds is the default kind, as in
        # ``label approved``.
        entry = tools.followed.by_id(_text(found.payload.get("label_id")))
        kind = entry.kind if entry is not None else None
        subject = _subject(store, found, entry)
        if found.stored_verdict is not None:
            return _report(
                item_id, DECIDED, subject, reason="a person has decided it, so it was not judged"
            )
        if genre_gate.returned_by(standing, found.payload):
            return _report(
                item_id, RETURNED, subject,
                reason="a person returned it to review, so it was not judged again",
            )
        judged, asked = _judged(job, cfg, declared, kind, found, subject)
        if not judged.held:
            _stamp(store, found, judged, run_id)
            # In review and still held, which an earlier build can leave: the
            # queue is the truth, so the hold goes.
            if standing is not None and standing.state == review.HOLD_HELD:
                review.release_hold(store, queue=queue, item_id=item_id)
            outcome = judged.verdict.value
        else:
            hold = review.withhold(
                store, item_id, group=subject.label_id, name=subject.label_name,
                reason=judged.reason, detail=judged.detail(), run_id=run_id,
            )
            if hold is None:
                return _changed(store, item_id, subject, asked)
            outcome = HELD
        return _report(item_id, outcome, subject, reason=judged.reason, judged=judged, asked=asked)


def _changed(
    store: review.ReviewStore, item_id: str, subject: _Subject, asked: bool
) -> dict[str, Any]:
    """A release that changed while it was judged, so nothing was moved: as it is now."""
    again = review.find(store, item_id)
    if again is None:
        report = _left_review(
            item_id, review.find_hold(store, queue=str(Queue.LABEL_RELEASE), item_id=item_id)
        )
    elif again.stored_verdict is not None:
        why = "a person decided it while it was being judged, so it was not held"
        report = _report(item_id, DECIDED, subject, reason=why)
    else:
        why = "a person returned it to review while it was being judged"
        report = _report(item_id, RETURNED, subject, reason=why)
    return {**report, "asked": asked}


def _left_review(item_id: str, standing: review.Hold | None) -> dict[str, Any]:
    """The report for a release that is not in review when it is looked for.

    Held when a hold is in force on it, whoever made it (usually this job's
    own, redone after a run died), never keyed on the hold's run, which is the
    run that first held it. Gone otherwise.
    """
    if standing is not None and standing.state == review.HOLD_HELD:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
    gone = _held_already(standing) if standing is not None else _Subject("", "", "", "", "")
    return _report(item_id, GONE, gone, reason="it was no longer in review when its turn came")


def handle(job, item, cfg) -> jobs.Produced:
    """Judge ONE pending release. The per item worker behind ``label.judge``.

    The item names the review item, and the configuration is the frozen one.
    Every release reports, because the summary is read from the reports.
    """
    try:
        report = _judge_one(job, str(item.item_id or ""), cfg)
    except CratekitError as exc:
        raise _parked(job, exc) from exc
    return ARTIFACTS.produced(cfg, job, item, report)


__all__ = [
    "ARTIFACTS", "CATALOGUE_UNREAD", "DECIDED", "GONE", "HELD", "NOTHING_PENDING", "NOT_JUDGED",
    "NOT_JUDGED_LEFT", "OUTCOMES", "PASSED", "RETURNED", "build_judge", "handle", "label_judge",
    "label_judge_argv", "pending", "summary",
]
