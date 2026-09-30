# R-770 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/230`, in the foreground, one at a time. Null
control 0 on each, 10,949 collected against 10,949, no collect drift, every
restore verified against `git show HEAD`, the installation state unchanged
across every child.

**`r770-a.md`**, 8 rows: six over the switch and the splice's own refusal in
`intake/ingest.py`, one over the landing's pre-move check, one sample. 7
killed, 1 zero.

**`r770-b.md`**, 8 rows: four over the shared order and the landing shell in
`intake/land_cli.py`, four over what `intake file` refuses before the
database is opened. 8 killed.

**`r770-c.md`**, 5 rows: the rest of what `intake file` refuses before its
gate, what a failure past the gate says, and the playlist's name. 5 killed.

**`r770-d.md`**, 4 rows: the digest's collection half, the engine's
unresolved target, the gate's explicit flag, and the composite table a's zero
owed. 4 killed.

**25 rows, which is the cap. 24 killed, 1 zero, and the zero has its
composite.** Six rows were considered and not run. Each is named in
`r770-d-rows.toml` with the reason it ranked below the cap.

## The zero, and what holds the line instead

`S1_stub_listing_spliced`, table a, was the fixed sample: a guard the unit
did not write. `ingest.place_files` refuses a U22 stub listing with
`intake-export-is-stub`. Removing that refusal killed nothing on its subset
and nothing on the full suite, 10,949 collected.

Its composite is `S1_composite_the_splice_takes_a_stub`, table d. The driver
pairs rows only inside one batch, so the row carries no `pairs_with` and the
pairing is recorded here. It removes the same refusal one call later, inside
`collection_xml.splice_tracks`, with `place_files`' own left in place: **2
kills** on a four file subset, 108 collected.

Read together: the stub listing is refused, and the refusal that does the
work is the inner one. The outer one is a second copy that nothing
distinguishes from the first. Filed as R-779, not on the board bar, since the
path is guarded.

## Rows that were met before they were measured

Two rows would have been zeros on the suite as first written, and a reader
should know the tests that kill them were written for the table.

- **`C4`, a failure past the gate loses its remedy.** The test first raised
  `rekordbox-running` with `quit-rekordbox`, which is that reason's default,
  so a wrapper that dropped the remedy answered the same. It now raises the
  engine's own registry skew, `tree-unconverged` with
  `restore-from-snapshot`. 1 kill.
- **`C6`, the digest without the collection plan.** The only staleness test
  retagged the title, which moves both halves of the digest, so either half
  alone covered for the other. Two tests were added: the file's size moved
  under the same tags, which only the collection half sees, and the artist
  changed, which only the verb's half sees. `C6` is the first; the second is
  `D3`, considered and not run. 1 kill.

`B8`, the target spelled as resolved, is killed by the refusal of a file
outside the library and by a direct test of the spelling on a library
configured through a link. The drive through the dispatcher names the file
through a link on a library configured by its real path, where both
spellings agree, so it does not kill this row on its own.

## Why four tables

The driver pays two full suite runs before its first row, measured here at
about five minutes together, and a relay task runs it in the foreground
under a ten minute ceiling. Table a took 7 minutes 17 seconds with its zero
promoted to a third full run. The last nine rows were split five and four so
a promoted zero would still fit.
