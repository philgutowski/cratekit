"""The ``crate`` entry point: one shell, one dispatcher, one conversion to a status.

R2 replaces thirty console scripts with one verb. That much is packaging. What
this file actually owns is narrower and more load-bearing: it is the ONLY place
in the package where a failure becomes a process exit status, and the only place
where a remediation token becomes something a person reads.

Four properties, each answering a defect in the source system:

1. **A parser is built without importing a feature module.** The registry is
   plain data; a module is imported only when its subcommand is being built, and
   an import that fails because an EXTRA is missing becomes a stub subcommand
   rather than an exception. So ``crate --help`` works with every heavy extra
   uninstalled (KTD7). An import that fails for any other reason propagates,
   because telling a user to install an extra when the real problem is a defect
   in our own module is both wrong and unfixable by them.

2. **Every verb returns an envelope, and the envelope's exit code is the process
   status.** In the source, the two largest entry points always exit zero
   because their ``main`` returns ``None``; any automation reading their status
   is reading a constant.

3. **``SystemExit`` is caught here on purpose.** It is a ``BaseException``, so
   ``except Exception`` does not see it. That exact gap is live in the source: an
   argument-parsing failure inside a called writer escapes its handler and
   surfaces as exit 2 from the orchestrator, where 2 is documented as lock
   contention. Catching it at the boundary is what keeps 2 meaning only what
   argparse means by it.

4. **Standard input is never read.** Not by a guarded prompt, not through an
   injected input function. A gate that has no answer exits with a documented
   code and leaves the run resumable, which is what makes the same decision
   answerable from a different process in a later session (R33).
"""

from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from cratekit import __version__
from cratekit.cli import gates, output, registry, render
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.cli.registry import Entry
from cratekit.core import config, profiles
from cratekit.core.cause import (
    Cause,
    CratekitError,
    JobBlocked,
    JobCancelled,
    Outcome,
    Remediation,
    Scope,
    access_refusal,
    classified,
)
from cratekit.core.exit_codes import ExitCode, Remedy


@dataclass
class Context:
    """Everything a verb is handed, and the only way it produces a result.

    A verb never prints, never exits, and never reads input. It returns an
    envelope. That is what lets the conformance suite drive every verb the same
    way and assert the same properties about each of them.
    """

    entry: Entry
    args: argparse.Namespace
    run: gates.RunState
    gate: gates.Gates
    started: str

    def envelope(
        self,
        *,
        data: Mapping[str, Any],
        outcome: Outcome = Outcome.OK,
        code: ExitCode = ExitCode.OK,
        schema: str | None = None,
        pending: PendingHumanAction | None = None,
        warnings: Sequence[Mapping[str, str]] = (),
        resumable: bool = False,
    ) -> Envelope:
        return output.build(
            verb=self.entry.name,
            run_id=self.run.run_id,
            schema=schema or self.entry.output_schema or output.current_schema("diagnostic"),
            started=self.started,
            outcome=outcome,
            code=code,
            data=data,
            pending=pending,
            warnings=warnings,
            resumable=resumable,
        )

    def run_job(self, store, job):
        """Run one queued job's items here, in this process.

        THE ONLY ROUTE A VERB HAS TO THE DRIVER, and it is a method rather than an
        import for a reason the layering guard enforces. A verb module is
        modules-ranked and :mod:`cratekit.cli.handlers` is CLI-ranked, so a verb
        that imported it directly would be reaching upward, which
        ``tests/test_layering.py`` refuses whether the import is at module scope or
        inside the function body. ``Context`` is already the one object every verb
        holds, so the driver arrives the same way the envelope does.

        Returns the ``cratekit.core.jobs.DriveResult`` and the drift warnings the
        verb should put on its envelope, together, so a verb never has to spell
        the drift wording itself. EXCEPT when every attempted item failed: the
        engine records the job as failed and raises there, which is the common
        failure path for a job with one item.

        THE IMPORT IS INSIDE THE METHOD and it is not a laziness preference. This
        package's ``__init__`` is imported by ``cratekit.core.jobs`` for the output
        envelope, and ``handlers`` imports ``cratekit.core.jobs``, so a
        module-scope import here is a cycle that leaves ``core.jobs`` half built
        for anything that imports it first. A worker script is exactly that.
        """
        from cratekit.cli import handlers

        result = handlers.run_job(store, job)
        return result, handlers.drift_warnings(result.drifted)


Handler = Callable[[Context], Envelope]


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _membership() -> profiles.Membership:
    """Which modules are on, tolerating an unconfigured machine.

    ``crate --help`` has to work before setup has ever run, so a missing or
    unreadable config resolves to the full preset rather than raising. Showing a
    verb that a later profile turns off is a smaller failure than a help screen
    that crashes on a fresh install, which is the one moment a new user has no
    way to diagnose anything.

    AND "UNREADABLE" WAS A CLAIM THIS FUNCTION DID NOT KEEP. ``config.load``
    stats the file before it reads it, and a stat under a directory this account
    cannot traverse raises ``PermissionError`` rather than any ``ConfigError``,
    so the paragraph above was true of a corrupt file and false of an unreadable
    one. This call sits OUTSIDE the dispatcher's try, in the parser construction
    every invocation runs first, so the result was a traceback out of ``crate
    --help`` on a machine whose configuration directory the operating system will
    not open. The verbs that actually need the configuration still meet the same
    refusal and report it; what may not happen is the help screen dying of it.
    """
    try:
        loaded = config.load()
    except (config.ConfigError, OSError):
        return profiles.resolve("full")
    try:
        return profiles.resolve(loaded.profile.name, dict(loaded.modules.explicit))
    except (profiles.UnknownProfile, profiles.UnknownModule):
        return profiles.resolve("full")


def _is_missing_extra(exc: ImportError, entry: Entry) -> bool:
    """True only when the failed import names one of the entry's extras modules.

    The gate is the whole point. A bare ``except ImportError`` turns every typo
    in one of our own modules into "install the analysis extra", which sends the
    user to fix something that was never broken and leaves the real defect
    invisible.
    """
    missing = (getattr(exc, "name", "") or "").split(".")[0]
    return bool(missing) and missing in entry.extras_modules


def _stub_cause(entry: Entry, exc: ImportError) -> Cause:
    return Cause(
        reason="module-extras-missing",
        message=(
            f"{entry.name} needs the {entry.extras!r} extra, and the dependency "
            f"{getattr(exc, 'name', 'it needs')!r} is not installed"
        ),
        remediation=Remediation(remedy=Remedy.INSTALL_MODULE_EXTRA),
        scope=Scope.RUN,
        origin=("cli.registry",),
        detail={
            "entry": entry.name,
            "extras": entry.extras,
            "install": render.install_command(entry),
        },
    )


def _group_parser(
    root: Any, groups: dict[tuple[str, ...], Any], path: tuple[str, ...]
) -> Any:
    """Return the subparser collection for a dotted path, creating it as needed."""
    if path in groups:
        return groups[path]
    parent = root if len(path) == 1 else _group_parser(root, groups, path[:-1])
    parser = parent.add_parser(path[-1], help=f"{path[-1]} commands")
    groups[path] = parser.add_subparsers(dest=f"_group_{'_'.join(path)}", metavar="<command>")
    return groups[path]


def build_parser(
    entries: Sequence[Entry] | None = None,
    *,
    membership: profiles.Membership | None = None,
    importer: Callable[[str], Any] = importlib.import_module,
) -> argparse.ArgumentParser:
    """Assemble the whole command tree without importing a disabled module.

    ``importer`` is injected so the conformance suite can drive the missing-extra
    path without uninstalling anything, and so a fake registry can be exercised
    against the real construction logic rather than against a copy of it.
    """
    parser = argparse.ArgumentParser(
        prog="crate",
        description="Acquisition and curation for rekordbox libraries.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--output",
        choices=("human", "json"),
        default="human",
        help="human rendering (default) or one JSON envelope on standard output",
    )
    parser.add_argument(
        "-d",
        "--decision",
        action="append",
        default=[],
        metavar="GATE=OPTION",
        help="answer a named gate; repeatable",
    )
    parser.add_argument(
        "--run",
        metavar="RUN_ID",
        help="continue a run that stopped at a gate, rather than starting a new one",
    )
    root = parser.add_subparsers(dest="_verb", metavar="<command>")

    groups: dict[tuple[str, ...], Any] = {}
    resolved = membership if membership is not None else _membership()

    for entry in entries if entries is not None else registry.landed_entries():
        if not entry.available_to(resolved):
            continue
        path = entry.path
        target = root if len(path) == 1 else _group_parser(root, groups, path[:-1])
        try:
            module = importer(entry.module)
        except ImportError as exc:
            if not _is_missing_extra(exc, entry):
                raise
            stub = target.add_parser(
                path[-1],
                help=f"{entry.summary}  (requires the {entry.extras!r} extra)",
            )
            stub.set_defaults(_entry=entry, _stub=exc, _handler=None)
            continue
        sub = target.add_parser(path[-1], help=entry.summary)
        sub.set_defaults(_entry=entry, _stub=None)
        getattr(module, entry.builder)(sub, entry)
    return parser


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def _drive_argv(envelope: Envelope) -> list[str] | None:
    """The command line that drives the job this invocation just queued, or None.

    HUMAN MODE ONLY, AND NEVER INTO THE ENVELOPE. The job is continued by its own
    verb's command rebuilt from the frozen payload, which is in the queue and not
    in the payload, and putting it there would change every consumer's json. So
    it is read back here, where the words are about to be written.

    ONLY FOR THE VERB THAT QUEUED IT. ``job resume`` answers with a queued job
    too, after it has already spawned the child driving it, and a second drive
    command under that one would invite two drivers onto one job. The job's own
    handler key names its verb, so the check is that it names this one.

    A LOOKUP THAT FAILS IS NOT A FAILED VERB, AND IT NAMES NO COMMAND. This runs
    in ``_emit``, outside the boundary that converts exceptions, after the job is
    queued, so anything it raises would be a traceback over a success. And no
    fallback command is named, because every one on offer, ``job resume``
    included, reads the same row through the same builder and refuses for the
    same reason. The job line still names the identifier.
    """
    data = envelope.data
    if not envelope.schema.startswith("job_state/") or data.get("state") != "queued":
        return None
    job_id = data.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return None
    from cratekit.cli import jobs as cli_jobs
    from cratekit.core import jobs

    try:
        with jobs.open_store() as store:
            job = jobs.get(store, job_id)
        if registry.by_handler_key(job.handler_key).name != envelope.verb:
            return None
        return cli_jobs.argv_for(job)
    except Exception:  # noqa: BLE001 - see the docstring, a success stays a success
        return None


def _emit(envelope: Envelope, *, as_json: bool, stdout, stderr) -> None:
    """Write the result. In JSON mode stdout carries the envelope and NOTHING else.

    Human text goes to standard error in JSON mode rather than being suppressed,
    so a person watching a scripted run still sees what happened while the
    consumer parsing stdout gets exactly one object.
    """
    if as_json:
        print(envelope.to_text(), file=stdout)
        if envelope.exit_code is not ExitCode.OK:
            print(render.render(envelope), end="", file=stderr)
        return
    stream = stdout if envelope.exit_code is ExitCode.OK else stderr
    print(render.render(envelope, drive=_drive_argv(envelope)), end="", file=stream)
    if envelope.cause is not None and envelope.cause.reason == "decision-required":
        print(render.render_gate(envelope.cause), end="", file=stderr)


def _run_state_for(entry: Entry, args: argparse.Namespace) -> gates.RunState:
    if args.run:
        state = gates.load(args.run)
        # A run record belongs to the verb that created it. Answering a gate on
        # one run and then continuing a different verb under that identifier
        # would apply a decision to a question nobody asked.
        if state.verb != entry.name:
            raise CratekitError(
                Cause(
                    reason="decision-unknown-gate",
                    message=f"run {state.run_id} belongs to {state.verb}, not to {entry.name}",
                    remediation=Remediation(remedy=Remedy.ANSWER_DECISION),
                    origin=("cli",),
                    detail={"run_id": state.run_id, "verb": state.verb},
                )
            )
        return state
    return gates.new_run(entry)


def _unhandled_cause(exc: BaseException) -> Cause:
    """The cause for anything that reached the boundary unconverted.

    THIS IS THE BLANKET, NOT THE CLASSIFICATION. It covers exactly what nobody
    caught, which was the mistake the round before this one made: the same rule
    was put here and in doctor's check runner on the stated property that "a site
    nobody has converted now comes out right", while eighteen of the nineteen
    sites in the package ARE converted and never reach either blanket. The
    decision now lives in ``cause.classified``, at the constructor every
    structured refusal passes through, and this function asks the SAME question
    of the unstructured remainder.

    The remainder is not small. ``Path.exists`` re raises under EPERM instead of
    answering False, so every ordinary looking filesystem question in the package
    is a site nobody has guarded, and this program keeps its own state in SQLite,
    whose refusals are not ``OSError`` at all.

    Everything else keeps ``internal-error``, which is the honest answer for a
    failure this program did not anticipate, and keeps ``report-defect`` with it.
    A kernel refusal carrying no path at all, which a bind to a privileged port
    and ``os.setuid`` both produce, is part of that remainder ON PURPOSE: there
    is nothing for the user to grant access TO, so claiming a path would be a
    confident wrong answer rather than a missed one.
    """
    refusal = access_refusal(exc)
    if refusal is not None:
        return Cause(
            reason=refusal.reason,
            message=f"{type(exc).__name__}: {exc}. {render.access_note(exc)}",
            remediation=Remediation(remedy=refusal.remedy),
            origin=("cli",),
            detail={"path": refusal.path, "access": str(refusal.kind)},
        )
    return Cause(
        reason="internal-error",
        message=f"{type(exc).__name__}: {exc}",
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        origin=("cli",),
    )


def main(argv: list[str] | None = None) -> int:
    """Parse, dispatch, and return the process status.

    The console-script wrapper turns the return value into the exit status, so
    this returning an ``ExitCode`` is what gives every verb a real status. It
    returns rather than exiting: a caller inside a test, and the job engine
    reading a child's result, both get an integer instead of an exception.
    """
    return run(sys.argv[1:] if argv is None else argv, stdout=sys.stdout, stderr=sys.stderr)


def run(argv: list[str], *, stdout, stderr) -> int:
    """The dispatcher, with its streams injected so a test drives the real path."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse owns status 2, and this is the boundary that keeps it owning
        # it. Its --help and --version paths exit 0 and pass straight through.
        return int(exc.code or 0)

    entry = getattr(args, "_entry", None)
    if entry is None:
        parser.print_help(file=stdout)
        return int(ExitCode.OK)

    started = output.timestamp()
    as_json = args.output == "json"
    state: gates.RunState | None = None

    try:
        stub = getattr(args, "_stub", None)
        if stub is not None:
            raise CratekitError(_stub_cause(entry, stub))

        supplied = gates.parse_decision_flags(args.decision)
        state = _run_state_for(entry, args)
        blocked = gates.blocked_by(state, entry.name)
        if blocked is not None:
            raise CratekitError(blocked)

        context = Context(
            entry=entry,
            args=args,
            run=state,
            gate=gates.Gates(state=state, supplied=supplied),
            started=started,
        )
        envelope = args._handler(context)
        gates.save(state)
    except CratekitError as exc:
        cause = exc.cause
        # A PARKED JOB IS BLOCKED TOO, AND IT IS NOT RESUMABLE IN THIS FIELD'S
        # SENSE (R-290). ``resumable`` names the GATE RUN: it tells a caller that
        # ``crate run`` can continue this run id, and it is what saves the run
        # state below. A parked job continues through its own verb with the job
        # id, never through the run, so setting it here would send a wrapper to a
        # command that cannot advance the work. The outcome carries the block.
        #
        # ``and not parked`` IS WHAT MAKES THAT TRUE. The flag came off the
        # cause's code alone, and ``jobs.transition`` names a missing
        # acknowledgment among the reasons to park, which is a gate code. The
        # comment above was a claim about every worker until this enforced it.
        parked = isinstance(exc, JobBlocked)
        resumable = cause.code in gates.GATE_CODES and not parked
        if state is not None and resumable:
            gates.save(state)
        if resumable or parked:
            outcome = Outcome.BLOCKED
        elif isinstance(exc, JobCancelled):
            outcome = Outcome.CANCELLED
        else:
            outcome = Outcome.FAILED
        envelope = output.from_cause(
            verb=entry.name,
            run_id=state.run_id if state is not None else output.new_run_id(),
            started=started,
            cause=cause,
            resumable=resumable,
            outcome=outcome,
        )
    except config.ConfigError as exc:
        # U2 already models configuration failures as five types with five
        # remediation TOKENS. Converting here rather than in each verb means a
        # verb that simply calls ``config.load()`` still refuses with the right
        # code and the right remedy, instead of surfacing as an internal defect.
        #
        # THROUGH THE CLASSIFICATION, because a config file this account cannot
        # read is not a config file to repair. "Repair or recreate it" over a
        # document that is byte for byte intact sends a user to rewrite work they
        # still have, and an untraversable PARENT fails the same way without
        # establishing that the file is there at all. ``ConfigError`` is not a
        # ``CratekitError``, so the constructor's own correction never sees it;
        # this is the one hop where it can.
        envelope = output.from_cause(
            verb=entry.name,
            run_id=state.run_id if state is not None else output.new_run_id(),
            started=started,
            cause=classified(
                Cause(
                    reason="config-unusable",
                    message=str(exc),
                    remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                    origin=("cli",),
                    detail={"kind": type(exc).__name__},
                ),
                exc,
            ),
        )
    except SystemExit as exc:
        # A verb, or something it called, tried to exit the process. Convert it
        # rather than letting it through: an escaped SystemExit(2) is how the
        # source system's three meanings of code 2 collide inside one process.
        envelope = output.from_cause(
            verb=entry.name,
            run_id=state.run_id if state is not None else output.new_run_id(),
            started=started,
            cause=Cause(
                reason="internal-error",
                message=f"a verb exited the process directly with status {exc.code!r}",
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli",),
            ),
        )
    except Exception as exc:  # noqa: BLE001 - the boundary converts everything
        envelope = output.from_cause(
            verb=entry.name,
            run_id=state.run_id if state is not None else output.new_run_id(),
            started=started,
            cause=_unhandled_cause(exc),
        )

    _emit(envelope, as_json=as_json, stdout=stdout, stderr=stderr)
    return int(envelope.exit_code)


if __name__ == "__main__":  # pragma: no cover - exercised by the console script
    raise SystemExit(main())
