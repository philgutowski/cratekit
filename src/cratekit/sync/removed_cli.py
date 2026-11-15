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
* the plan is shown, digested, and NOTHING IS WRITTEN: no row, no file, no
  account write, no record. Removing an offered row from the collection is
  U288's, behind its own gate, and the file reaches the Trash only through
  ``crate delete review``.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import removed

#: Nothing is offered, since a synced playlist was not read whole.
PARTIAL = "sync-removed-partial"

#: A downloaded playlist the account no longer lists.
GONE = "sync-removed-playlist-gone"

#: Session records that could not be read, so what a landing made may be unnamed.
RECORDS_UNREADABLE = "sync-removed-records-unreadable"

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


def sync_removed(ctx) -> Envelope:
    """Read every downloaded playlist again and answer each removed track. Writes nothing."""
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
    return ctx.envelope(
        data=payload(plan),
        outcome=Outcome.OK if plan.answers else Outcome.NO_OP,
        warnings=warnings_of(plan),
    )


__all__ = ["GONE", "PARTIAL", "RECORDS_UNREADABLE", "build_removed", "payload", "sync_removed"]
