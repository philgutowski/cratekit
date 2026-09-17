"""U27: the two restore verbs, and the ONE session that spans them.

WHY THIS FILE EXISTS SEPARATELY FROM THE CONFORMANCE SUITE. THREE of the nine
conformance properties actually arm against these verbs, not nine, and the
difference is worth stating because the shorter claim was made here first and an
independent review measured it: six identifiers mention ``[restore.list]`` and
seven mention ``[restore.run]``, which is properties 1, 2 and 3 plus one gate
walk. The others are AST sweeps over the package or are parametrized over a
population these entries are not in.

Every one of those three drives the EMPTY path: a library with no session log, no
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
from datetime import timedelta
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import exit_codes as reservations
from cratekit.cli import registry
from cratekit.core import config, jobs, preflight, rb_writer, restore, session, snapshot
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode, Remedy
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


def _offered_digest(refused: dict) -> str:
    """The digest the run RECORDED as offered, read off the run rather than the message.

    Through ``cli.gates`` because that is the value a later decision is compared
    against. The refusal envelope carries the gate and its options; the digest
    lives on the run, which is the whole point of it, so reading it from the
    envelope would measure a message and not the thing that makes an answer go
    stale. Non-empty is asserted here so a handler that offered nothing at all
    fails as a missing digest rather than as two equal absences.
    """
    from cratekit.cli import gates as cli_gates  # noqa: PLC0415

    offered = cli_gates.load(refused["run_id"]).offers.get(CONFIRM, "")
    assert offered, "the run recorded no digest for the confirmation gate"
    return offered


def _fake_rclone(cfg_value, monkeypatch) -> Path:
    """Put a stand-in for rclone on the ONE seam the product ships for it.

    ``CRATEKIT_BIN_RCLONE`` is ``core.binaries``'s per binary override, read
    before PATH, so what is replaced here is the external PROGRAM and nothing
    else: the argument parser, the gate flow, the session, the plan and the
    transfer construction are all the real ones. Patching a runner attribute
    cannot do this from a command line drive, because ``plan_restore`` binds its
    default runner at definition time and no flag reaches it.

    It answers ``lsf`` with one dated snapshot so a plan can be built, exits 0 on
    everything else, and appends each invocation to a log the caller reads. The
    log is what the assertions are taken over, so what is measured is the
    program's own view of what it was asked to do.
    """
    home = Path(config.installation_state_dir())
    home.mkdir(parents=True, exist_ok=True)
    log = home / "rclone-invocations.log"
    program = home / "fake-rclone"
    program.write_text(
        "#!/bin/sh\n"
        f'printf "%s\\n" "$*" >> "{log}"\n'
        'case " $* " in *" lsf "*) echo "2026-08-01T000000Z/" ;; esac\n'
        "exit 0\n"
    )
    program.chmod(0o755)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(program))
    del cfg_value
    return log


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
    database = config.state_path("rekordbox_db", cfg).name
    restored = tuple(
        sidecar.suffix
        for sidecar in config.state_file("rekordbox_db").sidecars
        if sidecar.restored
    )
    listing = "".join([database + "\n", *(database + suffix + "\n" for suffix in restored)])

    report = restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=lambda command: backup.CommandResult(
            returncode=0,
            stdout=listing if command.label == backup.LIST_SNAPSHOT_CONTENTS else "",
        ),
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    # DERIVED FROM THE STATE INVENTORY INTERSECTED WITH THE SNAPSHOT, NOT FROM
    # THE REPORT. Both of these assertions used to take their expected value from
    # ``report.pulled``, which made them X equals X: an independent reviewer's
    # mutation deduplicating the transfer labels killed nothing, because both
    # sides moved together. The inventory is the same declaration ``plan_restore``
    # reads to decide which companions MAY come back, and the listing is what
    # this snapshot actually holds, so together they are the honest independent
    # source for how many transfers a database restore is made of: the database
    # itself, plus one per sidecar the schema marks as restored AND the snapshot
    # holds. This listing holds every restored sidecar so the inventory is still
    # what moves the count.
    expected = 1 + len(restored)
    assert expected > 1, "the inventory restores no sidecar, so this pins nothing"

    assert report.outcome is None
    assert report.pulled == (backup.RESTORE_DATABASE,) * expected
    assert report.absent == ()

    payload = restore_cli._performed(report, {"digest": "d"})
    assert payload["totals"]["transfers"] == expected
    assert payload["totals"]["absent_sidecars"] == []
    assert [item["half"] for item in payload["items"]] == ["off-machine"] * expected
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
    """A typo gets a sentence about the identifier, not a traceback and not silence.

    RECORDED AGAINST A LIBRARY THAT HAS A SESSION, which is the whole measurement
    and which the first version of this test did not do. Over an EMPTY log the
    refusal is unavoidable: there is no other session to fall through to, so a
    handler that silently restored the newest one instead of refusing the named
    one would pass. Measured on the author's own table, row
    N2_an_unknown_identifier_is_not_refused: falling through to the newest
    session killed ZERO tests across the whole suite before this line existed,
    which is a person typing one character wrong and having a different session
    restored over their library.
    """
    recorded, _captured = completed_session(installed)

    code, envelope = _drive(["restore", "run", "no-such-session"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert code != int(ExitCode.USAGE)
    assert "no-such-session" in envelope["cause"]["message"]
    assert recorded.session_id not in envelope["cause"]["message"], (
        "the refusal names a session the person did not ask for"
    )


def test_a_rehearsal_neutralizes_the_mirror_transfers_too(cfg, tmp_path):
    """The dry run reaches BOTH halves, measured on the argv the runner is handed.

    Measured on the author's own table, row
    S7_a_rehearsal_performs_the_mirror_pull: hard coding the off-machine half to
    ``dry_run=False`` killed ZERO tests across the whole suite. The dry run test
    that existed drove only the capture half, so a rehearsal that transferred
    hundreds of gigabytes for real would have passed every assertion in this
    file.
    """
    acknowledge(cfg)
    (tmp_path / "recovered").mkdir()
    seen: list[tuple[str, ...]] = []

    def runner(command):
        seen.append(tuple(command.argv))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        dry_run=True,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    transfers = [argv for argv in seen if "copy" in argv]
    assert transfers, "the rehearsal described no transfer at all"
    for argv in transfers:
        assert "--dry-run" in argv, (
            f"a rehearsal handed the transfer {argv} with nothing neutralizing it"
        )


def test_the_mirror_is_pulled_before_the_capture_is_spent(cfg):
    """The order is the reason the two halves compose, and it is not asserted elsewhere.

    Measured on the author's own table, row S5_the_off_machine_half_runs_second:
    performing the capture restore FIRST killed ZERO tests. That order overwrites
    the session a person just restored with whatever the remote happened to hold,
    which is the failure the composition exists to avoid rather than a cosmetic
    sequencing choice.

    THE FIRST VERSION OF THIS TEST MEASURED THE END STATE AND STILL DIED AT ZERO.
    It stamped the database from inside the runner and compared the bytes
    afterwards, which a mutation that ran the capture restore BOTH before and
    after the pull satisfies exactly, because the last write is the capture
    either way. An end state cannot see an order. What is measured now is the
    world AS THE MIRROR RUNS: at that moment the database must still hold the
    live bytes, because the capture restore has not happened yet. Re-measured
    after the change and the row kills.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    database = config.state_path("rekordbox_db", cfg)
    live = b"database, generation two, written after the capture"
    database.write_bytes(live)
    observed: list[bytes] = []

    def runner(command):
        observed.append(database.read_bytes())
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    restore_cli.restore_under_one_session(
        cfg,
        session_id=record.session_id,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    assert observed, "the mirror half never ran, so no order was measured"
    assert observed[0] == live, (
        "the database had already been replaced when the mirror pull began, so "
        "the capture was spent first and the remote is about to land on top of it"
    )
    assert database.read_bytes() != live, (
        "the capture half never ran at all, so the order above is vacuous"
    )


def test_the_session_watches_the_whole_library_and_not_a_folder_inside_it(cfg):
    """The analysis watch names the library root, driven rather than read.

    Measured on the author's own table, rows S3 and S4: arming the watch on no
    roots at all, and arming it on the Music folder alone, each killed ZERO
    tests. A restore replaces the database and everything coupled to it, so
    anything under the library can move, and a watch that names nothing watches
    nothing while still reporting a clean session, which is worse than an absent
    guard because the report reads the same either way.

    THE COMPOSITE IS THE SECOND ASSERTION. The first says which root was armed;
    the second mutates the world the guard is over, by writing under the library
    but outside Music, and shows the armed watch is wide enough to be over it.
    """
    acknowledge(cfg)
    armed: list[tuple] = []
    real = restore.recovery_session

    def recording(cfg_value, **kwargs):
        armed.append(tuple(str(root) for root in kwargs.get("analysis_roots", ())))
        return real(cfg_value, **kwargs)

    record, _captured = completed_session(cfg)
    outside_music = Path(cfg.library.root) / "db"
    assert outside_music.is_dir(), "the fixture has no library directory outside Music"

    import unittest.mock  # noqa: PLC0415

    with unittest.mock.patch.object(restore, "recovery_session", recording):
        restore_cli.restore_under_one_session(
            cfg, session_id=record.session_id, **gate_seams(cfg)
        )

    assert armed == [(str(Path(cfg.library.root)),)], (
        f"the session was armed over {armed} rather than over the library root"
    )
    watched = Path(armed[0][0])
    assert outside_music != watched and watched in outside_music.parents, (
        "the armed root does not contain the part of the library a restore "
        "writes to, so the watch is narrower than the blast radius"
    )


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


def test_the_digest_moves_when_the_discard_set_moves(installed):
    """A wider destruction is a different decision, and the digest has to say so.

    Measured on the author's own table, row
    O2_the_discard_set_leaves_the_digest: dropping the discard list out of the
    digested offer killed ZERO tests. The cost is specific. A person approves
    restoring to a session while naming one later session they accept losing;
    with the list outside the digest, a second invocation naming three more
    sessions matches the recorded decision exactly and destroys work the person
    never agreed to lose.
    """
    target, _captured = completed_session(installed, started="2026-08-01T00:00:00+00:00", stamp="a")
    later, _second = completed_session(installed, started="2026-08-02T00:00:00+00:00", stamp="b")

    _code, narrow = _drive(["restore", "run", target.session_id])
    _code, wide = _drive(
        ["restore", "run", target.session_id, "--discard", later.session_id]
    )

    assert _offered_digest(narrow) != _offered_digest(wide), (
        "naming a session to discard did not move the digest, so a decision "
        "recorded against the narrow restore is honoured against the wide one"
    )


def test_the_digest_moves_when_the_mirror_half_is_added(installed):
    """Approving one session must not also authorise pulling a mirror off the network.

    Measured on the author's own table, row
    O3_the_off_machine_half_leaves_the_digest: dropping the off-machine item out
    of the digested offer killed ZERO tests. The two halves have very different
    costs, the mirror being hundreds of gigabytes over somebody's connection, and
    a digest that cannot tell them apart lets a decision made about the cheap one
    be honoured against the expensive one.
    """
    record, _captured = completed_session(installed)

    _code, capture_only = _drive(["restore", "run", record.session_id])
    _code, with_mirror = _drive(["restore", "run", record.session_id, "--from-backup"])

    assert _offered_digest(capture_only) != _offered_digest(with_mirror), (
        "adding the mirror half did not move the digest"
    )


def test_the_confirmation_gate_is_found_by_digest_source_and_not_by_position(installed):
    """The handler asks the gate the entry DIGESTS, whichever order they are written in.

    Measured on the author's own table, row G1_gate_found_by_position: taking
    ``gates[0]`` killed ZERO tests, and the reason is that the two declared gates
    happen to be written confirm-first today. That makes the guard true by
    coincidence, and the day somebody reorders the declaration the handler asks
    the cloud-sync question against a restore digest and the confirmation is
    never asked at all.

    DRIVEN OVER A REVERSED ENTRY rather than argued, so what is measured is the
    handler's selection and not the registry's current spelling.
    """
    entry = registry.entry("restore.run")
    reversed_entry = replace(entry, gates=tuple(reversed(entry.gates)))
    assert [spec.name for spec in reversed_entry.gates] != [
        spec.name for spec in entry.gates
    ], "the entry declares fewer than two gates, so this measures nothing"

    chosen = restore_cli._confirm_gate(reversed_entry)

    assert chosen.digest_source == "plan"
    assert chosen.name == CONFIRM
    assert chosen is not reversed_entry.gates[0], (
        "the handler took the first gate, which is the confirmation only by "
        "the order the entry happens to be written in"
    )


def test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default(
    cfg, tmp_path
):
    """The per-slug answer survives, which is the whole reason the table holds one.

    Measured on the author's own table, row
    R2_the_reserved_remediation_is_replaced_by_the_class_default: swapping the
    reserved remediation for ``report-defect`` killed ZERO tests. The cost is a
    person with an unconfigured remote being told to file a bug, and a person
    with no snapshot on the remote being told the same thing, when the
    reservation table already holds a different and correct sentence for each.
    """
    acknowledge(cfg)
    unconfigured = _without_remote(cfg)
    with pytest.raises(CratekitError) as excinfo:
        restore_cli.restore_under_one_session(
            unconfigured,
            session_id=None,
            from_backup=True,
            target=tmp_path,
            **gate_seams(cfg),
        )

    slug = str(backup.Refusal.REMOTE_NOT_CONFIGURED)
    expected = reservations.remediation_for(slug)
    got = excinfo.value.cause.remediation
    assert (got.remedy, got.steps) == (expected.remedy, expected.steps), (
        f"the refusal carries {got!r} rather than the reservation table's "
        f"{expected!r}, so the per-slug answer was discarded"
    )
    assert got.remedy != Remedy.REPORT_DEFECT, (
        "an unconfigured remote is not a defect in this program"
    )


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


# ═══════════════════════════════════════════════════════════════════════════
# Fix round 2: the two blocking findings an independent review drove, and the
# command-line coverage whose absence was the cause of eleven of its zero rows.
# ═══════════════════════════════════════════════════════════════════════════


def test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen(cfg):
    """BLOCKING finding 1, driven, and the measurement is what a person was told.

    ``backup.run_restore`` returned its results unread. The verb then built its
    report from the PLAN's command labels, so a restore whose every copy failed
    came back as two completed transfers and exit OK. That is not a cosmetic
    misreport: the live companion files are cleared BEFORE the first command, and
    the write-ahead log holds transactions committed since the last checkpoint,
    which are in no capture by construction. Measured before the fix: the log was
    deleted, the database was unchanged, and the person was told the restore had
    happened.

    THE RUNNER FAILS THE COPY AND NOT THE LISTING, which is the shape of the real
    condition: the remote is reachable enough to plan against, then the transfer
    fails on an expired token or a dropped connection.
    """
    acknowledge(cfg)
    database = config.state_path("rekordbox_db", cfg)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"transactions committed since the last checkpoint")

    def failing(command):
        if "lsf" in command.argv:
            return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")
        return backup.CommandResult(returncode=1, stdout="", stderr="connection refused")

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.restore_under_one_session(
            cfg,
            session_id=None,
            from_backup=True,
            snapshot="2026-08-01T000000Z",
            runner=failing,
            process_lister=lambda: (),
            **gate_seams(cfg),
        )

    cause = excinfo.value.cause
    assert cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert cause.code is not ExitCode.INTERNAL, (
        "an unreachable remote is not a defect in this program"
    )
    assert backup.RESTORE_DATABASE in cause.message, (
        "the refusal does not name which transfer failed"
    )
    assert cause.remediation.steps, (
        "the person is told the restore failed and not what to do about it"
    )
    # THE STATE THE REFUSAL LEAVES, ASSERTED RATHER THAN ASSUMED. The clearing is
    # the safety property the ordering exists for and is not undone, so what the
    # message promises about the world has to be true of the world.
    assert not wal.exists()
    assert str(wal.name) in cause.message or "companion" in cause.message


def test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass(cfg):
    """The same defect, one branch over, found by asking what else had the shape.

    ``run_restore``'s dry run branch returned its results unread exactly as the
    real branch did. It is not the lesser case: that function's own docstring
    argues a rehearsal is worth running because "a rehearsal that passes is then
    evidence the real run will reach its work", and that claim is false the
    moment a failing preview reports as a passing one. A person rehearses
    precisely to find out whether the remote is reachable.

    NOTHING IS CLEARED ON THIS PATH, which the refusal must not claim otherwise.
    A dry run performs nothing at all, including the clearing, so the live
    companions are still there.
    """
    acknowledge(cfg)
    database = config.state_path("rekordbox_db", cfg)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"still here, because a rehearsal clears nothing")

    def failing(command):
        if "lsf" in command.argv:
            return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")
        return backup.CommandResult(returncode=1, stdout="", stderr="connection refused")

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.restore_under_one_session(
            cfg,
            session_id=None,
            dry_run=True,
            from_backup=True,
            snapshot="2026-08-01T000000Z",
            runner=failing,
            process_lister=lambda: (),
            **gate_seams(cfg),
        )

    assert excinfo.value.cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert wal.exists(), "a rehearsal cleared the live companion files"


def test_a_transfer_that_succeeds_is_still_reported(cfg):
    """The other direction, so the refusal above is not simply a verb that refuses.

    A guard that fires on every run is indistinguishable from a broken verb, and
    a test that only drove the failure could not tell those apart.
    """
    acknowledge(cfg)

    report = restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        runner=lambda command: backup.CommandResult(returncode=0, stdout=""),
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    assert report.pulled, "a run whose every transfer succeeded reported nothing"


def test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar(cfg, tmp_path):
    """R-367 at the report a person reads.

    The snapshot this product takes holds ``master.db`` alone. The restore used
    to copy the write ahead log anyway, rclone exited 3, and the verb reported
    failure after the database had already landed.
    """
    acknowledge(cfg)
    (tmp_path / "recovered").mkdir()
    database = config.state_path("rekordbox_db", cfg).name

    report = restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=lambda command: backup.CommandResult(
            returncode=0,
            stdout=(database + "\n") if command.label == backup.LIST_SNAPSHOT_CONTENTS else "",
        ),
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    assert report.pulled == (backup.RESTORE_DATABASE,)
    assert report.absent == ("-wal",)
    payload = restore_cli._performed(report, {"digest": "d"})
    assert payload["totals"]["transfers"] == 1
    assert payload["totals"]["absent_sidecars"] == ["-wal"]


def test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect(installed):
    """BLOCKING finding 2, with its producer DRIVEN rather than hand mutated.

    THE PRODUCER IS THIS PRODUCT'S OWN RETENTION. ``restore.prune`` deletes a
    capture directory while the session record stays in the log, which is the
    ordinary end state of every library that keeps history bounded. Before the
    fix, ``restore list`` explained that state correctly in a sentence and
    ``restore run`` on the same session exited 1 with ``internal-error`` and
    ``report-defect`` carrying a raw errno: a person told to file a bug about a
    directory the tool removed on purpose.

    THE TWO SURFACES NOW SAY THE SAME SENTENCE, because it is computed once, in
    ``Restorable.unusable``, and both read it rather than each inventing one.
    """
    acknowledge(installed)
    record, captured = completed_session(installed)
    removed = restore.prune(
        installed, policy=restore.RetentionPolicy(keep=0, max_age=timedelta(0))
    )
    assert removed and not captured.root.exists(), (
        "retention removed nothing, so the state under test was never produced"
    )

    _code, listing = _drive(["restore", "list"])
    row = listing["data"]["items"][0]
    assert row["restorable"] is False
    sentence = row["unusable"]
    assert sentence, "the listing explains nothing, so there is nothing to agree with"

    code, envelope = _drive(["restore", "run", record.session_id])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-record-unusable"
    assert envelope["cause"]["remediation"]["remedy"] != str(Remedy.REPORT_DEFECT), (
        "a person is told to report a defect for a capture this product deleted"
    )
    assert sentence in envelope["cause"]["message"], (
        "the two surfaces give different accounts of one state"
    )


def test_an_unusable_capture_is_refused_before_the_mirror_moves_a_byte(cfg):
    """The half of finding 2 that costs something, and it is the ordering.

    With ``--from-backup`` the off machine half runs FIRST, so a refusal deferred
    to the plan let every transfer complete and the live companion files be
    cleared before anything asked whether the capture could be spent at all. The
    refusal now happens before any session opens, so the runner is never reached.
    """
    acknowledge(cfg)
    record, captured = completed_session(cfg)
    restore.prune(cfg, policy=restore.RetentionPolicy(keep=0, max_age=timedelta(0)))
    assert not captured.root.exists()
    ran: list[str] = []

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.restore_under_one_session(
            cfg,
            session_id=restore_cli._named(cfg, record.session_id).session_id,
            from_backup=True,
            runner=lambda command: ran.append(command.label),
            **gate_seams(cfg),
        )

    assert excinfo.value.cause.reason == "restore-record-unusable"
    assert ran == [], f"the mirror ran before the capture was checked: {ran}"


# ── the command-line surface the review found had none ───────────────────────


def test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher(
    installed, monkeypatch
):
    """``--from-backup``, driven end to end, which nothing did before.

    Eleven of the independent review's twenty one user facing zero rows were
    this: the three off machine flags appeared in no test, so the wiring could be
    changed freely with the suite green. The seam replaced here is the external
    program and nothing else, so the argument parser, the gate flow, the session
    and the plan are all the real ones.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    _code, refused = _drive(["restore", "run", "--from-backup"])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])

    assert code == int(ExitCode.OK), envelope
    invoked = log.read_text().splitlines() if log.exists() else []
    assert invoked, "the flag was accepted and no transfer was ever attempted"
    copies = [line for line in invoked if " copy " in f" {line} "]
    assert envelope["data"]["totals"]["transfers"] == len(copies), (
        f"the report claims {envelope['data']['totals']['transfers']} transfers and "
        f"the program was asked to copy {len(copies)} times"
    )
    assert all(item["half"] == "off-machine" for item in envelope["data"]["items"])


def test_without_the_flag_no_transfer_is_attempted_at_all(installed, monkeypatch):
    """The other direction, so the test above is not passing on a verb that always pulls.

    Measured on the review's own row: forcing the off machine half on for every
    run killed nothing, because no test ever established that a plain restore
    does not touch the network.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    _code, refused = _drive(["restore", "run"])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run"])

    assert code == int(ExitCode.OK), envelope
    invoked = log.read_text().splitlines() if log.exists() else []
    assert invoked == [], f"a restore nobody asked to pull reached the remote: {invoked}"


def test_include_mirror_adds_the_file_half_and_its_absence_leaves_it_out(cfg):
    """The flag that decides whether hundreds of gigabytes move, pinned both ways.

    Measured on the review's own row: forcing the mirror on for every run killed
    nothing. The two directions are asserted together because either one alone
    passes over a flag that is ignored.
    """
    acknowledge(cfg)
    captured: dict[bool, list[str]] = {}

    for wanted in (False, True):
        labels: list[str] = []

        def runner(command, sink=labels):
            sink.append(command.label)
            return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")

        restore_cli.restore_under_one_session(
            cfg,
            session_id=None,
            from_backup=True,
            include_mirror=wanted,
            snapshot="2026-08-01T000000Z",
            runner=runner,
            process_lister=lambda: (),
            **gate_seams(cfg),
        )
        captured[wanted] = labels

    assert backup.RESTORE_MIRROR in captured[True]
    assert backup.RESTORE_MIRROR not in captured[False], (
        "the mirror was pulled by a run that did not ask for it"
    )


def test_the_snapshot_flag_chooses_which_dated_snapshot_is_pulled(cfg):
    """``--snapshot``, pinned on the argv the transfer is actually given.

    Measured on the review's own row: ignoring the flag and always taking the
    newest killed nothing, because no test ever read the path a transfer was
    handed.
    """
    acknowledge(cfg)
    seen: list[tuple[str, ...]] = []

    def runner(command):
        seen.append(tuple(command.argv))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")

    restore_cli.restore_under_one_session(
        cfg,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-02T111111Z",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(cfg),
    )

    copies = [argv for argv in seen if "copy" in argv]
    assert copies, "no transfer was attempted"
    assert all("2026-08-02T111111Z" in " ".join(argv) for argv in copies), (
        f"the named snapshot did not reach the transfer: {copies}"
    )


# ── the two properties nothing pinned at either layer ─────────────────────────


def test_the_default_takes_the_newest_of_several_spendable_captures(cfg):
    """Newest FIRST, pinned where reversing the order can actually be seen.

    The independent review's strongest zero: reversing this module's walk over
    the listing killed nothing, and so did reversing ``list_sessions``'s own
    ordering one layer down. Both rows were inert because the only spendable
    session in the fixture the older test built was ALSO the oldest, so newest
    and oldest were the same row. Two spendable sessions is the smallest fixture
    in which the two answers differ.
    """
    older, _first = completed_session(cfg, started="2026-08-01T00:00:00+00:00", stamp="a")
    newer, _second = completed_session(cfg, started="2026-08-02T00:00:00+00:00", stamp="b")
    assert older.session_id != newer.session_id

    chosen = restore_cli._newest_restorable(cfg)

    assert chosen is not None
    assert chosen.session_id == newer.session_id, (
        f"the default took {chosen.session_id}, which is not the newest spendable "
        f"capture of the two"
    )


def test_a_capture_that_exists_but_is_unverified_is_not_spendable(cfg):
    """The VERIFIED half of spendable, which nothing pinned at either layer.

    A capture whose manifest is present and whose integrity check never passed is
    exactly the capture a restore must not reach for by default: the files are
    there and nothing has established they are the files. Measured on the
    review's own rows, widening ``restorable`` to drop this half killed nothing.
    """
    record, captured = completed_session(cfg)
    only = restore_cli._newest_restorable(cfg)
    assert only is not None and only.session_id == record.session_id, (
        "the fixture's own capture is not spendable, so this pins nothing"
    )

    manifest = captured.root / snapshot.MANIFEST_NAME
    document = json.loads(manifest.read_text())
    assert document.get("integrity_verified") is True, (
        "the fixture's capture was never verified, so clearing the flag pins nothing"
    )
    document["integrity_verified"] = False
    manifest.write_text(json.dumps(document))

    assert restore_cli._newest_restorable(cfg) is None, (
        "an unverified capture was offered as the default restore target"
    )

