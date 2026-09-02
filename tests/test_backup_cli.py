"""U45: ``crate backup run``, the shell over the backup engine (row 31).

WHAT THIS FILE IS FOR, since ``tests/modules/test_tools.py`` already drives the
engine. Two different claims. That file proves the ENGINE publishes a backup age
per portion and only on success when it is called directly. This one proves the
SHELL reaches that engine in a way that keeps the promise, and that the fact
lands where the thing that consumes it will look.

WHY THE CONSUMER IS DRIVEN RATHER THAN THE FILE ASSERTED. The unit's whole
purpose is that a destructive write session can see the backup a person just
took. Asserting the fact file's bytes would prove this file agrees with itself.
So every claim about publishing below is taken through
:func:`cratekit.core.backup_facts.ages`, which is the function
``core.session._shown_ages`` calls, and the acknowledgment a destructive session
records is minted at the end of the two that matter most so the age is read back
through the code that actually reads it.

ONE THING THIS FILE DOES NOT CLAIM. A failed backup does not make a destructive
session refuse; that gate is the ACKNOWLEDGMENT, which is a separate act by a
person and is absent or present regardless of any backup. What a failed backup
does is leave the age at ``never-recorded``, so the record of what the person was
shown says so, which is what R15's warning exists to put in front of them. The
tests below assert the state that is true rather than the refusal that is not.

THE STAND-IN RCLONE DISPATCHES ON ITS ARGV where a drive needs a plan built and a
transfer answered, following ``_fake_rclone`` in ``tests/test_restore_cli.py``:
``CRATEKIT_BIN_RCLONE`` is ``core.binaries``'s per-binary override, read before
PATH, so what is replaced is the external PROGRAM and nothing else. Where a test
is about the SHELL's reading of a result rather than about argument construction,
the injected ``runner`` seam is used instead and that is said in the test.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real remote account.
"""

from __future__ import annotations

import ast
import io
import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.backup import cli as backup_cli
from cratekit.cli import registry
from cratekit.core import backup_facts, binaries, config, jobs, profiles, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.tools import backup

#: A fixed instant, so an age is a computation rather than a race. Far enough
#: from any real clock that a test reading a real one would fail loudly.
MOMENT = datetime(2026, 8, 29, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library with the four backup destinations, SAVED.

    Saved and not merely built, because the work body loads the configuration
    from disk the way the dispatcher does. The environment variable is set as
    well as the file for the reason ``tests/test_restore.py`` gives for the same
    fixture: ``from_dict`` relocates a configured root onto whatever the
    environment says, so writing only the file leaves the value under test and
    the value in force as two different directories.
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
            "backup": {
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        }
    )
    config.save(built)
    config.reset_cache()
    config.state_path("rekordbox_db", built).write_bytes(b"database, generation one")
    return built


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    """No rekordbox process, injected, so no test depends on this machine.

    Injected rather than probed for the reason ``plan_backup`` takes the lister
    as a seam at all: the process probe is the one guard between a live database
    and a torn copy, and a suite that read this laptop's process table would pass
    or fail on whether somebody happened to have rekordbox open.
    """
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def rclone(monkeypatch, tmp_path) -> Path:
    """A stand-in for rclone on the ONE seam the product ships for it.

    It answers ``lsf`` with two dated archive folder names so the prune has
    something to work from, exits 0 on everything else, and logs every
    invocation. The log is what argv assertions are taken over, so what is
    measured is the program's own view of what it was asked to do.
    """
    log = tmp_path / "rclone-invocations.log"
    program = tmp_path / "fake-rclone"
    program.write_text(
        "#!/bin/sh\n"
        f'printf "%s\\n" "$*" >> "{log}"\n'
        'case " $* " in *" lsf "*) echo "2026-08-01T000000Z/"; echo "2026-08-02T000000Z/" ;; esac\n'
        "exit 0\n"
    )
    program.chmod(0o755)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(program))
    return log


@pytest.fixture
def rclone_that_cannot_list(monkeypatch, tmp_path) -> Path:
    """The same stand-in, except that ``lsf`` fails and everything else does not.

    THE ONE CONDITION THE ARCHIVE ROTATION CANNOT SURVIVE AND THE BACKUP CAN. A
    remote that answers a sync and refuses a listing gives a real backup and no
    rotation, which is the state the finding behind this unit says was reported
    to nobody. Built as a PROGRAM rather than as an injected runner because the
    claim is about what the shell reports over a real plan, and because failing
    by label through the runner seam would prove the seam rather than the
    condition.
    """
    log = tmp_path / "rclone-nolist-invocations.log"
    program = tmp_path / "fake-rclone-nolist"
    program.write_text(
        "#!/bin/sh\n"
        f'printf "%s\\n" "$*" >> "{log}"\n'
        'case " $* " in *" lsf "*) echo "the remote refused the listing" >&2; exit 3 ;; esac\n'
        "exit 0\n"
    )
    program.chmod(0o755)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(program))
    return log


@pytest.fixture
def no_rclone(monkeypatch, tmp_path):
    """A machine with no rclone at all, built rather than hoped for, and ASSERTED.

    THE MECHANISM IS THE PER-BINARY OVERRIDE AND NOT PATH, which is worth saying
    because the first draft of this fixture emptied PATH as well and read as
    though the two worked together. ``core.binaries.find`` reads the override
    first and returns None for a set-but-broken one "rather than falling through
    to PATH", so the override alone decides it. Emptying PATH would not have been
    enough on its own either: ``find`` consults the fallback directories after
    PATH, and a developer machine with rclone in one of them would have handed
    the plan a real program while this fixture claimed there was none.

    THE PRECONDITION IS ASSERTED RATHER THAN ASSUMED. That is the same discipline
    ``tests/test_pending_units.py`` enforces by forbidding a constructed skip:
    when a test needs a state the environment may not provide, assert it, so an
    environment that cannot produce it reports rather than passes quietly. Here
    the failure mode is specific and it is silent, since a run that found a real
    rclone would build a real plan and the refusal under test would simply not
    occur.
    """
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(tmp_path / "absent" / "rclone"))
    assert binaries.find("rclone") is None, (
        "rclone is still resolvable, so the refusal these tests drive would "
        "never be reached and they would pass over a plan that was really built"
    )


def _entry() -> registry.Entry:
    return registry.entry("backup.run")


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Run the REAL dispatcher and return the status with the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _answering(returncode: int, *, stdout: str = "", stderr: str = ""):
    """A runner that gives every command one answer, and records what it was asked.

    The injected seam rather than the stand-in program, because these drives are
    about what the SHELL does with a result and not about how the argv was built.
    """
    seen: list[backup.Command] = []

    def runner(command: backup.Command) -> backup.CommandResult:
        seen.append(command)
        return backup.CommandResult(returncode=returncode, stdout=stdout, stderr=stderr)

    runner.seen = seen  # type: ignore[attr-defined]
    return runner


def _failing_on(label: str):
    """A runner that fails only the commands carrying one label.

    Selective rather than uniform, because a runner that fails everything cannot
    produce the outcome that matters most here: one portion completing while the
    other does not. The label is matched WHOLE against ``Command.label`` rather
    than by substring, for the reason the engine gives for naming its labels as
    constants at all, that two spellings of one label make the preview and the run
    disagree about which command they are looking at.
    """

    def runner(command: backup.Command) -> backup.CommandResult:
        if command.label == label:
            return backup.CommandResult(returncode=1, stderr="connection refused")
        return backup.CommandResult(returncode=0)

    return runner


def _without_destinations(cfg_value):
    """The same configuration with the off-machine destinations removed.

    Built by REPLACING the field rather than by writing a second configuration
    dictionary, the way ``tests/test_restore_cli.py`` builds the same variant, so
    the library half stays byte for byte the one every other test here uses and
    the only difference is the one under test.
    """
    return replace(
        cfg_value,
        backup=replace(
            cfg_value.backup, remote="", dest="", archive_root="", db_dest_root=""
        ),
    )


def _ages(cfg) -> dict[str, backup_facts.PortionAge]:
    """Every portion's age, keyed by name, READ from the fact file.

    Through ``backup_facts.ages`` because that is the function
    ``core.session._shown_ages`` calls. Reading the JSON here would measure this
    file's opinion of the format rather than what the consumer sees.
    """
    return {str(entry.portion): entry for entry in backup_facts.ages(cfg, now=MOMENT)}


# ---------------------------------------------------------------------------
# The surface, and the module toggle
# ---------------------------------------------------------------------------


def test_the_verb_is_declared_landed_and_names_this_module():
    """The registry entry drives the conformance suite only once planned_in is gone.

    Asserted here as well as implied there, because ``landed`` being false is
    exactly the state that made row 31 sit uncovered while the board showed
    nothing owed: every conformance property is parametrised over LANDED, so a
    marker left in place buys silence rather than a failure.
    """
    entry = _entry()
    assert entry.landed, "planned_in is still set, so no conformance property arms"
    assert entry.module == "cratekit.backup.cli"
    assert entry.argv_builder == "backup_argv" and entry.long_running
    assert entry.module_id == "backup"
    assert entry.gates == (), (
        "this verb declares no gate on purpose; adding one obliges backup_argv to "
        "carry --run with the frozen gate run, which nothing here does"
    )


def test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one():
    """Both directions, because either alone passes over a toggle that is ignored.

    The membership is asked of the registry entry rather than of a rendered help
    text, so what is measured is the decision the dispatcher makes rather than a
    string. The rendered surface is covered by the conformance suite, which walks
    every landed entry.
    """
    entry = _entry()
    assert entry.available_to(profiles.resolve("full")), (
        "the backup module is in the full profile and the verb is not offered"
    )
    assert not entry.available_to(profiles.resolve("slim")), (
        "a slim install has no backup module, so this verb must not be offered"
    )


def test_queueing_needs_no_rclone_no_remote_and_no_volume(cfg, no_rclone, monkeypatch):
    """The handler files a job and resolves nothing, which is the whole split.

    Driven with the remote UNCONFIGURED as well as rclone absent, because both
    are refusals the work body raises and neither may reach the queueing half. A
    handler that planned here would refuse to file work on a machine where the
    work would have run fine once claimed, which is the case a person hits when
    they queue a backup before mounting the volume.
    """
    config.save(_without_destinations(cfg))
    config.reset_cache()
    code, envelope = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["job_id"], envelope
    assert envelope["schema"] == "job_state/1", envelope


# ---------------------------------------------------------------------------
# The resume, which is the only other thing a queued verb owes
# ---------------------------------------------------------------------------


def test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run():
    """Both directions of the flag, and the absence of --run, in one place.

    THE FLAG IS THE ONE WAY THIS BUILDER COULD DO REAL HARM. A resume that lost
    ``--dry-run`` turns a rehearsal into a real transfer that publishes a backup
    age, inside a detached child whose only output is a log nobody is watching.
    Asserting only the rehearsal direction would pass over a builder that always
    emits the flag, which breaks the other half just as completely.
    """

    class _Job:
        job_id = "job-one"

        def __init__(self, payload):
            self.payload = payload

    assert backup_cli.backup_argv(_Job({backup_cli.DRY_RUN: True})) == [
        "backup",
        "run",
        "--dry-run",
        "--job",
        "job-one",
    ]
    assert backup_cli.backup_argv(_Job({backup_cli.DRY_RUN: False})) == [
        "backup",
        "run",
        "--job",
        "job-one",
    ]
    assert backup_cli.backup_argv(_Job(None)) == ["backup", "run", "--job", "job-one"], (
        "a payload written by a build that did not freeze this key must still "
        "produce a command line, because the caller is a detached child"
    )
    for payload in ({backup_cli.DRY_RUN: True}, {backup_cli.DRY_RUN: False}, None):
        assert "--run" not in backup_cli.backup_argv(_Job(payload)), (
            "this verb declares no gate, so a --run here would name a run nothing "
            "was recorded against"
        )


def test_the_frozen_payload_and_the_parser_agree_about_the_flag(cfg):
    """The key the handler freezes is the key the builder reads, driven end to end.

    Through the real parser rather than by calling ``frozen_payload`` with a
    boolean, because the defect this guards against is a ``dest`` that does not
    match: an argument declared ``--dry-run`` without ``dest`` lands on
    ``args.dry_run`` anyway, and one declared with the wrong ``dest`` silently
    freezes ``False`` for ever while the flag parses fine.
    """
    for argv, wanted in ((["backup", "run"], False), (["backup", "run", "--dry-run"], True)):
        code, envelope = _drive(argv)
        assert code == int(ExitCode.OK), envelope
        with jobs.open_store() as store:
            job = jobs.get(store, envelope["data"]["job_id"])
        assert job.payload == {backup_cli.DRY_RUN: wanted}, (
            f"{argv} froze {job.payload}, so the resume would do different work "
            f"from the run it continues"
        )


# ---------------------------------------------------------------------------
# The age, which is the half of this unit that is not a shell
# ---------------------------------------------------------------------------


def test_a_run_that_succeeded_publishes_an_age_the_session_reads_back(cfg, rclone):
    """The unit's reason for existing, driven through the consumer.

    Every assertion here is taken through ``backup_facts.ages`` and then through
    the acknowledgment a destructive session records, rather than off the report
    the verb produced. A report is the verb's claim about the world; the
    acknowledgment is the world the next destructive verb will read.
    """
    before = _ages(cfg)
    assert all(
        entry.state is backup_facts.AgeState.NEVER_RECORDED for entry in before.values()
    ), "the fixture already carries a backup age, so nothing below measures a change"

    report = backup_cli.perform_backup({}, now=MOMENT)

    after = _ages(cfg)
    assert {name: entry.state for name, entry in after.items()} == {
        "files": backup_facts.AgeState.KNOWN,
        "database": backup_facts.AgeState.KNOWN,
    }, after
    assert all(entry.age == timedelta(0) for entry in after.values()), after

    shown = session.record_acknowledgment(
        cfg, now=MOMENT, terminal=lambda: True
    ).shown
    assert {entry.portion: entry.state for entry in shown} == {
        "files": "known",
        "database": "known",
    }, (
        "the destructive session's own record does not show the backup that was "
        "just taken, which is the whole failure this unit exists to prevent"
    )
    assert all(entry.age_seconds == 0.0 for entry in shown), shown

    assert report["ok"] is True and report["dry_run"] is False, report
    assert [row["state"] for row in report["ages"]] == ["known", "known"], report


def test_a_run_whose_every_transfer_failed_publishes_no_age_at_all(cfg, rclone):
    """The direction that costs data, and the one a green suite would not have.

    A backup that failed halfway and published a fresh age is worse than one that
    published nothing, because it tells the destructive session it is safe to
    proceed over a library that is not backed up. The runner answers non zero for
    every command, which is what rclone does when the remote is unreachable or the
    token has expired.

    The refusal is asserted as well as the absent age, because the two are
    independent failures: an engine that published nothing while the shell
    reported success still tells the person their backup completed.
    """
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            {}, runner=_answering(1, stderr="connection refused"), now=MOMENT
        )

    cause = excinfo.value.cause
    assert cause.reason == "backup-transfer-failed", cause.to_json()
    assert cause.code is not ExitCode.INTERNAL, (
        "an unreachable remote is not a defect in this program"
    )
    assert cause.code in set(ExitCode), cause.to_json()

    after = _ages(cfg)
    assert {name: entry.state for name, entry in after.items()} == {
        "files": backup_facts.AgeState.NEVER_RECORDED,
        "database": backup_facts.AgeState.NEVER_RECORDED,
    }, after

    shown = session.record_acknowledgment(
        cfg, now=MOMENT, terminal=lambda: True
    ).shown
    assert {entry.portion: entry.state for entry in shown} == {
        "files": "never-recorded",
        "database": "never-recorded",
    }, shown
    assert all(entry.age_seconds is None for entry in shown), shown


def test_a_rehearsal_reports_a_run_and_publishes_nothing(cfg, rclone):
    """The branch beside the two above, and the one the report has to distinguish.

    A dry run neutralizes every transfer and publishes nothing, so both portions
    report ``ran`` while the fact file is untouched. Without ``dry_run`` on the
    report, a rehearsal and a real run are indistinguishable in it, and the age
    read back is what makes the distinction checkable rather than asserted.
    """
    report = backup_cli.perform_backup({backup_cli.DRY_RUN: True}, now=MOMENT)

    assert report["dry_run"] is True and report["ok"] is True, report
    assert all(row["ran"] for row in report["portions"]), report
    assert [row["state"] for row in report["ages"]] == [
        "never-recorded",
        "never-recorded",
    ], "a rehearsal recorded a backup age, so the library reads as protected by a run that copied nothing"
    assert all(
        entry.state is backup_facts.AgeState.NEVER_RECORDED
        for entry in _ages(cfg).values()
    )


def _warnings_by_portion(report: dict) -> dict[str, list[str]]:
    return {row["portion"]: [w["code"] for w in row["warnings"]] for row in report["portions"]}


def test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup(
    cfg, rclone_that_cannot_list
):
    """The drive the finding behind this unit records as never having been run.

    NOT THROUGH THE DISPATCHER, and that is not an oversight. ``backup.run`` is
    long running and only enqueues, so ``cli.run(["backup", "run"])`` returns a
    job envelope carrying none of the keys below; every end-to-end drive in this
    file calls the work body for the same reason.

    BOTH HALVES IN ONE TEST, on purpose. The backup genuinely succeeded and the
    published age is genuinely fresh, so a later reader does not mistake the new
    warning for a failed backup. What is new is that the report now says the
    rotation did not happen, which is the whole of the finding: dated archive
    folders accumulate for as long as the condition lasts, and until now nothing
    said so.
    """
    report = backup_cli.perform_backup({}, now=MOMENT)

    assert report["ok"] is True and report["dry_run"] is False, report
    assert _warnings_by_portion(report) == {
        "files": [backup.ARCHIVE_LISTING_FAILED],
        "database": [],
    }, report

    after = _ages(cfg)
    assert {name: entry.state for name, entry in after.items()} == {
        "files": backup_facts.AgeState.KNOWN,
        "database": backup_facts.AgeState.KNOWN,
    }, "a stopped rotation was read as a failed backup, which it is not"
    assert all(entry.age == timedelta(0) for entry in after.values()), after

    invoked = rclone_that_cannot_list.read_text().splitlines()
    assert any(
        line.startswith("sync ") and "remote:mirror" in line for line in invoked
    ), (
        "the mirror never ran, so the fresh age above would be measuring a run "
        f"that copied nothing: {invoked}"
    )
    assert not any("purge" in line for line in invoked), (
        "a failed listing purged something, which is how a prune removes the "
        f"only archive there is: {invoked}"
    )


def test_a_backup_whose_rotation_completed_warns_about_nothing(cfg, rclone):
    """The companion drive, without which the guard above proves less than it looks.

    A report that carried the warning unconditionally, and a report whose key was
    never populated at all, both satisfy a test that only ever sees the failing
    remote. This is the same shell against the ordinary stand-in, whose ``lsf``
    answers two dated folders.
    """
    report = backup_cli.perform_backup({}, now=MOMENT)

    assert report["ok"] is True, report
    assert _warnings_by_portion(report) == {"files": [], "database": []}, report
    assert [row["state"] for row in report["ages"]] == ["known", "known"], report


def test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run(
    cfg, rclone_that_cannot_list
):
    """A preview exists to find out whether the remote is reachable.

    The listing is the one prune command a rehearsal really issues, so a preview
    against this remote had already discovered the rotation was impossible and
    described it as though it would happen. It publishes nothing either way,
    which is asserted here beside the warning so the two cannot be confused.
    """
    report = backup_cli.perform_backup({backup_cli.DRY_RUN: True}, now=MOMENT)

    assert report["dry_run"] is True and report["ok"] is True, report
    assert _warnings_by_portion(report)["files"] == [backup.ARCHIVE_LISTING_FAILED], report
    assert [row["state"] for row in report["ages"]] == [
        "never-recorded",
        "never-recorded",
    ], report


def test_a_failing_rehearsal_is_not_reported_as_a_passing_one(cfg):
    """The branch one over, which is where this defect class reproduced in U27.

    A person rehearses precisely to find out whether the remote is reachable, so a
    failing preview that reads as a passing one makes the rehearsal worthless. The
    engine routes both branches through the same reading; this asserts the shell
    does not undo that by treating ``dry_run`` as a reason to ignore the verdict.
    """
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            {backup_cli.DRY_RUN: True},
            runner=_answering(1, stderr="connection refused"),
            now=MOMENT,
        )
    assert excinfo.value.cause.reason == "backup-transfer-failed"


def test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran(cfg, rclone):
    """The state a library backed up without quitting rekordbox is genuinely in.

    THIS IS THE CASE THE PER PORTION FACT EXISTS FOR. The mirror completes and the
    database refuses, so a single aggregate timestamp would report this library as
    fully backed up, which is exactly the thing R15's warning exists to tell a
    person. The verb must exit OK, because refusing here would tell somebody their
    backup did not happen when the mirror did.
    """
    report = backup_cli.perform_backup(
        {}, now=MOMENT, process_lister=lambda: ("rekordbox",)
    )

    assert report["ok"] is True, report
    by_portion = {row["portion"]: row for row in report["portions"]}
    assert by_portion["files"]["ran"] is True
    assert by_portion["database"]["refusal"] == "rekordbox-running", report

    after = _ages(cfg)
    assert after["files"].state is backup_facts.AgeState.KNOWN
    assert after["database"].state is backup_facts.AgeState.NEVER_RECORDED, (
        "the database portion refused and its age moved anyway, so a torn-or-absent "
        "snapshot now reads as a current one"
    )


def test_the_report_is_built_from_the_outcome_and_never_from_the_plan(cfg, rclone):
    """The reporting half of the first-caller defect, driven rather than argued.

    The plan for this fixture names commands for both portions. The run fails
    every one of them. A report derived from the plan's labels would list both
    portions as transferred; the refusal below is what a report derived from the
    results produces instead, and the plan payload is asserted non-empty first so
    the test is not passing over a plan that was empty anyway.
    """
    plan = backup.plan_backup(cfg, now=MOMENT)
    planned = backup.plan_payload(plan)
    assert all(entry["will_run"] for entry in planned["portions"]), planned
    assert sum(len(entry["commands"]) for entry in planned["portions"]) >= 2, planned

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, runner=_answering(1, stderr="refused"), now=MOMENT)
    assert excinfo.value.cause.reason == "backup-transfer-failed"
    assert set(excinfo.value.cause.detail["portions"]) == {"files", "database"}


# ---------------------------------------------------------------------------
# Refusals, each with a code from the vocabulary
# ---------------------------------------------------------------------------


def test_a_machine_with_no_rclone_refuses_by_name(cfg, no_rclone):
    """The doctor check ``binary.rclone`` exists, so this must be a name not a trace.

    Every portion refuses for one reason here, and that reason travels rather than
    being folded into a summary slug, because ``rclone-missing`` carries
    ``install-binary`` and a summary would send a person somewhere vaguer. Nothing
    is published, which is asserted rather than assumed.
    """
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, now=MOMENT)

    cause = excinfo.value.cause
    assert cause.reason == str(backup.Refusal.RCLONE_MISSING), cause.to_json()
    assert cause.code is ExitCode.PRECONDITION, cause.to_json()
    assert cause.remediation.remedy is Remedy.INSTALL_BINARY, cause.to_json()
    assert all(
        entry.state is backup_facts.AgeState.NEVER_RECORDED
        for entry in _ages(cfg).values()
    )


def test_two_portions_refused_for_different_reasons_name_both(cfg, rclone, tmp_path):
    """No single remedy exists, so the summary slug carries every reason as a step.

    Reachable rather than hypothetical: an unmounted volume refuses the file half
    for ``library-root-absent`` while the database half refuses separately for
    ``database-absent``, and picking either one would report a mounted-volume
    problem as a missing-database one half the time.
    """
    # UNMOUNTED, by moving the whole tree aside rather than by hand-building an
    # outcome. The merge bar's third condition is that the input is reachable and
    # the producer was DRIVEN, and a two-refusal outcome assembled in this file is
    # a cost over an input nothing produces. This is what a person meets when the
    # external volume is not plugged in: the file half refuses for the root and
    # the database half refuses separately for the database.
    cfg.library.root.rename(tmp_path / "unplugged")

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, now=MOMENT)
    cause = excinfo.value.cause
    assert cause.reason == "backup-nothing-ran", cause.to_json()
    assert cause.code in set(ExitCode) and cause.code is not ExitCode.INTERNAL
    assert set(cause.detail["refusals"]) == {"files", "database"}
    joined = " ".join(cause.remediation.steps)
    assert "library-root-absent" in joined and "database-absent" in joined, joined


def test_an_unconfigured_remote_refuses_in_the_backup_vocabulary(cfg, rclone):
    """``BackupRefused`` is not a ``CratekitError``, so escaping it means internal-error.

    A person who has not run setup would be told to report a defect against this
    program. The slug is a declared reason with a reserved code, so it travels
    through unchanged and the remedy is the one the reservation names.
    """
    config.save(_without_destinations(cfg))
    config.reset_cache()

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, now=MOMENT)
    cause = excinfo.value.cause
    assert cause.reason == str(backup.Refusal.REMOTE_NOT_CONFIGURED), cause.to_json()
    assert cause.code is not ExitCode.INTERNAL, cause.to_json()
    assert cause.remediation.remedy is Remedy.RUN_SETUP, cause.to_json()


def test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing(cfg, rclone):
    """Reporting no age would say this library has never been backed up.

    Two conditions with opposite fixes, which is the argument
    ``BackupFactsUnreadable`` makes at length. Driven on the read-back path
    specifically, because that is the one this unit added: the engine publishes
    through a writer that tolerates nothing, and the shell is what opens the file
    again afterwards.
    """
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_bytes(b"{not json at all")

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.published_ages(cfg, now=MOMENT)
    cause = excinfo.value.cause
    assert cause.reason == "backup-facts-unreadable", cause.to_json()
    assert cause.remediation.remedy is Remedy.REPAIR_BACKUP_FACTS, cause.to_json()


def test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception(cfg):
    """Three remedies, and a permission is not a corruption.

    ``backup_facts.Remedy`` names three and one of them is a permission on a
    directory, which repairing a file does not touch. Fixing the remedy at
    ``repair-backup-facts`` here would send a person to reset the record of when
    their music was last protected in order to fix an access problem.
    """
    raised = backup_facts.BackupFactsUnreadable(
        "a directory on the way to it could not be opened",
        path=backup_facts.path_for(cfg),
        remedy=backup_facts.Remedy.GRANT_PATH_ACCESS,
    )

    def unreadable(*_args, **_kwargs):
        raise raised

    original = backup_facts.ages
    backup_facts.ages = unreadable  # noqa: B010 - restored below
    try:
        with pytest.raises(CratekitError) as excinfo:
            backup_cli.published_ages(cfg, now=MOMENT)
    finally:
        backup_facts.ages = original
    assert excinfo.value.cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS, (
        excinfo.value.cause.to_json()
    )


# ---------------------------------------------------------------------------
# The classifier, held at its own altitude
# ---------------------------------------------------------------------------


def test_nothing_that_ran_is_never_reported_as_a_refusal():
    """The other direction of ``refusal_for``, so it is not a function that always fires.

    A guard that refuses every run is indistinguishable from a broken verb, and
    the partial case above is the one that would be lost: refusing there tells a
    person their mirror did not happen when it did.
    """
    ran = backup.PortionOutcome(portion=backup_facts.Portion.FILES, ran=True)
    refused = backup.PortionOutcome(
        portion=backup_facts.Portion.DATABASE,
        ran=False,
        refusal=backup.Refusal.REKORDBOX_RUNNING,
        detail="rekordbox is running",
    )
    assert backup_cli.refusal_for(backup.BackupOutcome(stamp="s", portions=(ran,))) is None
    assert (
        backup_cli.refusal_for(backup.BackupOutcome(stamp="s", portions=(ran, refused)))
        is None
    )


def test_a_failed_portion_decides_the_run_even_when_the_other_completed():
    """Half a backup with a published age for the working half is not a success.

    The order matters: a portion that FAILED is checked before the question of
    whether anything ran, because a person told a backup succeeded stops looking.
    """
    ran = backup.PortionOutcome(portion=backup_facts.Portion.FILES, ran=True)
    failed = backup.PortionOutcome(
        portion=backup_facts.Portion.DATABASE,
        ran=False,
        detail="database portion failed: connection refused",
    )
    refusal = backup_cli.refusal_for(
        backup.BackupOutcome(stamp="s", portions=(ran, failed))
    )
    assert refusal is not None
    assert refusal.cause.reason == "backup-transfer-failed"
    assert refusal.cause.detail["portions"] == ["database"]


def test_an_outcome_with_no_portions_refuses_rather_than_raising():
    """``plan_backup`` cannot produce one, and the answer is still an answer.

    An index error here would surface as ``internal-error`` in a detached child
    whose only output is a log nobody is watching, and "nothing ran" is the same
    verdict however few portions there were.
    """
    refusal = backup_cli.refusal_for(backup.BackupOutcome(stamp="s", portions=()))
    assert refusal is not None and refusal.cause.reason == "backup-nothing-ran"


def test_a_supplied_configuration_is_used_rather_than_the_one_on_disk(cfg, rclone, tmp_path):
    """The frozen configuration the job driver's contract says a handler runs against.

    Both directions, because either alone passes over a parameter that is ignored:
    a run handed a configuration must use it, and a run handed none must load. The
    cost this guards is specific rather than general. A backup queued against one
    remote and claimed after the person reconfigured their destinations would copy
    the library somewhere they did not ask for, and would then publish an age
    naming a destination the queued run never targeted, which is the one thing
    ``BackupFact`` records ``destination`` to make visible.

    Measured off the DESTINATION the fact carries rather than off the report,
    because that is the field a later reader compares against their current
    remote.
    """
    elsewhere = replace(cfg, backup=replace(cfg.backup, dest="other:mirror"))

    backup_cli.perform_backup({}, cfg=elsewhere, now=MOMENT)
    assert _ages(cfg)["files"].destination == "other:mirror", (
        "the supplied configuration was ignored and the one on disk was loaded"
    )

    backup_cli.perform_backup({}, now=MOMENT)
    assert _ages(cfg)["files"].destination == "remote:mirror", (
        "with nothing supplied the configuration on disk is what a run targets"
    )


def test_the_shell_never_writes_the_backup_fact_itself():
    """One writer of one fact, asserted against the source rather than argued.

    The engine publishes from what transferred; anything the shell knows about is
    the plan. A second writer here is the shape that publishes a fresh age over a
    portion that refused, and it is invisible to every other test in this file,
    because the engine's own write already satisfies every one of them.

    AN AST WALK RATHER THAN A SUBSTRING, and the difference is not fastidiousness.
    A ``"backup_facts.record" not in source`` check was written first and it
    failed immediately, on the module's own docstring, which names the function to
    explain why the shell must not call it. A guard a comment can trip is a guard
    that gets widened rather than read, and widening it to ignore docstrings would
    have left it matching a call inside a string too.
    """
    tree = ast.parse(Path(backup_cli.__file__).read_text())
    called = {
        f"{node.func.value.id}.{node.func.attr}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
    }
    assert "backup_facts.record" not in called, (
        "the shell writes the backup fact, so two writers now decide one value"
    )
    assert "backup_facts.ages" in called, (
        "the walk found no call to ages either, so it is matching nothing and the "
        "assertion above is vacuous"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Round two: one test per user facing zero the round one table found
# ═══════════════════════════════════════════════════════════════════════════
#
# Every test below exists because `docs/mutation/u45-round-1.md` reported a
# guard this file did not hold. They are grouped rather than filed beside their
# subjects so that the round is visible as a round: a later reader can see what
# the author's own table could not kill, which is the number METHOD says an
# author's table is actually for.


def test_the_transfer_failure_says_no_age_was_published(cfg, rclone):
    """The sentence, not only the slug, because the sentence is what a person acts on.

    Round one row ``C7_failed_detail_dropped`` reworded this message and killed
    nothing: every assertion in this file read the reason and none read what the
    refusal actually told anybody. The message is the only place the run says the
    fact file was left alone, which is the difference between "try again" and
    "your library is not backed up and the tool knows it".

    Asserted by MEANING rather than by quoting the sentence whole, so a rewording
    that keeps the claim passes and one that drops the claim fails. Quoting it
    whole would be a guard that forbids this wording rather than this promise.
    """
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            {}, runner=_answering(1, stderr="connection refused"), now=MOMENT
        )
    message = excinfo.value.cause.message
    assert "backup age" in message and "published" in message, message
    assert "files" in message and "database" in message, (
        f"the refusal does not say which portions failed: {message}"
    )


def test_the_report_carries_the_age_number_and_not_only_the_state(cfg, rclone):
    """The number R15's warning quotes, which round one found nothing asserted.

    Row ``A3_age_seconds_always_none`` replaced every reported age with None and
    killed nothing: the acknowledgment drive asserts the seconds it reads back
    through the session, and this file never asserted the same value on the verb's
    OWN report. A report whose state says known and whose age is absent describes a
    library nobody can say anything about the freshness of.

    Driven at a moment an hour after the run rather than at the run's own instant,
    because zero is the one value a broken implementation and a correct one agree
    on, and the first draft of the guard above measured exactly that.
    """
    backup_cli.perform_backup({}, now=MOMENT)
    later = backup_cli.published_ages(cfg, now=MOMENT + timedelta(hours=1))
    assert [row["state"] for row in later] == ["known", "known"], later
    assert all(row["age_seconds"] == 3600.0 for row in later), later
    assert all(row["completed_at"] == MOMENT.isoformat() for row in later), later


def test_a_resume_reports_the_queued_job_rather_than_filing_a_second(cfg, rclone):
    """The ``--job`` branch, which round one found undriven.

    Row ``H3_resume_branch_dropped`` made every invocation enqueue and killed
    nothing, because every drive in this file queued a first backup and none
    continued one. The cost is specific: the job engine respawns a queued verb as a
    child carrying ``--job``, so a handler that always enqueues files a NEW backup
    on every respawn, the queue grows without bound, and the original never
    advances.

    The store is counted as well as the identifier, because a handler that
    enqueued a second job and then reported the first would satisfy the identifier
    assertion alone.

    THE ``rclone`` FIXTURE IS LOAD BEARING NOW AND WAS NOT BEFORE. Until the
    handler was bound this resume reported the job and ran nothing, so it needed no
    remote and took none. It drives real portions now, so without the stand-in it
    reads whatever rclone this laptop happens to have and passes or fails on that.
    Measured: it failed here on the first run after the binding, against a real
    rclone and a remote named ``remote:`` that does not exist.
    """
    code, first = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), first
    job_id = first["data"]["job_id"]

    code, second = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), second
    assert second["data"]["job_id"] == job_id, (
        "the resume filed a second backup rather than reporting the one queued"
    )
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1, (
            "a second job exists, so every respawn of this verb would add another"
        )


def test_the_outcome_answers_not_ok_when_a_portion_failed(cfg, rclone):
    """``BackupOutcome.ok``, which round one found nothing anywhere asserts as False.

    Row ``E5_outcome_ok_widened`` changed the property from ``all`` to ``any`` and
    killed nothing. This file asserts ``report["ok"] is True`` twice and never the
    other value, and the reason it cannot is worth stating rather than working
    around: :func:`refusal_for` raises whenever a portion failed, which is exactly
    the condition that makes ``ok`` false, so no report this shell can emit ever
    carries ``ok: false``. That is recorded as a residual.

    So the property is driven where it is reachable, on the ENGINE's own return
    value, which this unit is the first caller of. Both directions, because ``all``
    and ``any`` agree on every outcome where nothing failed.
    """
    plan = backup.plan_backup(cfg, now=MOMENT)

    both_fine = backup.run_backup(
        cfg, plan, runner=_answering(0), now=MOMENT, publish=False
    )
    assert both_fine.ok is True, both_fine

    one_failed = backup.run_backup(
        cfg,
        plan,
        runner=_failing_on(backup.SNAPSHOT_DATABASE),
        now=MOMENT,
        publish=False,
    )
    assert one_failed.ok is False, (
        "a portion whose transfer came back non zero left the outcome reporting ok, "
        "so any caller deciding on that field would report a failed backup as done"
    )
    assert [p.ran for p in one_failed.portions] == [True, False], one_failed


# ---------------------------------------------------------------------------
# U50: the portion is the item, and the item is what the driver claims
# ---------------------------------------------------------------------------


def _labels(runner) -> list[str]:
    """Every command label the injected runner was asked for, in order."""
    return [command.label for command in runner.seen]


def _running(*names: str):
    """A process lister answering with these names, for the database gate."""
    return lambda: tuple(names)


def test_a_named_portion_runs_only_its_own_half(cfg):
    """The narrowing, measured on both portions rather than asserted on one.

    Both directions, because a narrowing that returned the whole plan would still
    look right from the FILES side alone: the mirror is first in declaration order,
    so a report naming it appears whether or not the database also ran. The pair is
    what makes the claim checkable.
    """
    files = _answering(0)
    backup_cli.perform_backup(
        {}, portion=backup_facts.Portion.FILES, cfg=cfg, runner=files, now=MOMENT
    )
    assert _labels(files), "the files portion ran no commands at all"
    assert backup.SNAPSHOT_DATABASE not in _labels(files), (
        "a job item claiming the files portion also ran the database snapshot, so "
        "every item of the job would do the whole backup"
    )

    database = _answering(0)
    backup_cli.perform_backup(
        {}, portion=backup_facts.Portion.DATABASE, cfg=cfg, runner=database, now=MOMENT
    )
    assert _labels(database) == [backup.SNAPSHOT_DATABASE], (
        f"the database portion ran {_labels(database)}, not the snapshot alone"
    )


def test_no_portion_named_still_runs_the_whole_plan(cfg):
    """The default that keeps every caller older than the binding measuring the same thing."""
    whole = _answering(0)
    report = backup_cli.perform_backup({}, cfg=cfg, runner=whole, now=MOMENT)
    assert backup.SNAPSHOT_DATABASE in _labels(whole), _labels(whole)
    assert [entry["portion"] for entry in report["portions"]] == ["files", "database"]


def test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy(cfg, rclone):
    """THE HAZARD THIS FORECLOSES, and it is the reason this unit reversed a decision.

    An item that COMPLETES over a portion nothing copied is done for ever.
    ``jobs.complete_item`` writes ``done``, and ``jobs.retry`` re-arms only ``failed``
    and ``claimed`` rows, stating in its own docstring that "Items that are DONE stay
    done". So a build that suppressed this refusal because the other portion would
    run would leave a person who quits rekordbox and resumes with nothing happening,
    for ever, over a job reporting SUCCEEDED and a database that was never copied.

    The refusal carries the portion's RESERVED remediation rather than the class
    default, which is what makes failing it recoverable: ``quit-rekordbox`` names
    the thing the person does, after which the resume finishes the backup.
    """
    with pytest.raises(CratekitError) as caught:
        backup_cli.perform_backup(
            {},
            portion=backup_facts.Portion.DATABASE,
            cfg=cfg,
            runner=_answering(0),
            now=MOMENT,
            process_lister=_running("rekordbox"),
        )
    assert caught.value.cause.reason == str(backup.Refusal.REKORDBOX_RUNNING)
    assert caught.value.cause.remediation.remedy is Remedy.QUIT_REKORDBOX, (
        "the refusal lost its reserved remediation, so a person whose only problem "
        "is an open application is sent to a diagnostic instead of told to close it"
    )


def test_a_machine_with_no_rclone_fails_every_portion_by_name(cfg, no_rclone):
    """Nothing ran, so nothing is reported as done, and each item says why itself."""
    for portion in backup_facts.Portion:
        with pytest.raises(CratekitError) as caught:
            backup_cli.perform_backup({}, portion=portion, cfg=cfg, now=MOMENT)
        assert caught.value.cause.reason == str(backup.Refusal.RCLONE_MISSING)
        assert caught.value.cause.remediation.remedy is Remedy.INSTALL_BINARY, (
            "the class default replaced the reserved remedy, so a person with no "
            "rclone is told to run a diagnostic that would report the same thing"
        )


def test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion(cfg, rclone):
    """One portion's non zero return is that portion's failure and no other's."""
    with pytest.raises(CratekitError) as caught:
        backup_cli.perform_backup(
            {},
            portion=backup_facts.Portion.DATABASE,
            cfg=cfg,
            runner=_failing_on(backup.SNAPSHOT_DATABASE),
            now=MOMENT,
        )
    assert caught.value.cause.reason == "backup-transfer-failed"
    assert caught.value.cause.detail["portions"] == ["database"], caught.value.cause.detail


def test_the_queued_caller_does_not_read_the_age_back_inside_the_item(cfg, rclone):
    """R16: a condition found AFTER the work completed must not fail the item.

    THE SCENARIO IS A REHEARSAL, AND THE REASON IT HAS TO BE IS WORTH RECORDING,
    because the wider claim this guard was first written for turned out to be
    false and was measured here rather than argued. The wider claim was that in a
    REAL run an unreadable fact file would fail an item whose transfer had already
    completed. It cannot: ``run_backup`` publishes through ``backup_facts.record``,
    which reads the file before it writes, so the same unreadable file fails inside
    the ENGINE first and the portion never reaches this report at all. The two
    readers fail together because they are the same reader.

    A DRY RUN is where the two come apart, and it is reachable: ``run_backup``
    sets ``publish`` false for a rehearsal, so nothing reads the fact file on the
    way through, and the read back would be the only thing that touched it. Under
    the driver that would fail an item over a rehearsal that copied nothing and
    changed nothing, and every resume would do it again. So the caller that
    discards the report asks for the read not to happen.

    Driven with a fact file that is a DIRECTORY, which is one of the three
    conditions ``BackupFactsUnreadable`` names, so the refusal is the real one
    rather than a patched stand-in.
    """
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).mkdir()
    rehearsal = {backup_cli.DRY_RUN: True}

    report = backup_cli.perform_backup(
        rehearsal,
        portion=backup_facts.Portion.FILES,
        cfg=cfg,
        runner=_answering(0),
        now=MOMENT,
        read_back=False,
    )
    assert "ages" not in report, (
        "the queued caller read the age back, so an unreadable fact file would "
        "fail an item over a rehearsal that touched nothing"
    )
    assert report["dry_run"] is True, report

    with pytest.raises(CratekitError) as caught:
        backup_cli.perform_backup(
            rehearsal,
            portion=backup_facts.Portion.FILES,
            cfg=cfg,
            runner=_answering(0),
            now=MOMENT,
        )
    assert caught.value.cause.reason == "backup-facts-unreadable", (
        "reading the age back stopped refusing, so the guard above measures a "
        "difference between the two callers that no longer exists"
    )


def test_an_item_naming_something_that_is_not_a_portion_refuses_by_name(cfg):
    """A job queued by a build with a different portion vocabulary, diagnosed."""
    job = jobs.Job(
        job_id="J1",
        handler_key="backup.run",
        payload={},
        config_fingerprint="",
        config_toml="",
        library_id="",
        state=jobs.JobState.RUNNING,
        created=MOMENT.isoformat(),
        updated=MOMENT.isoformat(),
    )
    item = jobs.Item(
        job_id="J1", item_id="playlists", ordinal=0, state=jobs.ItemState.CLAIMED
    )
    with pytest.raises(CratekitError) as caught:
        backup_cli.handle(job, item, cfg)
    assert caught.value.cause.reason == "internal-error"
    assert "playlists" in caught.value.cause.message
    for portion in backup_facts.Portion:
        assert str(portion) in caught.value.cause.message, (
            "the refusal did not name the portions this build declares, so a "
            "reader cannot tell what the item should have said"
        )


def test_the_handler_uses_the_configuration_it_was_handed(cfg, tmp_path, rclone):
    """KTD9 through the handler: the frozen destination, not the one on disk.

    The cost of getting this wrong is specific to backup rather than general: a job
    queued against one remote and claimed after the person reconfigured their
    destinations copies the library somewhere they did not ask for, and publishes
    an age naming a destination the queued run never targeted.
    """
    frozen = replace(cfg, backup=replace(cfg.backup, dest="remote:the-frozen-one"))
    config.save(replace(cfg, backup=replace(cfg.backup, dest="remote:the-later-one")))
    config.reset_cache()

    job = jobs.Job(
        job_id="J2",
        handler_key="backup.run",
        payload={},
        config_fingerprint="",
        config_toml="",
        library_id="",
        state=jobs.JobState.RUNNING,
        created=MOMENT.isoformat(),
        updated=MOMENT.isoformat(),
    )
    item = jobs.Item(
        job_id="J2", item_id="files", ordinal=0, state=jobs.ItemState.CLAIMED
    )
    assert backup_cli.handle(job, item, frozen) is None, (
        "the handler produced something for the engine to commit, but a backup "
        "writes to a remote and leaves no local file to put in place"
    )
    invoked = rclone.read_text()
    assert "remote:the-frozen-one" in invoked, invoked
    assert "remote:the-later-one" not in invoked, (
        "the handler reached the configuration on disk rather than the one frozen "
        "on the job, which is the resume bug KTD9 closes"
    )


# ---------------------------------------------------------------------------
# U50: the queued backup runs, and the queue never reports an empty success
# ---------------------------------------------------------------------------


def _item_states(job_id: str) -> dict[str, str]:
    """Every item of one job, keyed by portion, READ BACK from the store."""
    with jobs.open_store() as store:
        return {item.item_id: str(item.state) for item in jobs.items(store, job_id)}


def test_a_backup_job_carries_one_item_per_declared_portion(cfg):
    """THE ZERO ITEM RULE, which is the hazard binding a worker would otherwise create.

    ``jobs.drive`` transitions a job whose item count is zero straight to SUCCEEDED
    by design: ``claim`` returns nothing on the first pass, nothing was attempted,
    nothing failed, and the final branch records success. So a bound handler over an
    empty item list does not leave the queue stuck the way R-198 describes. It
    reports a backup that copied nothing, which is strictly worse, because the
    first teaches a person that queues do not run and the second teaches them they
    are protected.

    The expectation is DERIVED from the enum rather than written as a pair, so this
    test cannot pass a build that adds a third portion and forgets to queue it.
    """
    code, envelope = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), envelope
    states = _item_states(envelope["data"]["job_id"])

    assert states, (
        "the backup was queued with no items at all, so driving it would report "
        "SUCCEEDED over a library nothing copied"
    )
    assert set(states) == {str(portion) for portion in backup_facts.Portion}, (
        f"the queued items are {sorted(states)}, which is not the set of portions "
        f"{[str(p) for p in backup_facts.Portion]} a backup is made of"
    )


def test_queueing_still_needs_nothing_from_the_machine(cfg, no_rclone, monkeypatch):
    """The items come from the enum, so the property queueing had before survives.

    Stated separately from the fixture-level test above it because this is what
    the derivation is FOR: items built from ``plan_backup`` would be the more direct
    answer and would make queueing resolve rclone, read the process table and stat
    the library root, so a person on an unmounted volume could not even file the
    job that would have run fine once the volume came back.
    """
    monkeypatch.setattr(Path, "is_dir", lambda self: False)
    code, envelope = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), envelope
    assert len(_item_states(envelope["data"]["job_id"])) == len(backup_facts.Portion)


def test_a_queued_backup_runs_every_portion_through_the_real_resume(cfg, rclone):
    """R-198's whole claim, closed for this verb and driven end to end.

    Through the DISPATCHER rather than by calling the handler, because the thing
    that was missing was never the work body: it was that nothing in ``src`` reached
    it. The item rows are read back from the store rather than taken off the
    envelope, so what is asserted is what the queue records rather than what the
    report says about itself.
    """
    code, queued = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    assert set(_item_states(job_id).values()) == {"pending"}

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == "succeeded", resumed["data"]
    assert set(_item_states(job_id).values()) == {"done"}, _item_states(job_id)

    invoked = rclone.read_text()
    assert "remote:mirror" in invoked and "remote:database-snapshots" in invoked, (
        "the driven job did not reach both portions, so a resume copies less than "
        "the backup the person asked for"
    )


def test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope(
    cfg, rclone
):
    """R9 and R15 together: the engine publishes it, and the shell reports it.

    The fact file is read through ``backup_facts.ages``, which is the function
    ``core.session._shown_ages`` calls, so what is checked is what a destructive
    session would see rather than this file's opinion of the format. The envelope
    is then compared against it rather than asserted on its own, because a resume
    that rendered a plausible age from the outcome would satisfy an envelope-only
    assertion while the session still saw ``never-recorded``.
    """
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    published = {
        str(entry.portion): entry for entry in backup_facts.ages(cfg)
    }
    for portion in backup_facts.Portion:
        assert published[str(portion)].state is backup_facts.AgeState.KNOWN, (
            f"the {portion} portion ran and published no age, so a destructive "
            f"session sees a library that has never been backed up"
        )

    reported = {entry["portion"]: entry for entry in resumed["data"]["ages"]}
    assert set(reported) == {str(p) for p in backup_facts.Portion}, reported
    for portion in backup_facts.Portion:
        assert reported[str(portion)]["state"] == str(backup_facts.AgeState.KNOWN)


def test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion(
    cfg, rclone, monkeypatch
):
    """R11, and THE ROUTE IS THE PART THAT IS EASY TO GET WRONG.

    A job with a failed item ends FAILED, and FAILED is terminal, so neither the
    ``--job`` branch nor ``jobs.drive`` will touch it again: ``job.is_open()`` is
    false and the engine refuses to re-drive a recorded answer. ``jobs.retry`` is
    the only thing that re-arms a failed item, and the shipped verb that calls it
    is ``crate job resume``, which then spawns a detached child. So the retry is
    driven here directly and the resume branch runs it, which is the same seam the
    child would take.

    The second pass is counted rather than assumed. That the mirror is NOT redone
    is the whole reason the portions are the items, and a test that only checked
    the database succeeded would pass just as well if both had run again.
    """
    def only_the_database_fails(command):
        if command.label == backup.SNAPSHOT_DATABASE:
            return backup.CommandResult(returncode=1, stderr="connection refused")
        return backup.CommandResult(returncode=0)

    monkeypatch.setattr(backup, "subprocess_runner", only_the_database_fails)
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]

    code, failed = _drive(["backup", "run", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    assert _item_states(job_id) == {"files": "done", "database": "failed"}, (
        _item_states(job_id)
    )

    seen: list[str] = []

    def everything_works(command):
        seen.append(command.label)
        return backup.CommandResult(returncode=0)

    monkeypatch.setattr(backup, "subprocess_runner", everything_works)
    with jobs.open_store() as store:
        jobs.retry(store, job_id)

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert _item_states(job_id) == {"files": "done", "database": "done"}
    assert backup.MIRROR not in seen, (
        f"the retry ran {seen}, so it redid the mirror that had already completed "
        f"and the per portion item ledger bought nothing"
    )


def test_a_job_in_which_nothing_ran_never_reports_success(cfg, no_rclone):
    """R13, driven through the dispatcher rather than at the work body.

    Asserted on what ``crate`` exits with and on what the item rows say, because
    that is where a person meets it. Every item fails, ``jobs.drive`` finds nothing
    processed, and the job is recorded FAILED before the refusal is raised.
    """
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code != int(ExitCode.OK), resumed
    assert set(_item_states(job_id).values()) == {"failed"}, _item_states(job_id)
    with jobs.open_store() as store:
        assert str(jobs.get(store, job_id).state) == "failed"


def test_the_configuration_the_worker_runs_against_is_the_frozen_one(cfg, rclone):
    """KTD9 end to end, and the drift the person is told about rather than silently given.

    The destination is what makes this concrete for backup rather than general: a
    job queued against one remote and claimed after the person reconfigured copies
    the library somewhere they did not ask for.
    """
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]

    config.save(replace(cfg, backup=replace(cfg.backup, dest="remote:somewhere-else")))
    config.reset_cache()

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    invoked = rclone.read_text()
    assert "remote:mirror" in invoked, invoked
    assert "remote:somewhere-else" not in invoked, (
        "the driven job copied to the destination configured after it was queued, "
        "which is the resume bug KTD9 closes"
    )
    assert any(w["code"] == "config-drift" for w in resumed.get("warnings", [])), (
        f"the run used the frozen configuration and did not say so: "
        f"{resumed.get('warnings')}"
    )


def test_a_queued_backup_reports_a_bound_worker(cfg):
    """R14, asked the way a person asks it rather than of the table.

    ``crate job show`` derives its ``worker`` field from the declaration table
    without importing anything, which is what lets a supervising process answer
    "will this job ever run" without pulling every feature module into itself. Until
    this unit the answer for a backup was ``none``, and R-203 says that field exists
    precisely so a queued job that will never run says so.

    Driven through the dispatcher rather than asserted on ``handlers.HANDLERS``,
    because the table having a key and the reporting surface reading it are two
    facts, and this unit changed only one of them.

    LIVES HERE RATHER THAN IN ``tests/test_handlers.py`` because it needs a real
    queued backup job, and the configuration and dispatcher fixtures for that are
    in this file. The population guards that quantify over the registry stay there
    and needed no edit, which is the property they were built for.
    """
    _, queued = _drive(["backup", "run"])
    code, shown = _drive(["job", "show", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), shown
    reported = shown["data"]["progress"]
    assert reported["worker"] == "bound", (
        f"a queued backup still reports {reported.get('worker')!r}, so the "
        f"surface that tells a person whether their job can run says it cannot"
    )
    assert reported["worker_reason"] is None, reported


def test_the_item_list_is_derived_from_the_portions_rather_than_written_out(
    cfg, monkeypatch
):
    """P3: the set is derived at run time, or it is a list in disguise.

    WHY THE ENUM IS REPLACED RATHER THAN THE PAIR ASSERTED. A test comparing
    ``backup_items()`` against ``backup_facts.Portion`` passes for a hand written
    ``("files", "database")`` too, because the two agree on every build that has
    exactly the portions this one has. That is what makes the derivation look
    untested when it is not: measured as a zero row on 2026-09-02, where replacing
    the comprehension with the literal pair killed nothing across the whole suite.

    So the enum is stood in for. A third portion is what a literal cannot follow,
    and it is exactly the condition P3 exists for: the planner would build an entry
    nothing claims, and the queue would run two thirds of a backup with everything
    green.
    """

    class ThreePortions(StrEnum):
        FILES = "files"
        DATABASE = "database"
        SETTINGS = "settings"

    monkeypatch.setattr(backup_facts, "Portion", ThreePortions)
    assert backup_cli.backup_items() == ("files", "database", "settings"), (
        "the item list did not follow a portion added to the enum, so it is a "
        "second declaration of the set rather than a reading of it"
    )


def test_the_handler_does_not_fail_an_item_over_the_age_read_back(cfg, rclone):
    """R16 through the HANDLER, which is the caller the guard is for.

    The work body's own guard is driven above. This drives the seam that uses it:
    ``handle`` asks for the read back not to happen, and the proof is that a fact
    file which cannot be read does not turn into a failed item. Measured as a zero
    row on 2026-09-02 without this test, because nothing drove the handler against
    an unreadable fact file at all.

    A REHEARSAL, for the reason the work body's test gives at length: in a real run
    the engine's own publish reads the same file first and fails there, so the two
    readers cannot be told apart. A dry run publishes nothing, so this read would be
    the only one.
    """
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).mkdir()

    job = jobs.Job(
        job_id="J3",
        handler_key="backup.run",
        payload={backup_cli.DRY_RUN: True},
        config_fingerprint="",
        config_toml="",
        library_id="",
        state=jobs.JobState.RUNNING,
        created=MOMENT.isoformat(),
        updated=MOMENT.isoformat(),
    )
    item = jobs.Item(
        job_id="J3", item_id="files", ordinal=0, state=jobs.ItemState.CLAIMED
    )
    assert backup_cli.handle(job, item, cfg) is None, (
        "the handler read the age back, so an unreadable fact file fails an item "
        "over a rehearsal that copied nothing and every resume repeats it"
    )


# ---------------------------------------------------------------------------
# U50 review round: what a second look, an old job and a broken fact file do
# ---------------------------------------------------------------------------


def test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice(
    cfg, rclone, monkeypatch
):
    """The check has to sit OUTSIDE the ``is_open`` branch, and this is why.

    Three reviewers found the same defect in the first draft independently. The
    re-raise was inside ``if job.is_open():``, which answers the run that CLOSES
    the job and gets the second look at it wrong: a job already FAILED on entry is
    not open, so the drive is skipped and the check was skipped with it. The verb
    then reported the failure once and exited 0 for ever after, over the same half
    copied library, which is the silence the check exists to break.

    Driven as two identical commands rather than one, because a test that resumes
    once cannot tell the two placements apart.
    """
    monkeypatch.setattr(backup, "subprocess_runner", _failing_on(backup.SNAPSHOT_DATABASE))
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]

    first, _ = _drive(["backup", "run", "--job", job_id])
    assert first != int(ExitCode.OK)

    second, envelope = _drive(["backup", "run", "--job", job_id])
    assert second != int(ExitCode.OK), (
        "the second look at a job that ended FAILED exited OK, so a person who "
        "runs the command again is told a half copied backup is fine"
    )
    assert second == first, (
        f"the same question got two answers, {first} then {second}"
    )
    assert envelope["cause"] is not None, envelope


def test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding(
    cfg, rclone
):
    """THE UPGRADE HAZARD, and it is the reason this guard is not paranoia.

    Before this unit ``backup_library`` enqueued with no ``item_ids`` at all. The
    queue is a durable file and this unit does not change its schema version, so a
    person who upgrades still has those jobs in it, and binding the handler is what
    makes them drivable. ``jobs.drive`` transitions a job whose item count is zero
    straight to SUCCEEDED, so driving one reports a backup over a library nothing
    copied, which is the exact hazard this whole unit is built to prevent arriving
    by the one door it did not watch.

    The job is built the way the OLD build built it, by calling ``enqueue`` with no
    items, rather than by deleting rows from a job this build queued. A test that
    deleted rows would prove the guard reads the ledger; this one proves it catches
    the shape that actually exists on someone's disk.
    """
    with jobs.open_store() as store:
        stale = jobs.enqueue(
            store,
            handler_key="backup.run",
            payload=backup_cli.frozen_payload(False),
            cfg=cfg,
        )
        assert jobs.items(store, stale.job_id) == (), (
            "the fixture queued items, so this test no longer builds the shape "
            "the previous build left behind"
        )

    code, envelope = _drive(["backup", "run", "--job", stale.job_id])
    assert code != int(ExitCode.OK), (
        "a backup job with no items reported success, so an upgrade turns every "
        "job queued by the old build into a backup that copied nothing"
    )
    with jobs.open_store() as store:
        assert jobs.get(store, stale.job_id).state is jobs.JobState.QUEUED, (
            "the empty job was driven anyway and is now terminal, so the refusal "
            "arrived after the damage it exists to prevent"
        )


def test_an_unwritable_fact_file_says_which_file_rather_than_report_defect(cfg, rclone):
    """The engine publishes THROUGH the fact file and can fail ON it.

    ``run_backup`` calls ``backup_facts.record`` once a portion's commands return
    zero, and ``record`` reads the file before it writes, so an unparseable file
    raises with the transfer already done. ``BackupFactsUnreadable`` is a plain
    ``Exception`` rather than a ``CratekitError``, so under the driver it would land
    in ``jobs.drive``'s ``except Exception`` and be recorded as ``internal-error``
    carrying ``report-defect``: a person with one bad file in their state directory
    told to file a bug against this program, with every retry repeating the whole
    transfer to reach the same line.

    The item still fails, which is right rather than a compromise: an age that
    cannot be published is a copy a destructive session cannot see. What is asserted
    here is that the person is told which file to fix.
    """
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).mkdir()

    with pytest.raises(CratekitError) as caught:
        backup_cli.perform_backup(
            {},
            portion=backup_facts.Portion.FILES,
            cfg=cfg,
            runner=_answering(0),
            now=MOMENT,
            read_back=False,
        )
    assert caught.value.cause.reason == "backup-facts-unreadable", (
        f"the publish failure surfaced as {caught.value.cause.reason!r}, which "
        f"sends a person to file a defect over a file they could repair"
    )
    assert caught.value.cause.remediation.remedy is not Remedy.REPORT_DEFECT
    assert str(backup_facts.path_for(cfg)) in caught.value.cause.detail["path"]


def test_the_ages_reported_are_the_ones_this_job_published(cfg, rclone, tmp_path):
    """The envelope describes THIS job, so it reads the job's own configuration.

    ``config.state_path`` resolves the fact file under the configured library, so a
    live configuration naming a different library points at a different file from
    the one the item wrote. Reading the live one would answer a question nobody
    asked, in the same envelope that reports the job.

    Driven by moving the library between queue and resume, which is the only way
    the two readings can differ.
    """
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    elsewhere = tmp_path / "another-library"
    (elsewhere / "Music").mkdir(parents=True)
    config.save(replace(cfg, library=replace(cfg.library, root=elsewhere)))
    config.reset_cache()

    code, again = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), again
    reported = {entry["portion"]: entry for entry in again["data"]["ages"]}
    for portion in backup_facts.Portion:
        assert reported[str(portion)]["state"] == str(backup_facts.AgeState.KNOWN), (
            f"the {portion} age read back as {reported[str(portion)]['state']}, so "
            f"the envelope answered from the live library rather than the one this "
            f"job copied"
        )
