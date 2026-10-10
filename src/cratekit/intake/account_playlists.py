"""Which playlist on the account each file of a landing came from (U113).

A pass sweeps the playlists the author made on the streaming account, and each
one becomes an INBOX playlist of its own, named exactly as the account names
it, holding the tracks that playlist brought in. This module answers the one
question that needs: which of the files about to land did which playlist ask
for. The name itself is chosen by :func:`cratekit.intake.batch_name.inbox_names`
and written by whichever medium lands the batch.

WHAT A PLAYLIST ASKED FOR IS READ FROM ITS JOB, never from the account again.
``crate sync all`` queues one ``intake.playlist`` job per playlist and records
the account's name for it on the job (``intake_cli.PLAYLIST_NAME``). Each item's
committed report says what the track resolved to, and the rows a landing can
carry are the ones the download was made from, ``missing`` and ``offered``. A
job with no recorded name, queued by a build before this unit or by ``crate
intake playlist`` alone, claims nothing, so its files stay in the batch's own
playlist exactly as they did. The hearts are a job of the same key and are not
a playlist the author made, so they claim nothing either.

A FILE IS TIED TO A ROW BY THE PRODUCT'S OWN MATCH RULE, for the reason the
label filing gives: ``acquire download`` stamps no provider id on a file. The
index is of THE FILES THE LANDING PLANNED and nothing else, since download
staging also holds partial downloads of attempts that never finished. A row
that resolves only to something close, a different version, claims nothing,
and the file stays in the batch's playlist rather than being filed by a guess.

A TRACK TWO PLAYLISTS BOTH ASKED FOR IS A MEMBER OF BOTH. The download fetched
it once, and each playlist's rows resolve to that one file.

TRACKS THE LIBRARY ALREADY OWNED ARE NOT ADDED, decided 2026-10-03 and recorded
as R-905. An owned row was resolved to a file already in the library and was
not downloaded, so it is not part of what this landing brought in. INBOX is the
listening queue that ``route inbox`` and the rotation work over, and a track
already filed under BY GENRE put back in it would be queued a second time.
Mirroring the whole account playlist would also need each owned file's row in
the collection, found by path, on both media, which no verb does yet.

THE HEARTS ARE TIED TO THEIR FILES THE SAME WAY, SINCE U120, and for another
purpose: a file the pass's hearts job asked for is a heart, and the landing
puts it into All Favorites and its quarter beside its INBOX playlist. The
hearts claim no INBOX playlist of their own, as before. The quarter is read
from the date the job froze on the row (``intake_cli.HEARTED``), never from
the account again, and a row frozen with no date is an undated heart.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.acquire import match, match_cli
from cratekit.core import config, jobs, session
from cratekit.favorites import placeholders
from cratekit.intake import batch_name, ingest
from cratekit.intake import cli as intake_cli

#: The report states a landing's files were downloaded for. ``owned`` and
#: ``suppressed`` rows were never downloaded, so no file of the landing is theirs.
CARRIED_STATES = frozenset({"missing", "offered"})

#: The job key a playlist of the account is queued under.
PLAYLIST_KEY = "intake.playlist"


@dataclass(frozen=True, slots=True)
class Source:
    """One playlist on the account a pass swept, and the rows it asked for."""

    playlist_id: str
    #: The account's name for it, exactly as the sweep listed it.
    name: str
    job_id: str
    wanted: tuple[match.Wanted, ...]


@dataclass(frozen=True, slots=True)
class Claimed:
    """One INBOX playlist a landing writes for one playlist on the account."""

    #: The name it lands as, the account's own or that with `` 2`` and on.
    name: str
    #: The account's name for it, which ``name`` differs from only by a count.
    account_name: str
    playlist_id: str
    #: The planned files it holds, in the order the landing planned them.
    files: tuple[Path, ...]

    def identity(self) -> dict[str, Any]:
        """What a gate's digest covers for it, so another split is another plan."""
        return {
            "name": self.name,
            "account": self.playlist_id,
            "files": [path.name for path in self.files],
        }


@dataclass(frozen=True, slots=True)
class HeartRow:
    """One heart a hearts job carried: the row, and when the account said it was made."""

    wanted: match.Wanted
    hearted: datetime | None
    #: The provider's identifier, the job's item key.
    ref: str
    job_id: str
    #: Whether the job SAID anything about the date: a row frozen by a build
    #: before U120 carries no key at all, and its quarter is nobody's to guess.
    known: bool = True

    @property
    def title(self) -> str:
        return f"{self.wanted.artist} - {self.wanted.spelled or self.wanted.title}"


@dataclass(frozen=True, slots=True)
class Hearted:
    """One planned file that is a heart, and the quarter playlist it goes to (U120)."""

    path: Path
    hearted: datetime | None
    ref: str
    known: bool = True

    @property
    def quarter(self) -> str | None:
        """The quarter playlist, ``Undated`` for a heart the account dates nowhere,
        and None for one whose job never said, which the backfill dates later."""
        return placeholders.quarter_label(self.hearted) if self.known else None


def is_hearts_job(job: jobs.Job) -> bool:
    """Whether ``job`` listed the account's hearts, whatever queued it."""
    return (
        job.handler_key in intake_cli.INTAKE_KEYS
        and str((job.payload or {}).get("source_id") or "") == intake_cli.FAVORITES_SOURCE_ID
    )


def carried_hearts(store, job: jobs.Job) -> tuple[HeartRow, ...]:
    """The rows a hearts job's download was made from, each with its frozen date.

    THE SAME STATES A PLAYLIST'S CLAIM READS, ``missing`` and ``offered``: an
    owned heart was never downloaded, so it is not a heart this build lands,
    which is the brief's conservative answer to the owned hearts not in All
    Favorites. The date is the row's own frozen key, read as the job froze it.
    """
    from cratekit.intake import missing_cli

    found: list[HeartRow] = []
    for report in missing_cli.job_reports(store, job):
        if report.get("state") not in CARRIED_STATES:
            continue
        said = report.get("track") or {}
        wanted = intake_cli.thawed(said)
        found.append(
            HeartRow(
                wanted=wanted,
                hearted=placeholders.parse_hearted(said.get(intake_cli.HEARTED)),
                ref=str(said.get("ref") or report.get("item_id") or ""),
                job_id=job.job_id,
                known=intake_cli.HEARTED in said,
            )
        )
    return tuple(found)


def prefer_dated(held: HeartRow | None, row: HeartRow) -> bool:
    """Whether ``row`` is the mention of a heart to keep over ``held``.

    ONE RULE FOR THE LANDING AND THE BACKFILL: the first mention, unless a
    later one knows the date where the first did not, since a job frozen by
    this build knows and an older one does not, and two readers that chose
    differently would put one heart in two quarters.
    """
    return held is None or (not held.known and row.known)


def hearts(cfg: config.Config, pass_name: str) -> tuple[HeartRow, ...]:
    """Every heart the pass's hearts jobs carried, in queue order, a row once."""
    found: dict[str, HeartRow] = {}
    with jobs.open_store() as store:
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
        for job in queued:
            if not is_hearts_job(job):
                continue
            for row in carried_hearts(store, job):
                if prefer_dated(found.get(row.ref), row):
                    found[row.ref] = row
    return tuple(found.values())


def hearted(
    cfg: config.Config, pass_name: str | None, files: Sequence[Path]
) -> tuple[Hearted, ...]:
    """Which of the planned ``files`` the pass's hearts asked for, with each one's quarter.

    THE ONE MATCH RULE :func:`claims` USES, over the planned files only, and
    the same answer for a landing of no pass: nothing, since no job ties a
    file to a heart then (a residual of U120, placed later by the backfill).
    A heart two rows resolve to one file for is one heart, the first row's.
    """
    if not pass_name or not files:
        return ()
    rows = hearts(cfg, pass_name)
    if not rows:
        return ()
    index = match.index_paths(files, template=match_cli.library_template(cfg))
    planned = {path.resolve(): path for path in files}
    order = {path: position for position, path in enumerate(files)}
    found: dict[Path, Hearted] = {}
    for row in rows:
        resolved = match.resolve_one(
            row.wanted,
            index,
            suppresses=_never_suppressed,
            suppression_id=_no_suppression_id,
        )
        if resolved.state is not match.MatchState.MATCHED:
            continue
        for path in resolved.paths:
            held = planned.get(Path(path).resolve())
            if held is not None and held not in found:
                found[held] = Hearted(path=held, hearted=row.hearted, ref=row.ref, known=row.known)
    return tuple(sorted(found.values(), key=lambda one: order[one.path]))


def _named(job: jobs.Job) -> str | None:
    """The account's name the job recorded, or None for a job that is not one of his playlists."""
    payload = job.payload or {}
    if job.handler_key != PLAYLIST_KEY:
        return None
    if str(payload.get("source_id") or "") == intake_cli.FAVORITES_SOURCE_ID:
        return None
    name = payload.get(intake_cli.PLAYLIST_NAME)
    if not isinstance(name, str) or not name.strip():
        return None
    return name


def sources(cfg: config.Config, pass_name: str) -> tuple[Source, ...]:
    """Every playlist of the account the pass ``pass_name`` swept, in queue order.

    The jobs are :func:`batch_name.pass_jobs`'s, the ones that SUCCEEDED, which
    is the comparison ``sync mark`` makes and the set the batch is named for. A
    job whose reports cannot be read refuses, through the reader ``intake
    missing`` and ``sync mark`` share, and the refusal comes before the gate,
    since the landing could not say which playlist its files belong to.
    """
    from cratekit.intake import missing_cli

    found: list[Source] = []
    with jobs.open_store() as store:
        # IN THE ORDER THE SWEEP QUEUED THEM, which the store lists newest first.
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
        for job in queued:
            name = _named(job)
            if name is None:
                continue
            reports = missing_cli.job_reports(store, job)
            found.append(
                Source(
                    playlist_id=str((job.payload or {}).get(intake_cli.SOURCE) or ""),
                    name=name,
                    job_id=job.job_id,
                    wanted=tuple(
                        intake_cli.thawed(report["track"])
                        for report in reports
                        if report.get("state") in CARRIED_STATES
                    ),
                )
            )
    return tuple(found)


def _never_suppressed(_recording: str, _address: object) -> bool:
    """No tombstone is consulted: a row is tied to a file this landing holds or to none."""
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


def claims(
    found: Sequence[Source], files: Sequence[Path], *, template: Any = None
) -> tuple[tuple[Source, tuple[Path, ...]], ...]:
    """Each source and the planned files its rows resolve to, sources that claim none left out.

    ``files`` are the landing's planned files, and the order each source's
    files are given in is theirs. ``template`` is the library's naming template,
    which is ``match_cli.library_view``'s builder rule.
    """
    if not found or not files:
        return ()
    index = match.index_paths(files, template=template)
    planned = {path.resolve(): path for path in files}
    order = {path: position for position, path in enumerate(files)}
    claimed: list[tuple[Source, tuple[Path, ...]]] = []
    for source in found:
        members: set[Path] = set()
        for wanted in source.wanted:
            resolved = match.resolve_one(
                wanted,
                index,
                suppresses=_never_suppressed,
                suppression_id=_no_suppression_id,
            )
            if resolved.state is not match.MatchState.MATCHED:
                continue
            for path in resolved.paths:
                held = planned.get(Path(path).resolve())
                if held is not None:
                    members.add(held)
        if members:
            claimed.append((source, tuple(sorted(members, key=order.__getitem__))))
    return tuple(claimed)


def split(
    cfg: config.Config, pass_name: str | None, files: Sequence[Path]
) -> tuple[tuple[Source, tuple[Path, ...]], ...]:
    """What each playlist of the account the pass swept claims of ``files``.

    Nothing for a landing given no pass, which is a landing of files nobody
    can trace to a playlist, and nothing for a plan of no files.
    """
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
    if not found:
        return ()
    return claims(found, files, template=match_cli.library_template(cfg))


def named(
    claimed: Sequence[tuple[Source, tuple[Path, ...]]], held: Iterable[str], *, batch: str
) -> tuple[Claimed, ...]:
    """Each claim with the INBOX name it lands as, given the names INBOX holds."""
    names = batch_name.inbox_names(
        (source.name for source, _files in claimed), held, batch=batch
    )
    return tuple(
        Claimed(
            name=name,
            account_name=source.name,
            playlist_id=source.playlist_id,
            files=files,
        )
        for name, (source, files) in zip(names, claimed, strict=True)
    )


def pending_names(cfg: config.Config) -> tuple[str, ...]:
    """Every account playlist an intake file still waiting on its import names.

    Rekordbox has not seen such a file, so no Fresh Export holds its playlists,
    and a second landing named only against the export would give one of them
    the same name. Read from the intake records, which list each by name.
    """
    records, _unreadable = session.scan_log(cfg)
    return tuple(
        str(entry["name"])
        for record in records
        if record.workflow == ingest.INTAKE_WORKFLOW
        and record.state is session.SessionState.AWAITING_IMPORT
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ()
        if isinstance(entry, dict) and entry.get("name")
    )


def unclaimed(files: Sequence[Path], claimed: Iterable[Claimed]) -> tuple[Path, ...]:
    """The planned files no account playlist claimed, which stay in the batch's playlist."""
    taken = {path for one in claimed for path in one.files}
    return tuple(path for path in files if path not in taken)


__all__ = [
    "CARRIED_STATES",
    "Claimed",
    "HeartRow",
    "Hearted",
    "Source",
    "carried_hearts",
    "claims",
    "hearted",
    "hearts",
    "is_hearts_job",
    "named",
    "pending_names",
    "prefer_dated",
    "sources",
    "split",
    "unclaimed",
]
