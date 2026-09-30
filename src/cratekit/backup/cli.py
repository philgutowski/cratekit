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

from dataclasses import replace
from datetime import datetime
from typing import Any, NoReturn

# ALIASED, because this package holds TWO modules called ``exit_codes`` and they
# are different things, which is the note ``session.restore_cli`` writes for the
# same pair. ``cratekit.cli.exit_codes`` is the reserved-cause table, which is
# what an engine refusal's remediation is looked up in;
# ``cratekit.core.exit_codes`` is the status vocabulary and the remedy tokens.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope
from cratekit.core import backup_facts, config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import backup

#: The payload key this build freezes. Named once so the handler and the argv
#: builder cannot drift: a key the handler freezes and the builder does not read
#: is a resume that quietly does different work from the run it continues.
DRY_RUN = "dry_run"

#: The payload key for the full comparison (R-757), frozen and rebuilt the way
#: the one above is and for the same reason: a resume that lost it would run
#: the fast comparison under a job a person queued to be the full one.
FULL = "full"

#: The advisory saying what the file comparison did (R-757). A warning because
#: the default renderer prints a verb's warnings and nothing of its payload, so
#: this is the only place a person reading the terminal meets the numbers.
COMPARISON = "backup-comparison"

#: The warning a second ``backup run`` carries when it reports the open job in
#: place of filing another (R-223). A warning and not a refusal, because nothing
#: went wrong: the backup the person asked for is already in the queue, and the
#: envelope they get back is that job's.
ALREADY_QUEUED = "backup-already-queued"

#: The warning every branch of a REHEARSAL carries, queued, reported or resumed
#: (R-221). A warning and not a refusal for the same reason as the one above:
#: nothing went wrong, and the person asked for exactly this.
REHEARSAL = "backup-rehearsal"

#: The ``progress`` key carrying each item's recorded outcome (R-349). Named in
#: core because ``job show`` renders the same key without importing this module.
OUTCOMES = backup_facts.OUTCOMES_FIELD


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


def _is_rehearsal(job) -> bool:
    """Whether this JOB is a rehearsal, read off the payload it was frozen with.

    THE PAYLOAD AND NEVER THE COMMAND LINE. ``--dry-run`` typed beside ``--job``
    selects nothing at all: the resume rebuilds the flag from the payload in
    :func:`backup_argv`, and the worker reads it from there too. A report taken
    off ``ctx.args`` would call a run that really copied a rehearsal whenever a
    person typed both flags, and the one word the envelope gives them about
    which kind of run it was is the word that has to be right.

    ``bool`` of one key, the way :func:`_open_twin` and :func:`perform_backup`
    already read it, so all four readers answer the same question the same way.
    """
    return bool((job.payload or {}).get(DRY_RUN))


def _is_full(job) -> bool:
    """Whether this JOB compares folder by folder, read off its frozen payload.

    The payload and never the command line, for the reason :func:`_is_rehearsal`
    gives: ``--full`` typed beside ``--job`` selects nothing.
    """
    return bool((job.payload or {}).get(FULL))


def comparison_warning(outcomes) -> tuple[dict[str, str], ...]:
    """What the file comparison did, as one sentence, or nothing (R-757).

    READ FROM THE RECORDED OUTCOME of the files item, which is what the run
    itself wrote, and from nowhere else. A job whose files item recorded no
    outcome, or one whose mirror never ran, says nothing here rather than
    reporting a comparison nobody measured.

    A NUMBER THAT WAS NOT READ IS SAID TO BE UNREAD. The engine reports None
    for a total rclone did not give, and printing that as zero would tell a
    person nothing was sent.

    A MODE THIS BUILD DOES NOT KNOW SAYS NOTHING, for the same reason. The
    sentence names the mode and offers the other one, and both halves would be
    invented over a record that carries neither word.

    A REHEARSAL IS SAID AS ONE. rclone counts what a dry run WOULD send, and
    "sent" over a run that copied nothing contradicts the rehearsal warning
    printed beside it. The flag is read from the same recorded outcome.
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
        else "The fast mode is: crate backup run"
    )
    return (
        {
            "code": COMPARISON,
            "message": (
                f"the file comparison ran in the {mode} mode and the mirror took "
                f"{said('seconds', 'seconds')}. It checked "
                f"{said('checked', 'files')} that were on both sides and {sent}. "
                f"Both modes compare every file by size and modification time. "
                f"{other}"
            ),
        },
    )


def rehearsal_warning() -> dict[str, str]:
    """The one sentence a rehearsal carries, spelled once for all four branches.

    WRITTEN IN A TENSE TRUE WHEREVER IT IS CARRIED, because this verb hands the
    same job back at queue time, when a second ask reports the open one, after
    the resume has finished, and on the refusal a failed resume raises. A
    sentence in the past tense is false on the first two and a sentence in the
    future tense is false on the last two, and the alternative, two spellings of
    one condition, is how the two come to disagree about what a rehearsal is.
    What is stated instead is a property of the JOB, which is true at every one
    of those moments.

    IT NAMES THE AGE AND NOT THE REPORT. The ages an envelope carries are read
    back from the fact file, so a rehearsal reports the PREVIOUS real run's and
    they are true, which is exactly why R-221 is a report a person believes. The
    two branches that hand back an identifier carry no ages at all, so a sentence
    about "the ages above" would be false on half the surfaces this rides. The
    fact file is what a destructive session reads and it is the same statement on
    all of them.
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
    """The same refusal, carrying the rehearsal sentence among the things to know.

    THE SECOND EXIT, AND THE ONE AN ENVELOPE NEVER REACHES. R-225 makes a job
    that closed carrying a cause leave through that cause rather than through an
    envelope, and a refusal envelope carries no warnings at all, so the warning
    above reaches every resume EXCEPT the one that failed. The corpus entry
    ``docs/solutions/workflow-issues/a-queued-verb-has-two-exits-and-an-advisory-
    on-the-envelope-only-reaches-one.md`` records that shape one module over, on
    ``tag retag``, and this is the same verb family meeting it again. A person
    whose rehearsal failed is owed the same word as one whose rehearsal
    succeeded, because neither run copied a byte, and without it a failed
    rehearsal reads as a real backup attempt that fell over.

    THE STEP IS APPENDED AND THE CAUSE IS OTHERWISE UNTOUCHED, which is the rule
    ``retag_cli.with_reload_step`` states: ``origin`` is append-only and a cause
    arriving at the CLI with a shortened trail means some hop re-created it,
    losing everything below. Two fields are replaced and ``origin``, ``inner``,
    ``detail``, ``scope`` and ``retryable`` travel through by construction. The
    remedy token stays the failure's own, because retrying is still the first
    thing to do and this is context rather than a competing instruction.

    A REAL RUN IS RETURNED UNCHANGED, OBJECT FOR OBJECT, so this cannot add a
    step to a refusal it has nothing to say about. Telling a person whose real
    backup failed that nothing was copied is false in the direction that stops
    them looking for the half that was. :func:`_raise_refusal` is what raises the
    result, and the identity above is the thing it branches on.

    THE TYPE IS CARRIED THROUGH AS WELL, BY ``cause.rebuilt`` (R-290). A parked
    job leaves as ``JobBlocked`` and the dispatcher reads that type, nothing on
    the cause, as the blocked outcome. Rebuilt as a plain ``CratekitError``, a
    rehearsal the worker parked would say ``failed`` over a job whose state is
    blocked, which is the hop ``retag_cli.with_reload_step`` was caught making.
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

    NOT ``_refuse``, which is what this was called for one round. This module
    already imports ``cause.refuse``, which BUILDS a cause and raises nothing,
    and a second name a letter apart that raises and returns nothing is the
    "one symbol meaning two things" METHOD lists among what a green suite
    cannot see. A reader grepping ``refuse`` here should find the builder.

    THE BRANCH IS WHAT THIS EXISTS FOR, and the first cut did not have it.
    ``raise extended from error`` reads correctly and becomes ``raise error from
    error`` on a real run, where :func:`_with_rehearsal_step` hands the same
    object straight back. A cause that is its own ``__cause__`` truncates the
    chain ``cause.classified`` walks, so a ``no-evidence`` refusal raised over a
    permission error stopped classifying as ``path-permission-denied`` and told a
    person to retry later instead of to grant access. ``retag_cli`` takes a bare
    ``raise`` on exactly this branch and this follows it.

    ``from error`` IS KEPT WHERE THE OBJECT REALLY CHANGED, because there the
    extended refusal genuinely did come from the original and the chain says so.
    """
    extended = _with_rehearsal_step(error, job)
    if extended is error:
        raise error
    raise extended from error


def _reported(store, job) -> dict:
    """One job as the ``job_state`` payload, on every branch of the verb.

    ``dry_run`` RIDES UNDER ``progress`` AND NEVER BESIDE IT. This verb declares
    ``job_state/1``, ``cli.output`` closes that surface with the four fields
    below and nothing else, so a per verb detail at the top level is an
    undeclared field and a consumer generated from the committed schema rejects
    the envelope. ``progress`` is declared ``object`` with no inner constraint,
    which is where a detail belongs. U51 paid for that distinction on the two
    outbound verbs and ``adopt.shell.reported`` states it in the same words; the
    conformance guard drove this branch and refused the first cut of this key.

    IT IS ON EVERY BRANCH because it is the machine-readable half of the warning
    beside it, and the two must not be able to disagree about one job. The
    default renderer prints a verb's outcome, its warnings and its run id and
    nothing of its payload, so the warning is what a person meets and this key is
    what a script reads.
    """
    progress = dict(jobs.progress(store, job.job_id))
    progress[DRY_RUN] = _is_rehearsal(job)
    # R-757, beside the rehearsal flag and read the same way, so a second ask
    # that is handed an open job can see which comparison that job will make.
    progress[FULL] = _is_full(job)
    # R-349, under ``progress`` for the reason above. Read from the same files
    # ``job show`` reads, so the two surfaces cannot disagree about one item.
    outcomes = backup_facts.read_outcomes(job.job_id)
    if outcomes is not None:
        progress[OUTCOMES] = outcomes
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": progress,
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
    parser.add_argument(
        "--full",
        action="store_true",
        dest="full",
        help=(
            "list the remote folder by folder instead of in one recursive pass, "
            "which takes most of an hour on a large library and does not depend "
            "on the recursive listing being complete"
        ),
    )
    parser.set_defaults(_handler=backup_library)


def frozen_payload(dry_run: bool, full: bool = False) -> dict[str, Any]:
    """What the queued job carries, and the only thing the resume is rebuilt from.

    ``bool`` rather than the argparse value straight through, so the payload holds
    a JSON boolean rather than whatever truthy object a caller handed the
    namespace. A payload key that is ``"false"`` as a string is true to every
    reader of it, and the reader here decides whether anything is copied.
    """
    return {DRY_RUN: bool(dry_run), FULL: bool(full)}


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
    if payload.get(FULL):
        argv.append("--full")
    return [*argv, "--job", job.job_id]


def backup_items() -> tuple[str, ...]:
    """The items one backup job carries: one per declared portion.

    DERIVED BY ITERATING THE ENUM, never by naming the two portions here. A list
    in this file is a second declaration of the set ``backup_facts.Portion``
    already owns, and the two disagree the day somebody adds a third portion:
    the planner would build an entry nothing claims, and the queue would run two
    thirds of a backup with a green suite. This is the same rule the seam
    decisions state as P3, that a name quantifying over a set derives it at run
    time.

    AND IT IS WHY THE ITEMS ARE NOT DERIVED FROM ``plan_backup``. The plan would
    be the more direct answer and it cannot be taken: planning resolves rclone,
    reads the process table and stats the library root, so items built from it
    would make queueing refuse on a machine where the work would have run fine
    once claimed. The enum needs nothing from the machine, and ``plan_backup``
    builds one entry per member on both of its paths, so the item set and the
    plan's portion set are the same set from the same source.
    """
    return tuple(str(portion) for portion in backup_facts.Portion)


def _refuse_an_empty_job(store, job) -> None:
    """Refuse to drive a backup job that has no items, rather than succeeding at it.

    THE JOB THIS CATCHES WAS QUEUED BY A BUILD THAT COULD NOT RUN IT. Before this
    unit ``backup_library`` called ``enqueue`` with no ``item_ids`` at all, and the
    queue is a durable file whose schema version this unit does not change, so a
    person who upgrades still has those jobs sitting in it. Binding the handler is
    what makes them drivable, and driving one is the exact hazard this unit exists
    to prevent: ``jobs.drive`` transitions a job whose item count is zero straight
    to SUCCEEDED, because nothing was attempted and nothing failed. The person
    resumes a backup filed weeks ago and is told it succeeded, over a library
    nothing copied.

    A REFUSAL RATHER THAN A REPAIR. Filling the items in would be the friendlier
    answer and it is the wrong one: the payload was frozen by a build with a
    different idea of what a backup job is, and inventing items for it here would
    run work under a configuration snapshot nobody checked against this shape. The
    remedy tells the person to file a new one, which costs a command and is honest.
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
    """The open job that already IS the backup being asked for, or None.

    Returns the job WITH the configuration it was frozen against, and None in that
    second place when the configuration could not be rebuilt.

    THE VERB PRINTS AN IDENTIFIER AND APPEARS TO HAVE DONE NOTHING, which is the
    shape that invites typing it again, and until R-223 closed the second
    invocation filed a second job. Each job takes its own driver lock, so the
    locks do not see each other, and two drivers then run ``rclone sync`` into one
    mirror at once.

    A TWIN IS THE SAME REQUEST, FOR THE SAME LIBRARY, AGAINST THE SAME PLACE. The
    same verb, the same library identity, the same rehearsal flag, and a frozen
    configuration sharing this one's mirror OR its archive root, since two syncs
    into one mirror interleave and two rotations over one archive root are each
    other's purge. The database snapshot root is not compared: every snapshot is
    its own dated folder, so two of them do not touch. The library is compared
    because the envelope says "this is your backup", and a job copying another
    library is not.

    THE REHEARSAL FLAG IS READ THE WAY THE WORK BODY READS IT, ``bool`` of one
    key, and the rest of the payload is not compared, THE COMPARISON MODE
    INCLUDED (R-757): a fast and a full backup write to one mirror, so they are
    the same claim on the destination, and the job handed back says which mode
    it is under ``progress``. :func:`backup_argv`
    already tolerates a key a later build may add, and whole-payload equality
    would make every job queued before such a build a stranger to every ask
    after it. A rehearsal and a real run stay two jobs: a rehearsal copies
    nothing, and answering a request for a real backup with an open rehearsal
    would hand a person a job that will never copy a byte.

    THE DESTINATIONS ARE THE JOB'S FROZEN ONES (KTD9), because those are where
    its driver will write whatever the file on disk says today. A job whose
    configuration cannot be rebuilt is a twin and not a stranger: could not read
    is not somewhere else. Only the configuration's own failures are caught, so
    a defect in the rebuild stays loud, and the warning for this case claims no
    destination because none was read.

    A JOB WITH NO ITEMS IS SKIPPED. It was queued by a build with no worker,
    :func:`_refuse_an_empty_job` refuses to drive it, and reporting it would
    answer a request for a backup with one that cannot happen.

    ONLY WHAT IS OPEN IS ASKED FOR. A failed or cancelled backup is a recorded
    answer and not a claim on the destination, and the queue's history grows for
    ever across every verb, so the terminal rows are never read at all.
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
    job, frozen: config.Config | None, *, asked_full: bool | None = None
) -> dict[str, str]:
    """The one warning a reported twin carries, in the JOB's terms.

    WHEN THE ASK AND THE JOB DIFFER IN MODE, THE SENTENCE SAYS SO (R-757). A
    person who asked for the full comparison and is handed an open fast job
    would otherwise resume it, watch a backup complete, and find doctor still
    asking for a full one. The job is still reported and nothing is filed,
    because the two write to one mirror.

    The destinations named are the frozen ones, because a twin can match on the
    archive root alone while its mirror differs from the one on disk today, and
    naming the live mirror would tell a person their new destination is being
    backed up by a job that will never write to it.
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
            f". It will run the {held} comparison and this ask was for the "
            f"{asked} one, so cancel it first if that is the one wanted"
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
    """Freeze the rehearsal flag and queue, or continue the job already queued.

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
            # RECONCILE FIRST. A resume arrives after something stopped, and a
            # claim left behind by a driver that died is state the queue cannot
            # see for itself.
            job = jobs.reconcile(store, ctx.args.job)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _refuse_an_empty_job(store, job)
                # The step that was missing until this unit. Everything above this
                # line already worked; nothing below it ever ran a portion. A job
                # every one of whose items failed raises out of here rather than
                # reaching the report, which is correct: the engine has already
                # recorded the job as failed and the refusal carries the item's
                # own cause.
                try:
                    _, warnings = ctx.run_job(store, job)
                except CratekitError as exc:
                    # THE THIRD EXIT, and it is not the one below. ``jobs.drive``
                    # raises from inside the drive when EVERY item failed, so a
                    # rehearsal in which nothing ran leaves here rather than
                    # through the re-raise further down, and an advisory placed
                    # only there would miss exactly the run that copied least.
                    _raise_refusal(exc, job)
                job = jobs.get(store, job.job_id)
            # A JOB THAT ENDED BADLY IS NOT AN OK EXIT, and this is the only
            # place that can say so. ``jobs.drive`` raises only when EVERY
            # attempted item failed; a run where the mirror completed and the
            # database did not returns normally with the job recorded failed, so
            # without this the verb exits 0 over half a backup. That is the merge
            # bar's "a clean report over state the tool could not read", and it is
            # the same sentence ``refusal_for`` enforces one layer down: a portion
            # that failed decides the run even when the other completed, because a
            # person told the backup succeeded stops looking and the half that
            # failed published no age.
            #
            # IT SITS OUTSIDE THE ``is_open`` BRANCH, and the first draft had it
            # inside. That draft answered the run that closes the job and got the
            # SECOND look at it wrong: a job already FAILED on entry is not open,
            # so the drive is skipped, and the check was skipped with it. Asking
            # twice about a half failed backup then answered "failed" once and
            # exit 0 for ever after, which is the same silence the check exists to
            # break. Out here it answers the same way however many times it is
            # asked.
            #
            # A CANCELLED JOB RAISES TOO, deliberately. An interrupt leaves work
            # unfinished, and a person who stopped a backup is owed a non zero
            # exit rather than a report that reads like a completed one.
            # SUCCEEDED carries no cause, so it is not reached by this at all.
            #
            # THE ENGINE'S OWN CAUSE IS RE-RAISED rather than a new one built
            # here. It already carries the counts, the retryable flag (which
            # follows the items, R-380), the remedy those items earned, and the
            # failing item's cause nested inside it, and a second wording for one
            # condition is how the two come to disagree about which one a run
            # met.
            #
            # THE MAPPING IS THE SHARED ONE AND THE EXIT IS THIS VERB'S OWN
            # (R-290). ``raise_for_state`` decides WHETHER the job leaves as a
            # refusal and as which type, a parked job as ``JobBlocked``, and
            # ``_raise_refusal`` adds the rehearsal word on the way out, keeping
            # that type.
            try:
                jobs.raise_for_state(job)
            except CratekitError as exc:
                _raise_refusal(exc, job)
            reported = _reported(store, job)
            # READ BACK HERE AND NOWHERE INSIDE THE ITEM. This is the same call
            # the work body deliberately does not make under the driver, and the
            # position is the whole point: an unreadable fact file refuses the
            # COMMAND here, where the person sees it and the already durable job
            # keeps its state, instead of failing an item whose transfer
            # completed and sending every later resume to repeat the transfer.
            #
            # AGAINST THE JOB'S FROZEN CONFIGURATION, not the one on disk. The
            # item published its age under ``jobs.frozen_config(job)``, and
            # ``config.state_path`` resolves the fact file under the configured
            # library, so reading with a live configuration that names a different
            # library reports a different file from the one this run wrote. The
            # envelope describes THIS job, so it answers from the configuration
            # this job ran against.
            #
            # AND ITS REFUSAL IS THE THIRD ONE THIS BRANCH CAN RAISE, which the
            # first cut of this unit left outside the rehearsal word. Its message
            # opens "the backup ran and the age it published cannot be read
            # back", which frames the failure as an age a real transfer wrote,
            # and over a rehearsal that frame is false in exactly the direction
            # R-221 exists to close: nothing was published, so the file being
            # unreadable is a corrupt file and not a lost record of this run. The
            # step says which kind of run it was rather than a second wording of
            # the condition.
            try:
                reported["ages"] = published_ages(jobs.frozen_config(job))
            except CratekitError as exc:
                _raise_refusal(exc, job)
            # THE SHARE WARNING IS ASKED HERE AND NOT READ FROM THE ITEM. The work
            # body's report does not leave a claimed item (R-221), so the warning
            # the plan carries would reach nobody. It is a fact about the frozen
            # configuration rather than about how the transfer went, so asking the
            # configuration again is the same answer rather than a second rule.
            #
            # THE SNAPSHOT IDENTITY WARNING RIDES WITH IT, for the same reason and
            # with a sharper cost: left on the plan alone, every backup of a
            # library with no recorded identity would write an unmarked snapshot
            # in silence, and the first word of it would be a restore refusing.
            #
            # THE REHEARSAL WORD RIDES WITH THEM AND IS ASKED OF THE JOB. It is
            # not a fact about the configuration like the other two, it is a
            # fact about what this job was frozen to do, and it is R-221's own
            # cost: without it a rehearsal resumes to succeeded with two items
            # done and true ages, and nothing says it copied nothing.
            warnings = (
                *warnings,
                *map(dict, backup.absent_analysis_share(jobs.frozen_config(job))),
                *map(dict, backup.snapshot_identity_warning(jobs.frozen_config(job))),
                *_rehearsal(job),
                # R-757. From what ``_reported`` just read, so the sentence and
                # the payload beside it are one reading of one file.
                *comparison_warning(reported["progress"].get(OUTCOMES)),
            )
            return ctx.envelope(data=reported, warnings=warnings)
        payload = frozen_payload(ctx.args.dry_run, ctx.args.full)
        found = _open_twin(
            store,
            handler_key=ctx.entry.handler_key,
            dry_run=payload[DRY_RUN],
            cfg=cfg,
        )
        if found is not None:
            twin, frozen = found
            # THE SAME ENVELOPE A FIRST ASK GETS, plus one warning, so a script
            # reading ``data.job_id`` continues the backup that exists whether it
            # asked first or second.
            #
            # THE OTHER WARNINGS DESCRIBE THE JOB REPORTED, for the reason the
            # resume branch above gives: the envelope describes THIS job, which
            # runs under the configuration it was frozen against. The live one
            # stands in only when the frozen one could not be rebuilt.
            described = cfg if frozen is None else frozen
            return ctx.envelope(
                data=_reported(store, twin),
                warnings=(
                    _already_queued(twin, frozen, asked_full=payload[FULL]),
                    *map(dict, backup.absent_analysis_share(described)),
                    *map(dict, backup.snapshot_identity_warning(described)),
                    # THE TWIN'S OWN, not this ask's. A rehearsal and a real run
                    # are never twins, so the two always agree here, and reading
                    # the job is what keeps that a property rather than a
                    # coincidence this branch depends on.
                    *_rehearsal(twin),
                ),
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            # ONE PORTION IS ONE ITEM. Without this the queue holds a job with
            # nothing to claim, and ``jobs.drive`` transitions a job whose item
            # count is zero straight to SUCCEEDED, so the driver reports a backup
            # that copied nothing.
            item_ids=backup_items(),
            cfg=cfg,
        )
        # Said at queue time as well, because a person who never resumes the job
        # by hand would otherwise learn about the share only from a later run.
        # The same argument carries the rehearsal word here: the detached child a
        # resume spawns writes to a log nobody is watching, so the moment the
        # identifier is handed over is the one moment this is certain to be read.
        return ctx.envelope(
            data=_reported(store, job),
            warnings=(
                *map(dict, backup.absent_analysis_share(cfg)),
                *map(dict, backup.snapshot_identity_warning(cfg)),
                *_rehearsal(job),
            ),
        )


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
        # RETRYABLE, and the flag is load bearing. A transfer that exited non
        # zero is a remote that answered the plan and then did not, a dropped
        # connection or a remote that went away mid copy, and the portion runs
        # again exactly as it did. The job cause reads this flag (R-380) and so
        # does ``jobs.retry`` before it re-arms the portion (R-390): left at
        # the default, every failed backup transfer was recorded as permanent
        # and the resume the per portion ledger exists for was refused.
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
    portion: backup_facts.Portion | None = None,
    cfg: config.Config | None = None,
    runner=backup.subprocess_runner,
    now: datetime | None = None,
    process_lister=None,
    read_back: bool = True,
    outcome_to: tuple[str, str] | None = None,
) -> dict:
    """Do the backup one queued job asks for, and report what actually happened.

    PURE OF THE JOB ENGINE ON PURPOSE, taking the payload rather than a job, the
    way ``run_master`` does one package over and for the same reason: the
    properties that matter most about this body, that a failed run publishes no
    age and that the age it does publish is the one the session will read, are
    then drivable without a configured machine, a job store and a claimed item.

    ``portion`` NARROWS THE RUN TO ONE HALF, and ``None`` runs the whole plan the
    way every caller before the handler did. One body rather than two, so the
    properties above stay drivable through the same function the queue uses; and
    a default that changes nothing, so the callers and tests that predate the
    binding keep measuring what they measured.

    ``read_back`` IS OFF FOR THE QUEUED CALLER, and the reason is narrower than
    the one first written here, which was measured and found false rather than
    argued. The claim was that a real run's unreadable fact file would fail an item
    whose transfer had already completed. It cannot: ``run_backup`` publishes
    through ``backup_facts.record``, which READS the file before it writes, so an
    unreadable file fails inside the engine first and the portion never reaches
    this report. The two are the same reader and they fail together.

    WHERE THEY COME APART IS A REHEARSAL. ``run_backup`` publishes nothing for a
    dry run, so nothing else touches the fact file and this read would be the only
    one. Under the driver that fails an item over a rehearsal that copied nothing
    and changed nothing, and every resume repeats it. So the read belongs where a
    failure refuses the COMMAND instead, which is the shell's own resume branch,
    and the handler, which discards this report anyway, asks for it not to happen
    here.

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

    :func:`handle` PASSES IT, and the fallback is what the unqueued callers take.

    ``outcome_to`` IS THE FAILURE CHANNEL OF R-349, a job and item identifier
    pair. When the finished run earns a refusal, the rendered outcome is written
    under that pair BEFORE the refusal is raised, so ``job show`` can name the
    rclone command that failed. It is written here and not returned, because a
    refusal is the only thing that leaves the item FAILED, and FAILED is the only
    state ``jobs.retry`` re-arms, and since R-390 it re-arms it only over a
    cause that is retryable, which :func:`refusal_for` marks a transfer exit
    as. The success channel is :func:`handle`'s ``Produced``.
    """
    cfg = _load() if cfg is None else cfg
    dry_run = bool(payload.get(DRY_RUN))
    try:
        plan = backup.plan_backup(
            cfg,
            now=now,
            process_lister=process_lister,
            full=bool(payload.get(FULL)),
        )
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
    if portion is not None:
        # NARROWED RATHER THAN FILTERED AT EXECUTION. ``run_backup`` iterates the
        # plan it is handed, so a plan holding one portion is how one portion runs
        # without a second execution path beside the one every other caller uses.
        # ``archive_keep`` rides the rebuilt plan rather than being passed again,
        # which is the rule ``BackupPlan``'s own docstring states: taken twice, the
        # two copies can disagree and the rotation deletes what the preview kept.
        #
        # ``plan.portion`` RAISES for a portion the planner did not build. That is
        # unreachable today and is left loud on purpose: ``plan_backup`` builds one
        # entry per declared portion on both of its paths, so the only way to reach
        # it is to add a member to ``backup_facts.Portion`` without teaching the
        # planner about it, and a KeyError naming the portion is a better answer
        # there than a run that quietly does one half.
        #
        # ``replace`` RATHER THAN A CONSTRUCTOR CALL, and the comment above is why:
        # naming ``stamp`` and ``archive_keep`` again here would be the second copy
        # it warns about, in the one function that rebuilds the plan. A field added
        # to ``BackupPlan`` later rides through this untouched, where a constructor
        # call would silently drop it and narrow the run in a way no test asks
        # about.
        plan = replace(plan, portions=(plan.portion(portion),))
    try:
        outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
    except backup_facts.BackupFactsUnreadable as exc:
        # THE ENGINE PUBLISHES THROUGH THIS FILE AND CAN FAIL ON IT, and until
        # this unit nothing was in a position to notice. ``run_backup`` calls
        # ``backup_facts.record`` after a portion's last command returns zero, and
        # ``record`` READS the file before it writes, so a fact file that cannot be
        # parsed raises here with the transfer already done.
        #
        # WHY IT IS TRANSLATED. ``BackupFactsUnreadable`` is a plain ``Exception``
        # rather than a ``CratekitError``, so under the driver it lands in
        # ``jobs.drive``'s ``except Exception`` and is recorded as
        # ``internal-error`` carrying ``report-defect``. A person whose state
        # directory holds one bad file would be told to file a bug against this
        # program, and every retry would repeat the whole transfer to reach the
        # same line. The remedy travels from the exception for the reason
        # :func:`published_ages` gives: that class names three conditions and one
        # of them is a directory permission, which repairing a file does not fix.
        #
        # THE ITEM STILL FAILS, and that is right rather than a compromise. The
        # age is what a destructive session reads, so a copy whose age cannot be
        # published is not yet the protection the person asked for. What changes
        # is that they are told which file to fix.
        raise refuse(
            "backup-facts-unreadable",
            f"the {portion or 'backup'} portion transferred and the age it "
            f"publishes cannot be written: {exc}. The copy exists; the fact a "
            f"destructive session reads does not",
            remedy=Remedy(str(exc.remedy)),
            origin=("backup", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
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
    # that decision from the wrong layer, and that is still true.
    #
    # THE PRUNE REACHES THIS REPORT, though no longer every reader of it.
    # ``_prune_archive`` classifies its own listing and purge return codes,
    # ``run_backup`` records the result on the portion, and ``outcome_payload``
    # renders it under ``warnings``, so the condition arrives in the engine's own
    # vocabulary rather than through a second reading of ``results`` here.
    #
    # AND IT LEAVES A CLAIMED ITEM NOW (R-349). :func:`handle` commits this
    # report as the item's artifact on success, and ``outcome_to`` writes it on a
    # refusal, so ``job show`` and the ``--job`` envelope read it back per item.
    # ``refusal_for`` IS APPLIED UNCHANGED AND UNQUALIFIED OVER A NARROWED RUN,
    # and the temptation this comment exists to refuse is to add a condition on
    # top of it. Its three branches already answer the question a single portion
    # asks: a portion that ran returns None, a portion whose transfer came back
    # non zero returns ``backup-transfer-failed``, and a portion the engine
    # refused returns that refusal with its RESERVED remediation, so a person
    # meets ``quit-rekordbox`` or ``mount-library-volume`` rather than a generic
    # one. Its whole-run sentence, that a refusal only ends the run when nothing
    # ran, is a statement about a run holding two portions; a run holding one is a
    # run in which nothing ran whenever that portion did not.
    #
    # THE FIRST DRAFT OF THIS UNIT SUPPRESSED THE REFUSAL when the other portion
    # would run, so that backing up with rekordbox open did not report a failure.
    # That is unrecoverable and this is where it would come back. ``complete_item``
    # writes ``done``, and ``jobs.retry`` re-arms only ``failed`` and ``claimed``,
    # saying so in its own docstring: "Items that are DONE stay done." The person
    # then quits rekordbox, resumes, and nothing happens, for ever, over a job
    # reporting SUCCEEDED. Failing the item is louder and it is the only one of the
    # two a resume can finish.
    refusal = refusal_for(outcome)
    if refusal is not None:
        if outcome_to is not None:
            raise _with_outcome_recorded(refusal, outcome, outcome_to)
        raise refusal
    # THE FLAG COMES OFF THE OUTCOME NOW and is not written on here. It was
    # written on here, by the one caller that thought of it, which made it a
    # field that is correct where somebody remembered and absent everywhere
    # else: the queued path renders no report at all and its envelope carried no
    # word of it, which is R-221. ``BackupOutcome`` records the run it was, so
    # the renderer answers for every reader rather than for this one.
    #
    # ``ages`` beside it is what makes the claim checkable rather than asserted,
    # since a rehearsal leaves every portion exactly as it found it.
    report = backup.outcome_payload(outcome)
    if read_back:
        report["ages"] = published_ages(cfg, now=now)
    return report


def _with_outcome_recorded(
    refusal: CratekitError, outcome: backup.BackupOutcome, outcome_to: tuple[str, str]
) -> CratekitError:
    """Write a failed run's outcome, and return the refusal to raise (R-349).

    THE REFUSAL IS RETURNED UNCHANGED when the write succeeds, object for object,
    so the item's cause is exactly what it was before this channel existed.

    WHEN THE WRITE FAILS, THE REFUSAL STILL WINS. The transfer failure is what the
    person has to act on; a record of it that could not be written is secondary,
    and letting the ``OSError`` escape would replace ``backup-transfer-failed``
    with ``internal-error`` and ``report-defect``. It is not chained with
    ``from`` either, because ``cause.classified`` walks the chain and a
    permission error under it would reclassify the refusal. The loss is said as
    a step instead, so ``job show`` printing no commands for this item is not
    read as an item that ran none.
    """
    job_id, item_id = outcome_to
    try:
        backup_facts.write_outcome(job_id, item_id, backup.outcome_payload(outcome))
    except OSError as exc:
        cause = refusal.cause
        return rebuilt(
            refusal,
            replace(
                cause,
                remediation=replace(
                    cause.remediation,
                    steps=(
                        *cause.remediation.steps,
                        f"the record of which commands this run ran could not be "
                        f"written, so job show will not list them: {exc}",
                    ),
                ),
            ),
        )
    return refusal


def _staged(final):
    """The staging path beside ``final``, so the engine's rename is atomic."""
    return final.with_name(final.name + ".staged")


def handle(job, item, cfg) -> "jobs.Produced | None":
    """Back up one portion. The per-item worker behind ``handler_key`` backup.run.

    THE ITEM NAMES THE PORTION, and there is nothing in the payload to read it
    from instead. That is the difference from ``master``, whose payload holds the
    one recording its single item also names: here the payload carries the
    rehearsal flag and the item carries the half of the library this claim is for,
    so reading the payload could not select a portion at all.

    IT RETURNS THE OUTCOME AS ITS ARTIFACT (R-349). rclone writes to the remote
    and leaves nothing local, so until R-349 this returned nothing and the
    report of which commands ran reached nobody. The rendered outcome is now the
    local file: staged beside its final path and handed back as a ``Produced``,
    so the engine owns the flush-then-rename exactly as it does for ``master``'s
    encode, and the item flips to done only once the record is durable.

    ONLY A SUCCESS TAKES THIS CHANNEL. A run that earned a refusal raises out of
    :func:`perform_backup`, which writes the same record directly first. Routing
    a failure through ``Produced`` would commit it and COMPLETE the item, and a
    done item is never re-armed: the person quits rekordbox, resumes, and gets a
    SUCCEEDED job over half a backup.

    ``cfg`` IS THE CONFIGURATION THIS JOB WAS FROZEN AGAINST (KTD9) and it is
    passed straight through. Nothing in this function loads one, and the guard in
    ``tests/test_handlers.py`` that says so reads only this function's own body and
    states in its own docstring that it cannot see a reload reached through a
    helper. This module HAS such a helper, ``_load``, used by the unqueued path, so
    the guard would not notice a call to it. Said here as well as there, because a
    guard described as closing a hole it only narrows is the thing a later reader
    trusts. A backup queued against one remote and claimed after the person
    reconfigured their destinations would otherwise copy the library somewhere they
    did not ask for and publish an age naming a destination the queued run never
    targeted.
    """
    named = str(item.item_id or "")
    try:
        portion = backup_facts.Portion(named)
    except ValueError:
        # THE SAME FUNCTION THAT QUEUED THE ITEMS names them in the refusal, so
        # what the message calls the declared portions is what a job would
        # actually have been given. Re-deriving the set here would be the second
        # declaration ``backup_items`` exists to prevent, and the copy that goes
        # stale is the one in the error path, which nobody reads until the day it
        # is wrong.
        declared = backup_items()
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
            remedy=Remedy.REPORT_DEFECT,
            origin=("backup", "cli"),
            detail={"item_id": named, "portions": list(declared)},
        ) from None
    # BEFORE the attempt, so the record on disk is only ever this attempt's.
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
    # ``atomic_write_bytes`` creates the directory owner only (P1) and the file
    # at 0600; the engine's ``commit_artifact`` then renames it over any record a
    # failed attempt of this item left, so the file always describes the latest.
    #
    # A RECORD THAT CANNOT BE STAGED DOES NOT FAIL THE ITEM. By this line the
    # transfer completed and the engine published its age, so the backup exists.
    # Failing here would record ``internal-error`` over a good backup and send
    # the retry to repeat the whole transfer. The item completes with no
    # artifact instead, which is exactly what it did before R-349.
    try:
        config.atomic_write_bytes(backup_facts.encode_outcome(report), staged)
    except OSError:
        return None
    return jobs.Produced(staged=staged, final=final)


__all__ = [
    "ALREADY_QUEUED",
    "COMPARISON",
    "DRY_RUN",
    "FULL",
    "OUTCOMES",
    "REHEARSAL",
    "backup_argv",
    "backup_items",
    "backup_library",
    "build",
    "comparison_warning",
    "frozen_payload",
    "handle",
    "perform_backup",
    "published_ages",
    "refusal_for",
    "rehearsal_warning",
]
