"""U27: the restore verbs, and the ONE session spanning both halves of a restore; taking the
lock twice in one process raises, so one acquisition is measurable (D1)."""

from __future__ import annotations

import io
import json
import shutil
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import exit_codes as reservations
from cratekit.cli import registry
from cratekit.core import config, jobs, preflight, processes, rb_writer, restore, session, snapshot
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.tools import backup
from cratekit.session import restore_cli
from tests import test_restore as restore_suite
from tests.test_restore import (
    _lock_taken_in_another_process,
    _raised,
    _refusal,
    acknowledge,
    completed_session,
    gate_seams,
)
from tests.test_restore import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_restore import acked as acked  # noqa: PLC0414 - fixture
from tests.test_restore import record as record  # noqa: PLC0414 - fixture

#: The configured library fixture, assigned so a test parameter cannot shadow an import.
cfg = restore_suite.cfg

#: The confirmation gate's declared name, spelled once.
CONFIRM = "restore.run.confirm"


@pytest.fixture
def installed(cfg, monkeypatch):
    """The same library, with the two PLATFORM seams answered for this machine."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    return cfg


@pytest.fixture
def remote_log(installed, monkeypatch) -> Path:
    """The installed library acknowledged, with the fake rclone's invocation log."""
    acknowledge(installed)
    return _fake_rclone(installed, monkeypatch)


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Run the REAL dispatcher and return the status with the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _answer(run_id: str, option: str) -> None:
    """R34's second act: the decision, recorded against the run, with its actor."""
    code, envelope = _drive(["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def _two_acts(argv: list[str], option: str = "restore") -> tuple[int, dict, dict]:
    """Drive ARGV, answer its gate with OPTION, and drive it again under the run."""
    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _answer(refused["run_id"], option)
    code, envelope = _drive(["--run", refused["run_id"], *argv])
    return code, refused, envelope


def _refused_as(code: int, envelope: dict, reason: str, exit_code=ExitCode.PRECONDITION):
    """The run was refused with ``exit_code``, naming ``reason``; its envelope."""
    assert code == int(exit_code), envelope
    assert envelope["cause"]["reason"] == reason, envelope
    return envelope


def _offered_digest(refused: dict) -> str:
    """The digest the run RECORDED as offered, read off the run rather than the message."""
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
    """Put a stand-in for rclone on the ONE seam the product ships for it."""
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
    """Say what the fake remote lists from now on. Callable between two acts."""
    home = Path(config.installation_state_dir())
    (home / REMOTE_SNAPSHOTS).write_text("".join(f"{name}/\n" for name in snapshots))
    if marker is OWN:
        marker = cfg_value.library.volume_id
    name = backup.identity_marker(marker) if marker is not None else None
    (home / REMOTE_MARKERS).write_text(f"{name}\n" if name else "")


def _one_session(cfg_value, runner, **overrides):
    """Both halves under one session, pulling ``STAMP`` with no rekordbox running."""
    arguments = {"session_id": None, "from_backup": True, "snapshot": STAMP, **overrides}
    return restore_cli.restore_under_one_session(
        cfg_value, runner=runner, process_lister=lambda: (), **arguments, **gate_seams(cfg_value)
    )


def _failing(command):
    """A remote that lists ``STAMP`` and refuses every transfer."""
    if "lsf" in command.argv:
        return backup.CommandResult(returncode=0, stdout=f"{STAMP}/\n")
    return backup.CommandResult(returncode=1, stdout="", stderr="connection refused")


def _outside(cfg_value, home: Path, held: bytes | None, on: str = "2026-09-20"):
    """The acknowledged layout with the database in ``home``, outside the root."""
    home.mkdir(parents=True)
    if held is not None:
        (home / "master.db").write_bytes(held)
    library = replace(
        cfg_value.library, db_path=home / "master.db", db_outside_root_acknowledged_on=on
    )
    return replace(cfg_value, library=library)


# The one session spanning both halves. This is the unit.


def test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock(
    cfg, tmp_path, acked, record
):
    """The wiring call U32 proved at the seam and could not make."""
    (tmp_path / "recovered").mkdir()
    observed: list[int] = []
    labels: list[str] = []

    def runner(command):
        labels.append(command.label)
        observed.append(_lock_taken_in_another_process(session.lock_path(cfg)))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    report = _one_session(
        cfg, runner, session_id=record.session_id, target=tmp_path / "recovered"
    )
    assert backup.RESTORE_DATABASE in labels, "the off-machine half never ran"
    assert observed and all(code != 0 for code in observed), (
        "a second process took the lock while the mirror was pulled: not one acquisition"
    )
    assert report.outcome is not None and report.outcome.performed, "the capture half never ran"
    assert report.pulled, "the report does not name the transfers the mirror half made"


def test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened(
    cfg, tmp_path, acked
):
    """The half that ran is named, and the half that did not is ``None``."""
    (tmp_path / "recovered").mkdir()
    database = config.state_path("rekordbox_db", cfg).name
    restored = tuple(
        sidecar.suffix
        for sidecar in config.state_file("rekordbox_db").sidecars
        if sidecar.restored
    )
    listing = "".join([database + "\n", *(database + suffix + "\n" for suffix in restored)])
    report = _one_session(
        cfg,
        lambda command: backup.CommandResult(
            returncode=0,
            stdout=listing if command.label == backup.LIST_SNAPSHOT_CONTENTS else "",
        ),
        target=tmp_path / "recovered",
    )

    # From the inventory and the listing, never the report: the database plus each sidecar.
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
    installed, tmp_path, acked
):
    """KTD25 at the boundary this unit created."""
    cause = _refusal(
        restore_cli.restore_under_one_session,
        _without_remote(installed),
        session_id=None,
        from_backup=True,
        target=tmp_path,
        **gate_seams(installed),
    )
    assert cause.reason == str(backup.Refusal.REMOTE_NOT_CONFIGURED)
    assert cause.code is not ExitCode.INTERNAL
    assert cause.remediation.remedy or cause.remediation.steps, (
        "the refusal reached a person with nothing to do about it"
    )


def _without_remote(cfg_value):
    """The same configuration with the off-machine destinations removed."""
    return replace(
        cfg_value,
        backup=replace(
            cfg_value.backup, remote="", dest="", archive_root="", db_dest_root=""
        ),
    )


# restore list


def test_the_listing_shows_a_session_with_its_timestamp_workflow_and_per_tree_counts(
    installed, record
):
    """AE18's first half, through the dispatcher, unacknowledged: read only, outside the gates."""
    code, envelope = _drive(["restore", "list"])
    assert code == int(ExitCode.OK), envelope
    rows = envelope["data"]["items"]
    assert rows, "the listing returned nothing on a library with a session"
    assert [row["session_id"] for row in rows] == [record.session_id]
    only = rows[0]
    assert only["started"] == record.started
    assert only["workflow"] == "library-sweep"
    assert only["restorable"] is True
    assert only["change"] == [{"tree": "routing", "created": 3, "updated": 1}]


def test_a_session_whose_capture_is_gone_is_listed_and_says_why(installed):
    """Reported rather than filtered, which is ``Restorable``'s decision carried out."""
    record, captured = completed_session(installed)
    shutil.rmtree(captured.root)
    code, envelope = _drive(["restore", "list"])
    assert code == int(ExitCode.OK), envelope
    only = envelope["data"]["items"][0]
    assert only["session_id"] == record.session_id
    assert only["restorable"] is False
    assert only["unusable"], "an unusable capture was listed with no sentence saying why"


# restore run: the two acts, and what is behind them


def test_the_confirmation_is_two_acts_and_then_the_database_comes_back(installed, acked, record):
    """AE18's second half, end to end, through the real dispatcher."""
    database = config.state_path("rekordbox_db", installed)
    before = database.read_bytes()
    database.write_bytes(b"database, generation two")
    code, refused, envelope = _two_acts(["restore", "run", record.session_id])
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    assert refused["resumable"] is True
    assert code == int(ExitCode.OK), envelope
    assert database.read_bytes() == before, "the verb reported OK and restored nothing"
    assert envelope["data"]["totals"]["steps"], "no step was reported as performed"


def test_an_aborted_confirmation_restores_nothing(installed, acked, record):
    """Abort is a real answer, and the measurement is the disk rather than the word."""
    database = config.state_path("rekordbox_db", installed)
    database.write_bytes(b"database, generation two")
    code, refused, envelope = _two_acts(["restore", "run", record.session_id], "abort")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert database.read_bytes() == b"database, generation two", (
        "a declined restore was performed anyway"
    )


def test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused(
    installed, acked, record
):
    """The digest is what makes a stale answer visible, and this is what puts it there."""
    code, refused = _drive(["restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    _answer(run_id, "restore")

    # The world moves: the recorded change summary is no longer the one shown.
    record.change = session.ChangeSummary(
        (session.TreeChange(tree="routing", created=99, updated=99),)
    )
    session.write_record(record, installed)
    code, envelope = _drive(["--run", run_id, "restore", "run", record.session_id])
    assert code == int(ExitCode.DECISION_STALE), envelope


def test_nothing_to_restore_is_an_outcome_and_opens_no_session(installed):
    """The empty path, and the proof that it takes no destructive session."""
    code, refused, envelope = _two_acts(["restore", "run"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["items"] == []


def test_a_confirmed_restore_queues_no_job_at_all(installed, acked, record):
    """Why the payload defect ``adopt.apply`` shipped cannot exist here, MEASURED."""
    code, refused, envelope = _two_acts(["restore", "run", record.session_id])
    assert code == int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == [], (
            "the restore queued a job, so it now owes the frozen run its explicit "
            "gate needs and nothing in this build supplies one"
        )


def test_a_session_identifier_nothing_recorded_is_refused_by_name(installed):
    """A typo gets a sentence about the identifier, not a traceback and not silence."""
    recorded, _captured = completed_session(installed)

    code, envelope = _drive(["restore", "run", "no-such-session"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert code != int(ExitCode.USAGE)
    assert "no-such-session" in envelope["cause"]["message"]
    assert recorded.session_id not in envelope["cause"]["message"], (
        "the refusal names a session the person did not ask for"
    )


def test_a_rehearsal_neutralizes_the_mirror_transfers_too(cfg, tmp_path, acked):
    """The dry run reaches BOTH halves, measured on the argv the runner is handed."""
    (tmp_path / "recovered").mkdir()
    seen: list[tuple[str, ...]] = []

    def runner(command):
        seen.append(tuple(command.argv))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    _one_session(cfg, runner, dry_run=True, target=tmp_path / "recovered")
    transfers = [argv for argv in seen if "copy" in argv]
    assert transfers, "the rehearsal described no transfer at all"
    for argv in transfers:
        assert "--dry-run" in argv, f"a rehearsal handed {argv} with nothing neutralizing it"


def test_the_mirror_is_pulled_before_the_capture_is_spent(cfg, acked, record):
    """The order is the reason the two halves compose, and it is not asserted elsewhere."""
    database = config.state_path("rekordbox_db", cfg)
    live = b"database, generation two, written after the capture"
    database.write_bytes(live)
    observed: list[bytes] = []

    def runner(command):
        observed.append(database.read_bytes())
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    _one_session(cfg, runner, session_id=record.session_id)
    assert observed, "the mirror half never ran, so no order was measured"
    assert observed[0] == live, "the capture was spent before the mirror pull began"
    assert database.read_bytes() != live, "the capture half never ran, so the order is vacuous"


def test_the_session_watches_the_whole_library_and_not_a_folder_inside_it(cfg, acked):
    """The analysis watch names the library root, driven rather than read."""
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

    assert armed == [(str(Path(cfg.library.root)),)], f"the session was armed over {armed}"
    watched = Path(armed[0][0])
    assert outside_music != watched and watched in outside_music.parents, (
        "the watch is narrower than the part of the library a restore writes to"
    )


def test_a_bare_run_takes_the_newest_spendable_capture_and_not_merely_the_newest(cfg):
    """The default has to skip an unusable row, or it refuses on every library that has one."""
    older, _first = completed_session(cfg, started="2026-08-01T00:00:00+00:00", stamp="a")
    newer, wrecked = completed_session(cfg, started="2026-08-02T00:00:00+00:00", stamp="b")
    shutil.rmtree(wrecked.root)
    chosen = restore_cli._newest_restorable(cfg)
    assert chosen is not None
    assert chosen.session_id == older.session_id, f"the default chose {newer.session_id}"


def test_a_dry_run_walks_every_step_and_performs_none_of_them(installed, acked, record):
    """The rehearsal, through the verb, measured against the database's bytes."""
    database = config.state_path("rekordbox_db", installed)
    database.write_bytes(b"database, generation two")
    code, refused, envelope = _two_acts(["restore", "run", record.session_id, "--dry-run"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["dry_run"] is True
    assert envelope["data"]["totals"]["steps"], "a rehearsal that described no step"
    assert database.read_bytes() == b"database, generation two", "a rehearsal performed it"


def test_the_discard_override_reaches_the_engine_as_identifiers(installed, acked):
    """R30's override, driven from the command line in both directions."""
    target, _captured = completed_session(installed, started="2026-08-01T00:00:00+00:00", stamp="a")
    later, _second = completed_session(installed, started="2026-08-02T00:00:00+00:00", stamp="b")
    code, _refused, envelope = _two_acts(["restore", "run", target.session_id])
    _refused_as(code, envelope, "restore-discards-committed-work", ExitCode.DECISION_REQUIRED)
    argv = ["restore", "run", target.session_id, "--discard", later.session_id]
    code, _refused, envelope = _two_acts(argv)
    assert code == int(ExitCode.OK), envelope


def test_the_digest_moves_when_the_discard_set_moves(installed):
    """A wider destruction is a different decision, and the digest has to say so."""
    target, _captured = completed_session(installed, started="2026-08-01T00:00:00+00:00", stamp="a")
    later, _second = completed_session(installed, started="2026-08-02T00:00:00+00:00", stamp="b")

    _code, narrow = _drive(["restore", "run", target.session_id])
    _code, wide = _drive(
        ["restore", "run", target.session_id, "--discard", later.session_id]
    )

    assert _offered_digest(narrow) != _offered_digest(wide), "the discard set moved no digest"


def test_the_digest_moves_when_the_mirror_half_or_the_rehearsal_flag_is_added(
    installed, monkeypatch, record
):
    """Approving one session authorises neither a mirror pull nor a full restore from a preview."""
    # The offer asks the remote which snapshot it is offering.
    _fake_rclone(installed, monkeypatch)
    _code, capture_only = _drive(["restore", "run", record.session_id])
    _code, with_mirror = _drive(["restore", "run", record.session_id, "--from-backup"])
    _code, preview = _drive(["restore", "run", record.session_id, "--dry-run"])
    assert _offered_digest(capture_only) != _offered_digest(with_mirror), "the mirror half"
    assert _offered_digest(preview) != _offered_digest(capture_only), "the rehearsal flag"


def test_the_confirmation_gate_is_found_by_digest_source_and_not_by_position(installed):
    """The handler asks the gate the entry DIGESTS, whichever order they are written in."""
    entry = registry.entry("restore.run")
    reversed_entry = replace(entry, gates=tuple(reversed(entry.gates)))
    assert [spec.name for spec in reversed_entry.gates] != [
        spec.name for spec in entry.gates
    ], "the entry declares fewer than two gates, so this measures nothing"

    chosen = restore_cli._confirm_gate(reversed_entry)

    assert chosen.digest_source == "plan"
    assert chosen.name == CONFIRM
    assert chosen is not reversed_entry.gates[0], "the handler took the first gate by position"


def test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default(
    cfg, tmp_path, acked
):
    """The per-slug answer survives, which is the whole reason the table holds one."""
    got = _refusal(
        restore_cli.restore_under_one_session,
        _without_remote(cfg),
        session_id=None,
        from_backup=True,
        target=tmp_path,
        **gate_seams(cfg),
    ).remediation
    expected = reservations.remediation_for(str(backup.Refusal.REMOTE_NOT_CONFIGURED))
    assert (got.remedy, got.steps) == (expected.remedy, expected.steps), (
        f"the refusal carries {got!r} rather than the reservation table's {expected!r}"
    )
    assert got.remedy != Remedy.REPORT_DEFECT, "an unconfigured remote is not a defect here"


def test_the_report_keeps_the_digest_the_decision_was_recorded_against(installed, acked, record):
    """The reported digest identifies the AUTHORISATION, never the work."""
    code, refused, envelope = _two_acts(["restore", "run", record.session_id])
    offered = refused["cause"]["detail"]
    assert code == int(ExitCode.OK), envelope
    from cratekit.cli import gates as cli_gates  # noqa: PLC0415
    recorded = cli_gates.load(refused["run_id"]).decisions[CONFIRM]
    assert envelope["data"]["digest"] == recorded.digest, (
        f"the report's digest is not the one the decision carries; the gate was "
        f"offered {offered.get('gate')!r}"
    )


# Fix round 2: the review's two blocking findings, and command line coverage


def test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen(cfg, acked):
    """BLOCKING finding 1, driven, and the measurement is what a person was told."""
    database = config.state_path("rekordbox_db", cfg)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"transactions committed since the last checkpoint")
    cause = _refusal(_one_session, cfg, _failing)
    assert cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert cause.code is not ExitCode.INTERNAL, "an unreachable remote is not a defect here"
    assert backup.RESTORE_DATABASE in cause.message, "the refusal names no failed transfer"
    assert cause.remediation.steps, "the person is not told what to do about it"
    # The companions were cleared and stay cleared, as the message says.
    assert not wal.exists()
    assert str(wal.name) in cause.message or "companion" in cause.message


def test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass(cfg, acked):
    """The same defect, one branch over, found by asking what else had the shape."""
    database = config.state_path("rekordbox_db", cfg)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"still here, because a rehearsal clears nothing")
    cause = _refusal(_one_session, cfg, _failing, dry_run=True)
    assert cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert wal.exists(), "a rehearsal cleared the live companion files"


def test_a_transfer_that_succeeds_is_still_reported(cfg, acked):
    """The other direction, so the refusal above is not simply a verb that refuses."""
    report = _one_session(cfg, lambda command: backup.CommandResult(returncode=0, stdout=""))
    assert report.pulled, "a run whose every transfer succeeded reported nothing"


def test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar(cfg, tmp_path, acked):
    """The report a person reads names the sidecar the snapshot did not hold."""
    (tmp_path / "recovered").mkdir()
    database = config.state_path("rekordbox_db", cfg).name
    report = _one_session(
        cfg,
        lambda command: backup.CommandResult(
            returncode=0,
            stdout=(database + "\n") if command.label == backup.LIST_SNAPSHOT_CONTENTS else "",
        ),
        target=tmp_path / "recovered",
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
    """R-338 at the report a person reads: the grids arrived, or it says they did not."""
    outside = _outside(cfg, tmp_path / "home" / "rekordbox", b"live")
    acknowledge(outside)
    (tmp_path / "recovered").mkdir()

    def runner(command):
        answers = {backup.LIST_SNAPSHOT_CONTENTS: "master.db\n", backup.LIST_SHARE: listing}
        return backup.CommandResult(returncode=0, stdout=answers.get(command.label, ""))

    report = _one_session(outside, runner, target=tmp_path / "recovered")
    assert report.pulled == pulled
    assert report.share == word
    totals = restore_cli._performed(report, {"digest": "d"})["totals"]
    assert totals["analysis_share"] == word


def test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean(
    cfg, tmp_path
):
    """Driven against the REAL analysis watch, with a runner that really writes."""
    outside = _outside(cfg, tmp_path / "home" / "rekordbox", b"live")
    acknowledge(outside)

    def runner(command):
        if command.label == backup.RESTORE_SHARE:
            grid = Path(command.argv[3]) / "PIONEER" / "USBANLZ" / "8d2" / "k" / "ANLZ0000.DAT"
            grid.parent.mkdir(parents=True, exist_ok=True)
            grid.write_bytes(b"PMAI")
        answers = {backup.LIST_SNAPSHOT_CONTENTS: "master.db\n", backup.LIST_SHARE: "PIONEER/\n"}
        return backup.CommandResult(returncode=0, stdout=answers.get(command.label, ""))

    report = _one_session(outside, runner)
    assert report.pulled == (backup.RESTORE_DATABASE,)
    assert report.share == "withheld"
    assert not list(Path(outside.library.root).rglob("ANLZ*"))


def test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect(installed, acked):
    """BLOCKING finding 2, with its producer DRIVEN rather than hand mutated."""
    record, captured = completed_session(installed)
    removed = restore.prune(
        installed, policy=restore.RetentionPolicy(keep=0, max_age=timedelta(0))
    )
    assert removed and not captured.root.exists(), "retention removed nothing"
    _code, listing = _drive(["restore", "list"])
    row = listing["data"]["items"][0]
    assert row["restorable"] is False
    sentence = row["unusable"]
    assert sentence, "the listing explains nothing, so there is nothing to agree with"
    argv = ["restore", "run", record.session_id]
    envelope = _refused_as(*_drive(argv), "restore-record-unusable")
    assert envelope["cause"]["remediation"]["remedy"] != str(Remedy.REPORT_DEFECT)
    assert sentence in envelope["cause"]["message"], "the two surfaces disagree on one state"


def test_an_unusable_capture_is_refused_before_the_mirror_moves_a_byte(cfg, acked):
    """The half of finding 2 that costs something, and it is the ordering."""
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
    installed, remote_log
):
    """``--from-backup``, driven end to end, which nothing did before."""
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup"])
    assert code == int(ExitCode.OK), envelope
    invoked = remote_log.read_text().splitlines() if remote_log.exists() else []
    assert invoked, "the flag was accepted and no transfer was ever attempted"
    copies = [line for line in invoked if " copy " in f" {line} "]
    assert envelope["data"]["totals"]["transfers"] == len(copies), envelope["data"]["totals"]
    assert all(item["half"] == "off-machine" for item in envelope["data"]["items"])


def test_without_the_flag_no_transfer_is_attempted_at_all(installed, remote_log):
    """The other direction, so the test above is not passing on a verb that always pulls."""
    code, refused, envelope = _two_acts(["restore", "run"])
    assert code == int(ExitCode.OK), envelope
    invoked = remote_log.read_text().splitlines() if remote_log.exists() else []
    assert invoked == [], f"a restore nobody asked to pull reached the remote: {invoked}"


def test_include_mirror_adds_the_file_half_and_its_absence_leaves_it_out(cfg, acked):
    """The flag that decides whether hundreds of gigabytes move, pinned both ways."""
    captured: dict[bool, list[str]] = {}
    for wanted in (False, True):
        labels: list[str] = []

        def runner(command, sink=labels):
            sink.append(command.label)
            return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")

        _one_session(cfg, runner, include_mirror=wanted)
        captured[wanted] = labels

    assert backup.RESTORE_MIRROR in captured[True]
    assert backup.RESTORE_MIRROR not in captured[False], "a mirror nobody asked for was pulled"


def test_the_snapshot_flag_chooses_which_dated_snapshot_is_pulled(cfg, acked):
    """``--snapshot``, pinned on the argv the transfer is actually given."""
    seen: list[tuple[str, ...]] = []

    def runner(command):
        seen.append(tuple(command.argv))
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")

    _one_session(cfg, runner, snapshot="2026-08-02T111111Z")
    copies = [argv for argv in seen if "copy" in argv]
    assert copies, "no transfer was attempted"
    assert all("2026-08-02T111111Z" in " ".join(argv) for argv in copies), copies


# ── the two properties nothing pinned at either layer ─────────────────────────


def test_the_default_takes_the_newest_of_several_spendable_captures(cfg):
    """Newest FIRST, pinned where reversing the order can actually be seen."""
    older, _first = completed_session(cfg, started="2026-08-01T00:00:00+00:00", stamp="a")
    newer, _second = completed_session(cfg, started="2026-08-02T00:00:00+00:00", stamp="b")
    assert older.session_id != newer.session_id

    chosen = restore_cli._newest_restorable(cfg)

    assert chosen is not None
    assert chosen.session_id == newer.session_id, f"the default took {chosen.session_id}"


def test_a_capture_that_exists_but_is_unverified_is_not_spendable(cfg):
    """The VERIFIED half of spendable, which nothing pinned at either layer."""
    record, captured = completed_session(cfg)
    only = restore_cli._newest_restorable(cfg)
    assert only is not None and only.session_id == record.session_id, "the fixture is unspendable"

    manifest = captured.root / snapshot.MANIFEST_NAME
    document = json.loads(manifest.read_text())
    assert document.get("integrity_verified") is True, "the fixture's capture was never verified"
    document["integrity_verified"] = False
    manifest.write_text(json.dumps(document))

    assert restore_cli._newest_restorable(cfg) is None, "an unverified capture was the default"



# R-368: a target that is the live library by another name, or beside a capture rollback.


def _sidecars_beside(path: Path) -> tuple[Path, ...]:
    """The live companion files, written so a run that clears them can be seen."""
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
    installed, scratch, remote_log
):
    """The close condition, driven through the dispatcher onto a scratch directory."""
    live = config.state_path("rekordbox_db", installed)
    companions = _sidecars_beside(live)
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup", "--target", str(scratch)])
    assert code == int(ExitCode.OK), envelope
    destinations = _copy_destinations(remote_log)
    assert destinations, "the flag was accepted and no transfer was ever attempted"
    assert all(place.startswith(str(scratch.resolve())) for place in destinations), destinations
    assert all(beside.exists() for beside in companions), "the LIVE companions were cleared"
    assert live.read_bytes() == b"database, generation one"


@pytest.mark.parametrize(
    "where, why",
    [
        ("root", "the library root itself"),
        ("inside", "a directory underneath the library root"),
        ("above", "the directory the library root sits in"),
    ],
)
def test_a_target_that_is_holds_or_sits_in_the_library_is_refused(
    installed, remote_log, where, why
):
    """The containment check, over the root and what equality alone does not cover."""
    root = Path(installed.library.root)
    named = {"root": root, "inside": root / "beneath", "above": root.parent}[where]
    if where == "inside":
        named.mkdir()

    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(named)])
    assert code == int(ExitCode.PRECONDITION), f"{why}: {envelope}"
    assert envelope["cause"]["reason"] == "restore-target-is-live-root", why
    assert envelope["cause"]["detail"]["check"] == "containment", why
    assert not remote_log.exists(), "the remote was reached by a run that is refused"


def test_a_target_whose_database_lands_on_the_live_one_is_refused(installed, tmp_path, remote_log):
    """The check the containment one cannot make, in the layout rekordbox ships."""
    home = tmp_path / "home" / "rekordbox"
    outside = _database_outside(installed, home)
    (home / "master.db").write_bytes(b"database, generation one")
    assert backup.database_target_for(outside, home) == config.state_path(
        "rekordbox_db", outside
    ), "the fixture does not reproduce the layout, so this pins nothing"
    assert not home.is_relative_to(outside.library.root), "containment would answer this"
    argv = ["restore", "run", "--from-backup", "--target", str(home)]
    envelope = _refused_as(*_drive(argv), "restore-target-is-live-root")
    assert envelope["cause"]["detail"]["check"] == "destination"
    assert not remote_log.exists(), "the remote was reached by a run that is refused"
    # The sentence names where the database would land, not only the slug.
    assert str(home / "master.db") in envelope["cause"]["message"], envelope
    assert "live database" in envelope["cause"]["message"], envelope


@pytest.mark.parametrize("case", ["no-pull", "beside-a-discard", "beside-a-named-session"])
def test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused(installed, case, acked):
    """The flag names where a pulled database goes, and never beside a rollback."""
    if case == "no-pull":
        argv = ["restore", "run", "--target", "/somewhere/else"]
    else:
        record, _captured = completed_session(installed)
        named = [record.session_id] if case == "beside-a-named-session" else []
        extra = ["--discard", "s-1"] if case == "beside-a-discard" else []
        argv = ["restore", "run", *named, "--from-backup", "--target", "/somewhere/else", *extra]

    _refused_as(*_drive(argv), "restore-target-invalid")


def test_a_target_run_rolls_no_session_back_even_by_default(
    installed, scratch, remote_log, record
):
    """The OTHER way a capture reaches a run, which the refusal above cannot see."""
    assert restore_cli._newest_restorable(installed) is not None, "no capture is spendable"
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup", "--target", str(scratch)])
    assert code == int(ExitCode.OK), envelope
    assert all(item["half"] == "off-machine" for item in envelope["data"]["items"])
    assert "converged" not in envelope["data"]["totals"], envelope["data"]["totals"]
    assert record.session_id in {
        entry.session_id for entry in restore.list_sessions(installed)
    }


def test_the_digest_moves_when_the_restore_is_pointed_somewhere_else(
    installed, scratch, remote_log
):
    """A decision about a rehearsal must not be honoured against the live restore."""
    _code, live = _drive(["restore", "run", "--from-backup"])
    _code, rehearsal = _drive(
        ["restore", "run", "--from-backup", "--target", str(scratch)]
    )
    assert _offered_digest(live) != _offered_digest(rehearsal), "the target moved no digest"


def test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal(
    installed, tmp_path, remote_log
):
    """The existing refusal, reached through the new flag rather than restated."""
    missing = tmp_path / "not-mounted"
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup", "--target", str(missing)])
    absent = str(backup.Refusal.RESTORE_TARGET_ABSENT)
    _refused_as(code, envelope, absent, ExitCode.LIBRARY_UNAVAILABLE)


def test_a_rehearsal_is_still_refused_while_rekordbox_is_running(
    installed, scratch, monkeypatch, remote_log
):
    """Today's live gates stay, which is half of what this unit promised."""
    _code, refused = _drive(["restore", "run", "--from-backup", "--target", str(scratch)])
    _answer(refused["run_id"], "restore")
    monkeypatch.setattr(
        "cratekit.core.processes.running_process_names", lambda: ("rekordbox",)
    )
    code, envelope = _drive(
        ["--run", refused["run_id"], "restore", "run", "--from-backup", "--target", str(scratch)]
    )
    _refused_as(code, envelope, "rekordbox-running", ExitCode.REKORDBOX_OPEN)


def test_a_relative_target_is_compared_as_the_place_it_names(installed, monkeypatch, acked):
    """The resolution, measured where leaving it out actually costs something."""
    root = Path(installed.library.root)
    monkeypatch.chdir(root.parent)
    argv = ["restore", "run", "--from-backup", "--target", root.name]
    envelope = _refused_as(*_drive(argv), "restore-target-is-live-root")
    # The refusal reports the resolved directory, not the word that was typed.
    assert envelope["cause"]["detail"]["target"] == str(root), envelope


def _database_outside(installed, home: Path):
    """Save the acknowledged layout with the database in ``home``, outside the root."""
    outside = _outside(installed, home, None, "2026-09-18")
    config.save(outside)
    config.reset_cache()
    return outside


def _live_by_another_spelling(where: Path, code: int, envelope: dict, check: str, why: str):
    """Refused as the live library where the filesystem folds case, and not otherwise."""
    if _case_folds(where):
        _refused_as(code, envelope, "restore-target-is-live-root")
        assert envelope["cause"]["detail"]["check"] == check
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings as two directories, so {why}"
        )


def _case_folds(where: Path) -> bool:
    """Whether this filesystem reads two spellings of one name as one directory."""
    probe = where / "Case_Probe"
    probe.mkdir()
    try:
        return (where / "case_probe").is_dir()
    finally:
        probe.rmdir()


def test_a_differently_cased_library_root_is_still_the_library(installed, tmp_path, remote_log):
    """The guard's own defect, found by this unit's review and driven here."""
    root = Path(installed.library.root)
    shouted = root.with_name(root.name.upper())
    assert str(shouted) != str(root), "the fixture's root is already upper case"
    live = config.state_path("rekordbox_db", installed)
    companions = _sidecars_beside(live)
    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])
    if _case_folds(tmp_path):
        _refused_as(code, envelope, "restore-target-is-live-root")
        assert all(beside.exists() for beside in companions), "the live companions were cleared"
        assert not remote_log.exists(), "the remote was reached by a run that is refused"
    else:
        assert envelope.get("cause", {}).get("reason") != "restore-target-is-live-root", (
            f"this filesystem holds the two spellings apart, so {shouted} is not the library"
        )


def test_a_differently_cased_database_directory_is_still_the_live_database(
    installed, tmp_path, acked
):
    """The same fold, on the destination check rather than on containment."""
    home = tmp_path / "home" / "Rekordbox"
    _database_outside(installed, home)
    (home / "master.db").write_bytes(b"database, generation one")
    shouted = home.with_name(home.name.upper())
    assert str(shouted) != str(home)
    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])
    _live_by_another_spelling(
        tmp_path, code, envelope, "destination",
        f"the database would land in {shouted} and not on the live one",
    )


def test_a_differently_cased_ancestor_still_puts_the_target_inside_the_library(
    installed, tmp_path, acked
):
    """The ancestor WALK, measured where the candidate itself is not the root."""
    root = Path(installed.library.root)
    (root / "beneath").mkdir()
    inside = root.parent / root.name.upper() / "beneath"
    assert not inside.is_relative_to(root), "the string test alone would answer this"
    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(inside)])
    _live_by_another_spelling(
        tmp_path, code, envelope, "containment", f"{inside} is not inside the library"
    )


def test_a_database_that_is_not_on_disk_yet_is_still_the_live_database(installed, tmp_path, acked):
    """The half of the destination check that ``samefile`` alone cannot make."""
    home = tmp_path / "home" / "rekordbox"
    _database_outside(installed, home)
    assert not (home / "master.db").exists(), "the half under measurement is not reached"
    shouted = home.with_name(home.name.upper())
    code, envelope = _drive(["restore", "run", "--from-backup", "--target", str(shouted)])
    _live_by_another_spelling(
        tmp_path, code, envelope, "destination",
        f"the database would land in {shouted} and not where the live one belongs",
    )


# Snapshot provenance, at the verb. What is approved is what arrives.

LATER = "2026-08-22T235959Z"


def _shown(refused: dict) -> dict:
    """The off-machine half as the refusal put it in front of the person."""
    assert refused["cause"]["reason"] == "decision-required", refused
    return refused["cause"]["detail"]["shown"]["off_machine"]


def _copied_from(log: Path) -> list[str]:
    """The source argument of every copy the fake program was asked to make."""
    lines = log.read_text().splitlines() if log.exists() else []
    return [line.split()[1] for line in lines if line.startswith("copy ")]


def test_a_backup_landing_between_the_two_acts_moves_the_digest(installed, remote_log):
    """The ledger's measurement, driven: offer and answer, then a second snapshot."""
    _code, refused = _drive(["restore", "run", "--from-backup"])
    item = _shown(refused)
    assert item["snapshot"] == STAMP
    _answer(refused["run_id"], "restore")
    _remote_holds((STAMP, LATER), cfg_value=installed)
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code != int(ExitCode.OK)
    assert _copied_from(remote_log) == [], f"a decision about {STAMP} was honoured"


def test_what_is_offered_is_what_is_pulled_and_reported(installed, monkeypatch, acked):
    """The newest stamp is resolved once, shown, approved, used, and named in the report."""
    log = _fake_rclone(installed, monkeypatch, snapshots=(STAMP, LATER))
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup"])
    item = _shown(refused)
    assert item["snapshot"] == LATER
    assert item["snapshot_named"] is False
    assert item["recorded_volume"] == preflight.normalize_identity(installed.library.volume_id)
    assert code == int(ExitCode.OK), envelope
    copied = _copied_from(log)
    assert copied and all(f"/{LATER}/db/" in source for source in copied), copied
    totals = envelope["data"]["totals"]
    assert totals["snapshot"] == LATER
    assert totals["recorded_volume"] == preflight.normalize_identity(
        installed.library.volume_id
    )


def test_the_ledgers_traversal_value_is_refused_at_the_verb(installed, remote_log):
    """Through the dispatcher, with the value the finding was measured with."""
    traversal = "../another-library-snapshots/2020-01-01T000000Z"
    argv = ["restore", "run", "--from-backup", "--snapshot", traversal]
    envelope = _refused_as(*_drive(argv), str(backup.Refusal.SNAPSHOT_NAME_INVALID))
    assert envelope["cause"]["remediation"]["steps"], envelope["cause"]
    assert not remote_log.exists() or remote_log.read_text() == ""


def test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes(
    installed, monkeypatch, acked
):
    log = _fake_rclone(installed, monkeypatch, marker="0000-AAAA")
    argv = ["restore", "run", "--from-backup", "--snapshot", STAMP]
    envelope = _refused_as(*_drive(argv), str(backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH))
    message = envelope["cause"]["message"]
    assert "0000-aaaa" in message
    assert preflight.normalize_identity(installed.library.volume_id) in message
    assert _copied_from(log) == []


def test_the_replaced_drive_flag_reaches_the_engine_and_the_digest(installed, monkeypatch, acked):
    """``--snapshot-volume``, driven end to end, and held to what it names."""
    log = _fake_rclone(installed, monkeypatch, marker="0000-AAAA")
    named = ["restore", "run", "--from-backup", "--snapshot", STAMP]
    _code, refused = _drive([*named, "--snapshot-volume", "0000-aaaa"])
    item = _shown(refused)
    assert item["expected_volume"] == "0000-aaaa"
    assert item["recorded_volume"] == "0000-aaaa"
    _answer(refused["run_id"], "restore")

    # Without the flag: refused as a mismatch before the recorded decision is consulted.
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
    installed, monkeypatch, acked
):
    """Every snapshot that exists on the day this lands is unmarked."""
    log = _fake_rclone(installed, monkeypatch, marker=None)
    code, envelope = _drive(["restore", "run", "--from-backup"])
    _refused_as(code, envelope, str(backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED))
    assert STAMP in envelope["cause"]["message"]
    code, refused, envelope = _two_acts(["restore", "run", "--from-backup", "--snapshot", STAMP])
    item = _shown(refused)
    assert item["snapshot_named"] is True
    assert item["recorded_volume"] is None
    assert code == int(ExitCode.OK), envelope
    assert _copied_from(log)


def test_a_restore_that_pulls_nothing_off_the_machine_still_asks_the_remote_nothing(
    installed, monkeypatch, record
):
    """The early listing is paid only by the half that needs it."""
    log = _fake_rclone(installed, monkeypatch)
    _drive(["restore", "run", record.session_id])
    assert not log.exists() or log.read_text() == ""


def test_the_digest_moves_when_the_expected_volume_is_stated(installed, remote_log):
    """The flag is part of what is approved, measured where it changes nothing else."""
    _code, plain = _drive(["restore", "run", "--from-backup"])
    stating = ["--snapshot-volume", installed.library.volume_id]
    _code, stated = _drive(["restore", "run", "--from-backup", *stating])
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
def test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for(installed, flags, record):
    """They were dropped in silence, ahead of a rollback nobody meant."""
    argv = ["restore", "run", record.session_id, *flags]
    envelope = _refused_as(*_drive(argv), "restore-flag-needs-pull")
    assert envelope["cause"]["detail"]["flags"] == [f for f in flags if f.startswith("--")]
    assert envelope["cause"]["remediation"]["steps"]


def test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled(installed, remote_log):
    """The window INSIDE the second act, which the digest cannot see."""
    home = Path(config.installation_state_dir())
    _code, refused = _drive(["restore", "run", "--from-backup"])
    _answer(refused["run_id"], "restore")
    (home / f"{REMOTE_SNAPSHOTS}.next").write_text(f"{STAMP}/\n{LATER}/\n")
    code, envelope = _drive(["--run", refused["run_id"], "restore", "run", "--from-backup"])
    assert code == int(ExitCode.OK), envelope
    assert not (home / f"{REMOTE_SNAPSHOTS}.next").exists(), "the remote never moved"
    copied = _copied_from(remote_log)
    assert copied and all(f"/{STAMP}/db/" in source for source in copied), copied


# restore bare-metal: the library volume is gone


def _recover(cfg, target, runner, **seams):
    """The bare metal session, accepted, into ``target`` through ``runner``."""
    return restore_cli.recover_under_bare_metal_session(
        cfg, target=target, accepted=True, runner=runner, **seams
    )


#: A file the mirror carries, relative to the volume it was taken from.
MIRRORED = "Music/a-track.flac"


class _Remote:
    """A runner answering the listings and PERFORMING each copy: ``failing`` labels write
    nothing, ``cut`` ones land and THEN fail, ``failing_files`` fail their own transfer."""

    def __init__(
        self,
        cfg_value,
        *,
        failing=(),
        mirrored=(MIRRORED,),
        holds=("master.db", "master.db-wal"),
        cut=(),
        failing_files=(),
    ):
        self.cfg = cfg_value
        self.failing = frozenset(failing)
        self.mirrored = tuple(mirrored)
        self.holds = tuple(holds)
        self.cut = frozenset(cut)
        self.failing_files = frozenset(failing_files)
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
            # A MIRRORED SHARE IS ALWAYS HELD, so an outside layout plans its transfer.
            return backup.CommandResult(0, "PIONEER/\n")
        if command.label in self.failing:
            return backup.CommandResult(3)
        if "--dry-run" in command.argv:
            return backup.CommandResult(0)
        source, destination = command.argv[2], Path(command.argv[3])
        if source.rsplit("/", 1)[-1] in self.failing_files:
            return backup.CommandResult(3)
        if command.label == backup.RESTORE_MIRROR:
            # AN ANCHORED EXCLUDE IS HONOURED, as rclone reads one.
            argv = command.argv
            excluded = {
                argv[i + 1] for i, arg in enumerate(argv[:-1]) if arg == "--exclude"
            }
            for relative in self.mirrored:
                if f"/{relative}" in excluded:
                    continue
                landed = destination / relative
                landed.parent.mkdir(parents=True, exist_ok=True)
                landed.write_bytes(b"mirrored")
        else:
            destination.mkdir(parents=True, exist_ok=True)
            (destination / source.rsplit("/", 1)[-1]).write_bytes(b"from the snapshot")
        return backup.CommandResult(3 if command.label in self.cut else 0)

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
    dead = restore_suite._volume_is_gone(cfg_value)
    return {**dead, "terminal": lambda: True, "process_lister": lambda: (), **overrides}


@pytest.fixture
def seams(cfg) -> dict:
    """``_gone``'s seams for the configured library."""
    return _gone(cfg)


def _replacement(tmp_path) -> Path:
    target = tmp_path / "replacement"
    target.mkdir()
    return target


@pytest.fixture
def target(tmp_path) -> Path:
    return _replacement(tmp_path)


@pytest.fixture
def scratch(tmp_path) -> Path:
    """An empty directory to rehearse a restore into."""
    (tmp_path / "rehearsal").mkdir()
    return tmp_path / "rehearsal"


def test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target(
    cfg, tmp_path, target, seams
):
    remote = _Remote(cfg)
    state = Path(config.installation_state_dir())
    before = _everything_on_disk(tmp_path, state)
    report = _recover(cfg, target, remote, **seams)
    assert (target / MIRRORED).read_bytes() == b"mirrored"
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"
    assert (target / "db" / "master.db-wal").exists()
    assert report.target == target
    assert report.database_target == target / "db" / "master.db"
    assert report.mirror == (backup.RESTORE_MIRROR,)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert report.snapshot == STAMP
    assert [c.label for c in remote.transfers][0] == backup.RESTORE_MIRROR
    destinations = [Path(c.argv[3]) for c in remote.transfers]
    assert len(destinations) == 3
    assert all(d == target or d.is_relative_to(target) for d in destinations), destinations
    after = _everything_on_disk(tmp_path, state)
    outside = {
        path
        for path in after.keys() - before.keys()
        if not Path(path).is_relative_to(target)
    }
    assert outside == {str(restore.recovery_lock_path())}, outside
    assert {p: b for p, b in after.items() if p in before} == before
    assert not Path(cfg.library.root).exists(), "the lost library's path was recreated"


def _mounted(cfg_value, tmp_path):
    """A library that is present and is the recorded volume, and NOTHING ELSE WRONG."""
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
    cause = _refusal(
        restore_cli.recover_under_bare_metal_session,
        cfg, target=target, accepted=accepted, runner=remote, **seams,
    )
    assert cause.reason == "recovery-target-refused"
    assert said in cause.message
    assert remote.calls == [], "the remote was asked something by a refused recovery"
    assert _everything_on_disk(tmp_path, state) == before
    assert not restore.recovery_lock_path().exists()


def test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it(cfg, target):
    """The verb never passes ``replacing_existing``, and has no flag that could."""
    (target / "db").mkdir(parents=True)
    (target / "db" / "master.db").write_bytes(b"somebody's library")
    remote = _Remote(cfg)
    cause = _refusal(_recover, cfg, target, remote, **_gone(cfg))
    assert cause.reason == "recovery-target-refused"
    assert "already holds master.db" in cause.message
    assert remote.calls == []
    assert (target / "db" / "master.db").read_bytes() == b"somebody's library"
    # A usage error prints no envelope, so the parser is asked rather than driven.
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(
            ["restore", "bare-metal", "--target", str(target), "--replace-existing"]
        )


def test_both_halves_run_inside_one_holding_of_the_recovery_lock(cfg, target, seams):
    """Asked from a REAL second interpreter, while each transfer is in flight."""
    observed: list[int] = []

    class _Watching(_Remote):
        def __call__(self, command):
            if command.label in (backup.RESTORE_MIRROR, backup.RESTORE_DATABASE):
                observed.append(_lock_taken_in_another_process(restore.recovery_lock_path()))
            return super().__call__(command)

    _recover(cfg, target, _Watching(cfg), **seams)
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
        cause = _refusal(_recover, cfg, target, remote, **seams)

    assert cause.reason == "session-lock-held", cause
    assert str(lock) in cause.message
    assert remote.calls == []
    assert list(target.iterdir()) == []


def test_the_verb_cannot_be_typed_without_naming_a_target():
    """No default, because the only default there could be is the lost volume."""
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["restore", "bare-metal", "--accept-replacement"])


def test_a_recovery_is_refused_underneath_a_running_rekordbox(cfg, target):
    remote = _Remote(cfg)
    seams = _gone(cfg, process_lister=lambda: ("rekordbox",))
    cause = _refusal(_recover, cfg, target, remote, **seams)
    assert cause.reason == "rekordbox-running"
    assert remote.transfers == []
    assert list(target.iterdir()) == []


def test_a_failed_mirror_stops_the_recovery_before_the_database(cfg, target, seams):
    """The engine runs every command before reading one; the verb runs a half."""
    remote = _Remote(cfg, failing={backup.RESTORE_MIRROR})
    cause = _refusal(_recover, cfg, target, remote, **seams)
    assert cause.reason == "restore-transfer-failed"
    assert cause.detail["half"] == restore_cli.MIRROR_HALF
    assert cause.detail["completed_halves"] == []
    assert "exited 3" in cause.detail["engine"]
    assert "database half was not attempted" in cause.message
    assert "cleared" not in cause.message
    assert not any("remove" in step for step in cause.remediation.steps)
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not list(target.rglob("*.db"))
    again = _recover(cfg, target, _Remote(cfg), **seams)
    assert again.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)


def test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove(cfg, target):
    remote = _Remote(cfg, failing={backup.RESTORE_DATABASE})
    cause = _refusal(_recover, cfg, target, remote, **_gone(cfg))
    assert cause.reason == "restore-transfer-failed"
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert cause.detail["completed_halves"] == [restore_cli.MIRROR_HALF]
    assert "mirror half completed" in cause.message
    assert "master.db" in cause.message
    assert cause.remediation.steps[0] == "do not open the library"
    assert "remove master.db and any companion" in cause.remediation.steps[-1]
    assert str(target / "db") in cause.remediation.steps[-1]
    assert (target / MIRRORED).exists()


def test_a_rehearsal_passes_the_same_gates_and_writes_nothing(cfg, target):
    remote = _Remote(cfg)
    report = _recover(cfg, target, remote, dry_run=True, **_gone(cfg))
    assert report.dry_run is True
    assert report.mirror == (backup.RESTORE_MIRROR,)
    assert len(report.database) == 2
    assert all("--dry-run" in c.argv for c in remote.transfers)
    assert list(target.iterdir()) == []
    cause = _refusal(
        restore_cli.recover_under_bare_metal_session,
        cfg, target=target, accepted=False, dry_run=True, runner=remote, **_gone(cfg),
    )
    assert "explicit decision" in cause.message


def test_a_failed_rehearsal_says_nothing_was_written(cfg, target):
    remote = _Remote(cfg, failing={backup.RESTORE_MIRROR})
    cause = _refusal(_recover, cfg, target, remote, dry_run=True, **_gone(cfg))
    assert "nothing was written" in cause.message
    assert cause.detail["dry_run"] is True
    assert not any("remove" in step for step in cause.remediation.steps)


def test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything(cfg, target):
    """The removal step is for a half that may have landed files. A rehearsal landed none."""
    remote = _Remote(cfg, failing={backup.RESTORE_DATABASE})
    cause = _refusal(_recover, cfg, target, remote, dry_run=True, **_gone(cfg))
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert "nothing was written" in cause.message
    assert not any("remove" in step for step in cause.remediation.steps)
    assert list(target.iterdir()) == []


#: An interrupted run's state directory beside the music: a review queue and a capture.
CARRIED = (MIRRORED, ".cratekit/queue.db", ".cratekit/snapshots/one/master.db")


def test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed(cfg, target, seams):
    """R-592. The rerun used to be refused until every database file was deleted."""
    first = _Remote(cfg, failing={backup.RESTORE_DATABASE}, mirrored=CARRIED)
    failed = _refusal(_recover, cfg, target, first, **seams)
    assert failed.detail["half"] == restore_cli.DATABASE_HALF
    assert (target / ".cratekit" / "queue.db").exists(), "the fixture landed nothing"
    report = _recover(cfg, target, _Remote(cfg, mirrored=CARRIED), **seams)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert (target / ".cratekit" / "queue.db").exists()
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"


def test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed(cfg, target, seams):
    """The mirror landed the queue and a capture, then dropped. No step, no refusal."""
    first = _Remote(cfg, cut={backup.RESTORE_MIRROR}, mirrored=CARRIED)
    failed = _refusal(_recover, cfg, target, first, **seams)
    assert failed.detail["half"] == restore_cli.MIRROR_HALF
    assert not any("remove" in step for step in failed.remediation.steps)
    assert len(list(target.rglob("*.db"))) == 2, "the fixture landed nothing"
    report = _recover(cfg, target, _Remote(cfg, mirrored=CARRIED), **seams)
    assert report.mirror == (backup.RESTORE_MIRROR,)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"


def test_a_mirror_still_carrying_the_database_does_not_land_it(cfg, target, seams):
    """A mirror taken before the backup excluded the database may still hold it."""
    stale = (*CARRIED, "db/master.db", "db/master.db-wal")
    first = _Remote(cfg, cut={backup.RESTORE_MIRROR}, mirrored=stale)
    with pytest.raises(CratekitError):
        _recover(cfg, target, first, **seams)
    assert (target / ".cratekit" / "queue.db").exists(), "the fixture landed nothing"
    assert not (target / "db" / "master.db").exists()
    assert not (target / "db" / "master.db-wal").exists()
    report = _recover(cfg, target, _Remote(cfg, mirrored=stale), **seams)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert (target / "db" / "master.db").read_bytes() == b"from the snapshot"


def test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step(
    cfg, target, seams
):
    """WHAT R-592 STILL LEAVES, driven. The database arrived and its log did not."""
    first = _Remote(cfg, mirrored=CARRIED, failing_files={"master.db-wal"})
    step = _refusal(_recover, cfg, target, first, **seams).remediation.steps[-1]
    assert (target / "db" / "master.db").exists(), "the fixture landed nothing"
    again = _refusal(_recover, cfg, target, _Remote(cfg, mirrored=CARRIED), **seams)
    assert "already holds master.db" in again.message
    assert "remove master.db and any companion" in step
    assert str(target / "db") in step
    for landed in (target / "db").glob("master.db*"):
        landed.unlink()
    report = _recover(cfg, target, _Remote(cfg, mirrored=CARRIED), **seams)
    assert report.database == (backup.RESTORE_DATABASE, backup.RESTORE_DATABASE)
    assert (target / ".cratekit" / "queue.db").exists()
    assert (target / "db" / "master.db-wal").read_bytes() == b"from the snapshot"


def test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half(cfg, target):
    """Asked twice, because the first answer is hours old by the second half."""
    remote = _Remote(cfg)
    answers = iter([(), ("rekordbox",)])
    seams = _gone(cfg, process_lister=lambda: next(answers))
    cause = _refusal(_recover, cfg, target, remote, **seams)
    assert cause.reason == "rekordbox-running"
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert cause.detail["completed_halves"] == [restore_cli.MIRROR_HALF]
    assert "mirror half completed" in cause.message
    assert "remove master.db and any companion" in cause.remediation.steps[-1]
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not list(target.rglob("master.db*"))


def test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one(
    cfg, tmp_path
):
    """rekordbox's own default layout: the database is on the internal disk."""
    home = tmp_path / "home" / "rekordbox"
    outside = _outside(cfg, home, b"alive, and never on the lost volume", "2026-09-18")
    assert backup.database_target_for(outside, tmp_path) == tmp_path / "master.db", (
        "the fixture does not reproduce the layout, so this pins nothing"
    )
    target = _replacement(tmp_path)
    # No write ahead log, so the plan names an absent companion the report must not.
    remote = _Remote(outside, holds=("master.db",))
    report = _recover(outside, target, remote, **_gone(outside))
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not (target / "master.db").exists()
    # The share rides the database half and is withheld before the remote is asked (R-338).
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
    """A machine whose library volume is gone, with the PLATFORM seams answered."""
    shutil.rmtree(cfg.library.root)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: "0000-not-this-disk")
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    monkeypatch.setattr(restore, "_is_mount_point", lambda _path: True)
    return cfg


def test_the_verb_recovers_both_halves_and_reports_them_apart(lost, monkeypatch, target):
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


def test_the_verb_refuses_without_the_acceptance_flag(lost, monkeypatch, target):
    log = _fake_rclone(lost, monkeypatch)
    argv = ["restore", "bare-metal", "--target", str(target)]
    envelope = _refused_as(*_drive(argv), "recovery-target-refused")
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
    _refused_as(code, envelope, "recovery-target-refused")
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

    recover = restore_cli.recover_under_bare_metal_session
    cause = _refusal(recover, cfg, target=target, accepted=True, **_gone(cfg))

    assert cause.reason == "rclone-missing"
    assert list(target.iterdir()) == []


def test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left(
    cfg, tmp_path, monkeypatch
):
    """U211. The scan's refusal, named, with the half it stopped at and the rerun step."""
    _fake_rclone(cfg, monkeypatch)
    target = _replacement(tmp_path)
    remote = _Remote(cfg)

    def scans():
        yield ()
        raise processes._unconfirmed([(300, "SystemError: proc_cmdline")])

    answers = scans()
    cause = _raised(
        processes.AbsenceUnconfirmed,
        _recover, cfg, target, remote, **_gone(cfg, process_lister=lambda: next(answers)),
    ).cause
    assert cause.reason == processes.UNCONFIRMED
    assert "process 300" in cause.message
    assert "mirror half completed" in cause.message
    assert cause.detail["half"] == restore_cli.DATABASE_HALF
    assert cause.detail["completed_halves"] == [restore_cli.MIRROR_HALF]
    assert cause.detail["pids"] == [300]
    assert "remove master.db and any companion" in cause.remediation.steps[-1]
    assert [c.label for c in remote.transfers] == [backup.RESTORE_MIRROR]
    assert not list(target.rglob("master.db*"))


# R-2071: the three place guards, measured where a filesystem that never folds case
# still holds two names for one place.


def test_a_second_name_for_the_live_database_file_is_still_the_live_database(
    installed, tmp_path, remote_log
):
    """A hard link is one file under two names, which a spelling test cannot see."""
    home = tmp_path / "home" / "rekordbox"
    _database_outside(installed, home)
    (home / "master.db").write_bytes(b"database, generation one")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "master.db").hardlink_to(home / "master.db")
    assert elsewhere.name != home.name, "the name plus parent half would answer this"
    argv = ["restore", "run", "--from-backup", "--target", str(elsewhere)]
    envelope = _refused_as(*_drive(argv), "restore-target-is-live-root")
    assert envelope["cause"]["detail"]["check"] == "destination", envelope
    assert not remote_log.exists(), "the remote was reached by a run that is refused"
    assert (home / "master.db").read_bytes() == b"database, generation one"


def test_an_ancestor_that_is_the_root_by_another_name_holds_the_place(tmp_path):
    """The ancestor walk, driven alone: the candidate is not the root, its parent is."""
    root = tmp_path / "library"
    (root / "beneath").mkdir(parents=True)
    alias = tmp_path / "alias"
    alias.symlink_to(root, target_is_directory=True)
    place = alias / "beneath"
    assert not place.is_relative_to(root), "the string test alone would answer this"
    assert not place.samefile(root), "the candidate alone would answer this"
    assert restore_cli._holds_or_is(root, place)
    assert not restore_cli._holds_or_is(root, tmp_path / "elsewhere" / "beneath")


def test_a_database_not_on_disk_in_a_folded_directory_is_still_the_live_database(
    installed, tmp_path, monkeypatch, remote_log
):
    """The name plus parent half, with the folding filesystem's answer planted.

    Linux never folds case, so the place test is answered as a folding one would
    answer it: the two spellings of the database's directory are one directory,
    and nothing else changes. The database itself is not on disk yet, so the
    landing alone matches nothing and only the second half can refuse.
    """
    home = tmp_path.resolve() / "home" / "rekordbox"
    _database_outside(installed, home)
    shouted = home.with_name(home.name.upper())
    assert not (home / "master.db").exists(), "the half under measurement is not reached"
    real = restore_cli._same_place

    def folding(one: Path, other: Path) -> bool:
        return {one, other} == {home, shouted} or real(one, other)

    monkeypatch.setattr(restore_cli, "_same_place", folding)
    argv = ["restore", "run", "--from-backup", "--target", str(shouted)]
    envelope = _refused_as(*_drive(argv), "restore-target-is-live-root")
    assert envelope["cause"]["detail"]["check"] == "destination", envelope
    assert not remote_log.exists(), "the remote was reached by a run that is refused"
