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
    "cratekit.core.restore": (
        "U32",
        "that a restore replaces exactly the derived coupled set, and that it "
        "keeps the source system's sidecar asymmetry: clear both live sidecars "
        "first, write back the -wal, never the -shm. THREE MORE OBLIGATIONS "
        "arrive with U8's destructive-session gates and are registered here "
        "because U32 owns the verb that spends them (P5). One: the verb holds "
        "ONE session across the plan and the run, passing its own open guard in "
        "as backup.plan_restore's and backup.run_restore's `gates`, because the "
        "default shape takes the lock twice and a second process can commit in "
        "the window between them, leaving the run to copy a snapshot over a "
        "commit its plan was built before. Two: the verb RESOLVES the session "
        "record after a successful restore, through "
        "session.resolve_unverified_session, because the session log is declared "
        "SURVIVES_ROLLBACK and the committed-unverified record therefore outlives "
        "the restore that answers it. Three: bare-metal recovery, where the "
        "library volume itself is gone, needs a path of its own; every gate U8 "
        "publishes is library-scoped by KTD21, so the lock, the acknowledgment "
        "and the log all sit on the disk that just died. Today that case refuses "
        "honestly with mount-library-volume, and refusing honestly is not the "
        "same as serving it",
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
