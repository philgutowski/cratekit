"""The night pass's budget across a night's firings (U293).

The night pass, ``sync.night``, runs unattended, and the account is not to be
pushed toward the lock it met at sitting 94, so a night has a budget of its own,
``[provider] night_calls``, that holds however many times the schedule fires
that night. This module keeps what the night has spent; the gate holds the
line call by call (:func:`cratekit.core.provider_gate.night`).

A NIGHT RUNS FROM NOON TO NOON, local time, so a firing at three in the
morning spends from the night that began the evening before, and the budget
frees at the next noon.

SPENT IS READ OFF THE GATE'S RUNNING TOTAL, never off this process's count.
The total counts every process that reads the gate, the night's detached
children and anything else running at night, so the night is charged at least
what it spent and can stop early, never late.

A FIRING IS CHARGED BEFORE ITS FIRST CALL. :func:`open_night` writes the
gate's total as the firing's mark before anything is asked of the provider,
and :func:`close_night` adds what the total moved by since and clears the
mark. A firing that died between the two leaves its mark, and the next firing
charges everything the total moved since it to its own night, whichever night
the dead one began in, so a crash is never a free night.

WHAT CANNOT BE READ REFUSES. A ledger that cannot be parsed, a gate whose
totals cannot be read, or a total below a firing's mark is a spend nobody can
measure, and the night pass makes no call over it. Only a ledger that does
not exist yet is an installation whose night pass has spent nothing.

THE STAGING LOCK SERIALIZES IT. Only the night pass, ``sync.night``, writes the
ledger, and it does so while holding :mod:`cratekit.core.staging_lock`, so two
firings never read and write it together.

Layer: core.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from cratekit.core import config, provider_gate
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy

#: The declared state entry, resolved under the gate's own directory (U278).
STATE_KEY = "night_budget"

#: The ledger's own schema version.
SCHEMA = 1

#: The hour, local time, a night begins and ends at.
NOON = 12

_ORIGIN = ("night_budget",)


def night_of(now: datetime) -> str:
    """The night ``now`` falls in, named by the date it began on."""
    local = now.astimezone()
    return (local - timedelta(hours=NOON)).date().isoformat()


def frees_at(now: datetime) -> datetime:
    """When the night ``now`` falls in ends, and the next one's budget begins."""
    local = now.astimezone()
    noon = local.replace(hour=NOON, minute=0, second=0, microsecond=0)
    return noon if local < noon else noon + timedelta(days=1)


@dataclass(frozen=True, slots=True)
class Ledger:
    """What the ledger holds: the night, its finished firings' spend, and the
    mark of a firing still open (or one that died)."""

    night: str | None = None
    spent: int = 0
    open_start: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "night": self.night,
            "spent": self.spent,
            "open": None if self.open_start is None else {"start": self.open_start},
        }


@dataclass(frozen=True, slots=True)
class Opened:
    """One firing's place in its night: the mark it wrote and what was left."""

    night: str
    start: int
    spent_before: int
    budget: int

    @property
    def remaining(self) -> int:
        return max(0, self.budget - self.spent_before)


def ledger_path() -> Path:
    return config.state_path(STATE_KEY)


def _unreadable(why: str, path: Path) -> CratekitError:
    return refuse(
        provider_gate.NIGHT,
        f"{why}, so what the night pass has spent tonight cannot be read and it "
        f"makes no call",
        remedy=Remedy.REPORT_DEFECT,
        steps=(f"look at {path} and the provider gate's state file beside it",),
        origin=_ORIGIN,
        detail={"ledger": str(path)},
    )


def _int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def read(path: Path | None = None) -> Ledger:
    """The ledger, an empty one when there is none yet, and a refusal when the
    file exists and cannot be understood."""
    target = path if path is not None else ledger_path()
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return Ledger()
    except OSError as exc:
        raise _unreadable(f"the night budget's ledger could not be read ({exc})", target) from None
    try:
        data = json.loads(text)
    except ValueError:
        raise _unreadable("the night budget's ledger is not JSON", target) from None
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise _unreadable("the night budget's ledger is not one this build reads", target)
    night = data.get("night")
    spent = _int(data.get("spent"))
    opened = data.get("open")
    start = None
    if opened is not None:
        start = _int(opened.get("start")) if isinstance(opened, dict) else None
        if start is None:
            raise _unreadable("the night budget's ledger holds a mark it cannot read", target)
    if spent is None or (night is not None and not isinstance(night, str)):
        raise _unreadable("the night budget's ledger holds a spend it cannot read", target)
    return Ledger(night=night, spent=spent, open_start=start)


def _write(ledger: Ledger, path: Path) -> None:
    config.mkdir_private(path.parent)
    payload = json.dumps(ledger.to_json(), indent=2, sort_keys=True) + "\n"
    config.atomic_write_bytes(payload.encode("utf-8"), path)


def _total(path: Path) -> int:
    """The gate's running total of calls, every identity's together."""
    spend = provider_gate.read_spend()
    if spend is None:
        raise _unreadable("the provider gate's state file could not be read", path)
    return spend.calls


def spent_tonight(now: datetime, *, path: Path | None = None) -> int:
    """What tonight has spent, its open mark charged as :func:`open_night`
    would charge it. For a report: it writes nothing."""
    target = path if path is not None else ledger_path()
    ledger = read(target)
    spent = ledger.spent if ledger.night == night_of(now) else 0
    if ledger.open_start is not None:
        moved = _total(target) - ledger.open_start
        if moved < 0:
            raise _unreadable(
                "the provider gate's running total is below the night pass's mark", target
            )
        spent += moved
    return spent


def open_night(budget: int, *, now: datetime, path: Path | None = None) -> Opened:
    """Charge this firing's place in its night and return it, or refuse when
    the night's budget is spent.

    A mark left by a firing that never closed is charged to tonight in full
    first, whichever night it began in, so the next firing starts from what it
    really spent; a mark of tonight's above the gate's total refuses, and one
    of an earlier night's is dropped.
    """
    target = path if path is not None else ledger_path()
    ledger = read(target)
    night = night_of(now)
    total = _total(target)
    spent = ledger.spent if ledger.night == night else 0
    if ledger.open_start is not None:
        # A DEAD FIRING'S MARK IS CHARGED TO TONIGHT, whichever night it began
        # in (review round one): a firing that died before noon and is read
        # after it spent calls nobody can place, so they are tonight's, early
        # and never late.
        moved = total - ledger.open_start
        if moved < 0 and ledger.night == night:
            raise _unreadable(
                "the provider gate's running total is below the mark an earlier "
                "firing of tonight left",
                target,
            )
        # A MARK OF AN EARLIER NIGHT ABOVE THE TOTAL is dropped at the new
        # night, as it was before the dead mark was charged (review round two):
        # what it spent cannot be read, and refusing over it would refuse every
        # night after until the ledger was edited by hand.
        spent += max(0, moved)
    if spent >= budget:
        # CHARGED BEFORE THE REFUSAL: a dead firing's mark is folded in, so
        # the ledger says what tonight spent and no mark is left to charge twice.
        _write(Ledger(night=night, spent=spent, open_start=None), target)
        frees = frees_at(now).isoformat(timespec="minutes")
        raise refuse(
            provider_gate.NIGHT,
            f"the night pass has spent {spent} of the {budget} calls to the streaming "
            f"provider it may make tonight, [provider] night_calls, counted from every "
            f"process that reads the gate, so it makes no call until the next night "
            f"begins at {frees}",
            remedy=Remedy.RETRY_LATER,
            steps=(
                f"the next night's pass runs after {frees}",
                "or raise [provider] night_calls for every night",
            ),
            origin=_ORIGIN,
            detail={"night": night, "spent": spent, "budget": budget, "frees_at": frees},
        )
    _write(Ledger(night=night, spent=spent, open_start=total), target)
    return Opened(night=night, start=total, spent_before=spent, budget=budget)


def close_night(opened: Opened, *, path: Path | None = None) -> int | None:
    """Add what this firing spent to its night and clear its mark; return the
    calls it spent, or None when that cannot be read. A gate that cannot be
    read, or a total below the mark, leaves the mark, so the next firing
    refuses over it rather than reading this one as free."""
    target = path if path is not None else ledger_path()
    try:
        total = _total(target)
    except CratekitError:
        return None
    spent = total - opened.start
    if spent < 0:
        return None
    _write(
        Ledger(night=opened.night, spent=opened.spent_before + spent, open_start=None), target
    )
    return spent


__all__ = [
    "NOON",
    "SCHEMA",
    "STATE_KEY",
    "Ledger",
    "Opened",
    "close_night",
    "frees_at",
    "ledger_path",
    "night_of",
    "open_night",
    "read",
    "spent_tonight",
]
