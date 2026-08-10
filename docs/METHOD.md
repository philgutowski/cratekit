# Method

This file is the operating instruction for the review wave. It is deliberately
fixed in size. It replaces the practice of having every agent read two long
narrative snapshots before doing any work.

The `docs/wave-state-*.md` files are HISTORY. They record what was measured and
why decisions were taken. Read one when you need the reasoning behind a rule.
Do not read them to find out how to work. That is this file.

## The merge bar, decided 2026-08-09

A branch merges when it has no open BLOCKING finding.

**A finding is BLOCKING only if all three hold:**

1. It was driven end to end, not argued from reading the source.
2. It has a named user facing cost. Someone loses data, is told something
   false, is blocked from a verb, or is shown a clean report over state the
   tool could not read.
3. **Its input is reachable, and the producer was DRIVEN.** A cost over an
   input nothing can produce is not a cost. Name the producer and drive it. If
   you cannot, the finding is a RESIDUAL and the report says the reachability
   is unmeasured. Say "N candidates were driven and none produces it", never
   "nothing produces it", because those are different measurements.

Condition 3 was added 2026-08-10 after a verifier returned BLOCKING on a
document it had hand mutated, and a second pass then drove four candidate
producers and found none. Establishing reachability inside the first pass costs
almost nothing. A second trip to establish it cost 258k tokens.

**Everything else is a RESIDUAL.** A docstring that overclaims, an assertion
that names the wrong number, a guard that kills zero tests, a document whose
count an independent table does not reproduce: all real, all worth recording,
none of them a reason to hold a merge. File them in `docs/residual-findings.md`
with their measured cost.

This floor exists because the previous bar, "the verifier found nothing", is
not a reachable state. A mutation table over a suite this size always finds a
zero death row, because that is a property of large test suites rather than of
any branch. Twenty consecutive blocking verdicts measured that.

**And a hard cap: each unit has at most two fix rounds left.** When they are
spent the unit merges, and every finding still open becomes a residual. The
floor is meant to end the loop on merit. The cap is what guarantees an end date
if it does not.

## Verification depth is proportional to blast radius

Full adversarial pass, independent verifier, for units that write or delete:
U12, U23, U24, U27, U32.

Light pass for read only reports and static registries: U16, U34, U38. A light
pass still derives its own table and is still run by an agent that did not
write the code. It is scoped, not trusting.

## Three things per agent, never shared

Its own worktree, its own venv, its own scratch directory named for its unit.

The venv rule exists because the editable install names the main checkout's
`src`, so a worktree with a symlinked venv verifies code it cannot see. Never
symlink one.

The scratch rule has the same shape and the same failure mode. A shared scratch
directory has collided twice on this project, once across eight agents and once
across three. Neither corrupted a measurement, and both times that was luck.

## The mutation table

Revert each new guard one at a time, run the suite, count the deaths. A guard
that kills zero tests is a finding.

**Scope it to the round's own diff**, plus a fixed sample of the unit's
existing guards. An eighty row sweep of the whole unit on every round is where
the budget goes and its yield is concentrated in the new code.

**Hard row caps: 25 rows on a light pass, 45 on a full one.** Nominal scoping did
not hold. Light passes ran 50 and 89 rows on 2026-08-10. When you hit the cap,
stop and **log what you dropped and why you ranked it below the cap**, so a
truncation is visible rather than read as coverage. One pass per unit per
session.

**Use `scripts/mutate.py`. Do not hand roll a driver.** It takes rows as data
and returns the table, and it holds every driver rule below as a property rather
than as an instruction you have to remember. Three of this project's recorded
incidents were hand rolled driver mistakes. The rules are kept below because you
still need to know what the script guarantees and why.

**Confirm deaths on a subset, spend a full suite only on zero rows.** Select
the subset as the test files importing the mutated module. A death on a subset
is a real death. A zero on a subset is not yet a zero, so promote it to a full
run before you report it.

**An author's own table is a draft, not a result.** Every fix agent on this
project has run its table honestly and still missed guards its own round
created, because it mutates what it believes it changed. Measured gaps between
an author's table and an independent one: 10 against 17, 39 against 49, 49
against 83.

**A zero death row on a guard with a USER FACING surface is acceptable only
when a composite shows what it does hold.** Pair it with a mutation of the thing
it guards and report both counts. A prose argument is not evidence.

**A zero row on a maintainer facing guard gets one line, not a composite.** The
severity floor says such a row can never block, so the composite buys
documentation rather than a decision. Measured 2026-08-10: one verifier produced
40 zero rows, another 14, another 11, and nearly every one was an assertion
about this repository's own source. Record it and move on.

**Write the table into the repository**, with full row descriptions and not
only counts, under `docs/mutation/`. A table that lives only in a chat message
is a claim. One was lost that way and a verifier could not check it.

## Reading discipline, because context is what you are billed for

Cost measured 2026-08-10 was a flat 2,400 tokens per tool call across four
agents. Every tool result stays in context and is re-sent on every later call,
so the bill is tool calls times context size. Thinking is cheap here. Reading is
not.

- **Never read a file over 400 lines whole.** Grep for the symbol, then read the
  region around it.
- **Every report opens with a verdict header under 60 lines**: the verdict, a
  numbered finding table with each finding's classification, and the battery
  numbers. A later agent reads the header and stops unless it needs a specific
  finding's detail.
- **Do not re-read a prior round's full mutation table.** Read its summary rows.

## Driver rules, every one of them paid for

- **Never pass `-q`,** including to a collection run. `pyproject.toml` already
  sets it, so yours becomes `-qq` and suppresses the summary line and the
  collect listing. Use `pytest --tb=no` for counts and
  `pytest --collect-only -o addopts=` for the collected count.
- **Check the collected count on every row.** A file that fails to COLLECT
  takes its tests with it and the run still looks green.
- **Run rows synchronously in the foreground.** A backgrounded driver outlived
  its parent twice and contaminated later rows.
- **Never let a driver invoke git.** `git checkout` silently discards
  uncommitted edits. Snapshot and rewrite file text yourself.
- **Verify restores against `git show HEAD:<path>`,** never against a scratch
  copy. A contaminated scratch copy certifies itself.
- **Set `PYTHONDONTWRITEBYTECODE=1`.** Two mutations of identical byte length
  written a second apart make CPython reuse cached bytecode and invent a result.
- **Read node ids from pytest report objects,** never by splitting a `FAILED`
  line on `" - "`. That separator appears inside parametrized ids here.
- **Reword a message mutation, never append.** The suite asserts with `in`.
- **Mutate to a realistic nearby value, and mutate coefficients too.** A bound
  whose multiplier can be halved with a green suite is not pinned.
- **Remove each guard layer alone.** A guard covered by another guard is a
  guard nothing covers.
- **A timing row carries a repeat count and a pass rate,** never one number.
- **Every number was measured or the report says it was not.** Offer no
  mechanism for a discrepancy without a measurement showing it operating.

## The four recurring defect patterns

1. **Absence read as evidence of absence.** "I could not observe" folded into
   "there is nothing there". The most productive pattern in this codebase.
2. **Identity that is not unique to the thing it identifies.** A path digest, an
   inode pair, a symbol fingerprint. Each was a single field trusted alone.
3. **A fix that lands on the performing path instead of the checking path.** It
   is correct in isolation and the hole stays open. One branch produced three in
   a row.
4. **A fix justified by a measurement taken on a fixture rather than on the
   tree.** The most dangerous, because it arrives with a confident number, a
   defensible argument and a green suite. Ask of every justifying number:
   was this taken on the tree, or on something authored alongside the fix?

A fifth, implied by all of them: **a fix round fixes the instance it was handed
and reproduces the class one file over.** After every fix, go looking for the
same shape elsewhere and say what you found.

## What a green suite cannot see, so hunt it separately

- A test whose expected value comes from the code under test, reducing the
  assertion to X equals X while genuinely exercising the code. Sweep with an
  AST walk over every `assert` in `tests/`, not a grep.
- A test that forbids a feature by naming the last implementation's symbols. It
  forbids that implementation, not the feature.
- Duplicate keys in a mapping several branches appended to.
- One symbol meaning two things in two modules.

## The battery

Nothing merges until all three are clean, run from inside the worktree with its
own venv:

    ./.venv/bin/ruff check src tests scripts
    ./.venv/bin/python -m pytest --tb=no
    ./.venv/bin/python scripts/scan_repo.py

## Committing and merging

- **No pull requests.** Feature branch per unit, merge to `main` locally, push
  `main`, delete the branch in both places now that branches are on the remote:
  `git branch -d <branch>` then `git push origin --delete <branch>`.
- **`git push origin --all` fails on this connection** with `RPC failed; HTTP
  400`. Push one branch at a time. `http.postBuffer` is already raised and does
  not fix it.
- **No em dashes, no en dashes, no double hyphens** in prose, comments, commit
  messages or issue bodies.
- **U24 and U27 merge WITHOUT closing trailers.** GitHub matches a closing
  keyword anywhere in a body, not only in trailer position. Before any merge
  commit, confirm this returns nothing:

      git log -1 --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

- **Residual numbers are APPEND ONLY. A number, once given, is that finding's
  for life.** Decided 2026-08-10, reversing the sequential renumber decided
  2026-08-09.

  At a merge, the numbers already on `main` DO NOT MOVE. The incoming branch's
  residuals are the ones that get fresh numbers, assigned above `main`'s current
  highest. Gaps are fine and are not tidied. A branch whose residuals collide
  with `main`'s is normal, because branches number independently, and the
  collision is resolved by moving the INCOMING side only.

  The renumber was certified safe on a sweep showing zero numeric `R-NN`
  citations in `src`, `tests` or `scripts`. That sweep missed a second surface:
  **GitHub issue titles carry the number in their text**, as in
  `R-14: Analysis-file paths are share-relative`. A renumber silently repoints
  every one of those at a different finding, and nothing in the repository can
  see it. Same defect class as a rule verified against source while a second
  surface carries the same coupling.

  Verify a merge with both of these:

      grep "^## R-" docs/residual-findings.md | sort | uniq -d   # must be empty
      git diff origin/main -- docs/residual-findings.md | grep '^-## R-'   # must be empty

- **Use git's merge algorithm only.** `diff3 -m` silently produces a broken
  merge of `tests/_pending.py`. Use a scratch clone and a real `git merge`.
- **Reconcile the collected count by identifier, not by total.** A total only
  check shows a healthy rise and hides a collapse.
- **Run `git log origin/main..main` before any push,** not only before a push
  you believe is a merge. A docs commit once carried a merge to the remote and
  fired a closing trailer before the battery had been run.

## Do not touch

U30's board state, U20, U29, R-9, A1, A2. The parked conformance branch is out
of scope until Phillip says otherwise, and its `write/metadata.py:195` defect is
still live on main.
