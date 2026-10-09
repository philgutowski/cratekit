"""Fill rekordbox's own defaults on a content row that lacks them (R-923).

WHY THIS EXISTS. The native landing made each row with the binding's
``add_content`` and set nothing else, so twenty one columns rekordbox fills on
every row it makes were left NULL. Such a row is accepted, analysed and stable,
and rekordbox will not load it to a deck. The landing now sets them; this is
the repair for rows landed before it did, done in place so every membership the
row already holds stays where it is.

WHAT IT WRITES IS :data:`cratekit.core.rb_writer.CONTENT_ROW_DEFAULTS` AND
NOTHING ELSE, and only into a column that is NULL. Each value is the column's
own empty, so nothing a person could have set is replaced: a value already
present, a rating or a colour included, is not listed and not written. The
write goes through :func:`cratekit.core.rb_writer.write_metadata_field` under
:data:`cratekit.core.rb_writer.ROW_DEFAULTS_POLICY`, registered by the apply
for its commit and put back after it, so the guard's writable columns widen for
this commit and for no other.

A LIVE ROW ONLY. The plan reads ``rb_local_deleted = 0`` from SQL, so a soft
deleted row, of which a live library holds hundreds with these columns NULL, is
never listed, and neither is a row whose marker cannot say.

EVERY WRITTEN ROW IS READ AGAIN FROM SQL AFTER THE COMMIT. Each planned column
must read as its default, and no column outside the planned ones and the
binding's bookkeeping may have moved. A tempo or a grid moving refuses there by
name, after the guard already refused it before the commit.

THE DIGEST NAMES NO COPY. No database path, no state path and no time, so a
rehearsal on a disposable copy of the database digests equal to the live plan
when the rows are the same, which is what lets a session approve the live write
on its own (R-922 is the landing that does not).

Layer: write. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees

#: The name a session record carries for this write.
WORKFLOW = "repair-rows"

#: What the write is filed under in a session record's change summary. A stable
#: identifier and never a display name.
CHANGE_KEY = "content.defaults"

#: The columns this repair fills, in the order the screen and the digest list them.
COLUMNS: tuple[str, ...] = tuple(rb_writer.CONTENT_ROW_DEFAULTS)

#: How many offending rows a refusal's sentence names. The detail carries all.
_NAMED_ROWS = 5

#: How many identifiers one SQL statement names. Under every SQLite build's
#: bound parameter limit, the oldest of which is 999.
_CHUNK = 500

_ORIGIN = ("write", "row_defaults")


@dataclass(frozen=True, slots=True)
class Item:
    """One live row with at least one default column NULL, and which ones."""

    content_id: str
    title: str
    path: str
    columns: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        """The item as the gate shows it and the digest covers it."""
        return {
            "content_id": self.content_id,
            "title": self.title,
            "path": self.path,
            "fills": list(self.columns),
        }


@dataclass(frozen=True, slots=True)
class DefaultsPlan:
    """Every live row missing a default, and how many live rows were read."""

    items: tuple[Item, ...]
    rows: int

    @property
    def fills(self) -> int:
        """Every column this plan writes, across every row."""
        return sum(len(item.columns) for item in self.items)

    def by_column(self) -> dict[str, int]:
        """How many rows each column is filled on, every column named, zeros included."""
        counts = dict.fromkeys(COLUMNS, 0)
        for item in self.items:
            for column in item.columns:
                counts[column] += 1
        return counts

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to.

        OVER THE ITEMS, THE ROW COUNT AND THE VALUES WRITTEN, AND NOTHING THAT
        NAMES A COPY, so a rehearsal on a disposable copy digests equal to the
        live plan when the rows are the same. The values are in it so a build
        that changes a default is a different plan.
        """
        return digest_of(
            {
                "kind": WORKFLOW,
                "items": [item.to_json() for item in self.items],
                "rows": self.rows,
                "defaults": {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()},
            }
        )


@dataclass(frozen=True, slots=True)
class Written:
    """What one apply did, and what the database says about it afterwards.

    ``wrong`` names each written row whose planned column does not read back as
    its default. ``moved`` names each written row with any other column changed
    beyond the binding's bookkeeping. Both are empty on a good run and
    :func:`assert_read_back` refuses when either is not.
    """

    session_id: str
    written: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def plan_rows(db: Any) -> DefaultsPlan:
    """Every live content row with a default column NULL, from SQL, by identifier.

    FROM SQL AND NOT FROM THE MAPPED ROWS, so a NULL is what the table holds and
    not what the binding substitutes on load. Ordered by identifier, so the
    digest is the same whatever order the database returns rows in.
    """
    from sqlalchemy import text

    selected = ", ".join(COLUMNS)
    result = db.session.execute(
        text(
            f"SELECT ID, Title, FolderPath, {selected} FROM {rb_writer.CONTENT_TABLE} "
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
        )
    )
    items: list[Item] = []
    rows = 0
    for row in result.mappings():
        rows += 1
        missing = tuple(column for column in COLUMNS if row[column] is None)
        if missing:
            items.append(
                Item(
                    content_id=str(row["ID"]),
                    title=str(row["Title"] or ""),
                    path=str(row["FolderPath"] or ""),
                    columns=missing,
                )
            )
    items.sort(key=lambda item: (len(item.content_id), item.content_id))
    return DefaultsPlan(items=tuple(items), rows=rows)


# ---------------------------------------------------------------------------
# The apply and the read back
# ---------------------------------------------------------------------------


def _chunks(values: Sequence[str]) -> Iterable[Sequence[str]]:
    for start in range(0, len(values), _CHUNK):
        yield values[start : start + _CHUNK]


def _columns(db: Any, content_ids: Sequence[str]) -> dict[str, dict[str, Any]]:
    """Every column of the named content rows, from SQL, by content identifier."""
    from sqlalchemy import text

    found: dict[str, dict[str, Any]] = {}
    for chunk in _chunks(content_ids):
        marks = ", ".join(f":id{index}" for index in range(len(chunk)))
        result = db.session.execute(
            text(f"SELECT * FROM {rb_writer.CONTENT_TABLE} WHERE ID IN ({marks})"),
            {f"id{index}": value for index, value in enumerate(chunk)},
        )
        for row in result.mappings():
            found[str(row["ID"])] = dict(row)
    return found


def _mapped(db: Any, content_ids: Sequence[str]) -> dict[str, Any]:
    """The mapped content rows the write sets fields on, by identifier."""
    from pyrekordbox.db6 import tables

    found: dict[str, Any] = {}
    for chunk in _chunks(content_ids):
        query = db.session.query(tables.DjmdContent).filter(tables.DjmdContent.ID.in_(chunk))
        for row in query.all():
            found[str(row.ID)] = row
    return found


def _named(offenders: Sequence[str]) -> str:
    """The first few offenders as a sentence, and how many more there are."""
    shown = "; ".join(offenders[:_NAMED_ROWS])
    more = len(offenders) - _NAMED_ROWS
    return shown + (f"; and {more} more, all in the detail" if more > 0 else "")


def assert_rows_as_planned(plan: DefaultsPlan, now: Mapping[str, Mapping[str, Any]]) -> None:
    """Refuse when a row to be written is not the row the plan read.

    THE PLAN IS MADE ON A READ HANDLE AND THE WRITE ON ANOTHER, so the apply
    asks SQL again whether each row is still live and whether every column the
    plan would fill is still NULL. A column given a value since, by rekordbox or
    by a person, is a row nobody was shown, and nothing is written for any row.
    """
    moved: list[str] = []
    for item in plan.items:
        row = now.get(item.content_id)
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
            moved.append(f"{item.content_id}: no longer a live row")
            continue
        filled = [column for column in item.columns if row.get(column) is not None]
        if filled:
            moved.append(f"{item.content_id}: {', '.join(filled)} set since the plan")
    if moved:
        raise refuse(
            "decision-stale",
            f"{len(moved)} of {len(plan.items)} row(s) to be written are not as the "
            f"plan read them, so nothing was written: " + _named(moved),
            steps=("run the verb again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


def judge(
    plan: DefaultsPlan,
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong. Answers (wrong, moved). Pure.

    COMPARED AS TEXT. The binding declares some of these columns strings where
    the live table declares integers, and SQLite stores the binding's ``'0'`` as
    rekordbox's 0 by affinity, so the same value can read back either way. The
    one float, ``SamplerGain``, was measured stored real on the live table; an
    integer affinity there would read back ``'0'`` and refuse here, after a
    durable commit, which the first live run would show at once.
    """
    wrong: list[str] = []
    moved: list[str] = []
    for item in plan.items:
        was, now = before.get(item.content_id), after.get(item.content_id)
        if was is None or now is None:
            wrong.append(f"{item.content_id}: the row could not be read")
            continue
        off = [
            column
            for column in item.columns
            if now.get(column) is None
            or str(now[column]) != str(rb_writer.CONTENT_ROW_DEFAULTS[column])
        ]
        if off:
            wrong.append(f"{item.content_id}: {', '.join(off)} not as the default")
        planned = set(item.columns)
        changed = sorted(
            column
            for column in now
            if column not in planned
            and column not in rb_writer.BOOKKEEPING_COLUMNS
            and now[column] != was.get(column)
        )
        if changed:
            moved.append(f"{item.content_id}: {', '.join(changed)}")
    return tuple(wrong), tuple(moved)


def _record_commit(record: session.SessionRecord, written: int, cfg: config.Config) -> None:
    """Record this write's commit on its session record, when it wrote anything.

    A RUN THAT WROTE NOTHING CLAIMS NO COMMIT: a restore reads a committed
    source as work it would discard.
    """
    if written <= 0:
        return
    session.record_commit(
        record,
        CHANGE_KEY,
        session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, updated=written),)),
        cfg,
    )


def _fill(plan: DefaultsPlan, mapped: Mapping[str, Any]) -> int:
    """Set every planned column on its mapped row through the field policy.

    Returns the rows written. A decision other than a write means the policy
    disagrees with a plan the staleness check has just passed, which is this
    module's defect and refuses before the commit.
    """
    owner = rb_writer.ROW_DEFAULTS_POLICY.owner
    written = 0
    for item in plan.items:
        row = mapped[item.content_id]
        for column in item.columns:
            decision = rb_writer.write_metadata_field(
                row, owner, column, rb_writer.CONTENT_ROW_DEFAULTS[column]
            )
            if decision is not rb_writer.Decision.WRITE:
                raise refuse(
                    "internal-error",
                    f"the row {item.content_id} was planned to have {column} filled "
                    f"and the field policy answered {decision}, so nothing was written",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=_ORIGIN,
                    detail={"content_id": item.content_id, "column": column},
                )
        written += 1
    return written


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: DefaultsPlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Fill the planned defaults, commit behind the guard, and read them back.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database writer here
    calls it: the three gates with a record kept, a capture the commit happens
    behind, the analysis watch over the roots named, the commit witness, and
    the guarded commit.

    THE ROWS ARE CHECKED AGAINST THE PLAN BEFORE THE SESSION IS ENTERED, so a
    stale plan refuses with no session record, no capture and nothing pending.
    The policy is registered after that check and before the first field is
    set, so the guard's writable columns include these for this commit.

    ``analysis_roots`` has no default for the reason the membership writer
    gives: a watch that watches nothing reports every session clean.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    content_ids = [item.content_id for item in plan.items]
    assert_rows_as_planned(plan, _columns(db, content_ids))
    mapped = _mapped(db, content_ids)
    # THE EVIDENCE IS READ BEFORE IT IS REPLACED, for the reason ``tag rows``
    # gives: the fingerprint recorded after the commit must not bless a
    # database recovered out of band.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    # REGISTERED FOR THIS COMMIT AND THEN PUT BACK. The policy is what admits
    # these columns, and a registration left behind would widen the guard for
    # every writer that commits later in the process. The registry as it was
    # is restored whatever happens inside, the baseline colour policy included.
    was = rb_writer.registered_field_policies()
    try:
        rb_writer.register_field_policy(rb_writer.ROW_DEFAULTS_POLICY)
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

            before = _columns(db, content_ids)
            written = 0
            try:
                written = _fill(plan, mapped)
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

            after = _columns(db, content_ids)
            session_id = record.session_id
    finally:
        rb_writer.reset_field_policies()
        for policy in was.values():
            rb_writer.register_field_policy(policy)

    wrong, moved = judge(plan, before, after)
    return Written(
        session_id=session_id,
        written=written,
        read_back=len(plan.items) - len(wrong),
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
            "a row given rekordbox's defaults has another column changed after the "
            "commit, which the guard should have refused before it: "
            + _named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        f"{len(written.wrong)} of {written.written} row(s) written do not read back "
        f"with rekordbox's defaults: " + _named(written.wrong),
        remedy=Remedy.REPORT_DEFECT,
        steps=undo,
        origin=_ORIGIN,
        detail={"wrong": list(written.wrong), "session": written.session_id},
    )


__all__ = [
    "CHANGE_KEY",
    "COLUMNS",
    "WORKFLOW",
    "DefaultsPlan",
    "Item",
    "Written",
    "apply_rows",
    "assert_read_back",
    "assert_rows_as_planned",
    "judge",
    "plan_rows",
]
