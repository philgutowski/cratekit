---
title: The set rename's guard reads the mark record and not the title, so after a strip whose rename failed it renames a set still carrying the prefix
found: at the review of #671, U242, round two, 2026-11-12.
issue: no
---

**The mechanism.** `export set --rename` refuses while a legacy archive
prefix mark stands, and since U242 a later strip record supersedes that mark.
The strip records each rename before it makes it, so a rename the provider
then refused leaves a strip record over a title still `DOWNLOADED <old>`. The
review drove it: `_standing_mark` answered none, and the rename gate showed
and applied `<old> -> <new>` over the prefixed title.

**Measured cost.** None measured: the end state equals a whole strip then a
rename, and the set stays taken by its id.

**Closes when:** the guard reads the title the account lists, or the strip
records its rename only once it lands. Ledger only.
