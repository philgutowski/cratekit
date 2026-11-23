---
title: A restore's gate and answer name no audio file it rewrites, nor the sessions their values came from
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** The files' half of a restore is planned under the gates,
after the question is asked, so `restore.run.confirm` shows only "Restore
this session, discarding everything after it?" and its digest covers no
file. The answer gives counts in `file_tags` and the default output reads
`restore.run: ok`. The files read include those of later sessions the discard
flag never named (one that committed nothing needs no discard). A title tag
edited by hand after the adopt is put back over, counted read back, and the
edited value is kept nowhere.

**Measured cost.** Driven at both review rounds: the gate envelope and the
real and dry answers read in JSON and in the default output. Nothing false is
said; the files a person is about to have rewritten are unsaid.

**Closes when:** the gate, or the dry run's items, list each file and the
session its value came from, and the run keeps the values it overwrote.
Ledger only.
