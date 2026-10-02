"""``crate tag retag``: confirm the selection, then run the correction.

WHAT THE PERSON IS CONFIRMING. The plan is the SELECTION, every file under the
folder whose genre the declared taxonomy calls too coarse to be a final tag, and
nothing else. It deliberately does not carry what each file will become, because
the lookup that answers that is the long-running work and running it before the
gate would make the gate decorative: the sweep would already have happened.

THE DIGEST IS OVER THAT SELECTION, so a person who approves forty files and then
drops another hundred into the folder gets a stale decision rather than a wider
sweep than the one they agreed to. :func:`cratekit.tagging.retag.select` sorts,
which is what makes the digest stable across two runs over one unchanged folder.

**AND THE RESUME DIGESTS THE FROZEN PAYLOAD RATHER THAN A FRESH WALK** (KTD8,
R13). This module used to rebuild the plan on every invocation, the resume
included, which was correct only while nothing wrote. A corrected file carries a
specific genre, so the next walk does not select it, so the plan digests
differently from the one the confirmation was recorded against, so
``cratekit.cli.gates`` raises ``DecisionStale``. Every respawn after the first
partial run meets it, for ever, over work somebody already approved. Measured
before the split as exit 11, ``the decision on 'tag.retag.confirm' was made
against a plan that has since changed``, on a job whose first file had been
corrected. So the rows the person approved are FROZEN in the payload and the
resume digests those, which is the rule
:func:`cratekit.modules.outbound.shell.resume` already states for the two
outbound verbs: the child the job engine spawns rebuilds its command line from
that payload, so both sides of the comparison have to be built from the same
frozen values or nothing can ever finish.

THE GATE IS FOUND BY ITS DIGEST SOURCE AND NOT BY POSITION. Indexing ``gates[0]``
would silently answer the wrong question the day somebody reorders the tuple. The
neighbour that made this concrete was the cloud-sync decision, which this entry
declared until the write narrowing below took it off: that decision belongs to
the guarded writer and is answered wherever that refusal is raised, and this verb
opens no database, so it could never raise it. The rule outlives the neighbour,
because the next verb to gain a second gate finds the handler already correct.

THE RUN ENDS BY NAMING THE VERB THAT WRITES THE ROW. The file carries the
corrected genre and the library row does not, because this verb writes the file
half only (R-185). The registry no longer claims that surface (R-246), so the
declaration and the code agree, and the envelope carries
:func:`library_row_warning`, which names the one act that makes the row agree
with the file. That act was a reload in rekordbox until the residual on stale
row genres gave the row a verb of its own, ``tag.rows``. A reload overwrites
every tag field, and at one sitting it changed keys, so it is no longer what
this verb sends a person to do. The queueing envelope carries it unconditionally and a successful
resume carries it only when a file was actually corrected; each of those two
functions says why at the line that attaches it.

AN EMPTY SELECTION STILL ASKS, AND STILL QUEUES NOTHING (R12). The first draft
of this unit skipped the gate when the plan was empty, on the argument that a
person's decision should not be spent on a sweep of nothing. That argument is
real and it loses to two things. Conformance 3 holds every declared gate to
FIRING, and a gate the registry declares and the verb sometimes skips is a
decision the product promises and does not always ask;
``tests/test_cli_contract.py`` reported it as unreachable within minutes.
:mod:`cratekit.adopt.apply_cli` had already decided the same question the other
way and says so in its own docstring, so skipping here would have left two
sibling verbs disagreeing about what an empty plan means. So the gate fires, and
THE ZERO ITEM RULE IS ENFORCED AFTER IT, by refusing to create a job at all when
the plan holds nothing: ``core.jobs`` drives a job with no items straight to
SUCCEEDED, so queueing one would report a clean correction over a folder nothing
touched.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

Layer: modules.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Mapping, Sequence

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, config, jobs, review, tags
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Outcome,
    Remediation,
    rebuilt,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import artifacts, retag, searchers, shell

#: The digest source the registry declares for the gate this handler answers.
PLAN = "plan"

#: Where the confirmed plan rows live in the frozen payload. Spelled once,
#: because the enqueue writes this key and the resume reads it, and a key one
#: side spells differently is a resume that digests an empty plan and refuses a
#: decision that was never stale.
ITEMS_KEY = "items"

#: Where the folder lives in the frozen payload. It is in the digest as well as
#: the rows, so the resume has to read it back from the same place
#: :func:`retag_argv` does.
FOLDER_KEY = "folder"

#: The warning code that names the half this build does not write. One slug, one
#: text, built in one place, because the queueing envelope and the resume
#: envelope both carry it and two spellings of one instruction is how a person
#: reads two different stories about one run.
LIBRARY_ROW_STALE = "library-row-not-updated"


def library_row_warning(folder: str) -> dict[str, str]:
    """What the person still has to do, because the row is not this verb's.

    THE ACT IS NAMED, NOT THE DEFECT. The file now carries the specific genre
    and the library row still carries the value the taxonomy called too coarse,
    because this verb writes the file half only (R-185). A person who is told
    only that the two disagree cannot act on it. The act is the row's own verb,
    which writes the genre from the file and no other column. It was a reload
    of the folder's tags in rekordbox before that verb existed, and a reload
    overwrites every tag field, so the message names the verb and says why not
    the reload.

    IT NAMES THE FOLDER. A resume is a detached child whose envelope a person
    reads later, next to other runs, so a warning that said "the folder" would
    leave them guessing which sweep it belonged to.

    THE TENSE IS THE PROPERTY OF THE VERB, NOT A REPORT OF THIS RUN, and that is
    what lets one text serve three moments. It is attached at queueing, before a
    single file has been looked at, on a resume that corrected files, and on a
    failure that corrected some of them. A sentence saying the genre WAS
    corrected would be false at the first of those: the confirmed sweep has not
    started, and one that refuses on its first item never corrects anything,
    so the person would have been sent to rekordbox over a folder nothing
    touched. What is true at all three is what this verb does and does not
    write, so the message states that and then names the act.

    AND IT IS NOT A PENDING HUMAN ACTION, which is the conservative call here
    rather than an oversight. That field is mandatory-verified by construction,
    ``verify_verb`` names a registered verb that proves the act was done, and
    nothing in this build can read the row back to prove a reload landed: a
    corrected file is never selected again, so a second retag over the folder
    reports the same clean zero whether the person reloaded or not. A pending
    action nobody can verify is the printed instruction that field exists to
    replace. Recorded as R-567 rather than faked with a verb that would answer
    the question wrong.
    """
    return {
        "code": LIBRARY_ROW_STALE,
        "message": (
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
            f"value, because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up, which writes each row's genre from its "
            f"file and no other column, where a reload in rekordbox overwrites "
            f"every tag field"
        ),
    }


def with_reload_step(error: CratekitError, folder: str) -> CratekitError:
    """The same refusal, carrying the reload among the things left to do.

    THE HALF CORRECTED SWEEP IS THE RUN THAT MOST NEEDS THIS AND IS THE ONE THAT
    WAS MISSING IT. R-225 makes a job that closed carrying a cause leave through
    that cause rather than through a normal envelope, which is right: a person
    whose folder was half corrected must not be told the sweep succeeded. The
    consequence was that the resume's warning, which rides a successful envelope,
    never reached exactly the interrupted run R-185 describes. The files that were
    corrected before the failure have stale rows whether or not the rest of the
    sweep ran.

    THE STEP IS APPENDED AND THE CAUSE IS OTHERWISE UNTOUCHED. ``origin`` is
    append-only and a cause arriving at the CLI with a shortened trail means some
    hop re-created it, losing everything below, so this replaces two fields and
    carries ``origin``, ``inner``, ``detail``, ``scope`` and ``retryable``
    through by construction rather than by rebuilding them. The remedy token
    stays whatever the failure's own is: retrying is still the first thing to do,
    and the reload is what is owed regardless of whether the retry happens.

    AND THE TYPE IS CARRIED THROUGH TOO, which the first version of this did not
    do. A parked job leaves as ``JobBlocked`` and the dispatcher reads that type,
    not anything on the cause, as the blocked outcome (R-290). Rebuilding it as a
    plain ``CratekitError`` said ``failed`` over a job whose state was blocked,
    for exactly the retag parked after correcting a file.
    """
    cause = error.cause
    reload_step = library_row_warning(folder)["message"]
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(
                cause.remediation, steps=(*cause.remediation.steps, reload_step)
            ),
        )
    )


#: Every reason a selected file can go unwritten, zero filled in the report. A
#: summary listing only the reasons it happened to see makes "none of those here"
#: and "this build does not count that" the same output, which is the rule
#: :func:`cratekit.adopt.scan.categories` states.
REASONS: tuple[str, ...] = (
    retag.NO_GENRE,
    retag.GENRE_SPECIFIC,
    retag.NO_ANSWER,
    retag.ANSWER_TOO_COARSE,
    retag.DECLINED_IN_REVIEW,
)


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.retag_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _plan_gate(ctx):
    """The declared gate whose decision is made against the plan.

    Refuses rather than defaulting when there is none. A handler that quietly
    skipped its confirmation because a registry edit dropped the gate would run a
    destructive sweep with nobody asked, and the conformance suite's reach check
    reads the registry rather than this file, so it would report the verb clean.
    """
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
    raise refuse(
        "refused-by-policy",
        "this verb is destructive and its registry entry declares no decision "
        "made against the plan, so there is nothing for a person to confirm",
        remedy=Remedy.REPORT_DEFECT,
        origin=("tagging", "retag_cli"),
        detail={"verb": ctx.entry.name},
    )


def digest_for(folder: str, items: Sequence[Mapping[str, str]]) -> str:
    """The identity of one plan: this folder, and these rows.

    PURE, AND THE REASON THE SPLIT EXISTS. Two callers need this answer and only
    one of them can walk a folder for it. The first invocation digests the walk;
    the resume digests the rows the person's confirmation was recorded against,
    which by then are the only description of that plan still in existence
    (KTD8).

    THE FOLDER IS IN THE DIGEST as well as the rows. Two different empty folders
    are two different decisions: approving a sweep of one is not approving a
    sweep of the other, and without the folder both would digest identically and
    a decision recorded against one would satisfy the gate for the other.

    The rows are re-built as plain dictionaries so a payload that has been
    through JSON digests identically to the plan it was frozen from.
    """
    return digest_of(
        {
            "kind": "tag.retag",
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
        }
    )


def plan_for(folder: str, declared) -> dict:
    """The plan this verb shows and the digest its decision is recorded against.

    SEPARATE FROM THE HANDLER ON PURPOSE. Built inline, the digest could only be
    reached through a configured machine, a job store and a gate, so the one
    property that matters most about it, that it is a function of what the person
    was shown, was measurable only by driving the whole verb. A mutation
    replacing it with a constant killed no test.
    """
    items = retag.plan_items(retag.select(Path(folder), declared=declared))
    return {
        "digest": digest_for(folder, items),
        "items": items,
        "totals": {"count": len(items)},
    }


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("folder", help="folder of audio whose genres may be too coarse")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the retag already queued under this identifier",
    )
    parser.set_defaults(_handler=retag_genres)


def retag_argv(job) -> list[str]:
    """The command line that continues one queued retag.

    IT CARRIES ``--run``. The confirm gate is ``explicit``, so R34 makes it
    answerable only by a separate act recorded against a run, and the child
    :mod:`cratekit.core.jobs` spawns is a fresh process in which ``cli.run`` mints
    a NEW run whenever ``--run`` is absent. A resume naming only the job would meet
    the gate with nothing recorded and exit DECISION_REQUIRED, and so would every
    respawn after it, leaving a confirmed sweep in the queue for ever. Two shipped
    verbs were driven to exactly that on 2026-08-23.

    The flag goes BEFORE the verb path because ``--run`` belongs to the root
    parser: a decision belongs to the invocation rather than to the subcommand.

    A job frozen by an older build carries no gate run and resumes without the
    flag, which returns it to the refusal it was already in rather than crashing a
    detached child whose only output is a log nobody is watching.
    """
    payload = job.payload or {}
    folder = str(payload.get(FOLDER_KEY) or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say happened to the folder.

    DERIVED FROM WHAT RAN, never from what was confirmed. The plan is a list of
    files somebody agreed to look at, and by drive time one of them has been
    corrected by hand, one has lost its genre altogether and one is gone. A
    report built from the plan would name all three as corrected, which is the
    clean-report-over-unwritten-state shape the merge bar exists to catch.

    READ BACK RATHER THAN ACCUMULATED IN MEMORY, which is what makes the number
    true across a resume: a sweep that corrected three of ten files and is
    continued tomorrow has ten reports on disk, and the person asking what
    happened means all ten.
    """
    skipped = {reason: 0 for reason in REASONS}
    corrected = 0
    asked = 0
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("reason") or "")
        if reason in skipped:
            skipped[reason] += 1
        elif report.get("written"):
            corrected += 1
        if reason in {retag.NO_ANSWER, retag.ANSWER_TOO_COARSE} and report.get(
            "review_item"
        ):
            asked += 1
    return {"corrected": corrected, "skipped": skipped, "asked": asked}


def _empty(reason: str, detail: str) -> tuple[dict, tuple[dict[str, str], ...]]:
    """The payload and warning for a folder with no genre to correct.

    THE HONEST ZERO, and it is a different thing from a job with no items.
    ``core.jobs`` reports a job with no items as SUCCEEDED by design, so a verb
    that queued one here would report a clean correction over a folder it never
    touched. The person was still asked, because the gate fires first; nothing is
    queued, and the envelope says which zero this is.

    THE PAYLOAD SHAPE IS :func:`cratekit.tagging.shell.no_op`'s rather than this
    module's, so the zero paths the two tagging verbs have cannot reintroduce
    R-234's null ``job_id`` separately.
    """
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def retag_genres(ctx) -> Envelope:
    """Offer the selection, wait for the confirmation, then queue and run it.

    THE UNNAMED FOLDER IS REFUSED BEFORE ANYTHING ELSE HAPPENS, including before
    the configuration is read. An empty string is a valid argument to a positional
    that takes one, so the parser accepts it, and ``Path("")`` is the CURRENT
    DIRECTORY: this verb rewrites the genre on every file it selects, so
    defaulting would correct whatever the person happens to be standing in. It has
    a slug of its own in ``cause.REASONS`` because it is this verb's refusal
    rather than a fact about a folder, which is what separates it from the two
    warnings below.

    THE GATE COMES BEFORE THE ZERO. An empty plan is still a plan a person can
    abort, and the folder is in its digest, so approving an empty sweep of one
    folder does not approve one of another. Nothing is queued afterwards either
    way. See the module docstring for why the first draft had this the other way
    round and what reported it.

    THE FOLDER IS FROZEN ABSOLUTE. A resume is a fresh process the job engine
    spawns, and a relative folder would resolve against whatever directory that
    process happens to start in, which is a correction pass over some other folder
    wearing this job's identifier. The digest is taken over the same absolute
    string the payload freezes, so the two sides of the resume's comparison cannot
    disagree about which folder was approved.
    """
    named = str(ctx.args.folder or "")
    if not named:
        raise refuse(
            "tag-retag-folder-unknown",
            "tag retag needs the folder whose genres it should correct",
            steps=("pass the folder after the verb",),
            origin=("tagging", "retag_cli"),
        )
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)

    folder = str(Path(named).expanduser().absolute())
    plan = plan_for(folder, active_taxonomy.load(cfg))
    # THE PLAN IS SHOWN THROUGH THE GATE LAYER (R-693): each file with the
    # genre it carries, the digest they were taken over, and the folder in
    # front of them, so a person confirms a sweep they have read.
    option = ctx.gate.require(_plan_gate(ctx), plan=plan, context={FOLDER_KEY: folder})
    if option == "abort":
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)

    if not plan["items"]:
        payload, warnings = (
            _empty(
                "tag-retag-nothing-coarse",
                f"no file under {folder} carries a genre this taxonomy calls too "
                f"coarse to be a final tag, so there is nothing to correct",
            )
            if Path(folder).is_dir()
            else _empty(
                "tag-retag-folder-absent",
                f"{folder} is not a folder on this machine, so there is nothing "
                f"to correct",
            )
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                FOLDER_KEY: folder,
                # THE CONFIRMED ROWS, FROZEN. They are what the resume digests,
                # and they are the only description of the approved plan that
                # survives the first file being corrected. See the module
                # docstring for the stall this closes.
                ITEMS_KEY: plan["items"],
                # THE GATE RUN IS FROZEN so the respawned child can name the run
                # the confirmation was recorded against. See ``retag_argv``.
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            # ONE CONFIRMED CANDIDATE IS ONE ITEM, named by its path. Without
            # them the queue holds a job with nothing to claim and the driver
            # reports an empty success over a correction it never made. The path
            # is absolute because the plan row is, and because a worker joining a
            # relative one onto its own working directory is the same defect the
            # frozen folder above exists to prevent.
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
            cfg=cfg,
        )
        # UNCONDITIONAL HERE, AND CONDITIONAL ON THE RESUME, for a reason that
        # is about who is reading. This envelope is the one the person gets back
        # in the terminal from the command they typed, before the detached child
        # runs anything, so it cannot yet know how many files will be corrected
        # and it is the last thing they read before walking away. Every file in
        # this plan was selected for carrying a genre the taxonomy calls too
        # coarse, so a sweep that corrects none of them is the unusual case and
        # "you may have nothing to reload" is a cheaper wrong answer than
        # silence. The resume knows what actually happened and says so there.
        return ctx.envelope(
            data=shell.reported(store, job),
            warnings=(library_row_warning(folder),),
        )


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the FROZEN plan, then drive the job's items.

    THIS BRANCH WALKS NOTHING. The rows are already in the payload and the items
    are already in the queue, so re-deriving them would make the resume ask its
    question about a folder that the run it is continuing has itself been
    changing. That is the stall the module docstring records, and it is the same
    rule :func:`cratekit.modules.outbound.shell.resume` states: the child the job
    engine spawns rebuilds its command line from this payload, so both sides of
    the comparison have to be built from the same frozen values.

    ABORT IS STILL ANSWERABLE HERE. A person who confirmed a sweep may stop it
    between the queueing and the drive, and the reply is the declared
    ``job_state`` shape rather than a summary of its own, so this zero cannot
    reintroduce R-234's null ``job_id``.

    EVERY OTHER RULE OF THE RESUME LIVES IN :func:`cratekit.tagging.shell.advance`,
    which reconciles a claim left by a driver that died, refuses a job carrying no
    items, drives, and raises rather than reporting when the job closed carrying a
    cause. That last one is R-225: a person whose folder was half corrected must
    not be handed a normal envelope the dispatcher exits 0 over.

    AND THAT RAISE IS WHY THE RELOAD IS NAMED ON BOTH ENDINGS. A half corrected
    folder has stale rows exactly as a fully corrected one does, and it leaves
    through the cause rather than through this function's envelope, so a warning
    attached only below would miss the run R-185 is actually about. The refusal
    gains the reload as one more step when the committed artifacts say a file was
    corrected, and gains nothing when none was.
    """
    with jobs.open_store() as store:
        queued = jobs.get(store, ctx.args.job)
        payload = queued.payload or {}
        folder = str(payload.get(FOLDER_KEY) or "")
        rows = [dict(row) for row in payload.get(ITEMS_KEY) or ()]
        # THE FROZEN PLAN IS SHOWN THE WAY THE FIRST ASK SHOWED IT (R-693):
        # the rows the confirmation was recorded against, and their digest.
        option = ctx.gate.require(
            _plan_gate(ctx),
            plan={"digest": digest_for(folder, rows), "items": rows},
            context={FOLDER_KEY: folder},
        )
        if option == "abort":
            return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=("tagging", "retag_cli"),
                nothing_to_run="report a correction over files it never looked at",
            )
        except CratekitError as failed:
            # THE REFUSAL CARRIES THE RELOAD WHEN ANYTHING WAS CORRECTED. The
            # artifacts are committed per item before the failure, so this
            # counts what actually landed rather than what was confirmed, and a
            # sweep that refused on its first item adds nothing to a refusal it
            # has no reload to name. See ``with_reload_step``.
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
        summary = _summary(cfg, job.job_id)
        # ON WHAT RAN, NEVER ON WHAT WAS CONFIRMED, which is the rule
        # ``_summary`` already states, applied to the warning as well as to the
        # report. A sweep whose every file was skipped or went to the review
        # queue corrected nothing, so no row went stale, so sending a person to
        # rekordbox would be work the run did not create for them. ``corrected``
        # is read back from the committed artifacts, so it stays true across a
        # resume: a job continued tomorrow counts what all of its runs wrote.
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
        return ctx.envelope(
            data=shell.reported(store, job, {"retag": summary}),
            warnings=warnings,
        )


def handle(job, item, cfg) -> jobs.Produced:
    """Correct ONE file's genre. The per item worker behind ``tag.retag``.

    THE GENRE IS RE-READ AT DRIVE TIME AND THE FROZEN ROW IS NOT TRUSTED. The
    plan is a description of the folder as it stood when somebody was asked, and
    the folder is not frozen. Between then and now a person may have corrected
    the file themselves, cleared the field, or deleted it, and each of those is a
    different answer this worker owes rather than a write it should make anyway.

    A FILE THAT IS GONE IS REFUSED WITH ITS OWN SLUG rather than reported done,
    on the rule ``adopt/scan_cli.handle`` states: an item that reported done
    having corrected nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. ``source-missing`` rather than a slug of this
    verb's own, because its reserved remediation is "nothing was read and nothing
    was written", which is exactly what this refusal promises. The sibling verb
    reuses it for the same reason.

    A BLANK GENRE BELONGS TO THE OTHER VERB. ``tag.folder`` owns an empty field
    under fill-if-empty and this verb owns the value it writes, so a file with
    nothing in the field must not be corrected here: one field under two policies
    is how a value a person set by hand loses to whichever verb ran last. The
    taxonomy answers ``is_too_coarse_as_source("")`` with True, which is why the
    check is for the blank rather than for the predicate.

    A GENRE THAT IS NOW SPECIFIC IS SOMEBODY'S CURATION and is reported rather
    than replaced. Writing anyway would make a queued job the thing that
    overwrites a person's own answer.

    THE SEARCHER IS LOOKED UP RATHER THAN CONSTRUCTED (KTD11, R23).
    ``ItemHandler`` is a fixed three argument callable, so a worker that built its
    own searcher inline would leave a test nowhere to hand a fake in and R18's no
    network proof unwritable. The lookup happens at CALL TIME, on the module
    rather than on a name imported from it, which is what makes the substitution
    reach this line. R-226 records the honest limit: the child ``crate job
    resume`` spawns is a fresh process and inherits nothing patched in another
    one, so a detached run always gets the live searcher.

    THE CONFIGURATION IS THE FROZEN ONE AND IS NOT LOADED HERE, and the review
    queue is opened against it. KTD9 closes the recorded resume bug where a
    queued run re-resolved its configuration; a handler that loaded one is that
    defect wearing a new hat, and a worker that opened the queue against a
    freshly loaded configuration would ask a person the same question in two
    places the day that path moves.

    THE REPORT CARRIES THE PREVIOUS VALUE AS WELL AS THE WRITTEN ONE, and that is
    load bearing rather than tidy. The database half of this verb is deferred, so
    the library row keeps the catch-all after the file stops carrying it, and a
    corrected file is never selected again. These artifacts are therefore the only
    record of which rows went stale, which is what the deferred half will read
    when it lands (R-185). ``written`` is also what the resume counts to decide
    whether the folder needs a reload at all, so a field dropped from this report
    silently stops a person being told.
    """
    path = Path(item.item_id)
    if not path.is_file():
        raise refuse(
            "source-missing",
            f"{path} is no longer a file, so there is nothing to correct for this "
            f"item. Nothing was read and nothing was written",
            steps=(
                "run the correction verb again over the folder as it now stands; "
                "this job was confirmed against a folder that has since changed",
            ),
            origin=("tagging", "retag_cli"),
            detail={"item": item.item_id},
        )
    declared = active_taxonomy.load(cfg)
    current = tags.read_genre_from_file(path) or ""
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
    elif not declared.is_too_coarse_as_source(current):
        result = retag.RetagResult(
            path=path, current=current, reason=retag.GENRE_SPECIFIC
        )
    else:
        with review.open_store(cfg) as store:
            result = retag.retag_one(
                retag.Candidate(path=path, current=current),
                searcher=searchers.for_taxonomy(declared),
                declared=declared,
                decided=retag.decided_index(store),
                store=store,
                # OFF THE JOB rather than spelled again here, so the queue the
                # person answers from names the verb the job was queued under
                # even if the two ever come to differ.
                handler_key=job.handler_key,
            )
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(result.path),
            "current": result.current,
            "written": result.written,
            "reason": result.reason,
            "proposed": result.proposed,
            "review_item": result.item_id,
        },
    )


__all__ = [
    "FOLDER_KEY",
    "ITEMS_KEY",
    "LIBRARY_ROW_STALE",
    "REASONS",
    "build",
    "digest_for",
    "handle",
    "library_row_warning",
    "plan_for",
    "retag_argv",
    "retag_genres",
    "with_reload_step",
]
