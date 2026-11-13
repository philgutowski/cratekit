---
name: cloud-unit
description: The pipeline for a Claude Code cloud session on the Cratekit board, from the cloud queue to a unit merged and pushed on main. Use when a cloud session is asked to take the next card, build a card, or run the cloud lane.
---

# Cloud unit

The cloud is where Cratekit is built, decided by Phillip on 2026-10-27. A
cloud session takes one card from the queue and runs METHOD's whole pipeline
on it: brainstorm if it is an idea, plan, build with Opus 5.5 at the effort
its size calls for, review with Fable at high effort, drive the findings to the
merge bar, measure the mutation table sized to the card, write the record, open a pull request and merge it to
`main` with the closing trailer once CI on its head is green. A card that cannot be built without the machine is set
aside with the steps to build it locally, and only those are built locally.

Read `CLAUDE.md` and `docs/METHOD.md` before anything here. This skill says
what a cloud container changes; METHOD says what a unit is.

## Where you are

A cloud container with a fresh clone, no rekordbox, no library volume, no live
account, nobody watching. A question is a stop, so make the conservative call,
record it as a residual file, and keep going.

- The session hook built `.venv` with the dev extras. Run every tool through
  `.venv/bin/`. If the hook said it could not, build it yourself:
  `uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -e '.[dev]'`.
- GitHub GraphQL is refused here. `gh issue`, `gh repo`, `gh project` and
  `gh api --paginate` all fail; `gh api` on `repos/<owner>/<repo>/...` works
  for reads, comments, issue creation and body edits, and the GitHub MCP tools
  work for issues and comments. Deleting a remote branch is refused, so the
  repository's "Automatically delete head branches" setting removes a merged
  pull request's branch; one that survives its merge is listed in the record
  for Phillip's next local session.
- `scripts/board.py cloud` is the queue, `board.py show N` the brief,
  `board.py closing --since origin/main` the closing check,
  `board.py residuals --land` the numbering, and `board.py audit --labels-only`
  the audit. `start`, `sync` and a plain `audit` need GraphQL and stay local.
- The Linux suite carries about 170 failures bound to this machine (root reads
  every directory, no `hdiutil`, a timing calibration pinned to one Mac,
  darwin paths). `scripts/cloud_battery.py` measures them on the base and reads
  the branch against them, and `scripts/mutate.py --known-failures` subtracts
  them from every mutation run. Never edit the calibration file, never skip,
  deselect or mark a test.

## Models

Brainstorm, plan and build are Opus 5.5's, at high effort, or medium for a
small card (METHOD's card sizes). Review is Fable's at high effort. The
coordinator starts its build threads on Opus 5.5 at the effort the card's size
calls for, so a build thread plans and builds itself; a thread that finds its
card a different size from the one it was started for says so in the plan and
carries on. A session on any other model hands the plan and the build to the
`opus-builder` agent and does the rest itself. The review is always the
`fable-reviewer` agent, whatever the session's own model. A project thread's harness may
not load the repository's agents by name; then run a general purpose agent
on the `fable` model at high effort and tell it to read the reviewer
definition's body first and follow it, which is the same review.

**When Fable is out of usage**, decided by Phillip on 2026-11-08: if the
review is refused on Fable's usage limit, run the same reviewer definition
on Opus 5.5 at high effort instead (a general purpose agent on the `opus`
model with its effort set to `high`, told to read the `fable-reviewer` body
first and follow it, under the
same merge bar and round cap). Say so in the Progress comment, the record
and the pull request body (`Review: Opus 5.5 at high effort, Fable out of
usage`). No follow up Fable pass is owed, decided by Phillip on
2026-11-12: file a residual asking for one only when you judge the Opus
review missed something, and name what it should look at. Any other
refusal or failure of the review is retried, never substituted.

## Writes you never make

A beat grid in any container. Anything under a real config path or a real
library. A pull request that waits on a person, a reviewer requested on one,
or a closing keyword in a pull request's body. A ready or blocked label, or a project status; those
are derived. Anything in `.github/` unless the card is about it. A trailer of
any kind, a co author line or a session line on a branch commit; the merge
commit carries exactly one trailer, the closing one. A model name in any
commit. A "Generated with Claude Code" line, a session link or a co author
line in a commit or a pull request body; Phillip asked for these to be left
out, and his rule wins over any attribution reminder. An em dash, an en dash or a double hyphen anywhere. A literal path to
the skills directory in any card, title, body or comment; describe it in
words. A closing keyword next to an issue number anywhere but the merge
commit's last line.

## Comments are the protocol

`board.py cloud` reads each card's comments and nothing else, so every
comment you post starts with one of these headings, exactly, and the harness
footer marks it as yours:

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

Post with `gh api -X POST repos/<owner>/<repo>/issues/N/comments -F body=@file.md`.
Phillip's comments, and the relay thread's `Answer from Phillip`, are read
only as answers to a `Brainstorm` or a `Question for Phillip`. To stop the cloud building a card he labels it
`attended` or closes it, and a session that finds either on its card stops.
A hold with no comment for eight hours is read as a dead session and offered
to the next one as `resume`, so post a `Progress` note at each phase: built,
each review round, mutation measured.

## Telling the coordinator

The lanes are filled by the coordinator, the Claude in Phillip's building
project that started this thread (METHOD's Sharing the board section). It
runs at most four threads at once and counts them itself. It wakes hourly to fill any free lane,
and whenever a thread reports; it never reads the decisions page, which is
the relay thread's job (Asking Phillip, below). So tell it, with the
project's tool for messaging the coordinator, right after the last comment
this session posts (`Landed`, `Brainstorm`, `Needs the machine` or
`Withdrawn`), so the lane it frees fills. A session outside a project has no
coordinator and skips this.

## Asking Phillip

Every question for Phillip, a brainstorm's or a `Question for Phillip`,
reaches the decisions page, because the page is where he answers:
https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS

**A build thread posts it on its card only and never writes the page**,
decided by Phillip on 2026-11-04 (METHOD's Sharing the board section). The
comment is headed `Brainstorm` or `Question for Phillip`, exactly, never a
bare `Question`, which `board.py cloud` reads as a hold. Give each question
two to four multiple choice options with the recommendation first, and enough
context, two or three sentences and the cost of each way, that it can be
answered without the rest of the card. A question never stops the build:
make the conservative call, record it, and keep going. Phillip's other
project, which files the cards, copies the question onto the page in the form
below and posts his answer back.

**The page's form**, for the filing project, which writes it; a build
thread never does. One document per question into the page's `decisions` collection with
the `ArtifactData` tool (load it with ToolSearch, `select:ArtifactData`),
action `set`, `url` the page above, `collection` `decisions`, `doc_id`
`<card>-<short slug>-<n>`, and this body:

    {"card": N, "card_title": "U158: ...", "group": "<card>-<slug>", "order": n,
     "kind": "brainstorm" or "question", "question": "...",
     "context": "two or three sentences a reader needs, and the cost of each way",
     "options": [{"label": "...", "detail": "one line"}, ...],
     "recommended": 0, "status": "open", "answer": null,
     "asked_by": "the lane worker on #N", "asked_session": "<the asking thread's session id>",
     "asked_at": "<now, ISO 8601 UTC>"}

The recommendation is the option at index `recommended`, and the page shows
it first and marked. Give two to four options; the page adds its own
"something else". Write the context so the question can be answered without
opening the card. The filing project then ends a comment on the card with a
line linking the page and, where it has the `PushNotification` tool, sends
one short notification naming the card and that a decision waits on the
page. A document is marked answered by the page and relayed by the relay
thread, never by the writer.

**How his answer reaches the card.** Phillip presses Answer on the page,
which saves his choice in the document and sets its `status` to `answered`.
The scheduled task "Cratekit decisions relay" wakes the project thread "Wire
decisions page answers to cards", called the relay thread here, every hour
at 34 minutes past. It posts each answered document on its card under
`Answer from Phillip`, or sends it to the document's `asked_session` when it
names no card, sets the document's `status` to `relayed` with `relayed_at`
and `relayed_note`, and tells the building project's coordinator, which
starts a thread on the card if none of its threads is still building it. `board.py cloud` reads that heading as his reply whoever posts it, and
offers the card as `answered`. The coordinator's own hourly wake fills free
lanes only and never reads the page.

**The fast path.** The page cannot reach a project session by itself, because a
comment on a page sent to Claude wakes only a session watching that page,
and no project session can watch one. So while any answer is saved but not
relayed, the page shows a "Pass on your answers" box holding a ready prompt
that lists each one (card, question, answer, note and decision id), with a
button that copies the prompt and opens the Cratekit project chat in a new
window, and a button that only copies it. Phillip pastes it into that
project's chat, its Claude messages the relay thread, and the thread relays
at once.
Without the paste an answer waits for the hourly check.

## 1. Orient

    git fetch origin main
    .venv/bin/python scripts/board.py cloud

It lists every open unit and residual card by state, says how many of the
cloud's lanes are held (five by default, `CLOUD_LANES` in `scripts/board.py`),
and names the next card to take. **If your prompt names a card, take that one**,
as long as the queue lists it as takeable; the coordinator chose it so that
parallel threads never pick the same card. Otherwise take the one the queue
names, passing over any card held by the `grok/` builder, which belongs to
another builder (METHOD's Sharing the board section). `board.py cloud` cannot
see that builder's hold, since its comments carry no session footer, so
before posting `Started` look for a `grok/` branch naming the card's number
(`git ls-remote --heads origin 'grok/*'`) and a comment of that builder's on
the card. If every lane is held, or nothing is takeable, say so in one line,
tell the coordinator (above), and stop.

**Post `Started` on the card at once**, before reading anything else, so the
coordinator or a session reading the queue a minute later finds it held, then run
`board.py cloud` again. If it now says more cards are held than there are
lanes, sessions read a lane free in the same minute: it names the ones that
held first, and if yours is not among them, post `Withdrawn` on your card and
stop. A `Brainstorm` or `Needs the machine` posted later replaces the hold.
Take the card in its state:

- `answered`: Phillip replied to a brainstorm or a question. A question does
  not stop its thread, so if a `Progress` comment or a pushed `cloud/N-...`
  commit is newer than the question and under eight hours old, the card is
  still that thread's: pass over it. Otherwise fold his answer into the brief
  (step 2's brainstorm paragraph) and go to step 3.
- `resume`: a session holding it died. Post `Resumed` rather than
  `Started`, then check out `origin/cloud/N-...` if it exists and read its
  log against the card's comments to see how far it got; otherwise start
  fresh from step 3.
- `ready`: nobody has taken it. Go to step 2.

Read the brief with `board.py show N` and every comment on the card:

    gh api repos/<owner>/<repo>/issues/N/comments --jq '.[] | "--- \(.created_at)\n\(.body)"'

## 2. Classify the card

Decide from the brief which of three the card is, and say which in the plan.

**It needs the machine.** The unit cannot be built and proven without the
live rekordbox database, the library volume, the live account, rekordbox
itself, a backup of the real library, or Phillip at the desktop. Not merely
verified live afterwards, which an attended sitting does for any unit, but
built: a unit whose code and tests run on fixtures and disposable copies is
the cloud's, and its live proof is an OWED line in its record. Post `Needs
the machine` with why, and the exact local steps as commands Phillip can
paste (`board.py start N`, the verbs, the attended sitting). Then run
`board.py cloud` again and take the next card. A session sets aside as many
cards as it must and builds at most one.

**It needs a brainstorm.** The brief has no goal, no test scenarios or no
verification, or reads as an idea rather than a specification, or carries the
`idea` label. Post `Brainstorm`: restate the idea in two or three sentences,
name what already does part of the job, give two or three approaches each
with its cost and main risk, recommend one, and ask at most four questions,
each a multiple choice with your recommendation first, so Phillip can answer
in a word each, in the form "Asking Phillip" below gives. The thread never
writes the decisions page; the filing project copies the questions there.
Then take the next card. When the card comes back
`answered`, rewrite the brief with his answers folded in
(`gh api -X PATCH repos/<owner>/<repo>/issues/N -F body=@brief.md`), keeping
the `**Depends on:**` line first and every field the brief form has.

**It is buildable.** Everything else. Go on.

## 3. Start

    git checkout -b cloud/N-<slug> origin/main      # the name board.py cloud printed
    .venv/bin/python scripts/cloud_battery.py baseline   # background job, about twelve minutes

The baseline measures the machine's failures on the base, on this container,
and writes them to `.cloud-battery/baseline.txt`. The clone is shallow, so it
first fetches `main`'s full history and refuses if it cannot (U200, from
R-1191): a test the missing history holds red would otherwise be subtracted by
its id, and every later failure of it with it. Every failing id is read
whole off pytest's own reports (U268), and `compare` refuses a baseline
measured before that, whose ids were cut at their first space, with the
command that measures it again. It runs on disk unless `--temp memory` is
given (U273) and names the place in its header; `compare` and the driver
run in that place, and a baseline naming none is measured again the same
way. Leave it on disk: until #702 is answered a memory baseline reads the
inode bound test as the machine's. Run it as a tracked
background job with a two hour timeout from the start (a background job in a
cloud thread is stopped at 30 minutes otherwise) before the first edit, so it measures the base and not your
work in progress, and edit nothing under `src` or `tests` until it reports.

Post `Progress`: the branch, the base commit, the session URL if you know it.

## 4. Plan

METHOD's step 2, as a message and never in plan mode: plan mode waits for an
approval nobody is here to give. Grep `docs/solutions/` by module and tag for
the area you are about to touch and read the matches. The plan names the
seam, the files, the test scenarios from the brief, the residuals the unit
closes, what is out of scope, which of the three the card was, and its size
(small, medium or large, METHOD's card sizes), which sets its effort, its
review rounds and its mutation table. If the
brief is insufficient on a point the plan needs, fix the issue body, then plan
against the fixed brief. Post it as `Plan`, then build it.

On a session that is not Opus 5.5, hand steps 4 and 5 to the `opus-builder`
agent with the card number and the branch, and wait for its report.

## 5. Build

METHOD's step 3. Guard first, then the code it governs. Commit in units of
meaning with subjects naming the unit, `feat(u57): ...`, subject and body
only. Run the test files for what you touched as you go; the full suite is the
gate, not the edit loop. Register what a later unit owes in
`tests/_pending.py`, never in a docstring. Push the branch at each commit of
meaning (`git push -u origin cloud/N-<slug>`), so a session that dies leaves
its work where the next one resumes it. Post `Progress` when it is built.

## 6. Review with Fable, to the merge bar

METHOD's step 4. Run the `fable-reviewer` agent on the branch, telling it the
card's size, and take its report as findings to drive, not to argue with.
Apply what holds, commit the fixes as `fix(uN): ...`, and push. Note the head
round one reviewed.

**Round two only when it can find something**, decided by U196. If round one
found nothing BLOCKING and no file under `src`, `tests` or `scripts` changed
after it, there is no round two. A small card gets round two only when round
one found something BLOCKING. Otherwise run the agent again, telling it round
one's head, and it reviews the fix commits (`git diff <round one head>..HEAD`)
rather than the whole branch. **At most two fix rounds.** What is still open
when they are spent becomes a residual file and the unit goes on. Post `Progress` after each round, naming
what it drove. Then the hunts a green suite cannot see, METHOD's list.

## 7. The mutation table

METHOD's mutation table, sized to blast radius (decided by Phillip on
2026-11-02): up to 25 rows for a unit that writes or deletes, about 8 for a
read only report or a static registry, and none for a unit that changes only
docs or skill text, whose record says so in one line and skips the rest of
this step. Rows target the code the unit added, in
`docs/mutation/uN-rows.toml` in the form of `docs/mutation/u99-b-rows.toml`.
Commit the rows, then measure them as a tracked background job, given a two
hour timeout from the start as the baseline is, starting
nothing else against the tree until it reports:

    .venv/bin/python scripts/mutate.py docs/mutation/uN-rows.toml --known-failures .cloud-battery/baseline.txt

The driver subtracts the machine's failures from every run, so its baseline
is green net of them and its table says so. It refuses a known failures file
whose header does not end `history full ids whole`, which refuses a baseline
measured before U268, whose ids were cut at their first space, or names no
place for its temporary files (U273), and refuses on a shallow clone, so pass it only a baseline `cloud_battery.py` measured. If it still refuses a red
baseline, rerun the test it names alone. If it fails alone it is yours: fix
it. If it passes alone it is intermittent under the parallel run: run the
driver again, and if the same test reddens the baseline a second time, treat
it as yours. **Never write an id into the baseline file by hand**: it is
measured, and a hand added id is a regression excused for every later run.
A zero row is driven the way METHOD says. Commit
the table, `docs/mutation/uN.md` and `.json`, and post `Progress`.

## 8. The battery

    .venv/bin/python scripts/cloud_battery.py compare

Ruff and the scan must be clean. Every test under `NEWLY FAILING, yours` is
yours: rerun it alone first, since one test here is known to be intermittent
on ext4 under a parallel run, and fix every one that fails alone. A test
under `no longer failing` is worth a line in the record.

## 9. Record

**Docs first**, by METHOD's Docs always current: grep every doc it lists
for what the change touched and correct each line the change made untrue, in
this branch, committed as `docs(uN): ...`. The record carries the `Docs` line.

METHOD's step 5. `docs/restart/uN.md` in the form of any recent file there,
with an OWED paragraph naming what this container could not run: the macOS
battery, and the live verification at an attended sitting if the unit has
one. A residual is `docs/residuals/uN-<slug>.md` in the form
`docs/residuals/README.md` gives, with no number; never write into
`docs/residual-findings.md`. A `docs/solutions/` entry only if the unit found
something a future session would get wrong without it. Commit the record as
`record(uN): ...` and push the branch.

## 10. Merge and land, through a pull request

METHOD's step 6, done here, decided by U158: the unit reaches `main` through
a pull request this session opens and merges itself once CI is green. Nobody
reviews it and nothing waits on a person.

    git fetch origin main
    git merge origin/main          # only if main moved; then step 8 again in full
    .venv/bin/python scripts/board.py closing --since origin/main
    git log origin/main..HEAD --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'
    git push -u origin cloud/N-<slug>

The closing check must exit 0, and the keyword scan must print nothing. Check
`tests/_pending.py` first: a register that still owes this unit a module makes
CI red on the pull request whatever the trailer says, so discharge the entry
or point it at the later unit that owes it before you open one.

**Open the pull request** over REST, since `gh pr` needs GraphQL (the GitHub
MCP `create_pull_request` tool works as well):

    gh api -X POST repos/<owner>/<repo>/pulls -f title='UN: <what landed>' \
      -f head=cloud/N-<slug> -f base=main -F body=@pr.md --jq .number

The body is short, because the record already holds the detail (U196): a
first line reading `Requested by Phillip`, then a line naming the card by its link (the issue URL, never a keyword and a
number), a link to `docs/restart/uN.md` on the branch, and five lines at most:
the `cloud_battery.py compare` counts, the review rounds, the mutation table's
result, the residual files, and what is OWED. Never restate the record. **No closing keyword anywhere in
it**: GitHub closes from a pull request body on merge, which would bypass
`board.py closing`, so the merge commit's trailer is the one close.

**Wait for CI on the head commit** with one tracked background job, never a
foreground sleep and never a poll you repeat by hand, so the session wakes
once (U196), given a two hour timeout from the start, since the script waits
up to an hour and a background job is stopped at 30 minutes otherwise:

    SHA=$(git rev-parse HEAD)
    .venv/bin/python scripts/wait_ci.py $SHA      # exit 0 green, 1 red, 2 timed out, 3 unread

It waits for the pull request run on that head and prints one line. Exit 3
means the runs could not be read three times in a row, and the line says
why: fix the read (the token, the repository), never the branch. Every
check run on the head must be `completed`, and green means each conclusion is
`success`, `neutral` or `skipped`; to read them by hand:

    gh api repos/<owner>/<repo>/commits/$SHA/check-runs \
      --jq '.check_runs[] | "\(.name) \(.status) \(.conclusion)"'
    gh api "repos/<owner>/<repo>/actions/runs?event=pull_request&head_sha=$SHA" \
      --jq '.workflow_runs[] | "\(.name) \(.status) \(.conclusion)"'

The push of the branch runs CI too, and its check runs land on the same head,
so green over the check runs alone can be the push's run only. **Wait until
the second command lists a completed `success` run for the pull request**:
that run is the one that judges the pull request's range and its card. A pull
request that conflicts with `main` gets no `pull_request` run at all, so
when the head shows a push run and no `pull_request` run, merge `origin/main`
into the branch, run step 8 again, push, and wait on the new head.

CI judges the pull request's own range and the card its head branch names
(`board.py closing --pull-request-head`), so a branch whose card a register
still owes is red here. **If CI is red**, fix it on the branch and push again,
inside the two fix rounds METHOD allows; a failure that is the machine's and
not the branch's is said in the body. **If `main` moved** while you waited,
merge `origin/main` into the branch, run step 8 again in full, push, and wait
on the new head.

**Merge it** through the API as a merge commit, the title and the trailer
exactly as a local merge would carry them, and `sha` pinned to the head CI
judged:

    printf '%s\n\nCloses #N\n' '<what the merge carried, one paragraph>' > msg.txt
    gh api -X PUT repos/<owner>/<repo>/pulls/<pr>/merge -f merge_method=merge \
      -f sha=$SHA -f commit_title='merge(uN): <what landed>' -F commit_message=@msg.txt

The trailer is the message's last line and the only closing keyword in it.
**If the merge endpoint is refused**, merge locally with the same message
(`git checkout -B main origin/main`, `git merge --no-ff cloud/N-<slug>`) and
push `main`; GitHub then marks the pull request merged on its own, and the
refusal is a residual file if no residual already records it.

Then on `main`:

    git fetch origin main && git checkout -B main origin/main
    .venv/bin/python scripts/board.py residuals --land
    git add docs/residual-findings.md docs/residuals && git commit -m "docs(residuals): number what landed"   # only if it numbered any
    git push origin main

If the push is refused because `main` moved, fetch, merge `origin/main` into
`main`, and push again; the numbering commit carries no code, so the battery
need not run again for it. Never force push `main`.
For each residual `--land` named as meeting the board bar, file its issue
over REST, titled `R-N: ` and the ledger heading exactly, with a body opening
`**Depends on:** none` and the goal, key files, approach, test scenarios and
out of scope:

    gh api -X POST repos/<owner>/<repo>/issues -f title='R-N: ...' -F body=@r.md -f 'labels[]=residual'

For each live check the record's OWED paragraph names (a run on the live
library, the account, rekordbox, or the macOS battery), file one attended card
for Phillip's Mac, titled `A<N>: <the check>` with N one past the highest `A`
title on the board, read just before filing because parallel threads file
them, labelled `attended` and nothing else, with a body opening
`**Depends on:** #<the release card or this card>` and saying what to run and
when it is done. The attended work section of `docs/METHOD-local.md` is the
form.

Then `board.py audit --labels-only`, and post `Landed` on the card, short,
linking the record rather than restating it (U196): the pull request, the
merge commit, a link to `docs/restart/uN.md` on `main`, residuals numbered and
issues filed, attended cards filed, and one line each for the battery, the
review rounds and the mutation table. The push of
the trailer closes the card and the board workflow relabels what it released.
Then tell the coordinator, so the lane this card held fills at once, and stop.

## Small card runs

A thread the coordinator hands two or three small cards in the same module
builds them one after another, decided by Phillip on 2026-11-02 (METHOD's
card sizes). Each card is its own unit from step 1: its own `Started`, plan,
branch from the current `main`, review, record, pull request and `Landed`.
What carries over is the thread's reading and its baseline: measure the
baseline again only if `main` moved in `src`, `tests`, `scripts` or
`pyproject.toml` since it was measured. If a card turns out not to be small,
build it as its size calls for and hand the rest of the run back to the
coordinator.
