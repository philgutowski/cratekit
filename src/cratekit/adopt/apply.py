"""Applying a plan: approval first, one entry at a time, and resumable.

RESUMABLE BY IDENTIFIER, not by a counter or a position. The ledger records the
identifier of every entry that landed, and the next run's work is the plan's
applicable entries minus those. A plan that grew, shrank or reordered between
two runs (somebody answered a genre question) still resumes correctly.

THE ORDER PER ENTRY IS: PLACE, RECORD THE ORIGINAL, WRITE THE TAG, MARK APPLIED.
A membership row is inside the database snapshot (KTD21b, R30); a genre string
in a file is outside every safety net. The recoverable write goes first, so a
refusal costs nothing: with the tag write first, one systemic refusal inside
``place`` left six files holding adoption's genre and an empty applied ledger.
The loop still never stops on a refusal, whatever scope it declares
(:func:`cratekit.core.cause.refuse` defaults to ``Scope.RUN``, so breaking on it
ended the pass on an ordinary per-track refusal, the failure U19 paid for).

WHAT A SECOND RUN DOES AFTER A CRASH AT EACH STEP:

* Before ``place``: nothing was written, and the re-run proceeds.
* Between ``place`` and the revert record: the re-run places again, a no-op by
  the membership writer's own dedup. No file was touched.
* Between the record and the tag write: the record holds what the file still
  has, so a revert is a no-op; the re-run keeps the record and writes the tag.
* Between the tag write and the mark: the re-run applies again, and the revert
  record is NOT refreshed, which is what keeps the original safe.
* During the mark (an append since U254): the torn last line reads as the mark
  that did not finish, which is the case above, and the next mark cuts it away.
* After the mark: nothing is outstanding for the entry. Correct.

The record and the tag write are ONE act, through
:func:`cratekit.adopt.revert.write_tag_with_record`, so a revert cannot land
between them. The membership write arrives as a parameter because which medium
a tree is written in is the tree registry's answer and how is
:mod:`cratekit.write.trees`'s; this module owns the approval, the order and the
ledger.

Layer: modules.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.adopt import revert
from cratekit.adopt.approval import require_approval
from cratekit.adopt.plan import AdoptionPlan, PlanEntry
from cratekit.adopt.revert_record import lock_for, read_document, read_raw
from cratekit.cli.output import timestamp
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.write.routing_pass import destination

#: The state entry this module owns.
STATE_KEY = "adoption_ledger"

#: The declared lock directory, shared with the revert ledger.
LOCK_KEY = "adoption_locks"

#: Bumped only when the on-disk shape changes incompatibly. 2 since U254: a
#: journal, a header line and one record appended per mark. A whole document at
#: 1 still reads and becomes a journal at its next mark.
SCHEMA_VERSION = 2

#: The schema of the whole document every build before U254 wrote on every mark.
DOCUMENT_SCHEMA_VERSION = 1

#: What a journal's header line says it is, which no document's first line says.
JOURNAL_FORMAT = "journal"

#: The tag field adoption writes when it writes one at all, named once so the
#: revert ledger's records and this module cannot disagree about it.
ADOPTED_TAG_FIELD = "genre"


class AppliedLedgerUnreadable(revert.LedgerUnreadable):
    """The applied ledger exists and cannot be understood.

    Never collapsed into "nothing applied yet": an empty ledger re-applies an
    approved plan from its first entry against a library that holds most of it.
    """

    document = STATE_KEY


#: Each field of a record, and the key it is written under on disk.
_KEYS = (
    ("entry_id", "entry"),
    ("tree", "tree"),
    ("content_id", "content"),
    ("bucket", "bucket"),
    ("sub", "sub"),
    ("actor", "actor"),
    ("digest", "digest"),
    ("applied", "applied"),
)


@dataclass(frozen=True, slots=True)
class AppliedEntry:
    """One plan entry that landed, and who was responsible for it.

    ``digest`` is the plan digest the approval was recorded against, kept per
    record so a ledger holding two approvals' work says which each piece is
    (R34).
    """

    entry_id: str
    tree: str
    content_id: str
    bucket: str
    sub: str
    actor: str
    digest: str
    applied: str

    def to_json(self) -> dict[str, Any]:
        return {key: getattr(self, name) for name, key in _KEYS}


@dataclass(frozen=True, slots=True)
class AppliedLedger:
    """Everything adoption has already applied to this library.

    A TUPLE rather than a mapping, so nothing keys on something a user can rename.
    """

    applied: tuple[AppliedEntry, ...] = ()

    @classmethod
    def of(cls, records: Iterable[AppliedEntry]) -> AppliedLedger:
        return cls(tuple(sorted(records, key=lambda held: held.entry_id)))

    def has(self, entry_id: str) -> bool:
        return any(entry.entry_id == entry_id for entry in self.applied)

    def entry_ids(self) -> frozenset[str]:
        return frozenset(entry.entry_id for entry in self.applied)

    def with_applied(self, entry: AppliedEntry) -> AppliedLedger:
        """This ledger plus ``entry``, replacing any record with the same id."""
        kept = tuple(held for held in self.applied if held.entry_id != entry.entry_id)
        return AppliedLedger.of((*kept, entry))


#: What an absent file resolves to: "nothing applied yet" is an answer.
EMPTY = AppliedLedger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory.

    COUPLED there, so a restore rolls it back with the memberships it records; a
    path composed here would be a state file nothing snapshots.
    """
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """The sibling lock, in the declared never-restored lock directory."""
    return lock_for(cfg, STATE_KEY)


def read(cfg: config.Config) -> AppliedLedger:
    """The effective ledger for this library. An absent file is the empty one.

    A journal (schema 2, U254) or the whole document every earlier build wrote
    (schema 1), read by the rules it always was. A read never writes; the next
    mark turns a document into a journal.
    """
    return _load(path_for(cfg))[0]


_refused = AppliedLedgerUnreadable.at


def _load(path: Path) -> tuple[AppliedLedger, bool]:
    """The ledger at ``path``, and whether a mark may append to the file as it is.

    Only a journal of this schema whose last line is whole is appendable; a
    record appended after torn bytes would bury them mid file, where they refuse.
    """
    raw = read_raw(path, _refused)
    if raw is None:
        return EMPTY, False
    if _is_journal(raw):
        return _read_journal(raw, path)
    return _read_document(raw, path), False


def _record_from(entry: object, *, path: Path, where: str) -> AppliedEntry:
    """One record, recognised field by field, or the refusal that names it.

    The ONE set of rules, shared by both shapes on disk and by the mark, so a
    record this module writes is a record it reads.
    """
    if not isinstance(entry, dict):
        raise _refused(
            path,
            f"{where} that is a {type(entry).__name__} rather than an object",
        )
    for name in ("entry", "tree", "content", "actor"):
        if not isinstance(entry.get(name), str) or not entry[name]:
            raise _refused(
                path,
                f"{where} with no {name}; a record that cannot say what it "
                f"applied, or who approved it, is worse than no record because it "
                f"still suppresses the work",
            )
    return AppliedEntry(**{name: str(entry.get(key) or "") for name, key in _KEYS})


def _read_document(raw: bytes, path: Path) -> AppliedLedger:
    """A schema 1 ledger, the whole document every build before U254 wrote."""
    data, version = read_document(
        raw, path, _refused, noun="an adoption ledger", schema_version=SCHEMA_VERSION
    )
    if version > DOCUMENT_SCHEMA_VERSION:
        raise _refused(
            path,
            f"is a whole document at schema version {version}, and from version "
            f"{SCHEMA_VERSION} on no build wrote the ledger as one",
        )
    entries = data.get("applied")
    if not isinstance(entries, list):
        raise _refused(
            path, f"has no applied array; its records are a {type(entries).__name__}"
        )

    records: list[AppliedEntry] = []
    seen: set[str] = set()
    for position, entry in enumerate(entries):
        record = _record_from(
            entry, path=path, where=f"holds a record at position {position}"
        )
        if record.entry_id in seen:
            raise _refused(
                path,
                f"holds two records for the entry {record.entry_id!r}; a ledger "
                f"that gives two answers for one piece of work cannot say who "
                f"applied it, and resolving that by line order picks an actor",
            )
        seen.add(record.entry_id)
        records.append(record)
    return AppliedLedger.of(records)


def _is_journal(raw: bytes) -> bool:
    """A journal says so on its first line; a document never has that line.

    A journal whose header is damaged therefore reads as a document, which
    refuses it as not JSON: refused either way, never read as empty.
    """
    try:
        header = json.loads(raw.split(b"\n", 1)[0].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return isinstance(header, dict) and header.get("format") == JOURNAL_FORMAT


def _read_journal(raw: bytes, path: Path) -> tuple[AppliedLedger, bool]:
    """A schema 2 ledger: a header line, then one record per line.

    ONLY THE LAST LINE MAY BE TORN: a mark is appended and synced whole under the
    lock before the next entry, so damage anywhere else refuses. A torn last line
    (unterminated, or not JSON) is the mark that did not finish and reads as NOT
    APPLIED; a last line that is a JSON object failing the record rules was
    written whole and refuses. A RE-MARK REPLACES: the later record stands.
    """
    lines = raw.split(b"\n")
    if len(lines) < 2:
        raise _refused(path, "holds a journal header with no line ending after it")
    header = json.loads(lines[0].decode("utf-8"))
    version = header.get("schema_version")
    if not isinstance(version, int):
        raise _refused(
            path,
            "carries no integer schema_version in its journal header, so nothing "
            "can be said about the shape of what follows it",
        )
    if version > SCHEMA_VERSION:
        raise _refused(
            path,
            f"was written at schema version {version}; this build understands "
            f"{SCHEMA_VERSION}",
            Remedy.UPGRADE_CRATEKIT,
        )
    if version != SCHEMA_VERSION:
        raise _refused(
            path,
            f"carries a journal header at schema version {version}, and no build "
            f"ever wrote a journal before version {SCHEMA_VERSION}",
        )

    body, tail = lines[1:-1], lines[-1]
    whole = not tail
    folded: dict[str, AppliedEntry] = {}
    for index, line in enumerate(body):
        position = index + 1
        try:
            parsed = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            if index == len(body) - 1 and whole:
                whole = False
                break
            raise _refused(
                path,
                f"holds a line, line {position + 1}, that is not readable as "
                f"JSON, and only the last line of a journal can be torn: {exc}",
            ) from exc
        record = _record_from(
            parsed, path=path, where=f"holds a record on line {position + 1}"
        )
        folded[record.entry_id] = record
    return AppliedLedger.of(folded.values()), whole


def _line(payload: Mapping[str, Any]) -> bytes:
    """One JSON object on one line. ``json.dumps`` escapes every newline inside it."""
    return json.dumps(payload, sort_keys=True).encode("utf-8") + b"\n"


def write(cfg: config.Config, ledger: AppliedLedger) -> Path:
    """Persist ``ledger`` whole as a journal, atomically and owner only.

    Only to create the file, to turn a document into a journal, and to cut a
    torn last record away; every other mark appends.
    """
    path = path_for(cfg)
    config.atomic_write_bytes(
        _line({"format": JOURNAL_FORMAT, "schema_version": SCHEMA_VERSION})
        + b"".join(_line(entry.to_json()) for entry in AppliedLedger.of(ledger.applied).applied),
        path,
    )
    return path


#: What this process last left at each ledger path, as ``os.stat`` reports it.
#: A file still exactly as this process left it (device, inode, size and time)
#: holds what this process validated and appended under the lock, so a mark
#: skips reading it. Anything else is read whole and validated first.
_LEFT: dict[str, tuple[int, int, int, int]] = {}


def _as_left(path: Path) -> tuple[int, int, int, int] | None:
    try:
        found = os.stat(path)
    except OSError:
        return None
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)


def mark_applied(cfg: config.Config, entry: AppliedEntry) -> Path:
    """Record that one entry landed: one synced line appended, UNDER THE LOCK.

    APPENDED, since U254: rewriting the whole ledger per mark wrote about N
    squared records. The file is rewritten whole only to create it, to turn an
    older document into a journal, or to cut a torn last record away, always
    from the file as read under the lock, since more than one plan accumulates
    in one ledger. The lock covers the read, the choice and the write: a dropped
    record re-applies a membership and re-writes a tag. The record is validated
    by the reader's rules first, so no later read refuses it. Returns the path.
    """
    path = path_for(cfg)
    line = _line(entry.to_json())
    _record_from(
        entry.to_json(),
        path=path,
        where=f"was refused a record for the entry {entry.entry_id!r}, one",
    )
    key = str(path)
    with config.exclusive_lock(lock_path(cfg)):
        known = _LEFT.pop(key, None)
        if known is not None and known == _as_left(path):
            config.append_durable_bytes(line, path)
        else:
            ledger, appendable = _load(path)
            if appendable:
                config.append_durable_bytes(line, path)
            else:
                write(cfg, ledger.with_applied(entry))
        left = _as_left(path)
        if left is not None:
            _LEFT[key] = left
    return path


def outstanding(plan: AdoptionPlan, ledger: AppliedLedger) -> tuple[PlanEntry, ...]:
    """The plan's applicable entries that have not landed, in plan order.

    DERIVED from the two records rather than stored, so a crash cannot leave a
    count disagreeing with the rows it counts.
    """
    done = ledger.entry_ids()
    return tuple(entry for entry in plan.applicable() if entry.entry_id not in done)


def membership_plan(
    entries: Sequence[PlanEntry], declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The mapping both tree writers take: (folder, sub) to the rows going in it.

    The display names are resolved HERE, at write time, from the active taxonomy
    and never stored (R19, D5), so a folder renamed between the plan and the
    apply orphans nothing; through :func:`cratekit.write.routing_pass.destination`
    so there is one resolution. An entry whose destination is no longer declared
    is SKIPPED rather than costing every other entry (U19).
    """
    grouped: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        try:
            folder, sub = destination(declared, entry.bucket, entry.sub)
        except KeyError:
            continue
        grouped.setdefault((folder, sub), []).append(entry.content_id)
    return grouped


@dataclass(frozen=True, slots=True)
class ApplyReport:
    """What one apply landed, what it skipped, and where a resume starts.

    ``resumed_at`` is the ORDINAL of the first entry this run had work for,
    derived from the outstanding set. Every outstanding entry is attempted, so
    ``applied`` plus ``failed`` accounts for all of them; there is no "stopped
    here" field because the loop never stops.
    """

    tree: str
    actor: str
    digest: str
    applied: tuple[str, ...] = ()
    already_applied: tuple[str, ...] = ()
    failed: Mapping[str, str] = field(default_factory=dict)
    resumed_at: int | None = None

    def __len__(self) -> int:
        return len(self.applied)


def apply_plan(
    cfg: config.Config,
    plan: AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    approval: object,
    place: Callable[[PlanEntry, str, str], None],
    tag_value: Callable[[PlanEntry, taxonomy.Taxonomy], str | None] | None = None,
    now: datetime | None = None,
) -> ApplyReport:
    """Apply an approved plan, one entry at a time, resuming where it left off.

    ``place`` writes ONE entry's membership with the display names resolved here,
    per entry so the ledger record follows the write it describes. A
    ``CratekitError`` from it FAILS THAT ENTRY AND NOTHING ELSE, its scope not
    consulted; a refusal that condemns the run costs time and no file write.

    ``tag_value`` says what, if anything, to write onto the file; None writes no
    tag, and there is no default that writes, because a tag write is the one act
    no restore undoes.

    THE APPROVAL IS CHECKED FIRST, against the plan in hand (R34), so a refused
    apply leaves the disk as it found it. The destructive-session boundary and
    the library lock are the caller's (R29, R31); the tag write runs outside
    them, which is the residual "adoption's tag write takes no destructive
    session and no library lock", owed by the apply command line in
    ``tests/_pending.py``.
    """
    granted = require_approval(plan, approval)
    ledger = read(cfg)
    pending = outstanding(plan, ledger)
    done = ledger.entry_ids()
    already = tuple(
        entry.entry_id for entry in plan.applicable() if entry.entry_id in done
    )
    report_resumed = pending[0].ordinal if pending else None

    applied: list[str] = []
    failed: dict[str, str] = {}
    for entry in pending:
        try:
            folder, sub = destination(declared, entry.bucket, entry.sub)
        except KeyError as exc:
            # PER ENTRY, never out of the run. See ``membership_plan``.
            failed[entry.entry_id] = str(exc)
            continue

        wanted = None if tag_value is None else tag_value(entry, declared)
        target = Path(entry.path) if entry.path else None
        if wanted is not None and target is not None:
            try:
                # ASKED BEFORE ANYTHING HAPPENS FOR THIS ENTRY, membership included:
                # raised from ``write_tags`` it ended the run, and asked after
                # ``place`` it left a placed entry that could never reach applied.
                tags.dialect_of(target.suffix.lower())
            except tags.UnsupportedContainer as exc:
                failed[entry.entry_id] = str(exc)
                continue

        # THE RECOVERABLE WRITE GOES FIRST, and a refusal here costs exactly this
        # entry whatever it condemns; the order is what makes it cost no file.
        try:
            place(entry, folder, sub)
        except CratekitError as exc:
            failed[entry.entry_id] = exc.cause.message
            continue

        if wanted is not None and target is not None:
            # THE ORIGINAL AND THE WRITE ARE ONE ACT, and a file that cannot be
            # identified (gone since the census) costs exactly this entry.
            try:
                _record, landed = revert.write_tag_with_record(
                    cfg,
                    target,
                    field=ADOPTED_TAG_FIELD,
                    written=wanted,
                    entry_id=entry.entry_id,
                    now=now,
                )
            except revert.AdoptedFileUnidentifiable as exc:
                failed[entry.entry_id] = exc.cause.message
                continue
            if not landed:
                failed[entry.entry_id] = "the container refused the tag write"
                continue
        # MARKED ONLY AFTER THE WRITE: a mark first would suppress work the
        # library never received, the one direction a re-run cannot recover (U19).
        mark_applied(
            cfg,
            AppliedEntry(
                entry_id=entry.entry_id,
                tree=entry.tree,
                content_id=entry.content_id,
                bucket=entry.bucket,
                sub=entry.sub,
                actor=granted.actor,
                digest=granted.digest,
                applied=timestamp(now),
            ),
        )
        applied.append(entry.entry_id)
    return ApplyReport(
        tree=plan.tree,
        actor=granted.actor,
        digest=granted.digest,
        applied=tuple(applied),
        already_applied=already,
        failed=failed,
        resumed_at=report_resumed,
    )


__all__ = [
    "ADOPTED_TAG_FIELD",
    "EMPTY",
    "JOURNAL_FORMAT",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "DOCUMENT_SCHEMA_VERSION",
    "AppliedEntry",
    "AppliedLedger",
    "AppliedLedgerUnreadable",
    "ApplyReport",
    "apply_plan",
    "lock_path",
    "mark_applied",
    "membership_plan",
    "outstanding",
    "path_for",
    "read",
    "write",
]
