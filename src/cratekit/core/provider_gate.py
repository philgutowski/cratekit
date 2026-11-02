"""One gate for every call the product makes to the streaming provider (R-705).

WHAT WENT WRONG. At the eleventh attended sitting a label sweep over 47 labels
drove the author's account into rate limiting, and three download runs beside
it failed the same way. Nothing spaced the calls, nothing stopped the sweep
once the provider had said no, and nothing told the four drivers they were
spending one allowance. The account cleared about ten minutes after the last
caller stopped. That account must never be pushed into a block, so this module
is the safety seam, and every other provider concern sits above it.

THE SEAM IS THE TRANSPORT, NOT THE CLIENT. The provider's own library keeps a
``requests.Session`` on each client as ``request_session`` and every call it
makes, a search, a page of releases, a login, a token refresh, and the reads
the model objects make on their own, ends in that object's ``request`` method.
:meth:`Gate.attach` replaces that one method on the instance, so the gate sees
the raw status and the ``Retry-After`` header before the client turns them into
its own exception and before any caller above can swallow them. The product
builds a client at exactly two sites, the catalogue and account opener in
``acquire/provider_session.py`` and the vendored downloader's own session in
``acquire/vendored.py``, and both attach here; a test walks the package and
refuses a third.

FOUR PROPERTIES, EACH ONE OF THE THREE FAILURES ABOVE OR THE ONE THAT WOULD
FOLLOW FROM FIXING THEM ALONE:

* **Pacing.** A minimum interval between consecutive calls, measured from the
  last call ANY process made, read from and written to one state file under one
  lock. Conservative by default and set in ``[provider]`` of the configuration.
* **A breaker.** A rate limit answer that survives the retry ladder trips the
  gate: :data:`TRIP_AFTER` consecutive rate limit answers is what one spent
  ladder costs, and a ``Retry-After`` at or above the cooldown is the provider
  asking for the cooldown outright. A trip is raised as the job engine's own
  ``Parked``, so an item in flight goes back to pending and the driver claims
  nothing further, which is the one thing a breaker exists to guarantee.
* **A cooldown that outlives the process.** The trip is written to the state
  file with the time it lifts, and every opener asks :meth:`Gate.assert_open`
  before it logs in, so a verb started from another shell inside the window
  refuses with the reason and the time, and makes no call.
* **One driver at a time.** The lock is held for the whole of one call, the
  wait for the interval included, so two processes never have a request in
  flight together and a second driver waits its turn rather than doubling the
  rate. A wait the provider asked for through ``Retry-After`` is longer than an
  interval and is taken OUTSIDE the lock, so a second driver waits on the same
  ``not_before`` rather than on the holder. A wait for the lock past
  :data:`LOCK_WAIT_S` plus one interval means the holder is not making progress,
  and is refused as a park rather than hung on, because a lock nobody releases
  is a hang nobody diagnoses.

WHAT IT COUNTS. Every call and every rate limit answer, in the state file as
running totals across processes and in this module for this process, so a
verb can report what its own run spent. The count is written BEFORE the
request is sent: a crash mid request is still a call the account saw.

THE CALL CEILING (U193). Nothing above capped how many calls one command
made: a full label build spent 3,026 before the breaker parked it. The
dispatcher opens a :func:`command` scope around every verb, and :meth:`Gate.call`
asks, under the lock and before the send, whether this command has already made
``[provider] calls_per_command`` calls, or the higher ceiling ``--calls`` set
for this one run. If it has, the call is not made and the refusal is the same
park a trip raises, so an item in flight goes back to pending, what the run did
is kept, and the count at the stop is the ceiling exactly. It is a line per
command, never per day, so the next run starts fresh. Outside any scope nothing
is capped, which only a library caller or a test is, since every verb passes
the dispatcher. A job's detached child is a fresh process: a ceiling raised for
the run reaches it through :data:`CALLS_ENV`, set only while the scope is open.

WHAT IT DOES NOT COVER. The vendored downloader fetches media segments through
its own session against a content delivery host. Those are not calls to the
provider's API and are not paced here.
"""

from __future__ import annotations

import json
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

#: The two declared state entries. Installation scoped, because the allowance
#: belongs to the account and not to a library: two libraries swept on one
#: account share one limit, so one file beside the credential is the only
#: placement that can tell the truth.
STATE_KEY = "provider_gate"
LOCK_KEY = "provider_gate_lock"

#: Consecutive rate limit answers that trip the breaker. Six is one initial
#: attempt plus the five retries ``acquire.listing.fetch_with_retry`` makes, so
#: "survived the ladder" and "tripped" are the same count, and a test pins the
#: two together since this module cannot import that one.
TRIP_AFTER = 6

#: How long one call waits for the driver lock before refusing, on top of one
#: interval. A holder holds the lock for one request and at most one interval,
#: never for a ``Retry-After`` wait, so a wait this long past the interval means
#: the holder is not making progress.
LOCK_WAIT_S = 120.0

#: How often a waiting call asks for the lock again.
LOCK_POLL_S = 0.05

#: The provider's rate limit status.
RATE_LIMIT_STATUS = 429

#: The two reasons this module refuses with. Both declared in ``cause.REASONS``.
COOLDOWN = "provider-cooldown"
HELD = "provider-gate-held"

#: The reason a command that made as many calls as its ceiling allows stops
#: with (U193), declared in ``cause.REASONS``.
CEILING = "provider-call-ceiling"

#: How a ceiling raised for one run reaches a job's detached child, which is a
#: fresh process with a fresh scope. Written by :func:`command` while its scope
#: is open and restored when it closes, so the next run reads the configuration.
CALLS_ENV = "CRATEKIT_PROVIDER_CALLS"

#: This process's own spend, across every gate it built. The dispatcher reads
#: the difference over one verb and reports it as the run's, which is true of
#: this process alone: another process spending the same account writes the
#: shared file, and that is what the file's totals are for.
_PROCESS_CALLS = 0
_PROCESS_RATE_LIMITED = 0


@dataclass(frozen=True, slots=True)
class GateSettings:
    """The numbers the configuration owns, frozen with a job like the rest.

    The defaults are the configuration module's, READ WHEN A SETTINGS OBJECT
    IS BUILT rather than bound at import, on the rule ``tests/test_config.py``
    enforces for every module: a gate built with no settings and one built off
    the file then agree on the numbers, and neither holds a copy.
    """

    min_interval_s: float = field(
        default_factory=lambda: float(config.DEFAULT_PROVIDER_MIN_INTERVAL_S)
    )
    cooldown_s: float = field(default_factory=lambda: float(config.DEFAULT_PROVIDER_COOLDOWN_S))
    calls_per_command: int = field(
        default_factory=lambda: int(config.DEFAULT_PROVIDER_CALLS_PER_COMMAND)
    )

    @classmethod
    def from_config(cls, cfg: Any) -> GateSettings:
        """Read the ``[provider]`` section off a loaded configuration.

        Takes the config as a PARAMETER rather than loading it, on the rule the
        adapter settings state: a job runs against the configuration frozen
        when it was queued, and a constructor that loads one cannot be
        exercised against two policies in one process.
        """
        provider = cfg.provider
        return cls(
            min_interval_s=float(provider.min_interval_s),
            cooldown_s=float(provider.cooldown_s),
            calls_per_command=int(provider.calls_per_command),
        )


@dataclass(frozen=True, slots=True)
class Spend:
    """Calls made and rate limit answers received, as running totals."""

    calls: int = 0
    rate_limited: int = 0

    def since(self, earlier: Spend) -> Spend:
        """What was spent between ``earlier`` and this snapshot."""
        return Spend(
            calls=max(0, self.calls - earlier.calls),
            rate_limited=max(0, self.rate_limited - earlier.rate_limited),
        )


@dataclass
class _State:
    """The state file's contents. Epoch seconds throughout, because the file is
    read by every process on the machine and compared against a wall clock."""

    last_call: float = 0.0
    not_before: float = 0.0
    consecutive: int = 0
    tripped_at: float | None = None
    lifts_at: float | None = None
    calls: int = 0
    rate_limited: int = 0
    trips: int = 0

    def cooling(self, now: float) -> bool:
        return self.lifts_at is not None and now < self.lifts_at

    def to_json(self) -> dict[str, Any]:
        return {
            "last_call": self.last_call,
            "not_before": self.not_before,
            "consecutive": self.consecutive,
            "tripped_at": self.tripped_at,
            "lifts_at": self.lifts_at,
            "calls": self.calls,
            "rate_limited": self.rate_limited,
            "trips": self.trips,
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
        return state


@dataclass
class Command:
    """One command's ceiling scope, opened by the dispatcher around a verb.

    ``started`` is this process's call count when the command began, so the
    command's spend is a difference and a test process that made calls before
    it is not charged for them. ``raised`` is the ceiling ``--calls`` set for
    this run, or None for the configured one. ``stopped`` is the refusal the
    gate raised when the ceiling was reached, kept here because a verb that
    catches a park per item and returns normally would otherwise leave a clean
    report over a run the ceiling cut short, and the dispatcher reads it.
    """

    started: int
    raised: int | None = None
    stopped: Cause | None = None

    def spent(self) -> int:
        return max(0, _PROCESS_CALLS - self.started)


#: The open command scope, or None outside the dispatcher.
_COMMAND: Command | None = None


def _raised_from_env() -> int | None:
    """The ceiling a parent run raised, read off :data:`CALLS_ENV`.

    A value that is not a positive whole number is ignored, so the configured
    ceiling, the lower of the two, holds: only :func:`command` writes the
    variable, and a hand written one that cannot be read must not lift the
    line it was meant to move.
    """
    text = os.environ.get(CALLS_ENV, "").strip()
    if not (text.isascii() and text.isdigit()):
        return None
    value = int(text)
    return value if value > 0 else None


@contextmanager
def command(calls: int | None = None) -> Iterator[Command]:
    """Open one command's ceiling scope for the length of a verb.

    ``calls`` is the ceiling raised for this run alone. A scope opened inside
    an open one, which ``run decide --continue`` does when it dispatches the
    verb again in the same process, yields the OUTER scope unchanged, so one
    command cannot spend its ceiling twice by nesting.
    """
    global _COMMAND
    if _COMMAND is not None:
        yield _COMMAND
        return
    raised = calls if calls is not None else _raised_from_env()
    previous = os.environ.get(CALLS_ENV)
    if calls is not None:
        os.environ[CALLS_ENV] = str(calls)
    scope = Command(started=_PROCESS_CALLS, raised=raised)
    _COMMAND = scope
    try:
        yield scope
    finally:
        _COMMAND = None
        if calls is not None:
            if previous is None:
                os.environ.pop(CALLS_ENV, None)
            else:
                os.environ[CALLS_ENV] = previous


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


# ---------------------------------------------------------------------------
# Retry-After, parsed in ONE place
# ---------------------------------------------------------------------------


def header_value(headers: object, name: str) -> object | None:
    """Read one header without assuming the container preserves case.

    ``requests`` returns a case-insensitive mapping and a hand-rolled client
    returns a plain dictionary, so a single ``headers[name]`` works against one
    of them and silently returns nothing against the other. Silently returning
    nothing here means falling back to our own backoff and ignoring a wait the
    provider explicitly asked for.
    """
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
    """Coerce a retry hint to seconds from ``now``, accepting both header forms.

    HTTP permits ``Retry-After`` as delta-seconds OR as a date, and the date form
    is parsed rather than dropped. Dropping it would fall back to our own
    backoff, which is capped, so a provider asking for an hour would be asked
    again in minutes. That is the retry-into-a-ban failure arriving through a
    parsing shortcut. THE ONE PARSER of this header in the tree: the download
    pacing reads the same hint off an exception and delegates here, so the two
    cannot disagree about what a wait says.
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
    """The response's ``Retry-After`` as seconds, or zero when it carries none
    that can be read. Zero rather than a guess, because the count of
    consecutive answers still trips the breaker without it."""
    seconds = retry_after_seconds(
        header_value(getattr(response, "headers", None), "Retry-After"), now
    )
    return seconds or 0.0


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------


class Gate:
    """The pacing gate over one provider account, shared across processes.

    ``clock`` and ``sleep`` are injectable so a suite drives every schedule
    without waiting it out; the two process tests use the real ones, because a
    lock the kernel holds cannot be faked.
    """

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
        #: This gate's own spend, for a test or a report that holds the gate.
        self.calls = 0
        self.rate_limited = 0
        #: The last park this gate raised and nothing has cleared since. The
        #: vendored downloader catches every exception inside its login and
        #: its download and answers "no" over them, so the adapter asks
        #: :meth:`raise_if_parked` after the tool returns and the park it
        #: swallowed comes out as itself.
        self._last_park: CratekitError | None = None

    # ── the state file ────────────────────────────────────────────────────

    def _read(self) -> _State:
        """A state file that cannot be read counts as fresh rather than
        refusing, because a corrupt counter must not lock the provider out.
        A trip that was lost this way costs one more ladder, not an account."""
        try:
            return _State.from_json(json.loads(self.path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            return _State()

    def _write(self, state: _State) -> None:
        config._mkdir_private(self.path.parent)
        payload = json.dumps(state.to_json(), indent=2, sort_keys=True) + "\n"
        config.atomic_write_bytes(payload.encode("utf-8"), self.path)

    def spend(self) -> Spend:
        """The running totals across every process, off the state file."""
        state = self._read()
        return Spend(calls=state.calls, rate_limited=state.rate_limited)

    # ── the lock ──────────────────────────────────────────────────────────

    @contextmanager
    def _held(self) -> Iterator[None]:
        """Hold the one call at a time lock, or refuse naming the wait.

        Polled with ``LOCK_NB`` rather than taken blocking, so the wait has an
        end this module chose and a test can drive it with a fake clock. THE
        FILE IS NEVER UNLINKED, for the reason the job driver lock gives: one
        holder unlinking the name while another creates a fresh file at it is
        how two processes each hold "the" lock.
        """
        config._mkdir_private(self.lock_path.parent)
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
        """A lock held past the wait is a fact about the ACCOUNT, not about
        the item in flight, so it is parked like a trip: the item goes back to
        pending and the driver claims nothing further, where a retryable
        refusal would send every remaining item into the same wait."""
        return Cause(
            reason=HELD,
            message=(
                f"another driver has held the streaming provider for "
                f"{waited:.0f} seconds without finishing a call; one call at a "
                f"time per account, so this run stopped without making one and "
                f"the remaining items stay queued"
            ),
            remediation=Remediation(remedy=Remedy.WAIT_FOR_HOLDER),
            scope=Scope.RUN,
            retryable=False,
            origin=("provider_gate",),
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
        return Cause(
            reason=COOLDOWN,
            message=(
                f"{opening}; every provider call is refused until {_iso(lifts)}, "
                f"{remaining} seconds from now, and the remaining items stay queued"
            ),
            remediation=Remediation(
                remedy=Remedy.RETRY_LATER,
                steps=(
                    f"wait until {_iso(lifts)}",
                    "then resume the job, or run the verb again",
                ),
            ),
            scope=Scope.RUN,
            retryable=False,
            origin=("provider_gate",),
            detail={
                "tripped_at": _iso(float(state.tripped_at or now)),
                "lifts_at": _iso(lifts),
                "remaining_s": remaining,
                "cooldown_s": self.settings.cooldown_s,
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
        higher = line * 2
        return Cause(
            reason=CEILING,
            message=(
                f"this command made {spent} {'call' if spent == 1 else 'calls'} to the "
                f"streaming provider, "
                f"{where}, so it stopped before the next one; what it did is kept "
                f"and the remaining items stay queued"
            ),
            remediation=Remediation(
                remedy=Remedy.FIX_COMMAND_LINE,
                steps=(
                    f"continue with a higher ceiling for one run: put --calls {higher} "
                    f"before the command and run it again",
                    "or raise [provider] calls_per_command in the configuration for every run",
                ),
            ),
            scope=Scope.RUN,
            retryable=False,
            origin=("provider_gate",),
            detail={
                "calls": spent,
                "ceiling": line,
                "raised": scope.raised is not None,
                "higher": higher,
            },
        )

    def _stopped(self, cause: Cause) -> CratekitError:
        """A refusal as the job engine's own park, so an item in flight is
        released rather than failed and the driver claims nothing further.

        Imported here rather than at the top because the engine imports the
        CLI package for its envelope and this module is imported by the
        adapters the CLI loads, which is a cycle at module scope.
        """
        from cratekit.core.jobs import Parked  # noqa: PLC0415 - see docstring

        parked = Parked(cause)
        self._last_park = parked
        return parked

    # ── the public surface ────────────────────────────────────────────────

    def assert_open(self) -> None:
        """Refuse, naming the lift time, when a trip is still cooling.

        Asked by every opener BEFORE it builds a client and logs in, so a verb
        started inside the window makes no call at all. Reads the shared file,
        so a trip another process wrote is refused here too.
        """
        state = self._read()
        now = self._clock()
        if state.cooling(now):
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

    def raise_if_parked(self) -> None:
        """Re-raise a park this gate raised that a caller swallowed, then ask
        the file.

        For the vendored downloader, which catches every exception inside its
        login and its download and answers "no" over them: a trip or a held
        lock the gate raised mid call would otherwise read as a rejected
        session or as no file came back, and the run would go on to the next
        item. The file is asked as well, so a trip another process wrote while
        the tool ran is refused here too.
        """
        if self._last_park is not None:
            raise self._last_park
        self.assert_open()

    def call(self, send: Callable[[], Any]) -> Any:
        """Make one provider call under the lock, paced, counted and watched.

        ``send`` returns the transport's response; the status is read off it.
        An exception out of ``send`` is the caller's to classify and is not a
        rate limit answer, so it neither counts as one nor breaks a run of them.

        A wait longer than one interval, which only a ``Retry-After`` produces,
        is taken with the lock RELEASED and the call asked for again after it:
        every driver reads the same ``not_before`` off the file and waits on it,
        rather than on the one holder, so the lock is never held for longer
        than one request and one interval, which is what the lock wait limit
        stands on.
        """
        while True:
            with self._held():
                state = self._read()
                now = self._clock()
                if state.cooling(now):
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))
                scope = _COMMAND
                if scope is not None:
                    line = ceiling(self.settings)
                    if scope.spent() >= line:
                        # BEFORE THE SEND, so the count at the stop is the
                        # ceiling exactly and the call that would pass it is
                        # never made.
                        cause = self._ceiling_cause(scope, line)
                        scope.stopped = cause
                        raise self._stopped(cause)
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)
                if due - now > self.settings.min_interval_s:
                    long_wait = due - now
                else:
                    return self._send_now(send, state, now, due)
            self._sleep(long_wait)

    def _send_now(self, send: Callable[[], Any], state: _State, now: float, due: float) -> Any:
        """The call itself, under the lock, with at most one interval's wait."""
        global _PROCESS_CALLS, _PROCESS_RATE_LIMITED
        if due > now:
            self._sleep(due - now)
            now = max(self._clock(), due)
        state.last_call = now
        state.calls += 1
        self.calls += 1
        _PROCESS_CALLS += 1
        self._write(state)

        response = send()

        if getattr(response, "status_code", None) == RATE_LIMIT_STATUS:
            now = self._clock()
            self.rate_limited += 1
            _PROCESS_RATE_LIMITED += 1
            state.rate_limited += 1
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

    def attach(self, client: Any) -> bool:
        """Route every request the client's transport makes through this gate.

        The transport is the ``requests.Session`` the provider's library keeps as
        ``request_session``; its ``request`` method is replaced ON THE INSTANCE,
        so ``get`` and ``post`` and the library's own helper all land here.
        Idempotent: attaching twice wraps the original once, so the vendored
        tool, which is a singleton and is built once per process, is not paced
        twice. Returns False for a client with no such transport, which is what
        a method level fake in the suite is; the two build sites in the product
        always hand over a real one, and a test walks the package for a third.
        """
        transport = getattr(client, "request_session", None)
        if transport is None or not callable(getattr(transport, "request", None)):
            return False
        original = getattr(transport, "_cratekit_unpaced_request", None) or transport.request

        def gated(method: Any, url: Any, *args: Any, **kwargs: Any) -> Any:
            return self.call(lambda: original(method, url, *args, **kwargs))

        transport._cratekit_unpaced_request = original
        transport._cratekit_gate = self
        transport.request = gated
        return True


def spend(path: Path | None = None) -> Spend:
    """The running totals off the state file, for a report that holds no gate."""
    return Gate(path=path).spend()


def process_spend() -> Spend:
    """What THIS process has spent, across every gate it built."""
    return Spend(calls=_PROCESS_CALLS, rate_limited=_PROCESS_RATE_LIMITED)


__all__ = [
    "CALLS_ENV",
    "CEILING",
    "COOLDOWN",
    "HELD",
    "LOCK_KEY",
    "LOCK_POLL_S",
    "LOCK_WAIT_S",
    "RATE_LIMIT_STATUS",
    "STATE_KEY",
    "TRIP_AFTER",
    "Command",
    "Gate",
    "GateSettings",
    "Spend",
    "ceiling",
    "command",
    "command_spent",
    "header_value",
    "process_spend",
    "retry_after_seconds",
    "spend",
]
