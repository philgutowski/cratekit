"""U57: the recognition identifier, driven through fakes. Nothing here spends.

The seam ``recognize.identify`` declared in U37 finally has an implementation
behind it, and this file is the proof that the implementation is BOUNDED: the
call count is known before the first chunk is carved, a spend refusal is a
different cause from a miss, the credentials are read only after the budget
has passed, and every attempt reaches the ledger whether or not an answer
came back. The battery passes with no credential recorded and no binary
installed, which is what the two injected seams are for.

D1 applies. Nothing here names a real key, a real host, or a real track.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from pathlib import Path

import pytest

from cratekit.core import secrets
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.intake import acrcloud, recognize
from cratekit.intake.acrcloud import Budget, Ledger, Match, Outcome, Request, Response
from cratekit.intake.recognize import Identified

# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


def hit(artist: str, title: str, *, isrc: str = "", score: int = 90, extra_artist: str = "") -> dict:
    """A MATCH answer naming one recording, in the service's own shape."""
    artists = [{"name": artist}]
    if extra_artist:
        artists.append({"name": extra_artist})
    return {
        "status": {"code": 0, "msg": "Success"},
        "metadata": {
            "music": [
                {
                    "title": title,
                    "artists": artists,
                    "album": {"name": "An Album"},
                    "external_ids": {"isrc": isrc} if isrc else {},
                    "score": score,
                }
            ]
        },
    }


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


def fixed_credentials() -> tuple[str, str]:
    return ("an-access-key", "a-signing-key")


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
    month: str = "2026-09",
    source: Path | None = None,
) -> Identified:
    return acrcloud.identify(
        source or Path("set.mp3"),
        transport=transport,
        carver=FakeCarver(duration_s),
        credentials=credentials,
        budget=budget,
        ledger=ledger,
        month=month,
    )


# ---------------------------------------------------------------------------
# Signing and the request
# ---------------------------------------------------------------------------


def test_the_signature_is_the_protocols_hmac_over_the_line_joined_tuple():
    expected = base64.b64encode(
        hmac.new(
            b"a-signing-key",
            "\n".join(["POST", "/v1/identify", "an-access-key", "audio", "1", "1700000000"]).encode(),
            hashlib.sha1,
        ).digest()
    ).decode()
    # The two values arrive through the fixture pair rather than as keyword
    # literals, because the repository scan reads ``access_key="..."`` as a
    # credential assignment, and a test that trains people to silence the
    # scan is worse than one that routes around its shape.
    access, signing = fixed_credentials()
    assert acrcloud.sign(access_key=access, timestamp="1700000000", signing_key=signing) == expected


def test_the_request_carries_the_access_key_and_never_the_signing_key():
    access, signing = fixed_credentials()
    request = acrcloud.request_for(b"pcm", access_key=access, signing_key=signing, timestamp="1700000000")
    assert request.fields["access_key"] == "an-access-key"
    assert request.fields["sample_bytes"] == "3"
    assert request.fields["timestamp"] == "1700000000"
    assert "a-signing-key" not in json.dumps(dict(request.fields))
    assert "a-signing-key" not in request.url
    assert request.url == f"https://{acrcloud.HOST}{acrcloud.ENDPOINT}"
    assert request.sample == b"pcm"


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------


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
        with pytest.raises(CratekitError) as excinfo:
            run(transport, duration_s=duration, ledger=ledger)
        assert excinfo.value.cause.reason in {
            "intake-recognition-spend-bound",
            "intake-recognition-failed",
        }
        assert transport.requests == []
    assert acrcloud.planned_calls(float("nan")) == 0
    assert acrcloud.planned_calls(float("inf")) == 0


def test_no_chunk_is_ever_taken_past_the_point_where_a_whole_one_fits():
    for whole in range(1, 400):
        for offset in acrcloud.sample_offsets(float(whole)):
            assert offset + acrcloud.CHUNK_S <= max(whole, acrcloud.CHUNK_S)


def test_a_two_hour_set_fits_under_the_per_run_bound_and_a_four_hour_file_does_not():
    assert len(acrcloud.sample_offsets(2 * 3600.0)) <= acrcloud.MAX_CALLS_PER_RUN
    assert len(acrcloud.sample_offsets(4 * 3600.0)) > acrcloud.MAX_CALLS_PER_RUN


# ---------------------------------------------------------------------------
# The response mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "payload, outcome",
    [
        (coded(0), Outcome.MATCH),
        (coded(1001), Outcome.MISS),
        (coded(2004), Outcome.MISS),
        (coded(3015), Outcome.MISS),
        (coded(3003), Outcome.QUOTA),
        (coded(3001), Outcome.AUTH),
        (coded(3002), Outcome.AUTH),
        (coded(3006), Outcome.AUTH),
        (coded(3014), Outcome.AUTH),
        (coded(2000), Outcome.TRANSIENT),
        (coded(2005), Outcome.TRANSIENT),
        (coded(2999), Outcome.TRANSIENT),
        (coded(3000), Outcome.TRANSIENT),
        (coded(3100), Outcome.TRANSIENT),
        (coded(9999), Outcome.UNCLASSIFIED),
        (coded(3005), Outcome.UNCLASSIFIED),
        (coded(3300), Outcome.UNCLASSIFIED),
        ({"status": {"msg": "no code"}}, Outcome.UNCLASSIFIED),
        ({"status": {"code": "0"}}, Outcome.UNCLASSIFIED),
        ({"status": {"code": True}}, Outcome.UNCLASSIFIED),
        ({"status": "broken"}, Outcome.UNCLASSIFIED),
        ({}, Outcome.UNCLASSIFIED),
    ],
)
def test_every_status_code_lands_in_exactly_one_family(payload, outcome):
    found, _code, _message = acrcloud.classify(payload)
    assert found is outcome


def test_a_quota_a_credential_or_a_transient_answer_is_never_read_as_a_miss():
    """The 565 call batch. A quota answer that reads as a miss is the defect."""
    for code in (3003, 3001, 3002, 3006, 3014, 2000, 2005, 3000, 3100, 9999):
        assert acrcloud.classify(coded(code))[0] is not Outcome.MISS


def test_a_chunk_nothing_could_be_fingerprinted_from_is_a_miss_not_a_quota():
    """3015 was the source system's second quota code, and it is the service
    saying this chunk carried nothing to fingerprint, which is a fact about
    the audio. Reading it as quota ended a whole set on one silent chunk."""
    for code in (2004, 3015):
        assert acrcloud.classify(coded(code))[0] is Outcome.MISS


def test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept():
    found = acrcloud.parse_match(
        hit("Aurora Bloom", "Sun Path (Someone Remix)", isrc="QZABC2600001", score=87),
        offset_s=25,
    )
    assert found is not None
    assert found.offset_s == 25
    assert found.score == 87
    assert found.wanted.artist == "Aurora Bloom"
    assert found.wanted.title == "Sun Path"
    assert found.wanted.version == "Someone Remix"
    assert found.wanted.isrc == "QZABC2600001"
    assert found.wanted.spelled == "Sun Path (Someone Remix)"
    assert found.wanted.ref == "", "a recognised track carries no provider identifier"


def test_the_primary_artist_is_the_first_named_and_never_a_join():
    found = acrcloud.parse_match(
        hit("Aurora Bloom", "Sun Path", extra_artist="Nova Reef"), offset_s=0
    )
    assert found is not None
    assert found.wanted.artist == "Aurora Bloom"


def test_a_match_naming_no_artist_or_no_title_is_none_rather_than_half_a_row():
    payload = hit("Aurora Bloom", "Sun Path")
    payload["metadata"]["music"][0]["artists"] = []
    assert acrcloud.parse_match(payload, offset_s=0) is None
    payload = hit("Aurora Bloom", "Sun Path")
    payload["metadata"]["music"][0]["title"] = "   "
    assert acrcloud.parse_match(payload, offset_s=0) is None


def test_a_match_with_no_music_and_a_malformed_score_are_handled():
    assert acrcloud.parse_match({"status": {"code": 0}, "metadata": {"music": []}}, offset_s=0) is None
    assert acrcloud.parse_match({"status": {"code": 0}, "metadata": {"music": "x"}}, offset_s=0) is None
    payload = hit("Aurora Bloom", "Sun Path", score=90)
    payload["metadata"]["music"][0]["score"] = "high"
    found = acrcloud.parse_match(payload, offset_s=0)
    assert found is not None and found.score == 0


def _match(offset: int, artist: str, title: str, *, isrc: str = "", score: int = 80) -> Match:
    found = acrcloud.parse_match(hit(artist, title, isrc=isrc, score=score), offset_s=offset)
    assert found is not None
    return found


def test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score():
    folded = acrcloud.fold(
        [
            _match(0, "Aurora Bloom", "Sun Path", isrc="X1", score=70),
            _match(25, "Aurora Bloom", "Sun Path", isrc="X1", score=95),
            _match(50, "Aurora Bloom", "Sun Path", isrc="X1", score=80),
            _match(75, "Nova Reef", "Tide", isrc="X2", score=60),
        ]
    )
    assert [(m.offset_s, m.wanted.title, m.score) for m in folded] == [
        (0, "Sun Path", 95),
        (75, "Tide", 60),
    ]


def test_a_record_played_twice_in_a_set_stays_twice():
    folded = acrcloud.fold(
        [
            _match(0, "Aurora Bloom", "Sun Path", isrc="X1"),
            _match(25, "Nova Reef", "Tide", isrc="X2"),
            _match(50, "Aurora Bloom", "Sun Path", isrc="X1"),
        ]
    )
    assert [m.wanted.title for m in folded] == ["Sun Path", "Tide", "Sun Path"]


def test_without_an_isrc_the_recording_token_decides_and_a_version_is_a_different_record():
    folded = acrcloud.fold(
        [
            _match(0, "Aurora Bloom", "Sun Path"),
            _match(25, "aurora bloom", "SUN PATH"),
            _match(50, "Aurora Bloom", "Sun Path (Someone Remix)"),
        ]
    )
    assert [(m.wanted.title, m.wanted.version) for m in folded] == [
        ("Sun Path", ""),
        ("Sun Path", "Someone Remix"),
    ]


def test_two_isrcs_that_differ_do_not_fold_even_when_the_names_agree():
    folded = acrcloud.fold(
        [
            _match(0, "Aurora Bloom", "Sun Path", isrc="X1"),
            _match(25, "Aurora Bloom", "Sun Path", isrc="X2"),
        ]
    )
    assert len(folded) == 2


# ---------------------------------------------------------------------------
# Identification through the fakes
# ---------------------------------------------------------------------------


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
    assert (result.calls, result.misses) == (2, 2)
    assert ledger.used("2026-09") == 2


def test_the_per_run_bound_refuses_before_any_carve_call_or_credential(ledger):
    transport = FakeTransport()
    asked = []

    def credentials():
        asked.append(True)
        return fixed_credentials()

    carver = FakeCarver(3600.0)
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.identify(
            Path("set.mp3"),
            transport=transport,
            carver=carver,
            credentials=credentials,
            budget=Budget(per_run=10),
            ledger=ledger,
            month="2026-09",
        )
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail["kind"] == "per-run"
    assert cause.detail["planned"] == len(acrcloud.sample_offsets(3600.0))
    assert cause.detail["bound"] == 10
    assert transport.requests == []
    assert carver.carved == []
    assert asked == [], "the keychain was asked before the budget was checked"
    assert ledger.used("2026-09") == 0


def test_the_monthly_bound_counts_what_the_ledger_already_holds(ledger):
    ledger.record(95, "2026-09")
    transport = FakeTransport()
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=100.0, budget=Budget(monthly=98), ledger=ledger)
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail == {"planned": 4, "used": 95, "bound": 98, "kind": "monthly"}
    assert cause.remediation.remedy == Remedy.RETRY_LATER
    assert transport.requests == []
    # A plan that fits exactly is allowed: 85 seconds is three chunks.
    fits = FakeTransport(miss(), miss(), miss())
    run(fits, duration_s=85.0, budget=Budget(monthly=98), ledger=ledger)
    assert len(fits.requests) == 3
    assert ledger.used("2026-09") == 98


def test_the_default_budget_bounds_the_run_and_not_the_month():
    assert Budget() == Budget(per_run=acrcloud.MAX_CALLS_PER_RUN, monthly=None)


def test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss(ledger):
    transport = FakeTransport(
        hit("Aurora Bloom", "Sun Path", isrc="X1"), coded(3003, "requests limit exceeded"), miss()
    )
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=60.0, ledger=ledger)
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-spend-bound"
    assert cause.detail["kind"] == "provider-quota"
    assert cause.detail["code"] == 3003
    assert cause.detail["calls"] == 2
    assert cause.remediation.remedy == Remedy.RETRY_LATER
    assert len(transport.requests) == 2, "a call was made after the quota answer"
    assert ledger.used("2026-09") == 2, "the calls made before the refusal were not counted"


def test_the_two_spend_refusals_and_a_miss_are_three_different_things(ledger):
    bound = pytest.raises(CratekitError)
    with bound as own:
        run(FakeTransport(), duration_s=100.0, budget=Budget(per_run=1), ledger=ledger)
    with bound as theirs:
        run(FakeTransport(coded(3003)), duration_s=20.0, ledger=ledger)
    missed = run(FakeTransport(miss()), duration_s=20.0, ledger=ledger)
    assert own.value.cause.reason == theirs.value.cause.reason == "intake-recognition-spend-bound"
    assert own.value.cause.detail["kind"] != theirs.value.cause.detail["kind"]
    assert missed.rows == () and missed.misses == 1


def test_a_credential_answer_ends_the_run_as_auth_failed(ledger):
    transport = FakeTransport(coded(3001, "invalid access key"), miss())
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=60.0, ledger=ledger)
    cause = excinfo.value.cause
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
    transport = FakeTransport(ConnectionError("down"), ConnectionError("down"))
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=40.0, ledger=ledger)
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-failed"
    assert cause.retryable is True
    assert cause.detail["calls"] == 2
    assert ledger.used("2026-09") == 2


def test_an_answer_this_build_cannot_classify_stops_the_run_naming_the_code(ledger):
    transport = FakeTransport(hit("Aurora Bloom", "Sun Path"), coded(3005, "something new"), miss())
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=60.0, ledger=ledger)
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-failed"
    assert cause.detail["code"] == 3005
    assert cause.detail["calls"] == 2
    assert len(transport.requests) == 2


def test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call(ledger):
    class Unreadable(FakeCarver):
        def duration(self, source: Path) -> float:
            raise RuntimeError("ffprobe could not read it")

    transport = FakeTransport()
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.identify(
            Path("set.mp3"), transport=transport, carver=Unreadable(0.0),
            credentials=fixed_credentials, ledger=ledger, month="2026-09",
        )
    assert excinfo.value.cause.reason == "intake-recognition-failed"
    assert transport.requests == []

    class Uncarvable(FakeCarver):
        def carve(self, source: Path, offset_s: int, chunk_s: int) -> bytes:
            if offset_s == 25:
                raise RuntimeError("ffmpeg died")
            return super().carve(source, offset_s, chunk_s)

    transport = FakeTransport(miss(), miss())
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.identify(
            Path("set.mp3"), transport=transport, carver=Uncarvable(60.0),
            credentials=fixed_credentials, ledger=ledger, month="2026-09",
        )
    assert excinfo.value.cause.reason == "intake-recognition-failed"
    assert excinfo.value.cause.detail["offset_s"] == 25
    assert len(transport.requests) == 1


def test_an_empty_recording_sends_nothing(ledger):
    with pytest.raises(CratekitError) as excinfo:
        run(FakeTransport(), duration_s=0.0, ledger=ledger)
    assert excinfo.value.cause.reason == "intake-recognition-failed"
    assert ledger.used("2026-09") == 0


# ---------------------------------------------------------------------------
# The ledger
# ---------------------------------------------------------------------------


def test_the_ledger_is_keyed_by_month_and_survives_a_corrupt_file(tmp_path):
    ledger = Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")
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


def test_recording_nothing_writes_nothing(tmp_path):
    ledger = Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")
    assert ledger.record(0, "2026-09") == 0
    assert not (tmp_path / "usage.json").exists()


def test_the_ledger_lives_in_the_declared_installation_state_entries():
    ledger = Ledger()
    from cratekit.core import config

    assert ledger.path == config.state_path(acrcloud.LEDGER_KEY)
    assert ledger.lock_path == config.state_path(acrcloud.LEDGER_LOCK_KEY)
    assert ledger.path.parent == ledger.lock_path.parent


def test_the_month_key_is_the_calendar_month():
    from datetime import datetime

    assert acrcloud.current_month(datetime(2026, 9, 9, 23, 59)) == "2026-09"
    assert acrcloud.current_month(datetime(2026, 1, 1, 0, 0)) == "2026-01"


# ---------------------------------------------------------------------------
# The credentials and the seam
# ---------------------------------------------------------------------------


def test_the_keychain_credentials_are_read_by_name_after_the_gate():
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")
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
    one is the wrong instruction the secrets module names three types to
    avoid, so the exception's remedy is the one passed on."""

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


def test_the_seam_binds_this_identifier_when_none_is_injected(monkeypatch, tmp_path):
    """``recognize.identify`` with no identifier is the paid path, over the
    shipped seams, which are looked up on the module at call time."""
    source = tmp_path / "set.mp3"
    source.write_bytes(b"ID3")
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    transport = FakeTransport(hit("Aurora Bloom", "Sun Path", isrc="X1"))
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(20.0))
    ledger = Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")
    monkeypatch.setattr(acrcloud, "Ledger", lambda: ledger)

    found = recognize.identify(source)

    assert isinstance(found, Identified)
    assert [(row.artist, row.title) for row in found.rows] == [("Aurora Bloom", "Sun Path")]
    assert (found.calls, found.chunks, found.misses, found.unreached) == (1, 1, 0, 0)
    assert transport.requests[0].fields["access_key"] == "k-1"
    assert ledger.used() == 1


def test_the_gate_still_refuses_with_no_credentials_before_the_seam_is_touched(monkeypatch, tmp_path):
    source = tmp_path / "set.mp3"
    source.write_bytes(b"ID3")
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    transport = FakeTransport()
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(20.0))
    with pytest.raises(CratekitError) as excinfo:
        recognize.identify(source)
    assert excinfo.value.cause.reason == "intake-recognition-unready"
    assert transport.requests == []


def test_the_bound_identifier_resolves_its_seams_at_call_time(monkeypatch, tmp_path):
    identifier = acrcloud.bound_identifier()
    transport = FakeTransport(miss())
    monkeypatch.setattr(acrcloud, "http_transport", transport)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(5.0))
    ledger = Ledger(path=tmp_path / "usage.json", lock_path=tmp_path / "usage.lock")
    monkeypatch.setattr(acrcloud, "Ledger", lambda: ledger)
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")
    assert identifier(Path("set.mp3")).rows == ()
    assert len(transport.requests) == 1


def test_a_fake_identifier_answering_bare_rows_is_normalised_by_the_seam(monkeypatch, tmp_path):
    monkeypatch.setattr(recognize.secrets, "exists", lambda name: True)
    monkeypatch.setattr(recognize.binaries, "find", lambda name: f"/usr/bin/{name}")
    found = recognize.identify(tmp_path / "x.mp3", identifier=lambda path: (match_row("A", "T"),))
    assert isinstance(found, Identified)
    assert [row.title for row in found.rows] == ["T"]
    assert (found.calls, found.chunks, found.misses, found.unreached) == (0, 0, 0, 0)


def match_row(artist: str, title: str):
    from cratekit.acquire.match import Wanted

    return Wanted(artist=artist, title=title)


# ---------------------------------------------------------------------------
# The stop on a service that stops answering
# ---------------------------------------------------------------------------


def test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent(ledger):
    """An offline machine costs a handful of attempts, not a whole set."""
    transport = FakeTransport(*([ConnectionError("down")] * 20))
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=600.0, ledger=ledger)
    cause = excinfo.value.cause
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
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=600.0, ledger=ledger)
    assert excinfo.value.cause.reason == "intake-recognition-failed"
    assert "HTTP 403" in excinfo.value.cause.message
    assert len(transport.requests) == acrcloud.UNREACHED_STOP


def test_a_ledger_that_cannot_record_stops_the_run_before_the_call(ledger, monkeypatch):
    from cratekit.core import config

    def unlockable(calls, month=None):
        raise config.ConfigLockUnavailable("the state directory is read only")

    monkeypatch.setattr(ledger, "record", unlockable)
    transport = FakeTransport(miss())
    with pytest.raises(CratekitError) as excinfo:
        run(transport, duration_s=20.0, ledger=ledger)
    assert excinfo.value.cause.reason == "intake-recognition-failed"
    assert excinfo.value.cause.detail["calls"] == 0
    assert transport.requests == [], "a call was made that the ledger could not count"


# ---------------------------------------------------------------------------
# U103: the recognition cache. A chunk already answered is not paid for again.
# ---------------------------------------------------------------------------


@pytest.fixture
def cache(tmp_path) -> acrcloud.RecognitionCache:
    return acrcloud.RecognitionCache(root=tmp_path / "identify_cache")


def real_recording(tmp_path, content: bytes = b"a recording", name: str = "set.mp3") -> Path:
    path = tmp_path / name
    path.write_bytes(content)
    return path


def counted_credentials():
    """Credentials that count how often the keychain was asked."""
    asked: list[int] = []

    def read() -> tuple[str, str]:
        asked.append(1)
        return fixed_credentials()

    read.asked = asked
    return read


def cached_run(transport, source, cache, ledger, *, duration_s=85.0, **kwargs) -> Identified:
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


def three_answers() -> list[dict]:
    return [hit("Aurora Bloom", "Sun Path", isrc="X1"), miss(), hit("Nova Reef", "Tide", isrc="X2")]


def test_a_second_pass_over_an_unchanged_recording_spends_nothing(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    first = cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    assert (first.calls, first.cached, first.cache_unwritten) == (3, 0, "")

    silent = FakeTransport()
    carver = FakeCarver(85.0)
    credentials = counted_credentials()
    second = cached_run(silent, source, cache, ledger, carver=carver, credentials=credentials)

    assert silent.requests == [], "a kept chunk reached the transport"
    assert carver.carved == [], "a kept chunk was carved"
    assert credentials.asked == [], "a pass that owes nothing asked the keychain"
    assert ledger.used("2026-09") == 3, "a kept chunk was counted as spend"
    assert second.rows == first.rows
    assert (second.calls, second.cached, second.chunks) == (0, 3, 3)
    assert (second.misses, second.unreached) == (first.misses, first.unreached)


def test_a_changed_file_misses_the_cache(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    source.write_bytes(b"a different recording under the same name")

    again = FakeTransport(miss(), miss(), miss())
    result = cached_run(again, source, cache, ledger)

    assert len(again.requests) == 3, "a changed file was served the old answers"
    assert result.rows == ()
    assert result.cached == 0


def test_the_same_bytes_under_another_name_hit_the_cache(tmp_path, cache, ledger):
    """The identity is the audio. A copy is the same recording."""
    cached_run(FakeTransport(*three_answers()), real_recording(tmp_path), cache, ledger)
    copy = real_recording(tmp_path, name="a copy.mp3")
    silent = FakeTransport()
    assert cached_run(silent, copy, cache, ledger).cached == 3
    assert silent.requests == []


def test_a_changed_chunk_plan_misses_the_cache(tmp_path, cache, ledger):
    """The same bytes measured to a different length are a different grid."""
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger, duration_s=85.0)
    longer = FakeTransport(miss(), miss(), miss(), miss())
    result = cached_run(longer, source, cache, ledger, duration_s=100.0)
    assert len(longer.requests) == 4
    assert result.cached == 0


def test_another_regional_host_misses_the_cache(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    other = FakeTransport(miss(), miss(), miss())
    cached_run(other, source, cache, ledger, host="identify-eu-west-1.example.invalid")
    assert len(other.requests) == 3


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
    base = dict(digest="d", offsets=(0, 25, 50))
    assert acrcloud.ChunkPlan(**base).key() != acrcloud.ChunkPlan(**{**base, **changed}).key()
    assert acrcloud.ChunkPlan(**base).key() == acrcloud.ChunkPlan(**base).key()


def test_the_digest_is_the_sha256_of_the_bytes(tmp_path):
    source = real_recording(tmp_path, b"exactly these bytes")
    assert acrcloud.content_digest(source) == hashlib.sha256(b"exactly these bytes").hexdigest()


def test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again(
    tmp_path, cache, ledger
):
    source = real_recording(tmp_path)
    first = cached_run(
        FakeTransport(hit("Aurora Bloom", "Sun Path"), ConnectionError("down"), coded(3000)),
        source, cache, ledger,
    )
    assert first.unreached == 2

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


def test_a_pass_that_raised_keeps_nothing(tmp_path, cache, ledger):
    """R-304's other half, stated as a test so nobody reads the cache as a resume."""
    source = real_recording(tmp_path)
    with pytest.raises(CratekitError):
        cached_run(FakeTransport(hit("Aurora Bloom", "Sun Path"), coded(3003)), source, cache, ledger)
    assert not cache.root.exists() or not list(cache.root.iterdir())


def plan_of(source: Path, duration_s: float = 85.0) -> acrcloud.ChunkPlan:
    return acrcloud.ChunkPlan(
        digest=acrcloud.content_digest(source), offsets=acrcloud.sample_offsets(duration_s)
    )


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
    source = real_recording(tmp_path)
    plan = plan_of(source)
    cache.write(plan, {0: miss()})
    assert cache.read(plan) == {0: miss()}
    held = json.loads(cache.path_for(plan).read_text())
    held["version"] = acrcloud.CACHE_VERSION + 1
    cache.path_for(plan).write_text(json.dumps(held))
    assert cache.read(plan) == {}


def test_only_an_answer_is_kept_or_served_in_either_direction(tmp_path, cache):
    """Removed alone, each layer still holds: the writer drops a non answer,
    and the reader refuses one a foreign writer left behind."""
    source = real_recording(tmp_path)
    plan = plan_of(source)
    cache.write(plan, {0: hit("Aurora Bloom", "Sun Path"), 25: coded(3003), 50: coded(3000)})
    assert sorted(json.loads(cache.path_for(plan).read_text())["answers"]) == ["0"]

    held = json.loads(cache.path_for(plan).read_text())
    held["answers"].update({"25": coded(3003), "50": "not an object", "75": miss(), "x": miss()})
    cache.path_for(plan).write_text(json.dumps(held))
    assert sorted(cache.read(plan)) == [0], "a non answer or an unplanned offset was served"


def test_the_cache_lives_in_its_declared_installation_state_entry():
    from cratekit.core import config

    assert acrcloud.RecognitionCache().root == config.state_path(acrcloud.CACHE_KEY)
    assert config.state_file(acrcloud.CACHE_KEY).root is config.StateRoot.INSTALLATION


def test_the_cache_document_is_private_and_holds_no_credential(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    (document,) = list(cache.root.iterdir())
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


def test_answers_that_cannot_be_kept_do_not_fail_the_pass_that_paid_for_them(
    tmp_path, cache, ledger, monkeypatch
):
    def failing(self, plan, answers):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(acrcloud.RecognitionCache, "write", failing)
    result = cached_run(FakeTransport(*three_answers()), real_recording(tmp_path), cache, ledger)
    assert [row.title for row in result.rows] == ["Sun Path", "Tide"]
    assert "PermissionError" in result.cache_unwritten


def test_a_pass_that_paid_for_nothing_writes_nothing_and_reports_nothing_unwritten(
    tmp_path, cache, ledger, monkeypatch
):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)

    def failing(self, plan, answers):
        raise AssertionError("a pass that paid for nothing rewrote the cache")

    monkeypatch.setattr(acrcloud.RecognitionCache, "write", failing)
    assert cached_run(FakeTransport(), source, cache, ledger).cache_unwritten == ""


def test_the_monthly_bound_reads_what_is_owed_and_the_per_run_bound_reads_the_grid(
    tmp_path, cache, ledger
):
    source = real_recording(tmp_path)
    cached_run(FakeTransport(*three_answers()), source, cache, ledger)
    spent = Budget(monthly=3)
    # The month is used up and the recording is fully kept: nothing is owed.
    assert cached_run(FakeTransport(), source, cache, ledger, budget=spent).cached == 3
    # The per run bound still refuses a grid this size, kept or not.
    with pytest.raises(CratekitError) as refused:
        cached_run(FakeTransport(), source, cache, ledger, budget=Budget(per_run=2))
    assert refused.value.cause.detail["kind"] == "per-run"
    # And a recording that owes calls into a spent month is refused for them.
    other = real_recording(tmp_path, b"another recording", name="other.mp3")
    with pytest.raises(CratekitError) as monthly:
        cached_run(FakeTransport(), other, cache, ledger, budget=spent)
    assert monthly.value.cause.detail == {"planned": 3, "used": 3, "bound": 3, "kind": "monthly"}


def test_the_bound_identifier_hands_the_cache_through(tmp_path, cache, ledger):
    source = real_recording(tmp_path)
    transport = FakeTransport(*three_answers())
    identifier = acrcloud.bound_identifier(
        transport=transport, carver=FakeCarver(85.0), ledger=ledger, cache=cache
    )
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-1")
    assert identifier(source).calls == 3
    assert identifier(source).calls == 0
