# U88 mutation tables, read

Two files, `u88.md` and `u88-b.md`, 25 rows in all over the guards U88 wrote:
the length reader, the long track planner, the apply step, the items and the
pending summary in `src/cratekit/write/routing_cli.py`, the add only writer in
`src/cratekit/write/trees.py`, and the `[long_tracks]` validation in
`src/cratekit/core/taxonomy.py` and the shipped template. Split so each batch
finishes inside one foreground call. One row was considered and dropped, logged
in `u88-b-rows.toml`: reading the intake keys alone instead of the whole
collection, which no single string revert expresses.

**21 of 25 rows kill. The four zeros are maintainer rows, each promoted to the
full suite by the driver, and every row's restore was verified against HEAD.**
These are the author's own tables, so a zero reads as "the author could not
kill it".

Every user surface row kills. L5, bypassing the planner's refusal of a root
FOLDER named like the playlist, killed nothing on its first run, because the
writer refuses the same node behind it and the warning still reached the
envelope. What it left was an offered plan naming additions the writer would
refuse. An assertion on the items was added to
`test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced` and `u88.md`
was measured again whole; L5 now kills one. The pairing row of the first run
was a single layer, not a composite, and is recorded as L7.

The zeros, one line each:

- **L7, the writer's own warning never surfaced.** Unreachable through the
  verb: the planner refuses the only node the writer would refuse and plans
  nothing, so the writer is not called.
- **A2, the writer called with nothing planned.** It then refuses the same
  folder again, and the result is a second copy of a warning the run already
  carries.
- **W2, the nothing new early return dropped.** The writer then re-emits the
  playlist it found, byte for byte, so the document does not change and the
  count stays zero.
- **W4, the insert writer's warning swallowed.** Unreachable after
  `root_playlist_members` has located the root and found no folder there, the
  only conditions `insert_root_playlist` refuses on.
