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
ledger would faithfully restore the thing it was supposed to undo.

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
from dataclasses import dataclass, field
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
    """One file's value for one tag field, as it was before adoption wrote it.

    ``original`` of None means the field was ABSENT, which is different from the
    field holding an empty string, and the difference is not academic: reverting
    an absent field by writing an empty string leaves a tag on the file that was
    never there. The writer below is told which of the two it is.
    """

    file: str
    field: str
    path: str
    original: str | None
    written: str
    recorded: str
    entry_id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "file": self.file,
            "field": self.field,
            "path": self.path,
            "original": self.original,
            "written": self.written,
            "recorded": self.recorded,
            "entry": self.entry_id,
        }


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
        original = entry.get("original")
        if original is not None and not isinstance(original, str):
            # None is a legitimate value here and means the field was absent.
            # Anything else is a document this build did not write.
            raise RevertLedgerUnreadable(
                f"{path} holds a record at position {position} whose original "
                f"value is a {type(original).__name__}",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        record = TagSnapshot(
            file=str(entry["file"]),
            field=str(entry["field"]),
            path=str(entry["path"]),
            original=original,
            written=str(entry["written"]),
            recorded=str(entry.get("recorded") or ""),
            entry_id=str(entry.get("entry") or ""),
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


def snapshot_before_write(
    cfg: config.Config,
    path: Path | str,
    *,
    field: str,
    written: str,
    entry_id: str = "",
    now: datetime | None = None,
    read_field: Callable[[Path, str], str | None] = tags.read_tag,
) -> TagSnapshot:
    """Record what the file holds now, BEFORE anything writes over it.

    Returns the record that is in the ledger for this file and field, which after
    a re-run is the one the FIRST attempt wrote. A caller that used the return
    value to decide what to restore therefore gets the original in both cases.

    THE WHOLE CYCLE IS UNDER THE LOCK, read included. The read decides what the
    write contains, so a lock around only the write protects nothing: the losing
    process still writes a set it read before the winner's record existed.
    """
    resolved = Path(path)
    with config._exclusive_lock(lock_path(cfg)):
        ledger = read(cfg)
        identifier = file_id(str(resolved))
        existing = ledger.snapshot(identifier, field)
        if existing is not None:
            return existing
        record = TagSnapshot(
            file=identifier,
            field=field,
            path=str(resolved),
            original=read_field(resolved, field),
            written=written,
            recorded=timestamp(now),
            entry_id=entry_id,
        )
        write(cfg, ledger.with_snapshot(record))
        return record


@dataclass(frozen=True, slots=True)
class RevertReport:
    """What a revert put back, and what it could not.

    ``failed`` carries one reason per file rather than a count, because the two
    ways this fails have different answers: a file that has since been deleted is
    not a defect, and a container this build cannot write is.
    """

    restored: tuple[str, ...] = ()
    failed: Mapping[str, str] = field(default_factory=dict)


def restore_tag(path: Path, tag_field: str, original: str | None) -> bool:
    """Put one field back to exactly what it was, ABSENCE INCLUDED.

    Two calls, because absence is not a value. :func:`cratekit.core.tags.write_tags`
    skips a None on purpose, so handing it ``{field: None}`` writes nothing and
    returns True, which reports a restore that did not happen. Restoring an absent
    field as an empty string is the other wrong answer: it leaves a tag on the
    file that was never there, and "exactly" is what the verification gate asks
    for.

    Both branches go through the module that owns container classification (S5),
    so the deletion and the write cannot disagree about where a field lives.
    """
    if original is None:
        return tags.clear_tags(path, [tag_field])
    return tags.write_tags(path, {tag_field: original})


def revert_tags(
    cfg: config.Config,
    *,
    entry_id: str | None = None,
    restore: Callable[[Path, str, str | None], bool] = restore_tag,
) -> RevertReport:
    """Put every recorded original back on disk, exactly.

    ``entry_id`` of None reverts everything the ledger holds; naming one reverts
    only the records that plan entry produced.

    A FALSE RETURN IS A FAILURE, and it has to be read rather than assumed. The
    tag writer returns False on any container trouble instead of raising, because
    one awkward file must not abort a batch; a caller that ignored the return
    value would report every file restored whatever happened to it, which is the
    reporting failure this whole ledger exists to avoid one step earlier.

    A RECORD IS DROPPED FROM THE LEDGER ONLY AFTER ITS FILE IS WRITTEN, and the
    drop happens under the lock in one cycle at the end. The reverse order loses
    the record for a write that then failed, which is the same data loss the
    ledger exists to prevent arriving through the undo.
    """
    ledger = read(cfg)
    restored: list[str] = []
    failed: dict[str, str] = {}
    settled: set[tuple[str, str]] = set()
    for record in ledger.snapshots:
        if entry_id is not None and record.entry_id != entry_id:
            continue
        target = Path(record.path)
        if not target.exists():
            failed[record.path] = "the file is no longer there"
            continue
        try:
            landed = restore(target, record.field, record.original)
        except (OSError, ValueError, tags.UnsupportedContainer) as exc:
            failed[record.path] = str(exc)
            continue
        if not landed:
            failed[record.path] = "the container refused the write"
            continue
        restored.append(record.path)
        settled.add((record.file, record.field))
    if settled:
        with config._exclusive_lock(lock_path(cfg)):
            write(cfg, read(cfg).without(frozenset(settled)))
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
]
