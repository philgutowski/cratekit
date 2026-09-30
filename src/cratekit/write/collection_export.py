"""A collection export written from database rows, in the shape the readers read (R-745).

WHAT WAS MISSING. Every verb that reads a Fresh Export had one source for it,
the application's own export menu, by hand, with the application open. The rows
that file is made of are rows this product already reads through a disposable
copy. This module turns those rows into the document, and opens nothing itself.

THE SHAPE IS THE READERS', NOT REKORDBOX'S, WHERE THE TWO DIFFER. The byte
readers in :mod:`cratekit.write.rbxml` are what every consuming verb goes
through, and three of their rules decide this file:

1. every line ends in a carriage return and a line feed, because an insert is
   placed two bytes ahead of a closing line and nothing checks what those two
   bytes are;
2. a folder with no children is written as an open line and a close line,
   where rekordbox writes it self closed, because a landing inserts a playlist
   into the intake folder and cannot insert into a tag with no body;
3. membership is one key element per line in the one spelling the membership
   reader matches, and anything else reads as an empty playlist.

NO TEMPO DATA IS CARRIED, AND THAT IS A DECISION RATHER THAN AN OMISSION. Every
row is written with the gridless constant and no tempo child element, whatever
the database holds for it. No verb reads a tempo off an export, so carrying one
would buy nothing, and a landing splices into this file and hands the result to
an import. The standing rule that nothing here writes a beat grid is absolute,
and the one way to prove a value safe is for it never to be written.

EVERY LOCATION IS WRITTEN WHERE THE FILE IS MOUNTED, NOT WHERE THE DATABASE
RECORDED IT (R-773). rekordbox records a path once, under the drive the database
was made on, and keeps recording it after the drive is renamed. Its own export
writes the current drive, and every verb that takes an export compares a
location with a path on this machine. So a recorded path goes through the one
resolver and the configured prefix rules on its way out, which is the rule
every other reader of the collection already applies. A file copied straight
from the rows named every track under a drive nothing mounts, and the import
proof matched none of them. A path under no rule is written as the database
holds it and counted, never dropped and never guessed at. So is a path whose
rule points somewhere a reader of this file would not read back as itself,
since the readers resolve a location through the same rules and the recorded
spelling is the one they can follow.

WHAT A REKORDBOX EXPORT CARRIES THAT THIS ONE DOES NOT is listed in the ledger
entry, and the ones a person would miss are the cue points, the tempo elements
and the colour. This file is for the verbs that read an export. It is not a
backup of anything.

Layer: write. It names no verb and no taxonomy display name.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.core import locations
from cratekit.core.cause import refuse
from cratekit.write import rbxml, trees
from cratekit.write.rbxml import xml_escape_attr

#: The name the playlist root carries in every export. A constant of the format
#: rather than a folder anybody declared, and no reader checks it.
ROOT_NAME = "ROOT"

#: The ``Attribute`` values the database gives a playlist row.
PLAYLIST_ATTRIBUTE = 0
FOLDER_ATTRIBUTE = 1
SMART_ATTRIBUTE = 4

#: Parent identifiers that mean "directly under the playlist root". The same
#: four spellings the writer's own lookups accept, restated because the writer
#: is a layer this module's readers must agree with and cannot import a private
#: name from.
ROOT_PARENTS = frozenset({"", "0", "root", "None"})

#: The export byte rekordbox spells for each star count. The database stores
#: stars, zero to five, and an export spells five stars 255.
STAR_BYTES: Mapping[int, int] = MappingProxyType(
    {0: 0, 1: 51, 2: 102, 3: 153, 4: 204, 5: 255}
)
_RATING_BYTES = frozenset(STAR_BYTES.values())

#: The container name an export spells for each file type the database codes.
KINDS: Mapping[int, str] = MappingProxyType(
    {1: "MP3 File", 4: "M4A File", 5: "FLAC File", 11: "WAV File", 12: "AIFF File"}
)

#: What opens the line that says who wrote this file. Matched as bytes by
#: :func:`provenance_of`, so it is spelled once.
PROVENANCE_LEAD = "cratekit-export"

_PROVENANCE = re.compile(rb"<!-- " + PROVENANCE_LEAD.encode("ascii") + rb" ((?:[^-]|-(?!->))*) -->")
_PROVENANCE_PAIR = re.compile(rb'([a-z-]+)="([^"]*)"')
_UNSAFE_IN_COMMENT = re.compile(r"[^A-Za-z0-9._:+ -]")
_HYPHEN_RUN = re.compile(r"-{2,}")
_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}")


@dataclass(frozen=True, slots=True)
class TrackRow:
    """One active collection row, as the fields the document spells.

    THERE IS NO TEMPO FIELD, so there is nothing for the emitter to write one
    from. A field that existed and was ignored would be one edit away from being
    interpolated.

    ``rating`` is the export byte, already folded from the stars the database
    stores. ``location`` is what the database recorded, a plain path or a
    location. :func:`render` resolves it to where the file is mounted, and the
    emitter encodes a plain path through the one encoder.
    """

    track_id: str
    name: str = ""
    artist: str = ""
    composer: str = ""
    album: str = ""
    genre: str = ""
    kind: str = ""
    size: int = 0
    total_time: int = 0
    disc_number: int = 0
    track_number: int = 0
    year: int = 0
    date_added: str = ""
    bit_rate: int = 0
    sample_rate: int = 0
    comments: str = ""
    play_count: int = 0
    rating: int = 0
    location: str = ""
    remixer: str = ""
    tonality: str = ""
    label: str = ""


@dataclass(frozen=True, slots=True)
class NodeRow:
    """One active playlist row: a folder, a playlist, or a kind this file omits.

    ``attribute`` is the database's own code and is never folded to a boolean,
    because a row that is neither a folder nor a playlist has to stay
    distinguishable from both. ``members`` is the playlist's content
    identifiers in stored order, tombstones already removed.
    """

    node_id: str
    parent_id: str
    name: str
    attribute: int
    seq: int
    members: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Provenance:
    """Who wrote the file, and what is known about the database it came from.

    THE DATABASE HOLDS NO APPLICATION VERSION, in any column this build reads.
    It holds its schema version. So the file says three things and labels each:
    the schema version read off the copy, the application version installed on
    this machine, and the version the recorded pin names. None of them is
    called "the version that last wrote the database", because nothing here can
    establish that. ``None`` is written as ``unknown`` and never left out, so a
    value that could not be read is told apart from a line that was truncated.
    """

    writer: str
    written: str
    schema: str | None = None
    installed: str | None = None
    pinned: str | None = None


@dataclass(frozen=True, slots=True)
class Omitted:
    """What the database held that the document does not, by reason.

    Counted rather than dropped silently. A file with fewer playlists than the
    library is either correct or truncated, and the counts are how a person
    tells which.
    """

    smart_playlists: tuple[str, ...] = ()
    unreachable_nodes: tuple[str, ...] = ()
    unreadable_kinds: tuple[str, ...] = ()
    dangling_members: int = 0
    unreadable_ratings: tuple[str, ...] = ()
    #: Collection rows and playlist names holding a character no XML document
    #: may carry, or a tab or a line break, each written as a space.
    normalised_text: tuple[str, ...] = ()
    #: Collection rows whose recorded location is neither a location nor an
    #: absolute path, a streamed track or a row with none, copied as recorded.
    not_file_paths: tuple[str, ...] = ()
    #: Collection rows recording a file under neither the library root nor any
    #: prefix rule, written as the database holds them (R-773).
    unmapped_paths: tuple[str, ...] = ()
    #: Where those rows are recorded, as each leading prefix and how many rows
    #: record it, most rows first. A drive that has gone dark is a new line
    #: here, where a bare count would hide it among rows that never resolve.
    unmapped_prefixes: tuple[tuple[str, int], ...] = ()
    #: Collection rows a prefix rule places somewhere a reader of this file
    #: would not read back as itself, written as the database holds them.
    left_to_rule: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Document:
    """The rendered bytes, and the counts they were written from."""

    content: bytes
    tracks: int
    folders: int
    playlists: int
    memberships: int
    omitted: Omitted
    #: Collection rows a prefix rule placed, written under the rule's target.
    remapped: int = 0


# ---------------------------------------------------------------------------
# Reading rows off an open handle
# ---------------------------------------------------------------------------


def _text(row: Any, name: str) -> str:
    value = getattr(row, name, None)
    return "" if value is None else str(value)


def _whole(row: Any, name: str) -> int:
    """One integer column, or zero when it holds nothing a count can be read from."""
    value = getattr(row, name, None)
    try:
        return int(value) if value is not None else 0
    except (TypeError, ValueError):
        return 0


def rating_byte(stars: Any) -> int | None:
    """The export byte for a stored rating, or None when it is on neither scale.

    A value already spelled as an export byte passes through, copied. None is
    the answer for anything else and the caller counts it, because writing such
    a row as unrated without saying so would tell a routing pass to rate it.
    """
    try:
        value = int(stars) if stars is not None else 0
    except (TypeError, ValueError):
        return None
    if value in STAR_BYTES:
        return STAR_BYTES[value]
    if value in _RATING_BYTES:
        return value
    return None


def _date_added(row: Any) -> str:
    """The day the row joined the collection, as the export spells a day.

    The stock date when it reads as a day, otherwise the day the row was
    created. Which of the two rekordbox exports is not measured here.

    THE FALLBACK IS THE DAY ON THIS MACHINE'S CLOCK. The database stores the
    creation time with its offset, and the day taken off it as stored is the
    day in Greenwich, which for an evening import is tomorrow.
    """
    stock = _text(row, "StockDate")
    if _DAY.match(stock):
        return stock[:10]
    created = getattr(row, "created_at", None)
    if created is None:
        return ""
    try:
        local = created.astimezone() if created.tzinfo is not None else created
        return local.date().isoformat()
    except AttributeError:
        text = str(created)
        return text[:10] if _DAY.match(text) else ""


def refuse_unusable_id(kind: str, identifier: str) -> None:
    """Refuse an identifier the membership reader could not read back.

    THE READERS MATCH DIGITS AND NOTHING ELSE. A key spelled any other way makes
    its playlist read as holding nothing, and a collection row spelled any other
    way is skipped when the next identifier is chosen, so the file would be
    written, would open, and would be wrong. Every identifier rekordbox assigns
    is digits, so this is a refusal about a database somebody else built.
    """
    if identifier.isascii() and identifier.isdigit():
        return
    raise refuse(
        "library-export-unusable",
        f"the {kind} row {identifier!r} has an identifier that is not digits, "
        f"and an export spelling it would read back with that row missing, so "
        f"no export was written",
        steps=("take the export from rekordbox for this library",),
        origin=("write.collection_export",),
        detail={"kind": kind, "identifier": identifier},
    )


#: The lookup tables a collection row names by identifier, as the handle's own
#: readers. Seven fields of a row resolve through these five.
LOOKUPS = ("get_artist", "get_album", "get_genre", "get_key", "get_label")


def _prime_lookups(db: Any) -> list[Any]:
    """Read each lookup table once, and hold the rows for as long as the read runs.

    WITHOUT THIS EVERY DISTINCT ARTIST IS ITS OWN QUERY. A row's artist, album,
    genre, key and label each resolve through a lazy relation, and a relation
    to a row the session has not met yet is one statement. On a library of ten
    thousand tracks that is several thousand statements against an encrypted
    file. A row the session already holds resolves with none, so the tables
    are read whole, five statements, and the rows are kept referenced because
    the session holds them weakly.
    """
    held: list[Any] = []
    for name in LOOKUPS:
        reader = getattr(db, name, None)
        if reader is not None:
            held.append(list(reader()))
    return held


def read_tracks(db: Any) -> tuple[tuple[TrackRow, ...], tuple[str, ...]]:
    """Every active collection row, and the rows whose rating could not be read.

    A TOMBSTONE IS OMITTED, through the one reader of the marker, which refuses
    a row that cannot say whether it is one. An export carries live rows only.

    THE STORED TEMPO IS NEVER READ. Not read and dropped: the column is not
    named anywhere in this module.
    """
    found: list[TrackRow] = []
    unrated: list[str] = []
    held = _prime_lookups(db)
    for row in db.get_content():
        if trees.soft_delete_marker(row):
            continue
        track_id = str(row.ID)
        refuse_unusable_id("collection", track_id)
        rating = rating_byte(getattr(row, "Rating", None))
        if rating is None:
            unrated.append(track_id)
            rating = 0
        found.append(
            TrackRow(
                track_id=track_id,
                name=_text(row, "Title"),
                artist=_text(row, "ArtistName"),
                composer=_text(row, "ComposerName"),
                album=_text(row, "AlbumName"),
                genre=_text(row, "GenreName"),
                kind=KINDS.get(_whole(row, "FileType"), ""),
                size=_whole(row, "FileSize"),
                total_time=_whole(row, "Length"),
                disc_number=_whole(row, "DiscNo"),
                track_number=_whole(row, "TrackNo"),
                year=_whole(row, "ReleaseYear"),
                date_added=_date_added(row),
                bit_rate=_whole(row, "BitRate"),
                sample_rate=_whole(row, "SampleRate"),
                comments=_text(row, "Commnt"),
                play_count=_whole(row, "DJPlayCount"),
                rating=rating,
                location=_text(row, "FolderPath"),
                remixer=_text(row, "RemixerName"),
                tonality=_text(row, "KeyName"),
                label=_text(row, "LabelName"),
            )
        )
    del held
    found.sort(key=lambda track: (int(track.track_id), track.track_id))
    return tuple(found), tuple(unrated)


def read_nodes(db: Any) -> tuple[NodeRow, ...]:
    """Every active playlist row, each playlist with its members in stored order.

    THE MEMBERSHIP TABLE IS READ ONCE and grouped, never once per playlist. A
    library holds a few hundred playlists and tens of thousands of membership
    rows, and a query per playlist is a few hundred walks of that table.

    A TOMBSTONED MEMBERSHIP IS OMITTED, as a tombstoned playlist is. Whether a
    member still names a live collection row is the emitter's question, since
    it is the one that holds the collection.
    """
    members: dict[str, list[tuple[int, str, str]]] = {}
    for song in db.get_playlist_songs():
        if trees.soft_delete_marker(song):
            continue
        members.setdefault(str(song.PlaylistID), []).append(
            (_whole(song, "TrackNo"), str(song.ID), str(song.ContentID))
        )

    found: list[NodeRow] = []
    for row in db.get_playlist():
        if trees.soft_delete_marker(row):
            continue
        node_id = str(row.ID)
        found.append(
            NodeRow(
                node_id=node_id,
                parent_id=_text(row, "ParentID"),
                name=_text(row, "Name"),
                attribute=_attribute(row),
                seq=_whole(row, "Seq"),
                members=tuple(
                    content_id for _order, _row_id, content_id in sorted(members.get(node_id, ()))
                ),
            )
        )
    return tuple(found)


#: What a playlist row's kind is recorded as when it could not be read. It is
#: none of the three codes the database uses, so the row is omitted and named.
UNREADABLE_ATTRIBUTE = -1


def _attribute(row: Any) -> int:
    """A playlist row's kind, or the unreadable code, and never a default kind.

    ZERO IS A PLAYLIST, so a reader that answered zero for a value it could not
    parse would write every such row as a playlist holding nothing.
    """
    value = getattr(row, "Attribute", None)
    if value is None or isinstance(value, bool):
        return UNREADABLE_ATTRIBUTE
    try:
        return int(value)
    except (TypeError, ValueError):
        return UNREADABLE_ATTRIBUTE


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _location(recorded: str) -> str:
    """The location attribute for one row's path, recorded or already mounted.

    A value that is already a location is copied. A plain path goes through the
    one encoder, because a second encoder is the byte mismatch that makes an
    import add a second row for a file the collection already holds.
    """
    if is_file_path(recorded):
        return locations.location_url(recorded)
    return clean_text(recorded)


def is_file_path(recorded: str) -> bool:
    """Whether the database recorded an absolute path, the one thing to encode.

    ANYTHING ELSE IS COPIED AS RECORDED. A location is already encoded. A
    streamed track records a provider's own reference, and the encoder would
    dress that as a file on this machine, which a reader then reports as a file
    that has gone missing.
    """
    return recorded.startswith("/") and not locations.looks_like_location(recorded)


def is_located(recorded: str) -> bool:
    """Whether what the database recorded names a file at all, by either spelling."""
    return is_file_path(recorded) or (
        bool(recorded) and locations.looks_like_location(recorded)
    )


class Mounting(Enum):
    """How one recorded location is written (R-773)."""

    #: Under the library root, or naming no file on this machine. Copied.
    AS_RECORDED = "as_recorded"
    #: A rule places it, and the place reads back as itself. Rewritten.
    PLACED = "placed"
    #: A rule places it somewhere a reader would not read back. Copied.
    LEFT_TO_ITS_RULE = "left_to_its_rule"
    #: Under neither the root nor any rule. Copied, and counted.
    UNDER_NO_RULE = "under_no_rule"


@dataclass(frozen=True, slots=True)
class Mounted:
    """What is written for one recorded location, and why."""

    location: str
    mounting: Mounting
    #: The leading prefix of a path under no rule, as the resolver names it.
    prefix: str | None = None


def mounted_location(
    recorded: str, *, root: Path | str, prefix_map: Sequence[locations.PrefixRule]
) -> Mounted:
    """What is written for one recorded location, and how it resolved (R-773).

    THE ONE DECODE AND RESOLVE STEP, NOT A SECOND ONE. ``trees.located`` is what
    doctor's survey and every routing pass read a row through, so the file and
    the ``library.paths_resolved`` note count the same rows as under no rule.

    ONLY A ROW A RULE PLACED IS REWRITTEN. A row under the library root is
    handed back as recorded, byte for byte, and so is a row under no rule,
    which the caller counts. An export that swapped in the current root
    without being told to would be inventing a fact.

    AND ONLY WHEN THE PLACE READS BACK AS ITSELF. The verbs that take this
    file resolve each location through the same root and the same rules. A
    path under the library root resolves to itself. A path a rule sends to a
    second volume does not, unless a rule maps that volume onto itself, and
    written there it would resolve under no rule at all, where the recorded
    spelling resolves through its rule as it always did. So does the target of
    one rule that a later rule moves again, and a target that is not an
    absolute path, which the configuration accepts. Each of those is left to
    its rule, written as the database holds it, which is also what rekordbox
    writes for a drive other than its own.

    A streamed track, a row with no path and a location naming another host
    name no file on this machine and are handed back as recorded. The first
    two are the resolver's own answer for a value that is not a path, so
    nothing here asks the question a second time.
    """
    try:
        _decoded, resolved = trees.located(recorded, root=root, prefix_map=prefix_map)
    except locations.LocationDecodeError:
        return Mounted(recorded, Mounting.AS_RECORDED)
    if resolved.resolution is locations.Resolution.UNMAPPED:
        return Mounted(recorded, Mounting.UNDER_NO_RULE, prefix=resolved.prefix)
    if resolved.resolution is locations.Resolution.REMAPPED and resolved.path is not None:
        read_back = locations.resolve_recorded_path(
            resolved.path, root=root, prefix_map=prefix_map
        )
        if read_back.path == resolved.path:
            return Mounted(resolved.path, Mounting.PLACED)
        return Mounted(recorded, Mounting.LEFT_TO_ITS_RULE)
    return Mounted(recorded, Mounting.AS_RECORDED)


#: Every character an XML 1.0 document may not carry, with the tab and the two
#: line breaks, which a document may carry and a parser folds to a space inside
#: an attribute. One space for each, so what is written is what is read back.
_NOT_ATTRIBUTE_TEXT = re.compile("[\x00-\x1f\ufffe\uffff\ud800-\udfff]")


def clean_text(value: str) -> str:
    """``value`` with every character an attribute cannot hold written as a space.

    THE BYTE READERS HERE WOULD TAKE THE CHARACTER AND REKORDBOX WOULD NOT. A
    control character in a title makes a document no parser accepts, and the
    file is read by this product, spliced into by a landing, and refused at the
    import. The caller counts the rows it changed.
    """
    return _NOT_ATTRIBUTE_TEXT.sub(" ", value)


_TEXT_FIELDS = (
    "name", "artist", "composer", "album", "genre", "kind", "date_added",
    "comments", "remixer", "tonality", "label",
)  # fmt: skip


def text_was_cleaned(track: TrackRow) -> bool:
    """Whether any text field of ``track`` is written differently from how it is held."""
    return any(clean_text(getattr(track, name)) != getattr(track, name) for name in _TEXT_FIELDS)


def track_element(track: TrackRow) -> str:
    """One collection row, gridless, in rekordbox's attribute order.

    THE TEMPO ATTRIBUTE IS A LITERAL IN THIS SOURCE, and the no beat grid suite
    holds it to being one. There is no child element, so there is no grid.
    """
    def escape(value: str) -> str:
        return xml_escape_attr(clean_text(value))

    refuse_unusable_id("collection", track.track_id)
    return (
        # THE IDENTIFIER AS IT IS HELD, never as a number. Membership is
        # written from the same string, and a leading zero dropped here would
        # leave a playlist naming a row the collection does not spell.
        f'    <TRACK TrackID="{track.track_id}" Name="{escape(track.name)}" '
        f'Artist="{escape(track.artist)}" Composer="{escape(track.composer)}"\r\n'
        f'           Album="{escape(track.album)}" Grouping="" '
        f'Genre="{escape(track.genre)}" Kind="{escape(track.kind)}" '
        f'Size="{int(track.size)}"\r\n'
        f'           TotalTime="{int(track.total_time)}" '
        f'DiscNumber="{int(track.disc_number)}" '
        f'TrackNumber="{int(track.track_number)}" '
        f'Year="{int(track.year)}" AverageBpm="0.00"\r\n'
        f'           DateAdded="{escape(track.date_added)}" '
        f'BitRate="{int(track.bit_rate)}" '
        f'SampleRate="{int(track.sample_rate)}" '
        f'Comments="{escape(track.comments)}"\r\n'
        f'           PlayCount="{int(track.play_count)}" Rating="{int(track.rating)}" '
        f'Location="{xml_escape_attr(_location(track.location))}"\r\n'
        f'           Remixer="{escape(track.remixer)}" '
        f'Tonality="{escape(track.tonality)}" '
        f'Label="{escape(track.label)}" Mix="">\r\n'
        f"    </TRACK>\r\n"
    )


def _comment_value(value: str | None) -> str:
    """One provenance value, made safe to sit inside a comment and a quoted pair.

    A comment may not hold two hyphens together and a quoted value may not hold
    a quote, so anything outside a small alphabet becomes a full stop, and so
    does a run of hyphens. The values are version strings and one timestamp,
    and none of them loses anything a reader needs.
    """
    if value is None or not str(value).strip():
        return "unknown"
    return _HYPHEN_RUN.sub(".", _UNSAFE_IN_COMMENT.sub(".", str(value).strip()))


def provenance_line(provenance: Provenance) -> str:
    """The comment that says this product wrote the file, and from what."""
    pairs = (
        ("writer", provenance.writer),
        ("written", provenance.written),
        ("database-schema", provenance.schema),
        ("application-installed", provenance.installed),
        ("application-pinned", provenance.pinned),
    )
    body = " ".join(f'{key}="{_comment_value(value)}"' for key, value in pairs)
    return f"<!-- {PROVENANCE_LEAD} {body} -->\r\n"


def provenance_of(content: bytes) -> dict[str, str] | None:
    """What a file says about who wrote it, or None when rekordbox wrote it.

    HOW A READER TELLS THE TWO APART. None is the answer for every export the
    application writes, since it writes no such line. It is read ahead of the
    document element only, so a comment somebody typed into a playlist name
    cannot answer for the file.
    """
    head = content[: max(0, content.find(b"<DJ_PLAYLISTS"))]
    match = _PROVENANCE.search(head)
    if match is None:
        return None
    return {
        key.decode("ascii"): value.decode("utf-8")
        for key, value in _PROVENANCE_PAIR.findall(match.group(1))
    }


def _product_version(provenance: Provenance) -> str:
    """The version the product line carries, which no reader reads."""
    for candidate in (provenance.installed, provenance.pinned):
        if candidate and str(candidate).strip():
            return _comment_value(candidate)
    return "0.0.0"


def _children(nodes: Iterable[NodeRow]) -> dict[str, list[NodeRow]]:
    """Each parent's children, in the order the database sequences them.

    Every root spelling is folded to one key. The identifier breaks a tie in
    the sequence, as a number, so two rows sharing a sequence come out in one
    order on every run.
    """
    grouped: dict[str, list[NodeRow]] = {}
    for node in nodes:
        parent = "" if node.parent_id in ROOT_PARENTS else node.parent_id
        grouped.setdefault(parent, []).append(node)
    for siblings in grouped.values():
        siblings.sort(key=lambda node: (node.seq, _ordinal(node.node_id), node.node_id))
    return grouped


def _ordinal(identifier: str) -> int:
    return int(identifier) if identifier.isascii() and identifier.isdigit() else 0


@dataclass(slots=True)
class _Tally:
    folders: int = 0
    playlists: int = 0
    memberships: int = 0
    dangling: int = 0


def _render_node(
    node: NodeRow,
    depth: int,
    grouped: Mapping[str, Sequence[NodeRow]],
    live: frozenset[str],
    written: set[str],
    tally: _Tally,
) -> str:
    """One folder or playlist and everything under it, as lines."""
    indent = rbxml.indent_at(depth)
    written.add(node.node_id)
    name = clean_text(node.name)
    if node.attribute == PLAYLIST_ATTRIBUTE:
        keys = [member for member in node.members if member in live]
        tally.dangling += len(node.members) - len(keys)
        tally.playlists += 1
        tally.memberships += len(keys)
        if not keys:
            return rbxml.empty_playlist(name, indent) + "\r\n"
        return (
            rbxml.playlist_open(name, len(keys), indent)
            + rbxml.track_key_lines(keys, rbxml.indent_at(depth + 1))
            + rbxml.node_close(indent)
        )

    tally.folders += 1
    body = [
        _render_node(child, depth + 1, grouped, live, written, tally)
        for child in _writable(grouped.get(node.node_id, ()))
    ]
    # OPEN AND CLOSE, EVEN WITH NOTHING BETWEEN THEM. rekordbox self closes a
    # childless folder. A landing inserts into the intake folder, and an intake
    # folder with nothing in it yet is the ordinary state of a new library.
    return rbxml.folder_open(name, len(body), indent) + "".join(body) + rbxml.node_close(indent)


def _writable(nodes: Iterable[NodeRow]) -> list[NodeRow]:
    """The nodes the document can spell: folders and playlists, nothing else."""
    return [node for node in nodes if node.attribute in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE)]


def render(
    tracks: Sequence[TrackRow],
    nodes: Sequence[NodeRow],
    provenance: Provenance,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
    unreadable_ratings: Sequence[str] = (),
) -> Document:
    """The whole document, and the counts it was written from.

    ``root`` AND ``prefix_map`` ARE REQUIRED, with no default, because a
    default is how a caller writes every location under a drive nothing mounts
    and is told nothing (R-773). A library with no rule passes an empty map
    and says so.

    THE DECLARED COUNTS ARE COUNTED FROM WHAT WAS WRITTEN, never carried from
    the query. The strict reader compares the collection's declared count with
    the rows it can locate and refuses a file where they differ, which is what
    catches a half copied export, so a count taken anywhere but from the lines
    themselves is a count that can disagree with them.

    A SMART PLAYLIST IS OMITTED AND NAMED. The database stores its rule and not
    its members, and a node whose kind the readers cannot classify makes the
    strict reader refuse the whole file. A NODE NOTHING REACHES FROM THE ROOT,
    its parent a tombstone or an omitted row, is omitted and named as well.
    """
    seen: set[str] = set()
    for track in tracks:
        if track.track_id in seen:
            raise refuse(
                "library-export-unusable",
                f"the collection holds the identifier {track.track_id!r} twice, "
                f"and an export carrying it twice is refused by every reader, so "
                f"no export was written",
                steps=("take the export from rekordbox for this library",),
                origin=("write.collection_export",),
                detail={"identifier": track.track_id},
            )
        seen.add(track.track_id)
    live = frozenset(seen)

    grouped = _children(nodes)
    written: set[str] = set()
    tally = _Tally()
    top = _writable(grouped.get("", ()))
    tree = "".join(_render_node(node, 1, grouped, live, written, tally) for node in top)

    smart = tuple(node.name for node in nodes if node.attribute == SMART_ATTRIBUTE)
    unreadable = tuple(
        node.name
        for node in nodes
        if node.attribute not in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE, SMART_ATTRIBUTE)
    )
    unreachable = tuple(
        node.name
        for node in _writable(nodes)
        if node.node_id not in written
    )
    normalised = tuple(track.track_id for track in tracks if text_was_cleaned(track)) + tuple(
        clean_text(node.name)
        for node in _writable(nodes)
        if node.node_id in written and clean_text(node.name) != node.name
    )
    unlocated = tuple(track.track_id for track in tracks if not is_located(track.location))

    # WHERE EACH FILE IS MOUNTED, resolved once per row and ahead of the
    # emitter, so the line and the counts are read off one answer.
    placed: list[TrackRow] = []
    unmapped: list[str] = []
    prefixes: Counter[str] = Counter()
    left: list[str] = []
    remapped = 0
    for track in tracks:
        mounted = mounted_location(track.location, root=root, prefix_map=prefix_map)
        if mounted.mounting is Mounting.PLACED:
            remapped += 1
            placed.append(replace(track, location=mounted.location))
            continue
        if mounted.mounting is Mounting.UNDER_NO_RULE:
            unmapped.append(track.track_id)
            prefixes[mounted.prefix or "?"] += 1
        elif mounted.mounting is Mounting.LEFT_TO_ITS_RULE:
            left.append(track.track_id)
        placed.append(track)

    root_indent = " " * rbxml.indent_at(0)
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        + provenance_line(provenance)
        + '<DJ_PLAYLISTS Version="1.0.0">\r\n'
        + f'  <PRODUCT Name="rekordbox" Version="{_product_version(provenance)}" '
        + 'Company="AlphaTheta"/>\r\n'
        + f'  <COLLECTION Entries="{len(tracks)}">\r\n'
        + "".join(track_element(track) for track in placed)
        + "  </COLLECTION>\r\n"
        + "  <PLAYLISTS>\r\n"
        + f'{root_indent}<NODE Type="{rbxml.FOLDER_TYPE}" Name="{ROOT_NAME}" '
        + f'Count="{len(top)}">\r\n'
        + tree
        + rbxml.node_close(rbxml.indent_at(0))
        + "  </PLAYLISTS>\r\n"
        + "</DJ_PLAYLISTS>\r\n"
    ).encode("utf-8")

    return Document(
        content=content,
        tracks=len(tracks),
        folders=tally.folders,
        playlists=tally.playlists,
        memberships=tally.memberships,
        omitted=Omitted(
            smart_playlists=smart,
            unreachable_nodes=unreachable,
            unreadable_kinds=unreadable,
            dangling_members=tally.dangling,
            unreadable_ratings=tuple(unreadable_ratings),
            normalised_text=normalised,
            not_file_paths=unlocated,
            unmapped_paths=tuple(unmapped),
            unmapped_prefixes=tuple(prefixes.most_common()),
            left_to_rule=tuple(left),
        ),
        remapped=remapped,
    )


__all__ = [
    "FOLDER_ATTRIBUTE",
    "KINDS",
    "PLAYLIST_ATTRIBUTE",
    "PROVENANCE_LEAD",
    "ROOT_NAME",
    "SMART_ATTRIBUTE",
    "UNREADABLE_ATTRIBUTE",
    "STAR_BYTES",
    "Document",
    "Mounted",
    "Mounting",
    "NodeRow",
    "Omitted",
    "Provenance",
    "TrackRow",
    "clean_text",
    "is_file_path",
    "is_located",
    "mounted_location",
    "provenance_of",
    "provenance_line",
    "rating_byte",
    "read_nodes",
    "read_tracks",
    "refuse_unusable_id",
    "render",
    "track_element",
]
