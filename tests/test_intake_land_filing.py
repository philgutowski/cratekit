"""U165: a native landing files its batch into BY GENRE + ENERGY under the same answer.

The landing predicts, before its rows exist, where adoption will file each
one, shows and digests the prediction, and after the commit plans adoption
over the rows it made and files them when every one is as predicted. These
tests drive the real dispatcher over real FLAC containers against the
disposable database ``tests/test_intake_land_native.py`` builds, with the
routing tree cut over, and pin what the brief asks: five files, three with a
genre, one without and one vocal, filed with one answer and read back; a plan
after the commit that differs files nothing and says so; a rehearsal digests
as the live plan; ``--land-only`` and a tree on the bridge file nothing; and
a landing that adds nothing files nothing.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli
from cratekit.core import config, rb_writer, tags, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import filing, native
from cratekit.write.routing_pass import destination
from tests.cli_drive import drive
from tests.test_intake_land_native import DECLARED, _land, _music, _query, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_land_vox_native import _calibrate, _seed_vocals


@pytest.fixture
def filing_library(native_library):
    """The native intake library with its routing tree cut over too, so a landing files."""
    cfg, root_id = native_library
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        tree_root = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    tree_registry.record_cutover(
        cfg,
        DECLARED.tree.id,
        root_id=tree_root,
        on=date(2026, 10, 31),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    return cfg, root_id


def _file(cfg: config.Config, silence: Path, name: str, **fields: object) -> Path:
    path = _stage(cfg, silence, name)
    if fields:
        assert tags.write_tags(path, fields)
    return path


def _content_id(cfg: config.Config, name: str) -> str:
    ((content_id,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", str(_music(cfg) / name)
    )
    return str(content_id)


def _homes(cfg: config.Config, content_id: str) -> set[tuple[str, str]]:
    """Every (folder, playlist) under the routing tree that holds this row, by display name."""
    rows = _query(
        cfg,
        "SELECT folder.Name, playlist.Name FROM djmdSongPlaylist member "
        "JOIN djmdPlaylist playlist ON playlist.ID = member.PlaylistID "
        "JOIN djmdPlaylist folder ON folder.ID = playlist.ParentID "
        "JOIN djmdPlaylist tree ON tree.ID = folder.ParentID "
        "WHERE member.ContentID = ? AND tree.Name = ? AND member.rb_local_deleted = 0",
        content_id,
        DECLARED.tree.display,
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


# ---------------------------------------------------------------------------
# Five files, one answer, filed and read back
# ---------------------------------------------------------------------------


def test_five_files_land_and_file_under_one_answer(filing_library, silence):
    cfg, _root = filing_library
    _calibrate(cfg)
    _seed_vocals(cfg)
    _five(cfg, silence)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
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
        ("One.flac", "deep_house", 7),
        ("Two.flac", "techno", 8),
        ("Three.flac", "tech_house", None),
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


def test_the_filed_rows_are_what_adopt_apply_then_finds_nothing_to_do_for(
    filing_library, silence
):
    cfg, _root = filing_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    from cratekit.adopt import apply as apply_engine
    from cratekit.adopt import collection

    collection.reset_cache()
    plan = apply_cli.current_plan(
        cfg, DECLARED, scope=frozenset({_content_id(cfg, "One.flac")})
    )
    assert apply_engine.outstanding(plan, apply_engine.read(cfg)) == ()


# ---------------------------------------------------------------------------
# A plan after the commit that differs files nothing, and the landing stands
# ---------------------------------------------------------------------------


def test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so(
    filing_library, silence, monkeypatch
):
    cfg, _root = filing_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    real = apply_cli.current_plan

    def moved(cfg, declared, **kwargs):
        # THE TREE MOVED BETWEEN THE ANSWER AND THE FILING: every sub reads
        # another, which is what a retagged energy or a redeclared band does.
        plan = real(cfg, declared, **kwargs)
        return replace(
            plan, entries=tuple(replace(entry, sub="elsewhere") for entry in plan.entries)
        )

    monkeypatch.setattr(filing.apply_cli, "current_plan", moved)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    (warning,) = [
        one for one in acted["warnings"] if one["code"] == filing.FILED_DIFFERENTLY_WARNING
    ]
    assert "One.flac" in warning["message"] and filing.ADOPT_APPLY in warning["message"]
    assert acted["data"]["totals"]["filing"] == filing.FILED_DIFFERENTLY
    assert acted["data"]["totals"]["added"] == 1
    assert _homes(cfg, _content_id(cfg, "One.flac")) == set()


# ---------------------------------------------------------------------------
# What files nothing
# ---------------------------------------------------------------------------


def test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files(
    filing_library, silence
):
    cfg, _root = filing_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    _code, filed = drive(_land())
    code, acted, refused = _two_acts(_land("--land-only"))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["files after landing"] == "nothing, asked with --land-only"
    assert "files into" not in shown["items"][0]
    assert shown["digest"] != filed["cause"]["detail"]["shown"]["digest"]
    assert "filing" not in acted["data"]["totals"]
    assert _homes(cfg, _content_id(cfg, "One.flac")) == set()


def test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it(
    native_library, silence
):
    cfg, _root = native_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    fact = refused["cause"]["detail"]["shown"]["files after landing"]
    assert fact.startswith("nothing, ") and "xml bridge" in fact
    assert f"crate tree cutover {DECLARED.tree.id}" in fact
    assert "filing" not in acted["data"]["totals"]


def test_a_landing_that_adds_no_row_files_nothing():
    landed = native.NativeLanded(
        tree_id="t",
        playlist="p",
        playlist_id="",
        added=(),
        present=(),
        memberships_added=0,
        session_id="s",
    )
    predicted = (
        filing.Prediction(
            target=Path("/nowhere/One.flac"),
            place=filing.plan_engine.predicted_place(DECLARED, "Deep House", 7, vox=False),
        ),
    )
    found = filing.file_landed(None, DECLARED, predicted, landed, actor="session")
    assert found.state == filing.NOTHING_TO_FILE


# ---------------------------------------------------------------------------
# The rehearsal digests as the live plan, prediction and all
# ---------------------------------------------------------------------------


def test_a_rehearsal_digests_as_the_live_landing_that_files(filing_library, silence):
    cfg, _root = filing_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    _file(cfg, silence, "Two.flac")
    code, rehearsed = drive(_land("--rehearse"))
    assert code == int(ExitCode.OK), rehearsed

    code, live = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), live
    shown = live["cause"]["detail"]["shown"]
    assert shown["digest"] == rehearsed["data"]["digest"]
    assert "equal to this plan's" in shown["rehearsal"]
    assert all("files into" in item for item in shown["items"])


def test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows(
    filing_library, silence
):
    """The collection cache may hold the library as it was before the landing;
    the filing forgets it first, or it plans the new rows as absent."""
    from cratekit.adopt import collection
    from tests.test_intake_land_native import GATE

    cfg, _root = filing_library
    _file(cfg, silence, "One.flac", genre="Deep House", energylevel=7)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    collection.reset_cache()
    collection.read_collection(cfg)

    code, acted = drive(["--run", run_id, *_land()])

    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["filing"] == filing.FILED
    assert _homes(cfg, _content_id(cfg, "One.flac")) != set()
