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

#: The lock that serializes the read-modify-write ``record_cutover`` performs. A
#: second DECLARED entry rather than a suffix composed from the first, because a
#: path built under a state root is a file the inventory does not know about.
LOCK_KEY = "tree_registry_lock"

#: Bumped only when the on-disk shape changes incompatibly. A file written by a
#: newer build is not guessed at: a wrong reading here decides which writer runs
#: against a real library, and no answer is better than a wrong one.
#:
#: VERSION 2 ADDED THE DERIVATION SOURCE, and it is a real incompatibility rather
#: than an added optional field. A version 1 record could name a native tree with
#: no source, and this build refuses that record rather than reading it, because
#: a native tree whose membership cannot be re-derived has no repair path at all
#: (R39). Nothing has ever written such a record: recording a cutover is the only
#: way one comes into existence and no unit that flips a tree has landed.
SCHEMA_VERSION = 2


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


class DerivationSource(StrEnum):
    """Where a tree's FULL membership comes from, if it can be re-derived at all.

    R39's precondition for a cutover, expressed as a value on the record rather
    than as a judgement somebody makes at the moment they flip. A tree that has
    gone database-native has exactly one repair path when a restore leaves it
    short, and that path is a full-scope rebuild: incremental sync cannot close
    the gap, because its scope is a watermark plus deduplication against what is
    already owned, and the files a restore orphaned are still on disk and still
    read as owned. So a tree whose membership no declared source can reproduce is
    a tree that must never flip, and this enum is the question asked out loud.

    THE TWO NON-DERIVABLE MEMBERS ARE NOT PLACEHOLDERS. Catalogued source folders
    come from a crawl of a third-party catalogue that answers differently month to
    month, so re-deriving one next year produces a different, equally honest
    answer rather than the same one. A hand-curated or hearts-driven playlist
    derives from no declared source whatsoever. Both stay on the XML bridge, and
    naming them here is what stops the flip being offered for them at all.
    """

    #: The declared taxonomy applied to what is on disk. Reproducible: the same
    #: files and the same template give the same membership, every time.
    TAXONOMY = "taxonomy"

    #: One folder per catalogued source, one playlist per release year, built
    #: from a catalogue crawl. NOT reproducible.
    CATALOGUE_CRAWL = "catalogue-crawl"

    #: A person's own playlist, or one driven by what they hearted upstream.
    #: NOT reproducible from anything this product declares.
    CURATED = "curated"


#: The sources a full rebuild can reproduce, and therefore the only sources a
#: tree may cut over on (R39).
#:
#: LISTED, while its complement below is DERIVED. The direction is the property
#: and it is the same one the deferred-routing ledger applies to its settled
#: states: a member added later lands in the NOT-rebuildable set by default, so a
#: source nobody has classified cannot let a tree flip by omission. Deriving this
#: half instead would hand a new member the permissive answer.
REBUILDABLE: frozenset[DerivationSource] = frozenset({DerivationSource.TAXONOMY})

#: Everything else, derived so the two halves cannot both miss a member (P3).
NOT_REBUILDABLE: frozenset[DerivationSource] = frozenset(DerivationSource) - REBUILDABLE

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

    ``source`` is where a full rebuild of this tree's membership would come from.
    It follows ``root_id`` exactly: None on the bridge, required once native. A
    native record naming no source is refused rather than defaulted, and the
    default that is not offered is the dangerous one. Anything this module could
    pick would say "yes, this tree can be rebuilt" about a tree nobody checked,
    and that sentence is only ever discovered to be false at the one moment it
    matters, which is after a restore has already left the tree short.
    """

    tree_id: str
    mode: Mode = DEFAULT_MODE
    cutover_on: date | None = None
    root_id: str | None = None
    source: DerivationSource | None = None

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
        if self.mode == Mode.DATABASE and self.source is None:
            raise ValueError(
                f"tree {self.tree_id!r} is recorded as database native with no "
                f"derivation source, so nothing can say whether its membership "
                f"could be rebuilt after a restore left it short; a native tree "
                f"with no rebuild path has no repair path at all (R39)"
            )
        if self.source is not None and self.source not in frozenset(DerivationSource):
            raise ValueError(
                f"tree {self.tree_id!r} declares the derivation source "
                f"{self.source!r}, which is not one of "
                f"{[str(s) for s in DerivationSource]}"
            )
        if self.mode == Mode.XML:
            # THE CONTRADICTION IN THE OTHER DIRECTION, which nothing refused. A
            # record saying "on the bridge" while carrying a cutover date, an
            # adopted root and a derivation source describes a tree that flipped
            # and a mode that says it did not, and every consumer believes the
            # mode: the bridge writer splices an export for a tree the database
            # owns, and ``database_native_trees`` leaves it out of the set the
            # restore detector reads. That shape arrives from a hand-edited file
            # or from a record that lost one key, and reading it either way is a
            # guess about which half is true.
            carried = [
                name
                for name in ("cutover_on", "root_id", "source")
                if getattr(self, name) is not None
            ]
            if carried:
                raise ValueError(
                    f"tree {self.tree_id!r} is recorded as still on the XML "
                    f"bridge while carrying {', '.join(carried)}, which only a "
                    f"tree that has cut over can have; the record contradicts "
                    f"itself, and every consumer believes the mode, so the bridge "
                    f"would write an export for a tree the database may already "
                    f"own and the restore detector would not see it at all"
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

    def derivation_source(self, tree_id: str) -> DerivationSource | None:
        """Where a rebuild of this tree's membership would come from, if anywhere.

        None for a tree on the bridge, because nothing has decided yet, and never
        None for a native one: :class:`TreeRecord` refuses that combination.
        """
        entry = self.record(tree_id)
        return None if entry is None else entry.source

    def database_native_trees(self) -> tuple[str, ...]:
        """Every tree the database owns, which is the set a restore endangers.

        Derived from the records rather than accumulated by a caller, because the
        caller that needs it is the one marking every native tree unconverged
        after an out-of-band restore, and a set built by hand there would miss
        the tree somebody flipped last week.
        """
        return tuple(
            entry.tree_id for entry in self.trees if entry.mode == Mode.DATABASE
        )

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


def lock_path(cfg: config.Config) -> Path:
    """Where the registry's exclusive lock lives, resolved through the inventory.

    A DECLARED entry rather than a path composed here, for the reason every other
    state file is declared: a file the inventory does not know about is a file
    nothing walks, captures or clears.
    """
    return config.state_path(LOCK_KEY, cfg)


def read(cfg: config.Config) -> Registry:
    """The effective registry for this library. An absent file is the empty one.

    P2, and it is the reason this function takes a ``Config`` rather than a path.
    Every runtime consumer resolves the file through the configuration it is
    already holding, including any environment override applied to the library
    root. A check that opened a path composed some other way would validate a
    file the writers never read, which is a check and a consumer disagreeing
    about their input.
    """
    path = path_for(cfg)
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
        raw_source = entry.get("source")
        raw_mode = entry.get("mode")
        if raw_mode is None:
            # NO DEFAULT, and the value it would have defaulted to is why. A
            # record that lost its ``mode`` key while keeping ``cutover_on``,
            # ``root`` and ``source`` read as ``Mode.XML``, which is a
            # self-contradictory shape nothing refused: the record says the tree
            # cut over on a date, adopted a root and named a rebuild source,
            # while its mode says it is still on the bridge. The consequences
            # compound. ``is_on_the_bridge`` answers True, so the bridge writer
            # splices an export for a tree the database owns and under U9's A2
            # verdict the next import replaces it. ``database_native_trees``
            # answers empty, and that set is the restore detector's whole input,
            # so one missing key switches the out-of-band detection off for the
            # entire library.
            raise TreeRegistryUnreadable(
                f"{path} holds a record for {tree_id!r} with no mode; the medium "
                f"that owns a tree is the one thing this file exists to say, and "
                f"the value it would default to sends the bridge writer at a tree "
                f"the database may already own and switches the restore detector "
                f"off for every tree in this library",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        try:
            records.append(
                TreeRecord(
                    tree_id=tree_id,
                    mode=Mode(str(raw_mode)),
                    cutover_on=cutover,
                    root_id=None if root_id is None else str(root_id),
                    source=None if raw_source is None else DerivationSource(str(raw_source)),
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
                "source": None if entry.source is None else str(entry.source),
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
    source: DerivationSource,
) -> Registry:
    """Move one tree to the database, naming the root it adopted and the day.

    Read, modify, write, rather than a whole file overwrite. Trees cut over one
    at a time by design, and a writer that replaced the file would erase every
    other tree's record on each flip.

    UNDER AN EXCLUSIVE LOCK, because that cycle is not made atomic by the atomic
    rename at the end of it. Two processes that both read, both add a record and
    both rename leave one flip on the floor while the call that lost it returns a
    registry reporting success, and the tree whose cutover was lost then takes
    its next write through the XML bridge. Under U9's A2 verdict importing that
    export replaces the database-native tree outright. The primitive is the one
    the config migration already takes rather than a third implementation.

    REBUILDABILITY IS CHECKED HERE, WHICH IS THE ONLY MOMENT IT CAN BE. A cutover
    is a one-way door: under U9's A2 verdict a tree that has taken a native write
    is permanently unsafe to import over, so there is no undo to fall back on
    once a restore has left it short. The question "could this tree's membership
    be rebuilt" therefore has to be answered before the flip rather than after
    the damage, and answering it after is how a library ends up with a native
    tree, a gap, and no path from one to the other.

    ``source`` IS REQUIRED AND CARRIES NO DEFAULT, AND THE DEFAULT THAT IS NOT
    OFFERED IS THE DANGEROUS ONE. The only value this function could pick is
    ``TAXONOMY``, because it is the only rebuildable member, and picking it says
    "yes, this tree can be rebuilt" about a tree nobody checked. That sentence is
    only ever discovered to be false at the one moment it matters, which is after
    a restore has already left the tree short and the one-way door has shut.
    :class:`TreeRecord` refuses a native record with no source for the same
    reason, so a default here would be this module handing out through a
    parameter exactly what it refuses one class up.

    THE COST OF THAT DECISION IS A CALL SITE IN ANOTHER UNIT, stated here rather
    than discovered at merge. U32 added a fixture call to this function after
    this parameter existed but before the two branches met, so on the merged tree
    ``tests/test_restore.py`` raises ``TypeError: record_cutover() missing 1
    required keyword-only argument: 'source'`` in two tests. Whoever merges adds
    ``source=DerivationSource.TAXONOMY`` to that fixture. A missing argument that
    stops the suite is the outcome this signature is FOR; the alternative was a
    silent default writing an unchecked claim about a real library into a
    one-way record.
    """
    if not root_id:
        raise ValueError(
            f"recording a cutover for {tree_id!r} needs the identifier of the "
            f"root it adopted; without one, a pre-cutover database restored "
            f"underneath this registry cannot be detected"
        )
    assert_rebuildable(tree_id, source)
    with config._exclusive_lock(lock_path(cfg)):
        updated = read(cfg).with_record(
            TreeRecord(
                tree_id=tree_id,
                mode=Mode.DATABASE,
                cutover_on=on,
                root_id=str(root_id),
                source=source,
            )
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


def assert_rebuildable(tree_id: str, source: DerivationSource | None) -> None:
    """Refuse a cutover for a tree whose membership nothing could rebuild (R39).

    Two refusals rather than one, because the two are different mistakes with
    different answers. A source this build does not recognise is a registry
    written by hand or by a newer build, and the answer is to fix the file. A
    source that is recognised and simply is not reproducible is a correct
    declaration about a tree that must stay on the bridge, and the answer is to
    leave it there.

    THE REFUSAL IS SCOPED TO THE TREE, never to the product. A library may hold
    one tree the taxonomy fully describes beside another that a person curates by
    hand, and the second one refusing to flip says nothing at all about the first.
    """
    if source is None or source not in frozenset(DerivationSource):
        raise TreeModeRefused(
            f"the tree {tree_id!r} names no derivation source this build "
            f"recognises, so nothing can say where a rebuild of its membership "
            f"would come from; a tree that cannot be rebuilt cannot be repaired "
            f"after a restore, and a cutover is a one-way door",
            tree_id=tree_id,
            mode=Mode.XML,
            attempted=Mode.DATABASE,
            remedy=Remedy.FIX_CONFIG_VALUES,
        )
    if source not in REBUILDABLE:
        raise TreeModeRefused(
            f"the tree {tree_id!r} derives its membership from {str(source)!r}, "
            f"which no rebuild can reproduce, so it stays on the XML bridge; a "
            f"catalogue crawl answers differently every month and a curated "
            f"playlist derives from nothing this product declares, and a native "
            f"tree that a restore leaves short has no other repair path",
            tree_id=tree_id,
            mode=Mode.XML,
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
    "LOCK_KEY",
    "MODES",
    "NOT_REBUILDABLE",
    "REBUILDABLE",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "DerivationSource",
    "Mode",
    "Registry",
    "RegistrySkew",
    "TreeModeRefused",
    "TreeRecord",
    "TreeRegistryUnreadable",
    "anchored_root",
    "assert_rebuildable",
    "lock_path",
    "path_for",
    "read",
    "record_cutover",
    "refuse_bridge_write",
    "refuse_database_write",
    "write",
]
