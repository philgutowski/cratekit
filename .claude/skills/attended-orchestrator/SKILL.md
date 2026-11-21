---
name: attended-orchestrator
description: Run a whole attended sitting on Phillip's Mac from one session. Reads the board for every open attended card, groups them into one battery, the sweeps on copies, the rekordbox settlements, one sync pass and its visit, drives rekordbox and app dialogs with desktop control, directs worker sessions Phillip starts with a one line kickoff through files in the ignored state folder, records and closes each card, and asks Phillip nothing. Use when Phillip says /attended-orchestrator, run the attended work, work the attended cards, or start an attended sitting.
---

# The attended sitting

This session is the orchestrator of an attended sitting on Phillip's Mac, in
the Cratekit checkout. It drives every open attended card on the board to
done, or to the furthest point it can reach today, and leaves a record of
each. It uses desktop control for rekordbox, the streaming app and any
dialog, so Phillip need not be at the keyboard, and it directs worker
sessions Phillip starts, so the long and noisy work happens outside its own
context.

**Attended only.** rekordbox is opened by an attended session and by
nothing else (CLAUDE.md, the standing constraints). A cloud session, a job
and a test never run this skill.

**Ask nothing.** Phillip's standing instruction, given 2026-11-21: "Don't
ask me any more questions just follow your recommendations until I say
otherwise." Unless he has since withdrawn it (check project memory or the
latest sitting record, and assume it holds), wherever a card, a skill or
METHOD would put a question to him, take the recommended option, or the
most conservative one when none is named, write the decision and why into
the sitting record, STATE.md and a Progress comment on the card, and carry
on. Leave for him only the steps that physically need him (hardware he must
plug in or carry) or that the permission system refuses; those go in the
closing report, never as a wait. This is the one place the skill departs
from CLAUDE.md, whose stop takes the conservative call: here the
recommendation wins, by that instruction, and the record says which was
taken.

## 1. Orientation, before anything else

1. Read `CLAUDE.md`, `docs/METHOD.md`, `docs/METHOD-local.md` and
   `RESTART-cratekit.md`. They are the contract and win over this skill
   wherever the two differ. Read the `rekordbox-visit`, `crate-sync` and
   `file-card` skills before their first step. Grep `docs/solutions/` by
   module before touching an area.
2. **CLAUDE.md's standing constraints are absolute**, every one of them:
   the beat grid, the live database written only through a gate answered as
   `session` once its rehearsal is read (a difference in a path read,
   recorded and approved; a failed rehearsal or a difference in what is
   written a stop), the backup rule, the conditions for opening rekordbox and
   the check after quitting it, and DJ_tools read only for code. Beside them
   METHOD's do not touch list, no personal data, credentials, library paths
   or absolute home paths in any committed file, and METHOD's commit forms with no model name, no co
   author, session or "Generated with" line and no dashes. Records name a
   track by artist and title and a folder by its role ("a copy of twenty
   library files in a temporary folder"), never by a path. Beside them, this
   sitting **never cuts a release**, whatever a card or skill suggests;
   **never writes the decisions page**; **never retires, moves, disables or
   changes anything of DJ_tools**, its files or its schedules; and **never
   starts a restore onto a drive**, since a bare metal restore erases the
   drive it restores onto, even one that appears mounted and spare. A card
   that asks for a release cut is left open and named in the closing report
   as Phillip's to ask for, by the `release` skill.
3. `git checkout main && git pull --ff-only`, then
   `.venv/bin/python scripts/board.py local` and
   `.venv/bin/python scripts/board.py cloud`. The open attended cards are the
   work list, and nothing else is. Read each with `board.py show N` and its
   comments: the issue is the brief, and its steps are the steps. Read its
   dependency line and whether each card it names is closed.
4. **Which `crate` runs each card.** Read `crate --version` and the latest
   tag. For each card, find the merge commit of the unit it proves
   (`git log --grep="^merge(uN)" origin/main`, or `merge(rN)` for a residual)
   and check
   `git merge-base --is-ancestor <that commit> v<installed version>`. A card
   whose unit is in the installed copy runs on it. A card whose unit landed
   after it runs on the development checkout's own `.venv/bin/crate` at the
   `main` commit pulled, and the record names that commit. Never install raw
   `main` with pipx, and never cut a release to get a newer copy.
5. Read the last sitting number in `docs/cutover.md`. This sitting is the
   next one. Every record goes under one sitting heading, append only, in the
   house form of the sitting before it, and the heading says this skill drove
   the sitting.

## 2. The shared state, and how the workers take direction

All coordination lives in one folder inside the checkout's ignored `.local/`
directory, so nothing in it is ever committed: `.local/attended/<DATE>/`,
with `<DATE>` the sitting's start date in the form 2026-11-21, kept for the
whole sitting across midnight. Create it at the start,
and write the real date wherever `<DATE>` appears, in the copy of
`WORKER.md` and the kickoff line too. Its layout:

    STATE.md                 the ledger, written by the orchestrator only
    WORKER.md                the worker rules, copied from this skill's folder
    workers/W1/order.md      the current order to W1, absent when it has none
    workers/W1/report.md     W1's report on its last order
    workers/W1/status        one word: starting, idle, working, retiring
    workers/W1/done/         finished orders and reports, numbered, kept
    workers/W2/...           the same for W2
    scratch/                 temporary copies, sweeps' JSON, database diffs

**STATE.md** lets any session, a fresh orchestrator included, pick up the
sitting cold. Keep it short and current: the sitting number and the `main`
commit; which `crate` each card runs on; one line per card with its status
(todo, in progress with whom, done with the record commit, left open and
why); every decision taken under the standing instruction with its reason;
who holds the live library and desktop control (always the orchestrator);
and the next step. Rewrite it after every step that changes any of these.

**An order** is a markdown file that stands alone: the cards it serves, the
goal, the exact commands (with which `crate`), what to read and count, what
the report must contain, and what the worker must not do. Write it under a
temporary name and rename it to `order.md`, so a worker never reads half a
file.

**A report** is the worker's answer, in the form `WORKER.md` gives. Long
output stays in `scratch/` and the report names the file. Read reports, not
logs. Once a report is read, move it into the worker's `done/` beside its
order, so the next wait does not return on it.

**Waiting without polling inside a turn.** To wait for a report, start a
background shell that exits when it appears with the worker idle or
retiring, run in the background so it wakes this session when it exits, and
get on with other work meanwhile:

    until [ -f .local/attended/<DATE>/workers/W1/report.md ] && grep -qxE 'idle|retiring' .local/attended/<DATE>/workers/W1/status; do sleep 30; done

A worker that reads `retiring` has stopped: read its report, then ask
Phillip for a fresh one, as Keeping context small below says.

**Starting the workers.** Right after orientation, copy this skill's
`WORKER.md` into the state folder with the date written in, create
`workers/W1` and `workers/W2` with status `starting`, post a macOS
notification besides saying it in the reply, and ask Phillip to open two new
terminal tabs in this checkout, run `claude` in each, and paste:

    You are Cratekit attended worker W1. Read .local/attended/<DATE>/WORKER.md and follow it.

(W2 in the second tab.) The notification:

    osascript -e 'display notification "Start workers W1 and W2" with title "Cratekit orchestrator"'

That is the only thing asked of him at the start. Do not wait on it: begin
the live work in section 4 at once. If a worker has not written `idle`
within thirty minutes, move its waiting `order.md` into its `done/` so a late
worker never runs it twice, and do the order through a subagent (the Agent
tool), so that only its report enters this context.

**Who does what.** The orchestrator alone: desktop control, rekordbox, the
streaming app, every live gated verb and its approval, `crate backup run`,
`crate session ack`, every commit, push, card comment and card close.
Workers: the macOS battery, sweeps and reads on copies in `scratch/`,
database diffs on disposable copies, reading the code and docs, drafting
records and card briefs. `WORKER.md` lists what a worker never does.

**The checkout holds still while a worker runs from it.** The battery, a
sweep and a database diff all run from this checkout's editable install, so no
commit, pull or checkout happens in it until the order's report is in: a
record drafted meanwhile waits in `scratch/`. A worker's sweep is a Cratekit
job, so rekordbox opens only between sweeps, when `rekordbox-visit`'s
preflight finds no job running.

**Keeping context small.** Give each order one job. A worker near half its
context finishes its order, writes `retiring` and stops; notify Phillip to
start a fresh one in a new tab with the same kickoff line, and it takes the
same name and reads `done/` for history. When this session's context passes
about half, finish the step in hand, bring STATE.md fully up to date,
release desktop control as the `rekordbox-visit` skill's preflight says, and
notify Phillip to start a fresh orchestrator with this skill. A fresh
orchestrator that finds STATE.md resumes from its next step and repeats no
done one.

## 3. How each card is closed

METHOD-local's attended work section is the procedure: a record and its
commit on `main`, then a merge pull, never a rebase or a force, and a push.
Fold each report's draft into the sitting's section of `docs/cutover.md`, or
the card's own file where its brief names one. Then post on the card,
headed `Progress` and naming the record's commit:

    gh api -X POST repos/<owner>/<repo>/issues/N/comments -F body=@file.md

and close it when its "Done when" holds whole:

    gh api -X PATCH repos/<owner>/<repo>/issues/N -f state=closed -f state_reason=completed

A card met only in part gets the Progress comment and stays open, saying
what is still owed and what it waits on. A run that shows code must change
is never fixed here: file a card with the `file-card` skill from the
worker's draft brief, and leave the attended card open saying so. A decision
taken under the standing instruction goes in the same Progress comment, as
"Decided by the session under Phillip's instruction of 2026-11-21", with the
options and why.

A question that cannot be settled even conservatively should not arise. If
one does, post it on its card under the exact heading `Question for
Phillip`, in the form the `cloud-unit` skill's Asking Phillip section gives,
take the recommended option at once, and carry on. The filing project copies
it to the decisions page; never write the page and never wait for an answer.

## 4. The work, in sittings

Group the cards so one battery, one sweep, one rekordbox sitting and one
sync pass each serve as many cards as they can, write the plan into
STATE.md, and run it in this order. The sittings that need no live library
go to the workers first, so they run while the live ones do.

**The battery (a worker, first).** One battery over the `main` commit
pulled, in this checkout with a clean tree, serves every card owing a macOS
battery at or after a merge that commit carries: CLAUDE.md's three
commands, plus any test file a card says must pass whole. The order asks for
the counts and every failure with its test id; the orchestrator judges
whether a failure is the card's. Never a worktree, because the editable
install names this checkout. A timing test that fails while a sweep loads
the machine is run again alone after it, never edited or skipped. Never
skip, deselect, mark or weaken a test, and never touch the timing
calibration.

**Sweeps and other reads on copies (a worker, beside the battery).** A card
that reads a `tag folder` run, a matcher or anything else off files runs on
copies in `scratch/`, never on the library's own files: the worker copies
the shape the card describes, clears what it says to clear, runs the verb
under `crate --output json`, and reports each number the card's "Done when" asks
for. One sweep shaped for several cards serves them all, and the order says
which card reads which count. A card whose unit is still open records what
this run read and closes only if its own "Done when" is met whole.

**Settlements in rekordbox (the orchestrator).** A card that asks what
rekordbox itself writes runs early, because a unit waits on it. Use a
throwaway file made in `scratch/` (a ten second silent AIFF) and a playlist
made by hand, never a real track; take the BEFORE and AFTER copies the card
asks for with `crate backup run`, each after both processes are confirmed
gone; hand the table by table comparison of disposable copies to a free
worker; put the library back as it was the next time rekordbox is open; and
record the shape as a `docs/solutions/` entry and a sitting line, and in the
waiting unit's brief under a heading naming the settling card.

**One sync pass and its visit (the orchestrator).** The `crate-sync` skill
runs it end to end, and the `rekordbox-visit` skill is its visit, on the
`crate` that carries every unit the pass's cards prove. Read each card's
"When" and serve every one the pass can: queue reads after the intake jobs
resolve (a review answered by the recommendation it shows, one with none
left open), refusal and tag paths from the pass's JSON, album cover and
timing reads if an album of the size a card asks for lands, and any
rekordbox probe a card owes, done inside the visit in place of its first
analysis, by either of its paths, and followed by the visit as that skill
writes it. A probe that
changes a rekordbox setting puts it back to Phillip's standard afterwards,
and a screenshot confirms it. If the pass lands nothing, record that and
leave the cards that needed files open, saying so.

**Checks that need a change on Phillip's account (the orchestrator, with
desktop control).** Where a card says Phillip should act in an app, the
choice is the session's: pick the safest candidate the card allows (one on
no playlist of his own and not among his favourites), note it, make the
change, run the check with rekordbox gone, then undo it and read the check
once more to show the undo. Never buy, delete, unfollow, or send anything
outside the project.

**U29 (#29), the cutover, prepared and never performed in bulk.** METHOD's
do not touch section keeps U29 attended. Order a worker to read
`tests/test_cutover_parity.py`, the Feature Inventory it names,
`docs/cutover.md` and A5 (#178), and report one row per inventory entry: the
covering verb, the sitting whose record proves it live, and whether it is
proven. Record in `docs/cutover.md` a cutover line for each workflow newly
proven since the last such reading, one line per workflow and never one
batch line, naming its proving sitting, and list what each unproven one
needs. DJ_tools is not retired while any A5 line is open or until Phillip
has said he has lived through a full cycle on Cratekit alone. Post the
summary and the decision on #29 as Progress, and leave it open.

**What waits on Phillip or the world.** Check each such card at the start
and again before the end; run it if its condition has come true, otherwise
record why it waits and leave it open. These never start without him:
hardware he must connect (a real player, a spare drive); a step the
permission system refuses, such as the trash answer in `crate delete review`
on a removal he chose, named in the closing report as the one command he
would run; and a card waiting on a unit still open, new music, a new
purchase or a seller he has not registered.

## 5. Before the end

1. Every attended card worked has a Progress comment naming the record's
   commit, and is closed or says exactly what it waits on.
2. `.venv/bin/python scripts/board.py audit`: repair drift with `sync`, and
   report a contradiction rather than repair it.
3. `git fetch --prune`, and list each `cloud/` branch with no open pull
   request and no held card as stale, as METHOD's Sharing the board section
   says. Delete none but a plainly finished `cloud/` branch merged into
   `main`, list the rest for Phillip, and never touch a `grok/` branch.
4. rekordbox and rekordboxAgent both gone, no Cratekit job running, desktop
   control released, and the scratch copies deleted.
5. Tell each worker it is done with an order that says only "The sitting is
   over. Write your final report and stop."
6. Bring STATE.md to its end state, then give Phillip one report he can
   paste into the Cratekit project chat: the sitting number and commit; the
   battery result; one line per card (closed with its record commit, a new
   card filed, or left open and what it waits on); every decision taken under
   his standing instruction, one line each; the stale branches; and the
   short list only he can do (hardware, a removal of his choosing, anything
   the permission system refused), each with the one step it needs. Post a
   final macOS notification that the sitting is done.
