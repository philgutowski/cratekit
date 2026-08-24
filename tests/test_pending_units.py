"""The meta-guard: a deferred guard cannot quietly become a permanent one.

U6 ports the safety net before the engine, so some ported guards name a module
that has not been written yet. Skipping those is correct. Skipping them
FOREVER is how a safety net acquires a hole that nobody can see, because a
skipped test is green in every summary anybody reads.

This file closes that. Three assertions, and each one blocks a different way the
hole opens:

1. **The declared set is exactly the intended set.** Adding a skip without
   recording it here fails the build. So "just skip it for now" is a visible
   decision in a diff rather than a one-line edit in a test file.
2. **Every pending target is genuinely still absent.** The moment a unit lands
   its module, this goes red. Nobody has to remember; forgetting is what fails.
3. **No test skips outside the registry.** A bare skip mark anywhere in the suite
   is rejected, so the registry cannot be routed around.

Together these make a skip a countdown rather than a hiding place.

WHAT MAKING IT GREEN ACTUALLY TAKES, because the obvious edit is the dangerous
one. A discharge is THREE edits in one commit: the entry in ``_pending.PENDING``,
the mirrored key in ``EXPECTED_PENDING`` below, and the ``@requires("<key>")``
decorator on every guard the key gated. Run
``grep -rn 'requires("<key>")' tests/`` before deleting anything, because a key
is usually cited from more than one file.

Deleting the entry alone does not arm a guard. ``requires()`` then raises
KeyError while the decorator is being evaluated, which happens at IMPORT and so
during COLLECTION, and the gated guard's whole file stops existing rather than
turning red. The asymmetry is why the wrong half is the likely one: skipping the
decorator edit breaks collection silently under a subset run, while skipping the
register edit only leaves this file red, which is completely visible.
``docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md``
carries the procedure and the U16 case where it cost 330 tests.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tests import _pending

TESTS_DIR = Path(__file__).resolve().parent

# The intended pending set, written out rather than derived. Duplicating the keys
# is the entire point: a change to the registry must be made in two places, and
# the second place is a test that a reviewer reads.
EXPECTED_PENDING = frozenset(
    {
        "path:skills",  # U28, the shipped operator skills
    }
)

# ``cratekit.session.restore_cli`` was here and is gone, because U27 landed both
# restore verbs and the one held session that spans them. The mirror in
# ``tests/_pending.PENDING`` went in the same commit, and ONE guard carried a
# ``@requires`` for this key,
# ``tests/test_restore.py::test_the_restore_verbs_hold_one_session_across_both_halves``.
# Its decorator came off in the same commit and it was then run on purpose, which
# is the third edit the header above says is the one people skip.

# ``cratekit.adopt.apply_cli`` was here and is gone, because U27 landed the shell
# and, with it, the one destructive session the residual titled "Adoption's tag
# write takes no destructive session and no library lock" asked for. The mirror in
# ``tests/_pending.PENDING`` went in the same commit, and no guard carried a
# ``@requires`` for the key, which was established by grep before the deletion
# rather than assumed.

# ``cratekit.cli.reports`` was here and is gone, because U27 landed the four
# report verbs, the coverage engine and the library-statistics engine. The mirror
# in ``tests/_pending.PENDING`` went in the same commit, and no guard carried a
# ``@requires`` for the key, which was established by grep before the deletion
# rather than assumed.

# ``cratekit.write.rebuild`` was here and is gone, because U36 landed it on `main`
# in this session and issue #36 closed. A register entry owed by a closed unit is
# the contradiction ``scripts/board.py audit`` exits 2 on, and it is owned by
# nobody. ``tests/_pending.py`` records which half of that entry U36's own suite
# discharged and which half became an always-armed tripwire in
# ``tests/test_restore.py``.

# U27 removed ``cratekit.cli.doctor`` when the health check landed. That UNGATED
# the two guards waiting on it, and ungating is not arming: as first written,
# neither of them could fail.
#
# The containment report in ``tests/test_config.py`` asked whether any finding
# contained both "db_path" and "atomic", and the OK branch of the very check
# under test says "library.db_path sits under library.root, so a snapshot commits
# atomically with a rename". ``atomic`` is inside ``atomically``, so a check that
# reported the CONTAINED answer unconditionally passed the guard against a
# database that is not contained.
#
# Conformance assertion 8 in ``tests/test_cli_contract.py`` ran the doctor and
# required every declared key to come back with an answer, which is identically
# the existence check it replaced: the keys are derived from the check table and
# every check returns its own key, so a stub emitting one empty finding per key
# passed while observing nothing.
#
# Both are behaviour now, and each is driven against the evasion that satisfied
# its first version as well as against correct code. The lesson is the one this
# file already teaches from the other side: deleting an entry from the register
# is the moment to read the guard it releases, because until that moment nothing
# has ever run it.
#
# U8's two entries were removed here when ``cratekit.core.snapshot`` and
# ``cratekit.core.session`` landed, which is the countdown working as designed.
# ``cratekit.core.session`` appeared TWICE in the literal above. A set makes a
# duplicate harmless, so nothing failed, and it is the same shape as the
# duplicate-key defect this repository has already shipped once with the whole
# suite green: every test over a mapping or a set iterates the RUNTIME object and
# is blind to an entry that was collapsed at parse time. The test below counts
# the literal's elements against the runtime length, which is the only check that
# can see it.


def test_the_intended_pending_set_has_no_duplicate_element():
    """A duplicate in the literal is silent, and silence is the whole problem.

    ``EXPECTED_PENDING`` exists to be READ in a diff, so an entry written twice
    means a reviewer sees one deletion and believes the countdown is finished
    while the second occurrence is still there. It collapsed harmlessly here
    because a set deduplicates; the same shape in the reason registry did not.
    """
    import ast
    import inspect

    literal = None
    for node in ast.walk(ast.parse(inspect.getsource(__import__(__name__, fromlist=["x"])))):
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == "EXPECTED_PENDING":
            literal = node.value

    assert literal is not None, "EXPECTED_PENDING is no longer a module-level assignment"
    # ``frozenset({...})``: the set is the call's first argument.
    elements = literal.args[0].elts if isinstance(literal, ast.Call) else literal.elts
    written = [element.value for element in elements]
    duplicates = sorted({key for key in written if written.count(key) > 1})
    assert not duplicates, f"written twice and collapsed at parse time: {duplicates}"
    assert len(written) == len(EXPECTED_PENDING)

# Guards that are repository-wide and work against the tree as it stands today.
# None of these may EVER be gated on a pending unit: they are what makes the
# units between here and U37 safe to write.
ALWAYS_ARMED_MODULES = (
    "test_portability.py",  # R1 literals and the repository-wide secret scan
    "test_layering.py",  # KTD23 import direction, R19 stable identifiers
    "test_packaging.py",  # R5 slim core, KTD19 interpreter bounds
)


def test_the_declared_pending_set_is_exactly_the_intended_set():
    declared = frozenset(_pending.PENDING)
    assert declared == EXPECTED_PENDING, (
        f"undeclared skips added: {sorted(declared - EXPECTED_PENDING)}; "
        f"stale entries to remove: {sorted(EXPECTED_PENDING - declared)}. "
        f"Every deferred guard is a decision, and it belongs in a diff."
    )


@pytest.mark.parametrize("key", sorted(EXPECTED_PENDING))
def test_a_pending_target_that_has_landed_must_be_removed_from_the_registry(key):
    """The countdown. This test is DESIGNED to fail when a unit lands.

    When it does, the fix is THREE edits in one commit, not one: the entry in
    ``_pending.PENDING``, the mirrored key in ``EXPECTED_PENDING`` above, and the
    ``@requires`` decorator on every guard the key gated. Only the third arms
    anything. The first two on their own take the gated guard's whole file out of
    COLLECTION, because ``requires()`` raises KeyError while the decorator is
    evaluated at import. Run the grep in the message below before deleting.

    The behaviour this buys is still the one we want: the person who lands the
    module cannot ship it without the guards that govern it turning on.
    """
    unit, what = _pending.PENDING[key]
    assert _pending._is_absent(key), (
        f"{key} now exists, so {unit} has landed. DISCHARGE IS THREE EDITS IN "
        f"ONE COMMIT AND THE FIRST TWO ALONE BREAK COLLECTION. One, remove "
        f"{key!r} from _pending.PENDING. Two, remove it from EXPECTED_PENDING in "
        f"this file. Three, remove the @requires({key!r}) decorator from EVERY "
        f"guard it gated, which is what actually arms them: run "
        f"`grep -rn 'requires(\"{key}\")' tests/` FIRST and act on every hit, "
        f"because a key is usually cited from more than one file. Doing one and "
        f"two without three makes requires() raise KeyError at import, so those "
        f"files fail to COLLECT and their tests stop existing rather than "
        f"failing. The armed guard asserts {what}, and it must now pass: run it "
        f"on purpose, because it has never executed once."
    )


def test_every_pending_entry_names_a_unit_and_what_it_guards():
    """A skip reason that does not say what unlocks it is a mystery, not a note."""
    for key, value in _pending.PENDING.items():
        unit, what = value
        assert unit.startswith("U") and unit[1:].isdigit(), (
            f"{key}: {unit!r} is not a unit identifier"
        )
        assert len(what) > 20, f"{key}: the description of what is guarded is too thin"


def _skip_marks_outside_the_registry(source: str) -> list[str]:
    """Return every skip construct that does not route through ``_pending``.

    Both decorator forms and the imperative ``pytest.skip(...)`` call are
    detected, because either one silently removes a guard.
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr in {"skip", "skipif"}:
            # pytest.mark.skip / pytest.mark.skipif
            value = node.value
            if (
                isinstance(value, ast.Attribute)
                and value.attr == "mark"
                and isinstance(value.value, ast.Name)
                and value.value.id == "pytest"
            ):
                found.append(f"pytest.mark.{node.attr}")
        if isinstance(node, ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "skip"
                and isinstance(func.value, ast.Name)
                and func.value.id == "pytest"
            ):
                found.append("pytest.skip()")
    return found


def test_no_test_skips_outside_the_registry():
    """The registry cannot be routed around.

    ``_pending.py`` is the one file allowed to construct a skip, since that is
    where the accounting lives. Anywhere else, a skip is a guard being switched
    off with no record of when it switches back on.
    """
    offenders: dict[str, list[str]] = {}
    for path in sorted(TESTS_DIR.rglob("*.py")):
        if path.name == "_pending.py" or path.name == Path(__file__).name:
            continue
        found = _skip_marks_outside_the_registry(path.read_text())
        if found:
            offenders[path.name] = found
    assert not offenders, (
        f"skips constructed outside tests/_pending.py: {offenders}. Route them "
        f"through _pending.requires(...) so they are counted and expire."
    )


@pytest.mark.parametrize("module", ALWAYS_ARMED_MODULES)
def test_repository_wide_guards_are_never_gated_on_a_pending_unit(module):
    """The guards that must work TODAY are asserted to have no gate at all.

    Portability, the secret scan, the layering rules, and the packaging rules all
    run against the tree as it stands. If one of them ever acquired a pending
    gate, every unit between here and U37 would be written without it, which is
    the exact failure U6 exists to prevent.
    """
    source = (TESTS_DIR / module).read_text()
    assert "_pending" not in source, (
        f"{module} is a repository-wide guard and must never be gated on a "
        f"pending unit; it has to bite from the moment it lands"
    )
