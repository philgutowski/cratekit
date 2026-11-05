"""``crate analyze check``: is the rekordbox visit done, and done right (U167).

The engine is :mod:`cratekit.analysis.rekordbox_check`, whose docstring says
what each verdict means. This module is how a person and a skill meet it, and
the one thing a skill needs from it is the exit status:

* **0** when the visit is done: every row in scope analysed, every grid read
  and constant (or variable on a row marked ``dyn``), and the title keys
  agreeing with rekordbox's about as often as the recorded agreement says;
* **12**, a pending action whose verify verb is this one, when rows are still
  waiting for rekordbox to analyse them;
* **27**, under ``analysis-suspect``, when what rekordbox wrote looks wrong.

A scope with no row in it ends ``no_op``, exit 0, with a warning saying nothing
was checked, since there is nothing waiting and nothing to vouch for.

It runs after rekordbox and its agent have quit, as every verb does: the
database is read through a disposable copy, which refuses while either runs.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from cratekit.analysis import rekordbox_check as rc
from cratekit.cli import output
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core import active_taxonomy, config
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.naming import MarkerRule, NameTemplate

_ORIGIN = ("analysis.check_cli",)

#: The warning a scope with no row in it ends on.
NOTHING_CHECKED = "analysis-check-nothing"

#: The warning naming the session records the log could not read.
RECORDS_UNREAD = "analysis-check-records-unread"

#: How many rows a check's detail names before it counts the rest.
_NAMED = 8


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
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb: a pass or a landing's session may name the rows, never both."""
    del entry
    named = parser.add_mutually_exclusive_group()
    named.add_argument(
        "--pass",
        dest="pass_name",
        default=None,
        help="check the rows the closed landings of this sync pass filed",
    )
    named.add_argument(
        "--session",
        dest="session_id",
        default=None,
        help="check the rows one closed landing filed, named by its session id",
    )
    parser.set_defaults(_handler=analyze_check)


def template_of(cfg: config.Config) -> NameTemplate:
    """The name template the heads were written with, the analysis run's own."""
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))


def _named(rows: list[rc.Row], say) -> str:
    """Up to :data:`_NAMED` rows, each in ``say``'s words, and how many more."""
    shown = "; ".join(say(row) for row in rows[:_NAMED])
    more = len(rows) - _NAMED
    return f"{shown}; and {more} more" if more > 0 else shown


def _title(row: rc.Row) -> str:
    return row.title or row.content_id


def _check(key: str, status: str, detail: str, remedy: Remedy | None = None) -> dict[str, Any]:
    """One diagnostic check, the doctor's shape."""
    return {
        "key": key,
        "title": key.replace("check.", "").replace("_", " "),
        "status": status,
        "detail": detail,
        "remedy": str(remedy) if remedy is not None else None,
    }


def checks_of(found: rc.Check) -> list[dict[str, Any]]:
    """The four questions the brief asks, each answered as a check, the scope first."""
    scope = found.scope
    passed = "; ".join(why for why in scope.passed_over if why)
    checks = [
        _check(
            "check.scope",
            "info",
            f"{len(found.rows)} row(s) from {scope.name}" + (f" ({passed})" if passed else ""),
        )
    ]
    gone = [row for row in found.rows if row.state == rc.GONE]
    if gone:
        # NAMED, NOT ONLY COUNTED (review round one): a row the scope held
        # whose collection row is missing or removed is read by nobody, and a
        # person reading an ok verdict should see which rows it did not cover.
        checks.append(
            _check(
                "check.gone",
                "info",
                f"{len(gone)} row(s) in scope are no longer in the collection and were "
                f"not checked: " + _named(gone, lambda row: f"{_title(row)} ({row.why})"),
            )
        )
    waiting = [row for row in found.rows if row.state == rc.NOT_ANALYSED]
    checks.append(
        _check(
            "check.analysed",
            "fail" if waiting else "ok",
            (
                f"{len(waiting)} of {len(found.rows)} row(s) not analysed: "
                + _named(waiting, lambda row: f"{_title(row)} ({row.why})")
            )
            if waiting
            else f"{found.counted(rc.ANALYSED)} row(s) analysed",
            Remedy.COMPLETE_PENDING_ACTION if waiting else None,
        )
    )
    suspect = [row for row in found.analysed if row.suspect_grid]
    summary = found.summary()
    checks.append(
        _check(
            "check.grids",
            "fail" if suspect else "ok",
            (
                f"{len(suspect)} grid(s) not right: "
                + _named(
                    suspect,
                    lambda row: (
                        f"{_title(row)} variable {row.grid.low / 100:.2f} to "
                        f"{row.grid.high / 100:.2f}, not marked {rc.DYN_VALUE}"
                        if row.grid.state == rc.VARIABLE
                        else f"{_title(row)} {row.grid.state}: {row.grid.why}"
                    ),
                )
            )
            if suspect
            else (
                f"{summary['grids'][rc.CONSTANT]} constant, "
                f"{summary['grids'][rc.VARIABLE]} variable on rows marked {rc.DYN_VALUE}"
            ),
        )
    )
    unkeyed = [row for row in found.analysed if row.key is None]
    checks.append(
        _check(
            "check.key_column",
            "info" if unkeyed else "ok",
            (
                f"{len(unkeyed)} analysed row(s) with the Key column empty: "
                + _named(unkeyed, _title)
            )
            if unkeyed
            else f"the Key column is filled on all {len(found.analysed)} analysed row(s)",
        )
    )
    counts = found.key_counts
    floor = summary["key_equal_floor"]
    compared = found.key_compared
    agreement = (
        f"{counts[rc.KEY_EQUAL]} of {compared} title key(s) equal rekordbox's, "
        f"{counts[rc.KEY_ONE_STEP]} one Camelot step away, {counts[rc.KEY_FAR]} far, "
        f"{counts[rc.KEY_UNKEYED]} not compared"
    )
    if floor is not None:
        agreement += (
            f"; the recorded agreement puts the floor for {compared} at "
            f"{100 * floor:.1f}% equal"
        )
    checks.append(
        _check("check.key_agreement", "fail" if found.key_suspect else "ok", agreement)
    )
    return checks


def payload(found: rc.Check) -> dict[str, Any]:
    """The diagnostic surface: the checks, and the summary with every row."""
    return {
        "checks": checks_of(found),
        "summary": {**found.summary(), "items": [row.as_dict() for row in found.rows]},
    }


def _waiting_action(ctx, found: rc.Check) -> PendingHumanAction:
    """What a person does next when rows wait: the visit, then this verb again."""
    waiting = found.counted(rc.NOT_ANALYSED)
    return PendingHumanAction(
        kind="external_step",
        id=f"analyze-check-{ctx.run.run_id}",
        summary=(
            f"{waiting} row(s) of {found.scope.name} are not analysed yet; analyse them "
            f"in rekordbox and check again"
        ),
        verify_verb=ctx.entry.name,
        steps=(
            f"open rekordbox, select {found.scope.name} and run Analyze Tracks on it",
            "quit rekordbox and let its background agent close",
            "run crate analyze check again",
        ),
    )


def _suspect_cause(found: rc.Check) -> Cause:
    """The refusal a suspect visit ends on, its steps naming what to analyse again."""
    summary = found.summary()
    variable = summary["variable_not_dyn"]
    unread = sum(summary["grids"][state] for state in (rc.ABSENT, rc.MISSING, rc.UNREADABLE))
    said = []
    steps = []
    if variable:
        said.append(
            f"{variable} row(s) have variable grids and are not marked {rc.DYN_VALUE}, the "
            f"widest moving {summary['widest_span']:.2f} inside one track"
        )
        steps.append(
            "analyse those rows again in rekordbox with Analysis Mode Normal, which gives "
            "a track one tempo"
        )
    if unread:
        said.append(f"{unread} analysed row(s) have a grid this check could not read")
        steps.append("analyse those rows again in rekordbox so each writes its analysis file")
    if found.key_suspect:
        counts = found.key_counts
        said.append(
            f"only {counts[rc.KEY_EQUAL]} of {found.key_compared} title keys equal "
            f"rekordbox's, below the {100 * summary['key_equal_floor']:.1f}% the recorded "
            f"agreement allows for that many"
        )
        steps.append(
            "check that rekordbox's key analysis was on, and compare a few far keys by ear"
        )
    steps.append("quit rekordbox and its agent, then run crate analyze check again")
    error = refuse(
        "analysis-suspect",
        f"rekordbox analysed {found.scope.name} and the result looks wrong: "
        + "; ".join(said),
        steps=tuple(steps),
        origin=_ORIGIN,
        detail={"verdict": rc.SUSPECT, "scope": found.scope.kind},
    )
    return error.cause


def warnings_of(found: rc.Check) -> list[dict[str, str]]:
    """What the envelope says beside the verdict."""
    warnings = []
    if found.scope.unreadable_records:
        warnings.append(
            {
                "code": RECORDS_UNREAD,
                "message": (
                    f"the session log could not be listed, so a landing of "
                    f"{found.scope.name} in it is not in this check"
                    if found.scope.log_unlisted
                    else f"{found.scope.unreadable_records} session record(s) could not be "
                    f"read, so a landing of {found.scope.name} among them is not in this "
                    f"check"
                ),
            }
        )
    if found.verdict == rc.NOTHING:
        warnings.append(
            {
                "code": NOTHING_CHECKED,
                "message": (
                    f"{found.scope.name} holds no row to check, so nothing was checked; "
                    f"name a landing with --pass or --session to check its rows"
                ),
            }
        )
    return warnings


def analyze_check(ctx) -> Envelope:
    """Read rekordbox's result for the rows in scope and answer with the verdict."""
    cfg = _load()
    found = rc.check(
        cfg,
        declared=active_taxonomy.load(cfg),
        template=template_of(cfg),
        pass_name=ctx.args.pass_name,
        session_id=ctx.args.session_id,
    )
    data = payload(found)
    warnings = warnings_of(found)
    verdict = found.verdict
    if verdict == rc.SUSPECT:
        # THROUGH ``from_cause``, the one boundary where a cause becomes a
        # status, with the checks and every row kept on the diagnostic surface,
        # since what looked wrong is exactly what a person needs next.
        refused = output.from_cause(
            verb=ctx.entry.name,
            run_id=ctx.run.run_id,
            started=ctx.started,
            cause=_suspect_cause(found),
            schema=ctx.entry.output_schema,
            data=data,
        )
        return replace(refused, warnings=tuple(warnings))
    if verdict == rc.WAITING:
        return ctx.envelope(
            data=data,
            outcome=Outcome.PENDING,
            code=ExitCode.PENDING_HUMAN,
            pending=_waiting_action(ctx, found),
            warnings=warnings,
        )
    return ctx.envelope(
        data=data,
        outcome=Outcome.NO_OP if verdict == rc.NOTHING else Outcome.OK,
        warnings=warnings,
    )


__all__ = [
    "NOTHING_CHECKED",
    "RECORDS_UNREAD",
    "analyze_check",
    "build",
    "checks_of",
    "payload",
    "template_of",
    "warnings_of",
]
