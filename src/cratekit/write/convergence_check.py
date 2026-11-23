"""Where a governed tree's declared destinations land, and whether the tree matches (U36).

The destination planning and the read-only check :mod:`cratekit.write.rebuild`
runs around its write, and a diagnostic runs alone; every name the rebuild
uses is also reachable from that module. A destination resolves through the recorded node
identifiers first and by display name only when nothing was recorded, so a
rename is written into rather than doubled.

LAYER: write. Read only: nothing here opens a session, takes a lock or writes.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Any, Callable, Collection, Iterable, Sequence

from cratekit.core import config, convergence, locations, routing, taxonomy, tree_registry
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import genre_favorites, routing_pass, trees
from cratekit.write.tree_read import DeclaredPlacement, TreeNode, read_tree

# ---------------------------------------------------------------------------
# What the database actually holds
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Destination:
    """One declared destination and the node in the database it means.

    ``folder`` and ``playlist`` are the names a write must use: a recorded
    node's CURRENT names when one is found, so a folder renamed in rekordbox is
    written into rather than created again beside itself.
    """

    bucket: str
    sub: str
    folder: str
    playlist: str
    node: TreeNode | None = None
    renamed: bool = False

    def difference(
        self, direction: Direction, content_id: str, location: str | None = None
    ) -> Difference:
        """One track this destination holds or lacks against the declaration."""
        return Difference(
            direction, self.bucket, self.sub, self.folder, self.playlist, content_id, location
        )


def by_display_pair(nodes: Iterable[TreeNode]) -> dict[tuple[str, str], list[TreeNode]]:
    """The nodes keyed on the folder and playlist names a name-targeted write reaches."""
    out: dict[tuple[str, str], list[TreeNode]] = {}
    for node in nodes:
        out.setdefault((node.folder_display, node.playlist_display), []).append(node)
    return out


def only_one(candidates: Sequence[TreeNode]) -> TreeNode | None:
    """The sole candidate, or None: two nodes on one display pair are never chosen by position."""
    return candidates[0] if len(candidates) == 1 else None


def resolve_destinations(
    declared: taxonomy.Taxonomy,
    placements: Sequence[DeclaredPlacement],
    nodes: Sequence[TreeNode],
    record: convergence.TreeConvergence | None,
) -> tuple[Destination, ...]:
    """Bind each declared destination to the node a previous write actually used.

    THE RESOLUTION ORDER: recorded identifier, then declared display name, then
    nothing (the write creates it). A recorded identifier that no longer
    resolves falls back rather than refusing, or the damage would break its own
    repair. THE DESTINATION SET IS THE UNION OF WHAT THIS RUN DERIVED AND WHAT A
    PREVIOUS WRITE RECORDED, so a destination that lost every declared track is
    still compared rather than falling into ``foreign``.
    """
    by_ids = {(node.folder_id, node.playlist_id): node for node in nodes}
    by_display = by_display_pair(nodes)

    derived = {(entry.bucket, entry.sub) for entry in placements}
    wanted = set(derived)
    if record is not None:
        wanted |= {(entry.bucket, entry.sub) for entry in record.nodes}

    out: list[Destination] = []
    for bucket, sub in sorted(wanted):
        names = _declared_display(declared, bucket, sub, derived=(bucket, sub) in derived)
        if names is None:
            # A RECORDED DESTINATION THIS TAXONOMY NO LONGER DECLARES IS SKIPPED,
            # not refused; it is reported as ``undeclared``.
            continue
        folder_display, sub_display = names
        recorded = None if record is None else record.node(bucket, sub)
        node = None
        if recorded is not None:
            node = by_ids.get((recorded.folder_id, recorded.playlist_id))
        if node is None:
            # Ambiguity is left unresolved here and refused by
            # ``assert_addressable`` with both candidates named.
            node = only_one(by_display.get((folder_display, sub_display), ()))
        if node is None:
            out.append(Destination(bucket, sub, folder_display, sub_display))
            continue
        shown = (node.folder_display, node.playlist_display)
        out.append(Destination(bucket, sub, *shown, node, shown != (folder_display, sub_display)))
    return tuple(out)


def _declared_display(
    declared: taxonomy.Taxonomy, bucket: str, sub: str, *, derived: bool
) -> tuple[str, str] | None:
    """The two display names a destination means, None, or a structured refusal.

    ``derived=True``: this run's own derivation produced an identifier the same
    taxonomy cannot name, so it refuses with a defect remedy (S4).
    ``derived=False``: only the node record names it, an ordinary template edit,
    so it answers None and the caller reports it.
    """
    try:
        return routing_pass.destination(declared, bucket, sub)
    except KeyError as exc:
        if not derived:
            return None
        raise refuse(
            "routing-destination-renamed",
            f"this rebuild's own derivation placed a track in {bucket}/{sub} and "
            f"this library's taxonomy declares no such destination; one document "
            f"has contradicted itself, and inventing a name for it would create a "
            f"folder nobody chose",
            remedy=Remedy.REPORT_DEFECT,
            steps=(
                "run the convergence check, which reports what this tree holds "
                "and writes nothing",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={"bucket": bucket, "sub": sub},
        ) from exc


def undeclared_destinations(
    declared: taxonomy.Taxonomy, record: convergence.TreeConvergence | None
) -> tuple[str, ...]:
    """Recorded destinations this taxonomy no longer declares, as stable identifiers.

    Reported rather than refused (a template edit is ordinary and reversible)
    and rather than silent (the playlist is still under a governed root).
    """
    if record is None:
        return ()
    return tuple(
        sorted(
            f"{entry.bucket}/{entry.sub}"
            for entry in record.nodes
            if _declared_display(declared, entry.bucket, entry.sub, derived=False) is None
        )
    )


def assert_addressable(
    tree_id: str, destinations: Sequence[Destination], nodes: Sequence[TreeNode]
) -> None:
    """Refuse a destination set a name-targeted write cannot tell apart.

    Every find-or-create in the guarded writer targets a playlist by the name
    rekordbox shows, so three shapes are refused before anything is written:
    two declared destinations on one display pair, two on one node, and one
    display pair carried by two nodes under the root. A person has to say
    which node is real.
    """
    by_pair: dict[tuple[str, str], Destination] = {}
    by_node: dict[tuple[str, str], Destination] = {}
    for entry in destinations:
        pair = (entry.folder, entry.playlist)
        clash = by_pair.get(pair)
        if clash is not None:
            raise refuse(
                "tree-unconverged",
                f"the tree {tree_id!r} resolves the declared destinations "
                f"{clash.bucket}/{clash.sub} and {entry.bucket}/{entry.sub} to "
                f"one folder and playlist named {entry.folder!r} and "
                f"{entry.playlist!r}; every write here targets a playlist by the "
                f"name rekordbox shows, so both sets of tracks would go into "
                f"whichever node that name reaches first and each track would sit "
                f"in two playlists at once, and the record written afterwards "
                f"would name one node for both destinations, after which no "
                f"rebuild could ever converge this tree again",
                remedy=Remedy.FIX_CONFIG_VALUES,
                steps=(
                    "give the two folders distinct names in rekordbox, or make "
                    "this library's taxonomy declare distinct names for them",
                    "run the convergence check again, which writes nothing",
                ),
                scope=Scope.RUN,
                origin=("tree_rebuild",),
                detail={
                    "tree_id": tree_id,
                    "folder": entry.folder,
                    "playlist": entry.playlist,
                    "destinations": [f"{clash.bucket}/{clash.sub}", f"{entry.bucket}/{entry.sub}"],
                },
            )
        by_pair[pair] = entry
        if entry.node is None:
            continue
        node = (entry.node.folder_id, entry.node.playlist_id)
        collided = by_node.get(node)
        if collided is not None:
            raise refuse(
                "tree-unconverged",
                f"the tree {tree_id!r} resolves the declared destinations "
                f"{collided.bucket}/{collided.sub} and "
                f"{entry.bucket}/{entry.sub} to one playlist row; a rebuild would "
                f"file both sets of tracks into it and report the other "
                f"destination short forever, and an additive rebuild cannot take "
                f"either set back out",
                remedy=Remedy.FIX_CONFIG_VALUES,
                steps=(
                    "separate the two destinations in rekordbox, then run the "
                    "rebuild, which rebuilds the node record from what it finds",
                ),
                scope=Scope.RUN,
                origin=("tree_rebuild",),
                detail={
                    "tree_id": tree_id,
                    "node": f"{entry.node.folder_id}/{entry.node.playlist_id}",
                    "destinations": [
                        f"{collided.bucket}/{collided.sub}",
                        f"{entry.bucket}/{entry.sub}",
                    ],
                },
            )
        by_node[node] = entry

    counted = by_display_pair(nodes)
    doubled = sorted(pair for pair in by_pair if len(counted.get(pair, ())) > 1)
    if doubled:
        raise refuse(
            "tree-unconverged",
            f"the tree {tree_id!r} holds more than one playlist named "
            + ", ".join(f"{folder!r}/{playlist!r}" for folder, playlist in doubled)
            + "; a writer that targets a playlist by name cannot tell them apart, "
            "so it would write to the first one twice and to the second one never",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=(
                "rename or remove the duplicate folder or playlist in rekordbox",
                "run the convergence check again, which writes nothing",
            ),
            scope=Scope.RUN,
            origin=("tree_rebuild",),
            detail={
                "tree_id": tree_id,
                "duplicated": [f"{folder}/{playlist}" for folder, playlist in doubled],
            },
        )


def plan_destinations(
    declared: taxonomy.Taxonomy,
    placements: Sequence[DeclaredPlacement],
    standing: Sequence[TreeNode],
    record: convergence.TreeConvergence | None,
    *,
    tree_id: str,
) -> tuple[tuple[Destination, ...], dict[tuple[str, str], list[str]]]:
    """Resolve every declared placement into the two names the writer targets.

    Resolve through the node map, refuse an ambiguous pair, key the plan on the
    display names. The destinations come back beside the plan so the writer
    records where each landed without re-resolving by name.
    """
    destinations = resolve_destinations(declared, placements, standing, record)
    assert_addressable(tree_id, destinations, standing)
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}
    plan: dict[tuple[str, str], list[str]] = {}
    for entry in placements:
        destination = by_key[(entry.bucket, entry.sub)]
        plan.setdefault((destination.folder, destination.playlist), []).append(entry.location)
    return destinations, plan


def _under_recorded_folders(
    destinations: Sequence[Destination],
    plan: dict[tuple[str, str], list[str]],
    record: convergence.TreeConvergence | None,
    standing: Sequence[TreeNode],
) -> tuple[tuple[Destination, ...], dict[tuple[str, str], list[str]]]:
    """A Favorites with no node of its own goes under the folder its bucket's record binds.

    Resolving it by the declared name under a renamed folder would make a
    second folder holding only Favorites.
    """
    if record is None:
        return tuple(destinations), plan
    display_of = {node.folder_id: node.folder_display for node in standing}
    recorded_folder: dict[str, str] = {}
    for entry in record.nodes:
        if entry.folder_id in display_of:
            recorded_folder.setdefault(entry.bucket, entry.folder_id)
    moved: list[Destination] = []
    for entry in destinations:
        folder_id = recorded_folder.get(entry.bucket)
        if entry.node is not None or folder_id is None:
            moved.append(entry)
            continue
        folder_now = display_of[folder_id]
        if folder_now != entry.folder:
            locations = plan.pop((entry.folder, entry.playlist), [])
            plan.setdefault((folder_now, entry.playlist), []).extend(locations)
            entry = replace(entry, folder=folder_now, renamed=True)
        moved.append(entry)
    return tuple(moved), plan


# ---------------------------------------------------------------------------
# The convergence check
# ---------------------------------------------------------------------------

#: The dimension name a derivation with no vocal calibration reports as not
#: compared (D7); the ``with vox`` classes are not judged on such a run.
VOCAL_DIMENSION = "vocal"

#: The word a summary names a playlist :func:`unidentified` found by (R-1991).
NOT_COMPARED = "not-compared"


class Direction(StrEnum):
    """Which way a difference points. Both are reported; only one is repairable."""

    #: The declaration places a track here and the database does not hold it.
    MISSING = "missing"
    #: The database holds a track in a declared destination that the declaration
    #: does not place there.
    UNEXPECTED = "unexpected"


@dataclass(frozen=True, slots=True)
class Difference:
    """One track, one destination, and which way the two sides disagree."""

    direction: Direction
    bucket: str
    sub: str
    folder: str
    playlist: str
    content_id: str | None = None
    location: str | None = None

    def summary(self) -> str:
        """One line naming the difference by its STABLE identifiers.

        A folder name somebody has since renamed would name something they
        cannot find.
        """
        what = self.content_id or self.location or "?"
        return f"{self.direction}:{self.bucket}/{self.sub}:{what}"


@dataclass(frozen=True, slots=True)
class ConvergenceReport:
    """What one tree's declaration and one tree's database rows say, side by side.

    Two sets are reported and are NOT differences: ``unmatched``, every declared
    file that reached no single active row, which no playlist can hold, and
    ``foreign``, every node under the governed root no declared destination
    resolves to and that :func:`namesakes` does not compare (R-1949): one
    whose names declare nothing, a manual class such as Candy, one rekordbox
    removed, or one in a dimension this run did not compare. A playlist
    :func:`unidentified` names is in ``unidentified`` instead (R-1991). THE
    ACTIVE-ROW RULE APPLIES TO BOTH DIRECTIONS.
    """

    tree_id: str
    root_id: str
    missing: tuple[Difference, ...] = ()
    unexpected: tuple[Difference, ...] = ()
    unmatched: tuple[trees.RowMatch, ...] = ()
    foreign: tuple[str, ...] = ()
    renamed: tuple[str, ...] = ()
    not_compared: tuple[str, ...] = ()
    #: How many placements the derivation produced. ZERO IS NOT CONVERGED.
    derived: int = 0
    #: Every declared destination holding a track more than once, as
    #: ``bucket/sub:content_id``. A doubling an additive write cannot undo.
    doubled: tuple[str, ...] = ()
    #: Destinations the NODE RECORD names that this taxonomy no longer declares,
    #: reported so "not compared" reads apart from "matched".
    undeclared: tuple[str, ...] = ()
    #: Every playlist :func:`unidentified` names, as ``folder/playlist`` in the
    #: names a person finds them by: NOT COMPARED, so never converged (R-1991).
    unidentified: tuple[str, ...] = ()

    @property
    def differences(self) -> tuple[Difference, ...]:
        """Both directions, in one tuple, because R39 asks for both."""
        return self.missing + self.unexpected

    @property
    def converged(self) -> bool:
        """Whether this tree matches what the library declares. FOUR conditions.

        No difference in either direction; a derivation that placed something;
        no playlist holding a track twice, which an additive rebuild cannot
        repair; and no playlist the check could not tie to a destination that
        may be one (R-1991), which a clean report would stand over unread.
        """
        return (
            not self.differences
            and self.derived > 0
            and not self.doubled
            and not self.unidentified
        )

    def summaries(self) -> tuple[str, ...]:
        """Everything that stands between this tree and a cleared flag.

        The doubled rows and the playlists not compared included, since this is
        the evidence the clearing call is handed.
        """
        return (
            tuple(entry.summary() for entry in self.differences)
            + tuple(f"doubled:{entry}" for entry in self.doubled)
            + tuple(f"{NOT_COMPARED}:{entry}" for entry in self.unidentified)
        )


def _uncompared_playlist_subs(
    declared: taxonomy.Taxonomy, not_compared: Sequence[str]
) -> set[str]:
    """The playlist signal classes whose source this run could not read (U119).

    Their source is a playlist a person can empty on any day, so their
    differences leave the comparison; their destinations stay resolved.
    """
    if genre_favorites.FAVORITES_DIMENSION not in tuple(not_compared):
        return set()
    return {
        entry.id
        for entry in declared.sub_classes
        if entry.additive and entry.signal == taxonomy.SIGNAL_PLAYLIST
    }


def _additive_ids(declared: taxonomy.Taxonomy, signal: str) -> set[str]:
    """The additive sub class ids the declaration derives from ``signal``."""
    return {
        entry.id for entry in declared.sub_classes if entry.additive and entry.signal == signal
    }


def _uncompared_subs(declared: taxonomy.Taxonomy, not_compared: Sequence[str]) -> set[str]:
    """The sub class ids whose dimension a run named as not compared."""
    skipped = _uncompared_playlist_subs(declared, not_compared)
    if VOCAL_DIMENSION in tuple(not_compared):
        skipped |= _additive_ids(declared, taxonomy.SIGNAL_VOX)
    return skipped


def declared_names(declared: taxonomy.Taxonomy) -> dict[tuple[str, str], tuple[str, str]]:
    """The destinations a derivation files into, keyed on their two display names.

    Per bucket, the places a track competes for, its genre subs and every sub
    class automation derives, each named as
    :func:`cratekit.write.routing_pass.destination` names it. A manual class
    (the shipped Candy) is a person's to fill, so its names are no evidence of
    anything and it is left out. A former or split place is named only by its
    holder's own band, so it is not a destination of its own here. A pair two
    destinations share keeps the first in sorted order, so the answer never
    depends on declaration order.
    """
    classes = {
        entry.id
        for entry in declared.sub_classes
        if entry.policy is not taxonomy.SubPolicy.MANUAL
    }
    found: dict[tuple[str, str], tuple[str, str]] = {}
    for bucket in sorted(declared.buckets, key=lambda entry: entry.id):
        _kind, competing = routing.competing_subs(declared, bucket.id)
        subs = set(competing) | {genre.id for genre in bucket.genre_subs} | classes
        for sub in sorted(subs):
            try:
                names = routing_pass.destination(declared, bucket.id, sub)
            except KeyError:
                continue
            found.setdefault(names, (bucket.id, sub))
    return found


def namesakes(
    declared: taxonomy.Taxonomy,
    nodes: Sequence[TreeNode],
    destinations: Sequence[Destination],
    not_compared: Sequence[str],
    record: convergence.TreeConvergence | None = None,
) -> tuple[Destination, ...]:
    """The playlists under the root no destination resolved to that bear a declared one's names.

    THE PLAYLIST A TRACK WAS LEFT IN IS COMPARED THOUGH NOTHING DERIVES INTO IT
    (R-1949): a cleared second genre leaves its track in that genre's folder,
    and while no other track is filed there the playlist was read as a
    person's own, so a check called the tree matching over a membership no
    genre files. Each is compared with nothing declared there. A destination
    this run derived or a record names already has its node, so a second node
    with its names is left as it was; so is a dimension this run did not
    compare, whose absence is not evidence (U119), and a playlist rekordbox
    removed, which nobody sees. A folder a previous write recorded, whose name
    now declares no bucket, is read by its bucket's declared name, so a folder
    renamed in rekordbox is still compared once a write has recorded it; a
    folder that bears a declared bucket's name is read by that name.
    """
    covered = {(entry.bucket, entry.sub) for entry in destinations}
    resolved = {
        (entry.node.folder_id, entry.node.playlist_id)
        for entry in destinations
        if entry.node is not None
    }
    skipped = _uncompared_subs(declared, not_compared)
    names = declared_names(declared)
    known = set(declared.bucket_ids())
    bucket_names = {declared.bucket(bucket_id).display for bucket_id in known}
    recorded_folder = {
        entry.folder_id: declared.bucket(entry.bucket).display
        for entry in (() if record is None else record.nodes)
        if entry.bucket in known
    }
    out: list[Destination] = []
    for node in nodes:
        if node.removed or (node.folder_id, node.playlist_id) in resolved:
            continue
        folder = node.folder_display
        if folder not in bucket_names:
            folder = recorded_folder.get(node.folder_id, folder)
        place = names.get((folder, node.playlist_display))
        if place is None or place in covered or place[1] in skipped:
            continue
        out.append(Destination(*place, node.folder_display, node.playlist_display, node))
    return tuple(out)


def unidentified(
    declared: taxonomy.Taxonomy,
    nodes: Sequence[TreeNode],
    compared: Collection[tuple[str, str]],
    not_compared: Sequence[str],
    record: convergence.TreeConvergence | None,
    filed: Collection[str],
) -> tuple[TreeNode, ...]:
    """The playlists under the root no name or record ties to a bucket that may hold a leftover.

    A FOLDER RENAMED IN REKORDBOX THAT NO WRITE RECORDED (R-1991): its name
    declares no bucket and the record names none, so a playlist under it
    bearing a declared destination's playlist name could be any bucket's, and
    :func:`namesakes` cannot compare it. While it holds a track this run files
    (``filed``), it may be a genre's playlist holding a cleared second genre's
    track, so it is named as not compared rather than read as a person's own.
    Left as they were, in ``foreign``: a node already ``compared``, one
    rekordbox removed, one under a folder whose name declares a bucket or that
    any record names (:func:`namesakes` read those), one whose name no
    destination bears or bears only in a dimension this run did not compare
    (U119), and one holding no filed track.
    """
    names = declared_names(declared)
    readings: dict[str, set[str]] = {}
    for (_folder, playlist), (_bucket, sub) in names.items():
        readings.setdefault(playlist, set()).add(sub)
    skipped = _uncompared_subs(declared, not_compared)
    bucket_names = {declared.bucket(bucket_id).display for bucket_id in declared.bucket_ids()}
    recorded = {entry.folder_id for entry in (() if record is None else record.nodes)}
    return tuple(
        node
        for node in nodes
        if not node.removed
        and (node.folder_id, node.playlist_id) not in compared
        and node.folder_display not in bucket_names
        and node.folder_id not in recorded
        and readings.get(node.playlist_display, set()) - skipped
        and node.content_ids & set(filed)
    )


def check(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
    placements: Sequence[DeclaredPlacement],
    rows: Iterable[trees.ContentRow],
    root_exists: Callable[[str], bool],
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    not_compared: Sequence[str] = (),
) -> ConvergenceReport:
    """Report, for one governed tree, how the declaration and the database differ.

    READ ONLY, so it runs against a library that is refusing every write; it
    resolves destinations exactly as the rebuild does.
    """
    root_id = tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
    rules = trees.prefix_rules(cfg, prefix_map)

    # ONE walk of the library, before anything is compared: ``rows`` may be a
    # database cursor, which reads empty to whoever walks it second.
    index = trees.index_active_rows(rows, root=cfg.library.root, prefix_map=rules)
    matches = trees.match_indexed_rows(
        [entry.location for entry in placements], index, root=cfg.library.root, prefix_map=rules
    )
    resolved_id: dict[str, str] = {}
    unmatched: list[trees.RowMatch] = []
    for match in matches:
        if match.outcome is trees.MatchOutcome.MATCHED and match.content_id:
            resolved_id[match.requested] = match.content_id
        else:
            unmatched.append(match)

    nodes = read_tree(db, root_id)
    record = convergence.read(cfg).tree(tree_id)
    destinations = resolve_destinations(declared, placements, nodes, record)
    assert_addressable(tree_id, destinations, nodes)
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}

    wanted: dict[tuple[str, str], set[str]] = {}
    missing: list[Difference] = []
    for entry in placements:
        content_id = resolved_id.get(entry.location)
        if content_id is None:
            continue  # surfaced through ``unmatched`` above
        destination = by_key[(entry.bucket, entry.sub)]
        wanted.setdefault((entry.bucket, entry.sub), set()).add(content_id)
        held = frozenset() if destination.node is None else destination.node.content_ids
        if content_id not in held:
            missing.append(destination.difference(Direction.MISSING, content_id, entry.location))

    governed = {
        (entry.node.folder_id, entry.node.playlist_id): entry
        for entry in (
            *destinations,
            *namesakes(declared, nodes, destinations, not_compared, record),
        )
        if entry.node is not None
    }
    # Only active rows count on this side too: a membership on a soft-deleted
    # track is a leftover nobody can act on.
    active = {content_id for ids in index.values() for content_id in ids}
    unread = {
        (node.folder_id, node.playlist_id)
        for node in unidentified(
            declared, nodes, governed, not_compared, record, set(resolved_id.values()) & active
        )
    }
    unexpected: list[Difference] = []
    foreign: list[str] = []
    not_read: list[str] = []
    doubled: list[str] = []
    for node in nodes:
        destination = governed.get((node.folder_id, node.playlist_id))
        if destination is None:
            shown = f"{node.folder_display}/{node.playlist_display}"
            (not_read if (node.folder_id, node.playlist_id) in unread else foreign).append(shown)
            continue
        # A doubled row is damage whether or not the declaration places it here.
        for content_id in sorted(node.doubled & active):
            doubled.append(f"{destination.bucket}/{destination.sub}:{content_id}")
        declared_here = wanted.get((destination.bucket, destination.sub), set())
        for content_id in sorted((node.content_ids & active) - declared_here):
            unexpected.append(destination.difference(Direction.UNEXPECTED, content_id))
    if unexpected:
        # The file each leftover row resolved to, since a person finds a track
        # by its file and not by its row identifier (R-312).
        located_at = {
            content_id: location for location, ids in index.items() for content_id in ids
        }
        unexpected = [
            replace(entry, location=located_at.get(entry.content_id or ""))
            for entry in unexpected
        ]

    # A PLAYLIST DIMENSION THIS RUN COULD NOT READ IS NOT A DIFFERENCE (U119).
    uncompared = _uncompared_playlist_subs(declared, not_compared)
    if uncompared:
        missing = [entry for entry in missing if entry.sub not in uncompared]
        unexpected = [entry for entry in unexpected if entry.sub not in uncompared]
    return ConvergenceReport(
        tree_id=tree_id,
        root_id=root_id,
        missing=tuple(missing),
        unexpected=tuple(unexpected),
        unmatched=tuple(unmatched),
        foreign=tuple(sorted(foreign)),
        renamed=tuple(
            sorted(f"{entry.bucket}/{entry.sub}" for entry in destinations if entry.renamed)
        ),
        not_compared=tuple(not_compared),
        derived=len(placements),
        doubled=tuple(sorted(doubled)),
        undeclared=undeclared_destinations(declared, record),
        unidentified=tuple(sorted(not_read)),
    )
