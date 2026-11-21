"""``crate sync removed``: each downloaded track taken off its playlist on the account (U287).

The engine is :mod:`cratekit.sync.removed`, and its docstring says what is
downloaded, what is synced, when a track counts as removed and how each row is
answered. This module is the order a person meets it in:

* the session log is read once, and the downloaded playlists found from it,
  before anything is opened or asked;
* the database is read on a disposable copy, so the verb refuses while
  rekordbox or its agent runs and never holds the live file;
* the account is asked only when something was downloaded: its playlist list
  once, then each downloaded playlist, and every other synced playlist and
  the account's hearts only when a removal was found, since only then does
  "still on another synced playlist" need an answer;
* the plan is shown, digested; a plan that offers nothing ends there and
  writes nothing;
* a plan that offers a row reads the backup acknowledgment, then asks the
  explicit gate ``sync.removed.confirm`` over the digested plan, every offered,
  kept and left row on its screen (U288);
* only ``apply`` opens the database to write, refusing while rekordbox or its
  agent runs, and the engine takes the plan again on that handle and refuses
  ``decision-stale`` when anything moved in between. The offered rows leave the
  collection as rekordbox's own Remove from Collection takes them out, and no
  file is touched: each file reaches the Trash only through the next ``crate
  delete review``, which reads the session record this writes.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, analysis_store, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import removed

#: Nothing is offered, since a synced playlist was not read whole.
PARTIAL = "sync-removed-partial"

#: A downloaded playlist the account no longer lists.
GONE = "sync-removed-playlist-gone"

#: Session records that could not be read, so what a landing made may be unnamed.
RECORDS_UNREADABLE = "sync-removed-records-unreadable"

#: The explicit gate a removal from the collection is asked behind (U288).
CONFIRM_GATE = "sync.removed.confirm"

#: What the apply took out of the collection, read back.
APPLIED = "sync-removed-applied"

def build_removed(parser, entry) -> None:
    del entry
    parser.set_defaults(_handler=sync_removed)


def payload(plan: removed.RemovedPlan) -> dict[str, Any]:
    """The plan as the envelope carries it, every answer, then each playlist not read whole."""
    items: list[dict[str, Any]] = [{"action": one.answer, **one.identity()} for one in plan.answers]
    items.extend(
        {"action": "playlist", **one.identity()}
        for one in plan.listings
        if one.state != removed.READ
    )
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(plan.answers),
            removed.OFFERED: plan.count(removed.OFFERED),
            removed.KEPT: plan.count(removed.KEPT),
            removed.LEFT: plan.count(removed.LEFT),
            "playlists read": sum(1 for one in plan.listings if one.state == removed.READ),
            "playlists not read whole": sum(
                1 for one in plan.listings if one.state in removed.NOT_WHOLE
            ),
            "playlists gone": sum(1 for one in plan.listings if one.state == removed.GONE),
            "partial": plan.partial,
        },
        "chunk": None,
    }


def warnings_of(plan: removed.RemovedPlan) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    if plan.partial:
        named = "; ".join(
            f"{one.name or one.account} ({one.state}: {one.why})"
            for one in plan.listings
            if one.state in removed.NOT_WHOLE
        )
        found.append(
            {
                "code": PARTIAL,
                "message": (
                    f"nothing is offered, since a synced playlist was not read whole and "
                    f"whether a removed track is still on it cannot be answered: {named}"
                ),
            }
        )
    gone = [one for one in plan.listings if one.state == removed.GONE]
    if gone:
        found.append(
            {
                "code": GONE,
                "message": (
                    f"{len(gone)} synced playlist(s) the account no longer lists, so none "
                    f"of their tracks is offered: "
                    + ", ".join(one.account for one in gone)
                ),
            }
        )
    if plan.unreadable:
        found.append(
            {
                "code": RECORDS_UNREADABLE,
                "message": (
                    f"{plan.unreadable} session record(s) could not be read, so a "
                    f"playlist a landing downloaded, the folder it filed into, or the "
                    f"twin it made may be unknown here; a row that needed one is kept "
                    f"or left out, never offered on its account"
                ),
            }
        )
    return found


def facts(plan: removed.RemovedPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: each offered row, then what is written."""
    return {
        "offered": [
            f"{one.artist} - {one.title}, taken off {', '.join(one.removed_from)}: {one.file}"
            for one in plan.offered
        ],
        "kept or left": len(plan.answers) - len(plan.offered),
        "writes": (
            "each offered row out of the rekordbox collection, with every membership, "
            "cue, history entry, analysis file row and mixer row naming it, as "
            "rekordbox's Remove from Collection does; no other row, no playlist row and "
            "no file. crate delete review then offers each file to the Trash"
        ),
    }


def _gate(entry) -> Any:
    for spec in entry.gates:
        if spec.name == CONFIRM_GATE:
            return spec
    raise LookupError(f"{entry.name} declares no {CONFIRM_GATE} gate")


def sync_removed(ctx) -> Envelope:
    """Answer each removed track, then, behind the gate, take the offered rows out of the collection."""
    cfg = sync_cli._load()
    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    records, unreadable = session.scan_log(cfg)
    found = removed.downloaded(cfg, records)
    with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
        reads: dict[str, removed.Listing] = {}
        if found:
            from cratekit.label import catalogue
            from cratekit.modules.outbound import pairs

            account = catalogue.resolve(cfg)
            listed = removed.account_listing(account)
            recorded = removed.recorded_contents(cfg)
            reads = removed.read_account(
                account, [one.account for one in found], listed=listed, recorded=recorded
            )
            if removed.removals(found, reads):
                others = [
                    one
                    for one in removed.synced(
                        cfg,
                        found,
                        paired=pairs.paired_ids(cfg),
                        swept_now=removed.job_playlists(cfg),
                        listed=listed,
                    )
                    if one not in reads
                ]
                reads.update(
                    removed.read_account(account, others, listed=listed, recorded=recorded)
                )
                reads[removed.HEARTS] = removed.read_hearts(account)
        plan = removed.plan_removed(
            cfg,
            db,
            declared=declared,
            registry=registry,
            records=records,
            found=found,
            reads=reads,
            unreadable=len(unreadable),
        )
    data = payload(plan)
    warnings = warnings_of(plan)
    if not plan.offered:
        return ctx.envelope(
            data=data,
            outcome=Outcome.OK if plan.answers else Outcome.NO_OP,
            warnings=warnings,
        )
    # BEFORE THE GATE (R-733), and only once something is offered, so a run
    # that lists and offers nothing asks for nothing.
    session.assert_backup_acknowledged(cfg)
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    done = written(
        cfg,
        plan,
        declared=declared,
        registry=registry,
        records=records,
        found=found,
        reads=reads,
        unreadable=len(unreadable),
    )
    data["totals"] = {
        **data["totals"],
        "removed": len(done.rows),
        "rows deleted": sum(done.deleted.values()),
    }
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": APPLIED,
                "message": (
                    f"{len(done.rows)} track(s) taken out of the rekordbox collection, "
                    f"{sum(done.deleted.values())} row(s) in all, each read back from the "
                    f"database: "
                    + "; ".join(f"{one.artist} - {one.title}" for one in done.rows)
                    + f". No file was touched: crate delete review offers each file to "
                    f"the Trash. Undo with a restore of session {done.session_id}"
                ),
            },
        ],
    )


def written(
    cfg,
    plan: removed.RemovedPlan,
    **kwargs: Any,
) -> removed.Removed:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return removed.apply_removed(
            cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg), **kwargs
        )
    finally:
        rb_writer.close_db(db)


__all__ = [
    "APPLIED",
    "CONFIRM_GATE",
    "GONE",
    "PARTIAL",
    "RECORDS_UNREADABLE",
    "build_removed",
    "facts",
    "payload",
    "sync_removed",
    "written",
]
