"""The one register of guards that are written but not yet armed.

U6 ports the safety net BEFORE the engine it guards, on purpose: a guard that
arrives after the code it governs can only ever confirm what already shipped,
while a guard that arrives first makes the violation impossible to introduce
silently. The cost of that ordering is that some ported guards name a module
that does not exist yet.

The rule for handling that cost, and the reason this file exists:

1. A pending guard keeps its FULL ported assertion body. It is never weakened,
   never reduced to a placeholder, and the production module is never stubbed
   just to make it green. A stub would turn a real guard into a test of the stub.
2. It is gated behind a skip whose reason names the unit that unblocks it, so
   anyone reading a skipped test learns what has to land, not just that something
   is missing.
3. Every such skip is declared here, and tests/test_pending_units.py asserts the
   declared set is exactly the intended set AND that each target is genuinely
   still absent. The moment a unit lands its module, that meta-test goes red and
   the only way to make it green is to delete the entry, which arms the guard.

That third point is the whole design. Without it, a skip added for a good reason
in August is still silently skipping in December, and the safety net has a hole
nobody can see. With it, a skip is a countdown, not a hiding place.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Guards awaiting the module they govern.
#
# key   -> a stable identifier for the thing that is missing. For an import
#          target this is the dotted module path, checked with find_spec. For a
#          non-import target it is a "path:" key, checked against the filesystem.
# value -> (unit that lands it, one line saying what the guard asserts)
# ---------------------------------------------------------------------------
PENDING: dict[str, tuple[str, str]] = {
    "cratekit.intake.collection_xml": (
        "U37",
        "the COLLECTION TRACK emitter that must never emit a <TEMPO> element. "
        "A SECOND OBLIGATION arrives with U19 and is registered here because U37 "
        "owns the pipeline that owes it (P5): intake must record each new track's "
        "routing intent AT THE MOMENT the placement is decided, through "
        "cratekit.write.routing_pass.record_intents, rather than at the end of "
        "the run. U19's whole mechanism hangs off that one call. Without it "
        "nothing is ever deferred, every run closes with no outstanding tracks "
        "because none were ever recorded, and the deferred-routing suite stays "
        "green over a feature that never runs. A THIRD OBLIGATION, same unit and "
        "same reason: a run that deferred a placement closes through "
        "cratekit.write.routing_pass.close_run, never through "
        "cratekit.core.session.close_session, because the gate is opt-in and its "
        "bypass is the exported call",
    ),
    "cratekit.acquire.match_cli": (
        "U16",
        "that R11's three states are split the way U11 declared them: the "
        "NEEDS REVIEW state becomes persisted review items in the version-match "
        "queue, while matched and missing stay a plain match result, and neither "
        "of those two ever reaches the queue. Registered here rather than "
        "asserted in a docstring because U11 settled the split and U16 is the "
        "first unit that can violate it (P5)",
    ),
    "cratekit.modules.reports": (
        "U34",
        "that the duplicate audit's pairs become review items in the queue U11 "
        "declared for them, which is half of R26. The source system's audit "
        "prints and never records, so a pair somebody already judged an "
        "intentional alternate is reported again on every run, and a private "
        "ignore file beside the report would satisfy the brief and re-create the "
        "defect. Registered here because U11 declared the surface and nothing "
        "else forces it to exist (P5)",
    ),
    "cratekit.adopt": (
        "U23",
        "that the adoption plan is presented as review items rather than as a "
        "plan file, which is the other half of R26. A plan approved 30 percent "
        "through and resumed in a later session needs verdicts that outlive the "
        "process that collected them, which is exactly what a file the user edits "
        "cannot give it",
    ),
    "cratekit.intake": (
        "U37",
        "that a path repair proposal is offered into the queue U11 declared for "
        "it rather than applied. A wrong answer re-points a library row at "
        "somebody else's file, so the proposal is never applied without a "
        "decision, and the decision is never read back out of a file somebody "
        "edited",
    ),
    "cratekit.deletion.cli": (
        "U24",
        "that a declined file and a tombstoned version are recorded through the "
        "decision stores U11 shipped, and are therefore REVOCABLE: R35 says a "
        "declined file is never offered again until the decline is revoked and "
        "R36 says a tombstone is listable and revocable, and both sentences are "
        "false if the deletion pass keeps its own file instead",
    ),
    "cratekit.cli.doctor": (
        "U27",
        "that a database acknowledged outside the library root is REPORTED on "
        "every run, so the snapshot that is a copy rather than an atomic commit "
        "stays visible long after the date somebody accepted it",
    ),
    "path:skills": (
        "U28",
        "the shipped operator skills the skills lint runs over",
    ),
    "cratekit.cli.exit_codes": (
        "U38",
        "that every structured refusal cause the standalone utilities raise has "
        "a reserved exit code and a remediation, which is the S4 obligation "
        "applied to this unit: a refusal with no reserved code collapses to a "
        "bare status at the process boundary and cannot be recovered downstream",
    ),
    # APPENDED RATHER THAN FILED BESIDE A SIBLING, deliberately, for the reason
    # the verb registry gives for the same choice: two entries inserted into the
    # middle of one mapping by two units auto-merge, and an append conflicts
    # textually, which is a conflict somebody reads.
    "cratekit.write.routing_cli": (
        "U20",
        "the command-line surface for the four route.* verbs, and the obligation "
        "that every one of them closes its run through "
        "cratekit.write.routing_pass.close_run rather than through the exported "
        "cratekit.core.session.close_session, because the close gate is opt-in "
        "and its bypass is the public call. REGISTERED HERE RATHER THAN LEFT AS "
        "A planned_in MARKER because scripts/board.py reads this file and "
        "nothing else, so an obligation carried only by a marker on a closing "
        "unit is owned by nobody the moment that unit closes (P5). RE-POINTED "
        "FROM U19 TO U20, and the reasoning is left legible because it is a "
        "judgement a human may want to move again: U19 could not land the "
        "module because conformance 3 requires a landed gated verb to exit OK "
        "once its gate is answered, and a destructive db_tree verb cannot do "
        "that on a machine with no database. U20 is the unit that flips trees "
        "to database-native and therefore must ship a destructive database "
        "surface anyway. A SECOND OBLIGATION rides on the same unit because the "
        "same unit owns the records it needs: a re-run of the routing pass after "
        "somebody renames a destination folder must CONVERGE rather than refuse. "
        "U19 refuses today, which is correct but is not service. Converging "
        "needs a persisted map from the stable destination identifiers to the "
        "node identifiers a previous write used, which is the shape the tree "
        "registry already has for a tree's adopted root, and U20 is the unit "
        "that owns that record. Building a second one inside the routing pass "
        "would give two answers to which node a destination is",
    ),
    "cratekit.session.restore_cli": (
        "U27",
        "the command-line surface for the two restore verbs, which the registry "
        "declares against this module and which U32 could not land. REGISTERED "
        "HERE RATHER THAN LEFT AS A planned_in MARKER for the reason the routing "
        "CLI above gives at length: scripts/board.py reads this file and nothing "
        "else, so an obligation carried only by a marker on a closing unit is "
        "owned by nobody the moment that unit closes (P5). WHY U32 COULD NOT LAND "
        "IT, stated so a human can judge whether to move this: conformance 3 "
        "requires a landed gated verb to exit OK once its gate is answered, and "
        "restore.run is destructive, writes db_tree, and would have to perform a "
        "real restore of a real capture against a real database to exit OK at "
        "all. The two verbs name one module, so landing either lands both. "
        "RE-POINTED TO U27 rather than to any other open unit, and the reasoning "
        "is left legible because it is a judgement somebody may want to move "
        "again: U27 owns the operator-facing surface, must already solve exactly "
        "this problem for doctor.repair-paths, which is destructive and carries "
        "the same marker, and ships the status verb whose own summary promises to "
        "report open runs and unconverged trees, which are the two things "
        "cratekit.core.restore and cratekit.core.reconcile now record. A SECOND "
        "OBLIGATION rides on the same module because the same module owns the "
        "composition: the verb holds ONE session across the whole restore, "
        "through cratekit.core.restore.recovery_session, and passes that value's "
        "`guard` in as backup.plan_restore's and backup.run_restore's `gates`. "
        "The default shape takes the library lock twice and a second process can "
        "commit in the window between them, leaving the run to copy a snapshot "
        "over a commit its plan was built before. U32 landed and tested the "
        "composition; what is left is the one wiring call, and it is left here "
        "because core may not import the modules layer",
    ),
    # KEYED ON THE MODULE U36 ACTUALLY LANDS. This entry said
    # ``cratekit.write.rebuild`` and no such module was ever going to exist: U36
    # lands ``cratekit.write.tree_rebuild``, and both the `converge` and `rebuild`
    # verbs are declared against ``cratekit.write.converge_cli`` in
    # ``cli/registry.py`` against U20. So ``_is_absent`` was permanently True and
    # ``scripts/board.py contradictions()`` would have returned exit 2 for the rest
    # of the project's life the moment U36 closed, which ``sync`` deliberately will
    # not repair. A key that can never resolve is not a countdown, it is a
    # permanent red light that teaches people to ignore the audit.
    "cratekit.write.tree_rebuild": (
        "U36",
        "TWO OBLIGATIONS, both about the same fact recorded in two places. "
        "FIRST, that an unconverged tree is cleared ONLY through a convergence "
        "check reporting no difference, never by a bare disposition. "
        "cratekit.core.reconcile records a tree marker and exposes one "
        "`disposition` call because effects and trees share a store, and that "
        "call is the softening path: a rebuild unit that closed a tree marker "
        "with a verdict and no convergence check would satisfy every test in "
        "this repository while leaving the tree exactly as short as it was. "
        "Registered here rather than asserted in a docstring because U32 built "
        "the store and U36 is the first unit that can violate it (P5). R39's own "
        "escape hatch is not this: an explicit, logged operator disposition that "
        "scopes the refusal to one tree is U36's to design, and it is a different "
        "act from a rebuild reporting success. SECOND, and this is the one that "
        "has to be discharged in the commit that removes this entry: U32 and U36 "
        "both discovered that a database-native tree can be left short, from "
        "opposite directions, and each wrote it into its own store with its own "
        "gate, exemption, clearing call and refusal slug. U32 settled the "
        "ownership on core.convergence and hands the fact over through "
        "core.restore._hand_tree_shortness_over, which resolves that module at "
        "call time because it does not exist in U32's build. When it does, the "
        "fallback branch in that function and the whole "
        "reconcile.Kind.UNCONVERGED_TREE path behind it are dead weight recording "
        "a fact a rebuild does not clear, and leaving them is how the two answers "
        "come apart again",
    ),
}


def _is_absent(key: str) -> bool:
    """True when the thing named by ``key`` has not landed yet.

    Import targets are probed with ``find_spec`` rather than a real import, so a
    probe can never execute module-level code and never has an import failure of
    its own to distinguish from absence.
    """
    if key.startswith("path:"):
        return not (REPO_ROOT / key[len("path:") :]).exists()
    try:
        return importlib.util.find_spec(key) is None
    except ModuleNotFoundError:
        # A parent package is missing, so the target is certainly missing too.
        return True


def requires(key: str) -> pytest.MarkDecorator:
    """Gate a ported guard on the unit that lands the thing it guards.

    Usage::

        @requires("cratekit.core.rb_writer")
        def test_creating_a_track_row_is_forbidden():
            ...

    The skip reason always names the unit, so ``pytest -rs`` reads as a work
    queue rather than as a list of mysteries.
    """
    if key not in PENDING:
        raise KeyError(
            f"{key!r} is not declared in _pending.PENDING. Add it there with the "
            f"unit that lands it, so tests/test_pending_units.py can hold it "
            f"accountable, or the skip becomes permanent by accident."
        )
    unit, what = PENDING[key]
    return pytest.mark.skipif(
        _is_absent(key),
        reason=f"{key} lands in {unit}; this guard asserts {what}",
    )
