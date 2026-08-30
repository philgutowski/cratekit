"""``crate backup run``: back the library up, and publish the age R15's warning reads.

U35 landed the ENGINE in :mod:`cratekit.modules.tools.backup` and never landed a
shell, so Feature Inventory row 31 sat uncovered while the registry declared this
verb against a closed unit. This file is the shell half, and nothing here
re-decides what the registry already declares.

**THE AGE IS PUBLISHED BY THE ENGINE, PER PORTION, AND THIS SHELL NEVER WRITES
IT.** :func:`cratekit.modules.tools.backup.run_backup` calls
``backup_facts.record`` itself, once per portion that actually completed, and a
portion that refused or failed leaves its previous fact untouched. A shell that
recorded a second time would be a second writer of one fact, and the two can
disagree in exactly the direction that costs data: the engine publishes from what
transferred, and anything the shell knows about is the PLAN. So the shell's whole
obligation here is the negative one, do not add to it and do not undo it.

**WHAT THE SHELL DOES OWN IS READING IT BACK.** :func:`published_ages` re-opens
the fact file after the run and reports what a destructive session would now see.
Not derived from the outcome, which would be a second copy of the engine's own
publish rule and would drift from it silently; read from the same file
:func:`cratekit.core.session._shown_ages` reads, so the verb's report and the
acknowledgment that gates every destructive verb answer from one source. If the
engine ever stopped publishing, this report says ``never-recorded`` rather than
congratulating the person.

That is not decoration. The backup age is what a destructive write session
consults before it lets anything through. A backup shell that runs and does not
put the fact where the session looks leaves the product refusing destructive work
on the grounds that no backup exists, immediately after the person took one.

**WHY THE OUTCOME IS READ RATHER THAN THE PLAN REPORTED.** This file is the FIRST
CALLER of ``plan_backup`` and ``run_backup`` in ``src``, verified with
``git grep -n run_backup -- src`` before the call was written, which returned the
definition, the ``__all__`` entry and a comment and nothing else. The corpus
entry ``docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-
owner-of-its-unreviewed-defects.md`` is what that grep is owed to: adding the
first caller to an existing internal function makes you the owner of its
unreviewed defects, and its sibling ``run_restore`` shipped a whole unit ignoring
its return codes because nothing had ever called it. ``run_backup`` reads its
return codes, so the half of that defect that lives in the engine is not here.
The half that lives in the SHELL is, and it is the one this file has to refuse to
reproduce: a report built from the plan's command labels rather than from the
results says two transfers completed over a run in which none did.
:func:`perform_backup` therefore builds its report from
``backup.outcome_payload`` and from the fact file, and touches
``backup.plan_payload`` nowhere.

**AND A RUN THAT FAILED IS A REFUSAL, WHICH IS THIS LAYER'S DECISION TO MAKE.**
``run_backup`` reports per portion rather than raising, deliberately: a mirror
that completed while the database was skipped is a successful mirror, and the
per-portion fact says so. That is the right answer for an engine and it is not an
exit code. :func:`refusal_for` is where the per-portion outcome becomes one, and
the property it exists for is that a run in which NOTHING was backed up never
exits OK. Exiting 0 over "rclone is not installed" is the merge bar's "shown a
clean report over state the tool could not read", and the entry's own
``binary.rclone`` doctor check is the product saying that condition has a name.

**WHY THIS VERB DECLARES NO GATE.** The registry declares none and this file
agrees rather than adding one. The run ADDS: a mirror, and a dated archive folder
of the versions the mirror overwrote. It replaces nothing a person kept, writes
no database row, and publishes nothing outward that cannot be taken back. The one
deletion in it is the archive prune, and three properties keep that from being a
decision the product raises: it runs only AFTER the mirror in its portion
succeeded, so a failed run never touches the safety net; it keeps
``archive_keep`` folders by the engine's own declared policy rather than by
anything typed here; and it is the rotation the feature is made of rather than a
surprise. What is left is time and network, both of which the typed command
already spends knowingly, and R34's gate machinery is for decisions the PRODUCT
raises rather than ones the person volunteered.

Declining it also keeps the verb out of ``tests/test_queued_resume_contract.py``'s
derived population, which is a consequence and not the reason: an explicit gate
plus ``long_running`` plus an ``argv_builder`` obliges the resume argv to carry
``--run`` with the frozen gate run, and that machinery would exist here purely to
guard a run that adds.

**WHY THE WORK BODY IS ``perform_backup`` AND NOT ``run_backup``.** The engine
already owns that name, and ``docs/METHOD.md`` lists "one symbol meaning two
things in two modules" among the things a green suite cannot see. A reader
grepping ``run_backup`` should find one function.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

Layer: modules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

# ALIASED, because this package holds TWO modules called ``exit_codes`` and they
# are different things, which is the note ``session.restore_cli`` writes for the
# same pair. ``cratekit.cli.exit_codes`` is the reserved-cause table, which is
# what an engine refusal's remediation is looked up in;
# ``cratekit.core.exit_codes`` is the status vocabulary and the remedy tokens.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope
from cratekit.core import backup_facts, config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import backup

#: The payload key this build freezes. Named once so the handler and the argv
#: builder cannot drift: a key the handler freezes and the builder does not read
#: is a resume that quietly does different work from the run it continues.
DRY_RUN = "dry_run"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("backup.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _engine_refusal(refusal: backup.Refusal, message: str, **detail: Any) -> CratekitError:
    """One engine refusal, carrying the reservation table's own remediation.

    NOT ``refuse``, and that is the whole reason this helper exists.
    ``cause.refuse`` defaults an absent remedy to the one the exit CODE declares,
    which for every backup refusal is ``run-doctor``, and the reservation table
    already holds a better answer per slug: ``rclone-missing`` carries
    ``install-binary``, ``remote-not-configured`` carries ``run-setup``, and
    ``no-snapshot-available`` carries steps rather than a token at all. A
    class-level default here throws all three away and tells a person to run a
    diagnostic that will tell them the thing this refusal already knows.

    Written after finding the same shape one module over, in
    ``session.restore_cli._refused``, which reads the same table for the same
    exception type. Its own mutation table measured what dropping this costs and
    recorded that swapping the reserved remediation for the class default killed
    ZERO tests. This shell is the second caller of that table for these slugs and
    it agrees with the first rather than inventing a second opinion beside it.

    THE SLUG IS CARRIED THROUGH UNCHANGED rather than folded into a nearby
    reason, for the reason that file gives: nine diagnoses flattened into one is
    a person being told to mount a volume when what is missing is a program.
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


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the backup already queued under this identifier",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help=(
            "walk the same plan with every transfer neutralized, copying nothing "
            "and recording no backup age"
        ),
    )
    parser.set_defaults(_handler=backup_library)


def frozen_payload(dry_run: bool) -> dict[str, Any]:
    """What the queued job carries, and the only thing the resume is rebuilt from.

    ``bool`` rather than the argparse value straight through, so the payload holds
    a JSON boolean rather than whatever truthy object a caller handed the
    namespace. A payload key that is ``"false"`` as a string is true to every
    reader of it, and the reader here decides whether anything is copied.
    """
    return {DRY_RUN: bool(dry_run)}


def backup_argv(job) -> list[str]:
    """The command line that continues one queued backup.

    IT CARRIES NO ``--run``. This verb declares no gate, so there is no decision
    frozen against a run and a ``--run`` here would name a run nothing was
    recorded against. The queued shells that DO carry it are the ones with an
    ``explicit`` gate, and ``tests/test_queued_resume_contract.py`` derives that
    population from the registry rather than from a list, so this verb joins it on
    the day somebody adds a gate and not before.

    THE FROZEN FLAG IS REBUILT, and dropping it is the one way this builder could
    do real harm: a resume that loses ``--dry-run`` turns a rehearsal into a real
    transfer that publishes a backup age, in a detached child whose only output is
    a log nobody is watching.

    A payload missing the key still produces a valid command line, which is
    forward tolerance for a key a later build may add rather than a case reachable
    today. The reason to carry it anyway is that the caller is that same detached
    child, so a ``KeyError`` there is invisible.
    """
    payload = job.payload or {}
    argv = ["backup", "run"]
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
    return [*argv, "--job", job.job_id]


def backup_library(ctx) -> Envelope:
    """Freeze the rehearsal flag and queue, or report the job already queued.

    NOTHING IS PLANNED HERE, deliberately, and the difference from the work body
    below is the whole reason queueing is separate from working. ``plan_backup``
    resolves rclone, reads the process table and stats the library root, and a
    shell that did any of that would refuse to QUEUE on a machine where the work
    would have run fine once claimed. Queueing needs no rclone, no remote and no
    volume, and the entry's two doctor checks are what tell a person about those
    before they type the verb.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=frozen_payload(ctx.args.dry_run),
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def published_ages(cfg: config.Config, *, now: datetime | None = None) -> list[dict]:
    """What a destructive session would now see, READ BACK from the fact file.

    Read rather than derived, and that is the load-bearing sentence in this
    module. The obvious implementation is to walk the outcome and call a portion
    published when it ran, which is a second copy of the engine's publish rule
    living in a different file from the rule it copies. The two would agree on the
    day this was written and would drift on any day the engine changed, and the
    direction of the drift is the expensive one: a report saying a portion is
    backed up over a fact file that says never-recorded sends a person into a
    destructive session believing they are covered.

    The SOURCE is shared with :func:`cratekit.core.session._shown_ages`, which is
    the thing that must not be duplicated. The rendering is per surface: that one
    writes the record of what a person was shown, this one answers a command.

    An unreadable fact file REFUSES rather than reporting nothing, for the reason
    :class:`cratekit.core.backup_facts.BackupFactsUnreadable` gives at length: an
    empty answer is byte for byte what a library with no backup would produce, and
    the two have opposite fixes. The remedy travels from the exception rather than
    being fixed at ``repair-backup-facts`` here, because that class names three
    and one of them is a permission on a directory, which repairing a file does
    not touch.
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
            "completed_at": (
                entry.completed_at.isoformat() if entry.completed_at is not None else None
            ),
            "destination": entry.destination,
        }
        for entry in reported
    ]


def refusal_for(outcome: backup.BackupOutcome) -> CratekitError | None:
    """The refusal a finished run earns, or None when something was backed up.

    THE PROPERTY THIS EXISTS FOR: a run in which nothing was backed up never exits
    OK. Everything below is that sentence split by which of the three ways it
    happened, because the three have three different fixes.

    A portion that FAILED is a transfer that came back non zero, which is the
    engine reporting ``ran=False`` with no refusal on it. That decides the whole
    run even when the other portion completed, because a person who is told a
    backup succeeded stops looking, and half a backup with a published age for the
    half that worked is precisely the state R15's per-portion warning exists to
    make visible rather than to hide behind one verdict.

    A portion that REFUSED did not fail: the engine decided before attempting
    anything that this half could not run, and the other half may well have. So a
    refusal only ends the run when NOTHING ran, and the normal state of a library
    backed up without quitting rekordbox first, files current and database
    skipped, reports success here exactly as the engine says it should.

    When nothing ran and every portion refused for ONE reason, that reason is the
    refusal, so a machine with no rclone gets ``rclone-missing`` with its reserved
    remedy rather than a summary slug that would send a person somewhere vaguer.
    When the reasons DIFFER there is no single remedy to name, and inventing one
    by taking the first portion's would report a mounted-volume problem as a
    missing-database one half the time. ``backup-nothing-ran`` carries all of them
    as steps instead, which is the same choice ``no-snapshot-available`` makes one
    module over: a sentence beats a plausible wrong command.

    An outcome with no portions at all cannot be produced by ``plan_backup``,
    which always builds one entry per declared portion. It lands on the last
    branch rather than on an index error, because the answer to "nothing ran" is
    the same however few portions there were.
    """
    failed = tuple(
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
    )
    if failed:
        return refuse(
            "backup-transfer-failed",
            "a transfer this backup ran came back non zero and the run did not "
            "complete: "
            + "; ".join(f"{entry.portion.value}: {entry.detail}" for entry in failed)
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
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
            only,
            said,
            portions=[entry.portion.value for entry in outcome.portions],
        )
    return refuse(
        "backup-nothing-ran",
        "no portion of this backup ran, and the two halves were refused for "
        "different reasons, so there is no one thing to fix",
        steps=tuple(
            f"{entry.portion.value}: {entry.refusal} because {entry.detail}"
            for entry in outcome.portions
            if entry.refusal is not None
        ),
        origin=("backup", "cli"),
        detail={
            "refusals": {
                entry.portion.value: str(entry.refusal)
                for entry in outcome.portions
                if entry.refusal is not None
            }
        },
    )


def perform_backup(
    payload: dict[str, Any],
    *,
    cfg: config.Config | None = None,
    runner=backup.subprocess_runner,
    now: datetime | None = None,
    process_lister=None,
) -> dict:
    """Do the backup one queued job asks for, and report what actually happened.

    PURE OF THE JOB ENGINE ON PURPOSE, taking the payload rather than a job, the
    way ``run_master`` does one package over and for the same reason: the
    properties that matter most about this body, that a failed run publishes no
    age and that the age it does publish is the one the session will read, are
    then drivable without a configured machine, a job store and a claimed item.
    Nothing in ``src`` claims a job item today (R-198), so built inside the handler
    this body would have no reachable caller at all.

    THE ENGINE'S WHOLE-RUN REFUSALS ARE TRANSLATED RATHER THAN LET ESCAPE.
    ``BackupRefused`` is not a ``CratekitError``, so the dispatcher's
    ``except Exception`` would convert it to ``internal-error``, which carries
    ``report-defect``, and a person who has not run setup yet would be told to
    file a bug against this program. Every member of ``Refusal`` is a declared
    reason with a reserved code AND a reserved remediation, and
    :func:`_engine_refusal` is what carries both rather than only the first.

    THE REPORT IS BUILT FROM THE OUTCOME AND FROM THE FACT FILE. ``plan_payload``
    is not called here and the plan is not reported, which is the shell half of
    the defect the first-caller learning records: the plan says what was going to
    be copied and the outcome says what was.

    ``cfg`` IS A PARAMETER BECAUSE THE JOB DRIVER'S CONTRACT SAYS SO.
    :func:`cratekit.core.jobs.drive` states that its handler "runs against
    ``frozen_config(job)``, which it reads off the job rather than loading fresh,
    because reloading is precisely the resume bug KTD9 closes". A work body that
    could only load fresh would be unable to honour that, and the cost is
    specific here rather than general: a backup queued against one remote and
    claimed after the person reconfigured their destinations would copy the
    library somewhere they did not ask for, and would publish an age naming a
    destination the queued run never targeted.

    NOTHING PASSES IT TODAY, because ``jobs.drive`` has no caller in ``src``
    (R-198), so the fallback is what every reachable path takes. The parameter is
    still here rather than deferred to the unit that binds the handler: the
    binding is a table of ``handler_key`` to callable, and a work body whose
    signature cannot accept the frozen configuration makes that unit choose
    between changing four shells and wiring the bug in.
    """
    cfg = _load() if cfg is None else cfg
    dry_run = bool(payload.get(DRY_RUN))
    try:
        plan = backup.plan_backup(cfg, now=now, process_lister=process_lister)
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
    # ``PortionOutcome.results`` IS DROPPED, AND HERE IS WHY, because the
    # first-caller learning says a returned value nobody inspects is the same
    # defect wearing a type annotation unless a comment says otherwise. Every
    # return code that DECIDES a portion has already been read: ``run_backup``
    # compares each one and stops the portion on the first non zero, which is
    # what ``ran`` then reports. The one class it deliberately does not fail on
    # is the archive prune, argued at length in ``_prune_archive``: by the time
    # it runs the mirror has completed, so the backup the person asked for
    # exists, and a stale folder using space is a smaller problem than sending
    # them to repeat the whole transfer. Failing the portion HERE would overrule
    # that decision from the wrong layer.
    #
    # What is genuinely lost is that a failed prune reaches no report at all, so
    # dated archive folders can accumulate with nothing saying so. Recorded as a
    # residual rather than fixed, because the fix is a new key in the outcome
    # payload and that payload is the ENGINE's.
    refusal = refusal_for(outcome)
    if refusal is not None:
        raise refusal
    report = backup.outcome_payload(outcome)
    # THE FLAG IS ON THE REPORT because a rehearsal and a real run are otherwise
    # indistinguishable in it: both list the same portions with ``ran`` true, and
    # only one of them copied anything or published an age. ``ages`` beside it is
    # what makes that checkable rather than asserted, since a rehearsal leaves
    # every portion exactly as it found it.
    report["dry_run"] = dry_run
    report["ages"] = published_ages(cfg, now=now)
    return report


__all__ = [
    "DRY_RUN",
    "backup_argv",
    "backup_library",
    "build",
    "frozen_payload",
    "perform_backup",
    "published_ages",
    "refusal_for",
]
