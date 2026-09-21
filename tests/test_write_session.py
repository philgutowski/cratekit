"""U8: the destructive-session boundary, its lock, and its acknowledgment.

The plan's test scenarios for this unit, one test per scenario, plus the two
standing debts it is on the hook to close.

* AE5. A session with no recorded acknowledgment parks blocked and names the fix.
* AE19. A second process refuses while the library lock is held, and names the
  holder.
* AE20. Every affirmative flag and configuration key together still leaves the
  acknowledgment required (R34).
* A non-interactive, agent-shaped invocation cannot mint an acknowledgment.
* A multi-source run refused at source two leaves source one committed and names
  both states; a resume skips source one (R29).
* A commit whose read-back disagrees ends ``committed-unverified``, advances
  nothing, and refuses the next write session (AE13).
* A capture that fails its integrity check blocks the commit behind it.
* A run holding an un-imported XML output reports that state and refuses to write
  a database surface for a row that does not exist.
* A nested session acquisition in one process is refused as a programming error
  rather than reported as a foreign lock holder.

Plus:

* The residual finding "The backup restore is not yet bound to the
  destructive-session gates". The backup restore passes the same gates, because KTD24 binds them to
  destruction and a restore destroys while writing no database row.
* The runtime half of R17's fifth surface: a real analysis file is moved while a
  session is open and the session refuses.

Everything is hermetic. The volume identity, the terminal probe, the process
liveness answer and the database handle are all injected, so no test depends on
what is mounted, what is running, or whether anybody is sitting at a terminal.
"""

from __future__ import annotations

import inspect
import json
import os
import re
import stat
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import config, locations, preflight, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.tools import backup
from tests import _mounts
from tests.test_config import valid_data

UTC = timezone.utc

#: The identity the fixture library records. Read from the config rather than
#: restated, wherever it is used.
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
    """The real gates with only the platform seams injected.

    Everything that would otherwise depend on this machine is supplied: the
    volume identity, and nothing else. The refusals themselves are real.
    """
    arguments = {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}
    arguments.update(overrides)
    return arguments


@pytest.fixture
def volume_matches(cfg, monkeypatch):
    """Make the platform's own identity probe agree with what the library recorded.

    Patched at the PRECONDITION seam rather than passed into the gate, so the
    tests below drive the gates with no seam injected at all, which is exactly
    how a caller that supplies nothing reaches them. Without this the volume
    refusal fires first and the result depends on which disk the temporary
    directory happens to be on.
    """
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


def acknowledge(cfg, **kwargs):
    """Mint an acknowledgment with the terminal check answered yes."""
    return session.record_acknowledgment(cfg, terminal=lambda: True, **kwargs)


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


# ═══════════════════════════════════════════════════════════════════════════
# The three gates: three codes, and nothing written on any refused path
# ═══════════════════════════════════════════════════════════════════════════


def test_the_three_refusals_carry_three_distinct_codes_and_write_nothing(cfg):
    """AE5 and AE19 together, asserted against the filesystem rather than assumed.

    "Zero writes" is the assertion people skip because it looks obvious. It is
    not: a gate that took the lock before checking the acknowledgment would leave
    a file behind on a refused path, and every other assertion here would still
    pass.
    """
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())

    def refuse_with(**arguments):
        before = state_fingerprint(*roots)
        with pytest.raises(CratekitError) as excinfo:
            with session.assert_gates(cfg, workflow="a-destructive-workflow", **arguments):
                raise AssertionError("the gates admitted a session they should have refused")
        assert state_fingerprint(*roots) == before, "a refused session left a trace"
        return excinfo.value.cause

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
    """The order is the property, not a preference.

    With the wrong disk mounted, the acknowledgment file and the lock both sit on
    a volume that is not this library. Reading either one first would answer a
    question about somebody else's disk, and "no acknowledgment recorded" is a
    perfectly convincing answer to get from the wrong library.
    """
    acknowledge(cfg)
    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(
            cfg,
            workflow="a-destructive-workflow",
            identity_provider=foreign_identity,
            mount_enumerator=lambda: (),
        ):
            pass
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert not session.lock_path(cfg).exists(), "the lock was created before the volume check"


@pytest.mark.parametrize("state", sorted(preflight.MountState, key=str))
def test_every_mount_verdict_has_a_declared_refusal_slug(state):
    """P3. A verdict added with no entry must fail here rather than fall through.

    A new mount state falling through to a default is how a refusal ends up
    wearing an unrelated code, which is the collapse the cause registry exists to
    prevent.
    """
    from cratekit.core.cause import REASONS

    if state is preflight.MountState.OK:
        assert state not in session._MOUNT_REASONS
        return
    slug = session._MOUNT_REASONS[state]
    assert REASONS[slug] is ExitCode.LIBRARY_UNAVAILABLE


# ═══════════════════════════════════════════════════════════════════════════
# The volume gate, for every volume a prefix rule points at
# ═══════════════════════════════════════════════════════════════════════════

_RECORDED_ELSEWHERE = "/recorded/on/another/machine"
_ARCHIVE = "AAAA-1111-the-archive"


@pytest.mark.parametrize("state", sorted(preflight.MountState, key=str))
def test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once(state):
    """A verdict is a pass or a declared refusal, and never both or neither.

    Two tables rather than one, so the property needs saying: a state in neither
    falls through to a default slug nobody chose, and a state in both passes
    while a reader of the refusal table believes it refuses.
    """
    from cratekit.core.cause import REASONS

    proved = state in session._MAPPED_PROVED
    refused = state in session._MAPPED_REASONS
    assert proved != refused
    if refused:
        assert REASONS[session._MAPPED_REASONS[state]] is ExitCode.LIBRARY_UNAVAILABLE


def test_the_verdicts_that_prove_a_rule_target_are_spelled_out():
    """The pass set, as a literal, because widening it is how the gate opens.

    ``LIBRARY_PATH_MISSING`` passes on purpose: the identity matched and only
    the directory is absent, which the pass following the rule asks about per
    row. Nothing else may join it without this line changing.
    """
    assert session._MAPPED_PROVED == {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
    }


def test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing(cfg, tmp_path):
    """Three answers, and the third is None rather than the library's identity.

    Defaulting the third to the library's identity is the hole: a library on the
    boot disk and an empty directory left standing where an external drive
    mounts are ON THE SAME DISK, so that default matches.
    """
    root = Path(cfg.library.root)
    own = locations.PrefixRule(_RECORDED_ELSEWHERE, str(root / "Old"), _ARCHIVE)
    inside = locations.PrefixRule(_RECORDED_ELSEWHERE, str(root / "Old"))
    the_root_itself = locations.PrefixRule(_RECORDED_ELSEWHERE, str(root))
    beside = locations.PrefixRule(_RECORDED_ELSEWHERE, str(root) + "-archive")
    outside = locations.PrefixRule(_RECORDED_ELSEWHERE, str(tmp_path / "archive"))

    assert session.expected_rule_identity(cfg, own) == _ARCHIVE
    assert session.expected_rule_identity(cfg, inside) == cfg.library.volume_id
    assert session.expected_rule_identity(cfg, the_root_itself) == cfg.library.volume_id
    assert session.expected_rule_identity(cfg, beside) is None, (
        "a directory whose NAME starts with the library root is not inside it"
    )
    assert session.expected_rule_identity(cfg, outside) is None


def _mapped(cfg, rules, **seams):
    return session.assert_mapped_volume_identities(cfg, rules, **seams)


def test_a_rule_onto_the_volume_it_recorded_passes(cfg, tmp_path, monkeypatch):
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)

    proved = _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE)])

    assert [status.state for status in proved] == [preflight.MountState.OK]
    assert proved[0].observed_identity == _ARCHIVE


def test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule(
    cfg, tmp_path, monkeypatch
):
    """R-44 Open 1. The decoy at the mount path is exactly the disk a rule reaches.

    The second rule is the wrong one, so the index in the refusal is evidence
    that every rule was asked rather than the first.
    """
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: "BBBB-a-decoy"}, otherwise=cfg.library.volume_id)
    rules = [
        locations.PrefixRule("/an/older/root", str(Path(cfg.library.root) / "Music")),
        locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE),
    ]

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, rules)

    cause = excinfo.value.cause
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
    """R-51. What an unclean eject leaves behind passes every existence check.

    The directory is there, so ``stat`` is satisfied, and it sits on whichever
    disk holds the mount path, so the identity read for it is that disk's. With
    nothing enumerated as mounted, the recorded volume is simply somewhere else.
    """
    stale = tmp_path / "Volumes" / "ARCHIVE"
    stale.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(stale), _ARCHIVE)])

    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert excinfo.value.cause.detail["state"] == str(preflight.MountState.FOREIGN_VOLUME)


def test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug(
    cfg, tmp_path, monkeypatch
):
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id)
    absent = tmp_path / "Volumes" / "ARCHIVE"

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(absent), _ARCHIVE)])

    assert excinfo.value.cause.reason == "mapped-volume-unmounted"
    assert str(absent) in excinfo.value.cause.remediation.steps[0]


def test_a_recorded_volume_mounted_somewhere_else_says_where(cfg, tmp_path, monkeypatch):
    actually = tmp_path / "Volumes" / "ARCHIVE 1"
    actually.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {actually: _ARCHIVE}, otherwise=cfg.library.volume_id)
    configured = tmp_path / "Volumes" / "ARCHIVE"

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(configured), _ARCHIVE)])

    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert str(actually.resolve()) in excinfo.value.cause.remediation.steps[0]


def test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity(
    cfg, tmp_path, monkeypatch
):
    """The refusal a person meets the day this gate arrives, one edit from a run.

    It names the rule by its config key and the identity the disk shows NOW, so
    the act is "check that is the right disk, then record it", not a search for
    how to read a volume identity.
    """
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive))])

    cause = excinfo.value.cause
    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["state"] == str(preflight.MountState.IDENTITY_NOT_RECORDED)
    assert cause.detail["observed_identity"] == _ARCHIVE
    step = cause.remediation.steps[0]
    assert _ARCHIVE in step and "library.location_prefix_map[0]" in step and "volume_id" in step


def test_a_volume_nested_under_the_library_root_is_not_the_library(cfg, monkeypatch):
    """The inside-the-root answer is an ASSERTION of the library's identity, not a pass."""
    nested = Path(cfg.library.root) / "Archive"
    nested.mkdir()
    _mounts.stand_in(monkeypatch, {nested: "BBBB-nested"}, otherwise=cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(nested))])

    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert excinfo.value.cause.detail["recorded_identity"] == cfg.library.volume_id


def test_a_rule_target_whose_identity_cannot_be_read_refuses(cfg, tmp_path, monkeypatch):
    """Destructive strength. "I could not look" is not "it is the right disk"."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: None}, otherwise=cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE)])

    assert excinfo.value.cause.detail["state"] == str(preflight.MountState.IDENTITY_UNAVAILABLE)


def test_a_matched_volume_with_the_directory_absent_is_left_to_the_pass_that_follows_the_rule(
    cfg, tmp_path, monkeypatch
):
    """The one non-OK pass, and the reason is that the identity question was answered."""
    archive = tmp_path / "Volumes" / "ARCHIVE"
    archive.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {archive: _ARCHIVE}, otherwise=cfg.library.volume_id)
    rule = locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive / "never-made"), _ARCHIVE)

    proved = _mapped(cfg, [rule])

    assert [status.state for status in proved] == [preflight.MountState.LIBRARY_PATH_MISSING]


def test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it(
    cfg, tmp_path, monkeypatch
):
    """The review's first finding, and the way a correct looking config reopens R-51.

    An ejected drive leaves its mount point on the disk that holds the mount
    directory. A rule that recorded THAT disk's identity, because a refusal once
    offered it or because the library shares the disk, matches the leftover
    directory perfectly. So the slot is asked about before any identity is
    compared, and what is recorded cannot talk it round.
    """
    volumes = tmp_path / "Volumes"
    leftover = volumes / "ARCHIVE"
    leftover.mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise=cfg.library.volume_id, slots_under=volumes)
    rule = locations.PrefixRule(_RECORDED_ELSEWHERE, str(leftover), cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [rule])

    assert excinfo.value.cause.reason == "mapped-volume-unmounted"
    assert excinfo.value.cause.detail["state"] == "mount_slot_empty"


def test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record(
    cfg, tmp_path, monkeypatch
):
    """The refusal that hands over an identity must not hand over the wrong disk's.

    Nothing recorded, drive ejected, mount point left behind. A walk upward from
    there reads the disk holding the mount directory, and a step saying "it
    identifies as that, record it" is an instruction to disarm this gate for
    good. The identity named here belongs to no volume in the test, so its
    absence from the whole refusal is the assertion.
    """
    volumes = tmp_path / "Volumes"
    (volumes / "ARCHIVE").mkdir(parents=True)
    _mounts.stand_in(monkeypatch, {}, otherwise="CCCC-the-boot-disk", slots_under=volumes)
    rule = locations.PrefixRule(_RECORDED_ELSEWHERE, str(volumes / "ARCHIVE"))

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [rule])

    cause = excinfo.value.cause
    assert cause.reason == "mapped-volume-unmounted"
    said = cause.message + " ".join(cause.remediation.steps) + json.dumps(cause.detail)
    assert "CCCC-the-boot-disk" not in said


def test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record(
    cfg, monkeypatch
):
    """The wording half. The identity compared was the LIBRARY'S, and the refusal says so.

    "The volume recorded on that rule" names a record that does not exist for a
    rule inside the library root, and "record it as that rule's volume_id" would
    invite a person to pin a nested disk as the answer.
    """
    nested = Path(cfg.library.root) / "Archive"
    nested.mkdir()
    _mounts.stand_in(monkeypatch, {nested: "BBBB-nested"}, otherwise=cfg.library.volume_id)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(nested))])

    cause = excinfo.value.cause
    assert "the library's volume" in cause.message
    assert "recorded on that rule" not in cause.message
    assert "volume_id" not in cause.remediation.steps[0]


def test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback(
    cfg, tmp_path, monkeypatch
):
    """The review's third finding. "I could not look" reaches a person as a refusal.

    The walk to a mount raises on a directory this account cannot traverse, and
    an ``OSError`` escaping a gate arrives at the command line as an internal
    defect with no slug, no exit code and no step.
    """
    archive = tmp_path / "archive"
    archive.mkdir()

    def cannot_walk(_path):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(preflight, "identity_source", cannot_walk)

    with pytest.raises(CratekitError) as excinfo:
        _mapped(cfg, [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE)])

    assert excinfo.value.cause.reason == "mapped-volume-mismatch"
    assert excinfo.value.cause.detail["state"] == "unreachable"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too(cfg, tmp_path):
    """The same finding at its second site, the read made while building the refusal."""
    archive = tmp_path / "archive"
    archive.mkdir()

    def provider(_path):
        raise PermissionError(13, "Permission denied")

    with pytest.raises(CratekitError) as excinfo:
        _mapped(
            cfg,
            [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive))],
            identity_provider=provider,
            mount_enumerator=lambda: (),
        )
    assert excinfo.value.cause.detail["state"] == "unreachable"


def test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points(
    cfg, tmp_path, monkeypatch
):
    """The review's fourth finding. A second volume inside the first is a third disk.

    The rule's target is on the archive and proves itself. One directory under
    it has another volume mounted in it, and a file in THAT directory would be
    trashed on a disk nothing identified. Both halves are asserted, because a
    probe that refuses everything passes the second half alone.
    """
    archive = tmp_path / "Volumes" / "ARCHIVE"
    inner = archive / "Music" / "On Another Disk"
    inner.mkdir(parents=True)
    (archive / "Music" / "Here").mkdir()
    _mounts.stand_in(
        monkeypatch, {archive: _ARCHIVE, inner: "BBBB-inner"}, otherwise=cfg.library.volume_id
    )
    rules = [
        locations.PrefixRule("/an/older/root", str(Path(cfg.library.root) / "Music")),
        locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE),
    ]
    assert len(_mapped(cfg, rules)) == 2

    held = session.assert_mapped_file_volume(
        cfg, rules, 1, archive / "Music" / "Here" / "a.flac"
    )
    assert held.ok and held.observed_identity == _ARCHIVE

    with pytest.raises(CratekitError) as excinfo:
        session.assert_mapped_file_volume(cfg, rules, 1, inner / "a.flac")

    cause = excinfo.value.cause
    assert cause.reason == "mapped-volume-mismatch"
    assert cause.detail["rule"] == 1 and cause.detail["probed"] == str(inner)
    assert cause.detail["observed_identity"] == "BBBB-inner"


def test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug(
    cfg, tmp_path, monkeypatch
):
    """The review's eighth finding. The table is indexed, so an undecided state is loud."""
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
            [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive), _ARCHIVE)],
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

    with pytest.raises(CratekitError) as excinfo:
        _mapped(
            cfg,
            [locations.PrefixRule(_RECORDED_ELSEWHERE, str(archive))],
            identity_provider=provider,
            mount_enumerator=lambda: (),
        )
    assert excinfo.value.cause.detail["observed_identity"] == _ARCHIVE
    assert seen, "the refusal read the identity through some other provider"


# ═══════════════════════════════════════════════════════════════════════════
# The lock
# ═══════════════════════════════════════════════════════════════════════════


def test_a_second_process_refuses_and_names_the_holder(cfg):
    """AE19. Naming the holder is the difference between waiting and guessing."""
    with session.session_lock(cfg):
        recorded = session.read_lock_holder(session.lock_path(cfg))
        assert recorded is not None
        assert recorded.pid == os.getpid()
        assert recorded.host and recorded.boot and recorded.started

        # A separate handle on the same file is what a second process looks like
        # to the kernel, so the in-process composition check must not see it.
        session._HELD.discard(str(session.lock_path(cfg).absolute()))
        with pytest.raises(CratekitError) as excinfo:
            with session.session_lock(cfg):
                pass
    cause = excinfo.value.cause
    assert cause.code is ExitCode.LIBRARY_BUSY
    assert str(os.getpid()) in cause.message


def test_a_nested_session_is_a_programming_error_not_a_foreign_holder(cfg):
    """The distinction matters because the two remedies are opposite.

    A foreign holder is waited for. A session nested inside another in ONE
    process can never resolve: the caller would be told to wait for itself,
    forever, and the report would name the run that is stuck as the thing
    blocking it.
    """
    with session.session_lock(cfg):
        with pytest.raises(session.SessionComposition) as excinfo:
            with session.session_lock(cfg):
                pass
    cause = excinfo.value.cause
    assert cause.code is ExitCode.INTERNAL
    assert cause.reason != "session-lock-held"
    assert "nest" in cause.message


def test_the_lock_file_is_never_unlinked_and_is_private_under_any_umask(cfg):
    """Unlinking a lock file is how two processes both come to believe they hold it.

    The first holds a lock on the inode and unlinks the NAME; the second creates
    a fresh file at that name and locks that instead, with nothing raised.
    """
    previous = os.umask(0)
    try:
        with session.session_lock(cfg) as held:
            assert held.exists()
            assert stat.S_IMODE(held.stat().st_mode) == config.PRIVATE_FILE_MODE
            assert (
                stat.S_IMODE(held.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
            )
        assert held.exists(), "the lock file was unlinked on release"
    finally:
        os.umask(previous)


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
        with pytest.raises(CratekitError) as excinfo:
            session.release_stale_lock(cfg)
    assert excinfo.value.cause.code is ExitCode.LIBRARY_BUSY


def test_a_holder_on_another_machine_or_another_boot_is_assumed_alive(cfg):
    """Fails towards alive on every question this process cannot answer.

    Guessing "dead" would let one machine clear another machine's claim on the
    library, and the operation the lock protects is the one that removes files.
    """
    here = session.current_holder()
    other_host = session.Holder(
        host="another-machine", boot=here.boot, pid=here.pid, started=here.started
    )
    other_boot = session.Holder(
        host=here.host, boot="0", pid=here.pid, started=here.started
    )
    assert session.holder_alive(other_host) is True
    assert session.holder_alive(other_boot) is True


def test_the_holder_carries_all_four_identifying_fields(cfg):
    """A bare process identifier is meaningless across machines and is reused."""
    holder = session.current_holder()
    assert {"host", "boot", "pid", "started"} == set(holder.to_json())
    assert session.Holder.from_json(holder.to_json()) == holder


# ═══════════════════════════════════════════════════════════════════════════
# The acknowledgment (KTD18, R34)
# ═══════════════════════════════════════════════════════════════════════════


def test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment(cfg):
    """The gate protecting the operation that removes files is not self-servable."""
    with pytest.raises(CratekitError) as excinfo:
        session.record_acknowledgment(cfg, terminal=lambda: False)
    cause = excinfo.value.cause
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.reason == "backup-acknowledgment-no-terminal"
    assert session.read_acknowledgment(cfg) is None


def test_the_terminal_check_is_a_terminal_check_and_not_a_standard_input_read():
    """R33 still holds. A terminal check does not consume a byte from anywhere.

    Derived from the source rather than asserted about behaviour, because the
    property is the ABSENCE of a read and absence is only visible structurally.
    """
    import ast

    source = Path(session.__file__).read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            raise AssertionError("the session module names standard input")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"input", "raw_input"}


def test_the_recorded_actor_is_derived_from_the_invocation_and_never_supplied():
    """R34's sharpest clause, asserted by INTROSPECTION rather than by reading.

    If a caller could name the actor, an agent driving the command line would
    mint the gate and sign somebody else's name to it. So the assertion is that
    no parameter could carry one, which stays true when the function is edited.
    """
    parameters = inspect.signature(session.record_acknowledgment).parameters
    assert not [name for name in parameters if "actor" in name.lower()]
    assert not [name for name in parameters if "user" in name.lower()]


def test_the_acknowledgment_records_the_backup_age_that_was_shown(cfg):
    """KTD18. An acknowledgment with no age is a click, not a decision.

    The portions are DERIVED from the backup fact vocabulary, so a portion added
    later cannot be silently absent from what a person was shown.
    """
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
    with pytest.raises(CratekitError) as excinfo:
        session.assert_backup_acknowledged(cfg, now=now + timedelta(hours=2))
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
    assert excinfo.value.cause.detail["expired"] is True


def test_the_acknowledgment_file_is_private_under_any_umask(cfg):
    previous = os.umask(0)
    try:
        acknowledge(cfg)
    finally:
        os.umask(previous)
    mode = stat.S_IMODE(session.ack_path(cfg).stat().st_mode)
    assert mode == config.PRIVATE_FILE_MODE


def test_no_blanket_affirmative_satisfies_the_acknowledgment(cfg):
    """AE20 and R34. Three affirmative surfaces exist, and all three are closed.

    R34 names a flag, a configuration key, and an environment variable, so each
    one is checked in the shape it would actually take, and each check is derived
    rather than restated.

    1. A FLAG would be a boolean parameter on the gate or on the consult. The set
       is read from the signatures, so a parameter added later is covered.
    2. A CONFIGURATION KEY would be a module toggle, which is the only boolean
       surface the configuration schema has. Every declared module is switched
       on, iterating the profile module registry rather than naming any of them.
    3. An ENVIRONMENT VARIABLE cannot satisfy something the code never reads, so
       the whole acknowledgment path is scanned for an environment read. That is
       structural on purpose: a behavioural test would have to guess the variable
       name, and the one that mattered would be the name nobody guessed. BOTH
       HALVES of the path are scanned: the CONSULT, which a session runs, and
       the MINT, which writes the record a session consults. Scanning only the
       consult would leave a variable free to decide who the record says was
       here, which is the same gate answered one step earlier.
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

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
            pass
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED

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


# ═══════════════════════════════════════════════════════════════════════════
# The session log
# ═══════════════════════════════════════════════════════════════════════════


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
    previous = os.umask(0)
    try:
        record = session.open_session(cfg, workflow="a-destructive-workflow")
    finally:
        os.umask(previous)
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
    with pytest.raises(CratekitError):
        session.close_session(record, cfg, state=session.SessionState.AWAITING_IMPORT)


def test_an_unreadable_record_does_not_stop_the_log_being_read(cfg):
    good = session.open_session(cfg, workflow="a-destructive-workflow")
    (session.log_dir(cfg) / "damaged.json").write_text("{not json")
    assert [r.session_id for r in session.records(cfg)] == [good.session_id]


# ═══════════════════════════════════════════════════════════════════════════
# One source per run (R29)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refusal_at_source_two_leaves_source_one_committed_and_names_both(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two", "three")
    )

    def run_one(source):
        if source == "two":
            raise refuse("refused-by-policy", "source two is not acceptable")
        return session.ChangeSummary((session.TreeChange(tree=f"tree-{source}", created=1),))

    with pytest.raises(CratekitError) as excinfo:
        session.commit_sources(record, ("one", "two", "three"), run_one, cfg=cfg)

    cause = excinfo.value.cause
    assert cause.detail["committed"] == ["one"]
    assert cause.detail["refused_source"] == "two"
    assert set(cause.detail["remaining"]) == {"two", "three"}
    assert cause.inner is not None and cause.inner.reason == "refused-by-policy"

    # And the same facts are on disk, not only in the exception.
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

    with pytest.raises(CratekitError):
        session.commit_sources(record, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two"]

    resumed = session.read_record(record.session_id, cfg)
    session.commit_sources(resumed, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two", "two"], "a committed source was run again"
    assert resumed.committed_sources() == ("one", "two")
    assert {entry.tree for entry in resumed.change.trees} == {"tree-one", "tree-two"}


# ═══════════════════════════════════════════════════════════════════════════
# The capture gate, and the post-commit read-back (AE13)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_capture_that_failed_its_check_blocks_the_commit_behind_it(cfg):
    record = snapshot.capture(cfg, verifier=lambda _path: False)
    with pytest.raises(CratekitError) as excinfo:
        snapshot.assert_verified(record)
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_read_back_that_disagrees_ends_committed_unverified_and_advances_nothing(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two")
    )
    session.attach_capture(record, "/captures/one/master.db", cfg)
    record.sources["one"] = str(session.SourceState.COMMITTED)
    record.change = session.ChangeSummary((session.TreeChange("tree-one", created=4),))
    session.write_record(record, cfg)

    disposed: list[str] = []

    class Engine:
        def dispose(self):
            disposed.append("engine")

    class Handle:
        session = object()
        engine = Engine()

        def close(self):
            disposed.append("session")

    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(
            record,
            cfg,
            expect=lambda _db: False,
            reopen=Handle,
        )
    cause = excinfo.value.cause
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
    """Closing a database does not release it: the pooled connection stays open.

    A restore over a file this process still holds produces an input-output error
    against a database that is perfectly intact, which reads as a corrupt restore
    at the worst possible moment. The full release is asserted rather than
    assumed, because the binding's own close looks like it is enough.
    """
    disposed: list[str] = []

    class Engine:
        def dispose(self):
            disposed.append("engine")

    class Handle:
        session = object()
        engine = Engine()

        def close(self):
            disposed.append("session")

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    assert session.verify_commit(record, cfg, expect=lambda _db: True, reopen=Handle) is True
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
    with pytest.raises(CratekitError):
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
            pass
    assert excinfo.value.cause.reason == "session-committed-unverified"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_an_unresolved_session_keeps_its_capture_out_of_the_pruner(cfg):
    """The state is deliberately non-terminal, and this is what that buys."""
    capture_path = cfg.library.root / "captures" / "one" / "master.db"
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, capture_path, cfg)
    with pytest.raises(CratekitError):
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    assert rb_writer.default_protected_snapshot_paths(cfg) == {capture_path.resolve()}


# ═══════════════════════════════════════════════════════════════════════════
# The un-imported XML output as a first-class state
# ═══════════════════════════════════════════════════════════════════════════


def test_a_run_holding_an_unimported_output_refuses_a_database_surface(cfg):
    """XML surfaces are strictly upstream of database surfaces within a run.

    The XML is what creates the row. A database surface written before the import
    addresses a row the database does not contain, so the refusal is not caution,
    it is the invariant.
    """
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

    with pytest.raises(CratekitError) as excinfo:
        session.assert_database_surface_allowed(record)
    cause = excinfo.value.cause
    assert cause.code is ExitCode.PENDING_HUMAN
    assert cause.reason == "awaiting-import"
    assert cause.detail["verify_verb"] == "run.show"

    persisted = session.read_record(record.session_id, cfg)
    assert persisted.state is session.SessionState.AWAITING_IMPORT
    assert persisted.pending is not None
    assert persisted.pending.blocks == ("route.inbox",)


def test_the_pending_action_is_the_one_the_command_line_layer_already_enforces(cfg):
    """Connected to the existing mechanism rather than a parallel one.

    The command-line layer's own check refuses any verb named in ``blocks`` while
    the action is outstanding. Feeding the session's action straight into it is
    what makes the state load-bearing instead of advisory.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The runtime half of R17's fifth surface
# ═══════════════════════════════════════════════════════════════════════════


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
    """A REAL moved file, not an assertion that a function exists.

    This is the half the source scan cannot do. It forbids every symbol that
    serialises one of these files, and reading them stays legal by decision, so a
    grid rewritten through a handle the binding already returned names none of
    the forbidden symbols and is invisible to it.
    """
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
    # And reading them is still perfectly legal.
    with session.analysis_files_unmoved([tmp_path / "library"]):
        for path in session.analysis_files_under([tmp_path / "library"]):
            path.read_bytes()


def test_the_gates_can_arm_the_analysis_watch_for_the_body_of_a_session(cfg, tmp_path):
    """Composed at the one place every destructive session passes through.

    The roots are supplied by the caller rather than defaulted to the library
    root, because the alternative is walking a whole music volume on every
    session to watch files nothing intends to open. The default of watching
    nothing is closed by the countdown below.
    """
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
    """P5. The countdown that closes this unit's own softening path.

    Three obligations, all on the unit that lands the tree writers, and none of
    them enforceable from here today because the module does not exist:

    * pass the three gates rather than re-deriving any of them;
    * commit behind a capture that VERIFIED, which is what makes the undo real;
    * name the analysis roots it could touch, so the watch that is the runtime
      half of R17's fifth surface actually watches something.

    The third is the one that matters most, because the default is to watch
    nothing and a default that silently does nothing is exactly the shape a
    docstring assertion fails to prevent.

    ARMED AGAINST THE SYNTAX TREE, NOT THE SOURCE TEXT, and that distinction is
    the whole guard. Written as a substring search this passed the moment the
    module's own docstring explained why it calls these three, which is exactly
    what a module documenting its obligations does. The guard would then have
    survived every one of the calls being deleted. A docstring that satisfies
    the test written to check the docstring's claim is not a countdown, it is
    the softening path wearing the guard's clothes. The sibling obligation in
    tests/test_tree_registry.py already walks calls for this reason; this one
    now matches it.
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
    """P4. The claim is about a real API, so it is checked against that API.

    The alternatives are pulled out of the binding's own compiled pattern rather
    than retyped, so a binding that learns a fourth name fails here instead of
    quietly leaving one file unwatched.
    """
    from pyrekordbox.anlz import RE_ANLZ

    alternatives = re.search(r"\(([^)]*)\)", RE_ANLZ.pattern).group(1).split("|")
    assert alternatives, "the binding's pattern has no alternation, so the walk is broken"
    for suffix in alternatives:
        assert session.is_analysis_file(f"ANLZ0000.{suffix}"), suffix


def test_the_watched_set_covers_every_file_surface_five_declares():
    """And WIDER than the binding, deliberately.

    The binding recognises three names. R17's fifth surface declares four, and
    the fourth is a real grid-bearing file, so recognising only what the binding
    recognises would leave one unwatched. The four are read from that surface's
    own declaration rather than retyped here.
    """
    import tests.test_no_beatgrid_ever as surface_five

    declared = set(re.findall(r"``\.([0-9A-Z]{3})``", surface_five.__doc__))
    assert len(declared) == 4, f"surface five declares {sorted(declared)}"
    for suffix in declared:
        assert session.is_analysis_file(f"ANLZ0001.{suffix}"), suffix
    assert not session.is_analysis_file("ANLZ0001.TXT")
    assert not session.is_analysis_file("something.DAT")


# ═══════════════════════════════════════════════════════════════════════════
# The residual finding "The backup restore is not yet bound to the
# destructive-session gates": the backup restore passes the same gates
# ═══════════════════════════════════════════════════════════════════════════


def test_the_backup_restore_passes_the_destructive_session_gates(volume_matches, cfg, tmp_path):
    """KTD24. A restore destroys a library and writes no database row.

    A rule that bound the gates to database WRITES would leave the single most
    destructive operation in the product outside the safety spine entirely.
    """
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
    """The decision, asserted. See ``run_restore`` for the three reasons.

    The lock is the one that matters: a rehearsal running while another
    destructive session writes describes a library that is changing underneath
    it, so its preview is a report about a world that no longer exists.
    """
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
    """``cfg`` is required, so there is no way to reach it with nothing to gate on.

    An optional configuration would be a softening path: a caller that omitted it
    would get an ungated restore and no error, which is the shape P5 exists to
    close in the same commit that creates it.
    """
    parameters = inspect.signature(backup.run_restore).parameters
    assert parameters["cfg"].default is inspect.Parameter.empty
    assert parameters["cfg"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD


def test_every_backup_refusal_carries_one_code_in_both_cause_tables():
    """The two vocabularies agree about every refusal a verb can now surface.

    U27 is what made this matter. ``modules.tools.backup`` raises its own
    ``Refusal`` enum, and until ``restore run --from-backup`` landed nothing
    carried one out to a person, so the slugs lived only in
    ``cratekit.cli.exit_codes``, which holds the per-slug remediation, and not in
    ``cratekit.core.cause.REASONS``, which holds the status. A ``Cause`` built on
    an undeclared reason raises, so the verb would have crashed at the boundary
    it exists to translate.

    DERIVED FROM THE ENUM, NEVER LISTED (P3). A member added to ``Refusal`` later
    is covered on the day it appears, which is the whole difference between this
    and the hand-listed set it replaces. The reverse direction is already held by
    ``modules.tools.backup``'s own suite, which asserts every reserved slug is
    reachable.

    AND IT COMPARES THE CODES RATHER THAN MERE PRESENCE. Two tables that both
    know a slug and disagree about its status is worse than one that has never
    heard of it: the envelope and the process status would then describe
    different failures, which is the collapse KTD25 is about.
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


# ═══════════════════════════════════════════════════════════════════════════
# The latch has an exit, the log fails CLOSED, and the guards run on both paths
#
# Everything below was found by an adversarial read of this unit's own diff.
# Each one is a property the tests above asserted the happy half of and left the
# other half free to move.
# ═══════════════════════════════════════════════════════════════════════════


def _condemn(cfg):
    """Leave this library with one unresolved ``committed-unverified`` session."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, "/captures/one/master.db", cfg)
    with pytest.raises(CratekitError):
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)
    return record


def test_a_condemned_library_still_admits_the_recovery_its_remedy_names(cfg):
    """The latch may not condemn its own way out.

    ``verify_commit`` refuses with ``restore-from-snapshot``. A restore is itself
    a destructive session, so a latch that refused every destructive session
    would refuse the remedy it had just printed, and the library would have no
    exit but a hand-edited file in its own log.
    """
    acknowledge(cfg)
    condemned = _condemn(cfg)

    with pytest.raises(CratekitError) as refused:
        with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
            pass
    assert refused.value.cause.reason == "session-committed-unverified"

    with session.assert_gates(
        cfg,
        workflow="a-recovery-workflow",
        intent=session.Intent.RECOVERY,
        **open_gates(cfg),
    ) as held:
        assert held.intent is session.Intent.RECOVERY
    assert condemned.session_id


def test_a_recovery_session_is_exempt_from_the_latch_and_from_nothing_else(cfg):
    """One gate, not three. A recovery is still gated on all three.

    Declaring the intent buys exactly one thing. If it bought the acknowledgment
    too it would be the blanket affirmative R34 forbids, wearing a different
    word.
    """
    _condemn(cfg)
    recovery = {
        "workflow": "a-recovery-workflow",
        "intent": session.Intent.RECOVERY,
    }

    with pytest.raises(CratekitError) as no_ack:
        with session.assert_gates(cfg, **recovery, **open_gates(cfg)):
            pass
    assert no_ack.value.cause.code is ExitCode.ACK_REQUIRED

    acknowledge(cfg)
    with pytest.raises(CratekitError) as wrong_disk:
        with session.assert_gates(
            cfg, **recovery, identity_provider=foreign_identity, mount_enumerator=lambda: ()
        ):
            pass
    assert wrong_disk.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE

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
    """End to end through the real module, which is where the deadlock was.

    Before the intent existed, a condemned library refused ``plan_restore`` with
    the very reason whose remedy is a restore.
    """
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
    """The session log SURVIVES a rollback, deliberately, so the record outlives it.

    A user who did exactly what the refusal asked would otherwise find the next
    write still refused, with the remedy already spent.
    """
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
    with pytest.raises(CratekitError) as excinfo:
        session.resolve_unverified_session(record.session_id, cfg)
    assert excinfo.value.cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert session.read_record(record.session_id, cfg).state is session.SessionState.OPEN


def test_the_latch_refuses_a_record_this_build_cannot_read(cfg):
    """The gate reads the log STRICTLY. A tolerant reader fails OPEN.

    A schema bump on one file, or a state value a later build introduced, would
    otherwise make an unresolved commit vanish from the scan and admit the next
    destructive session against a library nobody can vouch for. Both shapes are
    driven, because they fail through different exceptions.
    """
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
    """The store is LIBRARY scoped, so its filenames land on the user's own disk.

    exFAT and FAT are ordinary choices for a library volume because that is what
    a CDJ reads, and neither accepts a colon; on Windows a colon is the
    alternate-data-stream separator. ``snapshot.new_stamp`` says exactly this in
    the same package. The identifier keeps its colons, because addressability and
    filename legality are different questions.
    """
    identifier = session.new_session_id()
    assert ":" in identifier, "the identifier space is the run identifier space"

    name = session.log_path(identifier, cfg).name
    assert not (set(name) & set(r'<>:"/\|?* ')), name
    assert name.isascii()

    # And the identifier the record carries is the un-sanitised one, so a support
    # conversation still refers to one identifier space.
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    written = json.loads(session.log_path(record.session_id, cfg).read_text())
    assert written["session_id"] == record.session_id
    assert session.read_record(record.session_id, cfg).session_id == record.session_id


def test_a_supplied_identifier_cannot_compose_a_path(cfg):
    """``open_session`` accepts one, and a separator in it would escape the store.

    A record outside the directory the pruning scan reads is a session that
    protects no capture and that no gate can see.
    """
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", session_id="../../escaped"
    )
    written = session.log_path(record.session_id, cfg)
    assert written.parent == session.log_dir(cfg)
    assert written.exists()
    assert session.records(cfg)[0].session_id == "../../escaped"


def test_a_per_source_refusal_widens_the_scope_and_never_narrows_it(cfg):
    """The blast radius is DECLARED, and a wrapper knows less than the thing it wraps.

    ``commit_sources`` knows one source refused. It does not know how much the
    underlying cause condemns. A drive ejected mid-run condemns the whole run,
    and rewriting that to one source tells the aggregate at boundary 4 that the
    sources beside it may advance their watermarks against a library that is no
    longer mounted.
    """
    from cratekit.core.cause import Scope

    def refusing_at(scope):
        record = session.open_session(
            cfg, workflow="a-destructive-workflow", sources=("one",)
        )

        def run_one(_source):
            raise refuse("refused-by-policy", "not this time", scope=scope)

        with pytest.raises(CratekitError) as excinfo:
            session.commit_sources(record, ("one",), run_one, cfg=cfg)
        return excinfo.value.cause

    assert refusing_at(Scope.RUN).scope is Scope.RUN
    assert refusing_at(Scope.SESSION).scope is Scope.SESSION
    assert refusing_at(Scope.ITEM).scope is Scope.SOURCE, "the wrapper's own scope applies"
    assert refusing_at(Scope.SOURCE).scope is Scope.SOURCE


def test_a_read_back_that_could_not_run_says_so_rather_than_saying_it_disagreed(cfg):
    """Three facts, one chain, and the recoverable one must not wear the other's face.

    An ejected volume, a drifted pin and a database that will not open are all
    recoverable. "The read-back disagreed" is not. Logging the first and
    reporting the second sends a user to restore a snapshot because a drive is
    unplugged.
    """
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
    """"Could not read" must never be recorded as "nothing to show" (KTD18).

    An acknowledgment whose ``shown`` list is empty is byte for byte what a
    library declaring no portions at all would write, and the remedies for those
    two are unrelated. An acknowledgment with no age is a click, not a decision.
    """
    from cratekit.core import backup_facts

    damaged = backup_facts.path_for(cfg)
    damaged.parent.mkdir(parents=True, exist_ok=True)
    damaged.write_text("{ this is not json")
    with pytest.raises(CratekitError) as excinfo:
        acknowledge(cfg)
    cause = excinfo.value.cause
    assert cause.reason == "backup-facts-unreadable"
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.remediation.remedy is Remedy.REPAIR_BACKUP_FACTS
    assert session.read_acknowledgment(cfg) is None, "a refused mint wrote a record"

    # And the remedy works: an ABSENT file is normal and still mints.
    damaged.unlink()
    assert acknowledge(cfg).shown


def test_a_fact_file_this_account_may_not_open_asks_for_access_not_for_repair(cfg):
    """A permission is not a corruption, and the acts are opposite.

    DRIVEN THROUGH ``read_facts`` RATHER THAN THROUGH A HAND BUILT EXCEPTION,
    because the finding is that a field the raise site sets was discarded, and a
    hand built exception can carry a field the code path never produces. So the
    ``PermissionError`` is made at the file boundary and ``cause.permission_denied``
    classifies it, exactly as it would on a configuration directory this account
    cannot traverse.

    THE PRECONDITION IS ASSERTED RATHER THAN ASSUMED, the way ``no_rclone`` in
    ``tests/test_backup_cli.py`` asserts its own: a run as an account the mode
    bits do not restrain reads the file successfully, and this test would then
    pass over a refusal that never happened.
    """
    from cratekit.core import backup_facts

    locked = backup_facts.path_for(cfg)
    locked.parent.mkdir(parents=True, exist_ok=True)
    locked.write_text("{}")
    locked.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            locked.read_bytes()

        with pytest.raises(CratekitError) as excinfo:
            acknowledge(cfg)
    finally:
        locked.chmod(0o600)

    cause = excinfo.value.cause
    assert cause.reason == "backup-facts-unreadable"
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS, (
        "a person whose configuration directory this account cannot open was "
        "told to repair or reset a file that is very likely intact"
    )
    assert session.read_acknowledgment(cfg) is None, "a refused mint wrote a record"


def test_a_fact_file_from_a_newer_build_asks_for_an_upgrade(cfg):
    """The third token, which travels the same way and had no guard.

    ``read_facts`` raises three remedies and the carry moves all three, so a
    fix measured only on the permission case would leave two thirds of it
    asserted rather than driven.
    """
    from cratekit.core import backup_facts

    newer = backup_facts.path_for(cfg)
    newer.parent.mkdir(parents=True, exist_ok=True)
    newer.write_text(
        json.dumps({"schema_version": backup_facts.SCHEMA_VERSION + 1, "portions": {}})
    )
    with pytest.raises(CratekitError) as excinfo:
        acknowledge(cfg)

    cause = excinfo.value.cause
    assert cause.reason == "backup-facts-unreadable"
    assert cause.remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_the_analysis_watch_runs_even_when_the_session_body_refuses(cfg, tmp_path):
    """The failing path is the one that matters MORE, not the one to skip.

    A session that refused is a session the user retries, so a grid rewritten
    before an unrelated refusal would be rewritten again on the next attempt and
    never once reported. The source scan cannot see this write by construction,
    which is the whole reason the runtime half exists.
    """
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
    """rekordbox analysing while a session runs is what the process guard forbids.

    All three kinds of drift count, and this is the third.
    """
    _analysis_tree(tmp_path / "library")
    fresh = tmp_path / "library" / "PIONEER" / "USBANLZ" / "one" / "ANLZ0002.DAT"
    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            fresh.write_bytes(b"analysed mid session")
    assert excinfo.value.cause.detail["changed"] == [f"{fresh} appeared"]


def test_a_rewrite_inside_one_tick_of_the_clock_is_caught_by_the_size(cfg, tmp_path):
    """The reason the fingerprint carries two signals rather than one.

    A filesystem's timestamp granularity is not infinite, and a grid rewrite
    almost always changes the length of the tag it lives in. The modification
    time is put back deliberately so only the size can carry the assertion.
    """
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
    """The third documented case, which the code did not implement.

    A shared machine that refuses to report another account's process start time
    would otherwise make every live holder read as dead, and the remedy printed
    is "release the stale lock" against a session that is writing right now.
    """
    here = session.current_holder()
    monkeypatch.setattr(session, "process_started", lambda _pid: session.UNKNOWN_IDENTITY)
    assert session.holder_alive(here) is True

    with pytest.raises(CratekitError) as excinfo:
        session.release_stale_lock(cfg, path=_lock_recording(cfg, here))
    assert excinfo.value.cause.remediation.remedy is Remedy.WAIT_FOR_HOLDER


def test_a_holder_whose_process_is_gone_is_still_judged_dead(cfg):
    """The other side of the same change, so failing towards alive stays bounded.

    "This platform will not say" and "there is no such process" are different
    answers, and only the second may clear another run's claim on the library.
    Both probes are the real ones here: a genuinely finished process is used
    rather than a stubbed answer, because a stub would prove only that the stub
    was consulted.
    """
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
    """R34's sharpest clause, asserted as BEHAVIOUR rather than as a signature.

    A signature scan sees a parameter. It does not see an environment read, and
    an agent driving the command line would use an environment read.
    """
    monkeypatch.setattr(session, "derive_actor", lambda: "the-derived-actor")
    recorded = acknowledge(cfg)
    assert recorded.actor == "the-derived-actor"
    assert json.loads(session.ack_path(cfg).read_text())["actor"] == "the-derived-actor"


def test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one(cfg, monkeypatch):
    """The seam is for the battery. The DEFAULT is what ships.

    Every other test hands ``terminal=`` a lambda, so all of them together prove
    only that the parameter is honoured. This pins the binding underneath it.
    """
    asked: list[bool] = []

    def probe():
        asked.append(True)
        return False

    monkeypatch.setattr(session, "has_controlling_terminal", probe)
    with pytest.raises(CratekitError) as excinfo:
        session.record_acknowledgment(cfg)
    assert asked, "the mint did not consult the real probe"
    assert excinfo.value.cause.reason == "backup-acknowledgment-no-terminal"


def test_the_real_terminal_probe_answers_no_when_there_is_no_terminal(monkeypatch):
    """And the probe itself, driven, so it cannot become ``return True``."""
    monkeypatch.setattr(os, "ctermid", lambda: str(Path("/nonexistent") / "tty"))
    assert session.has_controlling_terminal() is False


def test_the_volume_is_judged_before_a_restore_resolves_its_target(cfg, tmp_path):
    """``plan_restore``'s headline ordering claim, driven in the direction it claims.

    With the wrong disk at the configured root, the refusal has to be the
    volume's. Every other refusal in that body is reached by resolving a path,
    and resolving a path against the wrong volume is already the damage.
    """
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
    """A refusal is asserted everywhere. ZERO WRITES is the half that gets skipped.

    The real destructive half is driven with real gates, a ``clears`` tuple
    naming files that exist, and a recorder in place of the transfer. Moving the
    guard after the clearing loop leaves every other test in this file green and
    leaves a user's database without the write-ahead log it needs.
    """
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

    with pytest.raises(CratekitError) as excinfo:
        backup.run_restore(plan, cfg, runner=recorder, dry_run=False)

    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
    assert invoked == [], "a refused restore ran a transfer"
    for sidecar in sidecars:
        assert sidecar.exists(), f"a refused restore unlinked {sidecar.name}"
        assert sidecar.read_bytes() == b"the live write-ahead log"


# ═══════════════════════════════════════════════════════════════════════════
# The record a gated session keeps (R-12, R-375)
# ═══════════════════════════════════════════════════════════════════════════


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
    """R-598: the record's copy of the holder survives a kill, the lock's does not.

    Read while the gates are held, so both copies are on disk at once, and with
    no holder supplied, so the one the gates look up is the one compared.
    """
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
    with pytest.raises(CratekitError):
        with recording_gates(cfg):
            raise AssertionError("the gates admitted a session they should have refused")
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
    """CLOSED is a gated claim, and when it cannot be made the record still ENDS.

    Driven by taking the volume away between the gates and the close, which is
    the refusal ``close_session`` exists to raise. A record left OPEN here would
    refuse every later prune and cutover with no verb that abandons it, so the
    fallback is the opposite claim and not the absence of one. The refusal still
    surfaces, because a write whose close was refused did not end cleanly.
    """
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
    # The commit it recorded first is still what a restore reads.
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
    """A session the watch refuses must not already be on record as finished.

    The ordering fault this pins was real in two places: a record opened INSIDE
    the body exits before the gates do, so it closed CLOSED and released its
    capture, and then the watch refused the session over a moved grid. Driven
    with a real analysis file rewritten under an open session.
    """
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


def _capture_takers(src: Path) -> tuple[dict[str, set[str]], list[str]]:
    """Every FUNCTION in ``src`` that takes a capture, with what it still owes.

    Per function and not per module, because ``write/trees.py`` holds a dozen
    writers and a per-module reading is satisfied for all of them by the one that
    complies. Returns the unreadable spellings too: a capture imported by name
    or under an alias is a call this walk cannot attribute, and a guard that
    cannot read something says so rather than passing it.
    """
    import ast

    takers: dict[str, set[str]] = {}
    unreadable: list[str] = []
    for path in sorted(src.rglob("*.py")):
        if path.relative_to(src).as_posix() == "core/snapshot.py":
            continue
        tree = ast.parse(path.read_text())
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
            takes = False
            seen: set[str] = set()
            for node in ast.walk(function):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
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
            # The commit is recorded through a helper beside each writer, so
            # that spelling counts too, and each helper is checked for the real
            # call by ``test_each_commit_helper_records_the_commit``.
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
    """METHOD's fifth pattern, as a guard on the NEXT writer rather than a sweep of this one.

    R-12 and R-375 were one shape found twice: a function takes a capture inside
    the gates and keeps no record, so the undo it paid for cannot be listed,
    spent or protected. It asks for all three acts, because a record with no
    capture attached lists as unusable and one with no commit recorded is
    invisible to the restore that would discard it.
    """
    src = Path(session.__file__).resolve().parents[1]
    takers, unreadable = _capture_takers(src)

    assert not unreadable, (
        f"a capture is imported in a spelling this guard cannot follow: {unreadable}"
    )
    assert set(takers) == {
        "write/metadata_cli.py::mytags_vocals",
        "write/trees.py::write_tree_membership",
    }, (
        f"the set of functions that take a capture changed: {sorted(takers)}. A new "
        f"one owes a session record for it; name it here once it keeps one."
    )
    assert all(not missing for missing in takers.values()), takers


def test_the_capture_guard_reads_a_function_that_keeps_no_record(tmp_path):
    """The guard above, pointed at the shape it exists to catch.

    A compliant writer and a bare one in ONE module, which is the case a
    per-module reading waves through.
    """
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


def test_each_commit_helper_records_the_commit():
    """The helpers the guard accepts by name really do make the call."""
    import ast

    src = Path(session.__file__).resolve().parents[1]
    for relative, helper in (
        ("write/trees.py", "_record_membership_commit"),
        ("write/metadata_cli.py", "_record_mytags_commit"),
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
