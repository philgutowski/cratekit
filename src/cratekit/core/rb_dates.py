"""Every date the binding reads off a row is one it can place (U285).

pyrekordbox converts stored UTC text to naive local time, and DEADCA7's
``0001-01-01T00:00:00Z`` falls before year 1 west of UTC, failing the whole row.
:func:`install` wraps that conversion once, from ``rb_writer.open_db``, so a stamp
past the calendar's edge reads as :data:`FLOOR` or :data:`CEILING`. It writes
nothing, never hides an error that is not the calendar's edge, and never writes
a bound back as a ``masterPlaylists6.xml`` Timestamp.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Callable

#: A day inside the calendar, so every zone can convert it back.
FLOOR = datetime(1, 1, 2)
CEILING = datetime(9999, 12, 30)

#: Marks a wrapper, so a second install is a no op.
_MARK = "_cratekit_placeable"

_YEAR = re.compile(r"\s*(\d{4})-")

#: The only ValueError text answered as a bound; any other parse error is raised.
_PAST_THE_EDGE = {FLOOR: "year 0 is out of range", CEILING: "year 10000 is out of range"}


def _edge(value: str) -> datetime | None:
    """The bound a stamp at the calendar's edge reads as, by its own stored year, else None."""
    found = _YEAR.match(value) if isinstance(value, str) else None
    if found is None:
        return None
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)))


def placeable(convert: Callable[[str], datetime]) -> Callable[[str], datetime]:
    """``convert`` answering :data:`FLOOR` or :data:`CEILING` at the calendar's edges."""
    if getattr(convert, _MARK, False):
        return convert

    def string_to_datetime(value: str) -> datetime:
        try:
            moment = convert(value)
        except (OverflowError, ValueError) as exc:
            edge = _edge(value)
            if edge is None:
                raise
            if isinstance(exc, ValueError) and str(exc) != _PAST_THE_EDGE[edge]:
                raise
            return edge
        if moment.tzinfo is not None:
            # Not what the pinned binding answers; an aware value is not comparable to a bound.
            return moment
        return min(max(moment, FLOOR), CEILING)

    setattr(string_to_datetime, _MARK, True)
    string_to_datetime.__wrapped__ = convert  # type: ignore[attr-defined]
    return string_to_datetime


def keeps_bounds(update: Callable[..., None]) -> Callable[..., None]:
    """The binding's XML node update, never writing a bound as a Timestamp."""
    if getattr(update, _MARK, False):
        return update

    def wrapped(
        self: Any,
        playlist_id: Any,
        parent_id: Any = None,
        attribute: Any = None,
        updated_at: Any = None,
        lib_type: Any = None,
        check_type: Any = None,
    ) -> None:
        if isinstance(updated_at, datetime) and updated_at in (FLOOR, CEILING):
            updated_at = None
            if parent_id is None and attribute is None and lib_type is None and check_type is None:
                return None
        return update(self, playlist_id, parent_id, attribute, updated_at, lib_type, check_type)

    setattr(wrapped, _MARK, True)
    wrapped.__wrapped__ = update  # type: ignore[attr-defined]
    return wrapped


def install() -> None:
    """Wrap the binding's date conversion and its XML node update, once per process."""
    from pyrekordbox.db6 import aux_files, tables

    tables.string_to_datetime = placeable(tables.string_to_datetime)
    aux_files.MasterPlaylistXml.update = keeps_bounds(aux_files.MasterPlaylistXml.update)


def installed() -> bool:
    """Whether the binding's conversion and its XML node update are the wrapped ones."""
    from pyrekordbox.db6 import aux_files, tables

    return bool(
        getattr(tables.string_to_datetime, _MARK, False)
        and getattr(aux_files.MasterPlaylistXml.update, _MARK, False)
    )

