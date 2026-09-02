"""U49: the two session verbs, driven through the dispatcher rather than the API.

WHY THIS FILE EXISTS AND WHY IT DRIVES WHAT IT DRIVES.
``cratekit.core.session.record_acknowledgment`` and
``cratekit.core.session.release_stale_lock`` were both fully implemented and
fully tested before this unit, and neither had a caller anywhere in ``src``. The
suite was green because ``tests/test_write_session.py`` and
``tests/test_restore.py`` mint acknowledgments by calling the core function, so
every guard resting on that record was measured in a world where nothing a
person could type could produce one. That is the shape
``docs/solutions/workflow-issues/a-guard-safe-only-because-its-subject-is-
unimplemented-expires-when-it-lands.md`` names, and repeating it here would land
the verbs and prove nothing about them.

So every property below goes through ``cli.run``. Where the acknowledgment is
needed, it is minted by driving ``crate session ack`` and answering its gate,
never by calling ``record_acknowledgment``. The end-to-end test then drives a
REAL destructive verb, ``restore.run``, to completion on that acknowledgment,
because the claim this unit is making is that a person can spend the protection
and not that ``assert_gates`` returns.

THE LIVE REKORDBOX DATABASE IS NEVER TOUCHED. Every fixture here is a temporary
directory, taken from ``tests/test_restore.py`` by assignment for the reason
``tests/test_restore_cli.py`` states beside its own copy: a second definition is
a second thing to keep in step.
"""

from __future__ import annotations

import io
import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import pytest

from cratekit import cli
from cratekit.core import backup_facts, config, preflight, rb_writer, session
from cratekit.core.exit_codes import ExitCode, Remedy
from tests import test_restore as restore_suite
from tests.test_restore import completed_session

#: The configured, SAVED library fixture. Assignment rather than ``from ...
#: import`` for the reason ``tests/test_restore_cli.py`` gives: a fixture
#: imported by name is shadowed by every test parameter that uses it, and a
#: second copy is what drifts.
cfg = restore_suite.cfg

#: The two declared gate names, spelled once so no drive here can drift from the
#: registry entry it is answering.
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
    """A person is sitting here, asserted rather than inherited.

    Whether ``os.ctermid()`` opens depends on how the suite was launched, so a
    test that leaves it alone passes or fails on a property of the machine. What
    is replaced is only the answer to "could a person be here"; the REFUSING
    direction is driven in its own test below, where it is the thing under test
    rather than a precondition, and the default probe that ships is asserted in
    ``tests/test_write_session.py``.
    """
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)


@pytest.fixture
def installed(cfg, monkeypatch, at_a_terminal):
    """The library with the two PLATFORM seams answered for this machine.

    Only the answer to "which volume is this path on" is replaced, exactly as
    the conformance suite's fixture replaces it. Every gate these verbs are
    about still runs.
    """
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
    code, envelope = _drive(
        ["run", "decide", run_id, gate, option, "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), envelope


def _mint_through_the_cli(option: str = "acknowledged") -> tuple[int, dict, dict]:
    """Drive ``crate session ack`` all the way through, and return both halves.

    THE WHOLE POINT OF THIS HELPER is that nothing here calls
    ``record_acknowledgment``. Three invocations, because the gate is explicit
    and R34 says the command that discovers a question may not answer it.
    """
    code, refused = _drive(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _answer(run_id, ACK_GATE, option)
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    return code, refused, envelope


def _lock_recording(target_cfg, holder):
    """Write a lock file naming ``holder``. Same shape as test_write_session's."""
    path = session.lock_path(target_cfg)
    config.atomic_write_bytes(
        json.dumps({"holder": holder.to_json()}).encode("utf-8"), path
    )
    return path


def _a_process_that_is_gone() -> session.Holder:
    """A holder naming a process this boot really started and that really exited.

    A real finished process rather than a stubbed liveness answer, because a stub
    would prove the stub was consulted. ``holder_alive`` fails towards alive on
    anything it cannot establish, so a fabricated pid would be judged alive and
    the release would refuse for the wrong reason.
    """
    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    assert session.process_exists(finished.pid) is False
    here = session.current_holder()
    gone = session.Holder(
        host=here.host, boot=here.boot, pid=finished.pid, started="1.000"
    )
    assert session.holder_alive(gone) is False
    return gone


# ═══════════════════════════════════════════════════════════════════════════
# session ack
# ═══════════════════════════════════════════════════════════════════════════


def test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends(installed):
    """THE PROPERTY THIS WHOLE UNIT EXISTS FOR, end to end and both directions.

    Before: ``restore.run``, a landed destructive verb, refuses because no
    acknowledgment exists. After three commands typed by a person, the same verb
    completes. Neither half touches ``record_acknowledgment``.

    IT DRIVES A DESTRUCTIVE VERB AND NOT ``assert_gates``. Asserting that the
    gate function returns would be the core API again, one layer over the shape
    this unit was opened to fix. What is claimed is that a person can protect
    their library and then spend that protection, and only a verb can show that.
    """
    record, _captured = completed_session(installed)

    code, refused = _drive(["restore", "run", record.session_id])
    run_id = refused["run_id"]
    _answer(run_id, "restore.run.confirm", "restore")
    code, blocked = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert blocked["cause"]["reason"] == "backup-acknowledgment-missing", blocked
    assert code == int(ExitCode.ACK_REQUIRED), blocked

    code, _refusal, minted = _mint_through_the_cli()
    assert code == int(ExitCode.OK), minted
    assert minted["data"]["summary"]["recorded"] is True

    code, refused = _drive(["restore", "run", record.session_id])
    run_id = refused["run_id"]
    _answer(run_id, "restore.run.confirm", "restore")
    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert code == int(ExitCode.OK), envelope


def test_the_refusal_before_acknowledging_names_the_ages_it_consulted(installed):
    """R2 and R5 in one drive: an ABSENT fact file shows, it does not refuse.

    Every library has no fact file until its first backup, so a verb that
    refused here would be unreachable on exactly the library a person is trying
    to protect. What it must not do is show nothing: an acknowledgment with no
    age is a click rather than a decision, which is what KTD18 asks for the age
    alongside the question for.
    """
    code, refused = _drive(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["ages"], "the question was asked over nothing"
    assert {entry["portion"] for entry in shown["ages"]} == {
        str(portion) for portion in backup_facts.Portion
    }
    assert all(entry["state"] == "never-recorded" for entry in shown["ages"])


def test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer(installed):
    """The default output mode, which is the one nobody passes a flag to get.

    ``render_gate`` reads a fixed set of keys off the cause, so a fact carried
    into the envelope and not rendered would satisfy ``--output json`` and leave
    the person the acknowledgment is FOR answering a bare question.
    """
    code, text = _human(["session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), text
    assert "Database and music files are backed up" in text
    assert "portion=database" in text
    assert "state=never-recorded" in text


def test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states(installed):
    """Absent, live, and expired are three facts with three next moves.

    Reporting an expired record as no record would send a person to redo
    something they already did, which is the sentence ``read_acknowledgment``
    writes about its own file one layer down.
    """
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
    """R4, driven through ``read_facts`` on ALL THREE tokens and not one.

    ``backup_facts.Remedy`` declares three because a file this account may not
    open and a file whose contents are damaged have opposite fixes, and a build
    written by a newer version has a third. R-201 recorded what naming one token
    over all three costs on this exact path, and U48 measured that a carry driven
    on one case leaves the others unasserted. So each condition is MADE, not
    simulated: the exception is raised by the real reader at the real file
    boundary, because one built by hand can carry a field the code path never
    produces.
    """
    facts = backup_facts.path_for(installed)
    facts.parent.mkdir(parents=True, exist_ok=True)
    if damage == "permission":
        facts.write_text("{}")
        os.chmod(facts, 0o000)
        # THE PRECONDITION IS ASSERTED, NOT ASSUMED AND NOT SKIPPED AROUND. An
        # account the mode bits do not restrain reads the file anyway, and this
        # test would then pass over a refusal that never occurred, which is the
        # exact shape of guard the corpus warns about. A skip would hide the same
        # thing behind a green line, and this repository routes every skip
        # through ``tests/_pending.py`` so a skip is a countdown rather than a
        # wish. Failing here says plainly that the suite is being run as an
        # account that cannot measure this property.
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
    """R34: no answer smuggled into the command that discovered the question.

    An agent driving this command line would otherwise mint, in one invocation,
    the gate protecting the one operation that removes files.
    """
    code, envelope = _drive(["-d", f"{ACK_GATE}=acknowledged", "session", "ack"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["explicit"] is True
    assert session.read_acknowledgment(installed) is None


def test_an_inline_answer_cannot_overturn_a_recorded_abort(installed):
    """The precedence this verb is the first landed caller of, driven on purpose.

    ``Gates.require`` refuses an inline answer to an explicit gate only while
    NOTHING is recorded; once a decision exists, the inline value is preferred
    over it. That ordering is invisible until a verb whose gate mints something
    drives it, and this unit is that verb, so the question "can a flag overturn
    an answer a person deliberately recorded" gets asked here rather than
    discovered later. Asserted as the behaviour that ships: whatever the
    resolver decides, an ABORT a person recorded must not become a mint.
    """
    code, refused = _drive(["session", "ack"])
    run_id = refused["run_id"]
    _answer(run_id, ACK_GATE, "abort")

    code, envelope = _drive(
        ["--run", run_id, "-d", f"{ACK_GATE}=acknowledged", "session", "ack"]
    )
    assert session.read_acknowledgment(installed) is None, (
        "a flag on a later invocation overturned an abort a person recorded, so "
        "the explicit gate can be answered by the thing it gates (R34)"
    )
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["detail"]["explicit"] is True

    # And the recorded answer still stands on its own, so the fix refused the
    # FLAG rather than the run. Without this half the assertion above is also
    # satisfied by a resolver that stopped honouring recorded decisions.
    code, envelope = _drive(["--run", run_id, "session", "ack"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert session.read_acknowledgment(installed) is None


def test_the_answering_invocation_refuses_when_nobody_is_there(installed, monkeypatch):
    """The last thing between a detached job and a minted acknowledgment.

    Every other test here needs the probe to say yes, so without this one a
    regression that removed the check entirely would leave the suite green. The
    recorded decision survives the refusal, so the same person can answer again
    from a terminal without starting over.
    """
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
    """Re-acknowledging re-mints; it does not refuse and does not no-op.

    ``record_acknowledgment`` overwrites unconditionally, so a freshness check
    added in the shell would be a second rule about one record living in a
    different file from the rule it copies. The window moving is the observable
    consequence, and it is asserted rather than left to be discovered.
    """
    _code, _refused, first = _mint_through_the_cli()
    _code, _refused, second = _mint_through_the_cli()
    assert second["data"]["summary"]["recorded"] is True
    assert (
        second["data"]["summary"]["expires_at"] >= first["data"]["summary"]["expires_at"]
    )
    assert session.read_acknowledgment(installed).actor == session.derive_actor()


# ═══════════════════════════════════════════════════════════════════════════
# session release
# ═══════════════════════════════════════════════════════════════════════════


def test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first(installed):
    """The verb's whole job, plus the fact the person decided over.

    The prompt is fixed at declaration and says "another installation", which
    describes no particular claim. What makes this a decision rather than a
    click is that the refusal carries the recorded holder, so the person can see
    whose lock they are about to clear before they clear it.
    """
    gone = _a_process_that_is_gone()
    _lock_recording(installed, gone)

    code, refused = _drive(["session", "release"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["holder"]["pid"] == gone.pid
    run_id = refused["run_id"]
    _answer(run_id, RELEASE_GATE, "release")

    code, envelope = _drive(["--run", run_id, "session", "release"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["released"] is True
    assert envelope["data"]["summary"]["holder"]["pid"] == gone.pid
    assert session.read_lock_holder(session.lock_path(installed)) is None


def test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched(installed):
    """R9. One run clearing another run's claim mid-write is what the lock is for.

    The bytes are compared either side, because a refusal that already wrote
    something is the class of defect a return-code assertion cannot see.
    """
    here = session.current_holder()
    path = _lock_recording(installed, here)
    before = path.read_bytes()

    code, refused = _drive(["session", "release"])
    run_id = refused["run_id"]
    _answer(run_id, RELEASE_GATE, "release")
    code, envelope = _drive(["--run", run_id, "session", "release"])

    assert envelope["cause"]["reason"] == "session-lock-held", envelope
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.WAIT_FOR_HOLDER)
    assert path.read_bytes() == before
    assert session.read_lock_holder(path) == here


def test_a_stale_record_over_a_file_something_else_holds_is_still_refused(installed):
    """R19, ``release_stale_lock``'s fourth outcome and its least obvious one.

    The recorded holder is genuinely gone, so the claim looks stale, and the
    lock file cannot be taken anyway because this test process is holding it.
    That is a different world from a live record and it must not clear: the
    record being wrong says nothing about who is actually inside.

    THIS UNIT IS THE FIRST CALLER OF THAT FUNCTION, which is what puts its
    unreviewed branches here rather than in somebody's later surprise.
    """
    gone = _a_process_that_is_gone()
    path = _lock_recording(installed, gone)
    before = path.read_bytes()

    handle = session._open_lock_file(path)
    try:
        rb_writer._acquire_exclusive(handle)
        code, refused = _drive(["session", "release"])
        run_id = refused["run_id"]
        _answer(run_id, RELEASE_GATE, "release")
        code, envelope = _drive(["--run", run_id, "session", "release"])
    finally:
        rb_writer._release_exclusive(handle)
        handle.close()

    assert envelope["cause"]["reason"] == "session-lock-held", envelope
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.WAIT_FOR_HOLDER)
    assert path.read_bytes() == before


def test_releasing_a_lock_nobody_holds_asks_anyway_and_reports_a_no_op(installed):
    """R10 and the reason the gate still fires on the quiet path.

    Nothing recorded is the state of every healthy library. Refusing there would
    report a working machine as a broken one and hand a person a remedy for a
    condition with no remedy, which is ``restore_cli.perform_restore``'s
    decision for the same shape. The question is still asked, because
    conformance 3 holds every declared gate to firing and a verb whose question
    fires only when the answer matters is a verb nobody is ever asked by.
    """
    assert not session.lock_path(installed).exists()

    code, refused = _drive(["session", "release"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["holder"] is None
    run_id = refused["run_id"]
    _answer(run_id, RELEASE_GATE, "release")

    code, envelope = _drive(["--run", run_id, "session", "release"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"] == {"released": False, "recorded": False}


def test_aborting_the_release_clears_nothing(installed):
    """The other half of the gate, so the question is not decoration."""
    gone = _a_process_that_is_gone()
    path = _lock_recording(installed, gone)

    code, refused = _drive(["session", "release"])
    run_id = refused["run_id"]
    _answer(run_id, RELEASE_GATE, "abort")
    code, envelope = _drive(["--run", run_id, "session", "release"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert session.read_lock_holder(path) == gone


# ═══════════════════════════════════════════════════════════════════════════
# The registry, and what landing the module turned on
# ═══════════════════════════════════════════════════════════════════════════


def test_both_verbs_are_reachable_from_the_command_line(installed):
    """``crate --help`` is where a person finds out these exist at all.

    Read off the REAL parser the dispatcher builds rather than by driving
    ``--help``, because argparse prints help and exits the process, so a drive
    would assert against an empty capture while the text went past it.
    """
    assert "session" in cli.build_parser().format_help()
    code, envelope = _drive(["session", "ack"])
    assert envelope["verb"] == "session.ack", envelope
    code, envelope = _drive(["session", "release"])
    assert envelope["verb"] == "session.release", envelope


def test_neither_entry_still_claims_to_be_planned(installed):
    """R11, and it is one assertion about two entries on purpose.

    The countdown keys on the module string rather than on the verb name, so
    ``cratekit.session.cli`` appearing expires both markers or neither. Dropping
    one would leave the other declaring a module that exists, which
    ``test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`` catches
    and which is the exact miss ``the-brief-files-line-is-not-the-landing-path``
    was written about.
    """
    from cratekit.cli import registry

    for name in ("session.ack", "session.release"):
        entry = registry.entry(name)
        assert entry.planned_in is None, name
        assert entry.landed, name
        assert entry.module == "cratekit.session.cli", name
