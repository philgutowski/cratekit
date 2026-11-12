"""The account root kept to working custom playlists and the product's folders (U143).

PHILLIP'S RULE OF 2026-10-13. Only a working custom playlist belongs at the
account root: one the product did not make, that no ledger claims, holding
tracks, that he is still building, which the next sync prefixes and the filing
step files by its year. Everything else at the root is filed when its tracks
are already downloaded and removed when they are not. This step removes three
kinds and no other, each named on the account area's gate:

* THE SOURCE SYSTEM'S LABEL DEBRIS, a root playlist whose name carries the
  label batch's ` LIBRARY` suffix (R-361), is removed when every one of its
  tracks is already in a downloaded (taken) playlist of its label's folder. One
  with a track the folder lacks is left and the track is named; one whose
  tracks could not all be read, or whose label's folder a name cannot decide,
  is left with that reason. Unread is not none;
* AN EMPTY ROOT PLAYLIST no ledger claims is removed;
* A LEGACY YEAR FOLDER, a root folder named ``<year> Custom Playlists``, has
  each of its playlists moved into the ``<year>`` folder on the filing step's
  year rule, and is removed on a LATER run that reads it empty, never by the
  apply that emptied it, since the plan that removes it is one taken over an
  empty folder. One holding a folder is left: organize never moves a folder.

WHICH ROOT PLAYLISTS ARE CANDIDATES IS THE FILING PLAN'S CALL, its ``DEBRIS``
and ``EMPTY`` rows, so the two steps read one classification and a playlist is
never both filed and removed. A working custom playlist is a filing row left at
the root, and nothing here plans anything for it, whatever its age.

NOTHING IN A LABEL FOLDER, IN ``Mine``, OR IN ANY OTHER FOLDER A PERSON MADE IS
TOUCHED. A label folder is read, never written; a folder of any other name is
never read at all.

EVERY REMOVAL AND MOVE IS NAMED ON THE APPLIED TOTALS. Before each playlist
removal the apply reads again where the playlist sits and, for debris, what it
holds; a row no longer what the gate showed, or one the account member refuses
before sending anything, is KEPT, named on the totals and in a warning, and the
apply goes on. Any other refusal stops it, raised with what was already done
named, so a run says exactly what it removed.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import kinds, ledger
from cratekit.modules.outbound.service import RemoteAccount
from cratekit.organize import filing
from cratekit.sync.playlists import LIBRARY_PLAYLIST_SUFFIX, is_taken, taken_ids

_ORIGIN = ("organize.root",)

#: What becomes of one row.
REMOVE = "remove"
MOVE = "move"
LEFT = "left"

#: What a row names.
PLAYLIST = "playlist"
FOLDER = "folder"

#: The third kind beside ``kinds.DEBRIS`` and ``kinds.EMPTY``.
LEGACY = "legacy"

#: How many missing tracks a left debris row names before it counts the rest.
NAMED_MISSING = 10

#: Why a row is removed, one sentence each.
EVERY_TRACK_FILED = "every track is in the label folder"
HOLDS_NOTHING = "it holds no track"
FOLDER_EMPTY = "a legacy year folder read empty, its playlists already filed by year"


@dataclass(frozen=True, slots=True)
class RootRow:
    """One playlist or folder at the root, or in a legacy year folder, and its fate."""

    target: str
    name: str
    kind: str
    action: str
    what: str = PLAYLIST
    year: str = ""
    #: The legacy year folder a moved playlist leaves, or the label folder a
    #: debris playlist was compared against.
    folder: str = ""
    why: str = ""
    #: The tracks a debris removal was planned over, read again before the
    #: removal, so one given a track since the gate was answered is kept.
    tracks: tuple[str, ...] = ()

    def item(self, years: Mapping[str, filing.YearFolder]) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "id": self.target,
            "kind": self.what,
            "name": self.name,
            "action": self.action,
            "root_kind": self.kind,
        }
        if self.year:
            shown["year"] = self.year
        if self.folder:
            shown["from_folder" if self.kind == LEGACY else "label_folder"] = self.folder
        if self.action == MOVE:
            shown["folder"] = years[self.year].action
            shown["folder_id"] = years[self.year].folder_id
        if self.why:
            shown["why"] = self.why
        return shown

    def line(self) -> str:
        """The row as one line of the gate's removals."""
        return f"remove the {self.what} {self.name!r} ({self.kind}): {self.why}"


@dataclass(frozen=True, slots=True)
class RootPlan:
    """Every root row this step decided, and each year's folder a move names."""

    rows: tuple[RootRow, ...]
    years: Mapping[str, filing.YearFolder] = field(default_factory=dict)

    @property
    def removals(self) -> tuple[RootRow, ...]:
        return tuple(row for row in self.rows if row.action == REMOVE)

    @property
    def moves(self) -> tuple[RootRow, ...]:
        return tuple(row for row in self.rows if row.action == MOVE)

    @property
    def writes(self) -> bool:
        return bool(self.removals or self.moves)

    def identity(self) -> dict[str, Any]:
        """What the digest covers: every row, and every year's folder a move names."""
        return {
            "kind": "root",
            "rows": [
                [
                    row.target,
                    row.kind,
                    row.action,
                    row.what,
                    row.year,
                    row.folder,
                    row.why,
                    sorted(row.tracks),
                ]
                for row in self.rows
            ],
            "years": [
                [one.year, one.action, one.folder_id, one.stale, one.why]
                for one in (self.years[year] for year in sorted(self.years))
            ],
        }

    def items(self) -> list[dict[str, Any]]:
        return [row.item(self.years) for row in self.rows]


@dataclass
class Kept:
    """What an apply wrote, in the order it wrote it."""

    #: Each year's folder in hand, and the years whose folder this apply made.
    folders: dict[str, str] = field(default_factory=dict)
    created: list[str] = field(default_factory=list)
    #: Each move made, ``[playlist, folder]``, which is what a move back reads.
    moved: list[list[str]] = field(default_factory=list)
    #: Each removal made, ``[kind, identifier, name]``.
    removed: list[list[str]] = field(default_factory=list)
    #: Each removal the gate named and the apply did not make, because the
    #: playlist or folder is no longer what was planned, ``[kind, identifier,
    #: name, why]``. Nothing was sent for it.
    kept: list[list[str]] = field(default_factory=list)

    def totals(self) -> dict[str, Any]:
        return {
            "folders": dict(self.folders),
            "folders_created": list(self.created),
            "moved": [list(one) for one in self.moved],
            "removed": [list(one) for one in self.removed],
            "kept": [list(one) for one in self.kept],
        }


class _LabelFolders:
    """Each label's folder and the tracks its taken playlists hold, read once."""

    def __init__(
        self,
        cfg: config.Config,
        remote: RemoteAccount,
        root: Mapping[str, str],
        followed: Iterable[tuple[str, str]],
    ) -> None:
        self._cfg = cfg
        self._remote = remote
        self._root = root
        self._followed = tuple(followed)
        self._held: dict[str, tuple[int, frozenset[str]]] = {}
        self._taken: frozenset[str] | None = None

    def find(self, label: str) -> tuple[str, str]:
        """``(folder_id, "")`` for the label's folder, or ``("", why)`` when none is decided.

        A FOLLOWED LABEL'S RECORDED FOLDER, still at the root, is the label's
        whatever it is called now. Otherwise the one root folder named as the
        label is, and none or several leave the debris where it is.
        """
        for label_id, name in self._followed:
            if name == label:
                recorded = ledger.label_shape(self._cfg, label_id).folder_id
                if recorded and recorded in self._root:
                    return recorded, ""
        named = sorted(folder_id for folder_id, title in self._root.items() if title == label)
        if len(named) == 1:
            return named[0], ""
        if not named:
            return "", (
                f"no root folder is named {label!r}, so whether its tracks are "
                f"downloaded is not something this account can show"
            )
        return "", (
            f"the account holds {len(named)} root folders named {label!r}, so which "
            f"one is the label's is not something its name decides"
        )

    def downloaded(self, folder_id: str) -> tuple[int, frozenset[str]]:
        """How many taken playlists the folder holds, and every track on them.

        TAKEN BY THE RECORD OR BY THE OLD PREFIX (U242): ``label mark`` holds
        a year playlist as taken and changes no title, and one marked before
        it keeps the ``DOWNLOADED`` prefix until ``sync strip`` takes it off.
        The record is read once, the first time a folder is asked about, and
        an unreadable one refuses the row as any unread read does.
        """
        if folder_id not in self._held:
            if self._taken is None:
                self._taken = taken_ids(self._cfg)
            playlists = [
                playlist_id
                for playlist_id, name in self._remote.folder_playlists(folder_id).items()
                if is_taken(playlist_id, name, self._taken)
            ]
            tracks: set[str] = set()
            for playlist_id in playlists:
                tracks.update(str(one) for one in self._remote.playlist_tracks(playlist_id))
            self._held[folder_id] = (len(playlists), frozenset(tracks))
        return self._held[folder_id]


def _missing_named(names: Mapping[str, tuple[str, str]], missing: Sequence[str]) -> str:
    shown = [
        " - ".join(part for part in names.get(one, ("", one)) if part) or one
        for one in missing[:NAMED_MISSING]
    ]
    more = len(missing) - len(shown)
    return ", ".join(shown) + (f" and {more} more" if more else "")


def _debris(
    remote: RemoteAccount,
    folders: _LabelFolders,
    placed: filing.Placement,
    declared: int | None,
) -> RootRow:
    """One debris playlist, removed only when every track it holds is in its label's folder."""
    identity, name = placed.playlist_id, placed.name
    label = name[: -len(LIBRARY_PLAYLIST_SUFFIX)]

    def left(why: str, folder: str = "") -> RootRow:
        return RootRow(identity, name, kinds.DEBRIS, LEFT, folder=folder, why=why)

    if not isinstance(declared, int) or isinstance(declared, bool):
        return left(
            f"the listing gave no track count, so whether every track is in the "
            f"{label} folder is not known"
        )
    folder_id, why = folders.find(label)
    if why:
        return left(why)
    # A READ THAT FAILS LEAVES THIS ROW ALONE, with its reason, so one label
    # folder the provider would not list refuses no other row of the step.
    try:
        count, held = folders.downloaded(folder_id)
        if not count:
            return left(
                f"the {label} folder holds no downloaded playlist, so none of its tracks "
                f"is shown as downloaded",
                folder_id,
            )
        tracks = [str(one) for one in remote.playlist_tracks(identity)]
        # UNREAD IS NOT NONE. A track the account cannot play is left out of
        # the read and still counted, so a read short of the declared count
        # cannot say every track is filed, and the playlist stays.
        if len(tracks) != declared:
            return left(
                f"{len(tracks)} of its {declared!r} track(s) could be read, so whether "
                f"every one is in the {label} folder is not known",
                folder_id,
            )
        missing = [one for one in dict.fromkeys(tracks) if one not in held]
        if missing:
            return left(
                f"{len(missing)} of its tracks are in no downloaded playlist of the {label} "
                f"folder: {_missing_named(remote.track_names(identity), missing)}",
                folder_id,
            )
    except CratekitError as exc:
        return left(
            f"its tracks or the {label} folder could not be read, so nothing is planned "
            f"for it: {exc.cause.message}",
            folder_id,
        )
    return RootRow(
        identity,
        name,
        kinds.DEBRIS,
        REMOVE,
        folder=folder_id,
        why=EVERY_TRACK_FILED,
        tracks=tuple(dict.fromkeys(tracks)),
    )


def _legacy(
    cfg: config.Config,
    remote: RemoteAccount,
    root: Mapping[str, str],
    years: dict[str, filing.YearFolder],
    folder_id: str,
    name: str,
    year: str,
) -> list[RootRow]:
    """One legacy year folder: its playlists filed by year, or itself removed once empty."""
    held = remote.folder_playlists(folder_id)
    nested = remote.folder_folders(folder_id)
    if not held and not nested:
        return [RootRow(folder_id, name, LEGACY, REMOVE, what=FOLDER, year=year, why=FOLDER_EMPTY)]
    rows: list[RootRow] = []
    if held:
        if year not in years:
            years[year] = filing.year_folder(cfg, year, root)
        target = years[year]
        for playlist_id, title in sorted(held.items(), key=lambda pair: (pair[1], pair[0])):
            if target.why:
                rows.append(
                    RootRow(playlist_id, title, LEGACY, LEFT, year=year, folder=folder_id, why=target.why)
                )
            else:
                rows.append(
                    RootRow(
                        playlist_id,
                        title,
                        LEGACY,
                        MOVE,
                        year=year,
                        folder=folder_id,
                        why=f"filed from {name} into the {year} folder",
                    )
                )
    if nested:
        stays = f"it holds {len(nested)} folder(s), and organize never moves a folder, so it stays"
    elif years[year].why:
        stays = f"its playlists stay in it until the {year} folder is decided: {years[year].why}"
    else:
        stays = (
            f"it holds {len(held)} playlist(s), so it is removed by a later run that "
            f"reads it empty, never by the apply that empties it"
        )
    rows.append(RootRow(folder_id, name, LEGACY, LEFT, what=FOLDER, year=year, why=stays))
    return rows


def plan(
    cfg: config.Config,
    *,
    listed: Sequence[Any],
    remote: RemoteAccount,
    filed: filing.FilePlan,
    followed: Iterable[tuple[str, str]] = (),
) -> RootPlan:
    """Decide every removal and legacy move at the root. Reads, and writes nothing.

    ``filed`` is the filing step's plan over the same listing, whose ``DEBRIS``
    and ``EMPTY`` rows are this step's candidates. ``followed`` is each
    followed label as ``(label_id, name)``, for its recorded folder.
    """
    declared = {str(one.playlist_id): one.tracks for one in listed}
    # THE FILING PLAN'S OWN READ OF THE ROOT, taken over the same listing.
    root = filed.root
    folders = _LabelFolders(cfg, remote, root, followed)
    years: dict[str, filing.YearFolder] = {}
    rows: list[RootRow] = []
    for placed in filed.rows:
        if placed.action != filing.LEFT:
            continue
        if placed.why == filing.EMPTY:
            rows.append(
                RootRow(placed.playlist_id, placed.name, kinds.EMPTY, REMOVE, why=HOLDS_NOTHING)
            )
        elif placed.why == filing.DEBRIS:
            rows.append(_debris(remote, folders, placed, declared.get(placed.playlist_id)))
    for folder_id, name in sorted(root.items(), key=lambda pair: (pair[1], pair[0])):
        year = kinds.legacy_year(name)
        if year:
            rows.extend(_legacy(cfg, remote, root, years, folder_id, name, year))
    return RootPlan(rows=tuple(rows), years=years)


def _failed_part_way(exc: Exception, done: Kept) -> Exception:
    """The failure, with every folder made, move made and removal made named in it."""
    if done.moved or done.created or done.removed:
        wrote = (
            f"before this failed {len(done.created)} year folder(s) were created, "
            f"{len(done.moved)} playlist(s) were moved ("
            + ", ".join(f"{playlist} into {folder}" for playlist, folder in done.moved)
            + f") and {len(done.removed)} removed ("
            + ", ".join(f"the {kind} {name!r}" for kind, _target, name in done.removed)
            + ")"
        )
    else:
        wrote = "nothing was moved or removed before this failed"
    detail = done.totals()
    again = "run crate organize again; what was removed is not asked for twice"
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
    return RuntimeError(f"{wrote}. {type(exc).__name__}: {exc}")


#: The refusals an account removal raises BEFORE it sends anything: the
#: playlist or folder is no longer what the gate showed. The row is kept,
#: named on the totals, and the apply goes on to the next.
KEPT_PROBLEMS = frozenset(
    {"not-this-kind", "ledger-claimed", "not-owned", "not-a-legacy-folder", "not-empty"}
)


def _still_planned(remote: RemoteAccount, row: RootRow, in_folders: set[str]) -> str:
    """Why a planned playlist removal no longer holds, read now, or ``""``.

    THE ADAPTER CHECKS THE KIND, NOT THE PLACE OR THE TRACKS, so both are read
    again here: a playlist moved into a folder since the gate was answered is
    not at the root, and a debris playlist given a track since may hold one
    its label folder lacks.
    """
    if row.target in in_folders:
        return "it is in a folder now, and nothing in a folder is removed"
    if row.kind == kinds.DEBRIS:
        now = {str(one) for one in remote.playlist_tracks(row.target)}
        if not now <= set(row.tracks):
            return "it holds a track it did not hold when the gate was answered"
    return ""


def apply(cfg: config.Config, remote: RemoteAccount, planned: RootPlan) -> Kept:
    """File each legacy playlist by year, then make each removal the gate named.

    THE MOVES COME FIRST, since they remove nothing, then the playlist
    removals, then the folder removals, each through the account member
    narrowed to its kind. A row no longer what was planned is KEPT, nothing
    sent for it, and named on the totals; any other refusal STOPS the apply
    and is raised with what was done named.
    """
    done = Kept()

    def keep(row: RootRow, why: str) -> None:
        done.kept.append([row.kind, row.target, row.name, why])

    try:
        for row in planned.moves:
            if row.year not in done.folders:
                done.folders[row.year] = filing.reserve_year(
                    cfg, remote, planned.years[row.year], done.folders, done.created
                )
            remote.move_to_folder(row.target, done.folders[row.year])
            done.moved.append([row.target, done.folders[row.year]])
        playlists = [row for row in planned.removals if row.what == PLAYLIST]
        in_folders = filing.playlists_in_folders(remote) if playlists else set()
        for row in (*playlists, *(row for row in planned.removals if row.what == FOLDER)):
            if row.what == PLAYLIST:
                why = _still_planned(remote, row, in_folders)
                if why:
                    keep(row, why)
                    continue
            try:
                if row.what == PLAYLIST:
                    remote.remove_root_playlist(row.target, row.kind)
                else:
                    remote.remove_legacy_folder(row.target)
            except CratekitError as exc:
                if exc.cause.detail.get("problem") not in KEPT_PROBLEMS:
                    raise
                keep(row, exc.cause.message)
                continue
            done.removed.append([row.kind, row.target, row.name])
    except Exception as exc:
        raise _failed_part_way(exc, done) from exc
    return done


__all__ = [
    "EVERY_TRACK_FILED",
    "FOLDER",
    "FOLDER_EMPTY",
    "HOLDS_NOTHING",
    "KEPT_PROBLEMS",
    "LEFT",
    "LEGACY",
    "MOVE",
    "NAMED_MISSING",
    "PLAYLIST",
    "REMOVE",
    "Kept",
    "RootPlan",
    "RootRow",
    "apply",
    "plan",
]
