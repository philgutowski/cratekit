"""No newly copied block of six logical lines: the duplication check (U296).

U290 point 3: removed duplication cannot grow back. A package's copied
blocks must be on its allowance under ``tests/ratchets/duplication/``, which
only shrinks.

Exact copies only. A logical line is one statement's tokens joined by single
spaces, with comments, blank lines, lone strings and imports dropped, so a
re-indented or re-wrapped copy is still a copy; a block is six or more
consecutive logical lines standing in two or more places. The normalised
reading also matches tables, so it stays a reading in
``scripts/refactor_measure.py``.

The allowance is held in windows of exactly six lines, so removing a partner
copy can only shrink what is found, where a whole block's digest would
change in a package nobody touched. An edit bringing two stretches together
is a new copy and fails on its own branch.

A copied helper is read beside it (U329): a function body of three lines or
more defined identically in two files, compared as syntax trees, which a
window of six lines can miss.
"""

from __future__ import annotations

import ast
import collections
from pathlib import Path

from tests._refactor_measure import measure

REPO_ROOT = Path(__file__).resolve().parent.parent


def _block(count: int, *, prefix: str = "step") -> str:
    """``count`` distinct statements, one per line."""
    return "".join(f"{prefix}_{number} = compute({number})\n" for number in range(count))


def _held(sources: dict[str, str]) -> dict[str, collections.Counter[str]]:
    return measure.Copies(sources).held()


def _sources(**packages: str) -> dict[str, str]:
    """``{package: text}`` as one module per package under the source root."""
    return {f"src/cratekit/{name}/module.py": text for name, text in packages.items()}


# ── What a logical line is ───────────────────────────────────────────────────


def test_a_logical_line_is_a_statements_tokens_joined_by_single_spaces():
    lines = measure.logical_lines("total   =   first +\\\n    second\n")
    assert [line.text for line in lines] == ["total = first + second"]
    assert (lines[0].start, lines[0].end) == (1, 2)


def test_comments_blank_lines_docstrings_and_imports_are_not_logical_lines():
    source = (
        '"""A module docstring."""\n'
        "import os\n"
        "from pathlib import Path\n"
        "\n"
        "# a comment on its own line\n"
        "def read(path):  # a trailing comment\n"
        '    """A function docstring."""\n'
        "    return Path(path).read_text()\n"
    )
    assert [line.text for line in measure.logical_lines(source)] == [
        "def read ( path ) :",
        "return Path ( path ) . read_text ( )",
    ]


def test_indentation_is_not_part_of_a_logical_line():
    flat = measure.logical_lines("value = 1\n")
    nested = measure.logical_lines("if ready:\n    value = 1\n")
    assert nested[1].text == flat[0].text


def test_a_string_inside_a_statement_is_kept_and_only_a_lone_string_is_dropped():
    lines = measure.logical_lines('"alone"\nname = "kept"\n')
    assert [line.text for line in lines] == ['name = "kept"']


# ── The rule bites: six lines, in two places ─────────────────────────────────


def test_a_copy_of_six_lines_is_found_in_both_packages():
    held = _held(_sources(label=_block(6), sync=_block(6)))
    assert {package: sum(counts.values()) for package, counts in held.items()} == {
        "label": 1,
        "sync": 1,
    }
    assert set(held["label"]) == set(held["sync"])


def test_a_copy_of_five_lines_is_not_a_block():
    assert _held(_sources(label=_block(5), sync=_block(5))) == {}


def test_six_lines_that_differ_in_one_token_are_not_a_copy():
    changed = _block(6).replace("compute(3)", "compute(30)")
    assert changed != _block(6)
    assert _held(_sources(label=_block(6), sync=changed)) == {}


def test_a_copy_inside_one_file_is_found():
    source = _block(6) + "between = 1\n" + _block(6)
    held = _held({"src/cratekit/label/module.py": source})
    assert sum(held["label"].values()) == 2


def test_a_copy_that_was_only_reindented_recommented_and_rewrapped_is_still_found():
    original = _block(6)
    disguised = "def moved():\n" + "".join(
        f"    # step {number}\n    step_{number} = compute(\n        {number}\n    )\n\n"
        for number in range(6)
    )
    assert sum(_held(_sources(label=original, sync=disguised))["sync"].values()) == 1


def test_imports_do_not_count_toward_the_six_lines():
    """Six lines of which one is an import are five lines, and the header of a
    module is where every pair of files looks alike."""
    source = "import os\n" + _block(5)
    assert _held(_sources(label=source, sync=source)) == {}


def test_a_longer_copy_is_its_run_of_windows():
    """Eight copied lines are three windows of six, in each place."""
    held = _held(_sources(label=_block(8), sync=_block(8)))
    assert sum(held["label"].values()) == 3
    assert len(held["label"]) == 3


def test_the_block_size_is_six_logical_lines():
    assert measure.BLOCK_LINES == 6


# ── The allowance: a multiset of lines that only shrinks ─────────────────────


def test_a_block_on_the_allowance_passes_and_a_new_one_beside_it_fails():
    before = _sources(label=_block(6), sync=_block(6))
    allowed = _held(before)
    assert measure.over_allowance(_held(before), allowed) == {}

    fresh = _block(6, prefix="fresh")
    after = _sources(label=_block(6) + fresh, sync=_block(6), intake=fresh)
    excess = measure.over_allowance(_held(after), allowed)
    assert set(excess) == {"label", "intake"}
    assert sum(excess["label"].values()) == 1 and sum(excess["intake"].values()) == 1
    assert not set(excess["label"]) & set(allowed["label"]), "the allowed block was reported"


def test_removing_a_block_with_its_line_still_on_the_allowance_passes():
    allowed = _held(_sources(label=_block(6), sync=_block(6)))
    cleaned = _sources(label="shared = helper()\n", sync=_block(6))
    assert _held(cleaned) == {}
    assert measure.over_allowance(_held(cleaned), allowed) == {}


def test_an_allowance_is_its_own_packages_and_excuses_no_other():
    """A window ``label`` and ``sync`` may hold is not one ``intake`` may copy."""
    allowed = _held(_sources(label=_block(6), sync=_block(6)))
    spread = _sources(label=_block(6), sync=_block(6), intake=_block(6))
    excess = measure.over_allowance(_held(spread), allowed)
    assert set(excess) == {"intake"} and sum(excess["intake"].values()) == 1


def test_a_third_copy_of_an_allowed_block_in_the_same_package_fails():
    """The allowance counts places, so an allowed digest is not a licence to copy it again."""
    twice = {"src/cratekit/label/a.py": _block(6), "src/cratekit/label/b.py": _block(6)}
    allowed = _held(twice)
    assert sum(allowed["label"].values()) == 2
    thrice = {**twice, "src/cratekit/label/c.py": _block(6)}
    excess = measure.over_allowance(_held(thrice), allowed)
    assert sum(excess["label"].values()) == 1


def test_removing_a_partner_copy_does_not_fail_the_package_that_kept_its_lines():
    """Removing a partner copy cannot fail the package that kept its lines, held in windows.

    ``adopt`` holds eight lines, ``tagging`` copies all eight and ``intake`` the
    last seven; when ``tagging`` removes its copy, ``adopt`` finds a subset of its
    allowance, where a whole block would have become a new digest.
    """
    eight = _block(8)
    seven = "".join(eight.splitlines(keepends=True)[1:])
    before = _sources(adopt=eight, tagging=eight, intake=seven)
    allowed = _held(before)

    after = _sources(adopt=eight, tagging="shared = helper()\n", intake=seven)
    found = _held(after)
    assert measure.over_allowance(found, allowed) == {}
    assert set(found["adopt"]) < set(allowed["adopt"])

    blocks_before = {(run.path, run.logical) for run in measure.Copies(before).runs}
    blocks_after = {(run.path, run.logical) for run in measure.Copies(after).runs}
    assert ("src/cratekit/adopt/module.py", 8) in blocks_before
    assert ("src/cratekit/adopt/module.py", 7) in blocks_after


def test_a_deletion_that_brings_two_stretches_together_is_a_new_copy():
    """A deletion bringing two stretches together is a new copy, reported on its branch (row 4)."""
    first, second = _block(3, prefix="first"), _block(3, prefix="second")
    before = _sources(sync=first + second, label=first + _block(2, prefix="between") + second)
    assert _held(before) == {}
    after = _sources(sync=first + second, label=first + second)
    excess = measure.over_allowance(_held(after), _held(before))
    assert set(excess) == {"label", "sync"}


def test_overlapping_windows_in_one_file_are_two_places():
    """Seven identical statements in a row read as a copy, as the survey's instrument read them."""
    held = _held({"src/cratekit/label/module.py": "step = compute()\n" * 7})
    assert sum(held["label"].values()) == 2


def test_an_allowance_file_is_a_multiset_of_its_lines():
    text = "# what this file is\n\nabc\n  abc  \n# a note\ndef\n"
    assert measure.parse_allowance(text) == collections.Counter({"abc": 2, "def": 1})


def test_pruning_keeps_what_is_still_found_and_can_never_add_a_line():
    allowed = collections.Counter({"gone": 2, "kept": 2, "fewer": 3})
    found = collections.Counter({"kept": 2, "fewer": 1, "new": 4})
    kept = measure.pruned(found, allowed)
    assert kept == collections.Counter({"kept": 2, "fewer": 1})
    assert not kept - allowed, "pruning added a line the allowance did not hold"


def test_a_window_is_described_by_where_it_stands():
    sources = _sources(label="first = 0\n" + _block(6), sync=_block(6))
    copies = measure.Copies(sources)
    (digest,) = copies.repeated
    assert copies.describe(digest) == (
        "src/cratekit/label/module.py:2-7, src/cratekit/sync/module.py:1-6"
    )


# ── The real package ─────────────────────────────────────────────────────────


def test_no_package_holds_a_copied_block_beyond_its_allowance():
    sources = measure.read_sources(REPO_ROOT, [measure.SOURCE])
    copies = measure.Copies(sources)
    # A reading that read nothing would pass, so the reading is checked first.
    assert len(sources) > 100 and copies.logical_total > 10_000, (
        f"read {len(sources)} files and {copies.logical_total} logical lines, "
        "too few to be the package"
    )
    assert not any(f"/{measure.VENDOR}/" in path for path in sources)

    allowed = measure.read_allowances(REPO_ROOT, measure.DUPLICATION_ALLOWANCES)
    excess = measure.over_allowance(copies.held(), allowed)
    problems = [
        f"{package}: {count} place(s) of window {digest} beyond its allowance, "
        f"which stands at {copies.describe(digest)}"
        for package, counts in sorted(excess.items())
        for digest, count in sorted(counts.items())
    ]
    assert not problems, (
        "a block of six logical lines or more was copied. Give the lines one home "
        "and call it from each place; the allowance under "
        f"{measure.DUPLICATION_ALLOWANCES}/ is never added to:\n" + "\n".join(problems)
    )


# ── Identical function bodies (U329) ─────────────────────────────────────────
#
# A copied helper is the duplication the window reading misses: a body of three
# statements is half a window. A body is a function's arguments and its
# statements as syntax trees, its docstring dropped, so a re-wrapped or
# re-documented copy is still a copy; it counts from three physical lines.

BODY_LINES = 3


def identical_bodies(sources: dict[str, str]) -> list[list[str]]:
    """Each body defined in two or more files, as its places, ``path:line name``."""
    places: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for path, text in sources.items():
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            body = node.body[1:] if ast.get_docstring(node, clean=False) is not None else node.body
            if not body or body[-1].end_lineno - body[0].lineno + 1 < BODY_LINES:
                continue
            key = ast.dump(node.args) + "".join(ast.dump(statement) for statement in body)
            places[key].append((path, f"{path}:{node.lineno} {node.name}"))
    return sorted(
        sorted(place for _, place in found)
        for found in places.values()
        if len({path for path, _ in found}) > 1
    )


def _function(name: str, body: str, *, docstring: str = "") -> str:
    lines = [f'    """{docstring}"""'] if docstring else []
    lines += [f"    {line}" for line in body.splitlines()]
    return f"def {name}(path, *, strict=False):\n" + "\n".join(lines) + "\n"


_BODY = "found = read(path)\nif strict and not found:\n    raise ValueError(path)\nreturn found"


def test_a_body_defined_in_two_files_is_a_copy_whatever_its_docstring():
    found = identical_bodies(
        {
            "src/cratekit/core/one.py": _function("load", _BODY, docstring="One way."),
            "src/cratekit/write/two.py": _function("load", _BODY, docstring="Another way."),
        }
    )
    assert found == [["src/cratekit/core/one.py:1 load", "src/cratekit/write/two.py:1 load"]]


def test_a_renamed_function_with_the_same_body_is_still_a_copy():
    found = identical_bodies(
        {"a.py": _function("load", _BODY), "b.py": _function("read_it", _BODY)}
    )
    assert found == [["a.py:1 load", "b.py:1 read_it"]]


def test_a_body_under_three_lines_or_in_one_file_is_not_a_copy():
    short = "found = read(path)\nreturn found"
    assert not identical_bodies(
        {"a.py": _function("load", short), "b.py": _function("load", short)}
    )
    twice = _function("load", _BODY) + _function("again", _BODY)
    assert not identical_bodies({"a.py": twice})


def test_bodies_that_differ_in_an_argument_or_a_statement_are_not_copies():
    other_args = _function("load", _BODY).replace("strict=False", "strict=True")
    other_body = _function("load", _BODY.replace("ValueError", "KeyError"))
    base = _function("load", _BODY)
    assert not identical_bodies({"a.py": base, "b.py": other_args})
    assert not identical_bodies({"a.py": base, "b.py": other_body})


def test_no_function_body_is_defined_identically_in_two_files():
    sources = measure.read_sources(REPO_ROOT, [measure.SOURCE])
    assert len(sources) > 100, f"read {len(sources)} files, too few to be the package"
    found = identical_bodies(sources)
    assert not found, (
        "a function body of three lines or more is defined identically in two files. "
        "Give it one home and import it from each place:\n"
        + "\n".join(", ".join(places) for places in found)
    )
