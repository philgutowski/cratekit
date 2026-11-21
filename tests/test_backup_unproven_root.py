"""R-1761: a backup never treats a root it cannot prove is the library as the library.

THE DEFECT. An empty directory at the configured root, the mount point an
unmounted or lost drive can leave, was walked as a library with no files, and a
full check's ``rclone sync`` moved every file on the mirror into the run's dated
archive; a quick run planned the same as one move. Every test here drives the
real program between local folders, the way ``tests/test_backup_quick.py``
does, because the cost is what rclone does to the mirror and a stand in moves
nothing.

WHAT PROVES THE ROOT, decided at the plan of #893:

- the volume identity, when one is recorded and the platform reads one;
- a walk that holds files outside the library's own state folder, measured
  against the census the last completed backup kept in installation state,
  which a failed run does not remove the way it removes the record.

A refusal is a plan with no command, so nothing on the remote, in the record,
in the census or in either age moves. ``--library-emptied`` is the one way past
the second layer; the identity holds whatever it says.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.backup import cli as backup_cli
from cratekit.core import backup_facts, binaries, config, preflight
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup, backup_record

MOMENT = datetime(2026, 11, 1, 12, 0, 0, tzinfo=timezone.utc)
OLD = MOMENT - timedelta(days=30)
FILES = backup_facts.Portion.FILES
DATABASE = backup_facts.Portion.DATABASE
#: Every command that sends to, rewrites or moves off the mirror.
MOVERS = frozenset({backup.MIRROR, *backup.QUICK_LABELS})

#: The real assertion, taken before ``tests/conftest.py`` neutralizes it for
#: the test. The identity layer's own tests put it back.
REAL_ASSERT_LIBRARY_MOUNTED = preflight.assert_library_mounted


def _remote(tmp_path: Path) -> Path:
    return tmp_path / "remotes" / "remote"


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture
def real_rclone(monkeypatch, tmp_path) -> str:
    """The rclone on this machine, ASSERTED present, reading no real account."""
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
    root.mkdir()
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


def _write(path: Path, content: bytes, *, at: datetime = OLD) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    os.utime(path, (at.timestamp(), at.timestamp()))


MUSIC = {f"Music/track-{n:02}.flac": f"track {n}".encode() for n in range(12)}


def _seed(cfg) -> None:
    for rel, data in MUSIC.items():
        _write(cfg.library.root / rel, data)
    _write(config.state_path("rekordbox_db", cfg), b"database")


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


def _backup(cfg, *, at, runner=None, check=False, full=False, emptied=False, **seams):
    plan = backup.plan_backup(
        cfg, now=at, check=check, full=full, emptied=emptied, settings_dirs=(), **seams
    )
    outcome = backup.run_backup(cfg, plan, runner=runner or Counting(), now=at)
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


def _remote_state(tmp_path) -> dict[str, dict[str, bytes]]:
    """Everything on the remote: the mirror and every dated archive."""
    return {
        "mirror": _held(_remote(tmp_path) / "mirror"),
        "archive": _held(_remote(tmp_path) / "archive"),
    }


def _installation_state() -> dict[str, bytes | None]:
    """The record and the census, byte for byte, or None where absent."""
    out: dict[str, bytes | None] = {}
    for path in (backup_record.manifest_path(), backup_record.census_path()):
        out[path.name] = path.read_bytes() if path.is_file() else None
    return out


def _unmount(cfg, tmp_path) -> Path:
    """What an unmount leaves: the library moved away, an empty folder in its
    place. The library's own state folder, and the fact file in it, go with
    the volume."""
    away = tmp_path / "unplugged"
    cfg.library.root.rename(away)
    cfg.library.root.mkdir()
    return away


def _first_backup(cfg, tmp_path):
    _seed(cfg)
    _, outcome = _backup(cfg, at=MOMENT)
    assert outcome.ok, outcome
    assert len(_remote_state(tmp_path)["mirror"]) >= len(MUSIC)
    return outcome


# ---------------------------------------------------------------------------
# The defect, quick and full: an empty root with a backup on record refuses
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("asked", ["quick", "check", "full"])
def test_an_empty_root_with_a_completed_backup_on_record_refuses_and_moves_nothing(
    cfg, real_rclone, tmp_path, asked
):
    """THE DEFECT. Before the fix a full check moved all 12 mirror files into
    the dated archive and reset the files age; a quick run planned one move of
    every path. Now the files portion refuses before any command exists."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    installation = _installation_state()
    _unmount(cfg, tmp_path)

    later = MOMENT + timedelta(hours=1)
    runner = Counting()
    plan, outcome = _backup(
        cfg, at=later, runner=runner, check=asked == "check", full=asked == "full"
    )

    files = plan.portion(FILES)
    assert files.refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN, files
    assert files.commands == ()
    assert "12" in files.detail and "--library-emptied" in files.detail, files.detail
    assert [c for c in runner.ran if c.label in MOVERS] == [], runner.labels()
    assert _remote_state(tmp_path) == remote, "the refusal moved something on the remote"
    assert _installation_state() == installation, "the refusal touched the record or census"
    assert backup_facts.read_facts(cfg).get(FILES) is None, (
        "an age was published at the empty root"
    )
    assert not _portion(outcome, FILES).ran


def test_an_empty_root_after_a_failed_run_left_no_record_still_refuses(
    cfg, real_rclone, tmp_path
):
    """The record is removed before every transfer and a failed run leaves
    none, so the census, which no run removes, is what still says the library
    held files when the volume is then lost."""
    _first_backup(cfg, tmp_path)
    _write(cfg.library.root / "Music" / "new.flac", b"new")
    _, failed = _backup(
        cfg, at=MOMENT + timedelta(hours=1), runner=Counting(fail=backup.QUICK_SEND)
    )
    assert not _portion(failed, FILES).ran
    assert not backup_record.manifest_path().exists(), "a failed run kept its record"
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)

    runner = Counting()
    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=2), runner=runner)
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert runner.ran == [] or all(c.label not in MOVERS for c in runner.ran)
    assert _remote_state(tmp_path) == remote


def test_an_empty_root_with_only_the_record_on_record_refuses(cfg, real_rclone, tmp_path):
    """A record kept by a build before the census, and no census: the record's
    own entries are the history."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().unlink()
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)

    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert _remote_state(tmp_path) == remote


def test_a_damaged_census_counts_as_a_backup_having_happened(cfg, real_rclone, tmp_path):
    """Fail closed: a census that cannot be read says a backup was kept here,
    with a count nobody can read."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().write_bytes(b"{not json")
    backup_record.manifest_path().unlink()
    _unmount(cfg, tmp_path)
    # The state folder alone, as a lock or a log left at the mount point.
    _write(config.library_state_dir(cfg) / "stray.json", b"{}")

    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


def test_a_root_holding_nothing_at_all_refuses_with_no_history_anywhere(
    cfg, real_rclone, tmp_path
):
    """Not even the library's own state folder: no library Cratekit set up
    looks like this, whatever the installation remembers."""
    remote_before = {"mirror": {"Music/old.flac": b"old"}, "archive": {}}
    _write(_remote(tmp_path) / "mirror" / "Music" / "old.flac", b"old")

    runner = Counting()
    plan, outcome = _backup(cfg, at=MOMENT, runner=runner)
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert "not even" in plan.portion(FILES).detail
    assert all(c.label not in MOVERS for c in runner.ran)
    assert _remote_state(tmp_path) == remote_before


def test_a_mount_point_a_stray_file_landed_in_refuses_by_the_floor(cfg, real_rclone, tmp_path):
    """One file where twelve were: under a tenth of what the census holds."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)
    _write(cfg.library.root / "stray.txt", b"left by another program")

    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=1), check=True)
    files = plan.portion(FILES)
    assert files.refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN, files
    assert "a tenth" in files.detail
    assert _remote_state(tmp_path) == remote


def test_a_library_at_the_floor_still_backs_up(cfg, real_rclone, tmp_path):
    """Two of twelve is more than a tenth: a person who removed most of their
    library is backed up as before, and the archive keeps what went."""
    _first_backup(cfg, tmp_path)
    for rel in list(MUSIC)[2:]:
        (cfg.library.root / rel).unlink()

    plan, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    assert _portion(outcome, FILES).ran


def test_one_file_under_the_floor_refuses_and_one_at_it_runs(cfg, real_rclone, tmp_path):
    """The floor's edge, both sides: twenty files on record, one left is under
    a tenth and refuses, two left is a tenth and runs."""
    for n in range(20):
        _write(cfg.library.root / "Music" / f"t{n:02}.flac", b"x" * (n + 1))
    _backup(cfg, at=MOMENT)
    for n in range(2, 20):
        (cfg.library.root / "Music" / f"t{n:02}.flac").unlink()
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)

    (cfg.library.root / "Music" / "t01.flac").unlink()
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# ---------------------------------------------------------------------------
# The identity layer
# ---------------------------------------------------------------------------


@pytest.fixture
def real_identity(monkeypatch):
    """The identity assertion as shipped, which the suite neutralizes elsewhere."""
    monkeypatch.setattr(preflight, "assert_library_mounted", REAL_ASSERT_LIBRARY_MOUNTED)


def test_a_root_on_another_volume_refuses_before_the_walk(
    cfg, real_rclone, tmp_path, real_identity
):
    _seed(cfg)
    runner = Counting()
    plan, outcome = _backup(
        cfg,
        at=MOMENT,
        runner=runner,
        identity_provider=lambda path: "0000-1111",
        mount_enumerator=lambda: (),
    )
    files = plan.portion(FILES)
    assert files.refusal is backup.Refusal.LIBRARY_ROOT_FOREIGN, files
    assert "0000-1111" in files.detail
    assert all(c.label not in MOVERS for c in runner.ran)
    assert _remote_state(tmp_path)["mirror"] == {}


def test_the_identity_holds_whatever_the_flag_says(cfg, real_rclone, tmp_path, real_identity):
    _seed(cfg)
    plan = backup.plan_backup(
        cfg,
        now=MOMENT,
        only=FILES,
        settings_dirs=(),
        emptied=True,
        identity_provider=lambda path: "0000-1111",
        mount_enumerator=lambda: (),
    )
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_FOREIGN


def test_the_recorded_volume_at_the_root_backs_up(cfg, real_rclone, tmp_path, real_identity):
    _seed(cfg)
    plan, outcome = _backup(
        cfg, at=MOMENT, identity_provider=lambda path: "f1e2-d3c4", mount_enumerator=lambda: ()
    )
    assert plan.portion(FILES).refusal is None
    assert _portion(outcome, FILES).ran


def test_an_identity_the_platform_cannot_read_is_left_to_the_content(
    cfg, real_rclone, tmp_path, real_identity
):
    """Every Linux volume reads as no identity; the census holds there."""
    _first_backup(cfg, tmp_path)
    _unmount(cfg, tmp_path)
    plan = backup.plan_backup(
        cfg,
        now=MOMENT,
        only=FILES,
        settings_dirs=(),
        identity_provider=lambda path: None,
        mount_enumerator=lambda: (),
    )
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# ---------------------------------------------------------------------------
# The two ways a root with no music still backs up
# ---------------------------------------------------------------------------


def test_a_library_emptied_by_its_owner_backs_up_only_with_the_flag(cfg, real_rclone, tmp_path):
    _first_backup(cfg, tmp_path)
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()

    refused, _ = _backup(cfg, at=MOMENT + timedelta(hours=1), check=True)
    assert refused.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN, (
        "a full check asked for is not the override: an attended sitting runs one"
    )

    later = MOMENT + timedelta(hours=2)
    plan, outcome = _backup(cfg, at=later, emptied=True)
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    assert _portion(outcome, FILES).ran
    mirror = _remote_state(tmp_path)["mirror"]
    assert not any(rel in mirror for rel in MUSIC), "the emptied library's files stayed"
    archived = _held(_remote(tmp_path) / "archive" / backup.stamp_for(later))
    assert set(MUSIC) <= set(archived), "what the emptied run moved is not in its archive"

    # The census now says the library held nothing, so the next run over the
    # same empty library needs no flag.
    plan = backup.plan_backup(cfg, now=later + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)


def test_the_first_backup_of_a_new_empty_library_runs(cfg, real_rclone, tmp_path):
    """Set up and holding nothing but its state folder: no census, no record,
    no fact. It runs, as a full check that may move nothing off the mirror."""
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")

    plan, outcome = _backup(cfg, at=MOMENT)
    files = plan.portion(FILES)
    assert files.refusal is None, files
    assert files.kind == backup_facts.KIND_FULL
    (mirror,) = [c for c in files.commands if c.label == backup.MIRROR]
    assert "--max-delete" in mirror.argv
    assert mirror.argv[mirror.argv.index("--max-delete") + 1] == "0"
    assert _portion(outcome, FILES).ran, _portion(outcome, FILES)
    assert backup_record.read_census(cfg).files == 0


def test_a_new_empty_library_over_a_mirror_holding_files_moves_none_of_them(
    cfg, real_rclone, tmp_path
):
    """The no history case is the one the plan cannot tell from a lost volume
    with a stray state folder on a fresh installation, so rclone itself is
    told to move nothing, and the portion fails with the flag named."""
    _write(config.library_state_dir(cfg) / "lock.json", b"{}")
    for rel, data in MUSIC.items():
        _write(_remote(tmp_path) / "mirror" / rel, data)
    remote = _remote_state(tmp_path)

    _, outcome = _backup(cfg, at=MOMENT)
    files = _portion(outcome, FILES)
    assert not files.ran
    assert "--library-emptied" in files.detail, files.detail
    after = _remote_state(tmp_path)
    assert after["archive"] == {}, "a mirror file moved into the archive"
    for rel, data in remote["mirror"].items():
        assert after["mirror"].get(rel) == data, rel
    assert backup_facts.read_facts(cfg).get(FILES) is None


# ---------------------------------------------------------------------------
# Between the plan and the mirror
# ---------------------------------------------------------------------------


def test_a_volume_lost_between_the_plan_and_the_mirror_fails_before_rclone_sync(
    cfg, real_rclone, tmp_path
):
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), check=True, settings_dirs=())
    assert plan.portion(FILES).refusal is None
    _unmount(cfg, tmp_path)

    runner = Counting()
    outcome = backup.run_backup(cfg, plan, runner=runner, now=MOMENT + timedelta(hours=1))
    files = _portion(outcome, FILES)
    assert not files.ran
    assert backup.MIRROR not in runner.labels(), runner.labels()
    assert _remote_state(tmp_path) == remote


def test_a_root_emptied_on_the_same_volume_between_the_plan_and_the_mirror_fails(
    cfg, real_rclone, tmp_path
):
    """The device held and the files did not: the second half of the check."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), check=True, settings_dirs=())
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()

    runner = Counting()
    outcome = backup.run_backup(cfg, plan, runner=runner, now=MOMENT + timedelta(hours=1))
    assert not _portion(outcome, FILES).ran
    assert backup.MIRROR not in runner.labels()
    assert _remote_state(tmp_path) == remote


# ---------------------------------------------------------------------------
# Through the verb
# ---------------------------------------------------------------------------


def test_the_verb_refuses_with_the_reserved_remedy_and_leaves_the_ages(
    cfg, real_rclone, tmp_path
):
    _first_backup(cfg, tmp_path)
    ages = {e.portion: e.age for e in backup_facts.ages(cfg, now=MOMENT)}
    away = _unmount(cfg, tmp_path)

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup({}, now=MOMENT + timedelta(hours=1), portion=FILES)
    cause = excinfo.value.cause
    assert cause.reason == "library-root-unproven", cause.to_json()
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    joined = " ".join(cause.remediation.steps)
    assert "--library-emptied" in joined and "mount" in joined, joined

    # The library comes back: its own fact file says the age is untouched.
    cfg.library.root.rmdir()
    away.rename(cfg.library.root)
    assert {e.portion: e.age for e in backup_facts.ages(cfg, now=MOMENT)} == ages


def test_the_flag_is_frozen_in_the_payload_and_rebuilt_on_resume():
    payload = backup_cli.frozen_payload(False, check=False, emptied=True)
    assert payload[backup_cli.EMPTIED] is True

    class Job:
        job_id = "j1"

    job = Job()
    job.payload = payload
    assert "--library-emptied" in backup_cli.backup_argv(job)
    job.payload = backup_cli.frozen_payload(False)
    assert "--library-emptied" not in backup_cli.backup_argv(job)


def test_the_census_is_kept_for_its_root_and_mirror_only(cfg, real_rclone, tmp_path):
    _first_backup(cfg, tmp_path)
    held = json.loads(backup_record.census_path().read_text())
    assert held["files"] == len(MUSIC)
    held["dest"] = "remote:elsewhere"
    backup_record.census_path().write_text(json.dumps(held))
    assert backup_record.read_census(cfg) is None
