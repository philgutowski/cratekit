"""``crate label`` and ``crate sync labels``: registry, sweep, import, harvest.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long-running work queues a job. The increment engine is
``cratekit.sync.run.increment``; this shell freezes the source id and the
run id so two sources queued by ``sync all`` still share one intake file.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import catalogue, sweep
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, watermarks


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("label.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build_registry(parser, entry) -> None:
    parser.add_argument(
        "action",
        nargs="?",
        default="list",
        choices=("list", "add", "remove", "rename"),
        help="list (default), add, remove, or rename a favourite label",
    )
    parser.add_argument("name", nargs="?", help="display name or identifier")
    parser.add_argument("--to", dest="new_name", default=None, help="new display name")
    parser.add_argument("--match", default=None, help="copyright match needle")
    parser.set_defaults(_handler=registry_cmd)


def build_sync(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the increment already queued under this identifier",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        dest="run_id",
        help="intake run shared with the other sources in this sync",
    )
    parser.set_defaults(_handler=sync_labels)


def build_import(parser, entry) -> None:
    parser.add_argument("name", help="favourite label to import")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the import already queued under this identifier",
    )
    parser.set_defaults(_handler=import_label)


def build_harvest(parser, entry) -> None:
    parser.add_argument("playlist", help="playlist to harvest labels from")
    parser.set_defaults(_handler=harvest_playlist)


def sync_labels_argv(job) -> list[str]:
    argv = ["sync", "labels", "--job", job.job_id]
    run_id = (job.payload or {}).get("run_id")
    if run_id:
        argv.extend(["--run-id", str(run_id)])
    return argv


def label_import_argv(job) -> list[str]:
    name = str((job.payload or {}).get("name") or "")
    return ["label", "import", name, "--job", job.job_id]


def _checks_for(held: labels.Registry) -> list[dict]:
    if not held.labels:
        return [
            {
                "key": "labels.empty",
                "title": "favourite labels",
                "status": "ok",
                "detail": "no labels are registered",
                "remedy": None,
            }
        ]
    return [
        {
            "key": f"labels.{entry.label_id}",
            "title": entry.name,
            "status": "ok",
            "detail": entry.label_id,
            "remedy": None,
        }
        for entry in held.labels.values()
    ]


def registry_cmd(ctx) -> Envelope:
    store = labels.RegistryStore()
    action = ctx.args.action
    if action == "list":
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"count": len(held.labels)},
            }
        )
    name = ctx.args.name
    if not name:
        raise refuse(
            "label-name-invalid",
            f"label registry {action} needs a name",
            steps=("pass the label name after the action",),
            origin=("label.cli",),
        )
    if action == "add":
        label_id = store.add(name, match=ctx.args.match)
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"added": label_id, "count": len(held.labels)},
            }
        )
    if action == "remove":
        removed = store.remove(name)
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held),
                "summary": {"removed": removed, "count": len(held.labels)},
            }
        )
    if ctx.args.new_name is None:
        raise refuse(
            "label-name-invalid",
            "renaming a label needs the new display name on --to",
            steps=("pass --to with the new name",),
            origin=("label.cli",),
        )
    entry = store.load().resolve(name)
    if entry is None:
        raise refuse(
            "label-unknown",
            f"no favourite label is named {name!r}",
            steps=("list the registry and take the identifier from it",),
            origin=("label.cli",),
            detail={"name": name},
        )
    store.rename(entry.label_id, ctx.args.new_name)
    held = store.load()
    return ctx.envelope(
        data={
            "checks": _checks_for(held),
            "summary": {"renamed": entry.label_id, "count": len(held.labels)},
        }
    )


def queue_warnings() -> tuple[dict[str, str], ...]:
    """What a person should know at the moment they queue, rather than later.

    THE UNBOUND CATALOGUE IS A WARNING AND NOT A REFUSAL, which is the honest
    half of leaving the refusal to the worker. ``catalogue.bound`` says why the
    question is asked here at all: :func:`cratekit.label.catalogue.resolve`
    raises, and asking it at enqueue would refuse work a later build could run.
    What it would cost to say nothing is worse than it looks, because the worker
    runs inside a detached child whose only output is a log nobody is watching,
    so a person who is only told at drive time was told at the one moment they
    could do nothing with it.

    THE NAME IS SHARED WITH ``cratekit.modules.outbound.shell.queue_warnings``
    ON PURPOSE, and ``docs/METHOD.md`` warns about exactly one symbol meaning two
    things in two modules, so this is the line that says which of the two this
    is. It is the SAME thing on a second seam, the way ``_load`` and ``_reported``
    are already spelled once per queueing shell, rather than a second meaning for
    one word. What differs is only what each one has to look at: the outbound
    shell also reports the export rows it could not resolve, and a label sweep
    resolves nothing at enqueue by construction (KTD2), so this one asks a single
    question and takes no arguments at all.
    """
    if catalogue.bound():
        return ()
    return (
        {
            "code": "label-catalogue-unbound",
            "message": (
                "this build has no catalogue adapter for the label package, so "
                "this job will queue and then fail at the provider seam"
            ),
        },
    )


def _queue(ctx, *, payload: dict, item_ids: tuple[str, ...]) -> Envelope:
    """Queue one label job, or report the job already queued under ``--job``.

    ``item_ids`` IS A REQUIRED ARGUMENT rather than one defaulting to empty, and
    the default is what this unit removed. ``jobs.drive`` transitions a job whose
    item count is zero straight to SUCCEEDED, because nothing was attempted and
    nothing failed, so a shared helper that let a caller forget its items was one
    keyword away from a clean report over work the product never did. Each verb
    now has to say what its job is made of, and each says it in a different way:
    the sweep from the registry, the import from the entry it already resolved.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            item_ids=item_ids,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job), warnings=queue_warnings())


def sweep_items(held: labels.Registry) -> tuple[str, ...]:
    """The items one sweep job carries: one per registered favourite label.

    ONE FAVOURITE LABEL IS ONE ITEM (KTD1), and the identifier is the item id
    rather than the display name. Seam R19 and the registry's own D5 both forbid
    keying a persisted record on a name, and an item row is exactly that: a
    rename would move the name and leave the queue holding a label nothing can
    resolve.

    DERIVED FROM THE REGISTRY AND NEVER FROM A PROVIDER LISTING (KTD2).
    ``src/cratekit/backup/cli.py`` established the rule and states the reason:
    items must be derivable without touching the machine, so queueing cannot
    refuse where the work would have run once claimed. Listing the catalogue here
    would also freeze a snapshot that has moved by the time the driver claims it,
    and the registry is a local state document that needs no provider at all.
    """
    return tuple(entry.label_id for entry in held.labels.values())


def _sweep_items_or_refuse() -> tuple[str, ...]:
    """The sweep's items, or the refusal an empty registry earns.

    THE ZERO ITEM RULE, enforced before anything is written. A job with no items
    drives straight to SUCCEEDED, so queueing one here would file a sweep that
    reports a clean success over a registry it never read a label from. The
    remedy is a COMMAND rather than a diagnostic, because what is missing is a
    decision nobody has made yet rather than a fault in this installation.
    """
    items = sweep_items(labels.RegistryStore().load())
    if items:
        return items
    raise refuse(
        "label-registry-empty",
        "no favourite label is registered, so a sweep would queue a job with "
        "nothing to claim and would then report that it succeeded",
        steps=(
            "register a label with: crate label registry add <name>",
            "then run the sweep again",
        ),
        origin=("label.cli",),
    )


def sync_labels(ctx) -> Envelope:
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    # THE REGISTRY IS READ ONLY ON THE QUEUEING PATH. A resume reports the job it
    # was named, whose items were frozen when that job was queued, so loading the
    # registry there would let a label registered since then decide whether an
    # existing job may be looked at, and an emptied registry would refuse to
    # report a job whose items are all still sitting in the queue.
    items = () if ctx.args.job else _sweep_items_or_refuse()
    return _queue(ctx, payload={"source_id": "labels", "run_id": run_id}, item_ids=items)


def import_label(ctx) -> Envelope:
    held = labels.RegistryStore().load()
    entry = held.resolve(ctx.args.name)
    if entry is None:
        raise refuse(
            "label-unknown",
            f"no favourite label is named {ctx.args.name!r}",
            steps=("add the label to the registry before importing it",),
            origin=("label.cli",),
            detail={"name": ctx.args.name},
        )
    # ONE LABEL IS ONE ITEM, and there is NO ZERO ITEM GUARD on this path on
    # purpose. The refusal directly above makes one unreachable: an entry that
    # could not be resolved never reaches here, and one that could always yields
    # exactly one identifier. A guard would be a second check of a condition the
    # refusal already decides, and the copy that goes stale is the one nothing
    # can drive.
    return _queue(
        ctx,
        payload={"source_id": "labels", "name": entry.name, "label_id": entry.label_id},
        item_ids=(entry.label_id,),
    )


def harvest_playlist(ctx) -> Envelope:
    raise refuse(
        "label-playlist-unreadable",
        f"the playlist {ctx.args.playlist!r} could not be listed; harvest "
        f"needs a reachable provider playlist and will not invent labels",
        steps=("pass a playlist this account can read, then retry",),
        origin=("label.cli",),
        detail={"playlist": ctx.args.playlist},
    )


def run_increment(
    cfg: config.Config,
    source: sweep.LabelSource,
    *,
    owned: set[str] | frozenset[str],
    limit: int,
    run_id: str,
) -> run.IncrementResult:
    """Drive one labels increment. Shared run id keeps one intake file (R29)."""
    return run.increment(
        source,
        owned=owned,
        limit=limit,
        watermarks=watermarks.WatermarkStore(cfg),
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id=run_id,
        staging=Path(cfg.paths.download_staging),
    )


__all__ = [
    "build_harvest",
    "build_import",
    "build_registry",
    "build_sync",
    "harvest_playlist",
    "import_label",
    "label_import_argv",
    "queue_warnings",
    "registry_cmd",
    "run_increment",
    "sweep_items",
    "sync_labels",
    "sync_labels_argv",
]
