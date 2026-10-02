---
title: "A stop checked before the next read never fires when the last reads are the ones that failed"
date: 2026-10-02
category: workflow-issues
module: "src/cratekit/label/artists_cli.py"
problem_type: workflow_issue
component: core_logic
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "A verb walks a list, asks a provider about each entry, and stops after N failures in a row"
  - "The stop is a refusal raised at the top of the loop body, before the next read"
  - "The verb is a plain run and not a job, so its exit code is the only thing a script reads"
symptoms:
  - "The same outage refuses a run of N plus one entries and exits clean on a run of N"
  - "A second run over the few entries the first left reports success with every one of them failed"
  - "Failing lines in the output beside an outcome of ok or no_op and exit code 0"
related_components:
  - label
  - provider_gate
tags:
  - outage
  - exit-code
  - loop-bound
  - label-artists
  - r-840
---

# A stop checked before the next read never fires when the last reads are the ones that failed

## Problem

`crate label artists` reads one release per open review item and stops when
three reads in a row fail. The first build raised that refusal at the top of
the loop, before the next read, which is where `label judge` raises its own.
The built in review drove the case the suite had not: three items, the
provider down, three failed reads, and the loop ends with no fourth pass to
raise on. The verb returned `no_op` and exit code 0 over an outage. The same
outage with a fourth item exited `unavailable-transient`.

## Why it was not seen

The test for the bound used five items, so the check always had a next pass
to fire on. And the shape was copied from a job, where it is right: a
judging job records every failed item in the job's own state and the run
reads as unfinished whatever the worker returns. A plain verb has no such
record. Its exit code is all a script reads, and the second run of a
repair is by construction a short list of the entries most likely to fail.

## The rule

In a plain verb, decide the refusal after the walk from what the walk
recorded, and let the bound only end the walk early.

    for entry in entries:
        failed = read(entry)
        failed_in_a_row = failed_in_a_row + 1 if failed else 0
        if failed_in_a_row >= BOUND:
            break
    if unread:
        raise refuse("unavailable-transient", ...)

Then one failed read is a refusal as well, which is the other half the
review found: failing lines beside a clean exit.

## The test that holds it

Drive the bound with exactly as many entries as the bound, and with one
entry, beside the longer list. `test_an_outage_over_the_last_releases_of_a_run_is_the_same_refusal`
and `test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
in `tests/test_label_artists.py`.
