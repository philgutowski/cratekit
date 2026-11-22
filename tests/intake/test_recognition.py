"""U57: the recognition identifier, driven through fakes. Nothing here spends.

The proof that the implementation is BOUNDED: the call count is known before
the first chunk is carved, a spend refusal is a different cause from a miss,
the credentials are read only after the budget has passed, and every attempt
reaches the ledger whether or not an answer came back. D1 applies: nothing
here names a real key, a real host, or a real track.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path

import pytest

from cratekit.acquire.match import Wanted
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.intake import acrcloud, recognize
from cratekit.intake.acrcloud import Budget, Ledger, Match, Outcome, Request, Response
from cratekit.intake.recognize import Identified

# Fakes


def hit(artist: str, title: str, *, isrc: str = "", score: int = 90, extra_artist: str = "") -> dict:
    """A MATCH answer naming one recording, in the service's own shape."""
    artists = [{"name": artist}] + ([{"name": extra_artist}] if extra_artist else [])
    music = {
        "title": title,
        "artists": artists,
        "album": {"name": "An Album"},
        "external_ids": {"isrc": isrc} if isrc else {},
        "score": score,
    }
    return {"status": {"code": 0, "msg": "Success"}, "metadata": {"music": [music]}}


def miss() -> dict:
    return {"status": {"code": 1001, "msg": "No result"}}


def coded(code: int, msg: str = "") -> dict:
    return {"status": {"code": code, "msg": msg}}


class FakeCarver:
    """Answers a fixed duration and carves the offset into the bytes, so the
    transport can tell which chunk it was handed."""

    def __init__(self, duration_s: float) -> None:
        self.duration_s = duration_s
        self.carved: list[int] = []
        self.measured: list[Path] = []

    def duration(self, source: Path) -> float:
        self.measured.append(source)
        return self.duration_s

    def carve(self, source: Path, offset_s: int, chunk_s: int) -> bytes:
        self.carved.append(offset_s)
        return f"chunk@{offset_s}".encode()


class FakeTransport:
    """Answers each call from a script, in order. An entry may be a payload,
    an exception to raise, or a ``Response`` to return verbatim."""

    def __init__(self, *answers) -> None:
        self.answers = list(answers)
        self.requests: list[Request] = []

    def __call__(self, request: Request) -> Response:
        self.requests.append(request)
        if not self.answers:
            raise AssertionError("the transport was asked more than the script allows")
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        if isinstance(answer, Response):
            return answer
        return Response(status=200, body=json.dumps(answer).encode())


class MemoryLedger:
    """The ledger's two calls, in memory, for a pass of hundreds of calls that
    is about the parts and not the file (the real one fsyncs every call)."""

    def __init__(self) -> None:
        self.spent: dict[str | None, int] = {}

    def used(self, month: str | None = None) -> int:
        return self.spent.get(month, 0)

    def record(self, calls: int, month: str | None = None) -> int:
        self.spent[month] = self.used(month) + calls
        return self.spent[month]


def fixed_credentials() -> tuple[str, str]:
    return ("an-access-key", "a-signing-key")


def counted_credentials():
    """Credentials that count how often the keychain was asked."""
    asked: list[int] = []

    def read() -> tuple[str, str]:
        asked.append(1)
        return fixed_credentials()

    read.asked = asked
    return read


def record_keys() -> None:
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")


def shipped_seams(monkeypatch, transport, duration_s: float = 20.0) -> None:
    """Both binaries found, and the shipped transport and carver replaced."""
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(duration_s))


#: The host every direct call is handed (no default since R-301), off a real domain.
HOST = "identify-test.example.invalid"


@pytest.fixture
def ledger(tmp_path) -> Ledger:
    """A ledger of this test's own, under its own lock."""
    return Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")


def run(
    transport: FakeTransport,
    *,
    duration_s: float = 40.0,
    budget: Budget | None = None,
    ledger: Ledger | None = None,
    credentials=fixed_credentials,
    carver: FakeCarver | None = None,
) -> Identified:
    return acrcloud.identify(
        Path("set.mp3"),
        transport=transport,
        carver=carver or FakeCarver(duration_s),
        credentials=credentials,
        budget=budget or Budget(),
        host=HOST,
        ledger=ledger,
        month="2026-09",
    )


def refused(transport: FakeTransport, **kwargs):
    """The cause ``run`` refuses with."""
    with pytest.raises(CratekitError) as excinfo:
        run(transport, **kwargs)
    return excinfo.value.cause


# Signing and the request


def test_the_signature_is_the_protocols_hmac_over_the_line_joined_tuple():
    line = "\n".join(["POST", "/v1/identify", "an-access-key", "audio", "1", "1700000000"])
    expected = base64.b64encode(hmac.new(b"a-signing-key", line.encode(), hashlib.sha1).digest()).decode()
    # The pair arrives through the fixture rather than as keyword literals,
    # because the repository scan reads ``access_key="..."`` as a credential.
    access, signing = fixed_credentials()
    assert acrcloud.sign(access_key=access, timestamp="1700000000", signing_key=signing) == expected


def test_the_request_carries_the_access_key_and_never_the_signing_key():
    access, signing = fixed_credentials()
    request = acrcloud.request_for(
        b"pcm", access_key=access, signing_key=signing, host=HOST, timestamp="1700000000"
    )
    assert request.fields["access_key"] == "an-access-key"
    assert request.fields["sample_bytes"] == "3"
    assert request.fields["timestamp"] == "1700000000"
    assert "a-signing-key" not in json.dumps(dict(request.fields))
    assert "a-signing-key" not in request.url
    assert request.url == f"https://{HOST}{acrcloud.ENDPOINT}"
    assert request.sample == b"pcm"


# The grid


@pytest.mark.parametrize(
    "duration_s, offsets",
    [
        (0.0, ()),
        (-3.0, ()),
        (5.0, (0,)),
        (11.9, (0,)),
        (12.0, (0,)),
        (36.0, (0,)),
        (37.0, (0, 25)),
        (60.0, (0, 25)),
        (300.0, tuple(range(0, 289, 25))),
    ],
)
def test_the_grid_is_a_function_of_the_duration_alone(duration_s, offsets):
    assert acrcloud.sample_offsets(duration_s) == offsets


@pytest.mark.parametrize("duration_s", [0.0, 5.0, 12.0, 36.0, 37.0, 60.0, 300.0, 7200.0, 7199.5])
def test_the_planned_count_is_the_grids_length_without_building_it(duration_s):
    assert acrcloud.planned_calls(duration_s) == len(acrcloud.sample_offsets(duration_s))


def test_a_nonsense_duration_is_refused_by_the_bound_before_any_grid_exists(ledger):
    """A broken header answering two billion seconds must not allocate two
    billion offsets on the way to the refusal that exists for it."""
    for duration in (2_147_483_647.0, float("inf"), 1e18):
        transport = FakeTransport()
        cause = refused(transport, duration_s=duration, ledger=ledger)
        assert cause.reason in {"intake-recognition-spend-bound", "intake-recognition-failed"}
        assert transport.requests == []
    assert acrcloud.planned_calls(float("nan")) == 0
    assert acrcloud.planned_calls(float("inf")) == 0


def test_no_chunk_is_ever_taken_past_the_point_where_a_whole_one_fits():
    for whole in range(1, 400):
        for offset in acrcloud.sample_offsets(float(whole)):
            assert offset + acrcloud.CHUNK_S <= max(whole, acrcloud.CHUNK_S)


def test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling():
    """R-706. The eleventh sitting's mix was 5 hours 5 minutes, 732 calls."""
    assert len(acrcloud.sample_offsets(2 * 3600.0)) <= acrcloud.MAX_CALLS_PER_RUN
    assert acrcloud.planned_calls(5 * 3600.0 + 5 * 60) == 732
    assert acrcloud.parts_needed(732) == 2
    assert acrcloud.parts_needed(acrcloud.planned_calls(9 * 3600.0)) > acrcloud.MAX_PARTS
    assert acrcloud.MAX_PARTS == 3, "Phillip's decision names Part A, Part B and Part C"


# The response mapping

FAMILIES = {
    Outcome.MATCH: (0,),
    Outcome.MISS: (1001, 2004, 3015),
    Outcome.QUOTA: (3003,),
    Outcome.AUTH: (3001, 3002, 3006, 3014),
    Outcome.TRANSIENT: (2000, 2005, 2999, 3000, 3100),
    Outcome.UNCLASSIFIED: (9999, 3005, 3300),
}
MALFORMED = [{"status": {"msg": "no code"}}, {"status": {"code": "0"}}, {"status": {"code": True}}]


@pytest.mark.parametrize(
    "payload, outcome",
    [(coded(code), outcome) for outcome, codes in FAMILIES.items() for code in codes]
    + [(payload, Outcome.UNCLASSIFIED) for payload in [*MALFORMED, {"status": "broken"}, {}]],
)
def test_every_status_code_lands_in_exactly_one_family(payload, outcome):
    found, _code, _message = acrcloud.classify(payload)
    assert found is outcome


def test_a_quota_a_credential_or_a_transient_answer_is_never_read_as_a_miss():
    """The 565 call batch. A quota answer that reads as a miss is the defect.
    And 3015 is the service saying a chunk carried nothing to fingerprint, a
    fact about the audio: read as quota, it ended a set on one silent chunk."""
    for code in (3003, 3001, 3002, 3006, 3014, 2000, 2005, 3000, 3100, 9999):
        assert acrcloud.classify(coded(code))[0] is not Outcome.MISS
    for code in (2004, 3015):
        assert acrcloud.classify(coded(code))[0] is Outcome.MISS


def test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept():
    found = acrcloud.parse_match(
        hit("Aurora Bloom", "Sun Path (Someone Remix)", isrc="QZABC2600001", score=87), offset_s=25
    )
    assert found is not None
    assert (found.offset_s, found.score) == (25, 87)
    wanted = found.wanted
    assert (wanted.artist, wanted.title, wanted.version) == ("Aurora Bloom", "Sun Path", "Someone Remix")
    assert wanted.isrc == "QZABC2600001"
    assert wanted.spelled == "Sun Path (Someone Remix)"
    assert wanted.ref == "", "a recognised track carries no provider identifier"
    joined = acrcloud.parse_match(hit("Aurora Bloom", "Sun Path", extra_artist="Nova Reef"), offset_s=0)
    assert joined is not None
    assert joined.wanted.artist == "Aurora Bloom", "the primary artist is the first named"


def test_a_match_naming_no_artist_or_no_title_or_no_music_is_none_and_a_bad_score_is_zero():
    for field, value in (("artists", []), ("title", "   ")):
        payload = hit("Aurora Bloom", "Sun Path")
        payload["metadata"]["music"][0][field] = value
        assert acrcloud.parse_match(payload, offset_s=0) is None
    for music in ([], "x"):
        payload = {"status": {"code": 0}, "metadata": {"music": music}}
        assert acrcloud.parse_match(payload, offset_s=0) is None
    payload = hit("Aurora Bloom", "Sun Path", score=90)
    payload["metadata"]["music"][0]["score"] = "high"
    found = acrcloud.parse_match(payload, offset_s=0)
    assert found is not None and found.score == 0


def _match(offset: int, artist: str, title: str, isrc: str = "", score: int = 80) -> Match:
    found = acrcloud.parse_match(hit(artist, title, isrc=isrc, score=score), offset_s=offset)
    assert found is not None
    return found


@pytest.mark.parametrize(
    "heard, expected",
    [
        pytest.param(
            [
                (0, "Aurora Bloom", "Sun Path", "X1", 70),
                (25, "Aurora Bloom", "Sun Path", "X1", 95),
                (50, "Aurora Bloom", "Sun Path", "X1", 80),
                (75, "Nova Reef", "Tide", "X2", 60),
            ],
            [(0, "Sun Path", "", 95), (75, "Tide", "", 60)],
            id="adjacent-fold-to-first-offset-and-best-score",
        ),
        pytest.param(
            [
                (0, "Aurora Bloom", "Sun Path", "X1"),
                (25, "Nova Reef", "Tide", "X2"),
                (50, "Aurora Bloom", "Sun Path", "X1"),
            ],
            [(0, "Sun Path", "", 80), (25, "Tide", "", 80), (50, "Sun Path", "", 80)],
            id="played-twice-stays-twice",
        ),
        pytest.param(
            [
                (0, "Aurora Bloom", "Sun Path"),
                (25, "aurora bloom", "SUN PATH"),
                (50, "Aurora Bloom", "Sun Path (Someone Remix)"),
            ],
            [(0, "Sun Path", "", 80), (50, "Sun Path", "Someone Remix", 80)],
            id="no-isrc-the-token-decides-and-a-version-differs",
        ),
        pytest.param(
            [(0, "Aurora Bloom", "Sun Path", "X1"), (25, "Aurora Bloom", "Sun Path", "X2")],
            [(0, "Sun Path", "", 80), (25, "Sun Path", "", 80)],
            id="two-isrcs-that-differ-do-not-fold",
        ),
        pytest.param(
            # Two titles of emoji alone by one artist fold to one token, and
            # played back to back they are still two records.
            [
                (0, "Aurora Bloom", "\U0001f525"),
                (25, "Aurora Bloom", "\U0001f525"),
                (50, "Aurora Bloom", "\U0001f4a7"),
            ],
            [(0, "\U0001f525", "", 80), (50, "\U0001f4a7", "", 80)],
            id="two-emoji-titles-stay-two-rows",
        ),
    ],
)
def test_adjacent_answers_for_one_recording_fold_and_nothing_else_does(heard, expected):
    folded = acrcloud.fold([_match(*one) for one in heard])
    assert [(m.offset_s, m.wanted.title, m.wanted.version, m.score) for m in folded] == expected


# Identification through the fakes


def test_identification_returns_the_folded_rows_and_counts_every_call(ledger):
    transport = FakeTransport(
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        hit("Aurora Bloom", "Sun Path", isrc="X1"),
        miss(),
        hit("Nova Reef", "Tide", isrc="X2"),
    )
    result = run(transport, duration_s=100.0, ledger=ledger)
    assert [(row.artist, row.title) for row in result.rows] == [
        ("Aurora Bloom", "Sun Path"),
        ("Nova Reef", "Tide"),
    ]
    assert (result.calls, result.chunks, result.misses, result.unreached) == (4, 4, 1, 0)
    assert ledger.used("2026-09") == 4
    assert [r.fields["access_key"] for r in transport.requests] == ["an-access-key"] * 4
    assert [r.sample for r in transport.requests] == [b"chunk@0", b"chunk@25", b"chunk@50", b"chunk@75"]


def test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal(ledger):
    result = run(FakeTransport(miss(), miss()), duration_s=40.0, ledger=ledger)
    assert result.rows == ()
    assert (result.calls, result.misses, result.parts) == (2, 2, 1)
    assert ledger.used("2026-09") == 2


def test_the_per_run_bound_refuses_before_any_carve_call_or_credential(ledger):
    transport, carver, credentials = FakeTransport(), FakeCarver(3600.0), counted_credentials()
    cause = refused(
        transport, carver=carver, credentials=credentials, budget=Budget(per_run=10), ledger=ledger
    )
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail["kind"] == "per-run"
    assert cause.detail["planned"] == len(acrcloud.sample_offsets(3600.0))
    assert cause.detail["bound"] == 10
    assert transport.requests == []
    assert carver.carved == []
    assert credentials.asked == [], "the keychain was asked before the budget was checked"
    assert ledger.used("2026-09") == 0


def test_the_monthly_bound_counts_what_the_ledger_already_holds(ledger):
    ledger.record(95, "2026-09")
    transport = FakeTransport()
    cause = refused(transport, duration_s=100.0, budget=Budget(monthly=98), ledger=ledger)
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail == {
        "planned": 4,
        "used": 95,
        "bound": 98,
        "kind": "monthly",
        "key": acrcloud.MONTHLY_KEY,
    }
    assert cause.detail["key"] == "recognition.monthly_calls"
    assert "raise recognition.monthly_calls" in cause.message
    assert cause.remediation.remedy == Remedy.RETRY_LATER
    assert transport.requests == []
    # A plan that fits exactly is allowed: 85 seconds is three chunks.
    fits = FakeTransport(miss(), miss(), miss())
    run(fits, duration_s=85.0, budget=Budget(monthly=98), ledger=ledger)
    assert len(fits.requests) == 3
    assert ledger.used("2026-09") == 98


def test_a_hand_built_budget_bounds_the_run_and_the_shipped_one_bounds_the_month_too():
    """R-301. The configured budget always carries a month, the default one too."""
    assert Budget() == Budget(per_run=acrcloud.MAX_CALLS_PER_RUN, monthly=None)
    assert Budget.from_config(config.RecognitionConfig()) == Budget(
        per_run=acrcloud.MAX_CALLS_PER_RUN, monthly=config.DEFAULT_RECOGNITION_MONTHLY_CALLS
    )
    assert Budget.from_config(config.RecognitionConfig(monthly_calls=7)).monthly == 7


def test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss(ledger):
    quota = coded(3003, "requests limit exceeded")
    transport = FakeTransport(hit("Aurora Bloom", "Sun Path", isrc="X1"), quota, miss())
    cause = refused(transport, duration_s=60.0, ledger=ledger)
    assert cause.reason == "intake-recognition-spend-bound"
    assert (cause.detail["kind"], cause.detail["code"], cause.detail["calls"]) == ("provider-quota", 3003, 2)
    assert cause.remediation.remedy == Remedy.RETRY_LATER
    assert len(transport.requests) == 2, "a call was made after the quota answer"
    assert ledger.used("2026-09") == 2, "the calls made before the refusal were not counted"


def test_the_two_spend_refusals_and_a_miss_are_three_different_things(ledger):
    own = refused(FakeTransport(), duration_s=100.0, budget=Budget(per_run=1), ledger=ledger)
    theirs = refused(FakeTransport(coded(3003)), duration_s=20.0, ledger=ledger)
    missed = run(FakeTransport(miss()), duration_s=20.0, ledger=ledger)
    assert own.reason == theirs.reason == "intake-recognition-spend-bound"
    assert own.detail["kind"] != theirs.detail["kind"]
    assert missed.rows == () and missed.misses == 1


def test_a_credential_answer_ends_the_run_as_auth_failed(ledger):
    transport = FakeTransport(coded(3001, "invalid access key"), miss())
    cause = refused(transport, duration_s=60.0, ledger=ledger)
    assert cause.reason == "auth-failed"
    assert cause.detail["code"] == 3001
    assert cause.remediation.remedy == Remedy.SET_CREDENTIAL
    assert len(transport.requests) == 1


def test_a_transient_answer_or_a_transport_that_raised_skips_the_chunk_and_is_counted(ledger):
    transport = FakeTransport(
        coded(2005, "timeout"),
        ConnectionError("dropped"),
        Response(status=502, body=b"bad gateway"),
        Response(status=200, body=b"not json"),
        hit("Nova Reef", "Tide", isrc="X2"),
    )
    result = run(transport, duration_s=120.0, ledger=ledger)
    assert [row.title for row in result.rows] == ["Tide"]
    assert (result.calls, result.unreached, result.misses) == (5, 4, 0)
    assert ledger.used("2026-09") == 5, "an attempt that got no answer was not counted"


def test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set(ledger):
    cause = refused(FakeTransport(ConnectionError("down"), ConnectionError("down")), ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert cause.retryable is True
    assert cause.detail["calls"] == 2
    assert ledger.used("2026-09") == 2


def test_an_answer_this_build_cannot_classify_stops_the_run_naming_the_code(ledger):
    transport = FakeTransport(hit("Aurora Bloom", "Sun Path"), coded(3005, "something new"), miss())
    cause = refused(transport, duration_s=60.0, ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert (cause.detail["code"], cause.detail["calls"]) == (3005, 2)
    assert len(transport.requests) == 2


def test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call(ledger):
    class Unreadable(FakeCarver):
        def duration(self, source: Path) -> float:
            raise RuntimeError("ffprobe could not read it")

    class Uncarvable(FakeCarver):
        def carve(self, source: Path, offset_s: int, chunk_s: int) -> bytes:
            if offset_s == 25:
                raise RuntimeError("ffmpeg died")
            return super().carve(source, offset_s, chunk_s)

    transport = FakeTransport()
    cause = refused(transport, carver=Unreadable(0.0), ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert transport.requests == []
    transport = FakeTransport(miss(), miss())
    cause = refused(transport, carver=Uncarvable(60.0), ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert cause.detail["offset_s"] == 25
    assert len(transport.requests) == 1


def test_an_empty_recording_sends_nothing(ledger):
    cause = refused(FakeTransport(), duration_s=0.0, ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert ledger.used("2026-09") == 0


# The ledger


def test_the_ledger_is_keyed_by_month_and_survives_a_corrupt_file(tmp_path, ledger):
    assert ledger.used("2026-09") == 0
    assert ledger.record(3, "2026-09") == 3
    assert ledger.record(2, "2026-09") == 5
    assert ledger.record(4, "2026-10") == 4
    assert ledger.used("2026-09") == 5
    assert json.loads((tmp_path / "usage.json").read_text()) == {"2026-09": 5, "2026-10": 4}
    (tmp_path / "usage.json").write_text("{not json")
    assert ledger.used("2026-09") == 0, "a corrupt counter must not lock recognition out"
    assert ledger.record(1, "2026-09") == 1
    (tmp_path / "usage.json").write_text('{"2026-09": "seven", "2026-08": 2}')
    assert ledger.used("2026-09") == 0
    assert ledger.used("2026-08") == 2


def test_recording_nothing_writes_nothing(tmp_path, ledger):
    assert ledger.record(0, "2026-09") == 0
    assert not (tmp_path / "usage.json").exists()


def test_the_ledger_and_the_cache_live_in_their_declared_installation_state_entries():
    ledger = Ledger()
    assert ledger.path == config.state_path(acrcloud.LEDGER_KEY)
    assert ledger.lock_path == config.state_path(acrcloud.LEDGER_LOCK_KEY)
    assert ledger.path.parent == ledger.lock_path.parent
    assert acrcloud.RecognitionCache().root == config.state_path(acrcloud.CACHE_KEY)
    assert config.state_file(acrcloud.CACHE_KEY).root is config.StateRoot.INSTALLATION


def test_the_month_key_is_the_calendar_month():
    assert acrcloud.current_month(datetime(2026, 9, 9, 23, 59)) == "2026-09"
    assert acrcloud.current_month(datetime(2026, 1, 1, 0, 0)) == "2026-01"


# The credentials and the seam


def test_the_keychain_credentials_are_read_by_name_after_the_gate():
    record_keys()
    assert acrcloud.keychain_credentials() == ("k-1", "s-1")


def test_a_credential_missing_after_the_gate_is_credential_missing_with_its_own_remedy():
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.keychain_credentials()
    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy == Remedy.SET_CREDENTIAL
    assert cause.detail["credential"] == str(secrets.Credential.IDENTIFY_SIGNING_KEY)


def test_a_keychain_that_cannot_be_reached_keeps_the_stores_own_remedy(monkeypatch):
    """Telling a person to record a credential into a store that cannot hold
    one is the wrong instruction, so the exception's remedy is passed on."""

    def unreachable(name):
        raise secrets.CredentialBackendUnavailable("no keychain backend here", name=name)

    monkeypatch.setattr(secrets, "get", unreachable)
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.keychain_credentials()
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-unready"
    assert cause.remediation.remedy == Remedy.INSTALL_KEYCHAIN_BACKEND
    assert cause.detail["kind"] == "CredentialBackendUnavailable"


def test_the_gate_names_both_binaries_and_both_keys():
    assert recognize.BINARIES == ("ffmpeg", "ffprobe")
    missing = recognize.recognition_ready()
    for name in (str(secrets.Credential.IDENTIFY_KEY), str(secrets.Credential.IDENTIFY_SIGNING_KEY)):
        assert name in missing


def test_the_seam_binds_this_identifier_when_none_is_injected(monkeypatch, tmp_path, ledger):
    """``recognize.identify`` with no identifier is the paid path, over the
    shipped seams, which are looked up on the module at call time."""
    source = tmp_path / "set.mp3"
    source.write_bytes(b"ID3")
    record_keys()
    transport = FakeTransport(hit("Aurora Bloom", "Sun Path", isrc="X1"))
    shipped_seams(monkeypatch, transport)
    monkeypatch.setattr(acrcloud, "Ledger", lambda: ledger)
    found = recognize.identify(source, recognition=config.RecognitionConfig(host="identify-x.acrcloud.com"))
    assert isinstance(found, Identified)
    assert [(row.artist, row.title) for row in found.rows] == [("Aurora Bloom", "Sun Path")]
    assert (found.calls, found.chunks, found.misses, found.unreached) == (1, 1, 0, 0)
    assert transport.requests[0].fields["access_key"] == "k-1"
    assert transport.requests[0].url == f"https://identify-x.acrcloud.com{acrcloud.ENDPOINT}"
    assert ledger.used() == 1


@pytest.mark.parametrize("keys", [True, False], ids=["no-section", "no-credentials"])
def test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first(monkeypatch, tmp_path, keys):
    """R-301. A caller that forgot the section is told, rather than sent to a
    region and a month nobody chose; with no key the gate refuses first."""
    source = tmp_path / "set.mp3"
    source.write_bytes(b"ID3")
    if keys:
        record_keys()
    transport = FakeTransport()
    shipped_seams(monkeypatch, transport)
    if keys:
        with pytest.raises(TypeError, match="recognition section"):
            recognize.identify(source)
    else:
        with pytest.raises(CratekitError) as excinfo:
            recognize.identify(source)
        assert excinfo.value.cause.reason == "intake-recognition-unready"
    assert transport.requests == []


def test_the_bound_identifier_resolves_its_seams_at_call_time(monkeypatch, ledger):
    identifier = acrcloud.bound_identifier(config.RecognitionConfig())
    transport = FakeTransport(miss())
    shipped_seams(monkeypatch, transport, 5.0)
    monkeypatch.setattr(acrcloud, "Ledger", lambda: ledger)
    record_keys()
    assert identifier(Path("set.mp3")).rows == ()
    assert len(transport.requests) == 1


def test_a_fake_identifier_answering_bare_rows_is_normalised_by_the_seam(monkeypatch, tmp_path):
    monkeypatch.setattr(recognize.secrets, "exists", lambda name: True)
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    found = recognize.identify(tmp_path / "x.mp3", identifier=lambda path: (Wanted(artist="A", title="T"),))
    assert isinstance(found, Identified)
    assert [row.title for row in found.rows] == ["T"]
    assert (found.calls, found.chunks, found.misses, found.unreached) == (0, 0, 0, 0)


# The stop on a service that stops answering


def test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent(ledger):
    """An offline machine costs a handful of attempts, not a whole set."""
    transport = FakeTransport(*([ConnectionError("down")] * 20))
    cause = refused(transport, duration_s=600.0, ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert cause.detail["calls"] == acrcloud.UNREACHED_STOP
    assert cause.detail["unreached"] == acrcloud.UNREACHED_STOP
    assert len(transport.requests) == acrcloud.UNREACHED_STOP
    assert ledger.used("2026-09") == acrcloud.UNREACHED_STOP


def test_an_answer_resets_the_streak_so_a_blip_does_not_end_the_run(ledger):
    answers = [ConnectionError("blip")] * 4 + [miss()] + [ConnectionError("blip")] * 4 + [hit("A", "T")]
    result = run(FakeTransport(*answers), duration_s=250.0, ledger=ledger)
    assert (result.calls, result.unreached, result.misses) == (10, 8, 1)
    assert [row.title for row in result.rows] == ["T"]


def test_a_rejecting_host_stops_the_run_the_same_way(ledger):
    transport = FakeTransport(*([Response(status=403, body=b"forbidden")] * 20))
    cause = refused(transport, duration_s=600.0, ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert "HTTP 403" in cause.message
    assert len(transport.requests) == acrcloud.UNREACHED_STOP


def test_a_ledger_that_cannot_record_stops_the_run_before_the_call(ledger, monkeypatch):
    def unlockable(calls, month=None):
        raise config.ConfigLockUnavailable("the state directory is read only")

    monkeypatch.setattr(ledger, "record", unlockable)
    transport = FakeTransport(miss())
    cause = refused(transport, duration_s=20.0, ledger=ledger)
    assert cause.reason == "intake-recognition-failed"
    assert cause.detail["calls"] == 0
    assert transport.requests == [], "a call was made that the ledger could not count"


# U103: the recognition cache. A chunk already answered is not paid for again.


@pytest.fixture
def cache(tmp_path) -> acrcloud.RecognitionCache:
    return acrcloud.RecognitionCache(root=tmp_path / "identify_cache")


def real_recording(tmp_path, content: bytes = b"a recording", name: str = "set.mp3") -> Path:
    path = tmp_path / name
    path.write_bytes(content)
    return path


def cached_run(transport, source, cache, ledger, *, duration_s=85.0, **kwargs) -> Identified:
    kwargs.setdefault("budget", Budget())
    kwargs.setdefault("host", HOST)
    return acrcloud.identify(
        source,
        transport=transport,
        carver=kwargs.pop("carver", None) or FakeCarver(duration_s),
        credentials=kwargs.pop("credentials", fixed_credentials),
        ledger=ledger,
        cache=cache,
        month="2026-09",
        **kwargs,
    )


def cached_refusal(transport, source, cache, ledger, **kwargs):
    """The cause ``cached_run`` refuses with."""
    with pytest.raises(CratekitError) as excinfo:
        cached_run(transport, source, cache, ledger, **kwargs)
    return excinfo.value.cause


def three_answers() -> list[dict]:
    return [hit("Aurora Bloom", "Sun Path", isrc="X1"), miss(), hit("Nova Reef", "Tide", isrc="X2")]


def a_gap() -> FakeTransport:
    """One answer and two chunks that got none."""
    return FakeTransport(hit("Aurora Bloom", "Sun Path"), ConnectionError("down"), coded(3000))


def unwritable(monkeypatch, why: str = "") -> None:
    """A cache whose write raises: permission denied, or ``why`` as a failure."""

    def failing(self, plan, answers):
        if why:
            raise AssertionError(why)
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(acrcloud.RecognitionCache, "write", failing)


def test_a_second_pass_over_an_unchanged_recording_spends_nothing(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    first = cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    assert (first.calls, first.cached, first.cache_unwritten) == (3, 0, "")
    assert first.digest == acrcloud.content_digest(source)
    silent, carver, credentials = FakeTransport(), FakeCarver(85.0), counted_credentials()
    second = cached_run(silent, source, cache, ledger, carver=carver, credentials=credentials)
    assert silent.requests == [], "a kept chunk reached the transport"
    assert carver.carved == [], "a kept chunk was carved"
    assert credentials.asked == [], "a pass that owes nothing asked the keychain"
    assert ledger.used("2026-09") == 3, "a kept chunk was counted as spend"
    assert second.rows == first.rows
    assert (second.calls, second.cached, second.chunks) == (0, 3, 3)
    assert (second.misses, second.unreached) == (first.misses, first.unreached)


@pytest.mark.parametrize(
    "change, owed",
    [
        pytest.param({"content": b"a different recording under the same name"}, 3, id="file"),
        pytest.param({"duration_s": 100.0}, 4, id="chunk-plan"),
        pytest.param({"host": "identify-eu-west-1.example.invalid"}, 3, id="host"),
    ],
)
def test_a_changed_file_plan_or_host_misses_the_cache(tmp_path, cache, ledger, change, owed):
    """The same bytes measured to a different length are a different grid,
    and another regional host is another bucket."""
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    if "content" in change:
        source.write_bytes(change.pop("content"))
    again = FakeTransport(*[miss()] * owed)
    result = cached_run(again, source, cache, ledger, **change)
    assert len(again.requests) == owed, "a changed recording was served the old answers"
    assert result.rows == ()
    assert result.cached == 0


def test_the_same_bytes_under_another_name_hit_the_cache(tmp_path, cache, ledger):
    """The identity is the audio. A copy is the same recording."""
    cached_run(FakeTransport(*three_answers()), real_recording(tmp_path), cache, ledger)
    silent = FakeTransport()
    copy = real_recording(tmp_path, name="a copy.mp3")
    assert cached_run(silent, copy, cache, ledger).cached == 3
    assert silent.requests == []


@pytest.mark.parametrize(
    "changed",
    [
        {"digest": "another"},
        {"offsets": (0, 25)},
        {"chunk_s": 10},
        {"interval_s": 20},
        {"sample_rate": 8000},
        {"host": "elsewhere.example.invalid"},
    ],
    ids=lambda changed: next(iter(changed)),
)
def test_every_field_of_the_plan_moves_the_key(changed):
    base = dict(digest="d", offsets=(0, 25, 50), host=HOST)
    assert acrcloud.ChunkPlan(**base).key() != acrcloud.ChunkPlan(**{**base, **changed}).key()
    assert acrcloud.ChunkPlan(**base).key() == acrcloud.ChunkPlan(**base).key()


def test_the_digest_is_the_sha256_of_the_bytes(tmp_path):
    source = real_recording(tmp_path, b"exactly these bytes")
    assert acrcloud.content_digest(source) == hashlib.sha256(b"exactly these bytes").hexdigest()


def test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    assert cached_run(a_gap(), source, cache, ledger).unreached == 2
    fill = FakeTransport(miss(), hit("Nova Reef", "Tide"))
    second = cached_run(fill, source, cache, ledger)
    assert [r.sample for r in fill.requests] == [b"chunk@25", b"chunk@50"]
    assert (second.calls, second.cached, second.unreached) == (2, 1, 0)
    assert [row.title for row in second.rows] == ["Sun Path", "Tide"]


def test_kept_and_fresh_answers_fold_in_set_order(tmp_path, cache, ledger):
    """A gap filled between two chunks of one record folds to ONE row."""
    source = real_recording(tmp_path)
    same = hit("Aurora Bloom", "Sun Path", isrc="X1")
    cached_run(FakeTransport(same, ConnectionError("down"), same), source, cache, ledger)
    second = cached_run(FakeTransport(same), source, cache, ledger)
    assert [row.title for row in second.rows] == ["Sun Path"]


def test_a_pass_that_raised_keeps_what_it_had_already_paid_for(tmp_path, cache, ledger):
    """A quota refusal mid set. The answers before it are written on the way out."""
    source = real_recording(tmp_path)
    quota = FakeTransport(hit("Aurora Bloom", "Sun Path"), coded(3003))
    assert cached_refusal(quota, source, cache, ledger).detail["kind"] == "provider-quota"
    rest = FakeTransport(miss(), hit("Nova Reef", "Tide"))
    result = cached_run(rest, source, cache, ledger)
    assert [r.sample for r in rest.requests] == [b"chunk@25", b"chunk@50"]
    assert (result.calls, result.cached) == (2, 1)
    assert [row.title for row in result.rows] == ["Sun Path", "Tide"]


def test_answers_that_cannot_be_kept_neither_fail_the_pass_nor_replace_its_refusal(
    tmp_path, cache, ledger, monkeypatch
):
    unwritable(monkeypatch)
    quota = FakeTransport(hit("Aurora Bloom", "Sun Path"), coded(3003))
    cause = cached_refusal(quota, real_recording(tmp_path), cache, ledger)
    assert cause.reason == "intake-recognition-spend-bound"
    result = cached_run(FakeTransport(*three_answers()), real_recording(tmp_path), cache, ledger)
    assert [row.title for row in result.rows] == ["Sun Path", "Tide"]
    assert "PermissionError" in result.cache_unwritten


def test_refresh_reads_nothing_kept_and_lays_the_new_answers_over_the_document(
    tmp_path, cache, ledger
):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(hit("Aurora Bloom", "Sun Path"), miss(), miss()), source, cache, ledger)
    asked = FakeTransport(hit("Aurora Bloom", "Sun Path"), hit("Nova Reef", "Tide"), miss())
    refreshed = cached_run(asked, source, cache, ledger, refresh=True)
    assert len(asked.requests) == 3
    assert (refreshed.calls, refreshed.cached) == (3, 0)
    after = cached_run(FakeTransport(), source, cache, ledger)
    assert [row.title for row in after.rows] == ["Sun Path", "Tide"]


def plan_of(source: Path, duration_s: float = 85.0) -> acrcloud.ChunkPlan:
    return acrcloud.ChunkPlan(
        digest=acrcloud.content_digest(source),
        offsets=acrcloud.sample_offsets(duration_s),
        host=HOST,
    )


def test_the_write_is_a_merge_so_an_overlapping_pass_does_not_drop_what_another_paid_for(tmp_path, cache):
    plan = plan_of(real_recording(tmp_path))
    cache.write(plan, {0: hit("Aurora Bloom", "Sun Path")})
    # A second pass that began before that write knows only its own answer.
    cache.write(plan, {25: miss()})
    assert sorted(cache.read(plan)) == [0, 25]
    assert cache.path_for(plan).with_suffix(".lock").is_file()


@pytest.mark.parametrize(
    "document",
    [
        "not json at all",
        "[1, 2, 3]",
        json.dumps({"version": 1, "plan": {"digest": "someone else's"}, "answers": {"0": miss()}}),
    ],
    ids=["corrupt", "not-an-object", "another-plan"],
)
def test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist(
    tmp_path, cache, ledger, document
):
    source = real_recording(tmp_path)
    plan = plan_of(source)
    cache.root.mkdir(parents=True)
    cache.path_for(plan).write_text(document)
    assert cache.read(plan) == {}
    paid = FakeTransport(*three_answers())
    assert cached_run(paid, source, cache, ledger).cached == 0
    assert len(paid.requests) == 3


def test_a_document_from_another_cache_version_is_a_miss(tmp_path, cache):
    plan = plan_of(real_recording(tmp_path))
    cache.write(plan, {0: miss()})
    assert cache.read(plan) == {0: miss()}
    held = json.loads(cache.path_for(plan).read_text())
    held["version"] = acrcloud.CACHE_VERSION + 1
    cache.path_for(plan).write_text(json.dumps(held))
    assert cache.read(plan) == {}


def test_only_an_answer_is_kept_or_served_in_either_direction(tmp_path, cache):
    """Removed alone, each layer still holds: the writer drops a non answer,
    and the reader refuses one a foreign writer left behind."""
    plan = plan_of(real_recording(tmp_path))
    cache.write(plan, {0: hit("Aurora Bloom", "Sun Path"), 25: coded(3003), 50: coded(3000)})
    assert sorted(json.loads(cache.path_for(plan).read_text())["answers"]) == ["0"]
    held = json.loads(cache.path_for(plan).read_text())
    held["answers"].update({"25": coded(3003), "50": "not an object", "75": miss(), "x": miss()})
    cache.path_for(plan).write_text(json.dumps(held))
    assert sorted(cache.read(plan)) == [0], "a non answer or an unplanned offset was served"


def test_the_cache_document_is_private_and_holds_no_credential(tmp_path, cache, ledger):
    cached_run(FakeTransport(*three_answers()), real_recording(tmp_path), cache, ledger)
    (document,) = list(cache.root.glob("*.json"))
    assert document.stat().st_mode & 0o777 == 0o600
    text = document.read_text()
    assert "an-access-key" not in text and "a-signing-key" not in text


def test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so(
    tmp_path, cache, ledger
):
    result = cached_run(FakeTransport(*three_answers()), tmp_path / "gone.mp3", cache, ledger)
    assert result.calls == 3
    assert "digest" in result.cache_unwritten
    assert not cache.root.exists()


def test_a_pass_that_paid_for_nothing_writes_nothing_and_reports_nothing_unwritten(
    tmp_path, cache, ledger, monkeypatch
):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    unwritable(monkeypatch, "a pass that paid for nothing rewrote the cache")
    assert cached_run(FakeTransport(), source, cache, ledger).cache_unwritten == ""


def test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid(tmp_path, cache, ledger):
    """The ceiling reads the grid (R-706), and the run bound reads only what a
    part owes (`docs/mutation/u103-a.md` row A16 names the older property)."""
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    spent = Budget(monthly=3)
    # The month is used up and the recording is fully kept: nothing is owed.
    assert cached_run(FakeTransport(), source, cache, ledger, budget=spent).cached == 3
    # A grid under the parts ceiling is served kept whatever the run bound,
    # and the ceiling still refuses a grid over it before anything is read.
    served = cached_run(FakeTransport(), source, cache, ledger, budget=Budget(per_run=1))
    assert (served.cached, served.parts, served.calls) == (3, 3, 0)
    over = cached_refusal(FakeTransport(), source, cache, ledger, budget=Budget(per_run=1), duration_s=100.0)
    assert (over.detail["kind"], over.detail["ceiling"]) == ("per-run", 3)
    # And a recording that owes calls into a spent month is refused for them.
    other = real_recording(tmp_path, b"another recording", name="other.mp3")
    monthly = cached_refusal(FakeTransport(), other, cache, ledger, budget=spent)
    assert monthly.detail == {
        "planned": 3,
        "used": 3,
        "bound": 3,
        "kind": "monthly",
        "key": acrcloud.MONTHLY_KEY,
    }


def test_the_monthly_bound_counts_only_the_gap_on_a_partly_kept_recording(tmp_path, cache, ledger):
    """One chunk kept and two owed, with exactly two calls left in the month.
    Counting the whole grid against the month would refuse a pass that fits."""
    source = real_recording(tmp_path)
    cached_run(a_gap(), source, cache, ledger)
    assert ledger.used("2026-09") == 3
    fill = FakeTransport(miss(), miss())
    result = cached_run(fill, source, cache, ledger, budget=Budget(monthly=5))
    assert (result.calls, result.cached) == (2, 1)


def test_the_bound_identifier_hands_the_cache_through(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    identifier = acrcloud.bound_identifier(
        config.RecognitionConfig(),
        transport=FakeTransport(*three_answers()),
        carver=FakeCarver(85.0),
        ledger=ledger,
        cache=cache,
    )
    record_keys()
    assert identifier(source).calls == 3
    assert identifier(source).calls == 0


# R-706: a set longer than one run is identified in even parts, as one set


@pytest.mark.parametrize(
    "count, per_run, sizes",
    [
        (0, 400, ()),
        (1, 400, (1,)),
        (400, 400, (400,)),
        (401, 400, (201, 200)),
        (732, 400, (366, 366)),
        (1200, 400, (400, 400, 400)),
        (5, 2, (2, 2, 1)),
        (7, 3, (3, 2, 2)),
    ],
)
def test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound(count, per_run, sizes):
    grid = tuple(range(0, count * acrcloud.INTERVAL_S, acrcloud.INTERVAL_S))
    parts = acrcloud.partition(grid, per_run=per_run)
    assert tuple(len(part) for part in parts) == sizes
    assert tuple(offset for part in parts for offset in part) == grid, "a cut lost or moved a chunk"
    assert all(len(part) <= per_run for part in parts)
    assert len(parts) == acrcloud.parts_needed(count, per_run=per_run)


def test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set():
    """The eleventh sitting's shape: 732 chunks, two halves of 366. One pass,
    one result, and a record playing across the cut is one row and not two."""
    five_hours_five = 5 * 3600.0 + 5 * 60
    grid = acrcloud.sample_offsets(five_hours_five)
    assert len(grid) == 732
    answers: list[dict] = [miss()] * 732
    answers[0] = hit("Aurora Bloom", "Sun Path", isrc="X1")
    answers[365] = answers[366] = hit("Nova Reef", "Tide", isrc="X2")
    answers[731] = hit("Mira Vale", "Glass Hour", isrc="X3")
    carver, ledger = FakeCarver(five_hours_five), MemoryLedger()
    result = run(FakeTransport(*answers), carver=carver, ledger=ledger)
    assert result.parts == 2
    assert (result.calls, result.chunks, result.unreached) == (732, 732, 0)
    assert carver.carved == list(grid), "the parts were not walked in grid order, once each"
    assert ledger.used("2026-09") == 732
    assert [(row.artist, row.title) for row in result.rows] == [
        ("Aurora Bloom", "Sun Path"),
        ("Nova Reef", "Tide"),
        ("Mira Vale", "Glass Hour"),
    ], "the record across the cut folded to one row"


def test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential(ledger):
    transport, carver, credentials = FakeTransport(), FakeCarver(9 * 3600.0), counted_credentials()
    cause = refused(transport, carver=carver, credentials=credentials, ledger=ledger)
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail == {
        "planned": acrcloud.planned_calls(9 * 3600.0),
        "bound": acrcloud.MAX_CALLS_PER_RUN,
        "parts": acrcloud.MAX_PARTS,
        "ceiling": acrcloud.MAX_CALLS_PER_RUN * acrcloud.MAX_PARTS,
        "kind": "per-run",
    }
    assert f"more than {acrcloud.MAX_PARTS} parts" in cause.message
    assert "not one set" in cause.message
    assert transport.requests == []
    assert carver.carved == []
    assert credentials.asked == []
    assert ledger.used("2026-09") == 0


def test_the_month_is_asked_once_over_the_whole_set_before_the_first_part(ledger):
    """A 100 second recording is four chunks, two parts of two under a run
    bound of two. Two calls already spent and a month of five cannot afford
    the four, and a check per part would have let the first part through."""
    ledger.record(2, "2026-09")
    transport, budget = FakeTransport(), Budget(per_run=2, monthly=5)
    cause = refused(transport, duration_s=100.0, budget=budget, ledger=ledger)
    assert cause.detail["kind"] == "monthly"
    assert cause.detail["planned"] == 4, "the month was asked about one part, not the set"
    assert transport.requests == []
    assert ledger.used("2026-09") == 2
    # One call fewer spent and the whole set fits, so all four parts' chunks go.
    fits = Ledger(path=ledger.path.with_name("fits.json"), lock_path=ledger.lock_path)
    fits.record(1, "2026-09")
    result = run(FakeTransport(*[miss()] * 4), duration_s=100.0, budget=budget, ledger=fits)
    assert (result.parts, result.calls) == (2, 4)
    assert fits.used("2026-09") == 5


@pytest.mark.parametrize(
    "cut",
    [lambda offsets: (tuple(offsets),), lambda offsets: (tuple(offsets[:1]), tuple(offsets[1:]))],
    ids=["one-oversize-part", "oversize-second-part"],
)
def test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call(ledger, monkeypatch, cut):
    """The run bound is a property of the spend, not of the cut. A partition
    that returned an oversize part, first or LAST, meets the guard before the
    transport, so the parts before it are not paid for either."""
    monkeypatch.setattr(acrcloud, "partition", lambda offsets, *, per_run: cut(offsets))
    transport, carver = FakeTransport(), FakeCarver(100.0)
    cause = refused(transport, carver=carver, budget=Budget(per_run=2), ledger=ledger)
    assert cause.reason == "intake-recognition-spend-bound"
    assert (cause.detail["bound"], cause.detail["kind"]) == (2, "per-run")
    assert cause.detail["planned"] in (3, 4)
    assert "this run would take" in cause.message
    assert transport.requests == []
    assert carver.carved == []
    assert ledger.used("2026-09") == 0


def test_a_split_set_is_served_from_the_cache_as_one_plan(tmp_path, cache, ledger):
    """One chunk plan for the whole grid, so a second pass over a split set
    pays for nothing and still says how many parts it is."""
    source, split = real_recording(tmp_path), {"duration_s": 100.0, "budget": Budget(per_run=2)}
    first = cached_run(FakeTransport(*[miss()] * 4), source, cache, ledger, **split)
    assert (first.parts, first.calls) == (2, 4)
    second = cached_run(FakeTransport(), source, cache, ledger, **split)
    assert (second.parts, second.calls, second.cached) == (2, 0, 4)


def test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed(tmp_path, cache, ledger):
    source, split = real_recording(tmp_path), {"duration_s": 100.0, "budget": Budget(per_run=2)}
    gap = FakeTransport(miss(), ConnectionError("down"), ConnectionError("down"), miss())
    cached_run(gap, source, cache, ledger, **split)
    fill = FakeTransport(miss(), miss())
    result = cached_run(fill, source, cache, ledger, **split)
    assert (result.parts, result.calls, result.cached) == (2, 2, 2)
    assert len(fill.requests) == 2
