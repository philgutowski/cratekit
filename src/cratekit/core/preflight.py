"""The library volume precondition: is the RIGHT disk mounted where we think it is.

Tag readers degrade to None on an unreadable file so one damaged file cannot
abort a run. That degrade is only safe because this precondition runs first:
with the library volume unmounted every track would read as untagged, and the
router would quietly file the whole plan into the fallback bucket.

A directory check is not enough, because three broken states pass it: a
leftover empty mount point on the boot disk, a different disk at the configured
path, and a restored backup clone at that path. The clone is the dangerous one,
since deleting against it removes files the real library still references. So
the question is "is this the SAME VOLUME the library was configured against",
answered by the filesystem's own volume UUID read through a platform call. A
marker file would pass on the clone, and ``st_dev`` or ``f_fsid`` change between
mounts.

:class:`MountState` names each distinct outcome, because each has a different
fix. Members are structured causes (KTD25, D2): no verb, no command text, no
remediation prose; the CLI layer renders them and reserves an exit code each.

This module reads no configuration. The configured root and recorded identity
arrive as parameters and the platform seams as injected callables, so the whole
state machine is testable against synthetic volumes, and a new platform is a new
provider rather than a rewrite of the decision.
"""

from __future__ import annotations

import os
import sys
import uuid
from dataclasses import dataclass
from enum import Enum
from functools import partial
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable, Mapping, Sequence

from cratekit.core import cause

# How many on-volume paths the readability sampler stats before giving up,
# bounded so failing never means stat-ing thousands of files.
SAMPLE_SIZE = 5


class MountState(Enum):
    """Why the library volume is or is not usable, as a structured cause.

    Each member is a distinct diagnosis with a distinct fix. The CLI layer maps
    each to an exit code and remediation text; nothing here names a command.
    """

    OK = "ok"
    LIBRARY_PATH_MISSING = "library_path_missing"
    NOT_MOUNTED = "not_mounted"
    MOUNTED_ELSEWHERE = "mounted_elsewhere"
    FOREIGN_VOLUME = "foreign_volume"
    IDENTITY_UNAVAILABLE = "identity_unavailable"
    IDENTITY_NOT_RECORDED = "identity_not_recorded"


@dataclass(frozen=True)
class MountStatus:
    """Everything known about the configured library volume, after one probe.

    Both identities are carried even when they match, so a logged refusal shows
    what it compared.
    """

    state: MountState
    configured_root: Path
    mount_point: Path | None = None
    recorded_identity: str | None = None
    observed_identity: str | None = None
    found_at: Path | None = None

    @property
    def ok(self) -> bool:
        return self.state is MountState.OK


class LibraryVolumeError(Exception):
    """A refusal carrying its structured cause.

    Deliberately not a ``SystemExit``: a typed failure that collapses to an
    integer cannot be recovered or branched on downstream (KTD25).
    """

    def __init__(self, status: MountStatus, detail: str = "") -> None:
        self.status = status
        self.state = status.state
        self.detail = detail
        super().__init__(detail or status.state.value)


class LibraryUnreadableError(Exception):
    """The right volume is mounted, and the files on it still cannot be read.

    Separate from :class:`LibraryVolumeError` because the cause is separate
    (cloud eviction, permissions, a root pointing at the wrong tree), and
    identity cannot detect any of them.
    """

    def __init__(self, root: Path, sampled: int) -> None:
        self.root = root
        self.sampled = sampled
        super().__init__(
            f"all {sampled} sampled paths under the library root are missing while "
            f"the volume itself is mounted; refusing to treat unreadable files as "
            f"untagged ones"
        )


# ---------------------------------------------------------------------------
# Platform seam 1: volume identity
# ---------------------------------------------------------------------------

IdentityProvider = Callable[[Path], "str | None"]
MountEnumerator = Callable[[], Sequence[Path]]


def macos_volume_identity(path: Path) -> str | None:
    """The volume UUID from ``getattrlist(2)``, or None if unavailable.

    A platform call, not a subprocess. The UUID is stable across remount, a new
    mount point and a rename. None rather than raising, because "cannot tell"
    and "mismatch" have opposite remediations.
    """
    import ctypes
    import ctypes.util

    attr_bit_map_count = 5
    attr_vol_info = 0x80000000
    attr_vol_uuid = 0x00040000

    class _AttrList(ctypes.Structure):
        _fields_ = [("bitmapcount", ctypes.c_ushort), ("reserved", ctypes.c_uint16)] + [
            (name, ctypes.c_uint32)
            for name in ("commonattr", "volattr", "dirattr", "fileattr", "forkattr")
        ]

    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        libc.getattrlist.argtypes = [
            ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong,
        ]
        libc.getattrlist.restype = ctypes.c_int
    except (OSError, AttributeError):  # pragma: no cover - no libc to talk to
        return None

    request = _AttrList(attr_bit_map_count, 0, 0, attr_vol_info | attr_vol_uuid, 0, 0, 0)
    buffer = ctypes.create_string_buffer(64)
    result = libc.getattrlist(
        os.fsencode(str(path)), ctypes.byref(request), buffer, ctypes.sizeof(buffer), 0
    )
    if result != 0:
        return None

    # A 4-byte length then 16 UUID bytes. A filesystem without the attribute
    # returns success with a short buffer, so the length must be checked.
    length = int.from_bytes(buffer.raw[:4], sys.byteorder)
    if length < 20:
        return None
    raw = buffer.raw[4:20]
    if raw == b"\x00" * 16:
        # An all-zero UUID means no identity, or every such volume would match.
        return None
    return str(uuid.UUID(bytes=raw))


def windows_volume_identity(path: Path) -> str | None:  # pragma: no cover - needs Windows
    """The volume serial number from ``GetVolumeInformationW``, or None.

    Weaker than the macOS UUID (32 bits) but read from the kernel the same way.
    """
    import ctypes

    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        return None

    serial = ctypes.c_uint32()
    drive = str(Path(path).anchor)
    ok = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive), None, 0, ctypes.byref(serial), None, None, None, 0
    )
    if not ok or not serial.value:
        return None
    return f"{serial.value:08x}"


def normalize_identity(identity: str) -> str:
    """One spelling of a volume identity: surrounding space gone, case folded.

    Hex is case blind, and ``diskutil info`` prints uppercase where the adapters
    report lowercase.
    """
    return identity.strip().lower()


def same_identity(recorded: str, observed: str) -> bool:
    """Whether two spellings name one volume.

    Folded at compare time only, never at record time: the recorded value is
    also the ``library_id`` jobs and watermarks match exactly (R-344).
    """
    return normalize_identity(recorded) == normalize_identity(observed)


def null_volume_identity(path: Path) -> str | None:
    """No adapter for this platform. Always None, which is a refusal upstream.

    Never degrade to a path check or a marker file; both pass on a clone.
    """
    return None


def default_identity_provider() -> IdentityProvider:
    """The identity provider for the platform this is running on."""
    if sys.platform == "darwin":
        return macos_volume_identity
    if sys.platform.startswith("win"):
        return windows_volume_identity
    return null_volume_identity


# ---------------------------------------------------------------------------
# Platform seam 2: enumerating mounts
# ---------------------------------------------------------------------------


def local_mount_points() -> Sequence[Path]:
    """Currently mounted LOCAL filesystems, read from the kernel mount table.

    Local only, because a stale network mount can block on stat and a guard
    that hangs is worse than one that refuses. Imported lazily so an injected
    enumerator never loads the extension.
    """
    import psutil

    return [Path(part.mountpoint) for part in psutil.disk_partitions(all=False)]


# ---------------------------------------------------------------------------
# The real mount test
# ---------------------------------------------------------------------------


def containing_mount(path: Path) -> Path:
    """The mount point of the deepest existing ancestor of ``path``.

    Walks up because a library root may be a subdirectory of a mount, where
    ``os.path.ismount`` is False on a healthy setup. For reporting; a caller
    deciding whether an identity may be RECORDED asks :func:`identity_source`.
    """
    current = deepest_existing(path)
    while not os.path.ismount(current) and current != current.parent:
        current = current.parent
    return current


def deepest_existing(path: Path) -> Path:
    """The deepest ancestor of ``path``, or ``path`` itself, that exists."""
    current = Path(path).resolve()
    while not current.exists() and current != current.parent:
        current = current.parent
    return current


#: Where a platform mounts a volume: a directory and the depth beneath it at
#: which the mount point sits. It tells a path somebody will create from the
#: place a volume will appear, which ``stat`` cannot. Every row claims an empty
#: directory there is evidence of an absent volume, true for mounter-made
#: directories like ``/Volumes/<name>`` and the udisks locations. ``/mnt`` is
#: not a row: a person makes it by hand and it stays, so a library under it on
#: the root filesystem is ordinary and the row refused it forever (P7).
_VOLUME_MOUNT_LOCATIONS: Mapping[str, tuple[tuple[str, int], ...]] = MappingProxyType(
    {
        "darwin": (("/Volumes", 1),),
        "linux": (("/media", 1), ("/media", 2), ("/run/media", 2)),
    }
)


def volume_mount_locations() -> tuple[tuple[Path, int], ...]:
    """Where a volume mounts on THIS platform. Empty when the table has no row.

    A function so a caller can be driven against another platform's answer.
    Every row is resolved because the paths compared against it are, and an
    unresolved symlinked row would silently match nothing.
    """
    return tuple(
        (Path(directory).resolve(), depth)
        for directory, depth in _VOLUME_MOUNT_LOCATIONS.get(sys.platform, ())
    )


def _no_unless_refused(question: Callable[[], bool]) -> bool:
    """``question()``, where absent or unrepresentable answers False.

    A permission refusal raises instead, because "I could not look" is not
    "there is nothing there".
    """
    try:
        return question()
    except OSError as exc:
        if cause.permission_denied(exc) is not None:
            raise
        return False
    except ValueError:
        # An unrepresentable path, an embedded null among them: the question
        # was asked and the answer is no; nothing was refused.
        return False


def is_mount_point(path: Path) -> bool:
    """Whether the kernel has a filesystem mounted EXACTLY at ``path``.

    The one machine fact the mount rule turns on, a seam because a suite cannot
    mount a volume. The answer comes from ``os.path.ismount``, but a False is
    confirmed by the two stats it makes, because ``ismount`` swallows a
    permission error and an attached volume under an untraversable directory
    must raise rather than read as no volume. ``tests/test_doctor.py`` pins the
    real function in both directions.
    """
    if os.path.ismount(path):
        return True

    def confirm() -> bool:
        os.lstat(path)
        # The parent through the slot itself, which needs execute permission
        # ON the slot, so a mode 0o000 mount point raises here.
        os.lstat(os.path.join(path, os.pardir))
        return False

    return _no_unless_refused(confirm)


def slot_holds_a_volume(slot: Path) -> bool:
    """Whether a volume is mounted in ``slot``, under this name or another.

    ``os.path.ismount`` is False for a symlink, so what the symlink resolves to
    is asked too: a symlink to an ordinary boot disk directory holds no volume,
    and macOS's own boot entry, a symlink to ``/``, does (P7).
    """
    if is_mount_point(slot):
        return True
    try:
        behind = Path(slot).resolve()
    except ValueError:
        # An unrepresentable path answers no, as ``is_mount_point`` does.
        return False
    return behind != Path(slot) and is_mount_point(behind)


def device_of(path: Path) -> int | None:
    """The device ``path`` is on, read off its nearest ancestor that exists.

    None when nothing up to the root can be read, so a caller comparing two
    devices never takes two unreadable paths for one volume.
    """
    probe = path
    while True:
        try:
            return probe.stat().st_dev
        except OSError:
            if probe.parent == probe:
                return None
            probe = probe.parent


def names_one_path(left: Path, right: Path) -> bool:
    """Whether two paths name ONE thing on this filesystem, as the filesystem sees it.

    ``samefile`` compares ``(st_dev, st_ino)``, so two case spellings on a case
    insensitive volume are one path and on a case sensitive one are not; a
    comparison of path parts got that wrong. Equality first, so two equal
    spellings of an absent path still answer True. A permission refusal raises
    rather than reading as different.
    """
    if left == right:
        return True
    return _no_unless_refused(lambda: left.samefile(right))


def _is_a_volume_mount_location(
    path: Path, locations: Sequence[tuple[Path, int]]
) -> bool:
    """Whether ``path`` is exactly where this platform mounts a volume.

    Walks up the declared depth and asks :func:`names_one_path` whether the
    declared directory stands there, rather than subtracting strings.
    """
    for directory, depth in locations:
        ancestor = path
        for _ in range(depth):
            if ancestor == ancestor.parent:
                break
            ancestor = ancestor.parent
        else:
            if names_one_path(ancestor, directory):
                return True
    return False


def mount_location_ancestors(path: Path) -> tuple[Path, ...]:
    """Every place a volume would mount on the way down to ``path``.

    ``path`` itself counts, and every match is returned, since Linux mounters
    answer at two declared depths. Both the given spelling and its resolution
    are walked: resolving alone erased a slot whose symlink points out of the
    mount directory.
    """
    given = Path(os.path.abspath(path))
    resolved = Path(path).resolve()
    known = volume_mount_locations()
    found: list[Path] = []
    for chain in (given, resolved):
        for candidate in (chain, *chain.parents):
            if candidate in found:
                continue
            if _is_a_volume_mount_location(candidate, known):
                found.append(candidate)
    return tuple(found)


def identity_source(path: Path) -> Path | None:
    """The mount whose identity may be RECORDED for ``path``, or None.

    Narrower than :func:`containing_mount`: with the drive unplugged that walk
    reaches the boot disk, and recording its identity would let every
    destructive refusal pass there. So every mount slot on the way down is
    asked whether a volume is in it now:

    * no slot: ordinary storage, accepted at any depth, existing or not;
    * a slot with a volume: accepted at any depth below it;
    * a slot with nothing mounted, absent or a leftover directory: refused.

    Residual: a volume hand-mounted where the table names no slot is accepted
    while unmounted too.
    """
    resolved = Path(path).resolve()
    slots = mount_location_ancestors(path)
    if slots and not any(slot_holds_a_volume(slot) for slot in slots):
        return None
    return containing_mount(resolved)


def root_can_be_created(configured_root: Path | str) -> bool:
    """Whether library state may be CREATED under ``configured_root``.

    A write asks whether creating the root lands on the volume this run is about,
    not whether it exists. Raises over a permission refusal from
    :func:`is_mount_point` underneath, so a caller must handle that by name.
    """
    return identity_source(Path(configured_root)) is not None


def resolve_mount_state(
    configured_root: Path | str,
    recorded_identity: str | None,
    *,
    identity_provider: IdentityProvider | None = None,
    mount_enumerator: MountEnumerator | None = None,
) -> MountStatus:
    """Probe the configured library root and return one diagnosis.

    "Is the recorded volume mounted SOMEWHERE" is asked before "is the path
    wrong", because knowing where it is turns a dead end into a one-line fix.
    """
    root = Path(configured_root)
    identity_of = identity_provider or default_identity_provider()
    enumerate_mounts = mount_enumerator or local_mount_points

    if recorded_identity is None:
        # A check that cannot fail is not a check: a refusal for destructive work.
        return MountStatus(MountState.IDENTITY_NOT_RECORDED, configured_root=root, mount_point=None)

    root_exists = root.is_dir()
    mount = containing_mount(root)
    observed = identity_of(mount)
    probed = partial(
        MountStatus, configured_root=root, mount_point=mount, recorded_identity=recorded_identity
    )

    if observed is None:
        return probed(MountState.IDENTITY_UNAVAILABLE)

    if same_identity(recorded_identity, observed):
        return probed(
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
            observed_identity=observed,
        )

    for candidate in enumerate_mounts():
        found = identity_of(Path(candidate))
        if found is not None and same_identity(recorded_identity, found):
            return probed(
                MountState.MOUNTED_ELSEWHERE, observed_identity=observed, found_at=Path(candidate)
            )

    return probed(
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
        observed_identity=observed,
    )


class Reach(Enum):
    """What a mount outcome permits, when the answer is not a plain yes or no.

    Named members make the read and write tables comparable row by row.
    """

    ALWAYS = "always"
    NEVER = "never"
    #: Read fallback: is there anything at the configured root to read at all.
    IF_ROOT_EXISTS = "if-root-exists"
    #: Write fallback: would creating the root land on this run's volume.
    IF_ROOT_CAN_BE_CREATED = "if-root-can-be-created"


#: Whether library-scoped state at the configured root may be READ, total over
#: the enum. The conditional rows are where identity could not be asked, which
#: on a platform with no adapter is every volume; for a read the remaining
#: signal is whether anything is there.
_STATE_READABLE: dict[MountState, Reach] = {
    MountState.OK: Reach.ALWAYS,
    # The volume matched and the root is not on it, so nothing to read.
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
    MountState.NOT_MOUNTED: Reach.NEVER,
    MountState.MOUNTED_ELSEWHERE: Reach.NEVER,
    MountState.FOREIGN_VOLUME: Reach.NEVER,
    MountState.IDENTITY_UNAVAILABLE: Reach.IF_ROOT_EXISTS,
    MountState.IDENTITY_NOT_RECORDED: Reach.IF_ROOT_EXISTS,
}

#: Whether that state may be WRITTEN, differing from the read table in three
#: rows where a read signal must not stand in for a write: a matched identity
#: with an absent root is the moment to create it, and the conditional rows ask
#: whether creating the root lands on this run's volume.
_STATE_WRITABLE: dict[MountState, Reach] = {
    **_STATE_READABLE,
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
    MountState.IDENTITY_UNAVAILABLE: Reach.IF_ROOT_CAN_BE_CREATED,
    MountState.IDENTITY_NOT_RECORDED: Reach.IF_ROOT_CAN_BE_CREATED,
}


def _reachable(table: dict[MountState, Reach], status: MountStatus) -> bool:
    verdict = table[status.state]
    if verdict is Reach.IF_ROOT_EXISTS:
        return Path(status.configured_root).is_dir()
    if verdict is Reach.IF_ROOT_CAN_BE_CREATED:
        return root_can_be_created(status.configured_root)
    return verdict is Reach.ALWAYS


def library_state_is_readable(status: MountStatus) -> bool:
    """Whether library-scoped state at the configured root may be read and believed.

    More permissive than the destructive gate, since the worst case is a wrong
    report; a deletion still goes through :func:`assert_library_volume`.
    """
    return _reachable(_STATE_READABLE, status)


def library_state_may_be_written(status: MountStatus) -> bool:
    """Whether library-scoped state may be CREATED at the configured root.

    A separate question from :func:`library_state_is_readable`: a matching
    identity with an absent root is nothing to read and the right moment to write.
    """
    return _reachable(_STATE_WRITABLE, status)


def assert_library_volume(
    configured_root: Path | str,
    recorded_identity: str | None,
    *,
    destructive: bool,
    identity_provider: IdentityProvider | None = None,
    mount_enumerator: MountEnumerator | None = None,
) -> MountStatus:
    """Refuse unless the configured path holds the volume the library was set up on.

    Callable with no paths, so a destructive session refuses before resolving
    any. Call it before destructive path resolution and again just before the
    commit, since a volume can be ejected mid-run. ``destructive`` decides only
    whether an unavailable or unrecorded identity is fatal.
    """
    status = resolve_mount_state(
        configured_root, recorded_identity,
        identity_provider=identity_provider, mount_enumerator=mount_enumerator,
    )
    tolerable = {MountState.IDENTITY_UNAVAILABLE, MountState.IDENTITY_NOT_RECORDED}
    if status.ok or (not destructive and status.state in tolerable):
        return status
    raise LibraryVolumeError(status, _describe(status))


def _describe(status: MountStatus) -> str:
    """A factual sentence about what was observed. No verb, no command (D2)."""
    root = status.configured_root
    if status.state is MountState.NOT_MOUNTED:
        return f"the library volume is not mounted; {root} does not exist"
    if status.state is MountState.MOUNTED_ELSEWHERE:
        return f"the library volume is mounted at {status.found_at}, not at the configured {root}"
    if status.state is MountState.FOREIGN_VOLUME:
        return (
            f"a different volume occupies {root}: recorded identity "
            f"{status.recorded_identity}, mounted identity {status.observed_identity}"
        )
    if status.state is MountState.LIBRARY_PATH_MISSING:
        return f"the library volume is mounted but {root} is not a directory on it"
    if status.state is MountState.IDENTITY_UNAVAILABLE:
        return f"no volume identity is readable for the filesystem at {status.mount_point}"
    if status.state is MountState.IDENTITY_NOT_RECORDED:
        return "no volume identity was recorded for this library"
    return status.state.value


# ---------------------------------------------------------------------------
# The readability sampler, kept as a SECOND and separate check
# ---------------------------------------------------------------------------


def assert_paths_readable(
    sample_paths: Iterable[Path | str],
    *,
    root: Path | str,
    sample_size: int = SAMPLE_SIZE,
) -> None:
    """Refuse when the files a caller is about to read all appear to be missing.

    Separate from the identity gate: identity proves the right disk, this proves
    its files are reachable. One resolving path passes; paths outside ``root``
    (streaming pseudo-locations) are skipped, not misses; an empty sample is a
    no-op; sampling stops at ``sample_size``.
    """
    root_text = str(root)
    sampled = 0
    for candidate in sample_paths:
        if not str(candidate).startswith(root_text):
            continue
        if Path(candidate).exists():
            return
        sampled += 1
        if sampled >= sample_size:
            break
    if sampled == 0:
        return
    raise LibraryUnreadableError(Path(root), sampled)


def assert_library_mounted(
    sample_paths: Iterable[Path | str] = (),
    *,
    root: Path | str,
    recorded_identity: str | None = None,
    destructive: bool = False,
    sample_size: int = SAMPLE_SIZE,
    identity_provider: IdentityProvider | None = None,
    mount_enumerator: MountEnumerator | None = None,
) -> MountStatus:
    """The one precondition a workflow calls: right volume, and readable files.

    ``destructive=True`` is the only difference between the gate on a report and
    the gate on a deletion. ``root`` has no default, so no one's disk is baked in.
    """
    status = assert_library_volume(
        root, recorded_identity, destructive=destructive,
        identity_provider=identity_provider, mount_enumerator=mount_enumerator,
    )
    assert_paths_readable(sample_paths, root=root, sample_size=sample_size)
    return status
