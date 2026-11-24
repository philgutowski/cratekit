"""The mirror's comparison, its two modes, and what the run says about it.

The real rclone is driven, since the claims are about what it SENDS, between
temporary folders aliased as remotes so no account is read.
"""

from __future__ import annotations

import io
import json
import os
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.backup import cli as backup_cli
from cratekit.cli import doctor
from cratekit.core import backup_facts, binaries, config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup

MOMENT = datetime(2026, 8, 29, 12, 0, 0, tzinfo=timezone.utc)

#: The modes, as the payload the shell freezes for each.
FAST = {backup_cli.FULL: False}
FULL = {backup_cli.FULL: True}
MODES = pytest.mark.parametrize("payload", [FAST, FULL], ids=["fast", "full"])

#: The remotes the temporary rclone configuration declares as folder aliases.
REMOTES = ("remote", "fast", "full")


def _remote_folder(tmp_path: Path, name: str) -> Path:
    return tmp_path / "remotes" / name


def _folder(tmp_path: Path, destination: str) -> Path:
    """The temporary folder one ``remote:path`` destination really is."""
    name, _, inside = str(destination).partition(":")
    return _remote_folder(tmp_path, name) / inside


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def real_rclone(monkeypatch, tmp_path) -> str:
    """The rclone on this machine, asserted present (never skipped), reading no account."""
    monkeypatch.delenv("CRATEKIT_BIN_RCLONE", raising=False)
    declared = tmp_path / "rclone.conf"
    declared.write_text(
        "".join(
            f"[{name}]\ntype = alias\nremote = {_remote_folder(tmp_path, name)}\n\n"
            for name in REMOTES
        )
    )
    monkeypatch.setenv("RCLONE_CONFIG", str(declared))
    found = binaries.find("rclone")
    assert found is not None, "rclone, a declared binary of the backup module, is not installed"
    return str(found)


def _configured(
    root: Path, remote: str, tmp_path: Path, *, folders: tuple[str, ...] = ("Music", "db")
) -> config.Config:
    """A library at ``root`` holding ``folders``, whose three destinations are on the remote named."""
    root.mkdir(parents=True, exist_ok=True)
    for folder in folders:
        (root / folder).mkdir(exist_ok=True)
    return config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root), "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
            "backup": {
                "remote": remote, "dest": f"{remote}:mirror",
                "archive_root": f"{remote}:archive", "db_dest_root": f"{remote}:database",
            },
        }
    )


def _saved(tmp_path: Path, monkeypatch, *, folders: tuple[str, ...] = ("Music", "db")) -> config.Config:
    """The library at ``tmp_path / "library"`` on the remote ``remote``, saved and read fresh."""
    root = tmp_path / "library"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    built = _configured(root, "remote", tmp_path, folders=folders)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    return _saved(tmp_path, monkeypatch)


def _write(path: Path, content: bytes, *, at: datetime) -> None:
    """One file with a stated modification time, so no test races the clock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    stamp = at.timestamp()
    os.utime(path, (stamp, stamp))


def _one_track(cfg) -> None:
    """A library holds its music, since a backup refuses an empty root."""
    _write(cfg.library.root / "Music" / "fixture.flac", b"one track", at=MOMENT)


def _seed(cfg) -> Path:
    """Three tracks in the library, and the folder they live in."""
    music = cfg.library.root / "Music"
    tracks = {"kept.flac": b"kept, generation one", "retagged.flac": b"genre: house...."}
    for name, content in {**tracks, "removed.flac": b"removed, generation one"}.items():
        _write(music / name, content, at=MOMENT)
    return music


def _only(plan: backup.BackupPlan, portion=backup_facts.Portion.FILES) -> backup.BackupPlan:
    return replace(plan, portions=(plan.portion(portion),))


def _files_portion(report: dict) -> dict:
    (row,) = [r for r in report["portions"] if r["portion"] == "files"]
    return row


def _mirror(payload: dict, cfg, *, now: datetime, publish: bool = False) -> dict:
    """The FILES portion's rendered row from the real program, publishing only when
    asked, since the fact file a publish writes is under the library root."""
    full, check = bool(payload.get(backup_cli.FULL)), bool(payload.get(backup_cli.CHECK))
    narrowed = _only(backup.plan_backup(cfg, now=now, full=full, check=check))
    outcome = backup.run_backup(
        cfg, narrowed, now=now, dry_run=bool(payload.get(backup_cli.DRY_RUN)), publish=publish
    )
    return _files_portion(backup.outcome_payload(outcome))


def _held(folder: Path) -> dict[str, bytes]:
    """Every file under one folder, by relative path."""
    files = sorted(folder.rglob("*")) if folder.is_dir() else []
    return {str(path.relative_to(folder)): path.read_bytes() for path in files if path.is_file()}


def _mirror_command(cfg, **kwargs) -> backup.Command:
    _one_track(cfg)
    commands = _only(backup.plan_backup(cfg, now=MOMENT, **kwargs)).portions[0].commands
    (found,) = [command for command in commands if command.label == backup.MIRROR]
    return found


def test_the_two_modes_differ_by_the_listing_option_and_by_nothing_else(cfg, real_rclone):
    """The full mode is the fast one with one word removed, and nothing else."""
    fast = list(_mirror_command(cfg).argv)
    full = list(_mirror_command(cfg, full=True).argv)
    assert backup.FAST_LIST in fast and backup.FAST_LIST not in full
    assert [word for word in fast if word != backup.FAST_LIST] == full
    assert backup.comparison_mode(_mirror_command(cfg)) == "fast"
    assert backup.comparison_mode(_mirror_command(cfg, full=True)) == "full"


@pytest.mark.parametrize(
    "forbidden", ["--size-only", "--max-age", "--ignore-times", "--ignore-existing"]
)
def test_neither_mode_carries_an_option_that_can_skip_a_changed_file(cfg, real_rclone, forbidden):
    """Each would be faster and skip a changed file (a same length tag write, an old date)."""
    for full in (False, True):
        argv = _mirror_command(cfg, full=full).argv
        assert not any(word.startswith(forbidden) for word in argv), argv


@MODES
def test_nothing_changed_sends_nothing_and_says_so(cfg, real_rclone, payload, tmp_path):
    _seed(cfg)
    first = _mirror(payload, cfg, now=MOMENT)
    assert first["comparison"]["sent"] == 3, first
    # A file only in the library is sent unchecked, and a zero sent means nothing
    # changed only beside a count of what was compared.
    assert first["comparison"]["checked"] == 0, first

    said = _mirror(payload, cfg, now=MOMENT + timedelta(hours=1))["comparison"]
    assert said["sent"] == 0, said
    assert said["checked"] == 3, said
    assert isinstance(said["seconds"], float) and said["seconds"] > 0, said
    assert _held(_folder(tmp_path, cfg.backup.archive_root)) == {}


@MODES
def test_a_file_changed_in_content_and_not_in_size_is_sent(cfg, real_rclone, payload, tmp_path):
    """A tag write keeping the length, which a comparison of size alone skips."""
    music = _seed(cfg)
    _mirror(payload, cfg, now=MOMENT)
    before, after = b"genre: house....", b"genre: techno..."
    assert len(before) == len(after) and (music / "retagged.flac").read_bytes() == before
    _write(music / "retagged.flac", after, at=MOMENT + timedelta(minutes=30))
    later = MOMENT + timedelta(hours=1)
    row = _mirror(payload, cfg, now=later)
    assert row["comparison"]["sent"] == 1, row
    assert (_folder(tmp_path, cfg.backup.dest) / "Music" / "retagged.flac").read_bytes() == after
    assert _held(_folder(tmp_path, cfg.backup.archive_root) / backup.stamp_for(later)) == {
        "Music/retagged.flac": before
    }, "the version the mirror replaced is not in this run's dated archive folder"


@MODES
def test_an_added_file_is_sent_and_a_removed_one_is_archived(cfg, real_rclone, payload, tmp_path):
    music = _seed(cfg)
    _mirror(payload, cfg, now=MOMENT)
    _write(music / "added.flac", b"added", at=MOMENT + timedelta(minutes=30))
    (music / "removed.flac").unlink()
    later = MOMENT + timedelta(hours=1)
    row = _mirror(payload, cfg, now=later)
    assert row["comparison"]["sent"] == 1, row
    mirrored = _held(_folder(tmp_path, cfg.backup.dest))
    assert "Music/added.flac" in mirrored and "Music/removed.flac" not in mirrored
    assert _held(_folder(tmp_path, cfg.backup.archive_root) / backup.stamp_for(later)) == {
        "Music/removed.flac": b"removed, generation one"
    }


def test_the_two_modes_agree_on_what_to_send_for_the_same_fixture(
    tmp_path, monkeypatch, real_rclone
):
    """One set of changes made to two libraries, one run per mode."""
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    ended: dict[str, tuple[dict, dict, dict]] = {}
    for name, payload in (("fast", FAST), ("full", FULL)):
        root = tmp_path / name / "library"
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        one = _configured(root, name, tmp_path / name)
        music = _seed(one)
        _mirror(payload, one, now=MOMENT)
        _write(music / "retagged.flac", b"genre: techno...", at=MOMENT + timedelta(minutes=30))
        _write(music / "added.flac", b"added", at=MOMENT + timedelta(minutes=30))
        (music / "removed.flac").unlink()
        later = MOMENT + timedelta(hours=1)
        row = _mirror(payload, one, now=later)
        assert row["comparison"]["mode"] == name, row
        counts = {key: row["comparison"][key] for key in ("checked", "sent", "sent_bytes")}
        archived = _held(_folder(tmp_path, one.backup.archive_root) / backup.stamp_for(later))
        ended[name] = (counts, _held(_folder(tmp_path, one.backup.dest)), archived)

    assert ended["fast"] == ended["full"]
    assert ended["fast"][0]["sent"] == 2, ended["fast"]


def test_a_run_that_published_sends_its_own_record_next_time(cfg, real_rclone, tmp_path):
    """An unchanged library's full check sends the fact file the mirror carries;
    without the check it is skipped, as ``tests/test_backup_quick.py`` holds."""
    _seed(cfg)
    _mirror(FAST, cfg, now=MOMENT, publish=True)
    fact = backup_facts.path_for(cfg)
    assert cfg.library.root in fact.parents, "the fact file moved out of the library"

    later = MOMENT + timedelta(hours=1)
    row = _mirror({**FAST, backup_cli.CHECK: True}, cfg, now=later, publish=True)

    assert row["comparison"]["sent"] == 1, row
    sent = _folder(tmp_path, cfg.backup.dest) / fact.relative_to(cfg.library.root)
    carried = json.loads(sent.read_text())["portions"]["files"]["completed_at"]
    assert carried == MOMENT.isoformat(), "the second run sent another run's record"


def test_a_rehearsal_counts_what_it_would_send_and_sends_nothing(cfg, real_rclone, tmp_path):
    _seed(cfg)
    row = _mirror({backup_cli.DRY_RUN: True}, cfg, now=MOMENT)

    assert row["comparison"]["sent"] == 3, row
    assert _held(_folder(tmp_path, cfg.backup.dest)) == {}


def _answering(stderr: str, *, returncode: int = 0, elapsed: float | None = 12.5):
    """A stand in runner whose mirror answers as told."""

    def runner(command: backup.Command) -> backup.CommandResult:
        if command.label == backup.MIRROR:
            return backup.CommandResult(returncode=returncode, stderr=stderr, elapsed=elapsed)
        return backup.CommandResult(returncode=0)

    return runner


def _totals(**stats) -> str:
    return json.dumps({"level": "notice", "msg": "totals", "stats": stats})


def _run_files(cfg, runner, *, full: bool = False) -> backup.PortionOutcome:
    """The files portion's full check (a rerun would otherwise skip) over ``runner``."""
    _one_track(cfg)
    narrowed = _only(backup.plan_backup(cfg, now=MOMENT, full=full, check=True))
    (outcome,) = backup.run_backup(cfg, narrowed, runner=runner, now=MOMENT).portions
    return outcome


def test_totals_that_could_not_be_read_are_none_and_never_zero(cfg, real_rclone):
    """A run whose totals were not found must not answer that it sent nothing."""
    outcome = _run_files(cfg, _answering("a line that is not a totals object\n"))

    assert outcome.ran
    said = dict(outcome.comparison)
    assert said["sent"] is None and said["checked"] is None, said
    assert said["seconds"] == 12.5 and said["mode"] == "fast", said

    untimed = _run_files(cfg, _answering(_totals(checks=4, transfers=1), elapsed=None))
    assert untimed.comparison["seconds"] is None and untimed.comparison["sent"] == 1


def test_the_last_totals_logged_are_the_ones_reported(cfg, real_rclone):
    """A run longer than the interval logs totals more than once."""
    logged = "\n".join(
        [_totals(checks=10, transfers=1), "not json", _totals(checks=40, transfers=6)]
    )
    outcome = _run_files(cfg, _answering(logged))

    assert outcome.comparison["checked"] == 40 and outcome.comparison["sent"] == 6


def test_a_failed_mirror_says_why_in_words_and_how_far_it_got(cfg, real_rclone):
    """The mirror logs JSON, and the tail of a JSON log is the totals object."""
    went_away = json.dumps({"level": "error", "msg": "the remote went away"})
    logged = "\n".join([went_away, _totals(checks=40, transfers=6, errors=1)])
    outcome = _run_files(cfg, _answering(logged, returncode=5))

    assert not outcome.ran
    assert "the remote went away" in outcome.detail, outcome.detail
    assert "transfers" not in outcome.detail and "{" not in outcome.detail, outcome.detail
    assert outcome.comparison["sent"] == 6, outcome.comparison

    plain = _run_files(cfg, _answering("connection refused", returncode=5))
    assert plain.detail.endswith("connection refused"), plain.detail

    mixed = _run_files(
        cfg, _answering(logged + "\npanic: the program died outside its logger", returncode=2)
    )
    assert "the remote went away" in mixed.detail, mixed.detail
    # A plain line after a page of JSON is why the run died.
    assert mixed.detail.endswith("panic: the program died outside its logger"), mixed.detail


def test_a_portion_with_no_mirror_carries_no_comparison(cfg, real_rclone):
    config.state_path("rekordbox_db", cfg).write_bytes(b"database")
    narrowed = _only(backup.plan_backup(cfg, now=MOMENT), backup_facts.Portion.DATABASE)
    (outcome,) = backup.run_backup(cfg, narrowed, runner=_answering(""), now=MOMENT).portions

    assert outcome.ran and outcome.comparison is None
    whole = backup.BackupOutcome(stamp=narrowed.stamp, portions=(outcome,))
    (row,) = backup.outcome_payload(whole)["portions"]
    assert row["comparison"] is None


def _full_age(cfg, *, now: datetime = MOMENT) -> backup_facts.PortionAge:
    return backup_facts.full_comparison_age(cfg, now=now)


def test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison(cfg, real_rclone):
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED

    _run_files(cfg, _answering(_totals(checks=1)))
    # A fast run records no full comparison, or doctor would say one ran.
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED
    assert backup_facts.read_facts(cfg)[backup_facts.Portion.FILES].completed_at == MOMENT

    narrowed = _only(backup.plan_backup(cfg, now=MOMENT, full=True))
    backup.run_backup(cfg, narrowed, runner=_answering(_totals(checks=1)), now=MOMENT)
    assert _full_age(cfg).completed_at == MOMENT

    # A later fast run, the database portion with it, neither moves nor erases it.
    later = MOMENT + timedelta(days=3)
    fast = backup.plan_backup(cfg, now=later)
    backup.run_backup(cfg, fast, runner=_answering(_totals(checks=1)), now=later)
    held = _full_age(cfg, now=later)
    assert held.completed_at == MOMENT and held.age == timedelta(days=3), held
    assert backup_facts.read_facts(cfg)[backup_facts.Portion.FILES].completed_at == later


def test_a_full_mirror_that_failed_or_only_rehearsed_records_nothing(cfg, real_rclone):
    narrowed = _only(backup.plan_backup(cfg, now=MOMENT, full=True))

    backup.run_backup(cfg, narrowed, runner=_answering("", returncode=5), now=MOMENT)
    backup.run_backup(cfg, narrowed, runner=_answering(""), now=MOMENT, dry_run=True)

    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED


def _record(cfg, portion=backup_facts.Portion.FILES, *, at=MOMENT, where="somewhere", **kwargs):
    backup_facts.record(cfg, portion, completed_at=at, destination=where, **kwargs)


def _fact_file(**extra) -> str:
    """A fact file holding one files portion completed at ``MOMENT``."""
    files = {"completed_at": MOMENT.isoformat(), "destination": "remote:mirror"}
    return json.dumps({"schema_version": 1, "portions": {"files": files}, **extra})


def test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison(cfg):
    """An older build's backups were all full; a fast record carries that date on."""
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_fact_file())
    assert _full_age(cfg).completed_at == MOMENT

    later = MOMENT + timedelta(days=2)
    _record(cfg, at=later, where="remote:mirror")

    written = json.loads(path.read_text())
    assert written[backup_facts.FULL_COMPARISON_KEY]["completed_at"] == MOMENT.isoformat()
    assert _full_age(cfg, now=later).age == timedelta(days=2)


def test_a_build_with_two_modes_always_writes_the_key(cfg):
    """Null included, because the key's absence is what marks an older build."""
    _record(cfg, backup_facts.Portion.DATABASE)
    written = json.loads(backup_facts.path_for(cfg).read_text())
    assert backup_facts.FULL_COMPARISON_KEY in written
    assert written[backup_facts.FULL_COMPARISON_KEY] is None

    _record(cfg)
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED


def test_a_damaged_full_comparison_entry_refuses_its_own_reader_and_no_other(cfg):
    """The entry feeds one informational line and never the portions' ages."""
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    for held in ("yesterday", {"completed_at": "2026-08-29T12:00:00"}, {"completed_at": 7}):
        path.write_text(_fact_file(**{backup_facts.FULL_COMPARISON_KEY: held}))
        with pytest.raises(backup_facts.BackupFactsUnreadable):
            _full_age(cfg)
        assert _finding(cfg, now=MOMENT).status is doctor.Status.FAIL
        assert backup_facts.read_facts(cfg)[backup_facts.Portion.FILES].completed_at == MOMENT
        (files, _) = backup_facts.ages(cfg, now=MOMENT)
        assert files.usable and files.age == timedelta(0), files

        _record(cfg, backup_facts.Portion.DATABASE, where="remote:database")
        # A record that was not a full comparison leaves the unreadable entry.
        assert json.loads(path.read_text())[backup_facts.FULL_COMPARISON_KEY] == held

    _record(cfg, where="remote:mirror", full_comparison=True)
    assert _full_age(cfg).completed_at == MOMENT


def _probes(now: datetime) -> doctor.Probes:
    return replace(doctor.Probes(), now=now)


def _finding(cfg, *, now: datetime):
    report = doctor.run(cfg, probes=_probes(now))
    (found,) = [f for f in report.findings if f.key == "backup.full_comparison"]
    return found


def test_doctor_says_how_long_ago_a_full_comparison_last_ran(cfg):
    never = _finding(cfg, now=MOMENT)
    assert never.status is doctor.Status.INFO
    assert "no backup here" in never.detail and "crate backup run --full" in never.detail

    _record(cfg, where="a-remote:mirror", full_comparison=True)
    recent = _finding(cfg, now=MOMENT + timedelta(days=9))
    assert recent.status is doctor.Status.INFO
    assert "9 days ago" in recent.detail and "a-remote:mirror" in recent.detail
    assert "--full" not in recent.detail

    day_before = _finding(cfg, now=MOMENT + timedelta(days=doctor.FULL_COMPARISON_DUE_DAYS - 1))
    assert "--full" not in day_before.detail
    due = _finding(cfg, now=MOMENT + timedelta(days=doctor.FULL_COMPARISON_DUE_DAYS))
    assert due.status is doctor.Status.INFO and "crate backup run --full" in due.detail


def test_a_record_a_few_minutes_ahead_is_zero_days_old_and_not_minus_one(cfg):
    """Inside the tolerance a record is a known age, and its days are negative."""
    _record(cfg, at=MOMENT + timedelta(minutes=10), full_comparison=True)
    report = doctor.run(cfg, probes=_probes(MOMENT))
    for key in ("backup.full_comparison", "backup.age.files"):
        (found,) = [f for f in report.findings if f.key == key]
        assert found.status is doctor.Status.INFO, found
        assert " 0 days ago" in found.detail and "-1" not in found.detail, found


def test_doctor_refuses_a_full_comparison_recorded_ahead_of_now(cfg):
    _record(cfg, at=MOMENT + timedelta(days=2), full_comparison=True)
    assert _finding(cfg, now=MOMENT).status is doctor.Status.FAIL


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def test_the_full_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume(cfg):
    """Both directions, through the real parser and the resume's argv builder."""
    code, envelope = _drive(["backup", "run", "--full", "--dry-run"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"][backup_cli.FULL] is True
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert job.payload == {
        backup_cli.DRY_RUN: True, backup_cli.FULL: True, backup_cli.CHECK: False,
        backup_cli.EMPTIED: False,
    }
    resumed = ["backup", "run", "--dry-run", "--full", "--job", job.job_id]
    assert backup_cli.backup_argv(job) == resumed

    code, envelope = _drive(["backup", "run"])
    assert envelope["data"]["progress"][backup_cli.FULL] is False
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert backup_cli.backup_argv(job) == ["backup", "run", "--job", job.job_id]


def test_the_frozen_mode_is_the_one_the_plan_is_built_in(cfg, real_rclone, monkeypatch):
    """The payload reaches the planner; each drive starts with no record, so is full."""
    from cratekit.modules.tools import backup_record

    _one_track(cfg)
    for payload, wanted in ((FAST, "fast"), (FULL, "full"), ({}, "fast")):
        backup_record.invalidate(backup_record.manifest_path())
        report = backup_cli.perform_backup(
            payload, portion=backup_facts.Portion.FILES, cfg=cfg,
            runner=_answering(_totals(checks=2, transfers=0)), now=MOMENT,
        )
        row = _files_portion(report)
        assert row["comparison"]["mode"] == wanted, (payload, row)
        (mirror,) = [c for c in row["commands"] if c["label"] == backup.MIRROR]
        assert (backup.FAST_LIST in mirror["argv"]) is (wanted == "fast")


def test_the_resumed_verb_says_what_the_comparison_did(cfg, real_rclone):
    """Queue, resume and read through the dispatcher, both items of the job run."""
    _seed(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation one")
    code, queued = _drive(["backup", "run"])
    assert code == int(ExitCode.OK), queued

    code, envelope = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), envelope

    recorded = envelope["data"]["progress"][backup_cli.OUTCOMES]["files"]
    said = _files_portion(recorded)["comparison"]
    assert said["mode"] == "fast" and said["sent"] == 3 and said["seconds"] > 0, said

    (warning,) = [w for w in envelope["warnings"] if w["code"] == backup_cli.COMPARISON]
    assert "fast mode" in warning["message"] and " sent 3 files" in warning["message"]
    assert "checked 0 files" in warning["message"], warning
    assert warning["message"].endswith("crate backup run --full"), warning


def test_a_resumed_rehearsal_never_says_that_it_sent(cfg, real_rclone, tmp_path):
    _seed(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation one")
    _, queued = _drive(["backup", "run", "--dry-run"])
    code, envelope = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), envelope

    (warning,) = [w for w in envelope["warnings"] if w["code"] == backup_cli.COMPARISON]
    assert "would have sent 3 files and sent none" in warning["message"], warning
    assert _held(_folder(tmp_path, cfg.backup.dest)) == {}


def _queued_said(envelope: dict) -> str:
    (said,) = [w for w in envelope["warnings"] if w["code"] == backup_cli.ALREADY_QUEUED]
    return said["message"]


def test_a_second_ask_in_the_other_mode_is_told_the_open_job_differs(cfg):
    """Both directions, and the same mode says nothing about modes."""
    _, first = _drive(["backup", "run"])
    code, second = _drive(["backup", "run", "--full"])
    assert code == int(ExitCode.OK), second
    assert second["data"]["job_id"] == first["data"]["job_id"], "a second job was filed"
    said = _queued_said(second)
    assert "will run the fast comparison" in said, said
    assert "this ask was for the full one" in said, said

    _, same = _drive(["backup", "run"])
    assert "comparison" not in _queued_said(same), same

    with jobs.open_store() as store:
        jobs.cancel(store, first["data"]["job_id"])
    _, full = _drive(["backup", "run", "--full"])
    assert full["data"]["job_id"] != first["data"]["job_id"], full
    _, fast = _drive(["backup", "run"])
    said = _queued_said(fast)
    assert "will run the full comparison" in said, said
    assert "this ask was for the fast one" in said, said


def test_the_sentence_never_prints_an_unread_number_as_zero():
    def outcomes(comparison):
        return {"files": {"portions": [{"portion": "files", "comparison": comparison}]}}

    (unread,) = backup_cli.comparison_warning(
        outcomes({"mode": "full", "seconds": None, "checked": None, "sent": None})
    )
    assert unread["message"].count("an unread number of files") == 2, unread
    assert "an unread number of seconds" in unread["message"], unread
    assert " 0 " not in unread["message"], unread
    assert unread["message"].endswith("crate backup run --check"), unread

    for unknown in (None, "quick", 7):
        assert backup_cli.comparison_warning(outcomes({"mode": unknown, "sent": 1})) == (), unknown

    assert backup_cli.comparison_warning(None) == ()
    assert backup_cli.comparison_warning({"database": {"portions": []}}) == ()
    assert backup_cli.comparison_warning(outcomes(None)) == ()


def test_a_failed_full_run_is_still_a_refusal(cfg, real_rclone):
    _one_track(cfg)
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            FULL, portion=backup_facts.Portion.FILES, cfg=cfg,
            runner=_answering("", returncode=5), now=MOMENT,
        )
    assert excinfo.value.cause.reason == "backup-transfer-failed"
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED
