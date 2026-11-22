"""``crate doctor`` and ``crate status``: the environment, checked before it is spent.

Doctor answers named checks, each with a remedy token per failure, and
``cli/registry.py`` lets every verb declare the checks it depends on, so a
missing binary or credential is found before a paid step rather than during it
(R3). The check families live in ``doctor_model``, ``doctor_library``,
``doctor_keys``, ``doctor_backup`` and ``doctor_state``; this hub keeps
the table and the verbs.

* Every check answers on every run, so a consumer can diff two reports.
* The check order is part of the contract, the interpreter first since every
  other answer is worthless on an unsupported one.
* Whether a check is required follows the registry: a key is required when a
  verb declaring it is available under the active profile, so enabling a module
  turns its credential check from a note into a failure with no edit here.
* A failing doctor keeps its report, because the checks are the answer: it
  builds its own envelope with the report in ``data`` and a structured cause,
  and exits ``PRECONDITION``, or the code a check's own refusal reserves.

Layer note: CLI. It imports downward only, and it may render a remediation
token into words (D2).
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from cratekit.cli import gates, output, registry, render
from cratekit.cli.doctor_backup import (
    FULL_COMPARISON_DUE_DAYS,  # noqa: F401
    _check_backup_acknowledgment,
    _check_backup_portion,
    _check_backup_remote,
    _check_deadca7_push,
    _check_full_check,
    _check_full_comparison,
)
from cratekit.cli.doctor_keys import (
    BINARY_NAMES,
    CREDENTIALS_BY_CHECK,
    OFFERED_WHEN_SPENT,
    _check_adapter,
    _check_binary,
    _check_credential,
    _check_keychain,
    contract_members,
)
from cratekit.cli.doctor_library import (
    _check_config,
    _check_db_containment,
    _check_interpreter,
    _check_library_identity,
    _check_library_mounted,
    _check_paths_resolved,
    _check_rekordbox_closed,
    _check_rekordbox_pins,
    _check_taxonomy_schema,
    _check_trash,
    _library_state_unreadable,
    _origin_verdict,
    _volume_clause,
)
from cratekit.cli.doctor_model import (
    Finding,
    InstallOrigin,  # noqa: F401
    Probes,
    Report,
    Status,
    _declared_python_bound,  # noqa: F401
    _Inputs,
    _probe_trash,  # noqa: F401
    _unchecked,
    requires_check,
    satisfies,
)
from cratekit.cli.doctor_state import (
    BUDGET_CHECK,
    ISRC_CACHE_CHECK,
    NIGHT_CHECK,
    OPEN_GATES_CHECK,
    _check_commit_hook,
    _check_install_extras,
    _check_isrc_cache,
    _check_night_pass,
    _check_open_gates,
    _check_provider_budget,
    _check_release,
    _check_tree_registry,
    _check_unresolved_session,
    _open_state,  # noqa: F401
)
from cratekit.cli.output import Envelope
from cratekit.core import backup_facts, config, profiles, session, taxonomy, tree_registry
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, access_remedy
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def offered(key: str, membership: profiles.Membership) -> bool:
    """Whether setup offers ``key``'s credentials to this profile.

    True when an available verb declares the check, or when a verb
    :data:`OFFERED_WHEN_SPENT` names for it is switched on.
    """
    if requires_check(key, membership):
        return True
    spenders = OFFERED_WHEN_SPENT.get(key, ())
    return any(
        entry.name in spenders and entry.available_to(membership)
        for entry in registry.entries()
    )


def _check_taxonomy(inputs: _Inputs) -> Finding:
    key, title = "taxonomy.active", "active taxonomy template"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the active template")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    shipped, unlistable = taxonomy.shipped_templates()
    named = inputs.cfg.taxonomy.template
    if unlistable is not None:
        # "Could not look" is not "not present": a damaged install is a defect,
        # and setup cannot repair packaged data.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{unlistable}. Whether a template named {named!r} ships was "
                f"therefore not established, and neither was the active copy "
                f"beside the database. This is a damaged or partial install "
                f"rather than a configuration error, so re-running setup would "
                f"not repair it"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    if named not in shipped:
        # Asserted, so a configured name that does not ship cannot read green.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"taxonomy.template names {named!r} and no template ships under "
                f"that name; shipped: {', '.join(shipped)}. A re-run of setup "
                f"replaces a recorded name the shipped set does not contain"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    path = config.state_path("taxonomy_active", inputs.cfg)
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError):
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no active taxonomy template at {path}. S6 makes the library "
                f"self-describing by copying the chosen template beside the "
                f"database, and routing has no declared tree without it"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    except (OSError, UnicodeDecodeError) as exc:
        # Separate from "not there", since setup leaves an existing file alone,
        # and it claims no existence, since an untraversable parent lands here.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the active taxonomy template at {path} could not be read "
                f"({exc}), so whether the library declares a usable tree was not "
                f"established. Whether the file is even there is unknown too: a "
                f"directory on the way to it that this account cannot open fails "
                f"the same way. Setup leaves an existing copy alone, so this is a "
                f"permission or a corruption to repair rather than an answer to "
                f"give again"
            ),
            # A corruption is a defect to report, a permission one to grant.
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    try:
        declared = taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,
        )
    status, origin = _origin_verdict(inputs.cfg, text, named)
    return Finding(
        key=key,
        title=title,
        status=status,
        detail=(
            f"an active template at {path}, {_volume_clause(inputs)}, parses and "
            f"declares {len(declared.buckets)} buckets; taxonomy.template names "
            f"the shipped {named!r}; {origin}"
        ),
    )


@dataclass(frozen=True, slots=True)
class Check:
    """One named question and the function that answers it."""

    key: str
    run: Callable[[_Inputs], Finding]


def _bound(key: str, function: Callable[[str, _Inputs], Finding]) -> Check:
    """A check whose answer function serves a whole family of keys."""
    return Check(key=key, run=lambda inputs, _key=key: function(_key, inputs))


#: Every check in run order, which is part of the contract. The interpreter is
#: first because every other answer is worthless on an unsupported one. The
#: families expand from their own declarations, so a credential, binary or
#: backup portion added elsewhere is checked here without an edit.
CHECKS: tuple[Check, ...] = (
    Check("interpreter.version", _check_interpreter),
    Check("config.present", _check_config),
    Check("library.mounted", _check_library_mounted),
    Check("library.identity", _check_library_identity),
    Check("library.db_containment", _check_db_containment),
    Check("library.trash", _check_trash),
    Check("taxonomy.active", _check_taxonomy),
    # After the copy is known to parse (U132).
    Check("taxonomy.schema", _check_taxonomy_schema),
    Check("rekordbox.closed", _check_rekordbox_closed),
    Check("rekordbox.pins", _check_rekordbox_pins),
    # After the pins, since its answer comes off an open the binding pin governs.
    Check("library.paths_resolved", _check_paths_resolved),
    Check("keychain.reachable", _check_keychain),
    *(_bound(key, _check_credential) for key in sorted(CREDENTIALS_BY_CHECK)),
    *(_bound(f"binary.{name}", _check_binary) for name in BINARY_NAMES),
    Check("adapter.contract", _check_adapter),
    *(
        _bound(f"backup.age.{portion}", _check_backup_portion)
        for portion in backup_facts.PORTIONS
    ),
    # Right after the two ages it was minted over (U184).
    Check("backup.acknowledgment", _check_backup_acknowledgment),
    # After the ages it qualifies, before the remote they name (R-757).
    Check("backup.full_comparison", _check_full_comparison),
    Check("backup.full_check", _check_full_check),
    Check("backup.remote", _check_backup_remote),
    # After the backup checks, since it compares with the database age (U185).
    Check("deadca7.push", _check_deadca7_push),
    Check("session.unresolved", _check_unresolved_session),
    # Beside the session check, both being runs left waiting; never fails (U186).
    Check(OPEN_GATES_CHECK, _check_open_gates),
    # Another note on this installation's own state, never a failure (U206).
    Check(ISRC_CACHE_CHECK, _check_isrc_cache),
    # The other provider note, never a failure (U278).
    Check(BUDGET_CHECK, _check_provider_budget),
    # Another note on provider calls, never a failure (U293).
    Check(NIGHT_CHECK, _check_night_pass),
    # After the taxonomy check, which it lists trees from (R-235).
    Check("tree.registry", _check_tree_registry),
    Check("repo.commit_hook", _check_commit_hook),
    # Beside the release check, whose upgrade command it agrees with (U181).
    Check("install.extras", _check_install_extras),
    # Last, as the one network check, so a slow read holds up nothing (U159).
    Check("install.release", _check_release),
)

#: The keys this doctor answers, in run order. ``tests/test_cli_contract.py``
#: asserts every key a verb declares appears here, so an unwritten check fails
#: the build.
CHECK_KEYS: tuple[str, ...] = tuple(check.key for check in CHECKS)


def answer(check: Check, inputs: _Inputs) -> Finding:
    """One check's answer, with a check that raised turned into a FAIL.

    Applied to every check rather than inside each, so a check written later
    cannot take the whole report down. A ``CratekitError`` keeps its own cause,
    reason and remedy, since it refused rather than broke. Anything else is a
    FAIL, never INFO, because an unanswered question is not "nothing to do",
    and its remedy comes from ``cause.access_remedy`` so a permission problem is
    not called a defect.
    """
    try:
        return check.run(inputs)
    except CratekitError as exc:
        cause = exc.cause
        steps = "; ".join(cause.remediation.steps)
        return Finding(
            key=check.key,
            title=check.key,
            status=Status.FAIL,
            detail=cause.message + (f" ({steps})" if steps else ""),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
    except Exception as exc:  # noqa: BLE001 - see the docstring
        note = render.access_note(exc)
        return Finding(
            key=check.key,
            title=check.key,
            status=Status.FAIL,
            detail=(
                f"this check did not complete: {type(exc).__name__}: {exc}. The "
                f"answer is unknown rather than good, and the rest of the report "
                f"is below rather than discarded with it"
                + (f". {note}" if note else "")
            ),
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )


def run(cfg: config.Config | None = None, *, probes: Probes | None = None) -> Report:
    """Answer every check, always, and never raise.

    Every check answers on every run so the report can be diffed: one that
    cannot run says so as INFO, one that breaks is a FAIL through :func:`answer`.
    ``cfg`` is loaded here because reporting a missing configuration is
    doctor's first job on a broken install.
    """
    error: Exception | None = None
    if cfg is None:
        try:
            cfg = config.load()
        except config.ConfigError as exc:
            cfg, error = None, exc
    inputs = _Inputs(cfg, error, probes or Probes())
    return Report(tuple(answer(check, inputs) for check in CHECKS))


# ---------------------------------------------------------------------------
# crate doctor
# ---------------------------------------------------------------------------


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=doctor)


def failure_cause(report: Report, *, origin: str = "cli.doctor") -> Cause:
    """One cause carrying every failing check and its rendered fix.

    The steps let a consumer that reads only the cause learn which checks failed
    and what answers each. Public because the setup wizard raises the same
    refusal. A check that refused under its own reason leads with that reason,
    so its reserved exit code and slug survive; otherwise the reason is
    ``doctor-check-failed``, which maps to PRECONDITION.
    """
    steps = []
    for finding in report.failures:
        fix = render.remedy_text(finding.remedy) if finding.remedy is not None else None
        steps.append(f"{finding.key}: {finding.detail}" + (f" -> {fix}" if fix else ""))
    failing = [finding.key for finding in report.failures]
    refusal = next((f.cause for f in report.failures if f.cause is not None), None)
    if refusal is not None:
        return Cause(
            reason=refusal.reason,
            message=refusal.message,
            remediation=Remediation(
                remedy=refusal.remediation.remedy,
                steps=tuple(refusal.remediation.steps) + tuple(steps),
            ),
            scope=refusal.scope,
            retryable=refusal.retryable,
            origin=(origin,),
            detail={**dict(refusal.detail), "failing": failing},
        )
    return Cause(
        reason="doctor-check-failed",
        message=(
            f"{len(report.failures)} of {len(report.findings)} checks are failing"
        ),
        remediation=Remediation(steps=tuple(steps)),
        scope=Scope.RUN,
        retryable=True,
        origin=(origin,),
        detail={"failing": failing},
    )


def doctor(ctx: "Context") -> Envelope:
    report = run()
    schema = ctx.entry.output_schema or output.current_schema("diagnostic")
    if report.ok:
        return ctx.envelope(data=report.payload())
    cause = failure_cause(report)
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=schema,
        started=ctx.started,
        outcome=Outcome.FAILED,
        # Read off the cause: PRECONDITION for an ordinary failing report, or the
        # code a check's own refusal reserves.
        code=cause.code,
        data=report.payload(),
        cause=cause,
    )


# ---------------------------------------------------------------------------
# crate status
# ---------------------------------------------------------------------------


def build_status(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=status)


#: The key of ``crate status``'s one line for the open gates nobody will
#: answer (U170). Not under ``run.``, since it is many runs and not one.
OLD_GATES_KEY = "runs.old"


def _run_findings(
    older_than: timedelta | None = None, now: datetime | None = None
) -> list[Finding]:
    """Runs that stopped at a gate or are waiting on a person; :func:`_run_report`'s findings."""
    return _run_report(older_than, now)[0]


def _run_report(
    older_than: timedelta | None = None, now: datetime | None = None
) -> tuple[list[Finding], int]:
    """Runs that stopped at a gate or are waiting on a person, and how many were folded away.

    Read from the dispatcher's run records, the same state ``crate run show``
    addresses. Open gates idle past ``older_than`` that ``crate run retire``
    would retire, by :func:`gates.old_gate`, fold into one line (U170); every
    other run is listed. ``older_than`` None folds nothing.
    """
    found: list[Finding] = []
    old: list[gates.OldGate] = []
    moment = now or datetime.now(timezone.utc)
    try:
        records = sorted(gates.run_dir().glob("*.json"))
    except OSError:
        # A walk that refuses costs the report its run records, not the verb.
        # ``Path.glob`` swallows these errors today, but that is not a promise,
        # so the handler stays and ``tests/test_doctor.py`` exercises it.
        records = []
    for path in records:
        try:
            state = gates.load(path.stem)
        except CratekitError as exc:
            found.append(
                Finding(
                    key=f"run.{path.stem}",
                    title="run record",
                    status=Status.FAIL,
                    detail=exc.cause.message,
                    remedy=Remedy.REPORT_DEFECT,
                )
            )
            continue
        if state.open_gate is None and state.pending is None:
            continue
        if older_than is not None:
            aged = gates.old_gate(state, path, older_than=older_than, now=moment)
            if aged is not None and aged.retirable:
                old.append(aged)
                continue
        waiting = (
            f"open gate {state.open_gate}"
            if state.open_gate is not None
            else f"awaiting {state.pending.kind}"
        )
        found.append(
            Finding(
                key=f"run.{state.run_id}",
                title=state.verb,
                status=Status.INFO,
                detail=f"{waiting}, started {state.created}",
                remedy=Remedy.ANSWER_DECISION
                if state.open_gate is not None
                else Remedy.COMPLETE_PENDING_ACTION,
            )
        )
    if old and older_than is not None:
        found.append(_old_gates_line(old, older_than))
    return found, len(old)


def _old_gates_line(old: Sequence[gates.OldGate], older_than: timedelta) -> Finding:
    """The one line every retirable old gate is folded into, with the command (U170).

    The command is in ``detail`` because it carries the threshold, which a
    remedy token cannot.
    """
    days = older_than.days
    spans = sorted(one.idle_since[:10] for one in old)
    gates_word = "gate" if len(old) == 1 else "gates"
    days_word = "day" if days == 1 else "days"
    return Finding(
        key=OLD_GATES_KEY,
        title="old open gates",
        status=Status.INFO,
        detail=(
            f"{len(old)} open {gates_word} idle for more than {days} {days_word}, "
            f"from {spans[0]} to {spans[-1]}; crate run retire --older-than {days}d "
            f"answers each one abort after a confirm"
        ),
    )


def _source_findings(cfg: config.Config) -> list[Finding]:
    """Per-source sync state, from the session log and the watermark store.

    Each source's session state shows whether a resume would redo or skip work
    (R29), and its watermark is its last clean completion (U22). The watermark
    rows come from ``status_rows``, which derives the source set, so a new
    source cannot go unreported (P3).
    """
    from cratekit.sync import watermarks as sync_watermarks

    found: list[Finding] = []
    parsed, unreadable = session.scan_log(cfg)
    if session.log_unlisted(unreadable, cfg):
        # A log nobody could list is reported, never read as no source in
        # flight (R-1255).
        found.append(
            Finding(
                key="source.session-log",
                title="sources in the session log",
                status=Status.FAIL,
                detail=(
                    f"the session log directory {session.log_dir(cfg)} exists and "
                    f"cannot be listed by this account, so whether a source is "
                    f"refused or still in flight is unknown"
                ),
                remedy=Remedy.REPORT_DEFECT,
            )
        )
    for record in parsed:
        if record.terminal:
            continue
        for source, state in sorted(record.sources.items()):
            found.append(
                Finding(
                    key=f"source.{source}",
                    title=f"{source} in session {record.session_id}",
                    status=Status.FAIL
                    if state == str(session.SourceState.REFUSED)
                    else Status.INFO,
                    detail=f"{state} in workflow {record.workflow}",
                    remedy=Remedy.RESUME_JOB
                    if state == str(session.SourceState.REFUSED)
                    else None,
                )
            )
    try:
        rows = sync_watermarks.status_rows(cfg)
    except CratekitError as exc:
        found.append(
            Finding(
                key="source.watermarks",
                title="source watermarks",
                status=Status.FAIL,
                detail=exc.cause.message,
                remedy=exc.cause.remediation.remedy,
            )
        )
        return found
    for row in rows:
        found.append(
            Finding(
                key=f"source.{row['source_id']}.watermark",
                title=f"{row['source_id']} watermark",
                status=Status.INFO,
                detail=row["detail"],
            )
        )
    return found


def _tree_findings(cfg: config.Config) -> list[Finding]:
    """What medium owns each tree, and whether the registry can be read at all.

    An unreadable registry is a FAIL, never "no record", since no record reads
    as every tree still on the bridge and would send a byte write at a tree the
    database owns. This reports the record, not whether the database matches it.
    """
    try:
        found_registry = tree_registry.read(cfg)
    except CratekitError as exc:
        return [
            Finding(
                key="tree.registry",
                title="tree registry",
                status=Status.FAIL,
                detail=exc.cause.message,
                remedy=exc.cause.remediation.remedy,
            )
        ]
    return [
        Finding(
            key=f"tree.{record.tree_id}",
            title=f"tree {record.tree_id}",
            status=Status.INFO,
            detail=(
                f"{record.mode}, cutover {record.cutover_on or 'not recorded'}, "
                f"adopted root {record.root_id or 'none'}"
            ),
        )
        for record in found_registry.trees
    ]


def status(ctx: "Context") -> Envelope:
    cfg = config.load()
    runs, folded = _run_report(timedelta(days=cfg.reports.open_gate_stale_days))
    findings = runs + _source_findings(cfg) + _tree_findings(cfg)
    data = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            # Every open run, folded ones included.
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")) + folded,
            "old_gates": folded,
            "sources": sum(1 for f in findings if f.key.startswith("source.")),
            "trees": sum(1 for f in findings if f.key.startswith("tree.")),
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(data=data, outcome=Outcome.OK if findings else Outcome.NO_OP)


__all__ = [
    "BINARY_NAMES",
    "CHECKS",
    "CHECK_KEYS",
    "CREDENTIALS_BY_CHECK",
    "OFFERED_WHEN_SPENT",
    "Check",
    "Finding",
    "BUDGET_CHECK",
    "ISRC_CACHE_CHECK",
    "OPEN_GATES_CHECK",
    "Probes",
    "Report",
    "Status",
    "answer",
    "build",
    "build_status",
    "contract_members",
    "doctor",
    "failure_cause",
    "requires_check",
    "run",
    "satisfies",
    "status",
]
