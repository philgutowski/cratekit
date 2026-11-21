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
from dataclasses import replace
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

#: The real identity proof, taken before ``tests/conftest.py`` neutralizes it
#: for the test. The identity layer's own tests put it back.
REAL_IDENTITY_PROOF = backup._not_the_recorded_volume  # noqa: SLF001


def _remote(tmp_path: Path) -> Path:
    return tmp_path / "remotes" / "remote"


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())


@pytest.fixture(autouse=True)
def _the_machines_own_disk_is_never_read(monkeypatch):
    """U323: no test here asks the disk it runs on what volume it is.

    The identity proof falls back to the platform's provider and the kernel's
    mount table when a caller passes no seam. On a Mac the provider reads the
    temporary library's real volume UUID, which is never the fixture's recorded
    identity, so a backup a test meant as proven refused as foreign and mirrored
    nothing (A183's battery on 413c6bbd); on Linux it reads nothing and the
    same test passed. Each test states the identity it means instead, and a
    fallback reached here fails the test where it was reached. ``pytest.fail``
    is not an ``Exception``, so the proof's own catch of an unread identity
    cannot swallow it, and the teardown check holds should anything else.
    """
    reached: list[str] = []

    def fallback(name: str):
        def reach(*_args, **_kwargs):
            reached.append(name)
            pytest.fail(
                f"this test read the machine's own disk through preflight.{name}; "
                f"pass the identity_provider and mount_enumerator the test means"
            )

        return reach

    monkeypatch.setattr(
        preflight, "default_identity_provider", fallback("default_identity_provider")
    )
    monkeypatch.setattr(preflight, "local_mount_points", fallback("local_mount_points"))
    yield
    assert reached == [], f"the machine's own disk was read through {reached}"


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


def _on_the_recorded_volume(cfg):
    """The identity seams of a root that is the library's own volume."""
    return {
        "identity_provider": lambda path: cfg.library.volume_id,
        "mount_enumerator": lambda: (),
    }


def _first_backup(cfg, tmp_path, **identity):
    """Seed the library and back it up once, completed, onto an empty mirror.

    The identity is the test's to state (U323): by default the recorded volume,
    so the first backup never depends on what the machine's own disk reads; a
    test of another platform's answer passes that answer. A first backup that
    refuses or skips its files fails here, with its reason, rather than leaving
    a test to read an empty mirror as a history it never had.
    """
    _seed(cfg)
    plan, outcome = _backup(cfg, at=MOMENT, **(identity or _on_the_recorded_volume(cfg)))
    assert outcome.ok, outcome
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    assert _portion(outcome, FILES).ran, _portion(outcome, FILES)
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
    own entries are the history. The root holds a stray state folder, so it is
    the record and not an empty root that refuses."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().unlink()
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)
    _write(config.library_state_dir(cfg) / "lock.json", b"{}")

    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert "the record of the last completed backup held 12" in plan.portion(FILES).detail
    assert _remote_state(tmp_path) == remote


def test_a_record_kept_for_another_mirror_is_no_history(cfg, real_rclone, tmp_path):
    """The record answers only for its own root and mirror: one kept for
    another mirror leaves a state folder alone as a new library."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().unlink()
    manifest, _ = backup_record.read_manifest()
    backup_record.write_manifest(
        replace(cfg, backup=replace(cfg.backup, dest="remote:elsewhere")),
        manifest.excludes,
        manifest.entries,
        at=MOMENT,
        token=manifest.token,
    )
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()
    backup_facts.path_for(cfg).unlink()
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    (mirror,) = [c for c in plan.portion(FILES).commands if c.label == backup.MIRROR]
    assert backup._moves_nothing(mirror)  # noqa: SLF001


def test_with_no_census_or_record_the_librarys_own_fact_is_the_history(
    cfg, real_rclone, tmp_path
):
    """A library emptied on its own volume keeps its fact file, which is what
    a backup having happened looks like with installation state lost."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().unlink()
    backup_record.manifest_path().unlink()
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()

    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert "the library's own record of its backups held files" in plan.portion(FILES).detail

    backup_facts.path_for(cfg).write_text("{not json")
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN, (
        "a fact file that cannot be read is still a backup having happened"
    )


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


def test_a_census_that_cannot_be_read_as_a_file_is_a_backup_with_no_count(cfg):
    backup_record.census_path().parent.mkdir(parents=True, exist_ok=True)
    backup_record.census_path().mkdir()
    assert backup_record.read_census(cfg) == backup_record.Census(files=None)


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
    monkeypatch.setattr(backup, "_not_the_recorded_volume", REAL_IDENTITY_PROOF)


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
    """Every Linux volume reads as no identity; the census holds there. The
    platform reads none for the first backup as well, which is what kept the
    census this refusal stands on."""
    unread = {"identity_provider": lambda path: None, "mount_enumerator": lambda: ()}
    _first_backup(cfg, tmp_path, **unread)
    _unmount(cfg, tmp_path)
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=(), **unread)
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


def test_a_root_on_another_device_than_the_plan_read_fails_before_rclone_sync(
    cfg, real_rclone, tmp_path
):
    """The device half alone, with the library's files still in place: a
    volume swapped for another holding a copy is not the one walked."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    plan = backup.plan_backup(cfg, now=MOMENT + timedelta(hours=1), check=True, settings_dirs=())
    files = plan.portion(FILES)
    moved = replace(plan, portions=(replace(files, root_dev=files.root_dev + 1),))

    runner = Counting()
    outcome = backup.run_backup(cfg, moved, runner=runner, now=MOMENT + timedelta(hours=1))
    assert not _portion(outcome, FILES).ran
    assert "another volume" in _portion(outcome, FILES).detail
    assert backup.MIRROR not in runner.labels()
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
    for key, other in (("dest", "remote:elsewhere"), ("library_root", "/elsewhere")):
        moved = {**held, key: other}
        backup_record.census_path().write_text(json.dumps(moved))
        assert backup_record.read_census(cfg) is None, key
    backup_record.census_path().write_text(json.dumps(held))
    assert backup_record.read_census(cfg) == backup_record.Census(files=len(MUSIC))


def test_the_probe_reads_past_an_exclude_the_walk_cannot_translate(tmp_path):
    """A walk refused for an untranslatable exclude is where the probe stands
    in, so the probe must not refuse for the same reason."""
    root = tmp_path / "root"
    _write(root / ".cratekit" / "state.json", b"{}")
    assert backup_record.probe(root, ("/db/[master].db", ".DS_Store"), ".cratekit") == (
        True,
        0,
    )
    _write(root / "Music" / "a.flac", b"a")
    assert backup_record.probe(root, ("/db/[master].db",), ".cratekit") == (True, 1)
    _write(tmp_path / "empty" / ".DS_Store", b"")
    assert backup_record.probe(tmp_path / "empty", (".DS_Store",), ".cratekit") == (
        False,
        0,
    )


# ---------------------------------------------------------------------------
# Round one's findings, driven
# ---------------------------------------------------------------------------


def test_a_job_frozen_with_the_flag_and_driven_after_the_volume_went_refuses(
    cfg, real_rclone, tmp_path
):
    """Round one's B1: a job queued with the flag was handed to a plain ask
    and, driven after an unmount, emptied the mirror. The flag now passes only
    a root that still carries the library's own record of its backups."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)

    with pytest.raises(CratekitError) as excinfo:
        backup_cli.perform_backup(
            {backup_cli.EMPTIED: True}, now=MOMENT + timedelta(hours=1), portion=FILES
        )
    assert excinfo.value.cause.reason == "library-root-unproven"
    assert "does not carry" in excinfo.value.cause.message
    assert _remote_state(tmp_path) == remote
    assert not backup_facts.path_for(cfg).exists(), "a fact was published at the mount point"


def test_the_flag_reaches_the_plan_through_the_worker(cfg, real_rclone, tmp_path):
    _first_backup(cfg, tmp_path)
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()
    at = MOMENT + timedelta(hours=1)
    with pytest.raises(CratekitError):
        backup_cli.perform_backup({}, now=at, portion=FILES)
    backup_cli.perform_backup({backup_cli.EMPTIED: True}, now=at, portion=FILES)
    assert backup_record.read_census(cfg) == backup_record.Census(files=0)


def test_a_move_nothing_mirror_failing_for_another_reason_says_only_that(
    cfg, real_rclone, tmp_path
):
    """Round one's B2: the sentence about files on the remote is rclone's
    max-delete refusal's, and no other failure's."""
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    outcome = backup.run_backup(
        cfg, plan, runner=Counting(fail=backup.MIRROR), now=MOMENT
    )
    detail = _portion(outcome, FILES).detail
    assert "the remote went away" in detail
    assert "--library-emptied" not in detail and "holds files" not in detail, detail


def test_a_library_of_only_its_state_folder_skips_once_backed_up(cfg, real_rclone, tmp_path):
    """Round one's R1: the census of none makes the next run an ordinary one,
    so it skips when nothing changed and archives a state file that went."""
    state = config.library_state_dir(cfg)
    _write(state / "taxonomy.toml", b"[taxonomy]")
    _write(state / "notes.json", b"{}")
    _, first = _backup(cfg, at=MOMENT)
    assert _portion(first, FILES).ran

    _, second = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert _portion(second, FILES).kind == backup_facts.KIND_SKIPPED

    (state / "notes.json").unlink()
    _, third = _backup(cfg, at=MOMENT + timedelta(hours=2))
    assert _portion(third, FILES).ran, _portion(third, FILES)


@pytest.mark.parametrize("raised", [OSError("diskutil went away"), RuntimeError("psutil")])
def test_an_identity_read_that_raises_is_left_to_the_census(
    cfg, real_rclone, tmp_path, real_identity, raised
):
    """A read that raises is an unread identity, from the first backup on: it
    neither stops a backup of the library nor proves an unmounted root."""

    def broken(path):
        raise raised

    flaky = {"identity_provider": broken, "mount_enumerator": lambda: ()}
    _first_backup(cfg, tmp_path, **flaky)
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=(), **flaky)
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    _unmount(cfg, tmp_path)
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=(), **flaky)
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


def test_a_walk_that_refused_is_counted_so_the_floor_still_holds(cfg, real_rclone, tmp_path):
    """Round one's R2 (a): a name the walk refuses left the census with no
    count, and one stray file at the mount point then passed."""
    _seed(cfg)
    _write(cfg.library.root / "Music" / "line\nbreak.flac", b"x")
    plan, outcome = _backup(cfg, at=MOMENT)
    assert plan.portion(FILES).basis is None, "the walk did not refuse"
    assert plan.portion(FILES).held == len(MUSIC) + 1
    assert _portion(outcome, FILES).ran
    assert backup_record.read_census(cfg) == backup_record.Census(files=len(MUSIC) + 1)

    _unmount(cfg, tmp_path)
    _write(cfg.library.root / "stray.txt", b"stray")
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# ---------------------------------------------------------------------------
# Round two's findings, driven
# ---------------------------------------------------------------------------


def _a_database_fact_at_the_root(cfg) -> None:
    """What a refused job's database item leaves at a mount point when the
    database lives outside the root: a fact file holding a database fact."""
    backup_facts.record(
        cfg,
        DATABASE,
        completed_at=MOMENT,
        destination=str(cfg.backup.db_dest_root),
        kind=backup_facts.KIND_SNAPSHOT,
    )


def test_a_census_of_none_still_deletes_nothing_from_a_mirror_holding_files(
    cfg, real_rclone, tmp_path
):
    """Round two's B3: a library first backed up holding nothing, then a mirror
    that failed part way after its tracks arrived, then the volume lost. The
    census says none, so nothing refuses, and the full sync must still delete
    nothing from the mirror it would empty."""
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")
    _, first = _backup(cfg, at=MOMENT)
    assert _portion(first, FILES).ran
    assert backup_record.read_census(cfg) == backup_record.Census(files=0)

    # The failed run's part: tracks on the mirror the census never counted,
    # and the record it removed before sending.
    for rel, data in MUSIC.items():
        _write(_remote(tmp_path) / "mirror" / rel, data)
    backup_record.invalidate(backup_record.manifest_path())
    remote = _remote_state(tmp_path)

    away = _unmount(cfg, tmp_path)
    (config.library_state_dir(cfg)).mkdir(parents=True)
    (config.library_state_dir(cfg) / "taxonomy.toml").write_bytes(
        (away / ".cratekit" / "taxonomy.toml").read_bytes()
    )
    _a_database_fact_at_the_root(cfg)

    plan, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1))
    files = plan.portion(FILES)
    (mirror,) = [c for c in files.commands if c.label == backup.MIRROR]
    assert backup._moves_nothing(mirror)  # noqa: SLF001
    assert not _portion(outcome, FILES).ran
    after = _remote_state(tmp_path)
    assert after["archive"] == {}, "a mirror file moved into the archive"
    for rel, data in remote["mirror"].items():
        assert after["mirror"].get(rel) == data, rel


def test_the_flag_needs_a_files_fact_and_not_just_the_fact_file(cfg, real_rclone, tmp_path):
    """Round two's N2: the fact file a database item writes at a mount point
    holds a database fact only, and passes no flag."""
    _first_backup(cfg, tmp_path)
    remote = _remote_state(tmp_path)
    _unmount(cfg, tmp_path)
    _a_database_fact_at_the_root(cfg)
    assert backup_facts.path_for(cfg).is_file()

    plan, _ = _backup(cfg, at=MOMENT + timedelta(hours=1), emptied=True)
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert "completed files backup" in plan.portion(FILES).detail
    assert _remote_state(tmp_path) == remote


def test_a_plain_ask_is_told_the_open_job_carries_the_flag():
    """The twin warning's second direction, which round two found unpinned."""

    class Job:
        job_id = "j2"
        payload = backup_cli.frozen_payload(False, emptied=True)

    warning = backup_cli._already_queued(  # noqa: SLF001
        Job(), None, asked_full=False, asked_check=False, asked_emptied=False
    )
    assert "It was asked with --library-emptied" in warning["message"], warning
    plain = backup_cli._already_queued(  # noqa: SLF001
        Job(), None, asked_full=False, asked_check=False, asked_emptied=True
    )
    assert "--library-emptied" not in plain["message"], plain
