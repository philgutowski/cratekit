---
title: "A reader that recognises more than the writer finds reads a renamed playlist as already there, and the writer files the track a second time"
date: 2026-09-27
category: integration-issues
module: "src/cratekit/adopt/placements.py, src/cratekit/adopt/plan.py, src/cratekit/write/trees.py"
problem_type: integration_issue
component: seam_design
severity: high
root_cause: asymmetric_resolution
applies_when:
  - "A plan decides not to write because a read says the row is already where it is going"
  - "The read resolves a destination through recorded node identifiers and the write resolves it by display name"
  - "An add only writer sits behind a check that was written to be generous about what counts as held"
symptoms:
  - "A track sits in a playlist a person renamed in rekordbox and gains a second playlist under the taxonomy's name"
  - "The plan reports the entry applicable and the writer reports it added, where both should have said already present"
  - "A withhold written for a different sub never fires when the held sub and the planned sub are the same one"
related_components:
  - "adoption"
  - "tree_writer"
  - "convergence"
tags:
  - "adopt"
  - "placements"
  - "rename"
  - "node-record"
  - "add-only-writer"
  - "reader-writer-asymmetry"
---

## The trap

R-731 made the adoption plan read where a track already sits, so it could
withhold a track holding a different energy band. The reader was written to be
generous: a playlist counts as a destination when it carries the declared
names OR when the convergence record names its node, which is the order
`rebuild.resolve_destinations` argues and is what survives a rename.

The plan then exempted a track already in the sub it names, on the grounds
that the writer reports that row already present and adds nothing. That
sentence is true of the writer's OWN lookup and of nothing else.
`write_tree_membership` finds its folder and its playlist with
`ensure_folder` and `ensure_playlist`, by declared display name under the
anchor. A playlist renamed in rekordbox is invisible to it. So for a track in
a renamed `Med`, the reader said "holds med", the plan said "already there,
leave it to the writer", and the writer created a new `Med` and added the
track. The generous read turned the exemption into the double filing the unit
existed to stop.

The author's suite was green over it. The built in review found it by
reading the two lookups side by side, and a test that renames a playlist and
records its node failed before the fix.

## The rule

**"Already there" is a claim about what the WRITER will find, so it has to be
asked the way the writer asks.** A read that feeds a decision to skip a write
may recognise more than the writer does only if it says which part the writer
cannot see.

Here `Placements` carries `held`, everything a track holds by either route,
and `unnamed`, the part held through a node that does not carry the declared
names. A different competing sub withholds whichever route found it. The
planned sub exempts the entry only when it is held under the declared name.
Held under another name only, the entry is withheld and listed.

## When to apply

- Before writing "the writer will dedupe this", open the writer's lookup and
  compare it with the read that made the claim, key by key.
- When a check has two jobs, finding a conflict and proving a no-op, the
  generous resolution serves the first and the writer's own resolution serves
  the second. One resolution for both is wrong in one direction.

## Related

- R-731 in `docs/residual-findings.md`, and R-738 beside it, the same
  asymmetry for two folders of one name, recorded and not driven.
- The limitation `find_collisions` states in `adopt/plan.py`, which is this
  shape one level up, at the folder.
