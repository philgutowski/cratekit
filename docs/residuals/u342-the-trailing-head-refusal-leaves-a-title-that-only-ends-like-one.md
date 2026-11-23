---
title: analyze adopt leaves a headless title that only ends like a head, Type-2B-10, as no-head with no cause named
found: at review round two of #994, U342, 2026-11-23.
issue: no
---

**The mechanism.** Review round one made `core/naming.py`, `stamp_head`,
refuse a title carrying a head at its end, by `strip_trailing_head`, whose
pattern takes any ending of a hyphen, a wheel key, a hyphen and one to three
digits, spaced or not. A title that only ends that way, `Type-2B-10`,
`Symphony No. 5 - 3B - 7` or `Area 51 - 9B - 140`, is refused with it, and
`plan_row` names the row `no-head`, the word for a head it could not build.

**Measured cost.** Driven at review round two: a title tag `Type-2B-10`
landed and was left `no-head` on two runs, where round one's code stamped it
`06A - 124 - Type-2B-10`. The row is named and nothing is written or lost; it
keeps having no head. No real title of the shape was measured, and no
producer upstream of staging was driven.

**Closes when:** the refusal reads a trailing head only in the spaced form the
engine writes, or names its own reason so the row says why. Ledger only.
