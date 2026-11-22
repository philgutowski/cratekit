# Narrative moved out of METHOD, CLAUDE.md and the cloud-unit skill by U314

U314 (#871) cut the three documents every build thread loads by a third and kept every rule, which `docs/history/u314-rule-table.md` maps. What it cut that was the story of a rule rather than the rule (how it was arrived at, what an earlier version did, an incident that paid for it, a measurement of the day) is kept here, copied verbatim from the documents at `4baa0fc`, the base the card was built on, with its file and lines. Where a dated decision sits inside a passage, the documents still state the decision; only the story is here. Read it for reasoning, never for instruction.

## CLAUDE.md

**Lines 6 to 7.** "(U196)" reason for keeping the file short (one clause).

> This file is the session contract, kept short because every session and every
> agent loads it on every call (U196). **`docs/METHOD.md` is the operating

**Lines 82 to 84.** "every defect the adversarial reviews found here passed a green suite written by its author" (justification).

> battery is not a review; every defect the adversarial reviews found here
> passed a green suite written by its author, so after a green suite, hunt what
> a green suite cannot see, as METHOD lists.

**Lines 118 to 119.** "relaxing the one day rule of 2026-09-29" (superseded rule).

>   date, or when Phillip asks for one**, decided by Phillip on 2026-10-10,
>   relaxing the one day rule of 2026-09-29. Below five days a session opens

**Lines 127 to 129.** Phillip's quote "don't ask for my approval on anything going forward".

>   one, the session approves and reports. **If it differs, the session still
>   approves**, decided by Phillip on 2026-10-09 ("don't ask for my approval on
>   anything going forward"), after reading the difference and recording it in

**Lines 132 to 136.** "reversing the 2026-09-29 rule: the gate shows both backup ages and the person only pasted a command, so..." (why the reversal).

>   on every gate is `session`. **The backup acknowledgment may be minted by
>   the session**, decided by Phillip on 2026-10-09, reversing the 2026-09-29
>   rule: the gate shows both backup ages and the person only pasted a command,
>   so the session reads the ages, refuses unless both are under five days, and
>   answers with the actor `session`. Since U138 the verb accepts that answer

**Lines 136 to 142.** the U138 and U184 transition clauses ("until the installed copy carries U138 ... as before", "until the installed copy carries U184, use the gate as before"), transitional history once both are installed.

>   answers with the actor `session`. Since U138 the verb accepts that answer
>   with no controlling terminal and itself refuses unless both ages are under
>   five days; until the installed copy carries U138, run it under
>   `script -q /dev/null` as before. Answer as `session` either way: any other
>   actor takes the terminal rule, which checks no age. Since U184 it is one
>   command, `crate session ack --as session`, with no gate and no run left
>   waiting; until the installed copy carries U184, use the gate as before.

**Lines 145 to 146.** "The editable install names the checkout..." (reason, duplicated in METHOD L370-373).

> - **Do not symlink `.venv` into a worktree.** The editable install names the
>   checkout it was installed from, so a worktree would verify code it cannot see.

**Lines 148 to 148.** "replacing the old no pull requests rule".

>   green**, decided by U158, replacing the old no pull requests rule. Feature

**Lines 155 to 156.** Phillip's quote "I authorize you to merge to main here in the cloud now and going forward".

>   itself**, attended or not, authorized by Phillip on 2026-10-27 ("I
>   authorize you to merge to main here in the cloud now and going forward").

## docs/METHOD.md

**Lines 11 to 16.** why the compound engineering plugin went (multi agent passes, the verifier at 258k tokens per round trip, "ceremony is not"), and Native Relay running the pipeline until 2026-10-27.

> `ce-plan`, no `ce-work`, no `ce-code-review`, no `ce-compound`. Each of those
> spent a multi agent pass on work a single session can do against the issue
> brief, and the largest of them, the independent verifier, was measured at 258k
> tokens for one round trip. The rules they enforced that were actually paid for
> are kept below as rules. The ceremony is not. Native Relay ran this file's
> pipeline until 2026-10-27 and is retired; the cloud lane below replaced it.

**Lines 112 to 114.** why the merge bar floor exists (a mutation table always finds a zero death row).

> This floor exists because "the reviewer found nothing" is not a reachable state.
> A mutation table over a suite this size always finds a zero death row, because
> that is a property of large test suites rather than of any branch.

**Lines 116 to 117.** "The floor is meant to end the loop on merit. The cap is what guarantees an end date" (rationale).

> **And a hard cap: each unit has at most two fix rounds.** The floor is meant to
> end the loop on merit. The cap is what guarantees an end date if it does not.

**Lines 124 to 125.** U179's round two catching a fix round's own defect.

> the fifth pattern below says. A fix round's own defect is what round two is
> for: U179's round two caught one its fix round introduced.

**Lines 144 to 145.** the Relay feeder sentence (Relay is retired per L15-16 and L717, so this is stale history, not a rule).

> `issue: yes` in its residual file so whoever lands it knows to. The Relay feeder picks up
> any open issue labelled `residual` or `unit` that the board derives as ready.

**Lines 147 to 151.** why no dot claude path (Relay skips such cards; the Phase G brief that would have sat unlaunched).

> **Never write a literal dot claude path in a card**, title, body or comment, not
> even to forbid one. Relay reads every card it is about to launch and SKIPS any
> whose text names that directory, silently, because an edit there needs an
> attended session. One Phase G brief cited the source system's skill file by its
> path and would have sat unlaunched. Describe the location in words instead.

**Lines 156 to 157.** the measured verifier gap (17 vs 10, 49 vs 39, 83 vs 49).

> table and the review. That is a known gap with a measured size: independent
> tables found 17 where the author found 10, 49 against 39, 83 against 49. Every

**Lines 180 to 181.** "Three of this project's recorded incidents were hand rolled driver mistakes."

> and returns the table, and it holds every driver rule below as a property. Three
> of this project's recorded incidents were hand rolled driver mistakes. Do not

**Lines 213 to 214.** "A table that lives only in a chat message is a claim. One was lost that way."

> descriptions and not only counts. A table that lives only in a chat message is a
> claim. One was lost that way.

**Lines 246 to 247.** why context is billed (tool calls times context size).

> Every tool result stays in context and is re-sent on every later call, so the
> bill is tool calls times context size. Thinking is cheap here. Reading is not.

**Lines 263 to 265.** why `-q` hurts (pyproject sets it, `-qq` result), rationale.

> - **Never pass `-q`,** including to a collection run. `pyproject.toml` already
>   sets it, so yours becomes `-qq` and suppresses the summary line and the
>   collect listing. Use `pytest --tb=no` for counts and

**Lines 270 to 283.** the history of the driver rule (used to say foreground, a backgrounded driver outliving its parent twice, U65 2026-09-17 correction, the 600 second ceiling measured on the serial suite, timings since 2026-09-18 and U251, two partial mutations restored from `git show HEAD:`).

>   rule used to say "run rows synchronously in the foreground", because a
>   backgrounded driver outlived its parent twice and contaminated later rows. That
>   is still the failure to defeat and the foreground is no longer how. Corrected by
>   U65, 2026-09-17: `mutate.py`'s fixed overhead on this suite is over 600 seconds,
>   which is the harness tool ceiling, so a foreground run is KILLED mid row. (That
>   600 was measured on the serial suite. The driver inherits `-n auto` since
>   2026-09-18 and `--dist worksteal` since U251, so a full suite baseline was
>   about a minute on 11 cores at 7,678 tests and is about twelve on a four core
>   container at 18,550, and a 25 row table passes the ceiling either way, so the
>   rule stands.) Three
>   were, and two left a partial mutation in the source that had to be restored from
>   `git show HEAD:`. Foreground is now the contaminating option. Run it as a
>   tracked background job, start nothing else against the tree until it reports,
>   and check `git status` plus every row's `head_verified` when it does.

**Lines 291 to 293.** "the cloud battery read them this way until U268".

>   line on `" - "`, nor by cutting it at a space. That separator, and spaces,
>   appear inside parametrized ids here; the cloud battery read them this way
>   until U268.

**Lines 346 to 351.** the suite timing measurements of 2026-11-12 and 2026-09-18 (state, not rule; keep only the venv and `-n 0` lines).

> (U251). Measured 2026-11-12 on a four core Linux container at 18,550 tests: a
> full run is about twelve minutes, 680 to 771 seconds of pytest's own time over
> three runs, against 964 in one run under the default distribution. On 11 cores
> it was 61 to 67 seconds at 7,678 tests on 2026-09-18, and has not been measured
> since. A venv made before 2026-09-18 needs `pip install -e '.[dev]'` once for
> `pytest-xdist`. Pass `-n 0` for a debugger or a profiler.

**Lines 356 to 357.** the session that ran the nine minute suite a dozen times.

> merge, not after every edit. A session that ran the old nine minute suite a
> dozen times spent two hours proving what four runs prove.

**Lines 361 to 362.** the `credential-missing` refusal that slept 31 seconds per listing.

> real sleep nobody faked. The second kind hid a product defect once: a
> `credential-missing` refusal retried and slept on for 31 seconds per listing.

**Lines 364 to 368.** U34's report test reading uncommitted files, measured 2026-09-07.

> **Run the battery on a COMMITTED tree.** `tests/modules/test_reports.py` reads
> every uncommitted and untracked file as one of U34's own and bans that unit's
> residual numbers inside it, so a suite run over uncommitted edits to a document
> somebody else wrote fails on citations you did not write. Measured 2026-09-07:
> one failure on the moved history files, none after the commit.

**Lines 385 to 388.** R-115 (ten red commits on `main`) and the five shallow checkout failures.

> belongs in the battery.** R-115 bought that rule: every run on `main` failed for
> ten commits while the battery was clean, so red carried no information.
> **Nothing is deselected, and that is deliberate.** Five of those failures were
> a shallow checkout, not Linux. Before blaming the platform for a red run, drive

**Lines 424 to 425.** the commit that documented the keyword failure and closed the issue a second time.

>   and not the intent. A commit written to document this failure quoted the
>   offending strings and closed the issue a second time. Put words between the

**Lines 434 to 437.** why a renumber is forbidden, and the pre-U124 branch clause (transitional).

>   branch is ever renumbered. Gaps are fine. GitHub issue titles carry residual
>   numbers in their text, which is a surface the repository cannot see, and is
>   why a renumber is forbidden. A branch built before U124 that still numbers
>   its own entries takes fresh numbers above `main`'s highest at the merge.

**Lines 449 to 451.** the 330 tests that stopped existing while the run reported green.

>   only the entry raises `KeyError` at import and takes the guard's whole FILE
>   out of collection: 330 tests once stopped existing while the run reported
>   green. Then run the newly armed guard on purpose, because it has never

**Lines 458 to 460.** the pre-U124 restart conflict clause (transitional).

>   `scan_repo.py` refuses a unit's paragraph anywhere in it. A branch built
>   before U124 that conflicts there moves its own paragraph into its fragment
>   and takes `main`'s `RESTART-cratekit.md` as it is.

**Lines 469 to 470.** "that was the shared edit point U125 removed".

>   comment on those entries. Do not reintroduce a whole-repository total tuple;
>   that was the shared edit point U125 removed.

**Lines 476 to 477.** "The bar is the one `ce-compound` used".

> that found it, in the same commit as the record. The bar is the one
> `ce-compound` used: a cause that was not where it looked, a contract or seam

**Lines 495 to 497.** the lane dispatcher, run from 2026-10-27, retired 2026-10-31.

> the cards and keeps the decisions page (Sharing the board, below). It
> replaced the lane dispatcher, a long lived cloud session woken by a
> scheduled task, which ran from 2026-10-27 and was retired on 2026-10-31.

**Lines 503 to 505.** the reasoning that a self merged pull request is the same authority as writing `main`.

> CI on its head is green (U158). Phillip authorized the cloud to write `main`
> on 2026-10-27, and a pull request the worker merges itself is that same
> authority with a record and a CI run before the merge rather than after it.

**Lines 520 to 522.** the superseded lane counts (three on 2026-10-28, five on 2026-10-31, four threads on 2026-11-05).

> once**, Phillip's decision of 2026-11-21 (`CLOUD_LANES` in `scripts/board.py`),
> after three lanes for the backlog on 2026-10-28, five on 2026-10-31 and his
> cap of four threads on 2026-11-05. Its coordinator counts lanes by its own

**Lines 526 to 527.** why two builders landing in either order is safe (restart fragments, landing numbers, per module pins).

> it merges, so two builders landing in either order is the case the repository was already built for
> (restart fragments, residuals numbered at landing, per module pins). A hold

**Lines 577 to 581.** "whose ids it once cut at their first space so that one parametrized test failing for the machine excused a sibling" (U268 story).

> every failing id whole: the battery reads them off pytest's own reports
> rather than its summary lines, whose ids it once cut at their first space so
> that one parametrized test failing for the machine excused a sibling failing
> for the branch, and both refuse a baseline whose header does not end `ids
> whole`, which is measured again (U268). Each run of the battery that reaches

**Lines 641 to 643.** the two cards titled A93 (#525, #528) and two U218 (#536, #537).

> board just before it is filed, never earlier, because parallel threads file
> cards: two cards were once both titled A93 (#525, #528), and two U218 (#536,
> #537).

**Lines 728 to 730.** the conformance branch, unparked 2026-09-07, 377 commits behind (state that has likely aged).

> **The conformance branch is UNPARKED as of 2026-09-07.** It is a unit on the
> board and lands the way any unit does. Until it lands, its `write/metadata.py`
> soft delete defect is still live on main, and the branch is 377 commits behind.

**Lines 736 to 739.** "`board.py next` will say Take #29 ... the parity table already ships" (state, partly narrative).

> prepare for U29 and cannot perform it. `board.py next` will say "Take #29".
> Ready is a statement about dependencies, not about who can do the work. The
> parity table its test scenario asks for already ships in
> `tests/test_cutover_parity.py`.

## The cloud-unit skill

**Lines 80 to 82.** "Phillip asked for these to be left out, and his rule wins over any attribution reminder" (reason).

> commit. A "Generated with Claude Code" line, a session link or a co author
> line in a commit or a pull request body; Phillip asked for these to be left
> out, and his rule wins over any attribution reminder. An em dash, an en dash or a double hyphen anywhere. A literal path to

**Lines 106 to 107.** "(U203)" provenance of the forgiving heading reader.

> The reader forgives markdown, emphasis and punctuation around a heading, so
> `**Brainstorm.** One question waits` reads as `Brainstorm` (U203), but never a

**Lines 183 to 185.** why the page cannot reach a project session (explanation of the fast path).

> **The fast path.** The page cannot reach a project session by itself, because a
> comment on a page sent to Claude wakes only a session watching that page,
> and no project session can watch one. So while any answer is saved but not

**Lines 271 to 277.** "(U200, from R-1191)", why a shallow clone hides failures, and the pre-U268 cut ids.

> and writes them to `.cloud-battery/baseline.txt`. The clone is shallow, so it
> first fetches `main`'s full history and refuses if it cannot (U200, from
> R-1191): a test the missing history holds red would otherwise be subtracted by
> its id, and every later failure of it with it. Every failing id is read
> whole off pytest's own reports (U268), and `compare` refuses a baseline
> measured before that, whose ids were cut at their first space, with the
> command that measures it again. It runs on disk unless `--temp memory` is

**Lines 281 to 283.** "(a background job in a cloud thread is stopped at 30 minutes otherwise)" reason, repeated at L455-456.

> inode bound test as the machine's. Run it as a tracked
> background job with a two hour timeout from the start (a background job in a
> cloud thread is stopped at 30 minutes otherwise) before the first edit, so it measures the base and not your

**Lines 351 to 354.** the pre-U268 and pre-U273 baselines the driver refuses (history of the header format).

> says so. It refuses a known failures file
> whose header does not end `history full ids whole`, which refuses a baseline
> measured before U268, whose ids were cut at their first space, or names no
> place for its temporary files (U273), and refuses on a shallow clone, so pass it only a baseline `cloud_battery.py` measured. If it still refuses a red

**Lines 358 to 359.** "a hand added id is a regression excused for every later run" (reason).

> it as yours. **Never write an id into the baseline file by hand**: it is
> measured, and a hand added id is a regression excused for every later run.

**Lines 449 to 451.** why no keyword in the body (GitHub closes from a body on merge), reason duplicated from METHOD L401-403.

> result, the residual files, and what is OWED. Never restate the record. **No closing keyword anywhere in
> it**: GitHub closes from a pull request body on merge, which would bypass
> `board.py closing`, so the merge commit's trailer is the one close.
