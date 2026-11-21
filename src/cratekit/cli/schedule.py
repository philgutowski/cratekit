"""``crate schedule``: the night pass on launchd, installed, read and removed (U295).

``crate sync night`` (U293) is the sync pass run unattended up to its landing
gate. These three verbs put it on a schedule, so it runs overnight on the Mac
without anybody typing it:

* ``crate schedule install [--at HH:MM]`` writes ONE launchd user agent and
  loads it with ``launchctl bootstrap`` for the person's own GUI domain. An
  agent already installed is booted out first and replaced, never duplicated.
* ``crate schedule show`` reads it back: installed or not, the time, the
  ``crate`` it runs, whether launchd has it loaded, and the last night's line.
* ``crate schedule remove`` boots it out and deletes the plist. Nothing
  installed is a no op.

THE AGENT RUNS ``crate sync night`` AND NOTHING ELSE. Its program arguments are
exactly the absolute ``crate`` that ran the install, ``sync`` and ``night``: no
``-d``, no ``--calls``, no other verb, no shell. Every limit the night keeps is
the night verb's own (it answers no gate, mints no acknowledgment, refuses
beside rekordbox, a running job or another pass, and holds the night's budget),
so nothing here can widen it. ``show`` reads an installed agent's arguments
back and says so when they are anything else.

ONLY THE PERSON'S OWN LAUNCHAGENTS. The plist goes in ``Library/LaunchAgents``
under the home directory, resolved by :func:`launch_agents_dir` alone, and the
agent is loaded into ``gui/<uid>``, the logged in person's own domain. Never a
system domain, never ``/Library``, never root.

ONE PLACE STARTS A PROCESS. :func:`launchctl` is the only call into the
operating system that runs anything, by its absolute path, and the suite
replaces it in every test (``tests/conftest.py``), so no test ever loads,
starts or removes a launchd job. :func:`platform` is the one reading of the
platform, so the suite runs every verb as macOS on any machine.

NOTHING HALF INSTALLED. Success means the plist is written AND launchd reads
the agent loaded. A bootstrap that fails, or one launchd does not then read
loaded, is refused with launchctl's own words and the plist written for it is
removed, so the next ``show`` reads nothing installed rather than an agent
that will never fire. A bootout that leaves the agent loaded keeps its plist,
so ``show`` still reads what launchd holds.

NO ENVIRONMENT OF THE PERSON'S BEYOND WHAT THE RUN NEEDS. launchd starts the
agent with almost no environment. The plist carries a fixed ``PATH`` (the
directory of the ``crate`` it runs, the directories the binaries are looked for
in, and the system's own), and the Cratekit location overrides that were set at
the install, so the night reads the same configuration, state and library the
install did. Never a credential, and nothing else.

WHAT IT WRITES. The plist in the LaunchAgents directory and the directory of
the agent's log, the declared state entry ``schedule_log``. Nothing a library
knows about, which is why the registry entry declares no library surface, on
``crate skills install``'s argument.
"""

from __future__ import annotations

import argparse
import os
import plistlib
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import output, registry, sync_night
from cratekit.cli.output import Envelope
from cratekit.core import binaries, config, secrets
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.schedule",)

#: The agent's launchd label, and the plist's file name.
LABEL = "cratekit.sync-night"
PLIST_NAME = f"{LABEL}.plist"

#: The words the agent runs after the absolute ``crate``. Exactly these.
NIGHT_ARGV: tuple[str, ...] = ("sync", "night")

#: The one platform with launchd.
MACOS = "darwin"

#: The default firing, local time: deep in the night, outside the evening hours
#: the catalogue is busiest, and off the hour, when most scheduled work fires.
DEFAULT_AT: tuple[int, int] = (3, 17)

#: The declared state entry the agent's output is appended to.
LOG_KEY = "schedule_log"

#: launchctl, by its absolute path, so no PATH is read to find it.
LAUNCHCTL = "/bin/launchctl"

#: How long one launchctl call may take before it is read as failed.
LAUNCHCTL_TIMEOUT = 60

#: What ``launchctl print`` answers for a service launchd does not have.
NOT_LOADED_CODE = 113

#: The system's own directories, last on the agent's PATH.
SYSTEM_PATH: tuple[str, ...] = ("/usr/bin", "/bin", "/usr/sbin", "/sbin")

def carried_names() -> tuple[str, ...]:
    """The Cratekit location overrides an agent carries when they were set at
    the install, so the night resolves what the install resolved. Read from
    the configuration module when asked, never bound at import."""
    return (
        config.ENV_CONFIG_DIR,
        config.ENV_STATE_DIR,
        config.ENV_LIBRARY_ROOT,
        config.ENV_ISRC_CACHE_DIR,
        config.ENV_PROVIDER_GATE_DIR,
        config.ENV_DOWNLOAD_STAGING,
    )


#: Every key the agent's plist holds, and nothing else.
PLIST_KEYS: frozenset[str] = frozenset(
    {
        "Label",
        "ProgramArguments",
        "StartCalendarInterval",
        "StandardOutPath",
        "StandardErrorPath",
        "EnvironmentVariables",
        "RunAtLoad",
    }
)

#: The plist's mode: the person's own, read by launchd as them.
PLIST_MODE = 0o600


# ---------------------------------------------------------------------------
# The seams: the platform, the directory, the one process
# ---------------------------------------------------------------------------


def platform() -> str:
    """The running platform. The one reading of it, so the suite can name it."""
    return sys.platform


def uid() -> int:
    """The person's user id, whose GUI domain the agent is loaded into."""
    return os.getuid()


def launch_agents_dir() -> Path:
    """The person's own LaunchAgents directory, composed from the home directory.

    The one place the plist's directory is resolved. Composed from
    ``Path.home()`` so no home directory is spelled anywhere in this package.
    """
    return Path.home() / "Library" / "LaunchAgents"


def plist_path() -> Path:
    return launch_agents_dir() / PLIST_NAME


def log_path() -> Path:
    return config.state_path(LOG_KEY)


@dataclass(frozen=True, slots=True)
class Answer:
    """What one launchctl call answered: its exit code and its own words."""

    code: int
    words: str

    @property
    def ok(self) -> bool:
        return self.code == 0


def launchctl(*args: str) -> Answer:
    """Run launchctl once. THE ONLY PLACE THIS MODULE STARTS A PROCESS.

    A launchctl that cannot be started, or that outlives its timeout, answers
    a failure in its own words rather than raising, so every caller refuses
    through one path.
    """
    import subprocess  # noqa: PLC0415 - confined to the one seam

    try:
        done = subprocess.run(  # noqa: S603 - an absolute path and fixed words
            [LAUNCHCTL, *args],
            capture_output=True,
            text=True,
            timeout=LAUNCHCTL_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return Answer(code=-1, words=f"launchctl could not be run ({exc})")
    words = " ".join(part.strip() for part in (done.stderr, done.stdout) if part.strip())
    return Answer(code=done.returncode, words=words)


def _domain() -> str:
    return f"gui/{uid()}"


def _service() -> str:
    return f"{_domain()}/{LABEL}"


# ---------------------------------------------------------------------------
# What launchd holds
# ---------------------------------------------------------------------------

LOADED = "loaded"
NOT_LOADED = "not loaded"
UNKNOWN = "unknown"


def loaded() -> tuple[str, Answer]:
    """Whether launchd holds the agent: loaded, not loaded, or unknown.

    ONLY ``launchctl print``'s own not found code reads as not loaded. Any other
    failure is unknown and said as such, never read as absent.
    """
    answer = launchctl("print", _service())
    if answer.ok:
        return LOADED, answer
    if answer.code == NOT_LOADED_CODE:
        return NOT_LOADED, answer
    return UNKNOWN, answer


# ---------------------------------------------------------------------------
# The plist
# ---------------------------------------------------------------------------


def crate_path() -> Path:
    """The absolute ``crate`` that is running this install.

    The ``crate`` this process was started as, when it was; otherwise the one
    beside the interpreter running it, which is the same installation's. Not
    resolved through symbolic links, so an agent naming a link keeps following
    an upgrade that moves what the link names.
    """
    started_as = Path(sys.argv[0]) if sys.argv and sys.argv[0] else None
    if started_as is not None and started_as.name == "crate":
        return Path(os.path.abspath(started_as))
    return Path(os.path.abspath(Path(sys.executable).parent / "crate"))


def _resolved_crate() -> Path:
    found = crate_path()
    if not (found.is_absolute() and found.is_file() and os.access(found, os.X_OK)):
        raise refuse(
            "schedule-crate-unresolved",
            f"the crate this install would schedule, {found}, is not an executable "
            "file, so the night's agent would run nothing",
            steps=("run crate schedule install from the crate you installed",),
            origin=_ORIGIN,
            detail={"crate": str(found)},
        )
    return found


def environment(crate: Path, env: Mapping[str, str] | None = None) -> dict[str, str]:
    """The agent's whole environment: a fixed PATH and the carried overrides.

    The overrides are the location variables :func:`carried_names` names and the
    per binary overrides, taken from the install's environment when set. A
    credential is never carried, whatever its name.
    """
    source = os.environ if env is None else env
    named = carried_names()
    path: list[str] = []
    for directory in (str(crate.parent), *(str(d) for d in binaries.fallback_dirs()), *SYSTEM_PATH):
        if directory not in path:
            path.append(directory)
    carried = {"PATH": os.pathsep.join(path)}
    for name in sorted(source):
        if name.startswith(secrets.ENV_CREDENTIAL_PREFIX):
            continue
        if name in named or name.startswith(binaries.ENV_PREFIX):
            value = source[name]
            if value:
                carried[name] = value
    return carried


def agent(crate: Path, at: tuple[int, int], log: Path, env: Mapping[str, str]) -> dict[str, Any]:
    """The agent's plist, as a mapping. Frozen: these keys, and these only."""
    hour, minute = at
    return {
        "Label": LABEL,
        "ProgramArguments": [str(crate), *NIGHT_ARGV],
        "StartCalendarInterval": {"Hour": hour, "Minute": minute},
        "StandardOutPath": str(log),
        "StandardErrorPath": str(log),
        "EnvironmentVariables": dict(env),
        "RunAtLoad": False,
    }


@dataclass(frozen=True, slots=True)
class Installed:
    """An installed plist, read back."""

    at: tuple[int, int] | None
    crate: str | None
    runs_the_night: bool
    log: str | None
    environment: tuple[str, ...]


def read_agent(path: Path | None = None) -> Installed | None:
    """The installed plist, None when there is none, and ``ValueError`` naming
    why when a file is there and cannot be read as this agent."""
    target = path if path is not None else plist_path()
    try:
        data = target.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ValueError(f"{target} could not be read ({exc})") from None
    try:
        document = plistlib.loads(data)
    except Exception:  # noqa: BLE001 - plistlib raises several unrelated types
        raise ValueError(f"{target} is not a property list") from None
    if not isinstance(document, dict) or document.get("Label") != LABEL:
        raise ValueError(f"{target} is not the night pass's agent")
    program = document.get("ProgramArguments")
    crate = program[0] if isinstance(program, list) and program and isinstance(program[0], str) else None
    runs_the_night = (
        isinstance(program, list)
        and len(program) == 1 + len(NIGHT_ARGV)
        and crate is not None
        and Path(crate).is_absolute()
        and tuple(program[1:]) == NIGHT_ARGV
        and set(document) <= PLIST_KEYS
    )
    interval = document.get("StartCalendarInterval")
    at = None
    if isinstance(interval, dict):
        hour, minute = interval.get("Hour"), interval.get("Minute")
        if isinstance(hour, int) and isinstance(minute, int):
            at = (hour, minute)
    env = document.get("EnvironmentVariables")
    log = document.get("StandardOutPath")
    return Installed(
        at=at,
        crate=crate,
        runs_the_night=runs_the_night,
        log=log if isinstance(log, str) else None,
        environment=tuple(sorted(env)) if isinstance(env, dict) else (),
    )


def _clock_words(at: tuple[int, int] | None) -> str:
    return "no time" if at is None else f"{at[0]:02d}:{at[1]:02d}"


# ---------------------------------------------------------------------------
# The arguments
# ---------------------------------------------------------------------------


def _at(text: str) -> tuple[int, int]:
    """``HH:MM``, a time of day on the 24 hour clock."""
    hour_text, sep, minute_text = text.partition(":")
    if (
        sep
        and len(hour_text) in (1, 2)
        and len(minute_text) == 2
        and hour_text.isdigit()
        and minute_text.isdigit()
    ):
        hour, minute = int(hour_text), int(minute_text)
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return hour, minute
    raise argparse.ArgumentTypeError(
        f"must be a time of day as HH:MM on the 24 hour clock, found {text!r}"
    )


def build_install(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument(
        "--at",
        type=_at,
        default=DEFAULT_AT,
        metavar="HH:MM",
        help=(
            "when the night pass runs each night, local time on the 24 hour clock "
            f"(default {_clock_words(DEFAULT_AT)})"
        ),
    )
    parser.set_defaults(_handler=install)


def build_show(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.set_defaults(_handler=show)


def build_remove(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.set_defaults(_handler=remove)


# ---------------------------------------------------------------------------
# The verbs
# ---------------------------------------------------------------------------


def _macos_only(verb: str) -> None:
    running = platform()
    if running != MACOS:
        raise refuse(
            "schedule-platform-unsupported",
            f"crate schedule {verb} needs launchd, which is macOS's; this is "
            f"{running}, so there is no schedule to {verb} here",
            steps=("run crate sync night from this platform's own scheduler, or by hand",),
            origin=_ORIGIN,
            detail={"platform": running},
        )


def _launchctl_failed(what: str, answer: Answer, **detail: Any) -> Exception:
    said = answer.words or "nothing"
    return refuse(
        "schedule-launchctl-failed",
        f"{what}: launchctl answered {answer.code}, {said}",
        steps=("read crate schedule show, then run the verb again",),
        origin=_ORIGIN,
        detail={"launchctl_code": answer.code, "launchctl_words": answer.words, **detail},
    )


def _row(key: str, title: str, detail: str, status: str = "info") -> dict[str, Any]:
    return {"key": key, "title": title, "status": status, "detail": detail, "remedy": None}


def _boot_out(what: str) -> bool:
    """Boot the agent out if launchd may hold it. True when one was booted out.

    Read again after: only launchd's own not loaded answer lets a caller go
    on, so an agent still loaded, or one whose state cannot be read, refuses
    with the words that say why.
    """
    state, _answer = loaded()
    if state == NOT_LOADED:
        return False
    out = launchctl("bootout", _service())
    after, check = loaded()
    if after != NOT_LOADED:
        raise _launchctl_failed(what, out if not out.ok else check, state=after)
    return True


def _remove_plist(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError as exc:
        raise refuse(
            "schedule-agent-unwritten",
            f"the agent's plist {path} could not be removed ({exc})",
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=_ORIGIN,
            detail={"plist": str(path)},
        ) from None


def install(ctx: Context) -> Envelope:
    """Write the night pass's agent and load it. See the module docstring."""
    _macos_only("install")
    at: tuple[int, int] = ctx.args.at
    crate = _resolved_crate()
    target = plist_path()
    log = log_path()
    had_plist = target.exists()
    replaced = _boot_out("the schedule already installed could not be booted out") or had_plist
    env = environment(crate)
    payload = plistlib.dumps(agent(crate, at, log, env), sort_keys=True)
    try:
        config._mkdir_private(log.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        config.atomic_write_bytes(payload, target, mode=PLIST_MODE)
    except OSError as exc:
        raise refuse(
            "schedule-agent-unwritten",
            f"the night pass's agent could not be written to {target} ({exc})",
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=_ORIGIN,
            detail={"plist": str(target), "log": str(log)},
        ) from None
    answer = launchctl("bootstrap", _domain(), str(target))
    state, check = loaded() if answer.ok else (UNKNOWN, answer)
    if state != LOADED:
        # NOTHING HALF INSTALLED: whatever launchd took is booted out again and
        # the plist written for it is removed.
        launchctl("bootout", _service())
        _remove_plist(target)
        earlier = "; the schedule installed before it was removed too" if replaced else ""
        raise _launchctl_failed(
            f"the night pass's agent could not be loaded, so nothing is installed{earlier}",
            answer if not answer.ok else check,
            plist=str(target),
            replaced=replaced,
        )
    when = _clock_words(at)
    rows = [
        _row("schedule.agent", "agent", f"{target}, loaded into {_domain()}", "ok"),
        _row("schedule.at", "runs at", f"{when} each night, local time"),
        _row("schedule.crate", "runs", " ".join([str(crate), *NIGHT_ARGV])),
        _row("schedule.log", "log", str(log)),
    ]
    if replaced:
        rows.append(_row("schedule.replaced", "replaced", "the schedule installed before was replaced"))
    return ctx.envelope(
        data={
            "checks": rows,
            "summary": {
                "schedule": {
                    "label": LABEL,
                    "plist": str(target),
                    "at": when,
                    "crate": str(crate),
                    "argv": [str(crate), *NIGHT_ARGV],
                    "log": str(log),
                    "environment": sorted(env),
                    "loaded": True,
                    "replaced": replaced,
                }
            },
        },
        outcome=Outcome.OK,
    )


def _night_line() -> tuple[str, str]:
    try:
        record = sync_night.settle(sync_night.read_status())
    except ValueError as exc:
        return f"the night pass's record cannot be read: {exc}", "warn"
    if record is None:
        return "no night pass has run on this installation", "info"
    return str(record["line"]), "info"


def show(ctx: Context) -> Envelope:
    """Read the schedule back, and write nothing. See the module docstring."""
    _macos_only("show")
    target = plist_path()
    rows: list[dict[str, Any]] = []
    try:
        found = read_agent(target)
        unreadable = None
    except ValueError as exc:
        found, unreadable = None, str(exc)
    state, answer = loaded()
    if unreadable is not None:
        rows.append(_row("schedule.agent", "agent", f"the plist cannot be read: {unreadable}", "fail"))
    elif found is None:
        rows.append(_row("schedule.agent", "agent", f"not installed, no plist at {target}"))
    else:
        rows.append(_row("schedule.agent", "agent", f"installed at {target}", "ok"))
        rows.append(_row("schedule.at", "runs at", f"{_clock_words(found.at)} each night, local time"))
        if found.runs_the_night:
            rows.append(_row("schedule.crate", "runs", " ".join([str(found.crate), *NIGHT_ARGV])))
        else:
            rows.append(
                _row(
                    "schedule.crate",
                    "runs",
                    "the installed agent runs something other than crate sync night; "
                    "run crate schedule install to replace it",
                    "fail",
                )
            )
        if found.log:
            rows.append(_row("schedule.log", "log", found.log))
    if state == LOADED:
        loaded_words, loaded_status = f"loaded into {_domain()}", "ok" if found else "warn"
    elif state == NOT_LOADED:
        loaded_words, loaded_status = "not loaded", "warn" if found else "info"
    else:
        loaded_words = f"launchd could not be read ({answer.code}, {answer.words or 'nothing said'})"
        loaded_status = "warn"
    rows.append(_row("schedule.loaded", "launchd", loaded_words, loaded_status))
    line, line_status = _night_line()
    rows.append(_row("schedule.last", "last night", line, line_status))
    data = {
        "checks": rows,
        "summary": {
            "schedule": {
                "label": LABEL,
                "plist": str(target),
                "installed": found is not None,
                "unreadable": unreadable,
                "at": None if found is None or found.at is None else _clock_words(found.at),
                "crate": None if found is None else found.crate,
                "runs_the_night": None if found is None else found.runs_the_night,
                "environment": [] if found is None else list(found.environment),
                "loaded": state,
                "last": line,
            }
        },
    }
    problem = unreadable or (
        None if found is None or found.runs_the_night
        else f"the agent at {target} runs something other than crate sync night"
    )
    if problem is None:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    # AN AGENT THAT CANNOT BE READ, OR THAT RUNS ANYTHING BUT THE NIGHT, IS NOT
    # A CLEAN REPORT: the rows say what was read, and the exit says it failed.
    cause = refuse(
        "schedule-agent-unusable",
        problem,
        steps=("run crate schedule install to replace it, or crate schedule remove",),
        origin=_ORIGIN,
        detail={"plist": str(target)},
    ).cause
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=ctx.entry.output_schema or output.current_schema("diagnostic"),
        started=ctx.started,
        outcome=Outcome.FAILED,
        code=cause.code,
        data=data,
        cause=cause,
    )


def remove(ctx: Context) -> Envelope:
    """Boot the agent out and delete its plist. See the module docstring."""
    _macos_only("remove")
    target = plist_path()
    had_plist = target.exists()
    booted = _boot_out("the schedule could not be booted out, so its plist is kept")
    if had_plist:
        _remove_plist(target)
    if not (booted or had_plist):
        return ctx.envelope(
            data={
                "checks": [_row("schedule.agent", "agent", "nothing installed, nothing removed")],
                "summary": {"schedule": {"label": LABEL, "plist": str(target), "removed": False}},
            },
            outcome=Outcome.NO_OP,
        )
    rows = [_row("schedule.agent", "agent", f"removed {target}" if had_plist else "no plist was there", "ok")]
    rows.append(_row("schedule.loaded", "launchd", "booted out" if booted else "was not loaded"))
    return ctx.envelope(
        data={
            "checks": rows,
            "summary": {
                "schedule": {
                    "label": LABEL,
                    "plist": str(target),
                    "removed": True,
                    "booted_out": booted,
                    "deleted": had_plist,
                }
            },
        },
        outcome=Outcome.OK,
    )


__all__: Sequence[str] = (
    "Answer",
    "DEFAULT_AT",
    "LABEL",
    "NIGHT_ARGV",
    "PLIST_KEYS",
    "agent",
    "build_install",
    "build_remove",
    "build_show",
    "carried_names",
    "crate_path",
    "environment",
    "install",
    "launch_agents_dir",
    "launchctl",
    "loaded",
    "platform",
    "plist_path",
    "read_agent",
    "remove",
    "show",
)
