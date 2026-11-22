"""The decision stores: declines and tombstones that suppress a candidate.

Split from ``core.review`` to keep each module readable; every name here is
imported back into ``core.review`` and used from there, and only
``core.review`` imports this module, at its foot.
"""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli.output import canonical_json, timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import (
    SUPPRESSION_ID_PREFIX,
    _own_only,
    normalize_identity,
    normalize_kind,
)

# ---------------------------------------------------------------------------
# The decision stores: declines and tombstones
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Suppression:
    """One recorded decision that suppresses something, and its revocation.

    The same record shape as a review item, minus the candidates, because the
    question has already been answered. A revoked decision is KEPT with its
    revocation recorded rather than deleted: R36 requires a tombstone to be
    listable and revocable, and a store that forgets a revocation cannot report
    that the suppression ever existed.
    """

    suppression_id: str
    kind: str
    payload: Mapping[str, Any]
    actor: str
    recorded: str
    #: What the identifier was derived from, kept for the reason a review item
    #: keeps its own: an identifier nobody can trace back cannot be audited, so a
    #: collision and a duplicate look exactly alike afterwards. Optional, because
    #: a record written before this field existed is still a valid record.
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


#: The version of the DOCUMENT a decision store writes. Its own constant rather
#: than the export's, for the reason the export has one separate from the queue's
#: schema: these are three formats with three sets of readers, and coupling any
#: two of them forces a bump on people holding the third.
DECISION_STORE_VERSION = 1


def decision_store_keys() -> tuple[str, ...]:
    """The state entries that ARE decision stores, read from the inventory.

    DERIVED, not transcribed. This was a literal pair with a docstring saying it
    came from the inventory, which is P3's failure exactly: the name claimed a
    derivation and the code was a list, so a store added to the inventory would
    not appear here and a store removed from it would leave this module resolving
    a path nobody declared a root for. R35's declines and R36's tombstones are the
    two the plan names, and the inventory is where that is now written down.
    """
    return tuple(sorted(entry.key for entry in config.STATE_FILES if entry.decision_store))


#: The same set as a constant, for callers that read it as one. Computed once at
#: import from the inventory rather than spelled, so the two cannot disagree.
DECISION_STORE_KEYS: tuple[str, ...] = decision_store_keys()


class DecisionStore:
    """A revocable set of suppressions, on one of the declared state entries.

    It shares the review item's record shape and its identity rule: a decision is
    addressed by a content derived identifier, never by a display name, so the
    thing suppressed can be renamed without the suppression being orphaned.

    It is a document rather than a database, and that is a deliberate difference
    from the queue rather than an inconsistency. The state inventory declares each
    of these as one file; a queue is paged through by a person and written by two
    processes at once, while a decision store is read whole by an acquisition pass
    to answer "is this suppressed".

    A DOCUMENT IS NOT AN EXCUSE FOR A SINGLE WRITER, and this class used to assert
    one that nothing enforced and nothing in this product establishes. Recording
    and revoking are both a read then a write over one file, and
    ``atomic_write_bytes`` makes the RENAME atomic and does nothing for the cycle
    around it: two processes both read the same set, both add their own record,
    and the second rename discards the first one's while the call that lost
    returns a record reporting success. Eight processes recording twenty five
    decisions each left seventy one of two hundred on the disk. So every cycle
    here is taken under a sibling lock, which is what the queue next door gets
    from ``BEGIN IMMEDIATE``.
    """

    def __init__(self, key: str, cfg: config.Config) -> None:
        if key not in DECISION_STORE_KEYS:
            raise refuse(
                "review-queue-undeclared",
                f"{key!r} is not a declared decision store; declared: "
                f"{', '.join(DECISION_STORE_KEYS)}",
                steps=("declare the store in the state inventory before writing it",),
                scope=Scope.RUN,
                origin=("review",),
                detail={"key": key, "declared": list(DECISION_STORE_KEYS)},
            )
        self.key = key
        self.path = config.state_path(key, cfg)
        #: The sibling lock, on a NEVER_RESTORED entry of its own rather than
        #: beside the document. The stores are COUPLED, so a restore replaces the
        #: directory holding them, and a lock inside it would have its inode
        #: swapped under every process holding it, which is exclusion disappearing
        #: mid-session with nothing raised.
        self.lock_path = config.state_path("decision_store_locks", cfg) / f"{key}.lock"

    def _unusable(self, what: str, exc: BaseException | None = None) -> CratekitError:
        """One refusal for every way this document is not this document.

        The message is the same sentence in each case on purpose: what a person
        does about it does not depend on WHICH way the file is wrong, and the
        specific shape rides on the detail where a bug report can read it.
        """
        return refuse(
            "review-file-unusable",
            f"the {self.key} store at {self.path.name} could not be read ({what}), "
            f"so what it suppresses is unknown; treating it as empty would "
            f"re-acquire exactly what somebody removed on purpose",
            steps=("repair or restore the store before running anything that consults it",),
            scope=Scope.RUN,
            origin=("review",),
            detail={"store": self.key, "problem": what},
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        """Hold the sibling lock across one read then write cycle.

        BLOCKING, like the queue's busy timeout: two processes recording
        decisions should serialize rather than raise at a person. The lock file
        persists after release, deliberately, for the reason the config lock
        states at length: unlinking the name lets a second process take a lock on
        a fresh inode while the first still holds the old one, and both then
        believe they hold the only lock with nothing raised.

        A PLATFORM WITH NO ADVISORY LOCKING REFUSES, which is the config lock's
        decision and not a new one. Proceeding unlocked is the behaviour being
        fixed, so degrading to it on the platform where the fix cannot be applied
        would leave exactly the defect, reachable by anybody on that platform.
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
                scope=Scope.RUN,
                origin=("review",),
                detail={"store": self.key, "lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            handle.close()

    def _read(self) -> dict[str, Suppression]:
        """Load the store, treating anything it cannot RECOGNIZE as a refusal.

        An unreadable suppression list read as empty un-suppresses everything in
        it, silently, and the next acquisition pass then re-acquires exactly what
        somebody deleted on purpose. The gate half of U8's lesson applies here
        too: a tolerant reader on a path that governs an action fails open.

        REFUSAL IS THE ONLY ALTERNATIVE TO A CORRECT READ, and that is what this
        was missing. The guard covered the case where ``json.loads`` itself
        raised, so every document that was good JSON and was not this store fell
        through to an empty mapping: a top level list, a scalar, a version this
        build does not know, ``decisions`` present and null, a record whose
        identifier key had been renamed. Each one reported that the store
        suppressed nothing, and the empty result was then handed to the writer, so
        ONE further record deleted every prior decline from the disk.
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
            # A version stamped and never read is a version that proves nothing,
            # which is what this file had: the queue refuses on
            # review-schema-mismatch and an import refuses on a version mismatch,
            # and the third sibling wrote a version and ignored it.
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
                # Outside the try in the previous version, so this left as an
                # uncaught type error from inside ``suppresses``, which an
                # acquisition pass asks once per candidate.
                raise self._unusable(f"record {position} has a payload that is not a mapping")
            if entry.get("identity") is not None and not isinstance(entry["identity"], Mapping):
                raise self._unusable(f"record {position} has an identity that is not a mapping")
            suppression = Suppression.from_json(entry)
            found[suppression.suppression_id] = suppression
        return found

    def _write(self, recorded: Mapping[str, Suppression]) -> None:
        payload = {
            "version": DECISION_STORE_VERSION,
            "store": self.key,
            "decisions": [recorded[key].to_json() for key in sorted(recorded)],
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), self.path
        )

    def record(
        self,
        *,
        kind: str,
        identity: Mapping[str, Any],
        payload: Mapping[str, Any] | None = None,
        actor: str,
        beside: Sequence[tuple[str, Mapping[str, Any], Mapping[str, Any]]] = (),
    ) -> Suppression:
        """Suppress something, idempotently, and return the record.

        Re-recording an already suppressed thing changes nothing, including its
        timestamp. Re-recording a REVOKED one re-suppresses it, which is the only
        way a person changes their mind back.

        ``beside`` IS FOR ONE DECISION THAT IS SEVERAL RECORDS, each a (kind,
        identity, payload). They are written IN THE SAME WRITE as this record and
        ONLY WHEN THIS RECORD IS WRITTEN. One write, because a caller that undoes
        its work when this raises would otherwise be left with the first record
        standing and the thing it suppresses put back. Only then, because a
        record that already stood is a decision already taken, and a companion a
        person has since lifted on its own must not come back behind their back.
        A companion that already stands is left exactly as it is.

        THE WHOLE CYCLE IS UNDER THE LOCK. The read decides what the write
        contains, so a lock taken around only the write protects nothing: the
        losing process still writes a set it read before the winner's record
        existed, and the record it drops is a decline that will now be offered
        again or a tombstone that will now be re-acquired.
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
                    suppression_id=other_id,
                    kind=normalize_kind(other_kind),
                    identity=normalize_identity(other_identity),
                    payload=dict(other_payload or {}),
                    actor=actor,
                    recorded=suppression.recorded,
                )
            self._write(recorded)
            return suppression

    def revoke(
        self,
        suppression_id: str,
        *,
        actor: str,
        also: Callable[[Suppression, Mapping[str, Suppression]], Iterable[str]] | None = None,
    ) -> Suppression:
        """Lift a suppression, keeping the record of it having existed.

        Under the lock for the same reason ``record`` is, and the cost of losing
        one is worse: a dropped revocation leaves a suppression standing forever,
        and nothing ever offers the thing again, so nobody finds out.

        ``also`` NAMES THE OTHER RECORDS THAT GO WITH THIS ONE, and it is asked
        UNDER THE LOCK, with the records this write is about to replace. A caller
        that read the store, decided, and then revoked twice would be deciding
        from a set another process may have added to in between, which is the
        read outside the lock ``record`` argues against. They are lifted in the
        same write, so there is no half lifted state to be interrupted in. An
        identifier it names that is unknown or already lifted is passed over.
        """
        with self._locked():
            recorded = self._read()
            existing = recorded.get(suppression_id)
            if existing is None:
                raise refuse(
                    "review-item-unknown",
                    f"no {self.key} record has the identifier {suppression_id!r}",
                    steps=("list the store and take the identifier from it",),
                    scope=Scope.RUN,
                    origin=("review",),
                    detail={"store": self.key, "suppression_id": suppression_id},
                )
            if not existing.suppressing:
                return existing
            lifted_at = timestamp()

            def lifted(one: Suppression) -> Suppression:
                return Suppression(
                    suppression_id=one.suppression_id,
                    kind=one.kind,
                    identity=one.identity,
                    payload=one.payload,
                    actor=one.actor,
                    recorded=one.recorded,
                    revoked=True,
                    revoked_at=lifted_at,
                    revoked_by=actor,
                )

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
        """Whether this store currently suppresses that thing.

        Asked by an acquisition pass per candidate. It reports the suppression
        rather than omitting the candidate silently (R36), which is the caller's
        job; what this owes is a truthful answer, including a refusal when the
        store cannot be read.
        """
        found = self._read().get(suppression_id_for(self.key, kind, identity))
        return found is not None and found.suppressing

    def suppressions(self, *, include_revoked: bool = False) -> tuple[Suppression, ...]:
        """Every record, suppressing ones only unless asked for the rest.

        R36 says a tombstone is LISTABLE and revocable, and the two halves need
        each other: a revoked record that vanished from the listing would leave a
        person unable to tell "never suppressed" from "suppressed and lifted".
        """
        found = self._read()
        return tuple(
            found[key]
            for key in sorted(found)
            if include_revoked or found[key].suppressing
        )


def suppression_id_for(store_key: str, kind: str, identity: Mapping[str, Any]) -> str:
    """The stable identifier for one suppression. Same rule as a review item.

    Same NORMALIZATION too, and it matters more here: the deletion pass asks
    ``suppresses`` once per candidate, and a spelling difference between the pass
    that recorded the decline and the pass that consults it re-offers a file
    somebody deliberately declined.
    """
    if not identity:
        raise refuse(
            "review-selection-invalid",
            "a suppression needs an identity to be addressed by; an empty one "
            "collapses every record in the store onto a single entry",
            remedy=Remedy.REPORT_DEFECT,
            origin=("review",),
            detail={"store": store_key, "kind": kind},
        )
    digest = hashlib.sha256(
        canonical_json(
            {
                "store": store_key,
                "kind": normalize_kind(kind),
                "identity": normalize_identity(identity),
            }
        ).encode()
    ).hexdigest()
    return f"{SUPPRESSION_ID_PREFIX}_{digest[:24]}"
