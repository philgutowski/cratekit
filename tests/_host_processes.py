"""A host with rekordbox open, faked at psutil itself (U232).

The v0.13.0 cut was refused on a red Mac battery because rekordbox was open on
the machine, and two tests read the host's real process table. This module
models that machine on any machine: psutil's own ``pids``, ``Process`` and
``process_iter`` answer the real listing plus a ``rekordbox`` and a
``rekordboxAgent``. It sits BENEATH every seam the suite stubs, so the stubs in
``tests/conftest.py`` are what is proved, never bypassed.

Two ways in:

* the ``rekordbox_on_the_host`` fixture in ``tests/conftest.py``, for one test;
* this module as a pytest plugin, for the whole suite as it would run on a Mac
  with rekordbox open::

      .venv/bin/python -m pytest -p tests._host_processes

  The plugin installs the fake host for the life of the session, so the
  conftest's stubs and tripwire sit on top of it exactly as they sit on top of
  the real psutil, and a test that opts into the real table sees rekordbox.
"""

from __future__ import annotations

from collections.abc import Iterator

import psutil
import pytest

#: The two processes the host fakes, at pids past any platform's pid ceiling so
#: they can never be a real process's: macOS stops at 99998 and Linux at 2**22.
OPEN: dict[int, str] = {2**31 - 3: "rekordbox", 2**31 - 2: "rekordboxAgent"}


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
    """Put rekordbox and its agent on the host's process table, on ``monkeypatch``.

    The real listing stays: every real process is still listed and read by
    psutil itself, so a reader of the current process, the memory probe or a
    lock holder's liveness, answers as before.
    """
    real_pids = psutil.pids
    real_process = psutil.Process

    class Process(real_process):  # type: ignore[misc, valid-type]
        def __new__(cls, pid: int | None = None):  # noqa: D102
            if pid in OPEN:
                return _Open(pid, OPEN[pid])
            return super().__new__(cls)

    def pids() -> list[int]:
        return sorted({*real_pids(), *OPEN})

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
