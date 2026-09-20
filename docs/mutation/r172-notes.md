# R-172, the two mutation tables read together

Author run, 2026-09-20, on `relay/155` at `30aa77c`. Two tables, `r172-a.md`
over the plan pass that now owns a collision and `r172-b.md` over the apply pass
that now names what it did not do, run as two FOREGROUND batches because a Relay
session cannot wait on a background job and one 25 row invocation can pass the
600 second tool ceiling. Both tables are valid, every row's restore was verified
against HEAD, and each null control killed 0 of 9045 collected.

**25 rows, the cap, 25 killed. No zero.** That is the author's count and reads as
"the author could kill every row the author thought to write". The independent
tables in this repository's history found more than the author's every time they
were run.

Two rows kill only because the guard arrived with a test the author wrote for it
after the code review named the defect, said here so the 25 is not read as 25
guards the first suite covered:

- `A2_one_round_only` is the review's first finding reintroduced, the collision
  pass asking once instead of to a fixpoint. Its one killer,
  `test_a_target_a_collider_holds_is_held_back_too`, was written with the fix and
  was driven RED against a single pass before it went green.
- `B11_collision_step_always` is the review's second finding, the remediation
  telling a person to rename a file by hand over the four reasons that are not a
  collision. Its killer was written with the fix.

Two more rows measure guards whose tests were written in the same round and not
in answer to a review:

- `A7_targets_compared_exactly`, keyed through `_key` so two rendered names
  differing only in case are one name on the volume this product ships for. The
  fixture has to differ by more than case on disk, because a volume that ignores
  case cannot hold two names that do not.
- `A11_referenced_files_collide`, a file the collection references holding a
  rendered name it will never take. The cost is this unit's own with the sign
  reversed, a rename lost to a file that is not moving.

Twelve rows die to exactly one test. Each is one guard with one reason to exist,
and none was promoted to a full run because a death on a subset is a death.

`B15_reason_maps_to_ok` is the only row outside `write/naming_cli.py`. It maps
the new reason to a zero exit, so the envelope would say failed while the status
a script reads said fine, and its subset is 290 collected because the reserved
cause suite is in it.

## Considered and dropped at the cap

**None of these was measured.** Their reasons are in the two row files, and they
are `A6`, `A10`, `A12`, `A13`, `A14`, `A15`, `B10`, `B18`, `B19`, `B20`, `B21`
and `B22`. The shortest summary of the ranking: an existing guard far from this
diff is worth less than a new guard inside it, and a second row over the same
condition is worth less than the first.

## The hunts a green suite cannot see

- **Expected values from the code under test.** An AST walk over all 177 asserts
  in `tests/test_naming_apply_cli.py` returned 27 comparisons whose left side
  calls into the product. Every one compares against a literal or against a
  fixture's own filename, which is the input. None compares two calls into the
  code under test.
- **A test that forbids a feature by naming the last implementation's symbols.**
  `test_a_file_gone_after_the_plan_is_named_rather_than_skipped` monkeypatches
  the private `_plan_for`. If the verb stopped calling it, the file would never
  be deleted, no item would be outstanding and the assertion on the exit code
  would FAIL rather than pass vacuously. Checked by reading the fixture's
  failure direction, not assumed.
- **Duplicate keys in a mapping several branches appended to.** `REASONS` in
  `core/cause.py` is appended to by every unit. An AST pass over every dict
  literal in that file reports no duplicate string key.
- **One symbol meaning two things in two modules.** `incomplete` is this verb's
  totals key and its cause detail key, and `cli/setup.py:328` returns the string
  `"incomplete"` as a config migration state. The two never meet on one surface,
  and neither reads the other. `collides` is this verb's alone.
- **The first caller owns the engine's unreviewed failure paths.** This verb is
  the FIRST caller of `output.from_cause` outside `cli/__init__.py`, and the
  first anywhere to pass it a surface other than the diagnostic one together
  with a payload. Its paths were read as this unit's own: the schema argument is
  the documented way to name another surface, the code comes off the cause, the
  CLI boundary is appended once, and a reason mapped to a zero exit is caught by
  the envelope's own validator, which `B15` measures at nine deaths.
- **The same shape one file over.** Recorded in the closing note on R-172 and as
  R-559 to R-562. The tag write returning False was found this way and is fixed
  here; the rest are filed.
