"""Write the timing calibration for THIS machine, on a quiet machine.

Usage::

    .venv/bin/python scripts/calibrate_timing.py [--repeats N]

Runs the fixed reference workload the declared number of times and stores the
spread in ``tests/fixtures/timing_calibration.json``, which is the baseline
``tests._hardware.threshold_seconds`` expresses timing thresholds against.

Calibrate on a QUIET machine, never while other agents or heavy jobs run: the
baseline is meant to capture the machine, and a loaded machine writes a slow
baseline that then quietly loosens every threshold derived from it. The
relative spread is printed so an unquiet run is visible. Treat a spread over
about 0.25 as a reason to rerun, not a number to commit.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repeats",
        type=int,
        default=25,
        help="how many times to run the reference workload (default 25)",
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
    if payload["relative_spread"] > 0.25:
        print("WARNING: spread over 0.25, the machine does not look quiet; rerun before committing")
    write_calibration(payload, CALIBRATION_PATH)
    print(f"wrote {CALIBRATION_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
