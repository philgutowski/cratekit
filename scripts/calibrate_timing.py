"""Write the timing calibration for THIS machine, on a quiet machine.

Usage::

    .venv/bin/python scripts/calibrate_timing.py [--repeats N]

Stores the reference workload's spread in ``tests/fixtures/timing_calibration.json``,
the baseline ``tests._hardware.threshold_seconds`` scales against. A loaded
machine writes a slow baseline that loosens every threshold, so a spread over the
limit REFUSES to write (in write_calibration) unless a human passes ``--force``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repeats", type=int, default=25,
        help="how many times to run the reference workload (default 25)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="write even when the spread says the machine was not quiet",
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(REPO_ROOT))
    from tests._hardware import CALIBRATION_PATH, calibrate, write_calibration

    payload = calibrate(repeats=args.repeats)
    seconds = payload["seconds"]
    print(f"repeats:         {payload['repeats']}")
    print(f"median seconds:  {seconds['median']:.4f}")
    print(f"min seconds:     {seconds['min']:.4f}")
    print(f"max seconds:     {seconds['max']:.4f}")
    print(f"relative spread: {payload['relative_spread']:.3f}")
    try:
        write_calibration(payload, CALIBRATION_PATH, force=args.force)
    except ValueError as refusal:
        print(f"REFUSED: {refusal}")
        return 1
    print(f"wrote {CALIBRATION_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
