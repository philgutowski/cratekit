"""What the machine says: the installed application's version, the running processes, and the
settings file Cloud Library Sync is read from.

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name its callers read and raises the
refusals these readings feed; read them there. A name of the writer outside this file,
and every seam a test patches, is read through ``rb_writer`` at call time so a patch on
the writer bites here too (U300).
"""

from __future__ import annotations

import logging
import os
import sys
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterator, Mapping

from cratekit.core import config, processes
from cratekit.core.rb_call_time import writer as _writer

#: The writer's own logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.rb_writer")


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


def _default_app_probe() -> Callable[[Path], str | None]:
    if sys.platform == "darwin":
        return _macos_app_version
    # No probe elsewhere, Windows included: None degrades like an uninstalled application.
    return lambda _path: None


def _candidate_app_paths(cfg: config.Config | None) -> list[Path]:
    """Where to look for the installed application, most specific first, configuration before glob."""
    override = os.environ.get(ENV_APP_PATH)
    if override:
        return [Path(override)]
    configured = _writer()._pins(cfg).app_path
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
#: Values are ATTRIBUTE NAMES resolved on ``rb_writer`` at call time, so tests can patch the seams.
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
            raise _writer()._running(
                f"{name!r} is listed as a process holding the database but this "
                f"module has no way to ask whether it is running, so no write "
                f"can be declared safe",
                detail={"process": name},
            )
        try:
            if getattr(_writer(), probe_name)():
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
        settings = _writer().read_rekordbox_settings()
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
