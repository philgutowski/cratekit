"""``crate sync removed``: each downloaded track taken off its playlist on the account (U287).

The rules are :mod:`cratekit.sync.removed`'s; this is the order a person meets them in:

* the session log is read once, before anything is opened or asked;
* the database is read on a disposable copy, never the live file;
* the not found record is read before the account is asked, so an unreadable
  one refuses first (U320);
* the account is asked only when something was downloaded, and the other
  synced playlists and hearts only once a removal is found; the record is
  then written once;
* each synced playlist read whole is kept (R-1716, :mod:`cratekit.sync.removed_kept`),
  so a run the call ceiling or the hour's line stops is continued by running
  it again, which reads only what is left and any playlist the account's
  listing shows written since;
* a plan that offers nothing ends there, writing nothing;
* otherwise the backup acknowledgment, then the gate ``sync.removed.confirm``
  over the digested plan (U288, R-1830);
* only ``apply`` opens the database to write, where the engine replans and
  refuses ``decision-stale`` on any change. No file is touched; ``crate delete
  review`` offers them later from the session record.

``--retire`` (U320) reads every synced playlist, lists each unlisted one whose
id answered not found at the gate ``sync.removed.retire``, and writes the
record only on ``retire``. It makes no removal plan.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, analysis_store, jobs, rb_writer, session, tree_registry
from cratekit.core.cause import Cause, Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import removed, removed_kept, unavailable

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

#: The hearts listed short only by what the provider withholds, read whole (U320).
HEARTS_WITHHELD = "sync-removed-hearts-withheld"

#: A synced playlist the account answered not found for, not yet retired (U320).
UNAVAILABLE = "sync-removed-playlist-unavailable"

#: A synced playlist retired by the record, which holds nothing and stops nothing (U320).
RETIRED = "sync-removed-playlist-retired"

#: The explicit gate a person retires a playlist the account answered not found for behind (U320).
RETIRE_GATE = "sync.removed.retire"

#: What ``--retire`` retired.
RETIRED_NOW = "sync-removed-retired-now"

#: The command that retires them now. It reads every synced playlist the
#: held reads do not hold, two calls or more each, so a first one on a large
#: account needs raised ceilings, or runs again until it finishes (R-1716).
RETIRE_COMMAND = "crate --calls N --calls-per-hour M sync removed --retire"


def build_removed(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--retire",
        action="store_true",
        help=(
            "read every synced playlist, list each one the account no longer lists "
            "whose id answered not found, and retire them behind the explicit gate "
            "sync.removed.retire, so they stop holding back every removal; writes "
            "Cratekit's own record only, never the account or the database"
        ),
    )
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
            "playlists retired": sum(1 for one in plan.listings if one.state == removed.RETIRED),
            "memberships renumbered": plan.renumbered,
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
    withheld = [one for one in plan.listings if one.state == removed.WITHHELD]
    if withheld:
        found.append(
            {
                "code": HEARTS_WITHHELD,
                "message": f"{withheld[0].name}: {withheld[0].why}",
            }
        )
    seen = [
        one
        for one in plan.listings
        if one.noted is not None and not one.noted.is_retired
    ]
    if seen:
        found.append(
            {
                "code": UNAVAILABLE,
                "message": (
                    f"{len(seen)} synced playlist(s) the account no longer lists whose id "
                    f"answered not found: "
                    + "; ".join(
                        f"{one.account}"
                        + (f" ({one.name})" if one.name else "")
                        + f", seen unavailable on {one.noted.seen()}"
                        for one in seen
                        if one.noted is not None
                    )
                    + f". Each is retired by itself once it answers not found again a "
                    f"day after it first did, or now with `{RETIRE_COMMAND}`, behind the "
                    f"explicit gate {RETIRE_GATE}"
                ),
            }
        )
    retired = [one for one in plan.listings if one.state == removed.RETIRED]
    if retired:
        found.append(
            {
                "code": RETIRED,
                "message": (
                    f"{len(retired)} synced playlist(s) retired, holding nothing and "
                    f"stopping nothing: "
                    + "; ".join(
                        f"{one.account}" + (f" ({one.name})" if one.name else "") + f", {one.why}"
                        for one in retired
                    )
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


def facts(
    plan: removed.RemovedPlan,
    kept: removed_kept.SyncedReads | None = None,
    synced: tuple[str, ...] = (),
) -> dict[str, Any]:
    """What the gate puts in front of the items: each offered row, then what is written.

    A plan that took any synced playlist from held reads says so (R-1716), so
    the person answering knows how old what it rests on may be.
    """
    held = (
        {"held reads": kept.from_held(synced)} if kept is not None and kept.used else {}
    )
    return {
        **held,
        "offered": [
            f"{one.artist} - {one.title}, taken off {', '.join(one.removed_from)}: {one.file}"
            for one in plan.offered
        ],
        "kept or left": len(plan.answers) - len(plan.offered),
        "memberships renumbered": plan.renumbered,
        "writes": (
            "each offered row out of the rekordbox collection, with every membership, "
            "cue, history entry, analysis file row and mixer row naming it, as "
            "rekordbox's Remove from Collection does, and the tracks after it in each "
            "playlist it left moved up one place for each removed track before them, as "
            "rekordbox numbers them; no other "
            "row, no playlist row and no file. crate delete review then offers each file "
            "to the Trash"
        ),
    }


def _gate(entry, name: str = CONFIRM_GATE) -> Any:
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise LookupError(f"{entry.name} declares no {name} gate")


def _stopped(cause: Cause, kept: removed_kept.SyncedReads) -> Cause:
    """A park met while reading, said with how many synced playlists the store now holds (R-1716).

    COUNTED FROM THE STORE, whatever run read them, so a park before any read
    still says what the next run will not read again. The reason stands, so
    the dispatcher still reads it as the ceiling's or the hour's and names the
    command that continues.
    """
    standing = 0 if kept.unkept else kept.standing()
    if kept.unkept:
        said = (
            f"; the {len(kept.kept)} synced playlist(s) read whole on this run could not "
            f"be held ({kept.unkept}), so running it again reads them again"
        )
    else:
        said = (
            f"; {standing} synced playlist(s) read whole are held, {len(kept.kept)} of them "
            f"read on this run, each for {removed_kept.hours(removed_kept.HELD_FOR)} after "
            f"its read while the account lists it unchanged, so running crate sync "
            f"removed again, with or without a higher ceiling, reads only the rest; "
            f"nothing is offered from a run stopped part way"
        )
    return dataclasses.replace(
        cause, message=f"{cause.message}{said}", detail={**dict(cause.detail or {}), "kept": standing}
    )


def _read_synced(
    cfg, found, *, every: bool, record_now: bool = True
) -> tuple[dict[str, removed.Listing], removed_kept.SyncedReads | None]:
    """The account's reads, recorded in the not found record (U320), and the held reads.

    The downloaded playlists first; the rest and the hearts only once a removal
    is found, or with ``every``. The record is read before any call, so an
    unreadable one costs none, and written once after, unless ``record_now`` is
    false, so that ``--retire``'s abort writes nothing to it. Each playlist read
    whole is kept as it goes (R-1716), and the store is written on the way out
    whatever stops the run.
    """
    record = unavailable.UnavailableRecord(cfg)
    sightings = record.read()
    moment = unavailable.now()
    reads: dict[str, removed.Listing] = {}
    if not found and not every:
        return reads, None
    from cratekit.label import catalogue

    account = catalogue.resolve(cfg)
    kept = removed_kept.SyncedReads(cfg, moment)
    try:
        reads = _read_through(
            cfg, account, found, every=every, kept=kept, sightings=sightings, moment=moment
        )
    except jobs.Parked as exc:
        kept.flush()
        raise jobs.Parked(_stopped(exc.cause, kept)) from exc
    finally:
        kept.flush()
    if record_now:
        record.update(removed.noted(reads))
    return reads, kept


def _read_through(
    cfg, account, found, *, every: bool, kept: removed_kept.SyncedReads, sightings, moment
) -> dict[str, removed.Listing]:
    """:func:`_read_synced`'s reads, each playlist through ``kept``."""
    from cratekit.modules.outbound import pairs

    listed = removed.account_listing(account)
    recorded = removed.recorded_contents(cfg)
    # WHAT CRATEKIT CALLS EACH ONE, so an unlisted playlist is still named;
    # the pair store's names join once it is read, below.
    names = {one.account: one.name for one in found if one.name}
    asked = {
        "sightings": sightings,
        "moment": moment,
        "listed": listed,
        "recorded": recorded,
        "names": names,
        "kept": kept,
    }
    reads = removed.read_account(account, [one.account for one in found], **asked)
    if every or removed.removals(found, reads):
        paired = pairs.PairStore(cfg).all()
        names.update(
            {key: one.name for key, one in paired.items() if one.name and key not in names}
        )
        others = [
            one
            for one in removed.synced(
                cfg,
                found,
                paired=frozenset(paired),
                swept_now=removed.job_playlists(cfg),
                listed=listed,
            )
            if one not in reads
        ]
        reads.update(removed.read_account(account, others, **asked))
        if not every:
            reads[removed.HEARTS] = removed.read_hearts(account)
    return reads


def _kept_warnings(
    kept: removed_kept.SyncedReads | None, reads: dict[str, removed.Listing]
) -> list[dict[str, str]]:
    """What the held reads say, over the synced playlists this run answered (R-1716)."""
    if kept is None:
        return []
    return kept.warnings(account for account in reads if account != removed.HEARTS)


def retirable(reads: dict[str, removed.Listing]) -> list[removed.Listing]:
    """Each synced playlist the account no longer lists whose id answered not found on this read.

    THIS READ'S ANSWER, NEVER THE RECORD'S ALONE, and never one already retired.
    """
    return [
        one
        for one in reads.values()
        if one.not_found and one.noted is not None and not one.noted.is_retired
    ]


def retire(ctx, cfg) -> Envelope:
    """``--retire``: retire behind the explicit gate each playlist :func:`retirable` names (U320).

    Records nothing in the not found record until the gate answers
    ``retire``, then every read and each named playlist as retired by a
    person. The held reads (R-1716) are written as it reads, abort or not.
    It writes Cratekit's records only.
    """
    records, _unreadable = session.scan_log(cfg)
    found = removed.downloaded(cfg, records)
    reads, kept = _read_synced(cfg, found, every=True, record_now=False)
    named = retirable(reads)
    items = [
        {
            "action": "retire",
            "account": one.account,
            "name": one.name,
            "first seen unavailable": unavailable.day(one.noted.first),
            "seen unavailable": one.noted.seen(),
        }
        for one in named
        if one.noted is not None
    ]
    data = {
        # THE PLAYLISTS NAMED, NOT THE DATES, so drives either side of midnight
        # bind to one plan.
        "digest": digest_of(
            {
                "kind": "sync-removed-retire",
                "playlists": [{key: item[key] for key in ("account", "name")} for item in items],
            }
        ),
        "items": items,
        "totals": {"count": len(items), "playlists read": len(reads)},
        "chunk": None,
    }
    # A PLAYLIST THIS READ COULD NOT ASK IS SAID, so an outage is not a clean list.
    unasked = [
        one
        for one in reads.values()
        if (one.state in removed.NOT_WHOLE or one.state == removed.GONE) and not one.not_found
    ]
    warnings = _kept_warnings(kept, reads) + (
        [
            {
                "code": PARTIAL,
                "message": (
                    f"{len(unasked)} synced playlist(s) could not be read whole, or whose id "
                    f"failed other than not found, are not offered for retirement: "
                    + "; ".join(f"{one.name or one.account} ({one.why})" for one in unasked)
                ),
            }
        ]
        if unasked
        else []
    )
    if not named:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    context = {
        "retire": [
            f"{item['account']}" + (f" ({item['name']})" if item["name"] else "")
            + f": the account no longer lists it and its id answered not found on "
            f"{item['seen unavailable']}"
            for item in items
        ],
        "writes": (
            "Cratekit's own record of these playlists as retired, so they hold no track "
            "and stop no offer of crate sync removed; nothing on the account, nothing in "
            "the database and no file. A playlist retired that opens again is read again"
        ),
    }
    if ctx.gate.require(_gate(ctx.entry, RETIRE_GATE), plan=data, context=context) != "retire":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    moment = unavailable.now()
    unavailable.UnavailableRecord(cfg).update(
        {
            **removed.noted(reads),
            **{
                one.account: unavailable.retired_by_person(one.noted, moment)
                for one in named
                if one.noted is not None
            },
        }
    )
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": RETIRED_NOW,
                "message": (
                    f"{len(named)} synced playlist(s) retired: "
                    + ", ".join(item["account"] for item in items)
                    + ". Run crate sync removed again to plan without them"
                ),
            }
        ],
    )


def sync_removed(ctx) -> Envelope:
    """Answer each removed track, then, behind the gate, take the offered rows out of the collection."""
    cfg = sync_cli._load()
    if getattr(ctx.args, "retire", False):
        return retire(ctx, cfg)
    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    records, unreadable = session.scan_log(cfg)
    found = removed.downloaded(cfg, records)
    with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
        reads, kept = _read_synced(cfg, found, every=False)
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
    warnings = warnings_of(plan) + _kept_warnings(kept, reads)
    if not plan.offered:
        return ctx.envelope(
            data=data,
            outcome=Outcome.OK if plan.answers else Outcome.NO_OP,
            warnings=warnings,
        )
    # BEFORE THE GATE (R-733), and only once something is offered.
    session.assert_backup_acknowledged(cfg)
    synced = tuple(account for account in reads if account != removed.HEARTS)
    if (
        ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan, kept, synced))
        != "apply"
    ):
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
                    f"{sum(done.deleted.values())} row(s) in all and {done.renumbered} "
                    f"playlist membership(s) after them renumbered, each read back from the "
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
    "APPLIED", "CONFIRM_GATE", "GONE", "HEARTS_WITHHELD", "PARTIAL", "RECORDS_UNREADABLE",
    "RETIRED", "RETIRED_NOW", "RETIRE_COMMAND", "RETIRE_GATE", "UNAVAILABLE", "build_removed",
    "facts", "payload", "retirable", "retire", "sync_removed", "written"
]
