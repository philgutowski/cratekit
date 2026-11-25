---
title: Every reader that scans the run records parses each kept screen's plan, though only run show reads it
found: at the review of #1080, U961, 2026-11-25.
issue: no
---

**The mechanism.** `gates.RunState.from_json` turns every kept screen's
`shown`, JSON text of up to 64 KiB, into a mapping through `Screen.from_json`
on every load. The readers that scan every run record, `gates.siblings` on
each gated database verb and on `run decide`, `run retire`, the doctor's run
scan and `crate status`, load each record whole and never read a screen; only
`crate run show` does. U961 bounds which records hold one: `gates.record`
drops a gate's screen when it is answered or retired, and `Gates.require`
when it passes, so only a gate still waiting keeps one.

**Measured cost.** Driven at round one of the review: 300 records each
holding a cut screen of 70,026 bytes against the same 300 with none,
`gates.siblings` timed three times each, interleaved on one container: 0.118,
0.123 and 0.105 seconds against 0.013, 0.013 and 0.017, about 0.35 ms per kept
cut screen on every scan. How many unanswered gates with a large plan a real
state directory holds was not measured. Slowness only: nothing is lost or
misread.

**Closes when:** a screen's `shown` is parsed only when `run show` asks for
it, with a timing test holding a scan of records with cut screens to the
ratio of one without, or the count of kept screens in a real state directory
is read at an attended sitting and found small. Ledger only.
