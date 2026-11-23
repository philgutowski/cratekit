"""A listed module answering for its parts, each loaded when a name of it is first read (U331).

A feature package may import only the named interface
(``tests/test_import_rules.py``), so a core module off that list is reached
through the listed module it is a part of. Importing every part with its
module would load the process pool's machinery with the job queue on every
command, so the module binds ``__getattr__`` to :func:`answering` instead.

**THE NAME IS READ OFF THE PART EACH TIME, NEVER COPIED**, so there is one
binding: a test that patches the part is seen through the module, and nothing
drifts between two spellings of one function.

**THE TABLE IS A LITERAL**, because the import rules read it: the names in it
are the names the module answers for, and no others. A name the part does not
hold fails where it is read, so ``tests/test_core_parts.py`` reads every one.
A part's names are a sequence, or a mapping ``{offered: held}`` where a name
means nothing without its module's and so carries it (``tags.DRIFT_VARIABLE``).

Layer: infrastructure. Imports nothing of this package.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable, Mapping, Sequence
from typing import Any


def answering(
    module: str, parts: Mapping[str, Sequence[str] | Mapping[str, str]]
) -> Callable[[str], Any]:
    """The ``__getattr__`` of ``module`` for ``{part: its names}``, each part beside it."""
    package = module.rpartition(".")[0]
    table = {
        part: dict(names) if isinstance(names, Mapping) else {name: name for name in names}
        for part, names in parts.items()
    }
    home = {
        offered: (f"{package}.{part}", held)
        for part, names in table.items()
        for offered, held in names.items()
    }

    def read(name: str) -> Any:
        if name not in home:
            raise AttributeError(f"module {module!r} has no attribute {name!r}")
        part, held = home[name]
        return getattr(importlib.import_module(part), held)

    #: ``{part: {offered: held}}``, what the suite reads to check every name.
    read.parts = table  # type: ignore[attr-defined]
    return read


__all__ = ["answering"]
