"""The backup acknowledgment a destructive session requires, recorded and consulted (R34).

Part of :mod:`cratekit.core.session`, which re-exports every name its callers read; read them there. A
name of the session outside this file, and every seam a test patches, is read through
``session`` at call time so a patch on the session bites here too (U300).
"""

from __future__ import annotations

import json
import logging
import os
import socket
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from cratekit.core import backup_facts, config
from cratekit.core.call_time import session as _session
from cratekit.core.cause import (
    CratekitError,
    Scope,
    refuse,
)
from cratekit.core.exit_codes import Remedy

#: The session logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.session")


def _defect(message: str, **refusal: Any) -> CratekitError:
    """An ``internal-error`` refusal, whose remedy is to report the defect."""
    return refuse("internal-error", message, remedy=Remedy.REPORT_DEFECT, **refusal)


#: The library-scoped state entry this acknowledgment is written to.
ACK_KEY = "backup_ack"

#: Bumped only when the record's shape changes incompatibly.
ACK_SCHEMA_VERSION = 1

#: How long one acknowledgment answers for, bounded since an unbounded one is a
#: permanent affirmative (R34).
DEFAULT_ACK_VALIDITY = timedelta(hours=12)

#: The actor a session records its answer to the acknowledgment's gate under (U138).
SESSION_ACTOR = "session"

#: The oldest any backup portion may be for a session to mint (U138).
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

#: Which rule minted an acknowledgment; an older record reads as the terminal rule.
RULE_TERMINAL = "terminal"
RULE_SESSION_AGES = "session-ages"


@dataclass(frozen=True, slots=True)
class ShownAge:
    """One backup portion's age AS IT WAS SHOWN when the person answered,
    recorded rather than recomputed (KTD18)."""

    portion: str
    state: str
    age_seconds: float | None = None
    completed_at: str | None = None

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> ShownAge:
        return cls(
            portion=str(data["portion"]),
            state=str(data["state"]),
            age_seconds=data.get("age_seconds"),
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True, slots=True)
class Acknowledgment:
    """One recorded acknowledgment, with the actor and the window it answers for."""

    actor: str
    recorded_at: datetime
    expires_at: datetime
    shown: tuple[ShownAge, ...] = ()
    #: The rule that minted it, :data:`RULE_TERMINAL` or :data:`RULE_SESSION_AGES`.
    rule: str = RULE_TERMINAL
    #: The actor the run record holds for the gate's answer, or None. Never
    #: :attr:`actor`, which is derived.
    decided_by: str | None = None

    def valid_at(self, moment: datetime) -> bool:
        return moment < self.expires_at

    def to_json(self) -> dict[str, Any]:
        # No version bump for the two U138 keys, so older builds still read it.
        return {
            "schema_version": ACK_SCHEMA_VERSION,
            "actor": self.actor,
            "recorded_at": self.recorded_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "shown": [entry.to_json() for entry in self.shown],
            "rule": self.rule,
            "decided_by": self.decided_by,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Acknowledgment:
        version = data.get("schema_version")
        if version != ACK_SCHEMA_VERSION:
            raise _defect(
                f"the backup acknowledgment declares schema {version!r} and this "
                f"build understands {ACK_SCHEMA_VERSION}",
                detail={"schema_version": version},
            )
        return cls(
            actor=str(data["actor"]),
            recorded_at=datetime.fromisoformat(str(data["recorded_at"])),
            expires_at=datetime.fromisoformat(str(data["expires_at"])),
            shown=tuple(ShownAge.from_json(entry) for entry in (data.get("shown") or ())),
            rule=str(data.get("rule") or RULE_TERMINAL),
            decided_by=(
                str(data["decided_by"]) if data.get("decided_by") is not None else None
            ),
        )


def has_controlling_terminal() -> bool:
    """Whether this invocation has a terminal a person could be sitting at.

    A terminal check, not a read, since no verb reads standard input (R33).
    Falls back to the output stream where there is no terminal device.
    """
    ctermid = getattr(os, "ctermid", None)
    if ctermid is not None:
        try:
            descriptor = os.open(ctermid(), os.O_RDONLY)
        except OSError:
            return False
        os.close(descriptor)
        return True
    stream = sys.__stdout__
    try:
        return bool(stream is not None and stream.isatty())
    except (OSError, ValueError):  # pragma: no cover - a closed stream
        return False


def derive_actor() -> str:
    """Who this invocation is, derived from the invocation and never supplied (R34),
    or an agent could name itself into the audit trail.

    Reads ``pwd`` directly, since the convenience wrapper's module offers a
    password prompt the static guard forbids.
    """
    account = os.environ.get("USER") or os.environ.get("USERNAME") or _session().UNKNOWN_IDENTITY
    try:
        import pwd

        account = pwd.getpwuid(os.getuid()).pw_name
    except Exception as exc:  # noqa: BLE001 - no account database on this platform
        logger.debug("falling back to the environment for the account name: %s", exc)
    return f"{account}@{socket.gethostname()}"


def ack_path(cfg: config.Config) -> Path:
    """Where the acknowledgment lives, resolved through the state inventory."""
    return config.state_path(ACK_KEY, cfg)


def _shown_ages(cfg: config.Config, now: datetime) -> tuple[ShownAge, ...]:
    """The backup ages, read from the FACT file, since the backup module is opt-in.

    An unreadable fact file refuses rather than showing nothing, which would read
    as a library with no portions; an absent one mints normally. The remedy
    travels from ``read_facts``, so a permission is not reported as corruption.
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
            f"the backup ages this acknowledgment has to show cannot be read: "
            f"{exc}. Recording an acknowledgment now would say a person was shown "
            f"a clean sheet they were never shown",
            remedy=Remedy(str(exc.remedy)),
            scope=Scope.RUN,
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    return tuple(
        ShownAge(
            portion=str(entry.portion),
            state=str(entry.state),
            age_seconds=entry.age.total_seconds() if entry.age is not None else None,
            completed_at=(
                entry.completed_at.isoformat() if entry.completed_at is not None else None
            ),
        )
        for entry in reported
    )


def _too_old_for_a_session(shown: Sequence[ShownAge]) -> list[str]:
    """Each portion a session may not mint over, with why, in the order shown.

    An unknown age counts against the session, since could not tell is never
    fresh enough.
    """
    limit = SESSION_MAX_BACKUP_AGE.total_seconds()
    named = []
    for entry in shown:
        if entry.state != backup_facts.AgeState.KNOWN or entry.age_seconds is None:
            named.append(f"the {entry.portion} portion's age is not known ({entry.state})")
        elif entry.age_seconds >= limit:
            named.append(
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"
            )
    return named


def record_acknowledgment(
    cfg: config.Config,
    *,
    now: datetime | None = None,
    validity: timedelta = DEFAULT_ACK_VALIDITY,
    terminal: Callable[[], bool] | None = None,
    decided_by: str | None = None,
) -> Acknowledgment:
    """Mint the acknowledgment. A separate act from answering it, by a person.

    ``terminal`` is a test seam, not an override. THERE IS NO ACTOR PARAMETER
    and no affirmative one, or the gate would be under the control of what it
    gates. ``decided_by`` is a rule selector (U138): :data:`SESSION_ACTOR`
    swaps the terminal check for the rule that every portion reads under
    :data:`SESSION_MAX_BACKUP_AGE`.
    """

    moment = now or datetime.now(timezone.utc)
    if decided_by == SESSION_ACTOR:
        shown = _shown_ages(cfg, moment)
        stale = _too_old_for_a_session(shown)
        if stale:
            raise refuse(
                "backup-acknowledgment-backup-too-old",
                f"a session mints the backup acknowledgment only while every backup "
                f"portion is under {SESSION_MAX_BACKUP_AGE.days} days old, and "
                f"{'; '.join(stale)}; run a backup first, or a person acknowledges "
                f"from a terminal",
                remedy=Remedy.RUN_BACKUP,
                scope=Scope.RUN,
                detail={
                    "library": str(cfg.library.root),
                    "portions": [entry.to_json() for entry in shown],
                    "max_age_days": SESSION_MAX_BACKUP_AGE.days,
                },
            )
        rule = RULE_SESSION_AGES
    else:
        probe = terminal or _session().has_controlling_terminal
        if not probe():
            raise refuse(
                "backup-acknowledgment-no-terminal",
                "this invocation has no controlling terminal, so there is nobody here "
                "to acknowledge that the database and the music files are backed up; "
                "the acknowledgment is recorded by a person and consulted by the run",
                remedy=Remedy.ACKNOWLEDGE_BACKUP,
                scope=Scope.RUN,
                detail={"library": str(cfg.library.root)},
            )
        shown = _shown_ages(cfg, moment)
        rule = RULE_TERMINAL
    acknowledgment = Acknowledgment(
        actor=_session().derive_actor(),
        recorded_at=moment,
        expires_at=moment + validity,
        shown=shown,
        rule=rule,
        decided_by=decided_by,
    )
    config.atomic_write_bytes(
        json.dumps(acknowledgment.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n",
        ack_path(cfg),
    )
    return acknowledgment


def read_acknowledgment(cfg: config.Config) -> Acknowledgment | None:
    """The recorded acknowledgment, or None when this library has none.

    A file that exists and cannot be understood refuses, since reporting it as
    absent hides what is broken.
    """
    try:
        raw = ack_path(cfg).read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        # A read that did not happen, which establishes nothing about presence.
        raise _defect(
            f"the backup acknowledgment could not be read, and whether it is "
            f"even there was not established: {exc}",
            detail={"path": str(ack_path(cfg))},
        ) from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _defect(
            f"the backup acknowledgment is not readable as JSON: {exc}",
            detail={"path": str(ack_path(cfg))},
        ) from exc
    return Acknowledgment.from_json(data)


def assert_backup_acknowledged(
    cfg: config.Config, *, now: datetime | None = None
) -> Acknowledgment:
    """Consult the RECORD. Never an assertion made on this command line (R34).

    Absent and expired are one refusal, since the remedy is one act.
    """
    moment = now or datetime.now(timezone.utc)
    acknowledgment = read_acknowledgment(cfg)
    if acknowledgment is not None and acknowledgment.valid_at(moment):
        return acknowledgment
    recorded = acknowledgment.recorded_at.isoformat() if acknowledgment else None
    raise refuse(
        "backup-acknowledgment-missing",
        (
            "this destructive session has no backup acknowledgment within its "
            "validity window"
            + (f"; the last one was recorded at {recorded}" if recorded else "")
        ),
        remedy=Remedy.ACKNOWLEDGE_BACKUP,
        scope=Scope.SESSION,
        detail={
            "library": str(cfg.library.root),
            "recorded_at": recorded,
            "expired": acknowledgment is not None,
        },
    )
