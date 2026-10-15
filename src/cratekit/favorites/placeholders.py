"""The quarterly favourites playlists, named once, on both sides.

The source system puts the hearts the library does not own into one private
provider playlist per UTC quarter, ``Favorites 2026-Q2``, and those playlists are
the favourites source's to sweep. They are account playlists like any other, so
the playlists source would sweep them a second time unless it can tell them
apart, and the name is the only thing that tells them apart: no identifier for
them is recorded anywhere this build reads.

THE REKORDBOX SIDE IS NAMED HERE TOO, since U120. The source system filed an
owned heart into a playlist named for the UTC quarter it was hearted in,
``2026-Q4``, under the Favorites folder beside All Favorites, and a heart with
no date into ``Undated``. Since U145 the library files by MONTH instead,
``2026-10``, decided by the author on 2026-10-14, and no quarter playlist is
written again: the month rule below is the only one a placement asks, and
:data:`QUARTER_LABEL` survives only so ``crate favorites split`` can find the
quarter playlists it splits and retires. The account side's placeholder names
keep their quarters, since those are the source system's playlists to sweep.

A MODULE OF ITS OWN, WITH NO IMPORTS FROM THE PRODUCT, so the playlists source,
which is core and runs on the slim profile, can ask the question without
importing the favourites CLI or the outbound engines behind it (KTD7).
``cratekit.favorites.cli`` re-exports both names, which is where a reader of the
favourites source looks for them.

Layer: modules.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

#: The leading word every placeholder name carries, followed by its quarter.
PLACEHOLDER_PREFIX = "Favorites "

#: The quarter the source system could not date a heart into. Its hearts sit in
#: this one playlist until a later run resolves a date and moves them, so it is
#: the favourites source's in exactly the way a dated quarter is.
BACKLOG = "(undated backlog)"

#: A whole placeholder name, a dated quarter or the backlog. Anchored at both
#: ends by ``fullmatch`` at the call site, so ``All Favorites`` and
#: ``Favorites 2026-Q2 copy`` are not placeholders.
PLACEHOLDER_NAME = re.compile(
    re.escape(PLACEHOLDER_PREFIX) + r"(?:" + r"\d{4}-Q[1-4]" + r"|" + re.escape(BACKLOG) + r")"
)

#: The rekordbox playlist an owned heart with no date goes to, the source
#: system's own name for it (U120). The account side's is :data:`BACKLOG`.
UNDATED = "Undated"

#: A whole quarter label as rekordbox carried it before U145, ``2026-Q4``,
#: anchored at both ends by ``fullmatch`` at the call site. READ ONLY: it names
#: the playlists the month split retires, and nothing makes one any more.
QUARTER_LABEL = re.compile(r"\d{4}-Q[1-4]")

#: A whole month label as rekordbox carries it since U145, ``2026-10``,
#: anchored at both ends by ``fullmatch`` at the call site.
MONTH_LABEL = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])")


def as_utc(moment: datetime) -> datetime:
    """``moment`` in UTC. A naive datetime is taken to be UTC, the source system's rule."""
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def month_of(moment: datetime) -> str:
    """The UTC month label ``YYYY-MM`` a moment falls in, the one rule for every placement."""
    utc = as_utc(moment)
    return f"{utc.year:04d}-{utc.month:02d}"


def month_label(hearted: datetime | None) -> str:
    """The rekordbox playlist a heart goes to: its month, or :data:`UNDATED` with no date."""
    return UNDATED if hearted is None else month_of(hearted)


def parse_hearted(said: object) -> datetime | None:
    """The moment a frozen row says a heart was made, in UTC, or None when it says none.

    A datetime is taken as it is; text is read as ISO 8601, which is how a job
    freezes it; anything else, and text that does not read, is no date rather
    than a refusal, because a heart with no readable date is an undated heart
    and the undated playlist exists for exactly that.
    """
    if isinstance(said, datetime):
        return as_utc(said)
    if isinstance(said, str) and said.strip():
        try:
            return as_utc(datetime.fromisoformat(said.strip()))
        except ValueError:
            return None
    return None


def placeholder_name(quarter: str) -> str:
    """The placeholder playlist name for a quarter label such as ``2026-Q2``."""
    return f"{PLACEHOLDER_PREFIX}{quarter}"


def is_placeholder(name: str) -> bool:
    """Whether ``name`` is exactly a favourites placeholder's name, dated or backlog."""
    return PLACEHOLDER_NAME.fullmatch(str(name or "")) is not None


__all__ = [
    "BACKLOG",
    "MONTH_LABEL",
    "PLACEHOLDER_NAME",
    "PLACEHOLDER_PREFIX",
    "QUARTER_LABEL",
    "UNDATED",
    "as_utc",
    "is_placeholder",
    "month_label",
    "month_of",
    "parse_hearted",
    "placeholder_name",
]
