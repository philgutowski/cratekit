"""``crate sync bandcamp``: new Bandcamp purchases taken to their landing gate in one verb (U179).

Sitting 46 took 45 releases and 96 tracks from one seller to filed in
rekordbox in about two hours and 25 messages, every step typed by hand
(``docs/plans/2026-10-27-bandcamp-lane.md``). Since U176, U177 and U178 each
step is a verb: ``acquire bandcamp`` plans the purchases, ``acquire
bandcamp-fetch`` stages the new ones tagged with their label, ``tag folder``
gives a label's files its genre, and the tail and the landing are the chain
``sync land`` runs. This verb runs them in order, as one command.

THE BANDCAMP SOURCE OF THE SAME DRIVER, NOT A SECOND DRIVER. A sibling of
``crate sync land`` rather than a flag on it, so that verb's arguments and
envelope stay its own, and like ``label sync --go`` (U190) it runs the one
chain :mod:`cratekit.cli.tail` holds: the tail in its order over the absolute
batch folder, the stale tail job replaced, ``name apply``'s confirm answered
inline and the landing stopped at its gate. The preflight is ``sync land``'s
own. Only the source differs: the plan and the fetch in place of the pass, its
intake jobs, the missing list and the download.

EACH STEP IS THE EXISTING VERB THROUGH THE REAL DISPATCHER, under its own run
with its own refusals:

1. ``preflight``: refused while rekordbox runs, or a backup's driver is live;
2. ``plan``: ``acquire bandcamp`` with the sellers. A missing, expired or
   refused session ends the verb here with its login step, before anything is
   downloaded, and the plan's rows are what the closing report names as held
   as owned and which sellers no label names;
3. ``fetch``: ``acquire bandcamp-fetch`` into the batch folder, which drives
   its own job in the foreground. A fetch into the same batch still open from
   an earlier run is driven on through its ``--job`` command rather than
   queued a second time; one open into another batch is that batch's, and the
   verb ends PENDING naming the command that continues it. A release refused
   for good is recorded and skipped, the way ``sync land`` skips a lossy
   download; a parked or transient fetch ends the verb on its own refusal;
4. the tail, ``tag folder``, ``analyze run``, ``analyze restamp`` and ``name
   apply``, any step that does not succeed ending the verb there, so no landing
   is planned over files the tail has not run on;
5. ``rehearse``: ``intake land --rehearse`` on a copy (U162), with the same
   arguments the landing then takes, so the live gate names it;
6. ``land``: ``intake land`` with the batch's name and, when any staged file
   carries a label tag, ``--label-from-tags`` (U177), stopping at its
   explicit gate on its own run.

THE NAME IS READ FROM THE FILES, ``<date> Bandcamp <Label>`` when every staged
file's label tag names one label and ``<date> Bandcamp`` otherwise
(:func:`cratekit.intake.batch_name.bandcamp`), because the label tags are what
the landing files each file under, and a batch folder continued from an
earlier run holds that run's files too.

A BATCH FOLDER IS HOW THE VERB CONTINUES. Every purchase a fetch staged is
recorded fetched, so the plan never offers it again; a run that stopped in the
tail is continued by running the verb again with the same ``--batch``, which
finds nothing new or only what is new, and takes whatever the folder holds
through the tail again. NOTHING NEW AND NOTHING STAGED ends with no download
and no landing, and says so.

IT STOPS WHERE A PERSON MUST ACT. The landing reads the backup acknowledgment,
which this verb never mints, and asks its explicit gate on its own run, so the
envelope is then PENDING naming that run, the commands that answer and apply
it as the session, and the rekordbox visit after. It never starts a backup,
never opens rekordbox, never answers a gate but ``name apply``'s inline
confirm, and never writes a beat grid. A database native intake tree only,
since the rehearsal and ``--label-from-tags`` are.
"""

from __future__ import annotations

import argparse
import dataclasses
import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from cratekit.cli import registry, sync_land, tail
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.cli.tail import (
    ACK_STOP,
    ANALYZE,
    GUESS,
    LAND,
    LAND_VERB,
    NAME,
    REHEARSE,
    REKORDBOX_STEPS,
    RESTAMP,
    TAG,
)
from cratekit.core import config, jobs, tags
from cratekit.core.cause import CratekitError, Outcome, rebuilt
from cratekit.core.exit_codes import ExitCode

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.sync_bandcamp",)

#: The key every check carries, before its step.
NAMESPACE = "sync.bandcamp"

#: The steps, in the one order the verb runs them. Each is a check key on the
#: envelope, ``sync.bandcamp.<step>``.
PREFLIGHT = sync_land.PREFLIGHT
PLAN = "plan"
FETCH = "fetch"
STEPS: tuple[str, ...] = (
    PREFLIGHT, PLAN, FETCH, TAG, GUESS, ANALYZE, RESTAMP, NAME, REHEARSE, LAND,
)

#: The report row the staged files' tags are read into, after the tail.
TAGS = "tags"

#: The verbs the source runs, ahead of the shared tail.
PLAN_VERB = "acquire.bandcamp"
FETCH_VERB = "acquire.bandcamp-fetch"

#: The plan's dispositions this verb reads (``acquire.bandcamp_cli.Disposition``),
#: spelled here since this module imports no feature module at its top.
OWNED = "owned"
HELD = "held"

#: The warnings the closing report carries.
NO_GENRE = "sync-bandcamp-no-genre"
TAGS_UNREAD = "sync-bandcamp-tags-unread"
FETCH_REFUSED = "sync-bandcamp-fetch-refused"

#: The landing's flag that files each file under its own label tag (U177).
LABEL_FROM_TAGS = "--label-from-tags"


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument(
        "--seller",
        action="append",
        default=None,
        metavar="NAME",
        help=(
            "only this seller's purchases, by the account name in its address "
            "(NAME.bandcamp.com) or a registered label's name; repeat it for several"
        ),
    )
    parser.add_argument(
        "--batch",
        default=None,
        metavar="NAME",
        help=(
            "the batch folder under download staging to fetch into and land from "
            "('Bandcamp <today's date>' when omitted); name it again to continue a "
            "run that stopped, since whatever it holds is taken through the tail"
        ),
    )
    parser.set_defaults(_handler=sync_bandcamp)


def _sellers(named: Sequence[str] | None) -> list[str]:
    return [word for name in named or () for word in ("--seller", name)]


def again_command(batch: str, sellers: Sequence[str] | None) -> str:
    """The command that continues a run over ``batch``, as a person types it."""
    return shlex.join(["crate", "sync", "bandcamp", "--batch", batch, *_sellers(sellers)])


def _report(progress: Callable[[str], None] | None, again: str) -> tail.Chain:
    """The verb's record: the shared chain's, keyed ``sync.bandcamp`` and counting all nine steps."""
    return tail.Chain(
        progress=progress,
        namespace=NAMESPACE,
        title="sync bandcamp",
        steps=STEPS,
        origin=_ORIGIN,
        again=f"run it again: {again}",
        summary={
            "batch": None,
            "steps": [],
            "commands": [],
            "stopped_at": None,
            "replaced": [],
            "labels": {},
            "sellers_unregistered": [],
            "owned": [],
            "held": [],
            "fetch_jobs": [],
            "fetched": [],
            "fetched_items": [],
            "fetch_refused": [],
            "staged": [],
            "no_genre": [],
            "no_label": [],
            "tags_unread": [],
            "landing_name": None,
        },
    )


def _summary_of(envelope: dict[str, Any]) -> dict[str, Any]:
    data = envelope.get("data") or {}
    summary = data.get("summary") if isinstance(data, dict) else None
    return summary if isinstance(summary, dict) else {}


def _release(row: Mapping[str, Any]) -> str:
    return f"{row.get('artist', '')} - {row.get('title', '')} ({row.get('seller', '')})"


# ---------------------------------------------------------------------------
# Step 1: the plan
# ---------------------------------------------------------------------------


def _plan(report: tail.Chain, sellers: Sequence[str] | None) -> bool:
    """Plan the purchases; True when the plan has something to fetch.

    The plan's own refusal ends the verb, a session that is missing, expired or
    refused above all, so nothing is downloaded over an account nobody could
    read. What it holds back as owned is kept for the closing report, with the
    library files each owned track resolved to.
    """
    envelope = tail.required(report, PLAN, ["acquire", "bandcamp", *_sellers(sellers)])
    summary = _summary_of(envelope)
    for row in summary.get("rows") or ():
        if not isinstance(row, dict):
            continue
        kept = [
            {
                "track": f"{one.get('artist') or row.get('artist', '')} - {one.get('title', '')}",
                "paths": list(one.get("paths") or ()),
            }
            for one in row.get("held") or ()
            if isinstance(one, dict)
        ]
        entry = {
            "item_id": row.get("item_id"),
            "release": _release(row),
            "tracks": kept,
        }
        if row.get("disposition") == OWNED:
            report.summary["owned"].append(entry)
        elif row.get("disposition") == HELD:
            report.summary["held"].append(entry)
    report.summary["labels"] = dict(summary.get("labels") or {})
    report.summary["sellers_unregistered"] = list(summary.get("sellers_unregistered") or ())
    to_fetch = int(summary.get("new") or 0) + int(summary.get("held") or 0)
    if envelope.get("outcome") == str(Outcome.NO_OP) or not to_fetch:
        report.check(
            PLAN,
            "info",
            f"the account has nothing new to fetch ({summary.get('purchases', 0)} "
            f"purchase(s), {summary.get('owned', 0)} owned, {summary.get('fetched', 0)} "
            f"fetched before)",
        )
        return False
    report.check(
        PLAN,
        "ok",
        f"{to_fetch} purchase(s) to fetch of {summary.get('purchases', 0)}, "
        f"{summary.get('owned', 0)} owned, {len(report.summary['held'])} with "
        f"tracks held back as owned",
    )
    return True


# ---------------------------------------------------------------------------
# Step 2: the fetch
# ---------------------------------------------------------------------------


class _Elsewhere(Exception):
    """A fetch into another batch folder is still open, and it is that batch's to finish."""

    def __init__(self, job: jobs.Job, batch: str) -> None:
        super().__init__(job.job_id)
        self.job = job
        self.batch = batch


def _fetch_jobs(cfg: config.Config) -> list[jobs.Job]:
    """Every Bandcamp fetch of this library, newest first."""
    key = registry.entry(FETCH_VERB).handler_key
    with jobs.open_store() as store:
        return [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == key and job.library_id == cfg.library.volume_id
        ]


def _batch_of(job: jobs.Job) -> str:
    from cratekit.acquire import bandcamp_cli  # noqa: PLC0415 - one module's payload key

    return str((job.payload or {}).get(bandcamp_cli.BATCH) or "")


def _open_fetch(cfg: config.Config, batch: str) -> list[jobs.Job]:
    """Every open fetch into ``batch``, oldest first; one into another batch is raised.

    A FETCH LEFT OPEN HOLDS ITS PURCHASES UNRECORDED, so the plan offers them
    again and a second fetch would download them a second time. Each one into
    this batch is driven on, every one and not only the newest, so none is
    left open and unnamed behind a run that reached its gate; one into
    another batch is named, since which batch a person continues is theirs
    to say.
    """
    held = [job for job in _fetch_jobs(cfg) if job.is_open()]
    for job in held:
        if _batch_of(job) != batch:
            raise _Elsewhere(job, _batch_of(job))
    return list(reversed(held))


def _fetched(report: tail.Chain, job: jobs.Job) -> None:
    """Read a settled fetch: what it staged, and what it refused for good and skipped.

    A RELEASE REFUSED FOR GOOD IS RECORDED AND SKIPPED, a lossy only offer
    above all, and the rest go on to the tail. A fetch still open, parked or
    failed with anything a retry could mend ends the verb on its own refusal,
    since what it holds is still coming.
    """
    from cratekit.acquire import bandcamp_cli  # noqa: PLC0415 - one module's payload key

    with jobs.open_store() as store:
        held = jobs.items(store, job.job_id)
    releases = (job.payload or {}).get(bandcamp_cli.RELEASES) or {}

    def named(item: jobs.Item) -> str:
        frozen = releases.get(item.item_id)
        return _release(frozen) if isinstance(frozen, Mapping) else item.item_id

    done = [item for item in held if item.state is jobs.ItemState.DONE]
    failed = [item for item in held if item.state is jobs.ItemState.FAILED]
    permanent = [item for item in failed if item.cause is not None and not item.cause.retryable]
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
    report.summary["fetch_jobs"].append(job.job_id)
    if job.state is not jobs.JobState.SUCCEEDED and not settled_with_refusals:
        raise tail.Stop(FETCH, tail.job_error(report, job))
    # ONE RELEASE IS COUNTED ONCE ACROSS THE RUN'S FETCHES. Two fetches left
    # open into one batch can hold the same purchase, and the second finds it
    # in the record and ends its item done without staging anything, so a
    # release an earlier fetch of this run already staged is not staged again
    # here, and one refused before and staged now is no longer refused.
    seen = set(report.summary["fetched_items"])
    staged = [item for item in done if item.item_id not in seen]
    report.summary["fetched_items"].extend(item.item_id for item in staged)
    report.summary["fetched"].extend(named(item) for item in staged)
    taken = set(report.summary["fetched_items"])
    already = {row["item_id"] for row in report.summary["fetch_refused"]}
    refused = [
        {
            "item_id": item.item_id,
            "release": named(item),
            "reason": item.cause.reason if item.cause else None,
            "message": item.cause.message if item.cause else None,
        }
        # THE FETCH NEVER SKIPS AN ITEM, unlike ``acquire download`` since U169:
        # a release it refuses fails for good, so the failed items are all.
        for item in permanent
        if item.item_id not in taken and item.item_id not in already
    ]
    report.summary["fetch_refused"] = [
        row for row in report.summary["fetch_refused"] if row["item_id"] not in taken
    ] + refused
    report.check(
        FETCH,
        "fail" if permanent and not done else "ok",
        f"fetch job {job.job_id} staged {len(staged)} release(s)"
        + (f", {len(done) - len(staged)} already staged by this run" if len(done) > len(staged) else "")
        + (f"; {len(permanent)} refused and skipped" if permanent else ""),
    )


def _warn_refused(report: tail.Chain) -> None:
    """The one warning naming every release the run's fetches refused, said once."""
    refused = report.summary["fetch_refused"]
    if refused:
        report.warnings.append(
            {
                "code": FETCH_REFUSED,
                "message": (
                    f"{len(refused)} release(s) were refused by the fetch and are skipped: "
                    + "; ".join(f"{row['release']} ({row['reason']})" for row in refused)
                ),
            }
        )


def _drive_open(report: tail.Chain, cfg: config.Config, batch: str) -> None:
    """Drive on a fetch into the batch an earlier run left open, before anything is planned.

    Before the plan, because what it fetches is recorded as it goes, and a
    plan asked first would offer those purchases again.
    """
    for held in _open_fetch(cfg, batch):
        report.check(FETCH, "info", f"driving on the fetch {held.job_id} left open into {batch}")
        _fetched(report, tail.settle(report, FETCH, held))


def _fetch(report: tail.Chain, cfg: config.Config, batch: str, sellers: Sequence[str] | None) -> None:
    """Fetch what the plan found new into the batch, the fetch driving its own job."""
    before = {job.job_id for job in _fetch_jobs(cfg)}
    argv = ["acquire", "bandcamp-fetch", "--batch", batch, *_sellers(sellers)]
    code, envelope = report.call(FETCH, argv)
    queued = [job for job in _fetch_jobs(cfg) if job.job_id not in before]
    if not queued:
        if tail.succeeded(code, envelope):
            report.check(FETCH, "info", "the fetch found nothing new to stage")
            return
        raise tail.Stop.of(FETCH, tail.cause_of(report, FETCH, argv, code, envelope))
    job = queued[0]
    if job.is_open() and job.state is not jobs.JobState.BLOCKED:
        job = tail.settle(report, FETCH, job)
    _fetched(report, job)


# ---------------------------------------------------------------------------
# After the tail: what the staged files say
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class _Read:
    labels: tuple[str | None, ...]


def _read_tags(report: tail.Chain, files: Sequence[Path]) -> _Read:
    """Each staged file's genre and label, read after the tail.

    UNREAD IS NOT NONE. A file whose tags could not be read is named apart,
    never counted as a file with no genre, and its label is taken as none, so
    the batch is not named for a label nobody could read.
    """
    labels: list[str | None] = []
    for path in files:
        try:
            read = tags.read_tags_checked(path, ("genre", "label"))
        except tags.TagReadFailed:
            report.summary["tags_unread"].append(path.name)
            labels.append(None)
            continue
        if not (read.get("genre") or "").strip():
            report.summary["no_genre"].append(path.name)
        label = (read.get("label") or "").strip() or None
        if label is None:
            report.summary["no_label"].append(path.name)
        labels.append(label)
    no_genre, unread = report.summary["no_genre"], report.summary["tags_unread"]
    if no_genre:
        report.warnings.append(
            {
                "code": NO_GENRE,
                "message": (
                    f"{len(no_genre)} staged file(s) have no genre after the tail and "
                    f"will wait in INBOX to be sorted: " + ", ".join(no_genre)
                ),
            }
        )
    if unread:
        report.warnings.append(
            {
                "code": TAGS_UNREAD,
                "message": (
                    f"{len(unread)} staged file(s) could not have their tags read, so "
                    f"their genre and label are unknown: " + ", ".join(unread)
                ),
            }
        )
    report.check(
        TAGS,
        "warn" if no_genre or unread else "ok",
        f"{len(files)} staged file(s): {len(no_genre)} with no genre, "
        f"{len(report.summary['no_label'])} with no label tag, {len(unread)} unread",
    )
    return _Read(labels=tuple(labels))


def _landing(cfg: config.Config, read: _Read) -> list[str]:
    """The landing's arguments after the folder: the batch's name, and the label flag."""
    from cratekit.intake import batch_name  # noqa: PLC0415 - one module's naming rule

    name = batch_name.bandcamp(cfg, read.labels)
    argv = ["--name", name]
    if any(read.labels):
        argv.append(LABEL_FROM_TAGS)
    return argv


def _staged(folder: Path) -> tuple[Path, ...]:
    from cratekit.intake import landing  # noqa: PLC0415 - the landing's own listing

    return landing.listing(folder) if folder.is_dir() else ()


# ---------------------------------------------------------------------------
# Where it stops
# ---------------------------------------------------------------------------


def _attended(ctx: Context, report: tail.Chain, stop: tail.Attend, again: str) -> Envelope:
    """The PENDING envelope the verb ends on when a step waits for a person."""
    if stop.step == REHEARSE and stop.cause.reason != ACK_STOP:
        # A REHEARSAL STOPPED ON ANY OTHER GATE CODE, a stale one above all, is
        # run again by the step's own words; the landing it is for follows.
        after = (
            "then plan the landing: crate "
            + shlex.join(word for word in stop.argv if word != tail.REHEARSE_FLAG),
            "it stops at its own gate: answer it as the session with crate run "
            "decide, then apply it with --run, as its output names",
            *REKORDBOX_STEPS,
        )
    elif stop.step in (LAND, REHEARSE):
        after = REKORDBOX_STEPS
    else:
        after = (f"then continue: {again}",)
    said = tail.attended(report, stop, after=after)
    summary = "the batch " + said.summary
    if stop.step == LAND:
        summary = "the batch is fetched, tagged, analysed, named and rehearsed; " + summary
    pending = PendingHumanAction(
        kind=said.kind,
        id=f"sync-bandcamp-{ctx.run.run_id}",
        summary=summary,
        verify_verb=LAND_VERB if stop.step in (LAND, REHEARSE) else ctx.entry.name,
        steps=said.steps,
    )
    return ctx.envelope(
        data=report.data(),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=report.warnings,
    )


def _elsewhere(ctx: Context, report: tail.Chain, held: _Elsewhere, sellers) -> Envelope:
    """The PENDING envelope when a fetch into another batch is still open."""
    report.summary["stopped_at"] = FETCH
    report.summary["open_fetch"] = {"job_id": held.job.job_id, "batch": held.batch}
    step = f"continue that batch first: {again_command(held.batch, sellers)}"
    report.check(
        FETCH,
        "info",
        f"the fetch {held.job.job_id} into {held.batch} is still {held.job.state}, and "
        f"its purchases would be fetched twice by a second one",
    )
    report.summary["attended"] = [step]
    pending = PendingHumanAction(
        kind="external_step",
        id=f"sync-bandcamp-{ctx.run.run_id}",
        summary=(
            f"a Bandcamp fetch into {held.batch} is still open; continue that batch "
            f"before fetching into another"
        ),
        verify_verb=ctx.entry.name,
        steps=(step,),
    )
    return ctx.envelope(
        data=report.data(),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=report.warnings,
    )


def _ended(report: tail.Chain, stop: tail.Stop, again: str) -> CratekitError:
    """The refusal a stopped run ends with: the step's own, the run in its detail."""
    cause = stop.error.cause
    report.summary["stopped_at"] = stop.step
    remedy = cause.remediation.remedy
    report.check(stop.step, "fail", cause.message, remedy=str(remedy) if remedy else None)
    steps = cause.remediation.steps
    if stop.continues and stop.step != PLAN:
        steps = (
            *steps,
            f"what was fetched is kept in its batch folder; continue with: {again}",
        )
    return rebuilt(
        stop.error,
        dataclasses.replace(
            cause,
            remediation=dataclasses.replace(cause.remediation, steps=steps),
            detail={**dict(cause.detail or {}), "sync_bandcamp": report.data()},
        ),
    )


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def _batch(given: str | None) -> str:
    from cratekit.acquire import bandcamp_cli  # noqa: PLC0415 - the fetch's own rule

    return bandcamp_cli.staging_batch(given)


def sync_bandcamp(ctx: Context) -> Envelope:
    """Take new Bandcamp purchases to their landing gate. See the module docstring."""
    cfg = tail.load_config(_ORIGIN)
    sellers = ctx.args.seller
    batch = _batch(ctx.args.batch)
    again = again_command(batch, sellers)
    report = _report(ctx.progress, again)
    report.summary["batch"] = batch
    sync_land.preflight(report, cfg)
    folder = (cfg.paths.download_staging.expanduser() / batch).absolute()
    try:
        _drive_open(report, cfg, batch)
        planned = _plan(report, sellers)
        if planned:
            _fetch(report, cfg, batch, sellers)
        _warn_refused(report)
        files = _staged(folder)
        if not files:
            report.check(
                FETCH,
                "info",
                f"nothing is staged in {folder}, so nothing is tagged or landed",
            )
            raise tail.Done(FETCH)
        if not planned:
            report.check(
                FETCH,
                "info",
                f"taking on the {len(files)} file(s) already staged in {folder}",
            )
        folder = tail.through_name(report, folder, cfg)
        files = _staged(folder)
        report.summary["staged"] = [path.name for path in files]
        landing = _landing(cfg, _read_tags(report, files))
        report.summary["landing_name"] = landing[1]
        tail.rehearse(report, folder, landing)
        tail.land(report, folder, landing)
    except tail.Done as done:
        report.summary["stopped_at"] = done.step
    except tail.Attend as stop:
        return _attended(ctx, report, stop, again)
    except _Elsewhere as held:
        return _elsewhere(ctx, report, held, sellers)
    except tail.Stop as stop:
        raise _ended(report, stop, again) from None
    return ctx.envelope(data=report.data(), outcome=Outcome.NO_OP, warnings=report.warnings)


__all__ = [
    "FETCH",
    "FETCH_REFUSED",
    "FETCH_VERB",
    "LABEL_FROM_TAGS",
    "NAMESPACE",
    "NO_GENRE",
    "PLAN",
    "PLAN_VERB",
    "STEPS",
    "TAGS",
    "TAGS_UNREAD",
    "again_command",
    "build",
    "sync_bandcamp",
]
