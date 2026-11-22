"""The owned hearts the account carries, placed where a landing now puts them (U120, U146).

``crate favorites backfill`` asks; this module gathers and writes, and the
native landing calls :func:`plan_owned` and :func:`apply` for a pass that
brought no file. A heart to place is one a hearts job reported, in any state,
whose row resolves to a file the library holds, and that All Favorites and a
dated playlist beside it do not both hold (:func:`placement.filed`).

**THE ACCOUNT IS ASKED ONCE, ONLY WHEN A HEART NEEDS PLACING**: a heart a whole
listing lacks is taken back, one a short or uncounted listing lacks is held
back, and one the author took out of All Favorites stays out. **THE DATE IS THE
JOB'S, ELSE THE ACCOUNT'S**, else ``Undated``. **NOTHING IS TAKEN AWAY** (R36).

Layer: modules.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Sequence

from cratekit.acquire import match, match_cli
from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, jobs, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.favorites import colour, placeholders, placement, spine
from cratekit.intake import account_playlists, batch_name, native
from cratekit.intake import cli as intake_cli
from cratekit.write import trees

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: The session workflow the backfill is recorded under, and its plan's kind.
WORKFLOW = "favorites-placement"

_ORIGIN = ("favorites", "backfill")

#: Why a heart was taken back, as the screen names it.
REMOVED_IN_REKORDBOX = "removed from the playlist in rekordbox"
OFF_THE_ACCOUNT = "no longer on the account"


@dataclass(frozen=True, slots=True)
class OwnedHeart:
    """One heart a hearts job reported whose track the library holds now, and its row."""

    ref: str
    path: Path
    content_id: str
    title: str
    job_id: str
    hearted: datetime | None
    #: Where the date came from: ``job``, ``account``, or ``none``; for a
    #: heart taken back, why.
    dated_by: str
    #: Whether the job froze a date key at all; only a row with none is dated
    #: from the account, so a job's "no date" is Undated by both paths.
    known: bool = True

    @property
    def month(self) -> str:
        return placeholders.month_label(self.hearted)

    @classmethod
    def of(
        cls, row: account_playlists.HeartRow, path: Path, content_id: str, *, known: bool = True
    ) -> OwnedHeart:
        """The heart a job's row reports, on the library row its file is."""
        dated_by = "job" if row.hearted is not None else "none"
        return cls(row.ref, path, content_id, row.title, row.job_id, row.hearted, dated_by, known)


def hearts_jobs(cfg: config.Config) -> tuple[jobs.Job, ...]:
    """Every succeeded hearts job on this library, oldest first, however it was queued."""
    with jobs.open_store() as store:
        found = [
            job
            for job in batch_name.succeeded_intake_jobs(store, cfg)
            if account_playlists.is_hearts_job(job)
        ]
    return tuple(sorted(found, key=lambda job: (job.created, job.job_id)))


def reported(cfg: config.Config) -> tuple[list[account_playlists.HeartRow], tuple[str, ...]]:
    """Every row the library's hearts jobs reported, any state, oldest job first, and jobs unread.

    A JOB WHOSE REPORTS CANNOT BE READ IS SKIPPED AND NAMED rather than refusing:
    the store holds every job ever queued, one queued before U57 has no items,
    and one old job must not make every later heart unplaceable.
    """
    rows: list[account_playlists.HeartRow] = []
    unreadable: list[str] = []
    with jobs.open_store() as store:
        for job in hearts_jobs(cfg):
            try:
                rows.extend(account_playlists.carried_hearts(store, job, states=None))
            except CratekitError:
                unreadable.append(job.job_id)
    return rows, tuple(unreadable)


def carried(
    cfg: config.Config,
) -> tuple[tuple[account_playlists.HeartRow, ...], tuple[str, ...]]:
    """Every heart the library's hearts jobs reported, in any state, a provider identifier once, and the jobs unread.

    THE MENTION THAT KNOWS ITS DATE WINS, else the first, by the rule the
    landing's claims use.
    """
    found, unreadable = reported(cfg)
    rows: dict[str, account_playlists.HeartRow] = {}
    for row in found:
        if account_playlists.prefer_dated(rows.get(row.ref), row):
            rows[row.ref] = row
    return tuple(rows.values()), unreadable


def owned_paths(
    cfg: config.Config, rows: Sequence[account_playlists.HeartRow]
) -> list[tuple[account_playlists.HeartRow, Path]]:
    """Each heart with the library file it resolves to now, hearts the library lacks left out.

    Resolved as the intake worker resolves, tombstones included. A heart that
    resolves to several files, a lossless twin beside a marked copy, is placed
    on each; where the file sits is not asked (U146).
    """
    if not rows:
        return []
    return resolved(match_cli.library_view(cfg), [(row, row.wanted) for row in rows])


def resolved(view: tuple[Any, Any, Any], wanted: Iterable[tuple[Any, match.Wanted]]) -> list:
    """Each ``(key, track)`` with every library file the one match rule resolves the track to."""
    index, suppresses, identify = view
    found: list[tuple[Any, Path]] = []
    for key, track in wanted:
        hit = match.resolve_one(track, index, suppresses=suppresses, suppression_id=identify)
        if hit.state is match.MatchState.MATCHED:
            found.extend((key, Path(said)) for said in hit.paths)
    return found


@dataclass(frozen=True, slots=True)
class Listing:
    """The account's hearts as listed once: each one's date, and whether the list is whole."""

    #: Every provider identifier the listing carried, with its date or None.
    dates: dict[str, datetime | None]
    #: The provider's shortfall when the listing came back short (R-504), else None.
    short: catalogue.HeartsShortfall | None = None
    #: Whether the listing is known WHOLE: a count was published and reached.
    #: A listing with no published count says nothing about a heart it lacks.
    whole: bool = False


def listed(cfg: config.Config) -> Listing:
    """The account's hearts, listed once through the one hearts listing.

    A listing that cannot be read refuses with its own reason. A SHORT LISTING
    IS CARRIED BACK: a heart absent from it may be one the provider withheld,
    and the caller holds it back rather than taking it back.
    """
    from cratekit.label import catalogue
    from cratekit.label import cli as label_cli

    found = catalogue.resolve(cfg)
    tracks, short = label_cli.favourite_tracks_or_refuse(found, intake_cli.FAVORITES)
    # WHOLE ONLY WHEN THE PROVIDER PUBLISHED A COUNT AND THE LISTING REACHED IT.
    declared = getattr(found, "hearts_declared", None)
    whole = short is None and declared is not None and len(tracks) >= declared
    dates: dict[str, datetime | None] = {}
    for track in tracks:
        ref = str(getattr(track, "id", "") or "")
        if not ref:
            # A ROW WITH NO IDENTIFIER IS NO HEART'S EVIDENCE.
            continue
        when = placeholders.parse_hearted(intake_cli.hearted_on(track))
        if dates.get(ref) is None:
            dates[ref] = when
    return Listing(dates=dates, short=short, whole=whole)


def source_members(db: Any, home: placement.Home) -> tuple[tuple[str, str], ...]:
    """Every live member of the source playlist with its title, in row order.

    THE ROWS THE BACKFILL COLOURS WITHOUT A JOB (U153): a member of All
    Favorites is a favourite whatever put it there.
    """
    found: list[tuple[str, str]] = []
    for content_id in _member_order(placement.members(db, home.source_id)):
        row = db.get_content(ID=content_id)
        if row is None:
            continue
        found.append((content_id, str(getattr(row, "Title", "") or "")))
    return tuple(found)


def _member_order(content_ids: Iterable[str]) -> list[str]:
    """A stable order over content ids: numeric ones by value, anything else after, by its text."""
    return sorted(
        content_ids, key=lambda c: (0, int(c), "") if str(c).isdigit() else (1, 0, str(c))
    )


def gather(cfg: config.Config, db: Any, *, home: placement.Home) -> BackfillPlan:
    """Every owned heart to place with its row and its date, and what was left aside, unplanned."""
    rows, unreadable = carried(cfg)
    located = owned_paths(cfg, rows)
    left = BackfillPlan(hearts=(), unreadable=unreadable, recolour=source_members(db, home))
    if not located:
        return left
    by_path = native.content_ids_for(db, cfg, [path for _row, path in located])
    # THE SOURCE MEMBERS ARE READ ONCE, by source_members for the colour read.
    in_source = frozenset(cid for cid, _title in left.recolour)
    filed = placement.filed(db, home)
    # THE AUTHOR'S DECISION IN REKORDBOX: a membership marked removed and not
    # live again was taken out by hand, and is never put back.
    removed = placement.members_marked_removed(db, home.source_id) - in_source
    candidates: list[OwnedHeart] = []
    taken: list[OwnedHeart] = []
    seen: set[str] = set()
    already = 0
    for row, path in located:
        content_id = by_path.get(str(path))
        if content_id is None or content_id in seen:
            continue
        seen.add(content_id)
        if content_id in in_source and content_id in filed:
            already += 1
            continue
        heart = OwnedHeart.of(row, path, content_id, known=row.known)
        if content_id in removed:
            taken.append(replace(heart, dated_by=REMOVED_IN_REKORDBOX))
            continue
        candidates.append(heart)
    if not candidates:
        return replace(left, taken_back=tuple(taken), already=already)
    listing = listed(cfg)
    hearts: list[OwnedHeart] = []
    held: list[OwnedHeart] = []
    asked = 0
    for heart in candidates:
        # NOT ON THE ACCOUNT NOW: taken back off a listing known whole, else
        # held back, since the provider may have withheld it.
        if not heart.ref or heart.ref not in listing.dates:
            if listing.whole:
                taken.append(replace(heart, dated_by=OFF_THE_ACCOUNT))
            else:
                held.append(heart)
            continue
        # THE JOB'S DATE FIRST, AND ITS "NO DATE" TOO: only a row frozen with no
        # key at all, before U120, is dated from the listing.
        if not heart.known:
            when = listing.dates.get(heart.ref)
            if when is not None:
                heart = replace(heart, hearted=when, dated_by="account")
                asked += 1
        hearts.append(heart)
    return replace(
        left,
        hearts=tuple(sorted(hearts, key=lambda one: (one.month, one.title))),
        asked=asked,
        held_back=tuple(held),
        withheld=listing.short.withheld if listing.short is not None else 0,
        taken_back=tuple(taken),
        uncounted=not listing.whole and listing.short is None,
        already=already,
    )


def owned_in_library(
    cfg: config.Config, db: Any, rows: Sequence[account_playlists.HeartRow]
) -> tuple[OwnedHeart, ...]:
    """A pass's owned hearts with the row each one's report file is, for the landing (U146).

    THE REPORT'S OWN FILES, the first one an active row holds alone (U128). A
    ROW WHOSE JOB FROZE NO DATE KEY IS LEFT TO THE BACKFILL, which can date it
    from the account, since Undated is for good. The first mention wins.
    """
    known = [row for row in rows if row.known and row.paths]
    paths = [Path(said) for row in known for said in row.paths]
    if not paths:
        return ()
    by_path = native.single_rows_for(db, cfg, paths)
    found: list[OwnedHeart] = []
    seen: set[str] = set()
    for row in known:
        for said in row.paths:
            content_id = by_path.get(str(Path(said)))
            if content_id is None:
                continue
            if content_id not in seen:
                seen.add(content_id)
                found.append(OwnedHeart.of(row, Path(said), content_id))
            break
    return tuple(found)


@dataclass(frozen=True, slots=True)
class BackfillPlan:
    """The hearts to place against the home as it stands, read on one handle."""

    hearts: tuple[OwnedHeart, ...]
    #: None until :func:`_planned` places the hearts against the home.
    placements: placement.PlacementPlan | None = None
    #: How many dates the account supplied for this plan.
    asked: int = 0
    digest: str = ""
    #: Hearts a listing not known whole did not carry, held back unplaced (R-504).
    held_back: tuple[OwnedHeart, ...] = ()
    #: Jobs whose reports could not be read, skipped.
    unreadable: tuple[str, ...] = ()
    #: The listing's shortfall, when it was short.
    withheld: int = 0
    #: Hearts the author took back, in rekordbox or on the account. Not placed.
    taken_back: tuple[OwnedHeart, ...] = ()
    #: The account was listed and published no count.
    uncounted: bool = False
    #: Owned hearts already in All Favorites and a dated playlist, not listed.
    already: int = 0
    #: The source's members the colour read covered, carried so the replan
    #: reads the same rows' colour again rather than walking the playlist (U153).
    recolour: tuple[tuple[str, str], ...] = ()

    @property
    def undated(self) -> int:
        return sum(1 for one in self.hearts if one.hearted is None)

    @property
    def by_month(self) -> dict[str, int]:
        """How many hearts go to each month, in month order, Undated last."""
        counts = Counter(one.month for one in self.placements.placements)
        return dict(sorted(counts.items(), key=lambda kv: (kv[0] == placeholders.UNDATED, kv[0])))

    @property
    def writes(self) -> bool:
        return self.placements.writes

    def identity(self) -> dict[str, Any]:
        return {"kind": WORKFLOW, **self.placements.identity()}


def plan(cfg: config.Config, db: Any, *, source: str) -> BackfillPlan:
    """Gather the owned hearts and plan their placement against the home."""
    home = placement.resolve_home(db, source)
    return _planned(db, home, gather(cfg, db, home=home))


def plan_owned(
    cfg: config.Config, db: Any, *, source: str, rows: Sequence[account_playlists.HeartRow]
) -> BackfillPlan:
    """The landing's owned hearts that All Favorites lacks, planned as the backfill plans (U146).

    FOR A LANDING THAT BROUGHT NO FILE, under the landing's gate and through
    :func:`apply`. A heart taken out of All Favorites by hand and still hearted
    joins again: dropping a favourite is un-hearting on the account as well.
    The account is not listed again; the pass's own job is the listing.
    """
    home = placement.resolve_home(db, source)
    in_source = placement.members(db, home.source_id)
    hearts = tuple(
        one for one in owned_in_library(cfg, db, rows) if one.content_id not in in_source
    )
    return _planned(db, home, BackfillPlan(hearts=hearts))


def _planned(db: Any, home: placement.Home, gathered: BackfillPlan) -> BackfillPlan:
    """``gathered``'s hearts and recolours planned against ``home`` on this handle, and digested."""
    hearts = [(one.content_id, one.hearted, one.title) for one in gathered.hearts]
    placements = placement.plan_placements(db, home, hearts, recolour=gathered.recolour)
    planned = replace(gathered, placements=placements)
    return replace(planned, digest=digest_of(planned.identity()))


def replan(db: Any, approved: BackfillPlan, *, source: str) -> BackfillPlan:
    """The approved hearts planned again on this handle, so the digest compares the database.

    NOT GATHERED AGAIN: the walk that found them is minutes on a real library,
    and what can move in between is the home, what it holds and each row's
    colour, which the digest covers.
    """
    return _planned(db, placement.resolve_home(db, source), approved)


def payload(planned: BackfillPlan, cfg: config.Config) -> dict[str, Any]:
    """The plan as the gate shows it: one item per heart."""
    by_row = {one.content_id: one for one in planned.placements.placements}
    root = Path(cfg.library.root)
    items = []
    for heart in planned.hearts:
        one = by_row[heart.content_id]
        shown = heart.path.relative_to(root) if heart.path.is_relative_to(root) else heart.path
        items.append(
            {
                "action": "place",
                "row": heart.content_id,
                "title": heart.title,
                "path": str(shown),
                "month": one.month,
                "into_source": one.into_source,
                "into_month": one.into_month,
                "into_colour": one.into_colour,
                "dated_by": heart.dated_by,
                "job": heart.job_id,
            }
        )
    # THE ROWS PLACED ALREADY THAT TAKE PINK (U153), so the screen lists every row written.
    items.extend(
        {"action": "colour", "row": one.content_id, "title": one.title}
        for one in planned.placements.recolour
    )
    return spine.shown(planned, items, {
        "count": len(planned.hearts),
        "adds": planned.placements.adds,
        "creates": len(planned.placements.creates),
        "colours": planned.placements.colours,
        "colour held": len(planned.placements.held),
        "undated": planned.undated,
        "dates from the account": planned.asked,
        "held back": len(planned.held_back),
        "taken back": len(planned.taken_back),
        "jobs unread": len(planned.unreadable),
        "already placed": planned.already,
    })


def facts(planned: BackfillPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.placements.home
    where = f"{home.source_name!r} (row {home.source_id})"
    if home.folder_name:
        where += f" under {home.folder_name!r}"
    facts: dict[str, Any] = {
        "into": where,
        "hearts to place": len(planned.hearts),
        "by month": [f"{month}: {count}" for month, count in planned.by_month.items()],
        "memberships to add": planned.placements.adds,
        "month playlists to create": list(planned.placements.creates),
        "rows to colour Pink": planned.placements.colours,
        "undated": planned.undated,
        "dates asked of the account": planned.asked,
        "already placed": planned.already,
    }
    if planned.placements.colour_skipped:
        facts["rows to colour Pink"] = f"none, {planned.placements.colour_skipped}"
    if planned.placements.held:
        facts["colour held"] = [one.said() for one in planned.placements.held]
    if planned.held_back:
        why = (
            f"{planned.withheld} withheld by the provider"
            if planned.withheld
            else "the listing published no count, so a heart it lacks cannot be told from one withheld"
        )
        facts["held back"] = (
            f"{len(planned.held_back)} heart(s) the account's listing did not carry, {why}; "
            f"not placed this run"
        )
    if planned.taken_back:
        facts["taken back"] = [
            f"{one.title}, {one.dated_by}" for one in planned.taken_back
        ]
    if planned.unreadable:
        facts["jobs unread"] = list(planned.unreadable)
    return facts


def landing_facts(planned: BackfillPlan) -> dict[str, Any]:
    """The facts a landing that brought no file shows over its owned hearts (U146).

    THE BACKFILL'S, less the account and the hearts already placed, which the
    landing never asks.
    """
    shown = facts(planned)
    for key in ("dates asked of the account", "already placed"):
        shown.pop(key, None)
    shown["files to land"] = 0
    return shown


@dataclass(frozen=True, slots=True)
class Backfilled:
    placed: placement.Placed
    session_id: str
    #: What read back from SQL disagrees with the plan, empty when nothing does.
    disagreements: tuple[str, ...] = ()


def _record_backfill_commit(
    record: session.SessionRecord, placed: placement.Placed, cfg: config.Config
) -> None:
    """Record the commit on the session, memberships created and rows coloured under the favourites key."""
    if placed.added <= 0 and not placed.coloured:
        return
    record.detail[placement.PLACED_KEY] = placed.to_json()
    change = spine.change(placed.added, len(placed.coloured))
    session.record_commit(record, placement.RECORD_KEY, change, cfg)


def _read_back(db: Any, placed: placement.Placed, planned: BackfillPlan) -> tuple[str, ...]:
    """Each playlist that, read live, lacks a heart the plan says is in it.

    EVERY MONTH THE PLAN NAMES, by the row the write used or the one the plan
    found live, so a month row that went between the two acts is a
    disagreement and not a silence.
    """
    problems: list[str] = []
    wanted_source = {one.content_id for one in planned.placements.placements}
    missing = sorted(wanted_source - placement.members(db, placed.source_id))
    if missing:
        problems.append(f"{placed.source_name!r} lacks {len(missing)} row(s): {', '.join(missing)}")
    rows = dict(planned.placements.home.present)
    rows.update({name: row for name, row, _count in placed.months})
    for name in sorted({one.month for one in planned.placements.placements}):
        wanted = {one.content_id for one in planned.placements.placements if one.month == name}
        row = rows.get(name)
        held = placement.members(db, row) if row else frozenset()
        gone = sorted(wanted - held)
        if gone:
            problems.append(f"{name!r} lacks {len(gone)} row(s): {', '.join(gone)}")
    # AND EVERY ROW THE PLAN COLOURS READS PINK (U153).
    pink = planned.placements.pink
    grey = [
        row
        for row in planned.placements.to_colour
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") != pink
    ]
    if grey:
        problems.append(f"{len(grey)} row(s) do not read Pink: {', '.join(grey)}")
    return tuple(problems)


def apply(
    cfg: config.Config,
    db: Any,
    approved: BackfillPlan,
    *,
    source: str,
    analysis_roots: Iterable[Path | str],
) -> Backfilled:
    """Place the approved hearts in one guarded commit, then read them back.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST and a digest that moved refuses.
    """
    watched, planned = spine.prepared(
        cfg, db, analysis_roots, lambda: replan(db, approved, source=source), approved,
        "the favourites are not as the approved plan read them, so no heart was placed",
        _ORIGIN,
    )
    shown = planned.placements
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record, capture = trees.attached_capture(gates, cfg, db)
        placed: placement.Placed | None = None

        def landed() -> None:
            if placed is not None:
                _record_backfill_commit(record, placed, cfg)

        with spine.witnessed(db, landed):
            placed = placement.place(
                db,
                shown.home,
                [(one.content_id, one.month) for one in shown.placements if one.adds],
                pink=shown.pink,
                to_colour=shown.to_colour,
                held=shown.held,
                colour_skipped=shown.colour_skipped,
            )
            rb_writer.commit_guarded(db)
        if placed.added or placed.coloured:
            convergence.record_fingerprint(cfg, db)
        return Backfilled(
            placed=placed,
            session_id=record.session_id,
            disagreements=_read_back(db, placed, planned),
        )


def assert_read_back(done: Backfilled) -> None:
    """Refuse an answer the database does not hold."""
    spine.verified(done, "the favourites read back from the database are not the plan's", _ORIGIN)


__all__ = [
    "Backfilled",
    "BackfillPlan",
    "Listing",
    "OFF_THE_ACCOUNT",
    "OwnedHeart",
    "REMOVED_IN_REKORDBOX",
    "WORKFLOW",
    "apply",
    "assert_read_back",
    "carried",
    "facts",
    "gather",
    "hearts_jobs",
    "landing_facts",
    "listed",
    "owned_in_library",
    "owned_paths",
    "reported",
    "payload",
    "plan",
    "plan_owned",
    "replan",
    "source_members",
]
