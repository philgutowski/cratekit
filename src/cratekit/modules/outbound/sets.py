"""A set's tracklist as a private playlist on the account, and its archive (R-837).

The source system keeps a set on the account one way: the identified set, or a
tracklist somebody typed, becomes one private playlist, and once the set has
been downloaded that playlist is prefixed ``DOWNLOADED `` and filed in a root
folder named for the year the set was processed, so the account's root does
not fill with sets. This module is both steps, each planned and then applied,
against the account seam.

ADD ONLY, BECAUSE THE PROTOCOL IS. A playlist is created, tracks are added, a
folder is created and a playlist is put in one. One retitle is the archive
mark, recorded in ``sync mark``'s record so ``sync unmark`` can take it off.
The other follows the library (U140): a set whose INSPIRATION playlist a
person renamed has its account playlist renamed to match, and the ledger's key
and the job's frozen name move with it, so a backfill finds it and makes no
twin.

THE PLAN READS AND WRITES NOTHING. Each tracklist row arrives already decided,
matched to one provider track or left out with its reason, and the plan
compares the matched tracks with the playlist recorded for the set's name and
what that playlist now holds. A second run onto the same set plans nothing.

THE ARCHIVE PUTS THE PLAYLIST IN ITS FOLDER FIRST AND THEN READS ITS TITLE
THERE. The account seam reads a title only through a folder's listing, so the
recheck before the rename, ``sync/marks.py``'s rule, is made on the listing of
the folder the playlist was just put in. A move changes where a playlist sits
and nothing it holds, so a playlist moved and then found retitled by a person
has lost nothing, and is left with its title.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.folders import MARK_PREFIX
from cratekit.modules.outbound.service import RemoteAccount

_ORIGIN = ("outbound", "sets")

#: What happens to the set playlist, and to the year folder.
CREATE = "create"
REUSE = "reuse"
ADOPT = "adopt"

#: How many tracks one add carries, so each chunk is recorded as it lands.
CHUNK = 100

#: What the archive does to the playlist's title once it is in the folder.
MARK = "mark"
#: Why the archive leaves a title alone, one word each.
ALREADY_MARKED = "already-marked"
RETITLED = "retitled-since-built"
#: The folder's listing did not show the playlist just put in it, so there is
#: no title to recheck, and a rename without one is not made.
NOT_LISTED = "not-listed"


@dataclass(frozen=True, slots=True)
class SetRow:
    """One tracklist row, decided: the provider track it is, or why there is none."""

    position: int
    artist: str
    title: str
    remote_id: str = ""
    #: How the row was matched, ``ref``, ``isrc``, ``library-isrc``, ``accepted``
    #: or ``search``.
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
        # A SET WITH NOTHING MATCHED IS NOT MADE. An empty private playlist
        # under the set's name is not the set, and recorded it would be reused
        # by every later run as though it were.
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
    cfg: config.Config,
    name: str,
    rows: Sequence[SetRow],
    account: RemoteAccount,
    *,
    year: str,
) -> SetPlan:
    """Decide the set's playlist against the ledger and the account.

    A TRACK RECORDED AS ADDED AND NO LONGER ON THE PLAYLIST was taken off by a
    person and is not put back, on ``folders.plan``'s rule, and neither is one
    the provider refused before. A track named by two rows of the set is asked
    for once.
    """
    wanted = tuple(dict.fromkeys(row.remote_id for row in rows if row.matched))
    recorded = ledger.set_playlist(cfg, name)
    if recorded is None:
        return SetPlan(name=name, year=year, action=CREATE, rows=tuple(rows), add=wanted)
    asked = recorded.added | recorded.refused
    # THE PLAYLIST IS READ EVERY TIME, one paged read, so a track a person took
    # off is said as taken off rather than shown as on the playlist from what
    # the record says was written.
    held = set(account.playlist_tracks(recorded.remote_id))
    return SetPlan(
        name=name,
        year=recorded.year or year,
        action=REUSE,
        rows=tuple(rows),
        remote_id=recorded.remote_id,
        add=tuple(one for one in wanted if one not in asked and one not in held),
        refused=frozenset(one for one in wanted if one in recorded.refused and one not in held),
        on_playlist=frozenset(one for one in wanted if one in held),
        taken_off=frozenset(
            one for one in wanted if one in recorded.added and one not in held
        ),
    )


def apply_set(
    cfg: config.Config, account: RemoteAccount, planned: SetPlan, done: SetApplied
) -> SetApplied:
    """Make the playlist if none is recorded and add the planned tracks, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was written
    before the raise, for the refusal to name. Each chunk is recorded as it
    lands, so a run started again plans only what is left.
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


# ── the archive ─────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ArchivePlan:
    """The year folder and the one set playlist the archive files in it."""

    playlist: ledger.SetPlaylist
    year: str
    folder_action: str
    folder_id: str = ""
    #: A recorded folder the account no longer lists, so its record is replaced.
    stale_folder: str = ""
    #: The playlist's title in the folder, when it is in the folder already.
    #: ``None`` while it is not, since the seam reads a title only there.
    title: str | None = None

    @property
    def to(self) -> str:
        return MARK_PREFIX + self.playlist.name

    @property
    def move(self) -> bool:
        return self.title is None

    @property
    def mark(self) -> bool:
        """Whether a rename is planned. One not yet in the folder is rechecked there."""
        return self.title is None or self.title == self.playlist.name

    @property
    def left(self) -> str:
        """Why the title is left alone, or ``""`` when it is not."""
        if self.title is None or self.title == self.playlist.name:
            return ""
        return ALREADY_MARKED if self.title.startswith(MARK_PREFIX) else RETITLED

    @property
    def writes(self) -> bool:
        return self.folder_action in (CREATE, ADOPT) or self.move or self.mark

    def identity(self) -> dict[str, Any]:
        return {
            "kind": "export-archive",
            "playlist": self.playlist.remote_id,
            "name": self.playlist.name,
            "to": self.to,
            "year": self.year,
            "folder": [self.folder_action, self.folder_id, self.stale_folder],
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
    #: Why the title was left after all, set when the recheck in the folder
    #: found it already marked or retitled.
    left: str = ""


def _ambiguous_folder(year: str, found: Sequence[str]) -> CratekitError:
    return refuse(
        "export-set-ambiguous",
        f"the account holds {len(found)} root folders named {year!r}, so which one "
        f"is the year's is not something its name decides, and nothing was written",
        steps=(
            "rename or merge the extra folders on the account so one carries the "
            "year, then archive again",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"folders": list(found), "name": year},
    )


def plan_archive(
    cfg: config.Config, playlist: ledger.SetPlaylist, account: RemoteAccount, *, year: str
) -> ArchivePlan:
    """Decide the year folder and the playlist's place and title in it."""
    recorded = ledger.set_folder(cfg, year)
    root = account.folders()
    stale = ""
    if recorded and recorded in root:
        action, folder_id = REUSE, recorded
    else:
        stale = recorded
        named = sorted(fid for fid, title in root.items() if title == year)
        if len(named) > 1:
            raise _ambiguous_folder(year, named)
        action, folder_id = (ADOPT, named[0]) if named else (CREATE, "")
    title = account.folder_playlists(folder_id).get(playlist.remote_id) if folder_id else None
    return ArchivePlan(
        playlist=playlist,
        year=year,
        folder_action=action,
        folder_id=folder_id,
        stale_folder=stale,
        title=title,
    )


def apply_archive(
    cfg: config.Config,
    account: RemoteAccount,
    planned: ArchivePlan,
    done: ArchiveApplied,
    *,
    record: Callable[[str, str], None],
) -> ArchiveApplied:
    """Make or reuse the folder, put the playlist in it, then mark it if still due.

    ``record`` is handed the title before and the title written, once the
    rename has landed, and raises if it cannot keep it.
    """
    playlist = planned.playlist
    folder_id, made = ledger.reserve_set_folder(
        cfg,
        planned.year,
        lambda: account.create_folder(planned.year),
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
    # THE RECHECK, ON THE FOLDER IT NOW SITS IN. A title that is no longer the
    # one it was built under is somebody's, and a prefixed one is already done.
    now = account.folder_playlists(folder_id).get(playlist.remote_id)
    if now is None:
        # NOT A RETITLE. A listing that does not show the playlist yet says
        # nothing about its title, so nothing is renamed and nobody is blamed.
        done.left = NOT_LISTED
        return done
    if now != playlist.name:
        done.left = ALREADY_MARKED if now.startswith(MARK_PREFIX) else RETITLED
        return done
    account.rename_playlist(playlist.remote_id, planned.to)
    done.marked = True
    record(playlist.name, planned.to)
    return done


# ── the rename that follows the library (U140) ──────────────────────────────


@dataclass(frozen=True, slots=True)
class RenamePlan:
    """A set's account playlist renamed to the name its INSPIRATION playlist carries.

    Three writes, each one skipped when it already holds: the title on the
    account, the ledger's key, and the name frozen on the set's job. ``name``
    is the key the playlist is recorded under now, which is ``to`` once an
    earlier run moved it, so a run that stopped part way plans only the rest.
    """

    job_id: str
    playlist: ledger.SetPlaylist
    to: str
    #: The name frozen on the job, ``""`` for a job queued before the freeze.
    frozen: str
    #: The INSPIRATION playlist's row, whose name ``to`` is.
    inspiration_id: str = ""

    @property
    def rename(self) -> bool:
        """Whether the account title and the ledger key are still to move."""
        return self.playlist.name != self.to

    @property
    def refreeze(self) -> bool:
        return self.frozen != self.to

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
    inspiration_id: str = "",
) -> RenamePlan | None:
    """The rename, or ``None`` when no account playlist is recorded for the set.

    ``names`` are the names the set's account playlist may be recorded under,
    in the order a person would expect: frozen on the job, then the posted
    day's form, then the queued day's. A record already under ``to`` wins over
    all of them, since that is a rename an earlier run made. Reads the ledger
    only; the title on the account is set by identifier, so no read of it
    stands between the plan and the write.
    """
    for name in (to, *names):
        if not name:
            continue
        recorded = ledger.set_playlist(cfg, name)
        if recorded is not None:
            return RenamePlan(
                job_id=job_id,
                playlist=recorded,
                to=to,
                frozen=frozen,
                inspiration_id=inspiration_id,
            )
    return None


def apply_rename(
    cfg: config.Config,
    account: RemoteAccount,
    planned: RenamePlan,
    done: RenameApplied,
    *,
    refreeze: Callable[[str], None],
) -> RenameApplied:
    """Retitle on the account, then move the ledger key, then refreeze the job, into ``done``.

    THE ACCOUNT FIRST, because it is the one write a person sees. A rename by
    identifier asked twice asks for one title, so a run that failed after it
    renames again and moves on. The key moves once the title is there, and
    the job last, since its old name is how a rerun finds the record if the
    move never landed. ``refreeze`` is handed the new name and raises if the
    job cannot take it.
    """
    playlist = planned.playlist
    if planned.rename:
        account.rename_playlist(playlist.remote_id, planned.to)
        done.renamed = True
        done.rekeyed = ledger.rename_set_playlist(
            cfg, playlist.name, planned.to, playlist.remote_id
        )
    if planned.refreeze:
        refreeze(planned.to)
        done.refrozen = True
    return done


__all__ = [
    "ADOPT",
    "ALREADY_MARKED",
    "ArchiveApplied",
    "ArchivePlan",
    "CHUNK",
    "CREATE",
    "MARK",
    "NOT_LISTED",
    "RETITLED",
    "REUSE",
    "RenameApplied",
    "RenamePlan",
    "SetApplied",
    "SetPlan",
    "SetRow",
    "apply_archive",
    "apply_rename",
    "apply_set",
    "plan_archive",
    "plan_rename",
    "plan_set",
]
