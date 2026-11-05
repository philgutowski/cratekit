---
title: A version shaped tag on a side branch inside a release pair refuses plan over that pair, with advice that drops part of it
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** `refuse_a_crossed_tag` in `scripts/release.py` refuses any
`v*` tag reachable from `--tip` and not from `--since` that is not at the tip,
including one on a side branch merged into the range. Its advice, `--since`
that tag, would start the range at the branch point and drop what came before.

**Measured cost.** Driven by the round two reviewer in a throwaway repository,
v0.2.5 tagged on a feature branch commit then merged: `plan --since v0.2.0
--tip v0.3.0` is refused. Not produced on the real repository, where all six
tags sit on `main`'s release commits.

**Closes when:** the scan counts only tags on the first parent line of the
range, or the refusal names the side branch. Ledger only.
