#!/usr/bin/env python3
"""Measure how far heads agree with rekordbox's own analysis (R-744).

Reads a disposable copy of the configured database, or of the database named
by ``--database``, and prints the four tempo buckets and the two key buckets
for every row whose filename carries a head. With ``--analyse N`` it also
runs this product's detector over N files rekordbox analysed itself and
prints the same buckets for the detector's answer, which is the method's own
rate. Writes nothing. Refuses while rekordbox or its agent is running.

    .venv/bin/python scripts/head_agreement.py
    .venv/bin/python scripts/head_agreement.py --database /path/to/copy.db
    .venv/bin/python scripts/head_agreement.py --analyse 300 --step 4

The recorded numbers in ``cratekit.analysis.detect`` were taken with
``--analyse 300 --step 4`` on 2026-09-30, and are replaced by hand from this
script's output after any change to the detector.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--database",
        type=Path,
        default=None,
        help="a rekordbox database to read a copy of, instead of the configured one",
    )
    parser.add_argument(
        "--analyse",
        type=int,
        default=0,
        metavar="N",
        help="also run the detector over N files rekordbox analysed itself",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=1,
        help="take every STEP-th eligible file for --analyse, spreading the sample",
    )
    parser.add_argument(
        "--json", action="store_true", help="print the distributions as JSON instead"
    )
    args = parser.parse_args(argv)

    from cratekit.analysis import agreement
    from cratekit.core import config

    cfg = config.load()
    rows = agreement.read_rows(cfg, database=args.database)
    stamped = agreement.compare(rows)
    computed = agreement.compare(row for row in rows if row.analysed_by_rekordbox)
    reports = {
        "heads_on_disk_against_every_stored_tempo": stamped,
        "heads_on_disk_against_rekordbox_own_analysis": computed,
    }
    if args.analyse > 0:
        from cratekit.analysis import detect

        if not detect.heavy_available():
            print("the analysis extra is not installed here, so --analyse cannot run")
            return 2
        window = (cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling)
        reports["detector_against_rekordbox_own_analysis"] = agreement.reanalyse(
            rows,
            cfg,
            detector=lambda path: detect.analyse_file(path, tempo_window=window),
            limit=args.analyse,
            step=args.step,
        )
    if args.json:
        import json

        print(json.dumps({name: found.as_dict() for name, found in reports.items()}, indent=2))
        return 0
    for name, found in reports.items():
        print(agreement.format_report(found, title=name.replace("_", " ")))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
