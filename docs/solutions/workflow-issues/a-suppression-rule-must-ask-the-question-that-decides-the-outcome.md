---
title: "A suppression rule must ask the question that decides the outcome, not the one that sounds equivalent"
date: 2026-09-21
category: workflow-issues
module: "core/routing.py suggest_tag, core/taxonomy.py bucket_for_display, tagging/cli.py"
problem_type: workflow_issue
component: core_logic
severity: medium
root_cause: incorrect_assumption
applies_when:
  - "A report or warning is being suppressed for values that look like they belong to the system"
  - "Two entry points share one declared table and each has its own tier order"
  - "A message about a written value is about to claim where that value ends up"
tags: [tagging, routing, taxonomy, r-650, r-247, off-taxonomy, suppression, two-entry-points]
---

# A suppression rule must ask the question that decides the outcome

## Problem

R-650 added a report for a genre written from `suggest_tag`'s last tier, the one
that passes an unrecognised source string through unchanged. The report needed a
suppression rule, because a bucket's own display name reaches that tier too and
reporting the library's own folder names as gaps is noise.

The first build suppressed on the declared VOCABULARY: every display the
template declares, buckets and subs. It reads as obviously right. It is wrong,
and it hides the exact defect the report exists to surface.

## Cause

`routing` has two entry points over one table and they do not share tier orders.
`resolve_bucket`'s display tier reads BUCKET displays only, deliberately, since
a sub's display answering it would place a track one level up the tree.

So a sub's display is a declared word that routing does not recognise. Written
onto a file it lands in the fallback bucket exactly like a word nobody ever
declared. Suppressing it because the template contains the string somewhere
means the one case that most needs reporting is the one that goes unreported.
Driven on `tests/taxonomies/second.toml`: `Birds`, `Water` and `Engines` are
each declared, each pass through, each route to `unfiled`.

The same holds for case. Every other tier of `suggest_tag` matches on a
lowercased value, so making the suppression case insensitive looks consistent.
But the tag is written VERBATIM and routing matches VERBATIM, so `nonelectronic`
lands in the catch-all while `NonElectronic` is placed. And this one is
produced by the shipped code rather than by a hand edited template:
`_bandcamp_tag` only ever selects a tag equal to its own lowercase.

The rule that works is the one that decides the outcome. `bucket_for_display`
is exactly the predicate for "routing will place this word where the template
says", so it is the suppression, and no second index is needed.

The same two entry points bit again in the warning's text, in the other
direction. It said the flagged words route to the fallback bucket, inheriting
that claim from R-650's own body. `suggest_tag`'s last tier and
`resolve_bucket`'s keyword tier read two different rule lists, so being off
taxonomy predicts nothing about the landing: `Psy-Trance` and
`Hardcore / Hard Techno` are off taxonomy and keyword routed to real buckets,
`gqom` and `Leftfield Bass` are off taxonomy and land in the catch-all.

## Next time

- When writing a suppression, name the OUTCOME it is protecting against and find
  the predicate that decides that outcome. "Is this word one of ours" and "will
  this word be placed where we said" sound like one question over a declared
  table with two entry points, and they are two.
- Before a message asserts a consequence of a value, drive the function that
  produces the consequence. Four strings through `resolve_bucket` took a minute
  and showed the claim false for half of them.
- A ledger entry's own cost paragraph is a claim, not evidence. R-650's said the
  string routes to the fallback, and the unit closing it inherited that into a
  user facing warning. R-247's body was wrong about this same seam and was
  corrected by the #170 build, which is the neighbouring entry in
  `unmapped-genre-only-means-a-deliberate-decline-so-a-tag-alias-cannot-answer-it.md`
  and the second time running in this area that a read premise did not survive
  being driven.
