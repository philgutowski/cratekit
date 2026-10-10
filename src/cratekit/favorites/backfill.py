"""The hearts this product landed before U120, placed where a landing now puts them.

``crate favorites backfill`` is the attended half of U120: the hearts the
favourites sync downloaded and landed while nothing put them into All
Favorites and their quarter are found, shown, and placed in one guarded
session. This module gathers them and writes them; ``backfill_cli`` asks.

**WHAT A LANDED HEART IS, STATED SO THE OPEN QUESTION STAYS OPEN.** The
account holds about two hundred hearts and All Favorites holds a hundred and
nine, and the brief leaves the owned hearts that are not favourites alone
until the author answers. So a heart is placed here only when all three hold:
a hearts job on this library CARRIED it, which is the ``missing`` or
``offered`` report that a download was made from and never an ``owned`` one;
the row resolves to a file the library holds now, by the one match rule; and
that file sits where a landing puts a file, directly in a batch folder under
the music dir (:func:`cratekit.intake.landing.is_landed_path`), which no file
the source system filed does. A heart that fails any one is left where it is
and is not listed.

**THE DATE IS THE JOB'S, ELSE THE ACCOUNT'S, ONCE.** A job frozen by this
build carries each heart's date on its row, and the quarter is read from there
as the landing reads it. Every job before this build carries none, so when a
heart to place has no date the account is listed once and read by provider
identifier; a heart the account no longer carries, or dates nowhere, is an
undated heart and goes to ``Undated``, and the screen says how many. The
account is asked only when a heart needs it, so a library with nothing to
place asks nothing.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.acquire import match, match_cli
from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, jobs, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.favorites import placeholders, placement
from cratekit.intake import account_playlists, batch_name, landing, native
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.label import cli as label_cli
from cratekit.write import trees

#: The session workflow the backfill is recorded under, and its plan's kind.
WORKFLOW = "favorites-placement"

_ORIGIN = ("favorites", "backfill")


@dataclass(frozen=True, slots=True)
class LandedHeart:
    """One heart a hearts job carried that the library now holds in a batch folder."""

    ref: str
    path: Path
    content_id: str
    title: str
    job_id: str
    hearted: datetime | None
    #: Where the date came from: ``job``, ``account``, or ``none``.
    dated_by: str

    @property
    def quarter(self) -> str:
        return placeholders.quarter_label(self.hearted)


# ---------------------------------------------------------------------------
# Gathering
# ---------------------------------------------------------------------------


def hearts_jobs(cfg: config.Config) -> tuple[jobs.Job, ...]:
    """Every succeeded hearts job on this library, oldest first, however it was queued."""
    with jobs.open_store() as store:
        found = [
            job
            for job in batch_name.succeeded_intake_jobs(store, cfg)
            if account_playlists.is_hearts_job(job)
        ]
    return tuple(sorted(found, key=lambda job: (job.created, job.job_id)))


def carried(
    cfg: config.Config,
) -> tuple[tuple[account_playlists.HeartRow, ...], tuple[str, ...]]:
    """Every heart the library's hearts jobs carried, a provider identifier once, and the jobs unread.

    THE MENTION THAT KNOWS ITS DATE WINS, else the first, by the rule the
    landing's claims use. A JOB WHOSE REPORTS CANNOT BE READ IS SKIPPED AND
    NAMED rather than refusing the whole backfill: the store holds every job
    ever queued, a job a build before U57 queued has no items, and one old
    job must not make every later heart unplaceable. The landing's own claim
    still refuses on such a job, since there it is the pass's one job.
    """
    rows: dict[str, account_playlists.HeartRow] = {}
    unreadable: list[str] = []
    with jobs.open_store() as store:
        for job in hearts_jobs(cfg):
            try:
                found = account_playlists.carried_hearts(store, job)
            except CratekitError:
                unreadable.append(job.job_id)
                continue
            for row in found:
                if account_playlists.prefer_dated(rows.get(row.ref), row):
                    rows[row.ref] = row
    return tuple(rows.values()), tuple(unreadable)


def landed_paths(
    cfg: config.Config, rows: Sequence[account_playlists.HeartRow]
) -> list[tuple[account_playlists.HeartRow, Path]]:
    """Each heart with the landed file it resolves to, hearts the library lacks left out.

    Resolved against the library as the intake worker resolves, tombstones
    included, so a heart whose file was deleted on purpose is not placed. A
    heart that resolves to several files, a lossless twin beside a marked
    copy, is placed on each landed one, since each is the same heart.
    """
    if not rows:
        return []
    index, suppresses, identify = match_cli.library_view(cfg)
    found: list[tuple[account_playlists.HeartRow, Path]] = []
    for row in rows:
        resolved = match.resolve_one(row.wanted, index, suppresses=suppresses, suppression_id=identify)
        if resolved.state is not match.MatchState.MATCHED:
            continue
        for said in resolved.paths:
            path = Path(said)
            if landing.is_landed_path(cfg, path):
                found.append((row, path))
    return found


@dataclass(frozen=True, slots=True)
class Dates:
    """What the dating found: each heart's date, how many the account gave, and a short listing."""

    by_ref: dict[str, datetime | None]
    asked: int
    #: The provider's shortfall when the listing came back short (R-504), else None.
    short: catalogue.HeartsShortfall | None = None


def dated(cfg: config.Config, rows: Sequence[account_playlists.HeartRow]) -> Dates:
    """Each heart's date by provider identifier, the account asked once for those whose job knows none.

    The account is asked only when some heart's job froze no date, through the
    one hearts listing, so a listing that cannot be read refuses with the
    listing's own reason. A SHORT LISTING IS CARRIED BACK, not discarded: the
    provider counts hearts it will not serve and leaves them out, so a heart
    absent from a short listing may be a dated heart withheld, and the caller
    holds it back rather than filing it as undated for good.
    """
    dates: dict[str, datetime | None] = {row.ref: row.hearted for row in rows}
    unknown = [row.ref for row in rows if not row.known]
    if not unknown:
        return Dates(by_ref=dates, asked=0)
    found = catalogue.resolve(cfg)
    listed, short = label_cli.favourite_tracks_or_refuse(found, intake_cli.FAVORITES)
    asked = 0
    wanted = set(unknown)
    for track in listed:
        ref = str(getattr(track, "id", "") or "")
        if ref in wanted:
            when = placeholders.parse_hearted(intake_cli.hearted_on(track))
            if when is not None:
                dates[ref] = when
                asked += 1
    return Dates(by_ref=dates, asked=asked, short=short)


@dataclass(frozen=True, slots=True)
class Gathered:
    """The landed hearts, and what finding them left aside."""

    hearts: tuple[LandedHeart, ...]
    #: How many dates the account supplied.
    asked: int
    #: Hearts whose job knows no date and the account's SHORT listing did not
    #: carry: held back unplaced, since a withheld heart is not an undated one.
    held_back: tuple[LandedHeart, ...] = ()
    #: The jobs whose reports could not be read, skipped and named.
    unreadable: tuple[str, ...] = ()
    short: catalogue.HeartsShortfall | None = None


def gather(cfg: config.Config, db: Any) -> Gathered:
    """Every landed heart with its row and its date, and what was left aside."""
    rows, unreadable = carried(cfg)
    located = landed_paths(cfg, rows)
    if not located:
        return Gathered(hearts=(), asked=0, unreadable=unreadable)
    by_path = native.content_ids_for(db, cfg, [path for _row, path in located])
    needed = [row for row, path in located if str(path) in by_path]
    dates = dated(cfg, needed)
    hearts: list[LandedHeart] = []
    held: list[LandedHeart] = []
    seen: set[str] = set()
    for row, path in located:
        content_id = by_path.get(str(path))
        if content_id is None or content_id in seen:
            continue
        seen.add(content_id)
        when = dates.by_ref.get(row.ref)
        if when is not None:
            dated_by = "job" if row.known else "account"
        else:
            dated_by = "none"
        heart = LandedHeart(
            ref=row.ref,
            path=path,
            content_id=content_id,
            title=row.title,
            job_id=row.job_id,
            hearted=when,
            dated_by=dated_by,
        )
        # A HEART THE JOB COULD NOT DATE AND A SHORT LISTING DID NOT CARRY is
        # held back: the provider may have withheld it dated, and Undated is
        # a placement this engine never undoes.
        if when is None and not row.known and dates.short is not None:
            held.append(heart)
            continue
        hearts.append(heart)
    return Gathered(
        hearts=tuple(sorted(hearts, key=lambda one: (one.quarter, one.title))),
        asked=dates.asked,
        held_back=tuple(held),
        unreadable=unreadable,
        short=dates.short,
    )


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BackfillPlan:
    """The hearts to place against the home as it stands, read on one handle."""

    hearts: tuple[LandedHeart, ...]
    placements: placement.PlacementPlan
    #: How many dates the account supplied for this plan.
    asked: int
    digest: str = ""
    #: Hearts the short listing left undated, held back unplaced (R-504).
    held_back: tuple[LandedHeart, ...] = ()
    #: Jobs whose reports could not be read, skipped.
    unreadable: tuple[str, ...] = ()
    #: The listing's shortfall, when it was short.
    withheld: int = 0

    @property
    def undated(self) -> int:
        return sum(1 for one in self.hearts if one.hearted is None)

    @property
    def writes(self) -> bool:
        return self.placements.writes

    def identity(self) -> dict[str, Any]:
        return {"kind": WORKFLOW, **self.placements.identity()}


def plan(cfg: config.Config, db: Any, *, source: str) -> BackfillPlan:
    """Gather the landed hearts and plan their placement against the home."""
    home = placement.resolve_home(db, source)
    found = gather(cfg, db)
    return _planned(
        db,
        home,
        found.hearts,
        asked=found.asked,
        held_back=found.held_back,
        unreadable=found.unreadable,
        withheld=found.short.withheld if found.short is not None else 0,
    )


def _planned(
    db: Any,
    home: placement.Home,
    hearts: Sequence[LandedHeart],
    *,
    asked: int,
    held_back: Sequence[LandedHeart] = (),
    unreadable: Sequence[str] = (),
    withheld: int = 0,
) -> BackfillPlan:
    placements = placement.plan_placements(
        db, home, [(one.content_id, one.hearted, one.title) for one in hearts]
    )
    planned = BackfillPlan(
        hearts=tuple(hearts),
        placements=placements,
        asked=asked,
        held_back=tuple(held_back),
        unreadable=tuple(unreadable),
        withheld=withheld,
    )
    return replace(planned, digest=digest_of(planned.identity()))


def replan(db: Any, approved: BackfillPlan, *, source: str) -> BackfillPlan:
    """The approved hearts planned again on this handle, so the digest compares the database.

    THE HEARTS ARE NOT GATHERED AGAIN: they are what was approved, and the
    walk that found them is minutes on a real library. What can move between
    the approval and the write is the home and what it holds, and that is
    what the digest covers.
    """
    return _planned(
        db,
        placement.resolve_home(db, source),
        approved.hearts,
        asked=approved.asked,
        held_back=approved.held_back,
        unreadable=approved.unreadable,
        withheld=approved.withheld,
    )


def payload(planned: BackfillPlan, cfg: config.Config) -> dict[str, Any]:
    """The plan as the gate shows it: one item per heart."""
    by_row = {one.content_id: one for one in planned.placements.placements}
    root = Path(cfg.library.root)
    items = []
    for heart in planned.hearts:
        one = by_row[heart.content_id]
        try:
            shown = str(heart.path.relative_to(root))
        except ValueError:
            shown = str(heart.path)
        items.append(
            {
                "action": "place",
                "row": heart.content_id,
                "title": heart.title,
                "path": shown,
                "quarter": one.quarter,
                "into_source": one.into_source,
                "into_quarter": one.into_quarter,
                "dated_by": heart.dated_by,
                "job": heart.job_id,
            }
        )
    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "adds": planned.placements.adds,
            "creates": len(planned.placements.creates),
            "undated": planned.undated,
            "dates from the account": planned.asked,
            "held back": len(planned.held_back),
            "jobs unread": len(planned.unreadable),
        },
        "chunk": None,
    }


def facts(planned: BackfillPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.placements.home
    where = f"{home.source_name!r} (row {home.source_id})"
    if home.folder_name:
        where += f" under {home.folder_name!r}"
    facts: dict[str, Any] = {
        "into": where,
        "landed hearts": len(planned.hearts),
        "memberships to add": planned.placements.adds,
        "quarter playlists to create": list(planned.placements.creates),
        "undated": planned.undated,
        "dates asked of the account": planned.asked,
    }
    if planned.held_back:
        facts["held back"] = (
            f"{len(planned.held_back)} heart(s) the account's short listing did not date, "
            f"{planned.withheld} withheld by the provider; not placed this run"
        )
    if planned.unreadable:
        facts["jobs unread"] = list(planned.unreadable)
    return facts


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Backfilled:
    placed: placement.Placed
    session_id: str
    #: What read back from SQL disagrees with the plan, empty when nothing does.
    disagreements: tuple[str, ...] = ()


def _record_backfill_commit(
    record: session.SessionRecord, placed: placement.Placed, cfg: config.Config
) -> None:
    """Record the commit on the session, as rows created under the favourites key."""
    if placed.added <= 0:
        return
    record.detail[placement.PLACED_KEY] = placed.to_json()
    session.record_commit(
        record,
        placement.RECORD_KEY,
        session.ChangeSummary((session.TreeChange(tree=placement.RECORD_KEY, created=placed.added),)),
        cfg,
    )


def _read_back(db: Any, placed: placement.Placed, planned: BackfillPlan) -> tuple[str, ...]:
    """Each playlist that, read live, lacks a heart the plan says is in it.

    EVERY QUARTER THE PLAN NAMES, not only those the write touched: a heart
    already in its quarter was not written and is read back all the same, by
    the row the write used or the one the plan found live, so a quarter row
    that went between the two acts is a disagreement and not a silence.
    """
    problems: list[str] = []
    wanted_source = {one.content_id for one in planned.placements.placements}
    missing = sorted(wanted_source - placement.members(db, placed.source_id))
    if missing:
        problems.append(f"{placed.source_name!r} lacks {len(missing)} row(s): {', '.join(missing)}")
    rows = dict(planned.placements.home.present)
    rows.update({name: row for name, row, _count in placed.quarters})
    for name in sorted({one.quarter for one in planned.placements.placements}):
        wanted = {one.content_id for one in planned.placements.placements if one.quarter == name}
        row = rows.get(name)
        held = placement.members(db, row) if row else frozenset()
        gone = sorted(wanted - held)
        if gone:
            problems.append(f"{name!r} lacks {len(gone)} row(s): {', '.join(gone)}")
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

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST and a digest that moved
    refuses, since the approved one was read on a handle that has since
    closed. THE SESSION SPINE IS CALLED, NOT REBUILT, as every membership
    writer calls it: the gates with a record kept, a capture verified before
    anything is written, the analysis watch over the roots named, the commit
    witness, the guarded commit, the record and the fingerprint.
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
            "the favourites are not as the approved plan read them, so no heart was "
            "placed; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.digest, "now": again.digest},
        )
    planned = again
    pairs = [
        (one.content_id, one.quarter)
        for one in planned.placements.placements
        if one.into_source or one.into_quarter
    ]
    # THE OUT OF BAND RESTORE IS DETECTED BEFORE THE FINGERPRINT IS TOUCHED,
    # as every writer that records one does: a database recovered from a
    # backup is compared and every native tree it emptied is marked, so the
    # fingerprint this write records afterwards blesses nothing. The Favorites
    # folder is no tree, so the detection marks and never refuses here.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
        placed: placement.Placed | None = None
        try:
            placed = placement.place(db, planned.placements.home, pairs)
            rb_writer.commit_guarded(db)
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed and placed is not None:
                _record_backfill_commit(record, placed, cfg)
            raise
        _record_backfill_commit(record, placed, cfg)
        if placed.added:
            convergence.record_fingerprint(cfg, db)
        disagreements = _read_back(db, placed, planned)
        session_id = record.session_id
    return Backfilled(placed=placed, session_id=session_id, disagreements=disagreements)


def assert_read_back(done: Backfilled) -> None:
    """Refuse an answer the database does not hold."""
    if done.disagreements:
        raise refuse(
            "session-committed-unverified",
            "the favourites read back from the database are not the plan's: "
            + "; ".join(done.disagreements)
            + "; the commit landed and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"disagreements": list(done.disagreements), "session": done.session_id},
        )


__all__ = [
    "Backfilled",
    "BackfillPlan",
    "Dates",
    "Gathered",
    "LandedHeart",
    "WORKFLOW",
    "apply",
    "assert_read_back",
    "carried",
    "dated",
    "facts",
    "gather",
    "hearts_jobs",
    "landed_paths",
    "payload",
    "plan",
    "replan",
]
