"""Marked custom playlists filed into their year folders on the account (U116).

THE HAND CONVENTION, MADE A STEP. The author moved each custom playlist into
the account folder for its year once he had downloaded it, and nothing did that
for him: ``sync mark`` prefixes a finished playlist and moves nothing, so a
marked playlist stayed at the account root. This step lists every playlist at
the root and names what becomes of each one:

* A PLAYLIST A SYNC MARKED, by ``sync mark``'s record and a mark still standing,
  is moved into the root folder named for the year of its mark;
* a label playlist is the label step's, and a set playlist is the archive's;
* the product's own working playlists stay where they are;
* anything else is reported and left, since nothing says it was downloaded.

THE YEAR FOLDER IS THE ONE THE SET ARCHIVE FILES INTO, read and reserved
through the same ledger entry, so a year holds one folder whichever step made
it. A folder recorded and still listed is reused, one root folder named as the
year is adopted, and none is created once, on apply, for every playlist of that
year. Two or more root folders named as the year leave that year's playlists
where they are, reported, since a playlist the plan cannot place is never moved.

ADD ONLY, BECAUSE THE PROTOCOL IS. A folder is created and a playlist is put in
one; nothing is renamed, nothing is removed. A move is undone by a move back,
and each move this step makes is named on the applied totals the run records,
playlist and folder, so the run says exactly what to put back.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger, sets
from cratekit.modules.outbound.service import RemoteAccount
from cratekit.organize import own
from cratekit.sync.playlists import is_swept_name

_ORIGIN = ("organize.filing",)

#: What becomes of one playlist at the root.
MOVE = "move"
LEFT = "left"

#: Why a playlist at the root is left there, one sentence each.
LABEL_STEP = "a label playlist, which the label step files"
SET_STEP = "a set playlist, which the set archive files"
WORKING = "one of the product's own working playlists, kept at the root"
PRODUCT_MADE = "made by the product and not a custom playlist"
UNMARKED = "not marked by a sync, so nothing says it was downloaded"
PREFIXED_UNMARKED = (
    "its name says downloaded but no sync recorded when, so no year can be chosen"
)
UNDATED = "its mark carries no year, so no year folder is its own"


def _ambiguous(year: str, count: int) -> str:
    return (
        f"the account holds {count} root folders named {year!r}, so which one is "
        f"the year's is not something its name decides"
    )


@dataclass(frozen=True, slots=True)
class YearFolder:
    """One year's folder as the plan found it."""

    year: str
    action: str
    folder_id: str = ""
    #: A recorded folder the account no longer lists, so its record is replaced.
    stale: str = ""
    #: Set when the year cannot be placed, and then nothing of the year moves.
    why: str = ""


@dataclass(frozen=True, slots=True)
class Placement:
    """One playlist at the account root, and what the plan does with it."""

    playlist_id: str
    name: str
    action: str
    year: str = ""
    why: str = ""

    def item(self, folder: YearFolder | None) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "id": self.playlist_id,
            "kind": "playlist",
            "name": self.name,
            "action": self.action,
        }
        if self.year:
            shown["year"] = self.year
        if folder is not None and self.action == MOVE:
            shown["folder"] = folder.action
            shown["folder_id"] = folder.folder_id
        if self.why:
            shown["why"] = self.why
        return shown


@dataclass(frozen=True, slots=True)
class FilePlan:
    """Every playlist at the root, each placed or left with its reason."""

    rows: tuple[Placement, ...]
    years: Mapping[str, YearFolder]

    @property
    def moves(self) -> tuple[Placement, ...]:
        return tuple(row for row in self.rows if row.action == MOVE)

    @property
    def writes(self) -> bool:
        return bool(self.moves)

    def creates(self) -> tuple[str, ...]:
        """The years whose folder a move needs and the account does not hold."""
        wanted = {row.year for row in self.moves}
        return tuple(
            sorted(year for year in wanted if self.years[year].action == sets.CREATE)
        )

    def identity(self) -> dict[str, Any]:
        """What the digest covers: every row at the root, and every year's folder."""
        return {
            "kind": "filing",
            "rows": [[row.playlist_id, row.action, row.year, row.why] for row in self.rows],
            "years": [
                [one.year, one.action, one.folder_id, one.stale, one.why]
                for one in (self.years[year] for year in sorted(self.years))
            ],
        }

    def items(self) -> list[dict[str, Any]]:
        return [row.item(self.years.get(row.year)) for row in self.rows]


@dataclass
class Filed:
    """What an apply wrote, in the order it wrote it."""

    #: Each year's folder in hand, and whether this apply created it.
    folders: dict[str, str] = field(default_factory=dict)
    created: list[str] = field(default_factory=list)
    #: Each move made, ``[playlist, folder]``, which is what a move back reads.
    moved: list[list[str]] = field(default_factory=list)

    def totals(self) -> dict[str, Any]:
        return {
            "folders": dict(self.folders),
            "folders_created": list(self.created),
            "moved": [list(one) for one in self.moved],
        }


def year_of_mark(marked: str) -> str:
    """The year a mark landed in local time, or ``""``.

    The stamp is stored in UTC. A mark at 20:00 Eastern on 31 December is the
    next day's UTC year, and filing by the UTC digits would put it in the wrong
    year folder. Local time is the year the person meant.
    """
    text = str(marked or "").strip()
    if not text:
        return ""
    try:
        when = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if when.tzinfo is not None:
        when = when.astimezone()
    return f"{when.year:04d}"


def _year_folder(cfg: config.Config, year: str, root: Mapping[str, str]) -> YearFolder:
    """The set archive's own decision of one year's folder, never refused here."""
    recorded = ledger.set_folder(cfg, year)
    if recorded and recorded in root:
        return YearFolder(year=year, action=sets.REUSE, folder_id=recorded)
    named = sorted(folder_id for folder_id, title in root.items() if title == year)
    if len(named) > 1:
        return YearFolder(year=year, action=LEFT, stale=recorded, why=_ambiguous(year, len(named)))
    if named:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
    return YearFolder(year=year, action=sets.CREATE, stale=recorded)


def _standing_marks(marks: Iterable[Any]) -> dict[str, str]:
    """Each playlist with a mark still standing, to the instant of its latest one."""
    standing: dict[str, str] = {}
    for entry in marks:
        if entry.unmarked:
            continue
        held = standing.get(entry.playlist_id)
        if held is None or str(entry.marked) > held:
            standing[entry.playlist_id] = str(entry.marked)
    return standing



def playlists_in_folders(remote: RemoteAccount) -> set[str]:
    """Every playlist any folder on the account holds, nested folders included.

    Root folders alone are not enough: a playlist two folders down (for example
    under Archive then 2025) is never listed by ``folder_playlists`` of a root
    folder, and treating it as at the root would move it out. Walk every folder
    the account reports, and every folder those hold.
    """
    held: set[str] = set()
    pending = list(remote.folders())
    seen: set[str] = set()
    while pending:
        folder_id = pending.pop()
        if folder_id in seen:
            continue
        seen.add(folder_id)
        held.update(remote.folder_playlists(folder_id))
        pending.extend(remote.folder_folders(folder_id))
    return held


def plan(
    cfg: config.Config,
    *,
    listed: Sequence[Any],
    remote: RemoteAccount,
    labels: Iterable[str],
    marks: Iterable[Any],
    working: Any,
) -> FilePlan:
    """Decide every playlist at the account root. Reads, and writes nothing.

    ``listed`` is every playlist the account created, ``marks`` is ``sync
    mark``'s record, and ``working`` answers whether a name is one of the
    product's own working playlists. A playlist in any folder is not at the
    root and is not this step's.
    """
    labels = tuple(labels)
    root = remote.folders()
    in_folders = playlists_in_folders(remote)
    label_built = ledger.label_playlist_ids(cfg)
    set_built = ledger.set_playlist_ids(cfg)
    at_root = [one for one in listed if one.playlist_id not in in_folders]
    made = ledger.product_made_among(cfg, (one.playlist_id for one in at_root))
    standing = _standing_marks(marks)
    years: dict[str, YearFolder] = {}
    rows: list[Placement] = []
    for one in sorted(at_root, key=lambda playlist: (playlist.name, playlist.playlist_id)):
        identity, name = str(one.playlist_id), str(one.name)
        if identity in label_built or own.label_of(name, labels) is not None:
            rows.append(Placement(identity, name, LEFT, why=LABEL_STEP))
            continue
        if identity in set_built:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
            continue
        if working(name):
            rows.append(Placement(identity, name, LEFT, why=WORKING))
            continue
        if identity not in standing:
            if identity in made:
                why = PRODUCT_MADE
            elif is_swept_name(name):
                why = PREFIXED_UNMARKED
            else:
                why = UNMARKED
            rows.append(Placement(identity, name, LEFT, why=why))
            continue
        year = year_of_mark(standing[identity])
        if not year:
            rows.append(Placement(identity, name, LEFT, why=UNDATED))
            continue
        if year not in years:
            years[year] = _year_folder(cfg, year, root)
        folder = years[year]
        if folder.why:
            rows.append(Placement(identity, name, LEFT, year=year, why=folder.why))
            continue
        rows.append(Placement(identity, name, MOVE, year=year))
    return FilePlan(rows=tuple(rows), years=years)


def _failed_part_way(exc: Exception, done: Filed) -> Exception:
    """The failure, with every folder made and every move made named in it."""
    if done.moved or done.created:
        wrote = (
            f"before this failed {len(done.created)} year folder(s) were created and "
            f"{len(done.moved)} playlist(s) were moved: "
            + ", ".join(f"{playlist} into {folder}" for playlist, folder in done.moved)
        ).rstrip(": ")
    else:
        wrote = "nothing was moved before this failed"
    detail = done.totals()
    again = "run crate organize again; a year folder made is reused, never made twice"
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
    # ANY OTHER FAILURE IS THIS BUILD'S OWN. ``organize`` names it a defect of
    # the step, and the message it reads carries what moved.
    return RuntimeError(f"{wrote}. {type(exc).__name__}: {exc}")


def apply(cfg: config.Config, remote: RemoteAccount, planned: FilePlan) -> Filed:
    """Make or reuse each year's folder, then move each planned playlist into it.

    STOPS AT THE FIRST REFUSAL and raises it with what moved named, so a
    provider that refuses part way leaves a run that says what to put back.
    """
    done = Filed()
    try:
        for row in planned.moves:
            folder = planned.years[row.year]
            if row.year not in done.folders:

                def create(year: str = row.year) -> str:
                    folder_id = remote.create_folder(year)
                    # Record as soon as the provider answers, before the ledger
                    # write: a write that raises must still name the folder made.
                    done.folders[year] = folder_id
                    done.created.append(year)
                    return folder_id

                folder_id, _made = ledger.reserve_set_folder(
                    cfg,
                    row.year,
                    create,
                    adopt=folder.folder_id if folder.action == sets.ADOPT else "",
                    stale=folder.stale,
                )
                done.folders[row.year] = folder_id
            remote.move_to_folder(row.playlist_id, done.folders[row.year])
            done.moved.append([row.playlist_id, done.folders[row.year]])
    except Exception as exc:
        raise _failed_part_way(exc, done) from exc
    return done


__all__ = [
    "LABEL_STEP",
    "LEFT",
    "MOVE",
    "PREFIXED_UNMARKED",
    "PRODUCT_MADE",
    "SET_STEP",
    "UNDATED",
    "UNMARKED",
    "WORKING",
    "FilePlan",
    "Filed",
    "Placement",
    "YearFolder",
    "apply",
    "plan",
    "playlists_in_folders",
    "year_of_mark",
]
