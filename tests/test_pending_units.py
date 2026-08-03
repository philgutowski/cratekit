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
   its module, this goes red, and the only way to make it green is to delete the
   entry, which arms the guard. Nobody has to remember; forgetting is what fails.
3. **No test skips outside the registry.** A bare skip mark anywhere in the suite
   is rejected, so the registry cannot be routed around.

Together these make a skip a countdown rather than a hiding place.
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
        "cratekit.intake.collection_xml",  # U37, the COLLECTION emitter
        "cratekit.core.restore",  # U32, the KTD21b replace
        "cratekit.acquire.match_cli",  # U16, R11's three states, split as U11 declared
        "cratekit.deletion.cli",  # U24, declines and tombstones through the decision stores
        "cratekit.modules.reports",  # U34, R26's duplicate audit as review items
        "cratekit.adopt",  # U23, R26's adoption plan as review items
        "cratekit.intake",  # U37, path repair proposals as review items
        "cratekit.cli.doctor",  # U27, the health check
        "path:skills",  # U28, the shipped operator skills
        "cratekit.cli.exit_codes",  # U38, the reserved exit-code vocabulary
        "cratekit.write.routing_cli",  # U20, the route.* verbs and the gated close
    }
)

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

    When it does, the fix is to delete the entry from ``_pending.PENDING`` and
    from ``EXPECTED_PENDING`` above. That single deletion arms every guard gated
    on it, which is the behaviour we want: the person who lands the module cannot
    ship it without the guards that govern it turning on.
    """
    unit, what = _pending.PENDING[key]
    assert _pending._is_absent(key), (
        f"{key} now exists, so {unit} has landed. Remove {key!r} from "
        f"_pending.PENDING and from EXPECTED_PENDING in this file. That arms the "
        f"guard asserting {what}, which must now pass."
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
#: U23's package is `cratekit.adopt` in the register and `cratekit.adoption` in
#: the registry. One of them is wrong and only U23 knows which, so it is recorded
#: here rather than picked by a branch that does not own that unit.
KNOWN_PACKAGE_NAME_DISAGREEMENTS = {("U23", "cratekit.adopt", "cratekit.adoption")}


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
    """
    board = _board()
    landed = TESTS_DIR.parent / "src" / "cratekit" / "write" / "tree_rebuild.py"
    assert not landed.exists(), "this fixture simulates U36 landing; it has landed"
    landed.write_text("# simulation, removed below\n")
    try:
        refusals = board.unresolved_closes(
            "Closes #32", {32: ["cratekit.write.rebuild", "cratekit.core.restore"]}
        )
    finally:
        landed.unlink()

    assert len(refusals) == 1
    assert "tree_rebuild" in refusals[0], (
        "the refusal must name the sibling that exists, or the reader is left to "
        "guess why a module is owed that nobody is going to write"
    )
    assert "cratekit.core.restore" not in refusals[0].split("note:", 1)[1], (
        "U32's live key has no near miss in its package and must not acquire a "
        "note; a note on a correct key is the false positive the rejected rule "
        "would have asserted"
    )
