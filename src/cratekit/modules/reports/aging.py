"""Feature Inventory row 20: the intake aging report.

Intake is a listening queue, and what goes wrong is that nothing in it ever
LOOKS old. This report bands every intake grouping by the date in its own name.

- The thresholds come from configuration only; ``AgingThresholds`` has no
  defaults, so there is no hardcoded policy to fall back on.
- No folder is named. Every grouping under the declared intake display, at any
  depth, is aged the same way, so a two stage workflow is two thresholds.
- An intake flow that is absent refuses rather than reading as one that is
  empty, since both would otherwise render as "nothing to do".
- There is no ledger: the report is a pure function of the names, the
  thresholds and today's date, and writes nothing. A decision that must outlive
  a process belongs in the review queue.

Layer note: MODULES. Gated by the ``reports`` toggle (R5).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from cratekit.core import config, taxonomy
from cratekit.core.cause import Scope, refuse
from cratekit.modules.reports.export import LibraryView, Playlist

#: ISO first, then the month first shapes intake names use (``lisa_06_19_2026``,
#: ``3_9_26_phil``, ``02_19_26 lisa``), anchored on digits rather than position.
_ISO_IN_NAME = re.compile(r"(20\d{2})-(\d{1,2})-(\d{1,2})")
_MONTH_FIRST_IN_NAME = re.compile(r"(\d{1,2})[_-](\d{1,2})[_-](\d{2,4})")

#: The window a two digit year is read into, so ``_99_`` is 2099 rather than
#: 1999. It bounds the year, not the age; a future date is caught in ``_grouping``.
_CENTURY = 2000
_YEAR_FLOOR = 2000
_YEAR_CEILING = 2099


class AgingPolicyInvalid(ValueError):
    """Thresholds built wrongly in code; a config FILE is caught by ``config.validate``."""


@dataclass(frozen=True, slots=True)
class AgingThresholds:
    """When an intake grouping is stale, and when expired. NEITHER HAS A DEFAULT."""

    stale_days: int
    expired_days: int

    def __post_init__(self) -> None:
        if self.stale_days < 1:
            raise AgingPolicyInvalid(
                f"stale_days is {self.stale_days}; a grouping cannot be stale "
                f"before it exists, and a threshold of zero reports every intake "
                f"list as stale on the day it is created"
            )
        if self.expired_days < self.stale_days:
            raise AgingPolicyInvalid(
                f"expired_days is {self.expired_days} and stale_days is "
                f"{self.stale_days}; expiry that arrives before staleness makes "
                f"the two bands overlap, and a grouping would be reported in both"
            )


def thresholds_from(cfg: config.Config) -> AgingThresholds:
    """The declared policy, read from configuration and from nowhere else."""
    return AgingThresholds(
        stale_days=cfg.reports.intake_stale_days,
        expired_days=cfg.reports.intake_expired_days,
    )


@dataclass(frozen=True, slots=True)
class Grouping:
    """One intake grouping and its date and age; None is UNKNOWN, never zero."""

    path: tuple[str, ...]
    track_count: int
    intake_date: date | None = None
    age_days: int | None = None

    @property
    def display(self) -> str:
        return self.path[-1] if self.path else ""


@dataclass(frozen=True, slots=True)
class AgingReport:
    """Every intake grouping, in exactly one band."""

    as_of: date
    thresholds: AgingThresholds
    expired: tuple[Grouping, ...] = ()
    stale: tuple[Grouping, ...] = ()
    current: tuple[Grouping, ...] = ()
    undated: tuple[Grouping, ...] = ()

    @property
    def groupings(self) -> tuple[Grouping, ...]:
        return (*self.expired, *self.stale, *self.current, *self.undated)


def parse_intake_date(name: str) -> date | None:
    """The FIRST plausible date in a grouping's name, or None.

    The first, because a renamed list carries its intake date at the front. An
    impossible day returns None, so the name is shown undated and gets fixed.
    """
    iso = _ISO_IN_NAME.search(name)
    if iso is not None:
        return _date_or_none(int(iso.group(1)), int(iso.group(2)), int(iso.group(3)))
    for match in _MONTH_FIRST_IN_NAME.finditer(name):
        month, day, year = (int(match.group(index)) for index in (1, 2, 3))
        if year < 100:
            year += _CENTURY
        if not (_YEAR_FLOOR <= year <= _YEAR_CEILING):
            continue
        found = _date_or_none(year, month, day)
        if found is not None:
            return found
    return None


def _date_or_none(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def intake_groupings(
    view: LibraryView, *, intake: taxonomy.Node, today: date
) -> tuple[Grouping, ...]:
    """Every playlist under the DECLARED intake flow, dated and aged.

    A grouping is any playlist with the intake display ANYWHERE above it, so an
    intake folder filed inside another is still aged, and two such folders both
    yield groupings. A tree with no such folder REFUSES, since returning nothing
    would read as a clear intake. Unreadable node kinds are refused once, in
    ``export``, so no view reaching here holds one.
    """
    wanted = intake.display
    if not view.has_folder(wanted):
        raise refuse(
            "intake-flow-absent",
            f"no folder named {wanted!r} appears anywhere in the exported tree, "
            f"so this report never found the intake flow it was asked about; "
            f"reporting nothing would read as an intake queue with nothing "
            f"waiting in it, which is the opposite conclusion",
            steps=(
                "check that the exported tree really holds the intake flow the "
                "taxonomy declares, and that the export is the current one",
                "if the flow is called something else in this library, change "
                "the declared display in the taxonomy template rather than "
                "renaming folders to match the software",
            ),
            scope=Scope.RUN,
            origin=("reports",),
            detail={"declared": wanted},
        )
    return tuple(
        _grouping(playlist, today=today)
        for playlist in view.playlists
        if wanted in playlist.path[:-1]
    )


def _grouping(playlist: Playlist, *, today: date) -> Grouping:
    """One playlist as a dated grouping. A future date is UNDATED, not current,
    because a typo in a year must not make a grouping permanently young.
    """
    intake_date = parse_intake_date(playlist.display)
    if intake_date is not None and intake_date > today:
        intake_date = None
    return Grouping(
        path=playlist.path,
        track_count=len(playlist.track_ids),
        intake_date=intake_date,
        age_days=None if intake_date is None else (today - intake_date).days,
    )


def intake_aging(
    view: LibraryView,
    *,
    intake: taxonomy.Node,
    thresholds: AgingThresholds,
    today: date,
) -> AgingReport:
    """Band every intake grouping by age. Reads a document, writes nothing.

    ``today`` has no default, so the answer never depends on the wall clock.
    """
    expired: list[Grouping] = []
    stale: list[Grouping] = []
    current: list[Grouping] = []
    undated: list[Grouping] = []
    for grouping in intake_groupings(view, intake=intake, today=today):
        if grouping.age_days is None:
            undated.append(grouping)
        elif grouping.age_days > thresholds.expired_days:
            expired.append(grouping)
        elif grouping.age_days > thresholds.stale_days:
            stale.append(grouping)
        else:
            current.append(grouping)
    return AgingReport(
        as_of=today,
        thresholds=thresholds,
        expired=_oldest_first(expired),
        stale=_oldest_first(stale),
        current=_oldest_first(current),
        undated=tuple(sorted(undated, key=lambda item: item.path)),
    )


def _oldest_first(groupings: list[Grouping]) -> tuple[Grouping, ...]:
    """Oldest first, then by path, so ties keep one order across runs."""
    return tuple(sorted(groupings, key=lambda item: (-(item.age_days or 0), item.path)))


__all__ = [
    "AgingPolicyInvalid",
    "AgingReport",
    "AgingThresholds",
    "Grouping",
    "intake_aging",
    "intake_groupings",
    "parse_intake_date",
    "thresholds_from",
]
