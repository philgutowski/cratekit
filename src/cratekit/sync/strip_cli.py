"""``sync.strip``: take the retired ``DOWNLOADED `` prefix off every account playlist (U242).

Decided by Phillip on 2026-11-11: the prefix dates from downloading playlists
by hand, Cratekit now records what it took in its own record, and the prefix
is to go everywhere. This is the one time verb that takes it off.

THE RECORD HOLDS A PLAYLIST BEFORE ITS TITLE CHANGES. The apply runs the
migration (:mod:`cratekit.sync.taken_cli`) first, holding every prefixed
playlist as taken, and then confirms from the record itself that it holds each
planned playlist before that playlist's rename. A playlist the record does not
hold is never renamed, so a stripped playlist is never offered as new.

ONE RENAME PER PREFIXED PLAYLIST, to its title less the prefix (every copy of
it, and the spaces around what is left). Refused, per playlist and named, when
what is left is empty, or names, ignoring case, another playlist the account
lists or another title this strip would write: two playlists of one title are
two a person cannot tell apart. A refused one keeps its prefix and stays taken.

THE PLAN IS SHOWN BEFORE ANYTHING IS RENAMED, every rename and every refusal on
the gate, and the run that carries out the answer lists the account again and
renames only a playlist whose title is still the one shown.

PACED BY THE PROVIDER GATE AND RESUMABLE. Every rename goes through the account
seam, so the gate's interval, cooldown and call ceiling apply. A stop part way,
the ceiling's included, keeps its own reason and remedy and names what was
stripped, and a run started again plans only what still carries the prefix.

EVERY OLD TITLE CAN BE PUT BACK. Each rename is recorded in the mark record
under the pass :data:`PASS` before it is made, the old title and the new, so
``crate sync unmark --pass prefix-strip`` restores the old title by the rule
it restores any mark by: only while the account still carries the title the
record says was written.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.sync import cli as sync_cli
from cratekit.sync import mark_record, playlists, taken_cli

_ORIGIN = ("sync.strip",)

#: The pass every strip rename is recorded under, so one unmark restores them.
PASS = "prefix-strip"

#: What a planned item carries, and what the apply turns it into.
STRIP = "strip"
STRIPPED = "stripped"
SKIP = "skip"

#: Why a prefixed playlist is left with its prefix, one word each.
COLLIDES = "collides"
NOTHING_LEFT = "nothing-left"
#: Why a planned playlist was not renamed after all: the recheck.
CHANGED_SINCE = "changed-since-plan"

NOTHING_SAID = "no playlist the account lists carries the prefix, so there is nothing to strip"


def build_strip(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--playlist",
        action="append",
        default=[],
        metavar="ID",
        help="only this prefixed playlist, by its account identifier; repeatable",
    )
    parser.set_defaults(_handler=sync_strip)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked",
        message,
        steps=steps,
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail=detail,
    )


def plan(listed: Mapping[str, str]) -> list[dict[str, Any]]:
    """One item per prefixed playlist the account lists, decided against every other title. Pure."""
    prefixed = {
        identity: name for identity, name in listed.items() if playlists.is_swept_name(name)
    }
    others: dict[str, str] = {}
    for identity, name in sorted(listed.items(), key=lambda one: (one[1], one[0])):
        if identity not in prefixed:
            others.setdefault(name.strip().casefold(), name)
    wanted = {identity: playlists.untaken_name(name) for identity, name in prefixed.items()}
    writes: dict[str, list[str]] = {}
    for identity, to in wanted.items():
        writes.setdefault(to.casefold(), []).append(identity)
    items: list[dict[str, Any]] = []
    for identity, name in sorted(prefixed.items(), key=lambda one: (one[1], one[0])):
        to = wanted[identity]
        base = {"id": identity, "name": name, "to": to}
        if not to:
            items.append(
                {
                    **base,
                    "action": SKIP,
                    "reason": NOTHING_LEFT,
                    "why": "nothing is left of its title without the prefix",
                }
            )
            continue
        clash = others.get(to.casefold())
        twins = sorted(prefixed[one] for one in writes[to.casefold()] if one != identity)
        if clash is not None or twins:
            said = (
                f"another playlist on the account is titled {clash!r}"
                if clash is not None
                else f"{', '.join(repr(one) for one in twins)} would be stripped to the same title"
            )
            items.append(
                {
                    **base,
                    "action": SKIP,
                    "reason": COLLIDES,
                    "why": f"{said}, so it keeps its prefix; rename one of them by hand",
                }
            )
            continue
        items.append({**base, "action": STRIP})
    return items


def _narrowed(items: list[dict[str, Any]], named: list[str], listed: Mapping[str, str]) -> list[dict[str, Any]]:
    """``--playlist`` narrows and never widens, and refuses what is not prefixed."""
    if not named:
        return items
    held = {item["id"] for item in items}
    strangers = [identity for identity in dict.fromkeys(named) if identity not in held]
    if strangers:
        raise _blocked(
            f"{', '.join(strangers)} is not a playlist the account lists with the prefix, "
            f"so there is nothing of it to strip; nothing was renamed",
            "name only prefixed playlists, by the identifiers the plan lists, or leave "
            "--playlist out",
            not_prefixed=strangers,
            titles={one: listed.get(one, "") for one in strangers},
        )
    wanted = set(named)
    return [item for item in items if item["id"] in wanted]


def _payload(items: list[dict[str, Any]], named: list[str]) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "kind": "sync-strip",
        "strips": sorted((item["id"], item["name"], item["to"]) for item in items if item["action"] == STRIP),
    }
    if named:
        identity["only"] = sorted(set(named))
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            STRIP: sum(1 for item in items if item["action"] == STRIP),
            SKIP: sum(1 for item in items if item["action"] == SKIP),
        },
        "chunk": None,
    }


def _shown(payload: dict[str, Any]) -> dict[str, Any]:
    shown: dict[str, Any] = {
        "renamed on the account": [
            f"{item['name']} -> {item['to']}"
            for item in payload["items"]
            if item["action"] == STRIP
        ],
        "left with the prefix": [
            f"{item['name']}: {item['why']}"
            for item in payload["items"]
            if item["action"] == SKIP
        ],
        "first": (
            "every prefixed playlist is recorded as taken in Cratekit's own record, so "
            "none is offered as new once its prefix is gone"
        ),
        "undone by": f"crate sync unmark --pass {PASS}",
    }
    if not payload["items"]:
        shown["nothing to strip"] = NOTHING_SAID
    return shown


def _failed_part_way(
    exc: Exception, landed: list[str], titles: dict[str, str], planned: list[str]
) -> CratekitError:
    """The failure, with what was already stripped named in it.

    ``sync unmark``'s rule: a refusal the account raised, the provider gate's
    call ceiling among them, keeps its reason, its remedy and its steps, and
    anything else is this build's own defect and says so.
    """
    done = [titles.get(identity, identity) for identity in landed]
    said = (
        f"{len(done)} playlist(s) had the prefix taken off before this stopped: "
        + ", ".join(done)
        if done
        else "no playlist had the prefix taken off before this stopped"
    )
    detail = {
        "stripped": list(landed),
        "still_prefixed": [identity for identity in planned if identity not in landed],
    }
    again = (
        "run crate sync strip again; a playlist already stripped is not planned again, "
        "and every one is recorded as taken"
    )
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{said}. The strip failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def sync_strip(ctx) -> Envelope:
    cfg = sync_cli._load()
    record = mark_record.MarkRecord(cfg)
    # THE RECORD FIRST, read under its lock, so one that cannot be read or
    # locked refuses before the account is listed or a credential asked for.
    record.ready()
    from cratekit.label import catalogue

    catalogue_found = catalogue.resolve(cfg)
    listed = playlists.account_names(catalogue_found)
    named = list(dict.fromkeys(str(one) for one in (ctx.args.playlist or ())))
    items = _narrowed(plan(listed), named, listed)
    payload = _payload(items, named)
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_shown(payload))
    planned = [item["id"] for item in items if item["action"] == STRIP]
    if not items:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "sync-strip-nothing", "message": NOTHING_SAID}],
        )
    if option != "apply" or not planned:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    # THE LEDGER BEFORE ANY TITLE CHANGES. Every prefixed playlist the account
    # lists is held as taken, the refused ones too, and the record is read
    # back: a planned playlist it does not hold refuses the whole strip here,
    # while every title is still prefixed.
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
    unheld = [identity for identity in planned if identity not in held]
    if unheld:
        raise _blocked(
            f"the record does not hold {', '.join(unheld)} as taken after recording it, so "
            f"stripping its prefix would offer it as new; nothing was renamed",
            "repair the mark record, run crate sync taken, then strip again",
            not_held=unheld,
        )

    from cratekit.modules.outbound import account

    remote = account.resolve(cfg)
    by_id = {item["id"]: item for item in items}
    titles = {identity: by_id[identity]["name"] for identity in planned}
    landed: list[str] = []
    changed: list[str] = []
    try:
        # THE RECHECK, against a listing taken after the answer, read once.
        now = playlists.account_names(catalogue_found)
        for identity in planned:
            item = by_id[identity]
            if now.get(identity) != item["name"]:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME, so a rename that lands is always one
            # the unmark can put back. One recorded and never made reads to
            # the unmark as a title already put back, which it is.
            record.record_marked(PASS, {identity: (item["name"], item["to"])})
            remote.rename_playlist(identity, item["to"])
            landed.append(identity)
    except Exception as exc:
        raise _failed_part_way(exc, landed, titles, planned) from exc

    done: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in items:
        if item["id"] in landed:
            done.append({**item, "action": STRIPPED})
        elif item["id"] in changed:
            done.append(
                {
                    **item,
                    "action": SKIP,
                    "reason": CHANGED_SINCE,
                    "why": (
                        "the account lists it under another title, or not at all, since "
                        "the plan was shown, so it was not renamed"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "sync-strip-changed-since-plan",
                    "message": f"{item['name']} changed on the account since the plan was "
                    f"shown and was not renamed",
                }
            )
        else:
            done.append(item)
    totals = {
        "count": len(done),
        STRIPPED: len(landed),
        SKIP: sum(1 for item in done if item["action"] == SKIP),
    }
    return ctx.envelope(
        data={**payload, "items": done, "totals": totals},
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = ["PASS", "build_strip", "plan", "sync_strip"]
