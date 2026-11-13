---
title: "A foreground mutation driver is killed by the harness tool ceiling and leaves the source mutated"
date: 2026-09-17
category: workflow-issues
module: scripts/mutate.py
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: undocumented_tool_behavior
resolution_type: sequencing_change
applies_when:
  - "scripts/mutate.py is about to be run for a unit's mutation table"
  - "A long running driver is being started and METHOD says to run it in the foreground"
  - "The source file a unit touched is unexpectedly dirty and nobody edited it"
symptoms:
  - "A Bash call reports the command was moved to the background after about ten minutes"
  - "git status shows a modified source file after a driver run that nobody edited"
  - "A trailing comment reading 'mutation driver null control, restored automatically' is in the source"
  - "docs/mutation/<name>.json does not exist after a long driver run"
tags:
  - mutation-table
  - mutate.py
  - driver
  - harness
  - tool-ceiling
  - working-tree
---

# A foreground mutation driver is killed by the tool ceiling and leaves the source mutated

## Context

U65 (issue #88) needed its author's mutation table. METHOD's driver rules said, in
the words they carried at the time, "Run rows synchronously in the foreground. A
backgrounded driver outlived its parent twice and contaminated later rows." That
rule was bought by two real incidents and reads as unambiguous.

It cannot be followed here, and the reason is not in this repository.

## What is actually going on

`scripts/mutate.py` runs a full baseline suite before any row, because a row
measured against a red baseline reads as a death. (Since U271 it reads that
baseline from the cloud battery's record of the same commit when every key
matches, and the null control is still a full run, so the overhead below
shrinks by one run and the rule stands.) On this suite that baseline is
about 400 seconds run by hand and longer under the driver, which runs pytest with
`-o addopts=` and its own report plugin. Add the per subset baselines and the null
control and the fixed overhead alone is past 600 seconds.

600 seconds is the harness's maximum Bash timeout. A foreground call that exceeds
it is not failed, it is **moved to the background and then killed**. Measured three
times in one session: a 25 row run, a repeat, and a deliberately minimal ONE row
probe. All three died. The one row probe is the important measurement, because it
proves the overhead is fixed rather than proportional to the table.

Two of the three died while a mutation was applied, and left the tree dirty. One
left this in `src/cratekit/acquire/listing.py`:

```
# mutation driver null control, restored automatically
```

That is the null control's own text, stranded because the process that promised to
restore it was killed. The same artifact is recorded in
`docs/mutation/sitting4-notes.md` from the fourth attended sitting, where it was
attributed to memory pressure. It was the tool ceiling.

Nothing is lost from the table itself: the driver rewrites its JSON sidecar after
every row, so a killed run resumes. What is lost is the tree's cleanliness, and a
session that does not check will run its battery over a mutated source.

## The correction

**The rule's target was never the foreground. It was a driver outliving its
parent while something else ran.** Those are different things, and on this harness
they point in opposite directions: the background job is tracked, runs to
completion and restores as designed, while the foreground job is the one that gets
killed holding a mutation.

So the rule is now one driver at a time, waited on, with nothing else touching the
tree, and `git status` checked when it reports. `docs/METHOD.md`'s driver rules
carry the corrected version.

The 25 row run that succeeded took about 25 minutes as a tracked background job
and ended clean: 23 killed, 2 zeros, no collect drift on any row, `head_verified`
true on all 25, null control 0.

## What to carry forward

- **Check `git status` after any driver run, including one that looked like it
  failed.** A killed driver is not a no op. If the source is dirty, restore it with
  `git show HEAD:<path> > <path>` and never from a scratch copy, which is the rule
  that already existed and is what makes this recoverable.
- **A run that produced no `docs/mutation/<name>.json` got nowhere**, because that
  file is written after every row. No sidecar means the kill landed during the
  baselines, and `--resume` has nothing to reuse.
- **Before blaming memory pressure or the machine for a driver that vanished,
  check the elapsed time against the tool ceiling.** The fourth sitting attributed
  this to memory and it was not.
- **The same ceiling applies to the full suite**, at about 400 seconds, which
  leaves little headroom. A unit that makes the suite slower should notice; U65
  took 31 seconds off it by accident, and that was the difference between a listing
  subset that ran in 32 seconds and one that ran in 1.2.
