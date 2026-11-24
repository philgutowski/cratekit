"""The parse memo the package wide guards share inside one test, held to its promises (U258).

``tests/_parse_memo.py`` hands one tree per source text to a sharing scope. It is
sound only if each text is parsed once per scope, never served stale, held by
nothing outside a scope, and never written to; and the at risk population test
that reads the package once still names a planted module.
"""

from __future__ import annotations

import ast
from collections.abc import Callable

import pytest

from tests import _parse_memo
from tests import _source_guards as guards
from tests import test_reserved_causes as reserved
from tests._parse_memo import parsed, shares_parses, sharing_parses


@pytest.fixture
def parses(monkeypatch):
    """Count every call ``ast.parse`` receives while the test runs."""
    calls: list[str] = []
    real = ast.parse

    def counting(source, *args, **kwargs):
        calls.append(source)
        return real(source, *args, **kwargs)

    monkeypatch.setattr(ast, "parse", counting)
    return calls


# One parse per text, inside a scope and only there


def test_inside_a_scope_one_text_is_parsed_once_however_many_ask(parses):
    source = "def read(row):\n    return row.rb_local_deleted\n"
    with sharing_parses():
        first = parsed(source)
        assert parsed(source) is first
        assert parsed(source.encode().decode()) is first, (
            "an equal text read back as a new string object is the same key"
        )
    assert parses == [source]
    assert ast.dump(first) == ast.dump(ast.parse(source))


def test_outside_a_scope_nothing_is_held_and_every_ask_parses(parses):
    source = "VALUE = 1\n"
    assert parsed(source) is not parsed(source)
    assert parses == [source, source]
    assert _parse_memo._TREES is None


def test_a_scope_drops_its_trees_when_it_ends_however_it_ends(parses):
    source = "VALUE = 1\n"
    with pytest.raises(RuntimeError), sharing_parses():
        held = parsed(source)
        raise RuntimeError("the test body failed")
    assert _parse_memo._TREES is None, "a failed test left its trees for the next"
    with sharing_parses():
        assert parsed(source) is not held
    assert len(parses) == 2


def test_a_scope_inside_a_scope_shares_the_outer_one_and_ends_with_it(parses):
    source = "VALUE = 1\n"
    with sharing_parses():
        outer = parsed(source)
        with sharing_parses():
            assert parsed(source) is outer
        assert parsed(source) is outer, "the inner scope ended the outer one's trees"
    assert _parse_memo._TREES is None
    assert parses == [source]


def test_a_decorated_test_shares_and_keeps_its_name_and_its_fixtures(parses):
    source = "VALUE = 1\n"

    def body(given):
        assert parsed(given) is parsed(given)
        return "answered"

    shared = shares_parses(body)
    assert shared.__name__ == "body" and shared.__wrapped__ is body
    assert shared(source) == "answered"
    assert parses == [source]
    assert _parse_memo._TREES is None
    assert getattr(
        reserved.test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned,
        "__wrapped__",
        None,
    ), "the at risk population test no longer shares its parses"
    assert getattr(
        reserved.test_pinned_populations_derive_totals_and_key_by_module, "__wrapped__", None
    ), "the pinned populations test no longer shares its parses"


def test_the_population_sweeps_parse_each_package_file_once_between_them(parses):
    """Inside one scope the first sweep parses each distinct text once, later sweeps none."""
    # The count is per file, so eighty modules measure it as well as the whole package.
    scanned = reserved.package_sources()[:80]
    distinct = {source for _, source in scanned}
    assert len(distinct) >= 51, f"the slice collapsed to {len(distinct)} texts"
    # The cause set parses through its own cache; asked first to keep it out of the count.
    reserved.declared_causes()
    parses.clear()
    with sharing_parses():
        by_module = reserved.kebab_literals_by_module(scanned)
        assert len(parses) == len(distinct), (
            f"one sweep of {len(distinct)} distinct texts called ast.parse "
            f"{len(parses)} times"
        )
        assert len(parses) == len(set(parses)), "a text was parsed twice in one sweep"
        holders = reserved.modules_holding_a_cause_literal(scanned)
        integers = {
            relative: reserved.holds_an_in_range_integer(source)
            for relative, source in scanned
        }
        assert len(parses) == len(distinct), (
            f"two more sweeps of the same texts parsed "
            f"{len(parses) - len(distinct)} of them again"
        )
    assert by_module and holders and any(integers.values()), (
        "the sweeps found nothing on the tree, so their counts measure nothing"
    )


# Never stale


def test_a_file_edited_inside_a_scope_is_read_as_it_now_is(tmp_path, parses):
    """An edit that keeps the file's length is read afresh, where a path or size key would not."""
    module = tmp_path / "planted.py"
    module.write_text('CODES = {"rclone-missing": 30}\n')
    # The cause set parses through its own cache; asked first to keep it out of the count.
    reserved.declared_causes()
    parses.clear()
    with sharing_parses():
        before = guards.reserved_code_tables_in(
            parsed(module.read_text()), reserved.declared_causes(), reserved.RANGE
        )
        module.write_text('CODES = {"rclone-missing": 3}\n ')
        after = guards.reserved_code_tables_in(
            parsed(module.read_text()), reserved.declared_causes(), reserved.RANGE
        )
    assert before == ["line 1: 'rclone-missing' -> status 30"]
    assert after == [], "the edited file was answered from the text it no longer holds"
    assert len(parses) == 2


# Never written

#: Real modules the shared questions have something to say about.
SHARED_MODULES = (
    "cli/exit_codes.py",
    "core/cause.py",
    "core/exit_codes.py",
    "write/metadata.py",
)

#: A planted second table, so a question a real module answers with nothing has one to lose.
PLANTED = {
    "core/planted_table.py": (
        'CODES = {\n    "rclone-missing": 30,\n    "rekordbox-running": 21,\n}\n'
    ),
}


def _questions(relative: str, source: str) -> dict[str, Callable[[], object]]:
    """Every question a sharing test asks of one module, each not yet asked."""
    package = reserved.package_of(relative)
    causes = reserved.declared_causes()
    pair = [(relative, source)]
    return {
        "reserved_code_tables_in": lambda: guards.reserved_code_tables_in(
            parsed(source), causes, reserved.RANGE, package
        ),
        "declared_enum_values": lambda: guards._declared_enum_values(parsed(source)),
        "named_without_own": lambda: reserved.modules_holding_a_named_cause(
            pair, own_declarations=False
        ),
        "named_with_own": lambda: reserved.modules_holding_a_named_cause(
            pair, own_declarations=True
        ),
        "cause_literals": lambda: reserved.modules_holding_a_cause_literal(pair),
        "kebab_literals": lambda: reserved.kebab_literals_by_module(pair),
        "in_range_integer": lambda: reserved.holds_an_in_range_integer(source),
    }


def _asked(
    questions: dict[str, Callable[[], object]], order: list[str]
) -> dict[str, object]:
    """Ask the questions in the order given and keep each answer by name."""
    return {name: questions[name]() for name in order}


def _fingerprint(tree: ast.AST) -> tuple[str, list[tuple[str, tuple[str, ...]]]]:
    """A tree's every field and position, and every attribute name, which ``ast.dump`` omits."""
    return (
        ast.dump(tree, include_attributes=True),
        [(type(node).__name__, tuple(sorted(vars(node)))) for node in ast.walk(tree)],
    )


def _sources() -> dict[str, str]:
    scanned = dict(reserved.package_sources())
    sources = {relative: scanned[relative] for relative in SHARED_MODULES}
    sources.update(PLANTED)
    return sources


def test_every_shared_question_leaves_a_shared_tree_as_a_fresh_parse_would():
    sources = _sources()
    with sharing_parses():
        trees = {relative: parsed(source) for relative, source in sources.items()}
        for relative, source in sources.items():
            questions = _questions(relative, source)
            _asked(questions, list(questions))
        for relative, source in sources.items():
            assert parsed(source) is trees[relative], (
                f"{relative} was parsed again, so this test shared no tree"
            )
    for relative, source in sources.items():
        assert _fingerprint(trees[relative]) == _fingerprint(ast.parse(source)), (
            f"a question wrote to the shared tree of {relative}, and every "
            f"question asked after it reads what that one left"
        )


def test_shared_trees_answer_alike_in_either_order_and_as_trees_of_their_own():
    """Questions over shared trees answer alike forward, backward, and each over a tree alone."""
    sources = _sources()
    forward: dict[str, dict[str, object]] = {}
    with sharing_parses():
        for relative, source in sources.items():
            questions = _questions(relative, source)
            forward[relative] = _asked(questions, list(questions))

    backward: dict[str, dict[str, object]] = {}
    with sharing_parses():
        for relative, source in reversed(list(sources.items())):
            questions = _questions(relative, source)
            backward[relative] = _asked(questions, list(reversed(list(questions))))
    assert forward == backward

    alone = {
        relative: _asked(_questions(relative, source), list(_questions(relative, source)))
        for relative, source in sources.items()
    }
    assert forward == alone, (
        "a question asked over a tree it shared answered differently from the "
        "same question asked over a tree of its own"
    )

    assert forward["core/planted_table.py"]["reserved_code_tables_in"]
    assert forward["core/planted_table.py"]["kebab_literals"]
    assert forward["core/planted_table.py"]["cause_literals"]
    assert forward["core/planted_table.py"]["in_range_integer"]
    assert forward["core/exit_codes.py"]["declared_enum_values"]
    assert forward["cli/exit_codes.py"]["reserved_code_tables_in"]
    assert any(answers["named_with_own"] for answers in forward.values())


# The population test that now reads the package once still sees all of it
# It stops at its first pin, so this proves only the kebab literal helper reads what
# it was handed; modules_holding_a_named_cause and holds_an_in_range_integer are
# unreached by this and by the parse count (review of 2026-11-12).


def test_the_at_risk_population_names_a_planted_module(monkeypatch):
    real = reserved.package_sources()
    planted = ("core/planted_table.py", PLANTED["core/planted_table.py"])
    monkeypatch.setattr(reserved, "package_sources", lambda: [*real, planted])
    with pytest.raises(AssertionError) as caught:
        reserved.test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned()
    assert "core/planted_table.py" in str(caught.value).split("\nassert ")[0]
