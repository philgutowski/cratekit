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
    "cratekit.core.tombstone": (
        "U24",
        "that cratekit.acquire.match's replicated copy of the tombstone identity "
        "and the domain module's original agree, over a table of inputs chosen "
        "for what a normalization change actually bites on rather than for "
        "readability: the store key, the kind, the fold, and the identity a raw "
        "row title produces. Two copies of one algorithm exist while U24 is in "
        "flight, because the identity is addressed by both a deletion pass and "
        "an acquisition pass and neither may import the other. A drift between "
        "them is silent from both sides: a tombstone recorded under one spelling "
        "is invisible to the other, the version reports missing, acquisition "
        "fetches it back, and a deletion somebody made on purpose is undone with "
        "the whole suite green. This is the ONE guard that can compare them, and "
        "it can only run once the domain module exists in the same tree, which "
        "is the moment this entry is deleted",
    ),
    # U16 APPENDED A SECOND OBLIGATION HERE AND IT HAS BEEN REMOVED, which is
    # worth a note because removing an obligation is normally the wrong move.
    # It said a tombstone must be recorded under cratekit.acquire.match's kind
    # and identity. Two things were wrong with it. It was FALSE ABOUT ITS OWN
    # GUARD: this file's header defines the second element as one line saying
    # what THE GUARD asserts, and the guard that arms on this key asserts store
    # construction, record, revoke, the deletion queue and no CSV writer, and
    # says nothing about a kind or an identity. And it pointed at the wrong
    # module: the identity belongs below both the pass that records it and the
    # pass that consults it, which is where U24 puts it as
    # cratekit.core.tombstone, so an obligation aimed at this unit to match a
    # feature module's spelling had the dependency backwards. What replaces it is
    # a guard that is armed today rather than a countdown:
    # test_the_tombstone_identity_is_u24s_algorithm_byte_for_byte pins the exact
    # identifier, so the two copies cannot drift while both exist.
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
