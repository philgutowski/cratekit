---
title: Eleven of the layer ladder's 21 placed modules can move one layer with tests/test_layering.py green, and five of them name no file
found: at the review of #853, U296, round one, 2026-11-21.
issue: no
---

**The mechanism.** U296 moved the ladder's named modules from alternations
inside three patterns to one line each in `_PLACED`, answering as before for
every module. What pins a placement is the parametrized list in
`test_every_planned_module_has_a_layer` and the real package's own imports,
and neither covers every line: `types`, `output`, `match`, `identity` and
`cli.envelope` are planned names with no file, and six more are not on the
parametrized list and would not break an import one layer away.

**Measured cost.** The review moved each of the 21 lines one layer in turn
and ran the file, 50 tests collected each time: no test failed for
`cli.envelope`, `cli.exit_codes`, `cli.prompt`, `core.identity`,
`core.locations`, `core.match`, `core.output`, `core.restore`, `core.secrets`,
`core.tombstone` and `core.types`. Carried from `main`, whose alternations
this table equals; the one line per module table makes it visible. Maintainer
facing: a wrong placement of one of those is caught only when an import
crosses it.

**Closes when:** each placed module that exists is on the parametrized list
and the five that name no file are removed or built. Ledger only.
