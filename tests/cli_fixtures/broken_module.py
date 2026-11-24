"""A verb module with a defect of our own: it imports something that is not there.

The name is NOT in the entry's extras group, so the shell must let this propagate:
no install fixes our typo, and naming a package manager hides the real failure.
"""

import cratekit.this_module_does_not_exist  # noqa: F401


def build(parser, entry):  # pragma: no cover - never reached
    parser.set_defaults(_handler=lambda ctx: None)
