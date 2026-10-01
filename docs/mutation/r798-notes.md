# R-798 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/238` after the first review's fix round, each in
the foreground and waited on. Every null control killed 0 of the full suite,
11,505 collected against 11,505, every row's collected count equalled its
subset's baseline, and after each table `git status` showed the table's own
two files and nothing else.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r798-a.md`, the kind rule and the loader's guards on a published rule | 8 | 8 | 0 |
| `r798-b.md`, the asking, the listing's holds and the shared reader | 9 | 9 | 0 |
| `r798-c.md`, the hold record, `label held` and `label approved` | 8 | 8 | 0 |

25 rows, the cap, one pass. No zero, so no composite was owed.

Subsets, named on every row and not derived. Table a ran
`tests/test_label_genre_gate.py`, `tests/test_taxonomy.py` and
`tests/test_routing_parity.py`, 1,070 collected. Table b ran
`tests/test_label_genre_gate.py`, `tests/test_label_approved.py`,
`tests/test_label_offer_window.py` and `tests/test_label_workers.py`, 308
collected. Table c ran three subsets by the file each row mutates: 385 for
`core/review.py`, 804 for `label/held_cli.py`, 188 for
`label/approved_cli.py`.

## What the cap dropped, and why each ranked below it

Nine candidate rows were written down and not measured. Each is in its
table's `dropped` list with its reason, and each guard has a test that names
it.

- Table a: the branch for a taxonomy with no published rule, whose removal
  changes the sentence and not the verdict, and the reserved kind `any`, the
  same guard family as the kind's shape.
- Table b: three tracks at most, whose cost is requests and not a verdict, a
  hold whose words cannot be read back, whose removal raises, the reader
  refusing to ask a failing provider, the same rule as the measured reset,
  and the hold dropped when its release is filed.
- Table c: a grouping counting only holds in force, a kind checked against
  the taxonomy, and a release counted unjudged only when both rules lacked a
  verdict.

## What no row measures

The template. The driver's null control is a comment appended to a Python
target, so no row mutates `taxonomy.default.toml`. What holds its published
rules is `MEASURED` in `tests/test_label_genre_gate.py`, the catalogue's 27
top level words written out with the kind each must be, and one
parametrized test per word that a dance label passes the dance words and
holds every other.

The guards the second fix round added. They came after the pass and the cap
is one pass. Each has a test that names it: three releases unread in a row
ending the asking, the same count held across the labels of one sweep job, a
hold in force on a queued release dropped, `default` clearing a kind and
refused as the kind of a word, a share rule needle folded when loaded, and
an unreadable registry refusing approval before the provider is resolved.

## The second review round, and what `r798-d` is

The first three tables were measured after the first fix round. The second
round then moved one measured line and replaced the code under another. H7,
a release the library holds in full not being asked about, now reads
ownership off the one resolution of each release. K1, the first rule that
matches winning, now loops over the matcher both rule tables share.
`r798-d` is those two guards against the lines as they stand, each row
naming the one it measures again, and one row on the shared matcher itself:
3 rows, 3 killed, null control 0 of 11,512.
