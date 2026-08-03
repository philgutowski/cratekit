"""The tree writers: one implementation per write, in either medium (U18).

WHAT THIS MODULE IS FOR. A tree is a named subtree of the playlist hierarchy, and
everything a workflow does to one comes through here. Two mediums serve them: the
XML bridge, which splices an export the user re-imports, and the database, which
writes membership rows directly. Which one is correct for a given tree at a given
moment is the registry's answer, not this module's, and asking it is not optional
in either direction.

WHAT IT REPLACES. The system being ported carried FIVE separate splice
implementations across four files, two copies of the rating writer, and a whole
second byte engine for the label subtree. They agreed on most inputs and
disagreed on the ones that mattered: one emitted a bare LF where its siblings
emitted CRLF, one created a sub-playlist without deduplicating while its twin
deduplicated, and one inserted a label folder unconditionally, so a second run
grew a second copy of the whole label. Nine golden files pin the exact bytes all
of them produced, and the collapse into one implementation is checked against
those bytes rather than against a reading of the code.

WHY THE LOCATES AND THE WRITES BOTH LIVE IN ``rbxml`` AND NOT HERE. That module's
claim is that a guard inside the byte writers covers every byte write, and the
claim is false the moment a call site can find a node for itself: a caller that
can locate a node can splice into it without ever calling a writer. So this
module locates nothing and splices nothing. It decides WHAT to write and calls an
emitter, every time, and every call names the tree it targets. A bridge call that
omits the tree is refused by nothing at all, and after a cutover it keeps
splicing an export for a tree the database owns.

WHY NO DISPLAY NAME IS SPELLED HERE. R19 puts every playlist display name in the
declared taxonomy, and the write layer is below the layer allowed to carry one.
So the routing tree, the intake flow, the catalog tree and the vocal sub-playlist
all arrive as declared values, and the identifiers this module does spell
(``VOX_SUB_CLASS``) are stable ids rather than anything a user sees. Renaming a
folder in rekordbox changes what the document says and changes nothing here.

WHAT THE DATABASE HALF OWES THE SESSION SPINE. It does not re-derive the gates,
take its own lock, or invent its own acknowledgment. It calls
:func:`cratekit.core.session.assert_gates`, commits behind a capture that
:func:`cratekit.core.snapshot.assert_verified` passed, and NAMES the analysis
roots it could touch so the runtime half of R17's fifth surface watches
something. That last one is the one that matters: the watch defaults to watching
nothing, so a writer that stays silent about its roots gets a green build and an
unwatched library.

THE U9 VERDICT THIS UNIT PROCEEDS UNDER (A2, recorded 2026-08-01). Neither clean
nor severed. rekordbox's XML playlist import REPLACES unconditionally, so there
is no merge lineage for a database write to sever, and a control playlist the
database never touched was destroyed and replaced anyway. The consequence is a
one-way door and it is why the registry exists: a tree that has taken a
database-native write is permanently unsafe to XML import, and the bridge guard
is what stops the next sweep walking through that door by accident.
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

#: The vocal sub-playlist's STABLE IDENTIFIER, never its display name. The
#: display lives in the declared taxonomy and is read from there, so a user who
#: renames the playlist keeps every track that is already in it.
VOX_SUB_CLASS = "with_vox"

#: The workflow name the database membership writer records in the session log.
#: A name for an operation, not a verb: the CLI layer owns verb names (D2).
MEMBERSHIP_WORKFLOW = "tree-membership"


# ---------------------------------------------------------------------------
# What a write did, reported rather than printed
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RouteReport:
    """What one sweep over the bridge changed, and what it could not.

    A report rather than the stream of prints the source system emitted, because
    this layer has no console: a sweep touches many playlists, one absent folder
    is a fact to carry to the end rather than a reason to abandon the other
    forty writes, and only the CLI decides how any of it is shown.
    """

    inserted: int = 0
    created: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class VoxReport:
    """What the vocal sweep changed, and every folder it could not serve.

    ``modified`` is the list callers read; ``warnings`` is the half that used to
    be thrown away. A folder blocked by a wrong-type collision produced a warning
    the emitter returned and this writer dropped on the floor, so the sweep
    reported the same thing for "already had it" and "could not write it".

    Iterable over ``modified`` so a caller that only wants the names, which is
    every caller the goldens describe, reads the same as it always did.
    """

    modified: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __iter__(self):
        return iter(self.modified)

    def __len__(self) -> int:
        return len(self.modified)

    def __eq__(self, other: object) -> bool:
        """Equal to the plain name list as well as to another report.

        The nine goldens and their sibling tests compare this against a list of
        display names, which is the whole contract a caller depends on. Keeping
        that comparison working is what lets the warnings channel be added
        without rewriting the byte-level tests that pin the output.
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

    Four answers rather than a path-or-None, because three of these are
    different problems with different fixes and fusing them is how a
    configuration error gets reported as a missing file (the split
    :mod:`cratekit.core.locations` already refuses to collapse).
    """

    MATCHED = "matched"
    AMBIGUOUS = "ambiguous"
    ABSENT = "absent"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class RowMatch:
    """One requested file and the active row it resolved to, or why it did not.

    ``content_ids`` is populated only for ``AMBIGUOUS`` and carries every active
    row that claimed the location, because the user has to see both to decide
    which one is the mistake.
    """

    requested: str
    outcome: MatchOutcome
    content_id: str | None = None
    content_ids: tuple[str, ...] = ()
    resolution: locations.Resolution | None = None


@dataclass(frozen=True)
class ContentRow:
    """The three columns row matching reads, and nothing else.

    A value rather than a live mapped object, so the matching below is pure and
    testable with no database at all. ``deleted`` is rekordbox's own soft-delete
    marker: a row carrying it is a tombstone, not a track.
    """

    content_id: str
    recorded: str
    #: NO DEFAULT, deliberately. A default of False means "active", which is the
    #: permissive answer, so a producer that forgot to read the soft-delete
    #: marker would hand every tombstone to the matcher as a live row. The whole
    #: value of the active-row rule is that a removed track cannot claim a
    #: location, and a silent default is how that rule stops being applied.
    deleted: bool


@dataclass(frozen=True)
class MembershipReport:
    """What one database membership session wrote, and what it skipped.

    ``skipped`` carries every :class:`RowMatch` that did not reach exactly one
    active row. They are surfaced rather than raised for the same reason a bridge
    sweep's warnings are: one unresolvable file is not a reason to abandon the
    session, and a silent skip is how a user comes to believe a sweep ran.
    """

    tree_id: str
    root_id: str
    added: int = 0
    already_present: int = 0
    skipped: tuple[RowMatch, ...] = ()
    playlists: tuple[str, ...] = field(default=())


class TreeUnreachable(ValueError):
    """The tree a sweep was pointed at is not there, or is not a folder.

    Raised rather than reported as an empty walk, because the two readings are
    indistinguishable to a caller and only one of them is harmless. A sweep over
    a tree that genuinely holds no folders changed nothing and is correct; a
    sweep that could not find the tree at all changed nothing and is a mistake
    somebody has to fix. Returning the same answer for both is how a run reports
    success over a document it never touched, which is the failure the system
    being ported shipped: its splicers warned and continued, and the user saw a
    green run and an empty playlist.
    """

    def __init__(self, tree_display: str, reason: str) -> None:
        self.tree_display = tree_display
        self.reason = reason
        super().__init__(f"the tree {tree_display!r} cannot be written: {reason}")


class DuplicateFolders(ValueError):
    """Two folders in one tree carry one display name.

    Refused rather than half served. Every writer here targets a folder BY NAME,
    which is what lets a re-run adopt what the last run created, and with two
    candidates a name-targeted write reaches the first one twice and the second
    one never. A caller seeing this has a tree to repair, and doing half the job
    silently would hide that from them until the counts stopped adding up.
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
    """One routing sweep, in the one implementation both public entry points use.

    The two entry points below differ by exactly one flag, and the system being
    ported expressed that difference as two whole copies of the sweep in two
    files. They then drifted: the creating copy emitted a bare LF for the
    existing-sub case its sibling emitted CRLF for, and only one of them
    deduplicated. One body, two names, and the goldens for both still match.
    """
    if rbxml.playlists_start(content) == -1:
        return RouteReport(warnings=(f"{rbxml.PLAYLISTS_SECTION} section not found",))

    inserted = 0
    created: list[str] = []
    warnings: list[str] = []
    # Sorted so a sweep's byte output depends on the plan's CONTENT and not on
    # the order a caller's dict happened to be built in. A golden compares bytes.
    for (folder_display, sub_display), track_ids in sorted(plan.items()):
        ids = list(track_ids)
        if not ids:
            continue
        result = rbxml.splice_into_subplaylist(
            content,
            folder_display,
            sub_display,
            ids,
            tree=tree,
            norm_by_tid=norm_by_tid,
            create_missing=create_missing,
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

    An absent sub is a WARNING here rather than a creation, and that is the
    difference from its sibling below. This sweep runs against a tree whose shape
    a person curated, so a sub that is missing is a fact about the plan (a bucket
    nobody made yet) rather than a licence to invent a playlist in somebody's
    library.
    """
    return _route(
        plan, content, tree=tree, norm_by_tid=norm_by_tid, create_missing=False
    )


def apply_unplaced_changes(
    plan: Mapping[tuple[str, str], Sequence[object]],
    content: bytearray,
    *,
    tree: rbxml.Tree | None = None,
    norm_by_tid: dict | None = None,
) -> RouteReport:
    """Route tracks that are in no sub-playlist yet, creating the sub when absent.

    The creating half. This sweep exists to leave nothing unplaced, so a bucket
    with no playlist yet is the ordinary case rather than a surprise, and
    refusing to create one would leave exactly the tracks it was run for behind.
    """
    return _route(
        plan, content, tree=tree, norm_by_tid=norm_by_tid, create_missing=True
    )


def apply_rating_changes(rating_plan: Mapping[object, object], content: bytearray) -> int:
    """Patch star ratings on collection tracks. Returns how many changed.

    ONE writer where the source had two identical ones in two files, which is why
    two goldens pin it: both are compared against this, and the merge is proven
    to have lost nothing only when both still match.

    No tree is named, and that is not an omission. A rating is an attribute of a
    track, membership of nothing, and it does not change medium when a tree cuts
    over, so there is no tree here for a guard to be keyed on.
    """
    return rbxml.apply_rating_changes(dict(rating_plan), content)


def _tree_folders(content: bytes, tree_display: str) -> tuple[str, ...]:
    """Every folder directly inside a named tree, by display name, in document order.

    Names rather than located spans, deliberately. Each write below shifts every
    offset after it, so a span gathered before the first write is a span that
    describes the document as it no longer is. Re-locating by name on each write
    is what makes the loop correct, and the duplicate check is what makes
    re-locating by name safe.

    The tree itself is found through the shared locate rather than through a
    filter written here. Spelling ``name and type`` as one condition would be a
    second implementation of that locate, and it would lose the answer that
    matters: a PLAYLIST carrying the tree's name is not "no tree", it is a tree
    this write cannot reach, and reporting it as absent means the sweep walks
    zero folders and tells the user it changed nothing.
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
        child.name
        for child in rbxml.child_nodes(content, node)
        if child.node_type == rbxml.FOLDER_TYPE
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

    THE HOLE THIS CLOSES, because it was open and a reviewer walked through it.
    An entry point that defaulted to ``rbxml.Tree(display=node.display)`` built an
    UNGOVERNED tree for a node the registry exists to govern. The emitter guard
    returns on its first line for an ungoverned tree, correctly, because most
    playlists in a real library are somebody's own. So the sweep spliced an export
    for a tree the database already owned, and under U9's A2 verdict importing
    that export replaces the database-native tree outright. The guard did not
    fail; it was never armed, and naming a tree without the registry that governs
    it is naming nothing.

    There is no ungoverned DEFAULT here, and that is the whole point.
    :class:`rbxml.Tree` refuses half a governed tree one layer down for exactly
    this reason, and offering the same hole through a default would be refusing
    it in one place and handing it out in the other. A caller that has genuinely
    loaded no records passes :data:`cratekit.core.tree_registry.EMPTY`, which is a
    sentence somebody can check. A caller writing a playlist this product does
    not govern still passes ``rbxml.Tree(display=...)`` itself, deliberately.
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
    declared: taxonomy.Taxonomy | None = None,
    *,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
    sub_class_id: str = VOX_SUB_CLASS,
) -> tuple[bytes, VoxReport]:
    """Give every folder in a tree the vocal sub-playlist, and report which gained one.

    rekordbox has no import path that creates an EMPTY playlist, and a splice can
    only splice into a playlist that already exists. So the vocal routing that
    follows has somewhere to write only because this ran first. It is the one
    write here that produces a node holding nothing.

    Idempotent by construction: a folder that already carries the playlist is left
    byte-identical, so re-running after a new folder appears touches only the new
    one and the returned list is exactly what changed.

    The declared taxonomy supplies both names. Passing your library's active
    template rather than letting this reach for the shipped default is what makes
    it correct for a user who renamed either one.

    EVERY WARNING IS CARRIED OUT, which is why this returns a report rather than
    the bare name list it used to. A folder the emitter could not serve, because
    a playlist of the vocal name already stands where the folder belongs, is not
    the same fact as a folder that already had the playlist, and both looked
    identical to a caller reading only the list of names that changed.
    """
    active = taxonomy.default_taxonomy() if declared is None else declared
    sub_display = active.sub_class(sub_class_id).display
    target = _governed_or_named(tree, registry, active.tree, what="the vocal sweep")

    content = bytearray(raw)
    modified: list[str] = []
    warnings: list[str] = []
    for folder_display in _tree_folders(content, target.display):
        result = rbxml.insert_empty_subplaylist(
            content, folder_display, sub_display, tree=target
        )
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

    Newest first is the ordering the folder is read in, and the dedup is across
    the whole year rather than per album: a track released on both a single and a
    compilation is one track, and the year's playlist that listed it twice is the
    shape the source system shipped.
    """
    out: list[tuple[str, list[object]]] = []
    for year in sorted(buckets, reverse=True):
        ids = rbxml.dedupe_track_ids(
            track_id for album in buckets[year] for track_id in album["track_ids"]
        )
        out.append((f"{label} {year}", ids))
    return out


def insert_record_labels_tree(
    xml_path: Path | str,
    label: str,
    buckets: Mapping[int, Sequence[Mapping[str, Any]]],
    out_path: Path | str,
    *,
    declared: taxonomy.Taxonomy | None = None,
    registry: tree_registry.Registry | None = None,
    tree: rbxml.Tree | None = None,
) -> Path:
    """Write one catalogued source's whole subtree into a copy of an export.

    Reads one document and writes another, never in place, because the file this
    reads is a fresh export the user still has to import and a partial byte
    splice into this format is not a partial success, it is a corrupt file.

    The catalog tree is CREATED when the document has none, and that is the one
    place here a tree comes into existence rather than being found: nobody's
    setup makes it, the first catalog import does. Which tree that is comes from
    the declared taxonomy, and a taxonomy that declares none refuses by name
    rather than inventing a folder in somebody's library from a default they
    never saw.
    """
    active = taxonomy.default_taxonomy() if declared is None else declared
    if tree is None:
        if active.catalog is None:
            raise cause.refuse(
                "catalog-tree-undeclared",
                "this library's taxonomy declares no catalog tree, so there is "
                "nothing to write a catalogued source into; the tree a catalog "
                "import lands in is declared alongside the routing tree and the "
                "intake flow, and this writer will not fabricate one",
                remedy=Remedy.FIX_CONFIG_VALUES,
                scope=cause.Scope.RUN,
            )
        tree = _governed_or_named(
            None, registry, active.catalog, what="the catalog import"
        )

    content = bytearray(Path(xml_path).read_bytes())
    warning = rbxml.insert_catalog_folder(
        content, label, _catalog_playlists(label, buckets), tree=tree
    )
    if warning is not None:
        # Nothing is written on a refusal, including the output file. A caller
        # that found an output document sitting there would reasonably import it.
        raise cause.refuse(
            "internal-error",
            f"the catalogued source {label!r} could not be written: {warning}",
            scope=cause.Scope.RUN,
        )
    destination = Path(out_path)
    # Atomically, like every other artifact this product persists. A partial
    # document at this path is not a partial success; it is a file the user is
    # told to import into a library that has no second copy.
    config.atomic_write_bytes(bytes(content), destination)
    return destination


# ---------------------------------------------------------------------------
# The database half: membership for rows that already exist
# ---------------------------------------------------------------------------


def _comparable(recorded: str, *, root: Path | str, prefix_map: Sequence[locations.PrefixRule]):
    """One recorded path, decoded and resolved into the form both sides compare in.

    BOTH sides of every comparison go through this, which is the whole rule the
    identity primitives exist to enforce: one side normalized and the other not
    is how 144 files with accented names went missing, and the two sides here are
    a path this machine can see and a path rekordbox wrote down years ago.
    """
    return locations.resolve_recorded_path(
        locations.location_to_path(str(recorded)), root=root, prefix_map=prefix_map
    )


def index_active_rows(
    rows: Iterable[ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> dict[str, tuple[str, ...]]:
    """Every ACTIVE row, grouped by the location it resolves to.

    THE ACTIVE-ROW RULE. rekordbox soft-deletes: a removed track keeps its row and
    gains a marker. Those rows are dropped here, before anything is compared, so a
    tombstone sitting beside the live row for the same file resolves cleanly
    rather than looking like a collision.

    Public and separate from the matching below, because a sweep matches many
    plan entries against ONE library. Folding the walk into the match would make
    a sweep re-read every row per entry, and it would do something worse than
    that: a caller whose rows are a database cursor rather than a list would get
    the whole library on the first entry and an exhausted iterator on the second,
    with every track after that reported as absent and the run reported clean.
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

    TWO ACTIVE ROWS ON ONE LOCATION ARE SKIPPED AND SURFACED, never written to
    both. It happens: an import that ran twice against a renamed volume leaves
    two live rows for one file, and membership written to both puts one track in
    a playlist twice under two identities, which the user then cannot remove by
    removing it once.

    Takes rows rather than a database handle, so the rule is testable without one
    and this module does no input of its own. A caller matching several times
    against one library builds the index once with :func:`index_active_rows` and
    passes it to :func:`match_indexed_rows` instead.
    """
    return match_indexed_rows(
        requested,
        index_active_rows(rows, root=root, prefix_map=prefix_map),
        root=root,
        prefix_map=prefix_map,
    )


def match_indexed_rows(
    requested: Iterable[Path | str],
    index: Mapping[str, Sequence[str]],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> tuple[RowMatch, ...]:
    """Match against an index already built, so a sweep walks the library once."""
    by_location = index
    out: list[RowMatch] = []
    for entry in requested:
        text = str(entry)
        resolved = _comparable(text, root=root, prefix_map=prefix_map)
        if resolved.path is None:
            out.append(
                RowMatch(text, MatchOutcome.UNRESOLVED, resolution=resolved.resolution)
            )
            continue
        candidates = tuple(by_location.get(resolved.path, ()))
        if not candidates:
            out.append(
                RowMatch(text, MatchOutcome.ABSENT, resolution=resolved.resolution)
            )
        elif len(candidates) > 1:
            out.append(
                RowMatch(
                    text,
                    MatchOutcome.AMBIGUOUS,
                    content_ids=candidates,
                    resolution=resolved.resolution,
                )
            )
        else:
            out.append(
                RowMatch(
                    text,
                    MatchOutcome.MATCHED,
                    content_id=candidates[0],
                    resolution=resolved.resolution,
                )
            )
    return tuple(out)


def _root_row(db: Any, root_id: str) -> Any:
    """The playlist row the cutover adopted, or a refusal naming it.

    Resolved through the binding's own lookup rather than by scanning, and
    refused rather than defaulted: a missing root here means the registry and the
    database disagree about a tree that has cut over, which is the same skew
    ``anchored_root`` refuses one step earlier. Reaching this with no row means
    the caller's ``root_exists`` probe and the database disagree, and writing
    unparented would put the whole tree beside itself.

    NO ``.first()`` HERE, and that is the binding's shape rather than a style
    choice. ``get_playlist`` returns a filtered QUERY for every keyword except
    ``ID``, where it returns the row itself, or None. A caller that reaches for
    ``.first()`` out of habit therefore works everywhere else in this package and
    raises an attribute error on exactly this lookup.
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


def _rollback_quietly(db: Any) -> None:
    """Undo pending work on the caller's handle. Never masks the original failure.

    A rollback that raises on the way out of an except block would replace the
    real cause with its own, and the real cause is the one worth reading. This is
    the one place in the module where swallowing is right, and it swallows only
    the cleanup.
    """
    try:
        db.session.rollback()
    except Exception:  # noqa: BLE001 - a failed cleanup must not hide its cause
        logger.warning("could not roll back the pending session after a failed write")


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

    THE MEDIUM IS CHECKED FIRST AND THROUGH THE SHARED ASSERTION.
    :func:`cratekit.core.tree_registry.anchored_root` refuses a tree still on the
    bridge, refuses a native record naming no root, and refuses a root this
    library does not have, which is the restored pre-cutover database. Spelling
    any of those checks here would be a second implementation of one rule, and
    the cost of the two disagreeing is a user with a duplicated tree.

    THE SESSION SPINE IS CALLED, NOT REBUILT. The three gates come from
    :func:`cratekit.core.session.assert_gates` in their argued order, the commit
    happens behind a capture :func:`cratekit.core.snapshot.assert_verified`
    passed, and the analysis roots this write could touch are NAMED, so the watch
    that is the runtime half of R17's fifth surface watches them instead of
    watching nothing.

    NAMES MATCH THE XML-ERA NAMES EXACTLY, which is what makes a cutover an
    adoption rather than a duplication: the folder this finds by name is the one
    the bridge wrote, and the tracks already in it stay in it.

    THE GRID RULE IS UNTOUCHED. Nothing here creates a content row, writes a
    tempo, or names an analysis column. Membership is rows in the playlist tables
    the whitelist already permits, on content rows somebody else's import made.

    ``analysis_roots`` HAS NO DEFAULT AND MAY NOT BE EMPTY, which is the whole
    reason this unit was registered against U8's countdown. The watch it arms
    watches nothing when nobody names a root, and a guard that silently watches
    nothing is worse than an absent one: it reports a clean session either way.
    A caller that genuinely has nowhere to watch has a library with no analysis
    files, which is a fact worth stating rather than expressing as an omission.

    THE SESSION IS THIS FUNCTION'S OWN, and no gates factory is accepted. R29
    declares the boundary as one source per run, so sharing a session across
    several trees is not this unit's to offer. Offering it would also reopen the
    hole U32 already registered: a caller supplying its own factory can supply
    one that names no analysis roots, and the argument above would be undone by
    the parameter meant to make it flexible.

    ``purpose`` IS A DECLARATION AND NOT A BYPASS. Its default is the restrictive
    answer, and the one thing declaring a rebuild changes is the pair of
    convergence latches whose own remedy is a rebuild. See
    :class:`cratekit.core.convergence.Purpose`. Everything above stays: the
    medium check, the anchored root, all three session gates, the verified
    capture, the analysis watch, and the guarded commit.

    ``intent`` IS THE SAME DECLARATION ONE LAYER DOWN, and it exists because this
    function had no way to make it. ``assert_gates`` is where the LATCHES live,
    and a latch that condemns its own remedy is the failure this repository has
    already shipped once. U32 puts a second latch there: an unreconciled restore
    refuses every ordinary destructive session, and the markers it refuses over
    include "this tree needs rebuilding". Calling into the gates with the default
    intent therefore meant the rebuild was refused by the latch whose refusal
    names the rebuild, with a hand-edited state file as the only way out. It is a
    parameter rather than something derived from ``purpose`` because the two
    words answer different questions to different modules, and folding one into
    the other is how a caller ends up declaring something it did not mean.

    IT DOES NOT WIDEN ANYTHING BY ITSELF. A ``RECOVERY`` intent also lifts the
    unresolved-session latch, whose remedy is a restore rather than a rebuild, so
    the rebuild asserts that one for itself before it calls this. See
    :func:`cratekit.write.rebuild.rebuild_tree`.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch "
            "nothing and this session would report itself clean whatever "
            "happened to the library's grids; name the roots this write could "
            "touch (R17's fifth surface, runtime half)"
        )
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    # THE CONVERGENCE GATE, and it is here rather than in a command-line module
    # for the reason the medium check above is: this is the one call every
    # database membership write goes through, so a guard placed here cannot be
    # bypassed by a caller that forgot it. It runs BEFORE the session opens,
    # takes no lock and writes nothing on the passing path, and refuses a tree a
    # restore left short rather than quietly adding to it and reporting clean.
    convergence.assert_tree_writable(cfg, db, tree_id, registry, purpose=purpose)
    resolved_map = (
        [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
        if prefix_map is None
        else list(prefix_map)
    )

    # ONE walk of the library, before the loop, and it is not only about speed.
    # Rebuilding it per plan entry would re-normalize every row once per entry,
    # and it would silently break the first caller whose rows are a database
    # cursor rather than a list: entry one would consume the whole iterator and
    # every entry after it would match nothing and be reported absent.
    index = index_active_rows(rows, root=cfg.library.root, prefix_map=resolved_map)

    added = 0
    already_present = 0
    skipped: list[RowMatch] = []
    touched: list[str] = []

    with session.assert_gates(
        cfg, workflow=workflow, analysis_roots=watched, intent=intent
    ):
        capture = snapshot.capture(cfg, db=db)
        snapshot.assert_verified(capture)

        # THE WRITE IS PARENTED TO THE ROOT THE CUTOVER ADOPTED. Asserting the
        # anchored root and then resolving the folder globally by name would
        # leave the assertion true and the write somewhere else: a folder of that
        # name under a different parent, or a new one at the database root beside
        # the tree instead of inside it. That is the silent parallel tree the
        # registry exists to prevent, arriving through the check meant to prevent
        # it. The root row is resolved once, here, and every folder hangs off it.
        anchor = _root_row(db, root_id)

        try:
            for (folder_display, sub_display), requested in sorted(plan.items()):
                matches = match_indexed_rows(
                    requested, index, root=cfg.library.root, prefix_map=resolved_map
                )
                resolved_ids = [
                    match.content_id
                    for match in matches
                    if match.outcome is MatchOutcome.MATCHED and match.content_id
                ]
                skipped.extend(
                    match
                    for match in matches
                    if match.outcome is not MatchOutcome.MATCHED
                )
                if not resolved_ids:
                    continue

                folder = rb_writer.ensure_folder(db, folder_display, parent=anchor)
                playlist = rb_writer.ensure_playlist(db, sub_display, folder)
                touched.append(f"{folder_display}/{sub_display}")
                for content_id in resolved_ids:
                    if rb_writer.add_membership(db, playlist, content_id):
                        added += 1
                    else:
                        already_present += 1

            rb_writer.commit_guarded(db)
        except BaseException:
            # Nothing durable has landed, but the objects this loop created are
            # still pending on the CALLER'S handle, and the guarded commit raises
            # on two of its refusals before reaching its own rollback. Left
            # pending, they land on whatever commits next and arrive under that
            # operation's name, which is the hazard the writer's own docstring
            # describes. Rolled back here, and re-raised unchanged: this is a
            # cleanup, never a place that decides an error is survivable.
            _rollback_quietly(db)
            raise

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
        tree_id=tree_id,
        root_id=root_id,
        added=added,
        already_present=already_present,
        skipped=tuple(skipped),
        playlists=tuple(touched),
    )


__all__ = [
    "MEMBERSHIP_WORKFLOW",
    "VOX_SUB_CLASS",
    "ContentRow",
    "DuplicateFolders",
    "MatchOutcome",
    "MembershipReport",
    "RouteReport",
    "RowMatch",
    "TreeUnreachable",
    "VoxReport",
    "add_vox_playlists",
    "apply_playlist_changes",
    "apply_rating_changes",
    "apply_unplaced_changes",
    "index_active_rows",
    "insert_record_labels_tree",
    "match_active_rows",
    "match_indexed_rows",
    "write_tree_membership",
]
