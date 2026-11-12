"""U241: ``analyze run`` measures its heads ahead of the driver, with no worse results.

The claim is "the same answer, sooner", so the first test here runs one folder
twice through the real verb, once on a machine refused a pool and once on a
machine that affords four workers, and holds the two folders to the same
bytes: every file's name, every file's content after the tag write, every
committed report and every item's state. The rest drive the ways a head
measured ahead can stop being the head the driver would measure, and what the
run says about its pool on both of a queued verb's exits.

THE WORKERS ARE REAL. Every pooled case spawns children that import this
module by name, which is why the detector here is a module level function
rather than the closure the other analysis suites bind: a closure cannot
reach a spawned child, and a pool that was never crossed proves nothing about
crossing it. The machine is not real: cores, available memory and pressure are
injected, so no case depends on what this container is doing.
"""

from __future__ import annotations

import hashlib
import multiprocessing
import os
import shutil
import signal
import time
from pathlib import Path

import numpy as np
import pytest

from cratekit.analysis import ahead, artifacts, detect, energy, light, vocals
from cratekit.analysis import cli as analysis_cli
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, cores, jobs, pool, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.cli_drive import drive, drive_human
from tests.test_analysis import _FakeModel
from tests.test_config import valid_data

GIB = 1024**3
MIB = 1024**2

#: Where a head leaves a mark saying which process measured it, and the process
#: that is the driver, both read from the environment so a spawned worker sees
#: what the test set.
SEEN = "CRATEKIT_AHEAD_SEEN"
DRIVER = "CRATEKIT_AHEAD_DRIVER"


# ---------------------------------------------------------------------------
# A detector a spawned worker can import
# ---------------------------------------------------------------------------


def fake_head(path: Path) -> dict | None:
    """A head read off the file's NAME, the same in every process, marked with who read it.

    The names steer it: ``slow`` waits in a worker, so later files finish
    first; ``dies`` takes its worker down; ``raises`` raises wherever it runs;
    ``keyless`` finds no key; ``broken`` could not be decoded.
    """
    name = path.name
    in_a_worker = str(os.getpid()) != os.environ.get(DRIVER, "")
    marks = os.environ.get(SEEN)
    if marks:
        Path(marks, f"{name}@{os.getpid()}").write_text("")
    if name.startswith("slow") and in_a_worker:
        time.sleep(0.6)
    if name.startswith("dies") and in_a_worker:
        os._exit(70)
    if name.startswith("raises"):
        raise RuntimeError(f"{name} cannot be measured")
    if name.startswith("keyless"):
        return None
    if name.startswith("broken"):
        return {"path": path, "terminal": detect.TERMINAL_UNDECODABLE}
    total = sum(name.encode())
    return {
        "path": path,
        "camelot": f"{total % 12 + 1}{'AB'[total % 2]}",
        "rate": 100 + total % 60,
        "drift": (total % 9) / 10.0,
        "drift_verdict": "steady",
        "energy": 1 + total % 10,
        "energy_status": energy.STATUS_CALIBRATED,
    }


def bind_fake_in_a_worker() -> None:
    """A worker's initializer: the same detector the driver has bound."""
    light.bind_detect(fake_head)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture(autouse=True)
def bound(monkeypatch, tmp_path):
    """The importable detector here and in the workers, a fake model, and the marks."""
    marks = tmp_path / "marks"
    marks.mkdir()
    monkeypatch.setenv(SEEN, str(marks))
    monkeypatch.setenv(DRIVER, str(os.getpid()))
    monkeypatch.setattr(light, "_DETECT", fake_head)
    monkeypatch.setattr(ahead, "_WORKER_BINDING", (bind_fake_in_a_worker, ()))
    monkeypatch.setattr(ahead, "_SESSIONS", {})
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _FakeModel)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(16000, 0.2, dtype=np.float32))
    yield marks
    for job_id in list(ahead._SESSIONS):
        ahead.close_session(job_id)


def machine(monkeypatch, *, core_count=6, available=64 * GIB, swap=0, used=10.0) -> None:
    """The machine the planner reads: cores, available bytes, and what it is already paying."""
    monkeypatch.setattr(cores, "usable_cores", lambda: core_count)
    monkeypatch.setattr(pool, "available_bytes", lambda: available)
    monkeypatch.setattr(
        pool, "memory_pressure", lambda: pool.Pressure(swap_used_bytes=swap, used_percent=used)
    )


NAMES = ("slow a", "b", "slow c", "d", "e", "keyless f", "broken g", "h")


def fill(folder: Path, silence: Path, names=NAMES) -> Path:
    folder.mkdir()
    for name in names:
        shutil.copy2(silence, folder / f"{name}.flac")
    return folder


def measured_by(marks: Path) -> dict[str, set[int]]:
    """Which processes measured each file, read off the marks the detector left."""
    found: dict[str, set[int]] = {}
    for mark in marks.iterdir():
        name, _, pid = mark.name.rpartition("@")
        found.setdefault(name, set()).add(int(pid))
    return found


def job_of(envelope: dict) -> str:
    return (envelope.get("data") or {}).get("job_id") or envelope["cause"]["detail"]["job_id"]


def states(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {item.item_id: str(item.state) for item in jobs.items(store, job_id)}


def resume_argv(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def what_is_on_disk(folder: Path) -> dict[str, str]:
    """Every file's name and the digest of its bytes, which holds every tag written."""
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(folder.iterdir())
    }


def reports_of(cfg, job_id: str, folder: Path) -> list[dict]:
    """The committed reports with the folder taken off each path, so two folders compare."""
    cleaned = []
    for report in artifacts.committed(cfg, job_id):
        report = dict(report)
        report["path"] = Path(report["path"]).name
        cleaned.append(report)
    return cleaned


def pool_check(envelope: dict) -> dict:
    (check,) = envelope["data"]["progress"]["analysis"]["checks"]
    assert check["key"] == "analyze.pool"
    return check


# ---------------------------------------------------------------------------
# No worse results: the pooled run against the serial run, on the same inputs
# ---------------------------------------------------------------------------


def test_a_pooled_run_leaves_exactly_what_the_serial_run_leaves(
    cfg, silence, tmp_path, monkeypatch, bound
):
    """The whole claim, through the verb: same names, same bytes, same reports, same states."""
    serial_folder = fill(tmp_path / "serial", silence)
    pooled_folder = fill(tmp_path / "pooled", silence)

    machine(monkeypatch, swap=12 * GIB)
    code, serial = drive(["analyze", "run", str(serial_folder)])
    assert code == int(ExitCode.OK), serial
    serial_marks = measured_by(bound)
    assert {pid for pids in serial_marks.values() for pid in pids} == {os.getpid()}, (
        "a machine refused a pool measured a head outside the driver"
    )
    for mark in bound.iterdir():
        mark.unlink()

    machine(monkeypatch)
    code, pooled = drive(["analyze", "run", str(pooled_folder)])
    assert code == int(ExitCode.OK), pooled
    pooled_marks = measured_by(bound)
    assert set(pooled_marks) == {f"{name}.flac" for name in NAMES}
    assert all(os.getpid() not in pids for pids in pooled_marks.values()), (
        f"the driver measured a head a worker should have: {pooled_marks}"
    )
    assert all(len(pids) == 1 for pids in pooled_marks.values()), "a head was measured twice"
    assert multiprocessing.active_children() == [], "a worker outlived its run"

    assert what_is_on_disk(pooled_folder) == what_is_on_disk(serial_folder)
    assert reports_of(cfg, job_of(pooled), pooled_folder) == reports_of(
        cfg, job_of(serial), serial_folder
    )
    assert states(job_of(pooled)) == states(job_of(serial))
    assert set(states(job_of(pooled)).values()) == {"done"}
    assert (
        pooled["data"]["progress"]["analysis"]["by_status"]
        == serial["data"]["progress"]["analysis"]["by_status"]
        == {"analyzed": 6, "skipped-no-key": 1, "skipped-undecodable": 1}
    )
    # And the serial run is the run this unit did not change: one head, read back.
    done = next(path for path in serial_folder.iterdir() if path.name.endswith(" - b.flac"))
    expected = fake_head(Path("b.flac"))
    assert tags.read_tag(done, "initialkey") == f"{int(expected['camelot'][:-1]):02d}{expected['camelot'][-1]}"
    assert tags.read_energy_from_file(done) == expected["energy"]


def test_the_driver_settles_items_in_item_order_whatever_order_the_heads_finish(
    cfg, silence, tmp_path, monkeypatch
):
    """``slow a`` is still being measured while ``b`` is done; ``a`` is still settled first."""
    folder = fill(tmp_path / "ordered", silence, names=("slow a", "b", "c"))
    machine(monkeypatch)
    order: list[str] = []
    real = artifacts.produced

    def produced(cfg_, job, item, report):
        order.append(item.item_id)
        return real(cfg_, job, item, report)

    monkeypatch.setattr(artifacts, "produced", produced)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert order == ["b.flac", "c.flac", "slow a.flac"], "the items are the sorted names"


def test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker(
    cfg, silence, tmp_path, monkeypatch, bound
):
    folder = fill(tmp_path / "mixed", silence, names=("03A - 120 - done", "fresh", "gone", "more"))
    machine(monkeypatch)
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    (folder / "gone.flac").unlink()

    code, resumed = drive(resume_argv(job_of(queued)))

    assert code != int(ExitCode.OK), "a missing file is a failed item, as it was"
    assert set(measured_by(bound)) == {"fresh.flac", "more.flac"}
    pool_step = resumed["cause"]["remediation"]["steps"][-1]
    assert "2 of 2 waiting file(s) were read from them" in pool_step


# ---------------------------------------------------------------------------
# The check line, on a machine of each kind
# ---------------------------------------------------------------------------


def test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "healthy", silence)
    machine(monkeypatch, core_count=6)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    check = pool_check(done)
    assert check["status"] == "ok"
    assert check["detail"].startswith(
        "4 workers measured key, tempo and energy ahead of this process: the "
        "ceiling of 4 is what held it"
    )
    assert check["detail"].endswith("8 of 8 waiting file(s) were read from them")
    assert check["remedy"] is None


def test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "swapped", silence)
    machine(monkeypatch, core_count=11, swap=int(11.8 * GIB))
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    check = pool_check(done)
    assert check["status"] == "info"
    assert check["detail"] == (
        "one worker, this process: 11.8 GB of swap is in use, at or over the "
        "1.0 GB gate, so no pool was planned, under a ceiling of 9"
    )
    assert multiprocessing.active_children() == []


def test_a_machine_using_most_of_its_memory_names_the_used_percent_gate(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "full", silence)
    machine(monkeypatch, core_count=11, used=92.0)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert pool_check(done)["detail"] == (
        "one worker, this process: memory is 92 percent in use, at or over the "
        "85 percent gate, so no pool was planned, under a ceiling of 9"
    )


def test_memory_overrules_a_wide_core_count(cfg, silence, tmp_path, monkeypatch):
    """Sixty four cores and room for two workers is two workers, and the line says memory."""
    folder = fill(tmp_path / "tight", silence)
    cost = light.costliest(list(folder.iterdir()))
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES + vocals.VOCAL_WORKER_BYTES
    # Enough, after the reserve and the headroom, for two workers and not three.
    available = reserve + (2 * cost * 100) // pool.DEFAULT_HEADROOM_PERCENT + cost // 2
    machine(monkeypatch, core_count=64, available=available)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    check = pool_check(done)
    assert check["status"] == "info"
    assert check["detail"].startswith("2 workers measured key, tempo and energy ahead")
    assert "available affords 2 at" in check["detail"]
    assert "under a ceiling of 62" in check["detail"]


def test_two_cores_leave_no_ceiling_for_a_pool(cfg, silence, tmp_path, monkeypatch):
    folder = fill(tmp_path / "small", silence)
    machine(monkeypatch, core_count=2)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert pool_check(done)["detail"].startswith(
        "one worker, this process: the ceiling of 1 is what held it"
    )


def test_the_person_reads_the_check_line_without_asking_for_json(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "read", silence, names=("a", "b"))
    machine(monkeypatch)
    code, text = drive_human(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), text
    assert "  [ok  ] analyze.pool: 2 workers measured key, tempo and energy ahead" in text


def test_a_resume_of_a_finished_job_still_says_what_pool_it_ran_with(
    cfg, silence, tmp_path, monkeypatch
):
    """The line is read off the record the drive left, not out of this process's memory."""
    folder = fill(tmp_path / "again", silence, names=("a", "b", "c"))
    machine(monkeypatch)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    first = pool_check(done)
    monkeypatch.setattr(ahead, "_SESSIONS", {})
    code, again = drive(resume_argv(job_of(done)))
    assert code == int(ExitCode.OK), again
    assert pool_check(again) == first
    assert first["detail"].startswith("3 workers")


def test_a_job_with_nothing_waiting_says_so_and_starts_nothing(
    cfg, silence, tmp_path, monkeypatch, bound
):
    folder = fill(tmp_path / "settled", silence, names=("03A - 120 - x", "04B - 99 - y"))
    machine(monkeypatch)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert pool_check(done)["detail"] == (
        "one worker, this process: no file was waiting to be measured"
    )
    assert measured_by(bound) == {}


def test_a_job_whose_record_is_gone_says_it_does_not_know(cfg, silence, tmp_path, monkeypatch):
    folder = fill(tmp_path / "lost", silence, names=("a",))
    machine(monkeypatch)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    record = artifacts._job_dir(artifacts.ARTIFACTS_DIRNAME, cfg, job_of(done)) / "pool.json"
    assert record.is_file()
    record.unlink()
    code, again = drive(resume_argv(job_of(done)))
    assert code == int(ExitCode.OK), again
    assert pool_check(again)["detail"].startswith("no pool was recorded for this job")


def test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job(
    cfg, silence, tmp_path, monkeypatch
):
    """Two workers measured all of it; the resume that only settles a row must not say one."""
    names = ("a", "slow b", "slow c")
    folder = fill(tmp_path / "kept", silence, names=names)
    machine(monkeypatch)
    real = artifacts.produced
    held: list[str] = []

    def produced(cfg_, job, item, report):
        staged = real(cfg_, job, item, report)
        if len(held) < 2:
            held.append(item.item_id)
            if len(held) == 2:
                os.kill(os.getpid(), signal.SIGINT)
        return staged

    monkeypatch.setattr(artifacts, "produced", produced)
    code, stopped = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.INTERRUPTED), stopped
    job_id = job_of(stopped)
    first = artifacts.pool_record(cfg, job_id)
    assert first["workers"] == 3

    # Finish the two files left by hand, as a second run would, so the resume
    # finds every name carrying its head and has nothing to measure.
    monkeypatch.setattr(artifacts, "produced", real)
    for path in sorted(folder.iterdir()):
        if not analysis_cli.carries_head(path, cfg):
            path.rename(path.with_name(f"03A - 120 - {path.name}"))
    code, resumed = drive(list(stopped["cause"]["detail"]["resume"]))

    assert artifacts.pool_record(cfg, job_id) == first, "a drive that measured nothing overwrote it"
    if code == int(ExitCode.OK):
        assert pool_check(resumed)["detail"].startswith("3 workers")


def test_a_pool_record_that_cannot_be_written_is_a_missing_line_and_never_a_failed_job(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "unwritable", silence, names=("a", "b"))
    machine(monkeypatch)

    def refuses(cfg_, job_id, record):
        raise OSError("the state directory is read only")

    monkeypatch.setattr(artifacts, "record_pool", refuses)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert set(states(job_of(done)).values()) == {"done"}
    assert pool_check(done)["detail"].startswith("no pool was recorded for this job")


def test_a_job_another_driver_holds_records_no_pool_and_adds_none_to_the_refusal(
    cfg, silence, tmp_path, monkeypatch, bound
):
    """This call ran nothing, so it has no pool to describe."""
    folder = fill(tmp_path / "held", silence, names=("a", "b"))
    machine(monkeypatch)
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job_id = job_of(queued)
    with jobs.driver_lock(job_id):
        code, refused = drive(resume_argv(job_id))
    assert code != int(ExitCode.OK)
    assert "pool" not in refused["cause"]["detail"]
    assert not any(step.startswith("the pool:") for step in refused["cause"]["remediation"]["steps"])
    assert artifacts.pool_record(cfg, job_id) is None
    assert measured_by(bound) == {}
    assert set(states(job_id).values()) == {"pending"}


def test_the_restamp_shares_the_resume_and_opens_no_run_ahead(cfg, silence, tmp_path, monkeypatch):
    """Only ``analyze run`` measures ahead; the restamp's answer carries no pool line."""
    assert analysis_cli.RUN_HANDLER_KEY == "analyze.run"
    folder = fill(tmp_path / "restamped", silence, names=("03A - 120 - x",))
    machine(monkeypatch)
    opened: list[str] = []
    real = analysis_cli._heads_ahead

    def watching(store, job):
        opened.append(job.handler_key)
        return real(store, job)

    monkeypatch.setattr(analysis_cli, "_heads_ahead", watching)
    energy.save_calibration(
        cfg,
        energy.calibrate(
            [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
        ),
    )
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: None)
    code, restamped = drive(["analyze", "restamp", str(folder)])
    assert opened == [], restamped
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert opened == ["analyze.run"]


def test_a_linked_or_malformed_pool_record_is_no_record(cfg, tmp_path):
    """An absent line on the answer, never one read through a link or out of a list."""
    directory = artifacts._job_dir(artifacts.ARTIFACTS_DIRNAME, cfg, "job-z")
    assert artifacts.pool_record(cfg, "job-z") is None
    written = artifacts.record_pool(cfg, "job-z", {"workers": 3, "detail": "three"})
    assert written == directory / artifacts.POOL_FILENAME
    assert artifacts.pool_record(cfg, "job-z") == {"workers": 3, "detail": "three"}
    assert [entry.name for entry in directory.iterdir()] == ["pool.json"], "a staging file was left"
    assert artifacts.committed(cfg, "job-z") == (), "the pool record was read as an item report"

    written.write_text("[1, 2, 3]")
    assert artifacts.pool_record(cfg, "job-z") is None
    written.write_text("{not json")
    assert artifacts.pool_record(cfg, "job-z") is None
    elsewhere = tmp_path / "elsewhere.json"
    elsewhere.write_text('{"workers": 9, "detail": "another job entirely"}')
    written.unlink()
    written.symlink_to(elsewhere)
    assert artifacts.pool_record(cfg, "job-z") is None
    assert analysis_cli._pool_check(None)["detail"].startswith("no pool was recorded")
    assert analysis_cli._pool_check({"workers": 2})["detail"].startswith("no pool was recorded")


def test_a_closure_bound_by_a_test_is_never_sent_to_a_worker(cfg, silence, tmp_path, monkeypatch):
    """The other analysis suites bind closures; their runs stay in this process and say so."""
    folder = fill(tmp_path / "closure", silence, names=("a", "b"))
    machine(monkeypatch)
    monkeypatch.setattr(ahead, "_WORKER_BINDING", None)
    monkeypatch.setattr(light, "_DETECT", lambda path: fake_head(path))
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    assert pool_check(done)["detail"] == (
        "one worker, this process: the bound detector cannot be sent to a worker"
    )


# ---------------------------------------------------------------------------
# The other exit: a run that failed, and a run that was stopped
# ---------------------------------------------------------------------------


def test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run(
    cfg, silence, tmp_path, monkeypatch
):
    names = ("a", "raises b", "c")
    serial_folder = fill(tmp_path / "serial", silence, names=names)
    pooled_folder = fill(tmp_path / "pooled", silence, names=names)

    machine(monkeypatch, swap=12 * GIB)
    serial_code, serial = drive(["analyze", "run", str(serial_folder)])
    machine(monkeypatch)
    pooled_code, pooled = drive(["analyze", "run", str(pooled_folder)])

    assert pooled_code == serial_code != int(ExitCode.OK)
    assert states(job_of(pooled)) == states(job_of(serial)) == {
        "a.flac": "done",
        "c.flac": "done",
        "raises b.flac": "failed",
    }
    assert what_is_on_disk(pooled_folder) == what_is_on_disk(serial_folder)
    with jobs.open_store() as store:
        stored = jobs.get(store, job_of(pooled)).cause
    cause = pooled["cause"]
    # The stored cause is carried through, never rebuilt: its trail and its own
    # steps are a prefix of what the person is shown.
    assert tuple(cause["origin"])[: len(stored.origin)] == stored.origin
    steps = cause["remediation"]["steps"]
    assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps)
    assert steps[-1].startswith("the pool: 3 workers measured key, tempo and energy ahead")
    assert "2 of 3 waiting file(s) were read from them and 1 measured here" in steps[-1]
    assert cause["detail"]["pool"]["workers"] == 3
    assert cause["detail"]["pool"]["remeasured"] == {"raised-in-a-worker": 1}
    assert serial["cause"]["remediation"]["steps"][-1].startswith(
        "the pool: one worker, this process: 12.0 GB of swap is in use"
    )


def test_an_interrupt_during_a_run_ahead_ends_the_workers_and_the_resume_finishes(
    cfg, silence, tmp_path, monkeypatch
):
    """The driver owns the stop: the item in hand is released, no worker is left behind."""
    names = ("a", "slow b", "slow c", "slow d")
    folder = fill(tmp_path / "stopped", silence, names=names)
    serial_folder = fill(tmp_path / "serial", silence, names=names)
    machine(monkeypatch)
    real = artifacts.produced
    hits: list[str] = []

    def produced(cfg_, job, item, report):
        staged = real(cfg_, job, item, report)
        if not hits:
            hits.append(item.item_id)
            os.kill(os.getpid(), signal.SIGINT)
        return staged

    monkeypatch.setattr(artifacts, "produced", produced)
    code, stopped = drive(["analyze", "run", str(folder)])

    assert code == int(ExitCode.INTERRUPTED), stopped
    assert hits == ["a.flac"]
    assert multiprocessing.active_children() == [], "a worker outlived the interrupt"
    assert set(states(job_of(stopped)).values()) == {"pending"}
    assert stopped["cause"]["detail"]["pool"]["workers"] == 4

    code, resumed = drive(list(stopped["cause"]["detail"]["resume"]))
    assert code == int(ExitCode.OK), resumed
    assert set(states(job_of(stopped)).values()) == {"done"}

    monkeypatch.setattr(artifacts, "produced", real)
    machine(monkeypatch, swap=12 * GIB)
    code, serial = drive(["analyze", "run", str(serial_folder)])
    assert code == int(ExitCode.OK), serial
    assert what_is_on_disk(folder) == what_is_on_disk(serial_folder)


def test_a_worker_that_dies_costs_the_run_nothing_but_its_pool(
    cfg, silence, tmp_path, monkeypatch, bound
):
    names = ("a", "dies b", "c", "d")
    folder = fill(tmp_path / "died", silence, names=names)
    serial_folder = fill(tmp_path / "serial", silence, names=names)
    machine(monkeypatch)
    code, done = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), done
    check = pool_check(done)
    assert check["status"] == "info"
    assert "the pool was stopped early" in check["detail"]
    assert set(states(job_of(done)).values()) == {"done"}
    assert os.getpid() in measured_by(bound)["dies b.flac"], "the driver never measured it"
    assert multiprocessing.active_children() == []

    machine(monkeypatch, swap=12 * GIB)
    code, serial = drive(["analyze", "run", str(serial_folder)])
    assert code == int(ExitCode.OK), serial
    assert what_is_on_disk(folder) == what_is_on_disk(serial_folder)


# ---------------------------------------------------------------------------
# A head measured ahead that the driver must not use
# ---------------------------------------------------------------------------


def _session(tmp_path, silence, monkeypatch, names, settings=None) -> tuple[ahead.Session, list[str]]:
    folder = fill(tmp_path / "direct", silence, names=names)
    machine(monkeypatch)
    paths = [str(folder / f"{name}.flac") for name in names]
    return ahead.open_session("job-under-test", paths, settings), paths


def _wait_for_mark(marks: Path, name: str) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if any(mark.name.startswith(f"{name}@") for mark in marks.iterdir()):
            return
        time.sleep(0.05)
    raise AssertionError(f"no process ever measured {name}")


def test_a_file_replaced_after_its_head_was_measured_is_measured_again(
    silence, tmp_path, monkeypatch, bound
):
    """Same name, different file: the worker's head is for a file that is no longer there."""
    session, (first, second) = _session(tmp_path, silence, monkeypatch, ("a", "b"))
    assert ahead.head("job-under-test", first, None)["camelot"]
    _wait_for_mark(bound, "b.flac")
    replacement = Path(second).with_suffix(".new")
    replacement.write_bytes(Path(second).read_bytes() + b"\0" * 64)
    os.replace(replacement, second)

    found = ahead.head("job-under-test", second, None)

    assert found["camelot"] == fake_head(Path("b.flac"))["camelot"]
    assert session.remeasured == {"file-changed": 1}
    assert (session.ahead, session.here) == (1, 1)
    assert os.getpid() in measured_by(bound)["b.flac"]


def test_a_file_rewritten_in_place_after_its_head_was_measured_is_measured_again(
    silence, tmp_path, monkeypatch, bound
):
    """Same inode, new content: the identity is not the inode alone."""
    session, (first, second) = _session(tmp_path, silence, monkeypatch, ("a", "b"))
    ahead.head("job-under-test", first, None)
    _wait_for_mark(bound, "b.flac")
    before = os.stat(second)
    with open(second, "r+b") as handle:
        handle.seek(0, os.SEEK_END)
        handle.write(b"\0" * 64)
    assert os.stat(second).st_ino == before.st_ino

    ahead.head("job-under-test", second, None)

    assert session.remeasured == {"file-changed": 1}


def test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone(
    silence, tmp_path, monkeypatch, bound
):
    """Same inode, same size: only the modification time says it was written."""
    session, (first, second) = _session(tmp_path, silence, monkeypatch, ("a", "b"))
    ahead.head("job-under-test", first, None)
    _wait_for_mark(bound, "b.flac")
    before = os.stat(second)
    os.utime(second, ns=(before.st_atime_ns, before.st_mtime_ns + 5_000_000_000))
    after = os.stat(second)
    assert (after.st_ino, after.st_size) == (before.st_ino, before.st_size)

    ahead.head("job-under-test", second, None)

    assert session.remeasured == {"file-changed": 1}


def test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone(
    silence, tmp_path, monkeypatch, bound
):
    """Same inode, same modification time: only the size says it was written."""
    session, (first, second) = _session(tmp_path, silence, monkeypatch, ("a", "b"))
    ahead.head("job-under-test", first, None)
    _wait_for_mark(bound, "b.flac")
    before = os.stat(second)
    with open(second, "r+b") as handle:
        handle.seek(0, os.SEEK_END)
        handle.write(b"\0" * 64)
    os.utime(second, ns=(before.st_atime_ns, before.st_mtime_ns))
    after = os.stat(second)
    assert (after.st_ino, after.st_mtime_ns) == (before.st_ino, before.st_mtime_ns)
    assert after.st_size != before.st_size

    ahead.head("job-under-test", second, None)

    assert session.remeasured == {"file-changed": 1}


def rewrites_as_it_reads(path: Path) -> dict | None:
    """A detector under which the file is written WHILE it is being read."""
    with open(path, "r+b") as handle:
        handle.seek(0, os.SEEK_END)
        handle.write(b"\0" * 64)
    return fake_head(path)


def test_the_identity_a_worker_returns_is_the_files_before_the_read(silence, tmp_path, monkeypatch):
    """A file written during its own read must not carry the written file's identity."""
    target = tmp_path / "moving.flac"
    shutil.copy2(silence, target)
    before = ahead.identity_of(str(target))
    monkeypatch.setattr(light, "_DETECT", rewrites_as_it_reads)

    measured, found = ahead.measure(str(target))

    assert found["camelot"]
    assert measured == before
    assert measured != ahead.identity_of(str(target)), "the fixture did not change the file"
    assert ahead.identity_of(str(tmp_path / "not there.flac")) is None


def test_settings_that_changed_mid_run_stop_the_pool_and_the_rest_is_measured_here(
    silence, tmp_path, monkeypatch, bound
):
    """The serial run reads its calibration per item, so a new one reaches the next item."""
    was = ahead.Settings(calibration=None, tempo_window=(80, 160), drift_cut=1.0)
    now = ahead.Settings(calibration={"n_tracks": 12}, tempo_window=(80, 160), drift_cut=1.0)
    session, (first, second, third) = _session(
        tmp_path, silence, monkeypatch, ("a", "b", "c"), settings=was
    )
    ahead.head("job-under-test", first, was)
    assert session.ahead == 1 and session.stream is not None

    ahead.head("job-under-test", second, now)
    ahead.head("job-under-test", third, now)

    assert session.stream is None and session.stopped == ahead.STOPPED_SETTINGS
    assert (session.ahead, session.here) == (1, 2)
    assert os.getpid() in measured_by(bound)["b.flac"]
    assert os.getpid() in measured_by(bound)["c.flac"]
    assert multiprocessing.active_children() == []
    assert "the pool was stopped early" in ahead.report(session)["detail"]


@pytest.mark.parametrize(
    "changed",
    [
        ahead.Settings(calibration=None, tempo_window=(90, 180), drift_cut=1.0),
        ahead.Settings(calibration=None, tempo_window=(80, 160), drift_cut=2.5),
    ],
    ids=["tempo-window", "drift-cut"],
)
def test_each_setting_a_head_is_measured_under_is_compared(
    silence, tmp_path, monkeypatch, changed
):
    was = ahead.Settings(calibration=None, tempo_window=(80, 160), drift_cut=1.0)
    session, (first,) = _session(tmp_path, silence, monkeypatch, ("a", "b"), settings=was)[0], (
        str(tmp_path / "direct" / "a.flac"),
    )
    ahead.head("job-under-test", first, changed)
    assert session.stopped == ahead.STOPPED_SETTINGS


def test_a_path_the_session_never_planned_and_a_job_with_no_session_are_measured_here(
    silence, tmp_path, monkeypatch, bound
):
    session, (first,) = _session(tmp_path, silence, monkeypatch, ("a", "b"))[0], (
        str(tmp_path / "direct" / "a.flac"),
    )
    stranger = tmp_path / "direct" / "late arrival.flac"
    shutil.copy2(silence, stranger)
    assert ahead.head("job-under-test", str(stranger), None)["camelot"]
    assert session.here == 1
    assert ahead.head("some-other-job", first, None)["camelot"]
    assert os.getpid() in measured_by(bound)["a.flac"]


def test_the_settings_a_worker_is_started_with_are_the_ones_the_item_binds(cfg):
    """One calibration read, two uses: what the detector is bound with and what a head is held to."""
    calibration = energy.calibrate(
        [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
    )
    energy.save_calibration(cfg, calibration)
    assert analysis_cli._fake_detect_bound() is True
    assert analysis_cli._settings(cfg) is None and analysis_cli._bind_defaults(cfg) is None
    light.bind_detect(None)
    settings = analysis_cli._bind_defaults(cfg)
    assert settings == analysis_cli._settings(cfg)
    assert settings.calibration == calibration.to_json()
    assert settings.tempo_window == (cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling)
    assert settings.drift_cut == cfg.analysis.drift_cut
    # And what a worker rebuilds from them is the calibration the driver read.
    assert energy.Calibration.from_json(settings.calibration) == energy.Calibration.from_json(
        calibration.to_json()
    )
    ahead.bind_shipped(settings.calibration, settings.tempo_window, settings.drift_cut)
    rebuilt = light._DETECT
    assert rebuilt.func is detect.analyse_file
    assert rebuilt.keywords == analysis_cli._BOUND_DETECT.keywords | {
        "calibration": energy.Calibration.from_json(settings.calibration)
    }


def test_an_unreadable_calibration_is_each_items_refusal_and_opens_no_pool(
    cfg, silence, tmp_path, monkeypatch
):
    folder = fill(tmp_path / "corrupt", silence, names=("a", "b"))
    machine(monkeypatch)
    monkeypatch.setattr(ahead, "_WORKER_BINDING", None)
    monkeypatch.setattr(light, "_DETECT", None)
    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    energy.calibration_path(cfg).parent.mkdir(parents=True, exist_ok=True)
    energy.calibration_path(cfg).write_text("{not json")

    code, refused = drive(resume_argv(job_of(queued)))

    assert code != int(ExitCode.OK)
    assert set(states(job_of(queued)).values()) == {"failed"}
    assert refused["cause"]["detail"]["pool"]["detail"] == (
        "one worker, this process: the energy calibration could not be read"
    )
    assert multiprocessing.active_children() == []


# ---------------------------------------------------------------------------
# What a light worker costs, and the pool planned from it
# ---------------------------------------------------------------------------


def test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length():
    assert light.LIGHT_BASE_BYTES == 384 * MIB
    assert light.LIGHT_BYTES_PER_SECOND == 3276800, "three and an eighth megabytes a second"
    assert light.worker_bytes(0) == 384 * MIB
    assert light.worker_bytes(600) == 384 * MIB + 1875 * MIB
    # Above what was measured on Linux at each end, a 45 second track and an
    # 11 minute one.
    assert light.worker_bytes(45) > 345 * MIB
    assert light.worker_bytes(660) > 1175 * MIB
    with pytest.raises(ValueError):
        light.worker_bytes(-1)
    with pytest.raises(ValueError):
        light.worker_bytes(float("nan"))


#: One light worker's peak resident memory, a fresh process per track, over six
#: library tracks on Phillip's Mac at sitting 94 (A121, 2026-11-12): arm64,
#: Python 3.12.5, librosa 1.0.0, 44.1 kHz stereo FLAC. Seconds, then megabytes.
MAC_PEAKS = ((236, 987), (376, 1281), (576, 1805), (668, 2105), (690, 2162), (729, 2346))


def _line_through(points) -> list[tuple[float, float]]:
    """Slope and intercept of the line through the ends, and of least squares."""
    (s0, p0), (s1, p1) = points[0], points[-1]
    ends = (p1 - p0) / (s1 - s0)
    n = len(points)
    mean_s = sum(s for s, _ in points) / n
    mean_p = sum(p for _, p in points) / n
    fit = sum((s - mean_s) * (p - mean_p) for s, p in points) / sum(
        (s - mean_s) ** 2 for s, _ in points
    )
    return [(ends, p0 - ends * s0), (fit, mean_p - fit * mean_s)]


def _todays_cost(seconds: float, rate: int, channels: int) -> int:
    """The cost U241 declared, from its literal figures: 320 MB plus 1.5 MB a second."""
    analysis = int(seconds * 1572864)
    decode = int(seconds * rate * 4 * (channels + 3))
    return 320 * MIB + max(analysis, decode)


@pytest.mark.parametrize(("seconds", "peak"), MAC_PEAKS)
def test_each_measured_mac_peak_is_under_what_its_length_declares(seconds, peak):
    """U275: every one of the six was over the declared figure before."""
    declared = light.worker_bytes(float(seconds), rate=44100, channels=2)
    assert declared >= peak * MIB
    # With room, not by a hair: the Linux figures' margin was a ninth and up.
    assert declared >= peak * MIB * 10 // 9


def test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line():
    """A ninth over the steeper measured slope, an eighth over the higher intercept.

    Linux measured 1.35 megabytes a second and declared 1.5, a ninth above;
    it measured an intercept of 284 and declared 320, an eighth above.
    """
    lines = _line_through(MAC_PEAKS)
    slope = max(s for s, _ in lines)
    intercept = max(i for _, i in lines)
    assert slope == pytest.approx(2.757, abs=0.001)
    assert intercept == pytest.approx(336.4, abs=0.1)
    assert light.LIGHT_BYTES_PER_SECOND >= slope * MIB * 10 / 9
    assert light.LIGHT_BASE_BYTES >= intercept * MIB * 9 / 8


@pytest.mark.parametrize("seconds", [0.0, 0.25, 1.0, 45.0, 236.0, 660.0, 3600.0, 86400.0])
@pytest.mark.parametrize("rate", [1, 8000, 22050, 44100, 48000, 96000, 192000, 384000])
@pytest.mark.parametrize("channels", [1, 2, 6])
def test_no_shape_of_file_costs_less_than_it_did_before_u275(seconds, rate, channels):
    """The pool never plans wider than it did: no cost falls, at any length or rate."""
    assert light.worker_bytes(seconds, rate=rate, channels=channels) >= _todays_cost(
        seconds, rate, channels
    )


def test_a_file_whose_length_is_unknown_costs_no_less_than_before(tmp_path):
    unreadable = tmp_path / "odd.flac"
    unreadable.write_bytes(b"\0" * 400_000)
    assert tags.audio_seconds(unreadable) is None
    assert light.cost_of(unreadable) >= _todays_cost(100.0, 1, 1)


def test_a_file_whose_length_is_unknown_is_still_planned_narrower(tmp_path, monkeypatch):
    """Not knowing the length bounds it by the size, which is the longer reading."""
    known = tmp_path / "known.flac"
    unknown = tmp_path / "unknown.flac"
    for path in (known, unknown):
        path.write_bytes(b"\0" * 8_000_000)
    # Eight megabytes of uncompressed CD audio run 45 seconds; any real
    # encoding of that size runs longer, and the unknown path reads 2000.
    seconds = 8_000_000 / (44100 * 2 * 2)
    monkeypatch.setattr(
        tags,
        "audio_shape",
        lambda path: (seconds, 44100, 2) if Path(path).name == "known.flac" else (None, None, None),
    )
    assert light.cost_of(unknown) > light.cost_of(known)
    machine(monkeypatch, core_count=12, available=24 * GIB)
    narrow = light.plan([unknown] * 6)
    wide = light.plan([known] * 6)
    assert narrow.workers < wide.workers


@pytest.mark.parametrize("available_gib", [4, 6, 8, 12, 18, 24, 32, 64])
def test_the_light_plan_is_never_wider_than_before_u275(monkeypatch, available_gib):
    names = {f"t{i}.flac": (float(s), 44100, 2) for i, (s, _) in enumerate(MAC_PEAKS)}
    shapes(monkeypatch, names)
    machine(monkeypatch, core_count=64, available=available_gib * GIB)
    planned = light.plan(list(names))
    before = pool.plan_pool(
        worker_bytes=_todays_cost(729.0, 44100, 2),
        items=len(names),
        ceiling=cores.worker_ceiling(reserved=light.LIGHT_RESERVED_CORES),
    )
    assert planned.workers <= before.workers


@pytest.mark.parametrize("available_gib", [4, 6, 8, 12, 18, 24, 32, 64])
def test_six_mac_tracks_plan_no_more_workers_than_memory_holds(monkeypatch, available_gib):
    """The card's scenario: the planner over the six measured lengths on the Mac."""
    names = {f"t{i}.flac": (float(s), 44100, 2) for i, (s, _) in enumerate(MAC_PEAKS)}
    shapes(monkeypatch, names)
    machine(monkeypatch, core_count=12, available=available_gib * GIB)
    planned = light.plan(list(names))
    assert planned.worker_bytes == light.worker_bytes(729.0) >= 2346 * MIB
    assert planned.workers <= max(1, available_gib * GIB // planned.worker_bytes)
    if planned.workers > 1:
        # Every worker at the largest peak the Mac measured still fits.
        assert planned.workers * 2346 * MIB <= available_gib * GIB


def test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker(monkeypatch):
    names = {f"t{i}.flac": (float(s), 44100, 2) for i, (s, _) in enumerate(MAC_PEAKS)}
    shapes(monkeypatch, names)
    machine(monkeypatch, core_count=12, available=8 * GIB)
    planned = light.plan(list(names))
    assert planned.workers <= 8 * GIB // light.worker_bytes(729.0) == 3
    assert planned.workers == 1, "the reserve and the headroom come off first"


def shapes(monkeypatch, known: dict[str, tuple]) -> None:
    """Stand in for the headers: each name's seconds, sample rate and channels."""
    monkeypatch.setattr(tags, "audio_shape", lambda path: known[Path(path).name])


def test_the_cost_is_set_by_the_costliest_track_in_the_batch(monkeypatch):
    shapes(
        monkeypatch,
        {"a.flac": (200.0, 44100, 2), "b.flac": (610.0, 44100, 2), "c.flac": (45.0, 44100, 2)},
    )
    machine(monkeypatch, core_count=8)
    plan = light.plan(["a.flac", "b.flac", "c.flac"])
    assert plan.worker_bytes == light.worker_bytes(610.0) == light.costliest(["b.flac"])
    assert plan.ceiling == 6 and plan.workers == 3


def test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length():
    """The decode reads the file at its own rate; everything after it works at 22050."""
    cd_quality = light.worker_bytes(660.0, rate=44100, channels=2)
    assert cd_quality == 384 * MIB + 660 * 3276800, "CD audio is the analysis line, unchanged"
    # At 96 kilohertz the decode is still under the analysis line the Mac's
    # peaks set (U275); 1213 megabytes were measured on Linux, and the
    # declared figure is above that.
    middle = light.worker_bytes(660.0, rate=96000, channels=2)
    assert 660 * 96000 * 4 * (2 + 3) < 660 * light.LIGHT_BYTES_PER_SECOND
    assert middle == cd_quality > 1213 * MIB
    high = light.worker_bytes(660.0, rate=192000, channels=2)
    assert high == 384 * MIB + 660 * 192000 * 4 * (2 + 3)
    assert high > cd_quality, "at 192 kilohertz the decode is the larger line"
    # Above both peaks measured for exactly this file, 2054 and 2180 megabytes.
    assert high > 2180 * MIB
    assert light.worker_bytes(660.0, rate=44100, channels=1) == cd_quality
    assert (light.DECODE_BYTES_PER_CHANNEL, light.DECODE_EXTRA_CHANNELS) == (4, 3)
    with pytest.raises(ValueError):
        light.worker_bytes(10.0, rate=0)
    with pytest.raises(ValueError):
        light.worker_bytes(10.0, channels=0)


def test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest(monkeypatch):
    shapes(
        monkeypatch,
        {"long.flac": (700.0, 44100, 2), "hires.flac": (600.0, 192000, 2)},
    )
    machine(monkeypatch, core_count=8)
    plan = light.plan(["long.flac", "hires.flac"])
    assert plan.worker_bytes == light.worker_bytes(600.0, rate=192000, channels=2)
    assert plan.worker_bytes > light.worker_bytes(700.0)
    assert light.longest_seconds(["long.flac", "hires.flac"]) == 700.0


def test_a_header_that_gives_a_length_and_no_rate_is_costed_at_the_highest_plausible(monkeypatch):
    shapes(monkeypatch, {"vague.flac": (300.0, None, None)})
    assert (light.ASSUMED_RATE, light.ASSUMED_CHANNELS) == (192000, 2)
    assert light.cost_of("vague.flac") == light.worker_bytes(300.0, rate=192000, channels=2)


def test_a_length_the_header_will_not_give_is_bounded_by_the_files_size(tmp_path, monkeypatch):
    unreadable = tmp_path / "odd.flac"
    unreadable.write_bytes(b"\0" * 400_000)
    assert tags.audio_seconds(unreadable) is None
    assert light.seconds_of(unreadable) == 400_000 / light.SLOWEST_BYTES_PER_SECOND == 100.0
    assert light.seconds_of(tmp_path / "not there.flac") == 0.0
    assert light.longest_seconds([]) == 0.0
    # The size's bound is the whole of it: no assumed rate is laid on top.
    assert light.cost_of(unreadable) == light.worker_bytes(100.0, rate=1, channels=1)
    assert light.cost_of(unreadable) == 384 * MIB + 100 * 3276800
    assert light.costliest([]) == light.LIGHT_BASE_BYTES


def test_a_real_files_length_rate_and_channels_are_read_off_its_header(silence):
    seconds, rate, channels = tags.audio_shape(silence)
    assert seconds == pytest.approx(1.0, abs=0.05)
    assert (rate, channels) == (44100, 2)
    assert tags.audio_seconds(silence) == seconds
    assert light.seconds_of(silence) == seconds
    assert light.cost_of(silence) == light.worker_bytes(seconds, rate=44100, channels=2)


@pytest.mark.parametrize("value", [0, -2, True, 44100.0, "2", None])
def test_a_header_rate_or_channel_count_that_is_not_a_count_is_unknown(tmp_path, monkeypatch, value):
    import mutagen

    class _Info:
        length = 10.0

    class _Handle:
        info = _Info()

    _Handle.info.sample_rate = value
    _Handle.info.channels = value
    monkeypatch.setattr(mutagen, "File", lambda path: _Handle())
    assert tags.audio_shape(tmp_path / "x.flac") == (10.0, None, None)


@pytest.mark.parametrize("length", [0.0, -3.0, float("inf"), float("nan"), True, "12"])
def test_a_header_length_that_is_not_a_positive_number_is_unknown(tmp_path, monkeypatch, length):
    import mutagen

    class _Info:
        pass

    class _Handle:
        info = _Info()

    _Handle.info.length = length
    monkeypatch.setattr(mutagen, "File", lambda path: _Handle())
    assert tags.audio_seconds(tmp_path / "x.flac") is None


def test_the_light_pool_is_refused_by_the_gates_whatever_the_cores_say(monkeypatch):
    monkeypatch.setattr(tags, "audio_shape", lambda path: (300.0, 44100, 2))
    machine(monkeypatch, core_count=32, swap=2 * GIB)
    plan = light.plan(["a.flac", "b.flac", "c.flac"])
    assert plan.in_process and plan.bound is pool.Bound.MEMORY_PRESSURE
    assert plan.ceiling == 30


def test_the_batch_runner_plans_the_same_pool_the_job_does(monkeypatch):
    monkeypatch.setattr(tags, "audio_shape", lambda path: (120.0, 44100, 2))
    machine(monkeypatch, core_count=4, swap=2 * GIB)
    monkeypatch.setattr(light, "_DETECT", fake_head)
    results = light.run(["a.flac", "keyless b.flac"])
    assert [found["terminal"] for found in results] == [None, "skipped-no-key"]


# ---------------------------------------------------------------------------
# The report's forms
# ---------------------------------------------------------------------------


def test_a_run_nobody_planned_a_pool_for_reports_one_worker_and_why():
    assert ahead.report(None) == {
        "workers": 1,
        "planned": False,
        "status": "info",
        "detail": "one worker, this process: no pool was planned for this run",
    }
    noted = ahead.note_unopened("job-x", ahead.WHY_NO_EXTRA)
    assert ahead.report(noted)["detail"] == (
        "one worker, this process: the analysis extra is not installed in this process"
    )
    assert ahead.close_session("job-x") is noted
    assert ahead.close_session("job-x") is None
