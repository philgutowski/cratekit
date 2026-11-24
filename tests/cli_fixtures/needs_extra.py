"""A verb module whose extras group is not installed.

It imports a module the entry declares in ``extras_modules``; blocking it in a test
reproduces a slim install without uninstalling anything.
"""

import a_third_party_analysis_library  # noqa: F401


def build(parser, entry):  # pragma: no cover - never reached while the extra is blocked
    parser.set_defaults(_handler=lambda ctx: None)
