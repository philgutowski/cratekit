---
title: "A queued worker rebuilds its seam per item, so anything that must be remembered across files needs a per process binder"
date: 2026-10-01
category: integration-issues
module: "src/cratekit/tagging/cli.py handle, tagging/searchers.py for_taxonomy, tagging/published.py for_lookup"
problem_type: integration_issue
component: seam_design
severity: medium
root_cause: incorrect_assumption
resolution_type: code_fix
applies_when:
  - "A worker's seam has to remember something from one item to the next: a refusal, a rate limit, a cache, a pacer"
  - "A new network source is being bound into a job handler through a for_taxonomy style binder"
  - "A test of a latch or a cache passes on one closure and the verb still asks on every file"
tags: [tagging, jobs, item-handler, binder, rate-limit, circuit-breaker, r-796, r-226]
---

# A queued worker rebuilds its seam per item

## Problem

R-796 added a general catalogue to `crate tag folder`. The first build bound
it the way the searcher is bound, `published.for_taxonomy(declared)` called
inside `handle`, which built a fresh lookup. Every answer was right and the
suite was green. The built in review found that a rate limited sweep would
spend the whole 429 backoff, 90 seconds, on every file, and keep sending
requests to a catalogue that had said stop.

## Cause

`ItemHandler` is a fixed three argument callable, and `handle` runs once per
item. The binders exist so a test can swap a fake in, and each one CONSTRUCTS
what it returns: `searchers.for_taxonomy` builds a new searcher, a new pacer
and a new fetch for every file. Nothing built there outlives the item. So a
closure variable that looks like run state, a latch, a memo, a pacer's last
touch, is per file state, and a unit test that calls one closure twice proves
the latch and says nothing about the verb.

A job IS driven in one process, `jobs.drive` claims items in a loop, so
process state does last the run. The seam just never held any.

## What works

Keep the memory in the object and make the BINDER hand back one object per
process. `published.for_lookup()` builds the lookup on first use and returns
the same one after, and `published.for_taxonomy` builds the cheap per item
seam over it. The refusal memory and the album memo live in the lookup.

U260 bound the picture fetch the same way. `searchers.for_images()` hands
back one remembering fetch per process, so an album's files, which name one
cover address, cost one paced request, and `searchers.reset_images()` drops
it. A shared object built once also freezes whatever it captured at build
time, the HTTP getter among them, so the suite resets it around every test.

Test it through the binders, one seam per file as the worker builds them,
`test_a_refusal_on_one_file_reaches_the_next_files_seam`, and through the
verb with a request count. Mutation row `V6_one_lookup_per_process` reverts
the binder to building per call and both die.

## Next time

- Before adding any cross file behaviour to a worker's seam, read `handle`
  and ask which object survives the item. If the binder constructs, nothing
  does.
- The searcher's own pacer is rebuilt per file for the same reason. It still
  paces, because every touch waits first, but it cannot honour anything a
  catalogue said on the previous file. R-791's fallbacks were asked on every
  file after a block for that reason, at one request each, until U281 handed
  the searcher the run's count of refusals in a row, `searchers.for_run`, keyed
  by the job and the drive's attempt so a new sweep starts its own.
- A detached resume is a fresh process, R-226, so per process memory is also
  the most a binder can promise. Memory across runs is a state file, and
  R-800 records that the one declared for lookups is unused.
