"""The ``crate`` entry point: one parser, one dispatcher, one conversion to a status.

This is the only place a failure becomes a process exit status and a
remediation token becomes words. A verb's module is imported only when
argparse selects it (U248), and a missing extra makes a stub rather than an
exception, so ``crate --help`` works with every extra uninstalled (KTD7); any
other import failure propagates, for its own verb only. Every verb returns an
envelope whose exit code is the status, ``SystemExit`` is caught at the
boundary so 2 keeps argparse's meaning, and standard input is never read: an
unanswered gate exits with a code and leaves the run resumable (R33).
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
from cratekit.core import config, processes, profiles, provider_gate
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

    A verb never prints, exits or reads input; it returns an envelope, so the
    conformance suite drives every verb alike. ``progress`` is a standard error
    writer in human output and None in JSON output, for a long verb's phase
    lines (R-924); it is never the result.
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

        A verb's only route to the driver, a method because a verb importing
        :mod:`cratekit.cli.handlers` would reach upward, which the layering
        guard refuses. Returns the ``DriveResult`` and the warnings for the
        envelope; when every attempted item failed the engine raises instead.
        The import is inside the method because a module scope one is a cycle
        through ``cratekit.core.jobs``.
        """
        from cratekit.cli import handlers

        result = handlers.run_job(store, job)
        return result, (*handlers.drift_warnings(result.drifted), *result.warnings)


Handler = Callable[[Context], Envelope]


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _membership() -> profiles.Membership:
    """Which modules are on, tolerating an unconfigured machine.

    ``crate --help`` must work before setup has run, so a missing, corrupt or
    unreadable config, ``OSError`` included, resolves to the full preset. This
    runs outside the dispatcher's try; the verbs that need the config still
    meet the refusal and report it.
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

    Otherwise a typo in our own module would read as "install the extra" and
    hide the real defect.
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


def _stub_help(entry: Entry) -> str:
    """The listing line of a verb whose extra is missing."""
    return f"{entry.summary}  (requires the {entry.extras!r} extra)"


class _Unbuilt:
    """One verb's subparser, made from registry data, whose module is not imported yet (U248).

    ``build`` does what the eager loop does, for the one verb argparse
    selected, on the subparser already listed under its name. ``listed`` is
    the pseudo action holding the listing line a stub replaces.
    """

    __slots__ = ("entry", "parser", "listed", "importer", "built", "asked")

    def __init__(
        self,
        entry: Entry,
        parser: argparse.ArgumentParser,
        listed: argparse.Action,
        importer: Callable[[str], Any],
    ) -> None:
        self.entry = entry
        self.parser = parser
        self.listed = listed
        self.importer = importer
        self.built = False
        self.asked = False

    def build(self) -> None:
        """Import the verb's module and run its builder, or make it the stub.

        An import failing for any reason but a missing extra propagates, so our
        own defect fails loudly. An ``ArgumentError`` leaves as a
        ``RuntimeError``, since inside argparse's parse it would read as the
        user's mistake. The verb counts as built only once its builder returned.
        """
        if self.built:
            return
        try:
            try:
                module = self.importer(self.entry.module)
            except ImportError as exc:
                if not _is_missing_extra(exc, self.entry):
                    raise
                self._stub(exc)
                return
            self.parser.set_defaults(_entry=self.entry, _stub=None)
            getattr(module, self.entry.builder)(self.parser, self.entry)
        except argparse.ArgumentError as exc:
            raise RuntimeError(
                f"building {self.entry.name} from {self.entry.module} is a defect: {exc}"
            ) from exc
        self.built = True

    def ask_for_listing(self) -> None:
        """Settle the listing line, importing only when the line could differ.

        Only a verb declaring extras can be a stub, so only it is imported, and
        only when a help screen lists it. Any other failure keeps the plain
        line, since its verb fails loudly when run. Asked once, because
        argparse walks the listing twice per help screen.
        """
        if self.built or self.asked or not self.entry.extras_modules:
            return
        self.asked = True
        try:
            self.importer(self.entry.module)
        except ImportError as exc:
            if _is_missing_extra(exc, self.entry):
                self._stub(exc)
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            pass

    def _stub(self, exc: ImportError) -> None:
        self.built = True
        self.listed.help = _stub_help(self.entry)
        self.parser.set_defaults(_entry=self.entry, _stub=exc, _handler=None)


class _LazyChoices(argparse._SubParsersAction):
    """argparse's own subcommand action, building a verb only when it is chosen (U248).

    argparse still decides which word is the verb, so nothing here reads the
    command line itself.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.unbuilt: dict[str, _Unbuilt] = {}

    def __call__(self, parser, namespace, values, option_string=None):  # noqa: ANN001
        waiting = self.unbuilt.get(values[0])
        if waiting is not None:
            waiting.build()
        super().__call__(parser, namespace, values, option_string)

    def _get_subactions(self):  # noqa: ANN202 - argparse's own private hook
        for waiting in self.unbuilt.values():
            waiting.ask_for_listing()
        return super()._get_subactions()


def _group_parser(
    root: Any,
    groups: dict[tuple[str, ...], Any],
    path: tuple[str, ...],
    choices: type[argparse.Action] = argparse._SubParsersAction,
) -> Any:
    """Return the subparser collection for a dotted path, creating it as needed."""
    if path in groups:
        return groups[path]
    parent = root if len(path) == 1 else _group_parser(root, groups, path[:-1], choices)
    parser = parent.add_parser(path[-1], help=f"{path[-1]} commands")
    groups[path] = parser.add_subparsers(
        dest=f"_group_{'_'.join(path)}", metavar="<command>", action=choices
    )
    return groups[path]


def build_parser(
    entries: Sequence[Entry] | None = None,
    *,
    membership: profiles.Membership | None = None,
    importer: Callable[[str], Any] = importlib.import_module,
    eager: bool = False,
) -> argparse.ArgumentParser:
    """Assemble the whole command tree without importing a disabled module.

    ``importer`` is injected so the suite drives the missing extra path without
    uninstalling anything. Lazy by default (U248): a verb's module is imported
    when argparse selects it. ``eager=True`` imports every verb, for a caller
    that walks each verb's arguments and as the suite's parity check.
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
    parser.add_argument(
        "--calls-per-hour",
        dest="calls_per_hour",
        type=_positive_calls,
        default=None,
        metavar="N",
        help=(
            "the most calls each identity may make to the streaming provider in an "
            "hour, counted across every command, raising [provider] calls_per_hour "
            "for this run only"
        ),
    )
    choices = argparse._SubParsersAction if eager else _LazyChoices
    root = parser.add_subparsers(dest="_verb", metavar="<command>", action=choices)

    groups: dict[tuple[str, ...], Any] = {}
    resolved = membership if membership is not None else _membership()

    for entry in entries if entries is not None else registry.landed_entries():
        if not entry.available_to(resolved):
            continue
        path = entry.path
        target = root if len(path) == 1 else _group_parser(root, groups, path[:-1], choices)
        if not eager:
            sub = target.add_parser(path[-1], help=entry.summary)
            target.unbuilt[path[-1]] = _Unbuilt(entry, sub, target._choices_actions[-1], importer)
            continue
        try:
            module = importer(entry.module)
        except ImportError as exc:
            if not _is_missing_extra(exc, entry):
                raise
            stub = target.add_parser(path[-1], help=_stub_help(entry))
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

    Human output only, never in the envelope, whose json would change. Only for
    the verb that queued it, since ``job resume`` has already spawned a driver.
    A failed lookup names no command and raises nothing, because this runs
    outside the boundary, after a success.
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

    Human text goes to standard error in JSON mode, so a person still sees it.
    """
    if as_json:
        print(envelope.to_text(), file=stdout)
        if envelope.exit_code is not ExitCode.OK:
            print(render.render(envelope), end="", file=stderr)
        return
    stream = stdout if envelope.exit_code is ExitCode.OK else stderr
    print(render.render(envelope, drive=_drive_argv(envelope)), end="", file=stream)
    if envelope.cause is not None and render.is_gate_screen(envelope.cause):
        print(render.render_gate(envelope.cause), end="", file=stderr)


def _progress_to(stderr) -> Callable[[str], None]:
    """A verb's progress lines, one per call, on standard error.

    Flushed, since standard error is not line buffered everywhere. A line that
    cannot be written is dropped, so a closed reader never ends paid work.
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
        # A run belongs to the verb that made it, or a decision would answer a
        # question nobody asked.
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


#: The warning every run that reached the streaming provider carries, with its
#: calls and rate limits (R-705). A warning, because the spend belongs to the
#: run and not to any verb's payload.
PROVIDER_SPEND = "provider-spend"

#: The warning every run that looked an ISRC up carries (U206): lookups the
#: cache settled and lookups asked of the provider.
ISRC_LOOKUPS = "isrc-lookups"


def _with_sibling_runs(envelope: Envelope, state: gates.RunState) -> Envelope:
    """The envelope of a run persisted at its gate, with every sibling run named (U186).

    Only for a database writing verb: each other run of it with an open gate or
    an answer from the last twelve hours is named as a warning. It refuses
    nothing. A reading that breaks says so rather than raising, since this runs
    inside the boundary's handler, or reading as "no other run".
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

    Asked at the boundary so every verb and seam is counted. This process's
    count, not the shared file's, which every driver on the machine writes.
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


def _unstored() -> int:
    """How many store failures a login in this process has met so far (R-1694).

    READ OFF THE MODULE ONLY WHEN SOMETHING LOADED IT, as the ISRC count is:
    a run that never loaded the provider session never logged in.
    """
    module = sys.modules.get("cratekit.acquire.provider_session")
    return 0 if module is None else len(module.unstored())


def _with_unstored(envelope: Envelope, before: int) -> Envelope:
    """The envelope with one line added when this run's login refreshed a
    session the keychain could not take (R-1694).

    The login went on, so the verb's own answer stands, on every branch: a
    person on the opt in for a machine with no keychain is told the refresh
    was not kept, and that the next run logs in again, rather than being
    blocked from the verb. The failure's class is named and never its words.
    """
    module = sys.modules.get("cratekit.acquire.provider_session")
    if module is None:
        return envelope
    met = module.unstored()[before:]
    if not met:
        return envelope
    entry = {
        "code": module.SESSION_NOT_STORED,
        "message": (
            f"the provider session this run's login refreshed could not be stored "
            f"({', '.join(dict.fromkeys(met))}), so the next run logs in again from "
            f"the stored session"
        ),
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

#: The write surfaces whose verbs may spend the hour's reserve (U278): a verb
#: that writes the account, or downloads, which writes files. Read off the
#: registry, so a verb added later is classed by what it declares it writes.
RESERVE_WRITES: frozenset[str] = frozenset({"remote", "files"})


def spends_reserve(entry: Entry, args: argparse.Namespace) -> bool:
    """Whether this command may spend the hour's reserve (U278).

    A verb that declares a write to the account or to files, unless it runs a
    report, which reads and plans and writes nothing. A verb with a read mode
    of its own narrows itself with ``provider_gate.reading``, as ``label sync``
    does for everything but ``--go``. Nothing widens a command past its verb.
    """
    if getattr(args, "report", False):
        return False
    return bool(entry.writes & RESERVE_WRITES)


def _gate_settings() -> provider_gate.GateSettings | None:
    """The configured gate numbers, or None when the configuration cannot be
    loaded, in which case the gate refuses the same ``--calls`` at its first
    call instead, off the configuration the verb loads."""
    try:
        return provider_gate.GateSettings.from_config(config.load())
    except Exception:  # noqa: BLE001 - see the docstring, the gate is the backstop
        return None


def _without(tokens: Sequence[str], flags: tuple[str, ...]) -> list[str]:
    """The tokens with each of ``flags`` taken out, given apart or with ``=``."""
    kept: list[str] = []
    skip = False
    for token in tokens:
        if skip:
            skip = False
            continue
        if token in flags:
            skip = True
            continue
        if token.startswith(tuple(f"{flag}=" for flag in flags)):
            continue
        kept.append(token)
    return kept


def _without_calls(tokens: Sequence[str]) -> list[str]:
    """The global options with any ``--calls`` and ``--calls-per-hour`` taken
    out, so each is given once (U278: the continue names the hour it needs)."""
    return _without(tokens, ("--calls", "--calls-per-hour"))


def _without_run(tokens: Sequence[str]) -> list[str]:
    """The command line with any ``--run`` taken out (U210)."""
    return _without(tokens, ("--run",))


def continue_command(argv: Sequence[str], entry: Entry, cause: Cause) -> str:
    """The exact command that continues a run the call ceiling stopped (U193).

    A job it was driving is parked with its remaining items pending, and the
    job engine names the job on the cause, so the command resumes THAT job: a
    verb run again would queue a second one. Anything else is this command line
    again with ``--calls`` raised, the global options kept, since a run that
    stopped at a gate continues by the same words.

    A verb whose write records its steps under its run names the run on the
    cause (U210), and the command carries ``--run`` for it when the command
    line did not already, so the continue is that run and not a new one. A
    verb that says its run cannot be continued (``fresh``) is named without
    the command line's own ``--run``, so the command starts a new run rather
    than one that refuses, or, when the cause names a run as well, continues
    THAT run in its place: ``label sync --go`` names the run whose go queued
    the download it stopped in, whichever run was driving it (U239).
    """
    detail = cause.detail or {}
    higher = str(detail.get("higher") or 2 * int(detail.get("ceiling") or 1))
    # THE HOUR IT NEEDS, NAMED BESIDE THE CEILING (U278): a ``--calls`` above
    # the configured hour is refused as printed without it, and a run whose
    # hour was raised continues with that hour.
    hour = detail.get("calls_per_hour")
    raised = ["--calls", higher, *(["--calls-per-hour", str(hour)] if hour else [])]
    job_id = detail.get("job_id")
    if job_id:
        return shlex.join(["crate", *raised, "job", "resume", str(job_id)])
    tokens = _without_run(argv) if detail.get("fresh") else list(argv)
    run_id = detail.get("run_id")
    named = any(token == "--run" or token.startswith("--run=") for token in tokens)
    run = ["--run", str(run_id)] if run_id and not named else []
    verb = _verb_argv(tokens, entry)
    if verb is None:
        return shlex.join(["crate", *run, *raised, *_without_calls(tokens)])
    lead = _without_calls(tokens[: len(tokens) - len(verb)])
    return shlex.join(["crate", *lead, *run, *raised, *verb])


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


def _with_run_continue(cause: Cause, state: gates.RunState) -> Cause:
    """A kept refusal's cause with its first step naming the command that continues the run.

    The step REPLACES the cause's first one, as the call ceiling's does,
    because that one says to run it again, and a person who follows it
    literally starts a fresh run and loses the answers this run keeps.
    """
    command = gates.continue_command(state)
    steps = (
        f"wait a moment for the process to finish exiting, then continue this "
        f"run with its answers: {command}",
        *cause.remediation.steps[1:],
    )
    return dataclasses.replace(
        cause,
        remediation=dataclasses.replace(cause.remediation, steps=steps),
        detail={**dict(cause.detail or {}), "continue": command, "run_id": state.run_id},
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
    with provider_gate.command(
        getattr(args, "calls", None),
        calls_per_hour=getattr(args, "calls_per_hour", None),
        reserve=spends_reserve(entry, args),
    ) as scope:
        envelope = _dispatched_in_scope(args, argv, entry, as_json=as_json, stderr=stderr)
    stopped = scope.stopped
    reported = envelope.cause is not None and envelope.cause.reason == (
        stopped.reason if stopped is not None else None
    )
    if stopped is not None and not reported:
        if stopped.reason == CALL_CEILING:
            command = continue_command(argv, entry, stopped)
            then = f"Continue with: {command}"
        else:
            # THE HOUR'S LINE (U278): continued by waiting, which no command
            # line can say, so the cause's own first step is the instruction.
            steps = stopped.remediation.steps
            then = steps[0][:1].upper() + steps[0][1:] if steps else ""
        entry_warning = {
            "code": stopped.reason,
            "message": (
                f"{stopped.message}; what this run reports after that point was not "
                f"read from the provider. {then}"
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
    unstored_before = _unstored()

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
        # A ``--calls`` THE HOUR CANNOT HOLD IS REFUSED BEFORE THE VERB RUNS
        # (U278), never capped in silence: a command line that says one ceiling
        # and runs another is a report over a run nobody asked for.
        if getattr(args, "calls", None) is not None:
            settings = _gate_settings()
            if settings is not None:
                over = provider_gate.over_the_line(settings)
                if over is not None:
                    raise CratekitError(over)

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
        # THE HOUR'S LINE IS A PARK TOO (U278) when the gate raised it as one:
        # what the run did is kept and it continues once the line frees. The
        # same reason refused before the verb ran, over ``--calls``, is a
        # command line to fix and stays a failure.
        from cratekit.core.jobs import Parked  # noqa: PLC0415 - the engine imports this package

        budget_stop = cause.reason == provider_gate.BUDGET and isinstance(exc, Parked)
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
        parked = isinstance(exc, JobBlocked) or ceiling_stop or budget_stop
        # A REFUSAL THAT KEEPS ITS RUN (U211). Raised before the step it
        # guards and clearing on its own, so the run is saved with its answers
        # and the cause names the command that continues it. ONLY THE SCAN'S
        # OWN REFUSAL, by its type (from review round two): a job that records
        # the same reason on a failed item and summarises it on the job's
        # cause cannot be continued by running the verb again, so that keeps
        # the job's own verdict and its honest step.
        kept = (
            isinstance(exc, processes.AbsenceUnconfirmed)
            and cause.reason in gates.KEPT_RUN_REASONS
            and not parked
        )
        if kept and state is not None:
            cause = _with_run_continue(cause, state)
        resumable = (cause.code in gates.GATE_CODES or kept) and not parked
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
    envelope = _with_unstored(envelope, unstored_before)
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
