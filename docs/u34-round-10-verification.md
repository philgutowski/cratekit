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

**MERGE.** No open blocking finding.

Finding 1 was written up as BLOCKING on the first pass and is **DOWNGRADED to a
residual** by the reachability measurement in the section "Finding 1's producer,
hunted" below. The defect is real and the cost is real, but the merge bar
requires a user facing cost, and a cost over an input nothing produces is not
one. Four candidate producers were driven and none of them emits the input.
Decisively, two REAL rekordbox exports off the live volume, 56 MB and 28250
playlist nodes each, are balanced, carry no raw bracket in any name, and declare
counts that agree with the walk on every single node.

What that measurement says precisely, and the distinction matters because it is
`METHOD.md`'s first defect pattern: **I measured that four driven candidates do
not produce it, not that nothing produces it.** One of the four, the predecessor
system, carries a live mechanism that DOES emit an unbalanced document, driven
and reproduced below, and what stops it is only that no writer in either tool
emits the byte it needs. That is a residual with a named trigger rather than an
absence.

Everything else was already a residual. The round's own structural claim HELD
under direct attack and its four blocking answers all reproduce. See "What held".

## Finding 1. An extra node close is accepted, and both reports render over a tree that was re-parented under them

**RESIDUAL**, downgraded from blocking. The defect and both costs below were
driven and stand exactly as measured. What changed is the second floor condition:
see "Finding 1's producer, hunted" for the reachability measurement that
withdraws the user facing cost.

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

**Condition two was withdrawn on measurement.** The first pass named the producer
as unmeasured. It has now been measured, and the section below is that
measurement. Four candidates driven, none produces the input, so the cost is not
reachable and this is a residual.

**Closes when** the check in "The fix, measured" lands, which costs nothing on
the suite and refuses both harmful spellings.

# Finding 1's producer, hunted

Four candidates, each driven, each reported separately. The question is narrow:
what writes an export whose playlist tree carries an unbalanced node close.

## Candidate 1. Cratekit's own write path. NOT FOUND, and here is what was driven

Every real splicer in `cratekit.write` was run on the write suite's own fixtures,
and after each call the playlist section was checked for balanced paired opens
against closes, and every node's declared `Count` or `Entries` against what the
walk finds under it.

Happy paths, all balanced and all counts exact:

    insert_intake_playlist, twice, and again for the idempotent replace
    insert_root_playlist, twice, including the same name replace
    insert_genre_folder, twice, then remove_folder_node on each
    remove_folder_node on a SELF CLOSED folder
    splice_into_subplaylist then remove_tracks_from_subplaylist
    insert_empty_subplaylist
    insert_catalog_folder into an absent tree, then a second time
    trees.apply_playlist_changes and trees.apply_unplaced_changes

Error and refusal paths, all balanced:

    a playlist named with a quote, a bracket, an ampersand, a slash, and with
      the literal close tag as its name
    a splice whose folder is absent, with create_missing off and on
    a removal of a track that is not there
    a removal of a folder that is not there
    a removal by a name that is a playlist rather than a folder
    a splice into a document whose tree count is ALREADY wrong

**No driven splicer, on any path, emitted an unbalanced tree.** The refusal paths
are the reason: `insert_catalog_folder` mutates a buffer and returns a warning,
and `trees.insert_record_labels_tree` raises on that warning BEFORE it persists
anything, so a half spliced buffer never reaches a file.

**One producer WAS found, and it is a count rather than a balance.** See finding 9.

## Candidate 2. A partial or interrupted write. NOT POSSIBLE, and it is structural

Every persist of an export in this product goes through
`config.atomic_write_bytes`. Read: it creates the temp file with `mkstemp` in the
TARGET's own directory so the rename is same filesystem, writes, flushes,
`os.fsync`es, and then `os.replace`s. There is no in place write of an XML
document anywhere in `src` outside the vendored tree. The only two writes in the
whole product that do not go through it are a mastering listing and a set builder
cache, neither of which is an export.

A crash, a signal or a full disk therefore leaves either the previous document or
the new one, never a half spliced one.

## Candidate 3. The predecessor. MECHANISM FOUND AND DRIVEN, input not producible

DJ_tools was imported read only. Nothing was written to it.

`dj_tools.DJ_common.rbxml.remove_folder_node` bounds a node's open tag with
`content.find(b">", node_start)` and then reads the byte before it to decide
whether the node is self closed. That find is NOT quote aware. XML does not
require a `>` to be escaped inside an attribute value, so a name carrying the
literal two bytes `/>` makes the walk read a paired open tag as self closed,
which makes the depth walk stop one close early, and the range deletion then
removes an open without its close.

**Driven, on a document built in the probe process:**

| the document | after remove_folder_node |
|-|-|
| ordinary names, the control | 2 opens, 2 closes, balanced |
| a raw bracket in a child's name | 2 opens, 2 closes, balanced |
| the literal `/>` in a child's name | **2 opens, 3 closes, UNBALANCED** |
| the literal `/>` in the target's own name | not found, no deletion, balanced |

Cratekit's own `remove_folder_node` was run on the identical input and returned a
balanced document, because its open tag regex is quote aware. The successor fixed
the class; the predecessor still carries it.

**And the input is not producible by either tool.** Both escapers were driven:

    predecessor xml_escape_attr('w/>120')  ->  'w/&gt;120'
    cratekit    xml_escape_attr('w/>120')  ->  'w/&gt;120'

So the byte has to arrive from rekordbox or from a hand edit, which is candidate 4.

## Candidate 4. rekordbox. MEASURED ON THE TREE, and it is the decisive one

Two real rekordbox 7.2.17 collection exports were read off the live library
volume, read only. The rekordbox database was not opened, named or copied, and
nothing was written to the volume. Aggregates only below; no track, artist or
playlist content is reproduced anywhere in this report.

| | `8-2-18-54.xml` | `8-214-32.xml` |
|-|-|-|
| size | 56.3 MB | 56.2 MB |
| paired opens in PLAYLISTS | 28189 | 28189 |
| closes | 28189 | 28189 |
| self closed nodes | 61 | 61 |
| balanced | **yes** | **yes** |
| names carrying a RAW `>` | **0** | **0** |
| names carrying a RAW `<` | 0 | 0 |
| names carrying an ESCAPED `&gt;` | 5 | 5 |
| folders and playlists found by the walk | 74 and 28176 | 74 and 28176 |
| distinct `Type` values in the tree | `0`, `1` | `0`, `1` |
| folders whose `Count` disagrees with the walk | **0** | **0** |
| playlists whose `Entries` disagrees with the walk | **0** | **0** |
| `read_export` | ACCEPTED, 10070 entries | ACCEPTED, 10070 entries |

Three things fall out of this table and each one matters.

1. **rekordbox escapes the bracket.** Five real playlist names in this library
   contain a `>`, and all five are written `&gt;`. Zero raw. So candidate 3's
   mechanism has no input on a rekordbox authored document.
2. **A real tree is balanced**, on 28250 nodes across two exports taken hours
   apart.
3. **rekordbox is NOT loose about `Count`.** Every one of 28250 nodes declares a
   count that agrees exactly with what the walk finds under it. Reading the
   declaration is therefore free on a real document, which is the question the
   fix depended on.

What is still UNMEASURED here: two exports from one library on one rekordbox
version. I did not measure another version, another library, or a document
somebody hand edited. A hand edit is a real thing in this workflow, and it is the
one route to the predecessor's mechanism that these measurements do not close.

## The fix, measured

The probe mirrors the check `read_export` already runs on the COLLECTION section
onto the playlist tree: every node's declared `Count` or `Entries` against what
the walk finds under it.

**Does it catch the document finding 1 is about, and does it refuse anything it
should not:**

| document | probe | wanted |
|-|-|-|
| the suite's own export, untouched | accept | accept |
| one stray close inside the intake folder | **REFUSE**, ROOT declares 2 holds 6, INBOX declares 5 holds 1 | refuse |
| one stray close at the top of the tree | **REFUSE**, the tree folder declares 2 holds 1 | refuse |
| one stray close just before the section close | accept | accept |
| the routing fixture, and with the collision bait | accept | accept |
| a legitimately empty folder, SELF CLOSED | accept | accept |
| a self closed empty PLAYLIST | accept | accept |
| real export `8-2-18-54.xml`, 28250 nodes | accept | accept |
| real export `8-214-32.xml`, 28250 nodes | accept | accept |

**Zero false refusals on either real export.** The one harmless spelling, a stray
close sitting outside the tree body, is correctly accepted, and so are both self
closed shapes.

**Suite cost: zero,** provided the check is ordered AFTER the unreadable kind
refusal. Placed before it, three of this round's own parametrized cases fail,
because they retype playlists and the count check then fires first and says the
wrong thing. Placed after it: **3522 passed, 15 skipped, 3537 collected,
identical to the baseline.**

**Runtime cost, with its repeat count and range**, on the 56 MB export, 5 repeats:

    read_export today          median 0.74s   range 0.74 to 0.75
    the count check alone      median 0.69s   range 0.67 to 0.69

So the check as probed roughly doubles the read of a real library. It is written
as a second walk; folded into `_read_nodes`, which already visits every node and
already has each `NodeSpan`, it costs close to nothing. Whoever lands it should
fold it rather than append it.

**One false refusal was found, and it is not the check's fault.** See finding 9.

## Finding 9. A create path that does not bump the count it invalidates

**RESIDUAL against U34. A finding against U18**, which is the unit that landed
`src/cratekit/write/rbxml.py` and `src/cratekit/write/trees.py`
(`feat(write): the tree writers, in both mediums`).

Two writers create the same node and only one of them keeps the parent's count
true.

- `insert_empty_subplaylist` inserts the node and then calls
  `_bump_count(content, folder, +1)`.
- `splice_into_subplaylist`'s `create_missing` path inserts the node and **does
  not bump anything.**

**Driven**, on the write suite's own routing fixture:

    after insert_genre_folder                     counts exact
    after insert_empty_subplaylist                counts exact
    after splice_into_subplaylist, existing sub   counts exact
    after splice_into_subplaylist CREATE_MISSING  BY GENRE / Deep House
                                                  declares 1, holds 2
    after trees.apply_unplaced_changes            BY GENRE / Deep House
                                                  declares 1, holds 2

The last row is the one that makes it production rather than a test only path:
`trees.apply_unplaced_changes` passes `create_missing=True`, so the unplaced
routing pass is a live caller.

The cost today is a document whose folder count understates its children.
rekordbox trusts the count over the children it can see, which the module's own
`remove_tracks_from_subplaylist` docstring states in as many words, so this is a
real write path defect and not merely cosmetic. The cost tomorrow is that it is
the ONE false refusal the finding 1 fix produces.

**Both floor conditions against U34.** Driven: yes. User facing cost attributable
to U34: none, this is not U34's file and U34 only reads. RESIDUAL here, and it
should be filed against U18's surface with the reproduction above.

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

- **Whether the fix should land on U34 at all.** My recommendation: **yes, the
  read side check belongs here**, because `read_export` is U34's file, the check
  is the one it already runs on the other section, it costs the suite nothing and
  refuses nothing real. Finding 9, the write side producer, does NOT belong here
  and should be filed against U18. The two are separable: the reader's job is to
  refuse a document it cannot trust whatever wrote it, and the writer's job is to
  keep the count true. Landing only the reader check would make U18's unplaced
  routing pass produce documents U34 refuses, so the two want to land in that
  order or together, and that ordering is the one thing a coordinator has to
  decide rather than a verifier.
- **rekordbox beyond one library on one version.** Two exports, both 7.2.17, both
  from the same library, taken hours apart. Another version or another library is
  unmeasured, and so is any hand edited export, which is the one live route to
  the predecessor's mechanism.
- **The predecessor's other five splice sites.** `remove_folder_node` in
  `DJ_common/rbxml.py` was driven. `label_library.py`, `setid_lib.py`,
  `sort_unplaced.py`, `create_vox_playlists.py` and `minimal_xml.py` also emit
  node closes and were NOT driven. The class is present in the one I drove, so
  the others are unmeasured rather than clean.
- **The CLI surface.** `cratekit.cli.reports` does not exist yet; the registry
  names it as a module a later unit lands. Every drive in this report goes through
  the module API directly, because there is no verb to drive.
- **Timing.** No timing row was taken. Nothing in this round's diff is on a hot
  path and no bound in it is a duration.
- **The parked conformance branch and the `write/metadata.py` defect** are out of
  scope per `METHOD.md` and were not touched.
