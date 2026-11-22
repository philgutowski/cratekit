"""``crate restore bare-metal``: the off-machine mirror and database onto a new drive.

The case ``restore run`` cannot serve: the library volume is gone, and every
gate ``restore run`` passes was on it. This spends
:func:`cratekit.core.restore.bare_metal_session` instead, rolling no session
back. The registry names :mod:`cratekit.session.restore_cli`, which re-exports
everything here.

Layer: modules. The backup module is imported where it is used, so the verb
builds with it toggled off.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import config, processes, restore
from cratekit.core.cause import Cause, CratekitError, Remediation

if TYPE_CHECKING:
    from cratekit.modules.tools import backup

#: The two halves of a recovery, in the only order in which a failure of the
#: first leaves nothing of the second.
MIRROR_HALF = "mirror"
DATABASE_HALF = "database"


def build_bare_metal(parser, entry) -> None:
    """Declare the recovery's arguments. The parameters are unannotated on purpose.

    ``--target`` is required: the configured volume is the one place this verb
    can never point. ``--accept-replacement`` is the acknowledgment, since the
    recorded one died with the volume, and the engine refuses it without a
    terminal. No flag names an occupied target for replacement.
    """
    del entry
    parser.add_argument(
        "--target",
        required=True,
        metavar="DIRECTORY",
        help=(
            "the mounted replacement volume to recover onto; it must exist, hold "
            "no database, and not be the folder the lost volume left behind"
        ),
    )
    parser.add_argument(
        "--accept-replacement", action="store_true", dest="accept_replacement",
        help=(
            "accept that a whole library is written onto the target; refused "
            "without it, and refused with it when nobody is at a terminal"
        ),
    )
    parser.add_argument("--snapshot", default=None, metavar="STAMP", help=(
        "which dated off-machine snapshot to pull; the newest by default"
    ))
    parser.add_argument(
        "--snapshot-volume", default=None, dest="snapshot_volume", metavar="IDENTITY",
        help=(
            "the volume identity the snapshot is expected to record, when it is "
            "not the one this installation remembers; used once, never recorded"
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help=(
        "rehearse both halves and transfer nothing, under the same gates"
    ))
    parser.set_defaults(_handler=perform_bare_metal)


@dataclass(frozen=True, slots=True)
class BareMetalReport:
    """What one recovery did, a half at a time.

    ``mirror`` and ``database`` are the transfers of each half that completed.
    ``database_elsewhere`` is where the configured database lives when it was
    never on the lost volume, and ``None`` otherwise.
    """

    target: Path
    database_target: Path
    mirror: tuple[str, ...]
    database: tuple[str, ...]
    dry_run: bool
    absent: tuple[str, ...] = ()
    snapshot: str | None = None
    recorded_volume: str | None = None
    database_elsewhere: Path | None = None


def rerun_step(database_target: Path) -> str:
    """What a rerun needs after a failure that may have landed the database.

    The engine refuses only the fileset at ``database_target`` (R-592), and the
    session opened over a target holding none of it, so whatever is there
    arrived during this run and removing it loses nothing.
    """
    return (
        f"before running the recovery again, remove {database_target.name} and any "
        f"companion of it in {database_target.parent} if one is there, because a "
        f"target already holding this library's database is refused; whatever is "
        f"there arrived during this run, and the rerun transfers the database "
        f"again. Nothing else on the target needs removing"
    )


def _database_elsewhere(cfg: config.Config) -> Path | None:
    """The configured database's path when it is NOT under the library root.

    In that layout, rekordbox's default, the database was never on the volume
    that died, and rebasing it onto the target would recover a file nothing reads.
    """
    database = config.state_path("rekordbox_db", cfg)
    try:
        database.relative_to(cfg.library.root)
    except ValueError:
        return database
    return None


def _halves(decided: backup.RestorePlan) -> tuple[tuple[str, backup.RestorePlan], ...]:
    """One plan, read as the two halves it already holds. Nothing is re-planned.

    ``backup.run_restore`` runs every command before reading a return code, so
    spending the halves separately keeps a failed mirror from landing a database
    the rerun would then be refused over. Split by label, in the plan's order.
    """
    from cratekit.modules.tools import backup

    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
    database = tuple(c for c in decided.commands if c.label != backup.RESTORE_MIRROR)
    return (
        (MIRROR_HALF, replace(decided, commands=mirror)),
        (DATABASE_HALF, replace(decided, commands=database)),
    )


def _absence_unconfirmed(
    exc: processes.AbsenceUnconfirmed, completed: Sequence[str], decided: backup.RestorePlan,
    *, dry_run: bool,
) -> processes.AbsenceUnconfirmed:
    """The scan's refusal at the database half, saying what the mirror half left (U211)."""
    declared = exc.declared_cause
    steps = tuple(declared.remediation.steps)
    if not dry_run:
        steps = (*steps, rerun_step(decided.database_target))
    cause = replace(
        declared,
        remediation=replace(declared.remediation, steps=steps),
        message=(
            f"{declared.message}. The mirror half completed onto {decided.target} "
            f"and the database half was not attempted"
        ),
        detail={
            **dict(declared.detail or {}), "half": DATABASE_HALF,
            "completed_halves": list(completed), "target": str(decided.target),
        },
    )
    return processes.AbsenceUnconfirmed(cause, exc.read)


def _half_failed(
    exc: backup.BackupRefused, half: str, *, completed: Sequence[str],
    decided: backup.RestorePlan, dry_run: bool,
) -> CratekitError:
    """A refusal from inside one half, saying which half and what is on the target.

    The reserved sentence for a failed transfer says companions were cleared and
    to rerun, which is false here, so the slug is kept and the sentence
    replaced; the engine's own rides in the detail. Only a real failure at the
    database half carries :func:`rerun_step`.
    """
    from cratekit.modules.tools import backup

    slug = str(exc.refusal)
    detail: dict[str, Any] = {
        "refusal": slug, "half": half, "completed_halves": list(completed),
        "target": str(decided.target), "dry_run": dry_run, "engine": exc.detail,
    }
    if exc.refusal is backup.Refusal.REKORDBOX_RUNNING:
        message = (
            f"{exc.detail} The mirror half completed onto {decided.target} and "
            f"the database half was not attempted."
        )
        steps: tuple[str, ...] = ("quit rekordbox and its background agent",)
    elif exc.refusal is not backup.Refusal.RESTORE_TRANSFER_FAILED:
        message = exc.detail
        steps = reservations.remediation_for(slug).steps
    elif dry_run:
        message = (
            f"the rehearsal's {half} half failed against the remote and nothing "
            f"was written to {decided.target}"
        )
        steps = ("check the remote is reachable, then rehearse again",)
    elif half == MIRROR_HALF:
        message = (
            f"the mirror half of the recovery onto {decided.target} failed part "
            f"way, and the database half was not attempted, so the target holds "
            f"no database from the snapshot"
        )
        steps = (
            "check the remote is reachable, then run the recovery again; what "
            "arrived stays and nothing needs removing first",
        )
    else:
        message = (
            f"the mirror half completed and the database half of the recovery "
            f"onto {decided.target} failed, so {decided.database_target.name} or "
            f"one of its companions may have arrived without the rest"
        )
        steps = ("do not open the library", "check the remote is reachable")
    if not dry_run and half == DATABASE_HALF:
        steps = (*steps, rerun_step(decided.database_target))
    return CratekitError(
        Cause(
            reason=slug,
            message=message,
            remediation=Remediation(
                remedy=None if steps else reservations.remediation_for(slug).remedy,
                steps=steps,
            ),
            origin=("modules.tools.backup", "session.restore_cli"),
            detail=detail,
        )
    )


def recover_under_bare_metal_session(
    cfg: config.Config, *, target: Path | str, accepted: bool, dry_run: bool = False,
    snapshot: str | None = None, snapshot_volume: str | None = None,
    terminal: object | None = None, identity_provider: object | None = None,
    mount_enumerator: object | None = None, mount_probe: object | None = None,
    runner: object | None = None, process_lister: object | None = None,
) -> BareMetalReport:
    """The mirror and the database, onto a replacement drive, inside ONE session.

    :func:`cratekit.core.restore.bare_metal_session` refuses, before its lock,
    unless the library is gone, the target is a real filesystem holding no
    database where this one lands, a person is at a terminal and ``accepted``
    is true. ``held.guard`` is the ``gates`` seam for both engine calls and
    ``held.authorises`` the only target path. rekordbox is asked about again
    before the database half, hours after the plan asked. A database that was
    never on the lost volume is not recovered; the mirror half runs alone. A
    rehearsal passes the same gates.
    """
    from cratekit.modules.tools import backup
    from cratekit.session.restore_cli import _refused, _seam

    with restore.bare_metal_session(
        cfg, target=target,
        acknowledged=accepted,
        terminal=terminal, identity_provider=identity_provider,
        mount_enumerator=mount_enumerator, mount_probe=mount_probe,
    ) as held:
        try:
            decided = backup.plan_restore(
                cfg, target=held.authorises, confirmed=True,
                snapshot=snapshot, snapshot_volume=snapshot_volume,
                include_mirror=True,
                # An outside share rides the database half, which is skipped
                # exactly when the share is outside (R-338).
                pull_share=False,
                gates=held.guard,
                **_seam("runner", runner), **_seam("process_lister", process_lister),
            )
        except backup.BackupRefused as exc:
            raise _refused(exc) from exc
        elsewhere = _database_elsewhere(cfg)
        ran_labels: dict[str, tuple[str, ...]] = {MIRROR_HALF: (), DATABASE_HALF: ()}
        completed: list[str] = []
        for half, portion in _halves(decided):
            if half == DATABASE_HALF and elsewhere is not None:
                continue
            try:
                if half == DATABASE_HALF:
                    try:
                        running = backup.rekordbox_processes_running(lister=process_lister)
                    except processes.AbsenceUnconfirmed as exc:
                        raise _absence_unconfirmed(
                            exc, completed, decided, dry_run=dry_run
                        ) from exc
                    if running:
                        raise backup.BackupRefused(
                            backup.Refusal.REKORDBOX_RUNNING,
                            f"{', '.join(running)} started while the mirror was "
                            f"arriving, and restoring a database underneath a "
                            f"live rekordbox replaces the file it holds open.",
                        )
                ran = backup.run_restore(
                    portion,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
                    **_seam("runner", runner),
                )
            except backup.BackupRefused as exc:
                raise _half_failed(
                    exc, half, completed=tuple(completed), decided=decided, dry_run=dry_run
                ) from exc
            # One result per command or a hard failure.
            ran_labels[half] = tuple(
                command.label for command, _result in zip(portion.commands, ran, strict=True)
            )
            completed.append(half)
        return BareMetalReport(
            target=decided.target, database_target=decided.database_target,
            mirror=ran_labels[MIRROR_HALF], database=ran_labels[DATABASE_HALF], dry_run=dry_run,
            absent=decided.absent_sidecars if elsewhere is None else (),
            snapshot=decided.snapshot, recorded_volume=decided.recorded_volume,
            database_elsewhere=elsewhere,
        )


def _recovered(report: BareMetalReport) -> dict[str, Any]:
    """The recovery as a ``plan/1`` payload, one item per transfer, named by half.

    The digest is an identity only: this verb declares no gate.
    """
    items: list[dict[str, Any]] = [
        {"half": MIRROR_HALF, "transfer": label} for label in report.mirror
    ]
    items += [{"half": DATABASE_HALF, "transfer": label} for label in report.database]
    return {
        "digest": digest_of({
            "kind": "restore.bare-metal", "target": str(report.target),
            "snapshot": report.snapshot, "recorded_volume": report.recorded_volume,
            "dry_run": report.dry_run,
        }),
        "items": items,
        "totals": {
            "mirror_transfers": len(report.mirror), "database_transfers": len(report.database),
            "dry_run": report.dry_run, "absent_sidecars": list(report.absent),
            "snapshot": report.snapshot, "recorded_volume": report.recorded_volume,
            "target": str(report.target),
            # Where the database is, whichever half put it there.
            "database_target": str(report.database_elsewhere or report.database_target),
            # A boolean, not a slug shaped word, which would join the pinned census.
            "database_was_on_the_lost_volume": report.database_elsewhere is None,
        },
        "chunk": None,
    }


def perform_bare_metal(ctx) -> Envelope:
    """Recover the mirror and the database onto the named replacement drive.

    No gate is asked: the flag is the explicit act. The path is made absolute
    and every judgement about it is the engine's.
    """
    cfg = load_config(("session.restore_cli",))
    report = recover_under_bare_metal_session(
        cfg, target=Path(ctx.args.target).expanduser().absolute(),
        accepted=ctx.args.accept_replacement,
        dry_run=ctx.args.dry_run, snapshot=ctx.args.snapshot,
        snapshot_volume=ctx.args.snapshot_volume,
    )
    return ctx.envelope(data=_recovered(report))


__all__ = [
    "DATABASE_HALF", "MIRROR_HALF", "BareMetalReport", "build_bare_metal", "perform_bare_metal",
    "recover_under_bare_metal_session", "rerun_step",
]
