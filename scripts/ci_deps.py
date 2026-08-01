#!/usr/bin/env python3
"""Print dependency specifiers read out of ``pyproject.toml``.

CI installs what this prints. It exists because the source system hand-mirrored
its dependency list into its workflow file and documented the mirror as a
maintenance hazard: adding a runtime dependency to ``pyproject.toml`` and
forgetting the workflow produced a ``ModuleNotFoundError`` at import time in CI,
with nothing pointing at the real cause. Deriving the list removes the class.

Usage::

    python scripts/ci_deps.py            # slim core dependencies
    python scripts/ci_deps.py analysis   # the analysis extra's dependencies

Output is one specifier per line, already quoted for a shell, so a workflow can
do ``pip install $(python scripts/ci_deps.py)``.
"""

from __future__ import annotations

import shlex
import sys
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def read_dependencies(extra: str | None = None) -> list[str]:
    """Return the dependency specifiers for the core, or for one extra.

    Passing an extra returns only that extra's own list, not the core plus the
    extra, because CI installs them in separate steps and wants to see which
    step pulled which weight.
    """
    with PYPROJECT.open("rb") as handle:
        data = tomllib.load(handle)

    project = data["project"]
    if extra is None:
        return list(project.get("dependencies", []))

    optional = project.get("optional-dependencies", {})
    if extra not in optional:
        known = ", ".join(sorted(optional)) or "none declared"
        raise KeyError(f"no extra named {extra!r} in pyproject.toml (known: {known})")
    return list(optional[extra])


def main(argv: list[str]) -> int:
    extra = argv[1] if len(argv) > 1 else None
    try:
        specifiers = read_dependencies(extra)
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 2
    for specifier in specifiers:
        print(shlex.quote(specifier))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
