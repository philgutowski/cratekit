"""One gate for every call the product makes to the streaming provider (R-705).

The account must never be pushed into a rate limit block, so this is the
safety seam under every other provider concern. :meth:`Gate.attach` replaces
``request`` on a client's ``request_session``, so the gate sees the raw status
and ``Retry-After`` before anything can swallow them. Clients are built at two
sites, ``acquire/provider_session.py`` and ``acquire/vendored.py``, and a test
refuses a third. In one state file under one lock the gate keeps:

* **Pacing**: a minimum interval from the last call any process made.
* **A breaker**: :data:`TRIP_AFTER` consecutive rate limit answers, or a
  ``Retry-After`` at or above the cooldown, raise the job engine's ``Parked``,
  so an item in flight goes back to pending.
* **A cooldown that outlives the process**, asked by every opener through
  :meth:`Gate.assert_open` before it logs in.
* **One driver at a time**: the lock is held for one call and at most one
  interval, a ``Retry-After`` wait is taken outside it, and a lock wait past
  :data:`LOCK_WAIT_S` plus one interval parks rather than hangs.
* **Counts**, written BEFORE the send, since a crash mid request is still a
  call the account saw.
* **The call ceiling (U193)**: inside a :func:`command` scope a command stops
  before passing ``calls_per_command`` or its ``--calls``.
* **Two identities, one allowance (U205)**: account and app credential calls
  share every line, counted apart under ``identities``.
* **The hour's budget (U278)**: the file sits under ``config.provider_gate_dir``
  so every copy reads one gate, and a call that would take an identity's last
  sixty minutes past its line parks as :data:`BUDGET`; a command that only
  reads stops ``reserve_share`` short of ``calls_per_hour``.
* **The night's line (U293)**: :func:`night` holds a night pass to a line off
  the gate's running total, parking as :data:`NIGHT`.

Every line only ever lowers, and a refusal is a park, never a retry. Media
segments fetched from a content host are not provider API calls.
"""

from __future__ import annotations

import json
import math
import os
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy

#: The two declared state entries, installation scoped because the allowance
#: belongs to the account and not to a library.
STATE_KEY = "provider_gate"
LOCK_KEY = "provider_gate_lock"

#: Consecutive rate limit answers that trip the breaker: one attempt plus the
#: five retries ``acquire.listing.fetch_with_retry`` makes, pinned by a test.
TRIP_AFTER = 6

#: How long one call waits for the driver lock before refusing, on top of one
#: interval, since a holder holds it for one request and one interval at most.
LOCK_WAIT_S = 120.0

#: How often a waiting call asks for the lock again.
LOCK_POLL_S = 0.05

#: The provider's rate limit status.
RATE_LIMIT_STATUS = 429

#: The reasons this module refuses with, all declared in ``cause.REASONS``:
#: a trip cooling, the lock held, and a command at its ceiling (U193).
COOLDOWN = "provider-cooldown"
HELD = "provider-gate-held"
CEILING = "provider-call-ceiling"

#: How a ceiling raised for one run reaches a job's detached child, set by
#: :func:`command` only while its scope is open.
CALLS_ENV = "CRATEKIT_PROVIDER_CALLS"

#: The reason a call past its identity's line for the hour, or a ``--calls``
#: above the hour's whole budget, is refused with (U278).
BUDGET = "provider-budget"

#: How an hour's budget raised for one run reaches a detached child.
BUDGET_ENV = "CRATEKIT_PROVIDER_CALLS_PER_HOUR"

#: The reason a call past the night pass's own line stops with (U293).
NIGHT = "provider-night-budget"

#: How the night's line reaches a detached child, as ``START:CALLS:NIGHT``.
NIGHT_ENV = "CRATEKIT_PROVIDER_NIGHT"

#: The window the budget is counted over, and the size of one count in it. A
#: minute's calls leave the window an hour after the minute ENDS, so a call is
#: held for longer than an hour, never for less.
WINDOW_S = 3600
BUCKET_S = 60

#: The two identities a call is made under (U205).
ACCOUNT = "account"
APP = "app"
IDENTITIES = (ACCOUNT, APP)

#: This process's own spend across every gate it built, which the dispatcher
#: reports as the run's.
_PROCESS_CALLS = 0
_PROCESS_RATE_LIMITED = 0
#: The share of the two above made under the app credentials (U205).
_PROCESS_APP_CALLS = 0
_PROCESS_APP_RATE_LIMITED = 0

#: App values recorded in the installation's index and missing from the
#: keychain this run, so its lookups went to the account; cleared when a
#: command's scope opens.
_APP_LOST: list[str] = []


@dataclass(frozen=True, slots=True)
class GateSettings:
    """The numbers the configuration owns. Defaults are read when a settings
    object is built, never bound at import (``tests/test_config.py``)."""

    min_interval_s: float = field(
        default_factory=lambda: float(config.DEFAULT_PROVIDER_MIN_INTERVAL_S)
    )
    cooldown_s: float = field(default_factory=lambda: float(config.DEFAULT_PROVIDER_COOLDOWN_S))
    calls_per_command: int = field(
        default_factory=lambda: int(config.DEFAULT_PROVIDER_CALLS_PER_COMMAND)
    )
    calls_per_hour: int = field(default_factory=lambda: int(config.DEFAULT_PROVIDER_CALLS_PER_HOUR))
    reserve_share: float = field(
        default_factory=lambda: float(config.DEFAULT_PROVIDER_RESERVE_SHARE)
    )

    @classmethod
    def from_config(cls, cfg: Any) -> GateSettings:
        """Read ``[provider]`` off a loaded configuration, passed in so a job
        runs against the configuration frozen when it was queued."""
        provider = cfg.provider
        return cls(
            min_interval_s=float(provider.min_interval_s),
            cooldown_s=float(provider.cooldown_s),
            calls_per_command=int(provider.calls_per_command),
            calls_per_hour=int(provider.calls_per_hour),
            reserve_share=float(provider.reserve_share),
        )


@dataclass(frozen=True, slots=True)
class Spend:
    """Calls made and rate limit answers received, as running totals of every
    identity; the ``app_`` pair is the app credentials' share (U205)."""

    calls: int = 0
    rate_limited: int = 0
    app_calls: int = 0
    app_rate_limited: int = 0

    @property
    def account_calls(self) -> int:
        return max(0, self.calls - self.app_calls)

    @property
    def account_rate_limited(self) -> int:
        return max(0, self.rate_limited - self.app_rate_limited)

    def since(self, earlier: Spend) -> Spend:
        """What was spent between ``earlier`` and this snapshot."""
        return Spend(
            calls=max(0, self.calls - earlier.calls),
            rate_limited=max(0, self.rate_limited - earlier.rate_limited),
            app_calls=max(0, self.app_calls - earlier.app_calls),
            app_rate_limited=max(0, self.app_rate_limited - earlier.app_rate_limited),
        )


@dataclass
class _State:
    """The state file's contents, in epoch seconds since every process on the
    machine reads it against a wall clock."""

    last_call: float = 0.0
    not_before: float = 0.0
    consecutive: int = 0
    tripped_at: float | None = None
    lifts_at: float | None = None
    calls: int = 0
    rate_limited: int = 0
    trips: int = 0
    #: The share of ``calls`` and ``rate_limited`` the app credentials made.
    app_calls: int = 0
    app_rate_limited: int = 0
    #: Each identity's calls by minute, pruned on every write (U278).
    window: dict[str, dict[int, int]] = field(default_factory=lambda: {i: {} for i in IDENTITIES})

    def cooling(self, now: float) -> bool:
        return self.lifts_at is not None and now < self.lifts_at

    def spent(self, identity: str, now: float) -> int:
        """The identity's calls in the window at ``now``."""
        return sum(_live(self.window.get(identity, {}), now).values())

    def totals(self) -> Spend:
        return Spend(self.calls, self.rate_limited, self.app_calls, self.app_rate_limited)

    def settle(self, now: float) -> bool:
        """Keep the window as :func:`_live` reads it at ``now``. True when it
        moved, so the caller writes it and a minute from the future is placed
        once rather than held until the clock catches up."""
        moved = False
        for identity in IDENTITIES:
            held = self.window.get(identity, {})
            live = _live(held, now)
            if live != held:
                self.window[identity] = live
                moved = True
        return moved

    def count(self, identity: str, now: float) -> None:
        """One more call by ``identity`` at ``now``, and the window pruned."""
        minutes = _live(self.window.get(identity, {}), now)
        bucket = _bucket(now)
        minutes[bucket] = minutes.get(bucket, 0) + 1
        self.window[identity] = minutes

    def to_json(self) -> dict[str, Any]:
        return {
            "last_call": self.last_call, "not_before": self.not_before,
            "consecutive": self.consecutive, "tripped_at": self.tripped_at,
            "lifts_at": self.lifts_at, "calls": self.calls,
            "rate_limited": self.rate_limited, "trips": self.trips,
            "identities": {
                ACCOUNT: {
                    "calls": max(0, self.calls - self.app_calls),
                    "rate_limited": max(0, self.rate_limited - self.app_rate_limited),
                },
                APP: {"calls": self.app_calls, "rate_limited": self.app_rate_limited},
            },
            "window": {
                identity: {str(bucket): n for bucket, n in sorted(minutes.items())}
                for identity, minutes in self.window.items()
            },
        }

    @classmethod
    def from_json(cls, data: Any) -> _State:
        if not isinstance(data, dict):
            return cls()
        state = cls()
        for name in ("last_call", "not_before"):
            setattr(state, name, _as_float(data.get(name), 0.0))
        for name in ("consecutive", "calls", "rate_limited", "trips"):
            setattr(state, name, _as_int(data.get(name)))
        for name in ("tripped_at", "lifts_at"):
            value = data.get(name)
            setattr(state, name, None if value is None else _as_float(value, None))
        # No ``identities`` is a file from before U205, every call the
        # account's. An app share above its total is clamped to it.
        identities = data.get("identities")
        app = identities.get(APP) if isinstance(identities, dict) else None
        if isinstance(app, dict):
            state.app_calls = min(_as_int(app.get("calls")), state.calls)
            state.app_rate_limited = min(_as_int(app.get("rate_limited")), state.rate_limited)
        # No ``window`` is a file from before U278, read as nothing spent.
        state.window = _window_from_json(data.get("window"))
        return state


@dataclass(frozen=True, slots=True)
class Night:
    """The night pass's line (U293): ``budget`` more calls past ``start``, the
    gate's running total when the firing began, on the night named ``night``."""

    start: int
    budget: int
    night: str

    def to_env(self) -> str:
        return f"{self.start}:{self.budget}:{self.night}"

    @classmethod
    def from_env(cls, text: str) -> Night | None:
        """The line off :data:`NIGHT_ENV`, or None when it cannot be read."""
        parts = text.strip().split(":", 2)
        if len(parts) != 3:
            return None
        start, budget, night = parts
        if not all(part.isascii() and part.isdigit() for part in (start, budget)) or not night:
            return None
        return cls(start=int(start), budget=int(budget), night=night)


@dataclass
class Command:
    """One command's ceiling scope around a verb: ``started`` is this process's
    call count when it began, ``raised`` its ``--calls``, and ``stopped`` the
    refusal the gate raised, kept for a verb that catches a park per item."""

    started: int
    raised: int | None = None
    stopped: Cause | None = None
    #: Whether this command may spend the hour's reserve (U278), only ever
    #: narrowed by :func:`reading`.
    reserve: bool = False
    #: The hour's budget raised for this run, or None for the configured one.
    hourly: int | None = None
    #: The class the scope was opened with, which :func:`spending` returns to.
    declared: bool = False
    #: The night pass's line while :func:`night` holds it (U293).
    night: Night | None = None

    def spent(self) -> int:
        return max(0, _PROCESS_CALLS - self.started)


#: The open command scope, or None outside the dispatcher.
_COMMAND: Command | None = None


def _positive_env(name: str) -> int | None:
    """A positive whole number off ``name``, else None, so a value that cannot
    be read never lifts the configured line."""
    text = os.environ.get(name, "").strip()
    if not (text.isascii() and text.isdigit()):
        return None
    value = int(text)
    return value if value > 0 else None


def _raised_from_env() -> int | None:
    """The ceiling a parent run raised, off :data:`CALLS_ENV`."""
    return _positive_env(CALLS_ENV)


def _hour_from_env() -> int | None:
    """The hour's budget a parent run raised, off :data:`BUDGET_ENV`."""
    return _positive_env(BUDGET_ENV)


def _night_from_env() -> Night | None:
    """The night's line a parent run opened, off :data:`NIGHT_ENV`."""
    text = os.environ.get(NIGHT_ENV, "")
    return Night.from_env(text) if text.strip() else None


@contextmanager
def _exported(name: str, value: int | str | None) -> Iterator[None]:
    """``name`` set to ``value`` for the body, and put back as it was after."""
    if value is None:
        yield
        return
    previous = os.environ.get(name)
    os.environ[name] = str(value)
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = previous


@contextmanager
def command(
    calls: int | None = None, *, calls_per_hour: int | None = None, reserve: bool = False
) -> Iterator[Command]:
    """Open one command's ceiling scope for the length of a verb.

    ``calls`` and ``calls_per_hour`` are raised for this run and exported to a
    detached child; ``reserve`` is whether the verb may spend the reserve. A
    nested scope yields the OUTER one, so a ceiling is never spent twice, with
    the inner verb's class for the body.
    """
    global _COMMAND
    if _COMMAND is not None:
        outer = _COMMAND
        before = (outer.reserve, outer.declared)
        outer.reserve = outer.declared = bool(reserve)
        try:
            yield outer
        finally:
            outer.reserve, outer.declared = before
        return
    raised = calls if calls is not None else _raised_from_env()
    hourly_raised = calls_per_hour if calls_per_hour is not None else _hour_from_env()
    _APP_LOST.clear()
    scope = Command(
        started=_PROCESS_CALLS, raised=raised, reserve=bool(reserve), hourly=hourly_raised,
        declared=bool(reserve),
        night=_night_from_env(),
    )
    with _exported(CALLS_ENV, calls), _exported(BUDGET_ENV, calls_per_hour):
        _COMMAND = scope
        try:
            yield scope
        finally:
            _COMMAND = None


@contextmanager
def night(
    start: int, calls: int, label: str, *, calls_per_hour: int, settings: GateSettings
) -> Iterator[Night]:
    """Hold the open command to the night pass's line for the body (U293).

    The line is ``calls`` past ``start`` (the gate's total when the firing
    began), never past what is left of the command's ceiling, and the hour
    only lowers to ``calls_per_hour``. Both are exported to a detached child.
    """
    scope = _COMMAND
    if scope is None:
        raise RuntimeError("the night's line is opened inside a command's scope only")
    left_of_ceiling = max(0, min(ceiling(settings), settings.calls_per_command) - scope.spent())
    held = Night(
        start=max(0, int(start)), budget=max(0, min(int(calls), left_of_ceiling)), night=label
    )
    if scope.night is not None:
        # Nested, the outer night's remainder is never widened.
        outer = scope.night
        left = outer.start + outer.budget - held.start
        if left < held.budget:
            held = Night(start=held.start, budget=max(0, left), night=held.night)
    hour = min(hourly(settings), max(1, int(calls_per_hour)))
    before = (scope.night, scope.hourly)
    scope.night = held
    scope.hourly = hour
    try:
        with _exported(NIGHT_ENV, held.to_env()), _exported(BUDGET_ENV, hour):
            yield held
    finally:
        scope.night, scope.hourly = before


def _night() -> Night | None:
    """The night's line the next call runs under: the open command's, else a
    parent's off the environment."""
    scope = _COMMAND
    return scope.night if scope is not None else _night_from_env()


def command_spent() -> int:
    """The calls the open command has made so far, 0 outside a scope."""
    scope = _COMMAND
    return scope.spent() if scope is not None else 0


def ceiling(settings: GateSettings | None = None) -> int:
    """The ceiling the open command runs under: the raised one, else the configured."""
    scope = _COMMAND
    if scope is not None and scope.raised is not None:
        return scope.raised
    return (settings or GateSettings()).calls_per_command


# The hour's budget (U278)


def _bucket(epoch: float) -> int:
    """The minute a call falls in, as the epoch second it starts at."""
    return int(epoch // BUCKET_S) * BUCKET_S


def _expires(bucket: int) -> float:
    """When a minute's calls leave the window: an hour after the minute ENDS,
    so a line read off it is never crossed by a call forgotten early."""
    return float(bucket + BUCKET_S + WINDOW_S)


def _live(window: Mapping[int, int], now: float) -> dict[int, int]:
    """The minutes still inside the window at ``now``.

    A minute stamped in the future, which only a clock set back writes, is
    counted in the current minute: dropped it would hand out a fresh hour,
    kept it would hold the line until the clock reached it.
    """
    current = _bucket(now)
    live: dict[int, int] = {}
    for bucket, n in window.items():
        if n <= 0:
            continue
        at = min(bucket, current)
        if _expires(at) > now:
            live[at] = live.get(at, 0) + n
    return live


def _frees_at(window: Mapping[int, int], now: float, line: int) -> float:
    """The first moment the window holds fewer calls than ``line``; a line of
    zero is answered with the moment the last minute leaves."""
    live = _live(window, now)
    spent = sum(live.values())
    if spent < line:
        return now
    over = spent - line + 1
    gone = 0
    last = now
    for bucket in sorted(live):
        gone += live[bucket]
        last = _expires(bucket)
        if gone >= over:
            return last
    return last


def _window_from_json(raw: Any) -> dict[str, dict[int, int]]:
    """Each identity's minutes off the file. An entry that cannot be read is
    dropped, since a corrupt counter must not lock the provider out."""
    window: dict[str, dict[int, int]] = {identity: {} for identity in IDENTITIES}
    if not isinstance(raw, dict):
        return window
    for identity in IDENTITIES:
        minutes = raw.get(identity)
        if not isinstance(minutes, dict):
            continue
        for key, value in minutes.items():
            try:
                bucket = int(key)
            except (TypeError, ValueError):
                continue
            count = _as_int(value)
            if count:
                window[identity][bucket] = window[identity].get(bucket, 0) + count
    return window


def hourly(settings: GateSettings | None = None) -> int:
    """The hour's budget for each identity: raised for this run, else the configured."""
    scope = _COMMAND
    if scope is not None and scope.hourly is not None:
        return scope.hourly
    raised = _hour_from_env() if scope is None else None
    if raised is not None:
        return raised
    return (settings or GateSettings()).calls_per_hour


def reserve_of(budget: int, share: float) -> int:
    """The calls of ``budget`` kept for writes and downloads, rounded UP."""
    return min(budget, max(0, math.ceil(round(budget * share, 6))))


def _reserving() -> bool:
    scope = _COMMAND
    return scope.reserve if scope is not None else False


def line_for(settings: GateSettings | None = None, *, reserve: bool | None = None) -> int:
    """How many calls an identity may have in the window before the next is
    refused: the whole budget with the reserve, less it without. ``reserve``
    None asks the open command, and outside a scope means the read line."""
    settings = settings or GateSettings()
    budget = hourly(settings)
    if reserve is None:
        reserve = _reserving()
    if reserve:
        return budget
    return budget - reserve_of(budget, settings.reserve_share)


@contextmanager
def spending() -> Iterator[None]:
    """Let the body spend the reserve if the verb declared it may (U278), for
    the go inside a read mode; never past the declared class."""
    scope = _COMMAND
    if scope is None:
        yield
        return
    before = scope.reserve
    scope.reserve = scope.declared
    try:
        yield
    finally:
        scope.reserve = before


def reading(settings: GateSettings | None = None) -> None:
    """Hold the open command to the read line from here on (U278); it only
    ever narrows. Given ``settings``, a ``--calls`` past the hour's budget is
    refused at once rather than at the first call."""
    scope = _COMMAND
    if scope is None:
        return
    scope.reserve = False
    if settings is not None:
        refused = over_the_line(settings)
        if refused is not None:
            raise CratekitError(refused)


def _who(identity: str) -> str:
    return "the account" if identity == ACCOUNT else "Cratekit's app credentials"


def _class_words(reserve: bool, budget: int, line: int) -> str:
    if reserve:
        return f"the whole of the hour's budget of {budget}"
    return (
        f"the line a command that only reads may reach, {line} of the hour's {budget}, "
        f"the other {budget - line} being kept for writes and downloads"
    )


def _calls_word(n: int) -> str:
    return "call" if n == 1 else "calls"


def hour_to_name(calls: int, settings: GateSettings | None = None) -> int | None:
    """The ``--calls-per-hour`` a printed command naming ``--calls calls`` must
    carry, or None when the configured hour already holds it (U278): the
    larger of the two, whenever it passes ``[provider] calls_per_hour``."""
    settings = settings or GateSettings()
    wanted = max(int(calls), hourly(settings))
    return wanted if wanted > settings.calls_per_hour else None


def hour_args(calls: int, settings: GateSettings | None = None) -> list[str]:
    """:func:`hour_to_name` as command line words, empty when none is needed."""
    hour = hour_to_name(calls, settings)
    return ["--calls-per-hour", str(hour)] if hour is not None else []


def over_the_line(settings: GateSettings | None = None) -> Cause | None:
    """The refusal for a ``--calls`` raised past the hour's budget, or None.

    Never a silent cap. Measured against the WHOLE budget, not this command's
    line, since a wrapper verb runs another whose line may be higher.
    """
    scope = _COMMAND
    if scope is None or scope.raised is None:
        return None
    settings = settings or GateSettings()
    budget = hourly(settings)
    if scope.raised <= budget:
        return None
    return _run_cause(
        reason=BUDGET,
        message=(
            f"--calls {scope.raised} asks for more calls than any command may make in "
            f"an hour, the hour's budget of {budget} for each identity, so nothing was "
            f"asked of the streaming provider"
        ),
        remediation=Remediation(
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(
                f"run it again with --calls {budget} or lower",
                "or raise the hour's budget for one run with --calls-per-hour, or "
                "[provider] calls_per_hour for every run",
            ),
        ),
        detail={"raised": scope.raised, "budget": budget, "reserve": scope.reserve},
    )


def _run_cause(
    reason: str, message: str, remediation: Remediation, detail: dict[str, Any]
) -> Cause:
    """A refusal of the whole run, never retryable."""
    return Cause(
        reason=reason, message=message, remediation=remediation, scope=Scope.RUN,
        retryable=False, origin=("provider_gate",), detail=detail,
    )


def _as_float(value: Any, fallback: Any) -> Any:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _as_int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iso(epoch: float) -> str:
    """An epoch second as the gate's refusals print it, for a report beside them."""
    return _iso(epoch)


# Retry-After, parsed in ONE place


def header_value(headers: object, name: str) -> object | None:
    """Read one header whether or not the container preserves case, so a
    plain dictionary never hides a wait the provider asked for."""
    get = getattr(headers, "get", None)
    if get is None:
        return None
    for candidate in (name, name.lower(), name.upper()):
        try:
            value = get(candidate)
        except (AttributeError, TypeError):
            return None
        if value is not None:
            return value
    if isinstance(headers, Mapping):
        wanted = name.lower()
        for key, value in headers.items():
            if isinstance(key, str) and key.lower() == wanted:
                return value
    return None


def retry_after_seconds(value: object, now: float) -> float | None:
    """Coerce a retry hint to seconds from ``now``, delta seconds or a date.

    The date form is parsed rather than dropped, since our own capped backoff
    would ask again too soon. THE ONE PARSER of this header in the tree.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value) if value >= 0 else None
    if not isinstance(value, str):
        return None
    text = value.strip()
    try:
        seconds = float(text)
    except ValueError:
        pass
    else:
        return seconds if seconds >= 0 else None
    try:
        when = parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError):
        return None
    if when is None:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0.0, when.timestamp() - now)


def _retry_after_of(response: Any, now: float) -> float:
    """The response's ``Retry-After`` in seconds, or zero when none can be
    read, since the consecutive count still trips the breaker."""
    headers = getattr(response, "headers", None)
    return retry_after_seconds(header_value(headers, "Retry-After"), now) or 0.0


# The gate


class Gate:
    """The pacing gate over one provider account, shared across processes.
    ``clock`` and ``sleep`` are injectable so a suite drives every schedule."""

    def __init__(
        self,
        settings: GateSettings | None = None,
        *,
        path: Path | None = None,
        lock_path: Path | None = None,
        clock: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.settings = settings or GateSettings()
        self.path = path if path is not None else config.state_path(STATE_KEY)
        self.lock_path = lock_path if lock_path is not None else config.state_path(LOCK_KEY)
        self._clock = clock
        self._sleep = sleep
        #: This gate's own spend.
        self.calls = 0
        self.rate_limited = 0
        #: The last park this gate raised and nothing has cleared since, for
        #: :meth:`raise_if_parked` after a tool that swallows exceptions.
        self._last_park: CratekitError | None = None

    # ── the state file ────────────────────────────────────────────────────

    def _read(self) -> _State:
        """A file that cannot be read counts as fresh, because a corrupt
        counter must not lock the provider out."""
        try:
            return _State.from_json(json.loads(self.path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            return _State()

    def _write(self, state: _State) -> None:
        config.mkdir_private(self.path.parent)
        payload = json.dumps(state.to_json(), indent=2, sort_keys=True) + "\n"
        config.atomic_write_bytes(payload.encode("utf-8"), self.path)

    def window_spend(self, identity: str = ACCOUNT) -> int:
        """The identity's calls in the last hour, off the state file (U278)."""
        return self._read().spent(identity, self._clock())

    def spend(self) -> Spend:
        """The running totals across every process, off the state file."""
        return self._read().totals()

    # ── the lock ──────────────────────────────────────────────────────────

    @contextmanager
    def _held(self) -> Iterator[None]:
        """Hold the one call at a time lock, or refuse naming the wait.

        Polled with ``LOCK_NB`` so the wait has an end a fake clock can drive.
        The file is never unlinked, so two processes never each hold "the" lock.
        """
        config.mkdir_private(self.lock_path.parent)
        fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        try:
            try:
                import fcntl  # noqa: PLC0415 - POSIX only, see the except
            except ImportError:  # pragma: no cover - no advisory locks here
                fcntl = None
            if fcntl is not None:
                limit = LOCK_WAIT_S + self.settings.min_interval_s
                started = self._clock()
                polls = 0
                while True:
                    try:
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        polls += 1
                        waited = self._clock() - started
                        if waited >= limit or polls >= limit / LOCK_POLL_S:
                            raise self._stopped(self._held_cause(waited)) from None
                        self._sleep(LOCK_POLL_S)
                os.ftruncate(fd, 0)
                os.write(fd, json.dumps({"pid": os.getpid()}).encode("utf-8"))
            yield
        finally:
            os.close(fd)  # closing the descriptor releases the lock; the file stays

    # ── the refusals ──────────────────────────────────────────────────────

    def _held_cause(self, waited: float) -> Cause:
        """A lock held past the wait is a fact about the ACCOUNT, so it parks
        like a trip rather than sending every item into the same wait."""
        return _run_cause(
            reason=HELD,
            message=(
                f"another driver has held the streaming provider for "
                f"{waited:.0f} seconds without finishing a call; one call at a "
                f"time per account, so this run stopped without making one and "
                f"the remaining items stay queued"
            ),
            remediation=Remediation(remedy=Remedy.WAIT_FOR_HOLDER),
            detail={"lock": str(self.lock_path), "waited_s": round(waited, 3)},
        )

    def _cooldown_cause(self, state: _State, now: float, *, tripped_now: bool) -> Cause:
        lifts = float(state.lifts_at or now)
        remaining = max(0, int(round(lifts - now)))
        if tripped_now:
            opening = (
                f"the streaming provider answered rate limited {TRIP_AFTER} calls in "
                f"a row, so this run stopped without asking it anything further"
            )
        else:
            opening = (
                f"the streaming provider rate limited this account at "
                f"{_iso(float(state.tripped_at or now))} and the cooldown has not "
                f"lifted, so nothing was asked of it"
            )
        return _run_cause(
            reason=COOLDOWN,
            message=(
                f"{opening}; every provider call is refused until {_iso(lifts)}, "
                f"{remaining} seconds from now, and the remaining items stay queued"
            ),
            remediation=Remediation(
                remedy=Remedy.RETRY_LATER,
                steps=(f"wait until {_iso(lifts)}", "then resume the job, or run the verb again"),
            ),
            detail={
                "tripped_at": _iso(float(state.tripped_at or now)), "lifts_at": _iso(lifts),
                "remaining_s": remaining, "cooldown_s": self.settings.cooldown_s,
                "rate_limited": state.rate_limited,
            },
        )

    def _ceiling_cause(self, scope: Command, line: int) -> Cause:
        spent = scope.spent()
        where = (
            "the ceiling raised for this run with --calls"
            if scope.raised is not None
            else "the ceiling for one command, [provider] calls_per_command"
        )
        # Doubled, but held to the hour's budget so the continue is never one
        # the hour refuses (U278). Never "what it did is kept" (U217).
        reach = hourly(self.settings)
        higher = min(line * 2, reach) if reach > line else line * 2
        hour = hour_to_name(higher, self.settings)
        raise_hour = f" --calls-per-hour {hour}" if hour is not None else ""
        return _run_cause(
            reason=CEILING,
            message=(
                f"this command made {spent} {_calls_word(spent)} to the "
                f"streaming provider, "
                f"{where}, so it stopped before the next one and the remaining items "
                f"stay queued; what it read and did not keep is read again when it "
                f"continues"
            ),
            remediation=Remediation(
                remedy=Remedy.FIX_COMMAND_LINE,
                steps=(
                    # The stored form, naming both shapes; the dispatcher
                    # replaces it with the one exact command.
                    f"continue with a higher ceiling for one run: a parked job with "
                    f"crate --calls {higher}{raise_hour} job resume JOB_ID, any other "
                    f"command by running it again with --calls {higher}{raise_hour} "
                    f"before it",
                    "or raise [provider] calls_per_command in the configuration for every run",
                ),
            ),
            detail={
                "calls": spent, "ceiling": line, "raised": scope.raised is not None,
                "higher": higher, "calls_per_hour": hour,
            },
        )

    def _budget_cause(
        self, state: _State, identity: str, now: float, line: int, spent: int
    ) -> Cause:
        """The hour's line reached for one identity (U278), parked like a trip
        and never retryable, since asking again inside the hour is the harm."""
        reserve = _reserving()
        budget = hourly(self.settings)
        frees = _frees_at(state.window.get(identity, {}), now, line)
        return _run_cause(
            reason=BUDGET,
            message=(
                f"{_who(identity)} has made {spent} {_calls_word(spent)} to the streaming "
                f"provider in the last "
                f"hour, from every command and copy that reads this gate, and "
                f"{_class_words(reserve, budget, line)}, so this run stopped before the "
                f"next call and the remaining items stay queued; the line frees at "
                f"{_iso(frees)}"
            ),
            remediation=Remediation(
                remedy=Remedy.RETRY_LATER,
                steps=(
                    f"wait until {_iso(frees)}, then resume the job, or run the verb again",
                    f"or raise the hour's budget for one run with crate --calls-per-hour "
                    f"{budget * 2} before the verb, or [provider] calls_per_hour for every run",
                ),
            ),
            detail={
                "identity": identity, "spent": spent, "line": line, "budget": budget,
                "reserve": reserve, "frees_at": _iso(frees), "window_s": WINDOW_S,
            },
        )

    def _night_cause(self, state: _State, held: Night) -> Cause:
        """The night pass's line reached (U293), or a running total below its
        mark, a spend nobody can read. Parked, never retryable."""
        spent = state.calls - held.start
        if spent < 0:
            message = (
                f"the provider gate's running total is {state.calls}, below the "
                f"{held.start} it held when the night pass of {held.night} began, so "
                f"what the night has spent cannot be read and the night pass "
                f"stopped before the next call"
            )
        else:
            message = (
                f"the night pass of {held.night} has made {spent} {_calls_word(spent)} to "
                f"the streaming provider since it began, counted from every command and "
                f"copy that reads this gate, and its line was {held.budget}, the lower "
                f"of what was left of the night's budget, [provider] night_calls, and "
                f"of one command's ceiling, [provider] calls_per_command, so it "
                f"stopped before the next call and the remaining items stay queued"
            )
        return _run_cause(
            reason=NIGHT,
            message=message,
            remediation=Remediation(
                remedy=Remedy.RETRY_LATER,
                steps=(
                    "the night pass's next firing continues it, or continue it by hand "
                    "at the Mac with crate sync land --pass-run and the pass's run",
                    "or raise [provider] night_calls, or [provider] calls_per_command "
                    "when one command's ceiling set the line",
                ),
            ),
            detail={
                "night": held.night, "spent": spent, "budget": held.budget,
                "start": held.start, "total": state.calls,
            },
        )

    def _stopped(self, cause: Cause) -> CratekitError:
        """A refusal as the job engine's own park, so an item in flight is
        released rather than failed. Imported here to avoid an import cycle."""
        from cratekit.core.jobs import Parked  # noqa: PLC0415 - see docstring

        parked = Parked(cause)
        self._last_park = parked
        return parked

    def _parked(self, scope: Command | None, cause: Cause) -> CratekitError:
        """:meth:`_stopped`, with the refusal kept on the open command."""
        if scope is not None:
            scope.stopped = cause
        return self._stopped(cause)

    # ── the public surface ────────────────────────────────────────────────

    def assert_open(self) -> None:
        """Refuse, naming the lift time, when a trip is still cooling. Asked by
        every opener before it logs in, off the shared file."""
        state = self._read()
        now = self._clock()
        if state.cooling(now):
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

    def raise_if_parked(self) -> None:
        """Re-raise a park a caller swallowed, then ask the file, for the
        vendored downloader, which answers "no" over every exception."""
        if self._last_park is not None:
            raise self._last_park
        self.assert_open()

    def call(self, send: Callable[[], Any], *, identity: str = ACCOUNT) -> Any:
        """Make one provider call under the lock, paced, counted and watched.

        An exception out of ``send`` is the caller's, not a rate limit answer.
        A wait longer than one interval, which only a ``Retry-After`` makes, is
        taken with the lock RELEASED and the call asked for again after it.
        """
        if identity not in IDENTITIES:
            raise ValueError(f"no provider identity is named {identity!r}")
        while True:
            with self._held():
                state = self._read()
                now = self._clock()
                if state.cooling(now):
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))
                # After the cooldown: a settled window the filesystem refuses
                # is left to the next write rather than raised.
                if state.settle(now):
                    try:
                        self._write(state)
                    except OSError:
                        pass
                scope = _COMMAND
                # The hour, then the night, then the ceiling, all before the send.
                over = over_the_line(self.settings)
                if over is not None:
                    raise self._parked(scope, over)
                hour_line = line_for(self.settings)
                spent = state.spent(identity, now)
                if spent >= hour_line:
                    cause = self._budget_cause(state, identity, now, hour_line, spent)
                    raise self._parked(scope, cause)
                held_night = _night()
                if held_night is not None and (
                    state.calls - held_night.start >= held_night.budget
                    or state.calls < held_night.start
                ):
                    raise self._parked(scope, self._night_cause(state, held_night))
                if scope is not None:
                    line = ceiling(self.settings)
                    if scope.spent() >= line:
                        raise self._parked(scope, self._ceiling_cause(scope, line))
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)
                if due - now > self.settings.min_interval_s:
                    long_wait = due - now
                else:
                    return self._send_now(send, state, now, due, identity)
            self._sleep(long_wait)

    def _send_now(
        self, send: Callable[[], Any], state: _State, now: float, due: float, identity: str
    ) -> Any:
        """The call itself, under the lock, with at most one interval's wait."""
        global _PROCESS_CALLS, _PROCESS_RATE_LIMITED, _PROCESS_APP_CALLS, _PROCESS_APP_RATE_LIMITED
        app = identity == APP
        if due > now:
            self._sleep(due - now)
            now = max(self._clock(), due)
        state.last_call = now
        state.calls += 1
        state.count(identity, now)
        self.calls += 1
        _PROCESS_CALLS += 1
        if app:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
        self._write(state)

        response = send()

        if getattr(response, "status_code", None) == RATE_LIMIT_STATUS:
            now = self._clock()
            self.rate_limited += 1
            _PROCESS_RATE_LIMITED += 1
            state.rate_limited += 1
            if app:
                state.app_rate_limited += 1
                _PROCESS_APP_RATE_LIMITED += 1
            state.consecutive += 1
            retry_after = _retry_after_of(response, now)
            if retry_after > 0:
                state.not_before = max(state.not_before, now + retry_after)
            if state.consecutive >= TRIP_AFTER or retry_after >= self.settings.cooldown_s:
                state.tripped_at = now
                state.lifts_at = now + max(self.settings.cooldown_s, retry_after)
                state.consecutive = 0
                state.trips += 1
                self._write(state)
                raise self._stopped(self._cooldown_cause(state, now, tripped_now=True))
            self._write(state)
            return response

        state.consecutive = 0
        state.not_before = 0.0
        self._last_park = None
        self._write(state)
        return response

    def attach(self, client: Any, *, identity: str = ACCOUNT) -> bool:
        """Route every request of the client's ``request_session`` through this
        gate under ``identity``, replacing ``request`` ON THE INSTANCE and only
        once. False for a client with no such transport."""
        if identity not in IDENTITIES:
            raise ValueError(f"no provider identity is named {identity!r}")
        transport = getattr(client, "request_session", None)
        if transport is None or not callable(getattr(transport, "request", None)):
            return False
        original = getattr(transport, "_cratekit_unpaced_request", None) or transport.request

        def gated(method: Any, url: Any, *args: Any, **kwargs: Any) -> Any:
            return self.call(lambda: original(method, url, *args, **kwargs), identity=identity)

        transport._cratekit_unpaced_request = original
        transport._cratekit_gate = self
        transport.request = gated
        return True


def spend(path: Path | None = None) -> Spend:
    """The running totals off the state file, for a report that holds no gate."""
    return Gate(path=path).spend()


def process_spend() -> Spend:
    """What THIS process has spent, across every gate it built."""
    return Spend(
        calls=_PROCESS_CALLS, rate_limited=_PROCESS_RATE_LIMITED,
        app_calls=_PROCESS_APP_CALLS,
        app_rate_limited=_PROCESS_APP_RATE_LIMITED,
    )


def note_app_lost(name: str) -> None:
    """Say that a recorded app value was missing from the keychain this run."""
    if name not in _APP_LOST:
        _APP_LOST.append(name)


def app_lost() -> tuple[str, ...]:
    """The app values this run found recorded and missing, in the order found."""
    return tuple(_APP_LOST)


def _report_state(target: Path) -> _State | None:
    """The state file for a report, or None when it cannot be read. A missing
    file raises ``FileNotFoundError`` for the caller to answer."""
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except OSError:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    return _State.from_json(data) if isinstance(data, dict) else None


def read_spend(path: Path | None = None) -> Spend | None:
    """The running totals off the state file, or None when it cannot be read.

    For a report, not for the gate: a report that read a corrupt file as fresh
    would show zero calls over a file it never read. A file that does not
    exist yet is nothing spent.
    """
    target = path if path is not None else config.state_path(STATE_KEY)
    try:
        state = _report_state(target)
    except FileNotFoundError:
        return Spend()
    return None if state is None else state.totals()


@dataclass(frozen=True, slots=True)
class Standing:
    """Where the account stands in the hour, off the one gate, for a report
    (U278): each identity's calls by minute, read at the one moment ``now``."""

    window: Mapping[str, Mapping[int, int]]
    now: float
    path: Path
    tripped_at: float | None = None
    lifts_at: float | None = None

    def spent(self, identity: str) -> int:
        return sum(_live(self.window.get(identity, {}), self.now).values())

    def frees_at(self, identity: str, line: int) -> float:
        return _frees_at(self.window.get(identity, {}), self.now, line)

    def cooling(self) -> bool:
        return self.lifts_at is not None and self.now < self.lifts_at


def read_standing(now: float | None = None, *, path: Path | None = None) -> Standing | None:
    """The hour's spend and any cooldown off the one gate, or None when its
    file cannot be read, on :func:`read_spend`'s rule."""
    target = path if path is not None else config.state_path(STATE_KEY)
    moment = time.time() if now is None else now
    try:
        state = _report_state(target)
    except FileNotFoundError:
        return Standing(window={}, now=moment, path=target)
    if state is None:
        return None
    return Standing(
        window=state.window, now=moment, path=target,
        tripped_at=state.tripped_at, lifts_at=state.lifts_at,
    )


__all__ = [
    "ACCOUNT", "APP", "BUCKET_S", "BUDGET", "BUDGET_ENV", "CALLS_ENV", "CEILING", "COOLDOWN",
    "HELD", "IDENTITIES", "LOCK_KEY", "LOCK_POLL_S", "LOCK_WAIT_S", "NIGHT", "NIGHT_ENV",
    "Night", "RATE_LIMIT_STATUS", "STATE_KEY", "app_lost", "TRIP_AFTER", "Command", "Gate",
    "GateSettings", "Spend", "Standing", "WINDOW_S", "ceiling", "command", "command_spent",
    "header_value", "hour_args", "hour_to_name", "hourly", "iso", "line_for", "night",
    "note_app_lost", "over_the_line", "process_spend", "read_spend", "read_standing",
    "reading", "spending", "reserve_of", "retry_after_seconds", "spend",
]
