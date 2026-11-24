"""The static verb registry: one table, lazily imported, fully introspectable (KTD7).

The rows live in the ``registry_*`` parts beside this module, which assembles
them into ``ENTRIES`` (U328), so no file of it passes 1,500 lines. Nothing here
imports a verb's module: ``module`` and ``builder`` are strings, imported
only when the module is enabled and its subcommand is built, and a missing extra
becomes a stub, so ``crate --help`` works on a slim install. Every entry carries
the metadata the conformance suite needs, so a new verb fails the build by
omission rather than by review. A ``planned_in`` entry is declared but not
landed, and ``tests/test_cli_contract.py`` expires the marker once its module
exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from cratekit.core import profiles
from cratekit.modules import extras as _extras

#: The distribution name for a missing extra's install command, spelled once in
#: ``modules.extras`` so a rename cannot desynchronize the workers and the CLI.
DISTRIBUTION = _extras.DISTRIBUTION


@dataclass(frozen=True, slots=True)
class GateSpec:
    """A decision point, declared statically rather than asked at a prompt.

    ``name`` is a stable identifier, never a prompt string, so an answer cannot
    drift onto another question when prompts are reordered. ``explicit`` marks
    a gate answerable only by a separate recorded act, never inline, by config
    or by environment (R34). ``digest_source`` names the artifact the decision
    binds to, so a plan that moves after approval makes the decision stale.
    """

    name: str
    options: tuple[str, ...]
    prompt: str
    explicit: bool = False
    digest_source: str | None = None

    def __post_init__(self) -> None:
        if len(self.options) < 2:
            raise ValueError(f"gate {self.name!r} needs at least two options to be a decision")
        if len(set(self.options)) != len(self.options):
            raise ValueError(f"gate {self.name!r} repeats an option")


#: What a verb may declare it writes. ``files`` and ``remote`` are included
#: because the destructive gates bind to destruction, not database writes (KTD24).
WRITE_SURFACES: frozenset[str] = frozenset({"db_tree", "db_metadata", "xml", "files", "remote"})

#: The surfaces written through the guarded rekordbox writer. A verb declaring
#: one must declare the cloud sync decision; derived here once, not re-listed (P3).
DB_WRITE_SURFACES: frozenset[str] = frozenset({"db_tree", "db_metadata"})

#: The decision reached when the guarded writer cannot read Cloud Library Sync
#: state, declared once and shared by every ``DB_WRITE_SURFACES`` verb. Explicit
#: (R34), and unscoped because a decision is recorded against the run's own verb.
CLOUD_SYNC_UNREADABLE_GATE = GateSpec(
    name="write.cloudsync.unreadable",
    options=("proceed", "abort"),
    prompt="Cloud Library Sync state could not be read; proceed anyway?",
    explicit=True,
)

#: The five structured-output surfaces R32 names.
EMIT_SURFACES: frozenset[str] = frozenset(
    {"plan", "match", "review_set", "job_state", "diagnostic"}
)


@dataclass(frozen=True, slots=True)
class Entry:
    """One verb, and every property the conformance suite asserts about it."""

    name: str
    summary: str
    module: str
    builder: str
    handler_key: str

    #: The Feature Inventory rows this verb satisfies, read by the parity check;
    #: a Cut row claimed by a verb fails the build.
    feature_rows: tuple[int, ...] = ()
    #: The source system's console scripts this verb replaces, the half of
    #: parity for scripts with no Feature Inventory row.
    source_scripts: tuple[str, ...] = ()

    #: The feature module that gates this verb, or None when it is core. The
    #: profile decides membership (D6); this names which verb it switches.
    module_id: str | None = None
    extras: str | None = None
    #: Third-party top-level modules the extras group provides. The stub fires
    #: only on these, so a defect in our own code is never reported as a missing extra.
    extras_modules: tuple[str, ...] = ()

    argv_builder: str | None = None
    interactive: bool = False

    emits: frozenset[str] = frozenset()
    output_schema: str | None = None
    gates: tuple[GateSpec, ...] = ()
    adjudicates: bool = False
    long_running: bool = False
    destructive: bool = False
    writes: frozenset[str] = frozenset()
    taxonomy_terms: tuple[str, ...] = ()
    doctor_checks: tuple[str, ...] = ()

    #: The unit that lands ``module``. None means it is here now.
    planned_in: str | None = None

    def __post_init__(self) -> None:
        problems: list[str] = []
        if not self.name.replace(".", "").replace("-", "").islower():
            problems.append("a verb name is lowercase dotted, never mixed case")
        if bool(self.emits) != bool(self.output_schema):
            problems.append(
                "a verb that emits a structured surface declares its schema, and "
                "one that declares a schema emits something (R32)"
            )
        if not self.emits <= EMIT_SURFACES:
            problems.append(f"undeclared emit surfaces: {sorted(self.emits - EMIT_SURFACES)}")
        if not self.writes <= WRITE_SURFACES:
            problems.append(f"undeclared write surfaces: {sorted(self.writes - WRITE_SURFACES)}")
        if (self.extras is None) != (not self.extras_modules):
            problems.append(
                "an extras group names the third-party modules it provides, or "
                "the stub cannot tell a missing extra from a defect in our own code"
            )
        # The stub prints ``extras`` as the install command, so it must name a
        # group pyproject declares, named one to one with its module (KTD7, R-4).
        if self.extras is not None and self.extras != self.module_id:
            problems.append(
                f"the extras group {self.extras!r} is not this verb's own module "
                f"{self.module_id!r}, and extras are named one to one with "
                "modules (KTD7)"
            )
        if self.extras is not None and self.extras not in profiles.EXTRAS_BACKED:
            problems.append(
                f"{self.extras!r} has no extras group in profiles.EXTRAS_BACKED, "
                "so the stub would print an install command for a group "
                "pyproject does not declare"
            )
        if ("files" in self.writes or self.name.startswith("delete.")) and not self.destructive:
            problems.append(
                "anything that writes files or deletes is destructive by "
                "definition (KTD24); the destructive-session gates bind to that "
                "flag, so a verb that lies here runs without them"
            )
        if self.long_running and not self.argv_builder:
            problems.append(
                "long-running work is queued and re-invoked as a subprocess "
                "(KTD26), which needs an argv builder to turn its frozen payload "
                "back into a command line"
            )
        if self.module_id is not None and self.module_id not in _KNOWN_MODULES:
            problems.append(
                f"{self.module_id!r} is not a declared feature module; "
                f"declared: {', '.join(sorted(_KNOWN_MODULES))}"
            )
        if self.planned_in is not None and not (
            self.planned_in.startswith("U") and self.planned_in[1:].isdigit()
        ):
            problems.append(f"{self.planned_in!r} is not a unit identifier")
        if problems:
            raise ValueError(
                f"registry entry {self.name!r} cannot register:\n"
                + "\n".join(f"  - {p}" for p in problems)
            )

    @property
    def landed(self) -> bool:
        """True when this verb's module exists in this build."""
        return self.planned_in is None

    @property
    def path(self) -> tuple[str, ...]:
        """The subcommand path a user types, as words."""
        return tuple(self.name.split("."))

    def available_to(self, membership: profiles.Membership) -> bool:
        """Whether this profile switches the verb on. Core verbs always are."""
        return self.module_id is None or self.module_id in membership.available


_KNOWN_MODULES: frozenset[str] = frozenset(profiles.MODULES) | profiles.ALWAYS_AVAILABLE


# ---------------------------------------------------------------------------
# The Feature Inventory, declared so parity is checkable rather than asserted
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Feature:
    """One Feature Inventory row: what it is and what the plan decided about it."""

    row: int
    title: str
    disposition: str  # core | module | reshaped | cut | defer


#: The plan's Feature Inventory, transcribed so the parity check runs without the
#: plan document. A ``core`` row needs no module, a ``module`` row is gated by
#: one, and a ``cut`` or ``defer`` row has no verb.
FEATURES: tuple[Feature, ...] = (
    Feature(1, "mix URL set identification", "module"),
    Feature(2, "tracklist intake", "module"),
    Feature(3, "streaming playlist import", "core"),
    Feature(4, "single file ingest", "core"),
    Feature(5, "identification only, no downloads", "module"),
    Feature(6, "vendored concurrent downloader", "core"),
    Feature(7, "fallback lossy acquisition", "module"),
    Feature(8, "genre and album art tagging", "core"),
    Feature(9, "audio analysis: key, BPM, energy", "module"),
    Feature(10, "vocal detection", "module"),
    Feature(11, "naming engine", "core"),
    Feature(12, "guarded database writes, per surface", "core"),
    Feature(13, "playlist routing to the declared taxonomy", "core"),
    Feature(14, "intake sorting and unplaced audit", "core"),
    Feature(15, "duplicate audit", "module"),
    Feature(16, "camelot padding pass", "cut"),
    Feature(17, "filename and path repair", "module"),
    #: Flipped from Cut (U40): tagging is fill if empty, so without this no verb
    #: can ever correct a coarse genre. Kept in step with the plan's row 18.
    Feature(18, "genre correction for a tag already too coarse", "module"),
    Feature(19, "streamed-track playlist scan", "cut"),
    Feature(20, "intake aging report", "module"),
    Feature(21, "favourite label registry and sweeps", "module"),
    Feature(22, "label import and label harvest", "module"),
    #: Flipped from Defer (R-835): the folder per label is otherwise lost when
    #: the source system retires.
    Feature(23, "label to streaming playlist folders", "module"),
    Feature(24, "hearted-track sync with auto-acquire", "module"),
    Feature(25, "sync orchestrator", "reshaped"),
    Feature(26, "embedded job engine", "core"),
    Feature(27, "setup wizard, config, profiles", "core"),
    Feature(28, "doctor and status diagnostics", "core"),
    Feature(29, "set builder", "module"),
    Feature(30, "set recording mastering", "module"),
    Feature(31, "library backup", "module"),
    Feature(32, "web dashboard and desktop application", "defer"),
    Feature(33, "operator skill layer", "module"),
    Feature(34, "library adoption", "module"),
    Feature(35, "public streaming playlist intake", "core"),
    Feature(36, "playlist export to a streaming service", "module"),
    Feature(37, "track deletion and tombstones", "module"),
)

#: Module rows realized as a configured policy rather than a toggle, named rather
#: than silently exempted. R21 makes lossy acquisition a marked policy value.
POLICY_ROWS: Mapping[int, str] = MappingProxyType(
    {7: "R21 makes this acquisition.lossless_policy, not a module toggle"}
)

#: Module toggles with no verb behind them: Feature 32 is deferred, not deleted.
#: Named so the "every toggle is used" check can tell them from a forgotten gate.
DEFERRED_MODULES: frozenset[str] = frozenset({"web", "desktop"})

#: The unit that lands ``cratekit.write.routing_cli``, named once so its four
#: entries move together. U20, the first unit to ship a destructive database
#: surface; ``tests/_pending.py`` holds the obligation (P5).
ROUTING_CLI_UNIT = "U20"

#: The unit that lands ``cratekit.cli.rebuild``. ``rebuild`` writes ``db_tree``
#: and rides with U20 as the route verbs do; ``converge`` landed apart (U36).
REBUILD_CLI_UNIT = "U20"
#: The unit that landed ``cratekit.cli.reports``, kept as the record of why its
#: four verbs live under ``cli`` (a modules path would import upward) and U27.
REPORTS_CLI_UNIT = "U27"
#: The unit that landed ``cratekit.adopt.apply_cli``. ``adopt.apply`` has a module
#: of its own so its countdown is about itself; ``adopt.scan`` landed apart.
ADOPT_APPLY_CLI_UNIT = "U27"
#: Where ``repair.paths`` lives and the unit that owns it: path repair is U37's,
#: and its own module keeps the doctor module's countdown off it.
REPAIR_CLI_MODULE = "cratekit.intake.repair_cli"
REPAIR_CLI_UNIT = "U37"


# ---------------------------------------------------------------------------
# The verbs
# ---------------------------------------------------------------------------
#
# Ordered by surface, not alphabetically, since a reader asks what the product
# can do about X, then by landing: the table is one literal tuple per part, each
# a contiguous slice in a module beside this one (U328), imported here because
# a part reads the names above. Two scripts read the parts as text
# (``refactor_measure.py`` ``verbs_from``, ``board.py`` ``planned_units``), so
# ``ENTRIES`` stays a tuple of starred part names and a part a tuple of calls.

from cratekit.cli.registry_later import LATER_VERBS  # noqa: E402
from cratekit.cli.registry_modules import MODULE_VERBS  # noqa: E402
from cratekit.cli.registry_pipeline import PIPELINE_VERBS  # noqa: E402
from cratekit.cli.registry_state import STATE_VERBS  # noqa: E402
from cratekit.cli.registry_sync import SYNC_VERBS  # noqa: E402

ENTRIES: tuple[Entry, ...] = (
    *STATE_VERBS,
    *PIPELINE_VERBS,
    *SYNC_VERBS,
    *MODULE_VERBS,
    *LATER_VERBS,
)

#: The verb names, read by ``tests/test_layering.py`` so no layer below the CLI
#: names a verb, from here so the guard cannot fall behind the registry.
VERB_NAMES: frozenset[str] = frozenset(entry.name for entry in ENTRIES)

_BY_NAME: Mapping[str, Entry] = MappingProxyType({entry.name: entry for entry in ENTRIES})
_BY_HANDLER: Mapping[str, Entry] = MappingProxyType({entry.handler_key: entry for entry in ENTRIES})

if len(_BY_NAME) != len(ENTRIES):  # pragma: no cover - a duplicate fails at import
    raise ValueError("two registry entries share a name")
if len(_BY_HANDLER) != len(ENTRIES):  # pragma: no cover - same
    raise ValueError("two registry entries share a handler key")


def entries() -> tuple[Entry, ...]:
    """Every declared verb, landed or planned."""
    return ENTRIES


def landed_entries() -> tuple[Entry, ...]:
    """Only the verbs whose module exists in this build."""
    return tuple(entry for entry in ENTRIES if entry.landed)


def entry(name: str) -> Entry:
    """One verb by name, or raise naming what is registered."""
    try:
        return _BY_NAME[name]
    except KeyError:
        raise KeyError(
            f"{name!r} is not a registered verb. A verb reachable from the CLI "
            f"but absent from the registry is invisible to every conformance "
            f"assertion, which is the failure the registry exists to prevent."
        ) from None


def by_handler_key(key: str) -> Entry:
    """One verb by the key the job engine re-invokes it with.

    It imports nothing (KTD26), so validating a queued handler keeps the lazy stubs.
    """
    try:
        return _BY_HANDLER[key]
    except KeyError:
        raise KeyError(f"{key!r} is not a registered handler key") from None


def features_by_row() -> Mapping[int, Feature]:
    """The Feature Inventory, indexed by row."""
    return MappingProxyType({feature.row: feature for feature in FEATURES})


def gate(name: str) -> tuple[Entry, GateSpec]:
    """Find a declared gate and the verb that owns it."""
    for item in ENTRIES:
        for spec in item.gates:
            if spec.name == name:
                return item, spec
    raise KeyError(
        f"{name!r} is not a declared gate. Gates are declared statically on the "
        f"registry entry that raises them, so a decision can be recorded before "
        f"the verb that consumes it ever runs."
    )


__all__ = [
    "CLOUD_SYNC_UNREADABLE_GATE",
    "DB_WRITE_SURFACES",
    "DEFERRED_MODULES",
    "DISTRIBUTION",
    "EMIT_SURFACES",
    "ENTRIES",
    "FEATURES",
    "POLICY_ROWS",
    "REBUILD_CLI_UNIT",
    "REPAIR_CLI_MODULE",
    "REPAIR_CLI_UNIT",
    "ROUTING_CLI_UNIT",
    "VERB_NAMES",
    "WRITE_SURFACES",
    "Entry",
    "Feature",
    "GateSpec",
    "by_handler_key",
    "entries",
    "entry",
    "features_by_row",
    "gate",
    "landed_entries",
]
