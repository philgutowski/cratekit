---
title: A Discogs token the API rejects fails every file Beatport misses instead of stopping the run once
found: at the review of #673, U244, 2026-11-12.
issue: no
---

**The mechanism.** A 401 from Discogs raises a run scoped refusal built from
`secrets.CredentialRejected`, as the brief prescribes. The job engine stops a
run only on a parked item, never on a refusal's scope, so each file Beatport
misses fails its own item with the login step inside it, and the verb's own
cause is the generic one. Since U244's fix round the asker remembers the
rejection and sends the token once a process, so the cost is failed items, not
requests. Those files are not offered to the general catalogue either.

**Measured cost.** Driven at the review over four files: four failed items,
no genre written, where the same folder with no token recorded had all four
tagged by the general catalogue. A person re-records the token and resumes.

**Closes when:** Phillip decides whether a rejected optional token should
stop the run once with one sentence, or degrade to not asked as a missing one
does; then the engine or the asker carries it. Ledger only: the workflow
finishes once the token is recorded again.
