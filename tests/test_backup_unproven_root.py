"""R-1761: a backup never treats a root it cannot prove is the library as the library.

An empty directory at the root, what an unmounted drive leaves, was walked as a
library with no files, and a full check moved every mirror file into the dated
archive. The real program runs between local folders, as in
``tests/test_backup_quick.py``. The root is proved by the volume identity, where
recorded and readable, and by a walk holding files outside the state folder
against the last completed backup's census. A refusal is a plan with no command;
``--library-emptied`` passes the second layer only.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest

from cratekit.backup import cli as backup_cli
from cratekit.core import backup_facts, config, preflight
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup, backup_record
from tests.test_backup_comparison import _held, _saved
from tests.test_backup_quick import (
    DATABASE,
    FILES,
    MOMENT,
    Counting,
    _planned,
    _portion,
    _remote,
    _write,
)
from tests.test_backup_quick import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_backup_quick import real_rclone as real_rclone  # noqa: PLC0414

#: Every command that sends to, rewrites or moves off the mirror.
MOVERS = frozenset({backup.MIRROR, *backup.QUICK_LABELS})

#: The real identity proof, taken before ``tests/conftest.py`` neutralizes it.
REAL_IDENTITY_PROOF = backup._not_the_recorded_volume  # noqa: SLF001


@pytest.fixture(autouse=True)
def _the_machines_own_disk_is_never_read(monkeypatch):
    """U323: no test asks the disk it runs on what volume it is.

    On a Mac the real UUID made a proven backup refuse as foreign, so each test
    states its identity, and a fallback fails with ``pytest.fail``.
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
def cfg(tmp_path, monkeypatch):
    """An empty library root, what an unmounted volume leaves until a test fills it."""
    (tmp_path / "library").mkdir()
    return _saved(tmp_path, monkeypatch, folders=())


MUSIC = {f"Music/track-{n:02}.flac": f"track {n}".encode() for n in range(12)}


def _seed(cfg) -> None:
    for rel, data in MUSIC.items():
        _write(cfg.library.root / rel, data)
    _write(config.state_path("rekordbox_db", cfg), b"database")


def _backup(cfg, *, at, runner=None, check=False, full=False, emptied=False, **seams):
    plan = backup.plan_backup(
        cfg, now=at, check=check, full=full, emptied=emptied, settings_dirs=(), **seams
    )
    outcome = backup.run_backup(cfg, plan, runner=runner or Counting(), now=at)
    return plan, outcome


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
    """What an unmount leaves: an empty folder where the library and its state were."""
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
    """Seed the library and back it up once onto an empty mirror, on the test's
    identity (U323); a first backup that refuses fails here, with its reason."""
    _seed(cfg)
    plan, outcome = _backup(cfg, at=MOMENT, **(identity or _on_the_recorded_volume(cfg)))
    assert outcome.ok, outcome
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    assert _portion(outcome, FILES).ran, _portion(outcome, FILES)
    assert len(_remote_state(tmp_path)["mirror"]) >= len(MUSIC)
    return outcome


# The defect, quick and full: an empty root with a backup on record refuses


@pytest.mark.parametrize("asked", ["quick", "check", "full"])
def test_an_empty_root_with_a_completed_backup_on_record_refuses_and_moves_nothing(
    cfg, real_rclone, tmp_path, asked
):
    """The defect: the files portion refuses before any command exists, where a full
    check moved all 12 mirror files and a quick run planned one move of every path."""
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
    """A failed run leaves no record, so the census, which no run removes, still says
    the library held files when the volume is then lost."""
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
    """With no census the record's own entries are the history, so the record and not
    an empty root refuses."""
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
    """The record answers only for its own root and mirror, not another mirror's."""
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
    """A library emptied on its own volume keeps its fact file, so a backup happened."""
    _first_backup(cfg, tmp_path)
    backup_record.census_path().unlink()
    backup_record.manifest_path().unlink()
    for rel in MUSIC:
        (cfg.library.root / rel).unlink()

    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN
    assert "the library's own record of its backups held files" in plan.portion(FILES).detail

    backup_facts.path_for(cfg).write_text("{not json")
    assert _planned(cfg, MOMENT).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN, (
        "a fact file that cannot be read is still a backup having happened"
    )


def test_a_damaged_census_counts_as_a_backup_having_happened(cfg, real_rclone, tmp_path):
    """Fail closed: a census that cannot be read says a backup was kept here."""
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
    """Not even the library's own state folder: no library Cratekit set up looks so."""
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
    """Two of twelve is more than a tenth, so a mostly removed library backs up as before."""
    _first_backup(cfg, tmp_path)
    for rel in list(MUSIC)[2:]:
        (cfg.library.root / rel).unlink()

    plan, outcome = _backup(cfg, at=MOMENT + timedelta(hours=1))
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    assert _portion(outcome, FILES).ran


def test_one_file_under_the_floor_refuses_and_one_at_it_runs(cfg, real_rclone, tmp_path):
    """The floor's edge: of twenty on record, one left refuses and two left runs."""
    for n in range(20):
        _write(cfg.library.root / "Music" / f"t{n:02}.flac", b"x" * (n + 1))
    _backup(cfg, at=MOMENT)
    for n in range(2, 20):
        (cfg.library.root / "Music" / f"t{n:02}.flac").unlink()
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)

    (cfg.library.root / "Music" / "t01.flac").unlink()
    assert _planned(cfg, MOMENT).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# The identity layer


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
    """Every Linux volume reads as no identity, so the census holds there."""
    unread = {"identity_provider": lambda path: None, "mount_enumerator": lambda: ()}
    _first_backup(cfg, tmp_path, **unread)
    _unmount(cfg, tmp_path)
    assert _planned(cfg, MOMENT, **unread).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# The two ways a root with no music still backs up


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

    # The census now says the library held nothing, so the next run needs no flag.
    plan = backup.plan_backup(cfg, now=later + timedelta(hours=1), only=FILES, settings_dirs=())
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)


def test_the_first_backup_of_a_new_empty_library_runs(cfg, real_rclone, tmp_path):
    """Nothing but its state folder and no history: a full check that moves nothing off."""
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
    """The no history case looks like a lost volume with a stray state folder, so
    rclone is told to move nothing and the portion fails with the flag named."""
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


# Between the plan and the mirror


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
    """The device half alone: a volume swapped for one holding a copy is not the one walked."""
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


# Through the verb


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
    """The probe stands in for a refused walk, so it must not refuse for the same reason."""
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


# Round one's findings, driven


def test_a_job_frozen_with_the_flag_and_driven_after_the_volume_went_refuses(
    cfg, real_rclone, tmp_path
):
    """Round one's B1: the flag passes only a root carrying the library's own record,
    so a queued job driven after an unmount does not empty the mirror."""
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
    """Round one's B2: the files on the remote sentence is rclone's max-delete refusal's."""
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=())
    outcome = backup.run_backup(
        cfg, plan, runner=Counting(fail=backup.MIRROR), now=MOMENT
    )
    detail = _portion(outcome, FILES).detail
    assert "the remote went away" in detail
    assert "--library-emptied" not in detail and "holds files" not in detail, detail


def test_a_library_of_only_its_state_folder_skips_once_backed_up(cfg, real_rclone, tmp_path):
    """Round one's R1: after a census of none the next run is an ordinary one."""
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
    """A read that raises is an unread identity: it neither stops nor proves a backup."""

    def broken(path):
        raise raised

    flaky = {"identity_provider": broken, "mount_enumerator": lambda: ()}
    _first_backup(cfg, tmp_path, **flaky)
    plan = backup.plan_backup(cfg, now=MOMENT, only=FILES, settings_dirs=(), **flaky)
    assert plan.portion(FILES).refusal is None, plan.portion(FILES)
    _unmount(cfg, tmp_path)
    assert _planned(cfg, MOMENT, **flaky).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


def test_a_walk_that_refused_is_counted_so_the_floor_still_holds(cfg, real_rclone, tmp_path):
    """Round one's R2 (a): a name the walk refuses no longer leaves the census countless."""
    _seed(cfg)
    _write(cfg.library.root / "Music" / "line\nbreak.flac", b"x")
    plan, outcome = _backup(cfg, at=MOMENT)
    assert plan.portion(FILES).basis is None, "the walk did not refuse"
    assert plan.portion(FILES).held == len(MUSIC) + 1
    assert _portion(outcome, FILES).ran
    assert backup_record.read_census(cfg) == backup_record.Census(files=len(MUSIC) + 1)

    _unmount(cfg, tmp_path)
    _write(cfg.library.root / "stray.txt", b"stray")
    assert _planned(cfg, MOMENT).refusal is backup.Refusal.LIBRARY_ROOT_UNPROVEN


# Round two's findings, driven


def _a_database_fact_at_the_root(cfg) -> None:
    """What a refused job's database item leaves at a mount point: a database fact."""
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
    """Round two's B3: an empty first backup, a mirror failed part way, the volume
    lost; nothing refuses, and the full sync must still delete nothing."""
    _write(config.library_state_dir(cfg) / "taxonomy.toml", b"[taxonomy]")
    _, first = _backup(cfg, at=MOMENT)
    assert _portion(first, FILES).ran
    assert backup_record.read_census(cfg) == backup_record.Census(files=0)

    # The failed run's part: uncounted tracks on the mirror, and its removed record.
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
    """Round two's N2: a database item's fact file at a mount point passes no flag."""
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
