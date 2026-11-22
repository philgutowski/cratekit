"""``label sync``'s go: one summary over every saved answer, one gate, one download.

U108. The answers saved since the last go become ONE summary under ONE explicit
gate, and on ``apply`` the download runs unattended, paced and resumable, for the
acquisition tail to land as any intake lands. Only the releases an ``all`` or a
``pick`` took are downloaded, while their review item is still ACCEPTED; the
size and the time are estimates (:data:`TRANSFER_BYTES_PER_SECOND`) and say so.

THE DOWNLOAD IS ``acquire download``'s OWN JOB, listed down ``label approved``'s
path and queued with :data:`ORIGIN_KEY`, so a track of a go's job is never asked
for twice. ONE JOB, ONE MANIFEST AND ONE LANDING PER GO, since ``intake land``
lands a whole folder: a go with an unfinished earlier job resumes only that.
Planned, queued and settled under the record's blocking lock.

THE TAIL IS RUN, NOT ONLY NAMED (U190): the report carries :data:`LAND_KEY` for
:mod:`cratekit.cli.label_sync` to hand to :mod:`cratekit.cli.tail`, set only when
the go's one download settled with a track done (R-1115). A GO UNDER ITS OWN RUN
TAKES ITS OWN DOWNLOAD ON, ASKING NOTHING (U239). A GO NEVER LANDS ANOTHER
DOWNLOAD AS ITS OWN (R-1467): anything in the staging folder that is not its own
refuses a fresh go before its gate and every tail after it.
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
from cratekit.intake import beside as staged
from cratekit.intake.beside import Beside, Waiting, continue_command
from cratekit.intake.land_cli import default_name
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import approved_cli, sync_cli
from cratekit.label import gate as genre_gate

#: The one gate, declared on the ``label.sync`` registry entry.
GATE = "label.sync.confirm"
#: The gate's answer that starts a download.
APPLY = "apply"
#: The prefix of the role a go's run records the landing its tail stopped at
#: under (U239), one role per job (:func:`landing_role`), in
#: :attr:`cratekit.cli.gates.RunState.related_runs`. Written by the CLI layer and
#: read here, so a later go under that run names that landing.
LANDING_ROLE = "landing"
#: The directory under the queue root where what each go's tail left in the
#: staging folder is kept, one file per job (R-1467, :func:`keep_tail`).
TAILS_DIRNAME = staged.TAILS_DIRNAME
#: The verb whose job the go queues. Its worker downloads; the go composes.
DOWNLOAD = staged.DOWNLOAD_KEY
#: The payload key a go's download job carries, naming the run and the manifest.
ORIGIN_KEY = staged.ORIGIN_KEY
#: The payload key ``sync all`` already uses for a job's intake run (R29).
RUN_KEY = staged.RUN_KEY
#: The report's key naming the tail the CLI layer runs after a download (U190).
LAND_KEY = "land"
#: The warning a go names each track its download FAILED for good under (R-1115);
#: a track the worker declined is named by its own ``acquire-refused`` warning.
REFUSED_WARNING = "label-sync-download-refused"
#: What every list a go writes is named after, before the digest.
LIST_PREFIX = "label-sync"
#: The marker an answer carries once a go has taken it.
SETTLED = sync_cli.SETTLED
#: The transfer rate the time estimate assumes, 20 megabits a second. An
#: assumption, not a measurement.
TRANSFER_BYTES_PER_SECOND = 2_500_000
#: The answers that take releases.
TAKING = frozenset({sync_cli.ALL, sync_cli.PICK})
#: The ways a release can fail to be read that waiting mends: an answer holding
#: one stays unsettled for the next go, while a release gone stays gone.
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
            "label_id": self.label_id, "label": self.label_name, "release": self.identity,
            "artist": self.artist, "title": self.title, "year": self.year, "tracks": self.tracks,
        }


@dataclass(frozen=True, slots=True)
class Held:
    """The download jobs earlier goes queued: those to resume, each with how many
    of its tracks are still to run, and every track held."""

    resume: tuple[tuple[jobs.Job, int], ...]
    tracks: frozenset[str]


def _left(items: Sequence[Any]) -> int:
    """How many of a job's items are neither done nor skipped."""
    return sum(item.state not in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED) for item in items)


def _goes_job(job: jobs.Job) -> bool:
    """Whether ``job`` is a download a go queued, by the origin it carries."""
    return job.handler_key == DOWNLOAD and isinstance((job.payload or {}).get(ORIGIN_KEY), Mapping)


def resumable(job: jobs.Job, left: int) -> bool:
    """Whether a go resumes this job: open, or stopped with tracks a retry re-arms.

    A job a signal CANCELLED or that ended FAILED with a retryable cause is
    resumed through ``jobs.retry``, which keeps every downloaded track done;
    one whose cause says no retry can succeed is not.
    """
    if job.is_open():
        return True
    if job.state is jobs.JobState.SUCCEEDED or not left:
        return False
    return job.cause is None or job.cause.retryable


def held_by_goes(store: jobs.JobStore) -> Held:
    """Every track a go's job holds, done or still to run, and the jobs to resume.

    A track of a job a go RESUMES is held unless skipped, since the resume
    claims it; of any other go job only when downloaded, so a failed one that
    cannot be retried may be asked for again.
    """
    resume: list[tuple[jobs.Job, int]] = []
    tracks: set[str] = set()
    for job in jobs.list_jobs(store):
        if not _goes_job(job):
            continue
        items = jobs.items(store, job.job_id)
        left = _left(items)
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
    """The releases one saved answer took, from what it recorded about each, with
    no provider call. A taken identity it did not record whole is still taken,
    with its counts unknown, never dropped."""
    label_id = _text(entry.get("label_id"))
    label_name = _text(entry.get("label_name")) or label_id
    raws = entry.get("releases") if isinstance(entry.get("releases"), list) else ()
    recorded = {
        one.identity: one
        for one in (sync_cli.Offered.from_json(raw) for raw in raws if isinstance(raw, Mapping))
        if one.identity
    }
    named = entry.get("taken")
    identities = [str(one) for one in named if isinstance(one, str) and one] if isinstance(
        named, list
    ) else list(recorded)
    found: list[Taken] = []
    for identity in identities:
        one = recorded.get(identity)
        item_id = (one.item_id if one is not None else None) or genre_gate.release_item_id(identity)
        if one is None:
            found.append(Taken(label_id, label_name, identity, item_id, "", "", "", None, None))
        else:
            found.append(
                Taken(label_id, label_name, identity, item_id, one.artist, one.title, one.year,
                      one.tracks, one.size)
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
    #: Jobs an earlier go left unfinished, as ``(job_id, tracks still to run)``;
    #: a go with any resumes them and queues nothing new.
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

        THE DIGEST IS OVER WHAT THE ANSWER DECIDES: the releases by label, the
        labels counted not now and stop, and the jobs a go would resume; never a
        job's progress, which moves while a decision waits.
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
            "answers": len(self.answers), "labels": list(self.taking),
            "releases": len(self.taken), "tracks": self.tracks, "size": self.size,
            "seconds": self.seconds, "unknown": self.unknown, "not_now": list(self.not_now),
            "stopped": list(self.stopped), "resume": [job_id for job_id, _left in self.open_jobs],
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
    """One summary over every saved answer no go has taken yet. A release two
    answers took is counted once, under the first answer that took it."""
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
    return Summary(
        answers=tuple(answers),
        taken=tuple(taken.values()),
        taking=tuple(taking),
        not_now=tuple(not_now),
        stopped=tuple(stopped),
        open_jobs=tuple((job.job_id, left) for job, left in held.resume),
        pace_s=pace_of(cfg),
    )


# ---------------------------------------------------------------------------
# The gate and the go
# ---------------------------------------------------------------------------


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.sync.go.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _gate(ctx):
    """The declared gate the go is asked through, or a refusal naming the defect,
    never a default: a go whose gate a registry edit dropped would ask nobody."""
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

    THE LANDING NAMES ITS OWN BATCH (U110): the go's run is handed as the pass
    (R-1056) and no ``--name``, so the batch takes the landing's date and label.
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
    """What the tail and the landing run over, the three the last command of
    :func:`tail` names as data, with the go's run and its job (U239), so the
    landing is recorded on the run whose go queued that job."""
    return {
        "folder": str(staging), "manifest": manifest, "pass": default_name(run_id),
        "run": run_id, "job": job_id,
    }


def landing_role(job_id: str) -> str:
    """The role a landing the tail reached for ``job_id`` is recorded under (U239),
    one per job, so a landing never answers for another download of the run."""
    return f"{LANDING_ROLE}.{job_id}"


def _drive(
    ctx, store: jobs.JobStore, job_id: str
) -> tuple[jobs.Job, list[dict[str, str]], acquire_cli.DownloadRead]:
    """Drive one go's download, and read how it settled (R-1115).

    A refusal of the drive is re-raised, with the way on to its landing
    (:func:`_carried`), UNLESS the job ended FAILED only by tracks refused for
    good: then its warnings are the declined tracks', read off the item rows.
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
        message = (
            f"{acquire_cli.track_name(job, item_id)} ({item_id}) failed for good "
            f"and is skipped ({row['reason']}): {row['message']}"
        )
        warnings.append({"code": REFUSED_WARNING, "message": message})
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


def _driven(
    ctx, store: jobs.JobStore, job_id: str, key: str, said: str,
    checks: list[dict[str, Any]], warnings: list[dict[str, str]], listed: int | None = None,
) -> tuple[jobs.Job, acquire_cli.DownloadRead, bool]:
    """Drive one download, add its line and its warnings, and say whether it
    settled with nothing done, which runs no tail."""
    job, drifted, read = _drive(ctx, store, job_id)
    warnings.extend(drifted)
    nothing = read.settled and not read.done
    count = len(jobs.items(store, job_id)) if listed is None else listed
    status = "fail" if nothing and read.refused else "ok"
    checks.append(_check(key, status, f"{said}: {_downloaded(read, count)}"))
    return job, read, nothing


def _report(
    summary: Summary, job: str | None, refused: Sequence[dict[str, Any]],
    landed: Sequence[str], land: dict[str, str] | None, *,
    also: Mapping[str, Any] | None = None, list_path: str | None = None,
    manifest: str | None = None, withdrawn: Sequence[str] = (), carried: Sequence[str] = (),
) -> dict[str, Any]:
    """The go's report of a go that did not decline."""
    return {
        **summary.to_json(),
        "declined": False,
        "job": job,
        **(also or {}),
        "list": list_path,
        "manifest": manifest,
        "withdrawn": list(withdrawn),
        "carried": list(carried),
        "refused": list(refused),
        "next": list(landed),
        LAND_KEY: land,
    }


def _waiting(summary: Summary, checks: list[dict[str, Any]]) -> None:
    """Say the answers saved beside a download wait for the next go."""
    if summary.answers:
        checks.append(_check(
            "waiting", "info",
            f"{len(summary.answers)} answer(s) wait for the next go, once this "
            f"download is landed: crate label sync --go",
        ))


def _ended(ctx, checks, report, warnings) -> Envelope:
    return ctx.envelope(
        data={"checks": checks, "summary": report}, outcome=Outcome.OK, warnings=tuple(warnings)
    )


def go(
    ctx, cfg: config.Config, *, walk: Sequence[str] | None = None,
    data: Mapping[str, Any] | None = None, wrote: bool = False,
) -> Envelope:
    """Show the summary, ask the gate, and on apply download what was answered for.

    Under the run of a go that already started a download, take that download
    on instead, asking nothing (:func:`_carry_on`, U239). ``walk`` is one line
    per label the walk answered, shown in front of the summary; ``data`` is the
    walk's own report, kept beside the go's; ``wrote`` says the walk wrote, so a
    run that answered and then declined is not a no-op.
    """
    spec = _gate(ctx)
    run_id = ctx.run.run_id
    document = sync_cli.load_record(cfg)
    with jobs.open_store() as store:
        summary = summarise(document, held_by_goes(store), cfg)
    # ABSOLUTE, as ``sync land`` takes it: a relative root once planned nothing (U169).
    staging = Path(cfg.paths.download_staging).expanduser().absolute()
    base = dict(data or {})
    checks: list[dict[str, Any]] = list(base.pop("checks", []))
    report: dict[str, Any] = dict(base.pop("summary", {}) or {})
    own = _own(ctx)
    if own is not None:
        # THIS RUN'S GO ALREADY STARTED A DOWNLOAD (U239): taken on, not asked again.
        return _carry_on(ctx, cfg, own, summary, staging, checks, report, wrote=wrote)
    # NOTHING IN THE FOLDER BUT WHAT THIS GO WOULD LAND (R-1467), read before the
    # gate; the jobs this go would resume are its own batch.
    with jobs.open_store() as store:
        found = beside(cfg, store, staging, {job_id for job_id, _left in summary.open_jobs})
    if found:
        raise _waiting_refusal(found, staging, walk)
    facts: dict[str, Any] = {"answered_this_run": list(walk)} if walk is not None else {}
    facts.update(summary.facts())
    facts["after_deciding"] = shlex.join(["crate", "--run", run_id, "label", "sync", "--go"])
    option = ctx.gate.require(spec, plan=summary.plan(), context=facts)

    checks.append(_check("summary", "info", _summary_line(summary)))
    if option == "abort":
        checks.append(_check(
            "declined", "ok",
            f"declined: nothing was downloaded, and the {len(summary.answers)} "
            f"answer(s) are kept for a later go: crate label sync --go",
        ))
        report["go"] = {**summary.to_json(), "declined": True, "job": None}
        return ctx.envelope(
            data={"checks": checks, "summary": report},
            outcome=Outcome.OK if wrote else Outcome.NO_OP,
        )

    if summary.open_jobs:
        return _resume(ctx, cfg, summary, staging, checks, report)

    warnings: list[dict[str, str]] = []
    withdrawn: list[Taken] = []
    listing = None
    queued: jobs.Job | None = None
    # PLANNED, QUEUED AND SETTLED UNDER THE RECORD'S LOCK, which blocks: a
    # second go waits here, then finds the job this one queued. The drive is outside it.
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
                cfg, releases, out=lambda: staging / LISTS_DIR,
                handler_key=ctx.entry.handler_key, prefix=LIST_PREFIX,
                already=held.tracks,
                excuse=frozenset({approved_cli.GONE, approved_cli.NO_IDENTIFIER}),
                elsewhere="make the lists folder under download staging writable",
            )
            written = listing.written
            if written.list_path is not None:
                with jobs.open_store() as store:
                    queued = acquire_cli.queue_list(
                        store, cfg, written.list_path, handler_key=DOWNLOAD,
                        extra={
                            ORIGIN_KEY: {"run": run_id, "manifest": str(written.manifest_path)},
                            RUN_KEY: run_id,
                        },
                    )
        # SETTLED AFTER THE QUEUE AND BEFORE THE DRIVE, so a go killed on either
        # side leaves the job for the next go to resume and asks for nothing
        # twice. An answer holding a release the provider did not answer for is
        # left unsettled, so the next go asks for that release again.
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
        checks.append(_check(
            "withdrawn", "info",
            f"{len(withdrawn)} release(s) an answer took are no longer accepted in "
            f"review and were not downloaded: "
            + ", ".join(f"{one.label_name} {one.identity}" for one in withdrawn),
        ))
    manifest = list_path = None
    if listing is not None:
        manifest = str(listing.written.manifest_path)
        if listing.written.list_path is not None:
            list_path = str(listing.written.list_path)
        checks.append(_check(
            "listed", "ok" if listing.listed else "info",
            f"{listing.listed} missing track(s) from {listing.passed} answered "
            f"release(s) listed to {listing.written.list_path}"
            if listing.listed
            else f"nothing to download: the library holds, or an earlier go already "
            f"holds, every track of the {listing.passed} answered release(s) the "
            f"genre gate passed",
        ))
        checks.append(_check(
            "held-by-a-go", "info",
            f"{listing.counts['queued']} track(s) an earlier go already holds, not "
            f"asked for again",
        ))
        checks.extend(approved_cli.listing_checks(listing, namespace="label.sync.go.list"))
    if retry:
        checks.append(_check(
            "carried", "fail",
            f"{len(retry)} release(s) could not be read, so the answer(s) holding "
            f"them are kept for the next go: crate label sync --go",
        ))
    checks.append(
        _check("settled", "info",
               f"{settled} answer(s) taken by this go; it asks about none of them again")
    )

    landed: list[str] = []
    land: dict[str, str] | None = None
    refused: list[dict[str, Any]] = []
    if queued is not None:
        with jobs.open_store() as store:
            queued, read, nothing = _driven(
                ctx, store, queued.job_id, "downloaded", f"job {queued.job_id}", checks,
                warnings, listing.listed,
            )
        refused = list(read.refused)
        if not nothing:
            landed = tail(staging, manifest, run_id)
        if read.landed:
            # A DOWNLOAD THAT FINISHED IN THE FOLDER WHILE THIS ONE DROVE (R-1467).
            with jobs.open_store() as store:
                _refuse_beside(
                    cfg, store, queued, staging, manifest,
                    run_id, landed, own={queued.job_id}, refused=refused,
                )
            land = landing(staging, manifest, run_id, queued.job_id)
        if land is None and landed:
            checks.append(_next_check(landed))
    if listing is None or listing.written.manifest_path is None:
        manifest = None
    report["go"] = _report(
        summary, queued.job_id if queued is not None else None, refused, landed, land,
        list_path=list_path, manifest=manifest, withdrawn=[one.identity for one in withdrawn],
        carried=sorted(retry),
    )
    return ctx.envelope(
        data={"checks": checks, "summary": report},
        outcome=Outcome.OK if queued is not None or settled or wrote else Outcome.NO_OP,
        warnings=tuple(warnings),
    )


def _next_check(landed: Sequence[str]) -> dict[str, Any]:
    return _check(
        "next", "info",
        "land it as any intake lands, in this order, before the next go adds to "
        "the same folder: " + "; then ".join(landed),
    )


def _resume(
    ctx, cfg: config.Config, summary: Summary, staging: Path,
    checks: list[dict[str, Any]], report: dict[str, Any],
) -> Envelope:
    """Resume what earlier goes left unfinished, and queue nothing new.

    ONE JOB PER GO: a resumed job and a new one would stage into one folder
    under two manifests, and the landing would take both as one batch. The
    answers saved since wait for the next go.
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
            job, read, nothing = _driven(
                ctx, store, job_id, f"resumed.{job_id}",
                f"resumed the earlier download {job_id}", checks, warnings,
            )
            resumed.append(job_id)
            refused.extend(read.refused)
            payload = dict(job.payload or {})
            manifest = dict(payload.get(ORIGIN_KEY) or {}).get("manifest")
            if isinstance(manifest, str) and manifest and not nothing:
                run_of = str(payload.get(RUN_KEY) or ctx.run.run_id)
                landed.extend(tail(staging, manifest, run_of))
                lands.append(landing(staging, manifest, run_of, job_id) if read.landed else None)
            else:
                lands.append(None)
    # ONE EARLIER JOB, LANDED, IS RUN ON THROUGH THE TAIL; several would need two
    # manifests on one landing, so their commands are printed.
    land = lands[0] if len(lands) == 1 else None
    if land is not None:
        # NOT BESIDE ANOTHER DOWNLOAD (R-1467), checked again once the resume drove.
        with jobs.open_store() as store:
            _refuse_beside(
                cfg, store, jobs.get(store, land["job"]), staging, land["manifest"],
                land["run"], landed, own=set(resumed), refused=refused,
            )
    _waiting(summary, checks)
    if landed and land is None:
        checks.append(_next_check(landed))
    report["go"] = _report(summary, None, refused, landed, land, also={"resumed": resumed})
    return _ended(ctx, checks, report, warnings)


def own_job(store: jobs.JobStore, run_id: str) -> jobs.Job | None:
    """The download job this run's go queued, or None (U239): a go queues at most
    one, and the job carries the run in its origin."""
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

    ONLY UNDER A RECORDED APPLY, and only a job this run's own go queued. A
    CANCELLED job is a person's stop, so the go falls through to its gate.
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

    Each stages into the same folder, so a tail run now would land both as one.
    A job stamped the same instant is counted, since which came first cannot be
    told. An earlier one and a plain download are read by :func:`beside` (R-1467).
    """
    found: list[jobs.Job] = []
    for other in jobs.list_jobs(store):
        if other.job_id == job.job_id or other.created < job.created:
            continue
        if not _goes_job(other):
            continue
        if other.is_open() or any(
            item.state is jobs.ItemState.DONE for item in jobs.items(store, other.job_id)
        ):
            found.append(other)
    return found


def keep_tail(cfg: config.Config, store: jobs.JobStore, job_id: str, staging: Path) -> int:
    """Keep what the staging folder holds as a go's tail stops, and return how many (R-1467).

    The tail's ``name apply`` renames every track, so this is the one record of
    them for a later ``--go`` under the run (:func:`cratekit.intake.beside.keep`).
    Called by the CLI layer however the tail ends; a write that fails raises.
    """
    return staged.keep(store, staged.go_record(cfg, job_id), staging, {job_id}, key=job_id)


def kept_tail(cfg: config.Config, job_id: str) -> frozenset[tuple[str, int, int]]:
    """What :func:`keep_tail` kept for ``job_id``, or nothing when it cannot be read,
    so a lost record refuses the go's own tail and never lands a file as its own."""
    return staged.kept(staged.go_record(cfg, job_id))


#: How many of the files no download names a refusal lists by name.
UNNAMED_SHOWN = staged.UNNAMED_SHOWN


def beside(
    cfg: config.Config, store: jobs.JobStore, staging: Path, own: Collection[str], *,
    kept: frozenset[tuple[str, int, int]] = frozenset(), own_pass: str | None = None,
) -> Beside:
    """What a landing of ``staging`` would take beside ``own``'s downloads (R-1467).

    :func:`cratekit.intake.beside.beside`, the reading ``sync land`` shares:
    anything that is not one of the go's own tracks at its download name, or a
    file its own tail left (``kept``) while ``own_pass`` has no landing proof.
    A folder or a library root that cannot be read refuses.
    """
    return staged.beside(
        cfg, store, staging, own, kept=kept, own_pass=own_pass, origin=("label.go",),
        again="then run the go again",
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
    cfg: config.Config, store: jobs.JobStore, job: jobs.Job, staging: Path,
    manifest: str | None, run_of: str, landed: Sequence[str], *, own: Collection[str],
    kept: frozenset[tuple[str, int, int]] = frozenset(), refused: Sequence[dict[str, Any]] = (),
) -> None:
    """Refuse a go's tail while the folder holds what is not its own (U239, R-1467).

    A later go job (:func:`_beside`) or anything else :func:`beside` reads
    would land with it as one batch. The refusal carries the landing, which the
    CLI layer turns into the commands to type, and the tracks refused for good.
    """
    later = _beside(store, job)
    known = [other.job_id for other in later]
    found = beside(
        cfg, store, staging, own, kept=kept, own_pass=default_name(run_of) if kept else None
    )
    if not later and not found:
        return
    waiting = tuple(one for one in found.waiting if one.job_id not in known)
    extra = Beside(folder=found.folder, waiting=waiting, unnamed=found.unnamed)
    said = [
        f"job {other.job_id} of the go under run {staged.origin_run(other)} downloaded into "
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

    THE CALL CEILING NAMES THE GO'S RUN, NOT THE JOB: ``job resume`` ends at a
    succeeded job with no next step, so the job id moves off ``job_id`` to
    ``job`` and the cause names the run with ``fresh``, which the dispatcher
    reads as "drop the command line's own ``--run``", so the continue is the go
    under the run whose decision started the download. A park, or a failure a
    retry may clear, adds that command as a step after its own remedy; a failure
    no retry can clear and a cancel are left as they were.
    """
    run = staged.origin_run(job)
    if run is None:
        return error
    cause = error.cause
    if cause.reason == provider_gate.CEILING:
        detail = {key: value for key, value in (cause.detail or {}).items() if key != "job_id"}
        detail.update({"job": job.job_id, "run_id": run, "fresh": True})
        return rebuilt(error, dataclasses.replace(cause, detail=detail))
    left = _left(jobs.items(store, job.job_id))
    if job.state is jobs.JobState.BLOCKED or (
        job.state is jobs.JobState.FAILED and resumable(job, left)
    ):
        steps = (
            *cause.remediation.steps,
            f"once the download can go on, take it to its landing with the decision "
            f"already given: {continue_command(run)}",
        )
        remediation = dataclasses.replace(cause.remediation, steps=steps)
        return rebuilt(error, dataclasses.replace(cause, remediation=remediation))
    return error


def _carry_on(
    ctx, cfg: config.Config, job_id: str, summary: Summary, staging: Path,
    checks: list[dict[str, Any]], report: dict[str, Any], *, wrote: bool = False,
) -> Envelope:
    """Take this run's own download on to its landing, asking nothing (U239).

    The decision recorded on this run started THIS download, so a go under it
    resumes the download if it is unfinished, reads it once it settled, and
    names its landing with the job's own manifest and the pass its run gives.
    Nothing new is queued (:func:`_resume`). NOT TWICE: a run whose tail already
    stopped at its landing for this job (:func:`landing_role`) names that
    landing's run and runs nothing. NOT BESIDE ANYTHING ELSE (R-1467): files no
    download names are this download's own only when its tail left them
    (:func:`keep_tail`) and its pass has no landing proof.
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
        also = {"continued": job_id, "resumed": []}
        if named:
            checks.append(_check(
                "landing", "info",
                f"this run's download {job_id} was taken through its tail to the "
                f"landing under run {named} already, so nothing was run again; "
                f"answer and apply that landing, or read it with: "
                + shlex.join(["crate", "run", "show", named]),
            ))
            report["go"] = _report(summary, job_id, refused, landed, land, also=also,
                                   manifest=manifest)
            # A WALK THAT REACHED THIS GO WROTE ITS ANSWERS, so it is not a no-op.
            return ctx.envelope(
                data={"checks": checks, "summary": report},
                outcome=Outcome.OK if wrote else Outcome.NO_OP,
            )
        listed = len(jobs.items(store, job_id))
        left = _left(jobs.items(store, job_id))
        if not job.is_open() and resumable(job, left):
            # STOPPED HALF FAILED WITH A CAUSE A RETRY MAY CLEAR: re-armed, as
            # :func:`_resume` re-arms.
            if not acquire_cli.read_download(store, job).settled:
                jobs.retry(store, job_id)
        job, read, nothing = _driven(
            ctx, store, job_id, "continued",
            f"took this run's download {job_id} on under the decision already given",
            checks, warnings, listed,
        )
        refused = list(read.refused)
        if manifest is not None and not nothing:
            landed = tail(staging, manifest, run_of)
        if read.landed:
            _refuse_beside(
                cfg, store, job, staging, manifest, run_of, landed,
                own={job_id}, kept=kept_tail(cfg, job_id),
                refused=refused,
            )
    if read.landed and manifest is not None:
        land = landing(staging, manifest, run_of, job_id)
    elif landed:
        checks.append(_next_check(landed))
    _waiting(summary, checks)
    report["go"] = _report(summary, job_id, refused, landed, land, also=also, manifest=manifest)
    return _ended(ctx, checks, report, warnings)


__all__ = [
    "APPLY", "DOWNLOAD", "GATE", "LANDING_ROLE", "LAND_KEY", "LIST_PREFIX", "ORIGIN_KEY",
    "REFUSED_WARNING", "RUN_KEY", "TRANSFER_BYTES_PER_SECOND", "Held", "Summary", "Taken",
    "Beside", "TAILS_DIRNAME", "Waiting", "continue_command", "duration_text", "go",
    "held_by_goes", "landing", "landing_role", "own_job", "pace_of", "resumable", "summarise",
    "beside", "tail", "keep_tail", "kept_tail",
]
