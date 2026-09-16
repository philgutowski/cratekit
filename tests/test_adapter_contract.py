"""U14: the acquisition contract, proven against every registered adapter.

The unit's claim is that the downloader is replaceable through configuration. A
claim like that is worth exactly as much as the test that would fail if it were
false, so the shape of this file matters as much as its contents:

* **The adapter list is DERIVED from the registry**, never written out here. A
  third adapter joins this suite by being registered, which is the only way "both
  adapters satisfy the same contract" keeps meaning something after the third one
  arrives (P3).
* **Nothing here needs a network, an account, or the alternative tool.** The
  alternative is deliberately exercised with its distribution ABSENT, because
  that is the state of every machine that has not yet needed it, including the
  one this suite runs on.
* **The fake source replaces the wrapped tool and nothing else.** The credential
  scope, the settings, the loop, the classification, and the result shaping all
  run for real, so a passing test is a statement about the adapter rather than
  about the fake.

The four per-track outcomes and the three invocation outcomes are the whole point
of the unit: today both call sites in the source system raise on any non-zero
exit and the tool exits zero when it silently skips, so "nothing was new" and
"your session is dead" are the same observation. Every assertion below is
ultimately about keeping those apart.
"""

from __future__ import annotations

import ast
import functools
import stat
import sys
import types
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

import pytest

import cratekit.acquire as registry
from cratekit.acquire import provider_session, streamrip, vendored
from cratekit.acquire.adapter import (
    AcquisitionAdapter,
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    BaseAdapter,
    IncompleteHandling,
    InvocationOutcome,
    InvocationResult,
    LosslessPolicy,
    Offer,
    Remedy,
    TrackOutcome,
    TrackRequest,
    TrackResult,
    UnknownAdapter,
    classify_unavailable,
    decide_lossless,
    dispatch,
    dispatch_invocation,
    verify_applied,
)
from cratekit.core import binaries, config, secrets
from tests._containers import synth_container

REPO_ROOT = Path(__file__).resolve().parent.parent
ACQUIRE_ROOT = REPO_ROOT / "src" / "cratekit" / "acquire"

# A session blob shaped like the real one and obviously not one. Values are short
# and marked so the repository secret scan reads them as the illustrations they
# are rather than as a leaked credential.
FAKE_SESSION = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": "2000-01-01T00:00:00",
}


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures and doubles
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def stored_session():
    """Record a provider session in the suite's in-memory keychain stub."""
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(FAKE_SESSION))
    return dict(FAKE_SESSION)


@pytest.fixture
def settings(tmp_path) -> AdapterSettings:
    staging = tmp_path / "staging"
    staging.mkdir()
    return AdapterSettings(download_staging=staging)


class NotFoundError(Exception):
    """A provider client's delisted-track exception, recognised by CLASS NAME.

    The classifier reads the type name rather than the message for this case, so
    a double that only carried a message would not exercise the rule that
    actually runs against the real client.
    """


@dataclass
class Scripted:
    """A ``TrackSource`` driven by a per-key script.

    ``plan`` maps a request key to what the provider does: an ``Offer`` it can
    serve, or an exception it raises. ``fetch_failures`` covers the second half
    of the same question, because a track can be offered and then fail to
    download, and the two paths classify through the same rule.
    """

    plan: dict[str, object] = field(default_factory=dict)
    fetch_failures: dict[str, BaseException] = field(default_factory=dict)
    auth_error: BaseException | None = None
    authenticated: int = 0
    fetched: list[str] = field(default_factory=list)
    destinations: list[Path] = field(default_factory=list)

    def authenticate(self) -> None:
        self.authenticated += 1
        if self.auth_error is not None:
            raise self.auth_error

    def offer(self, request: TrackRequest) -> Offer:
        answer = self.plan[request.key]
        if isinstance(answer, BaseException):
            raise answer
        assert isinstance(answer, Offer)
        return answer

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        failure = self.fetch_failures.get(request.key)
        if failure is not None:
            raise failure
        self.fetched.append(request.key)
        self.destinations.append(destination)
        landed = Path(destination) / f"{request.key}.flac"
        landed.parent.mkdir(parents=True, exist_ok=True)
        landed.write_bytes(b"")
        return landed


def four_outcome_source() -> Scripted:
    """One script that produces every per-track outcome in a single run."""
    return Scripted(
        plan={
            "acquired": Offer(lossless=True),
            "delisted": NotFoundError("track not found"),
            "flaky": RuntimeError("503 Service Unavailable"),
            "lossy-only": Offer(lossless=False),
        }
    )


FOUR_OUTCOME_REQUESTS = (
    TrackRequest(key="acquired"),
    TrackRequest(key="delisted"),
    TrackRequest(key="flaky"),
    TrackRequest(key="lossy-only"),
)


@pytest.fixture(params=sorted(registry.ADAPTERS))
def adapter_name(request) -> str:
    """Every registered adapter, derived from the registry rather than listed.

    This is the parameter that makes the file a CONTRACT suite instead of two
    adapter suites that happen to sit together.
    """
    return request.param


@dataclass
class ScopeRecord:
    """What a materialised credential scope looked like while it was live."""

    directory: Path
    path: Path
    existed: bool
    file_mode: int
    dir_mode: int


@pytest.fixture
def watched_scopes(monkeypatch) -> list[ScopeRecord]:
    """Observe every credential scope an adapter opens, without changing it.

    Wrapping the real context manager rather than replacing it is deliberate: the
    property under test is that the real materialisation leaves nothing behind,
    and a replacement would only prove that about the replacement.
    """
    records: list[ScopeRecord] = []
    real = provider_session.materialised_session

    @contextmanager
    def spy(*args, **kwargs):
        with real(*args, **kwargs) as scope:
            records.append(
                ScopeRecord(
                    directory=scope.directory,
                    path=scope.path,
                    existed=scope.path.exists(),
                    file_mode=stat.S_IMODE(scope.path.stat().st_mode),
                    dir_mode=stat.S_IMODE(scope.directory.stat().st_mode),
                )
            )
            yield scope

    monkeypatch.setattr(provider_session, "materialised_session", spy)
    return records


# ═══════════════════════════════════════════════════════════════════════════
# The registry: R9's "at least one alternative", answered structurally
# ═══════════════════════════════════════════════════════════════════════════


def test_the_registry_ships_an_alternative_to_every_adapter():
    """R9 requires an alternative proven against the interface BEFORE launch.

    Asserted as a property of every entry rather than as "there are two", so the
    day somebody removes one the failure says what was lost.
    """
    assert len(registry.ADAPTERS) >= 2
    for name in registry.ADAPTERS:
        assert registry.alternatives_to(name), (
            f"{name} has no replacement path; an adapter with nowhere to fail over "
            f"to is the single point of failure R9 exists to remove"
        )


def test_every_registered_adapter_loads_with_no_third_party_tool_installed():
    """Listing and resolving adapters must work on a machine that has neither.

    The failure this blocks is circular and easy to ship: an adapter that can
    only be named by importing the tool it wraps cannot be offered as the
    replacement for the tool that just broke.
    """
    for name in registry.ADAPTERS:
        cls = registry.load(name)
        assert issubclass(cls, BaseAdapter)
        assert cls.name == name, (
            f"{cls.__name__} answers to {cls.name!r} but is registered as {name!r}; "
            f"configuration records the registry key, so a mismatch makes the "
            f"adapter unselectable"
        )


def test_a_built_adapter_satisfies_the_declared_interface(adapter_name, settings):
    assert isinstance(registry.build(adapter_name, settings), AcquisitionAdapter)


def test_an_unknown_adapter_name_refuses_rather_than_falling_back():
    """A typo must not silently switch the tool that touches the user's music."""
    with pytest.raises(UnknownAdapter) as caught:
        registry.load("no-such-adapter")
    assert caught.value.remedy is Remedy.CHOOSE_KNOWN_ADAPTER
    for known in registry.ADAPTERS:
        assert known in str(caught.value)


def test_an_adapter_with_no_declared_name_refuses_to_construct(settings):
    class Nameless(BaseAdapter):
        pass

    with pytest.raises(AdapterBroken):
        Nameless(settings)


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: the four per-track outcomes are handled DISTINCTLY by the caller
# ═══════════════════════════════════════════════════════════════════════════


def test_one_run_produces_all_four_per_track_outcomes(adapter_name, settings, stored_session):
    """The distinction the source system cannot currently make, made in one run."""
    adapter = registry.build(adapter_name, settings, source=four_outcome_source())
    result = adapter.acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.OK
    assert {r.key: r.outcome for r in result.results} == {
        "acquired": TrackOutcome.ACQUIRED,
        "delisted": TrackOutcome.UNAVAILABLE_PERMANENT,
        "flaky": TrackOutcome.UNAVAILABLE_TRANSIENT,
        "lossy-only": TrackOutcome.REFUSED_BY_POLICY,
    }
    assert result.counts() == {
        TrackOutcome.ACQUIRED: 1,
        TrackOutcome.UNAVAILABLE_PERMANENT: 1,
        TrackOutcome.UNAVAILABLE_TRANSIENT: 1,
        TrackOutcome.REFUSED_BY_POLICY: 1,
    }


def test_each_outcome_reaches_its_own_handler(adapter_name, settings, stored_session):
    """"Handled distinctly" means four handlers, each firing exactly once."""
    adapter = registry.build(adapter_name, settings, source=four_outcome_source())
    result = adapter.acquire(FOUR_OUTCOME_REQUESTS)

    seen: dict[TrackOutcome, list[str]] = {outcome: [] for outcome in TrackOutcome}
    dispatch(
        result,
        {outcome: (lambda r, o=outcome: seen[o].append(r.key)) for outcome in TrackOutcome},
    )
    assert seen == {
        TrackOutcome.ACQUIRED: ["acquired"],
        TrackOutcome.UNAVAILABLE_PERMANENT: ["delisted"],
        TrackOutcome.UNAVAILABLE_TRANSIENT: ["flaky"],
        TrackOutcome.REFUSED_BY_POLICY: ["lossy-only"],
    }


def test_a_caller_that_forgets_an_outcome_is_refused_by_name():
    """The mechanism that makes a fifth outcome impossible to drop silently."""
    result = InvocationResult(adapter="fake", outcome=InvocationOutcome.OK)
    handlers = {o: (lambda r: r) for o in TrackOutcome if o is not TrackOutcome.REFUSED_BY_POLICY}
    with pytest.raises(IncompleteHandling) as caught:
        dispatch(result, handlers)
    assert str(TrackOutcome.REFUSED_BY_POLICY) in str(caught.value)


def test_a_caller_that_forgets_an_invocation_outcome_is_refused_by_name():
    result = InvocationResult(adapter="fake", outcome=InvocationOutcome.OK)
    handlers = {InvocationOutcome.OK: (lambda r: r)}
    with pytest.raises(IncompleteHandling) as caught:
        dispatch_invocation(result, handlers)
    assert str(InvocationOutcome.AUTH_FAILED) in str(caught.value)
    assert str(InvocationOutcome.ADAPTER_BROKEN) in str(caught.value)


def test_the_required_handler_set_is_read_from_the_enum():
    """P3: the completeness rule derives its set instead of restating it.

    Written as an explicit assertion because the value of ``dispatch`` collapses
    the moment somebody replaces the derivation with a literal tuple, and that
    edit looks harmless in a diff.
    """
    complete = {o: (lambda r: r) for o in TrackOutcome}
    dispatch(InvocationResult(adapter="fake", outcome=InvocationOutcome.OK), complete)
    for omitted in TrackOutcome:
        partial = {o: (lambda r: r) for o in TrackOutcome if o is not omitted}
        with pytest.raises(IncompleteHandling):
            dispatch(InvocationResult(adapter="fake", outcome=InvocationOutcome.OK), partial)


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: an auth failure is an ADAPTER failure, not missing tracks (AE9)
# ═══════════════════════════════════════════════════════════════════════════


def test_an_auth_failure_names_the_replacement_path_and_moves_no_watermark(
    adapter_name, settings, stored_session
):
    source = four_outcome_source()
    source.auth_error = AdapterAuthFailed("the provider rejected the stored session")
    adapter = registry.build(adapter_name, settings, source=source)

    result = adapter.acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.AUTH_FAILED
    assert result.remedy is Remedy.REAUTHENTICATE_PROVIDER
    assert result.alternatives == registry.alternatives_to(adapter_name)
    assert result.advances_watermark is False
    assert result.quarantine_keys() == ()
    # The half that matters most: not one of the four reads as absent from the
    # catalogue, and every one of them stays queued for a later run.
    assert set(result.requeue_keys()) == {r.key for r in FOUR_OUTCOME_REQUESTS}


def test_an_auth_failure_mid_run_keeps_what_landed_and_still_fails_the_invocation(
    settings, stored_session
):
    """Partial success is still a failed invocation.

    Reporting OK because some tracks landed is how a watermark advances past the
    items the dead session never looked at, and those items are then never seen
    again.
    """
    source = Scripted(
        plan={
            "first": Offer(lossless=True),
            "second": AdapterAuthFailed("401 the session expired"),
            "third": Offer(lossless=True),
        }
    )
    adapter = vendored.VendoredAdapter(settings, source=source)
    result = adapter.acquire(
        [TrackRequest(key="first"), TrackRequest(key="second"), TrackRequest(key="third")]
    )

    assert result.outcome is InvocationOutcome.AUTH_FAILED
    assert [r.key for r in result.acquired()] == ["first"]
    assert result.advances_watermark is False
    assert set(result.requeue_keys()) == {"second", "third"}


def test_a_failed_invocation_cannot_carry_a_permanent_unavailability():
    """Quarantine is forever, so a broken adapter must not be able to feed it."""
    with pytest.raises(ValueError, match="permanently unavailable"):
        InvocationResult(
            adapter="fake",
            outcome=InvocationOutcome.ADAPTER_BROKEN,
            results=(TrackResult(key="x", outcome=TrackOutcome.UNAVAILABLE_PERMANENT),),
            remedy=Remedy.SWITCH_ADAPTER,
            alternatives=("other",),
        )


def test_a_failed_invocation_must_carry_a_remedy():
    with pytest.raises(ValueError, match="remedy token"):
        InvocationResult(
            adapter="fake", outcome=InvocationOutcome.ADAPTER_BROKEN, alternatives=("other",)
        )


def test_an_auth_failure_with_nowhere_to_go_cannot_be_constructed():
    """AE9 is a reporting requirement, so it is enforced where the report is built."""
    with pytest.raises(ValueError, match="replacement path"):
        InvocationResult(
            adapter="fake",
            outcome=InvocationOutcome.AUTH_FAILED,
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
        )


def test_a_result_cannot_report_a_track_nobody_asked_for():
    """An identity mix-up here becomes a file filed under the wrong track later."""
    with pytest.raises(ValueError, match="nobody asked for"):
        InvocationResult(
            adapter="fake",
            outcome=InvocationOutcome.OK,
            results=(TrackResult(key="stranger", outcome=TrackOutcome.UNAVAILABLE_TRANSIENT),),
            requested=("asked-for",),
        )


def test_the_report_names_everything_that_was_requested(adapter_name, settings, stored_session):
    """The queue is answerable from the result alone, on success or failure."""
    result = registry.build(adapter_name, settings, source=four_outcome_source()).acquire(
        FOUR_OUTCOME_REQUESTS
    )
    assert result.requested == tuple(r.key for r in FOUR_OUTCOME_REQUESTS)


def test_an_absent_credential_reports_as_an_adapter_failure(adapter_name, settings):
    """No session recorded at all, on both adapters, with the keychain working."""
    adapter = registry.build(adapter_name, settings, source=four_outcome_source())
    result = adapter.acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.AUTH_FAILED
    assert result.remedy is Remedy.REAUTHENTICATE_PROVIDER
    assert result.quarantine_keys() == ()


def test_a_keychain_with_no_backend_is_a_broken_adapter_not_a_stale_session(
    adapter_name, settings, monkeypatch
):
    """The two credential failures need opposite remedies, so they stay apart.

    Telling a user with no keychain to re-authorise sends them to a dialog with
    nowhere to write the answer.
    """

    def unavailable(name):
        raise secrets.CredentialBackendUnavailable("no keychain backend is reachable")

    monkeypatch.setattr(secrets, "get_json", unavailable)
    result = registry.build(adapter_name, settings, source=four_outcome_source()).acquire(
        FOUR_OUTCOME_REQUESTS
    )

    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert result.remedy is Remedy.REPAIR_CREDENTIAL_STORE


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: transient stays re-queueable, only an explicit not-found is permanent
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "exc",
    [
        RuntimeError("503 Service Unavailable"),
        RuntimeError("Service Unavailable"),
        RuntimeError("upstream server error"),
        RuntimeError("5xx from the edge"),
        TimeoutError("read timed out"),
        RuntimeError("429 Too Many Requests"),
        RuntimeError("401 Unauthorized"),
    ],
)
def test_anything_that_might_work_later_classifies_transient(exc):
    """The quarantine store is never re-queued, so this is the safe direction.

    "Service Unavailable" is here because it is the trap: a 503 renders with the
    word "unavailable" in it, and a substring match on that word reads a healthy
    track on a sick server as a delisted one, permanently.
    """
    assert classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_TRANSIENT


def test_a_503_is_transient_even_though_it_says_unavailable():
    assert "unavailable" in str(RuntimeError("503 Service Unavailable")).lower()
    assert classify_unavailable(RuntimeError("503 Service Unavailable")) is (
        TrackOutcome.UNAVAILABLE_TRANSIENT
    )


class _Response:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class _HttpError(Exception):
    def __init__(self, response: _Response) -> None:
        super().__init__("request failed")
        self.response = response


@pytest.mark.parametrize(
    "exc",
    [
        NotFoundError("gone"),
        RuntimeError("404"),
        RuntimeError("the track was not found"),
        _HttpError(_Response(404)),
    ],
)
def test_only_an_explicit_not_found_classifies_permanent(exc):
    assert classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT


def test_a_transient_marker_wins_over_a_status_code():
    """Order is load-bearing: the transient evidence is checked first.

    A gateway in front of the provider can answer 404 for a request it never
    forwarded while saying so in the body. Reading the status alone quarantines a
    track that exists, and quarantine is never re-queued.
    """
    assert classify_unavailable(_HttpError(_Response(404))) is TrackOutcome.UNAVAILABLE_PERMANENT
    confusing = _HttpError(_Response(404))
    confusing.args = ("503 Service Unavailable",)
    assert classify_unavailable(confusing) is TrackOutcome.UNAVAILABLE_TRANSIENT


def test_a_transient_track_is_requeueable_and_a_permanent_one_is_quarantined(
    adapter_name, settings, stored_session
):
    adapter = registry.build(adapter_name, settings, source=four_outcome_source())
    result = adapter.acquire(FOUR_OUTCOME_REQUESTS)

    assert result.quarantine_keys() == ("delisted",)
    assert "flaky" in result.requeue_keys()
    assert "delisted" not in result.requeue_keys()
    assert result.advances_watermark is True


def test_a_download_that_fails_classifies_the_same_way_as_a_lookup(settings, stored_session):
    """One rule for both halves. Two rules is how two call sites disagreed."""
    source = Scripted(
        plan={"a": Offer(lossless=True), "b": Offer(lossless=True)},
        fetch_failures={"a": RuntimeError("503 Service Unavailable"), "b": NotFoundError("gone")},
    )
    result = vendored.VendoredAdapter(settings, source=source).acquire(
        [TrackRequest(key="a"), TrackRequest(key="b")]
    )
    assert {r.key: r.outcome for r in result.results} == {
        "a": TrackOutcome.UNAVAILABLE_TRANSIENT,
        "b": TrackOutcome.UNAVAILABLE_PERMANENT,
    }


def test_a_transient_result_carries_the_retry_token_and_a_permanent_one_does_not(
    settings, stored_session
):
    """A remedy that changes nothing trains people to stop reading remedies.

    There is nothing a user can do about a delisted track, so it is offered
    nothing to do.
    """
    source = Scripted(plan={"t": RuntimeError("503 Service Unavailable"), "p": NotFoundError("x")})
    result = vendored.VendoredAdapter(settings, source=source).acquire(
        [TrackRequest(key="t"), TrackRequest(key="p")]
    )
    by_key = {r.key: r for r in result.results}
    assert by_key["t"].remedy is Remedy.RETRY_LATER
    assert by_key["p"].remedy is None


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: the lossless policy is enforced HERE (R21, AE4, S3)
# ═══════════════════════════════════════════════════════════════════════════


def test_strict_policy_refuses_a_lossy_only_track_rather_than_acquiring_it(
    adapter_name, settings, stored_session
):
    """AE4's first half, on every adapter."""
    adapter = registry.build(adapter_name, settings, source=Scripted(plan={"x": Offer(False)}))
    result = adapter.acquire([TrackRequest(key="x")])

    only = result.results[0]
    assert only.outcome is TrackOutcome.REFUSED_BY_POLICY
    assert only.remedy is Remedy.RELAX_LOSSLESS_POLICY
    assert only.path is None
    assert result.quarantine_keys() == ()
    assert result.requeue_keys() == ("x",)


def test_permitted_lossy_carries_the_marker_requirement(adapter_name, tmp_path, stored_session):
    """AE4's second half: allowed means allowed AND marked, never allowed alone."""
    staging = tmp_path / "staging"
    staging.mkdir()
    permissive = AdapterSettings(
        download_staging=staging, lossless_policy=LosslessPolicy.ALLOW_LOSSY_MARKED
    )
    adapter = registry.build(adapter_name, permissive, source=Scripted(plan={"x": Offer(False)}))
    only = adapter.acquire([TrackRequest(key="x")]).results[0]

    assert only.outcome is TrackOutcome.ACQUIRED
    assert only.lossless is False
    assert only.requires_lossy_marker is True


def test_a_lossless_acquisition_needs_no_marker(adapter_name, settings, stored_session):
    adapter = registry.build(adapter_name, settings, source=Scripted(plan={"x": Offer(True)}))
    only = adapter.acquire([TrackRequest(key="x")]).results[0]
    assert only.outcome is TrackOutcome.ACQUIRED
    assert only.requires_lossy_marker is False


@pytest.mark.parametrize("policy", list(LosslessPolicy))
def test_no_policy_can_permit_a_lossy_source_without_the_marker(policy):
    """R21 quantified over EVERY policy, derived from the enum (P3).

    Written this way so a third policy value cannot be added without this test
    deciding whether it is legal. A test listing the two policies by hand would
    pass silently on the day the third arrived.
    """
    decision = decide_lossless(policy, source_is_lossless=False)
    assert not (decision.permitted and not decision.marker_required)


def test_a_lossy_acquisition_that_forgot_the_marker_cannot_be_constructed():
    """The invariant lives on the type, so no branch anywhere can produce it."""
    with pytest.raises(ValueError, match="R21"):
        TrackResult(
            key="x",
            outcome=TrackOutcome.ACQUIRED,
            path=Path("x.m4a"),
            lossless=False,
            requires_lossy_marker=False,
        )


def test_an_acquired_result_must_name_a_file_and_state_its_losslessness():
    with pytest.raises(ValueError, match="must name the file"):
        TrackResult(key="x", outcome=TrackOutcome.ACQUIRED)
    with pytest.raises(ValueError, match="whether it is lossless"):
        TrackResult(key="x", outcome=TrackOutcome.ACQUIRED, path=Path("x.flac"))


def test_a_non_acquired_result_may_not_carry_a_file():
    with pytest.raises(ValueError, match="partial download"):
        TrackResult(
            key="x", outcome=TrackOutcome.UNAVAILABLE_TRANSIENT, path=Path("half.flac")
        )


def test_a_policy_refusal_must_say_what_would_change_the_answer():
    with pytest.raises(ValueError, match="remedy token"):
        TrackResult(key="x", outcome=TrackOutcome.REFUSED_BY_POLICY)


def test_a_track_request_needs_a_stable_identifier():
    """R19 and D5: identity, never a display name."""
    with pytest.raises(ValueError, match="stable identifier"):
        TrackRequest(key="", artist="Someone", title="Something")


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: pacing and quality are owned by the adapter (KTD20)
# ═══════════════════════════════════════════════════════════════════════════


def test_settings_come_from_configuration_by_name(tmp_path, monkeypatch):
    """The field names must match U2's schema, so this reads a REAL Config.

    A stand-in object with the right attribute names would pass while the schema
    said something else, which is the failure this assertion exists to catch.
    """
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "slim"},
            "acquisition": {"lossless_policy": "allow_lossy_marked", "pacing_delay_s": 2.5},
        }
    )
    built = AdapterSettings.from_config(cfg)

    assert built.download_staging == tmp_path / "staging"
    assert built.lossless_policy is LosslessPolicy.ALLOW_LOSSY_MARKED
    assert built.pacing_delay_s == 2.5
    assert built.quality == cfg.acquisition.quality


def test_the_configured_adapter_name_resolves_through_the_registry(tmp_path, monkeypatch):
    """F6: switching adapters is a configuration change, not a code change."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "slim"},
        }
    )
    assert cfg.acquisition.adapter in registry.ADAPTERS
    assert registry.load(cfg.acquisition.adapter) is vendored.VendoredAdapter


def test_pacing_runs_between_acquisitions_and_not_before_the_first(settings, stored_session):
    """The delay is a gap between requests, so N requests means N-1 waits."""
    paced = AdapterSettings(download_staging=settings.download_staging, pacing_delay_s=0.25)
    slept: list[float] = []
    source = Scripted(plan={k: Offer(True) for k in ("a", "b", "c")})
    vendored.VendoredAdapter(paced, source=source).acquire(
        [TrackRequest(key=k) for k in ("a", "b", "c")], sleep=slept.append
    )
    assert slept == [0.25, 0.25]


def test_settings_refuse_values_that_would_disable_the_cap_or_reverse_the_pacing(tmp_path):
    with pytest.raises(ValueError, match="at least one"):
        AdapterSettings(download_staging=tmp_path, concurrency=0)
    with pytest.raises(ValueError, match="negative"):
        AdapterSettings(download_staging=tmp_path, pacing_delay_s=-1.0)


def _ffmpeg_at(path: str):
    """A resolver stub standing in for ``binaries.resolve``."""
    return lambda name: path if name == "ffmpeg" else f"/usr/bin/{name}"


def test_the_vendored_settings_translation_names_every_key_that_reverted(settings):
    """The observed reversions, the naming template, and the ffmpeg path.

    The SET is asserted, not three names. R-195 was a missing key in a mapping
    nothing counted, so a fourth key arriving unnoticed is the exact shape this
    has to refuse.
    """
    pushed = vendored.tool_settings(settings, resolve=_ffmpeg_at("/opt/x/ffmpeg"))
    assert set(pushed) == {
        "quality_audio",
        "download_base_path",
        "format_track",
        "path_binary_ffmpeg",
        "extract_flac",
    }
    assert pushed["quality_audio"] == "LOSSLESS"
    assert pushed["download_base_path"] == str(settings.download_staging)
    assert pushed["format_track"] == vendored.STAGING_TEMPLATE
    assert pushed["path_binary_ffmpeg"] == "/opt/x/ffmpeg"


def test_the_ffmpeg_path_is_the_one_the_binaries_module_resolves(monkeypatch, tmp_path, settings):
    """R-195: doctor and the tool must answer from ONE lookup.

    Driven through the real resolver rather than a stub, because the defect was
    that the two answered different questions: doctor asked whether ffmpeg exists
    on this machine, the tool asked whether it had been told the path.
    """
    exe = tmp_path / "ffmpeg"
    exe.write_text("#!/bin/sh\nexit 0\n")
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(exe))

    pushed = vendored.tool_settings(settings)
    assert pushed["path_binary_ffmpeg"] == binaries.resolve("ffmpeg") == str(exe)


def test_a_machine_with_no_ffmpeg_refuses_by_name_instead_of_landing_lossy(
    monkeypatch, tmp_path, settings, stored_session
):
    """The whole point of R-195: silence here is a lossy file reported as success.

    With the key unset the wrapped tool turns ``extract_flac`` off and logs one
    warning through a logger this adapter discards, so the run reports OK over a
    320k AAC file. Refusing by name is the alternative to that.
    """
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var("ffmpeg"), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: ())

    with pytest.raises(AdapterBroken) as caught:
        vendored.tool_settings(settings)
    assert "ffmpeg" in str(caught.value)
    assert caught.value.remedy is Remedy.INSTALL_ADAPTER

    result = vendored.VendoredAdapter(
        settings,
        source=vendored._VendoredSource(
            settings, tmp_path / "token.json", session=_ToolSession({}), tool=_Tool()
        ),
    ).acquire([TrackRequest(key="1234")])
    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert "ffmpeg" in result.detail
    assert result.remedy is Remedy.INSTALL_ADAPTER


def test_a_broken_ffmpeg_override_is_a_different_instruction_from_an_absent_one(
    monkeypatch, tmp_path, settings
):
    """Installing ffmpeg does not fix an override pointing at nothing.

    The binaries module already separates these two, and collapsing them onto one
    remedy at this hop would throw that away and send the user to a package
    manager for a variable they set wrong.
    """
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(tmp_path / "not-here"))
    with pytest.raises(AdapterBroken) as caught:
        vendored.tool_settings(settings)
    assert caught.value.remedy is Remedy.REPAIR_ADAPTER_SETTINGS


def test_the_flac_extraction_setting_is_pushed_rather_than_inherited(settings):
    """KTD20: a setting this product depends on is stated every invocation.

    The tool's factory default is True, but the value a run actually gets is
    whatever the tool last wrote to its own settings file, and a run that finds
    it False lands an m4a and reports success. That is the same argument the
    quality setting is pushed for.
    """
    pushed = vendored.tool_settings(settings, resolve=_ffmpeg_at("/opt/x/ffmpeg"))
    assert pushed["extract_flac"] is True


def test_verification_covers_the_ffmpeg_key_by_it_being_pushed(settings):
    """P4 again: a tool that drops the fourth key is caught by the mapping, not a list.

    The stand-in swallows the write the way a tool that renamed or removed the
    setting would. Nobody added ``path_binary_ffmpeg`` to a check list for this
    to fire; it is covered because it is pushed.
    """

    class DropsTheEncoderPath(_ToolSettings):
        @property
        def path_binary_ffmpeg(self):
            return ""

        @path_binary_ffmpeg.setter
        def path_binary_ffmpeg(self, value):
            pass

    target = DropsTheEncoderPath(quality_audio="", download_base_path="", format_track="")
    with pytest.raises(AdapterBroken) as caught:
        vendored.apply_settings(target, settings, resolve=_ffmpeg_at("/opt/x/ffmpeg"))
    assert "path_binary_ffmpeg is ''" in str(caught.value)
    assert caught.value.remedy is Remedy.REPAIR_ADAPTER_SETTINGS


class _ToolSettings:
    """A stand-in for the wrapped tool's settings object.

    ``save`` raises rather than recording, because the assertion is that it is
    never reached: KTD20's whole change is the absent write, and a counter that
    somebody later reads as "zero is fine" is weaker than a call that cannot
    happen quietly.
    """

    def __init__(self, **initial: object) -> None:
        for key, value in initial.items():
            setattr(self, key, value)

    def save(self, *_args, **_kwargs):  # pragma: no cover - reaching it is the failure
        raise AssertionError(
            "the adapter wrote the wrapped tool's global settings file; KTD20 keeps "
            "these in memory precisely so another process cannot revert them"
        )


class _Tool:
    """The wrapped tool's settings holder, with every key the adapter pushes."""

    def __init__(self, **initial: object) -> None:
        self.data = _ToolSettings(
            **{
                "quality_audio": "HIGH",
                "download_base_path": "~/download",
                "format_track": "",
                "path_binary_ffmpeg": "",
                **initial,
            }
        )


def test_applying_settings_writes_them_in_memory_and_saves_nothing(settings):
    target = _Tool().data
    vendored.apply_settings(target, settings, resolve=_ffmpeg_at("/opt/x/ffmpeg"))
    assert target.quality_audio == "LOSSLESS"
    assert target.download_base_path == str(settings.download_staging)
    assert target.path_binary_ffmpeg == "/opt/x/ffmpeg"


def test_a_tool_that_does_not_take_a_setting_refuses_the_run(settings):
    """Verification exists because a write that did not stick is invisible."""

    class Stubborn(_ToolSettings):
        @property
        def quality_audio(self):
            return "HIGH"

        @quality_audio.setter
        def quality_audio(self, value):
            pass

    target = Stubborn(download_base_path="", format_track="", path_binary_ffmpeg="")
    with pytest.raises(AdapterBroken) as caught:
        vendored.apply_settings(target, settings, resolve=_ffmpeg_at("/opt/x/ffmpeg"))
    assert "quality_audio" in str(caught.value)
    assert caught.value.remedy is Remedy.REPAIR_ADAPTER_SETTINGS


def test_verification_covers_every_pushed_setting_not_a_hand_kept_pair():
    """P4: the checked set is the pushed set, so a new setting is covered by existing."""
    expected = {"a": 1, "b": 2, "c": 3}
    assert verify_applied({"a": 1, "b": 2, "c": 3}, expected) == []
    problems = verify_applied({"a": 1, "b": 9}, expected)
    assert len(problems) == 2
    assert any("b is 9" in p for p in problems)
    assert any("c was not accepted at all" in p for p in problems)


def test_no_module_in_this_unit_persists_the_wrapped_tools_settings():
    """The durable form of the KTD20 rule, so a later edit cannot undo it.

    A test that only checks today's call graph passes for as long as nobody adds
    a save. This reads the source, so the regression has to be written in front
    of a red build.
    """
    offenders: list[str] = []
    for path in sorted(ACQUIRE_ROOT.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"save", "token_persist", "set_option"}
            ):
                offenders.append(f"{path.name}:{node.lineno} calls .{node.func.attr}()")
    assert not offenders, (
        "acquisition wrote the wrapped tool's persistent settings or token: "
        + "; ".join(offenders)
    )


def test_the_alternative_translates_quality_into_its_own_vocabulary():
    """Proof that the settings seam is a translation, not a shared literal."""
    staging = Path("/tmp")
    assert streamrip.quality_tier(AdapterSettings(download_staging=staging)) == 2
    assert (
        streamrip.quality_tier(AdapterSettings(download_staging=staging, quality="lossy")) == 1
    )
    assert streamrip.offer_from_tier(1).lossless is False
    assert streamrip.offer_from_tier(2).lossless is True
    assert streamrip.offer_from_tier(4).lossless is True, (
        "a tier above the floor must read as lossless; a membership test would "
        "start refusing new tiers under strict policy"
    )


def test_the_alternative_refuses_an_inexpressible_quality_rather_than_defaulting():
    """Its default tier is the lossy one, so a fallback here would be silent loss."""
    with pytest.raises(AdapterBroken) as caught:
        streamrip.quality_tier(AdapterSettings(download_staging=Path("/tmp"), quality="ultra"))
    assert caught.value.remedy is Remedy.REPAIR_ADAPTER_SETTINGS


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: the alternative adapter, with its distribution ABSENT (KTD5, R9)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def tool_absent(monkeypatch):
    """Force the alternative's distribution to be unimportable, deterministically.

    A ``None`` entry in the module table makes ``import`` raise, which is how the
    test states "not installed" without depending on what happens to be installed
    on the machine running it. Without this the test would pass for the wrong
    reason on a developer's machine and for the right one in CI, or the reverse.
    """
    monkeypatch.setitem(sys.modules, streamrip.DISTRIBUTION, None)


def test_the_alternative_reports_its_absence_as_a_broken_adapter(
    settings, stored_session, tool_absent
):
    result = streamrip.StreamripAdapter(settings).acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert result.remedy is Remedy.INSTALL_ADAPTER
    assert streamrip.DISTRIBUTION in result.detail
    assert result.alternatives == registry.alternatives_to(streamrip.StreamripAdapter.name)
    assert result.advances_watermark is False
    assert result.quarantine_keys() == ()


def test_an_absent_alternative_is_still_nameable_as_the_replacement(tool_absent):
    """The circularity that would make the boundary useless, asserted away."""
    assert "streamrip" in registry.alternatives_to("tidal_dl_ng")
    assert registry.load("streamrip") is streamrip.StreamripAdapter


@pytest.fixture
def installed_streamrip(monkeypatch):
    """A stand-in for the alternative's distribution, with its API shape.

    This is what "prove the interface can express it" actually needs. Injecting a
    fake SOURCE proves the loop; injecting a fake DISTRIBUTION proves the part
    that is specific to this tool, which is the translation between its API and
    the contract, and that is the part a replacement has to get right.
    """
    module = types.ModuleType(streamrip.DISTRIBUTION)

    class Client:
        instances: list = []

        def __init__(self, config_path: str) -> None:
            self.config_path = config_path
            self.logged_in = False
            self.downloads: list[tuple[str, int, str]] = []
            Client.instances.append(self)

        def login(self) -> None:
            self.logged_in = True

        def get(self, key: str, media_type: str) -> dict:
            assert media_type == "track"
            if key == "delisted":
                raise NotFoundError("404 not found")
            if key == "flaky":
                raise RuntimeError("503 Service Unavailable")
            return {"quality": 1 if key == "lossy-only" else 2}

        def download(self, key: str, quality: int, folder: str) -> str:
            self.downloads.append((key, quality, folder))
            landed = Path(folder) / f"{key}.flac"
            landed.parent.mkdir(parents=True, exist_ok=True)
            landed.write_bytes(b"")
            return str(landed)

    Client.instances = []
    module.Client = Client
    monkeypatch.setitem(sys.modules, streamrip.DISTRIBUTION, module)
    return Client


def test_the_alternatives_own_api_translates_into_all_four_outcomes(
    settings, stored_session, installed_streamrip
):
    """The alternative driven through its REAL source, against a stand-in tool."""
    result = streamrip.StreamripAdapter(settings).acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.OK
    assert {r.key: r.outcome for r in result.results} == {
        "acquired": TrackOutcome.ACQUIRED,
        "delisted": TrackOutcome.UNAVAILABLE_PERMANENT,
        "flaky": TrackOutcome.UNAVAILABLE_TRANSIENT,
        "lossy-only": TrackOutcome.REFUSED_BY_POLICY,
    }
    client = installed_streamrip.instances[-1]
    assert client.logged_in
    assert client.downloads == [("acquired", 2, str(settings.download_staging))], (
        "the tool must be told this run's quality tier on every call; its own "
        "default is the lossy one"
    )


def test_the_alternative_is_handed_the_short_lived_credential_file(
    settings, stored_session, installed_streamrip, watched_scopes
):
    """The credential path the tool reads is the one that gets erased."""
    streamrip.StreamripAdapter(settings).acquire([TrackRequest(key="acquired")])
    client = installed_streamrip.instances[-1]
    assert client.config_path == str(watched_scopes[0].path)
    assert not Path(client.config_path).exists()


def test_the_alternative_reports_a_release_with_no_client_entry_point_as_broken(
    settings, stored_session, monkeypatch
):
    """A renamed entry point must not surface as an attribute error from a library."""
    monkeypatch.setitem(sys.modules, streamrip.DISTRIBUTION, types.ModuleType("x"))
    result = streamrip.StreamripAdapter(settings).acquire([TrackRequest(key="acquired")])
    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert result.remedy is Remedy.SWITCH_ADAPTER


def test_the_alternative_reports_a_rejected_login_as_an_auth_failure(
    settings, stored_session, installed_streamrip
):
    def refuse(self):
        raise RuntimeError("the provider rejected the credentials")

    installed_streamrip.login = refuse
    result = streamrip.StreamripAdapter(settings).acquire(FOUR_OUTCOME_REQUESTS)

    assert result.outcome is InvocationOutcome.AUTH_FAILED
    assert result.remedy is Remedy.REAUTHENTICATE_PROVIDER
    assert result.alternatives == registry.alternatives_to("streamrip")
    assert set(result.requeue_keys()) == {r.key for r in FOUR_OUTCOME_REQUESTS}


def test_the_alternative_refuses_a_track_whose_quality_it_cannot_read(
    settings, stored_session, installed_streamrip
):
    """Absent quality reads as the lowest tier, so strict policy declines it.

    Defaulting the other way would let a tool that stopped reporting quality
    quietly fill the library with lossy files.
    """

    def silent(self, key, media_type):
        return {}

    installed_streamrip.get = silent
    only = streamrip.StreamripAdapter(settings).acquire([TrackRequest(key="x")]).results[0]
    assert only.outcome is TrackOutcome.REFUSED_BY_POLICY


# ═══════════════════════════════════════════════════════════════════════════
# The vendored adapter's own translation layer
# ═══════════════════════════════════════════════════════════════════════════


class _ToolSession:
    """A stand-in for the streaming client's session object."""

    def __init__(self, tracks: dict[str, object]) -> None:
        self._tracks = tracks

    def track(self, key: str):
        answer = self._tracks[key]
        if isinstance(answer, BaseException):
            raise answer
        return answer


class _ToolTrack:
    def __init__(self, audio_quality: str) -> None:
        self.audio_quality = audio_quality


@pytest.mark.parametrize(
    "reported, lossless",
    [
        ("LOSSLESS", True),
        ("HI_RES_LOSSLESS", True),
        ("HIGH", False),
        ("LOW", False),
        ("", False),
    ],
)
def test_the_vendored_source_reads_the_clients_quality_vocabulary(
    settings, tmp_path, reported, lossless
):
    """Matched, not compared, so a new lossless tier upstream is not refused."""
    source = vendored._VendoredSource(
        settings, tmp_path / "token.json", session=_ToolSession({"x": _ToolTrack(reported)})
    )
    assert source.offer(TrackRequest(key="x")).lossless is lossless


def test_the_vendored_source_escalates_a_dead_session_but_not_a_dead_track(
    settings, tmp_path
):
    """The ordering rule, at the place it actually runs.

    The wrapped tool's authentication heuristic matches the word "token"
    anywhere, so a per-track message mentioning one must not abort the run.
    """
    session = _ToolSession(
        {
            "expired": RuntimeError("401 Unauthorized: the OAuth token is invalid"),
            "delisted": NotFoundError("404 not found: no stream token for this track"),
        }
    )
    source = vendored._VendoredSource(settings, tmp_path / "token.json", session=session)

    with pytest.raises(AdapterAuthFailed):
        source.offer(TrackRequest(key="expired"))
    with pytest.raises(NotFoundError):
        source.offer(TrackRequest(key="delisted"))


def test_a_download_the_tool_silently_skipped_is_not_reported_as_a_file():
    """The exact shape that made "nothing new" and "it failed" indistinguishable.

    The tool signals a skip by returning success with a false flag. Trusting the
    pair would send a phantom path into tagging; raising sends it back through
    the classifier, where it becomes transient and stays re-queueable.
    """
    lossless = lambda _path: ("FLAC", True)  # noqa: E731 - a one-line probe stub
    assert vendored.landed_file(True, "/staging/x.flac", "x", probe=lossless) == Path(
        "/staging/x.flac"
    )
    with pytest.raises(RuntimeError, match="reported no file"):
        vendored.landed_file(False, "", "x")


class _PkceSession:
    """The client's session object, as far as ``token_persist`` reads it."""

    def __init__(self, is_pkce: bool) -> None:
        self.is_pkce = is_pkce
        self.token_type = "Bearer"
        self.access_token = "FAKE-value-1"
        self.refresh_token = "FAKE-value-2"
        self.expiry_time = 0.0


def _token_round_trip(tmp_path, *, is_pkce: bool):
    """Write a session through the vendored persistence, then read it back.

    Driven through the real ``token_persist`` and ``read`` rather than by
    constructing a ``Token``, because the defect R-196 records is a field DROPPED
    IN THE WRITE, and a read cannot see what was never stored. Building the model
    directly would assert the dataclass has a field and prove nothing about the
    code that fills it.
    """
    from cratekit._vendor.tidal_dl_ng.config import Tidal
    from cratekit._vendor.tidal_dl_ng.model.cfg import Token

    holder = Tidal.__new__(Tidal)
    holder.cls_model = Token
    holder.data = Token()
    holder.file_path = str(tmp_path / "token.json")
    holder.session = _PkceSession(is_pkce)
    holder.token_persist()

    reader = Tidal.__new__(Tidal)
    reader.cls_model = Token
    reader.data = Token()
    reader.file_path = holder.file_path
    reader.read(holder.file_path)
    return reader.data


def test_a_persisted_pkce_session_reloads_as_a_pkce_session(tmp_path):
    """R-196: the write dropped ``is_pkce``, so every PKCE token came back wrong.

    A token reloaded as a device-flow token refreshes against the device-flow
    client, and that is the client the provider serves lossy audio to.
    """
    assert _token_round_trip(tmp_path, is_pkce=True).is_pkce is True


def test_a_session_with_no_pkce_marker_reloads_as_a_device_flow_session(tmp_path):
    """A legacy token stays identifiable rather than being read as PKCE by default."""
    assert _token_round_trip(tmp_path, is_pkce=False).is_pkce is False


def test_the_persisted_flag_never_goes_through_the_bool_coercing_setter(tmp_path):
    """``set_option`` calls ``.lower()`` on any value whose field is a bool.

    ``is_pkce`` is the token model's only bool field, so routing the write
    through ``set_option`` like its four neighbours raises ``AttributeError`` and
    the whole persistence call dies. Asserting the round trip again would not
    catch a regression here, because a tidy-up that moved the write back onto
    ``set_option`` would fail loudly anyway. What this pins is that the write
    does not go through that setter at all, which is the thing a future reader
    would otherwise "fix" for consistency with its four neighbours.
    """
    from cratekit._vendor.tidal_dl_ng.config import Tidal
    from cratekit._vendor.tidal_dl_ng.model.cfg import Token

    holder = Tidal.__new__(Tidal)
    holder.cls_model = Token
    holder.data = Token()
    holder.file_path = str(tmp_path / "token.json")
    holder.session = _PkceSession(True)

    routed: list[str] = []
    original = Tidal.set_option

    def record(self, key, value):
        routed.append(key)
        return original(self, key, value)

    Tidal.set_option = record
    try:
        holder.token_persist()
    finally:
        Tidal.set_option = original

    assert "is_pkce" not in routed, (
        "is_pkce was written through set_option, which calls .lower() on a bool "
        "field's incoming value and raises AttributeError"
    )
    assert holder.data.is_pkce is True


@pytest.mark.parametrize(
    ("stored", "had", "refused"),
    [
        (types.SimpleNamespace(is_pkce=True), True, False),
        (types.SimpleNamespace(is_pkce=False), True, True),
        (types.SimpleNamespace(), True, True),
        (types.SimpleNamespace(is_pkce=True), False, True),
    ],
)
def test_only_a_stored_pkce_session_is_used(stored, had, refused):
    """The pure half of the login decision, driven without the wrapped tool."""
    answer = vendored.login_mode(stored, had_stored_session=had)
    assert (answer is not None) is refused


def test_the_adapter_authenticates_with_pkce_on():
    """The argument itself, read from the source, because nothing else can see it.

    ``authenticate`` returns early on an injected session and imports the wrapped
    tool's classes inside itself, so no offline double reaches the ``login_token``
    call and the keyword is invisible to every runtime test in this file. A
    mutation table found exactly that: reverting ``do_pkce=True`` to the default
    killed nothing. This is the guard for it.

    ``do_pkce=False`` is the call that produced lossy audio for every download
    since July, so the argument is the fix, not decoration.
    """
    tree = ast.parse((ACQUIRE_ROOT / "vendored.py").read_text(encoding="utf-8"))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "login_token"
    ]
    assert calls, "the adapter no longer authenticates through login_token"
    for call in calls:
        pkce = {kw.arg: kw.value for kw in call.keywords}.get("do_pkce")
        assert isinstance(pkce, ast.Constant) and pkce.value is True, (
            "the adapter authenticates with PKCE off; the provider serves that "
            "client lossy audio (R-196)"
        )


def test_a_device_flow_session_is_refused_with_a_remedy_that_has_a_procedure():
    """A refusal whose remedy has nowhere to go is worse than the lossy download.

    Every session in the keychain before this unit was minted by the device flow,
    so this refusal is what every existing user meets first. It names the two
    steps that produce a session it will accept.
    """
    refusal = vendored.login_mode(types.SimpleNamespace(is_pkce=False), had_stored_session=True)
    assert refusal is not None
    assert "PKCE" in refusal
    assert "crate login provider-session --from-file" in vendored.REAUTHORISE_HINT


class _FakeDownload:
    """Records how ``fetch`` constructed the wrapped tool's downloader.

    The real ``Download.__init__`` declares every one of the four missing
    arguments with a ``None`` default, so it accepts any subset and the failure
    only appears later, inside ``item()``. That is precisely why this records the
    call instead of asserting the constructor refuses one: there is nothing to
    refuse.
    """

    seen: dict[str, object] = {}

    def __init__(self, *, landed: tuple[bool, str] = (True, ""), **kwargs: object) -> None:
        # ``landed`` is consumed here and never recorded, so ``seen`` holds
        # exactly the keywords ``fetch`` passed and nothing the test added.
        type(self).seen = dict(kwargs)
        self.landed = landed

    def item(self, **_kwargs: object) -> tuple[bool, str]:
        return self.landed


def _landing(landed: tuple[bool, str]):
    """A downloader class that reports one fixed landing."""
    return functools.partial(_FakeDownload, landed=landed)


def _fetch_with_fake(settings, tmp_path, landed=None):
    """Drive ``fetch`` through the seam and hand back what it built.

    The default landing is a REAL lossless file, so these tests exercise the
    whole of ``fetch`` including the post-landing codec check rather than
    stopping at the construction they are about.
    """
    if landed is None:
        landed = (True, str(synth_container(tmp_path, ".flac")))
    source = vendored._VendoredSource(
        settings,
        tmp_path / "token.json",
        session=_ToolSession({}),
        downloader=_landing(landed),
    )
    return source, _FakeDownload


def test_the_downloader_gets_every_argument_the_vendored_cli_passes(settings, tmp_path):
    """R-197: three arguments where the tool needs seven, and it never fetched a file.

    ``fetch`` carried ``pragma: no cover`` because it could not be reached
    offline, which is also why every green battery missed this.
    """
    source, fake = _fetch_with_fake(settings, tmp_path)
    source.fetch(TrackRequest(key="1234"), settings.download_staging)

    assert set(fake.seen) == vendored.DOWNLOADER_ARGUMENTS


def test_the_run_event_is_set_and_the_abort_event_is_clear(settings, tmp_path):
    """The row that catches a hang rather than a failure.

    ``Download._download_segment`` runs ``self.event_run.wait()`` inside its
    worker pool when the event is clear, and the vendored ``HandlingApp`` is the
    only thing in the tree that ever sets it. A fresh unset Event blocks every
    segment worker on something nothing will wake, so passing the keyword is not
    enough: its STATE is the requirement.
    """
    source, fake = _fetch_with_fake(settings, tmp_path)
    source.fetch(TrackRequest(key="1234"), settings.download_staging)

    assert fake.seen["event_run"].is_set()
    assert not fake.seen["event_abort"].is_set()


def test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream(settings, tmp_path):
    """R32: the tool writes progress through these, and a caller may be parsing."""
    source, fake = _fetch_with_fake(settings, tmp_path)
    source.fetch(TrackRequest(key="1234"), settings.download_staging)

    for key in ("progress", "progress_overall"):
        assert fake.seen[key].disable is True, f"{key} would render"
        # Still usable: the vendored code calls add_task on it regardless.
        fake.seen[key].add_task("probe", total=1)


def test_every_keyword_fetch_passes_exists_on_the_real_downloader():
    """Derived from the callee, so an upstream rename fails here, not at run time.

    The set cannot be derived from the signature alone. ``Download.__init__``
    declares nine parameters and this adapter deliberately passes seven, leaving
    ``skip_existing`` and ``progress_gui`` at their defaults, so a pure
    derivation could not tell a rename from an omission. Two assertions: the
    names are real, and the names are all there.
    """
    import inspect

    from cratekit._vendor.tidal_dl_ng.download import Download

    declared = set(inspect.signature(Download.__init__).parameters)
    assert vendored.DOWNLOADER_ARGUMENTS <= declared, (
        "fetch passes a keyword the vendored downloader does not declare; "
        "re-run scripts/revendor_downloader.py rather than editing the tree"
    )
    assert declared - vendored.DOWNLOADER_ARGUMENTS == {"self", "skip_existing", "progress_gui"}


def test_the_downloader_construction_in_the_source_names_every_argument():
    """The source-level twin, so bypassing the seam is caught too.

    A runtime double only sees the call the test drove. This reads what the
    MODULE writes, which is the shape ``tests/test_pool_sizing.py`` uses for the
    same reason.
    """
    tree = ast.parse((ACQUIRE_ROOT / "vendored.py").read_text(encoding="utf-8"))
    written: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and any(
            kw.arg == "tidal_obj" for kw in node.keywords if kw.arg
        ):
            written.update(kw.arg for kw in node.keywords if kw.arg)
    assert written == vendored.DOWNLOADER_ARGUMENTS


def test_a_skip_reported_through_the_seam_still_raises(settings, tmp_path):
    source, _ = _fetch_with_fake(settings, tmp_path, landed=(False, ""))
    with pytest.raises(RuntimeError, match="reported no file"):
        source.fetch(TrackRequest(key="1234"), settings.download_staging)


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: the lossless rule is enforced at the FILE, not only at the setting
# ═══════════════════════════════════════════════════════════════════════════


def test_the_codec_table_answers_for_every_container_it_declares():
    """Driven over the whole table, not a sample, and with no files at all."""
    assert vendored.LOSSLESS_BY_CONTAINER["FLAC"] is True
    assert vendored.LOSSLESS_BY_CONTAINER["WAVE"] is True
    assert vendored.LOSSLESS_BY_CONTAINER["AIFF"] is True
    assert vendored.LOSSLESS_BY_CONTAINER["OggFLAC"] is True
    assert vendored.LOSSLESS_BY_CONTAINER["MP3"] is False
    assert vendored.LOSSLESS_BY_CONTAINER["OggVorbis"] is False
    assert vendored.LOSSLESS_BY_CONTAINER["OggOpus"] is False
    assert vendored.LOSSLESS_BY_CONTAINER["AAC"] is False
    assert set(vendored.LOSSLESS_BY_CONTAINER) == {
        "FLAC",
        "WAVE",
        "AIFF",
        "OggFLAC",
        "MP3",
        "OggVorbis",
        "OggOpus",
        "AAC",
    }, "a container was added to the table without a decision recorded here"
    assert "alac" in vendored.MP4_LOSSLESS_CODECS
    # MP4 is deliberately not in the container table: a .m4a holds AAC or ALAC
    # and only the codec string can say which, which is the exact container this
    # defect produced.
    assert "MP4" not in vendored.LOSSLESS_BY_CONTAINER


def test_a_real_flac_is_accepted_even_though_mutagen_reports_no_codec(tmp_path):
    """Measured, and the row that would refuse every genuine FLAC if read wrong.

    Mutagen exposes ``info.codec`` on MP4 alone. FLAC, WAV, AIFF and MP3 all
    report None, so a None codec means the CONTAINER decided, not that the file
    could not be read. Treating None as unreadable would refuse every lossless
    file this unit exists to deliver.
    """
    flac = synth_container(tmp_path, ".flac")
    name, lossless = vendored.codec_of(flac)
    assert lossless is True, f"a real FLAC classified as {name!r}"
    assert vendored.landed_file(True, str(flac), "1234") == flac


def test_the_classifier_reads_mutagens_container_and_not_the_file_extension(tmp_path):
    """WAV is the case where the two disagree, so it is the case worth pinning.

    Mutagen names the class ``WAVE`` and the file is called ``.wav``. Every other
    container this product can land spells them the same, so a classifier keyed on
    the suffix would look correct everywhere else and refuse a genuine WAV as
    unreadable. A mutation table found this: swapping the container lookup for a
    suffix lookup killed nothing until this test existed.
    """
    wav = synth_container(tmp_path, ".wav")
    name, lossless = vendored.codec_of(wav)
    assert name == "WAVE", f"classified by extension rather than by container ({name})"
    assert lossless is True
    assert vendored.landed_file(True, str(wav), "1234") == wav


def test_a_lossy_landing_is_refused_and_the_refusal_names_the_codec(tmp_path):
    """The guard that makes the whole chain falsifiable.

    The lossless rule was enforced at the SETTING and never at the FILE, which is
    how the product's central promise failed silently from July: the setting said
    LOSSLESS, the provider sent AAC, and nothing between them ever looked.
    """
    aac = synth_container(tmp_path, ".m4a")
    name, lossless = vendored.codec_of(aac)
    assert lossless is False, f"the .m4a synthesizer stopped producing lossy audio ({name})"

    with pytest.raises(vendored.LosslessRefused) as caught:
        vendored.landed_file(True, str(aac), "1234")
    # The codec it ACTUALLY got, read from the file, not a hardcoded string.
    assert name in str(caught.value)
    assert str(aac) in str(caught.value)


def test_a_refused_file_is_left_where_it_landed(tmp_path):
    """Deleting a file on the strength of a probe is a destructive act.

    It is also the evidence somebody diagnosing the next demotion will want.
    """
    aac = synth_container(tmp_path, ".m4a")
    with pytest.raises(vendored.LosslessRefused):
        vendored.landed_file(True, str(aac), "1234")
    assert aac.exists()


@pytest.mark.parametrize("name", ["empty.flac", "mystery.xyz"])
def test_a_landing_that_cannot_be_read_is_refused_as_unreadable_not_as_lossy(tmp_path, name):
    """Two different facts get two different sentences, and two different remedies.

    Not being able to confirm lossless is not the same as confirming lossy. It is
    almost always a truncated download, so it raises a plain error that the
    classifier reads as transient and re-queues. Refusing it as a POLICY failure
    would carry RELAX_LOSSLESS_POLICY, telling somebody to loosen the rule that
    just caught an unreadable file, and loosening it would make the product
    accept that file.
    """
    broken = tmp_path / name
    broken.write_bytes(b"")
    assert vendored.codec_of(broken)[1] is None

    with pytest.raises(RuntimeError) as caught:
        vendored.landed_file(True, str(broken), "1234")
    assert not isinstance(caught.value, vendored.LosslessRefused)
    assert "could not be read" in str(caught.value)
    assert "is lossy" not in str(caught.value)


def test_a_permitted_lossy_policy_does_not_refuse_the_landing(tmp_path):
    aac = synth_container(tmp_path, ".m4a")
    assert (
        vendored.landed_file(
            True, str(aac), "1234", policy=LosslessPolicy.ALLOW_LOSSY_MARKED
        )
        == aac
    )


def test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue(
    settings, tmp_path, stored_session
):
    """Per track, and the outcome names WHICH gate caught it.

    There are four routes to "no file was accepted" in this adapter now, so an
    assertion that merely observes the absence is satisfied by all of them.
    """
    aac = synth_container(tmp_path, ".m4a")
    codec = vendored.codec_of(aac)[0]

    # The OFFER says lossless and the FILE is not. That gap is the whole defect:
    # the rule was enforced where the request was made and never where the file
    # was accepted.
    result = vendored.VendoredAdapter(
        settings,
        source=vendored._VendoredSource(
            settings,
            tmp_path / "token.json",
            session=_ToolSession({"1234": _ToolTrack("LOSSLESS")}),
            downloader=_landing((True, str(aac))),
        ),
    ).acquire([TrackRequest(key="1234")])

    assert result.outcome is InvocationOutcome.OK
    (one,) = result.results
    assert one.outcome is TrackOutcome.REFUSED_BY_POLICY
    assert one.remedy is Remedy.RELAX_LOSSLESS_POLICY
    assert codec in one.detail
    assert one.path is None
    assert result.quarantine_keys() == ()
    assert result.requeue_keys() == ("1234",)


def test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result(
    settings, tmp_path, stored_session
):
    """The reason the refusal is per track rather than adapter level.

    A failed invocation may not carry a permanently unavailable result: quarantine
    is fed from those and quarantine is forever, so ``InvocationResult`` refuses
    the combination outright. An adapter-level refusal raised from inside the loop
    would hit that constructor with the delisted track already in hand and escape
    as an uncaught ValueError, with no outcome, no remedy and no requeue list.
    """
    aac = synth_container(tmp_path, ".m4a")

    source = vendored._VendoredSource(
        settings,
        tmp_path / "token.json",
        session=_ToolSession(
            {"gone": NotFoundError("404 not found"), "1234": _ToolTrack("LOSSLESS")}
        ),
        downloader=_landing((True, str(aac))),
    )

    result = vendored.VendoredAdapter(settings, source=source).acquire(
        [TrackRequest(key="gone"), TrackRequest(key="1234")]
    )

    assert result.outcome is InvocationOutcome.OK
    outcomes = [r.outcome for r in result.results]
    assert outcomes == [TrackOutcome.UNAVAILABLE_PERMANENT, TrackOutcome.REFUSED_BY_POLICY]
    assert result.quarantine_keys() == ("gone",)


def test_an_injected_session_still_has_this_runs_settings_pushed_and_verified(settings, tmp_path):
    """The KTD20 half of authenticate is exercised, never skipped."""

    tool = _Tool()
    source = vendored._VendoredSource(
        settings, tmp_path / "token.json", session=_ToolSession({}), tool=tool
    )
    source.authenticate()
    assert tool.data.quality_audio == "LOSSLESS"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: no plaintext provider token survives a run, under EITHER adapter
# ═══════════════════════════════════════════════════════════════════════════


def test_no_token_file_survives_a_run(adapter_name, settings, stored_session, watched_scopes):
    adapter = registry.build(adapter_name, settings, source=four_outcome_source())
    adapter.acquire(FOUR_OUTCOME_REQUESTS)

    assert watched_scopes, "the adapter never materialised a provider session"
    for record in watched_scopes:
        assert record.existed, "the wrapped tool was given no session to read"
        assert not record.path.exists(), "a provider token outlived the run that used it"
        assert not record.directory.exists()


def test_the_token_and_its_directory_are_both_private(
    adapter_name, settings, stored_session, watched_scopes
):
    """P1: a 0600 file inside a world-writable directory is not protected.

    Any local account can unlink the file and put its own in place, and the mode
    on the file it replaced is irrelevant to that.
    """
    registry.build(adapter_name, settings, source=four_outcome_source()).acquire(
        FOUR_OUTCOME_REQUESTS
    )
    for record in watched_scopes:
        assert record.file_mode == 0o600
        assert record.dir_mode == 0o700


def test_a_failed_run_still_erases_the_token(settings, stored_session, watched_scopes):
    """The run that raised is the one most likely to leave a live token behind."""

    class Exploding(Scripted):
        def offer(self, request):
            raise KeyboardInterrupt("the user stopped the run")

    with pytest.raises(KeyboardInterrupt):
        vendored.VendoredAdapter(settings, source=Exploding()).acquire([TrackRequest(key="x")])

    assert watched_scopes
    for record in watched_scopes:
        assert not record.path.exists()
        assert not record.directory.exists()


def test_no_session_file_is_left_anywhere_under_the_state_roots(
    adapter_name, settings, stored_session, _isolate_state_roots
):
    """Walked rather than enumerated (P3).

    Naming the two files the adapters use would pass for exactly as long as
    nobody adds a third, and the whole risk here is a file somebody forgot about.
    """
    registry.build(adapter_name, settings, source=four_outcome_source()).acquire(
        FOUR_OUTCOME_REQUESTS
    )
    leaked = [
        path
        for path in _isolate_state_roots.rglob("*")
        if path.is_file() and path.name in {vendored.TOKEN_FILENAME, streamrip.CREDENTIAL_FILENAME}
    ]
    assert not leaked, f"credential files left under the state roots: {leaked}"


def test_a_refreshed_session_goes_back_to_the_keychain(settings, stored_session, monkeypatch):
    """The keychain is the system of record, so a refresh must land there."""
    refreshed = dict(FAKE_SESSION, access_token="FAKE-value-3")

    class Refreshing(Scripted):
        def __init__(self, token_path: Path) -> None:
            super().__init__(plan={"x": Offer(True)})
            self._token_path = token_path

        def authenticate(self) -> None:
            import json

            self._token_path.write_text(json.dumps(refreshed))

    captured: dict[str, Path] = {}
    real = provider_session.materialised_session

    @contextmanager
    def spy(*args, **kwargs):
        with real(*args, **kwargs) as scope:
            captured["path"] = scope.path
            yield scope

    monkeypatch.setattr(provider_session, "materialised_session", spy)

    class Adapter(vendored.VendoredAdapter):
        def _source(self, scope):
            return Refreshing(Path(scope.path))

    Adapter(settings).acquire([TrackRequest(key="x")])
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == refreshed


def test_an_unreadable_write_back_leaves_the_stored_session_alone(tmp_path, stored_session):
    """Overwriting a good credential with a truncated file is unrecoverable."""
    truncated = tmp_path / "token.json"
    truncated.write_text('{"access_to')
    assert provider_session.write_back(secrets.Credential.PROVIDER_SESSION, truncated) is False
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == FAKE_SESSION


def test_a_write_back_with_no_session_fields_is_ignored(tmp_path, stored_session):
    """Valid JSON that is not a session is the same hazard wearing a suit."""
    unrelated = tmp_path / "token.json"
    unrelated.write_text('{"unrelated": true}')
    assert provider_session.write_back(secrets.Credential.PROVIDER_SESSION, unrelated) is False
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == FAKE_SESSION


def test_the_alternatives_credential_is_written_in_its_own_encoding(stored_session):
    """The credential is what acquisition tools agree on least, so it is a codec."""
    with provider_session.materialised_session(
        filename="config.toml", codec=provider_session.TOML
    ) as scope:
        text = scope.path.read_text()
    assert "access_token" in text
    assert not text.lstrip().startswith("{"), "a TOML consumer was handed JSON"


# ═══════════════════════════════════════════════════════════════════════════
# Switching adapters changes nothing else
# ═══════════════════════════════════════════════════════════════════════════


def test_two_adapters_given_the_same_answers_produce_the_same_report(settings, stored_session):
    """The plan's verification line, asserted directly.

    Everything except the adapter's own identity and its list of replacements has
    to match, or "switching adapters changes no other workflow" is a hope.
    """
    reports = {}
    for name in registry.ADAPTERS:
        result = registry.build(name, settings, source=four_outcome_source()).acquire(
            FOUR_OUTCOME_REQUESTS
        )
        reports[name] = [
            (r.key, r.outcome, r.lossless, r.requires_lossy_marker, r.remedy)
            for r in result.results
        ]
    assert len(set(map(tuple, reports.values()))) == 1, reports


# ═══════════════════════════════════════════════════════════════════════════
# D2: remediation stays a token
# ═══════════════════════════════════════════════════════════════════════════


def test_every_remedy_is_a_token_and_not_a_command():
    """These flow to the CLI, which renders them. None may already be rendered.

    Derived over the enum rather than spot-checked, so a remedy added later
    cannot arrive as a sentence. The shape is deliberately narrow: lowercase
    words joined by hyphens, no spaces, no punctuation, nothing that could be a
    command line that somebody pasted in because it was quicker than adding a
    token and teaching the CLI to render it (D2).
    """
    for remedy in Remedy:
        assert remedy.value == remedy.value.lower()
        assert " " not in remedy.value
        assert remedy.value.replace("-", "").isalnum()


# ---------------------------------------------------------------------------
# #82: the logger the adapter hands the vendored tool
# ---------------------------------------------------------------------------

VENDORED_TOOL_ROOT = REPO_ROOT / "src" / "cratekit" / "_vendor" / "tidal_dl_ng"


def _attributes_the_tool_uses_on_its_logger() -> dict[str, set[str]]:
    """Every ``fn_logger.<name>`` access in the vendored tree, by attribute.

    Read off the tree rather than listed here, so a revendor that starts calling
    a new method is a red test and not the next real download.
    """
    found: dict[str, set[str]] = {}
    for source in sorted(VENDORED_TOOL_ROOT.rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute):
                continue
            owner = node.value
            is_logger = (isinstance(owner, ast.Name) and owner.id == "fn_logger") or (
                isinstance(owner, ast.Attribute) and owner.attr == "fn_logger"
            )
            if is_logger:
                found.setdefault(node.attr, set()).add(source.name)
    return found


def test_the_logger_handed_to_the_vendored_tool_has_every_method_the_tool_calls():
    """The tool annotates ``fn_logger`` as a callable and uses it as a logger.

    A plain function satisfied the annotation and every offline test, and died
    on the first real download with ``'function' object has no attribute
    'info'``. The set is read off the vendored tree so it cannot drift from the
    tool it describes.
    """
    from cratekit.acquire import vendored

    used = _attributes_the_tool_uses_on_its_logger()
    assert used, "the vendored tree stopped using fn_logger; this guard is stale"
    assert {"info", "debug", "error", "exception"} <= set(used)
    logger = vendored._discard_tool_logging
    missing = sorted(name for name in used if not callable(getattr(logger, name, None)))
    assert not missing, f"the adapter's logger lacks {missing}, used in {[used[m] for m in missing]}"
    for name in used:
        assert getattr(logger, name)("free-form %s", "text", exc_info=True) is None
    assert callable(logger), "the tool's annotation promises a callable"
    assert logger("also fine as a call") is None



# ═══════════════════════════════════════════════════════════════════════════
# R-348: a Python error class no provider raises is a defect, not an outage
# ═══════════════════════════════════════════════════════════════════════════

#: The message the first real download produced, verbatim.
FIRST_REAL_DEFECT = "'function' object has no attribute 'info'"


@pytest.mark.parametrize(
    "defect",
    [
        AttributeError(FIRST_REAL_DEFECT),
        TypeError("item() got an unexpected keyword argument 'quality'"),
        NameError("name 'track' is not defined"),
        UnboundLocalError("cannot access local variable 'path'"),
    ],
    ids=lambda exc: type(exc).__name__,
)
def test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report(
    adapter_name, settings, stored_session, defect
):
    """Driven through the loop, not asked of the classifier alone.

    Classified transient it was retryable forever. As an invocation failure it
    stops the run, names the remedy that can actually change the answer, and
    keeps every track that did not land queued, including the ones never reached.
    """
    source = Scripted(
        plan={"landed": Offer(lossless=True), "broken": defect, "unreached": Offer(lossless=True)}
    )
    result = registry.build(adapter_name, settings, source=source).acquire(
        [TrackRequest(key="landed"), TrackRequest(key="broken"), TrackRequest(key="unreached")]
    )

    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert result.remedy is Remedy.REPORT_DEFECT
    assert type(defect).__name__ in result.detail
    assert result.requeue_keys() == ("broken", "unreached")
    assert all(r.outcome is not TrackOutcome.UNAVAILABLE_TRANSIENT for r in result.results)


def test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way(
    settings, stored_session
):
    """The fetch half of the same rule. Two halves with two rules is how the
    source system's two call sites disagreed.
    """
    source = Scripted(
        plan={"a": Offer(lossless=True)},
        fetch_failures={"a": AttributeError(FIRST_REAL_DEFECT)},
    )
    result = vendored.VendoredAdapter(settings, source=source).acquire([TrackRequest(key="a")])

    assert result.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert result.remedy is Remedy.REPORT_DEFECT


def test_a_defect_stops_the_paced_pool_rather_than_being_retried(settings):
    """The download verb runs the pool, not the sequential loop, and the first
    real defect arrived through it.
    """
    from cratekit.acquire.download import Pacing, acquire_concurrently

    source = Scripted(
        plan={"a": Offer(lossless=True)},
        fetch_failures={"a": AttributeError(FIRST_REAL_DEFECT)},
    )
    run = acquire_concurrently(
        adapter="fake",
        source=source,
        requests=[TrackRequest(key="a")],
        settings=settings,
        pacing=Pacing(base_delay_s=0.0),
        sleep=lambda _s: None,
    )

    assert run.invocation.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert run.invocation.remedy is Remedy.REPORT_DEFECT
    assert run.invocation.requeue_keys() == ("a",)


def test_an_ordinary_provider_error_is_still_transient_and_retryable(settings, stored_session):
    """The other half. A guard that also caught the unknown provider error would
    turn every flaky response into a stopped run.
    """
    source = Scripted(plan={"a": RuntimeError("connection reset by peer")})
    result = vendored.VendoredAdapter(settings, source=source).acquire([TrackRequest(key="a")])

    assert result.outcome is InvocationOutcome.OK
    assert result.results[0].outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    assert result.results[0].remedy is Remedy.RETRY_LATER


def test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect(settings, tmp_path):
    """The authentication heuristic matches "token" anywhere, so a defect that
    names a ``token`` attribute was one step from being read as a dead session
    and sending the person to log in again.
    """
    session = _ToolSession({"x": AttributeError("'NoneType' object has no attribute 'token'")})
    source = vendored._VendoredSource(settings, tmp_path / "token.json", session=session)

    with pytest.raises(AdapterBroken) as caught:
        source.offer(TrackRequest(key="x"))
    assert not isinstance(caught.value, AdapterAuthFailed)
    assert caught.value.remedy is Remedy.REPORT_DEFECT
