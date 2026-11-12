"""A verb module whose import raises argparse's own ArgumentError, a defect of ours."""

import argparse

_SHARED = argparse.ArgumentParser()
_SHARED.add_argument("--x")
_SHARED.add_argument("--x")


def build(parser, entry):  # pragma: no cover - never reached
    parser.set_defaults(_handler=lambda ctx: None)
