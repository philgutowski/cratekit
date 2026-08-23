"""``report.library``: what this library actually contains, as one read-only answer.

The source system has no such report. It has a playlist scanner that prints
folder names, a genre auditor that prints unplaced tracks, and nothing at all
that says how big the collection is, which declared buckets have never been used,
or what tempo range the library actually spans. A person answering "do I have
enough deep house to play a two hour set" reads a folder in rekordbox and counts.

Four questions, and each one exists because its absence cost something:

**Genres.** One row per folder directly beneath the governed tree, counted by
DISTINCT track rather than by playlist membership. Summing the sub-playlists
double counts every track filed under two energy bands, and that is the number a
person would otherwise use to decide a folder is twice the size it is.

**Tempo spread.** Read from the naming head through the DECLARED template, never
through a pattern of this module's own. The source system's set builder hardcoded
``key - bpm - title``, did not know about the lossy marker, and therefore matched
nothing at all for every marked file; the number it produced was a confident
answer over a fraction of the library. Entries whose head cannot be read are
counted and reported rather than dropped, because "the spread of what I could
read" and "the spread of the library" are different claims and only one of them
is checkable.

**Tree shape.** The declared depth beside the deepest path the export actually
holds, with the folder and playlist counts. A tree deeper than the template
declares is the shape the XML bridge cannot write, and knowing that before a
write attempt is the difference between a report and an incident.

**Gaps.** Three of them, kept separate because they are answered by three
different acts: a declared bucket with no folder is a taxonomy nobody has grown
into, an entry with no readable head is a file the naming pass has not reached,
and an entry in no playlist at all is what ``audit.coverage`` reports in full.
The last is a COUNT here and a list there, deliberately: a summary that inlined
ten thousand track names would be a summary of nothing.

**Nothing here is a policy.** No threshold decides a library is too small, no
bucket is called under-used, and no tempo is called wrong. Every number is a fact
about the export, and the judgement belongs to the person reading it.

Layer note: MODULES. Gated by the ``reports`` toggle (R5), like the aging report
it sits beside.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import taxonomy
from cratekit.core.naming import NameTemplate, parse_head
from cratekit.modules.reports.export import LibraryView


@dataclass(frozen=True, slots=True)
class GenreRow:
    """One folder directly beneath the governed tree, and what it holds.

    ``bucket_id`` is None for a folder the taxonomy does not declare. That is not
    an error and is not reported as one: a person is allowed folders the template
    has never heard of, and the row exists so they can see which ones those are
    without the report deciding anything about them.
    """

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

    ``readable`` and ``unreadable`` are both carried, and the reason is the whole
    point of this type: a spread over 40 percent of a library is a real number
    about an unreal population, and a consumer that sees only the range cannot
    tell that case from a complete one.

    Every field is None when nothing was readable, rather than zero. Zero beats
    per minute is a value a head can genuinely carry, and collapsing "no data"
    into it is how an empty report renders as a library of stopped records.
    """

    readable: int = 0
    unreadable: int = 0
    lowest: float | None = None
    highest: float | None = None
    median: float | None = None


@dataclass(frozen=True, slots=True)
class TreeShape:
    """What the export's tree looks like beside what the template declares.

    ``deepest`` counts the governed tree's own node, so a template declaring
    depth 3 and an export whose deepest governed playlist path is three segments
    long agree. Measuring one of them from the root and the other from the tree
    is how two numbers that describe one structure come to disagree by one
    forever.
    """

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
    """The tempo written into one name's head, or None when there is not one.

    Parsed rather than pattern matched, and the value is taken as written: a head
    carrying ``124`` and one carrying ``124.0`` are one tempo, and normalizing
    through ``float`` is what makes them compare as one. A head with no ``bpm``
    field at all, which a template declaring the field optional can produce,
    answers None rather than raising, because an optional field that is absent is
    a name this template accepts.
    """
    fields = parse_head(name, template=template)
    if not fields:
        return None
    written = fields.get("bpm")
    if written is None:
        return None
    try:
        return float(written)
    except ValueError:  # pragma: no cover - the head pattern admits digits only
        return None


def _median(values: list[float]) -> float:
    """The middle value, averaged across the pair when the count is even.

    Written here rather than imported because the allowlist governing this
    package admits no module that provides one, and that restriction is the
    reason the package cannot reach a disk. Four lines is the price.
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
    """One row per folder sitting directly under the governed tree.

    DISTINCT TRACKS, counted through a set per folder. The energy bands under a
    genre are separate playlists and a track sits in exactly one of them today,
    but nothing in the format enforces that and the taxonomy's own ``single_sub``
    shape exists because some buckets do not band at all. A sum over the
    sub-playlists is right until the first library that files a track twice, and
    then it is wrong in the direction that looks like success.
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


def tree_shape(view: LibraryView, *, declared: taxonomy.Taxonomy) -> TreeShape:
    """The declared depth beside the deepest path the governed tree actually holds.

    Measured over the GOVERNED tree only. A catalog tree is declared with its own
    node and a person's own top-level folders are theirs; counting either one
    here would report a library as deeper than the template allows because of a
    structure the template never claimed to describe.
    """
    tree_display = declared.tree.display
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]
    governed_playlists = [
        playlist.path for playlist in view.playlists if tree_display in playlist.path[:-1]
    ]
    deepest = max((len(path) for path in (*governed_folders, *governed_playlists)), default=0)
    return TreeShape(
        declared_depth=declared.tree_depth,
        deepest=deepest,
        folders=len(governed_folders),
        playlists=len(governed_playlists),
    )


def statistics(
    view: LibraryView, *, declared: taxonomy.Taxonomy, template: NameTemplate
) -> LibraryStatistics:
    """Describe one export. The whole report, so a caller makes one call.

    NOT CALLED ``library``, which is the module's own name, and not called ``run``
    either. This repository already records what two things called ``run`` in one
    call path cost, and a function whose dotted path repeats its module reads as a
    package attribute rather than as a call at every site that uses it.
    """
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


__all__ = [
    "Gaps",
    "GenreRow",
    "LibraryStatistics",
    "TempoSpread",
    "TreeShape",
    "genre_rows",
    "statistics",
    "tempo_spread",
    "tree_shape",
]
