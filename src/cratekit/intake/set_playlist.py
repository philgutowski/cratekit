"""A set intake leaves a permanent playlist of the set under INSPIRATION (U121).

INBOX is a queue the rotation clears, so every set intake also ends with a
playlist under the taxonomy's ``[inspiration]`` folder holding every identified
track the library owns, in the order the set played.

THE NAME IS THE SOURCE SYSTEM'S FORM, ``{M_DD_YY posted} {DJ} {set name} {M-YY
of the set}``, from the page the job froze (``intake_cli.PAGE``) or the flags,
which win. The first word is the posted day (U136). A word neither names is
refused before the gate, since a playlist named from a guess stays for good.

A MEMBER IS A ROW THE PRODUCT'S OWN MATCH RULE TIED TO THE SET, never a guess;
anything else is LEFT and listed by position and name. The write is the
guarded writer's, at a landing inside its single commit and for ``intake
inspiration`` in a session of its own, read back from SQL. Neither touches
INBOX, a beat grid or any content row.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, replace
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
    taxonomy,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import batch_name, fetch, ingest
from cratekit.intake import cli as intake_cli
from cratekit.intake.cli_identify import _note
from cratekit.write import routing_pass, trees

#: The job key a set is queued under, and the only key this module reads.
SET_KEY = "intake.set"

#: The refusal reasons this module owns, reserved in the cause vocabulary.
FOLDER_UNDECLARED = "inspiration-folder-undeclared"
UNNAMED = "set-playlist-unnamed"
#: The page named no upload date, so the naming day fell back to the landing day (U136).
POSTED_FALLBACK = "set-playlist-posted-fallback"
#: ``--posted`` named a day the job's frozen name does not open with, and the
#: frozen name won (U136).
POSTED_IGNORED = "set-playlist-posted-ignored"

#: The session record field naming the set playlist a commit wrote.
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

#: The report states a landing's files were downloaded for (U113's rule).
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


#: The flags that stand in for the page, each with its metavar and help.
_WORD_FLAGS = (
    ("--dj", "NAME", "who played the set, as the playlist names them (default: the uploader "
        "the fetched page named)"),
    ("--set-name", "NAME", "the set's name, abbreviated as you want it in the playlist "
        "(default: the fetched page's title, less the uploader's name in front of it)"),
    ("--set-date", "YYYY-MM", "the month the set is from, YYYY-MM or YYYY-MM-DD (default: "
        "the day the fetched page says the recording went up)"),
    ("--posted", "YYYY-MM-DD", "the day the set went up on its service, as the playlist opens "
        "with (default: the page's upload_date; the landing day when the page names none)"),
)


def add_word_arguments(parser) -> None:
    """The flags that stand in for the page, shared by both verbs."""
    for flag, metavar, text in _WORD_FLAGS:
        parser.add_argument(flag, default=None, metavar=metavar, help=text)


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


def _not_a(flag: str, value: str, kind: str, forms: str, exc: Exception | None = None):
    """The refusal of a date flag that names no ``kind``, so the set cannot be named."""
    why = f" ({exc})" if exc is not None else ""
    return refuse(
        UNNAMED,
        f"{flag} {value!r} is not a {kind}{why}, so the set's playlist cannot be named; "
        f"give it as {forms}",
        remedy=Remedy.FIX_COMMAND_LINE,
        origin=_ORIGIN,
        detail={flag.lstrip("-").replace("-", "_"): value},
    )


def _flag_day(flag: str, value: str, pattern: re.Pattern, kind: str, forms: str) -> date:
    """The day a date flag names, the first for a month that names none, or its refusal."""
    found = pattern.match(value.strip())
    if found is None:
        raise _not_a(flag, value, kind, forms)
    try:
        return date(int(found.group(1)), int(found.group(2)), int(found.group(3) or 1))
    except ValueError as exc:
        raise _not_a(flag, value, kind, forms, exc) from exc


def _page_day(text: str | None, *, month: bool = False) -> date | None:
    """The page's upload day, or the first of its month, or None for no date.

    A page date that is not a date names nothing, and the flag is asked for.
    """
    found = _PAGE_DATE.match((text or "").strip())
    if found is None:
        return None
    try:
        return date(int(found.group(1)), int(found.group(2)), 1 if month else int(found.group(3)))
    except ValueError:
        return None


def _month_of(flag: str | None, page_date: str | None) -> date | None:
    """The set's month: the flag when given, its day checked then dropped, else the page's."""
    if not flag:
        return _page_day(page_date, month=True)
    given = _flag_day("--set-date", flag, _FLAG_DATE, "month", "YYYY-MM or YYYY-MM-DD")
    return given.replace(day=1)


def words_from_page(
    page: Mapping[str, Any] | None,
    *,
    dj: str | None = None,
    set_name: str | None = None,
    set_date: str | None = None,
    job_id: str = "",
) -> SetWords:
    """The name's three words, the flags first and the page after.

    Refused by name when a word is missing, naming exactly the flags still
    wanted. ``job_id`` rides only in the refusal's detail, so a call before
    the job is queued names the set as a call after it does (U129).
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
    return words_from_page(
        page_of(job), dj=dj, set_name=set_name, set_date=set_date, job_id=job.job_id
    )


def frozen_name(job: jobs.Job) -> str:
    """The playlist name ``intake set`` froze on the job for the account and INSPIRATION (U129).

    Empty when the job predates the freeze or the set could not be named then;
    callers fall back to :func:`playlist_name`. ``export set --rename``
    refreezes it (U140), so it need not open with a day.
    """
    payload = job.payload if isinstance(job.payload, Mapping) else {}
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()


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

    ``--posted YYYY-MM-DD`` wins over the page's ``upload_date``; when neither
    names a day, the landing day is used with a warning for the screen. The
    INBOX batch name keeps the landing date.
    """
    if posted:
        return _flag_day("--posted", posted, _POSTED_FLAG, "day", "YYYY-MM-DD"), None
    if (found := _page_day(page_upload_date)) is not None:
        return found, None
    day = landing or today()
    return day, _note(
        POSTED_FALLBACK,
        f"the set's page named no upload date, so its playlists open with the "
        f"landing day {batch_name.set_day_word(day)}; pass --posted YYYY-MM-DD "
        f"to name another day",
    )


def ignored_posted(job: jobs.Job, posted: str | None) -> dict[str, str] | None:
    """The warning when ``--posted`` names a day the job's frozen name does not open with (U136).

    The frozen name wins, so every landing and backfill finds the one
    playlist, and the warning names both days. None when they agree or either
    is absent.
    """
    frozen = frozen_name(job)
    if not posted or not frozen:
        return None
    word = batch_name.set_day_word(naming_day(posted=posted)[0])
    opens = frozen.split()[0]
    if word == opens:
        return None
    return _note(
        POSTED_IGNORED,
        f"--posted {posted.strip()} names the day {word}, but this set's playlists "
        f"keep the name {frozen!r} frozen on its job when it was queued, which "
        f"opens with {opens}; the frozen name wins and --posted was not used",
    )


def naming_day_for(
    job: jobs.Job,
    *,
    posted: str | None = None,
    landing: date | None = None,
) -> tuple[date, dict[str, str] | None]:
    """:func:`naming_day` over the page this job froze."""
    upload = str(page_of(job).get(fetch.PAGE_UPLOAD_DATE) or "").strip()
    return naming_day(posted=posted, page_upload_date=upload, landing=landing)


def playlist_name(words: SetWords, *, on: date | None = None) -> str:
    """The source system's form: ``3_25_26 Public Service NYC Live at Signal 2-26``.

    ``on`` is the posted day from :func:`naming_day`; omitted, the landing day.
    """
    day = on or today()
    return batch_name.set_playlist_form(day, dj=words.dj, name=words.name, month=words.month)


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

    One refusal for both verbs: the playlist is a database node and the
    bridge's writers emit an export. The landing is told it can land without
    ``--set`` and backfill after the cutover.
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
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Left:
    """One track of the set the playlist will not hold, and why."""

    position: int
    artist: str
    title: str
    state: str
    why: str

    def identity(self) -> dict[str, Any]:
        return asdict(self)


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
    #: The playlist an earlier write for this job made, live under the folder,
    #: which this write adds to; empty when found or made by name.
    playlist_id: str = ""
    #: Warning when the naming day fell back to the landing day (U136), or None.
    posted_fallback: dict[str, str] | None = None
    #: The ``--posted`` string the plan was made with, so ``apply_alone``
    #: re-plans without flipping the fallback bit.
    posted: str | None = None
    #: Warning when the frozen name won over ``--posted`` (U136), or None. Not
    #: in :func:`identity`: it changes nothing written, so a re-plan keeps the digest.
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

    Refused by name when the taxonomy declares none, since this module will
    not invent one, and when the root holds it twice, since whichever the
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

        A path two active rows claim is not a row, the native landing's rule:
        one of a duplicate pair is the row that does not play.
        """
        held, _path, why = self.row_and_path(paths)
        return held, why

    def row_and_path(self, paths: Sequence[str]) -> tuple[str | None, str, str]:
        """:meth:`row_for`, with the path the row was found by (U287)."""
        if not paths:
            return None, "", NO_ROW
        ambiguous = False
        for found in trees.match_indexed_rows(
            paths, self._index, root=self._cfg.library.root, prefix_map=self._prefix_map
        ):
            if found.outcome is trees.MatchOutcome.AMBIGUOUS:
                ambiguous = True
                continue
            if found.content_id:
                return str(found.content_id), str(found.requested), ""
        return None, "", (AMBIGUOUS_ROWS if ambiguous else NO_ROW)


class _LibraryView:
    """The library as the match engine sees it, a person's answers read back, nothing written.

    The worker's resolve without the worker's writes: a plan may neither offer
    nor retire a review item, since a plan the person aborts has written
    nothing. A question is answered only by a person's verdict on the item
    the worker already filed, found by the question's own identity.
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

    Only a closed record whose source committed, so a landing that wrote
    nothing is not read as having named a playlist.
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

    R-1017. The name a backfill made the account playlist under, whatever the
    page words spell today, so it outlives the row and is read whether or not
    the playlist is still there.
    """
    return tuple(
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
    )


def recorded_playlist(
    cfg: config.Config, db: Any, job_id: str, folder_id: str
) -> tuple[str, str] | None:
    """The playlist an earlier write made for this job, its id and name, when it is live under the folder.

    THE SESSION RECORD IS THE JOB'S MEMORY OF ITS PLAYLIST, since the payload
    is frozen at the queue (KTD9). A set landed in two parts on two days then
    has one playlist, named for the first day, and a backfill adds to it
    rather than making a twin. A recorded playlist gone, removed or moved out
    of the folder is not an answer, and the write finds or makes one by name.
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
    """No tombstone is consulted: a row is tied to a file this landing holds or to none."""
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


def _members(
    reports: Sequence[Mapping[str, Any]],
    *,
    collection: _Collection,
    downloaded: Callable[[match.Wanted], tuple[tuple[str, ...], str]],
    owned_again: Callable[[match.Wanted], tuple[str, ...]] | None,
) -> tuple[tuple[Member, ...], tuple[Left, ...]]:
    """Each report, in order, as a member or a left row.

    ``downloaded`` answers a missing or offered row with the paths the rule
    tied it to and the state they give it, :data:`LANDED` for a landing's
    staged files and :data:`OWNED` for library files. ``owned_again``
    re-resolves an owned row whose report paths hold no row any more, for the
    backfill; None at a landing, where the report is fresh.
    """
    members: list[Member] = []
    left: list[Left] = []
    for position, report in enumerate(reports, start=1):
        track = report.get("track")
        track = track if isinstance(track, Mapping) else {}
        artist, title = str(track.get("artist") or ""), str(track.get("title") or "")
        state = str(report.get("state") or "")

        def owned(paths: Sequence[str]) -> bool:
            held, why = collection.row_for(paths)
            if held is None:
                left.append(Left(position, artist, title, state, why))
            else:
                members.append(Member(position, artist, title, OWNED, content_id=held))
            return held is not None

        if state == "owned":
            paths = tuple(str(path) for path in (report.get("paths") or ()))
            if owned_again is not None and collection.row_for(paths)[0] is None:
                paths = owned_again(intake_cli.thawed(track))
            owned(paths)
            continue
        if state not in DOWNLOADED_STATES:
            why = SUPPRESSED if state == "suppressed" else NOT_RESOLVED
            left.append(Left(position, artist, title, state, why))
            continue
        paths, how = downloaded(intake_cli.thawed(track))
        if not paths:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        if how == LANDED:
            members.append(Member(position, artist, title, LANDED, target=paths[0]))
            continue
        owned(paths)
    return tuple(members), tuple(left)


def _made_on(job: jobs.Job, on: date | None, posted: str | None) -> tuple[date, dict | None]:
    """The naming day and its fallback warning; a given ``on`` pins a re-plan's day.

    A pinned day keeps the fallback only when the job's page still names no
    day, so a ``--posted`` override survives ``apply_alone``.
    """
    if on is not None and posted is None:
        resolved, fallback = naming_day_for(job, landing=on)
        return on, fallback if resolved == on else None
    return naming_day_for(job, posted=posted, landing=today())


def _planned(
    job: jobs.Job,
    words: SetWords,
    node: taxonomy.Node,
    folder_id: str,
    recorded: tuple[str, str] | None,
    found: tuple[tuple[Member, ...], tuple[Left, ...]],
    made: tuple[date, dict | None],
    posted: str | None,
) -> SetPlaylistPlan:
    """The digested plan; a recorded playlist, else the frozen name, names it."""
    day, fallback = made
    plan = SetPlaylistPlan(
        job_id=job.job_id,
        name=recorded[1] if recorded else (frozen_name(job) or playlist_name(words, on=day)),
        tree_id=node.id,
        folder_display=node.display,
        folder_id=folder_id,
        words=words,
        members=found[0],
        left=found[1],
        made_on=day,
        playlist_id=recorded[0] if recorded else "",
        posted_fallback=None if recorded or frozen_name(job) else fallback,
        posted=posted,
        posted_ignored=ignored_posted(job, posted),
    )
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

    ``files`` pairs each staged file with its target. A downloaded row is
    tied to a staged file by the match rule over exactly those files (U113)
    and the member carries the TARGET, since its row is made at the apply. A
    row no staged file answers is asked of the library with review answers
    read back, since a track accepted at review as a library file is owned.
    """
    made = _made_on(job, on, posted)
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

    found = _members(
        reports, collection=_Collection(cfg, db), downloaded=downloaded, owned_again=None
    )
    return _planned(job, words, node, folder_id, recorded, found, made, posted)


def backfill_resolver(
    cfg: config.Config, db: Any
) -> Callable[[Sequence[Mapping[str, Any]]], tuple[tuple[Member, ...], tuple[Left, ...]]]:
    """The backfill's rule, every report resolved against the library as it is now.

    An owned row keeps its report paths first and is resolved again only when
    they hold no row any more; a downloaded row is asked of the library with
    review answers read back. Built once, the library indexed once, asked per
    job; the INBOX refill (U134) asks the same of an account playlist's job.
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

#: Why a track that is not MATCHED has no row; any other state is :data:`NOT_HELD`.
_NO_MATCH = {match.MatchState.NEEDS_REVIEW: UNANSWERED, match.MatchState.SUPPRESSED: TOMBSTONED}

#: One track's collection row, the file it was found by, and why there is none.
RowAndPath = tuple[str, str, str]


def library_rows(cfg: config.Config, db: Any) -> Callable[[match.Wanted], tuple[str, str]]:
    """Each wanted track's one collection row on ``db``, or empty and why not (U144).

    :func:`library_matches` without the path: the backfill's rule for a
    downloaded row, asked of a track with no job report. Only a MATCHED track
    has a row; a question nobody answered, a track the library lacks and a
    version deleted on purpose are each named, never guessed at.
    """
    row_of = library_matches(cfg, db)

    def row(wanted: match.Wanted) -> tuple[str, str]:
        held, _path, why = row_of(wanted)
        return held, why

    return row


def collection_rows(cfg: config.Config, db: Any) -> Callable[[Sequence[str]], RowAndPath]:
    """The one row each set of library paths resolves to on ``db``, with its path (U287)."""
    collection = _Collection(cfg, db)

    def row_of(paths: Sequence[str]) -> RowAndPath:
        held, path, why = collection.row_and_path(tuple(paths))
        return held or "", path, why

    return row_of


def library_matches(cfg: config.Config, db: Any) -> Callable[[match.Wanted], RowAndPath]:
    """Each wanted track's collection row and the library file it was found by (U287).

    Built once, the library indexed once, and asked per track. ``sync
    removed`` asks whether that file sits where the landing filed it.
    """
    row_of = collection_rows(cfg, db)
    library = _LibraryView(cfg)

    def found_by(wanted: match.Wanted) -> RowAndPath:
        found = library.resolve(wanted)
        if found.state is match.MatchState.MATCHED:
            return row_of(found.paths)
        return "", "", _NO_MATCH.get(found.state, NOT_HELD)

    return found_by


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

    :func:`backfill_resolver`'s rule, no question offered or retired by a
    plan. The naming day is the posted day (U136), so a backfill a week later
    finds the existing playlist by that name and never makes a twin (R-949).
    """
    made = _made_on(job, on, posted)
    folder_id, node = folder_for(db, declared)
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    found = backfill_resolver(cfg, db)(reports)
    return _planned(job, words, node, folder_id, recorded, found, made, posted)


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------


def payload(plan: SetPlaylistPlan) -> dict[str, Any]:
    """The plan as a gate shows it: one item per member, then one per left row."""
    items = [{"action": "add", **one.identity()} for one in plan.members]
    items += [{"action": "leave", **one.identity()} for one in plan.left]
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
    # The frozen name winning over --posted is the day said, when both are.
    if note := plan.posted_ignored or plan.posted_fallback:
        shown["posted day"] = note["message"]
    return shown


def posted_note(plan: SetPlaylistPlan) -> list[dict[str, str]]:
    """The warnings about the naming day (U136): it fell back, or ``--posted`` was not used."""
    return [*([dict(plan.posted_fallback)] if plan.posted_fallback else []), *ignored_note(plan)]


def ignored_note(plan: SetPlaylistPlan) -> list[dict[str, str]]:
    """The warning when ``--posted`` was not used because the frozen name won (U136)."""
    return [dict(plan.posted_ignored)] if plan.posted_ignored else []


LEFT_OUT = "set-playlist-left-out"
WRITTEN = "set-playlist-written"
NOTHING = "set-playlist-nothing-to-write"


def left_warning(left: Sequence[Left]) -> list[dict[str, str]]:
    """The one warning naming every track the playlist does not hold."""
    if not left:
        return []
    named = "; ".join(f"{one.position}. {one.artist} - {one.title} ({one.why})" for one in left)
    return [_note(
        LEFT_OUT,
        f"{len(left)} track(s) of the set are not in its playlist, because "
        f"nothing the product owns or landed was tied to them: {named}",
    )]


def nothing_note(plan: SetPlaylistPlan, *, left: int | None = None) -> list[dict[str, str]]:
    """The one note a write carries when the set has no member to hold.

    ``left`` is the write's own count when it ran and found no row to add,
    more than the plan's when every landed member's file was refused at the move.
    """
    count = len(plan.left) if left is None else left
    return [_note(
        NOTHING,
        f"no track of the set was owned or landed, so the playlist "
        f"{plan.name!r} was not written; {count} track(s) are listed as left out",
    )]


def written_note(written: Written) -> list[dict[str, str]]:
    """The one note a write carries naming the playlist it made and what it holds."""
    made = ", created at the playlist root" if written.folder_created else ""
    which = "made by this write" if written.playlist_created else "found and added to"
    return [_note(
        WRITTEN,
        f"the set's playlist {written.name!r} ({which}) holds {written.members} "
        f"track(s) under the folder (row {written.folder_id}{made}), "
        f"{written.added} added by this write and read back from the database",
    )]


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

    Public for ``crate organize``'s INSPIRATION parity step, which must find
    and make a set's playlist by this module's rule. Answers the folder,
    whether it was made, the playlist, whether it was made.
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

    A removed playlist is not found: rekordbox soft deletes a playlist a
    person removes, and memberships written into it nobody could see. The
    recorded playlist, checked live at the plan, is checked again here.
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

    Inside a caller's session, which commits or rolls back. ``by_target`` maps
    a landing's targets to the rows it just made; a member whose target made
    no row is left. ``add_memberships`` adds only what is absent, so a
    backfill run twice adds nothing, and a row two reports resolved to is one
    member. Nothing is written for a set of no members: an empty playlist
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

    Every id asked for is read back live. The order is held only for a
    playlist this commit filled, every membership added: a playlist found by
    name appends what it lacked after what it held, rekordbox's own order, so
    a second write that fills a gap mid set is not a failure. A member named
    twice is one membership.
    """
    wanted = list(dict.fromkeys(written.ids))
    live = set(written.read_back)
    missing = [one for one in wanted if one not in live]
    filled = written.added == len(wanted)
    named = set(wanted)
    in_order = [one for one in written.read_back if one in named] == wanted
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

    None, with nothing opened, for a plan of no members. THE SESSION SPINE IS
    CALLED, NOT REBUILT: the gates with a record kept, a capture verified
    before anything is written, the analysis watch over the roots named, the
    commit witness, and the guarded commit. The plan is taken again on this
    handle first, the rotation's rule, since the approved plan was read on a
    handle that has closed and a digest that moved writes nothing.
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
        record, capture = trees.attached_capture(gates, cfg, db)
        try:
            written = write_members(db, plan)
            assert written.playlist_id, "a plan with members writes"
            rb_writer.commit_guarded(db)
        except BaseException:
            trees.rollback_quietly(db)
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

    The landing calls this beside its own record, through
    :func:`record_commit`, so a restore sees both trees by name. Only when
    something was added or made: a rerun that changed no row must not tell a
    restore the folder committed.
    """
    if not written.playlist_id:
        return
    if not (written.added or written.playlist_created or written.folder_created):
        return
    record.detail[RECORD_KEY] = {
        "id": written.playlist_id,
        "name": written.name,
        "job": plan.job_id,
        "folder": written.folder_id,
    }
    changes = (session.TreeChange(tree=plan.tree_id, created=written.added),)
    session.record_commit(record, plan.tree_id, session.ChangeSummary(changes), cfg)


#: The public face of :func:`_record_set_commit`, for the landing's own helper.
record_commit = _record_set_commit
