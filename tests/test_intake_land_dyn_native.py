"""U157: a native landing marks the rows whose tempo moves with the dyn My Tag.

Driven through the real dispatcher against the disposable database the native
landing suite builds. A file whose drift, the tag ``analyze run`` writes, is at
or above the configured cut joins the collection carrying the ``dyn`` My Tag in
the same gated commit, so the person running Analyze Tracks selects those rows
for Dynamic and every other for Normal; the warning names both selections and
counts each. A file with too little pulse to judge reads unknown and lands as
steady, a file analysed before this unit reads unscored and is counted, and
neither is tagged on a guess. ``crate analyze check`` reads the mark with the
landing's own reader.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import dataclasses
import sqlite3
from pathlib import Path

import pytest

from cratekit.analysis import rekordbox_check
from cratekit.core import config, drift, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, native
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

#: A category any library holds once a person made one My Tag, which the writer
#: copies the Analysis category's shape from.
MOOD_ID = "8000"
#: The Analysis category and a dyn value inside it, for the tests that seed them.
ANALYSIS_ID = "9100"
DYN_ID = "9101"


def _seed_category(cfg: config.Config) -> None:
    """One My Tag category of the person's own, so the writer has a shape to copy."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdMyTag,
                ID=MOOD_ID,
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


def _seed_removed_dyn(cfg: config.Config) -> None:
    """The Analysis category holding a dyn value rekordbox removed."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdMyTag,
                ID=ANALYSIS_ID,
                Name=native.DYN_CATEGORY,
                Attribute=1,
                ParentID="root",
                Seq=1,
                UUID="analysis-category",
                rb_local_deleted=0,
            )
        )
        db_session.add(
            _row(
                tables.DjmdMyTag,
                ID=DYN_ID,
                Name=native.DYN_VALUE,
                Attribute=0,
                ParentID=ANALYSIS_ID,
                Seq=0,
                UUID="dyn-value",
                rb_local_deleted=1,
            )
        )
        db_session.commit()
    engine.dispose()


def _read(cfg: config.Config, silence: Path, name: str, level: str | None, verdict: str | None):
    """A staged file carrying this drift reading, or none at all."""
    path = _stage(cfg, silence, name)
    fields = {"driftlevel": level, "drift": verdict}
    if any(value is not None for value in fields.values()):
        assert tags.write_tags(path, fields)
    return path


def _content_id(cfg: config.Config, name: str) -> str:
    ((content_id,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", str(_music(cfg) / name)
    )
    return str(content_id)


def _marked(cfg: config.Config) -> frozenset[str]:
    """What ``crate analyze check`` reads as marked dyn, through its own reader."""
    db = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        return rekordbox_check.dyn_marked(db)
    finally:
        rb_writer.close_db(db)


def _with_cut(cfg: config.Config, cut: float) -> config.Config:
    changed = dataclasses.replace(cfg, analysis=dataclasses.replace(cfg.analysis, drift_cut=cut))
    config.save(changed)
    config.reset_cache()
    return changed


@pytest.fixture
def writable(native_library):
    """The landing library, holding one category of the person's and no dyn tag."""
    cfg, _root = native_library
    _seed_category(cfg)
    return cfg


def _codes(acted: dict) -> list[str]:
    """The warnings this unit owns or shares, without the vox tag's, which an
    uncalibrated library raises on every landing and U127 tests."""
    vox = {land_cli.VOX_NOT_WRITTEN, land_cli.VOX_UNSCORED}
    return [w["code"] for w in acted["warnings"] if w["code"] not in vox]


def _warning(acted: dict, code: str) -> str:
    (message,) = [w["message"] for w in acted["warnings"] if w["code"] == code]
    return message


def _shown(refused: dict) -> dict:
    return refused["cause"]["detail"]["shown"]


def _added_item(shown: dict, name: str) -> dict:
    (item,) = [i for i in shown["items"] if i["action"] == native.ADD and i["to"].endswith(name)]
    return item


# ---------------------------------------------------------------------------
# The drift against the cut
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("level", "verdict", "planned", "tagged"),
    [
        ("4.4", drift.VARIABLE, drift.VARIABLE, True),
        ("1.5", drift.VARIABLE, drift.VARIABLE, True),
        ("1.4", drift.STEADY, drift.STEADY, False),
        ("0.0", drift.STEADY, drift.STEADY, False),
        (None, drift.UNKNOWN, drift.UNKNOWN, False),
    ],
    ids=["moving", "exactly-at-the-cut", "below", "still", "too-little-pulse"],
)
def test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable(
    writable, silence, level, verdict, planned, tagged
):
    cfg = writable
    assert cfg.analysis.drift_cut == config.DEFAULT_DRIFT_CUT == 1.5
    _read(cfg, silence, "One.flac", level, verdict)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    item = _added_item(_shown(refused), "One.flac")
    assert item["drift_verdict"] == planned and item["dyn"] is tagged
    assert item["drift"] == (None if level is None else float(level))
    content_id = _content_id(cfg, "One.flac")
    assert (content_id in _marked(cfg)) is tagged, "the check reads another answer"
    (landed,) = [i for i in acted["data"]["items"] if i.get("content_id") == content_id]
    assert landed["dyn"] is tagged, "the report's read back disagrees with the table"
    assert acted["data"]["totals"].get("dyn tagged", 0) == int(tagged)
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]


def test_the_warning_names_both_selections_and_counts_each(writable, silence):
    cfg = writable
    _read(cfg, silence, "Live.flac", "6.2", drift.VARIABLE)
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)
    _read(cfg, silence, "Ambient.flac", None, drift.UNKNOWN)
    _read(cfg, silence, "Older.flac", None, None)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _marked(cfg) == {_content_id(cfg, "Live.flac")}
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]
    message = _warning(acted, land_cli.AWAITING_ANALYSIS)
    assert (
        f"on the 3 row(s) without the dyn My Tag with {drift.NORMAL_SETTINGS}" in message
    ), message
    assert f"on the 1 row(s) carrying it with {drift.DYNAMIC_SETTINGS}" in message, message
    assert "Analysis Mode Normal, high precision off, BPM/Grid, Phrase and KEY on" in message
    assert "Analysis Mode Dynamic" in message
    assert _shown(refused)["dyn My Tag"] == (
        "1 of 4 added row(s), each whose drift is at or above the cut 1.5 percent; "
        "1 file(s) carry no drift reading and get no tag"
    )
    assert acted["data"]["totals"]["dyn tagged"] == 1


def test_the_tag_is_written_under_one_value_and_counted_on_the_session(writable, silence):
    cfg = writable
    _read(cfg, silence, "One.flac", "3.0", drift.VARIABLE)
    _read(cfg, silence, "Two.flac", "9.9", drift.VARIABLE)
    _read(cfg, silence, "Three.flac", "0.2", drift.STEADY)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    categories = _query(cfg, "SELECT ID FROM djmdMyTag WHERE Name = ?", native.DYN_CATEGORY)
    values = _query(cfg, "SELECT ID, ParentID FROM djmdMyTag WHERE Name = ?", native.DYN_VALUE)
    assert len(categories) == 1 and len(values) == 1
    assert str(values[0][1]) == str(categories[0][0]), "the value is not inside the category"
    rows = _query(cfg, "SELECT ContentID FROM djmdSongMyTag WHERE MyTagID = ?", values[0][0])
    assert sorted(str(r[0]) for r in rows) == sorted(
        _content_id(cfg, name) for name in ("One.flac", "Two.flac")
    )
    (record,) = session.records(cfg)
    counts = {change.tree: change.created for change in record.change.trees}
    assert counts[native.DYN_CHANGE_KEY] == 2


def test_the_check_reads_the_value_the_landing_writes():
    """One constant and one reader, so the check and the landing cannot drift apart."""
    assert rekordbox_check.DYN_VALUE == native.DYN_VALUE == "dyn"
    assert rekordbox_check.dyn_marked is native.dyn_marked


# ---------------------------------------------------------------------------
# Never a guess
# ---------------------------------------------------------------------------


def test_a_file_with_no_drift_reading_is_counted_unscored_and_untagged(writable, silence):
    cfg = writable
    _read(cfg, silence, "Older.flac", None, None)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = _shown(refused)
    assert "1 file(s) carry no drift reading and get no tag" in shown["dyn My Tag"]
    item = _added_item(shown, "Older.flac")
    assert "dyn" not in item and "drift" not in item, "an unscored row is the fact line's"
    assert _marked(cfg) == frozenset()
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]
    assert "on the 1 row(s) without the dyn My Tag" in _warning(acted, land_cli.AWAITING_ANALYSIS)
    assert "on the 0 row(s) carrying it" in _warning(acted, land_cli.AWAITING_ANALYSIS)


def test_a_score_that_is_not_a_number_is_unscored_whatever_its_verdict_says(writable, silence):
    cfg = writable
    _read(cfg, silence, "One.flac", "lots", drift.VARIABLE)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert "1 file(s) carry no drift reading" in _shown(refused)["dyn My Tag"]
    assert _marked(cfg) == frozenset()


def test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows(
    native_library, silence
):
    """The writer refuses to invent a category's shape. Asked before the gate,
    so the batch lands, the screen says no tag is written, and the warning
    names each row the person must still run with Dynamic."""
    cfg, _root = native_library
    _read(cfg, silence, "Live.flac", "5.0", drift.VARIABLE)
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert native.DYN_NO_CATEGORY in _shown(refused)["dyn My Tag"]
    assert _added_item(_shown(refused), "Live.flac")["dyn"] is False
    assert acted["data"]["totals"]["added"] == 2
    assert _query(cfg, "SELECT COUNT(*) FROM djmdMyTag") == [(0,)]
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS, land_cli.DYN_NOT_WRITTEN]
    message = _warning(acted, land_cli.DYN_NOT_WRITTEN)
    assert "Live.flac" in message and "Straight.flac" not in message
    assert drift.DYNAMIC_SETTINGS in message and native.DYN_NO_CATEGORY in message


def test_a_library_with_no_category_and_no_variable_row_says_nothing_of_it(
    native_library, silence
):
    """The writer is asked only when a row needs it, so a steady batch on a
    library with no My Tag at all lands with no dyn warning and no block."""
    cfg, _root = native_library
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _shown(refused)["dyn My Tag"].startswith("0 of 1 added row(s)")
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]


def test_a_tag_written_under_a_removed_value_is_said_and_never_counted(native_library, silence):
    """The writer finds the value by name and reads no marker, so over a dyn
    value rekordbox removed it writes where the check does not read. The read
    back is the check's own, so the report counts no tag and the warning names
    the row, rather than calling it tagged."""
    cfg, _root = native_library
    _seed_removed_dyn(cfg)
    _read(cfg, silence, "One.flac", "5.0", drift.VARIABLE)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert "dyn tagged" not in acted["data"]["totals"]
    (item,) = [i for i in acted["data"]["items"] if i.get("content_id")]
    assert item["dyn"] is False
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.DYN_NOT_WRITTEN]
    assert "One.flac" in warning["message"] and "removed" in warning["message"]
    assert "on the 0 row(s) carrying it" in _warning(acted, land_cli.AWAITING_ANALYSIS)


def test_a_refused_commit_leaves_no_tag(writable, silence, monkeypatch):
    """The tag is pending on the landing's handle with its rows, so a refusal
    at the commit rolls both back."""
    cfg = writable
    _read(cfg, silence, "One.flac", "5.0", drift.VARIABLE)
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


def test_the_digest_moves_when_a_file_is_rescored_across_the_cut(writable, silence):
    cfg = writable
    path = _read(cfg, silence, "One.flac", "0.4", drift.STEADY)
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert tags.write_tags(path, {"driftlevel": "4.0", "drift": drift.VARIABLE})
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second

    assert (_added_item(_shown(first), "One.flac")["dyn"], _added_item(_shown(second), "One.flac")["dyn"]) == (
        False,
        True,
    )
    assert _shown(first)["digest"] != _shown(second)["digest"]


def test_the_digest_and_the_answer_move_with_the_cut(writable, silence):
    """The score is read against the cut configured now, not the verdict the
    analysis wrote beside it, so raising the cut lands the same file steady,
    and any change of cut is another plan."""
    cfg = writable
    _read(cfg, silence, "One.flac", "2.0", drift.VARIABLE)
    code, first = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    _with_cut(cfg, 3.0)
    code, second = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), second

    assert _added_item(_shown(first), "One.flac")["dyn"] is True
    assert _added_item(_shown(second), "One.flac")["drift_verdict"] == drift.STEADY
    assert _added_item(_shown(second), "One.flac")["dyn"] is False
    assert _shown(first)["digest"] != _shown(second)["digest"]


def _plan(rows: tuple[native.RowPlan, ...], **fields) -> native.NativePlan:
    """A plan of these rows and nothing else, for the engine's pure answers."""
    return native.NativePlan(
        tree_id="intake",
        root_id="root",
        root_name="INBOX",
        playlist="batch",
        database=Path("/db"),
        device_id="d",
        master_db_id="1",
        base_drive=None,
        current_drive=None,
        rows=rows,
        link=None,
        digest="",
        **fields,
    )


def _added(name: str, **fields) -> native.RowPlan:
    return native.RowPlan(
        source=Path(f"/staging/{name}"),
        target=Path(f"/music/{name}"),
        action=native.ADD,
        title=name,
        folder_path=f"/music/{name}",
        file_name=name,
        file_size=1,
        file_type=1,
        content_link=None,
        **fields,
    )


def test_the_engine_digest_covers_each_rows_drift_verdict_and_answer():
    """At the engine, where the file's own fingerprint is not in the digest."""
    cut = {"drift_cut": 1.5}
    tagged = native.identity(
        _plan((_added("One.flac", drift=4.0, drift_verdict=drift.VARIABLE, dyn=True),), **cut)
    )
    untagged = native.identity(
        _plan((_added("One.flac", drift=4.0, drift_verdict=drift.VARIABLE, dyn=False),), **cut)
    )
    rescored = native.identity(
        _plan((_added("One.flac", drift=4.1, drift_verdict=drift.VARIABLE, dyn=True),), **cut)
    )
    unknown = native.identity(
        _plan((_added("One.flac", drift=None, drift_verdict=drift.UNKNOWN),), **cut)
    )
    unscored = native.identity(
        _plan((_added("One.flac", drift=None, drift_verdict=drift.UNSCORED),), **cut)
    )
    recut = native.identity(
        _plan(
            (_added("One.flac", drift=4.0, drift_verdict=drift.VARIABLE, dyn=True),),
            drift_cut=2.0,
        )
    )
    blocked = native.identity(
        _plan(
            (_added("One.flac", drift=4.0, drift_verdict=drift.VARIABLE),),
            drift_cut=1.5,
            dyn_blocked=native.DYN_NO_CATEGORY,
        )
    )
    every = [tagged, untagged, rescored, unknown, unscored, recut, blocked]
    assert len({repr(one) for one in every}) == len(every)


def test_the_plan_counts_each_kind_of_row():
    rows = (
        _added("A.flac", drift=4.0, drift_verdict=drift.VARIABLE, dyn=True),
        _added("B.flac", drift=4.0, drift_verdict=drift.VARIABLE, dyn=False),
        _added("C.flac", drift=0.1, drift_verdict=drift.STEADY),
        _added("D.flac", drift_verdict=drift.UNKNOWN),
        _added("E.flac", drift_verdict=drift.UNSCORED),
    )
    plan = _plan(rows, drift_cut=1.5)
    assert [row.file_name for row in plan.dyn_tagged()] == ["A.flac"]
    assert [row.file_name for row in plan.drift_variable()] == ["A.flac", "B.flac"]
    assert [row.file_name for row in plan.drift_unscored()] == ["E.flac"]


def test_a_removed_membership_is_no_mark_to_the_shared_reader(writable, silence):
    """A soft deleted membership is no mark, so the reader the check and the
    landing share does not count a row rekordbox took the tag off."""
    cfg = writable
    _read(cfg, silence, "One.flac", "5.0", drift.VARIABLE)
    code, acted, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    content_id = _content_id(cfg, "One.flac")
    assert _marked(cfg) == {content_id}
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdSongMyTag SET rb_local_deleted = 1 WHERE ContentID = ?", (content_id,))
    conn.commit()
    conn.close()
    assert _marked(cfg) == frozenset()
