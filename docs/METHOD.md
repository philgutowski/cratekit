# Method

This file is the operating instruction. It is deliberately fixed in size and it
is the only document a session reads to learn how to work here. `CLAUDE.md` is
the session contract and points at this file. `RESTART-cratekit.md` is verified
state and nothing else.

**The compound engineering plugin is out of the loop, decided 2026-09-07.** No
`ce-plan`, no `ce-work`, no `ce-code-review`, no `ce-compound`. Each of those
spent a multi agent pass on work a single session can do against the issue
brief, and the largest of them, the independent verifier, was measured at 258k
tokens for one round trip. The rules they enforced that were actually paid for
are kept below as rules. The ceremony is not. Native Relay, which runs this
file's pipeline and none of those skills, is in the loop. See Relay below.

`docs/history/` is HISTORY. It holds the wave state files, the independent
reviews and the long narrative handoff. Read one when you need the reasoning
behind a rule. Do not read one to find out how to work. That is this file.

## The pipeline, one unit per session

A session takes one unit from the board and runs it to a pushed merge. Nobody is
watching, so a question is a stop, and a stop with nothing recorded is the one
ending the next session cannot diagnose. When a decision is genuinely the
person's, record it as a residual with the options and pick the conservative
one.

1. **Orient.** `board.py next`, `board.py show N`, `board.py start N`. The issue
   is the brief. Read this file, `RESTART-cratekit.md`, and `CONCEPTS.md` for
   any term that is unclear. Grep `docs/solutions/` by module and tag for the
   area you are about to touch, and read the entries that match.
2. **Plan, in plan mode, as a message.** The plan names the seam, the files,
   the test scenarios from the brief, the residuals the unit closes, and what is
   out of scope. It is not a document. `docs/plans/` is closed: nothing new is
   written there and the existing files are the record of units already built.
   If the brief is insufficient, fix the issue body, then plan against the fixed
   brief.
3. **Build.** Guard first, then the code it governs, so a violation is
   impossible to introduce silently rather than confirmed after the fact. Commit
   in units of meaning with subjects that name the unit, `feat(u57): ...`.
4. **Review.** Run the built in `/code-review` on the branch, drive every
   finding it raises rather than arguing with it, apply what holds, and commit
   the fixes. Then the mutation table below, capped at 25 rows. Then the hunts a
   green suite cannot see. At most two fix rounds; when they are spent, what is
   still open becomes a residual and the unit merges.
5. **Record.** Each residual is a file, `docs/residuals/<unit>-<slug>.md`,
   with no number; `docs/residuals/README.md` is the form. **A residual that
   meets the board bar below says `issue: yes`**, because the board is the
   queue and a finding nobody queued is a finding nobody does, and the issue
   is filed once the number exists. A `docs/solutions/` entry only if the unit
   found something a future session would get wrong without it, written
   directly in the existing frontmatter form. The unit's restart paragraph is
   its own file, `docs/restart/<unit>.md` (`u114.md`, `r572.md`), never a
   paragraph in `RESTART-cratekit.md`, which `scan_repo.py` refuses. No
   explainer, see below.
6. **Merge.** The battery from inside the checkout, the closing keyword scan
   over the whole range, merge to `main` locally, then on `main`
   `board.py residuals --land` and commit what it numbered, push `main`,
   delete the branch in both places, `board.py audit`. File the issue for
   each residual `--land` names as meeting the board bar.

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

**Everything else is a RESIDUAL.** A docstring that overclaims, an assertion
that names the wrong number, a guard that kills zero tests, a document whose
count an independent table does not reproduce: all real, all worth recording,
none of them a reason to hold a merge. File them with their measured cost.

This floor exists because "the reviewer found nothing" is not a reachable state.
A mutation table over a suite this size always finds a zero death row, because
that is a property of large test suites rather than of any branch.

**And a hard cap: each unit has at most two fix rounds.** The floor is meant to
end the loop on merit. The cap is what guarantees an end date if it does not.

## The board bar, decided 2026-09-18

Most residuals stay in the ledger and earn no issue. A residual earns one, the
moment it is filed, only when it is open and a person using the shipped verbs
pays for it in one of four ways: **(a)** files or database rows can be lost or
damaged, **(b)** the product says something false, a clean report over state it
could not read or a declared write it never performs, **(c)** a workflow a DJ
needs cannot finish, **(d)** a guard on a path that writes or deletes is absent
or kills nothing. A maintainer facing finding, a wording fix, a count in a
document, or anything that closes only at an attended sitting does not.

File it with `gh issue create --repo philgutowski/cratekit --label residual`,
titled `R-N: ` followed by the ledger heading EXACTLY, since `board.py audit`
compares the two, with a body opening `**Depends on:** none` and carrying goal,
key files, approach, test scenarios and out of scope. Add it to project 2.
Create the issue AFTER `board.py residuals --land` numbers it on `main`,
because a number is not the finding's until then. The unit marks it
`issue: yes` in its residual file so whoever lands it knows to. The Relay feeder picks up
any open issue labelled `residual` or `unit` that the board derives as ready.

**Never write a literal dot claude path in a card**, title, body or comment, not
even to forbid one. Relay reads every card it is about to launch and SKIPS any
whose text names that directory, silently, because an edit there needs an
attended session. One Phase G brief cited the source system's skill file by its
path and would have sat unlaunched. Describe the location in words instead.

## Verification is the author's, and says so

**No independent verifier, decided 2026-09-07.** The author runs the mutation
table and the review. That is a known gap with a measured size: independent
tables found 17 where the author found 10, 49 against 39, 83 against 49. Every
zero row therefore reads as "the author could not kill it", and the record
says exactly that in one line rather than pretending otherwise. Phillip can ask
for a full pass on a unit that writes or deletes, and it is his to ask for.

Verification depth is still proportional to blast radius. A unit that writes or
deletes gets its full 25 rows and a composite on every user facing zero. A read
only report or a static registry gets a table scoped to its new guards and a
line per zero.

## The mutation table

Revert each new guard one at a time, run the suite, count the deaths. A guard
that kills zero tests is a finding.

**Scope it to the round's own diff**, plus a fixed sample of the unit's
existing guards. **Hard cap: 25 rows, one pass per unit per session.** When you
hit the cap, stop and log what you dropped and why you ranked it below the cap,
so a truncation is visible rather than read as coverage.

**Use `scripts/mutate.py`. Do not hand roll a driver.** It takes rows as data
and returns the table, and it holds every driver rule below as a property. Three
of this project's recorded incidents were hand rolled driver mistakes. Do not
edit `tests/` while it runs: it snapshots and restores the src file it mutates
and nothing protects the suite.

**Confirm deaths on a subset, spend a full suite only on zero rows.** Select
the subset as the test files importing the mutated module. A death on a subset
is a real death. A zero on a subset is not yet a zero, so promote it to a full
run before you report it.

**A zero death row on a guard with a USER FACING surface is acceptable only
when a composite shows what it does hold.** Pair it with a mutation of the thing
it guards and report both counts. A prose argument is not evidence.

**A zero row on a maintainer facing guard gets one line, not a composite.**

**Write the table into the repository** under `docs/mutation/`, with full row
descriptions and not only counts. A table that lives only in a chat message is a
claim. One was lost that way.

## Reading discipline, because context is what you are billed for

Every tool result stays in context and is re-sent on every later call, so the
bill is tool calls times context size. Thinking is cheap here. Reading is not.

- **Never read a file over 400 lines whole.** Grep for the symbol, then read the
  region around it. `docs/residual-findings.md` is twelve thousand lines: grep
  for `^## R-NNN` and read that entry.
- **Delegate a sweep, keep the conclusion.** A search across many files goes to
  a read only subagent that returns the answer, not the file dumps.
- **Every report opens with a verdict header under 60 lines**: the verdict, a
  numbered finding table with each finding's classification, and the battery
  numbers.
- **Do not re-read a prior round's full mutation table.** Read its summary rows.

## Driver rules, every one of them paid for

- **Never pass `-q`,** including to a collection run. `pyproject.toml` already
  sets it, so yours becomes `-qq` and suppresses the summary line and the
  collect listing. Use `pytest --tb=no` for counts and
  `pytest --collect-only -o addopts=` for the collected count.
- **Check the collected count on every row.** A file that fails to COLLECT
  takes its tests with it and the run still looks green.
- **One driver at a time, waited on, with nothing else touching the tree.** The
  rule used to say "run rows synchronously in the foreground", because a
  backgrounded driver outlived its parent twice and contaminated later rows. That
  is still the failure to defeat and the foreground is no longer how. Corrected by
  U65, 2026-09-17: `mutate.py`'s fixed overhead on this suite is over 600 seconds,
  which is the harness tool ceiling, so a foreground run is KILLED mid row. (That
  600 was measured on the serial suite. The driver inherits `-n auto` since
  2026-09-18, so its baseline is now about a minute, and a 25 row table can
  still pass the ceiling, so the rule stands.) Three
  were, and two left a partial mutation in the source that had to be restored from
  `git show HEAD:`. Foreground is now the contaminating option. Run it as a
  tracked background job, start nothing else against the tree until it reports,
  and check `git status` plus every row's `head_verified` when it does.
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
   is correct in isolation and the hole stays open.
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
- The first caller of an engine owns the engine's unreviewed failure paths.
  `git grep -n <engine> -- src` before binding a worker, and if the definition
  is the only hit, read the engine's error paths as your own.

## The battery

Nothing merges until all three are clean, run from inside the checkout that
holds the branch, with that checkout's own venv:

    ./.venv/bin/ruff check src tests scripts
    ./.venv/bin/python -m pytest --tb=no
    ./.venv/bin/python scripts/scan_repo.py

**The suite is parallel and takes about a minute, measured 2026-09-18.**
`addopts` carries `-n auto`, so the command above already uses every core:
7,678 tests, 532 seconds serial, 61 to 67 parallel on 11 cores. A venv made
before that date needs `pip install -e '.[dev]'` once for `pytest-xdist`. Pass
`-n 0` for a debugger or a profiler.

**The full battery is the MERGE gate, not the edit loop.** While building, run
the test files for the modules you touched, `pytest tests/test_x.py`, which is
seconds. Run the full suite before the review, after each fix round and at the
merge, not after every edit. A session that ran the old nine minute suite a
dozen times spent two hours proving what four runs prove.

**A new slow test is a finding.** `pytest --durations=10` at the merge. A test
over ten seconds is either real work, a process pool or a disk image, or a
real sleep nobody faked. The second kind hid a product defect once: a
`credential-missing` refusal retried and slept on for 31 seconds per listing.

**Run the battery on a COMMITTED tree.** `tests/modules/test_reports.py` reads
every uncommitted and untracked file as one of U34's own and bans that unit's
residual numbers inside it, so a suite run over uncommitted edits to a document
somebody else wrote fails on citations you did not write. Measured 2026-09-07:
one failure on the moved history files, none after the commit.

**Do not symlink `.venv` into a worktree.** The editable install names the
checkout it was installed from, so a worktree with a borrowed venv verifies code
it cannot see. A worktree gets its own venv, `python3.12 -m venv .venv` then
`pip install -e '.[dev]'`, and its own scratch directory named for its unit.

## What CI is for, decided 2026-08-15

**The battery above is the merge gate. CI is not, and it does not run the
suite.** It proves PACKAGING and PORTABILITY, the two things the battery cannot
see from a laptop that already has everything: the package installs from a
clean checkout on 3.12 and 3.13, the slim profile pulls in no DSP and no ML
stack, the vendored downloader shipped, ruff is clean, and no personal path or
credential reached the tree.

**A step in `.github/workflows/ci.yml` must be able to pass. A check that cannot
belongs in the battery.** R-115 bought that rule: every run on `main` failed for
ten commits while the battery was clean, so red carried no information.
**Nothing is deselected, and that is deliberate.** Five of those failures were
a shallow checkout, not Linux. Before blaming the platform for a red run, drive
it.

## Committing and merging

- **No pull requests.** Feature branch per unit, merge to `main` locally, push
  `main`, delete the branch in both places: `git branch -d <branch>` then
  `git push origin --delete <branch>`.
- **`git push origin --all` fails on this connection** with `RPC failed; HTTP
  400`. Push one branch at a time.
- **No em dashes, no en dashes, no double hyphens** in prose, comments, commit
  messages or issue bodies. Favor commas over colons.
- **Check `tests/_pending.py` before writing a closing trailer.** If the
  register still owes the unit a module, the trailer would close an issue the
  repository says is unfinished, which is the exit 2 the audit reports. Merge
  without the trailer and close the issue when the register is discharged.
- **GitHub matches a closing keyword anywhere in a body, and scans every commit
  in the pushed range.** Scan the RANGE before every push, not only a merge:

      git log origin/main..main --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

  **NEVER WRITE A CLOSING KEYWORD ADJACENT TO AN ISSUE NUMBER, even to quote
  one, even inside backticks, even to say it is unsafe.** GitHub reads the text
  and not the intent. A commit written to document this failure quoted the
  offending strings and closed the issue a second time. Put words between the
  keyword and the number, or name the unit instead of its number. A branch
  already carrying such a string cannot be made safe by the merge commit:
  rewrite those bodies, or expect the close and reopen the issue after the push.
- **Residual numbers are APPEND ONLY. A number, once given, is that finding's
  for life.** A number is given at landing and nowhere else, decided by U124:
  a unit files its residuals unnumbered in `docs/residuals/`, and
  `board.py residuals --land`, which refuses off `main`, gives each the next
  number past the ledger's highest. So the numbers on `main` never move and no
  branch is ever renumbered. Gaps are fine. GitHub issue titles carry residual
  numbers in their text, which is a surface the repository cannot see, and is
  why a renumber is forbidden. A branch built before U124 that still numbers
  its own entries takes fresh numbers above `main`'s highest at the merge.
  Verify a merge with both:

      grep "^## R-" docs/residual-findings.md | sort | uniq -d              # must be empty
      git diff origin/main -- docs/residual-findings.md | grep '^-## R-'   # must be empty

- **Use git's merge algorithm only.** `diff3 -m` silently produces a broken
  merge of `tests/_pending.py`.
- **A countdown entry is discharged in THREE edits in one commit, and one alone
  is worse than none.** Delete the `PENDING` entry, delete the matching
  `EXPECTED_PENDING` key, and remove the `@requires("<key>")` decorator from
  EVERY guard it gated, after `grep -rn 'requires("<key>")' tests/`. Deleting
  only the entry raises `KeyError` at import and takes the guard's whole FILE
  out of collection: 330 tests once stopped existing while the run reported
  green. Then run the newly armed guard on purpose, because it has never
  executed once.
- **Reconcile the collected count by identifier, not by total.** A total only
  check shows a healthy rise and hides a collapse.
- **A unit's restart paragraph is its own file, decided by U124.** It goes in
  `docs/restart/<unit>.md`, so two units land in either order without a
  conflict. `RESTART-cratekit.md` keeps only the sections no unit owns, and
  `scan_repo.py` refuses a unit's paragraph anywhere in it. A branch built
  before U124 that conflicts there moves its own paragraph into its fragment
  and takes `main`'s `RESTART-cratekit.md` as it is.

- **Reserved-cause pins are per module, decided by U125.** The populations in
  `tests/test_reserved_causes.py` are pinned in
  `tests/_pinned_reserved_populations.py`: kebab literals and holders by module,
  non-reserved causes one slug per line. Totals are derived from those pins,
  never hand-edited. When a merge moves a pin, update only the modules (or
  slugs) that joined or left, measured on the merged tree, and put a dated
  comment on those entries. Do not reintroduce a whole-repository total tuple;
  that was the shared edit point U125 removed.

## Learnings, filed directly

A learning goes to `docs/solutions/<category>/<slug>.md` with the frontmatter the
existing entries carry, `module`, `problem_type`, `tags`, written by the session
that found it, in the same commit as the record. The bar is the one
`ce-compound` used: a cause that was not where it looked, a contract or seam
whose rules are not visible in the code, a decision reversed with a reason, or a
trap that cost real time. Routine work files nothing. `CONCEPTS.md` gains a term
when a unit introduces a word that carries a specific meaning here.

## Explanations, batched per phase, decided 2026-09-07

The standing rule that every change ships with an explanation Phillip can give
in an interview is met per phase, not per unit. Units land with commit messages
and the record. When a phase merges, Phillip runs the `code-explainer` skill
over the merged range once. A session does not run it.

## The order

`board.py next` orders the queue. The list serialized here on 2026-09-07 is
spent, every line of it landed or was closed back to the ledger by 2026-09-18,
and its text is in git history. On 2026-09-18 a parity audit against DJ_tools
found the product could not finish an acquisition workflow, and the board
gained Phase G, units U67 onward, plus the residuals that meet the board bar.
`docs/ideation/2026-09-18-parity-to-feature-complete.md` is the design those
units were cut from, read for reasoning, never for instruction. The issue is
the brief.

**#29, U29, stays attended and is never a session's to take.** See below.

## Relay, retired 2026-10-27

Native Relay, the feeder, the watcher, the fable builder and `/board-up` ran
this file's pipeline on Phillip's machine from 2026-09-07 to 2026-10-27. They
are abandoned, decided by Phillip on 2026-10-27, and the cloud lane below
replaces them. Their manifests and run state live outside this repository and
are not read. What they taught stays in `docs/solutions/` and in the driver
rules above, and `docs/history/` has how they ran.

## The cloud lane, decided 2026-10-27

**The cloud is where Cratekit is built.** A dispatcher, one long lived cloud
session with the repository attached, fills the cloud's lanes with fresh
worker sessions on Opus 5.5, one card each, following the `cloud-dispatch`
skill. A scheduled task wakes it every hour, and a worker wakes it the moment
it takes or frees a lane. A scheduled task made from the web dialog came out
as a chat task with no repository twice on 2026-10-27, which is why the
dispatcher exists: a session it creates carries the repository. Each worker
runs the `cloud-unit` skill, in the repository's Claude Code skills
directory, which is this file's pipeline with what a cloud container changes:
it takes its card, brainstorms it if it is an idea,
plans, builds, reviews, measures the mutation table, writes the record,
merges to `main` with the closing trailer and pushes `main`. Phillip
authorized the cloud to write `main` on 2026-10-27. **Only a card that
cannot be built without the machine is built locally**: the live database,
the library volume, the live account, rekordbox, or Phillip at the desktop.
The session sets it aside with a comment carrying the local steps, and a card
labelled `attended` is never offered at all.

**The queue is every open unit and residual card that is ready**, read by
`board.py cloud` from each card's comments over REST. The session writes no
label and no status. Its hold is its own comment headed `Started`, and its
plan, progress notes, brainstorm, set-aside and landing are comments headed
`Plan`, `Progress`, `Brainstorm`, `Needs the machine` and `Landed`; Phillip's
answer is any comment without the session footer after the question. **The
cloud builds three cards at once**, decided 2026-10-28 for the backlog
(`CLOUD_LANES` in `scripts/board.py`): each worker merges the latest `main`
into its branch and runs the battery again before it merges, so two builders
landing in either order is the case the repository was already built for
(restart fragments, residuals numbered at landing, per module pins). A hold
beyond the lane count withdraws, the earliest holds keeping theirs. A hold
with no comment for eight hours is a session that died, and the next one
resumes it from its pushed branch.

**A decision that is Phillip's goes on the decisions page**, https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS,
decided 2026-10-28. A worker that reaches one, a brainstorm's questions or a
question a brief leaves open, writes each question there as a multiple choice
with its recommendation first, says so on the card, and moves to the next
card. Phillip answers on the page whenever he likes; the dispatcher, at its
next `Dispatch`, posts each answer on its card under `Answer from Phillip`
(which `board.py cloud` reads as his reply and offers the card as
`answered`) or sends it to the session that asked, and marks it relayed.
Any session, attended or not, asks him this way rather than stopping.

**Opus 5.5 at high effort brainstorms, plans and builds; Fable at high
effort reviews.** The project settings fix the effort, the scheduled task
fixes the session's model, and the review is the `fable-reviewer` agent
whatever the session runs. A session on another model hands the plan and the
build to the `opus-builder` agent. The plan is posted on the card rather than
proposed in plan mode, because plan mode waits for an approval nobody is
there to give. The merge bar and the two round cap are unchanged.

**The battery on Linux is read against the base's own failures.** About 170
tests fail on the container for reasons bound to the machine (root reads
every directory, no `hdiutil`, the timing calibration pinned to one Mac,
darwin paths). `scripts/cloud_battery.py baseline` measures them on the base
commit before the first edit, `compare` reads the branch against them, and
`scripts/mutate.py --known-failures` subtracts them from every mutation run,
so the driver's baseline is green net of them and its table says so. Nothing
is skipped or marked, a newly failing test is the branch's, and a test that
fails only under a parallel run on ext4 is rerun alone before it is called
either. The macOS battery is owed on a Mac and named in each record's OWED
paragraph; it runs whenever Phillip next builds or sits locally.

**GitHub GraphQL is refused on the container**, so `gh issue`, `gh repo`,
`gh project` and `gh api --paginate` all fail there, and `board.py` reads the
issues over REST a numbered page at a time when the GraphQL count is refused.
`start`, `sync` and a plain `audit` stay local; `audit --labels-only` runs
in the cloud. The project's cards move only with a `BOARD_TOKEN` secret on
the board workflow, since no cloud session can write the project. Deleting a
remote branch is refused too, so merged `cloud/` branches stay until someone
prunes them locally. The repo scan reads the container's mounts as the
harness's under `CLAUDE_CODE_REMOTE`.

**A local session merges between cloud units, never during one.** When
`board.py cloud` says the lane is held, a local merge to `main` waits until
the card lands, or the cloud session meets a moved `main` at its merge and
has to merge it in and run the battery again.

## Do not touch

U30's board state, U20, R-9, A1, A2.

**The conformance branch is UNPARKED as of 2026-09-07.** It is a unit on the
board and lands the way any unit does. Until it lands, its `write/metadata.py`
soft delete defect is still live on main, and the branch is 377 commits behind.

**U29 stays attended, for a reason that will not expire.** Its brief says
"attended per workflow, do not batch cutovers", and it requires each
replacement to run correctly ON THE LIVE LIBRARY at least once. The live
rekordbox database is off limits by standing constraint, so a session can
prepare for U29 and cannot perform it. `board.py next` will say "Take #29".
Ready is a statement about dependencies, not about who can do the work. The
parity table its test scenario asks for already ships in
`tests/test_cutover_parity.py`.
