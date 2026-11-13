---
title: The rehearsal's refusal for a check copy with no room carries its origin by no test
found: at the review of #813, R-1677, 2026-11-13.
issue: no
---

**The mechanism.** `intake/land_cli.py` passes `origin=_ORIGIN` to
`snapshot.check_had_no_room` so the rehearsal's refusal for a throwaway copy
with no room carries the land verb in its cause's origin, as every
neighbouring refusal there does. The rehearsal's wrapper re-raises the cause
with the same origin on its way out, so dropping the argument loses nothing
a person reads.

**Measured cost.** Driven at round two: the call without the argument kills
no test. Maintainer facing only, the provenance trail in the envelope.

**Closes when:** a test asserts the origin trail of that refusal, or the
argument is dropped as redundant beside the wrapper. Ledger only.
