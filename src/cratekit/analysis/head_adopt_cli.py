"""``crate analyze adopt``: after the visit, a title whose key or tempo differs takes rekordbox's (U327).

A title with no head is given one built from rekordbox's key and tempo, planned
``stamped`` apart from the corrected rows, at the same gate (U342).

The engine is :mod:`cratekit.analysis.head_adopt`. THE ORDER IS ``tag rows``'S:
the backup acknowledgment first; the plan on a read handle closed before the
gate; the explicit gate over the digest, taking no inline answer, AN EMPTY PLAN
STILL ASKS; only ``apply`` over a plan that writes opens the database to write,
takes the plan again on that handle and refuses ``decision-stale`` if it moved.
``--leave`` holds a row out, in the plan and its digest. Every path says how
many rows were left and why, a partial apply's refusal included. An intake
tree that cannot be read refuses before the gate with its own reason.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from cratekit.analysis import head_adopt as ha
from cratekit.cli import output
from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome, refuse
from cratekit.core.naming import NameTemplate
from cratekit.intake.check_cli import template_of
from cratekit.tagging import plan_verbs
from cratekit.tagging.plan_verbs import counted, named, warning

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "analyze.adopt.confirm"

#: The warnings: nothing to write, what was written and read back, rows left,
#: answers only half read, a ``--leave`` naming no row this plan writes, an
#: INBOX / Analyze absent or empty, and session records the log could not read,
#: said on every path (review rounds one and two).
NOTHING_TO_WRITE = "adopt-nothing-to-write"
HEADS_WRITTEN = "adopt-heads-written"
ROWS_LEFT = "adopt-rows-left"
HALF_READ = "adopt-answer-half-read"
LEAVE_UNMATCHED = "adopt-leave-unmatched"
SCOPE_EMPTY = "adopt-scope-empty"
RECORDS_UNREAD = "adopt-records-unread"

#: The refusal over the files that did not take, after the rest landed.
UNWRITTEN = "analyze-adopt-unwritten"

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
    # WHAT THE SCOPE COULD NOT READ is shown at the gate too, so an empty plan is
    # never approved as a clean one (review round one).
    unread = [entry["message"] for entry in _unread(plan)]
    if unread:
        facts["unread"] = unread
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
        + named([f"{_title(item)} ({_why_left(item)})" for item in left]),
    )]


def _why_left(item: ha.Item) -> str:
    """A row's reason, and for a title with no head, which half rekordbox did not give."""
    if item.reason == ha.NO_HEAD_UNANSWERED and item.notes:
        return f"{item.reason}: {', '.join(item.notes)}"
    return item.reason


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


def _unread(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    """Why the scope holds nothing, and what it could not read, so an empty plan
    says what it stands on."""
    said = []
    passed = "; ".join(why for why in plan.scope.passed_over if why)
    if passed:
        said.append(warning(
            SCOPE_EMPTY,
            f"{passed}, so no row was planned; a landing already cleared from it is "
            f"named with --pass or --session",
        ))
    if plan.scope.unreadable_records:
        said.append(warning(
            RECORDS_UNREAD,
            f"{plan.scope.unreadable_records} session record(s) could not be read, so a "
            f"landing of {plan.scope.name} among them is not in this plan",
        ))
    return said


def _advisories(plan: ha.AdoptPlan) -> list[dict[str, str]]:
    return [*_unread(plan), *_left(plan), *_half(plan), *_unmatched(plan)]


def _nothing(plan: ha.AdoptPlan) -> dict[str, str]:
    if not plan.rows:
        return warning(
            NOTHING_TO_WRITE,
            f"no title is to be written: {plan.scope.name} holds no row in scope",
        )
    return warning(
        NOTHING_TO_WRITE,
        f"no title is to be written: {plan.counts[ha.AGREE]} of {plan.rows} row(s) of "
        f"{plan.scope.name} already carry rekordbox's key and tempo",
    )


def _written(plan: ha.AdoptPlan, written: ha.Written) -> dict[str, str]:
    files = written.files
    landed = frozenset(files.read_back)
    stamped = sum(1 for item in plan.writes if item.action == ha.STAMPED and item.content_id in landed)
    return warning(
        HEADS_WRITTEN,
        f"{len(files.read_back)} file(s) carry rekordbox's key and tempo in their title "
        f"tag and key tag, read back, {stamped} of them a title that had no head, and "
        f"{written.written} row(s) in their title, "
        f"{written.read_back} read back from the database as written, the title and no "
        f"other column; no file is renamed; a restore of session "
        f"{written.session_id} puts the rows back and each file's old title tag and "
        f"key tag, which its record keeps",
    )


def _unwritten(plan: ha.AdoptPlan, written: ha.Written) -> str:
    """The files that did not take, by title, as one clause, or empty."""
    files = written.files
    titles = {item.content_id: _title(item) for item in plan.items}
    parts = []
    if files.failed:
        parts.append(
            f"{len(files.failed)} could not be written: "
            + named([titles.get(one, one) for one in files.failed])
        )
    if files.wrong:
        parts.append(
            f"{len(files.wrong)} do not read back as written: "
            + named([titles.get(one, one) for one in files.wrong])
        )
    if not parts:
        return ""
    return (
        "these keep their old title in rekordbox, because their file did not take the "
        "new one: " + "; ".join(parts)
    )


def _unwritten_refusal(plan: ha.AdoptPlan, written: ha.Written):
    """Refuse over the files that did not take, after the rest landed."""
    files = written.files
    return refuse(
        UNWRITTEN,
        f"{len(files.read_back)} file(s) and {written.written} row(s) took rekordbox's key "
        f"and tempo, session {written.session_id}; " + _unwritten(plan, written),
        steps=(
            "check each named file can be written and is not open elsewhere",
            "run the verb again, which plans what is left",
        ),
        origin=_ORIGIN,
        detail={
            "failed": list(files.failed),
            "wrong": list(files.wrong),
            "session": written.session_id,
        },
    )


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
    # THE READ BACK OUTRANKS THE FILES: a row wrong in the database is the worse
    # news. Files that did not take are the caller's to refuse, with its advisories.
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

    answered = plan_verbs.applied(
        ctx,
        plan,
        data,
        _advisories,
        nothing=_nothing,
        apply=apply,
        said=lambda written: _written(plan, written),
    )
    written = held.get("written")
    if written is None or not (written.files.failed or written.files.wrong):
        return answered
    # A PARTIAL APPLY REFUSES, THROUGH ``from_cause``, the one boundary where a
    # cause becomes a status, its counts and every advisory kept: a row left
    # because its file could not be read is named here as on every path.
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
    "CONFIRM_GATE", "HALF_READ", "HEADS_WRITTEN", "LEAVE_UNMATCHED", "NOTHING_TO_WRITE",
    "RECORDS_UNREAD", "ROWS_LEFT", "SCOPE_EMPTY", "UNWRITTEN", "analyze_adopt", "apply_plan",
    "build", "read_plan", "scope_and_plan",
]
