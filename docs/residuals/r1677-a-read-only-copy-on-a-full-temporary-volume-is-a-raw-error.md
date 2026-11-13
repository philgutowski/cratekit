---
title: A read only diagnostic on a full temporary volume fails with a raw no space error and the remedy to report a defect
found: at the review of #813, R-1677, 2026-11-13.
issue: no
---

**The mechanism.** `rb_writer.read_only_copy`, through `disposable_copy`,
copies the database into the system's temporary directory for doctor, setup,
cutover, the collection export, favorites, shelve, the agreement check and the
rekordbox check. A full temporary volume raises the `OSError` from the copy,
which doctor's dispatcher renders as a check that did not complete with
`access_remedy(otherwise=REPORT_DEFECT)`, which answers `report-defect` for
no space (driven at round two). R-1677 measured and named the room
only for the integrity check's copy; these callers were left as they were.

**Measured cost.** Driven by the review: `doctor._survey_paths` with the
temporary directory on a 256 KiB tmpfs raises `[Errno 28] No space left on
device` from the copy. The rendering through doctor's dispatcher was read,
not driven. The message names the error, so nothing false is said, but the
remedy points at a defect rather than at the temporary volume. Predates this
card (R-372, R-1665).

**Closes when:** `read_only_copy` refuses a copy that found no room under
`snapshot-check-temp-full` or a sibling slug naming the temporary directory,
reusing `snapshot.check_had_no_room`. Ledger only: a remedy's wording on a read.
Two write verbs read through it first, `favorites.cli.read_pink_track_ids`
before a sweep queues and `cutover._one_root`, so a full temporary volume
stops them on the read with the raw error; they stop for a real reason, so no
write proceeds or is misreported and nothing is damaged.
