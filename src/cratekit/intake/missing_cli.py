"""``intake.missing``: the list document for a finished playlist intake (R-400).

``intake playlist`` resolves every track and stops; this verb reads the
finished job's committed reports and hands the missing rows to the one emitter,
:func:`cratekit.acquire.listdoc.write`, so a person gets a file ``acquire
download`` accepts without retyping a track.

ONLY MISSING IS LISTED. An owned track is held, an offered one is a question
nobody answered, and a suppressed one was deleted on purpose; listing any of
those would spend a download on an answer nobody gave. A report's state was
fixed when the job ran, so each row is asked of the library again at listing
time (R-502), and an offered row a person has answered since is decided by that
answer as the worker would (R-503). A row a download already staged, found by
the ISRC the downloader writes, is not listed again and lands with the download
that staged it (U212); a staging folder that cannot be read is said, never read
as empty.

A PARTIAL LIST THAT READS AS COMPLETE IS THE DEFECT THIS FILE IS SHAPED
AGAINST. A job still open, failed or cancelled is refused. A succeeded job is
listed only when every item has exactly one readable report, compared by item
identifier and not by count, because ``artifacts.committed`` skips a report it
cannot parse. A missing row the provider cannot name is handed on to a text
list on a failing check, never dropped. A row with no provider identifier is
named by its ISRC when exactly one identifier answers it (U78, R-401), and a
provider that cannot answer refuses before anything is written.

``--run RUN_ID`` lists a whole ``crate sync all`` pass as one (U73): the intake
jobs carrying the run AND queued for this library, since the queue is
installation scoped. One open job refuses the run, a failed or cancelled one is
refused unless ``--skip-failed`` leaves it out on a failing check, and a track
two playlists share is one row whose manifest keeps both.

``--list PATH`` resolves a text list against the library first, names a row
still missing by ISRC or by the one exact candidate a search holds, and offers
the rest for review through :mod:`cratekit.intake.candidates`; nothing is ever
listed from a fuzzy score (U79, R-302).

Not gated and not destructive: :func:`listdoc.write` refuses rather than
replaces a file that holds anything else, and nothing here composes ``acquire
download``, so nothing here can spend a download.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import shlex
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import jobs, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import candidates, land_cli, landing
from cratekit.intake import cli as intake_cli

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: The payload key ``crate sync all`` stamps each job it queues with.
RUN_ID = "run_id"

_ORIGIN = ("intake.missing",)

#: What a run's list and its landing's intake file are named after the run, so
#: the list, the download and the landing read as one pass. ``land_name`` in the
#: listing's subject is this pass, handed to the landing as ``--pass``.
SYNCED_SUFFIX = "_synced"

#: What the provenance sidecar says a listed row came from, by the job's key.
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

#: The four words a committed intake report may carry. Any other is refused: a
#: state this verb cannot read is a track it cannot say is or is not missing.
_WORDS = frozenset({"owned", "offered", "suppressed", "missing"})

#: What a row its job resolved missing has become since, by the summary key it
#: is counted under. A row still missing has no key: it is listed as before.
_SINCE: Mapping[match.MatchState, str] = {
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
    match.MatchState.NEEDS_REVIEW: "offered_since",
}

#: What a row its job offered, and a person has answered since, is now (R-503).
_ANSWERED: Mapping[match.MatchState, str] = {
    match.MatchState.MISSING: "answered_missing",
    match.MatchState.MATCHED: "answered_owned",
    match.MatchState.SUPPRESSED: "answered_suppressed",
    match.MatchState.NEEDS_REVIEW: "answered_offered",
}

#: The report word each state the consult answers is counted under.
_WORD = {**match_cli.SETTLED_WORDS, match.MatchState.MISSING: "missing"}

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
        "--job", metavar="JOB_ID", help="the finished intake job whose missing tracks to list"
    )
    # ITS OWN DEST, NOT ``run``: the dispatcher's global ``--run`` reads
    # ``args.run`` and would hand a sync pass's identifier to the gate loader.
    chosen.add_argument(
        "--run", dest="sync_run", metavar="RUN_ID",
        help="the sync all pass whose intake jobs to list as one",
    )
    chosen.add_argument(
        "--list", dest="text_list", metavar="PATH",
        help="a text list, the unlisted list of an earlier run or any tracklist, "
        "whose missing tracks to find on the provider and list",
    )
    parser.add_argument(
        "--skip-failed", action="store_true", dest="skip_failed",
        help="with --run, leave out a job that failed or was cancelled and say so",
    )
    parser.add_argument(
        "--out", metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=intake_missing)


def _resume_argv(job: jobs.Job) -> str:
    resume = intake_cli.playlist_argv if job.handler_key == "intake.playlist" else intake_cli.set_argv
    return shlex.join(resume(job))


def _unusable(message: str, *steps: str, inner=None, **detail: Any):
    return refuse(
        "intake-list-unusable", message, steps=steps, origin=_ORIGIN, detail=detail, inner=inner
    )


def _finished_or_refuse(store, job_id: str) -> jobs.Job:
    """The job, if it is an intake job that ran every track to the end."""
    job = jobs.get(store, job_id)
    if job.handler_key not in intake_cli.INTAKE_KEYS:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not an "
            f"intake job, so there are no intake reports to list",
            steps=("name the job an intake playlist or intake set run printed",), origin=_ORIGIN,
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    if job.state is not jobs.JobState.SUCCEEDED:
        argv = _resume_argv(job)
        raise _unusable(
            f"job {job.job_id} is {job.state}, not succeeded, so some of its tracks "
            f"may not be resolved and a list of the rest would read as complete",
            f"finish it with: crate {argv}" if job.is_open() else
            "queue the playlist again, let it finish, then list that job",
            inner=job.cause, job_id=job.job_id, state=str(job.state),
        )
    return job


def _reports_or_refuse(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """One readable report per item, read with the configuration the job froze.

    BY IDENTIFIER, NOT BY COUNT: a skipped report and a stray one would leave
    the count right and the list wrong.
    """
    wanted = [item.item_id for item in jobs.items(store, job.job_id)]
    if not wanted:
        # A JOB WITH NO ITEMS IS NOT A JOB WITH NOTHING MISSING (pre U57 builds):
        # zero reports against zero items would pass the comparison below.
        raise _unusable(
            f"job {job.job_id} has no items, so it never resolved a track; it was "
            f"queued by a build that did not record what its tracks were",
            "queue the playlist again and list the new job", job_id=job.job_id,
        )
    reports = intake_cli.ARTIFACTS.committed(jobs.frozen_config(job), job.job_id)
    reported = [str(report.get("item_id")) for report in reports]
    if sorted(reported) != sorted(wanted):
        raise _unusable(
            f"job {job.job_id} has {len(wanted)} item(s) and {len(reports)} readable "
            f"report(s), so a list from them would leave tracks out without saying so",
            "the reports under the job's artifacts folder are damaged or missing; "
            "queue the playlist again and list the new job",
            job_id=job.job_id, items=len(wanted), reports=len(reports),
            unreported=sorted(set(wanted) - set(reported)),
        )
    for report in reports:
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
            raise _unusable(
                f"the report for item {report.get('item_id')!r} of job {job.job_id} "
                f"does not say whether the track is missing, so the job cannot be listed",
                "queue the playlist again and list the new job",
                job_id=job.job_id, item_id=str(report.get("item_id")),
            )
    return reports


def job_reports(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """A finished intake job's committed reports, one per item, or the refusal."""
    return _reports_or_refuse(store, job)


def _out_dir(ctx, subject: Mapping[str, Any]) -> Path:
    if ctx.args.out:
        out = Path(str(ctx.args.out)).expanduser().absolute()
    else:
        out = intake_cli._load().paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out", out=str(out), **subject,
        )
    return out


def _changed_since(out: Path, name: str, rows) -> list[str]:
    """What an earlier list of this name names that ``rows`` do not, and the reverse.

    READ FROM THAT FILE, NOT INFERRED FROM THE JOB: a count of rows gained or
    answered says nothing about when the earlier list was written. One this
    cannot read gives no reason rather than a wrong one.
    """
    try:
        body = json.loads((out / f"{name}{listdoc.LIST_SUFFIX}").read_text(encoding="utf-8"))
        earlier = {str(t["id"]): f"{t['artist']} - {t['title']}" for t in body["tracks"]}
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

    A folder that cannot be written is a refusal, not an internal error telling
    a person to report a defect. A list that changed is refused over its
    earlier copy, since the name is fixed, and the refusal says what changed so
    it does not read as somebody else's file in the way.
    """
    try:
        return listdoc.write(out, name, rows, provenance, handed_on=handed_on)
    except listdoc.ListDocRefused as exc:
        why = _changed_since(out, name, rows)
        raise _unusable(
            str(exc), *why, "move the file aside or name another folder with --out", **subject
        ) from exc
    except OSError as exc:
        raise _unusable(
            f"the list could not be written ({type(exc).__name__}: "
            f"{exc.strerror or exc}); nothing acquire download could read was left behind",
            "name another folder with --out, or make this one writable",
            path=str(exc.filename or ""), **subject,
        ) from exc


def _text(path) -> str | None:
    return str(path) if path is not None else None


def _command(*argv: str, path) -> str | None:
    return shlex.join(["crate", *argv, str(path)]) if path is not None else None


def _summary_head(subject, written: listdoc.Written, counts) -> dict[str, Any]:
    """The keys every listing's summary opens with, in their order."""
    head = {**subject, "list": _text(written.list_path), "manifest": _text(written.manifest_path)}
    head.update(next=_command("acquire", "download", path=written.list_path))
    head.update(written=len(written.listed))
    return head | {word: counts[word] for word in ("missing", "owned", "offered", "suppressed")}


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return dict(key=f"intake.missing.{key}", title=key, status=status, detail=detail, remedy=None)


def _isrc_check(by_isrc: int) -> dict[str, Any]:
    said = f"{by_isrc} missing track(s) with no provider identifier named by ISRC and listed"
    return _check("isrc", "info", said)



def _source_ref(job: jobs.Job) -> str | None:
    return str((job.payload or {}).get(intake_cli.SOURCE) or "") or None


def provider_ref(wanted: match.Wanted) -> str:
    """The row's identifier if it is the PROVIDER'S, the rule ``listdoc`` writes by.

    Public, so ``acquire fallback`` never searches a second source for a row
    this verb would list by its id.
    """
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""


def _ids_or_unnamed(code: str, tracks: tuple[Any, ...]) -> tuple[str, ...] | _Unnamed:
    """The distinct identifiers an answer holds, or why they cannot be trusted.

    A track with no identifier is not dropped, or one named and one unnamed
    would read as one identifier and list a guess.
    """
    ids = [str(getattr(track, "id", "") or "").strip() for track in tracks]
    if any(not one for one in ids):
        return _Unnamed(UNREADABLE, f"the provider answered ISRC {code} with a track carrying "
                        f"no identifier, so the answer cannot be read as one track")
    return tuple(dict.fromkeys(ids))


def _catalogue_once(cfg=None) -> Callable[[], catalogue.Catalogue]:
    """A getter that resolves the catalogue on first use and once per run.

    Lazy, so a run with nothing to ask spends no login, and looked up on the
    module at call time, as ``label/catalogue.py`` states, so a suite can
    substitute it.
    """
    held: list[catalogue.Catalogue] = []

    def get() -> catalogue.Catalogue:
        if not held:
            from cratekit.label import catalogue  # noqa: PLC0415 - labels is toggleable

            held.append(catalogue.resolve(cfg if cfg is not None else intake_cli._load()))
        return held[0]

    return get


def _named_by_isrc(
    wanted: list[match.Wanted], resolve: Callable[[], catalogue.Catalogue] | None = None
) -> list[str | _Unnamed]:
    """Each row's one provider identifier, or why the provider cannot name it.

    The catalogue is resolved only when a row can be asked about, so a job whose
    rows all lack an ISRC spends no login. Every code is asked once, and every
    answer is in hand before the caller writes anything. The ISRC is folded and
    not validated, so a malformed one is named as malformed rather than absent.
    """
    codes = [match.fold_isrc(one.isrc) for one in wanted]
    askable = list(dict.fromkeys(code for code in codes if match.isrc_token(code)))
    answers: dict[str, tuple[str, ...] | _Unnamed] = {}
    if askable:
        found = (resolve or _catalogue_once())()
        # THE CODES THE CATALOGUE FILES NOTHING UNDER, asked in batches first
        # (U207). Every other code is still asked alone, since a batch names one
        # release a code and the row is listed only when the code names one.
        found.screen_isrcs(askable)
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
                    remedy=Remedy.RETRY_LATER, scope=Scope.RUN, origin=_ORIGIN,
                    detail={"isrc": code},
                ) from exc
            answers[code] = _ids_or_unnamed(code, tracks)
    named: list[str | _Unnamed] = []
    for one, code in zip(wanted, codes, strict=True):
        answer = answers.get(code)
        if not code:
            answer = _Unnamed(
                NO_ISRC, "it carries no ISRC, so the provider cannot be asked for it exactly")
        elif answer is None:
            answer = _Unnamed(MALFORMED, f"its ISRC {one.isrc!r} is not a well formed ISRC, so "
                              f"the provider was not asked")
        elif isinstance(answer, _Unnamed):
            pass
        elif len(answer) == 1:
            answer = answer[0]
        elif not answer:
            answer = _Unnamed(UNKNOWN, f"the provider files no track under ISRC {code}")
        else:
            # SORTED, so the provider's order never changes the file's bytes and
            # turns a repeat run into a refusal.
            answer = _Unnamed(SEVERAL, f"the provider files {len(answer)} tracks under ISRC {code} "
                f"({', '.join(sorted(answer))}), and which release to download is "
                f"not something the ISRC decides")
        named.append(answer)
    return named


def _run_jobs_or_refuse(
    store, run_id: str, *, skip_failed: bool
) -> tuple[list[jobs.Job], list[jobs.Job]]:
    """The run's finished intake jobs for THIS library, oldest first, and the skipped.

    THE LIBRARY AS WELL AS THE RUN, since the queue is installation scoped.
    Oldest first, the identifier breaking a tie, so a second run writes the
    same bytes and is recognised rather than refused.
    """
    if not run_id.strip():
        # A BLANK RUN IS NOT A RUN: a job queued with an empty run would match.
        raise _unusable("--run was given no run identifier",
                        "name the run a crate sync all pass printed", run_id=run_id)
    library_id = intake_cli._load().library.volume_id
    found = sorted(
        (job for job in jobs.list_jobs(store)
            if job.handler_key in intake_cli.INTAKE_KEYS
            and (job.payload or {}).get(RUN_ID) == run_id
            and job.library_id == library_id),
        key=lambda job: (job.created, job.job_id),
    )
    if not found:
        raise refuse(
            "job-unknown",
            f"no intake job queued for this library carries the run {run_id!r}, so "
            f"there is nothing to list for it",
            steps=("name the run a crate sync all pass printed on this library",
                   "a pass that queued no playlist has no intake jobs to list"),
            origin=_ORIGIN, detail={"run_id": run_id, "library_id": library_id},
        )
    still_open = [job for job in found if job.is_open()]
    if still_open:
        # ONE OPEN JOB REFUSES THE RUN: the rest would read as the whole pass.
        raise _unusable(
            f"{len(still_open)} of the {len(found)} intake job(s) in run {run_id} "
            f"are still open, so a list of the rest would read as the whole pass: "
            + ", ".join(f"{job.job_id} ({job.state})" for job in still_open),
            *(f"finish job {job.job_id} with: crate {_resume_argv(job)}" for job in still_open),
            "then list the run again", run_id=run_id, open=[job.job_id for job in still_open],
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
            inner=unfinished[0].cause, run_id=run_id, failed=[job.job_id for job in unfinished],
        )
    kept = [job for job in found if job.state is jobs.JobState.SUCCEEDED]
    if not kept:
        # EVERY JOB SKIPPED IS NOT NOTHING MISSING, which a no-op would read as.
        raise _unusable(
            f"every intake job in run {run_id} failed or was cancelled, so no track "
            f"of the pass was resolved and there is nothing to list",
            "queue those playlists again with crate sync all and list that run",
            run_id=run_id, failed=[job.job_id for job in unfinished],
        )
    return kept, unfinished


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[jobs.Job]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance: the first job it came from, and every one.

    FIRST SOURCE WINS, as the list document's own row does, and the rest are
    kept, so a track two playlists share still says both.
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
        ref: listdoc.Provenance(source=PROVENANCE_SOURCE[job.handler_key],
                                source_ref=_source_ref(job), source_refs=tuple(every[ref]))
        for ref, job in first.items()
    }


def _answered(offered: list[dict[str, Any]]) -> list[bool]:
    """Whether each offered report's review item carries an answer now (R-503).

    By the ``review_item`` key the worker offered it under, not one rebuilt
    from a library that may have moved. READ ONLY: an unanswered row is left
    where it is. A report naming no item stays offered, and a store that cannot
    be read refuses, because it is not a store where nobody answered.
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

    THE WORKER'S CONSULT, NOT A SECOND OPINION: the library view, then
    ``adjudicate`` for a question the library raises, so an answer a person
    already gave decides it, a rejection, a yes bound to its copy, a yes about
    a copy that is gone still a question. THE LIBRARY AS IT IS NOW, not as the
    job froze it, since a moved root would otherwise refuse or answer from the
    old folder. AN ABSENT LIBRARY IS NOT AN EMPTY ONE: every row would recheck
    missing.
    """
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
            f"the job found missing, or a person answered since, can be asked "
            f"again whether it is held now; nothing was written",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME, origin=_ORIGIN,
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    now = [match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
           for one in wanted]
    # BY THE JOB'S OWN VERB, since the review item is keyed by the asking handler.
    asked: dict[str, list[int]] = {}
    for n, one in enumerate(now):
        if match_cli.touches_the_queue(one):
            asked.setdefault(origins[n].handler_key, []).append(n)
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
                answered = match_cli.adjudicate(
                    items, match.MatchResult(matches=tuple(now[n] for n in at)),
                    handler_key=handler_key, suppresses=suppresses, suppression_id=identify,
                )
                for n, one in zip(at, answered.matches, strict=True):
                    now[n] = one
    return now


@dataclass(frozen=True, slots=True)
class _Staged:
    """What the staging folder holds of the rows asked.

    ``found`` pairs each staged row's position with the file that carries it,
    ``unread`` says why the folder could not be read, and ``unasked`` why
    nothing was compared with it, so the row never reads as a look it did not take.
    """

    folder: Path
    found: tuple[tuple[int, Path], ...] = ()
    unread: str = ""
    unasked: str = ""


def _own_rows(out: Path, name: str) -> tuple[frozenset[str], frozenset[str]]:
    """The provider ids and ISRCs this list's own earlier copy names, or nothing.

    A row it names is this list's, and a continued pass finds that row's
    download staged because this list asked for it, so it is never counted as
    an earlier pass's. A copy that cannot be read claims nothing, and a shorter
    list is then refused over it by the emitter, loudly.
    """
    try:
        body = json.loads((out / f"{name}{listdoc.LIST_SUFFIX}").read_text(encoding="utf-8"))
        tracks = list(body["tracks"])
        ids = frozenset(str(track["id"]).strip() for track in tracks)
        isrcs = frozenset(match.isrc_token(track.get("isrc")) for track in tracks)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return frozenset(), frozenset()
    return ids - {""}, isrcs - {""}


def _staged(wanted: list[match.Wanted], *, out: Path, name: str) -> _Staged:
    """Which of ``wanted`` a file in the download staging folder already carries.

    ABSENCE OF A READ IS NOT A MATCH: a row with no ISRC asks nothing, and a file
    whose tag is absent, malformed or unreadable holds no identity, so the row
    stays listed and the worst case is the download it always was. A folder
    that is there and cannot be read is said by the caller, never read as empty.
    """
    cfg = intake_cli._load()
    folder = Path(cfg.paths.download_staging).expanduser().absolute()
    asked = [(n, match.isrc_token(one.isrc)) for n, one in enumerate(wanted)]
    asked = [(n, token) for n, token in asked if token]
    if not asked:
        return _Staged(folder, unasked="no missing track carries an ISRC, so none was compared "
                       "with the download staging folder")
    try:
        if not folder.exists():
            return _Staged(folder, unasked=f"the download staging folder {folder} is not there, "
                           f"so nothing is staged")
        files = landing.listing(folder)
    except OSError as exc:
        return _Staged(folder, unread=str(exc.strerror or exc))
    if not files:
        return _Staged(folder, unasked=f"the download staging folder {folder} holds no file a "
                       f"landing would take, so nothing is staged")
    ids, isrcs = _own_rows(out, name)
    index = match.index_paths(files, template=match_cli.library_template(cfg))
    found: list[tuple[int, Path]] = []
    for n, token in asked:
        ref = provider_ref(wanted[n])
        if (ref and ref in ids) or token in isrcs:
            continue
        held = index.held_by_isrc(token)
        if held:
            found.append((n, held[0].path))
    return _Staged(folder, tuple(found))


def _staged_check(staged: _Staged | None, rows: list[tuple[match.Wanted, Path]]) -> dict[str, Any]:
    """The row that says what the staging folder held of the missing tracks."""
    if staged is not None and staged.unread:
        return _check(
            "staged",
            "fail",
            f"the download staging folder {staged.folder} could not be read "
            f"({staged.unread}), so no missing track was checked against what is "
            f"staged there, and one staged already is listed and downloaded again",
        )
    if rows:
        return _check("staged", "info", f"{len(rows)} missing track(s) are staged already in "
            f"{staged.folder if staged else ''} by a download not landed yet, so they "
            f"are not listed or downloaded again, and land with the download that staged them: "
            + "; ".join(f"{one.artist} - {one.title} as {path.name}" for one, path in rows))

    if staged is None:
        return _check("staged", "info", "no track is missing, so none was asked whether it is staged")
    if staged.unasked:
        return _check("staged", "info", staged.unasked)
    return _check("staged", "info", f"no missing track is staged already in {staged.folder}")


@dataclass
class _Tally:
    """What one listing's steps found, carried to its report."""

    counts: dict[str, int]
    since: dict[str, int] = field(default_factory=lambda: dict.fromkeys(_SINCE.values(), 0))
    now_answered: dict = field(default_factory=lambda: dict.fromkeys(_ANSWERED.values(), 0))
    by_isrc: int = 0
    handed: list[tuple[listdoc.Row, match.Wanted, _Unnamed]] = field(default_factory=list)
    unwritable: list[tuple[listdoc.Row, _Unnamed]] = field(default_factory=list)
    staged: _Staged | None = None
    staged_rows: list[tuple[match.Wanted, Path]] = field(default_factory=list)
    written: listdoc.Written = listdoc.Written(None, None, (), ())


def _listed(ctx, found: list[tuple[jobs.Job, tuple[dict[str, Any], ...]]], *, name: str,
            subject: dict[str, Any], checks: list[dict[str, Any]], after: str = "",
            left_out: tuple[jobs.Job, ...] = ()) -> Envelope:
    """Write one list from every missing report of ``found``, in order, and report it.

    ``subject`` names what was listed, a job or a run, on every refusal and at
    the head of the summary. ``checks`` are the caller's own rows, reported
    after the shared ones. ``left_out`` are the jobs a run skipped.
    """
    counts = {word: 0 for word in _WORDS}
    # IN REPORT ORDER, missing and offered together, so a list's bytes do not
    # depend on which rows were answered first.
    rows_in: list[tuple[jobs.Job, dict[str, Any]]] = []
    for job, reports in found:
        for report in reports:
            counts[report["state"]] += 1
            if report["state"] in ("missing", "offered"):
                rows_in.append((job, report))
    offered = [report for _job, report in rows_in if report["state"] == "offered"]
    answered = iter(_answered(offered))
    # AN OFFERED ROW NOBODY ANSWERED IS NOT ASKED AGAIN, which would offer it again.
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
    missing = [intake_cli.thawed(report["track"]) for _job, report in asking]
    origins = [job for job, _report in asking]
    tally = _Tally(counts)
    since, now_answered = tally.since, tally.now_answered
    if missing:
        # THE FOLDER BEFORE THE LIBRARY WALK AND THE PROVIDER, so a bad --out
        # spends neither.
        out = _out_dir(ctx, subject)
        now = _asked_again(missing, origins, subject)
        kept: list[int] = []
        for n, (one, (_job, report)) in enumerate(zip(now, asking, strict=True)):
            if report["state"] == "offered":
                # COUNTED AS WHAT THE ANSWER MADE IT, so the offered count is
                # what is still a question, which the check promises.
                now_answered[_ANSWERED[one.state]] += 1
                counts["offered"] -= 1
                counts[_WORD[one.state]] += 1
            elif one.state is not match.MatchState.MISSING:
                since[_SINCE[one.state]] += 1
            if one.state is match.MatchState.MISSING:
                kept.append(n)
        missing = [missing[n] for n in kept]
        origins = [origins[n] for n in kept]
        # STAGED AFTER THE LIBRARY IS ASKED: a row the library holds now is
        # owned, whatever is staged. Nothing still missing asks nothing.
        staged = tally.staged = _staged(missing, out=out, name=name) if missing else None
        gone = {n for n, _path in staged.found} if staged else set()
        tally.staged_rows = [(missing[n], path) for n, path in staged.found] if staged else []
        missing = [one for n, one in enumerate(missing) if n not in gone]
        origins = [job for n, job in enumerate(origins) if n not in gone]
        counts["missing"] = len(missing)
    if missing:
        rows = list(listdoc.rows_of(missing))
        bare = [n for n, row in enumerate(rows) if not str(row.ref or "").strip()]
        unnamed: set[int] = set()
        for n, answer in zip(bare, _named_by_isrc([missing[n] for n in bare]), strict=True):
            if isinstance(answer, _Unnamed):
                unnamed.add(n)
                tally.handed.append((rows[n], missing[n], answer))
            else:
                rows[n] = replace(rows[n], ref=answer)
                tally.by_isrc += 1
        kept = [n for n in range(len(rows)) if n not in unnamed]
        listed_rows = tuple(rows[n] for n in kept)
        writable = []
        for row, _wanted, why in tally.handed:
            try:
                listdoc.text_line(row)
            except listdoc.ListDocRefused:
                # ONE ROW IS NOT THE LIST. Refusing would withhold every track
                # the provider did name, so the row has its own failing check.
                tally.unwritable.append((row, why))
                continue
            writable.append(listdoc.HandedOn(row, why.reason))
        provenance = _provenance(listed_rows, [origins[n] for n in kept])
        tally.written = _written_or_refuse(
            out, name, listed_rows, provenance, subject, handed_on=writable)
    return _listed_report(ctx, tally, missing, subject, checks, after, left_out)


def _listed_report(ctx, tally: _Tally, missing, subject, checks, after, left_out) -> Envelope:
    """The listing's refusals for nothing written, then its checks and summary."""
    counts, since, now_answered = tally.counts, tally.since, tally.now_answered
    staged, staged_rows, written = tally.staged, tally.staged_rows, tally.written
    handed, unwritable = tally.handed, tally.unwritable
    listed = len(written.listed)
    unlisted = len(handed)
    in_file = unlisted - len(unwritable)
    if missing and not listed and not in_file:
        # MISSING TRACKS AND NOTHING WRITTEN IS NOT NOTHING TO DO. A no-op would
        # read exactly like a job where everything was owned.
        raise _unusable(
            f"{unlisted} missing track(s), none the provider can name exactly and "
            f"none writable as an 'Artist - Title' line, so nothing was written",
            "find these tracks on the provider by hand, add them to a playlist, "
            "and run intake playlist on it",
            unlisted_tracks=[{"artist": row.artist, "title": row.title, "reason": why.reason}
                             for row, why in unwritable],
            **subject,
        )
    if left_out and not listed and not unlisted and not staged_rows:
        # NOTHING LISTED WITH JOBS LEFT OUT IS NOT A PASS WITH NOTHING MISSING:
        # the skipped jobs' tracks were never resolved.
        raise _unusable(
            f"nothing is missing from the job(s) that finished, and "
            f"{len(left_out)} job(s) that failed or were cancelled were left out "
            f"unresolved, so this is not a pass with nothing to download: "
            + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in left_out),
            "queue those playlists again with crate sync all and list that run",
            failed=[job.job_id for job in left_out], **subject,
        )
    command = _command("acquire", "download", path=written.list_path)
    # THE ROUTE, NOT THE SORT. ``match run`` stops at missing and a missing text
    # row can never be downloaded (R-415); ``--list`` searches.
    handed_command = _command("intake", "missing", "--list", path=written.unlisted_path)
    gained = sum(since.values())
    what = "run" if "run_id" in subject else "job"
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}{after}"
    elif in_file:
        said = (f"nothing listed for download: the missing tracks were handed on to "
                f"{written.unlisted_path}; next: {handed_command}")
    elif staged_rows:
        said = (f"nothing listed for download: the {len(staged_rows)} missing track(s) are "
                f"staged already in {staged.folder if staged else ''}, and land with the "
                f"download that staged them")
    elif gained:
        said = (
            f"nothing listed: every track this {what} found missing is in the library, "
            f"deleted on purpose or offered for review since"
        )
    else:
        said = f"nothing listed: no track in this {what} is missing"
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
        _check("answered", "info",
            f"{sum(now_answered.values())} track(s) offered for review when the job ran "
            f"were answered since, asked again now: {now_answered['answered_missing']} "
            f"missing, {now_answered['answered_owned']} in the library, "
            f"{now_answered['answered_suppressed']} deleted on purpose, "
            f"{now_answered['answered_offered']} still a question the answer did not settle",
        ),
        _check("since", "info",
            f"{gained} track(s) missing when the job ran are not listed, asked again now: "
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
            f"deleted on purpose since, {since['offered_since']} held in another version "
            f"since and offered for review",
        ),
        _staged_check(staged, staged_rows),
        _isrc_check(tally.by_isrc),
        _check(
            "unlisted",
            "fail" if unlisted else "ok",
            f"{unlisted} missing track(s) the provider cannot name exactly are NOT in the "
            f"download list; {in_file} of them are in {written.unlisted_path} with the "
            f"reason, for: {handed_command}" if unlisted else "every missing track is in the list",
        ),
        _check("unwritable", "fail" if unwritable else "ok",
            f"{len(unwritable)} of them cannot be written as an 'Artist - Title' line and are in "
            f"no file: " + "; ".join(f"{row.artist} - {row.title} ({why.reason})"
                                     for row, why in unwritable)
            if unwritable else "every track handed on is in the text list"),
        *checks,
    ]
    summary = {
        **_summary_head(subject, written, counts),
        **since,
        **now_answered,
        "by_isrc": tally.by_isrc,
        "staged": len(staged_rows),
        "staging": _text(staged.folder if staged is not None else None),
        "staged_tracks": [
            {"artist": wanted.artist, "title": wanted.title, "isrc": match.isrc_token(wanted.isrc),
             "ref": provider_ref(wanted), "file": str(path)}
            for wanted, path in staged_rows
        ],
        "unlisted": unlisted,
        "unlisted_list": _text(written.unlisted_path),
        "unlisted_next": handed_command,
        "unlisted_tracks": [
            {"artist": row.artist, "title": row.title, "isrc": wanted.isrc, "why": why.why,
             "reason": why.reason, "in_file": not any(row is gone for gone, _why in unwritable)}
            for row, wanted, why in handed
        ],
    }

    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        # EVERY ROW STAGED IS SOMETHING TO LAND, and a no-op would end a pass
        # before the landing that takes them.
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
    )


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

    THE DIGEST IS WHAT LETS THE SECOND RUN HAPPEN. The run after a review answer
    lists more by design, and under a fixed name the emitter refused it. The
    same work still rewrites the same bytes under the same name.
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


def _searched(resolve: Callable[[], catalogue.Catalogue], wanted: list[match.Wanted]) -> list:
    """One search answer per row, every one in hand before anything is offered.

    The catalogue is resolved only when a row has to be searched for. A provider
    that could not answer refuses the whole verb with nothing offered and no
    file written: a partial pass would report the unasked rows as candidateless.
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
                steps=("run it again later", "if the search for this one row fails on every run, "
                       "take the row out of the list and run it again, so the rest are not "
                       "held back by it"),
                scope=Scope.RUN, origin=_ORIGIN, detail={"artist": one.artist, "title": one.listed},
            ) from exc
        answers.append(candidates.read_answer(one, rows))
    return answers


def _resolved(ctx, cfg, path: Path, subject: Mapping[str, Any]):
    """The list's counts, its distinct missing rows, and the library view it was read by."""
    wanted = match_cli.read_list(path)
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        # AN ABSENT LIBRARY IS NOT AN EMPTY ONE: every row would resolve missing
        # and be listed for download, held or not.
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no row of "
            f"the list can be told from a track the library already holds",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME, origin=_ORIGIN,
            detail={"music": str(music), **subject},
        )
    view = match_cli.library_view(cfg)
    index, suppresses, identify = view
    resolved = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
        with review.open_store(cfg) as items:
            resolved = match_cli.adjudicate(items, resolved, handler_key=ctx.entry.handler_key,
                                            suppresses=suppresses, suppression_id=identify)
    counts = {word: 0 for word in _WORDS}
    missing: list[match.Wanted] = []
    seen: set[str] = set()
    for settled in resolved.matches:
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None:
            counts[word] += 1
        else:
            counts["missing"] += 1
            # THE SAME LINE TWICE IS ONE ROW, on the match identifier.
            if settled.match_id not in seen:
                seen.add(settled.match_id)
                missing.append(settled.wanted)
    return counts, missing, view


def _held_since(proposals: list[candidates.Proposal], named: list[match.Wanted], view) -> None:
    """Add each named proposal's track to ``named``, unless the library holds it now."""
    index, suppresses, identify = view
    for n, one in enumerate(proposals):
        if one.state not in candidates.NAMED or one.track is None:
            continue
        if one.state == candidates.ACCEPTED:
            # AN ACCEPTED CANDIDATE IS ASKED OF THE LIBRARY AS ITSELF. The row it
            # answers stays missing when the candidate is another spelling or
            # version, so every later run would download the same track again.
            now = match.resolve_one(
                one.track, index, suppresses=suppresses, suppression_id=identify)
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n] = replace(one, state=candidates.HELD)
                continue
        named.append(one.track)


def _missing_for_list(ctx, given: str) -> Envelope:
    """List what a text list's missing rows can be named as, and offer the rest."""
    path = Path(given).expanduser().absolute()
    subject = {"list_in": str(path)}
    cfg = intake_cli._load()
    counts, missing, view = _resolved(ctx, cfg, path, subject)
    named: list[match.Wanted] = []
    by_isrc = 0
    proposals: list[candidates.Proposal] = []
    out: Path | None = None
    if missing:
        # THE FOLDER BEFORE THE PROVIDER, so a bad --out spends no lookup.
        out = _out_dir(ctx, subject)
        # ONLY THE PROVIDER'S OWN IDENTIFIER NAMES A ROW, the emitter's rule: a
        # row carrying another service's id is written with none, so it is bare.
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
            # THE QUEUE BEFORE THE PROVIDER, and every answer before any offer: a
            # row already answered or in front of a person spends no search, and
            # a provider failing part way leaves nothing offered.
            with review.open_store(cfg) as items:
                held = [candidates.settled(items, one) for one in unnamed]
            unasked = [one for one, said in zip(unnamed, held, strict=True) if said is None]
            answers = iter(_searched(resolve, unasked))
            with review.open_store(cfg) as items:
                for one, said in zip(unnamed, held, strict=True):
                    proposals.append(said if said is not None else candidates.propose(
                        items, one, next(answers), handler_key=ctx.entry.handler_key))

    _held_since(proposals, named, view)
    written = listdoc.Written(None, None, (), ())
    if named:
        rows = listdoc.rows_of(named)
        provenance = {str(row.ref).strip(): listdoc.Provenance(source=LIST_SOURCE,
                      source_ref=str(path)) for row in rows}
        written = _written_or_refuse(out, found_name(path, rows, provenance), rows, provenance,
                                     subject)
    return _found_report(ctx, path, subject, counts, by_isrc, proposals, written)


def _found_report(ctx, path, subject, counts, by_isrc, proposals, written) -> Envelope:
    """The ``--list`` refusal for nothing routed, then its checks and summary."""
    listed = len(written.listed)

    def of(*states: str) -> list[candidates.Proposal]:
        return [one for one in proposals if one.state in states]

    in_library = of(candidates.HELD)
    by_search = len(of(candidates.LISTED))
    by_review = len(of(candidates.ACCEPTED))
    asked = of(*candidates.ASKED)
    unfound = of(candidates.NO_CANDIDATES, candidates.REJECTED, candidates.STALLED)
    unfound_said = "; ".join(f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}"
                             for one in unfound)
    if unfound and not listed and not asked:
        # MISSING TRACKS, NOTHING WRITTEN AND NOTHING ASKED IS NOT NOTHING TO DO.
        raise _unusable(
            f"{len(unfound)} missing track(s) and the provider has a route to none of "
            f"them, so nothing was written and nothing is waiting in review: " + unfound_said,
            "find these tracks on the provider by hand, add them to a playlist, "
            "and run intake playlist on it",
            "a rejected or stalled row is asked again after: crate review clear ITEM_ID",
            tracks=[one.to_json() for one in unfound], **subject,
        )
    command = _command("acquire", "download", path=written.list_path)
    again = _command("intake", "missing", "--list", path=path)
    review_command = f"crate review list --queue {candidates.QUEUE} --kind {candidates.KIND}"
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}"
    elif asked:
        said = f"nothing listed yet: {len(asked)} row(s) are waiting in review; answer them, " \
            f"then run: {again}"
    else:
        said = "nothing listed: no track in this list is missing"
    checks = [
        _check("written", "ok" if listed else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check("offered", "info", f"{counts['offered']} held in another version, offered for "
               f"review and not listed until answered; see: crate review list"),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _isrc_check(by_isrc),
        _check("search", "info", f"{by_search} missing track(s) named by the one exact candidate "
               f"a provider search held, and listed"),
        _check("accepted", "info",
               f"{by_review} missing track(s) listed as the candidate accepted in review"
               + (f"; {len(in_library)} more accepted candidate(s) are already in the library "
                  f"or were deleted on purpose, and are not listed again" if in_library else "")),
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
        _check("unfound", "fail" if unfound else "ok",
               f"{len(unfound)} missing track(s) have no route to a download and are NOT in the "
               f"list: " + unfound_said if unfound
               else "every missing track is listed or waiting in review"),
    ]
    summary = {
        **_summary_head(subject, written, counts), "by_isrc": by_isrc, "by_search": by_search,
        "by_review": by_review, "in_library": len(in_library), "candidates_offered": len(asked),
        "unfound": len(unfound), "review_next": review_command if asked else None,
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

    ONE COMPARISON FOR EVERY READER OF A PASS (U110), made in the direction the
    name was built, so nothing puts the colons back. No run is no pass.
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
        _check("jobs", "info", f"{len(kept)} finished intake job(s) of run {run_id} listed as "
               "one: " + ", ".join(job.job_id for job in kept)),
        _check("skipped", "fail" if skipped else "ok",
               f"{len(skipped)} job(s) failed or were cancelled and their tracks are NOT in the "
               "list: " + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in skipped)
               if skipped else "every intake job in the run succeeded"),
    ]
    subject = {"run_id": run_id, "jobs": [job.job_id for job in kept],
               "skipped": [job.job_id for job in skipped],
               "sources": [_source_ref(job) for job in kept], "land_name": name}
    return _listed(
        ctx, found, name=name, subject=subject, checks=checks,
        # TRUE ON BOTH MEDIA, AND READS NEITHER (R-770): a hint must not be one
        # more thing that can refuse a listing. ``--pass``, not ``--name``
        # (U110): the pass names the intake file ``sync mark`` finds jobs by.
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
            raise _unusable("--skip-failed leaves failed jobs out of a run's list and means "
                            "nothing for a text list", "drop --skip-failed",
                            list=str(ctx.args.text_list))
        return _missing_for_list(ctx, str(ctx.args.text_list))
    if ctx.args.skip_failed:
        # A FLAG THAT WOULD MEAN NOTHING IS REFUSED, not ignored, or a failed
        # job's refusal would read as the flag not working.
        raise _unusable(
            "--skip-failed leaves failed jobs out of a run's list and means nothing "
            "for one job",
            "drop --skip-failed, or list the whole pass with --run", job_id=str(ctx.args.job),
        )
    with jobs.open_store() as store:
        job = _finished_or_refuse(store, str(ctx.args.job))
        reports = _reports_or_refuse(store, job)
    subject = {"job_id": job.job_id, "source": _source_ref(job)}
    return _listed(ctx, [(job, reports)], name=f"intake-{job.job_id}", subject=subject, checks=[])


__all__ = [
    "LISTS_DIR", "LIST_SOURCE", "MALFORMED", "NO_ISRC", "RUN_ID", "SEVERAL", "SYNCED_SUFFIX",
    "UNKNOWN", "UNREADABLE", "build_missing", "found_name", "intake_missing", "job_reports",
    "provider_ref", "synced_name",
]

