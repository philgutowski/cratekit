---
title: An unreadable kept screen is dropped on load, so a gate it was the only sign of reads as nothing waiting
found: at the review of #1080, U961, 2026-11-25.
issue: no
---

**The mechanism.** `gates._screens_from` leaves out every entry
`Screen.from_json` refuses (not a mapping, a kind it does not know, a field
of the wrong type, `shown` that is not JSON), and the next save writes the
record without it. For most gates the run still says it waits, by its open
gate, an offer with no answer, or an answer bound to another plan, and `run
show` names the gate with `screen_missing`. One gate has no other sign: a gate
with no digest source refused for an option it does not offer leaves no
offer, no open gate and no answer, so with its screen unreadable
`gates.waiting` reads nothing waiting and `run show` carries `gate: null`.
Absence read as evidence of absence, METHOD's first pattern.

**Measured cost.** None observed. Reaching it needs a record whose screen was
damaged or written by a later shape; 0 candidates were driven to produce one,
so its reachability is unmeasured. Nothing is written by the run that reads
as clean; continuing it refuses at the gate again and keeps a fresh screen.

**Closes when:** an unreadable entry is kept as written and its gate named
with `screen_missing` saying the kept screen could not be read, with a test
over the unknown option case above. Ledger only.
