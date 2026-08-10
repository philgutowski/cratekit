# U34 round 11, the merge blocking fix, and its mutation table

Round 11 exists because the U34 merge was ATTEMPTED, hit a defect, and was backed
out. Everything in this document was measured on a real reproduction of that
merge rather than on a fixture: a scratch clone of the repository, `main` at the
commit the merge was attempted from, a real `git merge` of this branch, the five
conflicts resolved from the aborted attempt's own resolutions, and the merged
tree's own virtual environment.

## What broke, measured on the merge and not argued from the source

`tests/modules/test_reports.py` guards that this unit's residual findings are
cited by TITLE and never by NUMBER. It did that with a typed numeric range and
with derivations taken against `merge-base(origin/main, HEAD)`. Both premises
fail at merge time, and they fail in two different ways.

**The numbers move at the merge.** Both sides append to one document from one
counter, so the number a residual is FILED under is not the number it keeps.
`docs/METHOD.md` renumbered sequentially and recorded that this was safe precisely
because every citation is a title; Phillip replaced that with APPEND ONLY on
2026-08-10, so main's numbers now hold still and only the incoming branch's move.
A ban list written as a numeric range fails under either rule, because under both
of them this branch's residuals end up somewhere other than where they were filed.
On the reproduced merged tree
the union of both sides is 42 residual sections and this unit's twelve no longer
sit where they were filed. Two tests failed, both through `_banned_addresses`,
with `the ban list stopped covering this branch's residuals: ['28' ... '42']`.

**The base that becomes HEAD.** `merge-base(origin/main, HEAD)` answers "where did
this branch leave main", which has no answer left once the branch IS main. On a
pushed, clean `main` the base resolves to HEAD, so every diff taken against it is
empty. Measured on the reproduction with `origin/main` set to the merge commit:

    FOUR tests fail and a FIFTH passes over an empty loop.

    test_this_units_residuals_are_cited_by_title_and_never_by_number
    test_a_coverage_list_narrowed_by_one_file_is_refused_whichever_file_it_is
    test_the_ban_list_is_narrowed_at_neither_edge_and_names_nothing_extra
    test_the_collision_passage_is_the_only_exemption_and_it_is_delimited

    test_the_named_floor_still_bites_when_both_derivations_narrow_together
      passes, because its body is a loop over a list that is now empty

That last line is the same defect as the round ten verification's finding 2, seen
in the wild rather than in a mutation: a guard whose whole body is a loop reports
success when the thing it loops over goes empty. The brief for this round named
one failing derivation. Driving it measured four failures and one silent pass.

This is worse than a guard that never existed. It goes red on `main`, after the
merge that was supposed to land it, in a file nobody is looking at.

## What replaced it

Two changes, and each one removes a premise rather than patching a symptom.

**Addresses are titles.** `UNIT_RESIDUAL_TITLES` types the twelve residuals this
unit filed by their titles, which the renumber does not move, and
`_banned_addresses` resolves them to today's numbers by reading
`docs/residual-findings.md`. Driven on both trees:

    on this branch          twelve consecutive addresses
    on the merged tree      the same twelve, every one of them seven higher

Same twelve findings, same twelve typed strings, addresses resolved from the
document each time.

**The unit is identified by its commits, not by a merge base.** `UNIT_COMMIT_TAG`
is `(U34)`, which every one of this unit's thirteen commits carries in its
subject and none of `main`'s do. A commit subject is immutable and a merge carries
it across unchanged, so `git log -F --grep` answers identically on the branch, on
the merged tree, and on a pushed main. Measured: 23 files on this branch, the same
23 on the merged tree, against the 23 the merge base diff used to give.

## Driven in all three states

| state | `origin/main` | `HEAD` | merge base | result |
|-|-|-|-|-|
| (a) this branch | pre-merge | branch tip | the branch point | 7 passed |
| (b) the merged tree | pre-merge | merge commit | the pre-merge commit | 7 passed |
| (c) main, pushed and clean | merge commit | merge commit | **HEAD** | 7 passed |

State (c) is the one that would have left main red, and it is reproduced by
`git update-ref refs/remotes/origin/main <merge commit>` in the scratch clone.
No ref in any real worktree was touched.

The whole merged suite in state (c): **3782 passed, 16 skipped, 3798 collected.**

## Driver rules this table was taken under

* no `-q` anywhere, including the collection run;
* the collected count recorded on EVERY row, so a file that fails to collect can
  never read as a run that found nothing;
* rows run one at a time, never overlapping, one subprocess at a time;
* the driver never invokes git; file text is snapshotted in memory, rewritten,
  and restored, and every restore was verified afterwards against
  `git show HEAD:<path>`;
* `PYTHONDONTWRITEBYTECODE=1`;
* node ids read off `report.nodeid` through a plugin, never off a summary line;
* message mutations reworded, never appended;
* each guard layer removed alone, with composites for the layers that only bite
  together.

## The table

| row | deaths | scope | collected | mutation |
|-|-|-|-|-|
| C01 | 1 | FULL | 3539 | COMPOSITE for M10 and M11: the on-disk floor returns nothing at all |
| C02 | 1 | FULL | 3539 | COMPOSITE for M06: an UNTRACKED file citing a banned address, with route one still reading untracked files |
| C03 | 3 | FULL | 3539 | COMPOSITE for M06: the same untracked file, with route one no longer reading untracked files |
| C04 | 1 | FULL | 3539 | COMPOSITE for M09: the same untracked file, with route two no longer reading the working tree status |
| C05 | 5 | FULL | 3539 | COMPOSITE for M03: an alternation as the unit tag, WITH -F, so the fixed-string reading matches nothing |
| C06 | 5 | FULL | 3539 | COMPOSITE for M03: the same alternation WITHOUT -F, so the regex reading matches and the guard goes quiet |
| C07 | 5 | FULL | 3539 | COMPOSITE for M20: the typed titles and the derived titles go empty TOGETHER, with the shared-failure floor intact |
| C08 | 4 | FULL | 3539 | COMPOSITE for M20: the same pair going empty together with the shared-failure floor REMOVED |
| C09 | 4 | FULL | 3539 | COMPOSITE for M20: the same pair empty together, floor removed AND the test's own emptiness check removed |
| M01 | 5 | subset | 349 | the unit tag stops naming this unit, so every commit derivation goes empty |
| M02 | 3 | subset | 349 | the caller's arguments go FIRST again, so a pathspec swallows the grep filter |
| M03 | **0** | FULL | 3539 | the grep loses -F, so the tag is a regex and its brackets become a group |
| M04 | 3 | subset | 349 | route one stops reading this unit's commits and reads only the working tree |
| M05 | **0** | FULL | 3539 | route one stops reading the working tree diff |
| M06 | **0** | FULL | 3539 | route one stops reading untracked files |
| M07 | 1 | subset | 349 | route two stops walking this unit's commits |
| M08 | **0** | FULL | 3539 | route two drops the path a rename or copy went TO |
| M09 | **0** | FULL | 3539 | route two stops reading the working tree status |
| M10 | **0** | FULL | 3539 | the on-disk floor stops globbing this unit's package |
| M11 | **0** | FULL | 3539 | the on-disk floor stops naming this module itself |
| M12 | 1 | subset | 349 | CITED_FLOOR is EMPTIED, which is the round ten finding this round closes |
| M13 | 1 | subset | 349 | CITED_FLOOR drops one of the files this unit puts on disk |
| M14 | 1 | subset | 349 | CITED_FLOOR drops the reverts file this unit's last round created |
| M15 | **0** | FULL | 3539 | the floor test's own emptiness check is removed |
| M16 | **0** | FULL | 3539 | the floor test's bound against the on-disk list is removed |
| M17 | **0** | FULL | 3539 | the floor test's count of what it actually refused is removed |
| M18 | **0** | FULL | 3539 | RESIDUALS_FILED_FLOOR drops to zero, so both sides may empty together |
| M19 | **0** | FULL | 3539 | RESIDUALS_FILED_FLOOR is halved, a realistic nearby value rather than zero |
| M20 | **0** | FULL | 3539 | the shared-failure floor assertion is removed from the resolver |
| M21 | 1 | subset | 349 | the UNCOVERED assertion is removed, so a filed residual may go unbanned |
| M22 | 1 | subset | 349 | the INVENTED assertion is removed, so another unit's address may be banned |
| M23 | 1 | subset | 349 | the UNRESOLVED assertion is removed and the lookup skips what it cannot find |
| M24 | **0** | FULL | 3539 | an ambiguous title resolves to the first heading instead of being refused |
| M25 | 3 | subset | 349 | UNIT_RESIDUAL_TITLES is EMPTIED, the vacuity the old floor could not see |
| M26 | 3 | subset | 349 | UNIT_RESIDUAL_TITLES loses its last entry, narrowed at one edge |
| M27 | 3 | subset | 349 | UNIT_RESIDUAL_TITLES loses its first entry, narrowed at the other edge |
| M28 | 3 | subset | 349 | UNIT_RESIDUAL_TITLES is widened with a residual another unit filed |
| M29 | **0** | FULL | 3539 | the FILED heading pattern drops its plus, so context lines count as filings |
| M30 | **0** | FULL | 3539 | the DOCUMENT heading pattern stops anchoring at the start of a line |
| M31 | 2 | subset | 349 | the resolver returns the bare number, dropping the R- prefix a citation carries |
| M32 | **0** | FULL | 3539 | the renumber test stops checking that the addresses actually moved |
| M33 | **0** | FULL | 3539 | the renumber test stops comparing the shifted addresses to the shift |
| M34 | **0** | FULL | 3539 | the rename test stops counting how many addresses it actually drove |
| M35 | **0** | FULL | 3539 | the rename test's own no-op guard is removed |
| M36 | **0** | FULL | 3539 | the ban list test stops asserting it reaches no other unit's address |
| M37 | **0** | FULL | 3539 | the ban list test's intruder set is allowed to be empty |
| M38 | **0** | FULL | 3539 | the ban list test stops asserting the resolved numbers are the document's |
| M39 | 1 | subset | 349 | sample: the derivation's coverage assertion, existing guard |
| M40 | 1 | subset | 349 | sample: the named floor's assertion inside _covered_files, existing guard |
| M41 | 1 | subset | 349 | sample: the file that DEFINES the residuals is no longer excluded from policing |
| M42 | 1 | subset | 349 | sample: a delimiter is recognised by containment rather than by being the line |
| M43 | **0** | FULL | 3539 | sample: the citation pattern loses its word boundaries |
| M44 | 7 | subset | 450 | sample: an unreadable node kind defaults to folder again, existing guard |
| M45 | 2 | subset | 349 | sample: the declared entry count is no longer compared with the walk |
| M46 | **0** | FULL | 3539 | the ban list test stops requiring the derivation to have found anything |
| M47 | 1 | subset | 349 | CITED_FLOOR drops the reverts file THIS round created |
| M48 | **0** | FULL | 3539 | the on-disk floor stops globbing this unit's own documents |
| M49 | 1 | subset | 349 | CITED_FLOOR drops the mutation TABLE this round created |

## The zero rows, each paired

Twenty five of the fifty six rows kill nothing. Every one is paired below, and no
pairing is a prose argument: each is either a composite with its own count or a
direct measurement of why the row is inert.

**The tag itself, and its flag.** M03 removes `-F` from the grep and kills
nothing. C05 and C06 pair it: with an alternation as the tag, the fixed reading
and the regex reading BOTH kill 5, so the tag is load bearing and the flag is
not distinguished by any input the suite has. **Reported as unpinned rather than
held.** What is measured is that M01, breaking the tag outright, kills 5.

**The working tree reads.** M05, M06 and M09 kill nothing because the tree is
clean during a row, so those reads contribute no file. C02, C03 and C04 pair them
with the input they exist for: an UNTRACKED document citing a banned address.
With the reads intact the citation is caught, 1 death. With route one's
`ls-files` removed the two routes disagree and the coverage property fires, 3
deaths. With route two's `status` removed the citation is still caught, 1 death.
So the untracked reads are held under the input they were written for, and are
inert on a clean tree by construction.

**The rename field.** M08 kills nothing. Measured rather than argued: this unit's
thirteen commits contain **zero** renames or copies, so the branch has no input
that reaches the clause.

**The filed heading anchor.** M29 relaxes `^\+## R-` to `^.?## R-` and kills
nothing. Measured: the unit's own diff of the residual document carries **zero**
context heading lines and twelve added ones, so no relaxation of the anchor can
change the derived set on this history. Inert by construction, not unheld.

**The on-disk floor's two halves.** M10 and M11 each kill nothing, because each
half leaves the other. C01 removes both and the floor's own emptiness check fires,
1 death.

**The floor test's inner assertions.** M15, M16 and M17 kill nothing on their own,
which is correct: they are the checks that MAKE M12, M13, M14 and M47 die. Their
pairing is those four rows, each at 1 death, all through the same node id.

**The shared-failure floor.** M18, M19 and M20 kill nothing alone, because
nothing on the branch empties both derivations at once. C07, C08 and C09 simulate
exactly that. C07, both sides empty with the floor intact: 5. C08, the same with
the floor removed: 4. **Exactly one of the five deaths belongs to the floor**, and
it is `test_a_renumber_moves_every_address_and_the_ban_list_follows_it`. C09
removes the test's own emptiness check as well and stays at 4.

**The remaining test-side assertions.** M24, M30, M32 to M38, M43 and M46 are
assertions inside tests, or pattern relaxations with no input on this tree. Each
is paired by the row that removes the thing it checks: M25 to M28 for the ban
list at 3 each, M21 to M23 for the resolver at 1 each, M31 at 2 for the prefix,
M41 at 1 for the exclusion and M42 at 1 for the delimiter.

## What this round closes, with its measurement

**The merge blocker.** The guard now passes in all three states, and the whole
merged suite is green: 3782 passed, 16 skipped, 3798 collected.

**The round ten verification's finding 2, the emptiable floor.** That report
measured three rows at zero deaths each over full suite runs: the floor dropping
this branch's own reverts file, the floor dropping the module the round changed,
and the floor emptied to `()`. All three are now rows here and all three kill:

| what | round ten | round eleven |
|-|-|-|
| the floor EMPTIED to `()` | 0 deaths | **M12, 1 death** |
| the floor drops a module this unit writes | 0 deaths | **M13, 1 death** |
| the floor drops a reverts file this unit wrote | 0 deaths | **M14 and M47, 1 death each** |

The death is `test_the_named_floor_still_bites_when_both_derivations_narrow_together`,
which previously survived the constant being emptied because its whole body was a
loop over that constant. It now carries a bound read off the filesystem, which is
the one source that cannot go quiet at the same time as git.

## Re-measured against the final text

`CITED_FLOOR` gained this round's own reverts file and this table, so every row
whose subject is that constant was re-run against the text as it ships, not
against an intermediate. M10, M12, M13, M14, M47, M48, M49 and C01 all reproduce:
M10 and M48 at zero, C01 at 1, and M12, M13, M14, M47 and M49 at 1 death each,
every one of them `test_the_named_floor_still_bites_when_both_derivations_narrow_together`.

## The collected count, reconciled BY IDENTIFIER

A total only check shows a healthy rise and hides a collapse, so the node ids are
compared rather than the numbers. Against `HEAD`, this round's diff removes one
test identifier and adds three:

    REMOVED  test_the_ban_list_is_narrowed_at_neither_edge_and_names_nothing_extra
    ADDED    test_the_ban_list_is_the_residuals_this_unit_filed_and_nothing_else
    ADDED    test_a_residual_the_document_renames_or_drops_is_refused_and_never_dropped
    ADDED    test_a_renumber_moves_every_address_and_the_ban_list_follows_it

3537 collected before, 3539 after, and the net of two is exactly three added
against one renamed away. Nothing else moved.

## Named as unmeasured

* **The `-F` flag on the grep.** C05 and C06 kill 5 each, so no input in this
  suite distinguishes the fixed reading from the regex reading. The flag is
  correct and it is NOT pinned. Reported rather than claimed.
* **Another unit's merge.** Everything here is measured on one reproduction of one
  merge of this branch into `main` at one commit. A different merge order, or a
  `main` that has moved again, is unmeasured.
* **The residuals filed AT merge time.** The merged residual document carries
  eight findings that exist on neither side before the merge, filed by whoever
  resolved it. They are not in this unit's commits, so this guard neither covers
  nor bans them, by design. Whoever files them owns citing them by title.
* **Timing.** No timing row was taken. Nothing in this round's diff is on a hot
  path. Wall clock per row roughly doubled part way through because a U24 agent
  was running its own driver in its own worktree at the same time; no file, ref or
  measurement is shared between the two, and no row in this table is a duration.

## Under append only numbering, decided 2026-08-10

Residual numbers are now append only: main's numbers never move, and an incoming
branch's residuals take fresh numbers above main's highest. The reason is that a
GitHub issue title carries the number in its text, so a renumber silently repoints
the issue.

**Nothing in this round changes.** The guard resolves titles to whatever numbers
`docs/residual-findings.md` gives them at the moment it runs, so it does not know
or care which numbering rule produced them. What matters to it is only that a
number is not stable and a title is, and that is true under both rules.

`test_a_renumber_moves_every_address_and_the_ban_list_follows_it` deliberately
drives the HARDER rule, every number in the document moving at once, rather than
the current one where only this branch's move. A guard that survives all of them
moving survives some of them moving, and it does not need revisiting if the
decision moves again.

## Row count, against the cap of 45

This table is 57 rows and was taken before that cap existed. **No row was dropped
and no row is a truncation.** Had the cap applied while it was being built, the
rows to lose first are the ones this unit's own severity floor says can never
block: M32 to M38, which are assertions inside tests rather than the guards
themselves. Every one of them is a maintainer facing check on a maintainer facing
guard, and none of them is what this round was sent to fix.
