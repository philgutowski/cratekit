"""``crate repair link``: a chosen ``ContentLink`` written onto one live row through
the guard, the experiment that asks whether that column keeps a landed row off a
deck (A32, R-928).

The library, the seams and the two acts are ``repair rows``'s, imported from its
suite rather than typed again: the same disposable database, the same platform
patches, the same acknowledgment. What is added is the column: every seeded row
is given the value rekordbox writes, and the rows a landing made are given the
binding's.
"""

# ruff: noqa: F811, the fixtures below are imported from the repair rows suite by name
from __future__ import annotations

import pytest

from cratekit.core import rb_writer
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.write import row_link, row_link_cli
from tests.cli_drive import drive
from tests.test_repair_rows import (  # noqa: F401, the fixtures are used by name
    UNTOUCHED,
    _bound,
    _content,
    _field_policies,
    _platform_seams,
    _release_process_locks,
    _sql,
    _whole,
    acknowledged,
    build,
    machine,
)

VERB = ["repair", "link"]
GATE = row_link_cli.CONFIRM_GATE
LINK = rb_writer.CONTENT_LINK_COLUMN

#: What rekordbox writes on nearly every row it makes, measured 2026-10-10.
HOUSE = 2950670
#: What the binding wrote on every row the landing made, measured the same day.
BINDING = 2973454
#: A value no row carries.
NOBODY = 4242424


def seed(cfg) -> None:
    """``repair rows``'s library with the column set: rekordbox's value on every
    row it made, the binding's on the two rows a landing made, made whole so the
    column is the one difference."""
    build(cfg)
    _sql(cfg, f"UPDATE djmdContent SET {LINK} = ?", HOUSE)
    _sql(cfg, f"UPDATE djmdContent SET {LINK} = ? WHERE ID IN ('101', '102')", BINDING)
    for content_id in ("101", "102"):
        _whole(cfg, content_id)


def _planned(cfg, content_id: str = "101", value: int = HOUSE) -> row_link.LinkPlan:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_link.plan_link(db, content_id=content_id, value=value)
    finally:
        rb_writer.close_db(db)


def _apply(cfg, plan: row_link.LinkPlan) -> row_link.Written:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_link.apply_link(cfg, db, plan, analysis_roots=[cfg.library.root])
    finally:
        rb_writer.close_db(db)


def _two_acts(content_id: str = "101", value: int = HOUSE) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    argv = [*VERB, content_id, str(value)]
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *argv])
    return code, acted, refused


# ═══════════════════════════════════════════════════════════════════════════
# The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_is_the_one_row_its_value_and_who_else_carries_each(machine):
    seed(machine)
    plan = _planned(machine)
    assert (plan.content_id, plan.value, plan.was) == ("101", HOUSE, str(BINDING))
    assert plan.title == "landed 101"
    # Every other live row carries the house value: 1, 2, 201, 401, 501, 601, 102
    # minus 102, which carries the binding's. The tombstone 301 is not counted.
    assert plan.carriers == 6
    assert plan.fellows == 1
    assert plan.rows == 8
    assert plan.to_json() == {
        "content_id": "101",
        "title": "landed 101",
        "path": plan.path,
        "column": LINK,
        "from": str(BINDING),
        "to": HOUSE,
    }


def test_an_unknown_identifier_refuses_by_name_before_any_gate(machine):
    seed(machine)
    with pytest.raises(CratekitError) as caught:
        _planned(machine, content_id="999")
    assert caught.value.cause.reason == row_link.ROW_UNKNOWN


def test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table(machine):
    seed(machine)
    with pytest.raises(CratekitError) as caught:
        _planned(machine, content_id="301")
    assert caught.value.cause.reason == row_link.ROW_UNKNOWN


def test_a_row_already_at_the_value_plans_nothing(machine):
    seed(machine)
    plan = _planned(machine, content_id="201", value=HOUSE)
    assert plan.writes is False and plan.was == str(HOUSE)


def test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = ? WHERE ID = '201'", NOBODY)
    plan = _planned(machine, content_id="201", value=NOBODY)
    assert plan.writes is False and plan.carriers == 0


def test_a_row_already_at_the_value_still_asks_and_then_writes_nothing(acknowledged):
    seed(acknowledged)
    before = _content(acknowledged)
    code, acted, refused = _two_acts("201", HOUSE)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == str(Outcome.NO_OP)
    assert refused["cause"]["detail"]["shown"]["rows to write"] == 0
    assert acted["data"]["totals"]["count"] == 0
    assert [warning["code"] for warning in acted["warnings"]] == [row_link_cli.NOTHING_TO_WRITE]
    assert _content(acknowledged) == before


def test_apply_refuses_a_plan_that_writes_nothing_as_a_defect(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged, content_id="201", value=HOUSE)
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "internal-error"


def test_a_value_no_other_live_row_carries_refuses(machine):
    seed(machine)
    with pytest.raises(CratekitError) as caught:
        _planned(machine, content_id="101", value=NOBODY)
    assert caught.value.cause.reason == row_link.VALUE_UNHELD


def test_a_value_only_a_tombstone_carries_refuses_as_unheld(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = ? WHERE ID = '301'", NOBODY)
    with pytest.raises(CratekitError) as caught:
        _planned(machine, content_id="101", value=NOBODY)
    assert caught.value.cause.reason == row_link.VALUE_UNHELD


def test_a_value_one_other_live_row_carries_is_enough(machine):
    seed(machine)
    # 102 carries the binding's value, so writing it onto a house row plans.
    plan = _planned(machine, content_id="201", value=BINDING)
    assert plan.carriers == 2 and plan.was == str(HOUSE)


def test_a_null_column_plans_with_an_empty_replaced_value(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = NULL WHERE ID = '101'")
    plan = _planned(machine)
    assert plan.was == "" and plan.fellows == 0


def test_the_digest_is_equal_on_a_copy_at_another_path(machine, tmp_path):
    import shutil

    seed(machine)
    copy = tmp_path / "elsewhere" / "master.db"
    copy.parent.mkdir()
    shutil.copy2(machine.library.db_path, copy)
    db = rb_writer.open_db(copy, unlock=False, cfg=machine)
    try:
        on_copy = row_link.plan_link(db, content_id="101", value=HOUSE)
    finally:
        rb_writer.close_db(db)
    assert on_copy.digest == _planned(machine).digest


def test_the_digest_moves_with_the_row_the_value_and_the_value_replaced(machine):
    seed(machine)
    one = _planned(machine, "101", HOUSE)
    assert one.digest != _planned(machine, "102", HOUSE).digest
    assert one.digest != _planned(machine, "201", BINDING).digest
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID = '101'")
    assert one.digest != _planned(machine, "101", HOUSE).digest


def test_the_digest_does_not_move_with_the_carrier_count(machine):
    seed(machine)
    one = _planned(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID = '501'")
    two = _planned(machine)
    assert two.carriers == one.carriers - 1
    assert two.digest == one.digest


# ═══════════════════════════════════════════════════════════════════════════
# The two acts and the apply
# ═══════════════════════════════════════════════════════════════════════════


def test_the_two_acts_write_the_one_column_on_the_one_row_and_move_no_other(acknowledged):
    seed(acknowledged)
    before = _content(acknowledged)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["rows to write"] == 1
    assert shown["value written"] == HOUSE
    assert shown["value replaced"] == str(BINDING)
    assert shown["other live rows carrying the value written"] == 6
    assert acted["data"]["totals"] == {
        "count": 1,
        "rows": 8,
        "carriers": 6,
        "fellows": 1,
        "written": 1,
        "read_back": 1,
    }
    after = _content(acknowledged)
    assert str(after["101"][LINK]) == str(HOUSE)
    moved = {
        column
        for column, value in after["101"].items()
        if column != LINK
        and column not in rb_writer.BOOKKEEPING_COLUMNS
        and value != before["101"][column]
    }
    assert moved == set()
    # The other landed row keeps the binding's value, and nothing else moved.
    assert str(after["102"][LINK]) == str(BINDING)
    assert after["102"] == before["102"]
    for content_id in UNTOUCHED:
        assert after[content_id] == before[content_id], content_id
    assert [warning["code"] for warning in acted["warnings"]] == [row_link_cli.LINK_WRITTEN]
    assert acted["warnings"][0]["message"].startswith("1 row now carries")
    # The policy the apply registered is gone again.
    assert rb_writer.CONTENT_LINK_POLICY.owner not in rb_writer.registered_field_policies()
    assert rb_writer.content_writable_columns() == {"ColorID"}


def test_the_gate_takes_no_inline_answer(acknowledged):
    seed(acknowledged)
    code, payload = drive(["-d", f"{GATE}=apply", *VERB, "101", str(HOUSE)])
    assert code == int(ExitCode.DECISION_REQUIRED), payload
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    seed(machine)
    code, payload = drive([*VERB, "101", str(HOUSE)])
    assert code == int(ExitCode.ACK_REQUIRED), payload
    assert payload["cause"]["reason"] == "backup-acknowledgment-missing"


def test_an_abort_writes_nothing(acknowledged):
    seed(acknowledged)
    code, refused = drive([*VERB, "101", str(HOUSE)])
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *VERB, "101", str(HOUSE)])
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == str(Outcome.NO_OP)
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_a_plan_refusal_reaches_no_gate(acknowledged):
    seed(acknowledged)
    code, payload = drive([*VERB, "999", str(HOUSE)])
    assert code == int(ExitCode.PRECONDITION), payload
    assert payload["cause"]["reason"] == row_link.ROW_UNKNOWN
    assert "run_id" not in payload or payload.get("gate") is None


def test_the_column_changed_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged)
    _sql(acknowledged, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID = '101'")
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "decision-stale"
    assert str(_content(acknowledged)["101"][LINK]) == "7"


def test_the_row_deleted_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged)
    _sql(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '101'")
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "decision-stale"
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_rekordbox_running_refuses_at_the_apply_and_writes_nothing(acknowledged, monkeypatch):
    seed(acknowledged)
    code, refused = drive([*VERB, "101", str(HOUSE)])
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, acted = drive(["--run", run_id, *VERB, "101", str(HOUSE)])
    assert code == int(ExitCode.REKORDBOX_OPEN), acted
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_the_guard_refuses_the_column_written_without_the_policy(acknowledged):
    """The policy is what admits the column: written bare, the guard refuses."""
    seed(acknowledged)
    from pyrekordbox.db6 import tables

    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        row = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID == "101").one()
        setattr(row, LINK, HOUSE)
        with pytest.raises(Exception) as caught:
            rb_writer.commit_guarded(db)
        assert LINK in str(caught.value)
    finally:
        rb_writer.close_db(db)
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_a_tempo_moved_beside_the_write_is_refused_by_the_guard(acknowledged, monkeypatch):
    """The probe's policy admits one column. A tempo set in the same commit is
    refused before it, and the column is not written either."""
    seed(acknowledged)
    real = rb_writer.write_metadata_field

    def and_a_tempo(row, owner, field_name, new_value, **kwargs):
        row.BPM = 12800
        return real(row, owner, field_name, new_value, **kwargs)

    monkeypatch.setattr(rb_writer, "write_metadata_field", and_a_tempo)
    plan = _planned(acknowledged)
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "whitelist-violation"
    row = _content(acknowledged)["101"]
    assert str(row[LINK]) == str(BINDING) and row["BPM"] == 0


def test_a_policy_registered_before_the_apply_survives_it(acknowledged):
    seed(acknowledged)
    other = rb_writer.FieldPolicy(owner="elsewhere", fields={"Commnt": rb_writer.Ownership.OWNED})
    rb_writer.register_field_policy(other)
    _apply(acknowledged, _planned(acknowledged))
    assert rb_writer.registered_field_policies()["elsewhere"] is other
    assert rb_writer.CONTENT_LINK_POLICY.owner not in rb_writer.registered_field_policies()


def test_the_write_is_recorded_on_a_session_with_a_capture(acknowledged):
    from cratekit.core import session

    seed(acknowledged)
    written = _apply(acknowledged, _planned(acknowledged))
    record = session.read_record(written.session_id, acknowledged)
    assert record.sources[row_link.CHANGE_KEY] == str(session.SourceState.COMMITTED)
    assert record.snapshot_path is not None


# ═══════════════════════════════════════════════════════════════════════════
# The read back, pure
# ═══════════════════════════════════════════════════════════════════════════


def _plan_of(value: int = HOUSE, was: str = str(BINDING)) -> row_link.LinkPlan:
    return row_link.LinkPlan(
        content_id="101",
        title="t",
        path="p",
        value=value,
        was=was,
        carriers=1,
        fellows=0,
        rows=2,
    )


def test_judge_accepts_the_value_read_back_as_the_live_tables_integer():
    before = {"101": {LINK: BINDING, "BPM": 0, "updated_at": "a"}}
    after = {"101": {LINK: HOUSE, "BPM": 0, "updated_at": "b"}}
    assert row_link.judge(_plan_of(), before, after) == ((), ())


def test_judge_names_a_value_that_did_not_take_and_a_column_that_moved():
    before = {"101": {LINK: BINDING, "BPM": 0}}
    after = {"101": {LINK: BINDING, "BPM": 12800}}
    wrong, moved = row_link.judge(_plan_of(), before, after)
    assert wrong == (f"101: {LINK} not {HOUSE}",)
    assert moved == ("101: BPM",)


def test_judge_names_a_row_that_could_not_be_read():
    wrong, moved = row_link.judge(_plan_of(), {}, {})
    assert wrong == ("101: the row could not be read",) and moved == ()


def test_assert_read_back_refuses_a_moved_column_as_the_guards_defect():
    with pytest.raises(CratekitError) as caught:
        row_link.assert_read_back(
            row_link.Written(session_id="s", written=1, read_back=1, moved=("101: BPM",))
        )
    assert caught.value.cause.reason == "whitelist-violation"
    assert "restore session s" in " ".join(caught.value.cause.remediation.steps)


def test_assert_read_back_refuses_a_wrong_value():
    with pytest.raises(CratekitError) as caught:
        row_link.assert_read_back(
            row_link.Written(session_id="s", written=1, read_back=0, wrong=("101: x",))
        )
    assert caught.value.cause.reason == "internal-error"


def test_assert_read_back_passes_a_clean_write():
    row_link.assert_read_back(row_link.Written(session_id="s", written=1, read_back=1))


def test_apply_refuses_an_empty_watch_before_touching_the_database(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged)
    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        with pytest.raises(ValueError):
            row_link.apply_link(acknowledged, db, plan, analysis_roots=[])
    finally:
        rb_writer.close_db(db)
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


# ═══════════════════════════════════════════════════════════════════════════
# The column and its policy
# ═══════════════════════════════════════════════════════════════════════════


def test_the_column_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard():
    from pyrekordbox.db6 import tables

    assert LINK in tables.DjmdContent.__table__.columns
    assert LINK not in rb_writer.BOOKKEEPING_COLUMNS
    assert LINK not in rb_writer.CONTENT_ROW_DEFAULTS
    assert dict(rb_writer.CONTENT_LINK_POLICY.fields) == {LINK: rb_writer.Ownership.OWNED}
    assert rb_writer.CONTENT_LINK_POLICY.owner not in rb_writer.registered_field_policies()
