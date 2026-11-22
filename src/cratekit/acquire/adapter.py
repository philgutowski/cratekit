"""The acquisition contract: what an adapter promises, as types rather than luck.

The vendored downloader's upstream is gone, so a provider change is survivable only
if a different tool can stand in behind one declared contract (R9). The contract
gives exactly one answer per requested track (ACQUIRED, UNAVAILABLE_PERMANENT,
UNAVAILABLE_TRANSIENT, REFUSED_BY_POLICY) and one per invocation (OK, AUTH_FAILED,
ADAPTER_BROKEN), so a dead session never reads as missing tracks (AE9).

The types enforce it: ``TrackResult`` refuses illegal combinations such as an
unmarked lossy file (R21), ``InvocationResult`` refuses a permanent unavailability
from a failed invocation because quarantine is forever, and ``dispatch`` reads the
outcome set off the enum so a new outcome breaks every caller loudly. Everything
above the source seam is pure, so both adapters are proven against one suite with
no account or tool installed.
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
from cratekit.core.config import RemediedError
from cratekit.core.provider_gate import GateSettings

# Remediation vocabulary


class Remedy(StrEnum):
    """What to do about an acquisition failure, as a TOKEN rather than a command.

    Only the CLI renders a token into text, because the text depends on platform and
    interface (D2). Same shape as ``core/config.py`` and ``core/secrets.py`` (S4).
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
    #: No keychain to read the session from, so re-authorising has nowhere to land.
    REPAIR_CREDENTIAL_STORE = "repair-credential-store"
    #: A transient provider failure. The track stays re-queueable; nothing to fix.
    RETRY_LATER = "retry-later"
    #: The tool's own settings did not take the values the adapter pushed in.
    REPAIR_ADAPTER_SETTINGS = "repair-adapter-settings"
    #: The provider refused this CLIENT (forbidden, bot challenge). Not
    #: ``RETRY_LATER``, because retrying a block is what turns it into a lockout.
    PAUSE_AND_CHECK_ACCOUNT = "pause-and-check-account"
    #: A defect in this program. Retrying repeats it forever, so report it.
    REPORT_DEFECT = "report-defect"


class AdapterError(RemediedError):
    """Base for acquisition failures. Always carries a structured remedy token."""

    remedy: Remedy = Remedy.SWITCH_ADAPTER


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

    PER TRACK, the same answer as a lossy offer under strict policy. As an
    invocation failure, an earlier permanent result in the batch would make the
    failed ``InvocationResult`` refuse to build at all.
    """

    remedy = Remedy.RELAX_LOSSLESS_POLICY


class NoFileLanded(RuntimeError):
    """The downloader answered with no file, carrying whatever cause it swallowed.

    TRANSIENT BY TYPE, whatever its words say (R-703): the quoted cause can read
    "not found" for a live track. The words are for a person; ``cause`` is for code,
    and every text reader (``classify_unavailable``, ``classify_signal``) asks the
    type first. A ``RuntimeError`` so readers of the old plain error still match.
    """

    def __init__(self, message: str, *, cause: BaseException | str | None = None) -> None:
        super().__init__(message)
        self.cause = cause


# The two outcome vocabularies


class TrackOutcome(StrEnum):
    """Exactly one of these per requested track (R9)."""

    ACQUIRED = "acquired"
    #: Only an EXPLICIT not-found, because this feeds quarantine, which is forever.
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
FAILED_INVOCATIONS = frozenset({InvocationOutcome.AUTH_FAILED, InvocationOutcome.ADAPTER_BROKEN})


# Requests and results


@dataclass(frozen=True, slots=True)
class TrackRequest:
    """One track to acquire, keyed by the provider's stable identifier (R19, D5).

    Nothing keys on artist or title, so a track retitled upstream still matches.
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

    Refused: ACQUIRED with no path or unknown losslessness, lossy and unmarked
    (R21), and a non-acquired result carrying a path, which is a half-download.
    """

    key: str
    outcome: TrackOutcome
    path: Path | None = None
    #: None only when the track was not acquired.
    lossless: bool | None = None
    #: Downstream naming MUST apply the lossy marker; its text is config's (S3).
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

    The watermark and quarantine decisions are computed here once, so a failed
    invocation never advances one or quarantines a track at any call site.
    """

    adapter: str
    outcome: InvocationOutcome
    results: tuple[TrackResult, ...] = ()
    #: Every key ASKED for, in order, so a run that died early can still say what
    #: remains to do (KTD25).
    requested: tuple[str, ...] = ()
    detail: str = ""
    remedy: Remedy | None = None
    #: Other registered adapter names, so a failure names the replacement (AE9).
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

    # The two decisions the sync layer makes from this.

    @property
    def ok(self) -> bool:
        return self.outcome is InvocationOutcome.OK

    @property
    def advances_watermark(self) -> bool:
        """Only a clean invocation moves a watermark, or unseen items are skipped."""
        return self.ok

    def acquired(self) -> tuple[TrackResult, ...]:
        return tuple(r for r in self.results if r.outcome is TrackOutcome.ACQUIRED)

    def quarantine_keys(self) -> tuple[str, ...]:
        """Tracks the caller may record as permanently unavailable; none on failure."""
        if not self.ok:
            return ()
        return tuple(r.key for r in self.results if r.outcome is TrackOutcome.UNAVAILABLE_PERMANENT)

    def requeue_keys(self) -> tuple[str, ...]:
        """Tracks that stay eligible for a later run.

        Clean: transients and policy refusals. Failed: everything requested that did
        not land, including tracks never reached, so a dead session is not read as
        an empty catalogue (AE9).
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
        """Per-outcome totals, every outcome present including the zeroes (P3)."""
        tally = {outcome: 0 for outcome in TrackOutcome}
        for result in self.results:
            tally[result.outcome] += 1
        return tally


# Exhaustive dispatch: the caller cannot ignore an outcome


class IncompleteHandling(AdapterError):
    """A caller supplied handlers for some outcomes but not all of them."""

    remedy = Remedy.SWITCH_ADAPTER


def dispatch(
    result: InvocationResult,
    handlers: Mapping[TrackOutcome, Callable[[TrackResult], object]],
) -> list[object]:
    """Route every per-track result to its handler, refusing partial coverage.

    The required set is read off ``TrackOutcome`` so a new outcome fails every
    caller at once rather than being dropped silently (P4).
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


# Permanence classification, ported verbatim in rule

#: Server-side trouble wording, checked FIRST so a 503 "Service Unavailable" never
#: reads as a delisted track and poisons quarantine.
TRANSIENT_MARKERS = ("503", "5xx", "server error", "service unavailable")


#: Python error classes a provider cannot raise, so each is a code defect that no
#: wait cures. ``UnboundLocalError`` is a ``NameError``.
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)


def raise_if_defect(exc: BaseException) -> None:
    """Escalate a code defect raised under a per-track call to ``AdapterBroken``.

    Asked BEFORE any reading of the message, since the text fallback would call it
    transient and retry it forever (R-348). Unlanded tracks stay queued.
    """
    if isinstance(exc, DEFECT_ERRORS):
        raise AdapterBroken(
            f"a defect in the acquisition code, not a provider failure "
            f"({type(exc).__name__}: {exc})",
            remedy=Remedy.REPORT_DEFECT,
        ) from exc


def classify_unavailable(exc: BaseException) -> TrackOutcome:
    """Classify a failed per-track lookup as permanently or transiently unavailable.

    ONLY an explicit not-found is permanent: a ``*NotFound`` class, a 404 status, or
    "404" / "not found" in the text. Everything else is transient, which costs only
    a retry. A ``NoFileLanded`` is transient first, since its text quotes a cause
    (R-703). The 404 status is read nearest the failure through the context chain,
    because a decode error can wrap it (R-1313).
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


# Lossless policy (R21, S3, AE4)


class LosslessPolicy(StrEnum):
    """The two legal answers. "Lossy allowed, marking off" is not expressible."""

    STRICT = "strict"
    ALLOW_LOSSY_MARKED = "allow_lossy_marked"


_LOSSY_DETAIL = "the provider offers this track only in a lossy format"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Whether to take this source, and what the taking obliges downstream.

    ``source_is_lossless`` is carried so the R21 invariant holds on the decision.
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
    """Apply the lossless policy to what the provider offers. Pure (AE4)."""
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


# Settings the ADAPTER owns (KTD20)


@dataclass(frozen=True, slots=True)
class AdapterSettings:
    """Quality, pacing, and destination, held in the adapter for one run (KTD20).

    Frozen and in memory, never in the tool's shared settings file, which races and
    resets to lossy defaults. ``verify_applied`` checks the tool accepted them.
    """

    download_staging: Path
    quality: str = "lossless"
    lossless_policy: LosslessPolicy = LosslessPolicy.STRICT
    #: None is the adapter's default; 0.0 means pacing off. Never a falsy test.
    pacing_delay_s: float | None = None
    #: Concurrent acquisitions; the only cap, read by U15's bounded pool.
    concurrency: int = 1
    #: The provider gate's numbers off ``[provider]`` (R-705), so the vendored
    #: session paces like the catalogue and the account.
    gate: GateSettings = GateSettings()

    def __post_init__(self) -> None:
        if self.concurrency < 1:
            raise ValueError("concurrency must be at least one acquisition at a time")
        if self.pacing_delay_s is not None and self.pacing_delay_s < 0:
            raise ValueError("a pacing delay cannot be negative")

    @classmethod
    def from_config(cls, cfg: object) -> AdapterSettings:
        """Build settings from a config passed in, so two policies fit one process."""
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


#: Sentinel for a setting the tool lacks entirely, which means the tool changed
#: shape, unlike a wrong value, which means a write did not stick.
_MISSING = object()


def verify_applied(
    applied: Mapping[str, object], expected: Mapping[str, object]
) -> list[str]:
    """Report every pushed setting the wrapped tool did not take (P3)."""
    problems: list[str] = []
    for key, want in expected.items():
        got = applied.get(key, _MISSING)
        if got is _MISSING:
            problems.append(f"{key} was not accepted at all (the setting is absent)")
        elif got != want:
            problems.append(f"{key} is {got!r}, must be {want!r}")
    return problems


# The source seam: the one place a real tool is touched


@dataclass(frozen=True, slots=True)
class Offer:
    """What the provider says it has for one track, before anything is fetched."""

    lossless: bool
    detail: str = ""


@runtime_checkable
class TrackSource(Protocol):
    """The tool-facing half of an adapter: three calls, all of them I/O.

    Raise ``AdapterAuthFailed`` for a rejected session and ``AdapterBroken`` when
    the tool cannot run. ``fetch`` may raise ``LosslessRefused`` for a wrong codec,
    which is REFUSED_BY_POLICY; anything else is classified per track. Checking
    the landed file is optional (R-213).
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

    The reference loop, stating the ORDER once for every adapter: authenticate,
    then per track offer, policy, fetch, pace. ``download.acquire_concurrently``
    is the paced pool on the same settings; unlike it, this loop reads an unset
    delay as no delay.
    """
    # Materialised first, so the requested set is reportable if auth fails.
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
            # Mid-run session death: keep what landed, queue the rest (AE9).
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

    Public so the paced pool in ``download`` runs this same step, never its own.
    """
    # The gate's park passes through both catches (R-705), or the driver would make
    # a second request into a block. Imported here to avoid an import cycle.
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
        # The wrong kind landed: the same refusal an honest offer would have given.
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
    """Turn a per-track exception into a classified result; only transients retry."""
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


# The adapter itself


@runtime_checkable
class AcquisitionAdapter(Protocol):
    """What configuration selects and the acquisition layer calls.

    Two members only, so any tool can substitute, not just one shaped like the old.
    """

    name: str

    def acquire(self, requests: Iterable[TrackRequest]) -> InvocationResult:
        """Acquire every requested track, reporting per the contract."""


class BaseAdapter:
    """Shared adapter plumbing: settings ownership and the delegation to the loop.

    NOT a dataclass, since a field would overwrite each adapter's class ``name``
    with the empty base value.
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
        #: An injected source replaces the wrapped tool and NOTHING else, so a fake
        #: source still tests the adapter.
        self._injected = source

    def _session_scope(self) -> AbstractContextManager[object]:
        """The credential lifetime for one invocation; a no-op by default."""
        return nullcontext(None)

    def _source(self, scope: object) -> TrackSource:  # pragma: no cover - overridden
        raise NotImplementedError

    def _alternatives(self) -> tuple[str, ...]:
        """Names to offer on failure, resolved at CALL time so a broken import works."""
        from cratekit.acquire import alternatives_to  # noqa: PLC0415 - see docstring

        return alternatives_to(self.name)

    def acquire(
        self,
        requests: Iterable[TrackRequest],
        *,
        sleep: Callable[[float], None] = time.sleep,
    ) -> InvocationResult:
        """Run one acquisition, with the credential live only for its duration.

        Adapter failures are caught HERE because both can occur before a source
        exists, and a caller always gets a result rather than an exception.
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
    "DEFECT_ERRORS", "FAILED_INVOCATIONS", "TRANSIENT_MARKERS", "AcquisitionAdapter",
    "AdapterAuthFailed", "AdapterBroken", "AdapterError", "AdapterSettings", "BaseAdapter",
    "IncompleteHandling", "InvocationOutcome", "InvocationResult", "LosslessPolicy",
    "LosslessRefused", "NoFileLanded", "Offer", "PolicyDecision", "Remedy", "TrackOutcome",
    "TrackRequest", "TrackResult", "TrackSource", "UnknownAdapter", "acquire_one",
    "acquire_with_source", "classify_unavailable", "raise_if_defect", "decide_lossless", "dispatch",
    "dispatch_invocation", "verify_applied",
]
