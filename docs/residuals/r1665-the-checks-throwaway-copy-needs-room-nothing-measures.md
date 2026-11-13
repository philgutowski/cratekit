---
title: The integrity check's throwaway copy needs room on the temporary volume that nothing measures, and a full one refuses the write as a failed check
found: at the review of #804, R-1665, 2026-11-13.
issue: yes
---

**The mechanism.** Since R-1665, `rb_writer.integrity_ok` copies the file set
it checks (the database, its log and index, the legacy playlist file) into a
private directory under the system's temporary directory and checks the copy,
so the capture itself is never opened. `snapshot.assert_room_for_capture`
measures only the capture store, on the library volume, so nothing asks
whether the temporary volume can hold a second copy of the database. When it
cannot, the copy raises, `integrity_ok` answers False with a log warning
naming the error, the capture records itself not verified, and every guarded
write refuses through `snapshot.assert_verified` with "did not pass its
integrity check" and the `report-defect` remedy. The true cause, no space on
the temporary volume, is in the log only.

**Measured cost.** Fails closed: nothing commits behind a capture that was
not checked, so no data is at risk. The review drove `snapshot.capture` with
the temporary directory on a 256 KiB tmpfs: the branch recorded the capture
not verified and refused, the temporary directory was left empty, and the
base recorded it verified. At verb level (`test_inbox_rotate` with the
temporary directory on tmpfs of 128 KiB to 800 KiB) base and branch failed and
passed at the same sizes, because SQLite's own temporary files already need
that much on the suite's small fixture. Whether a window exists on a full size
library, where the database is hundreds of megabytes and SQLite's own needs
are far smaller, is unmeasured; if it does, a DJ is told the capture failed
its check and to report a defect, when the disk is full.

**Closes when:** the room the throwaway copy needs is measured before the
capture and refused under the room slug with a remedy naming the temporary
volume, or the throwaway copy is placed on the store's volume and counted in
`assert_room_for_capture`, with a test that fills the temporary volume and
asserts the refusal names it. Earns an issue: a person is told something false
(board bar b) on the path every guarded write takes.
