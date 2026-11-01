"""U10: the job engine's properties, each named for the failure it prevents.

The engine is small; what makes it worth this many assertions is that every one
of them corresponds to something that actually went wrong once, either in the
source system or in the class of bug the plan records. So each test says which.

The subprocess tests are not slow versions of the in-process ones. A killed
process is the only way to produce the state the engine exists to recover from:
a claimed item whose driver is gone, a lock the kernel released, and a row that
still says running. An in-process fake can imitate the rows but not the kernel,
and the kernel is the half doing the work.
"""

from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
WORKER = Path(__file__).resolve().parent / "job_worker.py"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path):
    """A saved, loadable configuration. ``enqueue`` freezes exactly this."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def queue(tmp_path):
    """A queue in its own directory, so lock and log files are visible to a test."""
    root = tmp_path / "jobs"
    with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
        yield store, root


def _spawn_worker(*args: str) -> subprocess.Popen:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    return subprocess.Popen(
        [sys.executable, str(WORKER), *args],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _wait_for(path: Path, *, seconds: float = 20.0) -> None:
    """Block until a marker file appears, or fail naming what never arrived."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"{path.name} never appeared within {seconds}s")


def _attempts(ledger: Path) -> list[str]:
    return [line for line in ledger.read_text().splitlines() if line]


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: state discipline ported from the source manifest
# ═══════════════════════════════════════════════════════════════════════════


def test_a_queued_job_freezes_the_whole_configuration_not_a_subset(queue, cfg):
    """KTD9. A frozen subset un-freezes itself the next time somebody reads a key."""
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={"x": 1}, cfg=cfg)
    assert job.config_fingerprint == cfg.fingerprint()
    assert jobs.frozen_config(job).to_toml_dict() == cfg.to_toml_dict()
    assert job.library_id == cfg.library.volume_id


def test_a_job_records_the_library_it_targets(queue, cfg):
    """The queue is per install and a library is per config.

    Without the recorded identity, a queue drained after the user reconfigures
    runs against whatever volume is configured now, which is not the one the work
    was planned against.
    """
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    assert job.library_id == cfg.library.volume_id


def test_a_config_that_changed_while_queued_names_what_drifted(queue, cfg, tmp_path):
    """KTD9's second half, and the structural fix for a recorded resume bug.

    The bug: a base export re-resolved on resume, found something else, and could
    empty the output. The job here still runs against its frozen copy; what the
    engine adds is the ability to SAY which keys moved, so the user is not left
    wondering why their edit had no effect.
    """
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    assert jobs.drift(job, cfg) == ()

    moved = config.from_dict(
        {**cfg.to_toml_dict(), "paths": {"download_staging": str(tmp_path / "elsewhere")}}
    )
    drifted = jobs.drift(job, moved)
    assert drifted == ("paths.download_staging",)
    # The job still runs against the frozen copy, which is the whole point.
    assert jobs.frozen_config(job).paths.download_staging == cfg.paths.download_staging


def test_transitions_are_forward_only(queue, cfg):
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    with pytest.raises(CratekitError) as excinfo:
        jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    assert excinfo.value.cause.reason == "internal-error"


def test_an_unrecognized_state_on_disk_coerces_to_an_open_state_never_a_terminal_one(
    queue, cfg
):
    """The direction of the coercion is the load-bearing half.

    A malformed record degrading to ``queued`` costs at most a re-drive, and the
    item ledger makes that free. The same record degrading to ``succeeded`` is a
    false success, and nothing downstream can tell it from a real one.
    """
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    store.conn.execute(
        "UPDATE jobs SET state = ? WHERE job_id = ?", ("something-else", job.job_id)
    )
    store.conn.execute(
        "UPDATE job_items SET state = ? WHERE job_id = ?", ("nonsense", job.job_id)
    )
    assert jobs.get(store, job.job_id).state is jobs.JobState.QUEUED
    assert jobs.items(store, job.job_id)[0].state is jobs.ItemState.PENDING


def test_a_queue_written_at_another_schema_refuses_to_resume(tmp_path):
    """Ported discipline: the source versions one state file out of twenty-one."""
    path = tmp_path / "jobs" / jobs.QUEUE_FILENAME
    jobs.open_store(path).close()
    conn = sqlite3.connect(str(path))
    conn.execute("UPDATE queue_schema SET version = 99")
    conn.commit()
    conn.close()

    with pytest.raises(CratekitError) as excinfo:
        jobs.open_store(path)
    assert excinfo.value.cause.reason == "job-schema-mismatch"
    assert excinfo.value.cause.code is ExitCode.PRECONDITION


def test_an_unknown_job_refuses_with_a_code_from_the_vocabulary(queue):
    store, _ = queue
    with pytest.raises(CratekitError) as excinfo:
        jobs.get(store, "no-such-job")
    assert excinfo.value.cause.reason == "job-unknown"
    assert excinfo.value.cause.code is ExitCode.PRECONDITION
    assert excinfo.value.cause.remediation.steps


def test_states_of_answers_for_the_names_it_knows_and_omits_the_rest(queue, cfg):
    """An identifier with no row is ABSENT, never mapped to a state.

    "This queue has never heard of it" is not a state a job can be in, and the
    caller this exists for, ``acquire.cli.sweep_staging``, acts on exactly that
    difference: a staging directory naming an unknown job is another
    installation's and is left where it is.
    """
    store, _ = queue
    open_job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    done = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    jobs.transition(store, done.job_id, jobs.JobState.SUCCEEDED)

    answered = jobs.states_of(store, [open_job.job_id, done.job_id, "no-such-job"])

    assert answered == {
        open_job.job_id: jobs.JobState.QUEUED,
        done.job_id: jobs.JobState.SUCCEEDED,
    }
    assert jobs.states_of(store, []) == {}


def test_states_of_answers_past_the_parameter_limit_of_one_statement(queue, cfg):
    """More names than fit one ``IN`` clause, which is the case that reaches it.

    The caller is sweeping a staging tree that has never been swept, so the
    number of names it asks about is the number of jobs the installation ever
    ran. A single statement would raise ``sqlite3.OperationalError`` there, and
    the failure would land on the machine with the most to reclaim.
    """
    store, _ = queue
    made = [
        jobs.enqueue(
            store, handler_key="job.resume", payload={}, cfg=cfg, job_id=f"job-{n:05d}"
        ).job_id
        for n in range(jobs._ID_CHUNK + 7)
    ]

    answered = jobs.states_of(store, [*made, "no-such-job"])

    assert len(answered) == len(made)
    assert set(answered) == set(made)
    assert set(answered.values()) == {jobs.JobState.QUEUED}


def test_a_stored_cause_that_cannot_be_read_back_is_not_read_as_success(queue, cfg):
    """None means "no failure". An unparseable cause must never mean that."""
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    store.conn.execute(
        "UPDATE jobs SET cause = ? WHERE job_id = ?", ("{not json", job.job_id)
    )
    reloaded = jobs.get(store, job.job_id)
    assert reloaded.cause is not None
    assert reloaded.cause.reason == "no-evidence"


def test_everything_the_queue_writes_is_owner_only_under_any_umask(tmp_path, cfg):
    """Audited by WALKING the directory, never by naming the files in it.

    A test that lists the files it knows about is a test that misses the next one,
    and the next one here is a write-ahead log created by SQLite rather than by
    us. Directories are checked alongside files for the reason the config module
    already learned: a 0600 file inside a world-writable directory is not private,
    because unlink and rename are governed by the directory.
    """
    previous = os.umask(0o000)
    try:
        root = tmp_path / "queue-root"
        with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
            job = jobs.enqueue(
                store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"]
            )
            # Every writer this module has: the database, its sidecars, a driver
            # lock, and a job log. Exercised so the walk below has them all.
            with jobs.driver_lock(job.job_id, root=root):
                pass
            jobs.log_path(job.job_id, root=root).write_bytes(b"")
            env = dict(os.environ)
            env["PYTHONPATH"] = str(SRC_ROOT)
            pid = jobs.spawn(store, job, ["--version"], root=root, env=env)
            os.waitpid(pid, 0)
    finally:
        os.umask(previous)

    exposed = [
        str(path.relative_to(root))
        for path in sorted(root.rglob("*"))
        if path.stat().st_mode & 0o077
    ]
    assert not exposed, f"group or world accessible under the queue root: {exposed}"
    assert root.stat().st_mode & 0o077 == 0, "the queue directory itself is exposed"


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: blocked needs a reason (KTD25)
# ═══════════════════════════════════════════════════════════════════════════


def _throttled() -> Cause:
    return Cause(
        reason="unavailable-transient",
        message="the provider asked us to slow down",
        remediation=Remediation(remedy=Remedy.RETRY_LATER),
        scope=Scope.SOURCE,
        retryable=True,
    )


def _needs_acknowledgment() -> Cause:
    return Cause(
        reason="backup-acknowledgment-missing",
        message="this session has no recorded backup acknowledgment",
        remediation=Remediation(remedy=Remedy.ACKNOWLEDGE_BACKUP),
        scope=Scope.SESSION,
    )


def test_two_jobs_parked_under_one_state_still_carry_two_different_remediations(queue, cfg):
    """The plan names this case explicitly.

    A throttled provider and a missing acknowledgment are both ``blocked``. The
    source supervisor would give both the same status and put the difference in a
    log file; here the difference is a field.
    """
    store, _ = queue
    throttled = jobs.enqueue(store, handler_key="job.resume", payload={"a": 1}, cfg=cfg)
    unacknowledged = jobs.enqueue(store, handler_key="job.resume", payload={"b": 2}, cfg=cfg)

    jobs.block(store, throttled.job_id, _throttled())
    jobs.block(store, unacknowledged.job_id, _needs_acknowledgment())

    first = jobs.get(store, throttled.job_id)
    second = jobs.get(store, unacknowledged.job_id)
    assert first.state is second.state is jobs.JobState.BLOCKED
    assert first.cause.reason != second.cause.reason
    assert first.cause.remediation.remedy is Remedy.RETRY_LATER
    assert second.cause.remediation.remedy is Remedy.ACKNOWLEDGE_BACKUP


def test_parking_a_job_without_a_reason_is_refused(queue, cfg):
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    with pytest.raises(CratekitError):
        jobs.transition(store, job.job_id, jobs.JobState.BLOCKED)


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: durability (KTD8)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_artifact_is_flushed_and_renamed_before_the_row_flips_to_done(
    queue, cfg, tmp_path, monkeypatch
):
    """The ordering is the guarantee, so the ordering is what is asserted.

    Neither state writer in the source system flushes before replacing, so this
    is the one property in the whole engine that could not be ported and had to be
    added. A row that flips before the rename is durable leaves a job claiming an
    artifact that is not there, and "done" is exactly what a resume trusts.
    """
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["one"])

    events: list[str] = []
    real_fsync, real_replace = os.fsync, os.replace
    real_complete = jobs.complete_item

    monkeypatch.setattr(os, "fsync", lambda fd: (events.append("fsync"), real_fsync(fd))[1])
    monkeypatch.setattr(
        os, "replace", lambda a, b: (events.append("replace"), real_replace(a, b))[1]
    )
    monkeypatch.setattr(
        jobs,
        "complete_item",
        lambda *a, **k: (events.append("done"), real_complete(*a, **k))[1],
    )

    staged = tmp_path / "staged.txt"
    staged.write_text("payload")

    def handle(_job, _item):
        return jobs.Produced(staged=staged, final=tmp_path / "out" / "one.txt")

    jobs.drive(store, job.job_id, handle, root=root)

    assert events == ["fsync", "replace", "fsync", "done"], events
    assert (tmp_path / "out" / "one.txt").read_text() == "payload"
    assert not staged.exists()


def test_an_item_that_produces_nothing_still_completes(queue, cfg, tmp_path):
    """Not every unit of work makes a file, and the engine must not require one."""
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    result = jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    assert result.processed == 1
    assert result.job.state is jobs.JobState.SUCCEEDED


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: never an empty success
# ═══════════════════════════════════════════════════════════════════════════


def test_a_job_whose_every_item_fails_raises_rather_than_reporting_success(queue, cfg):
    """The recorded incident, as a test.

    Total lookup failure returned an empty list, the caller read that as "nothing
    new", and a playlist was permanently marked as fully downloaded holding zero
    tracks. Empty means verified empty only when the lookups succeeded.
    """
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )

    def always_fails(_job, _item):
        raise RuntimeError("the provider is unreachable")

    with pytest.raises(CratekitError) as excinfo:
        jobs.drive(store, job.job_id, always_fails, root=root)
    assert excinfo.value.cause.reason == "no-evidence"
    # The items failed as internal-error, which is not retryable. The envelope
    # used to claim unavailable-transient anyway, which is R-380.
    assert excinfo.value.cause.retryable is False
    # Recorded BEFORE the raise: a raise that left the row saying running would
    # be the unpersisted-decision half of the same incident.
    recorded = jobs.get(store, job.job_id)
    assert recorded.state is jobs.JobState.FAILED
    assert recorded.cause is not None
    assert recorded.cause.retryable is False


def test_attempting_nothing_is_a_no_op_and_not_a_failure(queue, cfg):
    """An up-to-date source must not look broken."""
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=[])
    result = jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    assert result.processed == 0
    assert result.job.state is jobs.JobState.SUCCEEDED
    jobs.evidence_or_raise(attempted=0, succeeded=0)


def test_a_partial_failure_fails_the_job_and_keeps_the_successes(queue, cfg):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["good", "bad"]
    )

    def sometimes(_job, item):
        if item.item_id == "bad":
            raise RuntimeError("this one is broken")
        return None

    result = jobs.drive(store, job.job_id, sometimes, root=root)
    assert (result.processed, result.failed) == (1, 1)
    assert result.job.state is jobs.JobState.FAILED
    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {"good": jobs.ItemState.DONE, "bad": jobs.ItemState.FAILED}


def _permanent_lookup() -> CratekitError:
    """The sitting's inner cause: the provider has no artist for this label."""
    return refuse(
        "sync-source-lookups-failed",
        "the provider has no artist named for this label",
        steps=("retry this source when the provider is reachable",),
        origin=("test",),
    )


def _transient_outage() -> CratekitError:
    return refuse(
        "unavailable-transient",
        "the provider asked us to slow down",
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("test",),
    )


def test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable(
    queue, cfg
):
    """R-380, the all failed half, which is also R-266's remaining engine half.

    The item rows already carry a non retryable cause. The job used to wrap them
    as unavailable-transient, retryable, resume-job, which is the instruction a
    person acts on.
    """
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )

    def always_permanent(_job, _item):
        raise _permanent_lookup()

    with pytest.raises(CratekitError) as excinfo:
        jobs.drive(store, job.job_id, always_permanent, root=root)
    envelope = excinfo.value.cause
    assert envelope.reason == "no-evidence"
    assert envelope.retryable is False
    assert envelope.remediation.remedy is not Remedy.RESUME_JOB
    assert envelope.inner is not None
    assert envelope.inner.reason == "sync-source-lookups-failed"
    recorded = jobs.get(store, job.job_id)
    assert recorded.cause is not None
    assert recorded.cause.reason == "sync-source-lookups-failed"
    assert recorded.cause.retryable is False
    assert recorded.cause.remediation.remedy is not Remedy.RESUME_JOB
    assert recorded.cause.inner is not None
    assert recorded.cause.inner.reason == "sync-source-lookups-failed"


def test_a_partial_failure_whose_failures_are_permanent_is_not_resumable(queue, cfg):
    """The sitting's mixed job: some items done, every failure permanent.

    A resume re-arms only the failed items, so the cost is crawling those again,
    not the successes. The lie is telling the person that resume can help.
    """
    store, root = queue
    job = jobs.enqueue(
        store,
        handler_key="job.resume",
        payload={},
        cfg=cfg,
        item_ids=["good", "bad"],
    )

    def sometimes(_job, item):
        if item.item_id == "bad":
            raise _permanent_lookup()
        return None

    result = jobs.drive(store, job.job_id, sometimes, root=root)
    assert (result.processed, result.failed) == (1, 1)
    assert result.job.state is jobs.JobState.FAILED
    cause = result.job.cause
    assert cause is not None
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is False
    assert cause.remediation.remedy is not Remedy.RESUME_JOB
    assert "finished 1 items and failed 1" in cause.message
    assert "permanent" in cause.message
    assert cause.inner is not None
    assert cause.inner.reason == "sync-source-lookups-failed"
    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {"good": jobs.ItemState.DONE, "bad": jobs.ItemState.FAILED}

    # R-390. ``retry`` used to re-arm the failed item anyway, and R-380 had only
    # stopped the job from SAYING resume. The verdict now holds on the one path
    # that could still perform one.
    with pytest.raises(CratekitError) as excinfo:
        jobs.retry(store, job.job_id)
    refusal = excinfo.value.cause
    assert refusal.reason == "job-not-retryable"
    assert refusal.code is ExitCode.PRECONDITION
    assert refusal.inner is not None
    assert refusal.inner.reason == "sync-source-lookups-failed"
    assert "permanent_reasons" not in refusal.detail
    untouched = jobs.get(store, job.job_id)
    assert untouched.state is jobs.JobState.FAILED
    assert untouched.cause is not None
    assert untouched.cause.reason == "sync-source-lookups-failed"
    after = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert after == {"good": jobs.ItemState.DONE, "bad": jobs.ItemState.FAILED}


def test_a_failed_job_with_no_recorded_cause_still_re_arms(queue, cfg):
    """R-390's edge: a missing verdict is not a permanent one.

    A build before R-380 recorded FAILED with no cause on some paths, and a
    person holding such a queue is owed the re-arm the verb always performed.
    The refusal reads the flag off the cause and a job with none falls through.
    """
    store, _root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )
    jobs.fail_item(
        store,
        job.job_id,
        "a",
        cause=Cause(
            reason="internal-error",
            message="this one broke",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("test",),
        ),
    )
    jobs.transition(store, job.job_id, jobs.JobState.FAILED)
    recorded = jobs.get(store, job.job_id)
    assert recorded.state is jobs.JobState.FAILED
    assert recorded.cause is None

    retried = jobs.retry(store, job.job_id)
    assert retried.state is jobs.JobState.QUEUED
    after = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert after["a"] is jobs.ItemState.PENDING


def test_resuming_a_job_of_permanent_failures_through_the_verb_refuses(
    cfg, default_queue
):
    """R-390 at the shell. The verb relies on the engine's refusal, nothing else.

    The refusal reaches the person in the foreground, before any child is
    spawned, with the item's own reason nested inside it, and the items are left
    exactly as the failure left them.
    """
    root = jobs.store_dir()
    job = jobs.enqueue(
        default_queue,
        handler_key="job.resume",
        payload={},
        cfg=cfg,
        item_ids=["good", "bad"],
        job_id="job-permanent",
    )

    def sometimes(_job, item):
        if item.item_id == "bad":
            raise _permanent_lookup()
        return None

    jobs.drive(default_queue, job.job_id, sometimes, root=root)

    code, envelope = _drive_cli(["job", "resume", "job-permanent"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "job-not-retryable"
    assert envelope["cause"]["inner"]["reason"] == "sync-source-lookups-failed"
    assert envelope["cause"]["remediation"]["remedy"] is None
    assert envelope["cause"]["remediation"]["steps"]
    states = {
        item.item_id: item.state for item in jobs.items(default_queue, job.job_id)
    }
    assert states == {"good": jobs.ItemState.DONE, "bad": jobs.ItemState.FAILED}
    assert jobs.get(default_queue, job.job_id).state is jobs.JobState.FAILED


def test_two_distinct_permanent_reasons_name_both_whichever_failed_last(queue, cfg):
    """R-391. The job cause used to take ``failed[-1].reason`` over a mixed job.

    A job that failed as both internal-error and sync-source-lookups-failed
    named whichever the driver claimed last, so the other was invisible outside
    the item rows. Driven in both item orders so the verdict is shown to depend
    on the set of reasons and not on the sequence.
    """
    store, root = queue

    def mixed_permanent(_job, item):
        if item.item_id == "lookup":
            raise _permanent_lookup()
        raise RuntimeError("this one is broken")

    causes = []
    for order in (["lookup", "broken"], ["broken", "lookup"]):
        job = jobs.enqueue(
            store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=order
        )
        with pytest.raises(CratekitError) as excinfo:
            jobs.drive(store, job.job_id, mixed_permanent, root=root)
        # The all failed envelope still nests the last item, whose own detail
        # is what a person acts on, and names every reason on its own detail
        # and in its message, so the foreground is not left with only the item
        # the driver claimed last.
        raised = excinfo.value.cause
        assert raised.reason == "no-evidence"
        assert raised.inner is not None
        assert raised.inner.reason in ("internal-error", "sync-source-lookups-failed")
        assert tuple(raised.detail["permanent_reasons"]) == (
            "internal-error",
            "sync-source-lookups-failed",
        )
        assert "internal-error" in raised.message
        assert "sync-source-lookups-failed" in raised.message
        recorded = jobs.get(store, job.job_id)
        assert recorded.cause is not None
        causes.append(recorded.cause)

    for cause in causes:
        assert cause.reason == "mixed-permanent-failures"
        assert cause.retryable is False
        assert cause.remediation.remedy is not Remedy.RESUME_JOB
        assert "internal-error" in cause.message
        assert "sync-source-lookups-failed" in cause.message
        assert "2 permanent" in cause.message
        # Built as the sorted tuple and read back off the row through JSON,
        # which holds a sequence and not a tuple, so the shape is compared as
        # a sequence and the ORDER is what is pinned.
        assert tuple(cause.detail["permanent_reasons"]) == (
            "internal-error",
            "sync-source-lookups-failed",
        )
    assert causes[0].reason == causes[1].reason
    assert causes[0].detail["permanent_reasons"] == causes[1].detail["permanent_reasons"]

    # The resume refusal names the same reasons at its own top level (R-390
    # over R-391), so a person is not sent into the nested cause to learn them.
    with pytest.raises(CratekitError) as excinfo:
        jobs.retry(store, job.job_id)
    refusal = excinfo.value.cause
    assert refusal.reason == "job-not-retryable"
    assert tuple(refusal.detail["permanent_reasons"]) == (
        "internal-error",
        "sync-source-lookups-failed",
    )


def test_one_shared_permanent_reason_is_still_the_jobs_reason(queue, cfg):
    """R-391 does not move R-380's case: three items, one reason, that reason."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )

    def always_permanent(_job, _item):
        raise _permanent_lookup()

    with pytest.raises(CratekitError):
        jobs.drive(store, job.job_id, always_permanent, root=root)
    cause = jobs.get(store, job.job_id).cause
    assert cause is not None
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is False
    assert "permanent_reasons" not in cause.detail
    assert "mixed" not in cause.message


def test_a_job_whose_failures_include_a_retryable_cause_stays_retryable(queue, cfg):
    """A resume can still help the items that failed transiently."""
    store, root = queue
    job = jobs.enqueue(
        store,
        handler_key="job.resume",
        payload={},
        cfg=cfg,
        item_ids=["good", "perm", "temp"],
    )

    def mixed(_job, item):
        if item.item_id == "perm":
            raise _permanent_lookup()
        if item.item_id == "temp":
            raise _transient_outage()
        return None

    result = jobs.drive(store, job.job_id, mixed, root=root)
    assert (result.processed, result.failed) == (1, 2)
    cause = result.job.cause
    assert cause is not None
    assert cause.retryable is True
    assert cause.reason == "unavailable-transient"
    assert cause.remediation.remedy is Remedy.RESUME_JOB
    assert "1 retryable" in cause.message
    assert "1 permanent" in cause.message


def test_an_all_failed_job_that_includes_a_retryable_cause_stays_retryable(queue, cfg):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["perm", "temp"]
    )

    def mixed(_job, item):
        if item.item_id == "perm":
            raise _permanent_lookup()
        raise _transient_outage()

    with pytest.raises(CratekitError) as excinfo:
        jobs.drive(store, job.job_id, mixed, root=root)
    assert excinfo.value.cause.reason == "no-evidence"
    assert excinfo.value.cause.retryable is True
    assert excinfo.value.cause.remediation.remedy is Remedy.RETRY_LATER


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: cancelled is not failed, and an interrupt aborts before a commit
# ═══════════════════════════════════════════════════════════════════════════


def test_cancelling_reports_cancelled_rather_than_failed(queue, cfg):
    """R22 names the distinction. The source registry cannot express it at all."""
    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    cancelled = jobs.cancel(store, job.job_id, stage="planning")
    assert cancelled.state is jobs.JobState.CANCELLED
    assert cancelled.state is not jobs.JobState.FAILED
    assert cancelled.cause.reason == "cancelled"
    assert cancelled.cause.code is ExitCode.INTERRUPTED
    assert cancelled.stage == "planning"


def test_an_interrupt_between_the_work_and_the_commit_leaves_no_artifact(
    queue, cfg, tmp_path
):
    """The abort point is BEFORE the commit, never inside it.

    The handler signals the process itself, which is as close to a real SIGINT as
    a test can get: the handler runs synchronously, records the flag, and the
    driver reaches its checkpoint with the item claimed and nothing written.
    """
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )
    staged = tmp_path / "staged-a.txt"
    final = tmp_path / "out" / "a.txt"

    def handle(_job, item):
        staged.write_text("half a session")
        os.kill(os.getpid(), signal.SIGINT)
        return jobs.Produced(staged=staged, final=final)

    result = jobs.drive(store, job.job_id, handle, root=root, stage="downloading")

    assert result.interrupted is True
    assert result.processed == 0
    assert not final.exists(), "the commit ran despite the interrupt"
    assert result.job.state is jobs.JobState.CANCELLED
    assert result.job.stage == "downloading"
    # Released, not failed: the item is redone whole on resume rather than
    # inheriting whatever half-state the interrupted attempt left behind.
    assert {item.state for item in jobs.items(store, job.job_id)} == {
        jobs.ItemState.PENDING
    }


def test_the_signal_handler_is_restored_afterwards(queue):
    """A driver that leaves its handler installed breaks whatever runs next."""
    before = signal.getsignal(signal.SIGINT)
    with jobs.interruptible():
        assert signal.getsignal(signal.SIGINT) is not before
    assert signal.getsignal(signal.SIGINT) is before


def test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot(queue, cfg):
    """Cancelled is terminal AND retryable; succeeded is terminal and finished.

    The cancelled half is also R-390's boundary: the refusal reads the cause's
    ``retryable`` flag, and ``cancel`` writes a retryable cause, so a job a
    person stopped with a signal still re-arms.
    """
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    jobs.cancel(store, job.job_id)
    cancelled = jobs.get(store, job.job_id)
    assert cancelled.cause is not None
    assert cancelled.cause.retryable is True
    assert jobs.retry(store, job.job_id).state is jobs.JobState.QUEUED

    jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    with pytest.raises(CratekitError):
        jobs.retry(store, job.job_id)


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: one driver per job, decided by holder liveness
# ═══════════════════════════════════════════════════════════════════════════


def test_a_second_driver_refuses_while_a_live_holder_has_the_lock(queue, cfg):
    """A slow run is never evicted, which is why there is no timeout anywhere."""
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    holder = _spawn_worker("hold", job.job_id, str(root))
    try:
        _wait_for(root / f"holding-{job.job_id}")
        with pytest.raises(jobs.DriverHeld) as excinfo:
            with jobs.driver_lock(job.job_id, root=root):
                pass
        assert excinfo.value.cause.reason == "job-driver-held"
        assert excinfo.value.cause.code is ExitCode.LIBRARY_BUSY
        assert str(holder.pid) in excinfo.value.cause.message
    finally:
        holder.kill()
        holder.wait(timeout=20)


def test_a_dead_holders_lock_is_reclaimed_without_any_timeout(queue, cfg):
    """The kernel releases an advisory lock when its holder dies.

    That IS the staleness rule. A timeout cannot tell a crashed driver from a slow
    one, and every timeout long enough to be safe for a slow run is too long to be
    useful after a crash.
    """
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    holder = _spawn_worker("hold", job.job_id, str(root))
    _wait_for(root / f"holding-{job.job_id}")
    holder.kill()
    holder.wait(timeout=20)

    # No sleep, no grace period: the lock is free the instant the holder is gone.
    with jobs.driver_lock(job.job_id, root=root) as path:
        assert json.loads(path.read_text())["pid"] == os.getpid()


def test_the_lock_file_survives_release(queue, cfg):
    """Unlinking on release is the classic way to lose the exclusion it provides."""
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    with jobs.driver_lock(job.job_id, root=root):
        pass
    assert jobs.lock_path(job.job_id, root=root).exists()


def test_a_running_row_with_no_live_driver_is_reconciled_back_to_queued(queue, cfg):
    """Disk truth is the lock, not the row.

    Believing the row would either refuse a resume forever or double-drive a job
    whose lock is genuinely held, and the source supervisor's answer to the same
    question is where its "no success without evidence" rule comes from.
    """
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING, stage="downloading")
    store.conn.execute(
        "UPDATE job_items SET state = ?, claimed_by = ? WHERE job_id = ?",
        (str(jobs.ItemState.CLAIMED), "a-dead-driver", job.job_id),
    )

    reconciled = jobs.reconcile(store, job.job_id, root=root)
    assert reconciled.state is jobs.JobState.QUEUED
    assert reconciled.stage == "downloading"
    assert jobs.items(store, job.job_id)[0].state is jobs.ItemState.PENDING


def test_reconcile_leaves_a_genuinely_running_job_alone(queue, cfg):
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    holder = _spawn_worker("hold", job.job_id, str(root))
    try:
        _wait_for(root / f"holding-{job.job_id}")
        assert jobs.reconcile(store, job.job_id, root=root).state is jobs.JobState.RUNNING
    finally:
        holder.kill()
        holder.wait(timeout=20)


# ═══════════════════════════════════════════════════════════════════════════
# Part 7: two processes writing job state
# ═══════════════════════════════════════════════════════════════════════════


def test_two_processes_claiming_the_same_job_never_claim_one_item_twice(
    queue, cfg, tmp_path
):
    """The claim is one immediate transaction, and this is what that buys.

    Under a deferred transaction both processes read the same lowest pending
    ordinal before either writes, and SQLite resolves it by failing one of them at
    COMMIT, which is after the work has already been decided.
    """
    store, root = queue
    item_ids = [f"item-{index:03d}" for index in range(60)]
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=item_ids
    )

    left = tmp_path / "left.log"
    right = tmp_path / "right.log"
    barrier = tmp_path / "go"
    left.write_text("")
    right.write_text("")
    workers = [
        _spawn_worker("claim", str(store.path), job.job_id, str(left), str(barrier)),
        _spawn_worker("claim", str(store.path), job.job_id, str(right), str(barrier)),
    ]
    time.sleep(0.5)  # both are past their imports and waiting on the barrier
    barrier.write_text("go")
    for worker in workers:
        out, err = worker.communicate(timeout=90)
        assert worker.returncode == 0, err or out

    claimed = _attempts(left) + _attempts(right)
    assert sorted(claimed) == sorted(item_ids), "an item was claimed twice or not at all"
    assert {item.state for item in jobs.items(store, job.job_id)} == {jobs.ItemState.DONE}
    assert jobs.progress(store, job.job_id)["settled"] == len(item_ids)
    # Both processes did real work, or the test proved nothing about concurrency.
    assert _attempts(left) and _attempts(right)


# ═══════════════════════════════════════════════════════════════════════════
# Part 8: the subprocess seam (KTD26)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_child_command_re_invokes_the_module_rather_than_a_console_script():
    """A console script is a generated wrapper whose path depends on the install.

    The source supervisor shells out to exactly those wrappers, which is one of
    the things this plan deletes.
    """
    command = jobs.child_command(["job", "resume", "abc"], executable="/usr/bin/python3")
    assert command == ["/usr/bin/python3", "-m", "cratekit.cli", "job", "resume", "abc"]


def test_a_spawned_job_runs_detached_and_its_output_lands_in_the_jobs_log(
    queue, cfg, tmp_path
):
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)

    pid = jobs.spawn(store, job, ["--version"], root=root, env=env)
    assert jobs.get(store, job.job_id).pid == pid

    log = jobs.log_path(job.job_id, root=root)
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and not log.read_text().strip():
        time.sleep(0.05)
    assert log.read_text().strip(), "the detached child produced no output"
    os.waitpid(pid, 0)


def test_the_engine_module_names_no_verb():
    """KTD23, asserted directly rather than only through the layering sweep.

    The engine re-invokes the product, so it is the module most tempted to spell a
    subcommand. It resolves one through the CLI layer instead, which is why the
    handler key exists at all.
    """
    from cratekit.cli import registry  # noqa: PLC0415 - a test may look upward

    source = (SRC_ROOT / "cratekit" / "core" / "jobs.py").read_text()
    for name in registry.VERB_NAMES:
        assert f'"{name}"' not in source, f"the engine spells the verb {name!r}"


# ═══════════════════════════════════════════════════════════════════════════
# Part 9: the handler-key seam, derived from the registry
# ═══════════════════════════════════════════════════════════════════════════


def test_every_landed_long_running_verb_actually_exposes_the_builder_it_declares():
    """Derived by walking the registry, so the next long-running verb is covered.

    The registry already refuses an entry that declares itself long-running with
    no argv builder. What it cannot check is that the named function EXISTS, and a
    declaration pointing at nothing fails only when somebody tries to resume, six
    units from now.
    """
    import importlib  # noqa: PLC0415

    from cratekit.cli import registry  # noqa: PLC0415

    missing: list[str] = []
    for entry in registry.entries():
        if not entry.long_running or not entry.landed:
            continue
        module = importlib.import_module(entry.module)
        if not callable(getattr(module, entry.argv_builder, None)):
            missing.append(f"{entry.name} -> {entry.module}.{entry.argv_builder}")
    assert not missing, f"declared argv builders that do not exist: {missing}"


# THE HANDLER-KEY IMPORT PROPERTY LIVES IN tests/test_cli_contract.py NOW, and a
# copy of it stood here until U42 removed this one. Both copies named
# ``acquire.download`` as their subject and asserted its module was not in
# ``sys.modules``, which held only because the module was unimplemented. When U42
# landed it, both failed on the same day on a lookup that had imported nothing,
# and the second copy was found by the full battery rather than by looking, which
# is METHOD's implied fifth pattern.
#
# Restating it here as well would have put a second weak measurement beside the
# real one: the property is about a CLEAN interpreter, which a test running late
# in this suite cannot be, and a mutation table proved the in-process form empty.
# What this file genuinely owes is the SUPERVISOR'S path, which the two tests
# below already drive: an unknown handler and a verb that has not landed both
# refuse before anything is imported.


def test_a_job_queued_for_a_handler_this_build_does_not_register_refuses(queue, cfg):
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415

    store, _ = queue
    job = jobs.enqueue(store, handler_key="not-a-handler", payload={}, cfg=cfg)
    with pytest.raises(CratekitError) as excinfo:
        jobs_cli.argv_for(job)
    assert excinfo.value.cause.reason == "internal-error"


def test_a_job_queued_for_a_verb_that_has_not_landed_refuses_rather_than_importing(
    queue, cfg, monkeypatch
):
    """The landed check in argv_for, held after the last planned queued verb.

    Until U25 this derived the subject from the registry. That population is
    now empty, so a synthetic planned entry keeps the refusal from rotting.
    """
    from dataclasses import replace

    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415
    from cratekit.cli import registry  # noqa: PLC0415

    store, _ = queue
    unlanded = [e for e in registry.entries() if not e.landed and e.argv_builder]
    assert not unlanded, (
        f"these queued verbs still carry planned_in: {[e.name for e in unlanded]}"
    )
    missing = "cratekit.vocals.missing_shell"
    fake = replace(
        registry.entry("analyze.vocals"),
        planned_in="U99",
        module=missing,
    )
    monkeypatch.setattr(
        registry,
        "ENTRIES",
        tuple(fake if e.name == fake.name else e for e in registry.ENTRIES),
    )
    monkeypatch.setattr(
        registry, "_BY_NAME", {**dict(registry._BY_NAME), fake.name: fake}
    )
    monkeypatch.setattr(
        registry,
        "_BY_HANDLER",
        {**dict(getattr(registry, "_BY_HANDLER", {})), fake.handler_key: fake},
    )
    job = jobs.enqueue(store, handler_key=fake.handler_key, payload={}, cfg=cfg)
    with pytest.raises(CratekitError) as excinfo:
        jobs_cli.argv_for(job)
    assert excinfo.value.cause.reason == "internal-error"
    assert missing not in sys.modules


def test_the_resume_builder_turns_a_frozen_job_back_into_a_command_line(queue, cfg):
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415

    store, _ = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg)
    assert jobs_cli.argv_for(job) == ["job", "resume", job.job_id]


# ═══════════════════════════════════════════════════════════════════════════
# Part 10: the four verbs
# ═══════════════════════════════════════════════════════════════════════════


def _drive_cli(argv: list[str]) -> tuple[int, dict]:
    import io  # noqa: PLC0415

    from cratekit import cli  # noqa: PLC0415

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


@pytest.fixture
def default_queue(cfg):
    """A queue at the DECLARED path, so the verbs find it the way a user would."""
    with jobs.open_store() as store:
        yield store


def test_listing_an_empty_queue_is_a_no_op_and_not_an_error(cfg, default_queue):
    code, envelope = _drive_cli(["job", "list"])
    assert code == int(ExitCode.OK)
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["jobs"] == []


def test_listing_reports_each_job_with_its_progress(cfg, default_queue):
    jobs.enqueue(
        default_queue,
        handler_key="job.resume",
        payload={},
        cfg=cfg,
        item_ids=["a", "b"],
        job_id="job-one",
    )
    code, envelope = _drive_cli(["job", "list"])
    assert code == int(ExitCode.OK)
    rows = envelope["data"]["progress"]["jobs"]
    assert [row["job_id"] for row in rows] == ["job-one"]
    assert rows[0]["progress"]["total"] == 2
    assert envelope["data"]["progress"]["counts"]["queued"] == 1


def test_a_state_filter_that_names_nothing_is_refused_rather_than_ignored(
    cfg, default_queue
):
    """A filter matching nothing looks exactly like an empty queue."""
    code, envelope = _drive_cli(["job", "list", "--state", "sideways"])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "job-unknown"


def test_showing_a_broken_job_succeeds_and_carries_the_jobs_cause_in_the_payload(
    cfg, default_queue
):
    """Reporting on a failure is not itself a failure.

    Mirroring the job's status onto the verb's status would leave a caller unable
    to tell "this job failed" from "I could not read this job", which is the
    KTD25 collapse one level up.
    """
    jobs.enqueue(
        default_queue, handler_key="job.resume", payload={}, cfg=cfg, job_id="job-two"
    )
    jobs.block(default_queue, "job-two", _throttled())

    code, envelope = _drive_cli(["job", "show", "job-two"])
    assert code == int(ExitCode.OK)
    assert envelope["cause"] is None
    assert envelope["data"]["state"] == "blocked"
    assert envelope["data"]["cause"]["reason"] == "unavailable-transient"


def test_showing_a_job_whose_config_moved_warns_and_names_the_keys(
    cfg, default_queue, tmp_path
):
    jobs.enqueue(
        default_queue, handler_key="job.resume", payload={}, cfg=cfg, job_id="job-three"
    )
    moved = config.from_dict(
        {**cfg.to_toml_dict(), "paths": {"download_staging": str(tmp_path / "elsewhere")}}
    )
    config.save(moved)
    config.reset_cache()

    code, envelope = _drive_cli(["job", "show", "job-three"])
    assert code == int(ExitCode.OK)
    assert envelope["warnings"], "a drifted configuration was not reported"
    assert "paths.download_staging" in envelope["warnings"][0]["message"]


def test_cancelling_through_the_verb_succeeds_and_reports_cancelled(cfg, default_queue):
    """A cancel that exited non-zero could not be told from a cancel that failed."""
    jobs.enqueue(
        default_queue, handler_key="job.resume", payload={}, cfg=cfg, job_id="job-four"
    )
    code, envelope = _drive_cli(["job", "cancel", "job-four"])
    assert code == int(ExitCode.OK)
    assert envelope["data"]["state"] == "cancelled"
    assert envelope["data"]["cause"]["reason"] == "cancelled"


def test_resuming_a_job_a_live_driver_already_holds_refuses_in_the_foreground(
    cfg, default_queue
):
    """The refusal has to reach the person, not a detached child's log file."""
    jobs.enqueue(
        default_queue, handler_key="job.resume", payload={}, cfg=cfg, job_id="job-five"
    )
    root = jobs.store_dir()
    holder = _spawn_worker("hold", "job-five", str(root))
    try:
        _wait_for(root / "holding-job-five")
        code, envelope = _drive_cli(["job", "resume", "job-five"])
        assert code == int(ExitCode.LIBRARY_BUSY)
        assert envelope["cause"]["reason"] == "job-driver-held"
    finally:
        holder.kill()
        holder.wait(timeout=20)


def test_every_job_verb_refuses_an_unknown_identifier_with_the_same_code(
    cfg, default_queue
):
    for argv in (["job", "show"], ["job", "cancel"], ["job", "resume"]):
        code, envelope = _drive_cli([*argv, "no-such-job"])
        assert code == int(ExitCode.PRECONDITION), argv
        assert envelope["cause"]["reason"] == "job-unknown", argv


# ═══════════════════════════════════════════════════════════════════════════
# Parking: the run stops, the item goes back, and nothing else is claimed
# ═══════════════════════════════════════════════════════════════════════════


def _blocked() -> Cause:
    return Cause(
        reason="provider-blocked",
        message="the provider refused this client",
        remediation=Remediation(steps=("check the account",)),
        scope=Scope.RUN,
        retryable=False,
    )


def test_a_parked_item_blocks_the_job_and_claims_nothing_further(queue, cfg):
    """A block is about the client, so the next claim is the second request
    into it. The engine stops at the first."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )
    seen: list[str] = []

    def handle(_job, item):
        seen.append(item.item_id)
        if item.item_id == "b":
            raise jobs.Parked(_blocked())
        return None

    result = jobs.drive(store, job.job_id, handle, root=root)

    assert seen == ["a", "b"], "the driver claimed past the block"
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause is not None
    assert result.job.cause.reason == "provider-blocked"
    assert result.job.cause.retryable is False
    assert result.processed == 1
    assert result.failed == 0


def test_the_parked_item_is_released_rather_than_failed(queue, cfg):
    """Failing it would strand it: ``retry`` re-arms failed items only for a
    terminal job, and a blocked job is open."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )

    def handle(_job, item):
        if item.item_id == "a":
            raise jobs.Parked(_blocked())
        return None

    jobs.drive(store, job.job_id, handle, root=root)

    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {"a": jobs.ItemState.PENDING, "b": jobs.ItemState.PENDING}
    assert all(item.claimed_by is None for item in jobs.items(store, job.job_id))
    assert all(item.cause is None for item in jobs.items(store, job.job_id))


def test_a_blocked_job_is_re_driven_from_the_parked_item_on_the_next_drive(queue, cfg):
    """The person resumes after checking the account, and the item that was in
    flight is the first one redone. Done items stay done."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )
    attempts: list[str] = []
    park = {"b"}

    def handle(_job, item):
        attempts.append(item.item_id)
        if item.item_id in park:
            raise jobs.Parked(_blocked())
        return None

    jobs.drive(store, job.job_id, handle, root=root)
    park.clear()
    result = jobs.drive(store, job.job_id, handle, root=root)

    assert attempts == ["a", "b", "b"]
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert result.job.cause is None


def test_parked_is_not_the_item_boundary(queue, cfg):
    """A plain refusal still fails the item and moves on; only the park signal
    stops the run. Both shapes in one job, so the difference is measured rather
    than assumed."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )

    def handle(_job, item):
        if item.item_id == "a":
            raise CratekitError(_throttled())
        if item.item_id == "c":
            raise jobs.Parked(_blocked())
        return None

    result = jobs.drive(store, job.job_id, handle, root=root)

    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {
        "a": jobs.ItemState.FAILED,
        "b": jobs.ItemState.DONE,
        "c": jobs.ItemState.PENDING,
    }
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.failed == 1


# ═══════════════════════════════════════════════════════════════════════════
# Declining (U169): the item is settled as skipped, and the job can succeed
# ═══════════════════════════════════════════════════════════════════════════


def _lossy() -> Cause:
    return Cause(
        reason="lossy-refused",
        message="the provider offers this track lossy only",
        remediation=Remediation(remedy=Remedy.RELAX_LOSSLESS_POLICY),
        scope=Scope.ITEM,
        retryable=False,
    )


def _declining(*declined: str, failing: tuple[str, ...] = ()):
    def handle(_job, item):
        if item.item_id in declined:
            raise jobs.Declined(_lossy())
        if item.item_id in failing:
            raise CratekitError(_throttled())
        return None

    return handle


def test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds(queue, cfg):
    """Sitting 47: three landed and one refused by policy is a finished job."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c", "d"]
    )

    result = jobs.drive(store, job.job_id, _declining("c"), root=root)

    assert result.job.state is jobs.JobState.SUCCEEDED
    assert result.job.cause is None
    assert (result.processed, result.failed, result.declined) == (3, 0, 1)
    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert held["c"].state is jobs.ItemState.SKIPPED
    assert held["c"].cause is not None and held["c"].cause.reason == "lossy-refused"
    assert held["c"].claimed_by is None
    assert all(held[key].state is jobs.ItemState.DONE for key in "abd")
    assert jobs.progress(store, job.job_id)["settled"] == 4


def test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing(queue, cfg):
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])

    result = jobs.drive(store, job.job_id, _declining("a"), root=root)

    assert result.job.state is jobs.JobState.SUCCEEDED
    assert (result.processed, result.failed, result.declined) == (0, 0, 1)


def test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both(queue, cfg):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )

    result = jobs.drive(store, job.job_id, _declining("b", failing=("c",)), root=root)

    assert result.job.state is jobs.JobState.FAILED
    cause = result.job.cause
    assert cause is not None
    assert cause.reason == "unavailable-transient", "a decline leaked into the verdict"
    assert cause.retryable is True
    assert cause.detail["declined"] == 1
    assert "1 more were declined and skipped" in cause.message
    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {
        "a": jobs.ItemState.DONE,
        "b": jobs.ItemState.SKIPPED,
        "c": jobs.ItemState.FAILED,
    }


def test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled(queue, cfg):
    """The policy that refused it is frozen on the job, so asking again would
    only be refused again."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )
    jobs.drive(store, job.job_id, _declining("a", failing=("b",)), root=root)
    jobs.retry(store, job.job_id)

    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {
        "a": jobs.ItemState.SKIPPED,
        "b": jobs.ItemState.PENDING,
        "c": jobs.ItemState.DONE,
    }


def test_a_job_with_no_decline_reports_no_declined_count(queue, cfg):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b"]
    )

    result = jobs.drive(store, job.job_id, _declining(failing=("a",)), root=root)

    assert result.job.cause is not None
    assert "declined" not in result.job.cause.detail
    assert "declined" not in result.job.cause.message


def test_a_retryable_cause_cannot_decline_an_item():
    with pytest.raises(ValueError, match="cannot decline"):
        jobs.Declined(_throttled())


def test_a_handler_that_declines_a_retryable_cause_fails_the_item_rather_than_skipping_it(
    queue, cfg
):
    """The guard bites inside a drive: the item boundary turns it into a failure."""
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])

    def handle(_job, item):
        raise jobs.Declined(_throttled())

    with pytest.raises(CratekitError):
        jobs.drive(store, job.job_id, handle, root=root)

    (item,) = jobs.items(store, job.job_id)
    assert item.state is jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "internal-error"


# ═══════════════════════════════════════════════════════════════════════════
# Part 11: stale intake jobs, named by playlist and cancelled in one pass (U182)
# ═══════════════════════════════════════════════════════════════════════════


def _intake_job(
    store,
    cfg,
    job_id: str,
    *,
    tracks: tuple[str, ...],
    days: float,
    source: str = "pl-a",
    name: str | None = "Warmup",
    handler_key: str = "intake.playlist",
) -> jobs.Job:
    """An intake job as a sweep queues it, ``days`` old, its tracks frozen and itemed."""
    payload: dict = {"source": source, "tracks": {t: {"artist": "A", "title": t} for t in tracks}}
    if name is not None:
        payload["playlist_name"] = name
    jobs.enqueue(
        store, handler_key=handler_key, payload=payload, cfg=cfg, item_ids=tracks, job_id=job_id
    )
    stamp = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with store.immediate() as conn:
        conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (stamp, job_id))
    return jobs.get(store, job_id)


def _stale(envelope: dict) -> dict:
    progress = envelope["data"]["progress"]
    return {field: [row["job_id"] for row in progress[field]] for field in ("cancel", "kept", "left")}


def _state(store, job_id: str) -> jobs.JobState:
    return jobs.get(store, job_id).state


def test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for(cfg, default_queue):
    """Sitting 51 could not judge 17 jobs: the playlist was frozen and never said."""
    _intake_job(default_queue, cfg, "named", tracks=("1",), days=40)
    _intake_job(default_queue, cfg, "by-hand", tracks=("2",), days=40, source="pl-z", name=None)
    jobs.enqueue(default_queue, handler_key="job.resume", payload={}, cfg=cfg, job_id="other")

    code, shown = _drive_cli(["job", "show", "named"])
    assert code == int(ExitCode.OK), shown
    assert shown["data"]["progress"]["playlist"] == "Warmup"
    assert shown["data"]["progress"]["source"] == "pl-a"

    code, listed = _drive_cli(["job", "list"])
    rows = {row["job_id"]: row for row in listed["data"]["progress"]["jobs"]}
    assert rows["named"]["playlist"] == "Warmup"
    assert rows["by-hand"]["playlist"] == "pl-z", "a job queued by hand is named by its source"
    assert "playlist" not in rows["other"], "a job of another verb gains no field"


def test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two(
    cfg, default_queue
):
    """The brief's first scenario: two jobs share a track set, one is older."""
    _intake_job(default_queue, cfg, "copy-old", tracks=("1", "2"), days=50)
    _intake_job(default_queue, cfg, "copy-new", tracks=("2", "1"), days=45, source="pl-b", name="Peak")
    _intake_job(default_queue, cfg, "lone", tracks=("3",), days=60, source="pl-c", name="Close")

    code, envelope = _drive_cli(["job", "cancel", "--stale-days", "30", "--dry-run"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _stale(envelope) == {"cancel": ["copy-old", "lone"], "kept": ["copy-new"], "left": []}
    rows = {row["job_id"]: row for row in envelope["data"]["progress"]["cancel"]}
    assert rows["copy-old"]["kept"] == "copy-new"
    assert "copy-new is kept" in rows["copy-old"]["reason"]
    assert rows["lone"]["kept"] is None
    assert rows["copy-old"]["same_tracks"] == ["copy-new"]
    assert "frees playlist 'Close' (pl-c)" in rows["lone"]["frees"]
    (kept,) = envelope["data"]["progress"]["kept"]
    assert "newest of 2" in kept["reason"]
    for job_id in ("copy-old", "copy-new", "lone"):
        assert _state(default_queue, job_id) is jobs.JobState.QUEUED, "a dry run cancelled"


def test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger(
    cfg, default_queue
):
    _intake_job(default_queue, cfg, "copy-old", tracks=("1", "2"), days=50)
    _intake_job(default_queue, cfg, "copy-new", tracks=("1", "2"), days=45, source="pl-b")
    _intake_job(default_queue, cfg, "young", tracks=("4",), days=3, source="pl-d")

    code, envelope = _drive_cli(["job", "cancel", "--stale-days", "30"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert _stale(envelope) == {"cancel": ["copy-old"], "kept": ["copy-new"], "left": ["young"]}
    assert _state(default_queue, "copy-old") is jobs.JobState.CANCELLED
    assert _state(default_queue, "copy-new") is jobs.JobState.QUEUED
    assert _state(default_queue, "young") is jobs.JobState.QUEUED
    (left,) = envelope["data"]["progress"]["left"]
    assert "within the 30 day(s)" in left["reason"]
    assert jobs.get(default_queue, "copy-old").cause.reason == "cancelled"


def test_a_running_job_is_never_listed_for_cancel_however_old(cfg, default_queue):
    """A row running under a live driver, and a queued row a driver holds."""
    _intake_job(default_queue, cfg, "driven", tracks=("1",), days=90)
    _intake_job(default_queue, cfg, "held", tracks=("2",), days=90, source="pl-b")
    jobs.transition(default_queue, "driven", jobs.JobState.RUNNING)
    with jobs.driver_lock("driven"), jobs.driver_lock("held"):
        code, envelope = _drive_cli(["job", "cancel", "--stale-days", "1"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    found = _stale(envelope)
    assert found["cancel"] == [] and found["kept"] == []
    assert sorted(found["left"]) == ["driven", "held"]
    assert _state(default_queue, "driven") is jobs.JobState.RUNNING
    assert _state(default_queue, "held") is jobs.JobState.QUEUED


def test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel(cfg, default_queue):
    _intake_job(default_queue, cfg, "parked", tracks=("1",), days=90)
    jobs.block(default_queue, "parked", _throttled())
    elsewhere = config.from_dict(
        {**cfg.to_toml_dict(), "library": {**cfg.to_toml_dict()["library"], "volume_id": "0000-1111"}}
    )
    _intake_job(default_queue, elsewhere, "foreign", tracks=("2",), days=90, source="pl-b")

    code, envelope = _drive_cli(["job", "cancel", "--stale-days", "1"])

    assert _stale(envelope) == {"cancel": [], "kept": [], "left": ["parked"]}
    (left,) = envelope["data"]["progress"]["left"]
    assert "crate job cancel parked" in left["reason"]
    assert _state(default_queue, "foreign") is jobs.JobState.QUEUED


def test_a_cancel_whose_playlist_another_open_job_holds_says_it_frees_nothing_yet(
    cfg, default_queue
):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    _intake_job(default_queue, cfg, "new", tracks=("2",), days=2)

    code, envelope = _drive_cli(["job", "cancel", "--stale-days", "30", "--dry-run"])

    (row,) = envelope["data"]["progress"]["cancel"]
    assert row["frees"] == "frees nothing yet: job new still holds playlist 'Warmup' (pl-a) out of every pass"


def test_a_negative_day_count_is_the_parsers_usage_error_and_cancels_nothing(cfg, default_queue):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    import io  # noqa: PLC0415

    from cratekit import cli  # noqa: PLC0415

    code = cli.run(
        ["--output", "json", "job", "cancel", "--stale-days", "-1"],
        stdout=io.StringIO(),
        stderr=io.StringIO(),
    )
    assert code == int(ExitCode.USAGE)
    assert _state(default_queue, "old") is jobs.JobState.QUEUED


def test_a_job_id_beside_stale_days_is_a_usage_error(cfg, default_queue):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    import io  # noqa: PLC0415

    from cratekit import cli  # noqa: PLC0415

    code = cli.run(
        ["--output", "json", "job", "cancel", "old", "--stale-days", "1"],
        stdout=io.StringIO(),
        stderr=io.StringIO(),
    )
    assert code == int(ExitCode.USAGE)
    assert _state(default_queue, "old") is jobs.JobState.QUEUED


def test_a_dry_run_of_one_job_cancels_nothing(cfg, default_queue):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)

    code, envelope = _drive_cli(["job", "cancel", "old", "--dry-run"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["dry_run"] is True
    assert _state(default_queue, "old") is jobs.JobState.QUEUED


def test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command(
    cfg, default_queue
):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    _drive_cli(["job", "cancel", "--stale-days", "30"])

    code, shown = _drive_cli(["job", "show", "old"])

    assert shown["data"]["state"] == "cancelled"
    assert shown["data"]["cause"]["reason"] == "cancelled"
