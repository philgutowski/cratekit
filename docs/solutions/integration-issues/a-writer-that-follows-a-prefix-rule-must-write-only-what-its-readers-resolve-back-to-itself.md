---
title: A writer that follows a prefix rule must write only what its readers resolve back to itself, or a row on a second volume stops resolving
date: 2026-09-30
category: integration-issues
module: "src/cratekit/write/collection_export.py, src/cratekit/core/locations.py, src/cratekit/modules/outbound/source.py, src/cratekit/write/trees.py"
problem_type: integration_issue
component: recorded_path_resolution
root_cause: wrong_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A writer is changed to spell a path where it is mounted, and every test passes on a fixture whose one rule points at the library root"
  - "After the change a track on a second drive reads as unmatched, or a routing pass cannot find its row, on a library with a rule onto that drive"
  - "A reader resolves the new spelling as UNMAPPED where it resolved the recorded spelling as REMAPPED"
applies_when:
  - "A writer is asked to apply library.location_prefix_map to what it stores or exports, so the two spellings of one file agree"
  - "A fix for the base drive and the mounted path disagreeing is being placed on the writing side"
  - "A fixture for a moved library records exactly one rule and its target is the root token"
tags:
  - "locations"
  - "prefix-map"
  - "collection-export"
  - "idempotence"
  - "base-drive"
  - "r773"
---

# A writer that follows a prefix rule must write only what its readers resolve back to itself

## Context

R-773: `crate export collection` wrote every `Location` as the database holds
it, under the base drive, and `intake imported` compares a location with a
path under the mounted root, so it matched nothing. The brief's remedy was to
apply `library.location_prefix_map` in the export. The first cut did exactly
that. Resolve the recorded path, and when a rule places it, write the target.

## What the first cut missed

Applying the rule in the writer does not take it out of the readers. The
verbs that take an export, the playlist export's ISRC read and the routing
pass's row match among them, run each location through
`resolve_recorded_path` with the same root and the same rules. So the written
value is resolved a second time, and the rewrite is safe only when the second
resolution gives back the same path.

- Rule target under the library root. The written path is `UNDER_ROOT` and
  resolves to itself. This is the author's library and the only shape setup
  writes.
- Rule target on a second volume, one drive's old name mapped to its new one
  with the library root somewhere else. The written path is under neither the root nor any
  `from`, so it resolves `UNMAPPED` with no path. The recorded spelling had
  resolved `REMAPPED` to the file. The fix made a working row stop working.
- Two rules in a chain. The first target is the second's `from`, so the
  written path resolves somewhere else again.
- A target that is not an absolute path, which validation accepts.

The suite was green over all of it, because the moved fixture holds one rule
and its target is the root token. The built in review found it by probing
the resolver with a second volume.

## The rule

**Rewrite a recorded path only when resolving the rewritten path returns the
rewritten path.** One extra call, in `collection_export.mounted_location`:

    read_back = locations.resolve_recorded_path(resolved.path, root=root, prefix_map=prefix_map)
    if read_back.path == resolved.path:
        ...write resolved.path
    ...otherwise write what the database holds

A row that fails the test is left to its rule, written as recorded, and the
readers follow the rule as they did before. An identity rule, `from` equal to
`to`, makes a second volume pass, which is the same declaration
`name apply` already asks for a folder outside the root.

## Why this is the general shape and not an export detail

R-772 is the same pair of spellings on the native landing's side, and its
closing condition offers "the plan resolves its own stored path through the
map". Any writer that takes that road meets the same second resolution. Ask
of the value about to be written: which readers resolve it, through what, and
is it a fixed point of that.

## Prevention

- A fixture for a moved library needs a rule whose target is not the root
  before a writer side fix is called done. One rule to the root token cannot
  show this.
- Hold the property with the resolver and not with the writer, in a test that
  spells the expected path as a literal:
  `test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`.
- Mutation row `M1_read_back_not_asked` in `docs/mutation/r773-a.md` is the
  guard removed alone. 4 kills.
