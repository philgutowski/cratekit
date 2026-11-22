"""The tree writers: one implementation per write, in either medium (U18).

Everything a workflow does to a tree (a named subtree of the playlist
hierarchy) comes through here, by the XML bridge (a spliced export the user
re-imports) or the database (membership rows written directly); which medium is
correct is the registry's answer. One implementation replaces the source's five
splicers, which disagreed where it mattered; nine goldens pin the bytes.

This module locates and splices nothing: ``rbxml`` does, so its guard covers
every byte write, and every call here names the tree it targets. No display
name is spelled here (R19). The database half calls the session spine
(:func:`cratekit.core.session.assert_gates`, a capture
:func:`cratekit.core.snapshot.assert_verified` passed) and NAMES the analysis
roots it could touch, or the watch (R17's fifth surface) watches nothing.

Under U9's A2 verdict an XML import replaces unconditionally, so a tree that has
taken a database-native write is permanently unsafe to XML import; the bridge
guard stops the next sweep walking through that door.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.core import (
    cause,
    config,
    convergence,
    locations,
    rb_writer,
    session,
    snapshot,
    taxonomy,
    tree_registry,
)
from cratekit.core.exit_codes import Remedy
from cratekit.write import rbxml

logger = logging.getLogger(__name__)

#: The vocal sub-playlist's stable identifier, never its display name, so a
#: user who renames the playlist keeps every track already in it.
VOX_SUB_CLASS = "with_vox"

#: The workflow name the database membership writer records in the session log.
#: A name for an operation, not a verb: the CLI layer owns verb names (D2).
MEMBERSHIP_WORKFLOW = "tree-membership"

#: The workflow name the membership move records, so a session that removed
#: something is told apart from one that only added.
MOVE_WORKFLOW = "tree-membership-move"


# ---------------------------------------------------------------------------
# What a write did, reported rather than printed
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RouteReport:
    """What one sweep over the bridge changed, and what it could not.

    A report, because one absent folder is a fact to carry to the end rather
    than a reason to abandon the other writes, and only the CLI prints.
    """

    inserted: int = 0
    created: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class VoxReport:
    """What the vocal sweep changed, and every folder it could not serve.

    ``warnings`` keeps "could not write it" apart from "already had it".
    Iterable over ``modified``, so a caller that wants only the names reads it
    as the plain list it used to be.
    """

    modified: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __iter__(self):
        return iter(self.modified)

    def __len__(self) -> int:
        return len(self.modified)

    def __eq__(self, other: object) -> bool:
        """Equal to the plain name list as well as to another report.

        The goldens compare this against a list of display names, which is the
        whole contract a caller depends on.
        """
        if isinstance(other, VoxReport):
            return (self.modified, self.warnings) == (other.modified, other.warnings)
        if isinstance(other, (list, tuple)):
            return list(self.modified) == list(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.modified, self.warnings))


class MatchOutcome(str, Enum):
    """Why one requested file did or did not reach a single content row.

    Four answers, because three are different problems with different fixes,
    and fusing them reports a configuration error as a missing file.
    """

    MATCHED = "matched"
    AMBIGUOUS = "ambiguous"
    ABSENT = "absent"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class RowMatch:
    """One requested file and the active row it resolved to, or why it did not.

    ``content_ids`` is set only for ``AMBIGUOUS``, with every active row that
    claimed the location, so the user sees both.
    """

    requested: str
    outcome: MatchOutcome
    content_id: str | None = None
    content_ids: tuple[str, ...] = ()
    resolution: locations.Resolution | None = None


@dataclass(frozen=True)
class ContentRow:
    """The three columns row matching reads, as a value, so matching is pure.

    ``deleted`` is rekordbox's soft-delete marker: a row carrying it is a
    tombstone, not a track.
    """

    content_id: str
    recorded: str
    #: No default: False would mean "active", so a producer that forgot the
    #: marker would hand every tombstone to the matcher as a live row.
    deleted: bool


def soft_delete_marker(row: Any) -> bool:
    """Read rekordbox's soft-delete marker off one mapped row, or REFUSE.

    The one implementation of the rule ``ContentRow.deleted`` states, for the
    routing pass (rows alive) and the deletion pass (rows not). A row that
    cannot report it refuses, ``None`` included, since a permissive default
    would place a removed track or hide a removal. The read is
    :func:`cratekit.core.rb_writer.soft_deleted` since R-758; this keeps the
    words a collection row is refused in.
    """
    return rb_writer.soft_deleted(
        row,
        message=(
            f"the collection row {getattr(row, 'ID', '?')!r} cannot say whether "
            f"it is a tombstone, and treating that as 'not deleted' would place a "
            f"track somebody removed from their library on purpose, or hide a "
            f"removal from the pass that acts on removals"
        ),
        origin=("trees",),
        detail={"content_id": str(getattr(row, "ID", ""))},
    )


@dataclass(frozen=True)
class MembershipReport:
    """What one database membership session wrote, and what it skipped.

    ``skipped`` is every :class:`RowMatch` that did not reach exactly one active
    row, surfaced rather than raised: one unresolvable file does not abandon
    the session, and a silent skip hides it.
    """

    tree_id: str
    root_id: str
    added: int = 0
    already_present: int = 0
    skipped: tuple[RowMatch, ...] = ()
    playlists: tuple[str, ...] = field(default=())


class TreeUnreachable(ValueError):
    """The tree a sweep was pointed at is not there, or is not a folder.

    Raised rather than reported as an empty walk, which would read as success
    over a document the sweep never touched.
    """

    def __init__(self, tree_display: str, reason: str) -> None:
        self.tree_display = tree_display
        self.reason = reason
        super().__init__(f"the tree {tree_display!r} cannot be written: {reason}")


class DuplicateFolders(ValueError):
    """Two folders in one tree carry one display name.

    Refused rather than half served: a writer targets a folder by name, so with
    two it reaches the first twice and the second never.
    """

    def __init__(self, tree_display: str, duplicated: Sequence[str]) -> None:
        self.tree_display = tree_display
        self.duplicated = tuple(duplicated)
        super().__init__(
            f"the tree {tree_display!r} holds more than one folder named "
            f"{', '.join(repr(name) for name in self.duplicated)}; a writer that "
            f"targets a folder by name cannot tell them apart, so it would write "
            f"to the first one twice and to the second one never"
        )


# ---------------------------------------------------------------------------
# The bridge half: routing, ratings, vocal subs, and the catalog subtree
# ---------------------------------------------------------------------------


def _route(
    plan: Mapping[tuple[str, str], Sequence[object]],
    content: bytearray,
    *,
    tree: rbxml.Tree | None,
    norm_by_tid: dict | None,
    create_missing: bool,
) -> RouteReport:
    """One routing sweep, the one body both entry points below use.

    The source carried two copies that drifted (a bare LF, a missing dedupe).
    """
    if rbxml.playlists_start(content) == -1:
        return RouteReport(warnings=(f"{rbxml.PLAYLISTS_SECTION} section not found",))

    inserted = 0
    created: list[str] = []
    warnings: list[str] = []
    # Sorted, so the bytes depend on the plan's content, not its dict order.
    for (folder_display, sub_display), track_ids in sorted(plan.items()):
        ids = list(track_ids)
        if not ids:
            continue
        result = rbxml.splice_into_subplaylist(
            content, folder_display, sub_display, ids,
            tree=tree, norm_by_tid=norm_by_tid, create_missing=create_missing,
        )
        if result.warning:
            warnings.append(result.warning)
            continue
        inserted += result.inserted
        if result.created:
            created.append(f"{folder_display}/{sub_display}")
    return RouteReport(inserted=inserted, created=tuple(created), warnings=tuple(warnings))


def apply_playlist_changes(
    plan: Mapping[tuple[str, str], Sequence[object]],
    content: bytearray,
    *,
    tree: rbxml.Tree | None = None,
    norm_by_tid: dict | None = None,
) -> RouteReport:
    """Route tracks into sub-playlists that already exist.

    An absent sub is a warning, not a creation: this tree's shape is curated by
    a person, so a missing sub is a fact about the plan.
    """
    return _route(plan, content, tree=tree, norm_by_tid=norm_by_tid, create_missing=False)


def apply_unplaced_changes(
    plan: Mapping[tuple[str, str], Sequence[object]],
    content: bytearray,
    *,
    tree: rbxml.Tree | None = None,
    norm_by_tid: dict | None = None,
) -> RouteReport:
    """Route tracks that are in no sub-playlist yet, creating the sub when absent.

    This sweep exists to leave nothing unplaced, so a bucket with no playlist
    yet is the ordinary case.
    """
    return _route(plan, content, tree=tree, norm_by_tid=norm_by_tid, create_missing=True)


def apply_rating_changes(rating_plan: Mapping[object, object], content: bytearray) -> int:
    """Patch star ratings on collection tracks. Returns how many changed.

    One writer where the source had two; both goldens pin it. No tree is named:
    a rating is an attribute of a track, so no guard is keyed on one.
    """
    return rbxml.apply_rating_changes(dict(rating_plan), content)


def root_playlist_members(content: bytes, name: str) -> tuple[str, ...] | str:
    """The track keys a playlist directly under the playlist root holds.

    Empty when no such playlist exists yet. A warning string when the root has
    no playlist tree, or a FOLDER of that name stands there, since the writer
    would refuse that node. Only the direct child the writer replaces is read.
    """
    root = rbxml.root_node(content)
    if root is None:
        return "ROOT node not found"
    node = rbxml.direct_child(content, root, name, rbxml.PLAYLIST_TYPE)
    if isinstance(node, str):
        return node
    return () if node is None else rbxml.track_keys(content, node)


def add_to_root_playlist(
    name: str, track_ids: Sequence[str], content: bytearray
) -> tuple[int, str | None]:
    """Add tracks to a root playlist, creating it, and never remove one.

    Returns how many tracks the playlist gained and a warning or None.
    :func:`cratekit.write.rbxml.insert_root_playlist` REPLACES the playlist, so
    the members it holds are written back ahead of the new ones. Nothing new is
    nothing written, so a rerun leaves the bytes alone. No tree: the playlist
    root is not one.
    """
    existing = root_playlist_members(content, name)
    if isinstance(existing, str):
        return 0, existing
    held = set(existing)
    new: list[str] = []
    for track_id in track_ids:
        key = str(track_id)
        if key not in held:
            held.add(key)
            new.append(key)
    if not new:
        return 0, None
    warning = rbxml.insert_root_playlist(name, [*existing, *new], content)
    if warning is not None:
        return 0, warning
    return len(new), None


def _tree_folders(content: bytes, tree_display: str) -> tuple[str, ...]:
    """Every folder directly inside a named tree, by display name, in document order.

    Names, not spans, since each write shifts every offset after it; the
    duplicate check makes re-locating by name safe. The tree is found through
    the shared locate, so a PLAYLIST wearing the tree's name refuses rather
    than reading as no tree.
    """
    root = rbxml.root_node(content)
    if root is None:
        raise TreeUnreachable(tree_display, "the document has no playlist ROOT node")
    node = rbxml.direct_child(content, root, tree_display, rbxml.FOLDER_TYPE)
    if isinstance(node, str):
        raise TreeUnreachable(tree_display, node)
    if node is None:
        raise TreeUnreachable(tree_display, "no folder of that name sits under ROOT")
    names = [
        child.name for child in rbxml.child_nodes(content, node) if child.node_type == rbxml.FOLDER_TYPE
    ]
    duplicated = sorted({name for name in names if names.count(name) > 1})
    if duplicated:
        raise DuplicateFolders(tree_display, duplicated)
    return tuple(names)


def _governed_or_named(
    tree: rbxml.Tree | None,
    registry: tree_registry.Registry | None,
    node: taxonomy.Node,
    *,
    what: str,
) -> rbxml.Tree:
    """The tree a bridge write targets: governed by the registry, or named outright.

    No ungoverned default: the emitter guard does nothing for an ungoverned
    tree, so defaulting one for a node the registry governs would splice an
    export for a tree the database owns. A caller with no records passes
    :data:`cratekit.core.tree_registry.EMPTY`; one writing a playlist this
    product does not govern passes ``rbxml.Tree(display=...)`` itself.
    """
    if tree is not None:
        return tree
    if registry is None:
        raise ValueError(
            f"{what} targets a tree the registry governs, so it needs either the "
            f"registry or an explicit tree. Pass registry=tree_registry.read(cfg), "
            f"or tree_registry.EMPTY when nothing is recorded yet. Passing neither "
            f"would build an ungoverned tree, and the bridge guard does not apply "
            f"to one, so a splice into a tree the database already owns would be "
            f"refused by nothing"
        )
    return rbxml.tree_for(node, registry)


def add_vox_playlists(
    raw: bytes,
    declared: taxonomy.Taxonomy,
    *,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
    sub_class_id: str = VOX_SUB_CLASS,
) -> tuple[bytes, VoxReport]:
    """Give every folder in a tree the vocal sub-playlist, and report which gained one.

    rekordbox's import cannot create an empty playlist and a splice needs one
    to exist, so vocal routing has somewhere to write only because this ran.
    Idempotent: a folder already holding it is left byte-identical. Both names
    come from the declared taxonomy, the library's active template (R-685).
    Every warning is carried out in the report.
    """
    sub_display = declared.sub_class(sub_class_id).display
    target = _governed_or_named(tree, registry, declared.tree, what="the vocal sweep")

    content = bytearray(raw)
    modified: list[str] = []
    warnings: list[str] = []
    for folder_display in _tree_folders(content, target.display):
        result = rbxml.insert_empty_subplaylist(content, folder_display, sub_display, tree=target)
        if result.warning:
            warnings.append(result.warning)
            continue
        if result.created:
            modified.append(folder_display)
    return bytes(content), VoxReport(modified=tuple(modified), warnings=tuple(warnings))


def _catalog_playlists(
    label: str, buckets: Mapping[int, Sequence[Mapping[str, Any]]]
) -> list[tuple[str, list[object]]]:
    """One playlist per year, newest first, with that year's ids deduplicated.

    Deduplicated across the year, not per album: a track on a single and a
    compilation is one track.
    """
    out: list[tuple[str, list[object]]] = []
    for year in sorted(buckets, reverse=True):
        ids = rbxml.dedupe_track_ids(
            track_id for album in buckets[year] for track_id in album["track_ids"]
        )
        out.append((f"{label} {year}", ids))
    return out


def _catalog_tree(
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry | None,
    tree: rbxml.Tree | None,
) -> rbxml.Tree:
    """The tree a catalogued source is written into, or a refusal by name."""
    if tree is not None:
        return tree
    if declared.catalog is None:
        raise cause.refuse(
            "catalog-tree-undeclared",
            "this library's taxonomy declares no catalog tree, so there is "
            "nothing to write a catalogued source into; the tree a catalog "
            "import lands in is declared alongside the routing tree and the "
            "intake flow, and this writer will not fabricate one",
            remedy=Remedy.FIX_CONFIG_VALUES,
            scope=cause.Scope.RUN,
        )
    return _governed_or_named(None, registry, declared.catalog, what="the catalog import")


def _insert_catalog(
    content: bytearray,
    label: str,
    playlists: Sequence[tuple[str, Sequence[object]]],
    tree: rbxml.Tree,
) -> None:
    warning = rbxml.insert_catalog_folder(content, label, playlists, tree=tree)
    if warning is not None:
        # Nothing is written on a refusal, the output file included, since a
        # caller finding an output document would reasonably import it.
        raise cause.refuse(
            "internal-error",
            f"the catalogued source {label!r} could not be written: {warning}",
            scope=cause.Scope.RUN,
        )


def check_record_labels_tree(
    raw: bytes,
    catalog: Mapping[str, Iterable[int]],
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
) -> None:
    """Every refusal :func:`insert_record_labels_tree` can make, and no write.

    ``catalog`` is each source name and the years it would be written under.
    The landing moves files out of staging before it writes the tree, so it
    asks first; the same resolution and byte writer run over a copy. Each year
    gets one id no document holds, not an empty list, since the writer returns
    early from a held playlist with nothing to add, before the refusals about
    its layout. An empty ``catalog`` asks nothing, the undeclared tree included.
    """
    if not catalog:
        return
    target = _catalog_tree(declared, registry, tree)
    trial = bytearray(raw)
    for label in sorted(catalog, reverse=True):
        years = sorted(set(catalog[label]), reverse=True)
        _insert_catalog(
            trial, label, [(f"{label} {year}", [_TRIAL_ID]) for year in years], target
        )


#: A track key no rekordbox document carries, since its keys are positive.
_TRIAL_ID = -1


def insert_record_labels_trees(
    xml_path: Path | str,
    catalog: Mapping[str, Mapping[int, Sequence[Mapping[str, Any]]]],
    out_path: Path | str,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
) -> Path:
    """Write every catalogued source in ``catalog`` in ONE read and ONE write.

    :func:`insert_record_labels_tree` for several sources, since the document
    is a whole collection. All or nothing: one refusal leaves the output
    untouched. Last name first, because a new folder goes in at the top, so a
    new tree reads A to Z; a folder already held stays where it is.
    """
    target = _catalog_tree(declared, registry, tree)
    content = bytearray(Path(xml_path).read_bytes())
    for label in sorted(catalog, reverse=True):
        _insert_catalog(content, label, _catalog_playlists(label, catalog[label]), target)
    destination = Path(out_path)
    # Atomically: a partial document is a file the user is told to import.
    config.atomic_write_bytes(bytes(content), destination)
    return destination


def insert_record_labels_tree(
    xml_path: Path | str,
    label: str,
    buckets: Mapping[int, Sequence[Mapping[str, Any]]],
    out_path: Path | str,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
) -> Path:
    """Write one catalogued source's whole subtree into a copy of an export.

    Never in place: the export is a file the user still has to import. The
    catalog tree is CREATED when the document has none, the one place a tree
    comes into existence here, and a taxonomy that declares none refuses by
    name. A source whose folder is already held is merged into, by
    :func:`rbxml.insert_catalog_folder`'s rule, and two folders of its name
    refuse (R-129).
    """
    return insert_record_labels_trees(
        xml_path, {label: buckets}, out_path, declared=declared, registry=registry, tree=tree
    )


# ---------------------------------------------------------------------------
# The database half: membership for rows that already exist
# ---------------------------------------------------------------------------


def located(
    recorded: str, *, root: Path | str, prefix_map: Sequence[locations.PrefixRule]
) -> tuple[str, locations.ResolvedPath]:
    """One recorded path, decoded ONCE, with how it resolves on this machine.

    Public since R-500, so ``write/naming_cli`` holds no copy of these calls.
    The decoded path comes back beside the resolution so no caller decodes twice.
    """
    decoded = locations.location_to_path(str(recorded))
    return decoded, locations.resolve_recorded_path(decoded, root=root, prefix_map=prefix_map)


def _comparable(recorded: str, *, root: Path | str, prefix_map: Sequence[locations.PrefixRule]):
    """One recorded path, decoded and resolved into the form both sides compare in.

    Both sides go through this: one side normalized and the other not is how
    144 files with accented names went missing.
    """
    return located(recorded, root=root, prefix_map=prefix_map)[1]


def index_active_rows(
    rows: Iterable[ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> dict[str, tuple[str, ...]]:
    """Every ACTIVE row, grouped by the location it resolves to.

    Soft-deleted rows are dropped first, so a tombstone beside the live row for
    one file is not a collision. Separate from matching so a sweep walks the
    library once: rows that are a cursor would be exhausted by the first entry.
    """
    by_location: dict[str, list[str]] = {}
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
        if resolved.path is None:
            continue
        by_location.setdefault(resolved.path, []).append(row.content_id)
    return {location: tuple(ids) for location, ids in by_location.items()}


def match_active_rows(
    requested: Iterable[Path | str],
    rows: Iterable[ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> tuple[RowMatch, ...]:
    """Resolve each requested file to the ONE active row that holds it.

    Two active rows on one location are skipped and surfaced, never both
    written, or one track sits in a playlist twice under two identities.
    Several matches against one library build the index once with
    :func:`index_active_rows` and use :func:`match_indexed_rows`.
    """
    index = index_active_rows(rows, root=root, prefix_map=prefix_map)
    return match_indexed_rows(requested, index, root=root, prefix_map=prefix_map)


def _match(
    text: str,
    index: Mapping[str, Sequence[str]],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
) -> RowMatch:
    resolved = _comparable(text, root=root, prefix_map=prefix_map)
    if resolved.path is None:
        return RowMatch(text, MatchOutcome.UNRESOLVED, resolution=resolved.resolution)
    candidates = tuple(index.get(resolved.path, ()))
    if not candidates:
        return RowMatch(text, MatchOutcome.ABSENT, resolution=resolved.resolution)
    if len(candidates) > 1:
        return RowMatch(
            text, MatchOutcome.AMBIGUOUS, content_ids=candidates, resolution=resolved.resolution
        )
    return RowMatch(
        text, MatchOutcome.MATCHED, content_id=candidates[0], resolution=resolved.resolution
    )


def match_indexed_rows(
    requested: Iterable[Path | str],
    index: Mapping[str, Sequence[str]],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> tuple[RowMatch, ...]:
    """Match against an index already built, so a sweep walks the library once."""
    return tuple(_match(str(entry), index, root=root, prefix_map=prefix_map) for entry in requested)


def _root_row(db: Any, root_id: str) -> Any:
    """The playlist row the cutover adopted, or a refusal naming it.

    Refused rather than defaulted: writing unparented would put the tree beside
    itself. No ``.first()``: ``get_playlist(ID=...)`` returns the row or None,
    not a query.
    """
    row = db.get_playlist(ID=str(root_id))
    if row is None:
        raise tree_registry.RegistrySkew(
            f"the adopted root {root_id!r} was reported present and could not be "
            f"read back, so the membership write has nothing to hang the tree's "
            f"folders from and would create them beside the tree instead",
            tree_id="",
            root_id=str(root_id),
        )
    return row


def attached_capture(gates: Any, cfg: config.Config, db: Any):
    """The session record and the verified capture every guarded write opens with.

    Attached before it is judged: a capture that fails its check is still a
    directory a person may look for, and restore lists it.
    """
    record = gates.record
    capture = snapshot.capture(cfg, db=db)
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture


def membership_positions(tables: Any) -> tuple[int, int, int]:
    """Where a membership row holds its playlist, its content row and its removal marker.

    Read off the node tables a writer took before its commit, for the check
    afterwards that every membership it made is one its plan named.
    """
    columns = tables.membership_columns
    playlist, content, marker = ("PlaylistID", "ContentID", rb_writer.SOFT_DELETE_COLUMN)
    return columns.index(playlist), columns.index(content), columns.index(marker)


def rollback_quietly(db: Any) -> None:
    """Undo pending work on the caller's handle. Never masks the original failure."""
    try:
        db.session.rollback()
    except Exception:  # noqa: BLE001 - a failed cleanup must not hide its cause
        logger.warning("could not roll back the pending session after a failed write")


def _undo_unless_landed(
    db: Any, witness: Any, record: session.SessionRecord, tree_id: str, added: int, cfg: config.Config
) -> None:
    """What a membership write does on its way out of a failure, before it re-raises.

    Rolled back, or the pending objects land on whatever commits next under
    its name. An exception is not proof nothing landed: the binding commits and
    then saves its playlist file, so a commit the witness saw is recorded.
    """
    rollback_quietly(db)
    if witness.landed:
        _record_membership_commit(record, tree_id, added, cfg)


def _record_membership_commit(
    record: session.SessionRecord, tree_id: str, added: int, cfg: config.Config
) -> None:
    """Record one tree's commit on its session record, when it added anything.

    A pass that added nothing claims no commit, or restoring past a week of
    no-op sweeps would make a person name each one. Nothing new exists when
    nothing was added. ``created`` is memberships added, the per-tree number
    ``restore list`` asks for.
    """
    if added <= 0:
        return
    session.record_commit(
        record,
        tree_id,
        session.ChangeSummary((session.TreeChange(tree=tree_id, created=added),)),
        cfg,
    )


def _watched(analysis_roots: Iterable[Path | str]) -> list[Path]:
    """The analysis roots a write names, refused when there are none.

    A watch over nothing reports any session clean (R17's fifth surface).
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch "
            "nothing and this session would report itself clean whatever "
            "happened to the library's grids; name the roots this write could "
            "touch (R17's fifth surface, runtime half)"
        )
    return watched


def _writable_root(
    cfg: config.Config,
    db: Any,
    tree_id: str,
    registry: tree_registry.Registry,
    root_exists: Callable[[str], bool],
    purpose: convergence.Purpose,
) -> str:
    """The tree's adopted root, once the medium and the convergence gate pass.

    Both through the shared assertions, and here because every database
    membership write passes through: the convergence gate runs before the
    session opens and refuses a tree a restore left short.
    """
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    convergence.assert_tree_writable(cfg, db, tree_id, registry, purpose=purpose)
    return root_id


@dataclass
class _Run:
    """One membership session's handle, record and counts, read on the way out of a failure."""

    cfg: config.Config
    db: Any
    tree_id: str
    record: session.SessionRecord
    added: int = 0
    already_present: int = 0
    removed: int = 0
    already_absent: int = 0
    touched: list[str] = field(default_factory=list)
    skipped: list[RowMatch] = field(default_factory=list)

    def add(self, playlist: Any, destination: tuple[str, str], ids: list[str]) -> None:
        """One call per playlist: which ids are new is the writer's question (R-10)."""
        self.touched.append("/".join(destination))
        inserted = rb_writer.add_memberships(self.db, playlist, ids)
        self.added += len(inserted)
        self.already_present += len(ids) - len(inserted)

    def undo_unless_landed(self, witness: Any) -> None:
        _undo_unless_landed(self.db, witness, self.record, self.tree_id, self.added, self.cfg)


def _add_planned(
    run: _Run,
    anchor: Any,
    plan: Mapping[tuple[str, str], Sequence[Path | str]],
    index: Mapping[str, Sequence[str]],
    rules: Sequence[locations.PrefixRule],
) -> None:
    """Each plan entry's matched rows into its playlist, every folder under the anchor.

    One lookup per folder: every folder hangs off the one anchor, and one
    ``ensure_folder`` just created is pending on this handle (R-10).
    """
    folders: dict[str, Any] = {}
    for (folder_display, sub_display), requested in sorted(plan.items()):
        matches = match_indexed_rows(requested, index, root=run.cfg.library.root, prefix_map=rules)
        resolved_ids = [
            match.content_id
            for match in matches
            if match.outcome is MatchOutcome.MATCHED and match.content_id
        ]
        run.skipped.extend(match for match in matches if match.outcome is not MatchOutcome.MATCHED)
        if not resolved_ids:
            continue
        if folder_display not in folders:
            folders[folder_display] = rb_writer.ensure_folder(run.db, folder_display, parent=anchor)
        playlist = rb_writer.ensure_playlist(run.db, sub_display, folders[folder_display])
        run.add(playlist, (folder_display, sub_display), resolved_ids)


def write_tree_membership(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    plan: Mapping[tuple[str, str], Sequence[Path | str]],
    rows: Iterable[ContentRow],
    root_exists: Callable[[str], bool],
    analysis_roots: Iterable[Path | str],
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    workflow: str = MEMBERSHIP_WORKFLOW,
    purpose: convergence.Purpose = convergence.Purpose.ROUTINE,
    intent: session.Intent = session.Intent.WRITE,
) -> MembershipReport:
    """Write membership for a database-native tree, for rows that already exist.

    :func:`cratekit.core.tree_registry.anchored_root` refuses a tree on the
    bridge, a record naming no root, and a root this library lacks (a restored
    pre-cutover database). Names match the XML-era names, so a cutover adopts
    rather than duplicates. No content row, tempo or analysis column is written.
    ``analysis_roots`` may not be empty, and the session is this function's own
    (R29), so no outside gates factory can name no roots.

    ``purpose`` lifts only the convergence latches whose remedy is a rebuild
    (:class:`cratekit.core.convergence.Purpose`); ``intent`` is that declaration
    for ``assert_gates``, where U32's latch would refuse the rebuild it names as
    its remedy. ``RECOVERY`` also lifts the unresolved-session latch, so the
    rebuild asserts that one itself (:func:`cratekit.write.rebuild.rebuild_tree`).
    """
    watched = _watched(analysis_roots)
    root_id = _writable_root(cfg, db, tree_id, registry, root_exists, purpose)
    resolved_map = (
        [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
        if prefix_map is None
        else list(prefix_map)
    )
    # ONE walk of the library, before the loop, since rows may be a cursor.
    index = index_active_rows(rows, root=cfg.library.root, prefix_map=resolved_map)

    # The record is opened inside the gates and before the capture (R-12), so
    # no capture goes unnamed by a record: one record per tree, the granularity
    # a person restores at, and R29's one source per run with the tree the source.
    with session.assert_gates(
        cfg, workflow=workflow, analysis_roots=watched, intent=intent, keep=session.Keep.RECORD
    ) as gates, rb_writer.commit_witness(db) as witness:
        record, capture = attached_capture(gates, cfg, db)
        run = _Run(cfg, db, tree_id, record)
        # Parented to the root the cutover adopted, never found globally by
        # name, which would grow the parallel tree the registry exists to prevent.
        anchor = _root_row(db, root_id)
        try:
            _add_planned(run, anchor, plan, index, resolved_map)
            rb_writer.commit_guarded(db)
        except BaseException:
            run.undo_unless_landed(witness)
            raise

        # RECORDED THE INSTANT THE COMMIT RETURNS, ahead of the fingerprint, so a
        # failed state write below cannot close the record looking empty.
        _record_membership_commit(record, tree_id, run.added, cfg)

        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT. It is what
        # lets the next run tell a database recovered out of band from one this
        # product changed itself, and taking it before the commit would record a
        # database this session then moved, so the next run would read its own
        # write as somebody else's restore. It sits outside the try above because
        # by here the commit has landed and there is nothing pending to roll
        # back; a failure now is a state write that failed, not a database write
        # that half happened.
        convergence.record_fingerprint(cfg, db)

    return MembershipReport(
        tree_id=tree_id, root_id=root_id, added=run.added, already_present=run.already_present,
        skipped=tuple(run.skipped), playlists=tuple(run.touched),
    )


# ---------------------------------------------------------------------------
# The move: the one writer that removes a membership (R-758)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MembershipMove:
    """One track, the playlist it belongs in, and the playlists it leaves.

    Display names, each a folder and a playlist under it. ``target`` is named
    whether or not the track is already there, since a removal waits on proof
    that it is.
    """

    content_id: str
    target: tuple[str, str]
    remove: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class MoveReport:
    """What one move session wrote, and what it would not.

    ``skipped``: tracks with no live collection row, untouched. ``held_back``:
    tracks not in their target when the removals began, removed from nothing.
    ``adds_committed``: the first commit landed, so a failure report can say a
    track sits in both places.
    """

    tree_id: str
    root_id: str
    added: int = 0
    already_present: int = 0
    removed: int = 0
    already_absent: int = 0
    skipped: tuple[str, ...] = ()
    held_back: tuple[str, ...] = ()
    playlists: tuple[str, ...] = field(default=())
    adds_committed: bool = False


class MoveInterrupted(Exception):
    """The move stopped after its additions landed and before its removals did.

    Carries the report as far as it got, the failure as ``__cause__``. Every
    track it moved is in its target and may still be where it was leaving: in
    both, never in neither.
    """

    def __init__(self, report: MoveReport) -> None:
        self.report = report
        super().__init__(
            f"the move of tree {report.tree_id!r} added {report.added} "
            f"membership(s) and removed none"
        )


def _live_content(db: Any, content_id: str) -> bool:
    """Whether the collection holds a live row for this identifier."""
    row = db.get_content(ID=str(content_id))
    return row is not None and not soft_delete_marker(row)


def _live_folders(db: Any, anchor: Any, folder_display: str) -> list[Any]:
    """Every live folder of one name directly under the adopted root."""
    anchor_id = str(anchor.ID)
    return [
        folder
        for folder in list(db.get_playlist(Name=folder_display))
        if rb_writer.is_folder(folder)
        and str(getattr(folder, "ParentID", "")) == anchor_id
        and not rb_writer.node_removed(folder)
    ]


def _live_playlists(db: Any, folders: Sequence[Any], sub_display: str) -> list[Any]:
    """Every live playlist of one name under any of these folders."""
    parents = {str(folder.ID) for folder in folders}
    return [
        playlist
        for playlist in list(db.get_playlist(Name=sub_display))
        if not rb_writer.is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in parents
        and not rb_writer.node_removed(playlist)
    ]


class _Destinations:
    """The live playlists answering to each destination, resolved once each.

    Found among LIVE nodes, unlike the additive writer's find or create, which
    can hand back a removed playlist where an addition is invisible and the
    proof of the target fails for ever; what is added to and removed from come
    from one walk. Every node carrying the names counts, as the placement
    reader counts them. A removal never creates.
    """

    def __init__(self, db: Any, anchor: Any) -> None:
        self._db = db
        self._anchor = anchor
        self._found: dict[tuple[str, str], list[Any]] = {}
        self._members: dict[str, set[str]] = {}

    def existing(self, destination: tuple[str, str]) -> list[Any]:
        if destination not in self._found:
            folder_display, sub_display = destination
            folders = _live_folders(self._db, self._anchor, folder_display)
            self._found[destination] = _live_playlists(self._db, folders, sub_display)
        return self._found[destination]

    def for_adding(self, destination: tuple[str, str]) -> Any:
        """The first live playlist for a destination, created when there is none."""
        found = self.existing(destination)
        if found:
            return found[0]
        folder_display, sub_display = destination
        folders = _live_folders(self._db, self._anchor, folder_display)
        folder = (
            folders[0]
            if folders
            else self._db.create_playlist_folder(folder_display, parent=self._anchor)
        )
        playlist = self._db.create_playlist(sub_display, parent=folder)
        self._found[destination] = [playlist]
        return playlist

    def members(self, playlist: Any) -> set[str]:
        """The tracks one playlist holds a live membership for. Read once."""
        key = str(playlist.ID)
        if key not in self._members:
            self._members[key] = {
                str(song.ContentID)
                for song in self._db.get_playlist_songs(PlaylistID=key)
                if not rb_writer.membership_removed(song)
            }
        return self._members[key]

    def holds(self, destination: tuple[str, str], content_id: str) -> bool:
        return any(
            str(content_id) in self.members(playlist) for playlist in self.existing(destination)
        )

    def forget_members(self) -> None:
        """Drop what was read, so the next read is of the database as committed."""
        self._members.clear()


def _add_targets(run: _Run, places: _Destinations, live: Sequence[MembershipMove]) -> None:
    """The additions, every one committed before any removal is attempted."""
    wanted: dict[tuple[str, str], list[str]] = {}
    for move in live:
        wanted.setdefault(move.target, []).append(move.content_id)
    with rb_writer.commit_witness(run.db) as witness:
        try:
            for destination, content_ids in sorted(wanted.items()):
                run.add(places.for_adding(destination), destination, content_ids)
            rb_writer.commit_guarded(run.db)
        except BaseException:
            run.undo_unless_landed(witness)
            raise


def _proven_leavers(
    places: _Destinations, live: Sequence[MembershipMove]
) -> tuple[list[str], dict[tuple[str, str], list[str]]]:
    """The tracks held back, and each destination's leavers, read after the additions.

    A removal is made only for a track proven to sit in its target, whether
    this call added it or found it there, since somebody may have taken it out.
    """
    held_back: list[str] = []
    leaving: dict[tuple[str, str], list[str]] = {}
    for move in live:
        if not places.holds(move.target, move.content_id):
            held_back.append(move.content_id)
            continue
        for destination in move.remove:
            if destination != move.target:
                leaving.setdefault(destination, []).append(move.content_id)
    return held_back, leaving


def _remove_leavers(
    run: _Run,
    places: _Destinations,
    leaving: Mapping[tuple[str, str], list[str]],
    interrupted: Callable[[], MoveReport],
) -> None:
    """The removals, in the second commit, the only one that admits a removal.

    Only an ordinary failure is raised as :class:`MoveInterrupted`: a refusal
    keeps its own type and remedy, and an interrupt or exit is not caught.
    """
    db = run.db
    with rb_writer.commit_witness(db) as witness:
        try:
            for destination, content_ids in sorted(leaving.items()):
                gone: set[str] = set()
                for playlist in places.existing(destination):
                    marked = rb_writer.remove_memberships(db, playlist, content_ids)
                    run.removed += len(marked)
                    gone.update(marked)
                if gone:
                    run.touched.append("/".join(destination))
                run.already_absent += len(set(content_ids) - gone)
            # The membership table alone: since U111 the removable set admits a
            # removed playlist node too, and a membership move removes no node.
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except Exception as exc:
            rollback_quietly(db)
            if witness.landed:
                _record_removal_commit(run.record, run.tree_id, run.removed, run.cfg)
                convergence.record_fingerprint(run.cfg, db)
                raise
            if isinstance(exc, cause.CratekitError):
                raise
            raise MoveInterrupted(interrupted()) from exc
        except BaseException:
            rollback_quietly(db)
            raise


def move_tree_membership(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    moves: Sequence[MembershipMove],
    root_exists: Callable[[str], bool],
    analysis_roots: Iterable[Path | str],
) -> MoveReport:
    """Move tracks between the playlists of one database native tree.

    The first writer that removes a membership, held to everything
    :func:`write_tree_membership` holds, for its reasons. Two commits in one
    session, the additions first, so a failure between them leaves a track in
    both playlists and never in neither, and a resume finishes the rest. The
    fingerprint is taken after each commit that landed. No ``workflow``,
    ``purpose`` or ``intent``: a recovery declaration would lift two latches in
    front of the only writer that removes.
    """
    watched = _watched(analysis_roots)
    root_id = _writable_root(cfg, db, tree_id, registry, root_exists, convergence.Purpose.ROUTINE)

    with session.assert_gates(
        cfg, workflow=MOVE_WORKFLOW, analysis_roots=watched,
        intent=session.Intent.WRITE, keep=session.Keep.RECORD,
    ) as gates:
        record, capture = attached_capture(gates, cfg, db)
        run = _Run(cfg, db, tree_id, record)

        places = _Destinations(db, _root_row(db, root_id))
        live = [move for move in moves if _live_content(db, move.content_id)]
        skipped = tuple(
            sorted({move.content_id for move in moves} - {move.content_id for move in live})
        )
        _add_targets(run, places, live)
        _record_membership_commit(record, tree_id, run.added, cfg)
        if run.added:
            convergence.record_fingerprint(cfg, db)

        def report(**extra: Any) -> MoveReport:
            return MoveReport(
                tree_id=tree_id, root_id=root_id, added=run.added,
                already_present=run.already_present, skipped=skipped,
                playlists=tuple(run.touched), adds_committed=True, **extra,
            )

        places.forget_members()
        held_back, leaving = _proven_leavers(places, live)
        _remove_leavers(run, places, leaving, lambda: report(held_back=tuple(held_back)))
        _record_removal_commit(record, tree_id, run.removed, cfg)
        if run.removed:
            convergence.record_fingerprint(cfg, db)

    return report(removed=run.removed, already_absent=run.already_absent, held_back=tuple(held_back))


def _record_removal_commit(
    record: session.SessionRecord, tree_id: str, removed: int, cfg: config.Config
) -> None:
    """Record the removals on the session record, as rows this session changed.

    ``updated``, never a negative ``created``: the row stays and carries a marker.
    """
    if removed <= 0:
        return
    session.record_commit(
        record,
        tree_id,
        session.ChangeSummary((session.TreeChange(tree=tree_id, updated=removed),)),
        cfg,
    )


__all__ = [
    "MEMBERSHIP_WORKFLOW", "MOVE_WORKFLOW", "VOX_SUB_CLASS", "MembershipMove", "MoveInterrupted",
    "MoveReport", "move_tree_membership", "ContentRow", "DuplicateFolders", "MatchOutcome",
    "MembershipReport", "RouteReport", "RowMatch", "TreeUnreachable", "VoxReport",
    "add_to_root_playlist", "add_vox_playlists", "apply_playlist_changes", "apply_rating_changes",
    "apply_unplaced_changes", "check_record_labels_tree", "index_active_rows",
    "insert_record_labels_tree", "insert_record_labels_trees", "match_active_rows",
    "match_indexed_rows", "membership_positions", "attached_capture", "rollback_quietly",
    "root_playlist_members", "soft_delete_marker", "write_tree_membership",
]
