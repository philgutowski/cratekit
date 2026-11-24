"""U165: a native landing files its batch into BY GENRE + ENERGY under the same answer.

On the native suite's disposable database with the routing tree cut over. Nothing here names a
real volume, person or track (D1)."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import apply_cli, collection
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.scan import Disposition, Readability
from cratekit.core import config, rb_writer, tags, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import filing, native
from cratekit.write.routing_pass import destination
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import _opened
from tests.test_intake_land_native import DECLARED, _answered, _land, _lands, _query, _shown, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence
from tests.test_intake_land_vox_native import _calibrate, _content_id, _seed_vocals


@pytest.fixture
def cfg(native_library) -> config.Config:
    """The native intake library with its routing tree cut over too, so a landing files."""
    cfg, _root_id = native_library
    with _opened(cfg, unlock=False) as handle:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        tree_root = str(root.ID)
    tree_registry.record_cutover(cfg, DECLARED.tree.id, root_id=tree_root, on=date(2026, 10, 31),
                                 source=tree_registry.DerivationSource.TAXONOMY)
    return cfg


def _file(cfg: config.Config, silence: Path, name: str, **fields: object) -> Path:
    path = _stage(cfg, silence, name)
    if fields:
        assert tags.write_tags(path, fields)
    return path


def _homes(cfg: config.Config, content_id: str) -> set[tuple[str, str]]:
    """Every (folder, playlist) under the routing tree that holds this row, by display name."""
    rows = _query(
        cfg, "SELECT folder.Name, playlist.Name FROM djmdSongPlaylist member "
        "JOIN djmdPlaylist playlist ON playlist.ID = member.PlaylistID "
        "JOIN djmdPlaylist folder ON folder.ID = playlist.ParentID "
        "JOIN djmdPlaylist tree ON tree.ID = folder.ParentID "
        "WHERE member.ContentID = ? AND tree.Name = ? AND member.rb_local_deleted = 0",
        content_id, DECLARED.tree.display,
    )
    return {(str(folder), str(playlist)) for folder, playlist in rows}


def _five(cfg: config.Config, silence: Path) -> None:
    """Three files with a genre, one without, and one vocal, as the brief lists them."""
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    _file(cfg, silence, "Two.flac", genre="Techno", energylevel=8)
    _file(cfg, silence, "Three.flac", genre="Tech House")
    path = _file(cfg, silence, "Four.flac")
    assert tags.clear_tags(path, ("genre",))
    _file(cfg, silence, "Five.flac", genre="Deep House", energylevel=6, voxlevel="9")


def test_five_files_land_and_file_under_one_answer(cfg, silence):
    _calibrate(cfg)
    _seed_vocals(cfg)
    _five(cfg, silence)
    acted, refused = _lands()
    shown = refused["cause"]["detail"]["shown"]
    assert shown["files after landing"].startswith(f"4 new row(s) into {DECLARED.tree.id}")
    assert "1 placed nowhere" in shown["files after landing"]
    predicted = {Path(item["to"]).name: item["files into"] for item in shown["items"]}
    assert predicted["Four.flac"].startswith("placed nowhere")
    assert "with_vox" in predicted["Five.flac"]
    assert acted["data"]["totals"]["filing"] == filing.FILED
    assert acted["data"]["totals"]["filed"] == 4
    assert acted["data"]["totals"]["placed nowhere"] == 1
    reported = {Path(item["to"]).name: item for item in acted["data"]["items"] if "to" in item}
    assert reported["Four.flac"]["files into"] == predicted["Four.flac"]
    codes = [one["code"] for one in acted.get("warnings", [])]
    assert filing.FILED_DIFFERENTLY_WARNING not in codes
    assert filing.NOT_FILED_WARNING not in codes
    for name, genre, energy in (
        ("One.flac", "deep_house", 7), ("Two.flac", "techno", 8), ("Three.flac", "tech_house", None)
    ):
        words = {"deep_house": "Deep House", "techno": "Techno", "tech_house": "Tech House"}
        place = filing.plan_engine.predicted_place(DECLARED, words[genre], energy, vox=False)
        assert place.bucket == genre
        assert destination(DECLARED, place.bucket, place.sub) in _homes(cfg, _content_id(cfg, name))
    assert _homes(cfg, _content_id(cfg, "Four.flac")) == set()
    vocal = filing.plan_engine.predicted_place(DECLARED, "Deep House", 6, vox=True)
    five = _homes(cfg, _content_id(cfg, "Five.flac"))
    assert destination(DECLARED, vocal.bucket, vocal.sub) in five
    assert destination(DECLARED, vocal.bucket, vocal.vocal_sub) in five
    # What was filed is what ``adopt apply`` then finds nothing to do for.
    collection.reset_cache()
    plan = apply_cli.current_plan(cfg, DECLARED, scope=frozenset({_content_id(cfg, "One.flac")}))
    assert apply_engine.outstanding(plan, apply_engine.read(cfg)) == ()


def test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so(cfg, silence, monkeypatch):
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    real = apply_cli.current_plan

    def moved(cfg, declared, **kwargs):
        # THE TREE MOVED BETWEEN THE ANSWER AND THE FILING: every sub reads
        # another, which is what a retagged energy or a redeclared band does.
        plan = real(cfg, declared, **kwargs)
        entries = tuple(replace(entry, sub="elsewhere") for entry in plan.entries)
        return replace(plan, entries=entries)
    monkeypatch.setattr(filing.apply_cli, "current_plan", moved)
    acted = _lands()[0]
    code = filing.FILED_DIFFERENTLY_WARNING
    (warning,) = [one for one in acted["warnings"] if one["code"] == code]
    assert "One.flac" in warning["message"] and filing.ADOPT_APPLY in warning["message"]
    assert acted["data"]["totals"]["filing"] == filing.FILED_DIFFERENTLY
    assert acted["data"]["totals"]["added"] == 1
    assert _homes(cfg, _content_id(cfg, "One.flac")) == set()


def test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart(cfg, silence):
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    _file(cfg, silence, "Two.flac")
    code, rehearsed = drive(_land("--rehearse"))
    assert code == int(ExitCode.OK), rehearsed
    filed = shown = _shown(_land())
    assert shown["digest"] == rehearsed["data"]["digest"]
    assert "equal to this plan's" in shown["rehearsal"]
    assert all("files into" in item for item in shown["items"])
    # Land only files nothing, and digests apart from the landing that files.
    acted, refused = _lands("--land-only")
    shown = refused["cause"]["detail"]["shown"]
    assert shown["files after landing"] == "nothing, asked with --land-only"
    assert not any("files into" in item for item in shown["items"])
    assert shown["digest"] != filed["digest"]
    assert "filing" not in acted["data"]["totals"]
    assert _homes(cfg, _content_id(cfg, "One.flac")) == set()


def test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it(
        native_library, silence):
    cfg, _root = native_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    acted, refused = _lands()
    fact = refused["cause"]["detail"]["shown"]["files after landing"]
    assert fact.startswith("nothing, ") and "xml bridge" in fact
    assert f"crate tree cutover {DECLARED.tree.id}" in fact
    assert "filing" not in acted["data"]["totals"]


def test_a_landing_that_adds_no_row_files_nothing():
    landed = native.NativeLanded(
        tree_id="t", playlist="p", playlist_id="", added=(), present=(), memberships_added=0,
        session_id="s")
    place = filing.plan_engine.predicted_place(DECLARED, "Deep House", 7, vox=False)
    predicted = (filing.Prediction(target=Path("/nowhere/One.flac"), place=place),)
    found = filing.file_landed(None, DECLARED, predicted, landed, actor="session")
    assert found.state == filing.NOTHING_TO_FILE


def test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows(cfg, silence):
    """The filing forgets a collection cache read before the commit."""
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    run_id = _answered(_land())[1]
    collection.reset_cache()
    collection.read_collection(cfg)
    code, acted = drive(["--run", run_id, *_land()])
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["filing"] == filing.FILED
    assert _homes(cfg, _content_id(cfg, "One.flac")) != set()


def test_a_landed_row_the_tree_could_not_place_refuses_before_the_ledger_is_marked():
    """The adopt worker's rule (R-148): a skipped membership stops the filing."""
    filing._refuse_unplaced(SimpleNamespace(skipped=()))
    skipped = SimpleNamespace(skipped=(SimpleNamespace(requested="Deep House / Mid"),))
    with pytest.raises(CratekitError) as caught:
        filing._refuse_unplaced(skipped)
    assert caught.value.cause.reason == "adopt-entries-failed"
    assert caught.value.cause.detail["unplaced"] == ["Deep House / Mid"]


def test_a_band_the_taxonomy_declares_no_sub_for_predicts_undeclared(monkeypatch):
    """The plan files such a track nowhere, so the prediction must say so too."""
    monkeypatch.setattr(plan_engine, "_sub_for", lambda *_args: None)
    place = plan_engine.predicted_place(DECLARED, "Deep House", 7, vox=False)
    assert place == plan_engine.Predicted(disposition=Disposition.UNDECLARED)


def test_an_entry_whose_vocal_is_not_added_reads_no_vocal_sub():
    """A vocal sub the plan will not write is not a place the landing predicted."""
    entry = plan_engine.PlanEntry(
        entry_id="e", content_id="9", recorded="One.flac", disposition=Disposition.ROUTE,
        category=next(iter(Readability)), genre="Deep House", tree=DECLARED.tree.id,
        bucket="deep_house", sub="mid", vocal=plan_engine.VOCAL_PRESENT, vocal_sub="vocal")
    assert plan_engine.Predicted.of(entry).vocal_sub == ""
    added = replace(entry, vocal=plan_engine.VOCAL_ADD)
    assert plan_engine.Predicted.of(added).vocal_sub == "vocal"


def test_the_census_a_landing_files_walks_only_the_rows_it_made(monkeypatch):
    """Scope names the landed ids; every other row stays out of the scan."""
    rows = (SimpleNamespace(content_id="1"), SimpleNamespace(content_id="2"))
    scanned: list[tuple] = []
    monkeypatch.setattr(apply_cli.collection, "read_collection", lambda _cfg, **_: rows)
    monkeypatch.setattr(apply_cli.collection, "prefix_rules", lambda _cfg: ())
    monkeypatch.setattr(
        apply_cli.scan, "scan_rows", lambda got, *_a, **_k: scanned.append(tuple(got)) or ())
    cfg = SimpleNamespace(library=SimpleNamespace(root="/library"))
    apply_cli.census(cfg, DECLARED, scope=frozenset({"2"}))
    apply_cli.census(cfg, DECLARED)
    assert [[row.content_id for row in got] for got in scanned] == [["2"], ["1", "2"]]
