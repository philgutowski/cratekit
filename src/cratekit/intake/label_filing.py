"""A native landing files its label tracks under the Record Labels tree (U156).

The native medium writes no intake file, so this module files a label batch
under ``Record Labels / <Label> / <Label> <year>`` in the database itself.

AN APPENDED TREE, NOT A CUTOVER. The catalogue tree stays on the xml bridge in
the registry, since a catalogue crawl is not rebuildable (R39). This writer
finds or makes the tree folder, each label folder and each year playlist, and
adds missing memberships; nothing it finds is renamed, moved or removed. It
runs only beside a database native intake tree, when the bridge landing that
writes this tree into an intake file can no longer run.

A label and year come from a manifest's rows (matched by
:func:`cratekit.intake.landing.match_label_rows` over the planned files only),
from ``--label NAME`` with each file's date tag year, or from each file's own
label and date tags (U177). A file with no year or label is named and filed
nowhere, never guessed; it still lands in its INBOX batch.

Names compare under NFC and not case, the bridge's rule (R-453); two siblings
of one name, or a node of the other kind, refuse (R-129). A new node goes last
among its siblings, since inserting one renumbers rows this landing must not
touch. The write is inside the landing's one session and commit, and read back
after it.

The bridge's reasons and match rule are imported where used, since
:mod:`cratekit.intake.landing` imports the native engine that imports this.

Layer: modules.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import match, match_cli
from cratekit.core import cause, config, rb_writer, session, tags, taxonomy
from cratekit.core.cause import Remedy
from cratekit.intake import ingest

if TYPE_CHECKING:  # pragma: no cover - typing only
    from cratekit.intake import landing

#: Where a plan's labels came from, as the gate screen and the record say it.
MANIFEST = "manifest"
LABEL = "label"
#: Each file's own label tag (U177).
TAGS = "tags"

#: The session record field naming every year playlist a commit filed into,
#: read by a later ``label mark`` of a native batch (R-916).
RECORD_KEY = "labels"
#: The session record field mapping each landed content row to its manifest
#: row's provider track (U150), so the account mirror needs no ISRC match.
PROVIDER_KEY = "provider_tracks"

#: A date tag's year: its leading four digits, ``2021`` or ``2021-03-05``.
_YEAR = re.compile(r"^\s*(\d{4})(?!\d)")

_ORIGIN = ("intake.label_filing",)

#: Every refusal here carries this module's origin.
refuse = partial(cause.refuse, origin=_ORIGIN)


def _folded(name: str) -> str:
    """A node name as two sibling names are compared, the bridge writer's rule."""
    return unicodedata.normalize("NFC", name)


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
    #: :data:`MANIFEST`, :data:`LABEL` or :data:`TAGS`.
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
    #: Each filed target and the one provider track its manifest rows name
    #: (U150); a target tied to two tracks is left out, since neither row
    #: decides which it is. Not in the digest: it is written to no table.
    refs: tuple[tuple[str, str], ...] = ()

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
    """The declared catalogue tree, refused by name when there is none or it is not appendable."""
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
        )
    # APPENDED ONLY BESIDE A NATIVE INTAKE TREE: on the bridge an intake file
    # import would land over what this appended, so reaching here is a defect.
    if declared is None or not medium.native:
        raise refuse(
            "internal-error",
            f"the intake tree {declared.intake.id!r} is on the xml bridge, so its "
            f"landing files labels into the intake file it writes and the "
            f"{node.display!r} tree is not appended to natively; nothing was moved",
            remedy=Remedy.REPORT_DEFECT,
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

    A smart playlist is neither, since the binding refuses a membership in one
    only at the write, after the files have moved.
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
                detail={"name": name, "row": str(row.ID)},
            )
    if len(named) > 1:
        raise refuse(
            "intake-list-unusable",
            f"{len(named)} {kind}s named {name!r} sit side by side {where}, so the "
            f"label filing has no one {kind} to add to; merge or rename them in "
            f"rekordbox, nothing was moved",
            detail={"name": name, "rows": [str(row.ID) for row in named]},
        )
    return str(named[0].ID) if named else ""


def _resolve(
    db: Any, node: taxonomy.Node, filed: Mapping[str, Mapping[int, Sequence[str]]]
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
                _live_children(db, tree_folder), label, folder=True, where=f"under {node.display!r}"
            )
            if tree_folder
            else ""
        )
        folders.append((label, folder))
        held = _live_children(db, folder) if folder else []
        for year in sorted(filed[label], reverse=True):
            name = f"{label} {year}"
            playlist = _sole(held, name, folder=False, where=f"under {label!r}") if folder else ""
            years.append(
                YearPlan(
                    label=label,
                    year=year,
                    playlist_id=playlist,
                    targets=tuple(dict.fromkeys(filed[label][year])),
                )
            )
    return tree_folder, tuple(folders), tuple(years)


def _planned(
    db: Any,
    node: taxonomy.Node,
    filed: Mapping[str, Mapping[int, Sequence[str]]],
    unfiled: Sequence[Unfiled],
    **given: Any,
) -> LabelPlan:
    """The plan over ``filed`` as the database holds its nodes now, ``given`` naming its source."""
    tree_folder, folders, years = _resolve(db, node, filed)
    return LabelPlan(
        tree_id=node.id,
        tree_display=node.display,
        tree_folder=tree_folder,
        folders=folders,
        years=years,
        unfiled=tuple(unfiled),
        **{"label": "", "manifest": "", "manifest_digest": "", **given},
    )


def _unwritten(target: str, because: str) -> Unfiled:
    """A planned file filed under no label after all, and why."""
    from cratekit.intake import landing

    return Unfiled(
        target=target,
        reason=landing.NOT_WRITTEN,
        sentence=f"{Path(target).name} was filed under no label playlist, because {because}",
    )


#: The first year a release can carry: below it (``0000``) is a placeholder, and
#: a year after next is a typing slip.
FIRST_YEAR = 1900


def _read_year(path: Path) -> tuple[int | None, str]:
    """The year a file's date tag names, or why not, an unreadable tag apart (pattern 1)."""
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
    db: Any, medium: ingest.IntakeMedium, *, label: str, files: Sequence[tuple[Path, Path]]
) -> LabelPlan:
    """Every file under ``label`` in its date tag's year; one with none is named."""
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
    return _planned(db, node, filed, unfiled, source=LABEL, label=name)


def _read_label(path: Path) -> tuple[str, str]:
    """The label a file's own label tag names, NFC and stripped, or empty and why (pattern 1)."""
    try:
        stored = tags.read_tags_checked(path, ("label",))["label"]
    except tags.TagReadFailed as exc:
        return "", f"its tags could not be read ({exc})"
    named = _folded(str(stored or "").strip())
    if not named:
        return "", "it carries no label tag"
    return named, ""


def plan_for_tags(
    db: Any, medium: ingest.IntakeMedium, *, files: Sequence[tuple[Path, Path]]
) -> LabelPlan:
    """Every file under the label its own label tag names, in its date tag's year (U177).

    A file with no label tag is named as filed nowhere, so one batch of several
    sellers files no file under another's label.
    """
    from cratekit.intake import landing

    node = _catalog_node(medium)
    filed: dict[str, dict[int, list[str]]] = {}
    unfiled: list[Unfiled] = []
    for source, target in files:
        label, why = _read_label(source)
        year: int | None = None
        if label:
            year, why = _read_year(source)
        if not label or year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no "
                        + (f"{label} year playlist" if label else "label playlist")
                        + f", because {why}; it is in the intake playlist"
                    ),
                )
            )
            continue
        filed.setdefault(label, {}).setdefault(year, []).append(str(target))
    return _planned(db, node, filed, unfiled, source=TAGS)


def plan_for_manifest(
    cfg: config.Config,
    db: Any,
    medium: ingest.IntakeMedium,
    *,
    manifest: landing.LabelManifest,
    files: Sequence[tuple[Path, Path]],
) -> LabelPlan:
    """Every manifest row tied to a planned file by the bridge's rule, on this handle.

    THE INDEX IS OF THE PLANNED FILES ONLY, since staging also holds other
    attempts' files, which this landing does not move.
    """
    from cratekit.intake import landing

    node = _catalog_node(medium)
    sources = [source for source, _target in files]
    index = match.index_paths(sources, template=match_cli.library_template(cfg))
    ids = {source.resolve(): str(target) for source, target in files}
    matched, unmatched = landing.match_label_rows(manifest.rows, index, ids)
    # ONE LABEL UNDER ITS FOLDED NAME, never two siblings that fold to one.
    filed: dict[str, dict[int, list[str]]] = {}
    for label, by_year in matched.items():
        for year, rows in by_year.items():
            filed.setdefault(_folded(label), {}).setdefault(year, []).extend(
                target for _row, targets in rows for target in targets
            )
    return _planned(
        db,
        node,
        filed,
        [Unfiled(target="", reason=one.reason, sentence=one.sentence) for one in unmatched],
        source=MANIFEST,
        manifest=str(manifest.path),
        manifest_digest=manifest.digest,
        refs=_refs(matched),
    )


def _refs(matched: Mapping[str, Mapping[int, Sequence[tuple[Any, Sequence[str]]]]]) -> tuple[tuple[str, str], ...]:
    """Each target and the one provider track the rows tied to it name, ordered by target."""
    named: dict[str, set[str]] = {}
    for by_year in matched.values():
        for rows in by_year.values():
            for row, targets in rows:
                # A ROW WITH NO ID NAMES NO TRACK, so it makes no claim on a file.
                ref = str(getattr(row, "ref", "") or "").strip()
                if not ref:
                    continue
                for target in targets:
                    named.setdefault(target, set()).add(ref)
    return tuple(
        (target, next(iter(refs))) for target, refs in sorted(named.items()) if len(refs) == 1
    )


def _restated(
    unfiled: Sequence[Unfiled], held: Mapping[str, object] | set[str], because: str
) -> tuple[Unfiled, ...]:
    """Every unfiled file whose file will not reach INBOX said so, in place of the plan's words.

    The plan says a file with no year is in the intake playlist, false of one
    left in staging or refused at the move. A row with no target keeps its words.
    """
    from cratekit.intake import landing

    return tuple(
        one
        if not one.target or one.target in held or one.reason == landing.NOT_WRITTEN
        else _unwritten(one.target, because)
        for one in unfiled
    )


def supported_only(plan: LabelPlan, kept: set[str]) -> LabelPlan:
    """The plan without the targets the landing will leave in staging, each named as unfiled.

    ``kept`` is every target the landing makes or finds a row for; a file of a
    suffix the database has no type for stays in staging, and no row answers it.
    """
    left: list[Unfiled] = []
    years: list[YearPlan] = []
    for one in plan.years:
        held = tuple(target for target in one.targets if target in kept)
        left.extend(
            _unwritten(target, "its file stays in staging")
            for target in one.targets
            if target not in kept
        )
        if held:
            years.append(replace(one, targets=held))
    restated = _restated(plan.unfiled, kept, "its file stays in staging")
    if not left and restated == plan.unfiled:
        return plan
    labels = {one.label for one in years}
    return replace(
        plan,
        folders=tuple(one for one in plan.folders if one[0] in labels),
        years=tuple(years),
        unfiled=(*restated, *left),
        refs=tuple(one for one in plan.refs if one[0] in kept),
    )


def label_of(plan: LabelPlan) -> dict[str, str]:
    """Each filed target and every playlist it goes in, which can be two years, for the gate."""
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
    said = {
        MANIFEST: f"the manifest {plan.manifest}",
        TAGS: "each file's own label tag, its year from its date tag",
    }.get(plan.source, f"--label {plan.label}, each file's year from its date tag")
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
    made = [label for label, folder in plan.folders if not folder]
    if made:
        # Named: a folder made beside one of another case (R-453) shows only here.
        shown["label folders made"] = made
    if plan.unfiled:
        shown["filed under no label"] = [one.sentence for one in plan.unfiled]
    return shown


def unfiled_warning(left: Sequence[Unfiled]) -> list[dict[str, str]]:
    """One warning per file or row filed under no label, in the words the screen showed."""
    return [{"code": one.reason, "message": one.sentence} for one in left]


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
    #: Each landed content row and its provider track, from the plan's
    #: ``refs`` through the rows the landing made or found (U150).
    provider: tuple[tuple[str, str], ...] = ()

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
            detail={"row": row_id},
        )
    return row


def write(db: Any, plan: LabelPlan, *, by_target: Mapping[str, str]) -> Written:
    """Find or make every planned node and add every member, pending on ``db``.

    Inside the landing's session, which commits or rolls back. ``by_target``
    maps targets to the rows made or found; a member with no row is left and
    named. No empty node is made, and ``add_memberships`` removes nothing.
    """
    left: list[Unfiled] = []
    wanted: list[tuple[YearPlan, tuple[str, ...]]] = []
    for one in plan.years:
        ids: list[str] = []
        for target in one.targets:
            held = by_target.get(target, "")
            if held:
                ids.append(held)
            else:
                left.append(_unwritten(target, "its file did not land"))
        if ids:
            wanted.append((one, tuple(dict.fromkeys(ids))))
    provider = tuple(
        (by_target[target], ref) for target, ref in plan.refs if by_target.get(target, "")
    )
    left = [*_restated(plan.unfiled, by_target, "its file did not land"), *left]
    nothing = Written(plan.tree_id, plan.tree_folder, False, (), (), tuple(left), provider)
    if not wanted:
        return nothing
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
            WrittenYear(one.label, one.year, str(playlist.ID), created, ids, added=len(added))
        )
    return replace(
        nothing,
        tree_folder=str(tree.ID),
        tree_created=tree_created,
        folders_created=tuple(made),
        years=tuple(written),
    )


def read_back(db: Any, written: Written) -> Written:
    """The same answer with every year playlist's live members read from SQL."""
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
                detail={
                    "playlist_id": one.playlist_id,
                    "planned": list(one.ids),
                    "read": list(one.read_back),
                    "missing": missing,
                },
            )


def record_commit(record: session.SessionRecord, written: Written, cfg: config.Config) -> None:
    """Name every year playlist filed on the record, and count it under the tree's id (R19).

    Only when something was added or made. A later ``label mark`` of a native
    batch reads the entries in place of an intake file (R-916).
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


def years_filed(record: session.SessionRecord, label: str) -> frozenset[str] | None:
    """The years one native landing's record says it filed a track under ``label``.

    What ``label mark --pass`` reads in place of an intake file (R-1056). A
    year counts only when its entry held a track, the bridge's rule, and the
    label compares under the landing's fold. A record that filed nothing
    answers empty; ``None`` is a key this build cannot read, which a caller
    must not take for nothing filed.
    """
    filed = record.detail.get(RECORD_KEY, [])
    if not isinstance(filed, list):
        return None
    wanted = _folded(label)
    years: set[str] = set()
    for entry in filed:
        if not isinstance(entry, dict):
            return None
        named, year, tracks = entry.get("label"), entry.get("year"), entry.get("tracks")
        if (
            not isinstance(named, str)
            or not isinstance(year, int)
            or isinstance(year, bool)
            or not isinstance(tracks, int)
            or isinstance(tracks, bool)
        ):
            return None
        if _folded(named) == wanted and tracks > 0:
            years.add(f"{year:04d}")
    return frozenset(years)


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
