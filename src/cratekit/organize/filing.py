"""Marked custom playlists filed into their year folders on the account (U116).

This step lists every playlist at the account root and names what becomes of
each one:

* A PLAYLIST A SYNC MARKED, by ``sync mark``'s record and a mark still standing,
  is moved into the root folder named for the year of its mark;
* a label playlist is the label step's, and a set playlist is the archive's;
* the product's own working playlists stay where they are;
* A PLAYLIST AN EXPORT MADE, by the ledger's record, is moved into the root
  ``Exports`` folder (U131);
* THE SOURCE SYSTEM'S LABEL DEBRIS, and an unclaimed playlist holding no
  track, are left for the root step (U143), :mod:`cratekit.organize.root`;
* A WORKING CUSTOM PLAYLIST, one no ledger claims and no sync marked, is left
  at the root whatever its age (U143), by Phillip's rule of 2026-10-13;
* ONE NO LEDGER CLAIMS THAT A SYNC CANNOT FILE BY A YEAR, its name prefixed
  with no mark recorded or its mark carrying no year, is moved into the root
  ``Mine`` folder (U131);
* what is left is reported and left with its reason.

A PLAYLIST IN A ``Mine`` THIS PRODUCT MADE IS STILL READ FOR ITS MARK (U131),
so a later sync's mark moves it on into its year folder. A playlist is never
moved out of a folder a person made.

THE YEAR FOLDER IS THE PLAIN ``<year>``, NEVER THE SETS' ``Downloaded Sets
<year>`` (U142), decided on the archive's rule: a recorded folder still listed
is reused, one root folder named as the year is adopted, none is created once.
Two or more root folders named as the year leave that year's playlists where
they are, since a playlist the plan cannot place is never moved.

ADD ONLY. Nothing is renamed or removed here; the root's removals are the root
step's. Each move is named on the applied totals, so the run says what to put
back.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.organize import own
from cratekit.sync.playlists import is_library_debris, is_taken

if TYPE_CHECKING:
    from cratekit.modules.outbound import kinds
    from cratekit.modules.outbound.service import RemoteAccount

_ORIGIN = ("organize.filing",)

#: What becomes of one playlist at the root.
MOVE = "move"
LEFT = "left"

#: Why a playlist at the root is left there, one sentence each.
LABEL_STEP = "a label playlist, which the label step files"
SET_STEP = "a set playlist, which the set archive files"
WORKING = "one of the product's own working playlists, kept at the root"
PRODUCT_MADE = "made by the product and not a custom playlist"
#: The three a root playlist is left for, the last kept at the root (U143).
DEBRIS = (
    "the source system's label debris, which the root step removes once its "
    "tracks are in its label's folder"
)
EMPTY = "it holds no track, so the root step removes it"
WORKING_CUSTOM = (
    "a working custom playlist, kept at the root until a sync marks it "
    "downloaded and it is filed by its year"
)
PREFIXED_UNMARKED = (
    "it is taken, by its old DOWNLOADED prefix or Cratekit's record of it, but no "
    "sync recorded when, so no year can be chosen"
)
UNDATED = "its mark carries no year, so no year folder is its own"
#: Why a playlist goes to its kind's folder rather than a year's (U131).
EXPORTED = "made by export playlist, so it is filed with the exports"


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


def folder_rows(folders: Mapping[str, Any]) -> list[list[str]]:
    """Each year's or kind's folder as a digest covers it, in name order."""
    return [
        [name, one.action, one.folder_id, one.stale, one.why]
        for name, one in sorted(folders.items())
    ]


@dataclass(frozen=True, slots=True)
class Placement:
    """One playlist at the account root, and what the plan does with it."""

    playlist_id: str
    name: str
    action: str
    year: str = ""
    why: str = ""
    #: The kind folder a move goes to, ``Mine`` or ``Exports``, when not a year.
    kind: str = ""

    def item(self, folder: YearFolder | kinds.KindFolder | None) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "id": self.playlist_id, "kind": "playlist", "name": self.name, "action": self.action
        }
        if self.year:
            shown["year"] = self.year
        if self.kind:
            shown["kind_folder"] = self.kind
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
    #: Each kind folder a row names, ``Mine`` and ``Exports`` (U131).
    kinds: Mapping[str, kinds.KindFolder] = field(default_factory=dict)
    #: The root's folders as this plan read them, identifier to name, which the
    #: root step (U143) reads rather than listing the root a second time.
    root: Mapping[str, str] = field(default_factory=dict)

    @property
    def moves(self) -> tuple[Placement, ...]:
        return tuple(row for row in self.rows if row.action == MOVE)

    @property
    def writes(self) -> bool:
        return bool(self.moves)

    def creates(self) -> tuple[str, ...]:
        """The years, then the kinds, whose folder a move needs and the account lacks."""
        from cratekit.modules.outbound import kinds, sets

        years = {row.year for row in self.moves if row.year}
        wanted = {row.kind for row in self.moves if row.kind}
        return (
            *sorted(year for year in years if self.years[year].action == sets.CREATE),
            *sorted(kind for kind in wanted if self.kinds[kind].action == kinds.CREATE),
        )

    def identity(self) -> dict[str, Any]:
        """What the digest covers: every row at the root, and every year's folder."""
        return {
            "kind": "filing",
            "rows": [
                [row.playlist_id, row.action, row.year, row.why, row.kind] for row in self.rows
            ],
            "years": folder_rows(self.years),
            "kinds": folder_rows(self.kinds),
        }

    def items(self) -> list[dict[str, Any]]:
        return [
            row.item(self.kinds.get(row.kind) if row.kind else self.years.get(row.year))
            for row in self.rows
        ]


@dataclass
class Filed:
    """What an apply wrote, in the order it wrote it."""

    #: Each year's folder in hand, and whether this apply created it.
    folders: dict[str, str] = field(default_factory=dict)
    created: list[str] = field(default_factory=list)
    #: Each kind's folder in hand, and the kinds whose folder this apply made.
    kinds: dict[str, str] = field(default_factory=dict)
    kinds_created: list[str] = field(default_factory=list)
    #: Each move made, ``[playlist, folder]``, which is what a move back reads.
    moved: list[list[str]] = field(default_factory=list)

    def totals(self) -> dict[str, Any]:
        return {
            "folders": dict(self.folders), "folders_created": list(self.created),
            "kind_folders": dict(self.kinds), "kind_folders_created": list(self.kinds_created),
            "moved": [list(one) for one in self.moved],
        }


def year_of_mark(marked: str) -> str:
    """The year a mark landed in local time, or ``""``.

    The stamp is stored in UTC, and a mark late on 31 December west of UTC is
    the next UTC year; local time is the year the person meant.
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


def year_folder(cfg: config.Config, year: str, root: Mapping[str, str]) -> YearFolder:
    """One year's folder on the set archive's rule, never refused here.

    The root step's legacy moves (U143) use this same rule, so the two steps
    file into one folder and never make two.
    """
    from cratekit.modules.outbound import kinds, ledger, sets

    recorded = ledger.set_folder(cfg, year)
    # A RECORD WHOSE FOLDER NOW CARRIES THE SETS' NAME IS NOT THE YEAR'S (U142),
    # since it would file custom playlists among the sets, NOR IS ONE NOW NAMED
    # AS A LEGACY YEAR FOLDER (U143), which would be emptied into itself.
    if (
        recorded
        and recorded in root
        and root[recorded] != sets.folder_name(year)
        and not kinds.legacy_year(root[recorded])
    ):
        return YearFolder(year=year, action=sets.REUSE, folder_id=recorded)
    named = sorted(folder_id for folder_id, title in root.items() if title == year)
    if len(named) > 1:
        why = (
            f"the account holds {len(named)} root folders named {year!r}, so which one is "
            f"the year's is not something its name decides"
        )
        return YearFolder(year=year, action=LEFT, stale=recorded, why=why)
    if named:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
    return YearFolder(year=year, action=sets.CREATE, stale=recorded)


def _standing_marks(marks: Iterable[Any], taken: Iterable[Any] = ()) -> dict[str, str]:
    """Each playlist with a mark still standing, to the instant of its latest one.

    ``taken`` is the record's taken ledger (U242): an entry a pass made, or one
    copied from a pass's legacy mark, stands at its stamp. One the migration
    made for an undated prefix does not, since its stamp is when it was found.
    """
    standing: dict[str, str] = {}

    def keep(playlist_id: str, marked: str) -> None:
        held = standing.get(playlist_id)
        if held is None or marked > held:
            standing[playlist_id] = marked

    for entry in marks:
        # A PREFIX A PASS WROTE, never a title ``sync strip`` wrote (U242).
        if not entry.unmarked and getattr(entry, "of_the_prefix", True):
            keep(entry.playlist_id, str(entry.marked))
    for entry in taken:
        if entry.held and entry.dated:
            keep(entry.playlist_id, str(entry.at))
    return standing


def playlists_in_folders(remote: RemoteAccount) -> set[str]:
    """Every playlist any folder on the account holds, nested folders included.

    A playlist two folders down is never listed by a root folder's
    ``folder_playlists``, and read as at the root it would be moved out.
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


def at_root(listed: Sequence[Any], in_folders: set[str] | frozenset[str]) -> list[Any]:
    """The listed playlists no folder holds, which are the ones at the account root."""
    return [one for one in listed if one.playlist_id not in in_folders]


def by_name(pairs: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """``(identifier, name)`` pairs in name, then identifier, order."""
    return sorted(pairs, key=lambda pair: (pair[1], pair[0]))


def plan(
    cfg: config.Config, *, listed: Sequence[Any], remote: RemoteAccount, labels: Iterable[str],
    marks: Iterable[Any], working: Any, taken: Iterable[Any] = (),
) -> FilePlan:
    """Decide every playlist at the account root. Reads, and writes nothing.

    ``listed`` is every playlist the account created, ``marks`` is ``sync
    mark``'s record, ``taken`` its taken ledger's entries (U242), and
    ``working`` answers whether a name is one of the product's own working
    playlists. A playlist in a folder is not this step's, save one in a
    ``Mine`` this product made (U131).
    """
    from cratekit.modules.outbound import kinds, ledger

    labels = tuple(labels)
    root = remote.folders()
    in_folders = playlists_in_folders(remote)
    label_built = ledger.label_playlist_ids(cfg)
    set_built = ledger.set_playlist_ids(cfg)
    exported = ledger.exported_playlist_ids(cfg)
    root_playlists = at_root(listed, in_folders)
    made = ledger.product_made_among(cfg, (one.playlist_id for one in root_playlists))
    taken = tuple(taken)
    standing = _standing_marks(marks, taken)
    held_taken = frozenset(entry.playlist_id for entry in taken if entry.held)
    years: dict[str, YearFolder] = {}
    kind_folders: dict[str, kinds.KindFolder] = {}
    rows: list[Placement] = []

    def year_row(identity: str, name: str, year: str) -> Placement:
        if year not in years:
            years[year] = year_folder(cfg, year, root)
        folder = years[year]
        if folder.why:
            return Placement(identity, name, LEFT, year=year, why=folder.why)
        return Placement(identity, name, MOVE, year=year)

    def kind_row(identity: str, name: str, kind: str, why: str) -> Placement:
        if kind not in kind_folders:
            kind_folders[kind] = kinds.decide(cfg, kind, root)
        folder = kind_folders[kind]
        if folder.why:
            return Placement(identity, name, LEFT, why=folder.why, kind=kind)
        return Placement(identity, name, MOVE, why=why, kind=kind)

    # A MARKED PLAYLIST ALREADY IN MINE moves on to its year, and only out of a
    # Mine this product made. Nothing else in Mine is shown: it is filed.
    mine = kinds.decide(cfg, kinds.MINE, root)
    if mine.made and mine.folder_id:
        for identity, name in by_name(remote.folder_playlists(mine.folder_id).items()):
            year = year_of_mark(standing.get(identity, ""))
            if year and identity not in label_built and identity not in set_built:
                row = year_row(str(identity), str(name), year)
                if row.action == MOVE:
                    rows.append(row)
    for one in sorted(root_playlists, key=lambda playlist: (playlist.name, playlist.playlist_id)):
        identity, name = str(one.playlist_id), str(one.name)
        if identity in label_built:
            rows.append(Placement(identity, name, LEFT, why=LABEL_STEP))
            continue
        if identity in set_built:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
            continue
        claimed = identity in exported or identity in made
        empty = not claimed and one.tracks == 0
        # DEBRIS IS ASKED BEFORE THE LABEL'S NAME (U143), since ``<label>
        # LIBRARY`` starts with a followed label's name and is not its playlist.
        if not claimed and is_library_debris(name):
            rows.append(Placement(identity, name, LEFT, why=EMPTY if empty else DEBRIS))
            continue
        # A TAKEN PLAYLIST IS NEVER READ AS A LABEL'S BY ITS NAME (U242).
        if not is_taken(identity, name, held_taken) and own.label_of(name, labels) is not None:
            rows.append(Placement(identity, name, LEFT, why=LABEL_STEP))
            continue
        if working(name):
            rows.append(Placement(identity, name, LEFT, why=WORKING))
            continue
        # AN EMPTY PLAYLIST IS THE ROOT STEP'S WHATEVER ITS MARK: it downloaded nothing.
        if empty:
            rows.append(Placement(identity, name, LEFT, why=EMPTY))
            continue
        year = year_of_mark(standing.get(identity, ""))
        if year:
            rows.append(year_row(identity, name, year))
            continue
        if identity in exported:
            rows.append(kind_row(identity, name, kinds.EXPORTS, EXPORTED))
            continue
        if identity in made:
            rows.append(Placement(identity, name, LEFT, why=PRODUCT_MADE))
            continue
        # UNCLAIMED AND UNMARKED: a working custom playlist, kept at the root (U143).
        if identity not in standing and not is_taken(identity, name, held_taken):
            rows.append(Placement(identity, name, LEFT, why=WORKING_CUSTOM))
            continue
        # UNCLAIMED AND NO YEAR FILES IT: the author's own, filed in Mine (U131).
        why = UNDATED if identity in standing else PREFIXED_UNMARKED
        rows.append(kind_row(identity, name, kinds.MINE, why))
    return FilePlan(rows=tuple(rows), years=years, kinds=kind_folders, root=dict(root))


def failed_part_way(exc: Exception, wrote: str, done: Any, again: str, origin) -> Exception:
    """An apply's failure with what it wrote first said in front, and its totals in detail.

    A refusal keeps its reason and remedy and gains ``again`` as a step; any
    other failure is this build's own, which ``organize`` names a defect.
    """
    if not isinstance(exc, CratekitError):
        return RuntimeError(f"{wrote}. {type(exc).__name__}: {exc}")
    cause = exc.cause
    return refuse(
        cause.reason, f"{wrote}. {cause.message}",
        remedy=cause.remediation.remedy, steps=(*cause.remediation.steps, again),
        scope=Scope.RUN, retryable=cause.retryable, origin=origin,
        detail={**dict(cause.detail), **done.totals()}, inner=cause,
    )


def reserve_year(
    cfg: config.Config, remote: RemoteAccount, folder: YearFolder, folders: dict[str, str],
    created: list[str],
) -> str:
    """The year's folder identifier, made once on the account if the plan found none.

    ``folders`` and ``created`` take a made folder as soon as the provider
    answers, before the ledger write, so a write that then raises still names
    it. A folder another step recorded first in the same apply is reused.
    """
    from cratekit.modules.outbound import ledger, sets

    def create() -> str:
        folder_id = remote.create_folder(folder.year)
        folders[folder.year] = folder_id
        created.append(folder.year)
        return folder_id

    adopt = folder.folder_id if folder.action == sets.ADOPT else ""
    return ledger.reserve_set_folder(cfg, folder.year, create, adopt=adopt, stale=folder.stale)[0]


def move_into_year(cfg, remote: RemoteAccount, years, done: Any, year: str, target: str) -> None:
    """Move one playlist into its year's folder, reserving the folder once per apply."""
    if year not in done.folders:
        done.folders[year] = reserve_year(cfg, remote, years[year], done.folders, done.created)
    remote.move_to_folder(target, done.folders[year])
    done.moved.append([target, done.folders[year]])


def apply(cfg: config.Config, remote: RemoteAccount, planned: FilePlan) -> Filed:
    """Make or reuse each year's folder, then move each planned playlist into it.

    STOPS AT THE FIRST REFUSAL and raises it with what moved named, so a
    provider that refuses part way leaves a run that says what to put back.
    """
    from cratekit.modules.outbound import kinds

    done = Filed()
    try:
        for row in planned.moves:
            if not row.kind:
                move_into_year(cfg, remote, planned.years, done, row.year, row.playlist_id)
                continue
            if row.kind not in done.kinds:
                done.kinds[row.kind] = kinds.reserve(
                    cfg, remote, planned.kinds[row.kind], done.kinds_created
                )
            remote.move_to_folder(row.playlist_id, done.kinds[row.kind])
            done.moved.append([row.playlist_id, done.kinds[row.kind]])
    except Exception as exc:
        if done.moved or done.created or done.kinds_created:
            wrote = (
                f"before this failed {len(done.created)} year folder(s) were created, "
                f"{len(done.kinds_created)} kind folder(s) were created and "
                f"{len(done.moved)} playlist(s) were moved: "
                + ", ".join(f"{playlist} into {folder}" for playlist, folder in done.moved)
            ).rstrip(": ")
        else:
            wrote = "nothing was moved before this failed"
        again = "run crate organize again; a year folder made is reused, never made twice"
        raise failed_part_way(exc, wrote, done, again, _ORIGIN) from exc
    return done


__all__ = [
    "DEBRIS", "EMPTY", "EXPORTED", "LABEL_STEP", "LEFT", "MOVE", "PREFIXED_UNMARKED",
    "PRODUCT_MADE", "SET_STEP", "UNDATED", "WORKING", "WORKING_CUSTOM", "FilePlan", "Filed",
    "Placement", "YearFolder", "apply", "at_root", "plan", "playlists_in_folders",
    "reserve_year", "year_folder", "year_of_mark",
]
