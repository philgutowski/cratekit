---
title: When an edit makes an old import reachable from a verb, the import rules name the package holding that import and not the edit
found: at the review of #853, U296, round one, 2026-11-21.
issue: no
---

**The mechanism.** Rule four files each cause of a dangling verb under the
package that holds the import of a toggle's home. An import that no remaining
verb reaches is not a cause and is on no allowance. When another package then
imports that module at top level, the old import becomes reachable and is
reported as new, under its own package, and the import that made it reachable
is named nowhere in the failure.

**Measured cost.** The review added `from cratekit.sync import pair_discover`
at the top of `session/cli.py`; the only line reported was
`sync: dangling export cratekit.modules.outbound.mirror`, in a package the
edit did not touch. Three such latent imports stand on the tree today, two in
`cli` and one in `sync`. Maintainer facing: the author of the edit reads a
failure about another card's package and has to find their own import by
asking what newly loads the named module.

**Closes when:** the failure also names a verb that newly dangles and the
chain of imports from it, or the area cards have emptied the dangling
allowances. Ledger only.
