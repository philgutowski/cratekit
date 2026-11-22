"""The static verb registry: one table, lazily imported, fully introspectable (KTD7).

Nothing here imports a module: ``module`` and ``builder`` are strings, imported
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
# can do about X. Later blocks are appended so concurrent branches conflict.

ENTRIES: tuple[Entry, ...] = (
    # ── Setup, profiles, and the run's own state (this unit) ────────────────
    Entry(
        name="profile.show",
        summary="show the active profile and which feature modules it switches on",
        module="cratekit.cli.verbs.profile", builder="build", handler_key="profile.show",
        feature_rows=(27,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=(),
    ),
    Entry(
        name="profile.set", summary="change the profile preset, and nothing else",
        module="cratekit.cli.verbs.profile", builder="build_set", handler_key="profile.set",
        feature_rows=(27,), emits=frozenset({"plan"}), output_schema="plan/1", writes=frozenset(),
        gates=(
            GateSpec(
                name="profile.set.apply", options=("apply", "abort"),
                prompt="Apply this change to module membership?", digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="run.show",
        summary="show a run's state, its outstanding gates, and any pending human action",
        module="cratekit.cli.verbs.runs", builder="build_show", handler_key="run.show",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="run.decide",
        summary="answer a named gate on a run, from any process and any later session",
        module="cratekit.cli.verbs.runs", builder="build_decide", handler_key="run.decide",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="run.retire",
        summary="answer abort on every open gate idle past a threshold, after one confirm",
        module="cratekit.cli.verbs.runs", builder="build_retire", handler_key="run.retire",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="run.retire.confirm", options=("apply", "abort"),
                prompt="Answer abort, as session, on each of these open gates?",
                #: Ordinary (U170): it writes only run state, only the answer no,
                #: and the digest binds the answer to the gates shown.
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="setup", summary="first-run wizard: library, credentials, taxonomy, profile",
        module="cratekit.cli.setup", builder="build", handler_key="setup", feature_rows=(27,),
        source_scripts=(),
        # Interactive, confined to one module so the static guard on standard
        # input can allow exactly one file.
        interactive=True, emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="doctor", summary="check the environment and report each failure with its fix",
        module="cratekit.cli.doctor", builder="build", handler_key="doctor", feature_rows=(28,),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="repair.paths",
        summary="propose a name for each file rekordbox would reject, and apply the accepted ones",
        module=REPAIR_CLI_MODULE, builder="build_repair_paths", handler_key="repair.paths",
        feature_rows=(17,), source_scripts=("dj-path-repair",), module_id="repair",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: Files only (U102): ``--apply`` renames accepted files. The database is
        #: only read, so no cloud sync decision, which a verb must reach to declare.
        writes=frozenset({"files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.paths.confirm", options=("apply", "abort"),
                prompt="Apply these accepted renames?", digest_source="plan",
            ),
        ),
    ),
    # ── A row's rekordbox defaults (R-923) ──────────────────────────────────
    Entry(
        name="repair.rows",
        summary=(
            "give each live library row rekordbox's own defaults where a "
            "column is empty, and its file's inode where the file id is random, so "
            "it loads to a deck; writes no file"
        ),
        module="cratekit.write.row_defaults_cli", builder="build", handler_key="repair.rows",
        # No feature row or source script: the source never created a row.
        # Gated by ``repair``, a corrective pass over rows the library holds.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The row only: ``rb_writer.CONTENT_ROW_DEFAULTS`` where NULL, and
        #: ``rb_writer.FILE_ID_COLUMN`` where the binding minted it (U115).
        writes=frozenset({"db_metadata"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.rows.confirm", options=("apply", "abort"),
                prompt="Give these rows rekordbox's own defaults?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The ContentLink probe (A32, R-928) ──────────────────────────────────
    Entry(
        name="repair.link",
        summary=(
            "write chosen values into the row probe columns, ContentLink "
            "and ISRC, of chosen live library rows, the experiment that asks which "
            "column keeps a landed row off a deck; writes no file"
        ),
        module="cratekit.write.row_link_cli", builder="build", handler_key="repair.link",
        # No feature row or source script; gated by ``repair`` as ``repair.rows`` is.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The named rows only, and only the ``rb_writer.ROW_PROBE_COLUMNS`` named.
        writes=frozenset({"db_metadata"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.link.confirm", options=("apply", "abort"),
                prompt="Write these probe values onto these rows?",
                #: Explicit (R34): a write to a row of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="status", summary="per-source sync state, open runs, and unconverged trees",
        module="cratekit.cli.doctor", builder="build_status", handler_key="status",
        feature_rows=(28,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="login", summary="record a provider credential in the OS keychain",
        module="cratekit.cli.verbs.login", builder="build", handler_key="login",
        feature_rows=(27,), source_scripts=("dj-tidal-login",), emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1", doctor_checks=("keychain.reachable",),
    ),
    # ── The write session and its safety spine ──────────────────────────────
    Entry(
        name="session.ack",
        summary="record the backup acknowledgment this destructive session needs",
        module="cratekit.session.cli", builder="build_ack", handler_key="session.ack",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.ack.backup", options=("acknowledged", "abort"),
                prompt="Database and music files are backed up; proceed?",
                # Explicit (R34): asserted per session by a named actor.
                explicit=True,
            ),
        ),
        # Landed with ``session.release`` (U49): one module string, one countdown.
    ),
    Entry(
        name="session.release", summary="release a library lock whose holder is gone, explicitly",
        module="cratekit.session.cli", builder="build_release", handler_key="session.release",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.release.confirm", options=("release", "abort"),
                prompt="Release the lock held by another installation?", explicit=True,
            ),
        ),
        # The prompt is asked even with no lock recorded, since conformance 3
        # holds every declared gate to firing (U49).
    ),
    Entry(
        name="restore.list",
        summary="list write sessions with their timestamp, workflow, and change summary",
        module="cratekit.session.restore_cli", builder="build_list", handler_key="restore.list",
        feature_rows=(12,), emits=frozenset({"review_set"}), output_schema="review_set/1",
        # Landed (U27); three of the nine conformance properties arm against it.
    ),
    Entry(
        name="restore.run",
        summary="restore a session snapshot, database and coupled state together",
        module="cratekit.session.restore_cli", builder="build_run", handler_key="restore.run",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        writes=frozenset({"db_tree", "db_metadata", "files"}), destructive=True,
        doctor_checks=("library.mounted", "library.identity", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="restore.run.confirm", options=("restore", "abort"),
                prompt="Restore this session, discarding everything after it?", explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        # Landed with its sibling above: one module.
    ),
    Entry(
        name="restore.bare-metal",
        summary="recover the mirror and the database onto a replacement drive",
        module="cratekit.session.restore_cli", builder="build_bare_metal",
        handler_key="restore.bare-metal", feature_rows=(12,), emits=frozenset({"plan"}),
        output_schema="plan/1", writes=frozenset({"files"}), destructive=True,
        doctor_checks=("rekordbox.closed",),
        # U96, a verb of its own because the library volume is gone. The library
        # checks are absent since this verb needs them to fail. No gate: one
        # could not end OK where the library is present, so
        # ``--accept-replacement``, refused without a terminal, is the explicit
        # act. No ``binary.rclone``, which would fail a slim core install; the
        # engine refuses by name instead. ``files``: the database is a copied file.
    ),
    Entry(
        name="converge",
        summary="report, per governed tree, whether declared membership matches the database",
        module="cratekit.cli.converge", builder="build", handler_key="converge",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=("library.mounted", "library.paths_resolved"),
    ),
    Entry(
        name="rebuild",
        summary="rebuild a governed tree's membership from declared sources and library truth",
        module="cratekit.cli.rebuild", builder="build", handler_key="rebuild", feature_rows=(12,),
        argv_builder="rebuild_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"db_tree"}), destructive=True,
        doctor_checks=(
            "library.mounted", "library.identity", "rekordbox.closed", "library.paths_resolved",
        ),
        gates=(
            CLOUD_SYNC_UNREADABLE_GATE,
            GateSpec(
                name="rebuild.accept", options=("accept", "abort"),
                prompt="Accept this tree as it stands? No rebuild can reproduce it.",
                #: Explicit (U219, R34): a named person disposes of a convergence
                #: refusal for a restored tree no rebuild can reproduce.
                explicit=True,
            ),
        ),
    ),
    # The two verbs over ``core.tree_registry`` (R-235). ``writes`` is empty:
    # they write this product's registry file and only read a database copy, so
    # no cloud sync decision. Not destructive, so no backup acknowledgment; the
    # precheck (verified snapshot, Fresh Export) and the explicit gate stand in.
    Entry(
        name="tree.cutover",
        summary="record one tree's cutover from the XML bridge to the database",
        module="cratekit.cli.cutover", builder="build", handler_key="tree.cutover",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        # ``tree.registry`` is not declared: it reports what these verbs record,
        # and an unreadable registry refuses both through the read itself.
        doctor_checks=("library.mounted", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="tree.cutover.approve", options=("approve", "abort"),
                prompt="Record this tree as database native, anchored to this root?",
                # One way: a revert undoes it only until the first native write.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tree.revert",
        summary="put a cut over tree back on the XML bridge, before its first native write",
        module="cratekit.cli.cutover", builder="build_revert", handler_key="tree.revert",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tree.revert.approve", options=("revert", "abort"),
                prompt="Put this tree back on the XML bridge?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── Jobs ────────────────────────────────────────────────────────────────
    # Under ``cli``, not ``core``: a verb module imports this registry (KTD23, U10).
    Entry(
        name="job.list", summary="list queued, running, blocked, and finished jobs",
        module="cratekit.cli.jobs", builder="build_list", handler_key="job.list",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    Entry(
        name="job.show", summary="show one job, its progress, and the cause behind its state",
        module="cratekit.cli.jobs", builder="build_show", handler_key="job.show",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    Entry(
        name="job.resume", summary="resume an interrupted job without repeating completed work",
        module="cratekit.cli.jobs", builder="build_resume", handler_key="job.resume",
        feature_rows=(26,),
        # The builder is declared because long running work needs one; a resume
        # re-invokes the job's own verb, resolved by ``cli.jobs.argv_for``.
        argv_builder="resume_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    Entry(
        name="job.cancel", summary="cancel a job; it reports as cancelled rather than as failed",
        module="cratekit.cli.jobs", builder="build_cancel", handler_key="job.cancel",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    # ── Review ──────────────────────────────────────────────────────────────
    # Under ``cli``, not ``core``, for the job verbs' reason (U11).
    Entry(
        name="review.list", summary="list every item awaiting a person's decision",
        module="cratekit.cli.review", builder="build_list", handler_key="review.list",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.resolve",
        summary="record a verdict on a review item so it is never asked again",
        module="cratekit.cli.review", builder="build_resolve", handler_key="review.resolve",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    # ── Intake ──────────────────────────────────────────────────────────────
    Entry(
        name="intake.set",
        summary="identify a set recording, or a mix URL fetched first, and resolve its tracks",
        module="cratekit.intake.cli", builder="build_set", handler_key="intake.set",
        feature_rows=(1, 2), source_scripts=("dj-pipeline",), module_id="identify",
        argv_builder="set_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        # The account playlist is a remote write behind its own gate, soft
        # skipped without a provider session (U129).
        writes=frozenset({"xml", "files", "remote"}), adjudicates=True, destructive=True,
        # Doctor fails on exactly what ``recognize.recognition_ready`` refuses on.
        # No ``binary.yt-dlp``: only a mix URL needs it, and refuses without it (U104).
        doctor_checks=(
            "library.mounted", "binary.ffmpeg", "binary.ffprobe", "credential.recognition",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.set.account.confirm", options=("apply", "abort"),
                prompt="Save this set as a private playlist on the streaming account?",
                # Explicit (R34): an account write.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="intake.identify",
        summary="identify the tracks in a set recording or a mix URL and stop; acquire nothing",
        module="cratekit.intake.cli", builder="build_identify", handler_key="intake.identify",
        feature_rows=(5,), source_scripts=("dj-setid",), module_id="identify",
        # A version the library may hold is offered for review (U103). Its own
        # tracklist file is no write surface, as for ``intake missing``.
        adjudicates=True, emits=frozenset({"match"}), output_schema="match/1",
        # The library is asked, so doctor must require it.
        doctor_checks=(
            "library.mounted", "binary.ffmpeg", "binary.ffprobe", "credential.recognition",
        ),
    ),
    Entry(
        name="intake.playlist", summary="import a streaming playlist's tracks into the library",
        module="cratekit.intake.cli", builder="build_playlist", handler_key="intake.playlist",
        feature_rows=(3, 35), argv_builder="playlist_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"xml", "files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="intake.missing",
        summary=(
            "write the list acquire download reads from the missing tracks of a "
            "finished intake job, a whole sync pass, or a text list searched on "
            "the provider"
        ),
        module="cratekit.intake.missing_cli", builder="build_missing",
        handler_key="intake.missing", feature_rows=(3, 35),
        # ``--list`` offers candidates and version questions for review (U79).
        adjudicates=True,
        # ``diagnostic/1``: the human renderer shows checks, and a person needs
        # the list's path and the download command (R-400).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # No write surface, so not destructive: two new files, never a replace.
        # The library is asked again, so doctor requires it (R-502).
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="intake.file", summary="ingest one audio file already on disk",
        module="cratekit.intake.file_cli", builder="build_file", handler_key="intake.file",
        feature_rows=(4,), emits=frozenset({"plan"}), output_schema="plan/1",
        #: On a database native intake tree the file becomes a content row and a
        #: batch playlist (R-770); on the bridge, an intake file.
        writes=frozenset({"xml", "files", "db_tree"}), destructive=True,
        #: The database checks hold for the native medium only.
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            # A content row, answered by a separate recorded act (R34, R-770).
            GateSpec(
                name="intake.file.native", options=("apply", "abort"),
                prompt="Add this file to the collection?", explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="intake.shelve",
        summary=(
            "file an imported batch folder into the processed tree, by year and date, "
            "and point its rows at it"
        ),
        module="cratekit.intake.shelve_cli", builder="build_shelve", handler_key="intake.shelve",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: One folder rename and the path column of its rows, never the tree (U154).
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            # A path write on the collection, answered by a recorded act (R34).
            GateSpec(
                name="intake.shelve.native", options=("apply", "abort"),
                prompt="Move these batches into the processed tree and point their rows at it?",
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="tag.folder", summary="tag a folder of audio with genre and album art",
        module="cratekit.tagging.cli", builder="build", handler_key="tag.folder",
        feature_rows=(8,), source_scripts=("dj-tag-folder",), argv_builder="tag_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True, doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="tag.retag",
        summary="replace a genre too coarse to be a final tag with a specific one",
        module="cratekit.tagging.retag_cli", builder="build", handler_key="tag.retag",
        feature_rows=(18,),
        #: No source script: the two cut genre migrations stay cut (``CUT.md``).
        source_scripts=(),
        #: Gated by ``repair``: correcting metadata the library already holds is
        #: an opt in second job, as ``repair.paths`` is for locations.
        module_id="repair", argv_builder="retag_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1",
        #: The file only (R-246): the row follows by ``tag.rows``, which the run
        #: names. No database is opened, so no cloud sync decision.
        writes=frozenset({"files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="tag.retag.confirm", options=("apply", "abort"),
                prompt="Correct the genre on these files?",
                #: Explicit because the verb queues: the recorded act gives the
                #: detached child a run to name (``test_queued_resume_contract``).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="name.apply", summary="rename files and rewrite name fields from the naming template",
        module="cratekit.write.naming_cli", builder="build", handler_key="name.apply",
        feature_rows=(11,), source_scripts=("dj-pad-camelot",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: Files only (U39). The database is only read, to hold back referenced
        #: files (U67), so no cloud sync decision. A partial run answers
        #: ``rename-incomplete`` on the plan surface (R-172).
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
        gates=(
            GateSpec(
                name="name.apply.confirm", options=("apply", "abort"),
                prompt="Apply these renames?", digest_source="plan",
            ),
        ),
        #: The naming half of intake; U21 landed only its per field policy.
    ),
    # ── Acquisition ─────────────────────────────────────────────────────────
    Entry(
        name="acquire.download", summary="acquire matched tracks through the configured adapter",
        module="cratekit.acquire.cli", builder="build", handler_key="acquire.download",
        feature_rows=(6, 7), argv_builder="download_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"files"}),
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        # Landed (U42). No gate, argued in ``cratekit.acquire.cli``'s docstring.
    ),
    Entry(
        name="acquire.audit",
        summary="report existing files that do not match the lossless policy",
        module="cratekit.acquire.cli", builder="build_audit", handler_key="acquire.audit",
        feature_rows=(7,), emits=frozenset({"review_set"}), output_schema="review_set/1",
        # Landed (U42), beside the verb above.
    ),
    Entry(
        name="acquire.fallback",
        summary=(
            "search SoundCloud and YouTube for a list's missing tracks and offer "
            "what they hold for review; downloads nothing"
        ),
        module="cratekit.acquire.fallback_cli", builder="build", handler_key="acquire.fallback",
        feature_rows=(7,),
        # Offers candidates and version questions for review (U80).
        adjudicates=True,
        # ``diagnostic/1``, for ``intake.missing``'s reason.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # NO WRITE SURFACE: it writes review items and nothing else.
        doctor_checks=("library.mounted", "binary.yt-dlp"),
    ),
    Entry(
        name="acquire.fallback-fetch",
        summary=(
            "download the second source candidates accepted in review into staging, "
            "marked lossy and tagged from the list's row"
        ),
        module="cratekit.acquire.fallback_cli", builder="build_fetch",
        handler_key="acquire.fallback-fetch", feature_rows=(7,), argv_builder="fetch_argv",
        long_running=True,
        # Resolving the list raises version questions, as ``acquire.fallback`` (U81).
        adjudicates=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "binary.yt-dlp", "binary.ffmpeg"),
        # No gate: it adds files to staging, each chosen in review.
    ),
    Entry(
        name="acquire.bandcamp",
        summary=(
            "list the Bandcamp account's purchases, newest first, each with what "
            "the library already owns; downloads nothing"
        ),
        module="cratekit.acquire.bandcamp_cli", builder="build", handler_key="acquire.bandcamp",
        feature_rows=(6,),
        # A plan a person reads, so the diagnostic surface (U176).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # No write surface: it only reads.
        doctor_checks=("library.mounted", "keychain.reachable"),
    ),
    Entry(
        name="acquire.bandcamp-fetch",
        summary=(
            "download the Bandcamp purchases the library does not own into a "
            "batch folder under download staging, what it owns held back"
        ),
        module="cratekit.acquire.bandcamp_cli", builder="build_fetch",
        handler_key="acquire.bandcamp-fetch", feature_rows=(6,), argv_builder="fetch_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "keychain.reachable"),
        # No gate: it adds owned purchases to its own staging folder.
    ),
    Entry(
        name="match.run",
        summary="resolve an external list against the library: matched, needs review, or missing",
        module="cratekit.acquire.match_cli", builder="build", handler_key="match.run",
        emits=frozenset({"match"}), output_schema="match/1", adjudicates=True,
    ),
    # ── Routing and audits ──────────────────────────────────────────────────
    Entry(
        name="route.inbox",
        summary="route the intake folder into the declared taxonomy, or an export's with --export",
        module="cratekit.write.routing_cli", builder="build_inbox", handler_key="route.inbox",
        feature_rows=(14,), source_scripts=("dj-sort-inbox",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        # ``--export`` writes a new file beside an export for a bridge tree (U86).
        writes=frozenset({"db_tree", "xml"}), destructive=True,
        taxonomy_terms=("inbox", "genre_energy"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="route.inbox.apply", options=("apply", "abort"),
                prompt="Apply this routing plan to the library?", digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="route.unplaced",
        summary=(
            "find tracks in the collection that no governed tree places, "
            "or place an export's with --export"
        ),
        module="cratekit.write.routing_cli", builder="build_unplaced",
        handler_key="route.unplaced", feature_rows=(14,), source_scripts=("dj-sort-unplaced",),
        emits=frozenset({"plan"}), output_schema="plan/1",
        # The database is only read (R-313), so no database surface, not
        # destructive, no cloud sync decision. ``--export`` writes a new file
        # beside the export (U91), so ``xml``. The pins stay: a read checks them.
        writes=frozenset({"xml"}), taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
    ),
    Entry(
        name="route.resort",
        summary=(
            "add already-routed tracks to their new place after a genre or energy "
            "change, additive, the old membership stays and is named"
        ),
        module="cratekit.write.routing_cli", builder="build_resort", handler_key="route.resort",
        feature_rows=(13,), source_scripts=("dj-resort-energy", "dj-resort-genre"),
        argv_builder="resort_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="route.resort.apply", options=("apply", "abort"),
                prompt="Add these tracks to the routing tree?",
                #: Explicit, for ``tag.retag.confirm``'s reason (U219); the plan
                #: digest lets a rehearsal hold the live run to it.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="audit.coverage", summary="report tracks the governed trees do not cover",
        module="cratekit.cli.reports", builder="build_coverage", handler_key="audit.coverage",
        feature_rows=(14,), source_scripts=("dj-audit-genres",), emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1", taxonomy_terms=("genre_energy",),
    ),
    Entry(
        name="audit.duplicates",
        summary="review-gated duplicate audit; never deletes, remembers intentional alternates",
        module="cratekit.cli.reports", builder="build_duplicates", handler_key="audit.duplicates",
        feature_rows=(15,), source_scripts=("dj-audit-genres",), module_id="duplicates",
        emits=frozenset({"review_set"}), output_schema="review_set/1", adjudicates=True,
    ),
    Entry(
        name="report.library",
        summary="read-only library statistics: genres, tempo spread, tree shape, gaps",
        module="cratekit.cli.reports", builder="build_library", handler_key="report.library",
        source_scripts=("dj-scan-playlists",), module_id="reports",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="report.intake-aging", summary="report intake items by age so stale ones are visible",
        module="cratekit.cli.reports", builder="build_intake_aging",
        handler_key="report.intake-aging", feature_rows=(20,),
        source_scripts=("dj-inbox-rotation",), module_id="reports",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1", taxonomy_terms=("inbox",),
    ),
    # ── Analysis ────────────────────────────────────────────────────────────
    Entry(
        name="analyze.run", summary="analyse audio for key, tempo, and energy",
        module="cratekit.analysis.cli", builder="build", handler_key="analyze.run",
        feature_rows=(9,), module_id="analysis", extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"), argv_builder="analyze_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True, doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="analyze.calibrate",
        summary="calibrate an analysis threshold against the library's own data",
        module="cratekit.analysis.cli", builder="build_calibrate", handler_key="analyze.calibrate",
        feature_rows=(9, 10), source_scripts=("dj-energy-calibrate", "dj-vocal-calibrate"),
        module_id="analysis", extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Library scoped state files need the library, but are not ``writes``,
        # which names library material. ffmpeg decodes an M4A (U263).
        doctor_checks=("library.mounted", "binary.ffmpeg"),
    ),
    Entry(
        name="analyze.validate", summary="score the analysers against labelled ground truth",
        module="cratekit.analysis.cli", builder="build_validate", handler_key="analyze.validate",
        feature_rows=(9,), source_scripts=("dj-analyze-validate",), module_id="analysis",
        extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="analyze.restamp",
        summary="re-stamp analysed values across the back catalogue after a recalibration",
        module="cratekit.analysis.cli", builder="build_restamp", handler_key="analyze.restamp",
        feature_rows=(9,), source_scripts=("energy_restamp", "energy_rerate"),
        module_id="analysis", extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        argv_builder="restamp_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"files", "db_metadata"}), destructive=True,
        # ffmpeg decodes what libsndfile cannot open, an M4A (U263).
        doctor_checks=("library.mounted", "rekordbox.pins", "binary.ffmpeg"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    Entry(
        name="analyze.vocals", summary="score tracks for vocal prominence and stamp the result",
        module="cratekit.vocals.cli", builder="build", handler_key="analyze.vocals",
        feature_rows=(10,), source_scripts=("dj-vox-backfill", "dj-vocal-restamp"),
        module_id="vocals", extras="vocals", extras_modules=("torch", "panns_inference"),
        argv_builder="vocals_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"files"}), destructive=True,
        taxonomy_terms=("with_vox",), doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="metadata.mytags-vocals",
        summary="mirror vocal scores into library tag categories on existing rows",
        module="cratekit.write.metadata_cli", builder="build_mytags_vocals",
        handler_key="metadata.mytags-vocals", feature_rows=(10,),
        source_scripts=("dj-vocal-mytags",), module_id="vocals", emits=frozenset({"plan"}),
        output_schema="plan/1", writes=frozenset({"db_metadata"}), destructive=True,
        taxonomy_terms=("with_vox",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # The ratio the verb refuses on, unmapped rows tag nothing (R-372).
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        #: My Tags, not content columns, so U21's per field policy does not apply.
    ),
    # ── Sync ────────────────────────────────────────────────────────────────
    Entry(
        name="sync.all",
        summary=(
            "queue each enabled source's own increment under one intake run; "
            "label releases are left to crate label sync"
        ),
        module="cratekit.sync.cli", builder="build_all", handler_key="sync.all",
        feature_rows=(25,), source_scripts=("dj-sync",),
        # Not long running: each source queues under its own key (U61, R-203).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            # ``sync.favorites.confirm``'s question, named for this run's verb;
            # ``Gates.hand_off`` carries the answer to the favourites job.
            GateSpec(
                name="sync.all.favorites.confirm", options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="sync.land",
        summary=(
            "take a sync pass to its landing in one verb: the pass, its intake "
            "jobs, the missing list, the download and the tail, stopping at the "
            "landing's gate"
        ),
        module="cratekit.cli.sync_land", builder="build", handler_key="sync.land",
        feature_rows=(25,),
        # Not long running: each job it drives queues under its own verb (U152).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The files its steps write. No database write: the landing stops at
        # its own explicit gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "credential.provider"),
        gates=(
            # Asked only when the vocal model cannot score (U181). Ordinary:
            # it writes nothing the pass would not, so ``-d`` answers it.
            GateSpec(
                name="sync.land.without-vocals", options=("go", "stop"),
                prompt=(
                    "Take the pass although the vocal model cannot score here, so "
                    "every row it lands carries no voxlevel and no vox My Tag?"
                ),
            ),
        ),
    ),
    Entry(
        name="sync.night",
        summary=(
            "run the sync pass unattended, for a schedule overnight: refuses beside "
            "rekordbox, a running job or another pass, holds the night's provider "
            "budget, answers no gate and stops at the landing's gate"
        ),
        module="cratekit.cli.sync_night", builder="build", handler_key="sync.night",
        feature_rows=(25,),
        # Not long running, for ``sync.land``'s reason (U293).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # ``sync land``'s files. No gate: the landing waits at its own gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "credential.provider"),
    ),
    # The night pass as a launchd agent (U295), core and macOS only by refusal.
    # No write surface and not destructive: only the agent's plist and log are
    # touched. No gate: every limit is the night verb's.
    Entry(
        name="schedule.install",
        summary=(
            "install the nightly run of crate sync night as a launchd agent of your "
            "own on macOS, replacing one already installed"
        ),
        module="cratekit.cli.schedule", builder="build_install", handler_key="schedule.install",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="schedule.show",
        summary=(
            "show the nightly run's schedule: installed or not, its time, the crate "
            "it runs, whether launchd has it loaded and the last night's line"
        ),
        module="cratekit.cli.schedule", builder="build_show", handler_key="schedule.show",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="schedule.remove",
        summary="unload the nightly run's launchd agent and delete it; nothing installed is a no op",
        module="cratekit.cli.schedule", builder="build_remove", handler_key="schedule.remove",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="sync.bandcamp",
        summary=(
            "take new Bandcamp purchases to their landing in one verb: the plan, the "
            "fetch tagged by label, the tail and a rehearsal, stopping at the "
            "landing's gate"
        ),
        module="cratekit.cli.sync_bandcamp", builder="build", handler_key="sync.bandcamp",
        feature_rows=(6,),
        # Not long running, for ``sync.land``'s reason (U179).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The files its steps write. No database write: the rehearsal uses a
        # copy, and the landing stops at its own explicit gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "keychain.reachable"),
    ),
    Entry(
        name="sync.labels",
        # Retired (U109), kept so a sweep queued earlier can resume with
        # ``--job``; otherwise it refuses ``verb-retired``.
        summary=(
            "resume a labels sweep queued before crate label sync replaced it; "
            "retired, it queues nothing new"
        ),
        module="cratekit.label.cli", builder="build_sync", handler_key="sync.labels",
        feature_rows=(21,), source_scripts=("dj-label-batch",), module_id="labels",
        argv_builder="sync_labels_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"xml", "files"}), adjudicates=True,
        destructive=True, doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="sync.favorites",
        summary="heart the library's favourites on the streaming service; add-only, never un-hearts",
        module="cratekit.favorites.cli", builder="build_sync", handler_key="sync.favorites",
        feature_rows=(24,), source_scripts=("dj-favorites",), module_id="favorites",
        argv_builder="sync_favorites_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        # The account only (R-424): it reads an export and colours no row; the
        # outbound ledger is not ``files``, as for ``export.playlist``. Kept
        # destructive, an account write nobody can roll back, pending a ruling.
        writes=frozenset({"remote"}), adjudicates=True, destructive=True,
        # No rekordbox check: the database is never opened. ``library.mounted``
        # stays because the outbound ledger is library scoped.
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm", options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True, digest_source="plan",
            ),
        ),
        # Landed (U33, R-130).
    ),
    Entry(
        name="label.registry",
        summary="list, add, and remove favourite labels, and adopt accepted harvested ones",
        module="cratekit.label.cli", builder="build_registry", handler_key="label.registry",
        feature_rows=(21,), source_scripts=("dj-label-batch",), module_id="labels",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="label.import", summary="bring one label's catalogue into the library",
        module="cratekit.label.cli", builder="build_import", handler_key="label.import",
        feature_rows=(22,), source_scripts=("dj-label-library",), module_id="labels",
        argv_builder="label_import_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"xml", "files"}), adjudicates=True,
        destructive=True, doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.approved",
        summary=(
            "write the list acquire download reads from the label releases "
            "accepted in review"
        ),
        module="cratekit.label.approved_cli", builder="build_approved",
        handler_key="label.approved", feature_rows=(22,), module_id="labels",
        # ``diagnostic/1``, for ``intake.missing``'s reason (R-402).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Another version the library holds is offered for review.
        adjudicates=True,
        # No write surface, as for ``intake.missing``.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.held",
        summary=(
            "list the releases the label genre gate is holding back, or return "
            "one to review"
        ),
        module="cratekit.label.held_cli", builder="build_held", handler_key="label.held",
        feature_rows=(21,), module_id="labels",
        # ``diagnostic/1``, since the renderer shows checks (R-798).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # ``return`` files a held release under the sweep's own key.
        adjudicates=True,
        # No write surface: the review database is this product's own record.
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="label.sync",
        summary=(
            "ask, label by label, about the releases new since each label was "
            "last asked, record each answer, then download what was answered for "
            "behind one gate"
        ),
        # A CLI module in front of ``label.sync_cli`` (U190), since only a CLI
        # module may reach the chain ``sync land`` runs.
        module="cratekit.cli.label_sync", builder="build_sync", handler_key="label.sync",
        feature_rows=(21,), module_id="labels",
        # Interactive (U107), reading only through ``cli/prompt.py``;
        # ``--next`` and ``--answer`` keep it scriptable.
        interactive=True,
        # ``diagnostic/1``, for ``label.held``'s reason.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # It files, accepts, supersedes and withholds review items.
        adjudicates=True,
        # The go writes a list and lands downloads in staging, so it is
        # destructive (U108, KTD24).
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="label.sync.confirm", options=("apply", "abort"),
                prompt="Download every release the saved answers took?",
                #: Explicit: starting an hours long unattended download is its
                #: own recorded act, never one more flag.
                explicit=True,
                #: Over the summary, so an answer saved later makes it stale.
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="label.judge",
        summary=(
            "judge the label releases waiting in review by their label's kind, "
            "and hold the ones the genre gate would not have filed"
        ),
        module="cratekit.label.judge_cli", builder="build_judge", handler_key="label.judge",
        feature_rows=(21,), module_id="labels", argv_builder="label_judge_argv",
        # Queued, so a pass over thousands of paced reads resumes (R-815).
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        # It moves releases into a hold and stamps the rest.
        adjudicates=True,
        # No write surface, on ``label.held``'s reasoning.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.artists",
        summary=(
            "give the open label releases whose artist reads as a provider "
            "object address the artist's name"
        ),
        module="cratekit.label.artists_cli", builder="build_artists", handler_key="label.artists",
        feature_rows=(21,), module_id="labels",
        # ``diagnostic/1``, for ``label.held``'s reason (R-840).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Not adjudicating: it only names an open item's artist. No write
        # surface, on ``label.held``'s reasoning. Not queued: a rerun asks only
        # what the last left.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.harvest",
        summary="harvest the labels behind a playlist's tracks; imports nothing",
        module="cratekit.label.cli", builder="build_harvest", handler_key="label.harvest",
        feature_rows=(22,), module_id="labels", emits=frozenset({"review_set"}),
        output_schema="review_set/1", adjudicates=True,
    ),
    # ── A label's folder of year playlists on the account (R-835) ───────────
    Entry(
        name="label.playlists",
        summary=(
            "build a followed label's folder of private year playlists on the "
            "streaming account; adds, never removes, and never adds a track the "
            "library removed through delete review"
        ),
        module="cratekit.label.playlists_cli", builder="build_playlists",
        handler_key="label.playlists", feature_rows=(23,), source_scripts=("dj-label",),
        module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only. Not destructive, as ``export.playlist``: every
        #: write adds. The outbound ledger is not a declared surface.
        writes=frozenset({"remote"}), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.playlists.confirm", options=("apply", "abort"),
                prompt="Build this label's folder of year playlists on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            # A build over ``playlists_cli.FULL_BUILD_CALLS`` provider calls
            # stops here first, since it spends the provider's patience (U191).
            GateSpec(
                name="label.playlists.crawl", options=("crawl", "abort"),
                prompt="Read this label's whole catalogue from the provider?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="label.mark",
        summary="record the year playlists of a label whose batch has landed as taken",
        module="cratekit.label.mark_cli", builder="build_mark", handler_key="label.mark",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface (U242): the account is read, and the mark is held
        #: in ``sync mark``'s record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.mark.confirm", options=("apply", "abort"),
                prompt="Record these year playlists as taken?",
                # Explicit, as ``sync.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── Taking dropped tracks off a label's year playlists (R-836) ──────────
    Entry(
        name="label.prune",
        summary=(
            "take the tracks the genre gate holds, the catalogue no longer "
            "confirms, or the library removed through delete review off the year "
            "playlists this product made for a label"
        ),
        module="cratekit.label.prune_cli", builder="build_prune", handler_key="label.prune",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``remove_tracks`` on a year playlist this product
        #: created. Destructive because it takes something away.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.prune.confirm", options=("apply", "abort"),
                prompt="Take these tracks off this label's year playlists on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── Adoption, deletion, export, standalone utilities ────────────────────
    Entry(
        name="adopt.scan",
        summary="scan an existing library and propose a mapping into the taxonomy",
        # Its own module, apart from ``adopt.apply`` (``ADOPT_APPLY_CLI_UNIT``).
        module="cratekit.adopt.scan_cli", builder="build", handler_key="adopt.scan",
        feature_rows=(34,), module_id="adoption", argv_builder="adopt_scan_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "library.paths_resolved"),
    ),
    Entry(
        name="adopt.apply", summary="apply an approved adoption plan, incrementally and resumably",
        module="cratekit.adopt.apply_cli", builder="build", handler_key="adopt.apply",
        feature_rows=(34,), module_id="adoption", argv_builder="adopt_apply_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="adopt.apply.approve", options=("approve", "abort"),
                prompt="Apply this adoption plan to the library?",
                # Explicit (R34), as the backup acknowledgment is.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # A verb that removes a membership (R-758), not a mode of the additive
    # ``route.resort``, since gates are declared per verb. Decided over
    # ``adopt.apply``'s plan and census (R-780).
    Entry(
        name="adopt.move",
        summary=(
            "move each track from the energy or style sub it holds to the one "
            "its own file names, adding before it removes"
        ),
        module="cratekit.adopt.move_cli", builder="build", handler_key="adopt.move",
        feature_rows=(13,), module_id="adoption", argv_builder="adopt_move_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="adopt.move.approve", options=("approve", "abort"),
                prompt=(
                    "Move these tracks, adding each to its new sub and then "
                    "removing it from the old one?"
                ),
                # Explicit (R34): a removal takes something away.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, two modules ──────────────────────────────────
    # Two modules so ``tombstone.list``, which writes nothing, did not wait on
    # the destructive verb (R36). ``delete.review`` runs inline, not queued
    # (U60, R-149): the person who confirmed the plan watches the files go.
    Entry(
        name="delete.review",
        summary="review tracks removed from the collection and trash the confirmed files",
        module="cratekit.deletion.cli", builder="build_review", handler_key="delete.review",
        feature_rows=(37,), module_id="deletion", emits=frozenset({"review_set"}),
        output_schema="review_set/1", adjudicates=True, destructive=True,
        writes=frozenset({"files"}),
        # ``library.trash`` only here, the one verb that trashes a file (R35);
        # a precondition, since the pass would otherwise refuse after the confirm.
        doctor_checks=(
            "library.mounted", "library.identity", "library.trash", "rekordbox.closed",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="delete.review.confirm", options=("trash", "abort"),
                prompt="Move these files to the system Trash?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tombstone.list",
        summary="list and revoke tombstones so a suppressed version is visible",
        module="cratekit.deletion.tombstone_cli", builder="build_tombstones",
        handler_key="tombstone.list", feature_rows=(37,), module_id="deletion",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="export.playlist", summary="export a library playlist to a streaming service",
        module="cratekit.export.cli", builder="build", handler_key="export.playlist",
        feature_rows=(36,), module_id="export", argv_builder="export_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"remote"}),
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.playlist.confirm", options=("export", "abort"),
                prompt="Write this playlist to the streaming service?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="export.prune",
        summary=(
            "take the tracks no longer in a library playlist off the remote "
            "playlist it was exported to"
        ),
        module="cratekit.export.prune_cli", builder="build_prune", handler_key="export.prune",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``remove_tracks`` on a playlist ``export.playlist``
        #: made. Destructive, for ``label.prune``'s reason.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.prune.confirm", options=("apply", "abort"),
                prompt="Take these tracks off the remote playlist on the streaming service?",
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A set as a playlist on the account, and its archive (R-837) ─────────
    Entry(
        name="export.set",
        summary=(
            "make an identified set or a typed tracklist a private playlist on the "
            "streaming account; adds, never removes"
        ),
        module="cratekit.export.set_cli", builder="build_set", handler_key="export.set",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only, and not destructive, as ``export.playlist``: a
        #: private playlist is created and filled. ``--rename`` (U140) retitles
        #: one this product made to its INSPIRATION name and takes nothing away.
        writes=frozenset({"remote"}),
        # The library: the backfill and the rename read the database (U129).
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm", options=("apply", "abort"),
                prompt="Make this set a private playlist on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="export.set.rename", options=("apply", "abort"),
                prompt=(
                    "Rename this set's playlist on the streaming account to its "
                    "INSPIRATION playlist's name, and record the new name?"
                ),
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="export.archive",
        summary=(
            "file a downloaded set's playlist in Downloaded Sets <year> on the "
            "streaming account, and record it as taken"
        ),
        module="cratekit.export.set_cli", builder="build_archive", handler_key="export.archive",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: the playlist moves into the year's folder (U142),
        #: held as taken in ``sync mark``'s record (U242). Destructive: the
        #: move changes where a person finds it.
        writes=frozenset({"remote"}), destructive=True,
        # The library: the backfill reads the database (U129).
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm", options=("apply", "abort"),
                prompt=(
                    "File this set playlist in Downloaded Sets for its year on the "
                    "streaming account?"
                ),
                # Explicit, as ``label.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="setbuild", summary="build a short set or transition around an anchor track",
        module="cratekit.setbuilder.cli", builder="build", handler_key="setbuild",
        feature_rows=(29,), source_scripts=("dj-set-builder",), module_id="setbuilder",
        emits=frozenset({"plan"}), output_schema="plan/1",
        # Landed (U43). Its index cache is library state, not ``writes``, as
        # for ``analyze.calibrate`` (R-188), so the verb is not destructive.
    ),
    Entry(
        name="master",
        summary="master a recorded set to a consistent loudness without touching the source",
        module="cratekit.master.cli", builder="build", handler_key="master", feature_rows=(30,),
        module_id="mastering",
        # Named so parity sees what the predecessor did (U105, R-193).
        source_scripts=("master_set.sh",), argv_builder="master_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"files"}),
        destructive=True, doctor_checks=("binary.ffmpeg",),
        # Landed (U44). No gate: it writes a new file and archives the original,
        # and ``--overwrite`` is itself the explicit act. So ``master_argv``
        # carries no ``--run``.
    ),
    Entry(
        name="backup.run",
        summary="back the library up, and publish the backup age the write session consults",
        module="cratekit.backup.cli", builder="build", handler_key="backup.run",
        feature_rows=(31,), source_scripts=("backup.sh",), module_id="backup",
        argv_builder="backup_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        # Landed (U45). No gate and no write surface, argued in the shell's
        # docstring: it only adds a mirror and an archive. So no ``--run``.
    ),
    Entry(
        name="skills.install", summary="install the operator skills that ship with the package",
        module="cratekit.skills.cli", builder="build", handler_key="skills.install",
        feature_rows=(33,), module_id="skills", emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # Landed (U28). The module path here is the one the dispatcher imports.
    ),
    # ── The rest of the review surface (U11) ────────────────────────────────
    # Appended rather than beside their siblings, so a concurrent branch
    # conflicts textually instead of auto merging unread.
    Entry(
        name="review.show",
        summary="show one review item whole: its payload, its candidates, its verdict",
        module="cratekit.cli.review", builder="build_show", handler_key="review.show",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.clear", summary="revoke a verdict, so a rejected item is asked about again",
        module="cratekit.cli.review", builder="build_clear", handler_key="review.clear",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.export", summary="write the queue to a versioned file, verdicts included",
        module="cratekit.cli.review", builder="build_export", handler_key="review.export",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.import",
        summary="take an exported queue back in, never overwriting a local verdict",
        module="cratekit.cli.review", builder="build_import", handler_key="review.import",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    # ── Deferred routing (U19) ──────────────────────────────────────────────
    # Appended rather than beside its siblings, for the reason above. Every
    # later block is appended the same way.
    Entry(
        name="route.pending",
        summary="place tracks whose routing was decided before the library held a row for them",
        module="cratekit.write.routing_cli", builder="build_pending", handler_key="route.pending",
        feature_rows=(13,), emits=frozenset({"plan"}), output_schema="plan/1",
        writes=frozenset({"db_tree"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    # ── Landing (U72) ───────────────────────────────────────────────────────
    Entry(
        name="intake.land",
        summary="move a folder of acquired files into the library and write one intake file",
        module="cratekit.intake.land_cli", builder="build_land", handler_key="intake.land",
        feature_rows=(3, 35), emits=frozenset({"plan"}), output_schema="plan/1",
        #: Files and one intake XML, never replacing a target, one lock per batch
        #: name (R-432). On a database native intake tree, content rows and a
        #: batch playlist behind the explicit gate (R-746). A set landing may
        #: archive the account playlist (U129); a landed heart is coloured (U153).
        writes=frozenset({"xml", "files", "db_tree", "db_metadata", "remote"}), destructive=True,
        #: The database checks hold for the native medium only;
        #: ``credential.provider`` is for the account archive (U129).
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.land.confirm", options=("apply", "abort"),
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
            ),
            # Content rows, answered by a separate recorded act (R34, R-746).
            GateSpec(
                name="intake.land.native", options=("apply", "abort"),
                prompt="Move these files into the library and add them to the collection?",
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The deferred mark (U82) ─────────────────────────────────────────────
    Entry(
        name="sync.mark",
        summary="record the account playlists a landed sync pass finished as taken",
        module="cratekit.sync.mark_cli", builder="build_mark", handler_key="sync.mark",
        feature_rows=(3, 25), source_scripts=("dj-sync",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: No write surface (U242): the account is only read, and each playlist
        #: is held as taken in the mark record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.mark.confirm", options=("apply", "abort"),
                prompt="Record these playlists as taken?",
                # Explicit (R34): a taken playlist is never offered again.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The mark, undone (R-838) ────────────────────────────────────────────
    Entry(
        name="sync.unmark",
        summary="let go what a sync pass took, and put back any title its mark wrote",
        module="cratekit.sync.unmark_cli", builder="build_unmark", handler_key="sync.unmark",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``rename_playlist`` back to the recorded title;
        #: a taken entry is let go in the record (U242). Destructive: the
        #: retitle lands on a playlist the product did not make.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.unmark.confirm", options=("apply", "abort"),
                prompt="Put these playlist titles back on the streaming account?",
                # Explicit, as ``sync.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The DOWNLOADED prefix, retired (U242) ───────────────────────────────
    Entry(
        name="sync.taken",
        summary=(
            "record every account playlist already taken, the prefixed and the "
            "marked, in Cratekit's own record"
        ),
        module="cratekit.sync.taken_cli", builder="build_taken", handler_key="sync.taken",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface: only the mark record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.taken.confirm", options=("apply", "abort"),
                prompt="Record these playlists as taken in Cratekit's own record?",
                #: Explicit (R34): a taken playlist is never offered again.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="sync.strip",
        summary=(
            "take the retired DOWNLOADED prefix off every account playlist, "
            "each recorded as taken first"
        ),
        module="cratekit.sync.strip_cli", builder="build_strip", handler_key="sync.strip",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``rename_playlist``, recorded first under
        #: ``prefix-strip`` so ``sync unmark`` can undo it. Destructive, for
        #: ``sync.unmark``'s reason.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.strip.confirm", options=("apply", "abort"),
                prompt=(
                    "Take the DOWNLOADED prefix off these playlists on the streaming "
                    "account?"
                ),
                # Explicit, as ``sync.unmark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The import proof (R-501) ────────────────────────────────────────────
    Entry(
        name="intake.imported",
        summary="prove an intake file imported, retire it, and settle its run",
        module="cratekit.intake.imported_cli", builder="build_imported",
        handler_key="intake.imported", feature_rows=(3, 35), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The intake file is renamed out of the pending scan, so destructive
        #: (KTD24). No gate: nothing is lost and renaming back undoes it.
        writes=frozenset({"xml", "files"}), destructive=True, doctor_checks=("library.mounted",),
    ),
    # ── The export, without rekordbox's menus (R-745) ───────────────────────
    Entry(
        name="export.collection",
        summary="write a collection export from a copy of the database, with rekordbox closed",
        module="cratekit.cli.export_collection", builder="build", handler_key="export.collection",
        # No feature row: the source system never produced an export.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        #: One new XML, never replaced, so not destructive; the database is read
        #: through a copy. Core, since the verbs reading the file are core.
        #: ``library.paths_resolved`` counts the unmapped rows (R-773).
        writes=frozenset({"xml"}),
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
    ),
    # ── The folder suggestion (R-797) ───────────────────────────────────────
    Entry(
        name="report.genres",
        summary=(
            "name every genre holding 50 or more tracks with no top level "
            "folder of its own; creates nothing"
        ),
        module="cratekit.adopt.genres_cli", builder="build", handler_key="report.genres",
        # No feature row. The adoption module, not reports: it reads the
        # database through adoption's collection reader.
        module_id="adoption", emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The database is only read, as for ``route.unplaced``; the pins stay.
        taxonomy_terms=("genre_energy",), doctor_checks=("library.mounted", "rekordbox.pins"),
    ),
    # ── A row's genre from its file (R-816) ─────────────────────────────────
    Entry(
        name="tag.rows",
        summary=(
            "write each library row's genre from its file where the two "
            "disagree, the genre and nothing else; writes no file"
        ),
        module="cratekit.tagging.rows_cli", builder="build", handler_key="tag.rows",
        # No feature row or source script. Gated by ``repair``, for
        # ``tag.retag``'s reason.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The row only, the ``GenreID`` relink (R-246); the file is the authority.
        writes=frozenset({"db_metadata"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # Unmapped rows are left alone, so the ratio decides the plan.
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.rows.confirm", options=("apply", "abort"),
                prompt="Write the genre on these rows from their files?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genres an older mapping wrote, corrected on the file (R-799) ────
    Entry(
        name="tag.remap",
        summary=(
            "rewrite the genre on files a tag job filed by a mapping the "
            "taxonomy has since changed, from what the job recorded; writes no row"
        ),
        module="cratekit.tagging.remap_cli", builder="build", handler_key="tag.remap",
        # No feature row or source script. Gated by ``repair``, as ``tag.rows`` is.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only: the row follows by ``tag.rows``, which the run names,
        #: so no database is opened and no cloud sync decision.
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tag.remap.confirm", options=("apply", "abort"),
                prompt="Rewrite the genre on these files?",
                #: Explicit (R34): a genre is written once and stays.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre for a row with none (U114) ──────────────────────────────────
    Entry(
        name="tag.suggest",
        summary=(
            "suggest a genre for each row with none on the row or the file, "
            "from its artist, its folder and optionally the catalogues; writes file and row"
        ),
        module="cratekit.tagging.suggest_cli", builder="build", handler_key="tag.suggest",
        # No feature row or source script. Core, as ``tag.folder``: adoption
        # files by genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file and the row, so they agree, the row as ``tag.rows`` writes it.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.suggest.confirm", options=("apply", "abort"),
                prompt="Write these suggested genres on the files and their rows?",
                #: Explicit (R34), for ``tag.rows.confirm``'s reason.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The needs genre backlog (U292) ──────────────────────────────────────
    Entry(
        name="tag.backlog",
        summary=(
            "sort every row adoption leaves under needs genre by cause, with "
            "each verb that settles it and one question per genre word no folder "
            "takes; writes nothing"
        ),
        module="cratekit.tagging.backlog_cli", builder="build", handler_key="tag.backlog",
        # No feature row or source script. Core, as ``tag.suggest``, whose plan
        # it reads; the diagnostic surface, as ``report.genres``.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The database is only read; ``--catalogue`` answers are state, not a surface.
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
    ),
    # ── The needs genre campaign (U294) ─────────────────────────────────────
    # A composer, as ``organize`` is: each step is another verb's, under one
    # gate over ``tag.backlog``'s plan.
    Entry(
        name="tag.campaign",
        summary=(
            "apply the needs genre backlog under one gate: tag rows, tag "
            "suggest at the floor, the answered words, then tag rows again; writes "
            "file and row, names the resort"
        ),
        module="cratekit.cli.verbs.tag_campaign", builder="build", handler_key="tag.campaign",
        # No feature row or source script. Gated by ``repair``, as ``tag.rows``,
        # its first and last step, so a composer is no way round a switch.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The union of its steps' surfaces.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.campaign.approve", options=("apply", "abort"),
                prompt=(
                    "Apply the needs genre campaign: the rows from their files, "
                    "the suggestions at the floor, and the answered words, each through "
                    "its own verb? Filing them into their folders asks its own gate."
                ),
                #: Explicit (R34): it stands for its steps' explicit gates.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX rotation (U111) ───────────────────────────────────────────
    Entry(
        name="inbox.rotate",
        summary=(
            "move stale INBOX batches into INBOX / Old and remove expired ones "
            "from Old, never a track"
        ),
        module="cratekit.intake.rotate_cli", builder="build", handler_key="inbox.rotate",
        # The half of the source's rotation the aging report left to a person.
        feature_rows=(20,), source_scripts=("dj-inbox-rotation",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The tree only: intake playlist nodes moved or soft deleted.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("inbox", "inbox_old"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.rotate.approve", options=("approve", "abort"),
                prompt=(
                    "Move these batches into Old and remove these from it, "
                    "keeping every track?"
                ),
                #: Explicit (R34): a removal takes a playlist out of the library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX refill (U134) ─────────────────────────────────────────────
    # Rebuilds an emptied INBOX mirror of an account playlist.
    Entry(
        name="inbox.refill",
        summary=(
            "refill each INBOX playlist a pass mirrored from the author's account, "
            "every track the library owns in the account's order, memberships only"
        ),
        module="cratekit.intake.refill_cli", builder="build", handler_key="inbox.refill",
        # No feature row: the source never mirrored an account playlist.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: memberships of playlists under the intake root.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inbox",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.refill.approve", options=("apply", "abort"),
                prompt="Add these tracks to their INBOX playlists?",
                #: Explicit (R34): a write outside the intake flow.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── INBOX / Analyze, cleared (U166) ─────────────────────────────────────
    # Clears the analysed rows out of the playlist the rekordbox visit selects.
    Entry(
        name="inbox.analyzed",
        summary=(
            "take every row rekordbox has analysed out of INBOX / Analyze, leaving "
            "each row still waiting, memberships only"
        ),
        module="cratekit.intake.analyzed_cli", builder="build", handler_key="inbox.analyzed",
        # No feature row: the source never kept an analysis queue.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: memberships of one intake playlist, soft deleted.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inbox",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.analyzed.approve", options=("apply", "abort"),
                prompt=(
                    "Take these analysed tracks out of INBOX / Analyze, keeping "
                    "every track in the collection?"
                ),
                #: Explicit (R34): a removal from a playlist.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The rekordbox visit, checked (U167) ─────────────────────────────────
    # A read only verdict on the visit; its exit status lets a skill wait on it.
    Entry(
        name="analyze.check",
        summary=(
            "read rekordbox's analysis of the landed rows and say whether the visit "
            "is done, still waiting, or suspect; reads a copy, writes nothing"
        ),
        module="cratekit.analysis.check_cli", builder="build", handler_key="analyze.check",
        # No feature row. Core, not analysis: it runs no detector, and the
        # landing it follows is core.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=("library.mounted", "rekordbox.closed"),
    ),
    # ── The set's permanent playlist (U121) ─────────────────────────────────
    # The backfill for a set landed without ``--set``.
    Entry(
        name="intake.inspiration",
        summary=(
            "write a landed set's permanent playlist under INSPIRATION, every "
            "identified track the library owns in set order, named the source system's way"
        ),
        module="cratekit.intake.inspiration_cli", builder="build",
        handler_key="intake.inspiration",
        # No feature row: the source made these by hand.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: one playlist under INSPIRATION, and its memberships.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inspiration",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="intake.inspiration.approve", options=("apply", "abort"),
                prompt="Write the set's playlist under INSPIRATION with these tracks?",
                #: Explicit (R34): the node stays in the library for good.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genre Favorites (U119) ──────────────────────────────────────────
    # The one path that removes a genre Favorites membership.
    Entry(
        name="favorites.refresh",
        summary=(
            "make every genre folder's Favorites playlist mirror All Favorites, "
            "adding what the folder holds that is a favourite and removing what is not"
        ),
        module="cratekit.favorites.refresh_cli", builder="build", handler_key="favorites.refresh",
        # No feature row: the source kept no Favorites per genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: each genre's Favorites playlist and its memberships.
        writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "favorites"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.refresh.approve", options=("approve", "abort"),
                prompt=(
                    "Make each genre folder's Favorites mirror All Favorites, adding "
                    "these and removing those?"
                ),
                #: Explicit (R34): a removal takes a membership away.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The landed hearts placed (U120) ─────────────────────────────────────
    # The backfill for hearts the landing did not place (U120, U146).
    Entry(
        name="favorites.backfill",
        summary=(
            "put every heart on the account whose track the library owns into All "
            "Favorites and the playlist of the month it was hearted in, adding and never removing"
        ),
        module="cratekit.favorites.backfill_cli", builder="build",
        handler_key="favorites.backfill",
        # No feature row: the landing does what the source's pass did.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: Memberships added, and the colour on members with none (U153).
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.backfill.approve", options=("approve", "abort"),
                prompt="Put these landed hearts into All Favorites and their month " "playlists?",
                #: Explicit (R34): a write to the live library's playlists.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The quarters split into months (U145) ───────────────────────────────
    # One time: splits the quarter playlists into months (U145).
    Entry(
        name="favorites.split",
        summary=(
            "split every quarter playlist beside All Favorites into the playlists of "
            "the months its hearts were hearted in, then retire the emptied quarters"
        ),
        module="cratekit.favorites.split_cli", builder="build", handler_key="favorites.split",
        # No feature row: the source filed by quarter.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: month memberships added, quarters soft deleted.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.split.approve", options=("approve", "abort"),
                prompt=(
                    "Put these quarter playlists' hearts into their month playlists and "
                    "retire the quarters?"
                ),
                #: Explicit (R34): it retires live playlists.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The Favorites folder put in order newest first (U180) ──────────────
    # One time: orders the months already in the folder newest first (U180).
    Entry(
        name="favorites.order",
        summary=(
            "put the folder that holds All Favorites in order: All Favorites first, "
            "the months newest first, then Undated, then everything else as it was"
        ),
        module="cratekit.favorites.order_cli", builder="build", handler_key="favorites.order",
        # No feature row: the source appended each month at the end.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: positions of the playlists in the Favorites folder.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.order.approve", options=("approve", "abort"),
                prompt="Put the Favorites folder in this order, newest month first?",
                #: Explicit (R34): it writes live playlist positions.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The retroactive tidy (U112) ─────────────────────────────────────────
    # A composer, as ``sync.all`` is: every step and write is another verb's.
    Entry(
        name="organize",
        summary=(
            "tidy rekordbox and the account by the product's own rules, one "
            "question per side; lists what you made and never moves it"
        ),
        module="cratekit.organize.cli", builder="build", handler_key="organize",
        # No feature row: each step's row is claimed by its own verb.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        #: The union of its steps' surfaces (U142, U144); no file is written.
        #: Destructive: the rotation, a mark and the root step (U143) remove or
        #: retitle what the product did not make.
        writes=frozenset({"db_tree", "db_metadata", "remote"}), destructive=True,
        taxonomy_terms=("genre_energy", "inbox", "inbox_old", "inspiration"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="organize.rekordbox.approve", options=("approve", "abort"),
                prompt=(
                    "Apply these steps to the rekordbox library? Nothing you "
                    "made is moved and no track is removed."
                ),
                #: Explicit (R34): it stands for its steps' explicit gates.
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="organize.account.apply", options=("apply", "abort"),
                prompt=(
                    "Apply these steps to the streaming account? Only the "
                    "removals listed are made: label debris whose tracks are in its "
                    "label's folder, empty root playlists, and an emptied legacy year "
                    "folder. A working custom playlist stays at the root until a "
                    "sync marks it downloaded, which files it in its year folder."
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A label's dated playlist heard (U123) ───────────────────────────────
    # The half of U117 after the author has heard a go's releases.
    Entry(
        name="label.heard",
        summary=(
            "mark a label's dated playlist heard: its tracks go in the year "
            "playlist and the dated playlist is removed from the account"
        ),
        module="cratekit.label.heard_cli", builder="build_heard", handler_key="label.heard",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only; the Record Labels tree stays on the bridge (R39).
        #: Destructive: it removes a dated playlist this product created.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.heard.confirm", options=("apply", "abort"),
                prompt=(
                    "Mark these releases heard, put the dated playlist's tracks in "
                    "the year, less any removed or pruned, and remove it from the "
                    "streaming account?"
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The taxonomy copy brought up to the shipped schema (U132) ───────────
    # Brings what the shipped template gained into a library's copy.
    Entry(
        name="taxonomy.upgrade",
        summary=(
            "add the classes, buckets and vocabulary tables the shipped taxonomy "
            "template declares and this library's copy lacks, and state the shipped "
            "schema version"
        ),
        module="cratekit.cli.verbs.taxonomy", builder="build", handler_key="taxonomy.upgrade",
        # No feature row: the source's taxonomy was code.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No declared surface: the taxonomy copy and its backup are library
        #: state. Not destructive: it only adds, keeping the old copy.
        writes=frozenset(),
        #: Not ``taxonomy.active``: the verb refuses an unusable copy itself.
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.upgrade.apply", options=("approve", "abort"),
                prompt=(
                    "Add these classes, buckets and vocabulary tables to this "
                    "library's taxonomy copy and state the shipped schema version?"
                ),
                #: Explicit (R34): every verb routes by the copy.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre word outside the taxonomy, answered in one command (U194) ──
    # The two answers for a genre word the taxonomy has no place for.
    Entry(
        name="taxonomy.alias",
        summary=(
            "save a genre word the taxonomy has no place for as a tagging alias "
            "of one of its genre folders, and retag the files carrying it; writes files"
        ),
        module="cratekit.cli.verbs.taxonomy_word", builder="build_alias",
        handler_key="taxonomy.alias",
        # No feature row: the source's aliases were code.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only, beside the taxonomy copy (library state). Rows follow
        #: by ``tag.rows``, so no cloud sync decision. Destructive: a genre is replaced.
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.alias.apply", options=("approve", "abort"),
                prompt=(
                    "Save this word as an alias of the genre in this library's "
                    "taxonomy copy, and retag the files carrying it?"
                ),
                #: Explicit (R34): every verb routes by the copy.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="taxonomy.folder",
        summary=(
            "make a genre word the taxonomy has no place for a genre folder of "
            "its own, with energy bands, in this library's taxonomy copy"
        ),
        module="cratekit.cli.verbs.taxonomy_word", builder="build_folder",
        handler_key="taxonomy.folder",
        # No feature row, for the alias's reason.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No declared surface, as ``taxonomy.upgrade``; ``route.resort`` files
        #: the tracks after. Not destructive: it only adds.
        writes=frozenset(), doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.folder.apply", options=("approve", "abort"),
                prompt="Add this genre folder to this library's taxonomy copy?",
                #: Explicit (R34), as the upgrade's.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A playlist pair, kept one list on both sides (U130) ─────────────────
    Entry(
        name="sync.pair",
        summary=(
            "keep one of your account playlists and one rekordbox playlist the "
            "same list, each side merged against the last sync"
        ),
        module="cratekit.sync.pair_cli", builder="build", handler_key="sync.pair",
        # No feature row: the source kept no list on both sides.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The rekordbox playlist's memberships and the account playlist's
        #: tracks. Destructive: a membership is taken off on both sides.
        writes=frozenset({"db_tree", "remote"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.pair.rekordbox", options=("apply", "skip"),
                prompt=(
                    "Write these additions, removals and order to the rekordbox "
                    "playlists, and queue these tracks for acquisition?"
                ),
                #: Explicit, as every database membership write is (R34).
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="sync.pair.account", options=("apply", "skip"),
                prompt=(
                    "Write these additions, removals and order to the streaming "
                    "account's playlists?"
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The custom playlist twins' backfill (U149) ──────────────────────────
    Entry(
        name="sync.twins",
        summary=(
            "give every downloaded custom playlist on the account its permanent "
            "twin in rekordbox's Custom Playlists <year> folder, paired to stay one list"
        ),
        module="cratekit.sync.twins_cli", builder="build", handler_key="sync.twins",
        # No feature row: the source kept no rekordbox copy.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: year folders, twin playlists and memberships. Not
        #: destructive: it removes nothing.
        writes=frozenset({"db_tree"}),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.twins.approve", options=("approve", "abort"),
                prompt=(
                    "Make these twins and their folders in rekordbox, and pair each "
                    "with its account playlist?"
                ),
                #: Explicit, as every database membership write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A twin's held tracks, let go at the author's choice (U221) ──────────
    Entry(
        name="sync.release",
        summary=(
            "let a custom playlist twin's held tracks be queued at the next "
            "crate sync pair, one twin by its account playlist or every twin"
        ),
        module="cratekit.sync.release_cli", builder="build", handler_key="sync.release",
        # No feature row: the source queued every missing track unasked.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface: only the pairs document, this product's own state.
        writes=frozenset(), doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="sync.release.approve", options=("approve", "abort"),
                prompt=(
                    "Let these twins' held tracks be queued for download at the "
                    "next crate sync pair?"
                ),
                #: Explicit: it decides what is downloaded next (U221).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre for the files every catalogue missed (U172) ─────────────────
    Entry(
        name="tag.guess",
        summary=(
            "give each file in a folder with no genre one guessed from its "
            "artist's other tracks and the playlist it came from; writes files"
        ),
        module="cratekit.tagging.guess_cli", builder="build", handler_key="tag.guess",
        # No feature row or source script. Core, as ``tag.folder``: every pass
        # runs it.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only; the database is only read, so no cloud sync decision.
        #: No gate, as ``tag.folder``: every guess is written (U172).
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
    ),
    # ── Tracks taken off a downloaded playlist (U287) ───────────────────────
    Entry(
        name="sync.removed",
        summary=(
            "list each downloaded track you took off its playlist on the streaming "
            "account, and take the offered ones out of the rekordbox collection behind a gate"
        ),
        module="cratekit.sync.removed_cli", builder="build_removed", handler_key="sync.removed",
        # No feature row. Core, as ``sync.taken``.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The collection (U288): a row and everything naming it, deleted as
        #: Remove from Collection does, playlists renumbered (R-1830). No file:
        #: only ``delete review`` trashes one.
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        doctor_checks=(
            "credential.provider", "library.mounted", "rekordbox.closed", "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="sync.removed.confirm", options=("apply", "abort"),
                prompt="Take these tracks out of the rekordbox collection?",
                #: Explicit (R34): a removal from the collection.
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="sync.removed.retire", options=("retire", "abort"),
                prompt="Retire these playlists the account no longer has?",
                #: Explicit (U320): a retired playlist stops protecting its
                #: tracks from removal. Writes only Cratekit's own record.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
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
