"""The quarter playlists under Favorites, split into months and retired (U145).

The author chose a month grain, so every live member of every quarter playlist
joins its own month's playlist and the emptied quarters are retired.
``crate favorites split`` asks; this module plans and writes.

**THE DATE IS THE JOB'S FIRST AND THE ACCOUNT'S SECOND**, the account listed
once and only when needed; a member dated nowhere goes to ``Undated``.
**ADD ONLY, THEN RETIRE**: the memberships in one commit, the quarters soft
deleted in a second, and only once every member reads back live in its month.
**THE DIGEST COVERS WHAT THE SPLIT IS FOR**, never what the months hold, so a
run stopped between the commits re-plans to the same digest and finishes.

Layer: modules.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.acquire import match, match_cli
from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session
from cratekit.core.cause import refuse
from cratekit.favorites import backfill, placeholders, placement, spine
from cratekit.intake import cli as intake_cli
from cratekit.intake import native
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


@dataclass(frozen=True, slots=True)
class Quarter:
    """One quarter playlist under the folder, and the content rows it holds live."""

    name: str
    playlist_id: str
    members: tuple[str, ...]


def quarters(db: Any, home: placement.Home) -> tuple[Quarter, ...]:
    """Every live plain playlist beside the source whose whole name is a quarter, ``2026-Q4``.

    Read from the home the placement resolved, so a quarter is only one where a
    landing would have put it, and in name order for the screen and the digest.
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


@dataclass(frozen=True, slots=True)
class Dating:
    """Each member's date and who said so by content row, and what finding them read."""

    by_row: Mapping[str, tuple[datetime | None, str]]
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

    THE ONE MATCH RULE THE INTAKE WORKER USES, tombstones included, then the one
    rule for a path against a row.
    """
    if not rows or not wanted:
        return {}
    found = backfill.resolved(view, [(when, track) for track, when in rows])
    paths = list(dict.fromkeys(path for _when, path in found))
    if not paths:
        return {}
    by_path = native.content_ids_for(db, cfg, paths)
    dates: dict[str, datetime] = {}
    for when, path in found:
        content_id = by_path.get(str(path))
        if content_id is not None and content_id in wanted and content_id not in dates:
            dates[content_id] = when
    return dates


def date_members(cfg: config.Config, db: Any, content_ids: Iterable[str]) -> Dating:
    """Each content row's date: a hearts job's frozen one, else the account's, else none.

    The library is walked once for both, and the account listed once, only when
    some row no job dates; a listing that cannot be read refuses with its reason.
    A JOB'S HEART IS READ IN EVERY STATE, since a heart the library owned when
    its job ran is still dated on its row, and A PROVIDER IDENTIFIER IS RESOLVED
    ONCE, its first dated mention winning, since the match is the slow part.
    """
    from cratekit.label import catalogue

    wanted = {str(content_id) for content_id in content_ids}
    if not wanted:
        return Dating(by_row={})
    view = match_cli.library_view(cfg)
    rows, unreadable = backfill.reported(cfg)
    found: dict[str, tuple[match.Wanted, datetime]] = {}
    for row in rows:
        if row.hearted is not None and row.ref not in found:
            found[row.ref] = (row.wanted, row.hearted)
    by_row = {
        content_id: (when, BY_JOB)
        for content_id, when in _tied(cfg, db, view, list(found.values()), wanted).items()
    }
    dating = Dating(by_row=by_row, unreadable=unreadable)
    rest = wanted - set(by_row)
    if rest:
        frozen, short = intake_cli.list_favorites(catalogue.resolve(cfg))
        dating = replace(dating, listed=True, withheld=short.withheld if short is not None else 0)
        account_rows = [
            (intake_cli.thawed(said), when)
            for said in frozen.values()
            if (when := placeholders.parse_hearted(said.get(intake_cli.HEARTED))) is not None
        ]
        for content_id, when in _tied(cfg, db, view, account_rows, rest).items():
            by_row[content_id] = (when, BY_ACCOUNT)
    by_row.update({content_id: (None, BY_NONE) for content_id in wanted - set(by_row)})
    return dating


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

    def said(self, row: str = "") -> str:
        """The member as a person reads it, by title, with the quarters it came from."""
        return f"{self.title or 'row ' + self.content_id} ({row}from {', '.join(self.quarters)})"


@dataclass(frozen=True, slots=True)
class SplitPlan:
    """The quarters to split against the home as it stands, read on one handle."""

    home: placement.Home
    quarters: tuple[Quarter, ...]
    #: Every live member of a quarter but those the author took back.
    members: tuple[Member, ...]
    #: Each month by name in order, with its members in quarter order.
    months: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    #: Each month's live members when planned, for the counts. NOT DIGESTED, so
    #: a run whose additions landed plans the same split.
    held: Mapping[str, frozenset[str]] = field(default_factory=dict)
    #: Members the author took out of All Favorites by hand: no month takes
    #: them, as the backfill never puts one back, and their quarter retires.
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
        """What the digest covers: the home, each quarter's row and members, each member's month.

        Never the months' rows or what they hold, so a run stopped after its
        additions re-plans to the digest it was approved for.
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


def _title(row: Any) -> str:
    """A content row's ``artist - title`` for the screen, a row that is not there left blank."""
    if row is None:
        return ""
    artist = str(getattr(row, "ArtistName", "") or "")
    title = str(getattr(row, "Title", "") or "")
    return f"{artist} - {title}" if artist else title


def taken_back(db: Any, home: placement.Home, content_ids: Iterable[str]) -> frozenset[str]:
    """The rows among ``content_ids`` the author took out of the source by hand.

    THE BACKFILL'S RULE (U120): a membership of the source rekordbox marked
    removed, unless the row is back in the source live, hearted again.
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
    dated: Callable[[set[str]], Dating],
) -> SplitPlan:
    """The split against ``home``, each member the author did not take back dated by ``dated``."""
    in_quarters: dict[str, list[str]] = {}
    for one in held_quarters:
        for content_id in one.members:
            in_quarters.setdefault(content_id, []).append(one.name)
    gone = taken_back(db, home, in_quarters)
    dating = dated(set(in_quarters) - gone)
    titles = {cid: _title(db.get_content(ID=cid)) for cid in in_quarters}
    every = [
        Member(cid, titles.get(cid, ""), tuple(names), *dating.by_row.get(cid, (None, BY_NONE)))
        for cid, names in in_quarters.items()
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

    With no quarter nothing is dated, so the account is never asked and the
    library never walked; a member the author took back is not dated either.
    """
    home = placement.resolve_home(db, source)
    return _planned(db, home, quarters(db, home), lambda wanted: date_members(cfg, db, wanted))


def replan(db: Any, approved: SplitPlan, *, source: str) -> SplitPlan:
    """The split planned again on this handle, the approved dates reused, so the digest compares the database.

    NOT DATED AGAIN: dating walks the library and may list the account, and
    what can move in between is the home and the quarters, which the digest
    covers. A member the approved plan never dated is undated here.
    """
    home = placement.resolve_home(db, source)
    dating = Dating(
        by_row={one.content_id: (one.hearted, one.dated_by) for one in approved.members},
        listed=approved.listed,
        withheld=approved.withheld,
        unreadable=approved.unreadable,
    )
    return _planned(db, home, quarters(db, home), lambda _wanted: dating)


def payload(planned: SplitPlan) -> dict[str, Any]:
    """The plan as the gate shows it: one item per month to fill and one per quarter to retire."""
    items: list[dict[str, Any]] = [
        {
            "action": "fill",
            "playlist": name,
            "count": len(ids),
            "adds": sum(1 for one in ids if one not in planned.held.get(name, frozenset())),
            "made": name in planned.creates,
        }
        for name, ids in planned.months.items()
    ]
    items.extend(
        {"action": "retire", "playlist": q.name, "row": q.playlist_id, "count": len(q.members)}
        for q in planned.quarters
    )
    by_source = Counter(one.dated_by for one in planned.members)
    return spine.shown(planned, items, {
        "count": len(items),
        "members": len(planned.members),
        "adds": planned.adds,
        "creates": len(planned.creates),
        "retires": len(planned.quarters),
        "undated": len(planned.undated),
        "taken back": len(planned.taken_back),
        "dates from jobs": by_source[BY_JOB],
        "dates from the account": by_source[BY_ACCOUNT],
        "jobs unread": len(planned.unreadable),
    })


def facts(planned: SplitPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.home
    where = repr(home.folder_name) if home.folder_name else "the playlist root"
    shown: dict[str, Any] = {
        "under": f"{where}, beside {home.source_name!r} (row {home.source_id})",
        "quarters to retire": [f"{one.name} ({len(one.members)})" for one in planned.quarters],
        "month playlists": [
            f"{name} ({len(ids)})" + (", made" if name in planned.creates else "")
            for name, ids in planned.months.items()
        ],
        "memberships to add": planned.adds,
    }
    if planned.undated:
        shown["undated"] = [
            one.said(f"row {one.content_id}, ") for one in planned.undated
        ]
    if planned.taken_back:
        shown["taken back"] = [
            f"{one.said(f'row {one.content_id}, ')}, removed from {home.source_name!r} in rekordbox"
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


def addition_violations(
    before: rb_writer.NodeTables,
    after: rb_writer.NodeTables,
    *,
    planned: Mapping[str, Iterable[str]],
    created: Mapping[str, tuple[str, str]],
) -> list[str]:
    """Every difference between two readings that the planned additions do not explain.

    ``planned`` maps each month row the write used to the content rows the plan
    names for it, ``created`` each row the write made to its ``(name, parent)``.
    PURE, so every branch is reachable with literal readings. It explains:

    * no content row differs, is added or disappears;
    * no membership row disappears or changes, and every one added is live and
      joins a planned month with a content row the plan names for THAT month;
    * the playlist rows added are exactly ``created``, live, plain, of the
      planned name and parent, and none disappears; an existing one moves only
      its bookkeeping, and only when it is a planned month or beside a made one.
    """
    wanted = {str(row): {str(content_id) for content_id in ids} for row, ids in planned.items()}
    p_cols = before.playlist_columns
    marker_at = p_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    name_at = p_cols.index("Name")
    kind_at = p_cols.index("Attribute")
    made: list[str] = []
    for key, (name, parent) in sorted(created.items()):
        row = after.playlists.get(key)
        if row is None:
            made.append(f"the planned month {name!r} (row {key!r}) was not made")
        elif (
            str(row[name_at]) != name
            or str(row[parent_at]) != str(parent)
            or row[marker_at]
            or int(row[kind_at] or 0) != 0
        ):
            made.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not a live plain playlist "
                f"named {name!r} under {parent!r}"
            )
    beside = {str(parent) for _name, parent in created.values()}
    violations = spine.drift(
        before,
        after,
        touches="the split",
        made=created,
        written=made,
        allowed=lambda key: (
            _BOOKKEEPING
            if key in wanted or str(before.playlists[key][parent_at]) in beside
            else frozenset()
        ),
        explains="the split's additions do not explain",
    )
    owner_at, content_at, m_marker = trees.membership_positions(before)
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
    """Refuse, before the commit, an addition the plan did not name, read from SQL."""
    spine.confined(
        db,
        lambda after: addition_violations(before, after, planned=planned, created=created),
        "the split's additions reached rows the plan did not name",
        _ORIGIN,
    )


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
    if added > 0 or retired > 0:
        session.record_commit(record, placement.RECORD_KEY, spine.change(added, retired), cfg)


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
    refuses. EACH COMMIT IS CONFINED FROM SQL BEFORE IT LANDS, the second
    admitting the playlist and membership tables alone, and no quarter is
    retired until every member it holds reads back live in its month.
    """
    watched, planned = spine.prepared(
        cfg, db, analysis_roots, lambda: replan(db, approved, source=source), approved,
        "the quarter playlists are not as the approved plan read them, so nothing was written",
        _ORIGIN,
    )
    home = planned.home
    written: list[tuple[str, str, int]] = []
    created: list[str] = []
    rows: dict[str, str] = {}
    retired: list[str] = []
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record, capture = trees.attached_capture(gates, cfg, db)

        # ── the additions, and their own commit ────────────────────────────
        added = 0
        with spine.witnessed(
            db, lambda: _record_split_commit(record, added=added, retired=0, cfg=cfg)
        ):
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
        with spine.witnessed(
            db, lambda: _record_split_commit(record, added=0, retired=len(retired), cfg=cfg)
        ):
            before = rb_writer.node_tables(db)
            for one in planned.quarters:
                rb_writer.remove_playlist_node(db, db.get_playlist(ID=one.playlist_id))
                retired.append(one.name)
            rb_writer.assert_node_changes_confined(
                db, before, moved={}, removed=[one.playlist_id for one in planned.quarters]
            )
            rb_writer.commit_guarded(db, removals=REMOVALS)
        convergence.record_fingerprint(cfg, db)
        return Split(
            months=tuple(written),
            created=tuple(created),
            retired=tuple(retired),
            session_id=record.session_id,
            disagreements=_read_back(db, planned, rows),
        )


def assert_read_back(done: Split) -> None:
    """Refuse an answer the database does not hold."""
    spine.verified(
        done,
        "the favourites read back from the database are not the split's",
        _ORIGIN,
        commits="commits",
    )


__all__ = [
    "BY_ACCOUNT",
    "BY_JOB",
    "BY_NONE",
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
