"""``crate report genres``: name every genre that has outgrown having no folder.

Which genres hold fifty or more tracks while no top level folder answers for
them (R-797), named with their counts.

IT CREATES NOTHING: it opens the database without write intent through the
adoption collection reader, takes no session, queues no job, files no review
item and writes no state file. It reads the database, not an export, because it
needs the genre of each row and the router, which the ``cratekit.cli.reports``
allowlist admits neither of. It does not read ``genre_gaps.json``, a count of
genres as they arrive that nothing writes.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.scan_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.adopt import collection
from cratekit.adopt import genres as genres_engine
from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy
from cratekit.core.cause import Outcome

#: The status every row carries: worth knowing, nothing to fix (doctor's INFO).
_INFO = "info"


#: The report's counts, in the order the summary carries them.
_COUNTED = ("threshold", "tracks", "with_folder", "without_folder", "no_genre", "too_coarse")


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: the threshold is the author's."""
    del entry
    parser.set_defaults(_handler=report_genres)


def _row(key: str, title: str, detail: str) -> dict[str, Any]:
    """One row of the diagnostic surface, at INFO and with no remedy."""
    return {"key": key, "title": title, "status": _INFO, "detail": detail, "remedy": None}


def _check(genre: genres_engine.GenreCount, threshold: int) -> dict[str, Any]:
    """One named genre as a row of the diagnostic surface."""
    return _row(
        f"genre.{genre.name}",
        genre.name,
        f"{genre.tracks} tracks and no top level folder of its own, "
        f"{genres_engine.where(genre)}; at or over {threshold}, so a folder "
        f"is worth deciding on, and none is made until the taxonomy declares one",
    )


def report_genres(ctx) -> Envelope:
    """Count the collection by genre and name what has no folder. Writes nothing."""
    cfg = load_config(("adopt.genres_cli",))
    declared = active_taxonomy.load(cfg)
    report = genres_engine.count(collection.read_collection(cfg), declared)

    checks = [_check(genre, report.threshold) for genre in report.named]
    if not checks:
        checks.append(
            _row(
                "genre.none",
                "no genre without a folder has reached the threshold",
                f"{len(report.genres)} genre(s) have no top level folder of "
                f"their own and none holds {report.threshold} tracks or more",
            )
        )
    data = {
        "checks": checks,
        "summary": {
            **{key: getattr(report, key) for key in _COUNTED},
            "named": len(report.named),
            "genres": [genres_engine.row_json(genre) for genre in report.genres],
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(data=data, outcome=Outcome.OK if report.tracks else Outcome.NO_OP)
