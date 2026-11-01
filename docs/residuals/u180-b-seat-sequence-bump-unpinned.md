---
title: The order's write of updated_at outside the binding's tracking kills no test, so a second sequence bump per moved row would ship green
found: at the review of #361, U180, 2026-11-01.
issue: no
---

**The mechanism.** `placement.seat` writes a moved row's `Seq` with the
binding's registry tracking it, one sequence bump for the move, and stamps
`updated_at` inside `db.registry.disabled()`, as the binding's own
`move_playlist` does. Removing the `disabled()` block leaves every test green
(177 tests in five files, at the review), so nothing holds the write to one
bump per move.

**Measured cost.** None measured. A second bump per moved row is what a
person would pay only if rekordbox's cloud sync read the extra increment as
a second change, and that was not driven.

**Closes when:** a test reads the row's `rb_local_usn` before and after a
seat and holds it to one increment, or the bump count is shown not to matter
to rekordbox. Ledger only.
