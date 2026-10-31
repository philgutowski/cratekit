---
title: A file with two artists or two genres lands its first value alone
found: at the review of #344, U163, 2026-10-31.
issue: no
---

**The mechanism.** `native._word` takes a tag's first value in every container,
so a multi-value artist or genre frame (what Picard and beets write for a
collaboration) lands the first artist or genre and drops the rest. Before the
review round the ID3 reader's NUL joined value was minted whole.

**Measured cost.** The second artist is absent from rekordbox's Artist column
for such a file until somebody edits it; filing reads the first genre, which
is the one adoption would match.

**Closes when:** rekordbox's own rendering of a multi-value frame is read on a
copy and the landing joins the values the same way. Ledger only.
