"""U149 at the landing: each account playlist a native landing writes gets its custom playlist twin.

In the landing's one commit, into ``Custom Playlists <landing year>``, with the INBOX
playlist's rows, marked as a pair. Nothing here is real (D1)."""

from __future__ import annotations

from pathlib import Path

from cratekit.core import config, rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, native
from cratekit.modules.outbound import pairs
from cratekit.sync import twins
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import _inbox, _land, _stage, swept
from tests.test_intake_land_account_playlists_native import pinned_day as pinned_day
from tests.test_intake_land_native import _answered, _lands, _members, _query
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence

FOLDER = twins.folder_name(2026)


def _twins(cfg: config.Config) -> dict[str, list[str]]:
    """Every live playlist in the one live ``Custom Playlists 2026`` and the titles it holds."""
    folders = _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
                     "AND COALESCE(rb_local_deleted, 0) = 0", FOLDER)
    if not folders:
        return {}
    ((folder,),) = folders
    rows = _query(cfg, "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND "
                  "rb_local_deleted = 0 ORDER BY Seq", str(folder))
    titles = {str(one): str(title) for one, title in _query(cfg, "SELECT ID, Title FROM djmdContent")}
    return {str(name): [titles[m] for m in _members(cfg, str(playlist_id))]
            for playlist_id, name in rows}


def _make(cfg: config.Config, name: str, *, parent: str = "", folder: bool = False) -> str:
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        above = handle.get_playlist(ID=parent) if parent else None
        make = handle.create_playlist_folder if folder else handle.create_playlist
        made = make(name, parent=above)
        handle.session.commit()
        return str(made.ID)
    finally:
        rb_writer.close_db(handle)


def _codes(envelope: dict) -> set[str]:
    return {warning["code"] for warning in envelope.get("warnings") or ()}


def test_a_landing_that_finishes_two_custom_playlists_writes_two_twins_and_marks_two_pairs(
    native_library, silence
):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One", "Two")), "pl-b": ("Deep Cuts", ("Three",))})
    for title in ("One", "Two", "Three"):
        _stage(cfg, silence, title)
    acted, refused = _lands(verb=_land())
    assert _twins(cfg) == {"Sunset Warmup": ["One", "Two"], "Deep Cuts": ["Three"]}
    assert _inbox(cfg, root_id) == {
        "Sunset Warmup 2026-10-03": ["One", "Two"], "Deep Cuts 2026-10-03": ["Three"]
    }
    held = pairs.PairStore(cfg).all()
    assert sorted(held) == ["pl-a", "pl-b"]
    assert all(one.twin and one.first for one in held.values())
    made = [item for item in acted["data"]["items"] if item["action"] == land_cli.TWIN]
    assert [(item["playlist"], item["account_id"], item["count"]) for item in made] == [
        (f"{FOLDER} / Sunset Warmup", "pl-a", 2), (f"{FOLDER} / Deep Cuts", "pl-b", 1)
    ]
    assert {one["id"] for one in made} == {one.rekordbox_id for one in held.values()}
    assert twins.LANDED in _codes(acted)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["custom playlist twins"] == f"{FOLDER} / Sunset Warmup; {FOLDER} / Deep Cuts"
    # The twin folder is made once, at the top level.
    folders = _query(
        cfg, "SELECT ID, ParentID FROM djmdPlaylist WHERE Name = ? AND rb_local_deleted = 0", FOLDER
    )
    assert len(folders) == 1
    assert str(folders[0][1]) in rb_writer.ROOT_PARENT_SENTINELS


def test_an_account_playlist_already_paired_gets_no_second_twin(native_library, silence):
    cfg, _root_id = native_library
    mine = _make(cfg, "Mine")
    pairs.PairStore(cfg).mark("pl-a", mine, name="Sunset Warmup")
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",)), "pl-b": ("Deep Cuts", ("Two",))})
    for title in ("One", "Two"):
        _stage(cfg, silence, title)
    _lands(verb=_land())
    assert _twins(cfg) == {"Deep Cuts": ["Two"]}
    assert pairs.PairStore(cfg).get("pl-a").rekordbox_id == mine
    assert not pairs.PairStore(cfg).get("pl-a").twin


def test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands(
    native_library, silence
):
    cfg, root_id = native_library
    folder = _make(cfg, FOLDER, folder=True)
    _make(cfg, "Sunset Warmup", parent=folder)
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    _stage(cfg, silence, "One")
    acted, refused = _lands(verb=_land())
    assert _inbox(cfg, root_id) == {"Sunset Warmup 2026-10-03": ["One"]}
    assert _twins(cfg) == {"Sunset Warmup": []}, "a second twin was made beside the first"
    assert pairs.PairStore(cfg).all() == {}
    assert land_cli.TWINS_LEFT in _codes(acted)
    assert "gets none" in refused["cause"]["detail"]["shown"]["custom playlist twins"]


def test_a_folder_made_after_the_gate_refuses_and_moves_nothing(native_library, silence):
    cfg, root_id = native_library
    swept(cfg, {"pl-a": ("Sunset Warmup", ("One",))})
    staged = _stage(cfg, silence, "One")
    run_id = _answered(_land())[1]
    _make(cfg, FOLDER, folder=True)
    code, acted = drive(["--run", run_id, *_land()])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted["cause"]
    assert staged.exists(), "the file moved under a plan that was stale"
    assert _inbox(cfg, root_id) == {}
    assert pairs.PairStore(cfg).all() == {}


def test_a_plan_with_no_account_playlist_plans_no_twin_and_digests_as_before():
    plan = native.NativePlan(
        tree_id="t", root_id="r", root_name="INBOX", playlist="b", database=Path("x"),
        device_id="d", master_db_id="m", base_drive=None, current_drive=None, rows=(), link=None,
        digest="",
    )
    assert "twins" not in native.identity(plan)
