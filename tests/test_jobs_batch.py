"""U270: the job engine hands a batch handler several items at once.

The export to the account sends a hundred tracks in one request, and the
items stay one per track, so the driver claims a batch of them, hands them to
the worker in one call, and settles each by its own outcome. Each test names
the property of the per item engine it keeps, or the batch rule it adds: a
raise is every item's outcome, a park releases the whole batch, a signal
releases a batch answered under it, and an item the handler gave no outcome
for is failed rather than read as done.
"""

from __future__ import annotations

import os
import signal

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy


@pytest.fixture
def cfg(tmp_path):
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
    root = tmp_path / "jobs"
    with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
        yield store, root


def _job(store, cfg, *ids: str) -> jobs.Job:
    return jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=list(ids))


def _states(store, job_id: str) -> dict[str, jobs.ItemState]:
    return {item.item_id: item.state for item in jobs.items(store, job_id)}


def _never(_job, _item):
    raise AssertionError("the per item handler is not called when a batch is given")


def _blocked() -> Cause:
    return Cause(
        reason="provider-blocked",
        message="the provider refused this client",
        remediation=Remediation(steps=("check the account",)),
        scope=Scope.RUN,
        retryable=False,
    )


def _transient(message: str = "the provider dropped the connection") -> CratekitError:
    return refuse(
        "unavailable-transient",
        message,
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("test",),
    )


def _all_done(seen: list[tuple[str, ...]]):
    def handle(_job, items, _stop):
        seen.append(tuple(item.item_id for item in items))
        return {item.item_id: None for item in items}

    return handle


# ═══════════════════════════════════════════════════════════════════════════
# Claiming
# ═══════════════════════════════════════════════════════════════════════════


def test_a_batch_is_claimed_in_ordinal_order_up_to_its_size(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "a", "b", "c", "d", "e")
    seen: list[tuple[str, ...]] = []

    result = jobs.drive(
        store, job.job_id, _never, root=root, batch=jobs.Batching(_all_done(seen), 2)
    )

    assert seen == [("a", "b"), ("c", "d"), ("e",)]
    assert result.processed == 5
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert set(_states(store, job.job_id).values()) == {jobs.ItemState.DONE}


def test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs(queue, cfg):
    """The engine's claim, not the worker's look ahead: a cancel or a second
    driver sees every item a write may be made for as claimed."""
    store, root = queue
    job = _job(store, cfg, "a", "b", "c")
    during: list[dict[str, jobs.ItemState]] = []

    def handle(_job, items, _stop):
        during.append(_states(store, job.job_id))
        return {item.item_id: None for item in items}

    jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert during[0] == {
        "a": jobs.ItemState.CLAIMED,
        "b": jobs.ItemState.CLAIMED,
        "c": jobs.ItemState.PENDING,
    }
    assert during[1]["c"] is jobs.ItemState.CLAIMED


def test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left(queue, cfg):
    store, _root = queue
    job = _job(store, cfg, "a", "b", "c")
    first = jobs.claim_batch(store, job.job_id, "one", 2)
    second = jobs.claim_batch(store, job.job_id, "two", 2)
    third = jobs.claim_batch(store, job.job_id, "three", 2)

    assert [item.item_id for item in first] == ["a", "b"]
    assert [item.item_id for item in second] == ["c"]
    assert third == ()
    assert {item.claimed_by for item in first} == {"one"}
    assert all(item.state is jobs.ItemState.CLAIMED for item in (*first, *second))


@pytest.mark.parametrize("limit", [0, -1])
def test_claim_batch_refuses_a_batch_of_no_items(queue, cfg, limit):
    store, _root = queue
    job = _job(store, cfg, "a")
    with pytest.raises(CratekitError) as refused:
        jobs.claim_batch(store, job.job_id, "one", limit)
    assert refused.value.cause.reason == "internal-error"
    assert _states(store, job.job_id) == {"a": jobs.ItemState.PENDING}


# ═══════════════════════════════════════════════════════════════════════════
# Each item settled by its own outcome
# ═══════════════════════════════════════════════════════════════════════════


def test_each_outcome_settles_its_own_item(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "done", "failed", "defect", "declined")

    def handle(_job, items, _stop):
        return {
            "done": None,
            "failed": _transient(),
            "defect": RuntimeError("a worker defect"),
            "declined": jobs.Declined(_blocked()),
        }

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 4))

    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert {key: item.state for key, item in held.items()} == {
        "done": jobs.ItemState.DONE,
        "failed": jobs.ItemState.FAILED,
        "defect": jobs.ItemState.FAILED,
        "declined": jobs.ItemState.SKIPPED,
    }
    assert held["failed"].cause.reason == "unavailable-transient"
    assert held["failed"].cause.retryable
    assert held["defect"].cause.reason == "internal-error"
    assert "a worker defect" in held["defect"].cause.message
    assert (result.processed, result.failed, result.declined) == (1, 2, 1)
    assert result.job.state is jobs.JobState.FAILED


def test_a_produced_artifact_is_committed_before_its_item_is_done(queue, cfg, tmp_path):
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        made = {}
        for item in items:
            staged = tmp_path / f"{item.item_id}.staged"
            staged.write_text(item.item_id)
            made[item.item_id] = jobs.Produced(staged=staged, final=tmp_path / "out" / item.item_id)
        return made

    jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    for key in ("a", "b"):
        assert held[key].state is jobs.ItemState.DONE
        assert (tmp_path / "out" / key).read_text() == key
        assert held[key].artifact == str(tmp_path / "out" / key)


def test_a_raise_out_of_the_batch_handler_is_every_items_outcome(queue, cfg):
    """The per item boundary applied to the one call that did them all."""
    store, root = queue
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []

    def handle(_job, items, _stop):
        calls.append(tuple(item.item_id for item in items))
        if "a" in calls[-1]:
            raise _transient()
        return {item.item_id: None for item in items}

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert calls == [("a", "b"), ("c",)]
    assert _states(store, job.job_id) == {
        "a": jobs.ItemState.FAILED,
        "b": jobs.ItemState.FAILED,
        "c": jobs.ItemState.DONE,
    }
    assert result.failed == 2
    assert result.job.state is jobs.JobState.FAILED


def test_a_batch_that_fails_every_item_records_the_job_failed_then_raises(queue, cfg):
    """No evidence is still no evidence when the items came in a batch."""
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        raise _transient()

    with pytest.raises(CratekitError):
        jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 5))

    assert jobs.get(store, job.job_id).state is jobs.JobState.FAILED
    assert set(_states(store, job.job_id).values()) == {jobs.ItemState.FAILED}


def test_an_item_the_handler_answered_nothing_for_is_failed_not_done(queue, cfg):
    """A missing answer is not evidence of work, the first defect pattern."""
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        return {"a": None}

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert held["a"].state is jobs.ItemState.DONE
    assert held["b"].state is jobs.ItemState.FAILED
    assert held["b"].cause.reason == "internal-error"
    assert "no outcome" in held["b"].cause.message
    assert result.job.state is jobs.JobState.FAILED


@pytest.mark.parametrize(
    "answer",
    [[None, None], ("a", "b"), "done"],
    ids=["list", "tuple", "text"],
)
def test_an_answer_that_is_not_one_outcome_per_item_fails_every_item(queue, cfg, answer):
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        return answer

    with pytest.raises(CratekitError):
        jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    held = jobs.items(store, job.job_id)
    assert {item.state for item in held} == {jobs.ItemState.FAILED}
    assert {item.cause.reason for item in held} == {"internal-error"}


def test_an_outcome_that_is_neither_produced_nor_an_exception_fails_its_item(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        return {"a": None, "b": "written"}

    jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    held = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert held["a"].state is jobs.ItemState.DONE
    assert held["b"].state is jobs.ItemState.FAILED
    assert held["b"].cause.reason == "internal-error"


# ═══════════════════════════════════════════════════════════════════════════
# A park and a signal stop the run, and release the batch whole
# ═══════════════════════════════════════════════════════════════════════════


def test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "a", "b", "c", "d")
    calls: list[tuple[str, ...]] = []

    def handle(_job, items, _stop):
        calls.append(tuple(item.item_id for item in items))
        if "c" in calls[-1]:
            raise jobs.Parked(_blocked())
        return {item.item_id: None for item in items}

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert calls == [("a", "b"), ("c", "d")]
    assert _states(store, job.job_id) == {
        "a": jobs.ItemState.DONE,
        "b": jobs.ItemState.DONE,
        "c": jobs.ItemState.PENDING,
        "d": jobs.ItemState.PENDING,
    }
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause.reason == "provider-blocked"


def test_a_park_answered_for_one_item_releases_the_whole_batch(queue, cfg):
    """Nothing of a parked batch is committed, the item that answered done
    included: the batch is one call and the park stops the call."""
    store, root = queue
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        return {"a": None, "b": jobs.Parked(_blocked())}

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert _states(store, job.job_id) == {
        "a": jobs.ItemState.PENDING,
        "b": jobs.ItemState.PENDING,
    }
    assert result.processed == 0
    assert result.job.state is jobs.JobState.BLOCKED


def test_a_parked_batch_is_driven_again_from_its_first_item(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []
    park = {"b"}

    def handle(_job, items, _stop):
        calls.append(tuple(item.item_id for item in items))
        if park & {item.item_id for item in items}:
            raise jobs.Parked(_blocked())
        return {item.item_id: None for item in items}

    jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))
    park.clear()
    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert calls == [("a", "b"), ("a", "b"), ("c",)]
    assert result.job.state is jobs.JobState.SUCCEEDED


def test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled(queue, cfg):
    """The per item checkpoint widened to the batch: a resume redoes it whole
    rather than inheriting part of it, and the handler saw the signal."""
    store, root = queue
    job = _job(store, cfg, "a", "b", "c", "d")
    asked: list[bool] = []
    calls: list[tuple[str, ...]] = []

    def handle(_job, items, stop):
        calls.append(tuple(item.item_id for item in items))
        asked.append(stop())
        os.kill(os.getpid(), signal.SIGINT)
        asked.append(stop())
        return {item.item_id: None for item in items}

    result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert calls == [("a", "b")]
    assert asked == [False, True]
    assert result.interrupted
    assert result.processed == 0
    assert _states(store, job.job_id) == {
        "a": jobs.ItemState.PENDING,
        "b": jobs.ItemState.PENDING,
        "c": jobs.ItemState.PENDING,
        "d": jobs.ItemState.PENDING,
    }
    assert result.job.state is jobs.JobState.CANCELLED


def test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other(queue, cfg):
    store, root = queue
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []

    def handle(_job, items, _stop):
        calls.append(tuple(item.item_id for item in items))
        return {item.item_id: None for item in items}

    real = jobs.complete_item

    def complete_then_signal(store_, job_id, item_id, **kwargs):
        real(store_, job_id, item_id, **kwargs)
        if item_id == "b":
            os.kill(os.getpid(), signal.SIGINT)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(jobs, "complete_item", complete_then_signal)
        result = jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, 2))

    assert calls == [("a", "b")]
    assert _states(store, job.job_id) == {
        "a": jobs.ItemState.DONE,
        "b": jobs.ItemState.DONE,
        "c": jobs.ItemState.PENDING,
    }
    assert result.interrupted


def test_the_per_item_handler_runs_when_no_batch_is_given(queue, cfg):
    """The single item path is unchanged: every handler but a batched one."""
    store, root = queue
    job = _job(store, cfg, "a", "b")
    seen: list[str] = []

    def handle(_job, item):
        seen.append(item.item_id)

    result = jobs.drive(store, job.job_id, handle, root=root)

    assert seen == ["a", "b"]
    assert result.job.state is jobs.JobState.SUCCEEDED
