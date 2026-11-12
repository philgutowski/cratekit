---
title: Two repair rows tests pass or fail by where ext4 places pytest's temporary directory
found: at the mutation table of #692, U263, 2026-11-12.
issue: no
---

**The mechanism.** `test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`
in `tests/test_repair_rows.py` writes a file in its temporary directory and
needs that file's inode above the bound of 2,000,000, the premise of a
volume whose counter has run past it, and
`test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`
needs the opposite of a fresh file there. On ext4 an
inode number follows the block group of its parent directory, which the
allocator chooses, so on a Linux container the test passes when pytest's
temporary root lands in a high group and fails when it does not.

**Measured cost.** On this container the test failed alone on the base
commit `6febd202` and on the branch, then passed on the base in a full run
twelve minutes later; it reddened one mutation driver baseline and killed
one null control, each an invalid batch. Pointing `TMPDIR` at a directory
whose inode was 3,744,431 made the first pass three runs in three, and
then reddened the second in the next driver baseline. So no temporary
directory holds both green on this container. Not seen on the
Mac, whose APFS hands out inodes from one counter.

**Closes when:** the test makes its premise rather than reading it from the
filesystem, by giving the row an id known to be the file's identity above
the bound. Ledger only.
