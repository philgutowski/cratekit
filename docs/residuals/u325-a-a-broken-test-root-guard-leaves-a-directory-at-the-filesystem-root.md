---
title: A broken test root guard lets tests/test_config_test_root.py leave a directory at the filesystem root, and eight of its tests then fail on that machine in every later run
found: while measuring the kill set replay of #930, U325, 2026-11-23.
issue: yes
---

**The mechanism.** `tests/test_config_test_root.py` aims its writes at
`OUTSIDE`, a directory named `cratekit-r926-outside-every-test-root` directly
under the filesystem root, and asserts each is refused and that `OUTSIDE`
does not exist. When `core/config.py`'s refusal is broken, which is what a
mutation row on that guard does (the r926 rows, `u254.C3_append_test_root`),
the write lands: the directory is made at the root with a config file, a
ledger and two lock files in it, and nothing removes it. From then on the
eight tests that assert `OUTSIDE` is absent fail on that machine in every
run, whatever the tree. The mutation driver's state guard (R-343) watches
only the configuration and state roots, so it does not see the leak.

**Measured cost.** On the replay container it reddened the null control of
the next batch (eight deaths), and every row measured after it whose subset
held that file, or that was promoted to the full suite, read killed by those
eight tests alone. #855's base tables carry twelve such rows, U325's after
tables four, all measured again on containers that never had the directory.
The session could not remove it: a recursive removal at the filesystem root
is refused by the harness and needs a person, so the container stayed
unusable for those eight tests. On a Mac the same leak would land in `/`,
where an unprivileged run cannot write, so it shows on Linux containers run
as root.

**Closes when:** the tests aim at a directory a fixture creates under the
system temporary directory and outside the test root (still outside every
allowance the guard knows), or remove `OUTSIDE` in a fixture's teardown
whatever the test's outcome, and the mutation driver's state guard watches
for a new entry at the filesystem root. Earns an issue: it silently corrupts
every later mutation measurement on the machine, which is the kind of
apparatus defect the null control exists to catch.
