"""Who holds a destructive session: the holder record, its liveness, and the library lock.

Part of :mod:`cratekit.core.session`, which re-exports every name here; read them there. A
name of the session outside this file, and every seam a test patches, is read through
``session`` at call time so a patch on the session bites here too (U300).
"""

from __future__ import annotations

import functools
import hashlib
import json
import logging
import math
import os
import re
import socket
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Iterator, Mapping

from cratekit.core import config, rb_writer
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Remediation,
    Scope,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.core.session_call_time import session as _session

if TYPE_CHECKING:
    from cratekit.core.session import SessionRecord


#: The session logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.session")


#: Recorded in place of a value this platform cannot answer, so a degraded
#: identity is never read as a confident one. The kernel still does the exclusion.
UNKNOWN_IDENTITY = "unknown"


@dataclass(frozen=True, slots=True)
class Holder:
    """Who holds the session lock, identified across machines and restarts.

    ``machine`` tells apart machines sharing a host name, so a holder from this
    machine's previous boot can be judged gone (R-647); ``pid`` is reused after
    a restart, ``boot`` detects that, and ``started`` tells apart two processes
    given one pid in one boot. An unknown machine is never evidence a holder is gone.
    """

    host: str
    boot: str
    pid: int
    started: str
    machine: str = UNKNOWN_IDENTITY

    def to_json(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "machine": self.machine,
            "boot": self.boot,
            "pid": self.pid,
            "started": self.started,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Holder:
        return cls(
            host=str(data.get("host", UNKNOWN_IDENTITY)),
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
            boot=str(data.get("boot", UNKNOWN_IDENTITY)),
            pid=int(data.get("pid", 0)),
            started=str(data.get("started", UNKNOWN_IDENTITY)),
        )

    def describe(self) -> str:
        return f"process {self.pid} on {self.host} (boot {self.boot}, started {self.started})"


def boot_identity() -> str:
    """This boot of this machine, or the declared unknown. Imports psutil lazily."""
    try:
        import psutil

        return f"{psutil.boot_time():.0f}"
    except Exception as exc:  # noqa: BLE001 - an unanswerable identity is not a failure
        logger.debug("boot identity is unavailable on this platform: %s", exc)
        return UNKNOWN_IDENTITY


#: The files a Linux machine keeps its identity in, the systemd one first.
_LINUX_MACHINE_ID_FILES = ("/etc/machine-id", "/var/lib/dbus/machine-id")

#: How the macOS hardware identity reads in the platform registry's output.
_IOREG_UUID = re.compile(r'"IOPlatformUUID"\s*=\s*"([^"]+)"')


def _raw_machine_identity() -> str | None:
    """The platform's own identifier for this machine, or None when it will not say."""
    if sys.platform == "darwin":
        completed = subprocess.run(
            ["/usr/sbin/ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        found = _IOREG_UUID.search(completed.stdout)
        return found.group(1) if found else None
    if sys.platform.startswith("linux"):
        for candidate in _LINUX_MACHINE_ID_FILES:
            try:
                text = Path(candidate).read_text().strip()
            except OSError:
                continue
            if text:
                return text
        return None
    if sys.platform == "win32":
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography"
        ) as key:
            return str(winreg.QueryValueEx(key, "MachineGuid")[0]) or None
    return None


@functools.cache
def machine_identity() -> str:
    """This machine, as an identity no other machine shares, or the declared unknown.

    Recorded as a digest, since it is only compared and a hardware serial does
    not belong in a record. Cached, since the macOS answer costs a subprocess.
    A cloned Linux image shares one identity, a case this narrows, not closes.
    """

    try:
        raw = _raw_machine_identity()
    except Exception as exc:  # noqa: BLE001 - an unanswerable identity is not a failure
        logger.debug("machine identity is unavailable on this platform: %s", exc)
        raw = None
    if not raw:
        return UNKNOWN_IDENTITY
    return hashlib.sha256(f"cratekit-machine:{raw}".encode()).hexdigest()[:32]


def process_started(pid: int) -> str:
    """When a process began, or the declared unknown, also for a process that
    does not exist; liveness is asked separately by :func:`process_exists`."""
    try:
        import psutil

        return f"{psutil.Process(pid).create_time():.3f}"
    except Exception as exc:  # noqa: BLE001 - see the docstring
        logger.debug("process start time is unavailable for %s: %s", pid, exc)
        return UNKNOWN_IDENTITY


def process_exists(pid: int) -> bool | None:
    """Whether a process with this identifier exists, or None when this cannot say.

    None is not False, or an unanswerable platform would clear a live holder's claim.
    """
    try:
        import psutil

        return bool(psutil.pid_exists(pid))
    except Exception as exc:  # noqa: BLE001 - an unanswerable question is not a failure
        logger.debug("process existence is unavailable for %s: %s", pid, exc)
        return None


def current_holder() -> Holder:
    """This process, as the lock file will record it."""
    pid = os.getpid()
    return Holder(
        host=socket.gethostname(),
        machine=_session().machine_identity(),
        boot=boot_identity(),
        pid=pid,
        started=_session().process_started(pid),
    )


#: How far apart two readings of one boot's start may land, since a clock
#: adjustment moves the wall clock boot reading.
BOOT_DRIFT_SECONDS = 60.0


def _gone_since_an_earlier_boot(holder: Holder, reference: Holder) -> bool:
    """Whether a holder from another boot is provably from THIS machine's earlier one.

    Proven only when the machine identity is known and equal, the holder's boot
    is earlier past the drift margin, and no process with its pid runs at all
    (R-647). Start times are not compared, since a stepped clock shifts a live
    process's start time with the boot reading on Linux.
    """
    if UNKNOWN_IDENTITY in (holder.machine, reference.machine):
        return False
    if holder.machine != reference.machine:
        return False
    try:
        earlier_by = float(reference.boot) - float(holder.boot)
    except ValueError:
        return False
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
        return False
    return _session().process_exists(holder.pid) is False


def holder_alive(holder: Holder, *, here: Holder | None = None) -> bool:
    """Whether a recorded holder is still running.

    FAILS TOWARDS ALIVE on every question this process cannot answer, since
    guessing dead lets one machine clear another's lock. A holder from this
    machine's earlier boot is gone (R-647). Existence and identity are asked
    separately: pids are recycled, but an unanswerable start time is not a mismatch.
    """
    reference = here or current_holder()
    if holder.host != reference.host:
        return True
    if UNKNOWN_IDENTITY in (holder.boot, reference.boot):
        return True
    if holder.boot != reference.boot:
        return not _gone_since_an_earlier_boot(holder, reference)
    if holder.started == UNKNOWN_IDENTITY:
        return True
    exists = _session().process_exists(holder.pid)
    if exists is not True:
        return exists is None
    observed = _session().process_started(holder.pid)
    if observed == UNKNOWN_IDENTITY:
        return True
    return observed == holder.started


class SessionComposition(CratekitError):
    """A session was opened inside a session, in one process.

    A programming error, checked before the kernel, which would report it as a
    foreign holder and tell the caller to wait for itself.
    """


#: Lock paths this process currently holds, read before the kernel is asked.
_HELD: set[str] = set()


def lock_path(cfg: config.Config) -> Path:
    """The whole-run lock, beside the library, distinct from the writer's narrow
    lock so a second process refuses at the door rather than part way through."""
    return config.state_path("session_lock", cfg)


def read_lock_holder(path: Path | str) -> Holder | None:
    """Who the lock file says holds it, or None when it says nobody or is unreadable.

    The content is advisory, only to name a holder; the kernel does the exclusion.
    """
    try:
        raw = Path(path).read_text()
    except OSError:
        return None
    try:
        # An empty or unparsable file says nobody, as json.loads refuses both.
        data = json.loads(raw)
        if not isinstance(data, Mapping) or not data.get("holder"):
            return None
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
        # A damaged record answers None too; the shell tells it from absent.
        return None


def _write_holder(handle: Any, holder: Holder | None) -> None:
    """Record, or clear, the holder inside the already-locked file."""
    handle.seek(0)
    handle.truncate()
    if holder is not None:
        handle.write(json.dumps({"holder": holder.to_json()}, sort_keys=True))
    handle.flush()
    os.fsync(handle.fileno())


def _open_lock_file(target: Path) -> Any:
    """Open the lock file, private, creating the directory private with it, since
    a replaceable lock file in an open directory loses the exclusion (P1)."""
    config.mkdir_private(target.parent)
    # Explicit mode, not the umask; read-write since the holder is replaced.
    descriptor = os.open(target, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
    handle = os.fdopen(descriptor, "r+")
    if hasattr(os, "chmod"):  # guarded: a POSIX mode is meaningless on some platforms
        try:
            # Fixes the mode of a lock an earlier build created.
            os.chmod(target, config.PRIVATE_FILE_MODE)
        except OSError as exc:
            # Not fatal: another account's file cannot be chmodded.
            logger.debug("could not set the mode on the session lock at %s: %s", target, exc)
    return handle


def _lock_held_refusal(target: Path, holder: Holder | None) -> CratekitError:
    """The refusal for a lock somebody else has, with the right remedy token.

    A running holder is waited for; a held lock whose holder is gone, reachable
    on a networked filesystem, is released by an explicit act.
    """
    if holder is not None and holder_alive(holder):
        return refuse(
            "session-lock-held",
            f"another destructive session holds the library lock at {target}: "
            f"{holder.describe()}",
            remedy=Remedy.WAIT_FOR_HOLDER,
            scope=Scope.SESSION,
            detail={"lock": str(target), "holder": holder.to_json()},
        )
    return refuse(
        "session-lock-held",
        f"the library lock at {target} is held and its recorded holder is not "
        f"running"
        + (f": {holder.describe()}" if holder is not None else " and is unrecorded"),
        remedy=Remedy.RELEASE_STALE_LOCK,
        scope=Scope.SESSION,
        detail={
            "lock": str(target),
            "holder": holder.to_json() if holder is not None else None,
            "stale": True,
        },
    )


@contextmanager
def session_lock(
    cfg: config.Config | None = None,
    *,
    path: Path | str | None = None,
    holder: Holder | None = None,
) -> Iterator[Path]:
    """Hold the whole-run lock for one destructive session.

    THE FILE IS NEVER UNLINKED, or a second process locks a fresh inode at the
    same name and both believe they hold it.
    """
    target = Path(path) if path is not None else lock_path(cfg or config.load())
    key = str(target.absolute())
    if key in _HELD:
        raise SessionComposition(
            Cause(
                reason="internal-error",
                message=(
                    f"a destructive session was opened inside another one in this "
                    f"process, on {target}. Sessions do not nest: the second "
                    f"acquisition can never succeed, and reporting it as a foreign "
                    f"holder would tell a caller to wait for itself"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                scope=Scope.RUN,
                origin=("session",),
                detail={"lock": str(target)},
            )
        )

    handle = _open_lock_file(target)
    acquired = False
    try:
        try:
            # The writer's own acquisition, so the two cannot differ.
            rb_writer._acquire_exclusive(handle)
        except OSError as exc:
            raise _lock_held_refusal(target, read_lock_holder(target)) from exc
        acquired = True
        _HELD.add(key)
        _write_holder(handle, holder or current_holder())
        yield target
    finally:
        if acquired:
            _HELD.discard(key)
            try:
                _write_holder(handle, None)
            except OSError as exc:
                logger.debug("could not clear the holder record on %s: %s", target, exc)
            try:
                rb_writer._release_exclusive(handle)
            except OSError as exc:  # pragma: no cover - the close below still frees it
                logger.debug("could not release the lock on %s: %s", target, exc)
        handle.close()


def release_stale_lock(
    cfg: config.Config | None = None, *, path: Path | str | None = None
) -> Holder | None:
    """Clear a dead holder's record. An EXPLICIT act, never an automatic one.

    Returns the holder cleared, or None. Refuses while the holder still runs.
    """

    target = Path(path) if path is not None else lock_path(cfg or config.load())
    recorded = read_lock_holder(target)
    if recorded is None:
        return None
    if holder_alive(recorded):
        raise refuse(
            "session-lock-held",
            f"the library lock at {target} is held by {recorded.describe()}, which "
            f"is still running, so its claim is not stale and is not releasable",
            remedy=Remedy.WAIT_FOR_HOLDER,
            scope=Scope.SESSION,
            detail={"lock": str(target), "holder": recorded.to_json()},
        )

    handle = _open_lock_file(target)
    try:
        try:
            rb_writer._acquire_exclusive(handle)
        except OSError as exc:
            raise refuse(
                "session-lock-held",
                f"the library lock at {target} could not be taken even though its "
                f"recorded holder {recorded.describe()} is gone, so something else "
                f"is holding the file",
                remedy=Remedy.WAIT_FOR_HOLDER,
                scope=Scope.SESSION,
                detail={"lock": str(target), "holder": recorded.to_json()},
            ) from exc
        _write_holder(handle, None)
        rb_writer._release_exclusive(handle)
    finally:
        handle.close()
    return recorded


def orphaned(record: SessionRecord, *, here: Holder | None = None) -> bool:
    """Whether an open record's owner is provably gone, so nothing will ever end it.

    Only an ``open`` record that names a holder :func:`holder_alive` judges gone
    (R-598); the other states wait on an import or a restore, and an intake
    landing stays open across processes with no holder. An unreadable holder is alive.
    """
    if record.state is not _session().SessionState.OPEN:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
    if not isinstance(recorded, Mapping):
        return False
    try:
        holder = Holder.from_json(recorded)
    except (TypeError, ValueError):
        return False
    return not holder_alive(holder, here=here)


def abandon_orphaned_sessions(
    cfg: config.Config,
    *,
    only: Iterable[str] | None = None,
    now: datetime | None = None,
) -> tuple[SessionRecord, ...]:
    """End every open record whose owner is provably gone, and return them.

    A SIGKILL or a power loss (R-647) leaves a record ``open`` for ever. ``only``
    limits the sweep to the records the caller showed (R-648). Abandoning is
    the ungated close; a recorded commit still reads as work a restore discards.
    """
    here = current_holder()
    shown = None if only is None else frozenset(only)
    return tuple(
        _session().close_session(record, cfg, state=_session().SessionState.ABANDONED, now=now)
        for record in _session().records(cfg)
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
    )
