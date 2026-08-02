"""Which medium owns each tree, and the cutover that moves one (KTD22, R14, R19).

A tree is a named subtree of the playlist hierarchy: the routing tree, the intake
tree, and whatever else a taxonomy declares. Every tree is written either by the
XML bridge, which splices bytes into an export the user re-imports, or natively
into the database. Exactly one of those is correct for a given tree at a given
moment, and getting it wrong is silent: the byte writer happily splices a tree
the database already owns, the user imports it, and rekordbox merges two trees
that were meant to be one. Nothing errors. The library just quietly grows a
second copy of itself.

This module is the record of which medium owns what, and it is the input both
guards read.

THREE PROPERTIES, EACH LEARNED FROM A DIFFERENT FAILURE.

**All trees start on the bridge, and that is not configurable at setup.** A
per-tree cutover is a migration, not a preference. Offering it as a setup
question would let a new user answer it before they have a library to migrate,
and the answer they would be guessing at is which of two write paths a tree they
have not created yet should use.

**It is library-scoped state and it is never committed (KTD22).** The mode, the
cutover date, and the adopted root's identifier all describe one person's
library. Committing them would ship the author's flips and the author's row
identifiers to everybody who clones, and it would put them somewhere the system
this replaces cannot read at all. The state inventory already declares the entry
COUPLED, which is the sharper half: a registry that rolls back while the database
does not, or the reverse, is the plan's top-ranked risk, and coupling them means
one snapshot carries both or neither.

**It carries the adopted root's identifier, so skew is detectable.** A mode alone
says a tree moved. It cannot say WHICH root it moved to, so a database restored
from before the cutover satisfies a mode check perfectly while holding no such
root, and the writer then creates one, which is the silent parallel tree in its
purest form. Recording the identifier turns that into a refusal.

WHY THE INVERSE CHECK LIVES HERE RATHER THAN IN THE DATABASE WRITER. Both
directions are the same question asked from opposite ends, and a check that lived
with each writer would be two implementations of one rule, which is how they come
to disagree. The database tree writers land in a later unit; the assertion they
are required to call ships here, and a gate in tests/test_tree_registry.py holds
that unit to calling it rather than hand-rolling its own.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Callable

from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy

#: The state entry this module owns. Named once, so the resolver and every caller
#: cannot disagree about which file is meant.
STATE_KEY = "tree_registry"

#: Bumped only when the on-disk shape changes incompatibly. A file written by a
#: newer build is not guessed at: a wrong reading here decides which writer runs
#: against a real library, and no answer is better than a wrong one.
SCHEMA_VERSION = 1


class Mode(StrEnum):
    """The medium that owns a tree's membership writes.

    Two members, and the set is closed. There is no third medium, so a mode this
    build does not recognise is a file to refuse rather than a shape to extend.
    """

    #: The XML bridge: bytes spliced into an export the user re-imports.
    XML = "xml"
    #: Native database writes, after this tree's cutover was recorded.
    DATABASE = "database"


#: Every mode this build understands, derived from the enum rather than repeated,
#: so a third member cannot exist in one place and not the other.
MODES: tuple[str, ...] = tuple(m.value for m in Mode)

#: Where every tree starts. Not configurable at setup: a cutover is a migration
#: with a date and an adopted root, not a preference somebody answers up front.
DEFAULT_MODE: Mode = Mode.XML


class TreeRegistryUnreadable(CratekitError):
    """The registry file exists and cannot be understood.

    Deliberately NOT collapsed into "no record", which would be read as "every
    tree is still on the bridge" and would send a byte write at a tree the
    database already owns. That is precisely the failure this module exists to
    prevent, so an unreadable file has to be its own answer.

    A ``CratekitError`` for the reason its two siblings below give. One slug
    covers every way this file can be unusable and the REMEDY is what differs:
    a registry from a newer build asks for an upgrade and a corrupt one asks for
    the doctor, and neither survives being flattened into a defect report.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="tree-registry-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("tree_registry",),
                detail={"path": str(path)},
            )
        )
        self.path = path
        self.remedy = remedy


class TreeModeRefused(CratekitError):
    """A write in the wrong medium for the tree it targets.

    One exception type for both directions, carrying which direction it was, so
    a caller can tell them apart without the two guards growing separate
    hierarchies that drift. ``tree_id`` is always populated: a refusal that does
    not name the tree leaves the reader to guess which of several a sweep was on
    when it stopped.

    A ``CratekitError`` RATHER THAN A PLAIN EXCEPTION, and that is S4 rather than
    tidiness. The command-line boundary converts anything that is not a
    structured cause into an internal defect with "report a defect" attached, so
    a refusal that carries a remedy and is not one of these arrives with its
    remedy discarded and its reader told to file a bug. Both directions carry
    DIFFERENT remedies, which is exactly why the remedy travels on the cause
    rather than being derived from the slug.
    """

    def __init__(
        self,
        message: str,
        *,
        tree_id: str,
        mode: str,
        attempted: str,
        remedy: Remedy,
    ) -> None:
        super().__init__(
            Cause(
                reason="tree-unconverged",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("tree_registry",),
                detail={"tree_id": tree_id, "mode": str(mode), "attempted": str(attempted)},
            )
        )
        self.tree_id = tree_id
        self.mode = mode
        self.attempted = attempted
        self.remedy = remedy


class RegistrySkew(CratekitError):
    """The registry and the database disagree about a tree that has cut over.

    The concrete case: a library restored from a snapshot taken before the
    cutover, beside a registry that was not rolled back with it. The mode says
    native, the adopted root is not there, and a writer that trusted the mode
    alone would create a second root beside the real one and report success.

    A ``CratekitError`` for the reason :class:`TreeModeRefused` gives. It is
    raised by the same anchoring call, reaches the same callers, and its remedy
    is not the class default for its code, so flattening it at the boundary
    would replace "restore from a snapshot" with "report a defect".
    """

    def __init__(self, message: str, *, tree_id: str, root_id: str | None) -> None:
        super().__init__(
            Cause(
                reason="tree-unconverged",
                message=message,
                remediation=Remediation(remedy=Remedy.RESTORE_FROM_SNAPSHOT),
                scope=Scope.RUN,
                origin=("tree_registry",),
                detail={"tree_id": tree_id, "root_id": root_id},
            )
        )
        self.tree_id = tree_id
        self.root_id = root_id
        self.remedy = Remedy.RESTORE_FROM_SNAPSHOT


@dataclass(frozen=True, slots=True)
class TreeRecord:
    """One tree's medium, when it moved, and what it adopted.

    ``tree_id`` is the taxonomy's stable identifier, never a display name (R19,
    D5). A tree renamed in rekordbox keeps its record; a record keyed on the name
    would be orphaned by the rename, and an orphaned record reads as "still on
    the bridge", which sends the next write to the wrong medium.

    ``root_id`` is the identifier of the root row the tree adopted at cutover. It
    is None while the tree is on the bridge, because there is nothing adopted
    yet, and it is required once the tree is native.
    """

    tree_id: str
    mode: Mode = DEFAULT_MODE
    cutover_on: date | None = None
    root_id: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in MODES:
            raise ValueError(
                f"tree {self.tree_id!r} declares mode {self.mode!r}, which is not "
                f"one of {list(MODES)}"
            )
        if self.mode == Mode.DATABASE and not self.root_id:
            raise ValueError(
                f"tree {self.tree_id!r} is recorded as database native with no "
                f"adopted root identifier; without one a restored pre-cutover "
                f"database cannot be told from the library the cutover ran against"
            )
        if self.mode == Mode.DATABASE and self.cutover_on is None:
            raise ValueError(
                f"tree {self.tree_id!r} is recorded as database native with no "
                f"cutover date; the date is what lets a reader place the flip "
                f"against the snapshots either side of it"
            )


@dataclass(frozen=True, slots=True)
class Registry:
    """Every record the registry holds. A tree with no record is on the bridge.

    Records are a TUPLE rather than a mapping keyed by tree. That is not a
    performance choice, there are a handful of trees. It keeps the identifier out
    of every key position in this module, so the R19 guard has nothing to
    interpret and a future reader has no dict to be tempted to key on a name.
    """

    trees: tuple[TreeRecord, ...] = ()

    def record(self, tree_id: str) -> TreeRecord | None:
        for entry in self.trees:
            if entry.tree_id == tree_id:
                return entry
        return None

    def mode(self, tree_id: str) -> str:
        """The medium that owns ``tree_id``. Unrecorded means the bridge."""
        entry = self.record(tree_id)
        return DEFAULT_MODE if entry is None else entry.mode

    def is_database_native(self, tree_id: str) -> bool:
        return self.mode(tree_id) == Mode.DATABASE

    def is_on_the_bridge(self, tree_id: str) -> bool:
        return self.mode(tree_id) == Mode.XML

    def tree_ids(self) -> tuple[str, ...]:
        return tuple(entry.tree_id for entry in self.trees)

    def with_record(self, record: TreeRecord) -> Registry:
        """This registry plus ``record``, replacing any record for the same tree.

        Pure, so a caller can compose a change and validate it before anything
        reaches disk, and so the guards can be exercised without a filesystem.
        """
        kept = tuple(e for e in self.trees if e.tree_id != record.tree_id)
        return Registry(tuple(sorted((*kept, record), key=lambda e: e.tree_id)))


#: The registry every library starts with, and the value an absent file resolves
#: to. Named, because "empty" is a real answer here and not a missing one.
EMPTY = Registry()


def path_for(cfg: config.Config) -> Path:
    """Where the registry lives, resolved through the state inventory.

    Through ``state_path`` rather than composed here. A module that builds its own
    path under a state root has invented a state file the inventory does not know
    about, so nothing that walks the inventory will snapshot it, and this is the
    one file whose snapshot coupling the plan's top-ranked risk is named after.
    """
    return config.state_path(STATE_KEY, cfg)


def read(cfg: config.Config) -> Registry:
    """The effective registry for this library. An absent file is the empty one.

    P2, and it is the reason this function takes a ``Config`` rather than a path.
    Every runtime consumer resolves the file through the configuration it is
    already holding, including any environment override applied to the library
    root. A check that opened a path composed some other way would validate a
    file the writers never read, which is a check and a consumer disagreeing
    about their input.
    """
    return read_path(path_for(cfg))


def read_path(path: Path) -> Registry:
    """The registry held at one named file. The reader, given an explicit target.

    :func:`read` is the one every runtime consumer uses, and it resolves the path
    from configuration for the reason P2 states. This exists for the one caller
    that legitimately means a DIFFERENT file: a restore compares the registry
    inside a capture against the live one, because that comparison is the exact
    record of which trees had cut over when the capture was taken. Doing it by
    date arithmetic instead is wrong by up to a day in both directions.

    Split out rather than added as an optional argument to :func:`read`, so a
    caller cannot pass a path by accident and quietly validate a file nothing
    else reads. Reaching for this one is a deliberate act with a visible name.
    """
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise TreeRegistryUnreadable(
            f"{path} exists but could not be read: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TreeRegistryUnreadable(
            f"{path} is not readable as JSON: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc
    if not isinstance(data, dict):
        raise TreeRegistryUnreadable(
            f"{path} does not hold an object at its top level",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise TreeRegistryUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if version > SCHEMA_VERSION:
        raise TreeRegistryUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )

    entries = data.get("trees")
    if not isinstance(entries, list):
        raise TreeRegistryUnreadable(
            f"{path} has no trees array",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    records: list[TreeRecord] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise TreeRegistryUnreadable(
                f"{path} holds a tree entry that is not an object",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        tree_id = entry.get("tree")
        if not isinstance(tree_id, str) or not tree_id.strip():
            raise TreeRegistryUnreadable(
                f"{path} holds a tree entry with no identifier; a record that "
                f"cannot say which tree it describes is worse than no record",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        if tree_id in seen:
            # Two answers for one tree is a file to refuse, not a shape to
            # resolve by position. The sort below is stable, so resolving it
            # would silently mean "whichever record was written first", and a
            # file that a merge or a restore concatenated would then report a
            # tree as still on the bridge while another record in the same file
            # says the database owns it. That is the wrong medium, chosen by
            # line order.
            raise TreeRegistryUnreadable(
                f"{path} holds two records for the tree {tree_id!r}; a registry "
                f"that gives two answers for one tree cannot say which medium "
                f"owns it, and guessing decides which writer runs against a "
                f"real library",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(tree_id)
        stamp = entry.get("cutover_on")
        cutover: date | None = None
        if stamp is not None:
            try:
                cutover = date.fromisoformat(str(stamp))
            except (TypeError, ValueError) as exc:
                raise TreeRegistryUnreadable(
                    f"{path} records {tree_id!r} as cutting over on {stamp!r}, "
                    f"which is not an ISO date",
                    path=path,
                    remedy=Remedy.RUN_DOCTOR,
                ) from exc
        root_id = entry.get("root")
        try:
            records.append(
                TreeRecord(
                    tree_id=tree_id,
                    mode=Mode(str(entry.get("mode", DEFAULT_MODE))),
                    cutover_on=cutover,
                    root_id=None if root_id is None else str(root_id),
                )
            )
        except ValueError as exc:
            # A structurally invalid record is refused rather than dropped. A
            # dropped record reads as "still on the bridge", which is the one
            # misreading that routes a write to the wrong medium.
            raise TreeRegistryUnreadable(
                f"{path} holds an unusable record: {exc}",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            ) from exc

    return Registry(tuple(sorted(records, key=lambda e: e.tree_id)))


def write(cfg: config.Config, registry: Registry) -> Path:
    """Persist ``registry`` for this library, atomically and owner only.

    Through ``config.atomic_write_bytes``, which applies the explicit file mode
    and creates the enclosing directories at the explicit directory mode. Both
    halves matter and P1 is the reason: a 0600 file inside a world writable
    directory can be unlinked and replaced by any local account, so its own mode
    decides nothing. This file decides which writer runs against a real library.
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        "trees": [
            {
                "tree": entry.tree_id,
                "mode": str(entry.mode),
                "cutover_on": None if entry.cutover_on is None else entry.cutover_on.isoformat(),
                "root": entry.root_id,
            }
            # Sorted so the bytes are a function of the content alone. An
            # unordered dump makes every write a diff even when nothing changed.
            for entry in sorted(registry.trees, key=lambda e: e.tree_id)
        ],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def record_cutover(
    cfg: config.Config,
    tree_id: str,
    *,
    root_id: str,
    on: date,
) -> Registry:
    """Move one tree to the database, naming the root it adopted and the day.

    Read, modify, write, rather than a whole file overwrite. Trees cut over one
    at a time by design, and a writer that replaced the file would erase every
    other tree's record on each flip.
    """
    if not root_id:
        raise ValueError(
            f"recording a cutover for {tree_id!r} needs the identifier of the "
            f"root it adopted; without one, a pre-cutover database restored "
            f"underneath this registry cannot be detected"
        )
    current = read(cfg)
    updated = current.with_record(
        TreeRecord(tree_id=tree_id, mode=Mode.DATABASE, cutover_on=on, root_id=str(root_id))
    )
    write(cfg, updated)
    return updated


# ---------------------------------------------------------------------------
# The two guards. One rule, asked from each end.
# ---------------------------------------------------------------------------


def refuse_bridge_write(tree_id: str, registry: Registry) -> None:
    """Refuse a byte splice into a tree the database already owns.

    Called by every emitter in the XML bridge. The refusal names the tree,
    because a sweep touches several and a message that does not say which one
    stopped it leaves the reader to guess.
    """
    if registry.is_database_native(tree_id):
        raise TreeModeRefused(
            f"the tree {tree_id!r} is database native since its recorded "
            f"cutover, so the XML bridge must not write it; splicing bytes into "
            f"an export for a tree the database owns creates a second tree beside "
            f"the real one on import, and nothing reports it",
            tree_id=tree_id,
            mode=registry.mode(tree_id),
            attempted=Mode.XML,
            remedy=Remedy.REPORT_DEFECT,
        )


def refuse_database_write(tree_id: str, registry: Registry) -> None:
    """Refuse a native write to a tree still on the bridge. The inverse check.

    Not symmetry for its own sake. Until a tree's cutover is recorded, the XML
    export is the only thing that has ever written it, so a native write lands
    rows the export knows nothing about and the next import overwrites them.
    """
    if registry.is_on_the_bridge(tree_id):
        raise TreeModeRefused(
            f"the tree {tree_id!r} is still on the XML bridge, so a database "
            f"writer must not write its membership; until the cutover is "
            f"recorded the export owns this tree and the next import would "
            f"overwrite whatever was written natively",
            tree_id=tree_id,
            mode=registry.mode(tree_id),
            attempted=Mode.DATABASE,
            remedy=Remedy.COMPLETE_PENDING_ACTION,
        )


def anchored_root(
    tree_id: str,
    registry: Registry,
    *,
    root_exists: Callable[[str], bool],
) -> str:
    """The adopted root identifier for a native tree, or a refusal.

    THE ASSERTION EVERY DATABASE TREE WRITER MAKES BEFORE WRITING MEMBERSHIP.
    Three failures, three distinct refusals, and collapsing any two of them costs
    the caller the ability to say what went wrong:

    * the tree is still on the bridge, so the write is in the wrong medium;
    * the record is native but names no root, which a valid record cannot be, so
      the file was edited by hand;
    * the record names a root the library does not have, which is the restored
      pre-cutover database. Creating one here is exactly the silent parallel tree.

    ``root_exists`` is supplied by the caller rather than looked up here, so this
    module performs no database input and stays testable without one.
    """
    refuse_database_write(tree_id, registry)
    entry = registry.record(tree_id)
    root_id = None if entry is None else entry.root_id
    if not root_id:
        raise RegistrySkew(
            f"the tree {tree_id!r} is recorded as database native but names no "
            f"adopted root, so there is nothing to write membership under",
            tree_id=tree_id,
            root_id=None,
        )
    if not root_exists(root_id):
        raise RegistrySkew(
            f"the tree {tree_id!r} adopted root {root_id!r} at its cutover and "
            f"this library has no such root; the database is older than the "
            f"registry, and writing now would create a second tree beside the "
            f"one the cutover adopted",
            tree_id=tree_id,
            root_id=root_id,
        )
    return root_id


__all__ = [
    "DEFAULT_MODE",
    "EMPTY",
    "MODES",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "Mode",
    "Registry",
    "RegistrySkew",
    "TreeModeRefused",
    "TreeRecord",
    "TreeRegistryUnreadable",
    "anchored_root",
    "path_for",
    "read",
    "read_path",
    "record_cutover",
    "refuse_bridge_write",
    "refuse_database_write",
    "write",
]
