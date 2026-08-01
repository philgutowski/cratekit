"""The ``crate`` entry point.

PLACEHOLDER (U1). This module exists so the console script declared in
``pyproject.toml`` resolves from the first commit and the cold-install job can
prove the entry point works. U5 replaces it with the real shell: the static
module registry with lazy imports, the versioned structured-output envelope,
the named-decision gates, and the single reserved exit-code vocabulary.

Nothing here should grow features. Anything added before U5 lands would have to
be retrofitted onto contracts that do not exist yet, which is the exact cost U5
is sequenced early to avoid.
"""

from __future__ import annotations

import sys

from cratekit import __version__

_PLACEHOLDER_HELP = f"""crate {__version__}

Cratekit is not yet wired up. The CLI shell, module registry, output envelope,
and gate contract land in U5; verbs register against them afterwards.

  crate --version    print the package version
  crate --help       print this message
"""


def main(argv: list[str] | None = None) -> int:
    """Print help or the version. Returns a process exit code."""
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] == "--version":
        print(__version__)
        return 0
    print(_PLACEHOLDER_HELP, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
