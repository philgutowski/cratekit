---
title: The menu bar app's minute refresh keeps a run record for every crate status call, and status slows as they grow
found: at the plan of #1085, U966, 2026-11-25.
issue: yes
---

**The mechanism.** The brief asks the app to refresh every minute and when
its menu opens, and the app runs `crate --output json status` to do it. The
dispatcher saves a run record for every verb that finishes, `status`
included (`cli/__init__.py`, `gates.save(state)` after the handler), and run
records are never pruned (`cli/gates.py`). `crate status` then lists and
loads every record twice, once for its own run lines and once for the glance
(R-2084). So the app grows the directory it reads by one record a call, and
each call reads all of them.

**Measured cost.** Driven on this container with the real `crate` over a
synthetic installation: three `crate --output json status` calls left three
new run records of 259 bytes each. At one call a minute that is 1,440 records
a day, about 370 KB of text and one file each. U960's review measured the
verb at 0.40 to 0.69 seconds with 200 records and 1.39 to 1.54 seconds with
20,000, which the minute refresh reaches in about two weeks. Past that the
time is unmeasured; if it keeps growing in step, the app's 30 second timeout
is reached in months, and from then on every refresh fails and the icon reads
`fail` for a reason that is the app's own. `crate run show` and anything else
that lists runs carries the same records. Not measured on a Mac.

**Closes when:** a polling read keeps no run record (the dispatcher skips the
save for a verb the registry declares as a read with no gate, or `status`
takes a flag the app passes), and `crate status` loads the records once
(R-2084). An engine card, outside the app's files. It earns an issue because
the app as specified produces it, and a status that the app can no longer
read in time is a workflow that cannot finish.
