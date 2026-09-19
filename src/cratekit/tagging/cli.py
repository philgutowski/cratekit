"""``crate tag folder``: queue genre tagging over a folder, and drive it.

WHAT THIS VERB DOES, AND WHY THAT IS QUEUEING RATHER THAN TAGGING. Every file in
a download folder is one or more questions asked of a public record catalogue,
paced so the catalogue keeps answering, so a folder of two hundred files is long
work by any definition. Conformance 5 says long work is queued rather than run
inline, for the reason the source system taught: a sweep that runs inline has no
record, no resume, and no way to answer "what is it doing" from anywhere but the
terminal it was started in. So this verb freezes the folder and the configuration
the run will use (KTD9), queues one job with one item per audio file, and reports
the job. :func:`handle` at the foot of this module is the worker behind it.

THE ITEMS ARE THE ENGINE'S OWN WALK, and that is KTD7 rather than a convenience.
:func:`cratekit.tagging.tag.audio_files` is what the engine tags one file per, so
it is what this shell queues one item per. A shell that walked the folder itself
would be a second opinion about which files the job covers, and the drift runs in
the expensive direction: a job reporting done over files it never queued.

THE IDENTIFIERS ARE RELATIVE TO THE FOLDER, so the frozen payload holds the only
absolute path and an item stays short enough to read in a job listing. Nothing
builds a filename out of one, because
:func:`cratekit.tagging.artifacts.final_path` names a report after the item's
ORDINAL, which is what makes an arbitrary identifier safe there.

THE FOLDER IS FROZEN ABSOLUTE. A resume is a fresh process that
``cratekit.cli.jobs`` spawns, and a relative folder would resolve against
whatever directory that process happens to start in, which is a sweep of some
other folder wearing this job's identifier.

Layer: modules.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope
from cratekit.core import art, config, jobs, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import artifacts, searchers, shell

# THE ENGINE IS ALIASED because this module already defines ``tag_folder`` and
# that function is the VERB, while :mod:`cratekit.tagging.tag` defines a
# ``tag_folder`` that is the ENGINE. One symbol meaning two things in one file is
# the defect ``docs/METHOD.md`` says to hunt, and this unit is where the shell
# imports the engine for the first time. ``adopt/scan_cli.py`` aliased its own
# engine import for exactly this shape, and U51 aliased three modules called
# ``export``.
from cratekit.tagging import tag as tag_engine


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token is carried straight through from the configuration error
    that raised it, so "no config at all" and "config written by a newer build"
    keep their different answers all the way to the CLI.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this modules-ranked file importing the layer above it (KTD23).
    """
    parser.add_argument("folder", help="folder of audio to tag")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the tagging job already queued under this identifier",
    )
    parser.set_defaults(_handler=tag_folder)


def tag_argv(job) -> list[str]:
    """The command line that continues one queued sweep.

    THE CONTRACT EVERY LONG-RUNNING VERB OWES: the payload is frozen at queue
    time (KTD9), so only the verb that queued it knows how to turn it back into
    an invocation. It names the JOB as well as the folder, which is what stops a
    resume from queueing a second record for one piece of work.
    """
    folder = job.payload.get("folder", "")
    return ["tag", "folder", folder, "--job", job.job_id]


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say happened to the folder.

    DERIVED FROM WHAT RAN, never from what was queued. A sweep that tagged three
    files of five and is continued tomorrow has five reports on disk and the
    person asking what happened means all five, which is why this reads the
    artifacts back rather than accumulating counts in memory.

    ZEROES INCLUDED for the skip reasons, on the rule
    :func:`cratekit.adopt.scan.categories` states: a summary listing only the
    reasons it happened to see makes "nothing here was already tagged" and "this
    build does not count that" the same output.

    THE UNRESOLVED STRINGS ARE NOT ZERO FILLED, and that is the opposite rule
    rather than an inconsistency. The skip reasons are a closed set this build
    declares, so their absence is a fact worth stating; a source genre is a word
    a catalogue chose, so there is no set to fill and every key present is one a
    person can go and add an alias for (R24).

    ``art_repair`` COUNTS EVERY STATUS THE REPAIR CAN REPORT, zero filled on the
    first rule, because it is a closed set this build declares. A report
    committed before the repair existed carries no status and is counted under
    none of them, since which status it would have had is not known.
    ``art_fetch`` is the same rule over new art, so ``unavailable`` stands next
    to ``embedded`` as a count a person can see was zero.
    """
    skipped = {
        reason: 0
        for reason in (tag_engine.HAS_GENRE, tag_engine.NO_HIT, tag_engine.UNMAPPED_GENRE)
    }
    art_repair = dict.fromkeys(art.REPAIR_STATUSES, 0)
    art_fetch = dict.fromkeys(tag_engine.ART_FETCH_STATUSES, 0)
    unresolved: dict[str, int] = {}
    tagged = 0
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
        if reason in skipped:
            skipped[reason] += 1
        elif report.get("genre_written"):
            tagged += 1
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
            unresolved[source_genre] = unresolved.get(source_genre, 0) + 1
        status = str(report.get("art_repair") or "")
        if status in art_repair:
            art_repair[status] += 1
        fetched = str(report.get("art_fetch") or "")
        if fetched in art_fetch:
            art_fetch[fetched] += 1
    return {
        "tagged": tagged,
        "skipped": skipped,
        "unresolved": unresolved,
        "art_repair": art_repair,
        "art_fetch": art_fetch,
    }


def _empty(reason: str, detail: str) -> tuple[dict, tuple[dict[str, str], ...]]:
    """The payload and warning for a folder with nothing to tag.

    THE HONEST ZERO, and it is a different thing from a job with no items. A
    folder holding no audio is a correct outcome and a common one;
    ``core.jobs`` reports a job with no items as SUCCEEDED by design, so a verb
    that queued one here would report a clean tagging sweep over a folder
    nothing walked. Nothing is queued and the envelope says which zero this is.

    THE PAYLOAD SHAPE IS :func:`cratekit.tagging.shell.no_op`'s rather than this
    module's, so the zero paths the two tagging verbs have cannot reintroduce
    R-234's null ``job_id`` separately.
    """
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def tag_folder(ctx) -> Envelope:
    """Queue one tagging sweep over a folder, and drive it on a resume.

    The handler key comes off the entry rather than being spelled again here, so
    the job the queue holds and the verb the registry declares cannot name two
    different things.

    THERE ARE THREE ZEROES AND THEY ARE THREE WARNINGS, because the person's
    next move differs for each: put some music in the folder, fix what they
    typed, or name a folder at all. The engine's walk answers empty for all
    three, which is correct for a walk and is exactly why they are told apart up
    here.

    THE UNNAMED FOLDER IS THE ONE THAT MATTERS. An empty string is a valid
    argument to a positional that takes one, so the parser accepts it, and
    ``Path("")`` is the CURRENT DIRECTORY. This verb writes to files, so
    resolving it would sweep whatever the person happens to be standing in.
    ``tag.retag`` refuses the same argument under ``tag-retag-folder-unknown``
    rather than defaulting, for that reason and no other. This zero is the same
    protection at the strength this unit can reach: a refusal needs a slug of its
    own in ``cause.REASONS``, and reusing the correction verb's would put that
    verb's name on this one's failure. Recorded as a residual.
    """
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)

    named = str(ctx.args.folder or "")
    if not named.strip():
        payload, warnings = _empty(
            "tag-folder-unnamed",
            "no folder was named, and this verb writes to the files it walks, so "
            "it will not fall back to the directory you are standing in",
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    folder = Path(named).expanduser().absolute()
    files = tag_engine.audio_files(folder)
    if not files:
        payload, warnings = (
            _empty(
                "tag-folder-no-audio",
                f"{folder} holds no audio files this build can tag, so there is "
                f"nothing to sweep",
            )
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
                f"{folder} is not a folder on this machine, so there is nothing "
                f"to sweep",
            )
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            # ONE AUDIO FILE IS ONE ITEM, relative to the frozen folder. Without
            # them the queue holds a job with nothing to claim and the driver
            # reports an empty success over a sweep it never took.
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job))


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Continue the sweep already queued under this identifier, and drive it.

    EVERY RULE OF THE RESUME LIVES IN :func:`cratekit.tagging.shell.advance`,
    which reconciles a claim left by a driver that died, refuses a job carrying
    no items, drives, and raises rather than reporting when the job closed
    carrying a cause. That last one is R-225: a person whose folder was half
    tagged must not be handed a normal envelope the dispatcher exits 0 over.
    """
    with jobs.open_store() as store:
        job, warnings = shell.advance(
            ctx,
            store,
            jobs.get(store, ctx.args.job),
            origin=("tagging", "cli"),
            nothing_to_run="report a tagging sweep over a folder it never walked",
        )
        return ctx.envelope(
            data=shell.reported(store, job, {"tagging": _summary(cfg, job.job_id)}),
            warnings=warnings,
        )


def handle(job, item, cfg) -> jobs.Produced:
    """Tag ONE file. The per item worker behind ``tag.folder``.

    THE SEARCHER IS LOOKED UP RATHER THAN CONSTRUCTED (KTD11, R23).
    ``ItemHandler`` is a fixed three argument callable, so a worker that built
    its own searcher inline would leave a test nowhere to hand a fake in and
    R18's no network proof unwritable. The lookup happens at CALL TIME, on the
    module rather than on a name imported from it, which is what makes the
    substitution reach this line. R-226 records the honest limit: the child
    ``crate job resume`` spawns is a fresh process and inherits nothing patched
    in another one, so a detached run always gets the live searcher.

    THE FOLDER IS FROZEN AND THE FILES IN IT ARE NOT. A file deleted between the
    queueing and the drive is refused with its own slug rather than skipped, on
    the rule ``adopt/scan_cli.handle`` states: an item that reported done having
    tagged nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. ``source-missing`` rather than a slug of this
    verb's own, because its reserved remediation is "nothing was read and
    nothing was written", which is exactly what this refusal promises, and
    because ``adopt-item-absent`` and ``outbound-item-absent`` each name the
    frozen SOURCE they were derived from rather than a file on disk.

    A CATALOGUE NOBODY COULD READ RAISES OUT OF HERE, and that is R19x working
    rather than a gap. :func:`cratekit.tagging.searchers.catalogue_searcher`
    declines when a source answered and had nothing, and refuses only when none
    of them answered at all, so this item fails, the rest of the folder is
    unaffected, and a retry redoes exactly the one that failed.

    THE CONFIGURATION IS THE FROZEN ONE AND IS NOT LOADED HERE. KTD9 closes the
    recorded resume bug where a queued run re-resolved its configuration; a
    handler that loaded one is that defect wearing a new hat.
    """
    folder = Path(str((job.payload or {}).get("folder") or ""))
    path = folder / item.item_id
    if not path.is_file():
        raise refuse(
            "source-missing",
            f"{path} is no longer a file, so there is nothing to tag for this "
            f"item. Nothing was read and nothing was written",
            steps=(
                "run the tagging verb again over the folder as it now stands; "
                "this job was queued against a folder that has since changed",
            ),
            origin=("tagging", "cli"),
            detail={"item": item.item_id, "folder": str(folder)},
        )
    result = tag_engine.tag_one(
        path,
        searcher=searchers.for_taxonomy(taxonomy.default_taxonomy()),
        fetch_image=searchers.for_images(),
    )
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(result.path),
            "genre_written": result.genre_written,
            "skipped": result.skipped,
            "source": result.source,
            "source_genre": result.source_genre,
            "art_repair": result.art_repair,
            "art_repair_detail": result.art_repair_detail,
            "art_fetch": result.art_fetch,
            "art_fetch_detail": result.art_fetch_detail,
        },
    )
