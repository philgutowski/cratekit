---
title: "A false claim in the auto loaded contract compounds silently, because every session begins by believing it"
date: 2026-08-14
last_updated: 2026-08-28
category: workflow-issues
module: CLAUDE.md
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: inadequate_documentation
resolution_type: documentation_update
applies_when:
  - "A file is auto loaded into every session and states a fact about the repository rather than an instruction"
  - "A contract sentence counts something the repository can count, and nobody has recounted it since it was written"
  - "An agent is about to create issues, files, or records so that a documented invariant becomes true"
  - "One batch of records created on one day is being described as though a rule produced it"
  - "Two registers hold overlapping items and one of them is being called the source of truth"
symptoms:
  - "A contract says every X has a Y, and counting X and Y gives ninety nine mismatches"
  - "The project owner asks what one of his own documented terms means and why it is not on the board"
  - "An agent invents a principle to explain a set whose members share only a creation date"
  - "Work is created to satisfy a documented invariant rather than because anybody wanted the work"
  - "The claim has been false for weeks and every check in the battery is still green"
related_components:
  - "documentation"
  - "tooling"
  - "testing_framework"
tags:
  - "contract-file"
  - "auto-loaded-context"
  - "unchecked-claim"
  - "stale-documentation"
  - "board"
  - "residual-finding"
  - "guard"
  - "silent-failure"
---

# A false claim in the auto loaded contract compounds silently, because every session begins by believing it

## Context

`CLAUDE.md` at the repo root is not an ordinary document. It is injected into
every session's system prompt before the session does anything, and it says so
about itself: "This file is the session contract" (`CLAUDE.md:6`). Nobody chooses
to open it. Every session has already read it by the time it reads anything else,
and reads it with the highest trust it gives any text in the repository, because
it is the thing that tells the session what the repository's rules are.

Until commit `e0387d9` on `main`, its section "The board is the queue" contained
this sentence, quoted exactly from `git show 9b03c0e:CLAUDE.md`:

> Every implementation unit, residual finding, and attended item is an issue on this
> repository, and the issue number matches the unit number: U11 is issue #11.

Two claims, both false, and they had been false for 12 days.

**The measurement.** `docs/residual-findings.md` carries 114 findings, counted as
`grep -c '^## R-'`, running from R-1 to R-115 with gaps, since residual numbers
are append only and a merge assigns the incoming branch's residuals fresh numbers
above `main`'s highest (`docs/METHOD.md:229`). Of those 114, exactly 15 have an
issue on the repository. Measured with:

```
gh issue list --repo philgutowski/cratekit --state all --limit 300 \
  --json number,title,createdAt
```

56 issues exist. 15 have a title matching `^R-[0-9]+:`. Thirteen of them predate this
session: #38 through #48, which are R-1 through R-11, and #52 and #53, which are
R-14 and R-15. The other two, #54 and #55 for R-102 and R-115, were created by the
session that found this. 38 unit issues plus A1, A2 and A3 make up the other 41.

The second claim fails too, and independently. U38 is issue #51, not #38, because
#38 is R-1. The corrected contract now says so, in its note that a unit number is not
guaranteed to match its issue number.

**When it went false.** The sentence was written in `00aa724` on 2026-08-02 at
16:07:37 local, and at that moment it was TRUE: the file held 11 residuals, and
issues #38 through #48 covering R-1 through R-11 had been created 14 minutes
earlier at 19:53 UTC. It was falsified at 17:34:56 the same day, one hour and 27
minutes later, by `d1f0ee9` adding R-12 and R-13 to the file. Neither has an issue
today. At 23:08 UTC the same evening, R-14 and R-15 got issues #52 and #53,
stepping over the gap without closing it.

Nothing else was created until this session. The date histogram is two buckets: 53
issues on 2026-08-02, and 3 on 2026-08-15 UTC, created at 01:46 by the session
that found this. So the 13 residuals that predate this session are not a
selection. They are one batch, made in one afternoon, before the file grew past
them.

**The claim did not live in one file, and the fix reached one of three.** The
sentence ORIGINATED in `docs/BOARD.md`, written by `86e3000` at 15:57:47, ten
minutes before it reached the contract, and there it is worse because it is a
TABLE: `docs/BOARD.md:13` and `:14` count 37 units and 11 residual findings, and
`:17` states "Issue numbers match unit numbers. U8 is issue #8, U37 is issue #37.
R-1 through R-11 are #38 to #48". `docs/HANDOFF.md:13` carries the same text
verbatim from the same commit: "All 37 units, the 11 residual findings, and the
attended items are issues".

**Both were still false at head after the first fix.** `e0387d9` corrected
`CLAUDE.md` and left the other two standing, which is this repository's fifth
recurring pattern, "a fix round fixes the instance it was handed and reproduces
the class one file over", committed in the same session that was documenting the
class. They were found afterwards, by a search that asked where else the sentence
lives rather than whether the one known copy was fixed. That search is the cheap
step and it is the one that did not happen first.

**All three are corrected as of 2026-08-15**, and none of the three now carries a
census. `docs/BOARD.md` and `docs/HANDOFF.md` state the build versus ledger rule
and point at the commands that produce a count, and BOARD.md records why it no
longer gives one. The sweep was repeated after the fix rather than assumed, which
is the step the first round skipped.

**Why the units kept their issues and the residuals did not.** `board.py start`
refuses to run without an issue. `scripts/board.py:329` raises on `no issue #N`,
`:331` on an already closed one, `:334` on a blocked one. A unit therefore cannot
be started without its issue existing, so the unit half of the sentence stayed
true by enforcement. A residual is written into a markdown file by hand and has no
such gate, so the residual half of the sentence decayed the moment somebody wrote
a finding and did not also open an issue. Which is to say: nobody had to do
anything wrong.

## A second occurrence, 2026-08-28: the commit that wrote this document also wrote the next false universal

`e0387d9` landed the guard and the first rewrite of the board section, 36
minutes before `54440a1`, titled "docs: the contract is the one file where a
false sentence compounds silently", which is the commit that wrote THIS
document. Its own body records touching `CLAUDE.md`'s backfill rationale one
more time: "CLAUDE.md's backfill rationale named the wrong surface: board.py
next filters to units, so what floods is the project board's Ready column."
That sentence is the one this section is about. The commit documenting the
danger of an unchecked universal in this file wrote a fresh, unchecked
universal into this file, in the same commit, and the claim below has carried
no checker since:

> `board.py next` filters to units and would be unaffected, so the damage is
> to the view a person reads rather than to the tool.

(`CLAUDE.md:44`, current text as of this writing.)

**The measurement.** `board.py next`'s ready list is genuinely filtered to
units: `ready = [n for n in graph.values() if n["unit"] and not n["closed"]
and not n["open_deps"]]` (`scripts/board.py:267`). A residual or attended issue
never appears as a candidate. But the sentence claims the tool is
`unaffected`, and the ranking that orders those candidates is a second
computation the sentence does not distinguish from the first. `build_graph`
gives every issue, unit or not, a `deps` list, taking it from `parse_deps` for
a unit and from `closes_with` for anything else in one ternary line
(`scripts/board.py:121`). Reverse edges are built from that combined pool with
no unit filter (`scripts/board.py:129` to `:132`), and the transitive reach score walks those
edges the same way, again with no unit filter, counting every open issue the
closure reaches: `node["reach"] = len({n for n in seen if not
by_number[n]["closed"]})` (`scripts/board.py:145`). `cmd_next` sorts the
filtered ready list by that score (`scripts/board.py:277`,
`key=lambda n: (-n["reach"], ...)`) and prints it as `f"releases
{node['reach']} open unit(s)"` (`scripts/board.py:295`), asserting a filter
that the candidate list has and the score does not.

**The concrete case.** Issue #39, `R-2: Four live portability and layering
violations in the source repository`, carries the `residual` label, not
`unit`, and its body reads `**Closes with:** #29 (U29)`. Because #39 is not a
unit, `build_graph` takes its `deps` from `closes_with`, giving it a `deps`
edge onto #29 exactly as though #39 were a unit depending on #29. That edge
became a reverse `unblocks` edge on #29, and #29's reach became 1. On
2026-08-28, `board.py next` ranked `#29 U29: Cutover and retirement` first,
`releases 1 open unit(s)`, ahead of `#60 U42` and `#63 U45`, both real units at
0 reach. Issue #29's own body opens `**Blocked.**`, and its verification
scenario, "the parity table is generated from the CLI verb inventory and
fails when a row has no covering verb," cannot pass until both #60 and #63
land. `board.py next` never surfaced either as the reason #29 was not
actually next. Running `tests/test_cutover_parity.py`'s `backlog()` and
`titles()` directly, independent of the issue graph entirely, gave the true
remaining rows (6, 7, and 31, covered by #60 and #63), which is what caught
the wrong pick before any branch was cut.

**Driven, not assumed: the reach defect is real and is not what decided this
pick.** Rebuilding `board.py`'s graph with the reach closure scoped to
unit-type nodes only, so #39's edge can no longer contribute, still ranks #29
first. Its reach drops to 0, tying #60 and #63, and the sort's tiebreak,
`key=lambda n: (-n["reach"], -len(n["unblocks"]), n["number"])`
(`scripts/board.py:277`), falls through to ascending issue number: 29 is
lower than 60 and 63. The decisive defect is one level up. `#29`'s own
`Depends on` line never names `#60` or `#63` at all, so `open_deps` is empty
for it and `board.py` has no way to know it is blocked on them, because
nothing told it so. U29's issue predates the discovery of U42 and U45 (both
found later, "discovered while handing off" per their own issue bodies) and
its dependency line was never amended to add them. So this session's actual
near miss was a stale dependency declaration on #29 itself, and the reach
computation's own defect, real and worth fixing on its own claim's merits, is
a second, independent thing that happened to be true at the same time rather
than the cause of the wrong pick.

**Fourteen days unchecked, same as the first claim, same file, same
mechanism.** `54440a1` landed 2026-08-14. This was found 2026-08-28. Nothing
in the battery evaluates it, for the identical reason `CONCEPTS.md`'s
`Battery` entry already gives for the first claim: `scan_repo.py` reads every
tracked file for machine specific paths and secrets, not for whether a
sentence about the codebase is true. `board.py audit` checks that a residual
issue's title still names the finding its number points at
(`repointed_residuals`, `scripts/board.py:404`); it does not check that a
residual's dependency edge, which is a legitimate and needed mechanism for
sequencing a fix behind the unit it depends on, cannot also distort that
unit's ranking. Nobody wrote a guard for this sentence when it was written,
because writing the sentence did not feel like writing a claim. It read like
an aside explaining why backfilling residuals onto the board is safe. It is
also, independently, an unqualified statement about what a specific function
computes, and this document exists because that is exactly the kind of
sentence this file cannot afford to leave unchecked.

**Still open, unlike the first occurrence.** The first false claim got both a
corrected sentence and a guard (`repointed_residuals`). This one has neither.
`scripts/board.py:145`'s reach computation still counts every open issue
reachable through `unblocks`, unit or not, and `CLAUDE.md:44` still asserts
the tool is unaffected. A fix needs to do one of two things, not describe a
third: filter the reach closure to unit-labeled nodes (change
`scripts/board.py:145` or the edges feeding it), or rewrite the sentence to
say what is actually true today, "the candidate list is filtered to units;
the score that ranks them is not." Either fix corrects the claim; neither
would have caught #29 on its own, since the driven check above shows its
dependency line, not its reach score, was the thing that was actually stale.
Checked against the other two homes this document already found for the
first claim's wording: as of 2026-08-28, neither `docs/BOARD.md` nor
`docs/HANDOFF.md` restates the `unaffected` claim, so this one has a single
home rather than three.

## Guidance

**The danger is not that documentation rots. It is WHERE this documentation
sits.** Rot is universal and mostly cheap. What makes this file different is the
combination of four properties, and it is the only file in the repository that has
all four:

1. It is auto-loaded, so it is read by every session without anybody choosing to
   read it.
2. It is the declared contract, so it is believed by default. A session that finds
   the code disagreeing with the contract will suspect the code first.
3. It makes claims about project STATE, not about code. State is not compiled, not
   imported, and not executed.
4. Therefore nothing checks it. Not the battery, not CI, not a reviewer, because a
   reviewer reads a diff and this sentence stopped appearing in diffs on
   2026-08-02.

**Rank the blast radius, because it is what decides how much care a sentence
deserves.** A false sentence in a normal document misleads whoever opens it, which
is sometimes nobody. A false sentence in the auto-loaded contract misleads
everyone, every time, starting before any work begins. The sibling document in
this directory records the same blind spot at the other end of the scale: a note
in a source docstring, addressed to one reader at one moment, false within one
hour and 47 minutes. Same mechanism, opposite radius.

**The specific smell is a contract asserting a UNIVERSAL about project state.**
"Every X is a Y." Universals about state are the claims most likely to be true
when written and false later, and the reason is structural: they are invalidated
by INACTION rather than by an edit. Nobody has to do anything wrong for "every
residual is an issue" to become false. They only have to not create issues. There
is no commit to catch, no diff to review, no moment where somebody decides
something. The claim simply stops being true while everyone behaves correctly.

Contrast a universal about code. "Every module under `src/cratekit/core` is
importable without the optional dependencies" is also a universal, but falsifying
it requires somebody to write an import, which is an act, which is reviewable, and
which a guard can be written against.

**State the RULE rather than the census, or make the census checkable.** This is
the fix and it generalizes. A census is a count at a moment. A rule is a
disposition that stays true as the count changes.

- Census, and it went stale: "Every residual finding is an issue."
- Rule, and it cannot go stale by inaction: "A residual earns an issue only if
  somebody decides to act on it", in the contract's build versus ledger section.

Where a census is genuinely the useful thing to say, say it with its date and its
provenance rather than as a standing fact. The contract now reads "Fifteen of one
hundred and fourteen do, which is an artifact of a single batch created on
2026-08-02 rather than a rule." That sentence can also go stale, but it goes stale
into being obviously historical rather than into being confidently wrong, and it
names the mechanism so the next reader can re-measure it in one command.

**When a contract must assert state, the claim needs a checker, and the checker
belongs wherever it can actually run.** Not necessarily in the test suite. Here the
check needs the network, because the state being asserted lives on GitHub, and the
battery must stay offline and deterministic. So it went into `board.py audit`,
which already talks to the network and is already the thing a session runs before
it ends.

**Write the guard that can hold, not the guard that restates the false claim.**
The obvious guard here is "every residual has an issue", and it is the wrong
guard: it would fail 99 times out of 114, and it SHOULD fail, because the
underlying claim was never something the project wanted to be true. Backfilling to
satisfy it would put 99 things on the board that nobody intends to do. The guard
that holds is the reverse one: an `R-N` issue that DOES exist must still name the
finding that number currently points at.

**And notice that the reverse guard is protecting a different thing than the false
sentence was.** It catches renumbering. A residual's number lives in its issue
TITLE, which is text on a server, and `docs/METHOD.md:239` records that the sweep
certifying the last renumber missed exactly that surface:

> The renumber was certified safe on a sweep showing zero numeric `R-NN`
> citations in `src`, `tests` or `scripts`. That sweep missed a second surface:
> **GitHub issue titles carry the number in their text**, as in
> `R-14: Analysis-file paths are share-relative`. A renumber silently repoints
> every one of those at a different finding, and nothing in the repository can
> see it. Same defect class as a rule verified against source while a second
> surface carries the same coupling.

So the good outcome of chasing a false census was a guard on a real coupling that
the census had been hiding. The census said the board and the file were mirrors,
and if they were mirrors there would be nothing to check. Once you admit they are
two registers answering two questions, the actual invariant between them becomes
visible.

**Report the mismatch as a CONTRADICTION, not as drift.** `board.py` already draws
that line and the reasoning transfers unchanged. Drift is a derived value that fell
out of date, and `sync` repairs it. A contradiction is two sources of truth
disagreeing, and `scripts/board.py:451` states why automatic repair is refused:
"repairing it automatically would mean picking one to overwrite, which is how the
wrong one wins silently." A residual title mismatch is exactly that shape. Either
the file was renumbered or the issue was retitled, and nothing in the tree knows
which.

**Reviewing a file for one property is not reviewing it.** (session history) The
contract was opened and assessed TWICE in the two days before this, by two earlier
`ce-compound` runs performing their Discoverability Check, on 2026-08-14 at 11:22
and again at 19:33. Both concluded the same thing, that `CLAUDE.md` surfaces
neither the solutions store nor the vocabulary file, and both logged
"Instruction-file edit: gap noted, not applied". So the file was examined twice for
whether it tells a session the truth about the repository, and the false sentence
was in the same section both times and was never read. A scoped review produces
the feeling of having reviewed, and the scope is invisible afterwards: what gets
recorded is "checked", not "checked for one thing".

**When you open a contract for any reason, the state claims in the section you are
touching are in scope.** That is the cheap version of the rule, and it is the same
correction the sibling document makes about coordination notes, arrived at from the
other direction.

**The agent-facing corollary, and it is the part worth saying out loud.** An agent
will not doubt the contract. It has no prior that would let it. The contract is the
highest trust text in the repository, it is presented as authoritative, and it
arrives before any evidence that could contradict it. A human maintainer carries a
vague sense that the README is probably a bit out of date; a fresh session carries
nothing of the kind. So this is the one file where being approximately right is not
good enough, and where "I will tidy the wording later" has a blast radius rather
than a cost.

## Why This Matters

Because the false sentence produced a wrong action, then a wrong explanation, then
a rationalisation defending the wrong explanation, in that order, before anybody
measured anything. All three happened inside the session that eventually found it.

**1. The wrong action.** The session read the contract, correctly, and concluded
that the board is the single source of truth for everything the repository owes.
Acting on that, it created three issues: #54 for R-102, #55 for R-115, and #56 for
A3, timestamped 2026-08-15 at 01:46:01, 01:46:17 and 01:46:36 UTC. Those are the
only three issues on the repository not created on 2026-08-02, and they exist
because a sentence written 12 days earlier said they had to. The reasoning was
sound given its premise. The premise had been false since the afternoon it was
written.

Two of the three are defensible on their own merits, which is worth saying,
because the failure here is not that three bad issues exist. It is that they were
created to satisfy a rule rather than because anybody decided to act on those
findings, which is a different reason and produces a different board.

**2. The wrong explanation.** The project owner then asked, in his own words, what
a residual even is and why it is not on the board. That question is the first
thing in the whole sequence that touched the actual state of the repository, and it
came from the person who had not read the contract that morning.

**3. The rationalisation.** Asked to recommend a course, the agent described the 13
residuals on the board as "the promoted ones", as though a promotion had happened.
That is an invented principle, constructed after the fact to make an accident look
like a policy. It is the most instructive moment in the sequence, because it is
where a false contract stopped merely misleading and started generating supporting
theory. The theory was plausible, internally consistent, and would have survived
any amount of further discussion.

**4. The measurement, finally.** Checking `createdAt` on them took one command
and ended it. All 13 were created within 3 hours and 15 minutes of each other on
2026-08-02, 11 of them within 10 seconds. There was no promotion, no selection, and
no principle. There was one batch, made while the file was 11 findings long, and
then the file grew and the batch did not.

**5. Why nothing caught it in 12 days.** `docs/METHOD.md:185` defines the battery
as three commands (`:190` through `:192`): `ruff check src tests scripts`, `pytest`,
and `scripts/scan_repo.py`.

Be exact about what this proves, because it is easy to overstate and a sibling
document had to be corrected for overstating it. `scan_repo.py` DOES read prose.
`scan_tree` at `scripts/scan_repo.py:475` walks every tracked path, skips only the
binary suffixes listed at `:71`, and runs `portability_violations` and
`secret_violations` over the text of everything else. `CLAUDE.md` was scanned on
every merge for 12 days. It is not an unread file.

The precise claim is narrower and it is the whole point: **nothing in the battery
evaluates whether a sentence is TRUE.** `scan_repo` asks whether text contains a
machine specific path or a credential. Those are properties of the string. Whether
"every residual finding is an issue" corresponds to the world is not a property of
the string, and no amount of reading the string harder will settle it. `CONCEPTS.md`
now records this as the boundary of the battery, in its `Battery` entry: "One of its parts does
read prose, hunting machine specific paths and secrets in any text it finds, but
nothing in it evaluates whether a sentence is TRUE."

That is the shared mechanism behind this document and its sibling, and it is why
they are a pair rather than two instances of documentation rot.

**6. What the fix actually was, both halves.**

The contract half. `CLAUDE.md:22` now opens the section with the split: "**The
board is the BUILD. `docs/residual-findings.md` is the LEDGER.** Two registers
answering two questions, and they are not mirrors of each other." Then units and
attended chores are the work and live on the board; a residual is a problem
recorded rather than fixed and lives in the file, "so it lives in the file and
usually has no issue at all"; the fifteen are named as a batch artifact; and
backfilling is forbidden by name with its reason (`:32`): "Putting the ledger on
the board would claim you intend to do a hundred things you have decided not to
do, and would bury the handful of units that are actually ready."

The guard half. `scripts/board.py` gained `residual_titles()` at `:387`, which
reads every `## R-N.` heading out of `docs/residual-findings.md` as text, and
`repointed_residuals()` at `:404`, which compares each `R-N:` issue title against
the heading that number now points at. `contradictions()` at `:439` folds the
result in at `:462` with `return found + repointed_residuals(graph)`, so a mismatch
surfaces through the audit that was already being run before every session ends,
with no new command to remember. `cmd_audit` at `:552` returns 2 when contradictions
exist and 1 for drift alone (`:583`).

**7. Driven, not asserted.** Baseline against the tree at `9cdc42e`:
`residual_titles()` parses 114 findings, the graph holds 15 issues matching
`^R-(\d+):`, and `repointed_residuals()` returns an empty list. `board.py audit`
prints "38 units: 28 done, 6 ready, 4 blocked" then "The board matches the
repository" and exits 0.

Then both failure modes, driven by substituting the parsed heading map in memory so
no tracked file was modified:

- R-14 retitled in the file. The guard reports
  `#52 R-14 names a different finding than the file does`, and prints both sides,
  the issue's `Analysis-file paths are share-relative, and the wrong join finds
  nothing` against the file's replacement text.
- The R-14 heading removed entirely. The guard reports `#52 R-14` with
  `the issue names it, docs/residual-findings.md has no such finding`.
- Restored. Empty list again, audit exit 0.

Both mismatches route through `contradictions()`, so both produce exit 2 rather
than exit 1, and the audit prints "Each one is a decision, not a repair"
(`scripts/board.py:576`) rather than offering a `sync`.

## When to Apply

Apply this whenever you are writing or editing a file that is loaded into a
session automatically. In this repository that is `CLAUDE.md`. Elsewhere it is
whatever the harness injects: a root agent instruction file, a skill body, a system
prompt fragment, a rules file. The trigger is the auto-loading, not the filename.

Concretely, stop and check when:

- **You are about to write "every", "all", "each", or "always" about project
  state** in a file every session reads. Ask what would have to happen for this to
  become false, and if the answer is "somebody does not do something", it will
  become false and nothing will tell you.
- **You are stating a count, a ratio, or a coverage claim.** "Fifteen of one
  hundred and fourteen" is fine WITH its date and its cause. "Every one" is not
  fine, because it has no date and reads as a rule.
- **You are describing the relationship between two registers.** Two lists that
  hold overlapping items will drift, always. Say which question each one answers
  rather than claiming they mirror.
- **You are editing that file for an unrelated reason.** This is the same
  correction the sibling document makes about coordination notes: editing the
  paragraph a claim lives in is not re-measuring the claim. Both documents now
  record a case of it.
- **A session has just acted on the contract and the result feels slightly
  wrong to the person who owns the project.** That reaction is the only detector
  this class of defect has. When the owner asks "why is it like that", the honest
  first move is to measure the state, not to explain the state. The explanation
  will be available and will be wrong.
- **You are about to explain why an existing set of things is the way it is.**
  If the explanation is a principle you did not read somewhere, check the
  timestamps before you offer it. Fifteen items with one shared creation minute is
  a batch. Fifteen items with fifteen different dates is a policy. The two look
  identical in a list and take one command to tell apart.
- **You are adding a check for a state claim.** Put it where it can run. A claim
  about the network cannot be checked by an offline suite, and forcing it in there
  either makes the suite flaky or makes the check a no-op.

Do NOT apply this as a reason to strip all state from the contract. A contract that
says nothing concrete is not safer, it is just less useful, and the reader will
reconstruct the missing state by guessing. The correction is to state state with a
date and a cause, or to give it a checker, not to go silent.

Do NOT apply the reasoning to ordinary documents at the same intensity. A stale
sentence in a handoff or a residual costs one reader one trip. The budget belongs
where the multiplier is.

## Examples

All commits are cited with the branch they sit on, because this project uses no
pull requests.

**The sentence, before and after.** From `git show 9b03c0e:CLAUDE.md`, the section
"The board is the queue":

> Every implementation unit, residual finding, and attended item is an issue on this
> repository, and the issue number matches the unit number: U11 is issue #11.

From `CLAUDE.md:22` onward at `9cdc42e`:

> **The board is the BUILD. `docs/residual-findings.md` is the LEDGER.** Two
> registers answering two questions, and they are not mirrors of each other.
>
> - Every implementation unit `U-N` is an issue, and so is every attended chore
>   `A-N`. Those are the work, and the board is where work is picked.
> - A residual `R-N` is a real problem that was recorded rather than fixed, because
>   it did not meet the bar to hold a merge. It is not a queued task, it is the
>   honest register of what is known and accepted, so it lives in the file and
>   usually has no issue at all. Fifteen of one hundred and fourteen do, which is
>   an artifact of a single batch created on 2026-08-02 rather than a rule.
>   **Do not backfill the rest.**

Note what changed in kind, not just in content. The old sentence is a census with
no date. The new text is a rule plus a dated census plus the reason the census
looks the way it does, and it names the wrong move so that a future session does
not have to rediscover why it is wrong.

**The census.**

| claim | measured | result |
|---|---|---|
| findings in `docs/residual-findings.md` | `grep -c '^## R-'` | 114 |
| highest number | `grep -o '^## R-[0-9]*' \| tail -1` | R-115, so the numbering has gaps |
| issues total | `gh issue list ... --json number,title` | 56 |
| issues titled `R-N:` | regex over titles | 15 |
| unit and chore issues | the remainder | 41, being 38 units plus A1, A2, A3 |
| issues created 2026-08-02 | `--json createdAt` | 53 |
| issues created 2026-08-15 | same | 3, all at 01:46 UTC, by the session that found this |

The 13 residual issues predating this session, in creation order: #38 through #48
covering R-1 through
R-11, all created 2026-08-02 between 19:53:49 and 19:53:58 UTC, so 11 issues in 9
seconds. Then #52 R-14 at 23:08:30 and #53 R-15 at 23:08:48. R-12 and R-13 were
skipped and remain skipped. #49 and #50 are A1 and A2, and #51 is U38, which is why
the unit numbering and the issue numbering diverge.

**The life of the claim, from git.**

| when | what | the claim |
|---|---|---|
| 2026-08-02 15:53 local | issues #38 to #48 created, covering R-1 to R-11 | (about to be) |
| 2026-08-02 16:07:37 | `00aa724` writes "Every implementation unit, residual finding, and attended item is an issue" into `CLAUDE.md` | TRUE, 11 findings and 11 issues |
| 2026-08-02 17:34:56 | `d1f0ee9` adds R-12 and R-13 to the file, with no issues | goes FALSE, 1h 27m later |
| 2026-08-02 19:08 local | #52 and #53 created for R-14 and R-15, stepping over the gap | still false |
| 2026-08-02 to 2026-08-14 | the file grows to 114 findings, no residual issues created | false, and worsening |
| 2026-08-15 01:46 UTC | a session reads the contract, believes it, and creates #54, #55, #56 | false, and now acted on |
| 2026-08-14 22:19:45 local | `e0387d9` corrects it and lands the guard | fixed |

The sentence stood for 12 days and 6 hours and was false for all but the first 87
minutes of it, so 12 days and 5 hours false. `e0387d9`'s own body rounds that to
"two weeks", which is the only imprecision in it.

**Why the units survived and the residuals did not.** `scripts/board.py:327`:

```python
node = graph.get(args.number)
if not node:
    raise Fail(f"no issue #{args.number}")
```

A unit cannot be started without its issue, and `board.py start` also refuses a
dirty tree (`:347`) and a non `main` branch (`:344`). The unit half of the sentence
was enforced by a program. The residual half was enforced by nobody, and the
difference is the whole outcome. This is worth generalizing: in any sentence of the
form "every A and every B is a C", check whether A and B are held true by the same
mechanism. Here they were not, and the half with no mechanism is the half that
rotted while the sentence kept looking like one coherent claim.

**The guard, and why it points the way it does.** `scripts/board.py:404`, from its
docstring:

> So the check is not that a residual has an issue. Most do not, and should
> not: the board is the build and the residual file is the ledger. The check
> is that an issue which DOES exist still names what its number now points at.

The parse is deliberately shallow. `residual_titles()` at `:387` matches
`^## R-(\d+)\.\s*(.+?)\s*$` line by line rather than parsing markdown, and says so:
"Read as text rather than parsed as a document, because the only structure this
needs is the heading line and the file is append only by rule."

**The two failure shapes, driven.** Substituting the heading map in memory, with no
tracked file touched:

```
RETITLED:
  #52 R-14 names a different finding than the file does
      issue: Analysis-file paths are share-relative, and the wrong join finds nothing
      file : Something else entirely
REMOVED:
  #52 R-14
      the issue names it, docs/residual-findings.md has no such finding
RESTORED: []
```

Baseline at `9cdc42e`: 114 findings parsed, 15 matching issues, 0 repointed,
`board.py audit` exits 0 with "The board matches the repository."

The two shapes are distinct on purpose. A retitle means the two registers disagree
about what a number means, and you have to decide which one moved. A missing
heading means the issue outlived the finding, which is what a renumber produces,
and it is the case `docs/METHOD.md:239` says the last certification sweep could not
see.

**A second reason backfilling could not have worked, which nobody argued at the
time.** (session history) A residual's number is not stable until its unit merges.
Every merge renumbers the incoming branch's residuals above `main`'s highest: U16's
block became R-66 to R-76, U27's R-20 to R-39 became R-80 to R-100, U23's became
R-81 to R-100. An issue opened for a residual while its branch is still in flight
therefore names a number that changes when the branch lands, and the issue title
keeps the old one. So the backfill the contract implied was not merely unwanted, it
was unstable at the exact moment somebody would most want to file. That is also
what `repointed_residuals()` now catches, which is the pleasing part: the guard
written after abandoning the backfill is the guard that would have been needed to
survive it.

**What the correction did not do.** It did not delete #54, #55 or #56. Two of the
three name real findings somebody may well act on, and R-115 in particular is a
live problem. Deleting them to make the board match a principle would be the same
mistake in the other direction: adjusting the state to fit the document. The
document was the thing that was wrong.

## Related

- **Its own second occurrence, above.** `CLAUDE.md:44`'s "`board.py next`
  filters to units and would be unaffected" was written by `54440a1`, the very
  commit that wrote this document, and stood unchecked for 14 days until
  issue #39's dependency edge on #29 falsified it (`scripts/board.py:145`,
  `:295`). Recorded in place rather than as a separate document, per the
  corpus-first rule this project's compounding tooling uses: the two are the
  same mechanism in the same file, and a second document would only need to
  point back here.
- `docs/solutions/workflow-issues/a-rewrite-is-not-a-re-measurement-of-the-claim-inside-it.md`,
  written the same day. **This is the pair, and they should be read together.**
  Both are about unverified prose that no check evaluates, and both were falsified
  by something happening elsewhere while the sentence sat still. The difference is
  radius and duration. That one is a coordination note in a docstring on one
  branch, claiming something about a second branch, addressed to whoever performs
  one merge, and it was false one hour and 47 minutes after being written. This one
  is the contract at the repository root, claiming something about the repository's
  own management state, read by every session that starts, and it was false for 12
  days. Same blind spot, opposite blast radius. The near symmetry in how fast each
  went false, one hour 47 minutes against one hour 27 minutes, is a coincidence
  worth noticing anyway: in both cases the claim was true when written and
  falsified the same afternoon by an act its author never saw.

  **This document also falsifies a sentence in that one, and the sentence was
  corrected in the same commit that added this file.** It read: "Every other claim
  in this repository is either executed by the suite or dated in
  `docs/residual-findings.md`. A docstring note is neither." The contract's board
  section was neither executed nor dated, and is not a docstring note, so it sat
  outside a set that document claimed was exhaustive. A document about unverified
  prose containing an unverified universal is not irony worth enjoying, it is the
  mechanism proving it generalizes past the instrument each document happens to be
  about. It is narrowed there now, with a pointer here.

- `docs/BOARD.md` and `docs/HANDOFF.md`: the other two homes of the same claim,
  both from `86e3000`, BOARD.md as a table. They survived the commit that fixed the
  contract and were corrected a day later, once a repo wide search asked where else
  the sentence lived. Neither now carries a count. The gap between "the contract is
  fixed" and "the claim is gone" lasted one day and is the most useful thing in this
  document, so it is recorded rather than smoothed over.
- `docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md`,
  the third merge time trap in this directory. Its subject is a register entry that
  IS enforced, and how discharging half of one silently removes a whole test file
  from collection. Read against this document it marks the other end of the range:
  there, the repository could state the obligation in a form the suite fails on, and
  the failure was in how the obligation was discharged. Here the claim could not be
  stated to the suite at all, so there was nothing to discharge and nothing to go
  red.
- `CONCEPTS.md`, the `Battery` entry and specifically its boundary
  paragraph at `:105`: the battery reads prose, hunting machine specific paths and
  secrets, and nothing in it evaluates whether a sentence is true. **That paragraph
  is the shared mechanism behind this document and the coordination note one**, and
  it is phrased carefully because the distinction is easy to get wrong in the
  direction of overclaiming. The sibling got it wrong twice and both were corrected
  on 2026-08-14: a draft said a conditional flag expression was the unreadable
  shape, and its Related section said the battery "cannot read" a docstring, when
  what the battery cannot do is judge whether a sentence is true.
- `CONCEPTS.md`, the `Coordination note` entry: "a register entry is an
  obligation the suite fails on, while a note is prose whose claim no check
  evaluates. So a note has no expiry, no owner, and no way to go red." Every word
  of that applies to the contract sentence, with one aggravation the entry does not
  cover: a note is read by one person once, and the contract is read by everyone
  always.
- `docs/residual-findings.md:7133`, R-115: a third instance of the same family, from
  a different direction. Ten consecutive CI runs on `main` were red while the local
  battery was clean, and its measured cost is stated as "a signal exists, is
  consulted by nobody, and cannot change state". A red that is red when the tree
  is perfect distinguishes nothing, exactly as a contract that is believed whether
  or not it is true distinguishes nothing. R-115 also notes that its version is
  harder to see because the useless signal sits OUTSIDE the battery. So does this
  one. R-115 originally attributed every red run to the workflow running Linux
  against a macOS product, and that attribution was itself a claim carried without
  measurement: on 2026-08-15 it was driven and five of the failures reproduced on
  macOS from a shallow checkout. The entry is closed, CI no longer runs the suite,
  and `a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it.md` carries
  the correction.
- `docs/METHOD.md:229` through `:245`, the append only rule for residual numbers and
  the sweep that certified the last renumber against `src`, `tests` and `scripts`
  while missing GitHub issue titles. That missed surface is precisely what
  `repointed_residuals()` now watches, and the passage names the defect class:
  "a rule verified against source while a second surface carries the same coupling."
- `docs/METHOD.md:185`, the battery definition, three commands and nothing else.
- Commit `e0387d9` on `main`: the fix, both halves, with the driven results in its
  body. Commit `9cdc42e` on `main`: `RESTART-cratekit.md` follows, replacing a prose
  next steps list with board numbers and recording the build versus ledger split as
  a standing decision (`RESTART-cratekit.md:74`) so a later session does not
  rediscover the backfill question.
- `scripts/board.py:439`, `contradictions()`: the existing argument this guard was
  filed under. Drift is a derived value `sync` repairs; a contradiction is two
  sources of truth disagreeing, and automatic repair "would mean picking one to
  overwrite, which is how the wrong one wins silently."
