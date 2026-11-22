"""The job engine's drive loop: one driver runs a job's items to an end (KTD8).

Split from ``core.jobs`` to keep each module readable; every name here is
imported back into ``core.jobs`` and used from there. Only ``core.jobs``
imports this module, at its foot, so the engine's names it reads are bound
when it loads. ``get`` and ``complete_item`` are read through ``core.jobs``,
so a test that patches them on the engine reaches the loop.
"""

from __future__ import annotations

import json
import os
import signal
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Sequence

from cratekit.core import config
from cratekit.core import jobs as _jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.jobs import (
    PERMANENT_REASONS,
    Item,
    ItemState,
    Job,
    JobState,
    JobStore,
    Produced,
    _permanent_reasons_of,
    _touch,
    block,
    cancel,
    claim,
    claim_batch,
    commit_artifact,
    drift,
    driver_lock,
    evidence_or_raise,
    fail_item,
    release_claims,
    transition,
)

# ---------------------------------------------------------------------------
# Interruption
# ---------------------------------------------------------------------------


@dataclass
class Interrupt:
    """A signal that arrived, held until the driver reaches a safe point.

    The handler does NOTHING except record. That is what makes "mid-write
    interruption aborts before commit, never during" true rather than hoped for:
    the loop decides where an interruption may take effect, and the durable rename
    is deliberately not one of those places.
    """

    signalled: bool = False
    signal_number: int | None = None
    stage: str | None = None

    def note(self, number: int) -> None:
        self.signalled = True
        self.signal_number = number


@contextmanager
def interruptible(*, stage: str | None = None) -> Iterator[Interrupt]:
    """Record SIGINT and SIGTERM instead of dying on them.

    Whatever was installed before is restored, so a caller that drives two jobs in
    one process does not leave the first one's handler behind. Handlers can only
    be installed on the main thread, so a worker thread degrades to no handling
    rather than raising: an engine unusable from a thread would be a worse defect
    than an uninterruptible one.
    """
    state = Interrupt(stage=stage)
    installed: list[tuple[int, Any]] = []

    def handler(number, frame) -> None:
        state.note(number)

    for number in (signal.SIGINT, signal.SIGTERM):
        try:
            installed.append((number, signal.signal(number, handler)))
        except (ValueError, OSError):  # pragma: no cover - non-main thread
            pass
    try:
        yield state
    finally:
        for number, previous in installed:
            try:
                signal.signal(number, previous)
            except (ValueError, OSError):  # pragma: no cover - non-main thread
                pass


# ---------------------------------------------------------------------------
# Driving
# ---------------------------------------------------------------------------

#: What one item's work looks like. It returns what it produced, and the engine
#: owns making that durable, because the flush-then-rename ordering is the one
#: thing a handler must not be able to get wrong.
Handler = Callable[[Job, Item], "Produced | None"]

#: What a handler that takes several items at once looks like (U270). It
#: receives the job, the items claimed for it in claim order, and a callable
#: that answers whether a signal arrived meanwhile, and it answers one outcome
#: per item id: what that item produced (or None), or the exception that item
#: met. The engine settles each outcome exactly as it settles one item's.
BatchHandler = Callable[
    [Job, "tuple[Item, ...]", Callable[[], bool]],
    "Mapping[str, Produced | Exception | None]",
]


@dataclass(frozen=True, slots=True)
class Batching:
    """A handler that takes up to ``size`` of a job's items in one call (U270).

    WHY THE ENGINE AND NOT THE WORKER. A worker that wrote the items after its
    own ahead of their claim would write for items the queue still calls
    pending, which a cancel between the two leaves written and unclaimed, and
    each later item would report as already done what its own run wrote. The
    driver claims the batch, so every item a write was made for is one the
    queue holds as claimed, and each is settled by its own outcome.
    """

    handle: BatchHandler
    size: int


@dataclass
class DriveResult:
    """What one drive pass did, for the caller that has to report it."""

    job: Job
    processed: int = 0
    failed: int = 0
    #: Items a handler DECLINED (U169): settled as skipped with their cause,
    #: neither done nor failed. See :class:`Declined`.
    declined: int = 0
    interrupted: bool = False
    drifted: tuple[str, ...] = field(default_factory=tuple)
    #: Warnings for the verb's report from what a worker held for the drive
    #: (U274): a provider session refreshed and not stored, say.
    warnings: tuple[dict[str, str], ...] = field(default_factory=tuple)


def _failure_verdict(
    failed: Sequence[Cause],
) -> tuple[str, bool, Remediation, tuple[str, ...]]:
    """Reason, retryable, remediation and the permanent reasons for a failed job.

    The item rows already carry the honest causes. The job cause a person is
    told to act on has to read them: a wrapper that always says the failure is
    transient tells someone to resume work that cannot succeed (R-380).

    When every failure is permanent and the items share one reason, that reason
    is the job's. When they do not, the job's reason is the reserved
    ``mixed-permanent-failures`` and the caller names every distinct reason,
    because taking the last item's reason, which this did, made every other
    reason invisible outside the item rows (R-391). The set is SORTED so the
    verdict depends on which reasons occurred and not on the order the driver
    claimed the items. The tuple is returned beside the slug so the caller names
    the same set the slug was chosen from, rather than deriving it a second time.
    """
    if not failed or any(cause.retryable for cause in failed):
        return (
            "unavailable-transient",
            True,
            Remediation(remedy=Remedy.RESUME_JOB),
            (),
        )
    reasons = tuple(sorted({cause.reason for cause in failed}))
    reason = reasons[0] if len(reasons) == 1 else "mixed-permanent-failures"
    return (
        reason,
        False,
        Remediation(
            steps=(
                "the failed items cannot succeed on resume; inspect each item's cause",
            )
        ),
        reasons,
    )


def _partial_failure_cause(
    job_id: str,
    result: DriveResult,
    inner: Cause | None,
    failed: Sequence[Cause],
) -> Cause:
    reason, retryable, remediation, reasons = _failure_verdict(failed)
    transient = sum(1 for cause in failed if cause.retryable)
    permanent = sum(1 for cause in failed if not cause.retryable)
    message = (
        f"job {job_id} finished {result.processed} items and failed "
        f"{result.failed}; the failures keep the job from succeeding and the "
        f"successes are already durable"
    )
    detail: dict[str, Any] = {
        "job_id": job_id,
        "processed": result.processed,
        "failed": result.failed,
        "retryable_failed": transient,
        "permanent_failed": permanent,
    }
    if result.declined:
        # U169. Said beside the failures rather than counted among them, so a
        # reader of a failed job still learns that some tracks were settled.
        message += f"; {result.declined} more were declined and skipped"
        detail["declined"] = result.declined
    if not retryable:
        message += "; every failure is permanent so resuming this job cannot succeed"
        if len(reasons) > 1:
            # R-391. The reason slug says the failures are mixed; the message and
            # the detail say WHICH, since the slug alone would hide them exactly
            # as the last item's reason did.
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
            detail[PERMANENT_REASONS] = reasons
    elif transient and permanent:
        message += f" ({transient} retryable, {permanent} permanent)"
    return Cause(
        reason=reason,
        message=message,
        remediation=remediation,
        scope=Scope.SOURCE,
        retryable=retryable,
        origin=("jobs",),
        detail=detail,
        inner=inner,
    )


def _parked_cause(cause: Cause, job_id: str) -> Cause:
    """A park's cause as the job records it, naming the job it parked (U193).

    The job id is added to the detail when the cause does not carry one, so a
    refusal that tells a person how to continue, the call ceiling's above all,
    can name the job to resume rather than a placeholder. A detail that already
    names a job keeps its own.
    """
    cause = cause.at("jobs.drive")
    if "job_id" in (cause.detail or {}):
        return cause
    return replace(cause, detail={**dict(cause.detail or {}), "job_id": job_id})


class Parked(CratekitError):
    """A handler's answer that the RUN must stop, not that the item failed.

    Raised by a per item worker when the provider refused the CLIENT rather than
    the track: a forbidden response, a bot wall, a wait so long it is a refusal.
    The acquisition layer returns that as a structured cause because it sits
    below the engine and may not park itself (KTD23), and this is the seam the
    engine parks ON.

    WHY A TYPE AND NOT A FIELD ON THE CAUSE. ``refuse`` defaults every cause to
    ``Scope.RUN``, so nearly every item refusal in the package already condemns
    the run by declaration, and keying the park on scope would park a master job
    over ``output-exists``. Keying it on ``retryable`` would park on a lossless
    refusal. A handler that wants the job parked says so with a raise nobody
    else makes by accident, which also keeps the act greppable.

    THE ITEM IS RELEASED, NOT FAILED. A block is a fact about the client and not
    about the track in flight, so the track goes back to pending and the next
    resume, which is a person's deliberate act after checking their account,
    redoes it. Failing it would strand it: ``retry`` re-arms failed items only
    for a TERMINAL job, and a blocked job is open.
    """

    def __init__(self, cause: Cause) -> None:
        super().__init__(cause)


class Declined(CratekitError):
    """A handler's answer that the item is SETTLED without being done (U169).

    Raised by a per item worker when the answer about this item is permanent
    and expected: the policy the job was frozen under refuses the track, which
    no resume can change. The item is recorded ``skipped`` with the cause, a
    skipped item counts as settled, and a job whose only unfinished items were
    declined SUCCEEDS. Sitting 47 is why: a download of 117 tracks landed 116,
    the last one existed only lossy, and the run reported ``failed`` over a
    list that had done exactly what the policy asked of it.

    A TYPE, FOR THE REASON :class:`Parked` IS ONE. Keying a skip on a field of
    the cause would decline every refusal that happens to carry it, and each
    worker decides for itself which of its answers are expected; the engine
    only records what it is told, with a raise nobody makes by accident.

    A RETRYABLE CAUSE IS REFUSED HERE, at construction. A skip is never re-armed
    by ``retry``, so declining a transient failure would strand a track a second
    attempt could have landed, and would report the run clean over it. The
    refusal is a ``ValueError`` rather than a cause, so inside a drive it lands
    on the item boundary as an internal failure, never as a silent skip.
    """

    def __init__(self, cause: Cause) -> None:
        if cause.retryable:
            raise ValueError(
                f"a retryable cause ({cause.reason}) cannot decline an item: a "
                f"skipped item is never retried, so it would strand work a "
                f"second attempt could finish"
            )
        super().__init__(cause)


def decline_item(store: JobStore, job_id: str, item_id: str, cause: Cause) -> None:
    """Settle one item as SKIPPED, keeping the cause that says why (U169)."""
    with store.immediate() as conn:
        conn.execute(
            "UPDATE job_items SET state = ?, cause = ?, claimed_by = NULL "
            "WHERE job_id = ? AND item_id = ?",
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
        )


def _internal_item_cause(item: Item, exc: Exception) -> Cause:
    return Cause(
        reason="internal-error",
        message=f"{type(exc).__name__}: {exc}",
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        scope=Scope.ITEM,
        origin=("jobs.drive",),
        detail={"item_id": item.item_id},
    )


def _no_outcome(item: Item) -> Exception:
    return LookupError(
        f"the batch handler answered no outcome for the item {item.item_id!r} it was given"
    )


def _batch_outcomes(
    batch: Batching, job: Job, claimed: tuple[Item, ...], stop: Callable[[], bool]
) -> dict[str, Produced | Exception | None]:
    """One outcome per claimed item, whatever the batch handler did (U270).

    A RAISE IS EVERY ITEM'S OUTCOME, the per item boundary applied to the one
    call that did them all. An answer that is not a mapping, or that leaves an
    item out, is the handler's defect, and the item it left out is failed as
    one rather than read as done: a missing answer is not evidence of work.
    """
    try:
        answered = batch.handle(job, claimed, stop)
    except Exception as exc:  # noqa: BLE001 - the item boundary converts
        return {item.item_id: exc for item in claimed}
    if not isinstance(answered, Mapping):
        wrong = TypeError(
            f"the batch handler answered {type(answered).__name__}, not one outcome per item"
        )
        return {item.item_id: wrong for item in claimed}
    outcomes: dict[str, Produced | Exception | None] = {}
    for item in claimed:
        if item.item_id not in answered:
            outcomes[item.item_id] = _no_outcome(item)
            continue
        outcome = answered[item.item_id]
        if outcome is not None and not isinstance(outcome, (Produced, Exception)):
            outcome = TypeError(
                f"the batch handler answered {type(outcome).__name__} for the item "
                f"{item.item_id!r}, which is neither what it produced nor what it met"
            )
        outcomes[item.item_id] = outcome
    return outcomes


def drive(
    store: JobStore,
    job_id: str,
    handle: Handler,
    *,
    root: Path | None = None,
    stage: str = "items",
    current_config: config.Config | None = None,
    batch: Batching | None = None,
) -> DriveResult:
    """Run a job's items to completion under one driver, resumably.

    ``batch`` HANDS THE ITEMS OVER SEVERAL AT A TIME (U270), up to its size in
    claim order, and ``handle`` is then not called. Each item is still settled
    by its own outcome, so the resume guarantee is the per item one: what was
    done stays done and what was claimed is redone. Three rules are the batch's
    own. A raise out of the batch handler is every item's outcome. A
    :class:`Parked` among the outcomes releases the WHOLE batch and blocks the
    job, since a batch is one call and the call is what the park stops. A
    batch answered while a signal is outstanding is released whole and nothing
    of it is committed, the per item checkpoint widened to the batch; the
    handler is given that signal, to stop early.

    The loop's shape IS the unit's contract, so each step says which property it
    provides:

    * the driver lock is taken FIRST, so a second driver refuses before it has
      touched a row;
    * orphaned claims are released once, so a killed run's single unfinished item,
      or its unfinished batch under ``batch``, is redone and nothing else is;
    * the interrupt flag is checked BETWEEN items and BEFORE a commit, never
      inside one;
    * an item's artifact is made durable before its row flips to done;
    * a total failure records the job as failed and then raises, rather than
      returning an empty success.

    ``handle`` receives the job and the item and returns what it produced. It runs
    against ``frozen_config(job)``, which it reads off the job rather than loading
    fresh, because reloading is precisely the resume bug KTD9 closes.
    """
    with driver_lock(job_id, root=root) as lock:
        job = _jobs.get(store, job_id)
        if not job.is_open():
            raise refuse(
                "internal-error",
                f"job {job_id} is {job.state} and a terminal state is not re-driven",
                remedy=Remedy.REPORT_DEFECT,
                origin=("jobs",),
                detail={"job_id": job_id, "state": str(job.state)},
            )
        drifted = drift(job, current_config) if current_config is not None else ()
        # Anything still claimed belongs to a driver that is gone, because this
        # process now holds the only lock that permits claiming.
        release_claims(store, job_id)
        with store.immediate() as conn:
            _touch(conn, job_id, attempts=job.attempts + 1, pid=os.getpid())
        job = transition(store, job_id, JobState.RUNNING, stage=stage)

        driver = f"{os.getpid()}@{lock.name}"
        result = DriveResult(job=job, drifted=drifted)
        last_cause: Cause | None = None
        failed_causes: list[Cause] = []

        def commit(item: Item, produced: Produced | None) -> None:
            artifact: Path | None = None
            if produced is not None and produced.staged is not None:
                if produced.final is None:
                    raise refuse(
                        "internal-error",
                        "an item produced a staged file with nowhere to put it",
                        remedy=Remedy.REPORT_DEFECT,
                        origin=("jobs",),
                        detail={"job_id": job_id, "item_id": item.item_id},
                    )
                artifact = commit_artifact(produced.staged, produced.final)
            _jobs.complete_item(store, job_id, item.item_id, artifact=artifact)
            result.processed += 1

        def failed(item: Item, cause: Cause) -> None:
            nonlocal last_cause
            last_cause = cause
            fail_item(store, job_id, item.item_id, cause)
            result.failed += 1
            failed_causes.append(cause)

        with interruptible(stage=stage) as interrupt:
            while batch is not None:
                if interrupt.signalled:
                    result.interrupted = True
                    break
                claimed = claim_batch(store, job_id, driver, batch.size)
                if not claimed:
                    break
                outcomes = _batch_outcomes(
                    batch, job, claimed, lambda: interrupt.signalled
                )
                parked = next(
                    (one for one in outcomes.values() if isinstance(one, Parked)), None
                )
                if parked is not None:
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, _parked_cause(parked.cause, job_id))
                    return result
                if interrupt.signalled:
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break
                for item in claimed:
                    outcome = outcomes[item.item_id]
                    if isinstance(outcome, Declined):
                        decline_item(
                            store, job_id, item.item_id, outcome.cause.at("jobs.drive")
                        )
                        result.declined += 1
                    elif isinstance(outcome, CratekitError):
                        failed(item, outcome.cause.at("jobs.drive"))
                    elif isinstance(outcome, Exception):
                        failed(item, _internal_item_cause(item, outcome))
                    else:
                        commit(item, outcome)
            while batch is None:
                if interrupt.signalled:
                    result.interrupted = True
                    break
                item = claim(store, job_id, driver)
                if item is None:
                    break
                try:
                    produced = handle(job, item)
                except Parked as exc:
                    # BEFORE the item boundary below, which would fail the item
                    # and claim the next one. The next claim is the second
                    # request into a block, which is the one thing the pacing
                    # layer exists to never make. The item goes back to pending
                    # and the job records why it stopped.
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, _parked_cause(exc.cause, job_id))
                    return result
                except Declined as exc:
                    # SETTLED, NOT FAILED (U169). Kept apart from the failure
                    # list, so neither the job's verdict nor its retryable
                    # flag reads a refusal the worker called expected.
                    decline_item(store, job_id, item.item_id, exc.cause.at("jobs.drive"))
                    result.declined += 1
                    continue
                except CratekitError as exc:
                    last_cause = exc.cause.at("jobs.drive")
                    fail_item(store, job_id, item.item_id, last_cause)
                    result.failed += 1
                    failed_causes.append(last_cause)
                    continue
                except Exception as exc:  # noqa: BLE001 - the item boundary converts
                    last_cause = _internal_item_cause(item, exc)
                    fail_item(store, job_id, item.item_id, last_cause)
                    result.failed += 1
                    failed_causes.append(last_cause)
                    continue

                if interrupt.signalled:
                    # The checkpoint that makes the guarantee real. The item is
                    # RELEASED rather than committed, so a resume redoes it whole
                    # instead of inheriting a half-written artifact, and the
                    # commit below is never entered with a signal outstanding.
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break

                commit(item, produced)

        if result.interrupted:
            result.job = cancel(store, job_id, stage=stage)
            return result

        attempted = result.processed + result.failed
        items_retryable = any(cause.retryable for cause in failed_causes)
        if attempted and not result.processed:
            # Recorded BEFORE raising. A raise that leaves the row saying running
            # is the unpersisted-decision half of the same incident: whatever
            # restarts next would have to guess what happened here.
            result.job = transition(
                store,
                job_id,
                JobState.FAILED,
                stage=stage,
                cause=_partial_failure_cause(
                    job_id, result, last_cause, failed_causes
                ),
            )
            # The last item stays nested, and the reasons the recorded verdict
            # named ride on the envelope's own detail (R-391), so the foreground
            # is not left with only the item the driver claimed last.
            evidence_or_raise(
                attempted=attempted,
                succeeded=0,
                failed_cause=last_cause,
                retryable=items_retryable,
                permanent_reasons=_permanent_reasons_of(result.job.cause).get(
                    PERMANENT_REASONS, ()
                )
                if result.job.cause is not None
                else (),
            )
        if result.failed:
            result.job = transition(
                store,
                job_id,
                JobState.FAILED,
                stage=stage,
                cause=_partial_failure_cause(
                    job_id, result, last_cause, failed_causes
                ),
            )
        else:
            result.job = transition(store, job_id, JobState.SUCCEEDED, stage=stage)
        return result
