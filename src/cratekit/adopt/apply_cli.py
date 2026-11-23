"""``crate adopt apply``: approve one adoption plan, then apply it under one session.

A MODULE OF ITS OWN, apart from ``adopt.scan``, because this verb writes and
declares gates while the scan only reads; see ``ADOPT_APPLY_CLI_UNIT`` in
:mod:`cratekit.cli.registry`. Its explicit gate is answered the way a person
answers one, through ``crate run decide`` on the run it reached, and the run is
resumed for the next gate.

THE SESSION IS THE POINT. :func:`apply_outstanding` is the run, so the one
destructive session opens there, around the whole loop: the volume identity, the
backup acknowledgment and the library lock are asserted before any entry.

SESSIONS DO NOT NEST: :func:`cratekit.core.session.session_lock` raises
``SessionComposition`` on a nested acquisition. So the ``place`` handed to the
loop COLLECTS memberships and writes nothing, and
:func:`cratekit.write.trees.write_tree_membership`, which owns its own session,
runs in a second, sequential session in :func:`handle`.

IT WRITES NO TAG. ``apply_plan``'s ``tag_value`` is left at None, because a tag
write is the one act no snapshot undoes and no ``adopt.revert`` verb is
registered to undo it (recorded in ``docs/residual-findings.md``).

ITS MEMBERSHIP WRITE NEEDS A TREE THAT HAS CUT OVER, so the refusal on an uncut
library names ``crate tree cutover`` as its step (R-235).

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer (KTD23), so the builder's parameters stay unannotated.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import artifacts, collection, placements, scan
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.approval import grant
from cratekit.cli.output import Envelope, approving_actor, load_config, no_job
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    jobs,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import genre_favorites, trees
from cratekit.write.routing_pass import destination

#: The name this run is recorded under in the session log: the verb's own, since
#: the session layer names no verb (D2) and a logged session says which command
#: opened it.
WORKFLOW = "adopt.apply"

#: The payload key holding who answered the approval gate. FROZEN because the
#: worker has no run to ask, and :func:`cratekit.adopt.approval.grant` refuses an
#: empty actor rather than let the worker invent one (R34).
ACTOR_KEY = "approved_by"

#: The memberships one apply gathers, by folder and playlist name, as locations.
_Gathered = Mapping[tuple[str, str], list[str]]

#: An apply has exactly one item, so its artifact always has ordinal zero.
_ITEM_ZERO = SimpleNamespace(ordinal=0)


def census(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    scope: frozenset[str] | None = None,
    one_read: rb_writer.SharedRead | None = None,
) -> tuple:
    """The scanned rows this run applies: the person's own collection, classified.

    Reads the configured database through
    :func:`cratekit.adopt.collection.read_collection` and stats every recorded
    file through :func:`cratekit.adopt.scan.scan_rows`, so this is the expensive
    call of an adoption pass. An empty return means an empty library.

    ``declared`` IS A PARAMETER so one plan entry cannot be built from two
    taxonomies. ``scope`` names the rows a landing just made (U165); None is the
    whole collection. ``one_read`` is a read only report's one handle (U267).
    """
    rows = collection.read_collection(cfg, one_read=one_read)
    if scope is not None:
        rows = tuple(row for row in rows if row.content_id in scope)
    return tuple(
        scan.scan_rows(
            rows, declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg)
        )
    )


def current_plan(
    cfg: config.Config,
    declared: taxonomy.Taxonomy,
    *,
    vocals: bool = True,
    scope: frozenset[str] | None = None,
    one_read: rb_writer.SharedRead | None = None,
) -> plan_engine.AdoptionPlan:
    """Rebuild the plan this run is approving, from the census rather than a file.

    The plan is rebuilt on every run and the applied ledger carries progress
    (R26). The tree comes off the declared taxonomy, never a flag (R19).

    THE ORDER: whether the library can be filed vocally is asked first, so an
    unreadable calibration refuses before the library is walked; then the census,
    so an unreadable library refuses as it always did; then the tree and the vox
    tag in one read (R-731, R-788). ``vocals`` is False for the move verb, which
    then reads neither the tag tables nor the calibration and plans no vocal
    membership. ``scope`` narrows the census alone, so a scoped plan withholds and
    files as the whole one would (U165). ``one_read`` is ``crate organize
    --report``'s one handle (U267); a plan an apply writes against is always read
    on its own handles.
    """
    standing = placements.vocal_standing(cfg, declared) if vocals else False
    scanned = census(cfg, declared, scope=scope, one_read=one_read)
    held, sung = (
        placements.read_holdings(cfg, declared, standing=standing, one_read=one_read)
        if vocals
        else (placements.read_placements(cfg, declared, one_read=one_read), plan_engine.NO_VOCALS)
    )
    return plan_engine.build_adoption_plan(
        scanned, declared, tree=declared.tree.id, placements=held, vocals=sung
    )


def _collector(
    into: dict[tuple[str, str], list[str]],
) -> Callable[[plan_engine.PlanEntry, str, str], None]:
    """A ``place`` that records one entry's destination and writes nothing.

    IT GROUPS THE ENTRY'S LOCATION, never its content identifier:
    ``write_tree_membership`` decodes every value as a recorded location, so a
    content identifier matches nothing and a session that wrote nothing reports
    as one that ran (U55). What comes back is what the loop reached.
    """

    def place(entry: plan_engine.PlanEntry, folder: str, sub: str) -> None:
        if entry.path:
            into.setdefault((folder, sub), []).append(entry.path)

    return place


def membership_locations(
    entries: Sequence[plan_engine.PlanEntry], declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The mapping :func:`cratekit.write.trees.write_tree_membership` takes.

    Keyed on display names and valued with locations, for the reason
    :func:`_collector` gives. DERIVED FROM THE PLAN, NOT THE RUN, so a kill
    between the ledger mark and the membership write is repaired on the re-run,
    which reports the rows already there. An entry whose destination the
    taxonomy no longer declares, or with no path, is skipped rather than raised.
    """
    return _locations(entries, declared, lambda entry: entry.sub)


def _locations(
    entries: Sequence[plan_engine.PlanEntry],
    declared: taxonomy.Taxonomy,
    sub_of: Callable[[plan_engine.PlanEntry], str],
) -> dict[tuple[str, str], list[str]]:
    """Group each entry's path under the folder and playlist one of its subs names."""
    grouped: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        if not entry.path:
            continue
        try:
            folder, sub = destination(declared, entry.bucket, sub_of(entry))
        except KeyError:
            continue
        grouped.setdefault((folder, sub), []).append(entry.path)
    return grouped


def vocal_locations(
    plan: plan_engine.AdoptionPlan, declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The vocal memberships this plan adds, in the mapping the tree writer takes.

    ONLY THE ADDITIONS: a track already there may be there through a playlist
    the writer cannot find by name, and handing it over again files it twice.
    Derived from the plan, as :func:`membership_locations` is.
    """
    return _locations(plan.vocal_additions(), declared, lambda entry: entry.vocal_sub)


def planned_memberships(
    plan: plan_engine.AdoptionPlan, declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """Every membership one apply hands the tree writer: the entries, then the vocal subs.

    ONE MAPPING AND ONE WRITE, so a vocal membership lands in the session the
    entry beside it does. A vocal sub never shares a key with a bucket's own sub,
    because :func:`cratekit.adopt.plan.vocal_sub` answers none for such a bucket.
    """
    wanted = membership_locations(plan.applicable(), declared)
    for key, rows in vocal_locations(plan, declared).items():
        wanted.setdefault(key, []).extend(rows)
    return wanted


def apply_outstanding(
    cfg: config.Config,
    plan: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    actor: str,
    tag_value: Callable[[plan_engine.PlanEntry, taxonomy.Taxonomy], str | None] | None = None,
    identity_provider: object | None = None,
    mount_enumerator: object | None = None,
) -> tuple[apply_engine.ApplyReport, _Gathered]:
    """Apply the outstanding entries of one plan inside ONE destructive session.

    ``analysis_roots`` names the library root and any analysis share outside it
    (R-14), since a watch over no root reports a clean session whatever happened
    (R17). The two preflight seams are forwarded as they arrive, None meaning the
    default. The approval is minted from ``actor``, who answered the explicit
    gate, never from a flag (R34). The memberships are returned, not written, for
    the nesting reason the module docstring gives.
    """
    gathered: dict[tuple[str, str], list[str]] = {}
    watched: tuple[Path, ...] = analysis_store.watch_roots(cfg)
    with session.assert_gates(
        cfg,
        workflow=WORKFLOW,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ):
        report = apply_engine.apply_plan(
            cfg,
            plan,
            declared,
            approval=grant(plan, actor=actor),
            place=_collector(gathered),
            tag_value=tag_value,
        )
    return report, gathered


def build(parser, entry) -> None:
    """Declare the verb's arguments. There is no ``--approve`` and no ``--yes`` (R34)."""
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the adoption pass already queued under this identifier "
            "rather than queueing a new one; this is how a resume re-invokes "
            "the verb"
        ),
    )
    parser.set_defaults(_handler=apply_adoption)


def adopt_apply_argv(job) -> list[str]:
    """The command line that continues one queued adoption pass.

    It names the job (KTD9) and CARRIES ``--run``: the approval gate is explicit,
    so a resume on a fresh run would meet it with nothing recorded and refuse for
    ever. A job queued by an older build has no run and resumes to the gate.
    """
    run_id = (job.payload or {}).get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(run_id)] if run_id else []
    return [*resume, "adopt", "apply", "--job", job.job_id]


def _approval_gate(entry):
    """The explicit approval gate off the entry, found by digest source, not position."""
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate digested against the plan, so "
        f"there is no question to ask before applying one",
        remedy=Remedy.REPORT_DEFECT,
        origin=("adopt.apply_cli",),
        detail={"verb": entry.name},
    )


#: The plan document's facts the approval gate shows beside its items, in order.
_FACTS = (
    "tree",
    "counts",
    "energy",
    "collisions",
    "placements",
    "withheld_by_placement",
    "held_elsewhere",
    "outside_root",
    "vocals",
    "vocal",
    "vocal_memberships",
)


def _digested(plan: plan_engine.AdoptionPlan) -> tuple[dict, dict]:
    """The plan as the approval gate shows it, and the facts beside it (R-693).

    THE ITEMS ARE THE APPLICABLE ENTRIES, the ones the digest lists, so a
    recorded answer never stands over a screen that reads differently. The rest
    is shown as counts, beside every entry withheld over a place its track holds
    (R-731), every track left out because its file is outside the library root
    (U956), and every vocal membership an apply may write, present or not
    (R-788), all read off the plan's own document.
    """
    document = plan_engine.to_json(plan)
    listed = {entry.entry_id for entry in plan.applicable()}
    return (
        {
            "digest": document["digest"],
            "items": [entry for entry in document["entries"] if entry["id"] in listed],
        },
        {key: document[key] for key in _FACTS},
    )


def _ask(ctx, cfg: config.Config, declared: taxonomy.Taxonomy):
    """Rebuild the plan and ask the approval gate against it: the plan, the gate,
    and the answer."""
    plan = current_plan(cfg, declared)
    spec = _approval_gate(ctx.entry)
    digested, facts = _digested(plan)
    return plan, spec, ctx.gate.require(spec, plan=digested, context=facts)


def apply_adoption(ctx) -> Envelope:
    """Ask the approval gate against this plan, then queue the pass.

    The plan is built before the gate, because the gate's digest IS the plan, and
    an empty plan still asks (conformance 3). No destructive session opens here:
    queueing writes nothing. ONE ITEM, AND IT IS THE PLAN: the applied ledger is
    what resumes an apply, and an item per entry would take a capture per track,
    so a plan with nothing applicable queues no job. The approving actor is
    frozen in the payload, since the worker has no run.
    """
    cfg = load_config(("adopt.apply_cli",))
    declared = active_taxonomy.load(cfg)
    if ctx.args.job:
        return _resume(ctx, cfg)

    plan, spec, option = _ask(ctx, cfg, declared)
    if option == "abort":
        # ``job_id`` is the empty string, never None, which the declared
        # ``job_state/1`` schema refuses (R-234).
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP)

    applicable = plan.applicable()
    if not applicable:
        return ctx.envelope(
            data=no_job("no-op"),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": "adoption-nothing-applicable",
                    "message": (
                        f"this plan holds {len(plan.firsts())} track(s) and none of "
                        f"them can be placed, so there is nothing to queue"
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
                "digest": plan.digest(),
                # WHO ANSWERED, off the run record and never a flag (R34).
                ACTOR_KEY: approving_actor(ctx, spec),
                # THE RUN, under the shared key, so the resume can answer the
                # explicit gate; see ``adopt_apply_argv``.
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            item_ids=(plan.digest(),),
            cfg=cfg,
        )
        return ctx.envelope(data=jobs.reported(store, job))


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the rebuilt plan, then drive the job's one item.

    The gate is asked against the rebuilt plan, so a moved digest meets
    ``DecisionStale`` before anything opens. :func:`cratekit.core.jobs.advance`
    reconciles before driving and raises on any closed job carrying a cause
    (R-225).
    """
    if _ask(ctx, cfg, active_taxonomy.load(cfg))[2] == "abort":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP)

    with jobs.open_store() as store:
        job, warnings = jobs.advance(
            ctx,
            store,
            jobs.get(store, ctx.args.job),
            origin=("adopt", "apply_cli"),
            nothing_to_run="report an adoption over a library it never touched",
        )
        summary = _summary(cfg, job.job_id)
        return ctx.envelope(
            data=jobs.reported(store, job, {"adoption": summary}),
            warnings=[*warnings, *favorites_warnings(summary)],
        )


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say the apply landed, read back."""
    applied: list[str] = []
    failed: dict[str, str] = {}
    added = already = 0
    playlists: list[str] = []
    favorites: dict[str, object] = {
        "added": 0,
        "removals_owed": 0,
        "created": [],
        "disagreements": [],
        "skipped": "",
        "cause": "",
        "schema_version": None,
    }
    for report in artifacts.committed(cfg, job_id):
        applied.extend(str(entry) for entry in report.get("applied") or ())
        failed.update({str(k): str(v) for k, v in (report.get("failed") or {}).items()})
        added += int(report.get("added") or 0)
        already += int(report.get("already_present") or 0)
        playlists.extend(str(name) for name in report.get("playlists") or ())
        kept = report.get("favorites") or {}
        # ONLY A REPORT WHOSE ATTEMPT RAN THE REFRESH SPEAKS, and the owed count
        # is the latest, not a sum: each attempt measures the same mirror again.
        if isinstance(kept, dict) and kept:
            favorites.update(
                added=int(favorites["added"]) + int(kept.get("added") or 0),
                removals_owed=int(kept.get("removals_owed") or 0),
                created=[*favorites["created"], *(kept.get("created") or ())],
                disagreements=[
                    *favorites["disagreements"],
                    *(str(one) for one in kept.get("disagreements") or ()),
                ],
                skipped=str(kept.get("skipped") or ""),
                cause=str(kept.get("cause") or ""),
                schema_version=kept.get("schema_version"),
            )
    return {
        "applied": sorted(set(applied)),
        "failed": failed,
        "added": added,
        "already_present": already,
        "playlists": sorted(set(playlists)),
        "favorites": favorites,
    }


#: The notes the resume carries when the mirror would take favourites out, when
#: the additive refresh's read back disagreed with its plan, and when it did not
#: run at all and why.
FAVORITES_REMOVALS_OWED = "favorites-removals-owed"
FAVORITES_UNVERIFIED = "favorites-unverified"
FAVORITES_SKIPPED = "favorites-skipped"


def favorites_warnings(summary: Mapping[str, object]) -> list[dict[str, str]]:
    """The notes an adoption carries about its additive refresh: owed, skipped, unverified."""
    kept = summary.get("favorites") or {}
    if not isinstance(kept, Mapping):
        return []
    notes: list[dict[str, str]] = []
    owed = int(kept.get("removals_owed") or 0)
    if owed > 0:
        notes.append(
            {
                "code": FAVORITES_REMOVALS_OWED,
                "message": (
                    f"{owed} track(s) sit in a genre Favorites and are not in the playlist "
                    f"it mirrors; an adoption only adds, so run the favorites refresh "
                    f"verb, which asks before it removes them"
                ),
            }
        )
    skipped = str(kept.get("skipped") or "")
    cause = str(kept.get("cause") or "")
    if skipped and cause == genre_favorites.CLASS_UNDECLARED:
        # THE CAUSE CODE IS THE NOTE'S CODE (U132), in the rebuild's wording.
        version = kept.get("schema_version")
        notes.append(genre_favorites.undeclared_note(int(version) if version is not None else None))
    elif skipped:
        added = int(kept.get("added") or 0)
        notes.append(
            {
                "code": FAVORITES_SKIPPED,
                "message": (
                    "the genre Favorites were not refreshed at the end of this adoption"
                    + (f" past {added} addition(s) that committed" if added else "")
                    + f": {skipped}"
                    + (f" ({cause})" if cause else "")
                ),
            }
        )
    disagreements = [str(one) for one in kept.get("disagreements") or ()]
    if disagreements:
        notes.append(
            {
                "code": FAVORITES_UNVERIFIED,
                "message": (
                    f"the genre Favorites read back after the adoption's refresh are not "
                    f"the plan's in {len(disagreements)} folder(s): "
                    + "; ".join(disagreements)
                    + "; the adoption's own writes are true, and the favorites refresh "
                    "verb reads the mirror again"
                ),
            }
        )
    return notes


def handle(job, item, cfg) -> jobs.Produced:
    """Apply one queued plan, then write its memberships. The ``adopt.apply`` worker.

    THE ORDER IS THE DESIGN:

    1. Rebuild the plan from a fresh census; the payload carries no library.
    2. Refuse ``decision-stale`` when the rebuilt digest is not the frozen one.
    3. :func:`file_plan`: the approval minted, the MEMBERSHIPS in a session of
       their own, then ``apply_outstanding``, which marks the ledger in the one
       destructive session and writes no tag, then the additive Favorites.
    4. Commit the artifact, and only then raise if anything failed.

    THE REPEATABLE WRITE GOES FIRST, measured (2026-09-02): with the mark first,
    an uncut tree left every entry marked and no row written, and the next run
    found nothing outstanding. A kill between the two costs one re-run reporting
    every row ``already_present``.

    IT RAISES RATHER THAN RETURNING A REPORT FULL OF FAILURES, because
    ``jobs.drive`` fails an item only on a raise; the artifact is committed first
    so what happened survives. On an uncut library it always raises, marks
    nothing, and names ``crate tree cutover`` and a fresh apply (R-235).
    """
    del item
    declared = active_taxonomy.load(cfg)
    plan = current_plan(cfg, declared)
    frozen_digest = str((job.payload or {}).get("digest") or "")
    if plan.digest() != frozen_digest:
        raise refuse(
            "decision-stale",
            "the collection has changed since this adoption was approved, so the "
            "plan this job would apply is not the plan anybody agreed to",
            steps=("run `crate adopt apply` again and approve the plan as it is now",),
            origin=("adopt", "apply_cli"),
            detail={"approved": frozen_digest, "current": plan.digest()},
        )

    actor = str((job.payload or {}).get(ACTOR_KEY) or "")
    membership, report, gathered, favorites = file_plan(
        cfg,
        plan,
        declared,
        actor=actor,
        refuse_unplaced=lambda found: _refuse_unplaced(found, job, cfg),
    )

    produced = artifacts.produced(
        cfg,
        job,
        _ITEM_ZERO,
        {
            "tree": report.tree,
            "actor": report.actor,
            "digest": report.digest,
            "applied": list(report.applied),
            "already_applied": list(report.already_applied),
            "failed": dict(report.failed),
            # THREE FIELD OBJECTS, NOT A JOINED KEY: shipped display names hold a
            # slash, so ``folder/sub`` would collapse two destinations onto one.
            "gathered": [
                {"folder": folder, "sub": sub, "rows": rows}
                for (folder, sub), rows in sorted(gathered.items())
            ],
            "added": membership.added,
            "already_present": membership.already_present,
            "playlists": list(membership.playlists),
            "unplaced": [str(match.requested) for match in membership.skipped],
            "skipped": [match.requested for match in membership.skipped],
            "favorites": favorites,
        },
    )
    if report.failed:
        _commit(produced)
        raise refuse(
            "adopt-entries-failed",
            f"{len(report.failed)} of this plan's entries could not be applied: "
            f"{', '.join(sorted(report.failed))}",
            steps=("read the committed artifact under the queue root for each entry's reason",),
            origin=("adopt", "apply_cli"),
            detail={"failed": sorted(report.failed)},
        )
    return produced


#: What :func:`file_plan` answers: the membership report, the apply's report,
#: what it gathered, and the Favorites summary.
_Filed = tuple[trees.MembershipReport, apply_engine.ApplyReport, _Gathered, dict[str, object]]


def file_plan(
    cfg: config.Config,
    plan: plan_engine.AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    actor: str,
    refuse_unplaced: Callable[[trees.MembershipReport], None],
) -> _Filed:
    """Step three of :func:`handle`, shared with a native landing (U165).

    The approval is minted BEFORE anything is written, because
    ``require_approval`` runs inside the apply, after the membership write. Then
    the memberships, ``refuse_unplaced`` before the ledger is marked, the apply,
    and the additive Favorites.
    """
    grant(plan, actor=actor)

    membership = _write_memberships(cfg, plan, declared)
    refuse_unplaced(membership)

    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)

    # THE GENRE FAVORITES (U119), additive only and in a session of their own;
    # what the mirror would take out is owed to the favorites refresh. A library
    # that declares no class is told so on every apply (U132), not only on one
    # that filed a track. A skip is reported with its reason, never a failure.
    favorites: dict[str, object] = {}
    if membership.added or genre_favorites.favorites_class(declared) is None:
        outcome = genre_favorites.refresh_additive(
            cfg, declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
        refreshed = outcome.refreshed
        favorites = {
            "added": refreshed.added if refreshed else 0,
            "created": list(refreshed.created) if refreshed else [],
            "removals_owed": refreshed.removals_owed if refreshed else 0,
            # THE READ BACK TRAVELS: an adoption that has landed reports it.
            "disagreements": list(refreshed.disagreements) if refreshed else [],
            "skipped": outcome.skipped,
            "cause": outcome.cause,
            # THE VERSION THE SKIP SAW, so an upgrade before the report cannot
            # make the note false.
            "schema_version": declared.schema_version,
        }

    return membership, report, gathered, favorites


def _refuse_unplaced(membership: trees.MembershipReport, job, cfg: config.Config) -> None:
    """Refuse before the ledger is marked when a row could not be placed (R-148).

    ``write_tree_membership`` surfaces a row it could not resolve to exactly one
    live row rather than raising, and marking every entry after it would record a
    track that reached no playlist as adopted. Nothing is marked yet, so a re-run
    recovers. The refusal names the rows: two live rows or none for one file,
    both repaired in rekordbox.
    """
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    artifacts.write(
        artifacts.staged_path(cfg, job.job_id, _ITEM_ZERO.ordinal),
        {"unplaced": unplaced, "added": membership.added, "playlists": list(membership.playlists)},
    )
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} track(s) in this plan could not be placed in the "
        f"library tree, so nothing has been recorded as adopted: "
        f"{', '.join(unplaced)}",
        steps=(
            "check each named file in rekordbox: the library holds either two "
            "live rows for it or none, and both are repaired there",
        ),
        origin=("adopt", "apply_cli"),
        detail={"unplaced": unplaced},
    )


def _commit(produced: jobs.Produced) -> None:
    """Make the staged artifact durable before raising past the engine, which
    commits a handler's ``Produced`` only when the handler returns it."""
    if produced.staged is not None and produced.final is not None:
        jobs.commit_artifact(produced.staged, produced.final)


def _write_memberships(
    cfg: config.Config, plan: plan_engine.AdoptionPlan, declared: taxonomy.Taxonomy
) -> trees.MembershipReport:
    """Write the plan's memberships in a session of their own.

    THE HANDLE IS A WRITE'S, opened with ``require_closed=True`` so the
    two-process refusal and the application pin run first; the reader's closed
    handle cannot be reused. The reader's ``CollectionRow`` stands in for
    ``ContentRow``: ``index_active_rows`` reads ``content_id``, ``recorded`` and
    ``deleted``, which both carry.
    """
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        return trees.write_tree_membership(
            cfg,
            handle,
            tree_id=plan.tree,
            registry=tree_registry.read(cfg),
            plan=planned_memberships(plan, declared),
            rows=collection.read_collection(cfg),
            root_exists=lambda root_id: root_id in known,
            # The library root and the analysis share, never empty (R17).
            analysis_roots=analysis_store.watch_roots(cfg),
            prefix_map=collection.prefix_rules(cfg),
        )
    except tree_registry.TreeModeRefused as exc:
        named = _naming_the_cutover(exc)
        if named is None:
            raise
        raise named from exc
    finally:
        rb_writer.close_db(handle)


def _naming_the_cutover(exc: tree_registry.TreeModeRefused) -> CratekitError | None:
    """The bridge refusal, with the verb that answers it as its step (R-235).

    ``core`` may name no verb (D2), so the refusal arrives with a remedy and no
    act; its slug, sentence and detail are carried unchanged and the steps and
    this hop are added. Only a database write refused on the XML bridge is
    reworded; anything else answers None and is re-raised as it came.
    """
    if exc.attempted != tree_registry.Mode.DATABASE or exc.mode != tree_registry.Mode.XML:
        return None
    cause = exc.cause
    return rebuilt(
        exc,
        replace(
            cause,
            remediation=Remediation(
                remedy=cause.remediation.remedy,
                steps=(
                    f"take a Fresh Export from rekordbox, then run `crate tree "
                    f"cutover {exc.tree_id} --export <that file>`; it names "
                    f"anything else the library owes before a tree can cut "
                    f"over, a snapshot or an import, and asks for approval "
                    f"once nothing is",
                    "once the tree has cut over, run `crate adopt apply` again "
                    "and approve the plan; this job ended on a cause a resume "
                    "cannot retry, and nothing it planned was marked applied",
                ),
            ),
            origin=(*cause.origin, "adopt.apply_cli"),
        ),
    )


#: Public for ``crate organize`` (U112), which shows this verb's screen and
#: reports what its worker landed.
digested = _digested
applied_summary = _summary
