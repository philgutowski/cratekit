---
name: cloud-unit
description: The pipeline for a Claude Code cloud session on the Cratekit board, from the cloud queue to a unit merged and pushed on main. Use when a cloud session is asked to take the next card, build a card, or run the cloud lane.
---

# Cloud unit

A cloud session takes one card from the queue and runs METHOD's whole
pipeline on it, to a pull request it merges to `main` with the closing trailer
once CI on its head is green, or sets the card aside with the steps to build
it locally. Read `CLAUDE.md` and `docs/METHOD.md` first: METHOD holds the
rules, its cloud lane section this lane's; this skill is the steps.

## Where you are

A cloud container with a fresh clone, no rekordbox, no library volume, no live
account, nobody watching. Run every tool through `.venv/bin/`, which the
session hook built with the dev extras; if it could not, build it with `uv
venv --python 3.12 .venv` and `uv pip install --python .venv/bin/python -e
'.[dev]'`. GraphQL is refused (METHOD's cloud lane), so use `gh api` on
`repos/<owner>/<repo>/...` or the GitHub MCP tools. `scripts/board.py cloud`
is the queue, `show N` the brief, `closing --since origin/main` the closing
check, `residuals --land` the numbering, `audit --labels-only` the audit.
About 170 tests fail here for the machine's reasons, read off the base by
`scripts/cloud_battery.py` and `scripts/mutate.py --known-failures`. Never
edit the calibration file, never skip, deselect or mark a test.

## Models

METHOD's cloud lane names who plans, builds and reviews. The coordinator
starts this thread on Opus 5.5 at its card's size's effort, so it plans and
builds itself, saying in the plan if the card is another size; a session not
on Opus 5.5 hands step 4 to `opus-builder`. A Fable stand in, or a review
where the harness cannot load agents by name, is a general purpose agent at
high effort on the `opus` (or `fable`) model told to read the `fable-reviewer`
definition first and follow it; a stand in is named `Review: Opus 5.5 at high
effort, Fable out of usage` in the Progress comment, the record and the pull
request body. Any other refusal or failure of the review is retried, never
substituted.

## Writes you never make

Every write CLAUDE.md and METHOD forbid; and anything under a real config path
or a real library, anything in `.github/` unless the card is about it, a ready
or blocked label or a project status, and a trailer, co author line or session
line on a branch commit, since the merge commit carries the one trailer.

## Comments are the protocol

`board.py cloud` reads each card's comments and nothing else, so every comment
you post starts with one of these headings, exactly, and the harness footer
marks it as yours:

| heading | means |
|---|---|
| `Started` | this session holds the card, and one of the lanes, until it lands |
| `Resumed` | this session took over a hold whose session died |
| `Plan` | the plan, under the hold |
| `Progress` | a note under the hold, which also refreshes it |
| `Brainstorm` | the card is an idea; the questions wait on Phillip |
| `Question for Phillip` | one decision the brief leaves open that cannot be made conservatively |
| `Answer from Phillip` | his answer from the decisions page, posted by the relay thread; read as his reply |
| `Needs the machine` | set aside, with the steps to build it locally |
| `Withdrawn` | this session lost a race for the lane and released the card |
| `Landed` | merged and pushed on `main` |

The reader forgives markdown, emphasis and punctuation around a heading, so
`**Brainstorm.** One question waits` reads as `Brainstorm` (U203), but never a
different word: a bare `Question`, or `Brainstorm notes`, is a heading it does
not know, and a card under one is read as held, then as a session that died.
Post with `gh api -X POST repos/<owner>/<repo>/issues/N/comments -F
body=@file.md`. Phillip's comments, and `Answer from Phillip`, are read only
as answers to a `Brainstorm` or a `Question for Phillip`. A session that finds
its card labelled `attended` or closed stops. A hold silent for eight hours is
offered as `resume`, so post a `Progress` note at each phase: built, each
review round, mutation measured.

**Tell the coordinator** that started this thread (METHOD's cloud lane), with
the project's tool for messaging it, right after this session's last comment
(`Landed`, `Brainstorm`, `Needs the machine` or `Withdrawn`), so the lane it
frees fills. A session outside a project has no coordinator.

## Asking Phillip

On the card only, under `Brainstorm` or `Question for Phillip` (CLAUDE.md):
each question with two to four multiple choice options, the recommendation
first, and enough context, two or three sentences and the cost of each way,
to be answered without the rest of the card. A question never stops the
build: make the conservative call, record it, and keep going.
`docs/decisions-page.md` is how it reaches the page and his answer the card.

## 1. Orient

    git fetch origin main
    .venv/bin/python scripts/board.py cloud

It lists the open cards by state, the lanes held, and the next card. **If your
prompt names a card, take that one**, as long as the queue lists it as
takeable; otherwise take the one the queue names. Pass over a card held by the
`grok/` builder (METHOD's Sharing the board): `board.py cloud` cannot see that
hold, so before posting `Started` look for a `grok/` branch naming the card's
number (`git ls-remote --heads origin 'grok/*'`) and a comment of that
builder's on the card. If every lane is held, or nothing is takeable, say so
in one line, tell the coordinator, and stop.

**Post `Started` on the card at once**, before reading anything else, then run
`board.py cloud` again. If it now says more cards are held than there are
lanes, it names the ones that held first; if yours is not among them, post
`Withdrawn` and stop. A `Brainstorm` or `Needs the machine` posted later
replaces the hold. Take the card in its state:

- `answered`: Phillip replied. If a `Progress` comment or a pushed
  `cloud/N-...` commit is newer than the question and under eight hours old,
  the card is still that thread's: pass over it. Otherwise fold his answer
  into the brief (step 2) and go to step 3.
- `resume`: a session holding it died. Post `Resumed`, check out
  `origin/cloud/N-...` if it exists and read its log against the comments to
  see how far it got; otherwise start fresh from step 3.
- `ready`: go to step 2.

Read the brief with `board.py show N` and every comment on the card:

    gh api repos/<owner>/<repo>/issues/N/comments --jq '.[] | "--- \(.created_at)\n\(.body)"'

## 2. Classify the card

Say in the plan which of three it is.

**It needs the machine** when it cannot be built and proven without what only
Phillip's Mac has (METHOD's cloud lane), or a backup of the real library.
Built, not merely verified live afterwards: a unit whose code and tests run on
fixtures and disposable copies is the cloud's, its live proof an OWED line in
its record. Post `Needs the machine` with why and the exact local steps as
commands Phillip can paste (`board.py start N`, the verbs, the attended
sitting), then run `board.py cloud` again and take the next card. A session
sets aside as many cards as it must and builds at most one.

**It needs a brainstorm** when the brief has no goal, no test scenarios or no
verification, reads as an idea, or carries the `idea` label. Post
`Brainstorm`: the idea in two or three sentences, what already does part of
the job, two or three approaches with the cost and main risk of each, your
recommendation, and at most four questions as Asking Phillip says, each
answerable in a word. Then take the next card. When it comes back `answered`,
rewrite the brief with his answers folded in (`gh api -X PATCH
repos/<owner>/<repo>/issues/N -F body=@brief.md`), keeping the `**Depends
on:**` line first and every field of the brief form.

**Otherwise it is buildable.** Go on.

## 3. Start

    git checkout -b cloud/N-<slug> origin/main      # the name board.py cloud printed
    .venv/bin/python scripts/cloud_battery.py baseline   # about twelve minutes

Run the baseline as a tracked background job with a two hour timeout from the
start (a background job in a cloud thread is stopped at 30 minutes otherwise),
before the first edit, and edit nothing under `src` or `tests` until it
reports. It writes `.cloud-battery/baseline.txt`. Leave it on disk, its
default (METHOD's cloud lane says why). Post `Progress`: the branch, the base
commit, the session URL if you know it.

## 4. Plan and build

METHOD's steps 2 and 3. Grep `docs/solutions/` by module and tag and read the
matches, then post the plan as `Plan`, never in plan mode, which waits for an
approval nobody is here to give: the seam, the files, the test scenarios from
the brief, the residuals the unit closes, what is out of scope, which of the
three the card is, and its size (METHOD's card sizes), which sets its effort,
review rounds and mutation table. Fix an insufficient brief in the issue body
first; a session not on Opus 5.5 gives `opus-builder` the card and the branch.

Guard first; commit in units of meaning named for the unit, `feat(u57): ...`,
subject and body only, running the test files for what you touched as you go.
Register what a later unit owes in `tests/_pending.py`, never in a docstring.
Push at each commit of meaning (`git push -u origin cloud/N-<slug>`), so a
session that dies leaves its work where the next one resumes it. Post
`Progress` when it is built.

## 5. Review, to the merge bar

Run the `fable-reviewer` agent on the branch, telling it the card's size, and
drive its findings rather than arguing with them. Commit the fixes as
`fix(uN): ...`, push, and note the head round one reviewed. Whether there is a
round two, and what it reads, is METHOD's merge bar and card sizes; tell the
agent round one's head. At most two fix rounds; what is still open becomes a
residual file. Post `Progress` after each round, naming what it drove. Then
the hunts a green suite cannot see (METHOD).

## 6. The mutation table

Sized by METHOD's mutation table, none for docs or skill text alone. Rows
target the code the unit added, in `docs/mutation/uN-rows.toml` in the form of
`docs/mutation/u99-b-rows.toml`. Commit the rows, run step 7's `compare` on
that head, then, editing and committing nothing between the two, measure them
as a tracked background job with a two hour timeout, starting nothing else
against the tree until it reports:

    .venv/bin/python scripts/cloud_battery.py compare
    .venv/bin/python scripts/mutate.py docs/mutation/uN-rows.toml --known-failures .cloud-battery/baseline.txt

Pass `--known-failures` only a baseline `cloud_battery.py` measured. If the
driver refuses a red baseline, rerun the test it names alone: failing alone
it is yours to fix; passing alone it is intermittent, so run the driver again,
and a test that reddens the baseline a second time is yours. **Never write an
id into the baseline file by hand**: it is measured, and a hand added id is a
regression excused for every later run. Commit the table,
`docs/mutation/uN.md` and `.json`, and post `Progress`.

**A card that restructures code** also replays the recorded kills of the files
it owns, before its first edit and after its last, each run as a table is
(`compare` on the committed head, then the driver), and `check` must exit 0:

    .venv/bin/python scripts/killset.py rows <paths> --out docs/mutation/uN-replay-before-rows.toml
    .venv/bin/python scripts/mutate.py docs/mutation/uN-replay-before-rows.toml --known-failures .cloud-battery/baseline.txt
    .venv/bin/python scripts/killset.py rows --after docs/mutation/uN-replay-before.json --out docs/mutation/uN-replay-after-rows.toml
    .venv/bin/python scripts/mutate.py docs/mutation/uN-replay-after-rows.toml --known-failures .cloud-battery/baseline.txt
    .venv/bin/python scripts/killset.py check docs/mutation/uN-replay-before.json docs/mutation/uN-replay-after.json

A row `rows --after` lists as unplaced is anchored by hand (the same
`source`, the new text and a `moved` reason) or mapped under `[[mapped]]` to
the row that now covers it. A replay cut at its timeout is run again with
`--resume` on the same commit. It also compares what the verbs print and
write, base against branch, in a scratch directory, first adding a scenario
under `tests/behaviour/` for any verb it touches that has none:

    .venv/bin/python scripts/behaviour_compare.py capture --out <scratch>/base --rev origin/main
    .venv/bin/python scripts/behaviour_compare.py capture --out <scratch>/branch
    .venv/bin/python scripts/behaviour_compare.py compare <scratch>/base <scratch>/branch

The record carries both results, and every difference `compare` printed is
removed or named there as a listed cleanup.

## 7. The battery

    .venv/bin/python scripts/cloud_battery.py compare

Run it on the head the rows were committed on, before the driver; a card with
no table runs it after the review. CI does not run the suite, so if anything
under `src`, `tests` or `scripts` changed since, run it again on the final
head. Ruff and the scan must be clean. Every test under `NEWLY FAILING, yours`
is yours: rerun it alone first, since one test is known to be intermittent on
ext4 under a parallel run, and fix every one that fails alone. A test under
`no longer failing` is worth a line in the record.

## 8. Record

**Docs first** (METHOD's Docs always current): correct every line the change
made untrue, committed as `docs(uN): ...`; the record carries the `Docs` line.
Then METHOD's step 5: `docs/restart/uN.md` in the form of a recent file there,
with an OWED paragraph naming what this container could not run (the macOS
battery, which METHOD-local's standing battery settles with no card, and the
live verification at an attended sitting if the unit has one); each
residual as `docs/residuals/uN-<slug>.md`, unnumbered, never
written into the ledger; a `docs/solutions/` entry only if METHOD's bar is
met. Commit as `record(uN): ...` and push.

## 9. Merge and land, through a pull request

METHOD's step 6 and its Committing and merging, done here (U158):

    git fetch origin main
    git merge origin/main          # only if main moved; then step 7 again in full
    .venv/bin/python scripts/board.py closing --since origin/main
    git log origin/main..HEAD --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'
    git push -u origin cloud/N-<slug>

The closing check must exit 0 and the keyword scan print nothing. Check
`tests/_pending.py` first: a register that still owes this unit a module makes
CI red on the pull request whatever the trailer says, so discharge the entry
or point it at the later unit that owes it. **Open the pull request** over
REST, since `gh pr` needs GraphQL (the GitHub MCP `create_pull_request` tool
works as well):

    gh api -X POST repos/<owner>/<repo>/pulls -f title='UN: <what landed>' \
      -f head=cloud/N-<slug> -f base=main -F body=@pr.md --jq .number

The body is short, since the record holds the detail (U196): a first line
`Requested by Phillip`, a line naming the card by its issue URL (never a
keyword and a number), a link to `docs/restart/uN.md` on the branch, and five
lines at most: the `compare` counts, the review rounds, the mutation table's
result, the residual files, and what is OWED. No closing keyword anywhere in
it.

**Wait for CI on the head** with one tracked background job with a two hour
timeout, since the script waits up to an hour, never a foreground sleep or a
poll repeated by hand (U196):

    SHA=$(git rev-parse HEAD)
    .venv/bin/python scripts/wait_ci.py $SHA      # exit 0 green, 1 red, 2 timed out, 3 unread

Exit 3 means the runs could not be read three times in a row: fix the read
(the token, the repository), never the branch. Green means every check run on
the head `completed` with `success`, `neutral` or `skipped`, and a completed
`success` run for the **pull request** event, since the branch's push run
lands on the same head (`commits/$SHA/check-runs` lists the first):

    gh api "repos/<owner>/<repo>/actions/runs?event=pull_request&head_sha=$SHA" \
      --jq '.workflow_runs[] | "\(.name) \(.status) \(.conclusion)"'

A pull request that conflicts with `main` gets no `pull_request` run, so when
the head shows a push run only, and whenever `main` moved while you waited,
merge `origin/main` in, run step 7 again in full, push, and wait on the new
head. **If CI is red**, fix it on the branch inside the two fix rounds; a
failure that is the machine's and not the branch's is said in the body.

**Merge it** as a merge commit, `sha` pinned to the head CI judged, the
trailer the message's last line and its only closing keyword:

    printf '%s\n\nCloses #N\n' '<what the merge carried, one paragraph>' > msg.txt
    gh api -X PUT repos/<owner>/<repo>/pulls/<pr>/merge -f merge_method=merge \
      -f sha=$SHA -f commit_title='merge(uN): <what landed>' -F commit_message=@msg.txt

If the endpoint is refused, merge locally with the same message
(`git checkout -B main origin/main`, `git merge --no-ff cloud/N-<slug>`) and
push `main`, and file the refusal as a residual unless one records it. Then:

    git fetch origin main && git checkout -B main origin/main
    .venv/bin/python scripts/board.py residuals --land
    git add docs/residual-findings.md docs/ledger docs/residuals && git commit -m "docs(residuals): number what landed"   # only if it numbered any
    git push origin main

If the push is refused because `main` moved, fetch, merge `origin/main` into
`main` and push again; the numbering commit carries no code, so the battery
need not run for it. Never force push `main`. For each residual `--land`
named as meeting the board bar, file its issue (METHOD's board bar):

    gh api -X POST repos/<owner>/<repo>/issues -f title='R-N: ...' -F body=@r.md -f 'labels[]=residual'

For each live check the OWED paragraph names (the live library, the account,
rekordbox), file one attended card, `A<N>: <the check>` (METHOD's local
work), labelled `attended` alone, its body opening `**Depends on:** #<the
release card or this card>` and saying what to run and when it is done, by
these rules (decided by Phillip on 2026-11-24, after the attended queue grew
with every landing):

- **Never a card for the macOS battery**, alone or as a half of a live card.
  The battery is owed by `main`, not by a unit, and METHOD-local's standing
  battery settles every merge before the commit it runs on. A test file the
  Mac must read green is named in the OWED paragraph, never on a card.
- **Never a card for a measurement only the Mac's test run could change**,
  such as a mutation row or a replay table the container could not hold.
  Record it in the table as unmeasured on Linux, with the reason. If the
  standing battery later shows a test newly failing there, that failure is
  a card of its own.
- **Never a card for what the next ordinary sitting does anyway.** A change
  to a sync pass, a landing, a visit or a tag run that the next pass shows
  without a step of its own goes in the OWED paragraph, under the words
  `Read at the next pass:`, and the `crate-sync` skill's closing report
  reads it there. A card is for a check that needs a step no ordinary
  sitting takes (a throwaway, a copy, a named verb).
- **One card per check, never one per landing.** Search the open attended
  cards first (`board.py local`). When one already runs the same verb on
  the same library or account, comment on it with what this landing adds,
  and do not file another.

Then `board.py audit --labels-only`, and post `Landed`, short, linking the
record rather than restating it (U196): the pull request, the merge commit,
`docs/restart/uN.md` on `main`, residuals numbered and issues filed, attended
cards filed, and a line each for the battery, the review rounds and the
mutation table. Tell the coordinator, and stop.

## Small card runs

A thread handed two or three small cards in the same module (METHOD's card
sizes) builds each as its own unit from step 1, reusing its reading and its
baseline; a card that turns out not to be small is built as its size calls
for, and the rest of the run goes back to the coordinator.
