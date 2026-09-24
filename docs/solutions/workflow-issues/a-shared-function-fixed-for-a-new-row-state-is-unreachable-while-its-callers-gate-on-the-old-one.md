---
title: "A shared function fixed for a new row state is unreachable while its callers gate on the old one"
date: 2026-09-23
category: workflow-issues
module: "acquire/match_cli.py adjudicate and touches_the_queue, intake/cli.py resolve_track, intake/missing_cli.py, label/approved_cli.py, acquire/fallback_cli.py"
problem_type: workflow_issue
component: core_logic
severity: high
root_cause: incomplete_seam_coverage
applies_when:
  - "New behaviour is added inside adjudicate for a row state it used to pass straight through"
  - "A caller opens the review store lazily, on a predicate written for the old behaviour"
  - "A residual about the queue is closed by a change to the engine and measured only through match run"
tags: [review, match, adjudicate, r-679, r-680, touches_the_queue, call-sites, lazy-open, checking-path]
---

# A shared function fixed for a new row state is unreachable while its callers gate on the old one

## Problem

R-679 was closed by teaching `adjudicate` to retire a row's open question
when resolution owns the row. The first build put the write in the right
place, the one function every resolution passes through, and drove it through
`match run`. The built in review found that four of `adjudicate`'s five
callers never handed it an owned row: the intake worker, the missing pass, the
label sweep and the fallback pass each opened the review store "only for a
question", with a gate on the needs-review state written before owned rows
had anything to do there. Those four are the verbs that filed the 85 stale
items the residual measured. Re-resolving the owning job through any of them
would have retired none.

## Cause

Opening the store lazily is a real economy, fifty opens to use it twice in
the per item worker, and each caller encoded the economy as its own predicate
on the row state. The predicate was correct for what `adjudicate` did at the
time. When `adjudicate` gained a second reason to touch the queue, the
function changed and the five predicates did not, and each is in a different
module. A green suite over `match run`, the one caller with no gate, said the
feature worked. This is METHOD's third defect pattern exactly: the fix landed
on the performing path and the checking path stayed as it was.

## Fix

One predicate, `match_cli.touches_the_queue`, owns "does this row have
business with the queue", a question or a rule owned row, and every caller
gates on it. A guard in the match suite lists every module that calls
`adjudicate` and asserts it names the predicate at least as many times as it
calls, since the missing pass calls twice. The intake worker's own path is
driven end to end.

## Next time

- Before adding behaviour to `adjudicate` for a state it used to pass through,
  `git grep -n "match_cli.adjudicate("` and read the line above each call. A
  caller that decides whether to open the store is a caller that decides
  whether the new behaviour runs. R-680's fix, whatever the record decides a
  superseded item should read once its row is missing, lands on the missing
  state, which every caller today passes through without opening the store:
  `touches_the_queue` has to widen first, or the fix is unreachable from
  every verb.
- Measure a queue change through the verb that filed the items, not the verb
  that is easiest to drive. The residual named the jobs; the jobs named the
  verb.
- A structural guard that counts gates against calls is what stops the next
  caller from re-encoding the old predicate. It holds only if the predicate
  is spelled once, by name, so keep the gate a call to `touches_the_queue`
  and not a re-derivation of it.
