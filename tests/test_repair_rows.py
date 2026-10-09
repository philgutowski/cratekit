"""``crate repair rows``: rekordbox's own defaults on a row that lacks them (R-923).

A row the native landing made before it set these columns would not load to a
deck. The repair fills each NULL default with rekordbox's value, through the
guarded writer, and touches nothing else. Every library here is disposable and
every row is written with plain SQL, so a NULL is a NULL and not a binding's
substitute.
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

from cratekit.core import config, preflight, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import row_defaults, row_defaults_cli
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

VERB = ["repair", "rows"]
GATE = row_defaults_cli.CONFIRM_GATE
DEFAULTS = rb_writer.CONTENT_ROW_DEFAULTS

#: Every column the repair may fill, as the live table stores it, as text.
WANTED = {column: str(value) for column, value in DEFAULTS.items()}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _field_policies():
    """The policy registry is process wide and the apply registers into it."""
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as ``tag rows`` patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set up machine with every module on and no acknowledgment yet."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(
        valid_data(
            root,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


@pytest.fixture
def acknowledged(machine) -> config.Config:
    session.record_acknowledgment(machine, terminal=lambda: True)
    return machine


def _sql(cfg: config.Config, statement: str, *params) -> list[tuple]:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        found = connection.execute(statement, params).fetchall()
        connection.commit()
        return found
    finally:
        connection.close()


def _content(cfg: config.Config) -> dict[str, dict]:
    """Every column of every content row, by identifier."""
    connection = sqlite3.connect(cfg.library.db_path)
    connection.row_factory = sqlite3.Row
    try:
        found = connection.execute("SELECT * FROM djmdContent").fetchall()
        return {str(row["ID"]): dict(row) for row in found}
    finally:
        connection.close()


def _whole(cfg: config.Config, content_id: str) -> None:
    """Give one row every default, as rekordbox would have made it."""
    sets = ", ".join(f"{column} = ?" for column in DEFAULTS)
    _sql(cfg, f"UPDATE djmdContent SET {sets} WHERE ID = ?", *DEFAULTS.values(), content_id)


def build(cfg: config.Config, *, landed=("101", "102"), whole=("201",), deleted=("301",)) -> Path:
    """A disposable library: rows a landing left bare, rows rekordbox made, tombstones.

    The two rows the disposable builder seeds are made whole, so a plan's items
    are exactly the rows named ``landed`` here.
    """
    db_path = Path(cfg.library.db_path)
    _build_disposable_database(db_path, with_tag_category=False)
    for content_id in ("1", "2"):
        _whole(cfg, content_id)
    for content_id in landed:
        _sql(
            cfg,
            "INSERT INTO djmdContent (ID, Title, FolderPath, BPM, rb_local_deleted, "
            "created_at, updated_at) VALUES (?, ?, ?, 0, 0, '2026-10-08', '2026-10-08')",
            content_id,
            f"landed {content_id}",
            str(Path(cfg.library.root) / "Music" / f"landed {content_id}.flac"),
        )
    for content_id in whole:
        _sql(
            cfg,
            "INSERT INTO djmdContent (ID, Title, BPM, rb_local_deleted, created_at, "
            "updated_at) VALUES (?, ?, 12400, 0, '2026-10-08', '2026-10-08')",
            content_id,
            f"made by rekordbox {content_id}",
        )
        _whole(cfg, content_id)
    for content_id in deleted:
        _sql(
            cfg,
            "INSERT INTO djmdContent (ID, Title, rb_local_deleted, created_at, updated_at) "
            "VALUES (?, ?, 1, '2026-10-08', '2026-10-08')",
            content_id,
            f"a tombstone {content_id}",
        )
    return db_path


def _planned(cfg: config.Config, path: Path | None = None) -> row_defaults.DefaultsPlan:
    db = rb_writer.open_db(path or cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_defaults.plan_rows(db)
    finally:
        rb_writer.close_db(db)


def _apply(cfg: config.Config, plan: row_defaults.DefaultsPlan) -> row_defaults.Written:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_defaults.apply_rows(cfg, db, plan, analysis_roots=[cfg.library.root])
    finally:
        rb_writer.close_db(db)


def _two_acts() -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *VERB])
    return code, acted, refused


def _as_text(row: dict) -> dict[str, str | None]:
    return {column: None if row[column] is None else str(row[column]) for column in DEFAULTS}


# ═══════════════════════════════════════════════════════════════════════════
# The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns(machine):
    build(machine)
    _sql(machine, "UPDATE djmdContent SET Rating = 3, Commnt = 'typed' WHERE ID = '102'")

    plan = _planned(machine)

    assert [item.content_id for item in plan.items] == ["101", "102"]
    by_id = {item.content_id: item for item in plan.items}
    assert by_id["101"].columns == row_defaults.COLUMNS
    assert by_id["102"].columns == tuple(
        column for column in row_defaults.COLUMNS if column not in ("Rating", "Commnt")
    )
    # Four live rows besides the two landed: the builder's two and one whole one.
    assert plan.rows == 5
    assert plan.fills == len(row_defaults.COLUMNS) * 2 - 2


def test_a_tombstone_is_never_listed_though_every_default_is_null(machine):
    build(machine, landed=(), deleted=("301", "302"))
    assert _planned(machine).items == ()


def test_the_digest_is_equal_on_a_copy_at_another_path(machine, tmp_path):
    """R-922's lesson: a rehearsal on a copy must be able to match the live plan."""
    live = build(machine)
    copy = tmp_path / "elsewhere" / "master.db"
    copy.parent.mkdir()
    shutil.copyfile(live, copy)

    assert _planned(machine).digest == _planned(machine, copy).digest


def test_the_digest_moves_when_a_planned_column_is_filled_elsewhere(machine):
    build(machine)
    before = _planned(machine).digest
    _sql(machine, "UPDATE djmdContent SET SamplerGain = 0.0 WHERE ID = '101'")
    assert _planned(machine).digest != before


# ═══════════════════════════════════════════════════════════════════════════
# The verb, end to end
# ═══════════════════════════════════════════════════════════════════════════


def test_the_two_acts_fill_every_null_default_and_move_no_other_column(acknowledged):
    build(acknowledged)
    _sql(acknowledged, "UPDATE djmdContent SET Rating = 3, Commnt = 'typed' WHERE ID = '102'")
    before = _content(acknowledged)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["count"] == 2
    assert acted["data"]["totals"]["written"] == 2
    assert acted["data"]["totals"]["read_back"] == 2
    after = _content(acknowledged)
    assert _as_text(after["101"]) == WANTED
    # A value present is never replaced: the rating and the comment a person set.
    assert after["102"]["Rating"] == 3 and after["102"]["Commnt"] == "typed"
    assert {k: v for k, v in _as_text(after["102"]).items() if k not in ("Rating", "Commnt")} == {
        k: v for k, v in WANTED.items() if k not in ("Rating", "Commnt")
    }
    # Nothing else on the written rows moved, and no other row moved at all.
    for content_id in ("101", "102"):
        moved = {
            column
            for column, value in after[content_id].items()
            if column not in DEFAULTS
            and column not in rb_writer.BOOKKEEPING_COLUMNS
            and value != before[content_id][column]
        }
        assert moved == set(), (content_id, moved)
    for content_id in ("1", "2", "201", "301"):
        assert after[content_id] == before[content_id], content_id
    codes = [warning["code"] for warning in acted["warnings"]]
    assert row_defaults_cli.DEFAULTS_WRITTEN in codes
    # The policy the apply registered is gone again: no later writer in this
    # process gains a column by it.
    assert rb_writer.ROW_DEFAULTS_POLICY.owner not in rb_writer.registered_field_policies()
    assert rb_writer.content_writable_columns() == {"ColorID"}


def test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing(acknowledged):
    build(acknowledged, landed=())
    before = _content(acknowledged)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["count"] == 0
    assert acted["outcome"] == "no_op"
    assert [warning["code"] for warning in acted["warnings"]] == [
        row_defaults_cli.NOTHING_TO_WRITE
    ]
    assert _content(acknowledged) == before


def test_the_gate_takes_no_inline_answer(acknowledged):
    build(acknowledged)
    code, envelope = drive(["-d", f"{GATE}=apply", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert _as_text(_content(acknowledged)["101"]) == dict.fromkeys(DEFAULTS)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    build(machine)
    code, envelope = drive(VERB)
    assert code != int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"].get("gate") != GATE


def test_an_abort_writes_nothing(acknowledged):
    build(acknowledged)
    before = _content(acknowledged)
    _code, refused = drive(VERB)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _content(acknowledged) == before


# ═══════════════════════════════════════════════════════════════════════════
# The engine's refusals
# ═══════════════════════════════════════════════════════════════════════════


def test_a_planned_column_set_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    build(acknowledged)
    plan = _planned(acknowledged)
    _sql(acknowledged, "UPDATE djmdContent SET ColorID = '3' WHERE ID = '102'")
    before = _content(acknowledged)

    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)

    assert caught.value.cause.reason == "decision-stale"
    assert "102" in caught.value.cause.message and "ColorID" in caught.value.cause.message
    assert _content(acknowledged) == before


def test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    build(acknowledged)
    plan = _planned(acknowledged)
    _sql(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '101'")
    before = _content(acknowledged)

    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)

    assert caught.value.cause.reason == "decision-stale"
    assert "101: no longer a live row" in caught.value.cause.message
    assert _content(acknowledged) == before


def test_rekordbox_running_refuses_at_the_apply_and_writes_nothing(acknowledged, monkeypatch):
    build(acknowledged)
    before = _content(acknowledged)
    _code, refused = drive(VERB)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, acted = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "rekordbox-running"
    assert session.records(acknowledged) == ()
    assert _content(acknowledged) == before


def test_the_guard_refuses_a_default_column_written_without_the_policy(acknowledged):
    """The policy is what admits these columns: written bare, the guard refuses."""
    build(acknowledged)
    from pyrekordbox.db6 import tables

    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        row = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID == "101").one()
        row.SamplerGain = 0.0
        with pytest.raises(Exception) as caught:
            rb_writer.commit_guarded(db)
        assert "SamplerGain" in str(caught.value)
    finally:
        rb_writer.close_db(db)
    assert _content(acknowledged)["101"]["SamplerGain"] is None


def test_the_policy_is_registered_by_the_apply_and_not_at_baseline():
    assert rb_writer.ROW_DEFAULTS_POLICY.owner not in rb_writer.registered_field_policies()
    assert not set(DEFAULTS) & rb_writer.content_writable_columns() - {"ColorID"}


def test_the_twenty_one_defaults_are_the_values_measured_on_the_live_library():
    """Pinned as literals, so the table cannot drift under tests that read it."""
    assert dict(rb_writer.CONTENT_ROW_DEFAULTS) == {
        "Rating": 0,
        "ColorID": "0",
        "DJPlayCount": 0,
        "DiscNo": 0,
        "DeliveryControl": "on",
        "SamplerTrackInfo": 0,
        "SamplerPlayOffset": 0,
        "SamplerGain": 0.0,
        "VideoAssociate": "0",
        "LyricStatus": 0,
        "ServiceID": 0,
        "ExtInfo": "null",
        "FileNameS": "",
        "Commnt": "",
        "Subtitle": "",
        "ReleaseDate": "",
        "ModifiedByRBM": "",
        "DeliveryComment": "",
        "Lyricist": "",
        "OrgFolderPath": "",
        "Reserved1": "",
    }
    # 0 == 0.0 to a dict, so the one float is held to its type by name.
    assert isinstance(rb_writer.CONTENT_ROW_DEFAULTS["SamplerGain"], float)
    assert all(
        isinstance(value, int) and not isinstance(value, bool)
        for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()
        if column in ("Rating", "DJPlayCount", "DiscNo", "SamplerTrackInfo",
                      "SamplerPlayOffset", "LyricStatus", "ServiceID")
    )


def test_every_default_is_a_real_column_and_none_is_an_analysis_column():
    from pyrekordbox.db6 import tables

    real = set(tables.DjmdContent.__table__.columns.keys())
    assert set(DEFAULTS) <= real
    assert not set(DEFAULTS) & rb_writer.CONTENT_ROW_EMPTY_COLUMNS
    assert rb_writer.ROW_DEFAULTS_POLICY.fields.keys() == DEFAULTS.keys()
    assert set(rb_writer.ROW_DEFAULTS_POLICY.fields.values()) == {
        rb_writer.Ownership.FILL_IF_EMPTY
    }


# ═══════════════════════════════════════════════════════════════════════════
# The read back, pure
# ═══════════════════════════════════════════════════════════════════════════


def _item(content_id: str = "101", columns=("SamplerGain", "DJPlayCount")) -> row_defaults.Item:
    return row_defaults.Item(content_id=content_id, title="t", path="p", columns=tuple(columns))


def test_judge_accepts_a_default_read_back_as_the_live_tables_integer():
    plan = row_defaults.DefaultsPlan(items=(_item(),), rows=1)
    before = {"101": {"SamplerGain": None, "DJPlayCount": None, "BPM": 0}}
    after = {"101": {"SamplerGain": 0.0, "DJPlayCount": 0, "BPM": 0}}
    assert row_defaults.judge(plan, before, after) == ((), ())


def test_judge_names_a_planned_column_still_null_and_a_column_that_moved():
    plan = row_defaults.DefaultsPlan(items=(_item(),), rows=1)
    before = {"101": {"SamplerGain": None, "DJPlayCount": None, "BPM": 0, "usn": 1}}
    after = {"101": {"SamplerGain": None, "DJPlayCount": "0", "BPM": 12400, "usn": 2}}
    wrong, moved = row_defaults.judge(plan, before, after)
    assert wrong == ("101: SamplerGain not as the default",)
    assert moved == ("101: BPM",)


def test_assert_read_back_refuses_a_moved_column_as_the_guards_defect():
    written = row_defaults.Written(session_id="s", written=1, read_back=1, moved=("101: BPM",))
    with pytest.raises(CratekitError) as caught:
        row_defaults.assert_read_back(written)
    assert caught.value.cause.reason == "whitelist-violation"
    assert "restore session s" in " ".join(caught.value.cause.remediation.steps)


def test_assert_read_back_refuses_a_wrong_value():
    written = row_defaults.Written(
        session_id="s", written=1, read_back=0, wrong=("101: SamplerGain not as the default",)
    )
    with pytest.raises(CratekitError) as caught:
        row_defaults.assert_read_back(written)
    assert caught.value.cause.reason == "internal-error"

