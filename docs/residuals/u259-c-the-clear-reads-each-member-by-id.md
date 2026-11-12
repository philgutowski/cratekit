---
title: crate inbox analyzed still reads each INBOX / Analyze member by its ID, one statement a row, twice per apply
found: at the build of #688, U259, 2026-11-12.
issue: no
---

**The mechanism.** U259 took the check off reads by ID and left the clear
alone, since the card named only the check. `analyzed.plan_clear` still calls
`member` for each live member of INBOX / Analyze, one `djmdContent` read by ID
a row, and `apply_clear` takes the plan again on the write handle, so an apply
reads every member twice more.

**Measured cost.** Not measured on the clear. On the check, the same per row
reads cost 18,574 statements and 3.4 seconds over 10,001 members on the
synthetic database, against 23 statements and 0.3 seconds batched. INBOX /
Analyze holds what one landing left, usually tens of rows, so the clear's
cost is small in practice.

**Closes when:** `plan_clear` reads the members a chunk of IDs to a
statement and judges them with `analyzed.judge`, its digest equal to today's
on the same database. Ledger only: a speed point, no false answer.
