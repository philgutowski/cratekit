"""The recording ``intake set`` and ``intake identify`` hear, and the tracklist they write.

A recording on this machine is lent as it is; a mix URL is fetched into a
scratch folder for the pass and removed after (U104). Both verbs write one
tracklist by one writer (R-925), and every note they add rides the envelope's
warnings channel, the one a person is shown. :mod:`cratekit.intake.cli`
re-exports every name a caller or test reads there.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import binaries, binary_refusal, config
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import fetch, normalize, pipeline, recognize
from cratekit.intake.cli_listing import _load, _unusable

#: The folder under download staging a tracklist lands in when ``--out`` is
#: not given, and what its file name ends in: 'Artist - Title' lines, the door
#: ``acquire match`` and ``intake missing --list`` both read.
TRACKLISTS_DIR = "tracklists"
TRACKLIST_SUFFIX = ".tracklist.txt"

#: How much of the recording's digest a tracklist's name carries: forty eight
#: bits, which no two sets a person owns will share.
TRACKLIST_DIGEST_CHARS = 12

#: The notes identification adds on the warnings channel, since the ``match``
#: surface is closed at three arrays and has no field for the file written.
TRACKLIST_WRITTEN = "tracklist-written"
#: The ``progress`` field ``intake set`` names its tracklist under (R-925).
TRACKLIST = "tracklist"
#: ``intake set``'s note when its job is queued and its tracklist was not written.
TRACKLIST_UNWRITTEN = "tracklist-unwritten"
CACHE_UNWRITTEN = "recognition-cache-unwritten"
CACHE_SERVED = "recognition-cached"
#: A set longer than one run's bound was identified in even parts and is still
#: one set: one tracklist, one job, one batch (R-706).
IN_PARTS = "recognition-in-parts"
MIX_SCRATCH_LEFT = "mix-scratch-left"


def _note(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def _recording_or_refuse(source: str) -> Path:
    """The recording as a file on this machine, absolute, or why not.

    Expanded before it is checked, since an unexpanded tilde is the input the
    expansion exists for. Absolute, because the child a resume spawns inherits
    the resuming process's directory.
    """
    path = Path(source).expanduser()
    if not path.is_file():
        raise _unusable(
            f"{source} is not a file on this machine",
            source=source,
        )
    return path.absolute()


def _local_or_none(source: str) -> Path | None:
    """The recording when ``source`` is a path, and None when it is a mix URL.

    A path naming nothing is refused here, before the gate; an address costs a
    download, so it waits until every free refusal has had its turn.
    """
    if normalize.is_url(source):
        return None
    return _recording_or_refuse(source)


@dataclass(slots=True)
class SetRecording:
    """The file a pass identifies, and what the pass calls it.

    ``ref`` is what is frozen, reported and shown: the absolute path of a local
    recording, or the ADDRESS of a fetched one, whose file is gone by the time
    anybody reads the job. ``stem`` names a tracklist and ``shown`` is the
    short name a sentence uses. ``leftover`` is a scratch folder that could
    not be removed. One object, so no helper can fall back to the scratch
    file's name when a caller forgets the address.
    """

    path: Path
    ref: str
    stem: str
    shown: str
    leftover: str | None = None
    #: What the page said, for a fetched mix (U121). Empty for a local file.
    page: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def local(cls, path: Path) -> SetRecording:
        return cls(path=path, ref=str(path), stem=path.stem, shown=path.name)


def _fetch_notes(held: SetRecording) -> tuple[dict[str, str], ...]:
    """A scratch folder that outlived its pass, said where a person reads it."""
    if held.leftover is None:
        return ()
    return (
        _note(
            MIX_SCRATCH_LEFT,
            f"the fetched mix could not be removed from {held.leftover}; it is "
            f"outside the library and is cleared the next time this address is "
            f"fetched, or delete the folder by hand",
        ),
    )


@contextmanager
def _recording(
    cfg: config.Config,
    source: str,
    local: Path | None,
    progress: fetch.Progress | None = None,
) -> Iterator[SetRecording]:
    """Lend the recording for one pass, fetching it first when it is a mix URL.

    A mix URL is fetched into a scratch folder under the state root, removed
    when the block ends however it ends, and refused before anything is
    fetched when that folder resolves under the library: a mix never lands
    beside the music. ``progress`` is told the fetch's steps (R-924).
    """
    if local is not None:
        yield SetRecording.local(local)
        return
    address = source.strip()
    try:
        found = fetch.fetcher()
    except binaries.BinaryNotFound as exc:
        raise binary_refusal.yt_dlp_missing(
            exc,
            {"source": address},
            said="Fetching a mix runs it, so nothing was fetched and nothing was sent.",
            origin=("intake.cli",),
        ) from exc
    try:
        with fetch.fetched(address, Path(cfg.library.root), found, progress=progress) as got:
            held = SetRecording(
                path=got.path,
                ref=address,
                stem=fetch.stem_of(address),
                shown=address,
                page=dict(got.page),
            )
            try:
                yield held
            except CratekitError as exc:
                raise _named_for_the_address(exc, held) from exc.__cause__
        held.leftover = got.leftover
    except fetch.ScratchUnderLibrary as exc:
        raise _unusable(
            f"the scratch folder a fetched mix lands in, {exc.scratch}, is inside "
            f"this library at {exc.library}, and a mix is never written under the "
            f"library; nothing was fetched",
            f"point {config.ENV_STATE_DIR} outside the library, or unset it",
            source=address,
            scratch=str(exc.scratch),
        ) from exc
    except fetch.ScratchUnusable as exc:
        raise _unusable(
            f"{exc}, so the mix at {address} was not fetched; nothing was sent",
            f"make that folder writable, or point {config.ENV_STATE_DIR} somewhere that is",
            source=address,
        ) from exc
    except fetch.SetFetchTimedOut as exc:
        # The one fetch failure known to be worth a retry; nothing else is
        # called retryable, or a driver would re-run a dead address for ever.
        raise refuse(
            "unavailable-transient",
            f"the mix at {address} could not be fetched ({exc}); nothing was sent "
            f"and nothing was kept",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            steps=(
                "run it again later",
                "or download the mix to a file yourself and run it on that file",
            ),
            origin=("intake.cli",),
            detail={"source": address},
        ) from exc
    except fetch.SeveralRecordings as exc:
        raise _unusable(
            f"{address} was not fetched: {exc}; nothing was sent and nothing was kept",
            "give the address of one recording on that page",
            source=address,
        ) from exc
    except fetch.SetFetchFailed as exc:
        raise _unusable(
            f"the mix at {address} could not be fetched ({exc}); nothing was sent "
            f"and nothing was kept. Whether the address or the network is at fault "
            f"is not known from a failed download",
            "open the address in a browser to check it still plays, then run it again",
            "a streaming playlist goes through intake playlist instead",
            "or download the mix to a file yourself and run it on that file",
            source=address,
        ) from exc


def _named_for_the_address(exc: CratekitError, held: SetRecording) -> CratekitError:
    """A refusal raised over a fetched mix, said about the ADDRESS.

    The identifier names the scratch file it was handed, removed before
    anybody reads the refusal, and some refusals follow paid calls, so the
    address replaces it in the message and the detail; the rest is kept.
    """
    cause = exc.declared_cause
    message = cause.message.replace(str(held.path), held.ref).replace(held.path.name, held.ref)
    detail = {
        key: held.ref if value == str(held.path) else value
        for key, value in dict(cause.detail).items()
    }
    detail.setdefault("source", held.ref)
    return rebuilt(exc, replace(cause, message=message, detail=detail))


def _coverage_or_refuse(
    result: pipeline.IdentifyResult, held: SetRecording
) -> tuple[dict[str, str], ...]:
    """The warnings a partially answered identification carries, or a refusal.

    Absence is not evidence of absence: chunks with no answer and the rest
    naming nothing is a failure, not a set nobody recognised, and a tracklist
    with holes says how many.
    """
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
            "intake-recognition-failed",
            f"{result.unreached} of {result.chunks} chunk(s) of {held.shown} got no "
            f"answer and the rest named nothing, so this is not a set nobody "
            f"recognised; {result.calls} call(s) were made and counted",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            origin=("intake.cli",),
            detail={
                "source": held.ref,
                "calls": result.calls,
                "unreached": result.unreached,
            },
        )
    return (
        _note(
            "recognition-incomplete",
            f"{result.unreached} of {result.chunks} chunk(s) got no answer, so "
            f"this tracklist has gaps; identify the recording again to fill them",
        ),
    )


def _parts_notes(result: pipeline.IdentifyResult, *, queued: bool) -> tuple[dict[str, str], ...]:
    """Said when the recording was identified in more than one run.

    The bound is not quoted: the identifier's budget is the one place that knows it.
    """
    if result.parts <= 1:
        return ()
    still = (
        "its tracks queue as one job and land as one batch"
        if queued
        else "its tracklist is one list"
    )
    return (
        _note(
            IN_PARTS,
            f"this recording is longer than one recognition run's bound, so it "
            f"was identified in {result.parts} even parts, {result.chunks} "
            f"chunk(s) in all; it is still one set, and {still}",
        ),
    )


def _cache_notes(result: pipeline.IdentifyResult) -> tuple[dict[str, str], ...]:
    """What the recognition cache did to this pass, said where a person reads it.

    A kept answer is last season's, so a pass that read some says how many and
    names the flag that pays for a fresh reading; answers that could not be
    kept mean the next pass over the recording pays again.
    """
    notes: list[dict[str, str]] = []
    if result.cached:
        notes.append(
            _note(
                CACHE_SERVED,
                f"{result.cached} of {result.chunks} chunk(s) were answered from "
                f"what the service said about this recording before and cost "
                f"nothing; pass --refresh to ask it again, which spends",
            )
        )
    if result.cache_unwritten:
        notes.append(
            _note(
                CACHE_UNWRITTEN,
                f"the {result.calls} recognition answer(s) this pass paid for "
                f"could not be kept ({result.cache_unwritten}), so another pass "
                f"over this recording pays for them again",
            )
        )
    return tuple(notes)


def _library_or_refuse(cfg: config.Config, source: Path | str) -> None:
    """Refuse, BEFORE THE SPEND, a library that is not there to be asked.

    An absent library is not an empty one: every track would resolve missing
    with a clean exit. Asked first because the answer is free now.
    """
    music = Path(cfg.library.root) / cfg.library.music_dir
    if music.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"this library's music folder {str(music)!r} is not there, so no identified "
        f"track could be told from one the library already holds; nothing was sent",
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        origin=("intake.cli",),
        detail={"music": str(music), "source": str(source)},
    )


def tracklist_name(held: SetRecording, digest: str) -> str:
    """The tracklist's file name: the recording's stem and a piece of its digest.

    The stem alone is not a name, since a recorder that calls every set REC001
    gives two nights one stem. The digest is of the recording's bytes; one
    that could not be read, or a fetched mix, is named by a digest of ``ref``.
    """
    token = digest or digest_of({"path": held.ref})
    return f"{held.stem}-{token[:TRACKLIST_DIGEST_CHARS]}{TRACKLIST_SUFFIX}"


def _tracklist_dir(cfg: config.Config, given: str | None, source: Path | str) -> Path:
    """Where the tracklist goes, a path that is not a folder refused BEFORE the spend."""
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = cfg.paths.download_staging / TRACKLISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
            f"it; nothing was sent",
            "name a folder with --out",
            out=str(out),
            source=str(source),
        )
    return out


def _tracklist_written(
    out: Path, held: SetRecording, result: pipeline.IdentifyResult
) -> dict[str, str]:
    """Write ``intake identify``'s tracklist and return the note that names it.

    An earlier reading of this recording is replaced, since the name carries
    its digest. A folder that cannot be written is refused, after the spend,
    so the refusal says truthfully what running again costs.
    """
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        path = _tracklist_path(out, held, result)
        if result.cache_unwritten:
            kept = "the recognition answers could not be kept either, so running again pays again"
        elif result.unreached:
            kept = (
                f"the recognition answers were kept, so running again pays only for the "
                f"{result.unreached} chunk(s) that got no answer"
            )
        else:
            kept = "the recognition answers were kept, so running again spends nothing"
        raise _unusable(
            f"the tracklist could not be written to {path} ({type(exc).__name__}: "
            f"{exc.strerror or exc}); {kept}",
            "name another folder with --out, or make this one writable",
            path=str(path),
            source=held.ref,
        ) from exc
    return _written_note(path, result)


def _write_tracklist(out: Path, held: SetRecording, result: pipeline.IdentifyResult) -> Path:
    """The one writer both verbs use; the ``OSError`` is each verb's own to say."""
    path = _tracklist_path(out, held, result)
    config.atomic_write_bytes(result.tracklist.encode("utf-8"), path)
    return path


def _tracklist_path(out: Path, held: SetRecording, result: pipeline.IdentifyResult) -> Path:
    return out / tracklist_name(held, result.digest)


def _written_note(path: Path, result: pipeline.IdentifyResult) -> dict[str, str]:
    return _note(
        TRACKLIST_WRITTEN, f"{len(result.rows)} identified track(s) written in order to {path}"
    )


def _set_tracklist(
    out: Path, held: SetRecording, result: pipeline.IdentifyResult, job_id: str
) -> tuple[Path | None, dict[str, str]]:
    """``intake set``'s tracklist: the path and the note, or None and why not.

    A failed write is said, not raised: the job is queued and is what the
    spend bought, and ``job show`` lists the same tracks from it.
    """
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
        return None, {
            "code": TRACKLIST_UNWRITTEN,
            "message": (
                f"the tracklist could not be written to {failed} ({type(exc).__name__}: "
                f"{exc.strerror or exc}); the job is queued, and its tracks are listed "
                f"by: crate job show {job_id}"
            ),
        }
    return path, _written_note(path, result)


def intake_identify(ctx) -> Envelope:
    """Identify the recording, write its tracklist, and ask the library about it.

    The rows go through ``match_cli.resolve_list`` under this verb's own key
    (R-422), so owned is ``matched``, a version the library may hold is
    OFFERED to the review queue, and an open question is a pending action.

    THE ORDER IS THE SPEND ORDER: configuration, recording, gate, tracklist
    folder and library are settled while a refusal is free, a mix URL is
    fetched last of those (U104), then the paid identifier runs, whose cache
    makes ``intake set`` after this verb cost no calls. The tracklist is
    written before the library is walked, so an unreadable library does not
    take it along. Nothing identified writes nothing and walks nothing.
    """
    cfg = _load()
    source = str(ctx.args.source)
    local = _local_or_none(source)
    recognize.assert_recognition_ready()
    shown = local if local is not None else source.strip()
    out = _tracklist_dir(cfg, ctx.args.out, shown)
    _library_or_refuse(cfg, shown)
    written = None
    with _recording(cfg, source, local, ctx.progress) as held:
        result = pipeline.identify_only(
            held.path,
            refresh=bool(ctx.args.refresh),
            recognition=cfg.recognition,
            progress=ctx.progress,
        )
        warnings = (
            _coverage_or_refuse(result, held)
            + _cache_notes(result)
            + _parts_notes(result, queued=False)
        )
        if result.rows:
            written = _tracklist_written(out, held, result)
    warnings += _fetch_notes(held)
    if written is None:
        return ctx.envelope(data=match.MatchResult(matches=()).payload(), warnings=warnings)
    resolved = match_cli.resolve_list(
        cfg, result.rows, handler_key=ctx.entry.handler_key, run_id=ctx.run.run_id
    )
    pending = resolved.pending
    return ctx.envelope(
        data=resolved.result.payload(),
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
        warnings=(written, *warnings, *resolved.warnings),
    )
