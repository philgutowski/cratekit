"""One pass stages at a time (U293).

Every download lands in the one staging folder and a landing takes the whole
of it, so two passes downloading together would each land the other's tracks.
R-1499 made a pass read the folder before its download and again around its
tail, and refuse beside anything that is not its own; that keeps a wrong
landing out, and it catches the collision only after both passes have spent
their downloads. Once a pass runs with nobody watching, the night pass,
``sync.night``, the collision has to be refused before either starts.

So ``sync.land``, ``label.sync`` with its go and ``sync.night`` each
hold this lock for the whole of a run, and a second refuses ``staging-held``
naming the holder's verb, process, run and start.

THE DRIVER LOCK'S RULES, FOR THE DRIVER LOCK'S REASONS
(:func:`cratekit.core.jobs.driver_lock`). Liveness is the kernel's: an
advisory lock is released when its holder's process dies, so a crashed pass's
lock is already gone and a slow one's is not, which no timeout can tell apart.
The file is never unlinked, since unlinking on release is how two processes
come to hold locks on two inodes at one name. The holder written inside is for
the refusal's words and is never the liveness test.

REENTRANT WITHIN ONE PROCESS. ``sync.night`` runs ``sync.land``
through the dispatcher in the same process, and an advisory lock on a second
descriptor would refuse its own holder, so a process that holds the lock
already holds it again by count and releases it when the outermost hold ends.

Layer: core. It knows a state entry and a verb's words, nothing of the verbs.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy

#: The declared state entry the lock is kept in.
STATE_KEY = "staging_lock"

#: The reason a second pass refuses with, declared in ``cause.REASONS``.
HELD = "staging-held"

_ORIGIN = ("staging_lock",)

#: This process's hold: the open descriptor, how many holds deep, and who.
_HANDLE: IO[str] | None = None
_DEPTH = 0
_HOLDER: dict[str, Any] | None = None


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def lock_path() -> Path:
    return config.state_path(STATE_KEY)


def _said(holder: dict[str, Any] | None) -> str:
    if not holder:
        return "a pass whose holder could not be read"
    parts = [str(holder.get("verb") or "a pass"), f"pid {holder.get('pid')}"]
    if holder.get("run_id"):
        parts.append(f"run {holder['run_id']}")
    if holder.get("started"):
        parts.append(f"since {holder['started']}")
    return ", ".join(parts)


def _read_holder(text: str) -> dict[str, Any] | None:
    try:
        holder = json.loads(text)
    except ValueError:
        return None
    return holder if isinstance(holder, dict) else None


def _held_error(what: str, holder: dict[str, Any] | None, path: Path) -> CratekitError:
    return refuse(
        HELD,
        f"another pass is staging downloads ({_said(holder)}), so {what} stages "
        f"nothing until it has finished; one pass stages at a time, since a landing "
        f"takes the whole staging folder",
        remedy=Remedy.WAIT_FOR_HOLDER,
        steps=(
            "wait for that pass to end, then run this again",
            "crate doctor shows the night pass's last line when the holder is "
            "crate sync night",
        ),
        retryable=True,
        origin=_ORIGIN,
        detail={"holder": holder, "lock": str(path)},
    )


@contextmanager
def held(verb: str, *, run_id: str | None = None, what: str | None = None) -> Iterator[None]:
    """Hold the staging lock for the body, or refuse naming the live holder.

    ``verb`` names the holder in a second pass's refusal, ``run_id`` its run,
    and ``what`` the act the refusal says is stopped, ``verb`` by default.
    """
    global _HANDLE, _DEPTH, _HOLDER
    if _HANDLE is not None:
        _DEPTH += 1
        try:
            yield
        finally:
            _DEPTH -= 1
        return
    path = lock_path()
    config._mkdir_private(path.parent)
    # os.open with an explicit mode, for the driver lock's reason: a lock any
    # local account could hold would refuse every pass.
    handle = os.fdopen(os.open(path, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE), "r+")
    try:
        try:
            import fcntl
        except ImportError:  # pragma: no cover - POSIX only in practice
            fcntl = None
        if fcntl is not None:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                handle.seek(0)
                raise _held_error(what or verb, _read_holder(handle.read()), path) from None
        record = {"pid": os.getpid(), "verb": verb, "run_id": run_id, "started": _now()}
        handle.seek(0)
        handle.truncate()
        json.dump(record, handle)
        handle.flush()
        _HANDLE, _DEPTH, _HOLDER = handle, 1, record
        try:
            yield
        finally:
            _HANDLE, _DEPTH, _HOLDER = None, 0, None
    finally:
        handle.close()  # closing the descriptor releases the lock; the file stays


__all__ = ["HELD", "STATE_KEY", "held", "lock_path"]
