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
import re
from pathlib import Path

import pytest

from tests import _pending

TESTS_DIR = Path(__file__).resolve().parent

# The intended pending set, written out rather than derived. Duplicating the keys
# is the entire point: a change to the registry must be made in two places, and
# the second place is a test that a reviewer reads.
# EMPTY, AND WRITTEN AS ``frozenset()`` RATHER THAN ``frozenset({})``. The second
# spelling is an empty DICT inside a frozenset call, which is still an empty
# frozenset at run time and is a different node to anything that parses this file.
# The duplicate guard below reads the literal through the AST and asked a set
# literal for its elements, so the braces form crashed it with an attribute error
# the moment the last key came out. Found by discharging the last entry.
EXPECTED_PENDING: frozenset[str] = frozenset()

# ``path:skills`` was here and is gone, because U28 landed the twelve shipped
# skills and the verb that installs them. The mirror in ``tests/_pending.PENDING``
# went in the same commit, and ONE guard carried a ``@requires`` for the key,
# ``tests/test_skills_lint.py::test_real_skills_pass_lint``, whose decorator came
# off in the same commit and which was then run on purpose.
#
# THE REGISTER IS NOW EMPTY. That is a first for this file and it is a real state
# rather than a broken one: every countdown this build opened has been discharged.
# ``EXPECTED_PENDING`` being empty still asserts something, namely that nobody has
# added a skip without declaring it, which is the whole point of the duplication.

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
        # BOTH ASSIGNMENT NODES, which the sibling guard over ``cause.REASONS``
        # in tests/test_cli_contract.py has always done and this one had not.
        # Annotating the register as ``frozenset[str]`` turns an ``Assign`` into
        # an ``AnnAssign`` and this walk stopped finding it, reporting the
        # register as no longer module level when it had simply gained a type.
        if isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == "EXPECTED_PENDING":
            literal = node.value

    assert literal is not None, "EXPECTED_PENDING is no longer a module-level assignment"
    # ``frozenset({...})``: the set is the call's first argument. ``frozenset()``
    # with no argument is the EMPTY register, which is the state this file reached
    # when U28 discharged the last countdown, and it has no elements to read
    # rather than being a failure to read them.
    if isinstance(literal, ast.Call):
        elements = literal.args[0].elts if literal.args else []
    else:
        elements = literal.elts
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


def test_the_empty_register_is_a_discharged_register_and_not_a_lost_one():
    """An empty register is reported OUT LOUD rather than as a mystery skip.

    ``pytest`` skips a parametrized test whose parameter set is empty, so the
    countdown below became a silent skip the moment U28 discharged the last
    entry. That is structurally correct, and it is also the exact shape this
    file's own header warns about: a skip that is fine in August and is still
    skipping in December with nobody able to see why. This test cannot be skipped
    and states the condition, so ``pytest -rs`` reads as "the register is empty"
    rather than as "something got skipped here".

    IT ALSO ASSERTS THE TWO REGISTERS AGREE while both are empty, which the
    comparison above does vacuously in that state.
    """
    assert _pending.PENDING == {}, (
        f"the register is not empty, so the countdown below is parametrized and "
        f"this test is stale: {sorted(_pending.PENDING)}"
    )
    assert EXPECTED_PENDING == frozenset()


@pytest.mark.parametrize("key", sorted(EXPECTED_PENDING))
def test_a_pending_target_that_has_landed_must_be_removed_from_the_registry(key):
    """The countdown. This test is DESIGNED to fail when a unit lands.

    IT IS CURRENTLY PARAMETRIZED OVER NOTHING, because U28 discharged the last
    entry, so pytest skips it. The test above is what says so in a run summary.
    Re-opening any countdown re-arms this one with no edit here.

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


# ═══════════════════════════════════════════════════════════════════════════
# The register's own spelling, and the trailer that would close it
#
# The countdown above proves an entry EXPIRES. It cannot prove the entry names
# something that could ever exist. A key naming a module no unit will ever build
# is absent forever, so `_is_absent` is permanently True, the countdown never
# fires, and the day the unit closes `board.py contradictions()` returns exit 2
# for the rest of the project's life, which `sync` deliberately will not repair.
# ═══════════════════════════════════════════════════════════════════════════


def _board():
    """Load `scripts/board.py` as a module, without putting scripts on the path.

    It imports nothing but the standard library at module level and does no work
    on import, so loading it is cheap and side-effect free. Loaded by path rather
    than installed because it is a script, not part of the distribution, and
    making it importable by name would be shipping it.
    """
    import importlib.util

    path = TESTS_DIR.parent / "scripts" / "board.py"
    spec = importlib.util.spec_from_file_location("board_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _registry_modules() -> set[str]:
    from cratekit.cli import registry

    return {entry.module for entry in registry.entries()}


#: Register keys that look like a command-line module and legitimately are not
#: one, with the reason. EMPTY, and it should stay that way: a key ending in
#: `.cli` that no verb declares is a key nothing can ever satisfy.
CLI_SHAPED_EXEMPTIONS: dict[str, str] = {}


def test_a_cli_shaped_register_key_names_a_module_some_verb_declares():
    """RULE A. A verb module in the register must be one the registry asks for.

    The register holds two kinds of key and they are not interchangeable. Most
    name an engine or a package: `cratekit.core.review`, `cratekit.modules.reports`,
    `cratekit.adopt`. Those are owed by a unit and nothing else has an opinion
    about their spelling. A key that ends in `.cli` or `_cli` is different,
    because it names a command-line surface, and the registry is where command
    line surfaces are declared. Two records of one fact that nothing compares are
    two records that drift.

    The drift is not theoretical and it is not cheap. A register key naming a
    module the registry never asks for cannot be satisfied by anybody: the module
    is absent forever, so the countdown never fires, and the moment the unit
    closes the board holds a contradiction that `sync` refuses to repair by
    design, because repairing it would mean choosing which record to overwrite.

    A key that is genuinely not a verb module goes in the exemption map WITH a
    reason, rather than the rule being narrowed until it stops firing.

    WHAT THIS DOES NOT REACH, said plainly, because a rule whose scope is
    implied gets trusted past it. It is a spelling check on ONE THIRD of the
    surface: register keys that look like verb modules. A non-CLI typo has
    identical consequences and is invisible here, `cratekit.core.restor` planted
    for U32 being the obvious one, and a misspelling on the REGISTRY side is
    structurally beyond it, since the registry is the thing being compared
    against. Rule B is what catches both of those, at the moment the unit closes,
    which is why the two ship together rather than either one alone.
    """
    registry_modules = _registry_modules()
    unclaimed = sorted(
        key
        for key in _pending.PENDING
        if (key.endswith(".cli") or key.endswith("_cli"))
        and key not in registry_modules
        and key not in CLI_SHAPED_EXEMPTIONS
    )
    assert not unclaimed, (
        f"register keys naming a command-line module no verb declares: "
        f"{unclaimed}. Nothing can ever land these as spelled, so the countdown "
        f"cannot fire and the unit's close becomes a permanent contradiction. "
        f"Fix the spelling, point it at the module the registry actually asks "
        f"for, or exempt it here with a reason."
    )


#: The one place the two registers disagree about a unit's own package name, and
#: it is a live defect rather than a style. Written as EXACT membership rather
#: than as an allowance, so U23 resolving it turns this red and forces the
#: deletion, exactly like the pending countdown above.
#:
#: EMPTY AT THE U59 MERGE, BECAUSE THE COUNTDOWN FIRED AND THIS IS THE DELETION
#: IT ASKED FOR. The entry read `("U23", "cratekit.adopt", "cratekit.adoption")`,
#: the register saying one package name and the registry saying another, recorded
#: rather than picked because only U23 knew which was wrong. U23 answered:
#: `src/cratekit/adopt/` is the package that shipped, `cratekit.adoption` is
#: spelled nowhere in the registry any more, and `_pending.PENDING` is empty, so
#: neither side still disagrees with the other. Deleting the entry is exactly
#: what the exact-membership shape above was built to force, and leaving it would
#: have been a permanent red light over a defect that no longer exists.
KNOWN_PACKAGE_NAME_DISAGREEMENTS: set[tuple[str, str, str]] = set()


def test_no_unit_declares_two_confusingly_similar_package_roots():
    """A NAME SIMILARITY HEURISTIC, and it is named as one because that is what it is.

    NEAR-MISS RATHER THAN DIFFERENCE, deliberately. A unit owning modules in two
    unrelated packages is ordinary and correct: U32 owes an engine in
    `cratekit.core` and a command-line surface in `cratekit.session`, and U34 owes
    `cratekit.modules` and `cratekit.reports`. Flagging those would be a guard
    firing on correct code, which is how a guard gets switched off.

    THE TEST IS `str.startswith`, NOT A DOTTED-SEGMENT TEST, and that is a real
    limitation rather than an oversight. The segment-aware form,
    `longer.startswith(shorter + ".")`, is the one that is always true, and it
    would stop catching the case this exists for: `cratekit.adoption` is not a
    package UNDER `cratekit.adopt`, it is a different word that starts the same
    way. So this is a heuristic on spelling, and it can be wrong. `cratekit.tag`
    beside `cratekit.tagging` would fire, and `cratekit.tagging` is already a real
    planned root for U37.

    WHAT MAKES THAT ACCEPTABLE is the second condition, which the shape depends
    on: both roots must be declared by the SAME UNIT. One unit owing both `tag`
    and `tagging` is worth a human look whether or not it is a typo. And because
    membership is pinned exactly, a false positive is a red suite whose cheapest
    honest answer is to add the pair to the pin with a note, which is a recorded
    decision in a diff, not a widened allowance that kills the rule.
    """
    per_unit: dict[str, set[str]] = {}
    for key, (unit, _) in _pending.PENDING.items():
        if not key.startswith("path:"):
            per_unit.setdefault(unit, set()).add(".".join(key.split(".")[:2]))
    from cratekit.cli import registry

    for entry in registry.entries():
        if entry.planned_in:
            per_unit.setdefault(entry.planned_in, set()).add(
                ".".join(entry.module.split(".")[:2])
            )

    found = {
        (unit, shorter, longer)
        for unit, roots in per_unit.items()
        for shorter in roots
        for longer in roots
        if shorter != longer and longer.startswith(shorter)
    }
    assert found == KNOWN_PACKAGE_NAME_DISAGREEMENTS, (
        f"package-name disagreements are {sorted(found)}, and this file declares "
        f"{sorted(KNOWN_PACKAGE_NAME_DISAGREEMENTS)}. One unit, one package name. "
        f"A new one is a typo about to become a permanent contradiction; a "
        f"resolved one is an entry to delete from the set above."
    )


def test_the_module_probe_tells_the_two_kinds_of_missing_apart():
    """RULE A's other half: a countdown that cannot fire looks exactly like one that can.

    ``find_spec`` has two failure modes and they were both being read as absence.
    It returns None when a module is missing from a package that EXISTS, which is
    a countdown armed and waiting for a file. It RAISES when an ANCESTOR is
    missing, which cannot be interpreted from the tree at all: nothing here can
    tell "that package is coming" from "that name is misspelled".

    Recognizing the difference is not the same as forbidding the second, and this
    file does not forbid it. Seventeen planned verb modules are in that state and
    almost all of them belong to units that have not started, so an assertion
    against it would fire on correct pending work. What the distinction buys is
    that a probe result now carries which case it is, and that a
    ``ModuleNotFoundError`` raised from INSIDE an ancestor that does exist stops
    being swallowed as absence.
    """
    assert _pending.module_state("cratekit.cli.registry") == _pending.PRESENT
    assert _pending.module_state("cratekit.cli.no_such_module") == _pending.ABSENT
    assert _pending.module_state("cratekit.no_such_package.cli") == _pending.ANCESTOR_MISSING
    assert _pending.module_state("cratekit.no_such_package") == _pending.ABSENT, (
        "a missing top-level child of a package that exists is plain absence, "
        "not a missing ancestor"
    )


# ── Rule B: the trailer is refused before it closes anything ─────────────────


def test_the_registry_s_planned_markers_are_a_register_the_board_now_reads():
    """Two registers exist, and until now `contradictions()` read one of them.

    ``planned_in`` on a registry entry makes exactly the promise
    ``tests/_pending.py`` makes: this module does not exist and unit U-n lands it.
    Reading only the first is how three closed units kept live markers for seven
    verbs between them with nothing ever saying so, because ``board.py audit``
    audits units against a register that never mentioned those verbs.
    """
    board = _board()
    planned = board.planned_units()
    from cratekit.cli import registry

    expected: dict[int, set[str]] = {}
    for entry in registry.entries():
        if entry.planned_in:
            expected.setdefault(int(entry.planned_in[1:]), set()).add(entry.module)
    assert {uid: sorted(mods) for uid, mods in expected.items()} == planned, (
        "the ast reader and the imported registry disagree about what is planned, "
        "so the audit is judging a different tree from the one that ships"
    )

    merged = board.owed_by_unit()
    for uid, modules in board.pending_units().items():
        assert set(modules) <= set(merged[uid]), "the merge dropped a pending entry"
    for uid, modules in planned.items():
        assert set(modules) <= set(merged[uid]), "the merge dropped a planned marker"


def test_a_closing_trailer_is_refused_while_a_register_still_owes_that_unit():
    """RULE B. The same comparison `audit` makes, moved before the event.

    ``contradictions()`` can only speak about issues that are ALREADY CLOSED. By
    then the close has cascaded, dependent units have moved to ready, and `sync`
    will not repair it because repairing means choosing which record to
    overwrite. The trailer is the moment the close is decided and the last moment
    refusing costs nothing.

    Driven against a synthetic register rather than the live one, so this test
    says the same thing next year when every unit here has landed.
    """
    board = _board()
    owed = {36: ["cratekit.write.converge_cli"], 8: ["cratekit.session.cli"]}

    assert board.unresolved_closes("feat: a thing\n\nCloses #36\n", owed)
    assert board.unresolved_closes("closes #8", owed), "the trailer is not case sensitive"
    assert not board.unresolved_closes("feat: a thing\n\nCloses #21\n", owed), (
        "a unit no register owes anything closes cleanly, or the rule refuses "
        "every merge and gets removed"
    )
    assert not board.unresolved_closes("see #36 for the reasoning", owed), (
        "a reference is not a trailer, and refusing one would make it impossible "
        "to explain in a commit body why a unit is still open"
    )


#: Every spelling GitHub closes an issue on. WRITTEN OUT rather than generated
#: from the pattern, because a table generated from the thing it tests passes
#: whatever the thing does.
#:
#: An earlier version of this file asserted that `Fixes #36` does NOT close, and
#: justified it with "only the trailer this repository's contract uses closes an
#: issue". That is false about GitHub, and worse than false: it certified the
#: hole, so the next reader would have found the gap already considered and
#: settled. A test may not assert a limitation into a fact.
CLOSING_SPELLINGS_GITHUB_ACTS_ON = (
    "Fix #36",
    "Fixes #36",
    "Fixed #36",
    "Close #36",
    "Closes #36",
    "Closed #36",
    "Resolve #36",
    "Resolves #36",
    "Resolved #36",
    "Closes: #36",
    "Closes #36.",
    "Closes #36, #33",
    "This closes #36.",
    "feat: a thing\n\nCloses #36\n",
    # The other reference form that closes an issue HERE.
    "Closes GH-36",
    # A revert. It really does close the issue, and the refusal is the point: a
    # revert un-lands the module, so the register re-owes the unit exactly then.
    'Revert "feat(write): converge (closes #36)"',
)

#: Messages that close nothing this repository tracks, and must stay exit 0. A
#: check that refuses these is a check somebody removes on the first afternoon it
#: blocks a commit that was fine.
MESSAGES_THAT_CLOSE_NOTHING = (
    "Closes #21",
    "see #36",
    "Closes #52",
    "look at #36 for why U36 is still open",
    "feat: x\n\nbody\n# Please enter the commit message\n# Closes #36\n",
    "feat: x\n\nCloses #21\n# ------------------------ >8 ------------------------\n+Closes #36\n",
    # THE SENTENCE THIS CHECK ASKS PEOPLE TO WRITE. A trailer, a blank line, then
    # an explanation of what stays open. `\s*` in the continuation crossed the
    # newline and refused both issues, so the code contradicted the contract its
    # own docstring states.
    "feat(write): converge\n\nCloses #21\n\nand #36 stays open until the export CLI lands.\n",
    # A link with a fragment is not a closing reference.
    "see https://example.com/notes/fixes#36 for the reasoning",
    # CROSS-REPOSITORY references close an issue in the NAMED repository and
    # nothing here. Matching them refused commits over units they have no
    # relationship to, and this is the realistic trigger rather than a
    # hypothetical: this repository vendors pyrekordbox, the owed unit numbers
    # run from 8 to 38, and upstream numbers collide with them constantly.
    "fixes numpy/numpy#36",
    "fixes https://github.com/dylanljones/pyrekordbox/issues/36",
    "chore(vendor): bump pyrekordbox\n\nfixes dylanljones/pyrekordbox#36 upstream\n",
)


@pytest.mark.parametrize("message", CLOSING_SPELLINGS_GITHUB_ACTS_ON)
def test_every_spelling_github_closes_on_is_refused(message):
    """One spelling out of eleven is a check that reports clean on the other ten.

    Each of these closes issue 36 on GitHub and cascades every unit waiting on
    it. The first version of this check matched `^Closes #n$` anchored to a whole
    line, on the reasoning that the contract says to write that exact trailer.
    GitHub does not read the contract.

    The comma continuation is caught deliberately over-inclusively. Whether
    GitHub closes the second issue in a list has moved with its parser, but the
    person writing it means to close both, and the costs are not symmetric: a
    false refusal is one reworded line, a miss is a close that has already
    cascaded and that `sync` will not repair.
    """
    board = _board()
    owed = {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]}
    assert board.unresolved_closes(message, owed), (
        f"{message!r} closes an issue on GitHub and this check reported clean"
    )


@pytest.mark.parametrize("message", MESSAGES_THAT_CLOSE_NOTHING)
def test_a_message_that_closes_nothing_owed_is_left_alone(message):
    """The direction that decides whether a check survives contact.

    Two of these are the ones that would have made it unusable rather than merely
    wrong: git hands the commit-msg hook the RAW file, so the template comments
    are in it, and `commit --verbose` puts the entire diff below a scissors line.
    A keyword anywhere in either would refuse a commit that closes nothing.
    """
    board = _board()
    owed = {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]}
    assert not board.unresolved_closes(message, owed), (
        f"{message!r} closes nothing this register owes, and was refused anyway"
    )


def test_the_closing_check_is_wired_where_it_cannot_be_forgotten():
    """WHERE RULE B LIVES, and why it is not one place.

    It judges a commit MESSAGE, which exists for one moment before it becomes
    history, so the only thing that can see it as it is written is a commit-msg
    hook. That is the copy nobody has to remember. But R-1 is the finding that a
    hook is absent from a fresh clone until somebody installs it, so a hook alone
    is a guard that is off exactly where it has never been run.

    So it is also a subcommand anybody can run, and `audit` makes the same
    comparison against issues that are already closed. The check itself is
    network-free, which is the property that lets it live in a hook at all: the
    rest of `audit` needs `gh`, and a hook that fails without a token is a hook
    that gets uninstalled.
    """
    config = (TESTS_DIR.parent / ".pre-commit-config.yaml").read_text()
    assert "board.py closing --message-file" in config
    assert "stages: [commit-msg]" in config

    board = _board()
    source = (TESTS_DIR.parent / "scripts" / "board.py").read_text()
    call = source[source.index("def unresolved_closes") : source.index("def cmd_closing")]
    assert "gh(" not in call, (
        "the closing check reaches the network, so it cannot run in a hook on a "
        "machine with no token, which is every machine the first time"
    )
    assert callable(board.cmd_closing)


def test_the_ci_step_judges_the_commits_the_push_added():
    """The step judged an EMPTY range on every push, and said so in its own comment.

    It took the merge base with `origin/main`. This repository opens no pull
    requests and pushes only `main`, so after a push `origin/main` is `HEAD`, the
    merge base is `HEAD`, and the range holds nothing. The trailer lives in the
    merge commit the push delivers, which is exactly what the range excluded, so
    the copy CI calls load-bearing had judged nothing at all.

    Asserted against the workflow text because there is no other way to see it
    from here. The shape that matters is that the range starts at the ref's
    PREVIOUS TIP and not at a merge base with the branch being pushed.
    """
    workflow = (TESTS_DIR.parent / ".github" / "workflows" / "ci.yml").read_text()
    step = workflow[workflow.index("A unit may not close while a register") :]
    step = step[: step.index("\n  portable:")]
    assert "github.event.before" in step, (
        "the range must start at the ref's previous tip; a merge base against "
        "the branch being pushed is empty by construction"
    )
    assert "merge-base" not in step
    assert "board.py closing --since" in step


def test_a_closing_reference_is_never_manufactured_across_two_commit_messages(
    tmp_path, monkeypatch
):
    """The reader must not invent a trailer neither commit wrote.

    `git log --format=%B` runs messages together, and the keyword-to-reference
    gap spans newlines, so a commit whose subject ends with the word "closes"
    followed by a commit whose body opens with `#36` produced a closing reference
    that is in neither message. A false refusal a person wrote costs one reworded
    line. This one costs a rewrite of history, or the deletion of the check,
    because the commits are already final.

    Driven through `cmd_closing`, since the concatenation is the subcommand's and
    not the function's, and asserting on `unresolved_closes` would go on passing
    with the defect fully in place.
    """
    board = _board()
    repo = tmp_path / "fixture"
    run, base = _seeded_repo(repo)
    # OLDEST FIRST HERE, NEWEST FIRST IN THE LOG. `git log` reverses these, so
    # the message that must END with the keyword is the one committed LAST, and
    # the message that must OPEN with the reference is committed first. Getting
    # that backwards produces a fixture that manufactures nothing and a row that
    # passes while measuring an empty range.
    for index, message in enumerate(
        ("#36 is the tracker for this", "docs: explain what this closes")
    ):
        (repo / f"f{index}.txt").write_text(f"{index}\n")
        run("git", "add", f"f{index}.txt")
        run("git", "commit", "-q", "--no-verify", "-F", "-", message_text=message)

    concatenated = run("git", "log", "--format=%B", f"{base}..HEAD")
    assert board.closing_references(concatenated, raw=False) == [36], (
        "this test's premise is that concatenation manufactures the match; it no "
        "longer does, so the row is measuring nothing"
    )

    monkeypatch.setattr(
        board, "owed_by_unit", lambda: {36: ["cratekit.write.converge_cli"]}
    )
    monkeypatch.chdir(repo)
    assert board.cmd_closing(_ClosingArgs(since=base)) == 0, (
        "a trailer neither commit wrote was refused"
    )


def test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ():
    """A trailer names an ISSUE. Both registers name a UNIT. They are not the same.

    U38 is issue #51, and U39 through U61 are issues #57 through #79. Reading the
    reference as a unit number is wrong in both directions: it misses the unit
    that is actually owed and refuses over a unit that is not. Twenty four units
    were mismatched on 2026-09-10, none of them owed a module that day, which is
    why nothing had surfaced it.
    """
    board = _board()
    owed = {38: ["cratekit.write.some_cli"]}
    units = {51: 38, 38: 26}

    resolved = board.unresolved_closes("Closes #51", owed, units=units)
    assert resolved, "closing U38's real issue must be refused while U38 is owed"
    assert "U38" in resolved[0]

    assert not board.unresolved_closes("Closes #38", owed, units=units), (
        "#38 is U26's issue here, and refusing it names a unit the message has "
        "no relationship to"
    )


def test_the_network_free_path_says_that_it_guessed_the_unit_number():
    """The guess is stated rather than worn as a fact.

    Without the board the mapping cannot be resolved, so the reference is read as
    a unit number. That is right for most units here and not for all, and a
    refusal that does not say so is a sentence the reader has no reason to doubt.
    """
    board = _board()
    refusals = board.unresolved_closes("Closes #38", {38: ["cratekit.write.some_cli"]})
    assert refusals
    assert "without consulting the board" in refusals[0]

    quiet = board.unresolved_closes(
        "Closes #38", {38: ["cratekit.write.some_cli"]}, units={38: 38}
    )
    assert quiet and "without consulting the board" not in quiet[0], (
        "a resolved mapping is not a guess and must not carry the caveat"
    )


def test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate():
    """The mapping exists only on GitHub, so it is derived from what the graph has.

    A duplicate unit number is a board editing mistake, and letting the later
    issue win would answer confidently about the wrong one. Dropped instead, so
    the contradiction check simply says nothing about that unit rather than
    saying something false.

    THE UNIT LABEL IS PART OF THE ANSWER, AND ITS ABSENCE IS ASSERTED HERE. A
    unit-shaped TITLE on an issue that carries no `unit` label is not a unit, and
    excluding it is what makes the label test inside `contradictions` redundant
    rather than load bearing. That redundancy was measured as a zero death row in
    `docs/mutation/u81.md`, and this is the assertion that turns the zero into an
    answer: the term cannot fire because nothing this function returns can name a
    non-unit issue.
    """
    board = _board()
    graph = {
        51: {"number": 51, "title": "U38: something", "unit": True},
        77: {"number": 77, "title": "U59: something else", "unit": True},
        90: {"number": 90, "title": "not a unit at all", "unit": False},
        91: {"number": 91, "title": "U59: a duplicate claim", "unit": True},
        92: {"number": 92, "title": "U40: a unit-shaped title, unlabelled", "unit": False},
    }
    assert board.units_by_issue_number(graph) == {38: 51}, (
        "U59 is claimed by two issues and must be dropped rather than resolved "
        "to whichever was seen last, and #92 names a unit in its title without "
        "carrying the label, so it is not one"
    )


def test_the_two_message_paths_are_cleaned_differently_because_they_have_to_be():
    """`raw` says which side of git's cleanup this text is on, and it is not symmetric.

    A message file handed to the commit-msg hook is PRE-cleanup and carries git's
    comments and, under `commit --verbose`, the whole diff. Those come out.

    `git log --format=%B` is POST-cleanup and final. It has no comments and no
    scissors block, so stripping there prevents no false refusal and can only
    delete a REAL trailer. Both shapes below were verified through the CLI: a
    body line beginning with `#` survives git's `whitespace` cleanup, which is
    what `-m` and `-F` use, and a scissors-shaped line typed by a person is
    removed as a comment while everything below it stays. Stripping was applied
    to the CI path, which this repository calls its load-bearing wiring, so it
    was doing its only possible harm exactly where it mattered most.
    """
    board = _board()
    owed = {36: ["m"], 33: ["n"]}

    on_a_hash_line = "docs: note\n\n#36 fixes #33 in passing"
    assert board.unresolved_closes(on_a_hash_line, owed, raw=False), (
        "git keeps a #-leading body line under whitespace cleanup, so this "
        "closes 33 and the CI path must see it"
    )

    typed_scissors = "docs: note\n#-- >8 --\nCloses #36\n"
    assert board.unresolved_closes(typed_scissors, owed, raw=False)
    assert board.unresolved_closes(typed_scissors, owed, raw=True), (
        "only git's OWN scissors line cuts a message; a shape that resembles one "
        "is removed as a comment and what follows reaches history"
    )

    real_scissors = (
        "docs: note\n"
        "# ------------------------ >8 ------------------------\n"
        "Closes #36\n"
    )
    assert not board.unresolved_closes(real_scissors, owed, raw=True), (
        "git cuts everything below its own scissors line, so nothing there can "
        "close anything"
    )

    assert board.unresolved_closes("docs: x\r\n\r\nCloses #36\r\n", owed, raw=True), (
        "CRLF was already handled and must not regress"
    )


def test_a_refusal_names_what_the_package_actually_contains():
    """The diagnosis, put where the refusal is read.

    A register key can name a module nobody will build, and the loudest symptom
    is a permanent exit 2 saying only that a module is owed. `cratekit.write.rebuild`
    absent while `cratekit.write.tree_rebuild` exists is a one-word difference
    invisible in that message.

    This is deliberately a NOTE rather than an assertion. A rule that asserted
    the mismatch was measured and rejected: it is a substring heuristic, and
    `cratekit.core.restore` is U32's live key today, so it would have gone red
    against a unit that did nothing wrong. And the failure was never silent to
    begin with, because a register entry keeps its unit owed for as long as the
    entry sits in the file, so Rule B refuses in either merge order. All the note
    does is move the diagnosis earlier, which is worth nothing if it costs a
    false positive and worth having if it costs none.

    RE-AIMED AT THE U59 MERGE, AND THE OLD SHAPE IS WORTH NAMING. It owed
    `cratekit.write.rebuild` and WROTE `src/cratekit/write/tree_rebuild.py` into
    the real package to play the sibling. Both halves expired: U36 landed
    `rebuild.py`, so the owed module now exists and `_near_misses` correctly
    short-circuits before it ever looks for a sibling, and the test went red
    holding a green rule. It is re-aimed rather than patched, because a test that
    creates a file inside `src/` to make its own premise true is one interrupted
    run away from leaving that file behind, and the merged tree supplies the
    same shape for free: `cratekit.write.routing` is genuinely absent and
    `routing_cli` and `routing_pass` are genuinely beside it. Nothing is written
    anywhere now, and the measurement is taken on the tree rather than on a
    fixture authored alongside it.
    """
    board = _board()
    refusals = board.unresolved_closes(
        "Closes #32", {32: ["cratekit.write.routing", "cratekit.core.restore"]}
    )

    assert len(refusals) == 1
    assert "routing_pass" in refusals[0], (
        "the refusal must name the sibling that exists, or the reader is left to "
        "guess why a module is owed that nobody is going to write"
    )
    assert "cratekit.core.restore" not in refusals[0].split("note:", 1)[1], (
        "U32's live key has no near miss in its package and must not acquire a "
        "note; a note on a correct key is the false positive the rejected rule "
        "would have asserted"
    )


def test_a_near_miss_note_is_skipped_once_the_owed_module_actually_lands():
    """The short-circuit, driven, because it is what expired the test above.

    `_near_misses` returns nothing for a module that EXISTS, which is right: a
    landed module needs no diagnosis. It is asserted here rather than left
    implicit, because the previous version of the test above depended on this
    branch never being taken and gave no signal when it started being taken.
    `cratekit.write.rebuild` is the exact module whose landing caused that.
    """
    board = _board()
    assert board._near_misses(["cratekit.write.rebuild"]) == [], (
        "a module that has landed must acquire no note; U36 shipped "
        "src/cratekit/write/rebuild.py and a note there would be a diagnosis of "
        "a problem that no longer exists"
    )


# ── Rule B's other half: the audit side, over a graph ────────────────────────
#
# `unresolved_closes` above is the check moved BEFORE the close. `contradictions`
# is the same comparison AFTER it, and it is the whole of what makes `board.py
# audit` exit 2. R-322 recorded that no test in this suite executed it, and it
# recorded that as a MEASUREMENT rather than an observation: U59 reverted the
# unit-to-issue indexing and killed zero, then paired that zero with a composite
# deleting the closure test entirely, which killed zero as well. Two zeros over
# one function is not a redundant guard, it is a function with no driver.
#
# WHERE THE DOUBLE SITS IS THE WHOLE DECISION, and R-322 asks for it out loud.
# `contradictions` takes the graph, and the graph comes from `gh`, so something
# has to be hand built. A hand-built GRAPH is the wrong answer: every derived key
# on a node, `closed`, `unit`, `open_deps`, `reach`, `unblocks`, would then be
# typed beside the test rather than produced by the code, which is METHOD's
# fourth defect pattern exactly, a measurement taken on a fixture authored
# alongside the thing it justifies. Add a key to `build_graph` and a typed graph
# goes on passing while the real one has moved.
#
# So the double is the PAYLOAD, the list of issue dicts `gh issue list --json`
# returns, and `build_graph` runs on it for real. That puts the fixture at the one
# boundary a test here genuinely cannot cross and leaves everything downstream of
# it under measurement. The payload can still drift from what `load_issues` asks
# for, and that is the one direction this shape does not close by construction,
# so it is closed by an assertion instead: the field list is read out of
# `load_issues`'s own source and compared against the fixture's keys.


#: The `--json` payload for one issue, exactly as `gh issue list` returns it.
#: Keys are asserted against `load_issues` in the test directly below, so this
#: cannot quietly fall behind the call it is standing in for.
def _issue(number: int, title: str, *, closed: bool, unit: bool, body: str = "") -> dict:
    return {
        "number": number,
        "title": title,
        "state": "CLOSED" if closed else "OPEN",
        "body": body,
        "labels": [{"name": "unit"}] if unit else [],
    }


def test_the_graph_double_carries_exactly_the_fields_load_issues_asks_gh_for():
    """The one way the payload double can drift, closed by reading the producer.

    Building the double at the network boundary means `build_graph` is measured
    rather than mimicked, and it leaves precisely one gap: the payload itself
    could stop resembling what `gh` is asked for. A field added to `load_issues`
    and not to `_issue` would make every test below run against an issue shape
    that no longer exists, and they would all still pass, because `build_graph`
    only reads the keys it reads today.

    So the field list is taken from the call rather than restated. Read off the
    source text because the argument list is positional strings inside a
    subprocess invocation, and there is nothing else to interrogate.
    """
    board = _board()
    source = (TESTS_DIR.parent / "scripts" / "board.py").read_text()
    call = source[source.index("def load_issues") : source.index("def parse_deps")]
    fields = re.findall(r'"([a-z,]*number,[a-z,]*)"', call)
    assert len(fields) == 1, (
        f"the --json field list is no longer a single literal in load_issues, so "
        f"this pin cannot read it: {fields}"
    )
    asked_for = set(fields[0].split(","))
    assert set(_issue(1, "U1: x", closed=False, unit=False)) == asked_for, (
        f"the payload double and load_issues disagree about the issue shape; gh is "
        f"asked for {sorted(asked_for)} and the double supplies "
        f"{sorted(_issue(1, 'U1: x', closed=False, unit=False))}"
    )
    assert callable(board.load_issues)


def test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on():
    """The detector, driven. R-322 is the finding that nothing drove it.

    Four cases in one graph, because the function's two failure directions are
    reached by different nodes and a graph holding only the positive case cannot
    see either of them.

    THE MISMATCHED NUMBER IS THE POINT. A register names a UNIT and the graph is
    keyed by ISSUE, and here U38 is issue #51 exactly as it is on the real board.
    Issue #38 is present too and belongs to a different unit that nothing owes, so
    reading the register's unit number as an issue number reports the wrong unit
    AND misses the right one, which is what the fixed code stopped doing and what
    `B5_contradictions_by_number` puts back.

    THE OPEN UNIT IS THE OTHER DIRECTION. U61 is owed a module and its issue is
    still open, which is not a contradiction at all: a register owing an open unit
    is the register working. Reporting it would teach a session that exit 2 is
    noise, which is the failure R-115 already bought a rule for.

    NO NODE HERE IS TITLED LIKE A RESIDUAL, and that is load bearing rather than
    incidental. `contradictions` composes the register comparison with
    `repointed_residuals`, which reads the real ledger from a path it computes
    itself, so a graph carrying an `R-n:` title makes this test's answer depend on
    a fourteen thousand line document nobody edited for it. The first draft used
    `R-4` for the non-unit node and picked up a real repoint finding on the second
    assertion. The attended-chore title exercises the same node shape, a board
    item that is not a unit, and drags nothing in with it.
    """
    board = _board()
    graph = board.build_graph(
        [
            _issue(51, "U38: the write routing pass", closed=True, unit=True),
            _issue(38, "U26: something else entirely", closed=True, unit=True),
            _issue(79, "U61: still in flight", closed=False, unit=True),
            _issue(90, "A2: an attended chore, and not a unit", closed=False, unit=False),
        ]
    )
    owed = {
        38: ["cratekit.write.routing"],
        61: ["cratekit.vocals.cli"],
        99: ["cratekit.nowhere.cli"],
    }

    found = board.contradictions(graph, owed=owed)

    assert len(found) == 1, (
        f"one closed unit here is owed a module and one open unit is, and only the "
        f"closed one is a contradiction; got {found}"
    )
    assert "#51" in found[0] and "U38" in found[0], (
        "the register owes U38, whose issue is #51; a report naming #38 has "
        "resolved a unit number as an issue number and is describing U26"
    )
    assert "cratekit.write.routing" in found[0], (
        "the refusal must name the module owed, because two registers can owe and "
        "the module is what says which file to open"
    )
    assert not any("#79" in line for line in found), (
        "U61 is owed a module and its issue is OPEN, which is the register "
        "working rather than the board contradicting it"
    )
    assert not any("#38" in line for line in found), (
        "#38 is U26's issue here and nothing owes U26; reporting it is the "
        "conflation that reported a contradiction over a unit nothing owed"
    )


def test_a_register_owing_a_unit_with_no_issue_at_all_is_silence_not_a_crash():
    """The branch that exists because the mapping can simply be absent.

    A unit number in a register need not appear on the board: a title can be
    edited, an issue can be transferred, and `units_by_issue_number` DROPS a unit
    two issues both claim, which is a deliberate absence rather than an accident.
    None of those is a contradiction and none of them may be a traceback either,
    because `audit` is the command a session runs before it stops and an audit
    that raises reports nothing about the drift it had already found.
    """
    board = _board()
    graph = board.build_graph(
        [
            _issue(77, "U59: the conformance unit", closed=True, unit=True),
            _issue(91, "U59: a duplicate claim on the same unit", closed=True, unit=True),
        ]
    )
    owed = {
        # Dropped by the mapping, because two issues claim it.
        59: ["cratekit.write.metadata_cli"],
        # Never on this board at all.
        99: ["cratekit.nowhere.cli"],
    }
    assert board.contradictions(graph, owed=owed) == [], (
        "U59 is claimed by two issues so the mapping drops it, U99 is not on the "
        "board, and the honest answer to both is to say nothing about that unit "
        "rather than to pick an issue or to raise"
    )


def test_a_repointed_residual_issue_is_reported_through_the_same_call(monkeypatch):
    """The other half of what `contradictions` returns, and it was undriven too.

    A residual's number lives in its ISSUE TITLE, which is a surface the
    repository cannot see, and the composed return is what carries that finding to
    `audit`. Dropping the second term would leave the function reporting only
    register contradictions with nothing anywhere saying the residual check had
    stopped happening.

    The document is supplied rather than read. Its real headings are append only
    and would serve, but a test that asserts over the live ledger is a test whose
    premise moves whenever somebody files a finding, and what is in question here
    is the comparison, not the parse. The parse is pinned separately below,
    against the real file, where the append-only rule makes that safe.
    """
    board = _board()
    graph = board.build_graph(
        [
            _issue(42, "R-5: the title the file agrees with", closed=False, unit=False),
            _issue(43, "R-6: a title the file no longer gives R-6", closed=False, unit=False),
            _issue(44, "R-900: a number the file has never held", closed=False, unit=False),
        ]
    )
    monkeypatch.setattr(
        board,
        "residual_titles",
        lambda: {
            5: "the title the file agrees with",
            6: "something else that R-6 now points at",
        },
    )

    found = board.contradictions(graph, owed={})

    assert len(found) == 2, f"one agreeing title, one repointed, one absent; got {found}"
    assert "#43" in found[0] and "R-6" in found[0]
    assert "#44" in found[1] and "R-900" in found[1]
    assert not any("#42" in line for line in found), (
        "a residual issue whose title still names what its number points at is "
        "correct, and flagging it is how this check gets switched off"
    )


def test_the_residual_heading_reader_reads_the_document_as_it_is_written():
    """The parse, pinned on the tree rather than on a double.

    `residual_titles` reads `docs/residual-findings.md` from a path it computes
    itself, so the only way to drive it honestly is against the real document.
    That is normally the wrong shape, since a test keyed to today's content passes
    for reasons unrelated to the code. It is the RIGHT shape here for one specific
    reason: residual numbers are append only by rule, and a renumber is forbidden
    precisely because issue titles carry these numbers. R-322's heading says the
    same thing next year as it does today, or a rule this project treats as
    absolute has been broken and a red test is the correct response.
    """
    board = _board()
    titles = board.residual_titles()
    assert titles[322] == "`contradictions()` is driven by nothing, and the composite proved it", (
        "the heading reader no longer reads a heading this document has held "
        "since it was filed, so either the parse changed or the append-only rule "
        "was broken"
    )
    assert 999999 not in titles


class _ClosingArgs:
    """The namespace `cmd_closing` reads, built here rather than through argparse.

    Going through `main()` would drive the parser as well, and the parser is not
    what is in question: what is untested is the GIT READING, which is the whole
    of the CI path.
    """

    def __init__(self, *, since=None, message_file=None):
        self.since = since
        self.message_file = message_file


def _seeded_repo(root: Path):
    """A throwaway git repository with one commit, and a runner bound to it.

    `--no-verify` throughout, because this repository's own commit-msg hook is
    the thing under test and a fixture that inherited it through a global hooks
    path would be measuring the hook rather than the function.
    """
    import subprocess

    root.mkdir(parents=True, exist_ok=True)

    def run(*argv, message_text=None):
        done = subprocess.run(
            argv,
            cwd=root,
            input=message_text,
            capture_output=True,
            text=True,
            check=False,
        )
        assert done.returncode == 0, f"{argv} failed: {done.stderr}"
        return done.stdout.strip()

    run("git", "init", "-q", "-b", "main")
    run("git", "config", "user.email", "fixture@example.invalid")
    run("git", "config", "user.name", "Fixture")
    run("git", "config", "commit.gpgsign", "false")
    (root / "seed.txt").write_text("seed\n")
    run("git", "add", "seed.txt")
    run("git", "commit", "-q", "--no-verify", "-m", "chore: seed")
    return run, run("git", "rev-parse", "HEAD")


@pytest.mark.parametrize("message", CLOSING_SPELLINGS_GITHUB_ACTS_ON)
def test_every_spelling_is_refused_through_a_real_commit_range(
    message, tmp_path, monkeypatch
):
    """The CI path, driven, and until now it was asserted only as source text.

    `test_every_spelling_github_closes_on_is_refused` hands `unresolved_closes` a
    string. That proves the regular expressions and nothing about the subcommand
    CI actually runs, which shells out to `git log --format=%B base..HEAD` and
    passes `raw=False`. Two things live only on this path and were driven
    nowhere: whether a real commit body survives the round trip through git at
    all, and the `raw=False` decision, which is the one that must NOT strip, on
    the grounds that a `#`-leading body line is a real trailer git keeps.

    The owed register is supplied rather than read off this repository. A test
    keyed to whatever `main` happens to owe today passes for a reason that has
    nothing to do with the code and fails the day somebody discharges a marker.
    """
    board = _board()
    repo = tmp_path / "fixture"
    run, base = _seeded_repo(repo)

    (repo / "one.txt").write_text("one\n")
    run("git", "add", "one.txt")
    run("git", "commit", "-q", "--no-verify", "-F", "-", message_text=message)

    monkeypatch.setattr(
        board,
        "owed_by_unit",
        lambda: {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]},
    )
    monkeypatch.chdir(repo)
    assert board.cmd_closing(_ClosingArgs(since=base)) == 2, (
        f"{message!r} reached history through git and the range check reported "
        f"clean, so CI would have let the close cascade"
    )


def test_a_hash_leading_body_line_survives_the_range_check(tmp_path, monkeypatch):
    """The asymmetry that made `raw` a parameter, driven on the path it protects.

    Git's `whitespace` cleanup, which `-F` and `-m` use, KEEPS a body line
    beginning with `#`. So a real trailer can reach history on such a line, and
    stripping comments on the range path would delete it and report clean. That
    is the CI path, the copy this repository calls the load-bearing one, so the
    strip would have done its only possible harm in the place it mattered most.
    """
    board = _board()
    repo = tmp_path / "fixture"
    run, base = _seeded_repo(repo)

    (repo / "one.txt").write_text("one\n")
    run("git", "add", "one.txt")
    run(
        "git",
        "commit",
        "-q",
        "--no-verify",
        "-F",
        "-",
        message_text="feat: x\n\n#36 was the tracker, and this Closes #36\n",
    )

    kept = run("git", "log", "--format=%B", f"{base}..HEAD")
    assert "Closes #36" in kept, (
        "git dropped the line, so this test is measuring git rather than the "
        "check and its premise has changed"
    )

    monkeypatch.setattr(
        board, "owed_by_unit", lambda: {36: ["cratekit.write.converge_cli"]}
    )
    monkeypatch.chdir(repo)
    assert board.cmd_closing(_ClosingArgs(since=base)) == 2


def test_an_unreadable_commit_range_is_nothing_to_judge_rather_than_a_refusal(
    tmp_path, monkeypatch
):
    """A check that fails where it cannot read is a check somebody deletes.

    CI fetches to a fixed depth and takes the merge base, and on a shallow clone
    that ref may simply not be there. Exit 0 with a sentence is the designed
    answer, and it is asserted here so that turning it into a refusal, or into a
    traceback, fails a row.
    """
    board = _board()
    empty = tmp_path / "not-a-repo"
    empty.mkdir()
    monkeypatch.chdir(empty)
    assert board.cmd_closing(_ClosingArgs(since="deadbeef")) == 0


def test_a_missing_message_file_refuses_with_a_sentence_not_a_traceback(tmp_path):
    """The hook path's bad invocation, which surfaces in place of the editor.

    An unhandled exception inside a commit-msg hook reads to the person running
    it as the tool being broken rather than the invocation being wrong, and the
    remedy they reach for is uninstalling the hook.
    """
    board = _board()
    assert board.cmd_closing(_ClosingArgs(message_file=str(tmp_path / "nope"))) == 1


def test_the_message_file_path_reads_the_file_and_refuses_on_it(tmp_path, monkeypatch):
    """The hook path end to end, including the pre-cleanup strip it owes.

    The template comment and the scissors block are what the hook sees and CI
    never does, so this is the one path where stripping is correct. Both are in
    the fixture, and the real trailer sits above them.
    """
    board = _board()
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text(
        "feat(write): converge\n"
        "\n"
        "Closes #36\n"
        "# Please enter the commit message for your changes.\n"
        "# ------------------------ >8 ------------------------\n"
        "+Closes #33\n"
    )
    monkeypatch.setattr(
        board,
        "owed_by_unit",
        lambda: {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]},
    )
    refusals = board.unresolved_closes(message.read_text(), raw=True)
    assert board.cmd_closing(_ClosingArgs(message_file=str(message))) == 2
    assert len(refusals) == 1, (
        "the diff below the scissors line was judged, so a commit --verbose "
        "would be refused over a trailer it never wrote"
    )
