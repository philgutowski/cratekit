"""A real out-of-process job driver, for the tests that need a process to kill.

Only a process that genuinely dies shows what the NEXT process believes
happened. Modes:

``drive``  run the item loop, stalling forever on a named item.
``seam``   the same through ``cratekit.cli.handlers.run_job`` and the real
           ``master`` handler, so SHIPPED code dies.
``claim``  claim items with no driver lock, racing another worker.
``hold``   take the driver lock and wait.

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

#: The loudnorm report the ``seam`` mode's encoder answers every measure pass
#: with, as ``tests/test_master_cli.py`` does.
LOUDNORM = (
    '{"input_i": "-20.0", "input_lra": "5.0", "input_tp": "-3.0", '
    '"input_thresh": "-30.0", "target_offset": "0.5", "output_i": "-14.0", '
    '"output_lra": "5.0", "output_tp": "-1.0"}'
)


def _append(ledger: Path, line: str) -> None:
    """Record an ATTEMPT, flushed immediately, since the process is about to be killed."""
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


def seam_encoder(ledger: Path, *, stall: str = "", marker_dir: Path | None = None):
    """The stand-in encoder both halves of the seam kill test use, one factory across interpreters.

    Each item's name is recorded and flushed first. With ``stall`` it writes a
    partial file, drops the marker the parent watches for, and sleeps until killed.
    """
    from cratekit.modules.tools import mastering

    def run(command):
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
        # The target is named for the SOURCE plus the output suffix, so stall on the
        # recording's name; ``target.stem`` would never match.
        name = target.name[: -len(mastering.OUTPUT_SUFFIX)]
        _append(ledger, name)
        if stall and name == stall and marker_dir is not None:
            target.write_bytes(b"half an encode")
            (marker_dir / f"stalled-{stall}").write_text("here")
            time.sleep(STALL_SECONDS)
        target.write_bytes(b"x" * 64)
        return mastering.CommandResult(returncode=0, stderr=LOUDNORM)

    return run


def run_seam(db: Path, job_id: str, root: Path, ledger: Path, stall: str) -> int:
    """Drive one job through the SHIPPED seam, stalling inside the real handler.

    The encoder is installed where the handler reads it at call time; the
    process dies holding a claim with a partial file staged.
    """
    from cratekit.cli import handlers
    from cratekit.modules.tools import mastering

    mastering.subprocess_runner = seam_encoder(ledger, stall=stall, marker_dir=root)
    with jobs.open_store(db) as store:
        handlers.run_job(store, jobs.get(store, job_id), root=root)
    return 0


def run_claim(db: Path, job_id: str, ledger: Path, barrier: Path) -> int:
    """Claim until the queue is empty, starting only once the barrier appears.

    The barrier and pause keep both processes in the loop at once.
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
