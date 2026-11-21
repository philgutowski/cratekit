---
title: The suite reads "every remaining verb still builds" from source, and an import made by a function a builder calls is not followed
found: while building #853, U296, 2026-11-21.
issue: no
---

**The mechanism.** Rule four of `tests/test_import_rules.py` asks that with a
toggle off and its homes unimportable every remaining verb still builds.
`refactor_measure.dangling` answers from source text: a verb loads what its
module's import runs, plus the imports written in its builder's own body. An
import inside a function the builder calls, or one made through
`importlib.import_module`, is not seen, and an import guarded by `try` and
`except ImportError` is read as one that runs. The driven reading, each toggle's
homes blocked in a fresh interpreter and every remaining verb imported and
built, is `scripts/refactor_measure.py imports --drive` and is not in the
suite.

**Measured cost.** On `ff8e5ec` the two readings agree on every toggle, 159
dangling verbs in all, and the one verb the first static reading missed
(`intake.set`, whose builder imports `intake.set_playlist`) is what the
builder's own imports are followed for. The driven reading took 12 seconds
by the author's clock and 15 to 16 by the review's on the four core
container, the whole command 18 to 19, against a budget of ten seconds for
every new check together, which is why the suite does not run it. So a verb can
come to dangle through a builder's helper with the suite green: the review
drove it, a helper called by `session.ack`'s builder importing `skills`, and
the real tree test passed while the driven reading named the verb. None of
the 120 landed verbs is that shape today. The other way, a guarded import the
review planted was called dangling by the suite and built by the driven
reading; the tree holds no such import, and rule three would fail it first.
Maintainer facing: no verb's behaviour changes, since a toggle that is off
does not make a package unimportable on a real install.

**Closes when:** the final audit of U290 (#872) runs `imports --drive` and
records that the two readings still agree, or the driven reading is made
cheap enough to join the suite. Ledger only.
