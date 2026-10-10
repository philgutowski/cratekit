"""``crate repair link``: chosen values written into the row probe columns of
chosen live rows through the guard, the experiment that asks which column keeps a
landed row off a deck (A32, R-928).

The library, the seams and the acknowledgment are ``repair rows``'s, imported
from its suite rather than typed again. What is added is the two probe columns:
every row rekordbox made is given the ContentLink and the empty ISRC rekordbox
writes, and the two rows a landing made are given the binding's ContentLink and
a NULL ISRC, so those two columns are the whole difference.
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
ISRC = rb_writer.ISRC_COLUMN

#: What rekordbox writes on nearly every row it makes, measured 2026-10-10.
HOUSE = 2950670
#: What the binding wrote on every row the landing made, measured the same day.
BINDING = 2973454
#: A value no row carries.
NOBODY = 4242424

#: The two rows a landing made, and the rows rekordbox made that stay live.
LANDED = ("101", "102")
MADE = ("1", "2", "201", "401", "501", "601")


def seed(cfg) -> None:
    """``repair rows``'s library with the probe columns set: rekordbox's values on
    every row it made, the binding's on the two rows a landing made, each made
    whole so the probe columns are the one difference."""
    build(cfg)
    _sql(cfg, f"UPDATE djmdContent SET {LINK} = ?, {ISRC} = ''", HOUSE)
    _sql(
        cfg,
        f"UPDATE djmdContent SET {LINK} = ?, {ISRC} = NULL WHERE ID IN ('101', '102')",
        BINDING,
    )
    for content_id in LANDED:
        _whole(cfg, content_id)


def _sets(*specs: str) -> list[str]:
    return [part for spec in specs for part in ("--set", spec)]


def _planned(cfg, *specs: str) -> row_link.ProbePlan:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_link.plan_probes(db, [row_link.parse_triple(spec) for spec in specs])
    finally:
        rb_writer.close_db(db)


def _apply(cfg, plan: row_link.ProbePlan) -> row_link.Written:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return row_link.apply_probes(cfg, db, plan, analysis_roots=[cfg.library.root])
    finally:
        rb_writer.close_db(db)


def _two_acts(*specs: str) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    argv = [*VERB, *_sets(*specs)]
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *argv])
    return code, acted, refused


def _refused(cfg, *specs: str) -> str:
    with pytest.raises(CratekitError) as caught:
        _planned(cfg, *specs)
    return caught.value.cause.reason


# ═══════════════════════════════════════════════════════════════════════════
# Parsing a triple
# ═══════════════════════════════════════════════════════════════════════════


def test_a_triple_reads_row_column_and_a_value_of_the_columns_type():
    assert row_link.parse_triple(f"101:{LINK}={HOUSE}") == row_link.Triple("101", LINK, HOUSE)
    assert row_link.parse_triple(f"101:{ISRC}=") == row_link.Triple("101", ISRC, "")
    assert row_link.parse_triple(f" 101 : {ISRC}=X1") == row_link.Triple("101", ISRC, "X1")


@pytest.mark.parametrize(
    "spec",
    [
        f"101{LINK}={HOUSE}",  # no colon
        f"101:{LINK}{HOUSE}",  # no equals
        f":{LINK}={HOUSE}",  # no row
        f"101:={HOUSE}",  # no column
        f"101:{LINK}=lots",  # not a whole number
        f"101:{LINK}=",  # an empty ContentLink is not a number
        "101:AnalysisUpdated=2",  # an analysis column, never the probe's
        "101:BPM=12800",  # a tempo, never anybody's
        "101:Title=x",  # any other column
    ],
)
def test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name(spec):
    with pytest.raises(CratekitError) as caught:
        row_link.parse_triple(spec)
    assert caught.value.cause.reason == row_link.PROBE_INVALID


def test_the_probe_columns_are_exactly_the_two_and_neither_is_an_analysis_column():
    from pyrekordbox.db6 import tables

    assert tuple(rb_writer.ROW_PROBE_COLUMNS) == (LINK, ISRC)
    for column in rb_writer.ROW_PROBE_COLUMNS:
        assert column in tables.DjmdContent.__table__.columns
        assert column not in rb_writer.BOOKKEEPING_COLUMNS
        assert column not in rb_writer.CONTENT_ROW_EMPTY_COLUMNS
        assert column not in rb_writer.CONTENT_ROW_DEFAULTS
    assert "AnalysisUpdated" in rb_writer.GRIDLESS_ON_CREATE_COLUMNS


def test_the_probe_policy_names_exactly_the_columns_asked_and_refuses_any_other():
    policy = rb_writer.row_probe_policy([ISRC])
    assert dict(policy.fields) == {ISRC: rb_writer.Ownership.OWNED}
    assert policy.owner == rb_writer.ROW_PROBE_OWNER
    with pytest.raises(ValueError):
        rb_writer.row_probe_policy([LINK, "AnalysisUpdated"])
    assert rb_writer.ROW_PROBE_OWNER not in rb_writer.registered_field_policies()


# ═══════════════════════════════════════════════════════════════════════════
# The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_is_each_triple_its_values_and_who_else_carries_each(machine):
    seed(machine)
    plan = _planned(machine, f"101:{LINK}={HOUSE}", f"101:{ISRC}=", f"102:{ISRC}=")
    assert [(p.content_id, p.column) for p in plan.probes] == [
        ("101", LINK),
        ("101", ISRC),
        ("102", ISRC),
    ]
    link, isrc, other = plan.probes
    assert (link.was, link.value, link.carriers, link.fellows) == (str(BINDING), HOUSE, 6, 1)
    assert (isrc.was, isrc.value, isrc.carriers, isrc.fellows) == (None, "", 6, 1)
    assert other.was is None and other.writes
    assert plan.writes == 3 and plan.content_ids == ["101", "102"]
    assert plan.columns_on("101") == (LINK, ISRC)
    assert plan.rows == 8
    assert link.to_json() == {
        "content_id": "101",
        "title": "landed 101",
        "path": link.path,
        "column": LINK,
        "from": str(BINDING),
        "to": str(HOUSE),
        "writes": True,
    }


def test_no_triple_at_all_refuses(machine):
    seed(machine)
    db = rb_writer.open_db(machine.library.db_path, unlock=False, cfg=machine)
    try:
        with pytest.raises(CratekitError) as caught:
            row_link.plan_probes(db, [])
    finally:
        rb_writer.close_db(db)
    assert caught.value.cause.reason == row_link.PROBE_INVALID


def test_the_same_row_and_column_twice_refuses(machine):
    seed(machine)
    assert _refused(machine, f"101:{LINK}={HOUSE}", f"101:{LINK}={HOUSE}") == row_link.PROBE_INVALID


def test_an_unknown_identifier_refuses_by_name_before_any_gate(machine):
    seed(machine)
    assert _refused(machine, f"999:{LINK}={HOUSE}") == row_link.ROW_UNKNOWN


def test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table(machine):
    seed(machine)
    assert _refused(machine, f"301:{LINK}={HOUSE}") == row_link.ROW_UNKNOWN


def test_one_bad_triple_refuses_the_whole_plan(machine):
    seed(machine)
    assert _refused(machine, f"101:{LINK}={HOUSE}", f"999:{ISRC}=") == row_link.ROW_UNKNOWN


def test_a_row_already_at_the_value_plans_nothing_for_that_triple(machine):
    seed(machine)
    plan = _planned(machine, f"201:{LINK}={HOUSE}", f"201:{ISRC}=")
    assert plan.writes == 0 and all(not p.writes for p in plan.probes)


def test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = ? WHERE ID = '201'", NOBODY)
    plan = _planned(machine, f"201:{LINK}={NOBODY}")
    assert plan.writes == 0 and plan.probes[0].carriers == 0


def test_a_value_no_other_live_row_carries_refuses(machine):
    seed(machine)
    assert _refused(machine, f"101:{LINK}={NOBODY}") == row_link.VALUE_UNHELD
    assert _refused(machine, f"101:{ISRC}=NOBODY") == row_link.VALUE_UNHELD


def test_a_value_only_a_tombstone_carries_refuses_as_unheld(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = ? WHERE ID = '301'", NOBODY)
    assert _refused(machine, f"101:{LINK}={NOBODY}") == row_link.VALUE_UNHELD


def test_the_bindings_value_onto_a_row_rekordbox_made_refuses_as_the_minority(machine):
    """The probe moves a row toward the value most rows carry, never away: the
    reverse write would take a row that loads and make the question worse."""
    seed(machine)
    with pytest.raises(CratekitError) as caught:
        _planned(machine, f"201:{LINK}={BINDING}")
    assert caught.value.cause.reason == row_link.VALUE_MINORITY
    assert caught.value.cause.detail["carriers"] == 2
    assert caught.value.cause.detail["fellows"] == 5


def test_a_null_counts_its_fellows_as_null_so_writing_one_back_is_the_minority(machine):
    """An ISRC of NULL is held by the two landed rows only. Writing the empty
    text over a rekordbox row's empty text is a no op, and a NULL is not a value
    the probe can ask for at all, so the minority rule is driven on text."""
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {ISRC} = 'X1' WHERE ID IN ('101', '102')")
    # 101 holds X1 with one fellow, 102; six rows hold the empty text.
    plan = _planned(machine, f"101:{ISRC}=")
    assert (plan.probes[0].carriers, plan.probes[0].fellows) == (6, 1)
    # 201 holds the empty text with five fellows; two hold X1: refused.
    assert _refused(machine, f"201:{ISRC}=X1") == row_link.VALUE_MINORITY


def test_a_value_carried_by_as_many_rows_as_the_rows_own_refuses_too(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID IN ('401', '501', '601')")
    # 601 holds 7 with two fellows; two rows carry the binding's value: equal, refused.
    assert _refused(machine, f"601:{LINK}={BINDING}") == row_link.VALUE_MINORITY


def test_a_value_more_rows_carry_than_the_rows_own_is_enough_though_not_the_house(machine):
    seed(machine)
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID IN ('401', '501')")
    probe = _planned(machine, f"101:{LINK}=7").probes[0]
    assert (probe.carriers, probe.fellows, probe.writes) == (2, 1, True)


def test_the_digest_is_equal_on_a_copy_at_another_path(machine, tmp_path):
    import shutil

    seed(machine)
    copy = tmp_path / "elsewhere" / "master.db"
    copy.parent.mkdir()
    shutil.copy2(machine.library.db_path, copy)
    specs = (f"101:{LINK}={HOUSE}", f"102:{ISRC}=")
    db = rb_writer.open_db(copy, unlock=False, cfg=machine)
    try:
        on_copy = row_link.plan_probes(db, [row_link.parse_triple(s) for s in specs])
    finally:
        rb_writer.close_db(db)
    assert on_copy.digest == _planned(machine, *specs).digest


def test_the_digest_is_equal_whatever_order_the_triples_are_given_in(machine):
    seed(machine)
    one = _planned(machine, f"101:{LINK}={HOUSE}", f"102:{ISRC}=", f"101:{ISRC}=")
    two = _planned(machine, f"101:{ISRC}=", f"102:{ISRC}=", f"101:{LINK}={HOUSE}")
    assert one.digest == two.digest


def test_the_digest_moves_with_the_rows_the_columns_and_both_values(machine):
    seed(machine)
    one = _planned(machine, f"101:{LINK}={HOUSE}")
    assert one.digest != _planned(machine, f"102:{LINK}={HOUSE}").digest
    assert one.digest != _planned(machine, f"101:{ISRC}=").digest
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID IN ('401', '501')")
    assert one.digest != _planned(machine, f"101:{LINK}=7").digest
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID = '101'")
    assert one.digest != _planned(machine, f"101:{LINK}={HOUSE}").digest


def test_the_digest_does_not_move_with_the_carrier_count(machine):
    seed(machine)
    one = _planned(machine, f"101:{LINK}={HOUSE}")
    _sql(machine, f"UPDATE djmdContent SET {LINK} = 7 WHERE ID = '501'")
    two = _planned(machine, f"101:{LINK}={HOUSE}")
    assert two.probes[0].carriers == one.probes[0].carriers - 1
    assert two.digest == one.digest


# ═══════════════════════════════════════════════════════════════════════════
# The two acts and the apply
# ═══════════════════════════════════════════════════════════════════════════


def test_the_two_acts_write_each_triple_and_move_no_other_column(acknowledged):
    seed(acknowledged)
    before = _content(acknowledged)

    code, acted, refused = _two_acts(f"101:{LINK}={HOUSE}", f"101:{ISRC}=", f"102:{ISRC}=")

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["values to write"] == 3 and shown["rows to write"] == 2
    assert shown["columns the probe may write"] == [LINK, ISRC]
    first = shown["each write, with who else carries each value"][0]
    assert first["from"] == str(BINDING) and first["to"] == str(HOUSE)
    assert first["other rows carrying the value written"] == 6
    assert acted["data"]["totals"] == {
        "count": 3,
        "probes": 3,
        "rows": 8,
        "rows_written": 2,
        "written": 3,
        "read_back": 3,
    }
    after = _content(acknowledged)
    assert str(after["101"][LINK]) == str(HOUSE) and after["101"][ISRC] == ""
    # 102 took its ISRC and keeps the binding's ContentLink.
    assert after["102"][ISRC] == "" and str(after["102"][LINK]) == str(BINDING)
    for content_id, written in (("101", {LINK, ISRC}), ("102", {ISRC})):
        moved = {
            column
            for column, value in after[content_id].items()
            if column not in written
            and column not in rb_writer.BOOKKEEPING_COLUMNS
            and value != before[content_id][column]
        }
        assert moved == set(), (content_id, moved)
    for content_id in UNTOUCHED:
        assert after[content_id] == before[content_id], content_id
    assert [warning["code"] for warning in acted["warnings"]] == [row_link_cli.LINK_WRITTEN]
    assert acted["warnings"][0]["message"].startswith("3 value(s) written on 2 row(s)")
    # The policy the apply registered is gone again.
    assert rb_writer.ROW_PROBE_OWNER not in rb_writer.registered_field_policies()
    assert rb_writer.content_writable_columns() == {"ColorID"}


def test_a_triple_already_at_its_value_is_shown_and_not_written(acknowledged):
    seed(acknowledged)
    before = _content(acknowledged)
    code, acted, _ = _two_acts(f"101:{ISRC}=", f"201:{LINK}={HOUSE}")
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["count"] == 1
    assert [item["writes"] for item in acted["data"]["items"]] == [True, False]
    after = _content(acknowledged)
    assert after["201"] == before["201"]
    assert after["101"][ISRC] == ""


def test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing(acknowledged):
    seed(acknowledged)
    before = _content(acknowledged)
    code, acted, refused = _two_acts(f"201:{LINK}={HOUSE}")
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == str(Outcome.NO_OP)
    assert refused["cause"]["detail"]["shown"]["values to write"] == 0
    assert acted["data"]["totals"]["count"] == 0
    assert [warning["code"] for warning in acted["warnings"]] == [row_link_cli.NOTHING_TO_WRITE]
    assert _content(acknowledged) == before


def test_apply_refuses_a_plan_that_writes_nothing_as_a_defect(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged, f"201:{LINK}={HOUSE}")
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "internal-error"


def test_the_gate_takes_no_inline_answer(acknowledged):
    seed(acknowledged)
    code, payload = drive(["-d", f"{GATE}=apply", *VERB, *_sets(f"101:{LINK}={HOUSE}")])
    assert code == int(ExitCode.DECISION_REQUIRED), payload
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    seed(machine)
    code, payload = drive([*VERB, *_sets(f"101:{LINK}={HOUSE}")])
    assert code == int(ExitCode.ACK_REQUIRED), payload
    assert payload["cause"]["reason"] == "backup-acknowledgment-missing"


def test_an_abort_writes_nothing(acknowledged):
    seed(acknowledged)
    argv = [*VERB, *_sets(f"101:{LINK}={HOUSE}")]
    code, refused = drive(argv)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *argv])
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == str(Outcome.NO_OP)
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_a_plan_refusal_reaches_no_gate(acknowledged):
    seed(acknowledged)
    code, payload = drive([*VERB, *_sets(f"999:{LINK}={HOUSE}")])
    assert code == int(ExitCode.PRECONDITION), payload
    assert payload["cause"]["reason"] == row_link.ROW_UNKNOWN


def test_a_malformed_triple_refuses_through_the_verb_before_any_gate(acknowledged):
    seed(acknowledged)
    code, payload = drive([*VERB, *_sets("101:AnalysisUpdated=2")])
    assert code == int(ExitCode.PRECONDITION), payload
    assert payload["cause"]["reason"] == row_link.PROBE_INVALID


def test_no_set_at_all_refuses_through_the_verb(acknowledged):
    seed(acknowledged)
    code, payload = drive(VERB)
    assert code == int(ExitCode.PRECONDITION), payload
    assert payload["cause"]["reason"] == row_link.PROBE_INVALID


def test_a_column_changed_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged, f"101:{LINK}={HOUSE}", f"102:{ISRC}=")
    _sql(acknowledged, f"UPDATE djmdContent SET {ISRC} = 'X1' WHERE ID = '102'")
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "decision-stale"
    after = _content(acknowledged)
    # Nothing was written on either row.
    assert str(after["101"][LINK]) == str(BINDING) and after["102"][ISRC] == "X1"


def test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged, f"101:{LINK}={HOUSE}")
    _sql(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '101'")
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, plan)
    assert caught.value.cause.reason == "decision-stale"
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_rekordbox_running_refuses_at_the_apply_and_writes_nothing(acknowledged, monkeypatch):
    seed(acknowledged)
    argv = [*VERB, *_sets(f"101:{LINK}={HOUSE}")]
    code, refused = drive(argv)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, acted = drive(["--run", run_id, *argv])
    assert code == int(ExitCode.REKORDBOX_OPEN), acted
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


def test_a_column_moved_after_the_commit_refuses_through_the_verb(acknowledged, monkeypatch):
    """The read back is what the verb answers with: a judge that finds a moved
    column after the commit refuses the run as the guard's defect, naming the
    session whose capture undoes the durable write."""
    seed(acknowledged)
    monkeypatch.setattr(row_link, "judge", lambda plan, before, after: ((), ("101: BPM",)))
    code, acted, _ = _two_acts(f"101:{LINK}={HOUSE}")
    assert code == int(ExitCode.REFUSED_BY_POLICY), acted
    assert acted["cause"]["reason"] == "whitelist-violation"
    assert "restore session" in " ".join(acted["cause"]["remediation"]["steps"])
    assert str(_content(acknowledged)["101"][LINK]) == str(HOUSE)


@pytest.mark.parametrize("column", [LINK, ISRC])
def test_the_guard_refuses_a_probe_column_written_without_the_policy(acknowledged, column):
    """The policy is what admits each column: written bare, the guard refuses."""
    seed(acknowledged)
    from pyrekordbox.db6 import tables

    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        row = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID == "101").one()
        setattr(row, column, HOUSE if column == LINK else "")
        with pytest.raises(Exception) as caught:
            rb_writer.commit_guarded(db)
        assert column in str(caught.value)
    finally:
        rb_writer.close_db(db)
    row = _content(acknowledged)["101"]
    assert str(row[LINK]) == str(BINDING) and row[ISRC] is None


def test_a_plan_writing_one_column_admits_only_that_one_to_the_guard(acknowledged, monkeypatch):
    """The policy is built from the columns written, so a ContentLink only plan
    that also sets an ISRC beside it is refused by the guard before the commit."""
    seed(acknowledged)
    real = rb_writer.write_metadata_field

    def and_an_isrc(row, owner, field_name, new_value, **kwargs):
        row.ISRC = ""
        return real(row, owner, field_name, new_value, **kwargs)

    monkeypatch.setattr(rb_writer, "write_metadata_field", and_an_isrc)
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, _planned(acknowledged, f"101:{LINK}={HOUSE}"))
    assert caught.value.cause.reason == "whitelist-violation"
    row = _content(acknowledged)["101"]
    assert str(row[LINK]) == str(BINDING) and row[ISRC] is None


def test_a_tempo_moved_beside_the_write_is_refused_by_the_guard(acknowledged, monkeypatch):
    """The probe's policy admits its columns only. A tempo set in the same
    commit is refused before it, and nothing is written."""
    seed(acknowledged)
    real = rb_writer.write_metadata_field

    def and_a_tempo(row, owner, field_name, new_value, **kwargs):
        row.BPM = 12800
        return real(row, owner, field_name, new_value, **kwargs)

    monkeypatch.setattr(rb_writer, "write_metadata_field", and_a_tempo)
    with pytest.raises(CratekitError) as caught:
        _apply(acknowledged, _planned(acknowledged, f"101:{LINK}={HOUSE}", f"101:{ISRC}="))
    assert caught.value.cause.reason == "whitelist-violation"
    row = _content(acknowledged)["101"]
    assert str(row[LINK]) == str(BINDING) and row["BPM"] == 0 and row[ISRC] is None


def test_a_policy_registered_before_the_apply_survives_it(acknowledged):
    seed(acknowledged)
    other = rb_writer.FieldPolicy(owner="elsewhere", fields={"Commnt": rb_writer.Ownership.OWNED})
    rb_writer.register_field_policy(other)
    _apply(acknowledged, _planned(acknowledged, f"101:{LINK}={HOUSE}"))
    assert rb_writer.registered_field_policies()["elsewhere"] is other
    assert rb_writer.ROW_PROBE_OWNER not in rb_writer.registered_field_policies()


def test_the_write_is_recorded_on_a_session_with_a_capture(acknowledged):
    from cratekit.core import session

    seed(acknowledged)
    written = _apply(acknowledged, _planned(acknowledged, f"101:{LINK}={HOUSE}", f"102:{ISRC}="))
    assert (written.written, written.rows, written.read_back) == (2, 2, 2)
    record = session.read_record(written.session_id, acknowledged)
    assert record.sources[row_link.CHANGE_KEY] == str(session.SourceState.COMMITTED)
    assert record.snapshot_path is not None


def test_apply_refuses_an_empty_watch_before_touching_the_database(acknowledged):
    seed(acknowledged)
    plan = _planned(acknowledged, f"101:{LINK}={HOUSE}")
    db = rb_writer.open_db(acknowledged.library.db_path, unlock=False, cfg=acknowledged)
    try:
        with pytest.raises(ValueError):
            row_link.apply_probes(acknowledged, db, plan, analysis_roots=[])
    finally:
        rb_writer.close_db(db)
    assert str(_content(acknowledged)["101"][LINK]) == str(BINDING)


# ═══════════════════════════════════════════════════════════════════════════
# The read back, pure
# ═══════════════════════════════════════════════════════════════════════════


def _probe(content_id="101", column=LINK, value=HOUSE, was=str(BINDING)) -> row_link.Probe:
    return row_link.Probe(
        content_id=content_id,
        title="t",
        path="p",
        column=column,
        value=value,
        was=was,
        carriers=1,
        fellows=0,
    )


def _plan_of(*probes: row_link.Probe) -> row_link.ProbePlan:
    return row_link.ProbePlan(probes=probes or (_probe(),), rows=2)


def test_judge_accepts_values_read_back_as_the_live_tables_types():
    plan = _plan_of(_probe(), _probe(column=ISRC, value="", was=None))
    before = {"101": {LINK: BINDING, ISRC: None, "BPM": 0, "updated_at": "a"}}
    after = {"101": {LINK: HOUSE, ISRC: "", "BPM": 0, "updated_at": "b"}}
    assert row_link.judge(plan, before, after) == ((), ())


def test_judge_names_a_value_that_did_not_take_and_a_column_that_moved():
    before = {"101": {LINK: BINDING, "BPM": 0}}
    after = {"101": {LINK: BINDING, "BPM": 12800}}
    wrong, moved = row_link.judge(_plan_of(), before, after)
    assert wrong == (f"101: {LINK} not {HOUSE!r}",)
    assert moved == ("101: BPM",)


def test_judge_counts_a_column_written_on_another_row_as_moved_here():
    """The planned columns are per row: an ISRC written on 102 does not excuse
    an ISRC that moved on 101, where only the ContentLink was written."""
    plan = _plan_of(_probe(), _probe(content_id="102", column=ISRC, value="", was=None))
    before = {"101": {LINK: BINDING, ISRC: None}, "102": {ISRC: None}}
    after = {"101": {LINK: HOUSE, ISRC: ""}, "102": {ISRC: ""}}
    wrong, moved = row_link.judge(plan, before, after)
    assert wrong == () and moved == ("101: ISRC",)


def test_judge_skips_a_triple_that_writes_nothing():
    plan = _plan_of(_probe(was=str(HOUSE)))
    assert plan.content_ids == []
    assert row_link.judge(plan, {}, {}) == ((), ())


def test_judge_names_a_row_that_could_not_be_read():
    wrong, moved = row_link.judge(_plan_of(), {}, {})
    assert wrong == ("101: the row could not be read",) and moved == ()


def test_assert_read_back_refuses_a_moved_column_as_the_guards_defect():
    with pytest.raises(CratekitError) as caught:
        row_link.assert_read_back(
            row_link.Written(session_id="s", written=1, rows=1, read_back=1, moved=("101: BPM",))
        )
    assert caught.value.cause.reason == "whitelist-violation"
    assert "restore session s" in " ".join(caught.value.cause.remediation.steps)


def test_assert_read_back_refuses_a_wrong_value():
    with pytest.raises(CratekitError) as caught:
        row_link.assert_read_back(
            row_link.Written(session_id="s", written=1, rows=1, read_back=0, wrong=("101: x",))
        )
    assert caught.value.cause.reason == "internal-error"


def test_assert_read_back_passes_a_clean_write():
    row_link.assert_read_back(row_link.Written(session_id="s", written=1, rows=1, read_back=1))
