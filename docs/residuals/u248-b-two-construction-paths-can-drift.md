---
title: The lazy and the eager parser build a verb by two copies of the same steps, which can drift
found: at the review of #677, U248, 2026-11-12.
issue: no
---

**The mechanism.** `cli.build_parser(eager=True)` keeps the construction loop
as it stood before U248, and `_Unbuilt.build` in `src/cratekit/cli/__init__.py`
does the same import, stub and builder steps for one verb when argparse selects
it. They already differ in one deliberate way: a builder's own
`argparse.ArgumentError` leaves the lazy path as a `RuntimeError`, because it is
raised inside argparse's parse, and leaves the eager path as itself. A later
change made to one copy and not the other would be caught by
`tests/test_cli_lazy.py` only where it changes printed help or a parse result.

**Measured cost.** None to a person: every command uses the lazy path, and the
eager one is used by the docs walk in the suite and by CI's cold install. Kept
twice on purpose, so the eager loop stays an independent oracle for the parity
tests rather than the code under test asked twice.

**Closes when:** the two are made to share the one step, with the parity tests
moved to a captured oracle, or the eager path is retired. Ledger only.
