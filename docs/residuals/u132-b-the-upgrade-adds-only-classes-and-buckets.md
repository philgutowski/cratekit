---
title: The taxonomy upgrade adds classes and buckets and no other section the shipped template gained
found: at the build of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** `core/taxonomy_upgrade.py` appends missing `[[sub_class]]`
and `[[bucket]]` entries and raises `schema_version`. A top level table the
shipped template gained (`[long_tracks]`, `[intake_old]`, `[inspiration]`), a
row it gained in an existing table (`[vocabulary.deezer]`, `[[fuzzy]]`,
`[[label_gate.rule]]`), and a child table it gained under a bucket the copy
already declares (a `[[bucket.formerly]]`) are not added, and doctor's
`taxonomy.schema` does not name them. `taxonomy.active` names a gained top
level section only for a copy with an origin record (R-689).

**Measured cost.** Not driven against a copy missing one of those. A verb that
needs such a section refuses or skips by name where it was written to (the
rotation, the long tracks playlist), so nothing is filed wrongly; the person is
told by that verb and not by doctor.

**Closes when:** the upgrade and doctor's check cover the other sections, each
with the same never change an entry rule, or a decision records that a person
adds those by hand. Ledger only.
