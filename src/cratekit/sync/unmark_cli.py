"""``sync.unmark``: put back the titles a pass's mark wrote, behind one gate (R-838).

The source system strips its swept prefix again when a run is abandoned. Here
``sync mark`` renames and this is the verb that renames back, so a mark written
by mistake is undone by the product and not by hand on the account.

THE RECORD SAYS WHAT A PASS MARKED, AND NOTHING ELSE DOES. ``sync mark`` keeps
:mod:`cratekit.sync.mark_record`, one entry per playlist a pass renamed, with
the title before and the title written. A playlist's title cannot say who put
the prefix on it, since the source system writes the same prefix and a person
can type it, so a playlist the record does not hold under the named pass is
never planned, and one named with ``--playlist`` is refused.

ONLY THE TITLE THE MARK WROTE IS PUT BACK. A playlist whose title on the
account is still exactly what the mark wrote is renamed to what it was before.
One retitled since, with the prefix or without it, is somebody's later decision
and is listed and left, and so is one the account no longer lists.

THE PASS IS NAMED, NOT FOUND. ``--pass`` takes the name the pass's list, batch
and intake file share, ``<run>_synced``, or the intake file ``sync mark`` was
handed, retired or not, from which that name is read. A name the record holds no
mark for is a plan of nothing, still gated, decided before the account is
listed or a credential is asked for, on ``sync mark``'s precedent.

THE PLAN IS SHOWN BEFORE ANYTHING IS RENAMED, and the run that carries out the
answer lists the account again and rechecks each title before its rename, so a
playlist retitled between the answer and the write is skipped and said.

IDEMPOTENT BY THE RECORD. Each rename that lands is stamped in the record as it
lands, so a second run finds every playlist already put back, plans nothing and
needs no account listing to say so.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import land_cli
from cratekit.sync import cli as sync_cli
from cratekit.sync import mark_cli, mark_record, playlists

_ORIGIN = ("sync.unmark",)

#: What a planned item carries, and what the apply turns it into.
UNMARK = "unmark"
UNMARKED = "unmarked"
SKIP = mark_cli.SKIP

#: Why a playlist the pass marked is not planned, one word each.
ALREADY_UNMARKED = "already-unmarked"
NOT_LISTED = mark_cli.NOT_LISTED
RENAMED_SINCE = "renamed-since-mark"
#: Another pass marked the playlist after this one did, so the prefix it
#: carries now is that pass's, and only that pass's unmark takes it off.
MARKED_AGAIN = "marked-again"
#: Why a planned playlist was not renamed after all: the recheck.
CHANGED_SINCE = mark_cli.CHANGED_SINCE

#: What the gate screen and the warning say about a pass the record has no mark of.
NO_MARK_SAID = (
    "the mark record holds no playlist this pass renamed on this library, so "
    "there is nothing to put back"
)


def build_unmark(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--pass",
        required=True,
        dest="pass_name",
        metavar="PASS",
        help=(
            "the pass whose marks to take off: its name, <run>_synced, or the "
            "intake file crate sync mark was given"
        ),
    )
    parser.add_argument(
        "--playlist",
        action="append",
        default=[],
        metavar="ID",
        help="only this playlist the pass marked, by its account identifier; repeatable",
    )
    parser.set_defaults(_handler=sync_unmark)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked",
        message,
        steps=steps,
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail=detail,
    )


def _pass_name(given: str) -> str:
    """The pass's name, read off an intake file's name when one was given."""
    name = land_cli.unretired_name(Path(given).name)
    if name.endswith(land_cli.INTAKE_SUFFIX):
        name = name[: -len(land_cli.INTAKE_SUFFIX)]
    if not name:
        raise _blocked(
            f"{given!r} names no pass, so there is no mark to put back",
            "pass the name crate intake missing --run printed, or the intake file "
            "crate sync mark was given",
            given=given,
        )
    return name


def _narrowed(
    found: tuple[mark_record.Marked, ...], named: list[str], name: str
) -> tuple[mark_record.Marked, ...]:
    """``--playlist`` narrows and never widens, and refuses what the pass did not mark."""
    if not named:
        return found
    held = {entry.playlist_id for entry in found}
    strangers = [identity for identity in dict.fromkeys(named) if identity not in held]
    if strangers:
        raise _blocked(
            f"pass {name} did not mark {', '.join(strangers)}, so this verb will not "
            f"rename it, whatever its title says; the prefix it carries was written "
            f"by something else",
            "name only playlists the pass marked, or leave --playlist out",
            not_marked=strangers,
            pass_name=name,
        )
    return tuple(entry for entry in found if entry.playlist_id in set(named))


def _later(entry: mark_record.Marked, every: tuple[mark_record.Marked, ...]) -> str:
    """The pass that marked the same playlist after ``entry``'s did, or ``""``.

    Timestamps are the record's own, written in one zone by one clock, so they
    order as text.
    """
    later = [
        other.pass_name
        for other in every
        if other.playlist_id == entry.playlist_id
        and other.pass_name != entry.pass_name
        and other.marked > entry.marked
    ]
    return later[-1] if later else ""


def _item(
    entry: mark_record.Marked,
    listed: dict[str, str] | None,
    every: tuple[mark_record.Marked, ...],
) -> dict[str, Any]:
    """One playlist the pass marked, decided against the account's titles now.

    ``listed`` is ``None`` when nothing asked for a listing, which is only ever
    a pass whose every mark has already been put back or superseded.
    """
    current = None if listed is None else listed.get(entry.playlist_id)
    base: dict[str, Any] = {
        "id": entry.playlist_id,
        "name": current or "",
        "marked_as": entry.to,
        "to": entry.name,
    }
    if entry.unmarked:
        return {
            **base,
            "action": SKIP,
            "reason": ALREADY_UNMARKED,
            "why": f"an unmark already put its title back, {entry.unmarked}",
        }
    later = _later(entry, every)
    if later:
        return {
            **base,
            "action": SKIP,
            "reason": MARKED_AGAIN,
            "why": (
                f"pass {later} marked it again after this one did, so the prefix "
                f"is that pass's to take off"
            ),
        }
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
            "why": "the account no longer lists it, so there is no title to put back",
        }
    if current == entry.name:
        # PUT BACK ALREADY, by hand or by an unmark whose stamp did not land.
        # The title is the one this verb would write, so there is nothing to do.
        return {
            **base,
            "action": SKIP,
            "reason": ALREADY_UNMARKED,
            "why": "its title is already the one it had before the mark",
        }
    if current != entry.to:
        how = (
            "still carries the prefix under another title"
            if playlists.is_swept_name(current)
            else "no longer carries the prefix"
        )
        return {
            **base,
            "action": SKIP,
            "reason": RENAMED_SINCE,
            "why": (
                f"it was retitled since the mark wrote {entry.to!r} and {how}, "
                f"so the later title is left as it is"
            ),
        }
    return {**base, "action": UNMARK}


def _payload(items: list[dict[str, Any]], *, name: str) -> dict[str, Any]:
    identity = {
        "kind": "sync-unmark",
        "pass": name,
        "unmarks": sorted(
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if item["action"] == UNMARK
        ),
    }
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            UNMARK: sum(1 for item in items if item["action"] == UNMARK),
            SKIP: sum(1 for item in items if item["action"] == SKIP),
        },
        "chunk": None,
    }


def _shown(payload: dict[str, Any], *, name: str, passes: tuple[str, ...]) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    shown: dict[str, Any] = {
        "pass": name,
        "put back on the account": [
            f"{item['marked_as']} -> {item['to']}"
            for item in payload["items"]
            if item["action"] == UNMARK
        ],
        "left alone": [
            f"{item['name'] or item['marked_as']}: {item['why']}"
            for item in payload["items"]
            if item["action"] == SKIP
        ],
    }
    if not payload["items"]:
        shown["nothing to put back"] = NO_MARK_SAID
        shown["passes the record holds"] = list(passes)
    return shown


def _failed_part_way(
    exc: Exception, landed: list[str], titles: dict[str, str], planned: list[str]
) -> CratekitError:
    """The failure, with what was already put back named in it.

    ``sync mark``'s rule: a refusal the account raised keeps its reason and its
    remedy, and anything else is this build's own defect and says so.
    """
    back = [titles.get(identity, identity) for identity in landed]
    said = (
        f"{len(back)} playlist(s) had their title put back before this failed: "
        + ", ".join(back)
        if back
        else "no playlist had its title put back before this failed"
    )
    detail = {
        "unmarked": list(landed),
        "still_marked": [identity for identity in planned if identity not in landed],
    }
    again = "run crate sync unmark again; a playlist already put back is skipped"
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
        f"{said}. The unmark step failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def sync_unmark(ctx) -> Envelope:
    cfg = sync_cli._load()
    name = _pass_name(str(ctx.args.pass_name))
    record = mark_record.MarkRecord(cfg)
    # THE RECORD FIRST, before the account is listed or a credential is asked
    # for. Neither can change which playlists the pass marked.
    every = record.all()
    found = _narrowed(
        tuple(entry for entry in every if entry.pass_name == name),
        list(ctx.args.playlist or ()),
        name,
    )
    standing = [entry for entry in found if not entry.unmarked and not _later(entry, every)]
    catalogue_found = None
    listed: dict[str, str] | None = None
    if standing:
        from cratekit.label import catalogue

        catalogue_found = catalogue.resolve(cfg)
        listed = playlists.account_names(catalogue_found)

    items = [_item(entry, listed, every) for entry in found]
    payload = _payload(items, name=name)
    option = ctx.gate.require(
        ctx.entry.gates[0],
        digest=payload["digest"],
        context=_shown(
            payload,
            name=name,
            passes=() if found else tuple(dict.fromkeys(e.pass_name for e in every)),
        ),
    )
    if not found:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "sync-unmark-no-mark", "message": f"{name}: {NO_MARK_SAID}"}],
        )
    by_id = {entry.playlist_id: entry for entry in found}
    planned = [item["id"] for item in items if item["action"] == UNMARK]
    if option != "apply" or not planned:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    from cratekit.modules.outbound import account

    # THE RECORD IS LOCKABLE BEFORE THE FIRST RENAME, so a stamp that cannot
    # land refuses while every title is still the mark's.
    record.ready()
    remote = account.resolve(cfg)
    titles = {identity: by_id[identity].to for identity in planned}
    landed: list[str] = []
    changed: list[str] = []
    try:
        # THE RECHECK, against a listing taken after the answer, read once.
        now = playlists.account_names(catalogue_found)
        for identity in planned:
            entry = by_id[identity]
            if now.get(identity) != entry.to:
                changed.append(identity)
                continue
            remote.rename_playlist(identity, entry.name)
            landed.append(identity)
            record.record_unmarked(name, identity)
    except Exception as exc:
        raise _failed_part_way(exc, landed, titles, planned) from exc

    done: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in items:
        if item["id"] in landed:
            done.append({**item, "action": UNMARKED})
        elif item["id"] in changed:
            done.append(
                {
                    **item,
                    "action": SKIP,
                    "reason": CHANGED_SINCE,
                    "why": (
                        "the account lists it under another title, or not at all, "
                        "since the plan was shown, so it was not renamed"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "sync-unmark-changed-since-plan",
                    "message": f"{item['marked_as']} changed on the account since the "
                    f"plan was shown and was not renamed",
                }
            )
        else:
            done.append(item)
    totals = {
        "count": len(done),
        UNMARKED: len(landed),
        SKIP: sum(1 for item in done if item["action"] == SKIP),
    }
    return ctx.envelope(
        data={**payload, "items": done, "totals": totals},
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = ["build_unmark", "sync_unmark"]
