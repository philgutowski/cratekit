"""The one adjudication surface: persisted review items, and the decision stores.

Every state the product asks a person to adjudicate is a persisted, addressable
review item, never a file the user must hand edit (R12). So a decision is
recorded once and never re-asked, REJECTED is a first class verdict that
suppresses an item until it is cleared, and the queue is library scoped (KTD21)
and coupled to the database (KTD21b), so a decision made on one installation
holds on another.

Outputs stay files. ``SURFACES`` declares which side each legacy file is on and
why, and ``offer`` refuses a queue that is not on the adjudicated side.

An item identifier is a function of the queue, the kind and an identity the
producer supplies, never a display name (D5) or a row number, so two producers
meaning one candidate agree without coordinating.

Storage is SQLite in write ahead log mode on the job engine's pragmas: a verdict
is a transaction, a second process is a normal case, and paging is a query.

Layer note: INFRASTRUCTURE. It reads configuration and touches the disk, and it
names no verb: a producer's key arrives as a value.

Naming: ``Suppression`` is not called ``Decision``, a name already meaning two
things in this package (``core.rb_writer``, ``cli.gates``). ``Item`` does
collide with ``jobs.Item`` and stays, since every call site spells the module;
importing the bare name from the wrong module yields different fields.
"""

from __future__ import annotations

import errno
import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli.output import canonical_json, timestamp
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.private_store import PrivateStore

#: The queue's own schema version. A cross version read REFUSES rather than
#: guessing. 2 stores the identity each item was addressed by, so an identifier
#: can be audited back to what it was derived from.
SCHEMA_VERSION = 2

#: The database inside the declared ``review_queue`` state directory. The
#: directory is the declared entry, because the write ahead sidecars live beside it.
QUEUE_FILENAME = "queue.db"

#: The version stamped into an exported document. Separate from the store's
#: schema, since an export is a wire format other tooling may read.
EXPORT_VERSION = 1

#: The prefix every item identifier carries, so one is recognizable in a log.
ID_PREFIX = "rv"

#: The prefix a decision store's records carry. Different from the item prefix,
#: so an identifier pasted into the wrong verb fails to resolve.
SUPPRESSION_ID_PREFIX = "dc"


class Queue(StrEnum):
    """The declared adjudication surfaces, as stable slugs.

    A queue name is an identifier, never a display name (R19), and is declared
    here so no producer can invent a queue nobody agreed on.
    """

    #: R11's third state: a candidate that is a DIFFERENT version of the wanted
    #: recording (a remix, an edit, a live take). Two kinds share it, told apart
    #: by kind and never by payload (U79): ``version-match`` asks about a copy
    #: the library holds, ``provider-candidate`` about a provider search hit.
    VERSION_MATCH = "version-match"

    #: A candidate from somewhere other than the configured provider. One kind,
    #: ``fallback-candidate`` (U80), filed by ``crate acquire fallback`` with each
    #: option an upload's page URL.
    FALLBACK_SOURCE = "fallback-source"

    #: A proposed genre value for a track, which decides where routing puts it.
    GENRE = "genre"

    #: A release a label sweep proposes taking into the library.
    LABEL_RELEASE = "label-release"

    #: Two library entries that may be one recording or a kept alternate (R26).
    DUPLICATES = "duplicates"

    #: A file left behind by a row the user removed from the collection (R35).
    DELETION = "deletion"

    #: A proposed mapping from an existing library structure into the taxonomy (R26).
    ADOPTION = "adoption"

    #: A recorded location the library cannot resolve, and the repair's candidate.
    PATH_REPAIR = "path-repair"


class Verdict(StrEnum):
    """How an item was settled. Two of these a person writes, and one the product.

    ACCEPTED settles the item in favour of a candidate. REJECTED settles it
    against every candidate and suppresses it until somebody clears it.

    SUPERSEDED (R-679) means a later resolution owned the row under a rule that
    never consults the queue, so nothing is left to decide. It is not a
    suppression, ``clear`` revokes it like any verdict, and only
    :func:`supersede` writes it: ``PERSON_VERDICTS`` is the command line's
    vocabulary, because a person cannot truthfully record "a rule settled this".
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


#: The verdicts a PERSON records, the only ones the command line offers.
#: Derived as a subtraction, so a fourth person verdict is added in one place.
PERSON_VERDICTS: tuple[Verdict, ...] = tuple(
    member for member in Verdict if member is not Verdict.SUPERSEDED
)


# The records


@dataclass(frozen=True, slots=True)
class Option:
    """One candidate a person may choose, addressed by a stable identifier.

    ``summary`` is for a screen and never the key, so rewriting a description
    does not orphan the decision made on it (R19).
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

    ``handler_key`` names the producer, in the registry's vocabulary, as a value.
    ``ordinal`` is the insertion order and what paging keys on, so an item
    inserted mid walk never shifts a later page.
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
    #: The verdict column AS STORED, which differs from ``verdict`` only when a
    #: newer build wrote a value this one cannot represent. An export carries
    #: it, so that decision is not handed on as "nobody decided"; every reader
    #: that acts reads ``verdict`` and treats the unknown one as undecided.
    stored_verdict: str | None = None

    @property
    def resolved(self) -> bool:
        return self.verdict is not None

    @property
    def suppressed(self) -> bool:
        """True when settled AGAINST every candidate. The item stays, so it is not re-offered."""
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

    ``next_cursor`` is the last ordinal on the page, a position, never an offset.
    """

    items: tuple[Item, ...]
    next_cursor: int | None = None

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)


def _same_value(stored: Any, wanted: Any) -> bool:
    """Whether a stored payload value satisfies a predicate's wanted one.

    Equal, or equal once both are text: a predicate typed at a command line is
    text and a stored field may be a number, and a filter matching nothing reads
    as an empty queue. ``None`` never matches ``"None"``, since absent and "says
    None" are different facts.
    """
    if stored == wanted:
        return True
    if stored is None or wanted is None:
        return False
    return str(stored) == str(wanted)


@dataclass(frozen=True, slots=True)
class Predicate:
    """A declarative selection, so batch resolution crosses a process boundary.

    Data rather than a callable, so it can be typed at a command line and
    recorded against a run: a queue, a kind, and equality on payload fields.
    """

    queue: str | None = None
    kind: str | None = None
    payload_equals: Mapping[str, Any] | None = None

    def is_empty(self) -> bool:
        return self.queue is None and self.kind is None and not self.payload_equals

    def matches(self, item: Item) -> bool:
        if self.queue is not None and item.queue != self.queue:
            return False
        # The kind is normalized on both sides, as the stored one is.
        if self.kind is not None and item.kind != normalize_kind(self.kind):
            return False
        for field_name, value in (self.payload_equals or {}).items():
            if not _same_value(item.payload.get(field_name), value):
                return False
        return True


# Identity


def normalize_kind(kind: str) -> str:
    """One spelling of a kind, so two producers naming one thing agree.

    A kind is free form producer input and an identifier, never a display name
    (R19, D5), so ``version_difference`` and ``version-difference`` are one kind.
    Both the stored kind and a predicate's are normalized.
    """
    collapsed = "-".join(str(kind).replace("_", "-").replace(" ", "-").casefold().split("-"))
    return collapsed.strip("-")


def normalize_identity(identity: Mapping[str, Any]) -> dict[str, Any]:
    """The identity as it is HASHED: one spelling per value, types folded.

    Producers disagree about ``7`` and ``"7"`` (a column, a parsed file, an
    argument), so numbers fold to text. NOT folded: ``None`` stays null, ``True``
    never becomes ``1``, and surrounding whitespace is kept, since merging those
    would settle a decision nobody made. A value of any other type is REFUSED
    rather than stringified, because a text collision would merge silently.
    """
    return {str(key): _normalize_identity_value(key, value) for key, value in identity.items()}


def _normalize_identity_value(field: str, value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        # Before the numeric branch, since a bool is an int; spelled as JSON spells it.
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # An integral float is the integer, as a spreadsheet hands it back.
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
        remedy=Remedy.REPORT_DEFECT, origin=("review",),
        detail={"field": str(field), "type": type(value).__name__},
    )


def item_id_for(queue: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one candidate. A pure function of what it IS.

    Content addressed, so ``offer`` is idempotent without a lookup and two
    producers agree without knowing of each other. The identity is normalized
    and serialized canonically. An EMPTY identity is refused, since every empty
    mapping hashes alike and would collapse a queue onto one item.
    """
    if not identity:
        raise refuse(
            "review-selection-invalid",
            "a review item needs an identity to be addressed by; an empty one "
            "hashes to a single value, so every item in the queue would collide "
            "onto it and the collision would look like deduplication",
            remedy=Remedy.REPORT_DEFECT, origin=("review",),
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
    """Refuse a queue the split does not declare, naming the ones it does."""
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
            scope=Scope.RUN, origin=("review",),
            detail={"queue": value, "declared": list(adjudicated_queues())},
        )
    return value


# Storage

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
    # What a producer's round left unoffered, per group (R-790); never an item.
    # ADDITIVE, so ``SCHEMA_VERSION`` does not move: an older build never reads
    # it, and a bump would refuse every existing queue over it.
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
    # What a producer withheld from a queue, and why (R-798). Neither an item nor
    # a suppression: a person can return it, and the row carries what would have
    # been filed. An open item taken back into a hold (R-815) is deleted in the
    # same transaction. Additive, as above.
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
    # The highest ordinal a deleted item ever held (R-815), one row, raised and
    # never lowered, so a deleted newest item's ordinal is never reused past a
    # reader's ``after`` cursor. Additive, as above.
    """
    CREATE TABLE IF NOT EXISTS ordinal_floor (
        id      INTEGER PRIMARY KEY CHECK (id = 1),
        ordinal INTEGER NOT NULL
    )
    """,
)

#: The next ordinal, as a scalar subquery: one past the highest any item holds
#: or ever held. Spelled once, so the two inserting writers agree.
_NEXT_ORDINAL = (
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
)


def _own_only(path: Path) -> None:
    """Force owner only permissions on one file, tolerating absence only.

    SQLite creates the database and sidecars under the umask, which could leave
    a world readable queue of a person's decisions (P1). A missing file is
    normal (no log beside a checkpointed database); any other failure refuses.
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
            scope=Scope.RUN, origin=("review",),
            detail={"path": str(path), "mode": config.PRIVATE_FILE_MODE},
        ) from exc


class ReviewStore(PrivateStore):
    """The connection to the queue, on the job engine's pragmas.

    ``synchronous=FULL`` because a lost verdict is a question asked again, and a
    busy timeout so two writers serialize. Every write is a read then write,
    hence the immediate transaction.
    """

    _own_only = staticmethod(_own_only)


def store_dir(cfg: config.Config) -> Path:
    """The declared review directory. Resolved through U2, never composed here."""
    return config.state_path("review_queue", cfg)


def queue_path(cfg: config.Config) -> Path:
    return store_dir(cfg) / QUEUE_FILENAME


def open_store(cfg: config.Config | None = None, *, path: Path | None = None) -> ReviewStore:
    """Open, and create if needed, the queue, its directory made private by config."""
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
            scope=Scope.RUN, origin=("review",),
            detail={"found": found, "expected": SCHEMA_VERSION},
        )


# Reading


def _coerce_verdict(raw: str | None) -> Verdict | None:
    """Read a stored verdict, degrading an unrecognized one into UNRESOLVED.

    An unknown verdict must not become a decision: a decision nobody made is
    worse than a question asked twice. Every SQL reader agrees through
    ``_UNRESOLVED``, because two builds share one library scoped queue (KTD21).
    """
    if not raw:
        return None
    try:
        return Verdict(raw)
    except ValueError:
        return None


#: The SQL predicate for "this build considers the item unresolved", and its
#: values. Derived from ``Verdict``, so a new verdict is added in one place.
_UNRESOLVED = (
    f"(verdict IS NULL OR verdict NOT IN ({', '.join('?' for _ in Verdict)}))",
    tuple(str(member) for member in Verdict),
)


def _payload_of(raw: str) -> dict[str, Any]:
    """A stored payload as every reader is shown it: a dict, else empty."""
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
    """One item, or refuse naming the identifier, so a typo is not an empty queue."""
    row = store.conn.execute(
        "SELECT * FROM review_items WHERE item_id = ?", (item_id,)
    ).fetchone()
    if row is None:
        raise refuse(
            "review-item-unknown",
            f"no review item in this library's queue has the identifier {item_id!r}",
            steps=("list the queue and take the identifier from it",),
            scope=Scope.RUN, origin=("review",),
            detail={"item_id": item_id},
        )
    return _item_from_row(row)


def find(store: ReviewStore, item_id: str) -> Item | None:
    """The stored item, or ``None`` when nobody has ever been asked this.

    ONLY AN UNKNOWN ITEM IS AN ABSENCE. Any other refusal of :func:`get` is
    raised, since a store that cannot be read is not "nobody was asked".
    """
    try:
        return get(store, item_id)
    except CratekitError as exc:
        if exc.cause.reason != "review-item-unknown":
            raise
        return None


#: How many items one page holds by default: a screenful, not a memory limit.
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

    Unresolved only by default, so a person coming back sees what is left.
    ``include_suppressed`` is separate from ``include_resolved`` so a rejection
    can be reviewed and revoked without listing everything. A non-positive
    limit is refused: SQLite reads a negative LIMIT as unbounded.
    """
    if limit is not None and int(limit) <= 0:
        raise refuse(
            "review-selection-invalid",
            f"a page holds at least one item and this asked for {int(limit)}; a "
            f"negative limit is unbounded in SQLite, so it reads the entire queue "
            f"and then discards part of what it read",
            steps=("ask for a positive number of items, or omit the limit for every item",),
            scope=Scope.RUN, origin=("review",),
            detail={"limit": int(limit)},
        )
    where = []
    values: list[Any] = []
    if queue is not None:
        where.append("queue = ?")
        values.append(_assert_declared_queue(queue))
    if kinds:
        # Normalized on both sides, as ``Predicate.matches`` does.
        where.append(f"kind IN ({', '.join('?' for _ in kinds)})")
        values.extend(normalize_kind(kind) for kind in kinds)
    if handler_key is not None:
        where.append("handler_key = ?")
        values.append(handler_key)
    if not include_resolved:
        unresolved, unresolved_values = _UNRESOLVED
        if include_suppressed:
            where.append(f"({unresolved} OR verdict = ?)")
            values.extend([*unresolved_values, str(Verdict.REJECTED)])
        else:
            where.append(unresolved)
            values.extend(unresolved_values)
    if after is not None:
        where.append("ordinal > ?")
        values.append(int(after))

    clause = f" WHERE {' AND '.join(where)}" if where else ""
    query = f"SELECT * FROM review_items{clause} ORDER BY ordinal"
    if limit is not None:
        # One more than asked for, so the query itself answers whether another page exists.
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
    """How many items are still open. A query, never a counter that can drift."""
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
    """Walk the queue a page at a time, holding one page in memory, for batch and export."""
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


# Writing


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

    IDEMPOTENT: re-offering a decided item never reopens it, overwrites its
    verdict or adds a row, and a resolved item keeps the payload it was decided
    on. An open item takes the newest payload. The identity is stored, and a
    candidate hashing onto an item with a DIFFERENT identity is refused rather
    than merged, since a merge could arrive pre-decided.
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
                (item_id, declared, stored_kind, encoded_identity, encoded_payload,
                 encoded_options, handler_key, now, now),
            )
        else:
            if row["identity"] is not None and row["identity"] != encoded_identity:
                raise refuse(
                    "review-selection-invalid",
                    f"two different candidates address the same review item "
                    f"{item_id}; the one already in the queue was offered for "
                    f"{row['identity']} and this one is for {encoded_identity}, so "
                    f"settling either would settle the other",
                    remedy=Remedy.REPORT_DEFECT, origin=("review",),
                    detail={
                        "item_id": item_id, "stored": row["identity"], "offered": encoded_identity
                    },
                )
            if row["verdict"] is None:
                # Still open: show the newest description. Writing the identity
                # backfills an imported item, since an export carries none.
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

    For a producer describing a candidate it is not offering again (R-815);
    :func:`offer` would insert a row that is gone, filing a candidate beside its
    own hold. Only over an empty verdict column, inside the write, as
    :func:`supersede`: a decided or unreadable verdict and an unknown identifier
    are each None. A CALLABLE is handed the open item's payload under the write
    lock and returns the payload to write, or None for nothing (R-840), so a
    caller changing some fields does not take back another writer's.
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


#: The payload field a producer stamps with the run that filed an item (R-790).
#: An item without it groups as an unrecorded run.
RUN_FIELD = "sweep_run"

def identity_of(store: ReviewStore, item_id: str) -> dict[str, Any] | None:
    """What this item was addressed by, or None for one that arrived by import."""
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

    An already resolved item refuses rather than being overwritten; clearing is
    the way through. An option the item does not offer refuses too.
    """
    if verdict not in PERSON_VERDICTS:
        # The machine's verdict has its own writer with its own invariants: no
        # option, only over an empty column, the rule named.
        raise refuse(
            "review-selection-invalid",
            f"{verdict} is not a verdict a person records; it is written by the "
            f"resolution that owns a row, through its own path",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM, origin=("review",),
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
            scope=Scope.ITEM, origin=("review",),
            detail={"item_id": item_id, "verdict": str(current.verdict), "actor": current.actor},
        )
    if option is not None and option not in {o.option_id for o in current.options}:
        raise refuse(
            "review-option-unknown",
            f"{option!r} is not a candidate this item offers; it offers "
            f"{', '.join(o.option_id for o in current.options) or 'none'}",
            steps=("choose one of the candidates the item offers, or record no candidate",),
            scope=Scope.ITEM, origin=("review",),
            detail={"item_id": item_id, "option": option},
        )
    now = timestamp()
    unresolved, unresolved_values = _UNRESOLVED
    with store.immediate() as conn:
        # Re-checked inside the transaction, so two racing processes yield one
        # winner, against the reader's unresolved predicate: an item shown as a
        # question because its verdict is unreadable can take an answer.
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
            scope=Scope.ITEM, origin=("review",),
            detail={"item_id": item_id, "verdict": str(settled.verdict)},
        )
    return get(store, item_id)


def clear(store: ReviewStore, item_id: str, *, actor: str) -> Item:
    """Revoke a verdict, putting the item back in front of a person (R35, R36).

    ``actor`` becomes the item's recorded actor: who reopened it. The early
    return reads the raw column, so an unreadable verdict is cleared too.
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

    Writes :attr:`Verdict.SUPERSEDED` with ``rule`` as the actor and no option,
    since the rule chose no candidate. ONLY OVER AN EMPTY COLUMN, narrower than
    ``resolve``: an unreadable verdict a newer build wrote is a decision, so an
    accepted, rejected or unreadable verdict stands. Never a refusal for an
    item settled or unknown; the producer asks about every question a row could
    have raised. One read finds the open ones and one guarded write retires
    them, and the items retired HERE are returned, read back by this stamp.
    """
    if not rule:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
            "would record that something settled the question and not what",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM, origin=("review",),
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

    An item another process settles or removes mid sweep is skipped, not
    raised, so the sweep reports what it did. An EMPTY predicate is refused, as
    it would answer a person's whole backlog without them.
    """
    if predicate.is_empty():
        raise refuse(
            "review-selection-invalid",
            "a batch resolution needs a predicate that selects something; an empty "
            "one matches the entire queue, which is a decision nobody made about "
            "items nobody looked at",
            steps=("name a queue, a kind, or a payload field to match on",),
            scope=Scope.RUN, origin=("review",),
            detail={},
        )
    settled: list[Item] = []
    # Collected before resolving: mutating under an open cursor skips matches.
    targets = [item.item_id for item in iter_items(store, predicate=predicate)]
    for item_id in targets:
        try:
            settled.append(resolve(store, item_id, verdict, actor=actor))
        except CratekitError as exc:
            if exc.cause.reason not in _RACED_OUT_OF_THE_SWEEP:
                raise
            # Settled or removed by somebody else since the walk: no longer outstanding.
    return tuple(settled)


#: The refusals meaning "this identifier stopped being outstanding", the only
#: class a batch may skip; anything else is about the batch and is raised.
_RACED_OUT_OF_THE_SWEEP = frozenset({"review-already-resolved", "review-item-unknown"})


# The decision stores: declines and tombstones, the one JSON file this module writes


@dataclass(frozen=True, slots=True)
class Suppression:
    """One recorded decision that suppresses something, and its revocation.

    A review item's record shape minus the candidates. A revoked record is KEPT
    with its revocation, so a tombstone stays listable and revocable (R36).
    """

    suppression_id: str
    kind: str
    payload: Mapping[str, Any]
    actor: str
    recorded: str
    #: What the identifier was derived from, so it can be audited. Optional: a
    #: record written before this field existed is still valid.
    identity: Mapping[str, Any] | None = None
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
            "identity": dict(self.identity) if self.identity is not None else None,
            "payload": dict(self.payload),
            "actor": self.actor,
            "recorded": self.recorded,
            "revoked": self.revoked,
            "revoked_at": self.revoked_at,
            "revoked_by": self.revoked_by,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Suppression:
        held = data.get("identity")
        return cls(
            suppression_id=str(data["id"]),
            kind=str(data.get("kind", "")),
            identity=dict(held) if isinstance(held, Mapping) else None,
            payload=dict(data.get("payload") or {}),
            actor=str(data.get("actor") or ""),
            recorded=str(data.get("recorded") or ""),
            revoked=bool(data.get("revoked", False)),
            revoked_at=data.get("revoked_at"),
            revoked_by=data.get("revoked_by"),
        )


#: The version of the DOCUMENT a decision store writes. Its own constant, apart
#: from the export's and the queue's, since each format has its own readers.
DECISION_STORE_VERSION = 1


def decision_store_keys() -> tuple[str, ...]:
    """The state entries that ARE decision stores, derived from the inventory (P3).

    R35's declines and R36's tombstones are the two the plan names.
    """
    return tuple(sorted(entry.key for entry in config.STATE_FILES if entry.decision_store))


#: The same set as a constant, computed once at import from the inventory.
DECISION_STORE_KEYS: tuple[str, ...] = decision_store_keys()


class DecisionStore:
    """A revocable set of suppressions, on one of the declared state entries.

    It shares the review item's identity rule: a content derived identifier,
    never a display name. A document rather than a database, because the
    inventory declares each as one file read whole to answer "is this
    suppressed". Every read then write cycle is taken under a sibling lock, as
    the queue has ``BEGIN IMMEDIATE``: an atomic rename alone lets a second
    writer discard the first one's record while both report success.
    """

    def __init__(self, key: str, cfg: config.Config) -> None:
        if key not in DECISION_STORE_KEYS:
            raise refuse(
                "review-queue-undeclared",
                f"{key!r} is not a declared decision store; declared: "
                f"{', '.join(DECISION_STORE_KEYS)}",
                steps=("declare the store in the state inventory before writing it",),
                scope=Scope.RUN, origin=("review",),
                detail={"key": key, "declared": list(DECISION_STORE_KEYS)},
            )
        self.key = key
        self.path = config.state_path(key, cfg)
        #: The sibling lock, on a NEVER_RESTORED entry of its own: a restore
        #: replaces the coupled stores' directory, and a lock inside it would
        #: lose its inode under every process holding it.
        self.lock_path = config.state_path("decision_store_locks", cfg) / f"{key}.lock"

    def _unusable(self, what: str, exc: BaseException | None = None) -> CratekitError:
        """One refusal for every way this document is unusable; the shape rides on the detail."""
        return refuse(
            "review-file-unusable",
            f"the {self.key} store at {self.path.name} could not be read ({what}), "
            f"so what it suppresses is unknown; treating it as empty would "
            f"re-acquire exactly what somebody removed on purpose",
            steps=("repair or restore the store before running anything that consults it",),
            scope=Scope.RUN, origin=("review",),
            detail={"store": self.key, "problem": what},
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        """Hold the sibling lock across one read then write cycle.

        BLOCKING, so writers serialize rather than raise at a person. The lock
        file persists after release, as the config lock's does, so no second
        process locks a fresh inode. A platform with no advisory locking
        refuses rather than proceeding unlocked.
        """
        config.mkdir_private(self.lock_path.parent)
        try:
            handle = config.flock_exclusive(self.lock_path, _own_only)
        except (ImportError, OSError) as exc:
            raise refuse(
                "review-file-unusable",
                f"the {self.key} store could not be locked ({exc}), and writing it "
                f"unlocked loses whatever a second process is writing at the same "
                f"time, silently, while reporting success",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN, origin=("review",),
                detail={"store": self.key, "lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            handle.close()

    def _read(self) -> dict[str, Suppression]:
        """Load the store, refusing anything it cannot RECOGNIZE.

        An unreadable store read as empty un-suppresses everything in it, and the
        next write would delete every prior decline. So refusal is the only
        alternative to a correct read, for bad JSON and for good JSON that is not
        this store alike.
        """
        found, raw = config.read_json_as_text(self.path, self._unusable)
        if not found:
            return {}
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> dict[str, Suppression]:
        """Turn a parsed document into records, or refuse. Positively, field by field."""
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a store")
        version = raw.get("version")
        if version != DECISION_STORE_VERSION:
            raise self._unusable(
                f"it says version {version!r} and this build writes "
                f"{DECISION_STORE_VERSION}"
            )
        store = raw.get("store")
        if store != self.key:
            raise self._unusable(f"it is the {store!r} store and this is {self.key!r}")
        entries = raw.get("decisions")
        if not isinstance(entries, list):
            raise self._unusable(
                f"its decisions are a {type(entries).__name__} rather than a list"
            )
        found: dict[str, Suppression] = {}
        for position, entry in enumerate(entries):
            if not isinstance(entry, Mapping):
                raise self._unusable(f"record {position} is a {type(entry).__name__}")
            if not entry.get("id"):
                raise self._unusable(f"record {position} has no identifier")
            if entry.get("payload") is not None and not isinstance(entry["payload"], Mapping):
                raise self._unusable(f"record {position} has a payload that is not a mapping")
            if entry.get("identity") is not None and not isinstance(entry["identity"], Mapping):
                raise self._unusable(f"record {position} has an identity that is not a mapping")
            suppression = Suppression.from_json(entry)
            found[suppression.suppression_id] = suppression
        return found

    def _write(self, recorded: Mapping[str, Suppression]) -> None:
        payload = {
            "version": DECISION_STORE_VERSION, "store": self.key,
            "decisions": [recorded[key].to_json() for key in sorted(recorded)],
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), self.path
        )

    def record(
        self, *, kind: str, identity: Mapping[str, Any], payload: Mapping[str, Any] | None = None,
        actor: str, beside: Sequence[tuple[str, Mapping[str, Any], Mapping[str, Any]]] = (),
    ) -> Suppression:
        """Suppress something, idempotently, and return the record.

        Re-recording a suppressing record changes nothing, timestamp included;
        re-recording a REVOKED one suppresses it again.

        ``beside`` holds the other records of one decision, each a (kind,
        identity, payload), written in the SAME write and ONLY when this record
        is written, so no half state survives a failure and a companion a person
        lifted alone does not come back. A companion already standing is left as
        it is. The whole cycle is under the lock, since the read decides the write.
        """
        identifier = suppression_id_for(self.key, kind, identity)
        with self._locked():
            recorded = self._read()
            existing = recorded.get(identifier)
            if existing is not None and existing.suppressing:
                return existing
            suppression = Suppression(
                suppression_id=identifier,
                kind=normalize_kind(kind),
                identity=normalize_identity(identity),
                payload=dict(payload or {}),
                actor=actor,
                recorded=timestamp(),
            )
            recorded[identifier] = suppression
            for other_kind, other_identity, other_payload in beside:
                other_id = suppression_id_for(self.key, other_kind, other_identity)
                standing = recorded.get(other_id)
                if standing is not None and standing.suppressing:
                    continue
                recorded[other_id] = Suppression(
                    suppression_id=other_id, kind=normalize_kind(other_kind),
                    identity=normalize_identity(other_identity),
                    payload=dict(other_payload or {}), actor=actor, recorded=suppression.recorded,
                )
            self._write(recorded)
            return suppression

    def revoke(
        self, suppression_id: str, *, actor: str,
        also: Callable[[Suppression, Mapping[str, Suppression]], Iterable[str]] | None = None,
    ) -> Suppression:
        """Lift a suppression, keeping the record of it having existed.

        Under the lock, as ``record`` is: a lost revocation leaves a suppression
        standing forever. ``also`` names the records that go with this one; it is
        asked UNDER THE LOCK with the records about to be replaced, and they are
        lifted in the same write. An identifier it names that is unknown or
        already lifted is passed over.
        """
        with self._locked():
            recorded = self._read()
            existing = recorded.get(suppression_id)
            if existing is None:
                raise refuse(
                    "review-item-unknown",
                    f"no {self.key} record has the identifier {suppression_id!r}",
                    steps=("list the store and take the identifier from it",),
                    scope=Scope.RUN, origin=("review",),
                    detail={"store": self.key, "suppression_id": suppression_id},
                )
            if not existing.suppressing:
                return existing
            lifted_at = timestamp()

            def lifted(one: Suppression) -> Suppression:
                return replace(one, revoked=True, revoked_at=lifted_at, revoked_by=actor)

            with_it = tuple(also(existing, dict(recorded))) if also is not None else ()
            revoked = lifted(existing)
            recorded[suppression_id] = revoked
            for other_id in with_it:
                other = recorded.get(other_id)
                if other is not None and other.suppressing:
                    recorded[other_id] = lifted(other)
            self._write(recorded)
            return revoked

    def suppresses(self, kind: str, identity: Mapping[str, Any]) -> bool:
        """Whether this store currently suppresses that thing, refusing if it cannot be read.

        Reporting a suppressed candidate is the caller's job (R36).
        """
        found = self._read().get(suppression_id_for(self.key, kind, identity))
        return found is not None and found.suppressing

    def suppressions(self, *, include_revoked: bool = False) -> tuple[Suppression, ...]:
        """Every record, suppressing ones only unless asked for the rest (R36)."""
        found = self._read()
        return tuple(
            found[key] for key in sorted(found) if include_revoked or found[key].suppressing
        )


def suppression_id_for(store_key: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one suppression, by the review item's rule.

    Normalized the same way, so a spelling difference between the pass that
    recorded a decline and the pass consulting it never re-offers the file.
    """
    if not identity:
        raise refuse(
            "review-selection-invalid",
            "a suppression needs an identity to be addressed by; an empty one "
            "collapses every record in the store onto a single entry",
            remedy=Remedy.REPORT_DEFECT, origin=("review",),
            detail={"store": store_key, "kind": kind},
        )
    digest = hashlib.sha256(
        canonical_json(
            {"store": store_key, "kind": normalize_kind(kind),
             "identity": normalize_identity(identity)}
        ).encode()
    ).hexdigest()
    return f"{SUPPRESSION_ID_PREFIX}_{digest[:24]}"


def unresolved_cause(outstanding: int) -> Cause:
    """The cause a caller raises when it cannot proceed past open review items.

    One spelling for every producer, with steps rather than a token, since no
    single command answers every queue.
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


# The groups, the holds, the exchange and the surfaces live in modules of
# their own; each reads this module's names above, so they are imported last.
from cratekit.core.review_exchange import (  # noqa: E402
    CONFLICT_ITEM_UNUSABLE,
    CONFLICT_LOCAL_VERDICT_STANDS,
    CONFLICT_NOT_APPLIED,
    CONFLICT_VERDICT_UNREADABLE,
    ImportResult,
    export_document,
    import_document,
)
from cratekit.core.review_groups import (  # noqa: E402
    GROUPED_KINDS,
    GROUPINGS,
    Round,
    grouped,
    record_round,
    rounds,
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
from cratekit.core.review_surfaces import (  # noqa: E402
    SURFACES,
    Surface,
    adjudicated_queues,
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
