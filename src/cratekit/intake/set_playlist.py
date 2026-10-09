"""A set intake leaves a permanent playlist of the set under INSPIRATION (U121).

``intake set`` identifies a recording and queues one item per track, ``intake
missing`` lists the ones to download, and ``intake land`` makes one INBOX batch
of the downloaded files. INBOX is the listening queue and the rotation clears
it after ninety days, so nothing kept the set as a whole anywhere. The author
decided on 2026-10-09 that every set intake ends with one more playlist, under
the folder the taxonomy declares as ``[inspiration]``, holding every identified
track the library owns, the ones it already had and the ones the intake
downloaded, in the order the set played them.

THE NAME IS THE SOURCE SYSTEM'S FORM, ``{M_DD_YY today} {DJ} {set name} {M-YY
of the set}``, for example ``10_09_26 Public Service NYC Live at Vonking 5-26``,
beside the two such playlists the source system left in the folder. The DJ and
the set's name come from the page the mix was fetched from, which the job
froze under ``intake_cli.PAGE``, and the set's month from the day the page
says it went up. A flag stands in for each, and a flag wins: the page title
is what the uploader typed, and the abbreviated set name the form asks for is
the author's to choose. A piece neither has is refused by name before the
gate, never defaulted, because a playlist named from a guess sits in the
library for good.

A MEMBER IS A ROW THE PRODUCT'S OWN MATCH RULE TIED TO THE SET, never a
guess. Each committed report of the job is read in item order. A row the
report called owned names the library files it resolved to, and each is
looked up in the collection the way the native landing looks a file up. A row
the report called missing or offered was downloaded, so at a landing it is
resolved against the files about to land, exactly as an account playlist
claims its files (U113), and the row made for that file joins the playlist
in the same commit; for a set already landed, it is resolved against the
library again, with the person's review answers read back. A row that
resolves to nothing, or to a file the collection holds no row for, is LEFT
and listed by position and name, so the screen says what the playlist does
not hold rather than holding something close.

THE WRITE IS THE GUARDED WRITER'S. At a landing the playlist is one more
node the native landing's single commit makes, after the batch and the
account playlists, so the set playlist and the batch land together or not at
all. The backfill verb, ``intake inspiration``, opens the same session spine
on its own for a job whose files already landed, and reads the playlist back
from SQL before it answers. Neither touches INBOX, a beat grid or any
content row.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    jobs,
    locations,
    rb_writer,
    session,
    snapshot,
    taxonomy,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import batch_name, fetch
from cratekit.intake import cli as intake_cli
from cratekit.write import routing_pass, trees

#: The job key a set is queued under, and the only key this module reads.
SET_KEY = "intake.set"

#: The refusal reasons this module owns, reserved in the cause vocabulary.
FOLDER_UNDECLARED = "inspiration-folder-undeclared"
UNNAMED = "set-playlist-unnamed"

#: The session record field naming the set playlist a commit wrote, by
#: identifier, name and the job it was made from.
RECORD_KEY = "set_playlist"
#: The session workflow the backfill verb's own write is recorded under.
WORKFLOW = "set-playlist"

#: What a member is: a row the library already held, or one the landing makes.
OWNED = "owned"
LANDED = "landed"

#: Why a row of the set is not in the playlist, in the words the screen shows.
NOT_RESOLVED = "neither owned nor landed"
NO_ROW = "owned on disk and not in the collection"
SUPPRESSED = "suppressed"
NOT_LANDED = "its file did not land"

#: The report states a landing's files were downloaded for, the account
#: playlists' own rule (U113): ``owned`` rows were never downloaded.
DOWNLOADED_STATES = frozenset({"missing", "offered"})

#: The ``--set-date`` forms, a month or a day, and the page's upload date.
_FLAG_DATE = re.compile(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$")
_PAGE_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})$")

_ORIGIN = ("intake.set_playlist",)


# ---------------------------------------------------------------------------
# The name
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SetWords:
    """The three words the name is made of: who played it, what it is, and when."""

    dj: str
    name: str
    #: The month the set is from, as the first of that month.
    month: date

    def identity(self) -> dict[str, str]:
        return {"dj": self.dj, "name": self.name, "month": self.month.strftime("%Y-%m")}


def add_word_arguments(parser) -> None:
    """The three flags that stand in for the page, shared by both verbs."""
    parser.add_argument(
        "--dj",
        default=None,
        metavar="NAME",
        help=(
            "who played the set, as the playlist names them (default: the uploader "
            "the fetched page named)"
        ),
    )
    parser.add_argument(
        "--set-name",
        dest="set_name",
        default=None,
        metavar="NAME",
        help=(
            "the set's name, abbreviated as you want it in the playlist (default: "
            "the fetched page's title, less the uploader's name in front of it)"
        ),
    )
    parser.add_argument(
        "--set-date",
        dest="set_date",
        default=None,
        metavar="YYYY-MM",
        help=(
            "the month the set is from, YYYY-MM or YYYY-MM-DD (default: the day the "
            "fetched page says the recording went up)"
        ),
    )


def today() -> date:
    """The naming date, the local calendar's. One seam with the batch name's."""
    return batch_name.today()


def _without_leading(title: str, dj: str) -> str:
    """``title`` less the uploader's name in front of it and the separator after it."""
    if not dj:
        return title
    head = title[: len(dj)]
    if head.casefold() != dj.casefold():
        return title
    rest = title[len(dj) :]
    stripped = re.sub(r"^\s*(?:[-:|–—]+\s*)?", "", rest)
    return stripped if stripped else title


def _month_of(flag: str | None, page_date: str | None) -> date | None:
    """The set's month: the flag when given, else the page's upload day, else None."""
    if flag:
        found = _FLAG_DATE.match(flag.strip())
        if found is None:
            raise refuse(
                UNNAMED,
                f"--set-date {flag!r} is not a month, so the set's playlist cannot be "
                f"named; give it as YYYY-MM or YYYY-MM-DD",
                remedy=Remedy.FIX_COMMAND_LINE,
                origin=_ORIGIN,
                detail={"set_date": flag},
            )
        return date(int(found.group(1)), int(found.group(2)), 1)
    if page_date:
        found = _PAGE_DATE.match(page_date.strip())
        if found is not None:
            return date(int(found.group(1)), int(found.group(2)), 1)
    return None


def words_for(
    job: jobs.Job,
    *,
    dj: str | None = None,
    set_name: str | None = None,
    set_date: str | None = None,
) -> SetWords:
    """The name's three words for this job, the flags first and the page after.

    REFUSED BY NAME WHEN A WORD IS MISSING, naming the flag that supplies it. A
    local recording has no page at all, and a page may name no uploader or no
    date, so the refusal lists exactly what is still wanted.
    """
    page = job.payload.get(intake_cli.PAGE) if isinstance(job.payload, Mapping) else None
    page = page if isinstance(page, Mapping) else {}
    who = (dj if dj is not None else str(page.get(fetch.PAGE_UPLOADER) or "")).strip()
    title = str(page.get(fetch.PAGE_TITLE) or "").strip()
    what = (set_name if set_name is not None else _without_leading(title, who)).strip()
    when = _month_of(set_date, str(page.get(fetch.PAGE_UPLOAD_DATE) or ""))
    missing = [
        flag
        for flag, value in (("--dj", who), ("--set-name", what), ("--set-date", when))
        if not value
    ]
    if missing:
        raise refuse(
            UNNAMED,
            f"the set's playlist cannot be named for job {job.job_id}: the recording's "
            f"page did not say {' or '.join(missing)}, so give {'it' if len(missing) == 1 else 'them'} "
            f"on the command line; nothing was written",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=tuple(f"pass {flag}" for flag in missing),
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "missing": missing, "page": dict(page)},
        )
    assert when is not None
    return SetWords(dj=who, name=what, month=when)


def playlist_name(words: SetWords, *, on: date | None = None) -> str:
    """The source system's form: ``10_09_26 Public Service NYC Live at Vonking 5-26``.

    The naming day is month, day and two digit year joined by underscores, the
    month without a leading zero and the day with one, as the folder's own
    examples have it (``5_28_26``, ``6_16_26``). The set's month is month and
    two digit year joined by a hyphen, the month without a leading zero.
    """
    made = on or today()
    return (
        f"{made.month}_{made.day:02d}_{made.year % 100:02d} {words.dj} {words.name} "
        f"{words.month.month}-{words.month.year % 100:02d}"
    )


# ---------------------------------------------------------------------------
# The job
# ---------------------------------------------------------------------------


def set_job_or_refuse(store: jobs.JobStore, job_id: str) -> jobs.Job:
    """The job, if it is a set job that ran every track to the end."""
    job = jobs.get(store, job_id)
    if job.handler_key != SET_KEY:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not a set "
            f"intake, so there is no set to make a playlist of",
            steps=("name the job an intake set run printed",),
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    if job.state is not jobs.JobState.SUCCEEDED:
        raise refuse(
            "intake-list-unusable",
            f"job {job.job_id} is {job.state}, not succeeded, so some of its tracks "
            f"may not be resolved and a playlist of the rest would read as the set",
            steps=(
                f"finish it with: crate {' '.join(intake_cli.set_argv(job))}"
                if job.is_open()
                else "identify the set again, let it finish, then name that job",
            ),
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "state": str(job.state)},
            inner=job.cause,
        )
    return job


def reports_of(cfg: config.Config, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """The job's committed reports in item order, through the one reader ``intake missing`` uses."""
    from cratekit.intake import missing_cli

    with jobs.open_store() as store:
        return missing_cli.job_reports(store, job)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Member:
    """One track of the set the playlist will hold, in set order."""

    position: int
    artist: str
    title: str
    #: :data:`OWNED` for a row the collection holds now, :data:`LANDED` for one
    #: the landing makes in the same commit.
    state: str
    #: The collection row, known now for an owned track.
    content_id: str = ""
    #: The landing's target for a track whose row is made at the apply.
    target: str = ""

    def identity(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "artist": self.artist,
            "title": self.title,
            "state": self.state,
            "content_id": self.content_id,
            "target": self.target,
        }


@dataclass(frozen=True, slots=True)
class Left:
    """One track of the set the playlist will not hold, and why."""

    position: int
    artist: str
    title: str
    state: str
    why: str

    def identity(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "artist": self.artist,
            "title": self.title,
            "state": self.state,
            "why": self.why,
        }


@dataclass(frozen=True, slots=True)
class SetPlaylistPlan:
    """The playlist a set gets: where it goes, what it is called, what it holds."""

    job_id: str
    name: str
    #: The declared folder's stable id, what the session record keys the
    #: commit under (R19), and its display, what rekordbox shows.
    tree_id: str
    folder_display: str
    #: The declared folder's row at the playlist root, or empty when the
    #: write creates it there.
    folder_id: str
    words: SetWords
    members: tuple[Member, ...]
    left: tuple[Left, ...]
    #: The day the name was made on, so a write after midnight keeps it.
    made_on: date | None = None
    digest: str = ""


@dataclass(frozen=True, slots=True)
class Written:
    """What a commit wrote for the set, read back from SQL after it."""

    name: str
    playlist_id: str
    folder_id: str
    folder_created: bool
    #: The rows the playlist was asked to hold.
    members: int
    #: The memberships this commit added; fewer when the playlist held some.
    added: int
    #: Every member the commit could not add, with the planned left rows after.
    left: tuple[Left, ...]
    #: The content ids the playlist was asked to hold, in set order.
    ids: tuple[str, ...] = ()
    #: The content ids read back under the playlist after the commit, in order.
    read_back: tuple[str, ...] = ()


def identity(plan: SetPlaylistPlan) -> dict[str, Any]:
    """What the digest covers: the folder, the name, every member and every left row."""
    return {
        "kind": "set-playlist",
        "job": plan.job_id,
        "name": plan.name,
        "tree": plan.tree_id,
        "folder": plan.folder_id,
        "folder_display": plan.folder_display,
        "words": plan.words.identity(),
        "made_on": plan.made_on.isoformat() if plan.made_on else "",
        "members": [one.identity() for one in plan.members],
        "left": [one.identity() for one in plan.left],
    }


def folder_for(db: Any, declared: taxonomy.Taxonomy) -> tuple[str, taxonomy.Node]:
    """The declared folder's row id at the playlist root, or empty to create it, and the node.

    REFUSED BY NAME WHEN THE TAXONOMY DECLARES NONE, the catalog's rule: the
    folder is declared in the template and this module will not invent one. A
    root that holds the folder twice is refused too, since whichever the
    query yielded first is not an answer. A removed folder is not there.
    """
    node = declared.inspiration
    if node is None:
        raise refuse(
            FOLDER_UNDECLARED,
            "this library's taxonomy declares no [inspiration] folder, so there is "
            "nowhere to keep the set's playlist for good; the folder is declared at "
            "the playlist root and this verb will not invent one",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=(
                "add an [inspiration] section with an id and a display to the "
                "library's active taxonomy, as the shipped template carries",
            ),
            origin=_ORIGIN,
        )
    live = [row for row in rb_writer.top_level_folders(db, node.display) if not rb_writer.node_removed(row)]
    if len(live) > 1:
        raise refuse(
            FOLDER_UNDECLARED,
            f"the playlist root holds {len(live)} folders named {node.display!r}, so "
            f"the set's playlist has no one folder to go in; nothing was written",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=("merge or rename the folders in rekordbox so one carries the name",),
            origin=_ORIGIN,
            detail={"display": node.display, "count": len(live)},
        )
    return (str(live[0].ID) if live else ""), node


def _holding(found: trees.RowMatch) -> str | None:
    """The active row a match names, the first of several when two claim it."""
    if found.content_id:
        return str(found.content_id)
    if found.content_ids:
        return str(found.content_ids[0])
    return None


class _Collection:
    """The collection's active rows, indexed once on this handle, asked by path."""

    def __init__(self, cfg: config.Config, db: Any) -> None:
        self._cfg = cfg
        self._prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
        self._index = trees.index_active_rows(
            routing_pass.content_rows(db), root=cfg.library.root, prefix_map=self._prefix_map
        )

    def row_for(self, paths: Sequence[str]) -> str | None:
        """The first row any of ``paths`` resolves to, or None."""
        if not paths:
            return None
        for found in trees.match_indexed_rows(
            paths, self._index, root=self._cfg.library.root, prefix_map=self._prefix_map
        ):
            held = _holding(found)
            if held is not None:
                return held
        return None


def _never_suppressed(_recording: str, _address: object) -> bool:
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


def _report_words(report: Mapping[str, Any]) -> tuple[str, str]:
    track = report.get("track") if isinstance(report.get("track"), Mapping) else {}
    return str(track.get("artist") or ""), str(track.get("title") or "")


def _wanted(report: Mapping[str, Any]) -> match.Wanted:
    track = report.get("track") if isinstance(report.get("track"), Mapping) else {}
    return intake_cli.thawed(track)


def _members(
    reports: Sequence[Mapping[str, Any]],
    *,
    collection: _Collection,
    downloaded: Callable[[match.Wanted], tuple[tuple[str, ...], str]],
    owned_again: Callable[[match.Wanted], tuple[str, ...]] | None,
) -> tuple[tuple[Member, ...], tuple[Left, ...]]:
    """Each report, in order, as a member or a left row.

    ``downloaded`` answers a missing or offered row with the paths the rule tied
    it to and the state those paths give the member, :data:`LANDED` for a
    landing's staged files and :data:`OWNED` for library files. ``owned_again``
    re-resolves an owned row whose report paths hold no row any more, for the
    backfill, and is None at a landing where the report is fresh.
    """
    members: list[Member] = []
    left: list[Left] = []
    for position, report in enumerate(reports, start=1):
        artist, title = _report_words(report)
        state = str(report.get("state") or "")
        if state == "owned":
            paths = tuple(str(path) for path in (report.get("paths") or ()))
            held = collection.row_for(paths)
            if held is None and owned_again is not None:
                held = collection.row_for(owned_again(_wanted(report)))
            if held is None:
                left.append(Left(position, artist, title, state, NO_ROW))
            else:
                members.append(Member(position, artist, title, OWNED, content_id=held))
            continue
        if state == "suppressed":
            left.append(Left(position, artist, title, state, SUPPRESSED))
            continue
        if state not in DOWNLOADED_STATES:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        paths, how = downloaded(_wanted(report))
        if not paths:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        if how == LANDED:
            members.append(Member(position, artist, title, LANDED, target=paths[0]))
            continue
        held = collection.row_for(paths)
        if held is None:
            left.append(Left(position, artist, title, state, NO_ROW))
        else:
            members.append(Member(position, artist, title, OWNED, content_id=held))
    return tuple(members), tuple(left)


def _digested(plan: SetPlaylistPlan) -> SetPlaylistPlan:
    return replace(plan, digest=digest_of(identity(plan)))


def plan_for_landing(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    job: jobs.Job,
    words: SetWords,
    reports: Sequence[Mapping[str, Any]],
    *,
    files: Sequence[tuple[Path, Path]],
    on: date | None = None,
) -> SetPlaylistPlan:
    """The playlist a landing writes beside its batch, over the files about to land.

    ``files`` pairs each staged file with its target, the native plan's own
    pairs. A downloaded row is tied to a staged file by the match rule over
    exactly those files, as an account playlist is (U113), and the member
    carries the TARGET, since the row is made at the apply and keyed by it.
    """
    made = on or today()
    folder_id, node = folder_for(db, declared)
    staged = [source for source, _target in files]
    targets = {source.resolve(): str(target) for source, target in files}
    index = match.index_paths(staged, template=match_cli.library_template(cfg))

    def downloaded(wanted: match.Wanted) -> tuple[tuple[str, ...], str]:
        found = match.resolve_one(
            wanted, index, suppresses=_never_suppressed, suppression_id=_no_suppression_id
        )
        if found.state is not match.MatchState.MATCHED:
            return (), LANDED
        tied = [targets[Path(path).resolve()] for path in found.paths if Path(path).resolve() in targets]
        return tuple(tied), LANDED

    members, left = _members(
        reports, collection=_Collection(cfg, db), downloaded=downloaded, owned_again=None
    )
    return _digested(
        SetPlaylistPlan(
            job_id=job.job_id,
            name=playlist_name(words, on=made),
            tree_id=node.id,
            folder_display=node.display,
            folder_id=folder_id,
            words=words,
            members=members,
            left=left,
            made_on=made,
        )
    )


def plan_for_backfill(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    job: jobs.Job,
    words: SetWords,
    reports: Sequence[Mapping[str, Any]],
    *,
    on: date | None = None,
) -> SetPlaylistPlan:
    """The playlist for a set whose files already landed, every row resolved against the library now.

    THE WORKER'S OWN RESOLVE, :func:`intake_cli.resolve_track`, which reads
    the library the job froze and reads back every answer a person gave about
    a row, so a track accepted at review is the file they accepted. A row the
    report called owned keeps its report paths first, and is resolved again
    only when those paths hold no row any more.
    """
    made = on or today()
    folder_id, node = folder_for(db, declared)
    intake_cli.reset_cache()

    def resolved(wanted: match.Wanted) -> tuple[str, ...]:
        found = intake_cli.resolve_track(wanted, job, cfg)
        return tuple(found.paths) if found.state is match.MatchState.MATCHED else ()

    members, left = _members(
        reports,
        collection=_Collection(cfg, db),
        downloaded=lambda wanted: (resolved(wanted), OWNED),
        owned_again=resolved,
    )
    return _digested(
        SetPlaylistPlan(
            job_id=job.job_id,
            name=playlist_name(words, on=made),
            tree_id=node.id,
            folder_display=node.display,
            folder_id=folder_id,
            words=words,
            members=members,
            left=left,
            made_on=made,
        )
    )


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------


def payload(plan: SetPlaylistPlan) -> dict[str, Any]:
    """The plan as a gate shows it: one item per member, then one per left row."""
    items: list[dict[str, Any]] = [
        {"action": "add", **one.identity()} for one in plan.members
    ]
    items.extend({"action": "leave", **one.identity()} for one in plan.left)
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {"count": len(items), "members": len(plan.members), "left": len(plan.left)},
        "chunk": None,
    }


def facts(plan: SetPlaylistPlan) -> dict[str, Any]:
    """The facts beside the items on a gate screen, one line per fact."""
    where = (
        f"{plan.folder_display} (row {plan.folder_id})"
        if plan.folder_id
        else f"{plan.folder_display}, created at the playlist root"
    )
    return {
        "set playlist": plan.name,
        "under": where,
        "set job": plan.job_id,
        "set tracks": len(plan.members),
        "set left out": len(plan.left),
    }


def left_warning(left: Sequence[Left]) -> list[dict[str, str]]:
    """The one warning naming every track the playlist does not hold."""
    if not left:
        return []
    named = "; ".join(
        f"{one.position}. {one.artist} - {one.title} ({one.why})" for one in left
    )
    return [
        {
            "code": LEFT_OUT,
            "message": (
                f"{len(left)} track(s) of the set are not in its playlist, because "
                f"nothing the product owns or landed was tied to them: {named}"
            ),
        }
    ]


LEFT_OUT = "set-playlist-left-out"
WRITTEN = "set-playlist-written"
NOTHING = "set-playlist-nothing-to-write"


def nothing_note(plan: SetPlaylistPlan) -> list[dict[str, str]]:
    """The one note a write carries when the set has no member to hold."""
    return [
        {
            "code": NOTHING,
            "message": (
                f"no track of the set was owned or landed, so the playlist "
                f"{plan.name!r} was not written; {len(plan.left)} track(s) are listed "
                f"as left out"
            ),
        }
    ]


def written_note(written: Written) -> list[dict[str, str]]:
    """The one note a write carries naming the playlist it made and what it holds."""
    made = ", created at the playlist root" if written.folder_created else ""
    return [
        {
            "code": WRITTEN,
            "message": (
                f"the set's playlist {written.name!r} holds {written.members} track(s) "
                f"under the folder (row {written.folder_id}{made}), {written.added} "
                f"added by this write and read back from the database in set order"
            ),
        }
    ]


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def _folder_row(db: Any, plan: SetPlaylistPlan) -> tuple[Any, bool]:
    """The folder the playlist goes under, found by the plan's id or created at the root."""
    if plan.folder_id:
        row = db.get_playlist(ID=plan.folder_id)
        if row is None or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the {plan.folder_display!r} folder (row {plan.folder_id}) is not live "
                f"any more, so the set's playlist has nowhere to go; nothing was written",
                origin=_ORIGIN,
                detail={"folder": plan.folder_id, "display": plan.folder_display},
            )
        return row, False
    return db.create_playlist_folder(plan.folder_display), True


def write_members(
    db: Any, plan: SetPlaylistPlan, *, by_target: Mapping[str, str] | None = None
) -> Written | None:
    """Make the playlist under its folder and add every member, pending on ``db``.

    INSIDE A CALLER'S SESSION, which commits or rolls back. ``by_target`` maps a
    landing's targets to the rows it just made; a member whose target made no
    row is left, listed, and the rest are added. The playlist is found by its
    name under the folder when it is there already, so a backfill run twice on
    one day adds nothing the second time, and ``add_memberships`` adds only
    what is absent.

    NOTHING IS WRITTEN FOR A SET OF NO MEMBERS, and the answer is None: a
    playlist holding nothing under a folder kept for good is not the set, and
    the caller says so with the left rows listed.
    """
    rows = dict(by_target or {})
    ids: list[str] = []
    left: list[Left] = []
    for one in plan.members:
        held = one.content_id or rows.get(one.target, "")
        if held:
            ids.append(held)
        else:
            left.append(Left(one.position, one.artist, one.title, one.state, NOT_LANDED))
    if not ids:
        return None
    folder, created = _folder_row(db, plan)
    playlist = rb_writer.ensure_playlist(db, plan.name, folder)
    added = rb_writer.add_memberships(db, playlist, ids)
    return Written(
        name=plan.name,
        playlist_id=str(playlist.ID),
        folder_id=str(folder.ID),
        folder_created=created,
        members=len(ids),
        added=len(added),
        left=(*left, *plan.left),
        ids=tuple(ids),
    )


def record_on(record: session.SessionRecord, written: Written, plan: SetPlaylistPlan) -> None:
    """Name the set playlist on the session record, beside whatever else it names."""
    record.detail[RECORD_KEY] = {
        "id": written.playlist_id,
        "name": written.name,
        "job": plan.job_id,
        "folder": written.folder_id,
    }


def read_back(db: Any, playlist_id: str) -> tuple[str, ...]:
    """The live content ids under the playlist, from SQL, in track order."""
    from sqlalchemy import text

    rows = db.session.execute(
        text(
            f"SELECT ContentID FROM {rb_writer.MEMBERSHIP_TABLE} WHERE PlaylistID = :id "
            f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY TrackNo"
        ),
        {"id": playlist_id},
    ).fetchall()
    return tuple(str(row[0]) for row in rows)


def assert_read_back(written: Written) -> None:
    """Refuse an answer the database does not hold: every member read back, in set order.

    A playlist found by its name may hold rows from an earlier run, so what is
    compared is the read back FILTERED to the ids this commit asked for, which
    must come back as all of them in the order the set played them. A member
    named twice in the set is one membership and counted once.
    """
    wanted = list(dict.fromkeys(written.ids))
    if wanted and [one for one in written.read_back if one in set(wanted)] != wanted:
        raise refuse(
            "session-committed-unverified",
            f"the set playlist {written.name!r} ({written.playlist_id}) read back from "
            f"the database holds {len(written.read_back)} track(s) and not the "
            f"{len(wanted)} the plan named, in that order; the commit landed and this "
            f"answer cannot be vouched for",
            origin=_ORIGIN,
            detail={
                "playlist_id": written.playlist_id,
                "planned": wanted,
                "read": list(written.read_back),
            },
        )


def apply_alone(
    cfg: config.Config,
    db: Any,
    plan: SetPlaylistPlan,
    *,
    declared: taxonomy.Taxonomy,
    job: jobs.Job,
    words: SetWords,
    reports: Sequence[Mapping[str, Any]],
    analysis_roots: Iterable[Path | str],
) -> Written | None:
    """Write the playlist in a session of its own, for a set already landed.

    None, with nothing opened, for a plan of no members: an empty playlist is
    not written and no session is spent learning that.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database tree writer
    calls it: the gates with a record kept, a capture verified before anything
    is written, the analysis watch over the roots named, the commit witness,
    and the guarded commit with nothing admitted beyond the whitelist, since a
    playlist row and its memberships are what every membership writer adds.
    The folder is looked up again on this handle, so a folder that went
    between the plan and the write refuses with nothing written.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    if not plan.members:
        return None
    # THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST, the rotation's rule: the
    # plan the person approved was read on a handle that has since closed,
    # and the folder, the collection or the library may have moved since.
    again = plan_for_backfill(
        cfg, db, declared, job, words, reports, on=plan.made_on
    )
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the set's playlist is not as the approved plan read it, so nothing was "
            "written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    written: Written | None = None
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
        try:
            written = write_members(db, plan)
            assert written is not None, "a plan with members writes"
            rb_writer.commit_guarded(db)
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed and written is not None:
                _record_set_commit(record, written, plan, cfg)
            raise
        _record_set_commit(record, written, plan, cfg)
        convergence.record_fingerprint(cfg, db)
        written = replace(written, read_back=read_back(db, written.playlist_id))
    return written


def _record_set_commit(
    record: session.SessionRecord, written: Written, plan: SetPlaylistPlan, cfg: config.Config
) -> None:
    """Record the commit on the session, under the declared folder's own id (R19).

    THE LANDING CALLS THIS BESIDE ITS OWN RECORD, through :func:`record_commit`,
    so the intake tree's entry counts the batch's memberships and this one
    counts the set's, and a restore weighing the session sees both by name.
    Named the way the write session guard reads a commit helper.
    """
    record_on(record, written, plan)
    changes = (session.TreeChange(tree=plan.tree_id, created=written.added),)
    session.record_commit(record, plan.tree_id, session.ChangeSummary(changes), cfg)


def record_commit(
    record: session.SessionRecord, written: Written, plan: SetPlaylistPlan, cfg: config.Config
) -> None:
    """The public face of :func:`_record_set_commit`, for the landing's own helper."""
    _record_set_commit(record, written, plan, cfg)


__all__ = [
    "DOWNLOADED_STATES",
    "FOLDER_UNDECLARED",
    "LANDED",
    "LEFT_OUT",
    "NOT_LANDED",
    "NOTHING",
    "NOT_RESOLVED",
    "NO_ROW",
    "OWNED",
    "RECORD_KEY",
    "SET_KEY",
    "SUPPRESSED",
    "UNNAMED",
    "WORKFLOW",
    "WRITTEN",
    "Left",
    "Member",
    "SetPlaylistPlan",
    "SetWords",
    "Written",
    "add_word_arguments",
    "apply_alone",
    "assert_read_back",
    "facts",
    "folder_for",
    "identity",
    "left_warning",
    "nothing_note",
    "payload",
    "plan_for_backfill",
    "plan_for_landing",
    "playlist_name",
    "read_back",
    "record_commit",
    "record_on",
    "reports_of",
    "set_job_or_refuse",
    "today",
    "words_for",
    "write_members",
    "written_note",
]
