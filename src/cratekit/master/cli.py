"""``crate master``: level a recorded set and encode it, never touching the source.

THE ENGINE'S CENTRAL PROMISE IS THAT THE SOURCE IS NEVER MODIFIED, and
:func:`~cratekit.modules.tools.mastering.archive_source` is how it keeps it: the
copy is taken BEFORE the first ffmpeg pass and its digest is compared against the
source rather than assumed. This shell exists to not undermine that, which is
mostly a list of things it refuses to offer.

NO FLAG SWITCHES OFF THE ARCHIVE. ``master`` takes an ``archive`` keyword and the
source system's script ships ``--no-archive``. Neither is exposed here and no
payload key carries one. A flag that skips the safety copy converts a recoverable
operation into a destructive one, which is the single thing this verb must never
be, so the capability is dropped rather than defaulted.

NO OUTPUT PATH IS COMPOSED HERE EITHER. ``output_path`` decides the destination
from the source stem and an optional directory, and this file passes the
directory through rather than building a name beside it. Two name-builders for
one file is how an in-place write arrives later, from the copy nobody updated.

THERE IS NO CONFIRM GATE, AND ``--overwrite`` IS WHY THAT NEEDS ARGUING. On the
ordinary path nothing is lost: the run writes a NEW file, archives the original,
and refuses ``output-exists`` rather than replacing a master somebody kept, so
there is no decision for a person to make and a gate would be decorative. That
warrant does NOT extend to ``--overwrite``. ``archive_source`` archives the
SOURCE only, and the encode writes straight to the destination with ``-y``, so a
failed encode under that flag leaves a truncated file where the previous master
was and no copy anywhere. What carries the decision on that path is the flag
itself: it is an act the person typed, and R34's gate machinery exists for
decisions the PRODUCT raises rather than ones the person volunteered. Gating a
flag somebody had to type asks the same question twice.

THE WORK IS A MODULE-LEVEL FUNCTION RATHER THAN A CLOSURE IN THE HANDLER.
``run_master`` takes plain data, so the properties that matter about it can be
driven without a configured machine and a job store. That is not a style
preference: nothing in ``src`` claims a job item today, so a work body built
inside the handler would be reachable by nothing at all.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

Layer: modules.
"""

from __future__ import annotations

import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import mastering

#: Payload keys this build freezes. Named once so the handler and the argv
#: builder cannot drift: a key the handler freezes and the builder does not read
#: is a resume that quietly does different work from the run it continues.
SOURCE = "source"
OUTPUT_DIR = "output_dir"
OVERWRITE = "overwrite"
#: U105. Present only when the recording arrived in more than one file, and then
#: it holds every part in the order the person named them, the first of which is
#: also ``SOURCE``. Absent for one file, so a single recording freezes exactly the
#: payload it froze before a join existed.
PARTS = "parts"
#: U105. Present only when ``--lufs`` was given. Absent means the engine's
#: default target, which is what every job queued before this key existed asked
#: for, so an old payload resumes as the run it was.
TARGET_LUFS = "target_lufs"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("master.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


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

    ``recording`` is one path or every part of a split recording, in order. One
    part, whichever way it is passed, freezes exactly the payload a single
    recording always froze, and so does an absent ``lufs``. A key is added only
    when the run asks for something a payload without it cannot say.

    AN EMPTY ``--output-dir`` IS NORMALIZED TO ABSENT HERE, which is the whole
    reason this is a function rather than a dict literal in the handler. An empty
    string reaches ``output_path`` as ``Path(".")`` and lands the master in
    whatever directory the process happens to be in, while ``master_argv`` drops a
    falsy flag and the respawned child writes beside the source instead. One
    invocation, two destinations, decided by which process ran it. Normalizing at
    the freeze makes the two agree by construction rather than by both remembering
    to test the same falsy value.

    BOTH PATHS ARE MADE ABSOLUTE HERE, and that is the same defect one level up.
    ``jobs.spawn`` starts the child with the RESUMING process's working directory,
    which need not be the one the person queued from, so a relative path freezes
    an instruction that means different files in different directories. The
    DIRECTORY needs it exactly as much as the recording does: ``master_argv``
    rebuilds ``--output-dir`` from this payload verbatim, so a relative one sends
    the master somewhere the person did not ask for and reports success for it,
    which is the failure the paragraph above is already about.

    ``Path.absolute`` is lexical: it resolves nothing, follows no link, and stats
    nothing, so it leaves the deliberate decision below not to read the file at
    queue time exactly as it was.
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

    THE ENGINE OWNS THE RANGE. ``Settings`` validates the target at construction,
    and this translates its refusal into a declared reason rather than holding a
    second copy of the bounds that could drift from the one ffmpeg is checked
    against.
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
            origin=("master", "cli"),
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

    IT CARRIES NO ``--run``. This verb declares no gate, so there is no decision
    frozen against a run and a ``--run`` here would name a run nothing was
    recorded against. The queued shells that DO carry it are the ones with an
    ``explicit`` gate, and ``tests/test_queued_resume_contract.py`` derives that
    population from the registry rather than from a list, so this verb joins it on
    the day somebody adds a gate and not before.

    EVERY FROZEN FLAG IS REBUILT. A resume that drops ``--overwrite`` meets the
    ``output-exists`` refusal the first attempt was told to ignore, and one that
    drops ``--output-dir`` writes the master somewhere the person did not ask for
    and reports success for it.

    A payload missing a key this build writes still produces a valid command line.
    That is forward tolerance for keys a later build may add rather than a case
    reachable today, since no payload of this shape can exist until this verb
    ships. The reason to carry it anyway is that the caller is a detached child
    whose only output is a log nobody is watching, so a ``KeyError`` there is
    invisible.
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
        # ONE TOKEN, WITH ``=``. A target is negative, and ``--lufs -16`` as two
        # tokens parses only while no option of this parser looks like a
        # negative number. The joined spelling parses whatever the parser grows.
        argv.append(f"--lufs={lufs}")
    return [*argv, "--job", job.job_id]


def master_recording(ctx) -> Envelope:
    """Freeze the recording and queue the work, or report the job already queued."""
    given = ctx.args.recording
    parts = [given] if isinstance(given, str) else list(given or [])
    parts = [str(p or "") for p in parts] or [""]
    if not all(parts):
        # ``source-missing`` rather than a slug of its own. Its reserved
        # remediation is "name a recording that exists; nothing was read and
        # nothing was written", which is the right sentence for an empty
        # positional as well as an absent file, and both are undone by the same
        # act. A second slug would split one remedy across two vocabularies.
        raise refuse(
            "source-missing",
            "master needs the recording to work on",
            steps=("pass the path to the recording after the verb",),
            origin=("master", "cli"),
        )
    # REFUSED BEFORE ANYTHING IS QUEUED. A target the engine would refuse is
    # known now, and queueing it would park a job whose only possible outcome is
    # that refusal, discovered by whoever resumes it.
    settings_for(ctx.args.lufs)
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            # RECONCILE FIRST. A resume arrives after something stopped, and a
            # claim left behind by a driver that died is state the queue cannot
            # see for itself.
            job = jobs.reconcile(store, ctx.args.job)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                # The step that was missing until U46. Everything above this line
                # already worked; nothing below it ever ran an item. A total
                # failure raises out of here rather than reaching the report,
                # which is correct: the engine has already recorded the job as
                # failed and the refusal carries the item's own cause.
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
            # A JOB THAT DID NOT END CLEANLY IS NOT AN OK EXIT, and this branch
            # returned one for every such job until R-225 was closed here. A
            # total failure raises out of the drive above, and nothing else did:
            # a job already failed on entry, a cancelled one and a parked one all
            # reached the report and exited 0. OUTSIDE the ``is_open`` branch so
            # the second ask about a failed job answers the way the first did.
            jobs.raise_for_state(job)
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
        # THE RECORDING IS NOT STATTED HERE, deliberately. Queueing needs neither
        # the file nor ffmpeg, and a stat in this handler would make the verb
        # refuse on a machine where the work would have run fine later. The cost
        # is that a mistyped path is reported as queued rather than refused; the
        # handler is where it is discovered, and it arrives there as the engine's
        # own ``source-missing`` on the item's row.
        payload = frozen_payload(
            parts, ctx.args.output_dir, ctx.args.overwrite, lufs=ctx.args.lufs
        )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            # ONE RECORDING IS ONE ITEM. Without it the queue holds a job with
            # nothing to claim, and the driver reports an empty success over work
            # it never did. A SPLIT RECORDING IS STILL ONE ITEM: its parts make
            # one master, and the item is named for the first part while the
            # payload carries the rest.
            item_ids=(str(payload[SOURCE]),),
            cfg=cfg,
        )
        # THE ORDER IS SAID BACK HERE, which is before anything is read or
        # written: queueing opens no audio file. A warning rather than a data
        # key, because ``job_state/1`` declares its fields and refuses an extra.
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
        return ctx.envelope(data=_reported(store, job), warnings=notices)


def run_master(payload: dict[str, Any], *, runner=mastering.subprocess_runner) -> dict:
    """Do the mastering one queued job asks for, and report what actually happened.

    PURE OF THE JOB ENGINE ON PURPOSE, taking the payload rather than a job. The
    engine's properties that matter most, that the source is byte-identical
    afterwards and that the archive was verified before anything else ran, are
    then drivable without a configured machine, a job store and a claimed item.
    Nothing in ``src`` claims an item today, so built inside the handler this body
    would have no reachable caller at all.

    THE ENGINE'S REFUSALS ARE TRANSLATED RATHER THAN LET ESCAPE.
    ``MasteringRefused`` is not a ``CratekitError``, so the dispatcher's
    ``except Exception`` converts it to ``internal-error``, which carries
    ``report-defect``. A person who mistyped a path would be told to file a bug
    against this program. Every member of ``Refusal`` is a declared reason with a
    reserved code, so the slug travels through unchanged.
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


#: Where a queued encode is written before it is put in place. Under the
#: DESTINATION's own parent rather than a temp directory, because the engine's
#: commit is an ``os.replace`` and that is atomic only within one filesystem, and
#: a mastered set is measured in gigabytes.
#:
#: NOT ``STAGING_DIRNAME``, which is what this was called first. That name is
#: already taken by ``cratekit.cli.setup``, where it means ``"Downloads"``, the
#: acquisition staging directory a person configures. One symbol meaning two
#: things in two modules is the defect ``docs/METHOD.md`` says to go looking for
#: once the suite is green, and these two mean nothing like each other.
MASTER_STAGING_DIRNAME = ".cratekit-master-staging"


def staging_dir(final: Path, job_id: str, ordinal: int) -> Path:
    """The staging directory for one item of one job, cleared and recreated.

    CLEARED, because whatever is in it belongs to an attempt that did not finish.
    That is the whole reason the encode is staged: ffmpeg is invoked with ``-y``
    and writes straight at whatever target it is given, so a run killed mid encode
    leaves a partial file behind. At the real destination that partial file is
    permanent damage, since the next resume meets ``output-exists`` and the
    refusal tells the person that replacing it would discard a master they kept,
    when the file is this queue's own corpse. In here it is just this attempt's
    leftovers.
    """
    directory = final.parent / MASTER_STAGING_DIRNAME / job_id / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory


def handle(job, item, cfg) -> jobs.Produced:
    """Master one queued recording. The per-item worker behind ``handler_key`` master.

    THE DESTINATION IS CHECKED HERE AND THE ENCODE HAPPENS ELSEWHERE, which is the
    only part of this that is not a thin call. ``mastering.master`` refuses
    ``output-exists`` against whatever directory it is writing into, so staging the
    encode would move that guard off the real destination and let the commit
    replace a master somebody kept. The check therefore comes up to the caller,
    using the engine's OWN name builder rather than a second one, which is the rule
    this module's docstring already states about ``output_path``.

    IT IS GUARDED ON THE SOURCE EXISTING so that a missing recording still gets the
    engine's own ``source-missing`` diagnosis in the engine's own order, rather
    than a destination complaint about a file that was never going to be read.

    ``cfg`` is the configuration this job was FROZEN against (KTD9). Mastering
    reads nothing from it today; it is a parameter rather than something this
    function loads so that the day it does, it cannot load a fresh one.
    """
    del cfg
    payload = dict(job.payload or {})
    # THE ITEM NAMES THE RECORDING, not the payload. They hold the same value for
    # a job this shell queued, since it freezes one recording and enqueues it as
    # the one item, and reading the payload instead is still wrong: it makes every
    # item of a multi-item job master the SAME file, and the second one onwards
    # then fails ``output-exists`` against the first one's output. Measured that
    # way once, on the four-item job in ``tests/test_job_seam.py``. The item is
    # what ``drive`` claims and the item is the unit of work.
    #
    # A SPLIT RECORDING'S PARTS COME FROM THE PAYLOAD, which is the exception to
    # the rule above and is safe for the reason the rule exists: this shell
    # enqueues a split recording as ONE item, so there is no second item for the
    # payload to make master the same file.
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
            f"{final} already exists. Replacing it silently would discard a "
            f"master that may already have been kept, and the settings that "
            f"produced it are not recorded anywhere.",
            origin=("master", "cli"),
            detail={"path": str(final)},
        )

    # NOTHING IS CREATED FOR A RECORDING THAT IS NOT THERE. ``source-missing``
    # reserves the remediation "name a recording that exists; nothing was read and
    # nothing was written", and building a staging tree first would falsify the
    # second half. It also matters when the destination's own parent is a volume
    # that is not mounted: the mkdir would either fail with an error about a
    # directory the person never named, or succeed against the mount point and
    # write into the empty directory underneath it. So the staging tree is built
    # only once the source is known to exist, and the engine still owns the
    # refusal itself.
    staged_into = (
        staging_dir(final, job.job_id, item.ordinal)
        if present
        else final.parent
    )
    staged: dict[str, Any] = {
        SOURCE: str(parts[0]),
        OUTPUT_DIR: str(staged_into),
        OVERWRITE: False,
    }
    if len(parts) > 1:
        staged[PARTS] = [str(p) for p in parts]
    if payload.get(TARGET_LUFS) is not None:
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
    reported = run_master(
        # OVERWRITE STAYS FALSE IN STAGING, and the clearing above is what makes
        # that safe. Passing True here instead also works and is worse: it is a
        # second mechanism covering the same leftover, so removing the clear
        # changed nothing a test could see. A guard covered by another guard is a
        # guard nothing covers, measured as a zero row on 2026-09-01.
        #
        # EVERY OTHER FROZEN KEY TRAVELS, the parts and the target with it. A
        # staged payload rebuilt from the three keys alone masters the first
        # part at the default target and commits that as the whole set.
        staged,
        # Resolved at CALL time, not bound at definition time, so a test can put a
        # stand-in encoder in front of it. ``run_master``'s own default is bound
        # when this module is imported and cannot be reached any other way.
        runner=mastering.subprocess_runner,
    )
    # THE REPORT IS READ FOR THE PATH, and there is no check behind it, which is a
    # decision rather than an omission. A check that the reported file exists was
    # written here first and then measured: it killed zero tests, because
    # ``mastering.master`` already refuses ``encoder-failed`` when the encode
    # reports success and produces nothing, so the branch was unreachable through
    # the only caller there is. An unreachable branch with a test that cannot drive
    # it is worse than no branch, so it is gone and the engine's own refusal is
    # what a person sees.
    #
    # The path itself comes off the report rather than from a second call to
    # ``output_path``. A mutation cannot tell those apart, since they agree by
    # construction; the reason is the one this module's docstring already gives,
    # that two name builders for one file is how an in-place write arrives later
    # from the copy nobody updated.
    return jobs.Produced(staged=Path(str(reported["output"])), final=final)


__all__ = [
    "MASTER_STAGING_DIRNAME",
    "build",
    "frozen_parts",
    "frozen_payload",
    "handle",
    "join_order_warning",
    "master_argv",
    "master_recording",
    "run_master",
    "settings_for",
    "staging_dir",
]
