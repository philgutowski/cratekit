---
title: "A sub promoted to a bucket stops competing where it sat, unless the taxonomy says where it was"
date: 2026-10-01
category: workflow-issues
module: "core/taxonomy.py FormerPlace, core/routing.py competing_subs, adopt/move.py, templates/taxonomy.default.toml"
problem_type: workflow_issue
component: core_logic
severity: high
root_cause: incorrect_assumption
applies_when:
  - "A style sub is being given a top level folder of its own, as R&B was and Rock may be next"
  - "A sub, a bucket or a playlist name is being removed from a taxonomy template"
  - "A new key is being added to the template that changes what a reader of the tree decides"
tags: [taxonomy, routing, adopt, move, placements, former-place, competing-sub, schema-version, r-797, r-731, r-758]
---

# A sub promoted to a bucket stops competing where it sat

## Problem

R-797 moved R&B from a style sub of the non electronic folder to a folder of
its own. The obvious edit is three hunks of the template: add the bucket,
move the aliases, delete the sub. It loads, routing is right, and the suite
is green.

It also breaks the tree for every track still in the old playlist, silently.
What a track holds is read through one question, `routing.competing_subs`,
asked of the taxonomy. A playlist the taxonomy no longer declares is not a
place to any reader. So adoption files the track into its new band while it
still sits in the old playlist, and `crate adopt move`, the one verb that
removes a membership, neither plans leaving that playlist nor lists it. It
plans inside one bucket and refuses a place the taxonomy does not declare.

## What was built

A bucket declares the playlist it left, `[[bucket.formerly]]`, and that
former place is a competing sub. The existing plan, gate and writer then do
the cross folder move with no new verb. Four things were wrong in the first
build and each was found by review, not by the suite.

1. **It has to compete in the folder that holds it as well.** Competing only
   in the bucket that declares it, a track in the old playlist whose genre
   names another style of the old folder was added to that style and never
   taken out. Before the promotion the move settled exactly that track. A
   former place competes in two buckets and is settled in the one the
   track's entry claims.
2. **A new key needs a schema version.** The loader ignores a key it does
   not know. A build older than the key loads the edited copy cleanly, sees
   no former place, and double files. The version is what an older build
   refuses by name, so a template that declares one must state version 2.
   There are two installed copies of this product on the author's machine,
   so this is reachable.
3. **A bucket's defaults are not the old folder's.** A bucket that omits
   `rates` gets a star rating derived from energy. The old folder said
   `rates = false`. Carry each per bucket flag over on purpose or flip it on
   purpose.
4. **A move is made on a reading, and leaving a former place is not that
   kind of move.** A track with no energy reading was left in the old
   playlist under `no-reading`, and stayed in two places once anything
   filed it in the no reading sub. Nothing has to be read to know a
   playlist the taxonomy stopped declaring is not a track's place.

## How to promote the next one

- Add the bucket with exactly the source strings the old sub's map rows
  held. `tests/test_routing_parity.py` asks the frozen legacy code which
  strings it filed in the old playlist and holds the new bucket's aliases
  equal to that set, so a string too many or too few fails by name. It is
  written for one promoted bucket and needs widening for a second.
- Declare `[[bucket.formerly]]` on it, and keep `schema_version = 2`.
- Do not repoint a keyword rule in the same change. A track already in the
  old folder's default sub on that keyword would be filed twice, and the
  default sub is not a former place. R-804 holds that decision.
- The library's own copy of the taxonomy takes the same edit by hand, after
  a backup. No verb upgrades it.
- Rehearse `crate adopt move` on a copy and read the tracks it lists as left
  before approving the live plan.

## What to check when a sub is only removed

Deleting a sub with no successor has the same first half of this problem:
its playlist stops being a place, `rebuild` reports its recorded node as
undeclared, and nothing moves its tracks. Decide where they go before the
sub leaves the template.
