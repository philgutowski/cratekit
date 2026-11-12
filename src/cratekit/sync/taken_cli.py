"""``sync.taken``: record every playlist already taken in Cratekit's own record (U242).

The ``DOWNLOADED `` prefix is retired, decided by Phillip on 2026-11-11. Until
now a playlist was known to be taken, finished with, by its title, and most of
the account's prefixed playlists were marked by hand, so only their title says
so. This verb is the migration that moves that knowledge into the record
(:mod:`cratekit.sync.mark_record`'s taken ledger) before anything takes the
prefix off, so no state exists in which a playlist taken today reads as new.

WHAT IT RECORDS. Every account playlist whose title carries the prefix, and
every mark of the prefix the record already holds that no unmark put back,
under the pass that wrote it and its own time, which is what filing reads a
year from. The cursor's playlists are COUNTED AND NOT COPIED: the cursor is
already the product's own record and keeps every one of them out of a sync,
and copying one whose pass still owes tracks would take it out of ``sync
mark``'s plan as though it were finished.

IDEMPOTENT. A playlist already held keeps the entry that holds it, so a second
run records nothing and says so. ``crate sync strip`` runs this same step
first, inside its own apply, so a strip never depends on a person having run
this one.

THE PLAN IS SHOWN BEFORE ANYTHING IS RECORDED, the account listed once, and
nothing is written to the account at all.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from cratekit.cli.output import Envelope, digest_of, timestamp
from cratekit.core import config
from cratekit.core.cause import Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import mark_record, playlists
from cratekit.sync.watermarks import WatermarkStore

#: What a planned item carries, and what the apply turns it into.
TAKE = "take"
TAKEN = "taken"
HELD = "held"


def build_taken(parser, entry) -> None:
    del entry
    parser.set_defaults(_handler=sync_taken)


def entries(
    marks: Sequence[mark_record.Marked], listed: Mapping[str, str], *, now: str
) -> list[mark_record.Taken]:
    """What the migration holds as taken: the record's standing prefix marks, then every prefixed title.

    A MARK OF THE PREFIX is one whose written title carries it, so a strip's
    own record, which writes the title without it, is never read as one. The
    latest standing mark of a playlist is the one kept, with its pass and its
    time. A prefixed title no mark covers is held as found, by the migration.
    """
    found: dict[str, mark_record.Taken] = {}
    for mark in sorted(marks, key=lambda one: (one.marked, one.pass_name)):
        if mark.unmarked or not playlists.is_swept_name(mark.to):
            continue
        found[mark.playlist_id] = mark_record.Taken(
            playlist_id=mark.playlist_id,
            name=playlists.untaken_name(mark.name),
            by=mark.pass_name,
            how=mark_record.BY_PASS,
            at=mark.marked or now,
        )
    for identity, name in sorted(listed.items(), key=lambda one: (one[1], one[0])):
        if identity in found or not playlists.is_swept_name(name):
            continue
        found[identity] = mark_record.Taken(
            playlist_id=identity,
            name=playlists.untaken_name(name),
            by=mark_record.MIGRATION,
            how=mark_record.FOUND_PREFIXED,
            at=now,
        )
    return list(found.values())


def migrate(
    cfg: config.Config, listed: Mapping[str, str], *, now: str | None = None
) -> tuple[list[mark_record.Taken], tuple[str, ...]]:
    """Record every playlist the migration holds as taken. Returns them and the ids newly held."""
    record = mark_record.MarkRecord(cfg)
    wanted = entries(record.ready(), listed, now=now or timestamp())
    return wanted, record.take(wanted)


def _cursor(cfg: config.Config) -> frozenset[str]:
    existing = WatermarkStore(cfg).read(playlists.SOURCE_ID)
    return frozenset(existing.swept) if existing is not None else frozenset()


def _payload(
    wanted: list[mark_record.Taken], held: frozenset[str], cursor: frozenset[str]
) -> dict[str, Any]:
    items = [
        {
            "id": one.playlist_id,
            "name": one.name,
            "by": one.by,
            "how": one.how,
            "action": HELD if one.playlist_id in held else TAKE,
        }
        for one in wanted
    ]
    taking = sorted(item["id"] for item in items if item["action"] == TAKE)
    covered = {one.playlist_id for one in wanted} | held
    return {
        "digest": digest_of({"kind": "sync-taken", "take": taking}),
        "items": items,
        "totals": {
            "count": len(items),
            TAKE: len(taking),
            HELD: len(items) - len(taking),
            "cursor": len(cursor),
            "cursor_only": len(cursor - covered),
        },
        "chunk": None,
    }


def _shown(payload: dict[str, Any]) -> dict[str, Any]:
    totals = payload["totals"]
    return {
        "recorded as taken": [
            f"{item['name'] or item['id']} ({item['how']}, {item['by']})"
            for item in payload["items"]
            if item["action"] == TAKE
        ],
        "already held": totals[HELD],
        "held by the sync cursor and not copied": totals["cursor_only"],
        "written": "Cratekit's own record only; nothing on the account is changed",
    }


def sync_taken(ctx) -> Envelope:
    cfg = sync_cli._load()
    record = mark_record.MarkRecord(cfg)
    # THE RECORD FIRST, read under its lock, so one that cannot be read or
    # locked refuses before the account is listed or a credential asked for.
    marks = record.ready()
    from cratekit.label import catalogue

    listed = playlists.account_names(catalogue.resolve(cfg))
    wanted = entries(marks, listed, now=timestamp())
    held = record.taken_ids()
    payload = _payload(wanted, held, _cursor(cfg))
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_shown(payload))
    taking = [one for one in wanted if one.playlist_id not in held]
    if option != "apply" or not taking:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    fresh = set(record.take(taking))
    items = [
        {**item, "action": TAKEN} if item["id"] in fresh else item for item in payload["items"]
    ]
    totals = {**payload["totals"], TAKEN: len(fresh)}
    return ctx.envelope(
        data={**payload, "items": items, "totals": totals},
        outcome=Outcome.OK if fresh else Outcome.NO_OP,
    )


__all__ = ["build_taken", "entries", "migrate", "sync_taken"]
