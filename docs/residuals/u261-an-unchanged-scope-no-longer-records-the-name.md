---
title: A scope that left the session unchanged no longer records the session's name in the credential index, which every login used to do
found: at the review of #690, U261, 2026-11-12, round one.
issue: no
---

**The mechanism.** Before U261 every scope wrote the session back through
`secrets.set_json`, which records the name in the presence index, so a
login repaired an index that had lost the name. An unchanged session is now
not written, so the index is left as it was.

**Measured cost.** Driven by the review: with the name removed from the
index and the session still in the keychain, an unchanged downloader scope
leaves `secrets.exists` False on the branch where `main` made it True. The
catalogue and the account then refuse `credential-missing` until the session
is recorded again, the remedy that refusal already names. The producers, a
full disk in the window `secrets.set` documents or a person removing a
damaged index, were not driven.

**Closes when:** a scope that read the session records its name in the
index when the index lacks it, without a keychain write, or the refusal's
remedy is judged enough. Ledger only.
