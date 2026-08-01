"""A real out-of-process job driver, for the tests that need a process to kill.

The unit's verification is "a long job killed at three different stages resumes
correctly each time", and the only honest way to run it is with a process that
genuinely dies. A thread cannot be SIGKILLed, an in-process fake cannot leave the
driver lock behind for the kernel to release, and neither one exercises the
question the engine actually answers: what does the NEXT process believe happened.

Three modes, one per property that needs a second process:

``drive``  run the item loop, stalling forever on a named item so the parent can
           kill it at a chosen point.
``claim``  claim items as fast as possible with no driver lock, so two of these
           racing prove the claim transaction is what serializes them.
``hold``   take the driver lock and wait, so the parent can test that a live
           holder is never evicted and a dead one's lock is reclaimed.

Not a test module: pytest does not collect it, and it is invoked only as a script.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from cratekit.core import jobs

#: Long enough that the parent always wins the race and kills it first, short
#: enough that a bug in the parent fails the suite instead of hanging it.
STALL_SECONDS = 120


def _append(ledger: Path, line: str) -> None:
    """Record an ATTEMPT, flushed immediately.

    Flushed because the process is about to be killed: an attempt recorded in a
    buffer that never reached the disk would make a reprocessed item look like it
    was never touched, which is the exact thing the test is counting.
    """
    with open(ledger, "a") as handle:
        handle.write(line + "\n")
        handle.flush()


def run_drive(db: Path, job_id: str, root: Path, ledger: Path, stall: str) -> int:
    def handle(job, item):
        _append(ledger, item.item_id)
        if item.item_id == stall:
            (root / f"stalled-{item.item_id}").write_text("here")
            time.sleep(STALL_SECONDS)
        staged = root / f"staged-{item.item_id}"
        staged.write_text(item.item_id)
        return jobs.Produced(staged=staged, final=root / "out" / f"{item.item_id}.txt")

    with jobs.open_store(db) as store:
        jobs.drive(store, job_id, handle, root=root)
    return 0


def run_claim(db: Path, job_id: str, ledger: Path, barrier: Path) -> int:
    """Claim until the queue is empty, starting only once the barrier appears.

    The barrier and the per-item pause exist so both processes are genuinely in
    the loop at the same time. Without them the first worker to start drains the
    whole queue before the second is done importing, and the test would pass while
    proving nothing about two writers at once.
    """
    while not barrier.exists():
        time.sleep(0.01)
    with jobs.open_store(db) as store:
        driver = f"claimer-{ledger.name}"
        while True:
            item = jobs.claim(store, job_id, driver)
            if item is None:
                return 0
            _append(ledger, item.item_id)
            jobs.complete_item(store, job_id, item.item_id)
            time.sleep(0.002)


def run_hold(job_id: str, root: Path) -> int:
    with jobs.driver_lock(job_id, root=root):
        (root / f"holding-{job_id}").write_text("here")
        time.sleep(STALL_SECONDS)
    return 0


def main(argv: list[str]) -> int:
    mode = argv[0]
    if mode == "drive":
        return run_drive(Path(argv[1]), argv[2], Path(argv[3]), Path(argv[4]), argv[5])
    if mode == "claim":
        return run_claim(Path(argv[1]), argv[2], Path(argv[3]), Path(argv[4]))
    if mode == "hold":
        return run_hold(argv[1], Path(argv[2]))
    raise SystemExit(f"unknown worker mode: {mode!r}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
