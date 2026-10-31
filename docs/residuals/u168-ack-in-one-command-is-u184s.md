---
title: The session's acknowledgment is still two commands until U184's one command mint lands
found: at the plan of #349, U168, 2026-10-31.
issue: no
---

**The mechanism.** U168's brief asks that `crate session ack` with no terminal
and both backup ages under five days mint in one call. U184 (#381) specifies
that same mint as `crate session ack --as session`, with its own scenarios: no
gate opened, no blocked run left, a valid acknowledgment reported rather than
minted again. Building an implicit form here, on the terminal test alone, would
make two rules for one record, so U168 stops at `session ack` and then
`run decide RUN session.ack.backup acknowledged --continue`, which records the
actor `session` with no terminal and mints under U138's age rule.

**Measured cost.** Two commands where the brief asked for one, and no `script`
wrapper or `--actor` to forget. Driven in `tests/test_run_decide_continue.py`.

**Closes when:** #381 lands. Ledger only.
