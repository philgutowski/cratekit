"""``crate restore list``, ``run`` and ``bare-metal``: the history, and its undo.

:mod:`cratekit.core.restore` decides and performs; this decides what the person
asked for, asks the one explicit question (R34), and holds ONE destructive
session around everything that follows. Both halves of ``restore run``, the
off-machine pull and the capture rollback, run inside one
:func:`cratekit.core.restore.recovery_session`, the pull taking the open
``held.guard`` as its ``gates`` so the lock is never given back and retaken.

The gate is asked before the session opens, since a session refuses an
unacknowledged library first and the question would never be asked. Its digest
is over the restore's identity (the session, its change summary, the discard
set, the pull, its resolved snapshot, the target and the rehearsal flag), not
the step list, which only exists under the lock.

``restore bare-metal``, for a library whose volume is gone, lives in
:mod:`cratekit.session.bare_metal_cli` and is re-exported here, the module the
registry names.

Layer: modules. It names :mod:`cratekit.cli.output` and :mod:`cratekit.cli.exit_codes`
and nothing else from the command-line layer, both foundation-ranked under
KTD25. The backup module is imported where it is used, so the verbs build with
it toggled off.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

# Aliased: ``cratekit.cli.exit_codes`` is the reserved-cause table a refusal's
# remediation is looked up in, not ``cratekit.core.exit_codes``.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import analysis_store, config, restore
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:
    from cratekit.modules.tools import backup

#: What ``review_set`` calls this listing. Deliberately not a
#: :class:`cratekit.core.review.Queue` member: nothing here is adjudicated.
LISTING = "restore"


def _refused(exc: backup.BackupRefused) -> CratekitError:
    """One off-machine refusal as a cause, with its reserved remediation.

    The slug is carried unchanged and its remediation read from the reservation
    table, never replaced by a class default.
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


def _verb_refusal(reason: str, message: str, step: str, **detail: Any) -> CratekitError:
    """A refusal this verb owns, with its one step written beside the condition.

    The verb's own slugs are registered in ``cratekit.core.cause``, not in the
    reservation table, which holds only what a module's refusal enum raises.
    """
    return CratekitError(
        Cause(
            reason=reason,
            message=message,
            remediation=Remediation(steps=(step,)),
            origin=("session.restore_cli",),
            detail=detail,
        )
    )


# ---------------------------------------------------------------------------
# restore list
# ---------------------------------------------------------------------------


def build_list(parser, entry) -> None:
    """Declare the listing's arguments, which are none. ``entry`` is unannotated (KTD23)."""
    del entry
    parser.set_defaults(_handler=list_restorable)


#: The guarded writer's ``RECORDED_REMOVALS_KEY``, spelled here so this package
#: reaches no more of the core; a test holds them equal.
RECORDED_REMOVALS_KEY = "collection_removed"


def _listed(entry: restore.Restorable) -> dict[str, Any]:
    """One session as a listing row; an unusable one is reported, never filtered."""
    listed: dict[str, Any] = {
        "session_id": entry.session_id, "started": entry.started, "workflow": entry.workflow,
        "restorable": entry.restorable,
        "unusable": entry.unusable,
        "change": [tree.to_json() for tree in entry.change.trees],
    }
    # A session that took rows out of the collection names each one (U288).
    recorded = entry.record.detail.get(RECORDED_REMOVALS_KEY)
    if isinstance(recorded, dict):
        listed["removed"] = [
            {key: str(row.get(key, "")) for key in ("content_id", "artist", "title", "file")}
            for row in recorded.get("rows") or ()
            if isinstance(row, dict)
        ]
    return listed


def list_restorable(ctx) -> Envelope:
    """Every recorded session, newest first, with what it changed.

    Read only and outside the session gates, so it answers on a busy library or
    one never acknowledged. ``unresolved`` is zero: nothing here awaits a verdict.
    """
    cfg = load_config(("session.restore_cli",))
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

    No ``--yes`` or ``--confirm``: the confirmation is the recorded answer to
    the explicit gate (R34). ``--discard`` takes repeated identifiers, never a
    boolean.
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
    parser.add_argument("--dry-run", action="store_true", help=(
        "walk every step and perform none of them, under the same gates"
    ))
    parser.add_argument("--from-backup", action="store_true", dest="from_backup", help=(
        "pull the database back from the off-machine mirror first, for the "
        "case where the volume itself was replaced and no local capture "
        "survived"
    ))
    parser.add_argument("--snapshot", default=None, metavar="STAMP", help=(
        "which dated off-machine snapshot to pull; the newest by default"
    ))
    parser.add_argument(
        "--snapshot-volume", default=None, dest="snapshot_volume", metavar="IDENTITY",
        help=(
            "the volume identity the snapshot is expected to record, for a "
            "library whose drive was replaced since the snapshot was taken; "
            "checked against the snapshot, used once and never recorded"
        ),
    )
    parser.add_argument("--include-mirror", action="store_true", dest="include_mirror", help=(
        "pull the music and everything else the mirror carried, not only the "
        "database; hundreds of gigabytes, so it is off by default"
    ))
    parser.add_argument("--target", default=None, metavar="DIRECTORY", help=(
        "restore the database into this directory instead of the live "
        "library, which is how a restore is rehearsed; needs the off-machine "
        "pull, and rolls no session back"
    ))
    parser.set_defaults(_handler=perform_restore)


#: The invocation, not the directory, is what this refuses: a target without
#: the pull and a target beside a capture rollback both misread ``--target``.
_target_invalid = partial(_verb_refusal, "restore-target-invalid", step=(
    "a restore target takes the database from the off-machine "
    "snapshot and rolls no write session back; ask for the "
    "off-machine pull, and name either a session to roll back or "
    "a target, never both"
))

#: A destination that is the live library, by either check; ``detail`` says which.
_target_is_live = partial(_verb_refusal, "restore-target-is-live-root", step=(
    "name a directory the live library is not inside and does "
    "not contain, and check where the database itself would land "
    "when the database sits outside the library root; restoring "
    "onto the live library is this verb with no target named"
))


def _same_place(one: Path, other: Path) -> bool:
    """Whether two paths name ONE place on the disk, rather than one spelling.

    ``samefile`` compares device and inode, so a differently cased spelling on a
    case insensitive filesystem (APFS, exFAT) is the same place. A path that
    does not exist cannot be the live library, so it falls back to ``==``.
    """
    try:
        return one.samefile(other)
    except OSError:
        return one == other


def _holds_or_is(root: Path, place: Path) -> bool:
    """Whether ``place`` IS ``root`` or sits underneath it, ancestor by ancestor.

    The string test answers first and cheaply; each ancestor is then asked with
    :func:`_same_place`, so a differently cased root still contains it.
    """
    if place == root or place.is_relative_to(root):
        return True
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))


def _restore_target(cfg: config.Config, args) -> Path | None:
    """The directory ``--target`` names, resolved and refused, or ``None``.

    ``None`` is the live restore, unchanged. A target refuses before the gate
    and before any session. Both paths are resolved first, a relative path
    comparing equal to nothing. Two checks: containment of the library root
    either way, and where the database itself would land, asked through
    ``backup.database_target_for`` because a database outside the root is
    rebased as ``target / name``. Existence is ``backup.plan_restore``'s check.
    """
    raw = getattr(args, "target", None)
    if raw is None:
        return None
    if not args.from_backup:
        raise _target_invalid(
            "a restore target is a place to put a database pulled from the "
            "off-machine snapshot, so it needs the off-machine pull; ask for it, "
            "or drop the target and restore the live library",
            target=str(raw),
        )
    if args.session_id is not None or args.discard:
        raise _target_invalid(
            "a restore into a directory that is not the library restores the "
            "database and nothing else; rolling a write session back moves state "
            "coupled to the live library and cannot be pointed elsewhere, so name "
            "a session or a target and not both",
            target=str(raw), session_id=args.session_id, discard=list(args.discard),
        )
    resolved = Path(raw).expanduser().resolve()
    root = Path(cfg.library.root).resolve()
    if _holds_or_is(root, resolved) or _holds_or_is(resolved, root):
        raise _target_is_live(
            f"{resolved} is the live library at {root}, or holds it, or sits "
            f"inside it; a rehearsal restores somewhere the live library is not, "
            f"and restoring onto the live library is this verb without a target",
            target=str(resolved),
            library_root=str(root),
            check="containment",
        )
    from cratekit.modules.tools import backup

    landing = backup.database_target_for(cfg, resolved).resolve()
    live = config.state_path("rekordbox_db", cfg).resolve()
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):
        raise _target_is_live(
            f"the database would land on {landing}, which is this library's live "
            f"database; the target is outside the library root and the database "
            f"is too, so naming its directory restores over it in place",
            target=str(resolved), database_target=str(landing), live_database=str(live),
            check="destination",
        )
    return resolved


def _newest_restorable(cfg: config.Config) -> restore.Restorable | None:
    """The session a bare ``crate restore run`` means: the newest restorable one."""
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
    return None


def _named(cfg: config.Config, session_id: str) -> restore.Restorable:
    """The session a person named, or a refusal that says which of the two is wrong.

    No such session and an unusable capture get different messages, the second
    the listing's own sentence. Refused before any session opens, so a pull
    never runs ahead of a capture that cannot be spent.
    """
    for entry in restore.list_sessions(cfg):
        if entry.session_id != session_id:
            continue
        if entry.unusable:
            raise _verb_refusal(
                "restore-record-unusable",
                f"session {session_id} cannot be restored: {entry.unusable}",
                "run the restore listing and choose a session whose "
                "capture is still spendable",
                session_id=session_id, unusable=entry.unusable,
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
    chosen: restore.Restorable | None, *, discarding: Sequence[str], from_backup: bool,
    snapshot: backup.ResolvedSnapshot | None, include_mirror: bool,
    snapshot_volume: str | None = None, target: Path | None = None, dry_run: bool = False,
) -> dict[str, Any]:
    """What the person is being asked to approve, as a ``plan/1`` payload.

    The items are the restore's two halves, each separately refusable. Every
    field that changes what happens is digested so a stale or different answer
    is refused: the change summary, the discard set, the resolved snapshot stamp
    and whose it is, the target (``"library"`` when absent), and the rehearsal
    flag, which belongs to the whole run.
    """
    items: list[dict[str, Any]] = []
    if from_backup:
        items.append(
            {
                "half": "off-machine",
                # Read directly: this half is offered only over a resolved snapshot.
                "snapshot": snapshot.stamp,
                "snapshot_named": snapshot.named,
                "recorded_volume": snapshot.recorded_volume,
                "expected_volume": snapshot_volume,
                "include_mirror": include_mirror,
                "target": str(target) if target is not None else "library",
            }
        )
    if chosen is not None:
        items.append(
            {
                "half": "capture", "session_id": chosen.session_id, "started": chosen.started,
                "workflow": chosen.workflow,
                "change": [tree.to_json() for tree in chosen.change.trees],
                "discarding": list(discarding),
            }
        )
    return {
        "digest": digest_of(
            {"kind": "restore.run", "items": items, "dry_run": dry_run}
        ),
        "items": items, "totals": {"halves": len(items), "dry_run": dry_run}, "chunk": None,
    }


#: The flags that describe the off-machine pull and mean nothing without it,
#: as the attribute argparse stores and the spelling a person typed.
_PULL_FLAGS = (
    ("snapshot", "--snapshot"),
    ("snapshot_volume", "--snapshot-volume"),
    ("include_mirror", "--include-mirror"),
)


def _refuse_pull_flags_without_the_pull(args) -> None:
    """A flag about the off-machine pull, with no pull asked for, is refused.

    Silently dropping it would roll the live library back while a person
    believed they had authorised a pull. ``--target`` has its own refusal.
    """
    if args.from_backup:
        return
    typed = [
        spelling
        for attribute, spelling in _PULL_FLAGS
        if getattr(args, attribute, None) not in (None, False)
    ]
    if not typed:
        return
    raise _verb_refusal(
        "restore-flag-needs-pull",
        f"{' and '.join(typed)} describe the off-machine pull, and this "
        f"restore did not ask for one, so it would have rolled the live "
        f"library back to a recorded session and ignored "
        f"{'them' if len(typed) > 1 else 'it'}",
        "add --from-backup to pull the database from the off-machine "
        "snapshot, or drop the flag to roll back a recorded session",
        flags=typed,
    )


def _confirm_gate(entry):
    """The explicit confirmation gate off the entry, found by digest source, not index."""
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

    ``pulled`` is the off-machine transfers by label, empty when no pull was
    asked; ``outcome`` is the capture restore, ``None`` when no session was
    named. ``absent`` is the suffixes the snapshot did not hold.
    """

    pulled: tuple[str, ...]
    outcome: restore.RestoreOutcome | None
    dry_run: bool
    absent: tuple[str, ...] = ()
    #: The snapshot the pull took and the identity its marker recorded, read
    #: off the plan built under the gates, so the report names what arrived.
    snapshot: str | None = None
    recorded_volume: str | None = None
    #: What the pull did about the analysis share, in the engine's own word
    #: (``backup.ShareRestore``), or None when it did not run (R-338).
    share: str | None = None


def restore_under_one_session(
    cfg: config.Config, *, session_id: str | None, discarding: Sequence[str] = (),
    dry_run: bool = False, from_backup: bool = False, snapshot: str | None = None,
    snapshot_volume: str | None = None, accept_unrecorded: bool | None = None,
    include_mirror: bool = False, target: Path | str | None = None,
    identity_provider: object | None = None, mount_enumerator: object | None = None,
    runner: object | None = None, process_lister: object | None = None,
) -> RestoreReport:
    """Both halves of a restore, inside ONE acquisition of the destructive gates.

    :func:`cratekit.core.restore.recovery_session` is entered once and
    ``held.guard`` is handed to the off-machine half as its ``gates``, so the
    lock is never taken twice. The pull runs first, then the capture rolls back
    onto what it laid down. ``confirmed=True`` states the explicit decision
    already recorded (R33). The verb refuses a target beside a session; this
    seam still takes both so the composition test can drive them together.
    ``analysis_roots`` names what the analysis watch must cover (R-14). Both
    halves are reported separately, ``outcome`` staying ``None`` when no
    capture was spent.
    """
    from cratekit.modules.tools import backup

    watched: tuple[Path, ...] = analysis_store.watch_roots(cfg)
    with restore.recovery_session(
        cfg,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ) as held:
        transferred: tuple[str, ...] = ()
        missing: tuple[str, ...] = ()
        arrived: dict[str, Any] = {}
        if from_backup:
            where = Path(target) if target is not None else Path(cfg.library.root)
            try:
                pulled = backup.plan_restore(
                    cfg, target=where,
                    confirmed=True,
                    snapshot=snapshot, snapshot_volume=snapshot_volume,
                    accept_unrecorded=accept_unrecorded,
                    include_mirror=include_mirror,
                    gates=held.guard,
                    **_seam("runner", runner), **_seam("process_lister", process_lister),
                )
                ran = backup.run_restore(
                    pulled,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard, **_seam("runner", runner),
                )
            except backup.BackupRefused as exc:
                raise _refused(exc) from exc
            # The results, not the plan's commands, one label per result, zipped
            # strictly so a short result list fails rather than reports less.
            transferred = tuple(
                command.label
                for command, _result in zip(pulled.commands, ran, strict=True)
            )
            missing = pulled.absent_sidecars
            arrived = {
                "snapshot": pulled.snapshot,
                "recorded_volume": pulled.recorded_volume,
                "share": str(pulled.share),
            }
        if session_id is None:
            return RestoreReport(
                pulled=transferred, outcome=None, dry_run=dry_run, absent=missing, **arrived
            )
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
            dry_run=dry_run, absent=missing, **arrived,
        )


def _seam(name: str, value: object) -> dict[str, Any]:
    """One injectable seam as keyword arguments, omitted entirely when unsupplied.

    ``backup.plan_restore`` defaults its runner to a real subprocess and reads
    ``None`` as no runner at all, so an absent seam must be an absent argument.
    """
    return {} if value is None else {name: value}


def _performed(report: RestoreReport, offered: dict[str, Any]) -> dict[str, Any]:
    """The result as a ``plan/1`` payload, keeping the digest the gate answered.

    Both halves are in ``items`` in the order they happened; ``converged`` is
    reported only when a capture was spent.
    """
    outcome = report.outcome
    items: list[dict[str, Any]] = [
        {"half": "off-machine", "transfer": label} for label in report.pulled
    ]
    items += [
        {
            "half": "capture", "act": str(step.act),
            "target": str(step.target) if step.target else None, "detail": step.detail,
        }
        for step in (outcome.performed if outcome is not None else ())
    ]
    totals: dict[str, Any] = {
        "transfers": len(report.pulled),
        "steps": len(outcome.performed) if outcome is not None else 0,
        "dry_run": report.dry_run, "absent_sidecars": list(report.absent),
    }
    if report.pulled:
        totals["snapshot"] = report.snapshot
        totals["recorded_volume"] = report.recorded_volume
        # One word: mirrored, pulled, absent or withheld (a live restore).
        totals["analysis_share"] = report.share
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
    return {"digest": offered["digest"], "items": items, "totals": totals, "chunk": None}


def perform_restore(ctx) -> Envelope:
    """Ask the confirmation gate, then restore under one session, or say there is nothing.

    Nothing to restore is a no-op that opens no session, but the gate still
    fires (conformance 3). A target selects no capture at all, so the default
    newest session is never rolled back beside a rehearsal.
    """
    cfg = load_config(("session.restore_cli",))
    target = _restore_target(cfg, ctx.args)
    _refuse_pull_flags_without_the_pull(ctx.args)
    requested = ctx.args.session_id
    if target is not None:
        chosen = None
    elif requested is None:
        chosen = _newest_restorable(cfg)
    else:
        chosen = _named(cfg, requested)

    pulling = _snapshot_offered(cfg, ctx.args) if ctx.args.from_backup else None
    offered = _offer(
        chosen, discarding=tuple(ctx.args.discard), from_backup=ctx.args.from_backup,
        snapshot=pulling, include_mirror=ctx.args.include_mirror,
        snapshot_volume=ctx.args.snapshot_volume, target=target, dry_run=ctx.args.dry_run,
    )
    spec = _confirm_gate(ctx.entry)
    # Shown as well as digested: which snapshot, taken when, and whose.
    shown = (
        {"off_machine": next(i for i in offered["items"] if i["half"] == "off-machine")}
        if pulling is not None
        else None
    )
    option = ctx.gate.require(spec, digest=offered["digest"], context=shown)
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
        # The stamp that was offered, never the flag, so the engine cannot
        # resolve a newer snapshot after the approval; ``accept_unrecorded``
        # keeps a listed stamp from looking typed.
        snapshot=pulling.stamp if pulling is not None else None,
        snapshot_volume=ctx.args.snapshot_volume,
        accept_unrecorded=pulling.named if pulling is not None else None,
        include_mirror=ctx.args.include_mirror,
        target=target,
    )
    return ctx.envelope(data=_performed(report, offered))


def _snapshot_offered(cfg: config.Config, args) -> backup.ResolvedSnapshot:
    """Which snapshot this restore would pull, asked of the remote BEFORE the gate.

    The one network reach before the answer, made only for a pull, so the
    approval names the database it approves. The engine checks again under the
    gates.
    """
    from cratekit.modules.tools import backup

    try:
        return backup.resolve_snapshot(
            cfg, snapshot=args.snapshot, snapshot_volume=args.snapshot_volume
        )
    except backup.BackupRefused as exc:
        raise _refused(exc) from exc


# The bare-metal verb, re-exported so the registry's module path keeps it.
from cratekit.session.bare_metal_cli import (  # noqa: E402
    DATABASE_HALF,
    MIRROR_HALF,
    BareMetalReport,
    _recovered,  # noqa: F401
    build_bare_metal,
    perform_bare_metal,
    recover_under_bare_metal_session,
    rerun_step,
)

__all__ = [
    "DATABASE_HALF", "LISTING", "MIRROR_HALF", "BareMetalReport", "RestoreReport",
    "build_bare_metal", "build_list", "build_run", "list_restorable", "perform_bare_metal",
    "perform_restore", "recover_under_bare_metal_session", "rerun_step",
    "restore_under_one_session",
]
