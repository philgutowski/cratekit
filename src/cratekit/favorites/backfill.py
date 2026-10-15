"""The owned hearts the account carries, placed where a landing now puts them (U120, U146).

``crate favorites backfill`` is the attended half of the favourites
placement: the hearts the library owns that are not in All Favorites and
their month are found, shown, and placed in one guarded session. This module
gathers them and writes them; ``backfill_cli`` asks. The native landing given
a pass calls :func:`plan_owned` and :func:`apply` too, for the owned hearts of
a pass that brought no file (U146).

**WHAT A HEART TO PLACE IS, SINCE U146.** The author answered U120's open
question on 2026-10-14: a heart on a track the library owns is a favourite,
whether this product downloaded it or the library held it already. So a heart
is placed here when a hearts job on this library REPORTED it, in any state,
and the row resolves to a file the library holds now, by the one match rule.
U120's two narrowings are gone: the job no longer has to have downloaded it,
and the file no longer has to sit in a batch folder under the music dir. A
heart All Favorites holds is placed only when no dated playlist beside it
holds it (:func:`placement.filed`), the heart a landing put in All Favorites
with no month; any other is already placed and is counted, not listed.

**THE ACCOUNT IS ASKED ONCE, AND ONLY WHEN A HEART NEEDS PLACING.** Every
heart to place is checked against the account's hearts, listed once, because
the backlog is every heart a job ever reported and the author may have taken
one back since. A heart a whole listing no longer carries is taken back and
named; one a short listing, or one with no published count, lacks is held
back and named, since it may be a heart the provider withheld. A heart the
author took out of All Favorites in rekordbox, a membership marked removed, is
taken back and named too, run after run.

**THE DATE IS THE JOB'S, ELSE THE ACCOUNT'S.** A job frozen since U120 carries
each heart's date on its row, and the month is read from there as the landing
reads it; a row with no date is dated from the listing, and a heart dated
nowhere goes to ``Undated``, and the screen says how many.

**NOTHING HERE TAKES A HEART OR A MEMBERSHIP AWAY**, R36 and the author's
"both sides add" of 2026-10-14.

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
from cratekit.intake import account_playlists, batch_name, native
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.label import cli as label_cli
from cratekit.write import trees

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

    @property
    def month(self) -> str:
        return placeholders.month_label(self.hearted)


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
    """Every heart the library's hearts jobs reported, in any state, a provider identifier once, and the jobs unread.

    EVERY STATE SINCE U146: an owned heart is a heart to place as much as one
    a job downloaded. THE MENTION THAT KNOWS ITS DATE WINS, else the first, by
    the rule the landing's claims use. A JOB WHOSE REPORTS CANNOT BE READ IS
    SKIPPED AND NAMED rather than refusing the whole backfill: the store holds
    every job ever queued, a job a build before U57 queued has no items, and
    one old job must not make every later heart unplaceable.
    """
    rows: dict[str, account_playlists.HeartRow] = {}
    unreadable: list[str] = []
    with jobs.open_store() as store:
        for job in hearts_jobs(cfg):
            try:
                found = account_playlists.carried_hearts(store, job, states=None)
            except CratekitError:
                unreadable.append(job.job_id)
                continue
            for row in found:
                if account_playlists.prefer_dated(rows.get(row.ref), row):
                    rows[row.ref] = row
    return tuple(rows.values()), tuple(unreadable)


def owned_paths(
    cfg: config.Config, rows: Sequence[account_playlists.HeartRow]
) -> list[tuple[account_playlists.HeartRow, Path]]:
    """Each heart with the library file it resolves to now, hearts the library lacks left out.

    Resolved against the library as the intake worker resolves, tombstones
    included, so a heart whose file was deleted on purpose is not placed. A
    heart that resolves to several files, a lossless twin beside a marked
    copy, is placed on each, since each is the same heart. WHERE THE FILE
    SITS IS NO LONGER ASKED (U146): a file the source system filed deep is the
    author's track as much as one a landing put in a batch folder.
    """
    if not rows:
        return []
    index, suppresses, identify = match_cli.library_view(cfg)
    found: list[tuple[account_playlists.HeartRow, Path]] = []
    for row in rows:
        resolved = match.resolve_one(row.wanted, index, suppresses=suppresses, suppression_id=identify)
        if resolved.state is not match.MatchState.MATCHED:
            continue
        found.extend((row, Path(said)) for said in resolved.paths)
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

    A listing that cannot be read refuses with the listing's own reason. A
    SHORT LISTING IS CARRIED BACK, not discarded: the provider counts hearts
    it will not serve and leaves them out, so a heart absent from a short
    listing may be a heart withheld, and the caller holds it back rather than
    taking it back.
    """
    found = catalogue.resolve(cfg)
    tracks, short = label_cli.favourite_tracks_or_refuse(found, intake_cli.FAVORITES)
    # WHOLE ONLY WHEN THE PROVIDER PUBLISHED A COUNT AND THE LISTING REACHED
    # IT. The count rides on the catalogue after its listing; a catalogue that
    # knows no count published none.
    declared = getattr(found, "hearts_declared", None)
    whole = short is None and declared is not None and len(tracks) >= declared
    dates: dict[str, datetime | None] = {}
    for track in tracks:
        ref = str(getattr(track, "id", "") or "")
        when = placeholders.parse_hearted(intake_cli.hearted_on(track))
        if dates.get(ref) is None:
            dates[ref] = when
    return Listing(dates=dates, short=short, whole=whole)


@dataclass(frozen=True, slots=True)
class Gathered:
    """The hearts to place, and what finding them left aside."""

    hearts: tuple[OwnedHeart, ...]
    #: How many dates the account supplied.
    asked: int
    #: Hearts a listing that is not known whole did not carry: held back
    #: unplaced, since a withheld heart is not one taken back.
    held_back: tuple[OwnedHeart, ...] = ()
    #: The jobs whose reports could not be read, skipped and named.
    unreadable: tuple[str, ...] = ()
    short: catalogue.HeartsShortfall | None = None
    #: Hearts the author took back: the All Favorites membership exists as
    #: REMOVED in rekordbox, or the account, listed whole, no longer carries
    #: the heart. Never placed, and named.
    taken_back: tuple[OwnedHeart, ...] = ()
    #: Whether the account was listed and no count was published, so a heart
    #: it lacks could not be told from one withheld.
    uncounted: bool = False
    #: Hearts the library owns that All Favorites and a dated playlist beside
    #: it already hold: counted, never listed, nothing to write.
    already: int = 0


def gather(cfg: config.Config, db: Any, *, home: placement.Home) -> Gathered:
    """Every owned heart to place with its row and its date, and what was left aside."""
    rows, unreadable = carried(cfg)
    located = owned_paths(cfg, rows)
    if not located:
        return Gathered(hearts=(), asked=0, unreadable=unreadable)
    by_path = native.content_ids_for(db, cfg, [path for _row, path in located])
    in_source = placement.members(db, home.source_id)
    filed = placement.filed(db, home)
    # THE AUTHOR'S DECISION IN REKORDBOX: a heart whose membership in the
    # source exists as removed, and is not live again, was taken out by hand,
    # and the backfill never puts it back, run after run.
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
        heart = OwnedHeart(
            ref=row.ref,
            path=path,
            content_id=content_id,
            title=row.title,
            job_id=row.job_id,
            hearted=row.hearted,
            dated_by="job" if row.hearted is not None else "none",
        )
        if content_id in removed:
            taken.append(replace(heart, dated_by=REMOVED_IN_REKORDBOX))
            continue
        candidates.append(heart)
    if not candidates:
        return Gathered(
            hearts=(), asked=0, unreadable=unreadable, taken_back=tuple(taken), already=already
        )
    listing = listed(cfg)
    hearts: list[OwnedHeart] = []
    held: list[OwnedHeart] = []
    asked = 0
    for heart in candidates:
        # NOT ON THE ACCOUNT NOW: on a listing known whole the author took it
        # back, and it is named; on a short listing, or one with no published
        # count, the provider may have withheld it, and it is held back.
        if heart.ref not in listing.dates:
            if listing.whole:
                taken.append(replace(heart, dated_by=OFF_THE_ACCOUNT))
            else:
                held.append(heart)
            continue
        if heart.hearted is None:
            when = listing.dates.get(heart.ref)
            if when is not None:
                heart = replace(heart, hearted=when, dated_by="account")
                asked += 1
        hearts.append(heart)
    return Gathered(
        hearts=tuple(sorted(hearts, key=lambda one: (one.month, one.title))),
        asked=asked,
        held_back=tuple(held),
        unreadable=unreadable,
        short=listing.short,
        taken_back=tuple(taken),
        uncounted=not listing.whole and listing.short is None,
        already=already,
    )


def owned_in_library(
    cfg: config.Config, db: Any, rows: Sequence[account_playlists.HeartRow]
) -> tuple[OwnedHeart, ...]:
    """A pass's owned hearts with the row each one's report file is, for the landing (U146).

    THE REPORT'S OWN FILES, the first one an active row holds, the rule an
    owned member of an account playlist is found by (U128). A ROW WHOSE JOB
    FROZE NO DATE KEY IS LEFT TO THE BACKFILL, which dates it from the account;
    the landing has no listing to read and Undated is a placement nothing
    undoes. A row the job dated nowhere goes to ``Undated``. One heart per
    row, the first mention of a row winning.
    """
    known = [row for row in rows if row.known and row.paths]
    paths = [Path(said) for row in known for said in row.paths]
    if not paths:
        return ()
    by_path = native.content_ids_for(db, cfg, paths)
    found: list[OwnedHeart] = []
    seen: set[str] = set()
    for row in known:
        for said in row.paths:
            content_id = by_path.get(str(Path(said)))
            if content_id is None:
                continue
            if content_id not in seen:
                seen.add(content_id)
                found.append(
                    OwnedHeart(
                        ref=row.ref,
                        path=Path(said),
                        content_id=content_id,
                        title=row.title,
                        job_id=row.job_id,
                        hearted=row.hearted,
                        dated_by="job" if row.hearted is not None else "none",
                    )
                )
            break
    return tuple(found)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BackfillPlan:
    """The hearts to place against the home as it stands, read on one handle."""

    hearts: tuple[OwnedHeart, ...]
    placements: placement.PlacementPlan
    #: How many dates the account supplied for this plan.
    asked: int
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

    @property
    def undated(self) -> int:
        return sum(1 for one in self.hearts if one.hearted is None)

    @property
    def by_month(self) -> dict[str, int]:
        """How many hearts go to each month, in month order, Undated last."""
        counts: dict[str, int] = {}
        for one in self.placements.placements:
            counts[one.month] = counts.get(one.month, 0) + 1
        return dict(
            sorted(counts.items(), key=lambda pair: (pair[0] == placeholders.UNDATED, pair[0]))
        )

    @property
    def writes(self) -> bool:
        return self.placements.writes

    def identity(self) -> dict[str, Any]:
        return {"kind": WORKFLOW, **self.placements.identity()}


def plan(cfg: config.Config, db: Any, *, source: str) -> BackfillPlan:
    """Gather the owned hearts and plan their placement against the home."""
    home = placement.resolve_home(db, source)
    found = gather(cfg, db, home=home)
    return _planned(
        db,
        home,
        found.hearts,
        asked=found.asked,
        held_back=found.held_back,
        unreadable=found.unreadable,
        withheld=found.short.withheld if found.short is not None else 0,
        taken_back=found.taken_back,
        uncounted=found.uncounted,
        already=found.already,
    )


def plan_owned(
    cfg: config.Config, db: Any, *, source: str, rows: Sequence[account_playlists.HeartRow]
) -> BackfillPlan:
    """The landing's owned hearts that All Favorites lacks, planned as the backfill plans (U146).

    FOR A LANDING THAT BROUGHT NO FILE, whose pass still listed the account's
    hearts: the owned ones not live in All Favorites join it and their month,
    under the landing's gate and through :func:`apply`. A heart taken out of
    All Favorites by hand and still hearted is not live there, so it joins
    again, the author's rule of 2026-10-14 that dropping a favourite is
    un-hearting on the account as well. The account is not listed again: the
    pass's own job is the listing.
    """
    home = placement.resolve_home(db, source)
    in_source = placement.members(db, home.source_id)
    hearts = tuple(
        one for one in owned_in_library(cfg, db, rows) if one.content_id not in in_source
    )
    return _planned(db, home, hearts, asked=0)


def _planned(
    db: Any,
    home: placement.Home,
    hearts: Sequence[OwnedHeart],
    *,
    asked: int,
    held_back: Sequence[OwnedHeart] = (),
    unreadable: Sequence[str] = (),
    withheld: int = 0,
    taken_back: Sequence[OwnedHeart] = (),
    uncounted: bool = False,
    already: int = 0,
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
        taken_back=tuple(taken_back),
        uncounted=uncounted,
        already=already,
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
        taken_back=approved.taken_back,
        uncounted=approved.uncounted,
        already=approved.already,
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
                "month": one.month,
                "into_source": one.into_source,
                "into_month": one.into_month,
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
            "taken back": len(planned.taken_back),
            "jobs unread": len(planned.unreadable),
            "already placed": planned.already,
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
        "hearts to place": len(planned.hearts),
        "by month": [f"{month}: {count}" for month, count in planned.by_month.items()],
        "memberships to add": planned.placements.adds,
        "month playlists to create": list(planned.placements.creates),
        "undated": planned.undated,
        "dates asked of the account": planned.asked,
        "already placed": planned.already,
    }
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

    EVERY MONTH THE PLAN NAMES, not only those the write touched: a heart
    already in its month was not written and is read back all the same, by
    the row the write used or the one the plan found live, so a month row
    that went between the two acts is a disagreement and not a silence.
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
        (one.content_id, one.month)
        for one in planned.placements.placements
        if one.into_source or one.into_month
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
    "Gathered",
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
    "listed",
    "owned_in_library",
    "owned_paths",
    "payload",
    "plan",
    "plan_owned",
    "replan",
]
