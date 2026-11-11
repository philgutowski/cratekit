---
title: Tag folder's --label naming a label that shares its display name with a label carrying a genre gives the folder the other label's genre
found: at the review of #648, U240, 2026-11-11, on main as it stood before the unit.
issue: yes
---

**The mechanism.** `crate label registry rename` accepts a name another label already carries, so two labels can share a display name. `_label_payload` in `src/cratekit/tagging/cli.py` resolves `--label` by identifier and freezes the label's display name; `_label_seam` then resolves that name again among the labels carrying a genre, by name, and finds the other one. U240 fixed the same shape on its own copyright path by carrying each label's genre by identifier; the `--label` path is outside its card.

**Measured cost.** Driven at round two of the review on `main` and on the branch: label Alpha with genre Deep House, label omega renamed to Alpha with no genre; `crate tag folder FOLDER --label omega` warns `tag-folder-label-no-genre`, then writes Deep House on every file with no label tag and asks no catalogue. A wrong genre on audio, reported as the label's, never corrected under fill if empty. Whether the live registry holds two labels sharing a name is unmeasured.

**Closes when:** `--label` freezes the label's identifier and its genre, and the seam answers the folder's label by identifier, with a test of the rename above; or `registry rename` refuses a taken name. Meets the board bar, (a) and (b): a wrong genre is written and reported as the label's.
