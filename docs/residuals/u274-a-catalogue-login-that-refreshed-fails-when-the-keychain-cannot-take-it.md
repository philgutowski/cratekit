---
title: A catalogue or account login that refreshed fails outright when the keychain cannot take the refreshed session
found: at U274's review round two, 2026-11-13, one file over from round one's blocker.
issue: yes
---

**The mechanism.** `provider_session._login` (U261) writes the client's
refreshed session back through `materialised_session` before the scope closes,
and nothing catches a refusal of that write. Under the product's own opt in
for a machine with no keychain, `CRATE_ALLOW_ENV_CREDENTIALS=1` with the
session in `CRATEKIT_CREDENTIAL_PROVIDER_SESSION`, keyring's fail backend
refuses every write, so any login whose access token the client library
refreshed raises `CredentialBackendUnavailable` out of `client_session`. U274
made the download's drive warn instead (`provider-session-not-stored`); the
catalogue and the account still fail.

**Measured cost.** Driven by the review on the branch with the stand in
client's refresh: `client_session` raises, so every verb that opens the
catalogue or the account is blocked for a person on the opt in once the
stored access token has expired, which is every run after its first hour.
The base has the same write back, so the branch did not cause it.

**Closes when:** the login's write back failure is caught the way the drive's
close catches it, the login goes on with the refreshed client, and the verb
says the session was not stored. A test drives the opt in with keyring's fail
backend and a refresh, through `client_session` and one verb.
