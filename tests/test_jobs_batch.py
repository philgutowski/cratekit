"""U270: the job engine hands a batch handler several items at once and settles each by its
own outcome: a raise is every item's, a park or a signal releases the batch whole, and an
item given no outcome is failed.
"""

from __future__ import annotations

import os
import signal

import pytest

from cratekit.core import jobs
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from tests.test_jobs import _blocked, _job, _states
from tests.test_jobs import _queue_template as _queue_template  # noqa: PLC0414
from tests.test_jobs import cfg as cfg  # noqa: PLC0414
from tests.test_jobs import queue as queue  # noqa: PLC0414
from tests.test_jobs import store as store  # noqa: PLC0414

CLAIMED, DONE, FAILED = jobs.ItemState.CLAIMED, jobs.ItemState.DONE, jobs.ItemState.FAILED
PENDING, SKIPPED = jobs.ItemState.PENDING, jobs.ItemState.SKIPPED


def _never(_job, _item):
    raise AssertionError("the per item handler is not called when a batch is given")


def _transient(message: str = "the provider dropped the connection") -> CratekitError:
    said = {"remedy": Remedy.RETRY_LATER, "retryable": True, "origin": ("test",)}
    return refuse("unavailable-transient", message, **said)


def _all_done(seen: list[tuple[str, ...]], *, raise_on=(), error=None):
    """A handler recording each batch, raising ``error()`` over an item in ``raise_on``."""
    def handle(_job, items, _stop):
        ids = tuple(item.item_id for item in items)
        seen.append(ids)
        if set(raise_on) & set(ids):
            raise error()
        return dict.fromkeys(ids)
    return handle


def _drive(queue, job, handle, size: int) -> jobs.DriveResult:
    store, root = queue
    return jobs.drive(store, job.job_id, _never, root=root, batch=jobs.Batching(handle, size))


def _held(store, job_id: str) -> dict:
    return {item.item_id: item for item in jobs.items(store, job_id)}


# Claiming
def test_a_batch_is_claimed_in_ordinal_order_up_to_its_size(queue, store, cfg):
    job = _job(store, cfg, "a", "b", "c", "d", "e")
    seen: list[tuple[str, ...]] = []
    result = _drive(queue, job, _all_done(seen), 2)
    assert seen == [("a", "b"), ("c", "d"), ("e",)]
    assert result.processed == 5
    assert result.job.state is jobs.JobState.SUCCEEDED
    assert set(_states(store, job.job_id).values()) == {jobs.ItemState.DONE}


def test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs(queue, store, cfg):
    """So a cancel or a second driver sees every item a write may be made for as claimed."""
    job = _job(store, cfg, "a", "b", "c")
    during: list[dict[str, jobs.ItemState]] = []

    def handle(_job, items, _stop):
        during.append(_states(store, job.job_id))
        return {item.item_id: None for item in items}
    _drive(queue, job, handle, 2)
    assert during[0] == {"a": CLAIMED, "b": CLAIMED, "c": PENDING}
    assert during[1]["c"] is jobs.ItemState.CLAIMED


def test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left(queue, store, cfg):
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
def test_claim_batch_refuses_a_batch_of_no_items(queue, store, cfg, limit):
    job = _job(store, cfg, "a")
    with pytest.raises(CratekitError) as refused:
        jobs.claim_batch(store, job.job_id, "one", limit)
    assert refused.value.cause.reason == "internal-error"
    assert _states(store, job.job_id) == {"a": jobs.ItemState.PENDING}


# Each item settled by its own outcome
def test_each_outcome_settles_its_own_item(queue, store, cfg):
    job = _job(store, cfg, "done", "failed", "defect", "declined")

    def handle(_job, items, _stop):
        defect, declined = RuntimeError("a worker defect"), jobs.Declined(_blocked())
        return {"done": None, "failed": _transient(), "defect": defect, "declined": declined}
    result = _drive(queue, job, handle, 4)
    held = _held(store, job.job_id)
    assert {key: item.state for key, item in held.items()} == {
        "done": DONE, "failed": FAILED, "defect": FAILED, "declined": SKIPPED
    }
    assert held["failed"].cause.reason == "unavailable-transient"
    assert held["failed"].cause.retryable
    assert held["defect"].cause.reason == "internal-error"
    assert "a worker defect" in held["defect"].cause.message
    assert (result.processed, result.failed, result.declined) == (1, 2, 1)
    assert result.job.state is jobs.JobState.FAILED


def test_a_produced_artifact_is_committed_before_its_item_is_done(queue, store, cfg, tmp_path):
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        made = {}
        for item in items:
            staged = tmp_path / f"{item.item_id}.staged"
            staged.write_text(item.item_id)
            made[item.item_id] = jobs.Produced(staged=staged, final=tmp_path / "out" / item.item_id)
        return made
    _drive(queue, job, handle, 2)
    held = _held(store, job.job_id)
    for key in ("a", "b"):
        assert held[key].state is jobs.ItemState.DONE
        assert (tmp_path / "out" / key).read_text() == key
        assert held[key].artifact == str(tmp_path / "out" / key)


def test_a_raise_out_of_the_batch_handler_is_every_items_outcome(queue, store, cfg):
    """The per item boundary applied to the one call that did them all."""
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []
    result = _drive(queue, job, _all_done(calls, raise_on={"a"}, error=_transient), 2)
    assert calls == [("a", "b"), ("c",)]
    assert _states(store, job.job_id) == {"a": FAILED, "b": FAILED, "c": DONE}
    assert result.failed == 2
    assert result.job.state is jobs.JobState.FAILED


def test_a_batch_that_fails_every_item_records_the_job_failed_then_raises(queue, store, cfg):
    """No evidence is still no evidence when the items came in a batch."""
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        raise _transient()
    with pytest.raises(CratekitError):
        _drive(queue, job, handle, 5)
    assert jobs.get(store, job.job_id).state is jobs.JobState.FAILED
    assert set(_states(store, job.job_id).values()) == {jobs.ItemState.FAILED}


@pytest.mark.parametrize(
    ("answer", "message"),
    [({"a": None}, "no outcome"), ({"a": None, "b": "written"}, "neither what it produced")],
    ids=["no-answer", "neither-produced-nor-an-exception"])
def test_an_item_without_a_usable_outcome_is_failed_not_done(queue, store, cfg, answer, message):
    """A missing answer is not evidence of work, nor is an answer of the wrong type."""
    job = _job(store, cfg, "a", "b")
    result = _drive(queue, job, lambda _job, _items, _stop: answer, 2)
    held = _held(store, job.job_id)
    assert held["a"].state is jobs.ItemState.DONE
    assert held["b"].state is jobs.ItemState.FAILED
    assert held["b"].cause.reason == "internal-error"
    assert message in held["b"].cause.message
    assert result.job.state is jobs.JobState.FAILED


@pytest.mark.parametrize(
    "answer", [[None, None], ("a", "b"), "done"], ids=["list", "tuple", "text"])
def test_an_answer_that_is_not_one_outcome_per_item_fails_every_item(queue, store, cfg, answer):
    job = _job(store, cfg, "a", "b")
    with pytest.raises(CratekitError):
        _drive(queue, job, lambda _job, _items, _stop: answer, 2)
    held = jobs.items(store, job.job_id)
    assert {item.state for item in held} == {jobs.ItemState.FAILED}
    assert {item.cause.reason for item in held} == {"internal-error"}


# A park and a signal stop the run, and release the batch whole
def test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job(queue, store, cfg):
    job = _job(store, cfg, "a", "b", "c", "d")
    calls: list[tuple[str, ...]] = []
    handle = _all_done(calls, raise_on={"c"}, error=lambda: jobs.Parked(_blocked()))
    result = _drive(queue, job, handle, 2)
    assert calls == [("a", "b"), ("c", "d")]
    assert _states(store, job.job_id) == {"a": DONE, "b": DONE, "c": PENDING, "d": PENDING}
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause.reason == "provider-blocked"


def test_a_park_answered_for_one_item_releases_the_whole_batch(queue, store, cfg):
    """Nothing of a parked batch is committed, the item answered done included."""
    job = _job(store, cfg, "a", "b")

    def handle(_job, items, _stop):
        return {"a": None, "b": jobs.Parked(_blocked())}
    result = _drive(queue, job, handle, 2)
    assert _states(store, job.job_id) == {"a": jobs.ItemState.PENDING, "b": jobs.ItemState.PENDING}
    assert result.processed == 0
    assert result.job.state is jobs.JobState.BLOCKED


def test_a_parked_batch_is_driven_again_from_its_first_item(queue, store, cfg):
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []
    park = {"b"}
    handle = _all_done(calls, raise_on=park, error=lambda: jobs.Parked(_blocked()))
    _drive(queue, job, handle, 2)
    park.clear()
    result = _drive(queue, job, handle, 2)
    assert calls == [("a", "b"), ("a", "b"), ("c",)]
    assert result.job.state is jobs.JobState.SUCCEEDED


def test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled(queue, store, cfg):
    """A resume redoes the batch whole, and the handler saw the signal."""
    job = _job(store, cfg, "a", "b", "c", "d")
    asked: list[bool] = []
    calls: list[tuple[str, ...]] = []

    def handle(_job, items, stop):
        calls.append(tuple(item.item_id for item in items))
        asked.append(stop())
        os.kill(os.getpid(), signal.SIGINT)
        asked.append(stop())
        return {item.item_id: None for item in items}
    result = _drive(queue, job, handle, 2)
    assert calls == [("a", "b")]
    assert asked == [False, True]
    assert result.interrupted
    assert result.processed == 0
    assert _states(store, job.job_id) == dict.fromkeys("abcd", jobs.ItemState.PENDING)
    assert result.job.state is jobs.JobState.CANCELLED


def test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other(queue, store, cfg, monkeypatch):
    job = _job(store, cfg, "a", "b", "c")
    calls: list[tuple[str, ...]] = []
    real = jobs.complete_item

    def complete_then_signal(store_, job_id, item_id, **kwargs):
        real(store_, job_id, item_id, **kwargs)
        if item_id == "b":
            os.kill(os.getpid(), signal.SIGINT)
    monkeypatch.setattr(jobs, "complete_item", complete_then_signal)
    result = _drive(queue, job, _all_done(calls), 2)
    assert calls == [("a", "b")]
    assert _states(store, job.job_id) == {"a": DONE, "b": DONE, "c": PENDING}
    assert result.interrupted


def test_the_per_item_handler_runs_when_no_batch_is_given(queue, cfg):
    """The single item path is unchanged: every handler but a batched one."""
    store, root = queue
    job = _job(store, cfg, "a", "b")
    seen: list[str] = []
    result = jobs.drive(store, job.job_id, lambda _job, item: seen.append(item.item_id), root=root)
    assert seen == ["a", "b"]
    assert result.job.state is jobs.JobState.SUCCEEDED
