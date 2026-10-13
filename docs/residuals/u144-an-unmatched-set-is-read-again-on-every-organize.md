---
title: A downloaded set with no match, or one the provider would not list, is read from the account again on every organize run
found: at the review of #321, U144, 2026-10-13.
issue: no
---

**The mechanism.** The INSPIRATION parity step (`organize/inspiration.py`, `plan`) skips a set only when INSPIRATION holds a playlist of its name. A set none of whose tracks matched a library row is planned `empty` and nothing is written for it, and a set whose listing the provider refused is planned `unread`. Neither leaves a record, so every later `crate organize` without `--only`, `--report` included, lists that set's tracks from the provider again and asks the library about each one. The rekordbox area therefore makes one provider listing per such set on every full run, and needs the account reachable to plan this step at all.

**Measured cost.** Not driven against the live account. On 2026-10-13 the account held 19 sets, 2 already in INSPIRATION; how many of the other 17 match nothing is the attended sitting's measurement. Each listing is one paced provider read (R-705's pacing), so the cost is seconds to minutes per run, no write and no loss. `--only adopt` and `--only rotate` never plan the step and pay nothing.

**Closes when:** a person decides whether an empty set should be remembered (a record of sets read and found empty, rekeyed when the library grows), or whether re-reading is the right price for noticing a set whose tracks later landed. Ledger only.
