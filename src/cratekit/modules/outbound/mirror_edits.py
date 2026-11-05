"""An edit made on the account to a mirrored playlist, told apart and decided (U201, U204).

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

THE FAVORITES FOLDER AND INBOX ARE READ BY THEIR OWN RULES (U204), each a tree
of its own, so a track held in one is never held in another:

* FAVORITES, by track across ``All Favorites`` and the filing playlists beside
  it (a month, ``Undated``, a quarter the split has not retired). A track added
  on the account to one month, or to All Favorites, is a FAVOURITE: the library
  places it as a heart is placed, in All Favorites and that month, or for an
  addition to All Favorites alone the month of its added time on the account,
  none when it sits in a filing playlist already. A track taken off All
  Favorites is an UNFAVOURITE: it leaves All Favorites and every filing
  playlist. Taken off a month alone, added to two months at once, or taken off
  All Favorites while put in a month, it is HELD and listed, since none of those
  says what the library should do;
* INBOX, by batch playlist: a track added on the account JOINS the batch, one
  taken off LEAVES it. One base per playlist, so the two sides cannot disagree
  there: a change both made is agreed.

A DOWNLOAD (U204). A track added on the account that the library owns no row
for, and that no snapshot of any mirrored playlist ever held, is HELD with
``acquire`` set: the organize step ``mirror-downloads`` queues it once, and
the mirror keeps it on the account until it lands, when this rule reads it as
the addition it is and the library takes it. A track a snapshot held once and
the library no longer owns left the collection, and is never fetched again.

HELD IS NEITHER CARRIED NOR UNDONE. A track added on the account to two band
playlists at once, one taken off its band and left in a derived playlist only,
one the library owns no row for (queued for download by U204) or owns two rows
for, and one whose playlist the account listed short, is held: the library is
not changed, the account is left as it is, and the gate names it. Nothing a
person did is lost to a refresh that could not read what they meant.

A PLAYLIST NEVER AGREED READS ITS ACCOUNT SIDE AS ITS SNAPSHOT, so every
difference on it is rekordbox's and nothing in the library changes: the first
refresh after U201 lands, and a playlist the mirror made since. A SHORT LISTING
CARRIES NO REMOVAL, since a track it leaves out is no evidence that a person
took it off: each track the snapshot holds that it does not list is held. Its
snapshot still advances, keeping its word on every track it did not list and
the mirror did not take off, so a change the mirror carried is not read again.

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


@dataclass(frozen=True, slots=True)
class Place:
    """One mirrored playlist an edit is read on: its account title, rekordbox names and kind.

    In the genre tree ``primary`` is a band playlist, a place routing files a
    track's band into, and anything else in a genre folder, a with vox, genre
    sub or genre Favorites playlist, is additive. In the Favorites tree it is
    ``All Favorites``, and a filing playlist is not. Every INBOX batch is
    primary. ``tree`` is which rule reads it (U204).
    """

    title: str
    folder: str
    playlist: str
    primary: bool
    tree: str = GENRE


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

    ``to`` is the place a MOVE, FOLDER, FAVOURITE, JOIN or LEAVE takes,
    ``content_id`` the library row a carried edit changes, and the three place
    tuples are titles, sorted.
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
    #: ``""`` when unknown, which dates its month, and whether it sits in a
    #: filing playlist already on either side, which gives it none.
    when: str = ""
    filed: bool = False

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
        if self.acquire:
            shown["acquire"] = True
        return shown


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
    if removed and not now and folders[0] in {place.folder for place in removed}:
        # TAKEN OFF ITS BAND AND LEFT IN A DERIVED PLAYLIST OF ITS OWN GENRE:
        # the genre is unchanged and the band is gone, so the account says
        # neither where it goes nor that it leaves.
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and left only in "
            f"{', '.join(_titles(added_more | now_more))}, which is derived from a band "
            f"of its own genre, so where it goes is not something the account says",
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
    """Decide every track a person changed on the account, tree by tree. Pure.

    ``owner`` is each account track to the library rows matched to it, which a
    carried edit needs exactly one of. Each tree is read by its own rule, and
    each playlist's hold covers only the tracks its own tree held (U204).
    """
    # EVERY TRACK A SNAPSHOT EVER HELD, across every tree: one the library no
    # longer owns left the collection and is never queued for download.
    known: set[str] = set()
    for one in playlists:
        known |= one.base
    decisions: list[Decision] = []
    for tree, rule in ((GENRE, _decide_genre), (FAVORITES, _decide_favorites), (INBOX, _decide_inbox)):
        mine = [one for one in playlists if one.place.tree == tree]
        if mine:
            decisions.extend(rule(mine, owner, frozenset(known)))
    return Decided(decisions=tuple(decisions), holds=_holds(playlists, decisions))


def _unread(playlists: Sequence[Mirrored]) -> set[str]:
    """Tracks a short listing left out of a playlist the snapshot holds them on.

    A SHORT LISTING SAYS NOTHING OF A TRACK IT LEAVES OUT: one the snapshot
    holds and the listing does not may be counted and unlisted, so it is
    neither a removal nor anything else. A track it lists is on the account.
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

    A track the library holds no row for is held on the account; one added there
    that no snapshot ever held is queued for download (U204). Two rows are held,
    since which one changes is not something the account says.
    """
    rows = sorted({str(one) for one in owner.get(track, ()) if str(one)})
    if not rows:
        if kind in ADDITIONS and track not in known:
            return Decision(
                track,
                HELD,
                f"{why}, and the library holds no track matched to it, so it is queued "
                f"for download and stays on the account until it lands",
                to=to,
                tree=tree,
                acquire=True,
                **shown,
            )
        return Decision(
            track,
            HELD,
            f"{why}, and the library holds no track matched to it, so nothing is "
            f"changed and it stays on the account",
            to=to,
            tree=tree,
            **shown,
        )
    if len(rows) > 1:
        return Decision(
            track,
            HELD,
            f"{why}, and {len(rows)} library rows match it, so which one changes is "
            f"not something the account says",
            to=to,
            tree=tree,
            **shown,
        )
    return Decision(
        track, kind, why, to=to, content_id=rows[0], settle=settle, tree=tree, **shown, **extra
    )


def _decide_genre(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]], known: frozenset[str]
) -> list[Decision]:
    """Every track a person changed on the account across the genre tree (U201)."""
    unread = _unread(playlists)

    def placed(track: str, side: str, primary: bool) -> frozenset[Place]:
        return frozenset(
            one.place
            for one in playlists
            if one.place.primary is primary and track in getattr(one, side)
        )

    decisions: list[Decision] = []
    for track in _tracks(playlists):
        was, now = placed(track, "base", True), placed(track, "account", True)
        there = placed(track, "rekordbox", True)
        shown = {
            "was": _titles(was),
            "account": _titles(now),
            "rekordbox": _titles(there),
        }
        if track in unread:
            decisions.append(Decision(track, HELD, _UNREAD, **shown))
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
        decisions.append(
            _carry(
                track,
                kind,
                why,
                owner,
                known,
                to=to,
                tree=GENRE,
                settle=tuple(
                    (one.place.folder, one.place.title, track in one.account)
                    for one in playlists
                    if not one.short
                ),
                shown=shown,
            )
        )
    return decisions


def _decide_favorites(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]], known: frozenset[str]
) -> list[Decision]:
    """Every track a person changed on the account across the Favorites folder (U204).

    All Favorites is the one primary place, and each filing playlist beside it
    is a month. The rule is the heart's: a FAVOURITE is placed as a heart is
    placed, and an UNFAVOURITE leaves the whole folder.
    """
    unread = _unread(playlists)

    def placed(track: str, side: str, primary: bool) -> frozenset[Place]:
        return frozenset(
            one.place
            for one in playlists
            if one.place.primary is primary and track in getattr(one, side)
        )

    decisions: list[Decision] = []
    for track in _tracks(playlists):
        was_s, now_s = bool(placed(track, "base", True)), bool(placed(track, "account", True))
        there_s = bool(placed(track, "rekordbox", True))
        was_m, now_m = placed(track, "base", False), placed(track, "account", False)
        there_m = placed(track, "rekordbox", False)
        shown = {
            "was": _titles(placed(track, "base", True) | was_m),
            "account": _titles(placed(track, "account", True) | now_m),
            "rekordbox": _titles(placed(track, "rekordbox", True) | there_m),
        }
        if track in unread:
            decisions.append(Decision(track, HELD, _UNREAD, tree=FAVORITES, **shown))
            continue
        added_s, removed_s = now_s and not was_s, was_s and not now_s
        added_m, removed_m = now_m - was_m, was_m - now_m
        if not (added_s or removed_s or added_m or removed_m):
            continue
        source = next((one.place for one in playlists if one.place.primary), None)
        extra: dict[str, Any] = {}
        if removed_s and added_m:
            why = (
                f"taken off {source.title if source else 'the favourites'} and put in "
                f"{', '.join(_titles(added_m))} on the account at once, so whether it is "
                f"a favourite is not something the account says"
            )
            decisions.append(Decision(track, HELD, why, tree=FAVORITES, **shown))
            continue
        if removed_s:
            kind, to = UNFAVOURITE, None
            why = f"taken off {source.title if source else 'the favourites'} on the account"
        elif len(added_m) > 1:
            why = (
                f"added on the account to {len(added_m)} month playlists at once "
                f"({', '.join(_titles(added_m))}), so which month it belongs in is not "
                f"something the account says"
            )
            decisions.append(Decision(track, HELD, why, tree=FAVORITES, **shown))
            continue
        elif added_m:
            ((to),) = added_m
            kind, why = FAVOURITE, f"put in {to.title} on the account"
        elif added_s:
            to = source
            kind, why = FAVOURITE, f"put in {to.title} on the account"
            extra = {
                "when": next(
                    (one.account_added.get(track, "") for one in playlists if one.place.primary),
                    "",
                ),
                "filed": bool(now_m or there_m),
            }
        else:
            why = (
                f"taken off {', '.join(_titles(removed_m))} on the account and left in "
                f"{source.title if source else 'the favourites'}: a month removal alone "
                f"is listed and not carried"
            )
            decisions.append(Decision(track, HELD, why, tree=FAVORITES, **shown))
            continue
        if there_s != was_s or there_m != was_m:
            if kind == UNFAVOURITE:
                if not there_s and not there_m:
                    decisions.append(
                        Decision(
                            track, AGREED, f"{why}, and rekordbox made the same change",
                            tree=FAVORITES, **shown,
                        )
                    )
                    continue
                if (there_s and not was_s) or (there_m - was_m):
                    decisions.append(
                        Decision(
                            track,
                            REKORDBOX,
                            f"{why}, and placed in the favourites in rekordbox since: an "
                            f"addition beats a removal, whose time is never known",
                            tree=FAVORITES,
                            **shown,
                        )
                    )
                    continue
            else:
                assert to is not None
                if there_s and (to.primary or to in there_m):
                    decisions.append(
                        Decision(
                            track, AGREED, f"{why}, and rekordbox made the same change",
                            to=to, tree=FAVORITES, **shown,
                        )
                    )
                    continue
                moved = there_m - was_m
                if moved and not to.primary:
                    said = _later(playlists, track, to, moved)
                    if said is not None:
                        decisions.append(
                            Decision(track, REKORDBOX, f"{why}, {said}", tree=FAVORITES, **shown)
                        )
                        continue
                    why = f"{why}, later than rekordbox placed it in {', '.join(_titles(moved))}"
        # AFTER THE WRITE rekordbox holds the track where the edit puts it and
        # nowhere it took it from; only a playlist both sides then agree on is
        # settled, and every other keeps the snapshot's word.
        after: dict[str, bool] = {}
        for one in playlists:
            if one.short:
                continue
            if kind == UNFAVOURITE:
                held_after = False
            else:
                held_after = track in one.rekordbox or one.place.primary or one.place == to
            if held_after == (track in one.account):
                after[one.place.title] = held_after
        decisions.append(
            _carry(
                track,
                kind,
                why,
                owner,
                known,
                to=to,
                tree=FAVORITES,
                settle=tuple(
                    (one.place.folder, one.place.title, after[one.place.title])
                    for one in playlists
                    if one.place.title in after
                ),
                shown=shown,
                **extra,
            )
        )
    return decisions


def _decide_inbox(
    playlists: Sequence[Mirrored], owner: Mapping[str, Sequence[str]], known: frozenset[str]
) -> list[Decision]:
    """Every track a person added to or took off an INBOX batch on the account (U204).

    Per playlist, since a batch is no place a track has one of: a track may sit
    in several batches. One base per playlist, so a change both sides made is
    agreed and nothing else can conflict.
    """
    decisions: list[Decision] = []
    for one in playlists:
        unread = _unread([one])
        for track in sorted(one.base | one.account | one.rekordbox):
            shown = {
                "was": (one.place.title,) if track in one.base else (),
                "account": (one.place.title,) if track in one.account else (),
                "rekordbox": (one.place.title,) if track in one.rekordbox else (),
            }
            if track in unread:
                decisions.append(Decision(track, HELD, _UNREAD, to=one.place, tree=INBOX, **shown))
                continue
            added = track in one.account and track not in one.base
            removed = track in one.base and track not in one.account
            if not (added or removed):
                continue
            kind = JOIN if added else LEAVE
            why = (
                f"put in {one.place.title} on the account"
                if added
                else f"taken off {one.place.title} on the account"
            )
            if (track in one.rekordbox) is added:
                decisions.append(
                    Decision(
                        track, AGREED, f"{why}, and rekordbox made the same change",
                        to=one.place, tree=INBOX, **shown,
                    )
                )
                continue
            decisions.append(
                _carry(
                    track,
                    kind,
                    why,
                    owner,
                    known,
                    to=one.place,
                    tree=INBOX,
                    settle=((one.place.folder, one.place.title, added),),
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
    """Each playlist's hold: every carried or held track of its tree left as the account has it.

    PER TREE (U204): a track held in the genre tree is still mirrored as
    rekordbox has it in the Favorites folder, and the reverse.
    """
    held: dict[str, set[str]] = {}
    for one in decisions:
        if one.outcome in CARRIED or one.outcome == HELD:
            held.setdefault(one.tree, set()).add(one.track)
    holds: dict[str, Hold] = {}
    for one in playlists:
        mine = held.get(one.place.tree, set())
        keep = frozenset(track for track in mine if track in one.account and track not in one.rekordbox)
        skip = frozenset(track for track in mine if track in one.rekordbox and track not in one.account)
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
    "ADDITIONS",
    "AGREED",
    "CARRIED",
    "FAVORITES",
    "FAVOURITE",
    "FOLDER",
    "GENRE",
    "HELD",
    "INBOX",
    "JOIN",
    "LEAVE",
    "MOVE",
    "REKORDBOX",
    "TREES",
    "UNFAVOURITE",
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
