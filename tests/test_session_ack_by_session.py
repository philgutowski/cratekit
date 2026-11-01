"""U138: the session mints the backup acknowledgment on the five day rule, with no terminal.

Decided by the author on 2026-10-09, the bound set at five days on 2026-10-10.
When the run record holds the gate's answer under the actor ``session``, the
terminal check is replaced by the age rule: every backup portion under five
days old mints, anything else is refused by name. A person's answer keeps the
terminal check. The record says which rule minted it.

Driven through the real dispatcher, three invocations each as R34 shapes them,
with nobody at a terminal. The backup ages are recorded through the fact file's
own writer. Every library here is a temporary one; no real backup is read.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from cratekit.core import backup_facts, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests import test_session_cli as session_suite
from tests.test_session_cli import (  # noqa: F401
    ACK_GATE,
    _drive,
    _nothing_is_running,
    _release_process_locks,
    at_a_terminal,
    installed,
)

#: The configured, saved library fixture, by assignment for the reason
#: ``tests/test_session_cli.py`` gives for its own.
cfg = session_suite.cfg

#: The actor a session answers under, spelled as the author's rule spells it.
SESSION = "session"
#: The bound, spelled as the rule spells it rather than read off the engine.
FIVE_DAYS = timedelta(days=5)


@pytest.fixture
def nobody_at_a_terminal(installed, monkeypatch):  # noqa: F811
    """The library, and no controlling terminal: a session running unattended."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: False)
    return installed


def _backed_up(cfg, **ages: timedelta) -> None:
    """Record each named portion as completed that long ago, through the fact writer."""
    now = datetime.now(UTC)
    for portion, age in ages.items():
        backup_facts.record(
            cfg,
            backup_facts.Portion(portion),
            completed_at=now - age,
            destination="/backups/probe",
        )


def _answered_by(actor: str) -> tuple[int, dict]:
    """Ask, answer as ``actor`` with run decide, and drive the mint."""
    code, refused = _drive(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, decided = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--actor", actor])
    assert code == int(ExitCode.OK), decided
    return _drive(["--run", run_id, "session", "ack"])


def test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days(
    nobody_at_a_terminal,
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=2), database=timedelta(days=4, hours=23))

    code, envelope = _answered_by(SESSION)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["recorded"] is True
    assert (summary["rule"], summary["decided_by"]) == ("session-ages", SESSION)
    kept = session.read_acknowledgment(cfg)
    assert kept is not None and kept.valid_at(datetime.now(UTC))
    assert (kept.rule, kept.decided_by) == ("session-ages", SESSION)
    # The record's own actor is the process's account, never the answer's.
    assert kept.actor == session.derive_actor() != SESSION
    assert {entry.portion for entry in kept.shown} == {"files", "database"}


@pytest.mark.parametrize(
    ("ages", "named"),
    [
        ({"files": timedelta(days=6), "database": timedelta(days=1)}, "files portion is 6.0 days old"),
        ({"files": timedelta(days=1), "database": FIVE_DAYS}, "database portion is 5.0 days old"),
        ({"files": timedelta(days=1)}, "database portion's age is not known (never-recorded)"),
        (
            {"files": timedelta(days=1), "database": -timedelta(days=2)},
            "database portion's age is not known (recorded-in-the-future)",
        ),
    ],
    ids=[
        "files-six-days",
        "database-exactly-five",
        "database-never-recorded",
        "database-recorded-in-the-future",
    ],
)
def test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown(
    nobody_at_a_terminal, ages, named
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, **ages)

    code, envelope = _answered_by(SESSION)

    assert code == int(ExitCode.ACK_REQUIRED), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "backup-acknowledgment-backup-too-old", cause
    assert named in cause["message"], cause["message"]
    assert "run a backup first" in cause["message"]
    assert cause["remediation"]["remedy"] == "run-backup", cause
    assert session.read_acknowledgment(cfg) is None


def test_a_session_with_a_terminal_is_still_held_to_the_ages(installed):  # noqa: F811
    """The age rule is the session's whatever the terminal says."""
    _backed_up(installed, files=timedelta(days=9), database=timedelta(days=1))

    code, envelope = _answered_by(SESSION)

    assert code == int(ExitCode.ACK_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "backup-acknowledgment-backup-too-old", envelope
    assert session.read_acknowledgment(installed) is None


def test_a_person_without_a_terminal_is_still_refused_over_fresh_backups(nobody_at_a_terminal):
    """The age rule widens the session's answer and nobody else's."""
    _backed_up(nobody_at_a_terminal, files=timedelta(days=1), database=timedelta(days=1))

    code, envelope = _answered_by("a-person")

    assert code == int(ExitCode.ACK_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "backup-acknowledgment-no-terminal", envelope
    assert session.read_acknowledgment(nobody_at_a_terminal) is None


def test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so(
    installed,  # noqa: F811
):
    """Old backups do not stop a person: their path is today's, ages shown, not judged."""
    _backed_up(installed, files=timedelta(days=30), database=timedelta(days=30))

    code, envelope = _answered_by("a-person")

    assert code == int(ExitCode.OK), envelope
    kept = session.read_acknowledgment(installed)
    assert (kept.rule, kept.decided_by) == ("terminal", "a-person")


def test_a_record_written_before_u138_reads_as_the_terminal_rule():
    """A record with neither key is what every acknowledgment was before this unit."""
    now = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
    older = {
        "schema_version": session.ACK_SCHEMA_VERSION,
        "actor": "someone@somewhere",
        "recorded_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=12)).isoformat(),
        "shown": [],
    }
    read = session.Acknowledgment.from_json(older)
    assert (read.rule, read.decided_by) == ("terminal", None)
    assert session.Acknowledgment.from_json(read.to_json()) == read


@pytest.mark.parametrize(
    ("age", "mints"),
    [(FIVE_DAYS - timedelta(seconds=1), True), (FIVE_DAYS, False)],
    ids=["a-second-under-five-days", "exactly-five-days"],
)
def test_the_bound_is_strict_at_exactly_five_days(cfg, age, mints):
    """On one clock, so "exactly" means exactly. Through the dispatcher the
    verb reads the clock a moment after the fact was written, which makes a
    five day fixture a little over and cannot tell under from at."""
    now = datetime(2026, 10, 12, 12, 0, tzinfo=UTC)
    for portion in backup_facts.Portion:
        backup_facts.record(cfg, portion, completed_at=now - age, destination="/backups/probe")
    if mints:
        kept = session.record_acknowledgment(cfg, now=now, decided_by=SESSION)
        assert (kept.rule, kept.decided_by) == ("session-ages", SESSION)
    else:
        with pytest.raises(CratekitError) as refused:
            session.record_acknowledgment(cfg, now=now, decided_by=SESSION)
        assert refused.value.cause.reason == "backup-acknowledgment-backup-too-old"
        assert session.read_acknowledgment(cfg) is None


def test_the_bound_is_five_days_as_the_author_set_it():
    assert session.SESSION_MAX_BACKUP_AGE == FIVE_DAYS


# ---------------------------------------------------------------------------
# U184: ``crate session ack --as session``, the session's mint in one command.
#
# Filed from the friction review of sitting 51: three invocations and a wrong
# turn at each became one. The age rule above is the only guard, and the flag
# reaches it with no gate, so every drive below is ONE invocation with nobody
# at a terminal, and every one ends with no run left waiting on an answer.
# ---------------------------------------------------------------------------

#: The one command, spelled as a session types it.
ONE_COMMAND = ["session", "ack", "--as", SESSION]


def _waiting_runs() -> list[str]:
    """Every recorded run still waiting on a gate or a person, by identifier."""
    from cratekit.cli import gates

    directory = gates.run_dir()
    if not directory.is_dir():
        return []
    waiting = []
    for path in sorted(directory.glob("*.json")):
        state = gates.load(path.stem)
        if state.open_gate is not None or state.pending is not None:
            waiting.append(state.run_id)
    return waiting


def test_one_command_mints_as_the_session_when_both_ages_are_four_days(
    nobody_at_a_terminal,
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=4), database=timedelta(days=4))

    code, envelope = _drive(ONE_COMMAND)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["recorded"], summary["already_valid"]) == (True, False)
    assert (summary["rule"], summary["decided_by"]) == ("session-ages", SESSION)
    kept = session.read_acknowledgment(cfg)
    assert kept is not None and kept.valid_at(datetime.now(UTC))
    assert (kept.rule, kept.decided_by) == ("session-ages", SESSION)
    assert kept.actor == session.derive_actor() != SESSION
    assert summary["expires_at"] == kept.expires_at.isoformat()
    assert {entry.portion for entry in kept.shown} == {"files", "database"}
    assert _waiting_runs() == []


def test_one_command_prints_the_expiry_a_person_reads(nobody_at_a_terminal):
    """The default renderer prints check rows and not the summary."""
    _backed_up(nobody_at_a_terminal, files=timedelta(days=1), database=timedelta(days=1))

    code, text = session_suite._human(ONE_COMMAND)

    assert code == int(ExitCode.OK), text
    kept = session.read_acknowledgment(nobody_at_a_terminal)
    assert "backup.acknowledgment: recorded now, by the session-ages rule" in text, text
    assert f"valid until {kept.expires_at.isoformat()}" in text, text
    assert "backup.age.files" in text and "backup.age.database" in text, text


@pytest.mark.parametrize(
    ("ages", "named"),
    [
        ({"files": FIVE_DAYS, "database": timedelta(days=4)}, "files portion is 5.0 days old"),
        ({"files": timedelta(days=4), "database": FIVE_DAYS}, "database portion is 5.0 days old"),
        ({"files": timedelta(days=4)}, "database portion's age is not known (never-recorded)"),
        ({}, "files portion's age is not known (never-recorded)"),
    ],
    ids=["files-five-days", "database-five-days", "database-unknown", "both-unknown"],
)
def test_one_command_refuses_naming_the_portion_and_records_nothing(
    nobody_at_a_terminal, ages, named
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, **ages)

    code, envelope = _drive(ONE_COMMAND)

    assert code == int(ExitCode.ACK_REQUIRED), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "backup-acknowledgment-backup-too-old", cause
    assert named in cause["message"], cause["message"]
    assert cause["remediation"]["remedy"] == "run-backup", cause
    assert session.read_acknowledgment(cfg) is None
    assert _waiting_runs() == []


def test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again(
    nobody_at_a_terminal,
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=1), database=timedelta(days=1))
    code, first = _drive(ONE_COMMAND)
    assert code == int(ExitCode.OK), first
    written = session.ack_path(cfg).read_bytes()

    code, second = _drive(ONE_COMMAND)

    assert code == int(ExitCode.OK), second
    assert second["outcome"] == "no_op", second
    summary = second["data"]["summary"]
    assert (summary["recorded"], summary["already_valid"]) == (False, True)
    assert summary["expires_at"] == first["data"]["summary"]["expires_at"]
    assert session.ack_path(cfg).read_bytes() == written
    rows = second["data"]["checks"]
    assert [row["key"] for row in rows] == ["backup.acknowledgment"], rows
    assert "already on record, not minted again" in rows[0]["detail"], rows
    assert _waiting_runs() == []


def test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups(installed):  # noqa: F811
    """Valid is what every destructive verb's gate accepts, whoever minted it."""
    _backed_up(installed, files=timedelta(days=30), database=timedelta(days=30))
    code, envelope = _answered_by("a-person")
    assert code == int(ExitCode.OK), envelope
    written = session.ack_path(installed).read_bytes()

    code, envelope = _drive(ONE_COMMAND)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["rule"] == "terminal", envelope
    assert envelope["data"]["summary"]["already_valid"] is True, envelope
    assert session.ack_path(installed).read_bytes() == written


def test_an_expired_acknowledgment_is_replaced_by_one_command(nobody_at_a_terminal):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=1), database=timedelta(days=1))
    earlier = datetime.now(UTC) - timedelta(hours=13)
    lapsed = session.record_acknowledgment(cfg, now=earlier, decided_by=SESSION)
    assert not lapsed.valid_at(datetime.now(UTC))

    code, envelope = _drive(ONE_COMMAND)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["recorded"] is True, envelope
    kept = session.read_acknowledgment(cfg)
    assert kept.recorded_at > lapsed.recorded_at and kept.valid_at(datetime.now(UTC))


def test_an_unreadable_acknowledgment_is_replaced_by_one_command(nobody_at_a_terminal):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=1), database=timedelta(days=1))
    path = session.ack_path(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json")

    code, envelope = _drive(ONE_COMMAND)

    assert code == int(ExitCode.OK), envelope
    assert session.read_acknowledgment(cfg).rule == "session-ages"


def test_without_the_flag_the_gate_still_appears(nobody_at_a_terminal):
    """The default road is today's: the explicit gate, and a run that waits on it."""
    _backed_up(nobody_at_a_terminal, files=timedelta(days=1), database=timedelta(days=1))

    code, envelope = _drive(["session", "ack"])

    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert _waiting_runs() == [envelope["run_id"]]
    assert session.read_acknowledgment(nobody_at_a_terminal) is None


@pytest.mark.parametrize("named", ["a-person", "cli", "Session"])
def test_the_flag_names_no_actor_but_the_session(nobody_at_a_terminal, named, capsys):
    """The one value it takes is a rule selector, so no caller can name a person."""
    _backed_up(nobody_at_a_terminal, files=timedelta(days=1), database=timedelta(days=1))

    code, text = session_suite._human(["session", "ack", "--as", named])

    assert code == int(ExitCode.USAGE), text
    assert f"invalid choice: '{named}'" in capsys.readouterr().err
    assert session.read_acknowledgment(nobody_at_a_terminal) is None
