"""The parse memo the package wide guards share, held to its three promises (U258).

``tests/_parse_memo.py`` hands one tree per source text to every guard that
asks. That buys back the parses the guards used to repeat, and it is only
sound if three things hold, each driven here rather than trusted:

1. ONE PARSE PER TEXT. A guard's sweep parses each file once, and a second
   sweep of the same texts parses nothing.
2. NEVER STALE. The key is the text itself, so a file edited between two
   sweeps is parsed afresh and answered from what it now says.
3. NEVER WRITTEN. Every guard question the sweeps ask, run over one shared tree
   in either order, gives the same answers, and leaves every tree equal to a
   fresh parse of its text, node by node, field by field, with no attribute
   added.
"""

from __future__ import annotations

import ast
from collections.abc import Callable

import pytest

from tests import _parse_memo
from tests import _source_guards as guards
from tests._parse_memo import parsed
from tests.modules import test_reports as reports
from tests.test_pool_sizing import (
    _attributes_read,
    _names_used,
    pool_plan_constructions,
    process_pool_constructions,
    unplanned_map_workers,
)
from tests.test_reserved_causes import (
    RANGE,
    converting_handlers,
    declared_causes,
    holds_an_in_range_integer,
    kebab_literals_by_module,
    modules_holding_a_cause_literal,
    modules_holding_a_named_cause,
    package_of,
    package_sources,
)


@pytest.fixture
def parses(monkeypatch):
    """Count every call ``ast.parse`` receives, starting from an empty memo."""
    calls: list[str] = []
    real = ast.parse

    def counting(source, *args, **kwargs):
        calls.append(source)
        return real(source, *args, **kwargs)

    _parse_memo.forget()
    monkeypatch.setattr(ast, "parse", counting)
    yield calls
    _parse_memo.forget()


# ═══════════════════════════════════════════════════════════════════════════
# One parse per text
# ═══════════════════════════════════════════════════════════════════════════


def test_one_text_is_parsed_once_however_many_ask(parses):
    source = "def read(row):\n    return row.rb_local_deleted\n"
    first = parsed(source)
    assert parsed(source) is first
    assert parsed(str(source.encode().decode())) is first, (
        "an equal text read back as a new string object is the same key"
    )
    assert parses == [source]
    assert ast.dump(first) == ast.dump(ast.parse(source))


def test_a_sweep_parses_each_package_file_once_and_a_second_sweep_none(parses):
    """The brief's count, over the real package and the helpers that sweep it.

    Three helpers of ``tests/test_reserved_causes.py`` walk the same files one
    after another, and before U258 each parsed every file again. Now the first
    walk parses each distinct text once, and the walks after it parse nothing.
    """
    scanned = package_sources()
    distinct = {source for _, source in scanned}
    assert len(distinct) >= 51, f"the package collapsed to {len(distinct)} texts"

    by_module = kebab_literals_by_module(scanned)
    assert len(parses) == len(distinct), (
        f"one sweep of {len(distinct)} distinct texts called ast.parse "
        f"{len(parses)} times"
    )
    assert len(parses) == len(set(parses)), "a text was parsed twice in one sweep"

    holders = modules_holding_a_cause_literal(scanned)
    integers = {relative: holds_an_in_range_integer(source) for relative, source in scanned}
    assert len(parses) == len(distinct), (
        f"two more sweeps of the same texts parsed "
        f"{len(parses) - len(distinct)} of them again"
    )
    assert by_module and holders and any(integers.values()), (
        "the sweeps found nothing on the tree, so their counts measure nothing"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Never stale
# ═══════════════════════════════════════════════════════════════════════════


def test_an_edited_text_is_parsed_afresh_and_answered_from_what_it_says(parses):
    clean = "def read(row):\n    return getattr(row, COLUMN, _ABSENT)\n"
    edited = 'def read(row):\n    return getattr(row, "rb_local_deleted", 0)\n'
    assert guards.permissive_soft_delete_reads_in(parsed(clean)) == []
    assert guards.permissive_soft_delete_reads_in(parsed(edited)) == [
        "line 2: getattr(row, 'rb_local_deleted', 0)"
    ]
    assert parses == [clean, edited]


def test_a_file_edited_between_two_sweeps_is_read_as_it_now_is(tmp_path, parses):
    """The case a key on the path or the size would get wrong, on disk.

    The edit keeps the file's length, so a key on the path, the size, or both
    would serve the old tree; the text differs, so the memo cannot.
    """
    module = tmp_path / "planted.py"
    module.write_text("import sys\n\n\ndef bail():\n    sys.exit(0)\n")
    before = guards.process_status_literals_in(parsed(module.read_text()))
    module.write_text("import sys\n\n\ndef bail():\n    sys.exit(7)\n")
    after = guards.process_status_literals_in(parsed(module.read_text()))
    assert before == []
    assert after == ["line 5: sys.exit(7)"]
    assert len(parses) == 2


def test_crossing_the_text_budget_empties_the_memo_and_answers_stay_right(
    monkeypatch, parses
):
    monkeypatch.setattr(_parse_memo, "TEXT_BUDGET", 40)
    first = "VALUE = 1\nOTHER = 2\n"
    second = "VALUE = 3\nOTHER = 4\nTHIRD = 5\n"
    one = parsed(first)
    assert parsed(first) is one
    parsed(second)
    assert parses == [first, second]
    again = parsed(first)
    assert again is not one, "the budget was crossed and the old tree was still served"
    assert ast.dump(again) == ast.dump(ast.parse(first))
    assert parses[:3] == [first, second, first]


# ═══════════════════════════════════════════════════════════════════════════
# Never written
# ═══════════════════════════════════════════════════════════════════════════

#: Real modules the swept questions have something to say about: a reservation
#: table owner, the vocabulary with its own enum, a soft delete reader, and a
#: module the reports audit admits. Chosen for size as well: the largest modules
#: take seconds a pass under the reports questions, and the planted texts below
#: carry the positive answers, so four real modules keep this under five seconds.
SHARED_MODULES = (
    "cli/exit_codes.py",
    "core/exit_codes.py",
    "write/metadata.py",
    "core/naming.py",
)

#: And one planted text per guard, so every question has a positive answer to
#: lose if a shared tree were written to.
PLANTED = {
    "core/planted_table.py": 'CODES = {\n    "rclone-missing": 30,\n    "rekordbox-running": 21,\n}\n',
    "core/planted_exit.py": "import sys\n\n\ndef bail():\n    sys.exit(7)\n",
    "core/planted_read.py": 'def read(row):\n    return getattr(row, "rb_local_deleted", 0)\n',
    "core/planted_pool.py": (
        "from concurrent.futures import ProcessPoolExecutor\n\n\n"
        "def run():\n    return ProcessPoolExecutor(max_workers=9)\n"
    ),
    "core/planted_writer.py": 'def stash(path, data):\n    getattr(path, "write_text")(data)\n',
}


def _questions(relative: str, source: str) -> dict[str, Callable[[], object]]:
    """Every question a package wide sweep asks of one module, each not yet asked."""
    package = package_of(relative)
    dotted = f"{package}.{relative.rsplit('/', 1)[-1].removesuffix('.py')}"
    causes = declared_causes()
    pair = [(relative, source)]
    return {
        "reserved_code_tables_in": lambda: guards.reserved_code_tables_in(
            parsed(source), causes, RANGE, package
        ),
        "process_status_literals_in": lambda: guards.process_status_literals_in(parsed(source)),
        "permissive_soft_delete_reads_in": lambda: guards.permissive_soft_delete_reads_in(
            parsed(source)
        ),
        "reads_soft_delete_marker_in": lambda: guards.reads_soft_delete_marker_in(parsed(source)),
        "_declared_enum_values": lambda: guards._declared_enum_values(parsed(source)),
        "converting_handlers": lambda: [
            ast.dump(handler) for handler in converting_handlers(parsed(source))
        ],
        "named_without_own": lambda: modules_holding_a_named_cause(pair, own_declarations=False),
        "named_with_own": lambda: modules_holding_a_named_cause(pair, own_declarations=True),
        "cause_literals": lambda: modules_holding_a_cause_literal(pair),
        "kebab_literals": lambda: kebab_literals_by_module(pair),
        "in_range_integer": lambda: holds_an_in_range_integer(source),
        "process_pool_constructions": lambda: process_pool_constructions(source),
        "pool_plan_constructions": lambda: pool_plan_constructions(source, package=package),
        "unplanned_map_workers": lambda: unplanned_map_workers(source, package=package),
        "names_used": lambda: _names_used(source),
        "attributes_read": lambda: _attributes_read(source),
        "filesystem_mutations": lambda: reports.filesystem_mutations(source),
        "resolved_imports": lambda: reports._resolved_imports(source, dotted),
        "import_module_calls": lambda: reports._import_module_calls(source),
        "names_bound_by": lambda: reports._names_bound_by(source),
        "unnamed_writers": lambda: reports._unnamed_writers(dotted, source),
    }


def _asked(
    questions: dict[str, Callable[[], object]], order: list[str]
) -> dict[str, object]:
    """Ask the questions in the order given and keep each answer by name."""
    return {name: questions[name]() for name in order}


def _fingerprint(tree: ast.AST) -> tuple[str, list[tuple[str, tuple[str, ...]]]]:
    """A tree's every field and position, and every attribute any node carries.

    ``ast.dump`` sees a rewritten field or a moved line; the attribute names see a
    note a guard left on a node, a parent pointer or a cache, which ``ast.dump``
    does not print.
    """
    return (
        ast.dump(tree, include_attributes=True),
        [(type(node).__name__, tuple(sorted(vars(node)))) for node in ast.walk(tree)],
    )


def _sources() -> dict[str, str]:
    scanned = dict(package_sources())
    sources = {relative: scanned[relative] for relative in SHARED_MODULES}
    sources.update(PLANTED)
    return sources


def test_every_swept_question_leaves_a_shared_tree_as_a_fresh_parse_would(parses):
    sources = _sources()
    trees = {relative: parsed(source) for relative, source in sources.items()}
    for relative, source in sources.items():
        questions = _questions(relative, source)
        _asked(questions, list(questions))
    for relative, source in sources.items():
        assert parsed(source) is trees[relative], (
            f"{relative} was parsed again, so this test shared no tree"
        )
        assert _fingerprint(trees[relative]) == _fingerprint(ast.parse(source)), (
            f"a guard question wrote to the shared tree of {relative}, and every "
            f"guard asking after it reads what that guard left"
        )


def test_two_orders_over_shared_trees_give_the_same_answers(parses):
    """The brief's scenario: guards sharing a tree answer alike in either order.

    The first pass asks each module's questions in the order written, the second,
    over a memo emptied and refilled, in the reverse order, and both are compared
    with answers from trees nobody else touched.
    """
    sources = _sources()
    forward: dict[str, dict[str, object]] = {}
    for relative, source in sources.items():
        questions = _questions(relative, source)
        forward[relative] = _asked(questions, list(questions))

    _parse_memo.forget()
    backward: dict[str, dict[str, object]] = {}
    for relative, source in reversed(list(sources.items())):
        questions = _questions(relative, source)
        backward[relative] = _asked(questions, list(reversed(list(questions))))
    assert forward == backward

    _parse_memo.forget()
    alone: dict[str, dict[str, object]] = {}
    for relative, source in sources.items():
        questions = _questions(relative, source)
        alone[relative] = {}
        for name in questions:
            _parse_memo.forget()
            alone[relative][name] = questions[name]()
    assert forward == alone, (
        "a question asked over a tree it shared answered differently from the "
        "same question asked over a tree of its own"
    )

    for relative in PLANTED:
        found = {name: answer for name, answer in forward[relative].items() if answer}
        assert found, f"no question found anything in {relative}, so it proves nothing"
    assert forward["core/planted_table.py"]["reserved_code_tables_in"]
    assert forward["core/planted_exit.py"]["process_status_literals_in"]
    assert forward["core/planted_read.py"]["permissive_soft_delete_reads_in"]
    assert forward["core/planted_pool.py"]["process_pool_constructions"]
    assert forward["core/planted_writer.py"]["unnamed_writers"]
