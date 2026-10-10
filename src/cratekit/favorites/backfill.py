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
from cratekit.core import config, convergence, jobs, rb_writer, session, snapshot
from cratekit.core.cause import refuse
from cratekit.favorites import placeholders, placement
from cratekit.intake import account_playlists, landing, native
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
            for job in jobs.list_jobs(store)
            if account_playlists.is_hearts_job(job)
            and job.library_id == cfg.library.volume_id
            and job.state is jobs.JobState.SUCCEEDED
        ]
    return tuple(sorted(found, key=lambda job: (job.created, job.job_id)))


def carried(cfg: config.Config) -> tuple[account_playlists.HeartRow, ...]:
    """Every heart the library's hearts jobs carried, a provider identifier once.

    THE FIRST DATED MENTION WINS, else the first mention: a heart listed by
    several jobs is one heart, and a job frozen by this build knows its date
    where an older one does not.
    """
    rows: dict[str, account_playlists.HeartRow] = {}
    with jobs.open_store() as store:
        for job in hearts_jobs(cfg):
            for row in account_playlists.carried_hearts(store, job):
                held = rows.get(row.ref)
                if held is None or (held.hearted is None and row.hearted is not None):
                    rows[row.ref] = row
    return tuple(rows.values())


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


def dated(
    cfg: config.Config, rows: Sequence[account_playlists.HeartRow]
) -> tuple[dict[str, datetime | None], int]:
    """Each heart's date by provider identifier, the account asked once for the undated.

    Answers the dates and how many came from the account. The account is asked
    only when some heart lacks a date, through the one hearts listing, so a
    short listing is read as the listing verb reads it and a listing that
    cannot be read refuses with the listing's own reason.
    """
    dates: dict[str, datetime | None] = {row.ref: row.hearted for row in rows}
    undated = [ref for ref, when in dates.items() if when is None]
    if not undated:
        return dates, 0
    found = catalogue.resolve(cfg)
    listed, _short = label_cli.favourite_tracks_or_refuse(found, intake_cli.FAVORITES)
    asked = 0
    for track in listed:
        ref = str(getattr(track, "id", "") or "")
        if ref in dates and dates[ref] is None:
            when = placeholders.parse_hearted(intake_cli.hearted_on(track))
            if when is not None:
                dates[ref] = when
                asked += 1
    return dates, asked


def gather(cfg: config.Config, db: Any) -> tuple[tuple[LandedHeart, ...], int]:
    """Every landed heart with its row and its date. Answers the hearts and the dates asked."""
    rows = carried(cfg)
    located = landed_paths(cfg, rows)
    if not located:
        return (), 0
    by_path = native.content_ids_for(db, cfg, [path for _row, path in located])
    needed = [row for row, path in located if str(path) in by_path]
    dates, asked = dated(cfg, needed)
    hearts: list[LandedHeart] = []
    seen: set[str] = set()
    for row, path in located:
        content_id = by_path.get(str(path))
        if content_id is None or content_id in seen:
            continue
        seen.add(content_id)
        when = dates.get(row.ref)
        hearts.append(
            LandedHeart(
                ref=row.ref,
                path=path,
                content_id=content_id,
                title=row.title,
                job_id=row.job_id,
                hearted=when,
                dated_by="none" if when is None else ("job" if row.hearted is not None else "account"),
            )
        )
    return tuple(sorted(hearts, key=lambda one: (one.quarter, one.title))), asked


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
    hearts, asked = gather(cfg, db)
    return _planned(db, home, hearts, asked)


def _planned(db: Any, home: placement.Home, hearts: Sequence[LandedHeart], asked: int) -> BackfillPlan:
    placements = placement.plan_placements(
        db, home, [(one.content_id, one.hearted, one.title) for one in hearts]
    )
    planned = BackfillPlan(hearts=tuple(hearts), placements=placements, asked=asked)
    return replace(planned, digest=digest_of(planned.identity()))


def replan(db: Any, approved: BackfillPlan, *, source: str) -> BackfillPlan:
    """The approved hearts planned again on this handle, so the digest compares the database.

    THE HEARTS ARE NOT GATHERED AGAIN: they are what was approved, and the
    walk that found them is minutes on a real library. What can move between
    the approval and the write is the home and what it holds, and that is
    what the digest covers.
    """
    return _planned(db, placement.resolve_home(db, source), approved.hearts, approved.asked)


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
        },
        "chunk": None,
    }


def facts(planned: BackfillPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.placements.home
    where = f"{home.source_name!r} (row {home.source_id})"
    if home.folder_name:
        where += f" under {home.folder_name!r}"
    return {
        "into": where,
        "landed hearts": len(planned.hearts),
        "memberships to add": planned.placements.adds,
        "quarter playlists to create": list(planned.placements.creates),
        "undated": planned.undated,
        "dates asked of the account": planned.asked,
    }


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
    """Each playlist that, read live, lacks a heart the plan put in it."""
    problems: list[str] = []
    wanted_source = {one.content_id for one in planned.placements.placements}
    missing = sorted(wanted_source - placement.members(db, placed.source_id))
    if missing:
        problems.append(f"{placed.source_name!r} lacks {len(missing)} row(s): {', '.join(missing)}")
    for name, row, _count in placed.quarters:
        wanted = {one.content_id for one in planned.placements.placements if one.quarter == name}
        gone = sorted(wanted - placement.members(db, row))
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
