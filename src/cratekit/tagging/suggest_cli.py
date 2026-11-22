"""``crate tag suggest``: offer a genre for a row with none, behind one gate (U114).

THE ORDER IS ``tag rows``'S, for its reasons: the backup acknowledgment before
the plan and the gate (R-733); the plan on a read handle closed before the
gate, refusing a library mostly under no prefix rule first (R-372); the gate
over the digested plan, AN EMPTY PLAN STILL ASKS; and only ``apply`` over a
plan that writes opens the database to write, so a running rekordbox refuses
BEFORE ANY FILE IS WRITTEN.

THE FILE IS WRITTEN FIRST AND THE ROW SECOND: each row checked as the plan read
it, each file written and read back, then the rows whose file read back written
through :func:`cratekit.tagging.rows.apply_rows`, the guarded writer ``tag
rows`` uses. A row write that fails after its file leaves what ``tag rows``
repairs.

WHAT IS WRITTEN IS CHOSEN ON THE COMMAND LINE AND COVERED BY THE DIGEST:
``--band`` the weakest band written, ``--leave`` a row held out, ``--set`` a
genre picked, which is how a split is written. The applying run takes the same
flags and refuses as stale if the plan differs. A row left out is offered again
next run. ``--catalogue`` asks the catalogues, paced, once per candidate, and
keeps their answers a week so the applying run reads the same ones. The gate
takes no inline answer (R34).

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, taxonomy
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.tagging import plan_verbs, rows, searchers, suggest
from cratekit.tagging.plan_verbs import counted, named

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "tag.suggest.confirm"

#: The plan writes nothing.
NOTHING_TO_WRITE = "suggest-nothing-to-write"

#: What the apply wrote and read back.
GENRES_WRITTEN = "suggest-genre-written"

#: Candidates offered and not written, with why.
ROWS_LEFT = "suggest-left"

#: Rows whose file carries a genre their row lacks, which ``tag rows`` writes.
FILE_AHEAD = "suggest-file-has-genre"

#: Rows whose file's genre could not be learned, so nothing was offered.
FILES_NOT_READ = "suggest-file-not-read"

#: Candidates the catalogue could not be read for.
CATALOGUE_UNREAD = "suggest-catalogue-unread"

#: An identifier given to ``--leave`` or ``--set`` names no candidate.
UNMATCHED = "suggest-unmatched"

#: What the majority refusal says cannot be done until a prefix rule exists.
_BLOCKED = "no row's genre can be suggested"

_ORIGIN = ("tagging", "suggest_cli")


def build(parser, entry) -> None:
    """Declare the verb. It reads the whole collection."""
    del entry
    parser.add_argument(
        "--band",
        choices=suggest.BANDS,
        default=suggest.HIGH,
        help="the weakest band of suggestion to write; high unless you say otherwise",
    )
    parser.add_argument(
        "--leave",
        action="append",
        default=[],
        metavar="CONTENT_ID",
        help="leave this row without a genre; repeat it for each row, and give "
        "the same rows again on the run that applies",
    )
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        dest="pick",
        metavar="CONTENT_ID=GENRE",
        help="write this genre on this row whatever was suggested, which is how "
        "a split is written; the genre must be one the taxonomy declares",
    )
    parser.add_argument(
        "--catalogue",
        action="store_true",
        help="also ask the catalogues tag folder asks, paced, once per row, and "
        "Deezer past a refusing Beatport once Discogs answered; the answers are "
        "kept a week so the run that applies reads the same ones",
    )
    parser.set_defaults(_handler=tag_suggest)


def picks(values: list[str], declared: taxonomy.Taxonomy) -> dict[str, str]:
    """Each ``--set`` as a content identifier and a genre, or a refusal.

    REFUSED BEFORE ANY ROW IS READ when one is not of the form, names a genre
    this module may not suggest, a person's pick included, or names one row
    twice with two genres.
    """
    found: dict[str, str] = {}
    for value in values:
        content_id, sep, genre = value.partition("=")
        content_id, genre = content_id.strip(), genre.strip()
        if not sep or not content_id or not genre:
            raise refuse(
                "review-selection-invalid",
                f"--set {value!r} is not CONTENT_ID=GENRE",
                origin=_ORIGIN,
                detail={"set": value},
            )
        if not suggest.suggestable(declared, genre):
            raise refuse(
                "review-selection-invalid",
                f"--set {value!r} names {genre!r}, which the active taxonomy does "
                f"not declare as a genre adoption files by, so this verb will not "
                f"write it",
                origin=_ORIGIN,
                detail={"set": value, "genre": genre},
            )
        if found.get(content_id, genre) != genre:
            raise refuse(
                "review-selection-invalid",
                f"--set names row {content_id} twice, as {found[content_id]!r} and "
                f"as {genre!r}",
                origin=_ORIGIN,
                detail={"content_id": content_id, "genres": [found[content_id], genre]},
            )
        found[content_id] = genre
    return found


def _payload(plan: suggest.SuggestPlan) -> dict[str, Any]:
    return plan_verbs.payload(
        plan,
        rows=plan.rows,
        band=plan.band,
        catalogue=plan.catalogue,
        outcomes=dict(plan.counts),
        groups=plan.groups(),
    )


def _facts(plan: suggest.SuggestPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the groups and the counts."""
    facts: dict[str, Any] = {
        "rows": plan.rows,
        "band": plan.band,
        "groups": plan.groups(),
        "outcomes": dict(plan.counts),
    }
    if plan.unmatched:
        facts["unmatched"] = list(plan.unmatched)
    return facts


def _advisories(plan: suggest.SuggestPlan) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    left = sum(plan.counts[name] for name in suggest.LEFT)
    if left:
        found.append(
            {
                "code": ROWS_LEFT,
                "message": (
                    f"{left} row(s) with no genre were offered and are left as they "
                    f"are ({counted(plan.counts, suggest.LEFT)}), each listed with its "
                    f"votes; --band widens what is written, --set picks a genre for "
                    f"one row, a split's included, and every one is offered again "
                    f"next run"
                ),
            }
        )
    if plan.counts[suggest.FILE_HAS_GENRE]:
        found.append(
            {
                "code": FILE_AHEAD,
                "message": (
                    f"{plan.counts[suggest.FILE_HAS_GENRE]} row(s) carry no genre "
                    f"and their file carries one, which tag rows writes onto the row"
                ),
            }
        )
    if plan.unread:
        found.append(
            {
                "code": FILES_NOT_READ,
                "message": (
                    f"{plan.unread} row(s) were not offered because their file's "
                    f"genre could not be read ({counted(plan.counts, rows.UNREAD)}); a "
                    f"volume that is not mounted reads as {rows.FILE_MISSING}"
                ),
            }
        )
    # A ROW UNREAD ONLY BY A CATALOGUE NOBODY ASKED is said as that, with how to
    # have it asked, never as catalogues that could not be read (U244). A ROW
    # ANOTHER CATALOGUE ANSWERED is said apart, naming the one unread (U322).
    unread = suggest.sort_unread(
        (item.content_id, item.catalogue) for item in plan.items if item.catalogue is not None
    )
    parts = []
    if unread.refused:
        parts.append(
            f"the catalogues could not be read for {len(unread.refused)} row(s), "
            f"{named(list(unread.refused))}, so those were suggested from the library "
            f"alone; a lookup nobody could read is kept for the day and asked "
            f"again on a later one"
        )
    if unread.partly:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those "
            f"were suggested without it"
        )
    if unread.no_token:
        parts.append(
            f"Discogs was not asked about {len(unread.no_token)} row(s), "
            f"{named(list(unread.no_token))}, because no Discogs token is recorded, so "
            f"those were suggested from the library alone; once one is, the next run "
            f"asks it. To record it: {searchers.DISCOGS_LOGIN_STEPS}"
        )
    if unread.token_unusable:
        parts.append(
            f"Discogs was not read for {len(unread.token_unusable)} row(s), "
            f"{named(list(unread.token_unusable))}, because the recorded Discogs token "
            f"could not be used, so those were suggested without it; to record a new "
            f"one: {searchers.DISCOGS_LOGIN_STEPS}"
        )
    if parts:
        found.append({"code": CATALOGUE_UNREAD, "message": "; ".join(parts)})
    if plan.unmatched:
        found.append(
            {
                "code": UNMATCHED,
                "message": (
                    f"--leave or --set named {named(list(plan.unmatched))}, and no "
                    f"row with no genre on the row or the file has that content "
                    f"identifier, so nothing was held or picked for it"
                ),
            }
        )
    return found


def _nothing(plan: suggest.SuggestPlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"no genre is to be written: {len(plan.items)} of {plan.rows} row(s) "
            f"carry no genre on the row or the file, and none has a suggestion at "
            f"or above {plan.band}"
        ),
    }


def _written(written: rows.Written) -> dict[str, str]:
    return {
        "code": GENRES_WRITTEN,
        "message": (
            f"{written.written} row(s) and their files now carry the suggested "
            f"genre, and {written.read_back} read back from the database as "
            f"written, the genre and no other column; a restore of session "
            f"{written.session_id} undoes the rows and NOT the files, which keep "
            f"the genre, so tag rows would write it back onto a restored row"
        ),
    }


def read_plan(
    cfg: config.Config,
    declared,
    *,
    band: str,
    leave: list[str],
    chosen: dict[str, str],
    catalogue: bool,
    progress,
) -> suggest.SuggestPlan:
    """The plan over the library as it stands, through a handle opened to read.
    The one plan, the verb's and ``tag campaign``'s (U294)."""
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        options = {"band": band, "leave": list(leave), "chosen": chosen, "progress": progress}
        if not catalogue:
            return suggest.plan_suggestions(cfg, db, declared, **options)
        with plan_verbs.kept(cfg, declared) as kept:
            return suggest.plan_suggestions(cfg, db, declared, catalogue=kept, **options)


def _write(cfg: config.Config, plan: suggest.SuggestPlan):
    """Check the rows, then inside one session write the files and their rows.

    ONE HANDLE, OPENED TO WRITE BEFORE ANY FILE IS TOUCHED, so a running
    rekordbox refuses with every file as it was. The row engine checks every row
    against the plan, then the files are written in its ``narrow`` step, behind
    the library lock, the volume check and the capture, and only the rows whose
    file read back are handed on.
    """
    held: dict[str, suggest.FilesWritten] = {}

    def files_first(_whole: rows.RowsPlan) -> rows.RowsPlan:
        held["files"] = suggest.write_files(plan)
        return suggest.rows_plan(plan, held["files"].read_back)

    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        written = rows.apply_rows(
            cfg,
            db,
            suggest.rows_plan(plan, (item.content_id for item in plan.writes)),
            analysis_roots=analysis_store.watch_roots(cfg),
            workflow=suggest.WORKFLOW,
            narrow=files_first,
        )
    finally:
        rb_writer.close_db(db)
    return held.get("files", suggest.FilesWritten()), written


def _unwritten(files: suggest.FilesWritten) -> str:
    """The files that did not take their genre, as one clause, or empty."""
    parts = []
    if files.moved:
        parts.append(f"{len(files.moved)} carried a genre by then: {named(list(files.moved))}")
    if files.failed:
        parts.append(f"{len(files.failed)} could not be written: {named(list(files.failed))}")
    if files.wrong:
        parts.append(f"{len(files.wrong)} do not read back: {named(list(files.wrong))}")
    if not parts:
        return ""
    return (
        "these row(s) were left without a genre on the row, because their file did "
        "not take it: " + "; ".join(parts)
    )


def _files_detail(files: suggest.FilesWritten) -> dict[str, list[str]]:
    return {"moved": list(files.moved), "failed": list(files.failed), "wrong": list(files.wrong)}


def _files_refusal(files: suggest.FilesWritten, written: rows.Written):
    """Refuse over the files that did not take their genre, after the rest landed."""
    return refuse(
        "tag-suggest-unwritten",
        f"{written.written} row(s) and their files were written, session "
        f"{written.session_id}; " + _unwritten(files),
        steps=(
            "check each named file can be written and is not open elsewhere",
            "run the verb again, which offers what is left",
        ),
        origin=_ORIGIN,
        detail={**_files_detail(files), "session": written.session_id},
    )


def _read_back(files: suggest.FilesWritten, written: rows.Written) -> None:
    """The row engine's read back, naming the files that did not take theirs too.

    THE READ BACK OUTRANKS THE FILES and keeps its own reason, since a row that
    reads back wrong is this product's defect and a file that would not take a
    genre is the file's; its sentence gains the files' clause.
    """
    try:
        rows.assert_read_back(written)
    except CratekitError as exc:
        clause = _unwritten(files)
        if not clause:
            raise
        cause = exc.cause
        raise refuse(
            cause.reason,
            f"{cause.message}; and {clause}",
            remedy=cause.remediation.remedy,
            steps=cause.remediation.steps,
            origin=_ORIGIN,
            detail={**dict(cause.detail or {}), "files": _files_detail(files)},
        ) from exc


def apply_plan(cfg: config.Config, plan: suggest.SuggestPlan) -> rows.Written:
    """Write the files and then their rows, and refuse over what did not take:
    the read back first, then the files' own refusal. The one apply path, the
    verb's and ``tag campaign``'s (U294)."""
    files, written = _write(cfg, plan)
    _read_back(files, written)
    if not files.clean:
        raise _files_refusal(files, written)
    return written


def tag_suggest(ctx) -> Envelope:
    """Suggest a genre for every row with none, ask, then write file and row."""
    cfg = load_config(("tagging.suggest_cli",))
    declared = active_taxonomy.load(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    chosen = picks(list(getattr(ctx.args, "pick", None) or ()), declared)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    args = ctx.args
    plan = read_plan(
        cfg,
        declared,
        band=args.band,
        leave=list(args.leave or ()),
        chosen=chosen,
        catalogue=bool(args.catalogue),
        progress=getattr(ctx, "progress", None),
    )
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
    return plan_verbs.applied(
        ctx,
        plan,
        data,
        _advisories,
        nothing=_nothing,
        apply=lambda: apply_plan(cfg, plan),
        said=_written,
    )


__all__ = [
    "CATALOGUE_UNREAD",
    "CONFIRM_GATE",
    "FILES_NOT_READ",
    "FILE_AHEAD",
    "GENRES_WRITTEN",
    "NOTHING_TO_WRITE",
    "ROWS_LEFT",
    "UNMATCHED",
    "apply_plan",
    "build",
    "picks",
    "read_plan",
    "tag_suggest",
]
