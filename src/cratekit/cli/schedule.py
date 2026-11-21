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
system domain and never a system directory; and all three verbs refuse to run
as root, whose ``gui/0`` is nobody's login.

IT NEVER CUTS A NIGHT SHORT, from a shell reading the installation the agent
carries. Install and remove hold the staging lock while they boot the agent
out, so a night pass in progress, which holds it for its whole run, is never
ended by launchd under it: the verb refuses ``staging-held`` and the night runs
on. The lock is the shell's installation's; a shell pointed at another state
directory holds another lock (a residual of review round two).

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
directory of the ``crate`` it runs, the directories the install found each
binary in, the directories the binaries are looked for in, and the system's
own); the configuration, state and provider gate
directories AS THE INSTALL RESOLVED THEM, absolute, whether an override, an XDG
variable or the platform's default found them (review round one, finding 1),
so the night reads the installation the install read; and the library, staging,
ISRC cache and binary overrides set at the install, each made absolute. Never a
credential, and nothing else.

WHAT IT WRITES. The plist in the LaunchAgents directory, the directory of the
agent's log, the declared state entry ``schedule_log``, and, for install and
remove, the staging lock's file under the installation's state. Nothing a library
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
from cratekit.core import binaries, config, staging_lock
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

def resolved_names() -> tuple[str, ...]:
    """The directories an agent always carries, as the install resolved them.
    Read from the configuration module when asked, never bound at import."""
    return (config.ENV_CONFIG_DIR, config.ENV_STATE_DIR, config.ENV_PROVIDER_GATE_DIR)


def override_names() -> tuple[str, ...]:
    """The location overrides an agent carries only when set at the install."""
    return (config.ENV_LIBRARY_ROOT, config.ENV_DOWNLOAD_STAGING, config.ENV_ISRC_CACHE_DIR)


def carried_names() -> tuple[str, ...]:
    """Every location name an agent may carry."""
    return (*resolved_names(), *override_names())


def binary_names() -> tuple[str, ...]:
    """The per binary overrides an agent carries when set: one per binary this
    build knows, never a name merely starting with the prefix."""
    known = (*binaries.INSTALLABLE_BINARIES, *sorted(binaries.PLATFORM_BINARIES))
    return tuple(sorted({binaries.env_var(name) for name in known}))


def allowed_names() -> frozenset[str]:
    """Every environment name an agent's plist may hold."""
    return frozenset({"PATH", *carried_names(), *binary_names()})


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
    return _absolute(config.state_path(LOG_KEY))


def _absolute(path: Path | str) -> Path:
    """Made absolute against the install's directory, never resolved through
    links, so a relative override names the place the install meant."""
    return Path(os.path.abspath(path))


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


def crate_runs(path: Path | str) -> bool:
    """Whether ``path`` is an absolute executable file launchd can start."""
    found = Path(path)
    return found.is_absolute() and found.is_file() and os.access(found, os.X_OK)


def _resolved_crate() -> Path:
    found = crate_path()
    if not crate_runs(found):
        raise refuse(
            "schedule-crate-unresolved",
            f"the crate this install would schedule, {found}, is not an executable "
            "file, so the night's agent would run nothing",
            steps=("run crate schedule install from the crate you installed",),
            origin=_ORIGIN,
            detail={"crate": str(found)},
        )
    return found


def environment(crate: Path) -> dict[str, str]:
    """The agent's whole environment, every value absolute.

    A fixed PATH; the configuration, state and provider gate directories as
    the install resolved them, always; and the location and binary overrides
    set at the install. A credential is never carried: no carried name is one.
    """
    source = os.environ
    path: list[str] = []
    # THE DIRECTORIES THE INSTALL FOUND EACH BINARY IN (review round two,
    # finding 3), so a binary on the person's PATH alone is found at night.
    found = (binaries.find(name) for name in binaries.INSTALLABLE_BINARIES)
    found_in = [str(_absolute(Path(hit).parent)) for hit in found if hit]
    for directory in (
        str(crate.parent), *found_in, *(str(d) for d in binaries.fallback_dirs()), *SYSTEM_PATH
    ):
        if directory not in path:
            path.append(directory)
    carried = {"PATH": os.pathsep.join(path)}
    resolved = (config.config_dir(), config.installation_state_dir(), config.provider_gate_dir())
    for name, directory in zip(resolved_names(), resolved, strict=True):
        carried[name] = str(_absolute(directory))
    for name in (*override_names(), *binary_names()):
        value = source.get(name)
        if value:
            carried[name] = str(_absolute(value))
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
    """An installed plist, read back, and everything in it that is not the
    agent this build writes."""

    at: tuple[int, int] | None
    crate: str | None
    program: tuple[str, ...]
    log: str | None
    environment: dict[str, str]
    problems: tuple[str, ...]

    @property
    def runs_the_night(self) -> bool:
        return not self.problems


def _interval(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, dict) or set(value) != {"Hour", "Minute"}:
        return None
    hour, minute = value["Hour"], value["Minute"]
    if type(hour) is not int or type(minute) is not int:
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return hour, minute


def read_agent(path: Path | None = None) -> Installed | None:
    """The installed plist, None when there is none, and ``ValueError`` naming
    why when a file is there and cannot be read as this agent.

    WHAT LAUNCHD WILL DO, NOT ONLY WHAT THE FILE SAYS (review round one,
    findings 2 and 7, and round two, finding 6). Every difference this can
    read from the plist this build writes is a problem: another key, another
    program or word, a crate that cannot run, a run at load, another calendar,
    a name in its environment this build never carries, a carried directory
    missing or relative, a log outside the state it carries. Any problem and
    ``show`` fails. A directory changed by hand to another absolute one is not
    told apart from one install wrote.
    """
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
    problems: list[str] = []
    keys = set(document)
    if keys != PLIST_KEYS:
        extra, missing = sorted(keys - PLIST_KEYS), sorted(PLIST_KEYS - keys)
        problems.append(
            "its keys differ from the agent this build writes"
            + (f", adding {', '.join(extra)}" if extra else "")
            + (f", missing {', '.join(missing)}" if missing else "")
        )
    raw = document.get("ProgramArguments")
    program = tuple(str(part) for part in raw) if isinstance(raw, list) else ()
    crate = program[0] if program else None
    if not (
        isinstance(raw, list)
        and all(isinstance(part, str) for part in raw)
        and program[1:] == NIGHT_ARGV
        and crate is not None
        and Path(crate).name == "crate"
    ):
        problems.append(f"it runs {' '.join(program) or 'nothing'}, not crate sync night")
    if crate is not None and not crate_runs(crate):
        problems.append(f"the crate it runs, {crate}, is not an executable file")
    if document.get("RunAtLoad") is not False:
        problems.append("it runs when it is loaded, not only at night")
    at = _interval(document.get("StartCalendarInterval"))
    if at is None:
        problems.append("its calendar is not one time each night")
    log = document.get("StandardOutPath")
    if not (isinstance(log, str) and Path(log).is_absolute() and document.get("StandardErrorPath") == log):
        problems.append("its output does not go to one absolute log")
    raw_env = document.get("EnvironmentVariables")
    env = (
        {str(k): str(v) for k, v in raw_env.items()} if isinstance(raw_env, dict) else {}
    )
    if not isinstance(raw_env, dict) or not all(isinstance(v, str) for v in raw_env.values()):
        problems.append("its environment is not a set of names and values")
    unknown = sorted(set(env) - allowed_names())
    if unknown:
        problems.append(f"its environment carries {', '.join(unknown)}, which this build never does")
    # THE INSTALLATION IT READS (review round two, finding 6): the directories
    # install always carries, each absolute, and its log in the state it names.
    absent = [name for name in ("PATH", *resolved_names()) if not env.get(name)]
    if absent:
        problems.append(f"its environment is missing {', '.join(absent)}")
    relative = sorted(
        name for name, value in env.items()
        if name != "PATH" and name in allowed_names() and not Path(value).is_absolute()
    )
    if relative:
        problems.append(f"its environment names {', '.join(relative)} relative to nowhere")
    state = env.get(config.ENV_STATE_DIR)
    if state and isinstance(log, str):
        expected = Path(state) / config.state_file(LOG_KEY).relative
        if Path(log) != expected:
            problems.append(f"its log is {log}, not {expected} in the state it carries")
    return Installed(
        at=at,
        crate=crate,
        program=program,
        log=log if isinstance(log, str) else None,
        environment=env,
        problems=tuple(problems),
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


def _as_the_person(verb: str) -> None:
    """Refuse root: ``gui/0`` is nobody's login, and a root owned plist or log
    directory would be one the person's own install could not replace."""
    if uid() == 0:
        raise refuse(
            "refused-by-policy",
            f"crate schedule {verb} runs as you, never as root, so the agent is "
            "yours and loads with your login",
            steps=(f"run crate schedule {verb} again as yourself, not as root",),
            origin=_ORIGIN,
            detail={"uid": 0},
        )


def _launchctl_failed(what: str, answer: Answer | None, **detail: Any) -> Exception:
    if answer is None:
        said = "launchd still holds the agent after launchctl answered its bootout"
        answer = Answer(code=0, words="")
    else:
        said = f"launchctl answered {answer.code}, {answer.words or 'nothing'}"
    return refuse(
        "schedule-launchctl-failed",
        f"{what}: {said}",
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
        if not out.ok:
            said: Answer | None = out
        elif after == LOADED:
            said = None
        else:
            said = check
        raise _launchctl_failed(what, said, state=after)
    # ONE WAS BOOTED OUT only when launchd held it or the bootout took: a
    # bootout refused over an agent launchd then reads absent booted nothing.
    return state == LOADED or out.ok


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


def _install(crate: Path, at: tuple[int, int]) -> tuple[Path, Path, dict[str, str], bool]:
    """The install under the staging lock: boot out, write, bootstrap, read back."""
    target = plist_path()
    log = log_path()
    had_plist = target.exists()
    booted = _boot_out("the schedule already installed could not be booted out")
    replaced = booted or had_plist
    env = environment(crate)
    payload = plistlib.dumps(agent(crate, at, log, env), sort_keys=True)
    try:
        config.mkdir_private(log.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        config.atomic_write_bytes(payload, target, mode=PLIST_MODE)
    except OSError as exc:
        # SAID, NOT LEFT TO BE FOUND (review round one, finding 3): the agent
        # installed before is booted out by now, and its plist is unchanged.
        earlier = (
            "; the schedule installed before is booted out and its plist kept, so it is "
            "off until the next login or an install that succeeds"
            if booted
            else ""
        )
        raise refuse(
            "schedule-agent-unwritten",
            f"the night pass's agent could not be written to {target} ({exc}){earlier}",
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=_ORIGIN,
            detail={"plist": str(target), "log": str(log), "booted_out": booted},
        ) from None
    answer = launchctl("bootstrap", _domain(), str(target))
    state, check = loaded() if answer.ok else (UNKNOWN, answer)
    if state != LOADED:
        # NOTHING HALF INSTALLED: whatever launchd took is booted out again, and
        # the plist written for it is removed only once launchd reads it absent
        # (review round one, finding 4); otherwise it is kept, so show and
        # remove still find what launchd may hold.
        launchctl("bootout", _service())
        after, _after_answer = loaded()
        failed = answer if not answer.ok else check
        if after != NOT_LOADED:
            raise _launchctl_failed(
                "the night pass's agent could not be loaded, and launchd may still hold "
                "it, so its plist is kept; crate schedule remove takes it away",
                failed,
                plist=str(target),
                replaced=replaced,
                state=after,
            )
        _remove_plist(target)
        earlier = "; the schedule installed before it was removed too" if replaced else ""
        raise _launchctl_failed(
            f"the night pass's agent could not be loaded, so nothing is installed{earlier}",
            failed,
            plist=str(target),
            replaced=replaced,
        )
    return target, log, env, replaced


def install(ctx: Context) -> Envelope:
    """Write the night pass's agent and load it. See the module docstring."""
    _macos_only("install")
    _as_the_person("install")
    at: tuple[int, int] = ctx.args.at
    crate = _resolved_crate()
    with staging_lock.held("crate schedule install", run_id=ctx.run.run_id):
        target, log, env, replaced = _install(crate, at)
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
                    "environment": dict(env),
                    "loaded": True,
                    "replaced": replaced,
                }
            },
        },
        outcome=Outcome.OK,
    )


def _night_line(found: Installed | None) -> tuple[str, str]:
    """The last night's line, read from the state the AGENT carries when one is
    installed (review round one, finding 7), so a shell pointed elsewhere
    still reads the night the agent writes."""
    path = None
    if found is not None and found.environment.get(config.ENV_STATE_DIR):
        relative = config.state_file(sync_night.STATUS_KEY).relative
        path = Path(found.environment[config.ENV_STATE_DIR]) / relative
    try:
        record = sync_night.settle(sync_night.read_status(path))
    except ValueError as exc:
        return f"the night pass's record cannot be read: {exc}", "warn"
    if record is None:
        return "no night pass has run on this installation", "info"
    return str(record["line"]), "info"


def show(ctx: Context) -> Envelope:
    """Read the schedule back, and write nothing. See the module docstring."""
    _macos_only("show")
    _as_the_person("show")
    target = plist_path()
    rows: list[dict[str, Any]] = []
    try:
        found = read_agent(target)
        unreadable = None
    except ValueError as exc:
        found, unreadable = None, str(exc)
    state, answer = loaded()
    problems: list[str] = []
    if unreadable is not None:
        problems.append(unreadable)
        rows.append(_row("schedule.agent", "agent", f"the plist cannot be read: {unreadable}", "fail"))
    elif found is None:
        rows.append(_row("schedule.agent", "agent", f"not installed, no plist at {target}"))
    else:
        rows.append(_row("schedule.agent", "agent", f"installed at {target}", "ok"))
        rows.append(_row("schedule.at", "runs at", f"{_clock_words(found.at)} each night, local time"))
        rows.append(
            _row(
                "schedule.crate",
                "runs",
                " ".join(found.program) or "nothing",
                "info" if found.runs_the_night else "fail",
            )
        )
        for problem in found.problems:
            problems.append(problem)
            rows.append(_row("schedule.problem", "not the night's agent", problem, "fail"))
        if found.log:
            rows.append(_row("schedule.log", "log", found.log))
    if state == LOADED:
        loaded_words, loaded_status = f"loaded into {_domain()}", "ok"
        if found is None and unreadable is None:
            # LAUNCHD HOLDS AN AGENT NO PLIST DESCRIBES: what it runs cannot be
            # read here, so the report is not clean.
            problem = f"launchd holds {LABEL} but no plist is at {target}; crate schedule remove unloads it"
            problems.append(problem)
            loaded_words, loaded_status = problem, "fail"
    elif state == NOT_LOADED:
        loaded_words, loaded_status = "not loaded", "warn" if found else "info"
    else:
        loaded_words = f"launchd could not be read ({answer.code}, {answer.words or 'nothing said'})"
        loaded_status = "warn"
    rows.append(_row("schedule.loaded", "launchd", loaded_words, loaded_status))
    line, line_status = _night_line(found)
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
                "argv": [] if found is None else list(found.program),
                "runs_the_night": None if found is None else found.runs_the_night,
                "problems": problems,
                # NEVER A VALUE THIS BUILD WOULD NOT CARRY (review round two,
                # finding 10): a name it never carries is named in problems.
                "environment": {} if found is None else {
                    name: value for name, value in found.environment.items()
                    if name in allowed_names()
                },
                "loaded": state,
                "last": line,
            }
        },
    }
    if not problems:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    # AN AGENT THAT CANNOT BE READ, OR THAT IS ANYTHING BUT THE NIGHT'S, IS NOT
    # A CLEAN REPORT: the rows say what was read, and the exit says it failed.
    cause = refuse(
        "schedule-agent-unusable",
        "; ".join(problems),
        steps=("run crate schedule install to replace it, or crate schedule remove",),
        origin=_ORIGIN,
        detail={"plist": str(target), "problems": problems},
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
    _as_the_person("remove")
    target = plist_path()
    with staging_lock.held("crate schedule remove", run_id=ctx.run.run_id):
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
    "allowed_names",
    "binary_names",
    "build_show",
    "carried_names",
    "crate_runs",
    "crate_path",
    "environment",
    "install",
    "launch_agents_dir",
    "launchctl",
    "loaded",
    "override_names",
    "platform",
    "plist_path",
    "read_agent",
    "remove",
    "resolved_names",
    "show",
)
