"""A host with rekordbox open, faked at psutil itself (U232).

psutil's own ``pids``, ``Process`` and ``process_iter`` answer the real
listing plus ``rekordbox`` and ``rekordboxAgent``, BENEATH every seam the
suite stubs, so the conftest's stubs are proved, never bypassed. Used through
the ``rekordbox_on_the_host`` fixture, or for a whole run as a plugin::

      .venv/bin/python -m pytest -p tests._host_processes
"""

from __future__ import annotations

from collections.abc import Iterator

import psutil
import pytest

#: The two processes the host fakes, at pids past any platform's pid ceiling so
#: they can never be a real process's: macOS stops at 99998 and Linux at 2**22.
OPEN: dict[int, str] = {2**31 - 3: "rekordbox", 2**31 - 2: "rekordboxAgent"}

#: psutil's own enumeration, captured at import, before any fixture runs, so
#: the fake host sits over the real table even beneath the conftest's tripwire.
_REAL_PIDS = psutil.pids
_REAL_PROCESS = psutil.Process


class _Open:
    """One faked process, readable the way psutil's ``Process`` is read."""

    def __init__(self, pid: int, name: str) -> None:
        self.pid = pid
        self._name = name

    def name(self) -> str:
        return self._name

    def status(self) -> str:
        return psutil.STATUS_RUNNING

    def is_running(self) -> bool:
        return True


def install(monkeypatch: pytest.MonkeyPatch) -> None:
    """Put rekordbox and its agent on the process table, on ``monkeypatch``, real ones kept."""
    class Process(_REAL_PROCESS):  # type: ignore[misc, valid-type]
        def __new__(cls, pid: int | None = None):  # noqa: D102
            if pid in OPEN:
                return _Open(pid, OPEN[pid])
            return super().__new__(cls)

    def pids() -> list[int]:
        return sorted({*_REAL_PIDS(), *OPEN})

    def process_iter(attrs=None, ad_value=None) -> Iterator[object]:  # noqa: ARG001
        for pid in pids():
            try:
                yield Process(pid)
            except psutil.NoSuchProcess:
                continue

    monkeypatch.setattr(psutil, "pids", pids)
    monkeypatch.setattr(psutil, "Process", Process)
    monkeypatch.setattr(psutil, "process_iter", process_iter)


_SESSION: list[pytest.MonkeyPatch] = []


def pytest_configure(config: pytest.Config) -> None:  # noqa: ARG001
    """As a plugin: rekordbox is open on the host for the whole session."""
    patch = pytest.MonkeyPatch()
    install(patch)
    _SESSION.append(patch)


def pytest_unconfigure(config: pytest.Config) -> None:  # noqa: ARG001
    while _SESSION:
        _SESSION.pop().undo()
