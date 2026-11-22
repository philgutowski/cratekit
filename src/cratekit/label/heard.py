"""A label's dated playlist heard: merged into the year and removed (U123).

The other half of :mod:`cratekit.label.dated`. Its releases are the dated
plan's own rule, so the two never disagree. The record's ``heard`` list is
written LAST, under its lock, so a run that fails part way finishes on the
next. The merge adds before it removes, and a track the provider would not add
keeps the playlist. A track the year must not hold (U243), removed from the
library or pruned off the year, is never merged. With ``--release`` the named
releases' tracks come off while another is unheard. A removal is asked only of
a playlist the outbound ledger vouches for. The Record Labels tree in
rekordbox is never written (R39).

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import dated, sync_cli

if TYPE_CHECKING:
    from cratekit.modules.outbound import folders

_ORIGIN = ("label.heard",)

#: The per label key in ``label_sync.json``, the dated plan's own.
HEARD = dated.HEARD

#: What happens to the dated playlist on the account.
REMOVE = "remove"
TAKE_OFF = "take off"
KEEP = "keep"
ABSENT = "absent"

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
    """Every release the dated playlist ``<year> new <day>`` is for, heard or not:
    taken by a go on ``day``, in the catalogue, dated to ``year``."""
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
    #: The tracks this run puts in the year, all on a removal.
    merging: tuple[str, ...] = ()
    #: Those of ``merging`` the year does not hold yet, less ``tombstoned``.
    add: tuple[str, ...] = ()
    #: Those of ``merging`` the year must not hold (U243): removed or pruned.
    tombstoned: tuple[str, ...] = ()
    #: The year is the one the ledger records, so what is added is recorded on it.
    year_recorded: bool = False
    #: A dated playlist the ledger records by this name and the folder does not hold.
    stray_id: str = ""

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
                "id": self.dated_id or self.stray_id,
                "kind": "playlist",
                "name": self.name,
                "action": self.action,
                "tracks": len(self.tracks),
                **({"why": why} if (why := _why(self)) else {}),
            }
        )
        if self.year_id and (self.add or self.merging):
            from cratekit.modules.outbound import folders

            items.append(
                {
                    "id": self.year_id,
                    "kind": "playlist",
                    "name": folders.year_name(self.label, self.year),
                    "action": "add",
                    "add": len(self.add),
                    "already": len(self.merging) - len(self.add) - len(self.tombstoned),
                    **({"removed from the library": len(self.tombstoned)} if self.tombstoned else {}),
                }
            )
        return items

    def payload(self) -> dict[str, Any]:
        return dated.gate_plan(
            digest_of(self.identity()),
            self.items(),
            {
                "heard": len(self.newly),
                "add": len(self.add),
                "remove": int(self.action == REMOVE),
                "take off": len(self.merging) if self.action == TAKE_OFF else 0,
                "writes": self.writes,
            },
        )


def _why(planned: HeardPlan) -> str:
    if planned.action == ABSENT and planned.stray_id:
        return (
            f"the label's folder holds no playlist by this name and the ledger records "
            f"one made here, {planned.stray_id}: if it is still on the account it is "
            f"outside the folder, and is left for you to remove by hand"
        )
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
    if planned.tombstoned and not planned.year_id:
        return (
            "every release of it is heard and every track it holds was removed from "
            "the library or taken off the year, so nothing goes in the year and it is "
            "removed"
        )
    return (
        "every release of it is heard, so its tracks go in the year, less any the "
        "year must not hold, and it is removed"
    )


def _refused(reason: str, message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(reason, message, steps=steps, scope=Scope.RUN, origin=_ORIGIN, detail=detail)


def _one_named(inside: Mapping[str, str], name: str, *also: str) -> str:
    """The one playlist in the folder carrying ``name`` or ``also``, empty for none,
    refused for two."""
    matching = sorted(pid for pid, title in inside.items() if title in (name, *also))
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
    from cratekit.modules.outbound import folders, ledger

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
        # ONE THE LEDGER RECORDS OUTSIDE THE FOLDER is said; the releases are heard.
        return replace(base, stray_id=shape.dated.get(name, ""))
    tracks = tuple(account.playlist_tracks(dated_id))
    if unheard:
        # A TRACK AN UNHEARD RELEASE ALSO CARRIES STAYS.
        def tracks_of(releases: Sequence[str]) -> set[str]:
            return {
                track
                for release in releases
                for track in (catalogue.by_release.get(release) or ("", ()))[1]
            }

        leaving = tracks_of(target) - tracks_of(unheard)
        merging = tuple(one for one in dict.fromkeys(tracks) if one in leaving)
        action = TAKE_OFF if merging else KEEP
    else:
        merging = tuple(dict.fromkeys(tracks))
        action = REMOVE
    if action in (REMOVE, TAKE_OFF) and not ledger.product_made(cfg, dated_id):
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
    planned = replace(base, action=action, dated_id=dated_id, tracks=tracks, merging=merging)
    if not merging:
        return planned
    recorded = shape.years.get(year)
    taken_away = set(catalogue.tombstoned) | (
        set(recorded.pruned) if recorded is not None else set()
    )
    if all(one in taken_away for one in merging):
        # EVERY TRACK WAS REMOVED (U243), so no year, which is never built, is asked.
        return replace(planned, tombstoned=merging)
    year_name = folders.year_name(catalogue.name, year)
    # THE RECORDED YEAR FIRST, then one by its name or pre U242 marked name.
    year_id = recorded.remote_id if recorded is not None and recorded.remote_id in inside else ""
    year_id = year_id or _one_named(inside, year_name, folders.MARK_PREFIX + year_name)
    if not year_id:
        raise _refused(
            "label-heard-no-year-playlist",
            f"the label's folder holds no {year_name!r}, so the tracks of {name!r} have "
            f"nowhere to go and nothing was written",
            f"run crate label playlists {catalogue.name} to build the year, then run "
            f"label heard again",
            name=year_name,
        )
    have = set(account.playlist_tracks(year_id))
    # A TRACK THE LIBRARY REMOVED IS NEVER ADDED (U243), but counted held.
    return replace(
        planned,
        year_id=year_id,
        year_recorded=recorded is not None and recorded.remote_id == year_id,
        add=tuple(one for one in merging if one not in have and one not in taken_away),
        tombstoned=tuple(one for one in merging if one in taken_away and one not in have),
    )


@dataclass
class Heard:
    """What an apply wrote, for the report and for a failure part way."""

    added: int = 0
    #: Tracks of ``merging`` the year must hold and does not, once the adds are done.
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
    return dated.refused_part_way(
        exc, wrote, again, detail, failed="Hearing the playlist", origin=_ORIGIN
    )


def record_heard(cfg: config.Config, label_id: str, releases: Sequence[str]) -> int:
    """Add ``releases`` to the label's heard list, under the record's lock. Returns how many."""
    if not releases:
        return 0
    with sync_cli.record_lock(cfg, "marking releases heard"):
        document = sync_cli.load_record(cfg)
        before = dated.heard(document, label_id)
        fresh = [one for one in dict.fromkeys(releases) if one not in before]
        if not fresh:
            return 0
        document["labels"].setdefault(label_id, {})[HEARD] = sorted({*before, *fresh})
        sync_cli.write_record(cfg, document)
    return len(fresh)


def apply(cfg: config.Config, account, planned: HeardPlan) -> Heard:
    """Write what the plan names, the account first and the record last."""
    from cratekit.modules.outbound import folders, ledger

    done = Heard()
    try:
        held: set[str] = set(planned.merging) - set(planned.add)
        for start in range(0, len(planned.add), folders.CHUNK):
            chunk = planned.add[start : start + folders.CHUNK]
            answered = set(account.add_tracks(planned.year_id, chunk))
            done.added += sum(1 for one in chunk if one in answered)
            held |= answered
            # RECORDED ON THE YEAR as the year build's adds are.
            if planned.year_recorded:
                ledger.record_label_tracks(
                    cfg,
                    planned.label_id,
                    planned.year,
                    added=[one for one in chunk if one in answered],
                    refused=[one for one in chunk if one not in answered],
                )
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
