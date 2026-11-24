"""U10: the job engine's properties, each named for the failure it prevents. Only a killed
process leaves a claimed item with no driver, so the subprocess tests are not slow copies.
"""

from __future__ import annotations

import dataclasses
import io
import json
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
import time
import tomllib
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import tomli_w

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

DONE, FAILED = jobs.ItemState.DONE, jobs.ItemState.FAILED
PENDING, SKIPPED = jobs.ItemState.PENDING, jobs.ItemState.SKIPPED
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
WORKER = Path(__file__).resolve().parent / "job_worker.py"


def _config_document(tmp_path: Path, **overrides) -> dict:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root),
            "volume_id": "F1E2-D3C4",
            "db_path": str(root / "db" / "master.db"),
        },
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
        **overrides,
    }


@pytest.fixture
def cfg(tmp_path):
    """A saved, loadable configuration. ``enqueue`` freezes exactly this."""
    built = config.from_dict(_config_document(tmp_path))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(scope="session")
def _queue_template(tmp_path_factory):
    """A fresh queue made once. A copy opens without the schema's commits."""
    path = tmp_path_factory.mktemp("queue-template") / jobs.QUEUE_FILENAME
    jobs.open_store(path).close()
    return path


def _seed(template: Path, path: Path) -> None:
    config.mkdir_private(path.parent)
    shutil.copyfile(template, path)


@pytest.fixture
def queue(tmp_path, _queue_template):
    """A queue in its own directory, so lock and log files are visible to a test."""
    root = tmp_path / "jobs"
    _seed(_queue_template, root / jobs.QUEUE_FILENAME)
    with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
        yield store, root


@pytest.fixture
def store(queue):
    return queue[0]


@pytest.fixture
def root(queue):
    return queue[1]


@pytest.fixture
def default_queue(cfg, _queue_template):
    """A queue at the DECLARED path, so the verbs find it the way a user would."""
    _seed(_queue_template, jobs.queue_path())
    with jobs.open_store() as store:
        yield store


def _job(store, cfg, *ids: str, payload=None, **kwargs) -> jobs.Job:
    kwargs.setdefault("handler_key", "job.resume")
    return jobs.enqueue(store, payload=payload or {}, cfg=cfg, item_ids=list(ids), **kwargs)


def _states(store, job_id: str) -> dict[str, jobs.ItemState]:
    return {item.item_id: item.state for item in jobs.items(store, job_id)}


def _child_env() -> dict[str, str]:
    return {**os.environ, "PYTHONPATH": str(SRC_ROOT)}


def _spawn_worker(*args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(WORKER), *args], env=_child_env(), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _wait_for(path: Path, *, seconds: float = 20.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"{path.name} never appeared within {seconds}s")


@contextmanager
def _held(job_id: str, root: Path):
    """A real process holding ``job_id``'s driver lock, killed on exit."""
    holder = _spawn_worker("hold", job_id, str(root))
    try:
        _wait_for(root / f"holding-{job_id}")
        yield holder
    finally:
        holder.kill()
        holder.wait(timeout=20)


def _attempts(ledger: Path) -> list[str]:
    return [line for line in ledger.read_text().splitlines() if line]


def _refused(call) -> Cause:
    with pytest.raises(CratekitError) as excinfo:
        call()
    return excinfo.value.cause


def _drive_cli(argv: list[str]) -> tuple[int, dict]:
    from cratekit import cli  # noqa: PLC0415
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def _ok(argv: list[str]) -> dict:
    code, envelope = _drive_cli(argv)
    assert code == int(ExitCode.OK), envelope
    return envelope


# Part 1: state discipline ported from the source manifest
def test_a_queued_job_freezes_the_whole_configuration_not_a_subset(store, cfg):
    """KTD9. A frozen subset un-freezes itself the next time somebody reads a key."""
    job = _job(store, cfg, payload={"x": 1})
    assert job.config_fingerprint == cfg.fingerprint()
    assert jobs.frozen_config(job).to_toml_dict() == cfg.to_toml_dict()
    assert job.library_id == cfg.library.volume_id


def test_a_job_records_the_library_it_targets(store, cfg):
    """A queue drained after a reconfigure still knows the volume it was planned for."""
    assert _job(store, cfg).library_id == cfg.library.volume_id


def test_a_config_that_changed_while_queued_names_what_drifted(store, cfg, tmp_path):
    """KTD9: the job runs on its frozen copy and names the keys that moved."""
    job = _job(store, cfg)
    assert jobs.drift(job, cfg) == ()
    moved = config.from_dict(
        {**cfg.to_toml_dict(), "paths": {"download_staging": str(tmp_path / "elsewhere")}})
    assert jobs.drift(job, moved) == ("paths.download_staging",)
    assert jobs.frozen_config(job).paths.download_staging == cfg.paths.download_staging


def test_a_job_frozen_under_the_retired_adapter_key_reports_no_drift(store, cfg):
    """U197: the old adapter key is no drift, while a real move is still named."""
    job = _job(store, cfg)
    assert cfg.acquisition.adapter == "vendored"
    frozen = tomllib.loads(job.config_toml)
    frozen["acquisition"]["adapter"] = "tidal_dl_ng"
    before_rename = dataclasses.replace(
        job, config_toml=tomli_w.dumps(frozen), config_fingerprint="queued before U197")
    assert jobs.drift(before_rename, cfg) == ()
    switched = config.from_dict(
        {**cfg.to_toml_dict(), "acquisition": {**frozen["acquisition"], "adapter": "streamrip"}})
    assert jobs.drift(before_rename, switched) == ("acquisition.adapter",)


def test_the_retired_key_fold_leaves_a_value_that_is_not_a_name_as_written(store, tmp_path):
    """Only a name is folded, as the loader folds only a name."""
    document = _config_document(tmp_path, profile={"name": "slim"}, acquisition={"adapter": 5})
    job = _job(store, config.from_dict(document))
    moved = config.from_dict({**document, "paths": {"download_staging": str(tmp_path / "x")}})
    assert jobs.drift(job, moved) == ("paths.download_staging",)


def test_transitions_are_forward_only(store, cfg):
    job = _job(store, cfg)
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    cause = _refused(lambda: jobs.transition(store, job.job_id, jobs.JobState.RUNNING))
    assert cause.reason == "internal-error"


def test_an_unrecognized_state_on_disk_coerces_to_an_open_state_never_a_terminal_one(store, cfg):
    """Degrading to ``queued`` costs a re-drive; to ``succeeded`` it is a false success."""
    job = _job(store, cfg, "a")
    store.conn.execute("UPDATE jobs SET state = ? WHERE job_id = ?", ("something-else", job.job_id))
    store.conn.execute("UPDATE job_items SET state = ? WHERE job_id = ?", ("nonsense", job.job_id))
    assert jobs.get(store, job.job_id).state is jobs.JobState.QUEUED
    assert jobs.items(store, job.job_id)[0].state is PENDING


def test_a_queue_written_at_another_schema_refuses_to_resume(tmp_path):
    path = tmp_path / "jobs" / jobs.QUEUE_FILENAME
    jobs.open_store(path).close()
    conn = sqlite3.connect(str(path))
    conn.execute("UPDATE queue_schema SET version = 99")
    conn.commit()
    conn.close()
    cause = _refused(lambda: jobs.open_store(path))
    assert cause.reason == "job-schema-mismatch"
    assert cause.code is ExitCode.PRECONDITION


def test_an_unknown_job_refuses_with_a_code_from_the_vocabulary(store):
    cause = _refused(lambda: jobs.get(store, "no-such-job"))
    assert cause.reason == "job-unknown"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.remediation.steps


def test_states_of_answers_for_the_names_it_knows_and_omits_the_rest(store, cfg):
    open_job = _job(store, cfg)
    done = _job(store, cfg)
    jobs.transition(store, done.job_id, jobs.JobState.SUCCEEDED)
    answered = jobs.states_of(store, [open_job.job_id, done.job_id, "no-such-job"])
    assert answered == {open_job.job_id: jobs.JobState.QUEUED, done.job_id: jobs.JobState.SUCCEEDED}
    assert jobs.states_of(store, []) == {}


def test_states_of_answers_past_the_parameter_limit_of_one_statement(store, cfg):
    """More names than fit one ``IN`` clause (R-289), copied from one enqueued row."""
    made = [f"job-{n:05d}" for n in range(jobs._ID_CHUNK + 7)]
    _job(store, cfg, job_id=made[0])
    row = dict(store.conn.execute("SELECT * FROM jobs WHERE job_id = ?", (made[0],)).fetchone())
    columns = ", ".join(row)
    with store.immediate() as conn:
        conn.executemany(
            f"INSERT INTO jobs ({columns}) VALUES ({', '.join('?' for _ in row)})",
            [tuple({**row, "job_id": job_id}.values()) for job_id in made[1:]])
    answered = jobs.states_of(store, [*made, "no-such-job"])
    assert len(answered) == len(made)
    assert set(answered) == set(made)
    assert set(answered.values()) == {jobs.JobState.QUEUED}


def test_a_stored_cause_that_cannot_be_read_back_is_not_read_as_success(store, cfg):
    """None means "no failure". An unparseable cause must never mean that."""
    job = _job(store, cfg)
    store.conn.execute("UPDATE jobs SET cause = ? WHERE job_id = ?", ("{not json", job.job_id))
    reloaded = jobs.get(store, job.job_id)
    assert reloaded.cause is not None
    assert reloaded.cause.reason == "no-evidence"


def test_everything_the_queue_writes_is_owner_only_under_any_umask(tmp_path, cfg):
    """Audited by walking the directory, so SQLite's sidecars and directories count."""
    previous = os.umask(0o000)
    try:
        root = tmp_path / "queue-root"
        with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
            job = _job(store, cfg, "a")
            # Every writer: the database and sidecars, a driver lock, a job log.
            with jobs.driver_lock(job.job_id, root=root):
                pass
            jobs.log_path(job.job_id, root=root).write_bytes(b"")
            pid = jobs.spawn(store, job, ["--version"], root=root, env=_child_env())
            os.waitpid(pid, 0)
    finally:
        os.umask(previous)
    written = sorted(root.rglob("*"))
    exposed = [str(path.relative_to(root)) for path in written if path.stat().st_mode & 0o077]
    assert not exposed, f"group or world accessible under the queue root: {exposed}"
    assert root.stat().st_mode & 0o077 == 0, "the queue directory itself is exposed"


# Part 2: blocked needs a reason (KTD25)
def _throttled() -> Cause:
    return Cause(
        reason="unavailable-transient", message="the provider asked us to slow down",
        remediation=Remediation(remedy=Remedy.RETRY_LATER), scope=Scope.SOURCE, retryable=True)


def _needs_acknowledgment() -> Cause:
    return Cause(
        reason="backup-acknowledgment-missing",
        message="this session has no recorded backup acknowledgment",
        remediation=Remediation(remedy=Remedy.ACKNOWLEDGE_BACKUP), scope=Scope.SESSION)


def test_two_jobs_parked_under_one_state_still_carry_two_different_remediations(store, cfg):
    """Both ``blocked``; the difference is a field, not a log line."""
    throttled = _job(store, cfg, payload={"a": 1})
    unacknowledged = _job(store, cfg, payload={"b": 2})
    jobs.block(store, throttled.job_id, _throttled())
    jobs.block(store, unacknowledged.job_id, _needs_acknowledgment())
    first = jobs.get(store, throttled.job_id)
    second = jobs.get(store, unacknowledged.job_id)
    assert first.state is second.state is jobs.JobState.BLOCKED
    assert first.cause.reason != second.cause.reason
    assert first.cause.remediation.remedy is Remedy.RETRY_LATER
    assert second.cause.remediation.remedy is Remedy.ACKNOWLEDGE_BACKUP


def test_parking_a_job_without_a_reason_is_refused(store, cfg):
    job = _job(store, cfg)
    with pytest.raises(CratekitError):
        jobs.transition(store, job.job_id, jobs.JobState.BLOCKED)


# Part 3: durability (KTD8)
def test_the_artifact_is_flushed_and_renamed_before_the_row_flips_to_done(
        store, root, cfg, tmp_path, monkeypatch):
    """The ordering is the guarantee: "done" is what a resume trusts."""
    job = _job(store, cfg, "one")
    events: list[str] = []
    def recorded(event, real):
        return lambda *a, **k: (events.append(event), real(*a, **k))[1]
    monkeypatch.setattr(os, "fsync", recorded("fsync", os.fsync))
    monkeypatch.setattr(os, "replace", recorded("replace", os.replace))
    monkeypatch.setattr(jobs, "complete_item", recorded("done", jobs.complete_item))
    staged = tmp_path / "staged.txt"
    staged.write_text("payload")
    produced = jobs.Produced(staged=staged, final=tmp_path / "out" / "one.txt")
    jobs.drive(store, job.job_id, lambda _job, _item: produced, root=root)
    assert events == ["fsync", "replace", "fsync", "done"], events
    assert (tmp_path / "out" / "one.txt").read_text() == "payload"
    assert not staged.exists()


def test_an_item_that_produces_nothing_still_completes(store, root, cfg):
    job = _job(store, cfg, "a")
    result = jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    assert result.processed == 1
    assert result.job.state is jobs.JobState.SUCCEEDED


# Part 4: never an empty success
def test_a_job_whose_every_item_fails_raises_rather_than_reporting_success(store, root, cfg):
    """Empty means verified empty only when the lookups succeeded."""
    job = _job(store, cfg, "a", "b", "c")
    broken = _failing(broken=("a", "b", "c"))
    cause = _refused(lambda: jobs.drive(store, job.job_id, broken, root=root))
    assert cause.reason == "no-evidence"
    # internal-error is not retryable, so neither is the envelope (R-380).
    assert cause.retryable is False
    # Recorded BEFORE the raise, never left saying running.
    recorded = jobs.get(store, job.job_id)
    assert recorded.state is jobs.JobState.FAILED
    assert recorded.cause is not None
    assert recorded.cause.retryable is False


def test_attempting_nothing_is_a_no_op_and_not_a_failure(store, root, cfg):
    """An up-to-date source must not look broken."""
    job = _job(store, cfg)
    result = jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    assert result.processed == 0
    assert result.job.state is jobs.JobState.SUCCEEDED
    jobs.evidence_or_raise(attempted=0, succeeded=0)


def test_a_partial_failure_fails_the_job_and_keeps_the_successes(store, root, cfg):
    job = _job(store, cfg, "good", "bad")
    result = jobs.drive(store, job.job_id, _failing(broken=("bad",)), root=root)
    assert (result.processed, result.failed) == (1, 1)
    assert result.job.state is jobs.JobState.FAILED
    assert _states(store, job.job_id) == {"good": DONE, "bad": FAILED}


def _permanent_lookup() -> CratekitError:
    return refuse(
        "sync-source-lookups-failed", "the provider has no artist named for this label",
        steps=("retry this source when the provider is reachable",), origin=("test",))


def _transient_outage() -> CratekitError:
    return refuse(
        "unavailable-transient", "the provider asked us to slow down",
        remedy=Remedy.RETRY_LATER, retryable=True, origin=("test",))


def _failing(permanent=(), transient=(), broken=()):

    def handle(_job, item):
        if item.item_id in permanent:
            raise _permanent_lookup()
        if item.item_id in transient:
            raise _transient_outage()
        if item.item_id in broken:
            raise RuntimeError("this one is broken")
        return None
    return handle


@pytest.mark.parametrize("ids", [("a", "b"), ("a", "b", "c")], ids=["two-items", "three-items"])
def test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable(
        store, root, cfg, ids):
    """R-380 and R-266: permanent items are not retryable; R-391 keeps one shared reason."""
    job = _job(store, cfg, *ids)
    envelope = _refused(lambda: jobs.drive(store, job.job_id, _failing(permanent=ids), root=root))
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
    assert "permanent_reasons" not in recorded.cause.detail
    assert "mixed" not in recorded.cause.message


def test_a_partial_failure_whose_failures_are_permanent_is_not_resumable(store, root, cfg):
    """Some items done, every failure permanent: resume cannot help."""
    job = _job(store, cfg, "good", "bad")
    result = jobs.drive(store, job.job_id, _failing(permanent=("bad",)), root=root)
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
    settled = {"good": DONE, "bad": FAILED}
    assert _states(store, job.job_id) == settled
    # R-390: ``retry`` holds the verdict and re-arms nothing.
    refusal = _refused(lambda: jobs.retry(store, job.job_id))
    assert refusal.reason == "job-not-retryable"
    assert refusal.code is ExitCode.PRECONDITION
    assert refusal.inner is not None
    assert refusal.inner.reason == "sync-source-lookups-failed"
    assert "permanent_reasons" not in refusal.detail
    untouched = jobs.get(store, job.job_id)
    assert untouched.state is jobs.JobState.FAILED
    assert untouched.cause is not None
    assert untouched.cause.reason == "sync-source-lookups-failed"
    assert _states(store, job.job_id) == settled


def test_a_failed_job_with_no_recorded_cause_still_re_arms(store, cfg):
    """R-390: a missing verdict, as a build before R-380 left, is not a permanent one."""
    job = _job(store, cfg, "a", "b")
    broke = Cause(
        reason="internal-error", message="this one broke",
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT), origin=("test",))
    jobs.fail_item(store, job.job_id, "a", cause=broke)
    jobs.transition(store, job.job_id, jobs.JobState.FAILED)
    recorded = jobs.get(store, job.job_id)
    assert recorded.state is jobs.JobState.FAILED
    assert recorded.cause is None
    retried = jobs.retry(store, job.job_id)
    assert retried.state is jobs.JobState.QUEUED
    assert _states(store, job.job_id)["a"] is PENDING


def test_resuming_a_job_of_permanent_failures_through_the_verb_refuses(cfg, default_queue):
    """R-390 at the shell: refused in the foreground, the items left as they were."""
    root = jobs.store_dir()
    job = _job(default_queue, cfg, "good", "bad", job_id="job-permanent")
    jobs.drive(default_queue, job.job_id, _failing(permanent=("bad",)), root=root)
    code, envelope = _drive_cli(["job", "resume", "job-permanent"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "job-not-retryable"
    assert envelope["cause"]["inner"]["reason"] == "sync-source-lookups-failed"
    assert envelope["cause"]["remediation"]["remedy"] is None
    assert envelope["cause"]["remediation"]["steps"]
    assert _states(default_queue, job.job_id) == {"good": DONE, "bad": FAILED}
    assert jobs.get(default_queue, job.job_id).state is jobs.JobState.FAILED


def test_two_distinct_permanent_reasons_name_both_whichever_failed_last(store, root, cfg):
    """R-391: in both item orders, the verdict is the set of reasons, not the last."""
    mixed_permanent = _failing(permanent=("lookup",), broken=("broken",))
    both = ("internal-error", "sync-source-lookups-failed")
    causes = []
    for order in (["lookup", "broken"], ["broken", "lookup"]):
        job = _job(store, cfg, *order)
        raised = _refused(lambda: jobs.drive(store, job.job_id, mixed_permanent, root=root))
        # The envelope nests the last item and names every reason beside it.
        assert raised.reason == "no-evidence"
        assert raised.inner is not None
        assert raised.inner.reason in both
        assert tuple(raised.detail["permanent_reasons"]) == both
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
        # Read back through JSON as a sequence: the ORDER is what is pinned.
        assert tuple(cause.detail["permanent_reasons"]) == both
    assert causes[0].reason == causes[1].reason
    assert causes[0].detail["permanent_reasons"] == causes[1].detail["permanent_reasons"]
    # The resume refusal names them at its own top level (R-390 over R-391).
    refusal = _refused(lambda: jobs.retry(store, job.job_id))
    assert refusal.reason == "job-not-retryable"
    assert tuple(refusal.detail["permanent_reasons"]) == both


def test_a_job_whose_failures_include_a_retryable_cause_stays_retryable(store, root, cfg):
    """A resume can still help the items that failed transiently."""
    job = _job(store, cfg, "good", "perm", "temp")
    handle = _failing(permanent=("perm",), transient=("temp",))
    result = jobs.drive(store, job.job_id, handle, root=root)
    assert (result.processed, result.failed) == (1, 2)
    cause = result.job.cause
    assert cause is not None
    assert cause.retryable is True
    assert cause.reason == "unavailable-transient"
    assert cause.remediation.remedy is Remedy.RESUME_JOB
    assert "1 retryable" in cause.message
    assert "1 permanent" in cause.message


def test_an_all_failed_job_that_includes_a_retryable_cause_stays_retryable(store, root, cfg):
    job = _job(store, cfg, "perm", "temp")
    handle = _failing(permanent=("perm",), transient=("temp",))
    cause = _refused(lambda: jobs.drive(store, job.job_id, handle, root=root))
    assert cause.reason == "no-evidence"
    assert cause.retryable is True
    assert cause.remediation.remedy is Remedy.RETRY_LATER


# Part 5: cancelled is not failed, and an interrupt aborts before a commit
def test_cancelling_reports_cancelled_rather_than_failed(store, cfg):
    """R22."""
    job = _job(store, cfg, "a")
    cancelled = jobs.cancel(store, job.job_id, stage="planning")
    assert cancelled.state is jobs.JobState.CANCELLED
    assert cancelled.state is not jobs.JobState.FAILED
    assert cancelled.cause.reason == "cancelled"
    assert cancelled.cause.code is ExitCode.INTERRUPTED
    assert cancelled.stage == "planning"


def test_an_interrupt_between_the_work_and_the_commit_leaves_no_artifact(
        store, root, cfg, tmp_path):
    """The abort point is before the commit; the handler signals its own process."""
    job = _job(store, cfg, "a", "b")
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
    # Released, not failed: redone whole on resume.
    assert set(_states(store, job.job_id).values()) == {PENDING}


def test_the_signal_handler_is_restored_afterwards(queue):
    before = signal.getsignal(signal.SIGINT)
    with jobs.interruptible():
        assert signal.getsignal(signal.SIGINT) is not before
    assert signal.getsignal(signal.SIGINT) is before


def test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot(store, root, cfg):
    """Cancelled is terminal and retryable (R-390); succeeded is finished."""
    job = _job(store, cfg, "a")
    jobs.cancel(store, job.job_id)
    cancelled = jobs.get(store, job.job_id)
    assert cancelled.cause is not None
    assert cancelled.cause.retryable is True
    assert jobs.retry(store, job.job_id).state is jobs.JobState.QUEUED
    jobs.drive(store, job.job_id, lambda _j, _i: None, root=root)
    with pytest.raises(CratekitError):
        jobs.retry(store, job.job_id)


# Part 6: one driver per job, decided by holder liveness
def test_a_second_driver_refuses_while_a_live_holder_has_the_lock(store, root, cfg):
    """A slow run is never evicted, which is why there is no timeout anywhere."""
    job = _job(store, cfg)
    with _held(job.job_id, root) as holder:
        with pytest.raises(jobs.DriverHeld) as excinfo:
            with jobs.driver_lock(job.job_id, root=root):
                pass
        assert excinfo.value.cause.reason == "job-driver-held"
        assert excinfo.value.cause.code is ExitCode.LIBRARY_BUSY
        assert str(holder.pid) in excinfo.value.cause.message


def test_a_dead_holders_lock_is_reclaimed_without_any_timeout(store, root, cfg):
    """The kernel releasing a dead holder's lock is the staleness rule."""
    job = _job(store, cfg)
    with _held(job.job_id, root):
        pass
    # No sleep, no grace period: the lock is free the instant the holder is gone.
    with jobs.driver_lock(job.job_id, root=root) as path:
        assert json.loads(path.read_text())["pid"] == os.getpid()


def test_the_lock_file_survives_release(store, root, cfg):
    """Unlinking on release is the classic way to lose the exclusion it provides."""
    job = _job(store, cfg)
    with jobs.driver_lock(job.job_id, root=root):
        pass
    assert jobs.lock_path(job.job_id, root=root).exists()


def test_a_running_row_with_no_live_driver_is_reconciled_back_to_queued(store, root, cfg):
    """Disk truth is the lock, not the row."""
    job = _job(store, cfg, "a")
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING, stage="downloading")
    store.conn.execute(
        "UPDATE job_items SET state = ?, claimed_by = ? WHERE job_id = ?",
        (str(jobs.ItemState.CLAIMED), "a-dead-driver", job.job_id))
    reconciled = jobs.reconcile(store, job.job_id, root=root)
    assert reconciled.state is jobs.JobState.QUEUED
    assert reconciled.stage == "downloading"
    assert jobs.items(store, job.job_id)[0].state is PENDING


def test_reconcile_leaves_a_genuinely_running_job_alone(store, root, cfg):
    job = _job(store, cfg)
    jobs.transition(store, job.job_id, jobs.JobState.RUNNING)
    with _held(job.job_id, root):
        assert jobs.reconcile(store, job.job_id, root=root).state is jobs.JobState.RUNNING


# Part 7: two processes writing job state
def test_two_processes_claiming_the_same_job_never_claim_one_item_twice(store, root, cfg, tmp_path):
    """The claim is one immediate transaction, never a deferred one."""
    item_ids = [f"item-{index:03d}" for index in range(60)]
    job = _job(store, cfg, *item_ids)
    left, right, barrier = tmp_path / "left.log", tmp_path / "right.log", tmp_path / "go"
    for log in (left, right):
        log.write_text("")
    workers = [
        _spawn_worker("claim", str(store.path), job.job_id, str(log), str(barrier))
        for log in (left, right)
    ]
    time.sleep(0.5)  # both are past their imports and waiting on the barrier
    barrier.write_text("go")
    for worker in workers:
        out, err = worker.communicate(timeout=90)
        assert worker.returncode == 0, err or out
    claimed = _attempts(left) + _attempts(right)
    assert sorted(claimed) == sorted(item_ids), "an item was claimed twice or not at all"
    assert set(_states(store, job.job_id).values()) == {DONE}
    assert jobs.progress(store, job.job_id)["settled"] == len(item_ids)
    # Both processes did real work, or the test proved nothing about concurrency.
    assert _attempts(left) and _attempts(right)


# Part 8: the subprocess seam (KTD26) and the handler key seam
def test_the_child_command_re_invokes_the_module_rather_than_a_console_script():
    """A console script's path depends on the install."""
    command = jobs.child_command(["job", "resume", "abc"], executable="/usr/bin/python3")
    assert command == ["/usr/bin/python3", "-m", "cratekit.cli", "job", "resume", "abc"]


def test_a_spawned_job_runs_detached_and_its_output_lands_in_the_jobs_log(store, root, cfg):
    job = _job(store, cfg)
    pid = jobs.spawn(store, job, ["--version"], root=root, env=_child_env())
    assert jobs.get(store, job.job_id).pid == pid
    log = jobs.log_path(job.job_id, root=root)
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and not log.read_text().strip():
        time.sleep(0.05)
    assert log.read_text().strip(), "the detached child produced no output"
    os.waitpid(pid, 0)


def test_the_engine_module_names_no_verb():
    """KTD23: the engine resolves a subcommand through the CLI layer by handler key."""
    from cratekit.cli import registry  # noqa: PLC0415 - a test may look upward
    source = (SRC_ROOT / "cratekit" / "core" / "jobs.py").read_text()
    for name in registry.VERB_NAMES:
        assert f'"{name}"' not in source, f"the engine spells the verb {name!r}"


def test_every_landed_long_running_verb_actually_exposes_the_builder_it_declares():
    """Walks the registry, which cannot itself check that the named builder EXISTS."""
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


# Handler key imports are tests/test_cli_contract.py's (U42); here both refuse unimported.


def test_a_job_queued_for_a_handler_this_build_does_not_register_refuses(store, cfg):
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415
    job = _job(store, cfg, handler_key="not-a-handler")
    cause = _refused(lambda: jobs_cli.argv_for(job))
    assert cause.reason == "internal-error"


def test_a_job_queued_for_a_verb_that_has_not_landed_refuses_rather_than_importing(
        store, cfg, monkeypatch):
    """On a synthetic planned entry, since U25 left the registry with none."""
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415
    from cratekit.cli import registry  # noqa: PLC0415
    unlanded = [e for e in registry.entries() if not e.landed and e.argv_builder]
    assert not unlanded, f"these queued verbs still carry planned_in: {[e.name for e in unlanded]}"
    missing = "cratekit.vocals.missing_shell"
    fake = dataclasses.replace(registry.entry("analyze.vocals"), planned_in="U99", module=missing)
    monkeypatch.setattr(
        registry, "ENTRIES", tuple(fake if e.name == fake.name else e for e in registry.ENTRIES))
    monkeypatch.setattr(registry, "_BY_NAME", {**dict(registry._BY_NAME), fake.name: fake})
    by_handler = {**dict(getattr(registry, "_BY_HANDLER", {})), fake.handler_key: fake}
    monkeypatch.setattr(registry, "_BY_HANDLER", by_handler)
    job = _job(store, cfg, handler_key=fake.handler_key)
    cause = _refused(lambda: jobs_cli.argv_for(job))
    assert cause.reason == "internal-error"
    assert missing not in sys.modules


def test_the_resume_builder_turns_a_frozen_job_back_into_a_command_line(store, cfg):
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415
    job = _job(store, cfg)
    assert jobs_cli.argv_for(job) == ["job", "resume", job.job_id]


# Part 9: the four verbs
def test_listing_an_empty_queue_is_a_no_op_and_not_an_error(cfg, default_queue):
    envelope = _ok(["job", "list"])
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["jobs"] == []


def test_listing_reports_each_job_with_its_progress(cfg, default_queue):
    _job(default_queue, cfg, "a", "b", job_id="job-one")
    envelope = _ok(["job", "list"])
    rows = envelope["data"]["progress"]["jobs"]
    assert [row["job_id"] for row in rows] == ["job-one"]
    assert rows[0]["progress"]["total"] == 2
    assert envelope["data"]["progress"]["counts"]["queued"] == 1


def test_a_state_filter_that_names_nothing_is_refused_rather_than_ignored(cfg, default_queue):
    """A filter matching nothing looks exactly like an empty queue."""
    code, envelope = _drive_cli(["job", "list", "--state", "sideways"])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "job-unknown"


def test_showing_a_broken_job_succeeds_and_carries_the_jobs_cause_in_the_payload(
        cfg, default_queue):
    """Reporting on a failure is not itself a failure (KTD25 one level up)."""
    _job(default_queue, cfg, job_id="job-two")
    jobs.block(default_queue, "job-two", _throttled())
    envelope = _ok(["job", "show", "job-two"])
    assert envelope["cause"] is None
    assert envelope["data"]["state"] == "blocked"
    assert envelope["data"]["cause"]["reason"] == "unavailable-transient"


def test_showing_a_job_whose_config_moved_warns_and_names_the_keys(cfg, default_queue, tmp_path):
    _job(default_queue, cfg, job_id="job-three")
    moved = config.from_dict(
        {**cfg.to_toml_dict(), "paths": {"download_staging": str(tmp_path / "elsewhere")}})
    config.save(moved)
    config.reset_cache()
    envelope = _ok(["job", "show", "job-three"])
    assert envelope["warnings"], "a drifted configuration was not reported"
    assert "paths.download_staging" in envelope["warnings"][0]["message"]


def test_cancelling_through_the_verb_succeeds_and_reports_cancelled(cfg, default_queue):
    """A cancel that exited non-zero could not be told from a cancel that failed."""
    _job(default_queue, cfg, job_id="job-four")
    envelope = _ok(["job", "cancel", "job-four"])
    assert envelope["data"]["state"] == "cancelled"
    assert envelope["data"]["cause"]["reason"] == "cancelled"


def test_resuming_a_job_a_live_driver_already_holds_refuses_in_the_foreground(cfg, default_queue):
    """The refusal has to reach the person, not a detached child's log file."""
    _job(default_queue, cfg, job_id="job-five")
    with _held("job-five", jobs.store_dir()):
        code, envelope = _drive_cli(["job", "resume", "job-five"])
        assert code == int(ExitCode.LIBRARY_BUSY)
        assert envelope["cause"]["reason"] == "job-driver-held"


def test_every_job_verb_refuses_an_unknown_identifier_with_the_same_code(cfg, default_queue):
    for argv in (["job", "show"], ["job", "cancel"], ["job", "resume"]):
        code, envelope = _drive_cli([*argv, "no-such-job"])
        assert code == int(ExitCode.PRECONDITION), argv
        assert envelope["cause"]["reason"] == "job-unknown", argv


# Parking: the run stops, the item goes back, and nothing else is claimed
def _blocked() -> Cause:
    return Cause(
        reason="provider-blocked", message="the provider refused this client",
        remediation=Remediation(steps=("check the account",)), scope=Scope.RUN, retryable=False)


def _parking(park: set[str], seen: list[str] | None = None):

    def handle(_job, item):
        if seen is not None:
            seen.append(item.item_id)
        if item.item_id in park:
            raise jobs.Parked(_blocked())
        return None
    return handle


def test_a_parked_item_blocks_the_job_and_claims_nothing_further(store, root, cfg):
    """A block is about the client, so the engine claims nothing after it."""
    job = _job(store, cfg, "a", "b", "c")
    seen: list[str] = []
    result = jobs.drive(store, job.job_id, _parking({"b"}, seen), root=root)
    assert seen == ["a", "b"], "the driver claimed past the block"
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause is not None
    assert result.job.cause.reason == "provider-blocked"
    assert result.job.cause.retryable is False
    assert result.processed == 1
    assert result.failed == 0


def test_the_parked_item_is_released_rather_than_failed(store, root, cfg):
    """Failing it would strand it, since a blocked job is open and not retried."""
    job = _job(store, cfg, "a", "b")
    jobs.drive(store, job.job_id, _parking({"a"}), root=root)
    assert _states(store, job.job_id) == {"a": PENDING, "b": PENDING}
    assert all(item.claimed_by is None for item in jobs.items(store, job.job_id))
    assert all(item.cause is None for item in jobs.items(store, job.job_id))


def test_a_blocked_job_is_re_driven_from_the_parked_item_on_the_next_drive(store, root, cfg):
    """The item in flight is the first one redone; done items stay done."""
    job = _job(store, cfg, "a", "b")
    attempts: list[str] = []
    park = {"b"}
    jobs.drive(store, job.job_id, _parking(park, attempts), root=root)
    park.clear()
    result = jobs.drive(store, job.job_id, _parking(park, attempts), root=root)
    assert attempts == ["a", "b", "b"]
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert result.job.cause is None


def test_parked_is_not_the_item_boundary(store, root, cfg):
    """A plain refusal fails the item and moves on; only a park stops the run."""
    job = _job(store, cfg, "a", "b", "c")
    def handle(_job, item):
        if item.item_id == "a":
            raise CratekitError(_throttled())
        if item.item_id == "c":
            raise jobs.Parked(_blocked())
        return None
    result = jobs.drive(store, job.job_id, handle, root=root)
    assert _states(store, job.job_id) == {"a": FAILED, "b": DONE, "c": PENDING}
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.failed == 1


# Declining (U169): the item is settled as skipped, and the job can succeed
def _lossy() -> Cause:
    return Cause(
        reason="lossy-refused", message="the provider offers this track lossy only",
        remediation=Remediation(remedy=Remedy.RELAX_LOSSLESS_POLICY), scope=Scope.ITEM,
        retryable=False)


def _declining(*declined: str, failing: tuple[str, ...] = ()):
    def handle(_job, item):
        if item.item_id in declined:
            raise jobs.Declined(_lossy())
        if item.item_id in failing:
            raise CratekitError(_throttled())
        return None
    return handle


def test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds(store, root, cfg):
    """Three landed and one refused by policy is a finished job."""
    job = _job(store, cfg, "a", "b", "c", "d")
    result = jobs.drive(store, job.job_id, _declining("c"), root=root)
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert result.job.cause is None
    assert (result.processed, result.failed, result.declined) == (3, 0, 1)
    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert held["c"].state is SKIPPED
    assert held["c"].cause is not None and held["c"].cause.reason == "lossy-refused"
    assert held["c"].claimed_by is None
    assert all(held[key].state is DONE for key in "abd")
    assert jobs.progress(store, job.job_id)["settled"] == 4


def test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing(store, root, cfg):
    job = _job(store, cfg, "a")
    result = jobs.drive(store, job.job_id, _declining("a"), root=root)
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert (result.processed, result.failed, result.declined) == (0, 0, 1)


def test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both(store, root, cfg):
    job = _job(store, cfg, "a", "b", "c")
    result = jobs.drive(store, job.job_id, _declining("b", failing=("c",)), root=root)
    assert result.job.state is jobs.JobState.FAILED
    cause = result.job.cause
    assert cause is not None
    assert cause.reason == "unavailable-transient", "a decline leaked into the verdict"
    assert cause.retryable is True
    assert cause.detail["declined"] == 1
    assert "1 more were declined and skipped" in cause.message
    assert _states(store, job.job_id) == {"a": DONE, "b": SKIPPED, "c": FAILED}


def test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled(store, root, cfg):
    """The refusing policy is frozen on the job, so asking again is refused again."""
    job = _job(store, cfg, "a", "b", "c")
    jobs.drive(store, job.job_id, _declining("a", failing=("b",)), root=root)
    jobs.retry(store, job.job_id)
    assert _states(store, job.job_id) == {"a": SKIPPED, "b": PENDING, "c": DONE}


def test_a_job_with_no_decline_reports_no_declined_count(store, root, cfg):
    job = _job(store, cfg, "a", "b")
    result = jobs.drive(store, job.job_id, _declining(failing=("a",)), root=root)
    assert result.job.cause is not None
    assert "declined" not in result.job.cause.detail
    assert "declined" not in result.job.cause.message


def test_a_retryable_cause_cannot_decline_an_item():
    with pytest.raises(ValueError, match="cannot decline"):
        jobs.Declined(_throttled())


def test_a_handler_that_declines_a_retryable_cause_fails_the_item_rather_than_skipping_it(
        store, root, cfg):
    """The guard bites inside a drive: the item boundary turns it into a failure."""
    job = _job(store, cfg, "a")
    def handle(_job, item):
        raise jobs.Declined(_throttled())
    with pytest.raises(CratekitError):
        jobs.drive(store, job.job_id, handle, root=root)
    (item,) = jobs.items(store, job.job_id)
    assert item.state is FAILED
    assert item.cause is not None and item.cause.reason == "internal-error"


# Part 10: stale intake jobs, named by playlist and cancelled in one pass (U182)
def _intake_job(
    store, cfg, job_id: str, *, tracks: tuple[str, ...], days: float, source: str = "pl-a",
    name: str | None = "Warmup", handler_key: str = "intake.playlist", swept: bool = False,
) -> jobs.Job:
    """An intake job as a sweep queues it, ``days`` old, its tracks frozen and itemed."""
    payload: dict = {"source": source, "tracks": {t: {"artist": "A", "title": t} for t in tracks}}
    if name is not None:
        payload["playlist_name"] = name
    if swept:
        payload["source_id"] = "playlists"
    jobs.enqueue(
        store, handler_key=handler_key, payload=payload, cfg=cfg, item_ids=tracks, job_id=job_id)
    stamp = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with store.immediate() as conn:
        conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (stamp, job_id))
    return jobs.get(store, job_id)


def _stale(envelope: dict) -> dict:
    progress = envelope["data"]["progress"]
    return {key: [row["job_id"] for row in progress[key]] for key in ("cancel", "kept", "left")}


def _state(store, job_id: str) -> jobs.JobState:
    return jobs.get(store, job_id).state


def test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for(cfg, default_queue):
    """The playlist was frozen on the job and never said."""
    _intake_job(default_queue, cfg, "named", tracks=("1",), days=40)
    _intake_job(default_queue, cfg, "by-hand", tracks=("2",), days=40, source="pl-z", name=None)
    _job(default_queue, cfg, job_id="other")
    shown = _ok(["job", "show", "named"])
    assert shown["data"]["progress"]["playlist"] == "Warmup"
    assert shown["data"]["progress"]["source"] == "pl-a"
    listed = _ok(["job", "list"])
    rows = {row["job_id"]: row for row in listed["data"]["progress"]["jobs"]}
    assert rows["named"]["playlist"] == "Warmup"
    assert rows["by-hand"]["playlist"] == "pl-z", "a job queued by hand is named by its source"
    assert "playlist" not in rows["other"], "a job of another verb gains no field"


def test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two(
        cfg, default_queue):
    _intake_job(default_queue, cfg, "copy-old", tracks=("1", "2"), days=50)
    _intake_job(
        default_queue, cfg, "copy-new", tracks=("2", "1"), days=45, source="pl-b", name="Peak")
    _intake_job(default_queue, cfg, "lone", tracks=("3",), days=60, source="pl-c", name="Close")
    envelope = _ok(["job", "cancel", "--stale-days", "30", "--dry-run"])
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
        cfg, default_queue):
    _intake_job(default_queue, cfg, "copy-old", tracks=("1", "2"), days=50)
    _intake_job(default_queue, cfg, "copy-new", tracks=("1", "2"), days=45, source="pl-b")
    _intake_job(default_queue, cfg, "young", tracks=("4",), days=3, source="pl-d")
    envelope = _ok(["job", "cancel", "--stale-days", "30"])
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
        envelope = _ok(["job", "cancel", "--stale-days", "1"])
    assert envelope["outcome"] == "no_op"
    found = _stale(envelope)
    assert found["cancel"] == [] and found["kept"] == []
    assert sorted(found["left"]) == ["driven", "held"]
    assert _state(default_queue, "driven") is jobs.JobState.RUNNING
    assert _state(default_queue, "held") is jobs.JobState.QUEUED


def test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel(cfg, default_queue):
    _intake_job(default_queue, cfg, "parked", tracks=("1",), days=90)
    jobs.block(default_queue, "parked", _throttled())
    document = cfg.to_toml_dict()
    document["library"]["volume_id"] = "0000-1111"
    elsewhere = config.from_dict(document)
    _intake_job(default_queue, elsewhere, "foreign", tracks=("2",), days=90, source="pl-b")
    envelope = _ok(["job", "cancel", "--stale-days", "1"])
    assert _stale(envelope) == {"cancel": [], "kept": [], "left": ["parked"]}
    (left,) = envelope["data"]["progress"]["left"]
    assert "crate job cancel parked" in left["reason"]
    assert _state(default_queue, "foreign") is jobs.JobState.QUEUED


UUID = "0f6e2c3a-1b2d-4e5f-8a9b-0c1d2e3f4a5b"


@pytest.mark.parametrize(
    ("queued", "frees"),
    [
        (
            [dict(job_id="old", days=60), dict(job_id="new", days=2)],
            "frees nothing yet: job new still holds playlist 'Warmup' (pl-a) out of every pass",
        ),
        (
            [
                dict(job_id="old", days=40, source=UUID, swept=True),
                dict(job_id="new", days=2, source=f"https://tidal.com/playlist/{UUID}", name=None),
            ],
            f"frees nothing yet: job new still holds playlist 'Warmup' ({UUID}) out of every pass",
        ),
        (
            [dict(job_id="old", days=60, source="https://[::1", name=None)],
            "frees playlist 'https://[::1', so the next pass queues it again",
        ),
    ],
    ids=["another-open-job-holds-it", "url-typed-by-hand-holds-the-swept-id", "unparseable-url"])
def test_a_stale_cancel_says_what_it_frees(cfg, default_queue, queued, frees):
    """A typed URL holds the id it names; ``https://[::1``, which the parser raises on, is kept."""
    for number, spec in enumerate(queued):
        _intake_job(default_queue, cfg, tracks=(str(number),), **spec)
    envelope = _ok(["job", "cancel", "--stale-days", "30", "--dry-run"])
    (row,) = envelope["data"]["progress"]["cancel"]
    assert row["job_id"] == "old"
    assert row["frees"] == frees


@pytest.mark.parametrize(
    "argv",
    [
        ["job", "cancel", "--stale-days", "-1"],
        ["job", "cancel", "--stale-days", "0"],
        ["job", "cancel", "old", "--stale-days", "1"],
    ],
    ids=["negative-days", "zero-days", "job-id-beside-stale-days"])
def test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing(
        cfg, default_queue, argv):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    from cratekit import cli  # noqa: PLC0415
    code = cli.run(["--output", "json", *argv], stdout=io.StringIO(), stderr=io.StringIO())
    assert code == int(ExitCode.USAGE), argv
    assert _state(default_queue, "old") is jobs.JobState.QUEUED


def test_a_dry_run_of_one_job_cancels_nothing(cfg, default_queue):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    envelope = _ok(["job", "cancel", "old", "--dry-run"])
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["dry_run"] is True
    assert _state(default_queue, "old") is jobs.JobState.QUEUED


def test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command(cfg, default_queue):
    _intake_job(default_queue, cfg, "old", tracks=("1",), days=60)
    _ok(["job", "cancel", "--stale-days", "30"])
    shown = _ok(["job", "show", "old"])
    assert shown["data"]["state"] == "cancelled"
    assert shown["data"]["cause"]["reason"] == "cancelled"


def test_a_job_whose_queued_time_cannot_be_read_is_never_stale(cfg, default_queue):
    _intake_job(default_queue, cfg, "garbled", tracks=("1",), days=90)
    _intake_job(default_queue, cfg, "naive", tracks=("2",), days=90, source="pl-b")
    with default_queue.immediate() as conn:
        conn.execute("UPDATE jobs SET created = 'yesterday' WHERE job_id = 'garbled'")
        conn.execute("UPDATE jobs SET created = '2026-01-01T00:00:00' WHERE job_id = 'naive'")
    envelope = _ok(["job", "cancel", "--stale-days", "1"])
    found = _stale(envelope)
    assert found["cancel"] == [] and sorted(found["left"]) == ["garbled", "naive"]
    assert all("age is unknown" in row["reason"] for row in envelope["data"]["progress"]["left"])
    assert envelope["data"]["state"] == "unchanged"
    assert _state(default_queue, "garbled") is jobs.JobState.QUEUED


def test_two_jobs_with_no_item_are_nobodys_copies(cfg, default_queue):
    _intake_job(default_queue, cfg, "empty-a", tracks=(), days=60)
    _intake_job(default_queue, cfg, "empty-b", tracks=(), days=50, source="pl-b")
    envelope = _ok(["job", "cancel", "--stale-days", "30", "--dry-run"])
    assert _stale(envelope) == {"cancel": ["empty-b", "empty-a"], "kept": [], "left": []}
    assert all(row["same_tracks"] == [] for row in envelope["data"]["progress"]["cancel"])


@pytest.mark.parametrize(
    ("spec", "frees"),
    [
        (
            dict(job_id="set", source="/mixes/a set.txt", handler_key="intake.set"),
            "frees no account playlist: a set job holds none out of a pass",
        ),
        (
            dict(job_id="hearts", source="favorites"),
            "frees the account's hearts, so the next pass queues it again",
        ),
    ],
    ids=["set-job", "hearts-job"])
def test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees(
        cfg, default_queue, spec, frees):
    """A set job frees no playlist and names no file as one; a hearts job frees the hearts."""
    _intake_job(default_queue, cfg, tracks=("1",), days=60, name=None, **spec)
    envelope = _ok(["job", "cancel", "--stale-days", "30", "--dry-run"])
    (row,) = envelope["data"]["progress"]["cancel"]
    assert row["frees"] == frees
    shown = _ok(["job", "show", spec["job_id"]])
    assert shown["data"]["progress"]["playlist"] == ""
    assert shown["data"]["progress"]["source"] == spec["source"]


def test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left(cfg, default_queue):
    """The listing's own lock check, which the cancel's recheck would otherwise hide."""
    _intake_job(default_queue, cfg, "held", tracks=("1",), days=90)
    with jobs.driver_lock("held"):
        envelope = _ok(["job", "cancel", "--stale-days", "1", "--dry-run"])
    assert _stale(envelope) == {"cancel": [], "kept": [], "left": ["held"]}
    (row,) = envelope["data"]["progress"]["left"]
    assert "a live driver holds it" in row["reason"]


def test_the_job_verbs_read_a_playlist_as_the_sweep_records_it(cfg, default_queue):
    """``playlist_identity`` must agree with ``recorded_as``; the hearts are the one difference."""
    from cratekit.cli import jobs as jobs_cli  # noqa: PLC0415
    from cratekit.sync import playlists  # noqa: PLC0415
    assert jobs_cli.INTAKE_SWEEP_ID == playlists.SOURCE_ID
    references = (
        (UUID, True), (UUID.upper(), True), ("pl-a", True), (UUID, False), (UUID.upper(), False),
        (f"https://tidal.com/playlist/{UUID}", False),
        (f"https://listen.tidal.com/playlist/{UUID}?u=share", False),
        ("pl-a", False), ("https://example.com/playlist/x", False),
    )
    for number, (source, swept) in enumerate(references):
        job = _intake_job(
            default_queue, cfg, f"j{number}", tracks=(str(number),), days=1, source=source,
            swept=swept)
        assert jobs_cli.playlist_identity(job, source) == playlists.recorded_as(job), source


def test_releasing_one_drivers_claims_leaves_another_drivers_claim(store, cfg):
    """U301. A named driver frees only what it claimed."""
    job = _job(store, cfg, "a", "b")
    jobs.claim(store, job.job_id, "first")
    jobs.claim(store, job.job_id, "second")
    assert jobs.release_claims(store, job.job_id, driver="first") == 1
    held = {item.item_id: (item.state, item.claimed_by) for item in jobs.items(store, job.job_id)}
    assert held == {"a": (PENDING, None), "b": (jobs.ItemState.CLAIMED, "second")}
