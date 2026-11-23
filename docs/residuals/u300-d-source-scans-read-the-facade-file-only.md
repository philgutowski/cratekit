---
title: Guards that scan the split modules by file or by module name do not read their parts, so a forbidden shape in a part passes them
found: at review rounds one and two of #857, U300, 2026-11-22.
issue: yes
---

**The mechanism.** U300 split `core/rb_writer.py`, `core/session.py` and
`core/restore.py` into parts that each module re-exports. Guards that scan a
module's own file, its `inspect.getsource`, or an import of its exact dotted
name read the module and not the code that moved to its parts. The two review
rounds drove each by injecting the forbidden shape into a part: it failed the
guard on the base and passed it on the branch.

- `tests/test_rb_writer_guard.py`: the writer raises no bare `RuntimeError(`
  or `SystemExit`, and `_raised_reasons`' scan of the refusals the writer
  raises, both over `rb_writer.py` alone; the soft-delete guard does not
  resolve the parts' call-time spelling `_writer().SOFT_DELETE_COLUMN`.
- `tests/test_cli_contract.py`: the writer never learns the gate's name or a
  flag string, over `rb_writer.py` alone.
- `tests/test_sync_night.py`: the night module may not import
  `cratekit.core.session`, matched with a following dot, so
  `cratekit.core.session_holders` and its siblings pass.
- `tests/test_config.py` and `tests/test_process_guard.py`, one scan each.

U300 kept what it could inside its own files: the one part function raising a
slug `_raised_reasons` reads went back into `rb_writer.py`, the parts read the
soft-delete column as `rb_writer.SOFT_DELETE_COLUMN` from a local binding,
which the soft-delete guard resolves (a permissive read written that way in a
part is caught), and the restore and session scans in `tests/test_restore.py`
and `tests/test_write_session.py` read the parts. The files above are not
U300's: `tests/test_rb_writer_guard.py` no card may edit, and the rest are on
other cards' lists.

**Measured cost.** None today: the reviews grepped every part for each scan's
forbidden text and found none, and five of the driven injections are still
caught by a wider guard. The cost is a guard on a path that writes or deletes
that kills nothing for code in the parts (board bar (d)): a permissive read
of the soft-delete marker on the removal path written in the parts'
`_writer()` spelling, or the unattended night job taking the library lock
through `session_holders`, would pass the guard written to stop it.

**Closes when:** each scan reads its module and its parts (by glob of the
module's file name, or by every module whose dotted name starts with the
module's own), the soft-delete guard resolves a call-time accessor, and the
night ban matches the parts. The writer guard file needs Phillip's leave to
change, since no card may touch it.
