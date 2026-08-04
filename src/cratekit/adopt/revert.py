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

**A RECORD IS ABOUT A FILE, AND A PATH IS NOT ONE.** First-write-wins below is
reachable only if two adoptions of one file agree about which file it is, and
they used to agree by hashing the path. A hardlink, a case varying spelling on a
case insensitive volume, and a rename between two runs are three ways one file
has two paths, and each of them produced a SECOND record whose ``original`` was
the value adoption itself had just written. The user's own value was then in no
file and in no record. Identity is ``(st_dev, st_ino)``, which asks the
filesystem instead of guessing from a name; the path stays in the record as an
address and as documentation. See :func:`identity_of` for why lowercasing the
path is the same defect pointed the other way.

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

**A record says what the file looked like when adoption left it.** A digest of
the whole file, stamped after the write, plus the size and modification time.
Only the digest decides anything. Without it the revert writes the recorded
original onto whatever is at that path now, which after somebody replaced the
file is a stranger's audio getting a genre it never had. What that evidence may
and may not conclude is the subject of :func:`_changed_since_adoption`, and it is
the part of this module that has been wrong most often.

**A record that cannot produce that digest REFUSES, and says which of the ways it
is.** There is no state in which the metadata stands in for the bytes, because
every value except the digest can be set by any tool that copies a file, and
every attempt to let one of them decide has ended with a file nobody could put
back. :class:`DigestState` is why an empty digest is no longer two facts at once.

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
import re
import stat as stat_module
import time
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Collection, Mapping

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


class AdoptedFileUnidentifiable(CratekitError):
    """The file about to be written to cannot be identified, so nothing is written.

    RECORDING IS NOT OPTIONAL, so failing to identify the file has to stop the
    write rather than proceed without a record. A tag write with no record behind
    it is the one operation in this product that cannot be undone by any means,
    which is the whole reason this module exists.

    It is per FILE and not per run. :func:`cratekit.adopt.apply.apply_plan`
    catches it and fails exactly that entry, which is the per-track versus
    per-pass rule this repository keeps paying for. The shape that reaches it is
    ordinary: a track present in the census and deleted before the apply gets to
    it.
    """

    def __init__(self, message: str, *, path: Path) -> None:
        super().__init__(
            Cause(
                reason="adoption-file-unidentifiable",
                message=message,
                remediation=Remediation(remedy=Remedy.RETRY_LATER),
                scope=Scope.ITEM,
                origin=("adopt",),
                detail={"path": str(path)},
            )
        )
        self.path = path


#: What the identity of a file is a statement ABOUT, spelled into the value so a
#: document cannot be read as the other scheme by accident.
IDENTITY_SCHEME = "dev-ino"

#: The identity this build writes: the volume and the inode, and nothing else.
_INODE_IDENTITY = re.compile(rf"^{IDENTITY_SCHEME}:-?\d+:-?\d+$")

#: The width the PREVIOUS scheme truncated its path digest to. Ledgers written by
#: it are still on disk, so the width is still load bearing: it is how
#: :func:`_legacy_file_id` finds the record an upgraded run has to keep rather
#: than write a second one beside. Changing it re-keys every legacy record and
#: strands the original each one holds.
_LEGACY_ID_WIDTH = 24

_LEGACY_IDENTITY = re.compile(rf"^[0-9a-f]{{{_LEGACY_ID_WIDTH}}}$")


def identity_of(path: Path) -> str:
    """The stable identifier for one file on disk: its VOLUME and its INODE.

    THE PATH IS NOT THE IDENTITY, and reading it as one destroyed user data. The
    previous scheme hashed the decoded, composition-normalized path, which is
    correct about exactly one of the ways two strings name one file and wrong
    about the rest:

    * **A hardlink or a symlink.** ``os.link(a, b)`` makes two names for one
      inode. Two path digests, two records, and the SECOND record's ``original``
      is whatever the first record's write had already put in the field, because
      :meth:`RevertLedger.with_snapshot`'s first-write-wins never engages between
      two different identities. The user's own value then exists in no file and
      no record.
    * **A case varying spelling on a case insensitive volume**, which is the APFS
      default and the platform this product targets. ``Song.flac`` and
      ``song.flac`` are ONE file and two path digests, with the same result.
    * **A rename between two adoption runs.** The file is the same file, the
      digest is different, and the second run records adoption's own value as the
      original.

    LOWERCASING THE PATH IS NOT THE FIX AND WAS NOT TAKEN. Case insensitivity is
    a property of the VOLUME rather than of the string, so a case sensitive
    volume genuinely can hold two files differing only in case, and folding them
    together is the same defect pointed the other way: one record for two files,
    one original lost. ``(st_dev, st_ino)`` answers all four shapes without
    deciding anything about strings, because it asks the filesystem which file it
    is instead of guessing from its name.

    THE PATH IS STILL RECORDED, because a person reading the ledger needs to know
    which file a record is about and the revert needs somewhere to look. It is
    documentation and an address, not identity.

    RAISES rather than falling back when the file cannot be stat'd. A fallback to
    the path would put a second identity scheme back into one ledger, which is
    the defect this function exists to remove.
    """
    try:
        info = path.stat()
    except OSError as exc:
        raise AdoptedFileUnidentifiable(
            f"{path} cannot be identified on this machine: {exc}. Nothing is "
            f"written to a file whose original cannot be recorded first, because "
            f"a tag write with no record behind it is the one thing this product "
            f"cannot undo",
            path=path,
        ) from exc
    return f"{IDENTITY_SCHEME}:{info.st_dev}:{info.st_ino}"


def _legacy_file_id(path: str) -> str:
    """The identifier the PREVIOUS scheme wrote, for finding its records.

    Kept solely so an upgraded run finds the record a legacy ledger already holds
    for this file and KEEPS it, rather than writing a second record whose
    ``original`` is the value adoption itself wrote. It is never written into a
    new record.

    A digest of the DECODED, composition-normalized path, which is the primitive
    U31 owns: the same accented filename arrives in two different codepoint
    sequences depending on who produced the string.
    """
    return hashlib.sha256(
        locations.location_to_path(str(path)).encode("utf-8")
    ).hexdigest()[:_LEGACY_ID_WIDTH]


def _is_an_identity(value: str) -> bool:
    """Whether ``value`` is an identifier one of the two schemes actually wrote.

    RECOGNIZED POSITIVELY, like every other field this reader takes off disk. The
    previous version accepted any non-empty string, so a record whose ``file``
    said ``not-a-digest`` restored normally and a build that changed the identity
    scheme left every old record in place as a second identity for the same file.
    """
    return bool(_INODE_IDENTITY.match(value) or _LEGACY_IDENTITY.match(value))


class DigestState(StrEnum):
    """What a record is able to say about the bytes adoption left behind.

    THREE NAMED STATES RATHER THAN AN EMPTY STRING, and the reason is the shape
    this module has now been wrong about four times: one value standing for two
    different facts. ``digest = ""`` meant BOTH "nothing about the bytes was ever
    written down" and "the read that was supposed to write them down failed", and
    on disk the two were indistinguishable forever afterwards. The second is a
    file this build wrote seconds earlier, where the digest could have been
    retried; the first is a document from a build that had no digest at all. They
    have different causes, they deserve different reports, and collapsing them
    meant nothing could ever tell them apart again.

    All three are recorded per record and none of them is an acceptance. Only
    :attr:`RECORDED` carries evidence, so only :attr:`RECORDED` can be compared
    against a file; the other two refuse and name themselves, and ``force``
    spends them one record at a time.
    """

    #: ``digest`` holds a sha256 of the whole file exactly as adoption left it.
    #: The one state :func:`_changed_since_adoption` can conclude anything from.
    RECORDED = "recorded"

    #: The stamping read was attempted and failed, after a retry. The record
    #: knows it should be carrying a digest and knows it is not.
    UNREADABLE = "unreadable"

    #: Nothing about the bytes was ever written down here. A record whose write
    #: never reached the stamp, or a document from a build that had no digest.
    ABSENT = "absent"


#: The states a document may spell, derived from the enum rather than listed
#: beside it, so a fourth state cannot arrive without the reader recognizing it.
_DIGEST_STATES: frozenset[str] = frozenset(str(member) for member in DigestState)


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

    THE LAST FOUR FIELDS ARE THE FILE AS ADOPTION LEFT IT, stamped after the
    write rather than before it, so a later revert can tell its own handiwork
    from a file somebody has since replaced. They are absent on a record whose
    write did not complete, which is the crash seam, and that record REFUSES
    rather than passing: see :class:`DigestState`.

    ONLY ``digest`` IS ABOUT THE BYTES, and confusing the other two for it is the
    mistake that shipped. ``size`` and ``mtime_ns`` are metadata that CORRELATE
    with the bytes: they are cheap, and either of them can be set to any value by
    any tool that copies a file. ``mtime_ns`` therefore DECIDES NOTHING and is
    recorded only so a person reading the ledger can see when adoption ran;
    ``size`` is consulted only as a shortcut that cannot change an answer, since
    two different sizes cannot be the same bytes. ``digest`` is over the file
    exactly as adoption left it, it is the only one of the three a replacement
    cannot forge, and it is also the only evidence that survives those same bytes
    being copied back from somewhere else. It is the ONLY thing
    :func:`_changed_since_adoption` accepts on.

    ``digest_state`` SAYS WHICH FACT AN EMPTY DIGEST IS, and it exists because
    the empty string was two facts at once. See :class:`DigestState`.

    TWO THINGS THAT LOOK LIKE IDENTITY AND ARE NOT. Each was proposed as proof
    and each is measured wrong, which is why they are named here rather than
    left for somebody to propose a third time.

    * **The value in the field.** ``written`` is a taxonomy bucket's DISPLAY
      name, so it is shared by most of the library it was written into. A
      stranger's recording whose own genre is that bucket satisfies "the field
      still holds what adoption wrote" exactly, and a revert that trusted it put
      one file's genre onto another file's audio, destroyed the replacement's own
      genre with no record anywhere, and dropped the ledger record.
    * **The inode.** The same inode is the same FILE and says nothing about its
      CONTENT. Both ``Path.write_bytes`` and ``cp`` truncate in place and keep
      the inode, measured True for both, and that is how a track is actually
      replaced. So an inode match cannot separate "this product rewrote a tag"
      from "somebody put a different recording here", and ``file`` is never
      consulted by :func:`_changed_since_adoption` for that reason.

    WHICH IS EXACTLY WHY ``file`` HOLDS IT, and the two uses must not be
    confused. ``file`` answers "which file is this record about", where
    ``(st_dev, st_ino)`` is precisely right and a path is precisely wrong (see
    :func:`identity_of`). ``digest`` answers "are these the bytes adoption left",
    where the inode says nothing at all. One record needs both answers and they
    are different questions.
    """

    #: WHICH FILE, as ``dev-ino:<st_dev>:<st_ino>``, or a legacy path digest on a
    #: record written before :func:`identity_of`. Never a path. See
    #: :func:`identity_of` for the four ways a path is not an identity.
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
            "digest": self.digest,
            "digest_state": str(self.digest_state),
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


def _digest(entry: dict, *, path: Path, position: int) -> str:
    """The recorded digest, recognized as a STRING rather than by truthiness.

    ``str(entry.get("digest") or "")`` was the shape here, and every falsy JSON
    value went through it into the same empty string: ``null``, ``0``, ``false``,
    ``""``, ``[]`` and ``{}`` all read back as "no digest" and took the fallback,
    while ``12345`` and ``["abc"]`` were stringified into a digest that could
    never match. Six shapes silently weakening a guard and two shapes quietly
    guaranteeing a refusal is not a recognition, it is a coincidence of what
    Python calls false.

    An absent key and an explicit null are the same fact here, unlike ``original``
    next door: both mean no digest was written, and neither can be read as one.
    Everything else is a document this build did not write.
    """
    found = entry.get("digest")
    if found is None:
        return ""
    if not isinstance(found, str):
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} whose digest is a "
            f"{type(found).__name__} rather than a string; a record whose only "
            f"unforgeable evidence is unreadable cannot be spent on a guess",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    return found


def _digest_state(
    entry: dict, digest: str, *, path: Path, position: int
) -> DigestState:
    """Which fact this record's digest, or lack of one, actually is.

    A DOCUMENT WITHOUT THE KEY IS DERIVED RATHER THAN REFUSED, because every
    record written before this state existed carries the ambiguity the state was
    added to remove, and refusing them would strand a whole ledger. The
    derivation is deliberately the conservative one: a digest present means it
    was recorded, and anything else means nothing about the bytes is available.
    Neither derived answer accepts a file; only the first can even be compared.

    AN ABSENT KEY AND AN EXPLICIT NULL ARE DIFFERENT FACTS HERE, which is the
    distinction ``original`` next door refuses to collapse and this field used to
    collapse silently. ``entry.get("digest_state")`` answers None for both, so a
    document spelling ``"digest_state": null`` took the older-document derivation
    reserved for a document that never had the key, while ``""`` was refused. A
    build that wrote null wrote a state it could not name, and the honest answer
    to a state this reader cannot name is the refusal below rather than a guess
    at what an older build would have meant. ``_digest`` next door states the
    opposite choice for its own field, and states why: there, both spellings mean
    the same thing.

    A STATE AND A DIGEST THAT CONTRADICT EACH OTHER ARE REFUSED, IN BOTH
    DIRECTIONS, because a record claiming to carry evidence it does not carry and
    a record carrying evidence it says it does not have are the same confusion
    this field exists to end. Only the first direction was checked, so a record
    spelling ``absent`` while holding a digest that matched the file exactly was
    accepted and then refused at the guard with ``no digest was recorded``, which
    is a false statement about the document on disk.
    """
    if "digest_state" not in entry:
        return DigestState.RECORDED if digest else DigestState.ABSENT
    found = entry["digest_state"]
    if not isinstance(found, str) or found not in _DIGEST_STATES:
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} whose digest_state is "
            f"{found!r}, which is not one of {sorted(_DIGEST_STATES)}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    state = DigestState(found)
    if state is DigestState.RECORDED and not digest:
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} that says its digest "
            f"was recorded and carries none; a record cannot claim evidence it "
            f"does not have",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if state is not DigestState.RECORDED and digest:
        raise RevertLedgerUnreadable(
            f"{path} holds a record at position {position} that says its digest "
            f"is {found!r} and carries one anyway; a record cannot disown the "
            f"evidence it is holding, and reporting that record as carrying no "
            f"digest says something false about the document on disk",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    return state


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
        if not _is_an_identity(str(entry["file"])):
            # POSITIVELY RECOGNIZED, like every other field here. Accepting any
            # non-empty string meant nothing could notice a record keyed by a
            # scheme this build does not write: a build that changed the
            # identifier left every old record in the document as a SECOND
            # identity for the same file, which is two records for one file
            # arriving through a constant nothing guarded.
            raise RevertLedgerUnreadable(
                f"{path} holds a record at position {position} whose file "
                f"identifier is {entry['file']!r}, which is neither this build's "
                f"{IDENTITY_SCHEME} identity nor the {_LEGACY_ID_WIDTH} character "
                f"path digest that preceded it; a record keyed by an unknown "
                f"scheme is a second identity for a file that already has one",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        original = _original_values(entry["original"], path=path, position=position)
        digest = _digest(entry, path=path, position=position)
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
            digest=digest,
            digest_state=_digest_state(entry, digest, path=path, position=position),
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
    """The record half, assuming the caller already holds the lock.

    THE LOOKUP IS WHAT MAKES FIRST-WRITE-WINS REACHABLE, and it is the half that
    was broken. Two recorded locations naming one file used to produce two
    identities, so :meth:`RevertLedger.with_snapshot` never saw the record it was
    supposed to keep, and the second record stored the value adoption itself had
    written as the "original". See :func:`identity_of` for the four spellings
    that do that.

    A LEGACY RECORD IS FOUND AND MIGRATED RATHER THAN LEFT BESIDE A NEW ONE. A
    ledger written by the path-digest scheme is on disk and its records hold the
    only copy of their originals. Looking only for the new identity would find
    nothing and write a second record whose original is adoption's value, which
    is the same data loss arriving through the upgrade rather than through a
    hardlink.

    THE RECORDED PATH IS REFRESHED WHEN IT NO LONGER NAMES THIS FILE, because the
    path is the revert's only address for it. A file renamed between two adoption
    runs is the same inode and a different name, and leaving the old name in the
    record points the revert at something that is not there.
    """
    ledger = read(cfg)
    identifier = identity_of(resolved)
    existing = ledger.snapshot(identifier, field)
    if existing is None:
        legacy = _legacy_file_id(str(resolved))
        held = ledger.snapshot(legacy, field)
        if held is not None:
            existing = replace(held, file=identifier)
            ledger = ledger.without(frozenset({(legacy, field)}))
            ledger = ledger.with_snapshot(existing)
            write(cfg, ledger)
    if existing is not None and existing.path != str(resolved):
        try:
            still_there = identity_of(Path(existing.path)) == identifier
        except AdoptedFileUnidentifiable:
            still_there = False
        if not still_there:
            existing = replace(existing, path=str(resolved))
            ledger = ledger.replacing(existing)
            write(cfg, ledger)
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


#: How long one file's bytes are waited for before the read gives up and SAYS SO.
#: A whole number of seconds because it is a patience, not a measurement: what it
#: separates is "this disk is busy" from "this file is being fetched across a
#: network", and nothing between those two needs deciding to the millisecond.
#: Generous rather than tight, because the answer to exceeding it is a refusal
#: the person then has to override.
_READ_DEADLINE_SECONDS = 30

#: One megabyte per read, which is what makes the deadline checkable at all: the
#: bound is asked BETWEEN blocks, so a smaller block asks it more often and a
#: whole-file read asks it never.
_READ_BLOCK_BYTES = 1024 * 1024


def digest_of(path: Path, *, deadline_seconds: float = _READ_DEADLINE_SECONDS) -> str:
    """A digest of the whole file. Empty when it cannot be read.

    Over the file's own bytes rather than its decoded audio, deliberately. What a
    later revert needs is "are these the bytes adoption left", and a copy that
    reproduces them exactly is the case this exists for. Decoding would answer a
    different and more expensive question, and would call a file whose tag
    somebody edited a match.

    THE EMPTY ANSWER IS NOT A DIGEST AND BOTH CALLERS TREAT IT AS ITS OWN FACT.
    No sha256 is the empty string, so "" is unambiguous here; what was ambiguous
    was what the callers did with it. :func:`_stamped` used to store it as though
    it were "no digest was recorded", and :func:`_changed_since_adoption` used to
    let it fall into the inequality and report a file nobody had touched as
    somebody else's bytes. Both now name it.

    A TIMEOUT RAISES AND IS NOT FOLDED INTO THE EMPTY ANSWER, which is the same
    "one value standing for two facts" this module has been wrong about
    repeatedly, and here it is worse than usual: ``TimeoutError`` IS an
    ``OSError``, so a plain ``except OSError`` swallows a deadline into "the
    bytes cannot be read", and a person is told their file is unreadable when
    what actually happened is that a provider is still fetching it. The
    ``except`` order below is load bearing for that reason.

    WHAT THE DEADLINE DOES AND DOES NOT BOUND, stated rather than implied. It is
    asked BETWEEN blocks, so it bounds a stream that is arriving slowly and it
    does NOT bound one ``read`` call that never returns at all. A blocking read
    against a filesystem that has stopped answering is uninterruptible from
    Python without a thread, and a thread would leave the read running after the
    answer was abandoned. The shapes that genuinely never return are answered
    one level up instead, by refusing anything that is not a regular file before
    a descriptor is ever opened: see :func:`_look_at`. Residual R-25 states what
    is left.
    """
    hasher = hashlib.sha256()
    give_up_at = time.monotonic() + deadline_seconds
    try:
        with path.open("rb") as handle:
            while True:
                block = handle.read(_READ_BLOCK_BYTES)
                if not block:
                    break
                hasher.update(block)
                if time.monotonic() > give_up_at:
                    raise TimeoutError(
                        f"{path} did not finish arriving within "
                        f"{deadline_seconds} seconds"
                    )
    except TimeoutError:
        raise
    except OSError:
        return ""
    return hasher.hexdigest()


#: How many times the stamping read is attempted before the record gives up and
#: SAYS SO. Two rather than one because the read happens microseconds after a
#: successful write of the same file, so the failures that reach it are the
#: transient ones: a descriptor exhausted by a parallel pass, a brief input
#: output error, a provider stalling. Two rather than many because a permission
#: that is not going to change does not become a different answer by being asked
#: again, and the honest response to that is a recorded state rather than a
#: retry loop holding the ledger's lock.
_STAMP_READ_ATTEMPTS = 2


def _stamp_digest(path: Path) -> str:
    """The digest of what was just written, retried before it is given up on.

    Empty means every attempt failed, which the caller records as
    :attr:`DigestState.UNREADABLE` rather than as "no digest". THAT DISTINCTION
    IS THE WHOLE POINT: a build that wrote this file seconds ago and could not
    read it back is not the same thing as a document written before digests
    existed, and the previous version stored both as an empty string.

    A DEADLINE ENDS THE RETRIES RATHER THAN DOUBLING THEM. The argument for
    asking twice is that a transient failure costs nothing to re-ask; a read that
    ran out of patience is the opposite, and asking again spends the whole
    deadline a second time with the ledger's lock held throughout.
    """
    found = ""
    for _attempt in range(_STAMP_READ_ATTEMPTS):
        try:
            found = digest_of(path)
        except TimeoutError:
            return ""
        if found:
            break
    return found


def _stamped(record: TagSnapshot, path: Path) -> TagSnapshot:
    """``record`` carrying the file as adoption has just left it.

    THE DIGEST COSTS ONE EXTRA READ PER FILE, and it is the only evidence in this
    record that survives the file being copied back from a backup: the inode
    moves, the time moves, and the bytes do not. The read is sequential and
    happens immediately after mutagen has rewritten the same file, so the pages
    are already warm.

    EVERY EXIT FROM HERE LEAVES THE RECORD SAYING WHAT IT KNOWS. A failed
    ``stat`` and a failed digest read are both recorded as
    :attr:`DigestState.UNREADABLE`, so neither can later be mistaken for a
    document that simply predates the digest. The failed ``stat`` branch used to
    carry a ``pragma: no cover`` asserting it could not happen because the write
    above had succeeded, which does not follow: a write returning does not make a
    later ``stat`` succeed, and the pragma was a claim about a branch nothing
    drove. It is driven now.

    THE FAILED ``stat`` BRANCH CLEARS THE STAMP RATHER THAN LEAVING IT. A re-run
    over an already-adopted file arrives here holding the FIRST run's digest, and
    the write one line above has just rewritten the file, so that digest now
    describes bytes that are gone. Keeping it produced a record spelling
    ``unreadable`` while carrying a digest, which is the contradiction
    :func:`_digest_state` refuses in both directions, so the record this build
    wrote made its own ledger unreadable at the next :func:`read`.
    """
    try:
        info = path.stat()
    except OSError:
        return replace(
            record,
            size=None,
            mtime_ns=None,
            digest="",
            digest_state=DigestState.UNREADABLE,
        )
    digest = _stamp_digest(path)
    return replace(
        record,
        size=info.st_size,
        mtime_ns=info.st_mtime_ns,
        digest=digest,
        digest_state=(
            DigestState.RECORDED if digest else DigestState.UNREADABLE
        ),
    )


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
    know is whether the file is still the one adoption wrote to, so the digest it
    compares against has to be adoption's own output.

    A CRASH BETWEEN THE WRITE AND THE STAMP LEAVES A RECORD THAT REFUSES, and it
    used to leave one that accepted anything at all. The window is not exotic: it
    is the whole mutagen tag write, which is the slowest part of this call, so an
    ordinary interrupt lands inside it. The record on disk then says size None,
    mtime None and no digest, and the previous version returned "unchanged" from
    that before consulting anything, so a file replaced months later with a
    different recording was restored over and reported clean. It now refuses and
    names itself for ``force``, which is the trade this module makes everywhere:
    refusing costs an override on a run somebody asked for, accepting costs a
    file nobody can put back. Residual R-26 records what that override costs.

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


class ByteRead(StrEnum):
    """How an attempt to read one file's bytes ended.

    FOUR OUTCOMES RATHER THAN A STRING AND AN EMPTY STRING, for the reason
    :class:`DigestState` gives about its own field: the previous shape answered
    "" for every way a read can fail, so a file being fetched across a network,
    a directory, a named pipe and a permission error were one fact on the way out
    and one message to the person.
    """

    #: The whole file was read and hashed.
    ANSWERED = "answered"

    #: There is no file there to hash: a directory, a named pipe, a socket, a
    #: device. Decided from ``st_mode`` BEFORE a descriptor is opened, which is
    #: what makes a FIFO cost nothing instead of blocking forever.
    NOT_A_REGULAR_FILE = "not-a-regular-file"

    #: The bytes did not arrive within :data:`_READ_DEADLINE_SECONDS`.
    TOOK_TOO_LONG = "took-too-long"

    #: The filesystem answered and refused, or the stat failed outright.
    UNREADABLE = "unreadable"

    #: The recorded size and the file's size disagree, so no read was attempted.
    #: The one shortcut in front of the digest, and it can never change an
    #: answer: two different sizes cannot be the same bytes.
    A_DIFFERENT_SIZE = "a-different-size"


@dataclass(frozen=True, slots=True)
class _Looked:
    """What the bytes at one path are, and the ``stat`` that dates the answer.

    ``stamp`` is what makes the answer re-usable. It is taken immediately BEFORE
    the read, so a later ``stat`` that still equals it says nothing has touched
    the file since, and the digest beside it is still about the bytes that are
    there now. That is the whole mechanism by which the read can happen outside
    the ledger's lock: see :func:`_look_before_the_lock`.
    """

    outcome: ByteRead
    digest: str = ""
    stamp: tuple[int, int, int, int] | None = None


def _stamp_of(info) -> tuple[int, int, int, int]:
    """The cheap facts that say a file has not been touched since it was read.

    The inode is in here for the reason it is NOT in a
    :class:`TagSnapshot`: this is a question about whether the same file is still
    there between two calls seconds apart, which is exactly what an inode
    answers, and not about whether its content is what somebody recorded, which
    is exactly what an inode does not.
    """
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)


def _look_at(target: Path, *, recorded_size: int | None = None) -> _Looked:
    """Ask what the bytes at ``target`` are, bounded, and date the answer.

    THE MODE IS ASKED BEFORE A DESCRIPTOR IS OPENED, and that is the fix for a
    hang rather than a tidiness. ``open`` on a named pipe blocks until a writer
    appears, which is FOREVER for a path nobody is writing to, and the whole pass
    holds the ledger's exclusive lock while it waits, so every apply and every
    revert in the library waits with it. ``exists`` answered True and ``stat``
    answered instantly; only the open did not return. It is the same kernel
    behaviour :func:`cratekit.adopt.scan._probe` refuses to walk into, and this
    module had no equivalent guard: a DIRECTORY at the recorded path reached the
    hash and was reported as "its bytes cannot be read here", which is a
    different fact from "that is not a file".

    THE SIZE SHORTCUT IS ASKED HERE rather than at the caller, so the read that
    it makes unnecessary is never started. It cannot change an answer, which is
    the only reason a shortcut in front of the evidence is tolerable at all.
    """
    try:
        info = target.stat()
    except OSError:
        return _Looked(ByteRead.UNREADABLE)
    stamp = _stamp_of(info)
    if not stat_module.S_ISREG(info.st_mode):
        return _Looked(ByteRead.NOT_A_REGULAR_FILE, stamp=stamp)
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE, stamp=stamp)
    try:
        found = digest_of(target)
    except TimeoutError:
        return _Looked(ByteRead.TOOK_TOO_LONG, stamp=stamp)
    if not found:
        return _Looked(ByteRead.UNREADABLE, stamp=stamp)
    return _Looked(ByteRead.ANSWERED, found, stamp)


def _looked_at_still(
    target: Path, sighted: _Looked | None, *, recorded_size: int | None
) -> _Looked:
    """``sighted`` if it is still current for ``target``, else a fresh look.

    ONE READ SITE, TWO CALLERS. The answer either came from before the lock was
    taken and is still exactly current, or it is taken now. What is deliberately
    NOT here is a second way of deciding about bytes: both branches end in
    :func:`_look_at`, so there is one definition of what the bytes at a path are.

    THE STAMP IS THE WHOLE OF THE RE-USE TEST. A sighting is spent only when a
    ``stat`` taken under the lock still equals the one taken beside the read, so
    anything that touched the file in between, including this pass's own restore
    of another record naming the same file, drops the sighting and the bytes are
    asked about again.
    """
    if sighted is not None and sighted.stamp is not None:
        try:
            info = target.stat()
        except OSError:
            return _Looked(ByteRead.UNREADABLE)
        if _stamp_of(info) == sighted.stamp:
            return sighted
    return _look_at(target, recorded_size=recorded_size)


def _changed_since_adoption(
    record: TagSnapshot, target: Path, sighted: _Looked | None = None
) -> str | None:
    """Why this file is not the one adoption wrote to, or None when it is.

    IT ACCEPTS ONLY EVIDENCE ABOUT THE BYTES, and the four ways this function has
    been wrong before are all the same mistake: taking something that is not
    identity for identity. Three of them reached for a value that merely
    correlates with the bytes; the fourth reached for no value at all and called
    the absence of evidence a pass.

    * **The field's own value is not identity.** ``record.written`` is a taxonomy
      bucket's DISPLAY name, shared by most of the library it was written into, so
      a stranger's recording whose own genre is that bucket satisfies it exactly.
      Measured: the revert then put one file's genre onto another file's audio,
      destroyed the replacement's own genre with no record anywhere, and dropped
      the ledger record.
    * **The inode is not identity either**, which is the version that did not
      ship. The same inode is the same FILE and says nothing about its CONTENT:
      ``Path.write_bytes`` and ``cp`` both truncate in place and keep it, measured
      True for both, and that is how a track is actually replaced.
    * **THE MODIFICATION TIME IS NOT IDENTITY, AND THAT ONE DID SHIP.** The
      previous version accepted "size and time unchanged" as its own definitive
      answer and returned before the digest it had recorded was ever consulted.
      ``st_mtime_ns`` is metadata, not content: ``os.utime``, ``touch -r``,
      ``cp -p``, ``rsync -a``, ``tar -x`` and every tag editor with a preserve
      modification time option all set it to whatever they are told. Measured
      against a genuinely different recording written to the path, padded to the
      recorded size and stamped back to the recorded time: size matched, time
      matched, THE RECORDED DIGEST DID NOT, and the revert restored anyway,
      overwrote the replacement's own genre and dropped the record. That is
      verbatim the harm this function's own refusal message names, reached while
      definitive contrary evidence sat unread in the record.

    * **NOTHING RECORDED IS NOT EVIDENCE EITHER, AND THAT ONE SHIPPED TWICE.**
      An unstamped record returned None before any evidence was consulted, and a
      record whose stamping read had failed fell back to the two values above.
      Both are reachable without forgery, an input output error or a cloud: the
      whole mutagen tag write sits between the record landing on disk and the
      stamp, and it is the slowest part of the operation, so an ordinary
      interrupt lands in it. Measured: a replaced recording of a different size
      and different content restored anyway, ``restored: 1  failed: {}``, the
      replacement's own genre destroyed with no record anywhere.

    SO THERE IS EXACTLY ONE ACCEPTANCE AND IT IS THE BYTES.

    1. **The recorded digest was asked and the file answered with it.** Reached
       only from :attr:`DigestState.RECORDED`, and nothing shortcuts it except a
       size mismatch, which cannot change the answer because two different sizes
       cannot be the same bytes. This is what an untouched file, a backup
       restore, an rsync without timestamps, a cloud re-download and a
       cloud-evicted file that nobody has rewritten all look like.

    Every other path REFUSES and names which of the seven it is, and ``force``
    spends any of them one record at a time:

    * the digest disagrees, so the bytes are not the recorded ones;
    * what is at that path is not a regular file at all;
    * the bytes did not arrive within the deadline;
    * the file cannot be read here to produce a digest at all;
    * the record was never stamped, which is the crash between the write and the
      stamp;
    * the record says its stamping read failed, so a digest was attempted and
      could not be taken;
    * the record carries no digest at all, which is a document predating them.

    THE EVICTION SHORTCUT WAS REMOVED RATHER THAN KEPT, and the measurement is
    why. It skipped the digest on a cloud-evicted file to avoid fetching it from
    a provider, and then the acceptance it produced called :func:`restore_tag`
    one line later, which opens the same file with mutagen and REWRITES it. The
    file is materialized either way, so on the accepting path the skip saved
    nothing and cost the only unforgeable evidence in the record. Nor is the
    population large: the census refuses to adopt an online-only file at all
    (:data:`cratekit.adopt.scan.ADOPTABLE`), so a record can only name an evicted
    file that was readable when adoption wrote it and was evicted afterwards. The
    cost that remains is real and is recorded as residual R-25.

    THE READ IS BOUNDED AND IT HAPPENS BEFORE THE LOCK IS TAKEN. Removing the
    shortcut left an UNBOUNDED fetch inside the exclusive lock that serializes
    every apply and every revert in the library, which R-25 recorded as a
    bandwidth cost and nothing else. Both halves are answered rather than
    documented: ``sighted`` carries the answer :func:`_look_before_the_lock`
    already took outside the lock, and :func:`digest_of` gives up after
    :data:`_READ_DEADLINE_SECONDS`.

    WHAT THE READ COSTS, stated for the case that dominates at scale rather than
    for the flattering one. On the ACCEPTING path it is strictly cheaper than the
    mutagen rewrite immediately behind it, so it is close to free. On the
    REFUSING path it is a whole-file hash that buys a refusal and no write, and a
    library re-tagged by another tool is entirely that case: driven over a four
    record ledger whose every file had been re-tagged elsewhere, this pass
    performed 4 whole-file sha256 reads, 0 writes and 4 refusals. That is not a
    cost the pass was already spending, and the previous version of this
    paragraph claimed it was. The read is kept because it is NECESSARY, not
    because it is free: without it the refusals above are decided by metadata
    anybody can forge.

    WHAT IS DELIBERATELY NOT COVERED, and it used to be. A later write of another
    field this module owns, ``energylevel`` for the analysis workflow, changes the
    bytes, so it refuses and the person overrides it per record. There is no
    evidence available here that separates that from a replacement without
    decoding the audio, and the last two attempts to find one both let the
    catastrophic case through. Refusing costs an override on a run somebody asked
    for; accepting costs a file nobody can put back. Recorded as residual R-22
    with the fix that would close it properly.

    The refusal is EVIDENCE RATHER THAN PERMISSION. See :func:`revert_tags`'s
    ``force``: a person who knows the file is theirs has to be able to say so, per
    record, or a wrong refusal strands a value as surely as a wrong restore
    overwrites one. That is the trade the module makes everywhere: refusing costs
    an override on a run somebody asked for, accepting costs a file nobody can
    put back.
    """
    if record.digest_state is not DigestState.RECORDED:
        return _replaced(record, _why_nothing_to_compare(record))
    looked = _looked_at_still(target, sighted, recorded_size=record.size)
    if looked.outcome is ByteRead.A_DIFFERENT_SIZE:
        # The one shortcut in front of the digest, kept only because it can never
        # change an answer: no hash of a differently sized file can match.
        return _replaced(record, _NOT_THE_RECORDED_BYTES)
    if looked.outcome is ByteRead.NOT_A_REGULAR_FILE:
        return _replaced(record, _NOT_A_REGULAR_FILE)
    if looked.outcome is ByteRead.TOOK_TOO_LONG:
        # NOT folded into "cannot be read". A file still arriving from a provider
        # is a file that will answer later, and telling somebody it is unreadable
        # sends them looking for damage that is not there.
        return _replaced(record, _TOOK_TOO_LONG_TO_READ)
    if looked.outcome is ByteRead.UNREADABLE:
        # An unreadable file is not a verdict about its content. Reporting it as
        # "these are somebody else's bytes" would send a person looking for a
        # replacement that never happened.
        return _replaced(record, _NOT_READABLE_TO_COMPARE)
    if looked.digest != record.digest:
        return _replaced(record, _NOT_THE_RECORDED_BYTES)
    return None


def _why_nothing_to_compare(record: TagSnapshot) -> str:
    """Which of the three ways this record can say nothing about the bytes.

    All three refuse, so this decides only what a person is told, and that is
    worth getting right: "the run died before it finished recording" and "this
    document predates digests" send somebody to different places.
    """
    if record.digest_state is DigestState.UNREADABLE:
        return _THE_STAMP_COULD_NOT_BE_READ
    if record.size is None or record.mtime_ns is None:
        return _THE_STAMP_NEVER_LANDED
    return _NO_DIGEST_WAS_RECORDED


#: The refusals, named once so a report and a test cannot spell them apart. Each
#: one is asserted as a LITERAL IN FULL in the suite rather than by reading the
#: constant back, because a test comparing the output against the constant the
#: output is built from asserts that X equals X and passes whatever either says.
#: In FULL because a leading substring is the same failure one step along: three
#: of these were asserted by their first clause only, so every word after it
#: could be reworded and no test moved.
_NOT_THE_RECORDED_BYTES = (
    "its bytes are not the ones this record was stamped from, and nothing here "
    "can say whether another program wrote them or this tool did"
)
_NOT_READABLE_TO_COMPARE = "its bytes cannot be read here to compare"
_NOT_A_REGULAR_FILE = (
    "what is at that path is not a regular file, so it has no bytes to compare"
)
_TOOK_TOO_LONG_TO_READ = (
    "its bytes did not finish arriving within the time this pass waits, which is "
    "what a file still being fetched from a provider looks like"
)
_THE_STAMP_NEVER_LANDED = (
    "adoption never finished recording what it left there, which is a run "
    "interrupted between the tag write and the stamp"
)
_THE_STAMP_COULD_NOT_BE_READ = (
    "adoption could not read back what it had just written, so the bytes it "
    "left were never recorded"
)
_NO_DIGEST_WAS_RECORDED = (
    "this record carries no digest, so nothing in it is about the bytes at all"
)

#: The two refusals that are about THE LEDGER rather than about the file, and the
#: reason they are separate from the ones above is what a person is told to do
#: next. See :func:`_cannot_say_which_record`.
_TWO_RECORDS_NAME_THIS_FILE = (
    "more than one record in this ledger names the file at that path, so which "
    "of their originals belongs to it cannot be decided from the ledger"
)
_FORCE_NAMES_MORE_THAN_ONE_RECORD = (
    "more than one record in this ledger carries that path and that field, so a "
    "force key naming them cannot say which single record it means"
)


def _replaced(record: TagSnapshot, why: str) -> str:
    """The refusal about the BYTES, naming the key that overrides THIS record.

    IT STATES THE EVIDENCE AND DOES NOT ACCUSE ANYBODY, which is a correction
    rather than a wording preference. The previous text read "the file cannot be
    recognized as the one adoption wrote to: its bytes are not the ones adoption
    left there", which tells a person their file was replaced. Several of the
    ways this refusal is reached are this tool's own doing: a second field
    written to the same file (R-22), a pass that died inside its own restore
    (R-24). A person who reads an accusation and is then handed a ``force`` key
    in the same breath does the thing the message implies, and forcing writes the
    recorded original over whatever is actually there.

    So it says what is known, says that the cause is not determinable from here,
    and says plainly that LEAVING IT is safe. The record keeps the original
    either way; that is the sentence that was missing.
    """
    return (
        f"this record cannot be matched to the file at that path: {why}. "
        f"Restoring the recorded original onto bytes that are not the recorded "
        f"ones writes one file's tag onto another file's audio, and nothing "
        f"anywhere records what it destroyed. If you know that file is the one "
        f"adoption wrote to, override this ONE record by reverting with "
        f"force={(record.path, record.field)!r}. If you do not know, leave it: "
        f"the record keeps the original either way and nothing is lost by "
        f"deciding later."
    )


def _cannot_say_which_record(record: TagSnapshot, why: str) -> str:
    """The refusal about the LEDGER, which deliberately offers no ``force``.

    ``force`` OVERRIDES EVIDENCE ABOUT BYTES AND CANNOT SUPPLY A MISSING FACT.
    What is missing in both cases below is which record belongs to the file, and
    a person answering "yes, that file is mine" does not answer it. Offering the
    override here is what completed the data loss this round exists to fix: two
    records for one file, the good one restored first, the bogus one refused with
    a message inviting an override, and the override wrote the value adoption had
    put there back onto the file as though it were the original.

    So this refusal names the ledger as the thing that is wrong and sends the
    person to the doctor rather than to a flag.
    """
    return (
        f"this record cannot be spent on the file at that path: {why}. force "
        f"does not apply: it overrides evidence about the BYTES, and what is "
        f"missing here is which record belongs to this file, which is a fact "
        f"about the ledger. Run the doctor over "
        f"{(record.path, record.field)!r} instead; every original is still "
        f"recorded and nothing has been written."
    )


def revert_tags(
    cfg: config.Config,
    *,
    entry_id: str | None = None,
    force: Collection[tuple[str, str]] = (),
    restore: Callable[[Path, str, tuple[str, ...] | None], bool] = restore_tag,
) -> RevertReport:
    """Put every recorded original back on disk, exactly.

    ``entry_id`` of None reverts everything the ledger holds; naming one reverts
    every record that entry's write went through. Matched through
    :meth:`TagSnapshot.written_by` rather than against the record's creator,
    because first-write-wins means a second adoption of a file writes through the
    FIRST record: matching on the creator alone answers "nothing to do" for work
    that demonstrably happened and leaves the file holding adoption's value.

    ``force`` NAMES THE RECORDS IT OVERRIDES, one ``(path, field)`` pair each,
    which is the same key :class:`RevertReport` reports them under. It exists
    because the guard is evidence and not permission: a heuristic over a file
    somebody else owns with no override is a heuristic that decides, and a wrong
    refusal strands the only copy of a value as surely as a wrong restore
    overwrites one.

    ``force`` CANNOT REACH TWO RECORDS AND CANNOT SUPPLY AN IDENTITY, which are
    the two limits on it and both were paid for. Its ``(path, field)`` key is not
    unique across records, so one entry used to override every record carrying
    that path; a key that names more than one record now overrides none of them
    and says so. And a record whose file another record also names refuses before
    ``force`` is consulted at all, because what is missing there is which record
    belongs to the file, which is not a fact an override supplies. See
    :func:`_cannot_say_which_record`.

    IT IS NOT A BOOLEAN, and that is the whole of its design. A pass-wide flag,
    which is what this was, is offered by a message printed PER RECORD: a person
    reads "override this" beside the one file they know is theirs, sets the flag,
    and overwrites every other refused file in the ledger at the same time.
    Naming them individually also makes ``entry_id`` unable to stand in, since two
    files written through one plan entry are two records. A caller that genuinely
    means all of them passes ``report.failed`` keys, which is an explicit act over
    a list it has just been shown.

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

    A RECORD IS DROPPED FROM THE LEDGER ONLY AFTER ITS FILE IS WRITTEN, AND
    IMMEDIATELY AFTER. Batching the drops to the end of the pass was worse by a
    whole pass: it left a record on disk for every file the run had already
    restored, none of which matched its own stamp any more, so all of them were
    refused forever while every other record settled. Settling each record as it
    lands costs one small document write per file instead of one per pass.

    IT NARROWS THAT WINDOW RATHER THAN CLOSING IT, and saying so is the point. A
    run that dies BETWEEN a restore landing and that record's drop reaching the
    disk still leaves one record describing bytes its own successful restore has
    already replaced, and the retry refuses exactly that record. Round 3 wrote
    this up as eliminated structurally, which is a stronger claim than the code
    makes: the window went from the whole pass to one record, and one record is
    not none. It cannot be closed from here without a journal, because the
    surviving evidence after such a crash is indistinguishable from a replacement
    without decoding the audio, which is R-22's wall. What makes the residue
    tolerable rather than merely small is that the damage is BOUNDED: the refused
    record names itself for ``force``, and forcing it writes the same original
    onto a file that already holds it. Residual R-24 states the window and the
    journal that would close it.

    THAT BOUND IS ABOUT THE WINDOW AFTER THE RESTORE, NOT THE ONE INSIDE IT, and
    the two are different windows. A death DURING ``restore``'s own rewrite is
    mutagen's write window rather than this pass's, and this module has no bound
    to offer for it: the container may be left half rewritten, and no undo log
    can put back bytes a partial write destroyed. What this module still
    guarantees there is the half it owns. The record is dropped only AFTER the
    restore returns, so a death inside the rewrite leaves the record on disk with
    the original still in it, the retry refuses because the bytes are neither the
    recorded ones nor anything else it knows, and the recorded original is still
    available to ``force``. Written down rather than claimed away, in R-24.

    ONE BAD RECORD COSTS ONE RECORD, which is the per-track versus per-pass rule
    this repository keeps paying for, applied to the undo log. The whole body of
    the loop is guarded, not just the ``restore`` call: ``record.field`` comes off
    disk, where :func:`read` recognizes it as a non-empty string and deliberately
    does not check it against :data:`cratekit.core.tags.FIELDS`, because refusing
    the whole document over one unknown field would strand every other record in
    it. A ledger written by a build with one more field is therefore ordinary, and
    it used to raise ``ValueError`` out of the pass before the lock released, so
    nothing settled and every retry died on the same record.

    ``restore`` RUNS INSIDE THE LOCK and must not take it again. See the module
    docstring: ``flock`` is per open file description, so a callback reaching back
    into this module hangs forever rather than raising.
    """
    restored: list[tuple[str, str]] = []
    failed: dict[tuple[str, str], str] = {}
    forced = {(str(path), str(field)) for path, field in force}
    sighted = _look_before_the_lock(cfg, entry_id=entry_id, forced=forced)
    with config._exclusive_lock(lock_path(cfg)):
        ledger = read(cfg)
        selected = tuple(
            record
            for record in ledger.snapshots
            if entry_id is None or record.written_by(entry_id)
        )
        confused = _records_that_cannot_be_told_apart(selected)
        crowded = _paths_more_than_one_record_carries(selected)
        for record in selected:
            reported = (record.path, record.field)
            if _key(record) in confused:
                failed[reported] = _cannot_say_which_record(
                    record, _TWO_RECORDS_NAME_THIS_FILE
                )
                continue
            if reported in forced and _key(record) in crowded:
                failed[reported] = _cannot_say_which_record(
                    record, _FORCE_NAMES_MORE_THAN_ONE_RECORD
                )
                continue
            try:
                refusal = _revert_one(
                    record,
                    reported in forced,
                    restore=restore,
                    sighted=sighted.get(_key(record)),
                )
            except (OSError, ValueError, tags.UnsupportedContainer) as exc:
                failed[reported] = str(exc)
                continue
            if refusal is not None:
                failed[reported] = refusal
                continue
            restored.append(reported)
            ledger = ledger.without(frozenset({(record.file, record.field)}))
            write(cfg, ledger)
    return RevertReport(restored=tuple(restored), failed=failed)


def _live_identity(path: Path) -> str | None:
    """Which file is at ``path`` right now, or None when that cannot be asked.

    NAMED RATHER THAN FALLING BACK TO THE PATH. A record whose file is missing or
    cannot be stat'd is one this pass knows nothing about, and answering with
    something derived from the path would put the identity scheme this round
    removed straight back in beside the one that replaced it. The callers below
    treat None as "not comparable with anything", which is what it is.
    """
    try:
        return identity_of(path)
    except AdoptedFileUnidentifiable:
        return None


def _records_that_cannot_be_told_apart(
    selected: tuple[TagSnapshot, ...],
) -> frozenset[tuple[str, str]]:
    """The records whose file another record in this pass also names.

    WHY THIS EXISTS AT ALL. :func:`identity_of` stops this build from WRITING two
    records for one file. It does nothing about the ledgers already on disk,
    where a hardlink, a case varying spelling on a case insensitive volume, or a
    rename between two runs each produced a second record whose ``original`` is
    the value adoption itself wrote. Restoring those in ledger order restores the
    real original and then offers to overwrite it with adoption's value, which is
    exactly what happened.

    THE WHOLE GROUP REFUSES, and picking one of them was tried and taken out
    again. The rule "the record carrying the file's own identity wins and the
    rest are ghosts" is decidable, and it makes one ``(path, field)`` key appear
    in ``restored`` AND in ``failed`` in the same report, which is the reporting
    collapse this round is also fixing one door along. It buys nothing real
    either: with :func:`identity_of` in the write path, a group where exactly one
    member carries the live identity is not a shape any sequence of adoptions
    produces. So the pass writes nothing, keeps every original, and says the
    ledger is what needs attention.

    A GROUP OF ONE IS NEVER CONFUSED, whatever its identity says. That is what
    keeps a legacy ledger working: one record for one file is unambiguous however
    it is keyed, and refusing on the SCHEME rather than on the ambiguity would
    strand every ledger written before this round.
    """
    groups: dict[tuple[str, str], list[TagSnapshot]] = {}
    for record in selected:
        found = _live_identity(Path(record.path))
        if found is not None:
            groups.setdefault((found, record.field), []).append(record)
    return frozenset(
        _key(member)
        for members in groups.values()
        if len(members) > 1
        for member in members
    )


def _paths_more_than_one_record_carries(
    selected: tuple[TagSnapshot, ...],
) -> frozenset[tuple[str, str]]:
    """The records a ``(path, field)`` force key could not have meant uniquely.

    ``force`` IS KEYED ON SOMETHING THAT IS NOT UNIQUE, which is the same defect
    as the ledger's old identity one layer up. The ledger keys on the file and
    the field; ``force`` keys on the PATH and the field, because a person has to
    be able to type it. Two records carrying one path therefore both matched one
    force entry, both were overridden, and both were restored, against the
    message's own promise to override "this ONE record".

    Refused rather than resolved, because the fact that would resolve it is which
    record belongs to the file, and that is the fact
    :func:`_records_that_cannot_be_told_apart` has already established cannot be
    had here. What is left is one force key and two candidates, and spending it
    on both is the outcome this refuses.

    THE TWO SETS OVERLAP COMPLETELY OR NOT AT ALL, and that is worth writing down
    because filtering one by the other was tried and measured as changing
    nothing. Two records sharing a path share a field's live identity too, so a
    ``(path, field)`` carried by more than one record is either a group that is
    entirely confused, when the path can be stat'd, or a group that is entirely
    not, when it cannot. Neither set can ever hold part of the other's group.
    """
    counted: dict[tuple[str, str], list[TagSnapshot]] = {}
    for record in selected:
        counted.setdefault((record.path, record.field), []).append(record)
    return frozenset(
        _key(record)
        for members in counted.values()
        if len(members) > 1
        for record in members
    )


def _look_before_the_lock(
    cfg: config.Config,
    *,
    entry_id: str | None,
    forced: Collection[tuple[str, str]],
) -> dict[tuple[str, str], _Looked]:
    """Hash every file this pass is going to ask about, BEFORE the lock is taken.

    THE LOCK SERIALIZES EVERY APPLY AND EVERY REVERT IN THE LIBRARY, and the read
    behind the guard is a whole-file hash that can be a network fetch. Held
    together, one evicted track's download blocked an unrelated
    :func:`write_tag_with_record` on a perfectly local file for the whole of that
    download. The read does not need the lock: what it produces is dated by a
    ``stat``, and :func:`_looked_at_still` spends it only while a ``stat`` taken
    UNDER the lock still equals that one.

    WHAT IT DOES NOT MOVE, stated because the flattering version of this claim is
    wrong. An ACCEPTED record is restored by mutagen reopening the same file
    under the lock, so an evicted file that passes the guard is fetched under the
    lock regardless. What moves outside is the REFUSING path, which is precisely
    the cost R-25 names: the evicted file that is downloaded in order to be
    refused, and the library re-tagged by another tool where every record is that
    case.

    IT IS BEST EFFORT IN EVERY DIRECTION. An unreadable ledger returns nothing
    and the locked read raises the same thing a moment later; a record whose file
    changed between here and the lock simply misses and is read again. Nothing
    here decides anything, which is what makes doing it unlocked safe.
    """
    try:
        ledger = read(cfg)
    except RevertLedgerUnreadable:
        return {}
    seen: dict[tuple[str, str], _Looked] = {}
    for record in ledger.snapshots:
        if entry_id is not None and not record.written_by(entry_id):
            continue
        if record.digest_state is not DigestState.RECORDED:
            continue
        if (record.path, record.field) in forced:
            continue
        seen[_key(record)] = _look_at(Path(record.path), recorded_size=record.size)
    return seen


def _revert_one(
    record: TagSnapshot,
    forced: bool,
    *,
    restore: Callable[[Path, str, tuple[str, ...] | None], bool],
    sighted: _Looked | None = None,
) -> str | None:
    """Put one record's original back. None on success, else why not."""
    target = Path(record.path)
    if not target.exists():
        return "the file is no longer there"
    if not forced:
        replaced = _changed_since_adoption(record, target, sighted)
        if replaced is not None:
            return replaced
    if not restore(target, record.field, record.original):
        return "the container refused the write"
    return None


__all__ = [
    "EMPTY",
    "IDENTITY_SCHEME",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "AdoptedFileUnidentifiable",
    "ByteRead",
    "DigestState",
    "RevertLedger",
    "RevertLedgerUnreadable",
    "RevertReport",
    "TagSnapshot",
    "identity_of",
    "lock_path",
    "path_for",
    "read",
    "restore_tag",
    "revert_tags",
    "snapshot_before_write",
    "write",
    "write_tag_with_record",
]
