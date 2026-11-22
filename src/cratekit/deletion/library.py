"""Reading the library for deletion. One walk, and not one row is written (KTD15).

A removed row is found three ways: rekordbox's own soft delete marker, which
keeps the writer's delete prohibition closed; the session record that names a
row ``crate sync removed`` deleted outright, :func:`recorded_removals` (U288),
since rekordbox 7.2 deletes on Remove from Collection and leaves no marker (A178,
A185); and a native landing's record of the rows it made,
:func:`landed_absences` (R-1037), for a landing the database shows was not
rolled back (R-1844). A row no Cratekit record names is invisible here. Rows are
read into frozen values, so every later stage works on data, not live objects.

**ONE WALK, PARTITIONED.** A second walk of a database CURSOR returns nothing,
which reports an empty library while the run reports clean; it has shipped once.

**THE MARKER AND THE SEQUENCE ARE BOTH READ, AND NEITHER IS DEFAULTED.** The
marker is :func:`cratekit.write.trees.soft_delete_marker`, shared with routing.
The sequence refuses: guessing low re-offers every removal on every run,
guessing high hides one forever.

Layer note: MODULES. It reads the database through the guarded binding and names
no verb.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping

from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.tombstone import reads_as_version
from cratekit.write import trees

#: What a version bearing column is GUARANTEED to hold, which decides whether its
#: value is believed and how it is SPELLED into a title.
VERSION_IS_AN_ARTIST = "artist"
VERSION_IS_A_DESIGNATION = "designation"


@dataclass(frozen=True, slots=True)
class RemovedRow:
    """One row the user removed from the collection, with everything deletion needs.

    ``size`` None means the row recorded none, which can never satisfy R37's size
    match; it is kept apart from zero, an empty file.
    """

    content_id: str
    recorded: str
    sequence: int
    size: int | None
    artist: str
    title: str
    isrc: str | None = None
    #: The mix name when rekordbox filed it in a column of its own; without it
    #: two versions sharing a bare ``Title`` share one tombstone. Kept beside the
    #: title, and ``stores.version_of`` composes the identity.
    version: str = ""
    #: What the column holding :attr:`version` MEANS, which decides how it is
    #: spelled; defaults to the designation, the reading that changes nothing.
    version_kind: str = VERSION_IS_A_DESIGNATION
    #: A non empty version column value NOT believed, kept for the audit of a
    #: tombstone that missed.
    version_unbelieved: str = ""


@dataclass(frozen=True, slots=True)
class CollectionRead:
    """The whole collection, read once, in the two shapes the pass needs.

    ``active`` is the FULL active half, because it is the evidence for the
    unreferenced proof and a subset proves a different claim (R37).
    """

    active: tuple[trees.ContentRow, ...]
    removed: tuple[RemovedRow, ...]
    #: Every row's UUID the walk read, live or marked, by content id, empty where
    #: the row holds none: what a landing's record is checked against (R-1844).
    uuids: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))


def _unreadable(
    reason: str, message: str, detail: dict[str, Any], remedy: Remedy = Remedy.RUN_DOCTOR
) -> CratekitError:
    """A run scoped refusal of this module's evidence."""
    return refuse(reason, message, remedy=remedy, origin=("deletion.library",), detail=detail)


def database_identity(db: Any) -> str:
    """The identity the watermark is bound to, ``DjmdProperty.DBID``.

    A rebuilt library is a different one and a moved library the same one. An
    unreadable identity REFUSES: an unbound watermark lets a rebuild report
    nothing to do forever.
    """
    try:
        held = db.get_property()
        row = held.first() if hasattr(held, "first") else held
        identity = getattr(row, "DBID", None) if row is not None else None
    except Exception as exc:  # noqa: BLE001 - any read failure is one refusal
        raise _unreadable(
            "canary-read-failed",
            f"the rekordbox database could not report its own identity ({exc}), so the deletion "
            "watermark cannot be bound to it and a rebuilt library would silently inherit a "
            "position measured in a sequence space that no longer exists",
            {"column": "DBID"},
        ) from exc
    if not identity:
        raise _unreadable(
            "canary-read-failed",
            "the rekordbox database reports no identity of its own, so the "
            "deletion watermark has nothing to be bound to",
            {"column": "DBID"},
        )
    return str(identity)


def current_sequence(db: Any) -> int:
    """The library's own update counter, where a first run baselines to (R35).

    The counter rather than the highest removed row: a library whose only
    removals are old would otherwise baseline low and read every later change as
    a removal. The caller takes the greater of the two anyway.
    """
    try:
        return int(db.get_local_usn() or 0)
    except Exception as exc:  # noqa: BLE001 - any read failure is one refusal
        raise _unreadable(
            "canary-read-failed",
            f"the rekordbox database could not report its update counter "
            f"({exc}), so a first run has no position to baseline at",
            {"column": "localUpdateCount"},
        ) from exc


def _sequence_of(row: Any) -> int:
    """The update sequence a removed row was stamped with, ``rb_local_usn``, or REFUSE.

    The counter rather than ``updated_at``: it is monotonic by construction, not
    by the clock being right.
    """
    value = getattr(row, "rb_local_usn", None)
    detail = {"content_id": str(getattr(row, "ID", "")), "column": "rb_local_usn"}
    if value is None or isinstance(value, bool):
        raise _unreadable(
            "removal-sequence-unreadable",
            f"the removed collection row {getattr(row, 'ID', '?')!r} cannot say which update it "
            "was removed by, so this run cannot tell whether it is a removal somebody has already "
            "answered for; there is no safe default, because guessing low re-offers every removal "
            "in the library and guessing high hides this one forever",
            detail,
        )
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise _unreadable(
            "removal-sequence-unreadable",
            f"the removed collection row {getattr(row, 'ID', '?')!r} reports {value!r} as its "
            "update sequence, which is not a number this run can compare a watermark against",
            detail,
        ) from exc


def _text(row: Any, attribute: str) -> str:
    """One text column, missing and empty folded together.

    Unlike the marker: an empty field of an identity is ordinary, and the
    identity refuses only when EVERY field is empty.
    """
    return str(getattr(row, attribute, "") or "")


def _identifier(row: Any, attribute: str) -> str:
    """One IDENTIFIER column, a missing one folded to empty rather than to ``'None'``.

    ``'None'`` is a truthy string that would address review items, declines and
    playlist membership. Empty is refused where it belongs: ``stores.identifiable``
    reports the row UNIDENTIFIABLE, so one bad row does not stop the pass.
    """
    value = getattr(row, attribute, None)
    return "" if value is None else str(value)


#: The columns that can hold a mix name, in the order they are believed. FIRST
#: BELIEVED VALUE WINS, since joining two would spell one mix twice.
#:
#: ``RemixerName`` is an association proxy into ``djmdArtist``: always an ARTIST
#: name, believed on sight and spelled through ``tombstone.remixer_title``.
#: ``Subtitle`` is free text (ID3 ``TIT3``) that holds labels and notes as often as
#: mix names, so it is believed only when it reads as a version
#: (``tombstone.VERSION_WORDS``).
_VERSION_COLUMNS: tuple[tuple[str, str], ...] = (
    ("RemixerName", VERSION_IS_AN_ARTIST),
    ("Subtitle", VERSION_IS_A_DESIGNATION),
)


def _version_of(row: Any) -> tuple[str, str, str]:
    """The mix name, what its column means, and what was NOT believed.

    A missing column answers "" (an absent mix name leaves the identity as wide
    as before). A column not believed is skipped, so the order keeps meaning
    what it says, and its value is carried out for the tombstone's audit.
    """
    unbelieved = ""
    for column, holds in _VERSION_COLUMNS:
        found = _text(row, column)
        if not found:
            continue
        if holds == VERSION_IS_A_DESIGNATION and not reads_as_version(found):
            unbelieved = unbelieved or found
            continue
        return found, holds, unbelieved
    return "", "", unbelieved


def _size_of(row: Any) -> int | None:
    try:
        size = int(getattr(row, "FileSize", None))
    except (TypeError, ValueError):
        return None
    return size if size > 0 else None


def _removed_row(row: Any, sequence: int) -> RemovedRow:
    """A removed row read through the same readers, marked or recorded."""
    version, kind, unbelieved = _version_of(row)
    return RemovedRow(
        content_id=_identifier(row, "ID"),
        recorded=_text(row, "FolderPath"),
        sequence=sequence,
        size=_size_of(row),
        artist=_text(row, "ArtistName"),
        title=_text(row, "Title"),
        isrc=_text(row, "ISRC") or None,
        version=version,
        version_kind=kind or VERSION_IS_A_DESIGNATION,
        version_unbelieved=unbelieved,
    )


def read_collection(rows: Iterable[Any]) -> CollectionRead:
    """Split one walk of the collection into the active rows and every removal.

    Unfiltered: the baseline needs the highest sequence and the filter, in
    ``run.plan``, needs the baseline. Takes mapped rows rather than a handle, so
    every branch is reachable without a database.
    """
    active: list[trees.ContentRow] = []
    removed: list[RemovedRow] = []
    uuids: dict[str, str] = {}
    for row in rows:
        uuids[_identifier(row, "ID")] = _text(row, "UUID")
        if not trees.soft_delete_marker(row):
            active.append(
                trees.ContentRow(
                    content_id=_identifier(row, "ID"),
                    recorded=_text(row, "FolderPath"),
                    deleted=False,
                )
            )
            continue
        removed.append(_removed_row(row, _sequence_of(row)))
    return CollectionRead(
        active=tuple(active), removed=tuple(removed), uuids=MappingProxyType(uuids)
    )


def _declared_membership_count(memberships: Any) -> int | None:
    """How many membership rows the DATABASE says it holds, or None if it cannot say.

    ``len`` for a sequence, ``count()`` for the binding's query; a spent cursor
    answers neither, which is the shape this catches.
    """
    try:
        return len(memberships)
    except TypeError:
        pass
    counter = getattr(memberships, "count", None)
    if counter is None:
        return None
    try:
        return int(counter())
    except Exception:  # noqa: BLE001 - any failure to count is "it cannot say"
        return None


def playlist_referenced(memberships: Any) -> frozenset[str]:
    """Every content row a live playlist entry still points at, PROVED COMPLETE.

    R37 keeps a file a playlist still references. For a removed row a playlist
    entry is the only surviving reference, and ``candidates.assert_complete``
    covers active rows only, so a walk that answers nothing would read as "no
    playlist references anything" and trash the file.

    So the walk must reach exactly the number the database declares: a short
    walk, an over long one, a database that cannot say, a walk that fails part
    way (a refusal, not a traceback, S4) and a live membership naming no row all
    refuse. An honest zero is accepted.
    """
    declared = _declared_membership_count(memberships)
    walked = 0
    referenced: set[str] = set()
    try:
        for row in memberships:
            walked += 1
            if not trees.soft_delete_marker(row):
                referenced.add(_identifier(row, "ContentID"))
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - any failure to walk is one refusal
        raise _unreadable(
            "deletion-evidence-incomplete",
            f"the walk of this library's playlist memberships failed after {walked} of them "
            f"({exc}), so the set of files a playlist still points at is whatever happened to "
            "arrive before the failure; every file missing from it would be proved unreferenced "
            "against a question that was never fully asked",
            {"walked": walked},
        ) from exc
    if "" in referenced:
        # A reference this pass cannot address would read as no reference.
        raise _unreadable(
            "deletion-evidence-incomplete",
            "a live playlist membership in this library names no collection row, so what it "
            "points at cannot be worked out; a reference this pass cannot address would read as "
            "no reference at all, and the file it protects would be offered for deletion",
            {"walked": walked},
        )
    if declared is None:
        raise _unreadable(
            "deletion-evidence-incomplete",
            "the rekordbox database cannot say how many playlist memberships it holds, so the "
            f"walk that just returned {walked} of them cannot be shown to have seen all of them; a "
            "membership this pass did not see is a playlist reference nothing reports, and the "
            "file it protects would be offered for deletion",
            {"walked": walked},
            Remedy.REPORT_DEFECT,
        )
    if walked != declared:
        raise _unreadable(
            "deletion-evidence-incomplete",
            f"the rekordbox database holds {declared} playlist memberships and this walk saw "
            f"{walked} of them, so the set of files a playlist still points at cannot be shown to "
            "be the whole set; every file missing from it would be proved unreferenced against a "
            "question that was never fully asked",
            {"declared": declared, "walked": walked},
        )
    return frozenset(referenced)


# A removal recorded rather than marked (U288, R-1037)

#: The key a session record names its removed rows under, and the columns each
#: keeps (the guarded writer's). Spelled here rather than imported, so this
#: package reaches no more of the core (U296); ``tests/test_sync_removed.py``
#: holds the two spellings equal.
RECORDED_REMOVALS_KEY = "collection_removed"
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


class _Recorded:
    """A recorded row's columns as attributes, so the readers above read it as a row."""

    def __init__(self, columns: Mapping[str, Any]) -> None:
        for name in RECORDED_COLUMNS:
            setattr(self, name, columns.get(name))


#: The key a native landing (``intake.native``) names the rows it made under,
#: held equal by ``tests/test_delete_landed_removed.py``. Its rows keep
#: :data:`RECORDED_COLUMNS` and the row's UUID under :data:`LANDED_UUID_KEY`.
LANDED_ROWS_KEY = "collection_landed"
LANDED_UUID_KEY = "uuid"


@dataclass(frozen=True, slots=True)
class LandedAbsence:
    """One row a landing made that the database no longer holds, before it is numbered.

    ``landed`` is the update count the landing's commit left; of two landings
    naming one row, the later one's is kept.
    """

    columns: Mapping[str, Any]
    landed: int

    def row(self, sequence: int) -> RemovedRow:
        """The removal, at the sequence its first sighting was given."""
        return _removed_row(_Recorded(self.columns), sequence)


@dataclass(frozen=True, slots=True)
class LandedRead:
    """What the landings' records offer, and the landings read as rolled back.

    ``rolled_back`` holds the absent rows' content ids of each landing of this
    database nothing shows was not rolled back, so the gate can count them
    (R-1844): a refusal nobody sees hid R-1844 itself.
    """

    absent: Mapping[str, LandedAbsence]
    rolled_back: tuple[frozenset[str], ...] = ()

    def unasked(self, numbered: Iterable[str]) -> int:
        """How many rolled back landings hold an absent row no earlier run numbered.

        A numbered row was asked about while its landing stood; counting those
        would grow the screen's number with every tidy up.
        """
        asked = {str(one) for one in numbered}
        return sum(1 for rows in self.rolled_back if rows - asked)


def _landing_stands(
    playlists: Any,
    rows: list[tuple[str, Mapping[str, Any], str]],
    *,
    uuids: Mapping[str, str],
    playlist_held: Callable[[str], bool],
) -> bool:
    """Whether the database holds a fact no database from before the landing holds.

    Either proof: a landed row held live or marked under the UUID the landing
    recorded (an id alone can be drawn again by a later import), or every
    playlist the landing made, in any state (R-1037).
    """
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
        # ``uuid and``: a row recorded with no UUID matches no row holding none.
        return True
    if not isinstance(playlists, (list, tuple)) or not playlists:
        return False
    return all(playlist_held(str(one)) for one in playlists)


def _records(
    details: Iterable[Mapping[str, Any]], key: str, database_identity: str
) -> Iterable[tuple[Mapping[str, Any], int]]:
    """Each record under ``key`` of THIS database that names a whole update count.

    A record of another database, or one that cannot say its sequence, offers
    nothing: skipped, never guessed at.
    """
    for detail in details:
        recorded = detail.get(key) if isinstance(detail, Mapping) else None
        if not isinstance(recorded, Mapping):
            continue
        if str(recorded.get("database_identity") or "") != str(database_identity):
            continue
        sequence = recorded.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool):
            continue
        yield recorded, sequence


def _columns_of(recorded: Mapping[str, Any]) -> Iterable[tuple[Mapping[str, Any], Any]]:
    """Each row entry of a record that carries a mapping of columns."""
    for entry in recorded.get("rows") or ():
        columns = entry.get("columns") if isinstance(entry, Mapping) else None
        if isinstance(columns, Mapping):
            yield columns, entry


def landed_absences(
    details: Iterable[Mapping[str, Any]],
    *,
    database_identity: str,
    present: Iterable[str],
    uuids: Mapping[str, str],
    playlist_held: Callable[[str], bool],
) -> LandedRead:
    """Every row a native landing made in THIS database that it holds no longer, by content id.

    ``present`` is every content id held, live or marked, plus every one a
    recorded removal answers for, so one row is one removal; ``uuids`` is every
    held row's UUID. One row named by two landings keeps the later one.

    A LANDING ROLLED BACK IS NO REMOVAL: ``restore run``, a bare metal recovery
    or a hand copy puts back a database from before it. So a record offers its
    absent rows only while :func:`_landing_stands`. Remove from Collection
    leaves the landing's other rows and its playlists (A178, A185); deleting a
    playlist in rekordbox deletes its row (A200). A landing that does not stand
    offers nothing and is listed in ``rolled_back``: keeping a file costs
    nothing.
    """
    held = {str(one) for one in present}
    found: dict[str, LandedAbsence] = {}
    rolled_back: list[frozenset[str]] = []
    for landed, sequence in _records(details, LANDED_ROWS_KEY, database_identity):
        rows: list[tuple[str, Mapping[str, Any], str]] = []
        for columns, entry in _columns_of(landed):
            content_id = _identifier(_Recorded(columns), "ID")
            if not content_id:
                continue
            uuid = entry.get(LANDED_UUID_KEY)
            rows.append((content_id, columns, uuid if isinstance(uuid, str) else ""))
        absent = [
            (content_id, columns) for content_id, columns, _uuid in rows if content_id not in held
        ]
        if not absent:
            continue
        if not _landing_stands(
            landed.get("playlists"), rows, uuids=uuids, playlist_held=playlist_held
        ):
            rolled_back.append(frozenset(content_id for content_id, _columns in absent))
            continue
        for content_id, columns in absent:
            seen = found.get(content_id)
            if seen is None or seen.landed < sequence:
                found[content_id] = LandedAbsence(columns=dict(columns), landed=sequence)
    return LandedRead(
        absent={key: found[key] for key in sorted(found)}, rolled_back=tuple(rolled_back)
    )


def playlist_ids(playlists: Iterable[Any]) -> frozenset[str]:
    """Every playlist row's id, live or marked: what a landing's record is checked against."""
    return frozenset(str(getattr(row, "ID", "")) for row in playlists if getattr(row, "ID", None))


def recorded_removals(
    details: Iterable[Mapping[str, Any]], *, database_identity: str, present: Iterable[str]
) -> tuple[RemovedRow, ...]:
    """Every row a recorded removal took out of THIS database that it still does not hold.

    A row held again, live or marked, is no removal (a restore brought it back).
    Each row is read through the marked row's readers at the update count the
    record names, so the watermark orders it with every other removal. One
    content id recorded twice keeps its later sequence.
    """
    held = {str(one) for one in present}
    found: dict[str, RemovedRow] = {}
    for recorded, sequence in _records(details, RECORDED_REMOVALS_KEY, database_identity):
        for columns, _entry in _columns_of(recorded):
            row = _removed_row(_Recorded(columns), sequence)
            if not row.content_id or row.content_id in held:
                continue
            seen = found.get(row.content_id)
            if seen is None or seen.sequence < row.sequence:
                found[row.content_id] = row
    return tuple(found[key] for key in sorted(found))
