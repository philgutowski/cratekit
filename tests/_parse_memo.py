"""One parse per source text per test process, for the guards that sweep the package.

A guard that walks every module asks ``ast.parse`` for each file it reads, and
several guards walk the same files in one process. Measured on 2026-11-12 over
five of them in one process, before this module existed: ``ast.parse`` called
5,934 times for about 660 source files, 13 s in the compiler alone (U258).
The answer to a parse depends on nothing but the text, so the text is the key.

KEYED ON THE TEXT ITSELF, never on a path, a modification time or a size. A
file edited during a run reads back as a different string, which is a
different key, so it is parsed afresh and an answer about the old text can
never be served for the new one. Two files holding the same text share one
tree, which is correct, because the tree is a function of the text alone.

READ ONLY BY CONTRACT, and the contract is driven rather than trusted. One
tree is handed to every guard that asks for that text, so a guard that wrote
to a node, an annotation, a parent pointer, a rewritten field, would leak that
write into every guard after it, in whatever order the workers ran them.
``tests/test_parse_memo.py`` runs every guard question the sweeps ask over one
shared tree in both orders and compares the tree with a fresh parse of the
same text, node by node and attribute by attribute. A guard that needs to
annotate nodes parses its own copy with ``ast.parse`` and never asks here.

Only the default parse is memoised: ``mode="exec"``, no type comments, no
feature version. A caller that needs another parses for itself.

THE MEMO IS NOT BOUNDED BY COUNT, and that is deliberate. A sweep visits the
files in one sorted order, so a cache smaller than the sweep evicts each tree
just before the next sweep asks for it and saves nothing. What it costs was
measured: every tree of the 681 files the guards sweep (``src``, ``scripts``
and ``tests``) is about 720 MB in one process. The bound below is on the text
held, sized to about twice what the swept trees hold today, and crossing it
empties the memo rather than serving anything stale.
"""

from __future__ import annotations

import ast

#: The most source text, in characters, whose trees are held at once. The swept
#: trees held 22.9 million characters on 2026-11-12, so this is about twice
#: that. Crossing it clears the memo: correctness never depends on a hit.
TEXT_BUDGET = 48_000_000

_TREES: dict[str, ast.Module] = {}
_held = 0


def parsed(source: str) -> ast.Module:
    """The tree ``ast.parse(source)`` gives, parsed once per distinct text.

    The caller must not mutate the tree it is handed: the same object goes to
    every other caller asking about the same text.
    """
    global _held
    tree = _TREES.get(source)
    if tree is None:
        tree = ast.parse(source)
        if _held + len(source) > TEXT_BUDGET:
            _TREES.clear()
            _held = 0
        _TREES[source] = tree
        _held += len(source)
    return tree


def forget() -> None:
    """Empty the memo, for a test that has to count parses from nothing."""
    global _held
    _TREES.clear()
    _held = 0
