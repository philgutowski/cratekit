---
title: Two landings from one main that cross the archive point conflict in the archive file as well as the working file
found: at the review of #871, U314, 2026-11-22.
issue: no
---

**The mechanism.** `board.py residuals --land` appends to
`docs/residual-findings.md` and, when the working file passes 5,000 lines,
moves its oldest entries into a new `docs/ledger/R-AAAA-R-BBBB.md`. Two
landings made from the same `main`, one of which crosses the limit, now
conflict in a hunk that mixes the archived entries with the new ones; when
both cross it, the archive file conflicts add and add. The race itself, two
landings taking one number, is older than U314, and METHOD's rule that a
numbering commit merges `origin/main` in and pushes again stands.

**Measured cost.** Driven on a git fixture with the limit at 60 and at 70 by
the review: the conflicts appear as described. How a session resolves the
larger conflict was not measured. A maintainer cost only; no verb a DJ runs
reads the ledger. About one landing in fifty crosses the limit at the
present rate.

**Closes when:** METHOD or `--land` says how to resolve it (take `main`'s
ledger files, delete the conflicting archive, land again, which `--land`'s
refusal of a title already held makes safe), or `--land` refuses to archive
when `main` moved since the fetch. Ledger only.
