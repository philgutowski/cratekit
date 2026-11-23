# U953 M21, composite on the base

Row M21 (`_held_age` reads the full comparison's held key whatever key it is
given, so `full_check_age` answers the full comparison's age) killed nothing
on the full suite at `cf246284`. It has a user facing surface, the full check
age the backup verb and doctor show, so it is paired with the same defect
written into the base, `f281c688`, before the cut folded the two readers:
`full_check_age`'s `held[FULL_CHECK_KEY]` read as `held[FULL_COMPARISON_KEY]`.

Run by hand on a `git archive` of the base, with the 15 test files that name
`backup_facts` or `full_check_age`, two workers, `TMPDIR` on a high inode
directory: 181 failing or erroring ids on the clean base and the same 181
with the mutant, so **0 kills on the base** as on the branch. Most of those
181 are tests that need `rclone`, absent on this container, so a kill on the
Mac is not ruled out. The cut lost no kill here; the gap is the base's,
recorded as residual `u953-d`.
