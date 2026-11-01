"""``crate sync twins``: every downloaded custom playlist gets its permanent rekordbox twin (U149).

The backfill, run once and safe to run again. It lists every root folder on the
account titled as a year, and in each every playlist the account lists as the
author's own whose name carries ``DOWNLOADED ``, leaving out a label's, a set's,
a mirrored one and any already paired. For each it plans the twin,
``Custom Playlists <year> / <name less the prefix>``, matches every account
track to a library row (``sync/twins.py`` says how), and names each track the
twin will not hold. One explicit gate shows every twin and every miss; the
approved write makes the folders and twins in one guarded commit, reads them
back, and marks each pair, so ``crate sync pair`` keeps the two one list from
then on.

A SECOND RUN PLANS NOTHING. Every playlist the first run made a twin for is
paired, and a paired playlist is counted and never planned, so the second run
opens no gate and ends NO_OP.

THE ORDER IS THE OTHER DATABASE WRITERS': the backup acknowledgment before
anything is read (R-733), the plan on a handle opened to read and closed, the
gate over the digested plan, the write on a handle opened with write intent
that reads the folders, names and rows again and refuses any that moved.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import twins

#: The gate, explicit: a write to the live library's playlist tree.
APPROVE_GATE = "sync.twins.approve"

#: The notes the verb carries on its warnings channel.
NOTHING = "sync-twins-nothing"
MADE = "sync-twins-made"
LEFT = "sync-twins-left"
MISSING = "sync-twins-missing"
SHORT = "sync-twins-listing-short"


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.set_defaults(_handler=sync_twins)


def _gate(entry):
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPROVE_GATE!r}")


def planned(cfg: config.Config) -> twins.Backfill:
    """Read the account, then plan over the library through a handle opened to read and closed."""
    from cratekit.label import catalogue
    from cratekit.modules.outbound import account, ledger, pairs
    from cratekit.sync import playlists

    found = catalogue.resolve(cfg)
    own = {one.playlist_id: str(one.name or "") for one in playlists._listed_or_refuse(found)}
    excluded = (
        ledger.label_playlist_ids(cfg)
        | ledger.label_dated_ids(cfg)
        | ledger.set_playlist_ids(cfg)
        | ledger.mirror_playlist_ids(cfg)
    )
    paired = frozenset(pairs.PairStore(cfg).all())
    remote = account.resolve(cfg)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return twins.plan_backfill(
            cfg, db, remote=remote, found=found, own=own, excluded=excluded, paired=paired
        )
    finally:
        rb_writer.close_db(db)


def written(cfg: config.Config, approved: twins.Backfill) -> twins.Written:
    """Write the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return twins.write(cfg, db, approved, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)


def _notes(plan: twins.Backfill) -> list[dict[str, str]]:
    """What a person reads beside the counts, whatever the answer."""
    notes: list[dict[str, str]] = []
    if plan.left:
        notes.append(
            {
                "code": LEFT,
                "message": (
                    f"{len(plan.left)} downloaded playlist(s) get no twin this run: "
                    + "; ".join(f"{one.account_name}: {one.why}" for one in plan.left)
                ),
            }
        )
    missing = [(one, miss) for one in plan.made for miss in one.misses]
    if missing:
        notes.append(
            {
                "code": MISSING,
                "message": (
                    f"{len(missing)} account track(s) are not in their twin, and the next "
                    f"crate sync pair queues each one the library lacks: "
                    + "; ".join(f"{one.name}: {miss.said()}" for one, miss in missing)
                ),
            }
        )
    short = [one for one in plan.made if not one.whole]
    if short:
        notes.append(
            {
                "code": SHORT,
                "message": (
                    f"the account withheld tracks of {len(short)} playlist(s), so each is "
                    f"paired with no snapshot and its first crate sync pair adds only: "
                    + ", ".join(one.account_name for one in short)
                ),
            }
        )
    return notes


def sync_twins(ctx) -> Envelope:
    """Plan every missing twin, ask, then make them and mark their pairs."""
    cfg = sync_cli._load()
    spec = _gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)
    plan = planned(cfg)
    data = twins.payload(plan)
    notes = _notes(plan)
    if not plan.writes:
        # NOTHING TO MAKE, NO QUESTION, so a second run over a backfilled
        # account opens no gate.
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *notes,
                {
                    "code": NOTHING,
                    "message": (
                        f"no downloaded custom playlist in a year folder lacks its twin "
                        f"({plan.paired} already paired), so nothing was written"
                    ),
                },
            ],
        )
    if ctx.gate.require(spec, plan=data, context=twins.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=notes)
    done = written(cfg, plan)
    twins.assert_read_back(plan, done)
    marked = twins.pair_backfilled(cfg, plan, done)
    totals: dict[str, Any] = {
        **data["totals"],
        "made": len(done.twins),
        "folders_made": len(done.folders_made),
        "added": done.added,
        "paired": marked,
    }
    return ctx.envelope(
        data={**data, "totals": totals},
        warnings=[
            *notes,
            {
                "code": MADE,
                "message": (
                    f"{len(done.twins)} twin(s) made and paired in rekordbox, "
                    f"{done.added} track(s) in all"
                    + (
                        f", in {len(done.folders_made)} new folder(s): "
                        + ", ".join(done.folders_made)
                        if done.folders_made
                        else ""
                    )
                    + f"; session {done.session_id}"
                ),
            },
        ],
    )


__all__ = ["APPROVE_GATE", "build", "planned", "sync_twins", "written"]
