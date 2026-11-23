"""Whether a database-native tree still matches what this library declares (U36).

Once a tree cuts over the database is the only copy of its membership, so a
database put back to an earlier state leaves the tree short, and incremental
sync cannot close the gap because the orphaned files still read as owned.

A Cratekit restore is not the case: KTD21b captures this record with the
database, so they agree. The case is a database recovered OUT OF BAND. It is
detected from rekordbox's local update count: a count that went backward, or
rows that moved while it stood still, is a database that went backward, while
ordinary use moves both forward together and stays silent (P7). A SIDEWAYS
copy with a higher count is not detected (P4).

An unconverged tree refuses only its own writes, and a difference nothing can
derive is disposed of by tree, by a named person, in the record.

LAYER: infrastructure. It names no verb (D2) and no display name (R19).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import config, rb_writer, tree_registry
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The state entry this module owns.
STATE_KEY = "tree_convergence"

#: The lock serializing every read-modify-write of the entry above, a declared
#: entry so the inventory knows it.
LOCK_KEY = "tree_convergence_lock"

#: Bumped only on an incompatible change; a newer file is refused, not guessed.
SCHEMA_VERSION = 1

#: The column rekordbox soft-deletes with, filtered AT THE DATABASE so a moved
#: column raises instead of counting tombstones. A third unshared spelling,
#: since sharing ``cratekit.write.trees.soft_delete_marker`` would be an upward
#: import (KTD23); if a fourth appears, hoist it into the foundation.
SOFT_DELETE_COLUMN = "rb_local_deleted"


def _refuse(reason: str, message: str, **fields: Any) -> CratekitError:
    """``refuse`` with the run scope and this module's origin, which every refusal here carries."""
    return refuse(reason, message, scope=Scope.RUN, origin=("convergence",), **fields)


class Purpose(StrEnum):
    """What a governed database write is FOR. Two answers, one pair of gates apart.

    Not an override: a ``REBUILD`` write keeps every other guard and is spared
    only the two latches whose own remedy is a rebuild, so the product never
    refuses the rebuild it asked for. Named ``Purpose`` because ``Intent`` is
    taken one package away. ``ROUTINE``, the restrictive answer, is the default.
    """

    ROUTINE = "routine"
    REBUILD = "tree-rebuild"


class Regression(StrEnum):
    """How the database went backward. Two shapes, recorded separately."""

    #: The local update count is lower than the one recorded at the last close.
    SEQUENCE_WENT_BACKWARD = "sequence-went-backward"

    #: The active row count moved while the update count did not, which
    #: rekordbox cannot do in one database.
    ROWS_MOVED_AT_A_STANDSTILL = "rows-moved-at-a-standstill"


class ConvergenceStateUnreadable(CratekitError):
    """The convergence record exists and cannot be understood.

    Never collapsed into "nothing is unconverged", the permissive reading. A
    ``CratekitError`` so the remedy survives the boundary (S4).
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="tree-convergence-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("convergence",),
                detail={"path": str(path)},
            )
        )
        self.path = path
        self.remedy = remedy


# The fingerprint: what the database looked like when Cratekit last left it


def _is_whole_number(value: Any) -> bool:
    """True for a real integer, and FALSE FOR A BOOLEAN.

    ``true`` would otherwise read as usn 1 and hide every regression.
    """
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class Fingerprint:
    """Three readings that together say which database this is and when.

    ``schema_version`` is recorded, not a trigger, since every upgrade moves it.
    """

    schema_version: str | None
    active_rows: int
    local_usn: int
    taken: str = ""

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Fingerprint:
        version = data.get("schema_version")
        rows = data.get("active_rows")
        usn = data.get("local_usn")
        if not _is_whole_number(rows) or not _is_whole_number(usn):
            raise ValueError(
                "a fingerprint needs an integer active row count and an integer "
                "local update count; without both there is no comparison to make "
                "and no way to say a database went backward"
            )
        return cls(
            schema_version=None if version is None else str(version),
            active_rows=rows,
            local_usn=usn,
            taken=str(data.get("taken") or ""),
        )


def probe(db: Any) -> Fingerprint:
    """Read the three numbers straight out of the database.

    The row count is filtered at the database, so a moved column raises rather
    than a defaulting accessor reading tombstones as live. Run under the
    autoflush guard, which needs a handle exposing a session; an absent one
    refuses. Each reading refuses separately with a structured cause (S4), so
    the failed reading is named.
    """
    session = getattr(db, "session", _NO_SESSION)
    if session is _NO_SESSION:
        raise _refuse(
            "library-fingerprint-unreadable",
            "this database handle exposes no session, so the autoflush guard "
            "this probe has to run under cannot be armed; a query issued outside "
            "it flushes the pending collections that every downstream write "
            "guard reads to decide what a commit would do, and the guard then "
            "passes a forbidden write it can no longer see",
            remedy=Remedy.REPORT_DEFECT,
            detail={"handle": type(db).__name__},
        )
    with rb_writer._no_autoflush(session):
        version = _reading(
            "schema version", lambda: rb_writer.db_schema_version(db)
        )
        active = _reading(
            "active row count", lambda: db.get_content(**{SOFT_DELETE_COLUMN: 0}).count()
        )
        usn = _reading("local update count", lambda: db.get_local_usn())
    return Fingerprint(
        schema_version=version,
        active_rows=_counted("active row count", active),
        local_usn=_counted("local update count", usn),
    )


#: Tells "no session attribute" from "session is None"; only one is a stand-in.
_NO_SESSION = object()


def _reading(what: str, read: Callable[[], Any]) -> Any:
    """One reading off the database, or a refusal that NAMES which one failed."""
    try:
        return read()
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - a database that cannot answer IS the answer
        raise _refuse(
            "library-fingerprint-unreadable",
            f"the database's {what} could not be read ({exc}), so whether this "
            f"is the database Cratekit last wrote to cannot be decided in either "
            f"direction",
            remedy=Remedy.RUN_DOCTOR,
            detail={"reading": what, "column": SOFT_DELETE_COLUMN},
        ) from exc


def _counted(what: str, value: Any) -> int:
    """A reading that must already BE a whole number, never one coerced into being."""
    if not _is_whole_number(value):
        raise _refuse(
            "library-fingerprint-unreadable",
            f"the database answered its {what} with {value!r}, which is not a "
            f"whole number; coercing it would build the comparison that decides "
            f"whether this library went backward out of a value nobody checked",
            remedy=Remedy.REPORT_DEFECT,
            detail={"reading": what, "found": type(value).__name__},
        )
    return value


def regression(previous: Fingerprint | None, current: Fingerprint) -> Regression | None:
    """Whether the database went backward between the two readings. Pure.

    No previous reading is not a regression, or a fresh install would refuse.
    Ordinary use moves both numbers forward and is silent (P7).
    """
    if previous is None:
        return None
    if current.local_usn < previous.local_usn:
        return Regression.SEQUENCE_WENT_BACKWARD
    if (
        current.local_usn == previous.local_usn
        and current.active_rows != previous.active_rows
    ):
        return Regression.ROWS_MOVED_AT_A_STANDSTILL
    return None


# The record


@dataclass(frozen=True, slots=True)
class Disposition:
    """A named person saying a difference this tree carries is not damage.

    The one escape from an otherwise permanent refusal. ``actor`` is required,
    so the product never vouches for a library on the user's behalf.
    """

    actor: str
    note: str = ""
    on: str = ""

    def __post_init__(self) -> None:
        if not str(self.actor).strip():
            raise ValueError(
                "disposing of a convergence difference records WHO decided it is "
                "not damage; a disposition with no actor is the product deciding "
                "on the user's behalf that their library is fine"
            )

    def to_json(self) -> dict[str, Any]:
        return {"actor": self.actor, "note": self.note, "on": self.on}

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Disposition:
        return cls(
            actor=str(data["actor"]),
            note=str(data.get("note") or ""),
            on=str(data.get("on") or ""),
        )


@dataclass(frozen=True, slots=True)
class DestinationNode:
    """One declared destination and the two playlist rows a write put it in.

    Makes a rebuild converge across a rename: resolving by display name after a
    rename would create the destination again and file every track twice.
    ``bucket`` and ``sub`` are stable identifiers, never display names (R19, D5).
    """

    bucket: str
    sub: str
    folder_id: str
    playlist_id: str

    def __post_init__(self) -> None:
        for name in ("bucket", "sub", "folder_id", "playlist_id"):
            if not str(getattr(self, name)).strip():
                raise ValueError(
                    f"a recorded destination needs a {name}; a half-recorded node "
                    f"cannot be resolved and would send the next rebuild back to "
                    f"resolving by display name, which is what it exists to avoid"
                )

    def to_json(self) -> dict[str, Any]:
        return {
            "bucket": self.bucket,
            "sub": self.sub,
            "folder": self.folder_id,
            "playlist": self.playlist_id,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> DestinationNode:
        return cls(
            bucket=str(data["bucket"]),
            sub=str(data["sub"]),
            folder_id=str(data["folder"]),
            playlist_id=str(data["playlist"]),
        )


def assert_injective(tree_id: str, nodes: Sequence[DestinationNode]) -> None:
    """Refuse a node map that is not one-to-one, in either direction.

    Two nodes for one destination are resolved by line order. Two destinations
    on one node file both sets of tracks into it, which an additive rebuild can
    never undo. There is no automatic fallback: :func:`read` refuses the record
    as unreadable, since dropping the nodes would resolve by display name. The
    answers are the doctor or a restore, and the read-only check reports it.
    """
    by_destination: dict[tuple[str, str], DestinationNode] = {}
    by_node: dict[tuple[str, str], DestinationNode] = {}
    for entry in nodes:
        destination = (entry.bucket, entry.sub)
        if destination in by_destination:
            raise ValueError(
                f"the tree {tree_id!r} records two nodes for the destination "
                f"{entry.bucket}/{entry.sub}; a destination that resolves to two "
                f"playlists is resolved by line order, which decides where a "
                f"rebuild writes a library's worth of tracks"
            )
        node = (entry.folder_id, entry.playlist_id)
        clash = by_node.get(node)
        if clash is not None:
            raise ValueError(
                f"the tree {tree_id!r} records the destinations "
                f"{clash.bucket}/{clash.sub} and {entry.bucket}/{entry.sub} "
                f"against one playlist row ({entry.folder_id}/"
                f"{entry.playlist_id}); two declared destinations sharing one "
                f"node means every rebuild files both sets of tracks into it and "
                f"reports the other destination short, and an additive rebuild "
                f"cannot undo that, so the tree could never converge again"
            )
        by_destination[destination] = entry
        by_node[node] = entry


@dataclass(frozen=True, slots=True)
class TreeConvergence:
    """One tree's convergence standing, and where its destinations landed.

    ``unconverged`` is a persisted FACT, since re-deriving it would ask the
    damaged database to report its own damage.
    """

    tree_id: str
    unconverged: bool = False
    reason: str | None = None
    since: str | None = None
    disposition: Disposition | None = None
    nodes: tuple[DestinationNode, ...] = ()

    def __post_init__(self) -> None:
        if not str(self.tree_id).strip():
            raise ValueError(
                "a convergence record needs the identifier of the tree it "
                "describes; a record that cannot say which tree it is about "
                "still refuses writes and names nothing for anyone to repair"
            )
        assert_injective(self.tree_id, self.nodes)

    @property
    def blocking(self) -> bool:
        """Whether this record refuses a governed write today.

        A disposed tree stays unconverged, so reports still say so, but does not block.
        """
        return self.unconverged and self.disposition is None

    def node(self, bucket: str, sub: str) -> DestinationNode | None:
        return next((e for e in self.nodes if e.bucket == bucket and e.sub == sub), None)

    def with_nodes(self, nodes: Iterable[DestinationNode]) -> TreeConvergence:
        """This record with ``nodes`` replacing any entry for the same destination."""
        merged = {(entry.bucket, entry.sub): entry for entry in self.nodes}
        for entry in nodes:
            merged[(entry.bucket, entry.sub)] = entry
        return replace(
            self,
            nodes=tuple(sorted(merged.values(), key=lambda e: (e.bucket, e.sub))),
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "tree": self.tree_id,
            "unconverged": self.unconverged,
            "reason": self.reason,
            "since": self.since,
            "disposition": None if self.disposition is None else self.disposition.to_json(),
            "nodes": [entry.to_json() for entry in self.nodes],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> TreeConvergence:
        flag = data.get("unconverged")
        if not isinstance(flag, bool):
            # NO DEFAULT: the default reads as converged and admits every write.
            raise ValueError(
                "a convergence record needs an explicit boolean unconverged "
                "field; the value it would otherwise default to is the one that "
                "admits a write to a tree a restore may have left short"
            )
        raw_nodes = data.get("nodes")
        if not isinstance(raw_nodes, list):
            # NO DEFAULT: an absent key would resolve by display name and double
            # the tree after a rename.
            raise ValueError(
                "a convergence record's nodes field is an array and is required; "
                "an absent one would read as 'nothing was ever recorded' and "
                "send the next rebuild back to resolving by display name, which "
                "doubles the tree after a rename"
            )
        raw_disposition = data.get("disposition")
        if raw_disposition is not None and not isinstance(raw_disposition, dict):
            raise ValueError("a convergence record's disposition is an object or null")
        return cls(
            tree_id=str(data["tree"]),
            unconverged=flag,
            reason=None if data.get("reason") is None else str(data["reason"]),
            since=None if data.get("since") is None else str(data["since"]),
            disposition=(
                None if raw_disposition is None else Disposition.from_json(raw_disposition)
            ),
            nodes=tuple(DestinationNode.from_json(entry) for entry in raw_nodes),
        )


@dataclass(frozen=True, slots=True)
class ConvergenceState:
    """Everything this library records about its governed trees.

    A tuple, not a mapping, so no identifier sits in a key position (R19).
    """

    fingerprint: Fingerprint | None = None
    trees: tuple[TreeConvergence, ...] = ()

    def tree(self, tree_id: str) -> TreeConvergence | None:
        return tree_registry.by_tree_id(self.trees, tree_id)

    def blocking_trees(self) -> tuple[str, ...]:
        return tuple(entry.tree_id for entry in self.trees if entry.blocking)

    def with_tree(self, record: TreeConvergence) -> ConvergenceState:
        kept = tuple(e for e in self.trees if e.tree_id != record.tree_id)
        return replace(
            self, trees=tuple(sorted((*kept, record), key=lambda e: e.tree_id))
        )

    def with_fingerprint(self, taken: Fingerprint) -> ConvergenceState:
        return replace(self, fingerprint=taken)


#: What a library with no record resolves to.
EMPTY = ConvergenceState()


# Reading and writing it


def path_for(cfg: config.Config) -> Path:
    """Where the record lives, through the inventory, since it is COUPLED."""
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """Where the record's exclusive lock lives, resolved through the inventory."""
    return config.state_path(LOCK_KEY, cfg)


def read(cfg: config.Config) -> ConvergenceState:
    """The effective record for this library. An absent file is the empty one.

    Every field is recognised positively and everything else refused, so a
    misread can never be written back as an empty store.
    """
    path = path_for(cfg)

    def unusable(
        message: str, *, remedy: Remedy = Remedy.RUN_DOCTOR
    ) -> ConvergenceStateUnreadable:
        return ConvergenceStateUnreadable(message, path=path, remedy=remedy)

    try:
        raw = config.read_bytes_if_present(path)
    except OSError as exc:
        raise unusable(f"{path} exists and could not be read: {exc}") from exc
    if raw is None:
        return EMPTY

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise unusable(f"{path} is not readable as JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise unusable(f"{path} does not hold an object at its top level")

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise unusable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
        )
    if version > SCHEMA_VERSION:
        raise unusable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            remedy=Remedy.UPGRADE_CRATEKIT,
        )

    raw_fingerprint = data.get("fingerprint")
    if raw_fingerprint is not None and not isinstance(raw_fingerprint, dict):
        raise unusable(f"{path} holds a fingerprint that is not an object")
    entries = data.get("trees")
    if not isinstance(entries, list):
        raise unusable(f"{path} has no trees array")

    records: list[TreeConvergence] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise unusable(f"{path} holds a tree record that is not an object")
        try:
            record = TreeConvergence.from_json(entry)
        except (KeyError, TypeError, ValueError) as exc:
            # Refused, not dropped, since a dropped record reads as fine.
            raise unusable(f"{path} holds an unusable tree record: {exc}") from exc
        if record.tree_id in seen:
            raise unusable(
                f"{path} holds two records for the tree {record.tree_id!r}; a "
                f"record that gives two answers for one tree cannot say whether "
                f"it is converged, and resolving that by line order decides "
                f"whether a write runs against a damaged library",
            )
        seen.add(record.tree_id)
        records.append(record)

    try:
        taken = None if raw_fingerprint is None else Fingerprint.from_json(raw_fingerprint)
    except (KeyError, TypeError, ValueError) as exc:
        raise unusable(f"{path} holds an unusable fingerprint: {exc}") from exc

    return ConvergenceState(
        fingerprint=taken, trees=tuple(sorted(records, key=lambda e: e.tree_id))
    )


def write(cfg: config.Config, state: ConvergenceState) -> Path:
    """Persist ``state`` for this library, atomically and owner only.

    The directory mode matters as much as the file's (P1).
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": None if state.fingerprint is None else state.fingerprint.to_json(),
        # Sorted so the bytes are a function of the content alone.
        "trees": [entry.to_json() for entry in sorted(state.trees, key=lambda e: e.tree_id)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


# The mutators. Every one holds the lock across read and write, because an
# atomic rename does not make the read-modify-write cycle atomic.


def record_fingerprint(
    cfg: config.Config, db: Any, *, now: datetime | None = None
) -> Fingerprint:
    """Write down what the database looks like as this session leaves it.

    CALLED AFTER THE COMMIT, NEVER BEFORE, or the next run sees its own change
    as a restore. A crash between the two leaves a stale reading, never a false
    refusal.
    """
    taken = replace(probe(db), taken=output.timestamp(now))
    with config.exclusive_lock(lock_path(cfg)):
        write(cfg, read(cfg).with_fingerprint(taken))
    return taken


def mark_unconverged(
    cfg: config.Config,
    tree_ids: Iterable[str],
    *,
    reason: str,
    now: datetime | None = None,
) -> ConvergenceState:
    """Flag trees as no longer matching what this library declares.

    A tree already flagged for the same reason keeps its original ``since``.
    """
    stamp = output.timestamp(now)
    with config.exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        for tree_id in tree_ids:
            current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
            if current.unconverged and current.reason == reason and current.disposition is None:
                continue
            # A DISPOSED TREE MARKED AGAIN IS A NEW REFUSAL, whatever its reason (U219).
            state = state.with_tree(
                replace(
                    current,
                    unconverged=True,
                    reason=reason,
                    since=stamp,
                    # A new refusal clears an old disposition nobody gave for it.
                    disposition=None,
                )
            )
        write(cfg, state)
    return state


def record_nodes(
    cfg: config.Config,
    tree_id: str,
    nodes: Iterable[DestinationNode],
    *,
    replace_all: bool = False,
) -> ConvergenceState:
    """Write down which playlist rows a write put each declared destination in.

    ``replace_all`` is for the rebuild, which considered every destination;
    merging would keep a dangling entry that can collide (:func:`assert_injective`).
    """
    with config.exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
        updated = (
            replace(current, nodes=tuple(sorted(nodes, key=lambda e: (e.bucket, e.sub))))
            if replace_all
            else current.with_nodes(nodes)
        )
        state = state.with_tree(updated)
        write(cfg, state)
    return state


def clear_unconverged(
    cfg: config.Config,
    tree_id: str,
    *,
    differences: Sequence[str],
    now: datetime | None = None,
    disposition: Disposition | None = None,
) -> ConvergenceState:
    """Take a tree out of the refusing state, on evidence or on a named decision.

    TWO WAYS THROUGH AND ONLY TWO: an empty ``differences`` from a check that
    just ran clears the flag, or a named disposition stops it refusing while it
    stays set. ``differences`` is the check's own list, so the refusal names it.
    """
    outstanding = [str(entry) for entry in differences]
    if outstanding and disposition is None:
        raise _refuse(
            "tree-unconverged",
            f"the tree {tree_id!r} still differs from what this library declares "
            f"in {len(outstanding)} place(s), so its unconverged flag stays set; "
            f"clearing it now would report the tree as repaired while the "
            f"membership it is missing is still missing",
            remedy=Remedy.REBUILD_TREE,
            steps=(
                "run the rebuild for this tree, which derives its whole "
                "membership from the declared taxonomy and what is on disk and "
                "writes back everything the database lacks",
                "a difference the rebuild cannot derive, such as a playlist "
                "somebody curated by hand under this tree, is answered by a "
                "named person disposing of it for this tree alone",
            ),
            detail={"tree_id": tree_id, "differences": outstanding[:20]},
        )

    stamp = output.timestamp(now)
    with config.exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
        if disposition is not None:
            if not current.blocking:
                # A disposition answers a refusal, and there is none to answer.
                raise _refuse(
                    "tree-unconverged",
                    f"the tree {tree_id!r} is not refusing anything, so there is "
                    f"no difference for anybody to dispose of; recording one now "
                    f"would leave a named person's acceptance standing over a "
                    f"library they were never shown",
                    remedy=Remedy.COMPLETE_PENDING_ACTION,
                    steps=(
                        "run the convergence check for this tree and dispose of "
                        "what it actually reports",
                    ),
                    detail={"tree_id": tree_id, "actor": disposition.actor},
                )
            settled = replace(
                current, disposition=replace(disposition, on=disposition.on or stamp)
            )
        else:
            settled = replace(
                current, unconverged=False, reason=None, since=None, disposition=None
            )
        state = state.with_tree(settled)
        write(cfg, state)
    return state


# The two assertions every governed write makes


def native_trees(cfg: config.Config, registry: tree_registry.Registry) -> tuple[str, ...]:
    """Every database-native tree in this library, from the record AND from disk.

    The union, so a caller passing a filtered registry cannot leave other native
    trees unmarked. A tree never written to is marked and never cleared (R-17).
    """
    return tuple(
        sorted(
            set(registry.database_native_trees())
            | set(tree_registry.read(cfg).database_native_trees())
        )
    )


@dataclass(frozen=True, slots=True)
class RestoreCheck:
    """What the detection found, and the two readings it decided from.

    So the refusal names both numbers without probing a second time.
    """

    regression: Regression | None
    previous: Fingerprint | None
    current: Fingerprint | None
    trees: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.regression is not None


def detect_out_of_band_restore(
    cfg: config.Config,
    db: Any,
    registry: tree_registry.Registry,
    *,
    now: datetime | None = None,
) -> RestoreCheck:
    """Compare the database against the fingerprint, MARK, and report. Never refuses.

    Separate from the refusal so a rebuild still detects before its close
    records a new fingerprint. It marks before returning, because the evidence
    moves on after the next rekordbox session. Every native tree is marked,
    since the evidence is about the whole database.
    """
    native = native_trees(cfg, registry)
    if not native:
        # Nothing has cut over, so nothing needs a fingerprint yet.
        return RestoreCheck(regression=None, previous=None, current=None)
    current = probe(db)
    previous = read(cfg).fingerprint
    found = regression(previous, current)
    if found is not None:
        mark_unconverged(cfg, native, reason=str(found), now=now)
    return RestoreCheck(
        regression=found, previous=previous, current=current, trees=native
    )


def assert_no_out_of_band_restore(
    cfg: config.Config,
    db: Any,
    registry: tree_registry.Registry,
    *,
    now: datetime | None = None,
) -> None:
    """Detect, and then refuse if the database went backward."""
    checked = detect_out_of_band_restore(cfg, db, registry, now=now)
    found = checked.regression
    if found is None:
        return
    raise _refuse(
        "tree-unconverged",
        f"this library's database went backward since Cratekit last wrote to it "
        f"({str(found)}), which no snapshot restore of ours explains, so every "
        f"tree the database owns is treated as short until it is rebuilt; the "
        f"membership a recovered database no longer holds is not something an "
        f"incremental sync can put back, because the files it lost are still on "
        f"disk and still read as already owned",
        remedy=Remedy.REBUILD_TREE,
        steps=(
            "run the convergence check, which reports per tree what the database "
            "is missing and what it holds that nothing declares",
            "run the rebuild for each tree it reports short",
        ),
        detail={
            "regression": str(found),
            "trees": list(checked.trees),
            "recorded_usn": (
                None if checked.previous is None else checked.previous.local_usn
            ),
            "found_usn": None if checked.current is None else checked.current.local_usn,
        },
    )


def assert_converged(cfg: config.Config, tree_id: str) -> None:
    """Refuse a governed write to a tree that is recorded as short.

    Read from the record alone, so it needs no mounted volume.
    """
    record = read(cfg).tree(tree_id)
    if record is None or not record.blocking:
        return
    raise _refuse(
        "tree-unconverged",
        f"the tree {tree_id!r} has been unconverged since {record.since} "
        f"({record.reason}), so writing to it now would add to a tree that is "
        f"already missing membership and report the run as clean",
        remedy=Remedy.REBUILD_TREE,
        steps=(
            "run the rebuild for this tree, which derives its whole membership "
            "from the declared taxonomy and what is on disk",
            "a difference the rebuild cannot derive is answered by a named "
            "person disposing of it for this tree alone",
        ),
        detail={"tree_id": tree_id, "reason": record.reason, "since": record.since},
    )


def assert_tree_writable(
    cfg: config.Config,
    db: Any,
    tree_id: str,
    registry: tree_registry.Registry,
    *,
    purpose: Purpose = Purpose.ROUTINE,
    now: datetime | None = None,
) -> None:
    """Both questions, in the order that makes the second one's answer current.

    The restore check runs first because it sets the flag the second reads, and
    one call means no caller arms half. A non ``ROUTINE`` purpose skips the two
    refusals but never the detection, so a rebuild cannot bless a recovered
    fingerprint and leave other emptied trees unmarked. Written as "only
    ROUTINE is refused" so a new purpose inherits the checking.
    """
    if purpose is Purpose.ROUTINE:
        assert_no_out_of_band_restore(cfg, db, registry, now=now)
        assert_converged(cfg, tree_id)
        return
    detect_out_of_band_restore(cfg, db, registry, now=now)

