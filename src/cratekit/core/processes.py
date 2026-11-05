"""Which rekordbox processes are running, asked one way by every caller.

WHY THIS MODULE EXISTS. Two call sites need the same answer and cannot share an
implementation:

* ``core.rb_writer`` refuses a database write while rekordbox is up, and asks
  pyrekordbox, which is the upstream authority on how rekordbox is found.
* ``modules.tools.backup`` refuses to snapshot a live database, and deliberately
  does NOT import pyrekordbox: backup is an optional module and must work on a
  slim install where the rekordbox extra is absent.

Both reasons are good, so the duplication of MECHANISM stays. What must never
duplicate is the process name list and the matching rule, and before this module
existed they did. The two copies had already drifted: one stripped the
executable suffix and one did not, so on Windows, where psutil reports
``rekordbox.exe``, the backup guard saw no rekordbox running and would have
snapshotted a database the application was actively writing. The database guard
was correct on the same machine, which is exactly why nothing caught it. A
divergence between two guards is invisible until you put them side by side.

So: one list, one rule, two mechanisms, and a test that pins the two mechanisms
to agree.

A PROCESS THE SCAN CANNOT READ (U211). Sitting 54 ended a live ``sync pair``
apply, both gates answered, as ``INTERNAL: SystemError: <built-in function
proc_cmdline> returned a result with an exception set``. A Pioneer daemon had
leaked hundreds of zombies, and on macOS psutil's ``name()`` reads the command
line for any name of fifteen characters or more, which raised out of a process
as it died. So the scan reads each process's name inside its own try, and
answers in one of three ways for a process it cannot read:

* gone, denied or a zombie as psutil reports it: skipped, since a process
  that is gone or a zombie holds no database, and a denied one is what
  pyrekordbox has always skipped;
* any other error, on a process whose status then reads zombie or which is
  then gone: skipped, for the same reason;
* any other error on a process still alive: :class:`AbsenceUnconfirmed`,
  naming the pid, once the whole list is walked. Never an absence read out
  of a process the scan could not read, and never an escape as ``INTERNAL``.
  A rekordbox process the scan did read is still answered as running.

The writer's mechanism asks pyrekordbox, whose own scan stops at the same
process, so ``core.rb_writer`` falls back to this scan when pyrekordbox raises.
One careful reading, two mechanisms still.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Iterable, Sequence

from cratekit.core.cause import Cause, CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The processes that hold the rekordbox database. BOTH matter. The agent is the
#: one that surprises people: it is always present, it holds the handle, and it
#: mutates the library through Cloud Library Sync with the window closed.
#:
#: This is the ONLY definition in the tree. ``tests/test_process_guard.py``
#: asserts that by walking the source, not by listing the modules it has seen.
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordboxAgent")

#: A source of running process names. Injected by every test, so no test loads
#: psutil and no test depends on what happens to be running on the machine.
ProcessLister = Callable[[], Iterable[str]]

#: The cause a scan refuses with when a live process could not be read (U211).
UNCONFIRMED = "rekordbox-absence-unconfirmed"


class AbsenceUnconfirmed(CratekitError):
    """The process scan met a live process it could not read, so rekordbox's absence is unknown.

    A subclass so a reader that reports rather than refuses, doctor, can tell
    this answer from every other refusal and say it as a note. ``read`` holds
    every ``(pid, name)`` the scan did read, so a caller that finds rekordbox
    among them answers that it is running, which is established, rather than
    that its absence is unknown.
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
        named = "; ".join(
            f"process {pid} ({error})" for pid, error in unreadable[:NAMED_PIDS]
        )
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
        detail={
            "pids": pids,
            "errors": [error for _pid, error in unreadable],
        },
    )
    return AbsenceUnconfirmed(refused.cause, read)


def _platform() -> Any:
    """The platform's process table, which is psutil, imported lazily.

    A seam rather than an import at the call, so a test hands the scan a fake
    table that raises exactly what a dying process raised, with no psutil
    process of its own.
    """
    import psutil

    return psutil


def _gone_or_zombie(platform: Any, pid: int, process: Any) -> bool:
    """Whether a process whose read failed is now gone or a zombie.

    False when its status cannot be read either, because a process that is
    neither readable nor known to be gone could be the one that holds the
    database.
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

    Walks the pid list rather than ``process_iter``, because an error raised
    while the iterator builds or prefetches a process escapes the generator
    and ends the walk, where here it ends one process's read. Walks the whole
    list before it answers, then refuses with :class:`AbsenceUnconfirmed`
    naming every live process it could not read, carrying what it did read;
    and refuses the same way over a pid list it cannot read at all.
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
    """A process name reduced to the form the name list is written in.

    Windows reports ``rekordbox.exe``; macOS and Linux report ``rekordbox``.
    Stripping the extension is what makes ONE list correct on all three, and it
    is the exact step whose absence made the backup guard blind on Windows.

    Matching stays EXACT after the strip, never a substring. A substring match
    makes an unrelated process whose name merely contains "rekordbox" refuse
    every backup forever, and a guard that refuses correct situations is one
    people learn to bypass (seam decision P7).
    """
    return os.path.splitext(name)[0]


def running_process_names() -> tuple[str, ...]:
    """Names of every running process, read from the platform.

    psutil is imported lazily so a caller that injects its own lister, which
    every test does, never loads the extension module at all. Refuses with
    :class:`AbsenceUnconfirmed` as :func:`running_processes` does.
    """
    return tuple(name for _pid, name in running_processes())


def rekordbox_pid(name: str, *, platform: Any = None) -> int:
    """The pid of the first running process named ``name``, or zero.

    The careful scan's answer in the shape pyrekordbox's ``get_process_id``
    gives, for the writer's fallback when pyrekordbox's own scan raises. A
    process of that name the scan did read is answered even when another
    could not be read, since its presence is established; its absence is not,
    so then the refusal stands.
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
    """Which rekordbox processes hold the database right now.

    Returned in the order of :data:`REKORDBOX_PROCESSES` rather than in the
    order the platform happened to list them, so a refusal message reads the
    same way every time it fires.
    """
    try:
        listed = tuple((lister or running_process_names)())
    except AbsenceUnconfirmed as exc:
        # A REKORDBOX PROCESS THE SCAN DID READ IS ESTABLISHED (U211), so it is
        # answered as running, the refusal every caller already has; only a
        # scan that read none of them leaves the absence unknown.
        seen = {executable_stem(name) for _pid, name in exc.read}
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
        listed = tuple(name for _pid, name in exc.read)
    present = {executable_stem(name) for name in listed}
    return tuple(name for name in REKORDBOX_PROCESSES if name in present)


__all__ = [
    "REKORDBOX_PROCESSES",
    "UNCONFIRMED",
    "AbsenceUnconfirmed",
    "ProcessLister",
    "executable_stem",
    "rekordbox_pid",
    "rekordbox_processes_running",
    "running_process_names",
    "running_processes",
]
