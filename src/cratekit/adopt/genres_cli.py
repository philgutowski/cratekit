"""``crate report genres``: name every genre that has outgrown having no folder.

WHAT IT ANSWERS (R-797). Which genres hold fifty or more tracks while no top
level folder answers for them. Rock at 109 under the non electronic folder is
the case it was written for. It names them with their counts and stops there.

IT CREATES NOTHING, AND THAT IS THE WHOLE OF ITS CONTRACT. It opens the
database without write intent, through the collection reader adoption uses,
takes no session, queues no job, files no review item and writes no state
file. A folder is added by a person editing the taxonomy and by nothing else.

WHY IT READS THE DATABASE AND NOT AN EXPORT, unlike the four verbs of
``cratekit.cli.reports``. Those are held to an import allowlist that admits no
database module and no router, on purpose, and this count needs both: the
genre each row carries and where routing files it. It also has no reason to
make a person export a collection first to be told what the collection holds.
So it sits beside the adoption readers and is switched with them, which is to
say it is always available.

WHY IT DOES NOT READ ``genre_gaps.json``. That file is declared as a count of
genre strings as they ARRIVE, nothing writes it, and a count of what the
library holds is never stale when it is taken on each run.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.scan_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.adopt import collection
from cratekit.adopt import genres as genres_engine
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy

#: The status every row here carries. A genre without a folder is worth
#: knowing and is nothing to fix, which is what doctor's INFO means.
_INFO = "info"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("adopt.genres_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: the threshold is the author's."""
    del entry
    parser.set_defaults(_handler=report_genres)


def _check(genre: genres_engine.GenreCount, threshold: int) -> dict[str, Any]:
    """One named genre as a row of the diagnostic surface."""
    return {
        "key": f"genre.{genre.name}",
        "title": genre.name,
        "status": _INFO,
        "detail": (
            f"{genre.tracks} tracks and no top level folder of its own, "
            f"{genres_engine.where(genre)}; at or over {threshold}, so a folder "
            f"is worth deciding on, and none is made until the taxonomy declares one"
        ),
        "remedy": None,
    }


def report_genres(ctx) -> Envelope:
    """Count the collection by genre and name what has no folder. Writes nothing."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    report = genres_engine.count(collection.read_collection(cfg), declared)

    checks = [_check(genre, report.threshold) for genre in report.named]
    if not checks:
        checks.append(
            {
                "key": "genre.none",
                "title": "no genre without a folder has reached the threshold",
                "status": _INFO,
                "detail": (
                    f"{len(report.genres)} genre(s) have no top level folder of "
                    f"their own and none holds {report.threshold} tracks or more"
                ),
                "remedy": None,
            }
        )
    data = {
        "checks": checks,
        "summary": {
            "threshold": report.threshold,
            "tracks": report.tracks,
            "with_folder": report.with_folder,
            "without_folder": report.without_folder,
            "no_genre": report.no_genre,
            "named": len(report.named),
            "genres": [genres_engine.row_json(genre) for genre in report.genres],
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(data=data, outcome=Outcome.OK if report.tracks else Outcome.NO_OP)


__all__ = ["build", "report_genres"]
