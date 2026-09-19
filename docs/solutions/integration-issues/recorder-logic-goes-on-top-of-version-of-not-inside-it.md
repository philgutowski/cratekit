---
title: "New tombstone recorder logic has to sit on top of version_of, and a decision that needs two records must be one store write"
date: 2026-09-19
category: integration-issues
module: src/cratekit/deletion/stores.py
problem_type: integration_issue
component: deletion
severity: high
resolution_type: code_fix
applies_when:
  - "A unit changes how the deletion pass composes or records a tombstone identity"
  - "A single deletion decision needs more than one tombstone record, such as a verbatim identity and a companion"
tags: [tombstone, version_of, identity_scheme, companion, record_tombstone, r-431]
---

# New tombstone recorder logic goes on top of version_of, and two records are one store write

## Problem

R-431 needed the deletion pass to record a second identity beside a credited tombstone, with the bracketed credit groups stripped, so a provider that spells a track without the guest could reach it. The obvious place to put the stripping was inside `version_of`, which already composes the identity.

## Cause

Two rules that the code does not announce.

1. `deletion.stores.identity_scheme` measures the rules by walking everything reachable from `version_of`. Logic added inside that function changes the pinned stamp, so every tombstone already on disk reads as written under a different scheme and is sent to the row lookup. Nothing fails loudly. Existing deletions just stop being consulted the fast way.
2. The deletion pass puts a trashed file back when `record_tombstone` raises. A decision that writes two records in two calls can fail between them, restore the file, and leave one orphan record behind.

## What to do next time

- Put new recorder logic in a wrapper over `version_of`, as `uncredited_version_of` does. Never edit `version_of` or anything it reaches unless changing the stamp is the intent.
- Write one decision as one store write. `DecisionStore.record` takes `beside` and `DecisionStore.revoke` takes `also` for this. Do not add a second `record_tombstone` call.
- Tombstones written before a companion existed still miss the provider shape. That gap is R-517 in `docs/residual-findings.md`.

Related: `a-field-on-wanted-that-guards-a-consult-must-cross-the-intake-freeze.md`.
