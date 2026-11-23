"""The name a landing gives its batch when nobody names it (U110).

A batch is a folder under the music folder and a playlist under INBOX, both
named ``<date> <source>``, ``2026-10-03 Tidal playlists``, read at a glance.
The run identifier still names the intake file, where the mark verbs find
their pass. The source is read from what was queued, never typed; the first
row that says anything decides:

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

TWO LANDINGS ON ONE DAY FROM ONE SOURCE NEVER SHARE A PLAYLIST: the second gets
`` 2``. A name is taken while its folder is under the music folder or a
session record keeps it (a shelve's, or a native landing's, which makes no such
folder, U164), since the native writer adds to an INBOX playlist by name and a
reused name would merge two batches silently. A Bandcamp batch is named by
:func:`bandcamp` (U179). An account playlist keeps its own name, dated at the
end (U113, U175), :func:`inbox_names`.

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
from cratekit.intake import ingest, landing

#: The words for each kind of pass job, in the order they are joined.
PLAYLISTS = "Tidal playlists"
FAVORITES = "Favorites"
SET = "Set"
#: More than one label in one manifest.
LABELS = "Labels"
#: What a batch of Bandcamp purchases came from, before its label (U179).
BANDCAMP = "Bandcamp"
#: A landing handed nothing that says where its files came from.
DOWNLOADS = "Downloads"

_ORDER = (PLAYLISTS, FAVORITES, SET)

#: The intake job key a set is queued under; the hearts share a playlist's key
#: and are told apart by ``source_id``.
_SET_KEY = "intake.set"

#: What a folder name on a library volume cannot carry.
_UNSAFE = re.compile(r'[/\\:*?"<>|\x00-\x1f]')


#: The shape :func:`readable` gives a name, held beside the writer so a reader
#: cannot drift from it (U111).
_DEFAULT_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2} \S")


def is_default_shape(name: str) -> bool:
    """Whether ``name`` has a default batch name's shape, which a person can type too."""
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
    return ingest.spoken(ordered) if ordered else None


def pass_jobs(cfg: config.Config, pass_name: str) -> list[jobs.Job]:
    """The intake jobs of the pass ``pass_name`` names that SUCCEEDED, on this library.

    ``sync mark``'s own comparison; only a success, since a batch is named for
    what it carries.
    """
    from cratekit.intake import missing_cli

    with jobs.open_store() as store:
        return [
            job for job in succeeded_intake_jobs(store, cfg) if missing_cli.in_pass(job, pass_name)
        ]


def succeeded_intake_jobs(store, cfg: config.Config) -> list[jobs.Job]:
    """Every intake job on this library that SUCCEEDED, newest first, of any pass or none."""
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

    A dangling link counts. Asked before the gate and again under the lock. A
    shelve (U154) or a native landing (U164) leaves no folder while its INBOX
    playlist keeps the name, so their records keep it taken. ``recorded`` is
    the set already read, for a caller asking about several names.
    """
    recorded = recorded_names(cfg) if recorded is None else recorded
    return os.path.lexists(landing.target_dir(cfg, name)) or name in recorded


def recorded_names(cfg: config.Config) -> frozenset[str]:
    """Every batch name a shelve moved out of the music folder or a native landing kept (U164)."""
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
    """The folder each batch was last filed in by a native landing, by batch name (U164)."""
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
    """Every session record, FAILING CLOSED on an unreadable one, which would free its name."""
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


#: The INBOX playlist every native landing fills with its new rows (U166),
#: RESERVED, since a batch of that name would be written into and rotated with
#: the waiting rows. A test holds it equal to :data:`cratekit.intake.native.ANALYZE`.
ANALYZE = "Analyze"


def dated(account_name: str, day: date) -> str:
    """An account playlist's INBOX name, ``Lisa_10_27_26 2026-10-27`` (U175)."""
    return f"{account_name} {day.isoformat()}"


def inbox_names(wanted: Iterable[str], held: Iterable[str], *, batch: str) -> tuple[str, ...]:
    """The INBOX playlist each account playlist lands as, in order (U113, U175).

    The account's name exactly (not a path), then :func:`today`'s date. A name
    ``held`` under INBOX, the batch's, or one taken earlier in this landing gets
    `` 2`` and on, compared exactly as the database writer finds a playlist.
    Every name ends in a date, so none is the reserved :data:`ANALYZE`.
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

    ``<date> Bandcamp <Label>`` when every file names one label, compared
    without case, else ``<date> Bandcamp``. Made free as every batch name is.
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


def set_day_word(day: date) -> str:
    """The first word of a set playlist name: ``3_25_26`` for 2026-03-25."""
    return f"{day.month}_{day.day:02d}_{day.year % 100:02d}"


def set_month_word(month: date) -> str:
    """The set's month half of the form: ``5-26`` for May 2026."""
    return f"{month.month}-{month.year % 100:02d}"


def set_playlist_form(day: date, *, dj: str, name: str, month: date) -> str:
    """The set playlist name, ``3_25_26 Public Service NYC Live at Signal 2-26``.

    The day is an argument, never today, so a backfill cannot invent a twin (R-949).
    """
    return f"{set_day_word(day)} {dj} {name} {set_month_word(month)}"
