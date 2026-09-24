# R-685, mutation notes

Two tables, sixteen rows, one pass, measured after the review round. The author's
own table, so every zero reads as "the author could not kill it".

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r685-a`, the loader and two verbs | 10 | 10 | 0 |
| `r685-b`, converge, the landing registry, the guard | 6 | 5 | 1 |

**Table A.** L1 is R-685's defect put back in the loader, a path nothing is at,
so every library routes by the shipped template. It kills ten, among them the
routing plan tests that write an edited or older active copy on the volume and
the landing test whose active copy declares no catalog tree. L2 to L7 each
revert one branch of the loader's narrow fallback or one remedy, and each is
killed by the loader test written for that branch.

**V1 and V2 are the verbs.** Each makes one verb parse the shipped text again,
the spelling the guard watches, and each is killed both by the guard and by a
behavior test through that verb. V2's composite, V2c, spells the same read as an
aliased default loader inside the function, and the landing test alone kills it,
so the verb is held by behavior and not only by the guard's spelling list.

**Table B.** C1 puts back the order the review found in `converge`, open the
database and then read the declaration, and C2 lets the loader's refusal escape
the try. The converge test kills both: its spy sees the open, or the verb raises
where it should answer NOT COMPARED. P1 makes `place_files` read the registry
again after the moves, and the landing's read count test kills it. G1 and G2 blind
the guard to aliases and to module attribute calls, and its self test kills both.

**G3, maintainer facing, zero promoted to 10149.** Every module is put on every
allow list, so the guard refuses nothing. On a clean tree the guard has no
offender to find, so nothing can die. What it holds is shown by V1 and V2, where
the guard is one of the killers of a real offender.

**Dropped, three rows, logged in `r685-b-rows.toml`.** V3 would repeat V1 for
set build, whose only holder is the guard, and no behavior test drives set build
over an edited active copy. O1 moves `label approved`'s read back after the
provider fetches. Its only cost is wasted network work, and a test would need a
refusing active copy and a counting provider. O2 makes `apply_export` read again
instead of taking the verb's declaration. The two reads agree unless the file
changes inside one invocation, which no test reaches.
