"""``crate session ack`` and ``crate session release``: minting and unsticking.

``session ack`` is the only caller of :func:`cratekit.core.session.record_acknowledgment`,
which every destructive verb's gate consults. ``session release`` releases the
LIBRARY LOCK, not the acknowledgment, when its holder is gone, and since R-598
also ends the open session records such a dead holder left. The verbs, gates and
prompts are the registry's declaration, implemented here unchanged.

The facts are read before the gate is asked, because a gate's prompt is fixed
and what a person decides over rides on the refusal. An absent fact file must
not refuse, or the verb would be unreachable before the first backup; an
unreadable one refuses with the remedy its exception carries. Neither verb opens
a session or declares a write.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, which is foundation-ranked under KTD25.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import backup_facts, config, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy


def _gate(entry, name: str):
    """The gate this verb asks, looked up by name off the entry, never by index."""
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate called {name!r}, so there is no "
                f"question to ask before it acts"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("session", "cli"),
            detail={"verb": entry.name, "gate": name},
        )
    )


# ---------------------------------------------------------------------------
# session ack
# ---------------------------------------------------------------------------


def build_ack(parser, entry) -> None:
    """Declare the verb's one flag. Parameters unannotated.

    No ``--yes``, ``--actor`` or ``--hours``: a caller must never name who
    acknowledged (R34). ``--as session`` (U184) takes one value only and selects
    the session's rule, which is narrower than a person's: the engine mints only
    over young backup ages. The recorded actor is still derived.
    """
    del entry
    parser.add_argument(
        "--as", dest="as_actor",
        choices=(session.SESSION_ACTOR,),
        default=None, help=(
            "mint as the session in one command, with no gate: the backup ages "
            "are read and the acknowledgment is recorded only while both are "
            "under five days old"
        ),
    )
    parser.set_defaults(_handler=record_ack)


def _rendered_ages(cfg: config.Config, now: datetime) -> list[dict[str, Any]]:
    """The published backup ages, read from the fact file and rendered for here.

    The remedy travels from the exception, since ``read_facts`` tells a
    permission from a damaged file from a newer schema (R-201).
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
            f"the backup ages this acknowledgment has to show cannot be read: "
            f"{exc}. Asking a person to acknowledge now would ask them over a "
            f"clean sheet nobody has seen",
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    return [
        {
            "portion": str(entry.portion), "state": str(entry.state),
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
            "completed_at": (
                entry.completed_at.isoformat() if entry.completed_at is not None else None
            ),
        }
        for entry in reported
    ]


def _on_record(cfg: config.Config, now: datetime) -> dict[str, Any] | None:
    """The acknowledgment on record, None when absent, or what made it unreadable.

    An unreadable record is described and not raised: this verb overwrites it,
    so refusing would leave a damaged record that can never be replaced.
    """
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
    if recorded is None:
        return None
    return {
        "actor": recorded.actor, "recorded_at": recorded.recorded_at.isoformat(),
        "expires_at": recorded.expires_at.isoformat(), "valid": recorded.valid_at(now),
    }


def record_ack(ctx) -> Envelope:
    """Show the ages, ask the question, and record the answer as a separate act.

    The gate is explicit, so the invocation that raises it cannot answer it
    (R34). Every answered drive re-mints. The engine refuses without a terminal
    unless the recorded answer is the session's (U138), in which case it mints
    only over young ages. ``--as session`` takes :func:`_mint_as_session`.
    """
    if getattr(ctx.args, "as_actor", None) == session.SESSION_ACTOR:
        return _mint_as_session(ctx)
    cfg = load_config(("session", "cli"))
    now = datetime.now(timezone.utc)
    shown = _rendered_ages(cfg, now)
    spec = _gate(ctx.entry, "session.ack.backup")
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )

    # The same moment is handed down, and nothing else about what was shown.
    # Who answered comes from the run record (U138), read before it is spent.
    answered = ctx.run.decisions.get(spec.name)
    acknowledgment = session.record_acknowledgment(
        cfg, now=now, decided_by=answered.actor if answered is not None else None
    )
    # The report comes from the record written, not the read above it.
    recorded_ages = [entry.to_json() for entry in acknowledgment.shown]
    # The decision is spent: a kept run identifier must not re-mint later.
    ctx.run.decisions.pop(spec.name, None)
    return ctx.envelope(
        data={
            "checks": [
                {
                    # ``key`` is the field ``cli.render``'s check table reads.
                    "key": f"backup.age.{entry['portion']}",
                    "status": "ok",
                    "detail": entry["state"],
                }
                for entry in recorded_ages
            ],
            "summary": {"recorded": True, **_described(acknowledgment)},
        }
    )


def _expiry_row(acknowledgment: session.Acknowledgment, *, minted: bool) -> dict[str, Any]:
    """The check row carrying the window, since the renderer never prints ``summary``."""
    said = "recorded now" if minted else "already on record, not minted again"
    return {
        "key": "backup.acknowledgment",
        "status": "ok",
        "detail": (
            f"{said}, by the {acknowledgment.rule} rule, valid until "
            f"{acknowledgment.expires_at.isoformat()}"
        ),
    }


def _described(acknowledgment: session.Acknowledgment) -> dict[str, Any]:
    """An acknowledgment as both mints report it, read off the record written."""
    return {
        "actor": acknowledgment.actor,
        "rule": acknowledgment.rule,
        "decided_by": acknowledgment.decided_by,
        "recorded_at": acknowledgment.recorded_at.isoformat(),
        "expires_at": acknowledgment.expires_at.isoformat(),
        "shown": [entry.to_json() for entry in acknowledgment.shown],
    }


def _summary(acknowledgment: session.Acknowledgment, *, minted: bool) -> dict[str, Any]:
    """What ``--as session`` reports, minted now or found on record."""
    return {
        "recorded": minted,
        "already_valid": not minted,
        **_described(acknowledgment),
    }


def _mint_as_session(ctx) -> Envelope:
    """``crate session ack --as session`` (U184): the session's mint, in one command.

    No gate is asked. The engine's session rule is the only age check. A valid
    acknowledgment on record is reported and not minted again; an unreadable one
    is not valid and is replaced.
    """
    cfg = load_config(("session", "cli"))
    now = datetime.now(timezone.utc)
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError:
        recorded = None
    if recorded is not None and recorded.valid_at(now):
        return ctx.envelope(
            data={
                "checks": [_expiry_row(recorded, minted=False)],
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.NO_OP,
        )
    acknowledgment = session.record_acknowledgment(
        cfg, now=now, decided_by=session.SESSION_ACTOR
    )
    return ctx.envelope(
        data={
            "checks": [
                *(
                    {"key": f"backup.age.{entry.portion}", "status": "ok", "detail": entry.state}
                    for entry in acknowledgment.shown
                ),
                _expiry_row(acknowledgment, minted=True),
            ],
            "summary": _summary(acknowledgment, minted=True),
        }
    )


# ---------------------------------------------------------------------------
# session release
# ---------------------------------------------------------------------------


def build_release(parser, entry) -> None:
    """Declare the verb's arguments, which are none, and no ``--force``."""
    del entry
    parser.set_defaults(_handler=release_lock)


def release_lock(ctx) -> Envelope:
    """Show the holder, ask the question, and clear a claim whose owner is gone.

    Nothing recorded is a no-op, not a failure. A running holder, or a gone one
    whose lock file still cannot be taken, refuses ``session-lock-held``. The
    gate fires even when there is nothing to release (conformance 3).
    """
    cfg = load_config(("session", "cli"))
    path = session.lock_path(cfg)
    holder = session.read_lock_holder(path)
    # ``read_lock_holder`` answers None for no holder and for a file it could
    # not understand; the second is told apart here.
    unreadable = holder is None and path.exists() and bool(path.read_bytes().strip())
    # The open records a dead holder left are shown before the question (R-598).
    orphans = [record for record in session.records(cfg) if session.orphaned(record)]
    spec = _gate(ctx.entry, "session.release.confirm")
    option = ctx.gate.require(
        spec,
        context={
            "holder": holder.to_json() if holder is not None else None,
            "record": "unreadable" if unreadable else ("present" if holder else "absent"),
            "orphans": [
                {"session_id": record.session_id, "workflow": record.workflow}
                for record in orphans
            ],
        },
    )
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"released": False, "aborted": True}},
            outcome=Outcome.NO_OP,
        )
    # The lock first, so a running holder refuses before any record is ended.
    # Records are judged again, only among those this invocation listed (R-648).
    cleared = session.release_stale_lock(cfg)
    abandoned = [
        record.session_id
        for record in session.abandon_orphaned_sessions(
            cfg, only=[record.session_id for record in orphans]
        )
    ]
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
    checks = [
        {"key": "session.record", "status": "ok", "detail": f"abandoned {sid}, its holder is gone"}
        for sid in abandoned
    ]
    records = {"abandoned": abandoned, "kept": kept}
    if cleared is None:
        return ctx.envelope(
            data={
                "checks": checks,
                "summary": {
                    "released": False, "recorded": False, "unreadable": unreadable, **records
                },
            },
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
        )
    lock = {"key": "session.lock", "status": "ok", "detail": cleared.describe()}
    return ctx.envelope(
        data={
            "checks": [lock, *checks],
            "summary": {"released": True, "holder": cleared.to_json(), **records},
        }
    )


__all__ = ["build_ack", "build_release", "record_ack", "release_lock"]
