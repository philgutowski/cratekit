"""A verb module whose builder declares one option twice, a defect argparse refuses."""


def build(parser, entry):
    parser.add_argument("--first")
    parser.add_argument("--first")
