"""``crate doctor`` and ``crate status``: the environment, checked before it is spent.

WHAT WAS WRONG. The source system has health checks, and they have exactly one
caller: an HTML template in a local web dashboard. No workflow consults them, so
nothing is ever a precondition to anything. A missing ``ffmpeg`` is discovered
part way through a download, after the identification calls have been paid for.
A dead provider session is discovered as "these tracks are missing". An unset
version pin is discovered by the writer refusing, one step before the write the
user was trying to make. Every one of those is knowable in advance, cheaply, and
none of it is asked.

So R3 is met here in two halves that have to arrive together:

* this module answers a named check and reports a fix per failure;
* ``cli/registry.py`` lets every verb DECLARE the checks it depends on, and
  ``tests/test_cli_contract.py`` asserts that anything which writes declares at
  least one, and that every declared key exists here.

The second half is the one the source system has no shape for at all.

THE CHECK SHAPE IS PORTED, WITH ONE SUBSTITUTION. The source returns
``{key, title, status, detail, fix}`` per check, with three statuses: ok, fail
and info. That shape is good and is kept, because it is already the ancestor of
this product's structured cause: it is the one place in that codebase that pairs
a failure with its exact remedy. The substitution is ``fix``, a sentence, for
``remedy``, a token the CLI renders (D2). A sentence is still allowed in
``detail`` for a fix that is not a command at all, because this IS the CLI layer
and rendering is what it is for.

WHAT IS ADDED, AND WHY EACH ONE.

* **The interpreter, before anything else.** KTD19 bounds the supported Python at
  both ends and the bound is declared once, in packaging metadata. It is READ
  from there rather than repeated here: a second copy is a copy that drifts, and
  the drift would be a check reporting green against a bound nobody enforces.
  It runs first because every other answer in this file is worthless if the
  interpreter is one the vendored tree has never run on.
* **The library volume, with unmounted told apart from moved.** ``core/preflight``
  already distinguishes five outcomes, and the whole reason it does is that a
  guard saying "the volume is wrong" sends the user to unplug a drive that was
  never the problem. Doctor reports which of the five it is, and both findings
  come from ONE probe rather than from two, so the mount and the identity can
  never disagree about the state they are describing.
* **External binaries, resolved before any spend.** Every installable binary is
  probed on every run, derived from ``core/binaries``' own table rather than
  listed here, so a binary added there is checked here the day it is added (P3).
* **The acquisition adapter, against the contract.** R9 says the point of the
  adapter boundary is that the downloader is replaceable. A configured
  alternative that does not satisfy the protocol is a substitution that fails at
  the first download rather than at configuration time, so the members are
  derived from the Protocol itself and checked on the configured class.
* **Credentials, per enabled module.** Presence only, never retrieval: reading a
  value on macOS raises an interactive authorization prompt, which in an
  unattended check means a hang rather than a report.
* **Backup age, per portion.** ``core/backup_facts`` answers per portion because
  the normal state of a library backed up without quitting rekordbox is "files
  current, database stale", and one aggregate number hides exactly that.

WHETHER A CHECK IS REQUIRED IS DERIVED, NOT DECIDED HERE. A check key is
required when some verb declaring it is available under the active profile.
That is what makes "a module enabled without its credential is reported" true by
construction: enabling ``identify`` makes ``intake.identify`` available, that
verb declares ``credential.recognition``, and the check turns from a note into a
failure with no edit to this file. The set is taken over EVERY registry entry
rather than only the landed ones, so the report does not change its mind about
what a profile needs as later units land.

WHY A FAILING DOCTOR DOES NOT DISCARD ITS REPORT. Every other refusal in the
product raises, and the dispatcher turns the cause into an envelope carrying an
empty diagnostic payload. That is right everywhere else and wrong here: the
checks ARE the answer, and a doctor that fails by throwing them away is useless
in exactly the case it exists for. So this module builds its own envelope, with
the full report in ``data`` and a structured cause beside it, and exits
``PRECONDITION``.

Layer note: CLI. It imports downward only, and it is the layer allowed to turn a
remediation token into words.
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
from cratekit.cli.doctor_credentials import (
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
    _check_taxonomy,
    _check_taxonomy_schema,
    _check_trash,
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
from cratekit.core import backup_facts, config, profiles, session, tree_registry
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, access_remedy
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def offered(key: str, membership: profiles.Membership) -> bool:
    """Whether setup offers ``key``'s credentials to this profile.

    When a verb it switches on declares the check, as before, and when one of
    the verbs :data:`OFFERED_WHEN_SPENT` names for it is switched on.
    """
    if requires_check(key, membership):
        return True
    spenders = OFFERED_WHEN_SPENT.get(key, ())
    return any(
        entry.name in spenders and entry.available_to(membership)
        for entry in registry.entries()
    )


@dataclass(frozen=True, slots=True)
class Check:
    """One named question and the function that answers it."""

    key: str
    run: Callable[[_Inputs], Finding]


def _bound(key: str, function: Callable[[str, _Inputs], Finding]) -> Check:
    """A check whose answer function serves a whole family of keys."""
    return Check(key=key, run=lambda inputs, _key=key: function(_key, inputs))


#: Every check, in the order they run, and the order IS part of the contract.
#: The interpreter comes first because every answer below it is worthless on an
#: interpreter the vendored tree has never run on. The three families are
#: expanded from their own declarations rather than typed out, so a credential, a
#: binary, or a backup portion added elsewhere is checked here without an edit.
CHECKS: tuple[Check, ...] = (
    Check("interpreter.version", _check_interpreter),
    Check("config.present", _check_config),
    Check("library.mounted", _check_library_mounted),
    Check("library.identity", _check_library_identity),
    Check("library.db_containment", _check_db_containment),
    Check("library.trash", _check_trash),
    Check("taxonomy.active", _check_taxonomy),
    # U132. After the copy is known to parse, which it reports on.
    Check("taxonomy.schema", _check_taxonomy_schema),
    Check("rekordbox.closed", _check_rekordbox_closed),
    Check("rekordbox.pins", _check_rekordbox_pins),
    # After the pins rather than beside the other library checks, because its
    # answer comes off an open the binding pin governs: a reader meets the pin
    # refusal first and this check's "could not be opened" second.
    Check("library.paths_resolved", _check_paths_resolved),
    Check("keychain.reachable", _check_keychain),
    *(_bound(key, _check_credential) for key in sorted(CREDENTIALS_BY_CHECK)),
    *(_bound(f"binary.{name}", _check_binary) for name in BINARY_NAMES),
    Check("adapter.contract", _check_adapter),
    *(
        _bound(f"backup.age.{portion}", _check_backup_portion)
        for portion in backup_facts.PORTIONS
    ),
    # U184. Right after the two ages, which are what it was minted over.
    Check("backup.acknowledgment", _check_backup_acknowledgment),
    # R-757. After the ages it qualifies and before the remote they all name.
    Check("backup.full_comparison", _check_full_comparison),
    Check("backup.full_check", _check_full_check),
    Check("backup.remote", _check_backup_remote),
    # U185. After the backup checks, since its warning is a comparison with
    # the database portion's age, and it names the same remedy they do.
    Check("deadca7.push", _check_deadca7_push),
    Check("session.unresolved", _check_unresolved_session),
    # U186. Beside the session check: both are this installation's own runs
    # left waiting, and a note here never fails the report.
    Check(OPEN_GATES_CHECK, _check_open_gates),
    # U206. Beside the open gates, another note about this installation's own
    # state that never fails the report.
    Check(ISRC_CACHE_CHECK, _check_isrc_cache),
    # U278. Beside the ISRC note, the other note about the provider, and like
    # it never a failure.
    Check(BUDGET_CHECK, _check_provider_budget),
    # U293. Beside the hour's budget, the other note about this installation's
    # provider calls, and like it never a failure.
    Check(NIGHT_CHECK, _check_night_pass),
    # R-235. Beside the session check because both report this product's own
    # library state, and after the taxonomy check, which it lists trees from.
    Check("tree.registry", _check_tree_registry),
    Check("repo.commit_hook", _check_commit_hook),
    # U181. Beside the release check, whose upgrade command it agrees with.
    Check("install.extras", _check_install_extras),
    # U159. Last, because it is the one check that reaches the network, and a
    # slow read should hold up nothing a person is waiting to see.
    Check("install.release", _check_release),
)

#: The keys this doctor can answer, in run order. ``tests/test_cli_contract.py``
#: asserts every key any verb declares appears here, so a verb declaring a check
#: nobody wrote fails the build rather than silently depending on nothing.
CHECK_KEYS: tuple[str, ...] = tuple(check.key for check in CHECKS)


def answer(check: Check, inputs: _Inputs) -> Finding:
    """One check's answer, and a THIRD outcome for the check that cannot give one.

    "Never raises" was a sentence in :func:`run`'s docstring and nothing made it
    true. Every check here reaches the outside world, and three of those reaches
    raise on an ordinary broken machine rather than returning a value:
    ``psutil`` refusing to enumerate processes, and ``Path.exists`` and
    ``Path.is_dir`` re-raising a permission error instead of answering False,
    which is what a library root under a directory this account cannot traverse
    produces. One of those took the ENTIRE report down, on precisely the machine
    the module's own opening argument says the report exists for: "a doctor that
    fails by throwing them away is useless in exactly the case it exists for".

    It is a FAIL rather than an INFO, and that is the load-bearing half. INFO is
    "worth knowing, nothing to do now", and a check that did not complete has not
    established that there is nothing to do. Green over an unanswered question is
    the defect this whole unit keeps being sent back for, and a rescue that
    reported one would be that defect wearing a handler.

    It is deliberately NOT per check. A handler inside each one is a handler that
    the next check written here will not have, and the property wanted is about
    every check rather than about the ones somebody remembered.

    AND IT ONLY RESCUES THE UNSTRUCTURED ONES. A ``CratekitError`` is not a check
    that broke, it is a check that REFUSED, and it already carries everything the
    rescue below invents: a declared reason, the reserved exit code that reason
    maps to, a remediation token and its steps. Flattening one produced a FAIL
    whose remedy was report-defect and whose detail read "this check did not
    complete", and the process left under PRECONDITION rather than under the
    reserved code, so a user with an unmounted drive was told to file a defect
    about it. Being not-per-check is exactly why that mattered: it is the shape
    every check written here inherits.

    AND THE UNSTRUCTURED LEG CLASSIFIES BEFORE IT BLAMES. This is the CHECKING
    path, and rescuing the structured refusals out of it left the remaining leg
    attaching report-defect to the exact condition the paragraph above names: a
    library root under a directory this account cannot traverse. One ``crate
    setup`` report then said "this is not a defect, grant this interpreter
    access" from the wizard's own note and "this is a defect; report it" three
    lines below from four checks at once, over one path and one permission.
    ``cause.access_remedy`` is the single decision, shared with the dispatcher,
    so a check nobody has guarded comes out right without a handler of its own.
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

    Every check answers on every run, including the ones that cannot be evaluated,
    because a report whose length depends on the machine is a report a consumer
    cannot diff. A check that cannot run says so as INFO and names why, and a
    check that BREAKS trying says so as FAIL through :func:`answer`.

    ``cfg`` is loaded here rather than required from the caller, because doctor's
    first job on a broken install is to report that there is no configuration,
    and a signature that demanded one could not do it.
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

    The steps exist so a consumer that reads only the cause, which is every
    consumer that got the failure across a process boundary, still learns which
    checks failed and what answers each of them. Turning a token into words
    happens here rather than lower down, which is the one place D2 allows it.

    Public because the wizard raises the same refusal for the same reason: a
    setup that wrote a valid config onto a machine that still cannot reach a
    write has not achieved what it was run for, and reporting OK would be a lie
    with the evidence sitting in the same envelope.

    A CHECK THAT REFUSED UNDER ITS OWN REASON KEEPS IT. ``doctor-check-failed``
    maps to PRECONDITION, which is the right answer for "some things this machine
    needs are not here" and the wrong one for a structured refusal that already
    reserved a code of its own: rewriting an unmounted library volume as "N
    checks are failing" drops the reserved 22 and the reason slug a caller
    branches on. The whole report still travels, as steps and in the envelope's
    data, so nothing is lost by leading with the refusal that named itself.
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
        # READ OFF THE CAUSE rather than written here. It is PRECONDITION for
        # every ordinary failing report, because that is what
        # ``doctor-check-failed`` maps to, and a check that refused under its own
        # reason leaves under the code that reason reserves.
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

    Read from the run records the dispatcher already persists, so this reports
    the same state ``crate run show`` addresses rather than a second notion of
    what an open run is.

    OPEN GATES IDLE PAST ``older_than`` ARE ONE LINE (U170): the count, the
    dates they span and the command that retires them, so a run of gates
    nobody will resume does not stand above the lines that matter. Only the
    gates that command would retire are folded, judged by the one predicate
    it reads, :func:`gates.old_gate`; an old gate it would keep, a record it
    cannot read and every newer gate are listed one by one as before.
    ``older_than`` None folds nothing.
    """
    found: list[Finding] = []
    old: list[gates.OldGate] = []
    moment = now or datetime.now(timezone.utc)
    try:
        records = sorted(gates.run_dir().glob("*.json"))
    except OSError:
        # THE TRIGGER IS UNOBSERVABLE AND THE CONTRACT IS NOT. Measured on this
        # interpreter, ``Path.glob`` swallows ``PermissionError`` inside its own
        # scandir walk and answers with an empty result for a directory that is a
        # plain file, so neither an unreadable state root nor a run directory
        # somebody replaced with a file reaches here through a real filesystem.
        # It is kept because the swallowing is an implementation detail of the
        # standard library rather than a documented promise, and losing the whole
        # status verb to a future change of mind would be worse than a handler
        # that never fires.
        #
        # What that argument does NOT excuse is leaving the promise unwritten,
        # which is how it sat as a rescue nothing exercised. The promise is that
        # a walk which refuses costs the report its run records rather than the
        # verb, and ``tests/test_doctor.py`` states it at the seam by handing
        # this a run directory that raises.
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
    remedy token cannot, and this is the layer that renders.
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

    R29 makes the destructive boundary one source per run, committed and captured
    independently, and the session record carries a state per source for exactly
    that reason: without it a resume either redoes committed work or skips
    uncommitted work and nothing outside can tell which. U22's watermark store
    is the other half: each source's last clean completion, reported rather than
    guessed. The rows come from ``cratekit.sync.watermarks.status_rows``, which
    derives the source set, so a source added there cannot go unreported (P3).
    """
    from cratekit.sync import watermarks as sync_watermarks

    found: list[Finding] = []
    parsed, unreadable = session.scan_log(cfg)
    if session.log_unlisted(unreadable, cfg):
        # A LOG NOBODY COULD LIST IS SAID, not read as no source in flight
        # (R-1255, review round one); the reporting reader would refuse the
        # whole status, which reports runs and trees the log does not hold.
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

    An unreadable registry is its own answer and is never collapsed into "no
    record": no record reads as "every tree is still on the bridge", which would
    send a byte write at a tree the database already owns.

    Whether a tree's declared membership actually MATCHES the database is a
    different question, it needs the database open, and the verb that answers it
    lands with the convergence check. What is reported here is the record.
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
            # EVERY open run, the folded ones included: folding is how they
            # are shown, never whether they are counted.
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
