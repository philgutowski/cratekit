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
from cratekit.intake.acrcloud import (
    Budget,
    Ledger,
    Match,
    Outcome,
    Request,
    Response,
)

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
) -> acrcloud.Recognition:
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
        (coded(3003), Outcome.QUOTA),
        (coded(3015), Outcome.QUOTA),
        (coded(3001), Outcome.AUTH),
        (coded(3002), Outcome.AUTH),
        (coded(3006), Outcome.AUTH),
        (coded(3014), Outcome.AUTH),
        (coded(2004), Outcome.TRANSIENT),
        (coded(2999), Outcome.TRANSIENT),
        (coded(3000), Outcome.TRANSIENT),
        (coded(9999), Outcome.UNCLASSIFIED),
        (coded(3005), Outcome.UNCLASSIFIED),
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


def test_a_non_zero_code_is_never_read_as_a_miss():
    """The 565 call batch. A quota answer that reads as a miss is the defect."""
    for code in (3003, 3015, 3001, 3002, 3006, 3014, 2004, 3000, 9999):
        assert acrcloud.classify(coded(code))[0] is not Outcome.MISS


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
        run(FakeTransport(coded(3015)), duration_s=20.0, ledger=ledger)
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
        coded(2004, "decode error"),
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


def test_a_credential_the_keychain_will_not_hand_over_is_the_gate_class():
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-1")
    with pytest.raises(CratekitError) as excinfo:
        acrcloud.keychain_credentials()
    cause = excinfo.value.cause
    assert cause.reason == "intake-recognition-unready"
    assert cause.remediation.remedy == Remedy.SET_CREDENTIAL
    assert cause.detail["credential"] == str(secrets.Credential.IDENTIFY_SIGNING_KEY)


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

    rows = recognize.identify(source)

    assert [(row.artist, row.title) for row in rows] == [("Aurora Bloom", "Sun Path")]
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
    assert identifier(Path("set.mp3")) == ()
    assert len(transport.requests) == 1
