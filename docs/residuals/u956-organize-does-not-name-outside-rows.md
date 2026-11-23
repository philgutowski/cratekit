---
title: crate organize approves the adoption digest without counting or naming the rows outside the library root
found: at the review of #1020, U956, 2026-11-23.
issue: no
---

**The mechanism.** `cratekit.organize.rekordbox._adoption` takes the adoption
screen from `apply_cli.digested` and shows its own counts (tracks read,
placeable, to file, vocal memberships to add), dropping the facts beside it.
So `organize.rekordbox.approve` binds the adoption digest, which since U956
covers the rows left outside the root, while its screen holds neither their
count nor their names. `adopt apply`'s own gate names them under
`outside_root`.

**Measured cost.** Driven by the round one reviewer: the organize gate showed
"tracks read 4, placeable 1, to file 1" and no word of the outside row.
Nothing false is said, since organize never showed excluded rows; a person
approving there is told less than at `adopt apply`.

**Closes when:** organize's adopt step counts the rows left outside the root,
or names them, beside its other counts, with a test. Ledger only.
