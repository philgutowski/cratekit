"""``crate tag rows``: write a row's genre from its file where the two disagree.

WHY THIS IS A VERB OF ITS OWN (R-816) and not a mode of ``tag retag``. That verb
owns the FILE and asks a catalogue what the genre should be. This one owns the
ROW, asks nobody, and reads the whole collection. A gate is declared per verb
and every declared gate has to fire, so a database gate asked in one mode only
is a gate the registry cannot state, which is the reason ``adopt move`` gives
for itself.

THE ORDER IS ``adopt move``'S, and the plan is made on a read handle:

* the backup acknowledgment is read before the plan is built and before the
  gate (R-733), so a person with none is refused before a walk of the whole
  collection and before they read a plan;
* the plan is made on a handle opened to read and closed before the gate, and
  what it returns is values;
* the gate is asked over the digested plan, AND AN EMPTY PLAN STILL ASKS, for
  the reason ``tag retag`` gives: every declared gate has to fire, and a gate
  the verb sometimes skips is a decision the product promises and does not
  always ask. A plan that writes nothing is then a no op;
* only ``apply`` over a plan that writes opens the database with write intent,
  so that is where a running rekordbox or its agent refuses, and the engine
  checks each row is still as the plan read it before the session is entered.

A LIBRARY IT CANNOT READ REFUSES BEFORE THE GATE (R-372). When most rows record
a path under no prefix rule the plan is empty for a reason a prefix rule fixes,
and the verb says so under the slug its sibling and doctor use.

``--leave`` HOLDS A ROW OUT. Every disagreement is read as the row lagging its
file, which is false of a genre set by hand in rekordbox, and the gate is apply
or abort over the whole plan. The held rows are part of the plan and of its
digest, so the run that applies names the same rows or refuses as stale.

THE SECOND INVOCATION REBUILDS THE PLAN from the database and the files, and
the gate compares its digest with the one the answer was recorded against. A
file whose genre changed between the plan and the apply moves the digest, and
the run refuses ``decision-stale`` with nothing written.

THE GATE TAKES NO INLINE ANSWER. It is answered by a separate recorded act with
an actor, the way every write to a live library's rows is (R34).

WHAT A PERSON READS. The default renderer prints nothing from a plan payload's
totals, so the gate screen carries the outcome counts and the most common word
pairs as facts in front of the items, and a run that wrote, or that found
nothing to write, carries one line saying what it counted. A run that left a
differing row alone says how many and why on every path, and names the act for
a word the library has no lookup row for.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import rows
from cratekit.write import metadata_cli

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
                origin=("tagging.rows_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


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


def _confirm_gate(entry):
    """The verb's own gate by name, never by position.

    The shared cloud sync gate sits beside it and is raised by the guarded
    writer, so indexing would bind this verb to the order the two are written
    in.
    """
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


def _payload(plan: rows.RowsPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {
            "count": len(plan.items),
            "rows": plan.rows,
            "outcomes": dict(plan.counts),
            "pairs": plan.pairs(),
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


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


def _counted(plan: rows.RowsPlan, names: tuple[str, ...]) -> str:
    return ", ".join(f"{plan.counts[name]} {name}" for name in names if plan.counts[name])


def _not_read(plan: rows.RowsPlan) -> list[dict[str, str]]:
    """The warning a run carries when a file's genre could not be learned."""
    if not plan.unread:
        return []
    return [
        {
            "code": FILES_NOT_READ,
            "message": (
                f"{plan.unread} of {plan.rows} row(s) were left alone because "
                f"their file's genre could not be read ({_counted(plan, rows.UNREAD)}); "
                f"a volume that is not mounted reads as {rows.FILE_MISSING}, and "
                f"nothing here says those rows agree with their files"
            ),
        }
    ]


def _left(plan: rows.RowsPlan) -> list[dict[str, str]]:
    """The warning a run carries when a differing row was left, with the act.

    ON EVERY PATH THAT ANSWERS, the run that wrote included. A person sent here
    to make the rows catch up is otherwise told the rows were written and not
    told that some still disagree. A WORD WITH NO LOOKUP ROW NAMES ITS ACT:
    this verb links a genre row and never makes one, and rekordbox makes one
    when a track is given that genre there.
    """
    count = sum(plan.counts[name] for name in rows.LEFT)
    if not count:
        return []
    message = (
        f"{count} row(s) differ from their file and were left alone "
        f"({_counted(plan, rows.LEFT)}), each listed with its reason"
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


def _refuse_a_library_it_cannot_read(cfg: config.Config, plan: rows.RowsPlan) -> None:
    """Refuse when most rows record a path under no prefix rule (R-372).

    THE SLUG, THE STEPS AND THE DETAIL ARE THE SIBLING VERB'S,
    :func:`cratekit.write.metadata_cli.majority_unmapped_cause`, so plan, apply
    and doctor's ``library.paths_resolved`` keep saying one thing. Without it a
    drive renamed with no rule plans nothing over thousands of rows, asks its
    gate over that, and ends as a no op a person had to approve to read.
    """
    if not plan.majority_unmapped:
        return
    totals = metadata_cli.ResolutionTotals(
        active=plan.rows,
        unresolved=plan.unread,
        unmapped=plan.counts[rows.PATH_UNMAPPED],
        prefixes=dict(plan.unmapped_prefixes),
    )
    raise CratekitError(metadata_cli.majority_unmapped_cause(cfg, totals, blocked=_BLOCKED))


def _plan(cfg: config.Config, declared, leave: list[str]) -> rows.RowsPlan:
    """The plan over the library as it stands, through a handle opened to read.

    ``require_closed`` is the opener's write intent flag and it is left False,
    as the collection reader leaves it, so the plan can be read with rekordbox
    open. The handle is closed before this returns.
    """
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return rows.plan_rows(cfg, db, declared, leave=leave)
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: rows.RowsPlan) -> rows.Written:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return rows.apply_rows(cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)


def tag_rows(ctx) -> Envelope:
    """Plan every row against its file, ask, then write the genre and read it back."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = _confirm_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, declared, list(getattr(ctx.args, "leave", None) or ()))
    _refuse_a_library_it_cannot_read(cfg, plan)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
    if not plan.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[_nothing(plan), *_advisories(plan)],
        )

    written = _write(cfg, plan)
    rows.assert_read_back(written)
    data["totals"] = {
        **data["totals"],
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(plan, written), *_advisories(plan)])


__all__ = [
    "CONFIRM_GATE",
    "FILES_NOT_READ",
    "GENRES_WRITTEN",
    "LEAVE_UNMATCHED",
    "NOTHING_TO_WRITE",
    "ROWS_LEFT",
    "build",
    "tag_rows",
]
