"""One parse per source text within one test, for the guards that sweep the package.

A guard that walks every module asks ``ast.parse`` for each file it reads, and
the slowest of them asked again and again inside ONE test: measured on
2026-11-12 over five of them in one process, ``ast.parse`` was called 5,934
times for about 660 source files (U258), most of it the at risk population in
``tests/test_reserved_causes.py`` parsing every package module once per helper,
six helpers deep. The answer to a parse depends on nothing but the text, so
inside a sharing scope the text is the key and each distinct text is parsed
once.

KEYED ON THE TEXT ITSELF, never on a path, a modification time or a size. A
file edited during a test reads back as a different string, which is a
different key, so it is parsed afresh and an answer about the old text can
never be served for the new one. Two files holding the same text share one
tree, which is correct, because the tree is a function of the text alone.

SCOPED TO ONE TEST, AND THAT IS A MEASUREMENT, NOT CAUTION. The first version
of this module held every tree for the life of the worker, so a later guard
sweeping the same files parsed nothing. Measured on a four core Linux
container, it cost more than it saved: every tree of the 681 files the guards
sweep is about 720 MB in one process, worker peak memory rose from about 250 MB
to about 950 MB, and the collector walking that many live nodes made the soft
delete sweep slower, 19.5 s to 22.5 s alone under pytest; outside pytest the
same sweep took 19.7 s without the memo, 25.0 s with it, and 17.9 s with it and
the collector switched off.
The guards that share files across tests (the two soft delete sweeps, the pool
sweep) spend their time in analysis, not in parsing, so retaining trees bought
them nothing. Outside a sharing scope :func:`parsed` is ``ast.parse`` and holds
nothing; inside one, trees live until the scope ends.

READ ONLY BY CONTRACT, and the contract is driven rather than trusted. Inside a
scope one tree is handed to every guard that asks for that text, so a guard that
wrote to a node, an annotation, a parent pointer, a rewritten field, would leak
that write into every guard after it. ``tests/test_parse_memo.py`` runs every
guard question the sweeps ask over shared trees in both orders and alone, and
compares each tree with a fresh parse of its text, node by node and attribute
by attribute. A guard that needs to annotate nodes parses its own copy with
``ast.parse`` and never asks here.

Only the default parse is memoised: ``mode="exec"``, no type comments, no
feature version. A caller that needs another parses for itself.
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
    """The tree ``ast.parse(source)`` gives, parsed once per text inside a scope.

    The caller must not mutate the tree it is handed: inside a scope the same
    object goes to every other caller asking about the same text.
    """
    if _TREES is None:
        return ast.parse(source)
    tree = _TREES.get(source)
    if tree is None:
        tree = ast.parse(source)
        _TREES[source] = tree
    return tree


@contextlib.contextmanager
def sharing_parses() -> Iterator[None]:
    """Share one tree per text until the block ends, then drop every one.

    A scope opened inside another adds nothing: the outer scope's trees serve
    it, and only the outermost scope drops them.
    """
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
