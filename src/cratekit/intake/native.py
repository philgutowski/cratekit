"""Land a batch in the collection through the guarded database writer (R-746).

On a library whose intake tree has cut over, this engine replaces the xml
landing's hand steps: one content row per landed file and one batch playlist
under the adopted intake root, through the session spine every database tree
writer uses, behind a plan and an approval the verb owns.

A CONTENT ROW IS THE ROW REKORDBOX ANALYSES INTO, so what it may carry is a
column policy asserted from SQL before the commit, in ``rb_writer``, and read
back after it here. The row carries what the file's tags and the filesystem
say; every column an analysis pass fills stays empty, named by
:data:`LEFT_EMPTY`.

What a row needs before rekordbox will show and load it, each measured on the
live library:

* its ``FolderPath`` under ``djmdProperty.BaseDBDrive``, not the mounted
  path, and its device the one whose ``MasterDBID`` is the library's
  ``DBID``: a library can hold two devices and the binding's pick is order
  dependent (A8);
* ``rb_file_id`` the landed file's inode, read when the row is made and never
  from the plan, since staging may sit on another volume (U115);
* ``ContentLink`` the value most of the library's live rows carry, read at
  plan time and covered by the digest (U126).

THE PLAN IS BUILT AGAINST THE DATABASE AND THE APPLY REBUILDS NOTHING. The
person approves the plan's digest; the apply writes that plan and asks the
database again only what the plan could not know, whether a row appeared in
between.

An account playlist gets its own INBOX playlist, created and never found by
name, so two landings never share one (U113); a ``--set`` landing adds to the
INBOX playlist its job recorded first (U135). Every row a landing creates
also joins :data:`ANALYZE` under the intake root, so the rekordbox visit
selects one playlist (U166).

``plan_rows`` and ``apply_rows`` mean something else in ``cratekit.tagging.rows``,
where a row exists already; here a row is one this engine adds.

The plan lives in :mod:`cratekit.intake.native_plan` and the apply in
:mod:`cratekit.intake.native_apply`; both are re-exported here, and every name
a caller or a test patches is looked up on this module.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

from cratekit.core import config, drift, locations, rb_writer, session
from cratekit.core.cause import Remedy, refuse
from cratekit.favorites import colour as colour_mod
from cratekit.favorites import placement
from cratekit.intake import ingest, label_filing, set_playlist
from cratekit.write import row_link, trees

if TYPE_CHECKING:
    # Annotation only: the module that defines them reaches this one.
    from cratekit.intake.account_playlists import Left, Member

#: What a planned row will do. A file whose suffix the binding has no file
#: type for is planned as UNSUPPORTED and left in staging by the landing, the
#: way a file whose target is occupied is: refused alone, and the batch lands.
ADD = "add"
PRESENT = "already present"
UNSUPPORTED = "unsupported"

#: The columns a landed row leaves for rekordbox, named once for the plan, the
#: record and the read back. THE WRITER'S LIST, not a copy of it: the guard is
#: what refuses a value here, and a second spelling is how the answer a person
#: reads and the answer the guard enforces come to differ.
LEFT_EMPTY: tuple[str, ...] = tuple(sorted(rb_writer.CONTENT_ROW_EMPTY_COLUMNS))

#: What the plan screen shows for :data:`cratekit.core.rb_writer.FILE_ID_COLUMN`
#: on a row to be added. A sentence and not a number, because the number is
#: read on the landed file when the row is made (U115).
FILE_ID_AT_LANDING = "the landed file's inode number, read when the row is made"

#: The session workflow a native landing is recorded under, the intake's own.
WORKFLOW = ingest.INTAKE_WORKFLOW

#: The session record field naming the batch playlist a landing wrote, its
#: identifier and its name. Read by ``inbox rotate`` for the landing date.
#: Since U135 a landing given ``--set`` also records the set job under
#: :data:`INBOX_JOB_KEY`, so a later landing of the same job finds that
#: playlist and adds to it under its first name.
BATCH_PLAYLIST_KEY = "batch_playlist"
#: The session record field naming the batch a landing filed and the folder
#: it filed it in (U164), written with the commit when the landing chose a
#: folder under the processed tree. Read by ``intake land`` so a batch landed
#: into again by its own name goes back to its folder, by the batch name rule
#: so the name stays taken, and by ``intake shelve`` to say there is nothing
#: to move.
FILED_BATCH_KEY = "filed_batch"
#: The key on a :data:`BATCH_PLAYLIST_KEY` entry naming the set job the
#: INBOX playlist was written for (U135). Absent on every landing that is
#: not a set, and on set landings from before this unit.
INBOX_JOB_KEY = "job"
#: The session record field naming the sync pass a landing was given with
#: ``--pass`` (R-777). Written with the commit, so ``sync mark --pass`` reads a
#: closed record naming the pass as the proof the pass landed, the one an
#: intake file is on the bridge.
PASS_KEY = "pass"

#: The session record field naming every row a landing made (R-1037): the
#: database by its identity, the update count the landing's commit left, the
#: playlists it made, and each row's :data:`LANDED_COLUMNS` and its UUID
#: (:data:`LANDED_UUID_KEY`) as the database holds them after the commit. rekordbox 7.2 deletes a row a person
#: removes OUTRIGHT (A178, A185), so the deletion pass reads a landed row the
#: database no longer holds as that removal, and this record is the only place
#: the row's file and identity are written down. Read by ``deletion.library``,
#: which spells it again (``tests/test_delete_landed_removed.py``).
LANDED_ROWS_KEY = "collection_landed"
#: The field each landed row's UUID is kept under, beside its columns (R-1844):
#: the row's identity, a fresh ``uuid4`` this landing wrote under a random id,
#: so no database from before the landing holds the pair and a row still held
#: under it proves the landing was not rolled back, whatever became of the
#: playlists it made. Spelled again in ``deletion.library``.
LANDED_UUID_KEY = "uuid"
#: The columns a landed row is named by: the ones a recorded removal keeps
#: (``rb_writer.RECORDED_COLUMNS``), spelled here so this package reaches no
#: further into the core.
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

#: The session record field listing the account playlists a landing wrote, each
#: by identifier and name (U113). The intake's one spelling, shared with the
#: intake file's record.
INBOX_PLAYLISTS_KEY = ingest.INBOX_PLAYLISTS_KEY

#: The playlist directly under the intake root every row a landing creates
#: joins (U166), so the rekordbox visit selects one playlist. Its display
#: form is ``<intake root> / Analyze``. Reserved: :func:`plan_rows` refuses a
#: batch of the name, and an account playlist of it lands dated, ``Analyze
#: 2026-10-27`` (U175), so never as it; :data:`cratekit.intake.batch_name.ANALYZE`
#: spells the same
#: value because that module reaches this one through the landing; a test
#: holds the two equal.
ANALYZE = "Analyze"

#: Why a playlist member is not in its INBOX playlist when its file made no
#: row (U128), the words the landing's warning names it with on both media.
NOT_LANDED = "its file did not land"

#: Why a landing plans no vox My Tag on any row it adds (U127), each a
#: sentence the screen and the warning say. The library recorded no vocal
#: calibration, so there is no cut to read a score against: the routing
#: passes leave the vocal dimension uncompared on the same reading (R-276),
#: and a tag written from the default cut would file a vocal sub the
#: derivation never would.
VOX_UNCALIBRATED = (
    "the library has no vocal calibration, so no score can be read against a cut; "
    "run crate analyze calibrate and then crate metadata mytags-vocals --apply"
)
#: The library holds no My Tag category for the writer to copy a row's shape
#: from, which :func:`cratekit.core.rb_writer.ensure_my_tag_value` refuses.
VOX_NO_CATEGORY = (
    "the library holds no My Tag category to copy a new one's shape from, so the "
    "Vocals category cannot be made; make any My Tag in rekordbox and then run "
    "crate metadata mytags-vocals --apply"
)

#: The calibration is there and cannot be read, so it refuses on every
#: surface that reads it; the landing names that refusal and writes no tag.
VOX_UNREADABLE = (
    "the vocal calibration could not be read ({why}), so no score can be read against "
    "a cut; run crate analyze calibrate again and then crate metadata mytags-vocals --apply"
)

#: The My Tag a landing gives every added row whose file's drift reads as
#: variable (U157), so the person running Analyze Tracks selects those rows for
#: Dynamic and every other for Normal. :mod:`cratekit.analysis.rekordbox_check`
#: reads the mark under this value, by importing it, so the check and the
#: landing cannot come to disagree. The category is the one it is made under
#: when the library holds none of that name, found by name otherwise.
DYN_VALUE = "dyn"
DYN_CATEGORY = "Analysis"
#: What the dyn tags are filed under in a session record's change summary, a
#: stable surface name as the vocals verb's ``my-tags.vocals`` is (R19).
DYN_CHANGE_KEY = "my-tags.analysis"
#: Why a landing that read variable rows gives none of them the dyn My Tag,
#: the writer's own refusal asked before the gate, as :data:`VOX_NO_CATEGORY`.
DYN_NO_CATEGORY = (
    "the library holds no My Tag category to copy a new one's shape from, so the "
    "Analysis category cannot be made; make any My Tag in rekordbox and run the "
    "rows this landing names with Analysis Mode Dynamic by hand"
)

_ORIGIN = ("intake.native",)

logger = logging.getLogger(__name__)


#: The content columns a landing links to a lookup row (U163), and the one it
#: writes the date tag's year to.
ARTIST_COLUMN = "ArtistID"
ALBUM_COLUMN = "AlbumID"
GENRE_COLUMN = "GenreID"
YEAR_COLUMN = "ReleaseYear"
#: The album's own artist, read back beside the row's words (U163).
ALBUM_ARTIST = "AlbumArtistID"

#: What the screen and the digest show for a word the commit mints a lookup
#: row for, in place of the id of the active row it would link (U163).
MINTED = "mint"

@dataclass(frozen=True, slots=True)
class Word:
    """One artist, album or genre word a row to be added carries, and the lookup row it takes (U163).

    THE FIRST ACTIVE ROW BY EXACT NAME, or a row the commit mints when the
    library has none, which is what Reload Tags did by hand. An album is found
    by its name and its album artist together, so two albums of one name by
    two artists stay two, and an album whose artist is minted is minted too.
    """

    table: str
    name: str
    #: The active row the plan found, empty when the commit mints one.
    row_id: str = ""
    #: The album artist an album word links, by its own artist word.
    album_artist: Word | None = None
    #: What a minted artist or album row stores in ``SearchStr``, the
    #: library's own convention for the table; None stores NULL.
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
    #: The ContentLink the library's live rows mostly carry, given to the row
    #: (U126). Set on a row to be added and None on every other, so the screen
    #: and the digest name it only where it is written.
    content_link: int | None
    #: The row already holding this file, when ``action`` is ``PRESENT``.
    content_id: str | None = None
    #: Why the file is planned as ``UNSUPPORTED``, in a sentence, else empty.
    why: str = ""
    #: The file's ``voxlevel``, read off the source for a row to be added
    #: against a calibrated cut (U127). None for a file with no readable score
    #: and for every row the vox tag is not planned on.
    voxlevel: int | None = None
    #: Whether the row is given the vox My Tag, its score clearing the cut.
    vox: bool = False
    #: The file's drift, a percent, and the verdict it reads as against the
    #: plan's cut (U157), read off the source for a row to be added: one of
    #: :data:`cratekit.core.drift.VERDICTS` or ``UNSCORED``, empty on a row
    #: that is not added. ``dyn`` is whether the row is given the dyn My Tag.
    drift: float | None = None
    drift_verdict: str = ""
    dyn: bool = False
    #: The file's artist, album and genre words and the lookup row each takes
    #: (U163), read off the source for a row to be added and None for a word
    #: the file does not carry, which leaves rekordbox's empty.
    artist: Word | None = None
    album: Word | None = None
    genre: Word | None = None
    #: The year of the file's date tag, written to ``ReleaseYear`` (U163).
    year: int | None = None

    def columns(self) -> dict[str, Any]:
        """Every column the writer sets on the row, by name, for the screen."""
        words = {
            column: word.shown()
            for column, word in (
                (ARTIST_COLUMN, self.artist),
                (ALBUM_COLUMN, self.album),
                (GENRE_COLUMN, self.genre),
            )
            if word is not None
        }
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

    A planned ``target``, whose row the apply makes or finds, or the
    ``content_id`` of a row the library held, found by path at plan time.
    ``member`` is what the landing planned it from, for the warning when its
    file does not land.
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
    #: Every member, the planned targets and the owned rows, in the account
    #: playlist's order (U128).
    members: tuple[PlaylistMember, ...]
    #: The account's own name for it, which ``name`` differs from only by a count.
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
    #: The month playlist, or None for a heart whose job froze no date key,
    #: which joins All Favorites here and takes its month from the backfill.
    month: str | None
    #: The provider's identifier for the heart, for the screen.
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

    PLANNED BEFORE THE GATE AND DIGESTED, so the screen says which files go
    into All Favorites and which month, and an answer given for one set of
    hearts is stale for another. ``skipped`` is the home's refusal when the
    source playlist is absent or doubled: the batch still lands, no heart is
    placed, and the backfill places them once the playlist exists.
    """

    source_name: str
    source_id: str
    folder_id: str
    folder_name: str
    items: tuple[HeartItem, ...]
    #: The month playlists live under the folder when the plan was made.
    present: tuple[str, ...] = ()
    skipped: str = ""
    #: The pass's hearts on tracks the library already holds that All
    #: Favorites lacks, placed in the same commit (U146).
    owned: tuple[OwnedHeartItem, ...] = ()
    #: The library's Pink row (U153), or empty with ``colour_skipped`` saying
    #: why, in which case the hearts are placed and none is coloured.
    pink: str = ""
    colour_skipped: str = ""
    #: The owned hearts with no colour, which take Pink with their placement.
    #: A landed file's new row has none by construction and is not listed.
    colour: tuple[str, ...] = ()
    #: The owned hearts a person coloured otherwise, named and left.
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
        # THE PINK ROW AND THE ROWS IT GOES ON (U153), so a heart coloured by
        # hand between the two acts, or a Pink row retired, is another plan.
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
    #: The ContentLink every added row is given, and how many live rows carry
    #: it (U126). Read once, at plan time, from the library, and None when the
    #: plan adds no row, since a landing that writes no row needs no value.
    link: row_link.LibraryLink | None
    digest: str
    #: The account playlists, each its own INBOX playlist (U113). The batch
    #: playlist, ``playlist``, holds only the rows none of them holds.
    playlists: tuple[PlaylistPlan, ...] = ()
    #: The sync pass the landing was given with ``--pass``, recorded with the
    #: commit under :data:`PASS_KEY` (R-777). None for a landing of no pass.
    pass_name: str | None = None
    #: The hearts among the rows and where they go (U120). None when the pass
    #: asked for no heart among these files, or the landing has no pass.
    favorites: FavoritesPlan | None = None
    #: The set's permanent playlist (U121), written in this same commit under
    #: the declared INSPIRATION folder, for a landing given ``--set``. None
    #: for every other landing.
    set_playlist: set_playlist.SetPlaylistPlan | None = None
    #: The label filing under the Record Labels tree (U156), planned by the
    #: caller on this handle over the same targets, or None when not asked for.
    labels: label_filing.LabelPlan | None = None
    #: The INBOX playlist an earlier landing of the same set job made (U135),
    #: which this write adds to; empty when the write finds or makes the
    #: playlist by its set name under the intake root.
    batch_playlist_id: str = ""
    #: The set job a landing given ``--set`` records on its batch playlist
    #: (U135), empty for every other landing.
    set_job_id: str = ""
    #: INBOX playlist names that look like earlier parts of this set from
    #: before U135, named on the screen and never joined automatically.
    inbox_leftovers: tuple[str, ...] = ()
    #: True when a set landing found a live INBOX playlist of the set's name
    #: that no earlier landing of this job recorded (U135), so the screen can
    #: say so apart from making one.
    inbox_found_by_name: bool = False
    #: The left rows of each account playlist that holds nothing here and so
    #: is not planned (U128), by its name, which the screen counts, the digest
    #: covers and the landing names.
    unplanned_left: tuple[tuple[str, Left], ...] = ()
    #: The calibrated with vox cut the scores were read against (U127), the one
    #: :func:`cratekit.write.metadata_cli.load_vocal_threshold` reads. None
    #: when the plan adds no row or the library recorded no calibration.
    vox_cut: float | None = None
    #: Why no added row is given the vox My Tag at all, a sentence, else empty.
    vox_blocked: str = ""
    #: The drift cut each added row's reading was judged against (U157),
    #: ``analysis.drift_cut``. None when the plan adds no row.
    drift_cut: float | None = None
    #: Why no variable row is given the dyn My Tag, a sentence, else empty.
    dyn_blocked: str = ""
    #: The live :data:`ANALYZE` playlist under the root the plan found (U166),
    #: empty when the write makes it.
    analyze_playlist_id: str = ""
    #: The folder a landing moves its files into (U164), chosen on the plan's
    #: handle and carried so the screen, the write and every row's target name
    #: one folder. None for a plan whose files are already in place.
    folder: Path | None = None
    #: The batch the folder is filed for, recorded with it (U164).
    batch: str = ""
    #: Where adoption would file each row to be added (U165), a
    #: :class:`cratekit.intake.filing.Prediction` per row, given by
    #: :func:`with_filing`. None for a landing that files nothing after it.
    filing: tuple[Any, ...] | None = None
    #: The custom playlist twins (U149), a ``sync.twins.LandingTwin`` per
    #: account playlist in ``playlists`` not paired yet, each written in this
    #: same commit with its INBOX playlist's rows, under ``Custom Playlists
    #: <year>``.
    twins: tuple[Any, ...] = ()

    def to_add(self) -> tuple[RowPlan, ...]:
        return tuple(row for row in self.rows if row.action == ADD)

    def vox_tagged(self) -> tuple[RowPlan, ...]:
        """The rows to be added that are given the vox My Tag (U127)."""
        return tuple(row for row in self.to_add() if row.vox)

    def vox_unscored(self) -> tuple[RowPlan, ...]:
        """The rows to be added whose file gave no score to read, and so no tag.

        Empty when no score was read at all, which ``vox_blocked`` says why.
        """
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
    #: ``rb_file_id`` as the table holds it after the commit, as text (U115).
    file_id: str = ""
    #: ``ContentLink`` as the table holds it after the commit (U126), None for NULL.
    content_link: int | None = None
    #: Whether the row carries the vox My Tag as adoption reads it, after the commit (U127).
    vox: bool = False
    #: Whether the row carries the dyn My Tag as ``analyze check`` reads it (U157).
    dyn: bool = False
    #: The row's words and year as the table holds them after the commit,
    #: through active lookup rows only, and as the plan gave them (U163).
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
    #: The account playlists written (U113). ``playlist_id`` is empty when every
    #: row went into one of these and the batch playlist held none.
    playlists: tuple[WrittenPlaylist, ...] = ()
    #: The hearts placed into All Favorites and their months (U120), in the
    #: same commit. None when the plan placed none.
    favorites: placement.Placed | None = None
    #: The set's permanent playlist written under INSPIRATION (U121), or None.
    set_playlist: set_playlist.Written | None = None
    #: What the commit filed under the Record Labels tree (U156), or None.
    labels: label_filing.Written | None = None
    #: The ContentLink the plan gave every added row (U126), which the read
    #: back is held to. None when the plan added no row.
    content_link: int | None = None
    #: Each account playlist track no INBOX playlist holds, by playlist name
    #: (U128): the plan's left rows and the members whose file did not land.
    left: tuple[tuple[str, Left], ...] = ()
    #: How many vox My Tag associations the commit wrote (U127).
    vox_written: int = 0
    #: Each added row's file that gave no score, so carries no tag (U127).
    vox_unscored: tuple[Path, ...] = ()
    #: Why no added row was given the tag at all, else empty (U127).
    vox_blocked: str = ""
    #: Each added row the plan tagged that adoption's reader does not answer
    #: after the commit (U127), so it reaches no with vox playlist.
    vox_missing: tuple[Path, ...] = ()
    #: Why adoption's reader could not answer after the commit, else empty.
    vox_unread: str = ""
    #: How many dyn My Tag associations the commit wrote (U157).
    dyn_written: int = 0
    #: Each added row whose file's drift read as variable, tagged or not.
    dyn_variable: tuple[Path, ...] = ()
    #: Each added row whose file carries no drift reading, so no tag.
    dyn_unscored: tuple[Path, ...] = ()
    #: Why no variable row was given the tag, else empty.
    dyn_blocked: str = ""
    #: Each added row the plan tagged dyn that the check's reader does not
    #: answer after the commit, and why it could not read, else empty.
    dyn_missing: tuple[Path, ...] = ()
    dyn_unread: str = ""
    #: The :data:`ANALYZE` playlist the commit added the rows to (U166), and
    #: its display name, empty when no row was added.
    analyze_id: str = ""
    analyze_name: str = ""
    #: How many memberships of it the commit added.
    analyze_added: int = 0
    #: The custom playlist twins the commit wrote (U149), a
    #: ``sync.twins.LandedTwin`` each, which the caller pairs.
    twins: tuple[Any, ...] = ()

    def names(self) -> tuple[str, ...]:
        """Every INBOX playlist the commit wrote, the batch's first when it wrote one."""
        batch = (self.playlist,) if self.playlist_id else ()
        return (*batch, *(written.name for written in self.playlists))


def recorded_inbox_playlist(
    cfg: config.Config, db: Any, job_id: str, root_id: str
) -> tuple[str, str] | None:
    """The INBOX playlist an earlier landing made for this set job, its id and name.

    THE SESSION RECORD IS THE JOB'S MEMORY OF ITS INBOX PLAYLIST (U135), the
    same shape :func:`cratekit.intake.set_playlist.recorded_playlist` uses for
    the permanent playlist under INSPIRATION. A closed landing whose batch
    playlist detail names this job and whose source committed, newest first.
    A recorded playlist that is gone, removed, or no longer under the intake
    root is not an answer, and the write finds or makes one by the set's name.
    """
    records, _unreadable = session.scan_log(cfg)
    found = [
        record
        for record in records
        if record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(BATCH_PLAYLIST_KEY), Mapping)
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id
    ]
    for record in sorted(found, key=lambda one: one.session_id, reverse=True):
        kept = record.detail[BATCH_PLAYLIST_KEY]
        playlist_id = str(kept.get("id") or "")
        if not playlist_id:
            continue
        row = db.get_playlist(ID=playlist_id)
        if (
            row is None
            or rb_writer.is_folder(row)
            or rb_writer.node_removed(row)
            or str(getattr(row, "ParentID", "") or "") != root_id
        ):
            continue
        return playlist_id, str(getattr(row, "Name", "") or kept.get("name") or "")
    return None


def leftover_set_inbox(
    cfg: config.Config,
    db: Any,
    job_id: str,
    root_id: str,
    set_name: str,
    *,
    keep_id: str = "",
) -> tuple[str, ...]:
    """INBOX playlist names that look like earlier parts of this set from before U135.

    A numbered twin of the set's name (``Name 2``) under the intake root, or a
    dated batch playlist an earlier ``--set`` landing of this job wrote before
    the record carried the job key. Named on the screen for the author; never
    joined automatically.
    """
    named: list[str] = []
    prefix = set_name + " "
    for held in inbox_held(db, root_id):
        if held == set_name:
            continue
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)
    records, _unreadable = session.scan_log(cfg)
    for record in records:
        if record.state is not session.SessionState.CLOSED:
            continue
        if str(session.SourceState.COMMITTED) not in record.sources.values():
            continue
        kept_set = record.detail.get(set_playlist.RECORD_KEY)
        if not isinstance(kept_set, Mapping) or kept_set.get("job") != job_id:
            continue
        batch = record.detail.get(BATCH_PLAYLIST_KEY)
        if not isinstance(batch, Mapping):
            continue
        if batch.get(INBOX_JOB_KEY):
            continue
        playlist_id = str(batch.get("id") or "")
        name = str(batch.get("name") or "")
        if not name or name == set_name or playlist_id == keep_id:
            continue
        if playlist_id:
            row = db.get_playlist(ID=playlist_id)
            if (
                row is None
                or rb_writer.is_folder(row)
                or rb_writer.node_removed(row)
                or str(getattr(row, "ParentID", "") or "") != root_id
            ):
                continue
            name = str(getattr(row, "Name", "") or name)
        if name and name not in named:
            named.append(name)
    return tuple(named)


def analyze_playlist(db: Any, root_id: str) -> Any | None:
    """The live, ordinary :data:`ANALYZE` playlist directly under the root, or None (U166).

    THE ONE FIND, for the landing that fills it and the clear that empties it,
    so the two never disagree about which playlist it is. A removed node is
    not found, for :func:`_batch_playlist_row`'s reason, and neither is a
    folder or a smart playlist of the name, which holds no membership a
    writer may add. Of two live ones the first the table lists is taken.
    """
    for row in list(db.get_playlist(Name=ANALYZE)):
        if str(getattr(row, "ParentID", "") or "") != str(root_id):
            continue
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
            continue
        return row
    return None


def inbox_held(db: Any, root_id: str) -> tuple[str, ...]:
    """Every name a live node anywhere under the intake root carries (U113).

    What a landing's account playlists are named against. Every descendant and
    not only the root's children, so a batch the rotation moved into ``Old``
    still holds its name. A removed node holds none: rekordbox no longer shows
    it, and an account playlist is created, never found by its name, so a
    removed node of that name is never written into.
    """
    return tuple(str(getattr(row, "Name", "") or "") for row in inbox_nodes(db, root_id))


def inbox_nodes(db: Any, root_id: str) -> tuple[Any, ...]:
    """Every live node anywhere under the intake root, folders included, in walk order.

    THE ONE WALK of what INBOX holds, :func:`inbox_held`'s names and the INBOX
    refill's playlists (U134), so the two never disagree about what is under
    the root.
    """
    # ONE READ OF THE TABLE, walked in memory, rather than a query per node.
    children: dict[str, list[Any]] = {}
    for row in list(db.get_playlist()):
        if not rb_writer.node_removed(row):
            children.setdefault(str(getattr(row, "ParentID", "") or ""), []).append(row)
    found: list[Any] = []
    pending = [str(root_id)]
    while pending:
        for row in children.get(pending.pop(), ()):
            found.append(row)
            pending.append(str(row.ID))
    return tuple(found)


def _playlist_identity(one: PlaylistPlan) -> dict[str, Any]:
    """One account playlist as the digest covers it, the owned rows and the left ones too.

    KEYS ADDED ONLY WHEN THERE ARE ANY, so a playlist of new files alone keeps
    the keys it had before U128; its targets are in the account playlist's
    order since then.
    """
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
    # THE VOX TAG ONLY WHEN A ROW IS ADDED (U127), the cut, why none, and each
    # added row's score and answer, so an approval given before a file was
    # rescored or the library recalibrated is stale for the tags it would write.
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
    # THE DYN TAG ONLY WHEN A ROW IS ADDED (U157), the cut, why none, and each
    # added row's drift, verdict and answer, so an approval given before a file
    # was rescored or the cut was changed is stale for the tags it would write.
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
    # THE ANALYZE PLAYLIST ONLY WHEN A ROW IS ADDED (U166), found or made, so
    # a plan that adds none digests as it did before this unit.
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
    # THE FILING ONLY WHEN THE LANDING FILES (U165), every prediction, so an
    # answer given for a landing that files is stale for one that does not.
    filing = (
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
    )
    # THE TWINS ONLY WHEN THERE ARE ANY (U149), so a landing with no account
    # playlist, or only paired ones, digests as it did before this unit.
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
        # THE LIBRARY BY ITS DEVICE AND MASTER ID, NEVER THE FILE (U161, R-922).
        # A rehearsal reads a copy at another path by design, so a digest that
        # named the file could never equal the live one; the screen names the
        # path, outside the digest.
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

    The binding stores the path it was given to stat and the first device it
    finds. Both are corrected here when they differ from the plan, on the
    object before the flush the guard performs, so the guard judges the row as
    it will be stored. A row the binding got right is left alone. Every column
    of :data:`cratekit.core.rb_writer.CONTENT_ROW_DEFAULTS` the binding left
    NULL is given rekordbox's own value the same way (R-923), the random
    file id the binding minted is replaced by the landed file's inode (U115),
    and the binding's ContentLink by the library's own (U126).
    """
    # THE MINTED ID IS COERCED TO TEXT (U153). ``generate_unused_id`` returns
    # an int and the ID column is text, so the row reads back as a string on
    # every later open, which is why this package stores ``str(content.ID)``
    # everywhere. The in-memory int is the one place the two forms diverge, and
    # it bit when the landing first dirtied an EXISTING content row in the same
    # commit as a new one, to colour a heart Pink: a flush cannot order a
    # djmdContent set whose pending rows mix an int ID and the text IDs every
    # stored row carries. Setting it to its stored form here, on the object
    # before the guard's flush, removes the divergence rather than the symptom.
    content.ID = str(content.ID)
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
    if str(content.MasterDBID) != plan.master_db_id:
        content.MasterDBID = plan.master_db_id
    # THE FILE ID IS THE INODE OF THE LANDED FILE, read now (U115). The binding
    # minted a random one on the row it made, and rekordbox will not load such
    # a row to a deck, so it is replaced on every row, never kept. It cannot be
    # handed to ``add_content``, which names the column itself.
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
    # THE LIBRARY'S CONTENTLINK, AS PLANNED (U126). The binding set it from the
    # TRACK menu item's counter and rekordbox will not load a row carrying
    # that, so it is replaced on every row with the value the screen showed.
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
    # REKORDBOX'S OWN DEFAULTS, ON THE SAME OBJECT BEFORE THE SAME FLUSH (R-923).
    # The binding leaves these NULL, and rekordbox will not load such a row to a
    # deck. Only a NULL is filled, so a value the binding chose stands.
    for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items():
        if getattr(content, column, None) is None:
            setattr(content, column, value)


def file_id_of(path: Path) -> int:
    """The value rekordbox writes to ``rb_file_id`` for a file it imports: its inode (U115)."""
    return os.stat(path).st_ino


def _holding(match: trees.RowMatch) -> str | None:
    """The active row a match names, the first of several when two claim it."""
    if match.content_id:
        return str(match.content_id)
    if match.content_ids:
        return str(match.content_ids[0])
    return None


def candidate_rows(db: Any, names: Iterable[str]) -> list[trees.ContentRow]:
    """The active rows whose stored path ends in one of ``names``, as the matcher reads them.

    A CANDIDATE SET, NOT THE ANSWER. The rows are found by the file name at
    the end of the stored path, which is the one part of it the base drive and
    the mounted spelling share, and every candidate is then put through the
    same resolver the plan used. That keeps the one rule for comparing a path
    on this machine with a path rekordbox wrote down, and reads a handful of
    rows instead of the collection.
    """
    from pyrekordbox.db6 import tables

    found: list[trees.ContentRow] = []
    for name in set(names):
        query = db.session.query(tables.DjmdContent).filter(
            tables.DjmdContent.FolderPath.like(f"%{name}")
        )
        for row in query.all():
            found.append(
                trees.ContentRow(
                    content_id=str(row.ID),
                    recorded=str(getattr(row, "FolderPath", "") or ""),
                    deleted=trees.soft_delete_marker(row),
                )
            )
    return found


def content_ids_for(db: Any, cfg: config.Config, paths: Sequence[Path]) -> dict[str, str]:
    """The active row holding each of ``paths``, by path, paths no row holds left out.

    THE ONE RULE FOR A PATH ON THIS MACHINE AGAINST A PATH REKORDBOX WROTE
    DOWN, asked of the candidate rows rather than the whole collection. The
    apply asks it of its targets below, and the favourites backfill (U120)
    asks it of the files the hearts resolve to. Two active rows on one path
    answer the first, which the matcher surfaces for the person to tidy.
    """
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    matches = trees.match_active_rows(
        list(paths),
        candidate_rows(db, (path.name for path in paths)),
        root=cfg.library.root,
        prefix_map=prefix_map,
    )
    found: dict[str, str] = {}
    for path, match in zip(paths, matches):
        held = _holding(match)
        if held is not None:
            found[str(path)] = held
    return found


def single_rows_for(db: Any, cfg: config.Config, paths: Sequence[Path]) -> dict[str, str]:
    """The one active row holding each of ``paths``, by path, a path two rows claim left out.

    :func:`content_ids_for` WITHOUT ITS FALLBACK, for a reader that must not
    guess: a file two active rows claim answers nothing here, the rule an
    owned member of an account playlist is found by (U128), so an owned heart
    (U146) never joins All Favorites as whichever duplicate came first.
    """
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    matches = trees.match_active_rows(
        list(paths),
        candidate_rows(db, (path.name for path in paths)),
        root=cfg.library.root,
        prefix_map=prefix_map,
    )
    return {
        str(path): str(match.content_id)
        for path, match in zip(paths, matches)
        if match.outcome is trees.MatchOutcome.MATCHED and match.content_id
    }


def dyn_marked(db: Any) -> frozenset[str]:
    """Every content row carrying a live My Tag value named :data:`DYN_VALUE`.

    THE ONE READER OF THE MARK, here beside the writer and called by
    ``crate analyze check`` as well as by the landing's read back, so what
    the landing reports as marked is what the check reads as marked.
    """
    marked: set[str] = set()
    for tag in db.get_my_tag(Name=DYN_VALUE):
        if rb_writer.soft_deleted(
            tag,
            message=(
                f"the My Tag row {getattr(tag, 'ID', '?')!r} cannot say whether rekordbox "
                f"removed it, so which rows are marked {DYN_VALUE} was not read"
            ),
            origin=_ORIGIN,
            detail={"my_tag_id": str(getattr(tag, "ID", ""))},
        ):
            continue
        for song in db.get_my_tag_songs(MyTagID=str(tag.ID)):
            if rb_writer.soft_deleted(
                song,
                message=(
                    f"the My Tag membership {getattr(song, 'ID', '?')!r} cannot say whether "
                    f"rekordbox removed it, so which rows are marked {DYN_VALUE} was not read"
                ),
                origin=_ORIGIN,
                detail={"song_my_tag_id": str(getattr(song, "ID", ""))},
            ):
                continue
            marked.add(str(song.ContentID))
    return frozenset(marked)


def live_inbox_named(db: Any, name: str, root_id: str) -> bool:
    """Whether a live (not removed) playlist of ``name`` sits under the intake root."""
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False


def assert_names_still_free(db: Any, plan: NativePlan) -> None:
    """Refuse an account playlist name INBOX came to hold after the plan chose it.

    ASKED BY THE LANDING BEFORE ITS FIRST MOVE, so a refusal leaves the files in
    staging for the landing to be run again, and asked again here before the
    first row, inside the session, for whatever took a name in between.
    """
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


def landed_passes(cfg: config.Config) -> tuple[str, ...]:
    """Every pass name a closed native landing committed, in name order (U174).

    THE NATIVE COUNTERPART OF THE INTAKE FILES AT THE LIBRARY ROOT, which is how
    ``crate organize`` finds the passes it marks (R-915). Read by the rule
    :func:`landings_of_pass` reads, so a pass listed here is one that function
    proves. A landing of no pass names none and is not listed. The names are
    every pass's, a label's or a set's as well as a sync's: which of them a
    sync pass owns is the mark's to decide, from its jobs.

    Read through :func:`cratekit.core.session.records`, so a log this account
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
    return tuple(
        sorted(
            {
                str(record.detail.get(PASS_KEY))
                for record in records
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
        )
    )


def landings_of_pass(cfg: config.Config, name: str) -> tuple[str, ...]:
    """The session ids of every closed native landing that committed ``name``.

    THE PROOF ``sync mark --pass`` WAITS FOR (R-777), the native counterpart of
    an intake file: a record of this workflow, closed, whose intake source
    committed and whose detail names the pass. A landing refused after its
    moves leaves its files in the library and adds no row, and its record
    names no pass, so its files cannot mark a playlist by being on disk.

    A LOG THIS ACCOUNT CANNOT LIST REFUSES (R-1255, review round two), through
    :func:`cratekit.core.session.records`: read as no landing, ``sync mark
    --pass`` told a person a recorded landing never committed and sent them to
    land the pass again.
    """
    records = session.records(cfg)
    return tuple(
        sorted(
            record.session_id
            for record in records
            if record.workflow == WORKFLOW
            and record.state is session.SessionState.CLOSED
            and str(session.SourceState.COMMITTED) in record.sources.values()
            and record.detail.get(PASS_KEY) == name
        )
    )


def assert_rows_gridless(landed: NativeLanded) -> None:
    """Refuse when a row read back after the commit carries an analysis value.

    THE GUARD HOLDS THIS BEFORE THE COMMIT, so reaching here is a defect in the
    guard rather than in the landing, and it is reported as one. The read is
    made anyway, because the record promises a column by column statement about
    the rows as rekordbox will find them, and a promise checked only before the
    write is a promise about a different moment.
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

    THE RESTAMP SETS BOTH BEFORE THE COMMIT and the read back reports them
    after, so reaching here means the binding or a guard dropped a column on
    the way to the table, and the row carries a value rekordbox will not load:
    a file id that is not its file's inode (U115), or a ContentLink that is not
    the one the plan read off the library (U126). The write is durable, so the
    refusal names the session whose capture undoes it.
    """
    wrong = [
        f"{row.content_id}: {rb_writer.FILE_ID_COLUMN} = {row.file_id!r}, "
        f"the file's inode is {file_id_of(row.target)}"
        for row in landed.added
        if str(row.file_id) != str(file_id_of(row.target))
    ]
    # NO SKIP: a row added with no value planned is as wrong as a row whose
    # value did not take, and None never equals a value read back.
    wrong += [
        f"{row.content_id}: {rb_writer.CONTENT_LINK_COLUMN} = {row.content_link!r}, "
        f"the library's is {landed.content_link!r}"
        for row in landed.added
        if landed.content_link is None or row.content_link != landed.content_link
    ]
    # THE WORDS AND THE YEAR (U163), read through active lookup rows, so a
    # link that did not take or names a tombstone reads as a word missing.
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


# THE PLAN AND THE APPLY, re-exported: they import this module's types, so
# they are imported last, and every caller keeps reaching them here.
from cratekit.intake.native_apply import (  # noqa: F401
    _analyze_row,
    _assert_words_unmoved,
    _batch_playlist_row,
    _dyn_read_back,
    _landed_rows,
    _Mints,
    _plain,
    _read_back,
    _record_landing_commit,
    _resolved_now,
    _rows_of,
    _tag_dyn,
    _tag_vox,
    _taken_since_the_plan,
    _vox_read_back,
    _words_back,
    apply_rows,
)
from cratekit.intake.native_plan import (  # noqa: F401
    _DRIFT_TAGS,
    _WORD_TAGS,
    SEARCH_EMPTY,
    SEARCH_NAME,
    _active_album_id,
    _active_id,
    _dyn_plan,
    _favorites_plan,
    _lookup_class,
    _property,
    _Resolver,
    _supported_only,
    _vox_plan,
    _word,
    _words_plan,
    anchored_intake_root,
    choose_device,
    file_type_of,
    plan_rows,
    search_convention,
    stored_folder_path,
    with_filing,
    year_of,
)
