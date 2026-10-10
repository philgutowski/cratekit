"""``crate tag suggest``: offer a genre for a row with none, behind one gate (U114).

THE ORDER IS ``tag rows``'S, and for its reasons:

* the backup acknowledgment is read before the plan is built and before the
  gate (R-733);
* the plan is made on a handle opened to read and closed before the gate, and a
  library most of whose rows are under no prefix rule refuses before it (R-372);
* the gate is asked over the digested plan, AND AN EMPTY PLAN STILL ASKS;
* only ``apply`` over a plan that writes opens the database with write intent,
  so a running rekordbox refuses there, BEFORE ANY FILE IS WRITTEN.

THE FILE IS WRITTEN FIRST AND THE ROW SECOND. Each row is checked to be as the
plan read it, then each file is written and read back, then the rows whose file
read back are written through :func:`cratekit.tagging.rows.apply_rows`, the
guarded writer ``tag rows`` uses, so file and row agree. A row write that fails
after its file was written leaves exactly what ``tag rows`` repairs.

WHAT IS WRITTEN IS CHOSEN ON THE COMMAND LINE AND COVERED BY THE DIGEST.
``--band`` is the weakest band written, ``high`` unless a person says
otherwise; ``--leave`` holds a row out; ``--set`` picks a genre for a row,
which is how a split is written. The run that applies is given the same flags,
rebuilds the plan, and refuses as stale if it differs. A row left out is not
recorded anywhere and is offered again next run.

``--catalogue`` ASKS THE CATALOGUES, paced, once per candidate, and keeps their
answers for a week so the run that applies reads the same ones.

THE GATE TAKES NO INLINE ANSWER, for the reason ``tag rows`` gives (R34).

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import published, rows, searchers, suggest
from cratekit.write import metadata_cli

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

#: How many identifiers a sentence names. The detail carries all.
_NAMED = 5

_ORIGIN = ("tagging", "suggest_cli")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.suggest_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


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
        help="also ask the catalogues tag folder asks, paced, once per row; the "
        "answers are kept a week so the run that applies reads the same ones",
    )
    parser.set_defaults(_handler=tag_suggest)


def _confirm_gate(entry):
    """The verb's own gate by name, never by position, as ``tag rows`` finds it."""
    for spec in entry.gates:
        if spec.name == CONFIRM_GATE:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {CONFIRM_GATE!r}, so there is no "
        f"question to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": CONFIRM_GATE},
    )


def picks(values: list[str], declared: taxonomy.Taxonomy) -> dict[str, str]:
    """Each ``--set`` as a content identifier and a genre, or a refusal.

    REFUSED BEFORE ANY ROW IS READ when one is not of the form, names a genre
    this module may not suggest, or names one row twice with two genres. A
    genre the taxonomy does not declare is never written by this verb, a
    person's pick included.
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
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {
            "count": len(plan.items),
            "rows": plan.rows,
            "band": plan.band,
            "catalogue": plan.catalogue,
            "outcomes": dict(plan.counts),
            "groups": plan.groups(),
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


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


def _counted(plan: suggest.SuggestPlan, names: tuple[str, ...]) -> str:
    return ", ".join(f"{plan.counts[name]} {name}" for name in names if plan.counts[name])


def _named(values: tuple[str, ...] | list[str]) -> str:
    shown = ", ".join(values[:_NAMED])
    more = len(values) - _NAMED
    return shown + (f" and {more} more" if more > 0 else "")


def _advisories(plan: suggest.SuggestPlan) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    left = sum(plan.counts[name] for name in suggest.LEFT)
    if left:
        found.append(
            {
                "code": ROWS_LEFT,
                "message": (
                    f"{left} row(s) with no genre were offered and are left as they "
                    f"are ({_counted(plan, suggest.LEFT)}), each listed with its "
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
                    f"genre could not be read ({_counted(plan, rows.UNREAD)}); a "
                    f"volume that is not mounted reads as {rows.FILE_MISSING}"
                ),
            }
        )
    unread = [
        item.content_id
        for item in plan.items
        if item.catalogue is not None and item.catalogue.said == suggest.UNREAD
    ]
    if unread:
        found.append(
            {
                "code": CATALOGUE_UNREAD,
                "message": (
                    f"the catalogues could not be read for {len(unread)} row(s), "
                    f"{_named(unread)}, so those were suggested from the library "
                    f"alone; a lookup nobody could read is kept for the day and asked "
                    f"again on a later one"
                ),
            }
        )
    if plan.unmatched:
        found.append(
            {
                "code": UNMATCHED,
                "message": (
                    f"--leave or --set named {_named(list(plan.unmatched))}, and no "
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


def _plan(cfg: config.Config, declared, args, chosen: dict[str, str], progress):
    """The plan over the library as it stands, through a handle opened to read."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        totals = metadata_cli.resolution_totals(cfg, db)
        if totals.majority_unmapped:
            raise CratekitError(
                metadata_cli.majority_unmapped_cause(cfg, totals, blocked=_BLOCKED)
            )
        options = {
            "band": args.band,
            "leave": list(args.leave or ()),
            "chosen": chosen,
            "progress": progress,
        }
        if not args.catalogue:
            return suggest.plan_suggestions(cfg, db, declared, **options)
        lookup = suggest.catalogue_lookup(
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
        )
        with suggest.KeptCatalogue(cfg, lookup) as kept:
            return suggest.plan_suggestions(cfg, db, declared, catalogue=kept, **options)
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: suggest.SuggestPlan):
    """Check the rows, then inside one session write the files and their rows.

    ONE HANDLE, OPENED TO WRITE BEFORE ANY FILE IS TOUCHED, so a running
    rekordbox refuses with every file as it was. The row engine then checks
    every row against the plan, so a row that gained a genre since refuses with
    nothing written, and enters the session spine: the library lock, the volume
    check and the capture all come before the first file is written, because
    the files are written in the engine's ``narrow`` step, and only the rows
    whose file read back are handed on.
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
        parts.append(f"{len(files.moved)} carried a genre by then: {_named(list(files.moved))}")
    if files.failed:
        parts.append(f"{len(files.failed)} could not be written: {_named(list(files.failed))}")
    if files.wrong:
        parts.append(f"{len(files.wrong)} do not read back: {_named(list(files.wrong))}")
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
    genre is the file's. Its sentence gains the files' clause, so neither is
    reported at the cost of the other.
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


def tag_suggest(ctx) -> Envelope:
    """Suggest a genre for every row with none, ask, then write file and row."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = _confirm_gate(ctx.entry)
    chosen = picks(list(getattr(ctx.args, "pick", None) or ()), declared)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, declared, ctx.args, chosen, getattr(ctx, "progress", None))
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
    if not plan.writes:
        return ctx.envelope(
            data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan), *_advisories(plan)]
        )

    files, written = _write(cfg, plan)
    _read_back(files, written)
    if not files.clean:
        raise _files_refusal(files, written)
    data["totals"] = {
        **data["totals"],
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(written), *_advisories(plan)])


__all__ = [
    "CATALOGUE_UNREAD",
    "CONFIRM_GATE",
    "FILES_NOT_READ",
    "FILE_AHEAD",
    "GENRES_WRITTEN",
    "NOTHING_TO_WRITE",
    "ROWS_LEFT",
    "UNMATCHED",
    "build",
    "picks",
    "tag_suggest",
]
