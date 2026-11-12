"""U246: no comprehension rebuilds the same set once for every element it tests.

``favorites = tuple(entry for entry in placements if entry not in set(derived))``
read as a membership test against a set and ran as a set built anew for every
placement: ``derived`` names nothing the comprehension binds, so every one of
those sets was the same set, and a rebuild of ten thousand tracks spent 17 of
its 28 seconds building it (the speed survey of 2026-11-12, card U246). Ten
comprehensions elsewhere carried the same shape over one playlist's length.

The guard walks every module under ``src/cratekit``, the vendored downloader
aside, and refuses a set (``set``, ``frozenset``, ``dict.fromkeys``, or a set or
dict comprehension) built anew per element from names that do not change per
element: anywhere in a comprehension's condition, or as the set a membership
test in its element tests against. A name varies when the comprehension binds
it, or a comprehension or lambda between it and the set does. The fix is the
one U246 made eleven times: build the set once, above the comprehension, and
test against the name.

A call with no argument is not the shape (an empty set costs nothing to make and
reads as a default), and neither is a call over the element itself
(``set(row.tags)``), which is a different set for each element. A ``for``
statement and a later ``for`` clause's iterable are not read; the record names
them.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).resolve().parent.parent / "src" / "cratekit"

COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)

#: The vendored downloader is not this project's code, and ruff skips it too.
VENDORED = SOURCE_ROOT / "_vendor"

#: The two set constructors, by their bare name or as ``builtins.set``.
SET_CALLS = frozenset({"set", "frozenset"})


def _binds(node: ast.AST) -> set[str]:
    """The names a comprehension's ``for`` clauses or a lambda's parameters bind."""
    if isinstance(node, COMPREHENSIONS):
        return {
            name.id
            for generator in node.generators
            for name in ast.walk(generator.target)
            if isinstance(name, ast.Name)
        }
    if isinstance(node, ast.Lambda):
        arguments = node.args
        every = [*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs]
        every += [one for one in (arguments.vararg, arguments.kwarg) if one is not None]
        return {one.arg for one in every}
    return set()


def _builds_a_set(node: ast.AST) -> bool:
    """``set(x)``, ``frozenset(x)``, ``dict.fromkeys(x)`` or a set or dict comprehension."""
    if isinstance(node, ast.SetComp | ast.DictComp):
        return True
    if not isinstance(node, ast.Call) or not node.args:
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in SET_CALLS
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        if func.value.id == "builtins":
            return func.attr in SET_CALLS
        return func.value.id == "dict" and func.attr == "fromkeys"
    return False


def _scoped_children(node: ast.AST, names: set[str]):
    """Each child of ``node`` with the names that vary where it is evaluated.

    A comprehension's own variables vary inside it, except in its first ``for``
    clause's iterable, which Python evaluates once in the enclosing scope. A
    lambda's parameters vary in its body.
    """
    if isinstance(node, COMPREHENSIONS):
        first, *rest = node.generators
        inner = names | _binds(node)
        yield first.iter, names
        yield first.target, inner
        for condition in first.ifs:
            yield condition, inner
        for generator in rest:
            yield generator, inner
        for part in ("elt", "key", "value"):
            if getattr(node, part, None) is not None:
                yield getattr(node, part), inner
        return
    inner = names | _binds(node)
    for child in ast.iter_child_nodes(node):
        yield child, inner


def _free(node: ast.AST) -> set[str]:
    """The names an expression reads that nothing inside it binds."""
    free: set[str] = set()
    pending: list[tuple[ast.AST, set[str]]] = [(node, set())]
    while pending:
        current, bound = pending.pop()
        if isinstance(current, ast.Name) and current.id not in bound:
            free.add(current.id)
        pending.extend(_scoped_children(current, bound))
    return free


def _membership_operands(expression: ast.AST):
    """Each right hand side of an ``in`` or ``not in`` written in the expression."""
    for node in ast.walk(expression):
        if isinstance(node, ast.Compare):
            for operator, right in zip(node.ops, node.comparators, strict=True):
                if isinstance(operator, ast.In | ast.NotIn):
                    yield right


def _invariant_sets(expression: ast.AST, varying: set[str], *, anywhere: bool):
    """Each set built in ``expression`` that reads none of the ``varying`` names.

    ``varying`` grows by what every comprehension or lambda between the
    comprehension and the set binds, since those change per element too.
    ``anywhere`` reads every set the expression builds; otherwise only a set
    that is the right hand side of a membership test.
    """
    found = []
    pending = [(expression, varying)]
    while pending:
        node, names = pending.pop()
        if _builds_a_set(node) and not (_free(node) & names):
            if anywhere or any(node is right for right in _membership_operands(expression)):
                found.append(node)
                continue
        pending.extend(_scoped_children(node, names))
    return found


def rebuilt_per_element(source: str) -> list[str]:
    """Each set a comprehension builds anew, per element, from a value it does not vary.

    Read in two places: anywhere in a condition (an ``if`` clause), and as the
    set a membership test in the element (or a dict comprehension's key or
    value) tests against. As ``line: expression``, in source order.
    """
    found: dict[int, tuple[int, str]] = {}
    for comprehension in ast.walk(ast.parse(source)):
        if not isinstance(comprehension, COMPREHENSIONS):
            continue
        varying = _binds(comprehension)
        places = [
            (condition, True)
            for generator in comprehension.generators
            for condition in generator.ifs
        ]
        places += [
            (part, False)
            for part in (
                getattr(comprehension, "elt", None),
                getattr(comprehension, "key", None),
                getattr(comprehension, "value", None),
            )
            if part is not None
        ]
        for place, anywhere in places:
            for built in _invariant_sets(place, varying, anywhere=anywhere):
                found[id(built)] = (built.lineno, ast.unparse(built))
    return [f"{line}: {text}" for line, text in sorted(found.values())]


def test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element():
    modules = [
        path for path in sorted(SOURCE_ROOT.rglob("*.py")) if VENDORED not in path.parents
    ]
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
        # The inner ``one`` is the set's own variable, not the comprehension's.
        "kept = [one for one in removes if one in set(str(one) for one in now)]",
        "kept = [e for e in xs if e in {o.id for o in options}]",
        "kept = [e for e in xs if e in builtins.set(ys)]",
        "kept = {k: v for k, v in pairs if k in {o: 1 for o in ys}}",
        "found = any(x in set(ys) for x in xs)",
        "kept = [a if a in set(ys) else b for a in xs]",
        "kept = {k: k in frozenset(ys) for k in xs}",
        "kept = {k in set(ys): k for k in xs}",
        "kept = [x not in set(ys) for x in xs]",
        "kept = {x in set(ys) for x in xs}",
        "kept = [e for e in xs if e in builtins.frozenset(ys)]",
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
        # A set that varies with an inner comprehension's or a lambda's variable.
        "kept = [e for e in xs if any(1 for g in e.groups if 'house' in set(g.tags))]",
        "kept = [e for e in xs if any(filter(lambda g: 'house' in set(g.tags), e.groups))]",
        "kept = [e for e in xs if any(1 for o in set(e.options) if o)]",
        # Built in the element but not tested against: a value, not a lookup.
        "kept = [frozenset(ys) for x in xs]",
        # An inner comprehension's first iterable reads the outer variable,
        # even when the inner one rebinds its name.
        "kept = [one for one in rows if 1 in {one for one in one.kids}]",
        "kept = [x for x in xs if x in set(x for x in x.kids)]",
        "kept = [e for e in xs if any(filter(lambda *g, **h: 'a' in set(g), e.groups))]",
    ],
)
def test_the_guard_passes_a_set_built_once_or_built_from_the_element(source):
    assert rebuilt_per_element(source) == [], source
