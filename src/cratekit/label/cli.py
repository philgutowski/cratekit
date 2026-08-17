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
from cratekit.label import registry as labels
from cratekit.label import sweep
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


def _queue(ctx, *, payload: dict) -> Envelope:
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def sync_labels(ctx) -> Envelope:
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    return _queue(ctx, payload={"source_id": "labels", "run_id": run_id})


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
    return _queue(ctx, payload={"source_id": "labels", "name": entry.name, "label_id": entry.label_id})


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
    "registry_cmd",
    "run_increment",
    "sync_labels",
    "sync_labels_argv",
]
