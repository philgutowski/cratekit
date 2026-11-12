"""A verb module that fails at import with something other than an ImportError."""

raise ValueError("a defect of our own, raised while the module is imported")


def build(parser, entry):  # pragma: no cover - never reached
    parser.set_defaults(_handler=lambda ctx: None)
