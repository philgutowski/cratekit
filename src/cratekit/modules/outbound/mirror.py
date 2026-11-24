"""A rekordbox folder mirrored onto the streaming account as one flat root folder (U147).

THE SHAPE. Every genre folder of the routing tree, and the Favorites folder, is
copied to the account as one root folder of the same name holding one private
playlist per rekordbox playlist. The root is flat (2026-10-13) because the
provider's app draws no nested folder, and a playlist's title carries its
folder, ``Deep House Low``, because the account's search shows a title alone.
The caller hands in the titles.

A MIRROR, NOT AN EXPORT. Each mirrored playlist ends a refresh holding exactly
the account tracks of its rekordbox playlist, a track added on the account by
hand included, which is safe because the ledger records every mirrored playlist
as one the product created and the account seam asks it before any removal
(R-836). A mirrored folder is never removed, and a mirrored playlist only when
it is the INBOX folder's and its batch left INBOX (U150); any other playlist the
tree no longer declares is left and named.

THE PLAN READS AND WRITES NOTHING. Every library row is matched through
``match_track``; a match is linked in the ledger and a miss remembered with
what it was asked under (R-1031), so a refresh asks only about new rows. A tie
between agreeing releases is broken by taking one (R-1032, pairs since U208),
since a listening copy writes nothing back. A folder is reused by the ledger's
record, then by its one exact name, else made; two of the name refuse it. A
playlist is reused by the ledger's record, else made; one of the same title the
ledger does not record is a person's, left and named.

THE APPLY RECORDS EACH WRITE AS IT LANDS, :mod:`folders`' rule, so a stopped
apply leaves everything recorded for the next plan. Tracks go 100 per add;
removals run last, so a track moving bands is on its new playlist first.

AN EDIT MADE ON THE ACCOUNT IS NOT UNDONE (U201, U204). Each playlist keeps a
snapshot of what both sides held when a refresh last finished it, and the
caller hands in a HOLD per playlist (:mod:`mirror_edits`): a held track is never
taken off nor added back. A short listing keeps the snapshot's word on every
track it did not list. Membership is mirrored, not order.

Layer: modules.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import folders, ledger
from cratekit.modules.outbound.mirror_edits import Hold
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
#: A person's playlist of the same title, left with nothing made beside it.
LEFT = "left"
#: The recorded playlist is not in the folder and could not be read, as one
#: deleted on the account looks.
UNREADABLE = "unreadable"
#: A retiring folder the account lacks that nothing would go into (U150).
UNMADE = "not made"
#: A mirrored playlist removed because what it mirrors left the folder (U150).
RETIRE = "remove"

#: The refusal of a name two folders take, on the account or in the library.
AMBIGUOUS_REASON = "account-mirror-ambiguous"

#: How many tracks one add carries, :data:`folders.CHUNK`'s number and reason.
CHUNK = 100

#: Why a row is left out of its mirrored playlist, when the account says no more.
NO_ISRC = "the row carries no ISRC, in the database or in its file"
NO_MATCH = "the account has no track this row's ISRC names"

#: A candidate that could not be read says nothing of the row, so such a miss
#: is never remembered (R-1031).
UNREAD = UNREADABLE_CANDIDATE

#: A miss remembered with a tie's words before ties were broken (R-1032) is
#: asked again rather than reused.
TIED = AGREEING_RELEASES


def title(folder: str, playlist: str) -> str:
    """A mirrored playlist's account title, ``<Folder> <Playlist>``."""
    return f"{folder} {playlist}"


@dataclass(frozen=True, slots=True)
class Row:
    """One library membership. ``isrc`` is the database's own code, folded, or empty."""

    content_id: str
    title: str = ""
    artist: str = ""
    isrc: str = ""
    path: str = ""
    #: When the membership was made in rekordbox, or ``""``; read for a genre
    #: folder only, where an edit's time is asked (U201).
    added: str = ""


@dataclass(frozen=True, slots=True)
class Source:
    """One rekordbox playlist of a folder, under the title its mirror takes."""

    name: str
    rows: tuple[Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Folder:
    """One rekordbox folder to mirror, under the root folder name it takes.

    ``retire`` is INBOX's (U150): a recorded playlist the folder no longer
    declares is removed unless its title is in ``present``, every node the
    folder holds now, since not recognising a batch is no evidence it left.
    """

    name: str
    playlists: tuple[Source, ...] = ()
    retire: bool = False
    present: frozenset[str] = frozenset()
    #: The edit rule reading it, ``mirror_edits.GENRE``, ``FAVORITES``,
    #: ``INBOX`` or ``WIP``, or ``""`` for a folder mirrored one way.
    edits: str = ""
    #: Each node of the folder that is not mirrored, ``(label, reason)`` (U214).
    unmirrored: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class Identity:
    """What the account is asked to match a row by: its code, its album, its title."""

    isrc: str = ""
    album: str = ""
    title: str = ""
    #: A code read off the file's own tag must agree with the row, since a file
    #: tagged with another recording's code would name the wrong track (R-879).
    agree: bool = False


#: Members that return the requests they made, counted by that number (U207).
SCREENS = frozenset({"screen_isrcs"})


class Counted:
    """The account seam with every call counted, the request count a run reports.

    A chunked add of 250 tracks is three; ``seconds`` runs from construction
    or the last :meth:`lap`.
    """

    def __init__(self, account: RemoteAccount) -> None:
        self._account = account
        self.requests = 0
        self.by_member: dict[str, int] = {}
        self._started = time.monotonic()

    def _count(self, name: str, spent: int) -> None:
        self.requests += spent
        self.by_member[name] = self.by_member.get(name, 0) + spent

    def __getattr__(self, name: str) -> Any:
        member = getattr(self._account, name)
        if not callable(member):
            return member

        def counted(*args: Any, **kwargs: Any) -> Any:
            if name in SCREENS:
                # A SCREEN SAYS WHAT IT SPENT (U207), one per batch at most.
                made = member(*args, **kwargs)
                self._count(name, int(made or 0))
                return made
            self._count(name, 1)
            return member(*args, **kwargs)

        return counted

    def lap(self) -> tuple[int, float]:
        """The requests and seconds since the last lap, and a new lap begun."""
        now = time.monotonic()
        said = (self.requests, round(now - self._started, 2))
        self.requests, self.by_member, self._started = 0, {}, now
        return said


class Matcher:
    """Library rows to account tracks: what is already known first, the provider second.

    A LINK is reused while the row's database code is empty or the one it was
    matched under, so a retagged row is matched again. A MISS is reused while
    the row is asked under what it was missed under (R-1031), :meth:`under`;
    ``rematch`` asks every miss again. ``known`` is each row's own provider
    track from a label landing (U150), answered before any miss or request.
    ``seen`` is a frozen plan's answers, so a rebuilt plan asks about none of
    its rows. A tie between agreeing releases is matched as one of them
    (R-1032), since a mirror writes nothing back; the hearts keep R-572's
    refusal. ``fresh`` and ``missed`` gather what an apply records.
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
        #: Rows a recorded provider track, or a remembered miss, answered.
        self.known = 0
        self.remembered = 0
        self.fresh: dict[str, tuple[str, str]] = {}
        self.missed: dict[str, tuple[str, tuple[str, ...]]] = {}
        #: Each content row's identity, read once (U207).
        self._identities: dict[str, Identity] = {}

    @property
    def seen(self) -> dict[str, tuple[str, str, str]]:
        """Every row's answer so far, ``(account track, ISRC, reason)``, for freezing."""
        return dict(self._seen)

    def _link(self, content_id: str, remote: str, isrc: str) -> None:
        if self._links.get(content_id) != (remote, isrc):
            self.fresh[content_id] = (remote, isrc)

    def match(self, row: Row) -> tuple[str, str]:
        """``(account track, "")`` for a matched row, ``("", reason)`` otherwise."""
        held = self._seen.get(row.content_id)
        if held is None:
            held = self._seen[row.content_id] = self._match(row)
        remote, isrc, reason = held
        if remote:
            self._link(row.content_id, remote, isrc)
        return remote, reason

    def adopt(self, content_id: str, remote: str) -> None:
        """Answer one row as the account track a mirror download fetched it as (U204).

        That row is that very track, so it is linked as it even where the
        provider broke a tie toward another release; called before any plan
        reads the rows, so every plan of the run reads one answer.
        """
        content_id, remote = str(content_id), str(remote)
        isrc = self._seen.get(content_id, ("", "", ""))[1]
        self._seen[content_id] = (remote, isrc, "")
        self._link(content_id, remote, isrc)

    def under(self, row: Row) -> tuple[str, ...]:
        """What a miss of this row is remembered under; the file's signature only without a code."""
        return (row.isrc, row.title, row.artist, row.path, "" if row.isrc else self._signature(row))

    def _settled(self, row: Row) -> tuple[str, tuple[str, str, str]] | None:
        """How a row is answered with no request, ``(kind, answer)``, or None.

        Reads only, so the screen and :meth:`_match` ask it alike (U207).
        """
        if row.content_id in self._seen:
            return "seen", self._seen[row.content_id]
        linked = self._links.get(row.content_id)
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
            return "linked", (linked[0], linked[1], "")
        own = self._known.get(row.content_id)
        if own:
            return "known", (own, row.isrc, "")
        missed = self._misses.get(row.content_id)
        if missed is not None and tuple(missed[1]) == self.under(row) and TIED not in missed[0]:
            return "remembered", ("", "", missed[0])
        return None

    def _identity(self, row: Row) -> Identity:
        """What the row is matched by, read once per content row, a file's tag included."""
        held = self._identities.get(row.content_id)
        if held is None:
            held = self._identities[row.content_id] = self._identify(row)
        return held

    def screen(self, rows: Iterable[Row]) -> int:
        """Screen every code these rows will ask, before any is asked; the requests made (U207)."""
        codes = [
            said.isrc
            for row in rows
            if self._settled(row) is None and (said := self._identity(row)).isrc
        ]
        return self._account.screen_isrcs(codes) if codes else 0

    def _match(self, row: Row) -> tuple[str, str, str]:
        settled = self._settled(row)
        if settled is not None:
            kind, answer = settled
            if kind == "known":
                self.known += 1
            elif kind == "remembered":
                self.remembered += 1
            return answer
        under = self.under(row)
        said = self._identity(row)
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
            reason = self._account.unmatched_reason(row.content_id) or NO_MATCH
            return self._missed(row, under, reason)
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
    #: What the snapshot is taken from (U201): the tracks held when planned,
    #: the snapshot then, the caller's hold, and whether the listing was short.
    held: frozenset[str] = frozenset()
    agreed: frozenset[str] | None = None
    hold: Hold = field(default_factory=Hold)
    short: bool = False
    #: Tracks held on the account rather than taken off or added back (U201).
    kept: int = 0

    def unlisted(self, gone: frozenset[str] = frozenset()) -> frozenset[str]:
        """Tracks a short listing's snapshot keeps its word on: agreed, not listed, not taken off."""
        if not self.short or self.agreed is None:
            return frozenset()
        return frozenset(self.agreed) - self.held - gone

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
        optional = (
            ("remote_id", self.remote_id),
            ("move", self.move),
            ("removed", list(self.removed_names)),
            ("unmatched", list(self.unmatched)),
            ("refused before", self.refused),
            ("held as the account has them", self.kept),
            ("short", self.short),
            ("why", self.why),
        )
        return shown | {key: value for key, value in optional if value}


@dataclass(frozen=True, slots=True)
class FolderPlan:
    """Everything one folder's gate line is asked over."""

    name: str
    folder_action: str
    folder_id: str = ""
    stale_folder: str = ""
    playlists: tuple[PlaylistPlan, ...] = ()
    #: Mirrored playlists the folder no longer declares, and each node it does
    #: not mirror (U214), named and left.
    left: tuple[str, ...] = ()
    #: The links this folder's rows used that the ledger does not hold yet.
    links: Mapping[str, tuple[str, str]] = field(default_factory=dict)
    #: Mirrored playlists to remove, ``(title, remote id)`` (U150).
    retire: tuple[tuple[str, str], ...] = ()

    @property
    def writes(self) -> bool:
        return (
            self.folder_action in (CREATE, ADOPT)
            or any(one.writes for one in self.playlists)
            or bool(self.retire)
        )

    def counts(self) -> dict[str, int]:
        steps = self.playlists
        return {
            "create folder": int(self.folder_action == CREATE),
            "create playlist": sum(1 for one in steps if one.action == CREATE),
            "add": sum(len(one.add) for one in steps),
            "remove": sum(len(one.remove) for one in steps),
            "unmatched": sum(len(one.unmatched) for one in steps),
            "left": len(self.left) + sum(1 for one in steps if one.action in (LEFT, UNREADABLE)),
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
        head = {"folder": self.name, "action": self.folder_action}
        why = f"what it mirrors left {self.name}, so the product removes the playlist it made"
        return [
            head | ({"folder_id": self.folder_id} if self.folder_id else {}),
            *(one.item() for one in self.playlists),
            *({"playlist": line, "action": LEFT} for line in self.left),
            *(
                {"playlist": name, "action": RETIRE, "remote_id": remote_id, "why": why}
                for name, remote_id in self.retire
            ),
        ]


def ambiguous(name: str, found: Sequence[str]) -> CratekitError:
    """Two root folders of a mirror's name: that folder refused by name, nothing written."""
    return refuse(
        AMBIGUOUS_REASON,
        f"the account holds {len(found)} root folders named {name!r}, so which one is the mirror "
        f"is not something its name decides, and nothing was planned for it",
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


def _reused(
    source: Source,
    mine: ledger.MirrorPlaylist,
    listing: PlaylistListing,
    placed: bool,
    hold: Hold,
    matcher: Matcher,
) -> PlaylistPlan:
    """A recorded playlist's step: what to add and take off, a hold's tracks left as they are."""
    names = listing.names
    wanted, unmatched = _wanted(source, matcher)
    on = set(names)
    keep = set(wanted)
    remove = tuple(one for one in names if one not in keep and one not in hold.keep)
    return PlaylistPlan(
        name=source.name,
        action=REUSE,
        remote_id=mine.remote_id,
        move=not placed,
        add=tuple(
            one for one in wanted if one not in on and one not in mine.refused and one not in hold.skip
        ),
        remove=remove,
        tracks=len(wanted),
        unmatched=unmatched,
        removed_names=tuple(f"{names[one][0]} - {names[one][1]} ({one})" for one in remove),
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

    ``root`` is the account's root folders, identifier to name, read once for
    every folder; two of the name raise :func:`ambiguous`. ``holds`` is each
    playlist's hold by title (U201), ``listings`` each recorded playlist's
    listing already read, by remote identifier.
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
        folder_action, folder_id = (ADOPT, named[0]) if named else (CREATE, "")
    # A RETIRING FOLDER IS MADE ONLY TO HOLD SOMETHING (U150).
    if folder_action == CREATE and folder.retire and not folder.playlists:
        folder_action = UNMADE
    inside = account.folder_playlists(folder_id) if folder_id else {}
    made = dict(recorded.playlists) if recorded is not None else {}

    steps: list[PlaylistPlan] = []
    for source in folder.playlists:
        mine = made.get(source.name)
        if mine is not None:
            placed = mine.remote_id in inside
            # ONE READ PER PLAYLIST, names and all, which the gate shows a
            # removal by and the adapter keeps for the add that follows.
            try:
                listing = listings.get(mine.remote_id)
                if listing is None:
                    listing = account.playlist_listing(mine.remote_id)
            except CratekitError as exc:
                if placed or exc.cause.reason != "unavailable-transient":
                    raise
                why = (
                    "the playlist recorded for it is not in the folder and could not be read, so "
                    "it may have been deleted on the account; nothing is made in its place"
                )
                steps.append(PlaylistPlan(source.name, UNREADABLE, mine.remote_id, why=why))
                continue
            hold = holds.get(source.name, Hold())
            steps.append(_reused(source, mine, listing, placed, hold, matcher))
            continue
        # A PERSON'S PLAYLIST IS DECIDED BEFORE ANY ROW IS MATCHED, since a
        # match would be a request for nothing.
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if theirs:
            why = (
                f"the folder holds {len(theirs)} playlist(s) of this title the product did not "
                f"make, so a person's playlist is left as it is and nothing is made beside it; "
                f"rename it on the account to let the mirror make its own"
            )
            steps.append(PlaylistPlan(source.name, LEFT, theirs[0], why=why))
            continue
        wanted, unmatched = _wanted(source, matcher)
        steps.append(
            PlaylistPlan(
                source.name, CREATE, move=True, add=wanted, tracks=len(wanted), unmatched=unmatched
            )
        )
    declared = {source.name for source in folder.playlists}
    left = [f"{label}: not mirrored, {reason}" for label, reason in folder.unmirrored]
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
            # STILL THERE, ONLY NOT RECOGNISED: absence is no evidence it left.
            left.append(
                f"{name} ({entry.remote_id}): still in {folder.name} in rekordbox but no "
                f"longer read as one to mirror, so it is left on the account as it is"
            )
        else:
            retire.append((name, entry.remote_id))
    return FolderPlan(
        name=folder.name,
        folder_action=folder_action,
        folder_id=folder_id,
        stale_folder=stale,
        playlists=tuple(steps),
        left=tuple(left),
        links=matcher.links_of([row for source in folder.playlists for row in source.rows]),
        retire=tuple(retire),
    )


def settled(planned: FolderPlan) -> dict[str, tuple[str, frozenset[str], frozenset[str]]]:
    """The snapshot of each playlist with nothing to write, by title, taken at the plan (U201)."""
    return {
        one.name: (one.remote_id, one.held, one.hold.tracks | one.unlisted())
        for one in planned.playlists
        if one.action == REUSE and not one.writes and one.remote_id
    }


@dataclass
class Applied(folders.Applied):
    """What an apply wrote, for the report and for a failure part way."""

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


def _kept(exc: CratekitError, name: str, done: Applied) -> None:
    """A removal refused with nothing sent is kept and named; any other refusal is raised."""
    if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:
        raise exc
    done.kept.append((name, exc.cause.message))


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
    written. ``links`` are the rows to record as matched, the folder's own by
    default; a caller planning several folders hands each every one its run
    matched. A removal refused with nothing sent (``outbound-remove-refused``
    at source scope) is kept and named, since the adds landed; any other
    refusal, a read back that differs above all, is raised.
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
            added_to.setdefault(step.name, set()).update(str(one) for one in chunk if one in held)
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
            _kept(exc, step.name, done)
            continue
        done.removed[step.name] = len(gone)
        landed[step.name] = {str(one) for one in gone}
    # THE SNAPSHOT, ONCE EVERY WRITE OF THE FOLDER LANDED (U201): what each
    # playlist held, less what came off, with what went on.
    snapshot = {}
    for step in planned.playlists:
        if step.name in remote_of:
            gone = frozenset(landed.get(step.name, set()))
            after = (set(step.held) - gone) | added_to.get(step.name, set())
            snapshot[step.name] = (
                remote_of[step.name],
                frozenset(after),
                step.hold.tracks | step.unlisted(gone),
            )
    ledger.record_mirror_agreed(cfg, planned.name, snapshot)
    # A RETIRED PLAYLIST GOES LAST, AND ITS RECORD AFTER IT (U150), so a ledger
    # write that fails leaves a record the next plan retires again, never a
    # playlist no record vouches for.
    for name, remote_id in planned.retire:
        try:
            account.remove_playlist(remote_id)
        except CratekitError as exc:
            _kept(exc, name, done)
            continue
        ledger.forget_mirror_playlist(cfg, planned.name, name, remote_id)
        done.retired.append(name)
    return done


__all__ = [
    "ADOPT", "AMBIGUOUS_REASON", "Applied", "CHUNK", "CREATE", "Counted", "Folder",
    "FolderPlan", "Identity", "LEFT", "Matcher", "NO_ISRC", "NO_MATCH", "PlaylistPlan",
    "RETIRE", "REUSE", "Row", "Source", "UNMADE", "UNREAD", "UNREADABLE", "ambiguous", "apply",
    "plan", "settled", "title",
]
