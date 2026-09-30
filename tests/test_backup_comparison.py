"""R-757: the mirror's comparison, its two modes, and what the run says about it.

WHAT WAS SLOW, MEASURED ON THE AUTHOR'S LIBRARY ON 2026-09-29. The remote was
listed one folder at a time, 22,433 folders at the rate the remote's request
pacing allows. The local walk took 1.5 seconds and more checkers changed
nothing. The fix is one option that lists the remote in one recursive pass, and
both modes still compare every file by size and modification time.

WHY THE REAL PROGRAM IS DRIVEN HERE, where every other backup test uses a
stand-in. The claims below are about what rclone SENDS when handed the argv this
product builds, and a stand-in sends nothing: it would prove the argv contains
the words and not that a changed file travels. So the mirror is run for real,
between two temporary folders. rclone's own configuration is pointed at a
temporary file, so no account on this machine is read, and that file declares
each remote as an alias of a temporary folder, because the configuration
refuses a destination that is not spelled ``remote:path`` (R-345).

WHAT THAT CANNOT MEASURE, said here so nobody reads it as covered. A local
folder has no recursive listing, so between two of them the option is accepted
and changes nothing. These tests prove the two modes agree on what to send and
that neither skips a changed file. That the recursive listing of a real remote
is complete is what the full mode and its doctor line exist to check, at an
attended sitting.

D1 APPLIES TO EVERY NAME HERE.
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


#: The remotes the temporary rclone configuration declares, each an alias of a
#: folder under the test's own temporary directory.
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
    """The rclone on this machine, ASSERTED present, reading no real account.

    Asserted rather than skipped, which is the rule ``tests/test_pending_units.py``
    enforces: a suite that skipped here would report green on a machine where
    none of the claims below was ever driven.
    """
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
    assert found is not None, (
        "rclone is not installed, so no test in this file can drive the mirror. "
        "It is a declared binary of the backup module"
    )
    return str(found)


def _configured(root: Path, remote: str, tmp_path: Path) -> config.Config:
    """A library at ``root`` whose three destinations are on the remote named."""
    (root / "Music").mkdir(parents=True, exist_ok=True)
    (root / "db").mkdir(parents=True, exist_ok=True)
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
                "remote": remote,
                "dest": f"{remote}:mirror",
                "archive_root": f"{remote}:archive",
                "db_dest_root": f"{remote}:database",
            },
        }
    )
    return built


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    built = _configured(root, "remote", tmp_path)
    config.save(built)
    config.reset_cache()
    return built


def _write(path: Path, content: bytes, *, at: datetime) -> None:
    """One file with a stated modification time, so no test races the clock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    stamp = at.timestamp()
    os.utime(path, (stamp, stamp))


def _seed(cfg) -> Path:
    """Three tracks in the library, and the folder they live in."""
    music = cfg.library.root / "Music"
    for name, content in (
        ("kept.flac", b"kept, generation one"),
        ("retagged.flac", b"genre: house...."),
        ("removed.flac", b"removed, generation one"),
    ):
        _write(music / name, content, at=MOMENT)
    return music


def _files_portion(report: dict) -> dict:
    (row,) = [r for r in report["portions"] if r["portion"] == "files"]
    return row


def _mirror(payload: dict, cfg, *, now: datetime, publish: bool = False) -> dict:
    """Run the FILES portion through the real program and return its rendered row.

    NOTHING IS PUBLISHED unless a test asks, and that is what makes the counts
    below exact. The fact file lives under the library root, so a run that
    publishes changes one file in the library it just mirrored, and the next run
    sends it. ``test_a_run_that_published_sends_its_own_record_next_time`` holds
    that, and every other drive here keeps it out of the count.
    """
    plan = backup.plan_backup(cfg, now=now, full=bool(payload.get(backup_cli.FULL)))
    narrowed = replace(plan, portions=(plan.portion(backup_facts.Portion.FILES),))
    outcome = backup.run_backup(
        cfg,
        narrowed,
        now=now,
        dry_run=bool(payload.get(backup_cli.DRY_RUN)),
        publish=publish,
    )
    return _files_portion(backup.outcome_payload(outcome))


def _held(folder: Path) -> dict[str, bytes]:
    """Every file under one folder, by relative path."""
    if not folder.is_dir():
        return {}
    return {
        str(path.relative_to(folder)): path.read_bytes()
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


# ---------------------------------------------------------------------------
# The argv, which is where the two modes differ and the only place they do
# ---------------------------------------------------------------------------


def _mirror_command(cfg, **kwargs) -> backup.Command:
    plan = backup.plan_backup(cfg, now=MOMENT, **kwargs)
    (found,) = [
        command
        for command in plan.portion(backup_facts.Portion.FILES).commands
        if command.label == backup.MIRROR
    ]
    return found


def test_the_two_modes_differ_by_the_listing_option_and_by_nothing_else(cfg, real_rclone):
    """The full mode is the fast one with one word removed.

    Asserted as a difference of the two argument lists rather than as two
    expected lists, because the property is that NOTHING ELSE differs: an
    exclude or the archive folder present in one mode and not the other would
    make the two send different things.
    """
    fast = list(_mirror_command(cfg).argv)
    full = list(_mirror_command(cfg, full=True).argv)

    assert backup.FAST_LIST in fast and backup.FAST_LIST not in full
    assert [word for word in fast if word != backup.FAST_LIST] == full
    assert backup.comparison_mode(_mirror_command(cfg)) == "fast"
    assert backup.comparison_mode(_mirror_command(cfg, full=True)) == "full"


@pytest.mark.parametrize("forbidden", ["--size-only", "--max-age", "--ignore-times", "--ignore-existing"])
def test_neither_mode_carries_an_option_that_can_skip_a_changed_file(
    cfg, real_rclone, forbidden
):
    """The candidates that were refused, held out of the command by name.

    A comparison by size alone skips a tag write that kept the file's length.
    A walk limited by age skips a file copied in with an old date and never
    sees a removal. Each would make the run faster and each skips a changed
    file, which the brief forbids whatever is chosen.
    """
    for full in (False, True):
        argv = _mirror_command(cfg, full=full).argv
        assert not any(word.startswith(forbidden) for word in argv), argv


# ---------------------------------------------------------------------------
# The four scenarios, through the real program
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("payload", [FAST, FULL], ids=["fast", "full"])
def test_nothing_changed_sends_nothing_and_says_so(cfg, real_rclone, payload, tmp_path):
    _seed(cfg)
    first = _mirror(payload, cfg, now=MOMENT)
    assert first["comparison"]["sent"] == 3, first

    second = _mirror(payload, cfg, now=MOMENT + timedelta(hours=1))

    said = second["comparison"]
    assert said["sent"] == 0, said
    assert said["compared"] == 3, (
        "a run that compared nothing also sends nothing, so the count of what "
        f"was compared is what makes a zero mean nothing changed: {said}"
    )
    assert isinstance(said["seconds"], float) and said["seconds"] > 0, said
    assert _held(_folder(tmp_path, cfg.backup.archive_root)) == {}


@pytest.mark.parametrize("payload", [FAST, FULL], ids=["fast", "full"])
def test_a_file_changed_in_content_and_not_in_size_is_sent(cfg, real_rclone, payload, tmp_path):
    """A tag write that keeps the file's length, which is the case that is skipped
    by any comparison trusting size alone.

    The two contents are the same length, asserted, and the modification time
    moves the way a write moves it.
    """
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


@pytest.mark.parametrize("payload", [FAST, FULL], ids=["fast", "full"])
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
    """One set of changes, made identically to two libraries, one run per mode.

    Two libraries rather than one run after the other, because the first run
    would leave the second nothing to send and they would agree on an empty set.
    """
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
        counts = {
            key: row["comparison"][key] for key in ("compared", "sent", "sent_bytes")
        }
        ended[name] = (
            counts,
            _held(_folder(tmp_path, one.backup.dest)),
            _held(_folder(tmp_path, one.backup.archive_root) / backup.stamp_for(later)),
        )

    assert ended["fast"] == ended["full"]
    assert ended["fast"][0]["sent"] == 2, ended["fast"]


def test_a_run_that_published_sends_its_own_record_next_time(cfg, real_rclone, tmp_path):
    """Why an unchanged library reports one file sent and not none.

    The fact file is library state and the mirror carries it, which is right:
    it is restored with the library. The cost is that the sentence a person
    reads never says zero after a real run. Recorded as a residual and held
    here so the number is explained by a test and not by a guess.
    """
    _seed(cfg)
    _mirror(FAST, cfg, now=MOMENT, publish=True)
    fact = backup_facts.path_for(cfg)
    assert cfg.library.root in fact.parents, "the fact file moved out of the library"

    later = MOMENT + timedelta(hours=1)
    row = _mirror(FAST, cfg, now=later, publish=True)

    assert row["comparison"]["sent"] == 1, row
    sent = _folder(tmp_path, cfg.backup.dest) / fact.relative_to(cfg.library.root)
    carried = json.loads(sent.read_text())["portions"]["files"]["completed_at"]
    assert carried == MOMENT.isoformat(), (
        "the record the second run sent is not the one the first run wrote"
    )


def test_a_rehearsal_counts_what_it_would_send_and_sends_nothing(cfg, real_rclone, tmp_path):
    _seed(cfg)
    row = _mirror({backup_cli.DRY_RUN: True}, cfg, now=MOMENT)

    assert row["comparison"]["sent"] == 3, row
    assert _held(_folder(tmp_path, cfg.backup.dest)) == {}


# ---------------------------------------------------------------------------
# The report, over a runner that answers what a test says it answers
# ---------------------------------------------------------------------------


def _answering(stderr: str, *, returncode: int = 0, elapsed: float | None = 12.5):
    def runner(command: backup.Command) -> backup.CommandResult:
        if command.label == backup.MIRROR:
            return backup.CommandResult(
                returncode=returncode, stderr=stderr, elapsed=elapsed
            )
        return backup.CommandResult(returncode=0)

    return runner


def _totals(**stats) -> str:
    return json.dumps({"level": "notice", "msg": "totals", "stats": stats})


def _run_files(cfg, runner, *, full: bool = False) -> backup.PortionOutcome:
    plan = backup.plan_backup(cfg, now=MOMENT, full=full)
    narrowed = replace(plan, portions=(plan.portion(backup_facts.Portion.FILES),))
    (outcome,) = backup.run_backup(cfg, narrowed, runner=runner, now=MOMENT).portions
    return outcome


def test_totals_that_could_not_be_read_are_none_and_never_zero(cfg, real_rclone):
    """A run whose totals were not found must not answer that it sent nothing."""
    outcome = _run_files(cfg, _answering("a line that is not a totals object\n"))

    assert outcome.ran
    said = dict(outcome.comparison)
    assert said["sent"] is None and said["compared"] is None, said
    assert said["seconds"] == 12.5 and said["mode"] == "fast", said

    untimed = _run_files(cfg, _answering(_totals(checks=4, transfers=1), elapsed=None))
    assert untimed.comparison["seconds"] is None and untimed.comparison["sent"] == 1


def test_the_last_totals_logged_are_the_ones_reported(cfg, real_rclone):
    """A run longer than the interval logs totals more than once."""
    logged = "\n".join(
        [_totals(checks=10, transfers=1), "not json", _totals(checks=40, transfers=6)]
    )
    outcome = _run_files(cfg, _answering(logged))

    assert outcome.comparison["compared"] == 40 and outcome.comparison["sent"] == 6


def test_a_failed_mirror_says_why_in_words_and_how_far_it_got(cfg, real_rclone):
    """The mirror logs JSON, and the tail of a JSON log is the totals object."""
    logged = "\n".join(
        [
            json.dumps({"level": "error", "msg": "the remote went away"}),
            _totals(checks=40, transfers=6, errors=1),
        ]
    )
    outcome = _run_files(cfg, _answering(logged, returncode=5))

    assert not outcome.ran
    assert "the remote went away" in outcome.detail, outcome.detail
    assert "transfers" not in outcome.detail and "{" not in outcome.detail, outcome.detail
    assert outcome.comparison["sent"] == 6, outcome.comparison

    plain = _run_files(cfg, _answering("connection refused", returncode=5))
    assert plain.detail.endswith("connection refused"), plain.detail


def test_a_portion_with_no_mirror_carries_no_comparison(cfg, real_rclone):
    config.state_path("rekordbox_db", cfg).write_bytes(b"database")
    plan = backup.plan_backup(cfg, now=MOMENT)
    narrowed = replace(plan, portions=(plan.portion(backup_facts.Portion.DATABASE),))
    (outcome,) = backup.run_backup(
        cfg, narrowed, runner=_answering(""), now=MOMENT
    ).portions

    assert outcome.ran and outcome.comparison is None
    (row,) = backup.outcome_payload(
        backup.BackupOutcome(stamp=plan.stamp, portions=(outcome,))
    )["portions"]
    assert row["comparison"] is None


# ---------------------------------------------------------------------------
# The fact, and doctor's reading of it
# ---------------------------------------------------------------------------


def _full_age(cfg, *, now: datetime = MOMENT) -> backup_facts.PortionAge:
    return backup_facts.full_comparison_age(cfg, now=now)


def test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison(cfg, real_rclone):
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED

    _run_files(cfg, _answering(_totals(checks=1)))
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED, (
        "a fast run recorded a full comparison, so doctor would say one ran"
    )
    assert backup_facts.read_facts(cfg)[backup_facts.Portion.FILES].completed_at == MOMENT

    plan = backup.plan_backup(cfg, now=MOMENT, full=True)
    narrowed = replace(plan, portions=(plan.portion(backup_facts.Portion.FILES),))
    backup.run_backup(cfg, narrowed, runner=_answering(_totals(checks=1)), now=MOMENT)
    assert _full_age(cfg).completed_at == MOMENT

    later = MOMENT + timedelta(days=3)
    fast = backup.plan_backup(cfg, now=later)
    backup.run_backup(cfg, fast, runner=_answering(_totals(checks=1)), now=later)
    held = _full_age(cfg, now=later)
    assert held.completed_at == MOMENT and held.age == timedelta(days=3), (
        "a later fast run, or the database portion beside it, moved or erased "
        f"the date of the last full comparison: {held}"
    )
    assert backup_facts.read_facts(cfg)[backup_facts.Portion.FILES].completed_at == later


def test_a_full_mirror_that_failed_or_only_rehearsed_records_nothing(cfg, real_rclone):
    plan = backup.plan_backup(cfg, now=MOMENT, full=True)
    narrowed = replace(plan, portions=(plan.portion(backup_facts.Portion.FILES),))

    backup.run_backup(cfg, narrowed, runner=_answering("", returncode=5), now=MOMENT)
    backup.run_backup(cfg, narrowed, runner=_answering(""), now=MOMENT, dry_run=True)

    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED


def test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison(cfg):
    """Every backup before this unit compared folder by folder.

    Their fact file has no key for it, and answering "never" over that file
    would tell a person whose every backup was a full one that none ever ran.
    The first fast record must then carry that date forward and not erase it.
    """
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "portions": {
                    "files": {
                        "completed_at": MOMENT.isoformat(),
                        "destination": "remote:mirror",
                    }
                },
            }
        )
    )
    assert _full_age(cfg).completed_at == MOMENT

    later = MOMENT + timedelta(days=2)
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=later, destination="remote:mirror"
    )

    written = json.loads(path.read_text())
    assert written[backup_facts.FULL_COMPARISON_KEY]["completed_at"] == MOMENT.isoformat()
    assert _full_age(cfg, now=later).age == timedelta(days=2)


def test_a_build_with_two_modes_always_writes_the_key(cfg):
    """Null included, because the key's absence is what marks an older build."""
    backup_facts.record(
        cfg, backup_facts.Portion.DATABASE, completed_at=MOMENT, destination="somewhere"
    )
    written = json.loads(backup_facts.path_for(cfg).read_text())
    assert backup_facts.FULL_COMPARISON_KEY in written
    assert written[backup_facts.FULL_COMPARISON_KEY] is None

    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=MOMENT, destination="somewhere"
    )
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED


def test_a_full_comparison_entry_that_cannot_be_read_refuses(cfg):
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    for held in ("yesterday", {"completed_at": "2026-08-29T12:00:00"}, {"completed_at": 7}):
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "portions": {},
                    backup_facts.FULL_COMPARISON_KEY: held,
                }
            )
        )
        with pytest.raises(backup_facts.BackupFactsUnreadable):
            _full_age(cfg)
        with pytest.raises(backup_facts.BackupFactsUnreadable):
            backup_facts.read_facts(cfg)


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

    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=MOMENT,
        destination="a-remote:mirror",
        full_comparison=True,
    )
    recent = _finding(cfg, now=MOMENT + timedelta(days=9))
    assert recent.status is doctor.Status.INFO
    assert "9 days ago" in recent.detail and "a-remote:mirror" in recent.detail
    assert "--full" not in recent.detail

    day_before = _finding(cfg, now=MOMENT + timedelta(days=doctor.FULL_COMPARISON_DUE_DAYS - 1))
    assert "--full" not in day_before.detail
    due = _finding(cfg, now=MOMENT + timedelta(days=doctor.FULL_COMPARISON_DUE_DAYS))
    assert due.status is doctor.Status.INFO and "crate backup run --full" in due.detail


def test_doctor_refuses_a_full_comparison_recorded_ahead_of_now(cfg):
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=MOMENT + timedelta(days=2),
        destination="somewhere",
        full_comparison=True,
    )
    assert _finding(cfg, now=MOMENT).status is doctor.Status.FAIL


# ---------------------------------------------------------------------------
# The flag, frozen and rebuilt, and the sentence a person reads
# ---------------------------------------------------------------------------


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def test_the_full_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume(cfg):
    """Both directions, through the real parser, for the reason the rehearsal
    flag's own test gives: a wrong ``dest`` freezes False for ever while the
    flag parses fine, and a builder that always emits the flag breaks the other
    half as completely.
    """
    code, envelope = _drive(["backup", "run", "--full", "--dry-run"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"][backup_cli.FULL] is True
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert job.payload == {backup_cli.DRY_RUN: True, backup_cli.FULL: True}
    assert backup_cli.backup_argv(job) == [
        "backup", "run", "--dry-run", "--full", "--job", job.job_id,
    ]

    code, envelope = _drive(["backup", "run"])
    assert envelope["data"]["progress"][backup_cli.FULL] is False
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert backup_cli.backup_argv(job) == ["backup", "run", "--job", job.job_id]


def test_the_frozen_mode_is_the_one_the_plan_is_built_in(cfg, real_rclone, monkeypatch):
    """The payload reaches the planner, asserted on the command that was run."""
    for payload, wanted in ((FAST, "fast"), (FULL, "full"), ({}, "fast")):
        report = backup_cli.perform_backup(
            payload,
            portion=backup_facts.Portion.FILES,
            cfg=cfg,
            runner=_answering(_totals(checks=2, transfers=0)),
            now=MOMENT,
        )
        row = _files_portion(report)
        assert row["comparison"]["mode"] == wanted, (payload, row)
        (mirror,) = [c for c in row["commands"] if c["label"] == backup.MIRROR]
        assert (backup.FAST_LIST in mirror["argv"]) is (wanted == "fast")


def test_the_resumed_verb_says_what_the_comparison_did(cfg, real_rclone):
    """End to end through the dispatcher and the real program: queue, resume, read.

    The database half is refused on purpose, by a rekordbox process that is not
    there being absent and a database file that is, so the job runs both items.
    """
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
    assert "fast mode" in warning["message"] and "sending 3 files" in warning["message"]
    assert warning["message"].endswith("crate backup run --full"), warning


def test_the_sentence_never_prints_an_unread_number_as_zero():
    def outcomes(comparison):
        return {"files": {"portions": [{"portion": "files", "comparison": comparison}]}}

    (unread,) = backup_cli.comparison_warning(
        outcomes({"mode": "full", "seconds": None, "compared": None, "sent": None})
    )
    assert "an unread number of files" in unread["message"], unread
    assert " 0 " not in unread["message"], unread
    assert unread["message"].endswith("crate backup run"), unread

    assert backup_cli.comparison_warning(None) == ()
    assert backup_cli.comparison_warning({"database": {"portions": []}}) == ()
    assert backup_cli.comparison_warning(outcomes(None)) == ()


def test_a_failed_full_run_is_still_a_refusal(cfg, real_rclone):
    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            FULL,
            portion=backup_facts.Portion.FILES,
            cfg=cfg,
            runner=_answering("", returncode=5),
            now=MOMENT,
        )
    assert excinfo.value.cause.reason == "backup-transfer-failed"
    assert _full_age(cfg).state is backup_facts.AgeState.NEVER_RECORDED
