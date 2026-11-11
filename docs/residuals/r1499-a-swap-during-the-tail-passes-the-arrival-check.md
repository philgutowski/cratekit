---
title: A swap of one file out and one in while the tail runs passes the arrival check
found: at the review of #665, R-1499, round two, 2026-11-11.
issue: no
---

**The mechanism.** `intake.beside.arrived` reads a new finished item of another download, or a change in how many files a landing would take. A person moving one file out and putting another in during the tail changes neither, and the arrival is renamed, planned and kept as the batch's own.

**Measured cost.** Driven at round two by moving files by hand during `analyze run`. The producer is a person swapping files mid tail.

**Closes when:** the check compares identities the tail cannot change (an ISRC each own download froze) rather than a count. Ledger only.
