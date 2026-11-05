"""The name a landing gives its batch when nobody names it (U110).

A batch is a folder under the music folder and one playlist under INBOX, and
both carry its name. That name used to be the run identifier, so INBOX filled
with ``2026-09-23T222241Z-4773_inboxed`` and nobody could tell one batch from
the next without opening it. The default is now the landing's date and what the
batch came from, ``2026-10-03 Tidal playlists``, read at a glance.

THE RUN IDENTIFIER DID NOT GO AWAY, IT MOVED. It names the intake file, which is
where ``sync mark`` reads its pass from and where ``label mark``, ``export
archive`` and ``intake imported`` find theirs, and it stays in the run record.
Only the folder and the playlist lost it.

WHAT THE BATCH CAME FROM IS READ FROM WHAT WAS QUEUED, never typed. The first of
these that says anything decides it:

==========================================  ====================================
what the landing is handed                  the words
==========================================  ====================================
a manifest whose label rows name one label  that label's name, ``Sudbeat``
a manifest whose label rows name several    ``Labels``
a pass whose jobs listed account playlists  ``Tidal playlists``
a pass whose jobs listed the hearts         ``Favorites``
a pass whose jobs listed a set              ``Set``
a pass of more than one of those            joined, ``Tidal playlists and Favorites``
nothing that says                           ``Downloads``
==========================================  ====================================

TWO LANDINGS ON ONE DAY FROM ONE SOURCE NEVER SHARE A PLAYLIST. The second gets
`` 2``, the third `` 3``. A name is taken while a folder of that name is under
the music folder, which the bridge makes and keeps as long as the tracks it
holds are in the library, or while a session record keeps it: a shelve's, or
a database native landing's, which files its batch under the processed tree
and makes no folder under the music folder at all (U164). The native writer
finds a playlist by its name under INBOX and adds to it, so a name reused
there would merge two batches silently.

A BATCH OF BANDCAMP PURCHASES IS NAMED BY ``crate sync bandcamp`` (U179),
``2026-11-01 Bandcamp PULS`` when every file's label tag names that one label
and ``2026-11-01 Bandcamp`` otherwise, through :func:`bandcamp`, made free the
same way, since the files' tags, not a manifest or a pass, say what it holds.

A PLAYLIST THE AUTHOR MADE ON THE ACCOUNT KEEPS ITS OWN NAME (U113), DATED (U175). The files
of a pass still land in the one batch folder named above, and the tracks each
account playlist brought in go into an INBOX playlist named as the account
names it with the landing's date at the end, ``Lisa_10_27_26 2026-10-27``
(U175), :func:`inbox_names`, so INBOX says which pass brought each one while
it stays flat. The batch playlist keeps only what no
account playlist claimed. :mod:`cratekit.intake.account_playlists` decides which
file is whose.

Layer: modules.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from datetime import date

from cratekit.acquire import listdoc
from cratekit.core import config, jobs
from cratekit.intake import cli as intake_cli
from cratekit.intake import landing

#: The words for each kind of pass job, in the order they are joined.
PLAYLISTS = "Tidal playlists"
FAVORITES = "Favorites"
SET = "Set"
#: More than one label in one manifest.
LABELS = "Labels"
#: What a batch of Bandcamp purchases came from, before its label when it has
#: one (U179): ``2026-11-01 Bandcamp PULS``.
BANDCAMP = "Bandcamp"
#: A landing handed nothing that says where its files came from.
DOWNLOADS = "Downloads"

_ORDER = (PLAYLISTS, FAVORITES, SET)

#: The intake job key a set is queued under. ``intake.playlist`` is split by
#: the job's own ``source_id``, because the hearts listing is queued under the
#: same key as a playlist.
_SET_KEY = "intake.set"

#: What a folder name on the volumes a library sits on cannot carry. A colon is
#: why a run identifier loses its own (``land_cli.default_name``), and a slash
#: would make the name two folders.
_UNSAFE = re.compile(r'[/\\:*?"<>|\x00-\x1f]')


#: The shape :func:`readable` gives a name: an ISO date, one space, then the
#: source words. Held here, beside the code that makes the name, so a reader
#: that recognises a batch by it cannot drift from the writer (U111).
_DEFAULT_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2} \S")


def is_default_shape(name: str) -> bool:
    """Whether ``name`` has the shape a landing's default batch name has.

    The shape only. A person can type a name of this shape too, so a reader
    deciding a playlist IS a batch asks something else as well.
    """
    return bool(_DEFAULT_SHAPE.match(name))


def today() -> date:
    """The landing's date, the local calendar's. A seam for the suite."""
    return date.today()


def _folder_safe(text: str) -> str:
    """``text`` as one plain folder name, or ``""`` when nothing of it survives."""
    said = " ".join(_UNSAFE.sub("-", text).split())
    return said.lstrip(".").strip()


def label_words(rows: Iterable[listdoc.ManifestRow]) -> str | None:
    """The words a manifest's label rows say, or None when they name no label."""
    named: dict[str, str] = {}
    for row in rows:
        label = _folder_safe(landing._label_of(row))
        if label:
            named.setdefault(label.casefold(), label)
    if not named:
        return None
    return next(iter(named.values())) if len(named) == 1 else LABELS


def job_word(job: jobs.Job) -> str | None:
    """The word one intake job of a pass says, or None for a job of no pass kind."""
    if job.handler_key == _SET_KEY:
        return SET
    if job.handler_key in intake_cli.INTAKE_KEYS:
        source_id = str((job.payload or {}).get("source_id") or "")
        return FAVORITES if source_id == intake_cli.FAVORITES_SOURCE_ID else PLAYLISTS
    return None


def joined(words: Iterable[str]) -> str | None:
    """Every distinct word, in the fixed order, as a person would say the list."""
    present = set(words)
    ordered = [word for word in _ORDER if word in present]
    if not ordered:
        return None
    if len(ordered) == 1:
        return ordered[0]
    return ", ".join(ordered[:-1]) + " and " + ordered[-1]


def pass_jobs(cfg: config.Config, pass_name: str) -> list[jobs.Job]:
    """The intake jobs of the pass ``pass_name`` names that SUCCEEDED, on this library.

    THE COMPARISON ``sync mark`` MAKES, :func:`missing_cli.in_pass`, and no
    copy of it. ONLY A JOB THAT SUCCEEDED, because a failed or cancelled one is
    what ``intake missing --skip-failed`` leaves out of the download, and a
    batch is named for what it carries.
    """
    from cratekit.intake import missing_cli

    with jobs.open_store() as store:
        return [
            job for job in succeeded_intake_jobs(store, cfg) if missing_cli.in_pass(job, pass_name)
        ]


def succeeded_intake_jobs(store, cfg: config.Config) -> list[jobs.Job]:
    """Every intake job on this library that SUCCEEDED, newest first, of any pass or none.

    THE ONE SPELLING of "a job of this library that carried something", which
    :func:`pass_jobs` narrows to one pass and the favourites backfill (U120)
    reads whole, so a new intake key or a new library identity is learned in
    one place.
    """
    return [
        job
        for job in jobs.list_jobs(store)
        if job.handler_key in intake_cli.INTAKE_KEYS
        and job.library_id == cfg.library.volume_id
        and job.state is jobs.JobState.SUCCEEDED
    ]


def source_words(
    cfg: config.Config,
    *,
    label_rows: Iterable[listdoc.ManifestRow] = (),
    pass_name: str | None = None,
) -> str:
    """What the batch came from, by the table in this module's docstring."""
    said = label_words(label_rows)
    if said is not None:
        return said
    if pass_name:
        said = joined(word for job in pass_jobs(cfg, pass_name) if (word := job_word(job)))
        if said is not None:
            return said
    return DOWNLOADS


def taken(cfg: config.Config, name: str, *, recorded: frozenset[str] | None = None) -> bool:
    """Whether a batch folder of ``name`` is under the music folder, or a record keeps the name.

    A link of that name counts as taken whether or not it leads anywhere, since
    a landing could not make its folder there either. Asked by :func:`free` to
    choose and by the landing again under its lock, since the choice is made
    before the gate and another landing can take the name in between.

    AND A NAME A RECORD KEEPS STAYS TAKEN. The folder rule rested on the folder
    staying under the music folder for as long as its tracks are in the
    library, while the batch's INBOX playlist keeps the name, and the native
    writer adds to an INBOX playlist by name. Two things end that: ``intake
    shelve`` filing the folder away (U154), and a database native landing
    putting its files straight into the processed tree (U164), which makes no
    folder under the music folder at all. A second landing on the same day
    would merge into the first one's playlist silently. Both write a session
    record naming the batch, and those records are read here, so the question
    needs no database handle and is answered the same before the gate and
    under the lock. ``recorded`` is the set already read, for a caller that
    asks about several names in a row.
    """
    recorded = recorded_names(cfg) if recorded is None else recorded
    return os.path.lexists(landing.target_dir(cfg, name)) or name in recorded


def recorded_names(cfg: config.Config) -> frozenset[str]:
    """Every batch name a shelve moved out of the music folder or a native landing kept (U164).

    A native landing names its batch playlist on its record with the commit,
    by :data:`cratekit.intake.native.BATCH_PLAYLIST_KEY`, and the batch it
    filed by :data:`cratekit.intake.native.FILED_BATCH_KEY`; both names are
    kept. A landing that committed nothing wrote neither and made no playlist
    to merge into.
    """
    from cratekit.intake import native, shelve

    names: set[str] = set()
    for record in _records(cfg):
        if record.workflow == shelve.WORKFLOW:
            moved = record.detail.get(shelve.SHELVED_KEY)
            if isinstance(moved, list):
                names.update(
                    str(one["batch"]) for one in moved if isinstance(one, dict) and one.get("batch")
                )
        elif record.workflow == native.WORKFLOW:
            for key in (native.BATCH_PLAYLIST_KEY, native.FILED_BATCH_KEY):
                kept = record.detail.get(key)
                name = kept.get("name") or kept.get("batch") if isinstance(kept, dict) else None
                if name:
                    names.add(str(name))
    return frozenset(names)


def filed_folders(cfg: config.Config) -> dict[str, str]:
    """The folder each batch was last filed in by a native landing, by batch name (U164).

    The records in the order the session log holds them, so a later landing of
    the same name names the folder last.
    """
    from cratekit.intake import native

    folders: dict[str, str] = {}
    for record in _records(cfg):
        if record.workflow != native.WORKFLOW:
            continue
        kept = record.detail.get(native.FILED_BATCH_KEY)
        if isinstance(kept, dict) and kept.get("batch") and kept.get("folder"):
            folders[str(kept["batch"])] = str(kept["folder"])
    return folders


def _records(cfg: config.Config) -> list:
    """Every session record, or the refusal naming the ones this build cannot read.

    FAILS CLOSED ON A RECORD IT CANNOT READ. The reporting scan drops an
    unreadable record, and a name rule that borrowed that policy would read a
    recorded name as free the day one record is damaged, which is the silent
    merge this rule exists to prevent. The refusal names the files, as the
    session gate's own refusal does.
    """
    from cratekit.core import session
    from cratekit.core.cause import Remedy, refuse

    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
        raise refuse(
            "internal-error",
            f"{session.unread_clause(unreadable, cfg)}, so no batch name can be called "
            "free; refusing rather than naming a batch after one a shelve or a landing "
            "may have filed",
            remedy=Remedy.REPORT_DEFECT,
            detail={
                "unreadable": [str(path) for path in unreadable],
                "unlisted": session.log_unlisted(unreadable, cfg),
            },
        )
    return list(parsed)


def free(cfg: config.Config, base: str) -> str:
    """``base``, or ``base 2``, ``base 3`` and on, the first no batch folder holds."""
    recorded = recorded_names(cfg)
    candidate, count = base, 1
    while taken(cfg, candidate, recorded=recorded):
        count += 1
        candidate = f"{base} {count}"
    return candidate


#: The name of the playlist under INBOX every native landing fills with the
#: rows it creates (U166), RESERVED: no batch or account playlist takes it,
#: since one that did would be found as that playlist and written into, and
#: aged and moved by the rotation with the rows still waiting in it.
#: :data:`cratekit.intake.native.ANALYZE` spells the same value, since this
#: module reaches that one through the landing; a test holds the two equal.
ANALYZE = "Analyze"


def dated(account_name: str, day: date) -> str:
    """An account playlist's INBOX name before it is made free: its name, then the day (U175).

    ``Lisa_10_27_26 2026-10-27``. THE DATE GOES AT THE END, Phillip's answer of
    2026-11-01: INBOX stays flat, every playlist keeps the name it was given,
    and the landing's date after it says which pass brought it. The batch's own
    name keeps its date first (U110), since that name is its folder's too.
    """
    return f"{account_name} {day.isoformat()}"


def inbox_names(wanted: Iterable[str], held: Iterable[str], *, batch: str) -> tuple[str, ...]:
    """The INBOX playlist each account playlist lands as, in order (U113, U175).

    THE ACCOUNT'S NAME EXACTLY, THEN THE LANDING'S DATE, ``Sunset Warmup
    2026-10-27`` for ``Sunset Warmup`` (:func:`dated`), with nothing of the
    account's name made folder safe, since a playlist name is not a path.
    The date is :func:`today`'s, the landing's, the one the batch name takes.
    A name already ``held`` under INBOX, the batch's own, or one an
    earlier playlist of this landing took, gets `` 2``, `` 3`` and on after the
    date, so one landing never adds its tracks to another's playlist. Compared
    exactly, the way the database writer finds a playlist by its name.

    :data:`ANALYZE` IS NEVER TAKEN (U166), and since U175 no longer needs
    holding here: every name this gives ends in a date, so none can be the
    reserved ``Analyze``, and an account playlist of that name lands as
    ``Analyze 2026-10-27``.
    """
    on = today()
    taken = {*held, batch}
    named: list[str] = []
    for account_name in wanted:
        base = dated(account_name, on)
        candidate, count = base, 1
        while candidate in taken:
            count += 1
            candidate = f"{base} {count}"
        taken.add(candidate)
        named.append(candidate)
    return tuple(named)


def readable(
    cfg: config.Config,
    *,
    label_rows: Iterable[listdoc.ManifestRow] = (),
    pass_name: str | None = None,
) -> str:
    """The batch name a landing takes when ``--name`` is not given."""
    words = source_words(cfg, label_rows=label_rows, pass_name=pass_name)
    return free(cfg, f"{today().isoformat()} {words}")


def bandcamp(cfg: config.Config, labels: Iterable[str | None]) -> str:
    """The batch name a landing of Bandcamp purchases takes, one label tag per file (U179).

    ``<date> Bandcamp <Label>`` when every file names the same label, compared
    without case as the label filing compares, and ``<date> Bandcamp`` when
    they name several, or any names none: a batch of two labels, or of a label
    and a seller no label names, is not that label's. A label that leaves
    nothing once made folder safe reads as none. Free as every batch name is,
    `` 2`` and on.
    """
    named: dict[str, str] = {}
    unnamed = False
    for label in labels:
        said = _folder_safe(label or "")
        if said:
            named.setdefault(said.casefold(), said)
        else:
            unnamed = True
    words = BANDCAMP
    if len(named) == 1 and not unnamed:
        words = f"{BANDCAMP} {next(iter(named.values()))}"
    return free(cfg, f"{today().isoformat()} {words}")


#: The shape a set's permanent playlist opens with (U121, U136): naming day,
#: who played it, what it is called, and the set's own month. The day is an
#: argument so a backfill names the set and not the day the backfill runs
#: (R-949).


def set_day_word(day: date) -> str:
    """The first word of a set playlist name: ``3_25_26`` for 2026-03-25.

    Month without a leading zero, day with one, two digit year, joined by
    underscores, as the folder's own examples have it (``5_28_26``, ``6_16_26``).
    """
    return f"{day.month}_{day.day:02d}_{day.year % 100:02d}"


def set_month_word(month: date) -> str:
    """The set's month half of the form: ``5-26`` for May 2026."""
    return f"{month.month}-{month.year % 100:02d}"


def set_playlist_form(day: date, *, dj: str, name: str, month: date) -> str:
    """The source system's set playlist name with the naming day as an argument.

    ``3_25_26 Public Service NYC Live at Signal 2-26``. Callers that want the
    posted day pass it; callers that want the landing day pass that. This form
    never defaults to today, so a backfill cannot invent a twin (R-949, U136).
    """
    return f"{set_day_word(day)} {dj} {name} {set_month_word(month)}"


__all__ = [
    "BANDCAMP",
    "DOWNLOADS",
    "FAVORITES",
    "LABELS",
    "PLAYLISTS",
    "SET",
    "bandcamp",
    "filed_folders",
    "free",
    "dated",
    "inbox_names",
    "is_default_shape",
    "job_word",
    "joined",
    "label_words",
    "pass_jobs",
    "readable",
    "recorded_names",
    "set_playlist_form",
    "set_month_word",
    "set_day_word",
    "source_words",
    "succeeded_intake_jobs",
    "taken",
    "today",
]
