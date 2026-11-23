"""A set's tracklist as a private playlist on the account, and its archive (R-837).

A set becomes one private playlist; once downloaded, the archive files it in a
root folder for the year it was processed, so the account's root does not fill
with sets. Both steps are planned, then applied, against the account seam.

THE ARCHIVE CHANGES NO TITLE (U242): the ``DOWNLOADED `` prefix is retired
(2026-11-11) and an archived set is held as taken in Cratekit's own record,
which ``crate organize``'s INSPIRATION step reads.

THE SET'S FOLDER IS ``Downloaded Sets <year>`` (U142), never the plain
``<year>`` folder a marked custom playlist is filed in; each is recorded under
its own name, so neither step reuses the other's folder.

ADD ONLY, BECAUSE THE PROTOCOL IS, but for one retitle that follows the library
(U140): a set whose INSPIRATION playlist a person renamed has its account
playlist, ledger key and frozen job name renamed to match, so a backfill makes
no twin.

THE PLAN READS AND WRITES NOTHING, so a second run onto the same set plans
nothing. THE ARCHIVE MOVES FIRST AND THEN READS THE TITLE in the folder, since
the seam reads a title only through a folder's listing (``sync/marks.py``'s
recheck); a playlist found retitled after the move has lost nothing.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.service import RemoteAccount
from cratekit.sync.playlists import is_swept_name, taken_ids

_ORIGIN = ("outbound", "sets")

#: What happens to the set playlist, and to the set's folder.
CREATE = "create"
REUSE = "reuse"
ADOPT = "adopt"

#: The set's root folder is this followed by the year (U142).
FOLDER_PREFIX = "Downloaded Sets "

#: How many tracks one add carries, so each chunk is recorded as it lands.
CHUNK = 100

#: What the archive does once the playlist is in the folder: hold it as taken.
MARK = "mark"
#: Why the archive leaves a title alone, one word each.
ALREADY_MARKED = "already-marked"
RETITLED = "retitled-since-built"
#: The folder's listing did not show the playlist just put in it, so there is
#: no title to recheck.
NOT_LISTED = "not-listed"


def folder_name(year: str) -> str:
    """The root folder a year's downloaded sets are filed in, ``Downloaded Sets 2026``."""
    return FOLDER_PREFIX + year


@dataclass(frozen=True, slots=True)
class SetRow:
    """One tracklist row, decided: the provider track it is, or why there is none."""

    position: int
    artist: str
    title: str
    remote_id: str = ""
    #: How it was matched: ``ref``, ``isrc``, ``library-isrc``, ``accepted`` or ``search``.
    how: str = ""
    #: Why it was not, in words for a person. Empty for a matched row.
    reason: str = ""

    @property
    def matched(self) -> bool:
        return bool(self.remote_id)


@dataclass(frozen=True, slots=True)
class SetPlan:
    """Everything the set's gate is asked over, decided against the account as it is."""

    name: str
    year: str
    action: str
    rows: tuple[SetRow, ...]
    remote_id: str = ""
    #: The matched tracks the playlist does not hold yet, in tracklist order.
    add: tuple[str, ...] = ()
    #: Matched tracks the provider refused before, not asked for again.
    refused: frozenset[str] = frozenset()
    #: Matched tracks on the playlist now.
    on_playlist: frozenset[str] = frozenset()
    #: Matched tracks recorded as written and no longer on the playlist.
    taken_off: frozenset[str] = frozenset()

    @property
    def unmatched(self) -> tuple[SetRow, ...]:
        return tuple(row for row in self.rows if not row.matched)

    @property
    def writes(self) -> bool:
        # A SET WITH NOTHING MATCHED IS NOT MADE: an empty playlist recorded
        # under its name would be reused by every later run as the set.
        return bool(self.add)

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every write, and the name it lands under."""
        return {
            "kind": "export-set",
            "name": self.name,
            "action": self.action,
            "remote_id": self.remote_id,
            "add": list(self.add),
        }


@dataclass
class SetApplied:
    """What an apply wrote, for the report and for a failure part way."""

    remote_id: str = ""
    created: bool = False
    added: list[str] = field(default_factory=list)
    refused: list[str] = field(default_factory=list)


def plan_set(
    cfg: config.Config, name: str, rows: Sequence[SetRow], account: RemoteAccount, *, year: str
) -> SetPlan:
    """Decide the set's playlist against the ledger and the account.

    A track recorded as added and no longer on the playlist was taken off by a
    person and is not put back, nor one the provider refused before; a track
    two rows name is asked for once.
    """
    wanted = tuple(dict.fromkeys(row.remote_id for row in rows if row.matched))
    recorded = ledger.set_playlist(cfg, name)
    if recorded is None:
        return SetPlan(name, year, CREATE, tuple(rows), add=wanted)
    asked = recorded.added | recorded.refused
    # READ EVERY TIME, so a track a person took off is said as taken off.
    held = set(account.playlist_tracks(recorded.remote_id))
    return SetPlan(
        name,
        recorded.year or year,
        REUSE,
        tuple(rows),
        recorded.remote_id,
        add=tuple(one for one in wanted if one not in asked and one not in held),
        refused=frozenset(one for one in wanted if one in recorded.refused and one not in held),
        on_playlist=frozenset(one for one in wanted if one in held),
        taken_off=frozenset(one for one in wanted if one in recorded.added and one not in held),
    )


def apply_set(
    cfg: config.Config, account: RemoteAccount, planned: SetPlan, done: SetApplied
) -> SetApplied:
    """Make the playlist if none is recorded and add the planned tracks, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was
    written; each chunk is recorded as it lands, so a rerun plans the rest.
    """
    remote_id, made = ledger.reserve_set_playlist(
        cfg, planned.name, planned.year, lambda: account.create_playlist(planned.name)
    )
    done.remote_id, done.created = remote_id, made
    for start in range(0, len(planned.add), CHUNK):
        chunk = planned.add[start : start + CHUNK]
        held = set(account.add_tracks(remote_id, chunk))
        added = [one for one in chunk if one in held]
        refused = [one for one in chunk if one not in held]
        ledger.record_set_tracks(cfg, planned.name, added=added, refused=refused)
        done.added.extend(added)
        done.refused.extend(refused)
    return done


@dataclass(frozen=True, slots=True)
class ArchivePlan:
    """The set's folder for its year and the one set playlist the archive files in it."""

    playlist: ledger.SetPlaylist
    year: str
    folder_action: str
    folder_id: str = ""
    #: A recorded folder the account no longer lists, so its record is replaced.
    stale_folder: str = ""
    #: The playlist's title in the folder, ``None`` while it is not in it.
    title: str | None = None
    #: Whether Cratekit's record already holds the playlist as taken (U242).
    taken: bool = False

    @property
    def folder_name(self) -> str:
        return folder_name(self.year)

    @property
    def move(self) -> bool:
        return self.title is None

    @property
    def mark(self) -> bool:
        """Whether the set is to be held as taken. One not yet in the folder is rechecked there."""
        return not self.left

    @property
    def left(self) -> str:
        """Why the set is not marked: taken, by the record or a legacy prefix, or retitled."""
        if self.taken:
            return ALREADY_MARKED
        if self.title is None or self.title == self.playlist.name:
            return ""
        return ALREADY_MARKED if is_swept_name(self.title) else RETITLED

    @property
    def writes(self) -> bool:
        """Whether the account changes; an adoption alone is no write (U142)."""
        return self.move or self.mark

    def identity(self) -> dict[str, Any]:
        return {
            "kind": "export-archive",
            "playlist": self.playlist.remote_id,
            "name": self.playlist.name,
            "taken": self.taken,
            "year": self.year,
            "folder": [self.folder_action, self.folder_id, self.stale_folder],
            "folder_name": self.folder_name,
            "move": self.move,
            "mark": self.mark,
        }


@dataclass
class ArchiveApplied:
    """What an archive wrote."""

    folder_id: str = ""
    folder_created: bool = False
    moved: bool = False
    marked: bool = False
    #: Why the title was left after all, when the recheck in the folder found
    #: it already marked or retitled.
    left: str = ""


def _ambiguous_folder(name: str, found: Sequence[str]) -> CratekitError:
    return refuse(
        "export-set-ambiguous",
        f"the account holds {len(found)} root folders named {name!r}, so which one "
        f"holds the year's sets is not something its name decides, and nothing was written",
        steps=(
            "rename or merge the extra folders on the account so one carries the "
            "name, then archive again",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"folders": list(found), "name": name},
    )


def plan_archive(
    cfg: config.Config, playlist: ledger.SetPlaylist, account: RemoteAccount, *, year: str
) -> ArchivePlan:
    """Decide the set's folder for ``year`` and the playlist's place and title in it.

    The folder is found by its name (U142): the ledger's record reused while
    the account lists it, one root folder of the name adopted, two refused,
    none created on apply.
    """
    name = folder_name(year)
    recorded = ledger.set_folder(cfg, name)
    root = account.folders()
    stale = ""
    if recorded and recorded in root:
        action, folder_id = REUSE, recorded
    else:
        stale = recorded
        named = sorted(fid for fid, title in root.items() if title == name)
        if len(named) > 1:
            raise _ambiguous_folder(name, named)
        action, folder_id = (ADOPT, named[0]) if named else (CREATE, "")
    title = account.folder_playlists(folder_id).get(playlist.remote_id) if folder_id else None
    return ArchivePlan(
        playlist, year, action, folder_id, stale, title, taken=playlist.remote_id in taken_ids(cfg)
    )


def apply_archive(
    cfg: config.Config,
    account: RemoteAccount,
    planned: ArchivePlan,
    done: ArchiveApplied,
    *,
    record: Callable[[str], None],
) -> ArchiveApplied:
    """Make or reuse the folder, put the playlist in it, then mark it if still due.

    ``record`` holds the set as taken by the title it carries in the folder,
    raising if it cannot. No title changes (U242).
    """
    playlist = planned.playlist
    folder_id, made = ledger.reserve_set_folder(
        cfg,
        planned.folder_name,
        lambda: account.create_folder(planned.folder_name),
        adopt=planned.folder_id if planned.folder_action == ADOPT else "",
        stale=planned.stale_folder,
    )
    done.folder_id, done.folder_created = folder_id, made
    if planned.move:
        account.move_to_folder(playlist.remote_id, folder_id)
        done.moved = True
    if not planned.mark:
        done.left = planned.left
        return done
    # THE RECHECK, ON THE FOLDER IT NOW SITS IN: a title other than the one it
    # was built under is somebody's, and a prefixed one is already taken.
    now = account.folder_playlists(folder_id).get(playlist.remote_id)
    if now is None:
        # NOT A RETITLE: a listing without it says nothing about its title.
        done.left = NOT_LISTED
        return done
    if now != playlist.name:
        done.left = ALREADY_MARKED if is_swept_name(now) else RETITLED
        return done
    record(playlist.name)
    done.marked = True
    return done


@dataclass(frozen=True, slots=True)
class RenamePlan:
    """A set's account playlist renamed to the name its INSPIRATION playlist carries (U140).

    Three writes, each skipped when it already holds: the account title, the
    ledger's key, the name frozen on the job. ``playlist.name`` is the key it
    is recorded under now, ``to`` once an earlier run moved it.
    """

    job_id: str
    playlist: ledger.SetPlaylist
    #: The INSPIRATION playlist's name as the account and the ledger spell it.
    to: str
    #: The name frozen on the job, ``""`` for a job queued before the freeze.
    frozen: str
    #: The INSPIRATION playlist's name as the library carries it, which the job
    #: freezes; ``to`` is its account spelling (a slash becomes a dash).
    live: str = ""
    #: The INSPIRATION playlist's row, whose name ``to`` is.
    inspiration_id: str = ""
    #: A second playlist recorded for the set under another of its names: a
    #: twin a rename would leave on the account with nothing recording it.
    twin: ledger.SetPlaylist | None = None

    @property
    def rename(self) -> bool:
        """Whether the account title and the ledger key are still to move."""
        return self.playlist.name != self.to

    @property
    def refreeze(self) -> bool:
        return self.frozen != (self.live or self.to)

    @property
    def writes(self) -> bool:
        return self.rename or self.refreeze

    def identity(self) -> dict[str, Any]:
        return {
            "kind": "export-set-rename",
            "job": self.job_id,
            "playlist": self.playlist.remote_id,
            "name": self.playlist.name,
            "to": self.to,
            "frozen": self.frozen,
            "live": self.live,
            "inspiration": self.inspiration_id,
        }


@dataclass
class RenameApplied:
    """What a rename wrote, for the report and for a failure part way."""

    renamed: bool = False
    rekeyed: bool = False
    refrozen: bool = False


def plan_rename(
    cfg: config.Config,
    *,
    job_id: str,
    names: Sequence[str],
    to: str,
    frozen: str,
    live: str = "",
    inspiration_id: str = "",
) -> RenamePlan | None:
    """The rename, or ``None`` when no account playlist is recorded for the set.

    ``names`` are the names the playlist may be recorded under, in the order a
    person expects (frozen, the landings' R-1017, the posted day's, the queued
    day's). A record under ``to`` is an earlier run's rename, TAKEN ONLY ALONE:
    beside another playlist under ``names``, or two playlists under two of
    them, it is a twin, named in ``twin`` rather than chosen. Reads the ledger
    only.
    """
    recorded_to = ledger.set_playlist(cfg, to) if to else None
    # EVERY NAME IS READ (R-1017), since two playlists under two older names
    # are a twin as surely as one under ``to``.
    older: list[ledger.SetPlaylist] = []
    for name in names:
        if not name or name == to:
            continue
        found = ledger.set_playlist(cfg, name)
        if found is not None and all(found.remote_id != one.remote_id for one in older):
            older.append(found)
    held = recorded_to or (older[0] if older else None)
    if held is None:
        return None
    twin = next((one for one in older if one.remote_id != held.remote_id), None)
    return RenamePlan(job_id, held, to, frozen, live, inspiration_id, twin)


def apply_rename(
    cfg: config.Config,
    account: RemoteAccount,
    planned: RenamePlan,
    done: RenameApplied,
    *,
    refreeze: Callable[[str], None],
) -> RenameApplied:
    """Retitle on the account, then move the ledger key, then refreeze the job, into ``done``.

    The account first, the write a person sees, and a rename by identifier
    asked twice asks for one title; the job last, since its old name is how a
    rerun finds the record. ``refreeze`` takes the library's own name and
    raises if the job cannot take it.
    """
    playlist = planned.playlist
    if planned.rename:
        account.rename_playlist(playlist.remote_id, planned.to)
        done.renamed = True
        done.rekeyed = ledger.rename_set_playlist(
            cfg, playlist.name, planned.to, playlist.remote_id
        )
    if planned.refreeze:
        refreeze(planned.live or planned.to)
        done.refrozen = True
    return done


__all__ = [
    "ADOPT", "ALREADY_MARKED", "ArchiveApplied", "ArchivePlan", "CHUNK", "CREATE",
    "FOLDER_PREFIX", "MARK", "NOT_LISTED", "RETITLED", "REUSE", "RenameApplied", "RenamePlan",
    "SetApplied", "SetPlan", "SetRow", "apply_archive", "apply_rename", "apply_set",
    "folder_name", "plan_archive", "plan_rename", "plan_set",
]
