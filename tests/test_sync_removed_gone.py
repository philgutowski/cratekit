"""U320: ``crate sync removed`` offers a removal again past short hearts and a playlist gone for good.

A179's run at sitting 101 was partial every time: synced playlists the account
no longer lists whose ids did not open, and hearts the provider withheld. Both
shapes run on ``tests/test_sync_removed.py``'s fixtures, the missing playlist
answering as the real adapter does, recorded rather than called. D1 applies.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests
from tidalapi.exceptions import ObjectNotFound

from cratekit.acquire import match
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue, tidal_catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import playlists, removed, removed_cli, unavailable
from tests._sync_builders import exited, failed
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist
from tests.test_label_tidal_catalogue import PLAYLIST, FakeClient
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_sync_removed import (
    DEEP,
    SUNSET,
    VERB,
    Account,
    Listed,
    _by_title,
    _five,
    _run,
    sunset,
    track,
)
from tests.test_sync_removed import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_removed import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_sync_removed import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_sync_removed import five_landed as five_landed  # noqa: PLC0414
from tests.test_sync_removed import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_sync_removed import land as land  # noqa: PLC0414
from tests.test_sync_removed import library as library  # noqa: PLC0414
from tests.test_sync_removed import machine as machine  # noqa: PLC0414
from tests.test_sync_removed import native_library as native_library  # noqa: PLC0414
from tests.test_sync_removed import offline as offline  # noqa: PLC0414
from tests.test_sync_removed import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_sync_removed import silence as silence  # noqa: PLC0414

#: A synced playlist the account no longer lists and nothing records: a pair.
PAIRED = "acc-paired"
FIRST = datetime(2026, 11, 21, 15, 30, tzinfo=timezone.utc)
SAME_DAY = FIRST + timedelta(hours=3)
NEXT_DAY = FIRST + timedelta(hours=25)
#: Eight hours past the first: a later calendar day, not yet a day apart.
NEXT_DATE = FIRST + timedelta(hours=9)
#: Sunset Warmup as the account lists it with New1 taken off.
NEW1_OFF = ("Held1", "New2", "Held2", "Held3")


class Clock:
    """The moment ``unavailable.now`` answers, moved by the test."""

    def __init__(self, monkeypatch, moment: datetime = FIRST) -> None:
        self.moment = moment
        monkeypatch.setattr(unavailable, "now", lambda: self.moment)


def recorded_failure(reference: str, status: int) -> tidal_catalogue.PlaylistUnresolvable:
    """The adapter's ``PlaylistUnresolvable`` for a request answering ``status``, recorded."""
    response = requests.Response()
    response.status_code = status
    http = requests.HTTPError(f"{status} for url: /v1/playlists/{reference}", response=response)
    inner: BaseException = http
    if status == 404:
        inner = ObjectNotFound(f"Playlist with id {reference} not found")
        inner.__cause__ = http
    outer = tidal_catalogue.PlaylistUnresolvable(
        f"the provider could not resolve the playlist {reference!r} ({inner})"
    )
    outer.__cause__ = inner
    return outer


def answering(account: Account, status: int, *references: str) -> None:
    """Each of ``references`` answers ``status`` when opened by its id."""
    original = account.fake.playlist_for
    named = set(references)

    def playlist_for(reference: str):
        if reference in named:
            account.fake.playlists_asked_for.append(reference)
            raise recorded_failure(reference, status)
        return original(reference)

    account.fake.playlist_for = playlist_for


def withholding(account: Account, withheld: int, *, served: int = 340) -> None:
    """``served`` hearts, the test's first, ``withheld`` more declared (R-504), A179's default."""
    filler = served - len(account.fake.hearts)
    account.fake.hearts.extend(
        track(f"Filler {number}", track_id=f"tid-filler-{number}") for number in range(filler)
    )

    def short():
        account.fake.heart_listings += 1
        served = tuple(account.fake.hearts)
        raise catalogue.HeartsShortfall(served, len(served) + withheld)

    account.fake.favourite_tracks = short


def _pair(cfg: config.Config) -> None:
    from cratekit.modules.outbound import pairs

    pairs.PairStore(config.load()).mark(PAIRED, "901", name="A Pair")


def _record() -> dict[str, unavailable.Sighting]:
    return unavailable.UnavailableRecord(config.load()).read()


def _playlists(out: dict) -> dict[str, dict]:
    return {item["account"]: item for item in out["data"]["items"] if item["action"] == "playlist"}


def _codes(out: dict) -> list[str]:
    return [one["code"] for one in out["warnings"]]


def _a_day_apart(clock: Clock) -> tuple[dict, dict]:
    """Two runs, the second a day and an hour after the first."""
    first = _run()
    clock.moment = NEXT_DAY
    return first, _run()


def _a179(cfg, silence, monkeypatch) -> Account:
    """New1 taken off Sunset Warmup; a pair nothing records answers not found; nine hearts withheld."""
    _five(cfg, silence)
    _pair(cfg)
    account = sunset(monkeypatch, *NEW1_OFF)
    answering(account, 404, PAIRED)
    withholding(account, 9)
    return account


@pytest.fixture
def a179(native_library, silence, monkeypatch, offline) -> config.Config:
    """The configuration once :func:`_a179` ran, with no network."""
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
    return cfg


# A179's shape, the defect


def test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart(
    a179, monkeypatch
):
    cfg = a179
    clock = Clock(monkeypatch)
    database = Path(cfg.library.db_path)
    before = hashlib.sha256(database.read_bytes()).hexdigest()

    first = _run()

    # One sighting: partial as before, the pair named with its first date and
    # the one command that retires it now.
    assert _by_title(first)["New1"]["why"] == removed.PARTIAL_READ
    assert first["data"]["totals"]["partial"] is True
    named = _playlists(first)
    assert named[PAIRED]["state"] == removed.UNREADABLE
    assert "first on 2026-11-21" in named[PAIRED]["why"]
    (seen,) = [one for one in first["warnings"] if one["code"] == removed_cli.UNAVAILABLE]
    assert PAIRED in seen["message"] and removed_cli.RETIRE_COMMAND in seen["message"]
    assert "seen unavailable on 2026-11-21" in seen["message"]
    # The hearts, short only by what the provider withholds, read whole and
    # named with both counts.
    assert named[removed.HEARTS]["state"] == removed.WITHHELD
    assert "349 declared, 340 listed, 9 withheld by the provider" in named[removed.HEARTS]["why"]
    assert removed_cli.HEARTS_WITHHELD in _codes(first)
    assert not _record()[PAIRED].is_retired

    clock.moment = SAME_DAY
    again = _run()

    assert _by_title(again)["New1"]["why"] == removed.PARTIAL_READ
    assert not _record()[PAIRED].is_retired

    clock.moment = NEXT_DAY
    offered = _run()

    answers = _by_title(offered)
    assert answers["New1"]["action"] == removed.OFFERED
    assert answers["New1"]["removed_from"] == [SUNSET]
    assert offered["data"]["totals"]["partial"] is False
    retired = _playlists(offered)[PAIRED]
    assert retired["state"] == removed.RETIRED
    assert "2026-11-21 and 2026-11-22" in retired["why"]
    assert offered["data"]["totals"]["playlists retired"] == 1
    assert removed_cli.RETIRED in _codes(offered)
    entry = _record()[PAIRED]
    assert entry.is_retired and entry.by == unavailable.BY_SIGHTINGS
    assert entry.first == unavailable.stamp(FIRST) and entry.last == unavailable.stamp(NEXT_DAY)
    # Retiring writes Cratekit's own record only.
    assert hashlib.sha256(database.read_bytes()).hexdigest() == before


def test_a_sighting_on_a_later_date_but_under_a_day_after_the_first_retires_nothing(
    a179, monkeypatch
):
    clock = Clock(monkeypatch, FIRST)
    _run()
    clock.moment = NEXT_DATE

    out = _run()

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert not _record()[PAIRED].is_retired


def failing_with(account: Account, error: BaseException, *references: str) -> None:
    """Each of ``references`` fails to open, the adapter's wrapper raised from ``error``."""
    original = account.fake.playlist_for
    named = set(references)

    def playlist_for(reference: str):
        if reference in named:
            outer = tidal_catalogue.PlaylistUnresolvable(f"could not resolve {reference!r}")
            outer.__cause__ = error
            raise outer
        return original(reference)

    account.fake.playlist_for = playlist_for


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(None, id="503"),
        # Round one's BLOCKING finding: the provider gate's lock raised FileNotFoundError.
        pytest.param(FileNotFoundError(2, "No such file or directory"), id="file-not-found"),
        pytest.param(ModuleNotFoundError("no module"), id="module-not-found"),
    ],
)
def test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired(
    five_landed, monkeypatch, error
):
    """A server error, or Python's own not found classes, are no sighting and never retire."""
    _pair(five_landed)
    account = sunset(monkeypatch, *NEW1_OFF)
    if error is None:
        answering(account, 503, PAIRED)
    else:
        failing_with(account, error, PAIRED)

    _first, out = _a_day_apart(Clock(monkeypatch))

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert _playlists(out)[PAIRED]["state"] == removed.UNREADABLE
    assert removed_cli.UNAVAILABLE not in _codes(out)
    assert _record() == {}
    assert not unavailable.answered_unavailable(error or recorded_failure(PAIRED, 503))


def test_two_runs_the_same_day_with_a_sighting_keep_one_digest(a179, monkeypatch):
    clock = Clock(monkeypatch)

    first = _run()
    clock.moment = SAME_DAY

    assert _run()["data"]["digest"] == first["data"]["digest"]


# The hearts


def test_hearts_short_only_by_what_the_provider_withholds_read_whole_and_still_keep_a_heart(
    five_landed, monkeypatch
):
    account = sunset(monkeypatch, "Held1")
    account.fake.hearts.append(track("New1"))
    withholding(account, 9)
    Clock(monkeypatch)

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [removed.HEARTS_NAME]
    assert answers["New2"]["action"] == removed.OFFERED
    assert out["data"]["totals"]["partial"] is False


def _hearts_of(fake: FakeCatalogue) -> removed.Listing:
    return removed.read_hearts(fake)


def _declaring(fake: FakeCatalogue, declared: int, served: tuple | None = None) -> FakeCatalogue:
    """``fake`` serving ``served``, or its hearts, as the shortfall of ``declared`` (R-504)."""

    def short():
        raise catalogue.HeartsShortfall(tuple(fake.hearts) if served is None else served, declared)

    fake.favourite_tracks = short
    return fake


@pytest.mark.parametrize(
    ("served", "declared"),
    [((), 5), ((track("One", track_id="tid-one"),), 1)],
    ids=["none-served", "nothing-withheld"],
)
def test_hearts_short_by_more_than_the_provider_withholds_stay_partial(served, declared):
    read = _hearts_of(_declaring(FakeCatalogue(), declared, served))

    assert read.state == removed.SHORT
    assert f"{declared} declared, {len(served)} listed" in read.why
    assert not read.holds(match.Wanted(artist="Probe", title="One", ref="tid-one"))


def _hearted(count: int, *first: Listed) -> FakeCatalogue:
    """An account hearting ``first`` and then ``count`` more."""
    hearts = [track(f"Heart {number}", track_id=f"tid-{number}") for number in range(count)]
    return FakeCatalogue(hearts=[*first, *hearts])


def _thirty(declared: int) -> FakeCatalogue:
    return _declaring(_hearted(29, track("One", track_id="tid-one")), declared)


def test_hearts_short_by_the_withheld_count_hold_every_heart_served():
    read = _hearts_of(_thirty(33))

    assert read.state == removed.WITHHELD
    assert "33 declared, 30 listed, 3 withheld by the provider" in read.why
    assert read.holds(match.Wanted(artist="Probe", title="One", ref="tid-one"))
    assert read.state not in removed.NOT_WHOLE


@pytest.mark.parametrize(
    ("declared", "state"),
    [(34, removed.SHORT), (33, removed.WITHHELD)],
    ids=["over-a-tenth", "a-tenth"],
)
def test_hearts_short_by_more_than_a_tenth_of_their_count_stay_partial(declared, state):
    """Round one: a window the provider dropped looks like a large shortfall."""
    read = _hearts_of(_thirty(declared))

    assert read.state == state
    assert f"{declared} declared, 30 listed" in read.why


def test_hearts_a_dropped_window_short_of_a_hearted_track_offer_nothing(five_landed, monkeypatch):
    """Round one's driven shape: 349 declared and 100 listed, the hearted New1 in the window lost."""
    withholding(sunset(monkeypatch, "Held1"), 249, served=100)
    Clock(monkeypatch)

    out = _run()

    assert out["data"]["totals"][removed.OFFERED] == 0
    assert _playlists(out)[removed.HEARTS]["state"] == removed.SHORT


# A retired playlist, read again


@pytest.fixture
def retired(native_library, silence, monkeypatch, offline) -> tuple[Account, Clock]:
    """A179's pair sighted twice a day apart, so retired, the clock a day on: (account, clock)."""
    cfg, _root = native_library
    account = _a179(cfg, silence, monkeypatch)
    clock = Clock(monkeypatch)
    _a_day_apart(clock)
    assert _record()[PAIRED].is_retired
    clock.moment = NEXT_DAY + timedelta(days=1)
    return account, clock


def _opens_again(account: Account, *tracks: Listed) -> None:
    """The retired pair's id opens again, serving ``tracks``."""
    account.fake.playlist_for = FakeCatalogue.playlist_for.__get__(account.fake)
    account.fake.playlists[PAIRED] = FakePagedPlaylist(list(tracks), declared=len(tracks))


def test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared(retired):
    account, _clock = retired
    _opens_again(account, track("New1"))

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == ["A Pair"]
    assert PAIRED not in _playlists(out)
    assert _record() == {}


def _unreadable_again(out: dict) -> None:
    """The run is partial again, the pair unreadable, and its retirement cleared."""
    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert _playlists(out)[PAIRED]["state"] == removed.UNREADABLE
    assert _record() == {}


def test_a_retired_playlist_the_account_lists_again_stops_every_offer_again(retired):
    account, _clock = retired
    account.fake.account.append(AccountPlaylist(playlist_id=PAIRED, name="A Pair", tracks=3))

    _unreadable_again(_run())


def test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other(
    land, monkeypatch
):
    cfg = land(also={"pl-b": (DEEP, ("New1", "New3"))})
    _pair(cfg)
    account = sunset(monkeypatch, "Held1", "Held2", "Held3")
    account.lists("pl-b", DEEP, [track("New1"), track("New3")])
    answering(account, 404, PAIRED)
    withholding(account, 9)

    _first, out = _a_day_apart(Clock(monkeypatch))

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]
    assert answers["New2"]["action"] == removed.OFFERED
    assert "New3" not in answers


def test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them(
    land, monkeypatch
):
    land(also={"pl-b": (DEEP, ("New1", "New3"))})
    answering(sunset(monkeypatch, *NEW1_OFF), 404, "pl-b")

    first, out = _a_day_apart(Clock(monkeypatch))

    first = _by_title(first)
    # One sighting: gone, still holding what its pass recorded (U287).
    assert first["New1"]["why"] == removed.ON_ANOTHER and first["New1"]["kept_by"] == [DEEP]
    # Retired: none of Deep Cuts' own tracks is a removal, and the account's
    # playlist keeps nothing. What keeps New1 now is the rekordbox twin the
    # landing made of Deep Cuts, a playlist of the person's, which is U287's
    # rule for a twin of a playlist the track did not leave.
    answers = _by_title(out)
    assert "New3" not in answers
    assert answers["New1"]["why"] == removed.IN_YOURS
    assert answers["New1"]["kept_by"] == [DEEP]
    assert _playlists(out)["pl-b"]["state"] == removed.RETIRED


# --retire, behind its explicit gate

RETIRE = [*VERB, "--retire"]


def _decide(run_id: str, answer: str) -> tuple[int, dict]:
    exited(drive(["run", "decide", run_id, removed_cli.RETIRE_GATE, answer, "--actor", "a-person"]))
    return drive(["--run", run_id, *RETIRE])


def _retire() -> dict:
    """``--retire`` asked, its gate answered retire, and the run carried out."""
    asked = exited(drive(RETIRE), ExitCode.DECISION_REQUIRED)
    return exited(_decide(asked["run_id"], "retire"))


def test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing(a179, monkeypatch):
    Clock(monkeypatch)
    state = config.state_path("sync_unavailable_record", config.load())

    asked = exited(drive(RETIRE), ExitCode.DECISION_REQUIRED)

    detail = asked["cause"]["detail"]
    assert detail["gate"] == removed_cli.RETIRE_GATE and detail["explicit"] is True
    assert not state.exists()
    aborted = exited(_decide(asked["run_id"], "abort"))
    assert aborted["outcome"] == "no_op"
    assert [item["account"] for item in aborted["data"]["items"]] == [PAIRED]
    assert aborted["data"]["items"][0]["seen unavailable"] == "2026-11-21"
    assert not state.exists()


def test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it(
    a179, monkeypatch
):
    Clock(monkeypatch)

    done = _retire()

    assert removed_cli.RETIRED_NOW in _codes(done)
    entry = _record()[PAIRED]
    assert entry.is_retired and entry.by == unavailable.BY_PERSON
    out = _run()
    assert _by_title(out)["New1"]["action"] == removed.OFFERED
    assert "by a person" in _playlists(out)[PAIRED]["why"]


def test_retire_offers_no_playlist_whose_id_failed_any_other_way(five_landed, monkeypatch):
    _pair(five_landed)
    answering(sunset(monkeypatch, "Held1"), 503, PAIRED)
    Clock(monkeypatch)

    out = exited(drive(RETIRE))

    assert out["outcome"] == "no_op"
    assert out["data"]["items"] == []
    assert _record() == {}


def _record_path() -> Path:
    path = config.state_path("sync_unavailable_record", config.load())
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def test_an_unreadable_record_refuses_before_the_account_is_asked(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    account = _a179(cfg, silence, monkeypatch)
    _record_path().write_text("not json", encoding="utf-8")

    out = failed(drive(VERB))

    assert out["cause"]["reason"] == "sync-unavailable-record-unusable", out
    assert account.fake.account_listings == 0


def test_the_verb_declares_the_retire_gate_explicit_on_the_plan():
    from cratekit.cli import registry

    entry = registry.entry("sync.removed")
    (retire,) = [spec for spec in entry.gates if spec.name == removed_cli.RETIRE_GATE]
    assert retire.options == ("retire", "abort")
    assert retire.explicit and retire.digest_source == "plan"


# The rules, held one at a time


def test_a_sighting_retires_only_a_day_after_the_first_and_a_retirement_stands():
    once = unavailable.sighted(None, "pl", "P", FIRST)
    assert not once.is_retired and once.first == once.last == unavailable.stamp(FIRST)
    same = unavailable.sighted(once, "pl", "P", SAME_DAY)
    assert not same.is_retired and same.last == unavailable.stamp(SAME_DAY)
    just_short = unavailable.sighted(once, "pl", "P", FIRST + timedelta(hours=23, minutes=59))
    assert not just_short.is_retired
    day = unavailable.sighted(once, "pl", "P", FIRST + unavailable.APART)
    assert day.is_retired and day.by == unavailable.BY_SIGHTINGS
    assert day.retired == unavailable.stamp(FIRST + unavailable.APART)
    assert unavailable.sighted(day, "pl", "P", NEXT_DAY + timedelta(days=5)) == day
    person = unavailable.retired_by_person(once, SAME_DAY)
    assert person.is_retired and person.by == unavailable.BY_PERSON
    assert unavailable.retired_by_person(day, SAME_DAY) == day


def _raised(make):
    try:
        make()
    except BaseException as exc:  # noqa: BLE001
        return exc
    raise AssertionError("nothing raised")


def _status(code: int) -> requests.Response:
    response = requests.Response()
    response.status_code = code
    return response


def test_only_a_not_found_answer_is_read_as_unavailable():
    assert unavailable.answered_unavailable(recorded_failure("pl", 404))
    assert not unavailable.answered_unavailable(recorded_failure("pl", 503))
    assert not unavailable.answered_unavailable(recorded_failure("pl", 429))
    # The digits of an id are never read as a status.
    assert not unavailable.answered_unavailable(RuntimeError("no playlist 24040417 (404)"))
    # The client's class, with no status attached anywhere.
    bare = tidal_catalogue.PlaylistUnresolvable("gone")
    bare.__cause__ = ObjectNotFound("Playlist with id pl not found")
    assert unavailable.answered_unavailable(bare)

    # A server error met while handling a not found is the server error.
    def met_while_handling():
        try:
            raise ObjectNotFound("Playlist with id pl not found")
        except ObjectNotFound:
            raise requests.HTTPError("503", response=_status(503))  # noqa: B904

    assert not unavailable.answered_unavailable(_raised(met_while_handling))


def test_the_real_adapter_reads_a_404_as_unavailable_and_a_server_error_not():
    def adapter(error: BaseException):
        class Answers(FakeClient):
            def playlist(self, playlist_id):
                raise error

        return tidal_catalogue.TidalCatalogue(Answers())

    missing = ObjectNotFound("Playlist with id x not found")
    missing.__cause__ = requests.HTTPError("404", response=_status(404))
    with pytest.raises(CratekitError) as gone:
        intake_cli.list_playlist_readable(adapter(missing), PLAYLIST)
    assert gone.value.cause.reason in playlists.PER_PLAYLIST_REASONS
    assert unavailable.answered_unavailable(gone.value)

    with pytest.raises(CratekitError) as down:
        intake_cli.list_playlist_readable(
            adapter(requests.HTTPError("500", response=_status(500))), PLAYLIST
        )
    assert down.value.cause.reason in playlists.PER_PLAYLIST_REASONS
    assert not unavailable.answered_unavailable(down.value)


def _write_record(cfg: config.Config, raw: object) -> unavailable.UnavailableRecord:
    record = unavailable.UnavailableRecord(cfg)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text(json.dumps(raw), encoding="utf-8")
    return record


_WHEN = "2026-11-21T00:00:00+00:00"


def _entry(**changed) -> dict:
    """One sighting as the record writes it, ``changed`` set over a first and last of _WHEN."""
    held = {"playlist_id": "pl", "name": "P", "first": _WHEN, "last": _WHEN}
    return {**held, "retired": "", "by": "", **changed}


def _refuses(record: unavailable.UnavailableRecord) -> None:
    with pytest.raises(CratekitError) as refused:
        record.read()
    assert refused.value.cause.reason == "sync-unavailable-record-unusable"


@pytest.mark.parametrize(
    "damage",
    [
        {"version": 2},
        {"library_id": "another"},
        {"playlists": "none"},
        {"playlists": [_entry(first="", last="")]},
        {"playlists": [_entry(first="2026-11-21")]},
        {"playlists": [_entry(retired="2026-11-22T00:00:00+00:00")]},
        {"playlists": [_entry(), _entry()]},
        {"playlists": [_entry(retired=_WHEN, by="hand")]},
    ],
    ids=["version", "library", "no-list", "no-sighting", "naive-time", "retired-by-nobody", "twice",
         "unknown-hand"],
)
def test_a_damaged_record_refuses_and_is_never_read_as_empty(native_library, damage):
    """A record naming a playlist twice or an unknown hand refuses as well."""
    cfg, _root = native_library
    raw = {"version": 1, "library_id": cfg.library.volume_id, "playlists": [], **damage}

    _refuses(_write_record(cfg, raw))


def test_the_record_reads_back_what_it_wrote_and_drops_an_entry_given_none(native_library):
    cfg, _root = native_library
    record = unavailable.UnavailableRecord(cfg)
    entry = unavailable.sighted(None, "pl", "P", FIRST)

    assert record.update({"pl": entry, "other": None}) == {"pl": entry}
    assert record.read() == {"pl": entry}
    assert record.update({"pl": None}) == {}
    assert record.read() == {}


def test_a_sighting_keeps_the_latest_instant_and_a_clock_set_back_moves_nothing():
    with_fraction = FIRST + timedelta(hours=1, microseconds=500)
    once = unavailable.sighted(None, "pl", "P", with_fraction)
    later = with_fraction + timedelta(microseconds=999_500)
    assert unavailable.sighted(once, "pl", "P", later).last == unavailable.stamp(later)
    # An earlier moment, a clock set back, moves nothing.
    assert unavailable.sighted(once, "pl", "P", FIRST).last == once.last


# Round one


def test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared(retired):
    """Round one: it opened, serving New1 beside a row with no identifier."""
    account, _clock = retired
    _opens_again(account, track("New1"), Listed("", "Nameless"))

    _unreadable_again(_run())


def test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired(
    retired
):
    account, clock = retired
    answering(account, 503, PAIRED)

    out = _run()

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    named = _playlists(out)[PAIRED]
    assert named["state"] == removed.UNREADABLE
    assert "retired on 2026-11-22" in named["why"]
    assert _record()[PAIRED].is_retired
    # Not found again: retired, and offering again, its dates unmoved.
    answering(account, 404, PAIRED)
    clock.moment = NEXT_DAY + timedelta(days=2)
    again = _run()
    assert _by_title(again)["New1"]["action"] == removed.OFFERED
    assert "2026-11-21 and 2026-11-22" in _playlists(again)[PAIRED]["why"]


def test_a_gone_downloaded_playlist_is_named_by_what_cratekit_calls_it(land, monkeypatch):
    land(also={"pl-b": (DEEP, ("New1", "New3"))})
    answering(sunset(monkeypatch, *NEW1_OFF), 404, "pl-b")
    Clock(monkeypatch)

    out = _run()

    assert _playlists(out)["pl-b"]["name"] == DEEP
    assert _record()["pl-b"].name == DEEP
    (seen,) = [one for one in out["warnings"] if one["code"] == removed_cli.UNAVAILABLE]
    assert f"pl-b ({DEEP})" in seen["message"]


def _said_partial(out: dict) -> str:
    (said,) = [one for one in out["warnings"] if one["code"] == removed_cli.PARTIAL]
    return said["message"]


def test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    account = _a179(cfg, silence, monkeypatch)
    Clock(monkeypatch)
    _run()
    assert PAIRED in _record()
    answering(account, 503, PAIRED)

    out = exited(drive(RETIRE))

    assert out["outcome"] == "no_op" and out["data"]["items"] == []
    assert "A Pair" in _said_partial(out)
    assert not _record()[PAIRED].is_retired


def test_retire_writes_every_reads_answer_with_the_retirement(land, monkeypatch):
    """A playlist seen before that opens on the retire's read is dropped as the plain run drops it."""
    cfg = land(also={"pl-b": (DEEP, ("New3",))})
    _pair(cfg)
    account = sunset(monkeypatch, "Held1")
    answering(account, 404, PAIRED, "pl-b")
    clock = Clock(monkeypatch)
    _run()
    assert set(_record()) == {PAIRED, "pl-b"}
    account.fake.playlist_for = FakeCatalogue.playlist_for.__get__(account.fake)
    account.fake.playlists["pl-b"] = FakePagedPlaylist([track("New3")], declared=1)
    answering(account, 404, PAIRED)
    clock.moment = SAME_DAY

    _retire()

    assert set(_record()) == {PAIRED}
    assert _record()[PAIRED].by == unavailable.BY_PERSON


def test_the_retire_gate_binds_across_midnight(a179, monkeypatch):
    """Round one: two drives either side of UTC midnight, nothing recorded before."""
    clock = Clock(monkeypatch, datetime(2026, 11, 21, 23, 55, tzinfo=timezone.utc))

    asked = exited(drive(RETIRE), ExitCode.DECISION_REQUIRED)
    clock.moment = datetime(2026, 11, 22, 0, 5, tzinfo=timezone.utc)
    exited(_decide(asked["run_id"], "retire"))

    assert _record()[PAIRED].by == unavailable.BY_PERSON


def test_a_not_found_met_only_while_handling_another_failure_is_not_one():
    def reset_while_handling():
        try:
            raise ObjectNotFound("Playlist with id pl not found")
        except ObjectNotFound:
            raise ConnectionResetError("reset by peer")  # noqa: B904

    assert not unavailable.answered_unavailable(_raised(reset_while_handling))

    def status_while_handling_a_404():
        try:
            raise requests.HTTPError("404", response=_status(404))
        except requests.HTTPError:
            raise requests.HTTPError("503", response=_status(503))  # noqa: B904

    assert not unavailable.answered_unavailable(_raised(status_while_handling_a_404))


def test_a_record_that_cannot_be_opened_refuses(native_library):
    cfg, _root = native_library
    record = unavailable.UnavailableRecord(cfg)
    record.path.mkdir(parents=True)

    _refuses(record)


# Round two


@pytest.mark.parametrize(
    ("served", "declared", "state"),
    [(920, 1020, removed.SHORT), (951, 1000, removed.WITHHELD), (950, 1000, removed.SHORT)],
    ids=["a-dropped-window", "forty-nine", "fifty"],
)
def test_hearts_short_by_half_a_page_or_more_stay_partial_on_any_account(served, declared, state):
    """Round two: 1,020 declared and a window of a hundred lost was within a tenth."""
    assert _hearts_of(_declaring(_hearted(served), declared)).state == state


def test_a_run_with_no_removal_never_reads_the_pair_store(five_landed, monkeypatch):
    """Round two: the store read moved ahead of the removal, so a damaged one refused a quiet run."""
    from cratekit.modules.outbound import pairs

    sunset(monkeypatch, "Held1", "New1", "New2", "Held2", "Held3")

    def refused(_self):
        raise AssertionError("the pair store was read")

    monkeypatch.setattr(pairs.PairStore, "all", refused)

    out = exited(drive(VERB))

    assert out["outcome"] == "no_op"


def test_retire_names_a_gone_playlist_whose_id_now_fails_another_way(land, monkeypatch):
    """Round two: a recorded gone playlist reads GONE, not short, and was silent."""
    land(also={"pl-b": (DEEP, ("New3",))})
    account = sunset(monkeypatch, "Held1")
    answering(account, 404, "pl-b")
    Clock(monkeypatch)
    _run()
    answering(account, 503, "pl-b")

    out = exited(drive(RETIRE))

    assert out["data"]["items"] == []
    assert DEEP in _said_partial(out)


def test_a_retired_listing_holds_nothing_whatever_it_carries():
    """The mutation table's M5: the state alone keeps a retired playlist from holding."""
    wanted = match.Wanted(artist="Probe", title="Song", isrc="usprb2600001", ref="tid-1")
    carried = removed.Listing(
        account="pl",
        name="P",
        state=removed.RETIRED,
        refs=frozenset({"tid-1"}),
        isrcs=frozenset({"USPRB2600001"}),
        recordings=frozenset({removed.recording(wanted)}),
    )
    assert not carried.holds(wanted)
    assert removed.RETIRED not in removed.NOT_WHOLE
