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
the music folder, because both media make that folder and it stays as long as
the tracks it holds are in the library. The native writer finds a playlist by
its name under INBOX and adds to it, so a name reused there would merge two
batches silently.

A PLAYLIST THE AUTHOR MADE ON THE ACCOUNT KEEPS ITS OWN NAME (U113). The files
of a pass still land in the one batch folder named above, and the tracks each
account playlist brought in go into an INBOX playlist named exactly as the
account names it, :func:`inbox_names`. The batch playlist keeps only what no
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
            job
            for job in jobs.list_jobs(store)
            if job.handler_key in intake_cli.INTAKE_KEYS
            and job.library_id == cfg.library.volume_id
            and job.state is jobs.JobState.SUCCEEDED
            and missing_cli.in_pass(job, pass_name)
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


def taken(cfg: config.Config, name: str) -> bool:
    """Whether a batch folder of ``name`` is under the music folder.

    A link of that name counts as taken whether or not it leads anywhere, since
    a landing could not make its folder there either. Asked by :func:`free` to
    choose and by the landing again under its lock, since the choice is made
    before the gate and another landing can take the name in between.
    """
    return os.path.lexists(landing.target_dir(cfg, name))


def free(cfg: config.Config, base: str) -> str:
    """``base``, or ``base 2``, ``base 3`` and on, the first no batch folder holds."""
    candidate, count = base, 1
    while taken(cfg, candidate):
        count += 1
        candidate = f"{base} {count}"
    return candidate


def inbox_names(wanted: Iterable[str], held: Iterable[str], *, batch: str) -> tuple[str, ...]:
    """The INBOX playlist each account playlist lands as, in order (U113).

    EXACTLY THE ACCOUNT'S NAME, ``Sunset Warmup`` for ``Sunset Warmup``, with no
    date and nothing made folder safe, since a playlist name is not a path. A
    name already ``held`` under INBOX, the batch's own, or one an earlier
    playlist of this landing took, gets `` 2``, `` 3`` and on, so one landing
    never adds its tracks to another's playlist. Compared exactly, the way the
    database writer finds a playlist by its name.
    """
    taken = {*held, batch}
    named: list[str] = []
    for base in wanted:
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


__all__ = [
    "DOWNLOADS",
    "FAVORITES",
    "LABELS",
    "PLAYLISTS",
    "SET",
    "free",
    "inbox_names",
    "is_default_shape",
    "job_word",
    "joined",
    "label_words",
    "pass_jobs",
    "readable",
    "source_words",
    "taken",
    "today",
]
