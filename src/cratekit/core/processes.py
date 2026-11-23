"""Which rekordbox processes are running, asked one way by every caller.

``core.rb_writer`` asks pyrekordbox; ``modules.tools.backup`` must work without
the rekordbox extra and asks psutil. Two mechanisms, but one name list and one
matching rule, so the two guards cannot drift (a suffix drift once blinded the
backup guard on Windows), and a test pins them to agree.

A process the scan cannot read (U211) is judged on its own, inside its own
try:

* gone, denied or a zombie as psutil reports it: skipped, since it holds no
  database (and pyrekordbox has always skipped a denied one);
* any other error, on a process whose status then reads zombie or which is
  then gone: skipped, for the same reason;
* any other error on a process still alive: :class:`AbsenceUnconfirmed`,
  naming the pid, once the whole list is walked. Never an absence read out
  of a process the scan could not read, and never an escape as ``INTERNAL``.
  A rekordbox process the scan did read is still answered as running.

``core.rb_writer`` falls back to this scan when pyrekordbox's own scan raises.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Iterable, Sequence

from cratekit.core.cause import Cause, CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The processes that hold the rekordbox database. Both matter: the agent holds
#: the handle and syncs the library with the window closed. The only definition
#: in the tree, which ``tests/test_process_guard.py`` asserts.
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordboxAgent")

#: A source of running process names, injected by tests so none loads psutil.
ProcessLister = Callable[[], Iterable[str]]

#: The cause a scan refuses with when a live process could not be read (U211).
UNCONFIRMED = "rekordbox-absence-unconfirmed"


class AbsenceUnconfirmed(CratekitError):
    """The process scan met a live process it could not read, so rekordbox's absence is unknown.

    A subclass so doctor can say it as a note. ``read`` holds every
    ``(pid, name)`` the scan did read, so rekordbox found there is running.
    """

    def __init__(self, cause: Cause, read: Iterable[tuple[int, str]] = ()) -> None:
        super().__init__(cause)
        self.read: tuple[tuple[int, str], ...] = tuple(read)


#: How many unreadable pids a refusal names before it counts the rest.
NAMED_PIDS = 5


def _unconfirmed(
    unreadable: Sequence[tuple[int | None, str]], read: Iterable[tuple[int, str]] = ()
) -> AbsenceUnconfirmed:
    """The refusal for the processes, or the process list, this scan could not read."""
    pids = [pid for pid, _error in unreadable if pid is not None]
    if not pids:
        error = unreadable[0][1] if unreadable else "no answer"
        what = f"the list of running processes could not be read ({error})"
        look = "look at the running processes with: ps -axo pid,stat,comm"
    else:
        named = "; ".join(f"process {pid} ({error})" for pid, error in unreadable[:NAMED_PIDS])
        more = len(unreadable) - NAMED_PIDS
        if more > 0:
            named += f"; and {more} more"
        one = len(unreadable) == 1
        what = (
            f"{named} could not be read and {'is' if one else 'are'} neither gone "
            f"nor a zombie, so {'it' if one else 'any of them'} could be rekordbox "
            f"or its agent"
        )
        look = f"look at the process with: ps -p {pids[0]} -o pid,stat,comm"
    refused = refuse(
        UNCONFIRMED,
        f"rekordbox's absence could not be confirmed: {what}. The step that "
        f"needed rekordbox closed was not run",
        remedy=Remedy.RETRY_LATER,
        steps=(
            "wait a moment for the process to finish exiting, then run it again",
            f"if it refuses again, {look}",
        ),
        scope=Scope.RUN,
        retryable=True,
        origin=("processes",),
        detail={"pids": pids, "errors": [error for _pid, error in unreadable]},
    )
    return AbsenceUnconfirmed(refused.cause, read)


def _platform() -> Any:
    """The platform's process table, psutil, imported lazily; a seam tests replace."""
    import psutil

    return psutil


def _gone_or_zombie(platform: Any, pid: int, process: Any) -> bool:
    """Whether a process whose read failed is now gone or a zombie.

    False when its status cannot be read either: it could hold the database.
    """
    try:
        target = process if process is not None else platform.Process(pid)
        return target.status() == platform.STATUS_ZOMBIE
    except platform.NoSuchProcess:
        # ``ZombieProcess`` is a subclass, so a status read that says zombie
        # by raising lands here too.
        return True
    except Exception:  # noqa: BLE001 - an unreadable status confirms nothing
        return False


def running_processes(*, platform: Any = None) -> tuple[tuple[int, str], ...]:
    """Every running process as ``(pid, name)``, each read in its own try.

    Walks the pid list, not ``process_iter``, whose errors end the whole walk.
    Walks every pid, then refuses with :class:`AbsenceUnconfirmed` naming each
    live process it could not read, carrying what it did read; a pid list it
    cannot read refuses the same way.
    """
    table = platform if platform is not None else _platform()
    try:
        pids = list(table.pids())
    except Exception as exc:  # noqa: BLE001 - no list is no confirmation
        raise _unconfirmed([(None, _spelled(exc))]) from exc
    found: list[tuple[int, str]] = []
    unreadable: list[tuple[int | None, str]] = []
    first: BaseException | None = None
    for pid in pids:
        process = None
        try:
            process = table.Process(pid)
            name = process.name()
        except (table.NoSuchProcess, table.ZombieProcess, table.AccessDenied):
            continue
        except Exception as exc:  # noqa: BLE001 - judged on the process below
            if _gone_or_zombie(table, pid, process):
                continue
            unreadable.append((pid, _spelled(exc)))
            first = first or exc
            continue
        if name:
            found.append((pid, str(name)))
    if unreadable:
        raise _unconfirmed(unreadable, found) from first
    return tuple(found)


def _spelled(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"


def executable_stem(name: str) -> str:
    """A process name without its extension (``rekordbox.exe`` on Windows).

    Matching stays exact after the strip, never a substring (seam decision P7).
    """
    return os.path.splitext(name)[0]


def running_process_names() -> tuple[str, ...]:
    """Names of every running process; refuses as :func:`running_processes` does."""
    return tuple(name for _pid, name in running_processes())


def rekordbox_pid(name: str, *, platform: Any = None) -> int:
    """The pid of the first running process named ``name``, or zero.

    The writer's fallback, shaped as pyrekordbox's ``get_process_id``. A read
    process of that name is answered even when another was unreadable;
    otherwise the refusal stands.
    """
    try:
        listed = running_processes(platform=platform)
    except AbsenceUnconfirmed as exc:
        listed = exc.read
        if not any(executable_stem(found) == name for _pid, found in listed):
            raise
    for pid, found in listed:
        if executable_stem(found) == name:
            return pid
    return 0


def rekordbox_processes_running(*, lister: ProcessLister | None = None) -> tuple[str, ...]:
    """Which rekordbox processes hold the database right now, in list order."""
    try:
        listed = tuple((lister or running_process_names)())
    except AbsenceUnconfirmed as exc:
        # A rekordbox process the scan did read is running (U211); only a scan
        # that read none leaves the absence unknown.
        seen = {executable_stem(name) for _pid, name in exc.read}
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
        listed = tuple(name for _pid, name in exc.read)
    present = {executable_stem(name) for name in listed}
    return tuple(name for name in REKORDBOX_PROCESSES if name in present)


__all__ = [
    "REKORDBOX_PROCESSES", "UNCONFIRMED", "AbsenceUnconfirmed", "ProcessLister",
    "executable_stem", "rekordbox_pid", "rekordbox_processes_running", "running_process_names",
    "running_processes",
]
