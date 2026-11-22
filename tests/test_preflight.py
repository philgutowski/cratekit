"""The library volume precondition: three broken states, three distinct refusals.

Exempt from the conftest fixture that disarms the precondition, so this drives
the real thing. The states look identical to a directory check and each has a
different fix; a backup clone at the configured path passes a directory check
completely. A second volume is simulated through the injected identity
provider and mount enumerator; the one real platform call is run separately.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core.preflight import (
    LibraryUnreadableError,
    LibraryVolumeError,
    MountState,
    assert_library_mounted,
    assert_library_volume,
    assert_paths_readable,
    containing_mount,
    default_identity_provider,
    local_mount_points,
    macos_volume_identity,
    null_volume_identity,
    resolve_mount_state,
)

RECORDED = "11111111-2222-3333-4444-555555555555"
FOREIGN = "99999999-8888-7777-6666-555555555555"


def fake_identity(mapping: dict[Path, str]):
    """An identity provider backed by a dict keyed on the mount point, as a real one reports."""
    def provider(path: Path) -> str | None:
        return mapping.get(Path(path))

    return provider


def fake_mounts(*paths: Path):
    def enumerator():
        return [Path(p) for p in paths]

    return enumerator


def _state(configured, recorded, mapping, *mounts):
    """``resolve_mount_state`` over a fake provider and enumerator."""
    return resolve_mount_state(
        configured,
        recorded,
        identity_provider=fake_identity(mapping),
        mount_enumerator=fake_mounts(*mounts),
    )


# The three refusals the plan names, plus the two the state machine adds


def test_a_volume_that_is_not_mounted_refuses_with_its_own_cause(tmp_path):
    """The path is absent and the recorded identity is on no mounted volume."""
    mount = containing_mount(tmp_path)
    status = _state(tmp_path / "library", RECORDED, {mount: FOREIGN}, mount)
    assert status.state is MountState.NOT_MOUNTED


def test_a_volume_mounted_elsewhere_refuses_and_names_where_it_actually_is(tmp_path):
    """Right drive, wrong place: naming where it was found is the whole value."""
    configured = tmp_path / "library"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    mapping = {containing_mount(tmp_path): FOREIGN, elsewhere: RECORDED}

    status = _state(configured, RECORDED, mapping, elsewhere)
    assert status.state is MountState.MOUNTED_ELSEWHERE
    assert status.found_at == elsewhere

    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            configured,
            RECORDED,
            destructive=True,
            identity_provider=fake_identity(mapping),
            mount_enumerator=fake_mounts(elsewhere),
        )
    assert caught.value.state is MountState.MOUNTED_ELSEWHERE
    assert str(elsewhere) in caught.value.detail


def test_a_foreign_volume_at_the_configured_path_refuses(tmp_path):
    """The dangerous one: a restored clone passes every check short of identity."""
    configured = tmp_path / "library"
    configured.mkdir()
    status = _state(configured, RECORDED, {containing_mount(configured): FOREIGN})
    assert status.state is MountState.FOREIGN_VOLUME
    assert status.observed_identity == FOREIGN
    assert status.recorded_identity == RECORDED


def test_the_three_refusals_are_distinguishable_from_each_other(tmp_path):
    """Three states, three causes: a single boolean would pass each test above."""
    not_mounted = tmp_path / "gone"
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    mapping = {containing_mount(tmp_path): FOREIGN, elsewhere: RECORDED}
    states = {
        _state(not_mounted, RECORDED, mapping).state,
        _state(foreign, RECORDED, mapping).state,
        _state(not_mounted, RECORDED, mapping, elsewhere).state,
    }
    assert states == {
        MountState.NOT_MOUNTED,
        MountState.FOREIGN_VOLUME,
        MountState.MOUNTED_ELSEWHERE,
    }


def test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause(tmp_path):
    """The right drive, the root not on it: a different fix from all three."""
    mount = containing_mount(tmp_path)
    status = _state(tmp_path / "no-such-subdirectory", RECORDED, {mount: RECORDED}, mount)
    assert status.state is MountState.LIBRARY_PATH_MISSING


def test_the_right_volume_at_the_configured_path_passes(tmp_path):
    """Healthy, asserted so the guard cannot refuse everything."""
    mount = containing_mount(tmp_path)
    status = assert_library_volume(
        tmp_path,
        RECORDED,
        destructive=True,
        identity_provider=fake_identity({mount: RECORDED}),
        mount_enumerator=fake_mounts(mount),
    )
    assert status.ok and status.state is MountState.OK


# Identity is asserted before anything resolves, and refuses when unreadable


def test_the_identity_gate_is_callable_with_no_paths_at_all(tmp_path):
    """A destructive session refuses before resolving one path: resolving
    against the wrong volume is already the damage."""
    configured = tmp_path / "library"
    configured.mkdir()
    resolved: list[Path] = []

    def tracking_provider(path: Path) -> str | None:
        resolved.append(Path(path))
        return FOREIGN

    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_mounted(
            root=configured,
            recorded_identity=RECORDED,
            destructive=True,
            identity_provider=tracking_provider,
            mount_enumerator=fake_mounts(),
        )
    assert caught.value.state is MountState.FOREIGN_VOLUME
    # Only the mount was probed. No library path was resolved or stat-ed.
    assert resolved == [containing_mount(configured)]


def test_an_unreadable_identity_refuses_a_destructive_verb(tmp_path):
    """Cannot tell is not fine: a path check or a marker file passes on a clone."""
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            tmp_path, RECORDED, destructive=True,
            identity_provider=null_volume_identity, mount_enumerator=fake_mounts(),
        )
    assert caught.value.state is MountState.IDENTITY_UNAVAILABLE


def test_an_unreadable_identity_lets_a_read_only_verb_proceed(tmp_path):
    """The asymmetry: the worst case of a read is a wrong report."""
    status = assert_library_volume(
        tmp_path, RECORDED, destructive=False,
        identity_provider=null_volume_identity, mount_enumerator=fake_mounts(),
    )
    assert status.state is MountState.IDENTITY_UNAVAILABLE


def test_no_recorded_identity_refuses_a_destructive_verb(tmp_path):
    """Adopting whatever is mounted would make the check true by construction."""
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            tmp_path, None, destructive=True,
            identity_provider=fake_identity({containing_mount(tmp_path): RECORDED}),
            mount_enumerator=fake_mounts(),
        )
    assert caught.value.state is MountState.IDENTITY_NOT_RECORDED


def test_the_refusal_carries_a_structured_cause_and_no_command_text(tmp_path):
    """KTD25 and D2: a cause the CLI renders and a caller can branch on, not a SystemExit."""
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            tmp_path / "library", RECORDED, destructive=True,
            identity_provider=fake_identity({containing_mount(tmp_path): FOREIGN}),
            mount_enumerator=fake_mounts(),
        )
    error = caught.value
    assert not isinstance(error, SystemExit)
    assert isinstance(error.state, MountState)
    for verb in ("crate ", "run ", "please "):
        assert verb not in error.detail.lower(), "remediation prose belongs to the CLI layer"


# The real mount test, and the real platform call


def test_a_leftover_directory_is_not_a_mount(tmp_path):
    """An empty directory where a volume mounted passes ``is_dir()``, not ``ismount``."""
    leftover = tmp_path / "library"
    leftover.mkdir()
    assert containing_mount(leftover) != leftover


def test_the_containing_mount_of_a_subdirectory_is_the_volume_it_lives_on(tmp_path):
    """A root may be a subdirectory of a mount, so the walk up is required."""
    nested = tmp_path / "Music" / "Crate"
    nested.mkdir(parents=True)
    assert containing_mount(nested) == containing_mount(tmp_path)


def test_the_containing_mount_of_a_path_that_does_not_exist_yet_resolves(tmp_path):
    """Resolution must work for the not-mounted case, where the path is absent."""
    assert containing_mount(tmp_path / "absent" / "deeper") == containing_mount(tmp_path)


def test_this_machines_own_volume_identity_is_readable_and_stable():
    """The real platform call: a value, the same twice, and for a second path."""
    provider = default_identity_provider()
    identity = provider(Path("/"))
    if identity is None:
        assert provider is not macos_volume_identity, (
            "on macOS the volume UUID must be readable; a None here means the "
            "getattrlist call regressed and every identity check would degrade"
        )
        return
    assert provider(Path("/")) == identity
    assert provider(containing_mount(Path.cwd())) is not None


def test_a_path_with_no_volume_identity_reads_as_none():
    """None, not a raise: "cannot tell" and "mismatch" have opposite remedies."""
    assert macos_volume_identity(Path("/definitely-not-a-real-mount-point")) is None


def test_the_mount_enumerator_reports_this_machines_mounts():
    """The enumerator has to actually see mounts, or MOUNTED_ELSEWHERE never fires."""
    mounts = local_mount_points()
    assert mounts, "no local mounts enumerated; the mounted-elsewhere state is dead code"
    assert Path("/") in mounts


# The readability sampler, kept separate on purpose


def test_one_resolving_path_passes(tmp_path):
    """A single moved file must never block a legitimate run."""
    present = tmp_path / "track.flac"
    present.write_bytes(b"x")
    assert_paths_readable(
        [tmp_path / "gone1.flac", present, tmp_path / "gone2.flac"], root=tmp_path
    )


def test_an_empty_sample_is_a_noop(tmp_path):
    assert_paths_readable([], root=tmp_path / "not-mounted")


def test_every_sampled_path_missing_refuses(tmp_path):
    with pytest.raises(LibraryUnreadableError):
        assert_paths_readable([tmp_path / f"t{i}.flac" for i in range(8)], root=tmp_path)


def test_sampling_is_bounded(tmp_path):
    """A resolving path just past the sample window still fails: it stopped looking."""
    paths = [tmp_path / f"t{i}.flac" for i in range(10)]
    paths[5].write_bytes(b"x")
    with pytest.raises(LibraryUnreadableError):
        assert_paths_readable(paths, root=tmp_path)


def test_streaming_pseudo_locations_outside_the_root_are_skipped(tmp_path):
    """Off-root streamed rows are skipped, not counted as misses on a healthy mount."""
    present = tmp_path / "Music" / "track.flac"
    present.parent.mkdir()
    present.write_bytes(b"x")
    streamed = [f"/v4/catalog/tracks/{n}/" for n in range(5)]
    assert_paths_readable([*streamed, present], root=tmp_path)


def test_a_sample_that_is_entirely_off_root_is_a_noop(tmp_path):
    assert_paths_readable(["/v4/catalog/tracks/1/", "stream:tracks:2"],
                          root=tmp_path / "library")


def test_readability_and_identity_are_separate_checks(tmp_path):
    """The right disk can still be evicted, unreadable or the wrong subtree."""
    mount = containing_mount(tmp_path)
    with pytest.raises(LibraryUnreadableError):
        assert_library_mounted(
            [tmp_path / f"t{i}.flac" for i in range(8)],
            root=tmp_path,
            recorded_identity=RECORDED,
            destructive=True,
            identity_provider=fake_identity({mount: RECORDED}),
            mount_enumerator=fake_mounts(mount),
        )


def test_the_precondition_has_no_default_library_root():
    """A default root would be one person's disk baked into shipped code (R1)."""
    with pytest.raises(TypeError):
        assert_library_mounted([])  # type: ignore[call-arg]


# R-344: the case of a spelling is not part of an identity

#: Hex with letters, unlike ``RECORDED``, whose case fold would be X equals X.
LETTERED = "0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
OTHER_LETTERED = "fedcba98-7654-4321-8fed-cba987654321"


def test_the_case_fold_fixtures_can_tell_a_fold_from_no_fold():
    assert LETTERED.upper() != LETTERED
    assert OTHER_LETTERED.upper() != OTHER_LETTERED


def test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports(tmp_path):
    """``diskutil`` prints the UUID upper case, ``getattrlist`` reads it lower."""
    status = _state(tmp_path, LETTERED.upper(), {containing_mount(tmp_path): LETTERED})
    assert status.state is MountState.OK


def test_an_identity_in_another_case_is_still_found_where_it_is_mounted(tmp_path):
    """The sweep over every mount compares the same way the configured one does."""
    configured = tmp_path / "configured"
    configured.mkdir()
    elsewhere = tmp_path / "elsewhere"
    mapping = {containing_mount(configured): OTHER_LETTERED, elsewhere: LETTERED}
    status = _state(configured, LETTERED.upper(), mapping, elsewhere)
    assert status.state is MountState.MOUNTED_ELSEWHERE
    assert status.found_at == elsewhere


def test_folding_the_case_does_not_make_a_different_volume_the_same_one(tmp_path):
    """A fold that also matched a different UUID is no identity."""
    status = _state(
        tmp_path, LETTERED.upper(), {containing_mount(tmp_path): OTHER_LETTERED.upper()}
    )
    assert status.state is MountState.FOREIGN_VOLUME


@pytest.mark.parametrize("refusal", [PermissionError(13, "denied"), OSError(1, "not permitted")])
def test_a_refused_look_raises_rather_than_reading_as_no_mount(tmp_path, monkeypatch, refusal):
    """U301. A stat or samefile this account may not make is not a no: it raises."""
    import os

    from cratekit.core import preflight
    real_lstat = os.lstat

    def refused(path, *args, **kwargs):
        if str(path).startswith(str(tmp_path)):
            raise refusal
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, "lstat", refused)
    monkeypatch.setattr(Path, "samefile", lambda self, other: (_ for _ in ()).throw(refusal))
    real_is_mount = getattr(preflight.is_mount_point, "real_is_mount", preflight.is_mount_point)
    with pytest.raises(OSError):
        real_is_mount(tmp_path / "slot")
    with pytest.raises(OSError):
        preflight.names_one_path(tmp_path / "a", tmp_path / "b")
