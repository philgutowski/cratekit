"""U27: the two restore verbs, and the ONE session that spans them.

WHY THIS FILE EXISTS SEPARATELY FROM THE CONFORMANCE SUITE. All nine conformance
properties drive both verbs the moment their entries lose ``planned_in``, and
every one of them drives the EMPTY path: a library with no session log, no
capture, and nothing to roll back to. None of them reaches the destructive
session, because a restore that would perform nothing deliberately does not open
one. So the thing the unit exists for would ship undriven if this file did not
exist.

WHAT THE UNIT EXISTS FOR. ``tests/_pending.py`` registered two obligations
against ``cratekit.session.restore_cli``: a command-line surface for the two
verbs the registry has declared since U32, and the ONE wiring call that hands the
already-open session's guard to the off-machine restore, so that a restore is one
acquisition of the library lock rather than two with a window in it. Both are
driven below, and the second is driven through the real
``backup.plan_restore``/``backup.run_restore`` rather than through a recorded
call, because taking the lock a second time in this process RAISES, which makes
the composition measurable rather than arguable.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core import config, jobs, preflight, rb_writer, session
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup
from cratekit.session import restore_cli
from tests import test_restore as restore_suite
from tests.test_restore import acknowledge, completed_session, gate_seams

#: The configured, SAVED library fixture, taken from the restore engine's own
#: suite by assignment rather than by ``from ... import``. A fixture imported by
#: name is shadowed by every test parameter that uses it, which the linter reads
#: as a redefinition; an attribute assignment registers it here exactly the same
#: way and says out loud that this is one fixture rather than a second copy of
#: one. A second copy is what would drift: this file's properties are about a
#: library whose configuration is on disk, because the dispatcher resolves it
#: from there.
cfg = restore_suite.cfg

#: The confirmation gate's declared name, spelled once so the drives below cannot
#: drift from the registry entry they are answering.
CONFIRM = "restore.run.confirm"


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock.

    Copied from ``tests/test_restore.py`` rather than imported, because an autouse
    fixture applies to the module that DECLARES it: importing the helper names
    from that file brings its helpers and not its autouse guards, and a session
    lock leaking across tests here would be attributed to whichever test ran next.
    """
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    """No rekordbox process, injected, so no test depends on this machine."""
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def installed(cfg, monkeypatch):
    """The same library, with the two PLATFORM seams answered for this machine.

    THE SEAMS ARE INJECTED AND THE GATES ARE NOT. Every test that drives a verb
    through the dispatcher gets its arguments from a command line, so there is no
    place to hand a provider in; without this the volume identity check compares
    the fixture's recorded identifier against the boot disk's, which is a
    property of the laptop rather than of the verb. What is replaced is only the
    answer to "which volume is this path on", exactly as the conformance suite's
    own fixture replaces it, and every gate this unit is about still runs.
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
    """Run the REAL dispatcher and return the status with the parsed envelope.

    Through ``cli.run`` rather than by calling the handler, because the handler
    takes a context the dispatcher builds, and every property below about gates,
    runs and exit codes is a property of that assembly rather than of the
    function.
    """
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _answer(run_id: str, option: str) -> None:
    """R34's second act: the decision, recorded against the run, with its actor."""
    code, envelope = _drive(
        ["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), envelope


def _lock_taken_in_another_process(path: Path) -> int:
    """Try to take the library lock in a REAL second interpreter. Zero means it succeeded.

    A thread would share this interpreter's open file descriptions, and an
    advisory lock is held per description, so a thread can only ever prove what
    this process already believes.
    """
    script = (
        "import fcntl, sys\n"
        "handle = open(sys.argv[1], 'a+')\n"
        "try:\n"
        "    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
        "except OSError:\n"
        "    sys.exit(3)\n"
        "sys.exit(0)\n"
    )
    return subprocess.run(
        [sys.executable, "-c", script, str(path)], capture_output=True
    ).returncode


# ═══════════════════════════════════════════════════════════════════════════
# The one session. This is the unit.
# ═══════════════════════════════════════════════════════════════════════════


def test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock(cfg, tmp_path):
    """The wiring call U32 proved at the seam and could not make.

    DRIVEN THROUGH THE REAL BACKUP FUNCTIONS, not through recorded calls, and
    that is what makes this a measurement. Both of them default to taking the
    library lock themselves, and ``core.session.session_lock`` RAISES
    ``SessionComposition`` when one is opened inside another in the same process,
    because the second acquisition can never succeed. So a verb that forgot to
    hand the guard down does not merely take the lock twice here: it fails, and
    the failure names the composition.

    THE FOREIGN PROBE RUNS FROM INSIDE THE OFF-MACHINE HALF, in the injected
    runner, because that is the only moment at which "the lock is held while the
    mirror is being pulled" is a fact about the world rather than about the call
    order. A probe after the call would pass over a verb that took no lock at all.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    (tmp_path / "recovered").mkdir()
    observed: list[int] = []
    labels: list[str] = []

    def runner(command):
        labels.append(command.label)
        observed.append(_lock_taken_in_another_process(session.lock_path(cfg)))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    report = restore_cli.restore_under_one_session(
        cfg,
        session_id=record.session_id,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    assert backup.RESTORE_DATABASE in labels, "the off-machine half never ran"
    assert observed and all(code != 0 for code in observed), (
        "a second process took the library lock while the mirror was being "
        "pulled, so the restore is not one acquisition"
    )
    assert report.outcome is not None and report.outcome.performed, (
        "the capture half never ran"
    )
    assert report.pulled, "the report does not name the transfers the mirror half made"


def test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened(
    cfg, tmp_path
):
    """The half that ran is named, and the half that did not is ``None``.

    THIS IS A DEFECT THE FIRST SHAPE OF THIS FUNCTION HAD. It returned only the
    capture outcome, so a run that pulled a whole mirror and named no session
    returned ``None`` and the verb reported zero steps performed: hundreds of
    gigabytes moved, and the output said nothing had happened.

    A fabricated ``RestoreOutcome`` is still refused for the other direction: it
    would report ``converged`` over state nothing looked at, which is the one
    question this unit answers conservatively everywhere else.
    """
    acknowledge(cfg)
    (tmp_path / "recovered").mkdir()

    report = restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=lambda command: backup.CommandResult(returncode=0, stdout=""),
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    assert report.outcome is None
    assert backup.RESTORE_DATABASE in report.pulled

    payload = restore_cli._performed(report, {"digest": "d"})
    assert payload["totals"]["transfers"] == len(report.pulled)
    assert [item["half"] for item in payload["items"]] == ["off-machine"] * len(
        report.pulled
    )
    assert "converged" not in payload["totals"], (
        "a run that spent no capture reported on the capture restore's own question"
    )


def test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception(
    installed, tmp_path, monkeypatch
):
    """KTD25 at the boundary this unit created.

    ``backup.Refusal`` is the backup module's own diagnosis set and nothing
    downstream can classify it. Before this verb existed no caller carried one
    out to a person, so an escaping ``BackupRefused`` would have arrived as an
    internal error telling somebody to report a defect for an unconfigured
    remote.

    THE SLUG SURVIVES, and that is the assertion rather than the exit code alone.
    Nine diagnoses folded into one nearby reason would tell a person to mount a
    volume when what is missing is a program.
    """
    acknowledge(installed)
    unconfigured = _without_remote(installed)
    with pytest.raises(CratekitError) as excinfo:
        restore_cli.restore_under_one_session(
            unconfigured,
            session_id=None,
            from_backup=True,
            target=tmp_path,
            **gate_seams(installed),
        )

    cause = excinfo.value.cause
    assert cause.reason == str(backup.Refusal.REMOTE_NOT_CONFIGURED)
    assert cause.code is not ExitCode.INTERNAL
    assert cause.remediation.remedy or cause.remediation.steps, (
        "the refusal reached a person with nothing to do about it"
    )


def _without_remote(cfg_value):
    """The same configuration with the off-machine destinations removed.

    Built by REPLACING the field rather than by writing a second configuration
    dictionary, so the library half stays byte for byte the one every other test
    here uses and the only difference is the one under test.
    """
    return replace(
        cfg_value,
        backup=replace(
            cfg_value.backup, remote="", dest="", archive_root="", db_dest_root=""
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
# restore list
# ═══════════════════════════════════════════════════════════════════════════


def test_the_listing_shows_a_session_with_its_timestamp_workflow_and_per_tree_counts(installed):
    """AE18's first half, through the dispatcher rather than through the engine."""
    record, _captured = completed_session(installed)

    code, envelope = _drive(["restore", "list"])

    assert code == int(ExitCode.OK), envelope
    rows = envelope["data"]["items"]
    assert [row["session_id"] for row in rows] == [record.session_id]
    only = rows[0]
    assert only["started"] == record.started
    assert only["workflow"] == "library-sweep"
    assert only["restorable"] is True
    assert only["change"] == [{"tree": "routing", "created": 3, "updated": 1}]


def test_a_session_whose_capture_is_gone_is_listed_and_says_why(installed):
    """Reported rather than filtered, which is ``Restorable``'s decision carried out.

    The session whose capture somebody deleted by hand is exactly the one a
    person is about to go looking for, and dropping it from the list answers
    their question with silence.
    """
    record, captured = completed_session(installed)
    for path in sorted(captured.root.rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    captured.root.rmdir()

    code, envelope = _drive(["restore", "list"])

    assert code == int(ExitCode.OK), envelope
    only = envelope["data"]["items"][0]
    assert only["session_id"] == record.session_id
    assert only["restorable"] is False
    assert only["unusable"], "an unusable capture was listed with no sentence saying why"


def test_the_listing_answers_on_a_library_that_has_never_acknowledged_a_backup(installed):
    """Read only, so it is outside the gates, and this is what proves it.

    The destructive-session gates refuse a library with no acknowledgment. A
    listing that entered them would be unanswerable on precisely the machine
    where the question a person is asking is whether they have a backup at all.
    """
    completed_session(installed)

    code, envelope = _drive(["restore", "list"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["items"], "the listing returned nothing on a library with a session"


# ═══════════════════════════════════════════════════════════════════════════
# restore run: the two acts, and what is behind them
# ═══════════════════════════════════════════════════════════════════════════


def test_the_confirmation_is_two_acts_and_then_the_database_comes_back(installed, monkeypatch):
    """AE18's second half, end to end, through the real dispatcher.

    R34's shape: the first invocation discovers the gate and exits resumable, the
    decision is recorded against that run by a named actor, and the resume
    continues the SAME run. The measurement is the database's bytes, not the exit
    code: a verb that reported OK and restored nothing would pass every
    assertion about status anybody writes.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)
    database = config.state_path("rekordbox_db", installed)
    before = database.read_bytes()
    database.write_bytes(b"database, generation two")

    code, refused = _drive(["restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    assert refused["resumable"] is True
    run_id = refused["run_id"]

    _answer(run_id, "restore")

    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert code == int(ExitCode.OK), envelope
    assert database.read_bytes() == before, "the verb reported OK and restored nothing"
    assert envelope["data"]["totals"]["steps"], "no step was reported as performed"


def test_an_aborted_confirmation_restores_nothing(installed, monkeypatch):
    """Abort is a real answer, and the measurement is the disk rather than the word.

    A verb that reported NO_OP and restored anyway would read correctly in every
    envelope anybody looks at.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)
    database = config.state_path("rekordbox_db", installed)
    database.write_bytes(b"database, generation two")

    code, refused = _drive(["restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _answer(run_id, "abort")

    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert database.read_bytes() == b"database, generation two", (
        "a declined restore was performed anyway"
    )


def test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused(
    installed, monkeypatch
):
    """The digest is what makes a stale answer visible, and this is what puts it there.

    ``digest_source="plan"`` on this gate is worth nothing unless the handler
    OFFERS the digest, and no other assertion in this file can see whether it
    did: every other path computes the same value on both drives, so it matches
    whether or not the gate was ever told.

    THE OFFER IS MOVED BY COMMITTING A LATER SESSION, which is the shape a real
    library moves by and is exactly the change a person needs their approval
    withdrawn for: they approved rolling back to a point, and since then somebody
    did more work that the same restore would now destroy.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)

    code, refused = _drive(["restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _answer(run_id, "restore")

    # The world moves: the session's recorded change summary is no longer the one
    # the person was shown when they answered.
    record.change = session.ChangeSummary(
        (session.TreeChange(tree="routing", created=99, updated=99),)
    )
    session.write_record(record, installed)

    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_STALE), envelope


def test_nothing_to_restore_is_an_outcome_and_opens_no_session(installed):
    """The empty path, and the proof that it takes no destructive session.

    NO ACKNOWLEDGMENT IS RECORDED HERE, deliberately. The destructive gates
    refuse a library that has never answered the backup question, so reaching OK
    at all is the measurement: a verb that opened the session to decide there was
    nothing to do would exit ACK_REQUIRED on every fresh install, which is every
    machine a person first types this on.
    """
    code, refused = _drive(["restore", "run"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _answer(run_id, "restore")

    code, envelope = _drive(["--run", run_id, "restore", "run"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["items"] == []


def test_a_confirmed_restore_queues_no_job_at_all(installed):
    """Why the payload defect ``adopt.apply`` shipped cannot exist here, MEASURED.

    That defect is specific to a long-running verb: the child a job driver spawns
    is a fresh process, so an argv naming only the job mints a NEW run, meets the
    explicit gate with nothing recorded against it, and exits DECISION_REQUIRED
    for ever. Its precondition is a queued job. ``restore.run`` declares no
    ``argv_builder`` and is not long running, so it has no frozen payload and
    nothing to respawn, which is what puts it outside the population
    ``tests/test_queued_resume_contract.py`` guards.

    ASSERTED AGAINST THE QUEUE RATHER THAN ARGUED FROM THE REGISTRY. "It declares
    no builder" is a fact about a table; "it enqueued nothing" is a fact about
    what the verb did, and only the second one fails if somebody adds a queueing
    branch without adding the flag.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)

    _code, refused = _drive(["restore", "run", record.session_id])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", record.session_id]
    )
    assert code == int(ExitCode.OK), envelope

    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == [], (
            "the restore queued a job, so it now owes the frozen run its explicit "
            "gate needs and nothing in this build supplies one"
        )


def test_a_session_identifier_nothing_recorded_is_refused_by_name(installed):
    """A typo gets a sentence about the identifier, not a traceback and not silence."""
    code, envelope = _drive(["restore", "run", "no-such-session"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert code != int(ExitCode.USAGE)
    assert "no-such-session" in envelope["cause"]["message"]


def test_a_bare_run_takes_the_newest_spendable_capture_and_not_merely_the_newest(cfg):
    """The default has to skip an unusable row, or it refuses on every library that has one.

    A capture somebody deleted by hand is LISTED on purpose. Choosing it as the
    default because it happens to be newest would turn an informative row into a
    refusal for everybody who has ever tidied a snapshot directory.
    """
    older, _first = completed_session(cfg, started="2026-08-01T00:00:00+00:00", stamp="a")
    newer, wrecked = completed_session(cfg, started="2026-08-02T00:00:00+00:00", stamp="b")
    for path in sorted(wrecked.root.rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    wrecked.root.rmdir()

    chosen = restore_cli._newest_restorable(cfg)

    assert chosen is not None
    assert chosen.session_id == older.session_id, (
        f"the default chose {newer.session_id}, whose capture cannot be spent"
    )


def test_a_dry_run_walks_every_step_and_performs_none_of_them(installed, monkeypatch):
    """The rehearsal, through the verb, measured against the database's bytes."""
    acknowledge(installed)
    record, _captured = completed_session(installed)
    database = config.state_path("rekordbox_db", installed)
    database.write_bytes(b"database, generation two")

    code, refused = _drive(["restore", "run", record.session_id, "--dry-run"])
    run_id = refused["run_id"]
    _answer(run_id, "restore")
    code, envelope = _drive(
        ["--run", run_id, "restore", "run", record.session_id, "--dry-run"]
    )

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["dry_run"] is True
    assert envelope["data"]["totals"]["steps"], "a rehearsal that described no step"
    assert database.read_bytes() == b"database, generation two", (
        "a rehearsal performed the restore"
    )


def test_the_discard_override_reaches_the_engine_as_identifiers(installed, monkeypatch):
    """R30's override, driven from the command line in both directions.

    Unnamed, the restore is refused because it would destroy a later session that
    committed. Named, the same restore proceeds. A boolean flag could not tell
    those apart, which is why the engine takes identifiers and why this asserts
    the refusal FIRST: a test that only drove the accepting half would pass over
    a handler that ignored the flag entirely.
    """
    acknowledge(installed)
    target, _captured = completed_session(installed, started="2026-08-01T00:00:00+00:00", stamp="a")
    later, _second = completed_session(installed, started="2026-08-02T00:00:00+00:00", stamp="b")

    code, refused = _drive(["restore", "run", target.session_id])
    run_id = refused["run_id"]
    _answer(run_id, "restore")
    code, envelope = _drive(["--run", run_id, "restore", "run", target.session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert envelope["cause"]["reason"] == "restore-discards-committed-work"

    code, refused = _drive(
        ["restore", "run", target.session_id, "--discard", later.session_id]
    )
    run_id = refused["run_id"]
    _answer(run_id, "restore")
    code, envelope = _drive(
        [
            "--run", run_id, "restore", "run", target.session_id,
            "--discard", later.session_id,
        ]
    )
    assert code == int(ExitCode.OK), envelope


def test_the_report_keeps_the_digest_the_decision_was_recorded_against(installed, monkeypatch):
    """The reported digest identifies the AUTHORISATION, never the work.

    Recomputing it over the performed steps would print a value that does not
    appear on the run record, and a person comparing the two would be looking at
    evidence that the approval did not cover this restore.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)

    code, refused = _drive(["restore", "run", record.session_id])
    run_id = refused["run_id"]
    offered = refused["cause"]["detail"]
    _answer(run_id, "restore")
    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])

    assert code == int(ExitCode.OK), envelope
    from cratekit.cli import gates as cli_gates  # noqa: PLC0415

    recorded = cli_gates.load(run_id).decisions[CONFIRM]
    assert envelope["data"]["digest"] == recorded.digest, (
        f"the report's digest is not the one the decision carries; the gate was "
        f"offered {offered.get('gate')!r}"
    )
