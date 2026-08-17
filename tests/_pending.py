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
   still absent. The moment a unit lands its module, that meta-test goes red.

That third point is the whole design. Without it, a skip added for a good reason
in August is still silently skipping in December, and the safety net has a hole
nobody can see. With it, a skip is a countdown, not a hiding place.

DISCHARGING AN ENTRY IS THREE EDITS IN ONE COMMIT, AND MAKING ONLY THE FIRST IS
WORSE THAN MAKING NONE. Deleting the entry does not arm anything by itself:

1. Delete the entry from PENDING below.
2. Delete the matching key from EXPECTED_PENDING in tests/test_pending_units.py,
   which duplicates every key on purpose.
3. Remove the @requires("<key>") decorator from EVERY guard the key gated, so
   those guards run unconditionally.

Find the decorator sites BEFORE deleting anything, because a key is usually
cited from more than one file and a grep that stops at the first hit is how the
second file loses its collection:

    grep -rn 'requires("<key>")' tests/

Some entries are cited by no decorator at all, and for those step 3 is empty.
The grep is what tells the two cases apart, which is why it runs first.

A decorator expression is evaluated when its module is IMPORTED, and pytest
imports a test module in order to collect it. So an entry deleted while a
decorator still names it is not one red test. requires() raises KeyError during
collection and the guard's whole FILE stops existing. On the U16 merge that was
330 tests. Then run the newly armed guard on purpose and read its result,
because it has never executed once, and reconcile the collected count by
identifier rather than by total. The full procedure and the worked case are in
docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md
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
    "path:skills": (
        "U28",
        "the shipped operator skills the skills lint runs over",
    ),
    # APPENDED RATHER THAN FILED BESIDE A SIBLING, deliberately, for the reason
    # the verb registry gives for the same choice: two entries inserted into the
    # middle of one mapping by two units auto-merge, and an append conflicts
    # textually, which is a conflict somebody reads.
    "cratekit.analysis": (
        "U25",
        "six things about every module in the analysis package, listed rather "
        "than summarized because the first version of this entry summarized and "
        "the summary claimed more than the guard checked. The package must plan "
        "through cratekit.core.pool.plan_pool and run through "
        "cratekit.core.pool.map_workers; no module there may build a process "
        "pool of its own in any import shape; no module there may build a "
        "PoolPlan of its own in any import shape; no map_workers call may be "
        "given a plan the module fabricated; and no module there may read a core "
        "count at any of the four spellings the sizing module itself is held to. "
        "Together that is R23 turned from a claim about a module into a claim "
        "about a run. U12 ships the sizing and nothing that uses it, so until the "
        "heavy passes land there is no pool in this product to exhaust anything. "
        "The source system derives BOTH of its pool widths from the core count, "
        "and a port that carries that arithmetic across reproduces the "
        "nine-worker kill with every arithmetic test U12 wrote still green. "
        "Registered here rather than left in a docstring because the "
        "repository-wide guards U12 arms cover the shipped tree and this package "
        "does not exist yet (P5). WHAT THE EARLIER ENTRY GOT WRONG, kept legible "
        "because it is the reason the list above is a list: it claimed the pools "
        "were sized here and by nothing else, while the guard checked only that "
        "SOME module called the planner and SOME module called the runner. A "
        "package whose light pass was sized correctly and whose vocal pass handed "
        "the same runner a hand-built plan of nine workers passed it",
    ),
    # cratekit.write.routing_cli LANDED WITH U20. The four route.* verbs close
    # through routing_pass.close_run, and a re-run after a destination rename
    # converges by reading U36's DestinationNode map.
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
    # cratekit.cli.rebuild LANDED WITH U20. The actor is typed. The flag is
    # cleared only through rebuild_tree.
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
    "cratekit.adopt.apply_cli": (
        "U27",
        "the command-line surface for adopt.apply, and with it the destructive "
        "session and the library lock that apply_plan honestly says it does not "
        "take (the residual titled 'adoption's tag write takes no destructive "
        "session and no library lock'). R29 says one source per run, and the "
        "loop is not "
        "a run, so only the verb can open that session. REGISTERED HERE RATHER "
        "THAN LEFT AS A planned_in MARKER because scripts/board.py reads this "
        "file and nothing else, so an obligation carried only by a marker on a "
        "closing unit is owned by nobody the moment that unit closes (P5). "
        "U23's own board entry does not appear in board.pending_units at all, "
        "so closing #23 produced no drift and no contradiction while two verbs "
        "shipped with no conformance coverage; that is R-13's failure verbatim "
        "and it is already live for U8, U15 and U35. "
        "ONLY adopt.apply IS BEHIND THE WALL. adopt.scan shared this verb's "
        "module string, declares no gate, writes nothing and is not destructive, "
        "so conformance 3 is an empty loop for it. It has landed as "
        "cratekit.adopt.scan_cli. "
        "WHAT THE WALL ACTUALLY IS, because R-13 states a close condition that "
        "will not close it. It is NOT the absence of a database, and that is "
        "proven by elimination: removing explicit=True from both of "
        "adopt.apply's gates still exits 10. It is two properties of "
        "test_conformance_3 itself. ONE: it answers gates inline with -d, and "
        "Gates.require correctly refuses an inline answer to an explicit=True "
        "gate, which is R34 working rather than failing, so any verb with an "
        "explicit gate cannot pass. TWO: it drives once per gate on a fresh run "
        "answering only that gate, so a verb declaring TWO gates always exits "
        "DECISION_REQUIRED on the other one. adopt.apply has both shapes at "
        "once. THE OWNER IS U27 on the reasoning that it lands doctor, it is "
        "the unit that makes a machine ready, and R-13 already names it as the "
        "natural owner of the conformance-3 correction. The correction is in "
        "flight on its own branch, so this entry may be spendable before U27 "
        "reaches it; a human moving it should move ADOPT_APPLY_CLI_UNIT in "
        "cratekit/cli/registry.py with it",
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
            f"{key!r} is not declared in _pending.PENDING. THIS MESSAGE HAS TWO "
            f"REMEDIES AND THEY POINT OPPOSITE WAYS, so read which case you are "
            f"in first. If you are ADDING a gated guard, add {key!r} to PENDING "
            f"and to EXPECTED_PENDING with the unit that lands it, so "
            f"tests/test_pending_units.py can hold it accountable, or the skip "
            f"becomes permanent by accident. If you are DISCHARGING because the "
            f"module has landed, the key is leaving rather than arriving and "
            f"adding it back is exactly backwards: you have deleted the entry "
            f"while a guard still carries @requires({key!r}), and this file is "
            f"failing to COLLECT rather than failing a test. Delete that "
            f"decorator from every site "
            f"`grep -rn 'requires(\"{key}\")' tests/` reports."
        )
    unit, what = PENDING[key]
    return pytest.mark.skipif(
        _is_absent(key),
        reason=f"{key} lands in {unit}; this guard asserts {what}",
    )
