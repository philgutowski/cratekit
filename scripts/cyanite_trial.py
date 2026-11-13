#!/usr/bin/env python3
"""Put what Cyanite hears in a track beside the folder it is filed in (U245).

A trial, not a feature: it sends a small set of MP3s you already filed by
hand to Cyanite, a paid service that analyses the audio, and writes a table of
Cyanite's genre, sub genre, mood and energy beside each file's folder today,
then the agreement per folder. It writes that table and its summary and
nothing else: no tag, no record, no library. Nothing tempo shaped is asked
for or written.

Without --send-to-cyanite it is a plan: it lists the files, says how many it
would upload and, with --price-per-track, what that would cost, and sends
nothing. With it, --cap and --price-per-track are both needed, a count over
the cap refuses, and the key is read from the keychain:

    crate login cyanite-key --from-file PATH
    .venv/bin/python scripts/cyanite_trial.py FOLDER --output trial.tsv
    .venv/bin/python scripts/cyanite_trial.py FOLDER --output trial.tsv \\
        --send-to-cyanite --cap 40 --price-per-track 0.10

The summary lands beside the table, ``trial-agreement.tsv``. A run cut short
keeps its rows; run it again with --resume and the same --output to send only
what has no answer. The folders are read through the library's active
taxonomy, or through --taxonomy PATH.

Exit codes: 0 done, or the plan; 1 stopped partway, rows kept; 2 refused,
nothing sent.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path, help="MP3 files, or folders of them")
    parser.add_argument("--output", type=Path, required=True, help="the new table to write, a .tsv")
    parser.add_argument(
        "--send-to-cyanite",
        action="store_true",
        help="upload the files to Cyanite, which costs money; without it nothing is sent",
    )
    parser.add_argument("--cap", type=int, default=None, help="the most files this run may upload")
    parser.add_argument(
        "--price-per-track",
        type=float,
        default=None,
        help="your Cyanite plan's price for one track, for the estimate",
    )
    parser.add_argument(
        "--resume", action="store_true", help="carry on the table --output already holds"
    )
    parser.add_argument(
        "--taxonomy",
        type=Path,
        default=None,
        help="a taxonomy template to read folders through, instead of the library's",
    )
    return parser


def _taxonomy(path: Path | None):
    """The taxonomy named, or the library's active copy, read without writing."""
    from cratekit.core import active_taxonomy, config, taxonomy

    if path is not None:
        return taxonomy.load_taxonomy(path.read_text(encoding="utf-8"))
    # WRITE BACK OFF: a configuration that wants migrating is read as it is,
    # since this trial writes nothing but its own table.
    return active_taxonomy.load(config.load_from_path(config.config_path(), write_back=False))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    from cratekit.core import secrets
    from cratekit.core.cause import CratekitError
    from cratekit.core.taxonomy import TaxonomyError
    from cratekit.tagging import cyanite

    try:
        declared = _taxonomy(args.taxonomy)
    except (TaxonomyError, OSError, CratekitError) as exc:
        print(f"refused, nothing was sent: {exc}", file=sys.stderr)
        return 2
    try:
        ran = cyanite.run(
            cyanite.Settings(
                paths=tuple(args.paths),
                output=args.output,
                send=args.send_to_cyanite,
                cap=args.cap,
                price=args.price_per_track,
                resume=args.resume,
            ),
            declared,
        )
    except (
        cyanite.TrialRefused,
        cyanite.TrialStopped,
        secrets.CredentialError,
        CratekitError,
    ) as exc:
        # Every one of these is raised before the first upload: a stop after it
        # is returned on the run, never raised.
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(
            f"stopped on a file error ({type(exc).__name__}: {exc.strerror or exc}); "
            f"any rows written are kept",
            file=sys.stderr,
        )
        return 1
    return 1 if ran.stopped else 0


if __name__ == "__main__":
    sys.exit(main())
