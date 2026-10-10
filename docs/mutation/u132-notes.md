# U132 mutation table, read

One table, the author's and not independent, measured by `scripts/mutate.py`
on `fable/300-taxonomy-behind-shipped-schema` at `6c218c3f`. Null control 0 of
13523, no collect drift, every restore verified against `git show HEAD`.

**`u132.md`**, 25 rows, the cap, over the planner
(`core/taxonomy_upgrade.py`), the verb (`cli/verbs/taxonomy.py`), the doctor
check, and the skipped step warnings in adopt apply, tree rebuild, the resort
resume and `genre_favorites`. 21 killed, 4 zero. Four more were considered
and logged as dropped in `u132-rows.toml` with the reason each ranked below
the cap: P5, P10, W7 and G2.

## The four zeros

- **V1, the verb's stale refusal after the answer.** User facing, and the
  composite is the suite as it stands:
  `test_a_copy_edited_between_the_answer_and_the_write_is_refused_as_stale`
  edits the copy between `run decide` and the resumed verb and still passes
  with the guard off, because the explicit gate compares the decided digest
  with the plan the resumed verb rebuilds before it returns an answer
  (`gates.py`, the `DecisionStale` raise in `require`). What V1 guards is the
  window inside one process between that answer and the second plan, which no
  test reaches. The property the person sees, an edited copy is never written
  over, is held by the gate and measured by that test.
- **V4, the read back's text comparison.** User facing. Its composite,
  V4_composite, writes the copy with one line more than the plan while the
  comparison is off, and kills 2:
  `test_the_verb_asks_then_writes_the_upgraded_copy_and_keeps_the_old_one` and
  `test_what_is_held_is_said_and_written_around`. So the property, the text on
  disk is the planned text, is held by the verb tests; the comparison itself
  catches a write `atomic_write_bytes` never makes in the suite.
- **P9, the placement's kept whole check, and P9_composite.** User facing, and
  the composite measured nothing as well. It shifted the placement one line
  into the following entry, and the following entry's span starts at its
  comment run, so the shifted block lands between two comment lines and the
  copy still parses to the same entries. The author could not kill it in this
  pass. A placement that breaks the parse is also refused by the candidate
  load (P3, killed) and by the tests that parse the result back, so what is
  unmeasured is the narrower case: a placement that parses and loads but moves
  keys from one entry to another. Filed as residual `u132-f`.

## What the kills say

The planner's holds are each measured on their own case: a word another
bucket files (P1), a word the shipped template itself files twice and so is
not a clash (P2), and a candidate that would not load (P3). The version raise
(P4, 15 kills) and the child table cut (P7, 20 kills) are what most of the
planner tests lean on. The verb's backup (V2), its name never taking an
earlier backup's (V6), the restore on a failed read back (V3) and the no gate
on an empty plan (V5) each kill. Doctor names the gap (D1) and tells a shipped
defect from the copy's (D2). The warnings fire on every apply whatever it
added (W1), carry the coded note and the copy's version (W2, W3), and on a
rebuild or a resort only for the routing tree that run drove (W4 to W6).
