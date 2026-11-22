"""The revert ledger: what each file's tag held before adoption overwrote it.

A tag write is the one operation the XML re-import safety net never covered: a
database is snapshotted before every write session (KTD21b, R30), a genre string
written into a file is not, and the value it replaced is gone when the write
returns. So the original is written down BEFORE the file is touched, and the
order is the whole design: recording after the write loses the original to a
crash in the window, while a record for a write that did not happen costs
nothing.

The rules, each paid for once:

* **The whole read-modify-write cycle is under a lock.** An atomic rename does
  nothing for the cycle around it, and two processes adding a record each lost
  one (eight processes, two hundred decisions, seventy one on disk).
* **A record is about a FILE, and nothing one ``stat`` returns is a file.** It
  carries three claims, the volume and inode, the path, and a digest of the
  bytes adoption left. :func:`_record_for` requires them to converge, settles
  the one disagreement the BYTES can answer, and refuses everything else; it
  never rewrites one claim to agree with another.
* **A record is written once and never refreshed.** A second call is a re-run
  after a crash, when the file already holds adoption's value; what accumulates
  is the list of plan entries that wrote through it.
* **What is recorded is the file's values EXACTLY**, through
  :func:`cratekit.core.tags.read_tag_values`: a stripped, first-only or
  absent-for-empty record reports the file restored when it is not.
* **The record and the write are ONE critical section.** A revert landing
  between them would empty the ledger and the write would then land with no
  original behind it, so :func:`write_tag_with_record` and :func:`revert_tags`
  hold the same lock across the whole act.
* **The lock is not reentrant.** ``flock`` is per open file description, so a
  caller's ``restore`` or ``write_field`` callback (both run inside the lock)
  that calls back into this module deadlocks rather than raising. A timeout or a
  reentrancy count would each cost more than it buys; both callbacks are meant
  to be pure.

The document lives in :mod:`cratekit.adopt.revert_record` and the evidence about
bytes in :mod:`cratekit.adopt.revert_changed`; this module is their public face,
the matching of a record to a file, the record-then-write, and the revert.

Layer: modules.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Callable, Collection, Mapping

from cratekit.adopt.revert_changed import (
    ByteRead,
    _changed_since_adoption,
    _look_at,
    _Looked,
    _size_of,
    _stamped,
)
from cratekit.adopt.revert_changed import digest_of as digest_of
from cratekit.adopt.revert_record import (
    EMPTY,
    IDENTITY_SCHEME,
    LOCK_KEY,
    SCHEMA_VERSION,
    STATE_KEY,
    AdoptedFileUnidentifiable,
    DigestState,
    RecordCannotBeMatched,
    RevertLedger,
    RevertLedgerUnreadable,
    TagSnapshot,
    _key,
    _legacy_file_id,
    identity_of,
    lock_path,
    path_for,
    read,
    write,
)
from cratekit.adopt.revert_record import LedgerUnreadable as LedgerUnreadable
from cratekit.cli.output import timestamp
from cratekit.core import config, tags

#: A field's values as a record holds them, None being the field ABSENT.
_Values = tuple[str, ...] | None

#: Records named by their ledger key, the file and the field.
_Keys = frozenset[tuple[str, str]]


@dataclass(frozen=True, slots=True)
class _Matched:
    """The record this file's evidence converged on, before and after re-addressing.

    ``was`` is the record as it sits in the ledger, what has to be REMOVED when
    its key changes; ``now`` is it with whichever address the evidence
    corrected. Equal when nothing moved, which costs no document write.
    """

    was: TagSnapshot
    now: TagSnapshot


def _re_addressed(
    record: TagSnapshot, *, identity: str, path_text: str, keep_path: bool
) -> _Matched:
    """``record`` addressed to the file the evidence just corroborated it is about.

    A caller passing ``keep_path=False`` has just found the file's BYTES equal to
    the record's digest, which a rename, a remount and an ``os.replace`` cannot
    forge; one passing True has a recorded path that still resolves to this
    file. There is no branch correcting a path on the inode alone: on a volume
    that recycles inodes that handed a dead file's original to a live one.
    """
    wanted_path = record.path if keep_path else path_text
    if record.file == identity and record.path == wanted_path:
        return _Matched(record, record)
    return _Matched(record, replace(record, file=identity, path=wanted_path))


def _one_or_none(found: list[TagSnapshot], *, resolved: Path, why: str) -> TagSnapshot | None:
    """The single record in ``found``, or a refusal because there is more than one."""
    if not found:
        return None
    if len(found) > 1:
        raise RecordCannotBeMatched(
            f"{resolved} cannot be matched to one record in the revert ledger: {why}. Nothing "
            f"is written to a file whose original cannot be recorded first, and choosing "
            f"between two records here decides which of two values a later revert puts on "
            f"this file. Nothing has been written and every original in the ledger is still "
            f"recorded; what has to be settled is the ledger.",
            path=resolved,
        )
    return found[0]


def _nothing_unrecorded_is_at_risk(
    record: TagSnapshot, *, written: str, current: Callable[[], _Values]
) -> bool:
    """Whether this write can lose a value the ledger does not already hold.

    NOT AN IDENTITY TEST: the addresses have settled which file this is, and a
    field's value says nothing about that. What is asked is whether the field
    holds a value nothing has written down, the only thing this write can
    destroy. It does not when it holds the record's own ``original``, what the
    record says adoption wrote, or what THIS call is about to write (a write
    that changes nothing loses nothing, which keeps a third adoption under
    another taxonomy working).
    """
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))


def _settled_or_refused(
    record: TagSnapshot, resolved: Path, *, identity: str, path_text: str, keep_path: bool,
    written: str, look: Callable[[], _Looked], current: Callable[[], _Values],
    size_here: int | None,
) -> _Matched:
    """A record whose ADDRESSES agree with this file, checked for what it can cost.

    Agreeing addresses settle WHICH file this is, not whether it still holds what
    adoption left: a file replaced in place by ``cp`` keeps both its inode and
    its path, and accepting it unchecked put one recording's genre on another's
    audio (round 8). A byte change alone is no refusal either, since every
    tagging session rewrites the file. What refuses is both at once: bytes that
    are not adoption's AND a field holding a value nothing accounts for. The
    cheap field read is asked first, so the common paths read no bytes.
    """
    if _nothing_unrecorded_is_at_risk(record, written=written, current=current):
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT, so whatever is in the field
        # was put there by adoption and first-write-wins is right.
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    raise RecordCannotBeMatched(
        _a_value_nothing_recorded(record, resolved, current()), path=resolved
    )


def _record_for(
    ledger: RevertLedger, resolved: Path, *, field: str, identity: str, written: str,
    look: Callable[[], _Looked], current: Callable[[], _Values],
    size_here: int | None,
) -> _Matched | None:
    """Which record in ``ledger`` is about the file at ``resolved``, if any.

    A record says which file it is about three times: ``file`` (the volume and
    inode adoption saw), ``path``, and ``digest`` (the bytes adoption left). THE
    CLAIMS MUST CONVERGE, AND ANY DIVERGENCE THE BYTES CANNOT SETTLE IS A
    REFUSAL: refusing costs one entry with the file untouched, guessing costs a
    value in no file and no record. Every shape was measured on a real
    filesystem:

    1. No record claims the file: a first adoption, a new record, no read.
    2. One record claims it by both identity and path: which file is settled;
       :func:`_settled_or_refused` asks whether the write can destroy anything.
    3. One record claims it by identity and its recorded path still resolves to
       this file (a hardlink, a case or composition spelling): the same check.
    4. One record claims it by identity and its path is gone or another file:
       a rename or a RECYCLED inode, which only the bytes separate.
    5. One record claims it by path and the identity moved (an ``os.replace``
       save, a remount): the bytes decide.
    6. Two different records claim it, one by each: refused, never resolved.

    Two records for one file and field never reach here: :func:`read` refuses
    the whole document. A record claimed by neither address is still searched
    for by its bytes among STRANDED records (:func:`_found_by_its_bytes`), which
    is what carries a legacy ledger through a rename. A digestless record whose
    file was both renamed and re-inoded cannot be found (the residual "a record
    with no digest cannot survive a rename").
    """
    path_text = str(resolved)
    legacy = _legacy_file_id(path_text)
    claimed = [record for record in ledger.snapshots if record.field == field]
    by_identity = _one_or_none(
        [record for record in claimed if record.file in (identity, legacy)],
        resolved=resolved,
        why=(
            "two records key to this file, one under the volume and inode it has now and one "
            "under the path digest an older build wrote"
        ),
    )
    by_path = _one_or_none(
        [record for record in claimed if record.path == path_text],
        resolved=resolved,
        why="two records carry this exact path for this field",
    )

    if by_identity is None and by_path is None:
        return _found_by_its_bytes(
            ledger, resolved, field=field, identity=identity, look=look, size_here=size_here
        )

    if by_identity is not None and by_path is not None:
        if by_identity is by_path:
            return _settled_or_refused(
                by_identity,
                resolved,
                identity=identity,
                path_text=path_text,
                keep_path=True,
                written=written,
                look=look,
                current=current,
                size_here=size_here,
            )
        raise RecordCannotBeMatched(
            f"{resolved} is claimed by two different records in the revert ledger: one is "
            f"keyed to the volume and inode this file has now, and a different one carries "
            f"this path. Both cannot be about this file, and nothing here can say which is. "
            f"Both originals are still recorded and nothing has been written; what has to be "
            f"settled is the ledger.",
            path=resolved,
        )

    if by_identity is not None:
        if _live_identity(Path(by_identity.path)) == identity:
            # One file under two names, so nothing to CORRECT; whether there is
            # anything to LOSE is
            # a different question and the shape below is where it is asked.
            return _settled_or_refused(
                by_identity,
                resolved,
                identity=identity,
                path_text=path_text,
                keep_path=True,
                written=written,
                look=look,
                current=current,
                size_here=size_here,
            )
        if _the_bytes_agree(by_identity, look, size_here):
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=False
            )
        raise RecordCannotBeMatched(_an_inode_is_not_a_file(by_identity, resolved), path=resolved)

    assert by_path is not None
    if _the_bytes_agree(by_path, look, size_here):
        return _re_addressed(by_path, identity=identity, path_text=path_text, keep_path=True)
    raise RecordCannotBeMatched(_a_path_is_not_a_file(by_path, resolved), path=resolved)


def _the_bytes_agree(
    record: TagSnapshot, look: Callable[[], _Looked], size_here: int | None
) -> bool:
    """Whether the file in hand is byte for byte what this record was stamped from.

    The one corroboration moving a file cannot forge. A record with no digest
    answers FALSE: the absence of evidence is not agreement. ``size_here`` is the
    file's own size, asked against the record's, because ``look`` is a closure
    that hands :func:`_look_at` no recorded size; it saves reads and cannot
    change an answer.
    """
    if record.digest_state is not DigestState.RECORDED:
        return False
    if record.size is not None and size_here is not None and record.size != size_here:
        return False
    looked = look()
    return looked.outcome is ByteRead.ANSWERED and looked.digest == record.digest


def _the_recorded_path_is_vacant(record: TagSnapshot) -> bool:
    """Whether the recorded path is DEMONSTRABLY not holding its file any more.

    AN UNMOUNTED VOLUME IS NOT A DELETED FILE: with mere absence as the test, a
    detached FAT volume handed its file's record to a byte identical backup, and
    one user value ended in no file and no record. So the containing directory
    must be present and answering. A record whose whole directory is gone is
    then not found by its bytes (the residual "a record whose whole directory is
    gone is not searched for by its bytes").
    """
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False


def _found_by_its_bytes(
    ledger: RevertLedger, resolved: Path, *, field: str, identity: str,
    look: Callable[[], _Looked], size_here: int | None,
) -> _Matched | None:
    """A stranded record whose bytes are this file's, when no address matched.

    EVERY FILTER THAT DOES NOT NEED THE BYTES RUNS BEFORE THE BYTES ARE READ: a
    record must be able to answer (this field, a digest, a size), its recorded
    path must be VACANT, and its size must be this file's. A healthy ledger
    strands nothing, so a first adoption of eight files reads eight times, not
    fifteen.
    """
    possible = [
        record
        for record in ledger.snapshots
        if record.field == field
        and record.digest_state is DigestState.RECORDED
        and record.size is not None
    ]
    if not possible:
        return None
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None
    stranded = [record for record in same_size if record.digest == looked.digest]
    matched = _one_or_none(
        stranded,
        resolved=resolved,
        why=(
            "two stranded records were stamped from exactly these bytes, so the bytes cannot "
            "say which of them this file is"
        ),
    )
    if matched is None:
        return None
    return _re_addressed(matched, identity=identity, path_text=str(resolved), keep_path=False)


def _a_value_nothing_recorded(
    record: TagSnapshot, resolved: Path, held: _Values
) -> str:
    """The refusal for a file whose field holds something the ledger never saw."""
    return (
        f"{resolved} is the file a record in the revert ledger is about, by both its volume "
        f"and inode and its path, but the bytes are not the ones adoption left and its "
        f"{record.field!r} now holds {held!r}, which is neither the {record.original!r} that "
        f"record kept nor a value adoption has written through it. Something rewrote this "
        f"file after adoption ran: a tag edited by hand, or a different recording put here in "
        f"place. Writing over it would put a value in no file and no record, and which of the "
        f"two happened is not a fact this file carries. Nothing was written and "
        f"{record.original!r} is still recorded for {(record.path, record.field)!r}."
    )


def _an_inode_is_not_a_file(record: TagSnapshot, resolved: Path) -> str:
    """The refusal for a record keyed to this inode whose own path is elsewhere."""
    return (
        f"{resolved} has the volume and inode a record in the revert ledger is keyed to, and "
        f"that record is about {record.path!r}, which is not this file and is no longer "
        f"there. An inode number is REUSED after the file holding it is deleted, which is "
        f"ordinary on the FAT and exFAT volumes rekordbox exports to, so this is either that "
        f"file renamed or an unrelated file that inherited its number. The bytes were asked "
        f"and did not answer to what that record was stamped from, so the two cannot be told "
        f"apart from here. Nothing was written to this file and its own tag value is "
        f"untouched; the record still holds {record.original!r} for "
        f"{(record.path, record.field)!r}."
    )


def _a_path_is_not_a_file(record: TagSnapshot, resolved: Path) -> str:
    """The refusal for a record carrying this path whose recorded inode has moved."""
    return (
        f"{resolved} is the path a record in the revert ledger carries, and the volume and "
        f"inode at that path are no longer the ones that record was written from. A save "
        f"that writes a temporary file and renames it over the original moves the inode "
        f"without moving the file, and so does a remount, and so does replacing the file with "
        f"a different one. The bytes were asked and did not answer to what that record was "
        f"stamped from, so the three cannot be told apart from here. Nothing was written to "
        f"this file and its own tag value is untouched; the record still holds "
        f"{record.original!r} for {(record.path, record.field)!r}."
    )


def _record_locked(
    cfg: config.Config, resolved: Path, *, field: str, written: str, entry_id: str,
    now: datetime | None, read_field: Callable[[Path, str], _Values],
) -> tuple[RevertLedger, TagSnapshot]:
    """The record half, assuming the caller already holds the lock.

    ``look`` (the whole file) and ``current`` (one tag field) each answer once
    per call however often they are asked, and a first adoption or an ordinary
    re-run asks neither. ``size_here`` is one ``stat`` up front, so a candidate
    can be discarded without reading it.
    """
    ledger = read(cfg)
    identity = identity_of(resolved)
    look = functools.cache(lambda: _look_at(resolved))
    current = functools.cache(lambda: read_field(resolved, field))
    matched = _record_for(
        ledger, resolved, field=field, identity=identity, written=written, look=look,
        current=current,
        size_here=_size_of(resolved),
    )
    if matched is None:
        record = TagSnapshot(
            file=identity, field=field, path=str(resolved), original=current(),
            written=written, recorded=timestamp(now), entry_id=entry_id,
            entries=(entry_id,) if entry_id else (),
        )
        ledger = ledger.with_snapshot(record)
        write(cfg, ledger)
        return ledger, record
    existing = matched.now
    if matched.now is not matched.was:
        # THE ADDRESS MOVED AND THE ORIGINAL DID NOT. The old key goes before the
        # new one is added, or first-write-wins keeps the stale key and the
        # ledger holds the same original twice.
        ledger = ledger.without(frozenset({_key(matched.was)}))
        ledger = ledger.with_snapshot(existing)
        write(cfg, ledger)
    # THE ORIGINAL IS NEVER TOUCHED HERE; only the list of entries grows.
    if not entry_id or existing.written_by(entry_id):
        return ledger, existing
    amended = replace(existing, entries=(*existing.entries, entry_id))
    ledger = ledger.replacing(amended)
    write(cfg, ledger)
    return ledger, amended


def _write_one(path: Path, field: str, value: str) -> bool:
    """The default write: one value into one field, through the one writer."""
    return tags.write_tags(path, {field: value})


def _records_only(_path: Path, _field: str, _value: str) -> bool:
    """A write that does not happen, for the record half on its own."""
    return False


def snapshot_before_write(
    cfg: config.Config, path: Path | str, *, field: str, written: str, entry_id: str = "",
    now: datetime | None = None,
    read_field: Callable[[Path, str], tuple[str, ...] | None] = tags.read_tag_values,
) -> TagSnapshot:
    """Record what the file holds now, BEFORE anything writes over it.

    Returns the record in the ledger for this file and field, which after a
    re-run is the FIRST attempt's. The whole cycle, read included, is under the
    lock. THIS IS THE RECORD HALF ONLY: a caller writing the tag itself leaves a
    window a revert can land in, which :func:`write_tag_with_record` closes.
    """
    return write_tag_with_record(
        cfg, path, field=field, written=written, entry_id=entry_id, now=now,
        read_field=read_field, write_field=_records_only,
    )[0]


def write_tag_with_record(
    cfg: config.Config, path: Path | str, *, field: str, written: str, entry_id: str = "",
    now: datetime | None = None,
    read_field: Callable[[Path, str], tuple[str, ...] | None] = tags.read_tag_values,
    write_field: Callable[[Path, str, str], bool] = _write_one,
) -> tuple[TagSnapshot, bool]:
    """Record the original and write the new value, as ONE indivisible act.

    Returns the record now behind the file and whether the write landed. The
    write is INSIDE the lock so a revert cannot restore the file and empty the
    ledger between the record and the write; two applies serialize, and the
    first record still wins.

    The stamp goes on AFTER the write, so the digest a revert compares against
    is adoption's own output. A crash between the write and the stamp leaves a
    record that REFUSES and names itself for ``force`` (the residual "an
    interrupted adoption leaves a record only a human can spend").
    ``write_field`` runs inside the lock and must not take it again.
    """
    resolved = Path(path)
    with config.exclusive_lock(lock_path(cfg)):
        ledger, record = _record_locked(
            cfg, resolved, field=field, written=written, entry_id=entry_id, now=now,
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

    Keyed on the file's path AND the field, as the ledger is (:func:`_key`), so
    two fields of one file are two reasons, not one. ``failed`` carries a reason
    per pair because the ways this fails have different answers.
    """

    restored: tuple[tuple[str, str], ...] = ()
    failed: Mapping[tuple[str, str], str] = field(default_factory=dict)

    def files(self) -> tuple[str, ...]:
        """The distinct paths this revert put back, in order, for a summary."""
        return tuple(dict.fromkeys(path for path, _field in self.restored))


def restore_tag(path: Path, tag_field: str, original: tuple[str, ...] | None) -> bool:
    """Put one field back to exactly what it was, ABSENCE INCLUDED.

    Two calls, because absence is not a value: ``write_tags`` skips a None and
    reports success, and an empty string leaves a tag that was never there. The
    present branch writes every recorded value, through the module that owns
    container classification (S5).
    """
    if original is None:
        return tags.clear_tags(path, [tag_field])
    return tags.write_tag_values(path, tag_field, original)


#: The refusals about THE LEDGER rather than the file, which tell a person to
#: settle the ledger rather than offering ``force``.
_TWO_RECORDS_NAME_THIS_FILE = (
    "more than one record in this ledger names the file at that path, so which "
    "of their originals belongs to it cannot be decided from the ledger"
)
_FORCE_NAMES_MORE_THAN_ONE_RECORD = (
    "more than one record in this ledger carries that path and that field, so a "
    "force key naming them cannot say which single record it means"
)


def _cannot_say_which_record(record: TagSnapshot, why: str) -> str:
    """The refusal about the LEDGER, which deliberately offers no ``force``.

    ``force`` overrides evidence about bytes and cannot supply which record
    belongs to a file; offering it here wrote adoption's own value back as the
    original. It names no verb to run either: an instruction that cannot be
    carried out sends a person looking for the command (the residual "the
    refusal's remedy names a verb that has not landed").
    """
    return (
        f"this record cannot be spent on the file at that path: {why}. force does not apply: "
        f"it overrides evidence about the BYTES, and what is missing here is which record "
        f"belongs to this file, which is a fact about the ledger. The record is "
        f"{(record.path, record.field)!r}; every original is still recorded and nothing has "
        f"been written."
    )


def revert_tags(
    cfg: config.Config, *, entry_id: str | None = None, force: Collection[tuple[str, str]] = (),
    restore: Callable[[Path, str, tuple[str, ...] | None], bool] = restore_tag,
) -> RevertReport:
    """Put every recorded original back on disk, exactly.

    ``entry_id`` of None reverts everything; naming one reverts every record that
    entry's write went through (:meth:`TagSnapshot.written_by`, not the creator,
    since a second adoption writes through the first record).

    ``force`` NAMES THE RECORDS IT OVERRIDES, one ``(path, field)`` pair each:
    the guard is evidence, not permission, and a pass-wide flag offered per
    record overwrote every other refused file. A key naming more than one record
    overrides none, and a record whose file another record also names refuses
    before ``force`` is consulted (:func:`_cannot_say_which_record`).

    The whole pass is under the ledger's lock, so a revert and an apply are
    orderable. A False from ``restore`` is a failure. A record is dropped right
    AFTER its file is written, which narrows a crash to one stranded record whose
    ``force`` writes the same original again (the residual "an interrupted
    revert pass still strands one record"); a death inside the rewrite itself
    leaves the record and its original in place. ONE BAD RECORD COSTS ONE
    RECORD: the whole loop body is guarded, since a field the reader does not
    check against ``tags.FIELDS`` used to raise out of the pass.
    ``restore`` runs inside the lock and must not take it again.
    """
    restored: list[tuple[str, str]] = []
    failed: dict[tuple[str, str], str] = {}
    forced = {(str(path), str(field)) for path, field in force}
    _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)
    with config.exclusive_lock(lock_path(cfg)):
        ledger = read(cfg)
        selected = tuple(
            record for record in ledger.snapshots if entry_id is None or record.written_by(entry_id)
        )
        # OVER THE WHOLE LEDGER AND NOT THE SELECTION: ambiguity is a property of
        # the document, and narrowing a group of two to the one an ``entry_id``
        # matched dissolved the refusal and let the survivor's ``force`` write
        # adoption's own value back as the original.
        confused = _records_that_cannot_be_told_apart(ledger.snapshots)
        crowded = _paths_more_than_one_record_carries(ledger.snapshots)
        for record in selected:
            reported = (record.path, record.field)
            if _key(record) in confused:
                failed[reported] = _cannot_say_which_record(record, _TWO_RECORDS_NAME_THIS_FILE)
                continue
            if reported in forced and _key(record) in crowded:
                failed[reported] = _cannot_say_which_record(
                    record, _FORCE_NAMES_MORE_THAN_ONE_RECORD
                )
                continue
            try:
                refusal = _revert_one(record, reported in forced, restore=restore)
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
    """Which file is at ``path`` right now, or None (comparable with nothing).

    Never a fallback derived from the path, which would bring back the identity
    scheme this one replaced.
    """
    try:
        return identity_of(path)
    except AdoptedFileUnidentifiable:
        return None


def _sharing(
    records: tuple[TagSnapshot, ...], key_of: Callable[[TagSnapshot], tuple[str | None, str]]
) -> _Keys:
    """The records whose ``key_of`` another record shares; a key opening with None
    shares nothing, and a group of one is never shared.
    """
    groups: dict[tuple[str | None, str], list[TagSnapshot]] = {}
    for record in records:
        found = key_of(record)
        if found[0] is not None:
            groups.setdefault(found, []).append(record)
    return frozenset(
        _key(member) for members in groups.values() if len(members) > 1 for member in members
    )


def _records_that_cannot_be_told_apart(selected: tuple[TagSnapshot, ...]) -> _Keys:
    """The records whose file another record in the LEDGER also names.

    Always passed the whole ledger (see :func:`revert_tags`). Ledgers already on
    disk hold such pairs (a hardlink, a case spelling, a rename, an
    ``os.replace`` save), and restoring them in order restores the original and
    then offers to overwrite it with adoption's value. THE WHOLE GROUP REFUSES:
    picking the member with the live identity put one key in ``restored`` AND
    ``failed``. A group of one is never confused, which keeps legacy ledgers
    working.
    """
    return _sharing(selected, lambda record: (_live_identity(Path(record.path)), record.field))


def _paths_more_than_one_record_carries(selected: tuple[TagSnapshot, ...]) -> _Keys:
    """The records a ``(path, field)`` force key could not have meant uniquely.

    ``force`` is keyed on what a person can type, which is not unique, and two
    records on one path were both overridden against the message's promise of
    "this ONE record". This set and the confused one overlap completely or not
    at all.
    """
    return _sharing(selected, lambda record: (record.path, record.field))


def _bring_the_bytes_within_reach(
    cfg: config.Config, *, entry_id: str | None, forced: Collection[tuple[str, str]]
) -> None:
    """Read every file this pass will ask about, BEFORE the lock, and DECIDE NOTHING.

    Reading here makes a provider materialize an evicted file, so the read under
    the lock is local and one download does not block an unrelated apply. Its
    answer is discarded: a read validated later by ``stat`` values spent stale
    bytes after a same-length rewrite inside one FAT time tick. It costs two
    reads per record the guard will read (the residual "a revert hashes every
    file it considers"), is best effort in every direction, and goes through
    :func:`_look_at` so a FIFO costs nothing here either.
    """
    try:
        ledger = read(cfg)
    except RevertLedgerUnreadable:
        return
    for record in ledger.snapshots:
        if (
            (entry_id is None or record.written_by(entry_id))
            and record.digest_state is DigestState.RECORDED
            and (record.path, record.field) not in forced
        ):
            _look_at(Path(record.path), recorded_size=record.size)


def _revert_one(
    record: TagSnapshot, forced: bool, *, restore: Callable[[Path, str, _Values], bool]
) -> str | None:
    """Put one record's original back. None on success, else why not."""
    target = Path(record.path)
    if not target.exists():
        return "the file is no longer there"
    if not forced:
        replaced = _changed_since_adoption(record, target)
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
    "RecordCannotBeMatched",
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
