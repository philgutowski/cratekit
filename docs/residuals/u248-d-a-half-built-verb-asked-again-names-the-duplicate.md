---
title: A verb whose builder failed part way, asked again on the same parser, names the duplicate it left and not its own defect
found: at the review of #677, U248, 2026-11-12.
issue: no
---

**The mechanism.** `_Unbuilt.build` in `src/cratekit/cli/__init__.py` counts a
verb built only once its builder returned, so a builder that raised part way is
asked again the next time the same parser selects it. The arguments it added
before it raised are still on the subparser, so the second attempt fails on a
duplicate option, which `build` reports as a `RuntimeError` naming that
duplicate rather than the builder's own first error.

**Measured cost.** None to a person. Driven by review round two with a fake
builder that adds an option and then raises: the first parse names its error,
the second names the duplicate. No production path parses twice on one parser:
`cli.run` and `cli.dispatch` build a new one per call, and every landed builder
runs cleanly in the eager build.

**Closes when:** the subparser is rebuilt fresh for a second attempt, or the
first error is kept and raised again. Ledger only.
