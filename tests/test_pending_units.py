"""The meta-guard: a deferred guard cannot quietly become a permanent one.

U6 ported guards that name modules not yet written, and skipping them is
correct; skipping them FOREVER is a hole nobody sees, since a skip is green in
every summary. Three assertions make a skip a countdown:

1. **The declared set is exactly the intended set**, so a new skip is a
   visible decision in a diff.
2. **Every pending target is genuinely still absent**, so landing the module
   turns this red.
3. **No test skips outside the registry.**

A discharge is THREE edits in one commit: the entry in ``_pending.PENDING``,
the mirrored key in ``EXPECTED_PENDING`` below, and the ``@requires("<key>")``
decorator on every guard the key gated (``grep -rn 'requires("<key>")'
tests/`` first). Deleting the entry alone makes ``requires()`` raise KeyError
at import, so the gated file drops out of COLLECTION rather than turning red.
``docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md``
has the procedure and the U16 case that cost 330 tests.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tests import _pending

TESTS_DIR = Path(__file__).resolve().parent

# The intended pending set, written out rather than derived, so a registry
# change is made in two places and the second is a test a reviewer reads.
# Written ``frozenset()``, not ``frozenset({})``, which is an empty DICT node
# and crashed the duplicate guard's literal reader.
EXPECTED_PENDING: frozenset[str] = frozenset()

# EMPTY since U28 discharged ``path:skills``, the last countdown. It still
# asserts that nobody added a skip without declaring it.

# ``cratekit.session.restore_cli`` was discharged by U27, its one guard's
# decorator removed in the same commit.

# ``cratekit.adopt.apply_cli`` was discharged by U27; no guard carried it.

# ``cratekit.cli.reports`` was discharged by U27; no guard carried it.

# ``cratekit.write.rebuild`` was discharged by U36; ``tests/_pending.py``
# records which half became an always-armed tripwire in ``tests/test_restore.py``.

# U27 removed ``cratekit.cli.doctor`` and U8 its two entries. Ungating is not
# arming: the two guards released by the doctor could not fail as first written,
# so a discharge is the moment to read the guard it releases.


def test_the_intended_pending_set_has_no_duplicate_element():
    """A duplicate in the ``EXPECTED_PENDING`` literal is silent at runtime, so it is counted."""
    import ast
    import inspect

    literal = None
    for node in ast.walk(ast.parse(inspect.getsource(__import__(__name__, fromlist=["x"])))):
        target = None
        # BOTH ASSIGNMENT NODES, so annotating the register as ``frozenset[str]`` does
        # not lose it.
        if isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == "EXPECTED_PENDING":
            literal = node.value

    assert literal is not None, "EXPECTED_PENDING is no longer a module-level assignment"
    # ``frozenset({...})``: the set is the first argument; ``frozenset()`` is the
    # empty register, with no elements to read.
    if isinstance(literal, ast.Call):
        elements = literal.args[0].elts if literal.args else []
    else:
        elements = literal.elts
    written = [element.value for element in elements]
    duplicates = sorted({key for key in written if written.count(key) > 1})
    assert not duplicates, f"written twice and collapsed at parse time: {duplicates}"
    assert len(written) == len(EXPECTED_PENDING)

# Repository-wide guards that work against the tree as it stands. None may EVER
# be gated on a pending unit.
ALWAYS_ARMED_MODULES = (
    "test_portability.py",  # R1 literals and the repository-wide secret scan
    "test_layering.py",  # KTD23 import direction, R19 stable identifiers
    "test_packaging.py",  # R5 slim core, KTD19 interpreter bounds
    "test_duplication.py",  # U296: no newly copied block of six logical lines
    "test_import_rules.py",  # U296: private names, the core interface, the toggles
)


def test_the_declared_pending_set_is_exactly_the_intended_set():
    declared = frozenset(_pending.PENDING)
    assert declared == EXPECTED_PENDING, (
        f"undeclared skips added: {sorted(declared - EXPECTED_PENDING)}; "
        f"stale entries to remove: {sorted(EXPECTED_PENDING - declared)}. "
        f"Every deferred guard is a decision, and it belongs in a diff."
    )


def test_the_empty_register_is_a_discharged_register_and_not_a_lost_one():
    """An empty register is reported out loud, not as a mystery skip, and both registers agree.

    The countdown below is parametrized over nothing and so skipped; this test
    cannot be skipped and says why.
    """
    assert _pending.PENDING == {}, (
        f"the register is not empty, so the countdown below is parametrized and "
        f"this test is stale: {sorted(_pending.PENDING)}"
    )
    assert EXPECTED_PENDING == frozenset()


@pytest.mark.parametrize("key", sorted(EXPECTED_PENDING))
def test_a_pending_target_that_has_landed_must_be_removed_from_the_registry(key):
    """The countdown, DESIGNED to fail when a unit lands; discharge it by the three edits above."""
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
    """Every skip that does not route through ``_pending``: both marks and ``pytest.skip``."""
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
    """``_pending.py`` is the one file allowed to construct a skip."""
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
    """Portability, secrets, layering and packaging guards have no pending gate at all."""
    source = (TESTS_DIR / module).read_text()
    assert "_pending" not in source, (
        f"{module} is a repository-wide guard and must never be gated on a "
        f"pending unit; it has to bite from the moment it lands"
    )


# ── The register's own spelling, and the trailer that would close it ─────────
#
# The countdown proves an entry EXPIRES, not that it names something that can
# exist. A key no unit will build is absent forever, and when the unit closes
# ``board.py contradictions()`` exits 2 for good.


def _board():
    """Load ``scripts/board.py`` by path: it is a script, standard library only, inert on import."""
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
#: one, with the reason. EMPTY, and it should stay that way.
CLI_SHAPED_EXEMPTIONS: dict[str, str] = {}


def test_a_cli_shaped_register_key_names_a_module_some_verb_declares():
    """RULE A. A verb module in the register must be one the registry asks for.

    A key ending ``.cli`` or ``_cli`` names a command-line surface, which the
    registry declares; one it never asks for is absent forever and leaves a
    contradiction ``sync`` will not repair. A genuine exception goes in the
    exemption map with a reason. This is a spelling check on that third of the
    surface only; Rule B catches the rest when the unit closes.
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


#: The places the two registers disagree about a unit's own package name, by
#: EXACT membership, so a resolution forces the deletion. Emptied at the U59
#: merge when U23 settled ``cratekit.adopt`` against ``cratekit.adoption``.
KNOWN_PACKAGE_NAME_DISAGREEMENTS: set[tuple[str, str, str]] = set()


def test_no_unit_declares_two_confusingly_similar_package_roots():
    """A name similarity heuristic: one unit declaring two roots, one prefixing the other.

    A unit owning unrelated packages is ordinary (U32, U34). ``str.startswith``
    rather than a dotted segment test, since ``cratekit.adoption`` is not under
    ``cratekit.adopt``; it can be wrong, so a false positive is answered by adding
    the pair to the pin with a note.
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
    """RULE A's other half: ``find_spec`` returning None and raising are two kinds of missing.

    None is a module missing from a package that exists, a countdown armed.
    Raising means an ancestor is missing, which the tree cannot interpret. It is
    not forbidden, since planned verbs sit in that state, but the probe now says
    which case it is, and a ``ModuleNotFoundError`` from inside an existing
    ancestor is no longer swallowed as absence.
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
    """The registry's ``planned_in`` markers are a register too, and the board reads them."""
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
    """RULE B. ``audit``'s comparison moved before the event, to the closing trailer.

    ``contradictions()`` speaks only after the close has cascaded. Driven against
    a synthetic register, so it holds after every unit has landed.
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


#: Every spelling GitHub closes an issue on, written out rather than generated
#: from the pattern, which would pass whatever the pattern did.
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
    # A revert closes the issue too, and un-lands the module, so it is refused.
    'Revert "feat(write): converge (closes #36)"',
)

#: Messages that close nothing this repository tracks, and must stay exit 0.
MESSAGES_THAT_CLOSE_NOTHING = (
    "Closes #21",
    "see #36",
    "Closes #52",
    "look at #36 for why U36 is still open",
    "feat: x\n\nbody\n# Please enter the commit message\n# Closes #36\n",
    "feat: x\n\nCloses #21\n# ------------------------ >8 ------------------------\n+Closes #36\n",
    # THE SENTENCE THIS CHECK ASKS PEOPLE TO WRITE: a trailer, a blank line, then
    # what stays open. ``\s*`` crossing the newline once refused both.
    "feat(write): converge\n\nCloses #21\n\nand #36 stays open until the export CLI lands.\n",
    # A link with a fragment is not a closing reference.
    "see https://example.com/notes/fixes#36 for the reasoning",
    # CROSS-REPOSITORY references close an issue elsewhere; pyrekordbox's issue
    # numbers collide with the owed units constantly.
    "fixes numpy/numpy#36",
    "fixes https://github.com/dylanljones/pyrekordbox/issues/36",
    "chore(vendor): bump pyrekordbox\n\nfixes dylanljones/pyrekordbox#36 upstream\n",
)


@pytest.mark.parametrize("message", CLOSING_SPELLINGS_GITHUB_ACTS_ON)
def test_every_spelling_github_closes_on_is_refused(message):
    """Every spelling GitHub closes on is refused, not only ``Closes #n`` on a line of its own.

    The comma continuation is caught over-inclusively: a false refusal is one
    reworded line, a miss is a cascaded close ``sync`` will not repair.
    """
    board = _board()
    owed = {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]}
    assert board.unresolved_closes(message, owed), (
        f"{message!r} closes an issue on GitHub and this check reported clean"
    )


@pytest.mark.parametrize("message", MESSAGES_THAT_CLOSE_NOTHING)
def test_a_message_that_closes_nothing_owed_is_left_alone(message):
    """Template comments and a ``commit --verbose`` diff below the scissors close nothing."""
    board = _board()
    owed = {36: ["cratekit.write.converge_cli"], 33: ["cratekit.export.cli"]}
    assert not board.unresolved_closes(message, owed), (
        f"{message!r} closes nothing this register owes, and was refused anyway"
    )


def test_the_closing_check_is_wired_where_it_cannot_be_forgotten():
    """WHERE RULE B LIVES: a commit-msg hook, a subcommand, and ``audit`` after the close.

    A message exists for one moment, so only a hook sees it as written; but R-1
    found a hook absent from a fresh clone, so it is a subcommand too. The check
    is network-free, which is what lets it live in a hook.
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
    """CI judges the range from the ref's PREVIOUS TIP, never a merge base."""
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

    ``git log --format=%B`` runs messages together, so a subject ending "closes"
    before a body opening ``#36`` made a reference in neither. Driven through
    ``cmd_closing``, which does the concatenation.
    """
    board = _board()
    repo = tmp_path / "fixture"
    run, base = _seeded_repo(repo)
    # OLDEST FIRST HERE, NEWEST FIRST IN THE LOG: the message that must END with the
    # keyword is committed LAST, or the fixture manufactures nothing.
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
    """A trailer names an ISSUE and the registers name a UNIT: U38 is issue #51."""
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
    """Without the board the reference is read as a unit number, and the refusal says it guessed."""
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
    """The unit to issue map: read off titles, a duplicate dropped, the unit label required.

    A duplicate is dropped rather than letting the later issue answer wrongly.
    A unit-shaped title without the ``unit`` label is not a unit, which makes the
    label test inside ``contradictions`` redundant by construction
    (``docs/mutation/u81.md``).
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
    """``raw`` says which side of git's cleanup the text is on.

    The hook's message file is pre-cleanup, with comments and a ``--verbose``
    diff, which come out. ``git log --format=%B`` is final: a ``#``-leading body
    line survives ``whitespace`` cleanup, so stripping there could only delete a
    real trailer, on the CI path.
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
    """A refusal notes a sibling module the package does contain, as a note, never an assertion.

    A permanent exit 2 naming an owed ``cratekit.write.rebuild`` hid a one-word
    difference. An assertion was rejected as a substring heuristic that would fire
    on U32's live ``cratekit.core.restore``. Measured on the merged tree:
    ``cratekit.write.routing`` is absent beside ``routing_cli`` and
    ``routing_pass``, so nothing is written into ``src/``.
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
    """``_near_misses`` says nothing once the owed module exists."""
    board = _board()
    assert board._near_misses(["cratekit.write.rebuild"]) == [], (
        "a module that has landed must acquire no note; U36 shipped "
        "src/cratekit/write/rebuild.py and a note there would be a diagnosis of "
        "a problem that no longer exists"
    )


# ── Rule B's other half: the audit side, over a graph ────────────────────────
#
# ``contradictions`` is the comparison AFTER the close, and what makes ``board.py
# audit`` exit 2; R-322 measured that nothing drove it. The double is the
# PAYLOAD ``gh issue list --json`` returns, and ``build_graph`` runs on it for
# real, since a hand-built graph would type every derived key beside the test.
# The one drift this leaves, the payload against ``load_issues``'s field list,
# is closed by an assertion that reads the field list from its source.


#: The ``--json`` payload for one issue, as ``gh issue list`` returns it, its
#: keys checked against ``load_issues`` below.
def _issue(number: int, title: str, *, closed: bool, unit: bool, body: str = "") -> dict:
    return {
        "number": number,
        "title": title,
        "state": "CLOSED" if closed else "OPEN",
        "body": body,
        "labels": [{"name": "unit"}] if unit else [],
    }


def test_the_graph_double_carries_exactly_the_fields_load_issues_asks_gh_for():
    """The payload double carries exactly the fields ``load_issues`` asks ``gh`` for.

    Read structurally from the string after ``--json`` in its syntax tree, not by
    a pattern over field names, which could not express ``closedAt`` and would
    misdiagnose a drift.
    """
    board = _board()
    source = (TESTS_DIR.parent / "scripts" / "board.py").read_text()
    call = next(
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.FunctionDef) and node.name == "load_issues"
    )
    literals = [
        node.value
        for node in ast.walk(call)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]
    fields = [
        following
        for argument, following in zip(literals, literals[1:])
        if argument == "--json"
    ]
    assert len(fields) == 1, (
        f"the --json field list is no longer a single string literal following a "
        f"`--json` argument in load_issues, so this pin cannot read it: {fields}"
    )
    asked_for = set(fields[0].split(","))
    assert set(_issue(1, "U1: x", closed=False, unit=False)) == asked_for, (
        f"the payload double and load_issues disagree about the issue shape; gh is "
        f"asked for {sorted(asked_for)} and the double supplies "
        f"{sorted(_issue(1, 'U1: x', closed=False, unit=False))}"
    )
    assert callable(board.load_issues)


def test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on():
    """The detector, driven (R-322): a closed unit a register still owes is the exit 2 case.

    Four cases in one graph. U38 is issue #51 as on the real board and issue #38
    belongs to another unit, so reading a unit number as an issue reports the
    wrong unit and misses the right one. An open owed unit (U61) is no
    contradiction (R-115). No node is titled like a residual, since
    ``repointed_residuals`` reads the real ledger.
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
    """A register owing a unit with no issue at all is silence, not a crash."""
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
    """A repointed residual issue is reported through the same ``contradictions`` call."""
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


def test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it(monkeypatch):
    """With no ``owed`` supplied the live register is read, the only path ``cmd_audit`` takes.

    ``owed = owed or {}`` would keep every other test green while ``audit``
    stopped reporting, R-322's own failure one frame up.
    """
    board = _board()
    graph = board.build_graph(
        [_issue(51, "U38: the write routing pass", closed=True, unit=True)]
    )
    monkeypatch.setattr(board, "owed_by_unit", lambda: {38: ["cratekit.write.routing"]})

    found = board.contradictions(graph)

    assert len(found) == 1 and "#51" in found[0], (
        f"with no register supplied, the live one must be read; got {found}"
    )
    assert board.contradictions(graph, owed={}) == [], (
        "an explicitly EMPTY register is not the same as no register at all, and "
        "collapsing the two is how the default stops being reachable"
    )


def test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1(monkeypatch):
    """``audit`` exits 2 on a contradiction and 1 on drift, as ``CLAUDE.md`` tells sessions.

    Every name ``cmd_audit`` calls is module level and replaced here, so it runs
    without ``gh``. No node is titled like a residual, as above.
    """
    board = _board()
    payload = [
        _issue(51, "U38: the write routing pass", closed=True, unit=True),
        _issue(79, "U61: still in flight", closed=False, unit=True),
    ]
    monkeypatch.setattr(board, "repo_slug", lambda: ("fixture", "cratekit"))
    monkeypatch.setattr(board, "load_issues", lambda: payload)
    monkeypatch.setattr(board, "reconcile", lambda owner, apply, labels_only=False: [])
    monkeypatch.setattr(board, "owed_by_unit", lambda: {38: ["cratekit.write.routing"]})

    class _AuditArgs:
        labels_only = True

    assert board.cmd_audit(_AuditArgs()) == 2, (
        "a closed unit a register still owes is a contradiction, and exit 2 is "
        "what tells a session that a sync will not repair it"
    )

    monkeypatch.setattr(board, "owed_by_unit", lambda: {})
    monkeypatch.setattr(
        board, "reconcile", lambda owner, apply, labels_only=False: ["#79 says Ready"]
    )
    assert board.cmd_audit(_AuditArgs()) == 1, (
        "drift with no contradiction is exit 1, the code that sends a session to "
        "`board.py sync` rather than to a decision"
    )

    monkeypatch.setattr(board, "reconcile", lambda owner, apply, labels_only=False: [])
    assert board.cmd_audit(_AuditArgs()) == 0


def test_the_residual_heading_reader_reads_the_document_as_it_is_written():
    """The residual heading reader, pinned on the real document.

    Safe on live content only because residual numbers are append only: R-322's
    heading reads the same next year, or an absolute rule was broken.
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
    """The namespace ``cmd_closing`` reads, built here: the git reading is under test."""

    def __init__(self, *, since=None, message_file=None, pull_request_head=None):
        self.since = since
        self.message_file = message_file
        self.pull_request_head = pull_request_head


def _seeded_repo(root: Path):
    """A throwaway git repository with one commit, and a runner bound to it.

    ``--no-verify`` throughout, so a global hooks path cannot put the hook under
    test into the fixture.
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
    """The CI path, driven through a real commit range with ``raw=False``.

    The string test above proves the patterns only; a real body's round trip
    through git and the no-strip decision live here. The owed register is
    supplied, so the test does not depend on what ``main`` owes today.
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
    """A ``#``-leading body line is a real trailer git keeps, and the range check reads it."""
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
    """An unreadable range, as on a shallow clone, exits 0 with a sentence."""
    board = _board()
    empty = tmp_path / "not-a-repo"
    empty.mkdir()
    monkeypatch.chdir(empty)
    assert board.cmd_closing(_ClosingArgs(since="deadbeef")) == 0


def test_a_missing_message_file_refuses_with_a_sentence_not_a_traceback(tmp_path):
    """A missing message file refuses with a sentence, since a hook traceback gets uninstalled."""
    board = _board()
    assert board.cmd_closing(_ClosingArgs(message_file=str(tmp_path / "nope"))) == 1


def test_the_message_file_path_reads_the_file_and_refuses_on_it(tmp_path, monkeypatch):
    """The hook path end to end, stripping the template comment and scissors block it owes."""
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


# --------------------------------------------------------------------------
# U158: a pull request's own range, and the close its merge will write


def _owed_36(board, monkeypatch, owed=True):
    monkeypatch.setattr(
        board,
        "owed_by_unit",
        lambda: {36: ["cratekit.write.converge_cli"]} if owed else {},
    )


def _branch_commit(tmp_path):
    """A seeded repository with one trailer free commit after its base."""
    repo = tmp_path / "fixture"
    run, base = _seeded_repo(repo)
    (repo / "one.txt").write_text("one\n")
    run("git", "add", "one.txt")
    run("git", "commit", "-q", "--no-verify", "-m", "feat(u36): converge")
    return repo, base


def test_a_pull_request_range_closing_a_unit_still_owed_is_refused(tmp_path, monkeypatch):
    """The merge writes the trailer after CI, so the ``cloud/N-slug`` head's card is judged."""
    board = _board()
    repo, base = _branch_commit(tmp_path)
    _owed_36(board, monkeypatch)
    monkeypatch.chdir(repo)
    args = _ClosingArgs(since=base, pull_request_head="cloud/36-converge")
    assert board.cmd_closing(args) == 2, (
        "a pull request whose card a register still owes passed CI, so the merge "
        "would close a unit the repository says is unfinished"
    )


def test_the_same_pull_request_passes_once_the_register_is_discharged(tmp_path, monkeypatch):
    board = _board()
    repo, base = _branch_commit(tmp_path)
    _owed_36(board, monkeypatch, owed=False)
    monkeypatch.chdir(repo)
    args = _ClosingArgs(since=base, pull_request_head="cloud/36-converge")
    assert board.cmd_closing(args) == 0


def test_a_push_to_main_is_judged_exactly_as_before(tmp_path, monkeypatch):
    """No head branch, no implied close: only the trailers in the range count."""
    board = _board()
    repo, base = _branch_commit(tmp_path)
    _owed_36(board, monkeypatch)
    monkeypatch.chdir(repo)
    assert board.cmd_closing(_ClosingArgs(since=base)) == 0, (
        "a range with no trailer was refused, so a push now judges a close "
        "nobody wrote"
    )


@pytest.mark.parametrize(
    ("head", "card"),
    [
        ("cloud/339-pull-request-per-unit", 339),
        ("cloud/36-x", 36),
        ("main", None),
        ("feature/36-x", None),
        ("cloud/no-number", None),
        ("", None),
        (None, None),
    ],
)
def test_only_a_cloud_branch_names_the_card_its_merge_closes(head, card):
    assert _board().pull_request_card(head) == card


def _closing_step_script() -> str:
    workflow = (TESTS_DIR.parent / ".github" / "workflows" / "ci.yml").read_text()
    step = workflow[workflow.index("A unit may not close while a register") :]
    step = step[step.index("        run: |\n") + len("        run: |\n") :]
    lines = []
    for line in step.splitlines():
        if line.strip() and not line.startswith("          "):
            break
        lines.append(line[10:])
    return "\n".join(lines) + "\n"


def _drive_closing_step(tmp_path, env):
    """Run the workflow step's own shell with a `python` that records its argv."""
    import os
    import subprocess

    bindir = tmp_path / "bin"
    bindir.mkdir()
    record = tmp_path / "argv.txt"
    fake = bindir / "python"
    fake.write_text(f'#!/bin/sh\necho "$@" > "{record}"\nexit 0\n')
    fake.chmod(0o755)
    done = subprocess.run(
        ["bash", "-eo", "pipefail", "-c", _closing_step_script()],
        env={"PATH": f"{bindir}:{os.environ['PATH']}", **env},
        capture_output=True,
        text=True,
        check=False,
    )
    return done, (record.read_text().strip() if record.exists() else None)


def test_the_ci_step_judges_a_pull_request_from_its_base_with_its_head(tmp_path):
    done, argv = _drive_closing_step(
        tmp_path,
        {
            "EVENT": "pull_request",
            "PUSHED_FROM": "",
            "PR_BASE": "abc123",
            "PR_HEAD_REF": "cloud/339-pull-request-per-unit",
        },
    )
    assert done.returncode == 0, done.stderr
    assert argv == (
        "scripts/board.py closing --since abc123 "
        "--pull-request-head cloud/339-pull-request-per-unit"
    ), "the step no longer judges a pull request's own range and the card it closes"


def test_a_pull_request_event_with_no_base_sha_exits_0_and_says_why(tmp_path):
    done, argv = _drive_closing_step(
        tmp_path,
        {"EVENT": "pull_request", "PUSHED_FROM": "", "PR_BASE": "", "PR_HEAD_REF": "x"},
    )
    assert done.returncode == 0
    assert argv is None
    assert "no base sha" in done.stdout


@pytest.mark.parametrize("before", ["", "0" * 40])
def test_a_push_with_no_previous_tip_exits_0_and_says_why(tmp_path, before):
    done, argv = _drive_closing_step(
        tmp_path, {"EVENT": "push", "PUSHED_FROM": before, "PR_BASE": "", "PR_HEAD_REF": ""}
    )
    assert done.returncode == 0
    assert argv is None
    assert "no previous tip" in done.stdout


def test_a_push_is_judged_from_its_previous_tip_with_no_head(tmp_path):
    done, argv = _drive_closing_step(
        tmp_path,
        {"EVENT": "push", "PUSHED_FROM": "def456", "PR_BASE": "", "PR_HEAD_REF": ""},
    )
    assert done.returncode == 0, done.stderr
    assert argv == "scripts/board.py closing --since def456"


def test_the_closing_check_reads_full_history_in_ci():
    """A depth one checkout judges one commit whatever range it is handed."""
    workflow = (TESTS_DIR.parent / ".github" / "workflows" / "ci.yml").read_text()
    scan = workflow[workflow.index("  scan:") : workflow.index("A unit may not close")]
    assert "fetch-depth: 0" in scan
    step = workflow[workflow.index("A unit may not close while a register") :]
    step = step[: step.index("\n  portable:")]
    assert "--depth" not in step, "a shallow fetch would truncate the full history again"


def test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable(
    tmp_path, monkeypatch
):
    """The implied close needs no history, so an unreadable base cannot excuse it."""
    board = _board()
    repo, _base = _branch_commit(tmp_path)
    _owed_36(board, monkeypatch)
    monkeypatch.chdir(repo)
    args = _ClosingArgs(since="no-such-ref", pull_request_head="cloud/36-converge")
    assert board.cmd_closing(args) == 2


@pytest.mark.parametrize(
    "body",
    ["Closes #339", "this fixes #12 too", "Resolved   #7", "Card\nCloses #339\n"],
)
def test_a_closing_keyword_in_the_pull_request_body_is_refused(tmp_path, body):
    done, argv = _drive_closing_step(
        tmp_path,
        {
            "EVENT": "pull_request",
            "PUSHED_FROM": "",
            "PR_BASE": "abc123",
            "PR_HEAD_REF": "cloud/339-x",
            "PR_BODY": body,
        },
    )
    assert done.returncode == 2
    assert argv is None, "the range was judged after the body had already refused"
    assert "closing keyword" in done.stdout


def test_a_card_link_in_the_pull_request_body_is_not_a_keyword(tmp_path):
    done, argv = _drive_closing_step(
        tmp_path,
        {
            "EVENT": "pull_request",
            "PUSHED_FROM": "",
            "PR_BASE": "abc123",
            "PR_HEAD_REF": "cloud/339-x",
            "PR_BODY": "Card: https://github.com/philgutowski/cratekit/issues/339\nThe closing check.",
        },
    )
    assert done.returncode == 0, done.stdout
    assert argv is not None
