"""The list of a finished intake job or a sync pass, step by step.

MISSING WHEN THE JOB RAN IS ASKED AGAIN AT LISTING TIME (R-502). Each missing
row is asked of the library as it is now, through the consult the worker
used, and a row now held, deleted on purpose or a question is counted under
``since`` and not listed. The reports are not rewritten.

AN OFFERED ROW IS LISTABLE ONCE IT IS ANSWERED (R-503). Its review item is
looked up read only by the identifier its report names; an unanswered row
stays offered, and an answered one goes through the same consult, so the
answer decides it as the worker would.

A TRACK ALREADY STAGED IS NOT LISTED AGAIN (U212). A row still missing is
asked of the files a landing would take from the staging folder, by the ISRC
the downloader writes, and a row a staged file carries lands with the download
that staged it. A file whose ISRC cannot be read matches nothing, a row this
list's own earlier copy names is never subtracted, and a folder that cannot be
read is said on a failing row, never read as empty.

A shorter or longer list than an earlier copy of the same name is refused by
the emitter, and the refusal says what changed.
"""

from __future__ import annotations

import json
import shlex
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import jobs, review
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import cli as intake_cli
from cratekit.intake import landing
from cratekit.intake.missing_common import (
    _WORDS,
    _check,
    _download_command,
    _isrc_check,
    _named_by_isrc,
    _out_dir,
    _summary_head,
    _Unnamed,
    _unusable,
    _written_or_refuse,
    provider_ref,
)

#: What the provenance sidecar says a listed row came from, by the job's key.
PROVENANCE_SOURCE: Mapping[str, str] = {"intake.playlist": "playlist", "intake.set": "set"}

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
        return _Staged(
            folder,
            unasked="no missing track carries an ISRC, so none was compared with the "
            "download staging folder",
        )
    try:
        if not folder.exists():
            return _Staged(
                folder,
                unasked=f"the download staging folder {folder} is not there, so nothing is staged",
            )
        files = landing.listing(folder)
    except OSError as exc:
        return _Staged(folder, unread=str(exc.strerror or exc))
    if not files:
        return _Staged(
            folder,
            unasked=f"the download staging folder {folder} holds no file a landing "
            f"would take, so nothing is staged",
        )
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
        return _check(
            "staged",
            "info",
            f"{len(rows)} missing track(s) are staged already in "
            f"{staged.folder if staged else ''} by a download not landed yet, so they "
            f"are not listed or downloaded again, and land with the download that "
            f"staged them: "
            + "; ".join(f"{one.artist} - {one.title} as {path.name}" for one, path in rows),
        )
    if staged is None:
        return _check("staged", "info", "no track is missing, so none was asked whether it is staged")
    if staged.unasked:
        return _check("staged", "info", staged.unasked)
    return _check("staged", "info", f"no missing track is staged already in {staged.folder}")


def _source_ref(job: jobs.Job) -> str | None:
    return str((job.payload or {}).get(intake_cli.SOURCE) or "") or None


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
        ref: listdoc.Provenance(
            source=PROVENANCE_SOURCE[job.handler_key],
            source_ref=_source_ref(job),
            source_refs=tuple(every[ref]),
        )
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
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=("intake.missing",),
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    now = [
        match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
        for one in wanted
    ]
    # BY THE JOB'S OWN VERB, since the review item is keyed by the asking handler.
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


@dataclass
class _Tally:
    """What one listing's steps found, carried to its report."""

    counts: dict[str, int]
    since: dict[str, int] = field(default_factory=lambda: dict.fromkeys(_SINCE.values(), 0))
    now_answered: dict[str, int] = field(
        default_factory=lambda: dict.fromkeys(_ANSWERED.values(), 0)
    )
    by_isrc: int = 0
    handed: list[tuple[listdoc.Row, match.Wanted, _Unnamed]] = field(default_factory=list)
    unwritable: list[tuple[listdoc.Row, _Unnamed]] = field(default_factory=list)
    staged: _Staged | None = None
    staged_rows: list[tuple[match.Wanted, Path]] = field(default_factory=list)
    written: listdoc.Written = listdoc.Written(None, None, (), ())


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
        tally.written = _written_or_refuse(
            out,
            name,
            listed_rows,
            _provenance(listed_rows, [origins[n] for n in kept]),
            subject,
            handed_on=writable,
        )
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
            unlisted_tracks=[
                {"artist": row.artist, "title": row.title, "reason": why.reason}
                for row, why in unwritable
            ],
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
            failed=[job.job_id for job in left_out],
            **subject,
        )
    command = _download_command(written)
    # THE ROUTE, NOT THE SORT. ``match run`` stops at missing and a missing text
    # row can never be downloaded (R-415); ``--list`` searches.
    handed_command = (
        shlex.join(["crate", "intake", "missing", "--list", str(written.unlisted_path)])
        if written.unlisted_path is not None
        else None
    )
    gained = sum(since.values())
    what = "run" if "run_id" in subject else "job"
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}{after}"
    elif in_file:
        said = (
            f"nothing listed for download: the missing tracks were handed on to "
            f"{written.unlisted_path}; next: {handed_command}"
        )
    elif staged_rows:
        said = (
            f"nothing listed for download: the {len(staged_rows)} missing track(s) "
            f"are staged already in {staged.folder if staged else ''}, and land with "
            f"the download that staged them"
        )
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
        _staged_check(staged, staged_rows),
        _isrc_check(tally.by_isrc),
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
        **_summary_head(subject, written, counts),
        **since,
        **now_answered,
        "by_isrc": tally.by_isrc,
        "staged": len(staged_rows),
        "staging": str(staged.folder) if staged is not None else None,
        "staged_tracks": [
            {
                "artist": wanted.artist,
                "title": wanted.title,
                "isrc": match.isrc_token(wanted.isrc),
                "ref": provider_ref(wanted),
                "file": str(path),
            }
            for wanted, path in staged_rows
        ],
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
        # EVERY ROW STAGED IS SOMETHING TO LAND, and a no-op would end a pass
        # before the landing that takes them.
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
    )
