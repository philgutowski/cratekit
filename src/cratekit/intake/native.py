"""Land a batch in the collection through the guarded database writer (R-746).

On a library whose intake tree has cut over: one content row per landed file
and one batch playlist under the adopted intake root, through the session
spine every database tree writer uses, behind a plan and an approval.

A CONTENT ROW IS THE ROW REKORDBOX ANALYSES INTO, so it carries only what the
file's tags and the filesystem say, asserted from SQL before the commit in
``rb_writer`` and read back after it here; every analysis column stays empty
(:data:`LEFT_EMPTY`). Its path is under the base drive, its device the
library's own (A8), its file id the landed file's inode (U115) and its
ContentLink the library's (U126): rekordbox will not load a row without them.

THE PLAN IS BUILT AGAINST THE DATABASE AND THE APPLY REBUILDS NOTHING: it asks
again only whether a row appeared since the approved digest. Each account
playlist gets its own INBOX playlist (U113), and every new row joins
:data:`ANALYZE` (U166). A row here is one this engine adds, unlike in
``cratekit.tagging.rows``.

The plan and the readers are in ``native_plan`` and the apply's steps in
``native_apply``, each reached through this module too; every name a test
patches here stays looked up here. Opens no database of its own.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

from cratekit.core import config, convergence, drift, rb_writer, session, tree_registry
from cratekit.core.cause import Remedy, refuse
from cratekit.favorites import colour as colour_mod
from cratekit.favorites import placement
from cratekit.intake import ingest, label_filing, set_playlist
from cratekit.write import metadata_cli, row_link, trees

if TYPE_CHECKING:
    # Annotation only: the module that defines them reaches this one.
    from cratekit.intake.account_playlists import Left, Member

#: What a planned row will do. A file the binding has no file type for is
#: UNSUPPORTED and left in staging alone, as an occupied target is; the batch lands.
ADD = "add"
PRESENT = "already present"
UNSUPPORTED = "unsupported"

#: The columns a landed row leaves for rekordbox. THE WRITER'S LIST, not a
#: copy: a second spelling is how what a person reads and what the guard
#: enforces come to differ.
LEFT_EMPTY: tuple[str, ...] = tuple(sorted(rb_writer.CONTENT_ROW_EMPTY_COLUMNS))

#: What the screen shows for the file id of a row to be added: a sentence,
#: because the number is read on the landed file when the row is made (U115).
FILE_ID_AT_LANDING = "the landed file's inode number, read when the row is made"

#: The session workflow a native landing is recorded under, the intake's own.
WORKFLOW = ingest.INTAKE_WORKFLOW

#: Record field naming the batch playlist a landing wrote, by id and name,
#: which ``inbox rotate`` ages it by.
BATCH_PLAYLIST_KEY = "batch_playlist"
#: Record field naming the batch a landing filed and its folder (U164), so a
#: batch landed again by its name goes back there and the name stays taken.
FILED_BATCH_KEY = "filed_batch"
#: Key on a batch playlist entry naming the set job it was written for (U135),
#: so a later landing of the same job adds to it under its first name.
INBOX_JOB_KEY = "job"
#: Record field naming the sync pass given with ``--pass`` (R-777), written
#: with the commit, so ``sync mark --pass`` reads it as proof the pass landed.
PASS_KEY = "pass"

#: Record field naming every row a landing made (R-1037): the database
#: identity, the update count the commit left, the playlists it made, and each
#: row's :data:`LANDED_COLUMNS` and UUID. rekordbox deletes a removed row
#: outright, so this record is the only place its file and identity are
#: written down. Spelled again in ``deletion.library``.
LANDED_ROWS_KEY = "collection_landed"
#: The field each landed row's UUID is kept under (R-1844): a fresh uuid4 no
#: database from before the landing holds, so a row still held under it proves
#: the landing was not rolled back. Spelled again in ``deletion.library``.
LANDED_UUID_KEY = "uuid"
#: The columns a landed row is named by, ``rb_writer.RECORDED_COLUMNS``
#: spelled here so this package reaches no further into the core.
LANDED_COLUMNS: tuple[str, ...] = (
    "ID",
    "FolderPath",
    "FileSize",
    "ArtistName",
    "Title",
    "ISRC",
    "RemixerName",
    "Subtitle",
)

#: Record field listing the account playlists a landing wrote (U113).
INBOX_PLAYLISTS_KEY = ingest.INBOX_PLAYLISTS_KEY

#: The playlist under the intake root every row a landing creates joins
#: (U166), so the rekordbox visit selects one playlist. Reserved: no batch may
#: take it and an account playlist of the name lands dated (U175).
#: ``batch_name.ANALYZE`` spells it again, held equal by a test.
ANALYZE = "Analyze"

#: Why a playlist member is not in its INBOX playlist when its file made no row (U128).
NOT_LANDED = "its file did not land"

#: Why a landing plans no vox My Tag (U127). Without a calibration there is
#: no cut to read a score against, and a tag from the default cut would file
#: a vocal sub the derivation never would.
VOX_UNCALIBRATED = (
    "the library has no vocal calibration, so no score can be read against a cut; "
    "run crate analyze calibrate and then crate metadata mytags-vocals --apply"
)
#: No My Tag category for the writer to copy a row's shape from.
VOX_NO_CATEGORY = (
    "the library holds no My Tag category to copy a new one's shape from, so the "
    "Vocals category cannot be made; make any My Tag in rekordbox and then run "
    "crate metadata mytags-vocals --apply"
)
#: The calibration is there and cannot be read.
VOX_UNREADABLE = (
    "the vocal calibration could not be read ({why}), so no score can be read against "
    "a cut; run crate analyze calibrate again and then crate metadata mytags-vocals --apply"
)

#: The My Tag every added row whose drift reads variable gets (U157), so
#: Analyze Tracks selects those rows for Dynamic. ``analysis.rekordbox_check``
#: imports it, so the check and the landing cannot disagree.
DYN_VALUE = "dyn"
DYN_CATEGORY = "Analysis"
#: What the dyn tags are filed under in a record's change summary (R19).
DYN_CHANGE_KEY = "my-tags.analysis"
#: Why no variable row is given the dyn My Tag, asked before the gate.
DYN_NO_CATEGORY = (
    "the library holds no My Tag category to copy a new one's shape from, so the "
    "Analysis category cannot be made; make any My Tag in rekordbox and run the "
    "rows this landing names with Analysis Mode Dynamic by hand"
)

_ORIGIN = ("intake.native",)

logger = logging.getLogger(__name__)

#: The content columns a landing links to a lookup row (U163), the year
#: column, and the album's own artist, read back beside the row's words.
ARTIST_COLUMN = "ArtistID"
ALBUM_COLUMN = "AlbumID"
GENRE_COLUMN = "GenreID"
YEAR_COLUMN = "ReleaseYear"
ALBUM_ARTIST = "AlbumArtistID"

#: What the screen and the digest show for a word the commit mints a row for (U163).
MINTED = "mint"


@dataclass(frozen=True, slots=True)
class Word:
    """One artist, album or genre word a row to be added carries, and the lookup row it takes (U163).

    THE FIRST ACTIVE ROW BY EXACT NAME, or a row the commit mints, as Reload
    Tags did. An album is found by name and album artist together, so two
    albums of one name by two artists stay two.
    """

    table: str
    name: str
    #: The active row the plan found, empty when the commit mints one.
    row_id: str = ""
    #: The album artist an album word links, by its own artist word.
    album_artist: Word | None = None
    #: What a minted artist or album row stores in ``SearchStr``; None is NULL.
    search: str | None = None

    def key(self) -> tuple[str, str, str]:
        """What one commit mints once: the table, the name and an album's artist."""
        artist = self.album_artist.name if self.album_artist is not None else ""
        return (self.table, self.name, artist)

    def shown(self) -> dict[str, Any]:
        """The word, its row or ``mint``, and what a mint stores, for the screen and the digest."""
        shown: dict[str, Any] = {"name": self.name, "row": self.row_id or MINTED}
        if self.album_artist is not None:
            shown["album artist"] = self.album_artist.shown()
        if not self.row_id and self.table != rb_writer.GENRE_TABLE:
            shown["SearchStr"] = self.search
        return shown


@dataclass(frozen=True, slots=True)
class RowPlan:
    """One file, the row it would add, and every column that row would carry."""

    source: Path
    target: Path
    action: str
    title: str
    folder_path: str
    file_name: str
    file_size: int
    file_type: int
    #: The library's ContentLink (U126), set only on a row to be added.
    content_link: int | None
    #: The row already holding this file, when ``action`` is ``PRESENT``.
    content_id: str | None = None
    #: Why the file is planned as ``UNSUPPORTED``, in a sentence, else empty.
    why: str = ""
    #: The file's ``voxlevel`` (U127), None when unread, and whether the row
    #: is given the vox My Tag, its score clearing the cut.
    voxlevel: int | None = None
    vox: bool = False
    #: The file's drift, its verdict against the plan's cut (U157), and
    #: whether the row is given the dyn My Tag. Empty on a row not added.
    drift: float | None = None
    drift_verdict: str = ""
    dyn: bool = False
    #: The file's artist, album and genre words (U163), None for a word the
    #: file does not carry.
    artist: Word | None = None
    album: Word | None = None
    genre: Word | None = None
    #: The year of the file's date tag, written to ``ReleaseYear`` (U163).
    year: int | None = None

    def columns(self) -> dict[str, Any]:
        """Every column the writer sets on the row, by name, for the screen."""
        words = {column: word.shown() for column, word in self.linked() if word is not None}
        return {
            "Title": self.title,
            "FolderPath": self.folder_path,
            "FileNameL": self.file_name,
            "FileSize": self.file_size,
            "FileType": self.file_type,
            rb_writer.FILE_ID_COLUMN: FILE_ID_AT_LANDING,
            **(
                {rb_writer.CONTENT_LINK_COLUMN: self.content_link}
                if self.content_link is not None
                else {}
            ),
            **words,
            **({YEAR_COLUMN: self.year} if self.year is not None else {}),
        }

    def linked(self) -> tuple[tuple[str, Word | None], ...]:
        """Each column linked to a lookup row, and the word it takes (U163)."""
        return ((ARTIST_COLUMN, self.artist), (ALBUM_COLUMN, self.album), (GENRE_COLUMN, self.genre))

    def words(self) -> dict[str, Any]:
        """The words the row is planned to read back with, by column (U163)."""
        return {
            ARTIST_COLUMN: self.artist.name if self.artist is not None else "",
            ALBUM_COLUMN: self.album.name if self.album is not None else "",
            ALBUM_ARTIST: (
                self.album.album_artist.name
                if self.album is not None and self.album.album_artist is not None
                else ""
            ),
            GENRE_COLUMN: self.genre.name if self.genre is not None else "",
            YEAR_COLUMN: self.year,
        }


@dataclass(frozen=True, slots=True)
class PlaylistMember:
    """One track an account playlist's INBOX playlist holds (U128).

    A planned ``target``, or the ``content_id`` of a row the library held.
    ``member`` names it in the warning when its file does not land.
    """

    target: Path | None = None
    content_id: str = ""
    member: Member | None = None

    def identity(self) -> str:
        return str(self.target) if self.target is not None else f"row {self.content_id}"


@dataclass(frozen=True, slots=True)
class PlaylistPlan:
    """One INBOX playlist a landing writes for a playlist the author made on the account (U113)."""

    #: The name it is created under, chosen against what INBOX holds.
    name: str
    #: The account's identifier for the playlist it carries.
    account: str
    #: Every member, planned and owned, in the account playlist's order (U128).
    members: tuple[PlaylistMember, ...]
    account_name: str = ""
    #: The account playlist's rows it does not hold, each with why (U128).
    left: tuple[Left, ...] = ()

    @property
    def targets(self) -> tuple[Path, ...]:
        """The planned targets it holds, in the account playlist's order."""
        return tuple(one.target for one in self.members if one.target is not None)

    @property
    def owned(self) -> int:
        return sum(1 for one in self.members if one.target is None)


@dataclass(frozen=True, slots=True)
class HeartItem:
    """One planned file the pass's hearts asked for, and the month playlist it joins (U120, U145)."""

    target: Path
    #: The month playlist, or None when the job froze no date key; the
    #: backfill gives that heart its month.
    month: str | None
    ref: str


@dataclass(frozen=True, slots=True)
class OwnedHeartItem:
    """One heart of the pass on a track the library already holds, and its month (U146)."""

    content_id: str
    month: str
    ref: str
    title: str = ""


@dataclass(frozen=True, slots=True)
class FavoritesPlan:
    """The hearts a landing places (U120): their home, each one's month, or why none.

    PLANNED BEFORE THE GATE AND DIGESTED, so an answer given for one set of
    hearts is stale for another. ``skipped`` is the home's refusal when the
    source playlist is absent or doubled: the batch still lands, no heart is
    placed, and the backfill places them later.
    """

    source_name: str
    source_id: str
    folder_id: str
    folder_name: str
    items: tuple[HeartItem, ...]
    #: The month playlists live under the folder when the plan was made.
    present: tuple[str, ...] = ()
    skipped: str = ""
    #: Hearts on tracks the library holds that All Favorites lacks (U146).
    owned: tuple[OwnedHeartItem, ...] = ()
    #: The library's Pink row (U153), or empty with ``colour_skipped`` saying why.
    pink: str = ""
    colour_skipped: str = ""
    #: The owned hearts with no colour, which take Pink, and those a person
    #: coloured otherwise, named and left.
    colour: tuple[str, ...] = ()
    held: tuple[colour_mod.Held, ...] = ()

    @property
    def months(self) -> tuple[str, ...]:
        """Every month the hearts go to, by name, so the screen reads in one order."""
        return tuple(
            sorted(
                {item.month for item in self.items if item.month}
                | {one.month for one in self.owned}
            )
        )

    @property
    def unknown(self) -> int:
        """How many hearts take no month here, their job having frozen no date key."""
        return sum(1 for item in self.items if item.month is None)

    @property
    def creates(self) -> tuple[str, ...]:
        return tuple(month for month in self.months if month not in self.present)

    def home(self) -> placement.Home:
        return placement.Home(
            source_name=self.source_name,
            source_id=self.source_id,
            folder_id=self.folder_id,
            folder_name=self.folder_name,
            present={},
        )

    def identity(self) -> dict[str, Any]:
        """The digest's view: the owned hearts a key only when there are any (U146)."""
        identity: dict[str, Any] = {
            "source": self.source_name,
            "source_id": self.source_id,
            "folder": self.folder_id,
            "skipped": self.skipped,
            "hearts": [
                {"to": str(item.target), "month": item.month, "ref": item.ref}
                for item in self.items
            ],
        }
        if self.owned:
            identity["owned"] = [
                {"row": one.content_id, "month": one.month, "ref": one.ref} for one in self.owned
            ]
        # THE PINK ROW AND ITS ROWS (U153): a heart coloured by hand between
        # the two acts is another plan.
        identity["pink"] = self.pink
        if self.colour:
            identity["colour"] = list(self.colour)
        return identity


@dataclass(frozen=True, slots=True)
class WrittenPlaylist:
    """One INBOX playlist the commit wrote for an account playlist, read for the report."""

    name: str
    playlist_id: str
    account: str
    tracks: int


@dataclass(frozen=True, slots=True)
class NativePlan:
    """What :func:`apply_rows` will write, and the fingerprint it was planned at."""

    tree_id: str
    root_id: str
    root_name: str
    playlist: str
    database: Path
    device_id: str
    master_db_id: str
    base_drive: str | None
    current_drive: str | None
    rows: tuple[RowPlan, ...]
    #: The ContentLink every added row is given and its counts (U126), read
    #: at plan time; None when the plan adds no row.
    link: row_link.LibraryLink | None
    digest: str
    #: The account playlists, each its own INBOX playlist (U113); the batch
    #: playlist holds only the rows none of them holds.
    playlists: tuple[PlaylistPlan, ...] = ()
    #: The ``--pass`` name, recorded with the commit (R-777).
    pass_name: str | None = None
    #: The hearts among the rows and where they go (U120).
    favorites: FavoritesPlan | None = None
    #: A ``--set`` landing's permanent playlist under INSPIRATION (U121).
    set_playlist: set_playlist.SetPlaylistPlan | None = None
    #: The label filing under the Record Labels tree (U156).
    labels: label_filing.LabelPlan | None = None
    #: The INBOX playlist an earlier landing of the same set job made (U135),
    #: added to; empty when the write finds or makes it by the set's name.
    batch_playlist_id: str = ""
    #: The set job a ``--set`` landing records on its batch playlist (U135).
    set_job_id: str = ""
    #: INBOX names that look like earlier parts of this set from before U135,
    #: shown and never joined automatically.
    inbox_leftovers: tuple[str, ...] = ()
    #: Whether a set landing found a live INBOX playlist of the set's name no
    #: landing of this job recorded (U135).
    inbox_found_by_name: bool = False
    #: The left rows of each account playlist holding nothing here (U128).
    unplanned_left: tuple[tuple[str, Left], ...] = ()
    #: The vox cut the scores were read against (U127), and why no row is tagged.
    vox_cut: float | None = None
    vox_blocked: str = ""
    #: The drift cut the readings were judged against (U157), and why no
    #: variable row is tagged.
    drift_cut: float | None = None
    dyn_blocked: str = ""
    #: The live :data:`ANALYZE` playlist the plan found (U166), empty when made.
    analyze_playlist_id: str = ""
    #: The folder the files move into and the batch it is filed for (U164).
    folder: Path | None = None
    batch: str = ""
    #: Where adoption would file each added row (U165), from :func:`with_filing`.
    filing: tuple[Any, ...] | None = None
    #: The custom playlist twins written in the same commit (U149).
    twins: tuple[Any, ...] = ()

    def to_add(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == ADD)

    def vox_tagged(self) -> tuple[RowPlan, ...]:
        """The rows to be added that are given the vox My Tag (U127)."""
        return tuple(row for row in self.to_add() if row.vox)

    def vox_unscored(self) -> tuple[RowPlan, ...]:
        """The rows to be added whose file gave no score, empty when none was read."""
        if self.vox_cut is None or self.vox_blocked:
            return ()
        return tuple(row for row in self.to_add() if row.voxlevel is None)

    def dyn_tagged(self) -> tuple[RowPlan, ...]:
        """The rows to be added that are given the dyn My Tag (U157)."""
        return tuple(row for row in self.to_add() if row.dyn)

    def drift_variable(self) -> tuple[RowPlan, ...]:
        """The rows to be added whose drift reads as variable, tagged or not (U157)."""
        return tuple(row for row in self.to_add() if row.drift_verdict == drift.VARIABLE)

    def drift_unscored(self) -> tuple[RowPlan, ...]:
        """The rows to be added whose file carries no drift reading, and so no tag (U157)."""
        return tuple(row for row in self.to_add() if row.drift_verdict == drift.UNSCORED)

    def present(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == PRESENT)

    def unsupported(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == UNSUPPORTED)


@dataclass(frozen=True, slots=True)
class AddedRow:
    """One row the commit landed, read back from SQL after it."""

    target: Path
    content_id: str
    title: str
    folder_path: str
    #: The analysis columns and what each holds, every one expected empty.
    empty: dict[str, Any]
    #: ``rb_file_id`` as text (U115) and ``ContentLink`` (U126), as stored.
    file_id: str = ""
    content_link: int | None = None
    #: Whether the row carries the vox (U127) and dyn (U157) My Tags as their readers see them.
    vox: bool = False
    dyn: bool = False
    #: The row's words and year as stored, through active lookup rows, and as planned (U163).
    words: dict[str, Any] = field(default_factory=dict)
    planned: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NativeLanded:
    """What the commit landed: the rows, the playlist, and the memberships."""

    tree_id: str
    playlist: str
    playlist_id: str
    added: tuple[AddedRow, ...]
    present: tuple[RowPlan, ...]
    memberships_added: int
    session_id: str
    #: The account playlists written (U113); ``playlist_id`` is empty when
    #: they took every row.
    playlists: tuple[WrittenPlaylist, ...] = ()
    #: The hearts placed (U120), the set's playlist (U121) and the label
    #: filing (U156) the same commit wrote, each None when not planned.
    favorites: placement.Placed | None = None
    set_playlist: set_playlist.Written | None = None
    labels: label_filing.Written | None = None
    #: The ContentLink the plan gave every added row (U126), which the read back is held to.
    content_link: int | None = None
    #: Each account playlist track no INBOX playlist holds, by playlist name (U128).
    left: tuple[tuple[str, Left], ...] = ()
    #: The vox My Tag (U127): associations written, rows whose file gave no
    #: score, why none was tagged, rows tagged that adoption's reader does not
    #: answer after the commit, and why it could not read.
    vox_written: int = 0
    vox_unscored: tuple[Path, ...] = ()
    vox_blocked: str = ""
    vox_missing: tuple[Path, ...] = ()
    vox_unread: str = ""
    #: The dyn My Tag (U157), in the same shape, with the rows that read variable.
    dyn_written: int = 0
    dyn_variable: tuple[Path, ...] = ()
    dyn_unscored: tuple[Path, ...] = ()
    dyn_blocked: str = ""
    dyn_missing: tuple[Path, ...] = ()
    dyn_unread: str = ""
    #: The :data:`ANALYZE` playlist the rows joined (U166), its display name,
    #: and how many memberships the commit added; empty when no row was added.
    analyze_id: str = ""
    analyze_name: str = ""
    analyze_added: int = 0
    #: The custom playlist twins the commit wrote (U149), which the caller pairs.
    twins: tuple[Any, ...] = ()

    def names(self) -> tuple[str, ...]:
        """Every INBOX playlist the commit wrote, the batch's first when it wrote one."""
        batch = (self.playlist,) if self.playlist_id else ()
        return (*batch, *(written.name for written in self.playlists))


def _playlist_identity(one: PlaylistPlan) -> dict[str, Any]:
    """One account playlist as the digest covers it; owned and left rows only when there are any."""
    identity: dict[str, Any] = {
        "name": one.name,
        "account": one.account,
        "targets": [str(target) for target in one.targets],
    }
    if one.owned:
        identity["members"] = [member.identity() for member in one.members]
    if one.left:
        identity["left"] = [row.identity() for row in one.left]
    return identity


def identity(plan: NativePlan) -> dict[str, Any]:
    """What the digest covers: every fact the apply writes, and the library it writes to.

    The database's path is the one fact the screen shows that is left out
    (U161), since two copies of one library carry the same device, master id
    and rows and a rehearsal on one must digest as the other.
    """
    split = (
        {"playlists": [_playlist_identity(one) for one in plan.playlists]}
        if plan.playlists
        else {}
    )
    unplanned = (
        {"unplanned_left": [[name, row.identity()] for name, row in plan.unplanned_left]}
        if plan.unplanned_left
        else {}
    )
    favorites = {"favorites": plan.favorites.identity()} if plan.favorites is not None else {}
    kept = (
        {"set_playlist": set_playlist.identity(plan.set_playlist)}
        if plan.set_playlist is not None
        else {}
    )
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
    # THE VOX (U127) AND DYN (U157) TAGS ONLY WHEN A ROW IS ADDED, each row's
    # reading and answer, so an approval given before a file was rescored or
    # the cut changed is stale for the tags it would write.
    vox = (
        {
            "vox": {
                "cut": plan.vox_cut,
                "blocked": plan.vox_blocked,
                "rows": [[str(row.target), row.voxlevel, row.vox] for row in plan.to_add()],
            }
        }
        if plan.to_add()
        else {}
    )
    dyn = (
        {
            "dyn": {
                "cut": plan.drift_cut,
                "blocked": plan.dyn_blocked,
                "rows": [
                    [str(row.target), row.drift, row.drift_verdict, row.dyn]
                    for row in plan.to_add()
                ],
            }
        }
        if plan.to_add()
        else {}
    )
    # Each key below only when it applies, so a plan without it digests as before.
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
    filing = (
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
    )
    twins = {"twins": [one.identity() for one in plan.twins]} if plan.twins else {}
    return {
        **split,
        **twins,
        **unplanned,
        **favorites,
        **kept,
        **filed,
        **vox,
        **dyn,
        **analyze,
        **filing,
        "kind": "land-native",
        "tree": plan.tree_id,
        "root": plan.root_id,
        "playlist": plan.playlist,
        "batch_playlist": plan.batch_playlist_id,
        "set_job": plan.set_job_id,
        "inbox_leftovers": list(plan.inbox_leftovers),
        "inbox_found_by_name": plan.inbox_found_by_name,
        # THE LIBRARY BY ITS DEVICE AND MASTER ID, NEVER THE FILE (U161): a
        # rehearsal reads a copy at another path and must digest as the live one.
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
        "rows": [
            {
                "from": str(row.source),
                "to": str(row.target),
                "action": row.action,
                "content_id": row.content_id,
                "columns": row.columns(),
            }
            for row in plan.rows
        ],
        "left_empty": list(LEFT_EMPTY),
        # THE COUNTS AS WELL AS THE VALUE, since the screen shows both (U126).
        "content_link": (
            {"value": plan.link.value, "carriers": plan.link.carriers, "rows": plan.link.rows}
            if plan.link is not None
            else None
        ),
    }


def _restamp(content: Any, row: RowPlan, plan: NativePlan) -> None:
    """Put the planned path and device, the file id, the link and rekordbox's defaults on the row the binding made.

    ON THE OBJECT BEFORE THE GUARD'S FLUSH, so the guard judges the row as it
    will be stored. Each value fixes something rekordbox will not load a row
    to a deck without.
    """
    # THE MINTED ID AS TEXT, AS STORED (U153): a flush cannot order pending
    # djmdContent rows that mix the binding's int ID with stored text IDs.
    content.ID = str(content.ID)
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
    if str(content.MasterDBID) != plan.master_db_id:
        content.MasterDBID = plan.master_db_id
    # THE LANDED FILE'S INODE, read now (U115), never the binding's random id.
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
    # THE LIBRARY'S CONTENTLINK, AS PLANNED (U126), never the menu counter.
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
    # REKORDBOX'S OWN DEFAULTS where the binding left NULL (R-923).
    for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items():
        if getattr(content, column, None) is None:
            setattr(content, column, value)


def file_id_of(path: Path) -> int:
    """The value rekordbox writes to ``rb_file_id`` for a file it imports: its inode (U115)."""
    return os.stat(path).st_ino


def assert_names_still_free(db: Any, plan: NativePlan) -> None:
    """Refuse an account playlist name INBOX came to hold after the plan chose it.

    ASKED BEFORE THE FIRST MOVE, so a refusal leaves the files in staging, and
    again before the first row, for whatever took a name in between.
    """
    from cratekit.intake.native_plan import inbox_held

    if not plan.playlists:
        return
    held = set(inbox_held(db, plan.root_id))
    clash = sorted(one.name for one in plan.playlists if one.name in held)
    if clash:
        raise refuse(
            "decision-stale",
            f"the intake folder holds {', '.join(repr(name) for name in clash)} since "
            f"this landing chose those names, so nothing was written; run the landing "
            f"again and it takes the next free name",
            origin=_ORIGIN,
            detail={"names": clash, "root": plan.root_id},
        )


def assert_rows_gridless(landed: NativeLanded) -> None:
    """Refuse when a row read back after the commit carries an analysis value.

    THE GUARD HOLDS THIS BEFORE THE COMMIT, so reaching here is the guard's
    defect. It is read anyway, because the record promises what the rows hold
    as rekordbox will find them.
    """
    carried = [
        f"{row.content_id}: {name} = {value!r}"
        for row in landed.added
        for name, value in row.empty.items()
        if value not in rb_writer.EMPTY_ON_CREATE
    ]
    if carried:
        raise refuse(
            "whitelist-violation",
            "a landed row carries an analysis value after the commit, which the "
            "guard should have refused before it: " + "; ".join(carried),
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"carried": carried},
        )


def assert_rows_identified(landed: NativeLanded) -> None:
    """Refuse when a landed row's file id or link read back is not what it was given.

    THE RESTAMP SETS THEM BEFORE THE COMMIT, so reaching here means a column
    was dropped on the way to the table and rekordbox will not load the row.
    The write is durable, so the refusal names the session that undoes it.
    """
    wrong = [
        f"{row.content_id}: {rb_writer.FILE_ID_COLUMN} = {row.file_id!r}, "
        f"the file's inode is {file_id_of(row.target)}"
        for row in landed.added
        if str(row.file_id) != str(file_id_of(row.target))
    ]
    # NO SKIP: a row added with no value planned is as wrong as one that did not take.
    wrong += [
        f"{row.content_id}: {rb_writer.CONTENT_LINK_COLUMN} = {row.content_link!r}, "
        f"the library's is {landed.content_link!r}"
        for row in landed.added
        if landed.content_link is None or row.content_link != landed.content_link
    ]
    # THE WORDS AND THE YEAR (U163): a link to a tombstone reads as missing.
    wrong += [
        f"{row.content_id}: {column} reads {row.words.get(column)!r}, the file's is {want!r}"
        for row in landed.added
        for column, want in row.planned.items()
        if row.words.get(column) != want
    ]
    if wrong:
        raise refuse(
            "internal-error",
            "a landed row does not carry the file id, link or words it was given "
            "after the commit, so rekordbox will not load it to a deck or will "
            "show it without them: " + "; ".join(wrong),
            remedy=Remedy.REPORT_DEFECT,
            steps=(f"the write is durable; restore session {landed.session_id} to undo it",),
            origin=_ORIGIN,
            detail={"wrong": wrong, "session": landed.session_id},
        )


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: NativePlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> NativeLanded:
    """Write the plan: the rows, the playlist under the root, the memberships.

    THE SESSION SPINE IS CALLED, NOT REBUILT: the gates with a record kept, a
    capture, the analysis watch over ``analysis_roots``, the commit witness and
    the guarded commit, whose ``creations`` admits the content rows (R-760).

    ALL OR NOTHING IN THE DATABASE: every write is pending on one handle until
    one commit, and a refusal before it rolls the handle back. The files are in
    the library by then, which the caller reports.
    """
    from cratekit.intake import native_apply as steps
    from cratekit.intake.native_apply import _analyze_row, _tag_dyn, _tag_vox, _vox_read_back

    watched = steps._assert_unchanged(cfg, db, plan, analysis_roots)
    added_ids: list[tuple[RowPlan, str]] = []
    present: list[RowPlan] = list(plan.present())
    memberships = 0
    vox_written = 0
    dyn_written = 0
    analyze_id = ""
    analyze_added = 0
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, capture = trees.attached_capture(gates, cfg, db)

        anchor = db.get_playlist(ID=plan.root_id)
        if anchor is None:
            raise tree_registry.RegistrySkew(
                f"the adopted intake root {plan.root_id!r} was reported present and "
                f"could not be read back, so the batch playlist has nothing to hang "
                f"from and would be created beside the tree instead",
                tree_id=plan.tree_id,
                root_id=plan.root_id,
            )
        playlist_id = ""
        # EVERY PLAYLIST ROW BEFORE THIS LANDING (R-1037), so its record names
        # only the playlists it MADE, which no rollback to before it can hold.
        playlists_before = frozenset(str(row.ID) for row in db.get_playlist())
        written: list[WrittenPlaylist] = []
        left: list[tuple[str, Left]] = [
            *plan.unplanned_left,
            *((one.name, row) for one in plan.playlists for row in one.left),
        ]
        placed: placement.Placed | None = None
        set_written: set_playlist.Written | None = None
        labels_written: label_filing.Written | None = None
        twins_written: tuple[Any, ...] = ()
        failed: BaseException | None = None
        try:
            # BEFORE THE FIRST ROW, so a refusal adds nothing: an account
            # playlist is created, so a name taken since would show twice.
            assert_names_still_free(db, plan)
            if plan.twins:
                from cratekit.sync import twins as twin_mod

                twin_mod.recheck_landing(db, plan.twins)
            to_add = plan.to_add()
            taken = steps._taken_since_the_plan(db, cfg, to_add)
            # THE WORDS ARE ASKED AGAIN (U163), so a lookup row made or retired
            # since the approval refuses rather than linking what nobody approved.
            steps._assert_words_unmoved(db, [row for row in to_add if str(row.target) not in taken])
            mints = steps._Mints(db)
            for row in to_add:
                held = taken.get(str(row.target))
                if held is not None:
                    present.append(replace(row, action=PRESENT, content_id=held))
                    continue
                content = db.add_content(row.target, Title=row.title)
                _restamp(content, row, plan)
                mints.link(content, row)
                added_ids.append((row, str(content.ID)))
            # THE VOX (U127) AND DYN (U157) MY TAGS, in the same commit, on the
            # rows this landing made that the plan tagged; additive.
            vox_written = _tag_vox(db, added_ids)
            dyn_written = _tag_dyn(db, added_ids)
            # Every file the plan named, new row or already there.
            by_target = {str(row.target): content_id for row, content_id in added_ids}
            by_target.update({str(row.target): row.content_id for row in present if row.content_id})
            claimed = {str(target) for one in plan.playlists for target in one.targets}
            # IN THE ACCOUNT PLAYLIST'S ORDER (U128). A member whose file made
            # no row is left, and named, rather than silently absent.
            accounts = []
            for one in plan.playlists:
                ids: list[str] = []
                for member in one.members:
                    held = (
                        member.content_id
                        if member.target is None
                        else by_target.get(str(member.target), "")
                    )
                    if held:
                        ids.append(held)
                    elif member.member is not None:
                        left.append((one.name, member.member.left(NOT_LANDED)))
                if ids:
                    accounts.append((one, ids))
            ordered = steps._batch_order(plan, by_target, claimed)
            # THE BATCH PLAYLIST HOLDS WHAT NO ACCOUNT PLAYLIST CLAIMED, and is
            # not written when that is nothing.
            if ordered or not accounts:
                playlist = steps._batch_playlist_row(db, plan, anchor)
                memberships = len(rb_writer.add_memberships(db, playlist, ordered))
                playlist_id = str(playlist.ID)
            for one, ids in accounts:
                created = db.create_playlist(one.name, parent=anchor)
                count = len(rb_writer.add_memberships(db, created, ids))
                memberships += count
                written.append(
                    WrittenPlaylist(
                        name=one.name,
                        playlist_id=str(created.ID),
                        account=one.account,
                        tracks=count,
                    )
                )
            # EACH ACCOUNT PLAYLIST'S TWIN (U149), the copy that stays when the
            # INBOX one rotates out.
            if plan.twins:
                from cratekit.sync import twins as twin_mod

                twins_written = twin_mod.write_landing(
                    db, plan.twins, {one.account: ids for one, ids in accounts}
                )
            # EVERY ROW THIS LANDING MADE JOINS ANALYZE (U166); a row already
            # held is not added, since rekordbox has had it.
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
                analyze_id = str(analyze.ID)
                analyze_added = len(
                    rb_writer.add_memberships(
                        db, analyze, [content_id for _row, content_id in added_ids]
                    )
                )
            # THE HEARTS (U120): into All Favorites and each one's month, a row
            # present as much as one added, and the owned hearts (U146).
            if plan.favorites is not None and (plan.favorites.items or plan.favorites.owned):
                pairs: list[tuple[str, str | None]] = [
                    (by_target[str(item.target)], item.month)
                    for item in plan.favorites.items
                    if str(item.target) in by_target
                ]
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
                # AND PINK (U153) on each new row and each uncoloured owned heart.
                to_colour = [
                    by_target[str(item.target)]
                    for item in plan.favorites.items
                    if str(item.target) in by_target
                ]
                to_colour.extend(plan.favorites.colour)
                placed = placement.place(
                    db,
                    plan.favorites.home(),
                    pairs,
                    pink=plan.favorites.pink,
                    to_colour=to_colour,
                    held=plan.favorites.held,
                    colour_skipped=plan.favorites.colour_skipped,
                )
            # THE SET'S PERMANENT PLAYLIST (U121) and THE LABEL FILING (U156),
            # by target; a member whose file made no row is left and named.
            if plan.set_playlist is not None:
                set_written = set_playlist.write_members(db, plan.set_playlist, by_target=by_target)
            if plan.labels is not None:
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
            # THE LOOKUP TABLES ONLY WHEN A WORD WAS MINTED (U163).
            rb_writer.commit_guarded(
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
            )
        except BaseException as exc:
            trees.rollback_quietly(db)
            if not witness.landed:
                raise
            # THE COMMIT LANDED BEFORE THE FAILURE, so it is recorded, then raised.
            failed = exc
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
            cfg,
            landed=steps._landed_rows(
                db, plan, added_ids, (playlist_id, *(one.playlist_id for one in written)),
                before=playlists_before,
            ),
            playlist_id=playlist_id,
            written=written,
            placed=placed,
            set_written=set_written,
            vox_written=vox_written,
            dyn_written=dyn_written,
            labels_written=labels_written,
            twins_written=twins_written,
        )
        if failed is not None:
            raise failed
        convergence.record_fingerprint(cfg, db)
        if set_written is not None and set_written.playlist_id:
            set_written = replace(
                set_written, read_back=set_playlist.read_back(db, set_written.playlist_id)
            )
        if labels_written is not None:
            labels_written = label_filing.read_back(db, labels_written)

        landed = []
        # ONLY WHEN A TAG WAS PLANNED: a new row carries no tag it was not given.
        voxed, vox_unread = (
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
        )
        dyned, dyn_unread = (
            steps._dyn_read_back(db) if any(row.dyn for row, _ in added_ids) else (frozenset(), "")
        )
        for row, content_id in added_ids:
            values, title, folder_path, file_id, link = steps._read_back(db, content_id)
            landed.append(
                AddedRow(
                    target=row.target,
                    content_id=content_id,
                    title=title,
                    folder_path=folder_path,
                    empty=values,
                    file_id=file_id,
                    content_link=link,
                    vox=content_id in voxed,
                    dyn=content_id in dyned,
                    words=steps._words_back(db, content_id),
                    planned=row.words(),
                )
            )
        session_id = record.session_id

    unscored = {row.target for row in plan.vox_unscored()}

    def targets(keep: Any) -> tuple[Path, ...]:
        return tuple(row.target for row, content_id in added_ids if keep(row, content_id))

    return NativeLanded(
        tree_id=plan.tree_id,
        playlist=plan.playlist,
        playlist_id=playlist_id,
        added=tuple(landed),
        present=tuple(present),
        memberships_added=memberships,
        session_id=session_id,
        playlists=tuple(written),
        favorites=placed,
        set_playlist=set_written,
        labels=labels_written,
        content_link=plan.link.value if plan.link is not None else None,
        left=tuple(left),
        vox_written=vox_written,
        vox_unscored=targets(lambda row, _id: row.target in unscored),
        vox_blocked=plan.vox_blocked if added_ids else "",
        vox_missing=tuple(
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
        ),
        vox_unread=vox_unread,
        dyn_written=dyn_written,
        dyn_variable=targets(lambda row, _id: row.drift_verdict == drift.VARIABLE),
        dyn_unscored=targets(lambda row, _id: row.drift_verdict == drift.UNSCORED),
        dyn_blocked=plan.dyn_blocked if added_ids else "",
        dyn_missing=targets(lambda row, content_id: row.dyn and content_id not in dyned),
        dyn_unread=dyn_unread,
        analyze_id=analyze_id,
        analyze_name=f"{plan.root_name} / {ANALYZE}" if analyze_id else "",
        analyze_added=analyze_added,
        twins=twins_written,
    )


def _record_landing_commit(
    record: session.SessionRecord,
    plan: NativePlan,
    rows: int,
    memberships: int,
    cfg: config.Config,
    *,
    playlist_id: str,
    landed: Mapping[str, Any] | None = None,
    written: Sequence[WrittenPlaylist] = (),
    placed: placement.Placed | None = None,
    set_written: set_playlist.Written | None = None,
    vox_written: int = 0,
    dyn_written: int = 0,
    labels_written: label_filing.Written | None = None,
    twins_written: Sequence[Any] = (),
) -> None:
    """Record the commit on the session, once anything landed.

    TWO COUNTS UNDER TWO NAMES: the memberships under the intake tree, which
    ``restore list`` and ``tree cutover`` read, and the rows under the content
    table, since a restore that discards them discards tracks.
    """
    hearts = placed.added if placed is not None else 0
    coloured = len(placed.coloured) if placed is not None else 0
    if (
        rows <= 0
        and memberships <= 0
        and hearts <= 0
        and coloured <= 0
        and not (set_written and set_written.playlist_id)
        and not (labels_written and labels_written.changed())
    ):
        return
    # THE BATCH PLAYLIST BY ID AND NAME (U111), so ``inbox rotate`` ages it
    # from the day it landed.
    if playlist_id:
        kept = {"id": playlist_id, "name": plan.playlist}
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id
        record.detail[BATCH_PLAYLIST_KEY] = kept
    # THE BATCH AND ITS FILED FOLDER (U164), so the name stays taken.
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY] = {"batch": plan.batch, "folder": str(plan.folder)}
    # EVERY ROW IT MADE (R-1037), so the deletion pass offers a landed row's
    # file once rekordbox has deleted the row outright.
    if landed is not None:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
    # THE PASS (R-777), what ``sync mark --pass`` reads as proof it landed.
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
    # EACH ACCOUNT PLAYLIST BY ID (U113), aged from this record and never by
    # its name, whose date (U175) is a label.
    if written:
        record.detail[INBOX_PLAYLISTS_KEY] = [
            {
                "id": one.playlist_id,
                "name": one.name,
                ingest.INBOX_ACCOUNT_KEY: one.account,
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
            }
            for one in written
        ]
    # EACH LABEL ROW'S PROVIDER TRACK (U150), so the account mirror fills this
    # batch's INBOX playlist from its own tracks.
    if labels_written is not None and labels_written.provider:
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
    # THE HEARTS UNDER THEIR OWN KEY (U120): the Favorites folder is nobody's
    # registered tree, so a restore sees them apart from the memberships.
    if placed is not None and (hearts > 0 or coloured > 0):
        record.detail[placement.PLACED_KEY] = placed.to_json()
    changes = []
    if memberships > 0:
        changes.append(session.TreeChange(tree=plan.tree_id, created=memberships))
    if rows > 0:
        changes.append(session.TreeChange(tree=rb_writer.CONTENT_TABLE, created=rows))
    # ONLY A TREE THAT CHANGED IS RECORDED COMMITTED, or a restore and a revert
    # would read a change the intake tree never had.
    if changes:
        session.record_commit(record, plan.tree_id, session.ChangeSummary(tuple(changes)), cfg)
    # Each of the rest is counted under its own key, apart from the batch.
    if hearts > 0 or coloured > 0:
        _record_count(record, placement.RECORD_KEY, cfg, created=hearts, updated=coloured)
    if set_written is not None and plan.set_playlist is not None:
        set_playlist.record_commit(record, set_written, plan.set_playlist, cfg)
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
    if twins_written:
        from cratekit.sync import twins as twin_mod

        record.detail[twin_mod.RECORD_KEY] = [
            {"id": one.playlist_id, "name": one.name, ingest.INBOX_ACCOUNT_KEY: one.account_id}
            for one in twins_written
        ]
        created = len(twins_written) + sum(one.tracks for one in twins_written)
        _record_count(record, twin_mod.RECORD_KEY, cfg, created=created)
    if vox_written > 0:
        _record_count(record, metadata_cli.CHANGE_KEY, cfg, created=vox_written)
    if dyn_written > 0:
        session.record_commit(
            record,
            DYN_CHANGE_KEY,
            session.ChangeSummary((session.TreeChange(tree=DYN_CHANGE_KEY, created=dyn_written),)),
            cfg,
        )


def _record_count(
    record: session.SessionRecord, key: str, cfg: config.Config, *, created: int, updated: int = 0
) -> None:
    """Record a commit of ``created`` and ``updated`` under ``key``, its own tree."""
    change = session.TreeChange(tree=key, created=created, updated=updated)
    session.record_commit(record, key, session.ChangeSummary((change,)), cfg)


def __getattr__(name: str) -> Any:
    """A name of the plan, the readers or the apply's steps, found on first use.

    Each of them imports this module's types, so importing them here would be a cycle.
    """
    from importlib import import_module

    # NEVER A DUNDER: the import system asks for ``__path__`` while a sibling
    # is still importing this module, and must be told there is none.
    siblings = () if name.startswith("__") else ("native_plan", "native_apply")
    for sibling in siblings:
        module = import_module(f"cratekit.intake.{sibling}")
        if hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
