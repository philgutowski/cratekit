---
title: "A copy run redirects the installation state too, so the ISRC cache needs its own pointer to stay shared"
date: 2026-11-05
category: workflow-issues
module: "cratekit.acquire.isrc_cache, cratekit.core.rehearsal"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - "A verb that looks ISRCs up is rehearsed on a disposable copy before its live run"
  - "A rehearsal redirects CRATEKIT_STATE_DIR, by hand or through core.rehearsal.redirected"
  - "Something installation scoped is meant to be shared between a copy run and the live run"
symptoms:
  - "The live run's isrc-lookups line says every lookup was asked of the provider, after a rehearsal that asked the same ones"
  - "An isrc_cache.json appears in the copy run's scratch state directory"
tags:
  - disposable-copy
  - isrc-cache
  - installation-state
  - rehearsal
---

# A copy run redirects the installation state too, so the ISRC cache needs its own pointer

## The trap

U206's brief put the ISRC cache beside `provider_gate.json`, in the
installation's state directory, on the reasoning that a copy run redirects
`library.state_dirname` and so would still share it with the live run. That
holds for the sitting 13 procedure only. Every copy run since sitting 39 also
copies the installation state and redirects `CRATEKIT_STATE_DIR`
(`docs/cutover.md`, sittings 39 onward), and `core.rehearsal.redirected` does
the same for the body of any built in rehearsal. Under either, the cache
resolves into the scratch state, the rehearsal pays for its lookups there, the
scratch is removed, and the live run pays again: the very cost the card was
filed for.

## The rule

`CRATEKIT_ISRC_CACHE_DIR`, when set, names the directory the cache and its
lock live in (`config.ENV_ISRC_CACHE_DIR`). `core.rehearsal.redirected` sets it
to the live directory, resolved before it moves the state directory, and
restores it on the way out. A copy run by hand exports it the same way, set
to the live installation state directory, the folder doctor's
`provider.isrc-cache` note names the cache file in, BEFORE it exports its own
`CRATEKIT_STATE_DIR`. Sharing is safe because the cache holds only
what the provider said about its catalogue and marks nothing done; the copy run
still keeps every ledger, lock and run record of its own.

## How to apply

Before redirecting the installation state for any reason, ask whether
something under it is a fact about the outside world rather than about this
run. If it is, the redirect throws away a measurement the live run will pay
for again, and it wants its own pointer, as this one has.
