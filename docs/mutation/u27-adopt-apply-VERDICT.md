# U27, cratekit.adopt.apply_cli: author's mutation pass, verdict

**Verdict: MERGE.** No open blocking finding. Two rounds, 24 rows plus two null
controls, 40 pytest invocations. Round one measured three user facing zeros;
round two re-measured all three against the guards written to answer them and
every one kills. No zero rows remain, and no row was reclassified to get there.

**An author's own table is a draft, not a result.** No independent verifier ran
against this unit. Everything below was measured by the agent that wrote the
code, which METHOD says has missed guards its own round created on every unit so
far, with measured gaps of 10 against 17, 39 against 49 and 49 against 83.

| # | finding | class | where |
|---|---|---|---|
| 1 | the queued apply could never be resumed: the driver's child minted a fresh run and met an explicit gate with nothing recorded, for ever | FIXED in this unit | `60441e9` |
| 2 | the analysis watch was armed but no test said on which roots | FIXED, test | `S3` round 2 |
| 3 | the approval gate's digest was never offered and nothing could see it | FIXED, test | `G3` round 2 |
| 4 | the resume branch read the stale row rather than reconciling | FIXED, test | `G5` round 2 |
| 5 | adoption's memberships are collected and never written | RESIDUAL R-148 | not this unit's to close |

Finding 1 is the one worth reading. It was a real defect reachable by any person
who approved an adoption, and it was found by a row asking a different question.

## The numbers

| round | rows | killed | zero | collect-error | baseline | control |
|---|---|---|---|---|---|---|
| 1 (`u27-adopt-apply-author`) | 21 | 18 | 3 | 1 | 6147 green | killed 0 |
| 2 (`u27-adopt-apply-round-2`) | 3 | 3 | 0 | 0 | 6150 green | killed 0 |

Both controls killed zero, which is what makes the rest of each table
believable.

## The row that matters

`S1_no_session_at_all` removes the destructive session from around the whole
`apply_plan` loop, which is R-81's condition unchanged. It kills 5: all four
refusals plus the lock-held observation. The session this unit exists to add is
pinned by tests that measure the disk rather than the call order.

## The collect-error, which is expected rather than a problem

`R1_marker_restored` puts `planned_in` back on the registry entry. That
deliberately changes the conformance parametrization, so collection moves 1140
to 1138: `test_conformance_1_structured_output_is_actually_emitted[adopt.apply]`
and `test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[adopt.apply]`
stop existing, which is precisely the arming the marker controls. It killed 3
anyway. The driver refuses to call a row with collection drift a zero, correctly,
and the drift here is the mutation's own intended effect rather than a broken
import.

## Two rows were removed before measuring rather than measured

Both for the same reason, and it is the reason the 2026-08-23 learning gives:
a row whose new text behaves identically to its old text on this tree is not a
failed measurement, it is not a measurement, and promoting its zero costs a full
suite run to say nothing.

- `S5_seams_forwarded_as_none` measured a `_providers` helper that chose between
  omitting a keyword argument and passing `None`. `assert_gates` reads the two
  identically, so it was two spellings of one behaviour. The helper was deleted
  from the module rather than the row from the table.
- `P2_census_indirection_bypassed` swapped `census(cfg)` for a literal empty
  tuple, and `census` returns an empty tuple. Replacing a constant with an alias
  of itself, named in the learning as one of the three inert shapes. Replaced
  with `P2_census_returns_a_row`, which moves the value and kills 6.

## What a green suite still cannot see here

The membership half of an apply has no coverage because it has no code, and it
has no code because no unit in this build lands a collection reader. R-148 holds
that, with the mechanism: `write_tree_membership` refuses a caller supplied gates
factory and `session_lock` raises rather than nesting, so R-81's close condition
as written cannot be satisfied with that function as the `place`.
