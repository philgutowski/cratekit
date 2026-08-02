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

import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from cratekit.cli.output import canonical_json, timestamp
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The queue's own schema version. A cross version read REFUSES rather than
#: guessing, for the reason the job engine states: an unversioned state file
#: cannot be migrated without reverse engineering whatever wrote it.
SCHEMA_VERSION = 1

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
    VERSION_MATCH = "version-match"

    #: A candidate from somewhere other than the configured provider, offered
    #: because the wanted recording is not available there at all.
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
    """What a person decided. Two answers, and the second one is the new half.

    ACCEPTED means the item is settled in favour of a candidate. REJECTED means
    the item is settled AGAINST every candidate, and it suppresses the item until
    somebody explicitly clears it. The source system has no representation for the
    second at all, which is the whole reason its unresolved items roll forward.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"


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
            "decision where there is no question yet."
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
            "verdict": str(self.verdict) if self.verdict is not None else None,
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
        if self.kind is not None and item.kind != self.kind:
            return False
        for field_name, value in (self.payload_equals or {}).items():
            if not _same_value(item.payload.get(field_name), value):
                return False
        return True


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


def item_id_for(queue: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one candidate. A pure function of what it IS.

    Content addressed rather than allocated, which is what makes ``offer``
    idempotent without a lookup table and what lets two producers agree on the
    same item without either knowing about the other. The identity mapping is
    serialized canonically, so a producer that builds its mapping in a different
    key order does not manufacture a second item for the same candidate.

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
        canonical_json({"queue": str(queue), "kind": kind, "identity": dict(identity)}).encode()
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
)


def _own_only(path: Path) -> None:
    """Force owner only permissions on one file, tolerating absence.

    SQLite creates the database and its sidecars itself, and everything it
    creates inherits the umask. Under a permissive umask that is a world readable
    queue of everything a person has decided about their library, and a world
    WRITABLE one is worse: the directory mode governs unlink and rename, so the
    file mode alone would prove nothing (P1).

    Absence is normal rather than exceptional: a database with no uncheckpointed
    transactions legitimately has no log beside it.
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    try:
        os.chmod(path, config.PRIVATE_FILE_MODE)
    except OSError:
        pass


def _make_private(path: Path) -> None:
    """The database AND its sidecars, with the suffixes taken from the inventory.

    The suffix set comes from the config module rather than from a pair of
    literals here. A private copy of that list is a copy that forgets the write
    ahead log, which is where the queue's contents actually are until a
    checkpoint.
    """
    _own_only(path)
    for sidecar in config.SQLITE_SIDECARS:
        _own_only(path.with_name(path.name + sidecar.suffix))


class ReviewStore:
    """The connection to the queue, and the one place its pragmas are decided.

    The pragmas are the job engine's, deliberately: ``synchronous=FULL`` because a
    verdict lost to a power cut is a question a person is asked again, and the
    whole unit exists so that does not happen; a busy timeout because two
    processes writing verdicts should serialize rather than raise at a user.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.conn = sqlite3.connect(str(path), isolation_level=None, timeout=30.0)
        self.conn.row_factory = sqlite3.Row
        # The mode goes on BEFORE the write ahead log pragma: SQLite gives the log
        # and shared memory files the permissions the database file has when it
        # creates them, so doing this afterwards leaves two umask moded sidecars
        # beside a correctly moded database.
        _make_private(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute("PRAGMA busy_timeout=30000")

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> ReviewStore:
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    @contextmanager
    def immediate(self) -> Iterator[sqlite3.Connection]:
        """A transaction that takes the write lock UP FRONT.

        Every write here is a read then write: allocate the next ordinal, or read
        a verdict before replacing it. Under a deferred transaction two processes
        both read first and SQLite resolves it by failing one of them at COMMIT,
        after the decision has already been taken.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield self.conn
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")


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
    config._mkdir_private(resolved.parent)
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
    """
    if not raw:
        return None
    try:
        return Verdict(raw)
    except ValueError:
        return None


def _item_from_row(row: sqlite3.Row) -> Item:
    try:
        payload = json.loads(row["payload"])
    except ValueError:
        payload = {}
    try:
        options = json.loads(row["options"])
    except ValueError:
        options = []
    return Item(
        item_id=row["item_id"],
        queue=row["queue"],
        kind=row["kind"],
        payload=payload if isinstance(payload, dict) else {},
        options=tuple(
            Option.from_json(option) for option in options if isinstance(option, dict)
        ),
        handler_key=row["handler_key"],
        ordinal=int(row["ordinal"]),
        created=row["created"],
        updated=row["updated"],
        verdict=_coerce_verdict(row["verdict"]),
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
    """
    where = []
    values: list[Any] = []
    if queue is not None:
        where.append("queue = ?")
        values.append(_assert_declared_queue(queue))
    if kinds:
        where.append(f"kind IN ({', '.join('?' for _ in kinds)})")
        values.extend(kinds)
    if handler_key is not None:
        where.append("handler_key = ?")
        values.append(handler_key)
    if not include_resolved:
        if include_suppressed:
            where.append("(verdict IS NULL OR verdict = ?)")
            values.append(str(Verdict.REJECTED))
        else:
            where.append("verdict IS NULL")
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
    if queue is None:
        row = store.conn.execute(
            "SELECT COUNT(*) AS n FROM review_items WHERE verdict IS NULL"
        ).fetchone()
    else:
        row = store.conn.execute(
            "SELECT COUNT(*) AS n FROM review_items WHERE verdict IS NULL AND queue = ?",
            (_assert_declared_queue(queue),),
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
    """
    declared = _assert_declared_queue(queue)
    item_id = item_id_for(declared, kind, identity)
    now = timestamp()
    encoded_payload = json.dumps(dict(payload), sort_keys=True)
    encoded_options = json.dumps([option.to_json() for option in options])
    with store.immediate() as conn:
        row = conn.execute(
            "SELECT verdict FROM review_items WHERE item_id = ?", (item_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO review_items (item_id, queue, kind, payload, options, "
                "handler_key, ordinal, verdict, option, actor, created, updated, decided) "
                "VALUES (?, ?, ?, ?, ?, ?, "
                "(SELECT COALESCE(MAX(ordinal), 0) + 1 FROM review_items), "
                "NULL, NULL, NULL, ?, ?, NULL)",
                (
                    item_id,
                    declared,
                    kind,
                    encoded_payload,
                    encoded_options,
                    handler_key,
                    now,
                    now,
                ),
            )
        elif row["verdict"] is None:
            # Still open, so the newest description of the candidate is the
            # useful one: a producer that learned more about it since the last
            # run should show a person what it knows now.
            conn.execute(
                "UPDATE review_items SET payload = ?, options = ?, handler_key = ?, "
                "updated = ? WHERE item_id = ?",
                (encoded_payload, encoded_options, handler_key, now, item_id),
            )
    return get(store, item_id)


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
    with store.immediate() as conn:
        # The verdict is re-checked INSIDE the transaction. The read above is what
        # produces the good refusal message; this is what makes two processes
        # racing to answer one item resolve to one winner instead of two.
        row = conn.execute(
            "UPDATE review_items SET verdict = ?, option = ?, actor = ?, decided = ?, "
            "updated = ? WHERE item_id = ? AND verdict IS NULL",
            (str(verdict), option, actor, now, now, item_id),
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
    """
    current = get(store, item_id)
    if not current.resolved:
        return current
    with store.immediate() as conn:
        conn.execute(
            "UPDATE review_items SET verdict = NULL, option = NULL, actor = ?, "
            "decided = NULL, updated = ? WHERE item_id = ?",
            (actor, timestamp(), item_id),
        )
    return get(store, item_id)


def resolve_where(
    store: ReviewStore,
    predicate: Predicate,
    verdict: Verdict,
    *,
    actor: str,
) -> tuple[Item, ...]:
    """Resolve every UNRESOLVED item the predicate matches, and nothing else.

    Already resolved items are skipped rather than refused. A batch is a filter
    over what is outstanding, and making one settled item abort the whole sweep
    would mean a person could never batch resolve twice.

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
        settled.append(resolve(store, item_id, verdict, actor=actor))
    return tuple(settled)


# ---------------------------------------------------------------------------
# Export and import, for anyone who genuinely wants a file
# ---------------------------------------------------------------------------


def export_document(store: ReviewStore, *, queue: str | None = None) -> dict[str, Any]:
    """Every item, resolved ones included, as a versioned document.

    JSON rather than a comma separated file, and the difference is the point: the
    thing being replaced is a format a person edits by hand and a program reads
    back, where a stray column break silently changes what somebody decided. This
    is a transport, not an editing surface, and importing it goes through the same
    validation every other write does.
    """
    predicate = Predicate(queue=queue) if queue is not None else None
    return {
        "export": EXPORT_VERSION,
        "queue": str(queue) if queue is not None else "",
        "exported": timestamp(),
        "items": [
            item.to_json()
            for item in iter_items(store, predicate=predicate, include_resolved=True)
        ],
    }


@dataclass(frozen=True, slots=True)
class ImportResult:
    """What an import did, per item, so a caller can report rather than guess."""

    inserted: tuple[str, ...] = ()
    resolved: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


def import_document(
    store: ReviewStore, document: Mapping[str, Any], *, actor: str
) -> ImportResult:
    """Take items and verdicts back in, refusing to overwrite a local decision.

    A CONFLICT is reported and not applied. Two people who both resolved the same
    item differently is a real situation, and picking one silently is how the
    losing decision disappears with nobody told. Everything else applies: an item
    the local queue has never seen is inserted whole, and a verdict on an item
    that is locally still open is recorded.

    THE IMPORT IS TOTAL. Every item the document carries is attempted, and one
    that cannot be applied joins the conflicts rather than aborting the run. A
    partial import that stopped at item forty would leave the queue in a state
    nobody asked for and report nothing about it, which is the same shape as a
    refusal that has already written something.
    """
    version = document.get("export")
    if version != EXPORT_VERSION:
        raise refuse(
            "review-file-unusable",
            f"this export says version {version!r} and this build reads "
            f"{EXPORT_VERSION}; importing across versions would guess at what the "
            f"other one meant by a verdict",
            steps=("export again from the build that wrote this file",),
            scope=Scope.RUN,
            origin=("review",),
            detail={"found": version, "expected": EXPORT_VERSION},
        )
    inserted: list[str] = []
    applied: list[str] = []
    unchanged: list[str] = []
    conflicts: list[str] = []
    for raw in document.get("items") or ():
        if not isinstance(raw, Mapping) or not raw.get("id"):
            continue
        item_id = str(raw["id"])
        incoming = _coerce_verdict(raw.get("verdict"))
        if raw.get("verdict") and incoming is None:
            # A verdict this build has no representation for. Reported rather
            # than dropped: reading it as "no verdict" would silently discard a
            # decision somebody made, and the file would look imported.
            conflicts.append(item_id)
            continue
        row = store.conn.execute(
            "SELECT * FROM review_items WHERE item_id = ?", (item_id,)
        ).fetchone()
        if row is None:
            try:
                _insert_imported(store, raw)
            except CratekitError:
                conflicts.append(item_id)
                continue
            inserted.append(item_id)
            if incoming is not None and not _apply_incoming(store, item_id, raw, incoming, actor):
                conflicts.append(item_id)
            continue
        local = _item_from_row(row)
        if incoming is None or local.verdict is incoming:
            unchanged.append(item_id)
            continue
        if local.resolved:
            conflicts.append(item_id)
            continue
        if _apply_incoming(store, item_id, raw, incoming, actor):
            applied.append(item_id)
        else:
            conflicts.append(item_id)
    return ImportResult(
        inserted=tuple(inserted),
        resolved=tuple(applied),
        unchanged=tuple(unchanged),
        conflicts=tuple(conflicts),
    )


def _apply_incoming(
    store: ReviewStore,
    item_id: str,
    raw: Mapping[str, Any],
    verdict: Verdict,
    actor: str,
) -> bool:
    """Record an incoming verdict, reporting rather than raising when it cannot be.

    The refusals ``resolve`` raises are about THIS item: a candidate the item
    does not offer, or a race with another process. Neither says anything about
    the ninety-nine items after it in the file, so neither may end the import.
    """
    try:
        resolve(
            store,
            item_id,
            verdict,
            option=raw.get("option"),
            actor=str(raw.get("actor") or actor),
        )
    except CratekitError:
        return False
    return True


def _insert_imported(store: ReviewStore, raw: Mapping[str, Any]) -> None:
    """Insert an item that arrived from a file, at this queue's own ordinal.

    The ordinal is re-allocated rather than carried across, because it is a
    position in THIS queue. Importing somebody else's positions would interleave
    two orderings and make paging skip items on both sides of the join.
    """
    queue = _assert_declared_queue(str(raw.get("queue", "")))
    now = timestamp()
    options = [
        Option.from_json(option).to_json()
        for option in raw.get("options") or ()
        if isinstance(option, Mapping)
    ]
    with store.immediate() as conn:
        conn.execute(
            "INSERT INTO review_items (item_id, queue, kind, payload, options, "
            "handler_key, ordinal, verdict, option, actor, created, updated, decided) "
            "VALUES (?, ?, ?, ?, ?, ?, "
            "(SELECT COALESCE(MAX(ordinal), 0) + 1 FROM review_items), "
            "NULL, NULL, NULL, ?, ?, NULL)",
            (
                str(raw["id"]),
                queue,
                str(raw.get("kind", "")),
                json.dumps(dict(raw.get("payload") or {}), sort_keys=True),
                json.dumps(options),
                str(raw.get("handler_key") or ""),
                str(raw.get("created") or now),
                now,
            ),
        )


# ---------------------------------------------------------------------------
# The decision stores: declines and tombstones
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Suppression:
    """One recorded decision that suppresses something, and its revocation.

    The same record shape as a review item, minus the candidates, because the
    question has already been answered. A revoked decision is KEPT with its
    revocation recorded rather than deleted: R36 requires a tombstone to be
    listable and revocable, and a store that forgets a revocation cannot report
    that the suppression ever existed.
    """

    suppression_id: str
    kind: str
    payload: Mapping[str, Any]
    actor: str
    recorded: str
    revoked: bool = False
    revoked_at: str | None = None
    revoked_by: str | None = None

    @property
    def suppressing(self) -> bool:
        return not self.revoked

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.suppression_id,
            "kind": self.kind,
            "payload": dict(self.payload),
            "actor": self.actor,
            "recorded": self.recorded,
            "revoked": self.revoked,
            "revoked_at": self.revoked_at,
            "revoked_by": self.revoked_by,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Suppression:
        return cls(
            suppression_id=str(data["id"]),
            kind=str(data.get("kind", "")),
            payload=dict(data.get("payload") or {}),
            actor=str(data.get("actor") or ""),
            recorded=str(data.get("recorded") or ""),
            revoked=bool(data.get("revoked", False)),
            revoked_at=data.get("revoked_at"),
            revoked_by=data.get("revoked_by"),
        )


#: The state entries that are decision stores, taken from the inventory rather
#: than spelled here, so a store cannot exist at a path nobody declared a root
#: for. R35's declines and R36's tombstones are the two the plan names.
DECISION_STORE_KEYS: tuple[str, ...] = ("declines", "tombstones")


class DecisionStore:
    """A revocable set of suppressions, on one of the declared state entries.

    It shares the review item's record shape and its identity rule: a decision is
    addressed by a content derived identifier, never by a display name, so the
    thing suppressed can be renamed without the suppression being orphaned.

    It is a document rather than a database, and that is a deliberate difference
    from the queue rather than an inconsistency. The state inventory declares each
    of these as one file; a queue is paged through by a person and written by two
    processes at once, while a decision store is read whole by an acquisition pass
    to answer "is this suppressed".
    """

    def __init__(self, key: str, cfg: config.Config) -> None:
        if key not in DECISION_STORE_KEYS:
            raise refuse(
                "review-queue-undeclared",
                f"{key!r} is not a declared decision store; declared: "
                f"{', '.join(DECISION_STORE_KEYS)}",
                steps=("declare the store in the state inventory before writing it",),
                scope=Scope.RUN,
                origin=("review",),
                detail={"key": key, "declared": list(DECISION_STORE_KEYS)},
            )
        self.key = key
        self.path = config.state_path(key, cfg)

    def _read(self) -> dict[str, Suppression]:
        """Load the store, treating an unreadable file as a REFUSAL, not as empty.

        An unreadable suppression list read as empty un-suppresses everything in
        it, silently, and the next acquisition pass then re-acquires exactly what
        somebody deleted on purpose. The gate half of U8's lesson applies here
        too: a tolerant reader on a path that governs an action fails open.
        """
        if not self.path.exists():
            return {}
        try:
            raw = json.loads(self.path.read_text())
        except (OSError, ValueError) as exc:
            raise refuse(
                "review-file-unusable",
                f"the {self.key} store at {self.path.name} could not be read, so "
                f"what it suppresses is unknown; treating it as empty would "
                f"re-acquire exactly what somebody removed on purpose",
                steps=("repair or restore the store before running anything that consults it",),
                scope=Scope.RUN,
                origin=("review",),
                detail={"store": self.key},
            ) from exc
        entries = raw.get("decisions") if isinstance(raw, Mapping) else None
        found: dict[str, Suppression] = {}
        for entry in entries or ():
            if isinstance(entry, Mapping) and entry.get("id"):
                suppression = Suppression.from_json(entry)
                found[suppression.suppression_id] = suppression
        return found

    def _write(self, recorded: Mapping[str, Suppression]) -> None:
        payload = {
            "version": EXPORT_VERSION,
            "store": self.key,
            "decisions": [recorded[key].to_json() for key in sorted(recorded)],
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), self.path
        )

    def record(
        self,
        *,
        kind: str,
        identity: Mapping[str, Any],
        payload: Mapping[str, Any] | None = None,
        actor: str,
    ) -> Suppression:
        """Suppress something, idempotently, and return the record.

        Re-recording an already suppressed thing changes nothing, including its
        timestamp. Re-recording a REVOKED one re-suppresses it, which is the only
        way a person changes their mind back.
        """
        identifier = suppression_id_for(self.key, kind, identity)
        recorded = self._read()
        existing = recorded.get(identifier)
        if existing is not None and existing.suppressing:
            return existing
        suppression = Suppression(
            suppression_id=identifier,
            kind=kind,
            payload=dict(payload or {}),
            actor=actor,
            recorded=timestamp(),
        )
        recorded[identifier] = suppression
        self._write(recorded)
        return suppression

    def revoke(self, suppression_id: str, *, actor: str) -> Suppression:
        """Lift a suppression, keeping the record of it having existed."""
        recorded = self._read()
        existing = recorded.get(suppression_id)
        if existing is None:
            raise refuse(
                "review-item-unknown",
                f"no {self.key} record has the identifier {suppression_id!r}",
                steps=("list the store and take the identifier from it",),
                scope=Scope.RUN,
                origin=("review",),
                detail={"store": self.key, "suppression_id": suppression_id},
            )
        if not existing.suppressing:
            return existing
        revoked = Suppression(
            suppression_id=existing.suppression_id,
            kind=existing.kind,
            payload=existing.payload,
            actor=existing.actor,
            recorded=existing.recorded,
            revoked=True,
            revoked_at=timestamp(),
            revoked_by=actor,
        )
        recorded[suppression_id] = revoked
        self._write(recorded)
        return revoked

    def suppresses(self, kind: str, identity: Mapping[str, Any]) -> bool:
        """Whether this store currently suppresses that thing.

        Asked by an acquisition pass per candidate. It reports the suppression
        rather than omitting the candidate silently (R36), which is the caller's
        job; what this owes is a truthful answer, including a refusal when the
        store cannot be read.
        """
        found = self._read().get(suppression_id_for(self.key, kind, identity))
        return found is not None and found.suppressing

    def suppressions(self, *, include_revoked: bool = False) -> tuple[Suppression, ...]:
        """Every record, suppressing ones only unless asked for the rest.

        R36 says a tombstone is LISTABLE and revocable, and the two halves need
        each other: a revoked record that vanished from the listing would leave a
        person unable to tell "never suppressed" from "suppressed and lifted".
        """
        found = self._read()
        return tuple(
            found[key]
            for key in sorted(found)
            if include_revoked or found[key].suppressing
        )


def suppression_id_for(store_key: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one suppression. Same rule as a review item."""
    if not identity:
        raise refuse(
            "review-selection-invalid",
            "a suppression needs an identity to be addressed by; an empty one "
            "collapses every record in the store onto a single entry",
            remedy=Remedy.REPORT_DEFECT,
            origin=("review",),
            detail={"store": store_key, "kind": kind},
        )
    digest = hashlib.sha256(
        canonical_json({"store": store_key, "kind": kind, "identity": dict(identity)}).encode()
    ).hexdigest()
    return f"{SUPPRESSION_ID_PREFIX}_{digest[:24]}"


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


__all__ = [
    "DECISION_STORE_KEYS",
    "DEFAULT_PAGE",
    "EXPORT_VERSION",
    "ID_PREFIX",
    "QUEUE_FILENAME",
    "SCHEMA_VERSION",
    "SURFACES",
    "Suppression",
    "DecisionStore",
    "ImportResult",
    "Item",
    "Option",
    "Page",
    "Predicate",
    "Queue",
    "ReviewStore",
    "Surface",
    "Verdict",
    "adjudicated_queues",
    "clear",
    "count_unresolved",
    "suppression_id_for",
    "export_document",
    "get",
    "import_document",
    "item_id_for",
    "iter_items",
    "list_items",
    "offer",
    "open_store",
    "queue_path",
    "resolve",
    "resolve_where",
    "store_dir",
    "unresolved_cause",
]
