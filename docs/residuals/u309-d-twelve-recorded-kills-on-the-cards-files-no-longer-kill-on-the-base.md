---
title: Twelve recorded kills on organize, the outbound module and export no longer kill on the base itself
found: at the kill set replay of #866, U309, 2026-11-22.
issue: no
---

**The mechanism.** The replay before U309's first edit measured, on the base `c919209`, every recorded kill on the card's 34 source files: 639 rows from `killset.py rows`, in six batches. 627 were killed. Twelve recorded no death at all, so `killset.py check` does not hold the branch to them and they are none of U309's: eight read zero, `u142.S11_read_handle_requires_closed`, `u112-b.A6_exported_not_product_made`, `u51-item-derivation.H1_export_item_not_payload`, `r1308.M10_count_unchecked`, `u116.M13_utc_year`, `u227.R12_tree_filter`, `u214.M12_frozen_pairs` and `u226.M18_waited_unformatted`; four broke collection with no death, `r572.A1_album_rule_gone`, `r572.A3_album_over_two_hearts`, `r572.A6_album_despite_unreadable` and `r356-a.A13_reason_never_stored`. Each row's measurement is in `docs/mutation/u309-replay-before-a.md` to `-f.md`.

**Measured cost.** Unknown per row. A zero is a guard whose test was removed, merged or weakened since its table was measured, or a guard written twice so one mutation no longer bites; a collection error with no death is a mutation that breaks an import, which the driver cannot read as a kill. Either way the guard may hold today with no test that proves it.

**Closes when:** each of the twelve is driven on `main`: a test that kills it written where the guard is user facing, or the row recorded as no longer applying with its reason. Ledger only.
