"""The read-only view of a rekordbox export, recognized positively or refused.

Both reports in this package read one document: a collection export. This module
turns those bytes into values, once, and every locate it uses is a primitive from
``cratekit.write.rbxml`` rather than a parser written here. That reuse is not
tidiness. The byte engine already knows that an attribute value may contain an
angle bracket, that a childless folder is exported self closed and therefore has
no matching close tag, and that a track element spans several lines in a real
export and one line in a minimal one. A second reader would have to learn all
three again, and the ones it failed to learn would fail silently, on somebody
else's library.

**WHY THIS REFUSES INSTEAD OF RETURNING AN EMPTY LIBRARY.** The failure this
module is built against is the one U11's decision store shipped: a reader that
could not tell a wrong document from an empty one. There, only a parse error was
caught, so every document that was well formed and was not the store read as
"nothing is suppressed", and the next write then destroyed the file. The shape of
the mistake transfers exactly. A duplicate audit handed a file that is not an
export, or an export truncated by a failed copy, would find no collection tracks,
report no duplicates, and look identical to a clean library. Nobody would ever
find out, because the correct answer for a clean library is also nothing.

So the document is recognized POSITIVELY, one structure at a time, and anything
that fails a check is refused with the structure named:

1. the ``DJ_PLAYLISTS`` root element, which is what makes this an export at all;
2. a ``COLLECTION`` section;
3. a declared entry count on that section;
4. a ``PLAYLISTS`` section;
5. the playlist root node inside it;
6. and the declared entry count AGREES with the number of track elements
   located. That last one is the check that catches a half copied file. The count
   is written by whatever produced the document, so a document where the two
   disagree was either truncated or edited by something that did not maintain it,
   and in both cases the tracks this module can see are not the library.

Layer note: MODULES. It reads bytes a caller hands it and reaches nothing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cratekit.core.cause import Scope, refuse
from cratekit.write import rbxml

#: The document element every rekordbox export carries. Matched as a lead rather
#: than parsed, because the version attribute varies and the question here is
#: only "is this the format".
#:
#: It is looked for anywhere ahead of the COLLECTION section rather than at byte
#: zero. A real export opens with an XML declaration, and possibly a byte order
#: mark, so a check anchored at the start of the file would refuse every
#: document rekordbox actually writes.
DOCUMENT_ELEMENT = "<DJ_PLAYLISTS"

#: The attribute the COLLECTION section declares its size with.
ENTRY_COUNT_ATTRIBUTE = "Entries"


@dataclass(frozen=True, slots=True)
class CollectionEntry:
    """One row of the collection, as the fields a report compares or shows.

    ``name`` is the rekordbox display field and carries this library's naming
    head, so a caller that wants the title alone strips the head through the
    DECLARED template rather than through a regular expression of its own. That
    is not a detail: the source system's set builder hardcoded ``key - bpm -
    title``, did not know about the lossy marker, and therefore matched nothing
    for every marked file.

    ``playlists`` is where this entry sits in the tree, as full display paths. It
    is carried for REPORTING and is never part of any identity: a person judging
    two entries needs to see that one is filed under one folder and one under
    another, and a decision keyed on that would be orphaned by the next tidy up.

    There is no soft-delete marker here, and its absence is a fact about the
    format rather than an omission. ``trees.ContentRow`` requires one because a
    database row can be a tombstone; an export carries live rows only, so there
    is no marker to read and no permissive default to get wrong.
    """

    track_id: str
    name: str
    artist: str
    location: str
    playlists: tuple[tuple[str, ...], ...] = ()


@dataclass(frozen=True, slots=True)
class Playlist:
    """One playlist node, with the display path that reaches it.

    The path excludes the playlist root's own name, exactly as ``rbxml`` builds
    it, because the root is a constant of the format rather than part of any tree
    somebody named.
    """

    path: tuple[str, ...]
    track_ids: tuple[str, ...]

    @property
    def display(self) -> str:
        return self.path[-1] if self.path else ""


@dataclass(frozen=True, slots=True)
class LibraryView:
    """One export, read once, as the two things a report asks about.

    Materialized rather than generated. Both reports walk the entries more than
    once, and an iterable consumed once and reused is how U18's row index came to
    report every track absent while the run reported clean.
    """

    entries: tuple[CollectionEntry, ...]
    playlists: tuple[Playlist, ...]

    def entry(self, track_id: str) -> CollectionEntry | None:
        """One entry by identifier, for a caller holding exactly one.

        A LINEAR SCAN, and the hazard is stated rather than hidden: calling this
        once per entry is a walk of the collection per entry, which on a real
        library is the N times M shape U18 shipped and then had to remove. Both
        reports here index once and read the index, and anything that needs
        every entry should do the same rather than reach for this.
        """
        for found in self.entries:
            if found.track_id == track_id:
                return found
        return None


def _unusable(what: str, *, detail: dict[str, object] | None = None):
    """One refusal for every way this document is not a collection export.

    The sentence differs per structure because that is the half a person can act
    on: "this is not an export" and "this export is truncated" send somebody to
    two different places. The remediation is the same in every case, since the
    answer is always to produce the document again from rekordbox.
    """
    return refuse(
        "library-export-unusable",
        f"the collection export could not be read ({what}), so what it says about "
        f"the library is unknown; reading it as an empty library would report a "
        f"clean result over a document this build never understood",
        steps=(
            "export the collection again from rekordbox and point the report at "
            "the new file",
        ),
        scope=Scope.RUN,
        origin=("reports",),
        detail=dict(detail or {}, problem=what),
    )


def read_export_file(path: Path | str) -> LibraryView:
    """Read one export off disk. The only file this package ever opens.

    Bytes rather than text, because every locate downstream is a byte offset and
    decoding first would move all of them.
    """
    located = Path(path)
    try:
        content = located.read_bytes()
    except OSError as exc:
        raise _unusable(
            "it could not be opened", detail={"path": located.name}
        ) from exc
    return read_export(content)


def read_export(content: bytes) -> LibraryView:
    """Recognize a collection export, or refuse naming what is missing."""
    document_at = content.find(DOCUMENT_ELEMENT.encode("utf-8"))
    if document_at == -1:
        raise _unusable("it is not a rekordbox collection export")

    collection = rbxml.collection_span(content)
    if collection is None:
        raise _unusable("it carries no COLLECTION section")
    if collection[0] < document_at:
        # The sections have to sit INSIDE the document element. A file that
        # carries both in the wrong order is not an export that lost something,
        # it is something else that happens to contain both names.
        raise _unusable("its COLLECTION section sits outside the document element")

    declared = _declared_entry_count(content, collection)
    tracks = rbxml.collection_tracks(content)
    if declared != len(tracks):
        raise _unusable(
            "its COLLECTION declares a different number of tracks than it holds",
            detail={"declared": declared, "located": len(tracks)},
        )

    if rbxml.playlists_span(content) is None:
        raise _unusable("it carries no PLAYLISTS section")
    root = rbxml.root_node(content)
    if root is None:
        raise _unusable("its PLAYLISTS section has no root node")

    playlists = _read_playlists(content, root)
    return LibraryView(
        entries=_read_entries(content, tracks, playlists),
        playlists=playlists,
    )


def _declared_entry_count(content: bytes, collection: tuple[int, int]) -> int:
    """The COLLECTION section's own count, bounded to its open tag.

    The search window ends at the first track element rather than at the end of
    the section. Scanning the whole section for the attribute name would find one
    inside a track's own display name, which is a value a user chose and can
    therefore contain anything at all.
    """
    open_start, close_start = collection
    first_track = content.find(b"<TRACK", open_start, close_start)
    limit = first_track if first_track != -1 else close_start
    span = rbxml.attribute_span(
        content, ENTRY_COUNT_ATTRIBUTE, start=open_start, end=limit
    )
    if span is None:
        raise _unusable("its COLLECTION section declares no entry count")
    raw = content[span[0] : span[1]].decode("utf-8", "replace")
    try:
        return int(raw)
    except ValueError as exc:
        raise _unusable(
            "its COLLECTION entry count is not a number", detail={"found": raw}
        ) from exc


def _read_playlists(content: bytes, root: rbxml.NodeSpan) -> tuple[Playlist, ...]:
    """Every playlist node under the root, with its display path.

    Folders are walked through and not returned. A folder holds nodes rather than
    tracks, so it has no membership to report, and returning both kinds would
    make every consumer re-ask which one it was holding.
    """
    return tuple(
        Playlist(path=path, track_ids=rbxml.track_keys(content, node))
        for path, node in rbxml.walk_nodes(content, root)
        if node.node_type == rbxml.PLAYLIST_TYPE
    )


def _read_entries(
    content: bytes,
    tracks: tuple[rbxml.TrackSpan, ...],
    playlists: tuple[Playlist, ...],
) -> tuple[CollectionEntry, ...]:
    """The collection rows, each carrying the playlist paths that hold it.

    The placement index is built ONCE and read per entry. Rebuilding it per entry
    is an N times M walk over a real library, and worse than slow: the same shape
    in U18's tree writer silently matched nothing after the first entry whenever
    the rows arrived as a cursor.
    """
    placements: dict[str, list[tuple[str, ...]]] = {}
    for playlist in playlists:
        for track_id in playlist.track_ids:
            placements.setdefault(track_id, []).append(playlist.path)

    out: list[CollectionEntry] = []
    for track in tracks:
        found = rbxml.attributes(content, track)
        out.append(
            CollectionEntry(
                track_id=track.track_id,
                name=found.get("Name", ""),
                artist=found.get("Artist", ""),
                location=found.get("Location", ""),
                playlists=tuple(placements.get(track.track_id, ())),
            )
        )
    return tuple(out)


__all__ = [
    "DOCUMENT_ELEMENT",
    "ENTRY_COUNT_ATTRIBUTE",
    "CollectionEntry",
    "LibraryView",
    "Playlist",
    "read_export",
    "read_export_file",
]
