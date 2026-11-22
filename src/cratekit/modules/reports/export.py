"""The read-only view of a rekordbox export, recognized positively or refused.

Every locate is a primitive from ``cratekit.write.rbxml``, never a second parser
here: the byte engine already handles brackets inside attribute values, self
closed folders and multi line track elements, and a second reader would fail
silently where it did not.

A document that is not an export, or is truncated, would otherwise read as an
empty library and report a clean result. So each structure is checked and a
failure is refused with the structure named: the ``DJ_PLAYLISTS`` root; a
``COLLECTION`` section whose declared entry count AGREES with the tracks located
(the check that catches a half copied file); no ``TrackID`` twice (every later
answer is addressed by it); a ``PLAYLISTS`` section with its root node; and
every node declaring its kind. The kind is three valued, decided once by
``rbxml.node_kind``, because reading a node as "a playlist, or else a folder"
put misread nodes into ``folders`` and satisfied the guard meant to catch them.

Layer note: MODULES. It reads bytes a caller hands it and reaches nothing.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from cratekit.core.cause import Scope, refuse
from cratekit.write import rbxml

#: The document element of every export, matched as a lead because the version
#: attribute varies. Found anywhere ahead of COLLECTION, not at byte zero, since
#: a real export opens with an XML declaration and perhaps a byte order mark.
DOCUMENT_ELEMENT = "<DJ_PLAYLISTS"

#: The attribute the COLLECTION section declares its size with.
ENTRY_COUNT_ATTRIBUTE = "Entries"


@dataclass(frozen=True, slots=True)
class CollectionEntry:
    """One row of the collection, as the fields a report compares or shows.

    ``name`` carries the naming head; a caller wanting the title strips it
    through the DECLARED template, never a regular expression of its own.
    ``playlists`` is for REPORTING only and never part of an identity, since a
    tidy up would orphan a decision keyed on it. An export carries live rows
    only, so there is no soft delete marker.
    """

    track_id: str
    name: str
    artist: str
    location: str
    playlists: tuple[tuple[str, ...], ...] = ()


@dataclass(frozen=True, slots=True)
class Playlist:
    """One playlist node; its path excludes the playlist root, as ``rbxml`` builds it."""

    path: tuple[str, ...]
    track_ids: tuple[str, ...]

    @property
    def display(self) -> str:
        return self.path[-1] if self.path else ""


@dataclass(frozen=True, slots=True)
class LibraryView:
    """One export, read once and materialized, since reports walk it more than once.

    ``folders`` is what tells a structure that is absent from one present and
    empty: a folder holds no tracks, so it never appears in ``playlists``. There
    is no tuple for nodes of unreadable kind; ``read_export`` refuses first.
    """

    entries: tuple[CollectionEntry, ...]
    playlists: tuple[Playlist, ...]
    folders: tuple[tuple[str, ...], ...] = ()

    def has_folder(self, display: str) -> bool:
        """Whether any folder in the tree carries ``display``, at any depth."""
        return any(path and path[-1] == display for path in self.folders)

    def entry(self, track_id: str) -> CollectionEntry | None:
        """One entry by identifier. A LINEAR SCAN: index once for many lookups."""
        for found in self.entries:
            if found.track_id == track_id:
                return found
        return None


def _unusable(what: str, *, detail: dict[str, object] | None = None):
    """One refusal for every way this is not an export, naming the structure."""
    return refuse(
        "library-export-unusable",
        f"the collection export could not be read ({what}), so what it says about "
        f"the library is unknown; reading it as an empty library would report a "
        f"clean result over a document this build never understood",
        steps=("export the collection again from rekordbox and point the report at the new file",),
        scope=Scope.RUN,
        origin=("reports",),
        detail=dict(detail or {}, problem=what),
    )


def read_export_file(path: Path | str) -> LibraryView:
    """Read one export off disk, as bytes since every locate is a byte offset."""
    located = Path(path)
    try:
        content = located.read_bytes()
    except OSError as exc:
        raise _unusable("it could not be opened", detail={"path": located.name}) from exc
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
        # The sections must sit INSIDE the document element.
        raise _unusable("its COLLECTION section sits outside the document element")

    declared = _declared_entry_count(content, collection)
    tracks = rbxml.collection_tracks(content)
    if declared != len(tracks):
        raise _unusable(
            "its COLLECTION declares a different number of tracks than it holds",
            detail={"declared": declared, "located": len(tracks)},
        )

    repeated = sorted(
        track_id
        for track_id, seen in Counter(track.track_id for track in tracks).items()
        if seen > 1
    )
    if repeated:
        raise _unusable(
            "its COLLECTION carries the same TrackID more than once",
            detail={"repeated": repeated},
        )

    if rbxml.playlists_span(content) is None:
        raise _unusable("it carries no PLAYLISTS section")
    root = rbxml.root_node(content)
    if root is None:
        raise _unusable("its PLAYLISTS section has no root node")

    playlists, folders, unreadable = _read_nodes(content, root)
    if unreadable:
        raise _unusable(
            "its PLAYLISTS section carries a node whose kind it does not declare",
            detail={
                "nodes": [" / ".join(path) for path, _ in unreadable],
                "found": sorted({found for _, found in unreadable}),
            },
        )
    return LibraryView(
        entries=_read_entries(content, tracks, playlists),
        playlists=playlists,
        folders=folders,
    )


def _declared_entry_count(content: bytes, collection: tuple[int, int]) -> int:
    """The COLLECTION section's own count, searched only up to the first track,
    since a track's display name can contain the attribute name.
    """
    open_start, close_start = collection
    first_track = content.find(b"<TRACK", open_start, close_start)
    limit = first_track if first_track != -1 else close_start
    span = rbxml.attribute_span(content, ENTRY_COUNT_ATTRIBUTE, start=open_start, end=limit)
    if span is None:
        raise _unusable("its COLLECTION section declares no entry count")
    raw = content[span[0] : span[1]].decode("utf-8", "replace")
    try:
        return int(raw)
    except ValueError as exc:
        raise _unusable(
            "its COLLECTION entry count is not a number", detail={"found": raw}
        ) from exc


def _read_nodes(
    content: bytes, root: rbxml.NodeSpan
) -> tuple[
    tuple[Playlist, ...],
    tuple[tuple[str, ...], ...],
    tuple[tuple[tuple[str, ...], str], ...],
]:
    """Every node under the root as playlists, folders and unreadable nodes (with
    the ``Type`` seen), each with its display path. The root is located by
    position and never classified.
    """
    playlists: list[Playlist] = []
    folders: list[tuple[str, ...]] = []
    unreadable: list[tuple[tuple[str, ...], str]] = []
    for path, node in rbxml.walk_nodes(content, root):
        kind = rbxml.node_kind(node.node_type)
        if kind == rbxml.KIND_PLAYLIST:
            playlists.append(Playlist(path=path, track_ids=rbxml.track_keys(content, node)))
        elif kind == rbxml.KIND_FOLDER:
            folders.append(path)
        else:
            unreadable.append((path, node.node_type))
    return tuple(playlists), tuple(folders), tuple(unreadable)


def _read_entries(
    content: bytes,
    tracks: tuple[rbxml.TrackSpan, ...],
    playlists: tuple[Playlist, ...],
) -> tuple[CollectionEntry, ...]:
    """The collection rows, each with the playlist paths holding it, indexed ONCE."""
    placements: dict[str, list[tuple[str, ...]]] = {}
    for playlist in playlists:
        for track_id in playlist.track_ids:
            placements.setdefault(track_id, []).append(playlist.path)

    return tuple(
        CollectionEntry(
            track_id=track.track_id,
            name=(found := rbxml.attributes(content, track)).get("Name", ""),
            artist=found.get("Artist", ""),
            location=found.get("Location", ""),
            playlists=tuple(placements.get(track.track_id, ())),
        )
        for track in tracks
    )


__all__ = [
    "DOCUMENT_ELEMENT",
    "ENTRY_COUNT_ATTRIBUTE",
    "CollectionEntry",
    "LibraryView",
    "Playlist",
    "read_export",
    "read_export_file",
]
