"""The four read-only report verbs: two audits and two reports (U27).

    audit.coverage        what the governed tree does not file
    audit.duplicates      what the collection may hold twice
    report.library        what this library actually contains
    report.intake-aging   which intake groupings have gone stale

**One input, and it is a file rather than the database.** Every verb here takes a
rekordbox collection export and reads it through
:mod:`cratekit.modules.reports.export`. Nothing in this module opens the
rekordbox database, and that is structural rather than careful: the reports
package is held to an import allowlist that admits no database module at all, so
a report cannot acquire a handle that could commit even by mistake.

**The export is a POSITIONAL argument and there is no configured default.** The
product has no recorded location for an export, and inventing one would mean
picking a filename in somebody's library and then reading whatever is at it. A
stale export answers every question here confidently and wrongly, so the path a
person types is the path they last wrote, which is the only way this surface can
tell them which library they are looking at.

**Three of the four emit ``diagnostic/1``, which is doctor's surface**, and they
build it out of doctor's own :class:`~cratekit.cli.doctor.Finding` rather than a
second shape that happens to serialize the same keys today. One report inventing
its own check row is how two consumers of one schema come to disagree about what
``status`` may contain.

**The fourth adjudicates, so its answers are persisted rather than printed.** A
duplicate pair is a question only a person can settle, and settling it has to
outlive the run or the same pair is offered forever (R12). That is
``review.Queue.DUPLICATES`` and a REJECTED verdict in it, never a file beside the
report.

**Truncation is reported, never silent.** ``audit.coverage`` over a library
nobody has swept can name ten thousand tracks, so it takes a limit. The summary
carries the true total beside the number listed, and a run that dropped rows says
so in a check row of its own. A capped list that reads as a complete one is worse
than no list.

Layer: cli.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from cratekit.cli import registry
from cratekit.cli.doctor import Finding, Status
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.modules.reports import aging, coverage, duplicates, export
from cratekit.modules.reports import library as library_report

#: How many uncovered tracks a coverage run lists before it says it stopped.
#: A number rather than everything, because the diagnostic surface is one JSON
#: object and a library that has never been swept puts its whole collection in
#: it. Overridable per run, and the summary reports both numbers either way.
DEFAULT_COVERAGE_LIMIT = 200


def _load() -> config.Config:
    """The configuration, or the refusal U2 already modelled for each way it fails.

    Copied in shape from ``cli.rebuild`` rather than factored out with it, and
    that is deliberate for now: the two differ only in the origin they stamp, and
    a shared helper would have to take that as an argument, which is the same
    line count with one more indirection.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("cli.reports",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _template(cfg: config.Config) -> NameTemplate:
    """The declared naming shape, with the marker text config owns (S3).

    Same rule as ``acquire.match_cli.library_template`` and for the same reason:
    a configuration with no marker text is a configuration where no file carries
    one, and a marker rule with an empty literal is refused at construction.

    THE CITATION IS CHECKED RATHER THAN REMEMBERED. It first read
    ``match_cli._template``, which is not a symbol that module has, and a
    citation nothing verifies is how a reader is sent to a function that was
    renamed two units ago. ``write/naming_cli._template`` is the third copy of
    this shape and does NOT carry the empty-marker guard, so it raises at
    ``MarkerRule`` construction on a configuration with an empty marker. That is
    recorded here rather than fixed from this unit, because it is that unit's
    verb and its own suite's business.
    """
    marker = (cfg.naming.lossy_marker or "").strip()
    if not marker:
        return NameTemplate()
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=marker),))


def _view(ctx) -> export.LibraryView:
    """The export named on the command line, read once.

    The refusal for a path that is not readable, is not an export, or is a
    truncated one comes from ``export`` itself, so every verb here says the same
    sentence about the same file.
    """
    return export.read_export_file(Path(ctx.args.export))


def _as_of(ctx) -> date:
    """The day the aging report is run FOR, defaulting to today.

    A flag rather than only a clock read, because the engine takes ``today`` as a
    parameter precisely so an answer can be asserted against a fixture, and a
    shell that only ever passed ``date.today()`` would put the untestable shape
    back one layer up.
    """
    written = getattr(ctx.args, "as_of", None)
    if written is None:
        return datetime.now(timezone.utc).date()
    # ``is None`` RATHER THAN FALSINESS, and the difference is the whole point of
    # the refusal below. An empty string is something a person TYPED, so treating
    # it as an absent flag answers for a day nobody named, which is the exact
    # outcome the refusal exists to prevent. The first version of this function
    # wrote ``if not written`` and argued in its own docstring against the
    # behaviour it then had.
    try:
        return date.fromisoformat(written)
    except ValueError as exc:
        raise refuse(
            "report-as-of-invalid",
            f"{written!r} is not a date; an aging report run for a day nobody "
            f"can name would band every grouping against a value this shell "
            f"invented",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("pass the as-of flag as an ISO date, for example 2026-08-23",),
        ) from exc


def _export_argument(parser) -> None:
    """The one argument every verb here shares, added once so it cannot drift."""
    parser.add_argument(
        "export",
        metavar="EXPORT",
        help="a rekordbox collection export to read; nothing is written to it",
    )


# ---------------------------------------------------------------------------
# audit.coverage
# ---------------------------------------------------------------------------


def build_coverage(parser, entry: registry.Entry) -> None:
    _export_argument(parser)
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_COVERAGE_LIMIT,
        help=(
            "how many uncovered tracks to list; the summary reports the true "
            "total either way, and zero lists none"
        ),
    )
    parser.set_defaults(_handler=audit_coverage)


def audit_coverage(ctx) -> Envelope:
    """What the governed tree does not file, listed and counted.

    THE COUNT IS NOT DERIVED FROM THE LIST. ``uncovered`` comes off the report and
    ``listed`` off the slice, so a limit can never make the total agree with a
    truncated list, which is the one arithmetic that would hide the truncation
    from a consumer reading only the summary.
    """
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    report = coverage.survey(_view(ctx), tree=declared.tree)

    limit = max(0, int(ctx.args.limit))
    listed = report.uncovered[:limit]
    findings = [
        Finding(
            key=f"uncovered.{placement.entry.track_id}",
            title=f"{placement.entry.artist} - {placement.entry.name}".strip(" -"),
            status=Status.FAIL,
            detail=(
                f"in no playlist under {report.tree_display!r}; the collection "
                f"holds it at {placement.entry.location}"
            ),
            remedy=Remedy.COMPLETE_PENDING_ACTION,
        )
        for placement in listed
    ]
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )
    findings.extend(
        Finding(
            key=f"folder.{'/'.join(path)}",
            title=f"{path[-1]}",
            status=Status.INFO,
            detail=f"{held} tracks filed here",
        )
        for path, held in report.folders
    )

    data = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            "tree": report.tree_id,
            "display": report.tree_display,
            "entries": report.total,
            "covered": len(report.covered),
            "uncovered": len(report.uncovered),
            "listed": len(listed),
            "placements": report.placements,
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(
        data=data, outcome=Outcome.OK if report.uncovered else Outcome.NO_OP
    )


# ---------------------------------------------------------------------------
# audit.duplicates
# ---------------------------------------------------------------------------


def build_duplicates(parser, entry: registry.Entry) -> None:
    _export_argument(parser)
    parser.set_defaults(_handler=audit_duplicates)


def audit_duplicates(ctx) -> Envelope:
    """Offer every repeated recording into the review queue and report the queue.

    IDEMPOTENT BECAUSE THE ENGINE IS. A second run over the same library re-offers
    the same items, finds them already there, and leaves any verdict alone, so a
    pair somebody rejected comes back suppressed rather than as a question. That
    is the persistent ignore, and this verb keeps no state of its own to make it
    true.
    """
    cfg = _load()
    view = _view(ctx)
    with review.open_store(cfg) as store:
        report = duplicates.audit_and_offer(
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
        )
        outstanding = review.count_unresolved(store, queue=review.Queue.DUPLICATES)

    return ctx.envelope(
        data={
            "queue": str(review.Queue.DUPLICATES),
            "items": [item.to_json() for item in report.items],
            "unresolved": outstanding,
        },
        outcome=Outcome.OK if report.items else Outcome.NO_OP,
    )


# ---------------------------------------------------------------------------
# report.library
# ---------------------------------------------------------------------------


def build_library(parser, entry: registry.Entry) -> None:
    _export_argument(parser)
    parser.set_defaults(_handler=report_library)


def report_library(ctx) -> Envelope:
    """Genres, tempo spread, tree shape and gaps, as one diagnostic.

    Every row is INFO. Nothing here is a failure: an unused bucket is a taxonomy
    somebody has not grown into and a shallow tree is a library somebody is still
    building, and a report that painted either red would be this module deciding
    what a person's library should look like.
    """
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    stats = library_report.statistics(
        _view(ctx), declared=declared, template=_template(cfg)
    )

    findings = [
        Finding(
            key=f"genre.{row.bucket_id or '/'.join(row.path)}",
            title=row.display,
            status=Status.INFO,
            detail=(
                f"{row.tracks} tracks across {row.playlists} playlists"
                + ("" if row.bucket_id else "; this folder is not in the taxonomy")
            ),
        )
        for row in stats.genres
    ]
    findings.append(
        Finding(
            key="tempo.spread",
            title="tempo spread",
            status=Status.INFO,
            detail=(
                f"{stats.tempo.lowest} to {stats.tempo.highest}, median "
                f"{stats.tempo.median}, read from {stats.tempo.readable} of "
                f"{stats.tempo.readable + stats.tempo.unreadable} names"
                if stats.tempo.readable
                else (
                    f"no name in this export carries a readable head, so the "
                    f"tempo of {stats.tempo.unreadable} tracks is unknown"
                )
            ),
        )
    )
    findings.append(
        Finding(
            key="tree.shape",
            title=stats.tree_display,
            status=Status.INFO,
            detail=(
                f"{stats.shape.folders} folders and {stats.shape.playlists} "
                f"playlists, deepest path {stats.shape.deepest} against a "
                f"declared depth of {stats.shape.declared_depth}"
            ),
        )
    )
    if stats.shape.folders == 0:
        # ONE ROW, NOT ONE PER DECLARED BUCKET. This engine reports rather than
        # refuses when the governed tree is absent, which is the right call and is
        # argued where it is made: an empty count is a true answer. Rendering it
        # as a gap row per bucket was not. Driven on an export with no tree, the
        # shipped template produced eighteen "this bucket has no folder" rows,
        # every one of them true and none of them the thing that had gone wrong,
        # which is the shape doctor's own INFO status exists to avoid.
        findings.append(
            Finding(
                key="gap.tree",
                title=f"{stats.tree_display} is not in this export",
                status=Status.INFO,
                detail=(
                    f"no folder named {stats.tree_display!r} appears anywhere in "
                    f"the exported tree, so every declared bucket is unused and "
                    f"there is nothing below it to describe; check that this is "
                    f"the current export of the library you meant"
                ),
                remedy=Remedy.COMPLETE_PENDING_ACTION,
            )
        )
    else:
        for bucket_id in stats.gaps.unused_buckets:
            findings.append(
                Finding(
                    key=f"gap.bucket.{bucket_id}",
                    title=f"{bucket_id} has no folder",
                    status=Status.INFO,
                    detail=(
                        "the taxonomy declares this bucket and the export has no "
                        "folder for it"
                    ),
                )
            )

    data = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            "tree": stats.tree_id,
            "entries": stats.entries,
            "genres": len(stats.genres),
            "unused_buckets": len(stats.gaps.unused_buckets),
            "undeclared_folders": len(stats.gaps.undeclared_folders),
            "without_head": stats.gaps.entries_without_head,
            "in_no_playlist": stats.gaps.entries_in_no_playlist,
            "deeper_than_declared": stats.shape.deeper_than_declared,
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(
        data=data, outcome=Outcome.OK if stats.entries else Outcome.NO_OP
    )


# ---------------------------------------------------------------------------
# report.intake-aging
# ---------------------------------------------------------------------------


def build_intake_aging(parser, entry: registry.Entry) -> None:
    _export_argument(parser)
    parser.add_argument(
        "--as-of",
        dest="as_of",
        default=None,
        metavar="DATE",
        help="the ISO date to age against; today by default",
    )
    parser.set_defaults(_handler=report_intake_aging)


def report_intake_aging(ctx) -> Envelope:
    """Every intake grouping in exactly one band, oldest first.

    The thresholds come from configuration through ``aging.thresholds_from`` and
    from nowhere else. A default written here would be a second answer to a
    question the config file already answers, and it would be the copy nobody
    looks at.
    """
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    report = aging.intake_aging(
        _view(ctx),
        intake=declared.intake,
        thresholds=aging.thresholds_from(cfg),
        today=_as_of(ctx),
    )

    bands = (
        ("expired", report.expired, Status.FAIL),
        ("stale", report.stale, Status.INFO),
        ("current", report.current, Status.OK),
        ("undated", report.undated, Status.INFO),
    )
    findings = [
        Finding(
            key=f"{band}.{'/'.join(grouping.path)}",
            title=grouping.display,
            status=status,
            detail=(
                f"{grouping.track_count} tracks, "
                + (
                    "no date in the name"
                    if grouping.age_days is None
                    else f"{grouping.age_days} days old"
                )
            ),
            remedy=Remedy.COMPLETE_PENDING_ACTION if status is Status.FAIL else None,
        )
        for band, groupings, status in bands
        for grouping in groupings
    ]

    data = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            "as_of": report.as_of.isoformat(),
            "stale_days": report.thresholds.stale_days,
            "expired_days": report.thresholds.expired_days,
            "groupings": len(report.groupings),
            "expired": len(report.expired),
            "stale": len(report.stale),
            "current": len(report.current),
            "undated": len(report.undated),
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(
        data=data, outcome=Outcome.OK if report.groupings else Outcome.NO_OP
    )


__all__ = [
    "DEFAULT_COVERAGE_LIMIT",
    "audit_coverage",
    "audit_duplicates",
    "build_coverage",
    "build_duplicates",
    "build_intake_aging",
    "build_library",
    "report_intake_aging",
    "report_library",
]
