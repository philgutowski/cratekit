# Method

This file is the operating instruction, deliberately fixed in size, the one
document a session reads to learn how to work here; `CLAUDE.md` is the
contract and names the others. **The compound engineering plugin is out of the
loop**, decided 2026-09-07: no `ce-plan`, `ce-work`, `ce-code-review` or
`ce-compound`, the rules they enforced that were paid for kept below. Native
Relay is retired (`docs/METHOD-local.md`).

## The pipeline, one unit per session

A session takes one unit from the board and runs it to a pushed merge. A stop
with nothing recorded is the one ending the next session cannot diagnose, so
a decision that is genuinely the person's is recorded as a residual with the
options, and the conservative one is taken.

1. **Orient.** `board.py next`, `show N`, `start N` locally, `board.py cloud`
   in the cloud; the issue is the brief. Read this file, locally
   `RESTART-cratekit.md`, and grep what CLAUDE.md says to grep.
2. **Plan, as a message**, in plan mode locally: the seam, the files, the test
   scenarios from the brief, the residuals the unit closes, what is out of
   scope. Never a document (`docs/plans/` is closed, the record of units
   already built). Fix an insufficient brief in the issue body first.
3. **Build.** Guard first, then the code it governs, so a violation cannot be
   introduced silently. Commit in units of meaning with subjects that name the
   unit, `feat(u57): ...`.
4. **Review.** Locally the built in `/code-review`, in the cloud the
   `fable-reviewer` agent; drive every finding, apply what holds, commit the
   fixes, at most two rounds (the merge bar). Then the mutation table, then
   the hunts a green suite cannot see.
5. **Record.** Each residual is a file, `docs/residuals/<unit>-<slug>.md`, with
   no number, in the form `docs/residuals/README.md` gives; **one that meets
   the board bar says `issue: yes`**, since a finding nobody queued is a
   finding nobody does. The restart paragraph is its own file,
   `docs/restart/<unit>.md` (`u114.md`, `r572.md`), never a paragraph in
   `RESTART-cratekit.md`, which `scan_repo.py` refuses. A learning only on
   the bar below. No explainer.
6. **Merge** by Committing and merging below, then on `main`
   `board.py residuals --land`, commit what it numbered, push, delete the
   local branch, `board.py audit`, and file each issue `--land` names.

## Card sizes, decided by Phillip on 2026-11-02

The plan names the card's size, so the process is sized to what the card can
damage (U196). **A card that adds or changes a path that writes or deletes is
large, whatever its size in lines.** The merge bar, the two round cap and
every standing constraint are the same for every size.

- **Small**: under about 200 lines of source and no new or changed path that
  writes or deletes, or docs and skill text only. Medium effort, one review
  round by Fable at high effort, a second only if it finds something BLOCKING.
- **Medium**: everything else that writes or deletes nothing. High effort, up
  to two review rounds.
- **Large**: anything that writes or deletes. High effort, up to two review
  rounds, the full mutation table.

**A thread may build up to three small cards in the same module in a row**,
each its own unit on a fresh branch from `main`; the later ones reuse the
thread's Linux baseline unless `main` moved in `src`, `tests`, `scripts` or
`pyproject.toml` since it was measured.

## The merge bar, decided 2026-08-09

A branch merges when it has no open BLOCKING finding. **A finding is BLOCKING
only if all three hold:**

1. It was driven end to end, not argued from reading the source.
2. It has a named user facing cost: someone loses data, is told something
   false, is blocked from a verb, or is shown a clean report over state the
   tool could not read.
3. **Its input is reachable, and the producer was DRIVEN.** A cost over an
   input nothing can produce is not a cost. Name the producer and drive it; if
   you cannot, it is a RESIDUAL and the report says the reachability is
   unmeasured. Say "N candidates were driven and none produces it", never
   "nothing produces it".

**Everything else is a RESIDUAL**, filed with its measured cost: a docstring
that overclaims, an assertion naming the wrong number, a guard that kills zero
tests, a document count an independent table does not reproduce. "The
reviewer found nothing" is not a reachable state, so the floor ends the loop
on merit, and **a hard cap of two fix rounds per unit** guarantees an end.
**Round two reviews the fix, not the branch again** (U196): none when round one
found nothing BLOCKING and nothing under `src`, `tests` or `scripts` changed
after it; otherwise only the commits after round one, `git diff <round one
head>..HEAD`, the branch's diff at hand for context, hunting the class one
file over (the fifth pattern below).

## The board bar, decided 2026-09-18

Most residuals stay in the ledger and earn no issue. One earns an issue, the
moment it is filed, only when it is open and a person using the shipped verbs
pays for it in one of four ways: **(a)** files or database rows can be lost or
damaged, **(b)** the product says something false, a clean report over state
it could not read or a declared write it never performs, **(c)** a workflow a
DJ needs cannot finish, **(d)** a guard on a path that writes or deletes is
absent or kills nothing. A maintainer facing finding, a wording fix, a count
in a document, or anything that closes only at an attended sitting does not.

Its issue, labelled `residual` and put on project 2, is titled `R-N: ` and the
ledger heading EXACTLY, since `board.py audit` compares the two, and its body
opens `**Depends on:** none` and carries goal, key files, approach, test
scenarios and out of scope. Create it only AFTER `board.py residuals --land`
numbers the finding on `main`, since a number is not the finding's until then.

**Never write a literal dot claude path in a card**, title, body or comment,
not even to forbid one; describe the location in words.

## The mutation table

Revert each new guard one at a time, run the suite, count the deaths; a guard
that kills zero tests is a finding. **The author measures it, with no
independent verifier**, decided 2026-09-07. Independent tables have found more
(17 against 10, 49 against 39, 83 against 49), so a zero row reads "the author
could not kill it", in one line of the record, and Phillip may ask for a full
pass on a unit that writes or deletes. **Its depth is the blast radius**,
decided by Phillip on 2026-11-02 (U196): a unit that writes or deletes gets its
full 25 rows and a composite on every user facing zero, a read only report or
a static registry about 8 rows on its new guards and a line per zero, and a
change to docs or skill text alone no table and a line saying so. **Scope it to
the round's own diff**, plus a fixed sample of the unit's existing guards.
**Hard cap: 25 rows, one pass per unit per session**; at the cap, log what you
dropped and why, so a truncation is not read as coverage.

- **Use `scripts/mutate.py`, never a hand rolled driver.** It takes rows as
  data and holds every driver rule below as a property. Do not edit `tests/`
  while it runs: it restores only the src file it mutates.
- **Confirm deaths on a subset**, the test files importing the mutated module;
  a zero on a subset is promoted to a full run before it is reported.
- **The full baseline may be read, never the rest**, decided by Phillip on
  2026-11-13 (U271): the driver reads its full baseline from
  `cloud_battery.py`'s run record only when it is for this HEAD, the tree
  clean throughout that run and now, this host, boot, checkout and
  interpreter, the same known failures file by its sha256, and a run of every
  collected test with no `PYTEST_ADDOPTS`; otherwise it measures and says why.
  A red record refuses the batch. Every subset baseline is measured, the null
  control runs the full suite in the driver's own environment held to the
  read collected count, the table says which baseline was read and which
  measured, and `--measure-baseline` measures regardless.
- **A zero row on a guard with a user facing surface** needs a composite: pair
  it with a mutation of the thing it guards and report both counts; a prose
  argument is not evidence. **A zero on a maintainer facing guard** gets one
  line.
- **Write the table into the repository** under `docs/mutation/`, with full
  row descriptions; a table that lives only in a chat is a claim.
- **A restructuring is held to its recorded kills and its behaviour** (U297).
  It replays, with `scripts/killset.py` and the driver's uncapped `replay`
  pass, the kills recorded for the files it owns, before its first edit and
  after its last, and `killset.py check` fails on a kill lost and not mapped,
  with a reason, to a row that is killed; a unit's own table keeps its cap.
  And `scripts/behaviour_compare.py` compares what the scenarios under
  `tests/behaviour/` print, exit and write, base against branch, after a
  scenario is added for any touched verb that has none.
- **Duplication and seams are battery checks** (U296):
  `tests/test_duplication.py` fails on a copied block of six logical lines
  past its package's allowance in `tests/ratchets/duplication/`,
  `tests/test_import_rules.py` on an import crossing a package outside the
  rules, and `scripts/refactor_measure.py` measures both. `docs/DEVELOPING.md`
  documents these scripts, the `cloud-unit` skill the order they run in.

## Reading discipline, because every tool result is re-sent on every call

- **Never read a file over 400 lines whole.** Grep for the symbol, then read
  the region around it. Find a finding in the ledger, tens of thousands of
  lines, with `board.py residuals --search WORDS`, which names the file it is
  in, and read that entry. Never print every heading.
- **Delegate a sweep, keep the conclusion**, to a read only subagent.
- **Every report opens with a verdict header under 60 lines**: the verdict, a
  numbered finding table with each finding's classification, and the battery
  numbers.
- **Do not re-read a prior round's full mutation table**, only its summary.

## Driver rules, every one of them paid for

- **Never pass `-q`,** even to a collection run: `pyproject.toml` sets it, and
  `-qq` hides the summary and the collect listing. Use `pytest --tb=no` for
  counts, `pytest --collect-only -o addopts=` for the collected count.
- **Check the collected count on every row.** A file that fails to COLLECT
  takes its tests with it and the run still looks green.
- **One driver at a time, as a tracked background job, with nothing else
  touching the tree** until it reports, then check `git status` and every
  row's `head_verified`; never the foreground, whose 600 second tool ceiling
  kills a run mid row (U65, 2026-09-17).
- **Never let a driver invoke git.** `git checkout` silently discards
  uncommitted edits; snapshot and rewrite file text yourself.
- **Verify restores against `git show HEAD:<path>`,** never a scratch copy.
- **Set `PYTHONDONTWRITEBYTECODE=1`.** Two mutations of identical byte length
  a second apart make CPython reuse cached bytecode.
- **Read node ids from pytest report objects,** never by splitting a `FAILED`
  line on `" - "` or at a space; both appear inside parametrized ids (U268).
- **Reword a message mutation, never append.** The suite asserts with `in`.
- **Mutate to a realistic nearby value, and mutate coefficients too.**
- **Remove each guard layer alone**: one covered by another is covered by nothing.
- **A timing row carries a repeat count and a pass rate,** never one number.
- **Every number was measured or the report says it was not.** Offer no
  mechanism for a discrepancy without a measurement showing it operating.

## The four recurring defect patterns

1. **Absence read as evidence of absence.** "I could not observe" folded into
   "there is nothing there". The most productive pattern in this codebase.
2. **Identity that is not unique to the thing it identifies.** A path digest,
   an inode pair, a symbol fingerprint, each a single field trusted alone.
3. **A fix that lands on the performing path instead of the checking path.**
4. **A fix justified by a measurement taken on a fixture rather than on the
   tree.** The most dangerous, since it arrives with a confident number and a
   green suite. Ask of every justifying number where it was taken.

A fifth, implied by all of them: **a fix round fixes the instance it was
handed and reproduces the class one file over.** After every fix, look for
the same shape elsewhere and say what you found.

## What a green suite cannot see, so hunt it separately

- A test whose expected value comes from the code under test, X equals X.
  Sweep with an AST walk over every `assert` in `tests/`, not a grep.
- A test that forbids a feature by naming the last implementation's symbols.
- Duplicate keys in a mapping several branches appended to.
- One symbol meaning two things in two modules.
- The first caller of an engine owns its unreviewed failure paths:
  `git grep -n <engine> -- src` before binding a worker, and if the definition
  is the only hit, read the engine's error paths as your own.

## The battery

CLAUDE.md's three commands, from inside the checkout that holds the branch
with that checkout's own venv, the suite with `--tb=no`. It is parallel and
work stealing, `-n auto --dist worksteal` in `addopts` (U251), about twelve
minutes on a four core container; a venv made before 2026-09-18 needs
`pip install -e '.[dev]'` once, and `-n 0` serves a debugger or a profiler.

- **The full battery is the MERGE gate, not the edit loop**: while building,
  run the test files you touched; the full suite runs before the review,
  after each fix round and at the merge.
- **A new slow test is a finding.** `pytest --durations=10` at the merge: over
  ten seconds is a process pool, a disk image, or a real sleep nobody faked.
- **Run it on a COMMITTED tree**: `tests/modules/test_reports.py` reads every
  uncommitted and untracked file as U34's own and bans its residual numbers.
- **A worktree gets its own venv**, `python3.12 -m venv .venv` then
  `pip install -e '.[dev]'` (CLAUDE.md), and its own scratch directory named
  for its unit.

## What CI is for, decided 2026-08-15

**CI is not the merge gate and does not run the suite.** It proves packaging
and portability: the package installs from a clean checkout on 3.12 and 3.13,
the slim profile pulls in no DSP and no ML stack, the vendored downloader
shipped, ruff is clean, and no personal path or credential reached the tree.
**A step in `.github/workflows/ci.yml` must be able to pass**; a check that
cannot belongs in the battery (R-115). **Nothing is deselected.** Before
blaming the platform for a red run, drive it.

## Committing and merging

- **A pull request per unit, merged by the session that opened it once CI is
  green** (U158, 2026-10-28): every check on its head commit green, then
  merged through the API as a merge commit titled `merge(uN): <what landed>`
  ending with the closing trailer. **Never one that waits on a person**: no
  reviewer, no approval. Its body carries no closing keyword, which would
  bypass the closing check. CI judges its range and reads the card a merge
  will close off a `cloud/N-slug` head only, so a unit a register still owes
  cannot merge; a local unit's pull request is judged on its range, and its
  close on the push to `main`. A refused merge
  endpoint means a local merge with the same message, pushed. The `cloud-unit`
  skill's step 9 is how.
- **`git push origin --all` fails on this connection.** Push one branch at a
  time.
- **Check `tests/_pending.py` before writing a closing trailer.** If the
  register still owes the unit a module, merge without the trailer and close
  the issue when the register is discharged.
- **GitHub matches a closing keyword anywhere in a body, and in every commit
  of the pushed range.** Scan the RANGE before every push:

      git log origin/main..main --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

**NEVER WRITE A CLOSING KEYWORD ADJACENT TO AN ISSUE NUMBER, even to quote
one, even inside backticks, even to say it is unsafe.** Put words between
them, or name the unit. A branch already carrying one cannot be made safe by
the merge commit: rewrite those bodies, or expect the close and reopen the
issue after the push.
- **Residual numbers are APPEND ONLY; a number, once given, is that finding's
  for life.** It is given at landing and nowhere else (U124): a unit files its
  residuals unnumbered in `docs/residuals/`, and `board.py residuals --land`,
  which refuses off `main`, gives each the next number past the highest in the
  ledger, so numbers on `main` never move and gaps are fine. Issue titles
  carry the numbers, which is why a renumber is forbidden; a branch built
  before U124 that numbers its own entries takes fresh numbers at the merge.
  The ledger is the working file `docs/residual-findings.md` and its archive
  `docs/ledger/`, files of at most 5,000 lines by number range (U314);
  `--land` archives the working file's oldest entries when it passes that, and
  an amendment to an archived entry is made in its archive file. Verify a
  merge with:

      .venv/bin/python scripts/board.py residuals --check --against origin/main   # no heading duplicated or removed

- **Use git's merge algorithm only.** `diff3 -m` silently breaks a merge of
  `tests/_pending.py`.
- **A countdown entry is discharged in THREE edits in one commit, and one
  alone is worse than none**: delete the `PENDING` entry, delete its
  `EXPECTED_PENDING` key, and remove `@requires("<key>")` from EVERY guard it
  gated, after `grep -rn 'requires("<key>")' tests/`. Deleting only the entry
  raises `KeyError` at import and drops the guard's whole file from
  collection. Then run the newly armed guard on purpose.
- **Reconcile the collected count by identifier, not by total.**
- **A unit's restart paragraph is its own file** (U124); a branch built before
  U124 that conflicts in `RESTART-cratekit.md` moves its paragraph into its
  fragment and takes `main`'s file as it is.
- **Reserved-cause pins are per module** (U125): the populations in
  `tests/test_reserved_causes.py` are pinned through
  `tests/_pinned_reserved_populations.py`, kebab literals and holders one file
  per package under `tests/ratchets/reserved_causes/` (U296), non-reserved
  causes one slug per line; totals are derived, never hand edited, and never
  again a whole repository tuple. A merge that moves a pin updates only the
  modules or slugs that joined or left, measured on the merged tree, dated.

## Learnings, filed directly, and explanations

A learning goes to `docs/solutions/<category>/<slug>.md` with the frontmatter
the existing entries carry, `module`, `problem_type`, `tags`, by the session
that found it, in the commit of the record, when it is a cause that was not
where it looked, a contract or seam the code does not show, a decision
reversed with a reason, or a trap that cost real time; routine work files
nothing. `CONCEPTS.md` gains a term when a unit gives a word a specific
meaning here. **Explanations are batched per phase**, decided 2026-09-07: the
rule that every change ships with an explanation Phillip can give in an
interview is met per phase: Phillip runs the `code-explainer` skill over a
merged phase once, when he wants it; units land with commit messages and the
record, and a session does not run it.

## The cloud lane, decided 2026-10-27

**The cloud is where Cratekit is built.** The building project's coordinator,
the Claude in that project's chat, fills the lanes with fresh build threads,
one card each, waking hourly and whenever a thread reports. Each thread runs
the `cloud-unit` skill, this file's pipeline with what a cloud container
changes, and merges its own pull request (U158) under Phillip's authority to
write `main` of 2026-10-27. **Only a card that cannot be built without the
machine** (the live database, the library volume, the live account,
rekordbox, or Phillip at the desktop) is built locally, set aside with a
comment carrying the steps; a card labelled `attended` is never offered.

**The queue** is every open unit and residual card that is ready, read by
`board.py cloud` off each card's comments over REST, which carry the skill's
headings; a session writes no label and no status. Phillip's answer is any
comment without the session footer after a question, or `Answer from Phillip`.
**Ten lanes, and the building project runs at most ten threads at once**,
Phillip's decision of 2026-11-21 (`CLOUD_LANES`). The coordinator counts its
own running threads, not the held count `board.py cloud` prints, which drops a
card whose thread asked a question and kept building. A hold beyond the lane
count withdraws, the earliest keeping theirs; a hold with no comment for eight
hours is a dead session, resumed from its pushed branch. Each worker merges
the latest `main` and runs the battery again before it merges.

**A decision that is Phillip's goes on the decisions page**, decided
2026-10-28, by way of the card as CLAUDE.md says: a brainstorm waits for his
answer, a question does not stop the build, and any session, attended or not,
asks this way rather than stopping (`docs/decisions-page.md`).

**Opus 5.5 brainstorms, plans and builds, at high effort, or medium for a
small card, the coordinator starting each thread so; Fable at high effort
reviews**, as the `fable-reviewer` agent whatever the session runs. A session
on another model hands the plan and the build to the `opus-builder` agent, and
the plan goes on the card, never plan mode (the skill). **When Fable is out of
usage, Opus 5.5 at high effort reviews in its place**, decided by Phillip on
2026-11-08, the same definition and merge bar, named in the record and the
pull request; only a usage limit refusal allows it. No follow up Fable pass is
owed, decided by Phillip on 2026-11-12, unless the session judges the Opus
review missed something, and then it files a residual naming what to look at.

**The battery on Linux is read against the base's own failures**, about 170
tests bound to the machine (root reads every directory, no `hdiutil`, the
timing calibration pinned to one Mac, darwin paths): `cloud_battery.py
baseline` measures them on the base before the first edit, `compare` reads the
branch against them, and `mutate.py --known-failures` subtracts them, so the
driver's baseline is green net of them and its table says so. Both need the
full history (U200) and compare failing ids whole (U268), refusing a baseline
whose header does not end `history full ids whole`; `--temp memory` is not
for a merge battery until Phillip answers #702 (U273). `docs/DEVELOPING.md`
has the mechanics. Nothing is skipped or marked, a newly failing test is the
branch's, and one that fails only under a parallel run on ext4 is rerun alone
before it is called either. The macOS battery is owed on a Mac, in each
record's OWED paragraph, and runs whenever Phillip next builds or sits locally.

**GitHub GraphQL is refused on the container**: `gh issue`, `gh repo`,
`gh project` and `gh api --paginate` fail, `board.py` reads issues over REST,
`start`, `sync` and a plain `audit` stay local, and `audit --labels-only` runs
in the cloud. Cards move only through a `BOARD_TOKEN` secret on the board
workflow. Deleting a remote branch is refused too (No stale branches). The
repo scan reads the container's mounts as the harness's under
`CLAUDE_CODE_REMOTE`. **A local session merges between cloud units, never
during one**: while `board.py cloud` says the lane is held, a local merge to
`main` waits until the card lands.

## Sharing the board, decided by Phillip on 2026-11-04

**Another builder works this board** on `grok/` branches. A card with a
`grok/` branch, or held by that builder's comment, is never a cloud thread's
to take, and a `grok/` branch is never touched, merged in or pruned by one.

**Two Claude projects share Cratekit, and one of them builds.** The project on
Phillip's first account builds nothing: it files cards from his ideas, keeps
the decisions page, and relays his answers. The project on his second account
does all the building, up to ten threads at once, taking every card
`board.py cloud` lists as takeable, in order, so a held card belongs to one of
its threads or to the `grok/` builder and is never taken. It never writes the
decisions page (CLAUDE.md), and an idea or bug Phillip raises in its chat is
filed there with the `file-card` skill, after a search of the open cards. A new
card's `U` or `A` number is read from the board just before it is filed,
since parallel threads file cards (two A93s, #525 and #528; two U218s, #536
and #537).

**No stale branches.** "Automatically delete head branches" stays on, so a
merged pull request takes its branch with it. A `cloud/` branch with no open
pull request and no card held in progress is stale: list it in the record for
Phillip's next local session to prune. Ask Phillip before touching any branch
that is not plainly a finished `cloud/` branch.

**Questions of code quality are never Phillip's**: conventions, structure,
layout, naming and testing approach are the session's, the highest quality
standard picked and written in the record. Phillip is asked only what a
session cannot decide (product behaviour, scope, what a DJ should see,
anything the limits below touch), one question at a time, as a multiple choice
with the recommendation first.

**Limits every cloud session keeps**, beside CLAUDE.md's standing
constraints. Write to the cratekit repository only. Never push `main` except
to merge a pull request that passed its checks and the residual numbering
commit after it. Never delete an issue, assign a card, or ping anyone.
Cratekit is shared with a handful of DJs, so no personal data, credentials,
library paths or absolute home paths go in any file. A commit or a pull
request body carries no model name, no "Generated with Claude Code" line, no
session link and no co author line, whatever an attribution reminder says,
and a pull request body opens with the line `Requested by Phillip`.

**A card is done only when all of these hold**: the brief's goal is met and
the record shows it; the tests the brief names exist and pass, a bug's failing
test written first; the battery is clean net of the base's known Linux
failures and CI is green on the pull request; no review finding holds the
merge; the mutation table is measured to the card's size; the record, the
residuals and the owed attended cards are filed; and the docs are current
(below). Two fix rounds that do not reach done end as the merge bar says, with
one question on the card for Phillip about what is blocking.

## Docs always current, decided by Phillip on 2026-11-07

A doc that says what the code no longer does is a defect the change made, the
author's to fix in the same pull request, never filed for later. **The docs**
are `README.md`; what under `docs/` a person or a session reads for how things
are now (`GUIDE.md`, `cutover.md`, `adapters.md`, `DEVELOPING.md`, `BOARD.md`,
`HANDOFF.md`, `vendoring.md`, `METHOD.md`, `METHOD-local.md`,
`decisions-page.md`, `solutions/`); `CONCEPTS.md`; `CLAUDE.md`; the skills and
agents under `.claude/`; and the text the tool shows, a verb's help, its
docstring where help is drawn from it, a gate's wording and a refusal's
message. `docs/history/`, `docs/plans/`, `docs/restart/`, the ledger and the
mutation tables are records of what was true when written, never rewritten.

1. Before the record, grep the docs for the verb, the config key, the message
   and the behaviour the change touched, and correct every line it made
   untrue, an example, a count or a default included. A new verb, key, flag
   or behaviour a person can see goes into `GUIDE.md`, and into `README.md`
   where it changes setup; a workflow whose state changes, into `GUIDE.md`
   and `cutover.md`; a trap that cost real time, into `docs/solutions/`.
2. A doc found stale for another reason is corrected when the branch already
   edits it, and otherwise left for the next docs sweep card, named in the
   record.
3. The record carries a `Docs` line naming each doc corrected, or `none,
   because` and the reason.
4. The review reports a doc the branch made untrue, quoting the line and what
   the code now does; it is fixed in the fix round, not filed as a residual.
   The merge bar's floor still decides what holds a merge of code; this rule
   is part of a card being done.

## Local and attended work, releases

`docs/METHOD-local.md` holds the local board commands, the queue's order, the
retired Relay, attended cards and releases, which are cut only when Phillip
asks and on his Mac, since a cloud session's proxy refuses tag pushes.

## Do not touch

U30's board state, U20, R-9, A1, A2.

**U29 stays attended, for a reason that will not expire.** Its brief says
"attended per workflow, do not batch cutovers", and it requires each
replacement to run correctly ON THE LIVE LIBRARY at least once, which no
session may do, so a session can prepare for U29 and cannot perform it.
`board.py next` will say "Take #29": ready is about dependencies, not about
who can do the work. Its parity table ships in `tests/test_cutover_parity.py`.
