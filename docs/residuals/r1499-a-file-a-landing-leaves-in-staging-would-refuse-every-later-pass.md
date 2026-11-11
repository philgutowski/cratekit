---
title: A file a landing leaves in staging would refuse every later pass and go
found: at the review of #665, R-1499, round one, 2026-11-11.
issue: no
---

**The mechanism.** `intake/landing.py` and `intake/native.py` leave a file in staging on three rules (no declared sub, an occupied target, an unsupported suffix). Such a file is one no download names, its pass proven, so every later pass and go refuses beside it until a person moves it.

**Measured cost.** Reachability unmeasured: one candidate was driven (round one, d15, an occupied target) and it does not produce the file, the landing took the next free batch name.

**Closes when:** a landing that leaves a file says so, or the readings name a file a proven landing left. Ledger only.
