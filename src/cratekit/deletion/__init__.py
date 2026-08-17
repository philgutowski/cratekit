"""Track deletion and tombstones (U24): the one operation that removes music.

Feature 37, and the only thing this product does that a user cannot undo by
running something again. Everything in here is shaped by that. The package is
eight modules and the split is by what each one can be wrong ABOUT:

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
* ``tombstone_cli`` is ``crate tombstone list``.
* ``cli`` is ``crate delete review``, the gated half: offer removals, then
  trash the confirmed files. The conformance fixture substitutes a disposable
  database so the verb can exit OK after R34's two acts.
"""

from __future__ import annotations
