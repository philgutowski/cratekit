# U121 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `fable/278-set-inspiration-playlist`. Every row's subset
was `tests/test_set_inspiration_playlist.py`, with `tests/test_taxonomy.py`
beside it for the taxonomy row and `tests/intake/test_set_fetch.py` for the two
fetch rows.

**`u121.md`**, 25 rows at `575bfa7`, null control 0 of 12,875, no collect
drift, every restore verified against `git show HEAD`. 17 killed, 4 zero, each
promoted to the full suite and still zero, 4 refused because the review's fix
round had moved their text before the driver ran.

**`u121-b.md`**, 6 rows at `e9f8354`: the four refused rows retargeted and the
three zeros measured again against the tests they bought. Null control 0 of
12,878. 5 killed, 1 refused, the separator row again, because the rows file
written through a shell heredoc carried the two dashes as characters where the
source carries them as backslash escapes.

**`u121-c.md`**, 1 row at `1c6a0ae`, the separator row written through Python
with its escapes as text. Null control 0 of 12,878. Killed, 2.

**`u121-d.md`**, 6 rows at `3c00531`, the guards the watcher's review round
added: the recorded playlist read and checked live (D1, D6), a removed
namesake not written into (D2, 3 kills), a repeated row counted once (D3), no
record on a rerun that added nothing (D4), the left list carried when nothing
is written (D5). Null control 0 of 12,885. All 6 killed.

31 distinct mutations in all, 25 in the author's first pass under the cap of
25 and 6 for the watcher's round: **30 killed, 1 zero**. Five
more were considered and logged as dropped in `u121-rows.toml`: the
`--set-date` regex refusal and the page date's month (the parametrized refusal
test pins both and S5 measures the same unnamed surface), the undeclared folder
refusal (a traceback on `node.display` follows the dropped line, a death that
says nothing about the rule), the suppressed row's own left word (no test
queues a suppressed row), and `page_of`'s string check (the page tests pin it,
the same family as S18).

## The one zero

- **S16, a near match claims the staged file.** User facing: the rule is that a
  row resolving only to something close claims nothing. The mutation widened
  the tie from `MATCHED` to anything but `MISSING` and killed nothing, and a
  probe under `tests/` said why: a staged "One (Extended Mix)" resolves for a
  set wanting "One" as `needs_review`, `version-differs`, **with `paths` empty**.
  The candidates ride in `candidates`, not `paths`, so the mutated line had no
  path to tie and the row is an inert mutation, not a test gap. What the guard
  does hold is measured by S17 (5 kills, a downloaded row tied to nothing is
  listed and not dropped) and by
  `test_a_row_that_resolves_only_to_a_different_version_is_not_guessed`, which
  passes on the tree and would fail if any path reached the member.

## What the first table's zeros bought

Three rows were zero in the first table and killed in the second, each after a
test:

- **S15, members in title order.** Inert on the first suite because every set
  until then played its tracks in alphabetical order, One, Three, Two, so a
  sort by title changed nothing. `test_members_keep_the_sets_order_when_it_is_not_alphabetical`
  plays Two, One, Three. 1 kill.
- **S14, the backfill writes a plan whose digest moved.** The gate re-plans on
  every drive and compares digests, so the moved collection test was refused by
  the gate whether or not the engine's own re-plan on the write handle ran. A
  guard held by another guard is a guard nothing covers, so
  `test_the_engine_refuses_a_plan_whose_collection_moved_even_with_no_gate_in_front`
  calls `inspiration_cli.written` directly. 1 kill.
- **S10, a removed folder is written into.** The same shape: the landing's gate
  re-plans too, so the gone folder test never reached `_folder_row`.
  `test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front`
  removes the folder on the open handle and calls `write_members`. 1 kill.

## What the kills say

The name is held from every side: the uploader taken off the title (S1, 2) and
its separator with it (S2c, 2), the flag winning over the page (S4), a missing
word refused (S5, 6), the padding of the day and not the month (S6, 10). The job
is held to a finished set (S7, S8). The folder is held to one row (S9) and the
playlist to the folder and to its own name (S13, 2). A landed member is found by
its target (S11, 6), a set of no members writes nothing (S12, 2), a downloaded
row tied to nothing is listed (S17, 5), and a person's review answer is read
back (S3). The page reaches the job (S18, S19). Both verbs refuse a bridge tree
(S20r, S25r) and the backfill reads the acknowledgment before its gate (S24).
The landing writes the set in its commit (S21, 6) and names it on the record
(S22), and the taxonomy validates the declared node (S23).
