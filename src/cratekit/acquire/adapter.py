"""The acquisition contract: what an adapter promises, as types rather than luck.

WHY THIS EXISTS. The vendored downloader's upstream was deleted. When a provider
change breaks it, the only recovery is a different tool, and a different tool is
only substitutable if both are reachable through one declared contract (R9). The
contract is the product's insurance policy, so it is written first and both
adapters are written against it.

WHAT THE CONTRACT IS. Two answers, at two scales:

* Per requested track, exactly one of ACQUIRED, UNAVAILABLE_PERMANENT,
  UNAVAILABLE_TRANSIENT, REFUSED_BY_POLICY.
* Per invocation, exactly one of OK, AUTH_FAILED, ADAPTER_BROKEN.

Today neither distinction can be made. Both call sites in the source system raise
on any non-zero exit, and the tool exits zero when it silently skips a track. So
"nothing was new" and "authentication is dead" arrive identically, and AE9 cannot
be met at all: the user is told tracks are missing when what is actually missing
is their session.

WHY THE TYPES REFUSE TO BE IGNORED. A result object whose fields a caller may
quietly not read is a comment with a runtime cost. Three mechanisms make these
bite instead:

1. ``TrackResult`` validates its own combinations. An ACQUIRED result with no
   path cannot be constructed, and neither can a lossy acquisition that does not
   require the marker. R21's "no configuration in which a lossy file goes
   unmarked" is therefore a property of the type, not of a policy branch that
   somebody could add an else to.
2. ``InvocationResult`` refuses to carry a permanent unavailability when the
   invocation itself failed. Quarantine is fed from permanent results, and
   quarantine means never re-queued, so a broken adapter that could poison it is
   a bug that must be unrepresentable rather than merely unlikely.
3. ``dispatch`` derives the set of outcomes a caller must handle from the enum at
   run time. Adding a fifth outcome breaks every caller loudly at the point they
   would otherwise have silently dropped it.

WHAT IS PURE HERE AND WHY. The classifier, the policy decision, the settings
translation, and the result types touch no network, no subprocess, and no disk.
That is what lets both adapters be proven against the same suite on a machine
with no account, no credentials, and no alternative tool installed.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import AbstractContextManager, nullcontext
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol, runtime_checkable

from cratekit.core.cause import answered_not_found
from cratekit.core.provider_gate import GateSettings

# ---------------------------------------------------------------------------
# Remediation vocabulary
# ---------------------------------------------------------------------------


class Remedy(StrEnum):
    """What to do about an acquisition failure, as a TOKEN rather than a command.

    D2: remediation below the CLI is a structured token; only the CLI renders one
    into the text a user types, because the text depends on the platform, the
    package manager they actually have, and the interface they are sitting in
    front of. This module knows none of those.

    U5 owns the product-wide vocabulary and reserves a code and a remediation for
    every refusal in the system (S4). These are this unit's contribution to that
    reservation, in the same shape ``core/config.py`` and ``core/secrets.py``
    already use, not a competing scheme.
    """

    #: The session is dead. Re-authorise the SAME adapter.
    REAUTHENTICATE_PROVIDER = "reauthenticate-provider"
    #: The adapter itself cannot run. Point configuration at one that can (AE9).
    SWITCH_ADAPTER = "switch-adapter"
    #: The chosen adapter's third-party tool is not installed on this machine.
    INSTALL_ADAPTER = "install-adapter"
    #: ``acquisition.adapter`` names something no registry entry matches.
    CHOOSE_KNOWN_ADAPTER = "choose-known-adapter"
    #: Strict lossless policy refused a track that only exists lossy (R21, AE4).
    RELAX_LOSSLESS_POLICY = "relax-lossless-policy"
    #: There is no keychain to read the provider session from. Re-authorising is
    #: useless here: there is nowhere to put the answer.
    REPAIR_CREDENTIAL_STORE = "repair-credential-store"
    #: A transient provider failure. The track stays re-queueable; nothing to fix.
    RETRY_LATER = "retry-later"
    #: The tool's own settings did not take the values the adapter pushed in.
    REPAIR_ADAPTER_SETTINGS = "repair-adapter-settings"
    #: The provider refused this CLIENT rather than this request: a forbidden
    #: response or a bot challenge. Distinct from ``RETRY_LATER`` because the two
    #: instructions are opposites at the only moment either is read. Retrying a
    #: throttle is correct; retrying a block is what turns it into a lockout.
    PAUSE_AND_CHECK_ACCOUNT = "pause-and-check-account"
    #: The failure is a defect in this program, not in the provider or the
    #: machine. Retrying repeats it forever, so the only act is a report.
    REPORT_DEFECT = "report-defect"


class AdapterError(Exception):
    """Base for acquisition failures. Always carries a structured remedy token."""

    remedy: Remedy = Remedy.SWITCH_ADAPTER

    def __init__(self, message: str, *, remedy: Remedy | None = None) -> None:
        super().__init__(message)
        if remedy is not None:
            self.remedy = remedy


class UnknownAdapter(AdapterError):
    """Configuration names an adapter no registry entry matches."""

    remedy = Remedy.CHOOSE_KNOWN_ADAPTER


class AdapterAuthFailed(AdapterError):
    """The provider rejected the session. NOT a missing track (AE9)."""

    remedy = Remedy.REAUTHENTICATE_PROVIDER


class AdapterBroken(AdapterError):
    """The adapter cannot run at all: absent tool, failed import, bad settings."""

    remedy = Remedy.SWITCH_ADAPTER


class LosslessRefused(AdapterError):
    """A file landed and its codec is not what strict policy asked for.

    PER TRACK, not per invocation, and the distinction is load-bearing in both
    directions. An adapter-level failure raised from inside the per-track loop
    would make ``acquire_with_source`` build a failed ``InvocationResult``
    carrying the results that landed before it, and ``InvocationResult`` refuses
    a failed invocation holding any permanently unavailable result, so one
    delisted track earlier in the same batch would turn a codec refusal into an
    uncaught ValueError with no outcome and no requeue list.

    It is also the same answer the loop already gives when the OFFER says lossy
    under strict policy, which is the identical question asked earlier. A demoted
    client produces one of these per track and the pattern is the signal; one
    truncated file produces exactly one and does not end the run.
    """

    remedy = Remedy.RELAX_LOSSLESS_POLICY


class NoFileLanded(RuntimeError):
    """The downloader answered with no file, carrying whatever cause it swallowed.

    TRANSIENT BY TYPE, whatever its words say (R-703). The message names the
    provider's own error so a rate limit reads as a rate limit, and that error
    can be ``ObjectNotFound: Object not found`` from the album read a download
    makes after the offer has just found the track. ``classify_unavailable``
    reads text, so without this type the carried words would quarantine a live
    track for ever. A ``RuntimeError`` so every reader of the old plain error
    still matches it.

    THE WORDS ARE FOR A PERSON, THE CAUSE IS FOR CODE. ``cause`` holds what the
    tool swallowed, the exception or the message, and every reader that judges
    this error by its text asks the type first: ``classify_unavailable`` here
    and the paced pool's ``classify_signal``, which would otherwise read a
    carried "forbidden" as an account block and stop the run.
    """

    def __init__(self, message: str, *, cause: BaseException | str | None = None) -> None:
        super().__init__(message)
        self.cause = cause


# ---------------------------------------------------------------------------
# The two outcome vocabularies
# ---------------------------------------------------------------------------


class TrackOutcome(StrEnum):
    """Exactly one of these per requested track (R9)."""

    ACQUIRED = "acquired"
    #: The provider says this does not exist. Only an EXPLICIT not-found reaches
    #: here, because this is what feeds quarantine and quarantine is forever.
    UNAVAILABLE_PERMANENT = "unavailable-permanent"
    #: Anything that might work later: server errors, timeouts, rate limits.
    UNAVAILABLE_TRANSIENT = "unavailable-transient"
    #: The source exists and this product declined it. Lossless policy (R21).
    REFUSED_BY_POLICY = "refused-by-policy"


class InvocationOutcome(StrEnum):
    """Exactly one of these per adapter invocation (R9)."""

    OK = "ok"
    AUTH_FAILED = "auth-failed"
    ADAPTER_BROKEN = "adapter-broken"


#: Invocation outcomes that mean the adapter, not the catalogue, is the problem.
#: Derived once and used by the invariants below so a fourth invocation outcome
#: cannot be added without deciding which side of this line it falls on.
FAILED_INVOCATIONS = frozenset({InvocationOutcome.AUTH_FAILED, InvocationOutcome.ADAPTER_BROKEN})


# ---------------------------------------------------------------------------
# Requests and results
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrackRequest:
    """One track to acquire, keyed by the provider's stable identifier.

    ``key`` is an identifier, never a display name (R19, D5). Artist and title
    ride along for messages and for the naming engine downstream; nothing in this
    module keys on them, because a track that gets retitled upstream must still
    match the request that asked for it.
    """

    key: str
    artist: str = ""
    title: str = ""
    isrc: str = ""

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("a track request needs the provider's stable identifier")


@dataclass(frozen=True, slots=True)
class TrackResult:
    """The adapter's answer for one requested track. Self-validating.

    The invariants are the contract's teeth. Each one blocks a shape that the
    source system can currently produce:

    * ACQUIRED with no path: the current tool exits zero having skipped the
      track, so "success" and "silently nothing" are the same observation.
    * ACQUIRED with unknown losslessness: without it, R21's audit verb has no
      fact to audit and the marker decision is unanswerable.
    * Lossy and unmarked: the single failure R21 exists to prevent. Marking is
      mandatory wherever lossy is permitted at all, so an unmarked lossy result
      is not a policy the user could choose, it is a value that cannot exist.
    * A non-acquired result carrying a path: a path here means a file landed, and
      a file that landed while the outcome says otherwise is how a half-download
      gets tagged and imported.
    """

    key: str
    outcome: TrackOutcome
    path: Path | None = None
    #: None only when the track was not acquired.
    lossless: bool | None = None
    #: True when the downstream naming and tagging stages MUST apply the lossy
    #: marker. The marker's TEXT is naming policy owned by config (S3); this
    #: layer states only that it is required, which is the half it can know.
    requires_lossy_marker: bool = False
    detail: str = ""
    remedy: Remedy | None = None

    def __post_init__(self) -> None:
        if self.outcome is TrackOutcome.ACQUIRED:
            if self.path is None:
                raise ValueError(f"{self.key}: an acquired track must name the file it produced")
            if self.lossless is None:
                raise ValueError(f"{self.key}: an acquired track must state whether it is lossless")
            if self.lossless is False and not self.requires_lossy_marker:
                raise ValueError(
                    f"{self.key}: a lossy acquisition must require the marker. R21 permits "
                    f"lossy only WITH mandatory marking, so there is no configuration in "
                    f"which this combination is legal"
                )
        else:
            if self.path is not None:
                raise ValueError(
                    f"{self.key}: {self.outcome} carries a file path; a path means a file "
                    f"landed, and a landed file under a non-acquired outcome is a partial "
                    f"download about to be treated as a track"
                )
            if self.outcome is TrackOutcome.REFUSED_BY_POLICY and self.remedy is None:
                raise ValueError(
                    f"{self.key}: a policy refusal must name the remedy token, or the user "
                    f"is told no without being told what would change the answer"
                )


@dataclass(frozen=True, slots=True)
class InvocationResult:
    """The adapter's answer for one whole invocation, plus its per-track answers.

    ``advances_watermark`` and ``quarantine_keys`` are the two decisions the sync
    layer makes from this object, and both are computed here rather than by each
    caller. That placement is the point: "auth-failed and adapter-broken never
    advance a watermark and never quarantine a track" is one rule with one
    implementation, instead of a rule three call sites are each trusted to
    remember.
    """

    adapter: str
    outcome: InvocationOutcome
    results: tuple[TrackResult, ...] = ()
    #: Every key this invocation was ASKED for, in order. Carried so the result
    #: can answer "what still needs doing" on its own. Without it, an invocation
    #: that died before it looked at anything reports nothing about anything, and
    #: the caller has to reconstruct the queue from the request list it happens to
    #: still be holding. KTD25's claim is that a typed failure must be recoverable
    #: downstream, and "which tracks did I not get" is the recovery.
    requested: tuple[str, ...] = ()
    detail: str = ""
    remedy: Remedy | None = None
    #: Other registered adapter names, so a failure can name the replacement path
    #: (AE9) without this module importing a registry it sits below.
    alternatives: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.requested:
            asked = set(self.requested)
            stray = [r.key for r in self.results if r.key not in asked]
            if stray:
                raise ValueError(
                    f"{self.adapter}: reported on track(s) nobody asked for "
                    f"({', '.join(stray[:3])}); a result keyed to something outside the "
                    f"request is an identity mix-up, and downstream it becomes a file "
                    f"filed under the wrong track"
                )
        if self.outcome in FAILED_INVOCATIONS:
            if self.remedy is None:
                raise ValueError(
                    f"{self.adapter}: a failed invocation must carry a remedy token; a "
                    f"bare failure is the collapse KTD25 forbids"
                )
            poisoned = [
                r.key
                for r in self.results
                if r.outcome is TrackOutcome.UNAVAILABLE_PERMANENT
            ]
            if poisoned:
                raise ValueError(
                    f"{self.adapter}: {self.outcome} reported {len(poisoned)} track(s) as "
                    f"permanently unavailable ({', '.join(poisoned[:3])}); a broken adapter "
                    f"cannot know a track is delisted, and quarantine is never re-queued"
                )
        if self.outcome is InvocationOutcome.AUTH_FAILED and not self.alternatives:
            raise ValueError(
                f"{self.adapter}: an authentication failure must name the replacement "
                f"path (AE9). Reporting it with nowhere to go is the report that made "
                f"the source system's outage look like missing tracks"
            )

    # -- the two decisions the sync layer makes from this ------------------

    @property
    def ok(self) -> bool:
        return self.outcome is InvocationOutcome.OK

    @property
    def advances_watermark(self) -> bool:
        """Only a clean invocation moves a source's watermark forward.

        A watermark advanced across a failed run is how items go permanently
        unseen: the next run asks for everything after the mark, and the mark is
        past the things the failed run never looked at.
        """
        return self.ok

    def acquired(self) -> tuple[TrackResult, ...]:
        return tuple(r for r in self.results if r.outcome is TrackOutcome.ACQUIRED)

    def quarantine_keys(self) -> tuple[str, ...]:
        """Tracks the caller may record as permanently unavailable.

        Empty on any failed invocation, unconditionally. The construction-time
        invariant above already makes a permanent result unrepresentable there;
        this is the same rule stated where the caller reads it, so the two cannot
        drift apart.
        """
        if not self.ok:
            return ()
        return tuple(r.key for r in self.results if r.outcome is TrackOutcome.UNAVAILABLE_PERMANENT)

    def requeue_keys(self) -> tuple[str, ...]:
        """Tracks that stay eligible for a later run.

        On a clean invocation that is the transient set plus the policy refusals,
        since relaxing the policy changes the answer.

        On a FAILED invocation it is everything requested that did not land,
        including the tracks the adapter never reached. That is the half AE9
        turns on: an adapter that died at authentication looked at nothing, so
        reporting only what it managed to classify would present a dead session
        as a catalogue with nothing new in it.
        """
        if not self.ok:
            landed = {r.key for r in self.results if r.outcome is TrackOutcome.ACQUIRED}
            pending = self.requested or tuple(r.key for r in self.results)
            return tuple(key for key in pending if key not in landed)
        return tuple(
            r.key
            for r in self.results
            if r.outcome in (TrackOutcome.UNAVAILABLE_TRANSIENT, TrackOutcome.REFUSED_BY_POLICY)
        )

    def counts(self) -> Mapping[TrackOutcome, int]:
        """Per-outcome totals, with every outcome present including the zeroes.

        Derived from the enum rather than from what happened to occur, so a
        summary never omits a category by accident of an empty run (P3).
        """
        tally = {outcome: 0 for outcome in TrackOutcome}
        for result in self.results:
            tally[result.outcome] += 1
        return tally


# ---------------------------------------------------------------------------
# Exhaustive dispatch: the caller cannot ignore an outcome
# ---------------------------------------------------------------------------


class IncompleteHandling(AdapterError):
    """A caller supplied handlers for some outcomes but not all of them."""

    remedy = Remedy.SWITCH_ADAPTER


def dispatch(
    result: InvocationResult,
    handlers: Mapping[TrackOutcome, Callable[[TrackResult], object]],
) -> list[object]:
    """Route every per-track result to its handler, refusing partial coverage.

    The required set is read off ``TrackOutcome`` at run time. That is the whole
    mechanism: a fifth outcome added later fails every existing caller at once,
    at the call, instead of being silently dropped by whichever ``if`` chain
    happened not to mention it. Enumerating the four here instead would make this
    function a list in disguise (P4).
    """
    missing = sorted(str(o) for o in TrackOutcome if o not in handlers)
    if missing:
        raise IncompleteHandling(
            f"no handler for {', '.join(missing)}; every per-track outcome needs a "
            f"distinct answer, which is the distinction the contract exists to provide"
        )
    return [handlers[r.outcome](r) for r in result.results]


def dispatch_invocation(
    result: InvocationResult,
    handlers: Mapping[InvocationOutcome, Callable[[InvocationResult], object]],
) -> object:
    """The invocation-level twin of ``dispatch``, with the same completeness rule."""
    missing = sorted(str(o) for o in InvocationOutcome if o not in handlers)
    if missing:
        raise IncompleteHandling(
            f"no handler for {', '.join(missing)}; an unhandled invocation outcome is "
            f"how an authentication failure gets reported as missing tracks (AE9)"
        )
    return handlers[result.outcome](result)


# ---------------------------------------------------------------------------
# Permanence classification, ported verbatim in rule
# ---------------------------------------------------------------------------

#: Server-side trouble wording. A 503 renders as "Service Unavailable", and a
#: naive "unavailable" substring match reads that as a delisted track. Getting
#: this backwards poisons the quarantine store, and quarantine means never
#: re-queued, so the mistake is permanent and silent. Checked FIRST for exactly
#: that reason: the transient evidence wins over any later not-found reading.
TRANSIENT_MARKERS = ("503", "5xx", "server error", "service unavailable")


#: Python error classes a provider cannot raise. Each one means the code calling
#: the provider is wrong, whether that code is this repository's or the vendored
#: tool's, and no amount of waiting changes it. ``UnboundLocalError`` is a
#: ``NameError`` and is covered by it.
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)


def raise_if_defect(exc: BaseException) -> None:
    """Escalate a code defect raised under a per-track call to ``AdapterBroken``.

    Asked BEFORE any reading of the message. The per-track fallback reads text
    for provider signals and calls everything else transient, which is honest
    for an unknown provider error and wrong for a class no provider raises: the
    first real download reported ``'function' object has no attribute 'info'``
    as a retryable outage, and a job retrying it would have retried it forever
    (R-348). An invocation failure also keeps every unlanded track queued, so
    the fix is one report and one re-run rather than a lost batch.
    """
    if isinstance(exc, DEFECT_ERRORS):
        raise AdapterBroken(
            f"a defect in the acquisition code, not a provider failure "
            f"({type(exc).__name__}: {exc})",
            remedy=Remedy.REPORT_DEFECT,
        ) from exc


def classify_unavailable(exc: BaseException) -> TrackOutcome:
    """Classify a failed per-track lookup as permanently or transiently unavailable.

    Ported unchanged in rule from the source system, because the rule is the
    valuable part: ONLY an explicit not-found answer counts as permanent. An
    exception class named ``*NotFound``, a response status of 404, or "404" /
    "not found" in the text. Everything else, including network hiccups,
    timeouts, rate limits, and authentication errors, is transient.

    Authentication errors reaching here at all is a caller bug, not a
    classification question: an invocation whose session died reports AUTH_FAILED
    and classifies nothing. Treating them as transient is the safe reading if one
    slips through, since transient is re-queueable and costs a retry.

    A ``NoFileLanded`` is transient before any reading of its text, because its
    text is a swallowed cause quoted for a person to read, not the answer to
    this track's lookup (R-703). It is raised FROM that cause, so it is asked
    before the status below, which would otherwise find the cause's 404.

    THE 404 IS READ OFF THE STATUS NEAREST THE FAILURE, ``core.cause``'s
    ``answered_not_found`` (R-1313). The provider client decodes an error
    answer's body inside its handler of the HTTP error, so a 404 whose body is
    a page arrives as the decode error with the 404 three context links down,
    and read off the failure alone a delisted track was retried on every run.
    The class name and the text are still read off the failure alone.
    """
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
    if any(marker in text for marker in TRANSIENT_MARKERS):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    if "notfound" in type(exc).__name__.lower():
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if "404" in text or "not found" in text:
        return TrackOutcome.UNAVAILABLE_PERMANENT
    return TrackOutcome.UNAVAILABLE_TRANSIENT


# ---------------------------------------------------------------------------
# Lossless policy (R21, S3, AE4)
# ---------------------------------------------------------------------------


class LosslessPolicy(StrEnum):
    """The two legal answers. There is deliberately no third.

    A "lossy allowed, marking off" value is not validated away; it is not
    expressible. That is stronger, because a value that cannot be written cannot
    be reached by a migration, a hand-edited file, or a future default change.
    """

    STRICT = "strict"
    ALLOW_LOSSY_MARKED = "allow_lossy_marked"


_LOSSY_DETAIL = "the provider offers this track only in a lossy format"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Whether to take this source, and what the taking obliges downstream.

    ``source_is_lossless`` is carried rather than dropped so the R21 invariant can
    be stated on the DECISION rather than only on the result built from it. A
    decision object that has forgotten what it was deciding about can only be
    checked by inspecting its message text, and a check on message text is a
    check that a typo disables.
    """

    permitted: bool
    marker_required: bool
    source_is_lossless: bool
    remedy: Remedy | None = None
    detail: str = ""

    def __post_init__(self) -> None:
        if self.permitted and not self.source_is_lossless and not self.marker_required:
            raise ValueError(
                "a permitted lossy source must require the marker; R21 allows lossy only "
                "WITH mandatory marking, so this decision is not one the policy can reach"
            )


def decide_lossless(policy: LosslessPolicy, *, source_is_lossless: bool) -> PolicyDecision:
    """Apply the lossless policy to what the provider actually offers.

    Pure, and separated from the adapter loop on purpose: AE4's two halves are
    one function called with two policies, which is testable with no provider,
    no account, and no file.
    """
    if source_is_lossless:
        return PolicyDecision(permitted=True, marker_required=False, source_is_lossless=True)
    if policy is LosslessPolicy.STRICT:
        return PolicyDecision(
            permitted=False,
            marker_required=False,
            source_is_lossless=False,
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            detail=_LOSSY_DETAIL,
        )
    return PolicyDecision(
        permitted=True, marker_required=True, source_is_lossless=False, detail=_LOSSY_DETAIL
    )


# ---------------------------------------------------------------------------
# Settings the ADAPTER owns (KTD20)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AdapterSettings:
    """Quality, pacing, and destination, held in the adapter for one run.

    KTD20 moves these inside the adapter, and the failure class it removes is
    concrete rather than theoretical. In the source system they live in the
    downloaded tool's own global ``settings.json``, which the product mutates
    through subprocess calls before every run. Two observed events reset that
    file to factory defaults: two pacing writes racing each other, and a process
    kill landing mid-write. Factory defaults are lossy audio into the tool's own
    download directory, so a reset silently violated the lossless rule AND the
    path convention every later stage assumed, with no error until the wrong
    files turned up, or did not.

    Frozen, in memory, per invocation. A value that is never written to a shared
    file cannot be reverted by another process, so the guard the source system
    needed against its own settings file has nothing left to guard.

    The one thing that must still be checked is that the wrapped tool ACCEPTED
    these values, which is what ``verify_applied`` below is for.
    """

    download_staging: Path
    quality: str = "lossless"
    lossless_policy: LosslessPolicy = LosslessPolicy.STRICT
    #: None means "the adapter's own default", which ``download.Pacing`` supplies.
    #: An explicit 0.0 is a different answer from None: it means the user turned
    #: pacing off, so the two are never collapsed by a falsy test.
    pacing_delay_s: float | None = None
    #: Concurrent acquisitions. U15's bounded pool reads THIS field; there is no
    #: second cap anywhere, which is the whole point of KTD20 moving the setting
    #: off the wrapped tool's shared settings file.
    concurrency: int = 1
    #: The provider gate's two numbers (R-705), read off ``[provider]``. Carried
    #: here so the vendored adapter, which builds the tool's session itself,
    #: paces it with the same interval the catalogue and the account use, off
    #: the same frozen configuration.
    gate: GateSettings = GateSettings()

    def __post_init__(self) -> None:
        if self.concurrency < 1:
            raise ValueError("concurrency must be at least one acquisition at a time")
        if self.pacing_delay_s is not None and self.pacing_delay_s < 0:
            raise ValueError("a pacing delay cannot be negative")

    @classmethod
    def from_config(cls, cfg: object) -> AdapterSettings:
        """Build settings from a loaded configuration object.

        Takes the config as a PARAMETER rather than loading it. The adapter layer
        may read configuration, but a constructor that loads it cannot be
        exercised against two policies in one process, and proving both halves of
        AE4 needs exactly that.
        """
        acquisition = cfg.acquisition  # type: ignore[attr-defined]
        paths = cfg.paths  # type: ignore[attr-defined]
        return cls(
            download_staging=Path(paths.download_staging),
            quality=acquisition.quality,
            lossless_policy=LosslessPolicy(acquisition.lossless_policy),
            pacing_delay_s=acquisition.pacing_delay_s,
            concurrency=acquisition.concurrency,
            gate=GateSettings.from_config(cfg),
        )


#: Sentinel for "the wrapped tool has no such setting at all", which is a
#: different failure from "it has it and holds the wrong value": the first means
#: the tool changed shape under us, the second means a write did not stick.
_MISSING = object()


def verify_applied(
    applied: Mapping[str, object], expected: Mapping[str, object]
) -> list[str]:
    """Report every setting the wrapped tool did not take.

    The source system's guard checked two hand-named keys before every download.
    This checks every key the adapter pushed, because the guard's value was never
    in the two names: it was in refusing to run against settings that are not the
    ones we asked for. Iterating what was pushed means a third setting is covered
    by being pushed, not by somebody editing the guard (P3).
    """
    problems: list[str] = []
    for key, want in expected.items():
        got = applied.get(key, _MISSING)
        if got is _MISSING:
            problems.append(f"{key} was not accepted at all (the setting is absent)")
        elif got != want:
            problems.append(f"{key} is {got!r}, must be {want!r}")
    return problems


# ---------------------------------------------------------------------------
# The source seam: the one place a real tool is touched
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Offer:
    """What the provider says it has for one track, before anything is fetched."""

    lossless: bool
    detail: str = ""


@runtime_checkable
class TrackSource(Protocol):
    """The tool-facing half of an adapter: three calls, all of them I/O.

    Everything above this line is pure and everything below it is a real network
    or subprocess. Splitting them here is what makes the contract provable
    without an account: the conformance suite drives a fake source through the
    identical loop the vendored and alternative adapters use.

    Implementations raise ``AdapterAuthFailed`` when the session is rejected and
    ``AdapterBroken`` when the tool cannot run. ``fetch`` may also raise
    ``LosslessRefused`` when it inspected the file it landed and the codec is not
    what the policy asked for; that becomes REFUSED_BY_POLICY and does NOT go
    through ``classify_unavailable``, because the track is not unavailable, it is
    declined. Any other exception from ``offer`` or ``fetch`` is a per-track
    failure and goes to ``classify_unavailable``.

    Checking the landed file is OPTIONAL for an implementation and the contract
    says so rather than pretending otherwise: the vendored adapter does it, the
    alternative does not, and R-213 records that gap.
    """

    def authenticate(self) -> None:
        """Establish or refresh the provider session. Raises on failure."""

    def offer(self, request: TrackRequest) -> Offer:
        """What the provider has for this track. Raises when it has nothing."""

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        """Download the track and return the file that landed."""


def acquire_with_source(
    *,
    adapter: str,
    source: TrackSource,
    requests: Iterable[TrackRequest],
    settings: AdapterSettings,
    alternatives: Sequence[str] = (),
    sleep: Callable[[float], None] = time.sleep,
) -> InvocationResult:
    """Run one acquisition against a source, producing a contract-shaped result.

    Both shipped adapters delegate here, and that is deliberate rather than
    accidental reuse. What actually differs between two acquisition tools is
    credential handling, settings translation, and error vocabulary, all of which
    live in the source implementation. The ORDER of operations is contract, not
    implementation: authenticate, then per track offer, apply policy, fetch, pace.
    Letting each adapter re-write that order is how the source system ended up
    with two call sites that classify the same failure differently.

    Pacing lives in this loop because the adapter owns it (KTD20). U15's
    ``download.acquire_concurrently`` is the paced, bounded replacement for this
    loop and reads the SAME settings object rather than declaring a second cap or
    a second delay. This sequential form stays as the contract's reference
    implementation: it is what the conformance suite drives, and it is the one
    place the ORDER of operations is stated once for every adapter.

    Note the one deliberate difference. This loop reads the delay with ``or 0.0``
    and so treats an unset delay as no delay, which is what its own tests assume.
    The paced driver distinguishes unset from zero, because unset means "use the
    adapter's default" and zero means "the user turned pacing off".
    """
    # Materialised before authentication, not after. The requested set has to be
    # reportable even when the run dies on its first call, and an iterator that
    # was never walked cannot report anything.
    ordered = tuple(requests)
    requested = tuple(request.key for request in ordered)

    try:
        source.authenticate()
    except AdapterAuthFailed as exc:
        return InvocationResult(
            adapter=adapter,
            outcome=InvocationOutcome.AUTH_FAILED,
            requested=requested,
            detail=str(exc),
            remedy=exc.remedy,
            alternatives=tuple(alternatives),
        )
    except AdapterBroken as exc:
        return InvocationResult(
            adapter=adapter,
            outcome=InvocationOutcome.ADAPTER_BROKEN,
            requested=requested,
            detail=str(exc),
            remedy=exc.remedy,
            alternatives=tuple(alternatives),
        )

    results: list[TrackResult] = []
    delay = settings.pacing_delay_s or 0.0

    for index, request in enumerate(ordered):
        if index and delay:
            sleep(delay)
        try:
            outcome = acquire_one(source, request, settings)
        except AdapterAuthFailed as exc:
            # Mid-run session death. Everything already acquired is kept and
            # reported, but the invocation is a failure, so no watermark moves
            # and the untouched remainder stays queued rather than being read as
            # absent from the catalogue (AE9).
            return InvocationResult(
                adapter=adapter,
                outcome=InvocationOutcome.AUTH_FAILED,
                results=tuple(results),
                requested=requested,
                detail=str(exc),
                remedy=exc.remedy,
                alternatives=tuple(alternatives),
            )
        except AdapterBroken as exc:
            return InvocationResult(
                adapter=adapter,
                outcome=InvocationOutcome.ADAPTER_BROKEN,
                results=tuple(results),
                requested=requested,
                detail=str(exc),
                remedy=exc.remedy,
                alternatives=tuple(alternatives),
            )
        results.append(outcome)

    return InvocationResult(
        adapter=adapter,
        outcome=InvocationOutcome.OK,
        results=tuple(results),
        requested=requested,
        alternatives=tuple(alternatives),
    )


def acquire_one(
    source: TrackSource, request: TrackRequest, settings: AdapterSettings
) -> TrackResult:
    """One track, from offer through policy to file. Auth failures propagate.

    Public because the paced pool in ``download`` runs the SAME per-track step
    rather than writing its own. Duplicating the sequence there is how the source
    system ended up with two call sites classifying one provider failure two
    different ways, so the concurrent driver reuses this one and varies only what
    surrounds it.
    """
    # THE GATE'S TRIP PASSES THROUGH BOTH CATCHES BELOW (R-705). It is the job
    # engine's own park, and a park read as one dead track would fail the item
    # and let the driver claim the next one, which is the second request into a
    # block that the pacing layer exists to never make. Imported here because
    # the engine imports the CLI package, which imports this module.
    from cratekit.core.jobs import Parked  # noqa: PLC0415 - see the comment above

    try:
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken, Parked):
        raise
    except Exception as exc:  # noqa: BLE001 - one dead track never sinks the run
        raise_if_defect(exc)
        return _unavailable(request, exc)

    decision = decide_lossless(settings.lossless_policy, source_is_lossless=offer.lossless)
    if not decision.permitted:
        return TrackResult(
            key=request.key,
            outcome=TrackOutcome.REFUSED_BY_POLICY,
            detail=decision.detail,
            remedy=decision.remedy,
        )

    try:
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken, Parked):
        raise
    except LosslessRefused as exc:
        # A file landed and it is the wrong kind. Not a missing track and not a
        # broken adapter: the same refusal the offer check above would have given
        # had the provider told the truth about what it was going to send.
        return TrackResult(
            key=request.key,
            outcome=TrackOutcome.REFUSED_BY_POLICY,
            detail=str(exc),
            remedy=exc.remedy,
        )
    except Exception as exc:  # noqa: BLE001 - same rule as the lookup above
        raise_if_defect(exc)
        return _unavailable(request, exc)

    return TrackResult(
        key=request.key,
        outcome=TrackOutcome.ACQUIRED,
        path=Path(path),
        lossless=offer.lossless,
        requires_lossy_marker=decision.marker_required,
    )


def _unavailable(request: TrackRequest, exc: BaseException) -> TrackResult:
    """Turn a per-track exception into a classified result.

    A transient failure carries the retry token and a permanent one carries none,
    because there is nothing for the user to do about a delisted track and
    offering them a remedy that changes nothing is how remedies stop being read.
    """
    classification = classify_unavailable(exc)
    return TrackResult(
        key=request.key,
        outcome=classification,
        detail=str(exc),
        remedy=(
            Remedy.RETRY_LATER
            if classification is TrackOutcome.UNAVAILABLE_TRANSIENT
            else None
        ),
    )


# ---------------------------------------------------------------------------
# The adapter itself
# ---------------------------------------------------------------------------


@runtime_checkable
class AcquisitionAdapter(Protocol):
    """What configuration selects and the acquisition layer calls.

    Two members only. Keeping the surface this small is what makes the interface
    a real substitution point: an adapter that also had to expose the wrapped
    tool's session object, its settings file, or its progress callbacks would be
    substitutable only by something shaped like the tool it replaced.
    """

    name: str

    def acquire(self, requests: Iterable[TrackRequest]) -> InvocationResult:
        """Acquire every requested track, reporting per the contract."""


class BaseAdapter:
    """Shared adapter plumbing: settings ownership and the delegation to the loop.

    Not a convenience base class. It is the place the two things every adapter
    must do identically live, so that "both adapters satisfy the same contract"
    is a structural fact rather than a claim two files have to keep agreeing on.

    Deliberately NOT a dataclass. ``name`` is a class attribute each adapter
    overrides, and a dataclass field would assign the base value onto every
    instance at construction, silently replacing each adapter's identity with an
    empty string. That is the kind of defect that only shows up in the failure
    message of an unrelated outage.
    """

    #: The stable identifier configuration records. Overridden by every adapter.
    name: str = ""

    def __init__(self, settings: AdapterSettings, *, source: TrackSource | None = None) -> None:
        if not self.name:
            raise AdapterBroken(
                f"{type(self).__name__} declares no adapter name; the name is the "
                f"identifier configuration records and the registry resolves"
            )
        self.settings = settings
        #: An injected source replaces the wrapped tool and NOTHING else. The
        #: credential scope, the settings, the loop, and the result shaping all
        #: still run, which is what makes a test against a fake source a test of
        #: the adapter rather than a test of the fake.
        self._injected = source

    def _session_scope(self) -> AbstractContextManager[object]:
        """The credential lifetime for one invocation.

        Default is a no-op so an adapter that genuinely holds no credential does
        not have to pretend. Both shipped adapters override it with the private
        short-lived session file, which is what makes "no plaintext token
        survives a run" a property of the base flow rather than of each adapter
        remembering.
        """
        return nullcontext(None)

    def _source(self, scope: object) -> TrackSource:  # pragma: no cover - overridden
        raise NotImplementedError

    def _alternatives(self) -> tuple[str, ...]:
        """Names to offer when this adapter fails.

        Resolved through the registry at CALL time, not at import time, so an
        adapter can name its replacement while its own tool is unimportable.
        """
        from cratekit.acquire import alternatives_to  # noqa: PLC0415 - see docstring

        return alternatives_to(self.name)

    def acquire(
        self,
        requests: Iterable[TrackRequest],
        *,
        sleep: Callable[[float], None] = time.sleep,
    ) -> InvocationResult:
        """Run one acquisition, with the credential live only for its duration.

        The two adapter-level failures are caught HERE rather than inside the
        loop, because both can happen before there is a source at all: an absent
        tool and an unreadable credential are both "this adapter cannot run", and
        a caller must get one contract-shaped answer either way rather than an
        exception from one path and a result object from the other.
        """
        ordered = tuple(requests)
        try:
            with self._session_scope() as scope:
                source = self._injected if self._injected is not None else self._source(scope)
                return acquire_with_source(
                    adapter=self.name,
                    source=source,
                    requests=ordered,
                    settings=self.settings,
                    alternatives=self._alternatives(),
                    sleep=sleep,
                )
        except AdapterAuthFailed as exc:
            return InvocationResult(
                adapter=self.name,
                outcome=InvocationOutcome.AUTH_FAILED,
                requested=tuple(request.key for request in ordered),
                detail=str(exc),
                remedy=exc.remedy,
                alternatives=self._alternatives(),
            )
        except AdapterBroken as exc:
            return InvocationResult(
                adapter=self.name,
                outcome=InvocationOutcome.ADAPTER_BROKEN,
                requested=tuple(request.key for request in ordered),
                detail=str(exc),
                remedy=exc.remedy,
                alternatives=self._alternatives(),
            )


__all__ = [
    "DEFECT_ERRORS",
    "FAILED_INVOCATIONS",
    "TRANSIENT_MARKERS",
    "AcquisitionAdapter",
    "AdapterAuthFailed",
    "AdapterBroken",
    "AdapterError",
    "AdapterSettings",
    "BaseAdapter",
    "IncompleteHandling",
    "InvocationOutcome",
    "InvocationResult",
    "LosslessPolicy",
    "LosslessRefused",
    "NoFileLanded",
    "Offer",
    "PolicyDecision",
    "Remedy",
    "TrackOutcome",
    "TrackRequest",
    "TrackResult",
    "TrackSource",
    "UnknownAdapter",
    "acquire_one",
    "acquire_with_source",
    "classify_unavailable",
    "raise_if_defect",
    "decide_lossless",
    "dispatch",
    "dispatch_invocation",
    "verify_applied",
]
