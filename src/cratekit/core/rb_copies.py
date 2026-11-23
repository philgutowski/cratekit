"""Copies of the database: the snapshot, the disposable and read-only copies, their integrity check.

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name its callers read; read them there. A
name of the writer outside this file, and every seam a test patches, is read through
``rb_writer`` at call time so a patch on the writer bites here too (U300).
"""

from __future__ import annotations

import json
import logging
import shutil
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping

from cratekit.core import config
from cratekit.core.rb_call_time import writer as _writer

#: The writer's own logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.rb_writer")


def snapshot_db(
    db_path: Path | str | None = None,
    *,
    stamp: str,
    root: Path | str | None = None,
    db: Any = None,
    cfg: config.Config | None = None,
) -> Path:
    """Copy the database and everything it is incomplete without. Returns the copy.

    WRITE-AHEAD-LOG AWARE: a checkpoint on the caller's handle is the belt, the
    whole file-set copy (log included) the braces. IT DOES NOT PRUNE; the caller
    prunes after its commit (R30).
    """
    source = Path(db_path) if db_path is not None else _writer().live_db_path(cfg)
    destination_root = Path(root) if root is not None else _writer().snapshot_root(cfg)

    if db is not None:
        try:
            from sqlalchemy import text

            db.session.execute(text("PRAGMA wal_checkpoint(TRUNCATE)"))
        except Exception as exc:  # noqa: BLE001 - the checkpoint is the belt, not the braces
            logger.debug("snapshot checkpoint did not run, relying on the sidecar copy: %s", exc)

    destination = destination_root / stamp
    # A private directory too: a file in a world-writable one can be replaced (P1).
    config.mkdir_private(destination)
    return _writer()._copy_file_set(source, destination)


def _copy_file_set(source: Path, destination: Path) -> Path:
    """Copy a database and everything it is incomplete without into ``destination``.

    ONE LOOP FOR THE SNAPSHOT AND THE DISPOSABLE COPY, so a new sidecar reaches both (P4).
    """
    database, *companions = file_set(source)
    copied = destination / database.name
    shutil.copy2(database, copied)
    for companion in companions:
        if companion.exists():
            shutil.copy2(companion, destination / companion.name)
    return copied


def file_set(source: Path | str) -> tuple[Path, ...]:
    """The database first, then every file a copy takes along, present or not.

    Shared by the copy and the room measurement (R-1677) so they cannot drift (P4).
    """
    origin = Path(source)
    return (
        origin,
        *(origin.with_name(origin.name + suffix) for suffix in _writer().db_sidecar_suffixes()),
        origin.parent / _writer().MASTER_PLAYLIST_XML,
    )


def copy_file_set(source: Path | str, destination: Path) -> Path:
    """Copy a database's whole file set into an existing ``destination``, answering the copy (U162).

    THE CALLER ESTABLISHES THAT REKORDBOX IS CLOSED, as for :func:`disposable_copy`.
    """
    return _writer()._copy_file_set(Path(source), destination)


def disposable_root() -> Path:
    """The directory every throwaway copy is made in, asked once so the room measured is its (R-1677).

    ``tempfile`` reads ``TMPDIR``. Raises :class:`FileNotFoundError` when none is usable.
    """
    return Path(tempfile.gettempdir())


def _scratch_or_none() -> Path | None:
    try:
        return _writer().disposable_root()
    except OSError:
        return None


@contextmanager
def disposable_copy(source: Path | str) -> Iterator[Path]:
    """A throwaway copy of a database in a private temporary directory, then gone.

    THE ONE WAY A READ ONLY DIAGNOSTIC MAY REACH THE DATABASE (R-372): ``source``
    is copied as bytes, never opened. The 0700 directory (P1) is always removed.
    THE CALLER ESTABLISHES THAT REKORDBOX IS CLOSED, or the copy is torn.
    """
    origin = Path(source)
    directory = Path(tempfile.mkdtemp(prefix="cratekit-copy-", dir=_writer().disposable_root()))
    try:
        yield _writer()._copy_file_set(origin, directory)
    finally:
        shutil.rmtree(directory, ignore_errors=True)


@contextmanager
def read_only_copy(source: Path | str, *, cfg: config.Config | None = None) -> Iterator[Any]:
    """An OPEN handle on a disposable copy of ``source``, closed and removed after.

    The live path is never handed to the binding. No application pin, since a copy
    is a file; the binding and schema pins apply. REFUSES WHILE REKORDBOX OR ITS
    AGENT IS RUNNING, since the copy would be torn. A FILE THAT IS NOT A LIBRARY IS
    NAMED AS ONE (R-663): an empty copy (refused before the open) or one holding no
    canary table names the configured path under a setup remedy.
    """
    _writer().assert_rekordbox_closed("copying the database for a read only look")
    _writer().require_present(Path(source))
    with _writer().disposable_copy(source) as copied:
        refusal = None if copied.stat().st_size else _writer()._not_a_library(Path(source), copied)
        if refusal is not None:
            raise refusal
        try:
            db = _writer().open_db(copied, check_app_version=False, cfg=cfg)
        except _writer().RekordboxUnavailable as exc:
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _writer()._not_a_library(Path(source), copied)
            if refusal is None:
                raise
            raise refusal from exc
        try:
            yield db
        finally:
            _writer().close_db(db)


#: The tables the canary reads. A file holding NEITHER is not a library; holding one is drift.
CANARY_TABLES = ("agentRegistry", "djmdContent")


def _copy_tables(copied: Path) -> set[str] | None:
    """The table names in the copy's schema through the binding (for the key), or None, never empty."""
    from pyrekordbox import Rekordbox6Database
    from sqlalchemy import text

    try:
        with _writer()._binding_probe(strict=False):
            db = Rekordbox6Database(path=str(copied), unlock=_writer().unlock_needed(copied))
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
    try:
        rows = db.session.execute(text("SELECT name FROM sqlite_master WHERE type = 'table'"))
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
    finally:
        _writer().close_db(db)


def recorded_db_drives(db: Any) -> tuple[str | None, str | None]:
    """rekordbox's own record of where this database was made and where it is now (R-372).

    ``BaseDBDrive`` and ``CurrentDBDrive`` drive rekordbox's runtime path remap,
    offered by setup as a ``library.location_prefix_map`` rule. Blank is None, and
    the trailing separator is stripped since a prefix rule matches whole components.
    """
    from sqlalchemy import text

    row = db.session.execute(
        text("SELECT BaseDBDrive, CurrentDBDrive FROM djmdProperty LIMIT 1")
    ).first()
    if row is None:
        return None, None

    def _clean(value: Any) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return None
        stripped = value.strip().rstrip("/\\")
        return stripped or value.strip()

    return _clean(row[0]), _clean(row[1])


def integrity_ok(
    snapshot_database: Path | str,
    *,
    unlock: bool | None = None,
    raise_copy_failure: bool = False,
) -> bool:
    """True when a snapshot passes SQLite's own consistency check, through the writers' open path.

    No application pin, since a snapshot is a file; ``unlock`` is passed through
    unanswered. IT NEVER OPENS THE FILE IT IS GIVEN (R-1665): the last close of a
    write-ahead-log database deletes its log, which once removed files a
    capture's record lists, so the check opens a throwaway copy. A copy that
    cannot be made answers False, or with ``raise_copy_failure`` raises
    :class:`IntegrityCheckCopyFailed` (R-1677); every failure after the copy
    stays False, so a real integrity failure is never told as a copy failure.
    """
    from sqlalchemy import text

    copied = False
    try:
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = True
            try:
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
            except _writer().RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
            finally:
                # The full release: the throwaway directory is removed next.
                _writer().close_db(db)
    except OSError as exc:
        if raise_copy_failure and not copied:
            raise IntegrityCheckCopyFailed(snapshot_database, exc, _scratch_or_none()) from exc
        logger.warning(
            "the integrity check could not copy %s to check it, so it did not pass: %s",
            snapshot_database,
            exc,
        )
        return False


def restore_from_snapshot(
    snapshot_database: Path | str,
    db_path: Path | str | None = None,
    *,
    cfg: config.Config | None = None,
) -> None:
    """Put a snapshot back, write-ahead-log symmetrically.

    THE ASYMMETRY IS THE WHOLE POINT. Both LIVE sidecars are removed so no foreign
    log replays; the snapshot's log is copied back, since its transactions are
    the state; its shared-memory index is NOT, since a stale one beside a fresh
    log corrupts. Copying only the database silently reverted uncheckpointed frames.
    THE CALLER MUST HAVE RELEASED EVERY HANDLE through :func:`close_db`.
    """
    target = Path(db_path) if db_path is not None else _writer().live_db_path(cfg)
    source = Path(snapshot_database)

    _writer().assert_rekordbox_closed("restoring the database")

    for suffix in _writer().db_sidecar_suffixes():
        live_sidecar = target.with_name(target.name + suffix)
        if live_sidecar.exists():
            live_sidecar.unlink()

    shutil.copy2(source, target)
    for suffix in _writer().restored_sidecar_suffixes():
        snapshot_sidecar = source.with_name(source.name + suffix)
        if snapshot_sidecar.exists():
            shutil.copy2(snapshot_sidecar, target.with_name(target.name + suffix))

    playlist_xml = source.parent / _writer().MASTER_PLAYLIST_XML
    if playlist_xml.exists():
        shutil.copy2(playlist_xml, target.parent / _writer().MASTER_PLAYLIST_XML)


@dataclass(frozen=True, slots=True)
class RunStateVocabulary:
    """What the run-state store calls the fields this scan reads.

    A PARAMETER RATHER THAN A LITERAL: three typed literals were all wrong, and
    nothing was ever protected. ``core.session`` publishes its own instance (U8),
    and a guard writes a REAL session record and asserts the scan protects it.
    """

    state_key: str = "state"
    terminal_states: frozenset[str] = frozenset({"closed", "abandoned"})
    snapshot_key: str = "snapshot_path"


def read_run_state_records(run_state_dir: Path) -> list[Mapping[str, Any]]:
    """Every run-state record in one directory, one level deep, skipping anything unreadable.

    Any ``.json`` name counts, so this module never encodes another module's filename.
    """
    records: list[Mapping[str, Any]] = []
    try:
        entries = sorted(run_state_dir.glob("*.json"))
    except OSError:
        return records
    for entry in entries:
        try:
            parsed = json.loads(entry.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(parsed, Mapping):
            records.append(parsed)
    return records


def default_protected_snapshot_paths(
    cfg: config.Config | None = None,
    *,
    vocabulary: RunStateVocabulary | None = None,
    records: Iterable[Mapping[str, Any]] | None = None,
) -> set[Path]:
    """Snapshot paths an OPEN run still references, which pruning must never delete (R30).

    All parameters optional, so it stays the zero-argument provider and is drivable from a test.
    """
    vocab = vocabulary or RunStateVocabulary()
    if records is None:
        resolved = _writer()._loaded_config(cfg)
        if resolved is None:
            return set()
        records = read_run_state_records(config.state_path("session_log", resolved))

    protected: set[Path] = set()
    for record in records:
        state = str(record.get(vocab.state_key, "")).lower()
        if state in vocab.terminal_states:
            continue  # a finished run releases its snapshot
        recorded = record.get(vocab.snapshot_key)
        if not recorded:
            continue
        try:
            protected.add(Path(str(recorded)).resolve())
        except (OSError, ValueError):
            continue
    return protected


def snapshot_database_in(directory: Path) -> Path | None:
    """The database file inside a snapshot directory, by shape since its name is the user's, or None."""
    return next((found for found in sorted(directory.glob("*.db")) if found.is_file()), None)


def prune_snapshots(
    root: Path | str | None = None,
    *,
    keep: int = 5,
    protected_provider: Callable[[], set[Path]] | None = default_protected_snapshot_paths,
    cfg: config.Config | None = None,
) -> list[Path]:
    """Delete all but the newest ``keep`` snapshots, sparing any an open run holds.

    ``protected_provider`` None means no protection, for retention tests only. A
    PROVIDER THAT RAISES DELETES NOTHING. A protected path may be the directory or
    the database file inside it.
    """
    destination_root = Path(root) if root is not None else _writer().snapshot_root(cfg)
    if not destination_root.is_dir() or keep < 1:
        return []

    provider = protected_provider
    if provider is default_protected_snapshot_paths:
        # The CALLER's configuration, so the prune and the snapshot root agree.
        provider = partial(default_protected_snapshot_paths, cfg)

    try:
        protected = provider() if provider else set()
    except Exception as exc:  # noqa: BLE001 - a provider failure must not delete a recovery point
        logger.warning(
            "the protected-snapshot provider failed, so every snapshot is kept this run: %s",
            exc,
        )
        return []

    snapshots = sorted(
        (
            directory
            for directory in destination_root.iterdir()
            if directory.is_dir() and snapshot_database_in(directory) is not None
        ),
        key=lambda directory: directory.stat().st_mtime,
        reverse=True,
    )

    pruned: list[Path] = []
    for directory in snapshots[keep:]:
        database = snapshot_database_in(directory)
        if directory.resolve() in protected or (
            database is not None and database.resolve() in protected
        ):
            logger.info("keeping snapshot %s: an open run still references it", directory.name)
            continue
        shutil.rmtree(directory)
        pruned.append(directory)
        logger.info("pruned snapshot %s, keeping the newest %d", directory.name, keep)
    return pruned


class IntegrityCheckCopyFailed(Exception):
    """The throwaway copy the integrity check reads could not be made (R-1677).

    NO VERDICT, WHICH IS NOT A FAILED ONE (R-1665). Raised only with
    ``raise_copy_failure``; ``scratch`` is the intended directory, or None.
    """

    def __init__(self, source: Path | str, error: OSError, scratch: Path | None = None) -> None:
        self.source = Path(source)
        self.error = error
        self.scratch = scratch
        super().__init__(
            f"the integrity check's throwaway copy of {self.source} could not be made "
            f"in {scratch if scratch is not None else 'any temporary directory'}: {error}"
        )
