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
from cratekit.modules import extras as _extras

#: The distribution name, used to render the install command for a missing
#: extra. Spelled once in ``modules.extras``, which the workers can reach and
#: the CLI cannot be imported by, so a rename cannot desynchronize the two.
DISTRIBUTION = _extras.DISTRIBUTION


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
        # The stub prints ``extras`` as the install command, so it must name a
        # group that exists. Extras are named one to one with modules (KTD7), and
        # tests/test_config.py holds EXTRAS_BACKED equal to pyproject's groups, so
        # these two checks close the chain from a verb to the file pip reads. A
        # module that grows a heavy dependency now has to grow its extras group
        # too, rather than send a user to install one that is not there (R-4).
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
    #: Flipped from Cut on 2026-08-26 (U40), and the plan's own row 18 cell was
    #: amended in the same sitting because the parity check drift-tests the two
    #: trees against each other. The Cut justification was "one-time personal
    #: cleanups", and a 2026-08-24 audit falsified it: tagging is fill-if-empty by
    #: construction, so a mis-tagged arrival routes to the fallback bucket and no
    #: verb can ever look a better answer up. That is a permanent hole in a shipped
    #: workflow rather than one person's migration, and the title says the general
    #: capability rather than the decision this unit reverses.
    Feature(18, "genre correction for a tag already too coarse", "module"),
    Feature(19, "streamed-track playlist scan", "cut"),
    Feature(20, "intake aging report", "module"),
    Feature(21, "favourite label registry and sweeps", "module"),
    Feature(22, "label import and label harvest", "module"),
    #: Flipped from Defer on 2026-10-02 (R-835). The author reversed the
    #: non-replacement: the account's main structure, a folder per label, is
    #: no longer kept once the source system retires.
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
#: THE MARKER IS NOT THE ONLY RECORD, and as of 2026-08-02 it is read. It used
#: to say ``scripts/board.py`` reads ``tests/_pending.py`` "and nothing else",
#: which was true when it was written and is now false: ``planned_units()``
#: parses these markers, so a closed unit still carrying one is a contradiction
#: the board reports. The obligation stays registered in ``tests/_pending.py`` as
#: well, against U20, because that file is what a person reads (P5).
ROUTING_CLI_UNIT = "U20"

#: The unit that lands ``cratekit.cli.rebuild``, named ONCE so anything that
#: carries it moves with it.
#:
#: ONE VERB IS BEHIND THIS WALL AND ONE IS NOT, and the correction is worth
#: recording because U36 first parked both. The two verbs were declared against
#: ONE module, so the countdown, which keys on the module, held the read-only
#: verb behind the destructive one. ``converge`` declares no gates, writes
#: nothing and is destructive of nothing: conformance 3's loop body never
#: executes for it, conformance 5 and 6 filter it out, and 1 and 8 assert over
#: every entry landed or not. Nothing about the wall applied to it, and both of
#: this unit's refusals name it as remediation step one, so parking it parked
#: the remedy. It landed with U36 as ``cratekit.cli.converge``.
#:
#: ``rebuild`` genuinely is behind the wall: it writes ``db_tree``, it is
#: destructive, and conformance 3 requires a landed gated verb to exit OK once
#: its gate is answered, which it cannot do on a machine with no rekordbox
#: database at all. U20 flips trees to database-native, so it is the first unit
#: that must ship a destructive database surface anyway, and this rides with it
#: exactly as the four route verbs already do.
#:
#: THE MARKER IS NOT THE RECORD. ``scripts/board.py`` reads ``tests/_pending.py``
#: and nothing else, so this constant is a convenience for the reader and the
#: obligation itself is registered there, against U20 (P5). Leaving the marker
#: pointing at a unit that has closed would leave the obligation owned by nobody.
REBUILD_CLI_UNIT = "U20"
#: The unit that lands ``cratekit.cli.reports``, named ONCE so all four entries
#: that carry it move together, in the same shape as the constant above.
#:
#: IT WAS U34 AND IT IS NOW U27, and there are two separate reasons, both of
#: which somebody may want to revisit.
#:
#: THE MODULE PATH WAS UNBUILDABLE AS SPELLED. These entries named
#: ``cratekit.reports.cli``, which ``tests/test_layering.py`` ranks ``modules``
#: while this registry ranks ``cli``, so the module that must dispatch through
#: this table could not have imported it without an upward import. That is the
#: same correction U10 and U11 each made on landing, and the comments above the
#: job and review blocks record both. It is corrected here rather than left for
#: whoever picks the verbs up, because a path nobody can build is a fact worth
#: one line now and an afternoon later.
#:
#: THE OWNER MOVED BECAUSE U34 NEVER OWED A CLI. U34's declared file list is
#: ``src/cratekit/modules/reports/`` and its test module, and it landed exactly
#: that: the duplicate audit and the intake aging engines. Left marked U34, all
#: four markers would have named a closed unit the moment #34 merged, and
#: nothing would have noticed, because ``test_cli_contract`` only fires once the
#: module APPEARS and ``scripts/board.py`` reads ``tests/_pending.py`` alone.
#: That is R-13 verbatim, one wave later.
#:
#: U27 IS THE OWNER, on three grounds. It is the only open unit whose declared
#: file list already lands modules in this directory, ``cli/setup.py`` and
#: ``cli/doctor.py``, so ``cli/reports.py`` is the same act in the same place
#: rather than a new kind of work for a unit that does none of it. Three of the
#: four verbs emit ``diagnostic/1``, which is doctor's own output surface, and
#: U27 owns the check registry that surface is rendered against. And U27 is
#: unblocked today, so the obligation can be discharged next rather than parked
#: behind a dependency chain. What U27 inherits with it is real and is stated
#: rather than hidden: ``audit.coverage`` and ``report.library`` have no engine
#: anywhere in the tree, so that unit lands two report engines as well as the
#: shell. ``audit.duplicates`` and ``report.intake-aging`` are thin over engines
#: U34 already landed.
#:
#: THE MARKER IS NOT THE RECORD, exactly as above. The obligation is registered
#: in ``tests/_pending.py`` against U27, which is the file the board audit reads
#: (P5), and this constant is a convenience for the reader.
#:
#: IT HAS LANDED. ``cratekit.cli.reports`` shipped under U27 with the four
#: handlers, the coverage engine and the library-statistics engine the paragraph
#: above says the unit inherits, so none of the four entries carries a
#: ``planned_in`` any more and all nine conformance properties now drive them.
#: The constant stays, exactly as ``ROUTING_CLI_UNIT`` and ``REBUILD_CLI_UNIT``
#: stayed after their own modules landed: the reasoning above is why these verbs
#: are spelled and owned the way they are, and deleting the name would take the
#: record of that decision with it.
REPORTS_CLI_UNIT = "U27"
#: The unit that lands ``cratekit.adopt.apply_cli``, named ONCE for the same
#: reason ``ROUTING_CLI_UNIT`` is, and carrying the judgement rather than only
#: the answer.
#:
#: BOTH ADOPTION VERBS USED TO NAME ``cratekit.adoption.cli``, which is a package
#: that does not exist and no unit's file list has ever declared. Every other
#: authority says ``adopt``: issue #23's brief, ``docs/HANDOFF.md``, the pending
#: register, and the landed ``src/cratekit/adopt/``. The typo was not merely
#: cosmetic. ``test_a_planned_verb_whose_module_has_landed_must_lose_its_marker``
#: probes with ``find_spec`` inside ``except ModuleNotFoundError``, and
#: ``find_spec("cratekit.adoption.cli")`` raises on the MISSING PARENT
#: ``cratekit.adoption``, which the probe caught and read as "not present yet".
#: So the countdown could never fire, in this build or in any future one, and
#: closing #23 would have left two verbs shipping with no conformance coverage
#: and nothing on the board saying so. That is R-13's failure verbatim, and it is
#: already live three times over.
#:
#: THE TWO VERBS THEN SPLIT, because they were never in the same position.
#: ``adopt.scan`` declares no gate, writes nothing, and is not destructive, so
#: conformance 3 is an empty loop for it and it lands here. Only ``adopt.apply``
#: stays behind the wall, and it now names a module of its own so its countdown
#: is about itself.
#:
#: THE MARKER IS NOT THE RECORD. ``scripts/board.py`` reads ``tests/_pending.py``
#: and nothing else, so this constant is a convenience for the reader and the
#: obligation itself is registered there, against the same unit (P5). What the
#: wall actually is, which R-13 currently states wrongly, is written down in that
#: entry rather than here.
#:
#: IT HAS LANDED. ``cratekit.adopt.apply_cli`` shipped under U27 with the shell,
#: the plan-digested approval gate, and the one destructive session the residual
#: titled "Adoption's tag write takes no destructive session and no library lock"
#: asked for, so the entry no longer carries a ``planned_in`` and all nine
#: conformance properties drive it. The constant stays, exactly as
#: ``ROUTING_CLI_UNIT`` and ``REPORTS_CLI_UNIT`` stayed after their own modules
#: landed: the paragraphs above are why these two verbs are spelled and split the
#: way they are, and deleting the name would take the record of that with it.
#:
#: THE WALL WAS ALREADY DOWN when the marker was cleared, and the pending entry
#: still described it as standing. Conformance 3 answers an explicit gate through
#: ``crate run decide`` and resumes the same run for the next gate, and
#: ``write.cloudsync.unreadable`` is named in the suite's unreachable set, so this
#: verb's two gates are one reachable question and one exemption.
ADOPT_APPLY_CLI_UNIT = "U27"
#: Where ``repair.paths`` lives, and the unit that lands it.
#:
#: U102 OVERTOOK THE REASON BELOW AND NOT THE DECISION. The verb no longer
#: declares the cloud-sync gate or a database write, since it never performed
#: one, so the wall described here is gone. The module and the unit stay where
#: they are, because the path repair obligation still lives with U37.
#:
#: IT WAS ``cratekit.cli.doctor`` AND U27, AND IT IS NOW NEITHER. The reasoning is
#: written down rather than implied, in the same shape and for the same reason as
#: ``ROUTING_CLI_UNIT`` above, because it is a judgement somebody may want to move
#: again.
#:
#: The MODULE moved because the countdown that expires a ``planned_in`` marker
#: keys on the module, not on the verb: the moment ``cratekit.cli.doctor`` exists,
#: every entry naming it must lose its marker and satisfy the whole conformance
#: suite. Doctor and status can; this one cannot, and not for a reason effort
#: fixes. It declares the cloud-sync gate, which is ``explicit``, and conformance
#: 3 requires a declared gate to refuse once and then to exit OK when it is
#: answered. R34 makes an explicit gate answerable only by a separate recorded
#: act, never inline in the invocation that discovered it, so the second drive
#: refuses exactly like the first. It also writes ``db_metadata`` against a
#: database that does not exist on a machine with no library, which is the same
#: wall U19 hit and the reason the four routing verbs moved to U20.
#:
#: The UNIT is U37 because that is where path repair already lives:
#: ``tests/_pending.py`` registers, against U37 and ``cratekit.intake``, that a
#: path repair proposal is offered into the review queue rather than applied.
#: Splitting the verb from the obligation that governs it would leave two units
#: owning one feature row.
#:
#: THE MARKER IS NOT THE RECORD. ``scripts/board.py`` reads ``tests/_pending.py``
#: and nothing else, and that file already carries U37's path-repair obligation,
#: so this constant is a convenience for the reader (P5).
REPAIR_CLI_MODULE = "cratekit.intake.repair_cli"
REPAIR_CLI_UNIT = "U37"


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
    ),
    Entry(
        name="repair.paths",
        summary="propose a name for each file rekordbox would reject, and apply the accepted ones",
        module=REPAIR_CLI_MODULE,
        builder="build_repair_paths",
        handler_key="repair.paths",
        feature_rows=(17,),
        source_scripts=("dj-path-repair",),
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: Files only, corrected in U102, the same correction U39 made to
        #: ``name.apply``. The entry claimed ``db_metadata`` and the cloud sync
        #: decision from the design in which this verb re-pointed database rows,
        #: and no handler ever did: it offered proposals and wrote nothing. Since
        #: U102 ``--apply`` renames the files whose proposal a person accepted,
        #: which is a write to files. It READS the database, through the guard
        #: ``name.apply`` built, with ``require_closed`` False, so it never
        #: reaches the guarded writer or the decision that binds to write
        #: intent, and the conformance suite refuses a declared decision a verb
        #: cannot reach, in both directions. Rewriting the locations inside an
        #: export is not built, and whoever builds it declares what it writes.
        writes=frozenset({"files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.paths.confirm",
                options=("apply", "abort"),
                prompt="Apply these accepted renames?",
                digest_source="plan",
            ),
        ),
    ),
    # ── A row's rekordbox defaults (R-923) ──────────────────────────────────
    Entry(
        name="repair.rows",
        summary="give each live library row rekordbox's own defaults where a "
        "column is empty, and its file's inode where the file id is random, so "
        "it loads to a deck; writes no file",
        module="cratekit.write.row_defaults_cli",
        builder="build",
        handler_key="repair.rows",
        # NO FEATURE ROW AND NO SOURCE SCRIPT. The source system never created a
        # content row, so nothing there left one without rekordbox's defaults.
        #
        # GATED BY ``repair``, as ``repair.paths`` and ``tag.rows`` are: a
        # corrective pass over rows the library already holds.
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: THE ROW AND ONLY THE ROW, and of it only the columns
        #: ``rb_writer.CONTENT_ROW_DEFAULTS`` names, each only where NULL, and
        #: ``rb_writer.FILE_ID_COLUMN`` where the binding minted it (U115).
        writes=frozenset({"db_metadata"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="repair.rows.confirm",
                options=("apply", "abort"),
                prompt="Give these rows rekordbox's own defaults?",
                #: EXPLICIT (R34). A write to rows of a live library is answered
                #: by a separate recorded act with an actor.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The ContentLink probe (A32, R-928) ──────────────────────────────────
    Entry(
        name="repair.link",
        summary="write chosen values into the row probe columns, ContentLink "
        "and ISRC, of chosen live library rows, the experiment that asks which "
        "column keeps a landed row off a deck; writes no file",
        module="cratekit.write.row_link_cli",
        builder="build",
        handler_key="repair.link",
        # NO FEATURE ROW AND NO SOURCE SCRIPT. The source system never created a
        # content row, so it never had a column to probe.
        #
        # GATED BY ``repair``, as ``repair.rows`` is: a write over a row the
        # library already holds.
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: THE NAMED ROWS AND ONLY THEM, and of each only the columns of
        #: ``rb_writer.ROW_PROBE_COLUMNS`` its triples name.
        writes=frozenset({"db_metadata"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="repair.link.confirm",
                options=("apply", "abort"),
                prompt="Write these probe values onto these rows?",
                #: EXPLICIT (R34). A write to a row of a live library is
                #: answered by a separate recorded act with an actor.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
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
        # U49 LANDED IT, and it landed BOTH. The countdown keys on the module
        # string rather than on the verb name, so ``cratekit.session.cli``
        # appearing expires this marker and ``session.release``'s together;
        # dropping one would leave the other claiming a module that exists.
        # Until it landed, nothing in the product could mint the acknowledgment
        # ``assert_backup_acknowledged`` demands, so every destructive verb
        # refused and the suite was green because tests minted through the core
        # API. THREE properties arm against each of the two entries, not nine,
        # measured by differencing collected identifiers across the marker drop:
        # conformance 1's emission check, conformance 2's exit-code check and
        # conformance 3's gate walk, six cases across the pair, against the two
        # countdown cases that left. That is the same answer ``restore.list``
        # records below, and the "all nine" claim above is wrong for every entry.
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
        # U49 landed it, in the same commit and for the same reason as
        # ``session.ack`` above: one module string, one file, both markers. The
        # prompt is asked even when no lock is recorded, because conformance 3
        # holds every declared gate to firing, so it asserts a holder the verb
        # may already know is absent. That wording was left alone deliberately
        # and the observation is in the ledger: a unit that lands a declared
        # module and edits the declaration at once cannot say afterwards which
        # half its tests were measuring.
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
        # U27 LANDED IT. The marker was U32's, then U27's, and it is now gone
        # because ``cratekit.session.restore_cli`` exists, which is what starts
        # the conformance properties driving this verb rather than skipping it.
        # THREE of the nine arm against it, not nine, measured by differencing the
        # collected identifiers: the claim "all nine" was made here first and is
        # wrong for every entry, because several properties are AST sweeps over
        # the package and others are parametrized over populations most entries
        # are not in. The register entry the marker had to agree with went in the
        # same commit.
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
        # Landed with its sibling above, and by construction: both verbs name one
        # module, so landing either lands both.
    ),
    Entry(
        name="restore.bare-metal",
        summary="recover the mirror and the database onto a replacement drive",
        module="cratekit.session.restore_cli",
        builder="build_bare_metal",
        handler_key="restore.bare-metal",
        feature_rows=(12,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("rekordbox.closed",),
        # U96. THE CASE ``restore.run`` CANNOT SERVE, which is why it is a verb
        # and not a flag on that one: the library volume is gone, and every gate
        # that verb passes is read from beside the library.
        #
        # ``library.mounted`` AND ``library.identity`` ARE ABSENT ON PURPOSE.
        # Both are checks this verb requires to FAIL, since the engine refuses
        # a recovery while the recorded volume can be read, so declaring them
        # would tell a person their machine is unfit for the one verb that
        # needs it that way.
        #
        # IT DECLARES NO GATE, on ``master``'s precedent and for a harder
        # reason. An explicit gate is a decision recorded against a run, which
        # conformance 3 requires to end in OK on a machine whose library is
        # present, and this verb refuses on exactly that machine.
        # ``--accept-replacement`` is the explicit act, and the engine refuses
        # it from an invocation with no controlling terminal, so the flag
        # cannot be answered by a detached job. What that substitute is worth
        # is written at ``core.restore.bare_metal_session``.
        #
        # ``binary.rclone`` IS ABSENT TOO, on ``restore.run``'s precedent, and
        # the cost is known. This verb is core, and a core verb declaring that
        # check turns a missing rclone from a note into a failure on a slim
        # install that never asked for backups, which doctor's own suite
        # refuses. A recovery without the program still refuses by name, with
        # the install token, before anything is written.
        #
        # ``files`` AND NOT ``db_tree``. The database arrives as a file copied
        # from the remote; no row is written through the guarded writer.
    ),
    Entry(
        name="converge",
        summary="report, per governed tree, whether declared membership matches the database",
        module="cratekit.cli.converge",
        builder="build",
        handler_key="converge",
        feature_rows=(12,),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        doctor_checks=(
            "library.mounted",
            "library.paths_resolved",
        ),
    ),
    Entry(
        name="rebuild",
        summary="rebuild a governed tree's membership from declared sources and library truth",
        module="cratekit.cli.rebuild",
        builder="build",
        handler_key="rebuild",
        feature_rows=(12,),
        argv_builder="rebuild_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "library.identity",
            "rekordbox.closed",
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    # R-235. The two verbs over ``core.tree_registry``, which held the precheck,
    # the record and the revert since U20 with no caller under ``src``.
    #
    # ``writes`` IS EMPTY ON BOTH, on ``profile.set``'s precedent. What they
    # write is this product's own registry file, which is none of the declared
    # surfaces, and the database is only ever READ, through a disposable copy.
    # So neither reaches the guarded writer, neither declares the cloud sync
    # decision, and the conformance suite refuses a declared decision a verb
    # cannot reach.
    #
    # NOT ``destructive``, for the same reason and with its cost stated. The
    # destructive-session gates bind to that flag, so a cutover asks for no
    # backup acknowledgment. What stands in their place is the precheck, which
    # refuses without a verified snapshot and a Fresh Export, and the explicit
    # gate, which is the per-run act by a named actor R34 asks for.
    Entry(
        name="tree.cutover",
        summary="record one tree's cutover from the XML bridge to the database",
        module="cratekit.cli.cutover",
        builder="build",
        handler_key="tree.cutover",
        feature_rows=(12,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        # ``tree.registry`` IS NOT DECLARED, here or on the revert. That check
        # is the REPORT of what these verbs recorded, and conformance 8 holds a
        # declared precondition to refusing on a broken machine, where it says
        # instead that the volume is its own checks' to report. A registry
        # nobody can read still refuses both verbs, through the read itself.
        doctor_checks=("library.mounted", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="tree.cutover.approve",
                options=("approve", "abort"),
                prompt="Record this tree as database native, anchored to this root?",
                # The one way door. A revert is a complete undo only until the
                # tree takes its first native write.
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tree.revert",
        summary="put a cut over tree back on the XML bridge, before its first native write",
        module="cratekit.cli.cutover",
        builder="build_revert",
        handler_key="tree.revert",
        feature_rows=(12,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tree.revert.approve",
                options=("revert", "abort"),
                prompt="Put this tree back on the XML bridge?",
                explicit=True,
                digest_source="plan",
            ),
        ),
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
        summary="identify a set recording, or a mix URL fetched first, and resolve its tracks",
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
        # U129. The account playlist is a remote write behind its own gate; the
        # worker still acquires nothing, and a machine without a provider session
        # still identifies and queues, the playlist step soft skipping.
        writes=frozenset({"xml", "files", "remote"}),
        adjudicates=True,
        destructive=True,
        # THE CHECKS ARE THE GATE'S. ``recognize.recognition_ready`` refuses on
        # the two recognition keys, ffmpeg and ffprobe, so doctor has to fail on
        # exactly those or a machine doctor passes refuses at the verb.
        # ``credential.provider`` is declared for the account playlist (U129);
        # the playlist step soft skips when the account is unreachable so a
        # queued set is never lost. ``binary.yt-dlp`` IS DELIBERATELY ABSENT
        # (U104). Only a mix URL needs the downloader, so declaring it would
        # fail doctor on a machine that identifies every recording it is handed.
        # A URL without it refuses with ``yt-dlp-missing`` and the install hint,
        # before any spend.
        doctor_checks=(
            "library.mounted",
            "binary.ffmpeg",
            "binary.ffprobe",
            "credential.recognition",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.set.account.confirm",
                options=("apply", "abort"),
                prompt="Save this set as a private playlist on the streaming account?",
                # EXPLICIT, as export.set's is (R34): an account write.
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="intake.identify",
        summary="identify the tracks in a set recording or a mix URL and stop; acquire nothing",
        module="cratekit.intake.cli",
        builder="build_identify",
        handler_key="intake.identify",
        feature_rows=(5,),
        source_scripts=("dj-setid",),
        module_id="identify",
        # U103. The identified rows are asked of the library, and a version the
        # library may already hold is offered to the review queue under this
        # verb's own key. It writes a tracklist text file into a folder of its
        # own and declares no write surface, on the precedent ``intake
        # missing`` sets.
        adjudicates=True,
        emits=frozenset({"match"}),
        output_schema="match/1",
        # The library is asked, so a machine with no library mounted is one
        # doctor has to fail, or doctor passes a verb that refuses.
        doctor_checks=(
            "library.mounted",
            "binary.ffmpeg",
            "binary.ffprobe",
            "credential.recognition",
        ),
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
    ),
    Entry(
        name="intake.missing",
        summary=(
            "write the list acquire download reads from the missing tracks of a "
            "finished intake job, a whole sync pass, or a text list searched on "
            "the provider"
        ),
        module="cratekit.intake.missing_cli",
        builder="build_missing",
        handler_key="intake.missing",
        feature_rows=(3, 35),
        # U79. ``--list`` offers provider candidates, and a version question the
        # library raises, into the review queue under this verb's own key.
        adjudicates=True,
        # ``diagnostic/1`` because the default human renderer shows checks and
        # nothing else, and the one thing a person needs from this verb is the
        # list's path and the command that downloads it (R-400).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # NO WRITE SURFACE, and therefore not destructive, on the precedent
        # ``review export`` sets: it adds two new files beside nothing and
        # ``listdoc.write`` refuses rather than replaces a file holding anything
        # else, so there is nothing a destructive session's gates would protect.
        # R-502: every listing asks its missing rows of the library again, and
        # refuses an absent music folder, so doctor has to require it too.
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="intake.file",
        summary="ingest one audio file already on disk",
        module="cratekit.intake.file_cli",
        builder="build_file",
        handler_key="intake.file",
        feature_rows=(4,),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: AND THE COLLECTION, SINCE R-770. On a library whose intake tree is
        #: database native the file becomes one content row and one batch
        #: playlist under the adopted intake root, through the engine the
        #: landing uses and behind the explicit gate below. The intake tree's
        #: mode chooses, through the switch the landing reads. On the bridge
        #: the write is the intake file it always was.
        writes=frozenset({"xml", "files", "db_tree"}),
        destructive=True,
        #: The database checks hold for the native medium only, and doctor
        #: already requires all three, for the reason the landing's entry gives.
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            # R-770. One content row is the same new kind of write the native
            # landing makes, so it is answered the same way: by a separate
            # recorded act, never inline (R34), over a plan naming every
            # column the row sets.
            GateSpec(
                name="intake.file.native",
                options=("apply", "abort"),
                prompt="Add this file to the collection?",
                explicit=True,
                digest_source="plan",
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
        module="cratekit.intake.shelve_cli",
        builder="build_shelve",
        handler_key="intake.shelve",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: ONE FOLDER RENAME AND ONE COLUMN ON THE ROWS IT HOLDS (U154). The
        #: path column is a metadata column rekordbox keys the file by, written
        #: through a field policy registered for this commit alone, so the
        #: surface is the metadata one and the files one, and never the tree.
        writes=frozenset({"files", "db_metadata"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            # A path write on the collection is answered by a separate recorded
            # act, never inline (R34), over a plan naming every batch, every
            # row and the path each one will carry.
            GateSpec(
                name="intake.shelve.native",
                options=("apply", "abort"),
                prompt="Move these batches into the processed tree and point their rows at it?",
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
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
    ),
    Entry(
        name="tag.retag",
        summary="replace a genre too coarse to be a final tag with a specific one",
        module="cratekit.tagging.retag_cli",
        builder="build",
        handler_key="tag.retag",
        feature_rows=(18,),
        #: NO SOURCE SCRIPT. ``dj-split-genre-folders`` and ``dj-genre-research``
        #: stay cut in ``CUT.md`` and this verb does not resurrect either: both
        #: were one-time migrations between two named folders in one library, and
        #: the lookup engine inside the second one folded into tagging already.
        #: Claiming them here would reopen two decisions this unit did not reverse.
        source_scripts=(),
        #: Gated by ``repair`` rather than by a module of its own. A corrective
        #: pass over metadata the library ALREADY holds is the same job
        #: ``repair.paths`` does for a location the library already recorded, and
        #: the slim install is "bring music in and route it", where correcting what
        #: is already there is a second job a person opts into. A module gating one
        #: verb would also put a switch in every user's configuration that means
        #: nothing to anyone who has not met this exact failure.
        module_id="repair",
        argv_builder="retag_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        #: ONE SURFACE, THE FILE, AND THE NARROWING IS THE FIX FOR R-246. This
        #: entry declared ``db_metadata`` as well, after the row's ``GenreID``
        #: relink that ``write.metadata.plan_genre_retag`` performs under the
        #: ``RETAG_GENRE`` policy. This verb does not call it:
        #: ``tagging.retag.plan_library`` has no caller and
        #: ``tagging.retag.apply_library`` is called by ``tag.rows`` alone, which
        #: ``tests/test_tag_workers.py`` pins by walking the tree. So the verb
        #: rewrites the genre through ``core.tags.write_genre`` and stops, and a
        #: person who read the declaration was promised a write that never
        #: happened. The deferral itself is R-185 and is still open; what closes
        #: with this line is the claim about it. The verb now ends by naming
        #: ``tag.rows``, which brings the row back into agreement, see
        #: ``tagging.retag_cli.library_row_warning``.
        #:
        #: NO CLOUD SYNC DECISION EITHER, and that follows rather than being a
        #: second judgement. That gate binds to WRITE INTENT on the guarded
        #: writer, this verb opens no database at all, and the conformance suite
        #: refuses a declared decision a verb cannot reach in both directions.
        #: ``name.apply`` is the same shape already landed, for R-165.
        writes=frozenset({"files"}),
        adjudicates=True,
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="tag.retag.confirm",
                options=("apply", "abort"),
                prompt="Correct the genre on these files?",
                #: EXPLICIT, and the reason is the resume rather than the blast
                #: radius. This verb queues, so the confirmed work runs in a
                #: detached child; R34's separate recorded act is what gives that
                #: child a run to name, and ``tests/test_queued_resume_contract.py``
                #: derives its guard from exactly this combination. An ordinary
                #: gate would put the verb outside that guard while leaving the
                #: same permanent-stall shape in place, since a resume argv carries
                #: no inline answer either.
                explicit=True,
                digest_source="plan",
            ),
        ),
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
        #: Files only, corrected in U39. The handler renames on disk and
        #: rewrites the title tag. Since U67 it READS the database, to hold back
        #: every file the collection references, and that open is a read with
        #: ``require_closed`` False, so it never reaches the guarded writer or
        #: the cannot-read cloud sync DECISION, which binds to write intent
        #: only, and the conformance suite refuses a declared decision a verb
        #: cannot reach, in both directions. The read open DOES still refuse a
        #: library whose cloud sync is ON, and that refusal, like every other
        #: failed read, reaches a person as ``collection-unreadable`` carrying
        #: the inner cause's message and its ``disable-cloud-sync`` remedy. A
        #: collection that READ, consulted because something would be renamed,
        #: and holding a row under a volume no prefix rule names whose recorded
        #: file is absent too, refuses as ``collection-row-unmapped`` (R-500),
        #: since that row could name any file. A run that carried out part of its
        #: plan answers ``rename-incomplete`` on THIS surface rather than the
        #: diagnostic one (R-172), so the plan travels with the failure: two files
        #: rendering to one name are held back in the plan as ``collides``, and
        #: anything the apply pass could not do is named with its reason. It is
        #: the only non-success answer here that is not a refusal. The
        #: rekordbox Name half of the padding convention is
        #: ``write/metadata.plan_title_padding``, which no verb calls (R-165).
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
        ),
        #: U21 landed the per-field policy this verb applies, not the verb. The
        #: shell renames files on disk and rewrites name fields, which is the
        #: naming half of intake, so it travels with U37 beside the verb above it.
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
        # U42 LANDED IT. The marker was U15's, and U15 shipped the ENGINES in
        # ``cratekit.acquire`` without ever shipping a shell, so this entry named
        # a closed unit while rows 6 and 7 sat uncovered in the cutover backlog.
        # The verb declares no gate, and ``cratekit.acquire.cli`` argues why in
        # its module docstring rather than leaving the absence to be read as an
        # oversight the next person quietly corrects.
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
        # U42 LANDED IT, beside the verb above and for the same reason.
    ),
    Entry(
        name="acquire.fallback",
        summary=(
            "search SoundCloud and YouTube for a list's missing tracks and offer "
            "what they hold for review; downloads nothing"
        ),
        module="cratekit.acquire.fallback_cli",
        builder="build",
        handler_key="acquire.fallback",
        feature_rows=(7,),
        # U80. Second source candidates go into the fallback source queue, and
        # a version question the library raises into the match queue, both
        # under this verb's own key.
        adjudicates=True,
        # ``diagnostic/1`` for the reason ``intake.missing`` gives: what a
        # person needs is which rows were offered and where to answer them.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # NO WRITE SURFACE: it writes review items and nothing else.
        doctor_checks=("library.mounted", "binary.yt-dlp"),
    ),
    Entry(
        name="acquire.fallback-fetch",
        summary=(
            "download the second source candidates accepted in review into staging, "
            "marked lossy and tagged from the list's row"
        ),
        module="cratekit.acquire.fallback_cli",
        builder="build_fetch",
        handler_key="acquire.fallback-fetch",
        feature_rows=(7,),
        argv_builder="fetch_argv",
        long_running=True,
        # U81. It resolves the list exactly as ``acquire.fallback`` does, and
        # that resolution raises a version question into the match queue.
        adjudicates=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("library.mounted", "binary.yt-dlp", "binary.ffmpeg"),
        # No gate, for the reason ``acquire.download`` declares none: it adds
        # files into download staging, and every upload was chosen in review.
    ),
    Entry(
        name="acquire.bandcamp",
        summary=(
            "list the Bandcamp account's purchases, newest first, each with what "
            "the library already owns; downloads nothing"
        ),
        module="cratekit.acquire.bandcamp_cli",
        builder="build",
        handler_key="acquire.bandcamp",
        feature_rows=(6,),
        # U176. A plan a person reads, so the diagnostic surface: one check per
        # disposition and every purchase in the summary.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # NO WRITE SURFACE: it reads the account, the library and the record.
        doctor_checks=("library.mounted", "keychain.reachable"),
    ),
    Entry(
        name="acquire.bandcamp-fetch",
        summary=(
            "download the Bandcamp purchases the library does not own into a "
            "batch folder under download staging, what it owns held back"
        ),
        module="cratekit.acquire.bandcamp_cli",
        builder="build_fetch",
        handler_key="acquire.bandcamp-fetch",
        feature_rows=(6,),
        argv_builder="fetch_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("library.mounted", "keychain.reachable"),
        # No gate, for the reason ``acquire.download`` declares none: it adds
        # files into its own batch folder under download staging and replaces
        # nothing, and the purchases are the account's own.
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
    ),
    # ── Routing and audits ──────────────────────────────────────────────────
    Entry(
        name="route.inbox",
        summary="route the intake folder into the declared taxonomy, or an export's with --export",
        module="cratekit.write.routing_cli",
        builder="build_inbox",
        handler_key="route.inbox",
        feature_rows=(14,),
        source_scripts=("dj-sort-inbox",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        # U86. ``--export`` writes a new file beside a fresh export, for a tree
        # that has not cut over, so the verb writes the bridge as well.
        writes=frozenset({"db_tree", "xml"}),
        destructive=True,
        taxonomy_terms=("inbox", "genre_energy"),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="route.inbox.apply",
                options=("apply", "abort"),
                prompt="Apply this routing plan to the library?",
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="route.unplaced",
        summary="find tracks in the collection that no governed tree places, "
        "or place an export's with --export",
        module="cratekit.write.routing_cli",
        builder="build_unplaced",
        handler_key="route.unplaced",
        feature_rows=(14,),
        source_scripts=("dj-sort-unplaced",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        # THE DATABASE IS ONLY READ (R-313). Without ``--export`` the handler
        # opens it without write intent, takes no session and writes nothing,
        # so no database surface is declared, the verb is not destructive and
        # it names no cloud-sync decision. Declaring otherwise told a person to
        # close rekordbox before a read. U91 gave the source's
        # ``dj-sort-unplaced`` act back on the export medium: ``--export``
        # writes a NEW file beside the export, never the export and never the
        # database, so ``xml`` is the one surface. The volume stays: the tree
        # registry the report walks from is a state file on the library root,
        # and the sweep reads the files the export names. The pins stay too,
        # because the writer checks the binding pin on every open, a read
        # included, so a drifted binding refuses the report as well.
        writes=frozenset({"xml"}),
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
    ),
    Entry(
        name="route.resort",
        summary="add already-routed tracks to their new place after a genre or energy "
        "change, additive, the old membership stays and is named",
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
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    Entry(
        name="audit.coverage",
        summary="report tracks the governed trees do not cover",
        module="cratekit.cli.reports",
        builder="build_coverage",
        handler_key="audit.coverage",
        feature_rows=(14,),
        source_scripts=("dj-audit-genres",),
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        taxonomy_terms=("genre_energy",),
    ),
    Entry(
        name="audit.duplicates",
        summary="review-gated duplicate audit; never deletes, remembers intentional alternates",
        module="cratekit.cli.reports",
        builder="build_duplicates",
        handler_key="audit.duplicates",
        feature_rows=(15,),
        source_scripts=("dj-audit-genres",),
        module_id="duplicates",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        adjudicates=True,
    ),
    Entry(
        name="report.library",
        summary="read-only library statistics: genres, tempo spread, tree shape, gaps",
        module="cratekit.cli.reports",
        builder="build_library",
        handler_key="report.library",
        source_scripts=("dj-scan-playlists",),
        module_id="reports",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
    ),
    Entry(
        name="report.intake-aging",
        summary="report intake items by age so stale ones are visible",
        module="cratekit.cli.reports",
        builder="build_intake_aging",
        handler_key="report.intake-aging",
        feature_rows=(20,),
        source_scripts=("dj-inbox-rotation",),
        module_id="reports",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        taxonomy_terms=("inbox",),
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
        # It writes two library scoped state files, so the library has to be
        # there. Not in ``writes``, whose vocabulary is the library's own
        # material, files, database and XML, and a calibration is none of those.
        doctor_checks=("library.mounted",),
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
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # R-372: a plan over a collection most of whose rows record a path
            # no prefix rule maps would tag nothing and report ok. The check
            # reads the same ratio the verb refuses on.
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        #: This verb writes My Tags rather than content columns, so U21's per-field
        #: policy does not govern it at all. It is the vocal module's own surface
        #: and belongs with U25, beside the entry above it.
    ),
    # ── Sync ────────────────────────────────────────────────────────────────
    Entry(
        name="sync.all",
        summary=(
            "queue each enabled source's own increment under one intake run; "
            "label releases are left to crate label sync"
        ),
        module="cratekit.sync.cli",
        builder="build_all",
        handler_key="sync.all",
        feature_rows=(25,),
        source_scripts=("dj-sync",),
        # NOT long_running, AND NO argv_builder, since U61. This verb queues
        # nothing under its own key: it composes each source's own queueing
        # path under that source's own handler key, so a job under ``sync.all``
        # cannot exist and there is nothing for a builder to resume (R-203).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        gates=(
            # THE SAME QUESTION ``sync.favorites.confirm`` ASKS, over the same
            # digest, asked once for the whole pass. A separate name because a
            # decision is recorded against the run's own verb, and this run is
            # ``sync.all``'s. ``Gates.hand_off`` carries the recorded answer to a
            # run the favourites job's resume can load.
            GateSpec(
                name="sync.all.favorites.confirm",
                options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True,
                digest_source="plan",
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
        module="cratekit.cli.sync_land",
        builder="build",
        handler_key="sync.land",
        feature_rows=(25,),
        # NOT long_running, AND NO argv_builder (U152). Like ``sync all`` it
        # queues nothing under its own key: every job it drives is queued by
        # its own verb under that verb's key, and is driven here through that
        # verb's own ``--job`` command line, in the foreground.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # THE STEPS' FILES, written by the verbs it runs: the download, the
        # tags, the restamp and the renames. No database write: the landing it
        # plans stops at its explicit gate on its own run, so the collection is
        # written only by that verb, after a separate recorded answer.
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "credential.provider"),
    ),
    Entry(
        name="sync.labels",
        # RETIRED BY REDUCTION (U109). ``label.sync`` takes label releases now,
        # and ``sync.all`` no longer composes this source. The entry stays, its
        # handler key, worker and argv builder with it, because a sweep queued
        # before U109 is resumed through ``sync labels --job`` and would
        # otherwise have no way to run. Without ``--job`` it refuses
        # ``verb-retired`` and names the guided verb.
        summary=(
            "resume a labels sweep queued before crate label sync replaced it; "
            "retired, it queues nothing new"
        ),
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
    ),
    Entry(
        name="sync.favorites",
        summary="heart the library's favourites on the streaming service; add-only, never un-hearts",
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
        # THE REMOTE ACCOUNT IS THE ONLY SURFACE THIS VERB REACHES (R-424).
        # It declared four more. The handler reads a collection export and
        # calls ``hearts.heart_back`` with ``colors=None``, so no library row
        # is coloured, no Favorite tag is written and no playlist gains a
        # member: the three acts ``db_tree`` and ``db_metadata`` stood for.
        # There is no document written beside the export either, so no ``xml``.
        # The outbound write ledger is the one file a pass does touch and it is
        # not ``files``: ``export.playlist`` writes that same ledger through the
        # same shell and has always declared ``remote`` alone, so counting it
        # here would make one file two different surfaces. Narrowing it drops
        # the cloud-sync decision with it, since that gate belongs to
        # ``DB_WRITE_SURFACES`` and a verb declaring a question its work cannot
        # raise is the over-claim wearing a prompt. ``destructive`` STAYS: the
        # verb writes an account a person cannot roll back, and whether an
        # add-only remote write is destruction under KTD24 is a person's call.
        # It is recorded in `docs/residual-findings.md` as its own finding,
        # under a heading naming this verb and this flag, rather than decided
        # here: narrowing a claim in the cautious direction is a different act
        # from removing one that was false, and only the second was this
        # closure's to take.
        writes=frozenset({"remote"}),
        adjudicates=True,
        destructive=True,
        # NEITHER REKORDBOX CHECK SURVIVES THE NARROWING. The verb never opens
        # the database: it reads an export through this project's own reader,
        # so nothing binds it to a pyrekordbox version and nothing breaks if
        # rekordbox is running. ``library.mounted`` stays because the outbound
        # write ledger is library scoped, and losing it is how a second pass
        # hearts what the first one already hearted.
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
                options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True,
                digest_source="plan",
            ),
        ),
        # Landed by U33. The marker said U22; R-130 remounts this verb onto
        # the unit that creates cratekit.favorites.cli. U33 is that unit.
    ),
    Entry(
        name="label.registry",
        summary="list, add, and remove favourite labels, and adopt accepted harvested ones",
        module="cratekit.label.cli",
        builder="build_registry",
        handler_key="label.registry",
        feature_rows=(21,),
        source_scripts=("dj-label-batch",),
        module_id="labels",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
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
    ),
    Entry(
        name="label.approved",
        summary=(
            "write the list acquire download reads from the label releases "
            "accepted in review"
        ),
        module="cratekit.label.approved_cli",
        builder="build_approved",
        handler_key="label.approved",
        feature_rows=(22,),
        module_id="labels",
        # ``diagnostic/1`` for the reason ``intake.missing`` gives: the default
        # human renderer shows checks and nothing else, and what a person needs
        # from this verb is the list's path and the command that downloads it
        # (R-402).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # A track the library holds in another version is OFFERED into the match
        # queue under this verb's own key, the way an intake offers it.
        adjudicates=True,
        # NO WRITE SURFACE, and therefore not destructive, on ``intake.missing``'s
        # precedent: two new files, and ``listdoc.write`` refuses rather than
        # replaces a file holding anything else.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.held",
        summary=(
            "list the releases the label genre gate is holding back, or return "
            "one to review"
        ),
        module="cratekit.label.held_cli",
        builder="build_held",
        handler_key="label.held",
        feature_rows=(21,),
        module_id="labels",
        # ``diagnostic/1``, for the reason ``label.approved`` gives: what a
        # person needs is each held release, its reason, and the command that
        # returns it, and the default renderer shows checks (R-798).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # ``return`` FILES a held release into the label-release queue, under
        # the sweep's own key, so the item is the one the sweep would have filed.
        adjudicates=True,
        # NO WRITE SURFACE, and not destructive: the review database is this
        # product's own record, and a return adds one open item and changes one
        # hold's state. Nothing is downloaded and no tombstone is written.
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="label.sync",
        summary=(
            "ask, label by label, about the releases new since each label was "
            "last asked, record each answer, then download what was answered for "
            "behind one gate"
        ),
        # THE CLI MODULE IN FRONT OF THE VERB'S OWN (U190). Its builder is
        # ``label.sync_cli``'s and its handler runs that one unchanged, then the
        # tail and the landing a go names, through the chain ``sync land`` runs,
        # which only a CLI ranked module may reach.
        module="cratekit.cli.label_sync",
        builder="build_sync",
        handler_key="label.sync",
        feature_rows=(21,),
        module_id="labels",
        # THE SECOND INTERACTIVE VERB (U107). The brainstorm chose a question
        # asked in the terminal over an answer file, and every read of
        # standard input still happens in the one allowlisted module,
        # ``cli/prompt.py``. ``--next`` and ``--answer`` are the same verb
        # driven with no terminal, which is what keeps it scriptable.
        interactive=True,
        # ``diagnostic/1``, for the reason ``label.held`` gives: what a person
        # needs is each label's question, each answer recorded, and the
        # command that asks the next, and the default renderer shows checks.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # IT FILES AND DECIDES. A taken release is filed into the label-release
        # queue under the sweep's own key and recorded accepted, an open item
        # a label's answer did not take is superseded, and an open item the
        # gate would not have filed is withheld as ``label judge`` withholds.
        adjudicates=True,
        # THE GO WRITES FILES (U108): a list and its manifest, and the download
        # job it queues and drives in this process lands tracks in staging. So
        # the verb is destructive by KTD24's definition, though the asking half
        # still writes only this product's own review database and record.
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="label.sync.confirm",
                options=("apply", "abort"),
                prompt="Download every release the saved answers took?",
                #: EXPLICIT, the brief's word and the author's standing rule: a
                #: label release is downloaded only after it was answered for,
                #: and the start of a download that runs unattended for hours is
                #: asserted on its own and recorded with who made it, never
                #: answered by one more flag on the walk that reached it.
                explicit=True,
                #: Over the digest of the summary, so an answer saved after the
                #: decision is a stale decision rather than a download nobody
                #: was shown.
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
        module="cratekit.label.judge_cli",
        builder="build_judge",
        handler_key="label.judge",
        feature_rows=(21,),
        module_id="labels",
        argv_builder="label_judge_argv",
        # ONE ITEM PER PENDING RELEASE, each two provider reads and a few paced
        # catalogue requests, over a queue that held 2,755 when this landed
        # (R-815). Queued, so the pass picks up where it stopped.
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        # IT MOVES A RELEASE OUT OF THE LABEL-RELEASE QUEUE and into a hold, and
        # stamps the ones that stay, under the key the sweep filed them with.
        adjudicates=True,
        # NO WRITE SURFACE, and not destructive, on ``label.held``'s reasoning:
        # the review database is this product's own record. A hold is not a
        # rejection, no tombstone is written, and nothing is downloaded.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.artists",
        summary=(
            "give the open label releases whose artist reads as a provider "
            "object address the artist's name"
        ),
        module="cratekit.label.artists_cli",
        builder="build_artists",
        handler_key="label.artists",
        feature_rows=(21,),
        module_id="labels",
        # ``diagnostic/1``, for the reason ``label.held`` gives: what a person
        # needs is each release and what became of it, and the default
        # renderer shows checks (R-840).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # NOT ADJUDICATING. It files nothing and decides nothing: an open item
        # keeps its place and gains its artist's name, and a decided one is
        # never rewritten. NO WRITE SURFACE and not destructive, on
        # ``label.held``'s reasoning: the review database is this product's
        # own record. NOT QUEUED: one provider read per release that reads an
        # address, 29 when this landed, and a second run asks only about what
        # the first left, so there is nothing for a job to resume.
        doctor_checks=("library.mounted", "credential.provider"),
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
    ),
    # ── A label's folder of year playlists on the account (R-835) ───────────
    Entry(
        name="label.playlists",
        summary=(
            "build a followed label's folder of private year playlists on the "
            "streaming account; adds, never removes"
        ),
        module="cratekit.label.playlists_cli",
        builder="build_playlists",
        handler_key="label.playlists",
        feature_rows=(23,),
        source_scripts=("dj-label",),
        module_id="labels",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account. A folder and its year playlists are
        #: created, tracks are added and a playlist is put in the folder;
        #: nothing is removed, retitled or deleted. What was written is
        #: recorded in this product's own outbound ledger, which is not a
        #: declared surface. NOT destructive, on ``export.playlist``'s
        #: precedent: every write adds to the account.
        writes=frozenset({"remote"}),
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.playlists.confirm",
                options=("apply", "abort"),
                prompt="Build this label's folder of year playlists on the streaming account?",
                # EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
            # U191. A full build whose listing estimates more provider calls
            # than ``playlists_cli.FULL_BUILD_CALLS`` stops here before any
            # release is read. It writes nothing; it spends the provider's
            # patience, which a breaker trip on a label of thousands of
            # releases showed is worth a deliberate act of its own.
            GateSpec(
                name="label.playlists.crawl",
                options=("crawl", "abort"),
                prompt="Read this label's whole catalogue from the provider?",
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="label.mark",
        summary="prefix the year playlists of a label whose batch has landed",
        module="cratekit.label.mark_cli",
        builder="build_mark",
        handler_key="label.mark",
        feature_rows=(23,),
        module_id="labels",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account, and the one write is ``rename_playlist``
        #: on a year playlist the outbound ledger records for the label. Each
        #: rename is recorded in ``sync mark``'s record so ``sync unmark``
        #: puts it back. ``destructive`` for ``sync.mark``'s reason: a year
        #: playlist adopted by its name was made by a person, and a retitle
        #: lands on it.
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.mark.confirm",
                options=("apply", "abort"),
                prompt="Rename these year playlists on the streaming account?",
                # EXPLICIT, as sync.mark's is, for the same reason (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── Taking dropped tracks off a label's year playlists (R-836) ──────────
    Entry(
        name="label.prune",
        summary=(
            "take the tracks the genre gate holds or the catalogue no longer "
            "confirms off the year playlists this product made for a label"
        ),
        module="cratekit.label.prune_cli",
        builder="build_prune",
        handler_key="label.prune",
        feature_rows=(23,),
        module_id="labels",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account, and the one write is ``remove_tracks`` on
        #: a year playlist the outbound ledger records this product CREATED.
        #: What was taken off is recorded in the outbound ledger, which is not
        #: a declared surface. ``destructive`` because it is the first path
        #: that takes anything away from the account.
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.prune.confirm",
                options=("apply", "abort"),
                prompt="Take these tracks off this label's year playlists on the streaming account?",
                # EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── Adoption, deletion, export, standalone utilities ────────────────────
    Entry(
        name="adopt.scan",
        summary="scan an existing library and propose a mapping into the taxonomy",
        # LANDED. It shared a module string with its destructive sibling and was
        # held behind that sibling's wall for no reason of its own; see
        # ``ADOPT_APPLY_CLI_UNIT`` for the whole judgement.
        module="cratekit.adopt.scan_cli",
        builder="build",
        handler_key="adopt.scan",
        feature_rows=(34,),
        module_id="adoption",
        argv_builder="adopt_scan_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "library.paths_resolved",
        ),
    ),
    Entry(
        name="adopt.apply",
        summary="apply an approved adoption plan, incrementally and resumably",
        module="cratekit.adopt.apply_cli",
        builder="build",
        handler_key="adopt.apply",
        feature_rows=(34,),
        module_id="adoption",
        argv_builder="adopt_apply_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree", "db_metadata"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
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
    ),
    # R-758. THE FIRST VERB THAT REMOVES A MEMBERSHIP, and a verb of its own
    # rather than a mode of ``route.resort``. That verb is additive and says
    # so in its summary, and a gate is declared per verb: an approval asked in
    # a removing mode only is a gate this table cannot state and conformance 3
    # cannot hold to firing. It sits in this group because what it moves is
    # decided over ``adopt.apply``'s plan, read with the census that verb
    # reads, and since R-780 over every band bucket the tree doubles a track in.
    Entry(
        name="adopt.move",
        summary="move each track from the energy or style sub it holds to the one "
        "its own file names, adding before it removes",
        module="cratekit.adopt.move_cli",
        builder="build",
        handler_key="adopt.move",
        feature_rows=(13,),
        module_id="adoption",
        argv_builder="adopt_move_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="adopt.move.approve",
                options=("approve", "abort"),
                prompt="Move these tracks, adding each to its new sub and then "
                "removing it from the old one?",
                # A removal is the one write this product makes that takes
                # something away, so no blanket affirmative satisfies it (R34).
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, TWO MODULES, and the split is the decision ────
    #
    # The two verbs named one module and moved together, and the pair was
    # re-pointed away from U24 on the argument that neither could land. Half of
    # that argument was wrong. ``tombstone.list`` declares no gate, writes
    # nothing, is not destructive, and emits a review set, so conformance 3's
    # loop over its gates never executes a single iteration for it: nothing about
    # R-13's wall touches it, and R36 asks for tombstones to be LISTABLE and
    # revocable, which is a sentence the engine alone cannot satisfy because a
    # person cannot reach the engine.
    #
    # ``delete.review`` lands here. The 2026-08-02 note said it could not,
    # blaming the explicit gate. That wall is down. The remaining wall was a
    # missing database on the conformance fixture. The fixture now substitutes
    # a disposable database, so the verb can exit OK after R34's two acts.
    #
    # Splitting the module is what let ``tombstone.list`` land first. This half
    # stayed until the fixture existed.
    #
    # INLINE, NOT QUEUED, decided by U60. This entry used to declare
    # ``long_running`` with ``argv_builder="delete_argv"``, which is the queueing
    # contract, over a shell that plans, asks and trashes in the invocation that
    # was typed and never enqueued anything (R-149). The drop is the direction
    # taken: the gate is explicit and its digest is the plan, so the person who
    # confirmed a set of files watches them go rather than receiving a job id,
    # and a detached child would rebuild a plan nobody digested.
    Entry(
        name="delete.review",
        summary="review tracks removed from the collection and trash the confirmed files",
        module="cratekit.deletion.cli",
        builder="build_review",
        handler_key="delete.review",
        feature_rows=(37,),
        module_id="deletion",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
        adjudicates=True,
        destructive=True,
        writes=frozenset({"files"}),
        # ``library.trash`` is declared HERE and by nothing else, because
        # this is the only verb that moves a file to the Trash (R35). It is
        # a precondition rather than a note: the deletion pass calls
        # ``trash.assert_usable`` immediately before every move, so a volume
        # with no usable Trash refuses AFTER the review, after the confirm
        # gate, and against a plan already digested.
        doctor_checks=(
            "library.mounted",
            "library.identity",
            "library.trash",
            "rekordbox.closed",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="delete.review.confirm",
                options=("trash", "abort"),
                prompt="Move these files to the system Trash?",
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tombstone.list",
        summary="list and revoke tombstones so a suppressed version is visible",
        module="cratekit.deletion.tombstone_cli",
        builder="build_tombstones",
        handler_key="tombstone.list",
        feature_rows=(37,),
        module_id="deletion",
        emits=frozenset({"review_set"}),
        output_schema="review_set/1",
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
        gates=(
            GateSpec(
                name="export.playlist.confirm",
                options=("export", "abort"),
                prompt="Write this playlist to the streaming service?",
                explicit=True,
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
        module="cratekit.export.prune_cli",
        builder="build_prune",
        handler_key="export.prune",
        feature_rows=(36,),
        module_id="export",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account, and the one write is ``remove_tracks`` on
        #: the remote playlist ``export.playlist`` made, which the outbound
        #: ledger records. ``destructive`` on ``label.prune``'s reason.
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.prune.confirm",
                options=("apply", "abort"),
                prompt="Take these tracks off the remote playlist on the streaming service?",
                explicit=True,
                digest_source="plan",
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
        module="cratekit.export.set_cli",
        builder="build_set",
        handler_key="export.set",
        feature_rows=(36,),
        module_id="export",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account: a playlist is created private and tracks
        #: are added. What was written is recorded in this product's own
        #: outbound ledger, which is not a declared surface. NOT destructive,
        #: on ``export.playlist``'s precedent: every write adds to the account.
        #: A provider candidate accepted in review is READ, never offered.
        #: ``--rename JOB`` (U140) retitles one playlist this product made to
        #: the name the person already gave its INSPIRATION playlist, and
        #: refreezes that name on the set's job, which is this product's own
        #: state. Still not destructive: no track or playlist is taken away,
        #: and a playlist the archive marked is refused rather than retitled.
        writes=frozenset({"remote"}),
        # library.mounted: the no-name backfill opens the rekordbox database
        # over INSPIRATION (U129), and the rename reads it for the live name.
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm",
                options=("apply", "abort"),
                prompt="Make this set a private playlist on the streaming account?",
                # EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
            GateSpec(
                name="export.set.rename",
                options=("apply", "abort"),
                prompt="Rename this set's playlist on the streaming account to its "
                "INSPIRATION playlist's name, and record the new name?",
                # EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="export.archive",
        summary=(
            "file a downloaded set's playlist in Downloaded Sets <year> on the "
            "streaming account, prefixed as downloaded"
        ),
        module="cratekit.export.set_cli",
        builder="build_archive",
        handler_key="export.archive",
        feature_rows=(36,),
        module_id="export",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account: the year's Downloaded Sets folder is
        #: created (U142), the set playlist is put in it, and the playlist is
        #: retitled with the swept prefix, recorded in ``sync mark``'s record
        #: so ``sync unmark`` puts it back.
        #: ``destructive`` for ``label.mark``'s reason: a retitle lands on a
        #: title a person can see.
        writes=frozenset({"remote"}),
        destructive=True,
        # library.mounted: the no-name backfill opens the rekordbox database
        # when it looks up intake proofs under the library (U129).
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm",
                options=("apply", "abort"),
                prompt=(
                    "File this set playlist in Downloaded Sets for its year on the "
                    "streaming account?"
                ),
                # EXPLICIT, as label.mark's is, for the same reason (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
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
        # U43 LANDED IT. ``cratekit.setbuilder.cli`` ships the shell over the
        # engine U35 landed, so the marker is gone and the conformance properties
        # drive this entry rather than skipping it. It declares no write surface
        # and that is load bearing: ``writes={"files"}`` would make it
        # destructive by the invariant above. It DOES keep its index cache, the
        # library scoped state file ``setbuilder_index_cache``, and that is not
        # in ``writes`` on the ruling ``analyze.calibrate`` records above:
        # the vocabulary is the library's own material, files, database and
        # XML, and a cache is none of those (R-188).
    ),
    Entry(
        name="master",
        summary="master a recorded set to a consistent loudness without touching the source",
        module="cratekit.master.cli",
        builder="build",
        handler_key="master",
        feature_rows=(30,),
        module_id="mastering",
        # U105. The source system's ``master_set.sh`` is this verb's
        # predecessor, and until it was named here no test could notice that
        # the predecessor joined split recordings and took a target this verb
        # did not (R-193).
        source_scripts=("master_set.sh",),
        argv_builder="master_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
        # U44 LANDED IT. ``cratekit.master.cli`` ships the shell over the engine
        # U35 landed, so the marker is gone and the conformance properties drive
        # this entry rather than skipping it.
        #
        # THE FLAGS BELOW ARE WHAT THE MARKER WAS HIDING. ``writes={"files"}``
        # makes the verb destructive by the invariant above, and it declares NO
        # gate: the run writes a new file, archives the original with a verified
        # digest, and refuses rather than replacing a master somebody kept, so
        # there is no decision for a person to make. ``--overwrite`` is the one
        # path where something is lost, and the flag is itself the explicit act,
        # which is why no gate sits behind it. ``long_running`` binds
        # ``master_argv``, and that builder carries no ``--run`` precisely
        # because there is no gate whose decision would need a run to name.
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
        # U45 LANDED IT. ``cratekit.backup.cli`` ships the shell over the engine
        # U35 landed, so the marker is gone and the conformance properties drive
        # this entry rather than skipping it.
        #
        # WHY THE MARKER OUTLIVED THE UNIT IT NAMED. U35 landed the ENGINE and no
        # shell, and this entry went on naming a closed issue, so the board showed
        # nothing owed while row 31 sat uncovered. That is the same shape the
        # acquisition rows sat in until U42, and it is why ``planned_in`` is
        # reconciled against ``tests/_pending.PENDING`` rather than trusted.
        #
        # IT DECLARES NO GATE, and that is argued in the shell's own docstring
        # rather than here: the run adds a mirror and a dated archive, replaces
        # nothing a person kept, and writes no database row, so ``writes`` stays
        # empty and the verb is not destructive. ``long_running`` binds
        # ``backup_argv``, and that builder carries no ``--run`` precisely because
        # there is no gate whose decision would need a run to name.
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
        # U28 LANDED IT. ``cratekit.skills.cli`` ships the verb and
        # ``cratekit/skills/assets/`` ships the twelve skills it installs, so the
        # marker is gone and the conformance properties drive this entry rather
        # than skipping it. THE BRIEF'S FILES LINE NAMED ``src/cratekit/cli/skills.py``
        # AND THIS ENTRY WON, as it did for the restore verbs one unit earlier: a
        # module path declared here is the one the dispatcher imports, so a unit
        # that lands the brief's spelling instead lands a module nothing loads.
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
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    # ── Landing (U72) ───────────────────────────────────────────────────────
    #
    # Appended rather than beside its intake siblings, for the reason the block
    # above gives.
    Entry(
        name="intake.land",
        summary="move a folder of acquired files into the library and write one intake file",
        module="cratekit.intake.land_cli",
        builder="build_land",
        handler_key="intake.land",
        feature_rows=(3, 35),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: Files and one XML. The engine renames each file out of staging with
        #: ``os.replace`` and refuses a target that exists, and it refuses an
        #: intake file that exists before the first move. ``place_files`` itself
        #: writes with a plain overwrite, so that check is the only protection
        #: inside the engine. The window after each check is closed by the
        #: verb, which holds one lock per batch name across the apply and
        #: refuses a second landing under a held name (R-432). No
        #: database open. With ``--manifest`` the same XML also gains the label
        #: tree (U77): it is the intake file this run just made that is read
        #: and replaced, never the export, so the write surface is unchanged.
        #: AND THE COLLECTION, SINCE R-746. On a library whose intake tree is
        #: database native the same files, once moved, become content rows and
        #: one batch playlist under the adopted intake root through the guarded
        #: writer, behind the explicit gate below. The intake tree's mode
        #: chooses, the way the routing verbs choose.
        # U129. A set landing may also archive the account playlist, a remote
        # write, so the surface and the provider check join the landing's own.
        # U153. A landed heart's row is coloured Pink in the same commit, a
        # content column, so the metadata surface joins the tree's.
        writes=frozenset({"xml", "files", "db_tree", "db_metadata", "remote"}),
        destructive=True,
        #: The database checks hold for the native medium only, and declaring
        #: them here changes nothing doctor reports: it requires a check when
        #: ANY enabled verb declares it, and adoption, which every profile
        #: carries, already declares these three. ``credential.provider`` is
        #: for the account archive a set landing may perform (U129).
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.land.confirm",
                options=("apply", "abort"),
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
            ),
            # R-746. Content rows in the collection are a new kind of write,
            # answered by a separate recorded act and never inline (R34), and
            # the plan it binds to names every row with every column it sets.
            GateSpec(
                name="intake.land.native",
                options=("apply", "abort"),
                prompt="Move these files into the library and add them to the collection?",
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The deferred mark (U82) ─────────────────────────────────────────────
    #
    # Appended rather than beside its sync siblings, for the reason the
    # deferred routing block above gives.
    Entry(
        name="sync.mark",
        summary="prefix the account playlists a landed sync pass finished",
        module="cratekit.sync.mark_cli",
        builder="build_mark",
        handler_key="sync.mark",
        feature_rows=(3, 25),
        source_scripts=("dj-sync",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account. The only write is ``rename_playlist``, a
        #: retitle keyed by identifier that changes no membership. The cursor
        #: is READ and never written here, no file on the library is written
        #: and no database is opened. Each rename that lands is recorded in
        #: this product's own state, the mark record, which is not a declared
        #: surface. ``destructive`` because a retitle lands on a playlist the
        #: product did not make, and only ``sync unmark``, a separate gated
        #: act, puts the old title back (R-838).
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.mark.confirm",
                options=("apply", "abort"),
                prompt="Rename these playlists on the streaming account?",
                # EXPLICIT, as the other question about a write to the account
                # is. A retitle of a playlist the product did not make is
                # answered by a separate recorded act, never by one more flag
                # on the run that found the question (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── The mark, undone (R-838) ────────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="sync.unmark",
        summary="put back the account playlist titles a sync pass's mark wrote",
        module="cratekit.sync.unmark_cli",
        builder="build_unmark",
        handler_key="sync.unmark",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account, and the one write is ``rename_playlist``,
        #: a retitle back to the title the mark record says the playlist had.
        #: The record is this product's own state and is stamped as each rename
        #: lands; no file on the library is written and no database is opened.
        #: ``destructive`` for ``sync.mark``'s reason: the retitle lands on a
        #: playlist the product did not make.
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.unmark.confirm",
                options=("apply", "abort"),
                prompt="Put these playlist titles back on the streaming account?",
                # EXPLICIT, as sync.mark's is, for the same reason (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── The import proof (R-501) ────────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="intake.imported",
        summary="prove an intake file imported, retire it, and settle its run",
        module="cratekit.intake.imported_cli",
        builder="build_imported",
        handler_key="intake.imported",
        feature_rows=(3, 35),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The intake file this product wrote is RENAMED so the pending scan
        #: stops seeing it, which is a write to a file on the library, so it is
        #: declared as one and the verb is destructive by KTD24's definition.
        #: It is never deleted and never renamed over another file, the target
        #: being claimed first, which is why no confirm gate stands in front of
        #: it: nothing is lost and renaming back undoes it. The Fresh Export is
        #: read and never written, and no database is opened. The session
        #: record it settles is this product's own state, not a declared
        #: surface.
        writes=frozenset({"xml", "files"}),
        destructive=True,
        doctor_checks=("library.mounted",),
    ),
    # ── The export, without rekordbox's menus (R-745) ───────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="export.collection",
        summary="write a collection export from a copy of the database, with rekordbox closed",
        module="cratekit.cli.export_collection",
        builder="build",
        handler_key="export.collection",
        # NO FEATURE ROW. The inventory has no row for producing an export,
        # since the source system never did, and claiming one would make a
        # row look covered by a verb that does something else.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        #: One XML, where the person says, created exclusively and never
        #: replaced, which is why the verb is not destructive and asks nothing.
        #: THE DATABASE IS READ THROUGH A DISPOSABLE COPY and no database
        #: surface is declared. CORE, with no module behind it, although its
        #: sibling under this group is the export module's: the verbs that
        #: read this file are core, and a core workflow cannot wait on a
        #: module somebody switched off.
        #: ``library.paths_resolved`` joined with R-773, since a row under no
        #: prefix rule is written as the database holds it, and that check is
        #: where a person reads how many there are before relying on the file.
        writes=frozenset({"xml"}),
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
    ),
    # ── The folder suggestion (R-797) ───────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="report.genres",
        summary="name every genre holding 50 or more tracks with no top level "
        "folder of its own; creates nothing",
        module="cratekit.adopt.genres_cli",
        builder="build",
        handler_key="report.genres",
        # NO FEATURE ROW, for the reason ``export.collection`` gives: the source
        # system never counted this, and no inventory row asks for it.
        #
        # THE ADOPTION MODULE AND NOT THE REPORTS MODULE, although it sits in
        # the report group. Its siblings read an export through a package that
        # admits no database module. This one reads the database, through the
        # collection reader adoption uses, so it is switched with that reader,
        # which is always available.
        module_id="adoption",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # THE DATABASE IS ONLY READ, as ``route.unplaced`` argues for itself:
        # no surface is declared, the verb is not destructive, and it asks
        # nothing. The pins stay because the binding pin is checked on a read.
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.pins",
        ),
    ),
    # ── A row's genre from its file (R-816) ─────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="tag.rows",
        summary="write each library row's genre from its file where the two "
        "disagree, the genre and nothing else; writes no file",
        module="cratekit.tagging.rows_cli",
        builder="build",
        handler_key="tag.rows",
        # NO FEATURE ROW AND NO SOURCE SCRIPT. The source system patched the
        # genre attribute of an export and never wrote a database row, so no
        # inventory row asks for this and no script is replaced by it.
        #
        # GATED BY ``repair``, as ``tag.retag`` is and for its reason: a
        # corrective pass over metadata the library already holds.
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: THE ROW AND ONLY THE ROW. ``files`` is absent because nothing here
        #: writes one: the file is the authority in this direction and the
        #: engine calls no tag writer. This is the ``GenreID`` relink
        #: ``tag.retag`` declared and never performed (R-246), performed here
        #: for every row whose file disagrees and not only for a retagged one.
        writes=frozenset({"db_metadata"}),
        destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # The plan counts a row under no prefix rule and leaves it alone,
            # so a collection most of whose rows are unmapped plans nothing.
            # The check reads the ratio that makes that plan empty.
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.rows.confirm",
                options=("apply", "abort"),
                prompt="Write the genre on these rows from their files?",
                #: EXPLICIT (R34). A write to rows of a live library is answered
                #: by a separate recorded act with an actor, never by a flag on
                #: the command that discovered the gate.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genres an older mapping wrote, corrected on the file (R-799) ────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="tag.remap",
        summary="rewrite the genre on files a tag job filed by a mapping the "
        "taxonomy has since changed, from what the job recorded; writes no row",
        module="cratekit.tagging.remap_cli",
        builder="build",
        handler_key="tag.remap",
        # NO FEATURE ROW AND NO SOURCE SCRIPT. The source system had no general
        # catalogue and so no word of one to file again.
        #
        # GATED BY ``repair``, as ``tag.retag`` and ``tag.rows`` are: a
        # corrective pass over metadata the library already holds.
        module_id="repair",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: THE FILE AND ONLY THE FILE. The row follows by ``tag.rows``, which
        #: the run names, so no database is opened here and the cloud sync
        #: decision, which binds to write intent on the guarded writer, is not
        #: one this verb can reach.
        writes=frozenset({"files"}),
        destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tag.remap.confirm",
                options=("apply", "abort"),
                prompt="Rewrite the genre on these files?",
                #: EXPLICIT (R34). A genre is written once and stays, so the
                #: rewrite of one is answered by a separate recorded act with
                #: an actor, over a plan a person has read.
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── A genre for a row with none (U114) ──────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="tag.suggest",
        summary="suggest a genre for each row with none on the row or the file, "
        "from its artist, its folder and optionally the catalogues; writes file and row",
        module="cratekit.tagging.suggest_cli",
        builder="build",
        handler_key="tag.suggest",
        # NO FEATURE ROW AND NO SOURCE SCRIPT. The source system left a track
        # with no genre to a person in rekordbox, and no inventory row asks for
        # a suggestion.
        #
        # CORE, as ``tag.folder`` is: it tags, and a genre is what adoption
        # files by, so a core workflow does not wait on a module switched off.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: THE FILE AND THE ROW, so the two agree. The file through the one
        #: genre writer, the row through the ``GenreID`` relink ``tag.rows``
        #: performs, under the same guard.
        writes=frozenset({"files", "db_metadata"}),
        destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.suggest.confirm",
                options=("apply", "abort"),
                prompt="Write these suggested genres on the files and their rows?",
                #: EXPLICIT (R34), for the reason ``tag.rows.confirm`` gives.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX rotation (U111) ───────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The
    # report it grows out of is ``report.intake-aging``, which only reads.
    Entry(
        name="inbox.rotate",
        summary="move stale INBOX batches into INBOX / Old and remove expired ones "
        "from Old, never a track",
        module="cratekit.intake.rotate_cli",
        builder="build",
        handler_key="inbox.rotate",
        # Row 20 is the aging report's, and this is the half of the source
        # system's rotation that report left to a person.
        feature_rows=(20,),
        source_scripts=("dj-inbox-rotation",),
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else. A playlist node under the
        #: intake root is moved or soft deleted with its own memberships, and
        #: no content row, no file and no other playlist's membership changes.
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("inbox", "inbox_old"),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="inbox.rotate.approve",
                options=("approve", "abort"),
                prompt="Move these batches into Old and remove these from it, "
                "keeping every track?",
                #: EXPLICIT (R34). A removal takes a playlist out of the
                #: library, so no blanket affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX refill (U134) ─────────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The
    # rebuild of an account playlist's INBOX mirror from the pass that made it,
    # for a playlist emptied after it landed.
    Entry(
        name="inbox.refill",
        summary="refill each INBOX playlist a pass mirrored from the author's account, "
        "every track the library owns in the account's order, memberships only",
        module="cratekit.intake.refill_cli",
        builder="build",
        handler_key="inbox.refill",
        # NO FEATURE ROW. The source system never mirrored an account playlist.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: memberships of playlists already
        #: under the intake root. No content row, no playlist row, no file.
        writes=frozenset({"db_tree"}),
        taxonomy_terms=("inbox",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="inbox.refill.approve",
                options=("apply", "abort"),
                prompt="Add these tracks to their INBOX playlists?",
                #: EXPLICIT (R34). A write outside the intake flow, answered by
                #: a recorded act, as the set playlist's backfill is.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── INBOX / Analyze, cleared (U166) ─────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. Every
    # native landing adds the rows it creates to the one playlist the
    # rekordbox visit selects; this takes out each row rekordbox analysed.
    Entry(
        name="inbox.analyzed",
        summary="take every row rekordbox has analysed out of INBOX / Analyze, leaving "
        "each row still waiting, memberships only",
        module="cratekit.intake.analyzed_cli",
        builder="build",
        handler_key="inbox.analyzed",
        # NO FEATURE ROW. The source system never kept an analysis queue.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: memberships of one playlist
        #: under the intake root, soft deleted. No content row, no playlist
        #: row, no file.
        writes=frozenset({"db_tree"}),
        taxonomy_terms=("inbox",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="inbox.analyzed.approve",
                options=("apply", "abort"),
                prompt="Take these analysed tracks out of INBOX / Analyze, keeping "
                "every track in the collection?",
                #: EXPLICIT (R34). A removal from a playlist, answered by a
                #: recorded act, as the refill's addition is.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The rekordbox visit, checked (U167) ─────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. After
    # the visit, one read only answer: is every landed row analysed, is each
    # grid right, is the Key column filled, and how far rekordbox's key agrees
    # with the title's. Its exit status is the verdict, so a skill can wait on it.
    Entry(
        name="analyze.check",
        summary="read rekordbox's analysis of the landed rows and say whether the visit "
        "is done, still waiting, or suspect; reads a copy, writes nothing",
        module="cratekit.analysis.check_cli",
        builder="build",
        handler_key="analyze.check",
        # NO FEATURE ROW. The source system never read rekordbox's result back.
        # CORE, NOT THE ANALYSIS MODULE: it runs no detector and needs no
        # extra, it reads rekordbox's own analysis through the binding every
        # install has, and the landing it follows is core, so a slim install
        # that lands rows can ask whether rekordbox finished with them.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        doctor_checks=("library.mounted", "rekordbox.closed"),
    ),
    # ── The set's permanent playlist (U121) ─────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The
    # landing writes the playlist itself when given ``--set``; this is the
    # backfill for a set that landed without it.
    Entry(
        name="intake.inspiration",
        summary="write a landed set's permanent playlist under INSPIRATION, every "
        "identified track the library owns in set order, named the source system's way",
        module="cratekit.intake.inspiration_cli",
        builder="build",
        handler_key="intake.inspiration",
        # NO FEATURE ROW. The source system made these playlists by hand, and
        # the author decided on 2026-10-09 that every set intake leaves one.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: one playlist node under the
        #: declared INSPIRATION folder, that folder when the root lacks it, and
        #: the memberships. No content row, no file, no INBOX node.
        writes=frozenset({"db_tree"}),
        taxonomy_terms=("inspiration",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="intake.inspiration.approve",
                options=("apply", "abort"),
                prompt="Write the set's playlist under INSPIRATION with these tracks?",
                #: EXPLICIT (R34). A node written outside the intake flow stays
                #: in the library for good, so no blanket affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genre Favorites (U119) ──────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The one
    # path that removes a genre Favorites membership; the additive half runs at
    # the end of an adoption that files a track and inside the tree rebuild.
    Entry(
        name="favorites.refresh",
        summary="make every genre folder's Favorites playlist mirror All Favorites, "
        "adding what the folder holds that is a favourite and removing what is not",
        module="cratekit.favorites.refresh_cli",
        builder="build",
        handler_key="favorites.refresh",
        # NO FEATURE ROW. The source system never kept a Favorites per genre;
        # the author decided it on 2026-10-09.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: one Favorites playlist under
        #: each genre folder, and memberships added to it and marked removed
        #: from it. No content row, no file, no node removed.
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("genre_energy", "favorites"),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="favorites.refresh.approve",
                options=("approve", "abort"),
                prompt="Make each genre folder's Favorites mirror All Favorites, adding "
                "these and removing those?",
                #: EXPLICIT (R34). A removal takes a membership away, so no
                #: blanket affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The landed hearts placed (U120) ─────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The
    # native landing places a heart as it lands since U120, and an owned heart
    # too since U146; this is the backfill for the hearts placed before then,
    # every owned heart a hearts job reported, and for a landing whose source
    # playlist was absent and skipped the placement.
    Entry(
        name="favorites.backfill",
        summary="put every heart on the account whose track the library owns into All "
        "Favorites and the playlist of the month it was hearted in, adding and never removing",
        module="cratekit.favorites.backfill_cli",
        builder="build",
        handler_key="favorites.backfill",
        # NO FEATURE ROW. The source system did this as part of its favourites
        # pass; the author decided on 2026-10-09 that a landing does it here.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree, memberships added to All Favorites and to a
        #: month playlist, that playlist when the folder lacks it, and since
        #: U153 one content column, the colour, Pink on every member that has
        #: none. No content row made, no file, no node removed, no removal.
        writes=frozenset({"db_tree", "db_metadata"}),
        destructive=True,
        taxonomy_terms=("favorites",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="favorites.backfill.approve",
                options=("approve", "abort"),
                prompt="Put these landed hearts into All Favorites and their month "
                "playlists?",
                #: EXPLICIT (R34). A write to the live library's playlists, as
                #: the refresh's and the landing's are, so no blanket
                #: affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The quarters split into months (U145) ───────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. A one
    # time verb: since U145 a landed heart files by month, and this splits the
    # quarter playlists already under Favorites into months and retires them.
    Entry(
        name="favorites.split",
        summary="split every quarter playlist beside All Favorites into the playlists of "
        "the months its hearts were hearted in, then retire the emptied quarters",
        module="cratekit.favorites.split_cli",
        builder="build",
        handler_key="favorites.split",
        # NO FEATURE ROW. The source system filed by quarter; the author chose
        # months on 2026-10-14.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: memberships added to month
        #: playlists under the Favorites folder, those playlists when absent,
        #: and each quarter playlist retired with its own memberships, a soft
        #: delete. No content row and no file.
        writes=frozenset({"db_tree"}),
        destructive=True,
        taxonomy_terms=("favorites",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="favorites.split.approve",
                options=("approve", "abort"),
                prompt="Put these quarter playlists' hearts into their month playlists and "
                "retire the quarters?",
                #: EXPLICIT (R34). It retires playlists of the live library, so
                #: no blanket affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The retroactive tidy (U112) ─────────────────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. A
    # COMPOSER, as ``sync.all`` is: every step it plans is another verb's plan
    # and every write another verb's write, so it owns no rule of its own.
    Entry(
        name="organize",
        summary="tidy rekordbox and the account by the product's own rules, one "
        "question per side; lists what you made and never moves it",
        module="cratekit.organize.cli",
        builder="build",
        handler_key="organize",
        # NO FEATURE ROW. The source system never tidied retroactively, and
        # each row a step serves is claimed by the verb that owns the step.
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        #: The union of its steps' surfaces: adoption writes the tree and its
        #: rows, the rotation the tree, the label folders, the marks and the
        #: archive the account. The set archive reads the INSPIRATION folder
        #: for its second proof (U142), through a read handle, and the
        #: parity step (U144) writes a playlist per downloaded set under that
        #: folder, which is the tree, from the account's sets. No file is
        #: written by any step it composes,
        #: since the adoption is applied with no tag value. ``destructive``
        #: because the rotation removes an expired batch playlist, a mark
        #: retitles a playlist the product did not make, and the root step
        #: (U143) removes the account root's label debris, empty playlists and
        #: an emptied legacy year folder, each by name on the account's gate.
        writes=frozenset({"db_tree", "db_metadata", "remote"}),
        destructive=True,
        taxonomy_terms=("genre_energy", "inbox", "inbox_old", "inspiration"),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="organize.rekordbox.approve",
                options=("approve", "abort"),
                prompt="Apply these steps to the rekordbox library? Nothing you "
                "made is moved and no track is removed.",
                #: EXPLICIT (R34). It stands for ``adopt.apply.approve`` and
                #: ``inbox.rotate.approve``, both explicit.
                explicit=True,
                digest_source="plan",
            ),
            GateSpec(
                name="organize.account.apply",
                options=("apply", "abort"),
                prompt="Apply these steps to the streaming account? Only the "
                "removals listed are made: label debris whose tracks are in its "
                "label's folder, empty root playlists, and an emptied legacy year "
                "folder. A working custom playlist stays at the root until a "
                "sync marks it downloaded, which files it in its year folder.",
                #: EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A label's dated playlist heard (U123) ───────────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives. The
    # half of U117 that happens once the author has heard a go's releases.
    Entry(
        name="label.heard",
        summary=(
            "mark a label's dated playlist heard: its tracks go in the year "
            "playlist and the dated playlist is removed from the account"
        ),
        module="cratekit.label.heard_cli",
        builder="build_heard",
        handler_key="label.heard",
        feature_rows=(23,),
        module_id="labels",
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: One surface, the account: tracks added to a year playlist, and a
        #: dated playlist the outbound ledger records this product CREATED
        #: taken tracks off or removed. The heard list is written in the label
        #: review store and the ledger entry dropped, neither of which is a
        #: declared surface. Nothing in rekordbox is written: the Record
        #: Labels tree stays on the xml bridge (R39). ``destructive`` because
        #: it removes a playlist from the account.
        writes=frozenset({"remote"}),
        destructive=True,
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.heard.confirm",
                options=("apply", "abort"),
                prompt="Mark these releases heard, put the dated playlist's tracks in "
                "the year and remove it from the streaming account?",
                #: EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── The taxonomy copy brought up to the shipped schema (U132) ───────────
    #
    # Appended, for the reason the deferred routing block above gives. Setup
    # copies the shipped template once; this is how a class or a bucket the
    # shipped template gained since reaches a library's copy.
    Entry(
        name="taxonomy.upgrade",
        summary="add the classes and buckets the shipped taxonomy template declares "
        "and this library's copy lacks, and state the shipped schema version",
        module="cratekit.cli.verbs.taxonomy",
        builder="build",
        handler_key="taxonomy.upgrade",
        # NO FEATURE ROW. The source system had one taxonomy table in code and
        # nothing to upgrade.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: No declared surface: the library's taxonomy copy beside the
        #: database, and a dated backup of it, which are library state as the
        #: profile verb's configuration is. No database row, no audio file, no
        #: account. Not destructive: it only adds, and the copy as it was is
        #: kept beside it.
        writes=frozenset(),
        #: The copy it upgrades is read by the verb itself, which refuses an
        #: absent or unusable one by name before its gate, so taxonomy.active
        #: is not declared here as well.
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.upgrade.apply",
                options=("approve", "abort"),
                prompt="Add these classes and buckets to this library's taxonomy copy "
                "and state the shipped schema version?",
                #: EXPLICIT (R34). The copy is the declaration every verb routes
                #: by, so no blanket affirmative satisfies it.
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── A playlist pair, kept one list on both sides (U130) ─────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="sync.pair",
        summary="keep one of your account playlists and one rekordbox playlist the "
        "same list, each side merged against the last sync",
        module="cratekit.sync.pair_cli",
        builder="build",
        handler_key="sync.pair",
        # NO FEATURE ROW. The source system pulled a playlist one way and pushed
        # one the other, and kept no list on both sides.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: Two surfaces. The rekordbox playlist's memberships, added, soft
        #: removed and numbered through the guarded commit, and the account
        #: playlist's tracks, added, taken off and ordered, on a playlist the
        #: pairs record vouches for. No collection row and no audio file is
        #: written, and an acquisition is a queued intake job, not a write. The
        #: pair and its snapshot are this product's own state. ``destructive``
        #: because a membership is taken off on both sides.
        writes=frozenset({"db_tree", "remote"}),
        destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.pair.rekordbox",
                options=("apply", "skip"),
                prompt="Write these additions, removals and order to the rekordbox "
                "playlists, and queue these tracks for acquisition?",
                #: EXPLICIT, as every database membership write is (R34).
                explicit=True,
                digest_source="plan",
            ),
            GateSpec(
                name="sync.pair.account",
                options=("apply", "skip"),
                prompt="Write these additions, removals and order to the streaming "
                "account's playlists?",
                #: EXPLICIT, as every other write to the account is (R34).
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The custom playlist twins' backfill (U149) ──────────────────────────
    #
    # Appended, for the reason the deferred routing block above gives.
    Entry(
        name="sync.twins",
        summary="give every downloaded custom playlist on the account its permanent "
        "twin in rekordbox's Custom Playlists <year> folder, paired to stay one list",
        module="cratekit.sync.twins_cli",
        builder="build",
        handler_key="sync.twins",
        # NO FEATURE ROW. The source system let a custom playlist's rekordbox
        # copy rotate out and kept none.
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The database tree and nothing else: a top level folder per year when
        #: absent, a plain playlist per twin under it, and its memberships. No
        #: content row, no file, nothing on the account. The pairs it marks are
        #: this product's own state. Not ``destructive``: it removes nothing.
        writes=frozenset({"db_tree"}),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.twins.approve",
                options=("approve", "abort"),
                prompt="Make these twins and their folders in rekordbox, and pair each "
                "with its account playlist?",
                #: EXPLICIT, as every database membership write is (R34).
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
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
