"""The revert ledger's document: its records, its schema, its reader and writer.

The ledger is the only surviving copy of values adoption overwrote in files on
disk, so the reader RECOGNIZES EVERY FIELD POSITIVELY and refuses the rest. A
reader that caught only a parse error read a top-level list, a scalar, a null
records field and a newer build's document as an empty ledger, and the next
write destroyed it; an empty revert ledger says "nothing can be undone", which
is false about a file whose tag was already changed.

The adoption ledger in :mod:`cratekit.adopt.apply` is read by the same rules,
so the shared steps (the read, the JSON header, the refusal) live here.

Layer: modules.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable

from cratekit.core import config, locations
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy

#: The state entry this module owns.
STATE_KEY = "adoption_tag_revert_log"

#: The declared lock directory, shared with the applied ledger, so a third
#: adoption document cannot arrive without a lock.
LOCK_KEY = "adoption_locks"

#: Bumped only when the on-disk shape changes incompatibly. A newer document is
#: refused rather than guessed at.
SCHEMA_VERSION = 1


class LedgerUnreadable(CratekitError):
    """One of adoption's two ledgers exists and cannot be understood.

    One slug covers every way either file can be wrong and the REMEDY is what
    differs. ``document`` is the state key of the ledger a subclass is about.
    """

    document: str

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="adoption-ledger-unusable", message=message,
                remediation=Remediation(remedy=remedy), scope=Scope.RUN, origin=("adopt",),
                detail={"path": str(path), "document": self.document},
            )
        )
        self.path = path
        self.remedy = remedy

    @classmethod
    def at(cls, path: Path, message: str, remedy: Remedy = Remedy.RUN_DOCTOR) -> LedgerUnreadable:
        """The refusal for the document at ``path``, which every message opens with."""
        return cls(f"{path} {message}", path=path, remedy=remedy)


class RevertLedgerUnreadable(LedgerUnreadable):
    """The revert ledger exists and cannot be understood.

    Never collapsed into "no records": an empty ledger reads as "nothing was
    overwritten", which turns a recoverable tag write into a permanent one. A
    newer build's document asks for an upgrade and a corrupt one for the doctor.
    """

    document = STATE_KEY


class AdoptedFileUnidentifiable(CratekitError):
    """The file about to be written to cannot be identified, so nothing is written.

    A tag write with no record behind it is the one operation this product cannot
    undo, so failing to identify the file stops the write. Per FILE, not per run:
    :func:`cratekit.adopt.apply.apply_plan` fails exactly that entry.

    The remedy is a parameter and the slug is not: a file that cannot be stat'd
    may be back in a minute, while a ledger giving two answers will still give
    them in a minute, so telling that person to retry sends them round a loop.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy = Remedy.RETRY_LATER) -> None:
        super().__init__(
            Cause(
                reason="adoption-file-unidentifiable", message=message,
                remediation=Remediation(remedy=remedy), scope=Scope.ITEM, origin=("adopt",),
                detail={"path": str(path)},
            )
        )
        self.path = path


class RecordCannotBeMatched(AdoptedFileUnidentifiable):
    """The ledger's evidence about this file disagrees with itself, so nothing is written.

    A subclass so the one caller that handles the parent, ``apply_plan``, fails
    the entry and goes on; a sibling would escape that ``except`` and end the
    pass. Raised INSTEAD of picking a record: rewriting a record's path to the
    file in hand handed one file's record to another on every volume that
    recycles inode numbers, and the revert then wrote the dead file's original
    onto the live one.
    """

    def __init__(self, message: str, *, path: Path) -> None:
        super().__init__(message, path=path, remedy=Remedy.RUN_DOCTOR)


#: What an identity is a statement ABOUT, spelled into the value so a document
#: cannot be read as the other scheme by accident.
IDENTITY_SCHEME = "dev-ino"

#: The identity this build writes: the volume and the inode, and nothing else.
_INODE_IDENTITY = re.compile(rf"^{IDENTITY_SCHEME}:-?\d+:-?\d+$")

#: The width the PREVIOUS scheme truncated its path digest to. Legacy ledgers are
#: still on disk, so changing it re-keys every legacy record and strands its
#: original.
_LEGACY_ID_WIDTH = 24

_LEGACY_IDENTITY = re.compile(rf"^[0-9a-f]{{{_LEGACY_ID_WIDTH}}}$")


def identity_of(path: Path) -> str:
    """One CLAIM about which file this is: its volume and its inode, right now.

    Not an identity on its own; it is one of the three claims a record carries,
    and :func:`cratekit.adopt.revert._record_for` decides what a record is about.
    The pair is RECYCLED on FAT and exFAT, the format of every rekordbox export
    drive, and MOVES for a file nobody touched (a remount, an ``os.replace``
    save, a mount order change). The path is no identity either: a hardlink, a
    case varying spelling on a case insensitive volume and a rename are one file
    with two paths. Lowercasing the path is not the fix, because case
    sensitivity belongs to the volume.

    RAISES rather than falling back to the path when the file cannot be stat'd,
    so one string never means two different claims.
    """
    try:
        info = path.stat()
    except OSError as exc:
        raise AdoptedFileUnidentifiable(
            f"{path} cannot be identified on this machine: {exc}. Nothing is written to a "
            f"file whose original cannot be recorded first, because a tag write with no "
            f"record behind it is the one thing this product cannot undo",
            path=path,
        ) from exc
    return f"{IDENTITY_SCHEME}:{info.st_dev}:{info.st_ino}"


def _legacy_file_id(path: str) -> str:
    """The identifier the PREVIOUS scheme wrote, only for finding its records.

    So an upgraded run KEEPS the record a legacy ledger holds rather than writing
    a second whose ``original`` is adoption's own value. A digest of the decoded,
    composition-normalized path (U31); never written into a new record.
    """
    named = locations.location_to_path(str(path)).encode("utf-8")
    return hashlib.sha256(named).hexdigest()[:_LEGACY_ID_WIDTH]


def _is_an_identity(value: str) -> bool:
    """Whether ``value`` is an identifier one of the two schemes actually wrote."""
    return bool(_INODE_IDENTITY.match(value) or _LEGACY_IDENTITY.match(value))


class DigestState(StrEnum):
    """What a record is able to say about the bytes adoption left behind.

    Named states rather than an empty string, which stood for both "nothing was
    ever written down" and "the read that should have written it failed".
    Only :attr:`RECORDED` carries evidence and can be compared against a file;
    the other two refuse and name themselves, and ``force`` spends them one
    record at a time.
    """

    #: ``digest`` holds a sha256 of the whole file exactly as adoption left it.
    RECORDED = "recorded"

    #: The stamping read was attempted and failed, after a retry.
    UNREADABLE = "unreadable"

    #: Nothing about the bytes was written down: a write that never reached the
    #: stamp, or a document from a build that had no digest.
    ABSENT = "absent"


#: The states a document may spell, derived from the enum so a fourth state
#: cannot arrive without the reader recognizing it.
_DIGEST_STATES: frozenset[str] = frozenset(str(member) for member in DigestState)


@dataclass(frozen=True, slots=True)
class TagSnapshot:
    """One file's values for one tag field, as they were before adoption wrote.

    ``original`` of None means the field was ABSENT, which is not an empty
    string: restoring absence by writing ``""`` leaves a tag that was never
    there. It is a TUPLE because a field can hold several values.

    ``entry_id`` is the plan entry that CREATED the record and ``entries`` every
    entry that has written through it since; a targeted revert matches on the
    second, because a second adoption keeps the first record.

    The last four fields are the file as adoption LEFT it, stamped after the
    write. Only ``digest`` is about the bytes and only it decides anything:
    ``size`` is a shortcut that cannot change an answer and ``mtime_ns`` is for
    a person reading the ledger. ``digest_state`` says which fact an empty
    digest is. The value in the field (a bucket name shared across the library)
    and the inode (kept by an in-place replacement) are NOT evidence about
    content; ``file`` answers which file a record is about, ``digest`` whether
    its bytes are adoption's.
    """

    #: WHICH FILE, as ``dev-ino:<st_dev>:<st_ino>``, or a legacy path digest.
    #: Never a path.
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
    digest: str = ""
    digest_state: DigestState = DigestState.ABSENT

    def to_json(self) -> dict[str, Any]:
        return {
            "file": self.file, "field": self.field, "path": self.path,
            "original": None if self.original is None else list(self.original),
            "written": self.written, "recorded": self.recorded, "entry": self.entry_id,
            "entries": list(self.entries), "size": self.size, "mtime_ns": self.mtime_ns,
            "digest": self.digest, "digest_state": str(self.digest_state),
        }

    def written_by(self, entry_id: str) -> bool:
        """Whether ``entry_id``'s write went through this record."""
        return entry_id in (self.entries or ((self.entry_id,) if self.entry_id else ()))


def _key(snapshot: TagSnapshot) -> tuple[str, str]:
    """What identifies one record: the FILE and the FIELD, never the file alone.

    Adoption may write more than one field to one file, and keying on the file
    would let the second record replace the first.
    """
    return (snapshot.file, snapshot.field)


@dataclass(frozen=True, slots=True)
class RevertLedger:
    """Every tag value adoption has overwritten in this library.

    A TUPLE rather than a mapping, so nothing is tempted to key it on something
    a user can rename.
    """

    snapshots: tuple[TagSnapshot, ...] = ()

    def snapshot(self, file: str, field: str) -> TagSnapshot | None:
        found = (entry for entry in self.snapshots if (entry.file, entry.field) == (file, field))
        return next(found, None)

    def with_snapshot(self, snapshot: TagSnapshot) -> RevertLedger:
        """This ledger plus ``snapshot``, KEEPING any record already there.

        First write wins: the second call happens on a re-run after a crash, when
        the file holds what adoption wrote, so replacing would record the
        replacement as the original.
        """
        if self.snapshot(snapshot.file, snapshot.field) is not None:
            return self
        return RevertLedger(tuple(sorted((*self.snapshots, snapshot), key=_key)))

    def replacing(self, snapshot: TagSnapshot) -> RevertLedger:
        """This ledger with ``snapshot`` substituted for the record it keys to.

        Only for amending a record WITHOUT touching its ``original`` (appending a
        plan entry, stamping the file); :meth:`with_snapshot` is the way in.
        """
        return self.without(frozenset({_key(snapshot)})).with_snapshot(snapshot)

    def without(self, keys: frozenset[tuple[str, str]]) -> RevertLedger:
        """This ledger minus the records named, for use after a revert lands."""
        return RevertLedger(tuple(entry for entry in self.snapshots if _key(entry) not in keys))


#: What an absent file resolves to: "nothing has been overwritten" is an answer.
EMPTY = RevertLedger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory."""
    return config.state_path(STATE_KEY, cfg)


def lock_for(cfg: config.Config, state_key: str) -> Path:
    """The sibling lock of one adoption document, in the never-restored lock directory.

    Not beside the document: a restore that replaced the directory holding a
    lock would swap the inode a live advisory lock is held on, and both holders
    would go on believing they had exclusive access.
    """
    return config.state_path(LOCK_KEY, cfg) / f"{state_key}.lock"


def lock_path(cfg: config.Config) -> Path:
    """The revert ledger's sibling lock."""
    return lock_for(cfg, STATE_KEY)


def read_raw(path: Path, refused: Callable[..., LedgerUnreadable]) -> bytes | None:
    """An adoption document's bytes, None when there is none, refused when unreadable."""
    try:
        return config.read_bytes_if_present(path)
    except OSError as exc:
        raise refused(path, f"exists and could not be read: {exc}") from exc


def read_document(
    raw: bytes, path: Path, refused: Callable[..., LedgerUnreadable], *, noun: str,
    schema_version: int,
) -> tuple[dict, int]:
    """An adoption document's JSON object and its schema version, or the refusal."""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise refused(path, f"is not readable as JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise refused(path, f"holds a {type(data).__name__} at its top level rather than {noun}")
    version = data.get("schema_version")
    if not isinstance(version, int):
        raise refused(
            path,
            "carries no integer schema_version, so nothing can be said about the shape of "
            "what follows it",
        )
    if version > schema_version:
        raise refused(
            path,
            f"was written at schema version {version}; this build understands "
            f"{schema_version}",
            Remedy.UPGRADE_CRATEKIT,
        )
    return data, version


_refused = RevertLedgerUnreadable.at


def _original_values(original: Any, *, path: Path, at: str) -> tuple[str, ...] | None:
    """The recorded original: a list of values, a bare string (one value, an older
    document), or null (the field was absent). Anything else is refused.
    """
    if original is None:
        return None
    if isinstance(original, str):
        return (original,)
    if isinstance(original, list) and all(isinstance(v, str) for v in original):
        return tuple(original)
    kind = type(original).__name__
    raise _refused(path, f"{at} whose original value is a {kind} rather than the field's values")


def _entry_list(entry: dict, *, path: Path, at: str) -> tuple[str, ...]:
    """Every plan entry that wrote through this record, falling back to its creator."""
    found = entry.get("entries")
    if found is None:
        created = str(entry.get("entry") or "")
        return (created,) if created else ()
    if not isinstance(found, list) or not all(isinstance(v, str) for v in found):
        raise _refused(path, f"{at} whose entry list is a {type(found).__name__}")
    return tuple(found)


def _optional_int(entry: dict, name: str, *, path: Path, at: str) -> int | None:
    """One of the after-the-write stamps. Absent and null both mean unstamped."""
    found = entry.get(name)
    if found is None:
        return None
    if isinstance(found, bool) or not isinstance(found, int):
        raise _refused(path, f"{at} whose {name} is a {type(found).__name__} rather than a number")
    return found


def _digest(entry: dict, *, path: Path, at: str) -> str:
    """The recorded digest, recognized as a STRING rather than by truthiness.

    Absent and null both mean no digest was written. Every other non-string is
    refused: reading falsy JSON as "no digest" weakened the guard, and
    stringifying the rest guaranteed a digest that could never match.
    """
    found = entry.get("digest")
    if found is None:
        return ""
    if not isinstance(found, str):
        raise _refused(
            path,
            f"{at} whose digest is a {type(found).__name__} rather than a string; a record "
            f"whose only unforgeable evidence is unreadable cannot be spent on a guess",
        )
    return found


def _digest_state(entry: dict, digest: str, *, path: Path, at: str) -> DigestState:
    """Which fact this record's digest, or lack of one, actually is.

    A document WITHOUT the key predates the state and is derived conservatively
    (a digest present means recorded). An explicit null is a state no build can
    name and is refused, unlike ``_digest``'s field where both spellings mean
    the same. A state contradicting the digest is refused in BOTH directions.
    """
    if "digest_state" not in entry:
        return DigestState.RECORDED if digest else DigestState.ABSENT
    found = entry["digest_state"]
    if not isinstance(found, str) or found not in _DIGEST_STATES:
        raise _refused(
            path,
            f"{at} whose digest_state is {found!r}, which is not one of "
            f"{sorted(_DIGEST_STATES)}",
        )
    state = DigestState(found)
    if state is DigestState.RECORDED and not digest:
        raise _refused(
            path,
            f"{at} that says its digest was recorded and carries none; a record "
            f"cannot claim evidence it does not have",
        )
    if state is not DigestState.RECORDED and digest:
        raise _refused(
            path,
            f"{at} that says its digest is {found!r} and carries one anyway; a record cannot "
            f"disown the evidence it is holding, and reporting that record as carrying no "
            f"digest says something false about the document on disk",
        )
    return state


def read(cfg: config.Config) -> RevertLedger:
    """The effective ledger for this library. An absent file is the empty one."""
    path = path_for(cfg)
    raw = read_raw(path, _refused)
    if raw is None:
        return EMPTY
    data, _version = read_document(
        raw, path, _refused, noun="a revert ledger", schema_version=SCHEMA_VERSION
    )
    entries = data.get("snapshots")
    if not isinstance(entries, list):
        raise _refused(path, f"has no snapshots array; its records are a {type(entries).__name__}")

    records: list[TagSnapshot] = []
    seen: set[tuple[str, str]] = set()
    for position, entry in enumerate(entries):
        at = f"holds a record at position {position}"
        if not isinstance(entry, dict):
            raise _refused(path, f"{at} that is a {type(entry).__name__} rather than an object")
        for name in ("file", "field", "path", "written"):
            if not isinstance(entry.get(name), str) or not entry[name]:
                raise _refused(
                    path,
                    f"{at} with no {name}; a record that cannot say which file and field it "
                    f"describes cannot restore anything",
                )
        if "original" not in entry:
            # A missing key and a null are different facts: null means "the field
            # was absent, restore by deleting", and reading a missing key as null
            # deletes a field nobody recorded anything about.
            raise _refused(
                path,
                f"{at} with no original key at all; absence of a fact and absence AS a fact "
                f"are different, and reading the first as the second reverts by deleting a "
                f"field this ledger never saw",
            )
        if not _is_an_identity(str(entry["file"])):
            # A record keyed by a scheme this build does not write is a second
            # identity for a file that already has one.
            raise _refused(
                path,
                f"{at} whose file identifier is {entry['file']!r}, which is neither this "
                f"build's {IDENTITY_SCHEME} identity nor the {_LEGACY_ID_WIDTH} character path "
                f"digest that preceded it; a record keyed by an unknown scheme is a second "
                f"identity for a file that already has one",
            )
        original = _original_values(entry["original"], path=path, at=at)
        digest = _digest(entry, path=path, at=at)
        record = TagSnapshot(
            file=str(entry["file"]), field=str(entry["field"]), path=str(entry["path"]),
            original=original, written=str(entry["written"]),
            recorded=str(entry.get("recorded") or ""), entry_id=str(entry.get("entry") or ""),
            entries=_entry_list(entry, path=path, at=at),
            size=_optional_int(entry, "size", path=path, at=at),
            mtime_ns=_optional_int(entry, "mtime_ns", path=path, at=at),
            digest=digest, digest_state=_digest_state(entry, digest, path=path, at=at),
        )
        if _key(record) in seen:
            raise _refused(
                path,
                f"holds two records for {record.field!r} on one file; a ledger that gives two "
                f"answers for one field cannot say which value to restore, and resolving that "
                f"by line order decides what a user's file ends up holding",
            )
        seen.add(_key(record))
        records.append(record)
    return RevertLedger(tuple(sorted(records, key=_key)))


def write(cfg: config.Config, ledger: RevertLedger) -> Path:
    """Persist ``ledger`` atomically and owner only, sorted so the bytes are a
    function of the content alone.
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        "snapshots": [entry.to_json() for entry in sorted(ledger.snapshots, key=_key)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path
