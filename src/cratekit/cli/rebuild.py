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

ONE TREE IS ONE ITEM, and until U53 this verb passed no items at all. A job
with nothing to claim is one the driver walks in a single empty pass and
transitions straight to succeeded, so the queue reported a rebuild that
happened over a library nothing had read. The items come off the registry:
the tree the person named, or every tree that has cut over.

A LIBRARY WITH NOTHING NATIVE FILES NO JOB. There is no item list to build
for a library that has never flipped a tree, and filing an empty job is the
defect above. It is not a refusal either: nothing is wrong, there is simply
nothing to rebuild, so the verb says that and exits OK.

Layer: cli.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, tree_registry
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import rebuild as engine


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


def _no_op(state: str, **progress: Any) -> dict[str, Any]:
    """A run that correctly queued nothing.

    ``job_id`` is the empty string rather than None because the schema types it
    as a string (R-234), which is the same shape ``cratekit.intake.cli`` uses for
    the same answer.
    """
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}


def tree_items(entries: tree_registry.Registry, tree_id: str | None) -> tuple[str, ...]:
    """The trees one queued rebuild will claim, one item each.

    DERIVED FROM THE REGISTRY, never from a caller's list, which is the same
    direction :func:`cratekit.write.rebuild.rebuild_tree` takes about placements
    and for the same reason: the registry is what records that a tree has cut
    over, and a rebuild of a tree still on the bridge writes membership the next
    import overwrites.

    A NAMED TREE IS STILL FILTERED THROUGH ``is_database_native`` here rather
    than trusted from the refusal above. The refusal is what tells the person
    why; this is what decides the items, and two readings of one question that
    are only kept in agreement by the order of the lines is how one of them
    eventually gets moved.
    """
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)


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
    entries = tree_registry.read(cfg)
    if tree_id is not None and not entries.is_database_native(tree_id):
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
            # RECONCILE FIRST, then DRIVE. A resume arrives after something
            # stopped, and a claim a dead driver left behind is state the queue
            # cannot see for itself. Everything above this line already worked
            # before U46; nothing below it ever ran an item.
            job = jobs.reconcile(store, ctx.args.job)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
            return ctx.envelope(
                data=_reported(store, job),
                outcome=Outcome.OK,
                code=ExitCode.OK,
                warnings=warnings,
            )
        items = tree_items(entries, tree_id)
        if not items:
            # NOT A REFUSAL. A library that has never flipped a tree is the state
            # every library is in until its first cutover, and nothing about it
            # is wrong. What would be wrong is filing a job with nothing to
            # claim: the driver walks it in one empty pass and transitions it
            # straight to succeeded, so the queue would carry a rebuild that
            # reports as done over a library nothing read.
            return ctx.envelope(
                data=_no_op(
                    "no-native-tree",
                    trees=len(entries.tree_ids()),
                    native=0,
                ),
                outcome=Outcome.NO_OP,
                code=ExitCode.OK,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job), outcome=Outcome.OK, code=ExitCode.OK)


def handle(job, item, cfg) -> None:
    """Rebuild ONE governed tree. The per-item worker behind ``handler_key`` rebuild.

    THE ITEM IS THE TREE. ``item.item_id`` is the stable identifier this verb
    queued, so a job over three trees is three claims, three commits and three
    rows a resume can tell apart. A worker that rebuilt every tree per item would
    do the whole sweep once per tree and report each pass as one item's work.

    ``cfg`` IS THE FROZEN CONFIGURATION (KTD9) and is passed straight through.
    Nothing here loads one.

    IT PRODUCES NO ARTIFACT. A rebuild's output is playlist membership inside the
    library's own database, which the engine commits behind its own capture; there
    is no staged file for the driver to make durable, so this returns None rather
    than inventing a path for the engine's report.

    THE ACTOR IS NOT READ HERE, and that is deliberate rather than an omission.
    It is frozen on the payload so the queued job records who asked, and the one
    place the engine records a decision against a person is the convergence
    disposition, which a rebuild does not write. Handing this actor to a call
    that records an assertion would be the product asserting on the strength of a
    string, which is what R34 forbids.
    """
    del job
    # THE WORKFLOW IS NAMED HERE RATHER THAN DEFAULTED, so both workers over this
    # engine state what they write under and a reader comparing the two sees one
    # difference rather than one name and one absence.
    engine.rebuild_governed_tree(
        cfg, tree_id=str(item.item_id), workflow=engine.REBUILD_WORKFLOW
    )
    return None
