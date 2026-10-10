"""Write a chosen ``ContentLink`` onto one live content row, through the guard,
to learn whether that column is what keeps a binding made row off a deck (A32).

WHY THIS EXISTS. A row the native landing makes shows every column in
rekordbox, analyses on request, and will not load to a deck, while a row
rekordbox imports from the same file loads at once (R-928). The defaults were
filled (R-923) and the file id was given its inode (U115), and at sitting 36
of ``docs/cutover.md`` the repaired rows still would not load. Beyond the row's
own identity and two update counters, one ``djmdContent`` column still differs:
:data:`cratekit.core.rb_writer.CONTENT_LINK_COLUMN`, one value on every binding
row and another on nearly every row rekordbox made. This is the experiment
that tests it: one row, one value, one gated commit, then rekordbox opened and
the row's context menu read.

WHAT IT WRITES IS ONE COLUMN ON ONE ROW AND NOTHING ELSE, through
:func:`cratekit.core.rb_writer.write_metadata_field` under
:data:`cratekit.core.rb_writer.CONTENT_LINK_POLICY`, registered by the apply
for its commit and put back after it, so the guard's writable columns widen for
this commit and no other.

A LIVE ROW ONLY, AND A VALUE OTHER ROWS CARRY. The plan reads the row from SQL
with ``rb_local_deleted = 0`` and refuses a tombstone or an unknown id by name.
It counts the live rows carrying the value asked for and refuses when none
does: the probe copies a value rekordbox wrote onto a row it did not, and a
value nothing carries is a typo and not an experiment. A row already at the
value plans nothing, as ``repair rows`` does over a whole library: the gate
still asks and the apply is a no op.

THE ROW IS READ AGAIN FROM SQL AFTER THE COMMIT. The column must read as the
value, and no column outside it and the binding's bookkeeping may have moved.

THE DIGEST NAMES NO COPY. The row's id, the value and the value it replaces,
so a rehearsal on a disposable copy of the database digests equal to the live
plan when the row is the same, which is what lets a session approve the live
write on its own.

Layer: write. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import row_defaults, trees

#: The name a session record carries for this write.
WORKFLOW = "repair-link"

#: What the write is filed under in a session record's change summary. A stable
#: identifier and never a display name.
CHANGE_KEY = "content.link"

#: The column the probe writes, the writer's name for it.
LINK = rb_writer.CONTENT_LINK_COLUMN

#: No live row carries the identifier asked for.
ROW_UNKNOWN = "link-row-unknown"

#: No other live row carries the value asked for.
VALUE_UNHELD = "link-value-unheld"

_ORIGIN = ("write", "row_link")


@dataclass(frozen=True, slots=True)
class LinkPlan:
    """One live row, the value it carries, the value it will carry, and who else carries it."""

    content_id: str
    title: str
    path: str
    #: The value to write, as the live table stores it.
    value: int
    #: The value the row carries now, as text, so the apply can see it moved.
    was: str
    #: Live rows other than this one carrying ``value``.
    carriers: int
    #: Live rows other than this one carrying ``was``, the binding's value.
    fellows: int
    #: Live rows read.
    rows: int

    @property
    def writes(self) -> bool:
        """Whether the row carries another value than the one asked for."""
        return self.was != str(self.value)

    def to_json(self) -> dict[str, Any]:
        """The one item as the gate shows it and the digest covers it."""
        return {
            "content_id": self.content_id,
            "title": self.title,
            "path": self.path,
            "column": LINK,
            "from": self.was,
            "to": self.value,
        }

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to.

        OVER THE ROW, THE COLUMN, THE VALUE WRITTEN AND THE VALUE REPLACED, and
        nothing that names a copy, so a rehearsal on a disposable copy digests
        equal to the live plan when the row is the same. The counts are not in
        it: they are what the gate shows and not what the approval is for.
        """
        return digest_of({"kind": WORKFLOW, "items": [self.to_json()]})


@dataclass(frozen=True, slots=True)
class Written:
    """What one apply did, and what the database says about it afterwards.

    ``wrong`` says the column does not read back as the value. ``moved`` names
    each other column changed beyond the binding's bookkeeping. Both are empty
    on a good run and :func:`assert_read_back` refuses when either is not.
    """

    session_id: str
    written: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def _count(db: Any, value: Any, *, excluding: str) -> int:
    """How many live rows other than ``excluding`` carry ``value`` in the column."""
    from sqlalchemy import text

    found = db.session.execute(
        text(
            f"SELECT COUNT(*) FROM {rb_writer.CONTENT_TABLE} WHERE {LINK} = :value "
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
        ),
        {"value": value, "id": excluding},
    )
    return int(found.scalar() or 0)


def plan_link(db: Any, *, content_id: str, value: int) -> LinkPlan:
    """The one live row named, what it carries, and how many rows carry the value.

    FROM SQL AND NOT FROM THE MAPPED ROW, so the value read is what the table
    holds and not what the binding substitutes on load. The two refusals are
    the plan's and not the gate's, so a person is told before being asked. A
    row already at the value is not one of them: it is a plan that writes
    nothing, and the unheld value is not judged on it since nothing is copied.
    """
    from sqlalchemy import text

    row = (
        db.session.execute(
            text(
                f"SELECT ID, Title, FolderPath, {LINK} FROM {rb_writer.CONTENT_TABLE} "
                f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
            ),
            {"id": content_id},
        )
        .mappings()
        .first()
    )
    if row is None:
        raise refuse(
            ROW_UNKNOWN,
            f"no live content row carries the identifier {content_id!r}; a row "
            f"rekordbox has removed from the collection is not written to",
            steps=("name a live row's identifier, as the collection export or SQL shows it",),
            origin=_ORIGIN,
            detail={"content_id": content_id},
        )
    was = "" if row[LINK] is None else str(row[LINK]).strip()
    carriers = _count(db, value, excluding=content_id)
    if carriers == 0 and was != str(value):
        raise refuse(
            VALUE_UNHELD,
            f"no other live row carries {LINK} {value}; the probe copies a value "
            f"rekordbox wrote onto a row it did not, and a value nothing carries "
            f"is not that",
            steps=("read the value from a row rekordbox made and loads, and name that",),
            origin=_ORIGIN,
            detail={"content_id": content_id, "value": value},
        )
    fellows = _count(db, row[LINK], excluding=content_id) if was else 0
    rows = int(
        db.session.execute(
            text(
                f"SELECT COUNT(*) FROM {rb_writer.CONTENT_TABLE} "
                f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
            )
        ).scalar()
        or 0
    )
    return LinkPlan(
        content_id=str(row["ID"]),
        title=str(row["Title"] or ""),
        path=str(row["FolderPath"] or ""),
        value=value,
        was=was,
        carriers=carriers,
        fellows=fellows,
        rows=rows,
    )


# ---------------------------------------------------------------------------
# The apply and the read back
# ---------------------------------------------------------------------------


def assert_row_as_planned(plan: LinkPlan, now: Mapping[str, Mapping[str, Any]]) -> None:
    """Refuse when the row to be written is not the row the plan read.

    THE PLAN IS MADE ON A READ HANDLE AND THE WRITE ON ANOTHER, so the apply
    asks SQL again whether the row is still live and still carries the value
    the plan read. A row changed since is a row nobody was shown.
    """
    row = now.get(plan.content_id)
    if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
        why = "no longer a live row"
    elif ("" if row.get(LINK) is None else str(row[LINK]).strip()) != plan.was:
        why = f"{LINK} changed since the plan"
    else:
        return
    raise refuse(
        "decision-stale",
        f"the row {plan.content_id} is not as the plan read it ({why}), so nothing "
        f"was written",
        steps=("run the verb again and approve the plan as it is now",),
        origin=_ORIGIN,
        detail={"moved": [f"{plan.content_id}: {why}"]},
    )


def judge(
    plan: LinkPlan,
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong. Answers (wrong, moved). Pure.

    COMPARED AS TEXT, as ``repair rows`` compares: the binding declares the
    column an integer and SQLite stores what it is given by affinity, so the
    same value can read back either way.
    """
    was, now = before.get(plan.content_id), after.get(plan.content_id)
    if was is None or now is None:
        return (f"{plan.content_id}: the row could not be read",), ()
    wrong: list[str] = []
    if now.get(LINK) is None or str(now[LINK]).strip() != str(plan.value):
        wrong.append(f"{plan.content_id}: {LINK} not {plan.value}")
    changed = sorted(
        column
        for column in now
        if column != LINK
        and column not in rb_writer.BOOKKEEPING_COLUMNS
        and now[column] != was.get(column)
    )
    moved = (f"{plan.content_id}: {', '.join(changed)}",) if changed else ()
    return tuple(wrong), moved


def _record_commit(record: session.SessionRecord, written: int, cfg: config.Config) -> None:
    """Record this write's commit on its session record, when it wrote anything."""
    if written <= 0:
        return
    session.record_commit(
        record,
        CHANGE_KEY,
        session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, updated=written),)),
        cfg,
    )


def apply_link(
    cfg: config.Config,
    db: Any,
    plan: LinkPlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write the one value, commit behind the guard, and read the row back.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as ``repair rows`` calls it: the
    three gates with a record kept, a capture the commit happens behind, the
    analysis watch over the roots named, the commit witness, and the guarded
    commit. The row is checked against the plan before the session is entered,
    so a stale plan refuses with no record and no capture, and the policy is
    registered after that check and before the field is set.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    if not plan.writes:
        raise refuse(
            "internal-error",
            f"the row {plan.content_id} already carries {LINK} {plan.value}, so this "
            f"plan writes nothing and the apply should not have been reached",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"content_id": plan.content_id, "value": plan.value},
        )
    ids = [plan.content_id]
    assert_row_as_planned(plan, row_defaults._columns(db, ids))
    mapped = row_defaults._mapped(db, ids)
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    # REGISTERED FOR THIS COMMIT AND THEN PUT BACK, as the repair's two
    # policies are: a registration left behind would widen the guard for every
    # writer that commits later in the process.
    was = rb_writer.registered_field_policies()
    try:
        rb_writer.register_field_policy(rb_writer.CONTENT_LINK_POLICY)
        with (
            session.assert_gates(
                cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
            ) as gates,
            rb_writer.commit_witness(db) as witness,
        ):
            record = gates.record
            capture = snapshot.capture(cfg, db=db)
            session.attach_capture(record, capture.root, cfg)
            snapshot.assert_verified(capture)

            before = row_defaults._columns(db, ids)
            written = 0
            try:
                decision = rb_writer.write_metadata_field(
                    mapped[plan.content_id],
                    rb_writer.CONTENT_LINK_POLICY.owner,
                    LINK,
                    plan.value,
                )
                if decision is not rb_writer.Decision.WRITE:
                    raise refuse(
                        "internal-error",
                        f"the row {plan.content_id} was planned to have {LINK} written "
                        f"and the field policy answered {decision}, so nothing was written",
                        remedy=Remedy.REPORT_DEFECT,
                        origin=_ORIGIN,
                        detail={"content_id": plan.content_id, "column": LINK},
                    )
                written = 1
                rb_writer.commit_guarded(db)
            except BaseException:
                trees._rollback_quietly(db)
                # AN EXCEPTION IS NOT PROOF NOTHING LANDED. The witness is the
                # engine's own answer.
                if witness.landed:
                    _record_commit(record, written, cfg)
                raise
            _record_commit(record, written, cfg)
            convergence.record_fingerprint(cfg, db)

            after = row_defaults._columns(db, ids)
            session_id = record.session_id
    finally:
        rb_writer.reset_field_policies()
        for policy in was.values():
            rb_writer.register_field_policy(policy)

    wrong, moved = judge(plan, before, after)
    return Written(
        session_id=session_id,
        written=written,
        read_back=1 - len(wrong),
        wrong=wrong,
        moved=moved,
    )


def assert_read_back(written: Written) -> None:
    """Refuse when the database does not say what the plan said it would.

    A COLUMN THAT MOVED IS REPORTED AS THE GUARD'S DEFECT, because the guard
    holds that before the commit and reaching here means it did not. Either way
    the write is durable, so the refusal names the session whose capture undoes
    it.
    """
    if not written.wrong and not written.moved:
        return
    undo = (f"the write is durable; restore session {written.session_id} to undo it",)
    if written.moved:
        raise refuse(
            "whitelist-violation",
            "the probed row has another column changed after the commit, which "
            "the guard should have refused before it: " + row_defaults.named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        "the probed row does not read back as planned: " + row_defaults.named(written.wrong),
        remedy=Remedy.REPORT_DEFECT,
        steps=undo,
        origin=_ORIGIN,
        detail={"wrong": list(written.wrong), "session": written.session_id},
    )


__all__ = [
    "CHANGE_KEY",
    "LINK",
    "ROW_UNKNOWN",
    "VALUE_UNHELD",
    "WORKFLOW",
    "LinkPlan",
    "Written",
    "apply_link",
    "assert_read_back",
    "assert_row_as_planned",
    "judge",
    "plan_link",
]
