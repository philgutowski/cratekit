# U86 mutation tables, read

Two halves, `u86.md` and `u86-b.md`, 24 rows over the guards U86 wrote in
`src/cratekit/write/routing_cli.py` for `route inbox --export`, plus the one
writer the brief chose. Split in two so each half finishes inside one
foreground call. One row was considered and dropped, logged in `u86-b-rows.toml`:
the atomic write, which no test can observe short of killing the process mid
write and whose property belongs to `config.atomic_write_bytes`.

**19 of 24 kill. The 5 zeros are all maintainer surface, promoted to the full
suite of 7914 by the driver, and every row's restore was verified against
HEAD.** These are the author's own tables, so a zero reads as "the author could
not kill it".

Every user surface row kills. Two were added before the table ran, because
reading the guards showed nothing would kill them: the prefix map (E12) and the
verb's up front native tree refusal (E1), which the emitter guard behind it
answered with the same reason. Each layer of that refusal now has a test that
reaches it alone, and E1 and E2 each kill one.

The zeros, one line each:

- **E5, no PLAYLISTS section.** Covered by the next layer: `_inbox_keys`
  refuses `library-export-unusable` when the document has no playlist root.
- **E7, playlist nodes only.** A folder's track keys are its descendants'
  keys, which the walk reaches anyway, and the first seen dedupe drops the
  repeats, so reading folders too changes nothing observable.
- **E8, first seen dedupe.** The bridge writer deduplicates on insert, so a
  key named twice lands once either way. Only the item list would repeat it.
- **E13, absolute path condition.** A relative candidate is resolved against
  the working directory, and no fixture records one that exists there.
- **E24, intake as a direct child of ROOT.** No fixture holds a second folder
  of the intake name deeper in the tree, so the namesake the direct child rule
  guards against never appears.
