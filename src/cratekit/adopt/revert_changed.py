"""The revert ledger's evidence about BYTES: the digest, the stamp, and the guard.

A record says what the file looked like when adoption left it: a digest of the
whole file, stamped after the write, plus the size and modification time. ONLY
THE DIGEST DECIDES ANYTHING. Every other value can be set by any tool that
copies a file, and every attempt to let one of them decide ended with a stranger's
audio getting a genre it never had. A record that cannot produce the digest
REFUSES and says which of the ways it is.

Layer: modules.
"""

from __future__ import annotations

import hashlib
import stat as stat_module
import time
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path

from cratekit.adopt.revert_record import DigestState, TagSnapshot

#: How long one file's bytes are waited for before the read gives up and SAYS SO:
#: a patience separating "this disk is busy" from "this file is being fetched
#: across a network". Generous, because exceeding it is a refusal to override.
_READ_DEADLINE_SECONDS = 30

#: One megabyte per read. The deadline is asked BETWEEN blocks, so a block size
#: is what makes it checkable at all.
_READ_BLOCK_BYTES = 1024 * 1024


def digest_of(path: Path, *, deadline_seconds: float = _READ_DEADLINE_SECONDS) -> str:
    """A digest of the whole file's own bytes. Empty when it cannot be read.

    Over the bytes rather than the decoded audio: the question is "are these the
    bytes adoption left", and decoding would call a re-tagged file a match. No
    sha256 is the empty string, so "" is unambiguous and callers name it.

    A TIMEOUT RAISES rather than folding into the empty answer. ``TimeoutError``
    is an ``OSError``, so the ``except`` order below is load bearing: a provider
    still fetching a file must not be reported as an unreadable one. The deadline
    bounds a stream arriving slowly, not one ``read`` that never returns; those
    shapes are refused before a descriptor is opened (:func:`_look_at`).
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


#: How many times the stamping read is attempted. Two, because the read follows a
#: successful write of the same file so its failures are transient; not many,
#: because a permission does not change by being asked again under the lock.
_STAMP_READ_ATTEMPTS = 2


def _stamp_digest(path: Path) -> str:
    """The digest of what was just written, retried; empty when every attempt failed.

    The caller records empty as :attr:`DigestState.UNREADABLE`, never as "no
    digest". A deadline ends the retries rather than doubling them, since asking
    again would spend the whole deadline a second time under the lock.
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

    Every exit leaves the record saying what it knows: a failed ``stat`` and a
    failed read are both :attr:`DigestState.UNREADABLE`. The failed ``stat``
    CLEARS the stamp, because a re-run arrives holding the first run's digest of
    bytes the write just replaced, and ``unreadable`` with a digest is the
    contradiction the reader refuses.
    """
    try:
        info = path.stat()
    except OSError:
        return replace(
            record, size=None, mtime_ns=None, digest="", digest_state=DigestState.UNREADABLE
        )
    digest = _stamp_digest(path)
    return replace(
        record,
        size=info.st_size,
        mtime_ns=info.st_mtime_ns,
        digest=digest,
        digest_state=DigestState.RECORDED if digest else DigestState.UNREADABLE,
    )


class ByteRead(StrEnum):
    """How an attempt to read one file's bytes ended, one outcome per fact a
    person is told, rather than "" for every way a read can fail.
    """

    #: The whole file was read and hashed.
    ANSWERED = "answered"

    #: A directory, a named pipe, a socket, a device: decided from ``st_mode``
    #: BEFORE a descriptor is opened, so a FIFO costs nothing instead of blocking.
    NOT_A_REGULAR_FILE = "not-a-regular-file"

    #: The bytes did not arrive within :data:`_READ_DEADLINE_SECONDS`.
    TOOK_TOO_LONG = "took-too-long"

    #: The filesystem answered and refused, or the stat failed outright.
    UNREADABLE = "unreadable"

    #: The recorded size and the file's size disagree, so no read was attempted.
    #: Two different sizes cannot be the same bytes, so it never changes an answer.
    A_DIFFERENT_SIZE = "a-different-size"


@dataclass(frozen=True, slots=True)
class _Looked:
    """What the bytes at one path are, and how the attempt to read them ended.

    No ``stat`` is kept beside the answer to validate it later: size, time,
    device and inode all survive a same-length rewrite inside one FAT time tick,
    so none of them may decide that an earlier read still applies.
    """

    outcome: ByteRead
    digest: str = ""


def _look_at(target: Path, *, recorded_size: int | None = None) -> _Looked:
    """Ask what the bytes at ``target`` are, bounded.

    THE MODE IS ASKED BEFORE A DESCRIPTOR IS OPENED: ``open`` on a named pipe
    blocks forever, with the ledger's exclusive lock held and every apply and
    revert waiting on it. The size shortcut is asked here so the read it saves
    is never started.
    """
    try:
        info = target.stat()
    except OSError:
        return _Looked(ByteRead.UNREADABLE)
    if not stat_module.S_ISREG(info.st_mode):
        return _Looked(ByteRead.NOT_A_REGULAR_FILE)
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    try:
        found = digest_of(target)
    except TimeoutError:
        return _Looked(ByteRead.TOOK_TOO_LONG)
    if not found:
        return _Looked(ByteRead.UNREADABLE)
    return _Looked(ByteRead.ANSWERED, found)


def _size_of(target: Path) -> int | None:
    """How many bytes are at ``target``, or None when that cannot be asked.

    It can rule a record OUT (two sizes cannot be the same bytes) and never IN,
    so it never appears on an accepting path without the digest behind it.
    """
    try:
        return target.stat().st_size
    except OSError:
        return None


#: The refusals, named once. Each is asserted as a LITERAL IN FULL in the suite,
#: and so are the messages :func:`_replaced` and
#: ``revert._cannot_say_which_record`` build from them, by equality: a test
#: comparing output against the constant it is built from asserts X equals X.
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

#: What each read that produced no digest is told as. A file still arriving is
#: not "unreadable", and an unreadable one is not "somebody else's bytes": each
#: sends a person looking for something different.
_UNANSWERED = {
    ByteRead.A_DIFFERENT_SIZE: _NOT_THE_RECORDED_BYTES,
    ByteRead.NOT_A_REGULAR_FILE: _NOT_A_REGULAR_FILE,
    ByteRead.TOOK_TOO_LONG: _TOOK_TOO_LONG_TO_READ,
    ByteRead.UNREADABLE: _NOT_READABLE_TO_COMPARE,
}


def _changed_since_adoption(record: TagSnapshot, target: Path) -> str | None:
    """Why this file is not the one adoption wrote to, or None when it is.

    EXACTLY ONE ACCEPTANCE, AND IT IS THE BYTES: the recorded digest was asked
    and the file answered with it. The field's value, the inode, the
    modification time and the absence of a record were each once taken for
    identity, and each let a replaced recording be restored over. Every other
    path refuses and names which of the seven it is; ``force`` spends any of
    them one record at a time, because the refusal is evidence, not permission.

    The read happens under the lock every time; the pre-lock fetch
    (``revert._bring_the_bytes_within_reach``) only warms the file and decides
    nothing. A later Cratekit write of another field changes the bytes and
    refuses too; refusing costs an override, accepting costs a file nobody can
    put back (see the residual "the adoption revert cannot recognize its own
    file after another Cratekit write").
    """
    if record.digest_state is not DigestState.RECORDED:
        return _replaced(record, _why_nothing_to_compare(record))
    looked = _look_at(target, recorded_size=record.size)
    why = _UNANSWERED.get(looked.outcome)
    if why is None and looked.digest != record.digest:
        why = _NOT_THE_RECORDED_BYTES
    return None if why is None else _replaced(record, why)


def _why_nothing_to_compare(record: TagSnapshot) -> str:
    """Which of the three ways this record can say nothing about the bytes."""
    if record.digest_state is DigestState.UNREADABLE:
        return _THE_STAMP_COULD_NOT_BE_READ
    if record.size is None or record.mtime_ns is None:
        return _THE_STAMP_NEVER_LANDED
    return _NO_DIGEST_WAS_RECORDED


def _replaced(record: TagSnapshot, why: str) -> str:
    """The refusal about the BYTES, naming the key that overrides THIS record.

    It states the evidence and accuses nobody, since several ways here are this
    tool's own doing, and it says plainly that LEAVING the record is safe: a
    person told their file was replaced and handed a ``force`` key forces.
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
