---
title: a crate organize selection of listing steps only still asks each area's gate and shows the account's writes fact
found: at the review of #314, U137, 2026-10-12.
issue: no
---

**The mechanism.** `crate organize --only yours` (or `--only record-labels`)
plans only steps that write nothing, and each planned area still asks its
explicit gate, because U112 asks an area with nothing to do. The account
area's `writes` fact, "add only: folders are created and playlists filed and
prefixed", is set whatever the selection, so a narrowed area that can write
nothing still says what the whole area writes.

**Measured cost.** Driven in `test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
with `--report`, which asks nothing. Without `--report` a person answers two
gates through `crate run decide` for a run that writes nothing; the gate's
own "nothing to do" fact says so. Nothing false is written and no write is
missed.

**Closes when:** an area whose selected steps are all listings is planned and
reported as `--report` would, asking nothing, and the `writes` fact names
only what the selected kinds can write. Ledger only.
