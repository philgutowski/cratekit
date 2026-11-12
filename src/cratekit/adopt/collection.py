"""The collection reader: a rekordbox database becomes the rows the census walks.

THIS MODULE READS AND CANNOT WRITE, and that is a property of the code rather
than a promise in a docstring. Every open below goes through
:func:`cratekit.core.rb_writer.open_db` with ``require_closed`` left False, which
is that function's write-intent flag: a caller that wants to write says so, and
this one never does. Nothing here imports :mod:`cratekit.core.session`, nothing
calls ``commit``, and ``tests/test_adopt_collection.py`` asserts both by walking
this module's own syntax tree rather than by reading it.

WHY READING THE CONFIGURED DATABASE IS ALLOWED AT ALL, since the standing
constraint sounds absolute. It protects the live database against WRITES, and
against tests that can reach it. Three shipped verbs already read it through the
same gate: :mod:`cratekit.deletion.cli`, :mod:`cratekit.write.routing_cli` and
:mod:`cratekit.cli.converge`. What no test in this repository may do is reach the
configured one, so every driven test here builds a disposable database in a
temporary directory, or copies a supplied ``CRATEKIT_TEST_DB`` snapshot before
opening it.

TWO FUNCTIONS, AND THE SPLIT IS THE TESTABILITY DECISION.
:func:`collection_rows` takes an iterable of mapped rows and does no input of its
own, so every branch in the derivation is drivable with no database at all.
:func:`read_collection` is the thin half that opens a handle, hands the query
over, and closes. That is the shape
:func:`cratekit.write.routing_pass.content_rows` and
:func:`cratekit.deletion.library.read_collection` already use.

ONE NAME MEANS TWO THINGS AND THAT IS DELIBERATE, so it is said in both
directions rather than discovered. ``cratekit.deletion.library.read_collection``
takes ROWS and splits them into the live and the removed; this one takes a
CONFIG and returns the live collection. They are not interchangeable and neither
should grow the other's signature. :mod:`docs/METHOD.md` names this shape as one
to hunt for after a suite is green, so it is named here first.

Layer: modules. It reads configuration and the database and names no verb.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

from cratekit.adopt.scan import CollectionRow
from cratekit.core import config, locations, rb_writer
from cratekit.write import trees

#: Resolved absolute database path to the collection read from it. Populated by
#: :func:`read_collection` and cleared only by :func:`reset_cache`.
#:
#: WHY A CACHE AT ALL. ``cratekit.cli.handlers.run_job`` drives every item of a
#: job in ONE process, and both adopt workers need the collection per item.
#: Without this, a hundred item scan opens the database a hundred times and walks
#: the whole collection each time, which is the N times M shape
#: ``modules/reports/coverage.py`` records this repository shipping and removing
#: once already.
#:
#: WHAT IT HOLDS IS VALUES, NEVER A HANDLE. The handle is closed before
#: :func:`read_collection` returns, so nothing that can touch a database survives
#: in module state, and a cache somebody finds later cannot be turned into a
#: write by accident.
_CACHE: dict[str, tuple[CollectionRow, ...]] = {}

#: The same collection, indexed by content identifier. Populated beside
#: :data:`_CACHE` and cleared with it.
#:
#: WHY THE INDEX IS CACHED AND NOT ONLY THE ROWS. ``adopt.scan``'s worker runs
#: once per collection row and looks ONE row up, so building the index inside the
#: worker rebuilds it per item: N items times M rows, which on a library of fifty
#: thousand tracks is two and a half billion dictionary inserts across one census
#: that should have cost fifty thousand. The rows cache alone does not close it,
#: because what repeats is the indexing rather than the read.
_INDEX: dict[str, dict[str, CollectionRow]] = {}


def reset_cache() -> None:
    """Forget every cached collection.

    EXPLICIT RATHER THAN IMPLICIT, because a module level cache no test can clear
    is a cache that leaks one test's library into the next, and the leak reads as
    a passing assertion about rows the second test never created.
    """
    _CACHE.clear()
    _INDEX.clear()


def prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    """The configured volume rewrites, as the resolver's own type.

    BESIDE THE READER BECAUSE BOTH ADOPT VERBS NEED IT, and putting it in either
    verb would make the other one import a command-line module to reach it.

    THE FIFTH COPY OF THIS COMPREHENSION IN THIS TREE, and it is a copy rather
    than a shared helper because the four that exist live in
    ``write/routing_pass.py``, ``write/rebuild.py``, ``write/trees.py`` and
    ``deletion/run.py``, all of them other units' files. A helper in ``core``
    would be the right home and rewiring four modules to reach it is not this
    unit's change. Recorded rather than left for somebody to count.
    """
    return [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]


def genre_of(row: Any) -> str:
    """One row's genre display value, or the empty string.

    THROUGH THE BINDING'S OWN ASSOCIATION PROXY, never through a second join.
    ``DjmdContent.GenreName`` is an ``association_proxy`` onto ``DjmdGenre.Name``,
    so the binding owns the lookup and there is no second opinion to drift from
    it.

    A DANGLING ``GenreID`` READS AS NO GENRE, and the fusion is stated rather than
    discovered. Measured on 2026-09-02 against a disposable database built from
    the binding's own schema: a row whose ``GenreID`` names a ``djmdGenre`` row
    that does not exist returns ``None`` from the proxy without raising, which is
    indistinguishable from a row carrying no genre at all. Both answers reach
    :func:`cratekit.adopt.scan.classify_genre` as the empty string and both come
    back ``needs-genre``, so the fusion costs a person nothing here. It would cost
    something to a caller that wanted to tell a broken foreign key from a blank
    field, and no caller does.
    """
    return str(getattr(row, "GenreName", "") or "")


def collection_rows(rows: Any) -> Iterator[CollectionRow]:
    """Every collection row, as the four fields the census needs.

    A GENERATOR over the binding's own query, which is the natural shape for a
    whole-library read and the shape that punishes a consumer who walks it twice.
    :func:`read_collection` materializes it once; nothing else should walk it at
    all.

    A TOMBSTONE IS NOT DROPPED HERE. ``cratekit.adopt.scan.scan_rows`` skips a
    deleted row and says why, so dropping one here would be the same decision in
    two places, and the caller that wants to tell an empty library from a library
    of tombstones would have no way to.

    THE SOFT-DELETE MARKER IS READ, NEVER DEFAULTED, through
    :func:`cratekit.write.trees.soft_delete_marker`, which is this repository's
    one implementation of that read and now has a third producer.
    ``CollectionRow.deleted`` has no default on purpose and its comment gives the
    cost of supplying one: a producer that answers False for a row it could not
    ask hands every tombstone to the census as a live row, and adoption then
    proposes to put back a track the person removed on purpose. ``getattr(row,
    "rb_local_deleted", False)`` is the exact defect R-186 records one module
    over.
    """
    for row in rows:
        yield CollectionRow(
            content_id=str(row.ID),
            recorded=str(getattr(row, "FolderPath", "") or ""),
            genre=genre_of(row),
            deleted=trees.soft_delete_marker(row),
        )


def read_collection(
    cfg: config.Config, *, one_read: rb_writer.SharedRead | None = None
) -> tuple[CollectionRow, ...]:
    """The configured library's whole collection, read once and cached.

    THE OPEN IS A READ AND SAYS SO. ``require_closed`` is
    :func:`cratekit.core.rb_writer.open_db`'s write-intent flag, and leaving it
    False is the whole of what makes this a read. Everything the open side still
    enforces stays enforced: an unmounted volume is named as one, an absent file
    raises ``library-database-missing``, the binding pin is checked even on a
    read, and the cloud-sync canary and the schema pin both run.

    ``check_app_version`` IS PASSED FOR DOCUMENTATION AND DOES NOTHING HERE.
    ``open_db`` consults it only inside its ``require_closed`` branch, so on a
    read it is inert by construction. It is spelled anyway because a reader of
    this call should not have to go and find that out, and the mutation table
    records that no row covers it for the same reason.

    THE KEY IS ASKED FOR RATHER THAN ASSUMED, by ``open_db`` itself. A real
    library is encrypted and a disposable one is not, and either constant answer
    fails somewhere; see :func:`cratekit.core.rb_writer.unlock_needed`.

    THE HANDLE IS CLOSED BEFORE THIS RETURNS, in a ``finally``, through
    ``close_db`` rather than the binding's own close. That function's docstring
    records why: the binding leaves its pooled connection open, the process keeps
    holding the file and its write-ahead log, and everything works until a
    restore replaces those files underneath the live connection.

    ``one_read`` IS A READ ONLY REPORT'S ONE HANDLE (U267), read through and
    released rather than opened and closed here; it was opened with the same
    read intent, so the paragraphs above hold of it too.
    """
    target = rb_writer.live_db_path(cfg)
    key = str(Path(target).resolve())
    cached = _CACHE.get(key)
    if cached is not None:
        return cached

    handle = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            target,
            require_closed=False,
            check_app_version=False,
            cfg=cfg,
        )
    )
    try:
        found = tuple(collection_rows(handle.get_content()))
    finally:
        rb_writer.done_reading(handle, one_read)
    _CACHE[key] = found
    _INDEX[key] = {row.content_id: row for row in found}
    return found


def indexed(cfg: config.Config) -> dict[str, CollectionRow]:
    """The configured library's collection, keyed by content identifier.

    ONE INDEX PER PROCESS, for the reason :data:`_INDEX` gives. A caller that
    wants the rows in order asks :func:`read_collection`; a caller that wants one
    row by identifier asks this and does not build a mapping of its own.

    The returned mapping is the cached one rather than a copy, which is the same
    bargain :func:`read_collection` makes with its tuple: copying it per item
    would restore most of the cost the cache exists to remove. Nothing in this
    package mutates it, and a caller that did would be editing a cache rather than
    a library.
    """
    target = rb_writer.live_db_path(cfg)
    key = str(Path(target).resolve())
    if key not in _INDEX:
        # BUILT FROM THE ROWS RATHER THAN ASSUMED PRESENT AFTER THE READ. The two
        # registers are written and cleared together today, so a rows hit implies
        # an index hit and the subscript would always resolve. That is a property
        # of the current bodies rather than of this function, and the cost of it
        # ceasing to hold is a bare ``KeyError`` inside a job worker.
        _INDEX[key] = {row.content_id: row for row in read_collection(cfg)}
    return _INDEX[key]


__all__ = [
    "collection_rows",
    "indexed",
    "prefix_rules",
    "genre_of",
    "read_collection",
    "reset_cache",
]
