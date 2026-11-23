"""Track deletion and tombstones (U24): the one operation that removes music.

Feature 37, and the only thing a user cannot undo by running something again.
Split by what each module can be wrong ABOUT:

* ``library`` reads the collection and writes nothing (KTD15).
* ``candidates`` decides from the filesystem whether a removed row's file is
  unreferenced (R37); pure apart from one injected ``stat``.
* ``trash`` performs the only destructive act R18 permits, refusing rather than
  unlinking when the volume has no Trash.
* ``stores`` records declines and tombstones on the revocable decision stores.
* ``watermark`` remembers how far this library has been read.
* ``run`` is the order those are used in, and the order is the unit.
* ``cli`` is ``crate delete review`` and ``tombstone_cli`` is ``crate tombstone list``.
"""

from __future__ import annotations
