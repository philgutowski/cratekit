# Live-fire findings from the DJ_tools staging repair, 2026-08-02

Seven things learned by repairing 1,357 collection rows on the author's real library
over one attended session. None of them are in any documentation, several contradict
what a careful reading of the schema suggests, and four bear directly on units Cratekit
has already landed or has yet to write.

Source of record: `DJ_tools/docs/plans/2026-08-02-001-fix-staging-collection-repair-plan.md`,
`DJ_tools/docs/runbooks/2026-08-02-staging-repair-progress.md`, and
`DJ_tools/docs/solutions/integration-issues/rekordbox-marks-missing-files-lazily-and-relocate-affordances.md`.

---

## 1. There are two `PIONEER/USBANLZ` trees and only one is the analysis store

**Affects U23 (adoption), U32 (restore and reconciliation), and the backup module.**

A rekordbox library on an external volume has two directory trees that both end in
`PIONEER/USBANLZ`:

| Tree | Key shape | Leaves | Size | Rows resolving |
|---|---|---|---|---|
| `PIONEER/Master/share/PIONEER/USBANLZ/` | UUID | 10,213 | 3.4 GB | **10,066 of 10,070** |
| `PIONEER/USBANLZ/` | `P0xx/XXXXXXXX` | 2,364 | 834 MB | **0** |

`djmdContent.AnalysisDataPath` is stored **share-relative** (`/PIONEER/USBANLZ/8d2/...`).
Joining it to the volume root resolves **zero of 10,070 rows** and reads as "the
analysis files are missing". The second tree is the USB-export cache, written when
rekordbox exports to a device, and it is regenerable.

This cost real time in DJ_tools twice. It was carried as a genuine open item ("sampled
rows have AnalysisDataPath values that do not resolve") when it was a measurement
artifact. And a rollback step written specifically to protect beat grids named the
wrong tree, so it would have backed up 834 MB of regenerable device output while
leaving every grid it existed to protect uncovered.

**For Cratekit:** anything that resolves, backs up, verifies or adopts analysis data
must join to `PIONEER/Master/share`. `modules/tools/backup.py` documents
`<target>/PIONEER/Master/master.db` and says nothing about the analysis share; worth
confirming the share is inside whatever the backup covers, because a database restored
without its analysis tree brings back rows without their grids.

## 2. pyrekordbox's `db_dir` is not the database

**Cratekit is currently clean. This is about staying clean.**

`Rekordbox6Database(db_dir=...)` does **not** open the database in that directory.
`db_dir` names only where it looks for `masterPlaylists6.xml`. The database comes from
`path`, and **when `path` is empty it falls back to the rekordbox config's `db_path`,
which is the live library.**

A call passing `db_dir` alone reads live while appearing to read a copy, returns
entirely plausible rows, and gives no sign anything is wrong. A DJ_tools probe shipped
that way and reported figures from the live database for hours under a docstring
promising it never touched it. What caught it was a contradiction: two snapshot copies
with different sha256 sums returning identical results.

The lesson generalises past this one API: **refusing the live path as an argument is
not the same as not reading it.** Check the connection that actually opened
(`db.engine.url`), not the argument that was passed.

`src/cratekit/core/rb_writer.py:1051` correctly passes `path=`. It is the only such
call in the repo today. A test asserting that every `Rekordbox6Database` call passes
`path=` would keep it that way; DJ_tools added one as an AST assertion.

## 3. rekordbox marks missing files lazily

**Affects U23 (adoption) and any reconciliation or convergence check.**

rekordbox does not stat every row on launch. It marks a track missing only when
something makes it look: rendering that row, loading it, or otherwise touching it. A
library can be arbitrarily broken on disk and show almost no missing markers.

Measured: 1,356 rows pointing at paths that did not exist, in a playlist that should
have shown 369 missing tracks, displaying **2**. And the markers reset on every
restart, so a fresh launch shows a clean-looking library that is still a thousand rows
broken.

**A missing-marker count is a measurement of what rekordbox has bothered to check, not
of what is broken.** Count from an XML export or from the database. Any convergence
check that samples the UI's notion of missing is measuring the wrong thing.

## 4. What a relocate actually writes

**Affects U23 and U31 if either ever repairs a path.**

Measured by diffing a snapshot taken before any relocate against one taken after
rekordbox itself relocated 43 rows. One table, `djmdContent`, four columns:

| Column | Change |
|---|---|
| `FolderPath` | full path **including the filename**, not a directory |
| `rb_file_id` | cleared to `0` |
| `rb_local_usn` | bumped |
| `updated_at` | set to now |

**Nothing else changes.** `contentFile`, `contentCue`, `djmdCue`, `djmdMixerParam` and
`djmdSongPlaylist` were row-for-row identical, and `contentFile`'s analysis paths were
byte-identical because they are UUID-keyed.

Two details that are easy to get wrong:

- **`FolderPath` holds the full path including the filename.**
- **rekordbox writes the `BaseDBDrive` name, not the volume's current mount name.**
  On the library this was measured against, the volume had been renamed years earlier
  and 8,554 rows still stored the original name; exports write the current one and
  rekordbox maps it back on import. A relocate writes the stored name. Derive the
  prefix from the library's own rows rather than hardcoding either spelling, or a
  repair silently splits the collection across two.

**Relocate edits the row in place.** It does not mint a new `UUID`, a new analysis
directory, or a fresh grid. The grid survives because it is addressed by `UUID` and the
sidecar's `PPTH` tag is basename-relative (`?/<name>`), so a move that preserves the
filename cannot invalidate it. Verified: 904 beats, same directory, same `PPTH`, before
and after. Delete-and-re-import is the thing that loses everything; relocate is not it.

## 5. The relocate affordances, and the one adjacent to disaster

Clicking a missing marker opens a **File is Missing** dialog with exactly three items:

    Auto Relocate
    Relocate
    Remove from Collection

- `Relocate` prompts for a folder, so the operator chooses the search scope.
- `Auto Relocate` resolves without asking, from folders learned earlier. **It does not
  fan out**: run on one track it fixes that track and nothing else.
- Both work on a **multi-selection**, but only when every selected row is already
  marked missing. A selection containing unchecked or healthy rows returns the ordinary
  context menu, which carries **no relocate option at all**. Combined with finding 3,
  this is what makes a bulk relocate laborious: every row must be rendered first.
- A batch relocate **stays inside the selection**. Verified across 43 rows: zero rows
  outside the intended set changed `Location`.
- **`Remove from Collection` is the adjacent menu item, one row below `Relocate`**, and
  it is enabled on a multi-selection. It is the only irreversible action in a path
  repair: it destroys the row, the `UUID` that addresses the grid, the `ContentID` that
  addresses cues, and every membership. Putting the audio file back recovers none of it.

The ordinary multi-select context menu also offers **`Analyze Tracks`**, which
regenerates beat grids. Any Cratekit documentation that walks an operator through a
rekordbox repair should name both of these before the operator gets there.

## 6. Whitelist membership needs pinning, not just negative assertions

**Affects `core/rb_writer.py` directly.**

Cratekit's guard tests assert what must **not** be in the whitelist
(`test_the_beatgrid_table_is_still_absent_from_the_whitelist`, `djmdGenre not in
PERMITTED_ROW_TABLES`) and that every entry is a real table. None asserts the **exact
membership**.

Those are different questions and only exact membership catches a widening. Adding a
table or a column is a two-word diff that raises the ceiling for every writer in the
repo, present and future, and it passes a green suite as long as it is not one of the
specifically-forbidden names.

DJ_tools hit this while scoping a path write, added exact-membership pins for
`DJMDCONTENT_WRITABLE_COLUMNS`, `PERMITTED_ROW_TABLES` and `BOOKKEEPING_COLUMNS`, and
verified the pin bites by sneaking a column in: 2 tests went red where the same edit
had previously passed 24 green.

`BOOKKEEPING_COLUMNS` deserves the same treatment for a subtler reason. Entries there
are **ignored** when judging a modification, so an addition does not grant a write, it
stops the guard from looking at one. Quieter and worse.

## 7. rekordbox 7.2.17 is validated for writes

`PINNED_APP_VERSION` in DJ_tools was bumped from `7.2.14.0323` to `7.2.17.0303` on
2026-08-02 after checking the two risks the pin names, against the live library:

- **Key rotated?** No. The database unlocked with the pinned key.
- **Schema migrated?** No. `djmdProperty.DBVersion` = `6000`, unchanged.
  `quick_check: ok`. pyrekordbox 0.4.4 unchanged.

Beyond the static checks, a real write: 1,313 rows re-pointed on a snapshot copy
through pyrekordbox 0.4.4, read back correct, then the same on the live library with
every grid, rating, cue and membership verified intact afterwards.

Cratekit's HANDOFF records its own pin as deliberately not bumped, and that posture is
right: the pin is the author's deliberate act. This is the evidence available when he
chooses to make it.

---

## Suggested residual-findings entries

If these are worth carrying in `docs/residual-findings.md` rather than only here, the
two with live consequences are:

- **The analysis share path.** Confirm every place Cratekit resolves, backs up or
  verifies analysis data joins to `PIONEER/Master/share`, not the volume root. Closes
  when U23 and U32 are written against the right tree and a test pins it.
- **Exact whitelist membership.** Closes when `PERMITTED_ROW_TABLES`,
  the content-column allow-list and the bookkeeping set each have an exact-membership
  assertion, verified to fail on a deliberate widening.
