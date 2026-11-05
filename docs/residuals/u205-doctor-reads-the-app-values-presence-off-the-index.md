---
title: Doctor says the app credentials are recorded off the presence index, so a value deleted through the keychain reads as set while lookups go to the account
found: at the review of #495, U205, 2026-11-05.
issue: no
---

**The mechanism.** `credential.catalogue` in `cli/doctor.py` asks
`secrets.exists`, the installation's index of names it wrote, never the
keychain, on the rule `core/secrets.exists` gives (a retrieval can raise an
authorisation prompt). After round one of U205's review, the opener reads a
value the keychain no longer holds as absent and sends the lookups to the
account, so in that state doctor says the lookups go under the app while they
go to the account.

**Measured cost.** Driven by the review: a value deleted with
`keyring.delete_password`, doctor OK. The run's own spend line says
"none under Cratekit's app credentials", so the person is told the truth on
every run that reached the provider; only doctor's sentence is wrong.

**Closes when:** the product gains a way to un-record a credential that clears
the index with it, or doctor's sentence names that it read the index. Ledger
only: no data lost, and the verbs report where their calls went.
