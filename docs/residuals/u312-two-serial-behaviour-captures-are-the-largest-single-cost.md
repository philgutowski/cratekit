---
title: Two serial behaviour captures are the suite's largest single cost and only the script can make them cheaper
found: at the build of #869, U312, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
runs `scripts/behaviour_compare.py capture` twice, one after the other, into
one `--root` so the paths agree, and the script refuses a root another capture
holds, so they cannot overlap. Each runs every scenario under
`tests/behaviour/` serially with `PYTHONDONTWRITEBYTECODE=1`. Measured on
`1fab8cbd`: 125 of the suite's 1,210 summed test seconds in one test.

**Measured cost.** Maintainer facing: about 10 percent of the suite's CPU.

**Closes when:** a card that may edit `scripts/` lets two captures of one
commit compare equal without serial runs into one root (a root per capture
with paths rewritten, or bytecode allowed under a private cache), or measures
that nothing cheaper holds the same promise.
