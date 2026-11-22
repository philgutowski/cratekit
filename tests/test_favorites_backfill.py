"""U120, U146: ``crate favorites backfill`` places every owned heart All Favorites lacks.

Driven through the real dispatcher on the native landing suite's library: a
hearts job queued by hand and run, its tracks put in the library with nothing
placing them, then the verb plans, asks, places and reads back.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit.core import jobs, rb_writer, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import backfill, backfill_cli, placement
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from tests.cli_drive import drive
from tests.intake.test_workers import Track, bind_hearts
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_intake_land_hearts_native import (
    PINK_ID,
    RED_ID,
    SOURCE,
    UNKNOWN,
    _colour_of,
    _favorites,
    _home,
    hearts_swept,
)
from tests.test_intake_land_hearts_native import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_intake_land_native import _members, _query, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

VERB = ["favorites", "backfill"]
GATE = backfill_cli.APPROVE_GATE
BATCH = "2026-09-29-favorites"
UTC = timezone.utc
SEP = datetime(2026, 9, 29, 22, 0, tzinfo=UTC)
NOV = datetime(2026, 11, 3, 12, 0, tzinfo=UTC)
NOV_ISO = "2026-11-03T12:00:00+00:00"


@contextmanager
def _db(cfg):
    """A write handle on the test library, committed and closed."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        yield handle
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


def _stage(cfg, silence: Path, title: str) -> Path:
    """A file tagged the way the hearts job's rows read, so the match rule ties them."""
    path = Path(cfg.paths.download_staging) / f"{title}.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def _land(batch: str = BATCH) -> None:
    code, acted, _refused = _two_acts(["intake", "land", "--name", batch])
    assert code == int(ExitCode.OK), acted


def _seed(cfg, silence: Path, *titles: str, batch: str = BATCH) -> None:
    """Each track in the batch's folder with its row, as a landing with no pass leaves it."""
    folder = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / batch
    folder.mkdir(parents=True, exist_ok=True)
    with _db(cfg) as handle:
        artist = handle.get_artist(Name="Probe").one_or_none() or handle.add_artist("Probe")
        for title in titles:
            path = folder / f"{title}.flac"
            shutil.copyfile(silence, path)
            assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
            handle.add_content(path, Title=title, ArtistID=artist.ID)


def _landed_hearts(cfg, silence, titles: dict[str, str | None], *, batch: str = BATCH, land=False):
    """A hearts job run by hand, then its tracks in the library with nothing placing them.

    ``None`` is a row an older build froze with no date key at all. The rows are
    seeded as the landing leaves them, unless ``land`` asks for the landing itself.
    """
    job = hearts_swept(
        cfg, {title: (UNKNOWN if when is None else when) for title, when in titles.items()}, run_id=""
    )
    if land:
        for title in titles:
            _stage(cfg, silence, title)
        _land(batch)
    else:
        _seed(cfg, silence, *titles, batch=batch)
    return job


def _account(monkeypatch, dates: dict[str, datetime | None], *, declared: int | None | str = "whole"):
    """The account's hearts under the identifiers the jobs froze, WHOLE unless ``declared`` says not.

    ``None`` is a provider that published no count.
    """
    rows = []
    for title, when in dates.items():
        row = Track(f"tid-{title}", "Probe", title)
        if when is not None:
            row.user_date_added = when
        rows.append(row)
    fake = bind_hearts(monkeypatch, rows)
    fake.hearts_declared = len(rows) if declared == "whole" else declared
    return fake


@pytest.fixture
def home(native_library):
    """The native library with an empty All Favorites in its Favorites folder: cfg, folder, source."""
    cfg, _root_id = native_library
    return (cfg, *_home(cfg))


def _acts(verb: list[str] = VERB) -> tuple[int, dict, dict]:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _approved(verb: list[str] = VERB) -> tuple[dict, dict]:
    """The verb's two acts, approved, ending OK: the answer and the gate's refusal."""
    code, acted, refused = _acts(verb)
    assert code == int(ExitCode.OK), acted
    return acted, refused


def _note(acted: dict, code: str) -> str:
    (note,) = [w for w in acted["warnings"] if w["code"] == code]
    return note["message"]


def _live(cfg, playlist_id: str) -> list[str]:
    """The members a person sees: the removed rows left out, which ``_members`` keeps."""
    return [
        str(row[0])
        for row in _query(
            cfg,
            "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0 "
            "ORDER BY TrackNo",
            playlist_id,
        )
    ]


def _rows(cfg) -> dict[str, str]:
    return {str(title): str(row) for row, title in _query(cfg, "SELECT ID, Title FROM djmdContent")}


def _deep_row(cfg, silence: Path, title: str) -> str:
    """A track the library holds two folders deep, with its row, as the source system filed it."""
    deep = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025" / f"{title}.flac"
    deep.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, deep)
    assert tags.write_tags(deep, {"title": title, "artist": "Probe"})
    with _db(cfg) as handle:
        row = str(handle.add_content(deep, Title=title).ID)
    return row


def _take_out(cfg, playlist_id: str, row: str) -> None:
    """The membership of ``row`` taken out by hand: it stays, marked removed."""
    with _db(cfg) as handle:
        (entry,) = [
            one
            for one in handle.get_playlist_songs(PlaylistID=playlist_id)
            if str(one.ContentID) == row and not one.rb_local_deleted
        ]
        entry.rb_local_deleted = 1


def _put(cfg, playlist_id: str, row: str) -> None:
    with _db(cfg) as handle:
        handle.add_to_playlist(handle.get_playlist(ID=playlist_id), row)


def test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them(
    home, silence, monkeypatch
):
    cfg, folder_id, source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None, "Fractals": None, "Find My Way": None}, land=True)
    fake = _account(monkeypatch, {"Same Girl": SEP, "Fractals": SEP, "Find My Way": SEP, "Elsewhere": NOV})
    assert _favorites(cfg, folder_id) == {SOURCE: []}, "nothing placed them as they landed"

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert sorted(item["title"] for item in shown["items"]) == [
        "Probe - Find My Way",
        "Probe - Fractals",
        "Probe - Same Girl",
    ]
    assert {item["month"] for item in shown["items"]} == {"2026-09"}
    assert {item["dated_by"] for item in shown["items"]} == {"account"}
    assert shown["hearts to place"] == 3 and shown["memberships to add"] == 6
    assert shown["by month"] == ["2026-09: 3"]
    assert shown["month playlists to create"] == ["2026-09"]
    assert shown["dates asked of the account"] == 3 and shown["undated"] == 0
    assert shown["into"].startswith(f"{SOURCE!r} (row {source_id}) under 'Favorites'")
    # Once per plan, and the two acts are two plans.
    assert fake.heart_listings == 2
    assert _favorites(cfg, folder_id) == {
        SOURCE: ["Find My Way", "Fractals", "Same Girl"],
        "2026-09": ["Find My Way", "Fractals", "Same Girl"],
    } or sorted(_favorites(cfg, folder_id)[SOURCE]) == ["Find My Way", "Fractals", "Same Girl"]
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["added"], totals["created"]) == (3, 6, 1)
    note = _note(acted, backfill_cli.PLACED)
    assert "6 membership(s) placed: 3 into" in note
    assert "for 3 owned heart(s)" in note
    assert "2026-09 (made)" in note
    # Every item names the file by its path under the folder the landing filed it in (U164).
    filed = "Music/Processed_Tracks/2026/09_29_26 favorites/"
    assert all(item["path"].startswith(filed) for item in shown["items"])


def test_a_second_run_finds_the_same_hearts_and_writes_nothing(home, silence, monkeypatch):
    cfg, folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    _approved()

    acted, refused = _approved()

    assert acted["outcome"] == "no_op"
    assert "no owned heart needs placing, 1 already in" in _note(acted, backfill_cli.NOTHING_TO_PLACE)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["memberships to add"] == 0 and shown["month playlists to create"] == []
    assert shown["already placed"] == 1 and shown["items"] == []
    assert _favorites(cfg, folder_id) == {SOURCE: ["Same Girl"], "2026-09": ["Same Girl"]}
    assert len(_members(cfg, _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-09'")[0][0])) == 1


def test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not(
    home, silence, monkeypatch
):
    """A heart owned when its job ran, filed deep, is placed (U146); a file with no row is not."""
    cfg, folder_id, _source_id = home
    _deep_row(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": UNKNOWN, "Hand Filed": UNKNOWN, "Landed": UNKNOWN}, run_id="")
    hand = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "Hand Filed.flac"
    shutil.copyfile(silence, hand)
    assert tags.write_tags(hand, {"title": "Hand Filed", "artist": "Probe"})
    _seed(cfg, silence, "Landed")
    _account(monkeypatch, {"Owned": SEP, "Hand Filed": SEP, "Landed": NOV})

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert [item["title"] for item in shown["items"]] == ["Probe - Owned", "Probe - Landed"]
    assert shown["by month"] == ["2026-09: 1", "2026-11: 1"]
    placed = _favorites(cfg, folder_id)
    assert sorted(placed[SOURCE]) == ["Landed", "Owned"]
    assert (placed["2026-09"], placed["2026-11"]) == (["Owned"], ["Landed"])


def test_a_date_the_job_froze_wins_over_the_accounts(home, silence, monkeypatch):
    """The account is listed all the same, to learn it still carries the heart, and loses."""
    cfg, folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Dated": NOV_ISO})
    fake = _account(monkeypatch, {"Dated": SEP})

    _acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    (item,) = shown["items"]
    assert (item["month"], item["dated_by"]) == ("2026-11", "job")
    assert shown["dates asked of the account"] == 0
    assert fake.heart_listings == 2, "once per plan, and the two acts are two plans"
    assert _favorites(cfg, folder_id) == {SOURCE: ["Dated"], "2026-11": ["Dated"]}


def test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back(
    home, silence, monkeypatch
):
    cfg, folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Gone": None, "Kept": None})
    # The account, listed whole, no longer carries the first and dates the second nowhere.
    _account(monkeypatch, {"Kept": None})

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert shown["undated"] == 1 and shown["dates asked of the account"] == 0
    assert [(item["title"], item["month"], item["dated_by"]) for item in shown["items"]] == [
        ("Probe - Kept", "Undated", "none")
    ]
    assert shown["taken back"] == ["Probe - Gone, no longer on the account"]
    note = _note(acted, backfill_cli.UNDATED)
    assert "1 heart(s) carry no date" in note and "nothing moves a heart" in note
    assert "Probe - Gone (no longer on the account)" in _note(acted, backfill_cli.TAKEN_BACK)
    assert _favorites(cfg, folder_id) == {SOURCE: ["Kept"], "Undated": ["Kept"]}


def test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date(
    home, silence, monkeypatch
):
    cfg, folder_id, _source_id = home
    hearts_swept(cfg, {"Twice": UNKNOWN}, run_id="")
    _landed_hearts(cfg, silence, {"Twice": "2026-09-29T22:00:00+00:00"}, batch="2026-09-30-favorites")
    fake = _account(monkeypatch, {"Twice": NOV})

    _acted, refused = _approved()

    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["month"], item["dated_by"]) == ("2026-09", "job")
    assert fake.heart_listings == 2
    assert _favorites(cfg, folder_id) == {SOURCE: ["Twice"], "2026-09": ["Twice"]}


def test_the_record_carries_the_placement_under_the_favourites_key(home, silence, monkeypatch):
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})

    acted, _refused = _approved()

    (record,) = [r for r in session.records(cfg) if r.workflow == backfill.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert record.detail[placement.PLACED_KEY]["added_source"] == 1
    assert [(c.tree, c.created) for c in record.change.trees] == [(placement.RECORD_KEY, 2)]
    assert record.session_id in _note(acted, backfill_cli.PLACED)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(home, silence, monkeypatch):
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    session.ack_path(cfg).unlink()

    code, refused = drive(VERB)

    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_with_no_source_playlist_the_verb_refuses_by_name_before_the_gate(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    _landed_hearts(cfg, silence, {"Same Girl": None})
    fake = _account(monkeypatch, {"Same Girl": SEP})

    code, refused = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == placement.SOURCE_MISSING
    assert fake.heart_listings == 0, "the home is resolved before the library is walked"


def test_an_unreadable_account_refuses_only_when_a_heart_needs_placing(
    home, silence, monkeypatch
):
    """Every heart to place is checked against the account (U146); a placed library never asks."""
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Dated": NOV_ISO})
    _account(monkeypatch, {"Dated": NOV})
    acted, _refused = _approved()

    class Unreadable:
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing failed")

    monkeypatch.setattr(catalogue, "resolve", lambda _cfg: Unreadable())
    acted, _refused = _approved()
    assert acted["outcome"] == "no_op"

    _landed_hearts(cfg, silence, {"Undated Too": None}, batch="2026-09-30-favorites")
    code, refused = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"


def test_with_nothing_landed_the_gate_is_still_asked_and_nothing_is_written(
    home, monkeypatch
):
    cfg, folder_id, _source_id = home
    fake = _account(monkeypatch, {})

    acted, refused = _approved()

    assert acted["outcome"] == "no_op"
    assert refused["cause"]["detail"]["shown"]["hearts to place"] == 0
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_no_content_row_tempo_or_rating_is_written(home, silence, monkeypatch):
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")

    _approved()

    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == before
    ((bpm, rating, analysis),) = _query(
        cfg, "SELECT BPM, Rating, AnalysisDataPath FROM djmdContent WHERE Title = 'Same Girl'"
    )
    assert bpm in (None, 0) and rating in (None, 0) and not analysis


def test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated(
    home, silence, monkeypatch
):
    """R-504: a heart absent from a short listing may be one withheld, and Undated is for good."""
    cfg, folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Served": None, "Withheld": None})

    class Short(FakeCatalogue):
        def favourite_tracks(self):
            raise catalogue.HeartsShortfall(self.hearts, 5)

    served = Track("tid-Served", "Probe", "Served")
    served.user_date_added = SEP
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Short(hearts=[served])))

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert [item["title"] for item in shown["items"]] == ["Probe - Served"]
    assert shown["held back"].startswith("1 heart(s) the account's listing did not carry, 4 withheld")
    note = _note(acted, backfill_cli.HELD_BACK)
    assert "held back unplaced" in note and "4 withheld" in note
    assert acted["data"]["totals"]["held back"] == 1
    assert _favorites(cfg, folder_id) == {SOURCE: ["Served"], "2026-09": ["Served"]}


def test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named(
    home, silence, monkeypatch
):
    cfg, folder_id, _source_id = home
    with jobs.open_store() as store:
        old = jobs.enqueue(
            store,
            handler_key="intake.playlist",
            payload={"source": "favorites", "source_id": intake_cli.FAVORITES_SOURCE_ID},
            cfg=cfg,
            item_ids=(),
        )
        jobs.transition(store, old.job_id, jobs.JobState.SUCCEEDED)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})

    acted, refused = _approved()

    assert refused["cause"]["detail"]["shown"]["jobs unread"] == [old.job_id]
    assert old.job_id in _note(acted, backfill_cli.JOBS_UNREAD)
    assert _favorites(cfg, folder_id) == {SOURCE: ["Same Girl"], "2026-09": ["Same Girl"]}


def test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill(
    native_library, silence, monkeypatch
):
    """A landing of an older job puts the heart in All Favorites alone; the backfill adds its month."""
    from tests.test_intake_land_account_playlists_native import PASS

    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    hearts_swept(cfg, {"Old": UNKNOWN})
    _stage(cfg, silence, "Old")
    code, acted, _refused = _two_acts(["intake", "land", "--pass", PASS])
    assert code == int(ExitCode.OK), acted
    assert _favorites(cfg, folder_id) == {SOURCE: ["Old"]}
    _account(monkeypatch, {"Old": NOV})

    acted, refused = _approved()

    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["into_source"], item["into_month"], item["month"]) == (False, True, "2026-11")
    assert acted["data"]["totals"]["added"] == 1
    assert _favorites(cfg, folder_id) == {SOURCE: ["Old"], "2026-11": ["Old"]}


def test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one(
    home, silence, monkeypatch
):
    """The state rule is gone (U146): a heart owned when its job ran is placed all the same."""
    cfg, folder_id, _source_id = home
    _seed(cfg, silence, "Already", batch="2026-09-20 by hand")
    hearts_swept(cfg, {"Already": UNKNOWN, "Fresh": UNKNOWN}, run_id="")
    _seed(cfg, silence, "Fresh")
    _account(monkeypatch, {"Already": SEP, "Fresh": NOV})

    acted, refused = _approved()

    assert [item["title"] for item in refused["cause"]["detail"]["shown"]["items"]] == [
        "Probe - Already",
        "Probe - Fresh",
    ]
    placed = _favorites(cfg, folder_id)
    assert sorted(placed[SOURCE]) == ["Already", "Fresh"]
    assert (placed["2026-09"], placed["2026-11"]) == (["Already"], ["Fresh"])


def test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone(
    home, silence, monkeypatch
):
    """The path rule is gone (U146): a carried heart whose row sits two folders deep is placed."""
    cfg, folder_id, _source_id = home
    hearts_swept(cfg, {"Deep Filed": UNKNOWN, "Landed": UNKNOWN}, run_id="")
    _deep_row(cfg, silence, "Deep Filed")
    _seed(cfg, silence, "Landed")
    _account(monkeypatch, {"Deep Filed": SEP, "Landed": NOV})

    acted, refused = _approved()

    assert _rows(cfg)["Deep Filed"], "the collection holds the deep row"
    assert [item["title"] for item in refused["cause"]["detail"]["shown"]["items"]] == [
        "Probe - Deep Filed",
        "Probe - Landed",
    ]
    placed = _favorites(cfg, folder_id)
    assert (placed["2026-09"], placed["2026-11"]) == (["Deep Filed"], ["Landed"])


def test_the_write_itself_refuses_a_plan_whose_home_moved_with_no_gate_in_front(
    home, silence, monkeypatch
):
    """The engine's own stale check, driven without the gate that would refuse first."""
    cfg, _folder_id, source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    approved = backfill_cli.planned(cfg, source=SOURCE)
    assert approved.writes
    _put(cfg, source_id, _rows(cfg)["Same Girl"])

    with pytest.raises(CratekitError) as caught:
        backfill_cli.written(cfg, approved, source=SOURCE)

    assert caught.value.cause.reason == "decision-stale"
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-09'") == []


def test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back(
    home, silence, monkeypatch
):
    """A membership marked removed is the author's no, read so run after run."""
    cfg, folder_id, source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None, "Kept": None})
    _account(monkeypatch, {"Same Girl": SEP, "Kept": SEP})
    _approved()
    assert sorted(_favorites(cfg, folder_id)[SOURCE]) == ["Kept", "Same Girl"]
    _take_out(cfg, source_id, _rows(cfg)["Same Girl"])
    assert _live(cfg, source_id) == [_rows(cfg)["Kept"]]

    acted, refused = _approved()

    assert acted["outcome"] == "no_op"
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == [] and shown["already placed"] == 1, "Kept is placed already"
    assert shown["taken back"] == ["Probe - Same Girl, removed from the playlist in rekordbox"]
    assert "removed from the playlist in rekordbox" in _note(acted, backfill_cli.TAKEN_BACK)
    assert _live(cfg, source_id) == [_rows(cfg)["Kept"]]
    assert acted["data"]["totals"]["taken back"] == 1


def test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks(
    home, silence, monkeypatch
):
    """With no published count a heart the listing lacks cannot be told from one withheld."""
    cfg, folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Served": None, "Absent": None})
    _account(monkeypatch, {"Served": SEP}, declared=None)

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert [item["title"] for item in shown["items"]] == ["Probe - Served"]
    assert shown["held back"].startswith(
        "1 heart(s) the account's listing did not carry, the listing published no count"
    )
    assert "no published count" in _note(acted, backfill_cli.HELD_BACK)
    assert "taken back" not in shown
    assert _favorites(cfg, folder_id) == {SOURCE: ["Served"], "2026-09": ["Served"]}


def test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan(
    home, silence, monkeypatch
):
    """The digest covers the month rows, so the write never makes a playlist the screen did not list."""
    cfg, folder_id, _source_id = home
    with _db(cfg) as handle:
        q3_id = str(handle.create_playlist("2026-09", parent=handle.get_playlist(ID=folder_id)).ID)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    approved = backfill_cli.planned(cfg, source=SOURCE)
    assert approved.placements.creates == ()
    assert approved.identity()["months"] == {"2026-09": q3_id}
    with _db(cfg) as handle:
        handle.get_playlist(ID=q3_id).rb_local_deleted = 1

    with pytest.raises(CratekitError) as caught:
        backfill_cli.written(cfg, approved, source=SOURCE)

    assert caught.value.cause.reason == "decision-stale"
    assert _query(
        cfg, "SELECT COUNT(*) FROM djmdPlaylist WHERE Name = '2026-09' AND rb_local_deleted = 0"
    ) == [(0,)]


def test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named(
    home, silence, monkeypatch
):
    """Five owned hearts All Favorites lacks, one off the account and one taken out: three placed."""
    cfg, folder_id, source_id = home
    rows = {title: _deep_row(cfg, silence, title) for title in ("Aug", "Sep A", "Sep B", "Gone", "Out")}
    hearts_swept(
        cfg,
        {
            "Aug": "2026-08-02T10:00:00+00:00",
            "Sep A": "2026-09-01T10:00:00+00:00",
            "Sep B": UNKNOWN,
            "Gone": "2026-09-03T10:00:00+00:00",
            "Out": "2026-09-04T10:00:00+00:00",
        },
        run_id="",
    )
    _put(cfg, source_id, rows["Out"])
    _take_out(cfg, source_id, rows["Out"])
    _account(monkeypatch, {"Aug": SEP, "Sep A": SEP, "Sep B": SEP, "Out": SEP})

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert shown["hearts to place"] == 3
    assert shown["by month"] == ["2026-08: 1", "2026-09: 2"]
    assert shown["dates asked of the account"] == 1, "Sep B's job froze no date"
    assert sorted(shown["taken back"]) == [
        "Probe - Gone, no longer on the account",
        "Probe - Out, removed from the playlist in rekordbox",
    ]
    placed = _favorites(cfg, folder_id)
    assert sorted(_live(cfg, source_id)) == sorted(rows[t] for t in ("Aug", "Sep A", "Sep B"))
    assert placed["2026-08"] == ["Aug"] and sorted(placed["2026-09"]) == ["Sep A", "Sep B"]

    acted, refused = _approved()

    assert acted["outcome"] == "no_op", "the second run plans nothing"
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == [] and shown["already placed"] == 3


def test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month(
    home, silence, monkeypatch
):
    """A dated playlist beside the source files it already, even where the account dates it now."""
    cfg, folder_id, source_id = home
    row = _deep_row(cfg, silence, "Filed")
    hearts_swept(cfg, {"Filed": None}, run_id="")
    with _db(cfg) as handle:
        undated = handle.create_playlist("Undated", parent=handle.get_playlist(ID=folder_id))
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.add_to_playlist(undated, row)
    fake = _account(monkeypatch, {"Filed": NOV})

    acted, refused = _approved()

    # The row, placed by hand with no colour, takes Pink (U153), and no month is given.
    assert acted["outcome"] == "ok" and acted["data"]["totals"]["added"] == 0
    assert acted["data"]["totals"]["coloured"] == 1
    assert refused["cause"]["detail"]["shown"]["already placed"] == 1
    assert fake.heart_listings == 0, "nothing to place, so the account is not asked"
    assert _favorites(cfg, folder_id) == {SOURCE: ["Filed"], "Undated": ["Filed"]}


def test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month(
    native_library, silence, monkeypatch
):
    """At the playlist root every root playlist sits beside the source, and only a dated one files."""
    cfg, _root_id = native_library
    _folder_id, source_id = _home(cfg, folder=False)
    row = _deep_row(cfg, silence, "Rooted")
    hearts_swept(cfg, {"Rooted": NOV_ISO}, run_id="")
    with _db(cfg) as handle:
        other = handle.create_playlist("Warmup")
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.add_to_playlist(other, row)
    _account(monkeypatch, {"Rooted": NOV})

    acted, refused = _approved()

    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["into_source"], item["into_month"], item["month"]) == (False, True, "2026-11")
    ((month,),) = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-11' AND rb_local_deleted = 0"
    )
    assert _live(cfg, str(month)) == [row]


def test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now(
    home, silence, monkeypatch
):
    """Only a row with no date key at all is dated from the listing, so it files as the landing would."""
    cfg, folder_id, _source_id = home
    _deep_row(cfg, silence, "Dateless")
    hearts_swept(cfg, {"Dateless": None}, run_id="")
    _account(monkeypatch, {"Dateless": NOV})

    acted, refused = _approved()

    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["month"], item["dated_by"]) == ("Undated", "none")
    assert _favorites(cfg, folder_id) == {SOURCE: ["Dateless"], "Undated": ["Dateless"]}


def test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back(
    home, silence, monkeypatch
):
    """A removed membership beside a live one is a heart put back, not one taken back."""
    cfg, folder_id, source_id = home
    row = _deep_row(cfg, silence, "Back Again")
    hearts_swept(cfg, {"Back Again": NOV_ISO}, run_id="")
    _put(cfg, source_id, row)
    _take_out(cfg, source_id, row)
    _put(cfg, source_id, row)
    assert _live(cfg, source_id) == [row]
    _account(monkeypatch, {"Back Again": NOV})

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert "taken back" not in shown
    (item,) = shown["items"]
    assert (item["into_source"], item["into_month"], item["month"]) == (False, True, "2026-11")
    assert _favorites(cfg, folder_id)["2026-11"] == ["Back Again"]


def _paint(cfg, title: str, colour_id: str) -> None:
    """A colour set by hand, or a row placed before U153 that carries none."""
    import sqlite3

    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdContent SET ColorID = ? WHERE Title = ?", (colour_id, title))
        conn.commit()
    finally:
        conn.close()


def test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one(
    home, silence, monkeypatch
):
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None, "Fractals": None, "Find My Way": None})
    fake = _account(monkeypatch, {"Same Girl": SEP, "Fractals": SEP, "Find My Way": SEP})
    acted, _refused = _approved()
    assert acted["data"]["totals"]["coloured"] == 3
    assert all(_colour_of(cfg, title) == PINK_ID for title in ("Same Girl", "Fractals", "Find My Way"))
    # As the library stood before U153: placed, and no colour on two, Red on one.
    _paint(cfg, "Same Girl", "0")
    _paint(cfg, "Fractals", "")
    _paint(cfg, "Find My Way", RED_ID)
    listings = fake.heart_listings

    acted, refused = _approved()

    shown = refused["cause"]["detail"]["shown"]
    assert shown["hearts to place"] == 0 and shown["memberships to add"] == 0
    assert shown["rows to colour Pink"] == 2
    assert shown["colour held"] == ["Find My Way (Red)"]
    assert sorted((item["action"], item["title"]) for item in shown["items"]) == [
        ("colour", "Fractals"),
        ("colour", "Same Girl"),
    ]
    assert fake.heart_listings == listings, "a colour needs no account call"
    assert (_colour_of(cfg, "Same Girl"), _colour_of(cfg, "Fractals")) == (PINK_ID, PINK_ID)
    assert _colour_of(cfg, "Find My Way") == RED_ID
    totals = acted["data"]["totals"]
    assert (totals["added"], totals["coloured"], totals["colours"], totals["colour held"]) == (0, 2, 2, 1)
    assert _note(acted, backfill_cli.COLOUR_HELD).endswith("keep it: Find My Way (Red)")
    note = _note(acted, backfill_cli.PLACED)
    assert "2 row(s) coloured Pink" in note and "2 placed row(s)" in note
    # The record carries the colour as rows updated under the favourites key.
    records = [r for r in session.records(cfg) if r.workflow == backfill.WORKFLOW]
    assert len(records) == 2, "the first run and this one"
    assert sorted(len(r.detail["favorites_placed"]["coloured"]) for r in records) == [2, 3]
    assert all(r.state is session.SessionState.CLOSED for r in records)

    code, acted, refused = _acts()

    assert acted["outcome"] == "no_op", acted
    assert refused["cause"]["detail"]["shown"]["rows to colour Pink"] == 0
    assert refused["cause"]["detail"]["shown"]["items"] == []


def test_with_no_pink_row_the_backfill_places_the_hearts_and_warns(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg, pink=False)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})

    acted, refused = _approved()

    missing = "the library's colour table has no live row named Pink"
    assert refused["cause"]["detail"]["shown"]["rows to colour Pink"].startswith(f"none, {missing}")
    assert _favorites(cfg, folder_id) == {SOURCE: ["Same Girl"], "2026-09": ["Same Girl"]}
    assert _colour_of(cfg, "Same Girl") in ("", "0")
    assert _note(acted, backfill_cli.PINK_MISSING).startswith(f"no row is coloured: {missing}")
    assert acted["data"]["totals"]["coloured"] == 0


def test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write(
    home, silence, monkeypatch
):
    cfg, _folder_id, _source_id = home
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": SEP})
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _envelope = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    _paint(cfg, "Same Girl", RED_ID)

    code, acted = drive(["--run", run_id, *VERB])

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted["cause"]
    assert _colour_of(cfg, "Same Girl") == RED_ID


def test_member_order_is_numeric_and_tolerates_a_non_numeric_id():
    """A non-numeric content id must not take the whole plan down (U153)."""
    assert backfill._member_order(["10", "2", "1"]) == ["1", "2", "10"]
    assert backfill._member_order(["2", "odd", "1"]) == ["1", "2", "odd"]
