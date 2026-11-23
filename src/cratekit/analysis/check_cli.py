"""``crate analyze check``: is the rekordbox visit done, and done right (U167).

The engine is :mod:`cratekit.analysis.rekordbox_check`. What a skill needs
from this verb is the exit status: **0** when the visit is done, **12** (a
pending action verified by this verb) while rows wait for analysis, **27**
under ``analysis-suspect`` when a grid looks wrong. An empty scope ends
``no_op``, exit 0, with a warning that nothing was checked. A title whose key
or tempo differs from rekordbox's is counted and named with the verb that
gives the title rekordbox's, ``crate analyze adopt``, and never holds the
visit (U327).

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from cratekit.analysis import rekordbox_check as rc
from cratekit.cli import output
from cratekit.cli.output import Envelope, PendingHumanAction, load_config
from cratekit.core import active_taxonomy, config
from cratekit.core.cause import Cause, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.core.naming import NameTemplate

_ORIGIN = ("analysis.check_cli",)

#: The warning a scope with no row in it ends on.
NOTHING_CHECKED = "analysis-check-nothing"

#: The warning naming the session records the log could not read.
RECORDS_UNREAD = "analysis-check-records-unread"

#: The verb that gives a differing title rekordbox's key and tempo (U327).
ADOPT_VERB = "crate analyze adopt"

#: How many rows a check's detail names before it counts the rest.
_NAMED = 8


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
    return NameTemplate.lossy(cfg.naming.lossy_marker)


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
        # NAMED, NOT ONLY COUNTED: an ok verdict should say what it did not cover.
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
    compared = found.key_compared
    agreement = (
        f"{counts[rc.KEY_EQUAL]} of {compared} title key(s) equal rekordbox's, "
        f"{counts[rc.KEY_ONE_STEP]} one Camelot step away, {counts[rc.KEY_FAR]} far, "
        f"{counts[rc.KEY_UNKEYED]} not compared"
    )
    differing = found.differing
    headless = found.headless
    tempos = summary["tempo_differs"]
    agreement += f"; {tempos} title tempo(s) more than {rc.TEMPO_TOLERANCE} beat from rekordbox's"
    if differing:
        agreement += (
            f"; {len(differing)} title(s) name another key or tempo than rekordbox "
            f"found, and {ADOPT_VERB} gives them rekordbox's: "
            + _named(list(differing), _title)
        )
    if headless:
        # EVERY ROW A RUN SINCE U343 LANDED carries no head until the visit's
        # adopt stamps rekordbox's (U342), so the line names the verb for them too.
        agreement += (
            f"; {len(headless)} title(s) rekordbox keyed carry no head, and {ADOPT_VERB} "
            f"gives each it can one built from rekordbox's key and tempo, naming any "
            f"it leaves: " + _named(list(headless), _title)
        )
    checks.append(
        _check("check.key_agreement", "info" if differing or headless else "ok", agreement)
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
                    f"{found.scope.unreadable_records} session record(s) could not be "
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
    cfg = load_config(_ORIGIN)
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
    "ADOPT_VERB",
    "NOTHING_CHECKED",
    "RECORDS_UNREAD",
    "analyze_check",
    "build",
    "checks_of",
    "payload",
    "template_of",
    "warnings_of",
]
