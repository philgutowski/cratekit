"""U232: the suite reads the same whether or not rekordbox is running on the host.

The v0.13.0 cut was refused on a red Mac battery because rekordbox was open on
the machine, and two tests read the host's real process table. ``tests/conftest.py``
now answers both routes to that table as a machine with no rekordbox, and trips
on psutil's own enumeration beneath them. This file proves the three halves of
that: the stubs answer clear with rekordbox open on the host, a test that opts
in by name still reads the real host, and a test that reaches psutil's
enumeration without the opt in fails, even when the code it called swallowed
the refusal. The fake host is ``tests/_host_processes.py``, installed at psutil
itself so it is what the real scan would read.
"""

from __future__ import annotations

import os

import psutil
import pyrekordbox.utils
import pytest
from pyrekordbox.db6 import database

from cratekit.core import processes, rb_writer
from tests import _host_processes
from tests.conftest import REAL_PROCESS_TABLE

pytest_plugins = ("pytester",)

#: pyrekordbox's own walk, captured at import, before any fixture stubs it.
REAL_WALK = pyrekordbox.utils.get_process_id


# ═══════════════════════════════════════════════════════════════════════════
# rekordbox open on the host, read through the stubs
# ═══════════════════════════════════════════════════════════════════════════


def test_the_fake_host_lists_rekordbox_and_its_agent(rekordbox_on_the_host):
    listed = {pid: psutil.Process(pid).name() for pid in psutil.pids() if pid in rekordbox_on_the_host}
    assert listed == _host_processes.OPEN
    assert sorted(proc.name() for proc in psutil.process_iter() if proc.pid in rekordbox_on_the_host) == [
        "rekordbox",
        "rekordboxAgent",
    ]
    # The real listing is still there, read by psutil itself.
    assert os.getpid() in psutil.pids()
    assert psutil.Process().pid == os.getpid()


def test_the_careful_scan_reads_no_rekordbox_with_rekordbox_open_on_the_host(rekordbox_on_the_host):
    assert processes.running_processes() == ()
    assert processes.running_process_names() == ()
    assert processes.rekordbox_processes_running() == ()
    assert processes.rekordbox_pid("rekordbox") == 0
    assert processes.rekordbox_pid("rekordboxAgent") == 0


def test_pyrekordbox_reads_no_rekordbox_with_rekordbox_open_on_the_host(rekordbox_on_the_host):
    assert pyrekordbox.utils.get_rekordbox_pid() == 0
    assert pyrekordbox.utils.get_rekordbox_agent_pid() == 0
    # The binding's own name, which construction and commit ask, is covered too.
    assert database.get_rekordbox_pid() == 0
    with pytest.raises(RuntimeError, match="No process with name 'rekordbox' found!"):
        pyrekordbox.utils.get_rekordbox_pid(raise_exec=True)


def test_the_writers_guard_reads_clear_with_rekordbox_open_on_the_host(rekordbox_on_the_host):
    assert rb_writer.rekordbox_running() is False
    assert rb_writer.rekordbox_agent_running() is False
    assert rb_writer.rekordbox_processes_running() == ""
    rb_writer.assert_rekordbox_closed("a test's write")


def test_a_test_that_fakes_rekordbox_at_the_seam_still_sees_it(rekordbox_on_the_host, monkeypatch):
    """The stubs are a default: a test's own fake, on its own ``monkeypatch``, wins."""
    monkeypatch.setattr(pyrekordbox.utils, "get_process_id", lambda name, raise_exec=False: 7)
    assert rb_writer.rekordbox_processes_running() == "rekordbox, rekordboxAgent"

    class Table:
        NoSuchProcess = psutil.NoSuchProcess
        ZombieProcess = psutil.ZombieProcess
        AccessDenied = psutil.AccessDenied
        STATUS_ZOMBIE = psutil.STATUS_ZOMBIE

        def pids(self):
            return [9]

        def Process(self, pid):  # noqa: N802 - psutil's own name
            return _host_processes._Open(pid, "rekordboxAgent")

    monkeypatch.setattr(processes, "_platform", Table)
    assert processes.rekordbox_processes_running() == ("rekordboxAgent",)


# ═══════════════════════════════════════════════════════════════════════════
# The opt in, by name
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.real_process_table
def test_a_test_opted_in_reads_the_real_host():
    assert processes._platform() is psutil
    assert pyrekordbox.utils.get_process_id is REAL_WALK
    try:
        listed = processes.running_processes()
    except processes.AbsenceUnconfirmed as exc:
        # A host process the scan could not read is the host's own business;
        # what it did read is still the real table.
        listed = exc.read
    assert (os.getpid(), psutil.Process().name()) in listed


@pytest.mark.real_process_table
def test_the_fake_host_is_what_the_real_scan_reads(rekordbox_on_the_host):
    """The fake host models the Mac the cut was refused on, read without the stubs.

    pyrekordbox answers the FIRST process of a name, so on a host where
    rekordbox is really open that is the real one, never asserted to be a
    faked pid (U232, review round one): what is asserted is that the walk
    finds a rekordbox and that the faked pids are on the table it walks.
    """
    assert processes.rekordbox_processes_running() == ("rekordbox", "rekordboxAgent")
    for found, name in (
        (pyrekordbox.utils.get_rekordbox_pid(), "rekordbox"),
        (pyrekordbox.utils.get_rekordbox_agent_pid(), "rekordboxAgent"),
        (database.get_rekordbox_pid(), "rekordbox"),
    ):
        assert found != 0
        assert psutil.Process(found).name() == name
    # Names read for the faked pids only: a real process can be gone or denied
    # by the time it is read, which is the host's business, not this test's.
    walked = {proc.pid: proc for proc in psutil.process_iter()}
    assert {pid: walked[pid].name() for pid in rekordbox_on_the_host if pid in walked} == _host_processes.OPEN
    assert rb_writer.rekordbox_processes_running() == "rekordbox, rekordboxAgent"


def test_the_marker_is_registered(pytestconfig):
    assert any(line.startswith(f"{REAL_PROCESS_TABLE}:") for line in pytestconfig.getini("markers"))


# ═══════════════════════════════════════════════════════════════════════════
# The guard: a test that reaches the real table without the opt in fails
# ═══════════════════════════════════════════════════════════════════════════

INNER = '''
import psutil
import pytest

from cratekit.core import processes, rb_writer


def test_reaches_process_iter_and_swallows_the_refusal():
    try:
        list(psutil.process_iter())
    except Exception:
        pass


def test_reaches_pids_through_the_careful_scan_which_swallows_it():
    with pytest.raises(processes.AbsenceUnconfirmed):
        processes.running_processes(platform=psutil)


def test_the_stubbed_seams_never_reach_psutil():
    assert processes.rekordbox_processes_running() == ()
    assert rb_writer.rekordbox_processes_running() == ""


@pytest.mark.real_process_table
def test_opted_in_reaches_both():
    assert psutil.pids()
    assert next(iter(psutil.process_iter())) is not None
'''


def _inner_run(pytester):
    pytester.makeconftest(open(os.path.join(os.path.dirname(__file__), "conftest.py"), encoding="utf-8").read())
    pytester.makepyfile(test_inner=INNER)
    return pytester.runpytest_inprocess("-p", "no:cacheprovider")


@pytest.mark.real_process_table
def test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails(pytester):
    """Over the real conftest, in an inner session of its own.

    The inner session runs in this process, so this test carries the opt in
    itself: the inner session's own fixtures are the only ones that act.
    """
    result = _inner_run(pytester)

    result.assert_outcomes(passed=4, errors=2)
    out = result.stdout.str()
    assert "ERROR at teardown of test_reaches_process_iter_and_swallows_the_refusal" in out
    assert "ERROR at teardown of test_reaches_pids_through_the_careful_scan_which_swallows_it" in out
    assert "reached the host's real process table without the real_process_table marker" in out
    assert "psutil.process_iter was called from" in out
    assert "psutil.pids was called from" in out
    # The line that reached it is named, so the failure points at the test.
    assert "list(psutil.process_iter())" in out
