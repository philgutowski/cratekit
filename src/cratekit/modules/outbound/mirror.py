"""A rekordbox folder mirrored onto the streaming account as one flat root folder (U147).

THE SHAPE. The author listens on the account and curates in rekordbox, so every
genre folder of the routing tree, and the Favorites folder, is copied to the
account as one root folder of the same name holding one private playlist per
rekordbox playlist. The account root is flat by the 2026-10-13 decision, since
the provider's app does not draw a nested folder, so a three level tree becomes
one root folder per rekordbox folder. A playlist's account title carries its
folder, ``Deep House Low``, because the account's search and its flat playlist
list show a title without its folder. Which title each one takes is the
caller's: this module is handed the titles.

A MIRROR, NOT AN EXPORT. Each mirrored playlist ends a refresh holding exactly
the account tracks of its rekordbox playlist: a track that left rekordbox is
taken off, including one a person added on the account by hand. That removal is
permitted because every mirrored playlist is one the product CREATED, which the
ledger records (``ledger.reserve_mirror_playlist``) and the account seam asks
before any removal (R-836). The product never removes a mirrored folder, and
removes a mirrored playlist in one case only: the INBOX folder's, whose batch
left INBOX (U150), since the batch's tracks remain on the account in their
year, label or set playlists. Any other playlist the tree no longer declares
is left and named.

THE PLAN READS AND WRITES NOTHING. It reads the root folders, each mirrored
folder's playlists and each recorded playlist's tracks, and matches every
library row to an account track through ``match_track``, the matcher ``export
playlist`` uses. A row matched once is linked in the ledger, so a refresh asks
the provider only about rows it has not matched before, and a row it could not
match is remembered with what it was asked under and not asked again until that
changes (R-1031). Several releases that all agree with a row are a tie the
mirror breaks by taking one of them, since a listening copy writes nothing
back as the row's identity, where a heart or a pair refuses it (R-1032). What
exists is reused,
by the ledger's record first and by exact name second, never made twice:

* the folder: the one recorded, or the one root folder of the exact name, or a
  new one. Two root folders of the name refuse that folder by name, since which
  one is the mirror is not something a name decides; the caller plans the rest;
* a playlist: the one recorded, or a new one. A playlist of the same title in
  the folder that the ledger does not record is a person's, and is left alone
  and named rather than adopted, since a person's playlist never loses a track.

THE APPLY RECORDS EACH WRITE AS IT LANDS, :mod:`folders`' rule: the ledger takes
its lock before each create, so an unwritable ledger refuses before anything is
made, and an apply stopped part way leaves every folder and playlist recorded
for the next plan to reuse. Tracks go 100 per request through ``add_tracks``,
never one per call as ``export playlist`` adds them. Removals run last, so a
track moving from one band to another is on its new playlist before it leaves
its old one.

AN EDIT MADE ON THE ACCOUNT IS NOT UNDONE (U201). Each mirrored playlist keeps
its snapshot, the account tracks both sides held when a refresh last finished
it, recorded by the apply, or by the plan for a playlist with nothing to write.
The caller reads each genre playlist three ways (:mod:`mirror_edits`) and hands
in a HOLD per playlist: a track whose edit on the account the library takes, or
one held, is never taken off nor added back here. A playlist whose listing came
back short records no snapshot.

MEMBERSHIP, NOT ORDER. Added tracks are appended; the order inside a mirrored
playlist is not kept equal to rekordbox's, which the plan left to this unit and
this unit leaves out, since membership is the requirement.

Layer: modules.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.mirror_edits import Hold, agreed_after
from cratekit.modules.outbound.service import (
    AGREEING_RELEASES,
    UNREADABLE_CANDIDATE,
    PlaylistListing,
    RemoteAccount,
)

_ORIGIN = ("outbound", "mirror")

#: What happens to a folder, and to each playlist.
CREATE = "create"
REUSE = "reuse"
ADOPT = "adopt"
#: A playlist left alone: a person's of the same title, with nothing made beside it.
LEFT = "left"
#: A playlist left alone because the one recorded is not in the folder and
#: could not be read, which is what one deleted on the account looks like.
UNREADABLE = "unreadable"
#: A retiring folder the account lacks that nothing would go into (U150): not
#: made, since an empty root folder is nothing anyone asked for.
UNMADE = "not made"
#: A mirrored playlist removed from the account because what it mirrors left
#: the rekordbox folder (U150), the INBOX folder's retired batch.
RETIRE = "remove"

#: The refusal of a name two folders take, on the account or in the library.
AMBIGUOUS_REASON = "account-mirror-ambiguous"

#: How many tracks one add carries, :data:`folders.CHUNK`'s number and reason.
CHUNK = 100

#: Why a row is left out of its mirrored playlist, when the account says no more.
NO_ISRC = "the row carries no ISRC, in the database or in its file"
NO_MATCH = "the account has no track this row's ISRC names"

#: What a miss says when a candidate track could not be read, which is not an
#: answer about the row, so the miss is never remembered (R-1031). The
#: adapter formats its reason from the same constant.
UNREAD = UNREADABLE_CANDIDATE

#: What a miss says when it was a tie between agreeing releases, which the
#: matcher no longer misses on (R-1032), so a miss remembered with it before
#: the tie was broken is asked again rather than reused.
TIED = AGREEING_RELEASES


def title(folder: str, playlist: str) -> str:
    """A mirrored playlist's account title, ``<Folder> <Playlist>``."""
    return f"{folder} {playlist}"


@dataclass(frozen=True, slots=True)
class Row:
    """One library membership: the content row and what a match is made from.

    ``isrc`` is the database row's own code, already folded, or empty; the
    file's code is read only when this is empty and the row was never linked.
    """

    content_id: str
    title: str = ""
    artist: str = ""
    isrc: str = ""
    path: str = ""
    #: When the membership was made in rekordbox, as the database writes it,
    #: or ``""``; read for a genre folder only, where an edit's time is asked (U201).
    added: str = ""


@dataclass(frozen=True, slots=True)
class Source:
    """One rekordbox playlist of a folder, under the title its mirror takes."""

    name: str
    rows: tuple[Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Folder:
    """One rekordbox folder to mirror, under the root folder name it takes.

    ``retire`` is the INBOX folder's (U150): a playlist the ledger records as
    mirrored here that the folder no longer declares is REMOVED from the
    account, rather than left, when its title is not in ``present``, the
    account title of every node the rekordbox folder holds now, batch or not.
    One still present that only no longer reads as a batch is left, since
    not recognising a batch is no evidence that it left.
    """

    name: str
    playlists: tuple[Source, ...] = ()
    retire: bool = False
    present: frozenset[str] = frozenset()
    #: A genre folder of the routing tree, whose edits on the account the
    #: library takes (U201); the Favorites folder and INBOX are not, yet.
    genre: bool = False


@dataclass(frozen=True, slots=True)
class Identity:
    """What the account is asked to match a row by: its code, its album, its title."""

    isrc: str = ""
    album: str = ""
    title: str = ""
    #: Whether even one track the code names must agree with the row, which a
    #: code read off the file's own tag asks, since it did not come from the
    #: provider and a file tagged with another recording's code would name the
    #: wrong track (R-879).
    agree: bool = False


class Counted:
    """The account seam with every call counted, the request count a run reports.

    Every member the step calls is one request or more to the provider, and
    the count is of calls through the seam, so a chunked add of 250 tracks is
    three. ``seconds`` is the wall time since construction or the last
    :meth:`lap`.
    """

    def __init__(self, account: RemoteAccount) -> None:
        self._account = account
        self.requests = 0
        self.by_member: dict[str, int] = {}
        self._started = time.monotonic()

    def __getattr__(self, name: str) -> Any:
        member = getattr(self._account, name)
        if not callable(member):
            return member

        def counted(*args: Any, **kwargs: Any) -> Any:
            self.requests += 1
            self.by_member[name] = self.by_member.get(name, 0) + 1
            return member(*args, **kwargs)

        return counted

    def lap(self) -> tuple[int, float]:
        """The requests and seconds since the last lap, and a new lap begun."""
        now = time.monotonic()
        said = (self.requests, round(now - self._started, 2))
        self.requests, self.by_member, self._started = 0, {}, now
        return said


class Matcher:
    """Library rows to account tracks, the ledger's links first, the provider second.

    A LINK IS REUSED while the row's database code is empty or the code it was
    matched under, so a row retagged in the database with another code is
    matched again rather than kept on the old track. ``fresh`` gathers every
    link a plan used that the ledger does not yet hold, for an apply to record.

    A MISS IS REUSED while the row is asked under what it was missed under
    (R-1031): its database code, title, artist and path, and for a row with no
    database code its file's ``signature``, since the file's code is read only
    then. Anything else changing asks the provider again, and ``rematch`` asks
    every remembered miss. ``missed`` gathers each miss a plan found, for the
    ledger, except one whose reason says a candidate could not be read.

    ``seen`` IS A FROZEN PLAN'S MATCHES, every row's answer as the gate's plan
    found it, so a plan rebuilt from them asks the provider about no row they
    carry.

    ``known`` IS EACH ROW'S OWN PROVIDER TRACK (U150), what a label landing
    recorded from the manifest row its file was tied to. It answers a row the
    ledger does not link, before any remembered miss and before the provider,
    since it names the very track the file was downloaded as: no request, and
    no ISRC tie between agreeing releases to miss on.

    A TIE TAKES ONE RELEASE (R-1032). A mirrored playlist is a listening copy
    and writes nothing back as the row's identity, so the provider is asked
    with ``any_agreeing`` and a tie between releases that all agree with the
    row is matched as one of them, linked like any match and so kept by every
    later refresh. A miss remembered with the tie's words before that is asked
    again rather than reused, once, since asking again no longer misses on it.
    The hearts and the pairs keep R-572's refusal; they never pass it.
    """

    def __init__(
        self,
        account: RemoteAccount,
        links: Mapping[str, tuple[str, str]],
        identify: Callable[[Row], Identity],
        *,
        misses: Mapping[str, tuple[str, Sequence[str]]] | None = None,
        signature: Callable[[Row], str] | None = None,
        rematch: bool = False,
        seen: Mapping[str, tuple[str, str, str]] | None = None,
        known: Mapping[str, str] | None = None,
    ) -> None:
        self._account = account
        self._links = dict(links)
        self._identify = identify
        self._misses = {} if rematch else dict(misses or {})
        self._signature = signature or (lambda _row: "")
        self._seen: dict[str, tuple[str, str, str]] = dict(seen or {})
        self._known = {str(cid): str(remote) for cid, remote in (known or {}).items() if remote}
        #: How many rows a recorded provider track answered, never asked of the provider.
        self.known = 0
        self.fresh: dict[str, tuple[str, str]] = {}
        self.missed: dict[str, tuple[str, tuple[str, ...]]] = {}
        #: How many rows a remembered miss answered, never asked of the provider.
        self.remembered = 0

    @property
    def seen(self) -> dict[str, tuple[str, str, str]]:
        """Every row's answer so far, ``(account track, ISRC, reason)``, for freezing."""
        return dict(self._seen)

    def match(self, row: Row) -> tuple[str, str]:
        """``(account track, "")`` for a matched row, ``("", reason)`` otherwise."""
        held = self._seen.get(row.content_id)
        if held is None:
            held = self._match(row)
            self._seen[row.content_id] = held
        remote, isrc, reason = held
        if remote and self._links.get(row.content_id) != (remote, isrc):
            self.fresh[row.content_id] = (remote, isrc)
        return remote, reason

    def under(self, row: Row) -> tuple[str, ...]:
        """What a miss of this row is remembered under, and reused while it holds."""
        return (
            row.isrc,
            row.title,
            row.artist,
            row.path,
            "" if row.isrc else self._signature(row),
        )

    def _match(self, row: Row) -> tuple[str, str, str]:
        linked = self._links.get(row.content_id)
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
            return linked[0], linked[1], ""
        own = self._known.get(row.content_id)
        if own:
            self.known += 1
            return own, row.isrc, ""
        under = self.under(row)
        missed = self._misses.get(row.content_id)
        if missed is not None and tuple(missed[1]) == under and TIED not in missed[0]:
            self.remembered += 1
            return "", "", missed[0]
        said = self._identify(row)
        if not said.isrc:
            return self._missed(row, under, NO_ISRC)
        remote = self._account.match_track(
            identity=row.content_id,
            isrc=said.isrc,
            title=said.title,
            artist=row.artist,
            agree=said.agree,
            album=said.album,
            any_agreeing=True,
        )
        if not remote:
            return self._missed(
                row, under, self._account.unmatched_reason(row.content_id) or NO_MATCH
            )
        return str(remote), said.isrc, ""

    def _missed(self, row: Row, under: tuple[str, ...], reason: str) -> tuple[str, str, str]:
        if UNREAD not in reason:
            self.missed[row.content_id] = (reason, under)
        return "", "", reason

    def links_of(self, rows: Sequence[Row]) -> dict[str, tuple[str, str]]:
        """The fresh links among these rows, what one folder's apply records."""
        return {row.content_id: self.fresh[row.content_id] for row in rows if row.content_id in self.fresh}


@dataclass(frozen=True, slots=True)
class PlaylistPlan:
    """What a refresh does to one mirrored playlist."""

    name: str
    action: str
    remote_id: str = ""
    move: bool = False
    add: tuple[str, ...] = ()
    remove: tuple[str, ...] = ()
    #: How many account tracks the rekordbox playlist matched.
    tracks: int = 0
    #: Each library row left out, named, with why.
    unmatched: tuple[str, ...] = ()
    #: Each track to take off, named, which the gate shows.
    removed_names: tuple[str, ...] = ()
    #: Matched tracks the provider refused before, not asked again.
    refused: int = 0
    why: str = ""
    #: What the snapshot is taken from (U201): the account tracks the playlist
    #: held when planned, its snapshot then, ``None`` for none, the hold the
    #: caller handed in, and whether its listing came back short.
    held: frozenset[str] = frozenset()
    agreed: frozenset[str] | None = None
    hold: Hold = field(default_factory=Hold)
    short: bool = False
    #: Tracks held on the account rather than taken off or added back (U201).
    kept: int = 0

    @property
    def writes(self) -> bool:
        if self.action in (LEFT, UNREADABLE):
            return False
        return self.action == CREATE or self.move or bool(self.add) or bool(self.remove)

    def item(self) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "playlist": self.name,
            "action": self.action,
            "tracks": self.tracks,
            "add": len(self.add),
            "remove": len(self.remove),
        }
        if self.remote_id:
            shown["remote_id"] = self.remote_id
        if self.move:
            shown["move"] = True
        if self.removed_names:
            shown["removed"] = list(self.removed_names)
        if self.unmatched:
            shown["unmatched"] = list(self.unmatched)
        if self.refused:
            shown["refused before"] = self.refused
        if self.kept:
            shown["held as the account has them"] = self.kept
        if self.short:
            shown["short"] = True
        if self.why:
            shown["why"] = self.why
        return shown


@dataclass(frozen=True, slots=True)
class FolderPlan:
    """Everything one folder's gate line is asked over."""

    name: str
    folder_action: str
    folder_id: str = ""
    stale_folder: str = ""
    playlists: tuple[PlaylistPlan, ...] = ()
    #: Mirrored playlists the folder no longer declares, named and left.
    left: tuple[str, ...] = ()
    #: The links this folder's rows used that the ledger does not hold yet.
    links: Mapping[str, tuple[str, str]] = field(default_factory=dict)
    #: Mirrored playlists to remove from the account, ``(title, remote id)``,
    #: whose rekordbox playlist left a retiring folder (U150).
    retire: tuple[tuple[str, str], ...] = ()

    @property
    def writes(self) -> bool:
        return (
            self.folder_action in (CREATE, ADOPT)
            or any(one.writes for one in self.playlists)
            or bool(self.retire)
        )

    def counts(self) -> dict[str, int]:
        return {
            "create folder": int(self.folder_action == CREATE),
            "create playlist": sum(1 for one in self.playlists if one.action == CREATE),
            "add": sum(len(one.add) for one in self.playlists),
            "remove": sum(len(one.remove) for one in self.playlists),
            "unmatched": sum(len(one.unmatched) for one in self.playlists),
            "left": len(self.left)
            + sum(1 for one in self.playlists if one.action in (LEFT, UNREADABLE)),
            "remove playlist": len(self.retire),
        }

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every write, the titles among them."""
        return {
            "kind": "account-mirror",
            "folder": [self.name, self.folder_action, self.folder_id, self.stale_folder],
            "playlists": [
                [one.name, one.action, one.remote_id, one.move, list(one.add), list(one.remove)]
                for one in self.playlists
            ],
            "retire": [list(one) for one in self.retire],
        }

    def items(self) -> list[dict[str, Any]]:
        shown: list[dict[str, Any]] = [
            {
                "folder": self.name,
                "action": self.folder_action,
                **({"folder_id": self.folder_id} if self.folder_id else {}),
            }
        ]
        shown.extend(one.item() for one in self.playlists)
        shown.extend({"playlist": line, "action": LEFT} for line in self.left)
        shown.extend(
            {
                "playlist": name,
                "action": RETIRE,
                "remote_id": remote_id,
                "why": f"what it mirrors left {self.name}, so the product removes the playlist it made",
            }
            for name, remote_id in self.retire
        )
        return shown


def ambiguous(name: str, found: Sequence[str]) -> CratekitError:
    """Two root folders of a mirror's name: that folder refused by name, nothing written."""
    return refuse(
        AMBIGUOUS_REASON,
        f"the account holds {len(found)} root folders named {name!r}, so which one "
        f"is the mirror is not something its name decides, and nothing was planned "
        f"for it",
        steps=(
            "rename or merge the extra folders on the account so one carries the "
            "name, then run organize again",
        ),
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={"folders": list(found), "name": name},
    )


def _wanted(source: Source, matcher: Matcher) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """The account tracks a rekordbox playlist matched, in its order, and each row left out."""
    wanted: list[str] = []
    unmatched: list[str] = []
    for row in source.rows:
        remote, reason = matcher.match(row)
        if remote:
            wanted.append(remote)
        else:
            unmatched.append(f"{row.artist} - {row.title}: {reason}")
    return tuple(dict.fromkeys(wanted)), tuple(unmatched)


def plan(
    folder: Folder,
    account: RemoteAccount,
    *,
    recorded: ledger.MirrorFolder | None,
    root: Mapping[str, str],
    matcher: Matcher,
    holds: Mapping[str, Hold] | None = None,
    listings: Mapping[str, PlaylistListing] | None = None,
) -> FolderPlan:
    """Decide one mirrored folder and every playlist in it. Reads only.

    ``root`` is the account's root folders, identifier to name, read once by
    the caller for every folder. Raises :func:`ambiguous` for two root folders
    of the name. ``holds`` is each playlist's hold by title (U201), and
    ``listings`` each recorded playlist's listing the caller already read, by
    remote identifier, so it is not read twice.
    """
    holds = holds or {}
    listings = listings or {}
    stale = ""
    held_id = recorded.folder_id if recorded is not None else ""
    if held_id and held_id in root:
        folder_action, folder_id = REUSE, held_id
    else:
        stale = held_id
        named = sorted(fid for fid, name in root.items() if name == folder.name)
        if len(named) > 1:
            raise ambiguous(folder.name, named)
        if named:
            folder_action, folder_id = ADOPT, named[0]
        else:
            folder_action, folder_id = CREATE, ""
    # A RETIRING FOLDER IS MADE ONLY TO HOLD SOMETHING (U150): an INBOX with no
    # live batch, or one whose folder a person deleted with only removals
    # left, makes no empty root folder.
    if folder_action == CREATE and folder.retire and not folder.playlists:
        folder_action = UNMADE
    inside = account.folder_playlists(folder_id) if folder_id else {}
    made = dict(recorded.playlists) if recorded is not None else {}

    steps: list[PlaylistPlan] = []
    for source in folder.playlists:
        mine = made.get(source.name)
        if mine is not None:
            placed = mine.remote_id in inside
            # ONE READ PER PLAYLIST, names and all: the names are what the gate
            # shows a removal by, and the adapter keeps the membership it read
            # for the add that follows.
            try:
                listing = listings.get(mine.remote_id)
                if listing is None:
                    listing = account.playlist_listing(mine.remote_id)
            except CratekitError as exc:
                if placed or exc.cause.reason != "unavailable-transient":
                    raise
                steps.append(
                    PlaylistPlan(
                        name=source.name,
                        action=UNREADABLE,
                        remote_id=mine.remote_id,
                        why=(
                            "the playlist recorded for it is not in the folder and could "
                            "not be read, so it may have been deleted on the account; "
                            "nothing is made in its place"
                        ),
                    )
                )
                continue
            names = listing.names
            hold = holds.get(source.name, Hold())
            wanted, unmatched = _wanted(source, matcher)
            on = set(names)
            keep = set(wanted)
            remove = tuple(one for one in names if one not in keep and one not in hold.keep)
            steps.append(
                PlaylistPlan(
                    name=source.name,
                    action=REUSE,
                    remote_id=mine.remote_id,
                    move=not placed,
                    add=tuple(
                        one
                        for one in wanted
                        if one not in on and one not in mine.refused and one not in hold.skip
                    ),
                    remove=remove,
                    tracks=len(wanted),
                    unmatched=unmatched,
                    removed_names=tuple(
                        f"{names[one][0]} - {names[one][1]} ({one})" for one in remove
                    ),
                    refused=sum(1 for one in wanted if one in mine.refused and one not in on),
                    held=frozenset(on),
                    agreed=mine.agreed,
                    hold=hold,
                    short=listing.short,
                    kept=len(
                        [one for one in names if one not in keep and one in hold.keep]
                        + [one for one in wanted if one not in on and one in hold.skip]
                    ),
                )
            )
            continue
        # A PERSON'S PLAYLIST IS DECIDED BEFORE ANY ROW IS MATCHED, since
        # nothing is written to it and a match would be a request for nothing.
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if theirs:
            steps.append(
                PlaylistPlan(
                    name=source.name,
                    action=LEFT,
                    remote_id=theirs[0],
                    why=(
                        f"the folder holds {len(theirs)} playlist(s) of this title the "
                        f"product did not make, so a person's playlist is left as it is "
                        f"and nothing is made beside it; rename it on the account to "
                        f"let the mirror make its own"
                    ),
                )
            )
            continue
        wanted, unmatched = _wanted(source, matcher)
        steps.append(
            PlaylistPlan(
                name=source.name,
                action=CREATE,
                move=True,
                add=wanted,
                tracks=len(wanted),
                unmatched=unmatched,
            )
        )
    declared = {source.name for source in folder.playlists}
    left: list[str] = []
    retire: list[tuple[str, str]] = []
    for name, entry in sorted(made.items()):
        if name in declared:
            continue
        if not folder.retire:
            left.append(
                f"{name} ({entry.remote_id}): the folder no longer declares it, so it is "
                f"left on the account as it is"
            )
        elif name in folder.present:
            # STILL THERE, ONLY NOT RECOGNISED. A landing record that could not
            # be read, or a batch folder gone, unrecognises a batch that never
            # left; removing its playlist would read absence as evidence.
            left.append(
                f"{name} ({entry.remote_id}): still in {folder.name} in rekordbox but no "
                f"longer read as one to mirror, so it is left on the account as it is"
            )
        else:
            retire.append((name, entry.remote_id))
    rows = [row for source in folder.playlists for row in source.rows]
    return FolderPlan(
        name=folder.name,
        folder_action=folder_action,
        folder_id=folder_id,
        stale_folder=stale,
        playlists=tuple(steps),
        left=tuple(left),
        links=matcher.links_of(rows),
        retire=tuple(retire),
    )


def settled(planned: FolderPlan) -> dict[str, tuple[str, frozenset[str]]]:
    """The snapshot of each playlist with nothing to write, by title (U201).

    Such a playlist is already as the mirror would leave it, so its snapshot is
    taken at the plan, which the apply of a folder with no write never reaches.
    A playlist whose listing was short records none.
    """
    return {
        one.name: (one.remote_id, agreed_after(one.agreed, one.held, one.hold))
        for one in planned.playlists
        if one.action == REUSE and not one.writes and not one.short and one.remote_id
    }


@dataclass
class Applied:
    """What an apply wrote, for the report and for a failure part way."""

    folder_id: str = ""
    folder_created: bool = False
    created: list[str] = field(default_factory=list)
    moved: list[str] = field(default_factory=list)
    added: dict[str, int] = field(default_factory=dict)
    refused: dict[str, int] = field(default_factory=dict)
    removed: dict[str, int] = field(default_factory=dict)
    #: Playlists a removal was refused on, each with the refusal's words.
    kept: list[tuple[str, str]] = field(default_factory=list)
    #: Mirrored playlists removed from the account (U150).
    retired: list[str] = field(default_factory=list)

    def totals(self) -> dict[str, Any]:
        return {
            "folder_id": self.folder_id,
            "folder_created": self.folder_created,
            "created": list(self.created),
            "moved": list(self.moved),
            "added": sum(self.added.values()),
            "refused": sum(self.refused.values()),
            "removed": sum(self.removed.values()),
            "kept": [f"{name}: {why}" for name, why in self.kept],
            "retired": list(self.retired),
        }


def apply(
    cfg: config.Config,
    account: RemoteAccount,
    planned: FolderPlan,
    done: Applied,
    *,
    links: Mapping[str, tuple[str, str]] | None = None,
) -> Applied:
    """Carry out one folder's plan, recording each write as it lands, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was
    written before the raise. ``links`` are the rows to record as matched,
    the folder's own by default; a caller planning several folders hands every
    one its run matched, so a folder with nothing to write does not leave its
    rows to be matched again.

    A REMOVAL REFUSED WITH NOTHING SENT, ``outbound-remove-refused`` at source
    scope (positions unknown, or a playlist the ledger does not vouch for), is
    kept and named and the apply goes on, since the adds already landed and the
    other playlists are their own. ANY OTHER REFUSAL IS RAISED, the read back
    that differs above all: a track other than the asked ones may have come
    off, and the refusal's own words say to check the playlist by hand.
    """
    ledger.record_mirror_links(cfg, planned.links if links is None else links)
    if planned.folder_action == UNMADE:
        folder_id, created = "", False
    else:
        folder_id, created = ledger.reserve_mirror_folder(
            cfg,
            planned.name,
            lambda: account.create_folder(planned.name),
            adopt=planned.folder_id if planned.folder_action == ADOPT else "",
            stale=planned.stale_folder,
        )
    done.folder_id, done.folder_created = folder_id, created
    remote_of: dict[str, str] = {}
    added_to: dict[str, set[str]] = {}
    for step in planned.playlists:
        if step.action in (LEFT, UNREADABLE):
            continue
        remote_id, made = ledger.reserve_mirror_playlist(
            cfg, planned.name, step.name, lambda step=step: account.create_playlist(step.name)
        )
        remote_of[step.name] = remote_id
        if made:
            done.created.append(step.name)
        if made or step.move:
            account.move_to_folder(remote_id, folder_id)
            done.moved.append(step.name)
        for start in range(0, len(step.add), CHUNK):
            chunk = step.add[start : start + CHUNK]
            held = set(account.add_tracks(remote_id, chunk))
            added_to.setdefault(step.name, set()).update(
                str(one) for one in chunk if one in held
            )
            refused = [one for one in chunk if one not in held]
            ledger.record_mirror_refused(cfg, planned.name, step.name, refused)
            done.added[step.name] = done.added.get(step.name, 0) + len(chunk) - len(refused)
            if refused:
                done.refused[step.name] = done.refused.get(step.name, 0) + len(refused)
    landed: dict[str, set[str]] = {}
    for step in planned.playlists:
        if not step.remove or step.name not in remote_of:
            continue
        try:
            gone = account.remove_tracks(remote_of[step.name], step.remove)
        except CratekitError as exc:
            if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:
                raise
            done.kept.append((step.name, exc.cause.message))
            continue
        done.removed[step.name] = len(gone)
        landed[step.name] = {str(one) for one in gone}
    # THE SNAPSHOT, ONCE EVERY WRITE OF THE FOLDER LANDED (U201): what each
    # playlist held, less what came off, with what went on.
    ledger.record_mirror_agreed(
        cfg,
        planned.name,
        {
            step.name: (
                remote_of[step.name],
                agreed_after(
                    step.agreed,
                    (set(step.held) - landed.get(step.name, set())) | added_to.get(step.name, set()),
                    step.hold,
                ),
            )
            for step in planned.playlists
            if step.name in remote_of and not step.short
        },
    )
    # A RETIRED PLAYLIST GOES LAST, AND ITS RECORD AFTER IT (U150). Removed
    # first, so a ledger write that fails leaves a record the next plan
    # retires again, and the adapter answers a playlist already gone as
    # removed; forgotten first, a removal that failed would leave a playlist
    # no record vouches for, which nothing could then remove.
    for name, remote_id in planned.retire:
        try:
            account.remove_playlist(remote_id)
        except CratekitError as exc:
            if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:
                raise
            done.kept.append((name, exc.cause.message))
            continue
        ledger.forget_mirror_playlist(cfg, planned.name, name, remote_id)
        done.retired.append(name)
    return done


__all__ = [
    "ADOPT",
    "AMBIGUOUS_REASON",
    "Applied",
    "CHUNK",
    "CREATE",
    "Counted",
    "Folder",
    "FolderPlan",
    "Identity",
    "LEFT",
    "Matcher",
    "NO_ISRC",
    "NO_MATCH",
    "PlaylistPlan",
    "RETIRE",
    "REUSE",
    "Row",
    "Source",
    "UNMADE",
    "UNREAD",
    "UNREADABLE",
    "ambiguous",
    "apply",
    "plan",
    "settled",
    "title",
]
