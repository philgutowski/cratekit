---
title: The campaign's follow step gives the another spelling reason for any follower whose file word is not the answer's
found: at round two of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** `_rows_step` in `cli/verbs/tag_campaign.py` holds out a follower whose file word differs from the genre its answer filed, and names it `file-carries-another-spelling`. A follower whose file the alias walk never reached, so its file still carries the word exactly, gets the same reason. Round two produced it with a row whose path climbs out of the library root through `..`; a file at an absolute path outside the root is excluded by the census instead.

**Measured cost.** A false reason in the report; its advice, to retag the file by hand, still works. Reachability on a real library, through a prefix rule that points outside the root, was not driven.

**Closes when:** the reason tells a file the walk never reached apart from a file carrying another spelling. Ledger only.
