---
title: With the environment credential opt in set, a Discogs token setup links or relinks is reported linked while the environment's token is the one every read returns
found: at the review of #799, U283, 2026-11-13.
issue: no
---

**The mechanism.** `secrets.get` prefers the environment variable when
`CRATE_ALLOW_ENV_CREDENTIALS=1` and the token's variable are set. Setup's
Discogs step checks and stores the typed token in the keychain and says
"linked: Discogs accepted the token", and a later tag run reads the
environment's token instead. `crate login discogs-token --from-file` already
behaves the same way, and the brief required storing exactly as login does,
so the step kept the shared store's precedence.

**Measured cost.** Driven by the round one reviewer with both variables set
and `--relink-discogs`: the note said linked while `secrets.get` returned the
environment's value. Reachable only on a headless machine that opted in by
name; nobody on the Mac sets the opt in.

**Closes when:** setup and login both say, when the environment fallback is
on and names this credential, that the environment's value is the one used.
Ledger only: a maintainer's opt in, no data lost.
