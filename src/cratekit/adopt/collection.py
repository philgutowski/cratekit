"""The collection reader: a rekordbox database becomes the rows the census walks.

IT READS AND CANNOT WRITE, by construction: every open goes through
:func:`cratekit.core.rb_writer.open_db` with its write-intent flag
``require_closed`` False, nothing imports :mod:`cratekit.core.session`, and
nothing commits. ``tests/test_adopt_collection.py`` asserts all three on this
module's syntax tree. Reading the configured database is allowed, as three
shipped verbs do; no test may reach it, so tests build a disposable one.

TWO HALVES: :func:`collection_rows` derives rows with no input of its own, so
every branch runs without a database, and :func:`read_collection` opens, reads
and closes. ``cratekit.deletion.library.read_collection`` shares the name and
takes ROWS, splitting live from removed; this one takes a CONFIG and returns the
collection. Neither should grow the other's signature.

Layer: modules. It reads configuration and the database and names no verb.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

from cratekit.adopt.scan import CollectionRow
from cratekit.core import config, locations, rb_writer
from cratekit.write import trees

#: Resolved database path to the collection read from it, cleared only by
#: :func:`reset_cache`. ``run_job`` drives every item of a job in one process and
#: both adopt workers read per item, so without this a census reads the whole
#: collection once per row. It holds VALUES, never a handle.
_CACHE: dict[str, tuple[CollectionRow, ...]] = {}

#: The same collection by content identifier, populated and cleared with
#: :data:`_CACHE`. The scan worker looks one row up per item, so building the
#: index per item would cost rows times items.
_INDEX: dict[str, dict[str, CollectionRow]] = {}


def reset_cache() -> None:
    """Forget every cached collection, so one test's library never leaks into the next."""
    _CACHE.clear()
    _INDEX.clear()


def prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    """The configured volume rewrites, as the resolver's own type.

    Beside the reader because both adopt verbs need it, and neither should
    import the other's command-line module to reach it.
    """
    return [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]


def genre_of(row: Any) -> str:
    """One row's genre display value, or the empty string.

    Through the binding's own association proxy ``GenreName``, never a second
    join. A dangling ``GenreID`` answers None without raising, which reads as no
    genre; both reach the census as ``needs-genre``, and no caller tells them
    apart.
    """
    return str(getattr(row, "GenreName", "") or "")


def collection_rows(rows: Any) -> Iterator[CollectionRow]:
    """Every collection row, as the four fields the census needs.

    A tombstone is carried, not dropped: ``scan_rows`` skips it, and a caller
    must be able to tell an empty library from a library of tombstones. The
    soft-delete marker is read through
    :func:`cratekit.write.trees.soft_delete_marker` and never defaulted, since a
    permissive default would hand every tombstone to the census as live (R-186).
    """
    for row in rows:
        yield CollectionRow(
            content_id=str(row.ID),
            recorded=str(getattr(row, "FolderPath", "") or ""),
            genre=genre_of(row),
            deleted=trees.soft_delete_marker(row),
        )


def _key(cfg: config.Config) -> str:
    """The cache key: the resolved path of the configured database."""
    return str(Path(rb_writer.live_db_path(cfg)).resolve())


def read_collection(
    cfg: config.Config, *, one_read: rb_writer.SharedRead | None = None
) -> tuple[CollectionRow, ...]:
    """The configured library's whole collection, read once and cached.

    THE OPEN IS A READ: ``require_closed`` is left False, and everything else the
    open enforces still runs (an unmounted volume, ``library-database-missing``,
    the binding pin, the cloud-sync canary, the schema pin).
    ``check_app_version`` is inert on a read and spelled so a reader need not
    look. The key is asked by ``open_db`` itself (R-239). The handle is closed in
    a ``finally`` through ``close_db``, which releases the pooled connection.
    ``one_read`` is a read only report's one handle (U267), opened with the same
    intent and released rather than closed here.
    """
    key = _key(cfg)
    cached = _CACHE.get(key)
    if cached is not None:
        return cached

    handle = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
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

    The cached mapping itself, not a copy, which nothing here mutates. Built from
    the rows when absent rather than assumed present after a read, so a change to
    how the two caches are kept is not a bare ``KeyError`` in a worker.
    """
    key = _key(cfg)
    if key not in _INDEX:
        _INDEX[key] = {row.content_id: row for row in read_collection(cfg)}
    return _INDEX[key]
