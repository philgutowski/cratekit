---
title: behaviour_compare.py capture of a revision that lacks a module the tree's test fixtures import fails every scenario
found: at the last merge of main into #854, U297, 2026-11-21, after both review rounds were spent.
issue: no
---

**The mechanism.** `capture --rev REV` runs the working tree's scenarios,
fixtures and `tests/conftest.py` against a copy of that revision's `src/`.
U295 landed while this unit was built and added an autouse fixture to
`tests/conftest.py` that imports `cratekit.cli.schedule`. A revision from
before U295 has no such module, so every scenario errors as its fixtures are
set up. The same holds for any revision that lacks a product module, or a
name in one, that the tree's conftest or a fixture a scenario imports reads.

**Measured cost.** Driven once on the final tree: `capture --rev 0f0f1032`,
the commit before U295's merge, ended `6 errors`, exit 1, with no scenario
recorded and no manifest, so `compare` refuses the directory. It is loud and
nothing is compared wrongly. A card that compares its branch with
`origin/main` after merging it is not touched, since that base holds
everything the tree's fixtures import, unless the card's own branch adds a
module and makes the suite's fixtures import it: then its base cannot be
captured with the branch's tests, and the comparison the card owes has to be
taken before that fixture is added.

**Closes when:** the script's docstring says a revision must hold everything
the tree's fixtures import and what to do when it does not, or `capture`
names the missing module in its own words instead of six errors. Ledger
only.
