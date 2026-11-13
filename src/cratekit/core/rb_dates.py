"""Every date the binding reads off a row is one it can place (U285).

rekordbox stores ``created_at`` and ``updated_at`` as text at UTC. The pinned
binding, pyrekordbox 0.4.4, parses the text in ``tables.string_to_datetime``
and answers ``astimezone()`` of it made naive: the moment in this machine's
local time. DEADCA7 0.2.3 stamps its folder, its playlists and every membership
it pushes with ``0001-01-01T00:00:00Z``, read on a real push at sitting 98.
West of UTC that moment in local time falls before year 1, so the conversion
raises ``OverflowError``, the whole row fails to load, and any verb that walks
the playlist tree through the binding (organize's report, converge) failed
INTERNAL over the first push.

THE ONE SEAM. :func:`install` wraps the binding's conversion once per process,
from :func:`cratekit.core.rb_writer.open_db` before the binding is made, so
every handle Cratekit opens, on the database or on a copy, reads the same way.
The binding's ``DateTime`` column looks the function up in its module at every
row it reads, so a wrapper installed after an earlier query is still the one
called; a test pins that through a real handle.

WHAT IT ANSWERS. A stamp the conversion places at least a day inside the
calendar is answered exactly as the binding answers it. One it cannot place,
because local time would fall before year 1 or after year 9999, or one it
places within a day of either end, is answered as :data:`FLOOR` or
:data:`CEILING`. Both are naive like every other value the binding answers,
and both are a day inside the calendar, so a reader that converts them again
(``astimezone()``, ``timestamp()``) cannot overflow in any zone. So the zero
date reads as :data:`FLOOR` in every zone, west or east.

WHAT IT NEVER DOES. It writes nothing: a read value is the object mapper's
committed state, and an attribute nobody assigns is never in an update, so the
stored text stays exactly what the other app wrote (and U185's guard refuses
any write to its folder anyway). It never hides an error that is not the
calendar's edge: text the binding cannot parse still raises its own
``ValueError``, and an ``OverflowError`` from a stamp whose year is neither 1
nor 9999 is raised as it came.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Callable

#: The earliest moment answered: a day inside the calendar, so every zone can
#: convert it back.
FLOOR = datetime(1, 1, 2)
#: The latest moment answered, a day inside the calendar's end.
CEILING = datetime(9999, 12, 30)

#: Set on the wrapper, so a second install is a no op rather than a wrapper of
#: a wrapper.
_MARK = "_cratekit_placeable"

_YEAR = re.compile(r"\s*(\d{4})-")


def _edge(value: str) -> datetime | None:
    """The bound a stamp at the calendar's edge reads as, else None.

    Read off the stored text's own year, so the answer follows what the row
    says rather than where the conversion happened to fail.
    """
    found = _YEAR.match(value) if isinstance(value, str) else None
    if found is None:
        return None
    year = int(found.group(1))
    if year == FLOOR.year:
        return FLOOR
    if year == CEILING.year:
        return CEILING
    return None


def placeable(convert: Callable[[str], datetime]) -> Callable[[str], datetime]:
    """``convert`` answering :data:`FLOOR` or :data:`CEILING` at the calendar's edges."""
    if getattr(convert, _MARK, False):
        return convert

    def string_to_datetime(value: str) -> datetime:
        try:
            moment = convert(value)
        except OverflowError:
            edge = _edge(value)
            if edge is None:
                raise
            return edge
        if moment.tzinfo is not None:
            # Not what the pinned binding answers. An aware value converts
            # back in any zone only if its own offset allows, so it is
            # handed on as it came rather than compared with a naive bound.
            return moment
        if moment < FLOOR:
            return FLOOR
        if moment > CEILING:
            return CEILING
        return moment

    setattr(string_to_datetime, _MARK, True)
    string_to_datetime.__wrapped__ = convert  # type: ignore[attr-defined]
    return string_to_datetime


def install() -> None:
    """Wrap the binding's date conversion, once per process."""
    from pyrekordbox.db6 import tables

    tables.string_to_datetime = placeable(tables.string_to_datetime)


def installed() -> bool:
    """Whether the binding's conversion is the wrapped one."""
    from pyrekordbox.db6 import tables

    return bool(getattr(tables.string_to_datetime, _MARK, False))


__all__ = ["CEILING", "FLOOR", "install", "installed", "placeable"]
