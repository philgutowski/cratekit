# U89 mutation tables, read

Two files. `u89.md` is the table, 23 rows over the guards U89 wrote: the
shared loader and the tagging default in `src/cratekit/write/metadata_cli.py`,
the inbox apply, the export plan and apply, the resort worker and resume in
`src/cratekit/write/routing_cli.py`, the rebuild worker and resume in
`src/cratekit/cli/rebuild.py`, the convergence report in
`src/cratekit/cli/converge.py`, and the gap rule and the required keyword in
`src/cratekit/write/rebuild.py`. `u89-e6.md` is one confirming row, below.
Nothing was dropped; the table sits under the cap of 25.

**21 of 23 rows kill on the first run. The one user surface zero, E6, was
turned into a death by a new test and confirmed in `u89-e6.md`, killing one.
The remaining zero is a maintainer row.** Every restore was verified against
HEAD by the driver. These are the author's own tables, so a zero reads as "the
author could not kill it".

The zeros, one line each:

- **E6, the vocal writer's per folder warnings dropped.** User facing: a
  folder the emitter refused read the same as one that already had its sub.
  Its producer is a FOLDER of the vocal name where the playlist belongs.
  `test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served`
  drives it through the verb, and the confirming row kills 1 of 115.
- **R2, `rebuild_governed_tree` given back its None default.** Maintainer
  facing and zero by construction: every caller now passes the keyword, so a
  default nothing reaches changes no behaviour. The guard is against the next
  caller, which no test of today's callers can be.
