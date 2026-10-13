# u138 mutation notes

Author's table, 15 rows, one batch `u138`, light pass over the session's age
rule, the verb that hands down who answered, the record's two new keys, the
new remedy, and two existing guards as a fixed sample (the terminal check
and the reason's exit code). 14 detected, 1 zero. The author ran it, so a
zero reads as "the author could not kill it".

- **S5_bound_exclusive, killed 1 on rerun.** Making the five day bound
  exclusive measured zero in the batch: through the dispatcher the verb reads
  the clock a moment after the backup fact is written, so the "exactly five
  days" case was a little over and `>` refused it too. A core test on one
  clock was added after the batch, a second under five minting and exactly
  five refused, and the same row measured again in `u138-rerun`.
- **S4_state_not_read, zero, user facing, composite S3.** Dropping the
  state check leaves the age check, and `backup_facts` gives a portion an
  age only when its state is known (`_age_of`: `age=delta if state is
  AgeState.KNOWN else None`), so on today's three states the two checks
  agree and the mutant is equivalent. Kept for a state added later that
  carries an age. S3, which stops refusing at all, kills 5.

**Stops.** The first start was refused on a red subset baseline,
`tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`,
at a load average of 17 to 18 with the feeder and the watcher running; it
passed alone three times of three and the rerun's baseline was green.
