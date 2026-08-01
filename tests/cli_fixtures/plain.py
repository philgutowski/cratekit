"""A minimal working verb module, used to prove the ordinary build path."""


def build(parser, entry):
    parser.set_defaults(_handler=lambda ctx: ctx.envelope(data={"checks": [], "summary": {}}))
