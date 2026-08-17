"""``crate rebuild``: queue a full-scope rebuild of one governed tree (U20).

THE ACTOR IS TYPED. :class:`cratekit.core.convergence.Disposition` refuses an
empty actor, so this surface carries a real one on the command line. It is
never read from the process owner, never from a shell variable, and never
defaulted. An actor nobody typed is the product answering for the user.

THE FLAG IS CLEARED ONLY BY THE ENGINE. This module never names the
clearing call. The worker that runs the queued job calls
:func:`cratekit.write.rebuild.rebuild_tree`, which is handed the
convergence check's own difference list.

LONG WORK IS QUEUED. Conformance 5: a rebuild of a live tree is not an
inline sweep in the shell that started it.

Layer: cli.
"""

from __future__ import annotations

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, tree_registry
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("cli.rebuild",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry: registry.Entry) -> None:
    parser.add_argument(
        "--tree",
        default=None,
        help="one tree's stable identifier; every native tree by default",
    )
    parser.add_argument(
        "--actor",
        default=None,
        help="the named person taking responsibility for this rebuild",
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the rebuild already queued under this identifier",
    )
    parser.set_defaults(_handler=rebuild)


def rebuild_argv(job) -> list[str]:
    payload = job.payload
    argv = ["rebuild", "--actor", str(payload["actor"])]
    tree = payload.get("tree")
    if tree:
        argv.extend(["--tree", str(tree)])
    argv.extend(["--job", job.job_id])
    return argv


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def rebuild(ctx) -> Envelope:
    """Queue one rebuild, naming the person who asked for it."""
    actor = (getattr(ctx.args, "actor", None) or "").strip()
    if not actor:
        raise refuse(
            "rebuild-actor-required",
            "a rebuild needs a named person; an empty actor is the product "
            "answering for the user",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("pass the actor flag with the name of the person running this rebuild",),
        )
    cfg = _load()
    tree_id = getattr(ctx.args, "tree", None)
    if tree_id is not None:
        entries = tree_registry.read(cfg)
        if not entries.is_database_native(tree_id):
            raise refuse(
                "rebuild-tree-not-native",
                f"the tree {tree_id!r} is still on the XML bridge, so a "
                f"rebuild would write membership the next import would "
                f"overwrite",
                remedy=Remedy.COMPLETE_PENDING_ACTION,
                steps=("cut this tree over before rebuilding it",),
            )
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(
                data=_reported(store, jobs.reconcile(store, ctx.args.job)),
                outcome=Outcome.OK,
                code=ExitCode.OK,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": tree_id, "actor": actor},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job), outcome=Outcome.OK, code=ExitCode.OK)
