# r923, the author's notes

Twenty rows against the row defaults unit, issue #267, measured on
2026-10-09 at `f8327f7`: nineteen killed, one zero, baseline green over
12,768 collected, the null control zero, the installation state unchanged
across every child. A first run at 03:03Z aborted on a state leak that was
not the batch's: four run records appeared in the real state folder during
the baseline from another session's `crate doctor` and a config restore.
Rerun with that session quiet. The table is `r923.md`.

**N9, zero, maintainer, expected.** `_fill` refuses when the field policy
answers anything but WRITE. Every column the plan names is NULL by the
staleness check that runs first, and the policy is fill if empty, so the
answer is WRITE for every planned column and the branch is unreachable by
construction. It stays because the two facts it depends on live in two
modules, and a later policy change would otherwise write silently or not at
all with no refusal naming why. No test reaches it and none should have to.

**N17, killed, expected zero.** The write handle opened without
`require_closed` was expected to survive, since `commit_guarded` re-checks
rekordbox at commit and the test only asked for a non OK exit. The review
pinned the refusal's reason to `rekordbox-running` and the record log to
empty, and the commit time refusal spells a different cause, so the pin
holds the open time check as well. A kill the review bought.

**N12, killed, promoted.** Dropping the written values from the digest was
expected to survive, since no test changes a default. The literal pin test
the review asked for does not, but the twenty one values are also in the
digest test's equality across a copy, and dropping them changed what two
plans share. One kill, from the full suite.

**N19, 31 kills.** A tempo in the defaults table is refused by the landing
suite, the guard suite and the repair suite alike, the same constraint held
from three directions.

**Confirm pass.** None needed: no row's old string moved after the fix
round, because the fixes were made before the table ran.
