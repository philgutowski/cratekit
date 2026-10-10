"""A label's dated playlist heard: merged into the year and removed (U123).

U117 (:mod:`cratekit.label.dated`) keeps the releases a go took apart from the
ones already heard, in a playlist beside the year, ``<Label> <year> new
<date>``. This module is the other half: once the author has heard them, it
records them heard, puts the dated playlist's tracks in the year playlist, and
removes the dated playlist from the account.

THE RELEASES OF A DATED PLAYLIST are decided by the dated plan's own rule, so
the two can never disagree about which playlist a release is in: every release
a go took for the label on that local day, ``dated.taken_by_goes``, that the
catalogue dates to that year. One named on the command line that is not among
them is refused by name before the gate, and nothing is written.

HEARD IS A LIST OF RELEASE IDENTIFIERS per label in ``label_sync.json``,
``labels.<id>.heard``, and this module is the only writer. It is written LAST,
after the account, under the record's own lock, so a run that fails part way
leaves the releases unheard and a second run finishes what is left. A second
run over a playlist already merged plans nothing.

THE MERGE ADDS BEFORE IT REMOVES. Every track the dated playlist holds that the
year does not is added to the year first, and the dated playlist is removed
only once every track it held is in the year. A track the provider would not
add leaves the dated playlist where it is, said, rather than removed with the
one copy of that track. The year keeps every confirmed track as it does today.

SOME OF THE RELEASES, NOT ALL. Naming releases with ``--release`` marks those
heard. While another release of the playlist is still unheard, the named ones'
tracks are taken off the dated playlist, after the adds, and the playlist
stays; the run that hears the last one removes it.

A REMOVAL IS ASKED ONLY OF A PLAYLIST THE OUTBOUND LEDGER VOUCHES FOR, which is
one the dated plan created (``ledger.record_label_dated``). One reused by its
name was made by somebody else and the plan refuses it before the gate.

THE RECORD LABELS TREE IN REKORDBOX IS NOT WRITTEN, and the verb says so on
every run. It is the catalogue tree, which ``tree_registry.cutover_trees``
keeps on the xml bridge for good (R39), so the database writer ``inbox
rotate`` uses refuses it, and nothing writes a dated playlist there to merge.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import dated, sync_cli
from cratekit.modules.outbound import folders, ledger

_ORIGIN = ("label.heard",)

#: The per label key in ``label_sync.json``, the dated plan's own.
HEARD = dated.HEARD

#: What happens to the dated playlist on the account.
REMOVE = "remove"
TAKE_OFF = "take off"
KEEP = "keep"
ABSENT = "absent"

#: How many tracks one add carries, the year build's own chunk.
CHUNK = folders.CHUNK

#: What every run says about the rekordbox half.
TREE_SAID = (
    "the Record Labels tree in rekordbox is not changed: it is the catalogue "
    "tree, which stays on the xml bridge (R39), and nothing writes a dated "
    "playlist there to merge"
)

_YEAR = re.compile(r"^\d{4}$")


def _invalid(message: str, **detail: Any) -> CratekitError:
    return refuse(
        "label-heard-invalid",
        message,
        remedy=Remedy.FIX_COMMAND_LINE,
        steps=("name the label, the four digit year and the ISO date of the dated playlist",),
        origin=_ORIGIN,
        detail=detail,
    )


def checked_year(raw: str) -> str:
    """The four digit year, or the refusal a typo earns."""
    text = str(raw or "").strip()
    if not _YEAR.match(text):
        raise _invalid(f"{raw!r} is not a four digit year", year=str(raw))
    return text


def checked_day(raw: str) -> str:
    """The ISO date, or the refusal a typo earns."""
    text = str(raw or "").strip()
    try:
        return date.fromisoformat(text).isoformat()
    except ValueError as exc:
        raise _invalid(f"{raw!r} is not an ISO date, for example 2026-10-09", day=str(raw)) from exc


def releases_of(
    document: Mapping[str, Any], catalogue: folders.LabelCatalogue, year: str, day: str
) -> tuple[str, ...]:
    """Every release the dated playlist ``<year> new <day>`` is for, heard or not.

    The dated plan's rule: taken by a go on ``day``, in the catalogue, dated
    to ``year``.
    """
    took = dated.taken_by_goes(document, catalogue.label_id)
    return tuple(
        sorted(
            identity
            for identity, taken_on in took.items()
            if taken_on == day and (catalogue.by_release.get(identity) or ("",))[0] == year
        )
    )


@dataclass(frozen=True, slots=True)
class HeardPlan:
    """One dated playlist heard, against the record and the account as they are."""

    label_id: str
    label: str
    year: str
    day: str
    name: str
    #: Every release the dated playlist is for.
    releases: tuple[str, ...]
    #: The releases this run says were heard.
    target: tuple[str, ...]
    #: Those of ``target`` the record does not already hold as heard.
    newly: tuple[str, ...]
    #: Releases of the playlist still unheard once this run is done.
    unheard: tuple[str, ...]
    action: str = ABSENT
    dated_id: str = ""
    year_id: str = ""
    #: Every track the dated playlist holds.
    tracks: tuple[str, ...] = ()
    #: The tracks this run puts in the year: all of them on a removal, the
    #: named releases' on a take off.
    merging: tuple[str, ...] = ()
    #: Those of ``merging`` the year does not hold yet.
    add: tuple[str, ...] = ()

    @property
    def writes(self) -> bool:
        return bool(self.newly or self.add or self.action in (REMOVE, TAKE_OFF))

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every write, and the playlists it lands on."""
        return {
            "kind": "label-heard",
            "label": self.label_id,
            "playlist": [self.name, self.dated_id, self.action],
            "year": [self.year, self.year_id],
            "heard": list(self.newly),
            "add": list(self.add),
            "merging": list(self.merging),
        }

    def items(self) -> list[dict[str, Any]]:
        heard_before = set(self.target) - set(self.newly)
        items: list[dict[str, Any]] = [
            {
                "id": release,
                "kind": "release",
                "action": (
                    "mark heard"
                    if release in self.newly
                    else "already heard"
                    if release in heard_before
                    else "left unheard"
                ),
            }
            for release in self.releases
        ]
        items.append(
            {
                "id": self.dated_id,
                "kind": "playlist",
                "name": self.name,
                "action": self.action,
                "tracks": len(self.tracks),
                **({"why": _why(self)} if _why(self) else {}),
            }
        )
        if self.add or self.merging:
            items.append(
                {
                    "id": self.year_id,
                    "kind": "playlist",
                    "name": folders.year_name(self.label, self.year),
                    "action": "add",
                    "add": len(self.add),
                    "already": len(self.merging) - len(self.add),
                }
            )
        return items

    def payload(self) -> dict[str, Any]:
        items = self.items()
        return {
            "digest": digest_of(self.identity()),
            "items": items,
            "totals": {
                "count": len(items),
                "heard": len(self.newly),
                "add": len(self.add),
                "remove": int(self.action == REMOVE),
                "take off": len(self.merging) if self.action == TAKE_OFF else 0,
                "writes": self.writes,
            },
            "chunk": None,
        }


def _why(planned: HeardPlan) -> str:
    if planned.action == ABSENT:
        return "the label's folder on the account holds no playlist by this name"
    if planned.action == KEEP:
        return (
            f"{len(planned.unheard)} release(s) of it are still unheard and none of "
            f"its tracks belongs to the releases named"
        )
    if planned.action == TAKE_OFF:
        return (
            f"{len(planned.unheard)} release(s) of it are still unheard, so the named "
            f"releases' tracks come off it and it stays"
        )
    return "every release of it is heard, so its tracks go in the year and it is removed"


def _refused(reason: str, message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        reason,
        message,
        steps=steps,
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail=detail,
    )


def _one_named(inside: Mapping[str, str], name: str) -> str:
    """The one playlist in the folder carrying ``name``, empty for none, refused for two."""
    matching = sorted(pid for pid, title in inside.items() if title == name)
    if len(matching) > 1:
        raise _refused(
            "label-heard-ambiguous",
            f"the label's folder holds {len(matching)} playlists named {name!r}, so "
            f"which one is meant is not something a name decides, and nothing was written",
            "rename or merge the extra playlists on the account, then run label heard again",
            name=name,
            playlists=matching,
        )
    return matching[0] if matching else ""


def plan(
    cfg: config.Config,
    catalogue: folders.LabelCatalogue,
    account,
    document: Mapping[str, Any],
    *,
    year: str,
    day: str,
    named: Sequence[str] = (),
) -> HeardPlan:
    """Decide what hearing one dated playlist writes, or refuse before anything is."""
    name = dated.dated_name(catalogue.name, year, day)
    releases = releases_of(document, catalogue, year, day)
    if not releases:
        raise _refused(
            "label-heard-no-releases",
            f"no go took a release of {catalogue.name} dated {year} on {day}, so no "
            f"dated playlist named {name!r} is this product's, and nothing was written",
            "check the year and the date against the dated playlist's name on the account",
            label_id=catalogue.label_id,
            year=year,
            day=day,
        )
    asked = list(dict.fromkeys(str(one).strip() for one in named if str(one).strip()))
    outside = [one for one in asked if one not in releases]
    if outside:
        raise _refused(
            "label-heard-not-in-playlist",
            f"{', '.join(outside)} {'is' if len(outside) == 1 else 'are'} not a release "
            f"of the dated playlist {name!r}, whose releases are {', '.join(releases)}, "
            f"so nothing was marked heard and nothing was written",
            "name only releases of this dated playlist, or none to mark all of them heard",
            outside=outside,
            releases=list(releases),
        )
    heard = dated.heard(document, catalogue.label_id)
    target = tuple(asked) if asked else releases
    newly = tuple(one for one in target if one not in heard)
    unheard = tuple(one for one in releases if one not in heard and one not in target)
    base = HeardPlan(
        label_id=catalogue.label_id,
        label=catalogue.name,
        year=year,
        day=day,
        name=name,
        releases=releases,
        target=target,
        newly=newly,
        unheard=unheard,
    )

    shape = ledger.label_shape(cfg, catalogue.label_id)
    inside = account.folder_playlists(shape.folder_id) if shape.folder_id else {}
    dated_id = _one_named(inside, name)
    if not dated_id:
        return base
    tracks = tuple(account.playlist_tracks(dated_id))
    if unheard:
        named_tracks = {
            track for release in target for track in (catalogue.by_release.get(release) or ("", ()))[1]
        }
        merging = tuple(one for one in dict.fromkeys(tracks) if one in named_tracks)
        action = TAKE_OFF if merging else KEEP
    else:
        merging = tuple(dict.fromkeys(tracks))
        action = REMOVE
    if not ledger.product_made(cfg, dated_id):
        raise _refused(
            "label-heard-not-product-made",
            f"the outbound ledger does not record {name!r} ({dated_id}) as a playlist "
            f"this product created, so it is not this verb's to take anything off or "
            f"remove, and nothing was written",
            "merge and remove the playlist by hand in the provider's own player, then "
            "run label heard again to mark its releases heard",
            playlist_id=dated_id,
            name=name,
        )
    year_name = folders.year_name(catalogue.name, year)
    # THE RECORDED YEAR FIRST, when the folder still holds it, so a year the
    # mark retitled with the source system's prefix is still the year.
    recorded = shape.years.get(year)
    year_id = recorded.remote_id if recorded is not None and recorded.remote_id in inside else ""
    year_id = year_id or _one_named(inside, year_name)
    if merging and not year_id:
        raise _refused(
            "label-heard-no-year-playlist",
            f"the label's folder holds no {year_name!r}, so the tracks of {name!r} have "
            f"nowhere to go and nothing was written",
            f"run crate label playlists {catalogue.name} to build the year, then run "
            f"label heard again",
            name=year_name,
        )
    have = set(account.playlist_tracks(year_id)) if year_id else set()
    return replace(
        base,
        action=action,
        dated_id=dated_id,
        year_id=year_id,
        tracks=tracks,
        merging=merging,
        add=tuple(one for one in merging if one not in have),
    )


@dataclass
class Heard:
    """What an apply wrote, for the report and for a failure part way."""

    added: int = 0
    #: Tracks of ``merging`` the year does not hold once the adds are done.
    missing: list[str] = field(default_factory=list)
    taken_off: int = 0
    removed: bool = False
    #: True when a removal was planned and held back by ``missing``.
    kept: bool = False
    recorded: int = 0


def _failed_part_way(exc: Exception, done: Heard, planned: HeardPlan) -> CratekitError:
    """The failure, with what was already written named in it."""
    if done.added or done.taken_off or done.removed:
        wrote = (
            f"before this failed {done.added} track(s) were added to the year, "
            f"{done.taken_off} taken off {planned.name!r}"
            + (f", and {planned.name!r} was removed" if done.removed else "")
            + "; no release was marked heard"
        )
    else:
        wrote = "nothing was written before this failed"
    again = (
        "run crate label heard again; a track already in the year is not added twice "
        "and a playlist already removed is not asked for again"
    )
    detail = {
        "label_id": planned.label_id,
        "playlist": planned.name,
        "added": done.added,
        "taken_off": done.taken_off,
        "removed": done.removed,
    }
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. Hearing the playlist failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        steps=(again,),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def record_heard(cfg: config.Config, label_id: str, releases: Sequence[str]) -> int:
    """Add ``releases`` to the label's heard list, under the record's lock. Returns how many."""
    if not releases:
        return 0
    with sync_cli.record_lock(cfg, "marking releases heard"):
        document = sync_cli.load_record(cfg)
        held = document["labels"].setdefault(label_id, {})
        listed = held.get(HEARD)
        before = [one for one in listed if isinstance(one, str) and one] if isinstance(
            listed, list
        ) else []
        fresh = [one for one in releases if one not in before]
        if not fresh:
            return 0
        held[HEARD] = sorted({*before, *fresh})
        sync_cli.write_record(cfg, document)
    return len(fresh)


def apply(cfg: config.Config, account, planned: HeardPlan) -> Heard:
    """Write what the plan names, the account first and the record last."""
    done = Heard()
    try:
        held: set[str] = set(planned.merging) - set(planned.add)
        for start in range(0, len(planned.add), CHUNK):
            chunk = planned.add[start : start + CHUNK]
            answered = set(account.add_tracks(planned.year_id, chunk))
            done.added += sum(1 for one in chunk if one in answered)
            held |= answered
        done.missing = [one for one in planned.merging if one not in held]
        if planned.action == REMOVE:
            if done.missing:
                done.kept = True
            else:
                account.remove_playlist(planned.dated_id)
                done.removed = True
                ledger.forget_label_dated(cfg, planned.label_id, planned.dated_id)
        elif planned.action == TAKE_OFF:
            leaving = tuple(one for one in planned.merging if one in held)
            if leaving:
                done.taken_off = len(account.remove_tracks(planned.dated_id, leaving))
        done.recorded = record_heard(cfg, planned.label_id, planned.newly)
    except Exception as exc:
        raise _failed_part_way(exc, done, planned) from exc
    return done


__all__ = [
    "ABSENT",
    "HEARD",
    "KEEP",
    "REMOVE",
    "TAKE_OFF",
    "TREE_SAID",
    "Heard",
    "HeardPlan",
    "apply",
    "checked_day",
    "checked_year",
    "plan",
    "record_heard",
    "releases_of",
]
