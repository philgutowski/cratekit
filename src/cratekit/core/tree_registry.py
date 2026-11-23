"""Which medium owns each tree, and the cutover that moves one (KTD22, R14, R19).

Each tree is written either by the XML bridge or natively into the database,
and the wrong one is silent: rekordbox merges a spliced tree the database owns
into a second copy. This record is the input both guards read.

All trees start on the bridge; a cutover is a migration, not a setup choice.
The record is library-scoped, never committed, and COUPLED to the database, so
one snapshot carries both or neither (KTD22). It carries the adopted root's
identifier, so a database restored from before the cutover is a refusal rather
than a silent parallel tree. The inverse check lives here too, so both
directions are one rule; tests/test_tree_registry.py holds the database tree
writers to calling it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from cratekit.core import config, session, snapshot
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - typing only
    from cratekit.core.taxonomy import Taxonomy

#: The state entry this module owns.
STATE_KEY = "tree_registry"

#: The lock serializing ``record_cutover``, a declared entry so the inventory knows it.
LOCK_KEY = "tree_registry_lock"

#: Bumped only on an incompatible change; a newer file is refused, not guessed.
#: Version 2 requires a derivation source on a native record (R39).
SCHEMA_VERSION = 2


class Mode(StrEnum):
    """The medium that owns a tree's membership writes. A closed set."""

    #: The XML bridge: bytes spliced into an export the user re-imports.
    XML = "xml"
    #: Native database writes, after this tree's cutover was recorded.
    DATABASE = "database"


#: Every mode this build understands, derived from the enum.
MODES: tuple[str, ...] = tuple(m.value for m in Mode)


class DerivationSource(StrEnum):
    """Where a tree's FULL membership comes from, if it can be re-derived at all.

    R39's cutover precondition. A native tree left short by a restore has one
    repair path, a full rebuild, so a tree no declared source can reproduce
    must never flip. A catalogue crawl answers differently month to month and a
    curated playlist derives from nothing declared, so both stay on the bridge.
    """

#: The declared taxonomy applied to what is on disk. Reproducible.
    TAXONOMY = "taxonomy"

#: One folder per catalogued source, built from a crawl. NOT reproducible.
    CATALOGUE_CRAWL = "catalogue-crawl"

#: A person's own or hearts-driven playlist. NOT reproducible.
    CURATED = "curated"


#: The only sources a tree may cut over on (R39). LISTED, so an unclassified
#: new member lands in the not-rebuildable set by default.
REBUILDABLE: frozenset[DerivationSource] = frozenset({DerivationSource.TAXONOMY})

#: Everything else, derived so the two halves cannot both miss a member (P3).
NOT_REBUILDABLE: frozenset[DerivationSource] = frozenset(DerivationSource) - REBUILDABLE

#: Where every tree starts.
DEFAULT_MODE: Mode = Mode.XML


def cutover_trees(declared: Taxonomy) -> frozenset[str]:
    """The trees a cutover may record, by stable identifier (R-787).

    THE ONE OWNER OF THE ANSWER, asked by the cutover verb and the health report
    alike. Both trees are recorded with the taxonomy as source (R-746), so a
    tree with any other source gets a source of its own first, never a place
    here. The catalogue tree stays on the bridge (R39).
    """
    return frozenset({declared.tree.id, declared.intake.id})


class TreeRegistryUnreadable(CratekitError):
    """The registry file exists and cannot be understood.

    Never collapsed into "no record", which reads as "on the bridge" and sends
    a byte write at a tree the database owns. The remedy differs by cause.
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

    One type for both directions, always naming the tree. A ``CratekitError``
    so the boundary keeps the remedy, which differs by direction (S4).
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

    A pre-cutover database beside a registry not rolled back with it; trusting
    the mode alone would create a second root. Remedy is a restore.
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

    ``tree_id`` is the stable identifier, never a display name, since a rename
    would orphan the record (R19, D5). ``root_id`` and ``source`` are None on
    the bridge and required once native; a missing source is refused, not
    defaulted, because a default would claim an unchecked rebuild path.
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
            # The reverse contradiction: a bridge mode carrying cutover fields,
            # which every consumer would misread as on the bridge.
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


def by_tree_id(entries, tree_id: str):
    """The one of ``entries`` recorded for ``tree_id``, or None.

    A scan, so no reader is handed a mapping to key on a name.
    """
    for entry in entries:
        if entry.tree_id == tree_id:
            return entry
    return None


@dataclass(frozen=True, slots=True)
class Registry:
    """Every record the registry holds. A tree with no record is on the bridge.

    A tuple, not a mapping, so no identifier sits in a key position (R19).
    """

    trees: tuple[TreeRecord, ...] = ()

    def record(self, tree_id: str) -> TreeRecord | None:
        return by_tree_id(self.trees, tree_id)

    def mode(self, tree_id: str) -> str:
        """The medium that owns ``tree_id``. Unrecorded means the bridge."""
        entry = self.record(tree_id)
        return DEFAULT_MODE if entry is None else entry.mode

    def is_database_native(self, tree_id: str) -> bool:
        return self.mode(tree_id) == Mode.DATABASE

    def derivation_source(self, tree_id: str) -> DerivationSource | None:
        """Where a rebuild of this tree's membership would come from, if anywhere.

        None on the bridge, never None for a native tree.
        """
        entry = self.record(tree_id)
        return None if entry is None else entry.source

    def database_native_trees(self) -> tuple[str, ...]:
        """Every tree the database owns, which is the set a restore endangers.

        Derived from the records, so a recently flipped tree is never missed.
        """
        return tuple(
            entry.tree_id for entry in self.trees if entry.mode == Mode.DATABASE
        )

    def is_on_the_bridge(self, tree_id: str) -> bool:
        return self.mode(tree_id) == Mode.XML

    def tree_ids(self) -> tuple[str, ...]:
        return tuple(entry.tree_id for entry in self.trees)

    def with_record(self, record: TreeRecord) -> Registry:
        """This registry plus ``record``, replacing any record for the same tree. Pure."""
        kept = tuple(e for e in self.trees if e.tree_id != record.tree_id)
        return Registry(tuple(sorted((*kept, record), key=lambda e: e.tree_id)))

    def without_record(self, tree_id: str) -> Registry:
        """This registry with ``tree_id`` back on the bridge.

        A revert only before the tree has taken a native write.
        """
        kept = tuple(entry for entry in self.trees if entry.tree_id != tree_id)
        return Registry(kept)


#: The registry every library starts with, and what an absent file resolves to.
EMPTY = Registry()


def path_for(cfg: config.Config) -> Path:
    """Where the registry lives, through the inventory so it is snapshotted."""
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """Where the registry's lock lives, a declared entry the inventory knows."""
    return config.state_path(LOCK_KEY, cfg)


def read(cfg: config.Config) -> Registry:
    """The effective registry for this library. An absent file is the empty one.

    Takes a ``Config`` so it reads the file the writers use (P2).
    """
    return read_path(path_for(cfg))


def read_path(path: Path) -> Registry:
    """The registry held at one named file.

    Only for a restore comparing a capture's registry with the live one; split
    from :func:`read` so a path is never passed by accident.
    """

    def unusable(message: str, *, remedy: Remedy = Remedy.RUN_DOCTOR) -> TreeRegistryUnreadable:
        return TreeRegistryUnreadable(message, path=path, remedy=remedy)

    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise unusable(f"{path} exists but could not be read: {exc}") from exc

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

    entries = data.get("trees")
    if not isinstance(entries, list):
        raise unusable(f"{path} has no trees array")

    records: list[TreeRecord] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise unusable(f"{path} holds a tree entry that is not an object")
        tree_id = entry.get("tree")
        if not isinstance(tree_id, str) or not tree_id.strip():
            raise unusable(
                f"{path} holds a tree entry with no identifier; a record that "
                f"cannot say which tree it describes is worse than no record",
            )
        if tree_id in seen:
            # Two answers for one tree are refused, never resolved by line order.
            raise unusable(
                f"{path} holds two records for the tree {tree_id!r}; a registry "
                f"that gives two answers for one tree cannot say which medium "
                f"owns it, and guessing decides which writer runs against a "
                f"real library",
            )
        seen.add(tree_id)
        stamp = entry.get("cutover_on")
        cutover: date | None = None
        if stamp is not None:
            try:
                cutover = date.fromisoformat(str(stamp))
            except (TypeError, ValueError) as exc:
                raise unusable(
                    f"{path} records {tree_id!r} as cutting over on {stamp!r}, "
                    f"which is not an ISO date",
                ) from exc
        root_id = entry.get("root")
        raw_source = entry.get("source")
        raw_mode = entry.get("mode")
        if raw_mode is None:
            # NO DEFAULT: XML would read a cut over tree as on the bridge and
            # empty the restore detector's input.
            raise unusable(
                f"{path} holds a record for {tree_id!r} with no mode; the medium "
                f"that owns a tree is the one thing this file exists to say, and "
                f"the value it would default to sends the bridge writer at a tree "
                f"the database may already own and switches the restore detector "
                f"off for every tree in this library",
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
            # Refused, not dropped, since a dropped record reads as on the bridge.
            raise unusable(f"{path} holds an unusable record: {exc}") from exc

    return Registry(tuple(sorted(records, key=lambda e: e.tree_id)))


def write(cfg: config.Config, registry: Registry) -> Path:
    """Persist ``registry`` for this library, atomically and owner only.

    The directory mode matters as much as the file's (P1).
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
            # Sorted so the bytes are a function of the content alone.
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

    Read, modify, write under an exclusive lock, so concurrent flips cannot
    lose one; a lost flip sends the tree's next write through the bridge.
    Rebuildability is checked here, before the one-way door (U9's A2 verdict).
    ``source`` has no default, because the only possible default claims an
    unchecked rebuild path.
    """
    if not root_id:
        raise ValueError(
            f"recording a cutover for {tree_id!r} needs the identifier of the "
            f"root it adopted; without one, a pre-cutover database restored "
            f"underneath this registry cannot be detected"
        )
    assert_rebuildable(tree_id, source)
    with config.exclusive_lock(lock_path(cfg)):
        current = read(cfg)
        standing = current.record(tree_id)
        if standing is not None and standing.mode == Mode.DATABASE:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
            raise refuse(
                "cutover-already-recorded",
                f"the tree {tree_id!r} is already recorded as database native, "
                f"anchored to root {standing.root_id!r} since "
                f"{standing.cutover_on}; recording it again would move the "
                f"anchor or the day under a tree that may have taken writes",
                steps=("leave the record as it is; a tree cuts over once",),
                scope=Scope.RUN,
                origin=("tree_registry",),
                detail={
                    "tree_id": tree_id,
                    "root_id": standing.root_id,
                    "cutover_on": str(standing.cutover_on),
                    "asked_root_id": str(root_id),
                },
            )
        updated = current.with_record(
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


#: Intake XML names this product writes and a person still has to import.
PENDING_XML_SUFFIXES: tuple[str, ...] = (
    "_synced.xml",
    "_inboxed.xml",
    "_favorites.xml",
)


def pending_intake_xml(cfg: config.Config) -> tuple[Path, ...]:
    """Every un-imported intake XML sitting in this library or its staging.

    A Fresh Export is not in the set. The U22 ``*_synced.xml`` stub counts,
    because a cutover over debris starts dirty.
    """
    roots = (Path(cfg.library.root), Path(cfg.paths.download_staging))
    found: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.xml"):
            name = path.name
            if any(name.endswith(suffix) for suffix in PENDING_XML_SUFFIXES):
                found.append(path)
    return tuple(sorted(found))


@dataclass(frozen=True, slots=True)
class PrecheckResult:
    """One precheck's answer: which check, and the refusal it gave, if any.

    ``refusal`` is the whole exception, so reports show its own wording.
    """

    check: str
    refusal: CratekitError | None = None

    @property
    def passed(self) -> bool:
        return self.refusal is None

    @property
    def cause(self) -> Cause | None:
        return None if self.refusal is None else self.refusal.cause


def _whole_log(cfg: config.Config, *, so: str) -> tuple[session.SessionRecord, ...]:
    """Every session record, or a refusal when one of them could not be read.

    A gate that skipped an unreadable record would fail open. ``so`` finishes
    the sentence with what was not established.
    """
    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
        raise refuse(
            "internal-error",
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
            "writing the tree registry against a log it cannot read",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("tree_registry",),
            detail={
                "unreadable": [str(path) for path in unreadable],
                "unlisted": session.log_unlisted(unreadable, cfg),
            },
        )
    return parsed


def _open_runs(records: tuple[session.SessionRecord, ...]) -> list[session.SessionRecord]:
    """The runs that have not reached a terminal state and still owe something.

    A run owing only a deferred placement is not one (R-501).
    """
    return [
        record
        for record in records
        if not record.terminal and not session.owes_only_deferred_routing(record)
    ]


def _open_run_refusal(cfg: config.Config, export: Path) -> CratekitError | None:
    """An open run still holds a capture, and possibly an un-imported export."""
    del export
    open_runs = _open_runs(
        _whole_log(cfg, so="whether a run is still open was not established")
    )
    if not open_runs:
        return None
    first = open_runs[0]
    # The run's own steps when it has them, since this layer may not name a verb.
    owed: list[str] = []
    for record in open_runs:
        for step in record.pending.steps if record.pending is not None else ():
            if step not in owed:
                owed.append(step)
    if any(record.pending is None for record in open_runs):
        # The general wording for a run with no recorded action.
        owed.extend(
            (
                "close or abandon every open run",
                "import any export a run left in awaiting-import, then close it",
            )
        )
    return refuse(
        "cutover-open-run",
        f"session {first.session_id} has not reached a terminal state, so "
        f"a cutover would flip a tree while that run still holds a capture "
        f"and possibly an un-imported export",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=tuple(owed),
        scope=Scope.RUN,
        origin=("tree_registry",),
        detail={
            "sessions": [record.session_id for record in open_runs],
            "states": {record.session_id: str(record.state) for record in open_runs},
        },
    )


def _pending_xml_refusal(cfg: config.Config, export: Path) -> CratekitError | None:
    """An un-imported intake XML is work the next sync will try to consume."""
    del export
    pending = pending_intake_xml(cfg)
    if not pending:
        return None
    return refuse(
        "cutover-xml-pending",
        f"{len(pending)} un-imported intake XML file(s) are still sitting "
        f"in this library, so a cutover would proceed over work the next "
        f"run will try to consume",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=(
            "import or remove each pending intake XML",
            "do not treat a U22 stub listing as an importable splice",
        ),
        scope=Scope.RUN,
        origin=("tree_registry",),
        detail={"paths": [str(path) for path in pending]},
    )


def _export_refusal(cfg: config.Config, export: Path) -> CratekitError | None:
    """A Fresh Export is the XML-era fallback if the flip is walked back."""
    del cfg
    export_path = Path(export)
    if export_path.is_file() and export_path.stat().st_size != 0:
        return None
    return refuse(
        "cutover-export-missing",
        "a Fresh Export has to exist before a tree flips, so a failed "
        "validation still has an XML-era copy of the tree to walk back to",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=("take a Fresh Export from rekordbox and pass that file in",),
        scope=Scope.RUN,
        origin=("tree_registry",),
        detail={"export": str(export_path)},
    )


def _snapshot_refusal(cfg: config.Config, export: Path) -> CratekitError | None:
    """A verified snapshot is the restore target if validation fails."""
    del export
    store = snapshot.store_root(cfg)
    if store.is_dir():
        for child in store.iterdir():
            if not child.is_dir():
                continue
            try:
                record = snapshot.read_manifest(child)
            except CratekitError:
                continue
            if record.verified:
                return None
    return refuse(
        "cutover-snapshot-missing",
        "no verified snapshot exists for this library, so a failed "
        "cutover would have nothing to restore from in the same session",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=("take a library snapshot before flipping a tree",),
        scope=Scope.RUN,
        origin=("tree_registry",),
        detail={"store": str(store)},
    )


#: The precheck checks IN THE ORDER THEY REFUSE, one table for the assertion and
#: the report (P3). The name is for display only.
CUTOVER_CHECKS: tuple[
    tuple[str, Callable[[config.Config, Path], CratekitError | None]], ...
] = (
    ("no-open-run", _open_run_refusal),
    ("no-pending-intake-xml", _pending_xml_refusal),
    ("fresh-export", _export_refusal),
    ("verified-snapshot", _snapshot_refusal),
)


def cutover_precheck(cfg: config.Config, *, export: Path) -> tuple[PrecheckResult, ...]:
    """Every precheck's answer, without raising.

    The report half of :func:`assert_cutover_ready`, over the same table. Not
    the guard: :func:`flip` asserts for itself.
    """
    target = Path(export)
    results: list[PrecheckResult] = []
    for name, check in CUTOVER_CHECKS:
        results.append(PrecheckResult(check=name, refusal=check(cfg, target)))
    return tuple(results)


def assert_cutover_ready(cfg: config.Config, *, export: Path) -> None:
    """Refuse a flip while the library still owes an act or has no undo.

    The export is a path the caller names, never hunted for, since a hunt
    would pick pending debris. The first refusal in :data:`CUTOVER_CHECKS`
    order is raised.
    """
    target = Path(export)
    for _name, check in CUTOVER_CHECKS:
        refusal = check(cfg, target)
        if refusal is not None:
            raise refusal


def flip(
    cfg: config.Config,
    tree_id: str,
    *,
    root_id: str,
    on: date,
    source: DerivationSource,
    export: Path,
) -> Registry:
    """Precheck, then record one tree as database-native, as one act."""
    assert_cutover_ready(cfg, export=export)
    return record_cutover(cfg, tree_id, root_id=root_id, on=on, source=source)


#: How far before the cutover day a session may start and still count as a
#: write under it, since the day is local and the start is UTC. Errs toward counting.
NATIVE_WRITE_MARGIN = timedelta(days=1)


def _predates(started: str, cutover_on: date | None) -> bool:
    """Whether a session provably started before the cutover it is judged against.

    Anything unparseable or inside the margin answers False.
    """
    if cutover_on is None:
        return False
    try:
        began = datetime.fromisoformat(str(started).replace("Z", "+00:00")).date()
    except ValueError:
        return False
    return began < cutover_on - NATIVE_WRITE_MARGIN


def native_writes(cfg: config.Config, tree_id: str) -> tuple[str, ...]:
    """The sessions that wrote ``tree_id`` natively under its standing cutover.

    Read off the session log, which survives a rollback; a record naming the
    tree with a positive count is a native write. The whole log or a refusal.
    Sessions provably before the standing cutover are left out. The answer is
    "a write was taken", never "the rows remain", the conservative direction.
    """
    standing = read(cfg).record(tree_id)
    cutover_on = None if standing is None else standing.cutover_on
    records = _whole_log(
        cfg, so=f"whether the tree {tree_id!r} has taken a native write was not established"
    )
    return tuple(
        record.session_id
        for record in records
        if not _predates(record.started, cutover_on)
        and any(
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
            for change in record.change.trees
        )
    )


def assert_revertible(cfg: config.Config, tree_id: str) -> None:
    """Refuse a revert once the tree has taken a native write, or may have.

    An open run refuses too, because a write records its commit only after
    committing.
    """
    taken = native_writes(cfg, tree_id)
    if taken:
        raise refuse(
            "cutover-native-write-taken",
            f"the tree {tree_id!r} has taken {len(taken)} native write(s) since "
            f"it cut over, so the database owns it and it cannot go back on the "
            f"XML bridge; the next export splice would be imported over rows "
            f"the export never held",
            steps=(
                "leave the tree database native",
                "to undo the writes themselves, restore a capture taken before "
                "the cutover, which carries the registry back with the database",
            ),
            scope=Scope.RUN,
            origin=("tree_registry",),
            detail={"tree_id": tree_id, "sessions": list(taken)},
        )
    open_runs = _open_runs(
        _whole_log(cfg, so="whether a run is still open was not established")
    )
    if open_runs:
        raise refuse(
            "cutover-open-run",
            f"session {open_runs[0].session_id} has not reached a terminal "
            f"state, so whether it wrote the tree {tree_id!r} natively is not "
            f"established and the tree cannot go back on the XML bridge yet",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=("close or abandon every open run, then revert",),
            scope=Scope.RUN,
            origin=("tree_registry",),
            detail={
                "tree_id": tree_id,
                "sessions": [record.session_id for record in open_runs],
                "states": {record.session_id: str(record.state) for record in open_runs},
            },
        )


def revert_cutover(cfg: config.Config, tree_id: str) -> Registry:
    """Put ``tree_id`` back on the bridge.

    Safe only before a native write (U9's A2 verdict); after one the way back
    is a restore. Guarded under the session lock and the registry lock, so it
    may not be called inside a destructive session.
    """
    with session.session_lock(cfg), config.exclusive_lock(lock_path(cfg)):
        assert_revertible(cfg, tree_id)
        updated = read(cfg).without_record(tree_id)
        write(cfg, updated)
    return updated


# The two guards. One rule, asked from each end.


def refuse_bridge_write(tree_id: str, registry: Registry) -> None:
    """Refuse a byte splice into a tree the database already owns, naming the tree."""
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

    The next import would overwrite whatever was written natively.
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

    An unrecognised source and a non-reproducible one are different mistakes
    with different remedies. Scoped to the tree, never the product.
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
    Three distinct refusals: still on the bridge, native with no root, or a root
    the library lacks (a restored pre-cutover database). ``root_exists`` is the
    caller's, so this module does no database input.
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

