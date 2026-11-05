"""An edit made on the account to a mirrored genre playlist, told apart and decided (U201).

THE MIRROR WAS ONE WAY. ``crate organize`` copies every genre folder of the
routing tree onto the account (U147) and keeps each copy equal to rekordbox, so
a track a person moved on the account was put back at the next refresh. Since
U201 the mirror remembers, per playlist, the account tracks both sides held
when it last finished it, the SNAPSHOT (``ledger.MirrorPlaylist.agreed``), and
reads each playlist three ways: the snapshot, the account now and rekordbox
now. This module decides, from those alone, which track a person changed on the
account and what the library should do about it. It reads nothing and writes
nothing, so every rule below is drivable without a database, an account or a
gate.

ONE BASE, SO PER PLAYLIST A CHANGE HAS ONE SIDE. A track in the snapshot that
the account no longer holds was taken off on the account; one the account holds
that the snapshot does not was added there. The same reading of rekordbox gives
its changes. A track is never both added and removed on one side of one
playlist between two refreshes, as far as either side can show.

A GENRE TRACK IS READ ACROSS THE WHOLE TREE, by its PLACE: the band playlists
(an energy band, a bucket's single sub or a style, what ``routing.energy_sub``
files a track into) that hold it, on each side and in the snapshot. A track
taken off ``Deep House Low`` and added to ``Tech House Mid`` on the account is
one edit, a MOVE. One taken off its band and added nowhere in the tree is
UNFILED, Phillip's answer of 2026-11-04: its genre and energy are cleared and it
reads as unplaced. One added to a with vox or genre sub playlist of another
folder, with no band of its own added, takes that FOLDER's genre with its
energy kept, since such a playlist is read as its parent band is. A track taken
off a with vox or genre sub playlist alone is no edit: those are derived, and
the mirror puts it back as it always did.

THE MOST RECENT CHANGE WINS, U198's brief's rule, as far as a time can be read.
Where both sides changed one track's place differently since the snapshot:

* an ADDITION BEATS A REMOVAL, since neither side ever records when a track was
  taken off, so the removal's time is unknown and the addition keeps the track;
* two ADDITIONS follow the later of the account's added date and rekordbox's
  membership time, and with either unknown, or the two equal, rekordbox's place
  stands, the conservative call, recorded with U201. Every such call is named.

HELD IS NEITHER CARRIED NOR UNDONE. A track added on the account to two band
playlists at once, one taken off its band and left in a derived playlist only,
one the library owns no row for (queued for download by U204) or owns two rows
for, and one whose playlist the account listed short, is held: the library is
not changed, the account is left as it is, and the gate names it. Nothing a
person did is lost to a refresh that could not read what they meant.

A PLAYLIST NEVER AGREED READS ITS ACCOUNT SIDE AS ITS SNAPSHOT, so every
difference on it is rekordbox's and nothing in the library changes: the first
refresh after U201 lands, and a playlist the mirror made since. A SHORT LISTING
CARRIES NO EDIT, since a track it leaves out is no evidence that a person took
it off; each track it reads differently from the snapshot is held.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime

#: What becomes of one track a person changed on the account.
#: Rekordbox's change stands and the mirror writes it, as it always did.
REKORDBOX = "rekordbox"
#: Both sides made the same change; nothing is carried and nothing undone.
AGREED = "agreed"
#: Carried: the track takes the band playlist the account put it in.
MOVE = "move"
#: Carried: the track takes the account folder's genre, its energy kept.
FOLDER = "folder"
#: Carried: the track leaves the tree, its genre and energy cleared.
UNFILE = "unfile"
#: Neither carried nor undone, and named.
HELD = "held"

#: The outcomes the library takes.
CARRIED = frozenset({MOVE, FOLDER, UNFILE})


@dataclass(frozen=True, slots=True)
class Place:
    """One mirrored genre playlist: its account title, rekordbox names and kind.

    ``primary`` is a band playlist, a place routing files a track's band into;
    anything else in a genre folder, a with vox, genre sub or genre Favorites
    playlist, is additive.
    """

    title: str
    folder: str
    playlist: str
    primary: bool


@dataclass(frozen=True, slots=True)
class Mirrored:
    """One mirrored genre playlist read three ways, by account track.

    ``account`` is what the account holds now, ``rekordbox`` the account tracks
    the rekordbox playlist matched, and ``agreed`` the snapshot, ``None`` for a
    playlist never agreed. ``account_added`` and ``rekordbox_added`` are each
    track's added time on that side as text, absent when unknown.
    """

    place: Place
    account: frozenset[str] = frozenset()
    rekordbox: frozenset[str] = frozenset()
    agreed: frozenset[str] | None = None
    short: bool = False
    account_added: Mapping[str, str] = field(default_factory=dict)
    rekordbox_added: Mapping[str, str] = field(default_factory=dict)

    @property
    def base(self) -> frozenset[str]:
        """The snapshot, or the account side for a playlist never agreed."""
        return self.account if self.agreed is None else self.agreed


@dataclass(frozen=True, slots=True)
class Hold:
    """What the mirror leaves as it is on one playlist.

    ``keep`` is account tracks it never takes off, ``skip`` rekordbox's tracks
    it never adds, both because the track's own edit is carried or held.
    """

    keep: frozenset[str] = frozenset()
    skip: frozenset[str] = frozenset()

    @property
    def tracks(self) -> frozenset[str]:
        return self.keep | self.skip


@dataclass(frozen=True, slots=True)
class Decision:
    """One track a person changed on the account, and what becomes of it.

    ``to`` is the place a MOVE or FOLDER takes, ``content_id`` the library row
    a carried edit changes, and the three place tuples are titles, sorted.
    """

    track: str
    outcome: str
    why: str
    to: Place | None = None
    content_id: str = ""
    was: tuple[str, ...] = ()
    account: tuple[str, ...] = ()
    rekordbox: tuple[str, ...] = ()
    #: Every genre playlist read in full, ``(folder, title, held on the
    #: account)``, which the snapshot takes once the library took the edit.
    settle: tuple[tuple[str, str, bool], ...] = ()

    def item(self) -> dict[str, object]:
        shown: dict[str, object] = {
            "track": self.track,
            "outcome": self.outcome,
            "was": list(self.was),
            "account": list(self.account),
            "rekordbox": list(self.rekordbox),
            "why": self.why,
        }
        if self.to is not None:
            shown["to"] = self.to.title
        if self.content_id:
            shown["content_id"] = self.content_id
        return shown


@dataclass(frozen=True, slots=True)
class Decided:
    """Every track a person changed on the account, and every playlist's hold."""

    decisions: tuple[Decision, ...] = ()
    holds: Mapping[str, Hold] = field(default_factory=dict)

    @property
    def carried(self) -> tuple[Decision, ...]:
        return tuple(one for one in self.decisions if one.outcome in CARRIED)

    def hold(self, title: str) -> Hold:
        return self.holds.get(title, Hold())


def moment(text: str) -> datetime | None:
    """A time as either side writes it, with its zone, or ``None`` when it is unknown.

    The account's is ISO 8601; rekordbox writes ``YYYY-MM-DD HH:MM:SS.SSS
    +00:00``, a space before the zone. A time with no zone is unknown, since
    comparing it with one that has a zone would be a guess.
    """
    value = str(text or "").strip()
    if not value:
        return None
    if len(value) > 6 and value[-6] in "+-" and value[-7] == " ":
        value = value[:-7] + value[-6:]
    try:
        found = datetime.fromisoformat(value)
    except ValueError:
        return None
    return found if found.tzinfo is not None else None


def _titles(places: Iterable[Place]) -> tuple[str, ...]:
    return tuple(sorted(place.title for place in places))


def _intent(
    was: frozenset[Place], now: frozenset[Place], was_more: frozenset[Place], now_more: frozenset[Place]
) -> tuple[str, Place | None, str] | None:
    """What the account side did to one track's place, or ``None`` for nothing.

    ``was`` and ``now`` are its band places in the snapshot and on the account,
    ``was_more`` and ``now_more`` its additive ones.
    """
    added = now - was
    removed = was - now
    added_more = now_more - was_more
    if not added and not removed and not added_more:
        return None
    if len(added) == 1:
        (place,) = added
        return MOVE, place, f"put in {place.title} on the account"
    if len(added) > 1:
        return (
            HELD,
            None,
            f"added on the account to {len(added)} band playlists at once "
            f"({', '.join(_titles(added))}), so which one it belongs in is not "
            f"something the account says",
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {', '.join(_titles(removed))} on the account, left in {place.title}"
    if removed and len(now) > 1:
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and still in "
            f"{len(now)} band playlists there, so which one it belongs in is not "
            f"something the account says",
        )
    if not added_more:
        if not now_more:
            return UNFILE, None, (
                f"taken off {', '.join(_titles(removed))} on the account and added to "
                f"no other genre playlist"
            )
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and left only in "
            f"{', '.join(_titles(now_more))}, which is derived from a band, so where "
            f"it goes is not something the account says",
        )
    folders = sorted({place.folder for place in added_more})
    if len(folders) > 1:
        return (
            HELD,
            None,
            f"added on the account to playlists of {len(folders)} genres at once "
            f"({', '.join(_titles(added_more))}), so which genre it takes is not "
            f"something the account says",
        )
    if not removed and folders[0] in {place.folder for place in now}:
        # A DERIVED PLAYLIST OF ITS OWN GENRE: the band already says the
        # genre, so this is no edit, and the mirror writes rekordbox's side.
        return None
    (place,) = sorted(
        (one for one in added_more if one.folder == folders[0]), key=lambda one: one.title
    )[:1]
    return FOLDER, place, f"put in {place.title} on the account, read as the genre {place.folder}"


def _agrees(kind: str, to: Place | None, now: frozenset[Place]) -> bool:
    """Whether rekordbox's place is the one the account's edit asks for."""
    if kind == MOVE:
        return now == frozenset({to})
    if kind == UNFILE:
        return not now
    if kind == FOLDER:
        return bool(now) and all(place.folder == to.folder for place in now)
    return False


def decide(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]]
) -> Decided:
    """Decide every track a person changed on the account across one genre tree. Pure.

    ``owner`` is each account track to the library rows matched to it, which a
    carried edit needs exactly one of.
    """
    unread: set[str] = set()
    for one in playlists:
        if one.short and one.agreed is not None:
            unread |= one.account ^ one.agreed
    tracks = sorted(
        set().union(*((one.base | one.account | one.rekordbox) for one in playlists))
        if playlists
        else set()
    )

    def placed(track: str, side: str, primary: bool) -> frozenset[Place]:
        return frozenset(
            one.place
            for one in playlists
            if one.place.primary is primary and track in getattr(one, side)
        )

    decisions: list[Decision] = []
    for track in tracks:
        was, now = placed(track, "base", True), placed(track, "account", True)
        there = placed(track, "rekordbox", True)
        shown = {
            "was": _titles(was),
            "account": _titles(now),
            "rekordbox": _titles(there),
        }
        if track in unread:
            decisions.append(
                Decision(
                    track,
                    HELD,
                    "a playlist it is in listed short on the account, so what a "
                    "person did to it there cannot be read",
                    **shown,
                )
            )
            continue
        intent = _intent(
            was, now, placed(track, "base", False), placed(track, "account", False)
        )
        if intent is None:
            continue
        kind, to, why = intent
        if kind == HELD:
            decisions.append(Decision(track, HELD, why, **shown))
            continue
        if there != was:
            if _agrees(kind, to, there):
                decisions.append(
                    Decision(track, AGREED, f"{why}, and rekordbox made the same change", to=to, **shown)
                )
                continue
            if kind == UNFILE:
                decisions.append(
                    Decision(
                        track,
                        REKORDBOX,
                        f"{why}, and placed in {', '.join(_titles(there))} in rekordbox: "
                        f"an addition beats a removal, whose time is never known",
                        **shown,
                    )
                )
                continue
            if there:
                said = _later(playlists, track, to, there - was)
                if said is not None:
                    decisions.append(Decision(track, REKORDBOX, f"{why}, {said}", **shown))
                    continue
                why = (
                    f"{why}, later than rekordbox placed it in "
                    f"{', '.join(_titles(there))}"
                )
            else:
                why = (
                    f"{why}, and taken out of the tree in rekordbox: an addition beats "
                    f"a removal, whose time is never known"
                )
        rows = sorted({str(one) for one in owner.get(track, ()) if str(one)})
        if not rows:
            decisions.append(
                Decision(
                    track,
                    HELD,
                    f"{why}, and the library holds no track matched to it, so nothing "
                    f"is changed and it stays on the account; queuing it for download "
                    f"is U204's",
                    to=to,
                    **shown,
                )
            )
            continue
        if len(rows) > 1:
            decisions.append(
                Decision(
                    track,
                    HELD,
                    f"{why}, and {len(rows)} library rows match it, so which one "
                    f"changes is not something the account says",
                    to=to,
                    **shown,
                )
            )
            continue
        decisions.append(
            Decision(
                track,
                kind,
                why,
                to=to,
                content_id=rows[0],
                settle=tuple(
                    (one.place.folder, one.place.title, track in one.account)
                    for one in playlists
                    if not one.short
                ),
                **shown,
            )
        )
    return Decided(decisions=tuple(decisions), holds=_holds(playlists, decisions))


def _later(
    playlists: Sequence[Mirrored], track: str, to: Place | None, placed: frozenset[Place]
) -> str | None:
    """``None`` when the account's addition is the later, else why rekordbox's stands."""
    on_account = next(
        (one.account_added.get(track, "") for one in playlists if one.place == to), ""
    )
    in_rekordbox = (
        next(
            (one.rekordbox_added.get(track, "") for one in playlists if one.place in placed),
            "",
        )
        if len(placed) == 1
        else ""
    )
    account_at, rekordbox_at = moment(on_account), moment(in_rekordbox)
    there = ", ".join(_titles(placed)) or "another band"
    if account_at is None or rekordbox_at is None:
        return (
            f"and placed in {there} in rekordbox; the time of one of the two is "
            f"unknown, so rekordbox's place stands"
        )
    if account_at > rekordbox_at:
        return None
    return (
        f"and placed in {there} in rekordbox at {rekordbox_at.isoformat()}, not "
        f"earlier than the account's {account_at.isoformat()}, so rekordbox's place stands"
    )


def _holds(playlists: Sequence[Mirrored], decisions: Iterable[Decision]) -> dict[str, Hold]:
    """Each playlist's hold: every carried or held track left as the account has it."""
    held = {one.track for one in decisions if one.outcome in CARRIED or one.outcome == HELD}
    holds: dict[str, Hold] = {}
    for one in playlists:
        keep = frozenset(track for track in held if track in one.account and track not in one.rekordbox)
        skip = frozenset(track for track in held if track in one.rekordbox and track not in one.account)
        if keep or skip:
            holds[one.place.title] = Hold(keep=keep, skip=skip)
    return holds


def agreed_after(
    base: Iterable[str] | None, after: Iterable[str], held: Iterable[str]
) -> frozenset[str]:
    """The snapshot a playlist takes once the mirror finished it.

    ``base`` is the snapshot it has, ``None`` for none, ``after`` the account
    tracks it holds once the mirror's writes landed, and ``held`` the tracks
    its hold covers. A held track keeps the snapshot's word on it, so an edit
    held reads the same way at the next refresh, and an edit the library took
    reads as the word the library step settled; every other track is agreed as
    the account holds it, which is rekordbox's word once the mirror wrote it,
    and a removal the account refused stays agreed so the next refresh asks it
    again.
    """
    held = frozenset(held)
    now = frozenset(after)
    before = now if base is None else frozenset(base)
    return frozenset(track for track in now if track not in held) | frozenset(
        track for track in before if track in held
    )


__all__ = [
    "AGREED",
    "CARRIED",
    "FOLDER",
    "HELD",
    "MOVE",
    "REKORDBOX",
    "UNFILE",
    "Decided",
    "Decision",
    "Hold",
    "Mirrored",
    "Place",
    "agreed_after",
    "decide",
    "moment",
]
