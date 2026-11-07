"""U211: a process the rekordbox scan cannot read never ends a gated write as INTERNAL.

Sitting 54 ended a live ``crate sync pair`` apply, both gates answered, as
``INTERNAL: SystemError: <built-in function proc_cmdline> returned a result
with an exception set``. A Pioneer daemon had leaked hundreds of zombies, and
psutil's ``name()`` on macOS reads the command line for a long name, which
raised out of a process as it died.

Every scenario the brief names is driven here against a fake process table
that raises exactly what psutil raises, with psutil's own exception classes:
the scan itself, the writer's pyrekordbox probe and the binding's own probe at
open and commit, a gated ``sync pair`` through the dispatcher that meets the
refusal and is continued with ``--run``, and doctor's two process checks.
"""

from __future__ import annotations

import psutil
import pytest

from cratekit.cli import doctor, gates
from cratekit.core import processes, rb_writer
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.cli_drive import drive
from tests.test_analysis_store import contained as contained  # noqa: PLC0414
from tests.test_analysis_store import rclone_on_path as rclone_on_path  # noqa: PLC0414
from tests.test_analysis_store import volume as volume  # noqa: PLC0414
from tests.test_doctor import configured as configured  # noqa: PLC0414
from tests.test_doctor import find, probes
from tests.test_doctor import library as library  # noqa: PLC0414
from tests.test_sync_pair import ACCOUNT
from tests.test_sync_pair import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_pair import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_sync_pair import cfg as cfg  # noqa: PLC0414
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_sync_pair import sync as sync_both
from tests.test_sync_pair import world as world  # noqa: PLC0414

#: The writer's two probes as shipped, captured before any fixture fakes them,
#: so the end to end scenario drives their fallback rather than a stand in.
REAL_PROBES = {
    "rekordbox_running": rb_writer.rekordbox_running,
    "rekordbox_agent_running": rb_writer.rekordbox_agent_running,
}

#: The error the sitting met, word for word.
DYING = SystemError("<built-in function proc_cmdline> returned a result with an exception set")


# ═══════════════════════════════════════════════════════════════════════════
# A process table that fails the way psutil fails
# ═══════════════════════════════════════════════════════════════════════════


class FakeProcess:
    """One process: a name, or what reading it raises, and a status, or what that raises."""

    def __init__(self, pid, *, name=None, raises=None, status=psutil.STATUS_RUNNING, status_raises=None):
        self.pid = pid
        self._name = name
        self._raises = raises
        self._status = status
        self._status_raises = status_raises

    def name(self):
        if self._raises is not None:
            raise self._raises
        return self._name

    def status(self):
        if self._status_raises is not None:
            raise self._status_raises
        return self._status


class FakeTable:
    """psutil's surface the scan reads: ``pids``, ``Process`` and the exception classes."""

    NoSuchProcess = psutil.NoSuchProcess
    ZombieProcess = psutil.ZombieProcess
    AccessDenied = psutil.AccessDenied
    STATUS_ZOMBIE = psutil.STATUS_ZOMBIE

    def __init__(self, *processes_, built_raises=None, pids_raises=None):
        self._by_pid = {one.pid: one for one in processes_}
        self._built_raises = dict(built_raises or {})
        self._pids_raises = pids_raises

    def pids(self):
        if self._pids_raises is not None:
            raise self._pids_raises
        return sorted({*self._by_pid, *self._built_raises})

    def Process(self, pid):  # noqa: N802 - psutil's own name
        if pid in self._built_raises:
            raised = self._built_raises[pid]
            if isinstance(raised, list):
                # One answer per construction, so a process can fail as it is
                # built and read differently the second time it is asked.
                raise raised.pop(0)
            raise raised
        return self._by_pid[pid]


def rekordbox(pid=100):
    return FakeProcess(pid, name="rekordbox")


def agent(pid=101):
    return FakeProcess(pid, name="rekordboxAgent")


def finder(pid=200):
    return FakeProcess(pid, name="Finder")


@pytest.fixture
def table(monkeypatch):
    """Install a fake process table as the platform, and hand back the installer."""

    def install(*processes_, **kwargs) -> FakeTable:
        made = FakeTable(*processes_, **kwargs)
        monkeypatch.setattr(processes, "_platform", lambda: made)
        return made

    return install


def _scanned() -> tuple[str, ...]:
    return processes.rekordbox_processes_running()


# ═══════════════════════════════════════════════════════════════════════════
# The scan
# ═══════════════════════════════════════════════════════════════════════════


def test_a_readable_rekordbox_is_reported_running(table):
    table(finder(), rekordbox(), agent())
    assert _scanned() == ("rekordbox", "rekordboxAgent")
    assert processes.running_process_names() == ("rekordbox", "rekordboxAgent", "Finder")


def test_a_machine_with_no_rekordbox_reads_clear(table):
    table(finder(), FakeProcess(201, name="Safari"))
    assert _scanned() == ()


@pytest.mark.parametrize(
    "raised",
    [psutil.NoSuchProcess(300), psutil.AccessDenied(300), psutil.ZombieProcess(300)],
    ids=["gone", "denied", "zombie"],
)
def test_a_process_psutil_reports_gone_denied_or_zombie_is_skipped(table, raised):
    table(FakeProcess(300, raises=raised), rekordbox(), finder())
    assert _scanned() == ("rekordbox",)
    assert "Finder" in processes.running_process_names()


@pytest.mark.parametrize(
    "raised",
    [psutil.NoSuchProcess(300), psutil.AccessDenied(300), psutil.ZombieProcess(300)],
    ids=["gone", "denied", "zombie"],
)
def test_a_skipped_process_alone_leaves_the_machine_clear(table, raised):
    table(FakeProcess(300, raises=raised), finder())
    assert _scanned() == ()


def test_a_system_error_on_a_process_whose_status_reads_zombie_is_skipped(table):
    """The sitting's own case: the dying daemon, read as it died."""
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), finder())
    assert _scanned() == ()


@pytest.mark.parametrize(
    "status_raises",
    [psutil.NoSuchProcess(300), psutil.ZombieProcess(300)],
    ids=["gone", "zombie"],
)
def test_a_system_error_on_a_process_then_gone_or_zombie_is_skipped(table, status_raises):
    table(FakeProcess(300, raises=DYING, status_raises=status_raises), rekordbox())
    assert _scanned() == ("rekordbox",)


def test_a_system_error_on_a_live_process_refuses_naming_the_pid(table):
    table(FakeProcess(300, raises=DYING), finder())
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    cause = caught.value.cause
    assert cause.reason == processes.UNCONFIRMED == "rekordbox-absence-unconfirmed"
    assert cause.code is ExitCode.REKORDBOX_OPEN
    assert cause.code is not ExitCode.INTERNAL
    assert "process 300" in cause.message
    assert "SystemError" in cause.message
    assert "rekordbox's absence could not be confirmed" in cause.message
    assert cause.detail["pids"] == [300]
    assert cause.remediation.remedy is Remedy.RETRY_LATER
    assert any("ps -p 300" in step for step in cause.remediation.steps)


def test_a_live_process_whose_status_is_unreadable_too_refuses(table):
    table(FakeProcess(300, raises=DYING, status_raises=psutil.AccessDenied(300)))
    with pytest.raises(processes.AbsenceUnconfirmed):
        _scanned()


@pytest.mark.parametrize(
    "raised",
    [RuntimeError("an answer this reader has never seen"), OSError(5, "Input/output error")],
    ids=["runtime", "os"],
)
def test_any_other_error_on_a_live_process_refuses_rather_than_reading_absent(table, raised):
    table(FakeProcess(300, raises=raised))
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    assert caught.value.cause.detail["pids"] == [300]


def test_a_process_that_cannot_even_be_built_is_judged_the_same_way(table):
    """psutil builds a process before it reads one, and building can raise as well."""
    table(finder(), built_raises={300: DYING})
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    assert caught.value.cause.detail["pids"] == [300]


def test_a_process_that_fails_to_build_and_is_then_gone_is_skipped(table):
    table(finder(), built_raises={300: [DYING, psutil.NoSuchProcess(300)]})
    assert _scanned() == ()


def test_a_process_list_that_cannot_be_read_refuses_with_no_pid(table):
    table(pids_raises=OSError(1, "Operation not permitted"))
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    cause = caught.value.cause
    assert cause.detail["pids"] == []
    assert "list of running processes could not be read" in cause.message


def test_the_whole_list_is_walked_and_every_unreadable_pid_is_named(table):
    table(
        FakeProcess(300, raises=DYING),
        finder(),
        FakeProcess(301, raises=DYING),
        FakeProcess(302, raises=DYING, status=psutil.STATUS_ZOMBIE),
    )
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    assert caught.value.cause.detail["pids"] == [300, 301]
    assert caught.value.read == ((200, "Finder"),)


def test_many_unreadable_pids_are_counted_past_the_named_ones(table):
    dying = [FakeProcess(300 + n, raises=DYING) for n in range(processes.NAMED_PIDS + 3)]
    table(*dying)
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        _scanned()
    assert "and 3 more" in caught.value.cause.message
    assert len(caught.value.cause.detail["pids"]) == processes.NAMED_PIDS + 3


def test_a_rekordbox_the_scan_did_read_is_running_whatever_else_was_unreadable(table):
    """Running is established, so it is the answer; unknown is only for a scan that saw none."""
    table(FakeProcess(300, raises=DYING), agent())
    assert _scanned() == ("rekordboxAgent",)


def test_the_careful_pid_answers_as_pyrekordbox_does(table):
    table(finder(), rekordbox(pid=4242), FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE))
    assert processes.rekordbox_pid("rekordbox") == 4242
    assert processes.rekordbox_pid("rekordboxAgent") == 0


def test_the_careful_pid_refuses_over_an_unreadable_live_process(table):
    table(finder(), FakeProcess(300, raises=DYING))
    with pytest.raises(processes.AbsenceUnconfirmed):
        processes.rekordbox_pid("rekordbox")


def test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process(table):
    table(rekordbox(pid=4242), FakeProcess(300, raises=DYING))
    assert processes.rekordbox_pid("rekordbox") == 4242
    with pytest.raises(processes.AbsenceUnconfirmed):
        processes.rekordbox_pid("rekordboxAgent")


def test_the_scan_does_not_use_process_iter(table, monkeypatch):
    """The iterator dies with the first error it meets, which is the defect itself."""

    def refused(*_args, **_kwargs):
        raise AssertionError("process_iter was used")

    monkeypatch.setattr(psutil, "process_iter", refused)
    table(rekordbox())
    assert _scanned() == ("rekordbox",)


def test_the_seam_is_psutil_when_nothing_replaces_it():
    """Not a read of this machine's process table, which no test may depend on."""
    assert processes._platform() is psutil


# ═══════════════════════════════════════════════════════════════════════════
# The writer's mechanism, through pyrekordbox
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def real_probes(monkeypatch):
    """The writer's probes as shipped, over a pyrekordbox scan that meets the dying process."""
    for name, probe in REAL_PROBES.items():
        monkeypatch.setattr(rb_writer, name, probe)

    def dying_iter(*_args, **_kwargs):
        # pyrekordbox's own walk, meeting the process as the sitting's did.
        yield FakeProcess(300, raises=DYING)

    monkeypatch.setattr(psutil, "process_iter", dying_iter)


def test_pyrekordbox_alone_lets_the_dying_process_escape(real_probes):
    """The defect, measured on the binding this tree ships, so the fallback is needed."""
    from pyrekordbox.utils import get_rekordbox_pid

    with pytest.raises(SystemError):
        get_rekordbox_pid()


def test_the_writer_skips_a_zombie_pyrekordbox_could_not_read(real_probes, table):
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), finder())
    assert rb_writer.rekordbox_processes_running() == ""
    rb_writer.assert_rekordbox_closed("committing")


def test_the_writer_still_sees_rekordbox_beside_the_dying_process(real_probes, table):
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), rekordbox())
    with pytest.raises(rb_writer.RekordboxRunning):
        rb_writer.assert_rekordbox_closed("committing")


def test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal(real_probes, table):
    table(FakeProcess(300, raises=DYING), finder())
    with pytest.raises(processes.AbsenceUnconfirmed) as caught:
        rb_writer.assert_rekordbox_closed("committing")
    assert caught.value.cause.reason == processes.UNCONFIRMED
    assert isinstance(caught.value, CratekitError)


def test_a_missing_binding_is_not_read_as_a_scan_that_failed(monkeypatch, table):
    """ImportError is the install's problem, and the scan must not paper over it."""
    import builtins

    monkeypatch.setattr(rb_writer, "rekordbox_running", REAL_PROBES["rekordbox_running"])
    real_import = builtins.__import__

    def no_binding(name, *args, **kwargs):
        if name == "pyrekordbox.utils":
            raise ImportError("no pyrekordbox")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_binding)
    table(finder())
    with pytest.raises(ImportError):
        rb_writer.rekordbox_running()


# ═══════════════════════════════════════════════════════════════════════════
# The binding's own probe, at open and at commit
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def dying_binding(monkeypatch):
    """pyrekordbox's database module probing a process table that holds the dying process."""
    from pyrekordbox.db6 import database as binding

    def probe(*_args, **_kwargs):
        raise DYING

    monkeypatch.setattr(binding, "get_rekordbox_pid", probe)
    return binding


def test_the_binding_probe_skips_a_zombie_at_commit(dying_binding, table):
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE))
    with rb_writer._binding_probe(strict=True):
        assert dying_binding.get_rekordbox_pid() == 0
    with pytest.raises(SystemError):
        dying_binding.get_rekordbox_pid()


def test_the_binding_probe_names_rekordbox_at_commit(dying_binding, table):
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), rekordbox(pid=4242))
    with rb_writer._binding_probe(strict=True):
        assert dying_binding.get_rekordbox_pid() == 4242


def test_the_binding_probe_refuses_a_live_unreadable_process_at_commit(dying_binding, table):
    table(FakeProcess(300, raises=DYING))
    with rb_writer._binding_probe(strict=True), pytest.raises(processes.AbsenceUnconfirmed):
        dying_binding.get_rekordbox_pid()


def test_the_binding_probe_at_open_only_loses_a_warning(dying_binding, table):
    """At construction the binding only logs whether rekordbox runs; the writer's guard has asked already."""
    table(FakeProcess(300, raises=DYING))
    with rb_writer._binding_probe(strict=False):
        assert dying_binding.get_rekordbox_pid() == 0


def test_the_binding_probe_keeps_an_answer_the_binding_could_give(monkeypatch, table):
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *a, **k: 77)
    table(FakeProcess(300, raises=DYING))
    with rb_writer._binding_probe(strict=True):
        assert binding.get_rekordbox_pid() == 77


def test_the_binding_probe_is_put_back_after_a_refusal(dying_binding, table):
    original = dying_binding.get_rekordbox_pid
    table(FakeProcess(300, raises=DYING))
    with pytest.raises(processes.AbsenceUnconfirmed):
        with rb_writer._binding_probe(strict=True):
            dying_binding.get_rekordbox_pid()
    assert dying_binding.get_rekordbox_pid is original


# ═══════════════════════════════════════════════════════════════════════════
# A gated sync pair that meets the refusal, then continues with --run
# ═══════════════════════════════════════════════════════════════════════════


def _answered(w) -> str:
    """Both explicit gates answered apply, as a person answers them, and the run id."""
    code, first = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    for _ in range(2):
        code, asked = drive(["--run", run_id, *w.args()])
        if code != int(ExitCode.DECISION_REQUIRED):
            break
        gate = asked["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
    return run_id


def test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run(
    world, cfg, monkeypatch, table, dying_binding
):
    """The brief's end to end scenario, on a pair already marked as the sitting's were.

    Both gates are answered by a person, the write meets the scan, the run is
    kept with both answers, and ``--run`` writes both sides once the process
    has finished dying, with no gate asked again.
    """
    w = world(account=("1", "2"), rekordbox=("2", "3"))
    assert sync_both(w.args())[0] == int(ExitCode.OK)
    before = pairs.PairStore(cfg).get(ACCOUNT)
    w.account.playlists[ACCOUNT].append("t4")
    w.rekordbox_add("5")

    code, first = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    drive(["run", "decide", run_id, pair_cli.REKORDBOX_GATE, "apply", "--actor", "a-person"])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, "apply", "--actor", "a-person"])

    # The writer's probes as shipped, over a pyrekordbox walk that meets the
    # dying process, at the write.
    for name, probe in REAL_PROBES.items():
        monkeypatch.setattr(rb_writer, name, probe)

    def pyrekordbox_meets_it(*_args, **_kwargs):
        raise DYING

    import pyrekordbox.utils

    monkeypatch.setattr(pyrekordbox.utils, "get_rekordbox_pid", pyrekordbox_meets_it)
    monkeypatch.setattr(pyrekordbox.utils, "get_rekordbox_agent_pid", pyrekordbox_meets_it)
    table(FakeProcess(300, raises=DYING), finder())

    code, refused = drive(["--run", run_id, *w.args()])

    assert code == int(ExitCode.REKORDBOX_OPEN), refused
    assert refused["cause"]["reason"] == processes.UNCONFIRMED
    assert refused["resumable"] is True
    assert refused["outcome"] == "blocked"
    assert refused["run_id"] == run_id
    command = refused["cause"]["detail"]["continue"]
    assert command == f"crate --run {run_id} sync pair {ACCOUNT} --rekordbox {w.rekordbox_id}"
    steps = refused["cause"]["remediation"]["steps"]
    assert command in steps[0]
    assert steps[0].startswith("wait a moment for the process to finish exiting")
    # No step tells the person to start again, which would lose the answers.
    assert not any("run it again" in step for step in steps), steps
    assert "process 300" in refused["cause"]["message"]
    # Nothing was written on either side and the snapshot did not move.
    assert "5" in w.held() and "4" not in w.held()
    assert w.on_account() == ["t1", "t2", "t3", "t4"]
    assert pairs.PairStore(cfg).get(ACCOUNT).account == before.account
    # Both answers are still on the run.
    kept = gates.load(run_id)
    assert set(kept.decisions) == {pair_cli.REKORDBOX_GATE, pair_cli.ACCOUNT_GATE}

    # The process finished dying: a zombie now, which the writer's probes, the
    # scan and the binding's own probe at commit all skip.
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), finder())
    code, done = drive(["--run", run_id, *w.args()])

    assert code == int(ExitCode.OK), done
    assert "4" in w.held()
    assert "t5" in w.on_account()
    assert pairs.PairStore(cfg).get(ACCOUNT).account != before.account



def test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host(
    rekordbox_on_the_host, world, cfg, monkeypatch, table, dying_binding
):
    """U232: on a Mac with rekordbox open this exited 1 where it expects 0.

    The binding's own probe at commit, ``pyrekordbox.db6.database``'s bound
    ``get_rekordbox_pid``, walked the real host and refused the commit. The
    same scenario over a host listing rekordbox and its agent at psutil itself.
    """
    test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run(
        world, cfg, monkeypatch, table, dying_binding
    )

def test_a_rekordbox_running_refusal_still_ends_the_run_as_failed(world, monkeypatch):
    """The kept set is this one cause, not every refusal on rekordbox's code."""
    w = world(account=("1",), rekordbox=("2",))
    run_id = _answered(w)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.REKORDBOX_OPEN), refused
    assert refused["cause"]["reason"] == "rekordbox-running"
    assert refused["resumable"] is False
    assert refused["outcome"] == "failed"


# ═══════════════════════════════════════════════════════════════════════════
# Doctor reads it the same way
# ═══════════════════════════════════════════════════════════════════════════


def test_doctor_reads_a_skipped_zombie_as_nothing(configured, table):
    table(FakeProcess(300, raises=DYING, status=psutil.STATUS_ZOMBIE), finder())
    report = doctor.run(configured, probes=probes(process_lister=processes.running_process_names))
    closed = find(report, "rekordbox.closed")
    assert closed.status is doctor.Status.OK, closed


def test_doctor_names_an_unreadable_live_process_as_a_note(configured, table):
    table(FakeProcess(300, raises=DYING), finder())
    report = doctor.run(configured, probes=probes(process_lister=processes.running_process_names))
    closed = find(report, "rekordbox.closed")
    assert closed.status is doctor.Status.INFO, closed
    assert "process 300" in closed.detail
    assert "could not be confirmed" in closed.detail
    resolved = find(report, "library.paths_resolved")
    assert resolved.status is doctor.Status.INFO, resolved
    assert "process 300" in resolved.detail
    assert "no copy" in resolved.detail


def test_doctor_still_fails_a_running_rekordbox_beside_an_unreadable_process(configured, table):
    table(FakeProcess(300, raises=DYING), rekordbox())
    report = doctor.run(configured, probes=probes(process_lister=processes.running_process_names))
    closed = find(report, "rekordbox.closed")
    assert closed.status is doctor.Status.FAIL, closed
    assert closed.remedy is Remedy.QUIT_REKORDBOX


# ═══════════════════════════════════════════════════════════════════════════
# Round one's fixes: one answer from both mechanisms, the backup's files
# portion, and a continue step that does not say to start again
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "read",
    [(), (rekordbox(),), (agent(),), (rekordbox(), agent())],
    ids=["none", "rekordbox", "agent", "both"],
)
def test_both_mechanisms_agree_beside_a_live_unreadable_process(real_probes, table, read):
    """The writer asks one name at a time, and still answers what the scan read."""
    table(FakeProcess(300, raises=DYING), finder(), *read)
    try:
        from_scan = processes.rekordbox_processes_running()
    except processes.AbsenceUnconfirmed:
        from_scan = None
    try:
        from_writer = rb_writer.rekordbox_processes_running()
    except processes.AbsenceUnconfirmed:
        from_writer = None
    if not read:
        assert from_scan is None and from_writer is None
    else:
        assert from_scan == tuple(one._name for one in read)
        assert from_writer == ", ".join(from_scan)


def test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed(real_probes, table):
    """The agent settling after a quit is running; waiting for a dying process will not clear it."""
    table(FakeProcess(300, raises=DYING), agent())
    with pytest.raises(rb_writer.RekordboxRunning) as caught:
        rb_writer.assert_rekordbox_closed("committing")
    assert caught.value.cause.reason == "rekordbox-running"
    assert "rekordboxAgent" in caught.value.cause.message


def test_a_backup_refuses_the_database_portion_alone_and_still_mirrors(
    contained, rclone_on_path, table
):
    """The files portion runs; the database portion names the unreadable pid."""
    from cratekit.core import backup_facts, config
    from cratekit.modules.tools import backup

    database = config.state_path("rekordbox_db", contained)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"SQLite format 3\x00")
    table(FakeProcess(300, raises=DYING), finder())
    plan = backup.plan_backup(
        contained, process_lister=processes.running_process_names, settings_dirs=()
    )

    database = plan.portion(backup_facts.Portion.DATABASE)
    assert database.refusal is backup.Refusal.REKORDBOX_ABSENCE_UNCONFIRMED
    assert "process 300" in database.detail
    assert "no snapshot of the database was taken" in database.detail
    files = [one for one in plan.portions if one.portion is not backup_facts.Portion.DATABASE]
    assert files, "the plan has no portion but the database"
    assert all(one.will_run for one in files), [(one.portion, one.refusal) for one in files]
