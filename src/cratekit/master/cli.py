"""``crate master``: level a recorded set and encode it, never touching the source.

The engine archives and verifies the source before the first ffmpeg pass; this
shell must not undermine that. No flag switches the archive off, and no output
path is composed here: the engine's own name builder is the only one, since a
second copy is how an in-place write arrives later.

There is no confirm gate. The ordinary path writes a new file and refuses
``output-exists``, so nothing is lost; ``--overwrite`` can lose the previous
master, but it is an act the person typed, and a gate would ask twice.

The work is a module level function over plain data, so it is drivable without
a configured machine and a job store. Builders take an untyped ``entry`` so this
file does not import the CLI registry (KTD23).

Layer: modules.
"""

from __future__ import annotations

import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import config, jobs
from cratekit.core.cause import refuse
from cratekit.modules.tools import mastering

#: Payload keys this build freezes, named once so the handler and the argv
#: builder cannot drift into a resume that does different work.
SOURCE = "source"
OUTPUT_DIR = "output_dir"
OVERWRITE = "overwrite"
#: Every part in the order named, the first also ``SOURCE``. Only when the
#: recording arrived in several files, so one file freezes the payload it always did.
PARTS = "parts"
#: Only when ``--lufs`` was given. Absent means the engine's default target, so
#: an old payload resumes as the run it was.
TARGET_LUFS = "target_lufs"

#: The origin of every refusal this shell raises.
_ORIGIN = ("master", "cli")


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "recording",
        nargs="+",
        help=(
            "the set recording to master, as a path to a wav, aiff or flac file. "
            "A recording the player split into several files is named as every "
            "part, in order; they are joined in the order given and never sorted"
        ),
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the mastering already queued under this identifier",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        metavar="DIR",
        help=(
            "where the mastered file lands; beside the recording by default, and "
            "never over the recording itself under any value"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "replace an existing master rather than refusing. The previous one is "
            "not archived and a failed encode leaves nothing to fall back on"
        ),
    )
    parser.add_argument(
        "--lufs",
        type=float,
        default=None,
        metavar="N",
        help=(
            f"the integrated loudness target, between {mastering.LUFS_RANGE[0]:g} "
            f"and {mastering.LUFS_RANGE[1]:g}; "
            f"{mastering.DEFAULT_SETTINGS.target_lufs:g} by default"
        ),
    )
    parser.set_defaults(_handler=master_recording)


def frozen_payload(
    recording: str | Sequence[str],
    output_dir: str | None,
    overwrite: bool,
    *,
    lufs: float | None = None,
) -> dict[str, Any]:
    """What the queued job carries, and the only thing the resume is rebuilt from.

    A key is added only when the run asks for something a payload without it
    cannot say. An empty ``--output-dir`` is normalized to absent, so the queuing
    process and the respawned child cannot pick two destinations. Both paths are
    made absolute (lexically, reading nothing), because the child runs in the
    resuming process's working directory, not the queuing one's.
    """
    parts = [recording] if isinstance(recording, str) else list(recording)
    frozen = [str(Path(p).absolute()) if p else p for p in parts]
    payload: dict[str, Any] = {
        SOURCE: frozen[0] if frozen else "",
        OUTPUT_DIR: str(Path(output_dir).absolute()) if output_dir else None,
        OVERWRITE: bool(overwrite),
    }
    if len(frozen) > 1:
        payload[PARTS] = frozen
    if lufs is not None:
        payload[TARGET_LUFS] = float(lufs)
    return payload


def frozen_parts(payload: dict[str, Any]) -> list[str]:
    """Every part a payload names, in the order frozen. One element for one file."""
    parts = payload.get(PARTS)
    if parts:
        return [str(p) for p in parts]
    return [str(payload.get(SOURCE) or "")]


def settings_for(lufs: float | None) -> mastering.Settings:
    """The engine's settings for one target, or its default when none was given.

    The engine owns the range; its refusal is translated rather than its bounds
    copied here.
    """
    if lufs is None:
        return mastering.DEFAULT_SETTINGS
    try:
        return mastering.Settings(target_lufs=float(lufs))
    except ValueError as exc:
        raise refuse(
            "target-lufs-out-of-range",
            str(exc),
            steps=(
                f"pass --lufs between {mastering.LUFS_RANGE[0]:g} and "
                f"{mastering.LUFS_RANGE[1]:g}, or leave it out for the default; "
                f"nothing was queued, read or written",
            ),
            origin=_ORIGIN,
            detail={"lufs": str(lufs)},
        ) from exc


def join_order_warning(parts: Sequence[str]) -> dict[str, str]:
    """The order a split recording will be joined in, said back before it runs."""
    listed = "; ".join(f"{n}. {p}" for n, p in enumerate(parts, start=1))
    return {
        "code": "join-order",
        "message": (
            f"these {len(parts)} parts will be joined in the order given, not "
            f"sorted: {listed}. Nothing has been read or written yet."
        ),
    }


def master_argv(job) -> list[str]:
    """The command line that continues one queued mastering.

    No ``--run``, since this verb declares no gate. Every frozen flag is rebuilt,
    and a payload missing a key still yields a valid command line, because the
    caller is a detached child whose ``KeyError`` nobody would see.
    """
    payload = job.payload or {}
    argv = ["master", *frozen_parts(payload)]
    output_dir = payload.get(OUTPUT_DIR)
    if output_dir:
        argv += ["--output-dir", str(output_dir)]
    if payload.get(OVERWRITE):
        argv.append("--overwrite")
    lufs = payload.get(TARGET_LUFS)
    if lufs is not None:
        # One token with ``=``: a negative target as two tokens parses only while
        # no option of this parser looks like a negative number.
        argv.append(f"--lufs={lufs}")
    return [*argv, "--job", job.job_id]


def master_recording(ctx) -> Envelope:
    """Freeze the recording and queue the work, or report the job already queued."""
    given = ctx.args.recording
    parts = [given] if isinstance(given, str) else list(given or [])
    parts = [str(p or "") for p in parts] or [""]
    if not all(parts):
        # ``source-missing``: its reserved remedy fits an empty positional too.
        raise refuse(
            "source-missing",
            "master needs the recording to work on",
            steps=("pass the path to the recording after the verb",),
            origin=_ORIGIN,
        )
    # Refused before anything is queued: a job whose only outcome is this
    # refusal would be found by whoever resumes it.
    settings_for(ctx.args.lufs)
    cfg = load_config(("master.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
            # Reconcile first: a resume arrives after something stopped.
            job = jobs.reconcile(store, ctx.args.job)
            job, warnings = jobs.resumed(ctx, store, job)
            return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)
        # The recording is not statted here: queueing needs neither the file nor
        # ffmpeg, and a mistyped path surfaces as the engine's ``source-missing``.
        payload = frozen_payload(parts, ctx.args.output_dir, ctx.args.overwrite, lufs=ctx.args.lufs)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            # One recording, split or not, is one item; without it the driver
            # reports an empty success over work it never did.
            item_ids=(str(payload[SOURCE]),),
            cfg=cfg,
        )
        # A warning rather than a data key, because ``job_state/1`` refuses extras.
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
        return ctx.envelope(data=jobs.reported(store, job), warnings=notices)


def run_master(payload: dict[str, Any], *, runner=mastering.subprocess_runner) -> dict:
    """Do the mastering one queued job asks for, and report what actually happened.

    Takes the payload rather than a job so it is drivable without a job store.
    The engine's refusals are translated: ``MasteringRefused`` is not a
    ``CratekitError``, and escaping would report it as ``internal-error``.
    """
    parts = frozen_parts(payload)
    output_dir = payload.get(OUTPUT_DIR)
    settings = settings_for(payload.get(TARGET_LUFS))
    try:
        report = mastering.master_parts(
            parts,
            settings=settings,
            output_dir=Path(output_dir) if output_dir else None,
            overwrite=bool(payload.get(OVERWRITE)),
            runner=runner,
        )
    except mastering.MasteringRefused as exc:
        raise refuse(
            str(exc.refusal),
            exc.detail,
            origin=("master", "cli"),
            detail={"path": str(exc.path) if exc.path is not None else None},
        ) from exc
    return mastering.as_payload(report)


#: Where a queued encode is written before it is put in place: under the
#: destination's own parent, since the commit is an ``os.replace``, atomic only
#: within one filesystem. Not ``STAGING_DIRNAME``, which ``cli.setup`` already uses.
MASTER_STAGING_DIRNAME = ".cratekit-master-staging"


def staging_dir(final: Path, job_id: str, ordinal: int) -> Path:
    """The staging directory for one item of one job, cleared and recreated.

    Cleared because its contents are an unfinished attempt's: ffmpeg writes with
    ``-y``, and a partial file at the real destination would later be refused as
    a master somebody kept.
    """
    directory = final.parent / MASTER_STAGING_DIRNAME / job_id / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory


def handle(job, item, cfg) -> jobs.Produced:
    """Master one queued recording. The per-item worker behind ``handler_key`` master.

    The destination is checked here, with the engine's own name builder, because
    the encode is staged and the engine's ``output-exists`` would only see the
    staging directory. Only when the source exists, so a missing recording gets
    the engine's own ``source-missing``. ``cfg`` is the frozen configuration
    (KTD9), unused today.
    """
    del cfg
    payload = dict(job.payload or {})
    # The ITEM names the recording, so each item of a multi-item job masters its
    # own file. A split recording is enqueued as one item, so its parts come
    # from the payload.
    parts = (
        [Path(p) for p in frozen_parts(payload)]
        if payload.get(PARTS)
        else [Path(str(item.item_id or payload.get(SOURCE) or ""))]
    )
    present = all(p.is_file() for p in parts)
    output_dir = payload.get(OUTPUT_DIR)
    final = mastering.planned_output(
        parts, output_dir=Path(str(output_dir)) if output_dir else None
    )
    if present and final.exists() and not payload.get(OVERWRITE):
        raise refuse(
            str(mastering.Refusal.OUTPUT_EXISTS),
            mastering.output_exists_detail(final),
            origin=_ORIGIN,
            detail={"path": str(final)},
        )
    # Nothing is created for a recording that is not there: ``source-missing``
    # promises nothing was written, and the parent may be an unmounted volume.
    staged_into = staging_dir(final, job.job_id, item.ordinal) if present else final.parent
    # Overwrite stays false in staging, which the clearing makes safe; every
    # other frozen key travels, or the first part alone would be mastered.
    staged: dict[str, Any] = {SOURCE: str(parts[0]), OUTPUT_DIR: str(staged_into), OVERWRITE: False}
    if len(parts) > 1:
        staged[PARTS] = [str(p) for p in parts]
    if payload.get(TARGET_LUFS) is not None:
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
    # The runner is read at call time so a test can stand in for the encoder.
    reported = run_master(staged, runner=mastering.subprocess_runner)
    # The path comes off the report, not a second name builder; the engine
    # already refuses an encode that produced nothing.
    return jobs.Produced(staged=Path(str(reported["output"])), final=final)


__all__ = [
    "MASTER_STAGING_DIRNAME", "build", "frozen_parts", "frozen_payload", "handle",
    "join_order_warning", "master_argv", "master_recording", "run_master", "settings_for",
    "staging_dir",
]
