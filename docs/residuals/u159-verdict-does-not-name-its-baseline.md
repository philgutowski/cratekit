---
title: A battery verdict does not name the baseline it was read against, so a baseline on the same commit clears a release
found: at the review of #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** `cloud_battery.py compare` records `<sha> clean` for the
commit it measured, and `release.py cut` reads only that. A fresh container
that measures its baseline on the release commit and compares on the same
commit gets a vacuous clean: every failure is the baseline's.

**Measured cost.** Not driven to a wrong release. The release skill measures
the baseline only when none exists on the machine, which is where it bites.

**Closes when:** the verdict carries the baseline's commit and `cut` refuses a
verdict whose baseline is the commit it clears. Ledger only.
