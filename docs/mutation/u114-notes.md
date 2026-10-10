# u114 mutation notes

Author's table, 25 rows, one pass, measured on head d3d8a32. 24 killed, 1
zero, promoted to the full suite of 12919. The author ran it, so a zero reads
as "the author could not kill it".

The unit writes a genre onto files and their rows, so the table is the full
light pass of 25 rows over the new guards: the rules that decide what is
suggested, the band and the threshold, the file half of the apply, the row
engine's narrow step, the kept catalogue answers and the stop after unread
rows. Five rows were considered and dropped, each with its reason in
`u114-rows.toml`.

- **M8_off_taxonomy, zero.** The off taxonomy flag on a catalogue answer is
  checked before the answer can vote, and removing the check kills nothing.
  A word the catalogue passes through is by definition one no declared table
  matched, so the `suggestable` check beside it already refuses it, which is
  what M9 measures and kills. Maintainer facing, kept as belt and braces in
  case a future tier marks a declared word as passed through.

Two guards in the file half of the apply had no test reaching them before
the table was written, a file that gained a genre after the gate and a write
the writer reported that did not read back. Both tests were added first, in
their own commit, and M15 and M16 are the rows that measure them.
