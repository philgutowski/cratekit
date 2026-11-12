---
title: Three of U246's hoisted sets are built on paths that never read them, and two hash a value main never hashed there
found: at the review of #675, U246, 2026-11-12.
issue: no
---

**The mechanism.** Hoisting a set above its comprehension builds it even when
the comprehension tests nothing. `sync/pair_calls.py` builds `held_before` and
`held_after` when `removes` or `adds` is empty, and `sync/pair_cli.py` keeps an
`else set()` arm for `started` that no reader reaches when `folded` is false.
Two of them also hash their source before main did: `InvocationResult` in
`acquire/adapter.py` with requested keys and no results, and the inspiration
`assert_read_back` with live rows and no planned members. Given an unhashable
value there (round one passed a list as a requested key), main accepted it and
the branch raises `TypeError`.

**Measured cost.** None reachable found. Two producers were read and neither
yields an unhashable value: `request_for` takes the key from a text column and
`set_playlist.read_back` builds `str(row[0])`. Neither was driven through a
verb. The wasted builds are over one playlist's length.

**Closes when:** each set is built only where its comprehension runs, or a
test pins that every producer yields strings. Ledger only.
