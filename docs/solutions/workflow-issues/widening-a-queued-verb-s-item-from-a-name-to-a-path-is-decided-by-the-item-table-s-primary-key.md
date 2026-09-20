---
title: "Widening a queued verb's item from a name to a path is decided by the item table's primary key, not by taste"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/core/discovery.py, src/cratekit/core/jobs.py, src/cratekit/analysis/cli.py, src/cratekit/vocals/cli.py"
problem_type: workflow_issue
component: job_engine
root_cause: unverified_assumption
resolution_type: code_fix
applies_when:
  - "A queued verb is given a recursive, multi folder or multi source mode and its item ids have to widen"
  - "A unit is choosing between a relative path, a bare name and a synthetic id for a job item"
  - "A verb's item id is joined to a frozen root with the path operator anywhere in a worker"
  - "A walk is added to a verb and something in the tree is skipped rather than read"
  - "A queue command and a resume command each report on the same run"
symptoms:
  - "An enqueue raises an IntegrityError only on a library that happens to hold one filename twice"
  - "A recursive queue looks correct on a fixture of unique names and fails on a real tree"
  - "A worker reads a file outside the folder the job froze and the report shows the right path"
  - "A resume envelope is missing something the queue envelope said, and both are the same run"
  - "A guard added beside an existing one kills zero tests because the existing one gets there first"
related_components:
  - job_engine
  - resume
  - analysis
  - vocals
tags:
  - queued-verbs
  - item-identity
  - job-resume
  - recursive-walk
  - symlinks
  - mutation-table
  - u93
  - r-376
  - r-409
---

# Widening a queued verb's item from a name to a path is decided by the item table's primary key, not by taste

## Context

U93 gave `analyze restamp` and `analyze vocals` a `--recursive` mode so one
invocation over the library root could replace 343, the number of leaf folders
R-376 measured on the author's library. Both verbs freeze a folder in the job
payload and store one item per audio file, and both read their subject as
`folder / item.item_id`.

The brief decided that item ids would become POSIX relative paths and called it
a decision. It is not a decision. It is forced, and the thing that forces it is
two lines away from anything the unit touches.

## What was not where it looked

`core/jobs.py` declares:

    CREATE TABLE IF NOT EXISTS job_items (
        job_id     TEXT NOT NULL,
        item_id    TEXT NOT NULL,
        ...
        PRIMARY KEY (job_id, item_id)
    )

**The item id is a uniqueness constraint, not a label.** A recursive walk that
kept bare filenames hands `enqueue` two rows called `track.flac` the first time
a library holds that name in two genre folders, and the insert raises. Every
real DJ library holds that: an original in one bucket and an edit in another,
the same track filed under two energies, a compilation cut that appears twice.

This is the failure mode that hides perfectly in a fixture. A test tree authored
alongside the feature has unique names because the person writing it types
unique names. The bug is not in the walk, not in the verb, not in anything the
diff touches, and it surfaces only on somebody's real library.

**The rule this generalises to:** before widening what a queued item is, read
the item table's constraints, not the worker that consumes it. The consumer
tells you what the id has to MEAN. The schema tells you what it has to BE.

## The second thing the widening changes, which is a join

Once an item id may contain separators, this stops being an expression and
becomes a guard:

    folder / item.item_id

`Path("/library") / "/etc/passwd"` evaluates to `/etc/passwd`. An absolute right
hand side discards the base silently, and a `..` segment walks out of it one
level at a time. While every id was a bare filename produced by `iterdir` this
could not fire. The moment ids are path shaped it is a real surface, so the join
moved into `discovery.item_path`, which refuses an absolute or `..` id as a
defect rather than joining it.

Both verbs' `_folder_and_path` route through it, and the mutation table pins
both reversions separately, because "a fix that lands on one of two identical
call sites" is this project's third recurring defect pattern.

## Walking a tree means choosing what NOT to read, and saying so

A walk meets things a single `iterdir` never did. Three of them here:

* **A directory symlink.** `os.walk(followlinks=False)` makes a loop impossible
  by construction rather than survivable by a visited set that has to be
  correct. The cost is that a genre folder kept as a link contributes nothing.
* **A folder the process cannot list.** `os.walk` SWALLOWS the `OSError` unless
  you pass `onerror`. Without it, a permission or a failing enclosure produces
  no items and no complaint.
* **A dot directory.** `.Trashes` and `.Spotlight-V100` sit at the root of every
  exFAT stick, which is what a DJ stick is.

The first two are the same defect shape as the AppleDouble sidecar rule that was
already there: a clean report over state the tool never read. They are worth two
DIFFERENT warning codes and not one, because a declined link needs no action and
a locked folder needs somebody to fix a permission, and a warning whose remedy is
ambiguous gets ignored.

**What does NOT widen:** `analyze run`. Its last act on a track is a rename and
its resume marker is the Camelot head on the NAME, so its item identity is bound
to the filename. That constraint is already written up in
`a-worker-that-renames-its-item-owes-the-resume-an-exact-record`, and it is why
the third analysis verb was left alone deliberately rather than by oversight.

## The resume is the report, and it never re-walks

A queued verb has two exits. The queue envelope is the one a person scrolls
past; the resume envelope is the report that says the pass finished. An omission
put only on the queue is an omission most people never see, which is the same
shape as
`a-queued-verb-has-two-exits-and-an-advisory-on-the-envelope-only-reaches-one`.

The fix is NOT to re-walk on resume. Re-walking measures the tree as it is now
and reports it over a job queued against the tree as it was, which is a
different and worse lie. The walk's omissions are frozen into the payload beside
the mode, and the resume phrases them back through the same function the queue
used, so the two cannot describe one omission two ways.

## What the mutation table found that the review did not

`followlinks=False` kills zero tests. It is COVERED: the explicit `is_symlink()`
decline prunes every link out of `dirnames` before `os.walk` reaches the
question, so the keyword never gets to act. Its composite, removing the decline
and leaving the keyword, kills 6.

That is this repository's "a guard covered by another guard is a guard nothing
covers", and it is worth naming here because the covering guard was added in the
SAME commit. A redundant guard written by the same hand on the same day reads as
defence in depth and measures as decoration. The keyword stays, the zero is
recorded as R-589 with its composite, and the pair was deliberately not mutated
together because removing the decline while following links is the symlink loop
itself, which hangs a suite rather than failing it, and a hung driver leaves a
partial mutation in the source.

## Cost

One unit. The primary key was read before anything was written, so it cost
nothing here and would have cost a real library's first recursive pass. The
review round found the swallowed `os.walk` error, a plural only sentence, and
the resume half of the warning. The mutation table found the covered guard and
one genuine coverage hole, where dropping the unreadable half of the resume
warning killed zero because every resume case in the suite froze links only.
