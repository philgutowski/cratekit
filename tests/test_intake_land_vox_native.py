"""U127: every native landing writes the vox My Tag from the file's score.

R-841's decision, driven through the real dispatcher against the disposable
database the native landing suite builds: the tag owns the vocal sub, so a row
whose file's ``voxlevel`` is at or above the calibrated cut joins the
collection carrying the vox My Tag, in the same gated commit, and the reader
adoption files the vocal sub from answers it. A file with no score is named and
never tagged on a guess, a library with no calibration tags nothing and says
why, and a tag already on a row is never taken off.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from cratekit.adopt import placements as adopt_placements
from cratekit.core import config, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, native
from cratekit.write import metadata_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import _land, _music, _query, _stage, _two_acts
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


def _seed_vocals(cfg: config.Config, *tagged: str) -> None:
    """The Vocals category and its vox value, and these rows carrying the tag."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        if db_session.get(tables.DjmdMyTag, CATEGORY_ID) is None:
            db_session.add(
                _row(
                    tables.DjmdMyTag,
                    ID=CATEGORY_ID,
                    Name=metadata_cli.CATEGORY,
                    Attribute=1,
                    ParentID="root",
                    Seq=0,
                    UUID="vocals-category",
                    rb_local_deleted=0,
                )
            )
            db_session.add(
                _row(
                    tables.DjmdMyTag,
                    ID=VOX_ID,
                    Name=metadata_cli.VALUE_VOX,
                    Attribute=0,
                    ParentID=CATEGORY_ID,
                    Seq=0,
                    UUID="vox-value",
                    rb_local_deleted=0,
                )
            )
        for content_id in tagged:
            db_session.add(
                _row(
                    tables.DjmdSongMyTag,
                    ID=f"vox-{content_id}",
                    MyTagID=VOX_ID,
                    ContentID=content_id,
                    TrackNo=0,
                    UUID=f"vox-{content_id}",
                    rb_local_deleted=0,
                )
            )
        db_session.commit()
    engine.dispose()


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


@pytest.fixture
def calibrated(native_library):
    """The cut over library, calibrated, holding the Vocals category and nothing tagged."""
    cfg, _root = native_library
    _calibrate(cfg)
    _seed_vocals(cfg)
    return cfg


# ---------------------------------------------------------------------------
# The score against the cut
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("voxlevel", "tagged"),
    [(60, True), (5, True), (4, False), (0, False)],
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


def test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses(calibrated, silence):
    """The writer is the vocals verb's, so the association hangs on the one
    vox value the library already holds rather than a second one beside it,
    and the session record counts it under the verb's own key."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 30)
    _scored(cfg, silence, "Three.flac", 2)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    values = _query(cfg, "SELECT ID FROM djmdMyTag WHERE Name = ?", metadata_cli.VALUE_VOX)
    assert values == [(VOX_ID,)], "a second vox value was made beside the library's"
    rows = _query(cfg, "SELECT ContentID FROM djmdSongMyTag WHERE MyTagID = ?", VOX_ID)
    assert sorted(str(r[0]) for r in rows) == sorted(
        _content_id(cfg, name) for name in ("One.flac", "Two.flac")
    )
    (record,) = session.records(cfg)
    counts = {change.tree: change.created for change in record.change.trees}
    assert counts[metadata_cli.CHANGE_KEY] == 2
    assert acted["data"]["totals"]["vox tagged"] == 2


def test_a_library_with_another_category_only_gains_the_vocals_category(native_library, silence):
    """No Vocals category yet, and one the writer can copy a shape from: the
    landing makes it as the vocals verb would, and adoption reads the tag."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    cfg, _root = native_library
    _calibrate(cfg)
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdMyTag,
                ID="8000",
                Name="Mood",
                Attribute=1,
                ParentID="root",
                Seq=0,
                UUID="mood",
                rb_local_deleted=0,
            )
        )
        db_session.commit()
    engine.dispose()
    _scored(cfg, silence, "One.flac", 60)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _vox_tagged(cfg) == {_content_id(cfg, "One.flac")}


# ---------------------------------------------------------------------------
# Never a guess
# ---------------------------------------------------------------------------


def test_a_file_with_no_score_gets_no_tag_and_is_named(calibrated, silence):
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Unscored.flac", None)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert "1 file(s) carry no score" in shown["vox My Tag"]
    assert _vox_tagged(cfg) == {_content_id(cfg, "One.flac")}
    codes = [w["code"] for w in acted["warnings"]]
    assert codes == [land_cli.AWAITING_ANALYSIS, land_cli.VOX_UNSCORED]
    message = acted["warnings"][1]["message"]
    assert "Unscored.flac" in message and "One.flac" not in message


def test_a_library_with_no_calibration_tags_nothing_and_says_why(native_library, silence):
    """R-276's reading: no calibration is no cut, never the default one."""
    cfg, _root = native_library
    _seed_vocals(cfg)
    _scored(cfg, silence, "One.flac", 60)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert native.VOX_UNCALIBRATED in refused["cause"]["detail"]["shown"]["vox My Tag"]
    assert _vox_tagged(cfg) == frozenset()
    assert [w["code"] for w in acted["warnings"]] == [
        land_cli.AWAITING_ANALYSIS,
        land_cli.VOX_NOT_WRITTEN,
    ]
    assert native.VOX_UNCALIBRATED in acted["warnings"][1]["message"]
    assert "vox tagged" not in acted["data"]["totals"]


def test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch(
    native_library, silence
):
    """The writer refuses to invent a category's shape. Asked before the gate,
    so the batch lands and the screen says no tag is written, rather than the
    landing failing after its files moved."""
    cfg, _root = native_library
    _calibrate(cfg)
    _scored(cfg, silence, "One.flac", 60)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert native.VOX_NO_CATEGORY in refused["cause"]["detail"]["shown"]["vox My Tag"]
    assert acted["data"]["totals"]["added"] == 1
    assert _query(cfg, "SELECT COUNT(*) FROM djmdMyTag") == [(0,)]
    assert [w["code"] for w in acted["warnings"]][1:] == [land_cli.VOX_NOT_WRITTEN]


# ---------------------------------------------------------------------------
# Additive only
# ---------------------------------------------------------------------------


def test_a_hand_placed_tag_on_a_row_already_present_survives(calibrated, silence):
    """The landing tags only rows it adds and removes none: a row the
    collection held, tagged by hand, keeps its tag whatever its file scores."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 1)
    held = str(_music(cfg) / "Two.flac")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('held-2', 'held', ?, 0, '2026-01-01', '2026-01-01')",
        (held,),
    )
    conn.commit()
    conn.close()
    _seed_vocals(cfg, "held-2")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _vox_tagged(cfg) == {"held-2", _content_id(cfg, "One.flac")}
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongMyTag WHERE ContentID = 'held-2'") == [(1,)]


def test_a_refused_commit_leaves_no_tag(calibrated, silence, monkeypatch):
    """The tag is pending on the landing's handle with its rows, so a refusal
    at the commit rolls both back."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused

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


# ---------------------------------------------------------------------------
# What is approved
# ---------------------------------------------------------------------------


def test_the_digest_moves_when_a_tag_is_planned(calibrated, silence):
    """The same file, rescored across the cut, is another plan: an approval
    given for a row with no tag is not applied to one with a tag."""
    cfg = calibrated
    path = _scored(cfg, silence, "One.flac", 2)
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert tags.write_tags(path, {"voxlevel": "60"})
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second

    (one,) = first["cause"]["detail"]["shown"]["items"]
    (two,) = second["cause"]["detail"]["shown"]["items"]
    assert (one["vox"], two["vox"]) == (False, True)
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]


def test_the_digest_moves_with_the_cut(calibrated, silence):
    """A recalibration between two plans is another plan, even when the
    answer for this file is the same at both cuts."""
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    _calibrate(cfg, 6.0)
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]


def test_the_screen_counts_the_tagged_rows_against_the_cut(calibrated, silence):
    cfg = calibrated
    _scored(cfg, silence, "One.flac", 60)
    _scored(cfg, silence, "Two.flac", 1)
    code, refused = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["vox My Tag"] == (
        "1 of 2 added row(s), each whose voxlevel is at or above the cut 5"
    )
