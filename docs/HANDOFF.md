# Handoff: where Cratekit stands

Written 2026-08-01 so a session with no memory of the build can pick it up.
Revised the same day, after the three pending branches merged and the U7
hardening landed.

## State

`main` carries U1, U2, U3, U4, U5, U6, U7, U10, U13, U14, U15, U31, U35, plus
the W1 through W6 hardening and the A4 whitelist addition. Pushed to the private
remote. 2602 passed, 76 skipped, ruff clean, `scan_repo` clean.

**There are no unmerged branches and no worktrees.** The wave that was pending
in the previous revision of this document is landed.

## What the last merge cost, because the pattern is the point

Four collisions, and every one of them passed the test suite. A clean auto-merge
is still not evidence of compatibility.

1. **Two rekordbox process guards that disagreed about Windows.** The writer asks
   pyrekordbox, which strips the executable suffix; the backup module asked the
   platform directly and matched the bare name, because it must work on a slim
   install with the rekordbox extra absent. Both reasons are good, so the
   duplicated MECHANISM stays. On Windows, where psutil reports `rekordbox.exe`,
   the backup guard saw nothing running and would have snapshotted a database the
   application was actively writing. `core/processes.py` now owns the one list
   and the one matching rule.
2. **Sixteen remediation tokens the canonical vocabulary had never heard of.**
   The conformance test named `config` alone, because config was the only module
   declaring its own `Remedy` on the day it was written. Four more landed and
   none was a subset, so every one of their refusals rendered as the exit code's
   generic summary: a user told to store a credential read "an unexpected
   failure". The test now derives the module set by walking the package.
3. **A `.venv` symlink committed pointing at an absolute path**, on a tree where
   `scan_repo` exited 0. Structural: every rule reads a file's CONTENT and a
   symlink has none, so it was skipped before any rule saw it. The scan now
   judges symlink targets, and `.gitignore` had the matching gap, since `.venv/`
   with a trailing slash matches a directory only.
4. **The pre-commit scan was running Python 2.7.** `entry: python` resolved
   through PATH to an old installer's interpreter, so the R1 secret and
   portability scan died with a SyntaxError instead of scanning. Pinned to
   `python3`. All 139 tracked files were scanned afterwards and were clean.

## Finish a merge like this

Merge one branch at a time, and after each one run the full battery on the
COMBINED tree before touching the next:

    .venv/bin/ruff check src tests scripts
    .venv/bin/python -m pytest
    .venv/bin/python scripts/scan_repo.py

Then hunt what a green suite cannot see. The two shapes this repository keeps
producing are a duplicate key in a mapping that three branches all appended to,
and one symbol meaning two things in two modules. For the first, parse the dict
literal and compare its key count against the runtime length, because every
other test iterates the runtime dict and is blind to a shadowed key. For the
second, walk the package and look for a name defined in more than one module.

**A note on worktrees.** Do NOT symlink `.venv` into a worktree. The editable
install names the MAIN checkout's `src`, so a worktree runs its own tests against
the main tree's package: a worker verifies code it cannot see and gets false
results in both directions. `pyproject.toml` now carries `pythonpath = ["src"]`
under `[tool.pytest.ini_options]`, which resolves from pytest's rootdir and fixes
it. Symlinking the venv is also what committed the `.venv` symlink above and
destroyed the real virtualenv when the merge replaced the directory with a
self-referential link.

## Where the reasoning lives

Everything that shaped these decisions is in the source repository, because it
quotes that system's paths and this repository's portability guard rejects those
by design:

- `DJ_tools/docs/plans/2026-08-01-001-feat-dj-product-reengineering-plan.md`, the plan
- `DJ_tools/docs/migration/00-SEAM-DECISIONS.md`, **authoritative** over any brief
- `DJ_tools/docs/migration/`, the six unit briefs and the wave prompts
- `DJ_tools/docs/runbooks/`, the U9 attended gate and its results
- `DJ_tools/docs/solutions/integration-issues/`, the A1, A3 and A4 verdicts

Read the seam decisions before implementing anything. Part 5 in particular is
seven failure shapes learned the expensive way, and they apply to every unit.

## What the U9 gate changed

**A1 is CLEAN, CONDITIONAL, and it moved a boundary.** rekordbox accepts,
renders, auto-analyses and stably keeps a database-inserted gridless row. The
single condition is `djmdContent.ContentLink`, which must equal the mode of that
column over the target library's live rows. pyrekordbox hardcodes `645482`, and a
row whose value differs renders and analyses perfectly and **cannot be loaded to
a deck**, so it fails at the gig rather than at write time. New-track intake can
therefore leave the XML bridge. KTD2 and R16 are rescoped in the plan.

**A4 is TOLERATED**, so `djmdKey` is in `PERMITTED_ROW_TABLES`. The permission is
a ceiling and not a licence: the writer may never author a key value, per the
decision recorded in the A4 solutions entry, and U21 is rescoped to it.

**A3 is INFERRED**, with no staleness check needed. The cross-check is deleted.

## What is blocked, and on what

U18, U20 and U21 were gated on U9 and are unblocked. U8 and U32 were gated on
the writer and are unblocked. U11 and U12 were gated on the job engine and are
unblocked.

`tests/_pending.py` is the register. Each entry names the unit that owes the
work, so a gate that cannot run today is a countdown rather than a hole.

## Open items that are not code

1. **The rekordbox application pin is deliberately not bumped.** The mechanism is
   correct and S2 is satisfied: an unset pin refuses, a drifted pin refuses and
   names its remediation, and the wizard may propose but only an explicit named
   decision records. The source system's pin is older than the installed
   application, so its writers refuse. Re-validating a pin against a real write
   is the author's deliberate act and never a number an agent edits.
2. **The vendored downloader has never been smoke-tested end to end.** Clone,
   install, authorize, download one track, confirm the file carries no tempo tag.
   That last check is the only end-to-end proof of the beatgrid patch, and the
   upstream wrote a tempo tag in three containers before it was patched.
3. **Two naming decisions are recorded rather than resolved**, because both are
   persisted-slug migrations rather than tidy-ups. `authenticate-provider`,
   `reauthenticate` and `reauthenticate-provider` may be one idea. `Decision`
   means two different things in `core/rb_writer.py` and `cli/gates.py`, and
   `FEATURES` means two different things in `cli/registry.py` and
   `modules/tools/__init__.py`.
4. **The ANLZ guard's honest gap is closed but worth knowing.** `read_anlz_files`
   is legal and returns live objects, so the name scan also forbids the tag
   setters, derived from the binding. The runtime half, comparing ANLZ
   modification times across a write session, is registered against U8.
5. `docs/residual-findings.md` carries nine recorded items with what closes each.

## Four verification gates need the library volume

Deferred by design, not dropped, per seam decision Part 4. Each is written
complete and gated on its fixture rather than deleted.

| Unit | Gate | Needs |
|---|---|---|
| U3 | parity against the live library's genre tag values | a fresh XML export |
| U4 | the parser handles every name shape in the live library | the same export |
| U31 | every active row in a snapshot resolves to a real file | a database snapshot copy |
| U7 | database integration, and both writers' dry-run paths | a database snapshot copy |

The conventions are `CRATEKIT_TEST_DB` for a database snapshot and
`CRATEKIT_TEST_REKORDBOX_SETTINGS` for a settings directory. Both SUBSTITUTE
rather than skip: the battery runs either way and a supplied fixture strengthens
it.

## Three hazards worth carrying forward

**Autoflush in the guard path.** Giving the cloud canary a real predicate turned
it from reading nothing into running a query, and an ORM query autoflushes: a
caller's pending write was flushed out of the session and the additive whitelist
approved a commit it could no longer see. The guard would have passed a forbidden
write *because* the canary started working. W6 removed the query at the root, and
W2 made the guard resilient rather than merely unflushed by reading the binding's
update buffer as well. `_no_autoflush` stays regardless: deleting the containment
because its current occupant left is how the next probe inherits the hazard with
the fix already gone.

**Inspecting a transient instance poisons the process.** Reading a not-yet-flushed
object through the object mapper forces mapper configuration, and a failed
configuration is CACHED process-wide, so every later mapper use raises including
in code unrelated to the guard. Catching the exception does not undo it. Read the
instance dictionary instead. This cost twenty-three database tests in files the
change never touched.

**Closing a database does not release it.** The binding closes the session and
leaves the engine's pooled connection open, so the process still holds the file
and both sidecars. Restoring over them then produces a disk I/O error against a
database that is perfectly intact, which is a terrifying message at exactly the
wrong moment. Fixed here by disposing the engine; still live in the source.
