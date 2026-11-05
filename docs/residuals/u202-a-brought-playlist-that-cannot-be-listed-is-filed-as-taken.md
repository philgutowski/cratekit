---
title: An account playlist the provider cannot list is filed under the taken kind on the gate
found: at the second review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `pair_cli.plan` lists a brought playlist whose listing the
provider refuses under `pair_discover.TAKEN`, the kind whose counted words
are "the account already holds its folder or title for something else". The
`sync-pair-not-brought` warning carries the provider's own message, so only
the item's kind is wrong. And with no pair held, a provider that answers
nothing lists every brought playlist this way and the sync ends as a no op
with that warning, where with a pair held the same provider refuses the sync.

**Measured cost.** Driven by the second review: the gate item's `action` reads
`taken` for a transient provider error. Nothing is written either way.

**Closes when:** a listing failure has its own kind, and a refusal about the
whole account refuses whether or not a pair is held. Ledger only.
