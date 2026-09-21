---
title: An identifier re-key in an installation scoped store cannot rewrite library scoped state, so it records the move and the other side follows it
date: 2026-09-21
category: integration-issues
module: "src/cratekit/label/registry.py, src/cratekit/label/marks.py"
problem_type: integration_issue
component: label_registry_migration
root_cause: wrong_assumption
resolution_type: code_fix
severity: medium
symptoms:
  - "A brief says the registry loader rewrites label_id and any watermark keyed on the old id, and the loader has no configuration naming a library"
  - "A watermark year sits under an identifier no registry entry holds after the registry re-keyed"
  - "A sweep job queued before the re-key refuses label-unknown on the old identifier"
applies_when:
  - "An identifier a registry derives is changed and a second store keeps state keyed on it"
  - "The two stores have different scopes, installation against library"
tags:
  - "label-registry"
  - "watermarks"
  - "slug"
  - "migration"
  - "r381"
---

# An identifier re-key in an installation scoped store must be followed lazily

## Problem

R-381 changed `registry.slug` so `Sueño` is `sueno` and `Voll Schön` is
`voll-schoen`. The brief said the registry loader migrates a stored `sue-o`
entry and rewrites the watermark keyed on it in the same step.

## Cause

The registry is installation scoped and takes no configuration. The label
watermarks (`config.state_path("label_watermarks")`) are library scoped. The
loader cannot name a library, so it cannot reach the file to rewrite.

## What was built

- `migrate()` re-keys only an entry whose id is exactly the old fold of its own
  name, and never onto an identifier another entry holds. A collision leaves the
  old id.
- The registry writes a `renamed` map, old to new, into its own document.
- `marks._follow` reads `live_renames()` and moves the year on the next `read`
  or `advance`, under the watermark lock.
- A move is live only while nobody holds the old identifier. Once a new label
  reuses it, the move stops applying, or the new label would inherit the
  moved label's year.
- `Registry.get` follows a move too, for a job frozen on the old id.
- If the migrated registry cannot be written, `load` returns the document as
  stored, never an unwritten moved view.

## Next time

When a brief asks one store to rewrite another store's keys, check the scopes
first. If they differ, record the move where the first store can write and let
the second follow on read. Expire the record when the old key is reused.
