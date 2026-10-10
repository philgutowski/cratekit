---
title: "A genre split out of a bucket that keeps its bands needs a split place, not a former place"
date: 2026-10-09
category: workflow-issues
module: "core/taxonomy.py _check_former_places, adopt/move.py, write/rebuild.py, templates/taxonomy.default.toml"
problem_type: workflow_issue
component: core_logic
severity: medium
root_cause: incorrect_assumption
applies_when:
  - "A genre is being carved out of a bucket that still files its own tracks into live energy bands, as Soul was out of R&B"
  - "A plan says to copy the Hip-Hop or R&B former place shape for the next genre folder"
tags: [taxonomy, former-place, split-place, rebuild, adopt-move, u118]
---

# A genre split out of a bucket that keeps its bands needs a split place, not a former place

## Problem

U118 gave Soul and Hip-Hop their own folders. Hip-Hop worked as R&B had: its old
`non_electronic / hip_hop` playlist is declared as a former place and `crate adopt move`
carries the tracks over. Soul looked identical on paper, but its tracks sit in R&B's live
Low, Med and High bands. Declaring those as Soul's former place is refused at load, because
`_check_former_places` rejects a former place its holder still files into.

## Cause

A former place describes a spot that the holder has stopped using. R&B keeps using its
bands, so they cannot be a former place for anyone. The shape did not exist in the schema.

## What to do next time

- Use a split place (schema version 3). It competes only in the declaring bucket, so R&B's
  own bands are untouched.
- The tree path must count a split place as settled in both buckets, and in the holder
  whenever the track's genre names the declarer. If it only counts in one, the two buckets
  plan competing moves for the same track and the read back reports one of them unfinished.
- A moved track keeps every other membership (with vox and the like). Test the Soul track in
  `R&B / Med` ending in `Soul / Med` and nowhere in R&B.
- Mutation batches made only of template rows are refused by `mutate.py`, since the null
  control needs a Python target. Add a Python row to the batch.

Neighbour: [a sub promoted to a bucket stops competing where it sat](a-sub-promoted-to-a-bucket-stops-competing-where-it-sat-unless-the-taxonomy-says-where-it-was.md),
which covers the plain former place case.
