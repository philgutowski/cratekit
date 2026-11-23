"""U157: a native landing marks the rows whose tempo moves with the dyn My Tag.

A file at or above the configured cut joins carrying ``dyn`` in the gated commit
and the warning counts both kinds; too little pulse lands steady, an older file
is counted unscored, and neither is tagged on a guess. D1 applies.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from cratekit.analysis import rekordbox_check
from cratekit.core import config, drift, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, native
from tests.test_intake_land_native import _asked, _execute, _land, _query, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_land_vox_native import (
    _add_rows,
    _added,
    _content_id,
    _my_tag,
    _plan,
    _refused_at_the_commit,
)

#: A category of the person's own, which the writer copies the Analysis category's shape from.
MOOD_ID = "8000"
#: The Analysis category and a dyn value inside it, for the tests that seed them.
ANALYSIS_ID = "9100"
DYN_ID = "9101"


def _read(cfg: config.Config, silence: Path, name: str, level: str | None, verdict: str | None):
    """A staged file carrying this drift reading, or none at all."""
    path = _stage(cfg, silence, name)
    fields = {"driftlevel": level, "drift": verdict}
    if any(value is not None for value in fields.values()):
        assert tags.write_tags(path, fields)
    return path


def _marked(cfg: config.Config) -> frozenset[str]:
    """What ``crate analyze check`` reads as marked dyn, through its own reader."""
    db = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        return rekordbox_check.dyn_marked(db)
    finally:
        rb_writer.close_db(db)


@pytest.fixture
def writable(native_library):
    """The landing library, holding one category of the person's and no dyn tag."""
    cfg, _root = native_library
    _add_rows(cfg, _my_tag(MOOD_ID, "Mood", "root", "mood"))
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


# The drift against the cut
@pytest.mark.parametrize(
    ("level", "verdict", "planned", "tagged"),
    [
        ("4.4", drift.VARIABLE, drift.VARIABLE, True),
        ("1.5", drift.VARIABLE, drift.VARIABLE, True), ("1.4", drift.STEADY, drift.STEADY, False),
        ("0.0", drift.STEADY, drift.STEADY, False), (None, drift.UNKNOWN, drift.UNKNOWN, False),
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
    if tagged:
        assert _marked(cfg) == {content_id}
        # A soft deleted membership is no mark to the reader the check and the landing share.
        _execute(cfg, "UPDATE djmdSongMyTag SET rb_local_deleted = 1 WHERE ContentID = ?", content_id)
        assert _marked(cfg) == frozenset()


def test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection(
    writable, silence
):
    cfg = writable
    _read(cfg, silence, "Live.flac", "6.2", drift.VARIABLE)
    _read(cfg, silence, "Two.flac", "9.9", drift.VARIABLE)
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)
    _read(cfg, silence, "Ambient.flac", None, drift.UNKNOWN)
    _read(cfg, silence, "Older.flac", None, None)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    tagged = {_content_id(cfg, name) for name in ("Live.flac", "Two.flac")}
    assert _marked(cfg) == tagged
    categories = _query(cfg, "SELECT ID FROM djmdMyTag WHERE Name = ?", native.DYN_CATEGORY)
    values = _query(cfg, "SELECT ID, ParentID FROM djmdMyTag WHERE Name = ?", native.DYN_VALUE)
    assert len(categories) == 1 and len(values) == 1
    assert str(values[0][1]) == str(categories[0][0]), "the value is not inside the category"
    rows = _query(cfg, "SELECT ContentID FROM djmdSongMyTag WHERE MyTagID = ?", values[0][0])
    assert sorted(str(r[0]) for r in rows) == sorted(tagged)
    (record,) = session.records(cfg)
    assert {change.tree: change.created for change in record.change.trees}[native.DYN_CHANGE_KEY] == 2
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]
    message = _warning(acted, land_cli.AWAITING_ANALYSIS)
    dynamic = (
        f"first on the 2 row(s) carrying the dyn My Tag with {drift.DYNAMIC_SETTINGS} "
        "as the Normal run's"
    )
    normal = f"then last on the 3 row(s) without it with {drift.NORMAL_SETTINGS}"
    assert dynamic in message and normal in message, message
    # U954: the Dynamic run first and the Normal run last, so the mode the
    # next launch's Auto Analysis dialog reads is Normal.
    assert message.index(dynamic) < message.index(normal), message
    assert f"{normal}, so the mode the next launch reads is Normal" in message, message
    assert "Analysis Mode Normal, high precision off, BPM/Grid, Phrase and KEY on" in message
    assert "Analysis Mode Dynamic" in message
    # U319: both paths, the selections with Auto Analysis off and then the
    # one dialog with it on, before the clear that follows either.
    off = "rekordbox analyses nothing on its own with Auto Analysis off; open rekordbox, select the"
    assert off in message, message
    selections = message.index(normal)
    auto = message.index(f"; {land_cli.AUTO_ANALYSIS_STEP}; then crate inbox analyzed takes out")
    assert message.index(off) < selections < auto, message
    assert _shown(refused)["dyn My Tag"] == (
        "2 of 5 added row(s), each whose drift is at or above the cut 1.5 percent; "
        "1 file(s) carry no drift reading and get no tag"
    )
    assert acted["data"]["totals"]["dyn tagged"] == 2
def test_the_check_reads_the_value_the_landing_writes():
    """One constant and one reader, so the check and the landing cannot drift apart."""
    assert rekordbox_check.DYN_VALUE == native.DYN_VALUE == "dyn"
    assert rekordbox_check.dyn_marked is native.dyn_marked


# Never a guess
@pytest.mark.parametrize(("level", "verdict"), [(None, None), ("lots", drift.VARIABLE)])
def test_a_file_with_no_drift_reading_or_no_number_is_counted_unscored_and_untagged(
    writable, silence, level, verdict
):
    """A score that is not a number is unscored whatever its verdict says."""
    cfg = writable
    _read(cfg, silence, "Older.flac", level, verdict)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = _shown(refused)
    assert "1 file(s) carry no drift reading and get no tag" in shown["dyn My Tag"]
    item = _added_item(shown, "Older.flac")
    assert "dyn" not in item and "drift" not in item, "an unscored row is the fact line's"
    assert _marked(cfg) == frozenset()
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]
    assert "on the 1 row(s) without it" in _warning(acted, land_cli.AWAITING_ANALYSIS)
    assert "on the 0 row(s) carrying the dyn My Tag" in _warning(acted, land_cli.AWAITING_ANALYSIS)


def test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows(
    native_library, silence
):
    """The writer will not invent a category, so the batch lands untagged and the
    warning names each row to run with Dynamic."""
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


def test_a_library_with_no_category_and_no_variable_row_says_nothing_of_it(native_library, silence):
    """The writer is asked only when a row needs it, so a steady batch on a library
    with no My Tag at all lands with no dyn warning and no block."""
    cfg, _root = native_library
    _read(cfg, silence, "Straight.flac", "0.1", drift.STEADY)

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _shown(refused)["dyn My Tag"].startswith("0 of 1 added row(s)")
    assert _codes(acted) == [land_cli.AWAITING_ANALYSIS]


def test_a_tag_written_under_a_removed_value_is_said_and_never_counted(native_library, silence):
    """Over a removed dyn value the check's own read back counts no tag and names the row."""
    cfg, _root = native_library
    _add_rows(
        cfg, _my_tag(ANALYSIS_ID, native.DYN_CATEGORY, "root", "analysis-category", seq=1),
        _my_tag(DYN_ID, native.DYN_VALUE, ANALYSIS_ID, "dyn-value", removed=1),
    )
    _read(cfg, silence, "One.flac", "5.0", drift.VARIABLE)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert "dyn tagged" not in acted["data"]["totals"]
    (item,) = [i for i in acted["data"]["items"] if i.get("content_id")]
    assert item["dyn"] is False
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.DYN_NOT_WRITTEN]
    assert "One.flac" in warning["message"] and "removed" in warning["message"]
    assert "on the 0 row(s) carrying the dyn My Tag" in _warning(acted, land_cli.AWAITING_ANALYSIS)


def test_a_refused_commit_leaves_no_tag(writable, silence, monkeypatch):
    _read(writable, silence, "One.flac", "5.0", drift.VARIABLE)
    _refused_at_the_commit(writable, monkeypatch)


# What is approved
def test_the_digest_and_the_answer_move_with_a_rescore_and_with_the_cut(writable, silence):
    """The score is read against the cut configured now, and a rescore or a change
    of cut is another plan."""
    cfg = writable
    path = _read(cfg, silence, "One.flac", "0.4", drift.STEADY)
    first = _shown(_asked(_land()))
    assert tags.write_tags(path, {"driftlevel": "2.0", "drift": drift.VARIABLE})
    second = _shown(_asked(_land()))
    changed = dataclasses.replace(cfg, analysis=dataclasses.replace(cfg.analysis, drift_cut=3.0))
    config.save(changed)
    config.reset_cache()
    third = _shown(_asked(_land()))

    items = [_added_item(one, "One.flac") for one in (first, second, third)]
    assert [item["dyn"] for item in items] == [False, True, False]
    assert items[2]["drift_verdict"] == drift.STEADY
    assert len({first["digest"], second["digest"], third["digest"]}) == 3


def test_the_engine_digest_covers_each_rows_drift_verdict_and_answer():
    """At the engine, where the file's own fingerprint is not in the digest."""
    variable = {"drift": 4.0, "drift_verdict": drift.VARIABLE}
    every = [
        native.identity(_plan((_added("One.flac", **row),), drift_cut=cut, **blocked))
        for row, cut, blocked in (
            ({**variable, "dyn": True}, 1.5, {}), ({**variable, "dyn": False}, 1.5, {}),
            ({**variable, "drift": 4.1, "dyn": True}, 1.5, {}),
            ({"drift": None, "drift_verdict": drift.UNKNOWN}, 1.5, {}),
            ({"drift": None, "drift_verdict": drift.UNSCORED}, 1.5, {}),
            ({**variable, "dyn": True}, 2.0, {}),
            (variable, 1.5, {"dyn_blocked": native.DYN_NO_CATEGORY}),
        )
    ]
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
