"""U206: an ISRC the provider already answered is not asked again.

The cache sits at the two lookup seams, the outbound account's ``match_track``
and the catalogue's ``tracks_for_isrc``, and every scenario here is driven
through one of those two shipped classes over a fake client that counts what it
is asked. The client's own exception classes are used where the seams read a
failure by its class, because a fake class of the same name is a measurement
taken on something authored alongside the fix.

D1 applies. Every ISRC here is in a registrant range nobody holds.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import tidalapi
from tidalapi.exceptions import InvalidISRC, ObjectNotFound, TooManyRequests

from cratekit.acquire import isrc_cache, match
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.label import tidal_catalogue
from cratekit.modules.outbound import tidal_account
from tests.test_config import valid_data

ONE = "QZAAA2600001"
TWO = "QZAAA2600002"
DAY = isrc_cache.DAY_S
SRC_ROOT = Path(isrc_cache.__file__).resolve().parents[2]


# ═══════════════════════════════════════════════════════════════════════════
# Fakes: a client that answers from memory and counts every ISRC it is asked
# ═══════════════════════════════════════════════════════════════════════════


class Artist:
    def __init__(self, name: str) -> None:
        self.name = name


class Album:
    def __init__(self, name: str) -> None:
        self.name = name


class Track:
    """A provider track in the client's own shape."""

    def __init__(
        self,
        track_id: str,
        name: str = "",
        version: str | None = None,
        artists: tuple[str, ...] = (),
        album: str = "",
    ) -> None:
        self.id = int(track_id)
        self.name = name
        self.title = name
        self.version = version
        self.artists = [Artist(one) for one in artists]
        self.artist = self.artists[0] if self.artists else None
        self.album = Album(album) if album else None
        self.available = True


class Response:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class HTTPFailure(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"HTTP {status_code}")
        self.response = Response(status_code)


class Client:
    """Answers ``get_tracks_by_isrc`` from ``answers``: a track list, or an
    exception class or instance to raise. ``failures`` are raised first, one per
    call, before the answer is given."""

    def __init__(self, answers: dict | None = None, *, country: str | None = "GB") -> None:
        self.answers = dict(answers or {})
        self.failures: list[BaseException] = []
        self.asked: list[str] = []
        if country is not None:
            self.country_code = country

    def get_tracks_by_isrc(self, isrc: str):
        self.asked.append(isrc)
        if self.failures:
            raise self.failures.pop(0)
        answer = self.answers.get(isrc, ObjectNotFound)
        if isinstance(answer, BaseException) or (
            isinstance(answer, type) and issubclass(answer, BaseException)
        ):
            raise answer() if isinstance(answer, type) else answer
        return list(answer)


class Clock:
    def __init__(self, now: float = 1_800_000_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


@pytest.fixture
def clock() -> Clock:
    return Clock()


def cache(clock: Clock, days: int = 30) -> isrc_cache.Cache:
    return isrc_cache.Cache(days=days, clock=clock, sleep=lambda _: None)


def account(client: Client, made: isrc_cache.Cache) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(client, sleep=lambda _: None, cache=made)


def catalogue(client: Client, made: isrc_cache.Cache, monkeypatch) -> tidal_catalogue.TidalCatalogue:
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda _: None)
    return tidal_catalogue.TidalCatalogue(client, cache=made)


def single(track_id: str = "9001") -> list[Track]:
    return [Track(track_id, "Sun Path", artists=("Aurora Bloom",), album="Sun Path EP")]


def stored() -> dict:
    return json.loads(config.state_path(isrc_cache.STATE_KEY).read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════════════════
# An answer is asked once, by either seam, from any instance
# ═══════════════════════════════════════════════════════════════════════════


def test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc(clock):
    first = Client({ONE: single()})
    assert account(first, cache(clock)).match_track(identity="1", isrc=ONE) == "9001"
    second = Client({ONE: single()})

    assert account(second, cache(clock)).match_track(identity="1", isrc=ONE) == "9001"

    assert first.asked == [ONE]
    assert second.asked == []


def test_the_cache_file_sits_beside_the_provider_gate_not_under_the_library():
    assert config.state_file(isrc_cache.STATE_KEY).root is config.StateRoot.INSTALLATION
    assert config.state_file(isrc_cache.LOCK_KEY).root is config.StateRoot.INSTALLATION
    assert (
        config.state_path(isrc_cache.STATE_KEY).parent
        == config.state_path("provider_gate").parent
    )


def test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call(clock):
    """Two releases under one ISRC, one the row's version: ``_among`` chooses
    from the remembered tracks exactly as it chose from the live ones."""
    answer = [
        Track("9001", "Sun Path", artists=("Aurora Bloom",)),
        Track("9002", "Sun Path", version="Extended Mix", artists=("Aurora Bloom",)),
    ]
    live = Client({ONE: answer})
    row = {"identity": "1", "isrc": ONE, "title": "Sun Path (Extended Mix)", "artist": "Aurora Bloom"}
    assert account(live, cache(clock)).match_track(**row) == "9002"
    again = Client({ONE: answer})

    assert account(again, cache(clock)).match_track(**row) == "9002"
    assert again.asked == []


def test_a_tie_remembered_is_still_refused_with_its_reason(clock):
    answer = [
        Track("9001", "Sun Path", artists=("Aurora Bloom",), album="One"),
        Track("9002", "Sun Path", artists=("Aurora Bloom",), album="Two"),
    ]
    live = account(Client({ONE: answer}), cache(clock))
    live._hearts = set()
    row = {"identity": "1", "isrc": ONE, "title": "Sun Path", "artist": "Aurora Bloom"}
    assert live.match_track(**row) is None
    said = live.unmatched_reason("1")
    again = account(Client({ONE: answer}), cache(clock))
    again._hearts = set()

    assert again.match_track(**row) is None
    assert again.unmatched_reason("1") == said
    assert again._session.asked == []


def test_the_catalogue_and_the_account_share_one_answer(clock, monkeypatch):
    client = Client({ONE: single()})
    found = catalogue(client, cache(clock), monkeypatch).tracks_for_isrc(ONE)
    assert [str(track.id) for track in found] == ["9001"]
    later = Client({ONE: single()})

    assert account(later, cache(clock)).match_track(identity="1", isrc=ONE) == "9001"
    assert later.asked == []


def test_the_catalogue_answers_a_remembered_isrc_with_no_call(clock, monkeypatch):
    catalogue(Client({ONE: single()}), cache(clock), monkeypatch).tracks_for_isrc(ONE)
    again = Client({ONE: single()})

    found = catalogue(again, cache(clock), monkeypatch).tracks_for_isrc(ONE)

    assert [track.id for track in found] == ["9001"]
    assert again.asked == []


def test_a_different_country_is_a_different_key(clock):
    account(Client({ONE: single()}, country="GB"), cache(clock)).match_track(identity="1", isrc=ONE)
    elsewhere = Client({ONE: single()}, country="US")

    account(elsewhere, cache(clock)).match_track(identity="1", isrc=ONE)

    assert elsewhere.asked == [ONE]
    assert sorted(stored()["entries"]) == [f"{ONE}|GB", f"{ONE}|US"]


def test_a_spelling_that_is_not_its_own_fold_is_asked_and_never_kept(clock):
    lower = ONE.lower()
    client = Client({lower: single()})
    made = cache(clock)
    account(client, made).match_track(identity="1", isrc=lower)
    account(client, made).match_track(identity="1", isrc=lower)

    assert client.asked == [lower, lower]
    assert not config.state_path(isrc_cache.STATE_KEY).exists()


# ═══════════════════════════════════════════════════════════════════════════
# A not found is kept for a week, a found answer for the configured days
# ═══════════════════════════════════════════════════════════════════════════


def test_a_not_found_is_kept_and_asked_again_after_seven_days(clock):
    client = Client({})
    made = cache(clock)
    assert account(client, made).match_track(identity="1", isrc=ONE) is None
    clock.now += 7 * DAY - 1
    assert account(client, made).match_track(identity="1", isrc=ONE) is None
    assert client.asked == [ONE]

    clock.now += 1
    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE]


def test_the_catalogue_keeps_a_not_found_too(clock, monkeypatch):
    client = Client({})
    made = cache(clock)
    assert catalogue(client, made, monkeypatch).tracks_for_isrc(ONE) == ()

    assert catalogue(client, made, monkeypatch).tracks_for_isrc(ONE) == ()
    assert client.asked == [ONE]


def test_a_found_answer_is_asked_again_after_the_configured_days(clock):
    client = Client({ONE: single()})
    made = cache(clock, days=3)
    account(client, made).match_track(identity="1", isrc=ONE)
    clock.now += 3 * DAY - 1
    account(client, made).match_track(identity="1", isrc=ONE)
    assert client.asked == [ONE]

    clock.now += 1
    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE]


def test_a_found_answer_lives_thirty_days_unless_set(clock):
    client = Client({ONE: single()})
    made = isrc_cache.Cache(clock=clock)
    account(client, made).match_track(identity="1", isrc=ONE)
    clock.now += 30 * DAY - 1
    account(client, made).match_track(identity="1", isrc=ONE)
    assert client.asked == [ONE]
    clock.now += 1
    account(client, made).match_track(identity="1", isrc=ONE)
    assert client.asked == [ONE, ONE]


def test_a_not_found_lives_no_longer_than_a_shorter_setting(clock):
    client = Client({})
    made = cache(clock, days=2)
    account(client, made).match_track(identity="1", isrc=ONE)
    clock.now += 2 * DAY

    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE]


def test_an_expired_answer_is_replaced_by_the_new_one(clock):
    made = cache(clock, days=1)
    account(Client({ONE: single("9001")}), made).match_track(identity="1", isrc=ONE)
    clock.now += DAY
    account(Client({ONE: single("9002")}), made).match_track(identity="1", isrc=ONE)
    again = Client({ONE: single("9003")})

    assert account(again, made).match_track(identity="1", isrc=ONE) == "9002"
    assert again.asked == []


def test_an_answer_stamped_later_than_now_is_asked_again(clock):
    client = Client({ONE: single()})
    made = cache(clock)
    account(client, made).match_track(identity="1", isrc=ONE)
    clock.now -= 60

    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE]


def test_zero_days_asks_every_time_and_writes_nothing(clock, monkeypatch):
    client = Client({ONE: single()})
    made = cache(clock, days=0)
    for _ in range(3):
        account(client, made).match_track(identity="1", isrc=ONE)
    catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)

    assert client.asked == [ONE] * 4
    assert not config.state_path(isrc_cache.STATE_KEY).exists()


# ═══════════════════════════════════════════════════════════════════════════
# Only an answer is kept
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "failure",
    [HTTPFailure(500), HTTPFailure(401), TooManyRequests("slow down")],
    ids=["outage", "rejected-session", "rate-limit"],
)
def test_a_failed_lookup_is_never_kept_and_the_next_one_asks(clock, failure):
    client = Client({ONE: single()})
    client.failures = [failure] * 6
    made = cache(clock)
    with pytest.raises(CratekitError):
        account(client, made).match_track(identity="1", isrc=ONE)
    client.failures = []
    asked_before = len(client.asked)

    assert account(client, made).match_track(identity="1", isrc=ONE) == "9001"
    assert len(client.asked) == asked_before + 1


def test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept(clock):
    """The client raises ``InvalidISRC`` for an outage as well (the solutions
    entry), so the account path's no match over it is not remembered."""
    client = Client({ONE: InvalidISRC})
    made = cache(clock)
    assert account(client, made).match_track(identity="1", isrc=ONE) is None
    client.answers[ONE] = single()

    assert account(client, made).match_track(identity="1", isrc=ONE) == "9001"
    assert client.asked == [ONE, ONE]


def test_an_invalid_isrc_on_the_catalogue_is_raised_and_never_kept(clock, monkeypatch):
    client = Client({ONE: InvalidISRC})
    made = cache(clock)
    with pytest.raises(InvalidISRC):
        catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)
    client.answers[ONE] = single()
    asked_before = len(client.asked)

    assert [t.id for t in catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)] == [9001]
    assert len(client.asked) == asked_before + 1


@pytest.mark.parametrize(
    "failure",
    [HTTPFailure(500), HTTPFailure(401), TooManyRequests("slow down")],
    ids=["outage", "rejected-session", "rate-limit"],
)
def test_the_catalogue_never_keeps_a_failure(clock, monkeypatch, failure):
    client = Client({ONE: single()})
    client.failures = [failure] * 10
    made = cache(clock)
    with pytest.raises(Exception):  # noqa: B017 - the ladder re-raises the client's own
        catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)
    client.failures = []
    asked_before = len(client.asked)

    catalogue(client, made, monkeypatch).tracks_for_isrc(ONE)

    assert len(client.asked) == asked_before + 1


def test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found(clock):
    client = Client({})
    client.failures = [HTTPFailure(500)]
    made = cache(clock)
    assert account(client, made).match_track(identity="1", isrc=ONE) is None

    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE], "the retry's not found was not kept"


def test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing(clock):
    """The account reads the retry's ``InvalidISRC`` as no match, and what the
    attempt before it said decides nothing about keeping it."""
    client = Client({ONE: InvalidISRC})
    client.failures = [HTTPFailure(503)]
    made = cache(clock)
    account(client, made).match_track(identity="1", isrc=ONE)

    account(client, made).match_track(identity="1", isrc=ONE)

    assert client.asked == [ONE, ONE, ONE]


# ═══════════════════════════════════════════════════════════════════════════
# The file: set aside when it does not parse, readable under two writers
# ═══════════════════════════════════════════════════════════════════════════


def test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds(clock):
    path = config.state_path(isrc_cache.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json", encoding="utf-8")
    client = Client({ONE: single()})
    made = cache(clock)

    assert account(client, made).match_track(identity="1", isrc=ONE) == "9001"

    aside = made.set_aside()
    assert len(aside) == 1 and aside[0].read_text(encoding="utf-8") == "{ not json"
    assert list(stored()["entries"]) == [f"{ONE}|GB"]


def test_a_file_of_another_shape_is_set_aside_too(clock):
    path = config.state_path(isrc_cache.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": 99, "entries": {}}), encoding="utf-8")
    made = cache(clock)

    account(Client({ONE: single()}), made).match_track(identity="1", isrc=ONE)

    assert len(made.set_aside()) == 1


def test_a_file_that_cannot_be_read_answers_nothing_and_is_left_alone(clock, monkeypatch):
    path = config.state_path(isrc_cache.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    real = Path.read_text

    def refused(self, *args, **kwargs):
        if self == path:
            raise PermissionError(13, "Permission denied", str(self))
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refused)
    client = Client({ONE: single()})
    made = cache(clock)

    assert account(client, made).match_track(identity="1", isrc=ONE) == "9001"
    assert account(client, made).match_track(identity="1", isrc=ONE) == "9001"
    assert client.asked == [ONE, ONE]
    monkeypatch.undo()
    assert path.read_text(encoding="utf-8") == "{}"
    assert made.set_aside() == ()


def test_another_processs_answer_written_since_this_one_read_survives(clock):
    mine = cache(clock)
    theirs = cache(clock)
    account(Client({ONE: single("9001")}), mine).match_track(identity="1", isrc=ONE)
    account(Client({TWO: single("9002")}), theirs).match_track(identity="2", isrc=TWO)
    account(Client({}), mine).match_track(identity="3", isrc="QZAAA2600003")

    assert sorted(stored()["entries"]) == [f"{ONE}|GB", f"{TWO}|GB", "QZAAA2600003|GB"]


WRITER = textwrap.dedent(
    """
    import sys
    from pathlib import Path
    from cratekit.acquire import isrc_cache

    class Track:
        def __init__(self, track_id):
            self.id = track_id
            self.name = "Sun Path"
            self.artists = []

    path, lock, first, count = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    made = isrc_cache.Cache(days=30, path=path, lock_path=lock)
    for index in range(first, first + count):
        code = f"QZAAA26{index:05d}"
        assert made.remember(code, "GB", [Track(str(index))]), code
    """
)


def test_two_writer_processes_leave_one_readable_file_holding_both(tmp_path):
    script = tmp_path / "writer.py"
    script.write_text(WRITER, encoding="utf-8")
    path, lock = tmp_path / "isrc_cache.json", tmp_path / "isrc_cache.lock"
    env = {"PYTHONPATH": str(SRC_ROOT), "PYTHONDONTWRITEBYTECODE": "1"}
    import os

    children = [
        subprocess.Popen(
            [sys.executable, str(script), str(path), str(lock), str(first), "40"],
            env={**os.environ, **env},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for first in (1, 101)
    ]
    for child in children:
        _out, err = child.communicate(timeout=120)
        assert child.returncode == 0, err

    entries = json.loads(path.read_text(encoding="utf-8"))["entries"]
    assert len(entries) == 80
    assert isrc_cache.Cache(days=30, path=path, lock_path=lock).count() == 80


# ═══════════════════════════════════════════════════════════════════════════
# A remembered track reads as the client's own track reads
# ═══════════════════════════════════════════════════════════════════════════


def _client_track(**fields) -> tidalapi.media.Track:
    """A real client track built offline, the solutions entry's method:
    constructing a ``Session`` makes no request."""
    session = tidalapi.Session()
    payload = {
        "id": 9001,
        "title": "Sun Path",
        "duration": 300,
        "allowStreaming": True,
        "streamReady": True,
        "isrc": ONE,
        "version": "Extended Mix",
        "trackNumber": 1,
        "volumeNumber": 1,
        "artist": {"id": 1, "name": "Aurora Bloom", "type": "MAIN"},
        "artists": [
            {"id": 1, "name": "Aurora Bloom", "type": "MAIN"},
            {"id": 2, "name": "Nova Reef", "type": "FEATURED"},
        ],
        "album": {"id": 77, "title": "Sun Path EP", "cover": None, "videoCover": None},
        **fields,
    }

    class Missing(dict):
        def __missing__(self, key):
            return None

    return tidalapi.media.Track(session).parse_track(Missing(payload))


@pytest.mark.parametrize("available", [True, False], ids=["streamable", "withdrawn"])
def test_a_remembered_client_track_reads_as_the_client_track_does(clock, available):
    live = _client_track(allowStreaming=available, streamReady=available)
    made = cache(clock)
    made.remember(ONE, "GB", [live])
    (kept,) = made.recall(ONE, "GB")

    def read(track):
        return match.read_row(track, origin=match.TIDAL, position=1)

    assert read(kept) == read(live)
    assert str(kept.id) == str(live.id)
    assert tidal_account._streamable(kept) == tidal_account._streamable(live)
    assert tidal_account._album_name(kept) == tidal_account._album_name(live)
    assert tidal_account._artist_names(kept) == tidal_account._artist_names(live)
    assert tidal_account._shown_artist(kept) == tidal_account._shown_artist(live)
    for row in ("Sun Path (Extended Mix)", "Sun Path"):
        wanted = tidal_account._row_of(row, "Aurora Bloom, Nova Reef")
        assert tidal_account._agrees(wanted, kept) == tidal_account._agrees(wanted, live)


# ═══════════════════════════════════════════════════════════════════════════
# The setting and the counts
# ═══════════════════════════════════════════════════════════════════════════


def test_the_setting_reaches_the_cache_both_openers_build(tmp_path, monkeypatch):
    from cratekit.acquire import provider_session

    root = tmp_path / "library"
    built = config.from_dict(valid_data(root, provider={"isrc_cache_days": 4}))
    monkeypatch.setattr(provider_session, "client_session", lambda gate=None: Client({}))

    assert tidal_account.open_account(built)._cache.days == 4
    assert tidal_catalogue.open_catalogue(built)._cache.days == 4
    assert tidal_account.open_account()._cache.days == config.DEFAULT_PROVIDER_ISRC_CACHE_DAYS


@pytest.mark.parametrize("value", [-1, 1.5, True, "30"])
def test_a_days_value_that_is_not_a_whole_number_of_days_is_refused(tmp_path, value):
    problems = config.validate(valid_data(tmp_path / "library", provider={"isrc_cache_days": value}))
    assert len(problems) == 1
    assert "provider.isrc_cache_days" in problems[0]


def test_zero_days_is_a_valid_setting(tmp_path):
    assert config.validate(valid_data(tmp_path / "library", provider={"isrc_cache_days": 0})) == []


def test_the_process_counts_say_what_the_cache_settled_and_what_was_asked(clock):
    before = isrc_cache.process_lookups()
    made = cache(clock)
    account(Client({ONE: single()}), made).match_track(identity="1", isrc=ONE)
    account(Client({ONE: single()}), made).match_track(identity="1", isrc=ONE)
    account(Client({ONE: single()}), made).match_track(identity="1", isrc=ONE)

    assert isrc_cache.process_lookups().since(before) == isrc_cache.Lookups(remembered=2, asked=1)


# ═══════════════════════════════════════════════════════════════════════════
# Doctor names what the cache holds and every file it set aside
# ═══════════════════════════════════════════════════════════════════════════


def _doctor_note(cfg=None):
    from cratekit.cli import doctor
    from cratekit.cli.doctor import Probes

    inputs = doctor._Inputs(cfg, None, Probes())
    check = next(c for c in doctor.CHECKS if c.key == doctor.ISRC_CACHE_CHECK)
    return doctor.answer(check, inputs)


def test_doctor_names_a_set_aside_file_and_never_fails():
    import time

    clock = Clock(time.time())
    path = config.state_path(isrc_cache.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json", encoding="utf-8")
    account(Client({ONE: single()}), cache(clock)).match_track(identity="1", isrc=ONE)

    finding = _doctor_note()

    assert finding.status.name == "INFO", finding
    assert "1 ISRC answer kept" in finding.detail
    assert "1 file that could not be parsed" in finding.detail
    assert f"{path.name}{isrc_cache.SET_ASIDE}" in finding.detail


def test_doctor_says_when_the_cache_is_off(tmp_path):
    built = config.from_dict(valid_data(tmp_path / "library", provider={"isrc_cache_days": 0}))

    finding = _doctor_note(built)

    assert finding.status.name == "INFO"
    assert "isrc_cache_days is 0" in finding.detail
