---
title: A login whose refresh the keychain took and its index refused is reported as not stored, and the next resolve logs in again
found: at the review of #824, R-1694, round one, 2026-11-13.
issue: no
---

**The mechanism.** `secrets.set` writes the keychain, reads it back, then
records the name in the presence index. When only that last step refuses
(`credential-index-unreadable`, or an `OSError` writing the index), the
keychain already holds the refresh. `provider_session._login` catches the
failure as a store failure (R-1694), notes it, and returns the session it read
as the one the keychain holds, so the held session's blob is the old session.
The verb's `provider-session-not-stored` warning then says the refresh could
not be stored over a keychain that did store it, and the next resolve in the
process reads the refresh out of the keychain, finds it differs from the held
blob, and logs in afresh from it.

**Measured cost.** Driven by the review with the in memory keychain and
`secrets._record_name` refusing: two logins over three resolves where one was
enough, about two provider calls, and a warning that is half wrong (the
session was stored; the index was not). The producer was not reached: two
candidates were driven, a damaged index file with and without the opt in, and
neither produces it, since `catalogue_client`'s own presence check refuses a
damaged index first. Only an index damaged between that check and the write
back remains, not driven. No session is refused, lost or reused.

**Closes when:** the login reads the keychain back after a store failure and
holds what it reads, and the warning tells an index refusal from a keychain
refusal. Ledger only.
