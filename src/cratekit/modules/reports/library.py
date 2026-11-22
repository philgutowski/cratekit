"""``report.library``: what this library actually contains, as one read-only answer.

- **Genres**: one row per folder directly beneath the governed tree, counted by
  DISTINCT track, since summing sub playlists double counts a track filed twice.
- **Tempo spread**: read from the naming head through the DECLARED template,
  never a private pattern; unreadable heads are counted, not dropped.
- **Tree shape**: the declared depth beside the deepest governed path, since a
  deeper tree is one the XML bridge cannot write.
- **Gaps**: undeclared folders, unused buckets, entries without a head, and a
  COUNT of entries in no playlist (``audit.coverage`` lists them).

Nothing here is a policy: every number is a fact about the export.

Layer note: MODULES. Gated by the ``reports`` toggle (R5).
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import taxonomy
from cratekit.core.naming import NameTemplate, parse_head
from cratekit.modules.reports.export import LibraryView


@dataclass(frozen=True, slots=True)
class GenreRow:
    """One folder beneath the governed tree; ``bucket_id`` None if undeclared."""

    path: tuple[str, ...]
    tracks: int
    playlists: int
    bucket_id: str | None = None

    @property
    def display(self) -> str:
        return self.path[-1] if self.path else ""


@dataclass(frozen=True, slots=True)
class TempoSpread:
    """The tempo range of the entries whose head could be read.

    ``readable`` and ``unreadable`` are both carried, so a partial spread is
    visible as one. Every range field is None when nothing was readable, never
    zero, which is a tempo a head can carry.
    """

    readable: int = 0
    unreadable: int = 0
    lowest: float | None = None
    highest: float | None = None
    median: float | None = None


@dataclass(frozen=True, slots=True)
class TreeShape:
    """The export's tree beside the template; ``deepest`` counts the tree's node."""

    declared_depth: int
    deepest: int
    folders: int
    playlists: int

    @property
    def deeper_than_declared(self) -> bool:
        return self.deepest > self.declared_depth


@dataclass(frozen=True, slots=True)
class Gaps:
    """The three absences, kept apart because three different acts close them."""

    undeclared_folders: tuple[tuple[str, ...], ...] = ()
    unused_buckets: tuple[str, ...] = ()
    entries_without_head: int = 0
    entries_in_no_playlist: int = 0


@dataclass(frozen=True, slots=True)
class LibraryStatistics:
    """One export, described. Reads a document, writes nothing."""

    tree_id: str
    tree_display: str
    entries: int
    genres: tuple[GenreRow, ...]
    tempo: TempoSpread
    shape: TreeShape
    gaps: Gaps


def _bpm_of(name: str, *, template: NameTemplate) -> float | None:
    """The tempo in one name's head as a float, or None when there is none."""
    written = (parse_head(name, template=template) or {}).get("bpm")
    if written is None:
        return None
    try:
        return float(written)
    except ValueError:  # pragma: no cover - the head pattern admits digits only
        return None


def _median(values: list[float]) -> float:
    """The middle value, averaged across the pair when the count is even.

    Written here because the package's allowlist admits no module providing one.
    """
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def tempo_spread(view: LibraryView, *, template: NameTemplate) -> TempoSpread:
    """The tempo range of the collection, and how much of it could be read."""
    found: list[float] = []
    unreadable = 0
    for entry in view.entries:
        bpm = _bpm_of(entry.name, template=template)
        if bpm is None:
            unreadable += 1
        else:
            found.append(bpm)
    if not found:
        return TempoSpread(readable=0, unreadable=unreadable)
    return TempoSpread(
        readable=len(found),
        unreadable=unreadable,
        lowest=min(found),
        highest=max(found),
        median=_median(found),
    )


def genre_rows(view: LibraryView, *, declared: taxonomy.Taxonomy) -> tuple[GenreRow, ...]:
    """One row per folder directly under the governed tree, counting DISTINCT
    tracks through a set, since nothing stops a track being filed twice.
    """
    tree_display = declared.tree.display
    by_display = {bucket.display: bucket.id for bucket in declared.buckets}
    rows: list[GenreRow] = []
    for folder in view.folders:
        if len(folder) < 2 or folder[-2] != tree_display:
            continue
        tracks: set[str] = set()
        playlists = 0
        for playlist in view.playlists:
            if playlist.path[: len(folder)] != folder or len(playlist.path) <= len(folder):
                continue
            playlists += 1
            tracks.update(playlist.track_ids)
        rows.append(
            GenreRow(
                path=folder,
                tracks=len(tracks),
                playlists=playlists,
                bucket_id=by_display.get(folder[-1]),
            )
        )
    return tuple(sorted(rows, key=lambda row: row.path))


def _depth_under(path: tuple[str, ...], tree_display: str) -> int:
    """How deep ``path`` sits, counting the governed tree's own node as one.

    Measured from the FIRST occurrence of the tree, not the playlist root, so a
    tree filed inside another folder reports its true depth.
    """
    try:
        return len(path) - path.index(tree_display)
    except ValueError:  # pragma: no cover - callers filter to governed paths
        return 0


def tree_shape(view: LibraryView, *, declared: taxonomy.Taxonomy) -> TreeShape:
    """The declared depth beside the deepest path the GOVERNED tree holds; other
    trees are structures the template never claimed to describe.
    """
    tree_display = declared.tree.display
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]
    governed_playlists = [
        playlist.path for playlist in view.playlists if tree_display in playlist.path[:-1]
    ]
    deepest = max(
        (_depth_under(path, tree_display) for path in (*governed_folders, *governed_playlists)),
        default=0,
    )
    return TreeShape(
        declared_depth=declared.tree_depth,
        deepest=deepest,
        folders=len(governed_folders),
        playlists=len(governed_playlists),
    )


def statistics(
    view: LibraryView, *, declared: taxonomy.Taxonomy, template: NameTemplate
) -> LibraryStatistics:
    """Describe one export in one call; not ``library`` or ``run``, by rule."""
    rows = genre_rows(view, declared=declared)
    declared_ids = {bucket.id for bucket in declared.buckets}
    present_ids = {row.bucket_id for row in rows if row.bucket_id is not None}
    return LibraryStatistics(
        tree_id=declared.tree.id,
        tree_display=declared.tree.display,
        entries=len(view.entries),
        genres=rows,
        tempo=tempo_spread(view, template=template),
        shape=tree_shape(view, declared=declared),
        gaps=Gaps(
            undeclared_folders=tuple(row.path for row in rows if row.bucket_id is None),
            unused_buckets=tuple(sorted(declared_ids - present_ids)),
            entries_without_head=sum(
                1 for entry in view.entries if parse_head(entry.name, template=template) is None
            ),
            entries_in_no_playlist=sum(1 for entry in view.entries if not entry.playlists),
        ),
    )
