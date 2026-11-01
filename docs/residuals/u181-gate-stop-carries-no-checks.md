---
title: A sync pass stopped at the without vocals gate carries no checks on its envelope
found: at the review of #378, U181, 2026-11-01.
issue: no
---

**The mechanism.** `crate sync land` stops at `sync.land.without-vocals` by letting the gate's own decision required refusal leave the verb, and the dispatcher builds that envelope from the cause, so the preflight's ok row for rekordbox and backups and the vocal model row are not on it: `data.checks` is empty. The pass's other stops for a person keep their rows, since they end PENDING through the pass's own envelope.

**Measured cost.** Driven by the review on the real verb, exit 10. The gate screen carries every fact the question is asked over, so a person is told nothing false; the run record does not say the preflight passed before the stop.

**Closes when:** the gate's context carries the preflight rows, or the refusal's detail carries the pass's data the way a stopped step's does. Ledger only.
