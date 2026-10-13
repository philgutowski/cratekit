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
* A PLAYLIST AN EXPORT MADE, by the ledger's record, is moved into the root
  ``Exports`` folder (U131);
* THE SOURCE SYSTEM'S LABEL DEBRIS, and an unclaimed playlist holding no
  track, are left for the root step (U143), :mod:`cratekit.organize.root`,
  which removes each it can, by name on the gate;
* A WORKING CUSTOM PLAYLIST, one no ledger claims and no sync marked, is left
  at the root, whatever its age (U143). It is the one playlist that belongs
  there, until a sync marks it and this step files it by its year. Before
  U143 it was moved into ``Mine`` (U131), and Phillip's rule of 2026-10-13
  reversed that;
* ONE NO LEDGER CLAIMS THAT A SYNC CANNOT FILE BY A YEAR, its name prefixed
  with no mark recorded or its mark carrying no year, is moved into the root
  ``Mine`` folder (U131), by name on the gate;
* what is left, the product's other playlists and any playlist whose folder a
  name cannot decide, is reported and left with its reason.

A PLAYLIST IN ``Mine`` IS STILL READ FOR ITS MARK (U131). One filed in ``Mine``
and marked by a later sync moves on into its year folder, as one at the root
does. Only a ``Mine`` this product made is read so; a playlist is never moved
out of a folder a person made, and one adopted by its name may be a person's.

THE YEAR FOLDER IS THE PLAIN ``<year>``, NEVER THE SETS' FOLDER (U142). A set
is archived into ``Downloaded Sets <year>``, recorded in the same ledger map
under that name, so the two never share a folder. The year folder is decided on
the archive's rule: a folder recorded and still listed is reused, one root
folder named as the year is adopted, and none is created once, on apply, for
every playlist of that year. Two or more root folders named as the year leave
that year's playlists where they are, reported, since a playlist the plan
cannot place is never moved.

ADD ONLY. A folder is created and a playlist is put in one; nothing is renamed,
nothing is removed. The root's three removals are the root step's (U143), on
rows this plan leaves for it. A move is undone by a move back,
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
from cratekit.modules.outbound import kinds, ledger, sets
from cratekit.modules.outbound.service import RemoteAccount
from cratekit.organize import own
from cratekit.sync.playlists import is_library_debris, is_swept_name

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
    "its name says downloaded but no sync recorded when, so no year can be chosen"
)
UNDATED = "its mark carries no year, so no year folder is its own"
#: Why a playlist goes to its kind's folder rather than a year's (U131).
EXPORTED = "made by export playlist, so it is filed with the exports"


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
    #: The kind folder a move goes to, ``Mine`` or ``Exports``, when not a year.
    kind: str = ""

    def item(self, folder: YearFolder | kinds.KindFolder | None) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "id": self.playlist_id,
            "kind": "playlist",
            "name": self.name,
            "action": self.action,
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
        """The years whose folder a move needs and the account does not hold."""
        wanted = {row.year for row in self.moves if row.year}
        made = sorted(year for year in wanted if self.years[year].action == sets.CREATE)
        wanted_kinds = {row.kind for row in self.moves if row.kind}
        made += sorted(
            kind for kind in wanted_kinds if self.kinds[kind].action == kinds.CREATE
        )
        return tuple(made)

    def identity(self) -> dict[str, Any]:
        """What the digest covers: every row at the root, and every year's folder."""
        return {
            "kind": "filing",
            "rows": [
                [row.playlist_id, row.action, row.year, row.why, row.kind] for row in self.rows
            ],
            "years": [
                [one.year, one.action, one.folder_id, one.stale, one.why]
                for one in (self.years[year] for year in sorted(self.years))
            ],
            "kinds": [
                [one.kind, one.action, one.folder_id, one.stale, one.why]
                for one in (self.kinds[kind] for kind in sorted(self.kinds))
            ],
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
            "folders": dict(self.folders),
            "folders_created": list(self.created),
            "kind_folders": dict(self.kinds),
            "kind_folders_created": list(self.kinds_created),
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


def year_folder(cfg: config.Config, year: str, root: Mapping[str, str]) -> YearFolder:
    """One year's folder on the set archive's rule, never refused here.

    The root step's legacy moves (U143) decide the year's folder by this same
    rule, so the two steps file into one folder and never make two.
    """
    recorded = ledger.set_folder(cfg, year)
    # A RECORD WHOSE FOLDER NOW CARRIES THE SETS' NAME IS NOT THE YEAR'S (U142).
    # Before U142 the archive recorded its folder under the plain year, so a
    # person who renamed that folder to ``Downloaded Sets <year>`` left the
    # year's record pointing at the sets' folder. Reused by identifier, it would
    # file custom playlists among the sets, so it is read as stale and replaced.
    # NOR IS ONE NOW NAMED AS A LEGACY YEAR FOLDER (U143), which the root step
    # empties into the year's folder: reused, it would be emptied into itself.
    if (
        recorded
        and recorded in root
        and root[recorded] != sets.folder_name(year)
        and not kinds.legacy_year(root[recorded])
    ):
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


def at_root(listed: Sequence[Any], in_folders: set[str] | frozenset[str]) -> list[Any]:
    """The listed playlists no folder holds, which are the ones at the account root."""
    return [one for one in listed if one.playlist_id not in in_folders]


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
    root and is not this step's, save one in the ``Mine`` this product made,
    which is read for a mark that sends it on to its year (U131).
    """
    labels = tuple(labels)
    root = remote.folders()
    in_folders = playlists_in_folders(remote)
    label_built = ledger.label_playlist_ids(cfg)
    set_built = ledger.set_playlist_ids(cfg)
    exported = ledger.exported_playlist_ids(cfg)
    root_playlists = at_root(listed, in_folders)
    made = ledger.product_made_among(cfg, (one.playlist_id for one in root_playlists))
    standing = _standing_marks(marks)
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
        held = remote.folder_playlists(mine.folder_id)
        for identity, name in sorted(held.items(), key=lambda pair: (pair[1], pair[0])):
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
        if own.label_of(name, labels) is not None:
            rows.append(Placement(identity, name, LEFT, why=LABEL_STEP))
            continue
        if working(name):
            rows.append(Placement(identity, name, LEFT, why=WORKING))
            continue
        # AN EMPTY PLAYLIST IS THE ROOT STEP'S WHATEVER ITS MARK, since a
        # playlist holding nothing downloaded nothing to file by a year.
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
        # NO LEDGER CLAIMS IT AND NO SYNC MARKED IT: a working custom playlist,
        # kept at the root (U143), however old.
        if identity not in standing and not is_swept_name(name):
            rows.append(Placement(identity, name, LEFT, why=WORKING_CUSTOM))
            continue
        # NO LEDGER CLAIMS IT AND NO YEAR FILES IT, so it is the author's own
        # (U131), filed in Mine with the reason it is not filed by a year.
        why = UNDATED if identity in standing else PREFIXED_UNMARKED
        rows.append(kind_row(identity, name, kinds.MINE, why))
    return FilePlan(rows=tuple(rows), years=years, kinds=kind_folders, root=dict(root))


def _failed_part_way(exc: Exception, done: Filed) -> Exception:
    """The failure, with every folder made and every move made named in it."""
    if done.moved or done.created or done.kinds_created:
        wrote = (
            f"before this failed {len(done.created)} year folder(s) were created, "
            f"{len(done.kinds_created)} kind folder(s) were created and "
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


def reserve_year(
    cfg: config.Config,
    remote: RemoteAccount,
    folder: YearFolder,
    folders: dict[str, str],
    created: list[str],
) -> str:
    """The year's folder identifier, made once on the account if the plan found none.

    ``folders`` and ``created`` are the caller's, and take the folder and its
    year as soon as the provider answers a create, before the ledger write, so
    a write that then raises still names the folder made. A folder another
    step recorded first in the same apply is reused, never made twice.
    """

    def create() -> str:
        folder_id = remote.create_folder(folder.year)
        folders[folder.year] = folder_id
        created.append(folder.year)
        return folder_id

    folder_id, _made = ledger.reserve_set_folder(
        cfg,
        folder.year,
        create,
        adopt=folder.folder_id if folder.action == sets.ADOPT else "",
        stale=folder.stale,
    )
    return folder_id


def apply(cfg: config.Config, remote: RemoteAccount, planned: FilePlan) -> Filed:
    """Make or reuse each year's folder, then move each planned playlist into it.

    STOPS AT THE FIRST REFUSAL and raises it with what moved named, so a
    provider that refuses part way leaves a run that says what to put back.
    """
    done = Filed()
    try:
        for row in planned.moves:
            if row.kind:
                if row.kind not in done.kinds:
                    done.kinds[row.kind] = kinds.reserve(
                        cfg, remote, planned.kinds[row.kind], done.kinds_created
                    )
                remote.move_to_folder(row.playlist_id, done.kinds[row.kind])
                done.moved.append([row.playlist_id, done.kinds[row.kind]])
                continue
            if row.year not in done.folders:
                done.folders[row.year] = reserve_year(
                    cfg, remote, planned.years[row.year], done.folders, done.created
                )
            remote.move_to_folder(row.playlist_id, done.folders[row.year])
            done.moved.append([row.playlist_id, done.folders[row.year]])
    except Exception as exc:
        raise _failed_part_way(exc, done) from exc
    return done


__all__ = [
    "DEBRIS",
    "EMPTY",
    "EXPORTED",
    "LABEL_STEP",
    "LEFT",
    "MOVE",
    "PREFIXED_UNMARKED",
    "PRODUCT_MADE",
    "SET_STEP",
    "UNDATED",
    "WORKING",
    "WORKING_CUSTOM",
    "FilePlan",
    "Filed",
    "Placement",
    "YearFolder",
    "apply",
    "at_root",
    "plan",
    "playlists_in_folders",
    "reserve_year",
    "year_folder",
    "year_of_mark",
]
