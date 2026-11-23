---
title: The writer parts guard reads only refusals raised through the two factories, so a part's own refusal route is outside it
found: at review round one of #952, R-1890, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_rb_writer_parts_guard.py` applies the beat grid
suite's refusal scan to the writer's parts, and like that scan reads calls of
`_unavailable` and `_running`. A part's `_node_refusal("node-change-unconfined",
...)` at `rb_nodes.py`, a factory bound to a local name first, and a bare
`raise Exception(...)` each passed it (driven by the review).

**Measured cost.** None to a person: the population pins in
`tests/test_reserved_causes.py` failed on the unreserved slug through
`_node_refusal`, so a wider guard holds that route; the bare exception is the
same limit the beat grid suite's scan has. The file's docstring now says what
it reads.

**Closes when:** the writer's refusal scan reads every `CratekitError` a part
constructs, or the parts are held to raising through the two factories.
Ledger only.
