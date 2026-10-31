---
title: Rehearsal records accumulate in the installation state with nothing that prunes them, and every live landing gate reads them all
found: at the review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** Each finished rehearsal writes `rehearsals/<run>.json` under the installation state, holding its digest and plan lines, and `rehearsal.latest` reads every record on every native landing gate to find the newest of the same folder and batch. Nothing removes a record.

**Measured cost.** None at today's counts: a few records a sitting, each a few hundred kilobytes for a large batch. A slower gate screen after many hundreds.

**Closes when:** records older than the run retention, or beyond the newest few per folder and batch, are removed when a new one is written. Ledger only.
