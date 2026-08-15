---
title: "R-115 read five CI failures as platform from a run list, and driving one found a shallow checkout instead"
date: 2026-08-15
category: workflow-issues
module: .github/workflows/ci.yml
problem_type: workflow_issue
component: development_workflow
severity: high
resolution_type: workflow_improvement
applies_when:
  - "A residual or finding attributes a failure to a cause without reproducing it"
  - "A test guard derives its expectations from git history: git log, git blame, or a tag list"
  - "CI checkout behavior is assumed to match a local clone's history depth"
  - "A finding's own text says it was filed by reading a run list rather than a run"
  - "A CI job is being judged for whether it can ever pass in its current environment"
symptoms:
  - "CI fails consistently on tests that pass locally, attributed to platform without reproduction"
  - "A guard built on git log --grep fails only in CI and nowhere else"
  - "actions/checkout@v4 defaults to a one commit shallow clone, and a guard deriving its file list from git history sees almost none of it"
  - "git fetch --unshallow turns the same failures green with no code change"
  - "Five of the failures were named platform on inspection and none of the five was reproduced"
related_components:
  - testing_framework
  - tooling
  - documentation
tags:
  - ci
  - shallow-clone
  - git-log
  - root-cause
  - driven-verification
  - platform-attribution
  - github-actions
  - false-diagnosis
---

# R-115 read five CI failures as platform from a run list, and driving one found a shallow checkout instead

## Context

R-115 in `docs/residual-findings.md` (heading at `:7133`) records that every CI
run on `main` had failed for ten consecutive commits while the local battery was
clean for every one of them, so a red run distinguished nothing. That
observation was correct and it was worth recording. The entry then named the
cause, and every cause it named was the platform: `hdiutil` absent, so
`tests/test_hardware_fixtures.py` and `tests/test_adoption_hardware.py` fail
rather than skip by design; `rclone` absent, so `tests/test_restore.py` fails;
`test_committed_calibration_loads` refusing a timing calibration captured on a
different machine; and one deletion test receiving `OS linux not supported!`.
The entry says, in its own first line, that it was filed "by looking at the run
list rather than at a run".

That last sentence was honest and it was also the defect. On 2026-08-15 the
cause was driven rather than read, and the largest single group of failures on
the last red run turned out to have nothing to do with Linux. Five tests in
`tests/modules/test_reports.py` fail on any checkout with one commit of history,
on any operating system, because they derive what they check from `git log`.
`actions/checkout@v4` fetches one commit by default. The runner was not failing
because it was Linux; it was failing because it had no past.

The decision that closed R-115 (commit `e1bf172`, "ci: the workflow proves
packaging and portability, and stops running the suite", merged to `main` as
`b22e6a7`, "merge: R-115, CI proves packaging and portability rather than
nothing") did not depend on which reading was right, because the platform
causes are real too and the suite cannot pass on a hosted runner either way. But
the diagnosis was going to be written down as the reason, in the residual entry
and in METHOD, and a wrong reason in a durable record is exactly the thing this
directory's neighbouring documents are about. So the entry got a third
subsection, "THIS ENTRY'S OWN ACCOUNT OF THE CAUSE WAS INCOMPLETE, corrected by
driving it", and this document is the general form of what it says.

## Guidance

**A cause named from a log is a hypothesis.** METHOD's merge bar
(`docs/METHOD.md:17`, condition 1) says a finding is BLOCKING only if "it was
driven end to end, not argued from reading the source". The sibling document one
level up extended that from a finding's existence to a finding's mechanism. This
one extends it to a finding's CAUSE. Reading a run list tells you that a thing
is red. Reading a run's log tells you which tests are red and what their
assertion messages say. Neither tells you why, and an explanation that fits the
log is not the same as one that has been reproduced. R-115 fit five causes to a
log, all of them plausible, all of them platform, and the biggest group of
failures fit none of them.

**Before blaming the platform for a red CI run, clone at depth 1 on the machine
you have and run it.** This is the concrete rule, and it is ninety seconds. Most
of the ways a CI checkout differs from a developer checkout have nothing to do
with the operating system: it is shallow, it is clean, it has no untracked
files, it has no remote branches fetched, it has no `origin/main` to diff
against, and its `HEAD` may be a detached merge commit. Every one of those can be
reproduced on the laptop with `git clone --depth 1`. Do that first. Whatever is
still red after `git fetch --unshallow` on the same machine is the part that
might be the platform, and it is a smaller list.

**Any guard that reads git history has a truth that depends on how much history
the checkout has, and that dependency is invisible on a developer clone.** This
is the mechanism worth naming. `tests/modules/test_reports.py` derives which
files U34 writes and which residuals U34 filed by asking git which commits carry
the tag `(U34)` in their subject: `UNIT_COMMIT_TAG` at `:4308`, `_unit_log` at
`:4318` running `git log --format= -F --grep=(U34) HEAD`, `_unit_commits` at
`:4334`, `_files_this_unit_writes` at `:4342`,
`_files_this_unit_writes_by_a_second_route` at `:4374`, and
`_residual_titles_this_unit_filed` at `:4550`. On a full clone at `138c4e5` that
query finds fourteen commits and names twenty five files, re-driven while this
document was validated. The source's own docstrings at `:4306` and `:4357` still
say thirteen and twenty three, which were true when measured on the branch and
went stale when two later commits carried the tag: the very shape this document
is about, sitting inside the code it describes. On a clone with one commit whose
subject does not carry the tag it finds nothing, so the derived file list is
empty and the derived residual list is empty. A developer never sees this,
because a developer clone always has the whole history and a worktree shares it.
The design was chosen deliberately, and the docstring at `:4289` through `:4307`
says why: it replaced a merge base derivation that went empty once the branch
WAS main. It traded one history dependency for another, and the new one is
narrower but not zero.

**The guard failed honestly, and that is the design working.** The authors of
these guards anticipated an empty git derivation and refused to let it pass
silently. `_covered_files` at `:4429` asserts a typed floor of seventeen files,
`CITED_FLOOR` at `:4268`, is covered even when both derived routes go quiet;
`_banned_addresses` at `:4620` asserts at least `RESIDUALS_FILED_FLOOR` (`:4537`,
twelve) residuals were found; and
`test_the_named_floor_still_bites_when_both_derivations_narrow_together` at
`:4717` exists precisely because "a git derivation that answers emptily narrows
both routes at once". So on a shallow checkout the guards say `assert 0 >= 12`
and `assert 0 > 17` and fail loudly, which is what they were built to do. Nothing
here is a bug in the guard. What went wrong is that the person reading the red
run had a platform story already and did not open the five failures that did not
fit it.

**Say which attributions were driven and which were read, in the record.** The
corrected entry lists three groups. The five in `test_reports.py` are marked
"Driven on macOS, 2026-08-15". The Unicode composition pair in
`tests/test_adoption.py` and `tests/test_deletion.py`, and the four cgroup reader
failures in `tests/test_pool_sizing.py`, are marked "NOT DRIVEN, because no Linux
machine was available". Both are in the same entry, side by side, so a reader
knows how much to trust each. That is METHOD's rule at `:154` applied to a
diagnosis: "Every number was measured or the report says it was not." An
attribution that could not be driven is not worthless, but it has to be filed as
a reading, and a reading is a different measurement from a reproduction.

**The decision can be right while the diagnosis is wrong, and you still fix the
diagnosis.** Stopping the suite in CI was correct on the platform causes alone,
since `hdiutil` and the committed calibration will never pass on a hosted runner.
The shallow checkout finding would have been a one line workflow fix,
`fetch-depth: 0`, had it been the only cause. It was not the only cause, so the
decision stands. The reason to correct the entry anyway is that R-115 is a
durable record, METHOD now cites it as the thing that bought the CI rule, and a
future reader working out why the workflow does not run pytest will read the
causes and believe them. A durable record that names the wrong cause teaches the
wrong lesson every time it is opened.

## Why This Matters

1. **2026-08-14, after the U12 merge.** R-115 is filed. Ten red runs on `main`
   are counted from the run list. Five causes are named. All five are platform,
   and all five are real: those tests genuinely cannot pass on ubuntu. The entry
   says it was written from the list rather than from a run. The prior session's
   own record shows how short that reading was: at 23:11 the agent noticed "a
   failed CI run to look at", ran `gh run list`, and at 23:12 concluded "CI
   failures are all pre-existing and environmental: a Linux runner with no
   hdiutil, no rclone, and a different CPU count", then moved on to syncing the
   board. About one minute, no run opened (session history).

2. **What was not looked at.** The last red run's log holds more failures than
   the five named causes explain. Five of them are in `tests/modules/test_reports.py`,
   whose failing assertions are `fewer residuals filed than this unit is known to
   have filed: []` and `the two would be indistinguishable`. Neither message
   mentions a tool, a path, or an operating system. They say the derivation found
   nothing.

3. **2026-08-15, driving it.** A `git clone --depth 1` of the repository on macOS,
   the same machine the battery runs on, and `pytest tests/modules/test_reports.py`
   in the clone. Five failed, 344 passed, and the five are exactly the five from
   the run log. `git fetch --unshallow` in the same clone, same command: 349
   passed. The operating system did not change between the two runs. The amount
   of history did.

4. **The mechanism, from the source.** `_unit_commits` at `:4334` runs
   `git log --format=%H -F --grep=(U34) HEAD`. On the shallow clone `HEAD` is the
   only commit and its subject is a docs commit with no `(U34)`, so the tuple is
   empty. `_files_this_unit_writes` at `:4342` then contains only working tree
   changes, of which a fresh clone has none. `_covered_files` at `:4443` compares
   that against `CITED_FLOOR` and refuses at `:4444`. `_residual_titles_this_unit_filed` at
   `:4550` reads an empty diff and returns nothing, and `_banned_addresses` at
   `:4620` refuses that too. Every one of those refusals is a floor the guard's
   own authors put there for exactly this shape.

5. **The correction, and where it landed.** The residual entry gained its third
   subsection saying the account was incomplete and which parts were driven.
   `docs/METHOD.md` "What CI is for, decided 2026-08-15" (`:194`) closes with the
   paragraph "Before blaming the platform for a red CI run, drive it", carrying
   the same counts. `RESTART-cratekit.md:123` carries it as a driver rule.
   `.github/workflows/ci.yml` carries the decision in its header comment and no
   longer runs pytest anywhere. The first green CI run on `main` followed the
   merge.

6. **What would have happened otherwise.** The residual, METHOD and the workflow
   header would all say the suite is red in CI because of the platform. The next
   person to add a history reading guard would have no reason to think about
   checkout depth. And the next time a shallow checkout bit, in CI or in a fresh
   clone on a new machine, the platform story would be the first thing they read
   and the last thing they questioned.

## When to Apply

- A CI run is red and the local battery is green. Before writing down why, clone
  the repository at depth 1 on the machine you are sitting at and run the failing
  file. Then unshallow and run it again. Whatever survives both is the candidate
  platform list.
- You are writing a residual, a METHOD section, or a workflow comment that names
  the CAUSE of a failure. Ask whether the cause was reproduced or inferred, and
  write which. "Read from the log" and "driven" are both acceptable words in this
  repository's records; leaving the distinction out is not.
- You are adding or reviewing a test that shells out to `git log`, `git diff`,
  `git merge-base`, `git rev-list` or anything else that answers differently
  depending on how much of the repository is present. Say in its docstring what
  it needs from the checkout, and make sure the floor that fires when the
  derivation goes empty says so in its message.
- You already have an explanation that fits the symptoms and it is a
  comfortable one. That is the moment to open the failures that fit it least
  well, because those are the ones the explanation is not covering.
- The decision the diagnosis feeds would be the same either way. That is not a
  reason to skip correcting the diagnosis. The decision is made once; the record
  is read every time somebody wants to know why.

## Examples

### The shell sequence that drove it

Run from any scratch directory on the laptop, using the main checkout's venv,
which is safe here because `pyproject.toml:173` sets `pythonpath = ["src"]` so
pytest imports the tree it sits beside rather than the editable install.

```
git clone --depth 1 file:///path/to/Cratekit shallow
cd shallow
git rev-list --count HEAD
# 1
/path/to/Cratekit/.venv/bin/python -m pytest \
    tests/modules/test_reports.py -o addopts= -q
# FAILED tests/modules/test_reports.py::test_this_units_residuals_are_cited_by_title_and_never_by_number
# FAILED tests/modules/test_reports.py::test_a_coverage_list_narrowed_by_one_file_is_refused_whichever_file_it_is
# FAILED tests/modules/test_reports.py::test_the_ban_list_is_the_residuals_this_unit_filed_and_nothing_else
# FAILED tests/modules/test_reports.py::test_a_renumber_moves_every_address_and_the_ban_list_follows_it
# FAILED tests/modules/test_reports.py::test_the_collision_passage_is_the_only_exemption_and_it_is_delimited
# 5 failed, 344 passed

git fetch --unshallow
git rev-list --count HEAD
# 265
/path/to/Cratekit/.venv/bin/python -m pytest \
    tests/modules/test_reports.py -o addopts= -q
# 349 passed
```

`-o addopts=` clears the `-q` the project config sets so the FAILED lines print
by name. The whole sequence, both runs included, is under two minutes. It was
re-run while this document was written, against `main` at `138c4e5`, and the
counts above are from that re-run.

### The two assertion messages, and what they say

```
E   AssertionError: fewer residuals filed than this unit is known to have filed: []
E   assert 0 >= 12
tests/modules/test_reports.py:4620

E   AssertionError: the two would be indistinguishable
E   assert 0 > 17
tests/modules/test_reports.py:4710
```

Both are floors firing on an empty derivation. Neither names a tool, a path, or
an operating system. A reader with a platform explanation in hand can scroll past
both; a reader asking "what did this test actually derive" sees the empty list
in the first message and has the answer.

### How the corrected entry records the split

From R-115's third subsection, the shape to copy when part of a diagnosis could
be driven and part could not:

> Five in `tests/modules/test_reports.py` are a SHALLOW CHECKOUT. [...] **Driven
> on macOS, 2026-08-15**, on a `--depth 1` clone of this repository: the same
> five fail, 344 pass. `git fetch --unshallow` and all 349 pass. Nothing about it
> is the platform, and it would have been a one line workflow fix.
>
> Two in `tests/test_adoption.py` and two in `tests/test_deletion.py` are about
> one file in two Unicode composition forms, which APFS normalises and ext4 does
> not. Platform, and NOT DRIVEN, because no Linux machine was available.
>
> Four in `tests/test_pool_sizing.py` are U12's cgroup reader meeting a real
> cgroup filesystem. Platform, and NOT DRIVEN, for the same reason.

The words "driven" and "not driven" appear on every group. That is the whole
technique.

## Related

- `a-rewrite-is-not-a-re-measurement-of-the-claim-inside-it.md`: the same shape
  one level up. That document extends METHOD's "driven, not read" from a
  finding's existence to a finding's mechanism, and to the standing instructions
  a merge inherits. This one extends it to a finding's cause. In both cases the
  author had a true observation, wrote a confident explanation around it from
  reading rather than running, and the explanation was the part that was wrong.
  There the wrong sentence sat in a docstring; here it sat in a residual entry
  that METHOD was about to cite as the reason for a rule.
- `a-false-claim-in-the-auto-loaded-contract-compounds-silently.md`: the radius
  argument. A wrong cause in R-115 is read by whoever opens R-115; the same wrong
  cause carried into `docs/METHOD.md`, which every session reads, would be read
  by everybody. That is why the METHOD section was written with the corrected
  account and the counts rather than with the original five causes.
- `docs/METHOD.md:194`, "What CI is for, decided 2026-08-15": the rule that a
  step in the workflow must be able to pass and a check that cannot belongs in
  the battery, and its closing paragraph "Before blaming the platform for a red
  CI run, drive it". `docs/METHOD.md:17`, merge bar condition 1, "It was driven
  end to end, not argued from reading the source", is the rule this document is
  an application of. `docs/METHOD.md:154`, "Every number was measured or the
  report says it was not", is the form the correction takes.
- `docs/residual-findings.md:7133`, R-115, with its two appended subsections
  "DECIDED 2026-08-15, by a fourth option, and this finding is CLOSED" and "THIS
  ENTRY'S OWN ACCOUNT OF THE CAUSE WAS INCOMPLETE, corrected by driving it". The
  first records the decision and the three options it rejected; the second is the
  correction this document generalises.
- `.github/workflows/ci.yml`: the header comment carries the decision, the
  `portable` job replaces `test` and runs no pytest, and `cold-install` runs on
  3.12 and 3.13. Every `actions/checkout@v4` step in it still fetches one commit,
  which is fine now precisely because nothing in the workflow reads history.
- `tests/modules/test_reports.py:4268` through `:4460`: `CITED_FLOOR`, `UNIT_COMMIT_TAG`, the
  three git derivations, and `_covered_files`. The block's own
  docstrings record why it reads commit subjects rather than a merge base, and
  the floors in it are what turned an empty derivation into a loud failure rather
  than a silent pass.
- Commits on `main`: `e1bf172` "ci: the workflow proves packaging and
  portability, and stops running the suite", whose body carries the
  contemporaneous account of the drive, and `b22e6a7` "merge: R-115, CI proves
  packaging and portability rather than nothing", the merge that closed issue
  #55. `138c4e5` "docs: the wave state after the 2026-08-15 batch, nine units
  merged and CI green" records the first green run.
- `RESTART-cratekit.md:123`: the same lesson as a one paragraph driver rule for
  the next session.
