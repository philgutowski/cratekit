# Wave state, 2026-08-09: three verifications, one fix round, nothing merged

Continues `docs/wave-state-2026-08-04.md`, which stays authoritative for
everything before this date. Read that one for the wave's method, its four
recurring defect patterns and the standing driver rules. This file records only
what this session measured.

Phillip's two standing decisions for this session, both taken at the start:

1. **Narrow fan-out.** Verify two or three units, highest value first, rather
   than relaunching the seven agent wave that exhausted the weekly budget on
   2026-08-04.
2. **The merge exit criterion stands.** Nothing merges until a branch verifies
   CLEAN. The alternative, merging on zero BLOCKING with the rest recorded as
   residuals, was considered and declined.

## What is on main

`2c4a2f9` at session start, clean, 3422 passed and 17 skipped, `board.py audit`
exit 0. **No unit merged this session.** U32 remains the only unit ever to clear
the criterion.

## The three units chosen, and why the other three were not

Chosen on merge readiness under the clean criterion, since the point of spending
here is to convert budget into a merge rather than into more findings.

- **U24**, because round 8 was the unfinished work this session inherited, and
  because U24 gates U16 in merge order.
- **U34**, because read-only reports have the smallest blast radius and were
  therefore the likeliest to clear.
- **U38**, because a static registry verifies deterministically and cheaply.

**U12, U23 and U27 were deliberately left at their tips.** Their queued attacks
need a 25 run timing measurement, a mounted FAT image and a real read only
volume image respectively. That is where a budget disappears without producing a
merge. Their state is unchanged and `docs/wave-state-2026-08-04.md` still
describes them correctly.

## Verdicts

| unit | round verified | verdict | blocking | rows run by the verifier | zero rows found |
|---|---|---|---|---|---|
| U24 | 8 | BLOCKING | 3 | 17 | 1 |
| U34 | 9 | BLOCKING | 4 | 49 | 12 |
| U38 | 7 | BLOCKING | 4, plus 7 residuals | 83 | 21, of which 7 unaccounted |

Eighteen, nineteen and twenty consecutive blocking verifications.

**Severity has NOT reached the floor, and that is the answer to the open
question in the 2026-08-04 file.** U34's B2 is a report rendering CLEAN over
library state it could not read. That is well above "a test that cannot see what
it claims", which is where the previous session thought the severity had
settled.

## U24, and the round this session finished

Round 8 was inherited uncommitted and was **half done in the way that matters**:
`tombstone.fold_code` was fully written and documented, and it was never called.
`deletion/stores.py` still folded the ISRC with the free text `fold`. The whole
suite passed with all three of the round's changes in place, which is the
finding rather than a reassurance: every one was a guard no test covered.

Round 8 was completed, measured and committed at `df945fb`. It then verified
BLOCKING with three findings, and **the worst is round 8's own doing**.

### F1, and it is the third consecutive instance of the same pattern on one branch

`stores.spellings_earlier_builds_wrote` reconstructed the spelling earlier
builds wrote **by calling the LIVE composer**. Round 8 changed that composer, so
the reconstruction of history moved to what this build writes.

**The failure was silent rather than wrong.** Both sides of the comparison moved
together, so `verbatim == version_of(row)` became true and the function returned
the EMPTY TUPLE: not a wrong earlier spelling but no earlier spelling at all,
reported as "there is no history here". Driven at the round 8 tip over eight
version column shapes, six orphaned the record the parent build would have
written. The cost is the one that function's own docstring names: the row is
held open forever and the person is told to put back a file that is already in
the Trash where they put it.

**Generalise it: a function that reconstructs what an EARLIER build did must not
call the current implementation of the thing that changed.** That is not a
tombstone problem. Any backward compatibility shim written as "call today's code
and compare" has it, and it fails silently in the direction that reports no
work to do.

### F2, and it is why nothing caught F1

The single test covering that whole backward compatibility surface planted its
"earlier build's" record using the live `version_title`. Both sides moved
together, so it could not fail when that function changed. The X equals X shape,
sitting on the one path where it did real damage.

### F3

Round 8's own table mutated the tidy through the COMPOSITION limb twice and
never removed the FOLDING limb alone, which killed zero of 3458.

### Round 9, built and committed at `b5a4e86`, NOT yet verified

Two FROZEN historical composers, reconstruction from those rather than from the
live rule, three preceding spellings offered rather than one, and **every
historical spelling in the suite pinned to a LITERAL string**. The literal
pinning is the durable guard: the frozen functions still call live helpers that
could drift the same way, so freezing the limb that changed is what the code
guarantees and the literals are what guarantee the rest.

The frozen functions carry an explicit instruction not to keep them in sync. A
future round that changes composition ADDS one; editing one to match a new live
rule is exactly the defect they close.

Eight rows, no zero rows. **The first run of that table had two zero rows and
the reason is worth carrying.** Every remixer in the test set already ended in
`Remix`, so `already_spelled_as_a_remix` fired, the designation was never
appended, and the plain composer and the remixer composer produced the same
string. The two historical spellings coincided on every row, so neither the
second tuple entry nor the branch selecting it was exercised anywhere.

**And the first attempt to separate them was WRONG, which is the more useful
record.** A remixer differing only in WHITESPACE does not separate them:
`'Michael Woods '` composes a doubled space that `fold` collapses one step
later, so both builds write the same identity and there is no orphan. Only a
difference that survives folding orphans a record. Brackets survive it, interior
whitespace runs do not. `'[Michael Woods]'` is the separating shape. **The
literals were measured before being written into the test, after the reasoned
guess failed.**

## U34, round 9, BLOCKING with 4

**B2 is the finding of the session.** `write/rbxml.py` substitutes `""` for a
`Type` attribute that is absent or unreadable, and `reports/export.py` treats
anything not positively typed `"1"` as a folder. Driven end to end: a healthy
tree reports one expired and two stale intake groupings, and the same tree with
unreadable `Type` attributes reports nothing and **renders clean**.

The sharp part is the mechanism. `aging.py` refuses when the folder is absent,
and `export.py` states the folders tuple exists so that "not in this tree" and
"here and empty" cannot render identically. The misclassified nodes push their
own paths into `folders`, so **the unreadable children satisfy the guard written
to catch their loss**. There is a third state, "here and I could not read what
is in it", and it renders as the clean one. No fixture builds a `Type` other
than `"0"` or `"1"`, so nothing could see it.

- **B1.** `faint.discard` in `_record` is a guard nothing covers, zero deaths,
  and it is load bearing: without it an unresolved write overwrites a resolved
  one and a real configuration write goes unreported. Round 9's own table
  carries rows for `faint.add` and for `or key in faint` and none for the
  discard.
- **B3.** The derived coverage list can be silently narrowed on 8 of 18 files,
  including `docs/mutation/u34-round-9-reverts.py`, the file the same commit
  created. `CITED_FLOOR` names 9 files, and narrowing on a named one dies while
  narrowing on an unnamed one is silent. Deleting the floor assertion outright
  is also zero.
- **B4.** `UNIT_RESIDUALS = range(16, 27)` can be narrowed to `range(16, 26)`
  with zero deaths, so the ban list can stop covering `R-26`, which is the
  residual round 9 filed for its own stated cost. The assertion written to
  prevent exactly this checks `{"16", "25"}` and names the wrong number.

## U38, round 7, BLOCKING with 4 and 7 residuals

The branch is technically strong and the verifier said so: 22 of R-20's
published rows reproduce exactly, the baseline arithmetic reproduces, the
citation guard bites in every direction including the paired ones, and the two
comments claiming unreachability are genuinely true rather than merely undriven.

**B1. R-20's headline claim does not survive an independent table.** It closes
with "Zero rows would be findings and there are none", and an independently
derived 83 row table finds seven unaccounted zero rows.

**B3 is a new and sharp form of pattern 2, identity that is not unique to the
thing it identifies.** `test_the_guard_has_no_per_line_off_switch_at_all` asserts
`not hasattr(_guards, "_annotated_lines")`, `"_silenced_lines"`,
`"NOT_A_RESERVATION")` and `"tokenize" not in dir(_guards)`. That is **the
deleted hatch's fingerprint, not the property**. A fresh per-line escape hatch
with a different marker, no `tokenize` and none of those three names ships
green, wired in exactly where the deleted one was. Zero deaths.

**Generalise it: a test that forbids a feature by naming the last
implementation's symbols forbids that implementation, not the feature.**

- **B2.** A negative process status is a live, wholly uncovered bypass. Dropping
  the unary minus branch is silent, treating negatives as success is silent, and
  both together are silent. No fixture anywhere writes `exit(-1)`, while
  `cli/exit_codes.py` argues at length about negative statuses being signal
  numbers. The unit reasons about negatives and the only guard watching can be
  blinded to them.
- **B4.** Classifying an enum by its base is measurably indistinguishable from
  classifying it by its class name, because every enum name in `tests/` is one
  of three. The docstring rejects the rename-defeatable rule; measurement cannot
  tell the two apart.
- **R2, worth reading before citing the at-risk-population measurement again.**
  Its two halves are measured over different file populations with different
  resolvers. The "10 and 14" reproduce only when the two exempt table owner
  files are included and every assignment anywhere counts, which is wider than
  the shipped resolver. The comparison figures 25 and 5 reproduce exactly on the
  narrower basis. The conclusion survives; the symmetry of the argument does
  not.
- **R3.** None of the headroom or population numbers is pinned by any assertion.
  Six places in prose, zero tests. The justification for keeping the resolver
  widening decays silently as the tree grows.

## Two process failures, both mine

**The scratchpad was shared across three concurrent verifiers, and it collided.**
This is the "one scratch directory, eight agents" failure of 2026-08-04
recurring, and it happened because all three agents were pointed at one session
scratchpad. The U34 verifier's `rows.py` and `results.jsonl` were overwritten
mid run by another session's driver; it detected the collision, confirmed its
worktree clean and its snapshots matching HEAD, moved to a private
subdirectory, and continued. The U38 verifier found five foreign rows in the
shared results file and excluded them by their differing collected count. **No
measurement was corrupted, and that is luck plus two careful agents, not
design.** Next fan-out gives every agent its own directory, named for its unit.

**The round 8 mutation driver's collected count was an instrument that could not
fail.** It took the count from a run passed `-q`, which `pyproject.toml` already
sets, so it became `-qq`, the listing was suppressed, and every row reported
`collected=0` including the baseline. The driver's own docstring states the
never-pass-`-q` rule. The whole result set was discarded and re-measured rather
than the column being patched.

**The instrument that cannot fail is now the most common defect in this
project's own tooling, not just in the code under test.** Round 8's table, U34's
`CITED_FLOOR`, U38's R-20 completeness claim and U38's vacuous range test are
four instances in one session.

## The size gap between an author's table and an independent one

| unit | author's table | independent table | zero rows the author missed |
|---|---|---|---|
| U24 round 8 | 10 rows | 17 rows | 1 |
| U34 round 9 | 39 rows | 49 rows | 12 |
| U38 round 7 | 49 rows | 83 rows | 7 unaccounted |

This is the 2026-08-04 lesson holding without exception: **an author's own
mutation table is a draft, not a result.** Every one of these authors ran their
table honestly.

## What the next session should do

1. **U24 round 9 needs verification.** It is committed at `b5a4e86` and has
   never been attacked. It is the only round in flight.
2. **U34 needs fix round 10** for B1 through B4. B2 is the one with a real user
   facing cost and should lead.
3. **U38 needs fix round 8**, and B3 should lead: replace the fingerprint
   assertions with a property test that a guard cannot read a comment at all.
4. **U12, U23 and U27 are untouched** and their 2026-08-04 entries still stand.
5. The residual numbering decision from the 2026-08-04 file is still open and
   still blocks merges. Nothing this session changed it.
