"""Read-only library reports: Feature Inventory rows 15 and 20, and their siblings.

What they share is that NONE WRITES TO THE LIBRARY: no database row, audio
file, XML or private ledger. Every report reads a rekordbox export through
:mod:`export`, which uses the byte locates of ``cratekit.write.rbxml``, and
nothing here opens the rekordbox database.

A question a person must ANSWER is a review item; a result a person READS is
output. So :mod:`duplicates` offers into ``review.Queue.DUPLICATES``, where a
REJECTED verdict is the persistent ignore, and :mod:`aging` returns a value.

Layer note: MODULES, gated by the ``duplicates`` and ``reports`` toggles (R5).
Nothing is imported here, so importing one report never imports another (KTD7).
"""
