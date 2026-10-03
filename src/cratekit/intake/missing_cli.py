"""``intake.missing``: the list document for a finished playlist intake.

R-400's verb half, for the intake entrance. ``intake playlist`` resolves every
track to OWNED, OFFERED, SUPPRESSED or MISSING and stops, and ``acquire
download`` reads a list document nothing in the product wrote. This verb reads
the finished job's committed reports and hands the missing rows to the one
emitter, :func:`cratekit.acquire.listdoc.write`, so a person gets a file the
download verb accepts without retyping a track.

ONLY MISSING IS LISTED. An owned track is held, an offered one is a question a
person has not answered yet, and a suppressed one is a track somebody deleted
on purpose. Listing any of those would spend a download on an answer nobody gave.

MISSING WHEN THE JOB RAN IS ASKED AGAIN AT LISTING TIME (R-502). A report's
state was fixed when the job ran, and the second listing of a job whose tracks
were since downloaded and landed handed a person the same download again. Each
missing row is asked of the library and the tombstone store once more, through
the consult the worker used, against the library as it is now, and a row
that is now held, deleted on purpose or a question for a person is counted
under ``since`` and neither listed nor handed on. The reports are not
rewritten. A rerun over a library that gained nothing writes the same bytes;
one that gained every row writes nothing and names no download; one that gained
some writes a shorter list, which the emitter refuses over the job's earlier
list of the same name, and the refusal says so.

AN OFFERED ROW IS LISTABLE ONCE IT IS ANSWERED (R-503). The offered check sends
a person to ``crate review list``, and for as long as the listing read only the
report, no answer given there ever reached it. Each offered row's review item is
looked up by the identifier its report names, read only. An unanswered row stays
offered and nothing more is asked. An answered one goes through the same consult
as a missing row, so the answer decides it as the worker would: a rejection is
missing and listed unless a tombstone stands, a yes bound to a copy still held
is owned, and a yes about a copy that is gone stays a question. The counts say
what each row is now, and ``answered_*`` says how many got there by an answer.
A rejected row makes the job's list longer than an earlier copy of the same
name, which the emitter refuses, and the refusal says so.

A PARTIAL LIST THAT READS AS COMPLETE IS THE DEFECT THIS FILE IS SHAPED
AGAINST. A job that is still open, failed or was cancelled has not resolved
every track, so it is refused rather than listed. A succeeded job is listed only
when every one of its items has exactly one readable report, compared by item
identifier and not by count, because ``artifacts.committed`` skips a report it
cannot parse and a count that happened to match would hide which one it
skipped. A missing row the provider cannot name is written to the unlisted text
list below and the report says how many, as a failing check rather than a quiet
omission, so a job whose missing rows are ALL like that still writes a file and
never reads as a job where everything was owned.

``--run RUN_ID`` is the same list for a whole ``crate sync all`` pass (U73). A
pass queues one intake job per new playlist under one run, and R29 says a run
ends in one intake file, so it ends in one list too, named for the run, which
downloads and lands as one batch. The jobs are the intake jobs carrying the run
AND queued for this library, because the queue is installation scoped and the
run alone would merge two libraries' passes. Every rule above holds per job, and
the run adds two: one open job refuses the whole run, since the list would read
as the pass, and a failed or cancelled job is named and refused unless
``--skip-failed`` says to leave it out, in which case it is reported as a failing
check. A track two playlists share is one row, taken from the first job, and the
manifest keeps every playlist it came from.

A ROW WITH NO PROVIDER IDENTIFIER IS NAMED BY ITS ISRC OR HANDED ON, NEVER
GUESSED (U78, R-401). A recognised set track carries no provider identifier, so
before anything is written each such row is asked of the catalogue by ISRC, one
question per distinct code, and only when there is such a row at all. Exactly
one distinct identifier lists the row. No ISRC, a malformed one, an ISRC the
provider files nothing under, and one it files several tracks under (R-356, the
common case and not the rare one) all hand the row on to ``<name>.unlisted.json``,
a text list ``match run`` reads, with the reason above each line. A provider
that could not answer refuses the whole verb before any file is written, because
a partial answer would hand on a row that could have been named.

``--list PATH`` IS THE ROUTE FOR A ROW NOTHING NAMES EXACTLY (U79, R-302). The
input is the unlisted text list above, or any list ``match run`` reads: a typed
tracklist, a transcribed screenshot. Every row is resolved against the library
first, exactly as ``match run`` resolves it, so an owned track, a track held in
another version and a track deleted on purpose are never searched for. A row
that is still missing and carries no identifier is asked by ISRC when it has
one, and otherwise handed to :mod:`cratekit.intake.candidates`, where a search
is a proposal and never a pick: exactly one candidate matching under the
product's own fold is listed, anything else is offered for review with its
candidates, and an accepted candidate is listed by the next run. Nothing is
ever listed from a fuzzy score. The list is named for the input, with
``-found`` and a digest of what it lists after it, so it never lands on the
job's own list, and a second run that lists more, the run after a review
answer, writes a new list rather than refusing over the first.

Not gated and not destructive: it writes new files, and :func:`listdoc.write`
refuses rather than replaces a file that holds anything else, so it cannot
overwrite somebody's list. Nothing here composes ``acquire download``, so
nothing here can spend a download.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import shlex
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import artifacts, jobs, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import candidates, land_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue

#: The payload key ``crate sync all`` stamps each job it queues with.
RUN_ID = "run_id"

#: What a run's list and its landing's intake file are named after the run, so
#: the list, the download and the landing read as one pass. The batch itself is
#: named for the date and the source since U110, and ``land_name`` in the
#: listing's subject is this pass, handed to the landing as ``--pass``.
SYNCED_SUFFIX = "_synced"

#: What the provenance sidecar says a listed row came from, by the job's key.
#: A set job reaches the sidecar through a row its ISRC named (U78).
PROVENANCE_SOURCE: Mapping[str, str] = {"intake.playlist": "playlist", "intake.set": "set"}

#: What the sidecar says a row named from a list somebody already had came from.
LIST_SOURCE = "list"

#: What follows the input's name in the name of the list ``--list`` writes.
FOUND_SUFFIX = "-found"

#: How many bytes of digest follow that, the width ``label approved`` names its
#: lists with.
DIGEST_BYTES = 6

#: The suffixes an input list's file name may end in, longest first, taken off
#: before the list written from it is named.
_LIST_SUFFIXES = (listdoc.UNLISTED_SUFFIX, listdoc.LIST_SUFFIX, ".json", ".txt")

#: The folder under download staging a list lands in when ``--out`` is not given.
LISTS_DIR = "lists"

#: The four words a committed intake report may carry. A report carrying any
#: other is refused, because a state this verb cannot read is a track it cannot
#: say is or is not missing.
_WORDS = frozenset({"owned", "offered", "suppressed", "missing"})

#: What a row its job resolved missing has become since, by the summary key it
#: is counted under. A row still missing has no key: it is listed as before.
_SINCE: Mapping[match.MatchState, str] = {
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
    match.MatchState.NEEDS_REVIEW: "offered_since",
}

#: What a row its job offered for review, and a person has answered since, is
#: now, by the summary key it is counted under (R-503).
_ANSWERED: Mapping[match.MatchState, str] = {
    match.MatchState.MISSING: "answered_missing",
    match.MatchState.MATCHED: "answered_owned",
    match.MatchState.SUPPRESSED: "answered_suppressed",
    match.MatchState.NEEDS_REVIEW: "answered_offered",
}

#: The report word each state the consult answers is counted under.
_WORD: Mapping[match.MatchState, str] = {
    match.MatchState.MISSING: "missing",
    match.MatchState.MATCHED: "owned",
    match.MatchState.SUPPRESSED: "suppressed",
    match.MatchState.NEEDS_REVIEW: "offered",
}

#: Twelve characters: country, registrant, year, designation. Hyphens and
#: spaces are presentation and are folded away before the shape is asked, and a
#: code of any other shape is never sent to the provider.

#: Why a row was handed on rather than listed, one word a script can switch on.
NO_ISRC = "none"
MALFORMED = "malformed"
UNKNOWN = "unknown"
SEVERAL = "several"
UNREADABLE = "unreadable"


@dataclass(frozen=True, slots=True)
class _Unnamed:
    """A row the provider cannot name exactly: the word, and the sentence."""

    why: str
    reason: str


def build_missing(parser, entry) -> None:
    chosen = parser.add_mutually_exclusive_group(required=True)
    chosen.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="the finished intake job whose missing tracks to list",
    )
    # ITS OWN DEST, NOT ``run``. The dispatcher's global ``--run`` continues a
    # run stopped at a gate and reads ``args.run``; a subcommand flag writing
    # the same name would hand a sync pass's identifier to the gate loader.
    chosen.add_argument(
        "--run",
        dest="sync_run",
        default=None,
        metavar="RUN_ID",
        help="the sync all pass whose intake jobs to list as one",
    )
    chosen.add_argument(
        "--list",
        dest="text_list",
        default=None,
        metavar="PATH",
        help=(
            "a text list, the unlisted list of an earlier run or any tracklist, "
            "whose missing tracks to find on the provider and list"
        ),
    )
    parser.add_argument(
        "--skip-failed",
        action="store_true",
        dest="skip_failed",
        help="with --run, leave out a job that failed or was cancelled and say so",
    )
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=intake_missing)


def _resume_argv(job: jobs.Job) -> str:
    resume = intake_cli.playlist_argv if job.handler_key == "intake.playlist" else intake_cli.set_argv
    return shlex.join(resume(job))


def _unusable(message: str, *steps: str, inner=None, **detail: Any):
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        origin=("intake.missing",),
        detail=detail,
        inner=inner,
    )


def _finished_or_refuse(store, job_id: str) -> jobs.Job:
    """The job, if it is an intake job that ran every track to the end."""
    job = jobs.get(store, job_id)
    if job.handler_key not in intake_cli.INTAKE_KEYS:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not an "
            f"intake job, so there are no intake reports to list",
            steps=("name the job an intake playlist or intake set run printed",),
            origin=("intake.missing",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    if job.state is not jobs.JobState.SUCCEEDED:
        argv = _resume_argv(job)
        raise _unusable(
            f"job {job.job_id} is {job.state}, not succeeded, so some of its tracks "
            f"may not be resolved and a list of the rest would read as complete",
            f"finish it with: crate {argv}" if job.is_open() else
            "queue the playlist again, let it finish, then list that job",
            inner=job.cause,
            job_id=job.job_id,
            state=str(job.state),
        )
    return job


def _reports_or_refuse(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """One readable report per item, read with the configuration the job froze.

    BY IDENTIFIER, NOT BY COUNT. A report the reader skipped and a stray report
    for an item the job never had would leave the count right and the list
    wrong.
    """
    wanted = [item.item_id for item in jobs.items(store, job.job_id)]
    if not wanted:
        # A JOB WITH NO ITEMS IS NOT A JOB WITH NOTHING MISSING. A build before
        # U57 queued intake jobs with no items, and one that was driven reads
        # succeeded over a listing nothing resolved; zero reports against zero
        # items would pass the comparison below and report a clean empty list.
        raise _unusable(
            f"job {job.job_id} has no items, so it never resolved a track; it was "
            f"queued by a build that did not record what its tracks were",
            "queue the playlist again and list the new job",
            job_id=job.job_id,
        )
    reports = artifacts.committed(intake_cli.ARTIFACTS, jobs.frozen_config(job), job.job_id)
    reported = [str(report.get("item_id")) for report in reports]
    if sorted(reported) != sorted(wanted):
        absent = sorted(set(wanted) - set(reported))
        raise _unusable(
            f"job {job.job_id} has {len(wanted)} item(s) and {len(reports)} readable "
            f"report(s), so a list from them would leave tracks out without saying so",
            "the reports under the job's artifacts folder are damaged or missing; "
            "queue the playlist again and list the new job",
            job_id=job.job_id,
            items=len(wanted),
            reports=len(reports),
            unreported=absent,
        )
    for report in reports:
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
            raise _unusable(
                f"the report for item {report.get('item_id')!r} of job {job.job_id} "
                f"does not say whether the track is missing, so the job cannot be listed",
                "queue the playlist again and list the new job",
                job_id=job.job_id,
                item_id=str(report.get("item_id")),
            )
    return reports


def job_reports(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """A finished intake job's committed reports, one per item, or the refusal.

    The public face of the reader above, for a verb that asks what a job's
    tracks resolved to without listing them. ``crate sync mark`` is the caller.
    """
    return _reports_or_refuse(store, job)


def _out_dir(ctx, subject: Mapping[str, Any]) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = intake_cli._load().paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
            **subject,
        )
    return out


def _changed_since(out: Path, name: str, rows) -> list[str]:
    """What an earlier list of this name names that ``rows`` do not, and the reverse.

    READ FROM THAT FILE, NOT INFERRED FROM THE JOB. A count of rows the library
    gained or a person answered since the job ran says nothing about when the
    earlier list was written, so a row gained before it and one answered after
    it read as the same story. The earlier file is the only witness to what it
    names. One this cannot read gives no reason rather than a wrong one.
    """
    try:
        body = json.loads((out / f"{name}{listdoc.LIST_SUFFIX}").read_text(encoding="utf-8"))
        earlier = {
            str(track["id"]): f"{track['artist']} - {track['title']}" for track in body["tracks"]
        }
    except (OSError, ValueError, KeyError, TypeError):
        return []
    now = {str(row.ref or "").strip(): f"{row.artist} - {row.title}" for row in rows}
    gone = [said for ref, said in earlier.items() if ref not in now]
    new = [said for ref, said in now.items() if ref not in earlier]
    why = []
    if gone:
        why.append(
            f"if it is this list's earlier copy: {len(gone)} track(s) it names are not "
            f"in this one, no longer missing since it was written: " + "; ".join(gone)
        )
    if new:
        why.append(
            f"if it is this list's earlier copy: {len(new)} track(s) this one names are "
            f"not in it, missing since it was written: " + "; ".join(new)
        )
    return why


def _written_or_refuse(out: Path, name: str, rows, provenance, subject, handed_on=()):
    """The emitter's write, with both of its failures as this verb's refusal.

    A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL, as it is
    ``label approved``'s. The emitter converts what it reads and lets a failed
    write through, and left alone that reaches a person as an internal error
    telling them to report a defect over a folder they cannot write to.

    A LIST THAT CHANGED IS REFUSED OVER ITS EARLIER COPY, since the name is
    fixed by the job, and without the change said the refusal reads as
    somebody else's file in the way. Rows the library gained since (R-502) and
    rows a person answered since (R-503) both change it.
    """
    try:
        return listdoc.write(out, name, rows, provenance, handed_on=handed_on)
    except listdoc.ListDocRefused as exc:
        why = _changed_since(out, name, rows)
        raise _unusable(
            str(exc),
            *why,
            "move the file aside or name another folder with --out",
            **subject,
        ) from exc
    except OSError as exc:
        raise _unusable(
            f"the list could not be written ({type(exc).__name__}: "
            f"{exc.strerror or exc}); nothing acquire download could read was left behind",
            "name another folder with --out, or make this one writable",
            path=str(exc.filename or ""),
            **subject,
        ) from exc


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"intake.missing.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _source_ref(job: jobs.Job) -> str | None:
    return str((job.payload or {}).get(intake_cli.SOURCE) or "") or None




def _isrc_of(wanted: match.Wanted) -> str:
    """The row's ISRC folded and NOT validated, so a malformed one is still
    named as malformed below rather than read as absent. One fold, the index's."""
    return match.fold_isrc(wanted.isrc)


def _ids_or_unnamed(code: str, tracks: tuple[Any, ...]) -> tuple[str, ...] | _Unnamed:
    """The distinct identifiers an answer holds, or why they cannot be trusted.

    A TRACK WITH NO IDENTIFIER IS NOT DROPPED. Dropped, an answer of one named
    track and one unnamed would read as one identifier and list a guess.
    """
    ids = [str(getattr(track, "id", "") or "").strip() for track in tracks]
    if any(not one for one in ids):
        return _Unnamed(
            UNREADABLE,
            f"the provider answered ISRC {code} with a track carrying no identifier, "
            f"so the answer cannot be read as one track",
        )
    return tuple(dict.fromkeys(ids))


def _catalogue_once(cfg=None) -> Callable[[], catalogue.Catalogue]:
    """A getter that resolves the catalogue on first use and once per run.

    LAZY, so a run with nothing to ask spends no login, and SHARED, so a list
    with rows to ask by ISRC and rows to search for restores one session and
    not two. Looked up on the module at call time, the contract
    ``label/catalogue.py`` states, which is what lets a suite substitute it.
    """
    held: list[catalogue.Catalogue] = []

    def get() -> catalogue.Catalogue:
        if not held:
            held.append(catalogue.resolve(cfg if cfg is not None else intake_cli._load()))
        return held[0]

    return get


def _named_by_isrc(
    wanted: list[match.Wanted], resolve: Callable[[], catalogue.Catalogue] | None = None
) -> list[str | _Unnamed]:
    """Each row's one provider identifier, or why the provider cannot name it.

    THE CATALOGUE IS RESOLVED ONLY WHEN A ROW CAN BE ASKED ABOUT, so a job whose
    rows all lack an ISRC spends no login and refuses over no missing
    credential. It is looked up on the module at call time, the contract
    ``label/catalogue.py`` states, which is what lets a suite substitute it.
    Every code is asked once, however many rows carry it, and every answer is
    in hand before the caller writes anything.
    """
    codes = [_isrc_of(one) for one in wanted]
    askable = list(dict.fromkeys(code for code in codes if match.isrc_token(code)))
    answers: dict[str, tuple[str, ...] | _Unnamed] = {}
    if askable:
        found = (resolve or _catalogue_once())()
        for code in askable:
            try:
                tracks = tuple(found.tracks_for_isrc(code))
            except CratekitError:
                raise
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                raise refuse(
                    "unavailable-transient",
                    f"the streaming provider could not answer for ISRC {code} ({exc}), "
                    f"so the missing tracks it would name cannot be sorted into listed "
                    f"and handed on; nothing was written",
                    remedy=Remedy.RETRY_LATER,
                    scope=Scope.RUN,
                    origin=("intake.missing",),
                    detail={"isrc": code},
                ) from exc
            answers[code] = _ids_or_unnamed(code, tracks)
    named: list[str | _Unnamed] = []
    for one, code in zip(wanted, codes, strict=True):
        answer = answers.get(code)
        if not code:
            named.append(
                _Unnamed(NO_ISRC, "it carries no ISRC, so the provider cannot be asked for it exactly")
            )
        elif answer is None:
            named.append(
                _Unnamed(
                    MALFORMED,
                    f"its ISRC {one.isrc!r} is not a well formed ISRC, so the provider was not asked",
                )
            )
        elif isinstance(answer, _Unnamed):
            named.append(answer)
        elif len(answer) == 1:
            named.append(answer[0])
        elif not answer:
            named.append(_Unnamed(UNKNOWN, f"the provider files no track under ISRC {code}"))
        else:
            # SORTED, so the order the provider happened to answer in never
            # changes the file's bytes and turns a repeat run into a refusal.
            named.append(
                _Unnamed(
                    SEVERAL,
                    f"the provider files {len(answer)} tracks under ISRC {code} "
                    f"({', '.join(sorted(answer))}), and which release to download is "
                    f"not something the ISRC decides",
                )
            )
    return named


def _run_jobs_or_refuse(
    store, run_id: str, *, skip_failed: bool
) -> tuple[list[jobs.Job], list[jobs.Job]]:
    """The run's finished intake jobs for THIS library, oldest first, and the skipped.

    THE LIBRARY AS WELL AS THE RUN. The queue is installation scoped, and a run
    identifier alone would list another library's jobs into this one's download.
    Oldest first, the identifier breaking a tie, so a second run writes the same
    bytes and is recognised as the same list rather than refused.
    """
    if not run_id.strip():
        # A BLANK RUN IS NOT A RUN. Compared as it stands it would match nothing
        # today, and a job queued with an empty run would be listed as a pass.
        raise _unusable(
            "--run was given no run identifier",
            "name the run a crate sync all pass printed",
            run_id=run_id,
        )
    library_id = intake_cli._load().library.volume_id
    found = sorted(
        (
            job
            for job in jobs.list_jobs(store)
            if job.handler_key in intake_cli.INTAKE_KEYS
            and (job.payload or {}).get(RUN_ID) == run_id
            and job.library_id == library_id
        ),
        key=lambda job: (job.created, job.job_id),
    )
    if not found:
        raise refuse(
            "job-unknown",
            f"no intake job queued for this library carries the run {run_id!r}, so "
            f"there is nothing to list for it",
            steps=(
                "name the run a crate sync all pass printed on this library",
                "a pass that queued no playlist has no intake jobs to list",
            ),
            origin=("intake.missing",),
            detail={"run_id": run_id, "library_id": library_id},
        )
    still_open = [job for job in found if job.is_open()]
    if still_open:
        # ONE OPEN JOB REFUSES THE RUN. A list of the finished ones would read as
        # the whole pass, and the open job's tracks would never be listed.
        raise _unusable(
            f"{len(still_open)} of the {len(found)} intake job(s) in run {run_id} "
            f"are still open, so a list of the rest would read as the whole pass: "
            + ", ".join(f"{job.job_id} ({job.state})" for job in still_open),
            *(f"finish job {job.job_id} with: crate {_resume_argv(job)}" for job in still_open),
            "then list the run again",
            run_id=run_id,
            open=[job.job_id for job in still_open],
        )
    unfinished = [job for job in found if job.state is not jobs.JobState.SUCCEEDED]
    if unfinished and not skip_failed:
        raise _unusable(
            f"{len(unfinished)} of the {len(found)} intake job(s) in run {run_id} "
            f"failed or were cancelled, so their tracks are unresolved and a list "
            f"without them would read as the whole pass: "
            + ", ".join(f"{job.job_id} ({job.state})" for job in unfinished),
            "pass --skip-failed to list the rest and name these as left out",
            "or queue those playlists again with crate sync all and list that run",
            inner=unfinished[0].cause,
            run_id=run_id,
            failed=[job.job_id for job in unfinished],
        )
    kept = [job for job in found if job.state is jobs.JobState.SUCCEEDED]
    if not kept:
        # EVERY JOB SKIPPED IS NOT NOTHING MISSING. A no-op here would read like
        # a pass where the library already held everything.
        raise _unusable(
            f"every intake job in run {run_id} failed or was cancelled, so no track "
            f"of the pass was resolved and there is nothing to list",
            "queue those playlists again with crate sync all and list that run",
            run_id=run_id,
            failed=[job.job_id for job in unfinished],
        )
    return kept, unfinished


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[jobs.Job]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance: the first job it came from, and every one.

    FIRST SOURCE WINS, as the list document's own row does, and the rest are
    kept rather than dropped, so a track two playlists share still says both.
    """
    first: dict[str, jobs.Job] = {}
    every: dict[str, list[str]] = {}
    for row, job in zip(rows, origins, strict=True):
        ref = str(row.ref or "").strip()
        if not ref:
            continue
        first.setdefault(ref, job)
        refs = every.setdefault(ref, [])
        said = _source_ref(job)
        if said is not None and said not in refs:
            refs.append(said)
    return {
        ref: listdoc.Provenance(
            source=PROVENANCE_SOURCE[job.handler_key],
            source_ref=_source_ref(job),
            source_refs=tuple(every[ref]),
        )
        for ref, job in first.items()
    }


def _answered(offered: list[dict[str, Any]]) -> list[bool]:
    """Whether each offered report's review item carries an answer now (R-503).

    BY THE KEY THE WORKER OFFERED IT UNDER. Every report the worker commits
    names the item it asked, ``review_item``, so the item is found by that
    identifier rather than by one rebuilt from a library that may have moved
    since. READ ONLY: an unanswered row is left exactly where it is, nothing is
    offered and the library is not walked, so a job whose questions nobody
    answered lists as it always did. A report naming no item has no answer
    that could reach it and stays offered. A store that cannot be read refuses,
    because it is not a store where nobody answered.
    """
    if not offered:
        return []
    with review.open_store(intake_cli._load()) as items:
        said = []
        for report in offered:
            item_id = str(report.get("review_item") or "").strip()
            held = review.find(items, item_id) if item_id else None
            said.append(held is not None and held.resolved)
    return said


def _asked_again(
    wanted: list[match.Wanted], origins: list[jobs.Job], subject: Mapping[str, Any]
) -> list[match.TrackMatch]:
    """What each row resolves to now, asked the way the worker asked it.

    THE WORKER'S CONSULT, NOT A SECOND OPINION. Each row is resolved as
    :func:`cratekit.intake.cli.resolve_track` resolves it: the library view
    ``match_cli.library_view`` builds, then a question the library raises goes
    through ``adjudicate``, so an answer a person already gave decides it.
    Without that step a row a person answered as a different track would read
    here as a fresh question and drop out of the list for ever. The library is
    walked once, however many jobs a run holds.

    THE LIBRARY AS IT IS NOW, not as the job froze it. The question is whether
    the library holds the track today, and a library whose root moved since the
    job was queued would otherwise refuse as unmounted while mounted, or answer
    from the old folder. ``--list`` and ``sync mark`` ask the same question the
    same way.

    AN ABSENT LIBRARY IS NOT AN EMPTY ONE. Every row would recheck missing and
    the list would read as asked again when it was not.

    Two kinds of row come here, and the caller counts them apart: a row the
    job found missing (R-502), and a row the job offered for review that a
    person has answered since (R-503). The second is decided by that answer
    exactly as the worker decides it, rejection and tombstone, a yes bound to
    the copy it was about, a yes about a copy that is gone still a question.
    """
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
            f"the job found missing, or a person answered since, can be asked "
            f"again whether it is held now; nothing was written",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=("intake.missing",),
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    now = [
        match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
        for one in wanted
    ]
    # BY THE JOB'S OWN VERB, since the review item is keyed by the handler that
    # asked it and the worker asked under the job's.
    asked: dict[str, list[int]] = {}
    for n, one in enumerate(now):
        if match_cli.touches_the_queue(one):
            asked.setdefault(origins[n].handler_key, []).append(n)
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
                answered = match_cli.adjudicate(
                    items,
                    match.MatchResult(matches=tuple(now[n] for n in at)),
                    handler_key=handler_key,
                    suppresses=suppresses,
                    suppression_id=identify,
                )
                for n, one in zip(at, answered.matches, strict=True):
                    now[n] = one
    return now


def _listed(
    ctx,
    found: list[tuple[jobs.Job, tuple[dict[str, Any], ...]]],
    *,
    name: str,
    subject: dict[str, Any],
    checks: list[dict[str, Any]],
    after: str = "",
    left_out: tuple[jobs.Job, ...] = (),
) -> Envelope:
    """Write one list from every missing report of ``found``, in order, and report it.

    ``subject`` identifies what was listed, a job or a run, on every refusal
    and at the head of the summary. ``checks`` are the caller's own rows,
    reported after the ones every listing carries. ``left_out`` are the jobs a
    run skipped, whose tracks nothing resolved.
    """
    counts = {word: 0 for word in _WORDS}
    # IN REPORT ORDER, missing and offered together, so a row a person answered
    # is listed where its playlist put it and a list's bytes do not depend on
    # which rows were answered first.
    rows_in: list[tuple[jobs.Job, dict[str, Any]]] = []
    for job, reports in found:
        for report in reports:
            counts[report["state"]] += 1
            if report["state"] in ("missing", "offered"):
                rows_in.append((job, report))
    offered = [report for _job, report in rows_in if report["state"] == "offered"]
    answered = iter(_answered(offered))
    # AN OFFERED ROW NOBODY ANSWERED IS NOT ASKED AGAIN. It stays offered on the
    # check it always had, and asking it would offer it again from here.
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
    missing = [intake_cli.thawed(report["track"]) for _job, report in asking]
    origins = [job for job, _report in asking]
    written = listdoc.Written(None, None, (), ())
    handed: list[tuple[listdoc.Row, match.Wanted, _Unnamed]] = []
    unwritable: list[tuple[listdoc.Row, _Unnamed]] = []
    by_isrc = 0
    since = dict.fromkeys(_SINCE.values(), 0)
    now_answered = dict.fromkeys(_ANSWERED.values(), 0)
    out: Path | None = None
    if missing:
        # THE FOLDER BEFORE THE LIBRARY WALK AND THE PROVIDER, so a bad --out
        # spends neither.
        out = _out_dir(ctx, subject)
        now = _asked_again(missing, origins, subject)
        kept: list[int] = []
        for n, (one, (_job, report)) in enumerate(zip(now, asking, strict=True)):
            if report["state"] == "offered":
                # COUNTED AS WHAT THE ANSWER MADE IT. A rejected row is missing
                # and an accepted one is owned, and the offered count is what is
                # still a question, which is what the check promises (R-503).
                now_answered[_ANSWERED[one.state]] += 1
                counts["offered"] -= 1
                counts[_WORD[one.state]] += 1
            elif one.state is not match.MatchState.MISSING:
                since[_SINCE[one.state]] += 1
            if one.state is match.MatchState.MISSING:
                kept.append(n)
        missing = [missing[n] for n in kept]
        origins = [origins[n] for n in kept]
        counts["missing"] = len(missing)
    gained = sum(since.values())
    if missing:
        rows = list(listdoc.rows_of(missing))
        bare = [n for n, row in enumerate(rows) if not str(row.ref or "").strip()]
        unnamed: set[int] = set()
        if bare:
            for n, answer in zip(bare, _named_by_isrc([missing[n] for n in bare]), strict=True):
                if isinstance(answer, _Unnamed):
                    unnamed.add(n)
                    handed.append((rows[n], missing[n], answer))
                else:
                    rows[n] = replace(rows[n], ref=answer)
                    by_isrc += 1
        kept = [n for n in range(len(rows)) if n not in unnamed]
        listed_rows = tuple(rows[n] for n in kept)
        writable = []
        for row, _wanted, why in handed:
            try:
                listdoc.text_line(row)
            except listdoc.ListDocRefused:
                # ONE ROW IS NOT THE LIST. Refusing here would withhold every
                # track the provider did name, on every run and in any folder,
                # so the row is named on its own failing check instead.
                unwritable.append((row, why))
                continue
            writable.append(listdoc.HandedOn(row, why.reason))
        written = _written_or_refuse(
            out,
            name,
            listed_rows,
            _provenance(listed_rows, [origins[n] for n in kept]),
            subject,
            handed_on=writable,
        )
    listed = len(written.listed)
    unlisted = len(handed)
    in_file = unlisted - len(unwritable)
    if missing and not listed and not in_file:
        # MISSING TRACKS AND NOTHING WRITTEN IS NOT NOTHING TO DO. Reported as a
        # no-op it would read, to a person and to a script, exactly like a job
        # where everything was owned, and the tracks would be dropped.
        raise _unusable(
            f"{unlisted} missing track(s), none the provider can name exactly and "
            f"none writable as an 'Artist - Title' line, so nothing was written",
            "find these tracks on the provider by hand, add them to a playlist, "
            "and run intake playlist on it",
            unlisted_tracks=[
                {"artist": row.artist, "title": row.title, "reason": why.reason}
                for row, why in unwritable
            ],
            **subject,
        )
    if left_out and not listed and not unlisted:
        # NOTHING LISTED WITH JOBS LEFT OUT IS NOT A PASS WITH NOTHING MISSING.
        # The skipped jobs' tracks were never resolved, and a no-op would tell a
        # person and a script that the pass needs no download.
        raise _unusable(
            f"nothing is missing from the job(s) that finished, and "
            f"{len(left_out)} job(s) that failed or were cancelled were left out "
            f"unresolved, so this is not a pass with nothing to download: "
            + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in left_out),
            "queue those playlists again with crate sync all and list that run",
            failed=[job.job_id for job in left_out],
            **subject,
        )
    command = (
        shlex.join(["crate", "acquire", "download", str(written.list_path)])
        if written.list_path is not None
        else None
    )
    # THE ROUTE, NOT THE SORT. ``match run`` sorts these rows into owned, review
    # and missing and stops, and a missing text row can never be downloaded, so
    # naming it here sent a person to a dead end (R-415). ``--list`` searches.
    handed_command = (
        shlex.join(["crate", "intake", "missing", "--list", str(written.unlisted_path)])
        if written.unlisted_path is not None
        else None
    )
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}{after}"
    elif in_file:
        said = (
            f"nothing listed for download: the missing tracks were handed on to "
            f"{written.unlisted_path}; next: {handed_command}"
        )
    elif gained:
        said = (
            f"nothing listed: every track this {'run' if 'run_id' in subject else 'job'} "
            f"found missing is in the library, deleted on purpose or offered for review since"
        )
    else:
        said = f"nothing listed: no track in this {'run' if 'run_id' in subject else 'job'} is missing"
    checks = [
        _check("written", "ok" if listed else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} offered for review and not listed until answered; "
            f"see: crate review list, then list this again",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _check(
            "answered",
            "info",
            f"{sum(now_answered.values())} track(s) offered for review when the job ran "
            f"were answered since, asked again now: {now_answered['answered_missing']} "
            f"missing, {now_answered['answered_owned']} in the library, "
            f"{now_answered['answered_suppressed']} deleted on purpose, "
            f"{now_answered['answered_offered']} still a question the answer did not settle",
        ),
        _check(
            "since",
            "info",
            f"{gained} track(s) missing when the job ran are not listed, asked again now: "
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
            f"deleted on purpose since, {since['offered_since']} held in another version "
            f"since and offered for review",
        ),
        _check(
            "isrc",
            "info",
            f"{by_isrc} missing track(s) with no provider identifier named by ISRC and listed",
        ),
        _check(
            "unlisted",
            "fail" if unlisted else "ok",
            f"{unlisted} missing track(s) the provider cannot name exactly are NOT in the "
            f"download list; {in_file} of them are in {written.unlisted_path} with the "
            f"reason, for: {handed_command}"
            if unlisted
            else "every missing track is in the list",
        ),
        _check(
            "unwritable",
            "fail" if unwritable else "ok",
            f"{len(unwritable)} of them cannot be written as an 'Artist - Title' line "
            f"and are in no file: "
            + "; ".join(f"{row.artist} - {row.title} ({why.reason})" for row, why in unwritable)
            if unwritable
            else "every track handed on is in the text list",
        ),
        *checks,
    ]
    summary = {
        **subject,
        "list": str(written.list_path) if written.list_path is not None else None,
        "manifest": str(written.manifest_path) if written.manifest_path is not None else None,
        "next": command,
        "written": listed,
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
        **since,
        **now_answered,
        "by_isrc": by_isrc,
        "unlisted": unlisted,
        "unlisted_list": (
            str(written.unlisted_path) if written.unlisted_path is not None else None
        ),
        "unlisted_next": handed_command,
        "unlisted_tracks": [
            {
                "artist": row.artist,
                "title": row.title,
                "isrc": wanted.isrc,
                "why": why.why,
                "reason": why.reason,
                "in_file": not any(row is gone for gone, _why in unwritable),
            }
            for row, wanted, why in handed
        ],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed or unlisted else Outcome.NO_OP,
    )


def provider_ref(wanted: match.Wanted) -> str:
    """The row's identifier if it is the PROVIDER'S, the rule ``listdoc`` writes by.

    Public since U80: ``acquire fallback`` asks the same question, so a row
    this verb would list by its id is never searched for on a second source.
    """
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""


def found_name(
    path: Path,
    rows: tuple[listdoc.Row, ...] = (),
    provenance: Mapping[str, listdoc.Provenance] | None = None,
) -> str:
    """The name of the list written from the text list at ``path``.

    The input's own name with its list suffix off, ``-found`` after it, and a
    digest of everything the emitter compares: the rows and their provenance,
    which carries the input's full path. ``intake-J.unlisted.json`` writes
    ``intake-J-found-<digest>.list.json`` beside the job's ``intake-J.list.json``
    and never onto it. A character a file name should not carry becomes a
    hyphen, and a name with nothing left is ``tracklist``.

    THE DIGEST IS WHAT LETS THE SECOND RUN HAPPEN. The emitter refuses a name
    whose file holds other bytes, and the run after a review answer lists MORE
    than the run before it, by design. Under a fixed name that run was refused
    until somebody moved a file by hand, which the unit's review drove. The
    same work still rewrites the same bytes under the same name, and two
    tracklists that share a file name in two folders take two names, since the
    provenance names the folder.
    """
    body, _listed, _unlisted = listdoc.document(rows)
    said = {
        "tracks": body["tracks"],
        "provenance": [
            dataclasses.asdict((provenance or {})[track["id"]]) for track in body["tracks"]
        ],
    }
    encoded = json.dumps(said, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.blake2s(encoded, digest_size=DIGEST_BYTES).hexdigest()
    stem = path.name
    for suffix in _LIST_SUFFIXES:
        if stem.lower().endswith(suffix) and len(stem) > len(suffix):
            stem = stem[: -len(suffix)]
            break
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.")
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"


def _searched(
    resolve: Callable[[], catalogue.Catalogue], wanted: list[match.Wanted]
) -> list[candidates.Answer]:
    """One search answer per row, every one in hand before anything is offered.

    THE CATALOGUE IS RESOLVED ONLY WHEN A ROW HAS TO BE SEARCHED FOR, looked up
    on the module at call time as ``_named_by_isrc`` does. A provider that could
    not answer refuses the whole verb, with no provider candidate offered and
    no file written: a partial pass would report the unasked rows as having no
    candidate. A version question the LIBRARY raised is already in the queue by
    then, so the sentence says which offers it means.
    """
    if not wanted:
        return []
    found = resolve()
    answers: list[candidates.Answer] = []
    for one in wanted:
        try:
            rows = tuple(found.search_tracks(one.artist, candidates.query_title(one)))
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
            raise refuse(
                "unavailable-transient",
                f"the streaming provider could not answer a search for "
                f"{one.artist} - {one.listed} ({exc}), so the missing tracks cannot "
                f"be sorted into listed and offered; no provider candidate was "
                f"offered and no list was written",
                remedy=Remedy.RETRY_LATER,
                steps=(
                    "run it again later",
                    "if the search for this one row fails on every run, take the "
                    "row out of the list and run it again, so the rest are not "
                    "held back by it",
                ),
                scope=Scope.RUN,
                origin=("intake.missing",),
                detail={"artist": one.artist, "title": one.listed},
            ) from exc
        answers.append(candidates.read_answer(one, rows))
    return answers


def _missing_for_list(ctx, given: str) -> Envelope:
    """List what a text list's missing rows can be named as, and offer the rest."""
    path = Path(given).expanduser().absolute()
    subject = {"list_in": str(path)}
    cfg = intake_cli._load()
    wanted = match_cli.read_list(path)
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        # AN ABSENT LIBRARY IS NOT AN EMPTY ONE. The index of a folder that is
        # not there holds nothing, every row would resolve missing, and this
        # verb would list for download every track the library already holds.
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no row of "
            f"the list can be told from a track the library already holds",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=("intake.missing",),
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    resolved = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
        with review.open_store(cfg) as items:
            resolved = match_cli.adjudicate(
                items,
                resolved,
                handler_key=ctx.entry.handler_key,
                suppresses=suppresses,
                suppression_id=identify,
            )
    counts = {word: 0 for word in _WORDS}
    missing: list[match.Wanted] = []
    seen: set[str] = set()
    for settled in resolved.matches:
        if settled.state is match.MatchState.MATCHED:
            counts["owned"] += 1
        elif settled.state is match.MatchState.NEEDS_REVIEW:
            counts["offered"] += 1
        elif settled.state is match.MatchState.SUPPRESSED:
            counts["suppressed"] += 1
        else:
            counts["missing"] += 1
            # THE SAME LINE TWICE IS ONE ROW, on the match identifier.
            if settled.match_id not in seen:
                seen.add(settled.match_id)
                missing.append(settled.wanted)

    named: list[match.Wanted] = []
    by_isrc = 0
    proposals: list[candidates.Proposal] = []
    out: Path | None = None
    if missing:
        # THE FOLDER BEFORE THE PROVIDER, so a bad --out spends no lookup.
        out = _out_dir(ctx, subject)
        # ONLY THE PROVIDER'S OWN IDENTIFIER NAMES A ROW, the emitter's rule. A
        # row of another service's list carries that service's id, the emitter
        # writes it with none, and sorted here by its ref it was in no file and
        # on no check, a missing track dropped at exit zero. It is bare.
        resolve = _catalogue_once(cfg)
        bare = [one for one in missing if not provider_ref(one)]
        named = [one for one in missing if provider_ref(one)]
        unnamed: list[match.Wanted] = []
        for one, answer in zip(bare, _named_by_isrc(bare, resolve), strict=True):
            if isinstance(answer, _Unnamed):
                unnamed.append(one)
            else:
                # THE ORIGIN WITH THE REF, or the emitter takes the ref off again.
                named.append(replace(one, ref=answer, origin=match.TIDAL))
                by_isrc += 1
        if unnamed:
            # THE QUEUE BEFORE THE PROVIDER, and every answer before any offer.
            # A row already answered, or already in front of a person, spends no
            # search, and a provider that fails part way leaves nothing offered.
            with review.open_store(cfg) as items:
                held = [candidates.settled(items, one) for one in unnamed]
            unasked = [one for one, said in zip(unnamed, held, strict=True) if said is None]
            answers = iter(_searched(resolve, unasked))
            with review.open_store(cfg) as items:
                for one, said in zip(unnamed, held, strict=True):
                    proposals.append(
                        said
                        if said is not None
                        else candidates.propose(
                            items, one, next(answers), handler_key=ctx.entry.handler_key
                        )
                    )

    for n, one in enumerate(proposals):
        if one.state not in candidates.NAMED or one.track is None:
            continue
        if one.state == candidates.ACCEPTED:
            # AN ACCEPTED CANDIDATE IS ASKED OF THE LIBRARY AS ITSELF. The row it
            # answers stays missing for ever when the candidate is another
            # spelling or another version of it, so without this every later run
            # of the same list would list, and download, the same track again.
            now = match.resolve_one(
                one.track, index, suppresses=suppresses, suppression_id=identify
            )
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n] = replace(one, state=candidates.HELD)
                continue
        named.append(one.track)

    written = listdoc.Written(None, None, (), ())
    if named:
        rows = listdoc.rows_of(named)
        provenance = {
            str(row.ref).strip(): listdoc.Provenance(source=LIST_SOURCE, source_ref=str(path))
            for row in rows
        }
        written = _written_or_refuse(
            out, found_name(path, rows, provenance), rows, provenance, subject
        )
    listed = len(written.listed)

    def of(*states: str) -> list[candidates.Proposal]:
        return [one for one in proposals if one.state in states]

    in_library = of(candidates.HELD)

    by_search = len(of(candidates.LISTED))
    by_review = len(of(candidates.ACCEPTED))
    asked = of(*candidates.ASKED)
    unfound = of(candidates.NO_CANDIDATES, candidates.REJECTED, candidates.STALLED)
    if unfound and not listed and not asked:
        # MISSING TRACKS, NOTHING WRITTEN AND NOTHING ASKED IS NOT NOTHING TO DO.
        # A no-op would read exactly like a list the library already holds.
        raise _unusable(
            f"{len(unfound)} missing track(s) and the provider has a route to none of "
            f"them, so nothing was written and nothing is waiting in review: "
            + "; ".join(f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}" for one in unfound),
            "find these tracks on the provider by hand, add them to a playlist, "
            "and run intake playlist on it",
            "a rejected or stalled row is asked again after: crate review clear ITEM_ID",
            tracks=[one.to_json() for one in unfound],
            **subject,
        )
    command = (
        shlex.join(["crate", "acquire", "download", str(written.list_path)])
        if written.list_path is not None
        else None
    )
    again = shlex.join(["crate", "intake", "missing", "--list", str(path)])
    review_command = f"crate review list --queue {candidates.QUEUE} --kind {candidates.KIND}"
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}"
    elif asked:
        said = (
            f"nothing listed yet: {len(asked)} row(s) are waiting in review; answer "
            f"them, then run: {again}"
        )
    else:
        said = "nothing listed: no track in this list is missing"
    checks = [
        _check("written", "ok" if listed else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"listed until answered; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _check(
            "isrc",
            "info",
            f"{by_isrc} missing track(s) with no provider identifier named by ISRC and listed",
        ),
        _check(
            "search",
            "info",
            f"{by_search} missing track(s) named by the one exact candidate a provider "
            f"search held, and listed",
        ),
        _check(
            "accepted",
            "info",
            f"{by_review} missing track(s) listed as the candidate accepted in review"
            + (
                f"; {len(in_library)} more accepted candidate(s) are already in the "
                f"library or were deleted on purpose, and are not listed again"
                if in_library
                else ""
            ),
        ),
        _check(
            "candidates",
            "fail" if asked else "ok",
            f"{len(asked)} missing track(s) have provider candidates and no exact one "
            f"to list, so they are offered for review and NOT in the list: "
            + "; ".join(f"{one.wanted.artist} - {one.wanted.listed} ({one.item_id})" for one in asked)
            + f"; see: {review_command}; then run: {again}"
            if asked
            else "no missing track is waiting on a provider candidate",
        ),
        _check(
            "unfound",
            "fail" if unfound else "ok",
            f"{len(unfound)} missing track(s) have no route to a download and are NOT "
            f"in the list: "
            + "; ".join(f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}" for one in unfound)
            if unfound
            else "every missing track is listed or waiting in review",
        ),
    ]
    summary = {
        **subject,
        "list": str(written.list_path) if written.list_path is not None else None,
        "manifest": str(written.manifest_path) if written.manifest_path is not None else None,
        "next": command,
        "written": listed,
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
        "by_isrc": by_isrc,
        "by_search": by_search,
        "by_review": by_review,
        "in_library": len(in_library),
        "candidates_offered": len(asked),
        "unfound": len(unfound),
        "review_next": review_command if asked else None,
        "rows": [one.to_json() for one in proposals],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
    )


def synced_name(run_id: str) -> str:
    """The pass a run's list and its landing's intake file share, colons removed."""
    return f"{land_cli.default_name(run_id)}{SYNCED_SUFFIX}"


def in_pass(job: jobs.Job, pass_name: str) -> bool:
    """Whether ``job`` was queued by the run the pass ``pass_name`` is named for.

    ONE COMPARISON FOR EVERY READER OF A PASS, ``sync mark`` and the landing's
    batch name (U110), made in the direction the name was built: the job's own
    run is spelled as a pass and compared, and nothing puts the colons back. A
    job queued by no run belongs to no pass.
    """
    run_id = str((job.payload or {}).get(RUN_ID) or "")
    return bool(run_id) and synced_name(run_id) == pass_name


def _missing_for_run(ctx, run_id: str) -> Envelope:
    with jobs.open_store() as store:
        kept, skipped = _run_jobs_or_refuse(
            store, run_id, skip_failed=bool(ctx.args.skip_failed)
        )
        found = [(job, _reports_or_refuse(store, job)) for job in kept]
    name = synced_name(run_id)
    checks = [
        _check(
            "jobs",
            "info",
            f"{len(kept)} finished intake job(s) of run {run_id} listed as one: "
            + ", ".join(job.job_id for job in kept),
        ),
        _check(
            "skipped",
            "fail" if skipped else "ok",
            f"{len(skipped)} job(s) failed or were cancelled and their tracks are NOT "
            f"in the list: "
            + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in skipped)
            if skipped
            else "every intake job in the run succeeded",
        ),
    ]
    return _listed(
        ctx,
        found,
        name=name,
        subject={
            "run_id": run_id,
            "jobs": [job.job_id for job in kept],
            "skipped": [job.job_id for job in skipped],
            "sources": [_source_ref(job) for job in kept],
            "land_name": name,
        },
        checks=checks,
        # TRUE ON BOTH MEDIA, AND READS NEITHER (R-770). The landing takes an
        # export on the xml bridge and refuses one on a native intake tree, so
        # a hint that always named --export sent a person on a cut over library
        # to a refusal. It says both rather than reading the switch, because a
        # hint must not be one more thing that can refuse a listing.
        # ``--pass`` AND NOT ``--name`` (U110). The pass names the intake file,
        # which is how ``sync mark`` finds this run's jobs, and the batch itself
        # is named for the date and the playlists, not for the run.
        after=(
            f"; land what it downloads as one batch with: crate intake land "
            f"--pass {name}, adding --export XML, a Fresh Export of the collection, "
            f"while the intake tree is on the xml bridge, and no export once the "
            f"intake tree is database native"
        ),
        left_out=tuple(skipped),
    )


def intake_missing(ctx) -> Envelope:
    """List the missing tracks of one finished intake job or one sync pass, or say why not."""
    if ctx.args.sync_run is not None:
        return _missing_for_run(ctx, str(ctx.args.sync_run))
    if ctx.args.text_list is not None:
        if ctx.args.skip_failed:
            raise _unusable(
                "--skip-failed leaves failed jobs out of a run's list and means "
                "nothing for a text list",
                "drop --skip-failed",
                list=str(ctx.args.text_list),
            )
        return _missing_for_list(ctx, str(ctx.args.text_list))
    if ctx.args.skip_failed:
        # A FLAG THAT WOULD MEAN NOTHING IS REFUSED, not ignored. One job that
        # failed is refused either way, and a person who asked to skip it would
        # otherwise read that refusal as the flag not working.
        raise _unusable(
            "--skip-failed leaves failed jobs out of a run's list and means nothing "
            "for one job",
            "drop --skip-failed, or list the whole pass with --run",
            job_id=str(ctx.args.job),
        )
    with jobs.open_store() as store:
        job = _finished_or_refuse(store, str(ctx.args.job))
        reports = _reports_or_refuse(store, job)
    return _listed(
        ctx,
        [(job, reports)],
        name=f"intake-{job.job_id}",
        subject={"job_id": job.job_id, "source": _source_ref(job)},
        checks=[],
    )


__all__ = [
    "DIGEST_BYTES",
    "FOUND_SUFFIX",
    "LISTS_DIR",
    "LIST_SOURCE",
    "MALFORMED",
    "NO_ISRC",
    "PROVENANCE_SOURCE",
    "RUN_ID",
    "SEVERAL",
    "SYNCED_SUFFIX",
    "UNKNOWN",
    "UNREADABLE",
    "build_missing",
    "found_name",
    "intake_missing",
    "job_reports",
    "provider_ref",
    "synced_name",
]
