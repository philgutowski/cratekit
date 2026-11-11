---
title: A file's label tag reaches a label by identifier only when no label's name or name slug is the tag, so an old name another label's name slug carries goes to that label, and an identifier that is no slug is never reached
found: at the review of #658, R-1476, 2026-11-11.
issue: no
---

**The mechanism.** `_label_seam` in `src/cratekit/tagging/cli.py` reads a tag as a display name, then as a display name's slug, then as the identifier its own slug is, the last for a renamed label's old name. The engine helper `tag.tag_folder` in `src/cratekit/tagging/tag.py` takes `label` and not the new `folder_genre`, so a caller of it would answer `--label` as a name.

**Measured cost.** Driven at round two: Alpha with a genre renamed Zed, Omega renamed `Alpha!` with another genre, a file tagged `Alpha` takes Omega's genre where main gave Alpha's; two renames are needed and which label is meant is undefined. A tag equal to an identifier that is not slug shaped, such as one carried in a hand edited registry file, answers nothing where main answered by exact identifier; `add` and `adopt` both make identifiers with `slug`, so no verb was found to produce one. `tag.tag_folder` has no caller in `src`.

**Closes when:** the registry records a label's former names, so an old name is matched as itself, and `tag.tag_folder` takes `folder_genre` or is removed. Ledger only.
