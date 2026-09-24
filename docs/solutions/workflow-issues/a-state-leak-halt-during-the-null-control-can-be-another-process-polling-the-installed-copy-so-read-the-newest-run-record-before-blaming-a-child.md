---
title: A state leak halt during the null control can be another process polling the installed copy, so read the newest run record before blaming a child
date: 2026-09-24
category: workflow-issues
module: scripts/mutate.py
problem_type: workflow_issue
component: mutation_driver
severity: low
root_cause: shared_machine_state
resolution_type: diagnosis
applies_when:
  - The mutation driver stops with STATE LEAK and the real installation state
    grew by one entry while a child ran.
  - The row it stopped on is the null control or a row whose subset runs no
    verb that writes run records.
  - The Relay feeder or the installed pipx copy of cratekit is in use on the
    same machine.
  - The halt repeats on every rerun with the entry count unchanged, because a
    real job is running from the installed copy.
tags:
  - mutation-driver
  - state-leak
  - r-343
  - relay
  - run-record
  - job-queue
---

# A state leak halt during the null control can be another process polling the installed copy, so read the newest run record before blaming a child

## The symptom

On 2026-09-24, on `relay/202`, `scripts/mutate.py` stopped during the null
control with the STATE LEAK message: the real installation state under the
application support directory held 2892 entries before the child and 2893
after it. Nothing was measured. The message names two causes it cannot tell
apart, a child reaching the real machine (R-343) and something else writing
there while the child ran.

## Where the cause actually was

The new entry was `runs/2026-09-24T20:31:40Z-e763.json`, a run record for
the `status` verb with no decisions and no offers. No test in the subset
runs `status`, and every child of the driver runs under the installation
state sandbox, so the record was written by another process on the machine
running the installed copy of cratekit. The Relay feeder and runner were up
at the time. The pair of records at 13:03 and 14:00 the same day have the
same shape, so something polls the installed copy on its own schedule.

## The fix

None to the driver. The entry count was stable afterwards and the rerun
measured every row. The guard did what it is for, and the message is right
that it cannot tell the two causes apart. What it cannot say is which, and
the run record can.

## How to tell next time

Before rerunning, list the newest files under the runs directory of the real
state and read the newest one. A record whose `verb` is one the subset never
drives, with empty `decisions` and `offers`, is a poll by another process,
and the rerun is safe. A record whose verb is one the tests drive, or a
change to `config.toml` or a lock file, is R-343's shape and the child must be
found before anything is rerun.

The one caveat the guard already states: it watches the application support
root only. A child reaching the redirected home or data root is not seen by
this check, so a clean count is not proof of isolation, only the absence of
the one leak it measures.

## A second shape: a live job halts every rerun

On 2026-09-24, on `relay/203`, the first attempt halted on one new run record
as above, a `job.show` poll. The rerun halted again with the entry count
UNCHANGED, 2900 before and after. The change was the job queue's write ahead
log under `jobs/`: a real `crate sync labels` job, started from another
session against the installed copy, was running, and its lock file under
`jobs/` named a process that was still alive. While that job runs, the queue
changes under every child, so every rerun halts, and two bounded waits of
over nine minutes each did not see it end.

How to tell: an unchanged count with a halt means a file changed in place.
Read the lock files under `jobs/` and check whether the process each one
names is alive. If one is, the table cannot be measured until that job ends.

What not to do: the driver's watched roots follow `CRATEKIT_CONFIG_DIR` and
`CRATEKIT_STATE_DIR` in its own environment, so an empty directory there
gets the table to run. That turns off the one check for R-343's shape, which
is a decision for an attended session, not an unattended one. Record the
table as unmeasured in its notes file, commit the rows so a later session
can run them as they are, and say so in the ledger.

