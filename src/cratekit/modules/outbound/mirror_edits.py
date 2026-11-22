"""An edit made on the account to a mirrored playlist, told apart and decided (U201, U204).

Each mirrored playlist is read three ways: its SNAPSHOT
(``ledger.MirrorPlaylist.agreed``, what both sides held when a refresh last
finished it), the account now and rekordbox now. From those alone this module
decides which track a person changed on the account and what the library does
about it, reading and writing nothing, so every rule is drivable without a
database, an account or a gate. One base per playlist, so per side a track is
added or removed, never both.

THE GENRE TREE is read by each track's PLACE, the band playlists holding it.
Taken off one band and put in another on the account is a MOVE; taken off its
band and put nowhere is UNFILE (2026-11-04), its genre and energy cleared;
added to a with vox or genre sub playlist of another folder, with no band, takes
that FOLDER's genre, energy kept. Taken off a derived playlist alone is no edit.

THE MOST RECENT CHANGE WINS where both sides changed a place differently: an
addition beats a removal, whose time neither side records; two additions follow
the later added time, and with either unknown or the two equal rekordbox's place
stands, the conservative call. Every such call is named.

THE FAVORITES FOLDER AND INBOX have their own rules, each a tree of its own.
Favorites by track: added to a month or All Favorites is a FAVOURITE, placed as
a heart is; taken off All Favorites is an UNFAVOURITE, leaving every filing
playlist; a month removal alone, two months at once, or off All Favorites while
put in a month is HELD. INBOX by batch: added JOINS, taken off LEAVES, and a
change both sides made is agreed.

THE LIBRARY'S OWN MONTH IS NEVER REKORDBOX'S CHANGE (U236): a month the library
placed a FAVOURITE in, still held by that membership, is no rekordbox addition,
and a month a person put it in on the account replaces it
(:func:`placed_after`).

A DOWNLOAD (U204): a track added on the account that the library has no row
for and no snapshot ever held is HELD with ``acquire``, queued once, and kept on
the account until it lands. One a snapshot held once left the collection.

THE LANDING'S OWN FILING NEVER BEATS THE EDIT THAT QUEUED IT (U227): a track no
snapshot held, whose every band in rekordbox is one its landing filed it into,
is read as landed for the account's edit, which is carried. While that filing
stands, a never agreed queuing playlist's base is read without the track, as it
stood at the queue (U230); an agreed snapshot is never lifted.

HELD IS NEITHER CARRIED NOR UNDONE: the library and the account are left as
they are and the gate names it. A playlist never agreed reads its account side
as its snapshot, so every difference is rekordbox's. A SHORT LISTING carries no
removal: each track the snapshot holds that it does not list is held.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

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
#: Carried (U204): the track is placed as a heart is, in All Favorites and a month.
FAVOURITE = "favourite"
#: Carried (U204): the track leaves All Favorites and every filing playlist.
UNFAVOURITE = "unfavourite"
#: Carried (U204): the track joins an INBOX batch.
JOIN = "join"
#: Carried (U204): the track leaves an INBOX batch.
LEAVE = "leave"
#: Neither carried nor undone, and named.
HELD = "held"

#: The outcomes the library takes.
CARRIED = frozenset({MOVE, FOLDER, UNFILE, FAVOURITE, UNFAVOURITE, JOIN, LEAVE})

#: The edits that give a track a place, the ones a download is queued for (U204).
ADDITIONS = frozenset({MOVE, FOLDER, FAVOURITE, JOIN})

#: The trees an edit is read across, each by its own rule (U204).
GENRE = "genre"
FAVORITES = "favorites"
INBOX = "inbox"
TREES = (GENRE, FAVORITES, INBOX)

#: The three readings of a playlist, as :class:`Mirrored` names them, and as a
#: decision shows them.
_SIDES = ("base", "account", "rekordbox")
_SHOWN = ("was", "account", "rekordbox")


@dataclass(frozen=True, slots=True)
class Place:
    """One mirrored playlist an edit is read on: its account title, rekordbox names and kind.

    ``primary`` is a band playlist in the genre tree (a derived playlist is
    not), ``All Favorites`` in the Favorites tree, and every INBOX batch.
    ``tree`` is which rule reads it (U204).
    """

    title: str
    folder: str
    playlist: str
    primary: bool
    tree: str = GENRE


@dataclass(frozen=True, slots=True)
class Mirrored:
    """One mirrored playlist read three ways, by account track.

    ``agreed`` is the snapshot, ``None`` for a playlist never agreed; the two
    ``_added`` maps are each track's added time on that side, when known.
    """

    place: Place
    account: frozenset[str] = frozenset()
    rekordbox: frozenset[str] = frozenset()
    agreed: frozenset[str] | None = None
    short: bool = False
    account_added: Mapping[str, str] = field(default_factory=dict)
    rekordbox_added: Mapping[str, str] = field(default_factory=dict)
    #: The library's own placements here not yet on the account (U236), each
    #: still held by the membership its write made. Favorites filing only.
    placed: frozenset[str] = frozenset()

    @property
    def base(self) -> frozenset[str]:
        """The snapshot, or the account side for a playlist never agreed."""
        return self.account if self.agreed is None else self.agreed


@dataclass(frozen=True, slots=True)
class Hold:
    """What the mirror leaves as it is on one playlist.

    ``keep`` is account tracks it never takes off and ``skip`` rekordbox's it
    never adds, for an edit carried or held. ``stay`` keeps the snapshot's word
    even where both sides agree now (U204), so a Favorites edit planned and not
    applied is not half agreed away.
    """

    keep: frozenset[str] = frozenset()
    skip: frozenset[str] = frozenset()
    stay: frozenset[str] = frozenset()

    @property
    def tracks(self) -> frozenset[str]:
        return self.keep | self.skip | self.stay


@dataclass(frozen=True, slots=True)
class Decision:
    """One track a person changed on the account, and what becomes of it.

    ``to`` is the place a carried edit takes, ``content_id`` the library row it
    changes, and the three place tuples are titles, sorted.
    """

    track: str
    outcome: str
    why: str
    to: Place | None = None
    content_id: str = ""
    was: tuple[str, ...] = ()
    account: tuple[str, ...] = ()
    rekordbox: tuple[str, ...] = ()
    #: Every playlist of its tree read in full, ``(folder, title, held on the
    #: account)``, which the snapshot takes once the library took the edit.
    settle: tuple[tuple[str, str, bool], ...] = ()
    #: Which tree's rule decided it (U204).
    tree: str = GENRE
    #: A track added on the account that the library lacks, to queue (U204).
    acquire: bool = False
    #: A FAVOURITE put in All Favorites alone (U204): the account's added time,
    #: which dates its month, and whether a filing playlist holds it already.
    when: str = ""
    filed: bool = False
    #: A FAVOURITE moved between months (U204): the months it leaves.
    away: tuple[Place, ...] = ()
    #: Carried over the band its landing filed it into by its tags (U227).
    landed: bool = False

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
        optional = (
            ("content_id", self.content_id),
            ("acquire", self.acquire),
            ("landed", self.landed),
        )
        return shown | {key: value for key, value in optional if value}


@dataclass(frozen=True, slots=True)
class Decided:
    """Every track a person changed on the account, and every playlist's hold."""

    decisions: tuple[Decision, ...] = ()
    holds: Mapping[str, Hold] = field(default_factory=dict)

    @property
    def carried(self) -> tuple[Decision, ...]:
        return tuple(one for one in self.decisions if one.outcome in CARRIED)

    @property
    def wanted(self) -> tuple[Decision, ...]:
        """Every track added on the account that the library lacks, to queue (U204)."""
        return tuple(one for one in self.decisions if one.acquire)

    def hold(self, title: str) -> Hold:
        return self.holds.get(title, Hold())


def moment(text: str) -> datetime | None:
    """A time as either side writes it, with its zone, or ``None`` when it is unknown.

    Rekordbox writes a space before the zone. A time with no zone is unknown,
    since comparing it with one that has a zone would be a guess.
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


def _named(places: Iterable[Place]) -> str:
    return ", ".join(_titles(places))


def _placed(
    playlists: Sequence[Mirrored],
    track: str,
    side: str,
    primary: bool,
    lifted: frozenset[str] = frozenset(),
) -> frozenset[Place]:
    """The places of one kind holding ``track`` on one side, a lifted base left out (U230)."""
    return frozenset(
        one.place
        for one in playlists
        if one.place.primary is primary
        and track in getattr(one, side)
        and not (side == "base" and one.place.title in lifted)
    )


def _intent(
    was: frozenset[Place], now: frozenset[Place], was_more: frozenset[Place], now_more: frozenset[Place]
) -> tuple[str, Place | None, str] | None:
    """What the account side did to one track's place, or ``None`` for nothing.

    ``was`` and ``now`` are its band places in the snapshot and on the account,
    ``was_more`` and ``now_more`` its derived ones.
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
        return HELD, None, (
            f"added on the account to {len(added)} band playlists at once "
            f"({_named(added)}), so which one it belongs in is not something the account says"
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {_named(removed)} on the account, left in {place.title}"
    if removed and len(now) > 1:
        return HELD, None, (
            f"taken off {_named(removed)} on the account and still in {len(now)} band "
            f"playlists there, so which one it belongs in is not something the account says"
        )
    if not added_more:
        if not now_more:
            return UNFILE, None, (
                f"taken off {_named(removed)} on the account and added to no other genre playlist"
            )
        return HELD, None, (
            f"taken off {_named(removed)} on the account and left only in {_named(now_more)}, "
            f"which is derived from a band, so where it goes is not something the account says"
        )
    folders = sorted({place.folder for place in added_more})
    if len(folders) > 1:
        return HELD, None, (
            f"added on the account to playlists of {len(folders)} genres at once "
            f"({_named(added_more)}), so which genre it takes is not something the account says"
        )
    if removed and not now and folders[0] in {place.folder for place in removed}:
        # TAKEN OFF ITS BAND, LEFT IN A DERIVED PLAYLIST OF ITS OWN GENRE: the
        # account says neither where it goes nor that it leaves.
        return HELD, None, (
            f"taken off {_named(removed)} on the account and left only in "
            f"{_named(added_more | now_more)}, which is derived from a band of its own "
            f"genre, so where it goes is not something the account says"
        )
    if not removed and folders[0] in {place.folder for place in now}:
        # A DERIVED PLAYLIST OF ITS OWN GENRE: the band already says the genre.
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
    playlists: Sequence[Mirrored],
    owner: Mapping[str, Sequence[str]],
    filed: Mapping[str, Iterable[tuple[str, str]]] | None = None,
    queued: Mapping[str, Iterable[str]] | None = None,
) -> Decided:
    """Decide every track a person changed on the account, tree by tree. Pure.

    ``owner`` is each account track to its matched library rows, of which a
    carried edit needs exactly one. ``filed`` is each track a mirror download
    queued to the ``(folder, playlist)`` places its landing filed it into
    (U227), and ``queued`` each such track to the titles of the playlists whose
    job queued it (U230). Each playlist's hold covers its own tree (U204).
    """
    # EVERY TRACK A SNAPSHOT EVER HELD, by the playlists whose base holds it:
    # one the library no longer owns left the collection and is never queued.
    held_by: dict[str, set[str]] = {}
    for one in playlists:
        for track in one.base:
            held_by.setdefault(track, set()).add(one.place.title)
    known = frozenset(held_by)
    by_landing = {track: frozenset(places) for track, places in (filed or {}).items()}
    by_queue = {
        track: frozenset(str(title) for title in titles) for track, titles in (queued or {}).items()
    }

    def mine(tree: str) -> list[Mirrored]:
        return [one for one in playlists if one.place.tree == tree]

    decisions = [
        *_decide_genre(
            mine(GENRE),
            owner,
            known,
            by_landing,
            queued=by_queue,
            held_by={track: frozenset(titles) for track, titles in held_by.items()},
        ),
        *_decide_favorites(mine(FAVORITES), owner, known),
        *_decide_inbox(mine(INBOX), owner, known),
    ]
    return Decided(decisions=tuple(decisions), holds=_holds(playlists, decisions))


def _unread(playlists: Sequence[Mirrored]) -> set[str]:
    """Tracks a short listing left out of a playlist the snapshot holds them on.

    A SHORT LISTING SAYS NOTHING OF A TRACK IT LEAVES OUT, so such a track is
    neither a removal nor anything else.
    """
    unread: set[str] = set()
    for one in playlists:
        if one.short and one.agreed is not None:
            unread |= one.agreed - one.account
    return unread


def _tracks(playlists: Sequence[Mirrored]) -> list[str]:
    found: set[str] = set()
    for one in playlists:
        found |= one.base | one.account | one.rekordbox
    return sorted(found)


_UNREAD = (
    "a playlist the snapshot has it in listed short on the account without it, so "
    "whether a person took it off there cannot be read"
)


def _carry(
    track: str,
    kind: str,
    why: str,
    owner: Mapping[str, Sequence[str]],
    known: frozenset[str],
    *,
    to: Place | None,
    tree: str,
    settle: tuple[tuple[str, str, bool], ...],
    shown: Mapping[str, tuple[str, ...]],
    **extra: Any,
) -> Decision:
    """A carried edit on the one library row matched to the track, or why it is held.

    No row holds it on the account, queued for download when it was added
    there and no snapshot ever held it (U204); two rows hold it, since which
    one changes is not something the account says.
    """
    rows = sorted({str(one) for one in owner.get(track, ()) if str(one)})
    if not rows:
        acquire = kind in ADDITIONS and track not in known
        then = (
            "so it is queued for download and stays on the account until it lands"
            if acquire
            else "so nothing is changed and it stays on the account"
        )
        why = f"{why}, and the library holds no track matched to it, {then}"
        return Decision(track, HELD, why, to=to, tree=tree, acquire=acquire, **shown)
    if len(rows) > 1:
        why = (
            f"{why}, and {len(rows)} library rows match it, so which one changes is "
            f"not something the account says"
        )
        return Decision(track, HELD, why, to=to, tree=tree, **shown)
    return Decision(
        track, kind, why, to=to, content_id=rows[0], settle=settle, tree=tree, **shown, **extra
    )


def _decide_genre(
    playlists: Sequence[Mirrored],
    owner: Mapping[str, Sequence[str]],
    known: frozenset[str],
    filed: Mapping[str, frozenset[tuple[str, str]]],
    *,
    queued: Mapping[str, frozenset[str]],
    held_by: Mapping[str, frozenset[str]],
) -> list[Decision]:
    """Every track a person changed on the account across the genre tree (U201).

    ``filed`` and ``queued`` are :func:`decide`'s, and ``held_by`` each track
    to the titles of every playlist, of any tree, whose base holds it (U230).
    """
    unread = _unread(playlists)

    def decided(track: str) -> Decision | None:
        # AS IT STOOD WHEN THE DOWNLOAD WAS QUEUED (U230), :func:`_as_queued`.
        lifted = _as_queued(track, playlists, filed, queued)
        was, now, there = (_placed(playlists, track, side, True, lifted) for side in _SIDES)
        shown = dict(zip(_SHOWN, map(_titles, (was, now, there))))
        if track in unread:
            return Decision(track, HELD, _UNREAD, **shown)
        more = (_placed(playlists, track, side, False, lifted) for side in _SIDES[:2])
        intent = _intent(was, now, *more)
        if intent is None:
            return None
        kind, to, why = intent
        if kind == HELD:
            return Decision(track, HELD, why, **shown)
        extra: dict[str, Any] = {}
        if there != was:
            if _agrees(kind, to, there):
                why = f"{why}, and rekordbox made the same change"
                return Decision(track, AGREED, why, to=to, **shown)
            if kind == UNFILE:
                why = (
                    f"{why}, and placed in {_named(there)} in rekordbox: "
                    f"an addition beats a removal, whose time is never known"
                )
                return Decision(track, REKORDBOX, why, **shown)
            if there and _landed_there(track, there, bool(held_by.get(track, frozenset()) - lifted), filed):
                # THE LANDING'S OWN FILING (U227), which no person chose.
                why = (
                    f"{why}, and landed for the account's edit: its landing filed it in "
                    f"{_named(there)} by its own tags, which is no change made in rekordbox"
                )
                extra = {"landed": True}
            elif there:
                said = _later(playlists, track, to, there - was)
                if said is not None:
                    return Decision(track, REKORDBOX, f"{why}, {said}", **shown)
                why = f"{why}, later than rekordbox placed it in {_named(there)}"
            else:
                why = (
                    f"{why}, and taken out of the tree in rekordbox: an addition beats "
                    f"a removal, whose time is never known"
                )
        settle = tuple(
            (one.place.folder, one.place.title, track in one.account)
            for one in playlists
            if not one.short
        )
        return _carry(
            track, kind, why, owner, known, to=to, tree=GENRE, settle=settle, shown=shown, **extra
        )

    return [one for one in map(decided, _tracks(playlists)) if one is not None]


def _landed_there(
    track: str, there: frozenset[Place], held: bool, filed: Mapping[str, frozenset[tuple[str, str]]]
) -> bool:
    """Whether every band rekordbox holds ``track`` in is one its landing filed it into (U227).

    Only for a track no snapshot held, ``held`` false: once the library took
    the edit, the later change rule alone reads it.
    """
    places = filed.get(track)
    if not places or held:
        return False
    return _filed_by_landing(there, places)


def _filed_by_landing(there: frozenset[Place], places: frozenset[tuple[str, str]]) -> bool:
    """Whether rekordbox holds the track in a band and every band is one its landing filed."""
    return bool(there) and all((place.folder, place.playlist) in places for place in there)


def _as_queued(
    track: str,
    playlists: Sequence[Mirrored],
    filed: Mapping[str, frozenset[tuple[str, str]]],
    queued: Mapping[str, frozenset[str]],
) -> frozenset[str]:
    """The playlists whose base is read without ``track``, as it stood at the queue (U230).

    A download is queued only for a track no snapshot held, so a NEVER AGREED
    queuing playlist's base, its account side, says nothing of the library's
    history. An agreed snapshot is never lifted, since it takes the track only
    once the library took the edit, nor a short listing. Only while the
    landing's filing stands and the account, not rekordbox, still lists it
    there; every other base counts as before.
    """
    titles = queued.get(track)
    places = filed.get(track)
    if not titles or not places:
        return frozenset()
    there = frozenset(one.place for one in playlists if one.place.primary and track in one.rekordbox)
    if not _filed_by_landing(there, places):
        return frozenset()
    return frozenset(
        one.place.title
        for one in playlists
        if one.place.title in titles
        and one.agreed is None
        and not one.short
        and track in one.base
        and track in one.account
        and track not in one.rekordbox
    )


def _decide_favorites(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]], known: frozenset[str]
) -> list[Decision]:
    """Every track a person changed on the account across the Favorites folder (U204).

    All Favorites is the one primary place and each filing playlist a month:
    a FAVOURITE is placed as a heart is, an UNFAVOURITE leaves the whole folder.
    """
    unread = _unread(playlists)
    source = next((one.place for one in playlists if one.place.primary), None)
    favourites = source.title if source else "the favourites"

    def decided(track: str) -> Decision | None:
        def say(outcome: str, why: str, **more: Any) -> Decision:
            return Decision(track, outcome, why, tree=FAVORITES, **more, **shown)

        was_s, now_s, there_s = (bool(_placed(playlists, track, side, True)) for side in _SIDES)
        was_m, now_m, there_m = (_placed(playlists, track, side, False) for side in _SIDES)
        # THE LIBRARY'S OWN MONTH (U236), never a change a person made in rekordbox.
        ours = frozenset(
            one.place for one in playlists if not one.place.primary and track in one.placed
        )
        shown = {
            key: _titles(_placed(playlists, track, side, True) | months)
            for key, side, months in zip(_SHOWN, _SIDES, (was_m, now_m, there_m))
        }
        if track in unread:
            return say(HELD, _UNREAD)
        added_s, removed_s = now_s and not was_s, was_s and not now_s
        added_m, removed_m = now_m - was_m, was_m - now_m
        if not (added_s or removed_s or added_m or removed_m):
            return None
        extra: dict[str, Any] = {}
        if removed_s and added_m:
            return say(HELD, (
                f"taken off {favourites} and put in {_named(added_m)} on the account at once, "
                f"so whether it is a favourite is not something the account says"
            ))
        if removed_s:
            kind, to = UNFAVOURITE, None
            why = f"taken off {favourites} on the account"
        elif len(added_m) > 1:
            return say(HELD, (
                f"added on the account to {len(added_m)} month playlists at once "
                f"({_named(added_m)}), so which month it belongs in is not something the "
                f"account says"
            ))
        elif added_m:
            ((to),) = added_m
            kind, why = FAVOURITE, f"put in {to.title} on the account"
            mine = ours - now_m
            if removed_m or mine:
                # A MOVE BETWEEN MONTHS leaves the old month too, and a month the
                # library placed it in (U236), so the library matches the account.
                extra = {"away": tuple(sorted(removed_m | mine, key=lambda one: one.title))}
                if removed_m:
                    why = f"{why}, taken off {_named(removed_m)}"
                if mine:
                    why = f"{why}, leaving {_named(mine)}, the month the library placed it in"
        elif added_s:
            to = source
            kind, why = FAVOURITE, f"put in {to.title} on the account"
            when = (one.account_added.get(track, "") for one in playlists if one.place.primary)
            extra = {"when": next(when, ""), "filed": bool(now_m or there_m)}
        else:
            return say(HELD, (
                f"taken off {_named(removed_m)} on the account and left in {favourites}: "
                f"a month removal alone is listed and not carried"
            ))
        if there_s != was_s or there_m != was_m:
            if kind == UNFAVOURITE:
                if not there_s and not there_m:
                    return say(AGREED, f"{why}, and rekordbox made the same change")
                if (there_s and not was_s) or (there_m - was_m - ours):
                    return say(REKORDBOX, (
                        f"{why}, and placed in the favourites in rekordbox since: an "
                        f"addition beats a removal, whose time is never known"
                    ))
            else:
                assert to is not None
                away = frozenset(extra.get("away", ()))
                if there_s and (to.primary or to in there_m) and not there_m & away:
                    return say(AGREED, f"{why}, and rekordbox made the same change", to=to)
                # The month the account put it in is no move of rekordbox's.
                moved = there_m - was_m - ours - {to}
                if moved and not to.primary:
                    said = _later(playlists, track, to, moved)
                    if said is not None:
                        return say(REKORDBOX, f"{why}, {said}")
                    why = f"{why}, later than rekordbox placed it in {_named(moved)}"
        # AFTER THE WRITE rekordbox holds the track where the edit puts it and
        # nowhere it took it from; only a playlist both sides then agree on is
        # settled, and every other keeps the snapshot's word.
        after: dict[str, bool] = {}
        for one in playlists:
            if one.short:
                continue
            if kind == UNFAVOURITE or one.place in extra.get("away", ()):
                held_after = False
            else:
                held_after = track in one.rekordbox or one.place.primary or one.place == to
            if held_after == (track in one.account):
                after[one.place.title] = held_after
        settle = tuple(
            (one.place.folder, one.place.title, after[one.place.title])
            for one in playlists
            if one.place.title in after
        )
        return _carry(
            track, kind, why, owner, known, to=to, tree=FAVORITES, settle=settle, shown=shown,
            **extra,
        )

    return [one for one in map(decided, _tracks(playlists)) if one is not None]


def _decide_inbox(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]], known: frozenset[str]
) -> list[Decision]:
    """Every track a person added to or took off an INBOX batch on the account (U204).

    Per playlist, since a track may sit in several batches; one base each, so
    a change both sides made is agreed and nothing else can conflict.
    """
    decisions: list[Decision] = []
    for one in playlists:
        unread = _unread([one])
        title = (one.place.title,)
        for track in sorted(one.base | one.account | one.rekordbox):
            shown = {
                "was": title if track in one.base else (),
                "account": title if track in one.account else (),
                "rekordbox": title if track in one.rekordbox else (),
            }
            if track in unread:
                decisions.append(Decision(track, HELD, _UNREAD, to=one.place, tree=INBOX, **shown))
                continue
            added = track in one.account and track not in one.base
            removed = track in one.base and track not in one.account
            if not (added or removed):
                continue
            why = f"{'put in' if added else 'taken off'} {one.place.title} on the account"
            if (track in one.rekordbox) is added:
                why = f"{why}, and rekordbox made the same change"
                decisions.append(Decision(track, AGREED, why, to=one.place, tree=INBOX, **shown))
                continue
            settle = ((one.place.folder, one.place.title, added),)
            kind = JOIN if added else LEAVE
            decisions.append(
                _carry(
                    track, kind, why, owner, known, to=one.place, tree=INBOX, settle=settle,
                    shown=shown,
                )
            )
    return decisions


def _later(
    playlists: Sequence[Mirrored], track: str, to: Place | None, placed: frozenset[Place]
) -> str | None:
    """``None`` when the account's addition is the later, else why rekordbox's stands."""
    on_account = next(
        (one.account_added.get(track, "") for one in playlists if one.place == to), ""
    )
    in_rekordbox = (
        next((one.rekordbox_added.get(track, "") for one in playlists if one.place in placed), "")
        if len(placed) == 1
        else ""
    )
    account_at, rekordbox_at = moment(on_account), moment(in_rekordbox)
    there = _named(placed) or "another band"
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
    """Each playlist's hold: every carried or held track of its own tree, as the account has it.

    An INBOX edit holds its own batch alone (U204).
    """
    held: dict[str, set[str]] = {}
    for one in decisions:
        if one.outcome in CARRIED or one.outcome == HELD:
            key = one.to.title if one.tree == INBOX and one.to is not None else one.tree
            held.setdefault(key, set()).add(one.track)
    holds: dict[str, Hold] = {}
    for one in playlists:
        key = one.place.title if one.place.tree == INBOX else one.place.tree
        mine = held.get(key, set())
        keep = frozenset(track for track in mine if track in one.account and track not in one.rekordbox)
        skip = frozenset(track for track in mine if track in one.rekordbox and track not in one.account)
        stay = frozenset(mine) if one.place.tree == FAVORITES else frozenset()
        if keep or skip or stay:
            holds[one.place.title] = Hold(keep=keep, skip=skip, stay=stay)
    return holds


def placed_after(
    placed: Mapping[str, str], after: Iterable[str], held: Iterable[str]
) -> dict[str, str]:
    """The placements a playlist keeps once the mirror finished it (U236).

    ``placed`` is each placed track to its membership's time, ``after`` what the
    account holds once the writes landed, ``held`` the hold's tracks. One the
    account now holds there, and no hold covers, is the snapshot's word now and
    is dropped; every other is kept, read only while rekordbox holds it by the
    membership it names.
    """
    now, kept = frozenset(after), frozenset(held)
    return {track: at for track, at in placed.items() if track in kept or track not in now}


def agreed_after(
    base: Iterable[str] | None, after: Iterable[str], held: Iterable[str]
) -> frozenset[str]:
    """The snapshot a playlist takes once the mirror finished it.

    A held track keeps the snapshot's word, ``base``, so it reads the same at
    the next refresh; every other is agreed as the account holds it ``after``
    the writes, a removal the account refused included, so it is asked again.
    """
    held = frozenset(held)
    now = frozenset(after)
    before = now if base is None else frozenset(base)
    return frozenset(track for track in now if track not in held) | frozenset(
        track for track in before if track in held
    )


__all__ = [
    "ADDITIONS", "AGREED", "CARRIED", "FAVORITES", "FAVOURITE", "FOLDER", "GENRE", "HELD",
    "INBOX", "JOIN", "LEAVE", "MOVE", "REKORDBOX", "TREES", "UNFAVOURITE", "UNFILE", "Decided",
    "Decision", "Hold", "Mirrored", "Place", "agreed_after", "decide", "moment", "placed_after",
]
