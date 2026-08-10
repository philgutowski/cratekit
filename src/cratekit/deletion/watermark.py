"""How far the deletion pass has read THIS library's removals, and what binds it.

R24 says no routine operation processes the whole library in one pass, and R35
says a first run on an existing library BASELINES prior removals rather than
presenting them. Both of those are this file. rekordbox stamps every row it
changes with an update sequence, so "the removals since the last run" is a
comparison against one number, and the number is what this document holds.

Three properties, and each one exists because its absence has a specific cost.

**IT IS BOUND TO A DATABASE IDENTITY.** A watermark is a position in one
database's sequence space, and it means nothing in another's. Somebody who
rebuilds their library from an export gets a database whose counter starts near
zero, so a watermark carried over from the old one sits above every sequence the
new database will issue for a long time, and the pass reports nothing to do
forever while removals pile up invisibly. Recording the identity the number was
taken against turns that from a silent nothing into a re-baseline.

**IT ADVANCES ONLY OVER WHAT IS FULLY HANDLED, AND ONLY CONTIGUOUSLY.** The pass
answers each removal with a category, and only some of those categories are
finished business. An unresolved row is not finished: R35 and AE16 both say so by
name, and advancing past it would hide a file the user still owns behind a number
nobody looks at. So the advance stops at the first sequence holding anything
unhandled, and it stops BEFORE it, not after: two rows can share one sequence,
and advancing to a sequence that still has an unhandled row on it skips that row
on the next run, permanently.

**THE READ AND THE WRITE ARE ONE LOCKED CYCLE.** ``atomic_write_bytes`` makes the
rename atomic and does nothing for the cycle around it. Two passes finishing at
once both read the same watermark, both advance from what they read, and the
second rename discards the first one's advance while the call that lost returns a
record reporting success. That is the same defect the decision stores shipped and
lost 122 of 200 decisions to, one package away, and it is worse here because the
losing advance re-offers files a person has already answered for. The lock is a
NEVER_RESTORED entry of its own rather than a file beside the document, because
the document is COUPLED: a restore replaces the directory holding it, and a lock
inside that directory has its inode swapped under every process holding it.

Layer note: MODULES. It reads configuration and touches the disk, and it names no
verb.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

#: The version of the document this module writes, and READS BACK. A version
#: stamped and never read proves nothing, which is exactly what the decision
#: store next door had wrong: it wrote one into every document and its reader
#: never looked, so a document from a newer build read as an empty store and the
#: next write destroyed it.
WATERMARK_VERSION = 1

#: The sequence a library that has never been baselined is at. Named rather than
#: written as a bare zero at three call sites, because the number and the meaning
#: are not the same thing: this is "no baseline", and a real library whose
#: counter genuinely sits at zero is still a library that has been baselined.
UNBASELINED = -1


@dataclass(frozen=True, slots=True)
class Watermark:
    """One recorded position, and the database it is a position in.

    ``sequence`` is the highest update sequence every removal at or below which
    has been fully handled. A removal is offered when its own sequence is
    strictly greater, so a sequence that is merely present in the document is not
    a claim that anything at it was deleted; it is a claim that nothing at it is
    still outstanding.
    """

    database_identity: str
    sequence: int
    recorded: str
    actor: str

    def applies_to(self, database_identity: str) -> bool:
        """Whether this position means anything for the database in front of us.

        The comparison is exact. A near miss is not a near answer: two libraries
        with different identities have unrelated sequence spaces, so a watermark
        from one is not an approximation of the other's, it is noise.
        """
        return self.database_identity == str(database_identity)

    def to_json(self) -> dict[str, Any]:
        return {
            "database_identity": self.database_identity,
            "sequence": self.sequence,
            "recorded": self.recorded,
            "actor": self.actor,
        }


def contiguous_sequence(
    handled: Mapping[int, bool] | Sequence[tuple[int, bool]],
    *,
    floor: int,
) -> int:
    """The highest sequence at or below which EVERYTHING is handled.

    Takes (sequence, handled) pairs rather than candidates, so the rule is
    testable without a library and so the one thing it decides stays visible: it
    decides nothing about what handled MEANS, which is the categoriser's job.

    A mapping is accepted as well as pairs because a caller that already has one
    entry per sequence should not have to flatten it, and a mapping of one
    sequence to one verdict cannot express the case this function exists for.
    Pairs can, so pairs are what the pass passes: several rows may share one
    sequence, and if any of them is outstanding the sequence is not clear.

    ``floor`` is where it starts, which is the watermark already recorded. The
    result never goes below it, because a watermark that moved backwards would
    re-present removals a person has already answered for, and the answer they
    already gave is not in the queue any more.
    """
    pairs = list(handled.items()) if isinstance(handled, Mapping) else list(handled)
    outstanding = sorted({sequence for sequence, done in pairs if not done})
    reached = floor
    for sequence in sorted({sequence for sequence, _done in pairs}):
        if outstanding and sequence >= outstanding[0]:
            break
        reached = max(reached, sequence)
    return reached


class WatermarkStore:
    """The deletion watermark, as one locked document on a declared state entry."""

    def __init__(self, cfg: config.Config) -> None:
        self.path: Path = config.state_path("deletion_watermark", cfg)
        self.lock_path: Path = config.state_path("deletion_watermark_lock", cfg)

    # The refusals.

    def _unusable(self, what: str) -> CratekitError:
        """One refusal for every way this document is not this document.

        The sentence is the same in each case deliberately, as its sibling in the
        decision stores argues: what a person does about it does not depend on
        WHICH way the file is wrong, and the specific shape rides on the detail
        where a bug report can read it.
        """
        return refuse(
            "deletion-watermark-unusable",
            f"the deletion watermark at {self.path.name} could not be read "
            f"({what}), so how much of this library's removal history has "
            f"already been dealt with is unknown; treating it as unset would "
            f"present every removal this library has ever had as if it had just "
            f"happened",
            steps=("repair or restore the deletion watermark before running deletion",),
            scope=Scope.RUN,
            origin=("deletion.watermark",),
            detail={"problem": what, "path": str(self.path)},
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        """Hold the exclusive lock across one read then write cycle.

        The lock class is the one ``core.config`` already ships for precisely
        this, rather than a fourth copy of the same twenty lines: it opens the
        file at an explicit mode inside a private directory, it never unlinks the
        name on release, and it REFUSES rather than proceeding unlocked on a
        platform with no advisory locking. Only the acquisition is translated
        into this module's own refusal; a failure raised by the body keeps its
        own identity.
        """
        lock = config._exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "deletion-watermark-unusable",
                f"the deletion watermark could not be locked ({exc}), and "
                f"advancing it unlocked discards whatever a second pass is "
                f"recording at the same time, silently, while reporting success",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=("deletion.watermark",),
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            lock.__exit__(None, None, None)

    # Reading.

    def read(self) -> Watermark | None:
        """The recorded position, or None when this library has never been baselined.

        REFUSAL IS THE ONLY ALTERNATIVE TO A CORRECT READ. None means one thing
        here, "no document exists", and a document that exists and cannot be
        recognized is never folded into it. The two have opposite consequences: a
        library with no document gets baselined and offered nothing, while a
        library whose document is corrupt would be baselined at TODAY's sequence
        and would silently lose every removal a person had not yet answered for.
        """
        if not self.path.exists():
            return None
        try:
            text = self.path.read_text()
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        try:
            raw = json.loads(text)
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> Watermark:
        """Turn a parsed document into a position, or refuse. Positively, field by field."""
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a watermark")
        version = raw.get("version")
        if version != WATERMARK_VERSION:
            raise self._unusable(
                f"it says version {version!r} and this build writes {WATERMARK_VERSION}"
            )
        identity = raw.get("database_identity")
        if not isinstance(identity, str) or not identity:
            raise self._unusable("it names no database identity")
        sequence = raw.get("sequence")
        # bool BEFORE int, because a bool IS an int in Python and ``True`` would
        # otherwise be accepted as the sequence 1.
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            raise self._unusable(
                f"its sequence is a {type(sequence).__name__} rather than a whole number"
            )
        return Watermark(
            database_identity=identity,
            sequence=sequence,
            recorded=str(raw.get("recorded") or ""),
            actor=str(raw.get("actor") or ""),
        )

    def _write(self, mark: Watermark) -> None:
        payload = {"version": WATERMARK_VERSION, **mark.to_json()}
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), self.path
        )

    # Writing.

    def baseline(
        self, *, database_identity: str, sequence: int, actor: str, now: str | None = None
    ) -> tuple[Watermark, bool]:
        """Record a starting position if this library needs one. Returns (mark, baselined).

        ``baselined`` is True when this call WROTE one, which is what the pass
        reports to the user: a first run presents nothing, and saying so is the
        difference between "there is nothing to delete" and "the history before
        now has been accepted as history" (R35).

        THE WHOLE DECISION IS UNDER THE LOCK, not just the write. The read is what
        decides whether to write at all, so a lock around the write alone would
        let two first runs both decide to baseline, and the second would overwrite
        a position the first had already advanced.

        A document belonging to a DIFFERENT database is replaced rather than
        refused. That is the re-baseline R35's first-run rule already describes,
        arriving by a different route: the sequence space it named is gone, and
        the only honest thing to do with a number measured in it is to stop using
        it. The old identity rides on the returned record's actor trail through
        the caller's report, so a person is told it happened.
        """
        with self._locked():
            existing = self.read()
            if existing is not None and existing.applies_to(database_identity):
                return existing, False
            mark = Watermark(
                database_identity=str(database_identity),
                sequence=int(sequence),
                recorded=now or timestamp(),
                actor=actor,
            )
            self._write(mark)
            return mark, True

    def advance(
        self, *, database_identity: str, sequence: int, actor: str, now: str | None = None
    ) -> Watermark:
        """Move the position forward, never backward, under the lock.

        THE STORED POSITION IS RE-READ INSIDE THE LOCK and the result is the
        greater of the two. The caller computed its number from a document it read
        before it did its work, and another pass may have advanced past it
        meanwhile; writing the caller's number unconditionally would then undo
        that advance and re-offer everything between.

        A document naming a DIFFERENT database refuses. Between the plan and the
        advance somebody rebuilt the library, so the sequence about to be written
        was measured in a space that no longer exists, and the removals it claims
        are handled are not the removals the new database will issue.
        """
        with self._locked():
            existing = self.read()
            if existing is not None and not existing.applies_to(database_identity):
                raise self._unusable(
                    f"it was recorded against database {existing.database_identity!r} "
                    f"and this run read database {str(database_identity)!r}"
                )
            reached = max(int(sequence), existing.sequence if existing is not None else UNBASELINED)
            mark = Watermark(
                database_identity=str(database_identity),
                sequence=reached,
                recorded=now or timestamp(),
                actor=actor,
            )
            self._write(mark)
            return mark


__all__ = [
    "UNBASELINED",
    "WATERMARK_VERSION",
    "Watermark",
    "WatermarkStore",
    "contiguous_sequence",
]
