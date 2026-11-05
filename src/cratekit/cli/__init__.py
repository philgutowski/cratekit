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
import dataclasses
import importlib
import shlex
import sys
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from cratekit import __version__
from cratekit.cli import gates, output, registry, render
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.cli.registry import Entry
from cratekit.core import config, profiles, provider_gate
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

    ``progress`` IS THE ONE EXCEPTION, and it is not output. A verb that runs
    for minutes before its envelope exists hands it a line saying which phase
    it is in and how far along (R-924). The dispatcher sets it to a writer on
    standard error in human output and leaves it None in JSON output, so the
    envelope is still the only thing on standard output and still the result,
    and a verb handed None does none of the work of measuring progress.
    """

    entry: Entry
    args: argparse.Namespace
    run: gates.RunState
    gate: gates.Gates
    started: str
    progress: Callable[[str], None] | None = None

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


def _positive_calls(text: str) -> int:
    """``--calls``: a positive whole number, refused by argparse otherwise (U193)."""
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"must be a positive whole number, found {text!r}")
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be a positive whole number, found {text!r}")
    return value


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
    parser.add_argument(
        "--calls",
        type=_positive_calls,
        default=None,
        metavar="N",
        help=(
            "the most calls to the streaming provider this one run may make, raising "
            "[provider] calls_per_command for this run only"
        ),
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


def _progress_to(stderr) -> Callable[[str], None]:
    """A verb's progress lines, one per call, on standard error.

    FLUSHED, because standard error is not line buffered everywhere and a
    progress line that sits in a buffer until the verb ends is the silence it
    exists to break.

    A LINE THAT CANNOT BE WRITTEN IS DROPPED. Progress is a hint and never the
    result, and it is written in the middle of paid work: a reader that closed
    standard error, ``2>&1 | head`` for one, would otherwise end a pass part
    way through its calls and lose the job those calls paid for.
    """

    def say(line: str) -> None:
        try:
            print(line, file=stderr, flush=True)
        except (OSError, ValueError):
            pass

    return say


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


#: The warning code every run that reached the streaming provider carries,
#: with its call count and how many answers were a rate limit (R-705). A
#: WARNING rather than a payload field, because every declared surface is
#: closed and the spend belongs to the run, not to any one verb's answer; and
#: because a heavy crawl is exactly the thing a person should see before it
#: becomes a block.
PROVIDER_SPEND = "provider-spend"

#: The warning code every run that looked an ISRC up carries (U206): how many
#: lookups a remembered answer settled and how many went to the provider. A
#: warning for the reason the spend is one, and beside it, so a rehearsal and
#: its live run can be read against each other.
ISRC_LOOKUPS = "isrc-lookups"


def _with_sibling_runs(envelope: Envelope, state: gates.RunState) -> Envelope:
    """The envelope of a run persisted at its gate, with every sibling run named (U186).

    At sitting 51 two sessions planned one database clear minutes apart and
    nothing said the other existed. So a verb declaring a database writing
    surface, at the moment its run is persisted at a gate, names each other run
    of the same verb with an open gate or an answer from the last twelve hours,
    as a warning a person reads and a code a session branches on.

    IT INFORMS AND REFUSES NOTHING: the exit code and the cause are the gate's,
    unchanged, and ``decision-stale`` on the write handle stays the only guard.
    A READING THAT BREAKS COSTS THE NAMES AND NEVER THE GATE, and says so. This
    runs inside the boundary's own handler, so anything it raised would replace
    the gate's envelope with a traceback; and a silent empty answer would read
    as "no other run", which is the absence this unit exists to end.
    """
    if not gates.writes_the_database(state.verb):
        return envelope
    try:
        found, unreadable = gates.siblings(state.verb, exclude=state.run_id)
        said = gates.sibling_warnings(found, unreadable, state.verb)
    except Exception as exc:  # noqa: BLE001 - see the docstring, the gate stays the gate
        said = [
            {
                "code": gates.SIBLING_RUN,
                "message": (
                    f"whether another run of {state.verb} holds or just answered a "
                    f"gate could not be read ({type(exc).__name__}: {exc})"
                ),
            }
        ]
    if not said:
        return envelope
    return dataclasses.replace(envelope, warnings=(*envelope.warnings, *said))


def _provider_spend() -> provider_gate.Spend:
    """What THIS process has spent so far, across every gate it built.

    Asked at the boundary rather than inside any verb, so the count covers
    every verb and every seam, and a verb that reaches the provider through a
    seam it does not know about is still reported. This process's own count
    and not the shared file's, because the file is written by every driver on
    the machine: a sweep another process was running would otherwise be
    reported as this run's calls. A job this verb drives runs in this process;
    a detached driver is its own invocation and reports its own.
    """
    return provider_gate.process_spend()


def _with_provider_spend(envelope: Envelope, before: provider_gate.Spend) -> Envelope:
    """The envelope with one spend line added when this run reached the provider.

    THE TWO IDENTITIES ARE NAMED APART (U205): how many calls went under the
    person's account session and how many under Cratekit's own app
    credentials, so a run whose catalogue lookups were meant to leave the
    account shows whether they did.
    """
    spent = _provider_spend().since(before)
    if spent.calls == 0:
        return envelope
    calls = "1 call" if spent.calls == 1 else f"{spent.calls} calls"
    limited = (
        "none answered with a rate limit"
        if spent.rate_limited == 0
        else f"{spent.rate_limited} answered with a rate limit"
    )
    app = "none" if spent.app_calls == 0 else str(spent.app_calls)
    lost = provider_gate.app_lost()
    why = (
        f". {' and '.join(lost)} {'is' if len(lost) == 1 else 'are'} recorded in this "
        f"installation and missing from the keychain, so the catalogue lookups went "
        f"to the account; record {'it' if len(lost) == 1 else 'them'} again with "
        f"crate login NAME --from-file PATH"
        if lost
        else ""
    )
    entry = {
        "code": PROVIDER_SPEND,
        "message": (
            f"{calls} to the streaming provider this run, {limited}; "
            f"{spent.account_calls} on the account and {app} under Cratekit's app "
            f"credentials{why}"
        ),
    }
    return dataclasses.replace(envelope, warnings=(*envelope.warnings, entry))


def _isrc_lookups() -> tuple[int, int]:
    """Lookups the ISRC cache settled and lookups asked of the provider, so far (U206).

    READ OFF THE MODULE ONLY WHEN SOMETHING LOADED IT, rather than imported
    here: the dispatcher imports nothing a verb does not need, and the counts
    move only inside that module, so a run that never loaded it looked
    nothing up. This process's own counts, for the reason the spend line gives.
    """
    module = sys.modules.get("cratekit.acquire.isrc_cache")
    if module is None:
        return (0, 0)
    done = module.process_lookups()
    return (done.remembered, done.asked)


def _with_isrc_lookups(envelope: Envelope, before: tuple[int, int]) -> Envelope:
    """The envelope with one line added when this run looked any ISRC up (U206)."""
    now = _isrc_lookups()
    remembered = max(0, now[0] - before[0])
    asked = max(0, now[1] - before[1])
    if remembered == 0 and asked == 0:
        return envelope
    lookups = "1 ISRC lookup" if remembered == 1 else f"{remembered} ISRC lookups"
    entry = {
        "code": ISRC_LOOKUPS,
        "message": f"{lookups} answered from the cache, {asked} asked of the streaming provider",
    }
    return dataclasses.replace(envelope, warnings=(*envelope.warnings, entry))


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


def _verb_argv(argv: Sequence[str], entry: Entry) -> tuple[str, ...] | None:
    """The verb's path and every argument after it, out of the whole command line (U168).

    The global options come before the verb, so the verb's own words start at
    the first place its path appears. None when it cannot be found, which a
    caller reads as a command line it cannot give back.
    """
    path = list(entry.path)
    tokens = list(argv)
    for index in range(len(tokens) - len(path) + 1):
        if tokens[index : index + len(path)] == path:
            return tuple(tokens[index:])
    return None


def dispatch(argv: Sequence[str], *, stderr) -> Envelope:
    """Parse and run one command line and answer its envelope, without writing it (U168).

    What ``run decide --continue`` calls to continue the verb that owns a run
    in this same process, so the one envelope the caller writes is that verb's.
    A command line argparse refuses is a defect here, since it is a recorded
    one given back.
    """
    parser = build_parser()
    try:
        args = parser.parse_args(list(argv))
    except SystemExit as exc:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=(
                    f"the recorded command line {' '.join(argv)!r} no longer parses "
                    f"(status {exc.code!r}), so the run cannot be continued from it"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli",),
            )
        ) from None
    entry = getattr(args, "_entry", None)
    if entry is None:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=f"the recorded command line {' '.join(argv)!r} names no verb",
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli",),
            )
        )
    return _dispatched(args, list(argv), entry, as_json=args.output == "json", stderr=stderr)


#: The warning a run carries when the call ceiling stopped it but the verb
#: caught the park and answered normally (U193).
CALL_CEILING = provider_gate.CEILING


def _without_calls(tokens: Sequence[str]) -> list[str]:
    """The global options with any ``--calls`` taken out, so it is given once."""
    kept: list[str] = []
    skip = False
    for token in tokens:
        if skip:
            skip = False
            continue
        if token == "--calls":
            skip = True
            continue
        if token.startswith("--calls="):
            continue
        kept.append(token)
    return kept


def continue_command(argv: Sequence[str], entry: Entry, cause: Cause) -> str:
    """The exact command that continues a run the call ceiling stopped (U193).

    A job it was driving is parked with its remaining items pending, and the
    job engine names the job on the cause, so the command resumes THAT job: a
    verb run again would queue a second one. Anything else is this command line
    again with ``--calls`` raised, the global options kept, since a run that
    stopped at a gate continues by the same words.
    """
    detail = cause.detail or {}
    higher = str(detail.get("higher") or 2 * int(detail.get("ceiling") or 1))
    job_id = detail.get("job_id")
    if job_id:
        return shlex.join(["crate", "--calls", higher, "job", "resume", str(job_id)])
    tokens = list(argv)
    verb = _verb_argv(tokens, entry)
    if verb is None:
        return shlex.join(["crate", "--calls", higher, *_without_calls(tokens)])
    lead = _without_calls(tokens[: len(tokens) - len(verb)])
    return shlex.join(["crate", *lead, "--calls", higher, *verb])


def _with_continue(cause: Cause, argv: Sequence[str], entry: Entry) -> Cause:
    """The ceiling's cause with its first step naming the exact command."""
    command = continue_command(argv, entry, cause)
    steps = (
        f"continue with a higher ceiling for one run: {command}",
        *cause.remediation.steps[1:],
    )
    return dataclasses.replace(
        cause,
        remediation=dataclasses.replace(cause.remediation, steps=steps),
        detail={**dict(cause.detail or {}), "continue": command},
    )


def _dispatched(
    args: argparse.Namespace, argv: Sequence[str], entry: Entry, *, as_json: bool, stderr
) -> Envelope:
    """Run one parsed verb inside one command's call ceiling scope (U193).

    The scope is opened HERE, around every verb, so a verb added later is under
    the ceiling without knowing about it. A run the ceiling stopped whose verb
    caught the park and answered normally carries a warning saying so, since a
    clean report over a run the ceiling cut short is a report over reads that
    were never made.
    """
    with provider_gate.command(getattr(args, "calls", None)) as scope:
        envelope = _dispatched_in_scope(args, argv, entry, as_json=as_json, stderr=stderr)
    stopped = scope.stopped
    reported = envelope.cause is not None and envelope.cause.reason == CALL_CEILING
    if stopped is not None and not reported:
        command = continue_command(argv, entry, stopped)
        entry_warning = {
            "code": CALL_CEILING,
            "message": (
                f"{stopped.message}; what this run reports after that point was not "
                f"read from the provider. Continue with: {command}"
            ),
        }
        envelope = dataclasses.replace(envelope, warnings=(*envelope.warnings, entry_warning))
    return envelope


def _dispatched_in_scope(
    args: argparse.Namespace, argv: Sequence[str], entry: Entry, *, as_json: bool, stderr
) -> Envelope:
    """Run one parsed verb and answer its envelope; every refusal is converted here."""
    started = output.timestamp()
    state: gates.RunState | None = None
    spent_before = _provider_spend()
    looked_before = _isrc_lookups()

    try:
        stub = getattr(args, "_stub", None)
        if stub is not None:
            raise CratekitError(_stub_cause(entry, stub))

        supplied = gates.parse_decision_flags(args.decision)
        state = _run_state_for(entry, args)
        # THE COMMAND LINE, ON A NEW RUN ONLY (U168): what ``run decide
        # --continue`` dispatches again. A continued run keeps its first one.
        if not args.run:
            state.argv = _verb_argv(argv, entry)
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
        if not as_json:
            context.progress = _progress_to(stderr)
        envelope = args._handler(context)
        gates.save(state)
    except CratekitError as exc:
        cause = exc.cause
        ceiling_stop = cause.reason == provider_gate.CEILING
        if ceiling_stop:
            cause = _with_continue(cause, argv, entry)
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
        # THE CALL CEILING IS A PARK TOO (U193), raised as ``Parked`` straight
        # out of a verb that drives no job. What the run did is kept, so it is
        # blocked at a line the person set and not failed.
        parked = isinstance(exc, JobBlocked) or ceiling_stop
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
        if state is not None and resumable:
            envelope = _with_sibling_runs(envelope, state)
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

    # AFTER EVERY BRANCH ABOVE, the refusals included: the sitting's failed
    # downloads spent calls into a live limit and nothing on the screen said so.
    envelope = _with_provider_spend(envelope, spent_before)
    envelope = _with_isrc_lookups(envelope, looked_before)
    return envelope


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

    as_json = args.output == "json"
    envelope = _dispatched(args, argv, entry, as_json=as_json, stderr=stderr)
    _emit(envelope, as_json=as_json, stdout=stdout, stderr=stderr)
    return int(envelope.exit_code)


if __name__ == "__main__":  # pragma: no cover - exercised by the console script
    raise SystemExit(main())
