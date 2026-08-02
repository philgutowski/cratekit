"""Feature Inventory row 15: the duplicate audit, and where its answers live.

The source system's audit walks one playlist at a time and prints a track id that
appears in it twice. Two things about that are wrong rather than merely limited.

**It cannot see the duplicate that matters.** A track id inside one playlist twice
is a membership mistake, and it is the cheap case. What a library actually
accumulates is two SEPARATE collection rows for one recording: the same record
acquired twice, months apart, filed under two different genre folders, each with
its own file on disk. Scoped to a playlist, that pair is invisible by
construction, because the two entries are never in the same list. This audit
compares the whole collection, so a pair spread across two folders is exactly
what it finds (and the placements it reports are what let a person see that is
what happened).

**It prints and never records.** So a pair somebody looked at last month and
judged an intentional alternate, a clean cut kept beside the explicit, an edit
kept beside the original, is reported again on every run, forever. There is no
representation for "I decided this and the answer was no". That is R12's whole
subject, and U11 built the surface: the pair becomes an item in
``review.Queue.DUPLICATES``, and a REJECTED verdict on it IS the persistent
ignore the brief asks for. **A private ignore file beside the report would
satisfy the brief and re-create the defect**, which is why the obligation was
registered as a countdown rather than trusted to a docstring (P5).

**The identity is the recording, not the pair and not the file.** An item is
addressed by the normalized artist and title, so:

* renaming a file, re-importing it, or moving it between folders does not orphan
  the decision, because none of those is in the identity;
* a third copy arriving later does not re-ask, because the question a person
  answered was about this recording rather than about a particular pair of rows;
* two installations that see the same library agree on the item without
  coordinating, which is what makes "the same decision is never re-asked" true
  across machines rather than only within one run.

**The normalization is deliberately timid.** Case is folded and runs of
whitespace collapse, and nothing else happens: no punctuation stripping, no
guessing that ``(Original Mix)`` and the bare title are one recording. Every
widening here buys a few more true pairs and costs false ones, and a false pair
is not free: the person has to reject it, and that rejection is a permanent
suppression keyed on the guess this module made. ``review.normalize_identity``
draws the same line for the same reason.

**Nothing here deletes, and nothing here acts on a verdict.** The audit reports
and records. Acting on an ACCEPTED verdict means removing a row and trashing a
file, which belongs to the deletion surface (R35, R36) and to the destructive
session gates that surface binds to. A report that quietly trashed the copy it
liked less would be the single most destructive thing in the product wearing the
word "audit".

Layer note: MODULES. Gated by the ``duplicates`` toggle (R5).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from cratekit.core import review
from cratekit.core.naming import NameTemplate, strip_heads
from cratekit.modules.reports.export import CollectionEntry, LibraryView

#: The kind every item in this queue carries. One kind rather than several,
#: because the question is the same in every case: are these one recording. The
#: kind is a stable identifier and never a display name (R19, D5).
KIND = "duplicate-recording"


@dataclass(frozen=True, slots=True)
class Recording:
    """What two entries have to agree on to be candidates for one recording.

    A value rather than a bare string, so the identity handed to the queue is a
    MAPPING with named fields. A single joined string would hash the same way for
    ``artist="a b"`` with ``title="c"`` and ``artist="a"`` with ``title="b c"``,
    and the collision would look like the audit working.
    """

    artist: str
    title: str

    def identity(self) -> dict[str, str]:
        """The mapping the queue addresses this recording by."""
        return {"artist": self.artist, "title": self.title}


@dataclass(frozen=True, slots=True)
class DuplicateGroup:
    """Every collection entry that resolves to one recording. Two or more.

    A GROUP rather than a list of pairs. Three copies of one record produce three
    pairs, which is the same question asked three times, and a person who
    answered one of them would still be shown the other two.
    """

    recording: Recording
    members: tuple[CollectionEntry, ...]

    @property
    def spans_playlists(self) -> bool:
        """Whether the members sit in different places in the tree.

        Reported rather than filtered on. Two copies in one playlist and two
        copies in two folders are both duplicates; the difference is only how
        they got there, and a person deciding wants to know which.
        """
        seen = {member.playlists for member in self.members}
        return len(seen) > 1

    def payload(self) -> dict[str, object]:
        """What a person is shown, which is never what the item is keyed on."""
        return {
            "artist": self.recording.artist,
            "title": self.recording.title,
            "copies": len(self.members),
            "members": [
                {
                    "track_id": member.track_id,
                    "name": member.name,
                    "artist": member.artist,
                    "location": member.location,
                    "playlists": [" / ".join(path) for path in member.playlists],
                }
                for member in self.members
            ],
        }

    def options(self) -> tuple[review.Option, ...]:
        """One candidate per copy: the one a person would keep.

        Offered so an ACCEPTED verdict can name WHICH copy survives, rather than
        recording only that the group was agreed to be duplicates. Nothing in
        this module reads the answer back; the deletion surface is the only thing
        licensed to act on it.
        """
        return tuple(
            review.Option(
                option_id=member.track_id,
                summary=member.name or member.location,
                detail={"location": member.location},
            )
            for member in self.members
        )


@dataclass(frozen=True, slots=True)
class DuplicateReport:
    """What one audit found and what of it is still an open question.

    ``outstanding`` is derived from the queue rather than from the groups,
    because that is the whole point: a group somebody already judged is still a
    group, and it is not still a question.
    """

    groups: tuple[DuplicateGroup, ...]
    items: tuple[review.Item, ...]

    @property
    def outstanding(self) -> tuple[review.Item, ...]:
        return tuple(item for item in self.items if not item.resolved)

    @property
    def suppressed(self) -> tuple[review.Item, ...]:
        """Groups settled AGAINST being duplicates: the intentional alternates."""
        return tuple(item for item in self.items if item.suppressed)


def normalize(value: str) -> str:
    """One spelling of a field, so two producers of one recording agree.

    Case folded and internal whitespace collapsed. That is the whole of it, and
    the restraint is the design: see this module's own docstring for why a
    cleverer normalization costs more than it buys.
    """
    return " ".join(str(value).casefold().split())


def recording_of(entry: CollectionEntry, *, template: NameTemplate) -> Recording:
    """The recording an entry is a copy of.

    The title comes from the display field with the naming head stripped through
    the DECLARED template, never through a private pattern. This library writes
    its key and tempo into the head and marks a lossy file there too, so a
    comparison against the raw display field would call two copies of one record
    different whenever they were analysed at different times, which is most of
    them.
    """
    return Recording(
        artist=normalize(entry.artist),
        title=normalize(strip_heads(entry.name, template=template)),
    )


def audit(view: LibraryView, *, template: NameTemplate) -> tuple[DuplicateGroup, ...]:
    """Every recording the collection holds more than one copy of.

    Whole-collection, never per playlist. Entries whose artist and title are both
    empty after normalization are skipped: they carry nothing to compare, and
    grouping them would collapse every untagged file in the library onto one
    item, which would look exactly like the audit working.
    """
    found: dict[tuple[str, str], list[CollectionEntry]] = {}
    for entry in view.entries:
        recording = recording_of(entry, template=template)
        if not recording.artist and not recording.title:
            continue
        found.setdefault((recording.artist, recording.title), []).append(entry)
    return tuple(
        DuplicateGroup(
            recording=Recording(artist=artist, title=title),
            members=tuple(members),
        )
        for (artist, title), members in sorted(found.items())
        if len(members) > 1
    )


def offer_groups(
    store: review.ReviewStore,
    groups: Sequence[DuplicateGroup],
    *,
    handler_key: str = "",
) -> DuplicateReport:
    """Put each group in front of a person, or return the answer already given.

    IDEMPOTENT, and that is the requirement rather than an optimization. The
    queue's ``offer`` is keyed on the identity below, so a second run over the
    same library re-offers the same items, finds them, and leaves any verdict
    alone. A group somebody rejected comes back as suppressed rather than as a
    question, which is the persistent ignore, arrived at without this module
    keeping any state of its own.

    That idempotence is also what makes a HALF FINISHED offer safe. If the queue
    refuses partway through a large audit, the groups already offered stay
    offered and the next run converges on the same set rather than duplicating
    it, so there is no need to wrap the loop in a transaction that would hold the
    queue's write lock for the length of a whole library walk.
    """
    return DuplicateReport(
        groups=tuple(groups),
        items=tuple(
            review.offer(
                store,
                queue=review.Queue.DUPLICATES,
                kind=KIND,
                identity=group.recording.identity(),
                payload=group.payload(),
                options=group.options(),
                handler_key=handler_key,
            )
            for group in groups
        ),
    )


def audit_and_offer(
    view: LibraryView,
    store: review.ReviewStore,
    *,
    template: NameTemplate,
    handler_key: str = "",
) -> DuplicateReport:
    """The audit and the offer as one call, which is how a caller wants it.

    NOT CALLED ``run``, deliberately. ``cratekit.cli.run`` is the process-level
    dispatcher, and a second ``run`` here would be the repository's own recorded
    hazard: a caller importing the bare name from the wrong module gets an
    entirely different signature, and the failure is an argument error rather
    than anything either module can catch. The verbose name also says which of
    the two halves happens first, which is the half that matters.
    """
    return offer_groups(store, audit(view, template=template), handler_key=handler_key)


__all__ = [
    "KIND",
    "DuplicateGroup",
    "DuplicateReport",
    "Recording",
    "audit",
    "audit_and_offer",
    "normalize",
    "offer_groups",
    "recording_of",
]
