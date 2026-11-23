"""``crate analyze adopt``: after the visit, a title whose key or tempo differs takes rekordbox's (U327).

The engine is :mod:`cratekit.analysis.head_adopt`. THE ORDER IS ``tag rows``'S:
the backup acknowledgment first; the plan on a read handle closed before the
gate; the explicit gate over the digest, taking no inline answer, AN EMPTY PLAN
STILL ASKS; only ``apply`` over a plan that writes opens the database to write,
takes the plan again on that handle and refuses ``decision-stale`` if it moved.
``--leave`` holds a row out, in the plan and its digest. Every path says how
many rows were left and why.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from typing import Any

from cratekit.analysis import head_adopt as ha
from cratekit.analysis.check_cli import template_of
from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome
from cratekit.core.naming import NameTemplate
from cratekit.tagging import plan_verbs
from cratekit.tagging.plan_verbs import counted, named, warning

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "analyze.adopt.confirm"

#: The warnings: nothing to write, what was written and read back, rows left,
#: answers only half read, and a ``--leave`` naming no row this plan writes.
NOTHING_TO_WRITE = "adopt-nothing-to-write"
HEADS_WRITTEN = "adopt-heads-written"
ROWS_LEFT = "adopt-rows-left"
HALF_READ = "adopt-answer-half-read"
LEAVE_UNMATCHED = "adopt-leave-unmatched"
FILES_UNWRITTEN = "adopt-files-unwritten"

#: What the majority refusal says cannot be done until a prefix rule exists.
_BLOCKED = "no landed row's file can be read to carry rekordbox's key and tempo"

_ORIGIN = ("analysis", "head_adopt_cli")


def build(parser, entry) -> None:
    """Declare the verb: a pass or a landing's session may name the rows, never both."""
    del entry
    named_scope = parser.add_mutually_exclusive_group()
    named_scope.add_argument(
        "--pass",
        dest="pass_name",
        default=None,
        help="adopt rekordbox's key and tempo on the rows the closed landings of this pass filed",
    )
    named_scope.add_argument(
        "--session",
        dest="session_id",
        default=None,
        help="adopt rekordbox's key and tempo on the rows one closed landing filed",
    )
    parser.add_argument(
        "--leave",
        action="append",
        default=[],
        metavar="CONTENT_ID",
        help=(
            "leave this row's title, title tag and key tag as they are whatever "
            "rekordbox found; repeat it for each row, and give the same rows again "
            "on the run that applies"
        ),
    )
    parser.set_defaults(_handler=analyze_adopt)


def _payload(plan: ha.AdoptPlan) -> dict[str, Any]:
    return plan_verbs.payload(
        plan,
        rows=plan.rows,
        scope=plan.scope.kind,
        scope_name=plan.scope.name,
        outcomes=dict(plan.counts),
        notes=dict(plan.notes),
        key_agreement=plan.relations(),
    )


def _facts(plan: ha.AdoptPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the scope, the counts, the relations."""
    facts: dict[str, Any] = {
        "scope": plan.scope.name,
        "rows": plan.rows,
        "outcomes": dict(plan.counts),
        "notes": dict(plan.notes),
        "key_agreement": plan.relations(),
    }
    if plan.leave_unmatched:
        facts["leave_unmatched"] = list(plan.leave_unmatched)
    return facts


def _title(item: ha.Item) -> str:
    return item.title or item.content_id


def _left(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    """The warning, on every path, naming the rows left alone and why."""
    left = [item for item in plan.items if item.reason]
    if not left:
        return []
    return [warning(
        ROWS_LEFT,
        f"{len(left)} of {plan.rows} row(s) were left alone "
        f"({counted(plan.counts, ha.LEFT)}): "
        + named([f"{_title(item)} ({item.reason})" for item in left]),
    )]


def _half(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    """The warning naming rows whose key or tempo rekordbox did not give."""
    noted = [item for item in plan.items if item.notes and not item.reason]
    if not noted:
        return []
    return [warning(
        HALF_READ,
        f"{len(noted)} row(s) took only half of rekordbox's answer "
        f"({counted(plan.notes, ha.NOTES)}), the other half left as the head has it: "
        + named([f"{_title(item)} ({', '.join(item.notes)})" for item in noted]),
    )]


def _unmatched(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    if not plan.leave_unmatched:
        return []
    return [warning(
        LEAVE_UNMATCHED,
        f"--leave named {', '.join(plan.leave_unmatched)}, and no row this plan "
        f"writes has that content identifier, so nothing was held for it",
    )]


def _advisories(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    return [*_left(plan), *_half(plan), *_unmatched(plan)]


def _nothing(plan: ha.AdoptPlan) -> dict[str, str]:
    return warning(
        NOTHING_TO_WRITE,
        f"no title is to be written: {plan.counts[ha.AGREE]} of {plan.rows} row(s) of "
        f"{plan.scope.name} already carry rekordbox's key and tempo",
    )


def _written(plan: ha.AdoptPlan, written: ha.Written) -> dict[str, str]:
    files = written.files
    return warning(
        HEADS_WRITTEN,
        f"{len(files.read_back)} file(s) carry rekordbox's key and tempo in their title "
        f"tag and key tag, read back, and {written.written} row(s) in their title, "
        f"{written.read_back} read back from the database as written, the title and no "
        f"other column; the file names keep their old head; undo the rows with a restore "
        f"of session {written.session_id}, whose record keeps each file's old title and "
        f"key tag",
    )


def _unwritten(written: ha.Written) -> list[dict[str, str]]:
    """The warning naming the files that did not take, whose rows were left."""
    files = written.files
    if not files.failed and not files.wrong:
        return []
    parts = []
    if files.failed:
        parts.append(f"{len(files.failed)} could not be written: {named(list(files.failed))}")
    if files.wrong:
        parts.append(f"{len(files.wrong)} do not read back: {named(list(files.wrong))}")
    return [warning(
        FILES_UNWRITTEN,
        "these row(s) keep their old title, because their file did not take the new "
        "one: " + "; ".join(parts) + "; run the verb again once the file can be written",
    )]


def scope_and_plan(
    cfg: config.Config, db, args, *, declared, template: NameTemplate
) -> ha.AdoptPlan:
    """The scope the arguments name and the plan over it, off ``db``."""
    scope = ha.resolve_scope(
        cfg,
        db,
        declared=declared,
        registry=tree_registry.read(cfg),
        pass_name=getattr(args, "pass_name", None),
        session_id=getattr(args, "session_id", None),
    )
    leave = list(getattr(args, "leave", None) or ())
    return ha.plan_adopt(cfg, db, scope, template=template, leave=leave)


def read_plan(cfg: config.Config, args, *, declared, template: NameTemplate) -> ha.AdoptPlan:
    """The plan over the library as it stands, through a handle opened to read and
    closed before this returns. A library mostly under no prefix rule refuses first."""
    with plan_verbs.reading(cfg, _BLOCKED) as db:
        return scope_and_plan(cfg, db, args, declared=declared, template=template)


def apply_plan(
    cfg: config.Config, approved: ha.AdoptPlan, args, *, declared, template: NameTemplate
) -> ha.Written:
    """Open the database to write, take the plan again on that handle, refuse if it
    moved, then write the files and the rows and read them back."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        again = scope_and_plan(cfg, db, args, declared=declared, template=template)
        ha.assert_plan_unchanged(approved, again)
        written = ha.apply_adopt(cfg, db, again, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)
    ha.assert_read_back(written)
    return written


def analyze_adopt(ctx) -> Envelope:
    """Plan every landed row against rekordbox's answer, ask, then write and read back."""
    cfg = load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    template = template_of(cfg)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = read_plan(cfg, ctx.args, declared=declared, template=template)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
    held: dict[str, ha.Written] = {}

    def apply() -> ha.Written:
        held["written"] = apply_plan(cfg, plan, ctx.args, declared=declared, template=template)
        return held["written"]

    return plan_verbs.applied(
        ctx,
        plan,
        data,
        lambda one: [*_unwritten(held["written"]), *_advisories(one)]
        if "written" in held
        else _advisories(one),
        nothing=_nothing,
        apply=apply,
        said=lambda written: _written(plan, written),
    )


__all__ = [
    "CONFIRM_GATE", "FILES_UNWRITTEN", "HALF_READ", "HEADS_WRITTEN", "LEAVE_UNMATCHED",
    "NOTHING_TO_WRITE", "ROWS_LEFT", "analyze_adopt", "apply_plan", "build", "read_plan",
    "scope_and_plan",
]
