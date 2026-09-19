# U90 mutation tables, read

Four files, measured by `scripts/mutate.py` on `relay/135`. There are three
batches because the driver pays a full suite baseline and a full suite null
control on every call, and a relay task runs every command under a 600 second
foreground ceiling. Each batch took 4 to 6 minutes.

- `u90-a.md`, the range guard and the parser, 7 rows, 7 killing.
- `u90-b.md`, what the hand path writes and reports, 8 rows, 8 killing.
- `u90-c.md`, the one reader and the fit's report of what it replaced,
  6 rows, 5 killing.
- `u90-c5.md`, C5 again after a new test answered its zero, 1 row, killing 1.

**21 rows over the unit's new guards, under the cap of 25. 20 of 21 kill on the
first run. The one zero, C5, was a user surface. A new test turned it into a
death, confirmed in `u90-c5.md`.** Every restore was verified against HEAD by
the driver, and every null control killed nothing. These are the author's own
tables, so a zero reads as "the author could not kill it".

The zero, one line:

- **C5, the one reader returns the stored threshold as written instead of the
  checked float.** User facing, promoted to a zero over the full suite of 8015.
  Its producer is a hand edited file carrying `"threshold": "5.0"`, which the
  reader accepts. Mutated, the record carries text, so the calibrate report's
  number format and every tagging comparison meet a string. Before this unit
  `load_vocal_threshold` returned the float directly, so nothing tested the
  conversion once the record came back whole.
  `test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`
  drives it through the reader and the hand cut's report. The confirming row
  kills 1 of 119.

Two rows were considered and dropped, logged in `u90-b-rows.toml`. B9 drops
`gender_margin` from the writer, and nothing in `src` reads that field. B10
rewords the out of range message, which is maintainer facing wording, and the
guard behind it is measured by A1 to A5.
