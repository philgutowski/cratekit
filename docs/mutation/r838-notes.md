# R-838 mutation table, read

Four batches, the author's and not independent, measured by
`scripts/mutate.py` on `relay/243` after the review's fix round, each in the
foreground with nothing else touching the tree. Split in batches only so each
driver run, with its full suite baseline and null control, fits one waited
command.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r838-a.md`, the unmark's narrowing and planning | 8 | 7 | 1 |
| `r838-b.md`, the unmark's digest, gate, recheck, stamp and failure | 8 | 8 | 0 |
| `r838-c.md`, the mark's record writes and the record's checks, plus U7 again | 9 | 7 | 2 |
| `r838-d.md`, R3 and R4 again | 2 | 2 | 0 |

Twenty four distinct rows, under the cap of 25, plus three re-measures.

**U7 killed nothing in batch a.** No test had the account stop listing a
playlist the pass marked, so dropping the `not-listed` branch let it fall
through to the title comparison unseen. Commit 26ad006 adds that test and
batch c measures the row again as `U7b_not_listed_rerun`, killed.

**R3 and R4 killed nothing in batch c.** R3 stamped the first entry the
record holds for a playlist under any pass, and no test had two passes mark
one playlist and then read whose entry was stamped. R4 removed the type check
on a mark's fields, which the emptiness check behind it shadowed for every
case the suite wrote. Commit b9b28d1 adds the read and a case whose fields are
all present with one not text, and batch d measures both again as killed.
