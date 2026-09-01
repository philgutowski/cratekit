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
        help="the set recording to master, as a path to a wav, aiff or flac file",
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
    parser.set_defaults(_handler=master_recording)


def frozen_payload(recording: str, output_dir: str | None, overwrite: bool) -> dict[str, Any]:
    """What the queued job carries, and the only thing the resume is rebuilt from.

    AN EMPTY ``--output-dir`` IS NORMALIZED TO ABSENT HERE, which is the whole
    reason this is a function rather than a dict literal in the handler. An empty
    string reaches ``output_path`` as ``Path(".")`` and lands the master in
    whatever directory the process happens to be in, while ``master_argv`` drops a
    falsy flag and the respawned child writes beside the source instead. One
    invocation, two destinations, decided by which process ran it. Normalizing at
    the freeze makes the two agree by construction rather than by both remembering
    to test the same falsy value.

    THE RECORDING IS MADE ABSOLUTE HERE, and that is the same defect one level
    up. ``jobs.spawn`` starts the child with the RESUMING process's working
    directory, which need not be the one the person queued from, so a relative
    path freezes an instruction that means different files in different
    directories. ``Path.absolute`` is lexical: it resolves nothing, follows no
    link, and stats nothing, so it leaves the deliberate decision below not to
    read the file at queue time exactly as it was.
    """
    return {
        SOURCE: str(Path(recording).absolute()) if recording else recording,
        OUTPUT_DIR: output_dir or None,
        OVERWRITE: bool(overwrite),
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
    argv = ["master", str(payload.get(SOURCE) or "")]
    output_dir = payload.get(OUTPUT_DIR)
    if output_dir:
        argv += ["--output-dir", str(output_dir)]
    if payload.get(OVERWRITE):
        argv.append("--overwrite")
    return [*argv, "--job", job.job_id]


def master_recording(ctx) -> Envelope:
    """Freeze the recording and queue the work, or report the job already queued."""
    recording = str(ctx.args.recording or "")
    if not recording:
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
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
        # THE RECORDING IS NOT STATTED HERE, deliberately. Queueing needs neither
        # the file nor ffmpeg, and a stat in this handler would make the verb
        # refuse on a machine where the work would have run fine later. The cost
        # is that a mistyped path is reported as queued rather than refused; the
        # handler is where it is discovered, and it arrives there as the engine's
        # own ``source-missing`` on the item's row.
        payload = frozen_payload(recording, ctx.args.output_dir, ctx.args.overwrite)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload=payload,
            # ONE RECORDING IS ONE ITEM. Without it the queue holds a job with
            # nothing to claim, and the driver reports an empty success over work
            # it never did.
            item_ids=(str(payload[SOURCE]),),
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


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
    source = str(payload.get(SOURCE) or "")
    output_dir = payload.get(OUTPUT_DIR)
    try:
        report = mastering.master(
            source,
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
STAGING_DIRNAME = ".cratekit-master-staging"


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
    directory = final.parent / STAGING_DIRNAME / job_id / str(ordinal)
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
    source = Path(str(item.item_id or payload.get(SOURCE) or ""))
    output_dir = payload.get(OUTPUT_DIR)
    final = mastering.output_path(
        source, output_dir=Path(str(output_dir)) if output_dir else None
    )
    if source.is_file() and final.exists() and not payload.get(OVERWRITE):
        raise refuse(
            str(mastering.Refusal.OUTPUT_EXISTS),
            f"{final} already exists. Replacing it silently would discard a "
            f"master that may already have been kept, and the settings that "
            f"produced it are not recorded anywhere.",
            origin=("master", "cli"),
            detail={"path": str(final)},
        )

    staged_into = staging_dir(final, job.job_id, item.ordinal)
    reported = run_master(
        # OVERWRITE STAYS FALSE IN STAGING, and the clearing above is what makes
        # that safe. Passing True here instead also works and is worse: it is a
        # second mechanism covering the same leftover, so removing the clear
        # changed nothing a test could see. A guard covered by another guard is a
        # guard nothing covers, measured as a zero row on 2026-09-01.
        {SOURCE: str(source), OUTPUT_DIR: str(staged_into), OVERWRITE: False},
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
    "STAGING_DIRNAME",
    "build",
    "frozen_payload",
    "handle",
    "master_argv",
    "master_recording",
    "run_master",
    "staging_dir",
]
