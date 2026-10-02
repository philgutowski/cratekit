---
title: A Row's Genre From Its File - Plan
type: fix
date: 2026-10-01
topic: row-genre-from-file
residual: R-816
execution: code
---

# A Row's Genre From Its File - Plan

## Goal

A verb writes a library row's genre from its file where the two disagree, the
genre and nothing else, so adoption and `crate report genres` read what the
files carry. The verb is `crate tag rows`.

## Problem

The source system's research pass of July 2026 split one genre folder in two.
It wrote the specific genre onto each file and moved the track in the playlist
tree, reading the live tag on disk by design, and it left the old word claimed
by no folder on purpose
(`DJ_tools/docs/plans/2026-07-08-002-feat-split-progressive-melodic-genre-plan.md`:
"the resort deliberately reads the live on-disk tag via each track's Location,
not the XML attribute"). The database rows were never reloaded.

Cratekit's adoption and its genre report read the row, so they see a word the
files no longer carry. No verb writes a row's genre from its file. `tag retag`
corrects the file and tells the person to reload the folder in rekordbox, and a
reload overwrites every tag field, which at sitting 26 changed keys.

### Measured, from the ledger

Taken on the author's library on 2026-10-01 and recorded in R-816. Not taken
again by this unit, which runs unattended and does not open the live database.

| Rows | Count |
|---|---|
| All rows | 10,272 |
| Agree with their file | 8,099 |
| Stale against a non blank file genre | 773 |
| Carry a genre the file does not | 1,233 |
| File not readable | 167 |

Of the 773: 630 say Progressive / Melodic where the file says Melodic House,
440, or Progressive House, 183. 136 are blank where the file says Melodic
House. 7 are other words.

## Key technical decisions

- **A new verb, `tag.rows`, and not a flag on `tag.retag`.** `tag retag` owns
  the file and asks a catalogue. This verb owns the row, asks nobody, and reads
  the whole collection rather than one folder. A gate is declared per verb and
  every declared gate has to fire, so a database gate asked in one mode only is
  a gate the registry cannot state. `adopt move` records the same reasoning.
- **The file is the authority in this direction only.** Nothing here calls a
  tag writer. The engine imports the tag reader and no writer, and a test holds
  the file bytes equal across a run.
- **The write is `GenreID` under the RETAG_GENRE policy that already exists.**
  `write.metadata.plan_genre_retag` builds the plan and
  `tagging.retag.apply_library` registers the policy, refuses a plan outside
  it, and applies it. Both have had no caller in `src` since U40 (R-185,
  R-246). This unit is their first caller and so owns their failure paths,
  which `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`
  states. `retag.plan_library` stays uncalled: it matches files a retag wrote
  to rows, the other direction.
- **A genre lookup row is linked and never created.** `resolve_genre_id`
  resolves the first active `djmdGenre` row by name, and `djmdGenre` is absent
  from the writer's permitted tables. A file word the library has no lookup row
  for is left alone and counted as `genre-unknown`. On the author's library
  both target words already have rows, because tracks imported since July
  carry them.
- **Unreadable is kept apart from blank.** The file is read with
  `tags.read_tags_checked`, so a container that would not open counts as
  `file-unreadable` and a file that opened with no genre counts as
  `file-blank`. The lenient reader folds both into None, which is METHOD's
  first defect pattern.
- **Every row lands in exactly one outcome**, and the totals carry every
  outcome zero filled:

  | Outcome | Meaning |
  |---|---|
  | `agree` | row word equals file word |
  | `write` | they differ, the file's word has a lookup row, the row is written |
  | `file-too-coarse` | they differ, the file's word is too coarse per the taxonomy and the row's word is specific |
  | `genre-unknown` | they differ, and no active lookup row carries the file's word |
  | `file-blank` | the file carries no genre |
  | `file-unreadable` | the file's tags could not be read |
  | `file-missing` | the path resolves and no file is there, which is also what an unmounted volume looks like |
  | `path-unmapped` | the recorded path is under no prefix rule |
  | `no-path` | the row records no path, or one that does not decode |

  A tombstoned row is skipped and not counted, as the genre report skips it.
- **Too coarse protects a specific word only.** A file word the taxonomy calls
  too coarse does not replace a row word that is non blank and not too coarse.
  When the row is blank or itself too coarse, the file's word is written: the
  row is no worse and now agrees with the file.
- **The plan lists every differing row.** Items are every row whose word
  differs from a non blank file word, each with the row's word, the file's
  word, and its action: `write`, or `leave` with the reason. Rows whose file is
  blank, missing or unreadable are counted by reason and not listed.
- **The digest covers the items and the outcome counts, and nothing copy
  specific.** Content id, row word, file word, action, reason and target genre
  id per item, plus the counts. No database path, no state path, no timestamp.
  A rehearsal on a disposable copy of the database, with library state
  redirected by `library.state_dirname`, digests equal to the live plan when
  the rows and files are the same, which is what the session's rehearsal rule
  compares.
- **The verb keeps no ledger.** Its plan is derived from the database and the
  files on every run. A rehearsal that goes past the gate on a copy writes a
  session record, a capture and a fingerprint, all under the redirected state
  directory, and nothing a live run reads as done.
- **Synchronous, on the order `adopt move` keeps, with the plan on a read
  handle.** The backup acknowledgment is read before the plan is built and
  before the gate (R-733). The plan is made on a handle opened to read and
  closed before the gate. The gate is explicit, answered by a separate
  recorded act (R34), and bound to the plan's digest. An empty plan still
  asks, and a plan that writes nothing is then a no op. Only `apply` over a
  plan that writes opens the database with write intent, which is where a
  running rekordbox refuses. The second invocation rebuilds the plan from the
  database and the files, and the gate refuses `decision-stale` when the
  digest moved. That is how one file changing between plan and apply refuses
  the apply.

  *Changed while building.* The first draft kept `intake land`'s order: the
  database opened with write intent before the plan, and an empty plan asking
  nothing. The conformance suite holds every declared gate to firing, its
  fixture carries no pin a write open would accept and no stale row, and the
  set of gates exempt from that rule is pinned with the words "a fourth one is
  a decision, not a diff". So the verb follows the three siblings that ask on
  an empty plan, and its gate is reached by the conformance drive with no
  exemption.
- **The write handle checks each row is still as the plan read it.** The plan
  and the write are on two handles, so before the capture is taken the engine
  reads each row to be written and refuses `decision-stale` when its genre
  moved or it stopped being a live row. Nothing is written for any of them.
- **The session spine is called, not rebuilt.** `session.assert_gates` with a
  kept record and the analysis watch over `analysis_store.watch_roots`, a
  verified capture attached to the record, the commit witness, and
  `rb_writer.commit_guarded`, whose whitelist admits `GenreID` because the
  policy is registered and nothing else on the content table.
- **The read back is from SQL, after the commit, and checks two things.** Each
  written row's `GenreID` resolves to the file's word. And every column of each
  written row is compared with a snapshot taken before the write: only
  `GenreID` and the binding's ten bookkeeping columns may differ. A beat grid,
  a tempo or a BPM moving would refuse here by name, after the guard already
  refused it before the commit.
- **Module `repair`, as `tag.retag` is.** Correcting metadata the library
  already holds is a second job a person opts into.
- **A person reads the summary without asking for JSON.** The gate screen
  carries the outcome counts and the most common word pairs as facts in front
  of the items. The applied run and the empty run each carry one warning line
  with the counts, because the default renderer prints nothing from a plan
  payload's totals.

## Implementation units

### U1. The engine: plan every row against its file

`src/cratekit/tagging/rows.py`. `plan_rows(cfg, db, declared)` walks
`db.get_content()` once, resolves each live row through `trees.located`, reads
the file's genre, and returns a `RowsPlan`: the items, the outcome counts, the
word pairs, the `metadata.Plan`, and the digest.

Tests: every outcome in the table from a row and a file made for it. Row and
file agree is not in the plan. A Deep House row with an Electronica file is
left alone. A blank row with a too coarse file is written. A tombstone is not
counted.

### U2. The engine: apply, and read back

`apply_rows(cfg, db, plan, analysis_roots=...)` in the same module. The spine,
the snapshot of the planned rows, `retag.apply_library`, the guarded commit,
the session record, the fingerprint, the read back.

Tests: planned, written, read back. Every other column of a written row is
unchanged. No file byte changes. A row the policy would skip is reported and
not counted written. A commit that raises records no commit.

### U3. The verb and its gate

`src/cratekit/tagging/rows_cli.py` and one appended registry entry, `tag.rows`.

Tests through the real dispatcher: the two acts then the write, a declined
gate writes nothing, no acknowledgment refuses before the gate, a file changed
between plan and apply refuses `decision-stale` with nothing written, a second
run after a clean one asks and is a no op, an empty plan never opens the
database to write, the plan is read with rekordbox open and the write refuses,
a row on a volume that is not mounted is counted and the run does not fail,
and after the run `report genres` no longer names the old word.

### U4. `tag retag` stops sending a person to a reload

`tagging/retag_cli.library_row_warning` names `crate tag rows`. The docstrings
in `tagging/retag.py` and the registry that say nothing calls the database
half are corrected, and the test that pins "nothing calls them" is narrowed to
what is still true.

### U5. The record

The mutation table under `docs/mutation/`, the ledger, `RESTART-cratekit.md`,
and `CONCEPTS.md` if a word needs it. R-816 stays open: it closes on the
attended run recorded in `docs/cutover.md`.

## Verification

- The test file for each unit while building, then the full battery on a
  committed tree: ruff, pytest, `scan_repo.py`.
- `/code-review` on the branch, at most two fix rounds.
- A mutation table capped at 25 rows over the new guards: each outcome's
  branch, the too coarse rule, the tombstone skip, the acknowledgment read, the
  gate, the policy registration, the read back's two checks.

## Out of scope

- Writing any file.
- The 1,233 rows that carry a genre their file does not.
- Moving a track between folders, which adoption owns.
- Creating a genre lookup row.
- The run on the author's library, which is owed to an attended sitting.
