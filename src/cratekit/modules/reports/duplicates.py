"""Feature Inventory row 15: the duplicate audit, and where its answers live.

The audit compares the whole collection, since the duplicate that matters is
two SEPARATE rows filed in two folders. Each group is an item in
``review.Queue.DUPLICATES``, where a REJECTED verdict IS the persistent ignore.
An item is addressed by the normalized artist and title, so moving or renaming
a copy keeps the decision. The normalization is timid on purpose (a false pair
costs a permanent suppression), and both halves of the identity are required.
Nothing here deletes or acts on a verdict; that is the deletion surface's job
(R35, R36) under its destructive session gates.

Layer note: MODULES. Gated by the ``duplicates`` toggle (R5).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from cratekit.core import review
from cratekit.core.locations import norm_for_compare
from cratekit.core.naming import NameTemplate, strip_heads
from cratekit.modules.reports.export import CollectionEntry, LibraryView

#: The kind every item in this queue carries, a stable identifier and never a
#: display name (R19, D5).
KIND = "duplicate-recording"

#: The verb whose answers these items are, so ``review.list_items`` finds them by
#: the name a person typed; an item with no handler key is invisible to that
#: query. A modules layer file naming its own verb is allowed (KTD23).
HANDLER_KEY = "audit.duplicates"


@dataclass(frozen=True, slots=True)
class Recording:
    """What two entries must agree on to be candidates for one recording.

    The identity is a MAPPING with named fields, since one joined string would
    collide across the artist and title boundary.
    """

    artist: str
    title: str

    def identity(self) -> dict[str, str]:
        """The mapping the queue addresses this recording by."""
        return {"artist": self.artist, "title": self.title}


@dataclass(frozen=True, slots=True)
class DuplicateGroup:
    """Every entry resolving to one recording: a GROUP, so three copies ask once."""

    recording: Recording
    members: tuple[CollectionEntry, ...]

    @property
    def spans_playlists(self) -> bool:
        """Whether the members sit in different places in the tree."""
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
        """One candidate per copy, so an ACCEPTED verdict names which survives.

        Nothing here reads the answer back; only the deletion surface acts on it.
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
    """What one audit found, and what of it is still an open question.

    ``outstanding`` comes from the queue: a judged group is still a group, and
    no longer a question.
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
    """One spelling of a field: NFC, case folded, whitespace collapsed.

    NFC through ``locations.norm_for_compare`` is a correctness rule, since a
    re-tag flipping the form would orphan a verdict. It runs on BOTH sides of
    the case fold, because ``casefold`` can emit a decomposed sequence.
    """
    folded = norm_for_compare(str(value)).casefold()
    return " ".join(norm_for_compare(folded).split())


def recording_of(entry: CollectionEntry, *, template: NameTemplate) -> Recording:
    """The recording an entry is a copy of.

    The title strips the naming head through the DECLARED template, since the
    head carries key, tempo and the lossy marker, which differ between copies.
    """
    return Recording(
        artist=normalize(entry.artist),
        title=normalize(strip_heads(entry.name, template=template)),
    )


def audit(view: LibraryView, *, template: NameTemplate) -> tuple[DuplicateGroup, ...]:
    """Every recording the collection holds more than one copy of.

    An entry missing EITHER half of its identity is skipped, not refused: a
    half tagged file is owed a tagging pass, not a duplicate question.
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

    IDEMPOTENT: ``offer`` is keyed on the identity, so a rerun finds the items
    and leaves their verdicts alone, and a half finished offer converges on the
    next run without holding the queue's lock for a whole walk.
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
    """The audit and the offer as one call; not ``run``, which ``cli.run`` owns."""
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
