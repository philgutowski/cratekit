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
6. the declared entry count AGREES with the number of track elements located.
   That one is the check that catches a half copied file. The count is written
   by whatever produced the document, so a document where the two disagree was
   either truncated or edited by something that did not maintain it, and in both
   cases the tracks this module can see are not the library;
7. and no ``TrackID`` appears twice. An identifier is what every later answer is
   addressed by: a duplicate group offers one option per copy keyed on it, so
   two rows sharing one identifier produce two options a person cannot tell
   apart, and an ACCEPTED verdict naming that option says nothing about which
   copy survives. The deletion surface would then be licensed by an ambiguous
   answer, which is worse than no answer;
8. and every node in the playlist tree says which KIND it is. A node whose
   ``Type`` this build cannot read is the same shape as everything above it, and
   it hid behind the fact that the tree was split in two: the classification ran
   "a playlist, or else a folder", so a node whose kind was a question was
   answered FOLDER. Driven on this suite's own export, retyping the playlists
   dropped seven playlists to none, put all twelve nodes into ``folders``, and
   the intake report then rendered a clean queue. WORSE, THE MISREAD NODES
   SATISFIED THE GUARD WRITTEN TO CATCH THEIR LOSS: ``has_folder`` asks whether
   the intake display appears among the folders, and the misread intake
   groupings put their own paths there. The duplicate audit lost every placement
   in the same run and still reported the group, so a person was shown two
   copies of one recording and nothing about where either one lives.

That last one is why the kind is a THREE valued question, decided once by
``rbxml.node_kind`` and refused here, rather than a boolean each report guards
for itself. Site by site guarding is what this repository has already paid for
three times: the state "it is here and I could not read what is in it" has to be
representable, or a caller ends up choosing which of the two readable answers to
report it as.

Layer note: MODULES. It reads bytes a caller hands it and reaches nothing.
"""

from __future__ import annotations

from collections import Counter
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
    """One export, read once, as the three things a report asks about.

    Materialized rather than generated. Both reports walk the entries more than
    once, and an iterable consumed once and reused is how U18's row index came to
    report every track absent while the run reported clean.

    ``folders`` is carried for one reason and it is the same reason this module
    refuses rather than returning an empty view: WITHOUT IT, "the structure you
    asked about is not in this tree" and "it is here and it is empty" are the
    same answer. A folder holds no tracks, so it never appears in ``playlists``,
    and a report that only had the playlists could not tell an intake flow that
    has been emptied from one that was never exported. Both would render as a
    clean report with nothing to do, and only one of them is true.

    THERE IS NO THIRD TUPLE FOR THE NODES WHOSE KIND COULD NOT BE READ, and that
    is the point rather than an omission. A view holding them would make every
    consumer decide what to do about them, which is the site by site guarding
    that failed: the two tuples above were already a guard against a structure
    going missing, and misread nodes satisfied it by putting their own paths into
    ``folders``. ``read_export`` refuses before a view exists, so this type can
    only ever describe a tree whose every node said what it was.
    """

    entries: tuple[CollectionEntry, ...]
    playlists: tuple[Playlist, ...]
    folders: tuple[tuple[str, ...], ...] = ()

    def has_folder(self, display: str) -> bool:
        """Whether any folder in the tree carries ``display``, at any depth.

        Asked rather than derived from the playlist paths, because the whole
        point of holding the folders is the case where a folder has no playlists
        under it to derive from.
        """
        return any(path and path[-1] == display for path in self.folders)

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


def _read_nodes(
    content: bytes, root: rbxml.NodeSpan
) -> tuple[
    tuple[Playlist, ...],
    tuple[tuple[str, ...], ...],
    tuple[tuple[tuple[str, ...], str], ...],
]:
    """Every node under the root, split by kind, each with its display path.

    The kinds are returned SEPARATELY rather than as one list a consumer has to
    re-ask about. A folder holds nodes rather than tracks, so it has no
    membership to report and never becomes a ``Playlist``; what it does carry is
    the fact that it EXISTS, which is the only way to tell a structure that is
    absent from one that is present and empty.

    THERE ARE THREE KINDS AND NOT TWO, and the split used to be an ``else``. A
    node is a playlist, a folder, or a node this build could not read, and the
    third one arrives here as the ``Type`` value that produced it so the refusal
    can name what it saw. The third kind is carried out rather than decided here
    because this function's job is to say what is in the tree; whether an
    unreadable node is fatal is ``read_export``'s question, asked once for both
    reports.

    The root itself is not classified, and that is not the same hole. It is
    located by POSITION rather than by its kind, nothing downstream asks what
    kind it is, and it is not in the walk this iterates.
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
