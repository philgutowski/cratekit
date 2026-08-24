"""``crate restore list`` and ``crate restore run``: the history, and its one undo.

WHAT THIS MODULE IS FOR. A capture nobody can spend is a directory of files, and
until this module existed the whole restore engine was reachable only from a
test. :mod:`cratekit.core.restore` decides and performs; this decides what the
person asked for, asks the one question R34 says has to be asked separately, and
then holds ONE destructive session around everything that follows.

ONE SESSION SPANS THE WHOLE VERB, and that is the second obligation
``tests/_pending.py`` registered against this module rather than a nicety. The
shape being refused is specific and was found by review: a plan that takes the
library lock and gives it back, followed by a run that takes it again, leaves a
window in which a second process passes the same gates and commits, after which
the run copies a snapshot over a commit its plan was built before.
:func:`cratekit.core.restore.recovery_session` is entered once, and both halves
of the restore run inside it. The off-machine half takes the already-open
``held.guard`` as its ``gates`` seam rather than acquiring its own, which is the
one wiring call U32 proved at the seam and could not make, because
``cratekit.core`` may not import the modules layer and
:mod:`cratekit.modules.tools.backup` is in it.

THE GATE IS ASKED BEFORE THE SESSION IS OPENED, and the ordering is forced
rather than chosen. ``restore.run.confirm`` is ``explicit``, so R34 makes it
answerable only by a separate recorded act against a run; the invocation that
discovers it exits DECISION_REQUIRED. A session opened before that question
would be opened, refused or held for nothing, and closed again on every drive
that only ever existed to raise the question. Worse, on a machine that has never
acknowledged a backup the session refuses FIRST, so the question a person has to
answer would never be asked at all and the verb would be unreachable on exactly
the library a restore is for.

WHAT THE DIGEST IS OVER, said plainly because the registry calls its source
"plan" and this is not the step list. The step list cannot exist before the
session, because :func:`cratekit.core.restore.plan` refuses without an open one,
so approving it would mean showing a person something only computable after the
lock was taken. What is digested instead is the restore's IDENTITY: the session
being restored, its recorded change summary, the sessions being discarded, and
whether the off-machine mirror is being pulled first. That is the value that
moves when the world moves, which is the whole job of a decision digest: a later
session committing between the offer and the answer changes the summary, the
digest moves, and the recorded decision is refused as stale. The step list is
then derived under the lock and checked again there, and
``restore._assert_override_names_them`` refuses independently when the discard
set does not name what a restore would actually destroy, so nothing here rests
on the digest alone.

NO WORKFLOW LABEL IS PASSED TO THE SESSION, and the whole verb is therefore
recorded under ``core.restore.CAPTURE_RESTORE_WORKFLOW``. An earlier version of
this paragraph said the point was to keep that label and
``backup.RESTORE_WORKFLOW`` distinguishable in the log, which is FALSE HERE and
was measured false by an independent review: handing the off machine half the
already open guard means ``backup._restore_gates`` returns that guard instead of
opening a session of its own, so its label never reaches the log at all, on any
path. One acquisition and two labels are mutually exclusive, and this unit chose
the acquisition. The consequence, that the session log cannot tell a run which
pulled a mirror from one which did not, is recorded rather than papered over.

Layer: modules. It names :mod:`cratekit.cli.output` and
:mod:`cratekit.cli.exit_codes` and nothing else from the command-line layer, and
both of those are foundation-ranked under KTD25 for the reason
``adopt.apply_cli`` gives at length: a modules-layer file reaching for
``registry.Entry`` to annotate a builder is the layering violation KTD23
refuses, while the output contract and the reserved-cause table are ranked below
every verb on purpose.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ALIASED, because this package holds TWO modules called ``exit_codes`` and
# they are different things. ``cratekit.cli.exit_codes`` is the reserved-cause
# table, which is what a refusal's remediation is looked up in;
# ``cratekit.core.exit_codes`` is the status vocabulary and the remedy tokens.
# Both are foundation-ranked and both are legitimately needed here, so the one
# whose name would otherwise be ambiguous says what it is instead.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, restore
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import backup

#: What ``review_set`` calls this listing. NOT a :class:`cratekit.core.review.Queue`
#: member, and the absence is the point rather than an oversight. Every declared
#: queue is an ADJUDICATED surface, and ``tests/test_review_queue.py`` holds the
#: enum and the surface table to being the same set in both directions, so a
#: member added for a listing nobody adjudicates would break that agreement and
#: would promise a verdict this verb never asks for. The schema's ``queue`` field
#: is a string naming the set, and this is the honest name for it.
LISTING = "restore"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token rides through from the configuration error that raised it,
    so "no config at all" and "config written by a newer build" keep their
    different answers all the way out to the shell (D2).
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("session.restore_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _refused(exc: backup.BackupRefused) -> CratekitError:
    """One off-machine refusal, in the vocabulary every other layer reads.

    ``backup.Refusal`` is the backup module's own diagnosis set and it is NOT a
    cause: nothing downstream can classify a bare exception, so it would arrive
    as an internal error with its remediation discarded, which is exactly the
    collapse KTD25 exists to stop. Its slug is already reserved in
    ``cratekit.cli.exit_codes`` with a code and a per-slug remediation, and that
    reservation is what is read here rather than a second opinion written beside
    it: ``no-snapshot-available`` carries steps, ``rclone-missing`` carries an
    install token, and a class-level default here would throw both away.

    THE SLUG IS CARRIED THROUGH UNCHANGED rather than folded into a nearby
    reason. Nine diagnoses flattened into one is a person being told to mount a
    volume when what is missing is a program, and the reservation table already
    decided that each of them is worth telling apart.
    """
    slug = str(exc.refusal)
    return CratekitError(
        Cause(
            reason=slug,
            message=exc.detail,
            remediation=reservations.remediation_for(slug),
            origin=("modules.tools.backup", "session.restore_cli"),
            detail={"refusal": slug},
        )
    )


# ---------------------------------------------------------------------------
# restore list
# ---------------------------------------------------------------------------


def build_list(parser, entry) -> None:
    """Declare the listing's arguments, which are none. Parameters unannotated.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this layer importing the one above it. See the module docstring.
    """
    del entry
    parser.set_defaults(_handler=list_restorable)


def _listed(entry: restore.Restorable) -> dict[str, Any]:
    """One session as a listing row: when, what, how much, and whether it is spendable.

    ``unusable`` IS REPORTED RATHER THAN FILTERED, which is
    :class:`cratekit.core.restore.Restorable`'s own decision carried out to the
    surface. A session whose capture somebody deleted by hand is exactly the
    session a person is about to go looking for, and dropping it from the list
    answers their question with silence.
    """
    return {
        "session_id": entry.session_id,
        "started": entry.started,
        "workflow": entry.workflow,
        "restorable": entry.restorable,
        "unusable": entry.unusable,
        "change": [
            {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
            for tree in entry.change.trees
        ],
    }


def list_restorable(ctx) -> Envelope:
    """Every recorded session, newest first, with what it changed.

    READ ONLY, AND OUTSIDE THE SESSION GATES. Listing resolves no path on the
    library volume and writes nothing, so requiring a backup acknowledgment and
    the library lock to answer "what could I roll back to" would make the
    question unanswerable on precisely the machine that needs it: one whose
    library is busy, or one where the thing a person is deciding is whether they
    have a backup at all.

    ``unresolved`` IS ZERO AND IS NOT A COUNT OF SESSIONS. It means what is OPEN
    in an adjudication queue, and nothing here awaits a verdict: a recorded
    session is a settled fact and a listing is not a backlog. Reporting the
    number of sessions there would tell a person they have work they do not,
    which is the reasoning ``deletion.tombstone_cli`` gives for the same field.
    """
    cfg = _load()
    listed = restore.list_sessions(cfg)
    return ctx.envelope(
        data={
            "queue": LISTING,
            "items": [_listed(entry) for entry in listed],
            "unresolved": 0,
        }
    )


# ---------------------------------------------------------------------------
# restore run
# ---------------------------------------------------------------------------


def build_run(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    THERE IS NO ``--yes`` AND NO ``--confirm``. The confirmation is the recorded
    answer to the explicit gate and there is no flag anywhere in this package
    that stands in for one (R34).

    ``--discard`` IS REPEATED IDENTIFIERS AND NEVER A BOOLEAN, which is
    :func:`cratekit.core.restore.plan`'s requirement carried to the surface
    unchanged. A restore reaching back past a later session that committed is
    destroying work somebody did on purpose, and a flag saying "yes" is an answer
    to a question nobody read.
    """
    del entry
    parser.add_argument(
        "session_id",
        nargs="?",
        default=None,
        help=(
            "the write session to roll back to; omitted means the newest one "
            "whose capture is spendable"
        ),
    )
    parser.add_argument(
        "--discard",
        action="append",
        default=[],
        metavar="SESSION_ID",
        dest="discard",
        help=(
            "a later session whose committed work this restore destroys, named "
            "explicitly; repeat once per session, and the set must match what "
            "the refusal listed"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="walk every step and perform none of them, under the same gates",
    )
    parser.add_argument(
        "--from-backup",
        action="store_true",
        dest="from_backup",
        help=(
            "pull the database back from the off-machine mirror first, for the "
            "case where the volume itself was replaced and no local capture "
            "survived"
        ),
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        metavar="STAMP",
        help="which dated off-machine snapshot to pull; the newest by default",
    )
    parser.add_argument(
        "--include-mirror",
        action="store_true",
        dest="include_mirror",
        help=(
            "pull the music and everything else the mirror carried, not only the "
            "database; hundreds of gigabytes, so it is off by default"
        ),
    )
    parser.set_defaults(_handler=perform_restore)


def _newest_restorable(cfg: config.Config) -> restore.Restorable | None:
    """The session a bare ``crate restore run`` means, or None.

    Newest FIRST is :func:`cratekit.core.restore.list_sessions`'s ordering and is
    not re-derived here. RESTORABLE rather than merely newest, because a capture
    somebody deleted by hand is listed on purpose and choosing it by default
    would turn an informative row into a refusal every time.
    """
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
    return None


def _named(cfg: config.Config, session_id: str) -> restore.Restorable:
    """The session a person named, or a refusal that says which of the two is wrong.

    TWO DIFFERENT FACTS, TWO DIFFERENT MESSAGES, and collapsing them is the
    failure this function exists to avoid. "No session has that identifier" sends
    a person to the listing; "that session's capture cannot be spent" sends them
    to a different session, and the row itself already carries the sentence
    saying why. One message for both would send half of them to the wrong place.

    IT REFUSES AN UNUSABLE CAPTURE HERE TOO, and the docstring that used to say
    the opposite was wrong in a way a person met. It claimed the plan refuses one
    under the lock "with the engine's own diagnosis, which is more specific than
    anything this layer could restate". Measured on 2026-08-23, by driving this
    product's OWN retention to delete a capture whose session record stays in the
    log, that diagnosis is a raw errno carrying ``internal-error`` and
    ``report-defect``: a person is told to file a bug about a directory the tool
    removed on purpose, while ``restore list`` sitting beside it explains the
    situation correctly in a sentence.

    SO THE SENTENCE THE LISTING ALREADY COMPUTED IS WHAT IS RAISED, rather than a
    second opinion invented here. ``Restorable.unusable`` is one string produced
    in one place, and both surfaces now say it.

    AND IT REFUSES BEFORE ANY SESSION OPENS, which is the half that matters with
    ``--from-backup``. The off machine pull runs first, so a refusal deferred to
    the plan let two transfers complete and the live companion files be cleared
    before anything looked at whether the capture could be spent at all.
    """
    for entry in restore.list_sessions(cfg):
        if entry.session_id != session_id:
            continue
        if entry.unusable:
            raise CratekitError(
                Cause(
                    reason="restore-record-unusable",
                    message=(
                        f"session {session_id} cannot be restored: {entry.unusable}"
                    ),
                    remediation=Remediation(
                        steps=(
                            "run the restore listing and choose a session whose "
                            "capture is still spendable",
                        )
                    ),
                    origin=("session.restore_cli",),
                    detail={"session_id": session_id, "unusable": entry.unusable},
                )
            )
        return entry
    raise CratekitError(
        Cause(
            reason="restore-record-unusable",
            message=(
                f"no write session on this library is recorded under "
                f"{session_id!r}; the listing verb shows every one that is"
            ),
            remediation=Remediation(
                steps=("run the restore listing to see the sessions this library recorded",)
            ),
            origin=("session.restore_cli",),
            detail={"session_id": session_id},
        )
    )


def _offer(
    chosen: restore.Restorable | None,
    *,
    discarding: Sequence[str],
    from_backup: bool,
    snapshot: str | None,
    include_mirror: bool,
) -> dict[str, Any]:
    """What the person is being asked to approve, as a ``plan/1`` payload.

    THE ITEMS ARE THE HALVES OF THE RESTORE, not its steps, for the reason the
    module docstring gives at length. Each half is named separately because they
    are separately refusable and separately expensive, and an approval that
    could not tell them apart would let a person who meant "roll back one
    session" also authorise pulling a mirror off the network.

    THE CHANGE SUMMARY IS IN THE DIGEST, and that is the field that does the
    work. A later session committing between the offer and the answer changes it,
    so the digest moves and the recorded decision is refused as stale rather than
    honoured against a library that is no longer the one it described.
    """
    items: list[dict[str, Any]] = []
    if from_backup:
        items.append(
            {
                "half": "off-machine",
                "snapshot": snapshot or "newest",
                "include_mirror": include_mirror,
            }
        )
    if chosen is not None:
        items.append(
            {
                "half": "capture",
                "session_id": chosen.session_id,
                "started": chosen.started,
                "workflow": chosen.workflow,
                "change": [
                    {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
                    for tree in chosen.change.trees
                ],
                "discarding": list(discarding),
            }
        )
    return {
        "digest": digest_of({"kind": "restore.run", "items": items}),
        "items": items,
        "totals": {"halves": len(items)},
        "chunk": None,
    }


def _confirm_gate(entry):
    """The explicit confirmation gate off the entry, found by digest source.

    BY ``digest_source`` RATHER THAN BY POSITION. This verb declares two gates
    and the shared cloud-sync one is raised by the guarded writer rather than
    asked here, so indexing ``gates[0]`` would bind this handler to the order
    they happen to be written in and would ask the wrong question the day
    somebody reorders them.
    """
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
                f"there is no question to ask before restoring"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("session.restore_cli",),
            detail={"verb": entry.name},
        )
    )


@dataclass(frozen=True, slots=True)
class RestoreReport:
    """What one restore did, in both halves, so neither can hide behind the other.

    TWO FIELDS RATHER THAN ONE, because a restore has two independently optional
    halves and a single value cannot say which of them ran. ``pulled`` is the
    off-machine transfers by label, empty when the mirror was not asked for;
    ``outcome`` is the capture restore, ``None`` when no session was named. Both
    empty is the honest description of a run that had nothing to do, and it is a
    different fact from either one alone.
    """

    pulled: tuple[str, ...]
    outcome: restore.RestoreOutcome | None
    dry_run: bool


def restore_under_one_session(
    cfg: config.Config,
    *,
    session_id: str | None,
    discarding: Sequence[str] = (),
    dry_run: bool = False,
    from_backup: bool = False,
    snapshot: str | None = None,
    include_mirror: bool = False,
    target: Path | str | None = None,
    identity_provider: object | None = None,
    mount_enumerator: object | None = None,
    runner: object | None = None,
    process_lister: object | None = None,
) -> RestoreReport:
    """Both halves of a restore, inside ONE acquisition of the destructive gates.

    This is the function ``tests/_pending.py`` registered against this module.
    The gates are entered once, by
    :func:`cratekit.core.restore.recovery_session`, and everything after that
    point happens inside the block it yields into: the off-machine pull, the
    plan, and the write.

    ``held.guard`` IS WHAT MAKES IT ONE ACQUISITION. ``backup.plan_restore`` and
    ``backup.run_restore`` each default to taking the library lock themselves, so
    calling them plainly from in here would be three acquisitions with two
    windows in them, and taking the lock a second time IN THIS PROCESS would be
    reported as a foreign holder, which is to say the caller would be told to
    wait for itself. The guard is a pass-through that does nothing, deliberately.

    THE OFF-MACHINE HALF RUNS FIRST when both are asked for, and the order is the
    whole reason they compose. The mirror lays down the database the volume lost;
    the capture then rolls that database and its coupled state back to a recorded
    session. The reverse order would restore a session and then overwrite it with
    whatever the remote happened to hold.

    ``confirmed=True`` IS NOT A FLAG STANDING IN FOR THE DECISION. The explicit
    gate is answered, recorded against a run with its actor, and checked before
    this function is called; ``plan_restore``'s parameter is how a caller states
    that a named decision exists, and R33 is why that module refuses to prompt
    for one itself.

    ``target`` IS A SEAM AND NOT A FLAG, and the verb never passes one. The
    capture half resolves every path it writes from ``cfg.library.root``, and
    :func:`cratekit.core.restore.plan` refuses a session that does not authorise
    that root, so a command line that pointed the mirror half somewhere else
    would put the two halves of one restore on two volumes: the database from the
    remote on a replacement disk, and the coupled state rolled back on the
    configured one. Recovering onto a different volume is a real thing to want
    and it is a different verb, with a different set of gates, which is what
    ``core.restore.bare_metal_session`` exists for. The parameter stays because a
    test needs somewhere to restore that is not this machine's real library.

    ``analysis_roots`` NAMES THE LIBRARY ROOT rather than being left empty. A
    restore replaces the database and everything coupled to it, so anything under
    the library can move, and a watch that names nothing watches nothing while
    still reporting a clean session.

    IT REPORTS BOTH HALVES SEPARATELY, and the earlier shape that returned only
    the capture outcome was wrong in a way a person would have met. A run that
    pulled a whole mirror and named no session returned ``None``, and the verb
    then reported zero steps performed: hundreds of gigabytes moved and the
    output said nothing had happened. ``outcome`` stays ``None`` when no capture
    was spent, because inventing an empty one would report a restore that
    converged over state nothing looked at, and ``pulled`` carries the other half
    so the absence of one is not read as the absence of both.
    """
    watched: tuple[Path, ...] = (Path(cfg.library.root),)
    with restore.recovery_session(
        cfg,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ) as held:
        transferred: tuple[str, ...] = ()
        if from_backup:
            where = Path(target) if target is not None else Path(cfg.library.root)
            try:
                pulled = backup.plan_restore(
                    cfg,
                    target=where,
                    confirmed=True,
                    snapshot=snapshot,
                    include_mirror=include_mirror,
                    gates=held.guard,
                    **_seam("runner", runner),
                    **_seam("process_lister", process_lister),
                )
                ran = backup.run_restore(
                    pulled,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
                    **_seam("runner", runner),
                )
            except backup.BackupRefused as exc:
                raise _refused(exc) from exc
            # THE RESULTS, NOT THE PLAN'S COMMANDS, and the earlier spelling of
            # this line was half of a blocking defect. Reporting the planned
            # labels said a transfer had happened whether or not it had, and
            # ``run_restore`` was returning its results unread, so a restore
            # whose every copy failed reported two completed transfers and exited
            # OK, with the live companion files already cleared. The reading is
            # now in ``run_restore`` where every caller gets it, and this line no
            # longer describes work it did not watch.
            #
            # ONE LABEL PER RESULT, zipped strictly, so a runner returning fewer
            # results than the plan holds commands is a hard failure here rather
            # than a report that quietly lists the shorter of the two.
            transferred = tuple(
                command.label
                for command, _result in zip(pulled.commands, ran, strict=True)
            )
        if session_id is None:
            return RestoreReport(pulled=transferred, outcome=None, dry_run=dry_run)
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=discarding,
            process_lister=process_lister,
        )
        return RestoreReport(
            pulled=transferred,
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
                process_lister=process_lister,
            ),
            dry_run=dry_run,
        )


def _seam(name: str, value: object) -> dict[str, Any]:
    """One injectable seam as keyword arguments, omitted entirely when unsupplied.

    ``backup.plan_restore`` DEFAULTS ITS RUNNER TO A REAL SUBPROCESS and reads
    ``None`` as an explicit choice of nothing, unlike the destructive-session
    helper the module docstring names, which reads ``None`` as "resolve the
    default". Forwarding ``None`` blindly would therefore hand the off-machine
    half a runner that is not callable, so the absent case has to be an absent
    ARGUMENT rather than a null one.

    THE NAME OF THAT HELPER IS NOT SPELLED HERE, and the omission is load
    bearing rather than coy. ``tests/test_restore.py`` refuses this module if its
    source contains that identifier anywhere, because entering the gates directly
    is exactly how the two acquisitions come back, and the guard reads text
    rather than intent. Prose explaining why a thing is forbidden is still the
    forbidden thing (P7).
    """
    return {} if value is None else {name: value}


def _performed(report: RestoreReport, offered: dict[str, Any]) -> dict[str, Any]:
    """The result as a ``plan/1`` payload, keeping the digest the gate answered.

    THE DIGEST DOES NOT MOVE BETWEEN THE OFFER AND THE REPORT. It identifies the
    decision this run was authorised under, so recomputing it over the performed
    steps would report a different value from the one recorded against the run,
    and a person comparing the two would be looking at evidence that the approval
    did not cover this work.

    BOTH HALVES ARE IN ``items``, in the order they happened, so a report cannot
    describe a mirror pull as nothing. ``converged`` is reported only when a
    capture was spent, because it is the capture restore's own question and
    answering it for a run that never asked would be the permissive reading of
    "nobody looked".
    """
    outcome = report.outcome
    items: list[dict[str, Any]] = [
        {"half": "off-machine", "transfer": label} for label in report.pulled
    ]
    items += [
        {
            "half": "capture",
            "act": str(step.act),
            "target": str(step.target) if step.target else None,
            "detail": step.detail,
        }
        for step in (outcome.performed if outcome is not None else ())
    ]
    totals: dict[str, Any] = {
        "transfers": len(report.pulled),
        "steps": len(outcome.performed) if outcome is not None else 0,
        "dry_run": report.dry_run,
    }
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
    return {"digest": offered["digest"], "items": items, "totals": totals, "chunk": None}


def perform_restore(ctx) -> Envelope:
    """Ask the confirmation gate, then restore under one session, or say there is nothing.

    NOTHING TO RESTORE IS AN OUTCOME, NOT A FAILURE. A library with no spendable
    capture and no off-machine pull asked for is the state of every install
    before its first write session, and refusing there would report a missing
    history as a broken machine. It returns the offer it made with no steps in
    it, so the report says what was considered rather than nothing at all.

    AND IT OPENS NO SESSION ON THAT PATH. The destructive gates refuse a library
    whose backup has never been acknowledged, so opening them to do zero work
    would make the verb unreachable on exactly the machine a person is trying to
    find out about. That is the same decision ``delete.review`` takes for the
    same reason: a baseline must not take a destructive session to move zero
    files.

    THE GATE STILL FIRES WHEN THERE IS NOTHING TO DO. Conformance 3 holds every
    declared gate to firing, and "nothing to restore" is an answer a person can
    still abort; skipping the question on an empty library would also make the
    one library that most needs asking the one that is never asked.
    """
    cfg = _load()
    requested = ctx.args.session_id
    chosen: restore.Restorable | None = None
    if requested is None:
        chosen = _newest_restorable(cfg)
    else:
        chosen = _named(cfg, requested)

    offered = _offer(
        chosen,
        discarding=tuple(ctx.args.discard),
        from_backup=ctx.args.from_backup,
        snapshot=ctx.args.snapshot,
        include_mirror=ctx.args.include_mirror,
    )
    spec = _confirm_gate(ctx.entry)
    option = ctx.gate.require(spec, digest=offered["digest"])
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)

    report = restore_under_one_session(
        cfg,
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
        dry_run=ctx.args.dry_run,
        from_backup=ctx.args.from_backup,
        snapshot=ctx.args.snapshot,
        include_mirror=ctx.args.include_mirror,
    )
    return ctx.envelope(data=_performed(report, offered))


__all__ = [
    "LISTING",
    "RestoreReport",
    "build_list",
    "build_run",
    "list_restorable",
    "perform_restore",
    "restore_under_one_session",
]
