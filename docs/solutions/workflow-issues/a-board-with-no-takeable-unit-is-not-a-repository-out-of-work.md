---
title: "A board with no takeable unit is not a repository out of work, because the ledger holds what the board was never given"
date: 2026-09-01
category: workflow-issues
module: "scripts/board.py, docs/residual-findings.md, CLAUDE.md, RESTART-cratekit.md"
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - "board.py next reports one Ready unit and it is attended, or reports nothing ready at all"
  - "A restart or handoff document is about to state that there is no work left on this board"
  - "A long unattended run is being provisioned and needs work to hand to it"
  - "A repository keeps two registers, one holding queued work and one holding recorded but unfixed findings"
  - "A residual is being weighed for promotion into a unit issue"
symptoms:
  - "The board reports 45 units, 44 done, 1 Ready, 0 blocked, and the one Ready unit is one no agent may take"
  - "board.py next prints Take #29 for U29 Cutover and retirement, which requires the live rekordbox library"
  - "board.py next still prints Take #29 after three genuinely takeable units are added below it"
  - "RESTART-cratekit.md states flatly that there is no takeable unit left on this board"
  - "docs/residual-findings.md holds 201 entries and 202 numbers, none of them queued as issues by design"
related_components:
  - "documentation"
  - "tooling"
tags:
  - "board"
  - "residual-finding"
  - "ledger"
  - "ready-state"
  - "attended-work"
  - "backlog"
  - "cutover"
  - "silent-failure"
---

# A board with no takeable unit is not a repository out of work, because the ledger holds what the board was never given

## Context

On 2026-09-01 a session was asked to set up a long unattended Relay run to get
Cratekit closer to code complete. It did the correct first thing, the one
`CLAUDE.md` names as the start of every session, and ran
`.venv/bin/python scripts/board.py next`. The answer came back as 45 units, 44
done, 1 Ready, 0 blocked, and the closing line `Take #29`.

Issue 29 is U29, "Cutover and retirement", and it is the single unit in this
repository that an agent must never take. Its own brief says "attended per
workflow, do not batch cutovers", and it requires each replacement workflow to
run correctly ON THE LIVE rekordbox library at least once. The live rekordbox
database is off limits by standing constraint. Both durable documents say so and
both say it loudly. `RESTART-cratekit.md` opens with "the one that is Ready is
the one you must not take" and then "**`board.py next` will say 'Take #29' and
you must not**". `docs/METHOD.md`'s "Do not touch" section carries a paragraph
written specifically so its reason would not expire, ending "Do not take it
because the board says Ready; Ready is a statement about dependencies, not about
who can do the work."

So the tool whose entire job is to answer "what should I work on" answered with
the one item nobody reading it was permitted to do, and the restart file's own
summary of the situation was "There is no takeable unit left on this board."

That sentence was true about the BOARD and false about the REPOSITORY.
`docs/residual-findings.md` on `main` held 201 entries under 202 numbers,
counted with `grep -c '^## R-'` and confirmed by the highest heading being R-202.
By deliberate design in `CLAUDE.md`, none of them is on the board. A residual is
"a real problem that was recorded rather than fixed, because it did not meet the
bar to hold a merge. It is not a queued task, it is the honest register of what
is known and accepted", and the contract says plainly "Do not backfill the rest",
with three good reasons. Putting the ledger on the board would claim intent to do
a hundred things nobody intends. It would flood the Ready column, because a non
unit issue with nothing waiting on it derives as Ready. And a residual's number is
unstable before its unit merges, since the number lives in the issue title and a
merge renumbers the incoming branch's residuals.

Every one of those reasons is correct. The consequence is that the ledger is
invisible to the tool by construction, and nothing in the tool says so at the
moment it reports an empty queue.

**This state was predicted, and the prediction is what makes it worth writing
down.** (session history) On 2026-08-29 a session found `board.py next` ranking
issue 29 first and repaired it correctly, by amending the issue's own dependency
line to name U42 and U45 and running `board.py sync`, which flipped the card to
Blocked without a label being touched. On 2026-08-30 U45 merged, its trailer
closed issue 63, the board workflow fired, and issue 29 flipped straight back to
Ready on the cascade. The restart file had warned it would. So the 2026-09-01
condition is not a new failure and not drift. It is the resting state of a
correct board, reached again the moment the last real dependency closed, and it
will be reached again after U46, U47 and U48 land.

Reading the ledger found three clusters carrying more product consequence than
anything the board had held. All three were verified against `main` before being
promoted, and all three survived that verification.

**R-198, nothing calls the job driver.** `cratekit.core.jobs.drive` has no caller
anywhere in `src`. The command that shows it cleanly is `git grep -n "drive(" --
src`, which on `main` returns exactly one line, the definition at
`src/cratekit/core/jobs.py:1181`. The other mentions of the name in `src` are not
calls: two strings that name the function inside causes it raises at
`jobs.py:1176` and `jobs.py:1242`, its `__all__` entry at `jobs.py:1414`, and two
docstrings in `src/cratekit/backup/cli.py` at 414 and 423, the second of which
states the absence outright in capitals.

**Two corrections to the ledger entry, found while re-verifying it, because both
change what a reader should expect.** R-198 says the search "returns its own
definition, two strings naming it in causes it raises, and nothing else", citing
`git grep -n "drive" -- src`. That command actually returns 221 lines on `main`,
and 99 word bounded, because `drive` is ordinary English in this codebase and
appears in prose about failing drives and drive letters across dozens of files.
Add the open paren. And R-198 says "the only driver that ever calls it is
`tests/job_worker.py`", which is true only of out of process drivers.
`git grep -rn "jobs\.drive(" -- src tests scripts` returns eight calls, one in
`tests/job_worker.py:57` and seven in `tests/test_jobs.py`, and that second file
is collected and runs on every battery. So the driver is not untested. It is well
tested and unreachable from the product, which is a sharper statement of the same
problem and the one worth carrying.
Sixteen resume branches across fifteen modules take the `if ctx.args.job:`
branch, reconcile, report and exit, so a queued job cycles between reported and
respawned while its items stay `pending` for ever. The entry calls itself a
cutover blocker in its own words and says the parity table cannot catch it,
because the parity table measures verbs.

**R-195, R-196 and R-197, the vendored downloader has never fetched a file.**
`_VendoredSource.fetch` at `src/cratekit/acquire/vendored.py:246` builds
`Download(tidal_obj, path_base, fn_logger)` at line 254. The vendored CLI at
`src/cratekit/_vendor/tidal_dl_ng/cli.py:250` builds the same object with five
further keywords, `skip_existing`, `progress`, `progress_overall`, `event_abort`
and `event_run`. Four of those are load bearing by R-197's own measurement, since
`Download.item()` dies on its first line at `self.event_abort.is_set()` against
`None`, and with the events but without the progress pair it returns a false flag
and logs nothing. Separately, `tool_settings` at `vendored.py:74` returns exactly
three settings and none of them is `path_binary_ffmpeg`, while
`Download.__init__`, which begins at `src/cratekit/_vendor/tidal_dl_ng/download.py:122`,
turns `extract_flac` off outright when that setting is empty, at lines 162 to 166. The tool does not read
PATH, so lossless extraction silently switches itself off while `crate doctor`
reports ffmpeg present. R-196 adds that the device flow client is served lossy
audio by the provider while a PKCE login on the same account, same track, same
minute is served a real FLAC. The product's central lossless promise has failed
silently since 2026-07-09, and `fetch` is marked `pragma: no cover` precisely
because the offline suite cannot reach it, which is why every green battery
missed it.

**R-200 and R-201, two silent wrong answers around the backup.** A failed archive
prune reaches no report, so dated remote folders accumulate unbounded with a
successful backup and a fresh published age standing over the silence. And the
destructive write session hard codes `remedy=Remedy.REPAIR_BACKUP_FACTS` over the
`GRANT_PATH_ACCESS` remedy the exception actually carries, in the refusal standing
immediately before the riskiest operation in the product. R-201 cites
that line as 1046, and on `main` today the hard coded line is
`src/cratekit/core/session.py:1048`, inside the `raise refuse(` that begins at
1043. The finding holds, its line number has drifted by two since 2026-08-29, and
the two sibling consumers named in the entry still carry the remedy through
correctly.

The action taken was to promote those into three unit issues in the house style,
U46 as issue 64, U47 as issue 65 and U48 as issue 66, each with a full brief
copied into the body and labeled `unit` and `phase-e`, then `board.py sync`.
The board went from 45 units, 44 done, 1 ready to 48 units, 44 done, 4 ready, 0
blocked, audit exit 0.

**And `board.py next` still said `Take #29`.** That is the part worth stopping on.
The three new units each reported "releases 0 open unit(s)" while issue 29
reported "releases 1", so it sorted above all of them and kept the recommendation
line. Adding real work to the board did not change what the board recommended.

## Guidance

**Distrust an empty board the moment its only Ready item is one you are not
allowed to take.** That is the exact condition, and it is narrower than "the
board looks quiet". A board with three ordinary units Ready is telling the truth.
A board whose Ready set is empty after you subtract what you may not perform is
not reporting that the work is finished, it is reporting that the dependency
graph has nothing left to say. Those are different claims and the tool prints
only the first.

**Do not trust the `Take #N` line to rerank after you add work.** It is sorted by
transitive reach, and reach counts every open issue rather than every open unit,
so a single residual that was given an issue can hold a unit at the top of the
list for ever. Issue 39 is R-2 and its body carries `**Closes with:** #29 (U29)`,
which is the entire reason issue 29 reports releasing one open unit. Read the
whole Ready list, not the arrow.

**When the Ready list is empty of takeable work, read `docs/residual-findings.md`
before concluding anything about the repository.** Not skimmed, and not only its
last few entries. It is the register the board deliberately excludes, so it is the
one place where a hundred known problems can sit while the queue reads as done.
Read the newest entries first, since they were written by the units closest to the
current tree, and read every entry that names itself a cutover blocker or says the
word "silently". Grepping it for `blocker`, `never`, `no caller` and `silently`
finds the load bearing ones fast. `CONCEPTS.md` and `docs/METHOD.md`'s merge bar
explain why an entry can be severe and still have been recorded rather than fixed,
which is the thing that makes the file counterintuitive.

**A residual becomes a unit only when somebody decides to act on it, and that
decision has a real cost.** Promotion is not relabeling. It requires a full brief
in the issue body in the house style, goal, requirements, dependencies, key
files, approach, test scenarios and verification, because `CLAUDE.md` says the
issue is the brief and a session that finds the brief insufficient is told to fix
the issue rather than work around it. It requires the `unit` label, because
`build_graph` in `scripts/board.py` reads `unit` to decide whether the body's
dependency line or its closes line supplies the edges, and `cmd_next` filters its
ready list to units. It requires a phase label so the card lands somewhere a
person reads. And it requires `board.py sync` afterwards, since `ready` and
`blocked` are derived values and hand editing them makes the board a thing that
has to be remembered rather than a thing that is true.

There is one worked precedent to copy from rather than inventing the shape again.
(session history) On 2026-08-25 R-168, a filename truncation measured at 149 of
150 sampled files, was judged to have crossed METHOD's three blocking conditions
and was promoted into issue 59 as U41, with the brief written by reading U40's
issue body as the template. That issue is closed and its body still cites R-168
by number.

**Promoting a residual does not renumber it, and must not.** `docs/METHOD.md`
states that residual numbers are append only and that a number, once given, is
that finding's for life, decided 2026-08-10 and reversing a sequential renumber
decided the day before. The reason is recorded there too, and it is exactly this
surface: GitHub issue titles carry the number in their text, a renumber silently
repoints every one of them at a different finding, and nothing in the repository
can see it. So carry the residual's existing number into the issue title, leave
the entry in the ledger where it is, and let `board.py audit` do its job of
checking that the issue still names the finding its number points at.

**Say which register you consulted when you report that a board is empty.** A
handoff line reading "there is no takeable unit left on this board" is accurate
and incomplete in a way that costs the next session a week. The honest form names
both registers, as in "the board has nothing takeable, and the ledger has N
entries nobody has triaged since R-M".

## Why This Matters

The mechanism is in `scripts/board.py` and it is small enough to state exactly.
`build_graph` parses each issue's dependency line into `deps`, computes
`open_deps` as the subset of those whose issues are still open, and
`derive_status` then answers from closure state and the graph alone. For a unit
it is one line, `return "Blocked" if node["open_deps"] else "Ready"`. The only
other thing that can divert a unit before it reaches that line is its card already
reading In Progress, which is a fact about a branch rather than about the work. So
Ready does not know what the work is, where it runs, what it touches, or who is
permitted to do it. It is a statement that every issue this
one declared a dependency on is closed, and nothing more, which is precisely what
`docs/METHOD.md` says about it in prose.

`cmd_next` then selects `n["unit"] and not n["closed"] and not n["open_deps"]`,
sorts by transitive reach and prints the top one as the thing to take. An
attended only unit satisfies that filter perfectly, so it is indistinguishable to
the tool from available work, and when it is the only survivor it becomes the
recommendation. The tool is not wrong about anything it claims. It is answering a
narrower question than the one the reader is asking.

**The same card has now failed in both directions, which is what identifies the
axis rather than the bug.** (session history) On 2026-08-28 issue 29 ranked first
while it was genuinely blocked, because its dependency line was stale. On
2026-09-01 it ranked first while it was genuinely unblocked and still untakeable.
Opposite errors, one shared cause: everything `board.py` knows about whether a
unit can be taken comes from that unit's declared dependency edges, and permission
is not an edge.

That is the smaller half. The larger half is that board emptiness is silent about
the ledger by construction, and the silence is a design decision rather than a
gap. `CLAUDE.md` keeps residuals off the board on purpose, and its three reasons
are good ones that this learning does not challenge. Backfilling 201 residuals
would claim an intent nobody has, would flood the Ready column since a non unit
issue with no closer derives as Ready, and would pin unstable numbers into issue
titles that a merge invalidates. Keeping them off the board is right.

The failure is therefore not in either register. It is in the join between them,
which exists only in a human reading step, and the reading step is skipped exactly
when the board says there is nothing to do, because that is the moment a session
believes it has its answer. Two registers, each correct, each honest about its own
scope, and the gap between them held a cutover blocker, a silently broken lossless
promise that had been broken for eight weeks, and a refusal that tells a person to
repair an intact file. None of that was hidden. All of it was written down, in
detail, by the sessions that found it, in the file the board is designed not to
show you.

## The guard that would catch half of this

Half of it is cheap and half of it is not, and the split is worth naming rather
than blurring.

The cheap half exists already and is not wired up. `derive_status` in
`scripts/board.py` has an `attended` branch that returns `"Attended"` before it
reaches the Ready computation, and four issues carry that label across all
states: 49 and 56 are closed attended chores, 50 is the open attended chore A2,
and 46 is a residual, R-9, that carries `attended` alongside `residual` because
its verification needs hardware. Issue 29 does not. It
carries `unit`, `ready` and `phase-f`. So the archetypal attended unit, the one
both durable documents warn about by number, is the one issue missing the label
the tool already understands. Two changes would close it. Add `attended` to issue
29 so the card stops reading Ready, and add `not n["attended"]` to `cmd_next`'s
ready filter so the recommendation stops naming it, since `cmd_next` does not
consult that flag today and the label alone would not silence the `Take` line.
Both belong to whoever next touches `board.py` rather than to this learning.

The expensive half has no test. Nothing can check that a session read
`docs/residual-findings.md` before concluding the repository is done, and no
assertion can decide whether a ledger entry deserves promotion, because that is a
product judgment about consequence. `board.py next` could print a line naming the
ledger and its entry count whenever its ready list is empty or contains only
attended units, which is a nudge rather than a guard and would have been enough
here. Beyond that it is a human reading step, which is why it is written down as
one.

## When to Apply

- `board.py next` returns one Ready unit and it is attended, or returns nothing
  ready at all.
- A restart file, handoff, or session summary is about to say the board is empty,
  the queue is drained, or the project is code complete.
- A long unattended run is being provisioned and needs work to hand to it, so the
  cost of picking wrong is a whole run rather than a wasted hour.
- Any moment the answer to "what is left" is being derived from a dependency
  graph, in this repository or anywhere else two registers split queued work from
  recorded work.
- Before promoting anything out of `docs/residual-findings.md`, so the append only
  numbering rule and the full brief requirement are both in view first.

## Examples

**The 2026-09-01 case, before.** `board.py next` printed 45 units, 44 done, 1
Ready, 0 blocked, and `Take #29`. `RESTART-cratekit.md` on `main` said "There is
no takeable unit left on this board. Every other issue is closed." Both were
accurate. `docs/residual-findings.md` at the same commit held 201 entries under
202 numbers, and three clusters of them were the highest consequence open problems
in the product.

**What the ledger held, verified against `main` in the same session.**
`git grep -n "drive(" -- src` returns one line, the definition at
`src/cratekit/core/jobs.py:1181`. Every call to `jobs.drive` in the repository is
in `tests/`, seven of them in the collected `tests/test_jobs.py`. The remaining
mentions in `src` are two cause strings, an `__all__` entry, and two docstrings in
`src/cratekit/backup/cli.py`, one of which states the absence outright at line
423. `src/cratekit/acquire/vendored.py:74`
returns three settings without `path_binary_ffmpeg` while
`src/cratekit/_vendor/tidal_dl_ng/download.py:162` to `:166` disables
`extract_flac` and `video_convert_mp4` together when that setting is empty. `src/cratekit/acquire/vendored.py:254` constructs
`Download` with three keywords where
`src/cratekit/_vendor/tidal_dl_ng/cli.py:250` passes eight.
`src/cratekit/core/session.py:1048` writes
`remedy=Remedy.REPAIR_BACKUP_FACTS` unconditionally. Each claim was read at the
line rather than taken from the entry, and the one discrepancy found was R-201's
citation of line 1046 against an actual 1048, drift of two lines since
2026-08-29.

**After.** Three issues created with full briefs, labeled `unit` and `phase-e`,
carrying their residual numbers in their titles. Issue 64 is U46, the job handler
registry, so queued work is actually run, for R-198. Issue 65 is U47, a lossless
landing, PKCE login and the ffmpeg the downloader is never told, for R-195, R-196
and R-197. Issue 66 is U48, the prune that fails into silence and the remedy the
session discards, for R-200 and R-201. After `board.py sync`, `board.py audit`
reports 48 units, 44 done, 4 ready, 0 blocked, and "The board matches the
repository". The residual entries stayed in the ledger under their original
numbers, unmoved.

**And the arrow did not move.** `board.py next` re-run after the sync listed all
four Ready units and still printed `Take #29`, because issue 39 declares
`**Closes with:** #29 (U29)` and that one residual issue gives issue 29 a
transitive reach of one against zero for each new unit. The fix for the pick was
to read the list and ignore the arrow.

**The counter example, so the rule is not read too widely.** This is not a licence
to promote residuals in bulk. 195 of the 201 stayed exactly where they are, and
should. What separated the six that moved was that each named a product behavior
that is wrong today for a user, not a docstring that overclaims or a test that
measures less than it says. The ledger's job is to hold the rest honestly, and it
is doing that job well.

## Related

- `docs/solutions/workflow-issues/a-false-claim-in-the-auto-loaded-contract-compounds-silently.md`
  is the parent of this learning and covers the same `CLAUDE.md` section, "The
  board is the queue", the same script, and the same issue 29. **This is not a
  fourth section of that document, and the difference is the mechanism rather
  than the episode.** That doc is about a sentence in an auto loaded contract
  being false and no check evaluating it, and its own second occurrence concluded
  the wrong pick was caused by a stale dependency declaration. This doc is about
  the derivation itself having no permission axis, which is true even when every
  dependency line is correct, as it was on 2026-09-01. Read that one first for why
  the two registers exist, then this one for what the split costs at the moment
  the queue empties.
- `docs/solutions/integration-issues/the-provider-serves-lossy-audio-to-the-device-flow-client-and-neither-the-vendored-tool-nor-the-adapter-can-log-in-any-other-way.md`
  is R-196 written up in full. It is the concrete proof that a ledger entry can be
  critical and correct and still sit unqueued for days, and it is one of the three
  findings promoted into U47.
- `docs/solutions/workflow-issues/an-explicit-gate-makes-a-queued-job-undriveable-without-the-run-id.md`
  found one verb's queued job undriveable for want of a run id in the payload.
  R-198, now U46, is the general case of the same shape: no queued job of any verb
  is driveable, because nothing calls the driver at all.
- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`
  is the rule U46 inherits. Landing the first call into the job driver makes that
  unit the owner of every unreviewed failure path the driver already carries.
- `docs/solutions/workflow-issues/a-guard-safe-only-because-its-subject-is-unimplemented-expires-when-it-lands.md`
  names what happens to the suite on the day U46 lands. Any guard that is green
  today because nothing drives a job is resting on a fact about what has not been
  built, and it expires on that merge.
- `docs/solutions/workflow-issues/a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md`
  applies to the ledger after a promotion. The entries stay where they are and the
  file is append only, so any pinned residual population is re-measured by
  differencing the sets rather than by checking that a total moved by six.
