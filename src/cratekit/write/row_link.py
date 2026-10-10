"""Write chosen values into the row probe columns of chosen live content rows,
through the guard, to learn which column keeps a binding made row off a deck
(A32, R-928).

WHY THIS EXISTS. A row the native landing makes shows every column in
rekordbox, analyses on request, and will not load to a deck, while a row
rekordbox imports from the same file loads at once (R-928). The defaults were
filled (R-923) and the file id was given its inode (U115), and at sitting 36
of ``docs/cutover.md`` the repaired rows still would not load. On 2026-10-10
every one of the 78 content columns was compared between the binding rows and
the rows rekordbox made, and three binding values occur on no row rekordbox
made: ``ContentLink``, ``ISRC`` stored NULL, and ``AnalysisUpdated`` at 1.
The first two are :data:`cratekit.core.rb_writer.ROW_PROBE_COLUMNS`. The third
is an analysis column the guard refuses under R17, and is tested by letting
rekordbox analyse a row again, never by writing it.

ONE PLAN, MANY TRIPLES, ONE REKORDBOX OPEN. A probe is a list of (row, column,
value) triples, so each subset of the candidates can sit on its own row and a
single reading of rekordbox's context menus answers every subset at once,
rather than one candidate per sitting.

WHAT IT WRITES IS THE NAMED COLUMNS ON THE NAMED ROWS AND NOTHING ELSE, through
:func:`cratekit.core.rb_writer.write_metadata_field` under a policy
:func:`cratekit.core.rb_writer.row_probe_policy` builds from exactly the
columns the plan writes, registered for the commit and put back after it.

A LIVE ROW ONLY, AND A VALUE MORE ROWS CARRY THAN CARRY THE ROW'S OWN. Each
triple's row is read from SQL with ``rb_local_deleted = 0`` and an unknown or
deleted one is refused by name. For each triple the plan counts the other live
rows carrying the value asked for in that column and the other live rows
carrying the value the row holds now, NULL counted as NULL, and refuses when
the first is zero or not above the second: the probe moves a row toward the
value the library's rows mostly carry, never away from it. A triple whose row
already holds the value plans nothing and is shown as such.

EVERY WRITTEN ROW IS READ AGAIN FROM SQL AFTER THE COMMIT. Each written column
must read as its value, and no column outside the ones written on that row and
the binding's bookkeeping may have moved.

THE DIGEST NAMES NO COPY. The rows, columns and values, written and replaced,
so a rehearsal on a disposable copy digests equal to the live plan when the
rows are the same, which is what lets a session approve the live write.

Layer: write. It opens no database of its own and names no verb.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
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

#: What the write is filed under in a session record's change summary.
CHANGE_KEY = "content.probe"

#: The ContentLink column, the writer's name for it.
LINK = rb_writer.CONTENT_LINK_COLUMN

#: The recording code column, the writer's name for it.
ISRC = rb_writer.ISRC_COLUMN

#: A triple that does not parse, names a column the probe may not write, gives a
#: ContentLink that is not a whole number, or repeats a row and column.
PROBE_INVALID = "link-probe-invalid"

#: No live row carries the identifier asked for.
ROW_UNKNOWN = "link-row-unknown"

#: No other live row carries the value asked for.
VALUE_UNHELD = "link-value-unheld"

#: Fewer live rows carry the value asked for than carry the row's own value.
VALUE_MINORITY = "link-value-minority"

#: No single ContentLink value is carried by more than half the library's live
#: rows, so a landing has no value of rekordbox's to give the row it makes (U126).
MAJORITY_UNCLEAR = "link-majority-unclear"

_ORIGIN = ("write", "row_link")

#: A ContentLink the landing will copy: an optional minus and ASCII digits,
#: nothing else, so ``int`` can never refuse what this accepted.
_WHOLE = re.compile(r"-?[0-9]+")


def _text(value: Any) -> str | None:
    """A stored value as the probe compares it: text, or None for NULL."""
    return None if value is None else str(value).strip()


@dataclass(frozen=True, slots=True)
class Triple:
    """One requested write: a row, a probe column, and the value to put there."""

    content_id: str
    column: str
    value: int | str


def _invalid(spec: str, why: str):
    return refuse(
        PROBE_INVALID,
        f"the probe {spec!r} cannot be planned: {why}",
        steps=("give each probe as ROW:COLUMN=VALUE, one --set per probe",),
        origin=_ORIGIN,
        detail={"probe": spec},
    )


def parse_triple(spec: str) -> Triple:
    """Read ``ROW:COLUMN=VALUE``. Pure. An empty value is the empty text.

    The column must be one of :data:`cratekit.core.rb_writer.ROW_PROBE_COLUMNS`
    and the value is converted to the type the column is stored as, so a
    ContentLink that is not a whole number refuses here rather than at SQL.
    """
    head, sep, raw = spec.partition("=")
    content_id, colon, column = head.partition(":")
    content_id, column = content_id.strip(), column.strip()
    if not sep or not colon or not content_id or not column:
        raise _invalid(spec, "it does not read as ROW:COLUMN=VALUE")
    kind = rb_writer.ROW_PROBE_COLUMNS.get(column)
    if kind is None:
        raise _invalid(
            spec,
            f"{column!r} is not a column the probe may write; it writes "
            f"{', '.join(rb_writer.ROW_PROBE_COLUMNS)} and nothing else",
        )
    if kind is int:
        try:
            return Triple(content_id, column, int(raw.strip()))
        except ValueError:
            raise _invalid(spec, f"{column} is stored as a whole number") from None
    return Triple(content_id, column, raw)


@dataclass(frozen=True, slots=True)
class Probe:
    """One planned triple: the row, what its column holds, and who else holds each value."""

    content_id: str
    title: str
    path: str
    column: str
    value: int | str
    #: What the column holds now, as text, None for NULL.
    was: str | None
    #: Other live rows holding ``value`` in this column.
    carriers: int
    #: Other live rows holding ``was`` in this column, NULL counted as NULL.
    fellows: int

    @property
    def writes(self) -> bool:
        """Whether the row holds another value than the one asked for."""
        return self.was != str(self.value)

    def to_json(self) -> dict[str, Any]:
        """The item as the gate shows it and the digest covers it, values as text."""
        return {
            "content_id": self.content_id,
            "title": self.title,
            "path": self.path,
            "column": self.column,
            "from": self.was,
            "to": str(self.value),
            "writes": self.writes,
        }


@dataclass(frozen=True, slots=True)
class ProbePlan:
    """Every planned triple, ordered by row then column, and the live rows read."""

    probes: tuple[Probe, ...]
    rows: int

    @property
    def writing(self) -> tuple[Probe, ...]:
        """The triples whose row holds another value, the only ones written."""
        return tuple(probe for probe in self.probes if probe.writes)

    @property
    def writes(self) -> int:
        return len(self.writing)

    @property
    def content_ids(self) -> list[str]:
        """Every row written, once each, in plan order."""
        return list(dict.fromkeys(probe.content_id for probe in self.writing))

    def columns_on(self, content_id: str) -> tuple[str, ...]:
        """The columns this plan writes on one row."""
        return tuple(p.column for p in self.writing if p.content_id == content_id)

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to.

        OVER EVERY TRIPLE, the value written and the value replaced, and nothing
        that names a copy. The counts are not in it: they are what the gate
        shows and not what the approval is for.
        """
        return digest_of({"kind": WORKFLOW, "items": [p.to_json() for p in self.probes]})


@dataclass(frozen=True, slots=True)
class Written:
    """What one apply did, and what the database says about it afterwards."""

    session_id: str
    written: int
    rows: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def _holding(db: Any, column: str, value: Any, *, excluding: str) -> int:
    """How many live rows other than ``excluding`` hold ``value`` in ``column``."""
    from sqlalchemy import text

    test = f"{column} IS NULL" if value is None else f"{column} = :value"
    found = db.session.execute(
        text(
            f"SELECT COUNT(*) FROM {rb_writer.CONTENT_TABLE} WHERE {test} "
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
        ),
        {"value": value, "id": excluding},
    )
    return int(found.scalar() or 0)


@dataclass(frozen=True, slots=True)
class LibraryLink:
    """The ContentLink the library's live rows mostly carry, and how many carry it (U126)."""

    value: int
    #: Live rows carrying ``value``.
    carriers: int
    #: Live rows read, NULL included.
    rows: int


def library_link(db: Any) -> LibraryLink:
    """The ContentLink more than half the live rows carry, or a refusal by name (U126).

    WHAT A ROW THE NATIVE LANDING MAKES IS GIVEN, read from the library rather
    than written down. The binding sets the column from a menu item's counter,
    and rekordbox refuses such a row a deck (R-928); rekordbox writes one value
    on nearly every row it makes, ``2950670`` on 10,312 of 10,498 live rows of
    the library measured on 2026-10-10. That number is a measurement of one
    library and not a constant of rekordbox, so it is read here on every plan.

    MORE THAN HALF, NULL COUNTED AS ITS OWN VALUE, and the value a whole
    number. A library with no rows, or whose rows split so that no value holds
    a majority, or whose majority is NULL, has nothing to copy, and the landing
    refuses before its gate rather than choose: a plurality is a guess about
    which value rekordbox will load, and a wrong guess is a row nobody can play.
    """
    from sqlalchemy import text

    counted = db.session.execute(
        text(
            f"SELECT {LINK}, COUNT(*) FROM {rb_writer.CONTENT_TABLE} "
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0 GROUP BY {LINK} "
            f"ORDER BY COUNT(*) DESC"
        )
    ).all()
    rows = sum(int(count) for _value, count in counted)
    value, carriers = counted[0] if counted else (None, 0)
    whole = _text(value)
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
        return LibraryLink(value=int(whole), carriers=int(carriers), rows=rows)
    shown = "no value" if not counted else ("NULL" if whole is None else repr(whole))
    raise refuse(
        MAJORITY_UNCLEAR,
        f"the most common {LINK} on the library's {rows} live row(s) is {shown}, "
        f"carried by {carriers}, which is not a whole number held by more than "
        f"half of them; a row this landing makes takes the value rekordbox "
        f"writes on its own rows, and with no clear majority there is none to take",
        steps=(
            "import these files through rekordbox's own import, which gives each row "
            "its own value; the native landing cannot choose one for this library",
        ),
        origin=_ORIGIN,
        detail={
            "column": LINK,
            "value": whole,
            "carriers": int(carriers),
            "rows": rows,
        },
    )


def plan_probes(db: Any, triples: Sequence[Triple]) -> ProbePlan:
    """Every triple planned against the live rows, or the first refusal by name.

    FROM SQL AND NOT FROM THE MAPPED ROWS, so a NULL is what the table holds.
    The refusals are the plan's and not the gate's, so a person is told before
    being asked. A triple whose row already holds the value is planned and not
    judged, since nothing is copied.
    """
    from sqlalchemy import text

    if not triples:
        raise _invalid("", "no probe was given")
    seen: set[tuple[str, str]] = set()
    for triple in triples:
        key = (triple.content_id, triple.column)
        if key in seen:
            raise _invalid(
                f"{triple.content_id}:{triple.column}",
                "that row and column are probed twice in one plan",
            )
        seen.add(key)

    probes: list[Probe] = []
    for triple in triples:
        column = triple.column
        row = (
            db.session.execute(
                text(
                    f"SELECT ID, Title, FolderPath, {column} FROM {rb_writer.CONTENT_TABLE} "
                    f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
                ),
                {"id": triple.content_id},
            )
            .mappings()
            .first()
        )
        if row is None:
            raise refuse(
                ROW_UNKNOWN,
                f"no live content row carries the identifier {triple.content_id!r}; "
                f"a row rekordbox has removed from the collection is not written to",
                steps=("name a live row's identifier, as the collection export or SQL shows it",),
                origin=_ORIGIN,
                detail={"content_id": triple.content_id},
            )
        was = _text(row[column])
        carriers = _holding(db, column, triple.value, excluding=triple.content_id)
        fellows = _holding(db, column, row[column], excluding=triple.content_id)
        probe = Probe(
            content_id=str(row["ID"]),
            title=str(row["Title"] or ""),
            path=str(row["FolderPath"] or ""),
            column=column,
            value=triple.value,
            was=was,
            carriers=carriers,
            fellows=fellows,
        )
        shown = "NULL" if was is None else repr(was)
        if probe.writes and carriers == 0:
            raise refuse(
                VALUE_UNHELD,
                f"no other live row carries {column} {triple.value!r}; the probe "
                f"copies a value rekordbox wrote onto a row it did not, and a value "
                f"nothing carries is not that",
                steps=("read the value from a row rekordbox made and loads, and name that",),
                origin=_ORIGIN,
                detail={"content_id": probe.content_id, "column": column, "value": triple.value},
            )
        if probe.writes and carriers <= fellows:
            raise refuse(
                VALUE_MINORITY,
                f"{carriers} other live row(s) carry {column} {triple.value!r} and "
                f"{fellows} carry the row's own {shown}, so the write would move the "
                f"row {probe.content_id} away from the value the library's rows mostly "
                f"carry; the probe only moves a row toward it",
                steps=("name a row that carries the minority value, and the majority value to write",),
                origin=_ORIGIN,
                detail={
                    "content_id": probe.content_id,
                    "column": column,
                    "value": triple.value,
                    "carriers": carriers,
                    "replaced": was,
                    "fellows": fellows,
                },
            )
        probes.append(probe)

    rows = int(
        db.session.execute(
            text(
                f"SELECT COUNT(*) FROM {rb_writer.CONTENT_TABLE} "
                f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
            )
        ).scalar()
        or 0
    )
    probes.sort(key=lambda p: (len(p.content_id), p.content_id, p.column))
    return ProbePlan(probes=tuple(probes), rows=rows)


# ---------------------------------------------------------------------------
# The apply and the read back
# ---------------------------------------------------------------------------


def assert_rows_as_planned(plan: ProbePlan, now: Mapping[str, Mapping[str, Any]]) -> None:
    """Refuse when a row to be written is not the row the plan read.

    THE PLAN IS MADE ON A READ HANDLE AND THE WRITE ON ANOTHER, so the apply
    asks SQL again whether each row is still live and each column still holds
    what the plan read. Nothing is written for any row when one has moved.
    """
    moved: list[str] = []
    for probe in plan.writing:
        row = now.get(probe.content_id)
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
            moved.append(f"{probe.content_id}: no longer a live row")
        elif _text(row.get(probe.column)) != probe.was:
            moved.append(f"{probe.content_id}: {probe.column} changed since the plan")
    if moved:
        moved = list(dict.fromkeys(moved))
        raise refuse(
            "decision-stale",
            f"{len(moved)} of the planned writes are not as the plan read them, so "
            f"nothing was written: " + row_defaults.named(moved),
            steps=("run the verb again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


def judge(
    plan: ProbePlan,
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong. Answers (wrong, moved). Pure.

    COMPARED AS TEXT, as ``repair rows`` compares, since SQLite stores what it
    is given by affinity and the same value can read back either way.
    """
    wrong: list[str] = []
    moved: list[str] = []
    for content_id in plan.content_ids:
        was, now = before.get(content_id), after.get(content_id)
        if was is None or now is None:
            wrong.append(f"{content_id}: the row could not be read")
            continue
        for probe in plan.writing:
            if probe.content_id != content_id:
                continue
            if now.get(probe.column) is None or _text(now[probe.column]) != str(probe.value):
                wrong.append(f"{content_id}: {probe.column} not {probe.value!r}")
        changed = row_defaults.moved_columns(was, now, planned=plan.columns_on(content_id))
        if changed:
            moved.append(f"{content_id}: {', '.join(changed)}")
    return tuple(wrong), tuple(moved)


def _record_commit(record: session.SessionRecord, rows: int, cfg: config.Config) -> None:
    """Record this write's commit on its session record, when it wrote anything."""
    if rows <= 0:
        return
    session.record_commit(
        record,
        CHANGE_KEY,
        session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, updated=rows),)),
        cfg,
    )


def apply_probes(
    cfg: config.Config,
    db: Any,
    plan: ProbePlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write every planned value, commit behind the guard, and read the rows back.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as ``repair rows`` calls it. The
    rows are checked against the plan before the session is entered, so a
    stale plan refuses with no record and no capture. The policy names exactly
    the columns written and is registered after that check.
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
            "this plan writes nothing, every row already holds its value, and the "
            "apply should not have been reached",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"probes": len(plan.probes)},
        )
    ids = plan.content_ids
    assert_rows_as_planned(plan, row_defaults.read_columns(db, ids))
    mapped = row_defaults.read_mapped(db, ids)
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    policy = rb_writer.row_probe_policy(p.column for p in plan.writing)
    with rb_writer.field_policies_for_commit(policy):
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

            before = row_defaults.read_columns(db, ids)
            written = 0
            try:
                for probe in plan.writing:
                    decision = rb_writer.write_metadata_field(
                        mapped[probe.content_id], policy.owner, probe.column, probe.value
                    )
                    if decision is not rb_writer.Decision.WRITE:
                        raise refuse(
                            "internal-error",
                            f"the row {probe.content_id} was planned to have "
                            f"{probe.column} written and the field policy answered "
                            f"{decision}, so nothing was written",
                            remedy=Remedy.REPORT_DEFECT,
                            origin=_ORIGIN,
                            detail={"content_id": probe.content_id, "column": probe.column},
                        )
                    written += 1
                rb_writer.commit_guarded(db)
            except BaseException:
                trees._rollback_quietly(db)
                # AN EXCEPTION IS NOT PROOF NOTHING LANDED. The witness is the
                # engine's own answer.
                if witness.landed:
                    _record_commit(record, len(ids), cfg)
                raise
            _record_commit(record, len(ids), cfg)
            convergence.record_fingerprint(cfg, db)

            after = row_defaults.read_columns(db, ids)
            session_id = record.session_id

    wrong, moved = judge(plan, before, after)
    return Written(
        session_id=session_id,
        written=written,
        rows=len(ids),
        read_back=written - len(wrong),
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
            "a probed row has another column changed after the commit, which the "
            "guard should have refused before it: " + row_defaults.named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        "a probed row does not read back as planned: " + row_defaults.named(written.wrong),
        remedy=Remedy.REPORT_DEFECT,
        steps=undo,
        origin=_ORIGIN,
        detail={"wrong": list(written.wrong), "session": written.session_id},
    )


__all__ = [
    "CHANGE_KEY",
    "ISRC",
    "LINK",
    "MAJORITY_UNCLEAR",
    "PROBE_INVALID",
    "ROW_UNKNOWN",
    "VALUE_MINORITY",
    "VALUE_UNHELD",
    "WORKFLOW",
    "LibraryLink",
    "Probe",
    "ProbePlan",
    "Triple",
    "Written",
    "apply_probes",
    "assert_read_back",
    "assert_rows_as_planned",
    "judge",
    "parse_triple",
    "plan_probes",
]
