"""Reading the library for deletion. One walk, and not one row is written (KTD15).

Deletion is driven by rekordbox's own soft-delete marker, which is the decision
that keeps the writer's unconditional delete prohibition closed: a removed row
persists with its path intact, so removals are identified exactly without this
unit ever creating, editing, or deleting a database row. Nothing in this module
writes. Nothing in this module can write: it reads mapped rows into frozen values
and hands those on, so every later stage in the pass operates on data rather than
on live objects that could be mutated by accident.

**ONE WALK, PARTITIONED.** The collection is read exactly once and split into the
active rows and the removed ones. Two walks would be twice the work on a library
of ten thousand rows, and the second walk of a database CURSOR returns nothing at
all, which is the shape that reports an empty library while the run reports clean.
That defect has already shipped in this repository once.

**THE MARKER AND THE SEQUENCE ARE BOTH READ, AND NEITHER IS DEFAULTED.** The
marker read is :func:`cratekit.write.trees.soft_delete_marker`, shared with the
routing pass so one rule has one implementation. The sequence has no shared
reader because only this unit needs it, and it refuses for the same reason: there
is no safe default. Guessing low re-offers every removal in the library on every
run; guessing high marks the row handled and nobody is ever asked about it.

Layer note: MODULES. It reads the database through the guarded binding and names
no verb.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees


@dataclass(frozen=True, slots=True)
class RemovedRow:
    """One row the user removed from the collection, with everything deletion needs.

    ``size`` is optional and its absence is meaningful: R37 requires the file's
    size to match the size the removed row RECORDED, so a row that recorded none
    can never satisfy that assertion and is never deletable. Modelling it as None
    rather than as zero keeps "the row said nothing" and "the row said the file
    is empty" apart, which are different facts with the same consequence today
    and could stop being so.
    """

    content_id: str
    recorded: str
    sequence: int
    size: int | None
    artist: str
    title: str
    isrc: str | None = None
    #: The mix name, when rekordbox filed it in a column of its own rather than
    #: inside the title. READ BECAUSE THE IDENTITY IS OTHERWISE NOT UNIQUE: a
    #: remix-heavy library holds two versions of one recording whose ``Title`` is
    #: the same bare string, and a tombstone keyed on artist and title alone
    #: suppresses both of them from one deletion. Kept beside the title rather
    #: than folded into it here, so the payload a person reads still shows what
    #: the row actually says while ``stores.version_of`` composes the identity.
    version: str = ""


@dataclass(frozen=True, slots=True)
class CollectionRead:
    """The whole collection, read once, in the two shapes the pass needs.

    ``active`` is the full active half rather than the part that looks relevant,
    because it is the evidence for the unreferenced proof: a proof built from a
    subset is a proof that a file is unreferenced BY THE ROWS SOMEBODY CHOSE TO
    LOOK AT, which is not the claim R37 makes.
    """

    active: tuple[trees.ContentRow, ...]
    removed: tuple[RemovedRow, ...]


def database_identity(db: Any) -> str:
    """The identity of the database in front of us, for binding the watermark to.

    ``DjmdProperty.DBID`` is rekordbox's own identifier for the library, so a
    rebuilt library is a different one and a moved library is the same one. That
    is exactly the property a watermark needs: the number it holds is a position
    in one database's sequence space and is noise in another's.

    An unreadable identity REFUSES, under the slug the guarded writer already
    uses for a database that opened and then could not answer a question it must
    be able to answer. Proceeding without it would leave the watermark unbound,
    which is the state where a rebuild silently reports nothing to do forever.
    """
    try:
        held = db.get_property()
        row = held.first() if hasattr(held, "first") else held
        identity = getattr(row, "DBID", None) if row is not None else None
    except Exception as exc:  # noqa: BLE001 - any read failure is one refusal
        raise refuse(
            "canary-read-failed",
            f"the rekordbox database could not report its own identity ({exc}), "
            f"so the deletion watermark cannot be bound to it and a rebuilt "
            f"library would silently inherit a position measured in a sequence "
            f"space that no longer exists",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"column": "DBID"},
        ) from exc
    if not identity:
        raise refuse(
            "canary-read-failed",
            "the rekordbox database reports no identity of its own, so the "
            "deletion watermark has nothing to be bound to",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"column": "DBID"},
        )
    return str(identity)


def current_sequence(db: Any) -> int:
    """The library's own update counter, which is where a first run baselines to.

    R35 says a first run on an existing library baselines prior removals rather
    than presenting them, and this is the number that means "prior". It is read
    from the counter rather than computed as the maximum over the removed rows,
    because the two differ in the case that matters: a library whose only
    removals are old would baseline to an old sequence, and every row rekordbox
    touched since would then look like a removal that happened after the
    baseline. The caller takes the greater of this and the rows it saw anyway,
    which costs nothing and closes the reverse case.
    """
    try:
        return int(db.get_local_usn() or 0)
    except Exception as exc:  # noqa: BLE001 - any read failure is one refusal
        raise refuse(
            "canary-read-failed",
            f"the rekordbox database could not report its update counter "
            f"({exc}), so a first run has no position to baseline at",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"column": "localUpdateCount"},
        ) from exc


def _sequence_of(row: Any) -> int:
    """The update sequence a removed row was stamped with, or REFUSE.

    Read from ``rb_local_usn``, which the live library confirmed is fully
    populated. The sibling candidate, ``updated_at``, is a timestamp and would
    work as a watermark too; the counter is chosen because it is monotonic by
    construction rather than by the machine's clock being correct, and a clock
    that steps backwards over a library sync would make the watermark skip
    removals that had not been looked at.
    """
    value = getattr(row, "rb_local_usn", None)
    if value is None or isinstance(value, bool):
        raise refuse(
            "removal-sequence-unreadable",
            f"the removed collection row {getattr(row, 'ID', '?')!r} cannot say "
            f"which update it was removed by, so this run cannot tell whether it "
            f"is a removal somebody has already answered for; there is no safe "
            f"default, because guessing low re-offers every removal in the "
            f"library and guessing high hides this one forever",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"content_id": str(getattr(row, "ID", "")), "column": "rb_local_usn"},
        )
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise refuse(
            "removal-sequence-unreadable",
            f"the removed collection row {getattr(row, 'ID', '?')!r} reports "
            f"{value!r} as its update sequence, which is not a number this run "
            f"can compare a watermark against",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"content_id": str(getattr(row, "ID", "")), "column": "rb_local_usn"},
        ) from exc


def _text(row: Any, attribute: str) -> str:
    """One text column, with a missing column and an empty one folded together.

    Folded deliberately, and it is the opposite decision from the marker one line
    up. A missing artist name is not a permissive answer to a safety question: it
    is one field of an identity, the identity refuses when EVERY field is empty,
    and a row with no artist and a real title is an ordinary record rather than a
    row that cannot be trusted.
    """
    return str(getattr(row, attribute, "") or "")


#: The columns that can hold a mix name, in the order they are believed.
#: ``RemixerName`` is rekordbox's own dedicated field and is what the application
#: fills in from a tag; ``Subtitle`` is where the same information lands when it
#: arrived from a file whose tags spelled it that way. FIRST NON-EMPTY WINS
#: rather than both being joined, because two columns describing one mix would
#: otherwise produce a title carrying it twice, and that is a second identity for
#: one version.
_VERSION_COLUMNS: tuple[str, ...] = ("RemixerName", "Subtitle")


def _version_of(row: Any) -> str:
    """The mix name from whichever column holds it, or the empty string.

    Read through :func:`_text`, so a binding that does not expose the column at
    all answers "" rather than raising. That is the right default HERE and would
    be the wrong one for the soft-delete marker: an absent mix name leaves the
    identity exactly as wide as it was before this was read, which is the
    behaviour that shipped, while an absent marker would decide whether a row is
    somebody's music.
    """
    for column in _VERSION_COLUMNS:
        found = _text(row, column)
        if found:
            return found
    return ""


def _size_of(row: Any) -> int | None:
    value = getattr(row, "FileSize", None)
    if value is None:
        return None
    try:
        size = int(value)
    except (TypeError, ValueError):
        return None
    return size if size > 0 else None


def read_collection(rows: Iterable[Any], *, since: int) -> CollectionRead:
    """Split one walk of the collection into the active rows and the recent removals.

    ``since`` is the recorded watermark, and the comparison is STRICTLY greater:
    the watermark names the highest sequence everything at or below which has
    been handled, so a row sitting exactly on it is one this pass has already
    finished with. Using greater-or-equal would re-offer the last row of every
    previous run, forever.

    Takes an iterable of mapped rows rather than a database handle, so every
    branch here is reachable without a database and the module does no input of
    its own. The caller passes ``db.get_content()``.
    """
    active: list[trees.ContentRow] = []
    removed: list[RemovedRow] = []
    for row in rows:
        if not trees.soft_delete_marker(row):
            active.append(
                trees.ContentRow(
                    content_id=str(row.ID),
                    recorded=_text(row, "FolderPath"),
                    deleted=False,
                )
            )
            continue
        sequence = _sequence_of(row)
        if sequence <= since:
            continue
        removed.append(
            RemovedRow(
                content_id=str(row.ID),
                recorded=_text(row, "FolderPath"),
                sequence=sequence,
                size=_size_of(row),
                artist=_text(row, "ArtistName"),
                title=_text(row, "Title"),
                isrc=_text(row, "ISRC") or None,
                version=_version_of(row),
            )
        )
    return CollectionRead(active=tuple(active), removed=tuple(removed))


def playlist_referenced(memberships: Iterable[Any]) -> frozenset[str]:
    """Every content row a live playlist entry still points at.

    R37 names a candidate that resolves to a path an on-volume playlist still
    references as its own category, never as a deletion. The membership rows
    carry the soft-delete marker too, and a membership rekordbox removed is not a
    reference; reading it through the same shared reader is what stops this
    module answering the marker question a second way.

    A removed CONTENT row whose membership rows are still live is the real shape
    of this: the user dragged the track out of the collection and the playlist
    entry survived, so the file is still spoken for by something they can see.
    """
    return frozenset(
        str(row.ContentID)
        for row in memberships
        if not trees.soft_delete_marker(row)
    )


__all__ = [
    "CollectionRead",
    "RemovedRow",
    "current_sequence",
    "database_identity",
    "playlist_referenced",
    "read_collection",
]
