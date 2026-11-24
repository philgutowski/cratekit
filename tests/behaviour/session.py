"""The session package's scenarios: the acknowledgment, the release and the three restore verbs (U311).

On the restore suite's library, `restore bare-metal` onto a stand in mount point.
"""

from __future__ import annotations

from cratekit.core import config, restore, session
from cratekit.core.exit_codes import ExitCode
from tests.test_restore import acknowledge, completed_session
from tests.test_restore import cfg as cfg  # noqa: PLC0414
from tests.test_restore_cli import CONFIRM, _fake_rclone, _replacement
from tests.test_restore_cli import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore_cli import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_restore_cli import installed as installed  # noqa: PLC0414
from tests.test_restore_cli import lost as lost  # noqa: PLC0414
from tests.test_session_cli import ACK_GATE, RELEASE_GATE, _before_a_power_loss, _left_by
from tests.test_session_cli import at_a_terminal as at_a_terminal  # noqa: PLC0414
from tests.test_write_session import _lock_recording

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)

#: The process a previous boot's holder names, fixed so two captures agree.
GONE_PID = 4242


def _through_the_gate(stage, gate: str, option: str, *argv: str):
    """Ask, decide and resume, each through the stage, and return the resume."""
    refused = stage.json(*argv)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, gate, option).code == OK
    return stage.json("--run", run_id, *argv)


def test_session_ack_through_its_gate(stage, installed, at_a_terminal):
    """The question in a person's rendering, an abort that records nothing, then the mint."""
    assert stage.crate("session", "ack").code == ASKED
    aborted = _through_the_gate(stage, ACK_GATE, "abort", "session", "ack")
    assert aborted.code == OK, aborted.stdout
    minted = _through_the_gate(stage, ACK_GATE, "acknowledged", "session", "ack")
    assert minted.code == OK, minted.stdout
    assert minted.envelope["data"]["summary"]["recorded"] is True
    assert stage.crate("session", "ack").code == ASKED


def test_session_release_through_its_gate(stage, installed, at_a_terminal, monkeypatch):
    """Nothing held, released and aborted; then a power loss's lock and record, released."""
    assert stage.crate("session", "release").code == ASKED
    quiet = _through_the_gate(stage, RELEASE_GATE, "release", "session", "release")
    assert quiet.code == OK, quiet.stdout
    assert quiet.envelope["outcome"] == "no_op"
    aborted = _through_the_gate(stage, RELEASE_GATE, "abort", "session", "release")
    assert aborted.code == OK, aborted.stdout

    dead = _before_a_power_loss(monkeypatch, pid=GONE_PID)
    assert session.holder_alive(dead) is False
    _lock_recording(installed, dead)
    session_id = _left_by(installed, dead, session.SessionState.OPEN)
    assert stage.crate("session", "release").code == ASKED
    released = _through_the_gate(stage, RELEASE_GATE, "release", "session", "release")
    assert released.code == OK, released.stdout
    assert released.envelope["data"]["summary"]["abandoned"] == [session_id]


def test_restore_run_puts_the_snapshot_back(stage, installed, monkeypatch):
    """`crate restore list`, a restore through its two acts, and the list again."""
    acknowledge(installed)
    record, _captured = completed_session(installed)
    database = config.state_path("rekordbox_db", installed)
    before = database.read_bytes()
    database.write_bytes(b"database, generation two")

    assert stage.crate("restore", "list").code == OK
    assert stage.json("restore", "list").code == OK
    assert stage.crate("restore", "run", record.session_id, "--dry-run").code == ASKED
    rehearsed = _through_the_gate(
        stage, CONFIRM, "restore", "restore", "run", record.session_id, "--dry-run"
    )
    assert rehearsed.code == OK, rehearsed.stdout
    assert stage.crate("restore", "run", record.session_id).code == ASKED
    restored = _through_the_gate(stage, CONFIRM, "restore", "restore", "run", record.session_id)
    assert restored.code == OK, restored.stdout
    assert database.read_bytes() == before
    assert stage.crate("restore", "list").code == OK
    assert stage.json("restore", "list").code == OK


def test_restore_run_with_nothing_to_restore(stage, installed):
    """A library with no write session: the listing is empty and the restore is an outcome."""
    assert stage.crate("restore", "list").code == OK
    assert stage.json("restore", "list").code == OK
    assert stage.crate("restore", "run").code == ASKED
    walked = _through_the_gate(stage, CONFIRM, "restore", "restore", "run")
    assert walked.code == OK, walked.stdout
    assert walked.envelope["outcome"] == "no_op"


def test_restore_bare_metal_onto_a_replacement(stage, lost, monkeypatch, tmp_path):
    """Refused without the acceptance flag, then both halves recovered, and the rehearsal."""
    target = _replacement(tmp_path)
    log = _fake_rclone(lost, monkeypatch)

    refused = stage.json("restore", "bare-metal", "--target", target)
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    stage.crate("restore", "bare-metal", "--target", target)
    rehearsed = stage.json(
        "restore", "bare-metal", "--target", target, "--accept-replacement", "--dry-run"
    )
    assert rehearsed.code == OK, rehearsed.stdout
    recovered = stage.json("restore", "bare-metal", "--target", target, "--accept-replacement")
    assert recovered.code == OK, recovered.stdout
    assert recovered.envelope["data"]["totals"]["database_transfers"] == 1
    assert "copy " in log.read_text()


def test_restore_bare_metal_refused_while_the_library_is_mounted(
    stage, installed, monkeypatch, tmp_path
):
    """The library is still here, so there is nothing to recover from bare metal."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    monkeypatch.setattr(restore, "_is_mount_point", lambda _path: True)
    target = _replacement(tmp_path)
    _fake_rclone(installed, monkeypatch)

    refused = stage.json("restore", "bare-metal", "--target", target, "--accept-replacement")
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    stage.crate("restore", "bare-metal", "--target", target, "--accept-replacement")
