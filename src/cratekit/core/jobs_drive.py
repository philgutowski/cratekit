"""The job engine's drive loop: one driver runs a job's items to an end (KTD8).

Every name here is imported back into ``core.jobs``, which imports this
module at its foot, so the engine's names are bound when it loads. ``get``
and ``complete_item`` are read through ``core.jobs``, so a test that patches
them on the engine reaches the loop.
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

    The handler only records, so the loop decides where an interruption takes
    effect, and the durable rename is never one of those places.
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

    The previous handlers are restored after. Off the main thread, where no
    handler can be installed, it degrades to no handling rather than raising.
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

#: One item's work: it returns what it produced, and the engine makes that durable.
Handler = Callable[[Job, Item], "Produced | None"]

#: Several items' work at once (U270): given the job, its claimed items in claim
#: order and a callable saying whether a signal arrived, it answers one outcome
#: per item id, what it produced (or None) or the exception it met.
BatchHandler = Callable[
    [Job, "tuple[Item, ...]", Callable[[], bool]],
    "Mapping[str, Produced | Exception | None]",
]


@dataclass(frozen=True, slots=True)
class Batching:
    """A handler that takes up to ``size`` of a job's items in one call (U270).

    The driver claims the batch, never the worker, so every item a write is
    made for is one the queue holds as claimed, settled by its own outcome.
    """

    handle: BatchHandler
    size: int


@dataclass
class DriveResult:
    """What one drive pass did, for the caller that has to report it."""

    job: Job
    processed: int = 0
    failed: int = 0
    #: Items a handler DECLINED (U169), settled as skipped. See :class:`Declined`.
    declined: int = 0
    interrupted: bool = False
    drifted: tuple[str, ...] = field(default_factory=tuple)
    #: Warnings for the verb's report from what a worker held for the drive (U274).
    warnings: tuple[dict[str, str], ...] = field(default_factory=tuple)


def _failure_verdict(failed: Sequence[Cause]) -> tuple[str, bool, Remediation, tuple[str, ...]]:
    """Reason, retryable, remediation and the permanent reasons for a failed job.

    Read from the item causes (R-380): transient if any failure is. When every
    failure is permanent, one shared reason is the job's, and several make it
    ``mixed-permanent-failures`` with every distinct reason returned, SORTED so
    the verdict does not depend on claim order (R-391).
    """
    if not failed or any(cause.retryable for cause in failed):
        return ("unavailable-transient", True, Remediation(remedy=Remedy.RESUME_JOB), ())
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
    job_id: str, result: DriveResult, inner: Cause | None, failed: Sequence[Cause]
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
        # U169: said beside the failures, never counted among them.
        message += f"; {result.declined} more were declined and skipped"
        detail["declined"] = result.declined
    if not retryable:
        message += "; every failure is permanent so resuming this job cannot succeed"
        if len(reasons) > 1:
            # R-391. The slug says the failures are mixed; the message and detail say WHICH.
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

    The job id is added when the detail carries none, so a refusal can name the
    job to continue; a detail that already names a job keeps its own.
    """
    cause = cause.at("jobs.drive")
    if "job_id" in (cause.detail or {}):
        return cause
    return replace(cause, detail={**dict(cause.detail or {}), "job_id": job_id})


class Parked(CratekitError):
    """A handler's answer that the RUN must stop, not that the item failed.

    Raised by a per item worker when the provider refused the CLIENT rather
    than the track (KTD23 keeps the acquisition layer from parking itself). A
    type, not a field on the cause, so nothing parks by accident: scope and
    ``retryable`` already mean other things. The item is RELEASED, not failed,
    since ``retry`` re-arms failed items only for a terminal job and a blocked
    job is open.
    """

    def __init__(self, cause: Cause) -> None:
        super().__init__(cause)


class Declined(CratekitError):
    """A handler's answer that the item is SETTLED without being done (U169).

    For a permanent, expected answer, such as the frozen policy refusing the
    track. The item is recorded ``skipped`` with the cause, which counts as
    settled, so a job whose only unfinished items were declined SUCCEEDS. A
    type for the reason :class:`Parked` is one.

    A RETRYABLE CAUSE IS REFUSED at construction, since a skip is never
    re-armed; as a ``ValueError``, so inside a drive it fails the item rather
    than skipping it silently.
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

    A RAISE IS EVERY ITEM'S OUTCOME. An answer that is not a mapping, or leaves
    an item out, is the handler's defect, and fails the items concerned: a
    missing answer is not evidence of work.
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

    The loop's shape is its contract:

    * the driver lock is taken FIRST, so a second driver refuses before it has
      touched a row;
    * orphaned claims are released once, so a killed run's one unfinished item,
      or batch, is redone and nothing else is;
    * the interrupt flag is checked BETWEEN items and BEFORE a commit, never
      inside one;
    * an item's artifact is made durable before its row flips to done;
    * a total failure records the job as failed and then raises.

    ``batch`` hands the items over up to its size at a time (U270) and
    ``handle`` is not called; each item is still settled by its own outcome. A
    :class:`Parked` among a batch's outcomes, or a signal outstanding when it
    answers, releases the WHOLE batch. ``handle`` runs against
    ``frozen_config(job)``, never a fresh load (KTD9).
    """
    with driver_lock(job_id, root=root) as lock:
        job = _jobs.get(store, job_id)
        if not job.is_open():
            raise refuse(
                "internal-error",
                f"job {job_id} is {job.state} and a terminal state is not re-driven",
                remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
                detail={"job_id": job_id, "state": str(job.state)},
            )
        drifted = drift(job, current_config) if current_config is not None else ()
        # Anything still claimed belongs to a driver that is gone: this process
        # holds the only lock that permits claiming.
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
                        remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
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
                parked = next((one for one in outcomes.values() if isinstance(one, Parked)), None)
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
                        decline_item(store, job_id, item.item_id, outcome.cause.at("jobs.drive"))
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
                    # BEFORE the item boundary, whose next claim would be a
                    # second request into a block. The item goes back to pending.
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, _parked_cause(exc.cause, job_id))
                    return result
                except Declined as exc:
                    # SETTLED, NOT FAILED (U169), and kept out of the job's verdict.
                    decline_item(store, job_id, item.item_id, exc.cause.at("jobs.drive"))
                    result.declined += 1
                    continue
                except CratekitError as exc:
                    failed(item, exc.cause.at("jobs.drive"))
                    continue
                except Exception as exc:  # noqa: BLE001 - the item boundary converts
                    failed(item, _internal_item_cause(item, exc))
                    continue

                if interrupt.signalled:
                    # The checkpoint: the item is RELEASED, never committed with
                    # a signal outstanding, so a resume redoes it whole.
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break

                commit(item, produced)

        if result.interrupted:
            result.job = cancel(store, job_id, stage=stage)
            return result

        attempted = result.processed + result.failed
        items_retryable = any(cause.retryable for cause in failed_causes)
        if not result.failed:
            result.job = transition(store, job_id, JobState.SUCCEEDED, stage=stage)
            return result
        # Recorded BEFORE a total failure raises, so the row never says running.
        result.job = transition(
            store,
            job_id,
            JobState.FAILED,
            stage=stage,
            cause=_partial_failure_cause(job_id, result, last_cause, failed_causes),
        )
        if not result.processed:
            # The last item stays nested, and the recorded verdict's reasons ride
            # on the envelope's own detail (R-391).
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
        return result
