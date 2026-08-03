"""Track deletion and tombstones (U24): the one operation that removes music.

Feature 37, and the only thing this product does that a user cannot undo by
running something again. Everything in here is shaped by that. The package is
seven modules and the split is by what each one can be wrong ABOUT:

* ``library`` reads the collection and writes nothing, ever (KTD15). Deletion is
  driven by rekordbox's own soft-delete marker precisely so the guarded writer's
  unconditional delete prohibition is never reopened.
* ``candidates`` decides, from the filesystem rather than from string comparison,
  whether a removed row's file is genuinely unreferenced (R37). It is pure apart
  from one injected ``stat``.
* ``trash`` performs the only destructive act R18 permits on a music file, and
  refuses when the volume has no Trash rather than falling back to an unlink.
* ``stores`` records declines and tombstones on the revocable decision stores
  U11 shipped, because R35 and R36 both say revocable and a private ledger would
  satisfy "remembered" and nothing else.
* ``watermark`` remembers how far this library has been read, bound to the
  database it was measured against, advancing only over what is finished.
* ``run`` is the order those are used in, and the order is the unit.
* ``tombstone_cli`` is ``crate tombstone list``, the one verb of this feature a
  person can reach today. R36 says a tombstone is listable AND revocable, and
  both words are about a person, so an engine that could do both while nothing a
  user could type asked it to satisfied neither.

HALF THE COMMAND-LINE SURFACE IS STILL MISSING, and that is recorded rather than
implied: ``tests/_pending.py`` registers ``cratekit.deletion.cli`` against U24,
which is this unit.

**THE REASON RECORDED FOR THAT ON 2026-08-02 IS STALE AND THIS IS THE
CORRECTION.** It said the wall was R34 and conformance 3: ``delete.review``
declares an EXPLICIT gate, conformance 3 drove the inline answer and then
required exit OK, so no explicitly gated verb could land. Main rewrote
conformance 3 and that wall is gone. Built and driven on a throwaway merge of
main, 2026-08-03: the verb refuses at its gate, refuses the inline answer without
recording it, takes the answer from a separate ``run decide`` act with its actor,
and resumes past the gate. Every act R34 asks for now works.

What stops it is the wall the stale note DENIED. This verb reads the collection,
so it cannot exit OK on a machine with no rekordbox database, and the conformance
fixture is such a machine: the drive ends at exit 22,
``library-directory-missing``. That is R-13's database wall, unchanged since it
was written, and it closes on a disposable database fixture rather than on
anything this package can do. The engine lands with its guards armed and the
review shell follows the fixture, not the gate.
"""

from __future__ import annotations
