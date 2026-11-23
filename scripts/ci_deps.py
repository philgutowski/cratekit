#!/usr/bin/env python3
"""Print dependency specifiers read out of ``pyproject.toml``, so CI never mirrors them by hand.

Usage::

    python scripts/ci_deps.py            # slim core dependencies
    python scripts/ci_deps.py analysis   # the analysis extra's dependencies

One raw specifier per line, deliberately UNQUOTED: consume it with ``xargs``,
never with command substitution, which does not remove quotes::

    python scripts/ci_deps.py | xargs -r python -m pip install
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def read_dependencies(extra: str | None = None) -> list[str]:
    """Return the core's dependency specifiers, or only one extra's own list."""
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
        print(specifier)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
