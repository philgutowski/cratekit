---
title: A night pass waiting at the acknowledgment leaves the status glance's attention at ok
found: at review round one of #1079, U960, 2026-11-25.
issue: no
---

**The mechanism.** `attention` reads `gate` from the run records with an
open gate. A night pass that stopped at `waiting-at-acknowledgment`, or at
plain `waiting`, holds no open gate, so `attention` can read `ok` while
`night.outcome` says the pass waits on a person. The brief's precedence
names no night word, and the glance carries the outcome for the app.

**Measured cost.** Read, not driven: the producer, a night pass stopping at
the acknowledgment, was not driven. The icon would read `ok` while a pass
waits; the glance's `night` key says so to anything that reads it.

**Closes when:** the menu bar app's card (#1085) decides whether a waiting
night outcome raises the icon, and if so the glance's `attention` takes it.
Ledger only.
