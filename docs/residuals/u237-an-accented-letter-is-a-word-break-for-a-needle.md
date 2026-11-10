---
title: A letter outside a to z is a word break when a needle is matched, so a needle still confirms a longer accented name
found: at the review of #645, U237, 2026-11-10.
issue: no
---

**The mechanism.** `fold_label` (`src/cratekit/label/verify.py`) turns every character outside a to z and 0 to 9 into a space before `labels_match` compares whole words, so an accented letter splits a word: `Rawax` confirms `Rawaxé`, `Sue` confirms `Sueño`, `Lumi` confirms `Lumière Records`, and `Cliché` never confirms `Cliche Music`. `Sueño` is a live label (`docs/cutover.md`).

**Measured cost.** Measured true on main and on the branch alike, so not a regression; it is the part of U237's goal that stays open for names with a letter outside a to z. Folding accents to their base letter in `fold_label` would close it, but `fold_label` also decides artist name equality in `tidal_catalogue`, so it is its own change.

**Closes when:** `fold_label` folds an accented letter to its base letter (or keeps letters whole) and every caller is checked against it. Ledger only.
