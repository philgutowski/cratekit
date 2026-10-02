# R-799 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/241` after both of the review's fix rounds, each
in the foreground and waited on. Every null control killed 0 of the full
suite, 12,053 collected against 12,053, every row's collected count equalled
its subset's baseline, every row's `head_verified` is true, and after each
table `git status` showed the table's own two files and nothing else.

| Table | Rows | Killed | Zero | Wall clock |
|---|---|---|---|---|
| `r799-a.md`, the loader, the rule for a folder's name, the resolver and the chooser | 10 | 10 | 0 | 398 s |
| `r799-b.md`, the correction's plan and its write | 9 | 9 | 0 | 342 s |
| `r799-c.md`, the record of a rewrite, the blank file and the verb | 6 | 6 | 0 | 330 s |

25 rows, the cap, one pass. No zero, so no composite was owed.

Three tables and not one, on R-821's arithmetic: a Relay session runs the
driver in the foreground under a 600 second ceiling. The machine was loaded
on this run, the suite took 79 to 119 seconds where it takes 61 to 67, and
the fixed cost of one invocation was about 300 seconds. The ten row table
finished 202 seconds inside the ceiling with no zero. One promoted zero
would have left it under 100.

Subsets, named on every row and not derived. Rows that mutate
`core/taxonomy.py`, `core/routing.py` and `tagging/published.py` ran
`tests/test_vocabulary.py`, `tests/test_published_genre.py` and
`tests/test_tag_remap.py`, 507 collected. Rows that mutate `tagging/remap.py`
and `tagging/remap_cli.py` ran `tests/test_tag_remap.py`, 92.

## The rows that die on one test

Five rows are held by a single test each. Each is a real death, and each is
one deleted test away from a zero.

- `P3_a_shops_genre_is_the_shops`. Killed by the test written while these
  rows were being planned. Before it, the only test of a record shop's later
  write used a word both sources file alike, so the row would have read zero.
- `P6_one_file_is_one_group`. Killed by the test of two cases of one file,
  which can only kill on a volume that folds case. On a volume that keeps two
  cases apart this row reads zero: resolving a path already folds `..`, `.`
  and links, so the file's own identity adds only case and hard links.
- `W1_a_file_is_read_again_before_it_is_written`, `W3_a_write_is_read_back`
  and `P11_blank_is_not_agreement`. One direct test each.

## What the cap dropped, and why each ranked below it

Thirteen candidate rows were written down and not measured. Each is in its
table's `dropped` list with its reason. The ones a reader should know about:

- The directory comparison that makes a folder typed in another case inside
  the library. Its count is a fact about the volume it ran on.
- A failed tag read taken for a blank genre. Never a write either way.
- The explicit gate in the registry. The conformance suite holds every
  explicit gate to refusing an inline answer.
- The digest covering the counts and the unread records. Two tests assert it
  moves, the family R-816's table measured.

## Not measured by any row

**The guard added after the tables.** The hunt found that a directory this
account cannot enter raised out of the plan, and the fix landed after the
one pass was spent. It has one test and no row.

**The shipped template's rows.** The driver mutates Python. The eleven rows
of the table, the alias and the map row are held by literals in
`tests/test_vocabulary.py` and by nothing here.
