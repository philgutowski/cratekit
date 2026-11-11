---
title: Tag folder's per file report lists a never attempted file, and a finished file whose report cannot be read, as tagged not at all with no reason
found: at the review of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** `_summary` in `src/cratekit/tagging/cli.py` lists every item of the job without a committed report as way `none`, with `failed` empty when the item carries no cause. A cancelled or parked sweep's never attempted files, and a finished file whose committed report is unreadable, read alike as files nothing tagged.

**Measured cost.** Driven at round two: a sweep cancelled before it ran reads "Of 3 file(s) ... 3 none", true of each file but unable to tell never run from nothing found; a report overwritten by hand made a file carrying its label's genre read as none, a producer nothing in `src` was found to make (only the staging directory is ever removed).

**Closes when:** a row carries the item's state, so a pending or cancelled item reads as not run, and a done item with no readable report as unread. Ledger only.
