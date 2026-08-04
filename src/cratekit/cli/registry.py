"""The static verb registry: one table, lazily imported, fully introspectable.

KTD7 says modules register in a static table rather than through entry points,
because every module lives in this repository and discovery machinery buys
nothing. Two consequences shape this file.

**Nothing here imports a module.** ``module`` and ``builder`` are strings. The
shell imports a module only when it is enabled AND its subcommand is being
built, and a failed import for a MISSING EXTRA becomes a stub subcommand rather
than a crash. That is what makes ``crate --help`` work on a slim install with
every heavy extra absent, and it is why this module imports nothing beyond the
standard library and the foundation.

**Every entry carries the metadata the conformance suite needs to interrogate
it.** The source system has the ancestor of this idea: a job-kind table with
five capability flags used to decide whether a job may touch the database or the
volume. What it cannot do is answer "does this verb participate in the output
contract", because that question has no field. Widening the entry from five
flags to the whole conformance surface is what lets a new verb fail the build by
OMISSION instead of by review. Coverage proves a verb exists; this proves it
conforms.

An entry whose ``planned_in`` names a unit is DECLARED but not landed. Declaring
it early is deliberate: the Feature Inventory parity check is only meaningful
over the whole surface, and the alternative is discovering at the last unit that
two Feature rows never acquired a verb. ``tests/test_cli_contract.py`` asserts
every planned module is genuinely still absent, so the marker expires the moment
its unit lands rather than surviving as a comment nobody re-reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from cratekit.core import profiles

#: The distribution name, used to render the install command for a missing
#: extra. Held here so the command is GENERATED from the registry rather than
#: written per module, which is what stops a rename desynchronizing it.
DISTRIBUTION = "cratekit"


@dataclass(frozen=True, slots=True)
class GateSpec:
    """A decision point, declared statically rather than asked at a prompt.

    ``name`` is a stable identifier and is never a prompt string. The source
    system binds its scripted answer to prompt ORDER, so inserting a prompt
    anywhere upstream silently makes the answer land on the wrong question, and
    nothing in the type system or the tests would notice. A named gate cannot
    drift that way.

    ``explicit`` marks a gate R34 forbids any blanket answer for. Those are
    satisfiable only from a decision recorded against the run by a separate,
    deliberate act, never inline in the invocation that hit the gate, and never
    from a config key or an environment variable.

    ``digest_source`` names the artifact whose identity the decision was made
    against. When it moves between the offer and the answer, the decision is
    stale rather than valid, which is the property that stops a user approving
    one plan and running a wider one.
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


#: What a verb may declare it writes. ``files`` and ``remote`` are here because
#: KTD24 binds the destructive gates to DESTRUCTION, not to database writes: a
#: verb that trashes audio files writes no database row and is the single most
#: destructive thing the product does.
WRITE_SURFACES: frozenset[str] = frozenset({"db_tree", "db_metadata", "xml", "files", "remote"})

#: The subset of those surfaces that goes through the guarded rekordbox writer.
#: A verb declaring one of these opens the database with write intent, so it can
#: reach the writer's cloud-sync refusals and must declare the decision that
#: answers the unreadable one. Named here so the rule is DERIVED in one place
#: rather than re-listed by every check that needs it: a hand-listed copy is a
#: copy that misses the next verb somebody adds (P3).
DB_WRITE_SURFACES: frozenset[str] = frozenset({"db_tree", "db_metadata"})

#: The decision a verb reaches when the guarded writer cannot READ rekordbox's
#: Cloud Library Sync state. Declared once and attached to every verb in
#: ``DB_WRITE_SURFACES`` rather than re-spelled per entry, because eleven copies
#: of one gate is eleven chances for one of them to drift a word.
#:
#: It is ``explicit`` because R34 forbids a blanket answer for anything in this
#: class: proceeding past a guard that could not rule out a concurrent writer is
#: a per-run act by a named actor, never a flag, a config key, or an environment
#: variable that answers it once for everything.
#:
#: The name is not scoped to a verb, unlike the confirm gates around it. That is
#: deliberate: this is one condition raised by one shared layer, and a decision
#: is recorded against the run's own verb, so a shared name cannot cross-answer
#: another run's gate.
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

    #: The Feature Inventory rows this verb satisfies. The parity check reads
    #: these, so a verb that satisfies a row without saying so leaves the row
    #: looking unimplemented, and a Cut row claimed by a verb fails the build.
    feature_rows: tuple[int, ...] = ()
    #: The source system's console scripts this verb replaces. The other half of
    #: parity: four live scripts have no Feature Inventory row at all, so a check
    #: keyed only on the inventory would pass while four workflows vanished.
    source_scripts: tuple[str, ...] = ()

    #: The feature module that gates this verb, or None when it is core. Names a
    #: member of ``profiles.MODULES``; the profile decides membership (D6) and
    #: this decides which verb that membership switches.
    module_id: str | None = None
    extras: str | None = None
    #: Third-party TOP-LEVEL module names the extras group provides. The stub
    #: fires only when the failed import names one of THESE. Without that gate a
    #: typo in one of our own modules surfaces to the user as "install the
    #: analysis extra", which is both wrong and unfixable by them.
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


#: The plan's Feature Inventory, transcribed. Dispositions drive the parity
#: check: a row dispositioned ``core`` must be reachable without enabling a
#: module, a ``module`` row must be gated by one, and a ``cut`` or ``defer`` row
#: must have no verb at all. Transcribing it here rather than parsing the plan
#: document keeps the check runnable in a clone that has no plan document.
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
    Feature(18, "one-off retag passes", "cut"),
    Feature(19, "streamed-track playlist scan", "cut"),
    Feature(20, "intake aging report", "module"),
    Feature(21, "favourite label registry and sweeps", "module"),
    Feature(22, "label import and label harvest", "module"),
    Feature(23, "label to streaming playlist folders", "defer"),
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

#: Rows whose "Module" disposition is realized as a configured POLICY rather
#: than a module toggle, with the reason. Exactly one, and it is named rather
#: than silently exempted: R21 makes lossy acquisition a policy value with
#: mandatory marking, so there is no configuration in which it is a module that
#: can be on and unmarked. A toggle would re-create exactly that state.
POLICY_ROWS: Mapping[int, str] = MappingProxyType(
    {7: "R21 makes this acquisition.lossless_policy, not a module toggle"}
)

#: Module toggles that exist with no verb behind them, and why that is correct.
#:
#: Feature 32 is deferred: the CLI is the launch product. The toggles and the
#: extras groups stay declared because deferring is not deleting, and a user who
#: installs the full profile should not have a setting appear later that was
#: silently absent. Named here so the "every toggle is used" check can tell a
#: deferred module from one whose verb somebody forgot to gate.
DEFERRED_MODULES: frozenset[str] = frozenset({"web", "desktop"})

#: The unit that lands ``cratekit.write.routing_cli``, named ONCE so all four
#: entries that carry it move together.
#:
#: IT WAS U19 AND IT IS NOW U20, and the reasoning is written down rather than
#: implied, because it is a judgement somebody may want to move again. U19 built
#: the deferred-routing ENGINE and its declared file list never contained a
#: command-line module. It could not have landed one either: conformance 3
#: requires a landed gated verb to exit OK once its gate is answered, and every
#: verb here writes ``db_tree`` and is destructive, which cannot exit OK on a
#: machine with no database. U20 flips trees to database-native, so it is the
#: first unit that must ship a destructive database surface anyway, and these
#: four ride with it.
#:
#: THE MARKER IS NOT THE RECORD. ``scripts/board.py`` reads ``tests/_pending.py``
#: and nothing else, so this constant is a convenience for the reader and the
#: obligation itself is registered there, against U20 (P5).
ROUTING_CLI_UNIT = "U20"


# ---------------------------------------------------------------------------
# The verbs
# ---------------------------------------------------------------------------
#
# Ordered by the surface they belong to rather than alphabetically, because the
# reader's question is almost always "what can this product do about X".

ENTRIES: tuple[Entry, ...] = (
    # ── Setup, profiles, and the run's own state (this unit) ────────────────
    Entry(
        name="profile.show",
        summary="show the active profile and which feature modules it switches on",
        module="cratekit.cli.verbs.profile",
        builder="build",
        handler_key="profile.show",
        feature_rows=(27,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        doctor_checks=(),
    ),
    Entry(
        name="profile.set",
        summary="change the profile preset, and nothing else",
        module="cratekit.cli.verbs.profile",
        builder="build_set",
        handler_key="profile.set",
        feature_rows=(27,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset(),
        gates=(
            GateSpec(
                name="profile.set.apply",
                options=("apply", "abort"),
                prompt="Apply this change to module membership?",
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="run.show",
        summary="show a run's state, its outstanding gates, and any pending human action",
        module="cratekit.cli.verbs.runs",
        builder="build_show",
        handler_key="run.show",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
    ),
    Entry(
        name="run.decide",
        summary="answer a named gate on a run, from any process and any later session",
        module="cratekit.cli.verbs.runs",
        builder="build_decide",
        handler_key="run.decide",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
    ),
    Entry(
        name="setup",
        summary="first-run wizard: library, credentials, taxonomy, profile",
        module="cratekit.cli.setup",
        builder="build",
        handler_key="setup",
        feature_rows=(27,),
        source_scripts=(),
        # The ONE interactive verb, and the only exemption from the no-standard-
        # input assertion. Its interactivity is confined to one module so the
        # static guard can allow exactly one file rather than a directory.
        interactive=True,
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U27",
    ),
    Entry(
        name="doctor",
        summary="check the environment and report each failure with its fix",
        module="cratekit.cli.doctor",
        builder="build",
        handler_key="doctor",
        feature_rows=(28,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U27",
    ),
    Entry(
        name="doctor.repair-paths",
        summary="repair recorded file paths the library can no longer resolve",
        module="cratekit.cli.doctor",
        builder="build_repair_paths",
        handler_key="doctor.repair-paths",
        feature_rows=(17,),
        source_scripts=("dj-path-repair",),
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_metadata"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in="U27",
    ),
    Entry(
        name="status",
        summary="per-source sync state, open runs, and unconverged trees",
        module="cratekit.cli.doctor",
        builder="build_status",
        handler_key="status",
        feature_rows=(28,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U27",
    ),
    Entry(
        name="login",
        summary="record a provider credential in the OS keychain",
        module="cratekit.cli.verbs.login",
        builder="build",
        handler_key="login",
        feature_rows=(27,),
        source_scripts=("dj-tidal-login",),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        doctor_checks=("keychain.reachable",),
        planned_in="U27",
    ),
    # ── The write session and its safety spine ──────────────────────────────
    Entry(
        name="session.ack",
        summary="record the backup acknowledgment this destructive session needs",
        module="cratekit.session.cli",
        builder="build_ack",
        handler_key="session.ack",
        feature_rows=(12,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.ack.backup",
                options=("acknowledged", "abort"),
                prompt="Database and music files are backed up; proceed?",
                # R34: no blanket flag, config key, or environment variable
                # satisfies this. It is asserted per session, by a named actor.
                explicit=True,
            ),
        ),
        planned_in="U8",
    ),
    Entry(
        name="session.release",
        summary="release a library lock whose holder is gone, explicitly",
        module="cratekit.session.cli",
        builder="build_release",
        handler_key="session.release",
        feature_rows=(12,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.release.confirm",
                options=("release", "abort"),
                prompt="Release the lock held by another installation?",
                explicit=True,
            ),
        ),
        planned_in="U8",
    ),
    Entry(
        name="restore.list",
        summary="list write sessions with their timestamp, workflow, and change summary",
        module="cratekit.session.restore_cli",
        builder="build_list",
        handler_key="restore.list",
        feature_rows=(12,),
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        # U27, NOT U32, and the two used to disagree. U32 declared these verbs and
        # could not land the module behind them, so the obligation moved to U27 in
        # tests/_pending.py while this marker stayed on the unit that was closing.
        # A marker naming a closed unit is owned by nobody, which is the failure the
        # register entry itself is written to prevent. tests/test_cli_contract.py
        # now asserts the two agree.
        planned_in="U27",
    ),
    Entry(
        name="restore.run",
        summary="restore a session snapshot, database and coupled state together",
        module="cratekit.session.restore_cli",
        builder="build_run",
        handler_key="restore.run",
        feature_rows=(12,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_tree", "db_metadata", "files"}),
        destructive=True,
        doctor_checks=("library.mounted", "library.identity", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="restore.run.confirm",
                options=("restore", "abort"),
                prompt="Restore this session, discarding everything after it?",
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        # U27 for the reason restore.list above gives: both verbs name one module,
        # so landing either lands both, and the register that owns the obligation
        # says U27.
        planned_in="U27",
    ),
    Entry(
        name="converge",
        summary="report, per governed tree, whether declared membership matches the database",
        module="cratekit.write.converge_cli",
        builder="build",
        handler_key="converge",
        feature_rows=(12,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        doctor_checks=("library.mounted",),
        planned_in="U36",
    ),
    Entry(
        name="rebuild",
        summary="rebuild a governed tree's membership from declared sources and library truth",
        module="cratekit.write.converge_cli",
        builder="build_rebuild",
        handler_key="rebuild",
        feature_rows=(12,),
        argv_builder="rebuild_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        doctor_checks=("library.mounted", "library.identity", "rekordbox.closed"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in="U36",
    ),
    # ── Jobs ────────────────────────────────────────────────────────────────
    # U10 landed these against ``cratekit.cli.jobs`` rather than the
    # ``cratekit.core.jobs_cli`` this table originally named. A verb module is a
    # CLI module: it imports this registry, and KTD23 ranks anything under
    # ``core`` below the CLI layer, so the original path could not have been
    # written without an upward import. The plan's own file list for U10 says
    # ``src/cratekit/cli/jobs.py``, which is what landed.
    Entry(
        name="job.list",
        summary="list queued, running, blocked, and finished jobs",
        module="cratekit.cli.jobs",
        builder="build_list",
        handler_key="job.list",
        feature_rows=(26,),
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    Entry(
        name="job.show",
        summary="show one job, its progress, and the cause behind its state",
        module="cratekit.cli.jobs",
        builder="build_show",
        handler_key="job.show",
        feature_rows=(26,),
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    Entry(
        name="job.resume",
        summary="resume an interrupted job without repeating completed work",
        module="cratekit.cli.jobs",
        builder="build_resume",
        handler_key="job.resume",
        feature_rows=(26,),
        # A resume re-invokes the job's OWN verb, so the argv it needs is that
        # verb's, not this one's. The builder is declared because the registry
        # requires one of anything long-running; it is the identity case, and
        # ``cli.jobs.argv_for`` is what actually resolves the queued handler.
        argv_builder="resume_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    Entry(
        name="job.cancel",
        summary="cancel a job; it reports as cancelled rather than as failed",
        module="cratekit.cli.jobs",
        builder="build_cancel",
        handler_key="job.cancel",
        feature_rows=(26,),
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    # ── Review ──────────────────────────────────────────────────────────────
    #
    # U11 landed these against ``cratekit.cli.review`` rather than the
    # ``cratekit.core.review_cli`` this table originally named, for the same
    # reason U10 moved the job verbs: a verb module imports this registry, and
    # KTD23 ranks anything under ``core`` below the CLI, so the original path
    # could not have been written without an upward import. The plan's own file
    # list for U11 says ``src/cratekit/cli/review.py``, which is what landed.
    Entry(
        name="review.list",
        summary="list every item awaiting a person's decision",
        module="cratekit.cli.review",
        builder="build_list",
        handler_key="review.list",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    Entry(
        name="review.resolve",
        summary="record a verdict on a review item so it is never asked again",
        module="cratekit.cli.review",
        builder="build_resolve",
        handler_key="review.resolve",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    # ── Intake ──────────────────────────────────────────────────────────────
    Entry(
        name="intake.set",
        summary="take a set recording or mix URL through the whole intake pipeline",
        module="cratekit.intake.cli",
        builder="build_set",
        handler_key="intake.set",
        feature_rows=(1, 2),
        source_scripts=("dj-pipeline",),
        module_id="identify",
        argv_builder="set_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"xml", "files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "binary.ffmpeg", "credential.provider"),
        planned_in="U37",
    ),
    Entry(
        name="intake.identify",
        summary="identify the tracks in a set and stop; download nothing",
        module="cratekit.intake.cli",
        builder="build_identify",
        handler_key="intake.identify",
        feature_rows=(5,),
        source_scripts=("dj-setid",),
        module_id="identify",
        emits=frozenset({"match"}),
        output_schema="match/1",
        doctor_checks=("credential.recognition",),
        planned_in="U37",
    ),
    Entry(
        name="intake.playlist",
        summary="import a streaming playlist's tracks into the library",
        module="cratekit.intake.cli",
        builder="build_playlist",
        handler_key="intake.playlist",
        feature_rows=(3, 35),
        argv_builder="playlist_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"xml", "files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        planned_in="U37",
    ),
    Entry(
        name="intake.file",
        summary="ingest one audio file already on disk",
        module="cratekit.intake.cli",
        builder="build_file",
        handler_key="intake.file",
        feature_rows=(4,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"xml", "files"}),
        destructive=True,
        doctor_checks=("library.mounted",),
        planned_in="U37",
    ),
    Entry(
        name="tag.folder",
        summary="tag a folder of audio with genre and album art",
        module="cratekit.tagging.cli",
        builder="build",
        handler_key="tag.folder",
        feature_rows=(8,),
        source_scripts=("dj-tag-folder",),
        argv_builder="tag_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
        planned_in="U37",
    ),
    Entry(
        name="name.apply",
        summary="rename files and rewrite name fields from the naming template",
        module="cratekit.write.naming_cli",
        builder="build",
        handler_key="name.apply",
        feature_rows=(11,),
        source_scripts=("dj-pad-camelot",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_metadata", "files"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        #: U21 landed the per-field policy this verb applies, not the verb. The
        #: shell renames files on disk and rewrites name fields, which is the
        #: naming half of intake, so it travels with U37 beside the verb above it.
        planned_in="U37",
    ),
    # ── Acquisition ─────────────────────────────────────────────────────────
    Entry(
        name="acquire.download",
        summary="acquire matched tracks through the configured adapter",
        module="cratekit.acquire.cli",
        builder="build",
        handler_key="acquire.download",
        feature_rows=(6, 7),
        argv_builder="download_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
    ),
    Entry(
        name="acquire.audit",
        summary="report existing files that do not match the lossless policy",
        module="cratekit.acquire.cli",
        builder="build_audit",
        handler_key="acquire.audit",
        feature_rows=(7,),
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        planned_in="U15",
    ),
    Entry(
        name="match.run",
        summary="resolve an external list against the library: matched, needs review, or missing",
        module="cratekit.acquire.match_cli",
        builder="build",
        handler_key="match.run",
        emits=frozenset({"match"}),
        output_schema="match/1",
        adjudicates=True,
        planned_in="U16",
    ),
    # ── Routing and audits ──────────────────────────────────────────────────
    Entry(
        name="route.inbox",
        summary="route the intake folder into the declared taxonomy",
        module="cratekit.write.routing_cli",
        builder="build_inbox",
        handler_key="route.inbox",
        feature_rows=(14,),
        source_scripts=("dj-sort-inbox",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("inbox", "genre_energy"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="route.inbox.apply",
                options=("apply", "abort"),
                prompt="Apply this routing plan to the library?",
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in=ROUTING_CLI_UNIT,
    ),
    Entry(
        name="route.unplaced",
        summary="find tracks in the collection that no governed tree places",
        module="cratekit.write.routing_cli",
        builder="build_unplaced",
        handler_key="route.unplaced",
        feature_rows=(14,),
        source_scripts=("dj-sort-unplaced",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in=ROUTING_CLI_UNIT,
    ),
    Entry(
        name="route.resort",
        summary="re-place already-routed tracks after a genre or energy change",
        module="cratekit.write.routing_cli",
        builder="build_resort",
        handler_key="route.resort",
        feature_rows=(13,),
        source_scripts=("dj-resort-energy", "dj-resort-genre"),
        argv_builder="resort_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in=ROUTING_CLI_UNIT,
    ),
    Entry(
        name="audit.coverage",
        summary="report tracks the governed trees do not cover",
        module="cratekit.reports.cli",
        builder="build_coverage",
        handler_key="audit.coverage",
        feature_rows=(14,),
        source_scripts=("dj-audit-genres",),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        taxonomy_terms=("genre_energy",),
        planned_in="U34",
    ),
    Entry(
        name="audit.duplicates",
        summary="review-gated duplicate audit; never deletes, remembers intentional alternates",
        module="cratekit.reports.cli",
        builder="build_duplicates",
        handler_key="audit.duplicates",
        feature_rows=(15,),
        source_scripts=("dj-audit-genres",),
        module_id="duplicates",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        adjudicates=True,
        planned_in="U34",
    ),
    Entry(
        name="report.library",
        summary="read-only library statistics: genres, tempo spread, tree shape, gaps",
        module="cratekit.reports.cli",
        builder="build_library",
        handler_key="report.library",
        source_scripts=("dj-scan-playlists",),
        module_id="reports",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U34",
    ),
    Entry(
        name="report.intake-aging",
        summary="report intake items by age so stale ones are visible",
        module="cratekit.reports.cli",
        builder="build_intake_aging",
        handler_key="report.intake-aging",
        feature_rows=(20,),
        source_scripts=("dj-inbox-rotation",),
        module_id="reports",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        taxonomy_terms=("inbox",),
        planned_in="U34",
    ),
    # ── Analysis ────────────────────────────────────────────────────────────
    Entry(
        name="analyze.run",
        summary="analyse audio for key, tempo, and energy",
        module="cratekit.analysis.cli",
        builder="build",
        handler_key="analyze.run",
        feature_rows=(9,),
        module_id="analysis",
        extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"),
        argv_builder="analyze_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
        planned_in="U25",
    ),
    Entry(
        name="analyze.calibrate",
        summary="calibrate an analysis threshold against the library's own data",
        module="cratekit.analysis.cli",
        builder="build_calibrate",
        handler_key="analyze.calibrate",
        feature_rows=(9, 10),
        source_scripts=("dj-energy-calibrate", "dj-vocal-calibrate"),
        module_id="analysis",
        extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U25",
    ),
    Entry(
        name="analyze.validate",
        summary="score the analysers against labelled ground truth",
        module="cratekit.analysis.cli",
        builder="build_validate",
        handler_key="analyze.validate",
        feature_rows=(9,),
        source_scripts=("dj-analyze-validate",),
        module_id="analysis",
        extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U25",
    ),
    Entry(
        name="analyze.restamp",
        summary="re-stamp analysed values across the back catalogue after a recalibration",
        module="cratekit.analysis.cli",
        builder="build_restamp",
        handler_key="analyze.restamp",
        feature_rows=(9,),
        source_scripts=("energy_restamp", "energy_rerate"),
        module_id="analysis",
        extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"),
        argv_builder="restamp_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files", "db_metadata"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in="U25",
    ),
    Entry(
        name="analyze.vocals",
        summary="score tracks for vocal prominence and stamp the result",
        module="cratekit.vocals.cli",
        builder="build",
        handler_key="analyze.vocals",
        feature_rows=(10,),
        source_scripts=("dj-vox-backfill", "dj-vocal-restamp"),
        module_id="vocals",
        extras="vocals",
        extras_modules=("torch", "panns_inference"),
        argv_builder="vocals_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        taxonomy_terms=("with_vox",),
        doctor_checks=("binary.ffmpeg",),
        planned_in="U25",
    ),
    Entry(
        name="metadata.mytags-vocals",
        summary="mirror vocal scores into library tag categories on existing rows",
        module="cratekit.write.metadata_cli",
        builder="build_mytags_vocals",
        handler_key="metadata.mytags-vocals",
        feature_rows=(10,),
        source_scripts=("dj-vocal-mytags",),
        module_id="vocals",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_metadata"}),
        destructive=True,
        taxonomy_terms=("with_vox",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        #: This verb writes My Tags rather than content columns, so U21's per-field
        #: policy does not govern it at all. It is the vocal module's own surface
        #: and belongs with U25, beside the entry above it.
        planned_in="U25",
    ),
    # ── Sync ────────────────────────────────────────────────────────────────
    Entry(
        name="sync.all",
        summary="queue every source's increment; there is no monolithic gated run",
        module="cratekit.sync.cli",
        builder="build_all",
        handler_key="sync.all",
        feature_rows=(25,),
        source_scripts=("dj-sync",),
        argv_builder="sync_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        planned_in="U22",
    ),
    Entry(
        name="sync.labels",
        summary="sync new releases from the favourite-label registry, on its own watermark",
        module="cratekit.label.cli",
        builder="build_sync",
        handler_key="sync.labels",
        feature_rows=(21,),
        source_scripts=("dj-label-batch",),
        module_id="labels",
        argv_builder="sync_labels_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"xml", "files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        planned_in="U26",
    ),
    Entry(
        name="sync.favorites",
        summary="sync hearted tracks both ways; add-only, never un-hearts",
        module="cratekit.favorites.cli",
        builder="build_sync",
        handler_key="sync.favorites",
        feature_rows=(24,),
        source_scripts=("dj-favorites",),
        module_id="favorites",
        argv_builder="sync_favorites_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree", "db_metadata", "xml", "files", "remote"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        planned_in="U22",
    ),
    Entry(
        name="label.registry",
        summary="list, add, and remove favourite labels",
        module="cratekit.label.cli",
        builder="build_registry",
        handler_key="label.registry",
        feature_rows=(21,),
        source_scripts=("dj-label-batch",),
        module_id="labels",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U26",
    ),
    Entry(
        name="label.import",
        summary="bring one label's catalogue into the library",
        module="cratekit.label.cli",
        builder="build_import",
        handler_key="label.import",
        feature_rows=(22,),
        source_scripts=("dj-label-library",),
        module_id="labels",
        argv_builder="label_import_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"xml", "files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        planned_in="U26",
    ),
    Entry(
        name="label.harvest",
        summary="harvest the labels behind a playlist's tracks; imports nothing",
        module="cratekit.label.cli",
        builder="build_harvest",
        handler_key="label.harvest",
        feature_rows=(22,),
        module_id="labels",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        adjudicates=True,
        planned_in="U26",
    ),
    # ── Adoption, deletion, export, standalone utilities ────────────────────
    Entry(
        name="adopt.scan",
        summary="scan an existing library and propose a mapping into the taxonomy",
        module="cratekit.adoption.cli",
        builder="build_scan",
        handler_key="adopt.scan",
        feature_rows=(34,),
        module_id="adoption",
        argv_builder="adopt_scan_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        planned_in="U23",
    ),
    Entry(
        name="adopt.apply",
        summary="apply an approved adoption plan, incrementally and resumably",
        module="cratekit.adoption.cli",
        builder="build_apply",
        handler_key="adopt.apply",
        feature_rows=(34,),
        module_id="adoption",
        argv_builder="adopt_apply_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree", "db_metadata"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="adopt.apply.approve",
                options=("approve", "abort"),
                prompt="Apply this adoption plan to the library?",
                # R34 names this alongside the backup acknowledgment: no blanket
                # affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in="U23",
    ),
    Entry(
        name="delete.review",
        summary="review tracks removed from the collection and trash the confirmed files",
        module="cratekit.deletion.cli",
        builder="build_review",
        handler_key="delete.review",
        feature_rows=(37,),
        module_id="deletion",
        argv_builder="delete_argv",
        long_running=True,
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        adjudicates=True,
        destructive=True,
        writes=frozenset({"files"}),
        doctor_checks=("library.mounted", "library.identity", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="delete.review.confirm",
                options=("trash", "abort"),
                prompt="Move these files to the system Trash?",
                explicit=True,
                digest_source="plan",
            ),
        ),
        planned_in="U24",
    ),
    Entry(
        name="tombstone.list",
        summary="list and revoke tombstones so a suppressed version is visible",
        module="cratekit.deletion.cli",
        builder="build_tombstones",
        handler_key="tombstone.list",
        feature_rows=(37,),
        module_id="deletion",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        planned_in="U24",
    ),
    Entry(
        name="export.playlist",
        summary="export a library playlist to a streaming service",
        module="cratekit.export.cli",
        builder="build",
        handler_key="export.playlist",
        feature_rows=(36,),
        module_id="export",
        argv_builder="export_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"remote"}),
        doctor_checks=("credential.provider",),
        planned_in="U33",
    ),
    Entry(
        name="setbuild",
        summary="build a short set or transition around an anchor track",
        module="cratekit.setbuilder.cli",
        builder="build",
        handler_key="setbuild",
        feature_rows=(29,),
        source_scripts=("dj-set-builder",),
        module_id="setbuilder",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        planned_in="U35",
    ),
    Entry(
        name="master",
        summary="master a recorded set to a consistent loudness without touching the source",
        module="cratekit.master.cli",
        builder="build",
        handler_key="master",
        feature_rows=(30,),
        module_id="mastering",
        argv_builder="master_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
        planned_in="U35",
    ),
    Entry(
        name="backup.run",
        summary="back the library up, and publish the backup age the write session consults",
        module="cratekit.backup.cli",
        builder="build",
        handler_key="backup.run",
        feature_rows=(31,),
        source_scripts=("backup.sh",),
        module_id="backup",
        argv_builder="backup_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
    ),
    Entry(
        name="skills.install",
        summary="install the operator skills that ship with the package",
        module="cratekit.skills.cli",
        builder="build",
        handler_key="skills.install",
        feature_rows=(33,),
        module_id="skills",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U28",
    ),
    # ── The rest of the review surface (U11) ────────────────────────────────
    #
    # Appended here rather than beside their two siblings above so that a branch
    # landing beside this one conflicts TEXTUALLY rather than auto-merging into a
    # tuple whose contents nobody re-read. The four verbs are what the plan's
    # approach names beyond list and resolve: addressing one item, revoking a
    # verdict, and the file for anyone who genuinely wants one.
    Entry(
        name="review.show",
        summary="show one review item whole: its payload, its candidates, its verdict",
        module="cratekit.cli.review",
        builder="build_show",
        handler_key="review.show",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    Entry(
        name="review.clear",
        summary="revoke a verdict, so a rejected item is asked about again",
        module="cratekit.cli.review",
        builder="build_clear",
        handler_key="review.clear",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    Entry(
        name="review.export",
        summary="write the queue to a versioned file, verdicts included",
        module="cratekit.cli.review",
        builder="build_export",
        handler_key="review.export",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    Entry(
        name="review.import",
        summary="take an exported queue back in, never overwriting a local verdict",
        module="cratekit.cli.review",
        builder="build_import",
        handler_key="review.import",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
    ),
    # ── Deferred routing (U19) ──────────────────────────────────────────────
    #
    # APPENDED HERE RATHER THAN BESIDE ITS THREE SIBLINGS, deliberately. Several
    # units land against this table at once, and a middle insertion is the shape
    # a merge resolves silently: two entries appended to different halves of one
    # tuple auto-merge, and the only thing that catches a name collision is the
    # import-time check below plus the conformance suite's length assertion.
    # An append conflicts textually, which is a conflict somebody reads.
    Entry(
        name="route.pending",
        summary="place tracks whose routing was decided before the library held a row for them",
        module="cratekit.write.routing_cli",
        builder="build_pending",
        handler_key="route.pending",
        feature_rows=(13,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        # The same module its three ``route.*`` siblings name, so all four expire
        # on one countdown. The engine behind it landed with U19; the CLI module
        # did not, and U19's declared file list never contained one. See
        # ``ROUTING_CLI_UNIT`` for why the countdown now runs against U20, and
        # ``tests/_pending.py`` for the register entry that actually owns it.
        planned_in=ROUTING_CLI_UNIT,
    ),
)

#: The verb names, as data. ``tests/test_layering.py`` reads this to enforce that
#: no layer below the CLI names a verb, and reads it from HERE rather than from a
#: hand-kept copy so the guard cannot fall behind the registry.
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

    Resolving a handler must not import anything (KTD26): the engine validates a
    queued job's handler before spawning, and validating by import would defeat
    the lazy-import stubs the whole scheme rests on.
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
