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
        "the command-line surface for delete.review, the one verb of this unit "
        "that could not land with the engine. THE RE-POINT TO U27 IS REVERTED "
        "and the reasoning is left legible because it is a judgement a human may "
        "want to move again. U27 is a wizard and a doctor: it ships no deletion "
        "domain, no destructive verb, and it proved on the same evening that it "
        "could not carry an explicitly gated verb by moving doctor.repair-paths "
        "away for this identical reason. Worse, it CLOSES in this wave, so the "
        "re-point moved a contradiction from one closing unit to another rather "
        "than resolving it. THE WALL RECORDED HERE ON 2026-08-02 IS STALE AND "
        "THIS IS THE CORRECTION. That entry said the wall was R34 and "
        "conformance 3, because an explicit gate could not be answered the way "
        "the product answers one, and it asserted that a missing database was "
        "NOT the problem. Main's 3269ab1 rewrote conformance 3 and the gate wall "
        "is down: built and driven on a throwaway merge of main on 2026-08-03, "
        "delete.review refuses at its gate, refuses an inline answer without "
        "recording it, takes the answer from a separate run decide act with its "
        "actor, and resumes past it. It then stops at exit 22, "
        "library-directory-missing, which is the wall the stale entry denied. "
        "Reading the collection is what this verb IS, so it cannot exit OK on a "
        "machine with no rekordbox database, and the conformance fixture is such "
        "a machine. That is R-13's original database wall, whose closing "
        "condition is a disposable fixture on the CRATEKIT_TEST_DB convention "
        "and whose natural owner is U27. THIS ENTRY IS THEREFORE WHAT MAKES A "
        "Closes #24 TRAILER RETURN board.py audit EXIT 2 PERMANENTLY, and "
        "clearing it is a decision about who owns the fixture rather than a "
        "repair. tombstone.list did NOT need to wait, declares no gate, and "
        "landed as cratekit.deletion.tombstone_cli. U24's other obligation, that "
        "a declined file and a tombstoned version are recorded through the "
        "revocable decision stores U11 shipped, is DISCHARGED: the package "
        "landed and the guard in tests/test_review_queue.py runs unconditionally "
        "over cratekit.deletion. TWO OBLIGATIONS OWED BY OTHER UNITS RIDE HERE, "
        "on this long-lived key, because both were first appended inside entries "
        "that the countdown forces this same wave to delete, which would have "
        "retired them the evening they were written (P5). One, owed by U27: "
        "doctor reports whether the library volume has a usable Trash, through "
        "cratekit.deletion.trash.probe with create=False so the check cannot "
        "pass by having run, because R35 sends a confirmed file to the system "
        "Trash and never to an unlink, and a person otherwise meets that refusal "
        "in the middle of a deletion. Two, owed by U16: a candidate the "
        "tombstone store suppresses is REPORTED as suppressed rather than "
        "omitted (R36), asked through cratekit.core.tombstone.version_identity "
        "rather than by comparing artist and title some other way, because a "
        "recorder and a consulter agreeing without coordinating is the only "
        "thing that makes a tombstone match anything at all",
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
        "would give two answers to which node a destination is. THAT MAP NOW "
        "EXISTS: U36 landed it as cratekit.core.convergence.DestinationNode, "
        "recorded per tree and read back through "
        "cratekit.write.rebuild.resolve_destinations, so the obligation on "
        "U20 narrowed from building the record to READING it. Building a second "
        "one would still give two answers",
    ),
    # THREE THINGS THE MERGE WITH U32 HAS TO DO IN THIS FILE AND ITS SIBLINGS,
    # verified against a real merge on 2026-08-02 rather than inferred:
    #
    # 1. U32 carries an entry keyed ``cratekit.write.tree_rebuild``, re-keyed
    #    there from ``cratekit.write.rebuild`` on the belief that U36 would ship
    #    the former. U36 ships ``src/cratekit/write/rebuild.py``, which is what
    #    issue #36's Files line names, so on the merged tree U32's key is the one
    #    that can never resolve. RE-KEY IT BACK TO ``cratekit.write.rebuild``.
    #    Left alone it is a permanent red light that teaches people to ignore the
    #    audit, which is the exact failure the U32 comment beside it describes.
    # 2. ``tests/test_pending_units.py`` carries the same spelling in
    #    ``EXPECTED_PENDING`` and moves with it.
    # 3. Once re-keyed, ``_is_absent`` answers False and the meta-test goes red,
    #    which is the countdown FIRING rather than a problem. Discharging it means
    #    deleting the entry in a commit that also removes the fallback branch in
    #    ``restore._hand_tree_shortness_over`` and the
    #    ``reconcile.Kind.UNCONVERGED_TREE`` path behind it, exactly as U32's own
    #    entry text asks.
    "cratekit.cli.rebuild": (
        "U20",
        "the command-line surface for the rebuild verb, and the obligation that "
        "the operator disposition which clears a refusal for one tree is an "
        "EXPLICIT, LOGGED act by a named person: never a flag that clears every "
        "tree, and never an actor derived from the environment or from the "
        "process owner. cratekit.core.convergence.Disposition refuses an empty "
        "actor, so the surface has to carry a real one, and the guard behind "
        "this entry drives that refusal directly. A SECOND OBLIGATION, same "
        "unit: the verb clears a tree's flag only through "
        "cratekit.write.rebuild.rebuild_tree, whose clearing call is handed the "
        "convergence check's own difference list, never through a bare "
        "convergence.clear_unconverged or a bare reconcile disposition. "
        "REGISTERED HERE RATHER THAN LEFT AS A planned_in MARKER because "
        "scripts/board.py reads this file and nothing else, so an obligation "
        "carried only by a marker on a closing unit is owned by nobody the "
        "moment that unit closes (P5). RE-POINTED FROM U36 TO U20 by the "
        "reasoning that re-pointed the routing CLI: conformance 3 requires a "
        "landed gated verb to exit OK once its gate is answered, and rebuild "
        "writes db_tree and is destructive, which cannot exit OK on a machine "
        "with no rekordbox database. U20 is the unit that flips trees to "
        "database-native and must therefore ship a destructive database surface "
        "anyway. ONLY REBUILD IS BEHIND THAT WALL. U36 first parked converge "
        "here too, because both verbs named one module and this countdown keys "
        "on the module; converge declares no gates, is destructive of nothing, "
        "and is what both of this unit's refusals name as remediation step one, "
        "so parking it parked the remedy. It landed with U36 as "
        "cratekit.cli.converge and is read only by contract: a diagnostic that "
        "needed the gates the unconverged flag is holding shut is a diagnostic "
        "nobody can reach",
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
    # THE ``cratekit.write.rebuild`` ENTRY WAS HERE AND IS DELETED, because U36
    # LANDED. It shipped ``src/cratekit/write/rebuild.py`` on `main` in this
    # session, and issue #36 is closed. A register that still owes a closed unit a
    # module is the contradiction ``scripts/board.py audit`` exits 2 on, and the
    # repository's own rule for that exit is to reopen the issue or clear the
    # entry, never to leave it: U36 is finished, so the entry goes.
    #
    # WHAT THE ENTRY WAS HOLDING, and where each half went, because deleting a
    # countdown without saying that is how an obligation evaporates:
    #
    # * that a rebuild clears an unconverged tree only on a convergence check and
    #   never on a bare disposition. U36's own suite drives this rather than
    #   grepping for it: `tests/test_rebuild.py` on `main` refuses
    #   `clear_unconverged` while the check still differs, and its rebuild
    #   disposes with REPAIRED rather than ACCEPTED. Discharged.
    # * that the call-time resolution of `core.convergence` in
    #   `core.restore._hand_tree_shortness_over`, and the
    #   `reconcile.Kind.UNCONVERGED_TREE` fallback behind it, are deleted once the
    #   two modules share a build. NOT discharged, and it cannot be discharged
    #   from this branch, whose tree has no `core.convergence` to import. It is
    #   item 3 of R-21 in `docs/residual-findings.md`, and
    #   `tests/test_restore.py` now carries an always-armed tripwire that fails
    #   the moment both modules are present with the fallback still there. That is
    #   a countdown that needs no register key, so it cannot be orphaned by a unit
    #   closing.
    # APPENDED, same reason as the entry above it.
    "cratekit.cli.reports": (
        "U27",
        "the command-line surface for audit.coverage, audit.duplicates, "
        "report.library and report.intake-aging, and the two report engines two "
        "of them still have none of: nothing in the tree computes tree coverage "
        "or library statistics. REGISTERED HERE RATHER THAN LEFT AS A planned_in "
        "MARKER for the reason R-13 records and mechanizes against: scripts/"
        "board.py reads this file and nothing else, test_cli_contract only fires "
        "once the module APPEARS, and an obligation carried only by a marker on "
        "a closing unit is owned by nobody the moment that unit closes (P5). "
        "RE-POINTED FROM U34, whose declared file list is the reports package "
        "and its test module and which landed exactly that, and whose four "
        "markers would all have named a closed unit the instant #34 merged. The "
        "module path moved too, from cratekit.reports.cli, which test_layering "
        "ranks modules while the registry it must dispatch through ranks cli, so "
        "it could not have been built as spelled; that is the same correction "
        "U10 and U11 each made on landing. U27 is the owner because it is the "
        "only open unit already landing modules in src/cratekit/cli/, because "
        "three of the four verbs emit the diagnostic surface doctor owns, and "
        "because it is unblocked today. The choice is a judgement and is left "
        "legible so a human can move it again",
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
