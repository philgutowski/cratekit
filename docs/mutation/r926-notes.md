# r926, the author's notes

Fifteen rows against the test root guard, issue #270, measured on
2026-10-09 at `8c41ca3`: fifteen killed, no zero, baseline green over
12,836 collected, the null control zero, the installation state unchanged
across every child. The table is `r926.md`. The author's table, so a zero
would have read as "the author could not kill it", and there is none.

**The brief's verification.** The live `config.toml` in the installation's
config directory read modification time 1791515018 (2026-10-08 23:03:38,
the restore) before the first edit of this branch, after every full suite
run on it, and after this table. No folder named for the outside path the
tests aim at exists at the filesystem root afterwards.

**P1, 19 kills, the brief's path resolution mutant.** `config_path`
answering a folder outside every temporary root is what a missed redirect
looks like from the writer's side. Every save it reached was refused, and
no byte landed, because the system volume is read only and the guard runs
before any directory is made.

**C2, 30 kills.** The conftest never registering a root is the state the
2026-10-08 probe ran in, applied to every test. The configuration is
refused everywhere and the temporary allowance keeps the primitives' own
scratch writes alive, which is why the count is thirty rather than every
test that saves.

**G6, one kill.** The lock check alone is killed only by the lock test,
because every lock in the four files is taken under a path the other two
call sites already check. It is the check that covers a lock a module
takes directly, the routing pass and the adoption revert among them.

**G9 and G10, subset of two files.** The provider gate tests are the ones
the review round measured writing a session token under a mkdtemp folder,
so they are the subset that proves the temporary allowance, and both rows
kill eleven there.

**Confirm pass.** None needed: the rows were written after the review's
fix round, against the committed text.
