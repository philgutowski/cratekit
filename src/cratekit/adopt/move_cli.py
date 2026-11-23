"""``crate adopt move``: move a track to the sub its own file names.

A VERB OF ITS OWN, NOT A MODE OF ``route resort`` (R-758). A gate is declared
per verb and every declared gate has to fire, so an approval asked in one mode
only is a gate the registry cannot state. What is moved is decided by the
reading adoption's census took, over adoption's own plan, so it sits beside
``adopt apply`` and is switched by the same module.

THE FIRST VERB THAT REMOVES A MEMBERSHIP, treated as the cutover was: plan,
gate, snapshot, read back. The backup acknowledgment is read before the gate
(R-733), so a person with none is refused before they read a plan.

THE APPROVED MOVES ARE FROZEN IN THE JOB, and adoption's plan is not. A move
changes the tree, so a run stopped after its additions rebuilds to another
plan, and a worker that compared digests would refuse to finish its own work.
The worker acts on the approved rows and checks each against the library as it
stands: a track whose reading moved, or that sits somewhere nobody was shown,
refuses the whole run, and a track already where it belongs is done.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping, Sequence

from cratekit.adopt import apply_cli, artifacts, genre_moves, placements, shell
from cratekit.adopt import move as move_engine
from cratekit.adopt import plan as plan_engine
from cratekit.cli.output import Envelope, approving_actor, load_config
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
from cratekit.core.cause import CratekitError, Outcome, refuse
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

#: The one step every stale refusal names.
_AGAIN = ("run `crate adopt move` again and approve the plan as it is now",)


def current_plan(cfg: config.Config, declared: taxonomy.Taxonomy) -> move_engine.MovePlan:
    """The move plan over the library as it stands, from adoption's own plan."""
    return move_engine.build_move_plan(
        apply_cli.current_plan(cfg, declared, vocals=False), declared, genre_moves.read(cfg)
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
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate digested against the plan, so "
        f"there is no question to ask before moving anything",
        remedy=Remedy.REPORT_DEFECT,
        origin=("adopt.move_cli",),
        detail={"verb": entry.name},
    )


def _declined(ctx, spec, document: Mapping[str, Any]) -> Envelope | None:
    """Ask ``spec`` over a plan document: the declined envelope on an abort.

    Every move is an item, and the tracks left ride beside them in full with
    the counts. The digest covers all of it.
    """
    shown = {"digest": document["digest"], "items": list(document["moves"])}
    facts = {key: document[key] for key in ("tree", "placements", "counts")}
    if (
        ctx.gate.require(spec, plan=shown, context={**facts, "left": list(document["left"])})
        == "abort"
    ):
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)
    return None


def move_adoption(ctx) -> Envelope:
    """Read the acknowledgment, ask the approval gate against this plan, then queue.

    AN EMPTY PLAN STILL ASKS, for the reason ``adopt apply`` gives, and then
    queues nothing.
    """
    cfg = load_config(("adopt.move_cli",))
    declared = active_taxonomy.load(cfg)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    if ctx.args.job:
        return _resume(ctx, cfg)

    plan = current_plan(cfg, declared)
    document = move_engine.to_json(plan)
    spec = _approval_gate(ctx.entry)
    if (declined := _declined(ctx, spec, document)) is not None:
        return declined

    if not plan.moves:
        message = (
            f"no track sits in a sub its own reading does not name, "
            f"and {len(plan.left)} are left where they are, each "
            f"listed with its reason, so there is nothing to queue"
        )
        warning = {"code": NOTHING_TO_MOVE, "message": message}
        return ctx.envelope(data=shell.no_op("no-op"), outcome=Outcome.NO_OP, warnings=(warning,))

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                "tree": plan.tree,
                "digest": document["digest"],
                PLAN_KEY: document,
                ACTOR_KEY: approving_actor(ctx, spec),
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            item_ids=(document["digest"],),
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job))


def _frozen(job) -> Mapping[str, Any]:
    """The plan document this job froze, PROVEN, or a refusal naming the job.

    Asked before anything is shown or performed, by the worker and the resume
    alike: the job is this verb's own, it carries a plan, and the digest of its
    rows taken again here is the one it was queued under and the one the
    document states, so the gate is never shown rows a digest does not describe.
    """

    def defect(message: str, **detail: Any) -> CratekitError:
        detail = {"job_id": job.job_id, **detail}
        return refuse(
            "internal-error", message, remedy=Remedy.REPORT_DEFECT, origin=_ORIGIN, detail=detail
        )

    if job.handler_key != HANDLER_KEY:
        raise defect(
            f"job {job.job_id} was queued by {job.handler_key!r} and is not a "
            f"move, so this verb has nothing to continue in it",
            handler_key=job.handler_key,
        )
    payload = job.payload or {}
    document = payload.get(PLAN_KEY)
    if not isinstance(document, Mapping):
        raise defect(
            f"job {job.job_id} carries no plan, so there is nothing anybody "
            f"approved for it to perform"
        )
    try:
        taken = move_engine.document_digest(document)
        stated = str(document["digest"])
    except (KeyError, TypeError) as exc:
        raise defect(
            f"job {job.job_id} carries a plan short of {exc}, so it cannot be "
            f"shown whole and nothing is performed from it"
        ) from exc
    queued_under = str(payload.get("digest") or "")
    if not (taken == stated == queued_under):
        raise refuse(
            "decision-stale",
            "the plan this job carries is not the plan its approval was "
            "recorded against, so nothing was written",
            steps=_AGAIN,
            origin=_ORIGIN,
            detail={"approved": queued_under, "stated": stated, "job_id": job.job_id},
        )
    return document


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the plan the job froze, then drive its one item.

    AGAINST THE FROZEN PLAN AND NOT A REBUILT ONE, unlike ``adopt apply``: a
    move that has begun has changed the tree, so a rebuilt digest would be
    stale by this verb's own hand. Whether the library still agrees with each
    approved row is the worker's question, asked row by row.
    """
    with jobs.open_store() as store:
        job = jobs.get(store, ctx.args.job)
        spec = _approval_gate(ctx.entry)
        if (declined := _declined(ctx, spec, _frozen(job))) is not None:
            return declined
        job, warnings = shell.advance(
            ctx,
            store,
            job,
            origin=_ORIGIN,
            nothing_to_run="report a move over a library it never touched",
        )
        return ctx.envelope(
            data=shell.reported(store, job, {"move": _summary(cfg, job.job_id)}), warnings=warnings
        )


#: The fields of a committed report that are lists of content identifiers.
#: ``neither`` is here so the one outcome no path should produce is on the
#: screen if one ever does.
_LISTED = ("moved", "in_both", "untouched", "neither", "gone", "skipped", "held_back")

#: The fields of a committed report that are counts.
_COUNTED = ("added", "already_present", "removed", "already_absent")


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's LAST committed report says the library holds.

    Never a sum: each report reads back every approved track, so adding an
    earlier attempt would count a track once as in both and once as moved.
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
        steps=_AGAIN,
        origin=_ORIGIN,
        detail={"moved_under": dict(detail)},
    )


def remaining(
    approved: Sequence[move_engine.Move],
    current: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
    moved: Mapping[str, frozenset[str]] | None = None,
) -> tuple[tuple[move_engine.Move, ...], tuple[str, ...]]:
    """What is left of the approved moves over the library as it stands.

    Returns the moves still to perform, each narrowed to what is left of it,
    and the tracks the collection no longer carries. A track already in its
    target and nowhere else is done, whatever its disposition, once its reading
    is proven to still name that target.

    IT REFUSES THE WHOLE RUN, ``decision-stale``, when any approved track has
    moved in a way nobody was shown, asked of
    :func:`cratekit.adopt.move.standing_in` for the bucket the move names: the
    approval covers a track arriving at its target and leaving the subs it was
    shown leaving, in either order, and nothing else. What competes is asked of
    the taxonomy as it is now, so a sub made a sub class since is not removed.
    A move across buckets (U339) is asked its target in the bucket it files
    into and its subs left in the bucket it leaves, with ``moved`` as the plan
    read it.
    """
    entries = move_engine.entries_by_track(current.entries)
    refused = move_engine.refused_buckets(current.entries)
    claimed = move_engine.claimed_buckets(current.entries)
    moved = move_engine.still_moved(current.entries, declared, moved)
    todo: list[move_engine.Move] = []
    gone: set[str] = set()
    stale: dict[str, str] = {}
    if not current.placements.read:
        raise _stale(approved, {move.content_id: "the tree could not be read" for move in approved})
    for move in approved:
        entry = move_engine.entry_for(entries, move.content_id, move.bucket)
        if entry is None:
            # ONCE PER TRACK, since a track may carry a move in each of two
            # buckets and is gone from the collection only once.
            gone.add(move.content_id)
            continue
        # THE READING, ASKED THE WAY THE PLAN ASKED IT (R-780): adoption's sub
        # in the bucket its entry claims, the resolver's answer in any other.
        if move_engine.reading_target(entry, move.into, declared) != move.target:
            stale[move.content_id] = "its reading names another place"
            continue
        _kind, competing = routing.competing_subs(declared, move.bucket)
        _kind, into = routing.competing_subs(declared, move.into)
        if move.target not in into or not set(move.remove) <= competing:
            stale[move.content_id] = "a sub it names no longer competes"
            continue
        # THE PLAN'S OWN RULE, ASKED OF THE LIBRARY AS IT STANDS.
        now = move_engine.standing_in(
            entry, move.bucket, current.placements, declared, tree=current.tree, refused=refused,
            elsewhere=move_engine.elsewhere_of(claimed, entry), moved=moved,
        )
        if isinstance(now, move_engine.Left):
            stale[move.content_id] = f"the plan as it stands leaves it: {now.reason}"
            continue
        # THE FOLDER A MOVE FILES INTO IS PART OF WHAT WAS APPROVED (U339): a
        # genre given again since names another, and nobody was shown that one.
        if isinstance(now, move_engine.Move) and now.into != move.into:
            stale[move.content_id] = "its genre names another folder now"
            continue
        held = set(
            move_engine.held_in(
                current.placements, declared, move.bucket, move.content_id,
                elsewhere=move_engine.elsewhere_of(claimed, entry),
            )
        )
        if now is None and move.target_bucket:
            # ACROSS BUCKETS, DONE IS IN THE TARGET AND OUT OF THE OLD BUCKET.
            arrived = move.target in current.placements.holds(move.into, move.content_id)
            if arrived and not held:
                continue
            stale[move.content_id] = "the plan as it stands does not move it"
            continue
        if now is None:
            unnamed = set(current.placements.holds_unnamed(move.bucket, move.content_id))
            if held == {move.target} and not unnamed & held:
                continue
            # A target held under another name only is a playlist the writer
            # cannot see, which nobody was shown.
            stale[move.content_id] = (
                "it holds its target under another name only"
                if held == {move.target}
                else "the plan as it stands does not move it"
                if held
                else "it holds no sub of its bucket any more"
            )
            continue
        if set(now.remove) - set(move.remove):
            stale[move.content_id] = "it holds a sub nobody was shown"
            continue
        if now.add and not move.add:
            stale[move.content_id] = "it has left the sub it was approved as holding"
            continue
        todo.append(replace(move, add=now.add, remove=now.remove, holds=now.holds))
    if stale:
        raise _stale(approved, stale)
    return tuple(todo), tuple(sorted(gone))


def membership_moves(
    moves: Sequence[move_engine.Move], declared: taxonomy.Taxonomy
) -> tuple[trees.MembershipMove, ...]:
    """The moves as the writer takes them, in the names the taxonomy declares.

    A DESTINATION THE TAXONOMY DOES NOT DECLARE REFUSES rather than being
    skipped as ``adopt apply`` skips one: here a skip would be a removal made
    with its addition dropped.

    THE TARGET AND THE PLACES LEFT ARE RESOLVED BY TWO FUNCTIONS, ON PURPOSE
    (R-797). A place left may be a former place in another bucket's folder,
    found by :func:`placements.named_place`. The target is asked of
    ``destination``, which refuses a former place, so a track is never filed
    into a playlist the taxonomy stopped declaring, whatever a frozen row says.
    """
    out: list[trees.MembershipMove] = []
    for move in moves:
        try:
            target = destination(declared, move.into, move.target)
            leaving = tuple(
                placements.named_place(declared, move.bucket, sub) for sub in move.remove
            )
        except KeyError as exc:
            raise refuse(
                "decision-stale",
                f"the taxonomy no longer declares a place the approved move of "
                f"{move.content_id} names, so nothing was written",
                steps=_AGAIN,
                origin=_ORIGIN,
                detail={"content_id": move.content_id, "bucket": move.bucket},
            ) from exc
        out.append(trees.MembershipMove(content_id=move.content_id, target=target, remove=leaving))
    return tuple(out)


def read_back(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    approved: Sequence[move_engine.Move],
    gone: Sequence[str],
    claimed: Mapping[str, frozenset[str]] | None = None,
) -> dict[str, list[str]]:
    """Where every approved track sits now, read off the database afresh.

    READ BACK RATHER THAN TAKEN FROM THE WRITER'S REPORT, the writer's own
    account of itself. ``moved`` holds its target and no other competing sub,
    ``in_both`` its target and another, ``untouched`` not its target, and
    ``neither`` no competing sub at all, which no path can produce and is
    listed so it would be seen. Each move is read back in its own bucket and
    each list names a track once, so a track whose two moves (R-780) ended
    differently is in two lists.

    ``claimed`` is :func:`cratekit.adopt.move.claimed_buckets` over the plan
    the run checked against: a split place a track's other entry claims is
    that entry's band, never one this move was leaving (U340).
    """
    held_now = placements.read_placements(cfg, declared)
    claimed = claimed or {}
    found: dict[str, set[str]] = {name: set() for name in ("moved", "in_both", "untouched")}
    found.update(neither=set(), gone=set(gone))
    for move in approved:
        if move.content_id in found["gone"]:
            continue
        elsewhere = claimed.get(move.content_id, frozenset()) - {move.bucket}
        held = move_engine.held_in(
            held_now, declared, move.bucket, move.content_id, elsewhere=elsewhere
        )
        if move.target_bucket:
            # ACROSS BUCKETS (U339): the target is read in the bucket it files
            # into, and every sub of the bucket left must be gone.
            arrived = move.target in held_now.holds(move.into, move.content_id)
            name = (
                ("in_both" if held else "moved")
                if arrived
                else ("untouched" if held else "neither")
            )
            found[name].add(move.content_id)
        elif not held:
            found["neither"].add(move.content_id)
        elif move.target not in held:
            found["untouched"].add(move.content_id)
        elif held == {move.target}:
            found["moved"].add(move.content_id)
        else:
            found["in_both"].add(move.content_id)
    return {name: sorted(ids) for name, ids in found.items()}


def handle(job, item, cfg) -> jobs.Produced:
    """Perform one approved move plan and read it back. The ``adopt.move`` worker.

    THE ORDER: prove the frozen rows are the rows approved and that somebody
    approved them; check each against the library as it stands,
    :func:`remaining`, refusing with nothing opened; one guarded session, a
    capture, the additions and their commit, then the removals and theirs;
    read every approved track back through a fresh handle; commit the report,
    and only then raise if any track is not moved.

    A RUN STOPPED BETWEEN THE ADDITIONS AND THE REMOVALS SAYS SO: the report
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
            "a move records WHO approved it, and this job names nobody, so nothing was written",
            steps=("run `crate adopt move` again and answer its gate as a separate act",),
            origin=_ORIGIN,
            detail={"job_id": job.job_id},
        )

    approved = move_engine.from_rows(document["moves"])
    current = apply_cli.current_plan(cfg, declared, vocals=False)
    todo, gone = remaining(approved, current, declared, genre_moves.read(cfg))

    written: trees.MoveReport | None = None
    interrupted: BaseException | None = None
    refused: CratekitError | None = None
    if todo:
        try:
            written = _write(cfg, str(document["tree"]), membership_moves(todo, declared))
        except trees.MoveInterrupted as exc:
            written, interrupted = exc.report, exc.__cause__ or exc
        except CratekitError as exc:
            # A REFUSAL KEEPS ITS OWN TYPE AND REMEDY. Held only to read the
            # library back and commit what it says, since a refusal at the
            # second commit is over additions that landed, then raised as it came.
            refused = exc

    found = read_back(
        cfg, declared, approved, gone, move_engine.claimed_buckets(current.entries)
    )
    # A GENRE MOVE READ BACK OUT OF ITS OLD BUCKET IS SPENT (U339), so the
    # bucket is never asked again for a track a person later puts there by hand.
    # EVERY FOLDER A TRACK LEFT, a track leaving two in one job included.
    left: dict[str, set[str]] = {}
    for move in approved:
        if move.target_bucket and move.content_id in found["moved"]:
            left.setdefault(move.content_id, set()).add(move.bucket)
    genre_moves.discharge(cfg, left)
    produced = artifacts.produced(
        cfg,
        job,
        item,
        {
            "tree": str(document["tree"]),
            "actor": actor,
            "digest": frozen_digest,
            **found,
            **{name: getattr(written, name) if written else 0 for name in _COUNTED},
            **{
                name: list(getattr(written, name)) if written else []
                for name in ("held_back", "skipped", "playlists")
            },
            "interrupted": interrupted is not None or refused is not None,
        },
    )
    unfinished = sorted({*found["in_both"], *found["untouched"], *found["neither"]})
    failed = refused is not None or interrupted is not None or unfinished
    if failed and produced.staged is not None and produced.final is not None:
        jobs.commit_artifact(produced.staged, produced.final)
    if refused is not None:
        raise refused
    if interrupted is not None or unfinished:
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
