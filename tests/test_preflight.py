"""The library volume precondition: three broken states, three distinct refusals.

This module is exempt from the conftest fixture that disarms the precondition
for the rest of the suite, so everything below exercises the real thing.

WHY THE THREE STATES ARE TESTED SEPARATELY. They all present identically to a
directory check, which is what the ported guard used, and each one has a
different fix. Telling a user "the volume is wrong" when the volume is fine and
the configured PATH is wrong sends them to unplug a drive for no reason. Worse,
a backup clone mounted at the configured path passes a directory check
completely, and a deletion pass against a clone removes files the real library
still references while every screen looks normal.

HOW A SECOND VOLUME IS SIMULATED WITHOUT A SECOND VOLUME. The identity provider
and the mount enumerator are injected seams. A fake provider is a dict lookup
from path to identity, and a fake enumerator is a list. That is not a compromise
for the sake of testing: it is why the platform-specific call is a seam at all,
and it means the decision logic is covered on every machine while the one real
ctypes call is exercised separately against this machine's own boot volume.
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
    """An identity provider backed by a dict, resolved by containing mount.

    Keyed on the MOUNT POINT rather than on the queried path, because that is
    what a real provider reports: every path on a volume shares its volume's
    identity.
    """

    def provider(path: Path) -> str | None:
        return mapping.get(Path(path))

    return provider


def fake_mounts(*paths: Path):
    def enumerator():
        return [Path(p) for p in paths]

    return enumerator


# ═══════════════════════════════════════════════════════════════════════════
# The three refusals the plan names, plus the two the state machine adds
# ═══════════════════════════════════════════════════════════════════════════


def test_a_volume_that_is_not_mounted_refuses_with_its_own_cause(tmp_path):
    """State one: the drive is not attached anywhere.

    The configured path does not exist, and the recorded identity turns up on no
    mounted volume. The fix is to attach the drive, and nothing else.
    """
    configured = tmp_path / "library"  # never created
    status = resolve_mount_state(
        configured,
        RECORDED,
        identity_provider=fake_identity({containing_mount(tmp_path): FOREIGN}),
        mount_enumerator=fake_mounts(containing_mount(tmp_path)),
    )
    assert status.state is MountState.NOT_MOUNTED


def test_a_volume_mounted_elsewhere_refuses_and_names_where_it_actually_is(tmp_path):
    """State two: right drive, wrong place.

    Naming the path it was found at is the whole value of this state. Without it
    the user is told the volume is missing while it sits mounted two directories
    away, and the fix is one line of configuration they cannot find.
    """
    configured = tmp_path / "library"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    status = resolve_mount_state(
        configured,
        RECORDED,
        identity_provider=fake_identity(
            {containing_mount(tmp_path): FOREIGN, elsewhere: RECORDED}
        ),
        mount_enumerator=fake_mounts(elsewhere),
    )
    assert status.state is MountState.MOUNTED_ELSEWHERE
    assert status.found_at == elsewhere

    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            configured,
            RECORDED,
            destructive=True,
            identity_provider=fake_identity(
                {containing_mount(tmp_path): FOREIGN, elsewhere: RECORDED}
            ),
            mount_enumerator=fake_mounts(elsewhere),
        )
    assert caught.value.state is MountState.MOUNTED_ELSEWHERE
    assert str(elsewhere) in caught.value.detail


def test_a_foreign_volume_at_the_configured_path_refuses(tmp_path):
    """State three, and the dangerous one: something else is mounted where we look.

    A restored backup clone is the case that matters. It has the right layout,
    the right database, and the right filenames, so every check short of volume
    identity passes on it. Deleting against a clone removes files the real
    library still references.
    """
    configured = tmp_path / "library"
    configured.mkdir()

    status = resolve_mount_state(
        configured,
        RECORDED,
        identity_provider=fake_identity({containing_mount(configured): FOREIGN}),
        mount_enumerator=fake_mounts(),
    )
    assert status.state is MountState.FOREIGN_VOLUME
    assert status.observed_identity == FOREIGN
    assert status.recorded_identity == RECORDED


def test_the_three_refusals_are_distinguishable_from_each_other(tmp_path):
    """The plan's scenario stated as one assertion: three states, three causes.

    A single boolean would satisfy every individual test above and would still
    be the guard this replaces.
    """
    not_mounted = tmp_path / "gone"
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    base = fake_identity({containing_mount(tmp_path): FOREIGN, elsewhere: RECORDED})
    states = {
        resolve_mount_state(not_mounted, RECORDED, identity_provider=base,
                            mount_enumerator=fake_mounts()).state,
        resolve_mount_state(foreign, RECORDED, identity_provider=base,
                            mount_enumerator=fake_mounts()).state,
        resolve_mount_state(not_mounted, RECORDED, identity_provider=base,
                            mount_enumerator=fake_mounts(elsewhere)).state,
    }
    assert states == {
        MountState.NOT_MOUNTED,
        MountState.FOREIGN_VOLUME,
        MountState.MOUNTED_ELSEWHERE,
    }


def test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause(tmp_path):
    """A fourth state, because it is a different fix from all three above.

    The drive is attached and it is the right drive; the configured root points
    at a directory that is not on it. Telling the user to check their cabling
    would be actively misleading.
    """
    mount = containing_mount(tmp_path)
    status = resolve_mount_state(
        tmp_path / "no-such-subdirectory",
        RECORDED,
        identity_provider=fake_identity({mount: RECORDED}),
        mount_enumerator=fake_mounts(mount),
    )
    assert status.state is MountState.LIBRARY_PATH_MISSING


def test_the_right_volume_at_the_configured_path_passes(tmp_path):
    """What healthy looks like, asserted so the guard cannot refuse everything."""
    mount = containing_mount(tmp_path)
    status = assert_library_volume(
        tmp_path,
        RECORDED,
        destructive=True,
        identity_provider=fake_identity({mount: RECORDED}),
        mount_enumerator=fake_mounts(mount),
    )
    assert status.ok and status.state is MountState.OK


# ═══════════════════════════════════════════════════════════════════════════
# Identity is asserted BEFORE anything resolves, and refuses when unreadable
# ═══════════════════════════════════════════════════════════════════════════


def test_the_identity_gate_is_callable_with_no_paths_at_all(tmp_path):
    """A destructive session must refuse before it resolves a single path.

    Resolving paths against the wrong volume is already the damage: the review
    screen fills with files from a clone and every one of them looks legitimate.
    So the identity check cannot be a function that needs a sample of paths to
    work, which is what the ported guard was.
    """
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
    """Cannot tell is not the same as fine.

    A provider that returns None means the platform has no adapter or the
    filesystem carries no identity. Degrading to a path check would pass on the
    clone, and degrading to a marker file on the volume would too, because a
    clone carries the marker.
    """
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            tmp_path, RECORDED, destructive=True,
            identity_provider=null_volume_identity, mount_enumerator=fake_mounts(),
        )
    assert caught.value.state is MountState.IDENTITY_UNAVAILABLE


def test_an_unreadable_identity_lets_a_read_only_verb_proceed(tmp_path):
    """The asymmetry, stated. The worst case of a read is a wrong report."""
    status = assert_library_volume(
        tmp_path, RECORDED, destructive=False,
        identity_provider=null_volume_identity, mount_enumerator=fake_mounts(),
    )
    assert status.state is MountState.IDENTITY_UNAVAILABLE


def test_no_recorded_identity_refuses_a_destructive_verb(tmp_path):
    """Nothing recorded means nothing asserted, and a check that cannot fail is not one.

    Same reasoning as an unset version pin: silently adopting whatever is
    currently mounted would make the assertion true by construction, forever.
    """
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            tmp_path, None, destructive=True,
            identity_provider=fake_identity({containing_mount(tmp_path): RECORDED}),
            mount_enumerator=fake_mounts(),
        )
    assert caught.value.state is MountState.IDENTITY_NOT_RECORDED


def test_the_refusal_carries_a_structured_cause_and_no_command_text(tmp_path):
    """KTD25 and D2 together: a token the CLI renders, not prose it prints.

    The ported guard raised a ``SystemExit`` subclass, so the only thing that
    survived to the process boundary was an exit status. A caller in the middle
    could neither branch on the cause nor add context to it.
    """
    configured = tmp_path / "library"
    with pytest.raises(LibraryVolumeError) as caught:
        assert_library_volume(
            configured, RECORDED, destructive=True,
            identity_provider=fake_identity({containing_mount(tmp_path): FOREIGN}),
            mount_enumerator=fake_mounts(),
        )
    error = caught.value
    assert not isinstance(error, SystemExit)
    assert isinstance(error.state, MountState)
    for verb in ("crate ", "run ", "please "):
        assert verb not in error.detail.lower(), "remediation prose belongs to the CLI layer"


# ═══════════════════════════════════════════════════════════════════════════
# The real mount test, and the real platform call
# ═══════════════════════════════════════════════════════════════════════════


def test_a_leftover_directory_is_not_a_mount(tmp_path):
    """The whole reason the directory check was replaced.

    An empty directory left behind where a volume used to mount satisfies
    ``is_dir()`` completely. ``os.path.ismount`` compares device and inode
    against the parent, so it is not fooled, and it is stdlib on every platform.
    """
    leftover = tmp_path / "library"
    leftover.mkdir()
    assert containing_mount(leftover) != leftover


def test_the_containing_mount_of_a_subdirectory_is_the_volume_it_lives_on(tmp_path):
    """A library root may legitimately be a subdirectory of a mount.

    Asking ``ismount`` about such a path directly returns False even when
    everything is healthy, so the walk up is required rather than defensive.
    """
    nested = tmp_path / "Music" / "Crate"
    nested.mkdir(parents=True)
    assert containing_mount(nested) == containing_mount(tmp_path)


def test_the_containing_mount_of_a_path_that_does_not_exist_yet_resolves(tmp_path):
    """Resolution must work for the not-mounted case, where the path is absent."""
    assert containing_mount(tmp_path / "absent" / "deeper") == containing_mount(tmp_path)


def test_this_machines_own_volume_identity_is_readable_and_stable():
    """The one test that runs the real platform call rather than a fake.

    Everything else injects a provider, which proves the decision logic and
    proves nothing about the ctypes call. This asserts the call returns a value,
    returns the SAME value twice, and reports the same identity for two paths on
    one volume, which is the property that makes it an identity at all.
    """
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
    """Unavailable must be None rather than an exception or a fabricated value.

    A provider that raised would make "cannot tell" indistinguishable from
    "mismatch", and those have opposite remediations.
    """
    assert macos_volume_identity(Path("/definitely-not-a-real-mount-point")) is None


def test_the_mount_enumerator_reports_this_machines_mounts():
    """The enumerator has to actually see mounts, or MOUNTED_ELSEWHERE never fires."""
    mounts = local_mount_points()
    assert mounts, "no local mounts enumerated; the mounted-elsewhere state is dead code"
    assert Path("/") in mounts


# ═══════════════════════════════════════════════════════════════════════════
# The readability sampler, kept separate on purpose
# ═══════════════════════════════════════════════════════════════════════════


def test_one_resolving_path_passes(tmp_path):
    """A single moved file must never block a legitimate run."""
    present = tmp_path / "track.flac"
    present.write_bytes(b"x")
    assert_paths_readable(
        [tmp_path / "gone1.flac", present, tmp_path / "gone2.flac"], root=tmp_path
    )


def test_an_empty_sample_is_a_noop(tmp_path):
    """Nothing to read means nothing to mis-route."""
    assert_paths_readable([], root=tmp_path / "not-mounted")


def test_every_sampled_path_missing_refuses(tmp_path):
    """The failure the whole module exists for, in its readability half."""
    with pytest.raises(LibraryUnreadableError):
        assert_paths_readable([tmp_path / f"t{i}.flac" for i in range(8)], root=tmp_path)


def test_sampling_is_bounded(tmp_path):
    """Failing must be cheap on a plan holding thousands of tracks.

    The proof is indirect and deliberate: a path that DOES resolve sits just past
    the sample window, and the guard still fires, which can only happen if it
    stopped looking.
    """
    paths = [tmp_path / f"t{i}.flac" for i in range(10)]
    paths[5].write_bytes(b"x")
    with pytest.raises(LibraryUnreadableError):
        assert_paths_readable(paths, root=tmp_path)


def test_streaming_pseudo_locations_outside_the_root_are_skipped(tmp_path):
    """Off-root paths are skipped, not counted as misses.

    A collection can open with streamed rows whose locations decode to something
    that is not on the volume at all. Counting those as misses trips the guard on
    a perfectly healthy mount, and a guard that cries wolf gets bypassed.
    """
    present = tmp_path / "Music" / "track.flac"
    present.parent.mkdir()
    present.write_bytes(b"x")
    streamed = [f"/v4/catalog/tracks/{n}/" for n in range(5)]
    assert_paths_readable([*streamed, present], root=tmp_path)


def test_a_sample_that_is_entirely_off_root_is_a_noop(tmp_path):
    """Nothing on the volume was sampled, so nothing about the volume was learned."""
    assert_paths_readable(["/v4/catalog/tracks/1/", "stream:tracks:2"],
                          root=tmp_path / "library")


def test_readability_and_identity_are_separate_checks(tmp_path):
    """They answer different questions and must not be merged.

    Identity proves the right disk is attached. It cannot detect a cloud-evicted
    tree, a permissions change, or a library root pointing at the wrong subtree,
    and all three of those pass an identity check and fail here.
    """
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
