"""The app mints the backup acknowledgment by the session's age rule, recorded as ``app`` (U962).

``crate session ack --as app`` mints in one command only while both backup ages
are under five days, and a ``run decide --actor app`` answer to the gate mints
by the same rule. The app is never given the terminal rule, which checks no
age, whatever the terminal says. D1 applies.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from cratekit.cli import gates
from cratekit.core import backup_facts, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests import test_session_cli as session_suite
from tests._sync_builders import exited
from tests.test_session_ack_by_session import _backed_up, _refused_too_old, _waiting_runs
from tests.test_session_cli import (  # noqa: F401
    ACK_GATE,
    _drive,
    _nothing_is_running,
    _release_process_locks,
    at_a_terminal,
    installed,
)

#: The configured, saved library fixture, assigned for the reason
#: ``tests/test_session_cli.py`` gives.
cfg = session_suite.cfg

#: The actor the app answers as, spelled as the brief spells it.
APP = "app"
#: The one command, spelled as the app runs it.
ONE_COMMAND = ["session", "ack", "--as", APP]
FOUR_DAYS = timedelta(days=4)
FIVE_DAYS = timedelta(days=5)
#: Old enough that only the terminal rule would mint over it.
A_MONTH = timedelta(days=30)


@pytest.fixture
def nobody_at_a_terminal(installed, monkeypatch):  # noqa: F811
    """The library, and no controlling terminal: the app runs crate with none."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: False)
    return installed


def _minted_by_the_app(cfg, summary: dict) -> session.Acknowledgment:
    """The summary and the record both say the app minted it by the ages rule: the record."""
    assert summary["recorded"] is True
    assert (summary["rule"], summary["decided_by"]) == ("session-ages", APP)
    kept = session.read_acknowledgment(cfg)
    assert kept is not None and kept.valid_at(datetime.now(UTC))
    assert (kept.rule, kept.decided_by) == ("session-ages", APP)
    # The record's own actor is the process's account, never the answer's.
    assert kept.actor == session.derive_actor() != APP
    assert {entry.portion for entry in kept.shown} == {"files", "database"}
    assert json.loads(session.ack_path(cfg).read_text())["decided_by"] == APP
    return kept


def _answered_by_the_app() -> tuple[str, tuple[int, dict]]:
    """Ask, answer as the app with run decide and no digest, and drive the mint."""
    run_id = exited(_drive(["session", "ack"]), ExitCode.DECISION_REQUIRED)["run_id"]
    exited(_drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--actor", APP]))
    return run_id, _drive(["--run", run_id, "session", "ack"])


# One command


def test_one_command_mints_as_the_app_when_both_ages_are_four_days(nobody_at_a_terminal):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=FOUR_DAYS, database=FOUR_DAYS)

    summary = exited(_drive(ONE_COMMAND))["data"]["summary"]
    assert (summary["recorded"], summary["already_valid"]) == (True, False)
    kept = _minted_by_the_app(cfg, summary)
    assert summary["expires_at"] == kept.expires_at.isoformat()
    assert _waiting_runs() == []


@pytest.mark.parametrize(
    ("ages", "named"),
    [
        ({"files": FIVE_DAYS, "database": FOUR_DAYS}, "files portion is 5.0 days old"),
        ({"files": FOUR_DAYS, "database": FIVE_DAYS}, "database portion is 5.0 days old"),
        ({"files": FOUR_DAYS}, "database portion's age is not known (never-recorded)"),
        ({}, "files portion's age is not known (never-recorded)"),
    ],
    ids=["files-five-days", "database-five-days", "database-unknown", "both-unknown"],
)
def test_one_command_refuses_naming_the_portion_and_records_nothing(
    nobody_at_a_terminal, ages, named
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, **ages)

    envelope = exited(_drive(ONE_COMMAND), ExitCode.ACK_REQUIRED)
    _refused_too_old(cfg, envelope, named)
    assert envelope["cause"]["message"].startswith(
        "the app mints the backup acknowledgment only while every backup portion is under 5 days old"
    )
    assert _waiting_runs() == []


def test_the_app_at_a_terminal_is_still_held_to_the_ages(installed):  # noqa: F811
    """A terminal does not hand the app the terminal rule, which would mint over a month."""
    _backed_up(installed, files=A_MONTH, database=A_MONTH)

    envelope = exited(_drive(ONE_COMMAND), ExitCode.ACK_REQUIRED)
    _refused_too_old(installed, envelope, "files portion is 30.0 days old")


def test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again(
    nobody_at_a_terminal,
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=FOUR_DAYS, database=FOUR_DAYS)
    first = exited(_drive(ONE_COMMAND))
    written = session.ack_path(cfg).read_bytes()

    second = exited(_drive(ONE_COMMAND))
    assert second["outcome"] == "no_op", second
    summary = second["data"]["summary"]
    assert (summary["recorded"], summary["already_valid"]) == (False, True)
    assert summary["decided_by"] == APP
    assert summary["expires_at"] == first["data"]["summary"]["expires_at"]
    assert session.ack_path(cfg).read_bytes() == written
    assert _waiting_runs() == []


def test_one_command_prints_the_rule_and_the_expiry_a_person_reads(nobody_at_a_terminal):
    _backed_up(nobody_at_a_terminal, files=FOUR_DAYS, database=FOUR_DAYS)

    text = exited(session_suite._human(ONE_COMMAND))
    kept = session.read_acknowledgment(nobody_at_a_terminal)
    assert "backup.acknowledgment: recorded now, by the session-ages rule" in text, text
    assert f"valid until {kept.expires_at.isoformat()}" in text, text


@pytest.mark.parametrize("named", ["App", "APP", "the-app"])
def test_the_flag_takes_the_app_by_its_exact_name_only(nobody_at_a_terminal, named, capsys):
    _backed_up(nobody_at_a_terminal, files=FOUR_DAYS, database=FOUR_DAYS)

    exited(session_suite._human(["session", "ack", "--as", named]), ExitCode.USAGE)
    assert f"invalid choice: '{named}'" in capsys.readouterr().err
    assert session.read_acknowledgment(nobody_at_a_terminal) is None


def test_the_sessions_one_command_is_unchanged(nobody_at_a_terminal):
    """The session's mint records the session and its refusal keeps its words."""
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=FOUR_DAYS, database=FIVE_DAYS)

    envelope = exited(_drive(["session", "ack", "--as", "session"]), ExitCode.ACK_REQUIRED)
    assert envelope["cause"]["message"].startswith(
        "a session mints the backup acknowledgment only while every backup portion is under 5 days old"
    )
    _backed_up(cfg, database=FOUR_DAYS)
    summary = exited(_drive(["session", "ack", "--as", "session"]))["data"]["summary"]
    assert summary["decided_by"] == "session"


# The gate, answered by the app


def test_the_app_answers_the_gate_with_no_digest_and_the_mint_takes_the_ages_rule(
    nobody_at_a_terminal,
):
    """The gate binds no plan, so the app's answer needs no digest; the mint is by ages."""
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=FOUR_DAYS, database=timedelta(days=1))

    run_id, minted = _answered_by_the_app()
    _minted_by_the_app(cfg, exited(minted)["data"]["summary"])


def test_the_apps_answer_reads_as_the_apps_in_run_show(nobody_at_a_terminal):
    run_id = exited(_drive(["session", "ack"]), ExitCode.DECISION_REQUIRED)["run_id"]
    exited(_drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--actor", APP]))

    rows = {row["key"]: row for row in exited(_drive(["run", "show", run_id]))["data"]["checks"]}
    assert rows[f"gate.{ACK_GATE}"]["detail"] == "acknowledged (recorded by app)"
    assert gates.load(run_id).decisions[ACK_GATE].actor == APP


@pytest.mark.parametrize("fixture", ["nobody_at_a_terminal", "installed"])
def test_the_apps_answer_over_old_backups_is_refused_with_or_without_a_terminal(
    request, fixture
):
    """Never the terminal rule, and never the no terminal refusal: the ages decide."""
    cfg = request.getfixturevalue(fixture)
    _backed_up(cfg, files=A_MONTH, database=timedelta(days=1))

    _, minted = _answered_by_the_app()
    _refused_too_old(cfg, exited(minted, ExitCode.ACK_REQUIRED), "files portion is 30.0 days old")


def test_a_person_without_a_terminal_is_still_refused_as_before(nobody_at_a_terminal):
    """The ages rule widens the session's answer and the app's, and nobody else's."""
    _backed_up(nobody_at_a_terminal, files=timedelta(days=1), database=timedelta(days=1))

    run_id = exited(_drive(["session", "ack"]), ExitCode.DECISION_REQUIRED)["run_id"]
    exited(_drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--actor", "the-app"]))
    envelope = exited(_drive(["--run", run_id, "session", "ack"]), ExitCode.ACK_REQUIRED)
    assert envelope["cause"]["reason"] == "backup-acknowledgment-no-terminal", envelope


# The engine


@pytest.mark.parametrize(
    ("age", "mints"),
    [(FIVE_DAYS - timedelta(seconds=1), True), (FIVE_DAYS, False)],
    ids=["a-second-under-five-days", "exactly-five-days"],
)
def test_the_apps_bound_is_strict_at_exactly_five_days(cfg, age, mints):
    now = datetime(2026, 11, 25, 12, 0, tzinfo=UTC)
    for portion in backup_facts.Portion:
        backup_facts.record(cfg, portion, completed_at=now - age, destination="/backups/probe")
    if mints:
        kept = session.record_acknowledgment(cfg, now=now, decided_by=APP)
        assert (kept.rule, kept.decided_by) == ("session-ages", APP)
    else:
        with pytest.raises(CratekitError) as refused:
            session.record_acknowledgment(cfg, now=now, decided_by=APP)
        assert refused.value.cause.reason == "backup-acknowledgment-backup-too-old"
        assert session.read_acknowledgment(cfg) is None


def test_a_terminal_never_hands_the_app_the_terminal_rule(cfg):
    """The terminal seam says yes, and the ages still refuse."""
    now = datetime(2026, 11, 25, 12, 0, tzinfo=UTC)
    for portion in backup_facts.Portion:
        backup_facts.record(cfg, portion, completed_at=now - A_MONTH, destination="/backups/probe")
    with pytest.raises(CratekitError) as refused:
        session.record_acknowledgment(cfg, now=now, decided_by=APP, terminal=lambda: True)
    assert refused.value.cause.reason == "backup-acknowledgment-backup-too-old"


def test_the_app_is_named_as_the_brief_names_it():
    assert session.APP_ACTOR == APP
