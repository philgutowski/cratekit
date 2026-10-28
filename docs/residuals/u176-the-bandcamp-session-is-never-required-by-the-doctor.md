---
title: The doctor never requires the Bandcamp session, and the setup wizard never offers it
found: at the second review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** `credential.bandcamp` is in `doctor.CREDENTIALS_BY_CHECK`
and no verb declares it in `doctor_checks`, so it is never required: the
doctor reports it as information naming the two verbs that spend it, and the
setup wizard, which offers only required credentials, does not ask for it.
Declaring it would make the doctor fail on every installation whose profile
switches on feature row 6 and has no Bandcamp account, and would make the
wizard ask each of them for a browser cookie.

**Measured cost.** None to the verbs: each refuses `auth-failed` naming
`crate login bandcamp-session --from-file PATH` when no session is recorded.
The choice is the conservative one, taken with nobody to ask; whether
Phillip wants the doctor to fail without a session is his.

**Closes when:** Phillip decides whether a Bandcamp session is required where
the verbs are switched on. Ledger only.
