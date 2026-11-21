---
title: The portability scan passes a tilde home path and an email address
found: at the review of #874, U316, 2026-11-21.
issue: no
---

**The mechanism.** `scan.portability_violations`, which the skills lint and
the scan share, matches the home directory by its absolute shape and the
volume by name. Driven at the review with no identity tokens: a line working
in a tilde path under the home's music folder, a `cd` into a tilde documents
path, and an email address each returned no violation.

**Measured cost.** None measured: no tracked file carries either today, and a
tilde path names no person by itself. A personal email address or a tilde
path to a real library in a skill or doc would land green in a public
repository.

**Closes when:** the scan refuses an email address outside an allowlisted
placeholder domain and a tilde path below the home, or the record says why
either is not personal. Ledger only.
