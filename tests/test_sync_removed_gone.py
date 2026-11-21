"""U320: ``crate sync removed`` offers a removal again past short hearts and a playlist gone for good.

A179's live run at sitting 101 offered nothing, because the plan was partial
on every run: thirteen synced playlists the account no longer lists, whose ids
did not open and whose contents no readable job recorded, and the hearts, 349
declared and 340 listed, the provider withholding nine. Both shapes are driven
here on the native landing fixtures ``tests/test_sync_removed.py`` drives, the
account a fake catalogue whose missing playlist answers as the real adapter
does: ``PlaylistUnresolvable`` raised from the client's ``ObjectNotFound``,
itself raised from the 404 the request answered, recorded rather than called.

D1 applies. Nothing here names a real volume, a real person or a real track.
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
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist
from tests.test_label_tidal_catalogue import PLAYLIST, FakeClient
from tests.test_sync_removed import (
    DEEP,
    SUNSET,
    VERB,
    Account,
    _by_title,
    _five,
    _run,
    track,
)
from tests.test_sync_removed import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_removed import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_sync_removed import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_sync_removed import fresh_cache as fresh_cache  # noqa: PLC0414
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


class Clock:
    """The moment ``unavailable.now`` answers, moved by the test."""

    def __init__(self, monkeypatch, moment: datetime = FIRST) -> None:
        self.moment = moment
        monkeypatch.setattr(unavailable, "now", lambda: self.moment)


def recorded_failure(reference: str, status: int) -> tidal_catalogue.PlaylistUnresolvable:
    """The failure the real adapter raises for a playlist whose request answered ``status``.

    The client raises ``ObjectNotFound`` from the 404's ``HTTPError``, and any
    other status as that ``HTTPError``; the adapter wraps either as
    ``PlaylistUnresolvable`` raised from it. Recorded, not called.
    """
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


def withholding(account: Account, withheld: int) -> None:
    """The hearts served as they stand, the account declaring ``withheld`` more (R-504)."""

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


def _a179(cfg, silence, monkeypatch) -> Account:
    """New1 taken off Sunset Warmup; a pair nothing records answers not found; nine hearts withheld."""
    _five(cfg, silence)
    _pair(cfg)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2"), track("Held2"), track("Held3")])
    answering(account, 404, PAIRED)
    withholding(account, 9)
    return account


# ---------------------------------------------------------------------------
# A179's shape, the defect
# ---------------------------------------------------------------------------


def test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
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
    assert "10 declared, 1 listed, 9 withheld by the provider" in named[removed.HEARTS]["why"]
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
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
    clock = Clock(monkeypatch, FIRST)
    _run()
    clock.moment = NEXT_DATE

    out = _run()

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert not _record()[PAIRED].is_retired


def test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    _pair(cfg)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2"), track("Held2"), track("Held3")])
    answering(account, 503, PAIRED)
    clock = Clock(monkeypatch)

    _run()
    clock.moment = NEXT_DAY
    out = _run()

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert _playlists(out)[PAIRED]["state"] == removed.UNREADABLE
    assert removed_cli.UNAVAILABLE not in _codes(out)
    assert _record() == {}


def test_two_runs_the_same_day_with_a_sighting_keep_one_digest(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
    clock = Clock(monkeypatch)

    first = _run()
    clock.moment = SAME_DAY

    assert _run()["data"]["digest"] == first["data"]["digest"]


# ---------------------------------------------------------------------------
# The hearts
# ---------------------------------------------------------------------------


def test_hearts_short_only_by_what_the_provider_withholds_read_whole_and_still_keep_a_heart(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])
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


@pytest.mark.parametrize(
    ("served", "declared"),
    [((), 5), ((track("One", track_id="tid-one"),), 1)],
    ids=["none-served", "nothing-withheld"],
)
def test_hearts_short_by_more_than_the_provider_withholds_stay_partial(served, declared):
    fake = FakeCatalogue()

    def short():
        raise catalogue.HeartsShortfall(served, declared)

    fake.favourite_tracks = short

    read = _hearts_of(fake)

    assert read.state == removed.SHORT
    assert f"{declared} declared, {len(served)} listed" in read.why
    assert not read.holds(match.Wanted(artist="Probe", title="One", ref="tid-one"))


def test_hearts_short_by_the_withheld_count_hold_every_heart_served():
    fake = FakeCatalogue(hearts=[track("One", track_id="tid-one")])

    def short():
        raise catalogue.HeartsShortfall(tuple(fake.hearts), 4)

    fake.favourite_tracks = short

    read = _hearts_of(fake)

    assert read.state == removed.WITHHELD
    assert "4 declared, 1 listed, 3 withheld by the provider" in read.why
    assert read.holds(match.Wanted(artist="Probe", title="One", ref="tid-one"))
    assert read.state not in removed.NOT_WHOLE


# ---------------------------------------------------------------------------
# A retired playlist, read again
# ---------------------------------------------------------------------------


def _retired_pair(cfg, silence, monkeypatch) -> tuple[Account, Clock]:
    account = _a179(cfg, silence, monkeypatch)
    clock = Clock(monkeypatch)
    _run()
    clock.moment = NEXT_DAY
    _run()
    assert _record()[PAIRED].is_retired
    return account, clock


def test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    account, clock = _retired_pair(cfg, silence, monkeypatch)
    account.fake.playlist_for = FakeCatalogue.playlist_for.__get__(account.fake)
    account.fake.playlists[PAIRED] = FakePagedPlaylist([track("New1")], declared=1)
    clock.moment = NEXT_DAY + timedelta(days=1)

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [PAIRED]
    assert PAIRED not in _playlists(out)
    assert _record() == {}


def test_a_retired_playlist_the_account_lists_again_stops_every_offer_again(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    account, clock = _retired_pair(cfg, silence, monkeypatch)
    account.fake.account.append(AccountPlaylist(playlist_id=PAIRED, name="A Pair", tracks=3))
    clock.moment = NEXT_DAY + timedelta(days=1)

    out = _run()

    assert _by_title(out)["New1"]["why"] == removed.PARTIAL_READ
    assert _playlists(out)[PAIRED]["state"] == removed.UNREADABLE
    assert _record() == {}


def test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New1", "New3"))})
    _pair(cfg)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("Held2"), track("Held3")])
    account.lists("pl-b", DEEP, [track("New1"), track("New3")])
    answering(account, 404, PAIRED)
    withholding(account, 9)
    clock = Clock(monkeypatch)
    _run()
    clock.moment = NEXT_DAY

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]
    assert answers["New2"]["action"] == removed.OFFERED
    assert "New3" not in answers


def test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New1", "New3"))})
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2"), track("Held2"), track("Held3")])
    answering(account, 404, "pl-b")
    clock = Clock(monkeypatch)

    first = _by_title(_run())
    clock.moment = NEXT_DAY
    out = _run()

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


# ---------------------------------------------------------------------------
# --retire, behind its explicit gate
# ---------------------------------------------------------------------------

RETIRE = [*VERB, "--retire"]


def _decide(run_id: str, answer: str) -> tuple[int, dict]:
    decided, envelope = drive(
        ["run", "decide", run_id, removed_cli.RETIRE_GATE, answer, "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    return drive(["--run", run_id, *RETIRE])


def test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
    Clock(monkeypatch)
    state = config.state_path("sync_unavailable_record", config.load())

    code, asked = drive(RETIRE)

    assert code == int(ExitCode.DECISION_REQUIRED), asked
    detail = asked["cause"]["detail"]
    assert detail["gate"] == removed_cli.RETIRE_GATE and detail["explicit"] is True
    assert not state.exists()
    code, aborted = _decide(asked["run_id"], "abort")
    assert code == int(ExitCode.OK), aborted
    assert aborted["outcome"] == "no_op"
    assert [item["account"] for item in aborted["data"]["items"]] == [PAIRED]
    assert aborted["data"]["items"][0]["seen unavailable"] == "2026-11-21"
    assert not state.exists()


def test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _a179(cfg, silence, monkeypatch)
    Clock(monkeypatch)

    code, asked = drive(RETIRE)
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    code, done = _decide(asked["run_id"], "retire")

    assert code == int(ExitCode.OK), done
    assert removed_cli.RETIRED_NOW in _codes(done)
    entry = _record()[PAIRED]
    assert entry.is_retired and entry.by == unavailable.BY_PERSON
    out = _run()
    assert _by_title(out)["New1"]["action"] == removed.OFFERED
    assert "by a person" in _playlists(out)[PAIRED]["why"]


def test_retire_offers_no_playlist_whose_id_failed_any_other_way(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    _pair(cfg)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])
    answering(account, 503, PAIRED)
    Clock(monkeypatch)

    code, out = drive(RETIRE)

    assert code == int(ExitCode.OK), out
    assert out["outcome"] == "no_op"
    assert out["data"]["items"] == []
    assert _record() == {}


def test_an_unreadable_record_refuses_before_the_account_is_asked(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    account = _a179(cfg, silence, monkeypatch)
    path = config.state_path("sync_unavailable_record", config.load())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")

    code, out = drive(VERB)

    assert code != int(ExitCode.OK)
    assert out["cause"]["reason"] == "sync-unavailable-record-unusable", out
    assert account.fake.account_listings == 0


def test_the_verb_declares_the_retire_gate_explicit_on_the_plan():
    from cratekit.cli import registry

    entry = registry.entry("sync.removed")
    (retire,) = [spec for spec in entry.gates if spec.name == removed_cli.RETIRE_GATE]
    assert retire.options == ("retire", "abort")
    assert retire.explicit and retire.digest_source == "plan"


# ---------------------------------------------------------------------------
# The rules, held one at a time
# ---------------------------------------------------------------------------


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
            failing = requests.Response()
            failing.status_code = 503
            raise requests.HTTPError("503", response=failing)  # noqa: B904

    assert not unavailable.answered_unavailable(_raised(met_while_handling))


def test_the_real_adapter_reads_a_404_as_unavailable_and_a_server_error_not():
    def adapter(error: BaseException):
        class Answers(FakeClient):
            def playlist(self, playlist_id):
                raise error

        return tidal_catalogue.TidalCatalogue(Answers())

    response = requests.Response()
    response.status_code = 404
    missing = ObjectNotFound("Playlist with id x not found")
    missing.__cause__ = requests.HTTPError("404", response=response)
    with pytest.raises(CratekitError) as gone:
        intake_cli.list_playlist_readable(adapter(missing), PLAYLIST)
    assert gone.value.cause.reason in playlists.PER_PLAYLIST_REASONS
    assert unavailable.answered_unavailable(gone.value)

    failing = requests.Response()
    failing.status_code = 500
    with pytest.raises(CratekitError) as down:
        intake_cli.list_playlist_readable(
            adapter(requests.HTTPError("500", response=failing)), PLAYLIST
        )
    assert down.value.cause.reason in playlists.PER_PLAYLIST_REASONS
    assert not unavailable.answered_unavailable(down.value)


def _write_record(cfg: config.Config, raw: object) -> unavailable.UnavailableRecord:
    record = unavailable.UnavailableRecord(cfg)
    record.path.parent.mkdir(parents=True, exist_ok=True)
    record.path.write_text(json.dumps(raw), encoding="utf-8")
    return record


@pytest.mark.parametrize(
    "damage",
    [
        {"version": 2},
        {"library_id": "another"},
        {"playlists": "none"},
        {"playlists": [{"playlist_id": "pl", "name": "P", "first": "", "last": "", "retired": "", "by": ""}]},
        {"playlists": [{"playlist_id": "pl", "name": "P", "first": "2026-11-21", "last": "2026-11-21T00:00:00+00:00", "retired": "", "by": ""}]},
        {"playlists": [{"playlist_id": "pl", "name": "P", "first": "2026-11-21T00:00:00+00:00", "last": "2026-11-21T00:00:00+00:00", "retired": "2026-11-22T00:00:00+00:00", "by": ""}]},
    ],
    ids=["version", "library", "no-list", "no-sighting", "naive-time", "retired-by-nobody"],
)
def test_a_damaged_record_refuses_and_is_never_read_as_empty(native_library, damage):
    cfg, _root = native_library
    raw = {"version": 1, "library_id": cfg.library.volume_id, "playlists": [], **damage}
    record = _write_record(cfg, raw)

    with pytest.raises(CratekitError) as refused:
        record.read()

    assert refused.value.cause.reason == "sync-unavailable-record-unusable"


def test_the_record_reads_back_what_it_wrote_and_drops_an_entry_given_none(native_library):
    cfg, _root = native_library
    record = unavailable.UnavailableRecord(cfg)
    entry = unavailable.sighted(None, "pl", "P", FIRST)

    assert record.update({"pl": entry, "other": None}) == {"pl": entry}
    assert record.read() == {"pl": entry}
    assert record.update({"pl": None}) == {}
    assert record.read() == {}

