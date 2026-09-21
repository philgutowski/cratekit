# R-187 with R-188 mutation pass, notes

Issue #175, branch `relay/175`, 2026-09-20. Two tables, `r187-a.md` and
`r187-b.md`, rows files beside each. **Twenty five rows, all twenty five
killed, no zero.** The author's own table and no independent one, which METHOD
requires to be said here rather than implied: every number below is what the
author could kill, not what is killable.

Two tables rather than one to stay inside the harness tool ceiling. Batch B
took 2 minutes 56 seconds and batch A 3 minutes 24, each run in the foreground
and waited on, with nothing else touching the tree. Every row reports
`head_verified` true and `git status` showed no source file changed after
either run.

**The cap was reached and six rows were dropped for it.** They are logged at
the head of `r187-a-rows.toml` with the reason each ranked below the cap: the
refusal's first step listing displays instead of paths, the stamp built without
sorting, the cached text fields left unvalidated, the modification time dropped
from the identity, the `resolve_anchor` branch inverted, and two copies under
one comparison key resolving to the first.

## The shape of the pass

Batch A is the matcher and the named form, seventeen rows. Eleven in the
engine: the exact comparison removed, the whole-word rule removed,
`WORD_THRESHOLD` moved down to 50 and up to 95 so it is pinned from both sides,
the first of several holding hits taken, the partial flag never set, the
candidates left in walk order, the supplied key discarded on a partial reach,
an ambiguous name falling through to "not in your library", the score cutoff
at zero, and the partial message replaced by the several tracks sentence. Six
in the shell: a punctuation only name searched for, the listing uncapped,
`--named` outside the exclusive group, a key beside a name let through, an
empty name paying for the walk, and no cache path passed, which is R-188
itself.

Batch B is the index cache, eight rows: the size dropped from the identity, an
entry that is not a mapping accepted, a wholly empty read cached, a cache
written after an empty walk, the template stamp unchecked, a bool counted as a
number, a cached track that cannot be rebuilt counted as current, and a current
entry not carried into the next cache.

## What the table does not show

Every guard in batch B was written in the fix round, after the built in review
found the hole it closes, and its test was written with it. So each death says
the test can see the guard removed. It does not say the test would have been
written without the review, and six of those eight holes were on `main` in the
engine, dormant, under a green suite.
