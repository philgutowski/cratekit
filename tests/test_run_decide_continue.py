"""U168: answering a gate is one command that records the answer and continues the run.

``crate run decide RUN GATE OPTION --continue`` records the answer, then
continues the verb that owns the run with the arguments its first invocation
recorded and ``--run RUN``, and answers with that verb's result. With no
``--actor`` the answer is recorded as ``session`` when the invocation has no
controlling terminal and as ``cli`` when it has one. An explicit gate still
takes no inline answer on the verb itself.

Driven through the real dispatcher. The acknowledgment is the gate sitting 47
spent four commands on; its ages are recorded through the fact file's own
writer, on a temporary library. D1 applies.
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from cratekit.cli import gates
from cratekit.cli.verbs import runs
from cratekit.core import session
from cratekit.core.exit_codes import ExitCode
from tests import test_session_cli as session_suite
from tests.test_session_ack_by_session import _backed_up
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


@pytest.fixture
def nobody_at_a_terminal(installed, monkeypatch):  # noqa: F811
    """The library, and no controlling terminal: a session running unattended."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: False)
    return installed


def _asked() -> str:
    code, refused = _drive(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused["run_id"]


# ---------------------------------------------------------------------------
# One command per gate
# ---------------------------------------------------------------------------


def test_a_session_answers_and_mints_in_one_command_with_no_actor_given(nobody_at_a_terminal):
    """Sitting 47's four commands are two: the question, and the answer that continues."""
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=2), database=timedelta(days=4))
    run_id = _asked()

    code, envelope = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--continue"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["verb"] == "session.ack" and envelope["run_id"] == run_id
    summary = envelope["data"]["summary"]
    assert summary["recorded"] is True
    assert summary["decided_by"] == "session"
    assert summary["rule"] == session.RULE_SESSION_AGES
    (note,) = [w for w in envelope["warnings"] if w["code"] == runs.DECISION_RECORDED]
    assert f"{ACK_GATE} answered acknowledged as session on run {run_id}" in note["message"]
    assert "session ack continued" in note["message"]
    assert session.read_acknowledgment(cfg) is not None


def test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer(
    nobody_at_a_terminal,
):
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=2), database=timedelta(days=6))
    run_id = _asked()

    code, envelope = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--continue"])

    assert code != int(ExitCode.OK), envelope
    assert envelope["verb"] == "session.ack"
    assert session.read_acknowledgment(cfg) is None
    assert gates.load(run_id).decisions[ACK_GATE].actor == "session"


def test_the_continuation_is_given_the_arguments_its_first_invocation_recorded(
    nobody_at_a_terminal,
):
    """The global options are the dispatcher's, not the verb's, and are not kept."""
    run_id = _asked()

    state = gates.load(run_id)

    assert state.argv == ("session", "ack")


def test_a_run_that_keeps_no_command_line_is_refused_with_the_answer_recorded(
    nobody_at_a_terminal,
):
    """A run recorded before this unit has nothing to continue with."""
    run_id = _asked()
    state = gates.load(run_id)
    state.argv = None
    gates.save(state)

    code, envelope = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--continue"])

    # NOT A GATE: the answer is recorded, so nothing offers to answer it again.
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "run-not-continuable"
    assert not envelope.get("resumable"), envelope
    assert f"crate --run {run_id} session ack" in envelope["cause"]["remediation"]["steps"][0]
    assert gates.load(run_id).decisions[ACK_GATE].option == "acknowledged"


# ---------------------------------------------------------------------------
# Who answered, by default
# ---------------------------------------------------------------------------


def test_with_no_terminal_and_no_actor_the_answer_is_the_sessions(nobody_at_a_terminal):
    run_id = _asked()

    code, envelope = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["actor"] == "session"
    assert "no controlling terminal" in envelope["data"]["summary"]["actor_because"]
    assert gates.load(run_id).decisions[ACK_GATE].actor == "session"


def test_at_a_terminal_and_no_actor_the_answer_is_the_command_lines(installed):  # noqa: F811
    run_id = _asked()

    code, envelope = _drive(["run", "decide", run_id, ACK_GATE, "acknowledged"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["actor"] == "cli"
    assert gates.load(run_id).decisions[ACK_GATE].actor == "cli"


def test_an_actor_given_is_recorded_whatever_the_terminal(nobody_at_a_terminal):
    run_id = _asked()

    _drive(["run", "decide", run_id, ACK_GATE, "acknowledged", "--actor", "a-person"])

    assert gates.load(run_id).decisions[ACK_GATE].actor == "a-person"


# ---------------------------------------------------------------------------
# The explicit gate is unchanged
# ---------------------------------------------------------------------------


def test_an_explicit_gate_still_refuses_an_inline_answer_on_the_verb(nobody_at_a_terminal):
    """--continue belongs to the separate run decide call, never to the verb's own."""
    cfg = nobody_at_a_terminal
    _backed_up(cfg, files=timedelta(days=2), database=timedelta(days=4))

    code, envelope = _drive(["-d", f"{ACK_GATE}=acknowledged", "session", "ack"])

    assert code != int(ExitCode.OK), envelope
    assert session.read_acknowledgment(cfg) is None
