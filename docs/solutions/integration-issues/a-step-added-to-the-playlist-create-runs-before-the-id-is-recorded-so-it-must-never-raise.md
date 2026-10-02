---
title: A step added to the playlist create runs before the id is recorded, so it must never raise
date: 2026-10-02
category: integration-issues
module: "src/cratekit/modules/outbound/tidal_account.py"
problem_type: integration_issue
component: outbound_adapter
root_cause: ordering_of_side_effects
resolution_type: design_rule
severity: high
symptoms:
  - "A playlist exists on the streaming account but the ledger has no identifier for it"
  - "The next item of a per item export creates a second playlist with the same name"
applies_when:
  - "Anything is added inside RemoteAccount.create_playlist, such as visibility (R-834) or folders (R-835)"
  - "A call after the provider's create can raise or be refused"
tags:
  - "outbound"
  - "tidal"
  - "ledger"
  - "r834"
  - "r835"
  - "r849"
---

## The trap

`TidalAccount.create_playlist` runs inside the lambda that
`ledger.reserve_playlist` resolves under its lock. The identifier is recorded
only after that lambda returns. Any step added after the provider's create and
before the return, such as setting the playlist private, can raise, and when it
does the remote playlist exists with no recorded identifier. The next item of a
per item export finds nothing recorded and creates another one.

## What was done for R-834

The private step is retried once, the create itself is never retried, and a
refusal that outlasts the retry is passed over so the playlist is still
recorded. That pass over is R-849, a known gap and not a fix.

## Next time

Whatever a unit adds to the create path, folders for R-835 included, is either
passed over on failure or moved after the reserve. Never raise from inside the
create. Test it with a fake client whose added step raises, and assert that the
playlist is recorded and that the next item makes no second create.
