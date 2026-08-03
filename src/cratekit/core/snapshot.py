"""KTD21b: the database and the state coupled to it, captured as one matched set.

The guarded writer already captures the database, the files the storage engine
keeps beside it, and rekordbox's own legacy playlist file. That is the DATABASE
half and it is complete. What it cannot do on its own is the other half: the
registry, the watermarks, the tombstones, the declines and the active taxonomy
template all describe the rows in that database, and a capture that takes one
without the other produces a recovery point that is internally inconsistent. That
inconsistency is the plan's top-ranked risk stated as a file layout.

So this module is the layer ABOVE ``rb_writer.snapshot_db`` rather than a second
copy of it. It composes:

1. the database half, delegated verbatim to the writer, because duplicating a
   copier that already handles the engine checkpoint would give the product two
   answers to one question;
2. the coupled half, copied from whatever ``config.snapshot_sources`` declares;
3. one verification of the captured database, whose verdict is part of the
   returned record because no session may commit behind a capture that did not
   verify;
4. one manifest recording exactly what was taken, because a restore has to know
   what it may replace and, just as importantly, what was legitimately absent.

THE CAPTURE SET IS DERIVED AND IS NEVER LISTED HERE. Every path comes from the
state inventory. A companion list maintained beside that inventory is the drift
the inventory exists to abolish, and the specific cost of that drift is a
database copied without the committed transactions the engine is still holding
outside the main file: a copy that opens cleanly and is quietly behind, which is
the worst shape a backup can take. There is deliberately no file-suffix literal
anywhere in this module, and ``tests/test_config.py`` asserts that by reading
this source.

ABSENCE IS NORMAL, NOT AN ERROR. A database that was just folded in by the
engine has no companion files beside it. A library that has never run a sweep
has no coupled directory yet. Every one of those paths is copied only if it is
there, and the manifest records which were and which were not, because "this was
not captured" and "this was captured empty" call for different restores.

RETENTION BELONGS TO U32 AND CAPACITY ARRIVED WITH IT. Nothing here prunes or
bounds; ``rb_writer.prune_snapshots`` already exists, ``core.restore`` gives it
the count, age and byte bounds R30 asks for, and this module's job is to make
what it spares real. What DID land here is the capacity refusal, and it landed
here rather than beside the retention policy because this is the function that
writes: a check placed anywhere else is a check some future caller reaches the
copy without. See :func:`assert_room_for_capture`, and :func:`assert_room_for`
underneath it, which the restore asks the same question of the library volume
because a restore copies the same bytes back the other way.

LAYER: infrastructure. It reads configuration, does input and output, and
carries remediation TOKENS rather than any text a user types (D2).
"""

from __future__ import annotations

import json
import logging
import os
import secrets
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from cratekit.core import config, rb_writer
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)

#: The record written inside every capture directory. A capture with no manifest
#: is a directory of files whose provenance a restore has to guess at.
MANIFEST_NAME = "capture.json"

#: Bumped only when the manifest's shape changes incompatibly. A manifest written
#: by a later build is not read: guessing at a shape this build does not know is
#: how a restore replaces the wrong set of files.
MANIFEST_SCHEMA_VERSION = 1

#: The state entry whose path is the database. Named once so this module and the
#: writer cannot disagree about which entry carries the companion declaration.
DATABASE_KEY = "rekordbox_db"

#: The state entry that holds captures. Named once for the same reason.
STORE_KEY = "snapshots"

#: Verifies one captured database file. A seam, so the battery can drive both
#: verdicts without a real rekordbox database, and so the verdict has exactly one
#: producer rather than one per caller.
Verifier = Callable[[Path], bool]


def new_stamp(now: datetime | None = None) -> str:
    """A sortable, filesystem-safe directory name for one capture.

    The random tail exists because two captures can begin inside the same second
    on a machine running a queued job beside an interactive one, and a collision
    would have the second capture write into the first one's directory.

    No colon and no space, unlike the run identifier, because this string becomes
    a directory name on whatever filesystem the user's library lives on and a
    colon is not a legal character on all of them.
    """
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H%M%SZ')}-{secrets.token_hex(2)}"


@dataclass(frozen=True, slots=True)
class CapturedSource:
    """One declared source and what became of it.

    ``captured`` is None when the source was simply not there, which is a normal
    outcome rather than a failure. Recording the ABSENCE explicitly is what lets
    a restore tell "there was nothing to put back" from "we never looked", and
    those two call for opposite behaviour.
    """

    source: Path
    captured: Path | None
    directory: bool = False

    @property
    def present(self) -> bool:
        return self.captured is not None

    def to_json(self) -> dict[str, Any]:
        return {
            "source": str(self.source),
            "captured": str(self.captured) if self.captured is not None else None,
            "directory": self.directory,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> CapturedSource:
        captured = data.get("captured")
        return cls(
            source=Path(str(data["source"])),
            captured=Path(str(captured)) if captured else None,
            directory=bool(data.get("directory", False)),
        )


@dataclass(frozen=True, slots=True)
class Capture:
    """One matched set on disk, and whether anything may commit behind it.

    ``integrity_verified`` is carried rather than re-derived on demand. The check
    runs once, immediately after the copy, against the bytes that were actually
    written; asking again later would answer about a file that has had time to
    change, and a gate whose input can move between the check and its use is not
    a gate.
    """

    stamp: str
    root: Path
    database: Path | None
    integrity_verified: bool
    sources: tuple[CapturedSource, ...] = ()
    manifest: Path | None = None

    @property
    def verified(self) -> bool:
        """True only when a database was captured AND it passed its check.

        Both halves, because a capture with no database at all would otherwise
        report as trivially sound while protecting nothing.
        """
        return self.database is not None and self.integrity_verified

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "stamp": self.stamp,
            "root": str(self.root),
            "database": str(self.database) if self.database is not None else None,
            "integrity_verified": self.integrity_verified,
            "sources": [entry.to_json() for entry in self.sources],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any], *, manifest: Path | None = None) -> Capture:
        version = data.get("schema_version")
        if version != MANIFEST_SCHEMA_VERSION:
            raise refuse(
                "internal-error",
                f"the capture manifest declares schema {version!r} and this build "
                f"understands {MANIFEST_SCHEMA_VERSION}; refusing to guess which "
                f"files a restore may replace",
                remedy=Remedy.UPGRADE_CRATEKIT,
                detail={"schema_version": version},
            )
        database = data.get("database")
        return cls(
            stamp=str(data["stamp"]),
            root=Path(str(data["root"])),
            database=Path(str(database)) if database else None,
            integrity_verified=bool(data.get("integrity_verified", False)),
            sources=tuple(
                CapturedSource.from_json(entry) for entry in (data.get("sources") or ())
            ),
            manifest=manifest,
        )


def store_root(cfg: config.Config) -> Path:
    """Where captures live: library-scoped, and outside everything they capture."""
    return config.state_path(STORE_KEY, cfg)


def database_paths(cfg: config.Config) -> tuple[Path, ...]:
    """The database and every file the storage engine keeps beside it.

    Composed by the inventory, never spelled here. This is the exact set
    ``rb_writer.snapshot_db`` already copies, and it is derived rather than
    restated so that "what the writer took" and "what this module skips" cannot
    drift apart into a file captured twice or a file captured never.
    """
    return (config.state_path(DATABASE_KEY, cfg), *config.sidecar_paths(DATABASE_KEY, cfg))


def _harden(root: Path) -> None:
    """Give every file and directory under ``root`` an explicit private mode.

    DERIVED BY WALKING, never by listing what was copied (P3). The copier
    preserves each source file's own permission bits, and the rekordbox database
    is world-readable on a normal install, so a capture that inherited those
    modes would be a world-readable copy of the user's whole library state.
    Walking also covers the files the writer copied, which a hand-list would miss
    the moment the writer learns to copy a fifth thing.

    Guarded on the platform having POSIX modes at all, so a filesystem without
    them degrades rather than crashing (P1).
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - every supported platform has it
        return
    for current, directories, files in os.walk(root):
        here = Path(current)
        for name in directories:
            _chmod(here / name, config.PRIVATE_DIR_MODE)
        for name in files:
            _chmod(here / name, config.PRIVATE_FILE_MODE)
    _chmod(root, config.PRIVATE_DIR_MODE)


def _chmod(path: Path, mode: int) -> None:
    """Best effort, and deliberately not fatal.

    A capture whose mode could not be tightened is still a capture, and refusing
    here would trade a permissions weakness for having no recovery point at all,
    which is the worse of the two.
    """
    try:
        os.chmod(path, mode)
    except OSError as exc:
        logger.debug("could not set the mode on %s: %s", path, exc)


def _refuse_if_nested(source: Path, store: Path) -> None:
    """Refuse when a declared source and the capture store contain each other.

    The schema already forbids this and ``tests/test_config.py`` asserts it. It
    is checked again HERE, at the moment of copying, because a derivation is only
    as good as its coverage of the real set (P4) and the failure it prevents is
    unbounded: a store inside a source means every capture contains every capture
    before it, so the tenth one costs the sum of the first nine.
    """
    if source == store or store in source.parents or source in store.parents:
        raise refuse(
            "internal-error",
            f"the declared capture source {source} and the capture store {store} "
            f"contain one another, so a capture would nest every earlier capture "
            f"inside the new one",
            remedy=Remedy.REPORT_DEFECT,
            detail={"source": str(source), "store": str(store)},
        )


def _copy(source: Path, destination: Path) -> CapturedSource:
    """Copy one declared source if it is there. Absence is a recorded outcome."""
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=False)
        return CapturedSource(source=source, captured=destination, directory=True)
    if source.is_file():
        shutil.copy2(source, destination)
        return CapturedSource(source=source, captured=destination, directory=False)
    return CapturedSource(source=source, captured=None, directory=False)


def _verify(database: Path, verifier: Verifier | None) -> bool:
    """Run the integrity check, failing CLOSED on anything unexpected.

    A verdict this module cannot produce is treated as "did not verify", because
    the verdict gates a commit and the safe direction for an unknown is to refuse
    it. Reporting True on an unreadable answer would put a session behind a
    capture nobody has established is sound, which is the one thing the check
    exists to prevent.
    """
    check = verifier if verifier is not None else rb_writer.integrity_ok
    try:
        return bool(check(database))
    except Exception as exc:  # noqa: BLE001 - a check that cannot answer has not passed
        logger.warning("the capture integrity check could not run, so it did not pass: %s", exc)
        return False


#: How much more room than the capture needs must be free before one is taken.
#:
#: A copy is not the only thing that lands: the manifest goes in beside it, the
#: engine checkpoint can grow the database file just before it is read, and a
#: filesystem driven to zero free bytes fails in ways that have nothing to do
#: with this write and are much harder to read afterwards. Ten percent is small
#: enough that it never refuses a capture a disk could genuinely hold.
CAPACITY_HEADROOM = 1.10


#: What one filesystem block costs when the platform will not say. Used only as
#: the floor for a file whose ``st_blocks`` is unavailable; every POSIX platform
#: this product supports reports it.
ALLOCATION_UNIT = 4096

#: What one directory entry costs beyond the blocks its file occupies. A copy of
#: a directory tree grows the destination's own directory structure as well as
#: allocating the files, and on a copy-on-write filesystem that growth is not
#: small. MEASURED rather than guessed; see :func:`_allocated_size`.
DIRECTORY_ENTRY_OVERHEAD = 2048


def _allocated_size(path: Path, *, entry_overhead: int = DIRECTORY_ENTRY_OVERHEAD) -> int:
    """What ``path`` costs a filesystem, not what its bytes add up to.

    THE DIFFERENCE IS TWO ORDERS OF MAGNITUDE ON THE SHAPE THIS PRODUCT ACTUALLY
    CAPTURES, which is why the apparent size is not used. A filesystem allocates
    whole blocks and grows its own directory structure, so a tree of many small
    documents costs far more than the sum of its file lengths. ``review_queue``
    and ``label_outcomes`` are both directories of small documents, and both are
    captured whole. Measured on the development machine:

    ======================  ==========  ===========  ==================
    coupled contents        ``st_size``  allocated   real free-space
    ======================  ==========  ===========  ==================
    10 MiB database only    10,485,760  10,489,856   10,489,856
    2,000 items, 120 bytes     241,024   8,200,192    9,617,408
    20,000 items, 60 bytes   1,201,024  81,928,192  112,484,352
    ======================  ==========  ===========  ==================

    The middle column is ``st_blocks * 512`` and it accounts for the blocks. The
    gap between it and the last column is the destination's own directory growth,
    which is why every entry also carries :data:`DIRECTORY_ENTRY_OVERHEAD`. With
    both terms the estimate is above the measured cost in all three rows, which
    is the direction that matters: an over-estimate refuses a capture that would
    have just fitted, and an under-estimate writes the truncated capture this
    exists to prevent.

    ``entry_overhead`` IS ZERO ON THE RESTORE SIDE, and the asymmetry is real
    rather than a tuning knob. The term above accounts for growth in the
    DESTINATION's own directory structure, which a capture genuinely causes: it
    writes a tree of entries that did not exist. A restore writes a tree back over
    one of nearly the same shape, so those entries already exist and the marginal
    growth is not a fresh allocation. Charging it on both sides refused restores
    that fit.

    Absence is normal rather than exceptional, exactly as it is everywhere else
    in this module: a database just folded in by the engine has no companion
    files, and a library that has never run a sweep has no coupled directory yet.
    A missing source contributes nothing, because it will contribute nothing to
    the copy.
    """
    try:
        if path.is_dir():
            total = entry_overhead
            for current, directories, files in os.walk(path):
                here = Path(current)
                total += entry_overhead * len(directories)
                for name in files:
                    total += _allocated_file(here / name, entry_overhead=entry_overhead)
            return total
        return _allocated_file(path, entry_overhead=entry_overhead)
    except OSError:
        return 0


def _allocated_file(path: Path, *, entry_overhead: int = DIRECTORY_ENTRY_OVERHEAD) -> int:
    """One file's cost: its blocks, or its rounded-up length, whichever is larger.

    The larger of the two, because ``st_blocks`` under-reports a SPARSE file and a
    copy of a sparse file is not sparse at the destination unless the copier was
    asked to make it so, and this module's copier is not.
    """
    try:
        stat_result = path.stat()
    except OSError:
        return 0
    blocks = getattr(stat_result, "st_blocks", None)
    occupied = 0 if blocks is None else int(blocks) * 512
    rounded = -(-int(stat_result.st_size) // ALLOCATION_UNIT) * ALLOCATION_UNIT
    return max(occupied, rounded) + entry_overhead


def _free_bytes(root: Path) -> int | None:
    """Free space on the filesystem that will hold ``root``, or None if unknowable.

    The capture directory does not exist yet, and neither may its parent, so the
    question is asked of the nearest ancestor that DOES exist. Asking about a
    path that is not there answers about nothing.

    None is not zero, and it is NOT a pass either. See
    :func:`assert_room_for`: every supported platform answers this, so the only
    way to reach None is a path that is disappearing or unreadable underneath the
    question, and that is a reason to refuse rather than to proceed.
    """
    probe = root
    while True:
        if probe.exists():
            try:
                return shutil.disk_usage(probe).free
            except OSError:
                return None
        if probe.parent == probe:
            return None
        probe = probe.parent


def assert_room_for_capture(
    cfg: config.Config,
    *,
    root: Path | str | None = None,
    headroom: float = CAPACITY_HEADROOM,
    free_bytes: int | None = None,
) -> int:
    """Refuse BEFORE a capture is taken when the store cannot hold one.

    Returns the estimate, so a caller that wants to report it does not have to
    compute it a second way.

    THE REFUSAL HAS TO COME FIRST, and that is the whole property. A copy that
    runs out of room part way leaves a truncated database inside a directory that
    looks like a capture, and the session then commits behind it. The integrity
    check would catch that particular file, but only after the partial write has
    already consumed the last of the disk and only if the truncation happens to
    land somewhere the check reads. Refusing up front costs one stat per source
    and leaves the store byte for byte as it was found.

    THE ESTIMATE IS DERIVED FROM THE SAME DECLARATION THE COPY USES. It walks
    ``database_paths`` and ``config.snapshot_sources``, which is exactly what
    :func:`capture` copies, so an entry added to the inventory is measured
    without anybody remembering to add it here (P4). It is measured in ALLOCATED
    bytes rather than in apparent ones, for the reason :func:`_allocated_size`
    states at length with the measurements behind it: the apparent size of a tree
    of small documents under-reports what the copy costs by up to two orders of
    magnitude, and both of this product's queue directories are exactly that
    shape.
    """
    destination_root = Path(root) if root is not None else store_root(cfg)
    sources = {*database_paths(cfg), *config.snapshot_sources(cfg)}
    playlist = config.state_path(DATABASE_KEY, cfg).parent / rb_writer.MASTER_PLAYLIST_XML
    sources.add(playlist)
    needed = sum(_allocated_size(source) for source in sorted(sources))
    return assert_room_for(
        needed,
        destination_root,
        what="one capture of this library",
        headroom=headroom,
        free_bytes=free_bytes,
    )


def assert_room_for(
    needed: int,
    destination: Path | str,
    *,
    what: str,
    steps: tuple[str, ...] = (
        "free space on the volume holding this path, or prune older captures, "
        "and run this again",
    ),
    headroom: float = CAPACITY_HEADROOM,
    free_bytes: int | None = None,
) -> int:
    """Refuse when ``destination``'s filesystem cannot hold ``needed`` bytes.

    Split out of :func:`assert_room_for_capture` so a RESTORE can ask the same
    question of the library volume. It had only one call site, inside the capture
    function, so a restore that copies a whole database and coupled tree back onto
    the library checked nothing about free space at all; and a restore is the verb
    people reach for when a disk is already misbehaving.

    A FILESYSTEM THAT WILL NOT REPORT ITS FREE SPACE REFUSES. That is the reverse
    of what this used to do, and the reverse is right. Every platform this product
    supports answers ``statvfs``, so the only way to get no answer is a path that
    is disappearing or unreadable underneath the question. Reading that as
    permission to proceed is reading the one signal that something is wrong as the
    all-clear.
    """
    where = Path(destination)
    available = free_bytes if free_bytes is not None else _free_bytes(where)
    required = int(needed * headroom)
    if available is None:
        raise refuse(
            "snapshot-store-full",
            f"the free space on the filesystem holding {where} could not be read, "
            f"so there is no way to know whether {what} fits; every supported "
            f"platform answers this question, which makes silence a symptom of the "
            f"path being unreadable rather than a platform that cannot say",
            steps=(
                "check that the volume holding this path is mounted and readable, "
                "and run this again",
            ),
            scope=Scope.SESSION,
            detail={"root": str(where), "required_bytes": required, "estimated_bytes": needed},
        )
    if available >= required:
        return needed
    raise refuse(
        "snapshot-store-full",
        f"{where} has {available} bytes free and {what} needs about {required}; "
        f"refusing before the copy rather than writing a truncated one and "
        f"committing behind it",
        steps=steps,
        scope=Scope.SESSION,
        detail={
            "root": str(where),
            "free_bytes": available,
            "required_bytes": required,
            "estimated_bytes": needed,
        },
    )


def restore_peak_bytes(record: Capture) -> int:
    """The largest TRANSIENT a restore of this capture needs. Not the sum.

    A CAPTURE AND A RESTORE HAVE OPPOSITE SHAPES AND ASKING THE SAME QUESTION OF
    BOTH REFUSES RESTORES THAT FIT. A capture copies everything into a directory
    that did not exist, so its cost is the SUM and the whole sum has to be free at
    once. A restore replaces things one at a time: a file is staged beside its
    target and renamed over it, which frees the old copy before the next step
    begins, and a directory is staged beside its target and swapped, which frees
    the old tree the same way. So at no moment does a restore hold more than one
    replacement's worth of extra space, and the steady-state delta is near zero
    because the library already holds the previous versions of everything being
    written.

    Measured on the shape that exposed it: an 8 MiB database, a 4 MiB write-ahead
    log and a 2,000 item coupled tree summed to 24,879,104 bytes and demanded
    27,367,014, so a volume with 9,437,184 free was refused, against a real peak
    of roughly 8.4 MiB. The peak measure asks for 9,227,468 and lets it through.

    Measured on the CAPTURE rather than on the live library, because the capture is
    what is about to be copied, and with ``entry_overhead`` at zero for the reason
    :func:`_allocated_size` gives.
    """
    return max(
        (
            _allocated_size(entry.captured, entry_overhead=0)
            for entry in record.sources
            if entry.captured is not None
        ),
        default=0,
    )


def capture(
    cfg: config.Config,
    *,
    stamp: str | None = None,
    db: Any = None,
    root: Path | str | None = None,
    verifier: Verifier | None = None,
    now: datetime | None = None,
) -> Capture:
    """Take one matched capture of the database and the state coupled to it.

    ``db`` is the caller's OPEN handle, passed straight through to the writer so
    it can fold the engine's outstanding transactions into the main file before
    the copy. That is the belt; copying the companion files is the braces, and
    the braces are what actually hold, because a fold can fail for reasons a
    capture has to survive.

    ``verifier`` and ``root`` exist so the battery can drive every branch without
    a rekordbox database and without a library volume. Neither is a safety
    escape: a verdict that does not come back true still blocks every commit
    behind it, whichever function produced it.
    """
    destination_root = Path(root) if root is not None else store_root(cfg)
    # BEFORE the collision check and before anything is created, because a
    # refusal that has already made a directory is a refusal that did something.
    assert_room_for_capture(cfg, root=destination_root)
    chosen = stamp or new_stamp(now)
    destination = destination_root / chosen
    if destination.exists():
        raise refuse(
            "internal-error",
            f"a capture directory already exists at {destination}; writing a "
            f"second capture into it would interleave two recovery points",
            remedy=Remedy.REPORT_DEFECT,
            detail={"stamp": chosen, "root": str(destination_root)},
        )

    store = store_root(cfg)
    already = set(database_paths(cfg))
    declared = config.snapshot_sources(cfg)
    for source in declared:
        _refuse_if_nested(source, store)

    # The database half, delegated. The writer owns the engine fold, the
    # companion files, and rekordbox's own legacy playlist file, and it owns them
    # in one place rather than two.
    try:
        database = rb_writer.snapshot_db(stamp=chosen, root=destination_root, db=db, cfg=cfg)
    except CratekitError:
        raise
    except OSError as exc:
        raise refuse(
            "library-database-missing",
            f"the rekordbox database could not be captured: {exc}",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            scope=Scope.SESSION,
            detail={"root": str(destination_root), "stamp": chosen},
        ) from exc

    captured: list[CapturedSource] = []

    # What the writer took, recorded by looking at the result rather than by
    # restating its behaviour. A restore reads this list, so it has to describe
    # the directory that exists and not the directory this module intended.
    for path in database_paths(cfg):
        landed = destination / path.name
        captured.append(
            CapturedSource(
                source=path, captured=landed if landed.exists() else None, directory=False
            )
        )
    playlist_name = rb_writer.MASTER_PLAYLIST_XML
    playlist_source = config.state_path(DATABASE_KEY, cfg).parent / playlist_name
    landed_playlist = destination / playlist_name
    captured.append(
        CapturedSource(
            source=playlist_source,
            captured=landed_playlist if landed_playlist.exists() else None,
            directory=False,
        )
    )

    # The coupled half. Everything the inventory declares that the writer did not
    # already take.
    for source in declared:
        if source in already:
            continue
        target = destination / source.name
        if target.exists():
            raise refuse(
                "internal-error",
                f"two declared capture sources land on the same name inside a "
                f"capture ({target.name}), so one would overwrite the other",
                remedy=Remedy.REPORT_DEFECT,
                detail={"source": str(source), "target": str(target)},
            )
        captured.append(_copy(source, target))

    _harden(destination)

    record = Capture(
        stamp=chosen,
        root=destination,
        database=database if database.exists() else None,
        integrity_verified=False,
        sources=tuple(captured),
    )
    verdict = _verify(record.database, verifier) if record.database is not None else False
    record = Capture(
        stamp=record.stamp,
        root=record.root,
        database=record.database,
        integrity_verified=verdict,
        sources=record.sources,
    )

    manifest = destination / MANIFEST_NAME
    config.atomic_write_bytes(
        json.dumps(record.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n", manifest
    )
    return Capture(
        stamp=record.stamp,
        root=record.root,
        database=record.database,
        integrity_verified=record.integrity_verified,
        sources=record.sources,
        manifest=manifest,
    )


def read_manifest(capture_root: Path | str) -> Capture:
    """Read one capture's manifest, or refuse naming the directory.

    U32 restores from this. It is here rather than there because the writer and
    the reader of a persisted shape belong together: two modules that each know
    half of a format is how a format acquires two incompatible readings.
    """
    root = Path(capture_root)
    path = root / MANIFEST_NAME
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise refuse(
            "internal-error",
            f"{path} could not be read, so there is no record of what this "
            f"capture holds and nothing may be restored from it: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"path": str(path)},
        ) from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise refuse(
            "internal-error",
            f"{path} is not readable as JSON: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"path": str(path)},
        ) from exc
    if not isinstance(data, Mapping):
        raise refuse(
            "internal-error",
            f"{path} does not hold an object at its top level",
            remedy=Remedy.REPORT_DEFECT,
            detail={"path": str(path)},
        )
    return Capture.from_json(data, manifest=path)


def assert_verified(record: Capture) -> None:
    """The gate. Nothing commits behind a capture that did not verify.

    Stated as its own function rather than as an ``if`` at each call site so that
    there is one answer to "may this session proceed" and one message when it may
    not. A capture that failed its check is not a smaller recovery point, it is
    the absence of one, and proceeding would put the commit's only undo behind a
    file nobody has established can be opened.

    IT ASKS THE DISK AS WELL AS THE MANIFEST, and the second question is not
    redundant. ``integrity_verified`` records a verdict reached at capture time
    about bytes that existed then; a partial cloud pull, an interrupted copy or a
    hand-cleared store can take those bytes away afterwards and leave the manifest
    saying they passed. A restore that trusted the manifest alone would rehearse
    clean, clear the live write-ahead log, and only then discover the file it was
    going to put in its place is not there.
    """
    if record.verified and record.database is not None and record.database.exists():
        return
    missing = record.database is not None and not record.database.exists()
    raise refuse(
        "snapshot-integrity-failed",
        (
            f"the capture at {record.root} records a database at "
            f"{record.database} that is no longer on disk, so the manifest's "
            f"verdict is about bytes that have since gone"
            if missing
            else f"the capture at {record.root} did not pass its integrity check, "
            f"so there is no verified recovery point for this session to commit "
            f"behind"
        ),
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.SESSION,
        detail={
            "stamp": record.stamp,
            "root": str(record.root),
            "database": str(record.database) if record.database is not None else None,
            "database_present": record.database is not None and record.database.exists(),
        },
    )


def assert_sources_present(record: Capture) -> None:
    """Refuse when the manifest names captured bytes the store no longer holds.

    :func:`assert_verified` covers the database, which is the file that matters
    most. This covers the rest of the matched set, and it exists for the same
    reason: a restore is a sequence of destructive steps, and finding out half way
    through that the source of step four is gone means steps one to three have
    already happened. Everything a restore is going to read is therefore checked
    before anything it is going to write.
    """
    absent = [
        str(entry.captured)
        for entry in record.sources
        if entry.captured is not None and not entry.captured.exists()
    ]
    if not absent:
        return
    raise refuse(
        "snapshot-integrity-failed",
        f"the capture at {record.root} records "
        + (
            f"{len(absent)} file it no longer holds"
            if len(absent) == 1
            else f"{len(absent)} files it no longer holds"
        )
        + ", so restoring from it would replace part of the library and then stop:\n"
        + "\n".join(f"  - {entry}" for entry in absent[:20]),
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.SESSION,
        detail={"stamp": record.stamp, "root": str(record.root), "absent": absent[:20]},
    )


__all__ = [
    "ALLOCATION_UNIT",
    "CAPACITY_HEADROOM",
    "DATABASE_KEY",
    "DIRECTORY_ENTRY_OVERHEAD",
    "MANIFEST_NAME",
    "MANIFEST_SCHEMA_VERSION",
    "STORE_KEY",
    "Capture",
    "CapturedSource",
    "Verifier",
    "assert_room_for",
    "assert_room_for_capture",
    "assert_sources_present",
    "assert_verified",
    "capture",
    "database_paths",
    "new_stamp",
    "read_manifest",
    "restore_peak_bytes",
    "store_root",
]
