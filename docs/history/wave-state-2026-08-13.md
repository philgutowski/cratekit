# Wave state, 2026-08-13: the harness got built, U16 merged, and a countdown nearly went silent

Continues `docs/wave-state-2026-08-10-evening.md`. The method lives in
`docs/METHOD.md`. This file is history: what was measured and what was decided.

## What is on main

`258a1cd`, pushed, clean. **4763 passed, 13 skipped.** `board.py audit` exit 0.

**U16 merged, and the hardware fixture harness merged with it.** The wave went
from five merged units to six. Three branches remain: u12, u23, u27.

## The hardware fixture harness, approved 2026-08-10 and deferred four sessions

Built first, deliberately, because it is what unblocks the other three units and
it had been the reason they were deferred each session since.

One reusable set in `tests/_hardware.py`, with `scripts/calibrate_timing.py`:

- **A timing runner** returning a `TimingTable` of the repeat count, every
  duration, and a pass rate against a threshold. METHOD says a timing row
  carries a repeat count and a pass rate, never one number, and this makes that
  the only shape the type can hold.
- **A FAT32 image** created and mounted with hdiutil at a private mountpoint and
  torn down on every exit path.
- **A read only volume** the caller populates while it is writable, which then
  remounts read only and refuses writes with `EROFS`.

Calibrated on a quiet machine: **median 0.0680s over 25 runs, relative spread
0.098**, well under the 0.25 that says the machine was busy. Thresholds are
expressed as multiples of that median rather than as absolute seconds.

### Two hardware facts, probed and recorded so nobody pays twice

**`newfs_msdos` cannot lay out FAT32 under roughly 33 MB, and hdiutil reports
that as `create failed, Operation not permitted`.** The first probe asked for
8 MB and read the answer as a sandbox permission problem, which it was not. The
fixture now refuses under 34 MB with an error naming the real cause.

**The macOS msdos driver ALLOWS symlinks on a mounted FAT volume.** Symlink
refusal is therefore not a FAT detector. The module reads the mount table
instead, through `filesystem_kind`.

### What the independent review of the harness found, and it found real things

The reviewer did not write the code and drove every finding. Three were
MEASUREMENT CORRUPTING, meaning they could hand a future verifier a confident
number that is false, which is this project's worst defect class. All three
were fixed **on the checking path**, which is defect pattern 3 stated as a
positive.

1. **The calibration recorded the machine and checked nothing.** The payload
   stored interpreter version and CPU count, and `load_calibration` validated
   neither, so a baseline measured on a different machine loaded silently. On a
   machine twice as fast, an operation that regressed from 0.05s to 0.15s would
   report 25/25 pass. Pattern 2, an identity field written on one path and
   trusted alone on the other. Loading now refuses a mismatch.

2. **The mount table lookup matched by substring and split on the first
   bracket.** macOS mounts a second volume with a duplicated label at
   `NAME (1)`, which is what every rekordbox stick labelled PIONEER produces.
   Asked about an ABSENT `NAME`, the old code matched the sibling's line and
   returned its filesystem, so `LookupError` as an absence signal would say a
   missing volume is present. That is exactly the question U27's doctor asks.
   The lookup now compares the whole path exactly.

3. **The read only volume trusted its own forced detach.** Between populating
   and remounting, a busy mount can exhaust the retries and take the `-force`
   path, which can strand unflushed data. The remount would then succeed, show
   `read-only`, and serve a volume missing part of what the caller wrote. The
   fixture now fingerprints what `populate` declared and verifies it after the
   remount.

Three smaller ones closed with them: a `TimingTable` could be constructed with a
repeat count disagreeing with its own durations and print a pass rate of 5.00;
teardown could rmtree THROUGH a still mounted volume when detach failed,
deleting the evidence; and an unquiet calibration printed a warning and then
wrote the file anyway, which is a check sitting beside the performing path
instead of gating it.

## U16, verified and merged

Light pass, round 8, first independent verification, by an agent that did not
write the code. **Verdict MERGE.** 25 rows against the light cap, 23 killed, two
confirmed zeros, 10 rows logged as dropped with their ranking reasons.

Both zeros are the same shape and both are residual: the suppression warning's
sentence and its machine readable code slug are each free to drift with a green
suite, because all ten assertions on the slug compare against the constant under
test, which is X equals X while genuinely exercising the code. The composite
pair is what makes them merge safely: **removing the suppressed rows from the
warning channel kills 20 tests**, so R36's presence guarantee is pinned while
the words carrying it are not. Filed as **R-77 and R-78**.

The slug finding is a clean illustration of condition 3 of the merge bar. Its
cost lands on a consumer that branches on the code, no such consumer exists in
the repository, so the input is unreachable today and the report says zero
in-repository candidate producers were driven because there are none, which is
not the claim that nothing ever will.

### Three things the merge found that neither tree could see alone

This is the defect class named on 2026-08-10, a rule verified on one surface
while another surface carries the same coupling. All three were found by
attempting the merge, not by any verifier.

**1. A countdown entry nearly took 330 tests out of collection.** U24 landed
`cratekit.core.tombstone` on main while U16's branch carried that algorithm
replicated byte for byte, guarded by a test gated on the module's absence. The
register's design is that the entry is deleted the moment the module lands,
which arms the guard. Deleting the entry alone is not that: `requires()` raises
`KeyError` at import, `tests/test_match_states.py` fails to COLLECT, and its
330 tests stop existing while the run reports green. **The discharge has two
halves, the entry and the decorator, and they move together.** Armed properly,
the guard passes: the two copies of the identity agree. That guard had been
waiting for this exact merge and had never once run.

**2. Three reserved cause pins moved, and they were re-measured rather than
widened.** U16 appends exactly one cause, `intake-list-unusable`. Population 100
to 101, non reserved half 78 to 79, kebab literal surface 239 to 256, named at
risk surface 17 to 18, literal at risk surface 36 to 38. The comparison those
numbers are spent on survived and widened rather than narrowed: the named
surface, 18, is still smaller than the literal surface, 38. The half that would
have signalled a real problem, modules holding a name resolving to a cause
declared somewhere else, **has been 8 across all three measurements** and no
merge has moved it. The residual's original figures were left standing as what
was measured on the day, with the re-measurements appended beneath, because
rewriting them in place would destroy the record of what the argument was bought
with.

**3. The collected count rose while 24 identifiers went missing.** Total went
4445 to 4776. Reconciled BY IDENTIFIER under `LC_ALL=C` against the UNION of
both sides, 24 identifiers present on a side were absent from the merge. All 24
are accounted for and none is lost coverage: 15 plus 1 are two renames main
made, whose parameter sets reconcile exactly (the conformance gate test went to
17 parameters, being main's 16 plus U16's `match.run`), and 8 are countdown
parameters that correctly retired as modules landed. A total only check would
have read the rise as health, which is precisely why METHOD says reconcile by
identifier.

## Hygiene

`docs/mutation-rows.md` is now an **archive** and says so in its first line. Its
procedure section was written for a hand rolled driver and had drifted into
contradicting METHOD on the expensive thing: it said rows are measured against
the whole suite unless the row says otherwise, while METHOD says confirm deaths
on the importing subset and spend a full suite only on the zeros. The historical
rounds are untouched.

The u32 branch, merged long ago and never deleted, is gone from both places with
its worktree. The u16 and fixtures branches went the same way at their merges.

## What the next session does

1. **U27, U23, U12, in that order, each with the harness.** All three have been
   deferred five sessions and the thing that blocked them is now built and
   proven. U27 merges WITHOUT a closing trailer.
2. `docs/METHOD.md` is 265 lines against the 80 it was written to be. It wants a
   trim pass, and the countdown lesson above is one line, not a section.
