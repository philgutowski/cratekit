---
title: A commit rewrites the masterPlaylists6.xml Timestamp of DEADCA7's nodes to the floor's instant, which depends on the zone
found: at round one of the review of #800, U285, 2026-11-13.
issue: no
---

**The mechanism.** pyrekordbox 0.4.4's `commit()` sets each playlist node's
`Timestamp` in `masterPlaylists6.xml` to the row's `updated_at` whenever the
two differ by more than a second. That is the binding's own behaviour on every
commit, for every node, before U285 as after it: a control push with an
ordinary stamp had its node rewritten to the stored instant. What U285 changes
is the value. A zero dated DEADCA7 row now reads as `FLOOR`, naive local, so a
node whose Timestamp is anything else is rewritten to `FLOOR`'s instant in the
machine's zone (`-62135492400000` in US Eastern, `-62135510400000` at UTC,
`-62135542800000` in Japan) rather than to the stored year 1 instant. The
database rows stay byte for byte; `deadca7_fixtures.written` reads the
database only, so nothing in the suite sees the file.

**Measured cost.** Driven on a fixture whose DEADCA7 nodes carry a 2026
Timestamp: another app's node in rekordbox's XML is changed by Cratekit's
first commit. Whether DEADCA7 writes those nodes at all, and with what
Timestamp, is unmeasured, and whether rekordbox or DEADCA7 reads that value
back for anything is unknown.

**Closes when:** the attended recheck of U285 reads the DEADCA7 nodes'
Timestamps in the copy's `masterPlaylists6.xml` before and after a full
organize on the copy. If a write changes them, a unit keeps the binding's XML
sync off the foreign folder's nodes. Ledger only, since it closes at an
attended sitting.
