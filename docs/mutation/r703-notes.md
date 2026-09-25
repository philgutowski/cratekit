# R-703 mutation notes

**Verdict: measured, 23 rows in three batches, 22 killed, one maintainer
facing zero.** Written on `relay/215`, 2026-09-24, by the author, so every
zero reads as "the author could not kill it".

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r703-a` | 10 | 10 | 0 |
| `r703-b` | 11 | 8 | 3, L2, L3, O2 |
| `r703-c` | 2 | 2 | 0 |

## The zeros

- **L2, a later exception overwrites the first, and L3, the message outranks
  the exception.** User facing: either one makes an item name the corrupt
  merge a rate limit left behind, or the tool's own reading, instead of the
  provider's answer. No test held either, because every fake logged exactly
  one failure. One test each was written after the batch,
  `test_the_first_exception_the_tool_logs_is_the_cause_not_its_consequence`
  and `test_the_providers_exception_outranks_a_message_the_tool_logged_first`,
  and batch C re-measured the same two mutations as C1 and C2: one kill
  each.
- **O2, the observed session wraps any callable, not only methods.**
  Maintainer facing, one line: the only test that reads a non method
  attribute through the proxy reads a non callable one, so wrapping every
  callable is not seen. What it would break is a callable helper object
  reached through the session losing its own attributes, which no call the
  vendored tree makes today does.

## How the guard was watched

The installed copy's `crate analyze vocals --recursive` job
`2026-09-24T21:04:27Z-fbe8` was running over the whole library volume and
writing the real jobs directory throughout, read from the process list and
not assumed. The first attempt at batch A, with the guard over the real
directory, stopped at its baseline with a `STATE LEAK`, 13797 entries to
13817, all of them the job's. It is not this session's to stop. Every batch
was therefore run the way `relay/214`, `relay/217` and `relay/218` ran
theirs, with `CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` pointed at fresh
empty temporary directories, which the guard watched. In place of the guard
over the real directory, every file in it outside `jobs/` was hashed before
batch A and after batch C: 390 files, digest `bda77d9a` both times. That
covers the configuration the guard exists to protect and not `jobs/`, so a
child reaching the real job queue would not have been seen.

## What the kills say

The seam is held at each of its layers. Dropping the observed session (V1,
4 kills), the proxy's note (O1, 5), the cause handed to `landed_file` (V3,
4) or its words (LF2, 4) all lose the Closes when test's reading of
`TooManyRequests` off the item cause. The type guards are held separately:
the classifier reading the carried text (A1) dies on the not found album
read, and the pool reading it (D1) dies on the carried "forbidden", "403"
and "429" cases, three kills from four parameters. The "Retry-After: 900"
case does not die on D1, because the pool reads a retry hint only after a
signal it already found. The escalation is held from both sides: removed
(V4, 2) and asked of a landed item too (V5, 1). V6 samples R-705's park
check, 2 kills.
