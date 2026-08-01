"""A verb module with a defect of our own: it imports something that is not there.

The missing name is NOT in the entry's extras group, so the shell must let this
propagate rather than tell the user to install an extra. A user cannot fix our
typo by installing anything, and pointing them at a package manager hides the
real failure behind a false one.
"""

import cratekit.this_module_does_not_exist  # noqa: F401


def build(parser, entry):  # pragma: no cover - never reached
    parser.set_defaults(_handler=lambda ctx: None)
