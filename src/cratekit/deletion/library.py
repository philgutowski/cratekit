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

from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.tombstone import reads_as_version
from cratekit.write import trees

#: What a version-bearing column is GUARANTEED to hold, which decides both
#: whether its value is believed and how the value is SPELLED into a title.
#: Declared kinds rather than a boolean, because the boolean answered only the
#: first question and the second one is where the tombstones were being lost.
VERSION_IS_AN_ARTIST = "artist"
VERSION_IS_A_DESIGNATION = "designation"


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
    #: What the column holding :attr:`version` is guaranteed to MEAN, which is
    #: what decides how the value is spelled into a title. An artist name and a
    #: designation compose differently and composing an artist name as though it
    #: were a designation is a tombstone no provider spelling can match. Defaults
    #: to the designation, which is the reading that changes nothing, so a caller
    #: constructing a row with a mix name in hand gets the composition that
    #: shipped rather than a silent re-spelling.
    version_kind: str = VERSION_IS_A_DESIGNATION
    #: A non-empty version column value this reader did NOT believe. Recorded so
    #: a suppression that missed can be audited: an empty ``version`` reads the
    #: same way for a row that never had one and for a row whose designation the
    #: vocabulary did not recognise, and only one of those is a defect.
    version_unbelieved: str = ""


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


def _identifier(row: Any, attribute: str) -> str:
    """One IDENTIFIER column, with a missing one folded to empty rather than to ``'None'``.

    **``str(row.ID)`` IS THE ``str(None)`` SHAPE THIS MODULE ALREADY REFUSED ONCE
    FOR ``DBID``, AND IT WAS STILL HERE FOR THE COLUMN THAT ADDRESSES EVERY
    DECISION.** A collection row whose ``ID`` is ``None`` produced the
    ``content_id`` ``'None'``, a perfectly ordinary truthy string, and that
    string then addressed the review item a person answers, the decline that
    remembers their answer, and the membership test that decides whether a
    playlist still points at the file. ``tombstone.removed_file_identity`` has a
    guard against exactly this and could never fire, because what reached it was
    already a string.

    Folded to EMPTY rather than refused here, because refusing is the identity
    module's job and it does refuse: an empty identifier reaches it and is turned
    away, ``stores.identifiable`` reports the row unidentifiable, and
    ``candidates.categorize`` answers ``UNIDENTIFIABLE`` before anything is
    resolved. That keeps one rule in one place and keeps a single unaddressable
    row from stopping a pass over a library full of good ones.
    """
    value = getattr(row, attribute, None)
    return "" if value is None else str(value)


#: The columns that can hold a mix name, in the order they are believed, each
#: with what it is guaranteed to hold. FIRST BELIEVED VALUE WINS rather than the
#: two being joined, because two columns describing one mix would otherwise
#: produce a title carrying it twice, and that is a second identity for one
#: version.
#:
#: **THE TWO COLUMNS ARE NOT GUARANTEED THE SAME THING, AND THE DIFFERENCE RUNS
#: FURTHER THAN BELIEF.** ``RemixerName`` is not a text column at all: it is an
#: association proxy over ``RemixerID`` into ``djmdArtist``, exactly as
#: ``ArtistName`` is, so rekordbox's own schema says a non-empty value is the
#: ARTIST who remixed this. That makes it believed on sight, and it also makes it
#: the wrong string to put in a title: a provider spells the version ``Strobe
#: (Michael Woods Remix)`` and never ``Strobe (Michael Woods)``, so
#: ``stores.version_of`` composes this column through
#: ``tombstone.remixer_title``.
#:
#: ``Subtitle`` is a free text column that maps to ID3 ``TIT3``, "subtitle or
#: description refinement", and in real files that holds a label, a featured
#: credit or a note as often as it holds a mix name. Believing it on sight put an
#: ordinary track's identity under ``atlas (anjunadeep)``, so the consulter, which
#: asks under the bare ``Atlas`` a provider hands it, answered NOT SUPPRESSED and
#: R36 silently did not work for that row. It is believed only when it reads as a
#: version, and both error rates of that test are measured on
#: ``tombstone.VERSION_WORDS``.
_VERSION_COLUMNS: tuple[tuple[str, str], ...] = (
    ("RemixerName", VERSION_IS_AN_ARTIST),
    ("Subtitle", VERSION_IS_A_DESIGNATION),
)


def _version_of(row: Any) -> tuple[str, str, str]:
    """The mix name, what the column that held it means, and what was NOT believed.

    Read through :func:`_text`, so a binding that does not expose the column at
    all answers "" rather than raising. That is the right default HERE and would
    be the wrong one for the soft-delete marker: an absent mix name leaves the
    identity exactly as wide as it was before this was read, which is the
    behaviour that shipped, while an absent marker would decide whether a row is
    somebody's music.

    A column that is not believed is SKIPPED rather than returned empty, so the
    order in :data:`_VERSION_COLUMNS` keeps meaning what it says if a third
    column is ever added below these two.

    **AND WHAT WAS SKIPPED IS CARRIED OUT RATHER THAN DROPPED.** A ``Subtitle``
    that does not read as a version leaves the row with a bare title, which is
    the measured failure direction of a closed vocabulary and the one that costs
    the user a track. Dropping the value made that invisible after the fact: the
    tombstone's payload showed an empty version, which reads exactly like a row
    that never had one. Carried out, it goes into the payload, so an audit
    looking at a suppression that missed can see the column value the identity
    was NOT composed from, which is the first thing to look at.
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
    value = getattr(row, "FileSize", None)
    if value is None:
        return None
    try:
        size = int(value)
    except (TypeError, ValueError):
        return None
    return size if size > 0 else None


def read_collection(rows: Iterable[Any]) -> CollectionRead:
    """Split one walk of the collection into the active rows and every removal.

    EVERY removal, unfiltered, and it used to take a ``since`` that filtered
    here as well. That parameter was dead by construction rather than merely
    unused: the only production call passed ``UNBASELINED``, because the baseline
    needs the highest sequence any removal in the library carries and the filter
    needs the baseline, so the walk cannot be filtered at all. The real filter
    lives in ``run.plan``, which applies it to the rows this returns, and one
    rule expressed twice with one copy permanently switched off is a guard
    nothing can be measured against: mutate it and the suite cannot notice.

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
                    content_id=_identifier(row, "ID"),
                    recorded=_text(row, "FolderPath"),
                    deleted=False,
                )
            )
            continue
        version, kind, unbelieved = _version_of(row)
        removed.append(
            RemovedRow(
                content_id=_identifier(row, "ID"),
                recorded=_text(row, "FolderPath"),
                sequence=_sequence_of(row),
                size=_size_of(row),
                artist=_text(row, "ArtistName"),
                title=_text(row, "Title"),
                isrc=_text(row, "ISRC") or None,
                version=version,
                version_kind=kind or VERSION_IS_A_DESIGNATION,
                version_unbelieved=unbelieved,
            )
        )
    return CollectionRead(active=tuple(active), removed=tuple(removed))


def _declared_membership_count(memberships: Any) -> int | None:
    """How many membership rows the database says it holds, or None if it cannot say.

    Asked BEFORE the walk and answered by the database rather than by the walk,
    which is the whole point: a number the walk computes cannot contradict the
    walk. A materialized sequence answers ``len``; the binding's query answers
    ``count()``, which issues its own statement. A spent cursor answers neither,
    and that is the shape this exists to catch.
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

    R37 names a candidate that resolves to a path an on-volume playlist still
    references as its own category, never as a deletion. The membership rows
    carry the soft-delete marker too, and a membership rekordbox removed is not a
    reference; reading it through the same shared reader is what stops this
    module answering the marker question a second way.

    A removed CONTENT row whose membership rows are still live is the real shape
    of this: the user dragged the track out of the collection and the playlist
    entry survived, so the file is still spoken for by something they can see.

    **THIS SET IS THE ONLY THING PROTECTING A TRACK A PLAYLIST STILL POINTS AT,
    AND IT USED TO BE THE ONE INPUT IN THIS MODULE WITH NO ASSERTION ON IT.**
    ``candidates.assert_complete`` cannot cover it: that proof is over the ACTIVE
    rows, and a removed content row is by definition absent from the active half,
    so a playlist entry is the only surviving statement that anybody still points
    at the file. A walk that answers nothing therefore reads as "no playlist
    references anything", which is the permissive answer, and the file is trashed.
    It is also the module's OWN named hazard, stated at the top of this file: the
    SECOND walk of a database cursor returns nothing at all, and that defect has
    already shipped in this repository once. It was guarded on the identity read
    and on the update sequence and left off the one input that decides whether a
    referenced file moves.

    So the database is asked how many rows it holds and the walk has to reach
    that number. A SHORT WALK REFUSES, and so does a database that cannot say,
    for the reason every other refusal here gives: there is no safe default,
    because the permissive reading of an unanswered question is the one that
    moves somebody's music.

    An honest ZERO is accepted, and only an honest one: a library whose playlists
    are all empty declares zero and walks zero, and those agree. A spent cursor
    declares nothing at all and is refused rather than read as that library.

    **THE COMPARISON IS EQUALITY RATHER THAN A FLOOR, AND IT USED TO BE A
    FLOOR.** ``walked < declared`` catches a walk that came back short and passes
    silently for a count that came back short, so any source that UNDERCOUNTS
    satisfies the proof by being wrong in the permissive direction: declare zero,
    walk one, and the assertion that exists to prove the walk complete agrees
    with a number that proves nothing. No production shape reaching it has been
    constructed, since both callers request a fresh query and ``Query.count()``
    issues its own statement, so this is a guard tightened rather than a defect
    observed. It is worth tightening because the whole point of the check is that
    the walk is compared against a number the walk did not produce, and a
    one-sided comparison quietly accepts the case where that number is the broken
    one.

    **A FAILURE INSIDE THE WALK IS A REFUSAL RATHER THAN A TRACEBACK.** The count
    is already taken through a handler that answers "it cannot say"; the walk
    itself was not, so a binding that raised partway through it reached the
    command line as an internal defect with the remedy discarded (S4). It stops
    the run either way, which is right: a membership walk that fails is a set of
    playlist references nothing can prove complete.
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
        raise refuse(
            "deletion-evidence-incomplete",
            f"the walk of this library's playlist memberships failed after "
            f"{walked} of them ({exc}), so the set of files a playlist still "
            f"points at is whatever happened to arrive before the failure; every "
            f"file missing from it would be proved unreferenced against a "
            f"question that was never fully asked",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"walked": walked},
        ) from exc
    if "" in referenced:
        # A LIVE MEMBERSHIP THAT NAMES NO ROW IS NOT A MEMBERSHIP NAMING NOTHING.
        # ``_identifier`` folds an absent column to empty, and empty matches no
        # removed row's identifier, so a reference this pass cannot address would
        # read as "no playlist points at that file" for whichever file it was
        # protecting. That is the permissive answer to the one question in this
        # module that decides whether somebody's music moves.
        raise refuse(
            "deletion-evidence-incomplete",
            "a live playlist membership in this library names no collection row, "
            "so what it points at cannot be worked out; a reference this pass "
            "cannot address would read as no reference at all, and the file it "
            "protects would be offered for deletion",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"walked": walked},
        )
    if declared is None:
        raise refuse(
            "deletion-evidence-incomplete",
            "the rekordbox database cannot say how many playlist memberships it "
            "holds, so the walk that just returned "
            f"{walked} of them cannot be shown to have seen all of them; a "
            "membership this pass did not see is a playlist reference nothing "
            "reports, and the file it protects would be offered for deletion",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"walked": walked},
        )
    if walked != declared:
        raise refuse(
            "deletion-evidence-incomplete",
            f"the rekordbox database holds {declared} playlist memberships and "
            f"this walk saw {walked} of them, so the set of files a playlist "
            f"still points at cannot be shown to be the whole set; every file "
            f"missing from it would be proved unreferenced against a question "
            f"that was never fully asked",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.library",),
            detail={"declared": declared, "walked": walked},
        )
    return frozenset(referenced)


__all__ = [
    "VERSION_IS_AN_ARTIST",
    "VERSION_IS_A_DESIGNATION",
    "CollectionRead",
    "RemovedRow",
    "current_sequence",
    "database_identity",
    "playlist_referenced",
    "read_collection",
]
