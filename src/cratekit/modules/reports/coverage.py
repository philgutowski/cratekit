"""Feature Inventory row 14's reporting half: what the governed tree does not hold.

The source system answers this question twice and never the same way. One script
walks the genre folders and prints what it finds; another sweeps unplaced tracks
and prints what it moved. Neither of them can say "the tree covers 9,842 of your
10,070 tracks and here are the 228 it misses", because both of them are passes
rather than reports, and a pass tells you what it did rather than what is true.

**This is the report, and the sweep is a different verb.** ``route.unplaced``
moves tracks. This one moves nothing, opens no database, and answers exactly one
question: which collection entries sit in no playlist under the DECLARED routing
tree. That separation is what makes the answer safe to look at before deciding
whether to run the sweep, and it is why the two live in different layers.

**Coverage is membership under the tree, at any depth.** An entry is covered when
one of its placements has the tree's declared display ANYWHERE above the playlist
holding it, exactly as :func:`aging.intake_groupings` decides what counts as an
intake grouping. Anchoring at position zero reported nothing at all for a person
who had filed the tree inside another folder, and that person has organized their
library rather than hidden it.

**A tree that is not in the export refuses.** Reporting every entry as uncovered
would be technically true and useless: a person whose export predates the tree, or
whose export was taken from the wrong library, would be told to re-file ten
thousand tracks. The two facts ``export`` already refuses to render identically,
"the structure is absent" and "the structure is empty", are kept apart here for
the same reason one module down.

**Placement is counted, not just presence.** An entry in three folders under the
tree is covered once and reported as filed three times, because a track that is
genuinely in three places is a different thing to look at from a track in one, and
the source system's per-playlist walk could not see it at all.

Layer note: MODULES. Row 14 is a Core row and this report is reachable without
enabling a module, which is why the entry declares no ``module_id``. The engine
lives here because it reads an export through :mod:`export` and the allowlist that
governs this package is what keeps it read only.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import taxonomy
from cratekit.core.cause import Scope, refuse
from cratekit.modules.reports.export import CollectionEntry, LibraryView


@dataclass(frozen=True, slots=True)
class Placement:
    """One entry and every path under the governed tree that holds it.

    ``paths`` is empty exactly when the entry is uncovered, so the two halves of
    the report are one type asked two ways rather than two types that can drift.
    """

    entry: CollectionEntry
    paths: tuple[tuple[str, ...], ...] = ()

    @property
    def covered(self) -> bool:
        return bool(self.paths)


@dataclass(frozen=True, slots=True)
class CoverageReport:
    """Every collection entry, partitioned by whether the governed tree holds it.

    The two tuples partition the collection and the suite asserts that they do. An
    entry in both is an entry somebody acts on twice, and an entry in neither is
    one the report was supposed to surface and did not.

    ``folders`` is the tree's own shape as the export has it, one row per folder
    directly beneath the tree, so a person reading a large uncovered count can see
    whether the tree is thin or whether the sweep simply has not run.
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
        """How many times the tree files something, which exceeds ``covered``.

        A track filed under two energy bands is one covered track and two
        placements, and the difference is the number a person actually asks about
        when a folder count looks too high.
        """
        return sum(len(item.paths) for item in self.covered)


def _refuse_absent(tree: taxonomy.Node):
    """The refusal for a governed tree the export does not contain.

    Worded around what the reader has to do rather than around what this module
    observed, because the two acts are different: an export taken before the tree
    existed is re-exported, and a tree the template misnames is a template to
    correct. Naming both is what stops somebody renaming folders to match the
    software, which is the direction R19 exists to prevent.
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
    """Every playlist path the governed tree holds, in export order.

    A path qualifies when the declared display sits ABOVE the playlist rather
    than at the front of the path, which is the same widening
    :func:`aging.intake_groupings` makes and for the same reason. A tree carrying
    the declared display twice yields playlists from both, because a report that
    silently picked one would hide the duplication from the person who has to fix
    it.
    """
    wanted = tree.display
    return tuple(
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
    )


def coverage(view: LibraryView, *, tree: taxonomy.Node) -> CoverageReport:
    """Partition the collection by whether the governed tree files it.

    Indexed once rather than asked per entry. ``LibraryView.entry`` is a linear
    scan and says so; calling it per placement is the N times M shape U18 shipped
    and then had to remove.
    """
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

    under = frozenset(governed_paths(view, tree=tree))
    held: dict[str, list[tuple[str, ...]]] = {}
    counts: dict[tuple[str, ...], int] = {}
    for playlist in view.playlists:
        if playlist.path not in under:
            continue
        counts[playlist.path] = len(playlist.track_ids)
        for track_id in playlist.track_ids:
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
    """Artist, then name, then identifier, so two runs of one library agree.

    The identifier is last rather than first because a person reads this list
    looking for records they recognise, and it is present at all because two
    entries can genuinely carry one artist and one name, which is the pair the
    duplicate audit exists to ask about.
    """
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)


__all__ = [
    "CoverageReport",
    "Placement",
    "coverage",
    "governed_paths",
]
