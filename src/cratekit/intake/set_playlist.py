"""A set intake leaves a permanent playlist of the set under INSPIRATION (U121).

``intake set`` identifies a recording and queues one item per track, ``intake
missing`` lists the ones to download, and ``intake land`` makes one INBOX batch
of the downloaded files. INBOX is the listening queue and the rotation clears
it after ninety days, so nothing kept the set as a whole anywhere. The author
decided on 2026-10-09 that every set intake ends with one more playlist, under
the folder the taxonomy declares as ``[inspiration]``, holding every identified
track the library owns, the ones it already had and the ones the intake
downloaded, in the order the set played them.

THE NAME IS THE SOURCE SYSTEM'S FORM, ``{M_DD_YY posted} {DJ} {set name} {M-YY
of the set}``, for example ``3_25_26 Public Service NYC Live at Signal 2-26``,
beside the two such playlists the source system left in the folder. The first
word is the day the set went up on its service, read from the page's
``upload_date`` the job froze, with ``--posted YYYY-MM-DD`` to override and the
landing day as the recorded fallback when the page names none (U136). The DJ
and the set's name come from the page under ``intake_cli.PAGE``, and the set's
month from ``--set-date`` or the same upload day. A flag stands in for each,
and a flag wins: the page title is what the uploader typed, and the abbreviated
set name the form asks for is the author's to choose. A piece neither has is
refused by name before the gate, never defaulted, because a playlist named
from a guess sits in the library for good. The form itself lives in
:mod:`cratekit.intake.batch_name` with the day as an argument, so a backfill
names the set and not the day it runs (R-949).

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
    review,
    session,
    snapshot,
    taxonomy,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import batch_name, fetch, ingest
from cratekit.intake import cli as intake_cli
from cratekit.write import routing_pass, trees

#: The job key a set is queued under, and the only key this module reads.
SET_KEY = "intake.set"

#: The refusal reasons this module owns, reserved in the cause vocabulary.
FOLDER_UNDECLARED = "inspiration-folder-undeclared"
UNNAMED = "set-playlist-unnamed"
#: The page named no upload date, so the naming day fell back to the landing day (U136).
POSTED_FALLBACK = "set-playlist-posted-fallback"
#: ``--posted`` named a day the job's frozen name does not open with, and the
#: frozen name won, so the flag named nothing (U136).
POSTED_IGNORED = "set-playlist-posted-ignored"

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
AMBIGUOUS_ROWS = "two collection rows claim its file"
SUPPRESSED = "suppressed"
NOT_LANDED = "its file did not land"

#: The report states a landing's files were downloaded for, the account
#: playlists' own rule (U113): ``owned`` rows were never downloaded.
DOWNLOADED_STATES = frozenset({"missing", "offered"})

#: The ``--set-date`` forms, a month or a day, and the page's upload date.
_FLAG_DATE = re.compile(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$")
_PAGE_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})$")
_POSTED_FLAG = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

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
    parser.add_argument(
        "--posted",
        default=None,
        metavar="YYYY-MM-DD",
        help=(
            "the day the set went up on its service, as the playlist opens with "
            "(default: the page's upload_date; the landing day when the page names none)"
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
    stripped = re.sub(r"^\s*(?:[-:|\u2013\u2014]+\s*)?", "", rest)
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
        try:
            # The day, when given, is checked as a day and then dropped.
            given = date(int(found.group(1)), int(found.group(2)), int(found.group(3) or 1))
            return given.replace(day=1)
        except ValueError as exc:
            raise refuse(
                UNNAMED,
                f"--set-date {flag!r} is not a month ({exc}), so the set's playlist "
                f"cannot be named; give it as YYYY-MM or YYYY-MM-DD",
                remedy=Remedy.FIX_COMMAND_LINE,
                origin=_ORIGIN,
                detail={"set_date": flag},
            ) from exc
    if page_date:
        found = _PAGE_DATE.match(page_date.strip())
        if found is not None:
            try:
                return date(int(found.group(1)), int(found.group(2)), 1)
            except ValueError:
                # A page date that is not a date names no month, and the flag
                # is asked for, exactly as a page with no date.
                return None
    return None


def words_from_page(
    page: Mapping[str, Any] | None,
    *,
    dj: str | None = None,
    set_name: str | None = None,
    set_date: str | None = None,
    job_id: str = "",
) -> SetWords:
    """The name's three words, the flags first and the page after.

    REFUSED BY NAME WHEN A WORD IS MISSING, naming the flag that supplies it. A
    local recording has no page at all, and a page may name no uploader or no
    date, so the refusal lists exactly what is still wanted. ``job_id`` rides
    only in the refusal's detail, so a call before the job is queued can name
    the set the same way a call after it does (U129).
    """
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
        where = f" for job {job_id}" if job_id else ""
        raise refuse(
            UNNAMED,
            f"the set's playlist cannot be named{where}: the recording's "
            f"page did not say {' or '.join(missing)}, so give {'it' if len(missing) == 1 else 'them'} "
            f"on the command line; nothing was written",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=tuple(f"pass {flag}" for flag in missing),
            origin=_ORIGIN,
            detail={"job_id": job_id, "missing": missing, "page": dict(page)},
        )
    assert when is not None
    return SetWords(dj=who, name=what, month=when)


def words_for(
    job: jobs.Job,
    *,
    dj: str | None = None,
    set_name: str | None = None,
    set_date: str | None = None,
) -> SetWords:
    """The name's three words for this job, the flags first and the page after."""
    page = job.payload.get(intake_cli.PAGE) if isinstance(job.payload, Mapping) else None
    return words_from_page(
        page if isinstance(page, Mapping) else {},
        dj=dj,
        set_name=set_name,
        set_date=set_date,
        job_id=job.job_id,
    )


def frozen_name(job: jobs.Job) -> str:
    """The playlist name ``intake set`` froze on the job for the account and INSPIRATION (U129).

    Empty when the job was queued before that freeze, or when the set could not
    be named at queue time. Callers fall back to :func:`playlist_name` then.
    SINCE U140 IT MAY NOT BE THE QUEUE TIME NAME: ``export set --rename``
    refreezes the name a person gave the INSPIRATION playlist, which need not
    open with a day.
    """
    payload = job.payload if isinstance(job.payload, Mapping) else {}
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()


def _page_upload_date(page: Mapping[str, Any] | None) -> str:
    """The page's upload_date string, or empty when the page carries none."""
    if not isinstance(page, Mapping):
        return ""
    return str(page.get(fetch.PAGE_UPLOAD_DATE) or "").strip()


def page_of(job: jobs.Job) -> Mapping[str, Any]:
    """The page the set job froze, or an empty mapping."""
    payload = job.payload if isinstance(job.payload, Mapping) else {}
    page = payload.get(intake_cli.PAGE)
    return page if isinstance(page, Mapping) else {}


def naming_day(
    *,
    posted: str | None = None,
    page_upload_date: str | None = None,
    landing: date | None = None,
) -> tuple[date, dict[str, str] | None]:
    """The day a set's playlists open with (U136).

    ``--posted YYYY-MM-DD`` wins over the page's ``upload_date`` (``YYYYMMDD``).
    When neither names a day, the landing day is used and a warning is returned
    for the screen. The INBOX batch name is not this day; it keeps the landing
    date through :func:`batch_name.readable`.
    """
    if posted:
        found = _POSTED_FLAG.match(posted.strip())
        if found is None:
            raise refuse(
                UNNAMED,
                f"--posted {posted!r} is not a day, so the set's playlist cannot be "
                f"named; give it as YYYY-MM-DD",
                remedy=Remedy.FIX_COMMAND_LINE,
                origin=_ORIGIN,
                detail={"posted": posted},
            )
        try:
            return date(int(found.group(1)), int(found.group(2)), int(found.group(3))), None
        except ValueError as exc:
            raise refuse(
                UNNAMED,
                f"--posted {posted!r} is not a day ({exc}), so the set's playlist "
                f"cannot be named; give it as YYYY-MM-DD",
                remedy=Remedy.FIX_COMMAND_LINE,
                origin=_ORIGIN,
                detail={"posted": posted},
            ) from exc
    raw = (page_upload_date or "").strip()
    if raw:
        found = _PAGE_DATE.match(raw)
        if found is not None:
            try:
                return date(int(found.group(1)), int(found.group(2)), int(found.group(3))), None
            except ValueError:
                pass
    day = landing or today()
    return day, {
        "code": POSTED_FALLBACK,
        "message": (
            f"the set's page named no upload date, so its playlists open with the "
            f"landing day {batch_name.set_day_word(day)}; pass --posted YYYY-MM-DD "
            f"to name another day"
        ),
    }


def ignored_posted(job: jobs.Job, posted: str | None) -> dict[str, str] | None:
    """The warning when ``--posted`` names a day the job's frozen name does not open with (U136).

    A job queued since U129 carries the name ``intake set`` froze, and that
    name wins over ``--posted`` so every landing and backfill of the set finds
    the one playlist. The flag is then not used, and saying so names both days.
    None without the flag, without a frozen name, or when the two agree.
    """
    frozen = frozen_name(job)
    if not posted or not frozen:
        return None
    day, _fallback = naming_day(posted=posted)
    word = batch_name.set_day_word(day)
    opens = frozen.split()[0]
    if word == opens:
        return None
    return {
        "code": POSTED_IGNORED,
        "message": (
            f"--posted {posted.strip()} names the day {word}, but this set's playlists "
            f"keep the name {frozen!r} frozen on its job when it was queued, which "
            f"opens with {opens}; the frozen name wins and --posted was not used"
        ),
    }


def naming_day_for(
    job: jobs.Job,
    *,
    posted: str | None = None,
    landing: date | None = None,
) -> tuple[date, dict[str, str] | None]:
    """:func:`naming_day` over the page this job froze."""
    return naming_day(
        posted=posted,
        page_upload_date=_page_upload_date(page_of(job)),
        landing=landing,
    )


def playlist_name(words: SetWords, *, on: date | None = None) -> str:
    """The source system's form: ``3_25_26 Public Service NYC Live at Signal 2-26``.

    The naming day is an argument on :func:`batch_name.set_playlist_form` (U136).
    Pass the posted day from :func:`naming_day`; when ``on`` is omitted the
    landing day is used, which is the recorded fallback for callers that have
    not yet resolved a page date.
    """
    made = on or today()
    return batch_name.set_playlist_form(
        made, dj=words.dj, name=words.name, month=words.month
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


def reports_of(store: jobs.JobStore, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """The job's committed reports in item order, through the one reader ``intake missing`` uses."""
    from cratekit.intake import missing_cli

    return missing_cli.job_reports(store, job)


def assert_native(medium: ingest.IntakeMedium, *, landing: bool) -> None:
    """Refuse a set playlist on a library whose intake tree is not database native.

    ONE REFUSAL FOR BOTH VERBS. The playlist is a database node and the
    bridge's writers emit an export, so the fact is the same whichever verb
    meets it, and so are the reason and the remedy. The landing is told it
    can land without ``--set`` and backfill after the cutover.
    """
    if medium.native:
        return
    declared = medium.declared
    tree_id = declared.intake.id if declared is not None else ""
    if declared is None:
        message = (
            "the library root is not reachable, so its taxonomy and its intake tree "
            "could not be read and the set's playlist cannot be written; nothing was "
            "written"
        )
        steps = ["mount the library volume and run it again"]
    else:
        message = (
            f"the intake tree {tree_id!r} is still on the xml bridge, so the set's "
            f"playlist, a database node, is not this product's to write here; cut the "
            f"intake tree over first, nothing was written"
        )
        steps = [
            f"run crate tree cutover {tree_id} --export with a Fresh Export to move the "
            f"intake tree to the database",
        ]
    if landing:
        steps.insert(
            0, "land without --set, and run crate intake inspiration --job after the cutover"
        )
        message = message.replace("nothing was written", "nothing was moved")
    raise refuse(
        "tree-unconverged",
        message,
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=tuple(steps),
        origin=_ORIGIN,
        detail={"tree_id": tree_id, "landing": landing},
    )


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
    #: The playlist an earlier write for this job made, read off its session
    #: record and live under the folder, which this write adds to; empty when
    #: the write finds or makes the playlist by name.
    playlist_id: str = ""
    #: Warning when the naming day fell back to the landing day (U136), or None.
    posted_fallback: dict[str, str] | None = None
    #: The ``--posted`` string the plan was made with, so ``apply_alone`` can
    #: re-plan without flipping the fallback bit when the day equals landing.
    posted: str | None = None
    #: Warning when ``--posted`` named another day than the frozen name opens
    #: with, which won (U136), or None. NOT in :func:`identity`: it changes
    #: nothing written, and a re-plan without the flag must keep the digest.
    posted_ignored: dict[str, str] | None = None
    digest: str = ""


@dataclass(frozen=True, slots=True)
class Written:
    """What a commit wrote for the set, read back from SQL after it."""

    name: str
    #: Empty when nothing was written: no member had a row to add.
    playlist_id: str
    folder_id: str
    folder_created: bool
    #: Whether this commit made the playlist row, or found one.
    playlist_created: bool
    #: The distinct rows the playlist was asked to hold.
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
        "playlist": plan.playlist_id,
        "folder_display": plan.folder_display,
        "words": plan.words.identity(),
        "made_on": plan.made_on.isoformat() if plan.made_on else "",
        "posted_fallback": bool(plan.posted_fallback),
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


class _Collection:
    """The collection's active rows, indexed once on this handle, asked by path."""

    def __init__(self, cfg: config.Config, db: Any) -> None:
        self._cfg = cfg
        self._prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
        self._index = trees.index_active_rows(
            routing_pass.content_rows(db), root=cfg.library.root, prefix_map=self._prefix_map
        )

    def row_for(self, paths: Sequence[str]) -> tuple[str | None, str]:
        """The one row the first of ``paths`` resolves to, or None and why not.

        A PATH TWO ACTIVE ROWS CLAIM IS NOT A ROW, the native landing's own
        rule: the playlist would hold whichever the index yielded first, and
        one of a duplicate pair is the row that does not play. Such a track is
        left and the screen says two rows claim its file.
        """
        if not paths:
            return None, NO_ROW
        ambiguous = False
        for found in trees.match_indexed_rows(
            paths, self._index, root=self._cfg.library.root, prefix_map=self._prefix_map
        ):
            if found.outcome is trees.MatchOutcome.AMBIGUOUS:
                ambiguous = True
                continue
            if found.content_id:
                return str(found.content_id), ""
        return None, (AMBIGUOUS_ROWS if ambiguous else NO_ROW)


class _LibraryView:
    """The library as the match engine sees it, a person's answers read back, nothing written.

    THE WORKER'S RESOLVE WITHOUT THE WORKER'S WRITES. ``intake set`` resolves a
    row through ``adjudicate``, which offers a review item for a question and
    retires one a rule has settled, and a PLAN may do neither: a plan the
    person aborts has written nothing, and the gate is asked over exactly
    what the screen showed. So the row is resolved against the same index and
    tombstone view the worker reads, and a question is answered only by the
    item the worker already filed, found by the question's own identity and
    read as the worker reads it, a person's verdict and nothing else.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._index, self._suppresses, self._suppression_id = match_cli.library_view(cfg)

    def resolve(self, wanted: match.Wanted) -> match.TrackMatch:
        found = match.resolve_one(
            wanted, self._index, suppresses=self._suppresses, suppression_id=self._suppression_id
        )
        if found.state is not match.MatchState.NEEDS_REVIEW:
            return found
        item_id = review.item_id_for(match_cli.QUEUE, match.QUESTION_KIND, found.question_identity)
        with review.open_store(self._cfg) as items:
            held = review.find(items, item_id)
        if held is None or held.verdict not in review.PERSON_VERDICTS:
            return found
        return match.apply_verdict(
            found,
            accepted=held.verdict is review.Verdict.ACCEPTED,
            option=held.option,
            offered=tuple(one.option_id for one in held.options),
            item_id=held.item_id,
            suppresses=self._suppresses,
            suppression_id=self._suppression_id,
        )

    def paths(self, wanted: match.Wanted) -> tuple[str, ...]:
        """The library files the row is tied to, or nothing when it is a question or missing."""
        found = self.resolve(wanted)
        return tuple(found.paths) if found.state is match.MatchState.MATCHED else ()


def _landed(cfg: config.Config, job_id: str) -> tuple[Mapping[str, Any], ...]:
    """The set playlist detail every landing of this job recorded, the newest first.

    A closed record whose source committed, so a landing that wrote nothing is
    not read as having named a playlist.
    """
    records, _unreadable = session.scan_log(cfg)
    found = [
        record
        for record in records
        if record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
        record.detail[RECORD_KEY]
        for record in sorted(found, key=lambda one: one.session_id, reverse=True)
    )


def recorded_names(cfg: config.Config, job_id: str) -> tuple[str, ...]:
    """The names this job's landings wrote its INSPIRATION playlist under, the newest first.

    R-1017. What a landing named the playlist is what a backfill made the
    set's account playlist under, so it is the name the outbound ledger holds,
    whatever the job's page words spell today. Read from the record, as the
    library carries it, whether or not the playlist is still there: unlike
    :func:`recorded_playlist`, which wants the live row, this wants the name
    the account playlist was made under, and that name outlives the row.
    """
    return tuple(
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
    )


def recorded_playlist(
    cfg: config.Config, db: Any, job_id: str, folder_id: str
) -> tuple[str, str] | None:
    """The playlist an earlier write made for this job, its id and name, when it is live under the folder.

    THE SESSION RECORD IS THE JOB'S MEMORY OF ITS PLAYLIST. The job's payload is
    frozen at queue time (KTD9) and no landing writes to it; the one later
    write is ``export set --rename`` refreezing the name once a person renamed
    the INSPIRATION playlist (U140). So what a landing wrote is read where the
    landing recorded it: a closed record whose set playlist
    detail names this job and whose source committed, the newest first. A set
    landed in two parts on two days then has one playlist, named for the first
    day, and a backfill adds to it rather than making a twin (the residual on
    a backfill naming the playlist for the day it runs). A
    recorded playlist that is gone, removed, or no longer under the declared
    folder is not an answer, and the write finds or makes one by name.
    """
    for kept in _landed(cfg, job_id):
        playlist_id = str(kept.get("id") or "")
        if not playlist_id:
            continue
        row = db.get_playlist(ID=playlist_id)
        if (
            row is None
            or rb_writer.is_folder(row)
            or rb_writer.node_removed(row)
            or str(getattr(row, "ParentID", "") or "") != folder_id
        ):
            continue
        return playlist_id, str(getattr(row, "Name", "") or kept.get("name") or "")
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
            held, why = collection.row_for(paths)
            if held is None and owned_again is not None:
                held, why = collection.row_for(owned_again(_wanted(report)))
            if held is None:
                left.append(Left(position, artist, title, state, why))
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
        held, why = collection.row_for(paths)
        if held is None:
            left.append(Left(position, artist, title, state, why))
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
    posted: str | None = None,
) -> SetPlaylistPlan:
    """The playlist a landing writes beside its batch, over the files about to land.

    ``files`` pairs each staged file with its target, the native plan's own
    pairs. A downloaded row is tied to a staged file by the match rule over
    exactly those files, as an account playlist is (U113), and the member
    carries the TARGET, since the row is made at the apply and keyed by it.
    A row no staged file answers is asked of the library next, with the
    person's review answers read back, since a track offered at review and
    accepted as a library file was never downloaded and is owned.

    The naming day is the posted day (U136): ``--posted``, else the page's
    upload_date, else the landing day with :data:`POSTED_FALLBACK` on the plan.
    When ``on`` is given it is the day already chosen (a re-plan pins it), so a
    ``--posted`` override survives ``apply_alone``.
    """
    if on is not None and posted is None:
        made = on
        _resolved, fallback = naming_day_for(job, landing=on)
        if _resolved != on:
            fallback = None
    else:
        made, fallback = naming_day_for(job, posted=posted, landing=today())
    folder_id, node = folder_for(db, declared)
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    staged = [source for source, _target in files]
    targets = {source.resolve(): str(target) for source, target in files}
    index = match.index_paths(staged, template=match_cli.library_template(cfg))
    library = _LibraryView(cfg)

    def downloaded(wanted: match.Wanted) -> tuple[tuple[str, ...], str]:
        found = match.resolve_one(
            wanted, index, suppresses=_never_suppressed, suppression_id=_no_suppression_id
        )
        if found.state is match.MatchState.MATCHED:
            tied = [
                targets[Path(path).resolve()]
                for path in found.paths
                if Path(path).resolve() in targets
            ]
            if tied:
                return tuple(tied), LANDED
        return library.paths(wanted), OWNED

    members, left = _members(
        reports, collection=_Collection(cfg, db), downloaded=downloaded, owned_again=None
    )
    return _digested(
        SetPlaylistPlan(
            job_id=job.job_id,
            name=recorded[1] if recorded else (frozen_name(job) or playlist_name(words, on=made)),
            tree_id=node.id,
            folder_display=node.display,
            folder_id=folder_id,
            words=words,
            members=members,
            left=left,
            made_on=made,
            playlist_id=recorded[0] if recorded else "",
            posted_fallback=None if recorded or frozen_name(job) else fallback,
            posted=posted,
            posted_ignored=ignored_posted(job, posted),
        )
    )


def backfill_resolver(
    cfg: config.Config, db: Any
) -> Callable[[Sequence[Mapping[str, Any]]], tuple[tuple[Member, ...], tuple[Left, ...]]]:
    """The backfill's rule, every report resolved against the library as it is now.

    THE WORKER'S VIEW WITHOUT ITS WRITES, :class:`_LibraryView`, and the
    collection indexed once on ``db``: a row the report called owned keeps its
    report paths first and is resolved again only when those paths hold no row
    any more; a downloaded row is asked of the library with a person's review
    answers read back. Built once and asked per job, so the library is indexed
    once however many jobs are read. The INBOX refill (U134) asks the same
    question of an account playlist's job.
    """
    collection = _Collection(cfg, db)
    library = _LibraryView(cfg)

    def resolve(
        reports: Sequence[Mapping[str, Any]],
    ) -> tuple[tuple[Member, ...], tuple[Left, ...]]:
        return _members(
            reports,
            collection=collection,
            downloaded=lambda wanted: (library.paths(wanted), OWNED),
            owned_again=library.paths,
        )

    return resolve


#: Why a track asked of the library by :func:`library_rows` has no row (U144),
#: beside the collection's own two, :data:`NO_ROW` and :data:`AMBIGUOUS_ROWS`.
UNANSWERED = "the match is a question no person has answered"
NOT_HELD = "no library file matches it"
TOMBSTONED = "a version of it was deleted on purpose"


def library_rows(cfg: config.Config, db: Any) -> Callable[[match.Wanted], tuple[str, str]]:
    """Each wanted track's one collection row on ``db``, or empty and why not (U144).

    THE BACKFILL'S RULE FOR A DOWNLOADED ROW, :func:`backfill_resolver`'s,
    asked of a track that has no job report: the match engine over the library
    as it is now with a person's review answers read back, then the one
    collection row the matched file resolves to. Only a MATCHED track has a
    row. A question nobody answered, a track the library lacks and a version
    deleted on purpose are each named, never guessed at. Built once, the
    library indexed once, and asked per track.
    """
    collection = _Collection(cfg, db)
    library = _LibraryView(cfg)

    def row_of(wanted: match.Wanted) -> tuple[str, str]:
        found = library.resolve(wanted)
        if found.state is match.MatchState.MATCHED:
            held, why = collection.row_for(tuple(found.paths))
            return held or "", why
        if found.state is match.MatchState.NEEDS_REVIEW:
            return "", UNANSWERED
        if found.state is match.MatchState.SUPPRESSED:
            return "", TOMBSTONED
        return "", NOT_HELD

    return row_of


def plan_for_backfill(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    job: jobs.Job,
    words: SetWords,
    reports: Sequence[Mapping[str, Any]],
    *,
    on: date | None = None,
    posted: str | None = None,
) -> SetPlaylistPlan:
    """The playlist for a set whose files already landed, every row resolved against the library now.

    THE WORKER'S VIEW WITHOUT ITS WRITES, :class:`_LibraryView`: the library
    as the match engine sees it now, every answer a person gave about a row
    read back, so a track accepted at review is the file they accepted, and
    no question offered or retired by a plan. A row the report called owned
    keeps its report paths first, and is resolved again only when those paths
    hold no row any more.

    The naming day is the posted day (U136), so a backfill a week later finds
    the existing playlist by that name and never makes a twin (R-949).
    When ``on`` is given it is the day already chosen (a re-plan pins it).
    """
    if on is not None and posted is None:
        made = on
        _resolved, fallback = naming_day_for(job, landing=on)
        if _resolved != on:
            fallback = None
    else:
        made, fallback = naming_day_for(job, posted=posted, landing=today())
    folder_id, node = folder_for(db, declared)
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    members, left = backfill_resolver(cfg, db)(reports)
    return _digested(
        SetPlaylistPlan(
            job_id=job.job_id,
            name=recorded[1] if recorded else (frozen_name(job) or playlist_name(words, on=made)),
            tree_id=node.id,
            folder_display=node.display,
            folder_id=folder_id,
            words=words,
            members=members,
            left=left,
            made_on=made,
            playlist_id=recorded[0] if recorded else "",
            posted_fallback=None if recorded or frozen_name(job) else fallback,
            posted=posted,
            posted_ignored=ignored_posted(job, posted),
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
    shown = {
        "set playlist": plan.name,
        "under": where,
        "playlist": (
            f"adds to the playlist an earlier write made (row {plan.playlist_id})"
            if plan.playlist_id
            else "found live by its name under the folder, or made"
        ),
        "set job": plan.job_id,
        "set tracks": len(plan.members),
        "set left out": len(plan.left),
    }
    if plan.posted_fallback:
        shown["posted day"] = plan.posted_fallback["message"]
    if plan.posted_ignored:
        shown["posted day"] = plan.posted_ignored["message"]
    return shown


def posted_note(plan: SetPlaylistPlan) -> list[dict[str, str]]:
    """The warnings about the naming day (U136): it fell back to the landing day, or ``--posted`` was not used."""
    return [
        *([dict(plan.posted_fallback)] if plan.posted_fallback else []),
        *ignored_note(plan),
    ]


def ignored_note(plan: SetPlaylistPlan) -> list[dict[str, str]]:
    """The warning when ``--posted`` was not used because the frozen name won (U136)."""
    return [dict(plan.posted_ignored)] if plan.posted_ignored else []


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


def nothing_note(plan: SetPlaylistPlan, *, left: int | None = None) -> list[dict[str, str]]:
    """The one note a write carries when the set has no member to hold.

    ``left`` is the write's own count when the write ran and found no row to
    add, which is more than the plan's when every landed member's file was
    refused at the move; the plan's count otherwise.
    """
    count = len(plan.left) if left is None else left
    return [
        {
            "code": NOTHING,
            "message": (
                f"no track of the set was owned or landed, so the playlist "
                f"{plan.name!r} was not written; {count} track(s) are listed as left out"
            ),
        }
    ]


def written_note(written: Written) -> list[dict[str, str]]:
    """The one note a write carries naming the playlist it made and what it holds."""
    made = ", created at the playlist root" if written.folder_created else ""
    which = "made by this write" if written.playlist_created else "found and added to"
    return [
        {
            "code": WRITTEN,
            "message": (
                f"the set's playlist {written.name!r} ({which}) holds {written.members} "
                f"track(s) under the folder (row {written.folder_id}{made}), "
                f"{written.added} added by this write and read back from the database"
            ),
        }
    ]


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def _folder_row(db: Any, folder_id: str, folder_display: str) -> tuple[Any, bool]:
    """The folder the playlist goes under, found by the plan's id or created at the root."""
    if folder_id:
        row = db.get_playlist(ID=folder_id)
        if row is None or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the {folder_display!r} folder (row {folder_id}) is not live "
                f"any more, so the set's playlist has nowhere to go; nothing was written",
                origin=_ORIGIN,
                detail={"folder": folder_id, "display": folder_display},
            )
        return row, False
    return db.create_playlist_folder(folder_display), True


def place_playlist(
    db: Any, *, folder_id: str, folder_display: str, name: str
) -> tuple[Any, bool, Any, bool]:
    """The folder and the playlist of ``name`` under it, each found live or made (U144).

    PUBLIC FOR ``crate organize``'s INSPIRATION parity step, which writes a
    set's playlist the way this module does and so must find and make it by
    the same rule: the folder by the plan's id, or created at the root when
    the plan read none; the live playlist of the name under it, or a new one.
    Answers the folder, whether it was made, the playlist, whether it was made.
    """
    folder, folder_created = _folder_row(db, folder_id, folder_display)
    playlist, playlist_created = _named_playlist_row(db, name, folder)
    return folder, folder_created, playlist, playlist_created


def _named_playlist_row(db: Any, name: str, folder: Any) -> tuple[Any, bool]:
    """The live playlist of ``name`` under ``folder``, or one made there."""
    parent_id = str(folder.ID)
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row, False
    return db.create_playlist(name, parent=folder), True


def _playlist_row(db: Any, plan: SetPlaylistPlan, folder: Any) -> tuple[Any, bool]:
    """The playlist the members go in: the recorded one, else found live by name, else made.

    A REMOVED PLAYLIST IS NOT FOUND. rekordbox soft deletes a playlist a
    person removes, and ``ensure_playlist`` matches name and parent alone, so
    a playlist deleted in rekordbox and written into the same day would hold
    memberships nobody can see. The live row of the name is taken, and a new
    one made when none is live. The recorded playlist, when the plan names
    one, was checked live at the plan and is checked again here.
    """
    if plan.playlist_id:
        row = db.get_playlist(ID=plan.playlist_id)
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the set's playlist {plan.name!r} (row {plan.playlist_id}) the plan "
                f"adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.playlist_id, "name": plan.name},
            )
        return row, False
    return _named_playlist_row(db, plan.name, folder)


def write_members(
    db: Any, plan: SetPlaylistPlan, *, by_target: Mapping[str, str] | None = None
) -> Written:
    """Make the playlist under its folder and add every member, pending on ``db``.

    INSIDE A CALLER'S SESSION, which commits or rolls back. ``by_target`` maps a
    landing's targets to the rows it just made; a member whose target made no
    row is left, listed, and the rest are added. The playlist is the one the
    plan names, else the live one of its name under the folder, else made, so
    a backfill run twice adds nothing the second time, and ``add_memberships``
    adds only what is absent. A row two reports resolved to is one member.

    NOTHING IS WRITTEN FOR A SET OF NO MEMBERS, and the answer says so with an
    empty playlist id and every left row listed: a playlist holding nothing
    under a folder kept for good is not the set.
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
    distinct = tuple(dict.fromkeys(ids))
    if not distinct:
        return Written(
            name=plan.name,
            playlist_id="",
            folder_id=plan.folder_id,
            folder_created=False,
            playlist_created=False,
            members=0,
            added=0,
            left=(*left, *plan.left),
        )
    folder, folder_created = _folder_row(db, plan.folder_id, plan.folder_display)
    playlist, playlist_created = _playlist_row(db, plan, folder)
    added = rb_writer.add_memberships(db, playlist, distinct)
    return Written(
        name=plan.name,
        playlist_id=str(playlist.ID),
        folder_id=str(folder.ID),
        folder_created=folder_created,
        playlist_created=playlist_created,
        members=len(distinct),
        added=len(added),
        left=(*left, *plan.left),
        ids=distinct,
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

    EVERY ID ASKED FOR IS READ BACK LIVE, whatever the playlist held before. THE
    ORDER IS HELD ONLY FOR A PLAYLIST THIS COMMIT FILLED, one whose every
    membership it added: a playlist found by its name from an earlier write
    appends what it lacked after what it held, rekordbox's own order for an
    added track, and a second write that fills a gap mid set is not a write
    that failed. A member named twice in the set is one membership and
    counted once.
    """
    wanted = list(dict.fromkeys(written.ids))
    live = set(written.read_back)
    missing = [one for one in wanted if one not in live]
    filled = written.added == len(wanted)
    in_order = [one for one in written.read_back if one in set(wanted)] == wanted
    if missing or (filled and not in_order):
        raise refuse(
            "session-committed-unverified",
            f"the set playlist {written.name!r} ({written.playlist_id}) read back from "
            f"the database holds {len(written.read_back)} live track(s), "
            f"{len(missing)} of the {len(wanted)} the plan named not among them"
            + ("" if missing else " and not in the order the set played them")
            + "; the commit landed and this answer cannot be vouched for",
            origin=_ORIGIN,
            detail={
                "playlist_id": written.playlist_id,
                "planned": wanted,
                "read": list(written.read_back),
                "missing": missing,
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
        cfg, db, declared, job, words, reports, on=plan.made_on, posted=plan.posted
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
            assert written.playlist_id, "a plan with members writes"
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

    ONLY WHEN SOMETHING WAS ADDED OR MADE, the landing's own rule for its tree:
    a same day rerun that found the playlist and added nothing changed no
    row, and a record saying the folder committed would tell a restore
    otherwise.
    """
    if not written.playlist_id:
        return
    if not (written.added or written.playlist_created or written.folder_created):
        return
    record_on(record, written, plan)
    changes = (session.TreeChange(tree=plan.tree_id, created=written.added),)
    session.record_commit(record, plan.tree_id, session.ChangeSummary(changes), cfg)


def record_commit(
    record: session.SessionRecord, written: Written, plan: SetPlaylistPlan, cfg: config.Config
) -> None:
    """The public face of :func:`_record_set_commit`, for the landing's own helper."""
    _record_set_commit(record, written, plan, cfg)


__all__ = [
    "AMBIGUOUS_ROWS",
    "DOWNLOADED_STATES",
    "FOLDER_UNDECLARED",
    "LANDED",
    "LEFT_OUT",
    "NOT_LANDED",
    "NOTHING",
    "NOT_HELD",
    "NOT_RESOLVED",
    "NO_ROW",
    "OWNED",
    "POSTED_FALLBACK",
    "POSTED_IGNORED",
    "RECORD_KEY",
    "SET_KEY",
    "SUPPRESSED",
    "TOMBSTONED",
    "UNANSWERED",
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
    "assert_native",
    "assert_read_back",
    "backfill_resolver",
    "facts",
    "folder_for",
    "identity",
    "ignored_note",
    "ignored_posted",
    "left_warning",
    "library_rows",
    "nothing_note",
    "page_of",
    "naming_day_for",
    "naming_day",
    "payload",
    "place_playlist",
    "plan_for_backfill",
    "plan_for_landing",
    "playlist_name",
    "posted_note",
    "read_back",
    "record_commit",
    "recorded_names",
    "recorded_playlist",
    "record_on",
    "reports_of",
    "set_job_or_refuse",
    "today",
    "frozen_name",
    "words_for",
    "words_from_page",
    "write_members",
    "written_note",
]
