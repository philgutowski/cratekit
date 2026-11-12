"""U246: no comprehension rebuilds the same set once for every element it tests.

``favorites = tuple(entry for entry in placements if entry not in set(derived))``
read as a membership test against a set and ran as a set built anew for every
placement: ``derived`` names nothing the comprehension binds, so every one of
those sets was the same set, and a rebuild of ten thousand tracks spent 17 of
its 28 seconds building it (the speed survey of 2026-11-12, card U246). Ten
comprehensions elsewhere carried the same shape over one playlist's length.

The guard walks every module under ``src/cratekit`` and refuses a
comprehension whose condition calls ``set``, ``frozenset`` or ``dict.fromkeys``
on a value that names none of the comprehension's own variables, since that
value is the same on every element. The fix is the one U246 made eleven times:
build the set once, above the comprehension, and test against the name.

A call with no argument is not the shape (an empty set costs nothing to make and
reads as a default), and neither is a call over the element itself
(``set(row.tags)``), which is a different set for each element.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).resolve().parent.parent / "src" / "cratekit"

COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)


def _bound(comprehension: ast.AST) -> set[str]:
    """Every name the comprehension's own ``for`` clauses bind."""
    return {
        node.id
        for generator in comprehension.generators
        for node in ast.walk(generator.target)
        if isinstance(node, ast.Name)
    }


def _builds_a_set(call: ast.Call) -> bool:
    """``set(x)``, ``frozenset(x)`` or ``dict.fromkeys(x)``, over an argument."""
    if not call.args:
        return False
    func = call.func
    if isinstance(func, ast.Name):
        return func.id in {"set", "frozenset"}
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "fromkeys"
        and isinstance(func.value, ast.Name)
        and func.value.id == "dict"
    )


def rebuilt_per_element(source: str) -> list[str]:
    """Each set a comprehension's condition builds anew from a value it does not vary.

    As ``line: expression``, in source order.
    """
    found: list[tuple[int, str]] = []
    for comprehension in ast.walk(ast.parse(source)):
        if not isinstance(comprehension, COMPREHENSIONS):
            continue
        bound = _bound(comprehension)
        for generator in comprehension.generators:
            for condition in generator.ifs:
                for call in ast.walk(condition):
                    if not (isinstance(call, ast.Call) and _builds_a_set(call)):
                        continue
                    named = {node.id for node in ast.walk(call) if isinstance(node, ast.Name)}
                    if not named & bound:
                        found.append((call.lineno, ast.unparse(call)))
    return [f"{line}: {text}" for line, text in sorted(found)]


def test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element():
    modules = sorted(SOURCE_ROOT.rglob("*.py"))
    assert len(modules) > 100, f"the walk found {len(modules)} modules under {SOURCE_ROOT}"
    offenders = [
        f"{path.relative_to(SOURCE_ROOT.parent)}:{hit}"
        for path in modules
        for hit in rebuilt_per_element(path.read_text())
    ]
    assert offenders == [], (
        "a comprehension builds the same set once for every element it tests; build "
        "it once above the comprehension:\n" + "\n".join(offenders)
    )


@pytest.mark.parametrize(
    "source",
    [
        "kept = tuple(e for e in placements if e not in set(derived))",
        "kept = [e for e in placements if e in frozenset(derived)]",
        "kept = {e for e in placements if e not in set(self.requested)}",
        "kept = [o for o in dict.fromkeys(adds) if o not in set(now)]",
        "kept = {k: v for k, v in pairs if k in dict.fromkeys(wanted)}",
        "kept = [e for e in xs if e and (e.id in set(ids) or e.name)]",
        "kept = [e for row in rows for e in row if e in set(other)]",
    ],
)
def test_the_guard_finds_the_shape_in_every_comprehension(source):
    assert len(rebuilt_per_element(source)) == 1, source


@pytest.mark.parametrize(
    "source",
    [
        "known = set(derived)\nkept = tuple(e for e in placements if e not in known)",
        "kept = [row for row in rows if 'house' in set(row.tags)]",
        "kept = [o for o in options if o.id in frozenset(o.allowed)]",
        "kept = [e for e in xs if e not in lookup.get(e.key, frozenset())]",
        "kept = [e for row in rows for e in row if e in set(row.extra)]",
        "kept = [e for e in set(derived) if e]",
        "kept = set(derived) - set(placements)",
    ],
)
def test_the_guard_passes_a_set_built_once_or_built_from_the_element(source):
    assert rebuilt_per_element(source) == [], source
