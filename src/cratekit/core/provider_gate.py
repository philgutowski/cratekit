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
builds a client of that library at exactly two sites, the catalogue and
account opener in ``acquire/provider_session.py`` and the vendored
downloader's own session in ``acquire/vendored.py``, and both attach here; a
test walks the package and refuses a third. The app credentials' catalogue
client (U205) keeps its transport under the same name, is built beside the
account opener and nowhere else, and attaches here the same way.

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

TWO IDENTITIES, ONE ALLOWANCE (U205). A call is made either under the
person's account session or under Cratekit's own app credentials, which the
catalogue client ``acquire.catalogue_api`` holds, and :meth:`Gate.attach`
names which when it wraps a client's transport. Every property above covers
both unchanged: one interval, one breaker, one cooldown, one ceiling. What
differs is the count. The state file keeps each identity's calls and rate
limit answers under ``identities`` beside the totals, and a file written
before U205, which has no such entry, loads with every call it counted on the
account, since until then every call was the account's. A version before U205
that rewrites the file keeps the totals and drops the entry, so the history it
held is read as the account's again; the totals stay true either way.

ONE ALLOWANCE PER ACCOUNT, AND A RESERVE (U278). On 2026-11-12 a disposable
copy whose installation state was redirected to scratch got a gate of its own:
fifty three small commands on it, each under its own ceiling, spent about
7,800 catalogue calls in twenty minutes, and the live breaker, which had seen
none of them, then refused the label go they had cost. Three things answer it.
The state file and its lock resolve under ``config.provider_gate_dir``, which
a redirected ``CRATEKIT_STATE_DIR`` does not move, so every installation state
pointed at the account reads one gate. Every call is counted in that file for
the minute it falls in, per identity, and a call that would take an
identity's last sixty minutes past its line is not sent: it parks as
:data:`BUDGET`, naming the spend, the line and the minute it frees, which no
number of separate commands can step around. And the line depends on the
command: one whose verb writes the account or downloads may spend the whole
of ``[provider] calls_per_hour``, and any other stops ``reserve_share`` of it
short, so a day of reads cannot use up what a go needs. ``--calls`` never
reaches past the line its command may spend to; one that asks to is refused
before a call is made. The window is checked before the ceiling, since a
continue with a higher ceiling cannot help a run the hour has stopped, and
after the cooldown, which keeps its own meaning: the budget never trips the
breaker, and a refusal of either is a park and never a retry.

WHAT IT DOES NOT COVER. The vendored downloader fetches media segments through
its own session against a content delivery host. Those are not calls to the
provider's API and are not paced here.
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

#: The reason a call past its identity's line for the hour stops with, and the
#: reason a ``--calls`` past that line is refused with (U278), declared in
#: ``cause.REASONS``.
BUDGET = "provider-budget"

#: How an hour's budget raised for one run reaches a job's detached child, on
#: :data:`CALLS_ENV`'s rule.
BUDGET_ENV = "CRATEKIT_PROVIDER_CALLS_PER_HOUR"

#: The window the budget is counted over, and the size of one count in it. A
#: minute's calls leave the window an hour after the minute ENDS, so the count
#: can only hold a call for longer than an hour, never for less.
WINDOW_S = 3600
BUCKET_S = 60

#: The two identities a call is made under (U205): the person's account
#: session, and Cratekit's own app credentials, which only the catalogue
#: client holds.
ACCOUNT = "account"
APP = "app"
IDENTITIES = (ACCOUNT, APP)

#: This process's own spend, across every gate it built. The dispatcher reads
#: the difference over one verb and reports it as the run's, which is true of
#: this process alone: another process spending the same account writes the
#: shared file, and that is what the file's totals are for.
_PROCESS_CALLS = 0
_PROCESS_RATE_LIMITED = 0
#: The share of the two above made under the app credentials (U205). The
#: account's share is the difference, so the totals the ceiling reads stay
#: the one count they were.
_PROCESS_APP_CALLS = 0
_PROCESS_APP_RATE_LIMITED = 0

#: The app values this process found recorded in the installation's index and
#: missing from the keychain, so its catalogue lookups went to the account
#: (U205's review, round two). Read by the dispatcher's spend line, so a run
#: that fell back says why none of its calls went under the app; cleared when
#: a command's scope opens, so one verb's finding is not the next one's.
_APP_LOST: list[str] = []


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
    calls_per_hour: int = field(
        default_factory=lambda: int(config.DEFAULT_PROVIDER_CALLS_PER_HOUR)
    )
    reserve_share: float = field(
        default_factory=lambda: float(config.DEFAULT_PROVIDER_RESERVE_SHARE)
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
            calls_per_hour=int(provider.calls_per_hour),
            reserve_share=float(provider.reserve_share),
        )


@dataclass(frozen=True, slots=True)
class Spend:
    """Calls made and rate limit answers received, as running totals.

    ``calls`` and ``rate_limited`` are every identity's together, and the
    ``app_`` pair is the share made under the app credentials (U205), so the
    account's share is the difference and the two can never sum to more than
    the totals.
    """

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
    #: The share of ``calls`` and ``rate_limited`` the app credentials made.
    app_calls: int = 0
    app_rate_limited: int = 0
    #: Each identity's calls by the minute they were made in, the minutes the
    #: window no longer holds pruned on every write (U278).
    window: dict[str, dict[int, int]] = field(
        default_factory=lambda: {identity: {} for identity in IDENTITIES}
    )

    def cooling(self, now: float) -> bool:
        return self.lifts_at is not None and now < self.lifts_at

    def spent(self, identity: str, now: float) -> int:
        """The identity's calls in the window at ``now``."""
        return sum(_live(self.window.get(identity, {}), now).values())

    def count(self, identity: str, now: float) -> None:
        """One more call by ``identity`` at ``now``, and the window pruned."""
        minutes = _live(self.window.get(identity, {}), now)
        bucket = _bucket(now)
        minutes[bucket] = minutes.get(bucket, 0) + 1
        self.window[identity] = minutes

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
        # NO ``identities`` IS A FILE WRITTEN BEFORE U205, every call in it the
        # account's, so the app's share is nothing. A share above the total it
        # is a share of is clamped to it, since the totals are what the ceiling
        # and every report before this unit read.
        identities = data.get("identities")
        app = identities.get(APP) if isinstance(identities, dict) else None
        if isinstance(app, dict):
            state.app_calls = min(_as_int(app.get("calls")), state.calls)
            state.app_rate_limited = min(_as_int(app.get("rate_limited")), state.rate_limited)
        # NO ``window`` IS A FILE WRITTEN BEFORE U278, read as nothing spent in
        # the hour: the window starts counting at the first call this build makes.
        state.window = _window_from_json(data.get("window"))
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
    #: Whether this command may spend the hour's reserve (U278): set by the
    #: dispatcher from the verb's declared writes, and only ever narrowed by
    #: :func:`reading` for a mode that only reads.
    reserve: bool = False
    #: The hour's budget raised for this run, or None for the configured one.
    hourly: int | None = None
    #: The class the dispatcher opened the scope with, which :func:`spending`
    #: returns to and never goes past.
    declared: bool = False

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


def _hour_from_env() -> int | None:
    """The hour's budget a parent run raised, read off :data:`BUDGET_ENV`, on
    :func:`_raised_from_env`'s rule: a value that cannot be read is ignored,
    so the configured budget holds."""
    text = os.environ.get(BUDGET_ENV, "").strip()
    if not (text.isascii() and text.isdigit()):
        return None
    value = int(text)
    return value if value > 0 else None


@contextmanager
def _exported(name: str, value: int | None) -> Iterator[None]:
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

    ``calls`` is the ceiling raised for this run alone, and ``calls_per_hour``
    the hour's budget raised for it (U278); both reach a detached child through
    the environment while the scope is open. ``reserve`` says whether the
    command may spend the hour's reserve, which the dispatcher reads off the
    verb's declared writes. A scope opened inside an open one, which ``run
    decide --continue`` does when it dispatches the verb again in the same
    process, yields the OUTER scope unchanged, so one command cannot spend its
    ceiling twice by nesting, nor widen its class.
    """
    global _COMMAND
    if _COMMAND is not None:
        yield _COMMAND
        return
    raised = calls if calls is not None else _raised_from_env()
    hourly_raised = calls_per_hour if calls_per_hour is not None else _hour_from_env()
    _APP_LOST.clear()
    scope = Command(
        started=_PROCESS_CALLS,
        raised=raised,
        reserve=bool(reserve),
        hourly=hourly_raised,
        declared=bool(reserve),
    )
    with _exported(CALLS_ENV, calls), _exported(BUDGET_ENV, calls_per_hour):
        _COMMAND = scope
        try:
            yield scope
        finally:
            _COMMAND = None


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


# ---------------------------------------------------------------------------
# The hour's budget (U278)
# ---------------------------------------------------------------------------


def _bucket(epoch: float) -> int:
    """The minute a call falls in, as the epoch second it starts at."""
    return int(epoch // BUCKET_S) * BUCKET_S


def _expires(bucket: int) -> float:
    """When a minute's calls leave the window: an hour after the minute ENDS.

    Every call in the minute is read as made at its last second, so the
    window can only count a call for longer than an hour, never for less, and
    a line read off it is never crossed by a call the window forgot early.
    """
    return float(bucket + BUCKET_S + WINDOW_S)


def _live(window: Mapping[int, int], now: float) -> dict[int, int]:
    """The minutes still inside the window at ``now``. A minute stamped in the
    future, which only a clock set back writes, is kept and counted: dropping
    it would hand the account a fresh hour for as long as the clock is wrong."""
    return {bucket: n for bucket, n in window.items() if _expires(bucket) > now and n > 0}


def _frees_at(window: Mapping[int, int], now: float, line: int) -> float:
    """The first moment the window holds fewer calls than ``line``.

    ``now`` when it already does. Otherwise the oldest minutes age out one by
    one until enough have gone; a line of zero never frees, and is answered
    with the moment the last minute leaves, since nothing sooner is true.
    """
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
    dropped rather than refused, on the rule the module keeps for its whole
    file: a corrupt counter must not lock the provider out, and the breaker
    still stands behind it."""
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
    """The calls of ``budget`` kept for writes and downloads, rounded UP, so a
    share never keeps less than it says."""
    return min(budget, max(0, math.ceil(round(budget * share, 6))))


def line_for(settings: GateSettings | None = None, *, reserve: bool | None = None) -> int:
    """How many calls an identity may have in the window before the next is refused.

    The whole budget for a command that spends the reserve, the budget less the
    reserve for any other. ``reserve`` None asks the open command; outside a
    scope a call is held to the read line, the stricter of the two, since only
    a library caller or a test makes one there.
    """
    settings = settings or GateSettings()
    budget = hourly(settings)
    if reserve is None:
        scope = _COMMAND
        reserve = scope.reserve if scope is not None else False
    if reserve:
        return budget
    return budget - reserve_of(budget, settings.reserve_share)


@contextmanager
def spending() -> Iterator[None]:
    """Let the body spend the reserve, if the verb declared it may (U278).

    For the one part of a read mode that is a go: ``label sync``'s walk ends
    at the go's gate, and a download behind it is what the reserve is kept
    for. Never past the class the dispatcher opened the command with, so a
    verb that declares no write cannot reach the reserve through it, and
    narrowed again on the way out.
    """
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
    """Hold the open command to the read line from here on (U278).

    For a verb that writes the account or downloads in one mode and only reads
    in another: ``label sync`` spends the reserve under ``--go`` alone. It only
    ever narrows: a read scope stays a read scope. Given ``settings``, a ceiling
    ``--calls`` raised past the read line is refused at once, before the verb
    makes a call, rather than at the first one.
    """
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


def over_the_line(settings: GateSettings | None = None) -> Cause | None:
    """The refusal for a ``--calls`` raised past the line this command may
    reach, or None. Never a silent cap: a ceiling the hour cannot hold is a
    command line that says one thing and runs another."""
    scope = _COMMAND
    if scope is None or scope.raised is None:
        return None
    settings = settings or GateSettings()
    line = line_for(settings)
    if scope.raised <= line:
        return None
    budget = hourly(settings)
    return Cause(
        reason=BUDGET,
        message=(
            f"--calls {scope.raised} asks for more calls than this command may make in "
            f"an hour: {_class_words(scope.reserve, budget, line)}, so nothing was asked "
            f"of the streaming provider"
        ),
        remediation=Remediation(
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(
                f"run it again with --calls {line} or lower",
                "or raise the hour's budget for one run with --calls-per-hour, or "
                "[provider] calls_per_hour for every run",
            ),
        ),
        scope=Scope.RUN,
        retryable=False,
        origin=("provider_gate",),
        detail={"raised": scope.raised, "line": line, "budget": budget, "reserve": scope.reserve},
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

    def window_spend(self, identity: str = ACCOUNT) -> int:
        """The identity's calls in the last hour, off the state file (U278)."""
        return self._read().spent(identity, self._clock())

    def spend(self) -> Spend:
        """The running totals across every process, off the state file."""
        state = self._read()
        return Spend(
            calls=state.calls,
            rate_limited=state.rate_limited,
            app_calls=state.app_calls,
            app_rate_limited=state.app_rate_limited,
        )

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
        # NEVER A CONTINUE THE HOUR WOULD REFUSE (U278). Doubled as before, but
        # held to the line this command may spend to, since a ``--calls`` past
        # it is refused before a call; at that line already, doubled anyway,
        # and the refusal it meets names --calls-per-hour.
        reach = line_for(self.settings)
        higher = min(line * 2, reach) if reach > line else line * 2
        # NEVER "WHAT IT DID IS KEPT" (U217). Said by every command, it was
        # false for each that read and did not keep, and a label listing paid
        # its whole cost again on every continue under those words. What a
        # command keeps is said by the command.
        return Cause(
            reason=CEILING,
            message=(
                f"this command made {spent} {'call' if spent == 1 else 'calls'} to the "
                f"streaming provider, "
                f"{where}, so it stopped before the next one and the remaining items "
                f"stay queued; what it read and did not keep is read again when it "
                f"continues"
            ),
            remediation=Remediation(
                remedy=Remedy.FIX_COMMAND_LINE,
                steps=(
                    # THE STORED FORM, read off ``job show`` when a detached
                    # child stopped: it names both shapes, since a job is
                    # continued by its id and never by queueing it again. The
                    # dispatcher replaces it with the one exact command.
                    f"continue with a higher ceiling for one run: a parked job with "
                    f"crate --calls {higher} job resume JOB_ID, any other command by "
                    f"running it again with --calls {higher} before it",
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

    def _budget_cause(
        self, state: _State, identity: str, now: float, line: int, spent: int
    ) -> Cause:
        """The hour's line reached for one identity (U278): a fact about the
        ACCOUNT, parked like a trip, so an item in flight goes back to pending,
        and never retryable, since asking again inside the hour is the harm."""
        scope = _COMMAND
        reserve = scope.reserve if scope is not None else False
        budget = hourly(self.settings)
        frees = _frees_at(state.window.get(identity, {}), now, line)
        who = _who(identity)
        calls = "call" if spent == 1 else "calls"
        return Cause(
            reason=BUDGET,
            message=(
                f"{who} has made {spent} {calls} to the streaming provider in the last "
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
            scope=Scope.RUN,
            retryable=False,
            origin=("provider_gate",),
            detail={
                "identity": identity,
                "spent": spent,
                "line": line,
                "budget": budget,
                "reserve": reserve,
                "frees_at": _iso(frees),
                "window_s": WINDOW_S,
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

    def call(self, send: Callable[[], Any], *, identity: str = ACCOUNT) -> Any:
        """Make one provider call under the lock, paced, counted and watched.

        ``send`` returns the transport's response; the status is read off it.
        ``identity`` is whose call it is, counted under that identity as well as
        in the totals; the interval, the breaker and the ceiling read the totals.
        An exception out of ``send`` is the caller's to classify and is not a
        rate limit answer, so it neither counts as one nor breaks a run of them.

        A wait longer than one interval, which only a ``Retry-After`` produces,
        is taken with the lock RELEASED and the call asked for again after it:
        every driver reads the same ``not_before`` off the file and waits on it,
        rather than on the one holder, so the lock is never held for longer
        than one request and one interval, which is what the lock wait limit
        stands on.
        """
        if identity not in IDENTITIES:
            # Asked here as well as at ``attach``, so a caller that names an
            # identity to the call directly cannot count calls nobody sees.
            raise ValueError(f"no provider identity is named {identity!r}")
        while True:
            with self._held():
                state = self._read()
                now = self._clock()
                if state.cooling(now):
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))
                scope = _COMMAND
                # THE HOUR, BEFORE THE CEILING (U278), and both before the send.
                # A ``--calls`` past what this command may reach is refused
                # outright, and a window at its line stops the call whoever
                # spent it, so no number of commands or copies steps around it.
                over = over_the_line(self.settings)
                if over is not None:
                    if scope is not None:
                        scope.stopped = over
                    raise self._stopped(over)
                hour_line = line_for(self.settings)
                spent = state.spent(identity, now)
                if spent >= hour_line:
                    cause = self._budget_cause(state, identity, now, hour_line, spent)
                    if scope is not None:
                        scope.stopped = cause
                    raise self._stopped(cause)
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
        """Route every request the client's transport makes through this gate.

        ``identity`` names whose calls they are, :data:`ACCOUNT` for the
        provider library's clients and :data:`APP` for the catalogue client
        (U205). Any other name is refused before anything is wrapped, since a
        call counted under a name the reports do not know is a call nobody sees.

        The transport is the ``requests.Session`` the provider's library keeps as
        ``request_session``; its ``request`` method is replaced ON THE INSTANCE,
        so ``get`` and ``post`` and the library's own helper all land here.
        Idempotent: attaching twice wraps the original once, so the vendored
        tool, which is a singleton and is built once per process, is not paced
        twice. Returns False for a client with no such transport, which is what
        a method level fake in the suite is; the two build sites in the product
        always hand over a real one, and a test walks the package for a third.
        """
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
        calls=_PROCESS_CALLS,
        rate_limited=_PROCESS_RATE_LIMITED,
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


def read_spend(path: Path | None = None) -> Spend | None:
    """The running totals off the state file, or None when it cannot be read.

    FOR A REPORT, NOT FOR THE GATE. The gate reads a file it cannot parse as
    fresh, because a corrupt counter must not lock the provider out; a report
    that did the same would show zero calls over a file it never read, so this
    answers None and the report says so. A file that does not exist yet is an
    installation that has made no call, and is answered as nothing spent.
    """
    target = path if path is not None else config.state_path(STATE_KEY)
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return Spend()
    except OSError:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None
    state = _State.from_json(data)
    return Spend(
        calls=state.calls,
        rate_limited=state.rate_limited,
        app_calls=state.app_calls,
        app_rate_limited=state.app_rate_limited,
    )


@dataclass(frozen=True, slots=True)
class Standing:
    """Where the account stands in the hour, off the one gate, for a report (U278).

    ``window`` is each identity's calls by minute as the file holds them, and
    ``now`` the moment the report reads them at, so every figure below is one
    reading and not several.
    """

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
    """The hour's spend and any cooldown off the one gate, or None when its file
    cannot be read, on :func:`read_spend`'s rule: the gate reads such a file as
    fresh, and a report that did would show an open hour over a file it never
    read. A file that does not exist yet is an hour with nothing spent."""
    target = path if path is not None else config.state_path(STATE_KEY)
    moment = time.time() if now is None else now
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return Standing(window={}, now=moment, path=target)
    except OSError:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None
    state = _State.from_json(data)
    return Standing(
        window=state.window,
        now=moment,
        path=target,
        tripped_at=state.tripped_at,
        lifts_at=state.lifts_at,
    )


__all__ = [
    "ACCOUNT",
    "APP",
    "BUCKET_S",
    "BUDGET",
    "BUDGET_ENV",
    "CALLS_ENV",
    "CEILING",
    "COOLDOWN",
    "HELD",
    "IDENTITIES",
    "LOCK_KEY",
    "LOCK_POLL_S",
    "LOCK_WAIT_S",
    "RATE_LIMIT_STATUS",
    "STATE_KEY",
    "app_lost",
    "TRIP_AFTER",
    "Command",
    "Gate",
    "GateSettings",
    "Spend",
    "Standing",
    "WINDOW_S",
    "ceiling",
    "command",
    "command_spent",
    "header_value",
    "hourly",
    "iso",
    "line_for",
    "note_app_lost",
    "over_the_line",
    "process_spend",
    "read_spend",
    "read_standing",
    "reading",
    "spending",
    "reserve_of",
    "retry_after_seconds",
    "spend",
]
