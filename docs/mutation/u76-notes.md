# U76 mutation tables, read

Three tables. All are the author's own, not independent, and all were measured
by `scripts/mutate.py` on `relay/121`. They are batches rather than one table
because Relay runs every command in the foreground. A 25 row table can pass the
harness ceiling of 600 seconds, and `u90-a` to `u90-d` set that precedent.

**`u76-a.md`**, 13 rows at `72e32f1`, cover the duplicate sibling refusal at
each level, the merge itself, the name fold, the join of the caller's pairs and
the copy that makes a refusal write nothing. The null control killed 0 of 8121,
with no collect drift. 12 were killed on the first run.

**`u76-b.md`**, 12 rows at `72e32f1`, cover the extension of a held playlist,
the self closed folder and playlist, the folder count, the newest first
placement and the four checks that a merge point starts its own line. The null
control killed 0 of 8121. 11 were killed on the first run.

**`u76-zeros.md`**, the two zeros run again at `be19821` after a test was
written for each. They are the same two rows, so the count stays at 25. Both
were killed.

- `P1_join_pairs`, user facing. On the merge path a repeated pair finds the
  playlist the first one wrote and extends it, so the join is only visible on
  the write that CREATES the folder, and no test drove that path with a
  repeated name. Killed by
  `test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`.
- `X5_entries_absent`, maintainer facing, because rekordbox writes `Entries`
  on every playlist. Killed by
  `test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`.

The four own line rows, L1 to L4, were driven before they had a test. Each
refused correctly on a crafted shape, and
`test_a_merge_point_sharing_its_line_refuses_and_writes_nothing` was written
from those five shapes before the table ran.

25 rows in all, which is the cap. One more was considered and is logged as
dropped with its reason in `u76-b-rows.toml`: the held playlist's own line
check, the sibling of L1 to L4. It is pinned by the same test's held playlist
shape.
