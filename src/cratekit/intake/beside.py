"""What the download staging folder holds beside a batch's own tracks (R-1467, R-1499).

Every download stages into the one folder, and ``intake land`` lands the whole
of it, so a verb that ends at a landing lands, under its own manifest and
pass, whatever else the folder holds. R-1467 made ``label sync --go`` read the
folder first and refuse beside anything that is not its own. R-1499 found
``crate sync land`` landing the same way, a label go's download waiting at its
landing's gate above all, so the reading is lifted here, out of
:mod:`cratekit.label.go`, and both verbs call this one.

WHAT A LANDING TAKES IS THE FOLDER, read as the landing reads it,
:func:`cratekit.intake.landing.listing`. A file there that is one of the
batch's own downloaded tracks, at the name it was downloaded under, is its
own. EVERY OTHER FILE IS BESIDE IT, whoever put it there: a track of another
download at its download name, a go's, a sync pass's, a plain ``acquire
download``'s or a fallback fetch's (any job that recorded the file as its
artifact), and a file no download names, which a tail's ``name apply`` renamed
or a person put there. Attribution, which job and which pass, is for the
message; the decision is the folder.

A BATCH'S OWN TRACKS RENAMED BY ITS OWN TAIL ARE READ AS ITS OWN BY A RECORD,
NEVER BY A COUNT. The tail renames every track before the landing's gate, so a
batch taken on again finds its tracks under names no download recorded.
:func:`keep` keeps each file the folder holds when the tail stops, by name,
size and modification time, the identity the landing's own digest reads, and
:func:`beside` reads a file no download names as the batch's own only when it
is one of those, and none once the batch's pass has a landing proof. A label
go's record is kept under its job (:func:`go_record`), a sync pass's under its
pass (:func:`pass_record`).

WHAT ARRIVES WHILE THE TAIL RUNS IS CAUGHT AFTER IT. A download another
process finishes during the tail is renamed by its ``name apply`` with the
batch's own, and nothing tells them apart after that. :func:`settled` is
taken as the tail starts and :func:`arrived` compares the folder with it
before the landing is planned; anything new refuses, and no record is kept.

A FOLDER OR A LIBRARY ROOT THAT CANNOT BE READ REFUSES, never reads as nothing
beside.

The label go's origin key and its continue command are spelled here rather
than imported, because :mod:`cratekit.label.go` imports this module and the
intake package does not import the go; the go names them from here.
"""

from __future__ import annotations

import json
import os
import shlex
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import listdoc
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli
from cratekit.intake.land_cli import default_name
from cratekit.intake.landing import listing as folder_listing
from cratekit.intake.missing_cli import RUN_ID, SYNCED_SUFFIX

#: The payload key every job a label go queues carries, naming its run and
#: manifest (U108). Spelled here, the go names it from here.
ORIGIN_KEY = "label_sync"

#: The payload key naming the run a job was queued under.
RUN_KEY = RUN_ID

#: Where a label go's tail record is kept under the queue root, one per job.
TAILS_DIRNAME = "label-go-tails"

#: Where a sync pass's tail record is kept under the queue root, one per pass.
PASS_TAILS_DIRNAME = "sync-pass-tails"

#: The handler key of ``acquire download``'s job, the only one a sync pass's
#: list is downloaded by.
DOWNLOAD_KEY = "acquire.download"

#: How many of the files no download names a refusal lists by name.
UNNAMED_SHOWN = 8

#: A file's identity in the folder: name, size, modification time.
Identity = tuple[str, int, int]


def origin_run(job: jobs.Job) -> str | None:
    """The run whose label go queued ``job``, off its origin, or None for another job."""
    origin = (job.payload or {}).get(ORIGIN_KEY)
    run = origin.get("run") if isinstance(origin, Mapping) else None
    return run if isinstance(run, str) and run else None


def continue_command(run_id: str) -> str:
    """The command that takes a label go's download on to its landing (U239)."""
    return shlex.join(["crate", "--run", run_id, "label", "sync", "--go"])


def pass_continue_command(run_id: str) -> str:
    """The command that takes a sync pass on to its landing (U183)."""
    return shlex.join(["crate", "sync", "land", "--pass-run", run_id])


def pass_of(job: jobs.Job) -> str | None:
    """The sync pass whose download ``job`` is, by its list's name, or None (R-1499).

    A sync pass lists its missing tracks into ``<pass>.list.json``, its pass
    named ``<run>_synced`` (:data:`cratekit.intake.missing_cli.SYNCED_SUFFIX`),
    and downloads that list; the name a pass's list and its landing share is
    how ``cli.tail`` names a pass's download too. A download whose list is
    named otherwise is no pass's.
    """
    if job.handler_key != DOWNLOAD_KEY:
        return None
    listed = Path(str((job.payload or {}).get(acquire_cli.LIST) or "")).name
    name = listed.removesuffix(listdoc.LIST_SUFFIX)
    if name == listed or not name.endswith(SYNCED_SUFFIX):
        return None
    return name


def pass_name(run_id: str) -> str:
    """The pass a sync run lists and lands under, ``<run without colons>_synced``."""
    return f"{default_name(run_id)}{SYNCED_SUFFIX}"


def _pass_runs(store: jobs.JobStore, library_id: str) -> dict[str, str]:
    """Each sync pass of this library by its name, to the run its intake jobs carry."""
    found: dict[str, str] = {}
    for job in jobs.list_jobs(store):
        run = str((job.payload or {}).get(RUN_KEY) or "")
        if run and job.handler_key in intake_cli.INTAKE_KEYS and job.library_id == library_id:
            found.setdefault(pass_name(run), run)
    return found


def resolved(path: Path | str) -> Path:
    return Path(path).expanduser().absolute().resolve()


def identity(path: Path) -> Identity:
    """A file in the folder as the landing's own digest names it: name, size, mtime."""
    stat = path.stat()
    return (path.name, stat.st_size, stat.st_mtime_ns)


def go_record(cfg: config.Config, job_id: str) -> Path:
    """Where a label go's tail record is kept, under its download job (R-1467)."""
    return jobs.store_dir(cfg) / TAILS_DIRNAME / f"{job_id}.json"


def pass_record(cfg: config.Config, name: str) -> Path:
    """Where a sync pass's tail record is kept, under its pass (R-1499)."""
    return jobs.store_dir(cfg) / PASS_TAILS_DIRNAME / f"{name}.json"


def _artifacts(store: jobs.JobStore, job_id: str) -> Iterable[Path]:
    return (
        resolved(item.artifact)
        for item in jobs.items(store, job_id)
        if item.state is jobs.ItemState.DONE and item.artifact
    )


def keep(
    store: jobs.JobStore, record: Path, staging: Path, own: Collection[str], *, key: str
) -> int:
    """Keep what the staging folder holds as a batch's tail stops, and return how many.

    THIS IS THE ONE RECORD OF A BATCH'S RENAMED TRACKS: each file the folder
    holds when the tail stops, by its name, size and modification time, so a
    file put there since, under any name, is never read as the batch's own.
    The folder held nothing but this batch when its tail started (every tail
    is refused beside anything else), and a file another download recorded at
    its download name is left out, since it is that download's. ``own`` is the
    batch's download jobs, ``key`` what the record names it by.

    Called by the CLI layer, which runs the tail, whichever way the tail ends;
    a record that cannot be written raises, for the caller to name.
    """
    folder = resolved(staging)
    held = [resolved(path) for path in folder_listing(folder)] if folder.is_dir() else []
    theirs = {
        path
        for job in jobs.list_jobs(store)
        if job.job_id not in own
        for path in _artifacts(store, job.job_id)
    }
    kept = sorted(identity(path) for path in held if path not in theirs)
    record.parent.mkdir(parents=True, exist_ok=True)
    written = record.with_name(f".{record.name}.tmp")
    written.write_text(json.dumps({"job": key, "folder": str(folder), "files": kept}))
    os.replace(written, record)
    return len(kept)


def kept(record: Path) -> frozenset[Identity]:
    """What :func:`keep` kept at ``record``, or nothing.

    NOTHING WHEN IT CANNOT BE READ, which is the safe reading here: a file the
    record does not name is beside the batch, so a lost record refuses the
    batch's own tail and never lands a file as its own.
    """
    try:
        document = json.loads(record.read_text())
        return frozenset(
            (str(name), int(size), int(mtime)) for name, size, mtime in document["files"]
        )
    except (OSError, ValueError, KeyError, TypeError):
        return frozenset()


@dataclass(frozen=True, slots=True)
class Waiting:
    """A download the staging folder may hold that no landing has taken (R-1467).

    ``run`` is the run whose label go queued it, ``pass_name`` the sync pass
    whose download it is and ``pass_run`` that pass's run where an intake job
    still names it (R-1499); all three are None for a download neither queued.
    ``verb`` is the handler that downloaded it, and ``tracks`` how many of its
    downloaded tracks the folder holds at the names they were downloaded
    under. A go's or a pass's download with none there is named only beside
    files no download names, when its pass has no landing proof, since its
    tail may have renamed them (:func:`beside`).
    """

    job_id: str
    run: str | None
    verb: str
    tracks: int
    pass_name: str | None = None
    pass_run: str | None = None

    def said(self) -> str:
        if self.run is not None:
            if self.tracks:
                return (
                    f"job {self.job_id} of the go under run {self.run}, with {self.tracks} "
                    f"track(s) no landing took"
                )
            return (
                f"job {self.job_id} of the go under run {self.run}, whose pass no landing "
                f"took, and whose tail may have renamed those tracks"
            )
        if self.pass_name is not None:
            if self.tracks:
                return (
                    f"job {self.job_id} of the sync pass {self.pass_name}, with "
                    f"{self.tracks} track(s) no landing took"
                )
            return (
                f"job {self.job_id} of the sync pass {self.pass_name}, which no landing "
                f"took, and whose tail may have renamed those tracks"
            )
        return (
            f"job {self.job_id} of {self.verb}, a download no go or sync pass queued, "
            f"with {self.tracks} track(s) no landing took"
        )

    def step(self, folder: Path) -> str:
        if self.run is not None:
            if not self.tracks:
                return (
                    f"if the tracks no download names are job {self.job_id}'s, renamed by "
                    f"its tail, take it on with: {continue_command(self.run)}, which runs "
                    f"its tail again, names the landing it reached, or refuses naming what "
                    f"else the folder holds"
                )
            return (
                f"take job {self.job_id} to its landing, or read the landing its tail "
                f"already reached and answer that, with: {continue_command(self.run)}; "
                f"it refuses, naming the tail by hand, while the folder holds anything else"
            )
        if self.pass_name is not None and self.pass_run is not None:
            command = pass_continue_command(self.pass_run)
            if not self.tracks:
                return (
                    f"if the tracks no download names are the sync pass "
                    f"{self.pass_name}'s, renamed by its tail, take that pass to its "
                    f"landing with: {command}; it refuses while the folder holds "
                    f"anything else"
                )
            return (
                f"take the sync pass {self.pass_name} to its landing with: {command}; "
                f"it refuses while the folder holds anything else"
            )
        # MOVED OUT FIRST (review round one): ``intake land`` over the folder
        # takes the whole of it, the batch's own tracks with these.
        return (
            f"move the tracks of job {self.job_id} out of {folder}, and land them on "
            f"their own as any intake lands"
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "job": self.job_id,
            "run": self.run,
            "verb": self.verb,
            "tracks": self.tracks,
            "pass": self.pass_name,
            "pass_run": self.pass_run,
        }


@dataclass(frozen=True, slots=True)
class Beside:
    """What the staging folder holds that a landing would take with a batch's own.

    ``waiting`` names the downloads it can be put down to, and ``unnamed``
    every file there that no download names. Empty when the folder holds
    nothing but the batch's own tracks.
    """

    folder: Path
    waiting: tuple[Waiting, ...] = ()
    unnamed: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return bool(self.waiting or self.unnamed)

    def said(self) -> str:
        parts = [one.said() for one in self.waiting]
        if self.unnamed:
            parts.append(
                f"{len(self.unnamed)} track(s) no download names, "
                + ", ".join(self.unnamed[:UNNAMED_SHOWN])
                + (", and more" if len(self.unnamed) > UNNAMED_SHOWN else "")
            )
        return "; ".join(parts)

    def steps(self) -> tuple[str, ...]:
        steps = [one.step(self.folder) for one in self.waiting]
        if self.unnamed:
            steps.append(
                f"move the track(s) no download names out of {self.folder}, and land "
                f"them on their own"
            )
        return tuple(steps)

    def to_json(self) -> dict[str, Any]:
        return {
            "folder": str(self.folder),
            "waiting": [one.to_json() for one in self.waiting],
            "unnamed": list(self.unnamed),
        }


def beside(
    cfg: config.Config,
    store: jobs.JobStore,
    staging: Path,
    own: Collection[str],
    *,
    kept: frozenset[Identity] = frozenset(),
    own_pass: str | None = None,
    origin: tuple[str, ...],
    again: str,
) -> Beside:
    """What a landing of ``staging`` would take beside ``own``'s downloads.

    WHAT A LANDING TAKES IS THE FOLDER, read as the landing reads it. A file
    there that is one of ``own``'s downloaded tracks, at the name it was
    downloaded under, is the batch's own. EVERY OTHER FILE IS BESIDE IT,
    whoever put it there, since the landing would file it under the batch's
    manifest and pass.

    ``kept`` is what the batch's own tail left in the folder when it stopped
    (:func:`keep`): a file no download names is read as its own only when it
    is one of those, by name, size and modification time, so a file put there
    since is still beside it. NOT WHEN ``own_pass`` LANDED: a pass with a
    landing proof has had its tracks taken out of the folder, so nothing there
    is read as its own by that record.

    NAMING, NOT DECIDING, IS WHAT THE LANDING PROOF IS FOR. A file no download
    names is put down to every go's or sync pass's download with a track
    recorded in the folder, none of them there, whose pass has no landing
    proof on either medium (:func:`cratekit.intake.land_cli.pass_landed`),
    since its tail may have renamed them; a pass that landed is not named. A
    library root or a session log the proof cannot read refuses.

    A folder that is not there holds nothing a landing could take; one that
    cannot be listed refuses, never reads as empty, under ``origin`` and with
    ``again`` as its last step.
    """
    folder = resolved(staging)
    try:
        held = {resolved(path) for path in folder_listing(folder)} if folder.is_dir() else set()
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed ({exc}), so whether it "
            f"holds a download no landing took cannot be read; nothing was queued or run",
            steps=(f"make {folder} readable, {again}",),
            origin=origin,
            detail={"folder": str(folder)},
        ) from exc
    downloads: dict[str, tuple[jobs.Job, list[Path]]] = {}
    for job in jobs.list_jobs(store):
        inside = [path for path in _artifacts(store, job.job_id) if path.parent == folder]
        if inside:
            downloads[job.job_id] = (job, inside)
    mine = [path for job_id in own for path in downloads.get(job_id, (None, []))[1]]
    others = held - set(mine)
    if not others:
        return Beside(folder=folder)
    runs: dict[str, str] | None = None

    def run_of_pass(name: str | None) -> str | None:
        nonlocal runs
        if name is None:
            return None
        if runs is None:
            runs = _pass_runs(store, cfg.library.volume_id)
        return runs.get(name)

    found: list[Waiting] = []
    named: set[Path] = set()
    for job_id, (job, paths) in downloads.items():
        if job_id in own:
            continue
        present = [path for path in paths if path in others]
        if present:
            named.update(present)
            name = pass_of(job)
            found.append(
                Waiting(
                    job_id=job_id,
                    run=origin_run(job),
                    verb=job.handler_key,
                    tracks=len(present),
                    pass_name=name,
                    pass_run=run_of_pass(name),
                )
            )
    unnamed = sorted(others - named)
    if unnamed and kept and not (own_pass and land_cli.pass_landed(cfg, own_pass)):
        unnamed = [path for path in unnamed if identity(path) not in kept]
    if unnamed:
        proven: dict[str, bool] = {}
        for job_id, (job, paths) in downloads.items():
            run = origin_run(job)
            name = pass_of(job) if run is None else None
            if job_id in own or (run is None and name is None):
                continue
            if any(path in others for path in paths):
                continue
            proof = (
                default_name(str((job.payload or {}).get(RUN_KEY) or run))
                if run is not None
                else name
            )
            if proof not in proven:
                proven[proof] = land_cli.pass_landed(cfg, proof)
            if not proven[proof]:
                found.append(
                    Waiting(
                        job_id=job_id,
                        run=run,
                        verb=job.handler_key,
                        tracks=0,
                        pass_name=name,
                        pass_run=run_of_pass(name),
                    )
                )
    return Beside(
        folder=folder, waiting=tuple(found), unnamed=tuple(path.name for path in unnamed)
    )


@dataclass(frozen=True, slots=True)
class Settled:
    """What the folder holds as a batch's tail starts, to tell what arrives during it.

    ``items`` is every finished item of every download but the batch's own
    whose recorded artifact is in the folder, by job and item, and ``count``
    how many files a landing of the folder would take. The tail's steps tag,
    analyse and rename in place and add no file, so neither moves while the
    tail runs unless something else put a file there.
    """

    items: frozenset[tuple[str, str]]
    count: int


def settled(store: jobs.JobStore, staging: Path, own: Collection[str]) -> Settled:
    """What :class:`Settled` says of ``staging`` now, ``own``'s downloads left out (R-1499)."""
    folder = resolved(staging)
    items = frozenset(
        (job.job_id, item.item_id)
        for job in jobs.list_jobs(store)
        if job.job_id not in own
        for item in jobs.items(store, job.job_id)
        if item.state is jobs.ItemState.DONE
        and item.artifact
        and resolved(item.artifact).parent == folder
    )
    count = len(folder_listing(folder)) if folder.is_dir() else 0
    return Settled(items=items, count=count)


def arrived(
    store: jobs.JobStore,
    staging: Path,
    own: Collection[str],
    before: Settled,
    *,
    origin: tuple[str, ...],
    batch: str,
    land_command: str,
) -> CratekitError | None:
    """The refusal for what arrived in the folder while a batch's tail ran, or None (R-1499).

    THE READING BEFORE THE TAIL CANNOT SEE WHAT ARRIVES DURING IT. A download
    another process drives settles into the folder while the tail runs, the
    tail's ``name apply`` renames it with the batch's own, and from then on
    nothing tells the two apart by name: the landing would take it under the
    batch's pass and the tail's record would keep it as the batch's own. So a
    finished item of another download in the folder that was not there as
    the tail started, or a change in how many files a landing would take,
    refuses before the landing is planned, and the caller keeps no record.
    The way on is to move what arrived out and land the batch's own by hand,
    since its tail ran over them. A folder that cannot be read refuses too.
    """
    folder = resolved(staging)
    try:
        after = settled(store, staging, own)
    except OSError as exc:
        return refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed again after {batch}'s "
            f"tail ({exc}), so whether anything arrived during it cannot be read; the "
            f"landing was not planned",
            steps=(f"make {folder} readable, then land {batch} with: {land_command}",),
            origin=origin,
            detail={"folder": str(folder)},
        )
    new = sorted({job_id for job_id, _item in after.items - before.items})
    if not new and after.count == before.count:
        return None
    said = []
    if new:
        said.append(f"download job(s) {', '.join(new)} finished track(s) into it")
    if after.count != before.count:
        said.append(
            f"it held {before.count} file(s) a landing would take as the tail started "
            f"and holds {after.count} now"
        )
    return refuse(
        "refused-by-policy",
        f"while {batch}'s tail ran, the staging folder {folder} changed: "
        + "; ".join(said)
        + "; the tail's name apply may have renamed what arrived with the batch's own, "
        "so the landing was not planned and the tail's record was not kept",
        steps=(
            f"move what arrived out of {folder}, reading each file's tags, since name "
            f"apply may have renamed it",
            f"then land {batch}'s own tracks, which its tail tagged and named, with: "
            f"{land_command}",
        ),
        origin=origin,
        detail={
            "folder": str(folder),
            "arrived": new,
            "before": before.count,
            "after": after.count,
        },
    )


__all__ = [
    "DOWNLOAD_KEY",
    "ORIGIN_KEY",
    "PASS_TAILS_DIRNAME",
    "RUN_KEY",
    "Settled",
    "TAILS_DIRNAME",
    "UNNAMED_SHOWN",
    "Beside",
    "arrived",
    "Identity",
    "Waiting",
    "beside",
    "continue_command",
    "go_record",
    "identity",
    "keep",
    "kept",
    "origin_run",
    "pass_continue_command",
    "pass_name",
    "pass_of",
    "pass_record",
    "resolved",
    "settled",
]
