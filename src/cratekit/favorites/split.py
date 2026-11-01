"""The quarter playlists under Favorites, split into months and retired (U145).

Until U145 a landed heart went into the playlist of the UTC quarter it was
hearted in, ``Favorites / 2026-Q4``, the source system's grain. The author
chose a month grain on 2026-10-14, and so the folder reads one way, the
quarters already there are split once: every live member of every quarter
playlist joins the playlist of its own month, ``2026-10``, and the emptied
quarter playlists are retired. ``crate favorites split`` asks; this module
plans and writes.

**THE DATE IS THE JOB'S FIRST AND THE ACCOUNT'S SECOND, LISTED ONCE.** A hearts
job freezes each heart's date on its row (``intake.cli.HEARTED``), so every
row of every hearts job on this library is read, whatever its match state,
and tied to the library's rows by the one match rule. A member no job dates
is looked for among the account's hearts, listed once and only when some
member needs it. A member dated nowhere goes to ``Undated`` and is named,
since its quarter is retired and Undated is the folder's one home for a heart
with no date.

**ADD ONLY, THEN RETIRE.** The memberships go in one commit, through the one
writer that owns "only when absent", and no heart is taken out of a month or
moved between months. The quarters are retired in a SECOND commit, each by
:func:`rb_writer.remove_playlist_node`, the soft delete the INBOX rotation
uses, and only once every member a quarter holds reads back live in its
month. A quarter the first commit did not empty is not retired.

**A RUN STOPPED PARTWAY RE-PLANS TO THE SAME DIGEST.** The digest covers what
the split is FOR, the home, each quarter's row and members and each member's
month, and never what the months hold already or whether they exist yet. So a
run whose first commit landed and whose second did not plans the same split,
is approved against the same digest, adds nothing and retires the quarters.
Once they are retired there is nothing to plan, and the verb asks nothing.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.acquire import match, match_cli
from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, jobs, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.favorites import backfill, placeholders, placement
from cratekit.intake import account_playlists, native
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.write import trees

#: The session workflow the split is recorded under, and its plan's kind.
WORKFLOW = "favorites-split"

#: The tables the retirement's commit admits a soft delete in: the quarter's
#: own row and its own memberships, the INBOX rotation's pair.
REMOVALS: tuple[str, ...] = (rb_writer.PLAYLIST_TABLE, rb_writer.MEMBERSHIP_TABLE)

#: What an existing playlist row may change while the split adds beside it:
#: the binding's position and bookkeeping, the columns a sibling of a moved
#: node may change in :func:`rb_writer.node_change_violations`.
_BOOKKEEPING = frozenset({"Seq", "updated_at", "usn", "rb_local_usn"})

#: Where a member's date came from.
BY_JOB = "job"
BY_ACCOUNT = "account"
BY_NONE = "none"

_ORIGIN = ("favorites", "split")


# ---------------------------------------------------------------------------
# What the folder holds
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Quarter:
    """One quarter playlist under the folder, and the content rows it holds live."""

    name: str
    playlist_id: str
    members: tuple[str, ...]


def quarters(db: Any, home: placement.Home) -> tuple[Quarter, ...]:
    """Every live plain playlist beside the source whose whole name is a quarter.

    By name, ``2026-Q4``, the name U120 and the source system gave them, read
    from the home the placement resolved, so a quarter is only ever one that
    sits where a landing would have put it. In name order, so the screen and
    the digest read in one order.
    """
    found: list[Quarter] = []
    for name, row in sorted(home.present.items()):
        if not placeholders.QUARTER_LABEL.fullmatch(name):
            continue
        held = [
            str(song.ContentID)
            for song in db.get_playlist_songs(PlaylistID=str(row))
            if not rb_writer.membership_removed(song)
        ]
        found.append(Quarter(name=name, playlist_id=str(row), members=tuple(dict.fromkeys(held))))
    return tuple(found)


# ---------------------------------------------------------------------------
# The dating: the job first, the account second
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Dated:
    """When one member was hearted, and who said so."""

    hearted: datetime | None
    dated_by: str


@dataclass(frozen=True, slots=True)
class Dating:
    """Each member's date by content row, and what finding them read."""

    by_row: Mapping[str, Dated]
    #: Whether the account was listed at all this run.
    listed: bool = False
    #: The provider's shortfall when the listing came back short (R-504).
    withheld: int = 0
    #: The hearts jobs whose reports could not be read, skipped and named.
    unreadable: tuple[str, ...] = ()


def _tied(
    cfg: config.Config,
    db: Any,
    view: tuple[Any, Any, Any],
    rows: Sequence[tuple[match.Wanted, datetime]],
    wanted: set[str],
) -> dict[str, datetime]:
    """The date of each wanted content row the dated ``rows`` resolve to, the first mention winning.

    THE ONE MATCH RULE THE INTAKE WORKER USES, tombstones included, then the
    one rule for a path against a row. A row two hearts resolve to takes the
    first one's date, which is the order the caller hands them in.
    """
    if not rows or not wanted:
        return {}
    index, suppresses, identify = view
    resolved: list[tuple[datetime, list[Path]]] = []
    for track, when in rows:
        found = match.resolve_one(track, index, suppresses=suppresses, suppression_id=identify)
        if found.state is match.MatchState.MATCHED:
            resolved.append((when, [Path(path) for path in found.paths]))
    paths = list(dict.fromkeys(path for _when, held in resolved for path in held))
    if not paths:
        return {}
    by_path = native.content_ids_for(db, cfg, paths)
    dates: dict[str, datetime] = {}
    for when, held in resolved:
        for path in held:
            content_id = by_path.get(str(path))
            if content_id is not None and content_id in wanted and content_id not in dates:
                dates[content_id] = when
    return dates


def _job_rows(cfg: config.Config) -> tuple[list[tuple[match.Wanted, datetime]], tuple[str, ...]]:
    """Each heart a hearts job on this library dated, once, oldest job first, whatever its state.

    NOT ONLY THE ROWS A DOWNLOAD WAS MADE FROM, as the backfill's are: a heart
    the library owned when its job ran is still dated on its row, and the
    quarters hold owned hearts above all. Read through the one reader of a
    hearts job's frozen rows, every state admitted. A PROVIDER IDENTIFIER IS
    RESOLVED ONCE, its first dated mention winning, since every sync freezes
    the whole listing again and the match is the slow part. A job whose
    reports cannot be read is skipped and named, for the backfill's reason.
    """
    found: dict[str, tuple[match.Wanted, datetime]] = {}
    unreadable: list[str] = []
    with jobs.open_store() as store:
        for job in backfill.hearts_jobs(cfg):
            try:
                rows = account_playlists.carried_hearts(store, job, states=None)
            except CratekitError:
                unreadable.append(job.job_id)
                continue
            for row in rows:
                if row.hearted is not None and row.ref not in found:
                    found[row.ref] = (row.wanted, row.hearted)
    return list(found.values()), tuple(unreadable)


def date_members(cfg: config.Config, db: Any, content_ids: Iterable[str]) -> Dating:
    """Each content row's date: a hearts job's frozen one, else the account's, else none.

    The library is walked once for both, and the account is listed once, only
    when some row no job dates, through the hearts listing every favourites
    verb reads, so a listing that cannot be read refuses with its own reason.
    """
    wanted = {str(content_id) for content_id in content_ids}
    if not wanted:
        return Dating(by_row={})
    view = match_cli.library_view(cfg)
    job_rows, unreadable = _job_rows(cfg)
    by_row: dict[str, Dated] = {
        content_id: Dated(when, BY_JOB)
        for content_id, when in _tied(cfg, db, view, job_rows, wanted).items()
    }
    listed = False
    withheld = 0
    rest = wanted - set(by_row)
    if rest:
        frozen, short = intake_cli.list_favorites(catalogue.resolve(cfg))
        listed = True
        withheld = short.withheld if short is not None else 0
        account_rows = [
            (intake_cli.thawed(said), when)
            for said in frozen.values()
            if (when := placeholders.parse_hearted(said.get(intake_cli.HEARTED))) is not None
        ]
        for content_id, when in _tied(cfg, db, view, account_rows, rest).items():
            by_row[content_id] = Dated(when, BY_ACCOUNT)
    for content_id in wanted - set(by_row):
        by_row[content_id] = Dated(None, BY_NONE)
    return Dating(by_row=by_row, listed=listed, withheld=withheld, unreadable=unreadable)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Member:
    """One content row a quarter holds, the quarters it sits in, and its month."""

    content_id: str
    title: str
    quarters: tuple[str, ...]
    hearted: datetime | None
    dated_by: str

    @property
    def month(self) -> str:
        return placeholders.month_label(self.hearted)


@dataclass(frozen=True, slots=True)
class SplitPlan:
    """The quarters to split against the home as it stands, read on one handle."""

    home: placement.Home
    quarters: tuple[Quarter, ...]
    #: The members a month takes, every live member of a quarter but those
    #: the author took back.
    members: tuple[Member, ...]
    #: Each month the members go to, by name in order, with its members in
    #: quarter order. Derived from ``members`` once, by :func:`_planned`.
    months: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    #: Each planned month's live members when planned, for the counts. NOT
    #: DIGESTED, so a run whose additions landed plans the same split.
    held: Mapping[str, frozenset[str]] = field(default_factory=dict)
    #: Members whose All Favorites membership rekordbox marked removed and
    #: that All Favorites no longer holds live: the author took the heart
    #: back, so no month takes it, as the backfill never puts one back. Named,
    #: and the quarter holding it still retires.
    taken_back: tuple[Member, ...] = ()
    digest: str = ""
    listed: bool = False
    withheld: int = 0
    unreadable: tuple[str, ...] = ()

    @property
    def adds(self) -> int:
        """The memberships the write would add, the ones a month already holds left out."""
        return sum(
            1
            for name, ids in self.months.items()
            for content_id in ids
            if content_id not in self.held.get(name, frozenset())
        )

    @property
    def creates(self) -> tuple[str, ...]:
        """The month playlists the write would make, by name."""
        return tuple(name for name in self.months if name not in self.home.present)

    @property
    def undated(self) -> tuple[Member, ...]:
        return tuple(one for one in self.members if one.hearted is None)

    @property
    def writes(self) -> bool:
        """Whether there is a quarter to retire, which is what the split is for."""
        return bool(self.quarters)

    def identity(self) -> dict[str, Any]:
        """What the digest covers: the split's intent, never the months' state.

        The home's rows, each quarter's row and live members, and each member's
        month. The month rows and what they hold are left out on purpose, so a
        run stopped after its additions re-plans to the digest it was approved
        for; a quarter that gained or lost a member, or a member whose date
        reads differently, is another plan.
        """
        return {
            "kind": WORKFLOW,
            **self.home.identity(),
            "quarters": [
                {"name": one.name, "row": one.playlist_id, "members": list(one.members)}
                for one in self.quarters
            ],
            "members": [{"row": one.content_id, "month": one.month} for one in self.members],
            "taken_back": [one.content_id for one in self.taken_back],
        }


def _titles(db: Any, content_ids: Iterable[str]) -> dict[str, str]:
    """Each content row's ``artist - title`` for the screen, a row that is not there left blank."""
    found: dict[str, str] = {}
    for content_id in content_ids:
        row = db.get_content(ID=content_id)
        if row is None:
            found[content_id] = ""
            continue
        artist = str(getattr(row, "ArtistName", "") or "")
        title = str(getattr(row, "Title", "") or "")
        found[content_id] = f"{artist} - {title}" if artist else title
    return found


def _in_quarters(held_quarters: Sequence[Quarter]) -> dict[str, list[str]]:
    """Each content row the quarters hold, in quarter order, with the quarters holding it."""
    found: dict[str, list[str]] = {}
    for one in held_quarters:
        for content_id in one.members:
            found.setdefault(content_id, []).append(one.name)
    return found


def taken_back(db: Any, home: placement.Home, content_ids: Iterable[str]) -> frozenset[str]:
    """The rows among ``content_ids`` the author took out of the source by hand.

    THE BACKFILL'S RULE (U120), read the same way: a membership of the source
    that rekordbox marked removed is the author un-hearting the track in the
    library. A row that is back in the source live was hearted again, so it
    is not taken back.
    """
    wanted = {str(content_id) for content_id in content_ids}
    removed = placement.members_marked_removed(db, home.source_id) & wanted
    if not removed:
        return frozenset()
    return frozenset(removed - placement.members(db, home.source_id))


def _planned(
    db: Any,
    home: placement.Home,
    held_quarters: Sequence[Quarter],
    dating: Dating,
) -> SplitPlan:
    in_quarters = _in_quarters(held_quarters)
    gone = taken_back(db, home, in_quarters)
    titles = _titles(db, in_quarters)
    every = [
        Member(
            content_id=content_id,
            title=titles.get(content_id, ""),
            quarters=tuple(names),
            hearted=dating.by_row.get(content_id, Dated(None, BY_NONE)).hearted,
            dated_by=dating.by_row.get(content_id, Dated(None, BY_NONE)).dated_by,
        )
        for content_id, names in in_quarters.items()
    ]
    members = tuple(one for one in every if one.content_id not in gone)
    by_month: dict[str, list[str]] = {}
    for one in members:
        by_month.setdefault(one.month, []).append(one.content_id)
    months = {name: tuple(by_month[name]) for name in sorted(by_month)}
    held = {
        name: placement.members(db, home.present[name]) if name in home.present else frozenset()
        for name in months
    }
    planned = SplitPlan(
        home=home,
        quarters=tuple(held_quarters),
        members=members,
        months=months,
        held=held,
        taken_back=tuple(one for one in every if one.content_id in gone),
        listed=dating.listed,
        withheld=dating.withheld,
        unreadable=dating.unreadable,
    )
    return replace(planned, digest=digest_of(planned.identity()))


def plan(cfg: config.Config, db: Any, *, source: str) -> SplitPlan:
    """The quarters under the home, each member dated, planned against what the folder holds.

    A library with no quarter playlist plans nothing, and nothing is dated,
    so the account is never asked and the library never walked. A member the
    author took back is not dated, since no month takes it.
    """
    home = placement.resolve_home(db, source)
    held = quarters(db, home)
    in_quarters = _in_quarters(held)
    wanted = set(in_quarters) - taken_back(db, home, in_quarters)
    dating = date_members(cfg, db, wanted) if wanted else Dating(by_row={})
    return _planned(db, home, held, dating)


def replan(db: Any, approved: SplitPlan, *, source: str) -> SplitPlan:
    """The split planned again on this handle, the approved dates reused, so the digest compares the database.

    THE MEMBERS ARE NOT DATED AGAIN: dating walks the library and may list the
    account, and what can move between the approval and the write is the home,
    the quarters and what they hold, which is what the digest covers. A member
    the approved plan never dated is undated here, which moves the digest.
    """
    home = placement.resolve_home(db, source)
    dating = Dating(
        by_row={one.content_id: Dated(one.hearted, one.dated_by) for one in approved.members},
        listed=approved.listed,
        withheld=approved.withheld,
        unreadable=approved.unreadable,
    )
    return _planned(db, home, quarters(db, home), dating)


def payload(planned: SplitPlan) -> dict[str, Any]:
    """The plan as the gate shows it: one item per month to fill and one per quarter to retire."""
    items: list[dict[str, Any]] = []
    for name, ids in planned.months.items():
        held = planned.held.get(name, frozenset())
        items.append(
            {
                "action": "fill",
                "playlist": name,
                "count": len(ids),
                "adds": sum(1 for content_id in ids if content_id not in held),
                "made": name in planned.creates,
            }
        )
    for one in planned.quarters:
        items.append(
            {
                "action": "retire",
                "playlist": one.name,
                "row": one.playlist_id,
                "count": len(one.members),
            }
        )
    by_source: dict[str, int] = {}
    for one in planned.members:
        by_source[one.dated_by] = by_source.get(one.dated_by, 0) + 1
    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "members": len(planned.members),
            "adds": planned.adds,
            "creates": len(planned.creates),
            "retires": len(planned.quarters),
            "undated": len(planned.undated),
            "taken back": len(planned.taken_back),
            "dates from jobs": by_source.get(BY_JOB, 0),
            "dates from the account": by_source.get(BY_ACCOUNT, 0),
            "jobs unread": len(planned.unreadable),
        },
        "chunk": None,
    }


def facts(planned: SplitPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.home
    where = repr(home.folder_name) if home.folder_name else "the playlist root"
    months = planned.months
    shown: dict[str, Any] = {
        "under": f"{where}, beside {home.source_name!r} (row {home.source_id})",
        "quarters to retire": [f"{one.name} ({len(one.members)})" for one in planned.quarters],
        "month playlists": [
            f"{name} ({len(ids)})" + (", made" if name in planned.creates else "")
            for name, ids in months.items()
        ],
        "memberships to add": planned.adds,
    }
    if planned.undated:
        shown["undated"] = [
            f"{one.title or 'row ' + one.content_id} (row {one.content_id}, from "
            f"{', '.join(one.quarters)})"
            for one in planned.undated
        ]
    if planned.taken_back:
        shown["taken back"] = [
            f"{one.title or 'row ' + one.content_id} (row {one.content_id}, from "
            f"{', '.join(one.quarters)}), removed from {home.source_name!r} in rekordbox"
            for one in planned.taken_back
        ]
    if planned.withheld:
        shown["withheld"] = (
            f"the account's hearts listed short, {planned.withheld} withheld by the "
            f"provider, so an undated member may be one of them"
        )
    if planned.unreadable:
        shown["jobs unread"] = list(planned.unreadable)
    return shown


# ---------------------------------------------------------------------------
# The confinement of the additions
# ---------------------------------------------------------------------------


def addition_violations(
    before: rb_writer.NodeTables,
    after: rb_writer.NodeTables,
    *,
    planned: Mapping[str, Iterable[str]],
    created: Mapping[str, tuple[str, str]],
) -> list[str]:
    """Every difference between two readings that the planned additions do not explain.

    ``planned`` maps each month playlist row the write used to the content rows
    the plan names for it, and ``created`` each playlist row the write made to
    its ``(name, parent)``. Empty means the additions were confined.

    PURE, as :func:`rb_writer.node_change_violations` is, so every branch is
    reachable with literal readings. What it explains, and nothing more:

    * no content row differs, is added or disappears;
    * no membership row disappears or changes, and every membership row added
      is live and joins a planned month with a content row the plan names for
      THAT month, so the writer cannot add a membership the plan did not name;
    * the playlist rows added are exactly ``created``, live, plain, of the
      planned name and under the planned parent, and no playlist row
      disappears; an existing one may move only its bookkeeping, and only
      when it is a planned month or sits beside a made one.
    """
    violations: list[str] = []
    wanted = {str(row): {str(content_id) for content_id in ids} for row, ids in planned.items()}
    if before.content != after.content:
        violations.append(f"a {rb_writer.CONTENT_TABLE} row changed, and the split touches no track")

    p_cols = before.playlist_columns
    marker_at = p_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    name_at = p_cols.index("Name")
    kind_at = p_cols.index("Attribute")
    for key in sorted(set(before.playlists) - set(after.playlists)):
        violations.append(f"the {rb_writer.PLAYLIST_TABLE} row {key!r} disappeared")
    added = set(after.playlists) - set(before.playlists)
    for key in sorted(added - set(created)):
        violations.append(f"an unplanned {rb_writer.PLAYLIST_TABLE} row {key!r} was added")
    beside = {str(parent) for _name, parent in created.values()}
    for key, (name, parent) in sorted(created.items()):
        row = after.playlists.get(key)
        if row is None:
            violations.append(f"the planned month {name!r} (row {key!r}) was not made")
            continue
        if (
            str(row[name_at]) != name
            or str(row[parent_at]) != str(parent)
            or row[marker_at]
            or int(row[kind_at] or 0) != 0
        ):
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not a live plain playlist "
                f"named {name!r} under {parent!r}"
            )
    for key in sorted(set(before.playlists) & set(after.playlists)):
        changed = {
            name
            for name, old, new in zip(p_cols, before.playlists[key], after.playlists[key])
            if old != new
        }
        if not changed:
            continue
        allowed = (
            _BOOKKEEPING
            if key in wanted or str(before.playlists[key][parent_at]) in beside
            else frozenset()
        )
        if changed - allowed:
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} changed {sorted(changed - allowed)}, "
                f"which the split's additions do not explain"
            )

    m_cols = before.membership_columns
    owner_at = m_cols.index("PlaylistID")
    content_at = m_cols.index("ContentID")
    m_marker = m_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    for key in sorted(set(before.memberships) - set(after.memberships)):
        violations.append(f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} disappeared")
    for key in sorted(set(before.memberships) & set(after.memberships)):
        if before.memberships[key] != after.memberships[key]:
            violations.append(
                f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} changed, and the split's "
                f"additions change no membership they did not make"
            )
    for key in sorted(set(after.memberships) - set(before.memberships)):
        row = after.memberships[key]
        owner, content_id = str(row[owner_at]), str(row[content_at])
        if row[m_marker] or content_id not in wanted.get(owner, set()):
            violations.append(
                f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} puts row {content_id!r} in "
                f"playlist {owner!r}, which the plan did not name"
            )
    return violations


def assert_additions_confined(
    db: Any,
    before: rb_writer.NodeTables,
    *,
    planned: Mapping[str, Iterable[str]],
    created: Mapping[str, tuple[str, str]],
) -> None:
    """Refuse, before the commit, an addition the plan did not name, read from SQL.

    The pending work is flushed DELIBERATELY, inside the transaction, so the
    second reading sees it and a refusal still rolls back, as
    :func:`rb_writer.assert_node_changes_confined` does for the same reason.
    """
    db.session.flush()
    violations = addition_violations(
        before, rb_writer.node_tables(db), planned=planned, created=created
    )
    if violations:
        db.rollback()
        raise refuse(
            "whitelist-violation",
            "the split's additions reached rows the plan did not name, read from SQL "
            "before the commit, so nothing was written:\n  - " + "\n  - ".join(violations),
            origin=_ORIGIN,
            detail={"violations": violations},
        )


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Split:
    """What one split wrote, read back from the database after its commits."""

    #: Each month written to: its name, its row, the memberships added.
    months: tuple[tuple[str, str, int], ...]
    created: tuple[str, ...]
    retired: tuple[str, ...]
    session_id: str
    disagreements: tuple[str, ...] = ()

    @property
    def added(self) -> int:
        return sum(count for _name, _row, count in self.months)


def _record_split_commit(
    record: session.SessionRecord, *, added: int, retired: int, cfg: config.Config
) -> None:
    """Record a commit on the session, as rows created and rows changed under the favourites key."""
    if added <= 0 and retired <= 0:
        return
    session.record_commit(
        record,
        placement.RECORD_KEY,
        session.ChangeSummary(
            (session.TreeChange(tree=placement.RECORD_KEY, created=added, updated=retired),)
        ),
        cfg,
    )


def _unemptied(db: Any, planned: SplitPlan, rows: Mapping[str, str]) -> list[str]:
    """Each quarter a member of which is not live in its month, read on this handle."""
    held = {name: placement.members(db, row) for name, row in rows.items()}
    month_of = {one.content_id: one.month for one in planned.members}
    problems: list[str] = []
    for one in planned.quarters:
        missing = sorted(
            content_id
            for content_id in one.members
            if content_id in month_of
            and content_id not in held.get(month_of[content_id], frozenset())
        )
        if missing:
            problems.append(
                f"{one.name!r} holds {len(missing)} row(s) its months do not: {', '.join(missing)}"
            )
    return problems


def _read_back(db: Any, planned: SplitPlan, rows: Mapping[str, str]) -> tuple[str, ...]:
    """Each month that lacks a planned member, and each quarter still live, read after the commits."""
    problems = _unemptied(db, planned, rows)
    for one in planned.quarters:
        row = db.get_playlist(ID=one.playlist_id)
        if row is not None and not rb_writer.node_removed(row):
            problems.append(f"{one.name!r} (row {one.playlist_id}) is still live")
    return tuple(problems)


def apply(
    cfg: config.Config,
    db: Any,
    approved: SplitPlan,
    *,
    source: str,
    analysis_roots: Iterable[Path | str],
) -> Split:
    """Add every member to its month in one commit, then retire the emptied quarters in a second.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST and a digest that moved
    refuses, since the approved one was read on a handle that has since
    closed. THE SESSION SPINE IS CALLED, NOT REBUILT, as the genre Favorites
    refresh calls it for its own two commits: the gates with a record kept,
    one capture verified before anything is written, the analysis watch over
    the roots named, a commit witness on each commit, and the guarded commit,
    the second admitting the playlist and the membership tables alone.

    EACH COMMIT IS CONFINED FROM SQL BEFORE IT LANDS: the additions by
    :func:`assert_additions_confined`, the retirements by
    :func:`rb_writer.assert_node_changes_confined`. And no quarter is retired
    until every member it holds reads back live in its month.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    again = replan(db, approved, source=source)
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            "the quarter playlists are not as the approved plan read them, so nothing "
            "was written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.digest, "now": again.digest},
        )
    planned = again
    home = planned.home
    # THE OUT OF BAND RESTORE IS DETECTED BEFORE THE FINGERPRINT IS TOUCHED,
    # as the backfill does: the Favorites folder is no tree, so the detection
    # marks and never refuses here.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))

    written: list[tuple[str, str, int]] = []
    created: list[str] = []
    rows: dict[str, str] = {}
    retired: list[str] = []
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)

        # ── the additions, and their own commit ────────────────────────────
        added = 0
        with rb_writer.commit_witness(db) as witness:
            try:
                parent = None
                if home.folder_id:
                    parent = db.get_playlist(ID=home.folder_id)
                    if parent is None or rb_writer.node_removed(parent):
                        raise refuse(
                            "decision-stale",
                            f"the folder {home.folder_name!r} (row {home.folder_id}) is not "
                            f"live any more, so nothing was written",
                            origin=_ORIGIN,
                            detail={"folder": home.folder_id},
                        )
                parent_id = str(parent.ID) if parent is not None else ""
                before = rb_writer.node_tables(db)
                made: dict[str, tuple[str, str]] = {}
                for name, ids in planned.months.items():
                    row, fresh = placement.month_row(db, name, parent, source_id=home.source_id)
                    rows[name] = str(row.ID)
                    if fresh:
                        db.session.flush()
                        made[str(row.ID)] = (name, parent_id or str(row.ParentID))
                        created.append(name)
                    count = len(rb_writer.add_memberships(db, row, ids))
                    added += count
                    written.append((name, str(row.ID), count))
                assert_additions_confined(
                    db,
                    before,
                    planned={rows[name]: ids for name, ids in planned.months.items()},
                    created=made,
                )
                if added or made:
                    rb_writer.commit_guarded(db)
            except BaseException:
                trees._rollback_quietly(db)
                if witness.landed:
                    _record_split_commit(record, added=added, retired=0, cfg=cfg)
                raise
        _record_split_commit(record, added=added, retired=0, cfg=cfg)
        if added:
            convergence.record_fingerprint(cfg, db)

        # ── the retirements, behind the additions ──────────────────────────
        unemptied = _unemptied(db, planned, rows)
        if unemptied:
            raise refuse(
                "session-committed-unverified",
                "the months do not hold every member of the quarters, so no quarter was "
                "retired: " + "; ".join(unemptied),
                origin=_ORIGIN,
                detail={"unemptied": unemptied, "session": record.session_id},
            )
        with rb_writer.commit_witness(db) as witness:
            try:
                before = rb_writer.node_tables(db)
                for one in planned.quarters:
                    rb_writer.remove_playlist_node(db, db.get_playlist(ID=one.playlist_id))
                    retired.append(one.name)
                rb_writer.assert_node_changes_confined(
                    db,
                    before,
                    moved={},
                    removed=[one.playlist_id for one in planned.quarters],
                )
                rb_writer.commit_guarded(db, removals=REMOVALS)
            except BaseException:
                trees._rollback_quietly(db)
                if witness.landed:
                    _record_split_commit(record, added=0, retired=len(retired), cfg=cfg)
                raise
        _record_split_commit(record, added=0, retired=len(retired), cfg=cfg)
        convergence.record_fingerprint(cfg, db)
        disagreements = _read_back(db, planned, rows)
        session_id = record.session_id
    return Split(
        months=tuple(written),
        created=tuple(created),
        retired=tuple(retired),
        session_id=session_id,
        disagreements=disagreements,
    )


def assert_read_back(done: Split) -> None:
    """Refuse an answer the database does not hold."""
    if done.disagreements:
        raise refuse(
            "session-committed-unverified",
            "the favourites read back from the database are not the split's: "
            + "; ".join(done.disagreements)
            + "; the commits landed and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"disagreements": list(done.disagreements), "session": done.session_id},
        )


__all__ = [
    "BY_ACCOUNT",
    "BY_JOB",
    "BY_NONE",
    "Dated",
    "Dating",
    "Member",
    "Quarter",
    "REMOVALS",
    "Split",
    "SplitPlan",
    "WORKFLOW",
    "addition_violations",
    "apply",
    "assert_additions_confined",
    "assert_read_back",
    "date_members",
    "facts",
    "payload",
    "plan",
    "quarters",
    "replan",
]
