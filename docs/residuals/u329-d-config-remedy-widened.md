---
title: config.Remedy is the whole remedy vocabulary since U329, so a configuration failure is no longer held to its six tokens
found: at review round one of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** U329 gave the six configuration remedy tokens one home by
making `core.config.Remedy` the canonical `core.exit_codes.Remedy`,
re-exported, rather than a subset enum of its own. So
`config.Remedy("quit-rekordbox")` is accepted where the base refused it,
`tests/test_config.py`'s `isinstance(kind.remedy, config.Remedy)` holds for
any canonical token, and `core.config` left the subset walk in
`tests/test_cli_contract.py`. A subset read off the canonical text was
driven first and broke the reserved causes guard's static enum rule (R-1905),
whose module may import only `ast` and `re`.

**Measured cost.** None to a user: for all six tokens `str`, `repr`, JSON, the
rendered fix line and the cause text are byte identical on base and head, and
`src` holds no iteration, `isinstance` or constructor on `config.Remedy`.
What is lost is a statement of which remedies a configuration failure may
name.

**Closes when:** a test names the remedies each configuration failure carries,
or the static enum rule reads a member written as another enum's value and
config declares its subset again by reading it. Ledger only.
