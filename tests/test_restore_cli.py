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
import shutil
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


#: The fake remote's two listings, as files beside the fake program.
REMOTE_SNAPSHOTS = "fake-remote-snapshots"
REMOTE_MARKERS = "fake-remote-markers"
#: "Marked for the library under test", as distinct from None, which is unmarked.
OWN = object()
STAMP = "2026-08-01T000000Z"


def _fake_rclone(cfg_value, monkeypatch, *, snapshots=(STAMP,), marker=OWN) -> Path:
    """Put a stand-in for rclone on the ONE seam the product ships for it.

    ``CRATEKIT_BIN_RCLONE`` is ``core.binaries``'s per binary override, read
    before PATH, so what is replaced here is the external PROGRAM and nothing
    else: the argument parser, the gate flow, the session, the plan and the
    transfer construction are all the real ones. Patching a runner attribute
    cannot do this from a command line drive, because ``plan_restore`` binds its
    default runner at definition time and no flag reaches it.

    It answers the three listings a restore makes, exits 0 on everything else,
    and appends each invocation to a log the caller reads. The log is what the
    assertions are taken over, so what is measured is the program's own view of
    what it was asked to do.

    THE THREE LISTINGS ARE TOLD APART, which the first version of this did not
    do: it answered every ``lsf`` with one dated folder, and that was enough
    while nothing read a snapshot's identity. The dated folders and the identity
    markers are read from two files ``_remote_holds`` rewrites, so a test can
    move the remote BETWEEN the two acts of one restore, which is the only way
    to drive what a backup landing in that window does.
    """
    home = Path(config.installation_state_dir())
    home.mkdir(parents=True, exist_ok=True)
    log = home / "rclone-invocations.log"
    program = home / "fake-rclone"
    program.write_text(
        "#!/bin/sh\n"
        f'printf "%s\\n" "$*" >> "{log}"\n'
        'case " $* " in\n'
        f'  *" lsf "*" --dirs-only "*) cat "{home / REMOTE_SNAPSHOTS}"\n'
        f'    if [ -f "{home / REMOTE_SNAPSHOTS}.next" ]; then\n'
        f'      mv "{home / REMOTE_SNAPSHOTS}.next" "{home / REMOTE_SNAPSHOTS}"; fi ;;\n'
        '  *" lsf "*"/db/ "*) ;;\n'
        f'  *" lsf "*) cat "{home / REMOTE_MARKERS}" ;;\n'
        "esac\n"
        "exit 0\n"
    )
    program.chmod(0o755)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(program))
    _remote_holds(snapshots, marker=marker, cfg_value=cfg_value)
    return log


def _remote_holds(snapshots, *, marker=OWN, cfg_value=None) -> None:
    """Say what the fake remote lists from now on. Callable between two acts.

    ONE MARKER FOR EVERY SNAPSHOT, because the fake program does not read which
    dated folder it was asked about. That is enough for every test here and it
    is a limit worth stating: no test in this file can hold one marked and one
    unmarked snapshot at once, and the engine's own suite is where that is driven.
    """
    home = Path(config.installation_state_dir())
    (home / REMOTE_SNAPSHOTS).write_text("".join(f"{name}/\n" for name in snapshots))
    if marker is OWN:
        marker = cfg_value.library.volume_id
    name = backup.identity_marker(marker) if marker is not None else None
    (home / REMOTE_MARKERS).write_text(f"{name}\n" if name else "")


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


def test_the_digest_moves_when_the_mirror_half_is_added(installed, monkeypatch):
    """Approving one session must not also authorise pulling a mirror off the network.

    Measured on the author's own table, row
    O3_the_off_machine_half_leaves_the_digest: dropping the off-machine item out
    of the digested offer killed ZERO tests. The two halves have very different
    costs, the mirror being hundreds of gigabytes over somebody's connection, and
    a digest that cannot tell them apart lets a decision made about the cheap one
    be honoured against the expensive one.
    """
    record, _captured = completed_session(installed)
    # The offer now asks the remote which snapshot it is offering, so the
    # off-machine half needs a remote to ask.
    _fake_rclone(installed, monkeypatch)

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
    """The report a person reads names the sidecar the snapshot did not hold.

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


@pytest.mark.parametrize(
    ("listing", "pulled", "word"),
    [
        ("PIONEER/\n", (backup.RESTORE_DATABASE, backup.RESTORE_SHARE), "pulled"),
        ("", (backup.RESTORE_DATABASE,), "absent"),
    ],
)
def test_a_restore_in_the_outside_layout_says_whether_the_share_came_back(
    cfg, tmp_path, listing, pulled, word
):
    """R-338 at the report a person reads: the grids arrived, or it says they did not.

    A backup taken before the share was carried holds no mirror of it. Rows
    restored from one look fine and have no analysis, so the totals name it.
    """
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    (home / "master.db").write_bytes(b"live")
    outside = replace(
        cfg,
        library=replace(
            cfg.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-20",
        ),
    )
    acknowledge(outside)
    (tmp_path / "recovered").mkdir()

    def runner(command):
        answers = {backup.LIST_SNAPSHOT_CONTENTS: "master.db\n", backup.LIST_SHARE: listing}
        return backup.CommandResult(returncode=0, stdout=answers.get(command.label, ""))

    report = restore_cli.restore_under_one_session(
        outside,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        target=tmp_path / "recovered",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(outside),
    )

    assert report.pulled == pulled
    assert report.share == word
    totals = restore_cli._performed(report, {"digest": "d"})["totals"]
    assert totals["analysis_share"] == word


def test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean(
    cfg, tmp_path
):
    """Driven against the REAL analysis watch, with a runner that really writes.

    The first version of this pulled the share on every outside restore. On the
    live path that put analysis files under the watched library root, and the
    session closed refused as moved analysis files after the database had
    already been replaced. The runner below writes a grid wherever a share
    transfer is aimed, so a pull that came back would fail this the same way.
    """
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    (home / "master.db").write_bytes(b"live")
    outside = replace(
        cfg,
        library=replace(
            cfg.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-20",
        ),
    )
    acknowledge(outside)

    def runner(command):
        if command.label == backup.RESTORE_SHARE:
            grid = Path(command.argv[3]) / "PIONEER" / "USBANLZ" / "8d2" / "k" / "ANLZ0000.DAT"
            grid.parent.mkdir(parents=True, exist_ok=True)
            grid.write_bytes(b"PMAI")
        answers = {backup.LIST_SNAPSHOT_CONTENTS: "master.db\n", backup.LIST_SHARE: "PIONEER/\n"}
        return backup.CommandResult(returncode=0, stdout=answers.get(command.label, ""))

    report = restore_cli.restore_under_one_session(
        outside,
        session_id=None,
        from_backup=True,
        snapshot="2026-08-01T000000Z",
        runner=runner,
        process_lister=lambda: (),
        **gate_seams(outside),
    )

    assert report.pulled == (backup.RESTORE_DATABASE,)
    assert report.share == "withheld"
    assert not list(Path(outside.library.root).rglob("ANLZ*"))


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



# ── R-368: a restore into a directory that is not the live library ────────────
#
# The verb could restore to exactly one place, the live library root, so the
# rehearsal a person runs BEFORE they need a restore was a session's script
# calling the engine with its ``target`` seam set. The flag below is that seam
# made reachable, and every property here is about the two things that made it
# unsafe to expose: a target that is the live library by another name, and a
# target beside a capture rollback, which can only ever be performed on the live
# library and would put the two halves of one restore on two volumes.


def _sidecars_beside(path: Path) -> tuple[Path, ...]:
    """The live companion files, written so a run that clears them can be seen.

    The suffixes come from the state inventory rather than from a literal here,
    which is the same declaration ``plan_restore`` reads to decide what a restore
    clears. A literal pair would keep passing on the day the inventory grows a
    third.
    """
    written = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        beside = path.with_name(path.name + sidecar.suffix)
        beside.write_bytes(b"live companion, not this restore's business")
        written.append(beside)
    assert written, "the inventory declares no companion, so this pins nothing"
    return tuple(written)


def _copy_destinations(log: Path) -> list[str]:
    """Where the program was asked to put each file, read off its own invocations."""
    lines = log.read_text().splitlines() if log.exists() else []
    return [line.split()[-1] for line in lines if " copy " in f" {line} "]


def test_a_target_restores_the_database_into_the_directory_it_names(
    installed, tmp_path, monkeypatch
):
    """The close condition, driven through the dispatcher onto a scratch directory.

    TWO MEASUREMENTS, because either alone passes over a flag that is read and
    then dropped. The first is where the transfer was pointed, taken off the
    program's own invocation log. The second is the live companion files, which
    are the cost of getting this wrong: ``run_restore`` clears the companions
    beside the database it is about to replace, so a rehearsal whose target was
    ignored deletes the live write-ahead log, and that log holds transactions
    committed since the last checkpoint, which are in no capture by construction.
    A rehearsal that destroys the one thing no backup holds is worse than no
    rehearsal.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)
    scratch = tmp_path / "rehearsal"
    scratch.mkdir()
    live = config.state_path("rekordbox_db", installed)
    companions = _sidecars_beside(live)

    _code, refused = _drive(["restore", "run", "--from-backup", "--target", str(scratch)])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", "--from-backup", "--target", str(scratch)]
    )

    assert code == int(ExitCode.OK), envelope
    destinations = _copy_destinations(log)
    assert destinations, "the flag was accepted and no transfer was ever attempted"
    assert all(place.startswith(str(scratch.resolve())) for place in destinations), (
        f"a restore asked for {scratch} was pointed at {destinations}"
    )
    assert all(beside.exists() for beside in companions), (
        "the rehearsal cleared the LIVE companion files beside the live database, "
        "which is the work no capture holds"
    )
    assert live.read_bytes() == b"database, generation one"


def test_a_target_that_is_the_library_root_is_refused(installed, monkeypatch):
    """The first destination check, over the spelling a person reaches for first.

    ``--target`` pointed at the library is not a rehearsal, it is the live
    restore with extra typing, and the two have different gates ahead of them in
    every direction this unit could grow. Refused rather than quietly accepted as
    a synonym, because a synonym is what makes the next check, the one below
    about where the database lands, look redundant.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    code, envelope = _drive(
        ["restore", "run", "--from-backup", "--target", str(installed.library.root)]
    )

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-target-is-live-root"
    assert not log.exists(), "the remote was reached by a run that is refused"


@pytest.mark.parametrize(
    "where, why",
    [
        ("inside", "a directory underneath the library root"),
        ("above", "the directory the library root sits in"),
    ],
)
def test_a_target_that_holds_the_library_or_sits_in_it_is_refused(
    installed, where, why
):
    """The rest of the containment check, which equality alone does not cover.

    A target INSIDE the library restores a database onto the volume the whole
    rehearsal exists to leave alone, and one ABOVE it is the library's own parent,
    where ``--include-mirror`` would copy the mirror back over the live tree. Both
    are the live library under a different name, which is why they share the
    slug the exact root gets.
    """
    acknowledge(installed)
    root = Path(installed.library.root)
    named = root / "beneath" if where == "inside" else root.parent
    if where == "inside":
        named.mkdir()

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(named)])

    assert code == int(ExitCode.PRECONDITION), f"{why}: {envelope}"
    assert envelope["cause"]["reason"] == "restore-target-is-live-root", why
    assert envelope["cause"]["detail"]["check"] == "containment", why


def test_a_target_whose_database_lands_on_the_live_one_is_refused(
    installed, tmp_path, monkeypatch
):
    """The check the containment one cannot make, in the layout rekordbox ships.

    ``database_target_for`` rebases the CONFIGURED database onto the target, and
    a database that sits outside the library root has no position relative to it,
    so the honest answer is its own name at the top of the target. That makes the
    parent directory of a live database a target which is not the library root,
    is neither above nor below it, and still restores ``master.db`` over the live
    file in place.

    THE LAYOUT IS THE ACKNOWLEDGED ONE, not an invented configuration. It is what
    ``library.db_outside_root_acknowledged_on`` exists for and it is rekordbox's
    own default, so this is the common installation rather than the exotic one.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    outside = replace(
        installed,
        library=replace(
            installed.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-18",
        ),
    )
    config.save(outside)
    config.reset_cache()
    (home / "master.db").write_bytes(b"database, generation one")
    assert backup.database_target_for(outside, home) == config.state_path(
        "rekordbox_db", outside
    ), "the fixture does not reproduce the layout, so this pins nothing"
    assert not home.is_relative_to(outside.library.root), (
        "the database's directory is inside the library root here, so the "
        "containment check would refuse it and this measures that instead"
    )

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(home)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-target-is-live-root"
    assert envelope["cause"]["detail"]["check"] == "destination"
    assert not log.exists(), "the remote was reached by a run that is refused"
    # THE SENTENCE, not only the slug. Measured on the author's own table, row
    # R1_the_live_root_refusal_is_reworded: rewriting this message killed
    # nothing. A person who named their database's own directory sees the
    # message and not the slug, and what it has to tell them is WHERE the file
    # would go, because the directory they typed is not the path that moves.
    assert str(home / "master.db") in envelope["cause"]["message"], envelope
    assert "live database" in envelope["cause"]["message"], envelope


def test_a_target_with_no_off_machine_pull_is_refused(installed):
    """The flag names where a PULLED database goes, so it needs the pull.

    Accepted silently it would be inert, which is the shape ``--snapshot`` and
    ``--include-mirror`` still have one line up: a flag a person typed, that the
    verb read, and that changed nothing about what it did. Here that inertness
    is dangerous rather than merely untidy, because the run it silently becomes
    is a rollback of the live library.
    """
    acknowledge(installed)

    code, envelope = _drive(["restore", "run", "--target", "/somewhere/else"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-target-invalid"


@pytest.mark.parametrize("extra", [["--discard", "s-1"], []])
def test_a_target_beside_a_capture_rollback_is_refused(installed, extra):
    """Both halves on two volumes is the composition this refuses outright.

    The capture half resolves every path it writes from ``cfg.library.root`` and
    the plan refuses a session that does not authorise that root, so a run that
    took a target AND a session would put the database from the remote in the
    scratch directory and roll the live library's coupled state back at the same
    time. Nobody would ask for that, and before this refusal existed it was the
    natural spelling of "rehearse the restore of this session".

    ``--discard`` IS THE SAME REFUSAL, because it is a capture-half argument as
    well: it names sessions whose committed work a rollback destroys, and there
    is no rollback here to destroy them.
    """
    acknowledge(installed)
    record, _captured = completed_session(installed)
    named = [record.session_id] if not extra else []

    code, envelope = _drive(
        ["restore", "run", *named, "--from-backup", "--target", "/somewhere/else", *extra]
    )

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-target-invalid"


def test_a_target_run_rolls_no_session_back_even_by_default(installed, tmp_path, monkeypatch):
    """The OTHER way a capture reaches a run, which the refusal above cannot see.

    A bare ``restore run`` means the newest spendable capture, so a library with
    a restorable session and a person asking only for a rehearsal would have
    rolled that session back on the live library without naming it. The refusal
    above covers the session somebody TYPED. This covers the one the verb would
    have chosen for them.
    """
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)
    record, _captured = completed_session(installed)
    assert restore_cli._newest_restorable(installed) is not None, (
        "no capture is spendable here, so a default nobody suppressed would be "
        "None anyway and this pins nothing"
    )
    scratch = tmp_path / "rehearsal"
    scratch.mkdir()

    _code, refused = _drive(["restore", "run", "--from-backup", "--target", str(scratch)])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", "--from-backup", "--target", str(scratch)]
    )

    assert code == int(ExitCode.OK), envelope
    assert all(item["half"] == "off-machine" for item in envelope["data"]["items"])
    assert "converged" not in envelope["data"]["totals"], (
        f"a rehearsal reported on the capture restore's own question, so a "
        f"session was spent: {envelope['data']['totals']}"
    )
    assert record.session_id in {
        entry.session_id for entry in restore.list_sessions(installed)
    }


def test_the_digest_moves_when_the_restore_is_pointed_somewhere_else(
    installed, tmp_path, monkeypatch
):
    """A decision about a rehearsal must not be honoured against the live restore.

    The digest is the identity of what a person approved, and where the database
    lands is most of what they are approving. Without the target in it, an
    answer recorded against ``--from-backup --target /some/scratch`` matches a
    later ``--from-backup`` exactly, and the recorded decision authorises a
    restore over the live library that nobody agreed to.
    """
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)
    scratch = tmp_path / "rehearsal"
    scratch.mkdir()

    _code, live = _drive(["restore", "run", "--from-backup"])
    _code, rehearsal = _drive(
        ["restore", "run", "--from-backup", "--target", str(scratch)]
    )

    assert _offered_digest(live) != _offered_digest(rehearsal), (
        "pointing the restore at a scratch directory did not move the digest, so "
        "a decision made about the rehearsal is honoured against the live library"
    )


def test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal(
    installed, tmp_path, monkeypatch
):
    """The existing refusal, reached through the new flag rather than restated.

    ``plan_restore`` already refuses a target that is not a directory, with its
    own reserved slug and its own remediation, so the verb deliberately does not
    ask the question a second time: a guard covered by another guard is a guard
    nothing covers. What this measures is that the flag reaches that refusal
    rather than inventing a second sentence for the same fact.
    """
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)
    missing = tmp_path / "not-mounted"

    _code, refused = _drive(["restore", "run", "--from-backup", "--target", str(missing)])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", "--from-backup", "--target", str(missing)]
    )

    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == str(backup.Refusal.RESTORE_TARGET_ABSENT)


def test_a_rehearsal_is_still_refused_while_rekordbox_is_running(
    installed, tmp_path, monkeypatch
):
    """Today's live gates stay, which is half of what this unit promised.

    A restore into a scratch directory touches nothing rekordbox holds open, so
    this refusal is conservative rather than necessary, and it is kept on purpose:
    the gates are the ones the live restore passes, unchanged, and loosening them
    for a target is a decision with its own blast radius. That the rehearsal still
    takes the library lock and still needs rekordbox closed is recorded as a
    finding rather than claimed as the finished shape.
    """
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)
    scratch = tmp_path / "rehearsal"
    scratch.mkdir()

    _code, refused = _drive(["restore", "run", "--from-backup", "--target", str(scratch)])
    _answer(refused["run_id"], "restore")
    monkeypatch.setattr(
        "cratekit.core.processes.running_process_names", lambda: ("rekordbox",)
    )
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", "--from-backup", "--target", str(scratch)]
    )

    assert code == int(ExitCode.REKORDBOX_OPEN), envelope
    assert envelope["cause"]["reason"] == "rekordbox-running"


def test_a_relative_target_is_compared_as_the_place_it_names(installed, monkeypatch):
    """The resolution, measured where leaving it out actually costs something.

    A relative path compares equal to nothing: ``Path("library")`` is neither the
    configured root nor inside it, whatever directory the person is standing in.
    So a guard over the raw argument passes a target that IS the library root,
    typed from the directory above it, and the restore lands on the live
    database. The comparison is between two places on the disk, not two
    spellings.
    """
    acknowledge(installed)
    root = Path(installed.library.root)
    monkeypatch.chdir(root.parent)

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", root.name])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-target-is-live-root"
    # WHAT THE RESOLUTION ITSELF IS FOR, now that the filesystem answers the
    # comparison. Measured on the author's own table, row G7_target_not_resolved:
    # dropping the resolution killed nothing, because ``samefile`` stats a
    # relative path against the working directory and answers correctly without
    # it. What is left is the REPORT, and it is not nothing: a refusal that
    # echoes back the word somebody typed tells them their target is the library
    # without saying which directory that resolved to, which is the one fact
    # they do not already have.
    assert envelope["cause"]["detail"]["target"] == str(root), envelope


def _case_folds(where: Path) -> bool:
    """Whether this filesystem reads two spellings of one name as one directory.

    ASKED OF THE DIRECTORY THE TEST WILL USE, not of the platform. macOS ships
    APFS case insensitive and can be formatted case sensitive, and an external
    drive holding a library is frequently exFAT, so a check keyed on
    ``sys.platform`` would answer for the wrong volume on the machine it most
    matters on.
    """
    probe = where / "Case_Probe"
    probe.mkdir()
    try:
        return (where / "case_probe").is_dir()
    finally:
        probe.rmdir()


def test_a_differently_cased_library_root_is_still_the_library(
    installed, tmp_path, monkeypatch
):
    """The guard's own defect, found by this unit's review and driven here.

    ``Path.resolve`` followed by ``==`` or ``is_relative_to`` compares STRINGS.
    On a case insensitive filesystem, which is APFS as macOS ships it and exFAT
    on the external drive a DJ library normally lives on, the library root typed
    in another case is the same directory and both of those answer that the two
    paths are unrelated. Measured before the fix, through the real dispatcher:
    exit 0, the transfer pointed at the live database's own directory, and the
    live write-ahead log unlinked. The rehearsal destroyed the one thing no
    capture holds.

    BOTH FILESYSTEMS ARE ASSERTED rather than one being skipped, and neither is
    faked. Whether two spellings are one directory is a fact about the volume the
    test is running on, so a monkeypatched ``samefile`` would measure the stub;
    and a skip would make this whole property invisible on a machine where it
    happens not to hold, which is how a guard rots. Where the names are two
    places the refusal would be WRONG, so the expectation flips with the
    filesystem and the run says which branch it took.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)
    root = Path(installed.library.root)
    shouted = root.with_name(root.name.upper())
    assert str(shouted) != str(root), "the fixture's root is already upper case"
    live = config.state_path("rekordbox_db", installed)
    companions = _sidecars_beside(live)

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])

    if _case_folds(tmp_path):
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "restore-target-is-live-root"
        assert all(beside.exists() for beside in companions), (
            "a target spelled in another case was accepted and cleared the live "
            "companion files"
        )
        assert not log.exists(), "the remote was reached by a run that is refused"
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings as two directories, so "
            f"{shouted} is not the library and refusing it names the wrong fact"
        )


def test_a_differently_cased_database_directory_is_still_the_live_database(
    installed, tmp_path, monkeypatch
):
    """The same fold, on the destination check rather than on containment.

    The two checks compare different pairs of paths, so a fix on one of them is
    not a fix on the other. This is the acknowledged layout again, where the
    target is the live database's own directory and only the spelling differs.

    BOTH FILESYSTEMS AGAIN, for the reason the test above gives at length.
    """
    acknowledge(installed)
    home = tmp_path / "home" / "Rekordbox"
    home.mkdir(parents=True)
    outside = replace(
        installed,
        library=replace(
            installed.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-18",
        ),
    )
    config.save(outside)
    config.reset_cache()
    (home / "master.db").write_bytes(b"database, generation one")
    shouted = home.with_name(home.name.upper())
    assert str(shouted) != str(home)

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])

    if _case_folds(tmp_path):
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "restore-target-is-live-root"
        assert envelope["cause"]["detail"]["check"] == "destination"
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings as two directories, so the "
            f"database would land in {shouted} and not on the live one"
        )


def test_the_digest_moves_when_the_rehearsal_flag_does(installed):
    """The hole one flag over, found by this unit's review of the target.

    ``--dry-run`` walks every step and performs none, so it is the cheapest thing
    a person can be asked to approve. With it outside the digest, the decision
    recorded against a preview matched a later invocation without the flag
    exactly, and authorised a real restore over the live database. Driven before
    the fix: the answer given to the rehearsal was honoured, the run exited OK,
    one real copy landed on the live database and the live log was gone.
    """
    record, _captured = completed_session(installed)

    _code, preview = _drive(["restore", "run", record.session_id, "--dry-run"])
    _code, real = _drive(["restore", "run", record.session_id])

    assert _offered_digest(preview) != _offered_digest(real), (
        "the rehearsal flag did not move the digest, so a decision made about a "
        "preview is honoured against a restore that performs every step"
    )


def test_a_differently_cased_ancestor_still_puts_the_target_inside_the_library(
    installed, tmp_path
):
    """The ancestor WALK, measured where the candidate itself is not the root.

    Measured on the author's own table, row G6_ancestors_not_walked: asking
    ``samefile`` of the candidate alone killed nothing, because every case folded
    drive above named the root itself, where one question is enough. A directory
    three levels inside a library whose ROOT was typed in another case is the
    shape that needs the walk, and it is the one a person produces by pasting a
    path from somewhere that shouted it.
    """
    acknowledge(installed)
    root = Path(installed.library.root)
    (root / "beneath").mkdir()
    inside = root.parent / root.name.upper() / "beneath"
    assert not inside.is_relative_to(root), (
        "the two spellings share a prefix here, so the string test alone answers "
        "this and the walk is not what is being measured"
    )

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(inside)])

    if _case_folds(tmp_path):
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "restore-target-is-live-root"
        assert envelope["cause"]["detail"]["check"] == "containment"
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings as two directories, so "
            f"{inside} is not inside the library"
        )


def test_a_database_that_is_not_on_disk_yet_is_still_the_live_database(
    installed, tmp_path
):
    """The half of the destination check that ``samefile`` alone cannot make.

    Measured on the author's own table, row
    G14_the_destination_check_is_equality_only: dropping the name and parent
    half killed nothing, because every drive of it had the live database sitting
    on disk, where one stat answers the question. A database the configuration
    names and the disk does not hold is not an exotic state, it is the state a
    person is restoring FROM: the file is gone, which is why they are here. With
    the file absent there is nothing to stat, so a case folded spelling of its
    own directory passes the first half and lands ``master.db`` exactly where the
    live one belongs.
    """
    acknowledge(installed)
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    outside = replace(
        installed,
        library=replace(
            installed.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-18",
        ),
    )
    config.save(outside)
    config.reset_cache()
    assert not (home / "master.db").exists(), (
        "the database is on disk here, so the first half of the check answers "
        "this and the half under measurement is not reached"
    )
    shouted = home.with_name(home.name.upper())

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])

    if _case_folds(tmp_path):
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "restore-target-is-live-root"
        assert envelope["cause"]["detail"]["check"] == "destination"
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings as two directories, so the "
            f"database would land in {shouted} and not where the live one belongs"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Snapshot provenance, at the verb. What is approved is what arrives.
# ═══════════════════════════════════════════════════════════════════════════

LATER = "2026-08-22T235959Z"


def _shown(refused: dict) -> dict:
    """The off-machine half as the refusal put it in front of the person."""
    assert refused["cause"]["reason"] == "decision-required", refused
    return refused["cause"]["detail"]["shown"]["off_machine"]


def _copied_from(log: Path) -> list[str]:
    """The source argument of every copy the fake program was asked to make."""
    lines = log.read_text().splitlines() if log.exists() else []
    return [line.split()[1] for line in lines if line.startswith("copy ")]


def test_a_backup_landing_between_the_two_acts_moves_the_digest(installed, monkeypatch):
    """The ledger's measurement, driven: offer and answer, then a second snapshot.

    The word for "whichever is newest" was what entered the digest, so the
    resumed drive kept its digest and pulled the snapshot that had appeared
    since. Now the answer is refused as stale and nothing is copied, and the
    offer that replaces it names the snapshot a person would really get.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    _code, refused = _drive(["restore", "run", "--from-backup"])
    item = _shown(refused)
    assert item["snapshot"] == STAMP
    _answer(refused["run_id"], "restore")

    _remote_holds((STAMP, LATER), cfg_value=installed)
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code != int(ExitCode.OK)
    assert _copied_from(log) == [], (
        f"a decision made about {STAMP} was honoured and pulled {_copied_from(log)}"
    )


def test_what_is_offered_is_what_is_pulled(installed, monkeypatch):
    """The newest stamp is resolved once, shown, approved, and then used."""
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch, snapshots=(STAMP, LATER))

    _code, refused = _drive(["restore", "run", "--from-backup"])
    item = _shown(refused)
    assert item["snapshot"] == LATER
    assert item["snapshot_named"] is False
    assert item["recorded_volume"] == preflight.normalize_identity(installed.library.volume_id)
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])

    assert code == int(ExitCode.OK), envelope
    copied = _copied_from(log)
    assert copied and all(f"/{LATER}/db/" in source for source in copied), copied


def test_the_ledgers_traversal_value_is_refused_at_the_verb(installed, monkeypatch):
    """Through the dispatcher, with the value the finding was measured with.

    Before the gate is asked, so a person is never invited to approve it, and
    with nothing but the refusal in the program's own log: the value never
    reached an argument list.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    code, envelope = _drive(
        [
            "restore", "run", "--from-backup",
            "--snapshot", "../another-library-snapshots/2020-01-01T000000Z",
        ]
    )

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == str(backup.Refusal.SNAPSHOT_NAME_INVALID)
    assert envelope["cause"]["remediation"]["steps"], envelope["cause"]
    assert not log.exists() or log.read_text() == ""


def test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes(
    installed, monkeypatch
):
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch, marker="0000-AAAA")

    code, envelope = _drive(["restore", "run", "--from-backup", "--snapshot", STAMP])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == str(backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH)
    message = envelope["cause"]["message"]
    assert "0000-aaaa" in message
    assert preflight.normalize_identity(installed.library.volume_id) in message
    assert _copied_from(log) == []


def test_the_replaced_drive_flag_reaches_the_engine_and_the_digest(installed, monkeypatch):
    """``--snapshot-volume``, driven end to end, and held to what it names.

    In the digest because it is most of what is being approved when a snapshot
    is not plainly this library's own: an answer given to a restore of this
    library's snapshot must not be honoured against one that names another.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch, marker="0000-AAAA")
    named = ["restore", "run", "--from-backup", "--snapshot", STAMP]

    _code, refused = _drive([*named, "--snapshot-volume", "0000-aaaa"])
    item = _shown(refused)
    assert item["expected_volume"] == "0000-aaaa"
    assert item["recorded_volume"] == "0000-aaaa"
    _answer(refused["run_id"], "restore")

    # The same answer, against the invocation without the flag: refused, and
    # refused as a mismatch before the recorded decision is even consulted.
    code, envelope = _drive(["--run", refused["run_id"], *named])
    assert envelope["cause"]["reason"] == str(backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH)
    assert _copied_from(log) == []

    code, envelope = _drive(
        ["--run", refused["run_id"], *named, "--snapshot-volume", "0000-aaaa"]
    )
    assert code == int(ExitCode.OK), envelope
    assert _copied_from(log), "the flag was accepted and nothing was pulled"

    _remote_holds((STAMP,), marker="9999-BBBB")
    code, envelope = _drive([*named, "--snapshot-volume", "0000-aaaa"])
    assert envelope["cause"]["reason"] == str(backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH)


def test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled(
    installed, monkeypatch
):
    """Every snapshot that exists on the day this lands is unmarked.

    The refusal has to work with no new backup, because a person whose drive
    just died cannot take one, so it names the stamp and naming it is enough.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch, marker=None)

    code, envelope = _drive(["restore", "run", "--from-backup"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == str(backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED)
    assert STAMP in envelope["cause"]["message"]

    named = ["restore", "run", "--from-backup", "--snapshot", STAMP]
    _code, refused = _drive(named)
    item = _shown(refused)
    assert item["snapshot_named"] is True
    assert item["recorded_volume"] is None
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(["--run", refused["run_id"], *named])
    assert code == int(ExitCode.OK), envelope
    assert _copied_from(log)


def test_a_restore_that_pulls_nothing_off_the_machine_still_asks_the_remote_nothing(
    installed, monkeypatch
):
    """The early listing is paid only by the half that needs it.

    The reason the stamp was left out of the digest in the first place was that
    resolving it reaches the network before the gate. That is now true of
    ``--from-backup`` and must stay false of everything else.
    """
    record, _captured = completed_session(installed)
    log = _fake_rclone(installed, monkeypatch)

    _drive(["restore", "run", record.session_id])

    assert not log.exists() or log.read_text() == ""


def test_the_digest_moves_when_the_expected_volume_is_stated(installed, monkeypatch):
    """The flag is part of what is approved, measured where it changes nothing else.

    Stating this library's own identity resolves exactly as saying nothing does,
    so the two offers differ in the flag and in no other field, and an answer
    given to one must still not be honoured against the other.
    """
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)

    _code, plain = _drive(["restore", "run", "--from-backup"])
    _code, stated = _drive(
        ["restore", "run", "--from-backup", "--snapshot-volume", installed.library.volume_id]
    )

    assert _shown(plain)["recorded_volume"] == _shown(stated)["recorded_volume"]
    assert _offered_digest(plain) != _offered_digest(stated)


@pytest.mark.parametrize(
    "flags",
    [
        ["--snapshot-volume", "0000-aaaa"],
        ["--snapshot", STAMP],
        ["--include-mirror"],
        ["--snapshot", STAMP, "--include-mirror"],
    ],
)
def test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for(installed, flags):
    """They were dropped in silence, ahead of a rollback nobody meant.

    A person typing the expected volume believes they authorised a replaced
    drive's snapshot, and with the pull flag forgotten the verb went on to offer
    a capture rollback of the live library without a word about the flag.
    """
    record, _captured = completed_session(installed)

    code, envelope = _drive(["restore", "run", record.session_id, *flags])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "restore-flag-needs-pull"
    assert envelope["cause"]["detail"]["flags"] == [f for f in flags if f.startswith("--")]
    assert envelope["cause"]["remediation"]["steps"]


def test_the_report_names_the_snapshot_that_arrived(installed, monkeypatch):
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch, snapshots=(STAMP, LATER))

    _code, refused = _drive(["restore", "run", "--from-backup"])
    _answer(refused["run_id"], "restore")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])

    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert totals["snapshot"] == LATER
    assert totals["recorded_volume"] == preflight.normalize_identity(
        installed.library.volume_id
    )


def test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled(
    installed, monkeypatch
):
    """The window INSIDE the second act, which the digest cannot see.

    The answer is checked against an offer built from one listing, and the
    engine plans a moment later. Were it handed the flag rather than the stamp
    that was offered, it would resolve the newest snapshot again, after the
    approval, and pull whatever had landed in between. The fake remote changes
    its answer after the first listing of the second act to stand in for that.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)
    home = Path(config.installation_state_dir())

    _code, refused = _drive(["restore", "run", "--from-backup"])
    _answer(refused["run_id"], "restore")
    (home / f"{REMOTE_SNAPSHOTS}.next").write_text(f"{STAMP}/\n{LATER}/\n")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])

    assert code == int(ExitCode.OK), envelope
    assert not (home / f"{REMOTE_SNAPSHOTS}.next").exists(), "the remote never moved"
    copied = _copied_from(log)
    assert copied and all(f"/{STAMP}/db/" in source for source in copied), copied


# ═══════════════════════════════════════════════════════════════════════════
# restore bare-metal: the library volume is gone
# ═══════════════════════════════════════════════════════════════════════════

#: A file the mirror carries, relative to the volume it was taken from.
MIRRORED = "Music/a-track.flac"


class _Remote:
    """A runner that answers the listings and PERFORMS a copy as a file write.

    The shell stand-in above transfers nothing, which is enough to read what
    rclone was asked and not enough to say where bytes landed. This one writes a
    file at every destination it is handed, so "only under the target" is
    measured on the disk rather than read off an argument list. ``failing``
    names the labels that exit non-zero, and a failing transfer writes nothing.
    """

    def __init__(
        self,
        cfg_value,
        *,
        failing=(),
        mirrored=(MIRRORED,),
        holds=("master.db", "master.db-wal"),
    ):
        self.cfg = cfg_value
        self.failing = frozenset(failing)
        self.mirrored = tuple(mirrored)
        self.holds = tuple(holds)
        self.calls: list[backup.Command] = []

    def __call__(self, command: backup.Command) -> backup.CommandResult:
        self.calls.append(command)
        if command.label == backup.LIST_SNAPSHOTS:
            return backup.CommandResult(0, f"{STAMP}/\n")
        if command.label == backup.LIST_SNAPSHOT_IDENTITY:
            return backup.CommandResult(
                0, f"{backup.identity_marker(self.cfg.library.volume_id)}\n"
            )
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(0, "".join(f"{name}\n" for name in self.holds))
        if command.label == backup.LIST_SHARE:
            # A MIRRORED SHARE IS ALWAYS HELD, so an outside layout plans the
            # share's transfer and a test that sees none is seeing a decision.
            return backup.CommandResult(0, "PIONEER/\n")
        if command.label in self.failing:
            return backup.CommandResult(3)
        if "--dry-run" in command.argv:
            return backup.CommandResult(0)
        source, destination = command.argv[2], Path(command.argv[3])
        if command.label == backup.RESTORE_MIRROR:
            for relative in self.mirrored:
                landed = destination / relative
                landed.parent.mkdir(parents=True, exist_ok=True)
                landed.write_bytes(b"mirrored")
        else:
            destination.mkdir(parents=True, exist_ok=True)
            (destination / source.rsplit("/", 1)[-1]).write_bytes(b"from the snapshot")
        return backup.CommandResult(0)

    @property
    def transfers(self) -> list[backup.Command]:
        moving = (backup.RESTORE_MIRROR, backup.RESTORE_DATABASE, backup.RESTORE_SHARE)
        return [c for c in self.calls if c.label in moving]


def _everything_on_disk(*roots: Path) -> dict[str, bytes | None]:
    """Every path under the roots with its bytes, directories as ``None``."""
    seen: dict[str, bytes | None] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            seen[str(path)] = path.read_bytes() if path.is_file() else None
    return seen


def _gone(cfg_value, **overrides) -> dict:
    """The engine suite's dead volume, plus a person at a terminal."""
    seams = restore_suite._volume_is_gone(cfg_value)
    seams["terminal"] = lambda: True
    seams["process_lister"] = lambda: ()
    seams.update(overrides)
    return seams


def _replacement(tmp_path) -> Path:
    target = tmp_path / "replacement"
    target.mkdir()
    return target


def test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target(cfg, tmp_path):
    target = _replacement(tmp_path)
    seams = _gone(cfg)
    remote = _Remote(cfg)
    state = Path(config.installation_state_dir())
    before = _everything_on_disk(tmp_path, state)

    report = restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=remote, **seams
    )

    assert (target / MIRRORED).read_bytes() == b"mirrored"
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"
    assert (target / "db" / "master.db-wal").exists()
    assert report.target == target
    assert report.database_target == target / "db" / "master.db"
    assert report.mirror == (backup.RESTORE_MIRROR,)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert report.snapshot == STAMP
    assert [c.label for c in remote.transfers][0] == backup.RESTORE_MIRROR

    after = _everything_on_disk(tmp_path, state)
    outside = {
        path
        for path in after.keys() - before.keys()
        if not Path(path).is_relative_to(target)
    }
    assert outside == {str(restore.recovery_lock_path())}, outside
    assert {p: b for p, b in after.items() if p in before} == before
    assert not Path(cfg.library.root).exists(), "the lost library's path was recreated"


def test_every_transfer_is_pointed_under_the_target_and_nowhere_else(cfg, tmp_path):
    target = _replacement(tmp_path)
    remote = _Remote(cfg)

    restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=remote, **_gone(cfg)
    )

    destinations = [Path(c.argv[3]) for c in remote.transfers]
    assert len(destinations) == 3
    assert all(d == target or d.is_relative_to(target) for d in destinations), destinations


def _mounted(cfg_value, tmp_path):
    """A library that is present and is the recorded volume, and NOTHING ELSE WRONG.

    The mount probe answers yes on purpose. The replacement directory sits beside
    the configured root, which is the second shape the stub check refuses, and
    that refusal's sentence contains the word "unmounted". Without the probe, a
    test asserting on "mounted" is held up by the stub check alone, and the
    identity gate, the one that keeps the two restores apart, can be deleted
    with the suite green. Measured: that is what the mutation table's row found.
    """
    return _replacement(tmp_path), {
        **gate_seams(cfg_value),
        "terminal": lambda: True,
        "mount_probe": lambda _path: True,
    }


def _a_stub(cfg_value, tmp_path):
    seams = _gone(cfg_value, mount_probe=lambda _path: False)
    stub = Path(cfg_value.library.root)
    stub.mkdir()
    return stub, seams


def _no_terminal(cfg_value, tmp_path):
    return _replacement(tmp_path), _gone(cfg_value, terminal=lambda: False)


REFUSED_BEFORE_THE_LOCK = {
    "the library is still mounted": (_mounted, True, "nothing to recover from bare metal"),
    "the target is the stub on the internal disk": (_a_stub, True, "internal disk"),
    "nobody is at a terminal": (_no_terminal, True, "no controlling terminal"),
    "the replacement was not accepted": (
        lambda c, t: (_replacement(t), _gone(c)),
        False,
        "explicit decision",
    ),
}


@pytest.mark.parametrize("case", sorted(REFUSED_BEFORE_THE_LOCK))
def test_a_refusal_before_the_lock_leaves_the_disk_untouched(cfg, tmp_path, case):
    arrange, accepted, said = REFUSED_BEFORE_THE_LOCK[case]
    target, seams = arrange(cfg, tmp_path)
    seams.setdefault("process_lister", lambda: ())
    remote = _Remote(cfg)
    state = Path(config.installation_state_dir())
    before = _everything_on_disk(tmp_path, state)

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=accepted, runner=remote, **seams
        )

    assert excinfo.value.cause.reason == "recovery-target-refused"
    assert said in excinfo.value.cause.message
    assert remote.calls == [], "the remote was asked something by a refused recovery"
    assert _everything_on_disk(tmp_path, state) == before
    assert not restore.recovery_lock_path().exists()


def test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it(
    cfg, tmp_path
):
    """The verb never passes ``replacing_existing``, and has no flag that could."""
    target = _replacement(tmp_path)
    (target / "deep" / "er").mkdir(parents=True)
    (target / "deep" / "er" / "master.db").write_bytes(b"somebody's library")
    remote = _Remote(cfg)

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, runner=remote, **_gone(cfg)
        )

    assert excinfo.value.cause.reason == "recovery-target-refused"
    assert "already holds master.db" in excinfo.value.cause.message
    assert remote.calls == []
    assert (target / "deep" / "er" / "master.db").read_bytes() == b"somebody's library"
    # A usage error prints no envelope, so the parser is asked rather than driven.
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(
            ["restore", "bare-metal", "--target", str(target), "--replace-existing"]
        )


def test_both_halves_run_inside_one_holding_of_the_recovery_lock(cfg, tmp_path):
    """Asked from a REAL second interpreter, while each transfer is in flight."""
    target = _replacement(tmp_path)
    seams = _gone(cfg)
    observed: list[int] = []

    class _Watching(_Remote):
        def __call__(self, command):
            if command.label in (backup.RESTORE_MIRROR, backup.RESTORE_DATABASE):
                observed.append(_lock_taken_in_another_process(restore.recovery_lock_path()))
            return super().__call__(command)

    restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=_Watching(cfg), **seams
    )

    assert observed == [3, 3, 3], observed
    assert _lock_taken_in_another_process(restore.recovery_lock_path()) == 0


def test_a_recovery_already_running_here_refuses_the_second_one(cfg, tmp_path):
    """The engine's busy path, which this verb is the first caller to own."""
    import fcntl  # noqa: PLC0415

    target = _replacement(tmp_path)
    seams = _gone(cfg)
    remote = _Remote(cfg)
    lock = restore.recovery_lock_path()
    lock.parent.mkdir(parents=True, exist_ok=True)
    with open(lock, "a+") as other:
        fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(CratekitError) as excinfo:
            restore_cli.recover_under_bare_metal_session(
                cfg, target=target, accepted=True, runner=remote, **seams
            )

    assert excinfo.value.cause.reason == "session-lock-held", excinfo.value.cause
    assert str(lock) in excinfo.value.cause.message
    assert remote.calls == []
    assert list(target.iterdir()) == []


def test_the_verb_cannot_be_typed_without_naming_a_target():
    """No default, because the only default there could be is the lost volume."""
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["restore", "bare-metal", "--accept-replacement"])


def test_a_recovery_is_refused_underneath_a_running_rekordbox(cfg, tmp_path):
    target = _replacement(tmp_path)
    remote = _Remote(cfg)

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg,
            target=target,
            accepted=True,
            runner=remote,
            **_gone(cfg, process_lister=lambda: ("rekordbox",)),
        )

    assert excinfo.value.cause.reason == "rekordbox-running"
    assert remote.transfers == []
    assert list(target.iterdir()) == []


def test_a_failed_mirror_stops_the_recovery_before_the_database(cfg, tmp_path):
    """The engine runs every command before reading one; the verb runs a half."""
    target = _replacement(tmp_path)
    seams = _gone(cfg)
    remote = _Remote(cfg, failing={backup.RESTORE_MIRROR})

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, runner=remote, **seams
        )

    cause = excinfo.value.cause
    assert cause.reason == "restore-transfer-failed"
    assert cause.detail["half"] == restore_cli.MIRROR_HALF
    assert cause.detail["completed_halves"] == []
    assert "exited 3" in cause.detail["engine"]
    assert "database half was not attempted" in cause.message
    assert "cleared" not in cause.message
    assert cause.remediation.steps[-1] == restore_cli.RERUN_STEP
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not list(target.rglob("*.db"))

    again = restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=_Remote(cfg), **seams
    )
    assert again.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)


def test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove(cfg, tmp_path):
    target = _replacement(tmp_path)
    remote = _Remote(cfg, failing={backup.RESTORE_DATABASE})

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, runner=remote, **_gone(cfg)
        )

    cause = excinfo.value.cause
    assert cause.reason == "restore-transfer-failed"
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert cause.detail["completed_halves"] == [restore_cli.MIRROR_HALF]
    assert "mirror half completed" in cause.message
    assert "master.db" in cause.message
    assert cause.remediation.steps[0] == "do not open the library"
    assert cause.remediation.steps[-1] == restore_cli.RERUN_STEP
    assert (target / MIRRORED).exists()


def test_a_rehearsal_passes_the_same_gates_and_writes_nothing(cfg, tmp_path):
    target = _replacement(tmp_path)
    remote = _Remote(cfg)

    report = restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, dry_run=True, runner=remote, **_gone(cfg)
    )

    assert report.dry_run is True
    assert report.mirror == (backup.RESTORE_MIRROR,)
    assert len(report.database) == 2
    assert all("--dry-run" in c.argv for c in remote.transfers)
    assert list(target.iterdir()) == []

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=False, dry_run=True, runner=remote, **_gone(cfg)
        )
    assert "explicit decision" in excinfo.value.cause.message


def test_a_failed_rehearsal_says_nothing_was_written(cfg, tmp_path):
    target = _replacement(tmp_path)
    remote = _Remote(cfg, failing={backup.RESTORE_MIRROR})

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, dry_run=True, runner=remote, **_gone(cfg)
        )

    assert "nothing was written" in excinfo.value.cause.message
    assert excinfo.value.cause.detail["dry_run"] is True
    assert restore_cli.RERUN_STEP not in excinfo.value.cause.remediation.steps


def test_a_rerun_is_refused_until_the_step_the_refusal_gave_is_followed(cfg, tmp_path):
    """DRIVEN, AND A KNOWN LIMIT RATHER THAN A PROPERTY ANYBODY WANTS.

    The mirror excludes this library's own database and nothing else with that
    suffix, and it carries the state directory beside the library, which holds
    the review queue and every capture. So any run cut off after the mirror has
    started leaves an occupied target, the engine refuses an occupied target,
    and the verb has no flag that names one for replacement. What this holds is
    that the step the failure gives is TRUE: followed exactly, the rerun
    completes, and what was removed comes back. The ledger entry titled "An
    interrupted bare metal recovery is refused on rerun until every database
    file it landed is removed" records the limit. When that closes, the first
    half of this test is what changes.
    """
    target = _replacement(tmp_path)
    seams = _gone(cfg)
    carried = (MIRRORED, ".cratekit/queue.db", ".cratekit/snapshots/one/master.db")
    first = _Remote(cfg, failing={backup.RESTORE_DATABASE}, mirrored=carried)
    with pytest.raises(CratekitError) as failed:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, runner=first, **seams
        )
    assert failed.value.cause.remediation.steps[-1] == restore_cli.RERUN_STEP

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, runner=_Remote(cfg, mirrored=carried), **seams
        )
    assert "already holds" in excinfo.value.cause.message

    for landed in list(target.rglob("*.db")):
        landed.unlink()
    report = restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=_Remote(cfg, mirrored=carried), **seams
    )

    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert (target / ".cratekit" / "queue.db").exists()
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"


def test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half(cfg, tmp_path):
    """Asked twice, because the first answer is hours old by the second half."""
    target = _replacement(tmp_path)
    remote = _Remote(cfg)
    answers = iter([(), ("rekordbox",)])

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg,
            target=target,
            accepted=True,
            runner=remote,
            **_gone(cfg, process_lister=lambda: next(answers)),
        )

    cause = excinfo.value.cause
    assert cause.reason == "rekordbox-running"
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert cause.detail["completed_halves"] == [restore_cli.MIRROR_HALF]
    assert "mirror half completed" in cause.message
    assert cause.remediation.steps[-1] == restore_cli.RERUN_STEP
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not list(target.rglob("master.db*"))


def test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one(
    cfg, tmp_path
):
    """rekordbox's own default layout: the database is on the internal disk."""
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    (home / "master.db").write_bytes(b"alive, and never on the lost volume")
    outside = replace(
        cfg,
        library=replace(
            cfg.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-18",
        ),
    )
    assert backup.database_target_for(outside, tmp_path) == tmp_path / "master.db", (
        "the fixture does not reproduce the layout, so this pins nothing"
    )
    target = _replacement(tmp_path)
    # A snapshot with no write ahead log, so the plan DOES name an absent
    # companion and the report's silence about it is a decision under test.
    remote = _Remote(outside, holds=("master.db",))

    report = restore_cli.recover_under_bare_metal_session(
        outside, target=target, accepted=True, runner=remote, **_gone(outside)
    )

    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not (target / "master.db").exists()
    # THE SHARE RIDES THE DATABASE HALF (R-338). It was beside the database, so
    # it was never on the lost volume either, and the remote holding a mirror of
    # it is not a reason to pour gigabytes of it onto the replacement.
    # Withheld before the remote is asked, so a listing that fails cannot
    # refuse a recovery of the music over a share it was never going to pull.
    assert [c.label for c in remote.calls if c.label == backup.LIST_SHARE] == []
    assert not (target / "share").exists()
    assert (home / "master.db").read_bytes() == b"alive, and never on the lost volume"
    assert report.database == ()
    assert report.absent == ()
    assert report.database_elsewhere == home / "master.db"
    totals = restore_cli._recovered(report)["totals"]
    assert totals["database_was_on_the_lost_volume"] is False
    assert totals["database_target"] == str(home / "master.db")


@pytest.fixture
def lost(cfg, monkeypatch):
    """A machine whose library volume is gone, with the PLATFORM seams answered.

    The dispatcher takes its arguments from a command line, so there is nowhere
    to hand a probe in. What is replaced is what ``installed`` replaces and for
    its reason, plus the two answers a temporary directory cannot give: that a
    person is at a terminal, and that the target is a mount point.
    """
    shutil.rmtree(cfg.library.root)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: "0000-not-this-disk")
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    monkeypatch.setattr(restore, "_is_mount_point", lambda _path: True)
    return cfg


def test_the_verb_recovers_both_halves_and_reports_them_apart(lost, monkeypatch, tmp_path):
    target = _replacement(tmp_path)
    log = _fake_rclone(lost, monkeypatch)

    code, envelope = _drive(
        ["restore", "bare-metal", "--target", str(target), "--accept-replacement"]
    )

    assert code == int(ExitCode.OK), envelope
    assert envelope["verb"] == "restore.bare-metal"
    totals = envelope["data"]["totals"]
    assert totals["mirror_transfers"] == 1
    assert totals["database_transfers"] == 1
    assert totals["absent_sidecars"] == ["-wal"]
    assert totals["target"] == str(target)
    assert totals["database_was_on_the_lost_volume"] is True
    assert totals["database_target"] == str(target / "db" / "master.db")
    assert totals["snapshot"] == STAMP
    assert [item["half"] for item in envelope["data"]["items"]] == [
        restore_cli.MIRROR_HALF,
        restore_cli.DATABASE_HALF,
    ]
    # THE THIRD WORD, not the last: the mirror transfer ends in its tuning flags.
    destinations = [
        Path(line.split()[2]) for line in log.read_text().splitlines() if line.startswith("copy ")
    ]
    assert len(destinations) == 2
    assert all(d == target or d.is_relative_to(target) for d in destinations), destinations


def test_the_verb_refuses_without_the_acceptance_flag(lost, monkeypatch, tmp_path):
    target = _replacement(tmp_path)
    log = _fake_rclone(lost, monkeypatch)

    code, envelope = _drive(["restore", "bare-metal", "--target", str(target)])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "recovery-target-refused"
    assert "explicit decision" in envelope["cause"]["message"]
    assert not log.exists() or "copy" not in log.read_text()


def test_the_verb_refuses_while_the_library_is_mounted(installed, monkeypatch, tmp_path):
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    # So the stub check cannot be what refuses. See ``_mounted``.
    monkeypatch.setattr(restore, "_is_mount_point", lambda _path: True)
    target = _replacement(tmp_path)
    log = _fake_rclone(installed, monkeypatch)

    code, envelope = _drive(
        ["restore", "bare-metal", "--target", str(target), "--accept-replacement"]
    )

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "recovery-target-refused"
    assert "nothing to recover from bare metal" in envelope["cause"]["message"]
    assert not log.exists() or log.read_text() == ""
    assert list(target.iterdir()) == []


def test_the_recovery_verb_declares_no_gate_and_no_check_it_needs_to_fail():
    entry = registry.entry("restore.bare-metal")
    assert entry.gates == ()
    assert entry.destructive is True
    assert not {"library.mounted", "library.identity"} & set(entry.doctor_checks)


def test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing(
    cfg, tmp_path, monkeypatch
):
    """The registry entry declares no check for the program, so the verb says it."""
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(tmp_path / "no-such-program"))
    monkeypatch.setenv("PATH", str(tmp_path))
    target = _replacement(tmp_path)

    with pytest.raises(CratekitError) as excinfo:
        restore_cli.recover_under_bare_metal_session(
            cfg, target=target, accepted=True, **_gone(cfg)
        )

    assert excinfo.value.cause.reason == "rclone-missing"
    assert list(target.iterdir()) == []
