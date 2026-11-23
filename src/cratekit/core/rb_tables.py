"""The additive whitelist's tables and the writable-column registry, part of :mod:`cratekit.core.rb_writer`.

Read them through ``rb_writer``, which re-exports every name here. Data, not logic: the
tables are value for value what the writer judged against before the split (U300).
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Iterable, Iterator, Mapping

#: Parent identifiers meaning "top-level tag category": the schema has used all four spellings.
ROOT_PARENT_SENTINELS = ("", "0", "root", "None")

#: The content table, named once so the judge and the registry cannot disagree.
CONTENT_TABLE = "djmdContent"

#: The lookup tables a landing links a row's artist, album and genre to (U163).
ARTIST_TABLE = "djmdArtist"
ALBUM_TABLE = "djmdAlbum"
GENRE_TABLE = "djmdGenre"
LOOKUP_TABLES: tuple[str, ...] = (ARTIST_TABLE, ALBUM_TABLE, GENRE_TABLE)

#: Tables a writer may CREATE rows in. ANY unlisted table is refused, so grid and analysis
#: rows are structurally impossible (R17). Static, never feature-derived. THE CONTENT TABLE
#: STAYS OUT: only the native landing creates one, by naming it in ``creations`` (R-746).
PERMITTED_ROW_TABLES = frozenset(
    {"djmdPlaylist", "djmdSongPlaylist", "djmdMyTag", "djmdSongMyTag", "djmdKey"}
)

#: Analysis columns a row THIS PRODUCT CREATES may never declare (W3). An honest list, not a
#: derivation (P4); a test holds every name to a real content column.
GRIDLESS_ON_CREATE_COLUMNS = frozenset(
    {
        "BPM",
        "Analysed",
        "AnalysisDataPath",
        "AnalysisUpdated",
        "CueUpdated",
    }
)

#: What a CONTENT row this product creates must leave for rekordbox's analysis to fill (A8):
#: the five above, the key (never authored), the sample and rate columns, and the artwork.
#: The same honest list and schema test.
CONTENT_ROW_EMPTY_COLUMNS = GRIDLESS_ON_CREATE_COLUMNS | frozenset(
    {
        "KeyID",
        "SampleRate",
        "BitRate",
        "BitDepth",
        "ImagePath",
    }
)

#: What rekordbox writes on every content row it makes and ``add_content`` leaves NULL
#: (R-923); without them a row will not load to a deck. EVERY VALUE IS THE COLUMN'S OWN
#: EMPTY, so a later fill-if-empty still reads it unset. None is an analysis column.
#: Measured, not derived, and held to real column names by the schema test.
CONTENT_ROW_DEFAULTS: Mapping[str, Any] = MappingProxyType(
    {
        "Rating": 0,
        "ColorID": "0",
        "DJPlayCount": 0,
        "DiscNo": 0,
        "DeliveryControl": "on",
        "SamplerTrackInfo": 0,
        "SamplerPlayOffset": 0,
        "SamplerGain": 0.0,
        "VideoAssociate": "0",
        "LyricStatus": 0,
        "ServiceID": 0,
        "ExtInfo": "null",
        "FileNameS": "",
        "Commnt": "",
        "Subtitle": "",
        "ReleaseDate": "",
        "ModifiedByRBM": "",
        "DeliveryComment": "",
        "Lyricist": "",
        "OrgFolderPath": "",
        "Reserved1": "",
    }
)

#: The tables an analysis pass writes rows into FOR a content row. A row this product creates
#: owns none, read from SQL before its commit.
CONTENT_ANALYSIS_TABLES: tuple[str, ...] = ("djmdCue", "djmdMixerParam", "contentFile")

#: Tables a commit may be ASKED to admit a CREATION in beyond the whitelist, and the whole of
#: them, by ``creations`` on one commit so every other writer keeps refusing them. Naming any
#: other table refuses. The content row still carries :data:`CONTENT_ROW_EMPTY_COLUMNS`,
#: judged in memory and from SQL. The lookup tables joined with U163 (R-921), minted only
#: for a word with no active row and linked in the same commit (A4).
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES})

#: The membership table, named once for the removal rule and its primitive.
MEMBERSHIP_TABLE = "djmdSongPlaylist"

#: The playlist and folder table, named once for the node removal (U111).
PLAYLIST_TABLE = "djmdPlaylist"

#: Tables a commit may be ASKED to admit a removal (a soft delete marker change) in, and the
#: whole of them, by ``removals``; naming another table refuses. A hard delete is only by
#: ``deletions`` (U288). The playlist table joined with U111, guarded by
#: :func:`remove_playlist_node` and :func:`assert_node_changes_confined`. Never content.
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})

#: The tables rekordbox's own Remove from Collection deletes a track's rows from OUTRIGHT,
#: content first (A178, A185); admitted only by ``deletions`` (U288). Not done here: the
#: orphaned artist and album rows, and the analysis folder.
COLLECTION_REMOVAL_TABLES: tuple[str, ...] = (
    CONTENT_TABLE,
    MEMBERSHIP_TABLE,
    "djmdCue",
    "contentCue",
    "contentFile",
    "djmdSongHistory",
    "djmdMixerParam",
)

#: The same tables as a set: what ``deletions`` may name. Static.
DELETABLE_TABLES = frozenset(COLLECTION_REMOVAL_TABLES)

#: The column a row of another table names a content row by.
CONTENT_REFERENCE_COLUMN = "ContentID"

#: The column a few tables name ANY row by (``imageFile``), asked too. ``uuidIDMap`` names
#: rows by ``CurrentID`` and is not asked.
TARGET_REFERENCE_COLUMN = "TargetID"

#: The registry row whose counter the binding advances at every commit.
LOCAL_UPDATE_COUNT = "localUpdateCount"

#: A membership row's position and its playlist reference, for the renumbering (R-1830).
TRACK_NUMBER_COLUMN = "TrackNo"
PLAYLIST_REFERENCE_COLUMN = "PlaylistID"

#: The session record key naming the rows a removal took out: a hard delete leaves no
#: marker for the deletion pass (R-1037).
RECORDED_REMOVALS_KEY = "collection_removed"

#: The collection row's columns a recorded removal keeps, read before the delete.
RECORDED_COLUMNS: tuple[str, ...] = (
    "ID",
    "FolderPath",
    "FileSize",
    "ArtistName",
    "Title",
    "ISRC",
    "RemixerName",
    "Subtitle",
)

#: What a node change may move on a playlist row it does not plan: a sibling's position.
_SIBLING_COLUMNS = frozenset({"Seq", "updated_at", "usn", "rb_local_usn"})

#: What a planned move may change on its own row.
_MOVED_COLUMNS = _SIBLING_COLUMNS | {"ParentID"}


class Ownership(StrEnum):
    """How strongly an operation owns a field: ``OWNED`` overwrites, ``FILL_IF_EMPTY`` spares a set value."""

    OWNED = "owned"
    FILL_IF_EMPTY = "fill_if_empty"


@dataclass(frozen=True, slots=True)
class FieldPolicy:
    """One operation's declared fields, and how strongly it owns each.

    Operations register themselves, so the writable set is the union of what is enabled (R14).
    """

    owner: str
    fields: Mapping[str, Ownership]


#: The baseline operation, the track colour write, so the guard is strict rather than vacuous.
TRACK_COLOR_POLICY = FieldPolicy(
    owner="track-color",
    fields=MappingProxyType({"ColorID": Ownership.OWNED}),
)

#: The repair of a row a landing created without rekordbox's defaults (R-923), registered by
#: it alone. FILL IF EMPTY with the column's own empty, so a set colour or rating is kept.
ROW_DEFAULTS_POLICY = FieldPolicy(
    owner="row-defaults",
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.FILL_IF_EMPTY)),
)

#: The column rekordbox keys a row's file by: THE FILE'S INODE AT IMPORT (U115, R-928). It
#: need not match today, but the binding's random 28 bit id never loads to a deck. NOT A
#: BOOKKEEPING COLUMN, which would blind the guard for every writer.
FILE_ID_COLUMN = "rb_file_id"

#: The upper bound of the binding's random id; past it, magnitude cannot tell random from stale.
BINDING_ID_LIMIT = 1 << 28

#: The repair of a row the binding gave a random file id (U115), registered by it alone.
#: OWNED: the value replaced is the binding's, never a person's.
FILE_ID_POLICY = FieldPolicy(
    owner="row-file-id",
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.OWNED}),
)

#: The full path of the row's audio file.
FOLDER_PATH_COLUMN = "FolderPath"

#: The one write that moves a row's file (U154, ``intake shelve``), registered by it alone,
#: since a path write is how a row points at nothing. OWNED: the file is renamed first.
SHELVE_POLICY = FieldPolicy(
    owner="shelve",
    fields=MappingProxyType({FOLDER_PATH_COLUMN: Ownership.OWNED}),
)

#: Set by ``add_content`` from the TRACK menu item and to one value by rekordbox, meaning
#: unknown (A32, R-928). NOT A BOOKKEEPING COLUMN; the probe owns it for its one commit.
CONTENT_LINK_COLUMN = "ContentLink"

#: The recording code: rekordbox stores empty text where the binding leaves NULL (A32).
ISRC_COLUMN = "ISRC"

#: THE COLUMNS THE ROW PROBE MAY WRITE, with each stored type (A32, R-928). ``AnalysisUpdated``
#: also differs but is an analysis column (R17), never written. Neither is bookkeeping.
ROW_PROBE_COLUMNS: Mapping[str, type] = MappingProxyType(
    {CONTENT_LINK_COLUMN: int, ISRC_COLUMN: str}
)

#: The owner a row probe registers its policy under.
ROW_PROBE_OWNER = "row-probe"


def row_probe_policy(columns: Iterable[str]) -> FieldPolicy:
    """The policy one probe commit registers: exactly the probe columns it writes, OWNED.

    Refuses a column outside :data:`ROW_PROBE_COLUMNS` with ``ValueError``.
    """
    wanted = set(columns)
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if outside:
        raise ValueError(f"not a row probe column: {sorted(outside)}")
    return FieldPolicy(
        owner=ROW_PROBE_OWNER,
        fields=MappingProxyType(dict.fromkeys(sorted(wanted), Ownership.OWNED)),
    )


_REGISTERED: dict[str, FieldPolicy] = {}


def register_field_policy(policy: FieldPolicy) -> None:
    """Declare one operation's fields; an unregistered operation writes nothing."""
    _REGISTERED[policy.owner] = policy


def reset_field_policies() -> None:
    """Return the registry to its baseline. For tests, and for a re-enabled profile."""
    _REGISTERED.clear()
    register_field_policy(TRACK_COLOR_POLICY)


def registered_field_policies() -> Mapping[str, FieldPolicy]:
    """Every operation currently permitted to write a content column."""
    return MappingProxyType(dict(_REGISTERED))


def content_writable_columns() -> frozenset[str]:
    """The union of every registered operation's declared fields, walked, never listed (P3)."""
    columns: set[str] = set()
    for policy in _REGISTERED.values():
        columns.update(policy.fields)
    return frozenset(columns)


reset_field_policies()


@contextmanager
def field_policies_for_commit(*policies: FieldPolicy) -> Iterator[None]:
    """Register the named policies for one commit, then restore the registry as it was (A32).

    A registration left behind would widen the guard for every later writer.
    """
    was = registered_field_policies()
    try:
        for policy in policies:
            register_field_policy(policy)
        yield
    finally:
        reset_field_policies()
        for policy in was.values():
            register_field_policy(policy)


#: Reported for an uninspectable object; outside every writable set, so it refuses.
UNINSPECTABLE = "<uninspectable>"

#: Reported for a re-parented row. Not an empty set, which would read as bookkeeping only:
#: it passes on a whitelisted table and refuses elsewhere.
MOVED = "<moved>"

#: Every spelling of "nobody wrote this" for a column an analysis pass fills. PUBLIC, so the
#: landing's read back uses the same notion of empty as the guard.
EMPTY_ON_CREATE: tuple[Any, ...] = (None, 0, 0.0, "", "0")

#: What "unset" means per column for fill-if-empty. An honest list, not a derivation (P4);
#: anything unnamed uses the two shared spellings.
FIELD_EMPTIES: Mapping[str, tuple[Any, ...]] = MappingProxyType(
    {
        "Title": (None, ""),
        "Rating": (None, "", 0, "0"),
        "GenreID": (None, "", 0, "0"),
        "KeyID": (None, "", 0, "0"),
        "ColorID": (None, "", 0, "0"),
    }
)
_DEFAULT_EMPTIES: tuple[Any, ...] = (None, "")
