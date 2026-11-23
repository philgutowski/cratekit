"""One parse per source text inside a sharing scope, for the guards that sweep the package.

The package-wide guards once called ``ast.parse`` 5,934 times for about 660
files in one process (U258). A parse depends only on the text, so inside a
scope the TEXT is the key: an edited file reads back as a new key and is
parsed afresh, and two files with one text share one tree.

Scoped, never held for the worker's life: holding every tree of the 681
swept files cost about 720 MB a worker and slowed the collector more than
the parses saved (measured on a four core Linux container). A scope is one
test, or one module whose tests all sweep the package, as
``tests/test_reserved_causes.py`` opens (U312). Outside a scope
:func:`parsed` is ``ast.parse`` and holds nothing.

READ ONLY BY CONTRACT, driven by ``tests/test_parse_memo.py``, which runs
every shared question over shared trees in both orders and alone and compares
each tree with a fresh parse, attribute by attribute. A guard that annotates
nodes parses its own copy. Only the default parse is memoised.
"""

from __future__ import annotations

import ast
import contextlib
import functools
from collections.abc import Callable, Iterator
from typing import TypeVar

_Test = TypeVar("_Test", bound=Callable[..., object])

#: The trees of the scope now open, by text, or None when no scope is open.
_TREES: dict[str, ast.Module] | None = None


def parsed(source: str) -> ast.Module:
    """The tree ``ast.parse(source)`` gives, once per text inside a scope; never mutate it."""
    if _TREES is None:
        return ast.parse(source)
    tree = _TREES.get(source)
    if tree is None:
        tree = ast.parse(source)
        _TREES[source] = tree
    return tree


@contextlib.contextmanager
def sharing_parses() -> Iterator[None]:
    """Share one tree per text until the block ends; a nested scope adds nothing."""
    global _TREES
    if _TREES is not None:
        yield
        return
    _TREES = {}
    try:
        yield
    finally:
        _TREES = None


def shares_parses(test: _Test) -> _Test:
    """Run one test inside :func:`sharing_parses`, its fixtures untouched."""

    @functools.wraps(test)
    def shared(*args, **kwargs):
        with sharing_parses():
            return test(*args, **kwargs)

    return shared  # type: ignore[return-value]
