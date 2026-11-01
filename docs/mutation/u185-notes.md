# U185 mutation notes

25 rows, the light cap, measured on the branch at `e280a69` by `scripts/mutate.py`
with the container's 169 machine failures subtracted. 23 killed, 2 zero after
promotion to the full suite. Every zero reads "the author could not kill it".

Two rows were dropped at the cap and are logged in the row file: the two
`pending_objects` sources the review measured at zero, filed as a residual, and
the failing read at open, which a test asserts directly.

## The two zeros, each with what does hold it

`F6_delete`, a hard delete of a row in DEADCA7's folder. Zero because the
additive whitelist refuses every hard delete before this layer is asked:
`guard_violations` reports "deletes a row in 'djmdPlaylist'; writers are
additive-only" for any `session.delete`, and `assert_session_whitelisted` runs
ahead of `assert_foreign_untouched` in the same rollback. The composite is the
whitelist's own pinned refusal, `test_a_real_delete_is_refused_and_rolled_back`
in `tests/test_rb_writer_db.py`, plus the review's round two scratch drive of a
`session.delete` on a pushed playlist, refused with the folder intact. Not a
mutation row of its own, since the cap was spent.

`F10_difference_changed_row`, the second reading's changed column branch for a
playlist row. Zero because every touch the tests make is caught first by the
pending object leg, and a raw rename of the folder is refused by the same
reading as every row being gone, since a renamed root is no longer a foreign
root. Only a raw column change on a row below the folder reaches it, and no
test makes one. `G4_second_reading_leg`, which removes the whole second
reading, kills 2, so the leg is held; this branch within it is not. Both zeros
are the residual on guard layers covering each other.
