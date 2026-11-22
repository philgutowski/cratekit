"""U45: ``crate backup run``, the shell over the backup engine (row 31).

``tests/modules/test_tools.py`` proves the engine publishes an age per portion;
this proves the shell keeps that promise, read back through
:func:`cratekit.core.backup_facts.ages`, the function a destructive session
reads. A failed backup leaves the age at ``never-recorded``; it does not itself
make a session refuse. The stand-in rclone sits on ``CRATEKIT_BIN_RCLONE``; where
a test is about the shell's reading of a result, the ``runner`` seam is used.
No name here is a real volume, person or remote account (D1).
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
from cratekit.cli import output, registry
from cratekit.core import backup_facts, binaries, config, jobs, profiles, session
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.tools import backup

#: A fixed instant, so an age is a computation rather than a race. Far enough
#: from any real clock that a test reading a real one would fail loudly.
MOMENT = datetime(2026, 8, 29, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library with the four backup destinations, SAVED."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    # R-1761. A library holds its music: an empty folder at the root is what an
    # unmounted volume leaves, and a backup now refuses it.
    (root / "Music" / "fixture.flac").write_bytes(b"one track")
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
    """No rekordbox process, injected, so no test depends on this machine."""
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def rclone(monkeypatch, tmp_path) -> Path:
    """A stand-in for rclone on the ONE seam the product ships for it."""
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
    """The same stand-in, except that ``lsf`` fails and everything else does not."""
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
    """A machine with no rclone at all, built rather than hoped for, and ASSERTED."""
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
    """A runner that gives every command one answer, and records what it was asked."""
    seen: list[backup.Command] = []

    def runner(command: backup.Command) -> backup.CommandResult:
        seen.append(command)
        return backup.CommandResult(returncode=returncode, stdout=stdout, stderr=stderr)

    runner.seen = seen  # type: ignore[attr-defined]
    return runner


def _failing_on(label: str):
    """A runner that fails only the commands carrying one label."""

    def runner(command: backup.Command) -> backup.CommandResult:
        if command.label == label:
            return backup.CommandResult(returncode=1, stderr="connection refused")
        return backup.CommandResult(returncode=0)

    return runner


def _without_destinations(cfg_value):
    """The same configuration with the off-machine destinations removed."""
    return replace(
        cfg_value,
        backup=replace(
            cfg_value.backup, remote="", dest="", archive_root="", db_dest_root=""
        ),
    )


def _queued_and_resumed(argv=("backup", "run")) -> tuple[dict, dict]:
    """Queue a backup and resume it, both through the dispatcher and both OK."""
    code, queued = _drive(list(argv))
    assert code == int(ExitCode.OK), queued
    code, resumed = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), resumed
    return queued, resumed


def _ages(cfg) -> dict[str, backup_facts.PortionAge]:
    """Every portion's age, keyed by name, READ from the fact file."""
    return {str(entry.portion): entry for entry in backup_facts.ages(cfg, now=MOMENT)}


# ---------------------------------------------------------------------------
# The surface, and the module toggle
# ---------------------------------------------------------------------------


def test_the_verb_is_declared_landed_and_names_this_module():
    """The registry entry drives the conformance suite only once planned_in is gone."""
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
    """Both directions, because either alone passes over a toggle that is ignored."""
    entry = _entry()
    assert entry.available_to(profiles.resolve("full")), (
        "the backup module is in the full profile and the verb is not offered"
    )
    assert not entry.available_to(profiles.resolve("slim")), (
        "a slim install has no backup module, so this verb must not be offered"
    )


def test_queueing_needs_no_rclone_no_remote_and_no_volume(cfg, no_rclone, monkeypatch):
    """The handler files a job and resolves nothing, which is the whole split."""
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
    """Both directions of the flag, and the absence of --run, in one place."""

    class _Job:
        job_id = "job-one"

        def __init__(self, payload):
            self.payload = payload

    assert backup_cli.backup_argv(_Job({backup_cli.DRY_RUN: True})) == [
        "backup", "run", "--dry-run", "--job", "job-one",
    ]
    assert backup_cli.backup_argv(_Job({backup_cli.DRY_RUN: False})) == [
        "backup", "run", "--job", "job-one",
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
    """The key the handler freezes is the key the builder reads, driven end to end."""
    for argv, wanted in ((["backup", "run"], False), (["backup", "run", "--dry-run"], True)):
        code, envelope = _drive(argv)
        assert code == int(ExitCode.OK), envelope
        with jobs.open_store() as store:
            job = jobs.get(store, envelope["data"]["job_id"])
        assert "--library-emptied" not in backup_cli.backup_argv(job)
        assert job.payload == {
            backup_cli.DRY_RUN: wanted,
            backup_cli.FULL: False,
            backup_cli.CHECK: False,
            backup_cli.EMPTIED: False,
        }, (
            f"{argv} froze {job.payload}, so the resume would do different work "
            f"from the run it continues"
        )


def test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume(cfg):
    """R-1761's flag, through the real parser for the reason the test above
    gives, and a second ask with it told that the open job lacks it."""
    code, envelope = _drive(["backup", "run", "--dry-run", "--library-emptied"])
    assert code == int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert job.payload[backup_cli.EMPTIED] is True, job.payload
    assert backup_cli.backup_argv(job) == [
        "backup", "run", "--dry-run", "--library-emptied", "--job", job.job_id,
    ]

    code, envelope = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), envelope
    code, envelope = _drive(["backup", "run", "--library-emptied"])
    (twin,) = [w for w in envelope["warnings"] if w["code"] == backup_cli.ALREADY_QUEUED]
    assert "--library-emptied" in twin["message"], twin["message"]


# ---------------------------------------------------------------------------
# The age, which is the half of this unit that is not a shell
# ---------------------------------------------------------------------------


def test_a_run_that_succeeded_publishes_an_age_the_session_reads_back(cfg, rclone):
    """The unit's reason for existing, driven through the consumer."""
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
    """The direction that costs data, and the one a green suite would not have."""
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
    """The branch beside the two above, and the one the report has to distinguish."""
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
    """The drive the finding behind this unit records as never having been run."""
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
    """The companion drive, without which the guard above proves less than it looks."""
    report = backup_cli.perform_backup({}, now=MOMENT)

    assert report["ok"] is True, report
    assert _warnings_by_portion(report) == {"files": [], "database": []}, report
    assert [row["state"] for row in report["ages"]] == ["known", "known"], report


def test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run(
    cfg, rclone_that_cannot_list
):
    """A preview exists to find out whether the remote is reachable."""
    report = backup_cli.perform_backup({backup_cli.DRY_RUN: True}, now=MOMENT)

    assert report["dry_run"] is True and report["ok"] is True, report
    assert _warnings_by_portion(report)["files"] == [backup.ARCHIVE_LISTING_FAILED], report
    assert [row["state"] for row in report["ages"]] == [
        "never-recorded",
        "never-recorded",
    ], report


def test_a_failing_rehearsal_is_not_reported_as_a_passing_one(cfg):
    """The branch one over, which is where this defect class reproduced in U27."""
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            {backup_cli.DRY_RUN: True},
            runner=_answering(1, stderr="connection refused"),
            now=MOMENT,
        )
    assert excinfo.value.cause.reason == "backup-transfer-failed"


def test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran(cfg, rclone):
    """The state a library backed up without quitting rekordbox is genuinely in."""
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
    """The reporting half of the first-caller defect, driven rather than argued."""
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
    """The doctor check ``binary.rclone`` exists, so this must be a name not a trace."""
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
    """No single remedy exists, so the summary slug carries every reason as a step."""
    # Unmounted by moving the whole tree aside, so the engine produces both
    # refusals rather than this file assembling them.
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
    """``BackupRefused`` is not a ``CratekitError``, so escaping it means internal-error."""
    config.save(_without_destinations(cfg))
    config.reset_cache()

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, now=MOMENT)
    cause = excinfo.value.cause
    assert cause.reason == str(backup.Refusal.REMOTE_NOT_CONFIGURED), cause.to_json()
    assert cause.code is not ExitCode.INTERNAL, cause.to_json()
    assert cause.remediation.remedy is Remedy.RUN_SETUP, cause.to_json()


def test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing(cfg, rclone):
    """Reporting no age would say this library has never been backed up."""
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_bytes(b"{not json at all")

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.published_ages(cfg, now=MOMENT)
    cause = excinfo.value.cause
    assert cause.reason == "backup-facts-unreadable", cause.to_json()
    assert cause.remediation.remedy is Remedy.REPAIR_BACKUP_FACTS, cause.to_json()


def test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception(cfg):
    """Three remedies, and a permission is not a corruption."""
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
    """The other direction of ``refusal_for``, so it is not a function that always fires."""
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
    """Half a backup with a published age for the working half is not a success."""
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
    # Retryable, or the portion could never be resumed (R-380, R-390).
    assert refusal.cause.retryable is True


def test_an_outcome_with_no_portions_refuses_rather_than_raising():
    """``plan_backup`` cannot produce one, and the answer is still an answer."""
    refusal = backup_cli.refusal_for(backup.BackupOutcome(stamp="s", portions=()))
    assert refusal is not None and refusal.cause.reason == "backup-nothing-ran"


def test_a_supplied_configuration_is_used_rather_than_the_one_on_disk(cfg, rclone, tmp_path):
    """The frozen configuration the job driver's contract says a handler runs against."""
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
    """One writer of one fact, asserted against the source rather than argued."""
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


def test_the_transfer_failure_says_no_age_was_published(cfg, rclone):
    """The sentence, not only the slug, because the sentence is what a person acts on."""
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
    """The number R15's warning quotes, which round one found nothing asserted."""
    backup_cli.perform_backup({}, now=MOMENT)
    later = backup_cli.published_ages(cfg, now=MOMENT + timedelta(hours=1))
    assert [row["state"] for row in later] == ["known", "known"], later
    assert all(row["age_seconds"] == 3600.0 for row in later), later
    assert all(row["completed_at"] == MOMENT.isoformat() for row in later), later


def test_a_resume_reports_the_queued_job_rather_than_filing_a_second(cfg, rclone):
    """The ``--job`` branch, which round one found undriven."""
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
    """``BackupOutcome.ok``, which round one found nothing anywhere asserts as False."""
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
    """The narrowing, measured on both portions rather than asserted on one."""
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
    # The snapshot and the marker that says whose it is, which belongs to the
    # database portion because it describes the database in that dated folder.
    assert _labels(database) == [backup.SNAPSHOT_DATABASE, backup.SNAPSHOT_IDENTITY], (
        f"the database portion ran {_labels(database)}, not the snapshot and its marker"
    )


def test_no_portion_named_still_runs_the_whole_plan(cfg):
    """The default that keeps every caller older than the binding measuring the same thing."""
    whole = _answering(0)
    report = backup_cli.perform_backup({}, cfg=cfg, runner=whole, now=MOMENT)
    assert backup.SNAPSHOT_DATABASE in _labels(whole), _labels(whole)
    assert [entry["portion"] for entry in report["portions"]] == ["files", "database"]


def test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy(cfg, rclone):
    """THE HAZARD THIS FORECLOSES, and it is the reason this unit reversed a decision."""
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
    """R16: a condition found AFTER the work completed must not fail the item."""
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
    """KTD9 through the handler: the frozen destination, not the one on disk."""
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
    produced = backup_cli.handle(job, item, frozen)
    # R-349 reversed the "returns nothing" half of this test: the outcome record
    # is now the item's artifact. What stays is that it is the only one.
    assert produced == jobs.Produced(
        staged=produced.staged, final=backup_facts.outcome_path("J2", "files")
    ), produced
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
    """THE ZERO ITEM RULE, which is the hazard binding a worker would otherwise create."""
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
    """The items come from the enum, so the property queueing had before survives."""
    monkeypatch.setattr(Path, "is_dir", lambda self: False)
    code, envelope = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), envelope
    assert len(_item_states(envelope["data"]["job_id"])) == len(backup_facts.Portion)


def _share_warnings(envelope: dict) -> list[dict]:
    return [
        w for w in envelope.get("warnings", []) if w["code"] == backup.ANALYSIS_SHARE_ABSENT
    ]


def _outside(cfg, tmp_path) -> Path:
    """Save the acknowledged layout, the database off the library volume. Returns its home."""
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    outside = replace(
        cfg,
        library=replace(
            cfg.library,
            db_path=home / "master.db",
            db_outside_root_acknowledged_on="2026-09-11",
        ),
    )
    config.save(outside)
    config.reset_cache()
    (home / "master.db").write_bytes(b"database, generation one")
    return home


def test_an_outside_analysis_share_is_carried_through_the_verb(cfg, rclone, tmp_path):
    """R-338, through the dispatcher: the share reaches the one program that copies."""
    home = _outside(cfg, tmp_path)
    grid = home / "share" / "PIONEER" / "USBANLZ" / "8d2" / "key" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True)
    grid.write_bytes(b"PMAI")

    queued, resumed = _queued_and_resumed()
    assert _share_warnings(queued) == [], queued
    assert _share_warnings(resumed) == [], resumed
    synced = [
        line for line in rclone.read_text().splitlines()
        if line.startswith(f"sync {home / 'share'} ")
    ]
    assert len(synced) == 1, rclone.read_text()
    assert "/analysis-share/" in synced[0]
    assert grid.read_bytes() == b"PMAI"


def test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume(
    cfg, rclone, tmp_path
):
    """Through the dispatcher, because the item's own report reaches nobody."""
    home = _outside(cfg, tmp_path)

    queued, resumed = _queued_and_resumed()
    assert len(_share_warnings(queued)) == 1, queued
    said = _share_warnings(resumed)
    assert len(said) == 1, resumed
    assert str(home / "share") in said[0]["message"], said
    assert " sync " + str(home / "share") not in rclone.read_text()


def _identity_warnings(envelope: dict) -> list[dict]:
    return [
        w
        for w in envelope.get("warnings", [])
        if w["code"] == backup.SNAPSHOT_IDENTITY_NOT_WRITTEN
    ]


def test_a_library_whose_identity_cannot_be_a_marker_is_told_so(cfg, rclone):
    """At queue and at resume, for the reason the share warning above is."""
    # Not a missing identity, which cannot be saved: a value with a space in
    # it passes validation and cannot be a marker's filename.
    config.save(replace(cfg, library=replace(cfg.library, volume_id="not a plain name")))
    config.reset_cache()

    queued, resumed = _queued_and_resumed()
    assert len(_identity_warnings(queued)) == 1, queued
    assert len(_identity_warnings(resumed)) == 1, resumed


def test_a_contained_share_and_a_plain_identity_draw_neither_warning(cfg, rclone):
    """The companions, so neither warning raised unconditionally passes the drives above."""
    queued, resumed = _queued_and_resumed()
    for envelope in (queued, resumed):
        assert _share_warnings(envelope) == [], envelope
        assert _identity_warnings(envelope) == [], envelope


def test_a_queued_backup_runs_every_portion_through_the_real_resume(cfg, rclone):
    """R-198's whole claim, closed for this verb and driven end to end."""
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
    """R9 and R15 together: the engine publishes it, and the shell reports it."""
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
    """R11, and THE ROUTE IS THE PART THAT IS EASY TO GET WRONG."""
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
    """R13, driven through the dispatcher rather than at the work body."""
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code != int(ExitCode.OK), resumed
    assert set(_item_states(job_id).values()) == {"failed"}, _item_states(job_id)
    with jobs.open_store() as store:
        assert str(jobs.get(store, job_id).state) == "failed"


def test_the_configuration_the_worker_runs_against_is_the_frozen_one(cfg, rclone):
    """KTD9 end to end, and the drift the person is told about rather than silently given."""
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
    """R14, asked the way a person asks it rather than of the table."""
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
    """P3: the set is derived at run time, or it is a list in disguise."""

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
    """R16 through the HANDLER, which is the caller the guard is for."""
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
    # Returning at all is the claim: a read back would have raised. The
    # ``Produced`` is R-349's outcome record, asserted in its own tests.
    produced = backup_cli.handle(job, item, cfg)
    assert produced is not None and produced.staged.is_file(), (
        "the handler read the age back, so an unreadable fact file fails an item "
        "over a rehearsal that copied nothing and every resume repeats it"
    )


# ---------------------------------------------------------------------------
# U50 review round: what a second look, an old job and a broken fact file do
# ---------------------------------------------------------------------------


def test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice(
    cfg, rclone, monkeypatch
):
    """The check has to sit OUTSIDE the ``is_open`` branch, and this is why."""
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
    """THE UPGRADE HAZARD, and it is the reason this guard is not paranoia."""
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
    """The engine publishes THROUGH the fact file and can fail ON it."""
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


def test_the_ages_reported_are_the_ones_this_job_published(
    cfg, rclone, tmp_path, monkeypatch
):
    """The envelope describes THIS job, so it reads the job's own configuration."""
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    elsewhere = tmp_path / "another-library"
    (elsewhere / "Music").mkdir(parents=True)
    (elsewhere / "db").mkdir(parents=True)
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
    # The database moves with the root, since KTD21b refuses to save it outside.
    config.save(
        replace(
            cfg,
            library=replace(
                cfg.library, root=elsewhere, db_path=elsewhere / "db" / "master.db"
            ),
        )
    )
    config.reset_cache()
    assert config.load().library.root == elsewhere, (
        "the live configuration still names the original library, so the two "
        "readings cannot differ and this test would pass either way"
    )
    assert not backup_facts.path_for(config.load()).exists(), (
        "the relocated library already has a fact file, so a live read would "
        "find ages there and the test would not distinguish the two sources"
    )

    code, again = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), again
    reported = {entry["portion"]: entry for entry in again["data"]["ages"]}
    for portion in backup_facts.Portion:
        assert reported[str(portion)]["state"] == str(backup_facts.AgeState.KNOWN), (
            f"the {portion} age read back as {reported[str(portion)]['state']}, so "
            f"the envelope answered from the live library rather than the one this "
            f"job copied"
        )


# ---------------------------------------------------------------------------
# One run is one rotation slot, through the queue (R-222)
# ---------------------------------------------------------------------------


class _ArchiveRemote:
    """A runner that HOLDS the dated archive folders, the way a remote does.

    The stand-in program answers every listing with the same two names, so it
    cannot show a purge taking a folder an earlier attempt wrote. Here a mirror
    writes the folder its ``--backup-dir`` names, a listing reads the set back and
    a purge removes from it.
    """

    def __init__(self, *folders: str) -> None:
        self.folders = set(folders)
        self.fail_mirror = False

    def __call__(self, command: backup.Command) -> backup.CommandResult:
        if command.label == backup.MIRROR:
            archive = command.argv[command.argv.index("--backup-dir") + 1]
            self.folders.add(archive.rsplit("/", 1)[1])
            if self.fail_mirror:
                return backup.CommandResult(returncode=1, stderr="connection reset")
        if command.label == backup.PRUNE_ARCHIVE:
            return backup.CommandResult(
                returncode=0, stdout="".join(f"{name}/\n" for name in sorted(self.folders))
            )
        if command.label == backup.PRUNE_ARCHIVE_FOLDER:
            self.folders.discard(command.argv[-1].rsplit("/", 1)[1])
        return backup.CommandResult(returncode=0)


def _stepped_clock(monkeypatch, start: datetime) -> None:
    """Every reading of the engine's clock is an hour after the last."""

    class Clock(datetime):
        current = start

        @classmethod
        def now(cls, tz=None):
            cls.current += timedelta(hours=1)
            return cls.current

    monkeypatch.setattr(backup, "datetime", Clock)


def test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote(
    cfg, rclone, monkeypatch
):
    """R-222 by the route a person takes: queue, fail, ``jobs.retry``, resume."""
    _stepped_clock(monkeypatch, MOMENT)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=MOMENT - timedelta(days=1),
        destination=str(cfg.backup.dest),
    )
    remote = _ArchiveRemote("2026-08-01T000000Z")
    remote.fail_mirror = True
    monkeypatch.setattr(backup, "subprocess_runner", remote)

    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, failed = _drive(["backup", "run", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    first_attempt = remote.folders - {"2026-08-01T000000Z"}
    assert len(first_attempt) == 1, remote.folders

    remote.fail_mirror = False
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    assert first_attempt <= remote.folders, (
        f"the retry left {sorted(remote.folders)}, so it purged the failed "
        f"attempt's archive and the only copies of what that attempt overwrote"
    )
    assert len(remote.folders) == 2, (
        f"the retry left {sorted(remote.folders)}: two attempts in one folder means "
        f"the clock did not step, and the settled folder still present means the "
        f"rotation stopped"
    )
    assert "2026-08-01T000000Z" not in remote.folders


# ---------------------------------------------------------------------------
# Asking twice is one backup (R-223)
# ---------------------------------------------------------------------------


def _codes(envelope: dict) -> list[str]:
    return [warning["code"] for warning in envelope.get("warnings") or ()]


def _job_count() -> int:
    with jobs.open_store() as store:
        return len(jobs.list_jobs(store))


def test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second(cfg):
    """R-223's closing condition. The verb prints an identifier and appears to
    have done nothing, which is the shape that invites typing it again."""
    code, first = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), first
    assert backup_cli.ALREADY_QUEUED not in _codes(first), first

    code, second = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), second
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert _job_count() == 1
    assert _codes(second).count(backup_cli.ALREADY_QUEUED) == 1, second
    said = next(w for w in second["warnings"] if w["code"] == backup_cli.ALREADY_QUEUED)
    assert first["data"]["job_id"] in said["message"], said


def test_a_rehearsal_and_a_real_run_are_two_jobs(cfg):
    """A rehearsal copies nothing, so it cannot interleave with a transfer, and
    answering a request for a real backup with an open rehearsal would report a
    job that will never copy a byte as the backup the person asked for."""
    _, rehearsal = _drive(["backup", "run", "--dry-run"])
    _, real = _drive(["backup", "run"])
    assert real["data"]["job_id"] != rehearsal["data"]["job_id"]
    assert backup_cli.ALREADY_QUEUED not in _codes(real), real
    assert _job_count() == 2


def test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job(cfg):
    """The open job is read by its FROZEN destinations. Another mirror and another
    archive cannot interleave with this one, and a person who reconfigured on
    purpose is owed the job they asked for."""
    _, first = _drive(["backup", "run"])
    config.save(
        replace(
            cfg,
            backup=replace(
                cfg.backup, dest="remote:second-mirror", archive_root="remote:second-archive"
            ),
        )
    )
    config.reset_cache()
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] != first["data"]["job_id"]
    assert _job_count() == 2


@pytest.mark.parametrize("shared", ["dest", "archive_root"])
def test_either_shared_destination_is_the_same_backup(cfg, shared):
    """Two syncs into one mirror interleave, and two rotations over one archive
    root prune each other, so sharing EITHER is enough."""
    _, first = _drive(["backup", "run"])
    moved = {"dest": "remote:second-mirror", "archive_root": "remote:second-archive"}
    del moved[shared]
    config.save(replace(cfg, backup=replace(cfg.backup, **moved)))
    config.reset_cache()
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert _job_count() == 1
    # The job's frozen destinations are named, not today's.
    said = next(w for w in second["warnings"] if w["code"] == backup_cli.ALREADY_QUEUED)
    assert "remote:mirror " in said["message"], said
    assert "remote:mirror-archive" in said["message"], said
    assert "remote:second-" not in said["message"], said


@pytest.mark.parametrize(
    "ending", [jobs.JobState.SUCCEEDED, jobs.JobState.FAILED, jobs.JobState.CANCELLED]
)
def test_a_backup_that_is_over_does_not_stand_in_for_a_new_one(cfg, ending):
    _, first = _drive(["backup", "run"])
    with jobs.open_store() as store:
        jobs.transition(store, first["data"]["job_id"], jobs.JobState.RUNNING)
        jobs.transition(store, first["data"]["job_id"], ending)
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] != first["data"]["job_id"]
    assert backup_cli.ALREADY_QUEUED not in _codes(second), second


def test_a_job_that_can_never_run_does_not_stand_in_for_a_backup(cfg):
    """The itemless job a previous build queued refuses when driven, so reporting
    it would answer a request for a backup with one that cannot happen."""
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key="backup.run",
            payload=backup_cli.frozen_payload(False),
            cfg=cfg,
        )
    _, queued = _drive(["backup", "run"])
    assert backup_cli.ALREADY_QUEUED not in _codes(queued), queued
    assert _job_count() == 2


def test_another_verb_s_open_job_is_not_a_backup(cfg):
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key="master.run",
            payload=backup_cli.frozen_payload(False),
            item_ids=backup_cli.backup_items(),
            cfg=cfg,
        )
    _, queued = _drive(["backup", "run"])
    assert backup_cli.ALREADY_QUEUED not in _codes(queued), queued
    assert _job_count() == 2


def test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere(
    cfg, monkeypatch
):
    """Could not read is not the same as somewhere else (METHOD's first pattern)."""
    _, first = _drive(["backup", "run"])

    def unreadable(job):
        raise ValueError("a configuration this build cannot rebuild")

    monkeypatch.setattr(jobs, "frozen_config", unreadable)
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert _job_count() == 1
    said = next(w for w in second["warnings"] if w["code"] == backup_cli.ALREADY_QUEUED)
    assert "could not be rebuilt" in said["message"], said
    assert "remote:mirror" not in said["message"], (
        f"the warning names a destination nobody read: {said}"
    )


def test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup(
    cfg, monkeypatch
):
    """Only the configuration's own failures mean "could not read". Anything else
    is a defect in this program, and reporting it as an open backup with exit 0
    is how it would stay unfound."""
    _drive(["backup", "run"])

    def broken(job):
        raise AttributeError("a defect, not an unreadable configuration")

    monkeypatch.setattr(jobs, "frozen_config", broken)
    code, second = _drive(["backup", "run"])
    assert code != int(ExitCode.OK), second
    assert _job_count() == 1


def test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger(cfg):
    """The rehearsal flag is compared the way the work body reads it. A job queued
    by a build that froze one more key is still the same backup."""
    with jobs.open_store() as store:
        older = jobs.enqueue(
            store,
            handler_key="backup.run",
            payload={**backup_cli.frozen_payload(False), "a_later_key": "anything"},
            item_ids=backup_cli.backup_items(),
            cfg=cfg,
        )
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] == older.job_id, second
    assert _job_count() == 1


def test_another_library_s_open_backup_is_not_this_library_s(cfg):
    """The envelope says "this is your backup", and a job copying another library
    is not, whatever destination the two were pointed at."""
    with jobs.open_store() as store:
        jobs.enqueue(
            store,
            handler_key="backup.run",
            payload=backup_cli.frozen_payload(False),
            item_ids=backup_cli.backup_items(),
            cfg=replace(cfg, library=replace(cfg.library, volume_id="0A0B-0C0D")),
        )
    _, queued = _drive(["backup", "run"])
    assert backup_cli.ALREADY_QUEUED not in _codes(queued), queued
    assert _job_count() == 2


def test_the_warnings_beside_a_reported_job_describe_that_job(cfg, tmp_path):
    """The open job was frozen with its analysis share off the volume, and the
    configuration on disk has since moved it back. The job reported will still run
    under the first, so that is the one the envelope describes."""
    home = tmp_path / "home" / "rekordbox"
    home.mkdir(parents=True)
    config.save(
        replace(
            cfg,
            library=replace(
                cfg.library,
                db_path=home / "master.db",
                db_outside_root_acknowledged_on="2026-09-11",
            ),
        )
    )
    config.reset_cache()
    _, first = _drive(["backup", "run"])
    assert len(_share_warnings(first)) == 1, first

    config.save(cfg)
    config.reset_cache()
    _, second = _drive(["backup", "run"])
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert len(_share_warnings(second)) == 1, second


# ---------------------------------------------------------------------------
# R-221: the queued path says which kind of run it was
# ---------------------------------------------------------------------------


def _rehearsal_said(envelope: dict) -> list[dict]:
    return [w for w in envelope.get("warnings") or () if w["code"] == backup_cli.REHEARSAL]


def test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied(cfg, rclone):
    """R-221's named cost, driven through the dispatcher on both of its exits."""
    code, queued = _drive(["backup", "run", "--dry-run"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]

    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == "succeeded", resumed["data"]
    assert set(_item_states(job_id).values()) == {"done"}, _item_states(job_id)

    assert resumed["data"]["progress"]["dry_run"] is True, resumed["data"]
    said = _rehearsal_said(resumed)
    assert len(said) == 1, resumed
    assert "copies nothing" in said[0]["message"], said


def test_the_new_key_rides_under_progress_and_the_surface_gains_nothing_else(
    cfg, rclone
):
    """THE DECLARED SURFACE, ASKED OF BOTH ENVELOPES AND NOT ONLY THE FIRST."""
    _, queued = _drive(["backup", "run", "--dry-run"])
    assert output.envelope_problems(queued) == [], queued
    assert "dry_run" not in queued["data"], (
        "the detail sat beside the declared fields, so a consumer generated from "
        "the committed schema rejects this envelope"
    )

    _, resumed = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert output.envelope_problems(resumed) == ["undeclared field 'ages'"], (
        "the resume envelope's undeclared fields moved. `ages` is the one this "
        "verb already shipped; anything else joining it is this branch's"
    )


def test_a_queued_real_backup_carries_no_rehearsal_word(cfg, rclone):
    """The companion, so a warning raised unconditionally cannot pass the drive
    above. A real run copied something and published an age for it, and telling
    a person it copied nothing is the same defect pointing the other way."""
    code, queued = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), queued
    assert _rehearsal_said(queued) == [], queued
    assert queued["data"]["progress"]["dry_run"] is False, queued["data"]

    code, resumed = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), resumed
    assert _rehearsal_said(resumed) == [], resumed
    assert resumed["data"]["progress"]["dry_run"] is False, resumed["data"]


def test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported(cfg):
    """Every branch that hands back an identifier says what that identifier will
    do, because a person who queues a rehearsal and never resumes it by hand
    would otherwise learn what it was only from the run that copied nothing."""
    code, first = _drive(["backup", "run", "--dry-run"])
    assert code == int(ExitCode.OK), first
    assert len(_rehearsal_said(first)) == 1, first

    code, second = _drive(["backup", "run", "--dry-run"])
    assert code == int(ExitCode.OK), second
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert backup_cli.ALREADY_QUEUED in _codes(second), second
    assert len(_rehearsal_said(second)) == 1, second
    assert second["data"]["progress"]["dry_run"] is True, second["data"]


def test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing(cfg):
    """The companion for the twin branch, WRITTEN BECAUSE THE MUTATION TABLE
    found nothing holding it. Making that branch carry the word unconditionally
    killed zero tests: the existing twin cases assert the already-queued code is
    present, and the rehearsal twin case asserts this one is, and neither asks
    what a real twin is NOT told. A person asking twice for a real backup would
    have been told the job they are being handed copies nothing."""
    code, first = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), first

    code, second = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), second
    assert second["data"]["job_id"] == first["data"]["job_id"], second
    assert backup_cli.ALREADY_QUEUED in _codes(second), second
    assert _rehearsal_said(second) == [], second
    assert second["data"]["progress"]["dry_run"] is False, second["data"]


def test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so(
    cfg, rclone
):
    """The exact state the entry describes, built rather than asserted: a real
    backup first, so the fact file holds true ages, then a rehearsal over it.
    """
    _, real = _drive(["backup", "run"])
    code, _ = _drive(["backup", "run", "--job", real["data"]["job_id"]])
    assert code == int(ExitCode.OK)
    published = {name: entry.completed_at for name, entry in _ages(cfg).items()}
    assert all(stamp is not None for stamp in published.values()), published

    _, rehearsal = _drive(["backup", "run", "--dry-run"])
    code, resumed = _drive(["backup", "run", "--job", rehearsal["data"]["job_id"]])
    assert code == int(ExitCode.OK), resumed

    assert {name: entry.completed_at for name, entry in _ages(cfg).items()} == published, (
        "the rehearsal published an age, which is a different defect from the one "
        "this test is about"
    )
    reported = {row["portion"]: row["state"] for row in resumed["data"]["ages"]}
    assert set(reported.values()) == {str(backup_facts.AgeState.KNOWN)}, reported
    assert len(_rehearsal_said(resumed)) == 1, (
        "the ages are the previous run's and true, and nothing said this run "
        "copied nothing, which is a rehearsal reading as a backup"
    )


def test_the_flag_on_the_envelope_is_the_jobs_own_and_not_the_command_lines(cfg, rclone):
    """THE SOURCE IS THE FROZEN PAYLOAD, which is what the worker reads."""
    _, queued = _drive(["backup", "run"])
    code, resumed = _drive(
        ["backup", "run", "--dry-run", "--job", queued["data"]["job_id"]]
    )
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["dry_run"] is False, resumed["data"]
    assert _rehearsal_said(resumed) == [], resumed


def _assert_extended_not_rebuilt(rehearsed: dict, control: dict) -> None:
    """The rehearsal's refusal is the real run's, field for field, plus one step."""
    for field in ("reason", "code", "retryable", "scope", "origin"):
        assert rehearsed[field] == control[field], (
            f"{field} moved between a rehearsal's refusal and the same failure's "
            f"without the flag, so the cause was rebuilt rather than extended"
        )
    # Only ``job_id`` legitimately differs between the two jobs' details.
    assert {k: v for k, v in rehearsed["detail"].items() if k != "job_id"} == {
        k: v for k, v in control["detail"].items() if k != "job_id"
    }, "detail moved, so the cause was rebuilt rather than extended"
    assert rehearsed["remediation"]["remedy"] == control["remediation"]["remedy"], (
        "the remedy token moved, and the rehearsal is context rather than a "
        "competing instruction about what to do next"
    )
    steps = rehearsed["remediation"]["steps"]
    kept = control["remediation"]["steps"]
    assert steps[: len(kept)] == kept, (
        "the rehearsal step replaced the failure's own steps instead of joining them"
    )
    assert len(steps) == len(kept) + 1


def test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal(cfg, monkeypatch):
    """THE SECOND EXIT, and the one an advisory on the envelope never reaches."""
    monkeypatch.setattr(backup, "subprocess_runner", _answering(1, stderr="refused"))
    _, queued = _drive(["backup", "run", "--dry-run"])
    code, refused = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    _, control_job = _drive(["backup", "run"])
    _, control = _drive(["backup", "run", "--job", control_job["data"]["job_id"]])

    assert code != int(ExitCode.OK), refused
    cause = refused["cause"]
    steps = cause["remediation"]["steps"]
    assert any("copies nothing" in step for step in steps), refused
    assert cause["reason"] == "no-evidence", cause
    _assert_extended_not_rebuilt(cause, control["cause"])


def test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal(cfg, monkeypatch):
    """THE OTHER REFUSING EXIT, which is a different line from the one above."""
    monkeypatch.setattr(
        backup, "subprocess_runner", _failing_on(backup.SNAPSHOT_DATABASE)
    )
    _, queued = _drive(["backup", "run", "--dry-run"])
    job_id = queued["data"]["job_id"]

    code, refused = _drive(["backup", "run", "--job", job_id])
    _, control_job = _drive(["backup", "run"])
    _, control = _drive(["backup", "run", "--job", control_job["data"]["job_id"]])

    assert code != int(ExitCode.OK), refused
    assert _item_states(job_id) == {"files": "done", "database": "failed"}, (
        "both items settled the same way, so this drove the exit the test above "
        "already covers rather than the one it is for"
    )
    steps = refused["cause"]["remediation"]["steps"]
    assert any("copies nothing" in step for step in steps), refused
    # A transfer exit is retryable, so the job cause is the engine's transient
    # verdict with the portion's refusal nested inside it (R-380, R-390).
    assert refused["cause"]["reason"] == "unavailable-transient", refused
    assert refused["cause"]["retryable"] is True, refused
    assert refused["cause"]["inner"]["reason"] == "backup-transfer-failed", refused
    _assert_extended_not_rebuilt(refused["cause"], control["cause"])


def test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added(
    cfg, monkeypatch
):
    """THE HOP THAT WORDS THE EXIT MUST NOT CHANGE WHAT KIND OF EXIT IT IS (R-290)."""
    from cratekit.cli import handlers
    from cratekit.core.cause import Outcome, refuse

    def parks(job, item, cfg):
        raise jobs.Parked(
            refuse(
                "provider-blocked",
                "the provider refused this client",
                remedy=Remedy.RETRY_LATER,
                origin=("test",),
            ).cause
        )

    _, queued = _drive(["backup", "run", "--dry-run"])
    job_id = queued["data"]["job_id"]
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)

    code, refused = _drive(["backup", "run", "--job", job_id])

    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED, refused
    assert refused["outcome"] == str(Outcome.BLOCKED), refused
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "provider-blocked", refused
    steps = refused["cause"]["remediation"]["steps"]
    assert any("copies nothing" in step for step in steps), refused


def test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was(
    cfg, rclone
):
    """THE THIRD REFUSING EXIT, which the first cut of this unit left uncovered."""
    _, queued = _drive(["backup", "run", "--dry-run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert set(_item_states(job_id).values()) == {"done"}, _item_states(job_id)

    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_bytes(b"{not json at all")
    code, refused = _drive(["backup", "run", "--job", job_id])

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "backup-facts-unreadable", refused
    steps = refused["cause"]["remediation"]["steps"]
    assert any("copies nothing" in step for step in steps), refused


def test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step(cfg, rclone):
    """The companion for the third exit, so the step cannot ride every refusal."""
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_bytes(b"{not json at all")
    code, refused = _drive(["backup", "run", "--job", job_id])

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "backup-facts-unreadable", refused
    steps = refused["cause"]["remediation"]["steps"]
    assert not any("copies nothing" in step for step in steps), refused


def test_a_refusal_this_verb_re_raises_is_never_its_own_cause(cfg):
    """THE DEFECT THE FIRST CUT SHIPPED, guarded at the helper that raises."""
    with jobs.open_store() as store:
        real = jobs.enqueue(
            store,
            handler_key="backup.run",
            payload=backup_cli.frozen_payload(False),
            item_ids=backup_cli.backup_items(),
            cfg=cfg,
        )
        rehearsal = jobs.enqueue(
            store,
            handler_key="backup.run",
            payload=backup_cli.frozen_payload(True),
            item_ids=backup_cli.backup_items(),
            cfg=cfg,
        )

    for job, extended in ((real, False), (rehearsal, True)):
        original = CratekitError(
            Cause(
                reason="backup-transfer-failed",
                message="a transfer came back non zero",
                remediation=Remediation(remedy=Remedy.RETRY_LATER),
                origin=("backup", "cli"),
            )
        )
        try:
            backup_cli._raise_refusal(original, job)
        except CratekitError as raised:
            assert raised.__cause__ is not raised, (
                "the refusal is its own cause, so the declared chain ends here "
                "and everything under it stops being classified"
            )
            assert (raised is not original) is extended, (
                "the extending branch and the pass-through branch answered the "
                "same way, so one of them is not doing its job"
            )
        else:  # pragma: no cover - the helper's whole contract is to raise
            pytest.fail("_refuse returned instead of raising")


def test_a_real_backup_that_ended_badly_gains_no_rehearsal_step(cfg, monkeypatch):
    """The companion for the second exit. A failed real run attempted transfers,
    and telling that person nothing was copied is false in the direction that
    stops them looking for the half that was."""
    monkeypatch.setattr(backup, "subprocess_runner", _answering(1, stderr="refused"))
    _, queued = _drive(["backup", "run"])
    code, refused = _drive(["backup", "run", "--job", queued["data"]["job_id"]])

    assert code != int(ExitCode.OK), refused
    steps = refused["cause"]["remediation"]["steps"]
    assert not any("copies nothing" in step for step in steps), refused


def test_the_outcome_itself_records_which_kind_of_run_it_was(cfg, rclone):
    """ONE FILE OVER, at the engine, which is where the two runs first became
    indistinguishable. ``BackupOutcome`` carried a stamp and portions and no word
    about the run, so every renderer of one had to be handed the flag separately
    and the queued renderer was not. The value is read off the outcome the engine
    returned rather than off the argument it was called with, because the engine
    couples ``dry_run`` to publishing and the outcome is meant to record the run
    that happened."""
    plan = backup.plan_backup(cfg, now=MOMENT)
    rehearsed = backup.run_backup(
        cfg, plan, runner=_answering(0), now=MOMENT, dry_run=True
    )
    performed = backup.run_backup(
        cfg, plan, runner=_answering(0), now=MOMENT, dry_run=False
    )

    assert rehearsed.dry_run is True and performed.dry_run is False
    assert backup.outcome_payload(rehearsed)["dry_run"] is True
    assert backup.outcome_payload(performed)["dry_run"] is False


# ---------------------------------------------------------------------------
# R-349: what each backup item ran reaches the job record, on both channels
# ---------------------------------------------------------------------------


def _shown_outcomes(job_id: str) -> dict | None:
    """What ``crate job show`` says each item ran, through the real dispatcher."""
    code, shown = _drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), shown
    return shown["data"]["progress"].get(backup_facts.OUTCOMES_FIELD)


def _argv_lines(outcome: dict) -> list[str]:
    """Every command one item's outcome names, one argv per line."""
    return [
        " ".join(command["argv"])
        for portion in outcome["portions"]
        for command in portion["commands"]
    ]


def test_a_queued_backup_names_every_command_it_ran_in_job_show(cfg, rclone):
    """R-349's first scenario: the item is DONE and ``job show`` names its argv."""
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    assert _item_states(job_id) == {"files": "done", "database": "done"}

    shown = _shown_outcomes(job_id)
    assert shown is not None and set(shown) == {"files", "database"}, shown
    recorded = [line for item in shown.values() for line in _argv_lines(item)]
    invoked = rclone.read_text().splitlines()
    assert sorted(" ".join(line.split()[1:]) for line in recorded) == sorted(invoked), (
        "job show does not name the commands rclone actually ran"
    )
    assert all(
        command["returncode"] == 0
        for item in shown.values()
        for portion in item["portions"]
        for command in portion["commands"]
    )
    assert resumed["data"]["progress"][backup_cli.OUTCOMES] == shown, (
        "the --job envelope and job show describe the same items differently"
    )


def test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one(cfg, rclone):
    """R-349's second scenario: a dry run is persisted and flagged ``dry_run``."""
    _, queued = _drive(["backup", "run", "--dry-run"])
    job_id = queued["data"]["job_id"]
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed

    shown = _shown_outcomes(job_id)
    assert shown is not None and set(shown) == {"files", "database"}, shown
    for item in shown.values():
        assert item["dry_run"] is True, item
    assert any("--dry-run" in line for line in _argv_lines(shown["files"])), (
        "the record names the real transfer rather than the neutralized one the "
        "rehearsal ran"
    )


def test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv(
    cfg, rclone, monkeypatch
):
    """R-349's third scenario, the one the residual was filed for."""
    monkeypatch.setattr(backup, "subprocess_runner", _failing_on(backup.SNAPSHOT_DATABASE))
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    code, failed = _drive(["backup", "run", "--job", job_id])
    assert code != int(ExitCode.OK), failed
    assert _item_states(job_id) == {"files": "done", "database": "failed"}
    with jobs.open_store() as store:
        database = next(i for i in jobs.items(store, job_id) if i.item_id == "database")
    assert database.cause is not None and database.cause.reason == "backup-transfer-failed"
    assert _ages(cfg)["database"].state is backup_facts.AgeState.NEVER_RECORDED

    shown = _shown_outcomes(job_id)
    assert shown is not None and "database" in shown, shown
    commands = [
        command
        for portion in shown["database"]["portions"]
        for command in portion["commands"]
    ]
    failing = [command for command in commands if command["returncode"] != 0]
    assert [command["label"] for command in failing] == [backup.SNAPSHOT_DATABASE], commands
    assert "remote:database-snapshots" in " ".join(failing[0]["argv"]), failing


def test_a_job_of_another_verb_grows_no_outcomes_field(cfg):
    """R-349's fourth scenario: the field is backup's, not every job's."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="tag.retag", payload={}, cfg=cfg, item_ids=("one",)
        )
    code, shown = _drive(["job", "show", job.job_id])
    assert code == int(ExitCode.OK), shown
    assert backup_facts.OUTCOMES_FIELD not in shown["data"]["progress"], shown


def test_a_failed_backup_item_is_re_armed_and_its_record_replaced(
    cfg, rclone, monkeypatch
):
    """R-349's fifth scenario: the failure channel never completes the item."""
    monkeypatch.setattr(backup, "subprocess_runner", _failing_on(backup.SNAPSHOT_DATABASE))
    _, queued = _drive(["backup", "run"])
    job_id = queued["data"]["job_id"]
    _drive(["backup", "run", "--job", job_id])

    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    assert _item_states(job_id)["database"] == "pending", _item_states(job_id)

    monkeypatch.setattr(backup, "subprocess_runner", _answering(0))
    code, resumed = _drive(["backup", "run", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    shown = _shown_outcomes(job_id)
    assert all(
        command["returncode"] == 0
        for portion in shown["database"]["portions"]
        for command in portion["commands"]
    ), shown["database"]
    assert not list(backup_facts.outcome_path(job_id, "database").parent.glob("*.staged"))


def test_the_outcome_record_is_private_under_a_permissive_umask(cfg, rclone):
    """P1 on the new directory, WALKED rather than listed (P3)."""
    import os
    import stat

    def mirror_fails(command):
        if command.label == backup.MIRROR:
            return backup.CommandResult(returncode=1, stderr="connection refused")
        return backup.CommandResult(returncode=0)

    previous = os.umask(0)
    try:
        _, queued = _drive(["backup", "run"])
        job_id = queued["data"]["job_id"]
        backup.subprocess_runner, saved = mirror_fails, backup.subprocess_runner
        try:
            _drive(["backup", "run", "--job", job_id])
        finally:
            backup.subprocess_runner = saved
    finally:
        os.umask(previous)

    root = config.state_path(backup_facts.OUTCOMES_KEY)
    found = [root, *root.rglob("*")]
    assert any(p.is_file() and p.stem == "files" for p in found), found
    assert any(p.is_file() and p.stem == "database" for p in found), found
    for path in found:
        mode = stat.S_IMODE(path.stat().st_mode)
        wanted = 0o700 if path.is_dir() else 0o600
        assert mode == wanted, f"{path} is {oct(mode)}, wanted {oct(wanted)}"


def test_a_record_that_cannot_be_written_does_not_replace_the_transfer_failure(
    cfg, monkeypatch
):
    """The failure channel's own failure keeps the refusal it was recording."""

    def cannot_write(*_args, **_kwargs):
        raise PermissionError("the outcome directory is read only")

    monkeypatch.setattr(backup_facts, "write_outcome", cannot_write)
    with pytest.raises(CratekitError) as caught:
        backup_cli.perform_backup(
            {},
            portion=backup_facts.Portion.DATABASE,
            cfg=cfg,
            runner=_failing_on(backup.SNAPSHOT_DATABASE),
            read_back=False,
            outcome_to=("J9", "database"),
        )
    assert caught.value.cause.reason == "backup-transfer-failed"
    assert any("could not be written" in step for step in caught.value.cause.remediation.steps)


def test_every_command_the_engine_ran_is_paired_with_its_own_return_code(cfg, rclone):
    """The engine half: ``commands`` and ``results`` are the same runner calls."""

    def listing_fails(command):
        if " lsf " in f" {' '.join(command.argv)} ":
            return backup.CommandResult(returncode=3)
        return backup.CommandResult(returncode=0)

    report = backup_cli.perform_backup(
        {}, portion=backup_facts.Portion.FILES, cfg=cfg, runner=listing_fails, read_back=False
    )
    commands = report["portions"][0]["commands"]
    assert [c["returncode"] for c in commands if "lsf" in c["argv"]] == [3], commands
    assert all(c["returncode"] == 0 for c in commands if "lsf" not in c["argv"]), commands


def _claimed(job_id: str, item_id: str) -> tuple[jobs.Job, jobs.Item]:
    """A running job and one claimed item, built by hand for the handler seam."""
    job = jobs.Job(
        job_id=job_id,
        handler_key="backup.run",
        payload={},
        config_fingerprint="",
        config_toml="",
        library_id="",
        state=jobs.JobState.RUNNING,
        created=MOMENT.isoformat(),
        updated=MOMENT.isoformat(),
    )
    return job, jobs.Item(
        job_id=job_id, item_id=item_id, ordinal=0, state=jobs.ItemState.CLAIMED
    )


def test_an_outcome_directory_that_cannot_be_listed_is_not_read_as_nothing(cfg):
    """R-349 review: ``glob`` swallows a permission error, ``iterdir`` does not."""
    backup_facts.write_outcome("J10", "files", {"portions": []})
    directory = backup_facts.outcome_path("J10", "files").parent
    directory.chmod(0o000)
    try:
        found = backup_facts.read_outcomes("J10")
    finally:
        directory.chmod(0o700)
    assert found is not None and backup_facts.UNLISTABLE in found, found


def test_a_retry_that_fails_another_way_does_not_show_the_last_attempt_s_commands(
    cfg, monkeypatch
):
    """R-349 review: the record on disk is only ever the current attempt's."""
    backup_facts.write_outcome("J11", "database", {"portions": [{"commands": ["old"]}]})

    def runner_breaks(command):
        raise RuntimeError("the runner itself fell over")

    monkeypatch.setattr(backup, "subprocess_runner", runner_breaks)
    job, item = _claimed("J11", "database")
    with pytest.raises(RuntimeError):
        backup_cli.handle(job, item, cfg)
    assert not backup_facts.outcome_path("J11", "database").exists(), (
        "the previous attempt's failed commands still describe an attempt that "
        "failed for a different reason"
    )


def test_a_record_that_cannot_be_staged_does_not_fail_a_completed_backup(
    cfg, monkeypatch
):
    """R-349 review: after the transfer, a record write error completes the item."""
    monkeypatch.setattr(backup, "subprocess_runner", _answering(0))

    real = config.atomic_write_bytes

    def cannot_stage(payload, path, **kwargs):
        # Only the staged record: the age publish shares this writer, and
        # failing it would be a different condition from the one under test.
        if path.name.endswith(".staged"):
            raise PermissionError("the outcome directory is read only")
        return real(payload, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", cannot_stage)
    job, item = _claimed("J12", "files")
    assert backup_cli.handle(job, item, cfg) is None


def test_a_record_that_cannot_be_parsed_is_reported_rather_than_skipped(cfg):
    """Skipping it would show the other item alone, as though this one never ran."""
    backup_facts.write_outcome("J13", "files", {"portions": []})
    backup_facts.outcome_path("J13", "database").write_text("{ not json")
    found = backup_facts.read_outcomes("J13")
    assert found is not None and set(found) == {"files", "database"}, found
    assert "unreadable" in found["database"], found
