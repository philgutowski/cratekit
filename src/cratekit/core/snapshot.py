"""KTD21b: the database and the state coupled to it, captured as one matched set.

The registry, watermarks, tombstones, declines and taxonomy template describe
the database's rows, so a capture taking one half without the other is an
inconsistent recovery point. This is the layer above ``rb_writer.snapshot_db``:
the database half delegated to the writer, the coupled half copied from
``config.snapshot_sources``, one integrity verdict, one flush to the disk
before the manifest (U272), and one manifest of what was taken and what was
absent. A capture that fails its check or its flush is recorded unverified.

THE CAPTURE SET IS DERIVED AND IS NEVER LISTED HERE. A companion list beside
the inventory drifts into a database copied without its outstanding log;
``tests/test_config.py`` asserts this source spells no file suffix.

ABSENCE IS NORMAL, NOT AN ERROR, and the manifest records it, because "not
captured" and "captured empty" call for different restores.

Retention is U32's. The capacity refusals live here because this function
writes: :func:`assert_room_for_capture`, :func:`assert_room_for` (also used by
restore) and :func:`assert_room_for_check` for the check's copy (R-1677).

LAYER: infrastructure, carrying remediation TOKENS rather than user text (D2).
"""

from __future__ import annotations

import errno
import json
import logging
import os
import secrets
import shutil
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from cratekit.core import config, rb_writer
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)

#: The record inside every capture directory; without it provenance is a guess.
MANIFEST_NAME = "capture.json"

#: Bumped only on an incompatible change. A later shape is refused, not guessed.
MANIFEST_SCHEMA_VERSION = 1

#: The state entry whose path is the database, named once so the writer agrees.
DATABASE_KEY = "rekordbox_db"

#: The state entry that holds captures.
STORE_KEY = "snapshots"

#: Verifies one captured database file, a seam so tests drive both verdicts.
Verifier = Callable[[Path], bool]


def _defect(message: str, *, detail: Mapping[str, Any]) -> CratekitError:
    """A refusal that only a defect in this build or its records can reach."""
    return refuse("internal-error", message, remedy=Remedy.REPORT_DEFECT, detail=detail)


def new_stamp(now: datetime | None = None) -> str:
    """A sortable, filesystem-safe directory name for one capture.

    Sixty-four random bits, because restore derives one staging directory per
    attempt from it and same-second attempts are ordinary; at sixteen bits a
    collision overwrites an earlier attempt's log. ``cli.output.new_run_id``
    carries the same width (U235). No colon or space, since it is a directory name.
    """
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H%M%SZ')}-{secrets.token_hex(8)}"


@dataclass(frozen=True, slots=True)
class CapturedSource:
    """One declared source and what became of it.

    ``captured`` is None when the source was absent, recorded so a restore can
    tell "nothing to put back" from "never looked".
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

    ``integrity_verified`` is carried, not re-derived, because the check ran on
    the bytes just written. It is true only when the check passed and the whole
    capture was then flushed to the disk (U272).
    """

    stamp: str
    root: Path
    database: Path | None
    integrity_verified: bool
    sources: tuple[CapturedSource, ...] = ()
    manifest: Path | None = None

    @property
    def verified(self) -> bool:
        """True only when a database was captured AND it passed its check."""
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

    Derived from the inventory, the same set ``rb_writer.snapshot_db`` copies.
    """
    return (config.state_path(DATABASE_KEY, cfg), *config.sidecar_paths(DATABASE_KEY, cfg))


def captured_paths(cfg: config.Config) -> frozenset[Path]:
    """Every path a capture takes: the database fileset, the legacy playlist file, and
    everything ``config.snapshot_sources`` declares. Restore replaces exactly these.
    """
    playlist = config.state_path(DATABASE_KEY, cfg).parent / rb_writer.MASTER_PLAYLIST_XML
    return frozenset({*database_paths(cfg), *config.snapshot_sources(cfg), playlist})


def _harden(root: Path) -> None:
    """Give every file and directory under ``root`` an explicit private mode.

    Derived by walking (P3), because the copier preserves source modes and the
    database is world readable on a normal install. Skipped without POSIX modes (P1).
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
    """Best effort, because a capture with loose modes beats no capture."""
    try:
        os.chmod(path, mode)
    except OSError as exc:
        logger.debug("could not set the mode on %s: %s", path, exc)


def _refuse_if_nested(source: Path, store: Path) -> None:
    """Refuse when a declared source and the capture store contain each other.

    Rechecked at copy time (P4), because a nested store makes every capture
    contain every earlier one.
    """
    if source == store or store in source.parents or source in store.parents:
        raise _defect(
            f"the declared capture source {source} and the capture store {store} "
            f"contain one another, so a capture would nest every earlier capture "
            f"inside the new one",
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


def _raise_walk_error(error: OSError) -> None:
    """Raise what ``os.walk`` would skip, because a skipped directory is not flushed."""
    raise error


def _flush(capture_root: Path, store: Path) -> None:
    """Put everything a capture holds on the disk, deepest first, then its store.

    Derived by walking (P3). Raises the first :class:`OSError`, because the
    caller records a verdict on the strength of this returning (U272).
    """
    for current, _directories, files in os.walk(
        capture_root, topdown=False, onerror=_raise_walk_error
    ):
        here = Path(current)
        for name in files:
            config.flush_to_disk(here / name)
        config.flush_to_disk(here)
    config.flush_to_disk(store)


def _write_manifest(record: Capture, manifest: Path) -> None:
    config.atomic_write_bytes(
        json.dumps(record.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n", manifest
    )


def _record_unverified(record: Capture, manifest: Path) -> None:
    """Write the capture's manifest saying NOT verified, before any refusal of it.

    A failed write still refuses, since a capture with no manifest is unusable.
    """
    try:
        _write_manifest(replace(record, integrity_verified=False), manifest)
    except OSError as written:
        logger.warning(
            "the capture at %s could not record that it is not verified: %s", record.root, written
        )


def _not_flushed(record: Capture, manifest: Path, exc: OSError) -> CratekitError:
    """Record the capture as NOT verified, then return the refusal to raise."""
    _record_unverified(record, manifest)
    return refuse(
        "snapshot-integrity-failed",
        f"the capture at {record.root} could not be flushed to the disk ({exc}), so it "
        f"is recorded as not verified and there is no recovery point for this session "
        f"to commit behind",
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        scope=Scope.SESSION,
        detail={
            "stamp": record.stamp,
            "root": str(record.root),
            "path": str(getattr(exc, "filename", None) or ""),
            "errno": getattr(exc, "errno", None),
        },
    )


#: A file's size and modification time, or None for a directory, whose times
#: move with its entries.
_Identity = tuple[int, int] | None


def _walked(capture_root: Path) -> dict[Path, _Identity]:
    """Every file and directory under a capture, derived by walking (P3)."""
    found: dict[Path, _Identity] = {}
    for current, directories, files in os.walk(capture_root, onerror=_raise_walk_error):
        here = Path(current)
        for name in directories:
            found[here / name] = None
        for name in files:
            status = (here / name).lstat()
            found[here / name] = (status.st_size, status.st_mtime_ns)
    return found


def _changed_by_the_check(before: Mapping[Path, _Identity], capture_root: Path) -> list[str]:
    """What the check removed or rewrote of the capture it was asked about.

    THE CHECK READS, AND A CAPTURE IS WHAT WAS COPIED (R-1665). A verdict counts
    only when the copy is unchanged. Additions are ignored, being in no record,
    and a walk that cannot finish answers as a change.
    """
    try:
        after = _walked(capture_root)
    except OSError as exc:
        return [f"the capture could not be walked again: {exc}"]
    changed: list[str] = []
    for path, identity in before.items():
        if path not in after:
            changed.append(f"{path} was removed")
        elif after[path] != identity:
            changed.append(f"{path} was rewritten")
    return changed


def _verify(database: Path, verifier: Verifier | None) -> bool:
    """Run the integrity check, failing CLOSED on anything unexpected.

    Only :class:`rb_writer.IntegrityCheckCopyFailed` passes through, for
    :func:`capture` to name (R-1677).
    """
    try:
        if verifier is None:
            return bool(rb_writer.integrity_ok(database, raise_copy_failure=True))
        return bool(verifier(database))
    except rb_writer.IntegrityCheckCopyFailed:
        # No verdict at all, which the capture names (R-1677).
        raise
    except Exception as exc:  # noqa: BLE001 - a check that cannot answer has not passed
        logger.warning("the capture integrity check could not run, so it did not pass: %s", exc)
        return False


#: How much more room than the capture needs must be free before one is taken,
#: for the manifest, checkpoint growth and a filesystem never driven to zero.
CAPACITY_HEADROOM = 1.10


#: The block size floor for a file whose ``st_blocks`` is unavailable. It shows
#: only on a sparse file, where ``tests/test_snapshot.py`` pins it.
ALLOCATION_UNIT = 4096

#: What one directory entry costs beyond its blocks; see :func:`_allocated_size`.
DIRECTORY_ENTRY_OVERHEAD = 2048


def _allocated_size(path: Path, *, entry_overhead: int = DIRECTORY_ENTRY_OVERHEAD) -> int:
    """What ``path`` costs a filesystem, not what its bytes add up to.

    A tree of small documents allocates up to two orders of magnitude more than
    its apparent size, measured on the queue directories, so each entry is
    charged blocks plus :data:`DIRECTORY_ENTRY_OVERHEAD` and the estimate errs
    high. A capture and the incoming half of a restore charge the overhead;
    only :func:`freed_bytes` passes zero, because over-counting what is given
    back puts the estimate below the real peak. A missing source counts zero.
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

    ``st_blocks`` under-reports a sparse file, and the copy is not sparse.
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

    Asked of the nearest existing ancestor. None refuses in :func:`assert_room_for`.
    """
    probe = nearest_existing(root)
    if not probe.exists():
        return None
    try:
        return shutil.disk_usage(probe).free
    except OSError:
        return None


def assert_room_for_capture(
    cfg: config.Config,
    *,
    root: Path | str | None = None,
    headroom: float = CAPACITY_HEADROOM,
    free_bytes: int | None = None,
) -> int:
    """Refuse BEFORE a capture is taken when the store cannot hold one.

    Returns the estimate. A copy that runs out of room leaves a truncated
    capture to commit behind. The estimate walks what :func:`capture` copies
    (P4), in allocated bytes.
    """
    destination_root = Path(root) if root is not None else store_root(cfg)
    needed = sum(_allocated_size(source) for source in sorted(captured_paths(cfg)))
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

    Shared with restore. A filesystem that will not report its free space
    refuses, because on a supported platform silence means an unreadable path.
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


#: Steps for a throwaway copy with no room (R-1677), since freeing disk is not
#: a command this product runs.
CHECK_ROOM_STEPS: tuple[str, ...] = (
    "free space on the volume holding the temporary directory named above, or "
    "set TMPDIR (TEMP on Windows) to a directory on a volume with room, and run "
    "this again",
)

#: The operating system's answers that mean a volume had no room.
_NO_ROOM_ERRNOS = frozenset(
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
)


def nearest_existing(path: Path) -> Path:
    """``path`` or its nearest ancestor that exists, or the root when none does.

    A capacity or permission question about a path not yet made is asked of it.
    """
    probe = path
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    return probe


def _device(path: Path) -> int:
    """The device of the nearest ancestor of ``path`` that exists, as ``stat`` reads it."""
    return os.stat(nearest_existing(path)).st_dev


def _same_volume(first: Path, second: Path) -> bool:
    """Whether two paths, made or not yet made, land on one filesystem.

    Unknown counts as shared, the direction that asks for more room.
    """
    try:
        return _device(Path(first)) == _device(Path(second))
    except OSError:
        return True


def assert_room_for_check(
    database: Path | str,
    *,
    store: tuple[Path, int] | None = None,
    headroom: float = CAPACITY_HEADROOM,
    free_bytes: int | None = None,
) -> int:
    """Refuse BEFORE a capture when the integrity check's throwaway copy has no room.

    Returns the estimate. The check copies :func:`rb_writer.file_set` to the
    temporary directory (R-1665), and a full temporary volume used to read as a
    failed check (R-1677). When ``store`` shares that volume, room is asked for
    the capture and the throwaway together.
    """
    try:
        scratch = rb_writer.disposable_root()
    except OSError as exc:
        raise refuse(
            "snapshot-check-temp-full",
            f"no temporary directory could be found for the integrity check's "
            f"throwaway copy of the database ({exc}), so the check could not run",
            steps=CHECK_ROOM_STEPS,
            scope=Scope.SESSION,
            detail={"root": None, "database": str(database)},
        ) from exc
    needed = sum(_allocated_size(member) for member in rb_writer.file_set(database))
    shared = store is not None and _same_volume(scratch, store[0])
    total = needed + (store[1] if store is not None and shared else 0)
    available = free_bytes if free_bytes is not None else _free_bytes(scratch)
    required = int(total * headroom)
    detail: dict[str, Any] = {
        "root": str(scratch),
        "database": str(database),
        "required_bytes": required,
        "estimated_bytes": needed,
        "shares_volume_with": str(store[0]) if store is not None and shared else None,
    }
    if available is None:
        raise refuse(
            "snapshot-check-temp-full",
            f"the free space on the volume holding the temporary directory {scratch} "
            f"could not be read, so there is no way to know whether the integrity "
            f"check's throwaway copy of the database fits there",
            steps=(
                "check that the volume holding the temporary directory is mounted "
                "and readable, or set TMPDIR (TEMP on Windows) to one that is, and "
                "run this again",
            ),
            scope=Scope.SESSION,
            detail=detail,
        )
    if available >= required:
        return needed
    sharing = (
        f", since that volume also holds the capture store at {store[0]}, which the "
        f"capture fills first"
        if store is not None and shared
        else ""
    )
    raise refuse(
        "snapshot-check-temp-full",
        f"the temporary directory {scratch} has {available} bytes free and the "
        f"integrity check's throwaway copy of the database needs about {required} "
        f"there{sharing}; refusing before the capture rather than taking one the "
        f"check cannot verify",
        steps=CHECK_ROOM_STEPS,
        scope=Scope.SESSION,
        detail={**detail, "free_bytes": available},
    )


def check_had_no_room(
    failed: rb_writer.IntegrityCheckCopyFailed, *, origin: tuple[str, ...] = ()
) -> CratekitError | None:
    """The refusal for a throwaway copy that ran out of room, or None for any other failure.

    For a volume that filled after the measure. Only no space and a quota count;
    the database is still never recorded verified.
    """
    code = getattr(failed.error, "errno", None)
    if code not in _NO_ROOM_ERRNOS:
        return None
    where = failed.scratch if failed.scratch is not None else "the temporary directory"
    return refuse(
        "snapshot-check-temp-full",
        f"the integrity check could not run: its throwaway copy of {failed.source} "
        f"found no room in {where} ({failed.error}), so the database has no verdict "
        f"and is not recorded as verified; nothing here says it is damaged",
        steps=CHECK_ROOM_STEPS,
        scope=Scope.SESSION,
        origin=origin,
        detail={
            "root": str(where),
            "database": str(failed.source),
            "errno": code,
        },
    )


def incoming_bytes(source: Path) -> int:
    """What a copy of ``source`` will ALLOCATE, charged with the entry overhead."""
    return _allocated_size(source, entry_overhead=DIRECTORY_ENTRY_OVERHEAD)


def freed_bytes(target: Path) -> int:
    """What removing ``target`` will give back, counted conservatively.

    Charged without the entry overhead, because over-counting what is given back
    puts the estimate below the real peak. The difference is one entry, and
    ``tests/test_restore.py`` pins the exact peak.
    """
    return _allocated_size(target, entry_overhead=0)


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

    ``db`` is the caller's open handle, passed to the writer to fold the log;
    the companion copies are what hold if the fold fails. ``verifier`` and
    ``root`` are test seams, and a false verdict still blocks every commit.
    """
    destination_root = Path(root) if root is not None else store_root(cfg)
    # Before anything is created, so a refusal has done nothing.
    estimate = assert_room_for_capture(cfg, root=destination_root)
    # The real check's throwaway needs room too (R-1677); a stand in makes none.
    if verifier is None:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
    chosen = stamp or new_stamp(now)
    destination = destination_root / chosen
    if destination.exists():
        raise _defect(
            f"a capture directory already exists at {destination}; writing a "
            f"second capture into it would interleave two recovery points",
            detail={"stamp": chosen, "root": str(destination_root)},
        )

    store = store_root(cfg)
    already = set(database_paths(cfg))
    declared = config.snapshot_sources(cfg)
    for source in declared:
        _refuse_if_nested(source, store)

    # The database half, delegated to the writer.
    try:
        database = rb_writer.snapshot_db(stamp=chosen, root=destination_root, db=db, cfg=cfg)
    except OSError as exc:
        raise refuse(
            "library-database-missing",
            f"the rekordbox database could not be captured: {exc}",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            scope=Scope.SESSION,
            detail={"root": str(destination_root), "stamp": chosen},
        ) from exc

    captured: list[CapturedSource] = []

    # Recorded from the result, because a restore reads what exists.
    playlist = config.state_path(DATABASE_KEY, cfg).parent / rb_writer.MASTER_PLAYLIST_XML
    for path in (*database_paths(cfg), playlist):
        landed = destination / path.name
        captured.append(
            CapturedSource(
                source=path, captured=landed if landed.exists() else None, directory=False
            )
        )

    # The coupled half, whatever the writer did not already take.
    for source in declared:
        if source in already:
            continue
        target = destination / source.name
        if target.exists():
            raise _defect(
                f"two declared capture sources land on the same name inside a "
                f"capture ({target.name}), so one would overwrite the other",
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
    # Walked before and after the check, so the verdict is about the listed bytes (R-1665).
    try:
        copied = _walked(destination)
    except OSError as exc:
        logger.warning("the capture at %s could not be walked before its check: %s", destination, exc)
        copied = None
    manifest = destination / MANIFEST_NAME
    try:
        verdict = (
            _verify(record.database, verifier)
            if record.database is not None and copied is not None
            else False
        )
    except rb_writer.IntegrityCheckCopyFailed as failed:
        # No room for the check's copy is refused as that, unverified first (R-1677).
        no_room = check_had_no_room(failed)
        if no_room is not None:
            _record_unverified(record, manifest)
            raise no_room from failed
        logger.warning("the capture integrity check could not run, so it did not pass: %s", failed)
        verdict = False
    if verdict and copied is not None:
        changed = _changed_by_the_check(copied, destination)
        if changed:
            logger.warning(
                "the integrity check changed the capture at %s, so it is not verified: %s",
                destination,
                "; ".join(changed[:20]),
            )
            verdict = False
    record = replace(record, integrity_verified=verdict)

    # THE COPY REACHES THE DISK BEFORE THE RECORD THAT VOUCHES FOR IT (U272),
    # because the check reads through the page cache.
    try:
        _flush(destination, destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc

    _write_manifest(record, manifest)

    # The manifest's rename is a directory entry an unflushed directory loses.
    try:
        config.flush_to_disk(destination)
        config.flush_to_disk(destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc
    return replace(record, manifest=manifest)


def read_manifest(capture_root: Path | str) -> Capture:
    """Read one capture's manifest, or refuse naming the directory.

    Here beside the writer, so one module knows the format.
    """
    root = Path(capture_root)
    path = root / MANIFEST_NAME
    try:
        raw = path.read_bytes()
    except OSError as exc:
        # ``from exc`` lets the refusal answer an OS refusal with an act.
        raise _defect(
            f"{path} could not be read, so there is no record of what this "
            f"capture holds and nothing may be restored from it: {exc}",
            detail={"path": str(path)},
        ) from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _defect(
            f"{path} is not readable as JSON: {exc}",
            detail={"path": str(path)},
        ) from exc
    if not isinstance(data, Mapping):
        raise _defect(
            f"{path} does not hold an object at its top level",
            detail={"path": str(path)},
        )
    return Capture.from_json(data, manifest=path)


def assert_verified(record: Capture) -> None:
    """The gate. Nothing commits behind a capture that did not verify.

    It also asks the disk, because the database can vanish after the manifest
    recorded it as verified.
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

    Checked before a restore writes anything, so it cannot stop half way.
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

