---
title: "The same text in another file is not the same guard, so a replayed row that moved needs a test in common or a person's word"
date: 2026-11-21
category: workflow-issues
module: "scripts/killset.py, scripts/mutate.py, docs/mutation"
problem_type: workflow_issue
component: mutation_driver
severity: high
root_cause: wrong_identity
resolution_type: guard
applies_when:
  - "A card that restructures code replays its recorded kills and killset.py rows with the after option lists a row as unplaced"
  - "killset.py check says a row is killed at a new anchor only by tests that did not kill it before"
  - "A refactor deletes a guard, or merges two guards written the same way, and the replay still reads every kill as kept"
tags:
  - mutation
  - kill-set
  - replay
  - refactor
  - identity
---

## The trap

A recorded mutation row is a file, an `old` text and a `new` text. After a
refactor the text is often in another file, and it is tempting to say the row
moved wherever its text now stands once. It did not always. 188 of the 7,093
live rows on `ff8e5ec` have exactly one twin, the same line in a neighbouring
file guarding something else. Delete the guard and the twin is the one place
the text is left, so the deleted row is "found", replayed at the twin, killed
by the twin's tests, and `check` reports a lost kill as kept.

U297's review found this twice. The first fix asked whether the file holding
the text now held it at the measured commit, and the twin's file can have
been renamed or split since, or the line written new in a file that did not
exist. Nothing read off today's holder settles it.

## What holds

Two rules, and both are needed.

- `killset.py rows --after BEFORE.json` places a row elsewhere only when its
  text stood in exactly one place under its top directory at the commit the
  BEFORE table was measured on (read from one `git archive`) and stands in
  exactly one now. Two places then means a twin, whatever its file is called
  today, and the row is listed as unplaced.
- A deleted guard and an identical line written new still read as one place
  then and one now. So `killset.py check` holds every row at a new anchor to
  being killed by at least one test, by function name, that killed it
  before. A test that moved with its code still has its name. When no test
  in common kills it, the reason `rows --after` wrote does not count, since
  it says only where the text is: a person writes the row's `moved` reason
  and thereby says it is the same guard.

## What to do with an unplaced row

Read where the guard went. If it is the same guard at new text, write a row
with the same `source`, the new `file`, `old` and `new`, and a `moved` reason
in your own words. If two guards became one, add a `[[mapped]]` entry naming
the surviving row and why. If the guard is gone, the kill is lost: say so in
the record and on the card, never map it to a row that merely holds the same
line.

## Also true

A replay is what the tests of one commit kill. It resumes only from a
sidecar of that commit with no tracked file changed since, and the driver
reads each row's source against the table it names before anything runs.
