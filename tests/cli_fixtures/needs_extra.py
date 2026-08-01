"""A verb module whose extras group is not installed.

The import below names a top-level third-party module that the entry declares in
``extras_modules``. Blocking it in a test reproduces a slim install exactly,
without uninstalling anything.
"""

import a_third_party_analysis_library  # noqa: F401


def build(parser, entry):  # pragma: no cover - never reached while the extra is blocked
    parser.set_defaults(_handler=lambda ctx: None)
