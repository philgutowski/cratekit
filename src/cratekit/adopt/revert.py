"""The revert ledger: what each file's tag held before adoption overwrote it.

WHY THIS EXISTS AT ALL, in one sentence from the brief: a tag write is the one
operation the XML re-import safety net never covered. Everything else adoption
does lands in the rekordbox database, and a database is snapshotted before every
write session and restorable afterwards (KTD21b, R30). A genre string written
into a file on disk is outside all of that. Re-importing an export does not put
it back, restoring the database does not put it back, and the value it replaced
is gone the instant the write returns.

So the original is written down BEFORE the file is touched, and the order is the
whole of the design. Recording after the write is the shape that looks identical
and loses data: a crash in the window leaves a file carrying the new value and no
record of the old one, which is unrecoverable by any means this product has. A
record for a write that then did not happen costs nothing, because reverting it
restores the value the file already holds.

WHAT MAKES THE RECORD SURVIVE. Two properties, and both are learned rather than
designed.

**The whole read-modify-write cycle is under a lock.**
:func:`cratekit.core.config.atomic_write_bytes` makes the RENAME atomic and does
nothing for the cycle around it. Two processes both read the same document, both
add their record, and the second rename discards the first while the call that
lost returns a record reporting success. That exact shape was shipped twice in
this repository, in the decision stores and in the routing ledger, and eight real
processes recording two hundred decisions left seventy one on the disk. It is
worse here than in either of those: a dropped decline is a question asked twice,
and a dropped revert record is a user's file permanently altered with no record
of what it said.

**A record is written once and never refreshed.** Recording the same field for
the same file twice keeps the FIRST value. The second call happens on a re-run
after a crash, and by then the file already carries the value adoption wrote, so
refreshing the record would overwrite the original with the replacement and the
ledger would faithfully restore the thing it was supposed to undo. What DOES
accumulate is the list of plan entries that wrote through the record, because a
targeted revert has to be answerable and the file's original is the same original
whichever entry asked for the write.

**What is recorded is the file's values EXACTLY.** Through
:func:`cratekit.core.tags.read_tag_values` rather than its convenient sibling.
The convenient reader strips whitespace, reports an empty value as absent, and
returns the first of several values, and every one of those is a difference this
ledger exists to preserve: a stripped original comes back stripped, an original
this ledger recorded as absent comes back DELETED because the writer takes the
absent branch, and a second value comes back not at all. A lossy record is worse
than no record, because it reports the file restored.

**The record and the write it describes are ONE critical section.** Taking the
lock for the record alone leaves a window: a revert issued between the record
landing and the tag write landing restores the file, empties the ledger, and then
the write puts adoption's value on a file with nothing behind it. The original is
gone and both reports read clean. So :func:`write_tag_with_record` holds the lock
across both, and :func:`revert_tags` holds the same lock across its whole pass.
Two applies still serialize into first-write-wins, which is the property that was
already true and is not weakened by the write moving inside the lock.

**A record says what the file looked like when adoption left it.** Size and
modification time, stamped after the write, and consulted only AFTER the field's
own value has failed to settle the question. Without any of it the revert writes
the recorded original onto whatever is at that path now, which after somebody
replaced the file is a stranger's audio getting a genre it never had. Without the
field check first, three ordinary libraries are refused forever; see
:func:`_changed_since_adoption`.

**THE LOCK IS NOT REENTRANT, AND TWO PUBLIC PARAMETERS CAN REACH IT.** ``flock``
is held per open file description, so a second acquisition from the same process
on a new descriptor blocks against the first and never returns. Nothing this
package ships does that. What can is a caller's own ``restore`` handed to
:func:`revert_tags`, or a caller's own ``write_field`` handed to
:func:`write_tag_with_record`: both run INSIDE the lock, so either of them
calling back into any function in this module that takes it deadlocks
permanently rather than raising. It is written down rather than defended against
because every defence costs more than it buys. A timeout turns a programming
error into a partial revert, which is the outcome this module exists to prevent,
and a reentrancy count would make a nested caller believe it holds exclusivity it
does not. Both callbacks exist to be pure: read a file, write a file, return a
boolean.

**The reader refuses everything it cannot recognize, positively, field by
field.** Catching only ``json.loads`` raising leaves a top-level list, a scalar,
a null records field, and a document from a newer build all reading as an empty
ledger, and the next write then destroys it. An empty revert ledger says "nothing
can be undone", which about a file somebody's tag write already changed is a
false statement with no way to notice it.

Layer: modules.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping

from cratekit.cli.output import timestamp
from cratekit.core import config, locations, tags
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy

#: The state entry this module owns. Named once, so the resolver and every
#: caller cannot disagree about which file is meant.
STATE_KEY = "adoption_tag_revert_log"

#: The declared directory the sibling locks live in, shared with the applied
#: ledger. A directory rather than an entry per document, so a third adoption
#: document cannot arrive without a lock.
LOCK_KEY = "adoption_locks"

#: Bumped only when the on-disk shape changes incompatibly. A document written by
#: a newer build is refused rather than guessed at: what is at stake is the only
#: surviving copy of values that are no longer in the files.
SCHEMA_VERSION = 1


class RevertLedgerUnreadable(CratekitError):
    """The revert ledger exists and cannot be understood.

    Deliberately NOT collapsed into "no records". An empty ledger reads as
    "nothing was overwritten", which is the one misreading that turns a
    recoverable tag write into a permanent one, and it is the reading a caller
    reaches for by default. One slug covers every way the file can be wrong and
    the REMEDY is what differs, exactly as the config, routing and registry
    readers already work: a document from a newer build asks for an upgrade and a
    corrupt one asks for the doctor.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="adoption-ledger-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("adopt",),
                detail={"path": str(path), "document": STATE_KEY},
            )
        )
        self.path = path
        self.remedy = remedy


def file_id(path: str) -> str:
    """The stable identifier for one file on disk.

    A digest of the DECODED, composition-normalized path, which is the primitive
    U31 owns and the reason it exists: the same accented filename arrives in two
    different codepoint sequences depending on who produced the string, and a
    ledger keyed on the raw text holds two records for one file. Here that would
    mean a revert that restored one of them and left the other, with the report
    saying both were done.
    """
    return hashlib.sha256(
        locations.location_to_path(str(path)).encode("utf-8")
    ).hexdigest()[:24]


@dataclass(frozen=True, slots=True)
class TagSnapshot:
    """One file's values for one tag field, as they were before adoption wrote.

    ``original`` of None means the field was ABSENT, which is different from the
    field holding an empty string, and the difference is not academic: reverting
    an absent field by writing an empty string leaves a tag on the file that was
    never there. :func:`restore_tag` is told which of the two it is.

    ``original`` is a TUPLE rather than one string, because a tag field can hold
    more than one value and recording the first of them destroys the rest with no
    record that there were any. ``("House", "Techno")`` and ``("House",)`` are
    different files, and only one of them is what the user had.

    ``entry_id`` is the plan entry that CREATED this record and ``entries`` is
    every plan entry that has written through it since. The first is history and
    the second is what a targeted revert matches on: a second adoption of an
    already-adopted file correctly keeps the first record, so a revert asking for
    the second entry would otherwise match nothing and report a clean pass over a
    file it left holding adoption's value.

    ``size`` and ``mtime_ns`` are the file as adoption LEFT it, stamped after the
    write rather than before it, so a later revert can tell its own handiwork
    from a file somebody has since replaced. Both are None on a record whose
    write did not complete, which is the crash seam and is treated as
    unverifiable rather than as a mismatch.
    """

    file: str
    field: str
    path: str
    original: tuple[str, ...] | None
    written: str
    recorded: str
    entry_id: str = ""
    entries: tuple[str, ...] = ()
    size: int | None = None
    mtime_ns: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "file": self.file,
            "field": self.field,
            "path": self.path,
            "original": None if self.original is None else list(self.original),
            "written": self.written,
            "recorded": self.recorded,
            "entry": self.entry_id,
            "entries": list(self.entries),
            "size": self.size,
            "mtime_ns": self.mtime_ns,
        }

    def written_by(self, entry_id: str) -> bool:
        """Whether ``entry_id``'s write went through this record."""
        return entry_id in (self.entries or ((self.entry_id,) if self.entry_id else ()))


def _key(snapshot: TagSnapshot) -> tuple[str, str]:
    """What identifies one record: the FILE and the FIELD, never the file alone.

    Adoption may write more than one field to one file, and a ledger keyed on the
    file alone would let the second write's record replace the first's. The
    revert would then restore one field and silently keep the other's new value,
    while reporting the file restored.
    """
    return (snapshot.file, snapshot.field)


@dataclass(frozen=True, slots=True)
class RevertLedger:
    """Every tag value adoption has overwritten in this library.

    Records are a TUPLE rather than a mapping, for the reason the tree registry
    and the routing ledger both give: it keeps the identifier out of every key
    position, so nothing is tempted to key it on something a user can rename.
    """

    snapshots: tuple[TagSnapshot, ...] = ()

    def snapshot(self, file: str, field: str) -> TagSnapshot | None:
        for entry in self.snapshots:
            if entry.file == file and entry.field == field:
                return entry
        return None

    def with_snapshot(self, snapshot: TagSnapshot) -> RevertLedger:
        """This ledger plus ``snapshot``, KEEPING any record already there.

        First write wins, and that is the opposite of every other ``with_``
        helper in this repository. See the module docstring: the second call
        happens on a re-run after a crash, by which time the file holds what
        adoption wrote, so replacing would record the replacement as the
        original.
        """
        if self.snapshot(snapshot.file, snapshot.field) is not None:
            return self
        return RevertLedger(
            tuple(sorted((*self.snapshots, snapshot), key=_key))
        )

    def replacing(self, snapshot: TagSnapshot) -> RevertLedger:
        """This ledger with ``snapshot`` substituted for the record it keys to.

        THE ONLY LEGITIMATE USE IS AMENDING A RECORD WITHOUT TOUCHING ITS
        ``original``, which is what appending a plan entry and stamping the file
        after the write both are. It is deliberately not the ordinary way in;
        :meth:`with_snapshot` is, and it keeps the first record precisely so the
        original cannot be replaced by what adoption wrote over it.
        """
        kept = tuple(
            held for held in self.snapshots if _key(held) != _key(snapshot)
        )
        return RevertLedger(tuple(sorted((*kept, snapshot), key=_key)))

    def without(self, keys: frozenset[tuple[str, str]]) -> RevertLedger:
        """This ledger minus the records named, for use after a revert lands."""
        return RevertLedger(
            tuple(entry for entry in self.snapshots if _key(entry) not in keys)
        )


#: What an absent file resolves to. Named, because "nothing has been overwritten"
#: is a real answer rather than a missing one.
EMPTY = RevertLedger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory."""
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """The sibling lock, in the declared never-restored lock directory.

    Not beside the document. The lock directory is its own state entry with its
    own snapshot role for the inode reason every lock in this product shares: a
    restore that replaced the directory holding a lock would swap the inode a
    live advisory lock is held on, and both holders would go on believing they
    had exclusive access.
    """
    return config.state_path(LOCK_KEY, cfg) / f"{STATE_KEY}.lock"


def _original_values(
    original: Any, *, path: Path, position: int
) -> tuple[str, ...] | None:
    """The recorded original, recognized positively in both shapes it takes.

    A LIST is what this build writes, because a tag field holds a list of values.
    A BARE STRING is accepted as the one-value case rather than refused, so a
    document written before the ledger learned to count values still restores
    what it recorded instead of refusing to restore anything. Null is the field
    having been absent. Everything else is a document this build did not write.
    """
    if original is None:
        return None
    if isinstance(original, str):
        return (original,)
    if isinstance(original, list) and all(isinstance(v, str) for v in original):
        return tuple(original)
    raise RevertLedgerUnreadable(
        f"{path} holds a record at position {position} whose original value is a "
        f"{type(original).__name__} rather than the field's values",
        path=path,
        remedy=Remedy.RUN_DOCTOR,
    )


def _entry_list(entry: dict, *, path: Path, position: int) -> tuple[str, ...]:
    """Every plan entry that wrote through this record.

    A record with no list falls back to the entry that created it, so a targeted
    revert against an older document matches exactly what it used to match.
    """
    found = entry.get("entries")
    if found is None:
        created = str(entry.get("entry") or "")
        return (created,) if created else ()
    if not isinstance(found, list) or not all(isinstance(v, str) for v in found):
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} whose entry list is a "
            f"{type(found).__name__}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    return tuple(found)


def _optional_int(entry: dict, name: str, *, path: Path, position: int) -> int | None:
    """One of the after-the-write stamps. Absent and null both mean unstamped."""
    found = entry.get(name)
    if found is None:
        return None
    if isinstance(found, bool) or not isinstance(found, int):
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} whose {name} is a "
            f"{type(found).__name__} rather than a number",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    return found


def read(cfg: config.Config) -> RevertLedger:
    """The effective ledger for this library. An absent file is the empty one.

    Every branch below is a POSITIVE recognition of a field rather than a guess
    at what a wrong one might do. That is the fix for the shape U11 shipped: a
    reader catching only a parse error treats a top-level list, a scalar, a null
    records field, and a document from another build as an empty store, and the
    next write then destroys the file.
    """
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise RevertLedgerUnreadable(
            f"{path} exists and could not be read: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RevertLedgerUnreadable(
            f"{path} is not readable as JSON: {exc}", path=path, remedy=Remedy.RUN_DOCTOR
        ) from exc
    if not isinstance(data, dict):
        raise RevertLedgerUnreadable(
            f"{path} holds a {type(data).__name__} at its top level rather than a "
            f"revert ledger",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    version = data.get("schema_version")
    if not isinstance(version, int):
        raise RevertLedgerUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if version > SCHEMA_VERSION:
        raise RevertLedgerUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )
    entries = data.get("snapshots")
    if not isinstance(entries, list):
        raise RevertLedgerUnreadable(
            f"{path} has no snapshots array; its records are a "
            f"{type(entries).__name__}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    records: list[TagSnapshot] = []
    seen: set[tuple[str, str]] = set()
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RevertLedgerUnreadable(
                f"{path} holds a record at position {position} that is a "
                f"{type(entry).__name__} rather than an object",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        for name in ("file", "field", "path", "written"):
            if not isinstance(entry.get(name), str) or not entry[name]:
                raise RevertLedgerUnreadable(
                    f"{path} holds a record at position {position} with no "
                    f"{name}; a record that cannot say which file and field it "
                    f"describes cannot restore anything",
                    path=path,
                    remedy=Remedy.RUN_DOCTOR,
                )
        if "original" not in entry:
            # THE ONE BRANCH THAT IS NOT A POSITIVE RECOGNITION IF IT IS LEFT
            # OUT. ``get`` answers None for a key that is absent and for a key
            # explicitly set to null, and here those are different facts: null
            # means "the field was absent, restore it by deleting", and a missing
            # key means the record never said. Reading the second as the first
            # deletes a field nobody recorded anything about.
            raise RevertLedgerUnreadable(
                f"{path} holds a record at position {position} with no original "
                f"key at all; absence of a fact and absence AS a fact are "
                f"different, and reading the first as the second reverts by "
                f"deleting a field this ledger never saw",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        original = _original_values(entry["original"], path=path, position=position)
        record = TagSnapshot(
            file=str(entry["file"]),
            field=str(entry["field"]),
            path=str(entry["path"]),
            original=original,
            written=str(entry["written"]),
            recorded=str(entry.get("recorded") or ""),
            entry_id=str(entry.get("entry") or ""),
            entries=_entry_list(entry, path=path, position=position),
            size=_optional_int(entry, "size", path=path, position=position),
            mtime_ns=_optional_int(entry, "mtime_ns", path=path, position=position),
        )
        if _key(record) in seen:
            raise RevertLedgerUnreadable(
                f"{path} holds two records for {record.field!r} on one file; a "
                f"ledger that gives two answers for one field cannot say which "
                f"value to restore, and resolving that by line order decides "
                f"what a user's file ends up holding",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(_key(record))
        records.append(record)
    return RevertLedger(tuple(sorted(records, key=_key)))


def write(cfg: config.Config, ledger: RevertLedger) -> Path:
    """Persist ``ledger`` atomically and owner only, through the shared writer."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        # Sorted so the bytes are a function of the content alone.
        "snapshots": [entry.to_json() for entry in sorted(ledger.snapshots, key=_key)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def _record_locked(
    cfg: config.Config,
    resolved: Path,
    *,
    field: str,
    written: str,
    entry_id: str,
    now: datetime | None,
    read_field: Callable[[Path, str], tuple[str, ...] | None],
) -> tuple[RevertLedger, TagSnapshot]:
    """The record half, assuming the caller already holds the lock."""
    ledger = read(cfg)
    identifier = file_id(str(resolved))
    existing = ledger.snapshot(identifier, field)
    if existing is None:
        record = TagSnapshot(
            file=identifier,
            field=field,
            path=str(resolved),
            original=read_field(resolved, field),
            written=written,
            recorded=timestamp(now),
            entry_id=entry_id,
            entries=(entry_id,) if entry_id else (),
        )
        ledger = ledger.with_snapshot(record)
        write(cfg, ledger)
        return ledger, record
    # THE ORIGINAL IS NEVER TOUCHED HERE. Only the list of entries that have
    # written through this record grows, and only when this entry is new to it.
    if not entry_id or existing.written_by(entry_id):
        return ledger, existing
    amended = replace(existing, entries=(*existing.entries, entry_id))
    ledger = ledger.replacing(amended)
    write(cfg, ledger)
    return ledger, amended


def _stamped(record: TagSnapshot, path: Path) -> TagSnapshot:
    """``record`` carrying the file as adoption has just left it."""
    try:
        info = path.stat()
    except OSError:  # pragma: no cover - the write above already succeeded
        return record
    return replace(record, size=info.st_size, mtime_ns=info.st_mtime_ns)


def _write_one(path: Path, field: str, value: str) -> bool:
    """The default write: one value into one field, through the one writer."""
    return tags.write_tags(path, {field: value})


def snapshot_before_write(
    cfg: config.Config,
    path: Path | str,
    *,
    field: str,
    written: str,
    entry_id: str = "",
    now: datetime | None = None,
    read_field: Callable[[Path, str], tuple[str, ...] | None] = tags.read_tag_values,
) -> TagSnapshot:
    """Record what the file holds now, BEFORE anything writes over it.

    Returns the record that is in the ledger for this file and field, which after
    a re-run is the one the FIRST attempt wrote. A caller that used the return
    value to decide what to restore therefore gets the original in both cases.

    THE WHOLE CYCLE IS UNDER THE LOCK, read included. The read decides what the
    write contains, so a lock around only the write protects nothing: the losing
    process still writes a set it read before the winner's record existed.

    THIS IS THE RECORD HALF ONLY, and a caller that goes on to write the tag
    itself has a window nothing covers: a revert landing between this call
    returning and that write landing takes the record away, and the write then
    puts adoption's value on a file with no original behind it. Use
    :func:`write_tag_with_record` for that, which is the same record under a lock
    that is still held when the write happens.
    """
    resolved = Path(path)
    with config._exclusive_lock(lock_path(cfg)):
        _ledger, record = _record_locked(
            cfg,
            resolved,
            field=field,
            written=written,
            entry_id=entry_id,
            now=now,
            read_field=read_field,
        )
        return record


def write_tag_with_record(
    cfg: config.Config,
    path: Path | str,
    *,
    field: str,
    written: str,
    entry_id: str = "",
    now: datetime | None = None,
    read_field: Callable[[Path, str], tuple[str, ...] | None] = tags.read_tag_values,
    write_field: Callable[[Path, str, str], bool] = _write_one,
) -> tuple[TagSnapshot, bool]:
    """Record the original and write the new value, as ONE indivisible act.

    Returns the record that now stands behind the file and whether the write
    landed.

    WHY THE WRITE IS INSIDE THE LOCK RATHER THAN AFTER IT. The ledger's lock used
    to cover each document's read-modify-write and nothing about the order of an
    apply against a revert. That left a window one instruction wide in the shape
    that matters: a revert issued while an apply is in flight reads the record,
    restores the file, and empties the ledger, and the apply's write then lands on
    a file with no record behind it. The original is permanently gone and both
    reports say the run was clean. Nothing about the ordering inside either
    function fixes that; only holding one lock across both halves does.

    WHAT THIS COSTS AND WHAT IT DOES NOT. Two applies now serialize on the tag
    write as well as on the record. They already serialized on the record, and
    the property that mattered there is untouched: the first run's record wins,
    the second finds it and keeps it, and the original survives both. What is
    bought is that a revert can no longer interleave with either of them.

    THE STAMP GOES ON AFTER THE WRITE, not before. What a later revert needs to
    know is whether the file is still the one adoption wrote to, so the size and
    time it compares against have to be adoption's own output. A crash between
    the write and the stamp leaves the record unstamped, which reverts without
    the check rather than refusing, because the alternative is a record that can
    never be spent.

    ``write_field`` RUNS INSIDE THE LOCK and must not take it again. See the
    module docstring: ``flock`` is per open file description, so a callback that
    reaches back into this module hangs forever rather than raising.
    """
    resolved = Path(path)
    with config._exclusive_lock(lock_path(cfg)):
        ledger, record = _record_locked(
            cfg,
            resolved,
            field=field,
            written=written,
            entry_id=entry_id,
            now=now,
            read_field=read_field,
        )
        landed = write_field(resolved, field, written)
        if landed:
            stamped = _stamped(record, resolved)
            if stamped != record:
                write(cfg, ledger.replacing(stamped))
                record = stamped
        return record, landed


@dataclass(frozen=True, slots=True)
class RevertReport:
    """What a revert put back, and what it could not.

    KEYED ON THE FILE AND THE FIELD, never on the file alone, for the same reason
    the ledger itself is (:func:`_key`). Adoption may write more than one field to
    one file, and a report keyed on the path collapses two different failures into
    one reason and lists one path twice among its successes. The ledger stayed
    right through that because it keys correctly; only the thing a person reads
    was lossy, which is the half nobody checks.

    ``failed`` carries one reason per pair rather than a count, because the ways
    this fails have different answers: a file that has since been deleted is not a
    defect, a file somebody replaced is a refusal, and a container this build
    cannot write is a bug.
    """

    restored: tuple[tuple[str, str], ...] = ()
    failed: Mapping[tuple[str, str], str] = field(default_factory=dict)

    def files(self) -> tuple[str, ...]:
        """The distinct paths this revert put back, in order, for a summary."""
        seen: list[str] = []
        for path, _field in self.restored:
            if path not in seen:
                seen.append(path)
        return tuple(seen)


def restore_tag(path: Path, tag_field: str, original: tuple[str, ...] | None) -> bool:
    """Put one field back to exactly what it was, ABSENCE INCLUDED.

    Two calls, because absence is not a value. :func:`cratekit.core.tags.write_tags`
    skips a None on purpose, so handing it ``{field: None}`` writes nothing and
    returns True, which reports a restore that did not happen. Restoring an absent
    field as an empty string is the other wrong answer: it leaves a tag on the
    file that was never there, and "exactly" is what the verification gate asks
    for.

    The present branch goes through :func:`cratekit.core.tags.write_tag_values`
    rather than its convenient sibling, because the record holds every value the
    field had and a writer that takes one string can only put one of them back.

    Both branches go through the module that owns container classification (S5),
    so the deletion and the write cannot disagree about where a field lives.
    """
    if original is None:
        return tags.clear_tags(path, [tag_field])
    return tags.write_tag_values(path, tag_field, original)


def _changed_since_adoption(
    record: TagSnapshot,
    target: Path,
    *,
    read_field: Callable[[Path, str], tuple[str, ...] | None],
) -> str | None:
    """Why this file is not the one adoption wrote to, or None when it is.

    THE FIELD IS ASKED BEFORE THE STAMP IS, and that ordering is the whole of
    this function. Size and modification time are CIRCUMSTANTIAL evidence about
    the file; the field's own value is DIRECT evidence about the thing the record
    describes. A guard that consults only the circumstantial evidence refuses
    three ordinary libraries, all of them measured:

    * A later write of any other field this module owns. Writing an energy
      rating, which is in :data:`cratekit.core.tags.FIELDS` for the analysis
      workflow, moved the size and the time and permanently blocked the adoption
      revert on a file still carrying adoption's own genre.
    * A byte-identical file whose time moved. A backup restore, an rsync without
      timestamps, a cloud re-download. Same bytes, same genre, refused forever.
    * An interrupted revert pass. It restores a file and dies before the ledger
      is rewritten, so on retry that record's stamp no longer matches its own
      successful restore, and it is refused for good while every other record
      settles. The file is correct and the ledger keeps a record nobody can ever
      clear.

    So two positive recognitions come first. The field still holding exactly what
    adoption WROTE is proof this is adoption's own output whatever the stamp
    says. The field already holding the recorded ORIGINAL is proof a restore
    already landed, and doing it again writes the same bytes and lets the record
    settle. Only when neither is true does the stamp decide, and only when the
    stamp is present: an unstamped record can only come from a crash between the
    write and the stamp, and refusing those would leave a record that can never
    be spent on a file that genuinely does carry adoption's value.

    Even then the refusal is EVIDENCE RATHER THAN PERMISSION. See
    :func:`revert_tags`'s ``force``: a person who knows the file is theirs has to
    be able to say so, or a wrong guess here is as unrecoverable as the write it
    was guarding.
    """
    current = read_field(target, record.field)
    if current is not None and tuple(current) == (record.written,):
        return None
    if current == record.original:
        return None
    if record.size is None or record.mtime_ns is None:
        return None
    try:
        info = target.stat()
    except OSError as exc:
        return str(exc)
    if info.st_size == record.size and info.st_mtime_ns == record.mtime_ns:
        return None
    return (
        "the file has changed since adoption wrote it and no longer carries the "
        "value adoption wrote, so the recorded original describes bytes that are "
        "no longer there; restoring it would put one file's tag onto another "
        "file's audio. Revert with force to override this."
    )


def revert_tags(
    cfg: config.Config,
    *,
    entry_id: str | None = None,
    force: bool = False,
    restore: Callable[[Path, str, tuple[str, ...] | None], bool] = restore_tag,
    read_field: Callable[[Path, str], tuple[str, ...] | None] = tags.read_tag_values,
) -> RevertReport:
    """Put every recorded original back on disk, exactly.

    ``entry_id`` of None reverts everything the ledger holds; naming one reverts
    every record that entry's write went through. Matched through
    :meth:`TagSnapshot.written_by` rather than against the record's creator,
    because first-write-wins means a second adoption of a file writes through the
    FIRST record: matching on the creator alone answers "nothing to do" for work
    that demonstrably happened and leaves the file holding adoption's value.

    ``force`` spends a record whose file no longer looks like the one adoption
    wrote to. IT EXISTS BECAUSE THE GUARD IS EVIDENCE AND NOT PERMISSION. The
    check in :func:`_changed_since_adoption` is a heuristic over a file somebody
    else owns, and a heuristic with no override is a heuristic that decides: a
    wrong refusal strands the only copy of a value exactly as surely as a wrong
    restore overwrites one. It is a parameter here rather than something the
    ``restore`` callback could reach, because the check runs BEFORE the callback
    and no callback can therefore see past it.

    THE WHOLE PASS IS UNDER THE LEDGER'S LOCK, which is the same lock
    :func:`write_tag_with_record` holds across a record and its write. That is
    what makes a revert and an apply orderable at all: without it a revert can
    land between an apply's record and its write, and the write then has no
    record behind it.

    A FALSE RETURN IS A FAILURE, and it has to be read rather than assumed. The
    tag writer returns False on any container trouble instead of raising, because
    one awkward file must not abort a batch; a caller that ignored the return
    value would report every file restored whatever happened to it, which is the
    reporting failure this whole ledger exists to avoid one step earlier.

    A RECORD IS DROPPED FROM THE LEDGER ONLY AFTER ITS FILE IS WRITTEN. The
    reverse order loses the record for a write that then failed, which is the same
    data loss the ledger exists to prevent arriving through the undo.

    ``restore`` and ``read_field`` BOTH RUN INSIDE THE LOCK and must not take it
    again. See the module docstring: ``flock`` is per open file description, so a
    callback reaching back into this module hangs forever rather than raising.
    """
    restored: list[tuple[str, str]] = []
    failed: dict[tuple[str, str], str] = {}
    settled: set[tuple[str, str]] = set()
    with config._exclusive_lock(lock_path(cfg)):
        ledger = read(cfg)
        for record in ledger.snapshots:
            if entry_id is not None and not record.written_by(entry_id):
                continue
            reported = (record.path, record.field)
            target = Path(record.path)
            if not target.exists():
                failed[reported] = "the file is no longer there"
                continue
            replaced = (
                None
                if force
                else _changed_since_adoption(record, target, read_field=read_field)
            )
            if replaced is not None:
                failed[reported] = replaced
                continue
            try:
                landed = restore(target, record.field, record.original)
            except (OSError, ValueError, tags.UnsupportedContainer) as exc:
                failed[reported] = str(exc)
                continue
            if not landed:
                failed[reported] = "the container refused the write"
                continue
            restored.append(reported)
            settled.add((record.file, record.field))
        if settled:
            write(cfg, ledger.without(frozenset(settled)))
    return RevertReport(restored=tuple(restored), failed=failed)


__all__ = [
    "EMPTY",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "RevertLedger",
    "RevertLedgerUnreadable",
    "RevertReport",
    "TagSnapshot",
    "file_id",
    "lock_path",
    "path_for",
    "read",
    "restore_tag",
    "revert_tags",
    "snapshot_before_write",
    "write",
    "write_tag_with_record",
]
