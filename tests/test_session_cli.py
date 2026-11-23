"""U49: the two session verbs, driven through the dispatcher rather than the API.

Every property goes through ``cli.run``: an acknowledgment is minted by driving
``crate session ack`` and answering its gate, never by calling
``record_acknowledgment``, and the end to end test spends it on a real
destructive verb. Every fixture is a temporary directory, shared with
``tests/test_restore.py`` by assignment.
"""

from __future__ import annotations

import io
import json
import os
import signal
import stat
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core import backup_facts, config, preflight, rb_writer, session
from cratekit.core.exit_codes import ExitCode, Remedy
from tests import test_restore as restore_suite
from tests.test_restore import completed_session
from tests.test_session_log_unlisted import _refuse_listing
from tests.test_write_session import _lock_recording

#: The configured, saved library fixture, by assignment so a test parameter of
#: the same name does not shadow an import.
cfg = restore_suite.cfg

#: The two declared gate names, spelled once.
ACK_GATE = "session.ack.backup"
RELEASE_GATE = "session.release.confirm"


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    """No rekordbox process, injected, so no test depends on this machine."""
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def at_a_terminal(monkeypatch):
    """A person is sitting here, asserted rather than inherited from the launch."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)


@pytest.fixture
def installed(cfg, monkeypatch, at_a_terminal):
    """The library with only the platform seams answered; every gate still runs."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    return cfg


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Run the REAL dispatcher and return the status with the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _human(argv: list[str]) -> tuple[int, str]:
    """The same dispatcher in its DEFAULT output mode, which is what a person reads."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue() + err.getvalue()


def _answer(run_id: str, gate: str, option: str) -> None:
    """R34's second act: the decision, recorded against the run, with its actor."""
    code, envelope = _drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def _through_the_gate(verb: str, gate: str, option: str) -> tuple[int, dict, dict]:
    """Drive ``crate session VERB`` through its explicit gate, and return both halves."""
    code, refused = _drive(["session", verb])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _answer(refused["run_id"], gate, option)
    code, envelope = _drive(["--run", refused["run_id"], "session", verb])
    return code, refused, envelope


def _mint_through_the_cli(option: str = "acknowledged") -> tuple[int, dict, dict]:
    """Mint through three invocations, never through ``record_acknowledgment``."""
    return _through_the_gate("ack", ACK_GATE, option)


def _release(option: str = "release") -> tuple[int, dict, dict]:
    """Drive ``crate session release`` through its gate, and return both halves."""
    return _through_the_gate("release", RELEASE_GATE, option)


def _a_process_that_is_gone() -> session.Holder:
    """A holder naming a process this boot really started and that really exited.

    A real finished process, since ``holder_alive`` fails towards alive on a
    fabricated pid.
    """
    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    assert session.process_exists(finished.pid) is False
    here = session.current_holder()
    gone = session.Holder(host=here.host, boot=here.boot, pid=finished.pid, started="1.000")
    assert session.holder_alive(gone) is False
    return gone


# ═══════════════════════════════════════════════════════════════════════════
# session ack
# ═══════════════════════════════════════════════════════════════════════════


def test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends(installed):
    """A destructive verb refuses before the mint and completes after it."""
    record, _captured = completed_session(installed)

    def restore_run() -> tuple[int, dict]:
        _code, refused = _drive(["restore", "run", record.session_id])
        _answer(refused["run_id"], "restore.run.confirm", "restore")
        return _drive(["--run", refused["run_id"], "restore", "run", record.session_id])

    code, blocked = restore_run()
    assert blocked["cause"]["reason"] == "backup-acknowledgment-missing", blocked
    assert code == int(ExitCode.ACK_REQUIRED), blocked

    code, _refusal, minted = _mint_through_the_cli()
    assert code == int(ExitCode.OK), minted
    assert minted["data"]["summary"]["recorded"] is True

    code, envelope = restore_run()
    assert code == int(ExitCode.OK), envelope


def test_the_refusal_before_acknowledging_names_the_ages_it_consulted(installed):
    """An absent fact file shows every portion as never recorded; it does not refuse."""
    code, refused = _drive(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["ages"], "the question was asked over nothing"
    assert {entry["portion"] for entry in shown["ages"]} == {
        str(portion) for portion in backup_facts.Portion
    }
    assert all(entry["state"] == "never-recorded" for entry in shown["ages"])


def test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer(installed):
    """The default output mode renders the ages beside the question."""
    code, text = _human(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), text
    assert "Database and music files are backed up" in text
    assert "portion=database" in text
    assert "state=never-recorded" in text


def test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states(installed):
    """Absent, live, and expired are three facts with three next moves."""
    _code, refused = _drive(["session", "ack"])
    assert refused["cause"]["detail"]["shown"]["acknowledgment"] is None

    _mint_through_the_cli()
    _code, refused = _drive(["session", "ack"])
    on_record = refused["cause"]["detail"]["shown"]["acknowledgment"]
    assert on_record["valid"] is True
    assert on_record["expires_at"]

    stale = session.Acknowledgment(
        actor="somebody",
        recorded_at=datetime.now(timezone.utc) - timedelta(days=2),
        expires_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    config.atomic_write_bytes(
        json.dumps(stale.to_json()).encode("utf-8"), session.ack_path(installed)
    )
    _code, refused = _drive(["session", "ack"])
    assert refused["cause"]["detail"]["shown"]["acknowledgment"]["valid"] is False


@pytest.mark.parametrize(
    "damage, expected",
    [
        ("permission", Remedy.GRANT_PATH_ACCESS),
        ("corrupt", Remedy.REPAIR_BACKUP_FACTS),
        ("newer", Remedy.UPGRADE_CRATEKIT),
    ],
)
def test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels(
    installed, damage, expected
):
    """Each of the three conditions is made at the real file, and its remedy travels."""
    facts = backup_facts.path_for(installed)
    facts.parent.mkdir(parents=True, exist_ok=True)
    if damage == "permission":
        facts.write_text("{}")
        os.chmod(facts, 0o000)
        # Asserted rather than skipped: an account the mode bits do not restrain
        # would pass this test over a refusal that never happened.
        assert not os.access(facts, os.R_OK), (
            "this account reads a file whose mode bits forbid it, so the "
            "permission branch of read_facts is unreachable from here and this "
            "assertion would pass over a refusal that never happened. Run the "
            "battery as an unprivileged account"
        )
    elif damage == "corrupt":
        facts.write_text("this is not json")
    else:
        facts.write_text(
            json.dumps({"schema_version": backup_facts.SCHEMA_VERSION + 1, "portions": {}})
        )

    try:
        code, envelope = _drive(["session", "ack"])
    finally:
        if damage == "permission":
            os.chmod(facts, stat.S_IRUSR | stat.S_IWUSR)

    assert envelope["cause"]["reason"] == "backup-facts-unreadable", envelope
    assert envelope["cause"]["remediation"]["remedy"] == str(expected), envelope
    assert code != int(ExitCode.OK)
    assert session.read_acknowledgment(installed) is None, (
        "an acknowledgment was recorded over ages nobody could read"
    )


def test_an_inline_answer_to_the_explicit_gate_is_refused_and_records_nothing(installed):
    """R34: no answer smuggled into the command that discovered the question."""
    code, envelope = _drive(["-d", f"{ACK_GATE}=acknowledged", "session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["explicit"] is True
    assert session.read_acknowledgment(installed) is None


def test_an_inline_answer_cannot_overturn_a_recorded_abort(installed):
    """An abort a person recorded never becomes a mint, and the run stays consistent."""
    code, refused = _drive(["session", "ack"])
    run_id = refused["run_id"]
    _answer(run_id, ACK_GATE, "abort")

    code, envelope = _drive(["--run", run_id, "-d", f"{ACK_GATE}=acknowledged", "session", "ack"])
    assert session.read_acknowledgment(installed) is None, (
        "a flag on a later invocation overturned an abort a person recorded, so "
        "the explicit gate can be answered by the thing it gates (R34)"
    )
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["explicit"] is True

    # Refusing the flag must not mark the answered gate open again.
    code, shown = _drive(["run", "show", run_id])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["summary"]["open_gate"] is None, shown
    assert not [row for row in shown["data"]["checks"] if row.get("status") == "open"], shown

    # And the recorded answer still stands on its own.
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert session.read_acknowledgment(installed) is None


def test_the_answering_invocation_refuses_when_nobody_is_there(installed, monkeypatch):
    """No terminal refuses the mint, and the decision survives for a second try."""
    code, refused = _drive(["session", "ack"])
    run_id = refused["run_id"]
    _answer(run_id, ACK_GATE, "acknowledged")

    monkeypatch.setattr(session, "has_controlling_terminal", lambda: False)
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert envelope["cause"]["reason"] == "backup-acknowledgment-no-terminal", envelope
    assert code == int(ExitCode.ACK_REQUIRED), envelope
    assert session.read_acknowledgment(installed) is None

    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.OK), envelope
    assert session.read_acknowledgment(installed) is not None


def test_answering_abort_records_nothing_and_says_so(installed):
    """Aborting is an outcome a person chose, not a failure of the verb."""
    code, _refused, envelope = _mint_through_the_cli("abort")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["recorded"] is False
    assert not session.ack_path(installed).exists()


def test_a_second_mint_replaces_the_record_and_moves_the_window(installed):
    """Re-acknowledging re-mints: both moments are distinct, not merely ordered."""
    _code, _refused, first = _mint_through_the_cli()
    _code, _refused, second = _mint_through_the_cli()
    assert second["data"]["summary"]["recorded"] is True
    assert second["data"]["summary"]["recorded_at"] != first["data"]["summary"]["recorded_at"]
    assert second["data"]["summary"]["expires_at"] != first["data"]["summary"]["expires_at"]
    on_disk = session.read_acknowledgment(installed)
    assert on_disk.actor == session.derive_actor()
    assert on_disk.expires_at.isoformat() == second["data"]["summary"]["expires_at"]
    # The report says what the person was shown, read off the record written.
    assert second["data"]["summary"]["shown"] == [entry.to_json() for entry in on_disk.shown]
    assert second["data"]["summary"]["shown"], "the mint reported no ages"


# ═══════════════════════════════════════════════════════════════════════════
# session release
# ═══════════════════════════════════════════════════════════════════════════


def test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first(installed):
    """The refusal carries the recorded holder, and the answer clears it."""
    gone = _a_process_that_is_gone()
    _lock_recording(installed, gone)

    code, refused, envelope = _release()
    assert refused["cause"]["detail"]["shown"]["holder"]["pid"] == gone.pid
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["released"] is True
    assert envelope["data"]["summary"]["holder"]["pid"] == gone.pid
    assert session.read_lock_holder(session.lock_path(installed)) is None


def test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched(installed):
    """A live holder refuses ``session-lock-held``, and the bytes are unchanged."""
    here = session.current_holder()
    path = _lock_recording(installed, here)
    before = path.read_bytes()

    _code, _refused, envelope = _release()

    assert envelope["cause"]["reason"] == "session-lock-held", envelope
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.WAIT_FOR_HOLDER)
    assert path.read_bytes() == before
    assert session.read_lock_holder(path) == here


def test_a_stale_record_over_a_file_something_else_holds_is_still_refused(installed):
    """A gone holder over a lock file this process holds is still refused (R19)."""
    gone = _a_process_that_is_gone()
    path = _lock_recording(installed, gone)
    before = path.read_bytes()

    handle = session._open_lock_file(path)
    try:
        rb_writer._acquire_exclusive(handle)
        _code, _refused, envelope = _release()
    finally:
        rb_writer._release_exclusive(handle)
        handle.close()

    assert envelope["cause"]["reason"] == "session-lock-held", envelope
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.WAIT_FOR_HOLDER)
    assert path.read_bytes() == before


def test_releasing_a_lock_nobody_holds_asks_anyway_and_reports_a_no_op(installed):
    """Nothing recorded still asks (conformance 3), and is a no-op, not a failure."""
    assert not session.lock_path(installed).exists()

    code, refused, envelope = _release()
    assert refused["cause"]["detail"]["shown"]["holder"] is None
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"] == {
        "released": False,
        "recorded": False,
        "unreadable": False,
        "abandoned": [],
        "kept": [],
    }


def test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question(
    installed, monkeypatch
):
    """R-1255: an unlistable log refuses before the question, and clears nothing."""
    gone = _a_process_that_is_gone()
    path = _lock_recording(installed, gone)
    before = path.read_bytes()
    _refuse_listing(monkeypatch, Path(session.log_dir(installed)))

    code, refused = _drive(["session", "release"])

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert "cannot be listed by this account" in refused["cause"]["message"]
    assert path.read_bytes() == before


def test_aborting_the_release_clears_nothing(installed):
    """The other half of the gate, so the question is not decoration."""
    gone = _a_process_that_is_gone()
    path = _lock_recording(installed, gone)

    code, _refused, envelope = _release("abort")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert session.read_lock_holder(path) == gone


# ═══════════════════════════════════════════════════════════════════════════
# session release, and the open records a hard killed write left (R-598)
# ═══════════════════════════════════════════════════════════════════════════


def _hard_killed_gated_write(cfg) -> str:
    """Enter the gates keeping a record, in a child, and SIGKILL it inside the body.

    A real kill in a forked child, so the kernel drops the child's lock and the
    record names a dead holder. Every failure in the child ends in ``os._exit``.
    """
    reader, writer = os.pipe()
    child = os.fork()
    if child == 0:  # pragma: no cover - measured by the parent's assertions
        try:
            # A lock another thread held at the fork stays held in the child;
            # the alarm turns that hang into a death by the wrong signal.
            signal.alarm(30)
            os.close(reader)
            gates = session.assert_gates(
                cfg, workflow="metadata.mytags-vocals", keep=session.Keep.RECORD
            )
            entered = gates.__enter__()
            os.write(writer, entered.record.session_id.encode("utf-8"))
            os.close(writer)
            os.kill(os.getpid(), signal.SIGKILL)
        finally:
            os._exit(3)
    os.close(writer)
    with os.fdopen(reader, "rb") as pipe:
        session_id = pipe.read().decode("utf-8")
    _pid, status = os.waitpid(child, 0)
    assert os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGKILL, status
    assert session_id, "the child never got inside the gates"
    return session_id


def _left_by(cfg, holder: session.Holder, state: session.SessionState) -> str:
    """A gated record naming ``holder``, persisted in ``state``, and its identifier."""
    record = session.open_session(cfg, workflow="write.trees", holder=holder)
    record.state = state
    session.write_record(record, cfg)
    return record.session_id


#: This machine's identity for the power loss tests, in the digest's shape.
THIS_MACHINE = "0123456789abcdef0123456789abcdef"


def _before_a_power_loss(monkeypatch, **changes) -> session.Holder:
    """A holder this machine's previous boot recorded, naming a process now gone (R-647)."""
    monkeypatch.setattr(session, "machine_identity", lambda: THIS_MACHINE)
    gone = _a_process_that_is_gone()
    fields = {
        **gone.to_json(),
        "machine": THIS_MACHINE,
        "boot": str(float(session.boot_identity()) - 86400),
        **changes,
    }
    return session.Holder.from_json(fields)


@pytest.mark.filterwarnings("ignore:This process .* is multi-threaded:DeprecationWarning")
@pytest.mark.parametrize("cut_off", ["hard-kill", "power-loss"])
def test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it(
    installed, tmp_path, monkeypatch, cut_off
):
    """R-598 and R-647: the open record refuses cutover until the release ends it.

    A SIGKILL is reproduced in a child; a restart cannot be staged, so its lock
    record and open record from the previous boot are written directly.
    """
    from cratekit.core import tree_registry
    from cratekit.core.cause import CratekitError
    from tests.test_intake_imported import _verified_snapshot

    _verified_snapshot(installed)
    _code, _refusal, minted = _mint_through_the_cli()
    assert minted["data"]["summary"]["recorded"] is True
    if cut_off == "hard-kill":
        session_id = _hard_killed_gated_write(installed)
        assert session.read_record(session_id, installed).state is session.SessionState.OPEN
    else:
        dead = _before_a_power_loss(monkeypatch)
        assert session.holder_alive(dead) is False
        _lock_recording(installed, dead)
        session_id = _left_by(installed, dead, session.SessionState.OPEN)

    export = tmp_path / "fresh-export.xml"
    export.write_text("<DJ_PLAYLISTS/>")
    with pytest.raises(CratekitError) as refused:
        tree_registry.assert_cutover_ready(installed, export=export)
    assert refused.value.cause.reason == "cutover-open-run"

    code, asked, envelope = _release()
    assert [row["session_id"] for row in asked["cause"]["detail"]["shown"]["orphans"]] == [
        session_id
    ]
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["abandoned"] == [session_id]
    ended = session.read_record(session_id, installed)
    assert ended.state is session.SessionState.ABANDONED
    if cut_off == "hard-kill":
        assert ended.ended is not None
    else:
        assert envelope["data"]["summary"]["released"] is True
        assert envelope["data"]["summary"]["holder"] == dead.to_json()
        assert session.read_lock_holder(session.lock_path(installed)) is None
    tree_registry.assert_cutover_ready(installed, export=export)


@pytest.mark.parametrize(
    "holder",
    ["another-machine-with-this-host-name", "recorded-before-the-machine-identity", "alive"],
)
def test_a_record_not_proven_dead_on_this_machine_is_kept(installed, monkeypatch, holder):
    """Another machine, a record older than the field, or a live holder: all stay open."""
    if holder == "alive":
        theirs = session.current_holder()
    else:
        machine = "f" * 32 if holder.startswith("another") else session.UNKNOWN_IDENTITY
        theirs = _before_a_power_loss(monkeypatch, machine=machine)
    session_id = _left_by(installed, theirs, session.SessionState.OPEN)
    before = session.log_path(session_id, installed).read_bytes()

    code, asked, envelope = _release()
    assert asked["cause"]["detail"]["shown"]["orphans"] == []
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["abandoned"] == []
    assert envelope["data"]["summary"]["kept"] == [session_id]
    assert session.log_path(session_id, installed).read_bytes() == before


@pytest.mark.parametrize(
    "state",
    [session.SessionState.AWAITING_IMPORT, session.SessionState.COMMITTED_UNVERIFIED],
)
def test_the_two_states_with_their_own_remedy_are_never_abandoned(installed, state):
    """A dead holder alone does not end a record whose state has its own remedy."""
    session_id = _left_by(installed, _a_process_that_is_gone(), state)
    before = session.log_path(session_id, installed).read_bytes()

    code, _asked, envelope = _release()
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["abandoned"] == []
    assert session.log_path(session_id, installed).read_bytes() == before


def test_an_open_record_that_names_no_holder_is_never_abandoned(installed):
    """No holder is no proof: an intake landing stays open with none (R-501)."""
    record = session.open_session(installed, workflow="intake")
    before = session.log_path(record.session_id, installed).read_bytes()

    code, _asked, envelope = _release()
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["abandoned"] == []
    assert envelope["data"]["summary"]["kept"] == [record.session_id]
    assert session.log_path(record.session_id, installed).read_bytes() == before


@pytest.mark.parametrize("ending", ["live-lock-holder", "abort"])
def test_a_refused_or_aborted_release_abandons_nothing(installed, ending):
    """A live lock holder refuses first, and an abort covers the records too."""
    if ending == "live-lock-holder":
        _lock_recording(installed, session.current_holder())
    session_id = _left_by(installed, _a_process_that_is_gone(), session.SessionState.OPEN)

    code, _asked, envelope = _release("abort" if ending == "abort" else "release")
    if ending == "abort":
        assert code == int(ExitCode.OK), envelope
        assert envelope["outcome"] == "no_op"
    else:
        assert envelope["cause"]["reason"] == "session-lock-held", envelope
    assert session.read_record(session_id, installed).state is session.SessionState.OPEN


def test_a_release_that_only_abandons_is_a_change_and_passes_the_contract(installed):
    """No lock to clear and one record ended is an OK outcome, not a no-op."""
    from cratekit.cli import output

    session_id = _left_by(installed, _a_process_that_is_gone(), session.SessionState.OPEN)

    code, _asked, envelope = _release()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] != "no_op", envelope
    assert envelope["data"]["summary"]["released"] is False
    assert envelope["data"]["summary"]["abandoned"] == [session_id]
    assert output.envelope_problems(envelope) == [], envelope


# ═══════════════════════════════════════════════════════════════════════════
# The registry, and what landing the module turned on
# ═══════════════════════════════════════════════════════════════════════════


def test_both_verbs_are_reachable_from_the_command_line(installed):
    """The subparser choices are the registration, walked rather than substring matched."""
    import argparse

    parser = cli.build_parser()
    groups = [
        action
        for action in parser._subparsers._group_actions  # noqa: SLF001 - argparse has no public walk
        if isinstance(action, argparse._SubParsersAction)
    ]
    assert groups, "the root parser declares no subcommands at all"
    session_group = groups[0].choices["session"]
    leaves = [
        action
        for action in session_group._subparsers._group_actions  # noqa: SLF001
        if isinstance(action, argparse._SubParsersAction)
    ]
    assert {"ack", "release"} <= set(leaves[0].choices)

    code, envelope = _drive(["session", "ack"])
    assert envelope["verb"] == "session.ack", envelope
    code, envelope = _drive(["session", "release"])
    assert envelope["verb"] == "session.release", envelope


def test_every_payload_either_verb_emits_is_one_the_contract_accepts(installed):
    """Success and no-op payloads, which the conformance drives never reach (R21)."""
    from cratekit.cli import output

    gone = _a_process_that_is_gone()

    _code, _refused, minted = _mint_through_the_cli()
    assert output.envelope_problems(minted) == [], minted

    _code, _refused, aborted = _mint_through_the_cli("abort")
    assert output.envelope_problems(aborted) == [], aborted

    _lock_recording(installed, gone)
    for option in ("release", "abort"):
        _code, _refused, envelope = _release(option)
        assert output.envelope_problems(envelope) == [], envelope


def test_the_check_rows_a_person_reads_name_the_portion(installed):
    """The default renderer reads ``key``; a row keyed otherwise renders ``[ok] ?``."""
    _mint_through_the_cli()
    code, refused = _drive(["session", "ack"])
    _answer(refused["run_id"], ACK_GATE, "acknowledged")
    code, text = _human(["--run", refused["run_id"], "session", "ack"])

    assert code == int(ExitCode.OK), text
    assert "backup.age.database" in text
    assert "] ?:" not in text, (
        "a check row rendered as a question mark, so the row is keyed by a "
        "field the check table does not read"
    )


def test_a_damaged_acknowledgment_record_can_still_be_replaced(installed):
    """A corrupt record is shown as unreadable and overwritten, never a lockout."""
    config.atomic_write_bytes(b"{not json at all", session.ack_path(installed))

    code, refused, envelope = _mint_through_the_cli()
    assert refused["cause"]["detail"]["shown"]["acknowledgment"]["unreadable"]
    assert code == int(ExitCode.OK), envelope
    assert session.read_acknowledgment(installed) is not None


def test_a_lock_record_that_cannot_be_understood_refuses_by_name(installed):
    """A lock record with a non numeric pid is reported unreadable, not as absent."""
    config.atomic_write_bytes(
        json.dumps({"holder": {"host": "x", "boot": "y", "pid": "not-a-number"}}).encode(),
        session.lock_path(installed),
    )

    code, refused, envelope = _release()
    assert refused["cause"]["detail"]["shown"]["record"] == "unreadable"
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["unreadable"] is True


def test_a_spent_acknowledgment_decision_cannot_be_replayed(installed):
    """R34: a recorded answer mints once; a fresh deliberate act mints again."""
    code, refused = _drive(["session", "ack"])
    run_id = refused["run_id"]
    _answer(run_id, ACK_GATE, "acknowledged")
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.OK), envelope
    first = session.read_acknowledgment(installed).expires_at

    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert session.read_acknowledgment(installed).expires_at == first

    _answer(run_id, ACK_GATE, "acknowledged")
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.OK), envelope


def test_a_gate_the_entry_does_not_declare_is_an_internal_error_by_name(installed):
    """The lookup is by name, and a missing name is an internal error, not a guess."""
    from cratekit.cli import registry
    from cratekit.core.cause import CratekitError
    from cratekit.session import cli as session_cli

    entry = registry.entry("session.ack")
    assert session_cli._gate(entry, ACK_GATE).name == ACK_GATE
    with pytest.raises(CratekitError) as raised:
        session_cli._gate(entry, "session.ack.nonesuch")
    assert raised.value.cause.reason == "internal-error"
    assert raised.value.cause.remediation.remedy is Remedy.REPORT_DEFECT


def test_neither_entry_still_claims_to_be_planned(installed):
    """R11: both entries name the landed module and neither is still planned."""
    from cratekit.cli import registry

    for name in ("session.ack", "session.release"):
        entry = registry.entry(name)
        assert entry.planned_in is None, name
        assert entry.landed, name
        assert entry.module == "cratekit.session.cli", name
