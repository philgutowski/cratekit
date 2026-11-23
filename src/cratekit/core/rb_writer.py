"""The guarded rekordbox database writer: the chain of refusals between automation and the library.

pyrekordbox has no version gating, write-ahead-log handling or locking, so every
link here is load-bearing. In firing order:

1. **Three version pins**: binding, database schema, rekordbox application. Drift
   refuses, because an update can rotate the key or migrate the schema.
2. **The two-process refusal**, application AND background agent, at open and at
   commit. The agent mutates the library through cloud sync with the app closed.
3. **The cloud-sync canary.** An active sync is a writer we cannot serialise against.
4. **A write-ahead-log-aware snapshot** with a symmetric restore, verified before
   anything commits behind it.
5. **The additive whitelist.** CREATE only in named playlist and tag tables, MODIFY
   only REGISTERED columns, DELETE nothing, so grid and analysis data is
   structurally unwritable (R17). Three exceptions, each only by a commit that
   names its table: a membership soft delete (R-758, :data:`REMOVABLE_TABLES`), a
   content row carrying only file facts with every analysis column asserted
   empty (R-746, :data:`ADMITTABLE_ROW_TABLES`), and Remove from Collection,
   proven from SQL to reach nothing but the renumbered ``TrackNo`` after it
   (U288, R-1830, :data:`DELETABLE_TABLES`, :func:`renumbered_positions`).
6. **A cross-process write-session lock**, held from snapshot through smoke test.

Every path is a late-bound accessor, an unset application pin refuses (S2),
pruning is a separate step after the commit (R30), and the writable column set
is registered per operation rather than maximal (R14).

LAYER: infrastructure. It carries remediation TOKENS, never user text (D2).
"""

from __future__ import annotations

import logging
import os
import shutil  # noqa: F401 - read as rb_writer.shutil where a test patches a copy
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Scope, name_the_database, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.rb_changes import Decision as Decision
from cratekit.core.rb_changes import _registry_changes as _registry_changes
from cratekit.core.rb_changes import _registry_created_instances as _registry_created_instances
from cratekit.core.rb_changes import _table_of as _table_of
from cratekit.core.rb_changes import (
    clear_registry_buffer,
    guard_violations,
    pending_changes,
    pending_objects,
)
from cratekit.core.rb_changes import metadata_decision as metadata_decision
from cratekit.core.rb_changes import write_metadata_field as write_metadata_field
from cratekit.core.rb_copies import CANARY_TABLES as CANARY_TABLES
from cratekit.core.rb_copies import IntegrityCheckCopyFailed as IntegrityCheckCopyFailed
from cratekit.core.rb_copies import RunStateVocabulary as RunStateVocabulary
from cratekit.core.rb_copies import _copy_file_set as _copy_file_set
from cratekit.core.rb_copies import _copy_tables as _copy_tables
from cratekit.core.rb_copies import copy_file_set as copy_file_set
from cratekit.core.rb_copies import (
    default_protected_snapshot_paths as default_protected_snapshot_paths,
)
from cratekit.core.rb_copies import disposable_copy as disposable_copy
from cratekit.core.rb_copies import disposable_root as disposable_root
from cratekit.core.rb_copies import file_set as file_set
from cratekit.core.rb_copies import integrity_ok as integrity_ok
from cratekit.core.rb_copies import prune_snapshots as prune_snapshots
from cratekit.core.rb_copies import read_only_copy as read_only_copy
from cratekit.core.rb_copies import recorded_db_drives as recorded_db_drives
from cratekit.core.rb_copies import restore_from_snapshot as restore_from_snapshot
from cratekit.core.rb_copies import snapshot_database_in as snapshot_database_in
from cratekit.core.rb_copies import snapshot_db as snapshot_db
from cratekit.core.rb_nodes import NodeTables as NodeTables
from cratekit.core.rb_nodes import add_membership as add_membership
from cratekit.core.rb_nodes import add_memberships as add_memberships
from cratekit.core.rb_nodes import add_my_tag as add_my_tag
from cratekit.core.rb_nodes import assert_node_changes_confined as assert_node_changes_confined
from cratekit.core.rb_nodes import ensure_folder as ensure_folder
from cratekit.core.rb_nodes import ensure_my_tag_value as ensure_my_tag_value
from cratekit.core.rb_nodes import ensure_playlist as ensure_playlist
from cratekit.core.rb_nodes import is_folder as is_folder
from cratekit.core.rb_nodes import move_playlist_node as move_playlist_node
from cratekit.core.rb_nodes import my_tag_writable as my_tag_writable
from cratekit.core.rb_nodes import node_change_violations as node_change_violations
from cratekit.core.rb_nodes import node_tables as node_tables
from cratekit.core.rb_nodes import remove_memberships as remove_memberships
from cratekit.core.rb_nodes import remove_playlist_node as remove_playlist_node
from cratekit.core.rb_nodes import top_level_folders as top_level_folders
from cratekit.core.rb_probes import _PROCESS_PROBES as _PROCESS_PROBES
from cratekit.core.rb_probes import LIBRARY_SYNC_SETTING as LIBRARY_SYNC_SETTING
from cratekit.core.rb_probes import SETTINGS_APP_DIRNAME as SETTINGS_APP_DIRNAME
from cratekit.core.rb_probes import TEST_SETTINGS_ENV as TEST_SETTINGS_ENV
from cratekit.core.rb_probes import (
    CloudSyncState,
    cloud_sync_active,
    cloud_sync_state,
    read_installed_app_version,
    rekordbox_processes_running,
)
from cratekit.core.rb_probes import _binding_probe as _binding_probe
from cratekit.core.rb_probes import _no_autoflush as _no_autoflush
from cratekit.core.rb_probes import read_rekordbox_settings as read_rekordbox_settings
from cratekit.core.rb_probes import rekordbox_agent_running as rekordbox_agent_running
from cratekit.core.rb_probes import rekordbox_running as rekordbox_running
from cratekit.core.rb_removal import (
    DatabaseReading,
    _mapped,
    assert_collection_removal_confined,
    collection_removal_violations,
    content_references,
    database_id,
    database_reading,
    recorded_columns,
    removal_renumbering,
    remove_from_collection,
    renumber_memberships,
)
from cratekit.core.rb_removal import renumbered_positions as renumbered_positions
from cratekit.core.rb_tables import _REGISTERED as _REGISTERED
from cratekit.core.rb_tables import ADMITTABLE_ROW_TABLES as ADMITTABLE_ROW_TABLES
from cratekit.core.rb_tables import ALBUM_TABLE as ALBUM_TABLE
from cratekit.core.rb_tables import ARTIST_TABLE as ARTIST_TABLE
from cratekit.core.rb_tables import BINDING_ID_LIMIT as BINDING_ID_LIMIT
from cratekit.core.rb_tables import COLLECTION_REMOVAL_TABLES as COLLECTION_REMOVAL_TABLES
from cratekit.core.rb_tables import (
    CONTENT_ANALYSIS_TABLES,
    CONTENT_ROW_EMPTY_COLUMNS,
    CONTENT_TABLE,
    DELETABLE_TABLES,
    EMPTY_ON_CREATE,
    GRIDLESS_ON_CREATE_COLUMNS,
    RECORDED_REMOVALS_KEY,
    ROOT_PARENT_SENTINELS,
)
from cratekit.core.rb_tables import CONTENT_LINK_COLUMN as CONTENT_LINK_COLUMN
from cratekit.core.rb_tables import CONTENT_ROW_DEFAULTS as CONTENT_ROW_DEFAULTS
from cratekit.core.rb_tables import FIELD_EMPTIES as FIELD_EMPTIES
from cratekit.core.rb_tables import FILE_ID_COLUMN as FILE_ID_COLUMN
from cratekit.core.rb_tables import FILE_ID_POLICY as FILE_ID_POLICY
from cratekit.core.rb_tables import FOLDER_PATH_COLUMN as FOLDER_PATH_COLUMN
from cratekit.core.rb_tables import GENRE_TABLE as GENRE_TABLE
from cratekit.core.rb_tables import ISRC_COLUMN as ISRC_COLUMN
from cratekit.core.rb_tables import LOCAL_UPDATE_COUNT as LOCAL_UPDATE_COUNT
from cratekit.core.rb_tables import LOOKUP_TABLES as LOOKUP_TABLES
from cratekit.core.rb_tables import MEMBERSHIP_TABLE as MEMBERSHIP_TABLE
from cratekit.core.rb_tables import MOVED as MOVED
from cratekit.core.rb_tables import PERMITTED_ROW_TABLES as PERMITTED_ROW_TABLES
from cratekit.core.rb_tables import PLAYLIST_TABLE as PLAYLIST_TABLE
from cratekit.core.rb_tables import RECORDED_COLUMNS as RECORDED_COLUMNS
from cratekit.core.rb_tables import REMOVABLE_TABLES as REMOVABLE_TABLES
from cratekit.core.rb_tables import ROW_DEFAULTS_POLICY as ROW_DEFAULTS_POLICY
from cratekit.core.rb_tables import ROW_PROBE_COLUMNS as ROW_PROBE_COLUMNS
from cratekit.core.rb_tables import ROW_PROBE_OWNER as ROW_PROBE_OWNER
from cratekit.core.rb_tables import SHELVE_POLICY as SHELVE_POLICY
from cratekit.core.rb_tables import TRACK_COLOR_POLICY as TRACK_COLOR_POLICY
from cratekit.core.rb_tables import UNINSPECTABLE as UNINSPECTABLE
from cratekit.core.rb_tables import FieldPolicy as FieldPolicy
from cratekit.core.rb_tables import Ownership as Ownership
from cratekit.core.rb_tables import content_writable_columns as content_writable_columns
from cratekit.core.rb_tables import field_policies_for_commit as field_policies_for_commit
from cratekit.core.rb_tables import register_field_policy as register_field_policy
from cratekit.core.rb_tables import registered_field_policies as registered_field_policies
from cratekit.core.rb_tables import reset_field_policies as reset_field_policies
from cratekit.core.rb_tables import row_probe_policy as row_probe_policy

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Refusals. Two types because callers discriminate: a snapshot integrity probe
# swallows an unavailable database but must NOT swallow a running application.
# Both carry a structured cause (KTD25).
# ---------------------------------------------------------------------------


class RekordboxUnavailable(CratekitError):
    """The database cannot be opened, fails a canary or a guard, or a precondition refuses."""


class RekordboxRunning(CratekitError):
    """The rekordbox application or its background agent is running and a write was requested."""


def _cause(reason: str, message: str, *, scope: Scope = Scope.SESSION, **kwargs: Any) -> Cause:
    """Build one cause through ``cause.refuse``, so the closed reason registry applies in one place."""
    return refuse(reason, message, scope=scope, **kwargs).cause


def _unavailable(reason: str, message: str, **kwargs: Any) -> RekordboxUnavailable:
    return RekordboxUnavailable(_cause(reason, message, **kwargs))


def _running(message: str, **kwargs: Any) -> RekordboxRunning:
    return RekordboxRunning(_cause("rekordbox-running", message, **kwargs))


# ---------------------------------------------------------------------------
# Configuration accessors, all late-bound: nothing resolves at import.
# ---------------------------------------------------------------------------

#: The environment variable pointing at a disposable database for the integration suite.
TEST_DB_ENV = "CRATEKIT_TEST_DB"

#: rekordbox's own legacy playlist file beside the database. Not Cratekit state, but it
#: travels through snapshot and restore because pyrekordbox reconciles against it on commit.
MASTER_PLAYLIST_XML = "masterPlaylists6.xml"

def db_sidecar_suffixes() -> tuple[str, ...]:
    """Every suffix a SQLite file travels with, DERIVED from the state schema (P4).

    A hand list would drift, and a capture would silently miss the log's transactions.
    """
    return tuple(sidecar.suffix for sidecar in config.SQLITE_SIDECARS)


def restored_sidecar_suffixes() -> tuple[str, ...]:
    """The subset a RESTORE writes back: a stale shared-memory index beside a fresh log corrupts."""
    return tuple(sidecar.suffix for sidecar in config.SQLITE_SIDECARS if sidecar.restored)


def _loaded_config(cfg: config.Config | None) -> config.Config | None:
    """The effective configuration, or None when this machine has none usable.

    None is not a pass: callers treat it as no recorded decisions, so the app pin
    refuses (S2). Errors are absorbed so the refusal arrives in the writer's vocabulary.
    """
    if cfg is not None:
        return cfg
    try:
        return config.load()
    except config.ConfigError as exc:
        logger.debug("no usable configuration for the guarded writer: %s", exc)
        return None


def _pins(cfg: config.Config | None = None) -> config.RekordboxConfig:
    """The three pins as configured, else schema defaults.

    Pins 1 and 2 are facts about the shipped build; pin 3 is about the user's
    machine and has no default (S2).
    """
    loaded = _loaded_config(cfg)
    return config.RekordboxConfig() if loaded is None else loaded.rekordbox


def pinned_pyrekordbox(cfg: config.Config | None = None) -> str:
    """The binding version this build is validated against."""
    return _pins(cfg).pinned_pyrekordbox


def pinned_db_version(cfg: config.Config | None = None) -> str:
    """The database schema version this build is validated against."""
    return _pins(cfg).pinned_db_version


def pinned_app_version(cfg: config.Config | None = None) -> str | None:
    """The recorded rekordbox application pin, or None, which refuses."""
    return _pins(cfg).pinned_app_version


def pin_validated_on(cfg: config.Config | None = None) -> str | None:
    """The date the recorded pin was confirmed against a real write, so a stale pin shows."""
    return _pins(cfg).validated_on


def live_db_path(cfg: config.Config | None = None) -> Path:
    """The configured rekordbox database. No default: one person's disk in code (R1, AE10)."""
    return config.state_path("rekordbox_db", cfg if cfg is not None else config.load())


def snapshot_root(cfg: config.Config | None = None) -> Path:
    """Where snapshots live: beside the library, and outside the coupled set to avoid nesting."""
    return config.state_path("snapshots", cfg if cfg is not None else config.load())


def write_lock_path(cfg: config.Config | None = None) -> Path:
    """The cross-process write-session lock, beside the library so every installation shares it (R31)."""
    return config.state_path("write_lock", cfg if cfg is not None else config.load())


#: The first bytes of an UNencrypted SQLite file. A real rekordbox 6 database is encrypted.
SQLITE_HEADER = b"SQLite format 3"


def unlock_needed(path: Path | str) -> bool:
    """True when the file at ``path`` is encrypted, so the binding needs the key.

    ASKED OF THE BYTES RATHER THAN ASSUMED: either constant answer fails somewhere,
    and no caller in ``src`` names one (R-239). An unreadable file answers True, so
    the open fails with the database's own refusal. Only the header is read.
    """
    try:
        with Path(path).open("rb") as handle:
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
    except OSError:
        return True


def close_db(db: Any) -> None:
    """Release a database handle COMPLETELY: the session AND the connection pool.

    The binding's close leaves the pooled connection holding the file, log and
    index, so a later restore underneath it gives the next reader an I/O error on
    an intact database. Tolerates a half-closed handle, since recovery unwinds.
    """
    try:
        if getattr(db, "session", None) is not None:
            db.close()
    finally:
        engine = getattr(db, "engine", None)
        if engine is not None:
            engine.dispose()


def integration_db_path() -> Path | None:
    """A disposable database for the integration suite, or None. Never the configured library."""
    raw = os.environ.get(TEST_DB_ENV)
    return Path(raw) if raw else None


# ---------------------------------------------------------------------------
# Pin 1: the installed binding
# ---------------------------------------------------------------------------


def assert_binding_version(cfg: config.Config | None = None) -> None:
    """Refuse unless the installed binding is exactly the validated version, on every open.

    No escape: the binding maps table shapes, and a mis-mapped read feeds the write after it.
    """
    import pyrekordbox

    pin = pinned_pyrekordbox(cfg)
    found = getattr(pyrekordbox, "__version__", "unknown")
    if found != pin:
        raise _unavailable(
            "pyrekordbox-pin-drift",
            f"the installed rekordbox binding is {found!r} and this build is "
            f"validated only against {pin!r}; re-validate against a snapshot "
            f"copy before moving the pin",
            detail={"installed": found, "pinned": pin},
        )


# ---------------------------------------------------------------------------
# Pin 2: the database's own schema version
# ---------------------------------------------------------------------------


def db_schema_version(db: Any) -> str | None:
    """The schema version the database stores, or None when it holds no property row.

    One reader for the pin and the fingerprint. IT DOES NOT CATCH: an unreadable
    table is evidence of a migration, unlike a missing row, and each caller
    attaches its own remedy.
    """
    from pyrekordbox.db6 import tables

    row = db.session.query(tables.DjmdProperty).first()
    return None if row is None else str(row.DBVersion)


def assert_schema_version(
    db: Any, *, force: bool = False, cfg: config.Config | None = None
) -> None:
    """Refuse when the stored schema version drifts from the pin, inside :func:`open_db`.

    An unreadable property table refuses too, as evidence of a migration. Folded
    into the open chain so no caller can forget it. ``force`` warns and continues;
    its flag belongs to the command-line layer (D2).
    """
    pin = pinned_db_version(cfg)
    try:
        found = db_schema_version(db)
    except Exception as exc:  # noqa: BLE001 - an unreadable property table IS drift
        raise _unavailable(
            "db-schema-pin-drift",
            f"the database schema version could not be read, which is itself "
            f"evidence of a migrated schema: {exc}",
            detail={"pinned": pin},
        ) from exc
    if found == pin:
        return
    message = (
        f"the database schema version is {found!r} and this build is validated "
        f"against {pin!r}; a rekordbox upgrade has most likely migrated the "
        f"schema, so re-run the validation checklist against a snapshot copy "
        f"before moving the pin"
    )
    if force:
        logger.warning("proceeding past a schema pin refusal by explicit request: %s", message)
        return
    raise _unavailable("db-schema-pin-drift", message, detail={"found": found, "pinned": pin})


# ---------------------------------------------------------------------------
# Pin 3: the installed application, two platform probes behind one accessor (R1).
# ---------------------------------------------------------------------------


def assert_app_version(*, force: bool = False, cfg: config.Config | None = None) -> None:
    """Refuse when the installed application drifts from the recorded pin.

    Refuses: a located version not EXACTLY the pin, and any located version when
    no pin was recorded. Warns and continues when the application cannot be found.
    When: inside :func:`open_db` on a write-intent open.

    EXACT, because the schema pin cannot see a point release and key extraction
    has broken across one. AN UNRECORDED PIN REFUSES (S2): a copied pin refuses
    nothing. A MISSING APPLICATION ONLY WARNS: it cannot hold the database open,
    though only the schema pin then guards, which the health check reports. The
    configuration error is re-raised as this module's type so one condition has
    one identity. The configuration is resolved once (P2, KTD9).
    """
    loaded = _loaded_config(cfg)
    found = read_installed_app_version(cfg=loaded)

    def detail(pin: str | None) -> dict[str, Any]:
        return {"installed": found, "pinned": pin, "validated_on": pin_validated_on(loaded)}

    if found is None:
        logger.warning(
            "the rekordbox application could not be located, so its version pin cannot "
            "be checked; only the database schema pin guards this session"
        )
        return

    if loaded is not None:
        try:
            loaded.assert_rekordbox_pin_recorded()
        except config.ConfigError as exc:
            raise _unavailable(
                "app-version-pin-unrecorded",
                f"the installed rekordbox application is version {found!r} and no "
                f"pin has ever been recorded for this machine, so there is nothing "
                f"to validate the write against: {exc}",
                remedy=Remedy.RECORD_REKORDBOX_PIN,
                detail={**detail(None), "config_error": type(exc).__name__},
            ) from exc

    pin = pinned_app_version(loaded)
    if found == pin:
        return

    message = (
        f"the installed rekordbox application is version {found!r} and the "
        f"recorded pin is {pin!r}; a rekordbox update can rotate the database "
        f"key or migrate the schema, so re-validate against a snapshot copy and "
        f"record the new pin with the date it was confirmed"
    )
    if force:
        logger.warning(
            "proceeding past an application pin refusal by explicit request: %s", message
        )
        return

    if not pin:
        # The configless machine: same slug and remedy as the unrecorded pin above,
        # so "you never pinned one" exits the same either way.
        raise _unavailable(
            "app-version-pin-unrecorded",
            message,
            remedy=Remedy.RECORD_REKORDBOX_PIN,
            detail=detail(pin),
        )
    raise _unavailable("app-version-pin-drift", message, detail=detail(pin))


# ---------------------------------------------------------------------------
# The two-process refusal, at three sites: open, commit, and restore, because
# restore replaces the file underneath whatever has it open.
# ---------------------------------------------------------------------------


def assert_rekordbox_closed(what: str) -> None:
    """Refuse while either rekordbox process is up; ``what`` names the refused operation."""
    running = rekordbox_processes_running()
    if running:
        raise _running(
            f"{running} is running, so {what} is refused; quit the application "
            f"and let the background agent settle before retrying",
            detail={"processes": running},
        )


# ---------------------------------------------------------------------------
# The cloud-sync canary
# ---------------------------------------------------------------------------


def assert_cloud_sync_readable(db: Any = None, *, force: bool = False) -> None:
    """Refuse a WRITE when the cloud-sync state cannot be determined.

    Unknown is a concurrent writer we cannot rule out, so it fails closed, naming
    the file and the error. WRITE intent only, so a read-only open still works on a
    machine with no settings. Its own slug, since "it is on" and "cannot tell" have
    opposite remedies (S4). ``force`` is a boolean and nothing else (D2).
    """
    if force:
        return
    verdict = cloud_sync_state(db)
    if verdict.state is not CloudSyncState.UNKNOWN:
        return
    raise _unavailable(
        "cloud-sync-unreadable",
        f"Cloud Library Sync could not be read, so a concurrent writer cannot be "
        f"ruled out and this write is refused: {verdict.reason}",
        # The token says a person must answer; the sentence says what to look at.
        remedy=Remedy.ANSWER_DECISION,
        steps=(
            "confirm Cloud Library Sync is switched off in rekordbox, which "
            "writes the setting this check reads",
        ),
        detail={"state": str(verdict.state), "evidence": verdict.reason},
    )


# ---------------------------------------------------------------------------
# Opening, and the generic canary
# ---------------------------------------------------------------------------


def handle_path(db: Any) -> str | None:
    """The database file an OPEN HANDLE is reading, from its engine URL, or None rather than a guess."""
    database = getattr(getattr(db, "engine", None), "url", None)
    spelled = getattr(database, "database", None)
    return str(spelled) if spelled else None


def canary(
    db: Any,
    *,
    write_intent: bool = False,
    force_cloud_canary: bool = False,
    path: Path | str | None = None,
) -> None:
    """Cheap reads that fail fast on key or schema drift, plus the cloud refusal.

    THE FILE IS NAMED ON THE FAILURE. This slug's default remedy is
    ``restore-from-snapshot``, which destroys data over a ``chmod 000``, and that
    is exactly what fails here as a bare driver error. The path makes it
    classifiable: ``path`` from the caller, else the handle's engine URL.
    """
    try:
        db.get_local_usn()
        db.get_content().first()
    except Exception as exc:  # noqa: BLE001 - any read failure means incompatible
        named = path if path is not None else handle_path(db)
        if named is not None:
            name_the_database(exc, named)
        where = f" at {named}" if named is not None else ""
        raise _unavailable(
            "canary-read-failed",
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
            detail={"path": str(named)} if named is not None else None,
        ) from exc

    if cloud_sync_active(db):
        raise _unavailable(
            "cloud-sync-active",
            f"Cloud Library Sync appears active, so a cloud agent may be mutating "
            f"the database concurrently: {cloud_sync_state(db).reason}",
        )
    if write_intent:
        assert_cloud_sync_readable(db, force=force_cloud_canary)


def require_present(target: Path) -> None:
    """Refuse a database path whose directory or file is absent, by the open's own causes.

    Shared with ``read_only_copy``, whose copy otherwise escaped as a raw ``FileNotFoundError``.
    """
    if not target.parent.exists():
        raise _unavailable(
            "library-directory-missing",
            f"the directory holding the rekordbox database does not exist: "
            f"{target.parent}; the library volume is most likely not mounted",
            detail={"directory": str(target.parent)},
        )
    if not target.exists():
        raise _unavailable(
            "library-database-missing",
            f"there is no rekordbox database at {target}",
            detail={"path": str(target)},
        )


def open_db(
    path: Path | str | None = None,
    *,
    require_closed: bool = False,
    check_app_version: bool = True,
    force_schema: bool = False,
    force_cloud_canary: bool = False,
    unlock: bool | None = None,
    cfg: config.Config | None = None,
) -> Any:
    """Open the rekordbox database behind the full open-side gate.

    THE ORDER OF THE CHECKS IS LOAD-BEARING:

    1. the parent directory, so an unmounted volume is named as one;
    2. the file itself;
    3. write intent only: the two-process refusal, then the application pin,
       before anything opens;
    4. the binding pin, unconditionally;
    5. the open itself, with any failure wrapped;
    6. the canary, then the schema pin.

    ``require_closed`` is the write-intent flag; the commit-side check is the
    real backstop. ``unlock`` is asked of the file unless a caller (only the
    integration suite) names it.
    """
    target = Path(path) if path is not None else live_db_path(cfg)

    require_present(target)

    if require_closed:
        assert_rekordbox_closed("opening the database for writing")
        if check_app_version:
            assert_app_version(cfg=cfg)

    assert_binding_version(cfg)

    from pyrekordbox import Rekordbox6Database

    # U285: a stamp the binding cannot place in local time reads as a bound.
    from cratekit.core import rb_dates

    rb_dates.install()

    if unlock is None:
        unlock = unlock_needed(target)

    try:
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(target), unlock=unlock)
    except Exception as exc:  # noqa: BLE001 - every open failure is one refusal
        # Kills nothing today (recorded in the mutation table), kept because this
        # slug shares the canary's ``restore-from-snapshot`` default.
        name_the_database(exc, target)
        raise _unavailable(
            "database-open-failed",
            f"the rekordbox database at {target} could not be opened: {exc}",
            detail={"path": str(target)},
        ) from exc

    clear_registry_buffer()

    canary(
        db,
        write_intent=require_closed,
        force_cloud_canary=force_cloud_canary,
        path=target,
    )
    assert_schema_version(db, force=force_schema, cfg=cfg)
    # U185: another app's top-level folder, remembered so a commit changing it is refused.
    from cratekit.core import foreign_tree

    foreign_tree.remember(db)
    return db


class SharedRead:
    """ONE READ HANDLE FOR A READ ONLY REPORT, opened at its first read (U267).

    LAZY, AND A FAILED OPEN IS NOT KEPT: each reader opens or refuses on its own
    merits through :func:`open_db` with read intent. EACH READER RELEASES IT, and
    a release empties the identity map so no reader takes a stale row; a read
    holds no lock. NEVER A WRITE HANDLE, and not a process-wide cache.
    :meth:`close` disposes it once; asking after the close is a defect.
    """

    def __init__(self, cfg: config.Config | None = None) -> None:
        self._cfg = cfg
        self._db: Any = None
        self._closed = False

    def handle(self) -> Any:
        """The one read handle, opened at the first call and answered after."""
        if self._closed:
            raise _defect("a read handle was asked of a shared read that was already closed")
        if self._db is None:
            self._db = open_db(
                live_db_path(self._cfg),
                require_closed=False,
                check_app_version=False,
                cfg=self._cfg,
            )
        return self._db

    def release(self, db: Any) -> None:
        """End one reader's read: the handle stays open and forgets every row it loaded."""
        if db is not self._db:
            raise _defect("a handle that is not the shared read's own was released through it")
        db.session.expunge_all()

    def close(self) -> None:
        """Close the handle once; a second close, or one with nothing opened, does nothing."""
        self._closed = True
        db, self._db = self._db, None
        if db is not None:
            close_db(db)


def _defect(message: str) -> CratekitError:
    return refuse(
        "internal-error",
        message,
        remedy=Remedy.REPORT_DEFECT,
        origin=("rb_writer", "shared_read"),
    )


def done_reading(db: Any, shared: SharedRead | None) -> None:
    """End a reader's use of ``db``: close it when it was the reader's own, release it when shared."""
    if shared is None:
        close_db(db)
    else:
        shared.release(db)


def _not_a_library(source: Path, copied: Path) -> RekordboxUnavailable | None:
    """The refusal for a copy that is empty or holds no canary table, else None (the canary's own)."""
    size = copied.stat().st_size
    if size:
        tables = _copy_tables(copied)
        if tables is None or tables.intersection(CANARY_TABLES):
            return None
        what = f"is {size} bytes and holds none of the tables a rekordbox library keeps"
    else:
        what = "is empty, 0 bytes"
    return _unavailable(
        "library-database-not-rekordbox",
        f"the file configured as the rekordbox database, {source}, {what}, so it "
        f"is not a rekordbox library; read off a copy, the file itself was not opened",
        remedy=Remedy.RUN_SETUP,
        steps=(
            "run setup again with --db-path naming the master.db rekordbox itself "
            "opens; a search for master.db can find more than one file, and the "
            "one to give is the one that is not empty",
        ),
        detail={"path": str(source), "size": size, "tables_read": list(CANARY_TABLES)},
    )


# ---------------------------------------------------------------------------
# The soft-delete marker, read here and nowhere else in the writer (R-758)
# ---------------------------------------------------------------------------


#: What "the row could not answer" looks like, distinct from every marker value.
_MARKER_ABSENT = object()


def soft_deleted(
    row: Any,
    *,
    message: str,
    origin: Sequence[str],
    detail: Mapping[str, Any],
) -> bool:
    """Read rekordbox's soft delete marker off one mapped row, or REFUSE.

    THE ONE READ OF THE MARKER FOR EVERY ROW KIND (R-758); callers supply only the
    words. A ROW THAT CANNOT SAY REFUSES, missing or ``None``, since every default
    is the permissive "live". :func:`removal_renumbering` refuses the same (R-1830).
    """
    marker = getattr(row, SOFT_DELETE_COLUMN, _MARKER_ABSENT)
    if marker is _MARKER_ABSENT or marker is None:
        raise refuse(
            "soft-delete-marker-unreadable",
            message,
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=tuple(origin),
            detail={**detail, "column": SOFT_DELETE_COLUMN},
        )
    return bool(marker)


def _row_removed(row: Any, kind: str, key: str, consequence: str) -> bool:
    """:func:`soft_deleted` for one playlist ``kind`` of row, its id in ``detail`` under ``key``."""
    return soft_deleted(
        row,
        message=(
            f"the {kind} row {getattr(row, 'ID', '?')!r} cannot say whether "
            f"rekordbox removed it, and treating that as live would {consequence}"
        ),
        origin=("rb_writer",),
        detail={key: str(getattr(row, "ID", ""))},
    )


def membership_removed(row: Any) -> bool:
    """Whether rekordbox, or this product, removed one membership row. Or REFUSE."""
    return _row_removed(
        row, "playlist membership", "membership_id", "report a track as filed where nobody can see it"
    )


def node_removed(row: Any) -> bool:
    """Whether one playlist or folder row carries the marker. Or REFUSE."""
    return _row_removed(row, "playlist", "playlist_id", "file a track in a playlist nobody can see")


# ---------------------------------------------------------------------------
# Tag primitives
# ---------------------------------------------------------------------------


def _mytag_templates(db: Any) -> tuple[Any, Any, Any]:
    """Mirror the shape of existing tag rows: (root parent, category, value).

    The binding defines no constants, and a fabricated attribute is a corruption that looks working.
    """
    root_parent = None
    category_attr = None
    value_attr = None
    for tag in db.get_my_tag():
        parent_id = str(getattr(tag, "ParentID", "") or "")
        if parent_id in ROOT_PARENT_SENTINELS:
            if category_attr is None:
                root_parent, category_attr = parent_id, getattr(tag, "Attribute", 0)
        elif value_attr is None:
            value_attr = getattr(tag, "Attribute", 0)
    if category_attr is None:
        # :func:`my_tag_writable` reads this reason by the same literal.
        raise _unavailable(
            "mytag-category-template-missing",
            "the library has no tag category to mirror, so there is nothing to "
            "copy the row shape from and this writer refuses to invent one",
        )
    if value_attr is None:
        value_attr = category_attr
    return root_parent, category_attr, value_attr


# ---------------------------------------------------------------------------
# The additive whitelist
# ---------------------------------------------------------------------------


#: rekordbox's soft-delete marker, named once so a reader is BOUND to it through the import
#: graph. Naming it does NOT make it readable permissively; see
#: ``tests/_source_guards.py:permissive_soft_delete_reads``.
SOFT_DELETE_COLUMN = "rb_local_deleted"


#: What a planned removal may change on its own row, and on its memberships.
_REMOVED_COLUMNS = frozenset({SOFT_DELETE_COLUMN, "updated_at", "usn", "rb_local_usn"})

#: Columns the binding and the object mapper bump on their own during a commit. All ten,
#: or a correct write trips the guard and the guard gets disabled (P7).
BOOKKEEPING_COLUMNS = frozenset(
    {
        "ID",
        "UUID",
        "usn",
        "rb_local_usn",
        "rb_data_status",
        "rb_local_data_status",
        SOFT_DELETE_COLUMN,
        "rb_local_synced",
        "created_at",
        "updated_at",
    }
)


def assert_foreign_untouched(db: Any) -> None:
    """Refuse a commit that would change another app's folder at the top (U185).

    ASKED TWO WAYS: the pending objects, and the subtree reread from SQL against
    the reading :func:`open_db` kept. A handle with no reading REFUSES.
    """
    from cratekit.core import foreign_tree

    before = foreign_tree.reading_at_open(db)
    if before is None:
        raise _unavailable(
            "whitelist-violation",
            f"{foreign_tree.OWNER}'s folder at the top of the playlist tree was not "
            f"read when this database handle opened, so whether this write leaves it "
            f"alone cannot be said; nothing was written",
            detail={"violations": ["the foreign folder was not read at open"]},
        )
    session = getattr(db, "session", None)
    violations = foreign_tree.pending_touches(pending_objects(session, db), before)
    violations += foreign_tree.differences(before, foreign_tree.read(session))
    if violations:
        raise _unavailable(
            "whitelist-violation",
            f"the pending write would change {foreign_tree.OWNER}'s folder at the top "
            f"of the playlist tree, which another app owns and this product leaves "
            f"exactly as it is; nothing was written:\n  - " + "\n  - ".join(violations),
            detail={"violations": list(violations)},
        )


def assert_created_rows_are_gridless(db: Any) -> None:
    """Verify from SQL that no row this session creates carries analysis data.

    NOT FROM THE OBJECT, which reports intent, not what the database stores after
    the binding's stamping and defaults. ORDERING IS LOAD BEARING: the deliberate
    flush comes after the guard captured its inputs and before the commit, so a
    violation still rolls back. THE ROWS COME FROM BOTH SOURCES (R-760), and a
    content row is held to :data:`CONTENT_ROW_EMPTY_COLUMNS` and to owning no
    analysis table row.
    """
    session = getattr(db, "session", None)
    if session is None:
        return

    from sqlalchemy import inspect as sa_inspect
    from sqlalchemy import text

    pending = {id(obj): obj for obj in session.new}
    instances = {**_registry_created_instances(db), **pending}
    if not instances:
        return

    # The flush populates the primary keys.
    try:
        session.flush()
    except Exception:  # noqa: BLE001 - a flush failure is the caller's to report
        return

    violations: list[str] = []
    for obj in instances.values():
        table = _table_of(obj)
        if table is None:
            continue
        policy = CONTENT_ROW_EMPTY_COLUMNS if table == CONTENT_TABLE else GRIDLESS_ON_CREATE_COLUMNS
        columns = {c.name for c in obj.__table__.columns} & policy
        if not columns:
            continue
        try:
            identity = sa_inspect(obj).identity
        except Exception:  # noqa: BLE001 - a stand in with no mapper state has no row
            continue
        if not identity:
            continue
        keys = [c.name for c in obj.__table__.primary_key.columns]
        where = " AND ".join(f"{k} = :{k}" for k in keys)
        selected = ", ".join(sorted(columns))
        row = session.execute(
            text(f"SELECT {selected} FROM {table} WHERE {where}"),
            dict(zip(keys, identity)),
        ).first()
        if row is None:
            continue
        for name, value in zip(sorted(columns), row):
            if value not in EMPTY_ON_CREATE:
                violations.append(f"{table}.{name} = {value!r}")
        if table == CONTENT_TABLE and len(keys) == 1:
            for owned in CONTENT_ANALYSIS_TABLES:
                count = session.execute(
                    text(f"SELECT COUNT(*) FROM {owned} WHERE ContentID = :id"),
                    {"id": identity[0]},
                ).scalar()
                if count:
                    violations.append(
                        f"{owned} holds {count} row(s) for the new {CONTENT_TABLE} "
                        f"row {identity[0]!r}"
                    )

    if violations:
        raise _unavailable(
            "whitelist-violation",
            "a row this session creates carries analysis data, which this product "
            "never writes; rekordbox derives the grid from the audio:\n  - "
            + "\n  - ".join(violations),
            detail={"violations": violations},
        )


def assert_session_whitelisted(
    session: Any,
    db: Any = None,
    *,
    removals: Iterable[str] = (),
    creations: Iterable[str] = (),
    deletions: Iterable[str] = (),
) -> None:
    """Raise unless the pending session touches only whitelisted tables and columns."""
    created, modified, removed = pending_changes(session, db)
    violations = guard_violations(
        created, modified, removed, removals=removals, creations=creations, deletions=deletions
    )
    if violations:
        raise _unavailable(
            "whitelist-violation",
            "the pending write session touches tables or columns outside the "
            "additive whitelist:\n  - " + "\n  - ".join(violations),
            detail={"violations": list(violations)},
        )


# ---------------------------------------------------------------------------
# The cross-process write-session lock
# ---------------------------------------------------------------------------


def _acquire_exclusive(handle: Any) -> None:
    """Take a non-blocking exclusive lock on an open file. Raises OSError on contention.

    The kernel releases it when the holder dies, which IS the stale-lock recovery;
    a pid file would race a live holder when reclaimed.
    """
    if sys.platform.startswith("win"):  # pragma: no cover - needs Windows
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _release_exclusive(handle: Any) -> None:
    if sys.platform.startswith("win"):  # pragma: no cover - needs Windows
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def write_session_lock(path: Path | str | None = None, *, cfg: config.Config | None = None):
    """Hold the write-session lock for a whole session: snapshot through smoke test.

    Two writers must not interleave. THE FILE IS NEVER UNLINKED, since that races
    a holder locking the inode. Narrower than ``core.session``'s lock, sharing the
    same acquisition helpers.
    """
    target = Path(path) if path is not None else write_lock_path(cfg)
    # A private directory too, or the lock file can be replaced (P1).
    config.mkdir_private(target.parent)

    handle = open(target, "a+")
    try:
        if hasattr(os, "chmod"):  # guarded: a POSIX mode is meaningless on some platforms
            try:
                os.chmod(target, config.PRIVATE_FILE_MODE)
            except OSError as exc:
                # Best effort: on a shared machine the mode may be unsettable, and
                # refusing would cost mutual exclusion itself.
                logger.debug("could not set the mode on the write lock at %s: %s", target, exc)
        try:
            _acquire_exclusive(handle)
        except OSError as exc:
            raise _unavailable(
                "write-lock-held",
                f"another writer holds the write-session lock at {target}; it is "
                f"not reclaimable by force, so wait for that run to finish",
                detail={"lock": str(target)},
            ) from exc
        yield target
    finally:
        try:
            _release_exclusive(handle)
        finally:
            handle.close()


# ---------------------------------------------------------------------------
# The guarded commit
# ---------------------------------------------------------------------------


class CommitWitness:
    """Whether the SQL commit on one handle has landed. See :func:`commit_witness`."""

    __slots__ = ("landed",)

    def __init__(self) -> None:
        self.landed = False

    def _mark(self, _session: Any) -> None:
        self.landed = True


@contextmanager
def commit_witness(db: Any) -> Iterator[CommitWitness]:
    """Tell a commit that LANDED and then raised from one that never landed.

    AN EXCEPTION OUT OF A COMMIT DOES NOT MEAN NOTHING WAS COMMITTED: the binding
    lands the SQL first, then saves the legacy playlist file, so a rollback then
    does nothing and a restore would silently reach past durable rows. Asked of
    SQLAlchemy's ``after_commit`` event, removed on the way out.
    """
    from sqlalchemy import event

    witness = CommitWitness()
    target = getattr(db, "session", None)
    if target is None:
        yield witness
        return
    event.listen(target, "after_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "after_commit", witness._mark)


def commit_guarded(
    db: Any,
    *,
    force_cloud_canary: bool = False,
    removals: Iterable[str] = (),
    creations: Iterable[str] = (),
    deletions: Iterable[str] = (),
) -> None:
    """Commit only when it is still safe to, and roll back rather than leak.

    ``removals`` (U111, U145), ``creations`` (R-746) and ``deletions`` (U288) are
    empty for every writer but their few, held to their tables by the whitelist
    and to their callers by source guards. RE-CHECKED AT COMMIT, UNCONDITIONALLY:
    rekordbox can launch mid-run, and the open-time refusal sits behind a flag. A
    GUARD FAILURE ROLLS THE SESSION BACK, so a refused write never lands later
    under another name. The binding's reconciliation logger is quietened for the
    commit only, restored in a finally.
    """
    assert_rekordbox_closed("committing")

    # EVERY PRE-COMMIT CHECK RUNS WITH THE AUTOMATIC FLUSH SUSPENDED, so no read
    # empties what the whitelist inspects; see ``_no_autoflush``.
    with _no_autoflush(getattr(db, "session", None)):
        if cloud_sync_active(db):
            raise _unavailable(
                "cloud-sync-active",
                f"Cloud Library Sync appears active, so this commit would race a "
                f"concurrent writer: {cloud_sync_state(db).reason}",
            )
        assert_cloud_sync_readable(db, force=force_cloud_canary)

        try:
            # Reads the buffer too, so an autoflushed write is still judged (W2).
            assert_session_whitelisted(
                db.session, db, removals=removals, creations=creations, deletions=deletions
            )
            assert_created_rows_are_gridless(db)
            assert_foreign_untouched(db)
        except RekordboxUnavailable:
            db.rollback()
            raise

    reconciliation_logger = logging.getLogger("pyrekordbox.db6.database")
    previous = reconciliation_logger.level
    reconciliation_logger.setLevel(logging.ERROR)
    try:
        with _binding_probe(strict=True):
            db.commit()
    finally:
        reconciliation_logger.setLevel(previous)


def _live_collection_row(db: Any, content_class: Any, key: str) -> Any:
    """The live collection row ``key``, or the refusal for one that is gone or cannot say (U288)."""
    row = db.session.get(content_class, key)
    if row is None or soft_deleted(
        row,
        message=(
            f"the collection row {key!r} cannot say whether rekordbox removed it, "
            f"and deleting it as live could take a track out twice"
        ),
        origin=("rb_writer",),
        detail={"content_id": key},
    ):
        raise _unavailable(
            "whitelist-violation",
            f"asked to take the collection row {key!r} out of the collection, and "
            f"the database holds no live row of that id; nothing was written",
            detail={"content_id": key},
        )
    return row


class CollectionRemoval:
    """One removal from the collection, prepared, then committed, then read back (U288).

    THE ONE ENTRY A VERB CALLS, so the order is the class's: :meth:`prepare`
    reads everything and writes nothing; :meth:`commit` deletes, renumbers
    (R-1830), proves both confined from SQL and commits with ``deletions``;
    :meth:`read_back` reads the whole database again.
    """

    def __init__(
        self,
        db: Any,
        content_ids: Sequence[str],
        identity: str,
        columns: Mapping[str, Mapping[str, Any]],
        before: DatabaseReading,
        renumbered: Mapping[str, tuple[str, int, int]] | None = None,
    ) -> None:
        self.db = db
        self.content_ids = tuple(content_ids)
        self.identity = identity
        self.columns = {key: dict(value) for key, value in columns.items()}
        self.before = before
        #: Rows :meth:`commit` renumbers, ``(playlist id, TrackNo now, TrackNo after)`` (R-1830).
        self.renumbered: dict[str, tuple[str, int, int]] = dict(renumbered or {})
        #: Rows deleted, by table, once :meth:`commit` has made them.
        self.deleted: dict[str, int] = {}

    @classmethod
    def prepare(cls, db: Any, content_ids: Iterable[str]) -> CollectionRemoval:
        """Prepare a removal from the collection, reading everything and writing NOTHING.

        REFUSED HERE: no live row, a row named outside the removal set, or a
        database with no identity, since the removal record is bound to it.
        """
        ids = tuple(dict.fromkeys(str(one) for one in content_ids))
        identity = database_id(db)
        if not identity:
            raise _unavailable(
                "canary-read-failed",
                "the rekordbox database reports no identity of its own, so the record of "
                "what was removed could not be bound to it; nothing was written",
                detail={"column": "DBID"},
            )
        content_class = _mapped(CONTENT_TABLE)
        columns: dict[str, dict[str, Any]] = {}
        for key in ids:
            columns[key] = recorded_columns(_live_collection_row(db, content_class, key))
        held = content_references(db, ids)
        if held:
            named = "; ".join(
                f"{key}: " + ", ".join(f"{table} ({count})" for table, count in sorted(tables.items()))
                for key, tables in sorted(held.items())
            )
            raise _unavailable(
                "whitelist-violation",
                f"rows in tables rekordbox's Remove from Collection was never measured on "
                f"name collection rows this removal would take out ({named}), so what it "
                f"would do with them is not known; nothing was written",
                detail={"tables": {key: dict(value) for key, value in sorted(held.items())}},
            )
        return cls(db, ids, identity, columns, database_reading(db), removal_renumbering(db, ids))


    @staticmethod
    def held(db: Any, content_ids: Iterable[str]) -> dict[str, dict[str, int]]:
        """Which of ``content_ids`` a table outside the removal set names, so the plan keeps them."""
        return content_references(db, content_ids)

    @staticmethod
    def renumbering(db: Any, content_ids: Iterable[str]) -> dict[str, tuple[str, int, int]]:
        """The membership rows removing ``content_ids`` would renumber, for the plan's count (R-1830)."""
        return removal_renumbering(db, content_ids)

    def commit(self, *, force_cloud_canary: bool = False) -> None:
        """Delete every planned row, renumber what follows it, prove both confined, and commit through the guard."""
        for content_id in self.content_ids:
            for table, rows in remove_from_collection(self.db, content_id).items():
                self.deleted[table] = self.deleted.get(table, 0) + len(rows)
        renumber_memberships(self.db, self.renumbered)
        assert_collection_removal_confined(self.db, self.before, removed=self.content_ids)
        commit_guarded(
            self.db, force_cloud_canary=force_cloud_canary, deletions=DELETABLE_TABLES
        )

    def read_back(self) -> list[str]:
        """Every difference the committed database shows that the removal does not explain."""
        return collection_removal_violations(
            self.before, database_reading(self.db), removed=self.content_ids, committed=True
        )

    def write_into(
        self,
        detail: dict[str, Any],
        *,
        sequence: int | None,
        about: Mapping[str, Mapping[str, Any]],
    ) -> None:
        """Name every removed row in a session record's ``detail``, under :data:`RECORDED_REMOVALS_KEY`.

        ``about`` is the verb's description of each row. ``sequence`` None means the
        deletion pass offers none of these files. Renumbered rows are named (R-1830).
        """
        recorded: dict[str, Any] = {
            "database_identity": self.identity,
            "sequence": sequence,
            "deleted": dict(sorted(self.deleted.items())),
            "rows": [
                {
                    "content_id": content_id,
                    **dict(about.get(content_id, {})),
                    "columns": dict(self.columns.get(content_id, {})),
                }
                for content_id in self.content_ids
            ],
        }
        # Only when something moved, so other records read as before.
        if self.renumbered:
            recorded["renumbered"] = [
                {"membership_id": key, "playlist_id": playlist, "from": was, "to": now}
                for key, (playlist, was, now) in sorted(self.renumbered.items())
            ]
        detail[RECORDED_REMOVALS_KEY] = recorded

