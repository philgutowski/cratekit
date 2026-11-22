"""``crate tag retag``: confirm the selection, then run the correction.

THE PLAN IS THE SELECTION, the files whose genre is too coarse, never what each
becomes: that lookup is the long work, and running it first would make the gate
decorative. THE RESUME DIGESTS THE FROZEN PAYLOAD, NEVER A FRESH WALK (KTD8,
R13), since a corrected file is no longer selected. The gate is found by its
digest source, not its position. This verb writes the file half only (R-185,
R-246), so a run names ``tag rows`` through :func:`library_row_warning`. AN
EMPTY SELECTION STILL ASKS AND QUEUES NOTHING (R12): every declared gate fires,
and a job with no items would report a clean success.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

Layer: modules.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Mapping, Sequence

from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import active_taxonomy, config, jobs, review, tags
from cratekit.core.cause import (
    CratekitError,
    Outcome,
    rebuilt,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import artifacts, retag, searchers, shell

#: The digest source the registry declares for the gate this handler answers.
PLAN = "plan"

#: Where the confirmed rows live in the frozen payload, spelled once because the
#: enqueue writes it and the resume reads it.
ITEMS_KEY = "items"

#: Where the folder lives in the frozen payload. It is in the digest too.
FOLDER_KEY = "folder"

#: The warning naming the half this build does not write, built in one place
#: since the queueing and the resume envelopes both carry it.
LIBRARY_ROW_STALE = "library-row-not-updated"


def library_row_warning(folder: str) -> dict[str, str]:
    """What the person still has to do, because the row is not this verb's: the
    act, ``tag rows``, and the folder, in a tense true at queueing, a resume and a
    failure. Not a pending human action, which nothing could verify (R-567)."""
    return {
        "code": LIBRARY_ROW_STALE,
        "message": (
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
            f"value, because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up, which writes each row's genre from its "
            f"file and no other column, where a reload in rekordbox overwrites "
            f"every tag field; that verb plans over the whole collection and not "
            f"this folder, lists every row it would write before it asks, and "
            f"leaves a genre the library has never held, saying what to do about it"
        ),
    }


def with_reload_step(error: CratekitError, folder: str) -> CratekitError:
    """The same refusal, carrying the reload among the steps, for a half
    corrected sweep leaving through its cause (R-225, R-185); every other field and
    the type the dispatcher reads (R-290) are carried by construction."""
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


#: Every reason a selected file can go unwritten, zero filled in the report, for
#: the rule :func:`cratekit.adopt.scan.categories` states.
REASONS: tuple[str, ...] = (
    retag.NO_GENRE, retag.GENRE_SPECIFIC, retag.NO_ANSWER, retag.ANSWER_TOO_COARSE,
    retag.DECLINED_IN_REVIEW,
)


def _plan_gate(ctx):
    """The declared gate whose decision is made against the plan, or a refusal:
    a dropped gate must not run a destructive sweep with nobody asked."""
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
    """The identity of one plan, this folder and these rows: the walk's on the
    first invocation, the frozen rows' on the resume (KTD8). Pure."""
    return digest_of(
        {
            "kind": "tag.retag",
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
        }
    )


def plan_for(folder: str, declared) -> dict:
    """The plan this verb shows and the digest its decision is recorded against,
    apart from the handler so the digest can be tested without driving the verb."""
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
    """The command line that continues one queued retag, carrying ``--run`` so
    the spawned child answers the explicit gate against the recorded run (R34)."""
    payload = job.payload or {}
    folder = str(payload.get(FOLDER_KEY) or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say happened to the folder: what ran,
    read back from disk so it stays true across a resume."""
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
    """The payload and warning for a folder with no genre to correct: nothing is
    queued and the envelope says which zero, in :func:`cratekit.tagging.shell.no_op`'s
    shape so R-234's null ``job_id`` cannot return."""
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def retag_genres(ctx) -> Envelope:
    """Offer the selection, wait for the confirmation, then queue and run it.
    An unnamed folder refuses first, since ``Path("")`` is the current directory;
    the folder is frozen absolute for the resume."""
    named = str(ctx.args.folder or "")
    if not named:
        raise refuse(
            "tag-retag-folder-unknown",
            "tag retag needs the folder whose genres it should correct",
            steps=("pass the folder after the verb",),
            origin=("tagging", "retag_cli"),
        )
    cfg = load_config(("tagging.retag_cli",))
    if ctx.args.job:
        return _resume(ctx, cfg)

    folder = str(Path(named).expanduser().absolute())
    plan = plan_for(folder, active_taxonomy.load(cfg))
    # THE PLAN IS SHOWN THROUGH THE GATE LAYER (R-693), the folder in front.
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
                # THE CONFIRMED ROWS, FROZEN, which the resume digests.
                ITEMS_KEY: plan["items"],
                # The gate run, which the respawned child names. See ``retag_argv``.
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            # ONE CONFIRMED CANDIDATE IS ONE ITEM, named by its absolute path.
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
            cfg=cfg,
        )
        # UNCONDITIONAL HERE: this is the last envelope the person reads before
        # the detached child runs, and a sweep correcting none is the rare case.
        return ctx.envelope(
            data=shell.reported(store, job),
            warnings=(library_row_warning(folder),),
        )


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Answer the gate from the FROZEN plan, walking nothing, then drive the
    job's items through :func:`cratekit.tagging.shell.advance`, naming the reload
    on either ending when a file was corrected."""
    with jobs.open_store() as store:
        queued = jobs.get(store, ctx.args.job)
        payload = queued.payload or {}
        folder = str(payload.get(FOLDER_KEY) or "")
        rows = [dict(row) for row in payload.get(ITEMS_KEY) or ()]
        # THE FROZEN PLAN IS SHOWN THE WAY THE FIRST ASK SHOWED IT (R-693).
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
        # ON WHAT RAN: a sweep that corrected nothing left no row stale.
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
        return ctx.envelope(
            data=shell.reported(store, job, {"retag": summary}),
            warnings=warnings,
        )


def handle(job, item, cfg) -> jobs.Produced:
    """Correct ONE file's genre. The per item worker behind ``tag.retag``.

    THE GENRE IS RE-READ AT DRIVE TIME: a gone file refuses, a blank one is ``tag
    folder``'s and one now specific is kept. The searcher is looked up on the
    module at call time (KTD11, R23), the configuration is the frozen one (KTD9),
    and the report keeps the previous value, the record of stale rows (R-185).
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
                # Off the job, so the queue names the verb it was queued under.
                handler_key=job.handler_key,
            )
    if result.reason == retag.UNWRITTEN_REASON:
        # THE ITEM FAILS AND THE REST OF THE JOB GOES ON (R-1103), as in ``tag
        # folder`` (U178). No report is committed, so it is never counted corrected.
        raise refuse(
            retag.UNWRITTEN_REASON,
            f"{path} would not take the genre {result.proposed!r}, so it still "
            f"carries {result.current!r}; nothing else about it was changed",
            steps=(
                "check the file can be written, is not locked and is not on a read "
                "only volume, then run tag retag over the folder again",
            ),
            origin=("tagging", "retag_cli"),
            detail={
                "item": item.item_id,
                "path": str(path),
                "genre": result.proposed,
                "current": result.current,
            },
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
    "FOLDER_KEY", "ITEMS_KEY", "LIBRARY_ROW_STALE", "REASONS", "build", "digest_for", "handle",
    "library_row_warning", "plan_for", "retag_argv", "retag_genres", "with_reload_step",
]
