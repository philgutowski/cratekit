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

**The normalization is deliberately timid.** Composition form is folded to NFC,
case is folded, and runs of whitespace collapse. Nothing else happens: no
punctuation stripping, no guessing that ``(Original Mix)`` and the bare title are
one recording. Every widening here buys a few more true pairs and costs false
ones, and a false pair is not free: the person has to reject it, and that
rejection is a permanent suppression keyed on the guess this module made.
``review.normalize_identity`` draws the same line for the same reason.

**The NFC fold is not a widening, and it is not optional.** Two spellings of one
accented name are not two names, they are one name written twice, and this
repository has already paid for treating them as two: the incident
``core.locations`` opens on deleted 144 still-referenced files because a raw
``==`` between an NFD disk path and an NFC ``Location`` reported every accented
file as unreferenced. The same split costs two things here, and the second is
worse than the missed duplicate. A re-tag that flips the form changes the
recording, therefore changes the item id, therefore re-asks a question somebody
already answered and orphans the earlier REJECTED verdict in the queue forever,
which is exactly what the third bullet above promises cannot happen. The fold
goes through ``locations.norm_for_compare`` rather than a second call to
``unicodedata`` here, because two implementations of one rule that agree today
disagree eventually and the disagreement is invisible until it has destroyed
something.

**Both halves of the identity are required.** An entry carrying an artist and no
title is not half a recording, it is a person's name, and grouping on it puts
every untagged file by one artist into one fabricated group. The dangerous
direction is the ACCEPTED verdict: it names which copy survives and licenses the
deletion surface to act on what may be three unrelated recordings.

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
from cratekit.core.locations import norm_for_compare
from cratekit.core.naming import NameTemplate, strip_heads
from cratekit.modules.reports.export import CollectionEntry, LibraryView

#: The kind every item in this queue carries. One kind rather than several,
#: because the question is the same in every case: are these one recording. The
#: kind is a stable identifier and never a display name (R19, D5).
KIND = "duplicate-recording"

#: The verb whose answers these items are, so ``review.list_items`` can be asked
#: for them by the name a person typed. Spelled here rather than left to the
#: caller because the registry already declares it for this verb, and a default
#: of "" opted every item this module produced out of the addressability
#: property ``test_conformance_4`` asserts for every adjudicating verb: an item
#: with no handler key is invisible to the one query a person has.
#:
#: A modules-layer file naming its own verb is the direction KTD23 allows, and
#: ``test_a_module_layer_file_may_name_its_own_concepts`` says so explicitly.
#: The rule is that a LOWER layer may not name a higher one.
HANDLER_KEY = "audit.duplicates"


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

    Composition folded to NFC, case folded, and internal whitespace collapsed.
    That is the whole of it, and the restraint is the design: see this module's
    own docstring for why a cleverer normalization costs more than it buys, and
    for why the NFC fold is not part of that restraint but a correctness rule
    this repository has already been billed for once.

    THE COMPOSITION FOLD RUNS ON BOTH SIDES OF THE CASE FOLD, which looks like a
    belt and braces and is not. ``norm_for_compare`` deliberately does not
    case-fold, which its own docstring says out loud, so the two are separate
    steps; and ``casefold`` can itself emit a decomposed sequence for a character
    whose lowercase form carries a combining mark, so composing only before it
    would hand back exactly the split this function exists to remove.
    """
    folded = norm_for_compare(str(value)).casefold()
    return " ".join(norm_for_compare(folded).split())


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

    Whole-collection, never per playlist. An entry missing EITHER half of its
    identity is skipped, and the rule is "both are required" rather than "not
    both are missing" because the half-tagged case fails the same way the
    untagged one does. Three files with no title and the artist ``Recondite``
    are three different records; grouped, they become one item with three
    options, and the collapse looks exactly like the audit working. The
    dangerous direction is the ACCEPTED verdict, which names which copy survives
    and hands the deletion surface a licence over three unrelated recordings.

    Reported by omission rather than by refusal, because a library legitimately
    holds files nobody has finished tagging and refusing the whole audit over
    them would be a report nobody can run. What is owed to those files is a
    tagging pass, not a duplicate question.
    """
    found: dict[tuple[str, str], list[CollectionEntry]] = {}
    for entry in view.entries:
        recording = recording_of(entry, template=template)
        if not recording.artist or not recording.title:
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
    handler_key: str = HANDLER_KEY,
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
    handler_key: str = HANDLER_KEY,
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
    "HANDLER_KEY",
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
