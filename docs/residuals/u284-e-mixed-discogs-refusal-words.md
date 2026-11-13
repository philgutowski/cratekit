---
title: A sweep mixing a Discogs refusal and a rejected token words every stopped file as the token's, and drops the wait step
found: at the review of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** `tagging.cli._refusal_stop` reads one Discogs note for the
whole sweep, the first non-empty one among the stopped files. In a sweep where
Discogs answers one file with a 403 (read, refused, retryable) and a later file
with a 401 (the token rejected, permanent), the stop says Discogs was not read
since it refused the recorded token, for both, and drops "run the pass or the
sweep again later" although the first file would mend by waiting.

**Measured cost.** Driven at review round two with fakes, a.flac 403 and b.flac
401 beside a refusing Beatport: the only step is recording a working token.
Recording one and running again mends both files; only the wording for the
first is wrong. A real Discogs answering 403 then 401 in one run was not
driven.

**Closes when:** the stop groups its files by why Discogs went unread and says
each group's words and steps. Ledger only.
