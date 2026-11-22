"""The favourites playlists named once, on both sides (KTD7: no product imports).

The account side: the source system's private quarter playlists, ``Favorites
2026-Q2``, which the playlists source must tell from other account playlists
by name. The rekordbox side: a heart filed in its UTC month's playlist,
``2026-10``, or ``Undated``; :data:`QUARTER_LABEL` survives only for the split.

Layer: modules.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

#: The leading word every placeholder name carries, followed by its quarter.
PLACEHOLDER_PREFIX = "Favorites "

#: The quarter the source system could not date a heart into, the source's too.
BACKLOG = "(undated backlog)"

#: A whole placeholder name, a dated quarter or the backlog, by ``fullmatch``.
PLACEHOLDER_NAME = re.compile(
    re.escape(PLACEHOLDER_PREFIX) + r"(?:" + r"\d{4}-Q[1-4]" + r"|" + re.escape(BACKLOG) + r")"
)

#: The rekordbox playlist a heart with no date goes to, the source system's name.
UNDATED = "Undated"

#: A whole quarter label as rekordbox carried it before U145, ``2026-Q4``, by
#: ``fullmatch``. READ ONLY: nothing makes one any more.
QUARTER_LABEL = re.compile(r"\d{4}-Q[1-4]")

#: A whole month label as a placement names it, ``2026-10``, by ``fullmatch``.
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

    Text is read as ISO 8601, as a job freezes it; anything that does not read
    is no date rather than a refusal, since an undated heart has its playlist.
    """
    if isinstance(said, datetime):
        return as_utc(said)
    if isinstance(said, str) and said.strip():
        try:
            return as_utc(datetime.fromisoformat(said.strip()))
        except ValueError:
            return None
    return None


def is_filing(name: str) -> bool:
    """Whether a playlist beside All Favorites files by date: a month, Undated, a quarter (U146)."""
    text = str(name or "")
    return (
        text == UNDATED
        or MONTH_LABEL.fullmatch(text) is not None
        or QUARTER_LABEL.fullmatch(text) is not None
    )


#: Where each kind of child of the folder holding All Favorites reads, lower first (U180).
RANK_SOURCE = 0
RANK_MONTH = 1
RANK_UNDATED = 2
RANK_OTHER = 3


def folder_rank(name: str, *, source: bool, plain: bool) -> tuple[int, int]:
    """Where a child of the folder that holds All Favorites reads, newest month first (U180).

    All Favorites first, by the caller's row; then each plain playlist named as
    a month, newest first; then a plain :data:`UNDATED`; then everything else at
    one rank, so a stable sort keeps their relative order.
    """
    if source:
        return (RANK_SOURCE, 0)
    text = str(name or "")
    if plain and MONTH_LABEL.fullmatch(text) is not None:
        year, month = text.split("-")
        return (RANK_MONTH, -(int(year) * 12 + int(month)))
    if plain and text == UNDATED:
        return (RANK_UNDATED, 0)
    return (RANK_OTHER, 0)


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
    "RANK_MONTH",
    "RANK_OTHER",
    "RANK_SOURCE",
    "RANK_UNDATED",
    "UNDATED",
    "as_utc",
    "folder_rank",
    "is_filing",
    "is_placeholder",
    "month_label",
    "month_of",
    "parse_hearted",
    "placeholder_name",
]
