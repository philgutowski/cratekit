---
title: The slowest package wide guards left after U258 spend their time in analysis, not in parsing
found: at the build of #687, U258, 2026-11-12.
issue: no
---

**The mechanism.** U258 shares parses inside the tests that asked the same
texts again and again, and that halved the at risk population test. Four of
the slowest guards it was filed against were measured and found to spend their
time elsewhere, so a parse memo cannot reach them:

- `tests/test_rb_writer_guard.py`, the permissive soft delete sweep and the
  reader pin, about 19.5 s and 15 s alone on a four core container. Each runs
  `SoftDeleteNames` and `_soft_delete_reads` over 681 files; the parse is about
  5 s of each. Measured outside pytest, the analysis of one sweep takes 10.3 s
  on trees already parsed. It makes about six passes over each tree, and
  `_laundered_reads` calls `_soft_delete_reads` once per `If` it walks, about
  69,000 calls for 683 files (69,064 and 69,052 in two measurements a few
  commits apart). An iterative `_own_nodes` in the same order was tried
  and measured no faster, 16.0 s against 15.4 s for the recursive one over the
  same analysis, with identical output.
- `tests/test_pool_sizing.py::test_no_module_outside_the_sizing_module_builds_a_process_pool`,
  about 12.5 s, the settling loop in `process_pool_constructions` walking each
  function again on every pass.
- `tests/test_skills_lint.py::test_real_skills_pass_lint`, about 4 s in the
  parallel run and 7.4 s under the profiler, 7.1 s of which is
  `cratekit.cli.build_parser` called 308 times, once per command line, by the
  documented choice in `real_parser` that a failed parse must not leak argparse
  state into the next line's verdict.

Sharing a guard's ANSWERS across tests, rather than its parses, is not safe
here: `tests/test_reserved_causes.py` and `tests/test_review_queue.py`
monkeypatch the guard module's own constants (`EXIT_CODE_MODULE`,
`EXIT_CODE_CLASS`, `MAX_HOPS`, `REVIEW_MODULE`), so an answer cached by text
would be served under the wrong rule.

**Measured cost.** Maintainer facing: about 50 s of a worker's time in each
full run, spread across four workers. Nothing a person using the verbs sees.

**Closes when:** a card of its own rewrites the soft delete analysis as fewer
passes, proved identical on the tree and on planted shapes the way U258's
comparison was, or decides the time is the price of the rule. Ledger only.
