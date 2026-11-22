"""``crate tag rows``: write a row's genre from its file where the two disagree.

A VERB OF ITS OWN (R-816), not a mode of ``tag retag``: that verb owns the file
and asks a catalogue, this one owns the row, asks nobody and reads the whole
collection, and a database gate asked in one mode only is one the registry
cannot state.

THE ORDER IS ``adopt move``'S: the backup acknowledgment before the plan and
the gate (R-733); the plan on a read handle closed before the gate, refusing a
library it cannot read first (R-372); the gate over the digested plan, AND AN
EMPTY PLAN STILL ASKS, since every declared gate has to fire; and only
``apply`` over a plan that writes opens the database to write, so that is where
a running rekordbox refuses, and each row is checked to be as the plan read it.

``--leave`` HOLDS A ROW OUT, for a genre set by hand in rekordbox. Held rows are
in the plan and its digest, so the applying run names the same rows or refuses
as stale. The second invocation rebuilds the plan, so a file that changed in
between refuses ``decision-stale`` with nothing written. The gate takes no
inline answer (R34).

WHAT A PERSON READS. The default renderer prints nothing of a plan's totals, so
the gate carries the counts and common word pairs as facts, and every path says
how many differing rows were left and why, naming the act for a word with no
lookup row.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.tagging import plan_verbs, rows
from cratekit.tagging.plan_verbs import counted

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "tag.rows.confirm"

#: Rows were left alone because their file's genre could not be learned.
FILES_NOT_READ = "rows-file-not-read"

#: The plan writes nothing.
NOTHING_TO_WRITE = "rows-nothing-to-write"

#: What the apply wrote and read back.
GENRES_WRITTEN = "rows-genre-written"

#: Rows that differ from a file that was read, and were left alone.
ROWS_LEFT = "rows-left-alone"

#: An identifier given to ``--leave`` names no row that differs from its file.
LEAVE_UNMATCHED = "rows-leave-unmatched"

#: What the majority refusal says cannot be done until a prefix rule exists.
_BLOCKED = "no row's genre can be compared with its file"

_ORIGIN = ("tagging", "rows_cli")


def build(parser, entry) -> None:
    """Declare the verb. It reads the whole collection, less the rows held out."""
    del entry
    parser.add_argument(
        "--leave",
        action="append",
        default=[],
        metavar="CONTENT_ID",
        help=(
            "leave this row's genre as it is whatever its file says, for a "
            "genre set by hand in rekordbox; repeat it for each row, and give "
            "the same rows again on the run that applies"
        ),
    )
    parser.set_defaults(_handler=tag_rows)


def _payload(plan: rows.RowsPlan) -> dict[str, Any]:
    return plan_verbs.payload(
        plan, rows=plan.rows, outcomes=dict(plan.counts), pairs=plan.pairs()
    )


def _facts(plan: rows.RowsPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and the pairs."""
    facts: dict[str, Any] = {
        "rows": plan.rows,
        "outcomes": dict(plan.counts),
        "pairs": plan.pairs(),
    }
    if plan.leave_unmatched:
        facts["leave_unmatched"] = list(plan.leave_unmatched)
    return facts


def _word(value: str) -> str:
    return repr(value) if value else "a blank genre"


def _not_read(plan: rows.RowsPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file's genre could not be learned."""
    if not plan.unread:
        return []
    return [
        {
            "code": FILES_NOT_READ,
            "message": (
                f"{plan.unread} of {plan.rows} row(s) were left alone because "
                f"their file's genre could not be read ({counted(plan.counts, rows.UNREAD)}); "
                f"a volume that is not mounted reads as {rows.FILE_MISSING}, and "
                f"nothing here says those rows agree with their files"
            ),
        }
    ]


def _left(plan: rows.RowsPlan) -> list[dict[str, str]]:
    """The warning a run carries when a differing row was left, with the act.

    ON EVERY PATH THAT ANSWERS, the run that wrote included, or a person is told
    the rows were written and not that some still disagree. A word with no
    lookup row names its act: this verb never makes a genre row, and rekordbox
    makes one when a track is given that genre there.
    """
    count = sum(plan.counts[name] for name in rows.LEFT)
    if not count:
        return []
    message = (
        f"{count} row(s) differ from their file and were left alone "
        f"({counted(plan.counts, rows.LEFT)}), each listed with its reason"
    )
    unknown = plan.unknown_words()
    if unknown:
        named = ", ".join(f"{word!r} on {held}" for word, held in unknown)
        message += (
            f"; the library has no genre row for {named}, and this verb links a "
            f"genre row and never makes one: give one track that genre in "
            f"rekordbox, which makes the row, then run this again"
        )
    return [{"code": ROWS_LEFT, "message": message}]


def _unmatched(plan: rows.RowsPlan) -> list[dict[str, str]]:
    """The warning a run carries when ``--leave`` named a row that does not differ."""
    if not plan.leave_unmatched:
        return []
    return [
        {
            "code": LEAVE_UNMATCHED,
            "message": (
                f"--leave named {', '.join(plan.leave_unmatched)}, and no row "
                f"with that content identifier differs from its file, so nothing "
                f"was held for it; a mistyped identifier is a row this plan writes"
            ),
        }
    ]


def _advisories(plan: rows.RowsPlan) -> list[dict[str, str]]:
    return [*_left(plan), *_unmatched(plan), *_not_read(plan)]


def _nothing(plan: rows.RowsPlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"no row's genre is to be written: {plan.counts[rows.AGREE]} of "
            f"{plan.rows} row(s) agree with their file"
        ),
    }


def _written(plan: rows.RowsPlan, written: rows.Written) -> dict[str, str]:
    pairs = "; ".join(
        f"{_word(pair['row'])} to {_word(pair['file'])}, {pair['rows']}" for pair in plan.pairs()
    )
    return {
        "code": GENRES_WRITTEN,
        "message": (
            f"{written.written} row(s) now carry their file's genre and "
            f"{written.read_back} read back from the database as written, the "
            f"genre and no other column; the most common: {pairs}; undo with a "
            f"restore of session {written.session_id}"
        ),
    }


def read_plan(cfg: config.Config, declared, leave: list[str]) -> rows.RowsPlan:
    """The plan over the library as it stands, through a handle opened to read."""
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        return rows.plan_rows(cfg, db, declared, leave=leave)


def apply_plan(cfg: config.Config, plan: rows.RowsPlan) -> rows.Written:
    """Apply the plan on a handle opened to write, refusing over what does not
    read back. The one apply path, the verb's and ``tag campaign``'s (U294)."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        written = rows.apply_rows(cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)
    rows.assert_read_back(written)
    return written


def tag_rows(ctx) -> Envelope:
    """Plan every row against its file, ask, then write the genre and read it back."""
    cfg = load_config(("tagging.rows_cli",))
    declared = active_taxonomy.load(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = read_plan(cfg, declared, list(getattr(ctx.args, "leave", None) or ()))
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
        said=lambda written: _written(plan, written),
    )


__all__ = [
    "CONFIRM_GATE",
    "FILES_NOT_READ",
    "GENRES_WRITTEN",
    "LEAVE_UNMATCHED",
    "NOTHING_TO_WRITE",
    "ROWS_LEFT",
    "apply_plan",
    "build",
    "read_plan",
    "tag_rows",
]
