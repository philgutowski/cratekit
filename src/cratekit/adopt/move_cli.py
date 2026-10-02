"""``crate adopt move``: move a track to the sub its own file names.

WHY THIS IS A VERB OF ITS OWN (R-758). ``route resort`` exists and is additive,
"the old membership stays and is named", and giving it a removing mode was the
other choice. It was not taken, for two reasons. A gate is declared per verb
and every declared gate has to fire, so an approval asked in one mode only is a
gate the registry cannot state. And what is moved is decided by the reading
adoption's census took off the file, over adoption's own plan: the entries
``adopt apply`` withholds over a place the track already holds, the ones it
finds already placed beside a stale sub, and, since R-780, every band bucket
the tree holds a track in twice whether or not its genre names that bucket.
So it sits beside ``adopt apply`` and is switched by the same module.

THIS IS THE FIRST VERB THAT REMOVES A MEMBERSHIP, and it is treated as the
cutover was: plan, gate, snapshot, read back.

THE BACKUP ACKNOWLEDGMENT IS READ BEFORE THE GATE IS ASKED (R-733). An approval
is the one way door, and ``adopt apply`` was measured taking one that the
session behind it then refused for want of an acknowledgment. Here a person
with none is refused before they read a plan, with the mint as the remedy.

THE APPROVED MOVES ARE FROZEN IN THE JOB, and adoption's plan is not. A move
changes what the tree holds, so a run stopped after its additions rebuilds to
a different plan, and a worker that compared digests would refuse to finish
its own work. The worker acts on the rows the approval was recorded against
and checks each against the library as it stands: a track whose reading moved,
or that sits somewhere nobody was shown, refuses the whole run, and a track
already where it belongs is done.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cratekit.adopt import apply_cli, artifacts, placements, shell
from cratekit.adopt import move as move_engine
from cratekit.adopt import plan as plan_engine
from cratekit.cli.output import Envelope
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    jobs,
    rb_writer,
    routing,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Outcome,
    Remediation,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees
from cratekit.write.routing_pass import destination

#: The name this run is recorded under where a verb's name is wanted.
WORKFLOW = "adopt.move"

#: The payload key holding who answered the approval gate. See
#: :data:`cratekit.adopt.apply_cli.ACTOR_KEY`.
ACTOR_KEY = apply_cli.ACTOR_KEY

#: The payload key holding the plan document the approval was recorded against.
PLAN_KEY = "plan"

#: The key this verb's jobs are queued under, which is the registry's.
HANDLER_KEY = "adopt.move"

#: The warning a run carries when the plan holds no move.
NOTHING_TO_MOVE = "move-nothing-planned"

_ORIGIN = ("adopt", "move_cli")


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
                origin=("adopt.move_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def current_plan(cfg: config.Config, declared: taxonomy.Taxonomy) -> move_engine.MovePlan:
    """The move plan over the library as it stands, from adoption's own plan."""
    return move_engine.build_move_plan(
        apply_cli.current_plan(cfg, declared, vocals=False), declared
    )


def build(parser, entry) -> None:
    """Declare the verb's arguments. THERE IS NO ``--approve`` AND NO ``--yes``."""
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the move already queued under this identifier rather "
            "than queueing a new one; this is how a resume re-invokes the verb"
        ),
    )
    parser.set_defaults(_handler=move_adoption)


def adopt_move_argv(job) -> list[str]:
    """The command line that continues one queued move, on the run that approved it."""
    run_id = (job.payload or {}).get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(run_id)] if run_id else []
    return [*resume, "adopt", "move", "--job", job.job_id]


def _approval_gate(entry):
    """The explicit approval gate off the entry, found by digest source."""
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
                f"there is no question to ask before moving anything"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("adopt.move_cli",),
            detail={"verb": entry.name},
        )
    )


def _digested(document: Mapping[str, Any]) -> tuple[dict, dict]:
    """A plan document as the gate shows it: every move, and the facts beside them.

    THE ITEMS ARE THE MOVES, EVERY ONE, each with the membership to add, the
    memberships to remove and the reading that decides it. The tracks left
    where they are ride beside them in full, with the counts by kind. The
    digest covers all of it.
    """
    return (
        {"digest": document["digest"], "items": list(document["moves"])},
        {
            "tree": document["tree"],
            "placements": document["placements"],
            "counts": document["counts"],
            "left": list(document["left"]),
        },
    )


def move_adoption(ctx) -> Envelope:
    """Read the acknowledgment, ask the approval gate against this plan, then queue.

    AN EMPTY PLAN STILL ASKS, for the reason ``adopt apply`` gives, and then
    queues nothing: a second approved run plans nothing and writes nothing.
    """
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    if ctx.args.job:
        return _resume(ctx, cfg)

    plan = current_plan(cfg, declared)
    document = move_engine.to_json(plan)
    spec = _approval_gate(ctx.entry)
    digested, facts = _digested(document)
    if ctx.gate.require(spec, plan=digested, context=facts) == "abort":
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)

    if not plan.moves:
        return ctx.envelope(
            data=shell.no_op("no-op"),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": NOTHING_TO_MOVE,
                    "message": (
                        f"no track sits in a sub its own reading does not name, "
                        f"and {len(plan.left)} are left where they are, each "
                        f"listed with its reason, so there is nothing to queue"
                    ),
                },
            ),
        )

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                "tree": plan.tree,
                "digest": document["digest"],
                PLAN_KEY: document,
                ACTOR_KEY: _approving_actor(ctx, spec),
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            item_ids=(document["digest"],),
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job))


def _frozen(job) -> Mapping[str, Any]:
    """The plan document this job froze, PROVEN, or a refusal naming the job.

    THREE THINGS ARE ASKED BEFORE ANYTHING IS SHOWN OR PERFORMED. The job is
    this verb's own, so a job another verb queued is never driven through this
    gate. It carries a plan. And the digest of the rows it carries, taken
    again here, is the digest the job was queued under and the one the
    document states, so the gate is never shown rows under a digest that does
    not describe them. The worker and the resume both come through here.
    """
    if job.handler_key != HANDLER_KEY:
        raise refuse(
            "internal-error",
            f"job {job.job_id} was queued by {job.handler_key!r} and is not a "
            f"move, so this verb has nothing to continue in it",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "handler_key": job.handler_key},
        )
    payload = job.payload or {}
    document = payload.get(PLAN_KEY)
    if not isinstance(document, Mapping):
        raise refuse(
            "internal-error",
            f"job {job.job_id} carries no plan, so there is nothing anybody "
            f"approved for it to perform",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"job_id": job.job_id},
        )
    try:
        taken = move_engine.document_digest(document)
        stated = str(document["digest"])
    except (KeyError, TypeError) as exc:
        raise refuse(
            "internal-error",
            f"job {job.job_id} carries a plan short of {exc}, so it cannot be "
            f"shown whole and nothing is performed from it",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"job_id": job.job_id},
        ) from exc
    queued_under = str(payload.get("digest") or "")
    if not (taken == stated == queued_under):
        raise refuse(
            "decision-stale",
            "the plan this job carries is not the plan its approval was "
            "recorded against, so nothing was written",
            steps=("run `crate adopt move` again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"approved": queued_under, "stated": stated, "job_id": job.job_id},
        )
    return document


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the plan the job froze, then drive its one item.

    AGAINST THE FROZEN PLAN AND NOT A REBUILT ONE, which is where this differs
    from ``adopt apply`` and why. A move that has begun has changed the tree
    the plan is built from, so a rebuilt digest would be stale by this verb's
    own hand. Whether the library still agrees with each approved row is the
    worker's question and it asks it row by row.
    """
    with jobs.open_store() as store:
        job = jobs.get(store, ctx.args.job)
        spec = _approval_gate(ctx.entry)
        digested, facts = _digested(_frozen(job))
        if ctx.gate.require(spec, plan=digested, context=facts) == "abort":
            return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)
        job, warnings = shell.advance(
            ctx,
            store,
            job,
            origin=_ORIGIN,
            nothing_to_run="report a move over a library it never touched",
        )
        return ctx.envelope(
            data=shell.reported(store, job, {"move": _summary(cfg, job.job_id)}),
            warnings=warnings,
        )


#: The fields of a committed report that are lists of content identifiers.
#: ``neither`` is here so that the one outcome no path should produce is on
#: the screen if one ever does, and the first version left it off.
_LISTED = ("moved", "in_both", "untouched", "neither", "gone", "skipped", "held_back")

#: The fields of a committed report that are counts.
_COUNTED = ("added", "already_present", "removed", "already_absent")


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's LAST committed report says the library holds.

    THE LAST ONE, and never a sum. Each report is a read back of every
    approved track, so the latest is the whole truth and adding an earlier
    attempt to it would count a track once as in both and once as moved.
    """
    reports = artifacts.committed(cfg, job_id)
    if not reports:
        return {}
    last = reports[-1]
    summary: dict[str, Any] = {name: list(last.get(name) or ()) for name in _LISTED}
    summary.update({name: int(last.get(name) or 0) for name in _COUNTED})
    return summary


def _stale(approved: Sequence[move_engine.Move], detail: Mapping[str, Any]) -> CratekitError:
    return refuse(
        "decision-stale",
        f"the library has changed under {len(detail)} track(s) of the {len(approved)} "
        f"approved move(s), so what this job would perform is not what anybody "
        f"agreed to, and nothing was written: {', '.join(sorted(detail))}",
        steps=("run `crate adopt move` again and approve the plan as it is now",),
        origin=_ORIGIN,
        detail={"moved_under": dict(detail)},
    )


def remaining(
    approved: Sequence[move_engine.Move],
    current: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
) -> tuple[tuple[move_engine.Move, ...], tuple[str, ...]]:
    """What is left of the approved moves over the library as it stands.

    Returns the moves still to perform, each narrowed to what is left of it,
    and the tracks the collection no longer carries. A track already in its
    target and nowhere else is done and is in neither.

    IT REFUSES THE WHOLE RUN, ``decision-stale``, when any approved track has
    moved in a way nobody was shown: its reading now names another sub, the
    plan as it stands would leave it or would not move it, it holds a
    competing sub that was neither its target nor one it was leaving, or it
    was approved as already in its target and is not there now. What the plan
    would do now is asked of :func:`cratekit.adopt.move.standing_in`, the body
    the plan was built from, for the bucket the move names, which since R-780
    need not be the bucket the track's genre names. Nothing is narrowed to
    fit. The approval covers a track arriving at its target and leaving the
    subs it was shown leaving, in either order, and nothing else.

    A TRACK ALREADY IN ITS TARGET AND NOWHERE ELSE IS DONE, whatever its
    disposition, once its reading is proven to still name that target above.
    The first version asked for ``route`` here as well, which only an entry
    claiming the bucket can carry, and a tree path move is over a bucket no
    entry claims.

    WHAT COMPETES IS ASKED AGAIN, of the taxonomy as it is now, so a sub a
    taxonomy edit turned into a sub class since the approval is not removed
    from.
    """
    entries = {entry.content_id: entry for entry in current.entries}
    refused = move_engine.refused_buckets(current.entries)
    todo: list[move_engine.Move] = []
    gone: set[str] = set()
    stale: dict[str, str] = {}
    if not current.placements.read:
        raise _stale(approved, {move.content_id: "the tree could not be read" for move in approved})
    for move in approved:
        entry = entries.get(move.content_id)
        if entry is None:
            # ONCE PER TRACK, since a track may carry a move in each of two
            # buckets and is gone from the collection only once.
            gone.add(move.content_id)
            continue
        # THE READING, ASKED THE WAY THE PLAN ASKED IT (R-780): adoption's sub
        # in the bucket its entry claims, the resolver's answer in any other.
        if move_engine.reading_target(entry, move.bucket, declared) != move.target:
            stale[move.content_id] = "its reading names another place"
            continue
        _kind, competing = routing.competing_subs(declared, move.bucket)
        if not {move.target, *move.remove} <= competing:
            stale[move.content_id] = "a sub it names no longer competes"
            continue
        # THE PLAN'S OWN RULE, ASKED OF THE LIBRARY AS IT STANDS.
        now = move_engine.standing_in(
            entry, move.bucket, current.placements, declared, tree=current.tree, refused=refused
        )
        if isinstance(now, move_engine.Left):
            stale[move.content_id] = f"the plan as it stands leaves it: {now.reason}"
            continue
        held = set(current.placements.holds(move.bucket, move.content_id)) & competing
        if now is None:
            unnamed = set(current.placements.holds_unnamed(move.bucket, move.content_id))
            if held == {move.target} and not unnamed & held:
                continue
            if held == {move.target}:
                # Its one place is a playlist the writer cannot see, which
                # nobody was shown. The first check asked for a routed entry
                # here and refused this shape by accident; it is refused on
                # purpose now.
                stale[move.content_id] = "it holds its target under another name only"
                continue
            stale[move.content_id] = (
                "it holds no sub of its bucket any more"
                if not held
                else "the plan as it stands does not move it"
            )
            continue
        if set(now.remove) - set(move.remove):
            stale[move.content_id] = "it holds a sub nobody was shown"
            continue
        if now.add and not move.add:
            stale[move.content_id] = "it has left the sub it was approved as holding"
            continue
        todo.append(
            move_engine.Move(
                move_id=move.move_id,
                content_id=move.content_id,
                location=move.location,
                bucket=move.bucket,
                kind=move.kind,
                target=move.target,
                add=now.add,
                remove=now.remove,
                holds=now.holds,
                energy=move.energy,
                genre=move.genre,
            )
        )
    if stale:
        raise _stale(approved, stale)
    return tuple(todo), tuple(sorted(gone))


def _summary_of(found: dict[str, set[str]]) -> dict[str, list[str]]:
    return {name: sorted(ids) for name, ids in found.items()}


def membership_moves(
    moves: Sequence[move_engine.Move], declared: taxonomy.Taxonomy
) -> tuple[trees.MembershipMove, ...]:
    """The moves as the writer takes them, in the names the taxonomy declares.

    A DESTINATION THE TAXONOMY DOES NOT DECLARE REFUSES, and is not skipped
    the way ``adopt apply`` skips one. There a skipped entry is a track not
    added. Here it would be a removal made with its addition dropped.

    THE TARGET AND THE PLACES LEFT ARE RESOLVED BY TWO FUNCTIONS, ON PURPOSE
    (R-797). A place a track leaves may be a former place, the playlist its
    bucket's tracks sat in before the bucket had a folder, which sits in
    another bucket's folder and is found by :func:`placements.named_place`.
    The target is asked of ``destination``, which knows no former place and
    refuses one, so a track is never filed into a playlist the taxonomy
    stopped declaring, whatever a frozen row says.
    """
    out: list[trees.MembershipMove] = []
    for move in moves:
        try:
            target = destination(declared, move.bucket, move.target)
            leaving = tuple(
                placements.named_place(declared, move.bucket, sub) for sub in move.remove
            )
        except KeyError as exc:
            raise refuse(
                "decision-stale",
                f"the taxonomy no longer declares a place the approved move of "
                f"{move.content_id} names, so nothing was written",
                steps=("run `crate adopt move` again and approve the plan as it is now",),
                origin=_ORIGIN,
                detail={"content_id": move.content_id, "bucket": move.bucket},
            ) from exc
        out.append(
            trees.MembershipMove(content_id=move.content_id, target=target, remove=leaving)
        )
    return tuple(out)


def read_back(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    approved: Sequence[move_engine.Move],
    gone: Sequence[str],
) -> dict[str, list[str]]:
    """Where every approved track sits now, read off the database afresh.

    READ BACK RATHER THAN TAKEN FROM THE WRITER'S REPORT, which is the
    writer's own account of itself. ``moved`` holds its target and no other
    competing sub. ``in_both`` holds its target and at least one other.
    ``untouched`` does not hold its target. ``neither`` holds no competing sub
    at all, which no path here can produce and is listed so that it would be
    seen.

    EACH LIST NAMES A TRACK ONCE. Since R-780 a track may carry a move in each
    of two buckets, and each move is read back in its own bucket, so a track
    whose two moves ended differently is in two lists, and one whose two
    ended the same is in that list once.
    """
    held_now = placements.read_placements(cfg, declared)
    found: dict[str, set[str]] = {
        "moved": set(), "in_both": set(), "untouched": set(), "neither": set(), "gone": set(gone)
    }
    for move in approved:
        if move.content_id in found["gone"]:
            continue
        _kind, competing = routing.competing_subs(declared, move.bucket)
        held = set(held_now.holds(move.bucket, move.content_id)) & competing
        if not held:
            found["neither"].add(move.content_id)
        elif move.target not in held:
            found["untouched"].add(move.content_id)
        elif held == {move.target}:
            found["moved"].add(move.content_id)
        else:
            found["in_both"].add(move.content_id)
    return _summary_of(found)


def handle(job, item, cfg) -> jobs.Produced:
    """Perform one approved move plan and read it back. The ``adopt.move`` worker.

    THE ORDER.

    1. Prove the frozen rows are the rows the approval was recorded against,
       by taking their digest again, and that somebody approved them.
    2. Check each against the library as it stands, :func:`remaining`. A
       library that moved refuses here, with nothing opened.
    3. One guarded session: a capture, the additions and their commit, then
       the removals and theirs.
    4. Read every approved track back through a fresh handle.
    5. Commit the report, and only then raise if any track is not moved.

    A RUN STOPPED BETWEEN THE ADDITIONS AND THE REMOVALS SAYS SO. The report
    lists the tracks in both subs, the job fails on a cause a resume retries,
    and the resume finds the additions present and makes the removals.
    """
    declared = active_taxonomy.load(cfg)
    document = _frozen(job)
    payload = job.payload or {}
    frozen_digest = str(payload.get("digest") or "")
    actor = str(payload.get(ACTOR_KEY) or "")
    if not actor.strip():
        raise refuse(
            "decision-required",
            "a move records WHO approved it, and this job names nobody, so "
            "nothing was written",
            steps=("run `crate adopt move` again and answer its gate as a separate act",),
            origin=_ORIGIN,
            detail={"job_id": job.job_id},
        )

    approved = move_engine.from_rows(document["moves"])
    todo, gone = remaining(
        approved, apply_cli.current_plan(cfg, declared, vocals=False), declared
    )

    written: trees.MoveReport | None = None
    interrupted: BaseException | None = None
    refused: CratekitError | None = None
    if todo:
        try:
            written = _write(cfg, str(document["tree"]), membership_moves(todo, declared))
        except trees.MoveInterrupted as exc:
            written, interrupted = exc.report, exc.__cause__ or exc
        except CratekitError as exc:
            # A REFUSAL KEEPS ITS OWN TYPE AND ITS OWN REMEDY. It is held only
            # long enough to read the library back and commit what it says,
            # since a refusal at the second commit is over additions that
            # landed, and it is raised again below as it came.
            refused = exc

    found = read_back(cfg, declared, approved, gone)
    produced = artifacts.produced(
        cfg,
        job,
        item,
        {
            "tree": str(document["tree"]),
            "actor": actor,
            "digest": frozen_digest,
            **found,
            "added": written.added if written else 0,
            "already_present": written.already_present if written else 0,
            "removed": written.removed if written else 0,
            "already_absent": written.already_absent if written else 0,
            "held_back": list(written.held_back) if written else [],
            "skipped": list(written.skipped) if written else [],
            "playlists": list(written.playlists) if written else [],
            "interrupted": interrupted is not None or refused is not None,
        },
    )
    unfinished = sorted({*found["in_both"], *found["untouched"], *found["neither"]})
    if refused is not None:
        if produced.staged is not None and produced.final is not None:
            jobs.commit_artifact(produced.staged, produced.final)
        raise refused
    if interrupted is not None or unfinished:
        if produced.staged is not None and produced.final is not None:
            jobs.commit_artifact(produced.staged, produced.final)
        raise refuse(
            "adopt-entries-failed",
            f"{len(unfinished)} track(s) of {len(approved)} approved move(s) did "
            f"not finish. {len(found['in_both'])} track(s) sit in the sub they were "
            f"moved to and in the one they were leaving, "
            f"{len(found['untouched'])} are where they were, and "
            f"{len(found['neither'])} are in neither: "
            f"{', '.join(unfinished)}"
            + (f". The run stopped on: {interrupted}" if interrupted is not None else ""),
            steps=(
                f"run `crate job resume {job.job_id}` to finish it; the "
                f"additions that landed are found present and the removals are made",
            ),
            retryable=True,
            origin=_ORIGIN,
            detail={
                "in_both": found["in_both"],
                "untouched": found["untouched"],
                "neither": found["neither"],
            },
        ) from interrupted
    return produced


def _write(
    cfg: config.Config, tree_id: str, moves: Sequence[trees.MembershipMove]
) -> trees.MoveReport:
    """Perform the moves through a handle of this function's own, opened to write."""
    handle_ = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        known = {str(row.ID) for row in handle_.get_playlist()}
        return trees.move_tree_membership(
            cfg,
            handle_,
            tree_id=tree_id,
            registry=tree_registry.read(cfg),
            moves=moves,
            root_exists=lambda root_id: root_id in known,
            analysis_roots=analysis_store.watch_roots(cfg),
        )
    finally:
        rb_writer.close_db(handle_)


def _approving_actor(ctx, spec) -> str:
    """Who the run record says answered the approval gate."""
    decision = ctx.run.decisions.get(spec.name)
    return decision.actor if decision is not None else ""


__all__ = [
    "ACTOR_KEY",
    "HANDLER_KEY",
    "NOTHING_TO_MOVE",
    "PLAN_KEY",
    "WORKFLOW",
    "adopt_move_argv",
    "build",
    "current_plan",
    "handle",
    "membership_moves",
    "move_adoption",
    "read_back",
    "remaining",
]
