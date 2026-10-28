---
name: cloud-unit
description: The pipeline for a Claude Code cloud session on the Cratekit board, from the cloud queue to a unit merged and pushed on main. Use when a cloud session is asked to take the next card, build a card, run the cloud lane, or when a scheduled task fires in this repository.
---

# Cloud unit

The cloud is where Cratekit is built, decided by Phillip on 2026-10-27. A
cloud session takes one card from the queue and runs METHOD's whole pipeline
on it: brainstorm if it is an idea, plan, build with Opus 5.5 at high effort,
review with Fable at high effort, drive the findings to the merge bar, measure
the mutation table, write the record, merge to `main` with the closing
trailer, push `main`. A card that cannot be built without the machine is set
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
  work for issues and comments. Deleting a remote branch is refused, so a
  pushed `cloud/` branch stays after its merge; that is expected.
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

Brainstorm, plan and build are Opus 5.5's at high effort. Review is Fable's at
high effort. The scheduled task starts its sessions on Opus 5.5 and the
project settings set the effort, so a scheduled session plans and builds
itself. A session on any other model hands the plan and the build to the
`opus-builder` agent and does the rest itself. The review is always the
`fable-reviewer` agent, whatever the session's own model.

## Writes you never make

A beat grid in any container. Anything under a real config path or a real
library. A pull request. A ready or blocked label, or a project status; those
are derived. Anything in `.github/` unless the card is about it. A trailer of
any kind, a co author line or a session line on a branch commit; the merge
commit carries exactly one trailer, the closing one. A model name in any
commit. An em dash, an en dash or a double hyphen anywhere. A literal path to
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
| `Answer from Phillip` | his answer from the decisions page, posted by the dispatcher; read as his reply |
| `Needs the machine` | set aside, with the steps to build it locally |
| `Withdrawn` | this session lost a race for the lane and released the card |
| `Landed` | merged and pushed on `main` |

Post with `gh api -X POST repos/<owner>/<repo>/issues/N/comments -F body=@file.md`.
Phillip's comments, and the dispatcher's `Answer from Phillip`, are read
only as answers to a `Brainstorm` or a `Question for Phillip`. To stop the cloud building a card he labels it
`attended` or closes it, and a session that finds either on its card stops.
A hold with no comment for eight hours is read as a dead session and offered
to the next one as `resume`, so post a `Progress` note at each phase: built,
each review round, mutation measured.

## Waking the dispatcher

The lanes are filled by a dispatcher session that a scheduled task wakes every
hour. A worker wakes it sooner: when its prompt names a dispatcher session,
send that session the message `Dispatch` with the claude-code-remote
`send_message` tool, right after `Started` (so the next free lane fills) and
right after the last comment this session posts (`Landed`, `Brainstorm`,
`Needs the machine` or `Withdrawn`, so the lane it frees fills). A worker with
no dispatcher named skips this; the hourly task still comes.

## Asking Phillip

Every question for Phillip, a brainstorm's or a `Question for Phillip`, goes
on the decisions page as well as on the card, because the page is where he
answers: https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS

Write one document per question into the page's `decisions` collection with
the `ArtifactData` tool (load it with ToolSearch, `select:ArtifactData`),
action `set`, `url` the page above, `collection` `decisions`, `doc_id`
`<card>-<short slug>-<n>`, and this body:

    {"card": N, "card_title": "U158: ...", "group": "<card>-<slug>", "order": n,
     "kind": "brainstorm" or "question", "question": "...",
     "context": "two or three sentences a reader needs, and the cost of each way",
     "options": [{"label": "...", "detail": "one line"}, ...],
     "recommended": 0, "status": "open", "answer": null,
     "asked_by": "the lane worker on #N", "asked_session": "<your session id>",
     "asked_at": "<now, ISO 8601 UTC>"}

The recommendation is the option at index `recommended`, and the page shows
it first and marked. Give two to four options; the page adds its own
"something else". Write the context so the question can be answered without
opening the card. Then end the card's comment with a line linking the page,
and if the `PushNotification` tool is available, send one short notification
naming the card and that a decision waits on the page. The dispatcher posts
his answer back on the card under `Answer from Phillip`, which is what
releases the card as `answered`; never mark a document answered or relayed
yourself.

## 1. Orient

    git fetch origin main
    .venv/bin/python scripts/board.py cloud

It lists every open unit and residual card by state, says how many of the
cloud's lanes are held (three by default, `CLOUD_LANES` in `scripts/board.py`),
and names the next card to take. **If your prompt names a card, take that one**,
as long as the queue lists it as takeable; the dispatcher chose it so that
parallel workers never pick the same card. Otherwise take the one the queue
names. If every lane is held, or nothing is takeable, say so in one line, wake
the dispatcher (below), and stop.

**Post `Started` on the card at once**, before reading anything else, so a
dispatcher or session reading the queue a minute later finds it held, then run
`board.py cloud` again. If it now says more cards are held than there are
lanes, sessions read a lane free in the same minute: it names the ones that
held first, and if yours is not among them, post `Withdrawn` on your card and
stop. A `Brainstorm` or `Needs the machine` posted later replaces the hold.
Then **wake the dispatcher**, so the next free lane fills now rather than at
the hour. Take the card in its state:

- `answered`: Phillip replied to a brainstorm or a question. Fold his answer
  into the brief (step 2's brainstorm paragraph) and go to step 3.
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
in a word each. Put the same questions on the decisions page, as "Asking
Phillip" below says. Then take the next card. When the card comes back
`answered`, rewrite the brief with his answers folded in
(`gh api -X PATCH repos/<owner>/<repo>/issues/N -F body=@brief.md`), keeping
the `**Depends on:**` line first and every field the brief form has.

**It is buildable.** Everything else. Go on.

## 3. Start

    git checkout -b cloud/N-<slug> origin/main      # the name board.py cloud printed
    .venv/bin/python scripts/cloud_battery.py baseline   # background job, about ten minutes

The baseline measures the machine's failures on the base, on this container,
and writes them to `.cloud-battery/baseline.txt`. Run it as a tracked
background job before the first edit, so it measures the base and not your
work in progress, and edit nothing under `src` or `tests` until it reports.

Post `Progress`: the branch, the base commit, the session URL if you know it.

## 4. Plan

METHOD's step 2, as a message and never in plan mode: plan mode waits for an
approval nobody is here to give. Grep `docs/solutions/` by module and tag for
the area you are about to touch and read the matches. The plan names the
seam, the files, the test scenarios from the brief, the residuals the unit
closes, what is out of scope, and which of the three the card was. If the
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

METHOD's step 4. Run the `fable-reviewer` agent on the branch and take its
report as findings to drive, not to argue with. Apply what holds, commit the
fixes as `fix(uN): ...`, push, and run the agent again on the fixed branch.
**At most two fix rounds.** What is still open when they are spent becomes a
residual file and the unit goes on. Post `Progress` after each round, naming
what it drove. Then the hunts a green suite cannot see, METHOD's list.

## 7. The mutation table

METHOD's mutation table, up to 25 rows targeted at the code the unit added, in
`docs/mutation/uN-rows.toml` in the form of `docs/mutation/u99-b-rows.toml`.
Commit the rows, then measure them as a tracked background job, starting
nothing else against the tree until it reports:

    .venv/bin/python scripts/mutate.py docs/mutation/uN-rows.toml --known-failures .cloud-battery/baseline.txt

The driver subtracts the machine's failures from every run, so its baseline
is green net of them and its table says so. If it still refuses a red
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

METHOD's step 5. `docs/restart/uN.md` in the form of any recent file there,
with an OWED paragraph naming what this container could not run: the macOS
battery, and the live verification at an attended sitting if the unit has
one. A residual is `docs/residuals/uN-<slug>.md` in the form
`docs/residuals/README.md` gives, with no number; never write into
`docs/residual-findings.md`. A `docs/solutions/` entry only if the unit found
something a future session would get wrong without it. Commit the record as
`record(uN): ...` and push the branch.

## 10. Merge and land

METHOD's step 6, done here.

    git fetch origin main
    git merge origin/main          # only if main moved; then step 8 again
    .venv/bin/python scripts/board.py closing --since origin/main
    git log origin/main..HEAD --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

The closing check must exit 0, and the keyword scan must print nothing. Check
`tests/_pending.py` before writing the trailer: if the register still owes
this unit a module, merge without it and say so in `Landed`. Then:

    git checkout -B main origin/main
    git merge --no-ff cloud/N-<slug>     # message: merge(uN): <what landed>, ending with the line Closes #N
    .venv/bin/python scripts/board.py residuals --land
    git add docs/residual-findings.md docs/residuals && git commit -m "docs(residuals): number what landed"   # only if it numbered any
    git push origin main

If the push is refused because `main` moved, fetch, merge `origin/main` into
`main`, run step 8 again in full, since two units can be green apart and red
together, and push again. Never force push `main`.
For each residual `--land` named as meeting the board bar, file its issue
over REST, titled `R-N: ` and the ledger heading exactly, with a body opening
`**Depends on:** none` and the goal, key files, approach, test scenarios and
out of scope:

    gh api -X POST repos/<owner>/<repo>/issues -f title='R-N: ...' -F body=@r.md -f 'labels[]=residual'

Then `board.py audit --labels-only`, and post `Landed` on the card: the merge
commit, the commits it carried, the battery counts from `compare`, the review
rounds and what each drove, the mutation table's result, tests added by file
and count, residuals numbered and issues filed, and what is OWED. The push of
the trailer closes the card and the board workflow relabels what it released.
Then wake the dispatcher, so the lane this card held fills at once, and stop.
