"""U120 on the native medium: a heart the favourites sync lands joins All Favorites and its month.

The hearts job run as ``crate sync all`` runs it, then landed with ``--pass``. D1.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.core import analysis_store, config, jobs, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import placement
from cratekit.intake import account_playlists, batch_name, land_cli, missing_cli, native
from cratekit.intake import cli as intake_cli
from cratekit.write import genre_favorites
from tests import cutover_fixtures
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import PASS, RUN, _inbox, _stage, swept
from tests.test_intake_land_account_playlists_native import pinned_day as pinned_day
from tests.test_intake_land_native import _members, _music, _query, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence

DECLARED = taxonomy.default_taxonomy()
CLASS = DECLARED.sub_class("favorites")
SOURCE = CLASS.signal_playlist
NOV = "2026-11-03T12:00:00+00:00"
SEP = "2026-09-29T22:00:00+00:00"
#: A row a build before U120 froze: no date key at all, so the month is unknown.
UNKNOWN = "unknown"


def hearts_swept(
    cfg: config.Config, titles: dict[str, str | None], *, run_id: str = RUN
) -> jobs.Job:
    """One hearts job, ``title -> when hearted, None for undated, UNKNOWN for no key``, run."""
    tracks = {}
    for title, hearted in titles.items():
        row = {"artist": "Probe", "title": title, "origin": match.TIDAL, "ref": f"tid-{title}"}
        if hearted is not UNKNOWN:
            row[intake_cli.HEARTED] = hearted
        tracks[f"tid-{title}"] = row
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store,
            cfg,
            handler_key="intake.playlist",
            reference=intake_cli.FAVORITES,
            tracks=tracks,
            run_id=run_id,
            source_id=intake_cli.FAVORITES_SOURCE_ID,
        )
    code, resumed = drive(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed
    return job


#: Two colour rows: the one the placement writes and one a person might choose (U153).
PINK_ID = "1"
RED_ID = "2"


def _colours(cfg: config.Config, *, pink: bool = True) -> None:
    """The colour table as rekordbox ships it, Pink and Red, or Red alone."""
    from pyrekordbox.db6 import tables

    from tests.test_rb_writer_db import _row

    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        have = {str(row.ID) for row in handle.get_color()}
        if pink and PINK_ID not in have:
            handle.session.add(
                _row(tables.DjmdColor, ID=PINK_ID, ColorCode=1, SortKey=1, Commnt="Pink")
            )
        if RED_ID not in have:
            handle.session.add(
                _row(tables.DjmdColor, ID=RED_ID, ColorCode=2, SortKey=2, Commnt="Red")
            )
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


def _home(cfg: config.Config, *, folder: bool = True, pink: bool = True) -> tuple[str, str]:
    """The Favorites folder holding an empty All Favorites, as the source system left it, and the colours."""
    _colours(cfg, pink=pink)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        parent = handle.create_playlist_folder("Favorites") if folder else None
        row = handle.create_playlist(SOURCE, parent=parent)
        handle.session.commit()
        return ("" if parent is None else str(parent.ID)), str(row.ID)
    finally:
        rb_writer.close_db(handle)


def _colour_of(cfg: config.Config, title: str) -> str:
    """The colour a row reads, by title, as rekordbox would show it."""
    ((value,),) = _query(cfg, "SELECT ColorID FROM djmdContent WHERE Title = ?", title)
    return str(value or "")


def _favorites(cfg: config.Config, folder_id: str) -> dict[str, list[str]]:
    """Every live plain playlist under the Favorites folder and the titles it holds."""
    rows = _query(
        cfg,
        "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND Attribute = 0 "
        "AND rb_local_deleted = 0 ORDER BY Name",
        folder_id,
    )
    titles = {str(i): str(t) for i, t in _query(cfg, "SELECT ID, Title FROM djmdContent")}
    return {str(name): [titles[m] for m in _members(cfg, str(pid))] for pid, name in rows}


def _land(pass_name: str = PASS) -> list[str]:
    return ["intake", "land", "--pass", pass_name]


def _landed() -> tuple[dict, dict]:
    code, acted, refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    return acted, refused


def _hearted(cfg: config.Config, silence: Path, titles: dict[str, str | None], **job) -> None:
    """One hearts job run, and each of its titles staged as a downloaded file."""
    hearts_swept(cfg, titles, **job)
    for title in titles:
        _stage(cfg, silence, title)


def test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it(
    native_library, silence
):
    cfg, root_id = native_library
    folder_id, source_id = _home(cfg)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    _hearted(cfg, silence, {"Hearted": NOV})
    batch = batch_name.readable(cfg, pass_name=PASS)
    acted, refused = _landed()
    assert _inbox(cfg, root_id) == {batch: ["Hearted"], "Sunset Warmup 2026-10-03": ["One"]}
    assert _favorites(cfg, folder_id) == {SOURCE: ["Hearted"], "2026-11": ["Hearted"]}
    # The screen said where the heart goes before anybody answered.
    shown = refused["cause"]["detail"]["shown"]
    assert (
        shown["hearts"]
        == f"1 file(s) the account hearts, into {SOURCE!r} under 'Favorites' and their month"
    )
    assert shown["month playlists"] == ["2026-11 (1 file(s)), made"]
    plan_items = {item["to"]: item for item in shown["items"]}
    assert plan_items[str(_music(cfg, batch) / "Hearted.flac")]["heart"] == "2026-11"
    assert "heart" not in plan_items[str(_music(cfg, batch) / "One.flac")]
    # And the report says what it placed.
    placed = [item for item in acted["data"]["items"] if item["action"] == land_cli.FAVORITES]
    assert [(i["playlist"], i["count"], i.get("created")) for i in placed] == [
        (SOURCE, 1, None),
        ("2026-11", 1, True),
    ]
    assert placed[0]["id"] == source_id
    assert acted["data"]["totals"]["hearts placed"] == 2
    assert acted["data"]["totals"]["memberships"] == 2, "the INBOX count is the INBOX count"
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_PLACED]
    assert note["message"] == (
        f"2 membership(s) placed: 1 into {SOURCE!r} and the rest into 2026-11 (made); "
        f"1 row(s) coloured Pink"
    )
    # And the heart's row is Pink, the file beside it is not (U153).
    assert shown["rows to colour Pink"] == 1
    assert _colour_of(cfg, "Hearted") == PINK_ID
    assert _colour_of(cfg, "One") in ("", "0")
    # In no genre Favorites: the only plain playlists named for the class are none.
    plain = "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 0 AND rb_local_deleted = 0"
    assert _query(cfg, plain, CLASS.display) == []


def test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated(
    native_library, silence
):
    """U145's AE1: the landing given a pass files by month, never by quarter."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _hearted(cfg, silence, {"October": "2026-10-20T18:30:00+00:00", "Hearted": None})
    _acted, refused = _landed()
    assert _favorites(cfg, folder_id) == {
        SOURCE: ["Hearted", "October"],
        "2026-10": ["October"],
        "Undated": ["Hearted"],
    }
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name LIKE '%-Q_'") == []
    assert refused["cause"]["detail"]["shown"]["month playlists"] == [
        "2026-10 (1 file(s)), made",
        "Undated (1 file(s)), made",
    ]


def test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites(
    native_library, silence
):
    """R11: the heart reaches a genre Favorites once adoption files it, and no grid,
    tempo or rating is written for it."""
    cfg, _root_id = native_library
    _home(cfg)
    _hearted(cfg, silence, {"Hearted": NOV})
    _landed()
    (record,) = [r for r in session.records(cfg) if placement.PLACED_KEY in r.detail]
    placed = record.detail[placement.PLACED_KEY]
    assert placed["source"] == SOURCE and placed["added_source"] == 1
    assert [(q["name"], q["added"]) for q in placed["months"]] == [("2026-11", 1)]
    assert placed["created"] == ["2026-11"]
    assert record.detail[native.PASS_KEY] == PASS
    changes = {c.tree: c.created for c in record.change.trees}
    assert changes[placement.RECORD_KEY] == 2
    # U166: the batch's one membership and INBOX / Analyze's one.
    assert changes[DECLARED.intake.id] == 2 and changes[rb_writer.CONTENT_TABLE] == 1
    ((bpm, rating, analysis),) = _query(
        cfg, "SELECT BPM, Rating, AnalysisDataPath FROM djmdContent WHERE Title = ?", "Hearted"
    )
    assert bpm in (None, 0) and rating in (None, 0) and not analysis
    ((content_id,),) = _query(cfg, "SELECT ID FROM djmdContent WHERE Title = ?", "Hearted")
    # The routing tree cut over, one genre folder, one band holding the heart.
    root_id = cutover_fixtures.one_root(cfg, DECLARED.tree.display)
    tree_registry.write(
        cfg,
        tree_registry.read(cfg).with_record(
            tree_registry.TreeRecord(
                tree_id=DECLARED.tree.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 10, 10),
                root_id=root_id,
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )
    soul = DECLARED.bucket("deep_house")
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        folder = handle.create_playlist_folder(soul.display, parent=handle.get_playlist(ID=root_id))
        band = handle.create_playlist("Low", parent=folder)
        handle.add_to_playlist(band, str(content_id))
        handle.session.commit()
        folder_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    outcome = genre_favorites.refresh_additive(
        cfg, DECLARED, analysis_roots=analysis_store.watch_roots(cfg)
    )
    assert outcome.skipped == "" and outcome.refreshed is not None
    assert outcome.refreshed.added == 1
    (favorites,) = _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ? AND rb_local_deleted = 0",
        CLASS.display,
        folder_id,
    )
    assert _members(cfg, str(favorites[0])) == [str(content_id)]


def test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made(
    native_library, silence
):
    """With no Pink row the landing still places the hearts, and warns."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg, pink=False)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist("2026-09", parent=handle.get_playlist(ID=folder_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    _hearted(cfg, silence, {"Older": SEP, "Newer": NOV})
    acted, refused = _landed()
    found = _favorites(cfg, folder_id)
    assert sorted(found[SOURCE]) == ["Newer", "Older"]
    assert found["2026-09"] == ["Older"] and found["2026-11"] == ["Newer"]
    assert refused["cause"]["detail"]["shown"]["month playlists"] == [
        "2026-09 (1 file(s))",
        "2026-11 (1 file(s)), made",
    ]
    assert acted["data"]["totals"]["hearts placed"] == 4
    assert {_colour_of(cfg, "Older"), _colour_of(cfg, "Newer")} <= {"", "0"}
    shown = refused["cause"]["detail"]["shown"]
    assert shown["rows to colour Pink"].startswith("none, the library's colour table has no live row named Pink")
    (note,) = [w for w in acted["warnings"] if w["code"] == "favorites-pink-colour-missing"]
    assert (
        "crate favorites backfill colours them once the library carries Pink again"
        in note["message"]
    )
    (placed,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_PLACED]
    assert placed["message"].endswith("; 0 row(s) coloured Pink")


def test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites(
    native_library, silence
):
    cfg, root_id = native_library
    folder_id, _source_id = _home(cfg)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("Shared",))})
    _hearted(cfg, silence, {"Shared": NOV})
    _landed()
    assert _inbox(cfg, root_id) == {"Sunset Warmup 2026-10-03": ["Shared"]}
    assert _favorites(cfg, folder_id) == {SOURCE: ["Shared"], "2026-11": ["Shared"]}
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE Title = ?", "Shared")) == 1


def test_a_landing_of_no_heart_touches_neither_all_favorites_nor_a_month(native_library, silence):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    acted, refused = _landed()
    assert _favorites(cfg, folder_id) == {SOURCE: []}
    assert "hearts" not in refused["cause"]["detail"]["shown"]
    assert [i for i in acted["data"]["items"] if i["action"] == land_cli.FAVORITES] == []
    assert "hearts placed" not in acted["data"]["totals"]
    assert [w["code"] for w in acted["warnings"] if w["code"].startswith("favorites")] == []


def test_a_landing_given_no_pass_places_no_heart(native_library, silence):
    """Without ``--pass`` nothing ties a file to a hearts job; the backfill places it later."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _hearted(cfg, silence, {"Hearted": NOV}, run_id="")
    code, acted, _refused = _two_acts(["intake", "land", "--name", "2026-10-03 by hand"])
    assert code == int(ExitCode.OK), acted
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said(
    native_library, silence
):
    cfg, root_id = native_library
    _hearted(cfg, silence, {"Hearted": NOV})
    batch = batch_name.readable(cfg, pass_name=PASS)
    acted, refused = _landed()
    assert _inbox(cfg, root_id) == {batch: ["Hearted"]}
    shown = refused["cause"]["detail"]["shown"]
    assert shown["hearts"].startswith("none placed, this library holds no live playlist named")
    (skipped,) = [i for i in shown["items"] if i["action"] == land_cli.FAVORITES]
    assert skipped["playlist"] == SOURCE and "no live playlist" in skipped["skipped"]
    assert shown["count"] == 2, "the skip is an item of the plan the digest covers"
    assert acted["data"]["totals"]["count"] == 1, "and not a file"
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_SKIPPED]
    assert (
        "no heart was placed" in note["message"] and "crate favorites backfill" in note["message"]
    )
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name IN ('2026-11', ?)", SOURCE) == []
    assert "hearts placed" not in acted["data"]["totals"]


def test_two_source_playlists_skip_the_placement_too(native_library, silence):
    cfg, _root_id = native_library
    _home(cfg)
    _home(cfg, folder=False)
    _hearted(cfg, silence, {"Hearted": NOV})
    acted, _refused = _landed()
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_SKIPPED]
    assert "2 live playlists" in note["message"]


def test_a_source_at_the_root_takes_its_months_beside_it(native_library, silence):
    cfg, _root_id = native_library
    _folder_id, source_id = _home(cfg, folder=False)
    _hearted(cfg, silence, {"Hearted": NOV})
    _acted, refused = _landed()

    assert refused["cause"]["detail"]["shown"]["hearts"].endswith(f"into {SOURCE!r} and their month")
    rows = _query(
        cfg,
        "SELECT Name, ParentID FROM djmdPlaylist WHERE Name = '2026-11' AND rb_local_deleted = 0",
    )
    assert [(n, str(p) in rb_writer.ROOT_PARENT_SENTINELS) for n, p in rows] == [("2026-11", True)]
    assert _members(cfg, source_id) == _members(cfg, str(_query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-11'")[0][0]))


def test_the_hearts_are_in_the_digest_so_another_set_is_another_plan(native_library, silence, monkeypatch):
    """And a home's refusal that is not the missing source refuses the landing."""
    cfg, _root_id = native_library
    _home(cfg)
    _hearted(cfg, silence, {"Hearted": NOV})
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, land_cli.NATIVE_GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    # Between the answer and the write the heart's month reads differently.
    monkeypatch.setattr(placement.placeholders, "month_label", lambda hearted: "2027-01")

    code, acted = drive(["--run", run_id, *_land()])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert (Path(cfg.paths.download_staging) / "Hearted.flac").is_file()

    def broken(db, name):
        raise refuse("decision-stale", "the playlist table could not be read", origin=("t",))

    monkeypatch.setattr(placement, "resolve_home", broken)
    code, refused = drive(_land())
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "decision-stale"
    assert (Path(cfg.paths.download_staging) / "Hearted.flac").is_file()


def test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart(
    native_library, silence
):
    """The claim rule alone, without a landing."""
    cfg, _root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    hearts_swept(cfg, {"Hearted": NOV, "Nowhere": SEP})
    staged = [_stage(cfg, silence, "One"), _stage(cfg, silence, "Hearted")]
    found = account_playlists.hearted(cfg, PASS, staged)
    assert [(one.path.name, one.month, one.ref) for one in found] == [
        ("Hearted.flac", "2026-11", "tid-Hearted")
    ]
    assert account_playlists.hearted(cfg, None, staged) == ()
    assert account_playlists.hearted(cfg, missing_cli.synced_name("no-such-run"), staged) == ()
    rows = account_playlists.hearts(cfg, PASS)
    assert sorted(row.ref for row in rows) == ["tid-Hearted", "tid-Nowhere"]
    assert {row.ref: row.hearted.isoformat() for row in rows} == {
        "tid-Hearted": NOV,
        "tid-Nowhere": SEP,
    }
    # Two hearts jobs in one pass, one with no date: the claim takes the one that
    # knows, as the backfill does.
    hearts_swept(cfg, {"Twice": UNKNOWN})
    hearts_swept(cfg, {"Twice": SEP})
    (found,) = account_playlists.hearted(cfg, PASS, [_stage(cfg, silence, "Twice")])
    assert (found.month, found.known) == ("2026-09", True)


def test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month(
    native_library, silence
):
    """An older job froze no date: All Favorites, and the month left to the backfill,
    never Undated, which the backfill would place twice."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _hearted(cfg, silence, {"Old": UNKNOWN, "New": NOV})
    acted, refused = _landed()
    assert _favorites(cfg, folder_id) == {SOURCE: ["New", "Old"], "2026-11": ["New"]}
    shown = refused["cause"]["detail"]["shown"]
    assert shown["month playlists"] == ["2026-11 (1 file(s)), made"]
    assert shown["month left to the backfill"].startswith("1 file(s) whose job froze no date")
    by_name = {Path(item["to"]).name: item for item in shown["items"] if "to" in item}
    assert by_name["Old.flac"]["heart"] == "month left to the backfill"
    assert by_name["New.flac"]["heart"] == "2026-11"
    assert acted["data"]["totals"]["hearts placed"] == 3
