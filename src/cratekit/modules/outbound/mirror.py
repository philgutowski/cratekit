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
before any removal (R-836). The product never removes a mirrored folder or
playlist: one the tree no longer declares is left and named.

THE PLAN READS AND WRITES NOTHING. It reads the root folders, each mirrored
folder's playlists and each recorded playlist's tracks, and matches every
library row to an account track through ``match_track``, the matcher ``export
playlist`` uses. A row matched once is linked in the ledger, so a refresh asks
the provider only about rows it has not matched before. What exists is reused,
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
from cratekit.modules.outbound.service import RemoteAccount

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

#: The refusal of a name two folders take, on the account or in the library.
AMBIGUOUS_REASON = "account-mirror-ambiguous"

#: How many tracks one add carries, :data:`folders.CHUNK`'s number and reason.
CHUNK = 100

#: Why a row is left out of its mirrored playlist, when the account says no more.
NO_ISRC = "the row carries no ISRC, in the database or in its file"
NO_MATCH = "the account has no track this row's ISRC names"


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


@dataclass(frozen=True, slots=True)
class Source:
    """One rekordbox playlist of a folder, under the title its mirror takes."""

    name: str
    rows: tuple[Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Folder:
    """One rekordbox folder to mirror, under the root folder name it takes."""

    name: str
    playlists: tuple[Source, ...] = ()


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
    """

    def __init__(
        self,
        account: RemoteAccount,
        links: Mapping[str, tuple[str, str]],
        identify: Callable[[Row], Identity],
    ) -> None:
        self._account = account
        self._links = dict(links)
        self._identify = identify
        self._seen: dict[str, tuple[str, str, str]] = {}
        self.fresh: dict[str, tuple[str, str]] = {}

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

    def _match(self, row: Row) -> tuple[str, str, str]:
        linked = self._links.get(row.content_id)
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
            return linked[0], linked[1], ""
        said = self._identify(row)
        if not said.isrc:
            return "", "", NO_ISRC
        remote = self._account.match_track(
            identity=row.content_id,
            isrc=said.isrc,
            title=said.title,
            artist=row.artist,
            agree=said.agree,
            album=said.album,
        )
        if not remote:
            return "", "", self._account.unmatched_reason(row.content_id) or NO_MATCH
        return str(remote), said.isrc, ""

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

    @property
    def writes(self) -> bool:
        return self.folder_action in (CREATE, ADOPT) or any(one.writes for one in self.playlists)

    def counts(self) -> dict[str, int]:
        return {
            "create folder": int(self.folder_action == CREATE),
            "create playlist": sum(1 for one in self.playlists if one.action == CREATE),
            "add": sum(len(one.add) for one in self.playlists),
            "remove": sum(len(one.remove) for one in self.playlists),
            "unmatched": sum(len(one.unmatched) for one in self.playlists),
            "left": len(self.left)
            + sum(1 for one in self.playlists if one.action in (LEFT, UNREADABLE)),
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
) -> FolderPlan:
    """Decide one mirrored folder and every playlist in it. Reads only.

    ``root`` is the account's root folders, identifier to name, read once by
    the caller for every folder. Raises :func:`ambiguous` for two root folders
    of the name.
    """
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
                names = account.track_names(mine.remote_id)
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
            wanted, unmatched = _wanted(source, matcher)
            on = set(names)
            keep = set(wanted)
            remove = tuple(one for one in names if one not in keep)
            steps.append(
                PlaylistPlan(
                    name=source.name,
                    action=REUSE,
                    remote_id=mine.remote_id,
                    move=not placed,
                    add=tuple(one for one in wanted if one not in on and one not in mine.refused),
                    remove=remove,
                    tracks=len(wanted),
                    unmatched=unmatched,
                    removed_names=tuple(
                        f"{names[one][0]} - {names[one][1]} ({one})" for one in remove
                    ),
                    refused=sum(1 for one in wanted if one in mine.refused and one not in on),
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
    left = tuple(
        f"{name} ({entry.remote_id}): the folder no longer declares it, so it is left "
        f"on the account as it is"
        for name, entry in sorted(made.items())
        if name not in declared
    )
    rows = [row for source in folder.playlists for row in source.rows]
    return FolderPlan(
        name=folder.name,
        folder_action=folder_action,
        folder_id=folder_id,
        stale_folder=stale,
        playlists=tuple(steps),
        left=left,
        links=matcher.links_of(rows),
    )


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
    folder_id, created = ledger.reserve_mirror_folder(
        cfg,
        planned.name,
        lambda: account.create_folder(planned.name),
        adopt=planned.folder_id if planned.folder_action == ADOPT else "",
        stale=planned.stale_folder,
    )
    done.folder_id, done.folder_created = folder_id, created
    remote_of: dict[str, str] = {}
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
            refused = [one for one in chunk if one not in held]
            ledger.record_mirror_refused(cfg, planned.name, step.name, refused)
            done.added[step.name] = done.added.get(step.name, 0) + len(chunk) - len(refused)
            if refused:
                done.refused[step.name] = done.refused.get(step.name, 0) + len(refused)
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
    "REUSE",
    "Row",
    "Source",
    "UNREADABLE",
    "ambiguous",
    "apply",
    "plan",
    "title",
]
