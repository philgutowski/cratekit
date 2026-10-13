---
title: A destructive session's record does not say which rule minted the acknowledgment it ran on
found: at the review of #315, U138, 2026-10-12.
issue: no
---

**The mechanism.** `assert_gates` opens a session record carrying the
acknowledgment's `actor` and `recorded_at` only. U138 adds `rule` and
`decided_by` to the acknowledgment file, and that file is overwritten on
every mint, so after a later mint nothing durable says whether an earlier
destructive session ran on a session minted acknowledgment or a person's.

**Measured cost.** None to a library: no write is allowed or refused
differently. An audit question, answered today only while the file has not
been re-minted. Not driven.

**Closes when:** `open_session` records the rule and the answering actor
beside the derived one. Ledger only, maintainer and audit facing.
