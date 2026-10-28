"""A native landing files its label tracks under the Record Labels tree (U156).

A label batch landed on the xml bridge files its tracks under ``Record Labels
/ <Label> / <Label> <year>`` inside the intake file the landing writes. The
native medium writes no intake file, so until this module a native landing
refused ``--manifest`` (R-771) and a label batch reached INBOX filed under
nothing. Bandcamp purchases made that common: a label's releases are bought
from the label's own account, so the label is known at download time and no
``label approved`` manifest exists for them.

AN APPENDED TREE, NOT A CUTOVER. The catalogue tree stays on the xml bridge in
the registry, because a catalogue crawl is not rebuildable (R39), and nothing
here records a cutover or rebuilds a node. This writer only appends: it finds
or makes the tree's folder at the playlist root, the label's folder under it
and the ``<Label> <year>`` playlist under that, and adds the memberships a
playlist lacks. Nothing it finds is renamed, moved, emptied or removed. It is
reached from the native landing alone, which runs only once the intake tree
is database native, and that is when the tree's one xml writer, the bridge
landing, can no longer run; :func:`plan` refuses by name on a library whose
intake tree is still on the bridge, so no caller can append beside an intake
file that will be imported over it.

TWO SOURCES OF A LABEL AND ITS YEAR. A manifest's rows carry both, and each row
is tied to a staged file by the bridge's own rule
(:func:`cratekit.intake.landing.match_label_rows`) over exactly the files the
landing planned, so a near match or a row no file answers is named and never
filed. ``--label NAME`` names the label for every file, and each file's year is
the leading four digits of its date tag: a file with no date tag, or one that
names no year, is named on the gate screen and filed nowhere, never given a
year on a guess. Either way the file still lands in its INBOX batch.

THE NAMES ARE COMPARED THE BRIDGE'S WAY, under canonical Unicode equivalence
and not case (R-453), and two siblings of one name refuse, as does a node of
the other kind, since whichever the query yielded first is not an answer
(R-129). A new node goes last among its siblings: inserting one at a position
renumbers every sibling after it, which is a write to rows this landing has no
business touching, so the order is the one thing this writer gives up beside
the bridge's newest first. A label folder this write makes gets its years
newest first, since it makes them in that order.

THE WRITE IS THE GUARDED WRITER'S, inside the landing's one session and one
commit, after the batch, the account playlists, the hearts and the set's
playlist, and every playlist it wrote is read back from SQL after the commit.

THE BRIDGE'S REASONS AND ITS MATCH RULE ARE IMPORTED WHERE THEY ARE USED, from
:mod:`cratekit.intake.landing`, which imports the native engine that imports
this module, so a module level import would be a cycle.

Layer: modules.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import match, match_cli
from cratekit.core import config, rb_writer, session, tags, taxonomy
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import ingest

if TYPE_CHECKING:  # pragma: no cover - typing only
    from cratekit.intake import landing

#: Where a plan's labels came from, as the gate screen and the record say it.
MANIFEST = "manifest"
LABEL = "label"

#: The session record field naming every year playlist a commit filed into,
#: which is what a later ``label mark`` of a native batch reads (R-916).
RECORD_KEY = "labels"

#: A date tag's year: its leading four digits, ``2021`` or ``2021-03-05``.
_YEAR = re.compile(r"^\s*(\d{4})(?!\d)")

_ORIGIN = ("intake.label_filing",)


def _folded(name: str) -> str:
    """A node name as two sibling names are compared, the bridge writer's rule."""
    return unicodedata.normalize("NFC", name)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class YearPlan:
    """One ``<Label> <year>`` playlist and the landing's targets it will hold."""

    label: str
    year: int
    #: The live playlist the write adds to, or empty when the write makes it.
    playlist_id: str
    #: The landing's targets, in the order the landing planned its files.
    targets: tuple[str, ...]

    @property
    def name(self) -> str:
        return f"{self.label} {self.year}"

    def identity(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "year": self.year,
            "playlist": self.playlist_id,
            "targets": list(self.targets),
        }


@dataclass(frozen=True, slots=True)
class Unfiled:
    """One file or manifest row this landing files under no label, and why."""

    #: The landing's target for a file, or empty for a manifest row no file answers.
    target: str
    reason: str
    sentence: str

    def identity(self) -> dict[str, Any]:
        return {"target": self.target, "reason": self.reason, "sentence": self.sentence}


@dataclass(frozen=True, slots=True)
class LabelPlan:
    """Where a landing's label tracks go: the tree, each label's folder, each year."""

    #: The declared catalogue tree's stable id, what the record keys the commit
    #: under (R19), and its display, what rekordbox shows at the playlist root.
    tree_id: str
    tree_display: str
    #: The tree's live folder at the root, or empty when the write makes it.
    tree_folder: str
    #: :data:`MANIFEST` or :data:`LABEL`.
    source: str
    #: The label ``--label`` named, or empty for a manifest.
    label: str
    #: The manifest's path and the fingerprint of its bytes, or empty.
    manifest: str
    manifest_digest: str
    #: Each label's live folder under the tree, or empty when the write makes it.
    folders: tuple[tuple[str, str], ...]
    years: tuple[YearPlan, ...]
    unfiled: tuple[Unfiled, ...]

    def folder_of(self, label: str) -> str:
        return dict(self.folders).get(label, "")

    def files(self) -> int:
        """The distinct targets filed under some label."""
        return len({target for one in self.years for target in one.targets})


def identity(plan: LabelPlan) -> dict[str, Any]:
    """What the digest covers: the source, the tree, every playlist and every file left out."""
    return {
        "kind": "label-filing",
        "source": plan.source,
        "label": plan.label,
        "manifest": plan.manifest,
        "manifest_bytes": plan.manifest_digest,
        "tree": plan.tree_id,
        "tree_display": plan.tree_display,
        "tree_folder": plan.tree_folder,
        "folders": [list(one) for one in plan.folders],
        "years": [one.identity() for one in plan.years],
        "unfiled": [one.identity() for one in plan.unfiled],
    }


def _catalog_node(medium: ingest.IntakeMedium) -> taxonomy.Node:
    """The declared catalogue tree, refused by name when there is none or it is not appendable.

    THE MEDIUM IS THE ONE SWITCH'S ANSWER (R-770), handed in by the verb that
    read it, never a second reading of the registry here.
    """
    declared = medium.declared
    node = declared.catalog if declared is not None else None
    if node is None:
        raise refuse(
            "catalog-tree-undeclared",
            "this library's taxonomy declares no catalog tree, so there is nowhere "
            "to file a label's tracks; the tree is declared alongside the routing "
            "tree and the intake flow, and this landing will not invent one, "
            "nothing was moved",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
        )
    # APPENDED ONLY BESIDE A NATIVE INTAKE TREE. While the intake tree is on
    # the bridge, its landing writes this tree into an intake file the person
    # imports, and an import of a playlist this writer appended to would land
    # over it. No caller reaches here then; a defect that did is refused.
    if declared is None or not medium.native:
        raise refuse(
            "internal-error",
            f"the intake tree {declared.intake.id!r} is on the xml bridge, so its "
            f"landing files labels into the intake file it writes and the "
            f"{node.display!r} tree is not appended to natively; nothing was moved",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"tree_id": declared.intake.id, "catalog": node.id},
        )
    return node


def _live_children(db: Any, parent_id: str | None) -> list[Any]:
    """Every live node directly under ``parent_id``, or under the playlist root for None."""
    rows = list(db.get_playlist())
    if parent_id is None:
        under = [row for row in rows if str(getattr(row, "ParentID", "")) in rb_writer.ROOT_PARENT_SENTINELS]
    else:
        under = [row for row in rows if str(getattr(row, "ParentID", "") or "") == parent_id]
    return [row for row in under if not rb_writer.node_removed(row)]


def _kind_of(row: Any) -> str:
    """What a node is, in a person's words: a folder, a playlist or a smart playlist."""
    if rb_writer.is_folder(row):
        return "folder"
    return "playlist" if int(getattr(row, "Attribute", 0) or 0) == 0 else "smart playlist"


def _of_kind(row: Any, *, folder: bool) -> bool:
    """Whether a node is a folder, or for ``folder=False`` a plain playlist.

    A SMART PLAYLIST IS NEITHER. The binding refuses a membership in one at
    the write, after the files have moved, so it is refused here, before the
    gate, as a node of the other kind.
    """
    return _kind_of(row) == ("folder" if folder else "playlist")


def _sole(children: Sequence[Any], name: str, *, folder: bool, where: str) -> str:
    """The id of the one live child named ``name`` of the kind asked for, or empty, or a refusal."""
    wanted = _folded(name)
    named = [row for row in children if _folded(str(getattr(row, "Name", "") or "")) == wanted]
    kind = "folder" if folder else "playlist"
    for row in named:
        if not _of_kind(row, folder=folder):
            other = _kind_of(row)
            raise refuse(
                "intake-list-unusable",
                f"a {other} named {name!r} sits {where} where the label filing "
                f"needs a {kind}, and replacing one with the other would lose what "
                f"it holds; rename it in rekordbox, nothing was moved",
                origin=_ORIGIN,
                detail={"name": name, "row": str(row.ID)},
            )
    if len(named) > 1:
        raise refuse(
            "intake-list-unusable",
            f"{len(named)} {kind}s named {name!r} sit side by side {where}, so the "
            f"label filing has no one {kind} to add to; merge or rename them in "
            f"rekordbox, nothing was moved",
            origin=_ORIGIN,
            detail={"name": name, "rows": [str(row.ID) for row in named]},
        )
    return str(named[0].ID) if named else ""


def _resolve(
    db: Any,
    node: taxonomy.Node,
    filed: Mapping[str, Mapping[int, Sequence[str]]],
) -> tuple[str, tuple[tuple[str, str], ...], tuple[YearPlan, ...]]:
    """The tree folder, each label's folder and each year's playlist, as the database holds them now."""
    tree_folder = _sole(
        _live_children(db, None), node.display, folder=True, where="at the playlist root"
    )
    folders: list[tuple[str, str]] = []
    years: list[YearPlan] = []
    for label in sorted(filed):
        folder = (
            _sole(
                _live_children(db, tree_folder),
                label,
                folder=True,
                where=f"under {node.display!r}",
            )
            if tree_folder
            else ""
        )
        folders.append((label, folder))
        held = _live_children(db, folder) if folder else []
        for year in sorted(filed[label], reverse=True):
            name = f"{label} {year}"
            playlist = (
                _sole(held, name, folder=False, where=f"under {label!r}") if folder else ""
            )
            years.append(
                YearPlan(
                    label=label,
                    year=year,
                    playlist_id=playlist,
                    targets=tuple(dict.fromkeys(filed[label][year])),
                )
            )
    return tree_folder, tuple(folders), tuple(years)


#: The first year a release can carry. A date tag below it, ``0000`` the commonest,
#: is a placeholder and not a year, and a year after next is a typing slip.
FIRST_YEAR = 1900


def _read_year(path: Path) -> tuple[int | None, str]:
    """The year a file's date tag names and, when there is none, why, in a person's words.

    A TAG THAT COULD NOT BE READ IS NOT A TAG THAT IS ABSENT (pattern 1), so the
    two are said apart: one is a fact about the file, the other about the read.
    """
    try:
        stored = tags.read_tags_checked(path, ("date",))["date"]
    except tags.TagReadFailed as exc:
        return None, f"its tags could not be read ({exc})"
    if not stored:
        return None, "it carries no date tag"
    found = _YEAR.match(stored)
    if found is None:
        return None, f"its date tag {stored!r} names no year"
    year = int(found.group(1))
    if not FIRST_YEAR <= year <= _today().year + 1:
        return None, f"its date tag {stored!r} names {year}, which is no release year"
    return year, ""


def _today() -> date:
    return date.today()


def year_of(path: Path) -> int | None:
    """The year a file's date tag names, its leading four digits within reason, or None."""
    return _read_year(path)[0]


def plan_for_label(
    db: Any,
    medium: ingest.IntakeMedium,
    *,
    label: str,
    files: Sequence[tuple[Path, Path]],
) -> LabelPlan:
    """Every file under ``label`` and the year its date tag names, on this handle.

    A FILE WITH NO YEAR IS NAMED, NOT GUESSED. The date tag is the only year a
    ``--label`` landing has, and a file whose tag is absent or opens with no
    four digit year is listed as filed nowhere; it still lands in INBOX.
    """
    from cratekit.intake import landing

    node = _catalog_node(medium)
    name = _folded(label.strip())
    filed: dict[str, dict[int, list[str]]] = {}
    unfiled: list[Unfiled] = []
    for source, target in files:
        year, why = _read_year(source)
        if year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no {name} year playlist, because "
                        f"{why}; it is in the intake playlist"
                    ),
                )
            )
            continue
        filed.setdefault(name, {}).setdefault(year, []).append(str(target))
    tree_folder, folders, years = _resolve(db, node, filed)
    return LabelPlan(
        tree_id=node.id,
        tree_display=node.display,
        tree_folder=tree_folder,
        source=LABEL,
        label=name,
        manifest="",
        manifest_digest="",
        folders=folders,
        years=years,
        unfiled=tuple(unfiled),
    )


def plan_for_manifest(
    cfg: config.Config,
    db: Any,
    medium: ingest.IntakeMedium,
    *,
    manifest: landing.LabelManifest,
    files: Sequence[tuple[Path, Path]],
) -> LabelPlan:
    """Every manifest row tied to a planned file by the bridge's rule, on this handle.

    THE INDEX IS OF THE PLANNED FILES ONLY, the bridge's rule for its batch
    folder: download staging also holds what other attempts left, and a row
    tied to a file this landing does not move is a row filed under nothing.
    """
    from cratekit.intake import landing

    node = _catalog_node(medium)
    sources = [source for source, _target in files]
    index = match.index_paths(sources, template=match_cli.library_template(cfg))
    ids = {source.resolve(): str(target) for source, target in files}
    matched, unmatched = landing.match_label_rows(manifest.rows, index, ids)
    # ONE LABEL UNDER ITS FOLDED NAME: two rows spelling one label composed and
    # decomposed are one folder, never two siblings that fold to one name.
    filed: dict[str, dict[int, list[str]]] = {}
    for label, by_year in matched.items():
        for year, rows in by_year.items():
            filed.setdefault(_folded(label), {}).setdefault(year, []).extend(
                target for _row, targets in rows for target in targets
            )
    tree_folder, folders, years = _resolve(db, node, filed)
    return LabelPlan(
        tree_id=node.id,
        tree_display=node.display,
        tree_folder=tree_folder,
        source=MANIFEST,
        label="",
        manifest=str(manifest.path),
        manifest_digest=manifest.digest,
        folders=folders,
        years=years,
        unfiled=tuple(Unfiled(target="", reason=one.reason, sentence=one.sentence) for one in unmatched),
    )


def supported_only(plan: LabelPlan, kept: set[str]) -> LabelPlan:
    """The plan without the targets the landing will leave in staging, each named as unfiled.

    ``kept`` is every target the landing makes or finds a row for. A file whose
    suffix the database has no type for stays in staging, so a year playlist
    that named it would plan a membership no row will ever answer.
    """
    from cratekit.intake import landing

    left: list[Unfiled] = []
    years: list[YearPlan] = []
    for one in plan.years:
        held = tuple(target for target in one.targets if target in kept)
        left.extend(
            Unfiled(
                target=target,
                reason=landing.NOT_WRITTEN,
                sentence=(
                    f"{Path(target).name} was filed under no label playlist, because "
                    f"its file stays in staging"
                ),
            )
            for target in one.targets
            if target not in kept
        )
        if held:
            years.append(
                YearPlan(label=one.label, year=one.year, playlist_id=one.playlist_id, targets=held)
            )
    if not left:
        return plan
    labels = {one.label for one in years}
    return LabelPlan(
        tree_id=plan.tree_id,
        tree_display=plan.tree_display,
        tree_folder=plan.tree_folder,
        source=plan.source,
        label=plan.label,
        manifest=plan.manifest,
        manifest_digest=plan.manifest_digest,
        folders=tuple(one for one in plan.folders if one[0] in labels),
        years=tuple(years),
        unfiled=(*plan.unfiled, *left),
    )


# ---------------------------------------------------------------------------
# What a person is shown and told
# ---------------------------------------------------------------------------


def label_of(plan: LabelPlan) -> dict[str, str]:
    """Each filed target and every playlist it goes in, for the gate screen's items.

    EVERY ONE, since two manifest rows can tie one file to two years, and a
    column naming the first would hide the second write.
    """
    named: dict[str, list[str]] = {}
    for one in plan.years:
        for target in one.targets:
            named.setdefault(target, []).append(one.name)
    return {target: ", ".join(names) for target, names in named.items()}


def facts(plan: LabelPlan) -> dict[str, Any]:
    """The facts beside the items on a gate screen, one line per fact."""
    where = (
        f"{plan.tree_display} (row {plan.tree_folder})"
        if plan.tree_folder
        else f"{plan.tree_display}, created at the playlist root"
    )
    said = (
        f"the manifest {plan.manifest}"
        if plan.source == MANIFEST
        else f"--label {plan.label}, each file's year from its date tag"
    )
    if not plan.years:
        where = "nothing, since no file has a label and year to be filed under"
    shown: dict[str, Any] = {
        "labels filed from": said,
        "labels filed under": where,
        "label playlists": [
            f"{one.name} ({len(one.targets)} file(s), "
            + ("added to)" if one.playlist_id else "made)")
            for one in plan.years
        ],
    }
    if plan.unfiled:
        shown["filed under no label"] = [one.sentence for one in plan.unfiled]
    return shown


def unfiled_warning(left: Sequence[Unfiled]) -> list[dict[str, str]]:
    """One warning per file or row filed under no label, in the words the screen showed."""
    return [{"code": one.reason, "message": one.sentence} for one in left]


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WrittenYear:
    """One year playlist a commit filed into."""

    label: str
    year: int
    playlist_id: str
    created: bool
    #: The content ids the playlist was asked to hold, in the landing's order.
    ids: tuple[str, ...]
    #: The memberships this commit added; fewer when the playlist held some.
    added: int
    #: The live content ids read back under the playlist after the commit.
    read_back: tuple[str, ...] = ()

    @property
    def name(self) -> str:
        return f"{self.label} {self.year}"


@dataclass(frozen=True, slots=True)
class Written:
    """What a commit filed under the tree, and every file or row left out."""

    tree_id: str
    tree_folder: str
    tree_created: bool
    folders_created: tuple[str, ...]
    years: tuple[WrittenYear, ...]
    left: tuple[Unfiled, ...]

    def added(self) -> int:
        return sum(one.added for one in self.years)

    def changed(self) -> bool:
        """Whether this commit added a membership or made a node."""
        return bool(
            self.added()
            or self.tree_created
            or self.folders_created
            or any(one.created for one in self.years)
        )


def _live_row(db: Any, row_id: str, *, folder: bool, what: str) -> Any:
    """The planned node, refused as stale when it is gone, removed or of the other kind."""
    row = db.get_playlist(ID=row_id)
    if row is None or rb_writer.node_removed(row) or not _of_kind(row, folder=folder):
        raise refuse(
            "decision-stale",
            f"the {what} (row {row_id}) the plan files into is not live any more, so "
            f"nothing was written",
            origin=_ORIGIN,
            detail={"row": row_id},
        )
    return row


def write(db: Any, plan: LabelPlan, *, by_target: Mapping[str, str]) -> Written:
    """Find or make every planned node and add every member, pending on ``db``.

    INSIDE THE LANDING'S SESSION, which commits or rolls back. ``by_target``
    maps a landing's targets to the rows it made or found; a member whose file
    made no row, because the move refused it, is left and named, and the rest
    are added. A year with no member left writes nothing, and a label with no
    year writes no folder, so the tree gains no empty node. ``add_memberships``
    adds only what a playlist lacks and removes nothing.
    """
    from cratekit.intake import landing

    left: list[Unfiled] = []
    wanted: list[tuple[YearPlan, tuple[str, ...]]] = []
    for one in plan.years:
        ids: list[str] = []
        for target in one.targets:
            held = by_target.get(target, "")
            if held:
                ids.append(held)
            else:
                left.append(
                    Unfiled(
                        target=target,
                        reason=landing.NOT_WRITTEN,
                        sentence=(
                            f"{Path(target).name} was filed under no label playlist, "
                            f"because its file did not land"
                        ),
                    )
                )
        if ids:
            wanted.append((one, tuple(dict.fromkeys(ids))))
    if not wanted:
        return Written(
            tree_id=plan.tree_id,
            tree_folder=plan.tree_folder,
            tree_created=False,
            folders_created=(),
            years=(),
            left=(*plan.unfiled, *left),
        )
    if plan.tree_folder:
        tree = _live_row(db, plan.tree_folder, folder=True, what=f"{plan.tree_display!r} folder")
        tree_created = False
    else:
        tree = db.create_playlist_folder(plan.tree_display)
        tree_created = True
    folders: dict[str, Any] = {}
    made: list[str] = []
    written: list[WrittenYear] = []
    for one, ids in wanted:
        folder = folders.get(one.label)
        if folder is None:
            planned = plan.folder_of(one.label)
            if planned:
                folder = _live_row(db, planned, folder=True, what=f"{one.label!r} folder")
            else:
                folder = db.create_playlist_folder(one.label, parent=tree)
                made.append(one.label)
            folders[one.label] = folder
        if one.playlist_id:
            playlist = _live_row(db, one.playlist_id, folder=False, what=f"{one.name!r} playlist")
            created = False
        else:
            playlist = db.create_playlist(one.name, parent=folder)
            created = True
        added = rb_writer.add_memberships(db, playlist, ids)
        written.append(
            WrittenYear(
                label=one.label,
                year=one.year,
                playlist_id=str(playlist.ID),
                created=created,
                ids=ids,
                added=len(added),
            )
        )
    return Written(
        tree_id=plan.tree_id,
        tree_folder=str(tree.ID),
        tree_created=tree_created,
        folders_created=tuple(made),
        years=tuple(written),
        left=(*plan.unfiled, *left),
    )


def read_back(db: Any, written: Written) -> Written:
    """The same answer with every year playlist's live members read from SQL."""
    from dataclasses import replace

    from cratekit.intake import set_playlist

    return replace(
        written,
        years=tuple(
            replace(one, read_back=set_playlist.read_back(db, one.playlist_id))
            for one in written.years
        ),
    )


def assert_read_back(written: Written) -> None:
    """Refuse an answer the database does not hold: every member of every year read back live."""
    for one in written.years:
        live = set(one.read_back)
        missing = [content for content in one.ids if content not in live]
        if missing:
            raise refuse(
                "session-committed-unverified",
                f"the label playlist {one.name!r} ({one.playlist_id}) read back from "
                f"the database holds {len(one.read_back)} live track(s), "
                f"{len(missing)} of the {len(one.ids)} the plan named not among "
                f"them; the commit landed and this answer cannot be vouched for",
                origin=_ORIGIN,
                detail={
                    "playlist_id": one.playlist_id,
                    "planned": list(one.ids),
                    "read": list(one.read_back),
                    "missing": missing,
                },
            )


def record_commit(record: session.SessionRecord, written: Written, cfg: config.Config) -> None:
    """Name every year playlist filed on the record, and count it under the tree's id (R19).

    ONLY WHEN SOMETHING WAS ADDED OR MADE, the landing's rule for its own tree.
    The year playlists are named by id, label and year, which is what a later
    ``label mark`` of a native batch reads in place of an intake file (R-916).
    """
    if not written.changed():
        return
    record.detail[RECORD_KEY] = [
        {
            "id": one.playlist_id,
            "name": one.name,
            "label": one.label,
            "year": one.year,
            "tracks": len(one.ids),
        }
        for one in written.years
    ]
    changes = (session.TreeChange(tree=written.tree_id, created=written.added()),)
    session.record_commit(record, written.tree_id, session.ChangeSummary(changes), cfg)


def item(written: WrittenYear, *, tree: str, session_id: str) -> dict[str, Any]:
    """The one item a landing appends for each year playlist it filed into."""
    return {
        "action": "playlist",
        "playlist": written.name,
        "id": written.playlist_id,
        "tree": tree,
        "created": written.created,
        "count": len(written.ids),
        "added": written.added,
        "session": session_id,
    }


__all__ = [
    "LABEL",
    "MANIFEST",
    "RECORD_KEY",
    "LabelPlan",
    "Unfiled",
    "Written",
    "WrittenYear",
    "YearPlan",
    "assert_read_back",
    "facts",
    "identity",
    "item",
    "label_of",
    "plan_for_label",
    "plan_for_manifest",
    "read_back",
    "record_commit",
    "supported_only",
    "unfiled_warning",
    "write",
    "year_of",
]
