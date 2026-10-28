---
title: A folder named Analyze under INBOX gets a plain Analyze playlist made beside it
found: at the first review of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** `native.analyze_playlist` takes only a live, ordinary
playlist (attribute 0) named `Analyze` directly under the intake root, so a
folder of that name is passed over and the first landing makes the queue
playlist beside it. INBOX then shows two nodes named Analyze, one a folder.

**Measured cost.** Driven with a folder row inserted from SQL, so the
producer, a person making that folder in rekordbox, was not driven. The
landing writes nothing into the folder; the visit would see two entries of
one name and has to pick the playlist.

**Closes when:** the landing refuses, or names the queue otherwise, when a
non playlist node holds the name, or the attended sitting confirms no such
folder exists. Ledger only.
