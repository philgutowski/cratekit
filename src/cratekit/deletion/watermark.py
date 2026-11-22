"""How far the deletion pass has read THIS library's removals, and what binds it.

R24 (no routine pass over the whole library) and R35 (a first run BASELINES prior
removals) are this file: rekordbox stamps every changed row with an update
sequence, so "removals since the last run" is a comparison against one number.

**IT IS BOUND TO A DATABASE IDENTITY.** A rebuilt library's counter restarts near
zero, so a carried over watermark would report nothing to do forever; the
identity turns that into a re-baseline.

**IT ADVANCES ONLY OVER WHAT IS FULLY HANDLED, AND ONLY CONTIGUOUSLY.** It stops
BEFORE the first sequence holding anything unhandled (R35, AE16): two rows can
share a sequence, and passing it would skip the unhandled one for good.

**IT NUMBERS A REMOVAL THAT CARRIES NO NUMBER OF ITS OWN (R-1037).** A row deleted
outright has no sequence, so the update count at the FIRST run that sees it
absent is kept here, read back by later runs, and forgotten when the row is held
again. A landing rolled back is told apart first (``library.landed_absences``).

**THE READ AND THE WRITE ARE ONE LOCKED CYCLE.** An atomic rename does nothing for
two passes advancing from one read (the decision stores lost 122 of 200 records
so). The lock is a NEVER_RESTORED entry of its own, because the document is
COUPLED and a restore would swap a lock beside it under its holders.

Layer note: MODULES. It reads configuration and touches the disk, and it names no
verb.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

#: The version this module writes, and READS BACK (a stamp nobody reads proves
#: nothing). Version 2 added the sightings (R-1037); version 1 reads as none.
WATERMARK_VERSION = 2
READABLE_VERSIONS = frozenset({1, WATERMARK_VERSION})

#: "No baseline", distinct from a real counter sitting at zero.
UNBASELINED = -1


@dataclass(frozen=True, slots=True)
class Watermark:
    """One recorded position, and the database it is a position in.

    ``sequence`` is the highest update sequence every removal at or below which
    is fully handled; a removal is offered when its own is strictly greater.
    """

    database_identity: str
    sequence: int
    recorded: str
    actor: str
    #: The sequence each absent landed row was given at its first sighting, by
    #: content id (R-1037), bound to ``database_identity`` with the position.
    absent: Mapping[str, int] = field(default_factory=dict)

    def applies_to(self, database_identity: str) -> bool:
        """Whether this position means anything for the database in front of us.

        Exact: another identity's sequence space is noise, not an approximation.
        """
        return self.database_identity == str(database_identity)

    def to_json(self) -> dict[str, Any]:
        return {
            "database_identity": self.database_identity,
            "sequence": self.sequence,
            "recorded": self.recorded,
            "actor": self.actor,
            "absent": dict(sorted(self.absent.items())),
        }


def contiguous_sequence(
    handled: Mapping[int, bool] | Sequence[tuple[int, bool]], *, floor: int
) -> int:
    """The highest sequence at or below which EVERYTHING is handled.

    Pairs, because several rows may share a sequence and one outstanding row
    holds it; a mapping is accepted too. Never below ``floor``, the recorded
    watermark: moving back would re-present answered removals.
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

    def _unusable(self, what: str) -> CratekitError:
        """One refusal for every way this document is not this document; the shape
        rides on the detail."""
        return refuse(
            "deletion-watermark-unusable",
            f"the deletion watermark at {self.path.name} could not be read ({what}), so how much "
            "of this library's removal history has already been dealt with is unknown; treating "
            "it as unset would present every removal this library has ever had as if it had just "
            "happened",
            steps=("repair or restore the deletion watermark before running deletion",),
            scope=Scope.RUN,
            origin=("deletion.watermark",),
            detail={"problem": what, "path": str(self.path)},
        )

    def _locked(self):
        """Hold the exclusive lock across one read then write cycle (``core.config.held``).

        Only the acquisition is translated into this module's refusal.
        """
        return config.held(
            self.lock_path,
            lambda exc: refuse(
                "deletion-watermark-unusable",
                f"the deletion watermark could not be locked ({exc}), and "
                f"advancing it unlocked discards whatever a second pass is "
                f"recording at the same time, silently, while reporting success",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=("deletion.watermark",),
                detail={"lock": str(self.lock_path)},
            ),
        )

    def read(self) -> Watermark | None:
        """The recorded position, or None when no document exists.

        A document that exists and cannot be recognised REFUSES, never None: a
        corrupt one read as absent would re-baseline at today's sequence and lose
        every unanswered removal.
        """
        found, raw = config.read_json_as_text(self.path, self._unusable)
        if not found:
            return None
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> Watermark:
        """Turn a parsed document into a position, or refuse. Positively, field by field."""
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a watermark")
        version = raw.get("version")
        if isinstance(version, bool) or version not in READABLE_VERSIONS:
            raise self._unusable(
                f"it says version {version!r} and this build writes {WATERMARK_VERSION}"
            )
        identity = raw.get("database_identity")
        if not isinstance(identity, str) or not identity:
            raise self._unusable("it names no database identity")
        sequence = raw.get("sequence")
        # bool before int: ``True`` is an int and would read as sequence 1.
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            raise self._unusable(
                f"its sequence is a {type(sequence).__name__} rather than a whole number"
            )
        absent = raw.get("absent", {})
        if not isinstance(absent, Mapping):
            raise self._unusable(f"its sightings are a {type(absent).__name__}, not a mapping")
        for content_id, sighted in absent.items():
            if not isinstance(content_id, str) or not content_id:
                raise self._unusable("a sighting names no content id")
            if isinstance(sighted, bool) or not isinstance(sighted, int):
                raise self._unusable(
                    f"the sighting of {content_id!r} is a {type(sighted).__name__} "
                    f"rather than a whole number"
                )
        return Watermark(
            database_identity=identity,
            sequence=sequence,
            recorded=str(raw.get("recorded") or ""),
            actor=str(raw.get("actor") or ""),
            absent=dict(absent),
        )

    def _write(self, mark: Watermark) -> None:
        payload = {"version": WATERMARK_VERSION, **mark.to_json()}
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), self.path
        )

    def baseline(
        self, *, database_identity: str, sequence: int, actor: str, now: str | None = None
    ) -> tuple[Watermark, bool]:
        """Record a starting position if this library needs one. Returns (mark, baselined).

        ``baselined`` is what the pass reports: history accepted, not nothing to
        delete (R35). The whole decision is under the lock, or two first runs
        could both baseline. A document of a DIFFERENT database is replaced, the
        re-baseline R35 describes.
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

        Re-read inside the lock and the greater kept, since another pass may have
        advanced meanwhile. A document of a DIFFERENT database refuses: the
        library was rebuilt between the plan and here.
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
                absent=dict(existing.absent) if existing is not None else {},
            )
            self._write(mark)
            return mark

    def sight(
        self, *, database_identity: str, absent: Iterable[str], present: Iterable[str], counter: int
    ) -> Watermark:
        """Number every absent landed row not yet numbered, and forget every one held again.

        A row first seen is numbered at ``counter``, past every earlier run's; on
        the baselining run that is at or under the new position, so it is
        history (R35). A numbered row keeps its number. A row in ``present`` (held
        live or marked) is dropped, so its next removal is new. Under the lock,
        refusing another database's document as :meth:`advance` does.
        """
        with self._locked():
            existing = self.read()
            if existing is None or not existing.applies_to(database_identity):
                raise self._unusable(
                    "it holds no position for the database this run read, so an "
                    "absent row has nothing to be numbered against"
                )
            held = {str(one) for one in present}
            kept = {key: value for key, value in existing.absent.items() if key not in held}
            for content_id in absent:
                if content_id in kept or content_id in held:
                    continue
                kept[str(content_id)] = int(counter)
            if kept == dict(existing.absent):
                return existing
            mark = replace(existing, absent=kept)
            self._write(mark)
            return mark
