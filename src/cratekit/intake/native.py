"""Land a batch in the collection through the guarded database writer (R-746).

The xml landing ends on five hand steps in rekordbox: point it at the intake
file, import one playlist, drag it into the intake folder, export again, run
``intake imported``. On a library whose intake tree has cut over, this engine
is the other medium: one content row per landed file and one batch playlist
under the adopted intake root, through the same session spine every database
tree writer uses, behind a plan and an approval the verb owns.

THIS IS A NEW KIND OF WRITE, and it is treated the way the cutover was. Every
row the guarded writer added before this unit was a membership, a playlist, a
folder or a tag association on rows rekordbox created. A CONTENT row is the
row rekordbox analyses into, so what it may carry is stated as a column policy
and asserted from SQL before the commit, in ``rb_writer``, and read back after
it here. The row carries what the file's tags and the filesystem say: a title,
a path, a name, a size, a type. Every column an analysis pass fills stays
empty for rekordbox to fill, and :data:`LEFT_EMPTY` names them so the record
and the envelope can say so.

WHAT SITTING 17 SETTLED, and this module obeys (A8, 2026-09-29, rekordbox
7.2.19, the live library):

* the stored path is under ``djmdProperty.BaseDBDrive``, which on a renamed
  volume is not the mounted path; rekordbox's own rows are, including rows it
  imported the same day. The binding is handed the mounted path to stat and the
  row is restamped with the base drive form before the commit;
* the device is the one whose ``MasterDBID`` equals the property table's
  ``DBID``. A library can hold two devices and the binding's default is order
  dependent, so the choice is made here and asserted, never trusted;
* the binding's bare row, ``add_content(path, Title=...)`` with every analysis
  column NULL, behaved exactly as a row dressed in rekordbox's own not yet
  analysed shape, so the simpler row is the one written;
* rekordbox analyses nothing on its own with Auto Analysis off. The answer
  says the rows await analysis. Triggering it is not this engine's.

WHAT SITTING 34 SETTLED (U115, R-928, 2026-10-09): a row the binding makes
carries a random ``rb_file_id`` and rekordbox will not load it to a deck,
whatever else the row holds. rekordbox's own value is the file's inode number
at the moment of import, so each row here is created with
``os.stat(target).st_ino``, read on the landed file at the moment the row is
made, never from the plan: staging may sit on another volume, where the inode
is another number. The screen names the column with
:data:`FILE_ID_AT_LANDING` rather than a value, so what was approved and what
was written cannot differ by a number the plan could not know.

WHAT SITTING 37 SETTLED (U126, R-928, 2026-10-10): a row the binding makes
carries the ``ContentLink`` the binding takes from a menu item's counter, and
rekordbox will not load it to a deck until it carries the value rekordbox
writes on its own rows. That value is read from the library at plan time,
:func:`cratekit.write.row_link.library_link`, the one more than half its live
rows carry, shown on the screen and covered by the digest, and set on each
row here. A library with no such value refuses before the gate.

THE PLAN IS BUILT AGAINST THE DATABASE AND THE APPLY REBUILDS NOTHING. The
verb opens the database with write intent, so an open rekordbox refuses before
anything is shown, plans every row and its columns, and digests them; the
person approves that digest. The apply takes the plan as approved and writes
it, and asks the database again only for what the plan could not know, which
is whether a row appeared between the two.

A PLAYLIST THE AUTHOR MADE ON THE ACCOUNT GETS ITS OWN (U113). A landing hands
the plan its account playlists, each named against :func:`inbox_held` and each
holding the rows it claimed; they are created under the root, never found by
name, so two landings never share one, and the batch playlist keeps the rest.
A landing given ``--set`` is the exception since U135: its INBOX playlist is
named for the set and a later landing of the same job adds to the playlist
the first one recorded, under its first name.
The record names every one by identifier, which is what ``inbox rotate`` ages
them by.

EVERY ROW A LANDING CREATES ALSO JOINS ONE PLAYLIST, :data:`ANALYZE` (U166),
directly under the intake root, found live or made in the same commit, so the
rekordbox visit selects that one playlist and runs Analyze Track over exactly
the rows waiting for it. Nothing else adds to it; ``crate inbox analyzed``
takes out each row rekordbox has analysed. A row the collection already held
is not added, since rekordbox has had it. No record names it as a batch, so
the rotation leaves it where it is.

``plan_rows`` AND ``apply_rows`` MEAN SOMETHING ELSE IN ``cratekit.tagging.rows``,
where a row is one that exists and whose genre is written from its file. Here
a row is a content row this engine adds. The two are not interchangeable.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

from cratekit.adopt import placements as adopt_placements
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    snapshot,
    tags,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.favorites import colour as colour_mod
from cratekit.favorites import placement
from cratekit.intake import ingest, label_filing, set_playlist
from cratekit.write import metadata, metadata_cli, routing_pass, row_link, trees

if TYPE_CHECKING:
    # The landing's own types, imported for annotation only: the module that
    # defines them reaches this one through the batch name and the landing.
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

#: The session record field listing the account playlists a landing wrote, each
#: by identifier and name (U113). The intake's one spelling, shared with the
#: intake file's record.
INBOX_PLAYLISTS_KEY = ingest.INBOX_PLAYLISTS_KEY

#: The playlist directly under the intake root every row a landing creates
#: joins (U166), so the rekordbox visit selects one playlist. Its display
#: form is ``<intake root> / Analyze``. Reserved: :func:`plan_rows` refuses a
#: batch of the name and an account playlist of it is named ``Analyze 2``,
#: through :data:`cratekit.intake.batch_name.ANALYZE`, which spells the same
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

_ORIGIN = ("intake.native",)


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

#: The lookup table each linked column names, and the tag its word is read from.
_WORD_TABLES: Mapping[str, str] = {
    ARTIST_COLUMN: rb_writer.ARTIST_TABLE,
    ALBUM_COLUMN: rb_writer.ALBUM_TABLE,
    GENRE_COLUMN: rb_writer.GENRE_TABLE,
}

#: The tags a row's words are read from, in one container open (U163).
_WORD_TAGS: tuple[str, ...] = ("artist", "album", "albumartist", "genre", "date")


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
    #: The :data:`ANALYZE` playlist the commit added the rows to (U166), and
    #: its display name, empty when no row was added.
    analyze_id: str = ""
    analyze_name: str = ""
    #: How many memberships of it the commit added.
    analyze_added: int = 0

    def names(self) -> tuple[str, ...]:
        """Every INBOX playlist the commit wrote, the batch's first when it wrote one."""
        batch = (self.playlist,) if self.playlist_id else ()
        return (*batch, *(written.name for written in self.playlists))


def _property(db: Any) -> Any:
    from pyrekordbox.db6 import tables

    return db.session.query(tables.DjmdProperty).first()


def choose_device(db: Any) -> tuple[str, str]:
    """The device whose ``MasterDBID`` is the library's own, as (device id, master id).

    ASSERTED, NEVER TRUSTED. ``add_content`` stamps the first device the query
    returns, and the author's library holds two, one per machine that has ever
    opened it. A row stamped with the other machine's device is a plausible way
    to get an invisible or cloud confused row, so the device is chosen here by
    the one rule that identifies the library, and the row is restamped when the
    binding chose differently. Several matches take the lowest identifier, so
    the answer is a function of the database and not of query order.
    """
    from pyrekordbox.db6 import tables

    property_row = _property(db)
    dbid = None if property_row is None else str(getattr(property_row, "DBID", "") or "")
    devices = list(db.session.query(tables.DjmdDevice).all())
    matching = sorted(
        (device for device in devices if dbid and str(device.MasterDBID) == dbid),
        key=lambda device: str(device.ID),
    )
    if not matching:
        raise refuse(
            "collection-unreadable",
            f"no device row in the database carries the library's own identifier "
            f"{dbid!r}, so a content row could not be stamped with the device that "
            f"owns this library; {len(devices)} device row(s) were read",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"dbid": dbid, "devices": [str(device.ID) for device in devices]},
        )
    return str(matching[0].ID), str(matching[0].MasterDBID)


def stored_folder_path(path: Path, *, base_drive: str | None, current_drive: str | None) -> str:
    """The ``FolderPath`` rekordbox's own rows would carry for a mounted ``path``.

    UNDER THE BASE DRIVE, NOT THE MOUNTED ONE. ``djmdProperty`` records where
    the database was made and where it is now, and rekordbox remaps the first
    to the second at runtime, so a row stored under the mounted path on a
    renamed volume is the odd one out. When the two differ and the path is
    under the current drive, the prefix is swapped; a library whose drive has
    never moved, and a path outside the drive, are stored as they are. NFC,
    because rekordbox stores NFC and the filesystem may hand back NFD, and one
    byte of difference is a second row for one file (KTD27).
    """
    text = locations.norm_for_compare(str(path))
    if base_drive and current_drive and base_drive != current_drive:
        current = locations.norm_for_compare(current_drive).rstrip("/\\")
        if text == current or text.startswith(current + os.sep):
            return locations.norm_for_compare(base_drive).rstrip("/\\") + text[len(current) :]
    return text


def file_type_of(path: Path) -> int | None:
    """The binding's file type for ``path``'s suffix, or None when it has none.

    The binding's own lookup raises the wrong exception class on a suffix it
    does not know, and it does so after the duplicate check, so it is asked
    here at plan time. None rather than a refusal, because the answer is one
    file's and the batch still lands: the file is planned as
    :data:`UNSUPPORTED` and stays in staging, the way an occupied target does.
    The xml landing takes every suffix ``AUDIO_EXTS`` names, since a Location
    is text, so a file this medium cannot name is not lost to the library.
    """
    from pyrekordbox.db6.tables import FileType

    name = path.suffix.lstrip(".").upper()
    found = getattr(FileType, name, None) if name else None
    return None if found is None else int(found.value)


def anchored_intake_root(db: Any, tree_id: str, registry: tree_registry.Registry) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``.

    THROUGH THE SHARED ASSERTION, which refuses a tree still on the bridge, a
    native record naming no root, and a root this library does not have. The
    first is rephrased in this verb's words with the verb that fixes it,
    because the shared refusal is written for a writer that arrived at the
    wrong medium by mistake and this one arrives there because the person has
    not cut the intake tree over yet.
    """
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so a landing "
            f"adds nothing to the collection through the database; the xml landing "
            f"takes --export, or cut the intake tree over first",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
                "or land with --export to splice the batch into that export as before",
            ),
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def plan_rows(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    batch: str,
    files: Sequence[tuple[Path, Path]],
    split: Sequence[PlaylistPlan] = (),
    unplanned_left: Sequence[tuple[str, Left]] = (),
    pass_name: str | None = None,
    hearts: Sequence[HeartItem] = (),
    favorites_source: str | None = None,
    owned_hearts: Sequence[OwnedHeartItem] = (),
    set_plan: set_playlist.SetPlaylistPlan | None = None,
    batch_playlist_id: str = "",
    set_job_id: str = "",
    inbox_leftovers: Sequence[str] = (),
    inbox_found_by_name: bool = False,
    labels: label_filing.LabelPlan | None = None,
) -> NativePlan:
    """Plan one row per file and one playlist, against the open database.

    ``hearts`` are the targets the pass's hearts job asked for, each with its
    month (U120, U145), and ``favorites_source`` the playlist every favourite is
    in. With both, the plan carries where each heart goes, resolved on this
    same handle; a home that cannot be resolved is a plan that SKIPS the
    placement and says why, never a refusal of the landing. ``owned_hearts``
    are the pass's hearts on rows the collection already holds (U146), the
    ones All Favorites lacks placed in the same commit.

    ``files`` pairs where each file is now with where the landing will put it.
    The row is planned for the target, since that is the path rekordbox will
    open, and the title is read off the source, since the tags do not move.

    ``split`` is a landing's account playlists (U113), named by the caller
    against :func:`inbox_held` on this same handle, each holding targets of
    ``files``. They are part of the plan and of its digest, and so are
    ``unplanned_left``, the left rows of the account playlists the caller found
    holding nothing (U128). ``set_plan`` is the
    set's permanent playlist (U121), planned by the caller on this same handle
    over the same targets, and part of the digest the same way. So is
    ``labels``, the label filing (U156), less any file this plan leaves in
    staging, each of which it names as filed nowhere.

    A FILE THE COLLECTION HOLDS IS PRESENT, NOT ADDED TWICE. The target is
    matched against every active row the way the membership writers match,
    through one index of the collection resolved on this machine, so a row
    stored under the base drive and a row stored under the mounted path both
    count. Two active rows on one path count as present too: adding a third
    is not the answer to a duplicate.
    """
    # THE QUEUE'S NAME IS RESERVED (U166). A batch playlist of that name would
    # be found as the queue and written into, and recorded as a batch the
    # rotation then moves into Old with every row still waiting in it.
    if batch == ANALYZE:
        raise refuse(
            "intake-list-unusable",
            f"the batch name {batch!r} is the playlist under INBOX every landing "
            f"fills with the rows awaiting analysis, so no batch may take it and "
            f"nothing was planned; land with another --name, or rename the file",
            origin=_ORIGIN,
            detail={"batch": batch},
        )
    root_id = anchored_intake_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    device_id, master_db_id = choose_device(db)
    base_drive, current_drive = rb_writer.recorded_db_drives(db)
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    index = trees.index_active_rows(
        routing_pass.content_rows(db), root=cfg.library.root, prefix_map=prefix_map
    )
    matches = trees.match_indexed_rows(
        [target for _source, target in files], index, root=cfg.library.root, prefix_map=prefix_map
    )
    rows: list[RowPlan] = []
    for (source, target), match in zip(files, matches):
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
            # NOT ABSENT, UNASKED (R-770). The matcher could not put the target
            # under the library root or a prefix rule, so it never looked for a
            # row, and planning an add over that is planning a second row for a
            # file the collection may hold. Every reader that resolves against
            # the root would drop the row it made, too.
            raise refuse(
                "intake-list-unusable",
                f"{target} resolves nowhere under the library at "
                f"{cfg.library.root} or its prefix rules, so the collection could "
                f"not be asked whether it already holds that file and no row was "
                f"planned for it",
                origin=_ORIGIN,
                detail={"target": str(target), "root": str(cfg.library.root)},
            )
        held = _holding(match)
        file_type = file_type_of(target)
        if file_type is None:
            action, why = (
                UNSUPPORTED,
                (
                    f"{target.name} has a suffix rekordbox's database has no file type "
                    f"for, so no content row can name it and it was left in staging; "
                    f"convert it, or land it through the xml bridge"
                ),
            )
        else:
            action, why = (ADD if held is None else PRESENT), ""
        rows.append(
            RowPlan(
                source=source,
                target=target,
                action=action,
                title=str(ingest.file_meta(source, cfg=cfg)["name"]),
                folder_path=stored_folder_path(
                    target, base_drive=base_drive, current_drive=current_drive
                ),
                file_name=target.name,
                file_size=source.stat().st_size,
                file_type=file_type or 0,
                content_link=None,
                content_id=held,
                why=why,
            )
        )
    # ONLY WHEN A ROW IS ADDED, and before anything is shown (U126). A
    # landing whose files the collection already holds writes memberships
    # alone, and a library with no value to give does not refuse it.
    link = (
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
    )
    if link is not None:
        rows = [
            replace(row, content_link=link.value) if row.action == ADD else row for row in rows
        ]
    rows, vox_cut, vox_blocked = _vox_plan(cfg, db, rows)
    rows = _words_plan(db, rows)
    kept, dropped = _supported_only(split, rows)
    if labels is not None:
        labels = label_filing.supported_only(
            labels, {str(row.target) for row in rows if row.action != UNSUPPORTED}
        )
    planned = NativePlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        playlist=batch,
        database=Path(rb_writer.handle_path(db) or rb_writer.live_db_path(cfg)),
        device_id=device_id,
        master_db_id=master_db_id,
        base_drive=base_drive,
        current_drive=current_drive,
        rows=tuple(rows),
        link=link,
        digest="",
        playlists=kept,
        unplanned_left=(*unplanned_left, *dropped),
        pass_name=pass_name,
        favorites=_favorites_plan(
            db, hearts, rows, source=favorites_source, owned=owned_hearts
        ),
        set_playlist=set_plan,
        labels=labels,
        batch_playlist_id=batch_playlist_id,
        set_job_id=set_job_id,
        inbox_leftovers=tuple(inbox_leftovers),
        inbox_found_by_name=inbox_found_by_name,
        vox_cut=vox_cut,
        vox_blocked=vox_blocked,
    )
    found = analyze_playlist(db, str(root_id))
    if found is not None:
        planned = replace(planned, analyze_playlist_id=str(found.ID))
    return replace(planned, digest=digest_of(identity(planned)))


def _vox_plan(
    cfg: config.Config, db: Any, rows: list[RowPlan]
) -> tuple[list[RowPlan], float | None, str]:
    """Each row to be added with its file's score and whether it is given the vox My Tag (U127).

    R-841'S DECISION: THE TAG OWNS THE VOCAL SUB, so a landing writes it from
    the same score and the same cut the routing passes read, and the tag a
    person filters by agrees with ``voxlevel`` from the moment the row exists.
    The cut is :func:`cratekit.write.metadata_cli.load_vocal_threshold`'s and
    the comparison is :func:`cratekit.write.metadata_cli.vocal_tag_values`',
    so a score exactly at the cut is tagged, as the vocals verb tags it.

    ONLY A ROW THIS LANDING ADDS. A row the collection already held is the
    repair's (A37), and a landing never removes a tag.

    NEVER A GUESS. No calibration recorded, or no My Tag category for the
    writer to copy, plans no tag on any row and says why in ``vox_blocked``.
    A file whose score cannot be read is planned with no score and no tag,
    and the landing names it. Read off the source, since the tags do not move.
    Answers the rows, the cut and the reason, in that order.
    """
    if not any(row.action == ADD for row in rows):
        return rows, None, ""
    try:
        cut = metadata_cli.load_vocal_threshold(cfg)
    except CratekitError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
        # routing passes refuse over it, and so does the vocals verb, which is
        # where the person repairs it; a batch held in staging over a tag the
        # landing can say it did not write would cost the whole intake.
        return rows, None, VOX_UNREADABLE.format(why=exc.cause.message)
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
    if not rb_writer.my_tag_writable(db):
        return rows, cut, VOX_NO_CATEGORY
    scored: list[RowPlan] = []
    for row in rows:
        if row.action != ADD:
            scored.append(row)
            continue
        level = tags.read_vox_from_file(row.source)
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
    return scored, cut, ""


def _words_plan(db: Any, rows: list[RowPlan]) -> list[RowPlan]:
    """Each row to be added with its artist, album and genre words and its year (U163).

    R-921'S ANSWER: THE LANDING WRITES WHAT RELOAD TAGS WROTE, so a landed row
    reads whole in rekordbox before anyone opens it and the visit is Analyze
    Tracks alone. Read off the source, since the tags do not move. Each word is
    resolved to the first active lookup row of its exact name, or planned as a
    mint, and the screen and the digest say which per row.

    NEVER THE KEY. ``KeyID`` is rekordbox's analysis and stays empty, as
    :data:`cratekit.core.rb_writer.CONTENT_ROW_EMPTY_COLUMNS` holds it, and the
    padded key the title head carries is Cratekit's own answer.

    ONLY A ROW THIS LANDING ADDS, as the vox tag is planned. A row the
    collection already held is ``crate tag rows``' to repair.
    """
    if not any(row.action == ADD for row in rows):
        return rows
    resolver = _Resolver(db)
    planned: list[RowPlan] = []
    for row in rows:
        if row.action != ADD:
            planned.append(row)
            continue
        read = tags.read_tags(row.source, _WORD_TAGS)
        artist = resolver.word(rb_writer.ARTIST_TABLE, _word(read["artist"]))
        album_artist = resolver.word(rb_writer.ARTIST_TABLE, _word(read["albumartist"]))
        planned.append(
            replace(
                row,
                artist=artist,
                album=resolver.album(_word(read["album"]), album_artist),
                genre=resolver.word(rb_writer.GENRE_TABLE, _word(read["genre"])),
                year=year_of(read["date"]),
            )
        )
    return planned


def _word(value: str | None) -> str:
    """A tag's first value as a lookup row's name, empty for a tag that holds only space.

    THE FIRST VALUE IN EVERY CONTAINER. The ID3 reader answers a multi-value
    frame as its values joined on NUL, where Vorbis and MP4 answer the first,
    and a NUL joined name is a lookup row no other row will ever share and a
    genre adoption files under nothing.
    """
    first = (value or "").split("\x00")[0]
    if not first.strip():
        return ""
    return first


def year_of(date: str | None) -> int | None:
    """The year a date tag opens with, as rekordbox's ``ReleaseYear`` holds it, else None (U163).

    The first four characters, when they are digits naming a year after zero,
    which covers the bare year, the ISO date and the ISO timestamp every
    tagger writes. Anything else is no year rather than a guess.
    """
    head = (date or "").strip()[:4]
    if len(head) != 4 or not head.isdigit() or int(head) == 0:
        return None
    return int(head)


class _Resolver:
    """The plan's lookup reads for one handle: each word resolved once, each table's convention read once (U163)."""

    def __init__(self, db: Any) -> None:
        self._db = db
        self._found: dict[tuple[str, str, str], str] = {}
        self._search: dict[str, str] = {}

    def word(self, table: str, name: str) -> Word | None:
        """The word for ``name`` in ``table``, linked or minted, or None for no name."""
        if not name:
            return None
        row_id = self._resolved((table, name, ""), lambda: _active_id(self._db, table, name))
        return self._shaped(Word(table=table, name=name, row_id=row_id))

    def album(self, name: str, album_artist: Word | None) -> Word | None:
        """The album word for ``name`` by ``album_artist``, or None for no name."""
        if not name:
            return None
        key = (rb_writer.ALBUM_TABLE, name, album_artist.name if album_artist else "")
        row_id = self._resolved(key, lambda: _active_album_id(self._db, name, album_artist))
        return self._shaped(
            Word(table=rb_writer.ALBUM_TABLE, name=name, row_id=row_id, album_artist=album_artist)
        )

    def _resolved(self, key: tuple[str, str, str], find: Any) -> str:
        if key not in self._found:
            self._found[key] = find()
        return self._found[key]

    def _shaped(self, word: Word) -> Word:
        """A mint given what its table stores in ``SearchStr``, a link as it is."""
        if word.row_id or word.table == rb_writer.GENRE_TABLE:
            return word
        if word.table not in self._search:
            self._search[word.table] = search_convention(self._db, word.table)
        convention = self._search[word.table]
        return replace(word, search=word.name if convention == SEARCH_NAME else convention)


def _lookup_class(table: str) -> Any:
    from pyrekordbox.db6 import tables

    return {
        rb_writer.ARTIST_TABLE: tables.DjmdArtist,
        rb_writer.ALBUM_TABLE: tables.DjmdAlbum,
        rb_writer.GENRE_TABLE: tables.DjmdGenre,
    }[table]


def _active_id(db: Any, table: str, name: str) -> str:
    """The first active row of ``table`` named exactly ``name``, as text, else empty."""
    rows = db.session.query(_lookup_class(table)).filter_by(Name=name)
    found = metadata.first_active_id(rows, table=table, name=name)
    return "" if found is None else str(found)


def _active_album_id(db: Any, name: str, album_artist: Word | None) -> str:
    """The first active album named ``name`` whose album artist is ``album_artist``'s row, else empty.

    An album artist the commit mints has no album yet, so its album is minted
    too. No album artist matches an album whose artist is empty.
    """
    if album_artist is not None and not album_artist.row_id:
        return ""
    want = album_artist.row_id if album_artist is not None else ""
    rows = [
        row
        for row in db.session.query(_lookup_class(rb_writer.ALBUM_TABLE)).filter_by(Name=name)
        if str(getattr(row, ALBUM_ARTIST, None) or "") == want
    ]
    found = metadata.first_active_id(rows, table=rb_writer.ALBUM_TABLE, name=name)
    return "" if found is None else str(found)


#: The ``SearchStr`` conventions :func:`search_convention` answers (U163): the
#: row's own name, the empty string, or NULL.
SEARCH_NAME = "name"
SEARCH_EMPTY = ""


def search_convention(db: Any, table: str) -> str | None:
    """What most active rows of ``table`` store in ``SearchStr``: their name, empty, or NULL (U163).

    UNMEASURED IN REKORDBOX, SO THE LIBRARY IS ASKED. What Reload Tags stores
    there was never read off a copy (the ideation's open question), and the
    library's own rows are the nearest witness, so a mint follows the
    majority of them, tombstones counted with the rest since they were stored
    by the same hand. A row storing anything else is not counted. A tie or a
    table with no counted row answers NULL, the binding's own default.
    """
    from collections import Counter

    counted: Counter[str | None] = Counter()
    for row in db.session.query(_lookup_class(table)):
        stored = getattr(row, "SearchStr", None)
        if stored is None:
            counted[None] += 1
        elif stored == "":
            counted[SEARCH_EMPTY] += 1
        elif stored == getattr(row, "Name", None):
            counted[SEARCH_NAME] += 1
    ranked = counted.most_common()
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
        return None
    return ranked[0][0]


def _favorites_plan(
    db: Any,
    hearts: Sequence[HeartItem],
    rows: Sequence[RowPlan],
    *,
    source: str | None,
    owned: Sequence[OwnedHeartItem] = (),
) -> FavoritesPlan | None:
    """Where the landing's hearts go, or None when it places none (U120, U146).

    AN OWNED HEART JOINS WHEN ALL FAVORITES DOES NOT HOLD IT LIVE (U146), so a
    heart a person took out of All Favorites by hand and still hearts on the
    account joins again: the author's rule of 2026-10-14 is that dropping a
    favourite takes both hand steps. A heart it holds already is no write.
    """
    writable = {str(row.target) for row in rows if row.action != UNSUPPORTED}
    kept = tuple(item for item in hearts if str(item.target) in writable)
    if not (kept or owned) or not source:
        return None
    try:
        home = placement.resolve_home(db, source)
    except CratekitError as exc:
        # THE ONE REFUSAL A LANDING ABSORBS: no source, or two. Anything else
        # the home's reading raised is the landing's refusal as it would be
        # any writer's, since a skipped placement over an unreadable table
        # would downgrade a fail closed check to a note.
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return FavoritesPlan(
            source_name=source,
            source_id="",
            folder_id="",
            folder_name="",
            items=(),
            skipped=exc.cause.message,
        )
    in_source = placement.members(db, home.source_id) if owned else frozenset()
    joining: list[OwnedHeartItem] = []
    seen: set[str] = set()
    for one in owned:
        if one.content_id in in_source or one.content_id in seen:
            continue
        seen.add(one.content_id)
        joining.append(one)
    if not kept and not joining:
        return None
    # THE COLOUR, READ ON THIS HANDLE (U153): the Pink row by name, absorbed
    # into a skip when the table has none, and each owned heart's colour now,
    # so only a row with none takes Pink and a row a person coloured is held.
    pink, colour_skipped = placement.read_pink(db)
    to_colour: tuple[str, ...] = ()
    held: tuple[colour_mod.Held, ...] = ()
    if pink and joining:
        sorted_rows = colour_mod.sort_rows(db, pink, [one.content_id for one in joining])
        to_colour, held = sorted_rows.to_colour, sorted_rows.held
    return FavoritesPlan(
        source_name=home.source_name,
        source_id=home.source_id,
        folder_id=home.folder_id,
        folder_name=home.folder_name,
        items=kept,
        present=tuple(sorted(home.present)),
        owned=tuple(joining),
        pink=pink,
        colour_skipped=colour_skipped,
        colour=to_colour,
        held=held,
    )


def _supported_only(
    split: Sequence[PlaylistPlan], rows: Sequence[RowPlan]
) -> tuple[tuple[PlaylistPlan, ...], tuple[tuple[str, Left], ...]]:
    """The account playlists over only the targets a row can be written for, and what was dropped.

    A file planned ``UNSUPPORTED`` stays in staging and no playlist can hold it,
    so it is not counted on the screen as one of a playlist's but listed as
    left. A playlist holding nothing else, new or owned, is not planned, and
    every left row it had is answered beside the kept ones by its name, so the
    landing still names it.
    """
    unsupported = {str(row.target) for row in rows if row.action == UNSUPPORTED}
    kept: list[PlaylistPlan] = []
    dropped: list[tuple[str, Left]] = []
    for one in split:
        members = tuple(
            member
            for member in one.members
            if member.target is None or str(member.target) not in unsupported
        )
        left = (
            *one.left,
            *(
                member.member.left(NOT_LANDED)
                for member in one.members
                if member.target is not None
                and str(member.target) in unsupported
                and member.member is not None
            ),
        )
        if members:
            kept.append(replace(one, members=members, left=left))
        else:
            dropped.extend((one.name, row) for row in left)
    return tuple(kept), tuple(dropped)


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
    # THE ANALYZE PLAYLIST ONLY WHEN A ROW IS ADDED (U166), found or made, so
    # a plan that adds none digests as it did before this unit.
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
    # THE FILING ONLY WHEN THE LANDING FILES (U165), every prediction, so an
    # answer given for a landing that files is stale for one that does not.
    filing = (
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
    )
    return {
        **split,
        **unplanned,
        **favorites,
        **kept,
        **filed,
        **vox,
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


def with_filing(plan: NativePlan, predicted: Sequence[Any]) -> NativePlan:
    """``plan`` with where adoption would file its rows, digested again (U165)."""
    filed = replace(plan, filing=tuple(predicted))
    return replace(filed, digest=digest_of(identity(filed)))


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


def _read_back(db: Any, content_id: str) -> tuple[dict[str, Any], str, str, str, int | None]:
    """The analysis columns, title, path, file id and link of one row, from SQL after the commit."""
    from sqlalchemy import text

    selected = ", ".join(LEFT_EMPTY)
    row = db.session.execute(
        text(
            f"SELECT Title, FolderPath, {rb_writer.FILE_ID_COLUMN}, "
            f"{rb_writer.CONTENT_LINK_COLUMN}, {selected} "
            f"FROM djmdContent WHERE ID = :id"
        ),
        {"id": content_id},
    ).first()
    if row is None:
        raise refuse(
            "internal-error",
            f"the content row {content_id!r} was committed and could not be read "
            f"back, so the landing cannot say what it holds",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"content_id": content_id},
        )
    values = dict(zip(LEFT_EMPTY, row[4:]))
    return (
        values,
        str(row[0] or ""),
        str(row[1] or ""),
        str(row[2] or ""),
        None if row[3] is None else int(row[3]),
    )


def _words_back(db: Any, content_id: str) -> dict[str, Any]:
    """One row's artist, album, album artist, genre and year, from SQL after the commit (U163).

    THROUGH ACTIVE LOOKUP ROWS ONLY, so a row linked to a tombstone reads as
    carrying no word, which is what rekordbox shows for it.
    """
    from sqlalchemy import text

    active = f"{rb_writer.SOFT_DELETE_COLUMN} = 0"
    row = db.session.execute(
        text(
            f"SELECT a.Name, al.Name, aa.Name, g.Name, c.{YEAR_COLUMN} "
            f"FROM {rb_writer.CONTENT_TABLE} c "
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
            f"LEFT JOIN {rb_writer.ALBUM_TABLE} al ON al.ID = c.{ALBUM_COLUMN} AND al.{active} "
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} aa ON aa.ID = al.{ALBUM_ARTIST} AND aa.{active} "
            f"LEFT JOIN {rb_writer.GENRE_TABLE} g ON g.ID = c.{GENRE_COLUMN} AND g.{active} "
            f"WHERE c.ID = :id"
        ),
        {"id": content_id},
    ).first()
    if row is None:
        return {}
    return {
        ARTIST_COLUMN: str(row[0] or ""),
        ALBUM_COLUMN: str(row[1] or ""),
        ALBUM_ARTIST: str(row[2] or ""),
        GENRE_COLUMN: str(row[3] or ""),
        YEAR_COLUMN: int(row[4]) if row[4] else None,
    }


def _resolved_now(resolver: _Resolver, word: Word) -> Word | None:
    """``word`` resolved again on the apply's handle, by the plan's own rule."""
    if word.table == rb_writer.ALBUM_TABLE:
        artist = (
            resolver.word(rb_writer.ARTIST_TABLE, word.album_artist.name)
            if word.album_artist is not None
            else None
        )
        return resolver.album(word.name, artist)
    return resolver.word(word.table, word.name)


def _rows_of(word: Word | None) -> tuple[str, str]:
    """The rows a word takes, its own and an album's artist, empty for a mint."""
    if word is None:
        return ("", "")
    artist = word.album_artist.row_id if word.album_artist is not None else ""
    return (word.row_id, artist)


def _assert_words_unmoved(db: Any, rows: Sequence[RowPlan]) -> None:
    """Refuse when a word resolves to another row now than the plan found (U163).

    The plan is what was approved and it is not rebuilt. A lookup row minted,
    retired or renamed since then changes which row a word links or whether
    it is minted, which the screen showed, so the answer is stale for it.
    """
    resolver = _Resolver(db)
    moved = []
    for row in rows:
        for word in (row.artist, row.album, row.genre):
            if word is None:
                continue
            now = _resolved_now(resolver, word)
            if _rows_of(now) != _rows_of(word):
                moved.append(
                    f"{row.target.name}: {word.table} {word.name!r} was "
                    f"{word.row_id or MINTED} and is {(now.row_id if now else '') or MINTED}"
                )
    if moved:
        raise refuse(
            "decision-stale",
            "a word a row would carry resolves to another lookup row than the plan "
            "found, so nothing was written; plan the landing again: " + "; ".join(moved),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


class _Mints:
    """The lookup rows one commit mints, each once per word, and the links to them (U163).

    BY HAND, NOT THROUGH THE BINDING'S ``add_artist`` AND KIN, which refuse a
    name any row holds, a tombstone included, and so would refuse exactly the
    word whose only namesake rekordbox retired. MINTED AND LINKED IN ONE
    COMMIT, because rekordbox garbage collects a lookup row nothing references
    (A4): a mint is pending on the landing's handle beside the row that links
    it, and a refusal rolls both back.
    """

    def __init__(self, db: Any) -> None:
        self._db = db
        self._made: dict[tuple[str, str, str], str] = {}

    def tables(self) -> tuple[str, ...]:
        """The lookup tables this commit minted a row in, to name in ``creations``."""
        return tuple(sorted({table for table, _name, _artist in self._made}))

    def link(self, content: Any, row: RowPlan) -> None:
        """Link the content row to each of its words' rows, minting a word's once, and write its year."""
        for column, word in (
            (ARTIST_COLUMN, row.artist),
            (ALBUM_COLUMN, row.album),
            (GENRE_COLUMN, row.genre),
        ):
            if word is not None:
                setattr(content, column, self.id_of(word))
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)

    def id_of(self, word: Word) -> str:
        """The row ``word`` links: the plan's active row, or the one this commit minted for it."""
        if word.row_id:
            return word.row_id
        key = word.key()
        if key not in self._made:
            self._made[key] = self._mint(word)
        return self._made[key]

    def _mint(self, word: Word) -> str:
        from uuid import uuid4

        kind = _lookup_class(word.table)
        # TEXT, AS THE STORED ROWS ARE (U153): the binding mints an int.
        columns: dict[str, Any] = {
            "ID": str(self._db.generate_unused_id(kind)),
            "Name": word.name,
            "UUID": str(uuid4()),
        }
        if word.table != rb_writer.GENRE_TABLE:
            columns["SearchStr"] = word.search
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST] = (
                self.id_of(word.album_artist) if word.album_artist is not None else None
            )
        made = kind.create(**columns)
        self._db.add(made)
        # FLUSHED AT ONCE, as the binding's own writers flush, so the next
        # mint's unused id is drawn against this one.
        self._db.flush()
        return str(made.ID)


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


def _taken_since_the_plan(db: Any, cfg: config.Config, rows: Sequence[RowPlan]) -> dict[str, str]:
    """Each planned target a row has taken since the plan was made, by target.

    The plan is what was approved and it is not rebuilt, so the one thing the
    apply asks the database again is the question whose answer can change
    under an approval: whether the file is in the collection now. A row that
    appeared is counted present rather than doubled. Asked before the first
    row is added, so nothing pending is flushed by the read, and asked of the
    candidate rows rather than the whole collection.
    """
    return content_ids_for(db, cfg, [row.target for row in rows])


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: NativePlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> NativeLanded:
    """Write the plan: the rows, the playlist under the root, the memberships.

    THE SESSION SPINE IS CALLED, NOT REBUILT, and it is the one the membership
    writers use: the three gates in their argued order with a record kept, a
    capture the commit happens behind, the analysis watch over the roots named,
    the commit witness, and the guarded commit. The one thing this commit says
    that no other does is ``creations``, which names the content table and
    admits the rows the whitelist would otherwise refuse (R-760).

    ALL OR NOTHING IN THE DATABASE. Every row and every membership is pending on
    one handle until one commit, and a refusal anywhere before it rolls the
    handle back, so a failure on the second of three files leaves the table as
    it was. The files are in the library by then, which the caller reports.

    ``analysis_roots`` has no default for the reason the membership writer
    gives: a watch that watches nothing reports every session clean.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    registry = tree_registry.read(cfg)
    root_id = anchored_intake_root(db, plan.tree_id, registry)
    if root_id != plan.root_id:
        raise refuse(
            "decision-stale",
            f"the intake tree {plan.tree_id!r} is anchored to root {root_id!r} and the "
            f"plan was made against {plan.root_id!r}, so nothing was written",
            origin=_ORIGIN,
            detail={"planned": plan.root_id, "anchored": root_id},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    added_ids: list[tuple[RowPlan, str]] = []
    present: list[RowPlan] = list(plan.present())
    memberships = 0
    vox_written = 0
    analyze_id = ""
    analyze_added = 0
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)

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
        written: list[WrittenPlaylist] = []
        left: list[tuple[str, Left]] = [
            *plan.unplanned_left,
            *((one.name, row) for one in plan.playlists for row in one.left),
        ]
        placed: placement.Placed | None = None
        set_written: set_playlist.Written | None = None
        labels_written: label_filing.Written | None = None
        try:
            # BEFORE THE FIRST ROW, so a refusal adds nothing. A name the plan
            # chose free that INBOX holds now would show two playlists of one
            # name, and an account playlist is created rather than found.
            assert_names_still_free(db, plan)
            to_add = plan.to_add()
            taken = _taken_since_the_plan(db, cfg, to_add)
            # THE WORDS ARE ASKED AGAIN BEFORE THE FIRST ROW (U163), as the
            # targets are, so a lookup row made or retired since the approval
            # refuses rather than linking what nobody approved.
            _assert_words_unmoved(db, [row for row in to_add if str(row.target) not in taken])
            mints = _Mints(db)
            for row in to_add:
                held = taken.get(str(row.target))
                if held is not None:
                    present.append(replace(row, action=PRESENT, content_id=held))
                    continue
                content = db.add_content(row.target, Title=row.title)
                _restamp(content, row, plan)
                mints.link(content, row)
                added_ids.append((row, str(content.ID)))
            # THE VOX MY TAG, IN THE SAME COMMIT (U127), on the rows this
            # landing made and only those the plan tagged. Additive: the writer
            # adds an association it does not find and removes none.
            vox_written = _tag_vox(db, added_ids)
            # In listing order: the files the plan named, in the order it named
            # them, whether the row is new or was already there.
            by_target = {str(row.target): content_id for row, content_id in added_ids}
            by_target.update({str(row.target): row.content_id for row in present if row.content_id})
            claimed = {str(target) for one in plan.playlists for target in one.targets}
            # IN THE ACCOUNT PLAYLIST'S ORDER (U128), a new row by its target and
            # an owned row by the id the plan found for it. A member whose file
            # made no row is left, and named, rather than silently absent.
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
            # IN SET ORDER WHEN THIS IS A SET LANDING (U135): the brief asks
            # for both landings' rows in set order on the joined INBOX playlist.
            # Landing files alone sort by name; the set's members carry positions.
            if plan.set_playlist is not None:
                ordered = []
                seen: set[str] = set()
                for member in plan.set_playlist.members:
                    target = str(member.target) if member.target else ""
                    if not target or target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
                for row in plan.rows:
                    target = str(row.target)
                    if target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
            else:
                ordered = [
                    by_target[str(row.target)]
                    for row in plan.rows
                    if str(row.target) in by_target and str(row.target) not in claimed
                ]
            # THE BATCH PLAYLIST HOLDS WHAT NO ACCOUNT PLAYLIST CLAIMED, and is
            # not written when that is nothing, as the intake file does it.
            # A SET LANDING ADDS TO THE RECORDED INBOX PLAYLIST (U135) when an
            # earlier landing of the same job left one live under the root.
            if ordered or not accounts:
                playlist = _batch_playlist_row(db, plan, anchor)
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
            # EVERY ROW THIS LANDING MADE JOINS ANALYZE (U166), in the same
            # commit and in the plan's order, so the visit selects one playlist.
            # A row already held is not added: rekordbox has had it.
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
                analyze_id = str(analyze.ID)
                analyze_added = len(
                    rb_writer.add_memberships(
                        db, analyze, [content_id for _row, content_id in added_ids]
                    )
                )
            # THE HEARTS, IN THE SAME COMMIT (U120): into All Favorites and
            # each one's month, a row already present as much as a row
            # added, so a heart landed twice is one membership. And the
            # pass's owned hearts All Favorites lacked (U146), by their rows.
            if plan.favorites is not None and (plan.favorites.items or plan.favorites.owned):
                pairs: list[tuple[str, str | None]] = [
                    (by_target[str(item.target)], item.month)
                    for item in plan.favorites.items
                    if str(item.target) in by_target
                ]
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
                # AND PINK ON EACH (U153): every row this landing made for a
                # heart, which carries no colour by construction, and the
                # owned hearts the plan read as uncoloured.
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
            # THE SET'S PERMANENT PLAYLIST, IN THE SAME COMMIT (U121): the rows
            # this landing made are keyed by target, and a member the landing
            # could not make a row for is left and listed, never guessed.
            if plan.set_playlist is not None:
                set_written = set_playlist.write_members(db, plan.set_playlist, by_target=by_target)
            # THE LABEL FILING, IN THE SAME COMMIT (U156): appended under the
            # Record Labels tree by target, a member whose file made no row
            # left and named, nothing found there removed.
            if plan.labels is not None:
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
            # THE LOOKUP TABLES ONLY WHEN A WORD WAS MINTED (U163), so a
            # landing that links every word admits what it did before.
            rb_writer.commit_guarded(
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
            )
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_landing_commit(
                    record,
                    plan,
                    len(added_ids),
                    memberships + analyze_added,
                    cfg,
                    playlist_id=playlist_id,
                    written=written,
                    placed=placed,
                    set_written=set_written,
                    vox_written=vox_written,
                    labels_written=labels_written,
                )
            raise

        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
            cfg,
            playlist_id=playlist_id,
            written=written,
            placed=placed,
            set_written=set_written,
            vox_written=vox_written,
            labels_written=labels_written,
        )
        convergence.record_fingerprint(cfg, db)
        if set_written is not None and set_written.playlist_id:
            set_written = replace(
                set_written, read_back=set_playlist.read_back(db, set_written.playlist_id)
            )
        if labels_written is not None:
            labels_written = label_filing.read_back(db, labels_written)

        landed = []
        # ONLY WHEN A TAG WAS PLANNED: a row this landing just made carries no
        # tag it did not write, so there is nothing else to read back.
        voxed, vox_unread = (
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
        )
        for row, content_id in added_ids:
            values, title, folder_path, file_id, link = _read_back(db, content_id)
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
                    words=_words_back(db, content_id),
                    planned=row.words(),
                )
            )
        session_id = record.session_id

    unscored = {row.target for row in plan.vox_unscored()}
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
        vox_unscored=tuple(
            row.target for row, _content_id in added_ids if row.target in unscored
        ),
        vox_blocked=plan.vox_blocked if added_ids else "",
        vox_missing=tuple(
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
        ),
        vox_unread=vox_unread,
        analyze_id=analyze_id,
        analyze_name=f"{plan.root_name} / {ANALYZE}" if analyze_id else "",
        analyze_added=analyze_added,
    )


def _tag_vox(db: Any, added: Sequence[tuple[RowPlan, str]]) -> int:
    """Give each added row the plan tagged the vox My Tag. Answers how many were written.

    THE VOCALS VERB'S OWN WRITER (U127), so the category and the value are
    found or made exactly as ``metadata mytags-vocals`` makes them, and an
    association already there is left as it is. Pending on the landing's
    handle, committed or rolled back with its rows.
    """
    content_ids = [content_id for row, content_id in added if row.vox]
    if not content_ids:
        return 0
    value = rb_writer.ensure_my_tag_value(db, metadata_cli.CATEGORY, metadata_cli.VALUE_VOX)
    return sum(1 for content_id in content_ids if rb_writer.add_my_tag(db, value, content_id))


def _vox_read_back(db: Any) -> tuple[frozenset[str], str]:
    """Every row carrying the vox My Tag as adoption reads it, after the commit (U127).

    ADOPTION'S OWN READER, :func:`cratekit.adopt.placements.vox_tagged`, and
    not a second reading of the table, because what the landing promises is
    that the next ``adopt apply`` files the row, and a tag the writer put under
    a category rekordbox removed is one that reader does not answer. A
    refusal it raises, a marker no row can state, is the answer's reason and
    not the landing's failure: the commit has landed by now. Answers the rows
    and the reason, empty when it read.
    """
    try:
        tagged = adopt_placements.vox_tagged(db)
    except CratekitError as exc:
        return frozenset(), exc.cause.message
    return tagged or frozenset(), ""


def _batch_playlist_row(db: Any, plan: NativePlan, anchor: Any) -> Any:
    """The INBOX playlist the batch members go in: the recorded one, else found or made.

    THE RECORDED PLAYLIST, when a set landing names one (U135), was checked
    live at the plan and is checked again here. Otherwise a live playlist of
    the name under the intake root is taken, and a new one made when none is
    live. A removed playlist is not found: rekordbox soft deletes a playlist a
    person removes, and :func:`rb_writer.ensure_playlist` matches name and
    parent alone, so a playlist deleted in rekordbox and written into would
    hold memberships nobody can see. The INSPIRATION path guards the same way.
    """
    if plan.batch_playlist_id:
        row = db.get_playlist(ID=plan.batch_playlist_id)
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the INBOX playlist {plan.playlist!r} (row {plan.batch_playlist_id}) "
                f"the plan adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.batch_playlist_id, "name": plan.playlist},
            )
        return row
    parent_id = str(anchor.ID)
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)


def _analyze_row(db: Any, plan: NativePlan, anchor: Any) -> Any:
    """The :data:`ANALYZE` playlist the added rows join: found live under the root, else made.

    FOUND AGAIN AT THE WRITE rather than taken from the plan, so a playlist
    made by another landing since this plan was read is joined and never made
    a second time. The plan's identifier is what the screen said; a playlist
    removed since is not written into, and a new one is made in its place.
    """
    del plan
    found = analyze_playlist(db, str(anchor.ID))
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)


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


def _record_landing_commit(
    record: session.SessionRecord,
    plan: NativePlan,
    rows: int,
    memberships: int,
    cfg: config.Config,
    *,
    playlist_id: str,
    written: Sequence[WrittenPlaylist] = (),
    placed: placement.Placed | None = None,
    set_written: set_playlist.Written | None = None,
    vox_written: int = 0,
    labels_written: label_filing.Written | None = None,
) -> None:
    """Record the commit on the session, once anything landed.

    TWO COUNTS UNDER TWO NAMES. The intake tree's entry is the memberships, the
    number ``restore list`` asks for and the one ``tree cutover`` reads to
    refuse a revert after a native write. The content table's entry is the rows,
    kept apart because a restore that discards them discards tracks, not
    memberships, and a person weighing that should see the difference.
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
    # THE BATCH PLAYLIST IS NAMED ON THE RECORD (U111), by identifier as well
    # as by name, so ``inbox rotate`` ages a batch from the day it landed
    # rather than from whatever the playlist row says. Written with the commit,
    # by the call that persists it.
    if playlist_id:
        kept = {"id": playlist_id, "name": plan.playlist}
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id
        record.detail[BATCH_PLAYLIST_KEY] = kept
    # AND THE BATCH AND ITS FILED FOLDER (U164), so the next landing of the
    # same name goes back to the folder and the name stays taken.
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY] = {"batch": plan.batch, "folder": str(plan.folder)}
    # AND THE PASS (R-777), which is what ``sync mark --pass`` reads as the
    # proof this pass landed. Only with the commit, never for a plan.
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
    # AND EACH ACCOUNT PLAYLIST (U113), whose name carries no date to age it by.
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
    # AND EACH LABEL ROW'S PROVIDER TRACK (U150), what its manifest row names,
    # so the account mirror fills this batch's INBOX playlist from its own
    # tracks. Persisted by whichever commit below records anything.
    if labels_written is not None and labels_written.provider:
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
    # AND THE HEARTS PLACED (U120), under their own key, since the Favorites
    # folder is nobody's registered tree and a restore weighing the intake
    # tree's memberships should see these apart from them.
    if placed is not None and (hearts > 0 or coloured > 0):
        record.detail[placement.PLACED_KEY] = placed.to_json()
    changes = []
    if memberships > 0:
        changes.append(session.TreeChange(tree=plan.tree_id, created=memberships))
    if rows > 0:
        changes.append(session.TreeChange(tree=rb_writer.CONTENT_TABLE, created=rows))
    # ONLY A TREE THAT CHANGED IS RECORDED COMMITTED. A landing whose every
    # file was present and in the batch already, with only the set's playlist
    # or the hearts written, leaves the intake tree as it was, and a record
    # saying the tree committed with no change would tell a restore and a
    # revert otherwise.
    if changes:
        session.record_commit(record, plan.tree_id, session.ChangeSummary(tuple(changes)), cfg)
    # AND THE HEARTS PLACED (U120), under the favourites key, so the record
    # counts the batch's memberships and the hearts' apart, as the backfill
    # records its own.
    if hearts > 0 or coloured > 0:
        session.record_commit(
            record,
            placement.RECORD_KEY,
            session.ChangeSummary(
                (
                    session.TreeChange(
                        tree=placement.RECORD_KEY, created=hearts, updated=coloured
                    ),
                )
            ),
            cfg,
        )
    # AND THE SET'S PLAYLIST (U121), under the declared folder's own id, so
    # the record counts the batch's memberships and the set's apart.
    if set_written is not None and plan.set_playlist is not None:
        set_playlist.record_commit(record, set_written, plan.set_playlist, cfg)
    # AND THE LABEL FILING (U156), under the catalogue tree's own id, so the
    # record counts the batch's memberships and the labels' apart.
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
    # AND THE VOX TAGS (U127), under the vocals verb's own key, so a restore
    # counts the tag associations apart from the rows they hang on.
    if vox_written > 0:
        session.record_commit(
            record,
            metadata_cli.CHANGE_KEY,
            session.ChangeSummary(
                (session.TreeChange(tree=metadata_cli.CHANGE_KEY, created=vox_written),)
            ),
            cfg,
        )


def landings_of_pass(cfg: config.Config, name: str) -> tuple[str, ...]:
    """The session ids of every closed native landing that committed ``name``.

    THE PROOF ``sync mark --pass`` WAITS FOR (R-777), the native counterpart of
    an intake file: a record of this workflow, closed, whose intake source
    committed and whose detail names the pass. A landing refused after its
    moves leaves its files in the library and adds no row, and its record
    names no pass, so its files cannot mark a playlist by being on disk.
    """
    records, _unreadable = session.scan_log(cfg)
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


__all__ = [
    "ADD",
    "BATCH_PLAYLIST_KEY",
    "FILED_BATCH_KEY",
    "FILE_ID_AT_LANDING",
    "ANALYZE",
    "INBOX_JOB_KEY",
    "INBOX_PLAYLISTS_KEY",
    "LEFT_EMPTY",
    "PRESENT",
    "UNSUPPORTED",
    "WORKFLOW",
    "AddedRow",
    "ALBUM_ARTIST",
    "ALBUM_COLUMN",
    "ARTIST_COLUMN",
    "GENRE_COLUMN",
    "MINTED",
    "SEARCH_EMPTY",
    "SEARCH_NAME",
    "YEAR_COLUMN",
    "Word",
    "FavoritesPlan",
    "HeartItem",
    "NativeLanded",
    "NativePlan",
    "OwnedHeartItem",
    "PlaylistPlan",
    "RowPlan",
    "WrittenPlaylist",
    "anchored_intake_root",
    "apply_rows",
    "assert_names_still_free",
    "assert_rows_gridless",
    "assert_rows_identified",
    "choose_device",
    "content_ids_for",
    "file_id_of",
    "file_type_of",
    "identity",
    "inbox_held",
    "inbox_nodes",
    "live_inbox_named",
    "leftover_set_inbox",
    "plan_rows",
    "recorded_inbox_playlist",
    "search_convention",
    "single_rows_for",
    "stored_folder_path",
    "with_filing",
    "year_of",
]
