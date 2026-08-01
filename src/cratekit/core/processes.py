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
"""

from __future__ import annotations

import os
from typing import Callable, Iterable

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
    every test does, never loads the extension module at all.
    """
    import psutil

    names: list[str] = []
    for process in psutil.process_iter(["name"]):
        name = (process.info or {}).get("name")
        if name:
            names.append(str(name))
    return tuple(names)


def rekordbox_processes_running(*, lister: ProcessLister | None = None) -> tuple[str, ...]:
    """Which rekordbox processes hold the database right now.

    Returned in the order of :data:`REKORDBOX_PROCESSES` rather than in the
    order the platform happened to list them, so a refusal message reads the
    same way every time it fires.
    """
    present = {executable_stem(name) for name in (lister or running_process_names)()}
    return tuple(name for name in REKORDBOX_PROCESSES if name in present)


__all__ = [
    "REKORDBOX_PROCESSES",
    "ProcessLister",
    "executable_stem",
    "rekordbox_processes_running",
    "running_process_names",
]
