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
which is this unit. ``delete.review`` declares an EXPLICIT gate; R34 makes an
explicit gate answerable only by a separate recorded act against the run, and
conformance 3 as it is written drives the inline answer and then requires exit
OK, so no explicitly gated verb in the registry can land until that assertion
answers a gate the way the product says a gate is answered. That is one wall and
it is not about databases: this verb writes files, opens no database with write
intent, and declares no database doctor check. The engine lands with its guards
armed and the review shell follows the wall coming down.
"""

from __future__ import annotations
