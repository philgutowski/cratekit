"""Feature Inventory row 20: the intake aging report, generalized.

Intake is a listening queue. Tracks land in it, somebody listens, and the ones
that earn a place get filed. What goes wrong is not that the queue fills up but
that nothing in it ever LOOKS old: a grouping from four months ago sits beside
one from yesterday, both rendered identically, and the queue silently becomes an
archive nobody reads.

The source system solves that for one person's library and hardcodes everything
about it: two day counts written into the module, one hardcoded holding folder
called by its display name, and a private sighting ledger on disk to approximate
how long something had been sitting in that folder. Three things change here, and
each closes a defect rather than tidying.

**The thresholds come from configuration.** ``AgingThresholds`` has no defaults
at all, which is the same decision ``naming.NameBudget`` makes and for the same
reason: config owns the values (S3), and a default here would be a second answer
to a question the config file already answers. The report cannot be run against a
hardcoded policy because there is no policy to fall back on.

**No folder is named, by anybody.** The source ages a top-level list one way and
a list inside a folder it calls by display name another way. This report ages
every intake grouping the same way, on the date in its own name, and reports the
path it was found at as context. So the two-stage workflow survives as two
thresholds rather than as a folder this module has to know about, and R19's rule
that a display name below the modules layer is never written into code is not
merely obeyed, it is unnecessary. U18 had to declare its catalog tree in the
taxonomy template for exactly this reason; this report needs nothing declared
because it names nothing.

**There is no ledger.** The source records, in a JSON file beside the report,
when it first saw each name inside the holding folder, so it can hold a deletion
back for one cycle. That file is a private, unlocked, read-then-write store of
decisions about a library, which is three separate things this product has
already been bitten by. It is not ported. This report is a pure function of the
names, the thresholds, and today's date, and it writes nothing at all. If the
parole idea is wanted later, its home is a verdict in the review queue, which is
where a decision that must outlive a process belongs.

Layer note: MODULES. Gated by the ``reports`` toggle (R5).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from cratekit.core import config, taxonomy
from cratekit.modules.reports.export import LibraryView, Playlist

#: ISO first, then the month-first shapes the intake convention actually uses:
#: ``lisa_06_19_2026``, ``3_9_26_phil``, ``02_19_26 lisa``. Both patterns are
#: anchored on digits rather than on position, because the date turns up at the
#: front of some names and the back of others.
_ISO_IN_NAME = re.compile(r"(20\d{2})-(\d{1,2})-(\d{1,2})")
_MONTH_FIRST_IN_NAME = re.compile(r"(\d{1,2})[_-](\d{1,2})[_-](\d{2,4})")

#: The window a two-digit year is read into. A grouping named ``_99_`` is a typo
#: rather than a list from 1999, and reading it as 1999 would report an age of
#: nine thousand days with a straight face.
_CENTURY = 2000
_YEAR_FLOOR = 2000
_YEAR_CEILING = 2099


class AgingPolicyInvalid(ValueError):
    """Thresholds that cannot describe a policy.

    A plain exception rather than a structured refusal, because this is reached
    only by constructing the value wrongly in code. The equivalent mistake made
    in a config FILE is caught by ``config.validate``, which reports it with the
    key that is wrong, and that is the path a user can actually be on.
    """


@dataclass(frozen=True, slots=True)
class AgingThresholds:
    """When an intake grouping counts as stale, and when as expired.

    NEITHER FIELD HAS A DEFAULT, on purpose. This is the value that makes the
    unit's "thresholds come from config, not from a hardcoded policy" true by
    construction rather than by inspection: there is no way to build one of these
    without supplying both numbers, so a caller cannot silently fall back to one
    person's habits.
    """

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
    """The declared policy, read from configuration and from nowhere else.

    One function, so there is one place the report's values come from. A caller
    that built the thresholds itself from some other source would be a second
    answer to a question the config file already answers (P2).
    """
    return AgingThresholds(
        stale_days=cfg.reports.intake_stale_days,
        expired_days=cfg.reports.intake_expired_days,
    )


@dataclass(frozen=True, slots=True)
class Grouping:
    """One intake grouping, its parsed intake date, and how old that makes it.

    ``intake_date`` and ``age_days`` are both None for a name carrying no date,
    and None means UNKNOWN rather than zero. A grouping nobody dated is reported
    as undated and is never aged, because guessing an age for it would eventually
    tell somebody to throw away a list that is a week old.
    """

    path: tuple[str, ...]
    track_count: int
    intake_date: date | None = None
    age_days: int | None = None

    @property
    def display(self) -> str:
        return self.path[-1] if self.path else ""


@dataclass(frozen=True, slots=True)
class AgingReport:
    """Every intake grouping, in exactly one band.

    The bands partition the groupings, and the test suite asserts that they do.
    A grouping reported in two bands is a grouping somebody acts on twice, and
    one reported in none is one the report was supposed to surface and did not.
    """

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
    """The first plausible date embedded in a grouping's name, or None.

    THE FIRST, deliberately. A name like ``6_01_26 lisa_5_26_26`` carries two,
    and the one that dates the grouping is the intake date at the front; taking
    the last would age the list from whenever somebody last edited the name.

    A shape that parses to an impossible day, ``13_45_26``, returns None rather
    than the next thing that nearly matches. Reporting it as undated puts it in
    front of a person with the name attached, which is the outcome that gets the
    name fixed.
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

    The intake node arrives as a declared taxonomy node rather than as a name
    this module knows, which is what keeps R19 true here. Every playlist beneath
    it is a grouping, at any depth: a person who filed some of them into a folder
    of their own has organized their intake, not left the report behind.

    A tree carrying two nodes with the intake display name yields groupings from
    BOTH, and that is deliberate. The writers refuse that shape because a write
    targeted by name cannot tell the two apart; a report that silently picked one
    would hide the duplication from the person who has to fix it.
    """
    wanted = intake.display
    out: list[Grouping] = []
    for playlist in view.playlists:
        if not playlist.path or playlist.path[0] != wanted:
            continue
        out.append(_grouping(playlist, today=today))
    return tuple(out)


def _grouping(playlist: Playlist, *, today: date) -> Grouping:
    intake_date = parse_intake_date(playlist.display)
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

    ``today`` is a parameter and has no default. A report whose answer depends on
    the wall clock cannot be asserted against a fixture, and the source system's
    equivalent took ``date.today()`` inside the function, so its own tests could
    only ever check the shape of the output.
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
    """Oldest first, then by path, so two groupings of one age keep an order.

    Sorting on the age alone leaves ties in whatever order the walk produced,
    which changes when somebody reorders their tree and makes two runs of an
    unchanged library look different.
    """
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
