"""The one adjudication surface: persisted review items, and the decision stores.

R12 says every state the product asks a person to adjudicate is a persisted,
addressable review item, never a file the user must hand edit. The source system
answers that question with a spread of comma-separated files a person opens in a
spreadsheet, edits, and saves. Three properties of that shape are the reason this
module exists, and each one is a defect rather than a preference:

1. **Nothing is recorded, so everything is re-asked.** A decision lives in the
   edited file, the file lives in a per set directory, and the next run rebuilds
   the file from scratch. So a person answers the same question every time, and
   an item nobody has got to yet is indistinguishable from one they already
   looked at and turned down.
2. **There is no rejected state at all.** A row a person considered and declined
   simply stays in the file, which is why unresolved items roll forward forever.
   A verdict here is first class, and REJECTED suppresses the item until it is
   explicitly cleared.
3. **A decision is invisible from anywhere else.** The file is beside one set on
   one machine. An item adjudicated on one installation must not be re-asked on
   another, which is why the queue is library scoped (KTD21) and coupled to the
   database (KTD21b).

**The split, stated rather than assumed.** Not every file a person can open is an
adjudication surface. A match result, a dropped list, a reconciliation report:
those are OUTPUTS, and outputs stay files. ``SURFACES`` declares which side each
one is on and why, and ``offer`` refuses a queue name that is not on the
adjudicated side, so the split has teeth rather than being documentation. The
plan counts the source system's hand edited files at fourteen; the enumeration
below is derived from the source tree rather than transcribed from that number,
because a stated count is not a checksum (seam decisions, Part 3).

**Identity.** An item identifier is a function of the queue, the kind, and an
identity mapping the producer supplies. It is never a display name (D5), and it
is never a row number in a file, because both change under the person who made
the decision. Two producers that mean the same candidate therefore agree without
coordinating, which is what makes "the same decision is never re-asked" true
across sources rather than only within one.

**Storage.** SQLite in write ahead log mode, the same shape and the same pragmas
as the job engine, for the same reasons: a claim or a verdict is a transaction, a
second process is a first class case rather than an accident, and paging is a
query rather than a slice of a list somebody already read into memory. The
decision stores for declines and tombstones share the RECORD shape, and are
written as the single documents the state inventory declares them to be, because
each is a small revocable set rather than a queue anything pages through.

Layer note: INFRASTRUCTURE. It reads configuration and touches the disk, and it
names no verb: the key of whatever produced an item arrives as a value, exactly
as the job engine's handler key does.

TWO NAMING DECISIONS, RECORDED because the repository hunts for one symbol
meaning two things and these are the two this module could have produced.

``Suppression`` is the record a decision store holds, and it is deliberately NOT
called ``Decision``. That name already means two things in this package, in
``core.rb_writer`` and in ``cli.gates``, and the collision is recorded rather
than fixed. A third meaning would turn a recorded annoyance into a genuine trap,
and the better name was available: what these records do is suppress something.

``Item`` DOES collide, with ``jobs.Item``, and it stays. Both are "one
addressable unit inside this module's own store", which is the same shape as
``TERMINAL_STATES`` and ``lock_path`` already judged correct in this repository:
one idea specialised per module. Every call site in this codebase spells the
module, so the two are never ambiguous where they are used. The hazard, stated so
the next reader does not have to rediscover it: a caller importing the bare name
from the wrong module gets a dataclass with entirely different fields, and the
failure is an attribute error rather than anything this module can catch.
"""

from __future__ import annotations

import errno
import hashlib
import json
import os
import sqlite3
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Sequence

from cratekit.cli.output import canonical_json, timestamp
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.private_store import PrivateStore

#: The queue's own schema version. A cross version read REFUSES rather than
#: guessing, for the reason the job engine states: an unversioned state file
#: cannot be migrated without reverse engineering whatever wrote it.
#:
#: 2 stores the IDENTITY each item was addressed by. A content addressed
#: identifier with no record of what it was derived from can be audited by
#: nobody: two candidates that hash alike are indistinguishable from one
#: candidate offered twice, and a normalization that merged two things it should
#: not have leaves no evidence at all.
SCHEMA_VERSION = 2

#: The database inside the declared ``review_queue`` state directory. The
#: DIRECTORY is the declared entry, not this file, because the queue keeps its
#: write ahead sidecars beside the database and all of them belong to one root.
QUEUE_FILENAME = "queue.db"

#: The version stamped into an exported document. Separate from the store's own
#: schema on purpose: an export is a wire format that other people's tooling may
#: read, and coupling it to the storage version would force a bump on anyone
#: holding a file whenever an index changed.
EXPORT_VERSION = 1

#: The prefix every item identifier carries, so an identifier is recognizable in
#: a log or a bug report without a lookup.
ID_PREFIX = "rv"

#: The prefix a decision store's records carry. DIFFERENT from the item prefix on
#: purpose: the two identifier spaces are addressed by different verbs, and one
#: pasted into the other must fail to resolve rather than silently miss.
SUPPRESSION_ID_PREFIX = "dc"


class Queue(StrEnum):
    """The declared adjudication surfaces, as stable slugs.

    A queue name is an identifier and never a display name (R19). It is declared
    here rather than passed in freely so that a producer cannot invent a queue
    nobody agreed on, which is exactly how the source system ended up with one
    review file per feature and no shared surface at all.
    """

    #: R11's third state. A candidate that is a DIFFERENT version of the wanted
    #: recording: a remix, an edit, a live take, a clean cut.
    #:
    #: TWO KINDS SHARE IT since U79, and they are told apart by kind and never
    #: by payload. ``version-match`` asks about a copy the LIBRARY holds.
    #: ``provider-candidate`` asks which track the PROVIDER's text search found
    #: is the wanted recording, which is the question the legacy file this
    #: surface was ported from asked, so it is the same surface and not a new
    #: one. Each kind has one producer and one reader, and neither reads the
    #: other's items.
    VERSION_MATCH = "version-match"

    #: A candidate from somewhere other than the configured provider, offered
    #: because the wanted recording is not available there at all.
    #:
    #: ONE KIND since U80, ``fallback-candidate``: which SoundCloud or YouTube
    #: upload, if any, is the wanted recording. Its producer is
    #: ``crate acquire fallback`` and each option is the upload's page URL.
    FALLBACK_SOURCE = "fallback-source"

    #: A proposed genre value for a track, which decides where the routing tree
    #: puts it.
    GENRE = "genre"

    #: A release a label sweep proposes taking into the library.
    LABEL_RELEASE = "label-release"

    #: Two library entries that may be one recording, or may be an intentional
    #: alternate somebody keeps on purpose (R26's audit half).
    DUPLICATES = "duplicates"

    #: A file left behind by a row the user removed from the collection (R35).
    DELETION = "deletion"

    #: A proposed mapping from an existing library structure into the declared
    #: taxonomy (R26).
    ADOPTION = "adoption"

    #: A recorded location the library can no longer resolve, and the candidate
    #: the repair pass believes it now points at.
    PATH_REPAIR = "path-repair"


class Verdict(StrEnum):
    """How an item was settled. Two of these a person writes, and one the product.

    ACCEPTED means the item is settled in favour of a candidate. REJECTED means
    the item is settled AGAINST every candidate, and it suppresses the item until
    somebody explicitly clears it. The source system has no representation for the
    second at all, which is the whole reason its unresolved items roll forward.

    SUPERSEDED means the question was never answered because it stopped being
    one: a later resolution owned the row the item asked about under a rule that
    never consults the queue, so there is nothing left for a person to decide.
    R-679 is the shape it retires. 85 of 88 open version questions on the live
    library asked about rows the ISRC and credited rules had since settled, and
    the vocabulary had no honest way to say so: ``rejected`` records a decision
    against every candidate that nobody made, and reads as exactly wrong when the
    candidate is the very file the rule now owns. So it is a third value, NOT a
    suppression, since :attr:`Item.suppressed` stays a rejection alone, and
    revocable by ``clear`` like any verdict. It is written by :func:`supersede`
    and nothing a person types: ``PERSON_VERDICTS`` is the command line's
    vocabulary, because a person recording "a rule settled this" would be
    recording something that did not happen.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


#: The verdicts a PERSON records. The command line offers these and no other,
#: so the machine's verdict cannot be typed by hand. Derived as a subtraction
#: rather than spelled, so a fourth person verdict is added in one place.
PERSON_VERDICTS: tuple[Verdict, ...] = tuple(
    member for member in Verdict if member is not Verdict.SUPERSEDED
)


@dataclass(frozen=True, slots=True)
class Surface:
    """One place the source system asks a person something, and which side it is on.

    ``why`` is not decoration. The question "is this an adjudication surface or an
    output" is the one a porting unit has to answer for every file it inherits,
    and an answer with no reasoning attached is a coin toss somebody will re-flip.
    """

    legacy_file: str
    adjudicated: bool
    why: str
    #: The queue this surface becomes, for an adjudicated one. None for an output,
    #: and the constructor of the queue refuses anything that is not a member here.
    queue: str | None = None


#: The split, declared. Derived by reading the source tree on 2026-08-02 rather
#: than transcribed from the plan's count, per Part 3 of the seam decisions: a
#: stated count is not a checksum, and two of the plan's counts were already off.
#: New surfaces join this table; a unit that needs a queue declares it here and in
#: ``Queue`` together, because a queue with no recorded reasoning is the shape
#: this table exists to replace.
SURFACES: tuple[Surface, ...] = (
    Surface(
        legacy_file="tidal_review.csv",
        adjudicated=True,
        queue=Queue.VERSION_MATCH,
        why=(
            "The version confirm gate. A text search resolves a wanted recording "
            "to something that may be a remix, an edit, or a live take, and only "
            "a person can say whether that is the same record. R11 names this as "
            "its own state precisely so it stops being silently treated as matched."
        ),
    ),
    Surface(
        legacy_file="fetch_review.csv",
        adjudicated=True,
        queue=Queue.FALLBACK_SOURCE,
        why=(
            "Candidates from another platform for a recording the configured "
            "provider does not carry. Ranked by a heuristic that the source "
            "system's own notes say grabs the wrong track as readily as the "
            "provider search does, so the ranking proposes and a person decides."
        ),
    ),
    Surface(
        legacy_file="genre_review.csv",
        adjudicated=True,
        queue=Queue.GENRE,
        why=(
            "A proposed genre per track, with a gate column the person edits by "
            "hand and the next stage reads back. It decides where the routing "
            "tree puts the track, so a wrong value is not cosmetic."
        ),
    ),
    Surface(
        legacy_file="batch_genre_review.csv",
        adjudicated=True,
        queue=Queue.GENRE,
        why=(
            "The same decision as the file above, accumulated across a batch. It "
            "is not a second surface: two files for one question is how a person "
            "answers in one and the other keeps asking. It folds into the genre "
            "queue, which is what makes batch resolution a predicate rather than "
            "a separate file."
        ),
    ),
    Surface(
        legacy_file="genre_research_review.csv",
        adjudicated=True,
        queue=Queue.GENRE,
        why=(
            "A third file asking the genre question, produced by the research "
            "pass. Same queue for the same reason as the batch file above."
        ),
    ),
    Surface(
        legacy_file="label_review.csv",
        adjudicated=True,
        queue=Queue.LABEL_RELEASE,
        why=(
            "Releases a label sweep proposes taking in. A person decides per "
            "release, and the decision has to survive the sweep that produced it "
            "or the next sweep offers the same releases again."
        ),
    ),
    Surface(
        legacy_file="batch_label_review.csv",
        adjudicated=True,
        queue=Queue.LABEL_RELEASE,
        why=(
            "The batch form of the label decision. Folds into the same queue, for "
            "the same reason the batch genre file does."
        ),
    ),
    Surface(
        legacy_file="missing_full.csv",
        adjudicated=True,
        queue=Queue.VERSION_MATCH,
        why=(
            "The missing list once a person has curated it by hand. Curation IS "
            "adjudication: the rows a person struck out are rejections, and with "
            "no rejected state to record them in they come back on the next run. "
            "It folds into the version match queue, which is where the candidate "
            "that provoked the curation already lives."
        ),
    ),
    Surface(
        legacy_file="not_acquired.csv",
        adjudicated=True,
        queue=Queue.VERSION_MATCH,
        why=(
            "The other half of the hand curated missing list, and the same "
            "decision recorded under a second name. Folds into the same queue."
        ),
    ),
    Surface(
        legacy_file="owned.csv",
        adjudicated=False,
        why=(
            "An OUTPUT. The matched half of a match result, which R32 already "
            "carries on the match surface with its three states. Nobody edits it "
            "to decide anything, and turning a result into a queue item would ask "
            "a person to confirm what the library already proves."
        ),
    ),
    Surface(
        legacy_file="missing.csv",
        adjudicated=False,
        why=(
            "An OUTPUT, and the missing half of the same match result. It becomes "
            "adjudication only once a person curates it, which is the separate "
            "surface declared above."
        ),
    ),
    Surface(
        legacy_file="tidal_matched.csv",
        adjudicated=False,
        why="An OUTPUT: what the provider resolved, before anyone judges it.",
    ),
    Surface(
        legacy_file="tidal_unmatched.csv",
        adjudicated=False,
        why="An OUTPUT: what the provider did not resolve at all.",
    ),
    Surface(
        legacy_file="other_platforms.csv",
        adjudicated=False,
        why=(
            "An OUTPUT, and specifically a WORK queue rather than a review queue: "
            "the fallback pass reads it and produces candidates. A machine "
            "consumes it, so making a person adjudicate it would insert a "
            "decision where there is no question yet. The pass is "
            "acquire.fallback since U80, and its input is the unlisted text "
            "list rather than this file; the candidates it produces are the "
            "adjudicated half, on the fallback-source queue."
        ),
    ),
    Surface(
        legacy_file="download_dropped.csv",
        adjudicated=False,
        why="An OUTPUT: a report of what an acquisition pass did not take.",
    ),
    Surface(
        legacy_file="label_review_dropped.csv",
        adjudicated=False,
        why=(
            "An OUTPUT: what the label filter removed before a person saw it. It "
            "explains a decision the software already made rather than asking for "
            "one."
        ),
    ),
    Surface(
        legacy_file="download_reconcile.csv",
        adjudicated=False,
        why="An OUTPUT: a reconciliation report between what was asked for and what landed.",
    ),
    Surface(
        legacy_file="catalog_unmatched.csv",
        adjudicated=False,
        why="An OUTPUT: catalog rows a crawl could not resolve, reported rather than asked about.",
    ),
    Surface(
        legacy_file="",
        adjudicated=True,
        queue=Queue.DUPLICATES,
        why=(
            "NEW. The source system's duplicate audit prints and never records, "
            "so a pair somebody has already judged an intentional alternate is "
            "reported again on every run."
        ),
    ),
    Surface(
        legacy_file="",
        adjudicated=True,
        queue=Queue.DELETION,
        why=(
            "NEW, required by R35: a removed row's file is presented for review "
            "and a declined file is never offered again until the decline is "
            "revoked, which is impossible without a persisted rejected state."
        ),
    ),
    Surface(
        legacy_file="",
        adjudicated=True,
        queue=Queue.ADOPTION,
        why=(
            "NEW, required by R26: adoption presents its whole plan for review and "
            "applies it incrementally and resumably, which needs the verdicts to "
            "outlive the process that collected them."
        ),
    ),
    Surface(
        legacy_file="",
        adjudicated=True,
        queue=Queue.PATH_REPAIR,
        why=(
            "NEW. A recorded location the library cannot resolve, paired with the "
            "candidate a repair pass believes it now points at. A wrong answer "
            "here re-points a library row at somebody else's file, so it is never "
            "applied without a decision."
        ),
    ),
)


def adjudicated_queues() -> tuple[str, ...]:
    """Every declared queue, sorted. DERIVED from the split, never listed twice."""
    return tuple(sorted({s.queue for s in SURFACES if s.adjudicated and s.queue is not None}))


# ---------------------------------------------------------------------------
# The records
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Option:
    """One candidate a person may choose, addressed by a stable identifier.

    ``summary`` is for a screen and is never the key. That separation is the same
    one R19 makes for taxonomy: a candidate's description is allowed to be
    rewritten, and rewriting it must not orphan the decision somebody made.
    """

    option_id: str
    summary: str
    detail: Mapping[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "summary": self.summary,
            "detail": dict(self.detail) if self.detail else {},
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Option:
        return cls(
            option_id=data["option_id"],
            summary=data.get("summary", ""),
            detail=dict(data.get("detail") or {}) or None,
        )


@dataclass(frozen=True, slots=True)
class Item:
    """One thing a person has to decide, and the decision once they have.

    ``handler_key`` names whatever produced the item, in the registry's own
    vocabulary, and it arrives as a VALUE. This module never spells one, exactly
    as the job engine never spells the command line it re-invokes.

    ``ordinal`` is the insertion order, and it is what paging keys on. Paging on
    an offset instead would shift every later page whenever an item is inserted,
    which for a queue that grows while somebody is working through it means
    silently skipping items.
    """

    item_id: str
    queue: str
    kind: str
    payload: Mapping[str, Any]
    options: tuple[Option, ...]
    handler_key: str
    ordinal: int
    created: str
    updated: str
    verdict: Verdict | None = None
    option: str | None = None
    actor: str | None = None
    decided: str | None = None
    #: The verdict column AS STORED, which is the same text as ``verdict`` except
    #: when a newer build wrote a value this one has no representation for. Kept
    #: so an EXPORT can carry it: rendering it as "no verdict" would hand the next
    #: installation a document saying nobody had decided, and the decision would
    #: be gone with nobody told. Every reader that acts on a verdict reads
    #: ``verdict`` and therefore treats an unknown one as undecided, which is the
    #: direction ``_coerce_verdict`` argues for.
    stored_verdict: str | None = None

    @property
    def resolved(self) -> bool:
        return self.verdict is not None

    @property
    def suppressed(self) -> bool:
        """True when this item is settled AGAINST every candidate.

        A suppressed item stays in the queue rather than being deleted. Deleting
        it would make the next producer offer it again, which is the roll forward
        this module exists to end.
        """
        return self.verdict is Verdict.REJECTED

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.item_id,
            "queue": self.queue,
            "kind": self.kind,
            "ordinal": self.ordinal,
            "payload": dict(self.payload),
            "options": [option.to_json() for option in self.options],
            "handler_key": self.handler_key,
            "verdict": self.stored_verdict,
            "option": self.option,
            "actor": self.actor,
            "created": self.created,
            "updated": self.updated,
            "decided": self.decided,
        }


@dataclass(frozen=True, slots=True)
class Page:
    """One page of items, and the cursor that continues it.

    ``next_cursor`` is the last ordinal on the page rather than a count, so a
    caller resumes from a POSITION and never from an offset that other writers
    have moved underneath it.
    """

    items: tuple[Item, ...]
    next_cursor: int | None = None

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)


def _same_value(stored: Any, wanted: Any) -> bool:
    """Whether a stored payload value satisfies a predicate's wanted one.

    Equal, OR equal once both are rendered as text. The second half is not
    sloppiness, it is the difference between a filter that works and one that
    silently matches nothing: a predicate typed at a command line arrives as
    TEXT, and a payload field a producer wrote as a number is a number. Comparing
    those two with ``==`` gives False for every row, and a filter that matches
    nothing is indistinguishable from a queue that is already empty, which is the
    exact failure this module refuses everywhere else.

    Deliberately not a general coercion. ``None`` never matches the string
    ``"None"``, because "this field is absent" and "this field says None" are
    different facts and matching them would let a typo select the absent ones.
    """
    if stored == wanted:
        return True
    if stored is None or wanted is None:
        return False
    return str(stored) == str(wanted)


@dataclass(frozen=True, slots=True)
class Predicate:
    """A declarative selection, so batch resolution crosses a process boundary.

    A callable predicate cannot be typed at a command line and cannot be recorded
    against a run, and both are requirements here rather than conveniences. So the
    selection is DATA: a queue, a kind, and equality on named payload fields.
    """

    queue: str | None = None
    kind: str | None = None
    payload_equals: Mapping[str, Any] | None = None

    def is_empty(self) -> bool:
        return self.queue is None and self.kind is None and not self.payload_equals

    def matches(self, item: Item) -> bool:
        if self.queue is not None and item.queue != self.queue:
            return False
        # The kind is normalized on both sides, exactly as the stored one is. A
        # predicate typed with one spelling of a kind must not silently match
        # nothing in a queue full of the other spelling, which is the failure
        # ``_same_value`` exists to prevent one field along.
        if self.kind is not None and item.kind != normalize_kind(self.kind):
            return False
        for field_name, value in (self.payload_equals or {}).items():
            if not _same_value(item.payload.get(field_name), value):
                return False
        return True


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


def normalize_kind(kind: str) -> str:
    """One spelling of a kind, so two producers naming one thing agree.

    A kind is an identifier and never a display name (R19, D5), and it is
    free-form producer input: nothing declares the set the way ``Queue`` declares
    the surfaces. Two producers that wrote ``version-difference`` and
    ``version_difference`` therefore meant one kind and produced two items for
    one candidate, which is the exact re-asking this module exists to end.

    The stored kind is the normalized one, and so is a predicate's. Normalizing
    only the identifier would leave ``--where kind=version_difference`` matching
    nothing while the queue is full of the other spelling, which is the failure
    ``_same_value`` already exists to prevent one field along.
    """
    collapsed = "-".join(str(kind).replace("_", "-").replace(" ", "-").casefold().split("-"))
    return collapsed.strip("-")


def normalize_identity(identity: Mapping[str, Any]) -> dict[str, Any]:
    """The identity as it is HASHED: one spelling per value, types folded.

    ``canonical_json`` distinguishes ``7`` from ``"7"``, and every producer of a
    review item takes its identity from somewhere that has an opinion about the
    difference: a database column is a number, a parsed comma separated file is
    text, a command line argument is always text. Hashing the raw values made the
    same candidate two items, so the person was asked twice and the second answer
    could not be recognized as the first.

    WHAT IS DELIBERATELY NOT FOLDED. ``None`` never becomes the text ``"None"``
    or the empty string, and ``True`` never becomes ``1``. This is the same line
    ``_same_value`` draws: "this field is absent" and "this field says None" are
    different facts, and collapsing them would merge two candidates onto one item
    and settle a decision nobody made about the second. Surrounding whitespace is
    kept for the same reason, since a path and a padded copy of it are not
    obviously the same file.

    A value this cannot recognize is REFUSED rather than stringified. An object
    whose text happens to collide with another one's would silently merge two
    candidates, and there is no way to notice afterwards.
    """
    return {str(key): _normalize_identity_value(key, value) for key, value in identity.items()}


def _normalize_identity_value(field: str, value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        # Before the numeric branch: a bool IS an int in Python, and "true" is
        # what JSON calls it, so a producer writing the JSON spelling agrees.
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # An integral float is the same fact as the integer, which is how a value
        # that went through a spreadsheet comes back.
        return str(int(value)) if value.is_integer() else repr(value)
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return {str(key): _normalize_identity_value(field, held) for key, held in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_identity_value(field, held) for held in value]
    raise refuse(
        "review-selection-invalid",
        f"the identity field {field!r} holds a {type(value).__name__}, which this "
        f"queue cannot address a decision by; an identity is text, numbers, "
        f"booleans, null, and nestings of those",
        remedy=Remedy.REPORT_DEFECT,
        origin=("review",),
        detail={"field": str(field), "type": type(value).__name__},
    )


def item_id_for(queue: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one candidate. A pure function of what it IS.

    Content addressed rather than allocated, which is what makes ``offer``
    idempotent without a lookup table and what lets two producers agree on the
    same item without either knowing about the other. The identity mapping is
    NORMALIZED and then serialized canonically, so neither a different key order
    nor a different spelling of one value manufactures a second item for the same
    candidate.

    An EMPTY identity is refused. Every empty mapping hashes to one value, so an
    empty identity would collapse a whole queue onto one item, and the collapse
    would look like deduplication working rather than like a defect.
    """
    if not identity:
        raise refuse(
            "review-selection-invalid",
            "a review item needs an identity to be addressed by; an empty one "
            "hashes to a single value, so every item in the queue would collide "
            "onto it and the collision would look like deduplication",
            remedy=Remedy.REPORT_DEFECT,
            origin=("review",),
            detail={"queue": str(queue), "kind": kind},
        )
    digest = hashlib.sha256(
        canonical_json(
            {
                "queue": str(queue),
                "kind": normalize_kind(kind),
                "identity": normalize_identity(identity),
            }
        ).encode()
    ).hexdigest()
    return f"{ID_PREFIX}_{digest[:24]}"


def _assert_declared_queue(queue: str) -> str:
    """Refuse a queue the split does not declare, naming the ones it does.

    This is what gives the split teeth. Without it, ``SURFACES`` would be a
    comment: anything could be pushed into the queue, including the outputs the
    table exists to keep OUT of it.
    """
    value = str(queue)
    if value not in adjudicated_queues():
        raise refuse(
            "review-queue-undeclared",
            f"{value!r} is not a declared adjudication surface; declared: "
            f"{', '.join(adjudicated_queues())}",
            steps=(
                "declare the queue in core.review together with the reason it is "
                "an adjudication surface rather than an output",
            ),
            scope=Scope.RUN,
            origin=("review",),
            detail={"queue": value, "declared": list(adjudicated_queues())},
        )
    return value


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

_SCHEMA = (
    "CREATE TABLE IF NOT EXISTS review_schema (version INTEGER NOT NULL)",
    """
    CREATE TABLE IF NOT EXISTS review_items (
        item_id     TEXT PRIMARY KEY,
        queue       TEXT NOT NULL,
        kind        TEXT NOT NULL,
        identity    TEXT,
        payload     TEXT NOT NULL,
        options     TEXT NOT NULL,
        handler_key TEXT NOT NULL,
        ordinal     INTEGER NOT NULL,
        verdict     TEXT,
        option      TEXT,
        actor       TEXT,
        created     TEXT NOT NULL,
        updated     TEXT NOT NULL,
        decided     TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS review_open ON review_items (queue, verdict, ordinal)",
    "CREATE UNIQUE INDEX IF NOT EXISTS review_order ON review_items (ordinal)",
    # WHAT A PRODUCER'S ROUND LEFT UNOFFERED, per group (R-790). A label sweep
    # offers a window of a label's newest releases and counts the rest here, so
    # a person can see there is more and raise the window for that label. It is
    # not an item and is never decided. ADDITIVE, SO ``SCHEMA_VERSION`` DOES NOT
    # MOVE: a build that predates the table never reads it, and a version bump
    # would refuse every existing queue over a table that changes no verdict.
    """
    CREATE TABLE IF NOT EXISTS offer_rounds (
        queue      TEXT NOT NULL,
        run_id     TEXT NOT NULL,
        group_key  TEXT NOT NULL,
        group_name TEXT NOT NULL,
        beyond     INTEGER NOT NULL,
        created    TEXT NOT NULL,
        PRIMARY KEY (queue, run_id, group_key)
    )
    """,
    # WHAT A PRODUCER WITHHELD FROM A QUEUE, AND WHY (R-798). A label sweep's
    # genre gate holds back a release that is not the kind of music its label is
    # followed for. A hold is not an item: it is never listed for a decision and
    # never decided. It is not a suppression either: nothing here keeps a
    # release out for good, and a person can return one to the queue. The row
    # carries what would have been filed, so returning it needs no producer.
    # A candidate already filed and still open can be taken back into one
    # (R-815): its item row is deleted in the transaction that writes the hold.
    # ADDITIVE, on the reasoning ``offer_rounds`` gives, so ``SCHEMA_VERSION``
    # does not move.
    """
    CREATE TABLE IF NOT EXISTS held_offers (
        queue      TEXT NOT NULL,
        item_id    TEXT NOT NULL,
        kind       TEXT NOT NULL,
        identity   TEXT NOT NULL,
        payload    TEXT NOT NULL,
        group_key  TEXT NOT NULL,
        group_name TEXT NOT NULL,
        reason     TEXT NOT NULL,
        detail     TEXT NOT NULL,
        state      TEXT NOT NULL,
        run_id     TEXT NOT NULL,
        created    TEXT NOT NULL,
        updated    TEXT NOT NULL,
        PRIMARY KEY (queue, item_id)
    )
    """,
    # THE HIGHEST ORDINAL A DELETED ITEM EVER HELD (R-815). Until an item could
    # be taken back into a hold no row was ever deleted, and the next ordinal
    # was one past the highest in the table. Deleting the newest item would
    # hand its ordinal to the next one filed, and a reader holding a cursor at
    # the old highest, ``review list --after``, would never be shown it. One
    # row, raised and never lowered. ADDITIVE, on the reasoning ``offer_rounds``
    # gives. A build that predates it allocates from the items alone, which is
    # the old behaviour and no worse than it was.
    """
    CREATE TABLE IF NOT EXISTS ordinal_floor (
        id      INTEGER PRIMARY KEY CHECK (id = 1),
        ordinal INTEGER NOT NULL
    )
    """,
)

#: The next ordinal, as a scalar subquery: one past the highest any item holds
#: or ever held. Spelled once, because the two writers that insert an item must
#: not come to allocate differently.
_NEXT_ORDINAL = (
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
)


def _own_only(path: Path) -> None:
    """Force owner only permissions on one file, tolerating absence.

    SQLite creates the database and its sidecars itself, and everything it
    creates inherits the umask. Under a permissive umask that is a world readable
    queue of everything a person has decided about their library, and a world
    WRITABLE one is worse: the directory mode governs unlink and rename, so the
    file mode alone would prove nothing (P1).

    Absence is normal rather than exceptional: a database with no uncheckpointed
    transactions legitimately has no log beside it. ABSENCE ONLY, and that is the
    whole of the narrowing: tolerating every operating system error meant a chmod
    the filesystem declined left a world readable queue of everything a person
    has decided about their library, with nothing raised, on exactly the
    platforms where the mode is the only protection there is.
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    try:
        os.chmod(path, config.PRIVATE_FILE_MODE)
    except FileNotFoundError:
        return
    except OSError as exc:
        if exc.errno == errno.ENOENT:  # pragma: no cover - raised as the class above
            return
        raise refuse(
            "review-file-unusable",
            f"{path.name} could not be made owner only ({exc.strerror}), so the "
            f"queue of what this library has decided would be readable by any "
            f"account on this machine",
            steps=(
                "put the library on a filesystem that carries POSIX modes, or "
                "correct the ownership of the review directory",
            ),
            scope=Scope.RUN,
            origin=("review",),
            detail={"path": str(path), "mode": config.PRIVATE_FILE_MODE},
        ) from exc


class ReviewStore(PrivateStore):
    """The connection to the queue, on the job engine's pragmas, deliberately.

    ``synchronous=FULL`` because a verdict lost to a power cut is a question a
    person is asked again, and a busy timeout because two processes writing
    verdicts should serialize rather than raise at a user. Every write here is
    a read then write, allocate the next ordinal or read a verdict before
    replacing it, which is what the immediate transaction is for.
    """

    _own_only = staticmethod(_own_only)


def store_dir(cfg: config.Config) -> Path:
    """The declared review directory. Resolved through U2, never composed here."""
    return config.state_path("review_queue", cfg)


def queue_path(cfg: config.Config) -> Path:
    return store_dir(cfg) / QUEUE_FILENAME


def open_store(cfg: config.Config | None = None, *, path: Path | None = None) -> ReviewStore:
    """Open, and create if needed, the queue. Directory mode included.

    The directory goes through the config module's private directory helper
    rather than through ``Path.mkdir``, which applies the umask to the mode it is
    given and creates intermediate levels at 0777 regardless.
    """
    resolved = path or queue_path(cfg or config.load())
    config.mkdir_private(resolved.parent)
    store = ReviewStore(resolved)
    _initialize(store)
    return store


def _initialize(store: ReviewStore) -> None:
    for statement in _SCHEMA:
        store.conn.execute(statement)
    row = store.conn.execute("SELECT version FROM review_schema").fetchone()
    if row is None:
        store.conn.execute("INSERT INTO review_schema (version) VALUES (?)", (SCHEMA_VERSION,))
        return
    found = int(row["version"])
    if found != SCHEMA_VERSION:
        raise refuse(
            "review-schema-mismatch",
            f"the review queue was written at schema {found} and this build speaks "
            f"{SCHEMA_VERSION}; reading a verdict across versions refuses rather "
            f"than guessing what the other version meant by one",
            steps=(
                "settle the outstanding items with the version that wrote them, or "
                "export them and import the export into this one",
            ),
            scope=Scope.RUN,
            origin=("review",),
            detail={"found": found, "expected": SCHEMA_VERSION},
        )


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def _coerce_verdict(raw: str | None) -> Verdict | None:
    """Read a stored verdict, degrading an unrecognized one into UNRESOLVED.

    The direction is the load bearing half, and it is the opposite of the job
    engine's for the same reason the job engine's is what it is. There, an
    unknown state must not become a terminal one, because a false success is
    undetectable. Here, an unknown verdict must not become a decision, because a
    decision nobody made is worse than a question asked twice.

    EVERY SQL CONSUMER AGREES WITH THIS, through ``_UNRESOLVED``. They used to ask
    the raw column whether it was NULL, which is a different question, and the
    queue is library scoped by KTD21 so two installations at different versions
    share one queue and the difference is reachable. An item carrying a verdict a
    newer build wrote was then not listed, not counted, refused a resolution with
    a message that was factually false, and left unchanged by ``clear``: settled
    according to the storage and unresolved according to the reader, which is P2
    exactly, and unreachable by every route.
    """
    if not raw:
        return None
    try:
        return Verdict(raw)
    except ValueError:
        return None


#: The SQL predicate for "this build considers the item unresolved", and its
#: values. DERIVED from ``Verdict`` rather than spelled, so a third verdict is
#: added in one place: a member added to the enum and forgotten here would make
#: every listing disagree with every reader again.
_UNRESOLVED = (
    f"(verdict IS NULL OR verdict NOT IN ({', '.join('?' for _ in Verdict)}))",
    tuple(str(member) for member in Verdict),
)


def _payload_of(raw: str) -> dict[str, Any]:
    """A stored payload as every reader is shown it. Never anything but a dict.

    Text that is not JSON, and JSON that is not an object, are both the empty
    payload. One reader, so a write that starts from the stored payload starts
    from what a caller listing the item saw.
    """
    try:
        payload = json.loads(raw)
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _item_from_row(row: sqlite3.Row) -> Item:
    payload = _payload_of(row["payload"])
    try:
        options = json.loads(row["options"])
    except ValueError:
        options = []
    return Item(
        item_id=row["item_id"],
        queue=row["queue"],
        kind=row["kind"],
        payload=payload,
        options=tuple(
            Option.from_json(option) for option in options if isinstance(option, dict)
        ),
        handler_key=row["handler_key"],
        ordinal=int(row["ordinal"]),
        created=row["created"],
        updated=row["updated"],
        verdict=_coerce_verdict(row["verdict"]),
        stored_verdict=row["verdict"],
        option=row["option"],
        actor=row["actor"],
        decided=row["decided"],
    )


def get(store: ReviewStore, item_id: str) -> Item:
    """One item, or refuse naming the identifier that did not resolve.

    Returning None would make a mistyped identifier indistinguishable from an
    empty queue, and the user's next move after each of those is different.
    """
    row = store.conn.execute(
        "SELECT * FROM review_items WHERE item_id = ?", (item_id,)
    ).fetchone()
    if row is None:
        raise refuse(
            "review-item-unknown",
            f"no review item in this library's queue has the identifier {item_id!r}",
            steps=("list the queue and take the identifier from it",),
            scope=Scope.RUN,
            origin=("review",),
            detail={"item_id": item_id},
        )
    return _item_from_row(row)


#: How many items one page holds when a caller does not say. Chosen to be a
#: screenful rather than a memory limit: the reason paging exists here is that a
#: person works through a queue a few at a time, and a run that materialized four
#: hundred items to show ten has already lost the property.
def find(store: ReviewStore, item_id: str) -> Item | None:
    """The stored item, or ``None`` when nobody has ever been asked this.

    ONLY AN UNKNOWN ITEM IS AN ABSENCE. Every other refusal of :func:`get` is
    re-raised, because a store that could not be read is not "nobody was asked",
    and a producer that read it as one would search and offer again over an
    answer somebody already gave. One spelling, so the two producers that ask
    this before offering cannot come to disagree about the reason.
    """
    try:
        return get(store, item_id)
    except CratekitError as exc:
        if exc.cause.reason != "review-item-unknown":
            raise
        return None


DEFAULT_PAGE = 50


def list_items(
    store: ReviewStore,
    *,
    queue: str | None = None,
    kinds: Sequence[str] | None = None,
    handler_key: str | None = None,
    include_resolved: bool = False,
    include_suppressed: bool = False,
    limit: int | None = DEFAULT_PAGE,
    after: int | None = None,
) -> Page:
    """One page of the queue, newest LAST, keyed on the insertion order.

    Unresolved only by default, which is the property the plan's second scenario
    names: a person who quits partway through a set and comes back is presented
    with what is left, not with the whole set again.

    ``include_suppressed`` is separate from ``include_resolved`` because a
    rejection is a decision a person may want to review and revoke, while the
    accepted items are simply done. Folding the two would make a rejected item
    reachable only by listing everything.

    A NON-POSITIVE limit is refused rather than interpreted. Zero and minus one
    crashed in the cursor arithmetic; minus two and below silently dropped items
    and reported success, because a negative LIMIT is unbounded in SQLite, so
    those paths read the whole queue and then sliced it in Python. That is the
    shape this function exists to avoid, arrived at by accident.
    """
    if limit is not None and int(limit) <= 0:
        raise refuse(
            "review-selection-invalid",
            f"a page holds at least one item and this asked for {int(limit)}; a "
            f"negative limit is unbounded in SQLite, so it reads the entire queue "
            f"and then discards part of what it read",
            steps=("ask for a positive number of items, or omit the limit for every item",),
            scope=Scope.RUN,
            origin=("review",),
            detail={"limit": int(limit)},
        )
    where = []
    values: list[Any] = []
    if queue is not None:
        where.append("queue = ?")
        values.append(_assert_declared_queue(queue))
    if kinds:
        # Normalized on BOTH sides, or a filter typed with one spelling of a kind
        # silently matches a queue full of the other, which is indistinguishable
        # from a queue that is already empty.
        where.append(f"kind IN ({', '.join('?' for _ in kinds)})")
        values.extend(normalize_kind(kind) for kind in kinds)
    if handler_key is not None:
        where.append("handler_key = ?")
        values.append(handler_key)
    if not include_resolved:
        if include_suppressed:
            unresolved, unresolved_values = _UNRESOLVED
            where.append(f"({unresolved} OR verdict = ?)")
            values.extend([*unresolved_values, str(Verdict.REJECTED)])
        else:
            unresolved, unresolved_values = _UNRESOLVED
            where.append(unresolved)
            values.extend(unresolved_values)
    if after is not None:
        where.append("ordinal > ?")
        values.append(int(after))

    clause = f" WHERE {' AND '.join(where)}" if where else ""
    query = f"SELECT * FROM review_items{clause} ORDER BY ordinal"
    if limit is not None:
        # One more than asked for, so "is there another page" is answered by the
        # query rather than by a second count that can disagree with it.
        query += " LIMIT ?"
        values.append(int(limit) + 1)

    rows = store.conn.execute(query, tuple(values)).fetchall()
    if limit is not None and len(rows) > limit:
        rows = rows[:limit]
        cursor: int | None = int(rows[-1]["ordinal"])
    else:
        cursor = None
    return Page(items=tuple(_item_from_row(row) for row in rows), next_cursor=cursor)


def count_unresolved(store: ReviewStore, *, queue: str | None = None) -> int:
    """How many items are still open. A query, never a counter kept beside them.

    A counter and the rows it counts can disagree after a crash. A query cannot,
    and this number is what the structured output reports as outstanding work.
    """
    unresolved, values = _UNRESOLVED
    if queue is None:
        row = store.conn.execute(
            f"SELECT COUNT(*) AS n FROM review_items WHERE {unresolved}", values
        ).fetchone()
    else:
        row = store.conn.execute(
            f"SELECT COUNT(*) AS n FROM review_items WHERE {unresolved} AND queue = ?",
            (*values, _assert_declared_queue(queue)),
        ).fetchone()
    return int(row["n"])


def iter_items(
    store: ReviewStore,
    *,
    predicate: Predicate | None = None,
    include_resolved: bool = False,
    page: int = DEFAULT_PAGE,
) -> Iterator[Item]:
    """Walk the queue a page at a time, holding one page in memory at once.

    Used by batch resolution and by export. Both of those are the operations most
    likely to meet a queue with thousands of items in it, and both would otherwise
    be written as "read everything, then filter", which is the shape that makes
    the paging in ``list_items`` decorative.
    """
    cursor: int | None = None
    while True:
        current = list_items(
            store,
            queue=predicate.queue if predicate is not None else None,
            kinds=(predicate.kind,) if predicate is not None and predicate.kind else None,
            include_resolved=include_resolved,
            include_suppressed=include_resolved,
            limit=page,
            after=cursor,
        )
        for item in current.items:
            if predicate is None or predicate.matches(item):
                yield item
        if current.next_cursor is None:
            return
        cursor = current.next_cursor


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def offer(
    store: ReviewStore,
    *,
    queue: str,
    kind: str,
    identity: Mapping[str, Any],
    payload: Mapping[str, Any],
    options: Sequence[Option] = (),
    handler_key: str = "",
) -> Item:
    """Put a candidate in the queue, or return the one that is already there.

    IDEMPOTENT, and that is the whole requirement. A producer re-offering an item
    a person has already decided must not reopen it, must not overwrite the
    verdict, and must not create a second row. The source system re-prompts
    unconditionally every run because there is nothing to be idempotent against.

    The payload of an ALREADY RESOLVED item is left alone. Refreshing it would
    mean the decision on record was made against something the store no longer
    shows, which is the staleness the plan digest exists to prevent one layer up.

    THE IDENTITY IS STORED, and a second candidate that hashes onto an existing
    item with a DIFFERENT identity is refused rather than merged. Merging is the
    failure that looks most like the feature working: the second producer's
    candidate silently becomes the first one's, and if the first is already
    settled the second arrives pre-decided by a person who never saw it.
    """
    declared = _assert_declared_queue(queue)
    item_id = item_id_for(declared, kind, identity)
    stored_kind = normalize_kind(kind)
    encoded_identity = canonical_json(normalize_identity(identity))
    now = timestamp()
    encoded_payload = json.dumps(dict(payload), sort_keys=True)
    encoded_options = json.dumps([option.to_json() for option in options])
    with store.immediate() as conn:
        row = conn.execute(
            "SELECT verdict, identity FROM review_items WHERE item_id = ?", (item_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO review_items (item_id, queue, kind, identity, payload, options, "
                "handler_key, ordinal, verdict, option, actor, created, updated, decided) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, "
                f"{_NEXT_ORDINAL}, "
                "NULL, NULL, NULL, ?, ?, NULL)",
                (
                    item_id,
                    declared,
                    stored_kind,
                    encoded_identity,
                    encoded_payload,
                    encoded_options,
                    handler_key,
                    now,
                    now,
                ),
            )
        else:
            if row["identity"] is not None and row["identity"] != encoded_identity:
                raise refuse(
                    "review-selection-invalid",
                    f"two different candidates address the same review item "
                    f"{item_id}; the one already in the queue was offered for "
                    f"{row['identity']} and this one is for {encoded_identity}, so "
                    f"settling either would settle the other",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("review",),
                    detail={
                        "item_id": item_id,
                        "stored": row["identity"],
                        "offered": encoded_identity,
                    },
                )
            if row["verdict"] is None:
                # Still open, so the newest description of the candidate is the
                # useful one: a producer that learned more about it since the last
                # run should show a person what it knows now. The identity is
                # written too, which backfills an item that arrived through an
                # import, since the export wire format carries no identity.
                conn.execute(
                    "UPDATE review_items SET identity = ?, payload = ?, options = ?, "
                    "handler_key = ?, updated = ? WHERE item_id = ?",
                    (encoded_identity, encoded_payload, encoded_options, handler_key, now, item_id),
                )
    return get(store, item_id)


def redescribe(
    store: ReviewStore,
    item_id: str,
    payload: Mapping[str, Any] | Callable[[dict[str, Any]], Mapping[str, Any] | None],
) -> Item | None:
    """Replace the payload of an item that is STILL OPEN, or None when it is not.

    R-815. For a producer that learned something about a candidate it filed
    earlier and is not offering it again. :func:`offer` does the same rewrite,
    and it INSERTS when the row is gone, which is right for a producer that is
    filing and wrong for one that is only describing: a candidate taken back
    into a hold a moment ago would be filed again beside its own hold.

    ONLY OVER AN EMPTY VERDICT COLUMN, inside the write, on the rule
    :func:`supersede` states. A decided item keeps the payload it was decided
    on, an item carrying a verdict this build cannot read keeps its own, and an
    identifier nothing answers to creates nothing. Each is None.

    A CALLABLE CHANGES THE PAYLOAD AS IT STANDS (R-840). It is handed the open
    item's payload, read under the write lock this function already takes, and
    returns the payload to write, or None to write nothing. That is the form
    for a caller changing some fields and keeping the rest: built from a
    payload it read earlier, the same write takes back whatever another writer
    put on the item in between. It is not called for an item that is not open.
    """
    with store.immediate() as conn:
        if callable(payload):
            held = conn.execute(
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(_payload_of(held["payload"]))
            if wanted is None:
                return None
        else:
            wanted = payload
        changed = conn.execute(
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ? AND verdict IS NULL",
            (json.dumps(dict(wanted), sort_keys=True), timestamp(), item_id),
        ).rowcount
    return get(store, item_id) if changed else None


@dataclass(frozen=True, slots=True)
class Round:
    """How much one producer's round left unoffered in one group (R-790)."""

    queue: str
    run_id: str
    group: str
    name: str
    beyond: int
    created: str


def record_round(
    store: ReviewStore,
    *,
    queue: str,
    run_id: str,
    group: str,
    name: str,
    beyond: int,
) -> Round:
    """Record what a round left beyond its offer, replacing that run's earlier answer.

    REPLACED, NOT ADDED. A resumed item runs its round again under the same run
    id, and its second answer is a count of the same catalogue, so summing the
    two would report the back catalogue twice.
    """
    declared = _assert_declared_queue(queue)
    now = timestamp()
    with store.immediate() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO offer_rounds "
            "(queue, run_id, group_key, group_name, beyond, created) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (declared, run_id, group, name, int(beyond), now),
        )
    return Round(
        queue=declared, run_id=run_id, group=group, name=name, beyond=int(beyond), created=now
    )


#: The payload field a producer stamps with the run that filed an item (R-790).
#: The label sweep is the one producer that does; an item filed before it did,
#: or by another producer, carries none and groups as an unrecorded run.
RUN_FIELD = "sweep_run"

#: What ``review list --group-by`` can group each queue by: the payload field
#: holding a group's key, and the one holding its display name, if any.
GROUPINGS: Mapping[str, Mapping[str, tuple[str, str | None]]] = {
    "label-release": {"label": ("label_id", "label_name"), "run": (RUN_FIELD, None)},
}

#: The kinds a grouping counts when the caller names none. The label-release
#: queue also holds the label NAMES harvest files, ``harvested-label``, which
#: carry neither a label identifier nor a run and would collapse into one
#: nameless group beside the releases a person is counting.
GROUPED_KINDS: Mapping[str, tuple[str, ...]] = {"label-release": ("label-release",)}


def grouped(
    store: ReviewStore,
    *,
    queue: str,
    by: str,
    kinds: Sequence[str] | None = None,
    include_resolved: bool = False,
    include_suppressed: bool = False,
) -> list[dict[str, Any]]:
    """One row per group of ``queue``, counting the items the same filters list.

    READS THE WHOLE SELECTION, a page at a time, because a count per group
    over one page would be a count of the page. Rows also come from recorded
    rounds, so a label whose window is full of decided items still shows how
    much of its catalogue it never offered.

    ``beyond`` is the recorded count of releases a round never examined, less
    each a label sweep read as plainly another label's by its copyright line
    (U238): for a label, its latest round's; for a run, the sum over the labels
    it swept.
    None where nothing was recorded, which is not the same answer as zero.

    ``held`` is how many candidates of the group a producer is withholding from
    the queue now (R-798): for a label, its holds in force; for a run, the ones
    that run first held. A group with holds and no items still gets its row,
    because a label whose every listed release was held is exactly the label a
    person needs to see.
    """
    declared = _assert_declared_queue(queue)
    fields = GROUPINGS.get(declared, {}).get(by)
    if fields is None:
        raise refuse(
            "review-selection-invalid",
            f"the {declared} queue cannot be grouped by {by!r}; it groups by "
            f"{', '.join(sorted(GROUPINGS.get(declared, {}))) or 'nothing'}",
            steps=("group the label-release queue by label or by run",),
            scope=Scope.RUN,
            origin=("review",),
            detail={"queue": declared, "group_by": by},
        )
    key_field, name_field = fields
    kinds = kinds or GROUPED_KINDS.get(declared)
    counts: dict[Any, int] = {}
    names: dict[Any, str] = {}
    labels_per_run: dict[Any, set[str]] = {}
    label_key = GROUPINGS[declared].get("label", (None, None))[0]
    cursor: int | None = None
    while True:
        page = list_items(
            store,
            queue=declared,
            kinds=kinds,
            include_resolved=include_resolved,
            include_suppressed=include_suppressed,
            limit=DEFAULT_PAGE,
            after=cursor,
        )
        for item in page.items:
            key = item.payload.get(key_field) or None
            counts[key] = counts.get(key, 0) + 1
            if name_field and item.payload.get(name_field):
                names.setdefault(key, str(item.payload[name_field]))
            if by == "run" and label_key and item.payload.get(label_key):
                labels_per_run.setdefault(key, set()).add(str(item.payload[label_key]))
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    recorded = rounds(store, queue=declared)
    withheld = holds(store, queue=declared)
    held: dict[Any, int] = {}
    if by == "label":
        latest: dict[Any, Round] = {}
        for found in recorded:
            latest[found.group] = found
            names.setdefault(found.group, found.name)
        for one in withheld:
            key = one.group or None
            held[key] = held.get(key, 0) + 1
            names.setdefault(key, one.name)
        keys = sorted(
            set(counts) | set(latest) | set(held),
            key=lambda k: (names.get(k) or str(k or "")).casefold(),
        )
        return [
            {
                "label": key,
                "label_name": names.get(key, ""),
                "items": counts.get(key, 0),
                "beyond": latest[key].beyond if key in latest else None,
                "swept": latest[key].run_id if key in latest else None,
                "held": held.get(key, 0),
            }
            for key in keys
        ]
    beyond_per_run: dict[Any, int] = {}
    for found in recorded:
        beyond_per_run[found.run_id] = beyond_per_run.get(found.run_id, 0) + found.beyond
        labels_per_run.setdefault(found.run_id, set()).add(found.group)
    for one in withheld:
        key = one.run_id or None
        held[key] = held.get(key, 0) + 1
        if one.group:
            labels_per_run.setdefault(key, set()).add(one.group)
    keys = list(counts) + [key for key in beyond_per_run if key not in counts]
    keys += [key for key in held if key not in keys]
    return [
        {
            "run": key,
            "items": counts.get(key, 0),
            "labels": len(labels_per_run.get(key, set())),
            "beyond": beyond_per_run.get(key),
            "held": held.get(key, 0),
        }
        for key in keys
    ]


def rounds(store: ReviewStore, *, queue: str) -> tuple[Round, ...]:
    """Every recorded round for ``queue``, oldest first."""
    rows = store.conn.execute(
        "SELECT * FROM offer_rounds WHERE queue = ? ORDER BY created, run_id, group_key",
        (_assert_declared_queue(queue),),
    ).fetchall()
    return tuple(
        Round(
            queue=row["queue"],
            run_id=row["run_id"],
            group=row["group_key"],
            name=row["group_name"],
            beyond=int(row["beyond"]),
            created=row["created"],
        )
        for row in rows
    )


def identity_of(store: ReviewStore, item_id: str) -> dict[str, Any] | None:
    """What this item was addressed by, or None for one that arrived by import.

    An identifier derived from a value nobody kept can be audited by nobody. This
    is what makes a duplicate or a collision detectable AFTER the fact rather
    than only preventable in advance.
    """
    row = store.conn.execute(
        "SELECT identity FROM review_items WHERE item_id = ?", (item_id,)
    ).fetchone()
    if row is None or row["identity"] is None:
        return None
    try:
        held = json.loads(row["identity"])
    except ValueError:  # pragma: no cover - this column is written by one place
        return None
    return held if isinstance(held, dict) else None


def resolve(
    store: ReviewStore,
    item_id: str,
    verdict: Verdict,
    *,
    option: str | None = None,
    actor: str,
) -> Item:
    """Record a person's decision, once.

    An ALREADY RESOLVED item refuses rather than being overwritten, and the
    refusal names clearing as the way through. Silently replacing a verdict would
    make "the same decision is never re-asked" mean "the last writer wins", and
    the two are only the same until two processes disagree.

    An option that the item does not offer refuses too. A verdict pointing at a
    candidate that was never on the list is a decision about something nobody
    showed the person.
    """
    if verdict not in PERSON_VERDICTS:
        # The machine's verdict has its own writer with its own invariants: no
        # option, only over an empty column, the rule named. Letting it in here
        # would let a batch or an import land it with a candidate and a person
        # as actor, and nothing downstream could tell that from a rule that ran.
        raise refuse(
            "review-selection-invalid",
            f"{verdict} is not a verdict a person records; it is written by the "
            f"resolution that owns a row, through its own path",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("review",),
            detail={"item_id": item_id, "verdict": str(verdict)},
        )
    current = get(store, item_id)
    if current.resolved:
        raise refuse(
            "review-already-resolved",
            f"review item {item_id} is already {current.verdict}, recorded by "
            f"{current.actor!r}; a verdict is replaced by clearing it first, never "
            f"by writing over it",
            steps=("clear the verdict on this item, then record the new one",),
            scope=Scope.ITEM,
            origin=("review",),
            detail={
                "item_id": item_id,
                "verdict": str(current.verdict),
                "actor": current.actor,
            },
        )
    if option is not None and option not in {o.option_id for o in current.options}:
        raise refuse(
            "review-option-unknown",
            f"{option!r} is not a candidate this item offers; it offers "
            f"{', '.join(o.option_id for o in current.options) or 'none'}",
            steps=("choose one of the candidates the item offers, or record no candidate",),
            scope=Scope.ITEM,
            origin=("review",),
            detail={"item_id": item_id, "option": option},
        )
    now = timestamp()
    unresolved, unresolved_values = _UNRESOLVED
    with store.immediate() as conn:
        # The verdict is re-checked INSIDE the transaction. The read above is what
        # produces the good refusal message; this is what makes two processes
        # racing to answer one item resolve to one winner instead of two.
        #
        # The condition is the READER's definition of unresolved, not "the column
        # is NULL". An item carrying a verdict this build cannot read is presented
        # as a question, so the answer to that question has to be able to land.
        row = conn.execute(
            f"UPDATE review_items SET verdict = ?, option = ?, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id = ? AND {unresolved}",
            (str(verdict), option, actor, now, now, item_id, *unresolved_values),
        )
        changed = int(row.rowcount or 0)
    if not changed:
        settled = get(store, item_id)
        raise refuse(
            "review-already-resolved",
            f"review item {item_id} was resolved by another process while this one "
            f"was deciding; it is {settled.verdict}, recorded by {settled.actor!r}",
            steps=("re-read the item, and clear its verdict if the decision should change",),
            scope=Scope.ITEM,
            origin=("review",),
            detail={"item_id": item_id, "verdict": str(settled.verdict)},
        )
    return get(store, item_id)


def clear(store: ReviewStore, item_id: str, *, actor: str) -> Item:
    """Revoke a verdict, putting the item back in front of a person.

    The named way out of a rejection. R35 and R36 both require exactly this shape
    for their own stores: a decline is remembered and never offered again UNTIL
    the decline is revoked, and a tombstone is listable and revocable. An item
    that could only be rejected would be a one way door.

    ``actor`` becomes the item's recorded actor, so an open item's actor names
    whoever last touched it rather than whoever decided it. That is the useful
    answer for an item nobody has decided: the question a person asks about a
    reopened item is who reopened it.

    THE EARLY RETURN READS THE RAW COLUMN. It used to read the coerced verdict,
    so an item carrying a value this build cannot read looked unresolved, and
    ``clear`` returned without touching the row that was the whole reason
    somebody was clearing it.
    """
    current = get(store, item_id)
    if current.stored_verdict is None:
        return current
    with store.immediate() as conn:
        conn.execute(
            "UPDATE review_items SET verdict = NULL, option = NULL, actor = ?, "
            "decided = NULL, updated = ? WHERE item_id = ?",
            (actor, timestamp(), item_id),
        )
    return get(store, item_id)


def supersede(store: ReviewStore, item_ids: Sequence[str], *, rule: str) -> tuple[Item, ...]:
    """Retire the OPEN items among these, whose question a later resolution has
    answered by owning the row, recording the rule that did. R-679.

    The verdict written is :attr:`Verdict.SUPERSEDED` and the ``actor`` column
    carries ``rule``, the resolution slug that owned the row, because the rule is
    what decided and the column is where a reader looks for who did. ``option``
    stays empty: the rule owned the row on its own evidence and did not choose
    among the candidates the item offered, and writing one would claim it had.

    ONLY OVER AN EMPTY COLUMN, which is narrower than ``resolve``'s condition
    and on purpose. ``resolve`` writes over a verdict this build cannot read,
    because a person answering a question they were shown must be able to land
    the answer. This is not a person: it runs on every resolution, and a value a
    newer build wrote on the shared queue is a decision somebody made on a build
    that could represent it. Overwriting it here would discard that decision
    silently, so the raw column has to be NULL, and an ``accepted``, a
    ``rejected`` or an unreadable verdict all stand.

    NEVER A REFUSAL for an item that is settled or unknown, which is the other
    difference from ``resolve``. The producer is a resolution walking a list of
    two hundred rows, asking about every question each row COULD have been
    asked under: most were never filed, and one a person answered before the
    rule existed is the expected case, not an error on its path.

    Several at once because that is how the producer asks: one read finds
    which of the four identities are open, and one guarded write inside one
    transaction retires them, so a queue where nothing is open costs one read
    and takes no write lock. Returns the items retired HERE, read back by the
    stamp this call wrote, so a caller counts what it did and not what it
    tried, and an item a person settled between the read and the write is
    theirs.
    """
    if not rule:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
            "would record that something settled the question and not what",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("review",),
            detail={"item_ids": list(item_ids)},
        )
    wanted = tuple(dict.fromkeys(str(item_id) for item_id in item_ids))
    if not wanted:
        return ()
    marks = ", ".join("?" for _ in wanted)
    open_ids = tuple(
        row["item_id"]
        for row in store.conn.execute(
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
            (str(Verdict.SUPERSEDED), rule, now, now, *open_ids),
        )
        retired = tuple(
            row["item_id"]
            for row in conn.execute(
                f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
                f"AND verdict = ? AND actor = ? AND decided = ? ORDER BY ordinal",
                (*open_ids, str(Verdict.SUPERSEDED), rule, now),
            )
        )
    return tuple(get(store, item_id) for item_id in retired)


def resolve_where(
    store: ReviewStore,
    predicate: Predicate,
    verdict: Verdict,
    *,
    actor: str,
) -> tuple[Item, ...]:
    """Resolve every UNRESOLVED item the predicate matches, and nothing else.

    Already resolved items are skipped rather than refused, INCLUDING one that
    another process settles while this sweep is running. The skip used to be
    implemented only in the collection filter, so it held within one process and
    failed the moment a second existed: the loser of any single item raised out
    of the loop after every verdict before it had already been written, and the
    caller reported nothing at all. Observed: a sweep that settled two hundred
    items reported zero and exited 30. A batch is a filter over what is
    outstanding, and a sweep that cannot say what it did is worse than one that
    did nothing.

    An EMPTY predicate is refused. ``resolve everything`` typed by accident is one
    keystroke away from ``resolve this queue``, and the second is recoverable
    while the first is a person's whole backlog answered without them.
    """
    if predicate.is_empty():
        raise refuse(
            "review-selection-invalid",
            "a batch resolution needs a predicate that selects something; an empty "
            "one matches the entire queue, which is a decision nobody made about "
            "items nobody looked at",
            steps=("name a queue, a kind, or a payload field to match on",),
            scope=Scope.RUN,
            origin=("review",),
            detail={},
        )
    settled: list[Item] = []
    # The identifiers are collected first and resolved afterwards, because the
    # walk is a live query over the same rows the resolution updates: mutating
    # under an open cursor is how a sweep silently skips half its own matches.
    targets = [item.item_id for item in iter_items(store, predicate=predicate)]
    for item_id in targets:
        try:
            settled.append(resolve(store, item_id, verdict, actor=actor))
        except CratekitError as exc:
            if exc.cause.reason not in _RACED_OUT_OF_THE_SWEEP:
                raise
            # Somebody else settled it, or removed it, between the walk and here.
            # Both mean "no longer outstanding", which is the one thing this
            # sweep was selecting for, so it is skipped exactly as an item that
            # was already settled when the walk ran.
    return tuple(settled)


#: The refusals that mean "this identifier stopped being outstanding", which is
#: the only class a batch may skip. Anything else is about the BATCH rather than
#: about one item, and swallowing it would turn a real failure into a short
#: report nobody questions.
_RACED_OUT_OF_THE_SWEEP = frozenset({"review-already-resolved", "review-item-unknown"})


def unresolved_cause(outstanding: int) -> Cause:
    """The cause a caller raises when it cannot proceed past open review items.

    Built here so every producer reports outstanding adjudication the same way,
    rather than each inventing its own sentence. It carries the remediation as
    steps rather than a token, because the fix is to answer questions in the
    queue and there is no single command that does it for every queue.
    """
    return Cause(
        reason="awaiting-human-action",
        message=(
            f"{outstanding} review items are waiting on a person; the work they "
            f"gate cannot be decided without them"
        ),
        remediation=Remediation(
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=("work through the outstanding review items and record a verdict on each",),
        ),
        scope=Scope.RUN,
        retryable=True,
        origin=("review",),
        detail={"unresolved": outstanding},
    )



# The holds, the exchange and the decision stores live in modules of their
# own and are used from here; each reads this module's names above, so they
# are imported last.
from cratekit.core.review_exchange import (  # noqa: E402
    CONFLICT_ITEM_UNUSABLE,
    CONFLICT_LOCAL_VERDICT_STANDS,
    CONFLICT_NOT_APPLIED,
    CONFLICT_VERDICT_UNREADABLE,
    ImportResult,
    export_document,
    import_document,
)
from cratekit.core.review_holds import (  # noqa: E402
    HOLD_HELD,
    HOLD_RETURNED,
    HOLD_STATES,
    WITHHELD_FIELD,
    Hold,
    find_hold,
    hold,
    holds,
    release_hold,
    return_hold,
    withhold,
)
from cratekit.core.review_suppressions import (  # noqa: E402
    DECISION_STORE_KEYS,
    DECISION_STORE_VERSION,
    DecisionStore,
    Suppression,
    decision_store_keys,
    suppression_id_for,
)

__all__ = [
    "CONFLICT_ITEM_UNUSABLE",
    "CONFLICT_LOCAL_VERDICT_STANDS",
    "CONFLICT_NOT_APPLIED",
    "CONFLICT_VERDICT_UNREADABLE",
    "DECISION_STORE_KEYS",
    "DECISION_STORE_VERSION",
    "DEFAULT_PAGE",
    "EXPORT_VERSION",
    "ID_PREFIX",
    "QUEUE_FILENAME",
    "SCHEMA_VERSION",
    "SURFACES",
    "Suppression",
    "DecisionStore",
    "HOLD_HELD",
    "HOLD_RETURNED",
    "HOLD_STATES",
    "Hold",
    "ImportResult",
    "Item",
    "Option",
    "Page",
    "Predicate",
    "Queue",
    "ReviewStore",
    "Round",
    "Surface",
    "PERSON_VERDICTS",
    "Verdict",
    "adjudicated_queues",
    "clear",
    "supersede",
    "count_unresolved",
    "decision_store_keys",
    "suppression_id_for",
    "export_document",
    "find",
    "find_hold",
    "get",
    "hold",
    "holds",
    "identity_of",
    "import_document",
    "item_id_for",
    "iter_items",
    "list_items",
    "normalize_identity",
    "normalize_kind",
    "offer",
    "open_store",
    "queue_path",
    "record_round",
    "redescribe",
    "release_hold",
    "resolve",
    "return_hold",
    "resolve_where",
    "rounds",
    "grouped",
    "GROUPINGS",
    "GROUPED_KINDS",
    "RUN_FIELD",
    "WITHHELD_FIELD",
    "store_dir",
    "unresolved_cause",
    "withhold",
]
