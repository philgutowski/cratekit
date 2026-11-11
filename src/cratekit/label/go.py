"""``label sync``'s go: one summary over every saved answer, one gate, one download.

U108, the second half of the guided label sync brainstormed with the author on
2026-10-02 (``docs/ideation/2026-10-02-guided-label-sync.md``). U107 asks label
by label and saves each answer as it is given. This module turns the answers
saved since the last go into ONE summary, asks ONE explicit gate over its
digest, and on ``apply`` downloads unattended, paced and resumable, leaving the
batch for the acquisition tail to land the way any intake lands. It is reached
two ways, at the end of the interactive walk once every label is answered, and
by ``label sync --go`` over answers already saved.

WHAT IS SUMMARISED IS THE ANSWERS, NOT THE REVIEW QUEUE. An answer saved and
not yet gone carries no :data:`SETTLED` marker. Only the releases an ``all`` or
a ``pick`` took are downloaded, and only while their review item is still
ACCEPTED: a release a person accepted by hand in review, which no answer took,
is never downloaded by the go, and one a person cleared after answering is
named and left. Nothing is downloaded that the author did not answer for. A
``not-now`` and a ``stop`` are counted in the summary and settled by the go
like any other answer, so each is counted once.

THE SIZE AND THE TIME ARE ESTIMATES, AND SAY SO. The size is what U107 recorded
when it asked: each track's duration from the provider's own rows at
``sync_cli.BYTES_PER_SECOND``, 110,000 bytes a second, which is a 16 bit 44.1
kHz FLAC averaged on dance music, with a track whose row carries no duration
counted at ``sync_cli.SECONDS_PER_TRACK``. The time is the configured pacing
delay for every track plus that size at :data:`TRANSFER_BYTES_PER_SECOND`.
Neither figure was measured against a real download on this tree. The live
sitting the brief owes is where the first comparison is taken.

THE DOWNLOAD IS ``acquire download``'s OWN JOB. The answered releases are listed
down ``label approved``'s path, :func:`cratekit.label.approved_cli.list_releases`,
which holds a release the genre gate holds, offers a track the library holds in
another version to the match queue rather than listing it, and writes the list
and its manifest through the one emitter. The list is then queued through
:func:`cratekit.acquire.cli.queue_list`, one item per track, and driven here.
A run stopped part way is resumed by ``label sync --go`` again, by ``acquire
download --job``, or by ``job resume``, and claims only the items still to run;
whichever finished it, ``--go`` under the go's own run then lands it (U239).

A SECOND START NEVER ASKS FOR A TRACK TWICE. Every job a go queues carries
:data:`ORIGIN_KEY`, and a track that is an item of one, done or still to run, is
passed to the listing as already held. The job store is that record and the
sync record is not, so a go killed between queueing its job and settling its
answers cannot queue the same tracks again on the next start.

A GO RESUMES WHAT AN EARLIER GO LEFT UNFINISHED, AND THEN ONLY THAT. A job
still open, stopped by a signal, or ended half failed with a retryable cause is
in the summary and in its digest, so the gate's answer covers resuming it, and
a go that has one queues nothing new: one job, one manifest and one landing per
go, because ``intake land`` lands a whole folder and two batches in it would
land as one. The answers saved since wait for the next go.

PLANNED, QUEUED AND SETTLED UNDER THE RECORD'S LOCK, which blocks, so a second
go started beside the first waits, finds the job the first one queued, and
refuses as stale rather than list the same tracks into a second job.

PACED THROUGH THE PROVIDER GATE BY THE WORKER. The download worker builds its
adapter through the registry and every provider call passes the shared gate. A
breaker that trips raises ``Parked``, the engine parks the job with its item
released, and this verb exits blocked with the cause rather than retry in a
loop. The go lists no label, so no sweep runs beside it.

LANDS LIKE ANY INTAKE. The manifest's rows say ``label``, which is what ``intake
land --manifest`` files under the Record Labels tree. The job carries the go's
run as its intake run (R29), and the report names the acquisition tail ending in
the landing under the batch name that run gives, so the batch playlist and the
tree are what a label landing produces today.

AND THE TAIL IS RUN, NOT ONLY NAMED, SINCE U190. The attended Defected sync of
2026-10-31 downloaded ten tracks and was then handed five commands to type. The
go cannot run them itself: this module is ranked a feature module and the
dispatcher is the CLI layer's. So the report carries :data:`LAND_KEY`, the
absolute staging folder, the manifest and the pass, and ``label.sync``'s CLI
module (:mod:`cratekit.cli.label_sync`) hands it to the chain ``sync land``
runs, :mod:`cratekit.cli.tail`, which ends at the landing's gate. It is set only
when the go's one download settled with a track done (R-1115, below): a go that declined,
listed nothing, downloaded nothing or is still downloading names no tail, and
neither does a resume over more than one earlier job, whose manifests one
landing of one folder cannot both carry. Then the commands are printed as before.

A TRACK REFUSED FOR GOOD IS NAMED AND SKIPPED, AND THE REST IS LANDED (R-1115).
The go reads its settled download through
:func:`cratekit.acquire.cli.read_download`, the one reading ``sync land`` uses:
a job that succeeded, or that ended FAILED only by tracks no retry can clear,
landed what it downloaded. ``drive_queued`` refuses for every FAILED job, so the
go reads the job back off the queue when it does and carries on over one that
reading calls settled; a transient failure, a park and a cancel still end the
go on the job's own refusal. Each refused track is named on the ``downloaded``
check and under ``refused`` in the report, a declined one by the worker's own
warning and a failed one by :data:`REFUSED_WARNING`. A go whose every track was
refused runs no tail and names none, since there is nothing in the folder to land.

A GO UNDER ITS OWN RUN TAKES ITS OWN DOWNLOAD ON, ASKING NOTHING (U239). The
attended label pass of 2026-11-10 stopped at the provider call ceiling part
way, finished its job with the ``job resume`` the refusal named, and then ran
``--go`` under the same run, which refused ``decision-stale`` over an empty
plan: the answers were settled and the job had succeeded, so nothing was left
to summarise, and the tail never ran. Now a ``--go`` under a run whose go
queued a job, with ``apply`` recorded, resumes that job if it is unfinished,
reads it once it has settled by whatever path, and names its landing, so the
tail runs and stops at the landing's gate with no new decision. A cancelled job
is not taken on and the gate refuses as before. A go job queued after it into
the same folder refuses the tail, with the commands, since the landing would
take both batches as one; and a run whose tail already reached its landing
names that landing and runs nothing (:data:`LANDING_ROLE`). The ceiling's own
continue command names that ``--go`` rather than the job, and every other stop
a go can take on adds it as a step (:func:`_carried`).

A GO NEVER LANDS ANOTHER DOWNLOAD AS ITS OWN (R-1467). Every download stages
into the one folder, and ``intake land`` lands the whole of it, so a fresh go
queued beside an earlier go's download that was never landed, or beside a
plain ``acquire download``, landed both as one batch under its own manifest and
pass, filing the other's tracks under no label. :func:`beside` reads what a
landing of the folder would take: anything there that is not one of the go's
own tracks at the name it was downloaded under is beside it, whoever put it
there, another download's track or a file no download names (a tail's ``name
apply`` renames every track before the landing's gate). A fresh go with
anything beside it refuses before its gate, naming each download it can put
the files down to (a go's by its pass, when no landing proof of that pass
exists on either medium, :func:`cratekit.intake.land_cli.pass_landed`), so a
go with nothing new to take names it too rather than ask over an empty plan;
and every tail, a fresh go's after its drive, a resume's and a run's own,
refuses beside it, with the landing in its detail. A run's own go reads files
no download names as its own tracks only when its tail already ran
(:func:`tail_role`), and never more of them than it renamed. A folder or a
library root that cannot be read refuses rather than reads as nothing beside.
"""

from __future__ import annotations

import dataclasses
import shlex
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import download
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, provider_gate, review
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Verdict
from cratekit.intake import land_cli
from cratekit.intake.land_cli import default_name
from cratekit.intake.landing import listing as folder_listing
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import approved_cli, sync_cli
from cratekit.label import gate as genre_gate

#: The one gate, declared on the ``label.sync`` registry entry.
GATE = "label.sync.confirm"
#: The gate's answer that starts a download.
APPLY = "apply"
#: The prefix of the role a go's run records the landing its tail stopped at
#: under (U239), in :attr:`cratekit.cli.gates.RunState.related_runs`, one role
#: per job (:func:`landing_role`). Written by the CLI layer, which runs the tail,
#: on the run whose go queued the job, and read here, so a later go under that
#: run names that landing rather than run the tail a second time.
LANDING_ROLE = "landing"
#: The prefix of the role a go's run records that its tail started under
#: (R-1467), one per job (:func:`tail_role`), written by the CLI layer.
TAIL_ROLE = "tail"
#: The verb whose job the go queues. Its worker downloads; the go composes.
DOWNLOAD = "acquire.download"
#: The payload key a go's download job carries, naming the run and the manifest.
ORIGIN_KEY = "label_sync"
#: The payload key ``sync all`` already uses for a job's intake run (R29).
RUN_KEY = "run_id"
#: The report's key naming the tail the CLI layer runs after a download (U190).
LAND_KEY = "land"
#: The warning a go names each track its download FAILED for good under (R-1115).
#: A track the worker declined is named by its own ``acquire-refused`` warning.
REFUSED_WARNING = "label-sync-download-refused"
#: What every list a go writes is named after, before the digest.
LIST_PREFIX = "label-sync"
#: The marker an answer carries once a go has taken it.
SETTLED = sync_cli.SETTLED
#: The transfer rate the time estimate assumes, 20 megabits a second. An
#: assumption, not a measurement; see the module docstring.
TRANSFER_BYTES_PER_SECOND = 2_500_000
#: The answers that take releases.
TAKING = frozenset({sync_cli.ALL, sync_cli.PICK})
#: The ways a release can fail to be read that waiting mends. An answer holding
#: one stays unsettled, so the next go asks for it again; a release that is
#: gone, or names nothing, stays that way and is not carried for ever.
RETRY_KINDS = frozenset({approved_cli.PROVIDER, approved_cli.NOT_ASKED})


# ---------------------------------------------------------------------------
# What the answers hold
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Taken:
    """One release an answer took, as the question measured it."""

    label_id: str
    label_name: str
    identity: str
    item_id: str
    artist: str
    title: str
    year: str
    tracks: int | None
    size: int | None

    def to_json(self) -> dict[str, Any]:
        return {
            "label_id": self.label_id,
            "label": self.label_name,
            "release": self.identity,
            "artist": self.artist,
            "title": self.title,
            "year": self.year,
            "tracks": self.tracks,
        }


@dataclass(frozen=True, slots=True)
class Held:
    """The download jobs earlier goes queued: those to resume, and every track held.

    ``resume`` pairs each job a go would resume with how many of its tracks
    are still to run.
    """

    resume: tuple[tuple[jobs.Job, int], ...]
    tracks: frozenset[str]


def resumable(job: jobs.Job, left: int) -> bool:
    """Whether a go resumes this job: open, or stopped with tracks a retry re-arms.

    A job a signal CANCELLED or that ended FAILED with a retryable cause is
    work a go started and did not finish, so it is resumed as an open one is,
    through ``jobs.retry``, which keeps every downloaded track done. One whose
    cause says no retry can succeed is not, and its failed tracks are not held.
    """
    if job.is_open():
        return True
    if job.state is jobs.JobState.SUCCEEDED or not left:
        return False
    return job.cause is None or job.cause.retryable


def held_by_goes(store: jobs.JobStore) -> Held:
    """Every track a go's job holds, done or still to run, and the jobs to resume.

    A track of a job a go RESUMES is held unless it was skipped, since the
    resume claims it. A track of any other go job is held only when it was
    downloaded: a failed one that cannot be retried never landed, so a later
    go may ask for it again.
    """
    resume: list[tuple[jobs.Job, int]] = []
    tracks: set[str] = set()
    for job in jobs.list_jobs(store):
        if job.handler_key != DOWNLOAD or not isinstance(
            (job.payload or {}).get(ORIGIN_KEY), Mapping
        ):
            continue
        items = jobs.items(store, job.job_id)
        left = sum(
            1 for item in items if item.state not in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)
        )
        again = resumable(job, left)
        if again:
            resume.append((job, left))
        for item in items:
            if item.state is jobs.ItemState.DONE or (
                again and item.state is not jobs.ItemState.SKIPPED
            ):
                tracks.add(item.item_id)
    return Held(resume=tuple(resume), tracks=frozenset(tracks))


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _taken_by(entry: Mapping[str, Any]) -> list[Taken]:
    """The releases one saved answer took, from what it recorded about each.

    The answer records every taken release whole, so the summary reads its
    measured tracks and size without asking the provider anything. An answer
    that names a taken identity it did not record whole is still taken, with
    its counts unknown, never dropped.
    """
    label_id = _text(entry.get("label_id"))
    label_name = _text(entry.get("label_name")) or label_id
    recorded = {
        one.identity: one
        for one in (
            sync_cli.Offered.from_json(raw)
            for raw in (entry.get("releases") if isinstance(entry.get("releases"), list) else ())
            if isinstance(raw, Mapping)
        )
        if one.identity
    }
    named = entry.get("taken")
    identities = [str(one) for one in named if isinstance(one, str) and one] if isinstance(
        named, list
    ) else list(recorded)
    found: list[Taken] = []
    for identity in identities:
        one = recorded.get(identity)
        found.append(
            Taken(
                label_id=label_id,
                label_name=label_name,
                identity=identity,
                item_id=(one.item_id if one is not None and one.item_id else None)
                or genre_gate.release_item_id(identity),
                artist=one.artist if one is not None else "",
                title=one.title if one is not None else "",
                year=one.year if one is not None else "",
                tracks=one.tracks if one is not None else None,
                size=one.size if one is not None else None,
            )
        )
    return found


@dataclass(frozen=True, slots=True)
class Summary:
    """Everything the gate is asked over, and the numbers a person judges it by."""

    #: The saved answers this summary covers, as ``(index, label, answered_at)``.
    answers: tuple[tuple[int, str, str], ...]
    taken: tuple[Taken, ...]
    taking: tuple[str, ...]
    not_now: tuple[str, ...]
    stopped: tuple[str, ...]
    #: Jobs an earlier go left unfinished, as ``(job_id, tracks still to run)``.
    #: A go with any resumes them and queues nothing new: one job, one
    #: manifest and one landing per go.
    open_jobs: tuple[tuple[str, int], ...]
    pace_s: float

    @property
    def tracks(self) -> int:
        return sum(one.tracks or 0 for one in self.taken)

    @property
    def size(self) -> int:
        return sum(one.size or 0 for one in self.taken)

    @property
    def unknown(self) -> int:
        """Releases whose tracks were unread when asked, so the counts leave them out."""
        return sum(1 for one in self.taken if one.tracks is None)

    @property
    def seconds(self) -> int:
        return round(self.tracks * self.pace_s + self.size / TRANSFER_BYTES_PER_SECOND)

    def plan(self) -> dict[str, Any]:
        """The plan the gate shows and the digest its decision is recorded against.

        THE DIGEST IS OVER WHAT THE ANSWER DECIDES: every release to download
        by label, the labels counted not now and stop, and the open jobs a go
        would resume. Not over a job's progress, which moves while a decision
        waits without changing what was decided.
        """
        items: list[dict[str, Any]] = [one.to_json() for one in self.taken]
        items.extend({"resume": job_id, "tracks_left": left} for job_id, left in self.open_jobs)
        return {
            "digest": digest_of(
                {
                    "kind": GATE,
                    "releases": [[one.label_id, one.identity] for one in self.taken],
                    "not_now": list(self.not_now),
                    "stopped": list(self.stopped),
                    "resume": [job_id for job_id, _left in self.open_jobs],
                }
            ),
            "items": items,
        }

    def facts(self) -> dict[str, Any]:
        """The summary's numbers, in the order a person reads them."""
        facts: dict[str, Any] = {
            "labels_taking_releases": len(self.taking),
            "releases": len(self.taken),
            "tracks": self.tracks,
            "estimated_size": sync_cli.size_text(self.size),
            "estimated_time": duration_text(self.seconds),
            "labels_answered_not_now": len(self.not_now),
            "labels_answered_stop_following": len(self.stopped),
        }
        if self.unknown:
            facts["releases_with_tracks_unread"] = self.unknown
        if self.open_jobs:
            facts["earlier_downloads_to_resume"] = len(self.open_jobs)
            facts["this_go"] = (
                "resumes the earlier download only, so it lands as one batch; the "
                "answers above wait for the next go"
            )
        return facts

    def to_json(self) -> dict[str, Any]:
        return {
            "answers": len(self.answers),
            "labels": list(self.taking),
            "releases": len(self.taken),
            "tracks": self.tracks,
            "size": self.size,
            "seconds": self.seconds,
            "unknown": self.unknown,
            "not_now": list(self.not_now),
            "stopped": list(self.stopped),
            "resume": [job_id for job_id, _left in self.open_jobs],
        }


def duration_text(seconds: int) -> str:
    """An estimate a person reads: minutes, hours and minutes past one hour."""
    minutes = max(0, round(seconds / 60))
    if minutes < 60:
        return f"about {minutes} min"
    return f"about {minutes // 60} h {minutes % 60} min"


def pace_of(cfg: config.Config) -> float:
    """The pacing delay a download waits before every track, as configured."""
    configured = cfg.acquisition.pacing_delay_s
    return float(configured) if configured is not None else download.DEFAULT_BASE_DELAY_S


def summarise(document: Mapping[str, Any], held: Held, cfg) -> Summary:
    """One summary over every saved answer no go has taken yet.

    A release two answers took is downloaded once and counted once, under the
    first answer that took it.
    """
    answers: list[tuple[int, str, str]] = []
    taken: dict[str, Taken] = {}
    taking: dict[str, None] = {}
    not_now: dict[str, None] = {}
    stopped: dict[str, None] = {}
    for index, entry in sync_cli.unsettled(document):
        label_id = _text(entry.get("label_id"))
        name = _text(entry.get("label_name")) or label_id
        answers.append((index, label_id, _text(entry.get("answered_at"))))
        word = entry.get("answer")
        if word in TAKING:
            releases = _taken_by(entry)
            for one in releases:
                taken.setdefault(one.identity, one)
            if releases:
                taking.setdefault(name)
        elif word == sync_cli.NOT_NOW:
            not_now.setdefault(name)
        elif word == sync_cli.STOP:
            stopped.setdefault(name)
    open_jobs = tuple((job.job_id, left) for job, left in held.resume)
    return Summary(
        answers=tuple(answers),
        taken=tuple(taken.values()),
        taking=tuple(taking),
        not_now=tuple(not_now),
        stopped=tuple(stopped),
        open_jobs=open_jobs,
        pace_s=pace_of(cfg),
    )


# ---------------------------------------------------------------------------
# The gate and the go
# ---------------------------------------------------------------------------


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.sync.go.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _gate(ctx):
    """The declared gate the go is asked through, or a refusal naming the defect.

    Refuses rather than defaulting, for ``tag retag``'s reason: a go that
    quietly skipped its question because a registry edit dropped the gate
    would download with nobody asked.
    """
    for spec in ctx.entry.gates:
        if spec.name == GATE:
            return spec
    raise refuse(
        "refused-by-policy",
        f"the label sync's registry entry declares no {GATE} gate, so there is "
        f"nobody to ask before downloading and nothing is downloaded",
        remedy=Remedy.REPORT_DEFECT,
        origin=("label.go",),
    )


def _summary_line(summary: Summary) -> str:
    facts = summary.facts()
    said = (
        f"{facts['labels_taking_releases']} label(s) taking {facts['releases']} "
        f"release(s), {facts['tracks']} track(s), {facts['estimated_size']}, "
        f"{facts['estimated_time']}; {facts['labels_answered_not_now']} label(s) "
        f"answered not now and {facts['labels_answered_stop_following']} stop following"
    )
    if summary.unknown:
        said += f"; {summary.unknown} release(s) with tracks unread when asked"
    if summary.open_jobs:
        said += f"; {len(summary.open_jobs)} earlier download(s) to resume"
    return said


def tail(staging: Path, manifest: str, run_id: str) -> list[str]:
    """The acquisition tail that lands what a go downloaded, as any intake lands.

    THE LANDING NAMES ITS OWN BATCH (U110). The go's run is handed as the pass,
    which names the intake file ``label mark --xml`` reads on the bridge and is
    the name ``label mark --pass`` takes on a native intake tree (R-1056), and
    no ``--name``, so the batch folder and its INBOX playlist take the
    landing's date and the label the manifest names rather than the run's
    identifier.
    """
    folder = str(staging)
    return [
        shlex.join(["crate", "tag", "folder", folder]),
        shlex.join(["crate", "analyze", "run", folder]),
        shlex.join(["crate", "analyze", "restamp", folder]),
        shlex.join(["crate", "name", "apply", "--root", folder]),
        shlex.join(
            ["crate", "intake", "land", folder, "--manifest", manifest, "--pass", default_name(run_id)]
        ),
    ]


def landing(staging: Path, manifest: str, run_id: str, job_id: str) -> dict[str, str]:
    """What the tail and the landing run over: the folder, the manifest and the pass.

    The same three the last command :func:`tail` names, as data, so the chain
    that runs them reads no command line back. With them the go's run and its
    job (U239), so the landing the tail reaches is recorded on the run whose
    go queued that job, under that job, whichever run drove it.
    """
    return {
        "folder": str(staging),
        "manifest": manifest,
        "pass": default_name(run_id),
        "run": run_id,
        "job": job_id,
    }


def landing_role(job_id: str) -> str:
    """The role a landing the tail reached for ``job_id`` is recorded under (U239).

    One role per job, so a landing recorded for one download never answers for
    another one under the same run.
    """
    return f"{LANDING_ROLE}.{job_id}"


def _drive(
    ctx, store: jobs.JobStore, job_id: str
) -> tuple[jobs.Job, list[dict[str, str]], acquire_cli.DownloadRead]:
    """Drive one go's download, and read how it settled (R-1115).

    ``drive_queued`` refuses for every job that did not end clean, and the
    engine raises inside the drive when every attempted item failed. Either
    refusal is re-raised unchanged UNLESS the job, read back off the queue,
    ended FAILED only by tracks refused for good, which is a download that
    landed what it landed. Its warnings are then the declined tracks' alone,
    read off the item rows, since the drive's own went with the refusal.

    A refusal that is re-raised names how the download reaches its landing
    afterwards, through :func:`_carried` (U239).
    """
    try:
        job, said = acquire_cli.drive_queued(ctx, store, job_id)
    except CratekitError as exc:
        job = jobs.get(store, job_id)
        read = acquire_cli.read_download(store, job)
        if not read.settled:
            carried = _carried(exc, store, job)
            if carried is exc:
                raise
            raise carried from None
        said = acquire_cli.declined_warnings(store, job)
    else:
        read = acquire_cli.read_download(store, job)
    warnings = [*said]
    reasons = {str(row["item_id"]): row for row in read.refused}
    for item_id in read.failed:
        row = reasons[item_id]
        warnings.append(
            {
                "code": REFUSED_WARNING,
                "message": (
                    f"{acquire_cli.track_name(job, item_id)} ({item_id}) failed for good "
                    f"and is skipped ({row['reason']}): {row['message']}"
                ),
            }
        )
    return job, warnings, read


def _downloaded(read: acquire_cli.DownloadRead, listed: int) -> str:
    """How a download ended, in words: its state, its count, and each refused track."""
    said = f"{read.job.state}, {read.done} of {listed} track(s) downloaded"
    if read.refused:
        said += f"; {len(read.refused)} refused for good and skipped: " + ", ".join(
            f"{row['item_id']} ({row['reason']})" for row in read.refused
        )
    if read.settled and not read.done:
        said += "; every track was refused for good, so no tail was run" if read.refused else (
            "; nothing landed, so no tail was run"
        )
    return said


def go(
    ctx,
    cfg: config.Config,
    *,
    walk: Sequence[str] | None = None,
    data: Mapping[str, Any] | None = None,
    wrote: bool = False,
) -> Envelope:
    """Show the summary, ask the gate, and on apply download what was answered for.

    Under the run of a go that already started a download, take that download
    on instead, asking nothing (:func:`_carry_on`, U239).

    ``walk`` is what the interactive walk did before it reached the gate, one
    line per label, carried in front of the summary so a person deciding sees
    what they just answered. ``data`` is the walk's own report, which the
    envelope keeps beside the go's, and ``wrote`` says the walk already wrote,
    so a run that answered and then declined is not reported as a no-op.
    """
    spec = _gate(ctx)
    run_id = ctx.run.run_id
    document = sync_cli.load_record(cfg)
    with jobs.open_store() as store:
        summary = summarise(document, held_by_goes(store), cfg)
    # ABSOLUTE, as ``sync land`` takes it: a relative root resolves against the
    # working directory, and the tail named over it once planned nothing (U169).
    staging = Path(cfg.paths.download_staging).expanduser().absolute()
    own = _own(ctx)
    if own is not None:
        # THIS RUN'S GO ALREADY STARTED A DOWNLOAD (U239), so its recorded
        # decision is the one that download runs under: taken on, not asked again.
        base = dict(data or {})
        return _carry_on(
            ctx,
            cfg,
            own,
            summary,
            staging,
            list(base.pop("checks", [])),
            dict(base.pop("summary", {}) or {}),
            wrote=wrote,
        )
    # NOTHING IN THE FOLDER BUT WHAT THIS GO WOULD LAND (R-1467), read before
    # the gate so nobody decides a go that would land another download as its
    # own. The jobs this go would resume are its own batch.
    with jobs.open_store() as store:
        found = beside(cfg, store, staging, {job_id for job_id, _left in summary.open_jobs})
    if found:
        raise _waiting_refusal(found, staging, walk)
    facts: dict[str, Any] = {}
    if walk is not None:
        facts["answered_this_run"] = list(walk)
    facts.update(summary.facts())
    facts["after_deciding"] = shlex.join(["crate", "--run", run_id, "label", "sync", "--go"])
    option = ctx.gate.require(spec, plan=summary.plan(), context=facts)

    base = dict(data or {})
    checks: list[dict[str, Any]] = list(base.pop("checks", []))
    report: dict[str, Any] = dict(base.pop("summary", {}) or {})
    checks.append(_check("summary", "info", _summary_line(summary)))
    if option == "abort":
        checks.append(
            _check(
                "declined",
                "ok",
                f"declined: nothing was downloaded, and the {len(summary.answers)} "
                f"answer(s) are kept for a later go: crate label sync --go",
            )
        )
        report["go"] = {**summary.to_json(), "declined": True, "job": None}
        return ctx.envelope(
            data={"checks": checks, "summary": report},
            outcome=Outcome.OK if wrote else Outcome.NO_OP,
        )

    if summary.open_jobs:
        return _resume(ctx, cfg, summary, staging, checks, report, wrote=wrote)

    warnings: list[dict[str, str]] = []
    withdrawn: list[Taken] = []
    listing = None
    queued: jobs.Job | None = None
    # PLANNED, QUEUED AND SETTLED UNDER THE RECORD'S LOCK, which blocks: a
    # second go waits here, then finds the job this one queued, so two goes
    # never list the same tracks into two jobs. The drive is outside it.
    with sync_cli.record_lock(cfg, "planning a go"):
        with jobs.open_store() as store:
            held = held_by_goes(store)
        if held.resume:
            raise refuse(
                "decision-stale",
                "another go queued a download while this one waited for the label "
                "sync record, so what was approved is no longer what would run; "
                "nothing was queued by this one",
                steps=("ask again with: crate label sync --go",),
                origin=("label.go",),
                detail={"queued": [job.job_id for job, _left in held.resume]},
            )
        releases: list[Any] = []
        if summary.taken:
            with review.open_store(cfg) as items:
                for one in summary.taken:
                    item = review.find(items, one.item_id)
                    if item is not None and item.verdict is Verdict.ACCEPTED:
                        releases.append(approved_cli.release_of(items, item))
                    else:
                        withdrawn.append(one)
        if releases:
            listing = approved_cli.list_releases(
                cfg,
                releases,
                out=lambda: staging / LISTS_DIR,
                handler_key=ctx.entry.handler_key,
                prefix=LIST_PREFIX,
                already=held.tracks,
                excuse=frozenset({approved_cli.GONE, approved_cli.NO_IDENTIFIER}),
                elsewhere="make the lists folder under download staging writable",
            )
            written = listing.written
            if written.list_path is not None:
                with jobs.open_store() as store:
                    queued = acquire_cli.queue_list(
                        store,
                        cfg,
                        written.list_path,
                        handler_key=DOWNLOAD,
                        extra={
                            ORIGIN_KEY: {"run": run_id, "manifest": str(written.manifest_path)},
                            RUN_KEY: run_id,
                        },
                    )
        # SETTLED AFTER THE QUEUE AND BEFORE THE DRIVE. A go killed before this
        # leaves its answers to the next go, which resumes the job and lists
        # nothing it holds; one killed after it leaves the job for the next go
        # to resume. An answer holding a release the provider did not answer
        # for is left unsettled, so the next go asks for that release again.
        retry = frozenset(
            failed.release.release_id
            for failed in (listing.failures if listing is not None else ())
            if failed.kind in RETRY_KINDS
        )
        document = sync_cli.load_record(cfg)
        settled = sync_cli.settle_in(
            document,
            summary.answers,
            marker={"run": run_id, "job": queued.job_id if queued is not None else None},
            keep=retry,
        )
        if settled:
            sync_cli.write_record(cfg, document)

    if withdrawn:
        checks.append(
            _check(
                "withdrawn",
                "info",
                f"{len(withdrawn)} release(s) an answer took are no longer accepted in "
                f"review and were not downloaded: "
                + ", ".join(f"{one.label_name} {one.identity}" for one in withdrawn),
            )
        )
    if listing is not None:
        checks.append(
            _check(
                "listed",
                "ok" if listing.listed else "info",
                f"{listing.listed} missing track(s) from {listing.passed} answered "
                f"release(s) listed to {listing.written.list_path}"
                if listing.listed
                else f"nothing to download: the library holds, or an earlier go already "
                f"holds, every track of the {listing.passed} answered release(s) the "
                f"genre gate passed",
            )
        )
        checks.append(
            _check(
                "held-by-a-go",
                "info",
                f"{listing.counts['queued']} track(s) an earlier go already holds, not "
                f"asked for again",
            )
        )
        checks.extend(approved_cli.listing_checks(listing, namespace="label.sync.go.list"))
    if retry:
        checks.append(
            _check(
                "carried",
                "fail",
                f"{len(retry)} release(s) could not be read, so the answer(s) holding "
                f"them are kept for the next go: crate label sync --go",
            )
        )
    checks.append(
        _check("settled", "info", f"{settled} answer(s) taken by this go; it asks about none of them again")
    )

    landed: list[str] = []
    land: dict[str, str] | None = None
    refused: list[dict[str, Any]] = []
    if queued is not None:
        with jobs.open_store() as store:
            queued, drifted, read = _drive(ctx, store, queued.job_id)
        warnings.extend(drifted)
        refused = list(read.refused)
        nothing = read.settled and not read.done
        checks.append(
            _check(
                "downloaded",
                "fail" if nothing and read.refused else "ok",
                f"job {queued.job_id}: {_downloaded(read, listing.listed)}",
            )
        )
        if not nothing:
            landed = tail(staging, str(listing.written.manifest_path), run_id)
        if read.landed:
            # A DOWNLOAD THAT FINISHED IN THE FOLDER WHILE THIS ONE DROVE (R-1467).
            with jobs.open_store() as store:
                _refuse_beside(
                    cfg, store, queued, staging, str(listing.written.manifest_path),
                    run_id, landed, own={queued.job_id}, refused=refused,
                )
            land = landing(staging, str(listing.written.manifest_path), run_id, queued.job_id)
        if land is None and landed:
            checks.append(_next_check(landed))
    report["go"] = {
        **summary.to_json(),
        "declined": False,
        "job": queued.job_id if queued is not None else None,
        "list": str(listing.written.list_path)
        if listing is not None and listing.written.list_path is not None
        else None,
        "manifest": str(listing.written.manifest_path)
        if listing is not None and listing.written.manifest_path is not None
        else None,
        "withdrawn": [one.identity for one in withdrawn],
        "carried": sorted(retry),
        "refused": refused,
        "next": landed,
        LAND_KEY: land,
    }
    return ctx.envelope(
        data={"checks": checks, "summary": report},
        outcome=Outcome.OK if queued is not None or settled or wrote else Outcome.NO_OP,
        warnings=tuple(warnings),
    )


def _next_check(landed: Sequence[str]) -> dict[str, Any]:
    return _check(
        "next",
        "info",
        "land it as any intake lands, in this order, before the next go adds to "
        "the same folder: " + "; then ".join(landed),
    )


def _resume(
    ctx,
    cfg: config.Config,
    summary: Summary,
    staging: Path,
    checks: list[dict[str, Any]],
    report: dict[str, Any],
    *,
    wrote: bool,
) -> Envelope:
    """Resume what earlier goes left unfinished, and queue nothing new.

    ONE JOB PER GO. A resumed job and a new one would download into the same
    staging folder under two manifests, and ``intake land`` lands a folder,
    so the first landing would take both batches under one name and file the
    other's tracks under no label. The answers saved since wait for the next
    go, which lists nothing the resumed job holds.
    """
    warnings: list[dict[str, str]] = []
    landed: list[str] = []
    resumed: list[str] = []
    refused: list[dict[str, Any]] = []
    lands: list[dict[str, str] | None] = []
    with jobs.open_store() as store:
        for job_id, _left in summary.open_jobs:
            job = jobs.get(store, job_id)
            if not job.is_open():
                # STOPPED BY A SIGNAL OR ENDED HALF FAILED: re-armed, with
                # every downloaded track left done.
                jobs.retry(store, job_id)
            job, drifted, read = _drive(ctx, store, job_id)
            warnings.extend(drifted)
            resumed.append(job_id)
            refused.extend(read.refused)
            nothing = read.settled and not read.done
            checks.append(
                _check(
                    f"resumed.{job_id}",
                    "fail" if nothing and read.refused else "ok",
                    f"resumed the earlier download {job_id}: "
                    f"{_downloaded(read, len(jobs.items(store, job_id)))}",
                )
            )
            payload = dict(job.payload or {})
            manifest = dict(payload.get(ORIGIN_KEY) or {}).get("manifest")
            if isinstance(manifest, str) and manifest and not nothing:
                run_of = str(payload.get(RUN_KEY) or ctx.run.run_id)
                landed.extend(tail(staging, manifest, run_of))
                lands.append(landing(staging, manifest, run_of, job_id) if read.landed else None)
            else:
                lands.append(None)
    # ONE EARLIER JOB, LANDED, IS RUN ON THROUGH THE TAIL. Several would need two
    # manifests on one landing of one folder, so their commands are printed.
    land = lands[0] if len(lands) == 1 else None
    if land is not None:
        # NOT BESIDE ANOTHER DOWNLOAD (R-1467), checked before the gate and
        # again here, once the resume has driven.
        with jobs.open_store() as store:
            _refuse_beside(
                cfg, store, jobs.get(store, land["job"]), staging, land["manifest"],
                land["run"], landed, own=set(resumed), refused=refused,
            )
    if summary.answers:
        checks.append(
            _check(
                "waiting",
                "info",
                f"{len(summary.answers)} answer(s) wait for the next go, once this "
                f"download is landed: crate label sync --go",
            )
        )
    if landed and land is None:
        checks.append(_next_check(landed))
    report["go"] = {
        **summary.to_json(),
        "declined": False,
        "job": None,
        "resumed": resumed,
        "list": None,
        "manifest": None,
        "withdrawn": [],
        "carried": [],
        "refused": refused,
        "next": landed,
        LAND_KEY: land,
    }
    return ctx.envelope(
        data={"checks": checks, "summary": report},
        outcome=Outcome.OK,
        warnings=tuple(warnings),
    )


def own_job(store: jobs.JobStore, run_id: str) -> jobs.Job | None:
    """The download job this run's go queued, or None when it queued none (U239).

    A go queues at most one job, and the job carries the run in its origin, so
    the job store is the record of it, as it is of every track a go holds.
    """
    for job in jobs.list_jobs(store):
        origin = (job.payload or {}).get(ORIGIN_KEY)
        if (
            job.handler_key == DOWNLOAD
            and isinstance(origin, Mapping)
            and origin.get("run") == run_id
        ):
            return job
    return None


def _own(ctx) -> str | None:
    """The job a go under this run takes on with no new decision, or None (U239).

    ONLY UNDER A RECORDED APPLY, and only a job this run's own go queued, so
    the decision taken on is the one that started that download. A CANCELLED
    job is not taken on: a cancel is a person's stop, so the go falls through
    to its gate, which refuses the moved plan and asks again.
    """
    recorded = ctx.gate.state.decisions.get(GATE)
    if recorded is None or recorded.option != APPLY:
        return None
    with jobs.open_store() as store:
        job = own_job(store, ctx.run.run_id)
    if job is None or job.state is jobs.JobState.CANCELLED:
        return None
    return job.job_id


def _beside(store: jobs.JobStore, job: jobs.Job) -> list[jobs.Job]:
    """The go jobs queued after ``job`` that hold downloaded tracks or are still open.

    Each downloads into the same staging folder, and ``intake land`` lands a
    whole folder, so a tail run now would land both batches as one. A job
    stamped the same instant is counted, since which came first cannot be
    told, and counting it refuses rather than mixes. Only later go jobs; an
    earlier one and a download no go queued are read by :func:`beside`, beside
    it (R-1467).
    """
    found: list[jobs.Job] = []
    for other in jobs.list_jobs(store):
        if other.job_id == job.job_id or other.created < job.created:
            continue
        if other.handler_key != DOWNLOAD or not isinstance(
            (other.payload or {}).get(ORIGIN_KEY), Mapping
        ):
            continue
        if other.is_open() or any(
            item.state is jobs.ItemState.DONE for item in jobs.items(store, other.job_id)
        ):
            found.append(other)
    return found


def _origin_run(job: jobs.Job) -> str | None:
    """The run whose go queued ``job``, off its origin, or None for another job."""
    origin = (job.payload or {}).get(ORIGIN_KEY)
    run = origin.get("run") if isinstance(origin, Mapping) else None
    return run if isinstance(run, str) and run else None


def continue_command(run_id: str) -> str:
    """The command that takes a go's download on to its landing (U239)."""
    return shlex.join(["crate", "--run", run_id, "label", "sync", "--go"])


def tail_role(job_id: str) -> str:
    """The role under which the run whose go queued ``job_id`` records that its tail started (R-1467).

    Written by the CLI layer just before it runs a go's tail, naming the run
    that runs it, on the run whose go queued the job, as :func:`landing_role`
    is. The tail's ``name apply`` renames every track before the landing's
    gate, so a later go under that run reads files no download names as ITS
    OWN tracks only when this is recorded (:func:`beside`).
    """
    return f"{TAIL_ROLE}.{job_id}"


#: How many of the files no download names a refusal lists by name.
UNNAMED_SHOWN = 8


@dataclass(frozen=True, slots=True)
class Waiting:
    """A download the staging folder may hold that no landing has taken (R-1467).

    ``run`` is the run whose go queued it, or None for a download no go
    queued, ``verb`` the handler that downloaded it, and ``tracks`` how many
    of its downloaded tracks the folder holds at the names they were
    downloaded under. A go's download with none there is named only beside
    files no download names, when its pass has no landing proof, since its
    tail may have renamed them (:func:`beside`).
    """

    job_id: str
    run: str | None
    verb: str
    tracks: int

    def said(self) -> str:
        if self.run is None:
            return (
                f"job {self.job_id} of {self.verb}, a download no go queued, with "
                f"{self.tracks} track(s) no landing took"
            )
        if self.tracks:
            return (
                f"job {self.job_id} of the go under run {self.run}, with {self.tracks} "
                f"track(s) no landing took"
            )
        return (
            f"job {self.job_id} of the go under run {self.run}, whose pass no landing "
            f"took, and whose tail may have renamed those tracks"
        )

    def step(self, folder: Path) -> str:
        if self.run is None:
            return (
                f"land the tracks of job {self.job_id} as any intake lands, or move "
                f"them out of {folder}"
            )
        return (
            f"take job {self.job_id} to its landing, or read the landing its tail "
            f"already reached and answer that, with: {continue_command(self.run)}"
        )

    def to_json(self) -> dict[str, Any]:
        return {"job": self.job_id, "run": self.run, "verb": self.verb, "tracks": self.tracks}


@dataclass(frozen=True, slots=True)
class Beside:
    """What the staging folder holds that a landing would take with a go's own (R-1467).

    ``waiting`` names the downloads it can be put down to, and ``unnamed``
    every file there that no download names. Empty when the folder holds
    nothing but the go's own tracks.
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
                f"land, or move out of {self.folder}, the track(s) no download names"
            )
        return tuple(steps)

    def to_json(self) -> dict[str, Any]:
        return {
            "folder": str(self.folder),
            "waiting": [one.to_json() for one in self.waiting],
            "unnamed": list(self.unnamed),
        }


def _resolved(path: Path | str) -> Path:
    return Path(path).expanduser().absolute().resolve()


def beside(
    cfg: config.Config,
    store: jobs.JobStore,
    staging: Path,
    own: Collection[str],
    *,
    renamed: bool = False,
) -> Beside:
    """What a landing of ``staging`` would take beside ``own``'s downloads (R-1467).

    WHAT A LANDING TAKES IS THE FOLDER, read as the landing reads it,
    :func:`cratekit.intake.landing.listing`. A file there that is one of
    ``own``'s downloaded tracks, at the name it was downloaded under, is the
    go's own. EVERY OTHER FILE IS BESIDE IT, whoever put it there, since the
    landing would file it under the go's manifest and pass: a track of another
    download at its download name, a go's or a plain ``acquire download``'s
    or a fallback fetch's (any job that recorded the file as its artifact), and
    a file no download names, which a tail's ``name apply`` renamed or a person
    put there.

    ``renamed`` says ``own``'s tail already ran (:func:`tail_role`), so files
    no download names may be its own tracks under the names ``name apply``
    gave them: they are read as its own, BUT NEVER MORE OF THEM than its
    downloaded tracks no longer at their download names, so a download added
    since is still beside it.

    NAMING, NOT DECIDING, IS WHAT THE LANDING PROOF IS FOR. A file no download
    names is put down to every go's download with a track recorded in the
    folder, none of them there, whose pass has no landing proof on either
    medium (:func:`cratekit.intake.land_cli.pass_landed`), since its tail may
    have renamed them; a pass that landed is not named. A library root or a
    session log the proof cannot read refuses.

    A folder that is not there holds nothing a landing could take; one that
    cannot be listed refuses, never reads as empty.
    """
    folder = _resolved(staging)
    try:
        held = {_resolved(path) for path in folder_listing(folder)} if folder.is_dir() else set()
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed ({exc}), so whether it "
            f"holds a download no landing took cannot be read; nothing was queued or run",
            steps=(f"make {folder} readable, then run the go again",),
            origin=("label.go",),
            detail={"folder": str(folder)},
        ) from exc
    downloads: dict[str, tuple[jobs.Job, list[Path]]] = {}
    for job in jobs.list_jobs(store):
        inside = [
            path
            for path in (
                _resolved(item.artifact)
                for item in jobs.items(store, job.job_id)
                if item.state is jobs.ItemState.DONE and item.artifact
            )
            if path.parent == folder
        ]
        if inside:
            downloads[job.job_id] = (job, inside)
    mine = [path for job_id in own for path in downloads.get(job_id, (None, []))[1]]
    others = held - set(mine)
    if not others:
        return Beside(folder=folder)
    found: list[Waiting] = []
    named: set[Path] = set()
    for job_id, (job, paths) in downloads.items():
        if job_id in own:
            continue
        present = [path for path in paths if path in others]
        if present:
            named.update(present)
            found.append(
                Waiting(job_id=job_id, run=_origin_run(job), verb=job.handler_key, tracks=len(present))
            )
    unnamed = sorted(others - named)
    if renamed and len(unnamed) <= sum(1 for path in mine if path not in held):
        unnamed = []
    if unnamed:
        proven: dict[str, bool] = {}
        for job_id, (job, paths) in downloads.items():
            run = _origin_run(job)
            if job_id in own or run is None or any(path in others for path in paths):
                continue
            name = default_name(str((job.payload or {}).get(RUN_KEY) or run))
            if name not in proven:
                proven[name] = land_cli.pass_landed(cfg, name)
            if not proven[name]:
                found.append(Waiting(job_id=job_id, run=run, verb=job.handler_key, tracks=0))
    return Beside(
        folder=folder, waiting=tuple(found), unnamed=tuple(path.name for path in unnamed)
    )


def _waiting_refusal(
    found: Beside, staging: Path, walk: Sequence[str] | None
) -> CratekitError:
    """A fresh go refused before its gate, naming what the folder holds (R-1467)."""
    detail: dict[str, Any] = found.to_json()
    if walk is not None:
        detail["answered_this_run"] = list(walk)
    return refuse(
        "refused-by-policy",
        f"the staging folder {found.folder} holds {found.said()}; a landing lands the "
        "whole folder, so this go would land them with its own, under its manifest "
        "and pass, and it did not ask its gate or queue a download",
        steps=(
            *found.steps(),
            "then ask again with: crate label sync --go"
            + ("; the answers given are saved" if walk is not None else ""),
        ),
        origin=("label.go",),
        detail=detail,
    )


def _refuse_beside(
    cfg: config.Config,
    store: jobs.JobStore,
    job: jobs.Job,
    staging: Path,
    manifest: str | None,
    run_of: str,
    landed: Sequence[str],
    *,
    own: Collection[str],
    renamed: bool = False,
    refused: Sequence[dict[str, Any]] = (),
) -> None:
    """Refuse a go's tail while the folder holds what is not its own (U239, R-1467).

    A go job queued after ``job`` (:func:`_beside`), and anything else
    :func:`beside` reads in the folder, would land with it as one batch, so
    the tail is not run, and the refusal carries the landing in its detail,
    which the CLI layer turns into the commands to type once the folder holds
    only this download. Tracks refused for good are carried too, since the
    go's report that names them is not returned.
    """
    later = _beside(store, job)
    known = [other.job_id for other in later]
    found = beside(cfg, store, staging, own, renamed=renamed)
    if not later and not found:
        return
    extra = Beside(
        folder=found.folder,
        waiting=tuple(one for one in found.waiting if one.job_id not in known),
        unnamed=found.unnamed,
    )
    said = [
        f"job {other.job_id} of the go under run {_origin_run(other)} downloaded into "
        f"the same staging folder after it"
        for other in later
    ]
    if extra:
        said.append(extra.said())
    raise refuse(
        "refused-by-policy",
        f"this run's download {job.job_id} is downloaded, and the staging folder "
        f"{found.folder} also holds " + "; ".join(said) + "; the landing lands the whole "
        "folder, so the tail was not run, since it would land the batches as one",
        steps=(
            *extra.steps(),
            "land each download on its own: the tail by hand once the folder holds "
            "only this run's tracks, as the next step names it",
        ),
        origin=("label.go",),
        detail={
            LAND_KEY: landing(staging, manifest, run_of, job.job_id) if manifest else None,
            "job": job.job_id,
            "beside": [*known, *(one.job_id for one in extra.waiting)],
            **extra.to_json(),
            "refused": list(refused),
            "next": list(landed),
        },
    )



def _carried(error: CratekitError, store: jobs.JobStore, job: jobs.Job) -> CratekitError:
    """A go's stopped download, refused with the way on that ends at its landing (U239).

    THE CALL CEILING NAMES THE GO'S RUN, NOT THE JOB. The dispatcher's
    continue command resumes a parked job by its id when the cause names one,
    and ``job resume`` ends at a succeeded job with no next step: the attended
    pass of 2026-11-10 took that path and the tail never ran. So the job id is
    moved off ``job_id`` to ``job``, and the cause names the go's run with
    ``fresh``, which the dispatcher reads as "drop the command line's own
    ``--run``" before adding this one: the continue is then the command line
    that stopped, ``crate --run RUN --calls N label sync --go`` for a go, under
    the run whose decision started the download, whichever run was driving it.

    ANY OTHER STOP A GO TAKES ON ADDS THAT COMMAND AS A STEP. A park, or a
    failure a retry may clear, is continued by its own remedy, and the step
    after it says how the download then reaches its landing. A failure no retry
    can clear and a cancel are left as they were: the go's run does not take
    either on.
    """
    run = _origin_run(job)
    if run is None:
        return error
    cause = error.cause
    if cause.reason == provider_gate.CEILING:
        detail = {key: value for key, value in (cause.detail or {}).items() if key != "job_id"}
        detail.update({"job": job.job_id, "run_id": run, "fresh": True})
        return rebuilt(error, dataclasses.replace(cause, detail=detail))
    left = sum(
        1
        for item in jobs.items(store, job.job_id)
        if item.state not in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)
    )
    if job.state is jobs.JobState.BLOCKED or (
        job.state is jobs.JobState.FAILED and resumable(job, left)
    ):
        steps = (
            *cause.remediation.steps,
            f"once the download can go on, take it to its landing with the decision "
            f"already given: {continue_command(run)}",
        )
        return rebuilt(
            error,
            dataclasses.replace(
                cause, remediation=dataclasses.replace(cause.remediation, steps=steps)
            ),
        )
    return error



def _carry_on(
    ctx,
    cfg: config.Config,
    job_id: str,
    summary: Summary,
    staging: Path,
    checks: list[dict[str, Any]],
    report: dict[str, Any],
    *,
    wrote: bool = False,
) -> Envelope:
    """Take this run's own download on to its landing, asking nothing (U239).

    The attended label pass of 2026-11-10 stopped at the call ceiling with 68
    of 106 tracks staged, finished the job with ``job resume``, and then ran
    ``--go`` under the same run: the answers were settled and a succeeded job
    is no longer one to resume, so the plan was empty, the gate refused it
    stale, and the tail never ran. The decision recorded on this run started
    THIS download, so a go under it resumes the download if it is unfinished,
    reads it once it settled, and names its landing for the CLI layer to run
    the tail on, with the job's own manifest and the pass its run gives.

    NOTHING NEW IS QUEUED, for the reason :func:`_resume` gives: one job, one
    manifest and one landing per go. Answers saved since wait for the next go.

    NOT TWICE. A run whose tail already stopped at its landing for this job,
    recorded under :func:`landing_role` by whichever run drove it, names that
    landing's run and runs nothing, since the folder may hold another batch by
    then and the landing would file it under this go's pass.

    NOT BESIDE ANYTHING ELSE (U239, R-1467). A go job queued after this one,
    and any file in the folder that is not this download's own, would land with
    it as one batch, so the go refuses with the landing in the detail, which the
    CLI layer turns into the commands to type (:func:`_refuse_beside`). Files no
    download names are read as this download's own tracks, renamed by its tail,
    only when this run recorded that its tail started (:func:`tail_role`).
    """
    run_id = ctx.run.run_id
    warnings: list[dict[str, str]] = []
    refused: list[dict[str, Any]] = []
    land: dict[str, str] | None = None
    landed: list[str] = []
    named = ctx.run.related_runs.get(landing_role(job_id))
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        payload = dict(job.payload or {})
        manifest = dict(payload.get(ORIGIN_KEY) or {}).get("manifest")
        manifest = manifest if isinstance(manifest, str) and manifest else None
        run_of = str(payload.get(RUN_KEY) or run_id)
        if named:
            checks.append(
                _check(
                    "landing",
                    "info",
                    f"this run's download {job_id} was taken through its tail to the "
                    f"landing under run {named} already, so nothing was run again; "
                    f"answer and apply that landing, or read it with: "
                    + shlex.join(["crate", "run", "show", named]),
                )
            )
            report["go"] = _carried_report(summary, job_id, manifest, refused, landed, land)
            # A WALK THAT REACHED THIS GO WROTE ITS ANSWERS, so it is not a no-op.
            return ctx.envelope(
                data={"checks": checks, "summary": report},
                outcome=Outcome.OK if wrote else Outcome.NO_OP,
            )
        listed = len(jobs.items(store, job_id))
        left = sum(
            1
            for item in jobs.items(store, job_id)
            if item.state not in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)
        )
        if not job.is_open() and resumable(job, left):
            # STOPPED HALF FAILED WITH A CAUSE A RETRY MAY CLEAR: re-armed, with
            # every downloaded track left done, as :func:`_resume` re-arms.
            if not acquire_cli.read_download(store, job).settled:
                jobs.retry(store, job_id)
        job, drifted, read = _drive(ctx, store, job_id)
        warnings.extend(drifted)
        refused = list(read.refused)
        nothing = read.settled and not read.done
        checks.append(
            _check(
                "continued",
                "fail" if nothing and read.refused else "ok",
                f"took this run's download {job_id} on under the decision already "
                f"given: {_downloaded(read, listed)}",
            )
        )
        if manifest is not None and not nothing:
            landed = tail(staging, manifest, run_of)
        if read.landed:
            _refuse_beside(
                cfg, store, job, staging, manifest, run_of, landed,
                own={job_id}, renamed=bool(ctx.run.related_runs.get(tail_role(job_id))),
                refused=refused,
            )
    if read.landed and manifest is not None:
        land = landing(staging, manifest, run_of, job_id)
    elif landed:
        checks.append(_next_check(landed))
    if summary.answers:
        checks.append(
            _check(
                "waiting",
                "info",
                f"{len(summary.answers)} answer(s) wait for the next go, once this "
                f"download is landed: crate label sync --go",
            )
        )
    report["go"] = _carried_report(summary, job_id, manifest, refused, landed, land)
    return ctx.envelope(
        data={"checks": checks, "summary": report},
        outcome=Outcome.OK,
        warnings=tuple(warnings),
    )


def _carried_report(
    summary: Summary,
    job_id: str,
    manifest: str | None,
    refused: Sequence[dict[str, Any]],
    landed: Sequence[str],
    land: dict[str, str] | None,
) -> dict[str, Any]:
    """The go's report when it took this run's own download on (U239)."""
    return {
        **summary.to_json(),
        "declined": False,
        "job": job_id,
        "continued": job_id,
        "resumed": [],
        "list": None,
        "manifest": manifest,
        "withdrawn": [],
        "carried": [],
        "refused": list(refused),
        "next": list(landed),
        LAND_KEY: land,
    }


__all__ = [
    "APPLY",
    "DOWNLOAD",
    "GATE",
    "LANDING_ROLE",
    "LAND_KEY",
    "LIST_PREFIX",
    "ORIGIN_KEY",
    "REFUSED_WARNING",
    "RUN_KEY",
    "TRANSFER_BYTES_PER_SECOND",
    "Held",
    "Summary",
    "Taken",
    "Beside",
    "TAIL_ROLE",
    "Waiting",
    "continue_command",
    "duration_text",
    "go",
    "held_by_goes",
    "landing",
    "landing_role",
    "own_job",
    "pace_of",
    "resumable",
    "summarise",
    "beside",
    "tail",
    "tail_role",
]
