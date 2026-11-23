---
title: tag set --playlist cannot name a playlist whose name starts or ends with a slash, or a path spelled without the spaces around the separator
found: at the review of #988, U339, round two, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/genre_set.py` `playlist_members` refuses a path that starts or ends with `/` or holds an empty name between ` / ` separators, before walking the tree, and matches names joined by ` / ` exactly. A playlist named `Sets w/` or `/r/ house` therefore cannot be named, a path typed `INBOX/Picks` refuses, and a folder `A / B` beside a folder `A` holding `B` reads as two nodes and refuses.

**Measured cost.** Driven on seeded names in round two; none of the shipped taxonomy's 110 folder and sub paths is affected (0 share a spelling, 8 of 22 bucket names hold the separator and resolve). The rows can still be named with `--row` or `--rows-from`, and the refusal says how a path is written.

**Closes when:** the walk accepts a name whose own text starts or ends with `/` when a live node carries it, with seeded nodes as its test.
