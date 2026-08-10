# U24 round 10, the mutation table

**Author written, and an author's table is a draft.** Every fix agent on this
project has run its table honestly and still missed guards its own round
created, because it mutates what it believes it changed. An independent verifier
runs one against this.

## How it was measured

* Driver: `mutate.py`, run synchronously in the foreground, one row at a time,
  from inside the worktree with its own `.venv`.
* The driver **never invokes git**. It snapshots each file's text in memory,
  rewrites it, restores it, and verifies each restore against a sha256 of
  `git show HEAD:<path>` taken in a separate shell step before the run. After
  the run, `git diff --quiet` confirmed the tree matches `HEAD` exactly.
* `PYTHONDONTWRITEBYTECODE=1` for every child process, and every `__pycache__`
  directory under `src` was removed before the first row.
* Counts from `pytest --tb=no`. Collected counts from
  `pytest --collect-only -o addopts=`. No row passed `-q`, which `pyproject.toml`
  already sets and which becomes `-qq`.
* **The collected count is reported on every row**, because a file that fails to
  COLLECT takes its tests with it and the run still looks green. It was 1206 on
  the baseline and on all 39 subset rows, with no exceptions.
* Subset: the nine test files that import `tombstone`, `deletion.stores`,
  `deletion.library`, `deletion.run` or `deletion.candidates`, which is
  `_pending`, `test_deferred_routing`, `test_layering`, `test_cli_contract`,
  `test_deletion`, `test_config`, `test_review_queue`, `test_tree_writer`,
  `test_tombstones`. Baseline 1206 collected, 1195 passed, 0 failed.
* A death on the subset is a real death. A zero on the subset was promoted to a
  full run before being reported as a zero.
* Scope: this round's own diff, plus a fixed sample of fourteen of U24's
  existing guards.

Full suite at the tip: 3504 collected, 3489 passed, 15 skipped.

## The rows

`deaths` is the count of tests that failed with the mutation applied. Every row
collected 1206.

### This round's diff: the row coordinate lookup

| id | deaths | what was reverted, and what it means if it kills nothing |
| --- | --- | --- |
| M1 | 1 | `_row_coordinates` accepts a `None` content identifier. A record whose payload names `null` would then name the row whose identifier is the string `None`, which is the `str(None)` shape this module has refused at three other doors. |
| M2 | 2 | `_row_coordinates` accepts a boolean. `str(True)` is `'True'`, an ordinary truthy name, and JSON carries booleans. |
| M3 | 1 | `_row_coordinates` treats a blank identifier as a name, so every record naming nothing shares one key with every row naming nothing. |
| M4 | 1 | The recorded path stops being composed to NFC. macOS hands out NFD and rekordbox stores NFC, so one path spelled two ways reads as two rows and the completed deletion is unrecognisable. |
| M15 | 1 | The `if coordinates is not None` filter is removed, so a record naming no row puts `None` in the set and every row that also names no row matches it. This is the record side of the same guard M3 is the row side of, and it is measured on its own because a guard covered by another guard is a guard nothing covers. |

### This round's diff: the identity scheme stamp

| id | deaths | what was reverted |
| --- | --- | --- |
| M5 | 10 | `identity_scheme` becomes the hand set constant it replaced, which is the instrument round 9 used and the one that goes silently wrong the first time a helper below it changes. |
| M6 | 1 | The digest drops the reader half, keeping only the composed identity. |
| M7 | 1 | The separator between probes is dropped from the digest. |
| M8 | **0** | `version_kind=kind or VERSION_IS_A_DESIGNATION` becomes `version_kind=kind`. **Promoted to a full run: 3504 collected, 3489 passed, 0 failed.** See the zero rows below. |
| M9 | 9 | The probe set is cut to its first row, so one branch is measured instead of twenty three. |
| M10 | 2 | The digest is truncated to two hex characters, so two schemes collide. A coefficient mutation, per the rule that a bound whose multiplier can be halved is not pinned. |
| M11 | 2 | `record_tombstone` stops stamping the era into the payload. |
| M12 | 2 | `summarize` stops emitting the era, so the listing cannot say why a tombstone missed. |
| M20 | 2 | The stamp prefix changes, so a stored stamp never equals a computed one. |
| M21 | 1 | The payload field is renamed, which is consistent inside this build and orphans the stamp in every store the previous build wrote. |

### This round's diff: the recogniser

| id | deaths | what was reverted |
| --- | --- | --- |
| M13 | 10 | No record is ever matched on its row, which is exactly the round 9 behaviour this round replaces. |
| M14 | 1 | Every record is matched on its row, so the stamp decides nothing. This is the row that makes the stamp load bearing rather than decorative: a row whose version column was edited after its deletion was recorded is read as already recorded, and the tombstone naming the version it claims now is never written. |
| M16 | 1 | A record of any kind at all contributes a row key, so a decline sitting in the tombstone store answers the tombstone question. |
| M17 | 10 | The row lookup is skipped for the row being asked about, which is the fix removed. |
| M18 | 1 | **B4.** `except Exception: return False` becomes `return True`, so a row nobody can identify reads as already recorded and a confirmed removal is retired for a file somebody merely renamed. |
| M19 | 1 | The recogniser stops counting revoked records, so revoking a tombstone re-opens a removal that was finished business. The docstring claimed this and nothing measured it before this round. |

### The fixed sample of U24's existing guards

| id | deaths | what was reverted |
| --- | --- | --- |
| E1 | 3 | `identifiable` reads an unaddressable row as addressable. |
| E2 | 23 | `version_of` composes a remixer as though it were a designation. |
| E3 | 2 | `ambiguous_versions` counts an absent code as a second recording. |
| E4 | 7 | `ambiguous_versions` refuses a convergence carrying one code. |
| E5 | 2 | `ambiguous_versions` folds the code as free text again. |
| E6 | 13 | `version_title` composes an empty bracket for every ordinary row. |
| E7 | 1 | `version_title` folds the untidied value while composing the tidied one. |
| E8 | 8 | `_already_carries` reads a featured credit group as a version group. |
| E9 | 2 | `removed_file_identity` accepts a boolean as a collection identifier. |
| E10 | 4 | `version_identity` accepts an identity with neither field. |
| E11 | 9 | `already_spelled_as_a_remix` tests the first word rather than the last. |
| E12 | 13 | `library._version_of` believes any `Subtitle` at all. |
| E13 | 2 | A confirmed absence is settled again even where a run already recorded it. |
| E14 | 3 | A row that can carry no tombstone is offered as an ordinary candidate. |

### The composites

Every zero row is paired with a mutation of the thing it guards, per the rule
that a prose argument is not evidence.

| id | deaths | what it shows |
| --- | --- | --- |
| C6 | 7 | The digest drops the COMPOSED identity and keeps the reader half. The composed identity is the load bearing limb; the reader half is added sensitivity on top of it. |
| C7 | 10 | The digest is fed nothing at all, separator included. The digest input is pinned; the separator alone is framing. |
| C8 | 1 | The probe version kind is forced to the artist branch. The field IS load bearing when its value can differ, which is what makes M8 an equivalent mutant rather than an unguarded line. |
| C16 | 11 | The kind test is inverted, so a version record is skipped. The kind expression carries the recogniser. |

## The zero rows

**One zero row out of 39, promoted to a full run.**

### M8, and it is an equivalent mutant

`version_kind=kind or VERSION_IS_A_DESIGNATION` becomes `version_kind=kind`.
Zero on the subset, zero on the full suite: 3504 collected, 3489 passed, 0
failed.

`library._version_of` returns an empty kind only on the path where it also
returns an empty version, since a believed column returns both together. With an
empty version `version_of` composes the same title through either branch, so the
mutant cannot produce a different identity for any input the reader can hand it.

**Paired with C8**, which forces the kind to the artist branch instead and kills
1: the field is load bearing wherever its value can actually differ. The `or`
default mirrors `library.read_collection`'s own, and having the two agree is what
keeps a future reader that starts returning a kind for an unbelieved column from
meaning two things in two places.

## Two rows in the first pass were defective, and are recorded rather than dropped

* **M9, first form.** It replaced the probe tuple with `(...) if False else
  (...)`, which evaluates to the full tuple, so the row was a no operation
  reporting zero. Rewritten as `_SCHEME_PROBES[:1]`, it kills 9. A mutation that
  does not mutate reports a zero that reads exactly like an unguarded line.
* **M15, first form.** It bypassed `_row_coordinates` on the record side
  entirely, so the row side's blank guard still caught the case and the row
  reported zero. Rewritten to remove only the `is not None` filter, it kills 1.

## Four zero rows were closed by fixtures rather than argued away

The first pass had eleven zero rows. Four were closed by writing the test the
guard was missing, which is the right response to a zero row:

* a record naming `null`, `true` or `false` is not a record naming the text those
  stringify to (M1, M2, M15);
* one path spelled NFD and NFC is one path (M4);
* a revoked tombstone still says a run recorded the deletion (M19);
* the stamp's payload field name and its VALUE are both wire formats and are
  both pinned to literals (M21, M6, M7, M10, M20).

The value pin deserves its own sentence. Every other assertion about the stamp is
an inequality under a monkeypatch, and an inequality survives any change that
moves both sides together, which is the exact shape that made four rounds of this
defect silent. Pinning the value is the only thing in the suite that can see it
move at all.
