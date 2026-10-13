---
title: A set exported under a tracklist's own name cannot follow its INSPIRATION rename
found: at the review of #317, U140, 2026-10-13.
issue: no
---

**The mechanism.** `export set --rename JOB` looks for the set's account
playlist under the INSPIRATION playlist's live name and the names the job
gives: frozen, the posted day's form and the queued day's. A set whose
account playlist was made by `export set TRACKLIST` under the file's stem,
or with `--name`, is recorded under none of those, so the rename refuses
with `export-set-rename-unresolved`. The refusal now says to rename such a
playlist on the account by hand rather than send it to the backfill, which
would make a twin.

**Measured cost.** Not met live: both sets on the live ledger were made by
a set intake under a job's name. A person who exported a set by tracklist
and later renamed its INSPIRATION playlist renames the account playlist and
edits the ledger key by hand.

**Closes when:** the rename accepts the recorded name to start from, or the
author decides the hand step is enough. Ledger only.
