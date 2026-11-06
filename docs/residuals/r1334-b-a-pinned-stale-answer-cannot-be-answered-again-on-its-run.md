---
title: A pinned stale answer cannot be answered again on its run, since a decide never replaces the pin
found: while building #567, R-1334, 2026-11-06.
issue: no
---

**The mechanism.** U161's pins are recorded while a gate is open and never
replaced once it is answered, and `gates.record` does not touch them. After a
stale refusal over a pinned fact (the database file a native landing names),
a second `crate run decide` records the same digest beside the old pin, so
every resume of that run is refused stale over the same fact again. R-1334's
screen is deliberately not carried on this refusal, since a decide after it
cannot apply anything.

**Measured cost.** None to the library: nothing is written. A person who
answers again on the run is refused again, and has to start a fresh run,
which the remedy, replan then decide, already says. Read from the source and
the unit tests in `tests/test_gate_stale_screen.py` and `tests/test_gate_pins.py`;
not driven through a verb.

**Closes when:** a pinned stale refusal either says a fresh run is the only
way on, or a decide after it records the pins the refusing run read, shown on
its screen. Ledger only.
