"""The SQLite store this program keeps for itself: one connection, opened private.

The job queue and the review queue are both one database file in a private
directory, opened on the same pragmas, made owner only before the write-ahead
log exists, and written in immediate transactions. Each wrote that out for
itself until U298, and the two copies had already come to differ in one place
on purpose, what a mode that cannot be set means, which is the one thing a
store still says for itself here.

A module of its own, and not part of ``core.jobs``, so that the review queue
does not import the job engine to open a file: the reports package may
persist through ``core.review`` alone (R12), and what that module reaches is
what its guard has to be able to name.

Layer: core.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator

from cratekit.core import config
from cratekit.core.cause import name_the_database


def make_private(path: Path, own_only: Callable[[Path], None]) -> None:
    """The database AND its sidecars, because the log is where the data actually is.

    The suffixes come from the config module's declared set, never from a pair
    of literals here: a copy that forgets the write-ahead log leaves the
    store's real contents unprotected until the next checkpoint. ``own_only``
    is the caller's, because each store decides what a refused mode means.
    """
    own_only(path)
    for sidecar in config.SQLITE_SIDECARS:
        own_only(path.with_name(path.name + sidecar.suffix))


class PrivateStore:
    """One SQLite store this program keeps: its connection, pragmas and transaction.

    The job queue and the review queue are both this, each with its own
    ``_own_only``. ``synchronous=FULL`` and not the write-ahead log's default of
    NORMAL, which lets a commit be lost on a power cut: the commit that matters
    in the queue is the one flipping an item to done AFTER its artifact is
    durable, and in the review queue a verdict a person would be asked again.
    """

    #: Forces one file owner only. Set by each store.
    _own_only: Callable[[Path], None]

    def __init__(self, path: Path) -> None:
        self.path = path
        # isolation_level=None turns OFF the driver's implicit transaction
        # management, which is what makes BEGIN IMMEDIATE below the real thing.
        # Left on, the driver opens a DEFERRED transaction that takes its write
        # lock at the first WRITE, which is after the SELECT that chose the item,
        # and that gap is precisely how two drivers claim the same item.
        #
        # THE DRIVER'S ERROR CARRIES NO PATH AND NO ERRNO, so the whole opening
        # sequence is named. A store this account cannot open raises
        # ``sqlite3.OperationalError("unable to open database file")``, which is
        # not an ``OSError``, so every errno-shaped classification was blind to
        # it and the verb exited "this is a defect; report it". The pragmas are
        # inside the same block because a database on a read only volume
        # connects and then refuses the write-ahead-log pragma. The path is
        # recorded on the SAME exception, which is re-raised untouched.
        try:
            self.conn = sqlite3.connect(str(path), isolation_level=None, timeout=30.0)
            self.conn.row_factory = sqlite3.Row
            # The mode goes on BEFORE the write-ahead-log pragma, because SQLite
            # gives the log and shared-memory files the permissions the database
            # file has when it creates them. Doing it afterwards would leave two
            # umask-moded sidecars beside a correctly moded database.
            make_private(path, self._own_only)
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=FULL")
            # A concurrent writer holds the database for one small transaction,
            # so waiting is right and failing immediately is not. The busy
            # timeout is the difference between two processes serializing and one
            # of them raising "database is locked" at the user.
            self.conn.execute("PRAGMA busy_timeout=30000")
        except sqlite3.Error as exc:
            name_the_database(exc, path)
            raise

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    @contextmanager
    def immediate(self) -> Iterator[sqlite3.Connection]:
        """A transaction that takes the write lock UP FRONT.

        KTD8 says items are claimed in an immediate transaction, and this is why:
        a read-then-write under a deferred transaction lets two drivers both read
        the same pending row before either writes, and SQLite resolves that by
        failing one of them at COMMIT, after the work has already been decided.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield self.conn
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")


__all__ = ["PrivateStore", "make_private"]
