"""A real out-of-process job driver, for the tests that need a process to kill.

The unit's verification is "a long job killed at three different stages resumes
correctly each time", and the only honest way to run it is with a process that
genuinely dies. A thread cannot be SIGKILLed, an in-process fake cannot leave the
driver lock behind for the kernel to release, and neither one exercises the
question the engine actually answers: what does the NEXT process believe happened.

Three modes, one per property that needs a second process:

``drive``  run the item loop, stalling forever on a named item so the parent can
           kill it at a chosen point.
``seam``   the same, but through ``cratekit.cli.handlers.run_job`` and the real
           ``master`` handler, so the process that dies is running SHIPPED code
           rather than a handler written beside the test. The two are different
           claims: ``drive`` proves the engine's resume guarantee, ``seam`` proves
           the binding does not lose it on the way through.
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

#: The one loudnorm report the ``seam`` mode's stand-in encoder answers every
#: measure pass with. Same block as ``tests/test_master_cli.py``: without it the
#: measurement is empty and the apply stage refuses long before an encode is built.
LOUDNORM = (
    '{"input_i": "-20.0", "input_lra": "5.0", "input_tp": "-3.0", '
    '"input_thresh": "-30.0", "target_offset": "0.5", "output_i": "-14.0", '
    '"output_lra": "5.0", "output_tp": "-1.0"}'
)


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


def run_seam(db: Path, job_id: str, root: Path, ledger: Path, stall: str) -> int:
    """Drive one job through the SHIPPED seam, stalling inside the real handler.

    The stand-in encoder is installed on the module attribute the handler reads at
    call time, which is the same seam ``tests/test_master_cli.py`` uses. It records
    the source it was asked to master and then sleeps if that source is the one the
    parent means to kill, so the process dies with a claim held and a partial file
    in the job's staging directory, which is exactly the state the resume has to
    survive.
    """
    from cratekit.cli import handlers
    from cratekit.modules.tools import mastering

    def encoder(command):
        argv = list(command.argv)
        if argv[0].endswith("ffprobe"):
            return mastering.CommandResult(
                returncode=0, stdout="sample_rate=44100\nsample_fmt=s16\n"
            )
        if "-f" in argv and "null" in argv:
            return mastering.CommandResult(returncode=0, stderr=LOUDNORM)
        target = Path(argv[-1])
        if "pcm_s24le" in argv:
            target.write_bytes(b"intermediate")
            return mastering.CommandResult(returncode=0)
        # The encode's target is named for the SOURCE plus the engine's output
        # suffix, so the recording's own name is what comes back out. Keying the
        # stall on ``target.stem`` instead compares "three" against
        # "three_mastered" and never fires, which reads as a handler that never
        # ran rather than as a harness that never matched.
        name = target.name[: -len(mastering.OUTPUT_SUFFIX)]
        _append(ledger, name)
        if name == stall:
            target.write_bytes(b"half an encode")
            (root / f"stalled-{stall}").write_text("here")
            time.sleep(STALL_SECONDS)
        target.write_bytes(b"x" * 64)
        return mastering.CommandResult(returncode=0, stderr=LOUDNORM)

    mastering.subprocess_runner = encoder
    with jobs.open_store(db) as store:
        handlers.run_job(store, jobs.get(store, job_id), root=root)
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
    if mode == "seam":
        return run_seam(Path(argv[1]), argv[2], Path(argv[3]), Path(argv[4]), argv[5])
    if mode == "claim":
        return run_claim(Path(argv[1]), argv[2], Path(argv[3]), Path(argv[4]))
    if mode == "hold":
        return run_hold(argv[1], Path(argv[2]))
    raise SystemExit(f"unknown worker mode: {mode!r}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
