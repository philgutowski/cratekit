---
title: Three guards of the import measure kill nothing, a plain import inside a function, a chain past a second handed module, and the drive formatting help
found: at the mutation table of #980, U331, 2026-11-24.
issue: no
---

**The mechanism.** Three rows of `docs/mutation/u331.md`, each on `scripts/refactor_measure.py` and each promoted to the full suite, read zero. M02 lets a plain `import cratekit.x` inside a function hand its module over, as if it were a top level import; the tests hold the same rule for a `from` import inside a function (M03, killed) and not for this spelling. M08 stops `Tree._reached` at the first module handed on, so a chain read past it is not followed further; no fixture reaches a module through two handed modules in one chain. M09 drops `parser.format_help()` from the script's `imports --drive`, which no test runs: the battery's own drive test in `tests/test_import_rules.py` formats help itself.

**Measured cost.** Maintainer facing. A regression in any of the three would let the measure read a reach off the list, or a dangling verb, as clean, while the battery's own rules, which share the reading, stay green over the same fixtures. Not driven against the tree: the measure reads 0 reaches off the list and 0 dangling verbs on the branch either way.

**Closes when:** a fixture test in `tests/test_refactor_measure.py` holds each reading, a lazy plain import, a chain through two handed modules, and a drive whose builder succeeds and whose help fails. Ledger only.
