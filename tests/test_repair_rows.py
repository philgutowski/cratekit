"""``crate repair rows``: rekordbox's own defaults on a row that lacks them (R-923),
and its file's inode on a row the binding numbered at random (U115).

A row the native landing made before it set these columns would not load to a
deck, and neither does one whose ``rb_file_id`` the binding minted. The repair
fills each NULL default with rekordbox's value and gives a random file id the
file's inode, through the guarded writer, and touches nothing else. Every
library here is disposable and every row is written with plain SQL, so a NULL
is a NULL and not a binding's substitute.

THE BOUND IS FIXED HERE. The volume's inode bound is a fresh file's inode, and
on the boot volume these tests run on it is above the binding's whole range, so
every test would read undecidable. The autouse fixture pins it, one test
exercises the real measurement, and one the undecidable answer.
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
FILE_ID = rb_writer.FILE_ID_COLUMN

#: The volume's inode bound every test but one judges against.
BOUND = 2_000_000
#: What the binding would mint: above the bound, inside its 28 bit range.
RANDOM_ID = 200_000_000
#: An inode rekordbox wrote years ago for a file copied since: under the bound.
STALE_ID = 1_500_000

#: The real measurement, kept before the fixture below replaces it.
REAL_INODE_BOUND = row_defaults.inode_bound

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
def _bound(monkeypatch):
    """The inode bound, pinned under the binding's range so a random id is seen."""
    monkeypatch.setattr(row_defaults, "inode_bound", lambda cfg: BOUND)


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


def _file(cfg: config.Config, content_id: str) -> Path:
    """The file a seeded row names, created on disk so it has an inode."""
    path = Path(cfg.library.root) / "Music" / f"row {content_id}.flac"
    path.write_bytes(b"fLaC")
    return path


def _row(cfg: config.Config, content_id: str, title: str, *, path: str | None, file_id, bpm=0):
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, Title, FolderPath, BPM, rb_local_deleted, "
        f"{FILE_ID}, created_at, updated_at) VALUES (?, ?, ?, ?, 0, ?, '2026-10-08', '2026-10-08')",
        content_id,
        title,
        path,
        bpm,
        file_id,
    )


def build(
    cfg: config.Config,
    *,
    landed=("101", "102"),
    whole=("201",),
    deleted=("301",),
    stale=("401",),
    zero=("501",),
    missing=("601",),
) -> Path:
    """A disposable library: rows a landing left bare and numbered at random, rows
    rekordbox made, tombstones, and the rows the file id rule must leave alone.

    The two rows the disposable builder seeds are made whole and carry no file
    id, so a plan's items are exactly the rows named ``landed`` here: each bare
    in every default, carrying :data:`RANDOM_ID`, and naming a file on disk.
    ``stale`` rows carry an id under the bound that is not their file's inode,
    ``zero`` rows carry 0, ``missing`` rows carry a random id and name no file,
    and every one of those is left as it is.
    """
    db_path = Path(cfg.library.db_path)
    _build_disposable_database(db_path, with_tag_category=False)
    for content_id in ("1", "2"):
        _whole(cfg, content_id)
    for content_id in landed:
        _row(cfg, content_id, f"landed {content_id}", path=str(_file(cfg, content_id)), file_id=RANDOM_ID)
    for content_id in whole:
        _row(cfg, content_id, f"made by rekordbox {content_id}", path=None, file_id=4242, bpm=12400)
        _whole(cfg, content_id)
    for content_id in stale:
        _row(cfg, content_id, f"copied since {content_id}", path=str(_file(cfg, content_id)), file_id=STALE_ID)
        _whole(cfg, content_id)
    for content_id in zero:
        _row(cfg, content_id, f"zero {content_id}", path=str(_file(cfg, content_id)), file_id=0)
        _whole(cfg, content_id)
    for content_id in missing:
        gone = str(Path(cfg.library.root) / "Music" / f"gone {content_id}.flac")
        _row(cfg, content_id, f"missing {content_id}", path=gone, file_id=RANDOM_ID + 1)
        _whole(cfg, content_id)
    for content_id in deleted:
        _sql(
            cfg,
            f"INSERT INTO djmdContent (ID, Title, rb_local_deleted, {FILE_ID}, created_at, "
            "updated_at) VALUES (?, ?, 1, ?, '2026-10-08', '2026-10-08')",
            content_id,
            f"a tombstone {content_id}",
            RANDOM_ID + 2,
        )
    return db_path


#: Every row ``build`` seeds that a repair must never touch.
UNTOUCHED = ("1", "2", "201", "301", "401", "501", "601")


def _inode(cfg: config.Config, content_id: str) -> int:
    return (Path(cfg.library.root) / "Music" / f"row {content_id}.flac").stat().st_ino


def _planned(
    cfg: config.Config, path: Path | None = None, *, bound: int = BOUND
) -> row_defaults.DefaultsPlan:
    db = rb_writer.open_db(path or cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_defaults.plan_rows(db, root=cfg.library.root, bound=bound)
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
    # Six live rows besides the two landed: the builder's two, one whole, one
    # stale, one zero and one whose file is gone.
    assert plan.rows == 8
    assert plan.fills == len(row_defaults.COLUMNS) * 2 - 2
    # U115: the two landed rows carry the binding's random id and are given
    # their file's inode; nothing else is.
    for content_id in ("101", "102"):
        assert by_id[content_id].file_id == _inode(machine, content_id)
        assert by_id[content_id].file_id_was == str(RANDOM_ID)
        assert by_id[content_id].to_json()["renumber"] == {
            "from": str(RANDOM_ID),
            "to": _inode(machine, content_id),
        }
    assert plan.renumbers == 2
    assert plan.bound == BOUND and not plan.undecidable
    assert plan.within_bound == 2, "the whole row at 4242 and the stale row"
    assert plan.zero == 3, "the builder's two NULL rows and the zero row"
    assert [(one.content_id, one.why) for one in plan.unrenumbered] == [
        ("601", row_defaults.FILE_MISSING)
    ]
    assert plan.unrenumbered[0].to_json()[FILE_ID] == str(RANDOM_ID + 1)


def test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own(machine):
    """The A8 row of 2026-09-29, repaired by R-923 and still unplayable: no
    default to fill, a random file id to replace."""
    build(machine, landed=())
    _row(machine, "701", "A8", path=str(_file(machine, "701")), file_id=RANDOM_ID)
    _whole(machine, "701")

    plan = _planned(machine)

    (item,) = plan.items
    assert item.content_id == "701" and item.columns == ()
    assert item.renumbers and item.file_id == _inode(machine, "701")
    assert plan.fills == 0 and plan.renumbers == 1


def test_an_id_above_the_bound_that_is_the_files_inode_is_not_random(machine):
    """On a volume whose counter has run past the bound a file's own inode is
    above it too, and reading the file is what tells it from a random id."""
    build(machine, landed=(), missing=())
    path = _file(machine, "801")
    _row(machine, "801", "matching", path=str(path), file_id=path.stat().st_ino)
    _whole(machine, "801")

    plan = _planned(machine)

    assert plan.items == () and plan.unrenumbered == ()
    assert plan.within_bound == 3


def test_a_path_that_does_not_resolve_leaves_the_row_and_names_why(machine):
    build(machine, landed=(), missing=())
    _row(machine, "901", "elsewhere", path="file://otherhost/x.flac", file_id=RANDOM_ID)
    _row(machine, "902", "no path", path="", file_id=RANDOM_ID)
    for content_id in ("901", "902"):
        _whole(machine, content_id)

    plan = _planned(machine)

    assert plan.items == ()
    assert [(one.content_id, one.why) for one in plan.unrenumbered] == [
        ("901", row_defaults.PATH_UNRESOLVED),
        ("902", row_defaults.PATH_UNRESOLVED),
    ]


def test_past_the_bindings_range_nothing_is_judged_random(machine):
    build(machine)
    plan = _planned(machine, bound=rb_writer.BINDING_ID_LIMIT)
    assert plan.undecidable
    assert plan.renumbers == 0 and plan.unrenumbered == ()
    # The defaults are still planned: the bound governs the file id alone.
    assert [item.content_id for item in plan.items] == ["101", "102"]
    assert all(not item.renumbers for item in plan.items)


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


def test_the_digest_moves_when_a_random_id_is_replaced_elsewhere(machine):
    build(machine)
    before = _planned(machine).digest
    _sql(machine, f"UPDATE djmdContent SET {FILE_ID} = 777 WHERE ID = '101'")
    assert _planned(machine).digest != before


def test_the_digest_is_equal_across_two_bounds_that_select_the_same_rows(machine):
    """A copy rehearsal and the live run each create their own file, so their
    bounds differ by at least one and the approval must not hang on it."""
    build(machine)
    assert _planned(machine, bound=BOUND).digest == _planned(machine, bound=BOUND + 5).digest


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
    facts = refused["cause"]["detail"]["shown"]
    assert facts[f"rows given their file's inode as {FILE_ID}"] == 2
    assert facts["the volume's inode bound"] == BOUND
    assert "why no file id is renumbered" not in facts
    assert acted["data"]["totals"]["written"] == 2
    assert acted["data"]["totals"]["read_back"] == 2
    assert acted["data"]["totals"]["renumbered"] == 2
    after = _content(acknowledged)
    assert _as_text(after["101"]) == WANTED
    # U115: the random id is gone and the file's inode is there, on both rows.
    for content_id in ("101", "102"):
        assert str(after[content_id][FILE_ID]) == str(_inode(acknowledged, content_id))
    # The stale, zero and missing file rows keep the id they had.
    assert str(after["401"][FILE_ID]) == str(STALE_ID)
    assert str(after["501"][FILE_ID]) == "0"
    assert str(after["601"][FILE_ID]) == str(RANDOM_ID + 1)
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
            and column != FILE_ID
            and column not in rb_writer.BOOKKEEPING_COLUMNS
            and value != before[content_id][column]
        }
        assert moved == set(), (content_id, moved)
    for content_id in UNTOUCHED:
        assert after[content_id] == before[content_id], content_id
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes == [row_defaults_cli.DEFAULTS_WRITTEN, row_defaults_cli.UNRENUMBERED]
    assert "601" in acted["warnings"][1]["message"]
    assert acted["data"]["totals"]["unrenumbered"][0]["content_id"] == "601"
    assert acted["data"]["totals"]["bound"] == BOUND
    # The policies the apply registered are gone again: no later writer in
    # this process gains a column by them.
    assert rb_writer.ROW_DEFAULTS_POLICY.owner not in rb_writer.registered_field_policies()
    assert rb_writer.FILE_ID_POLICY.owner not in rb_writer.registered_field_policies()
    assert rb_writer.content_writable_columns() == {"ColorID"}


def test_a_policy_registered_before_the_apply_survives_it(acknowledged):
    """The restore puts back what was there, not the baseline: a metadata
    operation enabled earlier in the process keeps its columns afterwards."""
    from types import MappingProxyType

    build(acknowledged)
    plan = _planned(acknowledged)
    rb_writer.register_field_policy(
        rb_writer.FieldPolicy(
            owner="probe", fields=MappingProxyType({"Subtitle": rb_writer.Ownership.OWNED})
        )
    )

    written = _apply(acknowledged, plan)

    assert written.written == 2
    assert set(rb_writer.registered_field_policies()) == {"track-color", "probe"}
    assert rb_writer.content_writable_columns() == {"ColorID", "Subtitle"}


def test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing(acknowledged):
    build(acknowledged, landed=(), missing=())
    before = _content(acknowledged)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["count"] == 0
    assert acted["outcome"] == "no_op"
    assert [warning["code"] for warning in acted["warnings"]] == [
        row_defaults_cli.NOTHING_TO_WRITE
    ]
    assert _content(acknowledged) == before


def test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing(acknowledged):
    build(acknowledged, landed=())
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert [warning["code"] for warning in acted["warnings"]] == [
        row_defaults_cli.NOTHING_TO_WRITE,
        row_defaults_cli.UNRENUMBERED,
    ]
    assert row_defaults.FILE_MISSING in acted["warnings"][1]["message"]


def test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered(acknowledged, monkeypatch):
    monkeypatch.setattr(row_defaults, "inode_bound", lambda cfg: rb_writer.BINDING_ID_LIMIT + 1)
    build(acknowledged)
    before = _content(acknowledged)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    facts = refused["cause"]["detail"]["shown"]
    assert facts[f"rows given their file's inode as {FILE_ID}"] == 0
    assert str(rb_writer.BINDING_ID_LIMIT) in facts["why no file id is renumbered"]
    assert acted["data"]["totals"] == {
        **acted["data"]["totals"],
        "written": 2,
        "renumbers": 0,
        "renumbered": 0,
    }
    assert [warning["code"] for warning in acted["warnings"]] == [
        row_defaults_cli.DEFAULTS_WRITTEN,
        row_defaults_cli.BOUND_UNDECIDABLE,
    ]
    after = _content(acknowledged)
    for content_id in ("101", "102"):
        assert str(after[content_id][FILE_ID]) == str(RANDOM_ID)
        assert _as_text(after[content_id]) == WANTED
    for content_id in UNTOUCHED:
        assert after[content_id] == before[content_id], content_id


def test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind(machine):
    state = config.library_state_dir(machine)
    state.mkdir(parents=True, exist_ok=True)
    probe = state / "older"
    probe.write_bytes(b"")
    before = sorted(p.name for p in state.iterdir())

    bound = REAL_INODE_BOUND(machine)

    assert isinstance(bound, int) and bound > probe.stat().st_ino
    assert sorted(p.name for p in state.iterdir()) == before


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


def test_a_file_id_changed_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    """rekordbox, or a person re-importing, may have numbered the row since."""
    build(acknowledged)
    plan = _planned(acknowledged)
    _sql(acknowledged, f"UPDATE djmdContent SET {FILE_ID} = 1234 WHERE ID = '101'")
    before = _content(acknowledged)

    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)

    assert caught.value.cause.reason == "decision-stale"
    assert f"101: {FILE_ID} changed since the plan" in caught.value.cause.message
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


def test_the_guard_refuses_a_file_id_written_without_the_policy(acknowledged):
    """The file id is not a bookkeeping column: written bare, the guard refuses."""
    build(acknowledged)
    from pyrekordbox.db6 import tables

    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        row = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID == "101").one()
        setattr(row, FILE_ID, _inode(acknowledged, "101"))
        with pytest.raises(Exception) as caught:
            rb_writer.commit_guarded(db)
        assert FILE_ID in str(caught.value)
    finally:
        rb_writer.close_db(db)
    assert str(_content(acknowledged)["101"][FILE_ID]) == str(RANDOM_ID)


def test_a_plan_that_renumbers_nothing_registers_no_file_id_policy(acknowledged, monkeypatch):
    """A run that fills defaults alone cannot write the column, even by defect."""
    seen: dict[str, set[str]] = {}
    real = rb_writer.commit_guarded

    def spy(db, **kwargs):
        seen["owners"] = set(rb_writer.registered_field_policies())
        return real(db, **kwargs)

    monkeypatch.setattr(rb_writer, "commit_guarded", spy)
    build(acknowledged)
    plan = _planned(acknowledged, bound=rb_writer.BINDING_ID_LIMIT)
    assert plan.renumbers == 0
    _apply(acknowledged, plan)
    assert rb_writer.ROW_DEFAULTS_POLICY.owner in seen["owners"]
    assert rb_writer.FILE_ID_POLICY.owner not in seen["owners"]


def test_the_policies_are_registered_by_the_apply_and_not_at_baseline():
    assert rb_writer.ROW_DEFAULTS_POLICY.owner not in rb_writer.registered_field_policies()
    assert rb_writer.FILE_ID_POLICY.owner not in rb_writer.registered_field_policies()
    assert not set(DEFAULTS) & rb_writer.content_writable_columns() - {"ColorID"}
    assert FILE_ID not in rb_writer.content_writable_columns()


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


def test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard():
    """U115. Owned, since the value replaced is present and wrong; not an analysis
    column; and NOT bookkeeping, which would blind the guard for every writer."""
    from pyrekordbox.db6 import tables

    assert FILE_ID in tables.DjmdContent.__table__.columns.keys()
    assert FILE_ID not in rb_writer.CONTENT_ROW_EMPTY_COLUMNS
    assert FILE_ID not in rb_writer.BOOKKEEPING_COLUMNS
    assert FILE_ID not in DEFAULTS
    assert dict(rb_writer.FILE_ID_POLICY.fields) == {FILE_ID: rb_writer.Ownership.OWNED}
    assert rb_writer.BINDING_ID_LIMIT == 2**28


@pytest.mark.parametrize(
    ("value", "state"),
    [
        (None, row_defaults.ZERO),
        ("", row_defaults.ZERO),
        (0, row_defaults.ZERO),
        ("0", row_defaults.ZERO),
        (BOUND, row_defaults.WITHIN),
        (str(BOUND), row_defaults.WITHIN),
        (1, row_defaults.WITHIN),
        ("not a number", row_defaults.WITHIN),
        (BOUND + 1, row_defaults.ABOVE),
        (str(RANDOM_ID), row_defaults.ABOVE),
        (f" {RANDOM_ID} ", row_defaults.ABOVE),
    ],
)
def test_a_file_id_is_judged_against_the_bound_alone(value, state):
    assert row_defaults.file_id_state(value, BOUND) == state


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


def test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved():
    renumbered = row_defaults.Item(
        content_id="101", title="t", path="p", columns=(), file_id=4242, file_id_was="200000000"
    )
    plan = row_defaults.DefaultsPlan(items=(renumbered, _item("102", ())), rows=2)
    before = {
        "101": {FILE_ID: "200000000", "BPM": 0},
        "102": {FILE_ID: "200000000", "BPM": 0},
    }
    after = {"101": {FILE_ID: 4242, "BPM": 0}, "102": {FILE_ID: 4242, "BPM": 0}}
    wrong, moved = row_defaults.judge(plan, before, after)
    assert wrong == ()
    assert moved == (f"102: {FILE_ID}",)


def test_judge_names_a_renumber_that_did_not_take():
    renumbered = row_defaults.Item(
        content_id="101", title="t", path="p", columns=(), file_id=4242, file_id_was="200000000"
    )
    plan = row_defaults.DefaultsPlan(items=(renumbered,), rows=1)
    before = {"101": {FILE_ID: "200000000"}}
    after = {"101": {FILE_ID: "200000000"}}
    wrong, moved = row_defaults.judge(plan, before, after)
    assert wrong == (f"101: {FILE_ID} not the file's inode",)
    assert moved == ()


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

