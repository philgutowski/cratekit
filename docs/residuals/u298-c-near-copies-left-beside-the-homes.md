---
title: Three near copies stand beside the homes U298 gave their helpers, each differing in shape
found: during U298 and its review, 2026-11-21.
issue: no
---

**The mechanism.** U298 replaced exact copies only, as its brief says. Three copies differ in shape and were left:

- `modules/outbound/shell.load_config` takes its origin as one string where `cli.output.load_config` takes a sequence. It gives the same cause for `(origin,)`.
- `_rollback_quietly` in `sync/removed.py` (landed by U288 beside this card) and in `write/metadata_cli.py` swallow a failed rollback without the warning `write.trees.rollback_quietly` logs.

**Measured cost.** None to a run. Three helpers keep a second spelling until their area cards fold them in. The rollback pair differs in a log line, so folding them changes what a log shows and is a listed UX cleanup.

**Closes when:** the outbound, sync and write area cards fold each into its home, naming the rollback's added log line if they take it. Ledger only.
