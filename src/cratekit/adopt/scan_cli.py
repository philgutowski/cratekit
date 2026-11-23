"""``crate adopt scan``: queue the census over an existing library.

A MODULE OF ITS OWN, apart from ``adopt.apply``, which writes, is destructive and
declares gates, while this verb only reads and declares none. The marker test that
expires a ``planned_in`` keys on the registry's ``module=`` string, so one module
shared by both held the ready half back (U23).

IT QUEUES RATHER THAN SCANS (conformance 5): a census stats every file, so the
verb freezes the configuration (KTD9), queues one job with one item per LIVE
collection row, and reports it; :func:`handle` classifies one row. Reading the
rows to derive the items is cheap; probing the files is the job's work.

There is no tree argument: the active taxonomy declares exactly one (R19).

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer (KTD23, KTD25), so the builder's parameters stay unannotated.
"""

from __future__ import annotations

# ``scan`` IS ALIASED because the verb below is a function of that name.
from cratekit.adopt import artifacts, collection
from cratekit.adopt import scan as scan_engine
from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import active_taxonomy, config, jobs
from cratekit.core.cause import Outcome, refuse


def build(parser, entry) -> None:
    """Declare the verb's arguments, unannotated for the layering reason above."""
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the census already queued under this identifier rather "
            "than queueing a new one; this is how a resume re-invokes the verb"
        ),
    )
    parser.set_defaults(_handler=scan)


def adopt_scan_argv(job) -> list[str]:
    """The command line that continues one queued census, naming the job (KTD9)."""
    return ["adopt", "scan", "--job", job.job_id]


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say the library looks like.

    Read back from what ran, so a census continued tomorrow counts every report,
    zeroes included (AE12).
    """
    categories = {str(member): 0 for member in scan_engine.Readability}
    dispositions = {str(member): 0 for member in scan_engine.Disposition}
    for report in artifacts.committed(cfg, job_id):
        for counts, field in ((categories, "readability"), (dispositions, "disposition")):
            value = str(report.get(field) or "")
            if value in counts:
                counts[value] += 1
    return {"categories": categories, "dispositions": dispositions}


def _empty(reason: str, detail: str) -> tuple[dict, tuple[dict[str, str], ...]]:
    """The payload and warning for a library with nothing to census.

    Nothing is queued: ``core.jobs`` reports a job with no items as SUCCEEDED, a
    clean success over a census that never ran. The payload is
    :func:`cratekit.cli.output.no_job`'s, so no zero path can bring back R-234's
    null ``job_id``.
    """
    return no_job("no-op"), ({"code": reason, "message": detail},)


def scan(ctx) -> Envelope:
    """Queue one census over the person's own collection, and drive it on a resume.

    The handler key comes off the entry. The items are derived from the
    collection, never the census, which would stat every file before the person
    is told anything. A library of tombstones is not an empty library, and only
    the collection can tell them apart, since ``scan_rows`` skips a deleted row.
    """
    cfg = load_config(("adopt.scan_cli",))
    if ctx.args.job:
        return _resume(ctx, cfg)

    rows = collection.read_collection(cfg)
    live = tuple(row.content_id for row in rows if not row.deleted)
    if not live:
        payload, warnings = (
            _empty(
                "collection-all-tombstones",
                f"every one of the {len(rows)} rows in this library is a removal "
                f"rekordbox has not purged, so there is nothing to adopt",
            )
            if rows
            else _empty(
                "collection-empty", "this library holds no tracks, so there is nothing to census"
            )
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": active_taxonomy.load(cfg).tree.id},
            # ONE LIVE ROW IS ONE ITEM, or the driver reports an empty success.
            item_ids=live,
            cfg=cfg,
        )
        return ctx.envelope(data=jobs.reported(store, job))


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Continue the census already queued under this identifier, and drive it.

    :func:`cratekit.core.jobs.advance` reconciles first, and raises on any closed
    job carrying a cause, CANCELLED included, rather than reporting it (R-225,
    R-290).
    """
    with jobs.open_store() as store:
        job, warnings = jobs.advance(
            ctx,
            store,
            jobs.get(store, ctx.args.job),
            origin=("adopt", "scan_cli"),
            nothing_to_run="report a census over a library it never read",
        )
        return ctx.envelope(
            data=jobs.reported(store, job, {"census": _summary(cfg, job.job_id)}), warnings=warnings
        )


def handle(job, item, cfg) -> jobs.Produced:
    """Classify ONE collection row. The per-item worker behind ``adopt.scan``.

    The collection is re-read at drive time, so a row removed or tombstoned in
    rekordbox since the queueing is refused with its own slug rather than raised
    out of the worker as a defect. The configuration is the frozen one (KTD9).
    One row per item is what lets a killed census resume where it stopped.
    """
    row = collection.indexed(cfg).get(item.item_id)
    if row is None or row.deleted:
        # A TOMBSTONE COUNTS AS ABSENT: the reader carries it, ``scan_rows``
        # skips it, and the unpack below would raise ``ValueError`` as a defect.
        raise refuse(
            "adopt-item-absent",
            f"the collection no longer holds a live row {item.item_id!r} for this "
            f"item, so there is nothing to classify for it",
            steps=("queue a fresh census; this one was planned against a library that has moved",),
            origin=("adopt", "scan_cli"),
            detail={"content_id": item.item_id},
        )
    declared = active_taxonomy.load(cfg)
    (classified,) = scan_engine.scan_rows(
        [row], declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg)
    )
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "content_id": classified.content_id,
            "recorded": classified.recorded,
            "path": classified.path,
            "readability": str(classified.readability),
            "disposition": str(classified.disposition),
            "genre": classified.genre,
            "bucket": classified.bucket,
            "match": classified.match,
        },
    )
