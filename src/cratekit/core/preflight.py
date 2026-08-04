"""The library volume precondition: is the RIGHT disk mounted where we think it is.

THE INCIDENT. Before this guard existed, every tag read went through a bare
``except: return None``. With the library volume unmounted, every track therefore
read as "no energy" and "no genre", which is a perfectly valid answer as far as
the router is concerned. The router did what it was told and filed the ENTIRE
plan into the fallback bucket, unrated, with no warning and no error. Nothing
failed. The library was simply reorganized wrongly, at scale, quietly. The tag
readers still degrade to None on an unreadable file, because one damaged file
must not abort a run, and that degrade is only safe because this precondition
runs first.

WHY A DIRECTORY CHECK IS NOT ENOUGH, which is the strengthening this module adds
over the guard it ports. The source system asked ``root.is_dir()``. Three
different broken states answer yes:

* a leftover empty mount-point directory on the boot disk, created when the
  volume was last ejected;
* a DIFFERENT disk mounted at the configured path;
* a restored BACKUP CLONE of the library mounted at the configured path.

The third is the dangerous one. A clone looks completely healthy: right layout,
right database, right filenames. Deletion against a clone deletes files that the
real library still references, and the review screen shows nothing unusual. So
the check is not "is something there" but "is this the SAME VOLUME the library
was configured against", answered by an identity the kernel reports rather than
by anything stored on the disk itself.

WHY NOT A MARKER FILE. It is the obvious portable answer and it is wrong in the
one case that matters: a clone carries the marker file too, so a marker-file
identity passes on the clone. Same reason ``st_dev`` and ``f_fsid`` are unusable,
though for a duller reason: both are kernel-assigned numbers that change between
mounts. The identity has to be the filesystem's own volume UUID, read through a
platform call.

THE FIVE OUTCOMES, and why they are five rather than one boolean. Each one has a
different fix, and a guard that says "the volume is wrong" without saying which
kind of wrong sends the user to unplug and replug a drive that was never the
problem. :class:`MountState` members are the structured cause (KTD25, D2): they
carry no verb, no command text, and no remediation prose. The CLI layer renders
a member into the sentence a user reads, so the vocabulary that owns exit codes
must reserve a code for each of them.

This module reads no configuration. The configured root and the recorded
identity arrive as parameters, and the platform seams arrive as injected
callables. That is what lets the whole state machine be tested against synthetic
volumes on a machine with one disk, and it is why the identity provider is a
seam rather than an ``if sys.platform`` inside the logic: adding Windows is a new
provider, not a rewrite of the decision.
"""

from __future__ import annotations

import os
import sys
import uuid
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable, Mapping, Sequence

from cratekit.core import cause

# How many on-volume paths the readability sampler will stat before giving up.
# Bounded because the alternative is stat-ing thousands of files just to fail.
SAMPLE_SIZE = 5


class MountState(Enum):
    """Why the library volume is or is not usable, as a structured cause.

    Every member is a distinct diagnosis with a distinct fix. The CLI layer maps
    each to an exit code and to remediation text; nothing here names a command,
    because a foundation-adjacent module that spells out a verb has quietly taken
    a decision that belongs one layer up.
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

    The observed and recorded identities are both carried even when they match,
    so a caller that logs a refusal can show what it compared. A refusal a user
    cannot check is a refusal a user learns to override.
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

    Deliberately NOT a ``SystemExit`` subclass. The source system raised one, so
    the only thing that survived to the process boundary was an exit status, and
    a caller in the middle could neither branch on the cause nor add context to
    it. A typed failure that collapses to an integer at any hop cannot be
    recovered downstream (KTD25), and the volume check is called from inside
    long-running work where recovery is exactly what a caller wants to attempt.
    """

    def __init__(self, status: MountStatus, detail: str = "") -> None:
        self.status = status
        self.state = status.state
        self.detail = detail
        super().__init__(detail or status.state.value)


class LibraryUnreadableError(Exception):
    """The right volume is mounted, and the files on it still cannot be read.

    A separate failure from :class:`LibraryVolumeError` because it has a separate
    cause: cloud eviction, a permissions change, or a library root pointing at a
    tree that no longer holds the music. Identity cannot detect any of those.
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

    A platform CALL, not a platform binary: no subprocess, no parsing of another
    tool's output, nothing that changes shape between operating-system releases.
    The value is stable across unmount, remount, a change of mount point, and a
    volume rename, which is the entire property that makes it an identity rather
    than a coincidence.

    Returns None rather than raising when the filesystem does not support the
    attribute. The caller treats an unavailable identity as its own outcome; a
    provider that raised would make "cannot tell" indistinguishable from
    "mismatch", and those have opposite remediations.
    """
    import ctypes
    import ctypes.util

    attr_bit_map_count = 5
    attr_vol_info = 0x80000000
    attr_vol_uuid = 0x00040000

    class _AttrList(ctypes.Structure):
        _fields_ = [
            ("bitmapcount", ctypes.c_ushort),
            ("reserved", ctypes.c_uint16),
            ("commonattr", ctypes.c_uint32),
            ("volattr", ctypes.c_uint32),
            ("dirattr", ctypes.c_uint32),
            ("fileattr", ctypes.c_uint32),
            ("forkattr", ctypes.c_uint32),
        ]

    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        libc.getattrlist.argtypes = [
            ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_size_t, ctypes.c_ulong,
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

    # The reply is a 4-byte length followed by the 16 UUID bytes. A filesystem
    # that does not carry the attribute returns SUCCESS with a short buffer, so
    # the length has to be checked or the parse reads whatever was in memory.
    length = int.from_bytes(buffer.raw[:4], sys.byteorder)
    if length < 20:
        return None
    raw = buffer.raw[4:20]
    if raw == b"\x00" * 16:
        # An all-zero UUID means "no identity", not "this identity". Treating it
        # as a value would make every such volume identical to every other.
        return None
    return str(uuid.UUID(bytes=raw))


def windows_volume_identity(path: Path) -> str | None:  # pragma: no cover - needs Windows
    """The volume serial number from ``GetVolumeInformationW``, or None.

    Thirty-two bits rather than a hundred and twenty-eight, so weaker than the
    macOS UUID, but real and read from the kernel by the same shape of call. It
    exists here to prove the seam is a seam: adding a platform is a function, not
    a change to the state machine below.
    """
    import ctypes

    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        return None

    serial = ctypes.c_uint32()
    drive = str(Path(path).anchor)
    ok = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive), None, 0,
        ctypes.byref(serial), None, None, None, 0,
    )
    if not ok or not serial.value:
        return None
    return f"{serial.value:08x}"


def null_volume_identity(path: Path) -> str | None:
    """No adapter for this platform. Always None, which is a refusal upstream.

    Never degrade to a path check and never degrade to a marker file. Both look
    like progress and both pass on the clone this whole module exists to catch.
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

    Local only. A stale network mount can block on stat for a long time, and a
    guard that hangs is worse than a guard that refuses, because the user cannot
    tell it apart from the work it was supposed to be protecting.

    Imported lazily so that a caller who injects its own enumerator, which every
    test does, never loads the extension module at all.
    """
    import psutil

    return [Path(part.mountpoint) for part in psutil.disk_partitions(all=False)]


# ---------------------------------------------------------------------------
# The real mount test
# ---------------------------------------------------------------------------


def containing_mount(path: Path) -> Path:
    """The mount point of the deepest existing ancestor of ``path``.

    ``os.path.ismount`` is the correct primitive and is genuinely cross-platform:
    on POSIX it compares device and inode against the parent and understands
    symlinks, on Windows it understands drive roots and reparse points. That
    replaces the directory check outright with no platform branch.

    The walk exists because a library root may legitimately be a SUBDIRECTORY of
    a mount. ``ismount`` on such a path is False even when everything is
    perfectly healthy, so asking it directly would refuse a working setup.

    Reporting is what this is for. A caller deciding whether an identity may be
    RECORDED wants :func:`identity_source`, which is this walk plus the question
    of whether it crossed anything that is not there.
    """
    current = deepest_existing(path)
    while not os.path.ismount(current) and current != current.parent:
        current = current.parent
    return current


def deepest_existing(path: Path) -> Path:
    """The deepest ancestor of ``path``, or ``path`` itself, that exists.

    Named because two callers need it and because it is half of what
    ``containing_mount`` does: that function starts here and then climbs to a
    mount point. Keeping the first half addressable is what lets a caller ask
    whether the climb crossed anything.
    """
    current = Path(path).resolve()
    while not current.exists() and current != current.parent:
        current = current.parent
    return current


#: WHERE A PLATFORM MOUNTS A VOLUME, as a directory and the depth beneath it at
#: which the mount point sits. A table, per platform, in the shape this module
#: already uses for identity providers, because it is the same kind of fact: what
#: this operating system does, declared once rather than branched on inline.
#:
#: It exists to answer one question that the filesystem alone cannot: a path that
#: does not exist yet is either a directory somebody will create, or the place a
#: volume will appear when it is attached, and those look identical to ``stat``.
#: The mount table describes the present and this describes where the future
#: arrives. On macOS an external volume mounts at ``/Volumes/<name>``, one level
#: down. On Linux the removable-media mounters use ``/media/<label>``,
#: ``/media/<user>/<label>`` and ``/run/media/<user>/<label>``.
#:
#: ``/mnt/<name>`` IS NOT A ROW, and it was one. The rule built on this table
#: refuses a slot with nothing mounted in it, so every row is a claim that an
#: empty directory THERE is evidence of an absent volume. That claim holds for a
#: directory some mounter creates and removes around a mount, which is what
#: ``/Volumes/<name>`` and the udisks locations are. It is false for ``/mnt``:
#: the filesystem hierarchy standard calls that the spot a person mounts
#: something on by hand, so the directory is made by hand and stays whether or
#: not anything is mounted, and a library living permanently at
#: ``/mnt/<name>/music`` on an ordinary root filesystem is an ordinary Linux
#: layout. With the row present that arrangement had no way through at all:
#: Linux has no identity adapter, so every mount outcome there is
#: ``IDENTITY_UNAVAILABLE`` and the write leg goes through
#: :func:`root_can_be_created`, which the row made permanently False. The wizard
#: refused to write the active template forever, doctor read for it, found
#: nothing and answered with "run setup", and the user re-ran setup forever.
#: Losing the row costs what R-18 already records for every hand-mounted
#: location: a drive mounted there is accepted while it is detached. That is a
#: gap in a platform that records no identity anyway, and it is smaller than a
#: guard that refuses a correct install with no way out (P7).
_VOLUME_MOUNT_LOCATIONS: Mapping[str, tuple[tuple[str, int], ...]] = MappingProxyType(
    {
        "darwin": (("/Volumes", 1),),
        "linux": (("/media", 1), ("/media", 2), ("/run/media", 2)),
    }
)


def volume_mount_locations() -> tuple[tuple[Path, int], ...]:
    """Where a volume mounts on THIS platform. Empty when the table has no row.

    A function rather than a constant so a caller can be driven against another
    platform's answer, which is the same seam shape ``default_identity_provider``
    is. An empty answer means this module knows of no auto-mount location here,
    and the caller treats that as "nothing to refuse", because inventing a
    location would refuse ordinary paths on a platform nobody has described.

    EVERY ROW IS RESOLVED, and that is not tidiness. The paths this is compared
    against are resolved, so one symlinked location silently matches nothing and
    the guard built on it becomes a no-op with no symptom: on a machine where the
    temporary directory is reached through a symlink, a synthetic ``/Volumes``
    under it never matched and every path under it was accepted.
    """
    return tuple(
        (Path(directory).resolve(), depth)
        for directory, depth in _VOLUME_MOUNT_LOCATIONS.get(sys.platform, ())
    )


def is_mount_point(path: Path) -> bool:
    """Whether the kernel has a filesystem mounted EXACTLY at ``path``.

    A named seam rather than a bare ``os.path.ismount`` call for the reason
    ``default_identity_provider`` is one: it is the single fact about the running
    machine that the rule below turns on, and a suite cannot mount a real volume.
    It answers False for a path that does not exist, which is a real answer:
    nothing is there, so nothing is mounted there.

    A PATH THIS ACCOUNT CANNOT STAT IS NOT AN EMPTY MOUNT SLOT, and calling it
    one was not a safe direction, it was a claim. ``os.path.ismount`` swallows
    every ``OSError`` and answers False, so with the volume ATTACHED and mounted
    under a directory this account cannot traverse, the caller was told "no
    volume is mounted there right now" and sent to plug in a drive that was
    already plugged in. Nothing had established that. A non answer converted into
    a positive assertion about the user's hardware is this branch's first
    recurring defect, and this was its seventh instance.

    So a False answer is CONFIRMED before it is returned, by asking the two
    questions ``ismount`` asks and letting them raise. The confirmation is the
    only thing added: the answer itself still comes from the standard library, so
    a platform that grows a new mount shape is answered by CPython rather than by
    a copy of its rules here.

    A SEAM STILL HAS TO BE PINNED, and this one was not: every test that drives
    the rule replaces it through the fixture, so the whole suite stayed green
    with the body replaced by ``return True`` AND with it replaced by
    ``return False``. ``return True`` accepts an ejected volume's leftover mount
    point, which is verbatim the blocking defect the rule exists to close, so the
    remedy the mount-location table already uses applies here too:
    ``tests/test_doctor.py`` asserts what this delegates to and drives the real
    function against a directory that IS a mount point on the running machine and
    one that is not.
    """
    if os.path.ismount(path):
        return True
    try:
        os.lstat(path)
        # The parent, through the slot itself, which is what ``ismount`` compares
        # against and what an unreadable slot refuses: resolving ".." needs
        # execute permission ON the directory, so a mount point with mode 0o000
        # raises here and answered False before.
        os.lstat(os.path.join(path, os.pardir))
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError as exc:
        if cause.permission_denied(exc) is not None:
            raise
        return False
    return False


def slot_holds_a_volume(slot: Path) -> bool:
    """Whether a volume is mounted in ``slot``, under this name or another.

    ``os.path.ismount`` answers False for a symlink by contract, which is right
    for "is a filesystem mounted at exactly this path" and wrong for the question
    the rule below is asking, which is whether the slot has a volume BEHIND it.
    Both readings have a case that only they get right, so both are asked:

    * a symlink standing in the mount directory and pointing at an ordinary
      directory elsewhere on the boot disk is a slot with no volume in it, and it shadows the mount point
      permanently, so a volume named SYMVOL attaches at ``SYMVOL 1`` instead.
      Reading an identity through it records the boot disk as the library's,
      which is the case-folding consequence reached by a second route;
    * every current macOS also puts the BOOT volume's own entry in that same
      mount directory, as a symlink to ``/``, and a library under it really is
      on the mounted boot volume. Refusing that would be a guard firing on a
      correct setup (P7).

    The difference between them is what the symlink resolves TO, so that is what
    is asked. ``is_mount_point`` stays the single seam underneath, so a test
    describing a machine still describes both answers.
    """
    if is_mount_point(slot):
        return True
    behind = Path(slot).resolve()
    return behind != Path(slot) and is_mount_point(behind)


def _names_one_path(left: Path, right: Path) -> bool:
    """Whether two paths name ONE thing on this filesystem, as the filesystem sees it.

    IT IS NAMED FOR WHAT IT ANSWERS. It was ``_names_one_directory`` and it never
    asked whether either side was a directory: two spellings of one regular file,
    and a FIFO compared with itself, both answered True under a name that
    promised otherwise. The caller compares an ancestor against a declared mount
    DIRECTORY, so the directory-ness it wants is a property of the declared row
    rather than something this comparison establishes, and a name that claimed
    otherwise is the kind of overclaim a reader trusts.

    THE STRING COMPARISON THIS REPLACES DISARMED THE WHOLE RULE FROM A SHELL.
    ``Path.relative_to`` compares path parts, which is case SENSITIVE, and the
    default macOS boot volume is case INSENSITIVE. So ``/volumes/NAME/Music`` and
    ``/Volumes/NAME/Music`` name one directory to every filesystem call and two
    different things to a guard built on parts: the canonical spelling refused
    with the drive detached and the lower-case one recorded the boot disk's UUID
    as the library's identity, for the life of that library.

    ``samefile`` compares ``(st_dev, st_ino)``, which is the filesystem's own
    answer, so it is right in BOTH directions without asking the platform
    anything. On a case-insensitive volume the two spellings share an inode and
    are one directory; on a case-sensitive one they are two directories with two
    inodes, or one of them does not exist, and either way this is False. The same
    comparison closes the symlinked-mount-directory case for free.

    The equality test comes first so that a pair of paths naming a directory that
    does not exist yet still answers, which ``samefile`` cannot: it stats both
    sides. Two DIFFERENT spellings of an absent directory answer False, which is
    the accepting direction, and that is the same answer the parts comparison
    gave for the same input.

    A COMPARISON THIS ACCOUNT COULD NOT MAKE IS NOT A COMPARISON THAT CAME BACK
    DIFFERENT. One handler over every ``OSError`` gave two case spellings of one
    directory on a case insensitive volume two different answers, True when both
    sides could be stat-ed and False when they could not, so PERMISSION rather
    than identity decided whether the mount rule saw a declared location at all.
    Absent and not-a-directory are real answers and stay False; a refusal from
    the operating system raises, and the callers that record an identity refuse
    over it by name.
    """
    if left == right:
        return True
    try:
        return left.samefile(right)
    except OSError as exc:
        if cause.permission_denied(exc) is not None:
            raise
        return False
    except ValueError:
        # An unrepresentable path, an embedded null among them. The comparison
        # was made and the answer is no; nothing was refused.
        return False


def _is_a_volume_mount_location(
    path: Path, locations: Sequence[tuple[Path, int]]
) -> bool:
    """Whether ``path`` is exactly where this platform mounts a volume.

    Asked by walking UP the declared number of levels and then asking the
    filesystem whether what is standing there is the declared directory, rather
    than by subtracting one string from another. See :func:`_names_one_path`
    for what that cost.
    """
    for directory, depth in locations:
        ancestor = path
        for _ in range(depth):
            if ancestor == ancestor.parent:
                break
            ancestor = ancestor.parent
        else:
            if _names_one_path(ancestor, directory):
                return True
    return False


def mount_location_ancestors(path: Path) -> tuple[Path, ...]:
    """Every place a volume would mount on the way down to ``path``.

    ``path`` itself counts, because a library root may BE a mount point. More
    than one can match and they are all returned: the removable-media mounters on
    Linux use ``/media/<label>`` and ``/media/<user>/<label>``, so one real path
    answers at two declared depths and only one of them is the mount.

    BOTH THE SPELLING GIVEN AND WHAT IT RESOLVES TO ARE WALKED, and the resolved
    chain alone was a hole. Resolving first is what makes a library reached
    through a symlinked parent match a declared row, and it also erases the row
    when the symlink points OUT of the mount directory: a symlinked mount point
    pointing at ``/elsewhere`` resolved to ``/elsewhere/library``, which crosses
    no declared location, so the rule found no slot to ask about and handed back
    the boot disk. A slot on either chain is a slot; :func:`slot_holds_a_volume`
    then decides whether anything is in it, and a symlink to a real mount is
    still a mount.
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

    The question is narrower than "which mount contains this path", and the
    difference is the whole point. ``containing_mount`` answers by walking up to
    the deepest existing ancestor and then to a mount point, which is correct for
    reporting and dangerous for recording: with the library drive unplugged,
    ``/Volumes/NAME/Music`` walks past the absent mount point to the boot disk,
    and recording THAT identity as the library's makes every destructive refusal
    pass against the disk holding the operating system.

    WHAT IS REFUSED IS A MOUNT SLOT THAT NOTHING IS MOUNTED IN, and that is the
    third rule here, because the first two were both about the wrong thing and
    the third was right about the question and wrong about the evidence.

    * "The root must already exist" refused every first run.
    * "The gap may be at most one level" refused every library nested two or more
      directories under an attached volume, which is the ordinary layout.
    * "Refuse only when the first MISSING directory is a mount location" reads
      absence as the whole hazard, and absence is only half of it. An ejected
      volume routinely leaves its mount point behind as an empty directory on the
      boot disk: that is the FIRST of the three broken states this module's own
      opening paragraphs exist to tell apart. With ``/Volumes/NAME`` sitting
      there as an ordinary directory, ``/Volumes/NAME/library`` crosses no gap at
      all, so the walk fell straight through to ``/`` and handed back the boot
      disk, which is verbatim the defect the first rule was written for.

    So the question is asked of the SLOT rather than of the gap: for every place
    on the way down where this platform mounts a volume, is a volume mounted
    there right now. Depth is not consulted, absence is not consulted, and what
    the filesystem is asked is the one thing it can actually answer.

    Three shapes:

    * no mount slot on the way down, so the path is on ordinary storage and the
      identity of whatever holds it is the identity it will keep. Accepted at any
      depth, existing or not;
    * a mount slot with a volume in it, so the identity read is that volume's.
      Accepted, at any depth below it;
    * a mount slot with nothing mounted in it, whether the directory is absent or
      is a leftover. REFUSED, because the identity a walk finds now belongs to
      whatever filesystem is above the slot rather than to the volume that will
      occupy it.

    A residual, stated because it is not covered: a volume hand-mounted somewhere
    this table does not name. It is accepted while mounted, which is correct, and
    accepted while unmounted, which is not. Naming the identity resolves it, and
    so does adding the location to the table.
    """
    resolved = Path(path).resolve()
    slots = mount_location_ancestors(path)
    if slots and not any(slot_holds_a_volume(slot) for slot in slots):
        return None
    return containing_mount(resolved)


def root_can_be_created(configured_root: Path | str) -> bool:
    """Whether library state may be CREATED under ``configured_root``.

    The write-side companion to "is anything there to read", and a different
    question from it. What a write needs to know is not whether the directory
    exists but whether creating it lands on the volume this run is talking about,
    which is what :func:`identity_source` answers. Sharing the read's "does it
    exist" test was a read signal applied to a write: it refused a first run on
    every platform with no identity adapter, which is every platform that is not
    macOS or Windows.
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

    Pure with respect to the outside world except through its two seams, which
    is what makes every branch below reachable in a test without a second disk.

    The order of the checks is the interesting part. "Is the recorded volume
    mounted SOMEWHERE" is asked before "is the configured path wrong", because
    knowing where the volume actually is turns a dead end into a one-line fix.
    """
    root = Path(configured_root)
    identity_of = identity_provider or default_identity_provider()
    enumerate_mounts = mount_enumerator or local_mount_points

    if recorded_identity is None:
        # Nothing was recorded, so nothing can be asserted. This is a refusal for
        # destructive work rather than a pass, for the same reason an unset
        # version pin is: a check that cannot fail is not a check.
        return MountStatus(
            MountState.IDENTITY_NOT_RECORDED, configured_root=root, mount_point=None
        )

    root_exists = root.is_dir()
    mount = containing_mount(root)
    observed = identity_of(mount)

    if observed is None:
        return MountStatus(
            MountState.IDENTITY_UNAVAILABLE,
            configured_root=root,
            mount_point=mount,
            recorded_identity=recorded_identity,
        )

    if observed == recorded_identity:
        return MountStatus(
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
            configured_root=root,
            mount_point=mount,
            recorded_identity=recorded_identity,
            observed_identity=observed,
        )

    for candidate in enumerate_mounts():
        if identity_of(Path(candidate)) == recorded_identity:
            return MountStatus(
                MountState.MOUNTED_ELSEWHERE,
                configured_root=root,
                mount_point=mount,
                recorded_identity=recorded_identity,
                observed_identity=observed,
                found_at=Path(candidate),
            )

    return MountStatus(
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
        configured_root=root,
        mount_point=mount,
        recorded_identity=recorded_identity,
        observed_identity=observed,
    )


class Reach(Enum):
    """What a mount outcome permits, when the answer is not a plain yes or no.

    Two of the four are conditions rather than verdicts, and they are DIFFERENT
    conditions, which is the thing a boolean table could not say. Writing them as
    named members is what makes the read table and the write table comparable
    row by row, and what makes "these two tables differ in exactly these rows" an
    assertion rather than a claim.
    """

    ALWAYS = "always"
    NEVER = "never"
    #: Read fallback: is there anything at the configured root to read at all.
    IF_ROOT_EXISTS = "if-root-exists"
    #: Write fallback: would creating the root land on the volume this run is
    #: talking about, rather than in a gap a volume will later occupy.
    IF_ROOT_CAN_BE_CREATED = "if-root-can-be-created"


#: Whether library-scoped state at the configured root may be READ, per mount
#: outcome. A TOTAL mapping over the enum.
#:
#: The two conditional rows are the states where the identity question could not
#: be ASKED, which is not the same as being answered wrongly: a platform with no
#: identity adapter answers None for every volume, mounted or not, so a table
#: with no conditional row would either lock that platform out of its own library
#: state entirely or hand it the same blanket yes it hands a machine with the
#: wrong disk attached. For a READ the remaining signal is whether anything is
#: there.
_STATE_READABLE: dict[MountState, Reach] = {
    MountState.OK: Reach.ALWAYS,
    # The volume matched and the ROOT is not on it. There is nothing under a
    # path that is not there, so there is nothing to read and no answer to give.
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
    MountState.NOT_MOUNTED: Reach.NEVER,
    MountState.MOUNTED_ELSEWHERE: Reach.NEVER,
    MountState.FOREIGN_VOLUME: Reach.NEVER,
    MountState.IDENTITY_UNAVAILABLE: Reach.IF_ROOT_EXISTS,
    MountState.IDENTITY_NOT_RECORDED: Reach.IF_ROOT_EXISTS,
}

#: Whether library-scoped state at the configured root may be WRITTEN. A SECOND
#: table over the same enum, differing in THREE rows, and every one of the three
#: is a place where a read signal had been standing in for a write signal.
#:
#: ``LIBRARY_PATH_MISSING`` is the first: the recorded identity MATCHED and only
#: the directory is absent, which is nothing to read and precisely the moment
#: when creating it is correct, a first run on the right volume or a library
#: folder somebody renamed. One shared table refused that write and printed a
#: sentence its own parenthetical contradicted.
#:
#: The other two are the conditional rows. "Is anything there" answers a read;
#: what a write needs to know is whether CREATING the root lands on the volume
#: this run is talking about. Sharing the read's condition refused a first run on
#: every platform with no identity adapter, for the same reason and with the same
#: false sentence, one leg further down.
_STATE_WRITABLE: dict[MountState, Reach] = {
    MountState.OK: Reach.ALWAYS,
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
    MountState.NOT_MOUNTED: Reach.NEVER,
    MountState.MOUNTED_ELSEWHERE: Reach.NEVER,
    MountState.FOREIGN_VOLUME: Reach.NEVER,
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

    Doctor asks before it reports on the active template and on the session log,
    because a path that is not there and a path on a disk that is not there
    produce identical bytes, none, and reading the second as "nothing to report"
    is a positive claim about a disk nobody looked at.

    Deliberately more permissive than the destructive gate:
    ``assert_library_volume`` already treats an unreadable identity as tolerable
    for non-destructive work, on the argument that the worst case there is a
    wrong report rather than deleted music. Reading a template is in that class.
    Deciding a DELETION is not, and that decision still goes through the
    assertion above, which is stricter on purpose.
    """
    return _reachable(_STATE_READABLE, status)


def library_state_may_be_written(status: MountStatus) -> bool:
    """Whether library-scoped state may be CREATED at the configured root.

    The wizard asks before it copies the active taxonomy beside the library,
    because writing library state onto whatever filesystem happens to be at that
    path leaves a leftover mount point on the boot disk and puts coupled state
    where no snapshot of that library will ever capture it.

    It is a separate question from :func:`library_state_is_readable` rather than
    the same one phrased twice, and the row that differs is the proof: a matching
    identity with an absent root is nothing to read and exactly the right moment
    to write. Sharing one answer between the two made the wizard refuse a correct
    first run and made doctor's explanation of the refusal false.
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

    Callable with no paths at all, and that is a requirement rather than a
    convenience: a destructive session must refuse BEFORE it resolves a single
    path, because resolving paths against the wrong volume is already the damage.

    Call it twice. Once before any destructive path resolution and once more
    immediately before the commit. A volume can be ejected mid-run, and a check
    that only ran at the start proves nothing about the moment the write lands.

    ``destructive`` decides one thing only: whether an UNAVAILABLE identity is
    fatal. A read-only workflow on a platform with no identity adapter may
    proceed, because the worst case is a wrong report. A destructive one may not,
    because the worst case is deleted music.
    """
    status = resolve_mount_state(
        configured_root,
        recorded_identity,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
    if status.ok:
        return status

    tolerable = {MountState.IDENTITY_UNAVAILABLE, MountState.IDENTITY_NOT_RECORDED}
    if not destructive and status.state in tolerable:
        return status

    raise LibraryVolumeError(status, _describe(status))


def _describe(status: MountStatus) -> str:
    """A factual sentence about what was observed. No verb, no command.

    Rendering a remediation is the CLI layer's job (D2). What this owes the CLI
    is the facts it cannot re-derive: which path was checked, and where the
    recorded volume actually turned up.
    """
    root = status.configured_root
    if status.state is MountState.NOT_MOUNTED:
        return f"the library volume is not mounted; {root} does not exist"
    if status.state is MountState.MOUNTED_ELSEWHERE:
        return (
            f"the library volume is mounted at {status.found_at}, not at the "
            f"configured {root}"
        )
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

    Not merged into the identity gate, because it answers a different question
    and needs different inputs. Identity proves the right disk is attached;
    this proves its files are actually reachable, which identity cannot tell you.
    A cloud-evicted tree, a permissions change, or a library root pointing at the
    wrong subtree all pass an identity check and fail here.

    Four behaviours, each of which exists because of a real false alarm:

    * ONE resolving path passes the whole check. A single moved file must never
      block a legitimate run.
    * Paths outside ``root`` are SKIPPED, not counted as misses. A collection can
      hold streaming pseudo-locations that decode to something outside the
      volume; counting those trips the guard on a perfectly healthy mount.
    * An empty sample is a no-op. Nothing to read means nothing to mis-route.
    * Sampling stops at ``sample_size``, so failing is cheap on a huge plan.
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

    One resolver bound at two strengths rather than two resolvers. Every workflow
    calls this; a destructive one passes ``destructive=True``, which is the only
    difference between the gate on a report and the gate on a deletion.

    ``root`` has no default. A default library root would be one person's disk
    baked into shipped code, and the whole configuration layer exists so that it
    is not.
    """
    status = assert_library_volume(
        root,
        recorded_identity,
        destructive=destructive,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
    assert_paths_readable(sample_paths, root=root, sample_size=sample_size)
    return status
