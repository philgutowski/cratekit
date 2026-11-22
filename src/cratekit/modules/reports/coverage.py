"""Feature Inventory row 14's reporting half: what the governed tree does not hold.

A report rather than a pass: ``route.unplaced`` moves tracks, and this moves
nothing, opens no database, and answers which collection entries sit in no
playlist under the DECLARED routing tree, so it is safe to read before sweeping.

An entry is covered when the tree's display sits ANYWHERE above a playlist
holding it, as :func:`aging.intake_groupings` decides, so a tree filed inside
another folder still counts. A tree absent from the export refuses rather than
reporting every track uncovered. Placements are counted, so a track filed three
times is covered once and shown filed three times.

Layer note: MODULES. Row 14 is a Core row, so the entry declares no
``module_id``; the engine lives here because it reads an export through
:mod:`export`, under this package's read only allowlist.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import taxonomy
from cratekit.core.cause import Scope, refuse
from cratekit.modules.reports.export import CollectionEntry, LibraryView


@dataclass(frozen=True, slots=True)
class Placement:
    """One entry and every governed path holding it; empty when it is uncovered."""

    entry: CollectionEntry
    paths: tuple[tuple[str, ...], ...] = ()

    @property
    def covered(self) -> bool:
        return bool(self.paths)


@dataclass(frozen=True, slots=True)
class CoverageReport:
    """Every collection entry, partitioned by whether the governed tree holds it.

    ``folders`` is the export's count per playlist under the tree, so a large
    uncovered count can be read as a thin tree or an unrun sweep.
    """

    tree_id: str
    tree_display: str
    covered: tuple[Placement, ...] = ()
    uncovered: tuple[Placement, ...] = ()
    folders: tuple[tuple[tuple[str, ...], int], ...] = ()

    @property
    def total(self) -> int:
        return len(self.covered) + len(self.uncovered)

    @property
    def placements(self) -> int:
        """How many times the tree files something, which can exceed ``covered``."""
        return sum(len(item.paths) for item in self.covered)


def _refuse_absent(tree: taxonomy.Node):
    """The refusal for a governed tree the export does not contain, naming both
    fixes so nobody renames folders to match the software.
    """
    return refuse(
        "governed-tree-absent",
        f"no folder named {tree.display!r} appears anywhere in the exported tree, "
        f"so this report never found the routing tree it governs; reporting every "
        f"track as uncovered would tell somebody to re-file a library that is "
        f"already filed",
        steps=(
            "check that the export really holds the routing tree the taxonomy "
            "declares, and that it is the current export",
            "if the tree is called something else in this library, change the "
            "declared display in the taxonomy template rather than renaming "
            "folders to match the software",
        ),
        scope=Scope.RUN,
        origin=("reports",),
        detail={"declared": tree.display, "tree": tree.id},
    )


def governed_paths(view: LibraryView, *, tree: taxonomy.Node) -> tuple[tuple[str, ...], ...]:
    """Every playlist path with the tree's display ABOVE it, in export order."""
    wanted = tree.display
    return tuple(
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
    )  # fmt: skip


def survey(view: LibraryView, *, tree: taxonomy.Node) -> CoverageReport:
    """Partition the collection by whether the governed tree files it.

    Not called ``coverage``, its module's name. ``held`` and the folder counts
    are built from the same RESOLVING track ids, so the folder rows always sum
    to ``placements`` even when a playlist names an entry the collection lacks.
    """
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

    under = frozenset(governed_paths(view, tree=tree))
    known = {entry.track_id for entry in view.entries}
    held: dict[str, list[tuple[str, ...]]] = {}
    counts: dict[tuple[str, ...], int] = {}
    for playlist in view.playlists:
        if playlist.path not in under:
            continue
        counts.setdefault(playlist.path, 0)
        for track_id in playlist.track_ids:
            if track_id not in known:
                continue
            counts[playlist.path] += 1
            held.setdefault(track_id, []).append(playlist.path)

    covered: list[Placement] = []
    uncovered: list[Placement] = []
    for entry in view.entries:
        paths = tuple(held.get(entry.track_id, ()))
        placement = Placement(entry=entry, paths=paths)
        (covered if paths else uncovered).append(placement)

    return CoverageReport(
        tree_id=tree.id,
        tree_display=tree.display,
        covered=tuple(covered),
        uncovered=tuple(sorted(uncovered, key=_by_name)),
        folders=tuple(sorted(counts.items())),
    )


def _by_name(placement: Placement) -> tuple[str, str, str]:
    """Artist, then name, then identifier, so two runs of one library agree."""
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)


__all__ = ["CoverageReport", "Placement", "governed_paths", "survey"]
