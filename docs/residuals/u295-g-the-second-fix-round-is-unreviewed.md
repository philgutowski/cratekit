---
title: The second fix round of U295 was not reviewed
found: at the record of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** Both fix rounds were spent. Round two reviewed `767ffa84..6cca323c`; the commit after it, `69765ae4`, was not reviewed. What to read: the agent's PATH built from `binaries.find` over the installable binaries, `read_agent`'s new checks (carried directories present and absolute, the log inside the carried state, the name of the crate), `show` refusing root, the summary's environment filtered to names this build carries, and the structural test's launcher names.

**Measured cost.** None measured; the unit's own tests and the mutation table cover the commit.

**Closes when:** a review of `6cca323c..69765ae4` reports nothing that holds.
