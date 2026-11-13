---
title: A drive killed outright leaves its token file until the next provider session scope on the account
found: at U274, 2026-11-13.
issue: no
---

**The mechanism.** A drive of a download job now holds its private token file
for every track it acquires, not for one. SIGINT and SIGTERM are recorded by
the engine and the drive closes normally, and an exception closes it too, so
the file goes on each of those. A SIGKILL, a power cut or a crash of the
interpreter runs no code, so the file stays in its private directory (0700,
the file 0600) until the next `materialised_session` on the same account
sweeps it: any later download, catalogue or account open.

**Measured cost.** Driven by the review with a real `kill -9` against a live
scope: the directory stayed, and the next scope removed it. Before U274 the
same kill left the same file; the window was one track rather than a drive.
The file is readable by the account alone.

**Closes when:** nothing short of an erase at boot closes it, which the
operating system's own temporary directory cleaning does. Ledger only.
