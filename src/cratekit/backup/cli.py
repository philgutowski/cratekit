"""``crate backup run``: back the library up, and publish the age R15's warning reads.

The engine, :mod:`cratekit.modules.tools.backup`, publishes each portion's age
itself through ``backup_facts.record``; this shell never writes it, because a
second writer of one fact can disagree with the first. What the shell owns is
reading the age back (:func:`published_ages`) from the same file a destructive
session reads, and turning a run in which nothing was backed up into a refusal
(:func:`refusal_for`). Reports are built from the outcome, never from the plan.

The verb declares no gate: the run only adds a mirror and a dated archive, and
its one deletion, the archive prune, runs only after its mirror succeeded.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23). Layer: modules.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Any, NoReturn

# Aliased: ``cratekit.cli.exit_codes`` is the reserved-cause table a refusal's
# remediation is looked up in, not ``cratekit.core.exit_codes``.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope, load_config
from cratekit.core import backup_facts, config, jobs
from cratekit.core.cause import Cause, CratekitError, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import backup

#: Payload keys this build freezes. Named once so the handler and the argv
#: builder cannot drift: a resume that lost one would do different work from
#: the run it continues.
DRY_RUN = "dry_run"
FULL = "full"
CHECK = "check"
EMPTIED = "library_emptied"

#: The advisory saying which kind of run a backup was (U317).
KIND = "backup-kind"

#: The advisory saying what the file comparison did (R-757). A warning because
#: the default renderer prints warnings and nothing of the payload.
COMPARISON = "backup-comparison"

#: The warning a second ``backup run`` carries when it reports the open job in
#: place of filing another (R-223).
ALREADY_QUEUED = "backup-already-queued"

#: The warning every branch of a rehearsal carries (R-221).
REHEARSAL = "backup-rehearsal"

#: The ``progress`` key carrying each item's recorded outcome (R-349), named in
#: core because ``job show`` renders it without importing this module.
OUTCOMES = backup_facts.OUTCOMES_FIELD


def _engine_refusal(refusal: backup.Refusal, message: str, **detail: Any) -> CratekitError:
    """One engine refusal, carrying the reservation table's own remediation.

    Not ``refuse``, whose default remedy would be the exit code's ``run-doctor``
    and would discard the per-slug remediation. The slug is carried unchanged.
    """
    slug = str(refusal)
    return CratekitError(
        Cause(
            reason=slug,
            message=message,
            remediation=reservations.remediation_for(slug),
            origin=("modules.tools.backup", "backup.cli"),
            detail={"refusal": slug, **detail},
        )
    )


def _is_rehearsal(job) -> bool:
    """Whether this job is a rehearsal, read off its frozen payload, never argv."""
    return bool((job.payload or {}).get(DRY_RUN))


def _is_full(job) -> bool:
    """Whether this job compares folder by folder, read off its frozen payload."""
    return bool((job.payload or {}).get(FULL))


def _is_check(job) -> bool:
    """Whether this job was asked for a full check, by either flag (U317)."""
    payload = job.payload or {}
    return bool(payload.get(CHECK)) or bool(payload.get(FULL))


def _outcome_row(outcomes, portion: backup_facts.Portion) -> tuple[dict | None, bool]:
    """One item's recorded portion row, and whether its run was a rehearsal."""
    recorded = (outcomes or {}).get(str(portion))
    if not isinstance(recorded, dict):
        return None, False
    found = None
    for row in recorded.get("portions") or ():
        if isinstance(row, dict) and row.get("portion") == str(portion):
            found = row
    return found, bool(recorded.get("dry_run"))


def kind_warning(outcomes, ages: list[dict] | None) -> tuple[dict[str, str], ...]:
    """Which kind of run this backup was, as one sentence, or nothing (U317).

    Read from the recorded outcomes, so an item that recorded nothing says
    nothing. The run's kind is the files portion's, except that a skipped files
    portion beside a new database snapshot is a quick run. The next full check
    is read back from the fact file, so a rehearsal never invents a date.
    """
    file_kinds = (backup.KIND_FULL, backup.KIND_QUICK, backup.KIND_SKIPPED)
    files, rehearsed = _outcome_row(outcomes, backup_facts.Portion.FILES)
    database, db_rehearsed = _outcome_row(outcomes, backup_facts.Portion.DATABASE)
    rehearsed = rehearsed or db_rehearsed
    parts: list[str] = []
    overall: str | None = None
    if files is not None and files.get("ran") and files.get("kind") in file_kinds:
        overall = files["kind"]
        parts.append(_files_sentence(files, rehearsed))
    database_kinds = (backup.KIND_SNAPSHOT, backup.KIND_UNCHANGED)
    if database is not None and database.get("ran") and database.get("kind") in database_kinds:
        if database["kind"] == backup.KIND_SNAPSHOT:
            parts.append(
                "the database would have been snapshotted"
                if rehearsed
                else "the database was snapshotted into a new dated folder"
            )
            if overall in (None, backup.KIND_SKIPPED):
                overall = backup.KIND_QUICK
        else:
            parts.append(
                "the database is what its last completed snapshot copied, so "
                + (
                    "no new snapshot would be taken"
                    if rehearsed
                    else "no new snapshot was taken and its age was reset"
                )
            )
            overall = overall or backup.KIND_SKIPPED
    if overall is None:
        return ()
    files_portion = str(backup_facts.Portion.FILES)
    due = next(
        (row.get("full_check_due") for row in ages or () if row.get("portion") == files_portion),
        None,
    )
    after = f"The next full check is due {due}" if due else "The next backup runs a full check"
    lead = "this rehearsal planned a" if rehearsed else "this backup was a"
    word = {"full": "full check", "quick": "quick run", "skipped": "skip"}[overall]
    message = (
        f"{lead} {word}: {'; '.join(parts)}. {after}; to run one now: crate backup run --check"
    )
    return ({"code": KIND, "message": message},)


def _files_sentence(row: dict, rehearsed: bool) -> str:
    """What the files portion did, in the words of its kind."""
    kind = row["kind"]
    changes = row.get("changes") if isinstance(row.get("changes"), dict) else {}
    found = ", ".join(
        f"{changes.get(name, 0)} {name}" for name in ("added", "changed", "rewritten", "removed")
    )
    took = backup_facts.took(row.get("seconds"))
    if kind == backup.KIND_SKIPPED:
        return (
            f"the files are what the last completed backup left, checked{took} "
            f"without listing the remote, so nothing was sent"
            + ("" if rehearsed else " and their age was reset")
        )
    if kind == backup.KIND_QUICK:
        said = row.get("comparison") if isinstance(row.get("comparison"), dict) else {}

        def number(key: str) -> str:
            value = said.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return "an unread number of"
            return f"{value:.0f}"

        verb = "would have sent" if rehearsed else "sent"
        return (
            f"against the record of the last completed backup the files had "
            f"{found}, and rclone {verb} {number('sent')} and archived "
            f"{number('archived')}{took}, listing nothing on the remote"
        )
    why = row.get("why") or "one was asked for"
    return f"the files were compared with the whole remote{took}, because {why}"


def comparison_warning(outcomes) -> tuple[dict[str, str], ...]:
    """What the file comparison did, as one sentence, or nothing (R-757).

    Read from the files item's recorded outcome only. A number rclone did not
    give is said to be unread, never zero; a mode this build does not know says
    nothing; a rehearsal says what it would have sent.
    """
    recorded = (outcomes or {}).get(str(backup_facts.Portion.FILES))
    if not isinstance(recorded, dict):
        return ()
    found = None
    for row in recorded.get("portions") or ():
        if isinstance(row, dict) and isinstance(row.get("comparison"), dict):
            found = row["comparison"]
    if found is None:
        return ()
    mode = found.get("mode")
    if mode not in (backup.COMPARISON_FAST, backup.COMPARISON_FULL):
        return ()

    def said(key: str, unit: str) -> str:
        value = found.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return f"an unread number of {unit}"
        return f"{value:.0f} {unit}"

    sent = (
        f"would have sent {said('sent', 'files')} and sent none"
        if recorded.get("dry_run")
        else f"sent {said('sent', 'files')}"
    )
    other = (
        "The full mode is: crate backup run --full"
        if mode == backup.COMPARISON_FAST
        else "The fast mode is: crate backup run --check"
    )
    message = (
        f"the file comparison ran in the {mode} mode and the mirror took "
        f"{said('seconds', 'seconds')}. It checked "
        f"{said('checked', 'files')} that were on both sides and {sent}. "
        f"Both modes compare every file by size and modification time. "
        f"{other}"
    )
    return ({"code": COMPARISON, "message": message},)


def rehearsal_warning() -> dict[str, str]:
    """The one sentence a rehearsal carries, spelled once for every branch.

    Stated as a property of the job, so it is true at queue time, on a second
    ask, after the resume and on a failed resume's refusal alike.
    """
    return {
        "code": REHEARSAL,
        "message": (
            "this backup is a rehearsal: it walks the whole plan with every "
            "transfer neutralized, so it copies nothing and publishes no backup "
            "age. The age a destructive session reads stays whatever the last "
            "real run left. Take a real backup with: crate backup run"
        ),
    }


def _rehearsal(job) -> tuple[dict[str, str], ...]:
    """The warning when this job is a rehearsal, and nothing when it is not."""
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()


def _with_rehearsal_step(error: CratekitError, job) -> CratekitError:
    """The same refusal, carrying the rehearsal sentence among its steps.

    A refusal envelope carries no warnings, so a failed rehearsal is told here.
    Only the steps change; ``rebuilt`` keeps the type, so a parked job still
    leaves as ``JobBlocked`` (R-290). A real run is returned unchanged, object
    for object.
    """
    if not _is_rehearsal(job):
        return error
    cause = error.cause
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(
                cause.remediation,
                steps=(*cause.remediation.steps, rehearsal_warning()["message"]),
            ),
        )
    )


def _raise_refusal(error: CratekitError, job) -> NoReturn:
    """Raise one refusal, carrying the rehearsal sentence when the job is one.

    A bare ``raise`` when nothing changed: ``raise error from error`` would make
    the cause its own ``__cause__`` and truncate the chain ``cause.classified``
    walks.
    """
    extended = _with_rehearsal_step(error, job)
    if extended is error:
        raise error
    raise extended from error


def _reported(store, job) -> dict:
    """One job as the ``job_state`` payload, on every branch of the verb.

    Per verb details ride under ``progress``, the one field ``job_state/1``
    leaves open; a top level key would be undeclared.
    """
    progress = dict(jobs.progress(store, job.job_id))
    progress[DRY_RUN] = _is_rehearsal(job)
    progress[FULL] = _is_full(job)
    # R-349, read from the same files ``job show`` reads.
    outcomes = backup_facts.read_outcomes(job.job_id)
    if outcomes is not None:
        progress[OUTCOMES] = outcomes
    cause = job.cause.to_json() if job.cause is not None else None
    return {"job_id": job.job_id, "state": str(job.state), "cause": cause, "progress": progress}


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("--job", default=None, metavar="JOB_ID", help=(
        "continue the backup already queued under this identifier"
    ))
    parser.add_argument("--dry-run", action="store_true", dest="dry_run", help=(
        "walk the same plan with every transfer neutralized, copying nothing "
        "and recording no backup age"
    ))
    parser.add_argument("--check", action="store_true", dest="check", help=(
        "run the full check now: list the remote, compare every file, and "
        "snapshot the database whether or not it changed. Without it a "
        "backup lists the remote when the last full check is a week old or "
        "when it cannot trust its record of the last backup, and otherwise "
        "sends only what changed since then, snapshots the database only if "
        "it changed, or is skipped when nothing did"
    ))
    parser.add_argument("--full", action="store_true", dest="full", help=(
        "run the full check listing the remote folder by folder instead of "
        "in one recursive pass, which takes most of an hour on a large "
        "library and does not depend on the recursive listing being complete"
    ))
    parser.add_argument(backup.EMPTIED_FLAG, action="store_true", dest="library_emptied", help=(
        "back up a library its owner emptied on purpose. Without it a backup "
        "refuses a library root that holds none of the library's files, or "
        "under a tenth of what the last backup held, because that is what an "
        "unmounted or lost volume leaves, and mirroring it would move the "
        "whole remote into the archive. It passes only a root that still "
        "carries the library's own record of a completed files backup, and "
        "never one on another volume than the library's"
    ))
    parser.set_defaults(_handler=backup_library)


def frozen_payload(
    dry_run: bool, full: bool = False, check: bool = False, emptied: bool = False
) -> dict[str, Any]:
    """What the queued job carries, as JSON booleans, and all a resume reads."""
    return {DRY_RUN: bool(dry_run), FULL: bool(full), CHECK: bool(check), EMPTIED: bool(emptied)}


def backup_argv(job) -> list[str]:
    """The command line that continues one queued backup.

    No ``--run``, because the verb declares no gate. Every frozen flag is
    rebuilt: a resume that lost ``--dry-run`` would turn a rehearsal into a real
    transfer in a detached child. A missing key still gives a valid line.
    """
    payload = job.payload or {}
    argv = ["backup", "run"]
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
    if payload.get(FULL):
        argv.append("--full")
    if payload.get(CHECK):
        argv.append("--check")
    if payload.get(EMPTIED):
        argv.append(backup.EMPTIED_FLAG)
    return [*argv, "--job", job.job_id]


def backup_items() -> tuple[str, ...]:
    """The items one backup job carries: one per declared portion.

    Derived from the enum (P3), and not from ``plan_backup``, which would make
    queueing need rclone, the process table and the volume.
    """
    return tuple(str(portion) for portion in backup_facts.Portion)


def _refuse_an_empty_job(store, job) -> None:
    """Refuse to drive a backup job that has no items, rather than succeeding at it.

    An older build queued backups with no items, and ``jobs.drive`` marks a job
    of zero items SUCCEEDED. Refused rather than repaired, because inventing
    items would run work under a payload nobody checked against this shape.
    """
    if jobs.items(store, job.job_id):
        return
    raise refuse(
        "internal-error",
        f"backup job {job.job_id} carries no items, so nothing would be copied "
        f"and the run would report success anyway. It was queued by a build that "
        f"had no worker for it",
        steps=(
            f"cancel it with: crate job cancel {job.job_id}",
            "then queue a new backup with: crate backup run",
        ),
        origin=("backup", "cli"),
        detail={"job_id": job.job_id},
    )


def _open_twin(store, *, handler_key: str, dry_run: bool, cfg: config.Config):
    """The open job that already IS the backup being asked for, or None (R-223).

    Returns the job with its frozen configuration, or None in that place when it
    could not be rebuilt (could not read is not somewhere else). A twin is the
    same verb and library, the same rehearsal flag, and a frozen mirror or
    archive root shared with this one, since two syncs into one mirror
    interleave. The comparison mode is not compared: both write one mirror. Jobs
    with no items and terminal jobs are never twins.
    """
    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    for job in jobs.list_jobs(store, states=open_states):
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
            continue
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
            continue
        if not jobs.items(store, job.job_id):
            continue
        try:
            frozen = jobs.frozen_config(job)
        except (config.ConfigError, ValueError):
            return job, None
        if (
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
        ):
            return job, frozen
    return None


def _already_queued(
    job, frozen: config.Config | None, *, asked_full: bool | None = None,
    asked_check: bool | None = None, asked_emptied: bool | None = None,
) -> dict[str, str]:
    """The one warning a reported twin carries, in the job's frozen terms.

    When the ask and the job differ in comparison mode, full check or
    ``--library-emptied``, the sentence says so, since the job is still reported
    and nothing is filed.
    """
    where = (
        "its frozen configuration could not be rebuilt, so where it writes is "
        "not known and it is treated as this backup"
        if frozen is None
        else f"it mirrors to {frozen.backup.dest} and archives under "
        f"{frozen.backup.archive_root}"
    )
    if asked_full is not None and asked_full != _is_full(job):
        held, asked = (
            (backup.COMPARISON_FAST, backup.COMPARISON_FULL)
            if asked_full
            else (backup.COMPARISON_FULL, backup.COMPARISON_FAST)
        )
        where += (
            f". It will run the {held} comparison if it runs a full check, and "
            f"this ask was for the {asked} one, so cancel it first if that is "
            f"the one wanted"
        )
    elif asked_check and not _is_check(job):
        where += (
            ". It runs a full check only if one is due and this ask was for one "
            "now, so cancel it first if that is the one wanted"
        )
    held_emptied = bool((job.payload or {}).get(EMPTIED))
    if asked_emptied is not None and asked_emptied != held_emptied:
        where += (
            f". It was not asked with {backup.EMPTIED_FLAG}, so it refuses a "
            f"library holding none of its files; cancel it first if this "
            f"library was emptied on purpose"
            if asked_emptied
            else f". It was asked with {backup.EMPTIED_FLAG}, which backs up a "
            f"library emptied on purpose; cancel it first unless that is what "
            f"this library is"
        )
    return {
        "code": ALREADY_QUEUED,
        "message": (
            f"backup job {job.job_id} is already open: {where}. It is reported "
            f"here and no second job was filed, because two backups sharing a "
            f"destination run at once and interleave. Continue it with: crate job "
            f"resume {job.job_id}. Or cancel it with: crate job cancel "
            f"{job.job_id}, and ask again"
        ),
    }


def backup_library(ctx) -> Envelope:
    """Freeze the payload and queue, or continue the job already queued.

    Nothing is planned here, so queueing never needs rclone, a remote or the
    volume.
    """
    cfg = load_config(("backup.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
            # Reconcile first: a claim left by a driver that died is invisible
            # to the queue otherwise.
            job = jobs.reconcile(store, ctx.args.job)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _refuse_an_empty_job(store, job)
                try:
                    _, warnings = ctx.run_job(store, job)
                except CratekitError as exc:
                    # ``jobs.drive`` raises here when every item failed, so the
                    # rehearsal word must be added on this exit too.
                    _raise_refusal(exc, job)
                job = jobs.get(store, job.job_id)
            # Outside the ``is_open`` branch, so a job that ended failed or
            # cancelled never exits OK however many times it is asked about.
            # The engine's own cause is re-raised, keeping its type (R-290).
            try:
                jobs.raise_for_state(job)
            except CratekitError as exc:
                _raise_refusal(exc, job)
            reported = _reported(store, job)
            # Read back here, not inside the item, so an unreadable fact file
            # refuses the command and not a completed transfer, and against the
            # job's frozen configuration, which is where the item published.
            try:
                reported["ages"] = published_ages(jobs.frozen_config(job))
            except CratekitError as exc:
                _raise_refusal(exc, job)
            # Asked of the frozen configuration and the job here, because the
            # work body's report does not leave a claimed item.
            warnings = (
                *warnings,
                *map(dict, backup.absent_analysis_share(jobs.frozen_config(job))),
                *map(dict, backup.snapshot_identity_warning(jobs.frozen_config(job))),
                *_rehearsal(job),
                *comparison_warning(reported["progress"].get(OUTCOMES)),
                *kind_warning(reported["progress"].get(OUTCOMES), reported["ages"]),
            )
            return ctx.envelope(data=reported, warnings=warnings)
        payload = frozen_payload(
            ctx.args.dry_run, ctx.args.full, ctx.args.check, ctx.args.library_emptied
        )
        found = _open_twin(
            store, handler_key=ctx.entry.handler_key, dry_run=payload[DRY_RUN], cfg=cfg
        )
        if found is not None:
            twin, frozen = found
            # The envelope a first ask gets, plus one warning; the other
            # warnings describe the job reported, under its frozen configuration.
            described = cfg if frozen is None else frozen
            return ctx.envelope(
                data=_reported(store, twin),
                warnings=(
                    _already_queued(
                        twin, frozen, asked_full=payload[FULL], asked_check=payload[CHECK],
                        asked_emptied=payload[EMPTIED],
                    ),
                    *map(dict, backup.absent_analysis_share(described)),
                    *map(dict, backup.snapshot_identity_warning(described)),
                    *_rehearsal(twin),
                ),
            )
        job = jobs.enqueue(
            store, handler_key=ctx.entry.handler_key, payload=payload,
            # One portion is one item; a job of zero items would succeed empty.
            item_ids=backup_items(),
            cfg=cfg,
        )
        # Said at queue time, the one moment the identifier is certainly read.
        return ctx.envelope(
            data=_reported(store, job),
            warnings=(
                *map(dict, backup.absent_analysis_share(cfg)),
                *map(dict, backup.snapshot_identity_warning(cfg)),
                *_rehearsal(job),
            ),
        )


def published_ages(cfg: config.Config, *, now: datetime | None = None) -> list[dict]:
    """What a destructive session would now see, read back from the fact file.

    Read rather than derived from the outcome, so it cannot drift from the
    engine's publish rule. An unreadable file refuses, carrying the exception's
    own remedy, because an empty answer would look like a library never backed up.
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
            f"the backup ran and the age it published cannot be read back: {exc}. "
            f"Reporting no age would say this library has never been backed up, "
            f"which is a different condition with a different fix",
            remedy=Remedy(str(exc.remedy)),
            origin=("backup", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    return [
        {
            "portion": str(entry.portion),
            "state": str(entry.state),
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
            "completed_at": _iso(entry.completed_at),
            "destination": entry.destination,
            # U317: the files portion's next full check as a date, None when the
            # next backup runs one, and always for the database.
            "full_check_due": _iso(entry.full_check_due and entry.full_check_due.date()),
        }
        for entry in reported
    ]


def _iso(moment) -> str | None:
    """A date or time as ISO 8601, or None for none."""
    return moment.isoformat() if moment is not None else None


def refusal_for(outcome: backup.BackupOutcome) -> CratekitError | None:
    """The refusal a finished run earns, or None when something was backed up.

    A portion that failed decides the run even when the other completed. A
    portion the engine refused ends the run only when nothing ran: one shared
    reason is raised with its reserved remedy, differing reasons become
    ``backup-nothing-ran`` with each as a step.
    """
    failed = tuple(
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
    )
    if failed:
        # Retryable: a transfer that exited non zero runs again as it did, and
        # the job cause and ``jobs.retry`` read this flag (R-380, R-390).
        return refuse(
            "backup-transfer-failed",
            "a transfer this backup ran came back non zero and the run did not "
            "complete: "
            + "; ".join(f"{entry.portion.value}: {entry.detail}" for entry in failed)
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
            retryable=True,
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
        )
    if any(entry.ran for entry in outcome.portions):
        return None
    refusals = {entry.refusal for entry in outcome.portions if entry.refusal is not None}
    if len(refusals) == 1:
        only = next(iter(refusals))
        said = next(entry.detail for entry in outcome.portions if entry.refusal is only)
        return _engine_refusal(
            only, said, portions=[entry.portion.value for entry in outcome.portions]
        )
    refused = [entry for entry in outcome.portions if entry.refusal is not None]
    return refuse(
        "backup-nothing-ran",
        "no portion of this backup ran, and the two halves were refused for "
        "different reasons, so there is no one thing to fix",
        steps=tuple(
            f"{entry.portion.value}: {entry.refusal} because {entry.detail}" for entry in refused
        ),
        origin=("backup", "cli"),
        detail={"refusals": {entry.portion.value: str(entry.refusal) for entry in refused}},
    )


def perform_backup(
    payload: dict[str, Any], *, portion: backup_facts.Portion | None = None,
    cfg: config.Config | None = None, runner=backup.subprocess_runner,
    now: datetime | None = None, process_lister=None, read_back: bool = True,
    outcome_to: tuple[str, str] | None = None,
) -> dict:
    """Do the backup one queued job asks for, and report what actually happened.

    Takes the payload rather than a job, so it is drivable without a store.
    ``portion`` narrows the run to one half. ``cfg`` is the job's frozen
    configuration (KTD9), loaded fresh only for unqueued callers. ``read_back``
    is off under the driver, where an unreadable fact file would fail a
    rehearsal's item on every resume; the shell's resume branch reads instead.
    ``outcome_to`` is a job and item pair a failed run's outcome is written
    under before the refusal is raised (R-349). Engine refusals are translated
    into causes with their reserved remediation.
    """
    cfg = load_config(("backup.cli",)) if cfg is None else cfg
    dry_run = bool(payload.get(DRY_RUN))
    try:
        plan = backup.plan_backup(
            cfg, now=now, process_lister=process_lister,
            full=bool(payload.get(FULL)),
            check=bool(payload.get(CHECK)),
            emptied=bool(payload.get(EMPTIED)),
            only=portion,
        )
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
    if portion is not None:
        # ``replace`` keeps every other plan field, ``archive_keep`` included;
        # ``plan.portion`` raises for a portion the planner did not build.
        plan = replace(plan, portions=(plan.portion(portion),))
    try:
        outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
    except backup_facts.BackupFactsUnreadable as exc:
        # The engine reads the fact file before publishing; translated so a bad
        # file names its fix instead of becoming ``internal-error``.
        raise refuse(
            "backup-facts-unreadable",
            f"the {portion or 'backup'} portion cannot read or write the record "
            f"of its age: {exc}. Whatever it copied exists; the fact a "
            f"destructive session reads does not",
            remedy=Remedy(str(exc.remedy)),
            origin=("backup", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    # Applied unqualified over a narrowed run: a done item is never re-armed, so
    # a refused portion must fail its item for a resume to finish it.
    refusal = refusal_for(outcome)
    if refusal is not None:
        if outcome_to is not None:
            raise _with_outcome_recorded(refusal, outcome, outcome_to)
        raise refusal
    report = backup.outcome_payload(outcome)
    if read_back:
        report["ages"] = published_ages(cfg, now=now)
    return report


def _with_outcome_recorded(
    refusal: CratekitError, outcome: backup.BackupOutcome, outcome_to: tuple[str, str]
) -> CratekitError:
    """Write a failed run's outcome, and return the refusal to raise (R-349).

    The refusal is returned unchanged when the write succeeds. When it fails the
    refusal still wins, unchained so ``cause.classified`` is not misled, and the
    lost record is said as a step.
    """
    job_id, item_id = outcome_to
    try:
        backup_facts.write_outcome(job_id, item_id, backup.outcome_payload(outcome))
    except OSError as exc:
        cause = refusal.cause
        steps = (
            *cause.remediation.steps,
            f"the record of which commands this run ran could not be "
            f"written, so job show will not list them: {exc}",
        )
        return rebuilt(refusal, replace(cause, remediation=replace(cause.remediation, steps=steps)))
    return refusal


def _staged(final):
    """The staging path beside ``final``, so the engine's rename is atomic."""
    return final.with_name(final.name + ".staged")


def handle(job, item, cfg) -> "jobs.Produced | None":
    """Back up one portion. The per-item worker behind ``handler_key`` backup.run.

    The item names the portion. The outcome is the item's artifact (R-349),
    staged and handed back so the engine commits it before the item is done;
    only a success takes this channel. ``cfg`` is the frozen configuration
    (KTD9), passed straight through and never reloaded here.
    """
    named = str(item.item_id or "")
    try:
        portion = backup_facts.Portion(named)
    except ValueError:
        declared = backup_items()
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
            remedy=Remedy.REPORT_DEFECT,
            origin=("backup", "cli"),
            detail={"item_id": named, "portions": list(declared)},
        ) from None
    # Before the attempt, so the record on disk is only ever this attempt's.
    backup_facts.clear_outcome(job.job_id, named)
    report = perform_backup(
        dict(job.payload or {}),
        portion=portion,
        cfg=cfg,
        # RESOLVED AT CALL TIME, not left to the default, so a test can put a
        # stand-in in front of it. ``perform_backup``'s own default is bound when
        # this module is imported and cannot be reached any other way.
        runner=backup.subprocess_runner,
        read_back=False,
        outcome_to=(job.job_id, named),
    )
    final = backup_facts.outcome_path(job.job_id, named)
    staged = _staged(final)
    # A record that cannot be staged does not fail the item: the backup exists
    # and its age is published, so it completes with no artifact.
    try:
        config.atomic_write_bytes(backup_facts.encode_outcome(report), staged)
    except OSError:
        return None
    return jobs.Produced(staged=staged, final=final)


__all__ = [
    "ALREADY_QUEUED", "COMPARISON", "DRY_RUN", "FULL", "OUTCOMES", "REHEARSAL", "backup_argv",
    "backup_items", "backup_library", "build", "comparison_warning", "frozen_payload", "handle",
    "perform_backup", "published_ages", "refusal_for", "rehearsal_warning",
]
