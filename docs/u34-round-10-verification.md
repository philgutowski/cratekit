# U34 round 10, independent verification

Verifier: an agent that did not write this code. Branch
`unit/u34-read-only-library-reports` at `1a7cdf7`, worktree `.worktrees/u34`,
that worktree's own `.venv`. Light pass per `docs/METHOD.md`, which assigns U34 a
light pass because it is a read only report surface. A light pass still derives
its own table and is scoped rather than trusting.

The independent mutation table is
`docs/mutation/u34-round-10-verification-table.md`. Fifty distinct rows plus four
untracked composites, against the author's thirty. Eleven zero rows against his
four.

## VERDICT

**BLOCKING**, on one finding. Everything else is a residual.

Finding 1 below is driven end to end through the live `read_export`,
`intake_aging` and `duplicates.audit` on the reports suite's own export fixture,
and it has two of the four user facing costs the merge bar names by hand: a
person is told something false, and a person is shown a clean report over state
the tool could not read.

Findings 2 through 8 are residuals. None of them costs a user anything: they are
a typed constant that can be emptied in silence, three assertions that name less
than they claim, and a documented count an independent table does not reproduce.

The verdict is one finding wide, not a rejection of the round. The round's own
structural claim HELD under direct attack, and its four blocking answers all
reproduce. See "What held" at the end.

## Finding 1. An extra node close is accepted, and both reports render over a tree that was re-parented under them

**BLOCKING.** Both floor conditions are met and each is addressed below.

**What was driven.** The reports suite's own `library_export()` fixture, with ONE
`</NODE>` inserted after the first intake grouping's close. Nothing else changed.
Every node in the document still declares a `Type` this build reads, so round
ten's new refusal is not what is being dodged; the classification is doing exactly
what it now says it does.

`rbxml.matching_close` counts depth forwards from a node's open tag, so an extra
close makes a folder's own close land early. Everything after the stray close
falls outside `INBOX`'s span and is re-attached to the root by `child_nodes`.

**The declared counts the document itself carries, measured on both:**

    BASELINE                            declares  holds
      ROOT                                  2       2
      INBOX                                 5       5
      INBOX / Old                           1       1

    ONE STRAY </NODE>                   declares  holds
      ROOT                                  2       6     DISAGREES
      INBOX                                 5       1     DISAGREES
      Old                                   1       1

**The verdict `read_export` returns on that document: ACCEPTED.** It builds a
`LibraryView` and hands it to both reports.

**Cost one, a person is told something false.** The intake aging report:

    baseline    5 groupings: 3 expired, 1 current, 1 undated
    strayed     1 grouping:  1 expired

Four intake groupings, two of them expired, are gone from the report. The intake
folder itself survives the walk, so `view.has_folder` is satisfied and
`intake_groupings` does not refuse. The person is shown a queue holding one list
over a library holding five, with no indication that anything was not read. This
is the same shape as the defect the round fixed, one structure over.

**Cost two, the duplicate audit invents placements.** The one duplicate group's
member placements:

    baseline    ['BY GENRE + ENERGY / Deep House / High',
                 'INBOX / phil_07_01_2026',
                 'INBOX / Old / phil_5_01_25']
                ['BY GENRE + ENERGY / Melodic House / Med',
                 'INBOX / 2026-06-15 bandcamp']

    strayed     ['BY GENRE + ENERGY / Deep House / High',
                 'INBOX / phil_07_01_2026',
                 'Old / phil_5_01_25']
                ['BY GENRE + ENERGY / Melodic House / Med',
                 '2026-06-15 bandcamp']

`Old / phil_5_01_25` and `2026-06-15 bandcamp` are locations that do not exist in
this library. The duplicate audit's whole job is to let a person decide which copy
survives, and it is naming a place to go and look that is not there. The audit
feeds `review.Queue.DUPLICATES`, whose ACCEPTED verdict licenses a deletion
surface, which is the escalation the module's own docstring calls out.

**How wide the hole is, measured across six spellings:**

| document | verdict |
|-|-|
| no corruption | ACCEPTED, correct, 5 groupings |
| one stray `</NODE>` inside the intake folder | ACCEPTED, 1 grouping, 2 invented placements |
| one stray `</NODE>` at the top of the tree | ACCEPTED, 2 playlists of 7, 1 invented placement |
| one stray `</NODE>` just before `</PLAYLISTS>` | ACCEPTED, correct, harmless |
| one `</NODE>` REMOVED inside the intake folder | REFUSED `library-export-unusable` |
| a node open tag this build cannot parse, mid tree | REFUSED `library-export-unusable` |
| a legitimately empty folder, self closed | ACCEPTED, correct |

So the hole is specific and it is one direction: an EXTRA close inside the tree.
The opposite corruption and an unparseable tag both already refuse, and a
legitimately empty folder still passes, so the fix does not have to trade a false
refusal for it.

**Condition one, driven end to end and not argued from source.** Met. Every number
above came from running `export.read_export`, `aging.intake_aging` and
`duplicates.audit` on the suite's own fixture, not from reading the parser.

**Condition two, a named user facing cost.** Met twice over. "Is told something
false" and "is shown a clean report over state the tool could not read" are both
named verbatim in the merge bar.

**Why this is in scope for a read only unit, stated rather than assumed.**
`read_export` already performs six structural refusals and one of them is the
identical check on the other section: `if declared != len(tracks)`, pinned by
`test_a_truncated_export_refuses_because_the_declared_count_disagrees` and
measured at 2 deaths as row V23. The PLAYLISTS section carries the same
declaration on every node, `Count` on every folder and `Entries` on every
playlist, and none of it is read. The module's own standard already covers this
class; the fix is the check it already wrote, applied to the section it did not
apply it to.

**What is UNMEASURED about this finding, named rather than glossed.** I did not
measure a producer that emits an unbalanced close. rekordbox writes balanced XML.
What I measured is that this module accepts one and reports over it. The module's
stated contract is "a wrong document is never an empty library", and it enforces
that contract on five other structures, so the input is in scope by the module's
own standard rather than by mine. A reviewer who disagrees with that framing
should read this as the strongest residual in the report rather than as a blocker,
and the fix is the same either way.

## Finding 2. The typed floor can be emptied with the whole suite green, and its own test then asserts nothing

**RESIDUAL.** The author named `CITED_FLOOR` as his weakest guard and he was
right about which one, though not about how it fails.

**Driven.** Three rows, each promoted to a full suite run of 3537 collected:

| row | mutation | deaths |
|-|-|-|
| V29 | `CITED_FLOOR` drops the reverts file this very commit created | **0** |
| V30 | `CITED_FLOOR` drops the module the round changed | **0** |
| V31 | `CITED_FLOOR` is emptied to `()` | **0** |

**The composite, because a zero row needs one.** The failure the floor exists for
is a merge base that resolves wrongly and empties both derivations at once. Row
V43 simulates it by making `_merge_base` return `HEAD`:

    V43  merge base broken, floor intact          4 deaths
    V45  merge base broken, floor EMPTIED         3 deaths
    V46  merge base broken, floor short one file  4 deaths

Exactly one of the four deaths belongs to the floor's own check, and that check
goes silent when the constant it reads is empty. The other three come from
neighbouring tests catching this particular simulation for their own reasons,
which is luck rather than coverage.

**The shape underneath, which is the part worth keeping.**
`test_the_named_floor_still_bites_when_both_derivations_narrow_together` is one of
the fourteen tests this round added, and its whole subject is that constant. Read
by node id, it appears in exactly one failure list in the fifty row table, V32's,
which removes the CHECK. It survives the CONSTANT being emptied, because its body
is a `for named in CITED_FLOOR:` loop wrapping a `pytest.raises`, and a loop over
an empty tuple is a test that passes while asserting nothing.

That is precisely the shape the round's own docstring names one level up: "A
floor that covers what it enumerates is not a property, it is the identity of the
files it lists." The round fixed that for the derived list and reproduced it in
the constant that backstops it, which is `METHOD.md`'s fifth pattern, a fix
reproducing its own class one file over.

**Both floor conditions.** Driven: yes, three full suite runs. User facing cost:
none. This guard polices how residual findings are cited inside this repository's
own documents. Nobody loses data, is told something false, is blocked from a verb,
or is shown a clean report. RESIDUAL.

**Closes when** the loop is given a lower bound it cannot satisfy vacuously, for
example asserting the constant's length against the count of files the second
derivation names, which is a number the same test already computes.

## Finding 3. Half of the new refusal's detail payload is asserted and half is not

**RESIDUAL.** Row V18 removes the `found` key from the refusal `detail` dict, the
key that tells a person which `Type` values the reader actually saw. Zero deaths
on the full suite, 3537 collected. Its sibling key in the same dict, `nodes`, is
row V17 at 3 deaths, because the parametrized test asserts
`f"{INTAKE.display} / phil_07_01_2026" in ...detail["nodes"]` and asserts nothing
at all about `found`.

The `found` key is the half that says WHAT was unreadable rather than WHERE, which
is the half a person needs to decide whether to re-export or to go and fix a
hand edit. It is new in this round and the author's table has a row for the paths
and none for the values.

Driven: yes. User facing cost: none today, because the key is present and correct
on the branch as it stands. RESIDUAL.

## Finding 4. The word a write refusal uses for a folder is not pinned

**RESIDUAL.** Row V09 respells `KIND_FOLDER` from `folder` to `directory`. Zero
deaths on the full suite. That constant is not only a comparison token: `_type_name`
returns it straight into the sentence "a folder named 'Deep House' is already
there, and this writer emits a playlist", which is a refusal a person reads and
acts on.

**Composite.** Row V39 rewords that whole sentence and kills 2, so the sentence is
pinned and the noun inside it is not. Row V13, which makes the same function
return the kind name bare, kills 1, so the UNREADABLE branch's wording is pinned
while the folder branch's is not.

Contrast row V10, respelling `KIND_PLAYLIST`, which kills 1. The two constants are
symmetrical in the code and asymmetric in the coverage.

Driven: yes. User facing cost: none on the branch as it stands. RESIDUAL.

## Finding 5. The new refusal has no fixture carrying exactly one unreadable node

**RESIDUAL.** Row V50 narrows the round's headline guard from `if unreadable:` to
`if unreadable[:-1]:`, so a document with exactly ONE unreadable node is accepted
and everything else still refuses. Zero deaths on the full suite.

**Composite.** Row V51 makes the same guard never fire at all and kills 3, so the
guard is genuinely held for the many node case.

The reason is visible in the fixture: every parametrized case does
`library_export().replace(old, new)` with no count, which retypes all seven
playlists at once. The single node case, which is what one hand edit or one
partial write actually produces, is not built anywhere in this repository.

Driven: yes. User facing cost: none, the shipped code refuses correctly on one
node. RESIDUAL.

## Finding 6. Two membership tests can be widened with the suite green

**RESIDUAL.** Two rows, both zero on the full suite, both WIDENINGS rather than
removals, which is the direction a composite that removes the guard cannot see.

| row | mutation | deaths | composite |
|-|-|-|-|
| V22 | `has_folder` matches the display anywhere in a folder path rather than at its last element | **0** | V40 always False kills 23, V41 always True kills 2 |
| V28 | the intake grouping filter reads `playlist.path` rather than `playlist.path[:-1]` | **0** | V42 dropping the filter entirely kills 5 |

V28 is the more interesting of the two. Under it, a playlist whose own name equals
the intake folder's display becomes an intake grouping and is aged. The composites
prove both tests are load bearing; neither proves the boundary they are written
at.

Driven: yes. User facing cost: none on the shipped code. RESIDUAL.

## Finding 7. The author's table is thirty rows against fifty, and eight of the differences are guards his own round created

**RESIDUAL.** The author reports 30 rows and 4 zero rows. The independent table is
50 distinct rows and 11 zero rows. Of the eleven, two are his own K15 and K18 and
reproduce his numbers exactly, one is inert by construction, and the remaining
eight are guards his table did not mutate: V09, V18, V22, V28, V29, V30, V31, V50.

Six of those eight sit on code this round wrote or on constants this round moved.
That is `METHOD.md`'s standing observation reproducing again, that a fix agent
mutates what it believes it changed. The measured gap this time is 30 against 50,
which sits inside the range the method already records.

His narrative claims that I reproduced and confirmed:

- 3522 passed, 15 skipped, 3537 collected. Confirmed on the baseline and on every
  full suite row in the independent table.
- V01 and V02 costing the same 7 each, confirmed.
- The untracked composite C0 to C3, reproduced with his numbers.
- `faint.discard` in `_record` being load bearing: independently measured at 2
  deaths as V47, with V48 at 4 and V49 at 2. His K11, K31 and K12 reproduce.
- Every one of the nine added test functions is killed by at least one row in the
  independent table.

Driven: yes. User facing cost: none. RESIDUAL.

## Finding 8. The write path residual's scope claim holds, driven rather than argued

**RESIDUAL, and it is the author's own filing, confirmed.** The round filed two
write path enumerations, one in `rbxml` that infers the enclosing tree and one in
`trees` that enumerates a tree's genre folders, as out of scope for a read only
unit. Attack four asked whether either is reachable from U34's own read path,
because if it is, it is not a residual by scope.

**Driven, not read.** Both functions were replaced with traps that raise on entry,
and then every public entry point this unit owns was run over the suite's own
export: `read_export`, `read_export_file`, `intake_aging`, `intake_groupings`,
`duplicates.audit`. All five completed with their correct answers. Neither trap
fired.

The import graph agrees: `export.py` imports `cratekit.write.rbxml` and nothing
else from `write`, and neither `aging.py` nor `duplicates.py` imports anything
from `write` at all. `cratekit.write.trees` is not reachable from the reports
package, and `_tree_node` is called only from the six write functions inside
`rbxml` itself.

The scope claim is correct and the residual stands as filed.

## What HELD under attack, stated as plainly as what did not

**The structural claim held.** The round's claim is that `rbxml.node_kind` is now
a total three valued function and `read_export` refuses before a `LibraryView`
exists, so a view type cannot describe a tree whose KINDS were a question. I
attacked it directly and could not break it.

What I tried:

1. **Other constructors.** `LibraryView` is constructed in exactly one place in
   `src`, at `export.py:275`, downstream of the refusal. The only other
   construction anywhere is a test fixture. There is no second reader, no cached
   view, no `dataclasses.replace` site, and no test helper promoted into `src`.
2. **The root node, which the round deliberately does not classify.** Driven with
   the root carrying `Type="2"`: the tree reads correctly, every child is still
   classified, and nothing downstream asks the root's kind. The docstring's
   justification is accurate.
3. **A self closing root.** Yields an empty tree, `has_folder` is False, aging
   refuses `intake-flow-absent`. Correct.
4. **A duplicate `Type` attribute on one node.** `node_at` builds its attribute
   dict with `dict(findall(...))`, so the LAST value wins. Undeclared first and
   declared second reads as the declared one; declared first and undeclared second
   refuses. The unsafe direction is the one that refuses.
5. **Every spelling `node_at` can hand the classifier**, directly: `"0"`, `"1"`,
   `""`, `"2"`, `" 1"`, `"01"`, `"TRUE"`, `"playlist"`. Only the two declared
   values answer positively; the other six answer unreadable. Total, as claimed.
6. **A node whose open tag the build cannot parse.** Refuses.

The one door I did find is finding 1, and it is not a kind door. Under a stray
close every node still says what it is, so the sentence the round actually wrote
is not falsified. What is falsified is the broader promise the module docstring's
numbered list makes, that every document failing a structural check is refused
with the structure named. Node balance is a structure it does not check.

**What a green suite cannot see, hunted separately.** An AST walk over every
`assert` in the round's two test files for an expected value that comes from the
code under test returned one candidate, `test_the_thresholds_come_from_the_configured_values`,
which on reading constructs its expected value from literal numbers and is a real
assertion. No duplicate keys in any dict or set literal under `src/cratekit`
outside the vendored tree. `node_kind`, all three `KIND_` constants and
`_type_name` each have exactly one home in `src`, so no symbol in this round's
surface means two things in two modules. No test in the round's surface forbids a
feature by naming the previous implementation's symbols.

## The battery, from inside the worktree with its own venv

    ./.venv/bin/ruff check src tests scripts     All checks passed
    ./.venv/bin/python -m pytest --tb=no          3522 passed, 15 skipped
    ./.venv/bin/python scripts/scan_repo.py       exit 0, no output

Collected count `3537`, taken with `pytest --collect-only -o addopts=`.

Working tree clean before and after every measurement. Every mutated file
restored by rewriting snapshotted text and then verified against
`git show HEAD:<path>`: `rbxml.py`, `export.py`, `aging.py`, `duplicates.py`,
`test_reports.py` and `test_rbxml.py` all match.

## Named as unmeasured

- **A producer of an unbalanced node close.** Finding 1 measures that this module
  accepts one and reports over it. It does not measure anything in this repository
  or in rekordbox that emits one. That link is unmeasured and the finding is
  written so the merge decision can be taken with it in view.
- **The CLI surface.** `cratekit.cli.reports` does not exist yet; the registry
  names it as a module a later unit lands. Every drive in this report goes through
  the module API directly, because there is no verb to drive.
- **Timing.** No timing row was taken. Nothing in this round's diff is on a hot
  path and no bound in it is a duration.
- **The parked conformance branch and the `write/metadata.py` defect** are out of
  scope per `METHOD.md` and were not touched.
