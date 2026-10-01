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
from cratekit.core import active_taxonomy, art, config, jobs
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

#: The warning a sweep carries when some of what it tagged is a word the declared
#: taxonomy does not know. A WARNING CODE AND NOT A CAUSE, on the rule the three
#: no-op codes in this module already follow: the verb succeeded, the files were
#: written, and a catalogue using a word this template has never declared is a
#: fact about the template rather than a reason anything did not happen.
OFF_TAXONOMY = "tag-folder-off-taxonomy"

#: The warning a sweep carries when some files were left untagged because a
#: catalogue could not be read for them, rather than because none carried them
#: (R-791). A warning and not a cause, on the same rule: the sweep did what it
#: could and the files are askable again on the next run.
SOURCES_UNREAD = "tag-folder-sources-unread"

#: The warning that names a catalogue which refused this machine with a bot
#: check or a block page on every file it was asked about. Apart from the count
#: above because the next move differs: a whole catalogue contributed nothing to
#: the run, which a person needs to know before they trust any decline in it.
SOURCE_BLOCKED = "tag-folder-source-blocked"


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

    ``off_taxonomy`` IS THE THIRD DISPOSITION AND IS COUNTED APART FROM BOTH. A
    file whose genre came from the catalogue's own word was written, so it is
    still in ``tagged``, and it is not a clean tag, so its string is listed here
    the way a decline's is listed in ``unresolved``. The two maps are never
    merged: a decline left the file askable and this one is already on disk,
    which are different jobs for the person reading them. Same not zero filled
    rule, for the same reason, and keyed on the SOURCE string rather than the
    written one, because the alias a person would add is written against what
    the catalogue said (R-650).

    ``art_repair`` COUNTS EVERY STATUS THE REPAIR CAN REPORT, zero filled on the
    first rule, because it is a closed set this build declares. A report
    committed before the repair existed carries no status and is counted under
    none of them, since which status it would have had is not known.
    ``art_fetch`` is the same rule over new art, so ``unavailable`` stands next
    to ``embedded`` as a count a person can see was zero.

    ``answers`` COUNTS FILES BY WHAT EACH CATALOGUE ANSWERED, zero filled over
    every source and every answer, so "Bandcamp was blocked on all 66" and
    "Bandcamp matched none of 66" are two different lines rather than one silence
    (R-791). A report committed before the answers were recorded counts under
    none of them, for the art repair's reason.
    """
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
    answer_values = (*(answer.value for answer in searchers.Answer), searchers.NOT_ASKED)
    answers = {source: dict.fromkeys(answer_values, 0) for source in searchers.SOURCES}
    art_repair = dict.fromkeys(art.REPAIR_STATUSES, 0)
    art_fetch = dict.fromkeys(tag_engine.ART_FETCH_STATUSES, 0)
    unresolved: dict[str, int] = {}
    off_taxonomy: dict[str, int] = {}
    tagged = 0
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
        if reason in skipped:
            skipped[reason] += 1
        elif report.get("genre_written"):
            tagged += 1
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
            unresolved[source_genre] = unresolved.get(source_genre, 0) + 1
        status = str(report.get("art_repair") or "")
        if status in art_repair:
            art_repair[status] += 1
        fetched = str(report.get("art_fetch") or "")
        if fetched in art_fetch:
            art_fetch[fetched] += 1
        for said in report.get("answers") or ():
            if not isinstance(said, dict):
                continue
            counted = answers.get(str(said.get("source") or ""))
            word = str(said.get("answer") or "")
            if counted is not None and word in counted:
                counted[word] += 1
    return {
        "tagged": tagged,
        "skipped": skipped,
        "unresolved": unresolved,
        "off_taxonomy": off_taxonomy,
        "answers": answers,
        "art_repair": art_repair,
        "art_fetch": art_fetch,
    }


def _unread_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Say how many files no catalogue answer settled, and which catalogue refused all.

    THE COUNT IS THE FIX FOR THE CLEAN NO-HIT (R-791). Without it a sweep whose
    fallbacks were all refused reads, on the surface a person reads, exactly as
    one whose fallbacks were all asked and had nothing.

    A CATALOGUE IS NAMED WHEN IT WAS BLOCKED ON EVERY FILE IT WAS ASKED ABOUT,
    and at least one. A file whose search ended at a Beatport match never asked
    the fallbacks, so "every file" is every file the catalogue was sent, not every
    file in the folder; counting the others would let a run where Beatport
    matched half the folder hide a fallback that was refused on the other half.
    In the walk's own source order, so two runs over one folder warn alike.

    THE COUNT NAMES WHAT WENT UNREAD, per source and per answer, because the
    three unread answers send a person to three places. A parse break is said to
    be a defect a rerun will not move, so it is never filed under the promise
    that the next run asks again and left there.
    """
    warnings: list[dict[str, str]] = []
    answers = summary.get("answers") or {}
    unread = (summary.get("skipped") or {}).get(tag_engine.SOURCES_UNREAD, 0)
    if unread:
        unread_words = (
            searchers.Answer.BLOCKED.value,
            searchers.Answer.UNREACHABLE.value,
            searchers.Answer.PARSE_BREAK.value,
        )
        seen = "; ".join(
            f"{source} {word} on {counted[word]}"
            for source, counted in answers.items()
            for word in unread_words
            if counted.get(word)
        )
        broken = any(
            counted.get(searchers.Answer.PARSE_BREAK.value) for counted in answers.values()
        )
        warnings.append(
            {
                "code": SOURCES_UNREAD,
                "message": (
                    f"{_files(unread)} left untagged because at least one "
                    f"catalogue could not be read for them, so whether any "
                    f"catalogue carries them is unknown. They are not reported as "
                    f"no-hit, and the next run over this folder asks again; each "
                    f"file's record says what every catalogue answered. Across "
                    f"the sweep: {seen}"
                    + (
                        ". A parse break is a defect in this software that "
                        "another run will not move; report it"
                        if broken
                        else ""
                    )
                ),
            }
        )
    for source, counted in answers.items():
        asked = sum(count for word, count in counted.items() if word != searchers.NOT_ASKED)
        if asked and counted.get(searchers.Answer.BLOCKED.value, 0) == asked:
            warnings.append(
                {
                    "code": SOURCE_BLOCKED,
                    "message": (
                        f"{source} refused every one of the {asked} searches it "
                        f"was sent, with a bot check, a block page or a rate "
                        f"limit that outlasted the backoff, rather than a result, "
                        f"so it contributed nothing to this run. This tool does "
                        f"not try to get past one; {source} stays unread until "
                        f"it answers this machine again"
                    ),
                }
            )
    return tuple(warnings)


def _files(count: int) -> str:
    """``1 file was`` or ``N files were``, the head of a sentence about files."""
    return "1 file was" if count == 1 else f"{count} files were"


def _off_taxonomy_warning(summary: dict) -> tuple[dict[str, str], ...]:
    """Say out loud that some of what was tagged is outside the declared table.

    THE PAYLOAD ALONE IS NOT THE FIX, which is the product decision inside this
    unit. R-650's cost is that a person is TOLD the folder tagged cleanly, and a
    count nobody reads leaves that sentence in place on the surface they do read.
    The warning names the strings, so the next move, adding an alias or leaving
    the word alone, is one a person can make without opening the artifacts.

    IT DOES NOT MAKE THE VERB FAIL, and that is deliberate. The files ARE tagged,
    the sweep is unattended by design, and turning a new genre into a failure
    would stop the very acquisition run this tier exists to let through. A
    warning on a success is the shape this module already uses for a no-op it
    wants seen.

    SORTED, because the order artifacts are committed in is the order files were
    walked, and a warning whose text changes between two runs over one unchanged
    folder is one nobody can diff.

    IT SAYS NOTHING ABOUT WHERE THE TRACKS LANDED, and the first draft did. It
    told the person these words route to the fallback bucket, which is the
    ledger entry's own second cost and is FALSE for a measured class: driven on
    2026-09-21, ``Psy-Trance`` and ``Hardcore / Hard Techno`` are both off
    taxonomy and both routed by a fuzzy rule to a real bucket, while ``gqom``
    and ``Leftfield Bass`` landed in the catch-all. The two tiers read two
    different rule lists, so one cannot be read off the other. Telling somebody
    their correctly filed tracks are in the wrong folder is the same defect this
    warning exists to fix, one turn further on, so this says only the part that
    is true of every word it names. Which of them also landed in the catch-all
    is recorded as a residual rather than guessed at here.
    """
    counted = summary.get("off_taxonomy") or {}
    if not counted:
        return ()
    files = sum(counted.values())
    words = ", ".join(sorted(counted))
    return (
        {
            "code": OFF_TAXONOMY,
            "message": (
                f"{files} of the {summary.get('tagged', 0)} files tagged were "
                f"given a genre your taxonomy has no place of its own for, from "
                f"these catalogue answers: {words}. Each word was written onto "
                f"its file exactly as the catalogue said it, so the tags on disk "
                f"are no longer only the ones your template declares; add an "
                f"alias for any you want the taxonomy to own"
            ),
        },
    )


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
        # ONE SUMMARY, READ ONCE. The warning is derived from the same dictionary
        # the payload carries, so the count a person is warned about and the
        # count they can go and read cannot disagree.
        summary = _summary(cfg, job.job_id)
        return ctx.envelope(
            data=shell.reported(store, job, {"tagging": summary}),
            warnings=tuple(warnings)
            + _off_taxonomy_warning(summary)
            + _unread_warnings(summary),
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
        searcher=searchers.for_taxonomy(active_taxonomy.load(cfg)),
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
            "off_taxonomy": result.off_taxonomy,
            # EVERY CATALOGUE'S ANSWER, so a later reader can tell what each one
            # said rather than only the disposition they added up to (R-791).
            "answers": [
                {
                    "source": said.source,
                    "answer": said.answer,
                    "source_genre": said.source_genre,
                    "note": said.note,
                }
                for said in result.answers
            ],
            "unread": {
                said.source: said.answer
                for said in result.answers
                if said.source in result.unread
            },
            "art_repair": result.art_repair,
            "art_repair_detail": result.art_repair_detail,
            "art_fetch": result.art_fetch,
            "art_fetch_detail": result.art_fetch_detail,
        },
    )
