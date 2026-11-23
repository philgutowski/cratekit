"""U8: the destructive-session boundary, its lock, and its acknowledgment.

One test per plan scenario (AE5, AE19, AE20, AE13, R29, R34), plus the backup
restore bound to the same gates (KTD24) and the runtime half of R17's fifth
surface. Everything is hermetic: volume identity, terminal probe, process
liveness and the database handle are injected.
"""

from __future__ import annotations

import contextlib
import inspect
import json
import os
import re
import stat
import subprocess
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import config, locations, preflight, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.tools import backup
from tests import _mounts
from tests.test_config import valid_data
from tests.test_restore import _refusal, _refusal_entering

UTC = timezone.utc

#: A foreign disk's identity; the fixture's own is read from the config.
_ELSEWHERE = "0000-0000-not-this-disk"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(
        valid_data(
            library,
            backup={
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        )
    )
    config.state_path("rekordbox_db", resolved).write_bytes(b"a database")
    return resolved


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


def matching_identity(cfg):
    """An identity provider that agrees with what the library recorded."""
    return lambda _path: cfg.library.volume_id


def foreign_identity(_path):
    return _ELSEWHERE


def open_gates(cfg, **overrides):
    """The real gates with only the volume identity seam injected."""
    arguments = {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}
    arguments.update(overrides)
    return arguments


@pytest.fixture
def volume_matches(cfg, monkeypatch):
    """Agree the platform's identity probe at the precondition seam, no gate seam."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


def acknowledge(cfg, **kwargs):
    """Mint an acknowledgment with the terminal check answered yes."""
    return session.record_acknowledgment(cfg, terminal=lambda: True, **kwargs)


def _gates_refusal(cfg, **arguments):
    """The cause the real gates refuse with, by default for a destructive workflow
    through the open seams, failing when they admit the session instead."""
    arguments = {"workflow": "a-destructive-workflow", **open_gates(cfg), **arguments}
    return _refusal_entering(session.assert_gates, cfg, **arguments)


@contextlib.contextmanager
def _umask(mask: int):
    """Run the body under ``mask``, since 022 hides a missing explicit mode."""
    previous = os.umask(mask)
    try:
        yield
    finally:
        os.umask(previous)


def _handle_recording(disposed: list[str]):
    """A database handle whose close and engine disposal are recorded in order."""

    class Engine:
        def dispose(self):
            disposed.append("engine")

    class Handle:
        session = object()
        engine = Engine()

        def close(self):
            disposed.append("session")

    return Handle


def state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root."""
    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        base = Path(root)
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                path = Path(current) / name
                try:
                    stat_result = path.stat()
                except OSError:  # pragma: no cover - vanished mid-walk
                    continue
                found[str(path)] = (stat_result.st_size, stat_result.st_mtime_ns)
    return found


# The three gates: three codes, and nothing written on any refused path


def test_the_three_refusals_carry_three_distinct_codes_and_write_nothing(cfg):
    """AE5 and AE19: three codes, and zero writes on every refused path."""
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())

    def refuse_with(**arguments):
        before = state_fingerprint(*roots)
        cause = _gates_refusal(cfg, **arguments)
        assert state_fingerprint(*roots) == before, "a refused session left a trace"
        return cause

    wrong_volume = refuse_with(
        identity_provider=foreign_identity, mount_enumerator=lambda: ()
    )
    assert wrong_volume.code is ExitCode.LIBRARY_UNAVAILABLE
    assert wrong_volume.reason == "library-volume-mismatch"

    no_acknowledgment = refuse_with(**open_gates(cfg))
    assert no_acknowledgment.code is ExitCode.ACK_REQUIRED
    assert no_acknowledgment.reason == "backup-acknowledgment-missing"

    acknowledge(cfg)
    contender = open(session.lock_path(cfg), "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        busy = refuse_with(**open_gates(cfg))
    finally:
        contender.close()
    assert busy.code is ExitCode.LIBRARY_BUSY
    assert busy.reason == "session-lock-held"

    assert len({wrong_volume.code, no_acknowledgment.code, busy.code}) == 3


def test_the_gates_admit_a_session_once_all_three_pass(cfg):
    acknowledge(cfg)
    with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)) as held:
        assert held.lock == session.lock_path(cfg)
        assert held.acknowledgment.actor
        assert held.volume.ok


def test_the_volume_is_judged_before_any_library_path_is_resolved(cfg):
    """The volume is judged first, or the lock is read off somebody else's disk."""
    acknowledge(cfg)
    cause = _refusal_entering(
        session.assert_gates,
        cfg,
        workflow="a-destructive-workflow",
        identity_provider=foreign_identity,
        mount_enumerator=lambda: (),
    )
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert not session.lock_path(cfg).exists(), "the lock was created before the volume check"


@pytest.mark.parametrize("state", sorted(preflight.MountState, key=str))
def test_every_mount_verdict_has_a_declared_refusal_slug(state):
    """P3: a new mount verdict with no slug fails here, not under a default code."""
    from cratekit.core.cause import REASONS

    if state is preflight.MountState.OK:
        assert state not in session._MOUNT_REASONS
        return
    slug = session._MOUNT_REASONS[state]
    assert REASONS[slug] is ExitCode.LIBRARY_UNAVAILABLE


# The volume gate, for every volume a prefix rule points at

_RECORDED_ELSEWHERE = "/recorded/on/another/machine"
_ARCHIVE = "AAAA-1111-the-archive"


@pytest.mark.parametrize("state", sorted(preflight.MountState, key=str))
def test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once(state):
    """A verdict is in exactly one of the pass and refusal tables."""
    from cratekit.core.cause import REASONS

    proved = state in session._MAPPED_PROVED
    refused = state in session._MAPPED_REASONS
    assert proved != refused
    if refused:
        assert REASONS[session._MAPPED_REASONS[state]] is ExitCode.LIBRARY_UNAVAILABLE


def test_the_verdicts_that_prove_a_rule_target_are_spelled_out():
    """The pass set as a literal, since widening it opens the gate.
    ``LIBRARY_PATH_MISSING`` passes because the identity matched."""
    assert session._MAPPED_PROVED == {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
    }


def test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing(cfg, tmp_path):
    """The third answer is None, since an empty mount-point directory sits on the
    library's boot disk and would match its identity."""
    root = Path(cfg.library.root)
    own = _rule(root / "Old", _ARCHIVE)
    inside = _rule(root / "Old")
    the_root_itself = _rule(root)
    beside = locations.PrefixRule(_RECORDED_ELSEWHERE, str(root) + "-archive")
    outside = _rule(tmp_path / "archive")

    assert session.expected_rule_identity(cfg, own) == _ARCHIVE
    assert session.expected_rule_identity(cfg, inside) == cfg.library.volume_id
    assert session.expected_rule_identity(cfg, the_root_itself) == cfg.library.volume_id
    assert session.expected_rule_identity(cfg, beside) is None, (
        "a directory whose NAME starts with the library root is not inside it"
    )
    assert session.expected_rule_identity(cfg, outside) is None


def _mapped(cfg, rules, **seams):
    return session.assert_mapped_volume_identities(cfg, rules, **seams)


def _rule(target, volume_id=None) -> locations.PrefixRule:
    """A rule recorded on another machine pointing at ``target``."""
    return locations.PrefixRule(_RECORDED_ELSEWHERE, str(target), volume_id)


def test_a_rule_onto_the_volume_it_recorded_passes(cfg, tmp_path, monkeypatch):
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)

    proved = _mapped(cfg, [_rule(archive, _ARCHIVE)])

    assert [status.state for status in proved] == [preflight.MountState.OK]
    assert proved[0].observed_identity == _ARCHIVE


def test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule(
    cfg, tmp_path, monkeypatch
):
    """R-44 Open 1: a decoy at the second rule refuses with its index."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: "BBBB-a-decoy"}, otherwise=cfg.library.volume_id)
    rules = [
        locations.PrefixRule("/an/older/root", str(Path(cfg.library.root) / "Music")),
        _rule(archive, _ARCHIVE),
    ]

    cause = _refusal(_mapped, cfg, rules)

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert cause.detail["rule"] == 1 and cause.detail["target"] == str(archive)
    assert cause.detail["recorded_identity"] == _ARCHIVE
    assert cause.detail["observed_identity"] == "BBBB-a-decoy"
    assert cause.remediation.remedy is None, (
        "the library volume's remedy is a false sentence about a mapped one"
    )
    assert "library.location_prefix_map[1]" in cause.remediation.steps[0]


def test_an_empty_directory_where_a_volume_mounts_is_not_that_volume(cfg, tmp_path, monkeypatch):
    """R-51: the empty directory an unclean eject leaves is not the volume."""
    stale = tmp_path / "Volumes" / "ARCHIVE"
    stale.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [_rule(stale, _ARCHIVE)])

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["state"] == str(preflight.MountState.FOREIGN_VOLUME)


def test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug(
    cfg, tmp_path, monkeypatch
):
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id)
    absent = tmp_path / "Volumes" / "ARCHIVE"

    cause = _refusal(_mapped, cfg, [_rule(absent, _ARCHIVE)])

    assert cause.reason == "mapped-volume-unmounted"
    assert str(absent) in cause.remediation.steps[0]


def test_a_recorded_volume_mounted_somewhere_else_says_where(cfg, tmp_path, monkeypatch):
    actually = tmp_path / "Volumes" / "ARCHIVE 1"
    actually.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {actually: _ARCHIVE}, otherwise=cfg.library.volume_id)
    configured = tmp_path / "Volumes" / "ARCHIVE"

    cause = _refusal(_mapped, cfg, [_rule(configured, _ARCHIVE)])

    assert cause.reason == "mapped-volume-mismatch"
    assert str(actually.resolve()) in cause.remediation.steps[0]


def test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity(
    cfg, tmp_path, monkeypatch
):
    """With nothing recorded, the refusal names the rule's config key and the
    identity the disk shows now, so the fix is one edit."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [_rule(archive)])

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["state"] == str(preflight.MountState.IDENTITY_NOT_RECORDED)
    assert cause.detail["observed_identity"] == _ARCHIVE
    step = cause.remediation.steps[0]
    assert _ARCHIVE in step and "library.location_prefix_map[0]" in step and "volume_id" in step


def test_a_volume_nested_under_the_library_root_is_not_the_library(cfg, monkeypatch):
    """Inside the root, the library's identity is asserted, not passed."""
    nested = Path(cfg.library.root) / "Archive"
    nested.mkdir()
    _mounts.stand_in(monkeypatch, {nested: "BBBB-nested"}, otherwise=cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [_rule(nested)])

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["recorded_identity"] == cfg.library.volume_id


def test_a_rule_target_whose_identity_cannot_be_read_refuses(cfg, tmp_path, monkeypatch):
    """Destructive strength. "I could not look" is not "it is the right disk"."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: None}, otherwise=cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [_rule(archive, _ARCHIVE)])

    assert cause.detail["state"] == str(preflight.MountState.IDENTITY_UNAVAILABLE)


def test_a_matched_volume_with_the_directory_absent_is_left_to_the_pass_that_follows_the_rule(
    cfg, tmp_path, monkeypatch
):
    """The one non-OK pass, and the reason is that the identity question was answered."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)
    rule = _rule(archive / "never-made", _ARCHIVE)

    proved = _mapped(cfg, [rule])

    assert [status.state for status in proved] == [preflight.MountState.LIBRARY_PATH_MISSING]


def test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it(
    cfg, tmp_path, monkeypatch
):
    """An empty mount slot refuses before any identity is compared, since a rule
    recording the slot's own disk would match the leftover directory (R-51)."""
    volumes = tmp_path / "Volumes"
    leftover = volumes / "ARCHIVE"
    leftover.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id, slots_under=volumes)
    rule = _rule(leftover, cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [rule])

    assert cause.reason == "mapped-volume-unmounted"
    assert cause.detail["state"] == "mount_slot_empty"


def test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record(
    cfg, tmp_path, monkeypatch
):
    """An ejected drive's refusal never offers the boot disk's identity to record,
    which would disarm the gate for good."""
    volumes = tmp_path / "Volumes"
    (volumes / "ARCHIVE").mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise="CCCC-the-boot-disk", slots_under=volumes)
    rule = _rule(volumes / "ARCHIVE")

    cause = _refusal(_mapped, cfg, [rule])

    assert cause.reason == "mapped-volume-unmounted"
    said = cause.message + " ".join(cause.remediation.steps) + json.dumps(cause.detail)
    assert "CCCC-the-boot-disk" not in said


def test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record(
    cfg, monkeypatch
):
    """Inside the root the identity compared was the library's, and the wording
    says so and offers no ``volume_id`` to record."""
    nested = Path(cfg.library.root) / "Archive"
    nested.mkdir()
    _mounts.stand_in(monkeypatch, {nested: "BBBB-nested"}, otherwise=cfg.library.volume_id)

    cause = _refusal(_mapped, cfg, [_rule(nested)])

    assert "the library's volume" in cause.message
    assert "recorded on that rule" not in cause.message
    assert "volume_id" not in cause.remediation.steps[0]


def test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback(
    cfg, tmp_path, monkeypatch
):
    """An untraversable path is a refusal, not an ``OSError`` traceback."""
    archive = tmp_path / "archive"
    archive.mkdir()

    def cannot_walk(_path):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(preflight, "identity_source", cannot_walk)

    cause = _refusal(_mapped, cfg, [_rule(archive, _ARCHIVE)])

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["state"] == "unreachable"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too(cfg, tmp_path):
    """The same finding at its second site, the read made while building the refusal."""
    archive = tmp_path / "archive"
    archive.mkdir()

    def provider(_path):
        raise PermissionError(13, "Permission denied")

    cause = _refusal(
        _mapped,
        cfg,
        [_rule(archive)],
        identity_provider=provider,
        mount_enumerator=lambda: (),
    )
    assert cause.detail["state"] == "unreachable"


def test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points(
    cfg, tmp_path, monkeypatch
):
    """A file is proved where it is: a volume mounted under the rule's target is a
    third disk. Both halves are asserted, since refuse-all passes the second."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    inner = archive / "Music" / "On Another Disk"
    inner.mkdir(parents=True)
    (archive / "Music" / "Here").mkdir()
    _mounts.stand_in(
        monkeypatch, {archive: _ARCHIVE, inner: "BBBB-inner"}, otherwise=cfg.library.volume_id
    )
    rules = [
        locations.PrefixRule("/an/older/root", str(Path(cfg.library.root) / "Music")),
        _rule(archive, _ARCHIVE),
    ]
    assert len(_mapped(cfg, rules)) == 2

    held = session.assert_mapped_file_volume(
        cfg, rules, 1, archive / "Music" / "Here" / "a.flac"
    )
    assert held.ok and held.observed_identity == _ARCHIVE

    cause = _refusal(session.assert_mapped_file_volume, cfg, rules, 1, inner / "a.flac")

    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["rule"] == 1 and cause.detail["probed"] == str(inner)
    assert cause.detail["observed_identity"] == "BBBB-inner"


def test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug(
    cfg, tmp_path, monkeypatch
):
    """The table is indexed, so an undecided state raises."""
    archive = tmp_path / "archive"
    archive.mkdir()
    undecided = {
        state: slug
        for state, slug in session._MAPPED_REASONS.items()
        if state is not preflight.MountState.FOREIGN_VOLUME
    }
    monkeypatch.setattr(session, "_MAPPED_REASONS", undecided)

    with pytest.raises(KeyError):
        _mapped(
            cfg,
            [_rule(archive, _ARCHIVE)],
            identity_provider=lambda _path: "BBBB-a-decoy",
            mount_enumerator=lambda: (),
        )


def test_the_seams_handed_in_are_the_seams_used(cfg, tmp_path):
    """An injected provider reaches the assertion, including the not-recorded read."""
    archive = tmp_path / "archive"
    archive.mkdir()
    seen: list[Path] = []

    def provider(path):
        seen.append(Path(path))
        return _ARCHIVE

    cause = _refusal(
        _mapped,
        cfg,
        [_rule(archive)],
        identity_provider=provider,
        mount_enumerator=lambda: (),
    )
    assert cause.detail["observed_identity"] == _ARCHIVE
    assert seen, "the refusal read the identity through some other provider"


# The lock


def test_a_second_process_refuses_and_names_the_holder(cfg):
    """AE19: the refusal names the holder."""
    with session.session_lock(cfg):
        recorded = session.read_lock_holder(session.lock_path(cfg))
        assert recorded is not None
        assert recorded.pid == os.getpid()
        assert recorded.host and recorded.boot and recorded.started

        # A separate handle is a second process to the kernel.
        session._HELD.discard(str(session.lock_path(cfg).absolute()))
        cause = _refusal_entering(session.session_lock, cfg)
    assert cause.code is ExitCode.LIBRARY_BUSY
    assert str(os.getpid()) in cause.message


def test_a_nested_session_is_a_programming_error_not_a_foreign_holder(cfg):
    """A nested session is a programming error, not a holder to wait for."""
    with session.session_lock(cfg):
        with pytest.raises(session.SessionComposition) as excinfo:
            with session.session_lock(cfg):
                pass
    cause = excinfo.value.cause
    assert cause.code is ExitCode.INTERNAL
    assert cause.reason != "session-lock-held"
    assert "nest" in cause.message


def test_the_lock_file_is_never_unlinked_and_is_private_under_any_umask(cfg):
    """Unlinking a lock lets a second process lock a fresh inode at the same name."""
    with _umask(0):
        with session.session_lock(cfg) as held:
            assert held.exists()
            assert stat.S_IMODE(held.stat().st_mode) == config.PRIVATE_FILE_MODE
            assert (
                stat.S_IMODE(held.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
            )
        assert held.exists(), "the lock file was unlinked on release"


def test_releasing_the_lock_clears_the_holder_so_the_next_run_is_not_told_to_wait(cfg):
    with session.session_lock(cfg):
        assert session.read_lock_holder(session.lock_path(cfg)) is not None
    assert session.read_lock_holder(session.lock_path(cfg)) is None


def test_releasing_a_dead_holders_lock_is_an_explicit_verb(cfg):
    """Never automatic. Clearing another run's claim mid-write is the failure."""
    lock = session.lock_path(cfg)
    lock.parent.mkdir(parents=True, exist_ok=True)
    dead = session.Holder(
        host=session.current_holder().host,
        boot=session.current_holder().boot,
        pid=os.getpid(),
        started="0.000",  # this process did not start at the epoch
    )
    lock.write_text(json.dumps({"holder": dead.to_json()}))

    assert session.holder_alive(dead) is False
    cleared = session.release_stale_lock(cfg)
    assert cleared == dead
    assert session.read_lock_holder(lock) is None


def test_releasing_a_live_holders_lock_refuses(cfg):
    with session.session_lock(cfg):
        cause = _refusal(session.release_stale_lock, cfg)
    assert cause.code is ExitCode.LIBRARY_BUSY


def test_a_holder_on_another_machine_or_another_boot_is_assumed_alive(cfg):
    """Fails towards alive, or one machine could clear another's claim mid delete."""
    here = session.current_holder()
    other_host = session.Holder(
        host="another-machine", boot=here.boot, pid=here.pid, started=here.started
    )
    other_boot = session.Holder(
        host=here.host, boot="0", pid=here.pid, started=here.started
    )
    assert session.holder_alive(other_host) is True
    assert session.holder_alive(other_boot) is True


def test_the_holder_carries_all_five_identifying_fields(cfg):
    """A bare process identifier is meaningless across machines and is reused."""
    holder = session.current_holder()
    assert {"host", "machine", "boot", "pid", "started"} == set(holder.to_json())
    assert session.Holder.from_json(holder.to_json()) == holder


def test_a_holder_recorded_before_the_machine_identity_reads_back_as_unknown(cfg):
    """A lock or record written by an earlier build names no machine, and says so."""
    legacy = {"host": "h", "boot": "100", "pid": 7, "started": "1.000"}
    assert session.Holder.from_json(legacy).machine == session.UNKNOWN_IDENTITY


def test_this_platform_names_its_machine_as_a_digest_not_the_serial(cfg):
    """The machine identity is a digest, never the serial, else the declared unknown."""
    machine = session.machine_identity()
    assert session.current_holder().machine == machine
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        assert re.fullmatch(r"[0-9a-f]{32}", machine), machine
    else:
        assert machine == session.UNKNOWN_IDENTITY or re.fullmatch(r"[0-9a-f]{32}", machine)


# ---------------------------------------------------------------------------
# A holder from an earlier boot of this machine (R-647)
# ---------------------------------------------------------------------------

#: A machine identity for the tests below, in the digest's shape.
THIS_MACHINE = "0123456789abcdef0123456789abcdef"


def _here() -> session.Holder:
    """This process, as a holder on a machine with a known identity and a numeric boot."""
    live = session.current_holder()
    return session.Holder(
        host=live.host, machine=THIS_MACHINE, boot="1000000", pid=live.pid, started=live.started
    )


def _before_a_power_loss(here: session.Holder, **changes) -> session.Holder:
    """A holder from this machine's previous boot, a day back, naming a real
    finished process so the platform is genuinely asked."""
    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    assert session.process_exists(finished.pid) is False
    fields = {
        "host": here.host,
        "machine": here.machine,
        "boot": str(float(here.boot) - 86400),
        "pid": finished.pid,
        "started": "900000.000",
    }
    fields.update(changes)
    return session.Holder(**fields)


def test_a_holder_from_an_earlier_boot_of_this_machine_is_gone(cfg):
    """No process survives a restart of its machine (R-647)."""
    here = _here()
    assert session.holder_alive(_before_a_power_loss(here), here=here) is False


@pytest.mark.parametrize(
    ("label", "changes"),
    [
        ("another machine with this host name", {"machine": "f" * 32}),
        ("recorded before the machine identity", {"machine": session.UNKNOWN_IDENTITY}),
        ("a boot inside the drift margin", {"boot": "999990"}),
        ("a boot exactly at the drift margin", {"boot": "999940"}),
        ("a later boot", {"boot": "1086400"}),
        ("a boot that is not a number", {"boot": "yesterday"}),
        ("a boot that is not finite", {"boot": "-inf"}),
    ],
)
def test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine(
    cfg, label, changes
):
    """Each cross boot condition fails alive, one row each from the gone holder.
    The host name is no proof, since a drive can move between same-named machines."""
    here = _here()
    assert session.holder_alive(_before_a_power_loss(here, **changes), here=here) is True, label


def test_a_boot_just_past_the_drift_margin_is_gone(cfg):
    """The margin is sixty seconds, pinned from both sides by this and the row above."""
    here = _here()
    assert session.BOOT_DRIFT_SECONDS == 60.0
    assert session.holder_alive(_before_a_power_loss(here, boot="999939"), here=here) is False


def test_two_unknown_machine_identities_are_not_one_machine(cfg):
    """Unknown on both sides compares equal as text, and proves nothing."""
    here = replace(_here(), machine=session.UNKNOWN_IDENTITY)
    gone = _before_a_power_loss(here)
    assert gone.machine == here.machine == session.UNKNOWN_IDENTITY
    assert session.holder_alive(gone, here=here) is True


def test_this_machine_with_no_identity_keeps_every_holder_from_another_boot(cfg):
    """An unknown on THIS side is as much a gap as one on the recorded side."""
    here = replace(_here(), machine=session.UNKNOWN_IDENTITY)
    gone = _before_a_power_loss(_here())
    assert session.holder_alive(gone, here=here) is True


def test_a_live_process_read_through_a_moved_clock_is_kept(cfg):
    """A live process keeps its claim when a moved clock moves the boot reading."""
    here = _here()
    moved = _before_a_power_loss(here, pid=here.pid, started=here.started)
    assert session.holder_alive(moved, here=here) is True


def test_a_live_process_whose_start_time_moved_with_the_clock_is_kept(cfg):
    """On Linux the start time moves with a stepped clock, so a live identifier keeps
    the claim whatever start time it reports."""
    here = _here()
    stepped = _before_a_power_loss(
        here, pid=here.pid, started=f"{float(here.started) - 86400:.3f}"
    )
    assert session.holder_alive(stepped, here=here) is True


def test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it(cfg, monkeypatch):
    """None is "will not say", and only a confident no may clear a claim."""
    here = _here()
    gone = _before_a_power_loss(here)
    monkeypatch.setattr(session, "process_exists", lambda pid: None)
    assert session.holder_alive(gone, here=here) is True


def test_the_lock_left_by_this_machines_earlier_boot_is_releasable(cfg, monkeypatch):
    """The release verb's lock half, through the same judgment and no other."""
    monkeypatch.setattr(session, "machine_identity", lambda: THIS_MACHINE)
    live = session.current_holder()
    dead = _before_a_power_loss(live)
    lock = _lock_recording(cfg, dead)

    assert session.release_stale_lock(cfg) == dead
    assert session.read_lock_holder(lock) is None


def test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable(
    cfg, monkeypatch
):
    """The drive moved, the other machine is writing, and its claim stands."""
    monkeypatch.setattr(session, "machine_identity", lambda: THIS_MACHINE)
    live = session.current_holder()
    theirs = _before_a_power_loss(live, machine="f" * 32)
    lock = _lock_recording(cfg, theirs)
    before = lock.read_bytes()

    cause = _refusal(session.release_stale_lock, cfg)
    assert cause.reason == "session-lock-held"
    assert lock.read_bytes() == before


# The acknowledgment (KTD18, R34)


def test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment(cfg):
    """The gate protecting the operation that removes files is not self-servable."""
    cause = _refusal(session.record_acknowledgment, cfg, terminal=lambda: False)
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.reason == "backup-acknowledgment-no-terminal"
    assert session.read_acknowledgment(cfg) is None


def test_the_terminal_check_is_a_terminal_check_and_not_a_standard_input_read():
    """R33: the terminal check reads no input, asserted structurally."""
    import ast

    from tests._split_modules import source_of

    # The session and its parts (U300): the terminal check lives in ``session_ack``.
    source = source_of("cratekit.core.session")
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            raise AssertionError("the session module names standard input")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"input", "raw_input"}


def test_the_recorded_actor_is_derived_from_the_invocation_and_never_supplied():
    """R34: no parameter can carry the actor, or an agent could sign another's name."""
    parameters = inspect.signature(session.record_acknowledgment).parameters
    assert not [name for name in parameters if "actor" in name.lower()]
    assert not [name for name in parameters if "user" in name.lower()]


def test_the_acknowledgment_records_the_backup_age_that_was_shown(cfg):
    """KTD18: the backup age shown is recorded for every declared portion."""
    from cratekit.core import backup_facts

    now = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=now - timedelta(days=2),
        destination="remote:mirror",
    )
    recorded = acknowledge(cfg, now=now)

    shown = {entry.portion: entry for entry in recorded.shown}
    assert set(shown) == {str(portion) for portion in backup_facts.Portion}
    assert shown[str(backup_facts.Portion.FILES)].age_seconds == timedelta(days=2).total_seconds()
    assert shown[str(backup_facts.Portion.DATABASE)].state == str(
        backup_facts.AgeState.NEVER_RECORDED
    )


def test_an_expired_acknowledgment_refuses_exactly_as_an_absent_one_does(cfg):
    now = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    acknowledge(cfg, now=now, validity=timedelta(hours=1))

    session.assert_backup_acknowledged(cfg, now=now + timedelta(minutes=30))
    cause = _refusal(session.assert_backup_acknowledged, cfg, now=now + timedelta(hours=2))
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.detail["expired"] is True


def test_the_acknowledgment_file_is_private_under_any_umask(cfg):
    with _umask(0):
        acknowledge(cfg)
    mode = stat.S_IMODE(session.ack_path(cfg).stat().st_mode)
    assert mode == config.PRIVATE_FILE_MODE


def test_no_blanket_affirmative_satisfies_the_acknowledgment(cfg):
    """AE20 and R34: no flag, configuration key or environment variable satisfies
    the acknowledgment.

    Flags are read from the signatures, every module toggle is switched on, and
    both the consult and the mint are scanned for environment reads, since a
    behavioural test would have to guess the variable name.
    """
    from cratekit.core import profiles

    for function in (session.assert_gates, session.assert_backup_acknowledged):
        booleans = [
            name
            for name, parameter in inspect.signature(function).parameters.items()
            if isinstance(parameter.default, bool)
        ]
        assert not booleans, f"{function.__name__} takes {booleans}, which is a blanket flag"

    toggles = {module: True for module in profiles.MODULES}
    assert toggles, "no module toggle was found, so the walk is broken"
    object.__setattr__(cfg.modules, "explicit", toggles)

    assert _gates_refusal(cfg).code is ExitCode.ACK_REQUIRED

    reads_environment = [
        function.__name__
        for function in (
            session.assert_gates,
            session.assert_backup_acknowledged,
            session.read_acknowledgment,
            session.ack_path,
            session.record_acknowledgment,
            session._shown_ages,
            session.Acknowledgment.to_json,
        )
        if "environ" in inspect.getsource(function) or "getenv" in inspect.getsource(function)
    ]
    assert not reads_environment, (
        f"{reads_environment} read the environment on the acknowledgment path, so a "
        f"variable could answer the one gate a person has to answer"
    )


# The session log


def test_the_log_records_everything_a_restore_has_to_judge(cfg):
    """Identifier, workflow, timestamp, capture path, change summary, state, actor."""
    acknowledged = acknowledge(cfg)
    record = session.open_session(
        cfg,
        workflow="a-destructive-workflow",
        actor=acknowledged.actor,
        acknowledged_at=acknowledged.recorded_at.isoformat(),
    )
    session.attach_capture(record, "/captures/one/master.db", cfg)
    record.change = session.ChangeSummary(
        (
            session.TreeChange(tree="tree-one", created=3, updated=1),
            session.TreeChange(tree="tree-two", created=0, updated=7),
        )
    )
    session.close_session(
        record,
        cfg,
        identity_provider=lambda _path: cfg.library.volume_id,
        mount_enumerator=lambda: (),
    )

    written = json.loads(session.log_path(record.session_id, cfg).read_text())
    assert written["session_id"] == record.session_id
    assert written["workflow"] == "a-destructive-workflow"
    assert written["started"]
    assert written[session.SNAPSHOT_KEY] == "/captures/one/master.db"
    assert written[session.STATE_KEY] == str(session.SessionState.CLOSED)
    assert written["actor"] == acknowledged.actor

    trees = {entry["tree"]: entry for entry in written["change"]["trees"]}
    assert trees["tree-one"]["created"] == 3
    assert trees["tree-two"]["updated"] == 7
    assert written["change"]["created"] == 3 and written["change"]["updated"] == 8


def test_a_session_record_is_private_under_any_umask(cfg):
    with _umask(0):
        record = session.open_session(cfg, workflow="a-destructive-workflow")
    path = session.log_path(record.session_id, cfg)
    assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE
    assert stat.S_IMODE(path.parent.stat().st_mode) == config.PRIVATE_DIR_MODE


def test_a_session_record_round_trips(cfg):
    record = session.open_session(cfg, workflow="a-destructive-workflow", sources=("one",))
    record.change = session.ChangeSummary((session.TreeChange("tree-one", created=2),))
    session.write_record(record, cfg)
    reread = session.read_record(record.session_id, cfg)
    assert reread.to_json() == record.to_json()


def test_closing_into_a_non_terminal_state_refuses(cfg):
    """A terminal state RELEASES the capture, so closing into a live one lies."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    _refusal(session.close_session, record, cfg, state=session.SessionState.AWAITING_IMPORT)


def test_an_unreadable_record_does_not_stop_the_log_being_read(cfg):
    good = session.open_session(cfg, workflow="a-destructive-workflow")
    (session.log_dir(cfg) / "damaged.json").write_text("{not json")
    assert [r.session_id for r in session.records(cfg)] == [good.session_id]


# One source per run (R29)


def test_a_refusal_at_source_two_leaves_source_one_committed_and_names_both(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two", "three")
    )

    def run_one(source):
        if source == "two":
            raise refuse("refused-by-policy", "source two is not acceptable")
        return session.ChangeSummary((session.TreeChange(tree=f"tree-{source}", created=1),))

    cause = _refusal(session.commit_sources, record, ("one", "two", "three"), run_one, cfg=cfg)

    assert cause.detail["committed"] == ["one"]
    assert cause.detail["refused_source"] == "two"
    assert set(cause.detail["remaining"]) == {"two", "three"}
    assert cause.inner is not None and cause.inner.reason == "refused-by-policy"

    # The same facts are on disk.
    persisted = session.read_record(record.session_id, cfg)
    assert persisted.sources["one"] == str(session.SourceState.COMMITTED)
    assert persisted.sources["two"] == str(session.SourceState.REFUSED)
    assert persisted.change.trees[0].tree == "tree-one"


def test_a_resume_skips_a_committed_source_and_finishes_the_rest(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two")
    )
    attempted: list[str] = []

    def run_one(source):
        attempted.append(source)
        if source == "two" and len(attempted) == 2:
            raise refuse("refused-by-policy", "not this time")
        return session.ChangeSummary((session.TreeChange(tree=f"tree-{source}", created=1),))

    _refusal(session.commit_sources, record, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two"]

    resumed = session.read_record(record.session_id, cfg)
    session.commit_sources(resumed, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two", "two"], "a committed source was run again"
    assert resumed.committed_sources() == ("one", "two")
    assert {entry.tree for entry in resumed.change.trees} == {"tree-one", "tree-two"}


# The capture gate, and the post-commit read-back (AE13)


def test_a_capture_that_failed_its_check_blocks_the_commit_behind_it(cfg):
    record = snapshot.capture(cfg, verifier=lambda _path: False)
    cause = _refusal(snapshot.assert_verified, record)
    assert cause.reason == "snapshot-integrity-failed"


def test_a_read_back_that_disagrees_ends_committed_unverified_and_advances_nothing(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two")
    )
    session.attach_capture(record, "/captures/one/master.db", cfg)
    record.sources["one"] = str(session.SourceState.COMMITTED)
    record.change = session.ChangeSummary((session.TreeChange("tree-one", created=4),))
    session.write_record(record, cfg)

    disposed: list[str] = []
    cause = _refusal(
        session.verify_commit,
        record,
        cfg,
        expect=lambda _db: False,
        reopen=_handle_recording(disposed),
    )
    assert cause.code is ExitCode.LIBRARY_UNREADABLE
    assert cause.reason == "session-committed-unverified"
    assert cause.detail["snapshot_path"] == "/captures/one/master.db"
    assert cause.detail["change"]["trees"][0]["tree"] == "tree-one"

    persisted = session.read_record(record.session_id, cfg)
    assert persisted.state is session.SessionState.COMMITTED_UNVERIFIED
    assert persisted.sources["two"] == str(session.SourceState.PENDING), (
        "a source was marked done behind a read-back that disagreed"
    )
    assert disposed == ["session", "engine"], (
        "the read-back handle was not fully released on the DISAGREEING path, "
        "which is the path a restore follows, so the restore would meet a file "
        "this process still holds open"
    )


def test_the_read_back_releases_the_database_completely(cfg):
    """The read-back disposes the engine too, since a pooled connection held open
    makes a restore over the file fail as if corrupt."""
    disposed: list[str] = []
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    handle = _handle_recording(disposed)
    assert session.verify_commit(record, cfg, expect=lambda _db: True, reopen=handle) is True
    assert disposed == ["session", "engine"]


def test_a_disagreement_reports_a_live_rekordbox_separately(cfg, monkeypatch):
    """Two facts with two fixes, carried as a chain rather than collapsed into one."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    cause = excinfo.value.cause
    assert cause.reason == "session-committed-unverified"
    assert cause.inner is not None
    assert cause.inner.reason == "rekordbox-running"
    assert cause.inner.code is ExitCode.REKORDBOX_OPEN


def test_an_unresolved_session_refuses_every_further_write(cfg):
    """Post-commit rollback does not exist, so the next write waits for a person."""
    acknowledge(cfg)
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    _refusal(session.verify_commit, record, cfg, expect=lambda _db: False, reopen=object)

    cause = _gates_refusal(cfg)
    assert cause.reason == "session-committed-unverified"
    assert cause.code is ExitCode.LIBRARY_UNREADABLE


def test_an_unresolved_session_keeps_its_capture_out_of_the_pruner(cfg):
    """The state is deliberately non-terminal, and this is what that buys."""
    capture_path = cfg.library.root / "captures" / "one" / "master.db"
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, capture_path, cfg)
    _refusal(session.verify_commit, record, cfg, expect=lambda _db: False, reopen=object)

    assert rb_writer.default_protected_snapshot_paths(cfg) == {capture_path.resolve()}


# The un-imported XML output as a first-class state


def test_a_run_holding_an_unimported_output_refuses_a_database_surface(cfg):
    """XML surfaces are upstream, since the import creates the row a database
    surface addresses."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.assert_database_surface_allowed(record)  # nothing pending, nothing refused

    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "Music" / "out.xml",
        summary="import the generated collection",
        verify_verb="run.show",
        blocks=("route.inbox",),
        steps=("import the file in rekordbox",),
    )
    session.mark_awaiting_import(record, pending, cfg)

    cause = _refusal(session.assert_database_surface_allowed, record)
    assert cause.code is ExitCode.PENDING_HUMAN
    assert cause.reason == "awaiting-import"
    assert cause.detail["verify_verb"] == "run.show"

    persisted = session.read_record(record.session_id, cfg)
    assert persisted.state is session.SessionState.AWAITING_IMPORT
    assert persisted.pending is not None
    assert persisted.pending.blocks == ("route.inbox",)


def test_the_pending_action_is_the_one_the_command_line_layer_already_enforces(cfg):
    """The pending import feeds the command line's own ``blocks`` check."""
    from cratekit.cli import gates, registry

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "Music" / "out.xml",
        summary="import the generated collection",
        verify_verb="run.show",
        blocks=("route.inbox",),
    )
    assert pending.kind == "rekordbox_import"

    entry = next(e for e in registry.entries() if e.name == "run.show")
    run = gates.new_run(entry)
    run.pending = pending
    assert gates.blocked_by(run, "route.inbox") is not None
    assert gates.blocked_by(run, "profile.show") is None


# The runtime half of R17's fifth surface


def _analysis_tree(root: Path) -> list[Path]:
    directory = root / "PIONEER" / "USBANLZ" / "one"
    directory.mkdir(parents=True)
    written = []
    for name in ("ANLZ0000.DAT", "ANLZ0000.EXT", "ANLZ0000.2EX", "ANLZ0000.3EX"):
        path = directory / name
        path.write_bytes(b"analysis")
        written.append(path)
    return written


def test_a_moved_analysis_file_refuses_the_session(cfg, tmp_path):
    """A real rewritten file refuses, the half the source scan cannot see."""
    written = _analysis_tree(tmp_path / "library")
    victim = written[1]

    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            victim.write_bytes(b"a rewritten grid")
            stat_result = victim.stat()
            os.utime(victim, ns=(stat_result.st_atime_ns, stat_result.st_mtime_ns + 10**9))

    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified"
    assert cause.code is ExitCode.REFUSED_BY_POLICY
    assert any(str(victim) in line for line in cause.detail["changed"])


def test_a_removed_analysis_file_refuses_too(cfg, tmp_path):
    """A destroyed grid is not a smaller problem than a rewritten one."""
    written = _analysis_tree(tmp_path / "library")
    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            written[0].unlink()
    assert "was removed" in excinfo.value.cause.detail["changed"][0]


def test_a_session_that_touches_nothing_passes(cfg, tmp_path):
    """P7. A guard that fires on correct code is one people route around."""
    _analysis_tree(tmp_path / "library")
    with session.analysis_files_unmoved([tmp_path / "library"]) as watched:
        assert len(watched) == 4
    # Reading them stays legal.
    with session.analysis_files_unmoved([tmp_path / "library"]):
        for path in session.analysis_files_under([tmp_path / "library"]):
            path.read_bytes()


def test_the_gates_can_arm_the_analysis_watch_for_the_body_of_a_session(cfg, tmp_path):
    """The gates arm the analysis watch over caller-supplied roots, not the whole
    volume; the empty default is closed by the countdown below."""
    written = _analysis_tree(tmp_path / "library")
    acknowledge(cfg)
    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(
            cfg,
            workflow="a-destructive-workflow",
            analysis_roots=[tmp_path / "library"],
            **open_gates(cfg),
        ):
            written[2].write_bytes(b"a rewritten grid, mid session")
            moved = written[2].stat()
            os.utime(written[2], ns=(moved.st_atime_ns, moved.st_mtime_ns + 10**9))
    assert excinfo.value.cause.reason == "anlz-modified"


def test_the_tree_writers_reach_for_the_session_spine(cfg):
    """P5: the tree writers call ``assert_gates`` and ``assert_verified`` and pass
    ``analysis_roots``, or the watch watches nothing.

    Checked on the syntax tree, since a substring search passes on the module's
    own docstring explaining the calls.
    """
    import ast
    import importlib

    trees = importlib.import_module("cratekit.write.trees")
    module = ast.parse(Path(trees.__file__).read_text(encoding="utf-8"))

    called: set[str] = set()
    keywords: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            called.add(node.func.attr)
        elif isinstance(node.func, ast.Name):
            called.add(node.func.id)
        keywords.update(kw.arg for kw in node.keywords if kw.arg)

    for obligation in ("assert_gates", "assert_verified"):
        assert obligation in called, (
            f"the tree writers do not CALL {obligation!r}, so the "
            f"destructive-session spine is optional for the unit that needs it most"
        )
    assert "analysis_roots" in keywords, (
        "the tree writers never pass analysis_roots to anything, so the watch "
        "that is the runtime half of R17's fifth surface watches nothing"
    )


def test_the_watched_set_is_never_narrower_than_the_binding_recognises():
    """P4: the suffixes come from the binding's own compiled pattern."""
    from pyrekordbox.anlz import RE_ANLZ

    alternatives = re.search(r"\(([^)]*)\)", RE_ANLZ.pattern).group(1).split("|")
    assert alternatives, "the binding's pattern has no alternation, so the walk is broken"
    for suffix in alternatives:
        assert session.is_analysis_file(f"ANLZ0000.{suffix}"), suffix


def test_the_watched_set_covers_every_file_surface_five_declares():
    """Wider than the binding: surface five's four declared suffixes, read from its
    docstring, since the fourth is a real grid-bearing file."""
    import tests.test_no_beatgrid_ever as surface_five

    declared = set(re.findall(r"``\.([0-9A-Z]{3})``", surface_five.__doc__))
    assert len(declared) == 4, f"surface five declares {sorted(declared)}"
    for suffix in declared:
        assert session.is_analysis_file(f"ANLZ0001.{suffix}"), suffix
    assert not session.is_analysis_file("ANLZ0001.TXT")
    assert not session.is_analysis_file("something.DAT")


# The residual finding "The backup restore is not yet bound to the
# destructive-session gates": the backup restore passes the same gates


def test_the_backup_restore_passes_the_destructive_session_gates(volume_matches, cfg, tmp_path):
    """KTD24: the gates bind to destruction, and a restore writes no database row."""
    target = tmp_path / "scratch"
    target.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        backup.plan_restore(
            cfg,
            target=target,
            confirmed=True,
            snapshot="2026-08-01T000000Z",
            runner=lambda command: backup.CommandResult(returncode=0),
            process_lister=lambda: (),
        )
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


def test_the_restores_own_refusals_survive_the_gates_being_added(cfg, tmp_path):
    """Added to, never replaced. An unconfirmed restore is still refused by name."""
    acknowledge(cfg)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg,
            target=tmp_path,
            confirmed=False,
            runner=lambda command: backup.CommandResult(returncode=0),
            process_lister=lambda: (),
            gates=lambda: session.assert_gates(
                cfg, workflow=backup.RESTORE_WORKFLOW, **open_gates(cfg)
            ),
        )
    assert excinfo.value.refusal is backup.Refusal.RESTORE_NOT_CONFIRMED


def test_a_rehearsed_restore_is_not_exempt_from_the_gates(volume_matches, cfg, tmp_path):
    """A rehearsal is gated too, since one run beside another write previews a
    library changing underneath it."""
    database_target = backup.database_target_for(cfg, tmp_path / "scratch")
    plan = backup.RestorePlan(
        target=tmp_path / "scratch",
        database_target=database_target,
        snapshot="2026-08-01T000000Z",
        clears=(),
        commands=(backup.Command(label=backup.RESTORE_DATABASE, argv=("rclone", "copy")),),
    )
    with pytest.raises(CratekitError) as excinfo:
        backup.run_restore(
            plan, cfg, runner=lambda command: backup.CommandResult(returncode=0), dry_run=True
        )
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


def test_the_destructive_half_of_a_restore_has_no_ungated_call_shape():
    """``cfg`` is required, since an optional one would be an ungated restore (P5)."""
    parameters = inspect.signature(backup.run_restore).parameters
    assert parameters["cfg"].default is inspect.Parameter.empty
    assert parameters["cfg"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD


def test_every_backup_refusal_carries_one_code_in_both_cause_tables():
    """Every backup refusal has one code in both cause tables (U27, KTD25).

    Derived from the enum (P3), and the codes are compared, not mere presence,
    since disagreeing tables describe different failures.
    """
    from cratekit.cli import exit_codes as reservations  # noqa: PLC0415
    from cratekit.core.cause import REASONS  # noqa: PLC0415

    assert backup.REFUSALS, "the refusal enum is empty, so nothing below is measured"
    disagreements = {
        str(refusal): (REASONS.get(str(refusal)), reservations.reserved(str(refusal)).code)
        for refusal in backup.REFUSALS
        if REASONS.get(str(refusal)) is not reservations.reserved(str(refusal)).code
    }
    assert not disagreements, (
        f"cause.REASONS and exit_codes.RESERVED_CAUSES give different statuses to "
        f"the same backup refusal: {disagreements}"
    )


# The latch has an exit, the log fails CLOSED, and the guards run on both paths.
# Found by an adversarial read: the other half of properties tested above.


def _condemn(cfg):
    """Leave this library with one unresolved ``committed-unverified`` session."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, "/captures/one/master.db", cfg)
    _refusal(session.verify_commit, record, cfg, expect=lambda _db: False, reopen=object)
    return record


def test_a_condemned_library_still_admits_the_recovery_its_remedy_names(cfg):
    """The latch admits the recovery its own remedy names."""
    acknowledge(cfg)
    condemned = _condemn(cfg)

    assert _gates_refusal(cfg).reason == "session-committed-unverified"

    with session.assert_gates(
        cfg,
        workflow="a-recovery-workflow",
        intent=session.Intent.RECOVERY,
        **open_gates(cfg),
    ) as held:
        assert held.intent is session.Intent.RECOVERY
    assert condemned.session_id


def test_a_recovery_session_is_exempt_from_the_latch_and_from_nothing_else(cfg):
    """Recovery is exempt from the latch only (R34)."""
    _condemn(cfg)
    recovery = {
        "workflow": "a-recovery-workflow",
        "intent": session.Intent.RECOVERY,
    }

    assert _gates_refusal(cfg, **recovery).code is ExitCode.ACK_REQUIRED

    acknowledge(cfg)
    wrong_disk = _refusal_entering(
        session.assert_gates,
        cfg, **recovery, identity_provider=foreign_identity, mount_enumerator=lambda: ()
    )
    assert wrong_disk.code is ExitCode.LIBRARY_UNAVAILABLE

    contender = open(session.lock_path(cfg), "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        with pytest.raises(CratekitError) as busy:
            with session.assert_gates(cfg, **recovery, **open_gates(cfg)):
                pass
    finally:
        contender.close()
    assert busy.value.cause.code is ExitCode.LIBRARY_BUSY


def test_the_restore_is_the_recovery_and_reaches_its_own_refusals(volume_matches, cfg, tmp_path):
    """End to end, a condemned library reaches ``plan_restore``'s own refusals."""
    acknowledge(cfg)
    _condemn(cfg)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg,
            target=tmp_path,
            confirmed=False,
            runner=lambda command: backup.CommandResult(returncode=0),
            process_lister=lambda: (),
        )
    assert excinfo.value.refusal is backup.Refusal.RESTORE_NOT_CONFIRMED


def test_resolving_the_record_is_what_clears_the_latch_not_the_restore(cfg):
    """The log survives a rollback, so resolving the record clears the latch."""
    acknowledge(cfg)
    condemned = _condemn(cfg)

    resolved = session.resolve_unverified_session(condemned.session_id, cfg)
    assert resolved.state is session.SessionState.ABANDONED
    assert resolved.terminal

    with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
        pass


def test_resolving_refuses_any_state_but_the_one_it_is_for(cfg):
    """Ending somebody else's OPEN session releases a capture a live run needs."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    cause = _refusal(session.resolve_unverified_session, record.session_id, cfg)
    assert cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert session.read_record(record.session_id, cfg).state is session.SessionState.OPEN


def test_the_latch_refuses_a_record_this_build_cannot_read(cfg):
    """The gate reads the log strictly, since a tolerant reader fails open. Both
    damage shapes are driven, since they raise differently."""
    acknowledge(cfg)
    condemned = _condemn(cfg)
    path = session.log_path(condemned.session_id, cfg)

    for damage in ({"schema_version": 2}, {"state": "committed-unverified-partially"}):
        written = json.loads(path.read_text())
        written.update(damage)
        path.write_text(json.dumps(written))

        assert session.records(cfg) == (), "the tolerant reader should still skip it"
        with pytest.raises(CratekitError) as excinfo:
            with session.assert_gates(
                cfg, workflow="a-destructive-workflow", **open_gates(cfg)
            ):
                raise AssertionError("the gates admitted a session against an unreadable log")
        assert excinfo.value.cause.detail["unreadable"] == [str(path)], damage


def test_the_session_log_filename_is_legal_on_a_library_volume(cfg):
    """Log filenames carry no colon, since exFAT and FAT library volumes refuse one;
    the identifier itself keeps its colons."""
    identifier = session.new_session_id()
    assert ":" in identifier, "the identifier space is the run identifier space"

    name = session.log_path(identifier, cfg).name
    assert not (set(name) & set(r'<>:"/\|?* ')), name
    assert name.isascii()

    # The record carries the unsanitised identifier.
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    written = json.loads(session.log_path(record.session_id, cfg).read_text())
    assert written["session_id"] == record.session_id
    assert session.read_record(record.session_id, cfg).session_id == record.session_id


def test_a_supplied_identifier_cannot_compose_a_path(cfg):
    """A separator in a supplied identifier cannot escape the store the scans read."""
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", session_id="../../escaped"
    )
    written = session.log_path(record.session_id, cfg)
    assert written.parent == session.log_dir(cfg)
    assert written.exists()
    assert session.records(cfg)[0].session_id == "../../escaped"


def test_a_per_source_refusal_widens_the_scope_and_never_narrows_it(cfg):
    """A wrapper widens a refusal's scope, never narrows it, since it knows less
    than the cause it wraps."""
    from cratekit.core.cause import Scope

    def refusing_at(scope):
        record = session.open_session(
            cfg, workflow="a-destructive-workflow", sources=("one",)
        )

        def run_one(_source):
            raise refuse("refused-by-policy", "not this time", scope=scope)

        cause = _refusal(session.commit_sources, record, ("one",), run_one, cfg=cfg)
        return cause

    assert refusing_at(Scope.RUN).scope is Scope.RUN
    assert refusing_at(Scope.SESSION).scope is Scope.SESSION
    assert refusing_at(Scope.ITEM).scope is Scope.SOURCE, "the wrapper's own scope applies"
    assert refusing_at(Scope.SOURCE).scope is Scope.SOURCE


def test_a_read_back_that_could_not_run_says_so_rather_than_saying_it_disagreed(cfg):
    """A read-back that could not run carries its typed cause, so an unplugged drive
    is not reported as a disagreement."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")

    def cannot_open():
        raise refuse("library-directory-missing", "the volume went away")

    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(record, cfg, expect=lambda _db: True, reopen=cannot_open)

    cause = excinfo.value.cause
    assert cause.reason == "session-committed-unverified"
    assert cause.inner is not None
    assert cause.inner.reason == "library-directory-missing", (
        "the typed read-back failure was swallowed into a log line"
    )
    assert session.read_record(record.session_id, cfg).state is (
        session.SessionState.COMMITTED_UNVERIFIED
    ), "a commit landed and nothing confirmed it, so the session is still unverified"


def test_both_the_read_back_failure_and_a_live_rekordbox_travel_together(cfg, monkeypatch):
    """Neither displaces the other; the general fact goes at the tail."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    record = session.open_session(cfg, workflow="a-destructive-workflow")

    def cannot_open():
        raise refuse("database-open-failed", "held by something")

    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(record, cfg, expect=lambda _db: True, reopen=cannot_open)

    chain = []
    cause = excinfo.value.cause
    while cause is not None:
        chain.append(cause.reason)
        cause = cause.inner
    assert chain == [
        "session-committed-unverified",
        "database-open-failed",
        "rekordbox-running",
    ]


def test_an_unreadable_backup_fact_file_refuses_the_mint(cfg):
    """"Could not read" is never recorded as "nothing to show" (KTD18)."""
    from cratekit.core import backup_facts

    damaged = backup_facts.path_for(cfg)
    damaged.parent.mkdir(parents=True, exist_ok=True)
    damaged.write_text("{ this is not json")
    cause = _refusal(acknowledge, cfg)
    assert cause.reason == "backup-facts-unreadable"
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.remediation.remedy is Remedy.REPAIR_BACKUP_FACTS
    assert session.read_acknowledgment(cfg) is None, "a refused mint wrote a record"

    # An absent file is normal and still mints.
    damaged.unlink()
    assert acknowledge(cfg).shown


def test_a_fact_file_this_account_may_not_open_asks_for_access_not_for_repair(cfg):
    """A permission failure asks for access, not repair, driven through
    ``read_facts`` with the precondition asserted, not assumed."""
    from cratekit.core import backup_facts

    locked = backup_facts.path_for(cfg)
    locked.parent.mkdir(parents=True, exist_ok=True)
    locked.write_text("{}")
    locked.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            locked.read_bytes()

        cause = _refusal(acknowledge, cfg)
    finally:
        locked.chmod(0o600)

    assert cause.reason == "backup-facts-unreadable"
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS, (
        "a person whose configuration directory this account cannot open was "
        "told to repair or reset a file that is very likely intact"
    )
    assert session.read_acknowledgment(cfg) is None, "a refused mint wrote a record"


def test_a_fact_file_from_a_newer_build_asks_for_an_upgrade(cfg):
    """The third remedy ``read_facts`` raises travels the same way."""
    from cratekit.core import backup_facts

    newer = backup_facts.path_for(cfg)
    newer.parent.mkdir(parents=True, exist_ok=True)
    newer.write_text(
        json.dumps({"schema_version": backup_facts.SCHEMA_VERSION + 1, "portions": {}})
    )
    cause = _refusal(acknowledge, cfg)

    assert cause.reason == "backup-facts-unreadable"
    assert cause.remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_the_analysis_watch_runs_even_when_the_session_body_refuses(cfg, tmp_path):
    """The watch runs when the body refuses, or a retried session rewrites a grid
    unreported, carrying the body's refusal inside."""
    written = _analysis_tree(tmp_path / "library")
    victim = written[0]

    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            victim.write_bytes(b"a rewritten grid")
            moved = victim.stat()
            os.utime(victim, ns=(moved.st_atime_ns, moved.st_mtime_ns + 10**9))
            raise refuse("refused-by-policy", "the smoke test failed")

    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified", (
        "the body's refusal hid a moved beat grid, which is the one rule the "
        "project calls inviolable"
    )
    assert cause.inner is not None and cause.inner.reason == "refused-by-policy", (
        "the body's own refusal was replaced rather than carried"
    )


def test_a_body_that_refuses_with_no_drift_keeps_its_own_refusal(cfg, tmp_path):
    """P7. The watch must not rewrite a refusal it has nothing to say about."""
    _analysis_tree(tmp_path / "library")
    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            raise refuse("refused-by-policy", "the smoke test failed")
    assert excinfo.value.cause.reason == "refused-by-policy"


def test_an_appearing_analysis_file_refuses_too(cfg, tmp_path):
    """An appearing analysis file is the third kind of drift."""
    _analysis_tree(tmp_path / "library")
    fresh = tmp_path / "library" / "PIONEER" / "USBANLZ" / "one" / "ANLZ0002.DAT"
    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            fresh.write_bytes(b"analysed mid session")
    assert excinfo.value.cause.detail["changed"] == [f"{fresh} appeared"]


def test_a_rewrite_inside_one_tick_of_the_clock_is_caught_by_the_size(cfg, tmp_path):
    """The size catches a rewrite inside one clock tick; the mtime is put back."""
    written = _analysis_tree(tmp_path / "library")
    victim = written[3]
    original = victim.stat()

    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            victim.write_bytes(b"a rewritten grid, longer than what was there")
            os.utime(victim, ns=(original.st_atime_ns, original.st_mtime_ns))
    assert excinfo.value.cause.reason == "anlz-modified"
    assert victim.stat().st_mtime_ns == original.st_mtime_ns, "the mtime moved after all"


def test_a_live_holder_this_platform_will_not_describe_is_assumed_alive(cfg, monkeypatch):
    """A live holder whose start time the platform hides is alive, or a writing
    session is offered up as stale."""
    here = session.current_holder()
    monkeypatch.setattr(session, "process_started", lambda _pid: session.UNKNOWN_IDENTITY)
    assert session.holder_alive(here) is True

    with pytest.raises(CratekitError) as excinfo:
        session.release_stale_lock(cfg, path=_lock_recording(cfg, here))
    assert excinfo.value.cause.remediation.remedy is Remedy.WAIT_FOR_HOLDER


def test_a_holder_whose_process_is_gone_is_still_judged_dead(cfg):
    """A genuinely finished process is still judged dead, since only "no such
    process", not "will not say", clears a claim. Real probes, no stub."""
    import subprocess

    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    assert session.process_exists(finished.pid) is False

    here = session.current_holder()
    gone = session.Holder(
        host=here.host, boot=here.boot, pid=finished.pid, started="1.000"
    )
    assert session.holder_alive(gone) is False

    cleared = session.release_stale_lock(cfg, path=_lock_recording(cfg, gone))
    assert cleared == gone
    assert session.read_lock_holder(session.lock_path(cfg)) is None


def _lock_recording(cfg, holder):
    """Write a lock file naming ``holder``, and return its path."""
    path = session.lock_path(cfg)
    config.atomic_write_bytes(
        json.dumps({"holder": holder.to_json()}).encode("utf-8"), path
    )
    return path


def test_the_recorded_actor_is_the_derived_one_and_not_a_name_from_anywhere_else(
    cfg, monkeypatch
):
    """R34 as behaviour, since a signature scan cannot see an environment read."""
    monkeypatch.setattr(session, "derive_actor", lambda: "the-derived-actor")
    recorded = acknowledge(cfg)
    assert recorded.actor == "the-derived-actor"
    assert json.loads(session.ack_path(cfg).read_text())["actor"] == "the-derived-actor"


def test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one(cfg, monkeypatch):
    """The mint's default terminal probe is the real one; every other test injects."""
    asked: list[bool] = []

    def probe():
        asked.append(True)
        return False

    monkeypatch.setattr(session, "has_controlling_terminal", probe)
    cause = _refusal(session.record_acknowledgment, cfg)
    assert asked, "the mint did not consult the real probe"
    assert cause.reason == "backup-acknowledgment-no-terminal"


def test_the_real_terminal_probe_answers_no_when_there_is_no_terminal(monkeypatch):
    """And the probe itself, driven, so it cannot become ``return True``."""
    monkeypatch.setattr(os, "ctermid", lambda: str(Path("/nonexistent") / "tty"))
    assert session.has_controlling_terminal() is False


def test_the_volume_is_judged_before_a_restore_resolves_its_target(cfg, tmp_path):
    """``plan_restore`` judges the volume first, since resolving a path against the
    wrong volume is already the damage."""
    with pytest.raises(CratekitError) as excinfo:
        backup.plan_restore(
            cfg,
            target=tmp_path / "a-target-that-does-not-exist",
            confirmed=True,
            snapshot="2026-08-01T000000Z",
            runner=lambda command: (_ for _ in ()).throw(AssertionError("the remote was read")),
            process_lister=lambda: (),
            gates=lambda: session.assert_gates(
                cfg,
                workflow=backup.RESTORE_WORKFLOW,
                intent=session.Intent.RECOVERY,
                identity_provider=foreign_identity,
                mount_enumerator=lambda: (),
            ),
        )
    cause = excinfo.value.cause
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert cause.reason == "library-volume-mismatch", (
        "a restore reached its own target check before the volume gate"
    )


def test_a_gate_refused_restore_deletes_nothing_and_transfers_nothing(
    volume_matches, cfg, tmp_path
):
    """A gate-refused restore clears and transfers nothing, with real gates."""
    target = tmp_path / "scratch"
    database_target = backup.database_target_for(cfg, target)
    database_target.parent.mkdir(parents=True, exist_ok=True)
    sidecars = tuple(
        database_target.with_name(database_target.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    for sidecar in sidecars:
        sidecar.write_bytes(b"the live write-ahead log")

    invoked: list[backup.Command] = []
    plan = backup.RestorePlan(
        target=target,
        database_target=database_target,
        snapshot="2026-08-01T000000Z",
        clears=sidecars,
        commands=(backup.Command(label=backup.RESTORE_DATABASE, argv=("rclone", "copy")),),
    )

    def recorder(command):
        invoked.append(command)
        return backup.CommandResult(returncode=0)

    cause = _refusal(backup.run_restore, plan, cfg, runner=recorder, dry_run=False)

    assert cause.code is ExitCode.ACK_REQUIRED
    assert invoked == [], "a refused restore ran a transfer"
    for sidecar in sidecars:
        assert sidecar.exists(), f"a refused restore unlinked {sidecar.name}"
        assert sidecar.read_bytes() == b"the live write-ahead log"


# The record a gated session keeps (R-12, R-375)


def recording_gates(cfg, **overrides):
    return session.assert_gates(
        cfg, workflow="a-recorded-write", keep=session.Keep.RECORD, **open_gates(cfg, **overrides)
    )


def test_the_gates_keep_nothing_unless_asked(cfg):
    """The default is what every capture-free caller already had: no record."""
    acknowledge(cfg)
    with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)) as gates:
        assert gates.record is None
    assert session.records(cfg) == ()


def test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment(cfg):
    """Read FROM the gates, so a caller cannot record a second spelling of them."""
    minted = acknowledge(cfg)
    with recording_gates(cfg) as gates:
        on_disk = session.read_record(gates.record.session_id, cfg)
        assert on_disk.state is session.SessionState.OPEN

    (only,) = session.records(cfg)
    assert only.workflow == "a-recorded-write"
    assert only.actor == minted.actor
    assert only.acknowledged_at == minted.recorded_at.isoformat()
    assert only.state is session.SessionState.CLOSED
    assert only.ended is not None


def test_the_record_names_the_holder_the_lock_names(cfg):
    """R-598: the record names the lock's holder, since only the record survives a
    kill. Read while both are on disk."""
    acknowledge(cfg)
    with recording_gates(cfg) as gates:
        on_disk = session.read_record(gates.record.session_id, cfg)
        in_lock = session.read_lock_holder(gates.lock)
        assert in_lock == session.current_holder()
        assert session.Holder.from_json(on_disk.detail[session.HOLDER_KEY]) == in_lock
        assert session.orphaned(on_disk) is False


def test_a_supplied_holder_reaches_the_record_as_well_as_the_lock(cfg):
    """One claimant, so a caller naming a holder cannot split the two copies."""
    acknowledge(cfg)
    named = session.Holder(host="elsewhere", boot="b", pid=4242, started="7.000")
    with recording_gates(cfg, holder=named) as gates:
        on_disk = session.read_record(gates.record.session_id, cfg)
        assert session.read_lock_holder(gates.lock) == named
        assert session.Holder.from_json(on_disk.detail[session.HOLDER_KEY]) == named


def _gone_holder() -> session.Holder:
    """A process this boot started and that has exited, so ``holder_alive`` says gone."""
    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    here = session.current_holder()
    gone = session.Holder(host=here.host, boot=here.boot, pid=finished.pid, started="1.000")
    assert session.holder_alive(gone) is False
    return gone


@pytest.mark.parametrize(
    ("state", "holder", "expected"),
    [
        (session.SessionState.OPEN, "gone", True),
        (session.SessionState.OPEN, "here", False),
        (session.SessionState.OPEN, None, False),
        (session.SessionState.OPEN, "other-host", False),
        (session.SessionState.OPEN, "unreadable", False),
        (session.SessionState.AWAITING_IMPORT, "gone", False),
        (session.SessionState.COMMITTED_UNVERIFIED, "gone", False),
        (session.SessionState.CLOSED, "gone", False),
        (session.SessionState.ABANDONED, "gone", False),
    ],
)
def test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone(cfg, state, holder, expected):
    """Every condition that keeps a record, one row each, and the one row that ends it."""
    here = session.current_holder()
    record = session.open_session(cfg, workflow="w")
    record.state = state
    if holder == "gone":
        record.detail[session.HOLDER_KEY] = _gone_holder().to_json()
    elif holder == "here":
        record.detail[session.HOLDER_KEY] = here.to_json()
    elif holder == "other-host":
        record.detail[session.HOLDER_KEY] = {**_gone_holder().to_json(), "host": "elsewhere"}
    elif holder == "unreadable":
        record.detail[session.HOLDER_KEY] = {"pid": "not-a-number"}
    assert session.orphaned(record) is expected


def test_abandon_orphaned_sessions_ends_only_the_orphans(cfg):
    """The sweep closes through the ungated close and leaves everything else as it was."""
    gone = _gone_holder()
    orphan = session.open_session(cfg, workflow="w", holder=gone)
    live = session.open_session(cfg, workflow="w", holder=session.current_holder())
    unowned = session.open_session(cfg, workflow="intake")
    kept_bytes = {
        r.session_id: session.log_path(r.session_id, cfg).read_bytes() for r in (live, unowned)
    }

    (ended,) = session.abandon_orphaned_sessions(cfg)

    assert ended.session_id == orphan.session_id
    assert session.read_record(orphan.session_id, cfg).state is session.SessionState.ABANDONED
    for session_id, before in kept_bytes.items():
        assert session.log_path(session_id, cfg).read_bytes() == before
    assert session.abandon_orphaned_sessions(cfg) == ()


def test_the_sweep_ends_only_the_orphans_it_was_shown(cfg):
    """The sweep ends what it was handed and nothing else, at the engine."""
    shown = session.open_session(cfg, workflow="w", holder=_gone_holder())
    unshown = session.open_session(cfg, workflow="w", holder=_gone_holder())

    (ended,) = session.abandon_orphaned_sessions(cfg, only=[shown.session_id])

    assert ended.session_id == shown.session_id
    assert session.read_record(unshown.session_id, cfg).state is session.SessionState.OPEN


def test_a_refused_gate_keeps_no_record(cfg):
    """No acknowledgment is minted, so the gates refuse, and a refusal writes nothing."""
    _refusal_entering(recording_gates, cfg)
    assert session.records(cfg) == ()


def test_a_body_that_raises_closes_abandoned_and_its_own_error_surfaces(cfg):
    acknowledge(cfg)
    with pytest.raises(RuntimeError, match="the body failed"):
        with recording_gates(cfg):
            raise RuntimeError("the body failed")

    (only,) = session.records(cfg)
    assert only.state is session.SessionState.ABANDONED


def test_a_log_that_cannot_record_the_abandonment_does_not_replace_the_error(cfg, monkeypatch):
    """Abandoning is an attempt. The error that ended the session is the one to see."""
    acknowledge(cfg)
    real_close = session.close_session

    def the_log_is_gone(record, *args, **kwargs):
        if kwargs.get("state") is session.SessionState.ABANDONED:
            raise OSError("the volume holding the log went away")
        return real_close(record, *args, **kwargs)

    monkeypatch.setattr(session, "close_session", the_log_is_gone)
    with pytest.raises(RuntimeError, match="the body failed"):
        with recording_gates(cfg):
            raise RuntimeError("the body failed")


def test_a_clean_close_that_refuses_ends_abandoned_rather_than_open(cfg, monkeypatch):
    """A refused clean close ends ABANDONED, never OPEN, which would block every
    later prune and cutover, and the refusal still surfaces."""
    acknowledge(cfg)
    answers = iter([cfg.library.volume_id])

    def identity_then_gone(_path):
        return next(answers, _ELSEWHERE)

    with pytest.raises(CratekitError) as excinfo:
        with recording_gates(cfg, identity_provider=identity_then_gone) as gates:
            session.record_commit(
                gates.record,
                "a-tree",
                session.ChangeSummary((session.TreeChange(tree="a-tree", created=1),)),
                cfg,
            )
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE

    (only,) = session.records(cfg)
    assert only.state is session.SessionState.ABANDONED
    # The commit recorded first is still what a restore reads.
    assert only.committed_sources() == ("a-tree",)


def test_a_recovery_closes_as_a_recovery(cfg):
    """The intent rides in on the gates, so a recovery's close is not gated twice."""
    acknowledge(cfg)
    answers = iter([cfg.library.volume_id])
    with recording_gates(
        cfg,
        intent=session.Intent.RECOVERY,
        identity_provider=lambda _path: next(answers, _ELSEWHERE),
    ):
        pass
    (only,) = session.records(cfg)
    assert only.state is session.SessionState.CLOSED


def test_the_record_closes_after_the_analysis_watch_has_judged_the_session(cfg):
    """The record closes after the analysis watch judges a rewritten grid."""
    acknowledge(cfg)
    grids = Path(cfg.library.root) / "PIONEER" / "USBANLZ"
    grids.mkdir(parents=True)
    grid = grids / "ANLZ0000.DAT"
    grid.write_bytes(b"a grid")

    with pytest.raises(CratekitError):
        with recording_gates(cfg, analysis_roots=[grids.parent]):
            grid.write_bytes(b"a different grid, longer")

    (only,) = session.records(cfg)
    assert only.state is session.SessionState.ABANDONED


def test_a_recorded_commit_is_on_disk_before_the_session_ends(cfg):
    acknowledge(cfg)
    change = session.ChangeSummary((session.TreeChange(tree="a-tree", created=3),))
    with recording_gates(cfg) as gates:
        record = gates.record
        session.record_commit(record, "a-tree", change, cfg)
        on_disk = session.read_record(record.session_id, cfg)
        assert on_disk.state is session.SessionState.OPEN
        assert on_disk.committed_sources() == ("a-tree",)
        assert on_disk.change == change
        session.record_commit(record, "a-tree", change, cfg)

    (only,) = session.records(cfg)
    assert only.change.trees == (session.TreeChange(tree="a-tree", created=6),)


#: The shared capture function since U298; it attaches before it judges, so a
#: caller still owes the record and the commit.
SHARED_CAPTURE = "attached_capture"


def _capture_takers(src: Path) -> tuple[dict[str, set[str]], list[str]]:
    """Every function in ``src`` that takes a capture, with what it still owes.

    Per function, since one compliant writer would satisfy a per-module reading.
    Unattributable spellings are returned, not passed. The shared function's own
    body is not a taker.
    """
    import ast

    takers: dict[str, set[str]] = {}
    unreadable: list[str] = []
    for path in sorted(src.rglob("*.py")):
        if path.relative_to(src).as_posix() == "core/snapshot.py":
            continue
        text = path.read_text()
        # Every shape below names one of these, so a file naming neither has none.
        if "snapshot" not in text and SHARED_CAPTURE not in text:
            continue
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or "").endswith("snapshot"):
                if any(alias.name == "capture" for alias in node.names):
                    unreadable.append(f"{path.name}: from {node.module} import capture")
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name.split(".")[-1] == "snapshot" and alias.asname not in (
                        None,
                        "snapshot",
                    ):
                        unreadable.append(f"{path.name}: snapshot imported as {alias.asname}")
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if function.name == SHARED_CAPTURE:
                continue
            takes = False
            seen: set[str] = set()
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                if (
                    node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
                ) == SHARED_CAPTURE:
                    takes = True
                    seen.add("attach_capture")
                if isinstance(node.func, ast.Name) and node.func.id == "record_commit":
                    seen.add("a recorded commit")
                if not isinstance(node.func, ast.Attribute):
                    continue
                receiver = node.func.value
                if (
                    node.func.attr == "capture"
                    and isinstance(receiver, ast.Name)
                    and receiver.id == "snapshot"
                ):
                    takes = True
                if node.func.attr == "assert_gates" and any(
                    keyword.arg == "keep" and ast.unparse(keyword.value).endswith("Keep.RECORD")
                    for keyword in node.keywords
                ):
                    seen.add("keep=Keep.RECORD")
                if node.func.attr == "attach_capture":
                    seen.add("attach_capture")
                if node.func.attr == "record_commit":
                    seen.add("a recorded commit")
            # A ``_record_*_commit`` helper counts, each checked by
            # ``test_each_commit_helper_records_the_commit``.
            for node in ast.walk(function):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id.startswith("_record_")
                    and node.func.id.endswith("_commit")
                ):
                    seen.add("a recorded commit")
            if takes:
                owed = {"keep=Keep.RECORD", "attach_capture", "a recorded commit"}
                takers[f"{path.relative_to(src).as_posix()}::{function.name}"] = owed - seen
    return takers, unreadable


def test_every_capture_taken_in_src_is_attached_to_a_record_and_its_commit_recorded():
    """Every capture taker keeps a record, attaches it, records its commit (R-12, R-375)."""
    src = Path(session.__file__).resolve().parents[1]
    takers, unreadable = _capture_takers(src)

    assert not unreadable, (
        f"a capture is imported in a spelling this guard cannot follow: {unreadable}"
    )
    assert set(takers) == {
        # R-746, the native landing.
        "intake/native.py::apply_rows",
        # U111, the INBOX rotation.
        "intake/rotate.py::apply_rotation",
        # U134, the INBOX refill.
        "intake/refill.py::apply_refill",
        # U166, the INBOX / Analyze clear.
        "intake/analyzed.py::apply_clear",
        # U121, a landed set's permanent playlist.
        "intake/set_playlist.py::apply_alone",
        # U154, the shelve.
        "intake/shelve.py::apply",
        # U144, INSPIRATION levelled with downloaded sets.
        "organize/inspiration.py::apply",
        # U201, an account edit to a mirrored genre playlist.
        "organize/mirror_edits.py::write",
        # R-816, a row's genre written from its file.
        "tagging/rows.py::apply_rows",
        # U120, the favourites backfill.
        "favorites/backfill.py::apply",
        # U145, the quarters split into months.
        "favorites/split.py::apply",
        # U180, the Favorites folder ordered.
        "favorites/order.py::apply",
        # U119, the genre Favorites refresh.
        "write/genre_favorites.py::apply_refresh",
        "write/metadata_cli.py::mytags_vocals",
        # U130, a playlist pair's rekordbox side.
        "write/playlist_pair.py::apply",
        # R-923, rekordbox's defaults on bare rows.
        "write/row_defaults.py::apply_rows",
        # A32, the row probe's values.
        "write/row_link.py::apply_probes",
        # U149, the custom playlist twins.
        "sync/twins.py::write",
        # U202, a pair's rekordbox side for an account playlist.
        "sync/pair_reverse.py::create",
        # U288, offered rows taken out of the collection.
        "sync/removed.py::apply_removed",
        # R-758. One capture before two commits, and both are recorded.
        "write/trees.py::move_tree_membership",
        "write/trees.py::write_tree_membership",
    }, (
        f"the set of functions that take a capture changed: {sorted(takers)}. A new "
        f"one owes a session record for it; name it here once it keeps one."
    )
    assert all(not missing for missing in takers.values()), takers


def test_the_capture_guard_reads_a_function_that_keeps_no_record(tmp_path):
    """The guard reads a bare writer beside a compliant one in one module."""
    module = tmp_path / "write" / "sample.py"
    module.parent.mkdir()
    module.write_text(
        "def good(cfg, db):\n"
        "    with session.assert_gates(cfg, workflow='w', keep=session.Keep.RECORD) as gates:\n"
        "        taken = snapshot.capture(cfg, db=db)\n"
        "        session.attach_capture(gates.record, taken.root, cfg)\n"
        "        session.record_commit(gates.record, 's', change, cfg)\n"
        "\n"
        "def bare(cfg, db):\n"
        "    with session.assert_gates(cfg, workflow='w'):\n"
        "        snapshot.capture(cfg, db=db)\n"
    )
    (tmp_path / "aliased.py").write_text("from cratekit.core.snapshot import capture\n")

    takers, unreadable = _capture_takers(tmp_path)

    assert takers == {
        "write/sample.py::good": set(),
        "write/sample.py::bare": {"keep=Keep.RECORD", "attach_capture", "a recorded commit"},
    }
    assert unreadable == ["aliased.py: from cratekit.core.snapshot import capture"]


def test_the_capture_guard_reads_a_writer_that_takes_its_capture_through_the_shared_function(
    tmp_path,
):
    """A writer using the shared function (U298) still owes the record and commit,
    and the shared function's own body is not read as a writer."""
    module = tmp_path / "write" / "sample.py"
    module.parent.mkdir()
    module.write_text(
        "def attached_capture(gates, cfg, db):\n"
        "    capture = snapshot.capture(cfg, db=db)\n"
        "    session.attach_capture(gates.record, capture.root, cfg)\n"
        "    return gates.record, capture\n"
        "\n"
        "def good(cfg, db):\n"
        "    with session.assert_gates(cfg, workflow='w', keep=session.Keep.RECORD) as gates:\n"
        "        record, capture = attached_capture(gates, cfg, db)\n"
        "        record_commit(record, 's', 1, cfg)\n"
        "\n"
        "def unrecorded(cfg, db):\n"
        "    with session.assert_gates(cfg, workflow='w', keep=session.Keep.RECORD) as gates:\n"
        "        record, capture = trees.attached_capture(gates, cfg, db)\n"
        "\n"
        "def bare(cfg, db):\n"
        "    with session.assert_gates(cfg, workflow='w') as gates:\n"
        "        trees.attached_capture(gates, cfg, db)\n"
    )

    takers, unreadable = _capture_takers(tmp_path)

    assert takers == {
        "write/sample.py::good": set(),
        "write/sample.py::unrecorded": {"a recorded commit"},
        "write/sample.py::bare": {"keep=Keep.RECORD", "a recorded commit"},
    }
    assert unreadable == []


def test_the_shared_capture_attaches_before_it_judges(cfg, monkeypatch):
    """The shared capture attaches before it judges and is ``src``'s only capture."""
    import ast
    from types import SimpleNamespace

    from cratekit.write import trees

    acts: list[str] = []
    taken = SimpleNamespace(root=Path("captures") / "one")
    gates = SimpleNamespace(record=object())

    def capture(given, *, db):
        acts.append("capture")
        assert given is cfg and db == "the handle"
        return taken

    def attach(record, root, given):
        acts.append("attach")
        assert record is gates.record and root == taken.root and given is cfg

    def judge(capture):
        acts.append("judge")
        assert capture is taken
        raise RuntimeError("the capture did not verify")

    monkeypatch.setattr(snapshot, "capture", capture)
    monkeypatch.setattr(session, "attach_capture", attach)
    monkeypatch.setattr(snapshot, "assert_verified", judge)

    with pytest.raises(RuntimeError, match="did not verify"):
        trees.attached_capture(gates, cfg, "the handle")
    assert acts == ["capture", "attach", "judge"]

    monkeypatch.setattr(snapshot, "assert_verified", lambda capture: acts.append("verified"))
    assert trees.attached_capture(gates, cfg, "the handle") == (gates.record, taken)

    src = Path(session.__file__).resolve().parents[1]
    direct = [
        f"{path.relative_to(src).as_posix()}::{function.name}"
        for path in sorted(src.rglob("*.py"))
        if path.relative_to(src).as_posix() != "core/snapshot.py"
        and "snapshot" in (text := path.read_text())
        for function in ast.walk(ast.parse(text))
        if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "capture"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "snapshot"
    ]
    assert direct == [f"write/trees.py::{SHARED_CAPTURE}"]


def test_each_commit_helper_records_the_commit():
    """The helpers the guard accepts by name really do make the call."""
    import ast

    src = Path(session.__file__).resolve().parents[1]
    for relative, helper in (
        ("write/trees.py", "_record_membership_commit"),
        ("write/row_defaults.py", "record_commit"),
        ("write/metadata_cli.py", "_record_mytags_commit"),
        ("intake/native.py", "_record_landing_commit"),
        ("intake/rotate.py", "_record_rotation_commit"),
        ("intake/shelve.py", "_record_shelve_commit"),
        ("intake/refill.py", "_record_refill_commit"),
        ("favorites/backfill.py", "_record_backfill_commit"),
        ("favorites/split.py", "_record_split_commit"),
        ("favorites/order.py", "_record_order_commit"),
        ("sync/twins.py", "_record_twins_commit"),
    ):
        tree = ast.parse((src / relative).read_text())
        (function,) = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == helper
        ]
        calls = {
            node.func.attr
            for node in ast.walk(function)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert "record_commit" in calls, f"{helper} never records the commit"
