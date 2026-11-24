---
title: The title differential's corpus is the tagging tests' string constants, so a test trim moves it
found: at the review of #984, U335, 2026-11-24.
issue: no
---

**The mechanism.** `scripts/title_differential.py` builds its corpus from every short string constant of fifteen tagging test files. A trim that folds tests or renames a fixture's file names changes that corpus: on this branch `corpus()` read 2,248 strings on the base and 2,318 on the head, 8 lost (among them the file names "a dance record" and "a disco record" of the remap fold) and 78 gained, mostly parametrize ids.

**Measured cost.** None measured: the script is a differential research tool run by hand, exits 0 always, and is not a verb. A later run compares a slightly different corpus than an earlier one.

**Closes when:** the corpus is a fixed data file the script owns, or the record of any run names the commit its corpus was read at. Ledger only: maintainer facing.
