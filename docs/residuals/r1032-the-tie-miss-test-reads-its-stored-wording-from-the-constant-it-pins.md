---
title: The test that the ledger's old tie misses are asked again builds the stored wording from the constant it pins, so a rewording of the constant's tail would leave them unasked with a green suite
found: at the second review of #329, R-1032, 2026-11-01.
issue: no
---

**The mechanism.** `test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
in `tests/test_organize_mirror_tie.py` writes its remembered miss from
`service.AGREEING_RELEASES`, and the adapter formats its reason from the
same constant, so the test cannot see the wording the live ledger actually
holds, which `main` at `f08defe` wrote from its own f string. The review
reworded the constant's tail to "of them agree with this row's artist and
title" on a copy and ran the five files that read it: 329 passed, none
killed. A full rewording is killed by three adapter tests, so only the tail
is unpinned.

**Measured cost.** None today: the review built `main`'s stored wording from
`f08defe`'s f string and the branch's constant is a substring of it, so the
4,304 tie misses of sitting 42 are recognised and asked again. The cost is
latent, a later rewording of the tail leaving every miss remembered under the
old words unasked and reported as remembered.

**Closes when:** the test stores its miss in `main`'s literal wording, the
words `f08defe` formatted, rather than from the constant. Ledger only: a
maintainer facing pin, after the unit's two fix rounds were spent.
