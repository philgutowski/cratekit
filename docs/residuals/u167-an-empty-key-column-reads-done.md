---
title: analyze check reads done when the Key column is empty on every analysed row
found: at the review of #348, U167, 2026-10-31.
issue: no
---

**The mechanism.** `rekordbox_check.Check.verdict` judges keys only by
agreement, over rows keyed on both sides. Rows with the Key column empty are
unkeyed, so with every analysed row unkeyed nothing is compared, the floor is
None, and the verdict falls to done with exit 0. The brief's verdict rule names
only variable grids and agreement far below the record, so this follows the
brief, and the `check.key_column` check says how many rows are empty, as
`info`.

**Measured cost.** Driven by the review: five rows landed and visited with no
key, exit 0. A skill reading only the status moves on with no key written. The
producer, a visit with rekordbox's key analysis off, was not driven against
rekordbox; U157's brief names KEY off as Phillip's standard setting, so whether
an empty Key column is wrong or expected after his visit is itself open.

**Closes when:** the attended visit records whether the Key column is filled
after Phillip's standard settings, and the verdict is changed to match, or this
is closed as expected. Ledger only: the report names the empty rows, so
nothing false is said.
