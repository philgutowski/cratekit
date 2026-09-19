# U72 mutation notes

Two tables, `u72.md` and `u72-b.md`, one light pass split in two so each driver
run finished inside the tool's 600 second ceiling. 24 rows, all killing, null
control 0 of 7837 in both, every restore verified against `HEAD`. This is the
author's table, not an independent one.

Every row is on a guard this unit added: the abort and empty plan branch, the
five fields of the plan digest one layer at a time, the gate's digest and the
registry's `digest_source`, the two defaults, where the intake file goes, each
field of the pending action (`blocks`, `verify_verb`, `kind`, `artifact`, and
its presence), the refused file warning and payload mark, the gate's shown
context, the empty folder check and its directory test, and the engine's new
public `listing`.

Three tests were added BEFORE the table ran, not in answer to a zero: an
answer given against one export, and one given for one folder, are each stale
for another, and staging holding only non-audio debris is a plan of nothing.
The digest's docstring claimed the first two and nothing held them.

`M23_listing_unfiltered` was zero on its derived subset, which is
`tests/test_landing.py` alone, and killed one test on promotion to the full
suite, the staging debris test in `tests/test_intake_land.py`.

One row dropped, `M25_option_equals_abort`: writing the branch as `option ==
"abort"` is equivalent under the two declared options, so no test can kill it.
