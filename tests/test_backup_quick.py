"""U317: a backup is skipped when nothing changed and sends only the change otherwise.

THE BRIEF'S SCENARIOS, DRIVEN THROUGH THE REAL PROGRAM. A quick run's claims are
about what rclone does with ``--files-from-raw -`` and ``--no-traverse``, so the
transfers run for real between temporary folders, the way
``tests/test_backup_comparison.py`` drives the full mirror and for its reason: a
stand in sends nothing, and would prove the argv holds the words and not that a
change arrives. rclone's configuration is a temporary file declaring each
remote an alias of a temporary folder, so no account on this machine is read.
Where a test needs a command to FAIL at a stated point, a runner wraps the real
one and answers that command itself.

THE FOUR MERGE BLOCKERS each have a test named for them: no skip while anything
changed, a quick run's remote holding every change it reports, no age after a
failed or partial run, and no read of the database unless both rekordbox
processes are confirmed gone.

WHAT THIS CANNOT MEASURE. A local folder answers ``--no-traverse`` lookups as
fast as a listing, so the speed the card is for is owed at an attended sitting
on the live remote, as is how a real remote counts a server side move.
"""

from __future__ import annotations

import gzip
import io
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.backup import cli as backup_cli
from cratekit.cli import doctor
from cratekit.core import backup_facts, binaries, config, processes
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup, backup_record

MOMENT = datetime(2026, 11, 1, 12, 0, 0, tzinfo=timezone.utc)
FILES = backup_facts.Portion.FILES
DATABASE = backup_facts.Portion.DATABASE


def _remote(tmp_path: Path) -> Path:
    return tmp_path / "remotes" / "remote"


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def real_rclone(monkeypatch, tmp_path) -> str:
    """The rclone on this machine, ASSERTED present, reading no real account.

    Asserted rather than skipped, for the reason ``tests/test_backup_comparison.py``
    gives: a skip would report green where none of this was driven.
    """
    monkeypatch.delenv("CRATEKIT_BIN_RCLONE", raising=False)
    declared = tmp_path / "rclone.conf"
    declared.write_text(f"[remote]\ntype = alias\nremote = {_remote(tmp_path)}\n")
    monkeypatch.setenv("RCLONE_CONFIG", str(declared))
    found = binaries.find("rclone")
    assert found is not None, (
        "rclone is not installed, so no test in this file can drive a backup. "
        "It is a declared binary of the backup module"
    )
    return str(found)


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir()
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
                "archive_root": "remote:archive",
                "db_dest_root": "remote:database",
            },
        }
    )
    config.save(built)
    config.reset_cache()
    return built


OLD = MOMENT - timedelta(days=30)


def _write(path: Path, content: bytes, *, at: datetime = OLD) -> None:
    """One file with a stated time, well outside the racy window unless asked."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    os.utime(path, (at.timestamp(), at.timestamp()))


def _seed(cfg) -> Path:
    music = cfg.library.root / "Music"
    _write(music / "kept.flac", b"kept, generation one")
    _write(music / "retagged.flac", b"genre: house")
    _write(music / "removed.flac", b"removed, generation one")
    _write(config.state_path("rekordbox_db", cfg), b"database, generation one")
    return music


class Counting:
    """The real runner, with every command it was handed kept in order."""

    def __init__(self, fail: str | None = None) -> None:
        self.ran: list[backup.Command] = []
        self.fail = fail

    def __call__(self, command: backup.Command) -> backup.CommandResult:
        self.ran.append(command)
        if command.label == self.fail:
            return backup.CommandResult(returncode=1, stderr="the remote went away")
        return backup.subprocess_runner(command)

    def labels(self) -> list[str]:
        return [command.label for command in self.ran]

    def fed(self, label: str, *, fact: bool = False) -> list[str]:
        """The paths one command was fed, the fact file left out unless asked.

        The fact file is written after the first backup's walk, so every quick
        run after it carries it too; the tests that are not about it read the
        rest.
        """
        (command,) = [c for c in self.ran if c.label == label]
        paths = (command.feed or "").splitlines()
        return paths if fact else [p for p in paths if not p.endswith("backup_facts.json")]


def _backup(cfg, *, at, runner=None, check=False, full=False, dry_run=False, only=None):
    plan = backup.plan_backup(
        cfg, now=at, check=check, full=full, only=only, settings_dirs=()
    )
    outcome = backup.run_backup(
        cfg, plan, runner=runner or Counting(), now=at, dry_run=dry_run
    )
    return plan, outcome


def _portion(outcome, which):
    (found,) = [p for p in outcome.portions if p.portion is which]
    return found


def _held(folder: Path) -> dict[str, bytes]:
    if not folder.is_dir():
        return {}
    return {
        path.relative_to(folder).as_posix(): path.read_bytes()
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


def _library_as_mirrored(cfg) -> dict[str, bytes]:
    """The library the mirror should hold: every file but the database set and
    the fact file, which every run rewrites after its transfer."""
    root = cfg.library.root
    leave = {backup_facts.path_for(cfg).relative_to(root).as_posix()}
    leave |= {p.relative_to(root).as_posix() for p in backup.database_fileset(cfg)}
    return {rel: data for rel, data in _held(root).items() if rel not in leave}


def _mirrored(cfg, tmp_path) -> dict[str, bytes]:
    held = _held(_remote(tmp_path) / "mirror")
    held.pop(backup_facts.path_for(cfg).relative_to(cfg.library.root).as_posix(), None)
    return held


def _ages(cfg, at) -> dict[str, timedelta | None]:
    return {str(entry.portion): entry.age for entry in backup_facts.ages(cfg, now=at)}


# ---------------------------------------------------------------------------
# Nothing changed: a skip, and both ages reset
# ---------------------------------------------------------------------------


def test_nothing_changed_is_a_skip_that_sends_nothing_and_resets_both_ages(cfg, real_rclone):
    _seed(cfg)
    _, first = _backup(cfg, at=MOMENT)
    assert first.ok
    assert _portion(first, FILES).kind == backup_facts.KIND_FULL
    assert _portion(first, DATABASE).kind == backup_facts.KIND_SNAPSHOT
    record = backup_record.manifest_path().read_bytes()

    later = MOMENT + timedelta(days=2)
    runner = Counting()
    plan, second = _backup(cfg, at=later, runner=runner)

    assert runner.ran == [], f"a skip ran {runner.labels()}"
    assert all(entry.will_run for entry in plan.portions)
    assert _portion(second, FILES).kind == backup_facts.KIND_SKIPPED
    assert _portion(second, DATABASE).kind == backup_facts.KIND_UNCHANGED
    assert second.ok and all(p.ran for p in second.portions)
    assert _ages(cfg, later) == {"files": timedelta(0), "database": timedelta(0)}
    assert backup_record.manifest_path().read_bytes() == record, (
        "a skip rewrote the record it was proved against"
    )
    facts = {f.portion: f for f in backup_facts.read_facts(cfg).values()}
    assert facts[FILES].kind == backup_facts.KIND_SKIPPED
    assert facts[DATABASE].kind == backup_facts.KIND_UNCHANGED


def test_the_fact_file_alone_changed_is_still_a_skip(cfg, real_rclone, tmp_path):
    """The one file a skip does not send, because every run rewrites it after
    its transfer and the remote's copy is a run behind under every kind."""
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    fact = backup_facts.path_for(cfg).relative_to(cfg.library.root).as_posix()
    assert backup_facts.path_for(cfg).is_file(), "the first run published no fact"
    assert fact not in backup_record.read_manifest()[0].entries, (
        "the fact file is written after the walk, so the first record cannot hold it"
    )

    _, second = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert _portion(second, FILES).kind == backup_facts.KIND_SKIPPED
    assert _portion(second, FILES).changes == {
        "added": 0, "changed": 0, "rewritten": 0, "removed": 0,
    }

    _write(cfg.library.root / "Music" / "added.flac", b"added")
    runner = Counting()
    _, third = _backup(cfg, at=MOMENT + timedelta(hours=2), runner=runner)
    assert _portion(third, FILES).kind == backup_facts.KIND_QUICK
    assert fact in runner.fed(backup.QUICK_SEND, fact=True), (
        "a quick run left the changed fact file behind when anything else was sent"
    )


# ---------------------------------------------------------------------------
# One file added, changed and removed: a quick run of only those
# ---------------------------------------------------------------------------


def test_an_added_a_changed_and_a_removed_file_are_a_quick_run_of_only_those(
    cfg, real_rclone, tmp_path
):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)

    _write(music / "added.flac", b"added")
    _write(music / "retagged.flac", b"genre: techno, longer", at=OLD + timedelta(days=1))
    (music / "removed.flac").unlink()

    later = MOMENT + timedelta(hours=1)
    runner = Counting()
    _, outcome = _backup(cfg, at=later, runner=runner)

    files = _portion(outcome, FILES)
    assert files.ran and files.kind == backup_facts.KIND_QUICK, files
    assert backup.MIRROR not in runner.labels(), "a quick run listed the remote"
    assert runner.fed(backup.QUICK_SEND) == ["Music/added.flac", "Music/retagged.flac"]
    assert runner.fed(backup.QUICK_ARCHIVE) == ["Music/removed.flac"]
    assert files.changes == {"added": 1, "changed": 1, "rewritten": 0, "removed": 1}
    # rclone's own count, which carries the fact file the first run wrote.
    assert files.comparison["sent"] == 3 and files.comparison["mode"] == "quick"

    # THE MERGE BLOCKER: the remote holds every change the run reports.
    assert _mirrored(cfg, tmp_path) == _library_as_mirrored(cfg)
    assert _held(_remote(tmp_path) / "archive" / backup.stamp_for(later)) == {
        "Music/retagged.flac": b"genre: house",
        "Music/removed.flac": b"removed, generation one",
    }, "what the quick run overwrote or removed is not in its dated archive"
    assert _ages(cfg, later)["files"] == timedelta(0)


def test_a_rewrite_that_kept_its_size_and_time_is_found_by_its_hash_and_sent(
    cfg, real_rclone, tmp_path
):
    """The racily clean file: written inside the walk's window, so the record
    hashed it, and rewritten keeping both its size and its time."""
    music = _seed(cfg)
    fresh = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    _write(music / "fresh.flac", b"first take", at=fresh)
    _backup(cfg, at=MOMENT)
    held = backup_record.read_manifest()[0].entries["Music/fresh.flac"]
    assert held.sha256 is not None, "a file inside the racy window was not hashed"

    _write(music / "fresh.flac", b"other take", at=fresh)
    runner = Counting()
    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1), runner=runner)

    assert _portion(outcome, FILES).kind == backup_facts.KIND_QUICK
    assert runner.fed(backup.QUICK_RESEND) == ["Music/fresh.flac"]
    assert "--ignore-times" in [c for c in runner.ran if c.label == backup.QUICK_RESEND][0].argv
    assert _mirrored(cfg, tmp_path)["Music/fresh.flac"] == b"other take"


def test_no_skip_while_anything_changed(cfg, real_rclone):
    """THE MERGE BLOCKER, over every kind of change the walk can see."""
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    changes = [
        lambda: _write(music / "new.flac", b"new"),
        lambda: _write(music / "kept.flac", b"kept, generation one", at=OLD + timedelta(seconds=1)),
        lambda: _write(music / "kept.flac", b"kept, generation two!", at=OLD + timedelta(seconds=1)),
        lambda: (music / "removed.flac").unlink(),
        lambda: _write(cfg.library.root / ".cratekit" / "history" / "note.json", b"{}"),
    ]
    for step, change in enumerate(changes, start=1):
        change()
        at = MOMENT + timedelta(hours=step)
        plan = backup.plan_backup(cfg, now=at, only=FILES, settings_dirs=())
        assert plan.portion(FILES).kind == backup_facts.KIND_QUICK, (step, plan)
        backup.run_backup(cfg, plan, runner=Counting(), now=at)


# ---------------------------------------------------------------------------
# A database change only: a snapshot only
# ---------------------------------------------------------------------------


def test_a_database_change_only_takes_a_snapshot_and_skips_the_files(
    cfg, real_rclone, tmp_path
):
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(config.state_path("rekordbox_db", cfg), b"database, generation two")

    later = MOMENT + timedelta(hours=1)
    runner = Counting()
    _, outcome = _backup(cfg, at=later, runner=runner)

    assert _portion(outcome, FILES).kind == backup_facts.KIND_SKIPPED
    assert _portion(outcome, DATABASE).kind == backup_facts.KIND_SNAPSHOT
    assert set(runner.labels()) == {backup.SNAPSHOT_DATABASE, backup.SNAPSHOT_IDENTITY}
    snapshot = _remote(tmp_path) / "database" / backup.stamp_for(later) / "db" / "master.db"
    assert snapshot.read_bytes() == b"database, generation two"
    assert _ages(cfg, later) == {"files": timedelta(0), "database": timedelta(0)}

    _, again = _backup(cfg, at=later + timedelta(hours=1))
    assert _portion(again, DATABASE).kind == backup_facts.KIND_UNCHANGED


def test_a_snapshot_whose_marker_failed_is_taken_again_next_time(cfg, real_rclone):
    """Round one's R2: an unmarked snapshot is not the one a restore takes."""
    _seed(cfg)
    _backup(cfg, at=MOMENT, runner=Counting(fail=backup.SNAPSHOT_IDENTITY))
    assert not backup_record.fingerprint_path().exists()
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=DATABASE, settings_dirs=())
    assert plan.portion(DATABASE).kind == backup_facts.KIND_SNAPSHOT


def test_the_second_reading_of_the_database_waits_on_a_second_scan(cfg, real_rclone):
    """Round one's R4: rekordbox started while the snapshot copied."""
    _seed(cfg)
    started = {"yes": False}

    class Starting(Counting):
        def __call__(self, command):
            if command.label == backup.SNAPSHOT_DATABASE:
                started["yes"] = True
            return super().__call__(command)

    hashed: list[Path] = []
    real_hash = backup_record._hash  # noqa: SLF001
    plan = backup.plan_backup(
        cfg, now=MOMENT, only=DATABASE, settings_dirs=(),
        process_lister=lambda: ("rekordboxAgent",) if started["yes"] else (),
    )
    import unittest.mock

    with unittest.mock.patch.object(
        backup_record, "_hash", lambda path: hashed.append(path) or real_hash(path)
    ):
        outcome = backup.run_backup(cfg, plan, runner=Starting(), now=MOMENT)
    database = _portion(outcome, DATABASE)
    assert database.ran
    assert hashed == [], "the database was read again with rekordbox running"
    assert not backup_record.fingerprint_path().exists()
    assert any(w["code"] == backup.BACKUP_RECORD_NOT_KEPT for w in database.warnings)


def test_a_sidecar_that_appeared_is_a_changed_database(cfg, real_rclone):
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    wal = config.state_path("rekordbox_db", cfg).with_name("master.db-wal")
    _write(wal, b"uncheckpointed")
    plan = backup.plan_backup(cfg, now=MOMENT, only=DATABASE, settings_dirs=())
    assert plan.portion(DATABASE).kind == backup_facts.KIND_SNAPSHOT


@pytest.mark.parametrize("scan", ["running", "unconfirmed"])
def test_no_read_of_the_database_unless_both_processes_are_confirmed_gone(
    cfg, real_rclone, monkeypatch, scan
):
    """THE MERGE BLOCKER. The fingerprint reads the database, so it sits below
    the process check, and neither a running nor an unconfirmed scan reaches it.

    The fingerprint is replaced by a recorder, and the database file itself is
    made unreadable to this process's own reads through ``open``, so a read
    reached by any other path would fail the drive too.
    """
    _seed(cfg)
    read: list[object] = []
    monkeypatch.setattr(
        backup_record, "database_fingerprint", lambda *a, **k: read.append(a) or "x"
    )
    hashed: list[Path] = []
    real_hash = backup_record._hash  # noqa: SLF001
    monkeypatch.setattr(
        backup_record, "_hash", lambda path: hashed.append(path) or real_hash(path)
    )

    def lister():
        if scan == "unconfirmed":
            raise processes._unconfirmed([(None, "the process table could not be read")])  # noqa: SLF001
        return ("rekordboxAgent",)

    plan = backup.plan_backup(
        cfg, now=MOMENT, only=DATABASE, settings_dirs=(), process_lister=lister
    )
    assert plan.portion(DATABASE).refusal in (
        backup.Refusal.REKORDBOX_RUNNING, backup.Refusal.REKORDBOX_ABSENCE_UNCONFIRMED,
    )
    assert read == [] and hashed == [], (
        "the database was read with rekordbox not confirmed gone"
    )


# ---------------------------------------------------------------------------
# A record missing, damaged or for another backup: a full run
# ---------------------------------------------------------------------------


def _damage(how: str, cfg) -> None:
    path = backup_record.manifest_path()
    if how == "missing":
        path.unlink()
    elif how == "corrupt":
        path.write_bytes(b"not gzip at all")
    else:
        data = json.loads(gzip.decompress(path.read_bytes()))
        if how == "older":
            data["schema_version"] = 0
        elif how == "another remote":
            data["dest"] = "elsewhere:mirror"
        elif how == "another volume":
            data["volume_id"] = "0000-0000"
        elif how == "other excludes":
            data["excludes"] = data["excludes"][1:]
        elif how == "a damaged entry":
            data["entries"]["Music/kept.flac"] = ["big", 0, None]
        elif how == "another library root":
            data["library_root"] = "/elsewhere"
        elif how == "another archive root":
            data["archive_root"] = "elsewhere:archive"
        elif how == "entries not a table":
            data["entries"] = [1]
        elif how == "no token":
            del data["token"]
        path.write_bytes(gzip.compress(json.dumps(data).encode()))
        if how == "a flipped byte":
            raw = bytearray(path.read_bytes())
            raw[len(raw) // 2] ^= 0xFF
            path.write_bytes(bytes(raw))


@pytest.mark.parametrize(
    "how",
    ["missing", "corrupt", "older", "another remote", "another volume", "other excludes",
     "a damaged entry", "another library root", "another archive root",
     "entries not a table", "no token", "a flipped byte"],
)
def test_a_record_missing_damaged_or_kept_for_another_backup_makes_a_full_run(
    cfg, real_rclone, how
):
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    _damage(how, cfg)

    runner = Counting()
    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1), runner=runner, only=FILES)
    files = _portion(outcome, FILES)
    assert files.kind == backup_facts.KIND_FULL and files.why, files
    assert backup.MIRROR in runner.labels()
    assert backup_record.read_manifest()[0] is not None, "the full run kept no record"


def test_a_run_by_another_installation_makes_the_next_run_full(cfg, real_rclone, tmp_path, monkeypatch):
    """Round one's B1: the mirror has writers that do not keep this record.

    A second installation backs up after a file was removed, archiving it off
    the mirror, and the file is then put back. This installation's record still
    holds it, so trusting the record would skip over a remote that lacks it.
    """
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    mine = os.environ["CRATEKIT_STATE_DIR"]

    (music / "removed.flac").unlink()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "second-installation"))
    _backup(cfg, at=MOMENT + timedelta(hours=1))
    monkeypatch.setenv("CRATEKIT_STATE_DIR", mine)
    _write(music / "removed.flac", b"removed, generation one")

    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=2))
    files = _portion(outcome, FILES)
    assert files.kind == backup_facts.KIND_FULL and "another installation" in files.why
    assert _mirrored(cfg, tmp_path) == _library_as_mirrored(cfg)


def test_a_failed_run_by_another_installation_makes_the_next_run_full(
    cfg, real_rclone, tmp_path, monkeypatch
):
    """Round two's finding: the other installation's run sent, then failed, so
    it published no fact for its token to be missing from. The token is struck
    from the library's fact when a run removes its own record, before it sends."""
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    mine = os.environ["CRATEKIT_STATE_DIR"]
    good = (music / "kept.flac").read_bytes()

    _write(music / "kept.flac", b"damaged", at=OLD + timedelta(days=5))
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "second-installation"))

    class SendsThenFails(Counting):
        def __call__(self, command):
            result = super().__call__(command)
            if command.label == backup.MIRROR:
                return backup.CommandResult(returncode=1, stderr="the remote filled up")
            return result

    _, failed = _backup(cfg, at=MOMENT + timedelta(hours=1), runner=SendsThenFails(), only=FILES)
    assert _portion(failed, FILES).ran is False
    assert _mirrored(cfg, tmp_path)["Music/kept.flac"] == b"damaged"
    monkeypatch.setenv("CRATEKIT_STATE_DIR", mine)
    _write(music / "kept.flac", good)

    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=3))
    files = _portion(outcome, FILES)
    assert files.kind == backup_facts.KIND_FULL, files
    assert _mirrored(cfg, tmp_path)["Music/kept.flac"] == good


def test_a_run_that_fails_strikes_the_token_from_the_library_fact(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    facts = backup_facts.read_facts(cfg)
    assert facts[FILES].summary[backup.RECORD_TOKEN]
    _write(music / "added.flac", b"added")
    _backup(cfg, at=MOMENT + timedelta(hours=1), runner=Counting(fail=backup.QUICK_SEND))
    facts = backup_facts.read_facts(cfg)
    assert backup.RECORD_TOKEN not in facts[FILES].summary
    assert facts[FILES].completed_at == MOMENT, "striking the token moved the age"


def test_a_fact_published_by_a_build_before_u317_makes_the_next_run_full(cfg, real_rclone):
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    backup_facts.record(
        cfg, FILES, completed_at=MOMENT + timedelta(hours=1), destination=str(cfg.backup.dest)
    )
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=2), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_FULL


def test_a_skip_carries_the_record_on_so_the_run_after_it_trusts_it(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _, skipped = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert _portion(skipped, FILES).kind == backup_facts.KIND_SKIPPED
    _write(music / "added.flac", b"added")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=2), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_QUICK


def test_the_last_full_check_eight_days_old_makes_a_full_run(cfg, real_rclone):
    _seed(cfg)
    _backup(cfg, at=MOMENT)

    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(days=6), settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_SKIPPED

    _, outcome = _backup(cfg, at=MOMENT + timedelta(days=8))
    files = _portion(outcome, FILES)
    assert files.kind == backup_facts.KIND_FULL and "8 days ago" in files.why, files
    assert _portion(outcome, DATABASE).kind == backup_facts.KIND_UNCHANGED, (
        "the weekly full check is the mirror's; an unchanged database is not copied"
    )
    check = backup_facts.full_check_age(cfg, now=MOMENT + timedelta(days=8))
    assert check.age == timedelta(0)


def test_a_quick_run_does_not_move_the_last_full_check(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")
    _, outcome = _backup(cfg, at=MOMENT + timedelta(days=3))
    assert _portion(outcome, FILES).kind == backup_facts.KIND_QUICK
    assert backup_facts.full_check_age(cfg, now=MOMENT + timedelta(days=3)).age == timedelta(days=3)
    assert backup_facts.full_check_due(
        backup_facts.full_check_age(cfg, now=MOMENT)
    ) == MOMENT + timedelta(days=backup_facts.FULL_CHECK_DAYS)


def test_the_check_flag_makes_a_full_run_and_a_snapshot_over_an_unchanged_library(
    cfg, real_rclone
):
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    for flags in ({"check": True}, {"full": True}):
        _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1), **flags)
        assert _portion(outcome, FILES).kind == backup_facts.KIND_FULL, flags
        assert _portion(outcome, DATABASE).kind == backup_facts.KIND_SNAPSHOT, flags


# ---------------------------------------------------------------------------
# A run that fails part way: no age, no record, and the next run full
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("fails", [backup.QUICK_ARCHIVE, backup.QUICK_SEND])
def test_a_quick_run_that_fails_midway_resets_no_age_and_leaves_no_record(
    cfg, real_rclone, fails
):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")
    (music / "removed.flac").unlink()

    later = MOMENT + timedelta(hours=3)
    _, outcome = _backup(cfg, at=later, runner=Counting(fail=fails), only=FILES)

    files = _portion(outcome, FILES)
    assert files.ran is False and files.kind == backup_facts.KIND_QUICK
    assert _ages(cfg, later)["files"] == timedelta(hours=3), "a failed run reset the age"
    assert backup_record.read_manifest()[0] is None, "a failed run left a record"

    runner = Counting()
    _, retried = _backup(cfg, at=later + timedelta(hours=1), runner=runner, only=FILES)
    assert _portion(retried, FILES).kind == backup_facts.KIND_FULL
    assert backup.MIRROR in runner.labels()


def test_a_full_run_that_fails_leaves_no_record_behind(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")
    _, outcome = _backup(
        cfg, at=MOMENT + timedelta(hours=1), runner=Counting(fail=backup.MIRROR), check=True
    )
    assert _portion(outcome, FILES).ran is False
    assert backup_record.read_manifest()[0] is None


def test_a_record_that_cannot_be_removed_stops_the_run_before_it_sends(
    cfg, real_rclone, monkeypatch
):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")

    def refuse(path):
        raise PermissionError(f"{path} is read only")

    monkeypatch.setattr(backup_record, "invalidate", refuse)
    runner = Counting()
    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1), runner=runner, only=FILES)
    files = _portion(outcome, FILES)
    assert files.ran is False and "could not be removed" in files.detail
    assert runner.ran == []
    assert _ages(cfg, MOMENT + timedelta(hours=1))["files"] == timedelta(hours=1)


def test_a_file_changed_while_the_transfer_ran_is_sent_again(cfg, real_rclone, tmp_path):
    """Both walks must agree for an entry to be trusted."""
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")

    class Meddling(Counting):
        def __call__(self, command):
            result = super().__call__(command)
            if command.label == backup.QUICK_SEND:
                _write(music / "kept.flac", b"kept, rewritten mid run", at=OLD + timedelta(days=2))
            return result

    _backup(cfg, at=MOMENT + timedelta(hours=1), runner=Meddling())
    assert backup_record.read_manifest()[0].entries["Music/kept.flac"] == backup_record.DOUBT

    runner = Counting()
    _backup(cfg, at=MOMENT + timedelta(hours=2), runner=runner)
    assert runner.fed(backup.QUICK_RESEND) == ["Music/kept.flac"], (
        "a doubt is resent with the times ignored, since a rewrite that kept its "
        "size and time would otherwise never be sent"
    )
    assert _mirrored(cfg, tmp_path)["Music/kept.flac"] == b"kept, rewritten mid run"


def test_a_doubt_rewritten_keeping_its_size_and_time_is_still_sent(cfg, real_rclone, tmp_path):
    """Round one's R1: the rewrite during the transfer put its time back.

    The file was just added, so its time is inside the racy window and both
    walks hash it; the hashes disagree, and the doubt that leaves must be sent
    with the times ignored. A file outside the window rewritten this way is
    invisible to any comparison of size and time, the full sync's included.
    """
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    fresh = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    _write(music / "added.flac", b"take one", at=fresh)

    class Meddling(Counting):
        def __call__(self, command):
            result = super().__call__(command)
            if command.label == backup.QUICK_SEND:
                _write(music / "added.flac", b"take two", at=fresh)
            return result

    _backup(cfg, at=MOMENT + timedelta(hours=1), runner=Meddling())
    _backup(cfg, at=MOMENT + timedelta(hours=2))
    assert _mirrored(cfg, tmp_path)["Music/added.flac"] == b"take two"


# ---------------------------------------------------------------------------
# What the walk cannot read is not absence
# ---------------------------------------------------------------------------


def _unlistable(monkeypatch, name: str) -> None:
    real = os.scandir

    def scandir(path):
        if Path(path).name == name:
            raise PermissionError(f"{path} cannot be listed")
        return real(path)

    monkeypatch.setattr(backup_record.os, "scandir", scandir)


def test_a_folder_that_cannot_be_listed_makes_a_full_run_and_never_an_archive(
    cfg, real_rclone, monkeypatch
):
    music = _seed(cfg)
    _write(music / "Crate" / "deep.flac", b"deep")
    _backup(cfg, at=MOMENT)
    _unlistable(monkeypatch, "Crate")

    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    files = plan.portion(FILES)
    assert files.kind == backup_facts.KIND_FULL and "could not be listed" in files.why
    assert backup.QUICK_ARCHIVE not in [c.label for c in files.commands]


def test_a_folder_gone_between_being_listed_and_being_read_makes_a_full_run(
    cfg, real_rclone, monkeypatch
):
    """Round one's B2: a volume unmounted under the walk is not every file on it removed."""
    music = _seed(cfg)
    _write(music / "Crate" / "deep.flac", b"deep")
    _backup(cfg, at=MOMENT)
    real = os.scandir

    def scandir(path):
        if Path(path).name == "Crate":
            raise FileNotFoundError(path)
        return real(path)

    monkeypatch.setattr(backup_record.os, "scandir", scandir)
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    files = plan.portion(FILES)
    assert files.kind == backup_facts.KIND_FULL and "was listed and then was not there" in files.why


@pytest.mark.parametrize(
    "after_the_plan", ["the path came back", "the root went away", "another volume"]
)
def test_a_removal_is_archived_only_while_the_walk_still_holds(
    cfg, real_rclone, tmp_path, after_the_plan, monkeypatch
):
    """Round one's B2, the plan to run half: the archive is asked again first."""
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    (music / "removed.flac").unlink()
    later = MOMENT + timedelta(hours=1)
    plan = backup.plan_backup(cfg, now=later, only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_QUICK
    root = cfg.library.root
    if after_the_plan == "the path came back":
        _write(music / "removed.flac", b"removed, generation one")
    elif after_the_plan == "the root went away":
        root.rename(root.with_name("library-unmounted"))
    else:
        _another_volume(monkeypatch, root)

    runner = Counting()
    outcome = backup.run_backup(cfg, plan, runner=runner, now=later)
    files = _portion(outcome, FILES)
    assert files.ran is False and "nothing was archived" in files.detail, files
    assert backup.QUICK_ARCHIVE not in runner.labels()
    assert "Music/removed.flac" in _mirrored(cfg, tmp_path)
    if after_the_plan == "the root went away":
        root.with_name("library-unmounted").rename(root)
    assert _ages(cfg, later)["files"] == timedelta(hours=1)


def _another_volume(monkeypatch, root: Path) -> None:
    """The root answers from another device, as a mount point does once unmounted."""
    real = os.stat

    class Moved:
        def __init__(self, status):
            self._status = status
            self.st_dev = status.st_dev + 1

        def __getattr__(self, name):
            return getattr(self._status, name)

    def stat(path, *args, **kwargs):
        found = real(path, *args, **kwargs)
        return Moved(found) if Path(path) == root else found

    monkeypatch.setattr(backup_record.os, "stat", stat)


def test_a_send_runs_only_while_the_root_is_the_volume_walked(
    cfg, real_rclone, tmp_path, monkeypatch
):
    """Round two's finding 4: an unmount after the plan with only an addition."""
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")
    later = MOMENT + timedelta(hours=1)
    plan = backup.plan_backup(cfg, now=later, only=FILES, settings_dirs=())
    _another_volume(monkeypatch, cfg.library.root)
    runner = Counting()
    outcome = backup.run_backup(cfg, plan, runner=runner, now=later)
    files = _portion(outcome, FILES)
    assert files.ran is False and "another volume" in files.detail, files
    assert runner.ran == []
    assert _ages(cfg, later)["files"] == timedelta(hours=1)


def test_a_name_holding_a_line_separator_is_one_path_to_the_archive_check(cfg):
    listed = backup_record.paths_list(["Music/Title\u2028Part.flac", "Music/b.flac"])
    assert backup_record.paths_from(listed) == ("Music/Title\u2028Part.flac", "Music/b.flac")


def test_an_excluded_system_folder_that_cannot_be_listed_is_never_entered(
    cfg, real_rclone, monkeypatch
):
    _seed(cfg)
    _write(cfg.library.root / ".Spotlight-V100" / "store.db", b"index")
    _backup(cfg, at=MOMENT)
    _unlistable(monkeypatch, ".Spotlight-V100")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_SKIPPED


def test_a_name_holding_a_line_break_makes_a_full_run(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "two\nlines.flac", b"odd")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_FULL
    assert "line break" in plan.portion(FILES).why


def test_the_walk_and_the_mirror_agree_on_what_the_library_holds(cfg, real_rclone, tmp_path):
    """The excludes and the symbolic link rule read the way rclone reads them: a
    full run over clutter, a link and the database leaves a record a second run
    finds unchanged, and the mirror holds exactly what the walk counted."""
    music = _seed(cfg)
    root = cfg.library.root
    _write(root / ".DS_Store", b"x")
    _write(music / ".DS_Store", b"x")
    _write(music / "._kept.flac", b"fork")
    _write(root / ".Trashes" / "501" / "gone.flac", b"trash")
    _write(root / "System Volume Information" / "x", b"x")
    (music / "link.flac").symlink_to(music / "kept.flac")
    _backup(cfg, at=MOMENT)

    walked = set(backup_record.read_manifest()[0].entries)
    fact = backup_facts.path_for(cfg).relative_to(root).as_posix()
    assert set(_mirrored(cfg, tmp_path)) == walked - {fact}
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_SKIPPED


def test_a_changed_name_in_decomposed_form_makes_a_full_run(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "Cafe\u0301.flac", b"decomposed")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_FULL
    assert "composed Unicode form" in plan.portion(FILES).why

    _write(music / "Caf\u00e9.flac", b"composed")
    (music / "Cafe\u0301.flac").unlink()
    _backup(cfg, at=MOMENT + timedelta(hours=2), check=True)
    _write(music / "Caf\u00e9.flac", b"composed, again")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=3), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_QUICK


def test_more_changes_than_a_quick_run_is_for_make_a_full_run(cfg, real_rclone, monkeypatch):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    monkeypatch.setattr(backup_record, "QUICK_LIMIT", 1)
    _write(music / "one.flac", b"1")
    _write(music / "two.flac", b"2")
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_FULL
    assert "more than the 1" in plan.portion(FILES).why


# ---------------------------------------------------------------------------
# A rehearsal plans the kind and keeps every record as it was
# ---------------------------------------------------------------------------


def test_a_rehearsal_of_a_quick_run_sends_nothing_and_keeps_the_record(cfg, real_rclone, tmp_path):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    record = backup_record.manifest_path().read_bytes()
    mirrored = _mirrored(cfg, tmp_path)
    _write(music / "added.flac", b"added")

    runner = Counting()
    _, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1), runner=runner, dry_run=True)

    assert _portion(outcome, FILES).kind == backup_facts.KIND_QUICK
    assert all("--dry-run" in c.argv for c in runner.ran if c.label in backup.QUICK_LABELS)
    assert runner.fed(backup.QUICK_SEND) == ["Music/added.flac"]
    assert backup_record.manifest_path().read_bytes() == record
    assert _mirrored(cfg, tmp_path) == mirrored


# ---------------------------------------------------------------------------
# The verb's report and doctor
# ---------------------------------------------------------------------------


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _run_verb(*flags: str) -> dict:
    code, queued = _drive(["backup", "run", *flags])
    assert code == int(ExitCode.OK), queued
    code, envelope = _drive(["backup", "run", "--job", queued["data"]["job_id"]])
    assert code == int(ExitCode.OK), envelope
    return envelope


def _kind_said(envelope) -> str:
    (said,) = [w for w in envelope["warnings"] if w["code"] == backup_cli.KIND]
    return said["message"]


def test_the_report_says_the_kind_what_changed_and_when_the_next_full_check_is_due(
    cfg, real_rclone
):
    music = _seed(cfg)
    first = _run_verb()
    assert _kind_said(first).startswith("this backup was a full check")
    (files_age,) = [a for a in first["data"]["ages"] if a["portion"] == "files"]
    due = files_age["full_check_due"]
    assert due is not None and due in _kind_said(first)

    second = _run_verb()
    said = _kind_said(second)
    assert said.startswith("this backup was a skip"), said
    assert "no new snapshot was taken" in said and "age was reset" in said

    _write(music / "added.flac", b"added")
    third = _run_verb()
    said = _kind_said(third)
    assert said.startswith("this backup was a quick run"), said
    assert "1 added, 0 changed, 0 rewritten, 0 removed" in said and "rclone sent 2" in said
    assert said.endswith("crate backup run --check")


def test_the_check_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume(cfg):
    code, envelope = _drive(["backup", "run", "--check", "--dry-run"])
    assert code == int(ExitCode.OK), envelope
    from cratekit.core import jobs

    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert job.payload[backup_cli.CHECK] is True
    assert backup_cli.backup_argv(job) == [
        "backup", "run", "--dry-run", "--check", "--job", job.job_id,
    ]


def test_doctor_names_the_last_run_and_the_next_full_check(cfg, real_rclone):
    music = _seed(cfg)
    _backup(cfg, at=MOMENT)
    _write(music / "added.flac", b"added")
    _backup(cfg, at=MOMENT + timedelta(days=1))

    from tests import doctor_machines

    inputs = doctor._Inputs(  # noqa: SLF001
        cfg, None, doctor_machines.green(now=MOMENT + timedelta(days=2))
    )
    files = doctor._check_backup_portion("backup.age.files", inputs)  # noqa: SLF001
    assert "a quick run" in files.detail and "1 added" in files.detail, files.detail
    check = doctor._check_full_check(inputs)  # noqa: SLF001
    assert "2 days ago" in check.detail, check.detail
    assert (MOMENT + timedelta(days=7)).date().isoformat() in check.detail, check.detail


def test_the_record_module_reads_files_and_writes_only_its_two_records():
    """Read off the source, as ``tests/test_analysis_store.py`` reads the backup
    module's: the walk hashes files, analysis files among them, and this module
    may author nothing but the two records, through the shared atomic writer.

    Every ``open`` is a binary read, and no call can create, copy, move or
    rename a file under the library.
    """
    import ast

    source = Path(backup_record.__file__).read_text()
    authoring = {
        "write_bytes", "write_text", "touch", "copy", "copy2", "copyfile",
        "copytree", "move", "replace", "rename", "mkdir", "rmtree", "chmod",
        "chown", "remove", "rmdir", "removedirs", "symlink_to", "hardlink_to",
        "link", "symlink", "utime", "truncate", "makedirs",
    }
    called: dict[str, list[ast.Call]] = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call):
            target = node.func
            name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
            called.setdefault(name, []).append(node)
    assert not (set(called) & authoring), sorted(set(called) & authoring)
    for call in called.get("open", []):
        assert [a.value for a in call.args if isinstance(a, ast.Constant)] == ["rb"], (
            ast.unparse(call)
        )
    writes = [ast.unparse(c) for c in called.get("atomic_write_bytes", [])]
    assert len(writes) == 2 and all(w.endswith(", path)") for w in writes), writes
    assert [ast.unparse(c) for c in called.get("unlink", [])] == ["path.unlink(missing_ok=True)"]


def test_the_kind_words_are_spelled_once_on_each_side_and_the_seconds_once():
    """The backup module and the fact file each hold the kind words, so a word
    added on one side cannot silently fail the other. A run's seconds are
    spelled by the fact file alone, for the shell and doctor both (U298)."""
    assert backup.KINDS == backup_facts.KINDS
    assert [backup_facts.took(seconds) for seconds in (None, True, 0, 0.4, 1, 41.6, 600)] == [
        "",
        "",
        " in under a second",
        " in under a second",
        " in 1 seconds",
        " in 42 seconds",
        " in 600 seconds",
    ]
    assert not hasattr(backup_cli, "_took")


def test_a_damaged_full_check_entry_never_refuses_the_ages(cfg, real_rclone):
    """``ages`` feeds the age a destructive session reads, so a damaged
    informational key is a reason for a full check and not a refusal."""
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    path = backup_facts.path_for(cfg)
    data = json.loads(path.read_text())
    data[backup_facts.FULL_CHECK_KEY] = "not an object"
    path.write_text(json.dumps(data))
    (files, _db) = backup_facts.ages(cfg, now=MOMENT)
    assert files.age == timedelta(0)
    assert files.full_check_due is None and "could not be read" in files.full_check_overdue
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).kind == backup_facts.KIND_FULL


@pytest.mark.parametrize("field", ["db_dest_root", "identity", "database"])
def test_a_fingerprint_taken_for_another_snapshot_is_not_compared(cfg, real_rclone, field):
    """The mutation table's zero row Q23: a fingerprint of the same database
    taken for another snapshot root, another library identity or another
    database path does not make this one unchanged."""
    _seed(cfg)
    _backup(cfg, at=MOMENT)
    path = backup_record.fingerprint_path()
    held = json.loads(path.read_text())
    held[field] = "elsewhere"
    path.write_text(json.dumps(held))
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), only=DATABASE, settings_dirs=())
    assert plan.portion(DATABASE).kind == backup_facts.KIND_SNAPSHOT
