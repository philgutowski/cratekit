---
title: The scope, origin and detail fields U953 folded into refusal helpers, and the full check's own age, are asserted by no test this container runs
found: at the mutation table of #953, U953, 2026-11-23.
issue: no
---

**The mechanism.** U953's table (`docs/mutation/u953.md`) broke each refusal
helper the cut wrote, and eight rows that change only a field the suite does
not read killed nothing on the full suite: the run scope or the origin of
every refusal from `tree_registry._refuse` (M1), `convergence._refuse` (M3),
`reconcile._refuse` (M4) and `restore._refuse_run` (M12); the writer's
default session scope in `rb_writer._cause` (M10); the detail key under which
`_row_removed` files a membership's or a node's id (M9); `read_lock_holder`
naming a holder from a record whose holder is an empty object (M25); and
`_held_age` reading the full comparison's held key for the full check (M21).
Each field was spelled at every call site on `main` and was unasserted there
too: the cut moved the literal into one place and lost no kill (the kill set
replay keeps all 364, and M21's composite on the base kills nothing either,
`docs/mutation/u953-m21-composite.md`). Three more zeros, M15, M18 and M24,
are equivalent mutants, since `internal-error`'s default remedy is already
report a defect.

**Measured cost.** Not driven to a person. A refusal's scope, origin and
detail travel in the JSON envelope a verb prints, and the full check age is
shown by the backup verb and doctor; a defect in one of them would pass the
suite. M21's tests mostly need `rclone`, absent here, so the Mac may kill it.

**Closes when:** a test asserts each refusal's envelope fields once per
helper, and one asserts that a full check age differs from a full comparison
age when the two held keys differ. Ledger only: no wrong value is produced
today.
