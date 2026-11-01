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
download --job``, or by ``job resume``, and claims only the items still to run.

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
when the go's one download SUCCEEDED with a track done: a go that declined,
listed nothing, downloaded nothing or is still downloading names no tail, and
neither does a resume over more than one earlier job, whose manifests one
landing of one folder cannot both carry. Then the commands are printed as before.
"""

from __future__ import annotations

import shlex
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import download
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, review
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Verdict
from cratekit.intake.land_cli import default_name
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import approved_cli, sync_cli
from cratekit.label import gate as genre_gate

#: The one gate, declared on the ``label.sync`` registry entry.
GATE = "label.sync.confirm"
#: The verb whose job the go queues. Its worker downloads; the go composes.
DOWNLOAD = "acquire.download"
#: The payload key a go's download job carries, naming the run and the manifest.
ORIGIN_KEY = "label_sync"
#: The payload key ``sync all`` already uses for a job's intake run (R29).
RUN_KEY = "run_id"
#: The report's key naming the tail the CLI layer runs after a download (U190).
LAND_KEY = "land"
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
    which names the intake file ``label mark`` reads, and no ``--name``, so the
    batch folder and its INBOX playlist take the landing's date and the label
    the manifest names rather than the run's identifier.
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


def landing(staging: Path, manifest: str, run_id: str) -> dict[str, str]:
    """What the tail and the landing run over: the folder, the manifest and the pass.

    The same three the last command :func:`tail` names, as data, so the chain
    that runs them reads no command line back.
    """
    return {"folder": str(staging), "manifest": manifest, "pass": default_name(run_id)}


def _landed(store: jobs.JobStore, job: jobs.Job) -> bool:
    """Whether ``job`` ended SUCCEEDED with at least one track downloaded."""
    if job.state is not jobs.JobState.SUCCEEDED:
        return False
    return bool(jobs.progress(store, job.job_id)["counts"][str(jobs.ItemState.DONE)])


def go(
    ctx,
    cfg: config.Config,
    *,
    walk: Sequence[str] | None = None,
    data: Mapping[str, Any] | None = None,
    wrote: bool = False,
) -> Envelope:
    """Show the summary, ask the gate, and on apply download what was answered for.

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

    # ABSOLUTE, as ``sync land`` takes it: a relative root resolves against the
    # working directory, and the tail named over it once planned nothing (U169).
    staging = Path(cfg.paths.download_staging).expanduser().absolute()
    if summary.open_jobs:
        return _resume(ctx, summary, staging, checks, report, wrote=wrote)

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
    if queued is not None:
        with jobs.open_store() as store:
            queued, drifted = acquire_cli.drive_queued(ctx, store, queued.job_id)
            done = jobs.progress(store, queued.job_id)["counts"][str(jobs.ItemState.DONE)]
            ran = _landed(store, queued)
        warnings.extend(drifted)
        checks.append(
            _check(
                "downloaded",
                "ok",
                f"job {queued.job_id}: {queued.state}, {done} of {listing.listed} "
                f"track(s) downloaded",
            )
        )
        landed = tail(staging, str(listing.written.manifest_path), run_id)
        if ran:
            land = landing(staging, str(listing.written.manifest_path), run_id)
        else:
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
    lands: list[dict[str, str] | None] = []
    with jobs.open_store() as store:
        for job_id, _left in summary.open_jobs:
            job = jobs.get(store, job_id)
            if not job.is_open():
                # STOPPED BY A SIGNAL OR ENDED HALF FAILED: re-armed, with
                # every downloaded track left done.
                jobs.retry(store, job_id)
            job, drifted = acquire_cli.drive_queued(ctx, store, job_id)
            warnings.extend(drifted)
            resumed.append(job_id)
            checks.append(
                _check(f"resumed.{job_id}", "ok", f"resumed the earlier download {job_id}: {job.state}")
            )
            payload = dict(job.payload or {})
            manifest = dict(payload.get(ORIGIN_KEY) or {}).get("manifest")
            if isinstance(manifest, str) and manifest:
                run_of = str(payload.get(RUN_KEY) or ctx.run.run_id)
                landed.extend(tail(staging, manifest, run_of))
                lands.append(landing(staging, manifest, run_of) if _landed(store, job) else None)
            else:
                lands.append(None)
    # ONE EARLIER JOB, LANDED, IS RUN ON THROUGH THE TAIL. Several would need two
    # manifests on one landing of one folder, so their commands are printed.
    land = lands[0] if len(lands) == 1 else None
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
        "next": landed,
        LAND_KEY: land,
    }
    return ctx.envelope(
        data={"checks": checks, "summary": report},
        outcome=Outcome.OK,
        warnings=tuple(warnings),
    )


__all__ = [
    "DOWNLOAD",
    "GATE",
    "LAND_KEY",
    "LIST_PREFIX",
    "ORIGIN_KEY",
    "RUN_KEY",
    "TRANSFER_BYTES_PER_SECOND",
    "Held",
    "Summary",
    "Taken",
    "duration_text",
    "go",
    "held_by_goes",
    "landing",
    "pace_of",
    "resumable",
    "summarise",
    "tail",
]
