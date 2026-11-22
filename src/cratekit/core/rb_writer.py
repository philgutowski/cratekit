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

import json
import logging
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from enum import StrEnum
from functools import partial
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import config, processes
from cratekit.core.cause import Cause, CratekitError, Scope, name_the_database, refuse
from cratekit.core.exit_codes import Remedy

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


def _cause(
    reason: str,
    message: str,
    *,
    remedy: Remedy | None = None,
    steps: Sequence[str] = (),
    scope: Scope = Scope.SESSION,
    detail: Mapping[str, Any] | None = None,
    inner: Cause | None = None,
) -> Cause:
    """Build one cause through ``cause.refuse``, so the closed reason registry applies in one place."""
    return refuse(
        reason,
        message,
        remedy=remedy,
        steps=steps,
        scope=scope,
        detail=detail,
        inner=inner,
    ).cause


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
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("rekordbox_db", resolved)


def snapshot_root(cfg: config.Config | None = None) -> Path:
    """Where snapshots live: beside the library, and outside the coupled set to avoid nesting."""
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("snapshots", resolved)


def write_lock_path(cfg: config.Config | None = None) -> Path:
    """The cross-process write-session lock, beside the library so every installation shares it (R31)."""
    resolved = cfg if cfg is not None else config.load()
    return config.state_path("write_lock", resolved)


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

#: Test-only relocation of the application bundle. It RELOCATES a configured value, never supplies one.
ENV_APP_PATH = "CRATEKIT_REKORDBOX_APP"


def _macos_app_version(app_path: Path) -> str | None:
    """The short version string from a macOS application bundle, or None."""
    import plistlib

    info = Path(app_path) / "Contents" / "Info.plist"
    try:
        with info.open("rb") as handle:
            data = plistlib.load(handle)
    except (OSError, ValueError):
        return None
    value = data.get("CFBundleShortVersionString")
    return str(value) if value else None


def _windows_app_version(app_path: Path) -> str | None:  # pragma: no cover - needs Windows
    """Placeholder probe for Windows: None degrades like an uninstalled application."""
    return None


def _default_app_probe() -> Callable[[Path], str | None]:
    if sys.platform == "darwin":
        return _macos_app_version
    if sys.platform.startswith("win"):
        return _windows_app_version
    return lambda _path: None


def _candidate_app_paths(cfg: config.Config | None) -> list[Path]:
    """Where to look for the installed application, most specific first, configuration before glob."""
    override = os.environ.get(ENV_APP_PATH)
    if override:
        return [Path(override)]
    configured = _pins(cfg).app_path
    if configured is not None:
        return [Path(configured)]
    if sys.platform == "darwin":
        import glob

        # Newest first: the newest install opened the database most recently.
        return [
            Path(found)
            for found in sorted(glob.glob("/Applications/rekordbox*/rekordbox.app"), reverse=True)
        ]
    return []


def read_installed_app_version(*, cfg: config.Config | None = None) -> str | None:
    """The installed rekordbox application version, or None, never an exception.

    A raise would look like drift, which has the opposite remedy. ``cfg`` is
    keyword-only so the pin and the probe read one configuration (P2).
    """
    probe = _default_app_probe()
    for candidate in _candidate_app_paths(cfg):
        version = probe(candidate)
        if version:
            return version
    return None


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
                detail={
                    "installed": found,
                    "pinned": None,
                    "validated_on": pin_validated_on(loaded),
                    "config_error": type(exc).__name__,
                },
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

    detail = {"installed": found, "pinned": pin, "validated_on": pin_validated_on(loaded)}
    if not pin:
        # The configless machine: same slug and remedy as the unrecorded pin above,
        # so "you never pinned one" exits the same either way.
        raise _unavailable(
            "app-version-pin-unrecorded",
            message,
            remedy=Remedy.RECORD_REKORDBOX_PIN,
            detail=detail,
        )
    raise _unavailable("app-version-pin-drift", message, detail=detail)


# ---------------------------------------------------------------------------
# The two-process refusal, at three sites: open, commit, and restore, because
# restore replaces the file underneath whatever has it open.
# ---------------------------------------------------------------------------


def _asked_or_scanned(name: str, ask: Callable[[], int]) -> int:
    """pyrekordbox's answer for one process, or the careful scan's when it raises (U211).

    pyrekordbox's walk dies on a process raising anything but its two caught
    errors as it exits. An ``ImportError`` is not a failed scan and propagates.
    """
    try:
        return ask()
    except ImportError:
        raise
    except Exception as exc:  # noqa: BLE001 - every escape from its walk is the scan's to judge
        logger.debug("pyrekordbox could not scan for %s, so the careful scan answers: %s", name, exc)
        return processes.rekordbox_pid(name)


def rekordbox_running() -> bool:
    """True when the rekordbox application itself is running."""
    from pyrekordbox.utils import get_rekordbox_pid

    return bool(_asked_or_scanned("rekordbox", get_rekordbox_pid))


def rekordbox_agent_running() -> bool:
    """True when the background agent is running: it mutates the library with the app closed."""
    from pyrekordbox.utils import get_rekordbox_agent_pid

    return bool(_asked_or_scanned("rekordboxAgent", get_rekordbox_agent_pid))


@contextmanager
def _binding_probe(*, strict: bool) -> Iterator[None]:
    """The binding's own rekordbox probe, answered carefully for the block's length (U211).

    The binding asks at construction (a log line) and inside ``commit`` (a raise),
    with the same fragile walk. Its own function is asked first, the careful scan
    only when that raises. ``strict`` (the commit's) lets the scan's refusal
    stand; off, an unconfirmed scan answers zero. The name is always put back.
    """
    from pyrekordbox.db6 import database as binding

    asked = binding.get_rekordbox_pid
    if getattr(asked, "_cratekit_careful", False):
        yield
        return

    def careful(*args: Any, **kwargs: Any) -> int:
        try:
            return _asked_or_scanned("rekordbox", partial(asked, *args, **kwargs))
        except processes.AbsenceUnconfirmed:
            if strict:
                raise
            return 0

    careful._cratekit_careful = True  # type: ignore[attr-defined]
    binding.get_rekordbox_pid = careful
    try:
        yield
    finally:
        if binding.get_rekordbox_pid is careful:
            binding.get_rekordbox_pid = asked


#: The probe for each name in the shared process list (``core.processes``).
#: Values are ATTRIBUTE NAMES resolved at call time, so tests can patch the seams.
_PROCESS_PROBES: Mapping[str, str] = MappingProxyType(
    {
        "rekordbox": "rekordbox_running",
        "rekordboxAgent": "rekordbox_agent_running",
    }
)


def rekordbox_processes_running() -> str:
    """The names of the rekordbox processes holding the database, comma joined, empty when clear.

    A shared-list name with no probe here raises: an unaskable process cannot be declared clear.
    """
    running = []
    unconfirmed: processes.AbsenceUnconfirmed | None = None
    for name in processes.REKORDBOX_PROCESSES:
        probe_name = _PROCESS_PROBES.get(name)
        if probe_name is None:
            raise _running(
                f"{name!r} is listed as a process holding the database but this "
                f"module has no way to ask whether it is running, so no write "
                f"can be declared safe",
                detail={"process": name},
            )
        try:
            if globals()[probe_name]():
                running.append(name)
        except processes.AbsenceUnconfirmed as exc:
            unconfirmed = unconfirmed or exc
    if unconfirmed is not None:
            # ONE ANSWER WITH ``core.processes`` (U211): a name any probe read is
            # running; only a scan that read none leaves the absence unknown.
        read = {processes.executable_stem(found) for _pid, found in unconfirmed.read}
        running = [name for name in processes.REKORDBOX_PROCESSES if name in running or name in read]
        if not running:
            raise unconfirmed
    return ", ".join(running)


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


class CloudSyncState(StrEnum):
    """What is known about Cloud Library Sync: "cannot tell" has a different fix from "on"."""

    OFF = "off"
    ON = "on"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class CloudSyncVerdict:
    """One reading of the cloud-sync state; ``reason`` quotes the key or row that decided it."""

    state: CloudSyncState
    reason: str


#: The setting rekordbox writes when the user toggles Cloud Library Sync (found 2026-08-01).
LIBRARY_SYNC_SETTING = "EnableLibrarySync"

#: The application-data subdirectory holding the settings file, named ``rekordbox6`` even
#: under rekordbox 7, so it is not derived from the application version.
SETTINGS_APP_DIRNAME = "rekordbox6"

#: A real rekordbox application-data directory for the canary's battery. A SUBSTITUTION, not
#: a skip: unset, the same assertions run on a settings file the test wrote.
TEST_SETTINGS_ENV = "CRATEKIT_TEST_REKORDBOX_SETTINGS"


def _no_autoflush(session: Any):
    """Suspend the session's automatic flush, degrading to a no-op without one.

    Every guard reads the session's PENDING collections, and a query through the
    session flushes them empty, so a probe that queries blinds the whitelist to a
    forbidden write. No pre-commit probe queries now; KEEP IT ANYWAY, because the
    containment belongs to the guard path, not its current occupant. A no-op
    without a session keeps the guards testable with stand-ins.
    """
    guard = getattr(session, "no_autoflush", None)
    if guard is None:
        return nullcontext()
    return guard


def read_rekordbox_settings(app_dir: Path | str | None = None) -> Mapping[str, Any]:
    """Parse rekordbox's settings file through the binding's reader. A seam: patch it HERE."""
    from pyrekordbox.config import get_pioneer_app_dir
    from pyrekordbox.config import read_rekordbox_settings as _read

    base = Path(app_dir) if app_dir is not None else get_pioneer_app_dir()
    return _read(base / SETTINGS_APP_DIRNAME)


def cloud_sync_state(db: Any = None) -> CloudSyncVerdict:
    """Read whether Cloud Library Sync is on, off, or unreadable, from the settings file only.

    ``db`` is DELIBERATELY NOT READ, keeping this off the :func:`_no_autoflush`
    hazard. The OFF encoding ``val="0"`` was observed (2026-08-01); the
    comparison is "not zero" so any positive encoding is caught. **The ON
    encoding is an untested inference**, unlike the markers below, which were
    checked against a real library and found FALSE: the cloud agent registry's
    row count (it refused every open for three days), the cloud property
    service name, the equipment authorisation file, the credential timestamp,
    and per-row content sync columns. TWO SETTINGS KEYS ARE TRAPS: the sync
    METHOD and the overwrite-list flag read enabled with sync off, so never
    match a "sync" substring.
    """
    try:
        settings = read_rekordbox_settings()
    except Exception as exc:  # noqa: BLE001 - any failure to read is "cannot tell"
        return CloudSyncVerdict(
            CloudSyncState.UNKNOWN,
            f"the rekordbox settings file could not be read, so {LIBRARY_SYNC_SETTING} "
            f"is unknown: {exc}",
        )

    if LIBRARY_SYNC_SETTING not in settings:
        return CloudSyncVerdict(
            CloudSyncState.UNKNOWN,
            f"the rekordbox settings file carries no {LIBRARY_SYNC_SETTING} value",
        )

    declared = settings[LIBRARY_SYNC_SETTING]
    if str(declared) not in ("0", "False"):
        return CloudSyncVerdict(
            CloudSyncState.ON,
            f"{LIBRARY_SYNC_SETTING}={declared!r} in the rekordbox settings file",
        )

    # A database staleness cross-check stood here and was deleted on evidence: the
    # settings file flips at toggle time (A1, A3). It also queried the caller's
    # session; read ``_no_autoflush`` before adding anything back here.
    return CloudSyncVerdict(CloudSyncState.OFF, f"{LIBRARY_SYNC_SETTING}={declared!r}")


def cloud_sync_active(db: Any) -> bool:
    """True only when the evidence says ON; unknown is refused by :func:`assert_cloud_sync_readable`."""
    return cloud_sync_state(db).state is CloudSyncState.ON


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


# ---------------------------------------------------------------------------
# Snapshot, integrity, restore, prune
# ---------------------------------------------------------------------------


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
    source = Path(db_path) if db_path is not None else live_db_path(cfg)
    destination_root = Path(root) if root is not None else snapshot_root(cfg)

    if db is not None:
        try:
            from sqlalchemy import text

            db.session.execute(text("PRAGMA wal_checkpoint(TRUNCATE)"))
        except Exception as exc:  # noqa: BLE001 - the checkpoint is the belt, not the braces
            logger.debug("snapshot checkpoint did not run, relying on the sidecar copy: %s", exc)

    destination = destination_root / stamp
    # A private directory too: a file in a world-writable one can be replaced (P1).
    config.mkdir_private(destination)
    return _copy_file_set(source, destination)


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
        *(origin.with_name(origin.name + suffix) for suffix in db_sidecar_suffixes()),
        origin.parent / MASTER_PLAYLIST_XML,
    )


def copy_file_set(source: Path | str, destination: Path) -> Path:
    """Copy a database's whole file set into an existing ``destination``, answering the copy (U162).

    THE CALLER ESTABLISHES THAT REKORDBOX IS CLOSED, as for :func:`disposable_copy`.
    """
    return _copy_file_set(Path(source), destination)


def disposable_root() -> Path:
    """The directory every throwaway copy is made in, asked once so the room measured is its (R-1677).

    ``tempfile`` reads ``TMPDIR``. Raises :class:`FileNotFoundError` when none is usable.
    """
    return Path(tempfile.gettempdir())


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


def _scratch_or_none() -> Path | None:
    try:
        return disposable_root()
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
    directory = Path(tempfile.mkdtemp(prefix="cratekit-copy-", dir=disposable_root()))
    try:
        yield _copy_file_set(origin, directory)
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
    assert_rekordbox_closed("copying the database for a read only look")
    require_present(Path(source))
    with disposable_copy(source) as copied:
        refusal = None if copied.stat().st_size else _not_a_library(Path(source), copied)
        if refusal is not None:
            raise refusal
        try:
            db = open_db(copied, check_app_version=False, cfg=cfg)
        except RekordboxUnavailable as exc:
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _not_a_library(Path(source), copied)
            if refusal is None:
                raise
            raise refusal from exc
        try:
            yield db
        finally:
            close_db(db)


#: The tables the canary reads. A file holding NEITHER is not a library; holding one is drift.
CANARY_TABLES = ("agentRegistry", "djmdContent")


def _copy_tables(copied: Path) -> set[str] | None:
    """The table names in the copy's schema through the binding (for the key), or None, never empty."""
    from pyrekordbox import Rekordbox6Database
    from sqlalchemy import text

    try:
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(copied), unlock=unlock_needed(copied))
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
    try:
        rows = db.session.execute(text("SELECT name FROM sqlite_master WHERE type = 'table'"))
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
    finally:
        close_db(db)


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
        with disposable_copy(snapshot_database) as checked:
            copied = True
            try:
                db = open_db(checked, check_app_version=False, unlock=unlock)
            except RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
            finally:
                # The full release: the throwaway directory is removed next.
                close_db(db)
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
    target = Path(db_path) if db_path is not None else live_db_path(cfg)
    source = Path(snapshot_database)

    assert_rekordbox_closed("restoring the database")

    for suffix in db_sidecar_suffixes():
        live_sidecar = target.with_name(target.name + suffix)
        if live_sidecar.exists():
            live_sidecar.unlink()

    shutil.copy2(source, target)
    for suffix in restored_sidecar_suffixes():
        snapshot_sidecar = source.with_name(source.name + suffix)
        if snapshot_sidecar.exists():
            shutil.copy2(snapshot_sidecar, target.with_name(target.name + suffix))

    playlist_xml = source.parent / MASTER_PLAYLIST_XML
    if playlist_xml.exists():
        shutil.copy2(playlist_xml, target.parent / MASTER_PLAYLIST_XML)


# --- the protected-snapshot provider seam ----------------------------------


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
        resolved = _loaded_config(cfg)
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
    for candidate in sorted(directory.glob("*.db")):
        if candidate.is_file():
            return candidate
    return None


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
    destination_root = Path(root) if root is not None else snapshot_root(cfg)
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


# ---------------------------------------------------------------------------
# Playlist and tag primitives
# ---------------------------------------------------------------------------

#: Parent identifiers meaning "top-level tag category": the schema has used all four spellings.
ROOT_PARENT_SENTINELS = ("", "0", "root", "None")


def _is_folder(playlist: Any) -> bool:
    return int(getattr(playlist, "Attribute", -1)) == 1


def is_folder(playlist: Any) -> bool:
    """Whether a playlist row is a FOLDER. The one spelling of that question."""
    return _is_folder(playlist)


def ensure_folder(db: Any, name: str, parent: Any = None) -> Any:
    """Find or create a playlist FOLDER by name, optionally under a parent.

    ``name`` has no default, so no taxonomy name lives here (R19). ``parent``
    scopes the match as :func:`ensure_playlist` does, since two trees may hold
    folders of one name; unscoped is for a top-level folder.
    """
    if parent is None:
        for playlist in db.get_playlist(Name=name):
            if _is_folder(playlist):
                return playlist
        return db.create_playlist_folder(name)

    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if _is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist_folder(name, parent=parent)


def top_level_folders(db: Any, name: str) -> tuple[Any, ...]:
    """Every playlist FOLDER named ``name`` sitting directly under the playlist root.

    All of them, so a caller recording an adopted root can require exactly one;
    a nested namesake is not a candidate. IT CREATES NOTHING and reads no soft
    delete marker. The rows are materialized before the caller reads further.
    """
    return tuple(
        playlist
        for playlist in list(db.get_playlist(Name=name))
        if _is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
    )


def ensure_playlist(db: Any, name: str, parent: Any) -> Any:
    """Find or create a playlist under a specific parent, never global by name."""
    parent_id = str(parent.ID)
    for playlist in db.get_playlist(Name=name):
        if not _is_folder(playlist) and str(getattr(playlist, "ParentID", "")) == parent_id:
            return playlist
    return db.create_playlist(name, parent=parent)


def add_memberships(db: Any, playlist: Any, content_ids: Iterable[str]) -> list[str]:
    """Add each track to a playlist when absent. Returns the ids it inserted, in order.

    THE ONE HOME OF "ONLY WHEN ABSENT" (R-10); a second spelling double inserts
    or skips. One presence query per call, each insert joining the set. Race-free
    ONLY under the write-session lock. A MEMBERSHIP MARKED REMOVED IS NOT PRESENT
    (R-758), or a track moved back would never return.
    """
    songs = list(db.get_playlist_songs(PlaylistID=str(playlist.ID)))
    present = {str(song.ContentID) for song in songs if not membership_removed(song)}
    highest = max((int(song.TrackNo or 0) for song in songs), default=0)
    inserted: list[str] = []
    for content_id in content_ids:
        key = str(content_id)
        if key in present:
            continue
        added = db.add_to_playlist(playlist, key)
        # AN APPEND GOES PAST THE HIGHEST POSITION, NOT PAST THE ROW COUNT (U288):
        # gaps and removed rows make count plus one collide with a live row.
        number = int(getattr(added, "TrackNo", 0) or 0)
        if added is not None and number <= highest:
            added.TrackNo = highest + 1
            number = highest + 1
        highest = max(highest, number)
        present.add(key)
        inserted.append(key)
    return inserted


def add_membership(db: Any, playlist: Any, content_id: str) -> bool:
    """Add a track to a playlist when absent, through :func:`add_memberships`. True when it inserted."""
    return bool(add_memberships(db, playlist, [content_id]))


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


def membership_removed(row: Any) -> bool:
    """Whether rekordbox, or this product, removed one membership row. Or REFUSE."""
    return soft_deleted(
        row,
        message=(
            f"the playlist membership row {getattr(row, 'ID', '?')!r} cannot say "
            f"whether rekordbox removed it, and treating that as live would "
            f"report a track as filed where nobody can see it"
        ),
        origin=("rb_writer",),
        detail={"membership_id": str(getattr(row, "ID", ""))},
    )


def node_removed(row: Any) -> bool:
    """Whether one playlist or folder row carries the marker. Or REFUSE."""
    return soft_deleted(
        row,
        message=(
            f"the playlist row {getattr(row, 'ID', '?')!r} cannot say whether "
            f"rekordbox removed it, and treating that as live would file a "
            f"track in a playlist nobody can see"
        ),
        origin=("rb_writer",),
        detail={"playlist_id": str(getattr(row, "ID", ""))},
    )


def remove_memberships(db: Any, playlist: Any, content_ids: Iterable[str]) -> list[str]:
    """Mark each track's live membership of one playlist removed. Returns the ids.

    THE ONE REMOVAL THIS PRODUCT MAKES, AND IT IS A SOFT DELETE (R-758): the
    marker set, ``updated_at`` now, ``TrackNo`` kept so nothing renumbers. Not
    the binding's ``remove_from_playlist``, which hard deletes and COMMITS BY
    ITSELF. rekordbox's observed removed rows all sat in removed playlists, so a
    single track out of a living one was not observed (in the ledger). EVERY LIVE
    ROW FOR THE PAIR IS MARKED; unheld ids are skipped. DOES NOT COMMIT: the
    caller commits through :func:`commit_guarded` naming this table in ``removals``.
    """
    from datetime import datetime

    wanted = {str(content_id) for content_id in content_ids}
    now = datetime.now()
    removed: list[str] = []
    for song in list(db.get_playlist_songs(PlaylistID=str(playlist.ID))):
        key = str(song.ContentID)
        if key not in wanted or membership_removed(song):
            continue
        setattr(song, SOFT_DELETE_COLUMN, 1)
        song.updated_at = now
        removed.append(key)
    return removed


# ---------------------------------------------------------------------------
# Playlist nodes: the move and the removal (U111)
# ---------------------------------------------------------------------------


def _node_refusal(reason: str, message: str, playlist: Any) -> CratekitError:
    return refuse(
        reason,
        message,
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.RUN,
        origin=("rb_writer",),
        detail={"playlist_id": str(getattr(playlist, "ID", ""))},
    )


def _plain_playlist(playlist: Any, what: str) -> None:
    """Refuse anything but a live, ordinary playlist. A folder carries a tree."""
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
            "whitelist-violation",
            f"{what} the playlist row {getattr(playlist, 'ID', '?')!r}, which is a "
            f"folder or a smart playlist; only an ordinary playlist is moved or "
            f"removed, so a node holding other nodes is never taken with it",
            playlist,
        )
    if node_removed(playlist):
        raise _node_refusal(
            "whitelist-violation",
            f"{what} the playlist row {getattr(playlist, 'ID', '?')!r}, which "
            f"rekordbox or this product already removed",
            playlist,
        )


def move_playlist_node(db: Any, playlist: Any, parent: Any) -> None:
    """Move one ordinary playlist to the end of a live folder. Never a folder.

    Through the binding's ``move_playlist``: parent and position change, old
    siblings close up, nothing held is touched. REFUSED, NOT SKIPPED: a folder or
    smart playlist, a removed node, a parent not a live folder. DOES NOT COMMIT.
    """
    _plain_playlist(playlist, "asked to move")
    if not _is_folder(parent) or node_removed(parent):
        raise _node_refusal(
            "whitelist-violation",
            f"asked to move a playlist into {getattr(parent, 'ID', '?')!r}, which "
            f"is not a live folder",
            playlist,
        )
    db.move_playlist(playlist, parent=parent)


def remove_playlist_node(db: Any, playlist: Any) -> list[str]:
    """Mark one ordinary playlist removed, with its own memberships. Returns their ids.

    THE SAME SOFT DELETE (R-758), as rekordbox's own removed playlists show. No
    content row and no other playlist's membership is touched; ``Seq`` stays.
    REFUSED: a folder (carries a tree), a smart playlist (no rows), a removed node.
    DOES NOT COMMIT: ``removals`` must name this and the membership table.
    """
    from datetime import datetime

    _plain_playlist(playlist, "asked to remove")
    held = [
        str(song.ContentID)
        for song in list(db.get_playlist_songs(PlaylistID=str(playlist.ID)))
        if not membership_removed(song)
    ]
    marked = remove_memberships(db, playlist, held)
    setattr(playlist, SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked


@dataclass(frozen=True)
class NodeTables:
    """The three tables a node change could reach, read from SQL with no mapper, row by row.

    Content is one digest per row, since only "did any row differ" is asked of it.
    """

    content: Mapping[str, str]
    playlists: Mapping[str, tuple]
    memberships: Mapping[str, tuple]
    playlist_columns: tuple[str, ...]
    membership_columns: tuple[str, ...]


def _rows_by_id(session: Any, table: str) -> tuple[dict[str, tuple], tuple[str, ...]]:
    from sqlalchemy import text

    result = session.execute(text(f"SELECT * FROM {table}"))
    columns = tuple(result.keys())
    at = columns.index("ID")
    return {str(row[at]): tuple(row) for row in result}, columns


def _row_digests(session: Any, table: str) -> dict[str, str]:
    import hashlib

    from sqlalchemy import text

    result = session.execute(text(f"SELECT * FROM {table}"))
    at = tuple(result.keys()).index("ID")
    return {
        str(row[at]): hashlib.sha256(repr(tuple(row)).encode("utf-8")).hexdigest()
        for row in result
    }


def node_tables(db: Any) -> NodeTables:
    """Read the content, playlist and membership tables from SQL, before and after a node change."""
    session = db.session
    content = _row_digests(session, CONTENT_TABLE)
    playlists, playlist_columns = _rows_by_id(session, PLAYLIST_TABLE)
    memberships, membership_columns = _rows_by_id(session, MEMBERSHIP_TABLE)
    return NodeTables(content, playlists, memberships, playlist_columns, membership_columns)


def _changed(columns: Sequence[str], before: tuple, after: tuple) -> set[str]:
    return {name for name, old, new in zip(columns, before, after) if old != new}


def node_change_violations(
    before: NodeTables,
    after: NodeTables,
    *,
    moved: Mapping[str, str],
    removed: Iterable[str],
    created: Iterable[str] = (),
) -> list[str]:
    """Every difference between two readings that the planned node change does not explain.

    ``moved`` maps playlist to new folder, ``removed`` and ``created`` name rows.
    Empty means the change was confined AND made. PURE. It explains only: no
    content change; membership marker going on inside removed playlists; a moved
    playlist live under its folder changing parent, position and bookkeeping; a
    removed one gaining the marker; EACH ASKED WHETHER IT CHANGED, so an unmade
    write refuses before the commit; others repositioned only in a parent a node
    left or joined; added playlist rows exactly ``created``, nothing else added
    or gone.
    """
    violations: list[str] = []
    gone = {str(key) for key in removed}
    planned_moves = {str(key): str(value) for key, value in moved.items()}
    if before.content != after.content:
        changed = sorted(
            key
            for key in set(before.content) | set(after.content)
            if before.content.get(key) != after.content.get(key)
        )
        violations.append(
            f"{len(changed)} {CONTENT_TABLE} row(s) changed, and a node change "
            f"touches no track: {', '.join(changed[:10])}"
        )

    p_cols = before.playlist_columns
    marker_at = p_cols.index(SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    for key in sorted(set(before.playlists) - set(after.playlists)):
        violations.append(f"the {PLAYLIST_TABLE} row {key!r} disappeared")
    added = set(after.playlists) - set(before.playlists)
    for key in sorted(added - {str(key) for key in created}):
        violations.append(f"an unplanned {PLAYLIST_TABLE} row {key!r} was added")
    # The parents a node left or joined: the only places a renumbering belongs.
    renumbered = {
        str(before.playlists[key][parent_at]) for key in planned_moves if key in before.playlists
    } | set(planned_moves.values())
    for key in sorted(planned_moves):
        new = after.playlists.get(key)
        if new is None or str(new[parent_at]) != planned_moves[key] or new[marker_at]:
            violations.append(
                f"the moved playlist {key!r} is not live under the planned "
                f"{planned_moves[key]!r}"
            )
    for key in sorted(gone):
        new = after.playlists.get(key)
        if new is None or not new[marker_at]:
            violations.append(f"the removed playlist {key!r} does not carry the marker")
    for key in sorted(set(before.playlists) & set(after.playlists)):
        old, new = before.playlists[key], after.playlists[key]
        changed = _changed(p_cols, old, new)
        if not changed:
            continue
        if key in planned_moves:
            allowed = _MOVED_COLUMNS
        elif key in gone:
            allowed = _REMOVED_COLUMNS
        elif str(old[parent_at]) in renumbered:
            allowed = _SIBLING_COLUMNS
        else:
            allowed = frozenset()
        stray = changed - allowed
        if stray:
            violations.append(
                f"the {PLAYLIST_TABLE} row {key!r} changed {sorted(stray)}, which the "
                f"planned node change does not explain"
            )

    m_cols = before.membership_columns
    owner_at = m_cols.index("PlaylistID")
    m_marker = m_cols.index(SOFT_DELETE_COLUMN)
    for key in sorted(set(before.memberships) ^ set(after.memberships)):
        violations.append(f"the {MEMBERSHIP_TABLE} row {key!r} was added or disappeared")
    # A REMOVED NODE KEEPS NO LIVE MEMBERSHIP, asked of every row it owns.
    for key in sorted(set(after.memberships)):
        row = after.memberships[key]
        if str(row[owner_at]) in gone and not row[m_marker]:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of the removed playlist "
                f"{str(row[owner_at])!r} is still live"
            )
    for key in sorted(set(before.memberships) & set(after.memberships)):
        old, new = before.memberships[key], after.memberships[key]
        changed = _changed(m_cols, old, new)
        if not changed:
            continue
        owner = str(old[owner_at])
        if owner not in gone:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of playlist {owner!r} changed "
                f"{sorted(changed)}, and only a removed playlist's own memberships may"
            )
            continue
        if changed - _REMOVED_COLUMNS or not new[m_marker]:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} of the removed playlist {owner!r} "
                f"changed {sorted(changed)}; only its marker may go on"
            )
    return violations


def assert_node_changes_confined(
    db: Any,
    before: NodeTables,
    *,
    moved: Mapping[str, str],
    removed: Iterable[str],
    created: Iterable[str] = (),
) -> None:
    """Refuse, before the commit, a node change that reached anything it did not plan.

    FROM SQL, after a deliberate flush inside the transaction. It judges rows
    (whose membership, which parent, which position), which the table and column
    whitelist cannot, nor the binding's untracked sibling renumbering. A REFUSAL
    ROLLS THE HANDLE BACK so nothing lands later under another operation's name.
    """
    db.session.flush()
    after = node_tables(db)
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if violations:
        db.rollback()
        raise _unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan, or did not make one it "
            "planned, read from SQL before the commit:\n  - " + "\n  - ".join(violations),
            detail={"violations": violations},
        )


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


def my_tag_writable(db: Any) -> bool:
    """Whether :func:`ensure_my_tag_value` could make a row here, asked before a plan promises one.

    THE WRITER'S OWN QUESTION, so a plan never promises a tag after its file moves (U127).
    """
    try:
        _mytag_templates(db)
    except RekordboxUnavailable as exc:
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return False
    return True


def ensure_my_tag_value(db: Any, category_name: str, value_name: str) -> Any:
    """Find or create a tag category and one value inside it. Returns the value row."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    root_parent, category_attr, value_attr = _mytag_templates(db)

    category = next((tag for tag in db.get_my_tag(Name=category_name)), None)
    if category is None:
        category = tables.DjmdMyTag.create(
            ID=db.generate_unused_id(tables.DjmdMyTag, is_28_bit=True),
            UUID=str(uuid4()),
            Name=category_name,
            Attribute=category_attr,
            ParentID=root_parent,
            Seq=0,
        )
        db.add(category)

    value = next(
        (
            tag
            for tag in db.get_my_tag(Name=value_name)
            if str(getattr(tag, "ParentID", "")) == str(category.ID)
        ),
        None,
    )
    if value is None:
        value = tables.DjmdMyTag.create(
            ID=db.generate_unused_id(tables.DjmdMyTag, is_28_bit=True),
            UUID=str(uuid4()),
            Name=value_name,
            Attribute=value_attr,
            ParentID=str(category.ID),
            Seq=0,
        )
        db.add(value)
    return value


def add_my_tag(db: Any, value_row: Any, content_id: str) -> bool:
    """Associate a track with a tag value when absent. True when it inserted."""
    from uuid import uuid4

    from pyrekordbox.db6 import tables

    existing = db.get_my_tag_songs(
        MyTagID=str(value_row.ID), ContentID=str(content_id)
    ).first()
    if existing is not None:
        return False
    db.add(
        tables.DjmdSongMyTag.create(
            ID=db.generate_unused_id(tables.DjmdSongMyTag),
            UUID=str(uuid4()),
            MyTagID=str(value_row.ID),
            ContentID=str(content_id),
            TrackNo=0,
        )
    )
    return True


# ---------------------------------------------------------------------------
# The additive whitelist
# ---------------------------------------------------------------------------

#: The content table, named once so the judge and the registry cannot disagree.
CONTENT_TABLE = "djmdContent"

#: The lookup tables a landing links a row's artist, album and genre to (U163).
ARTIST_TABLE = "djmdArtist"
ALBUM_TABLE = "djmdAlbum"
GENRE_TABLE = "djmdGenre"
LOOKUP_TABLES: tuple[str, ...] = (ARTIST_TABLE, ALBUM_TABLE, GENRE_TABLE)

#: Tables a writer may CREATE rows in. ANY unlisted table is refused, so grid and analysis
#: rows are structurally impossible (R17). Static, never feature-derived. THE CONTENT TABLE
#: STAYS OUT: only the native landing creates one, by naming it in ``creations`` (R-746).
PERMITTED_ROW_TABLES = frozenset(
    {"djmdPlaylist", "djmdSongPlaylist", "djmdMyTag", "djmdSongMyTag", "djmdKey"}
)

#: ``djmdKey`` is TOLERATED (A4): rekordbox left an external key row untouched. Create and
#: link in the SAME session (rekordbox collects unreferenced lookup rows), and resolve a
#: duplicate ``ScaleName`` first under the lock. A CEILING, NOT A LICENCE: Phillip decided
#: the writer never authors a key value, so the two answers stay comparable.

#: Analysis columns a row THIS PRODUCT CREATES may never declare (W3). An honest list, not a
#: derivation (P4); a test holds every name to a real content column.
GRIDLESS_ON_CREATE_COLUMNS = frozenset(
    {
        "BPM",
        "Analysed",
        "AnalysisDataPath",
        "AnalysisUpdated",
        "CueUpdated",
    }
)

#: What a CONTENT row this product creates must leave for rekordbox's analysis to fill (A8):
#: the five above, the key (never authored), the sample and rate columns, and the artwork.
#: The same honest list and schema test.
CONTENT_ROW_EMPTY_COLUMNS = GRIDLESS_ON_CREATE_COLUMNS | frozenset(
    {
        "KeyID",
        "SampleRate",
        "BitRate",
        "BitDepth",
        "ImagePath",
    }
)

#: What rekordbox writes on every content row it makes and ``add_content`` leaves NULL
#: (R-923); without them a row will not load to a deck. EVERY VALUE IS THE COLUMN'S OWN
#: EMPTY, so a later fill-if-empty still reads it unset. None is an analysis column.
#: Measured, not derived, and held to real column names by the schema test.
CONTENT_ROW_DEFAULTS: Mapping[str, Any] = MappingProxyType(
    {
        "Rating": 0,
        "ColorID": "0",
        "DJPlayCount": 0,
        "DiscNo": 0,
        "DeliveryControl": "on",
        "SamplerTrackInfo": 0,
        "SamplerPlayOffset": 0,
        "SamplerGain": 0.0,
        "VideoAssociate": "0",
        "LyricStatus": 0,
        "ServiceID": 0,
        "ExtInfo": "null",
        "FileNameS": "",
        "Commnt": "",
        "Subtitle": "",
        "ReleaseDate": "",
        "ModifiedByRBM": "",
        "DeliveryComment": "",
        "Lyricist": "",
        "OrgFolderPath": "",
        "Reserved1": "",
    }
)

#: The tables an analysis pass writes rows into FOR a content row. A row this product creates
#: owns none, read from SQL before its commit.
CONTENT_ANALYSIS_TABLES: tuple[str, ...] = ("djmdCue", "djmdMixerParam", "contentFile")

#: Tables a commit may be ASKED to admit a CREATION in beyond the whitelist, and the whole of
#: them, by ``creations`` on one commit so every other writer keeps refusing them. Naming any
#: other table refuses. The content row still carries :data:`CONTENT_ROW_EMPTY_COLUMNS`,
#: judged in memory and from SQL. The lookup tables joined with U163 (R-921), minted only
#: for a word with no active row and linked in the same commit (A4).
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES})

#: rekordbox's soft-delete marker, named once so a reader is BOUND to it through the import
#: graph. Naming it does NOT make it readable permissively; see
#: ``tests/_source_guards.py:permissive_soft_delete_reads``.
SOFT_DELETE_COLUMN = "rb_local_deleted"

#: The membership table, named once for the removal rule and its primitive.
MEMBERSHIP_TABLE = "djmdSongPlaylist"

#: The playlist and folder table, named once for the node removal (U111).
PLAYLIST_TABLE = "djmdPlaylist"

#: Tables a commit may be ASKED to admit a removal (a soft delete marker change) in, and the
#: whole of them, by ``removals``; naming another table refuses. A hard delete is only by
#: ``deletions`` (U288). The playlist table joined with U111, guarded by
#: :func:`remove_playlist_node` and :func:`assert_node_changes_confined`. Never content.
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})

# ---------------------------------------------------------------------------
# A track taken out of the collection, as rekordbox takes it out (U288)
# ---------------------------------------------------------------------------

#: The tables rekordbox's own Remove from Collection deletes a track's rows from OUTRIGHT,
#: content first (A178, A185); admitted only by ``deletions`` (U288). Not done here: the
#: orphaned artist and album rows, and the analysis folder.
COLLECTION_REMOVAL_TABLES: tuple[str, ...] = (
    CONTENT_TABLE,
    MEMBERSHIP_TABLE,
    "djmdCue",
    "contentCue",
    "contentFile",
    "djmdSongHistory",
    "djmdMixerParam",
)

#: The same tables as a set: what ``deletions`` may name. Static.
DELETABLE_TABLES = frozenset(COLLECTION_REMOVAL_TABLES)

#: The column a row of another table names a content row by.
CONTENT_REFERENCE_COLUMN = "ContentID"

#: The column a few tables name ANY row by (``imageFile``), asked too. ``uuidIDMap`` names
#: rows by ``CurrentID`` and is not asked.
TARGET_REFERENCE_COLUMN = "TargetID"

#: The registry row whose counter the binding advances at every commit.
LOCAL_UPDATE_COUNT = "localUpdateCount"

#: A membership row's position and its playlist reference, for the renumbering (R-1830).
TRACK_NUMBER_COLUMN = "TrackNo"
PLAYLIST_REFERENCE_COLUMN = "PlaylistID"

#: The session record key naming the rows a removal took out: a hard delete leaves no
#: marker for the deletion pass (R-1037).
RECORDED_REMOVALS_KEY = "collection_removed"

#: The collection row's columns a recorded removal keeps, read before the delete.
RECORDED_COLUMNS: tuple[str, ...] = (
    "ID",
    "FolderPath",
    "FileSize",
    "ArtistName",
    "Title",
    "ISRC",
    "RemixerName",
    "Subtitle",
)


#: What a node change may move on a playlist row it does not plan: a sibling's position.
_SIBLING_COLUMNS = frozenset({"Seq", "updated_at", "usn", "rb_local_usn"})

#: What a planned move may change on its own row.
_MOVED_COLUMNS = _SIBLING_COLUMNS | {"ParentID"}

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


class Ownership(StrEnum):
    """How strongly an operation owns a field: ``OWNED`` overwrites, ``FILL_IF_EMPTY`` spares a set value."""

    OWNED = "owned"
    FILL_IF_EMPTY = "fill_if_empty"


@dataclass(frozen=True, slots=True)
class FieldPolicy:
    """One operation's declared fields, and how strongly it owns each.

    Operations register themselves, so the writable set is the union of what is enabled (R14).
    """

    owner: str
    fields: Mapping[str, Ownership]


#: The baseline operation, the track colour write, so the guard is strict rather than vacuous.
TRACK_COLOR_POLICY = FieldPolicy(
    owner="track-color",
    fields=MappingProxyType({"ColorID": Ownership.OWNED}),
)

#: The repair of a row a landing created without rekordbox's defaults (R-923), registered by
#: it alone. FILL IF EMPTY with the column's own empty, so a set colour or rating is kept.
ROW_DEFAULTS_POLICY = FieldPolicy(
    owner="row-defaults",
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.FILL_IF_EMPTY)),
)

#: The column rekordbox keys a row's file by: THE FILE'S INODE AT IMPORT (U115, R-928). It
#: need not match today, but the binding's random 28 bit id never loads to a deck. NOT A
#: BOOKKEEPING COLUMN, which would blind the guard for every writer.
FILE_ID_COLUMN = "rb_file_id"

#: The upper bound of the binding's random id; past it, magnitude cannot tell random from stale.
BINDING_ID_LIMIT = 1 << 28

#: The repair of a row the binding gave a random file id (U115), registered by it alone.
#: OWNED: the value replaced is the binding's, never a person's.
FILE_ID_POLICY = FieldPolicy(
    owner="row-file-id",
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.OWNED}),
)

#: The full path of the row's audio file.
FOLDER_PATH_COLUMN = "FolderPath"

#: The one write that moves a row's file (U154, ``intake shelve``), registered by it alone,
#: since a path write is how a row points at nothing. OWNED: the file is renamed first.
SHELVE_POLICY = FieldPolicy(
    owner="shelve",
    fields=MappingProxyType({FOLDER_PATH_COLUMN: Ownership.OWNED}),
)

#: Set by ``add_content`` from the TRACK menu item and to one value by rekordbox, meaning
#: unknown (A32, R-928). NOT A BOOKKEEPING COLUMN; the probe owns it for its one commit.
CONTENT_LINK_COLUMN = "ContentLink"

#: The recording code: rekordbox stores empty text where the binding leaves NULL (A32).
ISRC_COLUMN = "ISRC"

#: THE COLUMNS THE ROW PROBE MAY WRITE, with each stored type (A32, R-928). ``AnalysisUpdated``
#: also differs but is an analysis column (R17), never written. Neither is bookkeeping.
ROW_PROBE_COLUMNS: Mapping[str, type] = MappingProxyType(
    {CONTENT_LINK_COLUMN: int, ISRC_COLUMN: str}
)

#: The owner a row probe registers its policy under.
ROW_PROBE_OWNER = "row-probe"


def row_probe_policy(columns: Iterable[str]) -> FieldPolicy:
    """The policy one probe commit registers: exactly the probe columns it writes, OWNED.

    Refuses a column outside :data:`ROW_PROBE_COLUMNS` with ``ValueError``.
    """
    wanted = set(columns)
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if outside:
        raise ValueError(f"not a row probe column: {sorted(outside)}")
    return FieldPolicy(
        owner=ROW_PROBE_OWNER,
        fields=MappingProxyType(dict.fromkeys(sorted(wanted), Ownership.OWNED)),
    )


_REGISTERED: dict[str, FieldPolicy] = {}


def register_field_policy(policy: FieldPolicy) -> None:
    """Declare one operation's fields; an unregistered operation writes nothing."""
    _REGISTERED[policy.owner] = policy


def reset_field_policies() -> None:
    """Return the registry to its baseline. For tests, and for a re-enabled profile."""
    _REGISTERED.clear()
    register_field_policy(TRACK_COLOR_POLICY)


def registered_field_policies() -> Mapping[str, FieldPolicy]:
    """Every operation currently permitted to write a content column."""
    return MappingProxyType(dict(_REGISTERED))


def content_writable_columns() -> frozenset[str]:
    """The union of every registered operation's declared fields, walked, never listed (P3)."""
    columns: set[str] = set()
    for policy in _REGISTERED.values():
        columns.update(policy.fields)
    return frozenset(columns)


reset_field_policies()


@contextmanager
def field_policies_for_commit(*policies: FieldPolicy) -> Iterator[None]:
    """Register the named policies for one commit, then restore the registry as it was (A32).

    A registration left behind would widen the guard for every later writer.
    """
    was = registered_field_policies()
    try:
        for policy in policies:
            register_field_policy(policy)
        yield
    finally:
        reset_field_policies()
        for policy in was.values():
            register_field_policy(policy)


def guard_violations(
    new: Iterable[tuple[str, Iterable[str]]],
    dirty: Iterable[tuple[str, Iterable[str]]],
    deleted: Iterable[str],
    *,
    content_columns: Iterable[str] | None = None,
    removals: Iterable[str] = (),
    creations: Iterable[str] = (),
    deletions: Iterable[str] = (),
) -> list[str]:
    """Judge a pending session against the whitelist. Empty means allowed.

    ``removals`` (soft deletes), ``creations`` (beyond the whitelist, R-746) and
    ``deletions`` (hard deletes, U288) name the tables this one commit admits,
    each empty for every writer but its one; a name outside
    :data:`REMOVABLE_TABLES`, :data:`ADMITTABLE_ROW_TABLES` or
    :data:`DELETABLE_TABLES` is itself a violation. An admitted content row is
    still judged against :data:`CONTENT_ROW_EMPTY_COLUMNS`; which rows a hard
    delete takes is judged from SQL by :func:`assert_collection_removal_confined`.
    PURE, so every branch is tested with literals. Returns EVERY violation.
    """
    writable = (
        frozenset(content_columns)
        if content_columns is not None
        else content_writable_columns()
    )
    violations: list[str] = []
    admitted = frozenset(removals)
    for table in sorted(admitted - REMOVABLE_TABLES):
        violations.append(
            f"asks to remove rows in {table!r}, and a removal is admitted in "
            f"{sorted(REMOVABLE_TABLES)} and nowhere else"
        )
    admitted &= REMOVABLE_TABLES
    creatable = frozenset(creations)
    for table in sorted(creatable - ADMITTABLE_ROW_TABLES):
        violations.append(
            f"asks to create rows in {table!r}, and a creation beyond the "
            f"whitelist is admitted in {sorted(ADMITTABLE_ROW_TABLES)} and nowhere else"
        )
    creatable &= ADMITTABLE_ROW_TABLES
    deletable = frozenset(deletions)
    for table in sorted(deletable - DELETABLE_TABLES):
        violations.append(
            f"asks to delete rows in {table!r}, and a delete is admitted in "
            f"{sorted(DELETABLE_TABLES)} and nowhere else"
        )
    deletable &= DELETABLE_TABLES

    for table, columns in new:
        if table == CONTENT_TABLE and table in creatable:
            # THE ONE ADMISSION (R-746), judged again from SQL in
            # ``assert_created_rows_are_gridless``.
            declared = {column for column in columns if column in CONTENT_ROW_EMPTY_COLUMNS}
            if declared:
                violations.append(
                    f"creates a {CONTENT_TABLE} row declaring analysis column(s): "
                    f"{sorted(declared)}; a row this product creates carries what "
                    f"the file says and rekordbox derives the rest from the audio"
                )
            continue
        if table in LOOKUP_TABLES and table in creatable:
            # U163: a minted lookup row is judged as any other creation.
            declared = {column for column in columns if column in GRIDLESS_ON_CREATE_COLUMNS}
            if declared:
                violations.append(
                    f"creates a row in {table!r} declaring analysis column(s): "
                    f"{sorted(declared)}; a row this product creates is gridless and "
                    f"rekordbox derives the grid from the audio"
                )
            continue
        if table == CONTENT_TABLE:
            violations.append(
                f"creates a {CONTENT_TABLE} row; only a landing whose commit admits "
                f"one by name may, and an import in the XML bridge is what every "
                f"other intake performs"
            )
            continue
        if table not in PERMITTED_ROW_TABLES:
            violations.append(f"creates a row in the non-whitelisted table {table!r}")
            continue
        # W3: a creation's columns are judged, not only its table.
        declared = {column for column in columns if column in GRIDLESS_ON_CREATE_COLUMNS}
        if declared:
            violations.append(
                f"creates a row in {table!r} declaring analysis column(s): "
                f"{sorted(declared)}; a row this product creates is gridless and "
                f"rekordbox derives the grid from the audio"
            )

    for table, columns in dirty:
        columns = set(columns)
        # THE MARKER IS JUDGED BEFORE THE BOOKKEEPING FILTER DROPS IT (R-758).
        if SOFT_DELETE_COLUMN in columns and table not in admitted:
            violations.append(
                f"changes the soft delete marker of a row in {table!r}, which "
                f"removes it; writers are additive-only and this commit admits "
                f"no removal there"
            )
        modified = {column for column in columns if column not in BOOKKEEPING_COLUMNS}
        if not modified:
            continue
        if table == CONTENT_TABLE:
            forbidden = modified - writable
            if forbidden:
                violations.append(
                    f"modifies non-whitelisted {CONTENT_TABLE} column(s): {sorted(forbidden)}"
                )
        elif table not in PERMITTED_ROW_TABLES:
            violations.append(
                f"modifies the non-whitelisted table {table!r}: {sorted(modified)}"
            )

    for table in deleted:
        # Additive only keeps the snapshot a real safety net: a deletion's damage is
        # invisible. The soft delete arrives as a modification. THE ONE HARD DELETE
        # (U288) is admitted only by ``deletions`` and judged from SQL before commit.
        if table in deletable:
            continue
        violations.append(f"deletes a row in {table!r}; writers are additive-only")

    return violations


#: Reported for an uninspectable object; outside every writable set, so it refuses.
UNINSPECTABLE = "<uninspectable>"

#: Reported for a re-parented row. Not an empty set, which would read as bookkeeping only:
#: it passes on a whitelisted table and refuses elsewhere.
MOVED = "<moved>"


def clear_registry_buffer() -> None:
    """Empty the binding's process-wide update buffer when a write session opens.

    The guard DEPENDS on the buffer describing this session only, so it is asserted here.
    """
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to clear
        return
    RekordboxAgentRegistry.clear_buffer()


def _table_of(obj: Any) -> str | None:
    table = getattr(obj, "__table__", None)
    return getattr(table, "name", None)


def _columns_of(obj: Any) -> set[str]:
    """The columns an EXISTING object reports as changed. Fails closed."""
    from sqlalchemy import inspect as sa_inspect

    try:
        return {
            attribute.key
            for attribute in sa_inspect(obj).attrs
            if attribute.history.has_changes()
        }
    except Exception:  # noqa: BLE001 - un-inspectable means treat as all-changed
        return {UNINSPECTABLE}


def _declared_columns(obj: Any) -> set[str]:
    """The columns a NOT YET FLUSHED object carries a value for. Fails closed.

    Read from the instance dictionary, never the mapper: a failed mapper
    configuration on a transient instance is CACHED process-wide.
    """
    table = getattr(obj, "__table__", None)
    if table is None:
        return {UNINSPECTABLE}
    names = {column.name for column in table.columns}
    try:
        state = vars(obj)
    except TypeError:  # no instance dictionary to read
        return {UNINSPECTABLE}
    return {key for key, value in state.items() if key in names and value is not None}


def _session_changes(
    session: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """Adapt an object-mapper session into the judge's inputs, keyed by instance.

    FAILS CLOSED with a placeholder column. NOT SUFFICIENT ON ITS OWN (W2): any
    flush, including autoflush before a query, empties ``new`` and ``dirty``.
    Keyed by ``id(instance)`` so the union with the registry buffer merges.
    """
    created = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _declared_columns(obj)) for obj in session.new
    }
    modified = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _columns_of(obj)) for obj in session.dirty
    }
    removed = {id(obj): (_table_of(obj) or UNINSPECTABLE) for obj in session.deleted}
    return created, modified, removed


def _buffer_entries(db: Any) -> list[tuple[Any, str | None, str, list[Any]]]:
    """ONE walk of the binding's update buffer, as ``(entry, op, key, instances)``.

    ``op`` None marks a shape not understood, which readers refuse. Empty without
    a handle (see :func:`_registry_changes`) or without the binding.
    """
    if db is None:
        return []
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to read
        return []
    walked: list[tuple[Any, str | None, str, list[Any]]] = []
    for entry in list(getattr(RekordboxAgentRegistry, "__update_sequence__", [])):
        try:
            target, op, key, _value = entry
        except (TypeError, ValueError):  # a shape this code does not understand
            walked.append((entry, None, "", []))
            continue
        instances = list(target) if isinstance(target, (list, tuple)) else [target]
        walked.append((entry, str(op), str(key) if key else "", instances))
    return walked


def _registry_changes(
    db: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """The same judgement inputs, read from the binding's own update buffer.

    The buffer is NOT emptied by a flush, which fixes W2, but the binding skips
    tracking for some internal operations and a raw ``session.add``, so the guard
    reads the UNION (P4). Runs no query. SCOPED TO A HANDLE: the buffer is
    process wide, and read without one it refused a legitimate write (P7).
    """
    created: dict[int, tuple[str, set[str]]] = {}
    modified: dict[int, tuple[str, set[str]]] = {}
    removed: dict[int, str] = {}

    for entry, op, key, instances in _buffer_entries(db):
        if op is None:
            # A shape this code does not understand refuses.
            modified[id(entry)] = (UNINSPECTABLE, {UNINSPECTABLE})
            continue
        for obj in instances:
            table = _table_of(obj)
            if table is None:
                modified[id(obj)] = (UNINSPECTABLE, {UNINSPECTABLE})
            elif op == "create":
                created[id(obj)] = (table, _declared_columns(obj))
            elif op == "update":
                seen = modified.get(id(obj))
                columns = set(seen[1]) if seen else set()
                columns.add(key if key else UNINSPECTABLE)
                modified[id(obj)] = (table, columns)
            elif op == "delete":
                removed[id(obj)] = table
            elif op == "move":
                modified[id(obj)] = (table, {MOVED})
            else:
                # An unknown operation refuses, so a future binding op fails loudly.
                modified[id(obj)] = (table, {UNINSPECTABLE})
    return created, modified, removed


def pending_changes(
    session: Any, db: Any = None
) -> tuple[list[tuple[str, set[str]]], list[tuple[str, set[str]]], list[str]]:
    """Everything this session will write, from BOTH sources, unioned; creation beats modification."""
    s_created, s_modified, s_removed = _session_changes(session)
    r_created, r_modified, r_removed = _registry_changes(db)

    created = {**r_created, **s_created}

    modified: dict[int, tuple[str, set[str]]] = {}
    for source in (r_modified, s_modified):
        for key, (table, columns) in source.items():
            seen = modified.get(key)
            modified[key] = (table, (set(seen[1]) if seen else set()) | set(columns))

    for key in created:
        modified.pop(key, None)

    removed = {**r_removed, **s_removed}

    return list(created.values()), list(modified.values()), list(removed.values())


def pending_objects(session: Any, db: Any = None) -> list[tuple[Any, str, frozenset[str]]]:
    """Every object this session will write, with ``create``, ``modify`` or ``delete`` and its columns.

    :func:`pending_changes`'s two sources kept as OBJECTS, for a guard asking which
    rows (U185). Shapes the buffer reader does not understand are left to the whitelist.
    """
    found: dict[int, tuple[Any, str, set[str]]] = {}

    def note(obj: Any, op: str, columns: Iterable[str]) -> None:
        seen = found.get(id(obj))
        if seen is not None and seen[1] == "create":
            return
        if seen is not None and op == "modify" and seen[1] == "modify":
            found[id(obj)] = (obj, op, seen[2] | set(columns))
            return
        found[id(obj)] = (obj, op, set(columns))

    for _entry, op, key, instances in _buffer_entries(db):
        for obj in instances:
            if op == "create":
                note(obj, "create", _declared_columns(obj))
            elif op == "delete":
                note(obj, "delete", ())
            elif op == "update":
                note(obj, "modify", (key or UNINSPECTABLE,))
            elif op == "move":
                note(obj, "modify", (MOVED,))
    if session is not None:
        for obj in list(getattr(session, "new", ())):
            note(obj, "create", _declared_columns(obj))
        for obj in list(getattr(session, "dirty", ())):
            note(obj, "modify", _columns_of(obj))
        for obj in list(getattr(session, "deleted", ())):
            note(obj, "delete", ())
    return [(obj, op, frozenset(columns)) for obj, op, columns in found.values()]


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


def _registry_created_instances(db: Any) -> dict[int, Any]:
    """The INSTANCES the binding's buffer records a creation for, keyed by identity, for the SQL read back."""
    found: dict[int, Any] = {}
    for _entry, op, _key, instances in _buffer_entries(db):
        if op != "create":
            continue
        for obj in instances:
            found[id(obj)] = obj
    return found


#: Every spelling of "nobody wrote this" for a column an analysis pass fills. PUBLIC, so the
#: landing's read back uses the same notion of empty as the guard.
EMPTY_ON_CREATE: tuple[Any, ...] = (None, 0, 0.0, "", "0")


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
# Per-field metadata policy: the semantic gate above the structural one
# ---------------------------------------------------------------------------


class Decision(StrEnum):
    """What the per-field policy says about one proposed write."""

    WRITE = "write"
    SKIP_SAME = "skip_same"
    SKIP_PRESENT = "skip_present"
    SKIP_UNOWNED = "skip_unowned"


#: What "unset" means per column for fill-if-empty. An honest list, not a derivation (P4);
#: anything unnamed uses the two shared spellings.
FIELD_EMPTIES: Mapping[str, tuple[Any, ...]] = MappingProxyType(
    {
        "Title": (None, ""),
        "Rating": (None, "", 0, "0"),
        "GenreID": (None, "", 0, "0"),
        "KeyID": (None, "", 0, "0"),
        "ColorID": (None, "", 0, "0"),
    }
)

_DEFAULT_EMPTIES: tuple[Any, ...] = (None, "")


def metadata_decision(
    owner: str,
    field_name: str,
    current: Any,
    new: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Decide one field write. Pure.

    CLOSED BY CONSTRUCTION: an unregistered operation or undeclared field writes nothing.
    """
    table = policies if policies is not None else _REGISTERED
    policy = table.get(owner)
    mode = None if policy is None else policy.fields.get(field_name)
    if mode is None:
        return Decision.SKIP_UNOWNED
    if str(current) == str(new):
        return Decision.SKIP_SAME  # idempotent: re-running a run is a no-op
    if mode is Ownership.OWNED:
        return Decision.WRITE
    empties = FIELD_EMPTIES.get(field_name, _DEFAULT_EMPTIES)
    return Decision.WRITE if current in empties else Decision.SKIP_PRESENT


def write_metadata_field(
    row: Any,
    owner: str,
    field_name: str,
    new_value: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Apply the per-field policy to one existing row and report what happened. Does not commit."""
    current = getattr(row, field_name, None)
    decision = metadata_decision(owner, field_name, current, new_value, policies=policies)
    if decision is Decision.WRITE:
        setattr(row, field_name, new_value)
    return decision


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


# The collection removal's own reads and checks (U288)


def _tables(session: Any) -> tuple[str, ...]:
    from sqlalchemy import text

    rows = session.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")
    ).fetchall()
    return tuple(str(row[0]) for row in rows if not str(row[0]).startswith("sqlite_"))


def _columns(session: Any, table: str) -> tuple[tuple[str, int], ...]:
    """Each column's name and its place in the primary key (0 when it is not in it)."""
    from sqlalchemy import text

    return tuple(
        (str(row[1]), int(row[5] or 0))
        for row in session.execute(text(f'PRAGMA table_info("{table}")')).fetchall()
    )


def content_references(db: Any, content_ids: Iterable[str]) -> dict[str, dict[str, int]]:
    """Every row naming one of ``content_ids`` in a table the removal does NOT delete from.

    From SQL over every table, by ``ContentID`` and by ``TargetID`` where present,
    so an unmapped table is asked too (``uuidIDMap``'s ``CurrentID`` is not).
    ``{content id: {table: rows}}``. A table A178 and A185 did not measure may
    hold a row rekordbox deletes or keeps, so the caller refuses rather than guesses.
    """
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    found: dict[str, dict[str, int]] = {}
    if not wanted:
        return found
    session = db.session
    for table in _tables(session):
        if table in DELETABLE_TABLES:
            continue
        names = {name for name, _pk in _columns(session, table)}
        asked = [CONTENT_REFERENCE_COLUMN] if CONTENT_REFERENCE_COLUMN in names else []
        if TARGET_REFERENCE_COLUMN in names:
            asked.append(TARGET_REFERENCE_COLUMN)
        for column in asked:
            statement = text(
                f'SELECT {column}, COUNT(*) FROM "{table}" '
                f"WHERE {column} IN :ids GROUP BY {column}"
            ).bindparams(bindparam("ids", expanding=True))
            for content_id, count in session.execute(statement, {"ids": wanted}).fetchall():
                held = found.setdefault(str(content_id), {})
                held[table] = held.get(table, 0) + int(count)
    return found


def _mapped(table: str) -> Any:
    from pyrekordbox.db6 import tables

    for mapper in tables.Base.registry.mappers:
        if getattr(mapper.class_, "__tablename__", None) == table:
            return mapper.class_
    raise _unavailable(
        "whitelist-violation",
        f"the binding maps no class for {table!r}, so a track's rows there cannot be "
        f"deleted through it; nothing was written",
        detail={"table": table},
    )


def database_id(db: Any) -> str | None:
    """rekordbox's own ``DjmdProperty.DBID``, or None, binding a recorded removal to its database."""
    held = db.get_property()
    row = held.first() if hasattr(held, "first") else held
    identity = getattr(row, "DBID", None) if row is not None else None
    return str(identity) if identity else None


def recorded_columns(row: Any) -> dict[str, Any]:
    """One collection row's :data:`RECORDED_COLUMNS`, read off it before it is deleted."""
    found: dict[str, Any] = {}
    for name in RECORDED_COLUMNS:
        value = getattr(row, name, None)
        found[name] = value if value is None or isinstance(value, (int, float)) else str(value)
    return found


def remove_from_collection(db: Any, content_id: str) -> dict[str, tuple[str, ...]]:
    """Delete one live track's every row in :data:`COLLECTION_REMOVAL_TABLES`. Returns them by table.

    THE ONE HARD DELETE THIS PRODUCT MAKES, and it is rekordbox's own (A178,
    A185): the content row and every row naming it in six tables, outright,
    playlist and history list rows left. Following members are renumbered by
    :class:`CollectionRemoval` (R-1830); history is not. THROUGH THE BINDING'S
    OWN DELETE, children first, so the whitelist sees each row. REFUSED, WITH
    NOTHING DELETED: no live row, or a row named outside the removal set
    (:func:`content_references`). DOES NOT COMMIT: the caller commits with
    ``deletions`` after :func:`assert_collection_removal_confined`.
    """
    key = str(content_id)
    content_class = _mapped(CONTENT_TABLE)
    row = db.session.get(content_class, key)
    if row is None or soft_deleted(
        row,
        message=(
            f"the collection row {key!r} cannot say whether rekordbox removed it, and "
            f"deleting it as live could take a track out twice"
        ),
        origin=("rb_writer",),
        detail={"content_id": key},
    ):
        raise _unavailable(
            "whitelist-violation",
            f"asked to take the collection row {key!r} out of the collection, and the "
            f"database holds no live row of that id; nothing was written",
            detail={"content_id": key},
        )
    held = content_references(db, (key,)).get(key, {})
    if held:
        named = ", ".join(f"{table} ({count})" for table, count in sorted(held.items()))
        raise _unavailable(
            "whitelist-violation",
            f"the collection row {key!r} is named by rows in {named}, which "
            f"rekordbox's Remove from Collection was never measured on, so what it "
            f"would do with them is not known; nothing was written",
            detail={"content_id": key, "tables": dict(sorted(held.items()))},
        )
    deleted: dict[str, tuple[str, ...]] = {}
    for table in COLLECTION_REMOVAL_TABLES[1:]:
        mapped = _mapped(table)
        found = list(
            db.session.query(mapped).filter(getattr(mapped, CONTENT_REFERENCE_COLUMN) == key)
        )
        for child in found:
            db.delete(child)
        deleted[table] = tuple(sorted(str(child.ID) for child in found))
    db.delete(row)
    deleted[CONTENT_TABLE] = (key,)
    return {table: deleted[table] for table in COLLECTION_REMOVAL_TABLES}


def renumbered_positions(
    memberships: Iterable[tuple[str, str, str, int | None, bool]],
    removed: Iterable[str],
) -> dict[str, tuple[str, int, int]]:
    """Which membership rows a removal renumbers, and to what. PURE (R-1830).

    ``memberships`` holds ``(membership id, playlist id, content id, TrackNo,
    live)``; returns ``{membership id: (playlist id, TrackNo now, TrackNo after)}``
    for rows that move. Measured (A197): each surviving LIVE row above a removed
    live row drops by one per such row below it, the binding's rule without its
    self-committing call. ONLY LIVE ROWS COUNT AND ONLY LIVE ROWS MOVE, or a
    marked row sharing a number would put two live rows on one place. A row with
    no number or an unreadable marker is neither lowered nor counted.
    """
    rows = [
        (str(key), str(playlist), str(content), number, bool(live))
        for key, playlist, content, number, live in memberships
    ]
    gone = {str(one) for one in removed}
    deleted: dict[str, list[int]] = {}
    for _key, playlist, content, number, live in rows:
        if content in gone and live and number is not None:
            deleted.setdefault(playlist, []).append(int(number))
    moved: dict[str, tuple[str, int, int]] = {}
    for key, playlist, content, number, live in rows:
        if content in gone or not live or number is None:
            continue
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
        if below:
            moved[key] = (playlist, int(number), int(number) - below)
    return moved


def removal_renumbering(db: Any, content_ids: Iterable[str]) -> dict[str, tuple[str, int, int]]:
    """The membership rows removing ``content_ids`` would renumber, read from SQL (R-1830).

    Asked on a read only copy for the plan's count and again on the write handle by
    :meth:`CollectionRemoval.prepare`. Reads and writes nothing else.
    """
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    if not wanted:
        return {}
    statement = text(
        f'SELECT "ID", "{PLAYLIST_REFERENCE_COLUMN}", "{CONTENT_REFERENCE_COLUMN}", '
        f'"{TRACK_NUMBER_COLUMN}", "{SOFT_DELETE_COLUMN}" FROM "{MEMBERSHIP_TABLE}" '
        f'WHERE "{PLAYLIST_REFERENCE_COLUMN}" IN (SELECT "{PLAYLIST_REFERENCE_COLUMN}" '
        f'FROM "{MEMBERSHIP_TABLE}" WHERE "{CONTENT_REFERENCE_COLUMN}" IN :ids)'
    ).bindparams(bindparam("ids", expanding=True))
    rows = db.session.execute(statement, {"ids": wanted}).fetchall()
    unreadable = sorted(str(row[0]) for row in rows if row[4] is None)
    if unreadable:
        # REFUSED, AS :func:`soft_deleted` REFUSES: other readers take NULL as live.
        raise refuse(
            "soft-delete-marker-unreadable",
            f"{len(unreadable)} playlist membership row(s) in a playlist this removal "
            f"would renumber cannot say whether rekordbox removed them, so where the "
            f"tracks after the removed one belong cannot be said; nothing was written",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("rb_writer",),
            detail={"membership_ids": unreadable[:20], "column": SOFT_DELETE_COLUMN},
        )
    return renumbered_positions(
        ((row[0], row[1], row[2], None if row[3] is None else int(row[3]), _live(row[4])) for row in rows),
        wanted,
    )


def _live(marker: Any) -> bool:
    """Whether a membership row's soft delete marker reads live; unreadable reads not live."""
    return marker is not None and not bool(marker)


def renumber_memberships(db: Any, moved: Mapping[str, tuple[str, int, int]]) -> None:
    """Write each planned ``TrackNo``, that one column and nothing else, inside the open transaction.

    ONE SQL UPDATE PER ROW, since rekordbox stamped nothing else (A197). Each names
    the planned old number, so a row that moved refuses and the handle rolls back.
    Held objects are expired. DOES NOT COMMIT.
    """
    from sqlalchemy import text

    statement = text(
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after '
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
    )
    session = db.session
    for key, (_playlist, before, after) in sorted(moved.items()):
        result = session.execute(statement, {"after": after, "key": key, "before": before})
        if result.rowcount != 1:
            db.rollback()
            raise _unavailable(
                "whitelist-violation",
                f"the playlist membership {key!r} no longer holds the place {before} the "
                f"removal planned to renumber from, so its renumbering was not written and "
                f"nothing was committed",
                detail={"membership_id": key, "planned": before},
            )
    for held in list(session.identity_map.values()):
        if _table_of(held) == MEMBERSHIP_TABLE and str(getattr(held, "ID", "")) in moved:
            session.expire(held)


@dataclass(frozen=True)
class DatabaseReading:
    """Every table of the database as it stands, row by row, read from SQL.

    ``rows``: per table, primary key (or ``rowid``) to a row digest. ``named``:
    for :data:`DELETABLE_TABLES`, the content row each names. ``counter``:
    ``localUpdateCount`` or None. ``positions``: per membership row its playlist,
    content, ``TrackNo``, liveness and a digest of the rest (R-1830).
    """

    rows: Mapping[str, Mapping[str, str]]
    named: Mapping[str, Mapping[str, str]]
    counter: int | None
    positions: Mapping[str, tuple[str, str, int | None, bool, str]] = field(default_factory=dict)


def database_reading(db: Any) -> DatabaseReading:
    """Read every table from SQL. Flushes nothing itself, as :func:`node_tables` does not."""
    import hashlib

    from sqlalchemy import text

    session = db.session
    rows: dict[str, dict[str, str]] = {}
    named: dict[str, dict[str, str]] = {}
    positions: dict[str, tuple[str, str, int | None, bool, str]] = {}
    for table in _tables(session):
        columns = _columns(session, table)
        keys = [name for name, place in sorted(columns, key=lambda one: one[1]) if place]
        names = [name for name, _place in columns]
        selected = ", ".join(f'"{name}"' for name in names)
        if keys:
            keyed = [names.index(name) for name in keys]
            result = session.execute(text(f'SELECT {selected} FROM "{table}"'))
        else:
            keyed = [len(names)]
            result = session.execute(text(f'SELECT {selected}, rowid FROM "{table}"'))
        reference = (
            names.index("ID")
            if table == CONTENT_TABLE
            else (names.index(CONTENT_REFERENCE_COLUMN) if CONTENT_REFERENCE_COLUMN in names else None)
        )
        placed = (
            (
                names.index(PLAYLIST_REFERENCE_COLUMN),
                names.index(CONTENT_REFERENCE_COLUMN),
                names.index(TRACK_NUMBER_COLUMN),
                names.index(SOFT_DELETE_COLUMN),
            )
            if table == MEMBERSHIP_TABLE
            and {
                PLAYLIST_REFERENCE_COLUMN,
                CONTENT_REFERENCE_COLUMN,
                TRACK_NUMBER_COLUMN,
                SOFT_DELETE_COLUMN,
            }
            <= set(names)
            else None
        )
        found: dict[str, str] = {}
        naming: dict[str, str] = {}
        for row in result:
            values = tuple(row)
            key = "|".join(str(values[at]) for at in keyed)
            found[key] = hashlib.sha256(repr(values[: len(names)]).encode("utf-8")).hexdigest()
            if table in DELETABLE_TABLES and reference is not None:
                naming[key] = str(values[reference])
            if placed is not None:
                playlist_at, content_at, number_at, marker_at = placed
                rest = tuple(
                    value for at, value in enumerate(values[: len(names)]) if at != number_at
                )
                number = values[number_at]
                positions[key] = (
                    str(values[playlist_at]),
                    str(values[content_at]),
                    None if number is None else int(number),
                    _live(values[marker_at]),
                    hashlib.sha256(repr(rest).encode("utf-8")).hexdigest(),
                )
        rows[table] = found
        if table in DELETABLE_TABLES:
            named[table] = naming
    counter = session.execute(
        text("SELECT int_1 FROM agentRegistry WHERE registry_id = :id"),
        {"id": LOCAL_UPDATE_COUNT},
    ).scalar() if "agentRegistry" in rows else None
    return DatabaseReading(rows, named, None if counter is None else int(counter), positions)


def collection_removal_violations(
    before: DatabaseReading,
    after: DatabaseReading,
    *,
    removed: Iterable[str],
    committed: bool = False,
) -> list[str]:
    """Every difference between two readings the planned removal does not explain.

    PURE. Empty means confined AND made. It explains only: rows gone from
    :data:`DELETABLE_TABLES` that named a ``removed`` row, EVERY such row gone and
    each removed row live before; no table or row added; no row changed but a
    planned renumbering to exactly :func:`renumbered_positions`'s number, every
    planned one made (R-1830); and with ``committed``, ``localUpdateCount``
    moving forward.
    """
    gone = {str(one) for one in removed}
    violations: list[str] = []
    planned = renumbered_positions(
        (
            (key, playlist, content, number, live)
            for key, (playlist, content, number, live, _rest) in before.positions.items()
        ),
        gone,
    )
    for table in sorted(set(before.rows) ^ set(after.rows)):
        violations.append(f"the table {table!r} appeared or disappeared")
    for content_id in sorted(gone):
        if content_id not in before.named.get(CONTENT_TABLE, {}):
            violations.append(f"the planned {CONTENT_TABLE} row {content_id!r} was not there")
    for table in sorted(set(before.rows) & set(after.rows)):
        old, new = before.rows[table], after.rows[table]
        for key in sorted(set(new) - set(old)):
            violations.append(f"an unplanned {table} row {key!r} was added")
        naming = before.named.get(table, {})
        for key in sorted(set(old) - set(new)):
            if table not in DELETABLE_TABLES or naming.get(key) not in gone:
                violations.append(f"the {table} row {key!r} disappeared, which no planned removal explains")
        for key in sorted(set(old) & set(new)):
            if table == MEMBERSHIP_TABLE and key in planned:
                violations.extend(_renumbering_violations(key, planned[key], before, after))
                continue
            if old[key] == new[key]:
                continue
            if committed and table == "agentRegistry" and key == LOCAL_UPDATE_COUNT:
                continue
            violations.append(f"the {table} row {key!r} changed, and a removal changes no row")
        for key, names in sorted(naming.items()):
            if names in gone and key in new:
                violations.append(
                    f"the {table} row {key!r} still names the removed {CONTENT_TABLE} row {names!r}"
                )
    if committed and (
        before.counter is None or after.counter is None or after.counter <= before.counter
    ):
        violations.append(
            f"{LOCAL_UPDATE_COUNT} did not move forward ({before.counter} to {after.counter})"
        )
    return violations


def _renumbering_violations(
    key: str,
    plan: tuple[str, int, int],
    before: DatabaseReading,
    after: DatabaseReading,
) -> list[str]:
    """What is wrong with one membership row the removal was to renumber, or nothing."""
    _playlist, was, wanted = plan
    then = before.positions.get(key)
    now = after.positions.get(key)
    if then is None or now is None:
        return [f"the {MEMBERSHIP_TABLE} row {key!r} could not be read for its renumbering"]
    found: list[str] = []
    if (now[0], now[1], now[3], now[4]) != (then[0], then[1], then[3], then[4]):
        found.append(
            f"the {MEMBERSHIP_TABLE} row {key!r} changed in a column other than "
            f"{TRACK_NUMBER_COLUMN}, and a renumbering moves that column alone"
        )
    if now[2] != wanted:
        found.append(
            f"the {MEMBERSHIP_TABLE} row {key!r} was to be renumbered from {was} to "
            f"{wanted} and holds {now[2]}"
        )
    return found


def assert_collection_removal_confined(
    db: Any, before: DatabaseReading, *, removed: Iterable[str]
) -> None:
    """Refuse, before the commit, a removal that reached anything it did not plan.

    FROM SQL after a deliberate flush, judging whose rows went and that nothing
    else moved, which the table-level whitelist cannot. A REFUSAL ROLLS BACK.
    """
    db.session.flush()
    violations = collection_removal_violations(before, database_reading(db), removed=removed)
    if violations:
        db.rollback()
        raise _unavailable(
            "whitelist-violation",
            "the removal from the collection reached rows it did not plan, or did not "
            "make one it planned, read from SQL before the commit:\n  - "
            + "\n  - ".join(violations[:20]),
            detail={"violations": violations},
        )


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
            columns[key] = recorded_columns(row)
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


__all__ = [
    "ADMITTABLE_ROW_TABLES",
    "BINDING_ID_LIMIT",
    "BOOKKEEPING_COLUMNS",
    "CONTENT_ANALYSIS_TABLES",
    "CONTENT_LINK_COLUMN",
    "CONTENT_ROW_DEFAULTS",
    "CONTENT_ROW_EMPTY_COLUMNS",
    "CONTENT_TABLE",
    "EMPTY_ON_CREATE",
    "CommitWitness",
    "ENV_APP_PATH",
    "FIELD_EMPTIES",
    "FILE_ID_COLUMN",
    "FOLDER_PATH_COLUMN",
    "SHELVE_POLICY",
    "FILE_ID_POLICY",
    "ISRC_COLUMN",
    "ROW_PROBE_COLUMNS",
    "ROW_PROBE_OWNER",
    "GRIDLESS_ON_CREATE_COLUMNS",
    "LIBRARY_SYNC_SETTING",
    "MASTER_PLAYLIST_XML",
    "MEMBERSHIP_TABLE",
    "NodeTables",
    "PERMITTED_ROW_TABLES",
    "PLAYLIST_TABLE",
    "REMOVABLE_TABLES",
    "COLLECTION_REMOVAL_TABLES",
    "CollectionRemoval",
    "TARGET_REFERENCE_COLUMN",
    "RECORDED_COLUMNS",
    "RECORDED_REMOVALS_KEY",
    "database_id",
    "recorded_columns",
    "CONTENT_REFERENCE_COLUMN",
    "DELETABLE_TABLES",
    "DatabaseReading",
    "LOCAL_UPDATE_COUNT",
    "assert_collection_removal_confined",
    "collection_removal_violations",
    "content_references",
    "database_reading",
    "remove_from_collection",
    "removal_renumbering",
    "renumber_memberships",
    "renumbered_positions",
    "PLAYLIST_REFERENCE_COLUMN",
    "TRACK_NUMBER_COLUMN",
    "ROW_DEFAULTS_POLICY",
    "ROOT_PARENT_SENTINELS",
    "SETTINGS_APP_DIRNAME",
    "SOFT_DELETE_COLUMN",
    "TEST_DB_ENV",
    "TEST_SETTINGS_ENV",
    "TRACK_COLOR_POLICY",
    "CloudSyncState",
    "CloudSyncVerdict",
    "Decision",
    "FieldPolicy",
    "Ownership",
    "RekordboxRunning",
    "RekordboxUnavailable",
    "RunStateVocabulary",
    "SQLITE_HEADER",
    "SharedRead",
    "add_membership",
    "add_memberships",
    "add_my_tag",
    "assert_app_version",
    "assert_foreign_untouched",
    "assert_binding_version",
    "assert_cloud_sync_readable",
    "assert_rekordbox_closed",
    "assert_schema_version",
    "assert_created_rows_are_gridless",
    "assert_session_whitelisted",
    "canary",
    "cloud_sync_active",
    "cloud_sync_state",
    "close_db",
    "done_reading",
    "clear_registry_buffer",
    "commit_guarded",
    "commit_witness",
    "content_writable_columns",
    "db_schema_version",
    "db_sidecar_suffixes",
    "default_protected_snapshot_paths",
    "ensure_folder",
    "top_level_folders",
    "ensure_my_tag_value",
    "my_tag_writable",
    "ensure_playlist",
    "MOVED",
    "UNINSPECTABLE",
    "field_policies_for_commit",
    "row_probe_policy",
    "guard_violations",
    "pending_changes",
    "pending_objects",
    "integration_db_path",
    "IntegrityCheckCopyFailed",
    "disposable_root",
    "file_set",
    "integrity_ok",
    "is_folder",
    "live_db_path",
    "membership_removed",
    "move_playlist_node",
    "node_change_violations",
    "node_removed",
    "node_tables",
    "assert_node_changes_confined",
    "remove_playlist_node",
    "metadata_decision",
    "open_db",
    "pin_validated_on",
    "pinned_app_version",
    "pinned_db_version",
    "pinned_pyrekordbox",
    "prune_snapshots",
    "read_installed_app_version",
    "read_rekordbox_settings",
    "read_run_state_records",
    "register_field_policy",
    "registered_field_policies",
    "remove_memberships",
    "rekordbox_agent_running",
    "rekordbox_processes_running",
    "rekordbox_running",
    "reset_field_policies",
    "restore_from_snapshot",
    "restored_sidecar_suffixes",
    "snapshot_database_in",
    "snapshot_db",
    "snapshot_root",
    "soft_deleted",
    "unlock_needed",
    "write_lock_path",
    "write_metadata_field",
    "write_session_lock",
]
