---
title: A mutation row on a part of the verb table derives the full suite as its subset
found: at the review of #977, U328, round one, 2026-11-23.
issue: no
---

**The mechanism.** A row with no `tests` of its own is given the test files
that import the mutated module (`mutate_table.derive_subset`). 91 test files
import `cratekit.cli.registry`; no test imports a part, since a verb is read
through the registry, so a row on `cli/registry_*.py` falls back to the full
suite.

**Measured cost.** Driven by the reviewer through `derive_subset`:
`cli/registry.py` gives 91 test files and each of the five parts the full
suite. The fallback is the safe direction, so no kill is missed; the cost is
a full run, about seven minutes on the cloud container, for each row a later
card writes on a verb's entry without naming its tests. Not timed on a real
row. The 35 replayed rows carry the tests their recorded kills name.

**Closes when:** `derive_subset` reads a part of a split module as its
module, the registry's parts by `cli/registry.py`'s own imports, or the rule
for a row on a part is written where rows are written. Ledger only.
