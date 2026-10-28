---
title: A node the native label filing makes goes last among its siblings, where the bridge puts a label first and a year newest first
found: at the plan of #337, U156, 2026-10-28.
issue: no
---

**The mechanism.** `rbxml.insert_catalog_folder` puts a new label folder first
under Record Labels and a new year playlist before the first held year that
sorts below it, so the bridge's tree reads newest first. The binding's
`create_playlist` takes a `seq`, and an insert at a position renumbers every
sibling after it, a write to rows the landing otherwise never touches and
that the guarded commit has not been asked to admit. `intake/label_filing.py`
passes none, so a node it makes goes last: a label folder it makes takes its
years newest first, since it makes them in that order, and a year added to a
label folder that already held years sits below them.

**Measured cost.** Driven in `tests/test_intake_land_labels_native.py`: a
2022 playlist added to a folder holding 2021 and 2019 reads after both. Order
only, nothing lost, and rekordbox sorts a folder by name on a click.

**Closes when:** the writer places a new node by the bridge's rule, with the
renumbered siblings admitted by the guarded commit and pinned by a test, or
the order is accepted as rekordbox's own and this is closed. Ledger only.
