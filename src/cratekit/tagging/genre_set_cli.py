"""``crate tag set GENRE``: give chosen rows a genre over the one they carry (U339).

The engine is :mod:`cratekit.tagging.genre_set`. THE ORDER IS ``analyze
adopt``'S: the genre refused first when the taxonomy does not declare it, then
the backup acknowledgment, then the plan on a read handle closed before the
gate; the explicit gate over the digest, taking no inline answer, AN EMPTY PLAN
STILL ASKS; only ``apply`` over a plan that writes opens the database to write,
takes the plan again on that handle and refuses ``decision-stale`` if it moved.
``--leave`` holds a row out, in the plan and its digest. A genre the library
has no lookup row for shows ``mint`` at the gate, and the apply makes the row
on the commit that links it. A run that wrote names
``adopt apply``, which files the rows under the new genre's folder, and
``adopt move`` where a row leaves the genre folder its old genre filed it in.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from cratekit.adopt import placements
from cratekit.cli import output
from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome, refuse
from cratekit.tagging import genre_set as gs
from cratekit.tagging import plan_verbs
from cratekit.tagging.plan_verbs import counted, named, warning

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "tag.set.confirm"

#: The warnings: nothing to write, what was written and read back, rows left,
#: a ``--leave`` naming no row in scope, a genre row the apply would make, and
#: the step that files the rows.
NOTHING_TO_WRITE = "set-nothing-to-write"
GENRE_WRITTEN = "set-genre-written"
ROWS_LEFT = "set-rows-left"
LEAVE_UNMATCHED = "set-leave-unmatched"
GENRE_ROW_TO_MAKE = "set-genre-row-to-make"
FILE_NEXT = "set-file-next"

#: The refusal over the files that did not take, after the rest landed.
UNWRITTEN = "tag-set-unwritten"

#: What the majority refusal says cannot be done until a prefix rule exists.
_BLOCKED = "no named row's file can be read to carry the genre"

_ORIGIN = ("tagging", "genre_set_cli")


def build(parser, entry) -> None:
    """Declare the verb: the genre, and the rows by identifier, file or playlist."""
    del entry
    parser.add_argument("genre", help="the genre to give the rows, as the taxonomy declares it")
    parser.add_argument(
        "--row",
        action="append",
        default=[],
        dest="rows",
        metavar="CONTENT_ID",
        help="give this row the genre; repeat it for each row",
    )
    parser.add_argument(
        "--rows-from",
        default=None,
        metavar="FILE",
        help="give the genre to every row whose content identifier is a line of "
        "this file; blank lines and anything after a # are skipped",
    )
    parser.add_argument(
        "--playlist",
        default=None,
        metavar="PATH",
        help="give the genre to every row of this playlist, named by its path "
        "from the top of the tree, each name joined by ' / ', as 'INBOX / Analyze'; "
        "a name holding ' / ' itself, as a genre folder's often does, is given as it is",
    )
    parser.add_argument(
        "--leave",
        action="append",
        default=[],
        metavar="CONTENT_ID",
        help="leave this row's genre as it is; repeat it for each row, and give "
        "the same rows again on the run that applies",
    )
    parser.set_defaults(_handler=tag_set)


def named_rows(args) -> tuple[list[str], str]:
    """The identifiers ``--row`` and ``--rows-from`` name, in order, and the
    playlist path, refused before anything is opened when nothing is named or
    the file cannot be read."""
    found = [str(one).strip() for one in getattr(args, "rows", None) or () if str(one).strip()]
    source = getattr(args, "rows_from", None)
    if source:
        try:
            # A BYTE ORDER MARK a text editor left is not part of the first id.
            text = Path(source).expanduser().read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as exc:
            raise refuse(
                "tag-set-scope-unknown",
                f"the rows file {source} could not be read ({exc.__class__.__name__}), "
                f"so no row was named from it and nothing was read",
                steps=("name a file holding one content identifier a line",),
                origin=_ORIGIN,
                detail={"rows_from": str(source)},
            ) from exc
        for line in text.splitlines():
            # WHAT FOLLOWS A # IS A COMMENT, on its own line or after an id.
            word = line.split("#", 1)[0].strip()
            if word:
                found.append(word)
    playlist = str(getattr(args, "playlist", None) or "").strip()
    if not found and not playlist:
        raise refuse(
            "tag-set-scope-unknown",
            "tag set needs the rows to give the genre: name them with --row, "
            "--rows-from or --playlist",
            steps=("name the rows with --row CONTENT_ID, --rows-from FILE or --playlist PATH",),
            origin=_ORIGIN,
        )
    return found, playlist


def _payload(plan: gs.SetPlan) -> dict[str, Any]:
    return plan_verbs.payload(
        plan,
        rows=len(plan.items),
        genre=plan.genre,
        genre_row=plan.shown_row,
        playlist=plan.playlist,
        outcomes=dict(plan.counts),
    )


def _facts(plan: gs.SetPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the genre, its row, the counts."""
    facts: dict[str, Any] = {
        "genre": plan.genre,
        "genre_row": plan.shown_row,
        "rows": len(plan.items),
        "outcomes": dict(plan.counts),
    }
    if plan.playlist:
        facts["playlist"] = plan.playlist
    if plan.leave_unmatched:
        facts["leave_unmatched"] = list(plan.leave_unmatched)
    return facts


def _title(item: gs.Item) -> str:
    return item.title or item.content_id


def _left(plan: gs.SetPlan) -> list[dict[str, str]]:
    """The warning, on every path, naming the rows left and why."""
    left = [item for item in plan.items if item.reason]
    if not left:
        return []
    return [warning(
        ROWS_LEFT,
        f"{len(left)} of {len(plan.items)} named row(s) were left as they are "
        f"({counted(plan.counts, gs.LEFT)}): "
        + named([f"{_title(item)} ({item.reason})" for item in left]),
    )]


def _to_make(plan: gs.SetPlan) -> list[dict[str, str]]:
    """The warning, on a path that wrote nothing, when the apply would make the
    genre's lookup row."""
    if not plan.mint:
        return []
    return [warning(
        GENRE_ROW_TO_MAKE,
        f"the library has no genre row for {plan.genre!r}, so the apply makes one, "
        f"on the commit that links the rows to it and only if a row is written; a "
        f"restore of its session takes the row back",
    )]


def _unmatched(plan: gs.SetPlan) -> list[dict[str, str]]:
    if not plan.leave_unmatched:
        return []
    return [warning(
        LEAVE_UNMATCHED,
        f"--leave named {', '.join(plan.leave_unmatched)}, and no named row has "
        f"that content identifier, so nothing was held for it",
    )]


def _advisories(plan: gs.SetPlan) -> list[dict[str, str]]:
    return [*_left(plan), *_unmatched(plan)]


def _nothing(plan: gs.SetPlan) -> dict[str, str]:
    return warning(
        NOTHING_TO_WRITE,
        f"no genre is to be written: {plan.counts[gs.ALREADY]} of {len(plan.items)} "
        f"named row(s) already carry {plan.genre!r} on the file and the row, and "
        f"the rest are left",
    )


def _written(plan: gs.SetPlan, written: gs.Written) -> list[dict[str, str]]:
    files = written.files
    made = (
        f", to the genre row {written.minted} this run made for it, the library "
        f"having none"
        if written.minted
        else ""
    )
    taken = ", takes the genre row away," if written.minted else ""
    said = [warning(
        GENRE_WRITTEN,
        f"{len(files.read_back)} file(s) carry the genre {plan.genre!r}, read back, "
        f"and {written.written} row(s) link it{made}, {written.read_back} read back "
        f"from the database as written, the genre and no other column; a restore "
        f"of session {written.session_id} puts the rows back{taken} and puts back "
        f"each file's old genre, which its record keeps",
    )]
    if written.written:
        leaving = sum(1 for item in plan.writes if item.leaves)
        moved = (
            f", then `crate adopt move`, which takes the {leaving} row(s) the tree "
            f"filed under their old genre out of that genre folder: its energy "
            f"band, `with vox`, genre sub and Favorites; a playlist you made "
            f"there, Candy among them, is never touched, and while one holds a "
            f"row that folder's Favorites keeps it too. A row the move files "
            f"itself gains its `with vox` at the next `crate adopt apply` and "
            f"its Favorites at the next `crate favorites refresh`"
            if leaving
            else ""
        )
        said.append(warning(
            FILE_NEXT,
            f"to file the rows under {plan.genre!r}, run `crate adopt apply`, which "
            f"files by its energy band each one the tree does not hold in that "
            f"genre's folder yet{moved}",
        ))
    return said


def _unwritten(plan: gs.SetPlan, written: gs.Written) -> str:
    """The files that did not take, by title, as one clause, or empty."""
    files = written.files
    titles = {item.content_id: _title(item) for item in plan.items}
    parts = []
    for ids, said in (
        (files.moved, "no longer carry the genre the plan read"),
        (files.failed, "could not be written"),
        (files.wrong, "do not read back as written"),
    ):
        if ids:
            parts.append(f"{len(ids)} {said}: " + named([titles.get(one, one) for one in ids]))
    if not parts:
        return ""
    return (
        "these keep their old genre on the row, because their file did not take "
        "the new one: " + "; ".join(parts)
    )


def _unwritten_refusal(plan: gs.SetPlan, written: gs.Written):
    """Refuse over the files that did not take, after the rest landed."""
    files = written.files
    return refuse(
        UNWRITTEN,
        f"{len(files.read_back)} file(s) and {written.written} row(s) took the genre "
        f"{plan.genre!r}, session {written.session_id}; " + _unwritten(plan, written),
        steps=(
            "check each named file can be written and is not open elsewhere",
            "run the verb again, which plans what is left",
        ),
        origin=_ORIGIN,
        detail={
            "moved": list(files.moved),
            "failed": list(files.failed),
            "wrong": list(files.wrong),
            "session": written.session_id,
        },
    )


def plan_on(
    cfg: config.Config, db, declared, genre: str, args, held: placements.Placements
) -> gs.SetPlan:
    """The plan the arguments name, off ``db``, with the tree as ``held`` reads it."""
    found, playlist = named_rows(args)
    return gs.plan_set(
        cfg,
        db,
        declared,
        genre,
        gs.scoped(db, found, playlist),
        playlist=playlist,
        leave=list(getattr(args, "leave", None) or ()),
        held=held,
    )


def read_plan(cfg: config.Config, declared, genre: str, args) -> gs.SetPlan:
    """The plan over the library as it stands, through a handle opened to read and
    closed before this returns. A library mostly under no prefix rule refuses first."""
    held = placements.read_placements(cfg, declared)
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        return plan_on(cfg, db, declared, genre, args, held)


def apply_plan(cfg: config.Config, approved: gs.SetPlan, declared, args) -> gs.Written:
    """Open the database to write, take the plan again on that handle, refuse if it
    moved, then write the files and the rows and read them back."""
    # THE TREE IS READ BEFORE THE WRITE HANDLE OPENS, through its own read handle.
    held = placements.read_placements(cfg, declared)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        again = plan_on(cfg, db, declared, approved.genre, args, held)
        gs.assert_plan_unchanged(approved, again)
        written = gs.apply_set(
            cfg, db, again, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)
    # THE READ BACK OUTRANKS THE FILES: a row wrong in the database is the worse news.
    gs.assert_read_back(written)
    return written


def tag_set(ctx) -> Envelope:
    """Plan every named row against the genre, ask, then write and read back."""
    cfg = load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # REFUSED BEFORE ANY READ: the genre and the scope's shape.
    genre = gs.assert_declared(declared, ctx.args.genre)
    named_rows(ctx.args)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = read_plan(cfg, declared, genre, ctx.args)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(
            data=data, outcome=Outcome.NO_OP, warnings=[*_to_make(plan), *_advisories(plan)]
        )
    if not plan.writes:
        return ctx.envelope(
            data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan), *_advisories(plan)]
        )
    written = apply_plan(cfg, plan, declared, ctx.args)
    data["totals"] = {**data["totals"], "written": written.written, "read_back": written.read_back}
    answered = ctx.envelope(data=data, warnings=[*_written(plan, written), *_advisories(plan)])
    if written.files.clean:
        return answered
    # A PARTIAL APPLY REFUSES, THROUGH ``from_cause``, its counts and every
    # advisory kept, as ``analyze adopt``'s does.
    refused = output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_unwritten_refusal(plan, written).cause,
        schema=ctx.entry.output_schema,
        data=answered.data,
    )
    return replace(refused, warnings=answered.warnings)


__all__ = [
    "CONFIRM_GATE", "FILE_NEXT", "GENRE_ROW_TO_MAKE", "GENRE_WRITTEN", "LEAVE_UNMATCHED", "NOTHING_TO_WRITE",
    "ROWS_LEFT", "UNWRITTEN", "apply_plan", "build", "named_rows", "read_plan", "tag_set",
]
