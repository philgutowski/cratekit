---
title: A continued sync pair answers only what it wrote itself, not what the stopped command made or queued
found: at the review of #500, U210, 2026-11-05.
issue: no
---

**The mechanism.** A ceiling stop is a park, and a parked envelope carries no
totals. The continue's OK envelope counts only its own command's writes
(`created_playlists`, `queued_jobs` and the rest in `sync_pair`,
`sync/pair_cli.py`), so the playlists the stopped command made and the jobs it
queued appear in no answer's totals. The continue's message says how many
pairs finished earlier in the run, and `totals.finished_before` counts them.

**Measured cost.** Driven at round one (S7): a job queued before the stop was
in `crate job list` and not in the continue's `queued_jobs`. Nothing is lost;
the report is incomplete.

**Closes when:** each pair's done step records what it made and queued, and the
continue's totals add the earlier commands' to its own. Ledger only.
