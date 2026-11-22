"""What the four favourites verbs and their writers share, written once.

:func:`run` is the verbs' one shape: the backup acknowledgment before anything
is read (R-733), the plan on a handle opened to read and closed, the gate over
the digested plan, the write on its own write handle, which takes the plan
again and refuses a digest that moved, then the read back. The writers share
their refusals, each in its own wording.

Layer: modules.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from cratekit.cli.output import Envelope, declared_gate
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome, refuse
from cratekit.write import trees

#: The key every favourites commit is recorded under on the session, as rows
#: created and rows changed. Not a tree id: the Favorites folder is nobody's tree.
RECORD_KEY = "favorites"


@contextmanager
def handle(cfg: config.Config, *, write: bool = False) -> Iterator[Any]:
    """The live library on a handle of the caller's own, opened to read or to write, and closed."""
    if write:
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    else:
        db = rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    try:
        yield db
    finally:
        rb_writer.close_db(db)


def note(code: str, message: str) -> dict[str, str]:
    """One warning a verb carries."""
    return {"code": code, "message": message}


def handles(engine: Any, plan: Callable[..., Any] | None = None) -> tuple[Callable, Callable]:
    """A verb's ``planned`` and ``written``: ``engine``'s plan and apply, each on its own handle.

    ``plan(cfg, db, source)`` stands in for ``engine.plan`` when its signature differs.
    """

    def planned(cfg: config.Config, *, source: str) -> Any:
        """The plan over the library as it stands, through a handle opened to read and closed."""
        with handle(cfg) as db:
            return plan(cfg, db, source) if plan else engine.plan(cfg, db, source=source)

    def written(cfg: config.Config, approved: Any, *, source: str) -> Any:
        """Apply the plan through a handle of this function's own, opened to write."""
        with handle(cfg, write=True) as db:
            roots = analysis_store.watch_roots(cfg)
            return engine.apply(cfg, db, approved, source=source, analysis_roots=roots)

    return planned, written


def notes(*said: tuple[Any, str, str]) -> list[dict[str, str]]:
    """Each ``(when, code, message)`` whose ``when`` holds, as a warning, in order."""
    return [note(code, message) for when, code, message in said if when]


def run(
    ctx,
    cfg: config.Config,
    gate: str,
    engine: Any,
    *,
    planned: Callable[[], Any],
    written: Callable[[Any], Any],
    idle: Callable[[Any], dict[str, str]],
    done: Callable[[Any, Any], tuple[dict[str, Any], dict[str, str]]],
    told: Callable[[Any], list[dict[str, str]]] = lambda plan: [],
    payload: Callable[[Any], dict[str, Any]] | None = None,
    gate_first: bool = False,
) -> Envelope:
    """Plan, ask, write and read back, through ``engine``'s payload, facts and read back.

    ``idle`` notes a plan with nothing to write, which opens no gate unless
    ``gate_first`` asks the gate first; ``done`` gives a write's totals and note.
    """
    spec = declared_gate(ctx.entry, gate)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned()
    data = (payload or engine.payload)(plan)
    if not (gate_first or plan.writes):
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[idle(plan)])
    warnings = told(plan)
    if ctx.gate.require(spec, plan=data, context=engine.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[*warnings, idle(plan)])

    result = written(plan)
    engine.assert_read_back(result)
    totals, said = done(plan, result)
    return ctx.envelope(
        data={**data, "totals": {**data["totals"], **totals}},
        warnings=[*warnings, said],
    )


def watched(analysis_roots: Iterable[Path | str]) -> list[Path]:
    """The roots the analysis-file watch covers, refused when there are none."""
    roots = [Path(root) for root in analysis_roots]
    if not roots:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    return roots


def fresh(again: Any, approved: Any, said: str, origin: tuple[str, str]) -> Any:
    """``again``, the plan taken on the write handle, refused when its digest moved."""
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            f"{said}; run it again and approve what it shows now",
            origin=origin,
            detail={"approved": approved.digest, "now": again.digest},
        )
    return again


def change(created: int, updated: int) -> session.ChangeSummary:
    """A commit's change under the favourites key, which is nobody's registered tree."""
    return session.ChangeSummary(
        (session.TreeChange(tree=RECORD_KEY, created=created, updated=updated),)
    )


@contextmanager
def witnessed(db: Any, landed: Callable[[], None]) -> Iterator[None]:
    """A commit witnessed: anything raised rolls back, and one that landed is still recorded."""
    with rb_writer.commit_witness(db) as witness:
        try:
            yield
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                landed()
            raise


def confined(
    db: Any,
    violations_of: Callable[[rb_writer.NodeTables], list[str]],
    said: str,
    origin: tuple[str, str],
) -> None:
    """Refuse, before the commit, a write that reached what its plan did not name, read from SQL.

    The pending work is flushed DELIBERATELY, inside the transaction, so the
    second reading sees it and a refusal still rolls back, as
    :func:`rb_writer.assert_node_changes_confined` does for the same reason.
    """
    db.session.flush()
    violations = violations_of(rb_writer.node_tables(db))
    if violations:
        db.rollback()
        raise refuse(
            "whitelist-violation",
            f"{said}, read from SQL before the commit, so nothing was written:\n  - "
            + "\n  - ".join(violations),
            origin=origin,
            detail={"violations": violations},
        )


def changed(columns: Iterable[str], before: Iterable[Any], after: Iterable[Any]) -> set[str]:
    """The columns one row's two readings differ in."""
    return {name for name, old, new in zip(columns, before, after) if old != new}


def verified(done: Any, said: str, origin: tuple[str, str], *, commits: str = "commit") -> None:
    """Refuse an answer the database does not hold."""
    if done.disagreements:
        raise refuse(
            "session-committed-unverified",
            f"{said}: "
            + "; ".join(done.disagreements)
            + f"; the {commits} landed and this answer cannot be vouched for",
            origin=origin,
            detail={"disagreements": list(done.disagreements), "session": done.session_id},
        )
