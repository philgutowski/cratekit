---
name: cloud-unit
description: The pipeline for a Claude Code cloud session on the Cratekit board, from the cloud queue to a branch ready for the watcher. Use when a cloud session is asked to take the next card, build a card, run the cloud lane, or when a scheduled task fires in this repository.
---

# Cloud unit

A cloud session builds one card of the board the way METHOD's pipeline says,
and stops where a Mac is needed. It takes the card from the cloud queue, posts
a plan, builds with Opus 5.5 at high effort, has Fable review the built, drives
the findings to the merge bar, writes the record, pushes the branch and posts
"Ready for the watcher". The watcher, on Phillip's machine, runs the macOS
battery, measures the mutation table, merges and pushes `main`. A card that
needs the machine is set aside with the steps to run it locally.

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
  `gh api --paginate` all fail; `gh api` on `repos/<owner>/<repo>/...` works,
  for reads, comments and body edits. The GitHub MCP tools work for issues and
  comments too.
- `scripts/board.py cloud` is the queue, `board.py show N` the brief, and
  `board.py closing --since origin/main` the closing check. `start`, `sync`
  and `audit` without `--labels-only` are not for a cloud session.
- The Linux suite carries about 170 failures bound to this machine (root
  reads every directory, no `hdiutil`, a timing calibration pinned to one
  Mac, darwin paths). `scripts/cloud_battery.py` tells yours from the
  machine's. Never edit the calibration file, never skip or mark a test.
- `scripts/mutate.py` is not run here: it needs a green baseline the Linux
  suite cannot give. You write the rows; the watcher measures them on macOS.

## Models

Brainstorm, plan and build are Opus 5.5's at high effort. Review is Fable's at
high effort. The scheduled task starts its sessions on Opus 5.5, and the
project settings set the effort, so a scheduled session plans and builds
itself. A session on any other model delegates the plan and build steps to the
`opus-builder` agent and does the rest itself. The review step always runs the
`fable-reviewer` agent, whatever the session's own model.

## Writes you never make

A beat grid in any container. Anything under a real config path or a real
library. `main`. A pull request. A label, a project status, a close. Anything
in `.github/`. A commit trailer, a co-author line, a session line. An em dash,
an en dash or a double hyphen anywhere. A literal path to the skills directory
in any card, title, body or comment, because the feeder skips a card whose
text names it; describe it in words.

## 1. Orient

    git fetch origin main
    .venv/bin/python scripts/board.py cloud

It lists every open card labelled `cloud` by state and names the one to take.
A card is the cloud's only with that label; add it to a card to send it here.
Take the one it names, in its state:

- `review-owed`: a review from the watcher arrived on a branch already pushed.
  Go to step 7.
- `answered`: Phillip replied to a brainstorm or a question. Go to step 3
  with his reply.
- `ready`: nobody has taken it. Go to step 2.

If it names nothing, the session is done: say so and stop. Never take a card
it lists as held, waiting, set aside, blocked or attended, and never take over
a stale hold: a session that died may have pushed commits, and what becomes of
them is Phillip's call. Say that the hold is stale, naming the card, and stop.

Read the brief with `board.py show N` and every comment on the card:

    gh api repos/<owner>/<repo>/issues/N/comments --jq '.[] | "--- \(.created_at)\n\(.body)"'

## 2. Classify the card

Decide, from the brief, which of three the card is. Say which in the plan.

**It needs the machine.** The brief requires the live rekordbox database, the
library volume, the live account, rekordbox itself, a backup of the real
library, or Phillip at the desktop, and the unit cannot be built and proven
without that. Not merely verified live afterwards, which every unit is at an
attended sitting, but built. Post a comment headed exactly `Needs the machine`
with: why, and the exact steps to run it locally, as commands Phillip can paste
(`board.py start N` and the verbs, or `/board-up` if the fable builder can
take it). Then run `board.py cloud` again and take the next card. A session
sets aside as many cards as it must and builds at most one.

**It needs a brainstorm.** The brief has no Goal, no test scenarios, or no
verification, or it reads as an idea rather than a specification, or it
carries the `idea` label. Post a comment headed exactly `Brainstorm`: restate
the idea in two or three sentences, name what already does part of the job,
give two or three approaches each with its cost and main risk, recommend one,
and ask at most four questions, each as a multiple choice with your
recommendation first, so Phillip can answer in a word each. Then take the next
card. When his answer arrives, `board.py cloud` offers the card as
`answered`: fold the answers into the brief by editing the issue body
(`gh api -X PATCH repos/<owner>/<repo>/issues/N -F body=@brief.md`), keeping
the `**Depends on:**` line first, and go on to step 3.

**It is buildable.** Everything else. Go on.

## 3. Start

    git checkout -b cloud/N-<slug> origin/main      # the name board.py cloud printed
    .venv/bin/python scripts/cloud_battery.py baseline   # in the background; about fifteen minutes

The baseline is the machine's failures measured on the base, on this
container, and `compare` later diffs the branch against it. Start it before
the first edit so it measures the base and not your work in progress.

Post a comment headed exactly `Started`: the branch, the base commit, and the
session URL if you know it. That comment is the cloud's hold on the card; the
next session reads it and takes another card.

## 4. Plan

METHOD's step 2, as a message, never in plan mode: plan mode waits for an
approval nobody is here to give. Grep `docs/solutions/` by module and tag for
the area you are about to touch, read the matches, then write the plan: the
seam, the files, the test scenarios from the brief, the residuals the unit
closes, what is out of scope, and which of the three the card was. If the
brief is insufficient on a point the plan needs, fix the issue body, then plan
against the fixed brief. Post it headed exactly `Plan`. Then build it.

On a session that is not Opus 5.5, hand steps 4 and 5 to the `opus-builder`
agent with the card number and the branch, and wait for its report.

## 5. Build

METHOD's step 3. Guard first, then the code it governs. Commit in units of
meaning with subjects naming the unit, `feat(u57): ...`, subject and body
only. Run the test files for what you touched as you go; the full suite is
the gate, not the edit loop. Register what a later unit owes in
`tests/_pending.py`, never in a docstring.

## 6. Review, to the merge bar

METHOD's step 4, with Fable as the reviewer. Run the `fable-reviewer` agent
on the branch and take its report as findings to drive, not to argue with.
Apply what holds, commit the fixes as `fix(uN): ...`, and run the agent again
on the fixed branch. **At most two fix rounds.** What is still open when they
are spent becomes a residual file and the unit is ready. Then:

- **The mutation rows.** Up to 25 rows targeted at the code you added, in
  `docs/mutation/uN-rows.toml`, in the form of `docs/mutation/u99-b-rows.toml`.
  Do not run `scripts/mutate.py`. The watcher measures the rows on macOS and
  posts the table; you commit it byte for byte when the review asks.
- **The hunts a green suite cannot see**, METHOD's list, by hand.

## 7. The battery

    .venv/bin/python scripts/cloud_battery.py compare

Ruff and the scan must be clean. Every test under `NEWLY FAILING, yours` is
yours to fix before the branch is ready, and a test under `no longer failing`
is worth a line in the report. The machine's failures are listed by count,
not fixed. Then the closing checks, both of which must pass:

    .venv/bin/python scripts/board.py closing --since origin/main
    git log origin/main..HEAD --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

The second must print nothing: a closing keyword next to an issue number
anywhere in the pushed range closes that issue, and the watcher writes the
trailer at the merge, not you.

For a `review-owed` card, check out its branch (`git checkout -t
origin/cloud/N-...`), fix what the review headed `Review from the watcher`
asks on that branch, run this step again, push, and post a comment headed
exactly `Review addressed` with the new tip and what changed. If the review
posted a measured mutation table, commit its files byte for byte as it says.

## 8. Record

METHOD's step 5. `docs/restart/uN.md` in the form of any recent file there,
with an OWED paragraph naming what this container could not run: the macOS
battery, the mutation measure, and the live verification at an attended
sitting. A residual is `docs/residuals/uN-<slug>.md` in the form
`docs/residuals/README.md` gives, with no number; never write into
`docs/residual-findings.md`. A `docs/solutions/` entry only if the unit found
something a future session would get wrong without it. Commit the record as
`record(uN): ...`.

## 9. Ready for the watcher

    git push -u origin cloud/N-<slug>

Then post a comment headed exactly `Ready for the watcher`: the tip SHA, the
commits on the base, the battery result with counts (`compare`'s three lines),
the review rounds and what each drove, what shipped, tests added by file and
count, residual files filed by path, the rows file path, and a "Deliberately
narrower" or "Noticed, not changed" line for anything left alone on purpose.
Then stop. The next cloud session reads the card again when the watcher
answers.
