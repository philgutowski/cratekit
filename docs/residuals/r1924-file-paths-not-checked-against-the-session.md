---
title: The files' half of a restore writes a recorded path without asking whether the session authorises it
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** Every target of the database half passes
`Held.authorises_path` before it is written; the title tag and key tag a
session kept are written at the recorded path, re-based as every recorded
path is, with no such check. The adopt wrote the same paths without one.

**Measured cost.** One candidate driven at review round one: a row whose file
sits outside the library root is left `path-unmapped` by the adopt, so no
entry names it, and no write outside the root was produced. A prefix map rule
resolving outside the root was not driven.

**Closes when:** the put back names a path the session does not authorise as
not written, or the plan refuses it. Ledger only: no input was driven to a
write.
