"""``crate rebuild``: queue a full-scope rebuild of one governed tree (U20).

The actor is typed on the command line, never read from the process owner,
never from a shell variable, and never defaulted, since an actor nobody typed
is the product answering for the user.
Only the engine clears the unconverged flag. The work is queued with one item
per native tree (U53); a library with no native tree files no job, since an
itemless job would report a rebuild over a library nothing read.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli import registry
from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import active_taxonomy, config, convergence, jobs, tree_registry
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli
from cratekit.write import rebuild as engine

#: Where each rebuilt tree's report is kept: what the after check found it left
#: and could not compare (R-635, R-2020), read back by the resume.
REBUILD_ARTIFACTS = jobs.Artifacts(final="rebuild-artifacts", staging="rebuild-staging")


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


def tree_items(entries: tree_registry.Registry, tree_id: str | None) -> tuple[str, ...]:
    """The trees one queued rebuild will claim, one item each.

    Derived from the registry, never a caller's list, since a tree still on
    the bridge would have its membership overwritten by the next import. A
    named tree is filtered here too, not trusted from the earlier refusal.
    """
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or itemless job, drive it, and report how it ended.

    Reconcile first, to release claims a dead driver left. The job must be a
    rebuild, since ``run_job`` resolves the worker from the job row. An
    itemless job is refused, since ``drive`` would record it succeeded. A job
    that closed badly, partly or on entry, is never an OK exit (R-225).
    """
    job = jobs.reconcile(store, job_id)
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not a "
            f"rebuild, so this verb will not drive it",
            steps=(f"resume it through its own verb, or with: crate job resume {job.job_id}",),
            origin=("cli.rebuild",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no tree to rebuild, so driving it would "
                f"report a rebuild that happened over a library nothing read. It "
                f"was queued by a build that did not record what its items were",
                remedy=Remedy.REPORT_DEFECT,
                steps=(
                    f"cancel it with: crate job cancel {job.job_id}",
                    "then queue the rebuild again, which records one item per tree",
                ),
                origin=("cli.rebuild",),
                detail={"job_id": job.job_id},
            )
        # The cut is read before anything is driven, as the worker reads it, so
        # a corrupt calibration refuses before any claim (U89). The file is not
        # frozen, so a later calibration is the one used.
        threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
        # The declaration the worker derives with, read the same way (R-685).
        declared = active_taxonomy.load(jobs.frozen_config(job))
        # Only the branch that drove says what the drive found (R-316, U132,
        # R-635, R-2020), on both its exits.
        drive = engine.ReportedDrive.of(store, job, REBUILD_ARTIFACTS)
        with drive.owing():
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
            jobs.raise_for_state(job)
        warnings = (*warnings, *drive.found(threshold, declared))
    jobs.raise_for_state(job)
    return ctx.envelope(
        data=jobs.reported(store, job),
        outcome=Outcome.OK,
        code=ExitCode.OK,
        warnings=warnings,
    )


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
    cfg = load_config(("cli.rebuild",))
    with jobs.open_store() as store:
        if ctx.args.job:
            # The resume reads no registry and no tree flag, so an unreadable
            # registry never blocks work whose items are already frozen.
            return _resume(ctx, store, ctx.args.job)
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
        declared = active_taxonomy.load(cfg)
        if tree_id is not None and not engine.derivable(declared, tree_id):
            # Never queued, since the engine would refuse it; a person answers
            # for it instead (U219).
            return _accept_as_it_stands(ctx, cfg, declared, tree_id)
        items = tuple(t for t in tree_items(entries, tree_id) if engine.derivable(declared, t))
        if not items:
            # Not a refusal, nothing is wrong. An itemless job would report a
            # rebuild done over a library nothing read, so none is filed.
            native = tree_items(entries, None)
            return ctx.envelope(
                data=no_job(
                    # A native tree the taxonomy does not derive is still native,
                    # so the state says which zero (U219).
                    "no-derivable-tree" if native else "no-native-tree",
                    trees=len(entries.tree_ids()),
                    native=len(native),
                ),
                outcome=Outcome.NO_OP,
                code=ExitCode.OK,
                warnings=_left_alone(entries, declared, items),
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
            cfg=cfg,
        )
        return ctx.envelope(
            data=jobs.reported(store, job),
            outcome=Outcome.OK,
            code=ExitCode.OK,
            # Only a sweep names what it left alone (U219): a rebuild of one
            # named tree skipped nothing.
            warnings=_left_alone(entries, declared, items) if tree_id is None else [],
        )


#: The gate a person answers to accept, as it stands, a tree no rebuild can
#: reproduce that a restore marked unconverged (U219).
ACCEPT_GATE = "rebuild.accept"


def _accept_as_it_stands(ctx, cfg: config.Config, declared: Any, tree_id: str) -> Envelope:
    """Let a named person accept a marked tree no rebuild can reproduce (U219).

    Nothing derives the intake tree's batches, so after a restore marks it a
    person disposes of the difference, recorded as a
    :class:`cratekit.core.convergence.Disposition` (R-789). The flag stays
    set, so reports still say unconverged, but writes stop refusing. The
    disposition names the gate's recorded actor, not ``--actor`` (R34). A tree
    that is not refusing has nothing to accept and is refused before the gate.
    """
    if tree_registry.read(cfg).is_database_native(tree_id):
        # Detect first, so the gate shows the record the database now warrants.
        engine.detect_restore(cfg)
    record = convergence.read(cfg).tree(tree_id)
    if record is None or not record.blocking:
        engine.assert_derivable(declared, tree_id)
    others = engine.other_declared_trees(declared)
    spec = next(gate for gate in ctx.entry.gates if gate.name == ACCEPT_GATE)
    option = ctx.gate.require(
        spec,
        context={
            "tree": f"{others.get(tree_id, tree_id)} ({tree_id})",
            "unconverged since": record.since,
            "reason": record.reason,
            "what accepting means": (
                "no rebuild can reproduce this tree, so its writes stop refusing "
                "over the restore and the tree is reported unconverged, accepted "
                "by you, until it is next marked"
            ),
        },
        # The answer is pinned to the mark it was given over, so a restore in
        # between makes it stale (U161).
        pinned={"since": str(record.since or ""), "reason": str(record.reason or "")},
    )
    if option != "accept":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, code=ExitCode.OK)
    engine.accept_as_it_stands(
        cfg, declared, tree_id, actor=ctx.gate.state.decisions[spec.name].actor
    )
    return ctx.envelope(
        data=no_job("accepted", tree=tree_id),
        outcome=Outcome.OK,
        code=ExitCode.OK,
    )


def _left_alone(
    entries: tree_registry.Registry, declared: Any, items: tuple[str, ...]
) -> list[dict[str, str]]:
    """The native trees this rebuild left alone because the taxonomy does not derive them (U219).

    Named, not dropped, so a person reads that it was on purpose (R-789).
    """
    others = engine.other_declared_trees(declared)
    skipped = [t for t in tree_items(entries, None) if t not in items and t in others]
    if not skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": "tree-not-derived",
            "message": f"left alone: {named}, which holds what the verbs that write "
            f"it put there and not anything a tag decides, so no rebuild can "
            f"reproduce it",
        }
    ]


def handle(job, item, cfg) -> jobs.Produced:
    """Rebuild one governed tree, the per-item worker behind ``handler_key`` rebuild.

    The item is the tree, so a resume can tell trees apart. ``cfg`` is the
    frozen configuration (KTD9). The write is database membership the engine
    commits itself; the item's report is what the check after it found the
    tree left and could not compare (R-635, R-2020), the resume's only way to
    learn it (R-443). The actor is deliberately not read, since a rebuild
    records no assertion against a person (R34).
    """
    tree_id = str(item.item_id)
    # The workflow is named, not defaulted, as the other worker over this engine does.
    report = engine.rebuild_governed_tree(
        cfg,
        tree_id=tree_id,
        workflow=engine.REBUILD_WORKFLOW,
        # The calibrated cut, or None on a library never calibrated (U89, D7).
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
    )
    return REBUILD_ARTIFACTS.produced(
        cfg, job, item, engine.after_report(tree_id, report.after, active_taxonomy.load(cfg))
    )
