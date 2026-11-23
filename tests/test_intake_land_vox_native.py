"""U127 (R-841): every native landing writes the vox My Tag from the file's score.

A row whose ``voxlevel`` is at or above the calibrated cut joins carrying the
tag in the same gated commit, read back by adoption's reader. An unscored file
is named and never tagged on a guess, no calibration tags nothing and says
why, and no tag on a row is taken off. D1 applies.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.adopt import placements as adopt_placements
from cratekit.core import config, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, native
from cratekit.write import metadata_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import (
    _asked,
    _execute,
    _hold,
    _land,
    _music,
    _query,
    _stage,
    _two_acts,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_rb_writer_db import _row

#: The with vox cut this library is calibrated at, the live library's own.
CUT = 5.0
#: The Vocals category and its vox value, as the vocals verb leaves them.
CATEGORY_ID = "9000"
VOX_ID = "9001"


def _calibrate(cfg: config.Config, threshold: float = CUT) -> None:
    """Record a with vox cut for this library, the way a calibration leaves one."""
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"threshold": threshold}), encoding="utf-8")


def _my_tag(tag_id: str, name: str, parent: str, uuid: str, *, removed: int = 0, seq: int = 0):
    """A djmdMyTag row: a category under ``root``, else a value under its category."""
    return ("DjmdMyTag", dict(ID=tag_id, Name=name, Attribute=1 if parent == "root" else 0,
                              ParentID=parent, Seq=seq, UUID=uuid, rb_local_deleted=removed))


def _add_rows(cfg: config.Config, *rows: tuple[str, dict]) -> None:
    """Add each (table class name, columns) row to the disposable library, skipping an ID it holds."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        for table, columns in rows:
            kind = getattr(tables, table)
            if db_session.get(kind, columns["ID"]) is None:
                db_session.add(_row(kind, **columns))
        db_session.commit()
    engine.dispose()


def _seed_vocals(cfg: config.Config, *tagged: str) -> None:
    """The Vocals category and its vox value, and these rows carrying the tag."""
    _add_rows(
        cfg,
        _my_tag(CATEGORY_ID, metadata_cli.CATEGORY, "root", "vocals-category"),
        _my_tag(VOX_ID, metadata_cli.VALUE_VOX, CATEGORY_ID, "vox-value"),
        *(
            ("DjmdSongMyTag", dict(ID=f"vox-{content_id}", MyTagID=VOX_ID, ContentID=content_id,
                                   TrackNo=0, UUID=f"vox-{content_id}", rb_local_deleted=0))
            for content_id in tagged
        ),
    )


def _scored(cfg: config.Config, silence: Path, name: str, voxlevel: int | None) -> Path:
    """A staged file carrying this score, or none at all."""
    path = _stage(cfg, silence, name)
    if voxlevel is not None:
        assert tags.write_tags(path, {"voxlevel": str(voxlevel)})
    return path


def _content_id(cfg: config.Config, name: str) -> str:
    ((content_id,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", str(_music(cfg) / name)
    )
    return str(content_id)


def _vox_tagged(cfg: config.Config) -> frozenset[str]:
    """What adoption reads to file a vocal sub, through adoption's own reader."""
    db = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        tagged = adopt_placements.vox_tagged(db)
    finally:
        rb_writer.close_db(db)
    return tagged or frozenset()


def _refused_at_the_commit(cfg: config.Config, monkeypatch) -> None:
    """A refusal at the commit rolls back the tag pending on the landing's handle with its rows."""
    refused = _asked(_land())

    def refuse_commit(db, **_kwargs):
        raise rb_writer.RekordboxUnavailable(
            rb_writer._cause("cloud-sync-active", "a probe refusal at the commit")
        )

    monkeypatch.setattr(rb_writer, "commit_guarded", refuse_commit)
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, land_cli.NATIVE_GATE, "apply", "--actor", "a"])
    assert decided == int(ExitCode.OK)
    code, acted = drive(["--run", run_id, *_land()])

    assert code != int(ExitCode.OK), acted
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongMyTag") == [(0,)]


@pytest.fixture
def calibrated(native_library):
    """The cut over library, calibrated, holding the Vocals category and nothing tagged."""
    cfg, _root = native_library
    _calibrate(cfg)
    _seed_vocals(cfg)
    return cfg


# The score against the cut
@pytest.mark.parametrize(
    ("voxlevel", "tagged"), [(60, True), (5, True), (4, False), (0, False)],
    ids=["above", "exactly-at-the-cut", "below", "zero"],
)
def test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut(
    calibrated, silence, voxlevel, tagged
):
    cfg = calibrated
    _scored(cfg, silence, "One.flac", voxlevel)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    (item,) = [i for i in shown["items"] if i["action"] == native.ADD]
    assert item["voxlevel"] == voxlevel and item["vox"] is tagged
    content_id = _content_id(cfg, "One.flac")
    # What adoption reads: a tagged row is filed under its bucket's with vox.
    assert (content_id in _vox_tagged(cfg)) is tagged
    (landed,) = [i for i in acted["data"]["items"] if i.get("content_id") == content_id]
    assert landed["vox"] is tagged, "the report's read back disagrees with the table"
    assert acted["data"]["totals"].get("vox tagged", 0) == int(tagged)
    # A scored file, tagged or not, is not a warning.
    assert [w["code"] for w in acted["warnings"]] == [land_cli.AWAITING_ANALYSIS]


def test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named(
    calibrated, silence
):
    """The writer is the vocals verb's, so the association hangs on the one vox
    value the library holds, counted under the verb's own key; an unscored file
    gets no tag and is named."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 30)
    _scored(cfg, silence, "Three.flac", 2)
    _scored(cfg, silence, "Unscored.flac", None)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    values = _query(cfg, "SELECT ID FROM djmdMyTag WHERE Name = ?", metadata_cli.VALUE_VOX)
    assert values == [(VOX_ID,)], "a second vox value was made beside the library's"
    tagged = {_content_id(cfg, name) for name in ("One.flac", "Two.flac")}
    rows = _query(cfg, "SELECT ContentID FROM djmdSongMyTag WHERE MyTagID = ?", VOX_ID)
    assert sorted(str(r[0]) for r in rows) == sorted(tagged)
    assert _vox_tagged(cfg) == tagged
    (record,) = session.records(cfg)
    counts = {change.tree: change.created for change in record.change.trees}
    assert counts[metadata_cli.CHANGE_KEY] == 2
    assert acted["data"]["totals"]["vox tagged"] == 2
    assert "1 file(s) carry no score" in refused["cause"]["detail"]["shown"]["vox My Tag"]
    codes = [w["code"] for w in acted["warnings"]]
    assert codes == [land_cli.AWAITING_ANALYSIS, land_cli.VOX_UNSCORED]
    message = acted["warnings"][1]["message"]
    assert "Unscored.flac" in message and "One.flac" not in message


def test_a_library_with_another_category_only_gains_the_vocals_category(native_library, silence):
    """No Vocals category yet, and one the writer can copy a shape from: the
    landing makes it as the vocals verb would, and adoption reads the tag."""
    cfg, _root = native_library
    _calibrate(cfg)
    _add_rows(cfg, _my_tag("8000", "Mood", "root", "mood"))
    _scored(cfg, silence, "One.flac", 60)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _vox_tagged(cfg) == {_content_id(cfg, "One.flac")}


# Never a guess
def test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen(
    calibrated, silence
):
    """U181 (sitting 51's batch, which the plan said in one clause): more than half
    the added rows unscored is a warning with a code naming the way on. The bound
    is more than half: one in two is the line's alone."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", None)
    shown = _asked(_land())["cause"]["detail"]["shown"]
    assert "1 file(s) carry no score" in shown["vox My Tag"]
    assert "warnings" not in shown

    _scored(cfg, silence, "Three.flac", None)
    shown = _asked(_land())["cause"]["detail"]["shown"]

    assert "2 file(s) carry no score" in shown["vox My Tag"], "the line stays"
    (warned,) = shown["warnings"]
    assert warned["code"] == land_cli.VOX_MOSTLY_UNSCORED
    assert "2 of the 3 row(s)" in warned["message"]
    assert "crate analyze vocals --unscored" in warned["message"]
    assert "install.extras" in warned["message"]


def _uncalibrated(cfg: config.Config) -> str:
    """R-276's reading: no calibration is no cut, never the default one."""
    _seed_vocals(cfg)
    return native.VOX_UNCALIBRATED


def _no_category(cfg: config.Config) -> str:
    """The writer refuses to invent a category's shape, asked before the gate, so
    the batch lands saying no tag is written rather than failing after its moves."""
    _calibrate(cfg)
    return native.VOX_NO_CATEGORY


def _unreadable(cfg: config.Config) -> str:
    """The calibration refuses on every surface that reads it: the landing names
    that and lands its rows, rather than holding the batch over a tag."""
    _seed_vocals(cfg)
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    return "could not be read"


@pytest.mark.parametrize("blocked", [_uncalibrated, _no_category, _unreadable])
def test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch(
    native_library, silence, blocked
):
    cfg, _root = native_library
    said = blocked(cfg)
    categories = _query(cfg, "SELECT COUNT(*) FROM djmdMyTag")
    _scored(cfg, silence, "One.flac", 60)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert said in refused["cause"]["detail"]["shown"]["vox My Tag"]
    assert acted["data"]["totals"]["added"] == 1
    assert "vox tagged" not in acted["data"]["totals"]
    assert _vox_tagged(cfg) == frozenset()
    assert _query(cfg, "SELECT COUNT(*) FROM djmdMyTag") == categories, "a category was made"
    assert [w["code"] for w in acted["warnings"]] == [
        land_cli.AWAITING_ANALYSIS, land_cli.VOX_NOT_WRITTEN,
    ]
    assert said in acted["warnings"][1]["message"]
def test_a_tag_written_under_a_removed_category_is_said_and_never_counted(calibrated, silence):
    """The writer finds the category by name and reads no marker, so over a removed
    Vocals category it writes where nobody sees: the read back is adoption's own,
    so the report counts no tag and the warning names the row."""
    cfg = calibrated
    _execute(cfg, "UPDATE djmdMyTag SET rb_local_deleted = 1 WHERE ID = ?", CATEGORY_ID)
    _scored(cfg, silence, "One.flac", 60)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert "vox tagged" not in acted["data"]["totals"]
    (item,) = [i for i in acted["data"]["items"] if i.get("content_id")]
    assert item["vox"] is False
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.VOX_NOT_WRITTEN]
    assert "One.flac" in warning["message"] and "removed" in warning["message"]


# Additive only
def test_a_hand_placed_tag_on_a_row_already_present_survives(calibrated, silence):
    """The landing tags only rows it adds and removes none: a row the collection
    held, tagged by hand, keeps its tag whatever its file scores. Landed into
    again by its own name (U164), so the batch goes back to its filed folder."""
    cfg = calibrated
    _scored(cfg, silence, "Zero.flac", 1)
    code, first, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), first
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 1)
    _hold(cfg, "held-2", str(_music(cfg) / "Two.flac"))
    _seed_vocals(cfg, "held-2")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _vox_tagged(cfg) == {"held-2", _content_id(cfg, "One.flac")}
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongMyTag WHERE ContentID = 'held-2'") == [(1,)]


def test_a_refused_commit_leaves_no_tag(calibrated, silence, monkeypatch):
    _scored(calibrated, silence, "One.flac", 60)
    _refused_at_the_commit(calibrated, monkeypatch)


# What is approved
def test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut(
    calibrated, silence
):
    """The same file rescored across the cut is another plan, so an approval for
    a row with no tag is not applied to one with a tag; and a recalibration is
    another plan even when the answer for each file is the same at both cuts."""
    cfg = calibrated
    path = _scored(cfg, silence, "One.flac", 2)
    _scored(cfg, silence, "Two.flac", 1)
    first = _asked(_land())["cause"]["detail"]["shown"]
    assert tags.write_tags(path, {"voxlevel": "60"})
    second = _asked(_land())["cause"]["detail"]["shown"]
    _calibrate(cfg, 6.0)
    third = _asked(_land())["cause"]["detail"]["shown"]

    assert second["vox My Tag"] == "1 of 2 added row(s), each whose voxlevel is at or above the cut 5"
    target = str(_music(cfg) / "One.flac")
    vox = [{i["to"]: i["vox"] for i in one["items"]}[target] for one in (first, second, third)]
    assert vox == [False, True, True]
    assert len({first["digest"], second["digest"], third["digest"]}) == 3


def _plan(rows: tuple[native.RowPlan, ...], **fields) -> native.NativePlan:
    """A plan of these rows and nothing else, for the engine's pure answers."""
    return native.NativePlan(
        tree_id="intake", root_id="root", root_name="INBOX", playlist="batch", database=Path("/db"),
        device_id="d", master_db_id="1", base_drive=None, current_drive=None, rows=rows, link=None,
        digest="", **fields,
    )


def _added(name: str, **fields) -> native.RowPlan:
    return native.RowPlan(
        source=Path(f"/staging/{name}"), target=Path(f"/music/{name}"), action=native.ADD,
        title=name, folder_path=f"/music/{name}", file_name=name, file_size=1, file_type=1,
        content_link=None, **fields,
    )


def test_the_engine_digest_covers_each_rows_score_and_answer():
    """At the engine, where the file's own fingerprint is not in the digest: one
    file at one cut answered tagged or not is two plans, as are two scores."""
    cut = {"vox_cut": CUT}
    tagged = native.identity(_plan((_added("One.flac", voxlevel=60, vox=True),), **cut))
    untagged = native.identity(_plan((_added("One.flac", voxlevel=60, vox=False),), **cut))
    rescored = native.identity(_plan((_added("One.flac", voxlevel=61, vox=True),), **cut))
    assert tagged != untagged
    assert tagged != rescored


def test_a_blocked_plan_names_no_file_unscored():
    """No score was read at all when the tag is blocked, so no file is called
    unscored: the reason is the block, said once, not each file's."""
    rows = (_added("One.flac"), _added("Two.flac"))
    assert _plan(rows, vox_cut=CUT, vox_blocked=native.VOX_NO_CATEGORY).vox_unscored() == ()
    assert _plan(rows, vox_blocked=native.VOX_UNCALIBRATED).vox_unscored() == ()
    assert [row.target.name for row in _plan(rows, vox_cut=CUT).vox_unscored()] == [
        "One.flac", "Two.flac",
    ]
