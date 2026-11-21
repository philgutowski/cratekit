"""U295: ``crate schedule`` installs, shows and removes the night pass on launchd.

WHAT THIS FILE GUARDS. The brief's two merge blockers first: the agent runs
``crate sync night`` and nothing else, and it is installed only in the
person's own LaunchAgents directory, loaded into their own GUI domain. Then
the three verbs' behaviour: install writes one agent and loads it, a second
install replaces it, a launchctl that fails leaves nothing half installed,
show reads every state without writing, and remove unloads and deletes.

WHAT STANDS IN. launchd, whole: :class:`Launchd` answers ``print``,
``bootstrap`` and ``bootout`` as launchctl does, over a set of loaded labels it
keeps itself, and reads every plist it is handed. The platform is named macOS
by :func:`mac`, the LaunchAgents directory is a temporary one, and the crate is
a temporary executable. ``tests/conftest.py`` replaces the shipped launchctl
seam in every test, so a test that forgets this fixture fails rather than
reaching launchd.
"""

from __future__ import annotations

import ast
import os
import plistlib
import sys
from pathlib import Path
from typing import Any

import pytest

from cratekit.cli import registry, schedule, sync_night
from cratekit.core import binaries, config
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive

SOURCE = Path(schedule.__file__)
UID = 501
DOMAIN = f"gui/{UID}"
SERVICE = f"{DOMAIN}/{schedule.LABEL}"


class Launchd:
    """launchctl standing in, over the labels it holds loaded.

    ``fail`` maps a launchctl word to the answer it gives instead; ``stuck``
    makes a bootout answer success and leave the agent loaded.
    """

    def __init__(self) -> None:
        self.loaded: dict[str, dict[str, Any]] = {}
        self.calls: list[tuple[str, ...]] = []
        self.fail: dict[str, schedule.Answer] = {}
        self.stuck = False
        self.stuck_absent = False

    def __call__(self, *args: str) -> schedule.Answer:
        self.calls.append(args)
        verb = args[0]
        if verb in self.fail:
            return self.fail[verb]
        if verb in ("print", "bootout"):
            assert args[1] == SERVICE, f"launchctl {verb} asked {args[1]}, not the person's agent"
        if verb == "print":
            label = args[1].rsplit("/", 1)[-1]
            if label in self.loaded:
                return schedule.Answer(0, f"{label} = {{ state = not running }}")
            return schedule.Answer(113, f'Could not find service "{label}" in domain')
        if verb == "bootstrap":
            assert args[1] == DOMAIN, f"bootstrapped into {args[1]}, not the person's domain"
            document = plistlib.loads(Path(args[2]).read_bytes())
            label = document["Label"]
            if label in self.loaded:
                return schedule.Answer(5, "Bootstrap failed: 5: Input/output error")
            self.loaded[label] = document
            return schedule.Answer(0, "")
        if verb == "bootout":
            label = args[1].rsplit("/", 1)[-1]
            if label not in self.loaded and self.stuck_absent:
                return schedule.Answer(3, "Boot-out failed: 3: No such process")
            if label not in self.loaded:
                return schedule.Answer(3, "Boot-out failed: 3: No such process")
            if not self.stuck:
                del self.loaded[label]
            return schedule.Answer(0, "")
        raise AssertionError(f"launchctl {verb} was not expected")

    def verbs(self) -> list[str]:
        return [call[0] for call in self.calls]


@pytest.fixture
def crate(tmp_path) -> Path:
    path = tmp_path / "venv" / "bin" / "crate"
    path.parent.mkdir(parents=True)
    path.write_text("#!/bin/sh\n")
    path.chmod(0o755)
    return path


@pytest.fixture
def agents(tmp_path) -> Path:
    return tmp_path / "home" / "Library" / "LaunchAgents"


@pytest.fixture
def mac(monkeypatch, crate, agents) -> Launchd:
    """A Mac: launchd standing in, the person's LaunchAgents, and a crate."""
    launchd = Launchd()
    monkeypatch.setattr(schedule, "platform", lambda: schedule.MACOS)
    monkeypatch.setattr(schedule, "launchctl", launchd)
    monkeypatch.setattr(schedule, "uid", lambda: UID)
    monkeypatch.setattr(schedule, "launch_agents_dir", lambda: agents)
    monkeypatch.setattr(schedule, "crate_path", lambda: crate)
    return launchd


def _plist(agents: Path) -> dict[str, Any]:
    return plistlib.loads((agents / schedule.PLIST_NAME).read_bytes())


def _tree(*roots: Path) -> dict[str, bytes]:
    found: dict[str, bytes] = {}
    for root in roots:
        if root.is_dir():
            for current, _dirs, files in os.walk(root):
                for name in files:
                    path = Path(current) / name
                    found[str(path)] = path.read_bytes()
    return found


# ---------------------------------------------------------------------------
# The registry, and the guards
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["schedule.install", "schedule.show", "schedule.remove"])
def test_each_verb_declares_no_library_write_and_no_gate(name):
    entry = registry.entry(name)

    assert entry.landed and entry.module == "cratekit.cli.schedule"
    assert entry.writes == frozenset() and not entry.destructive
    assert entry.gates == () and not entry.long_running


def test_the_suite_stands_launchd_in_for_every_test(_no_live_launchd):
    """The conftest guard: the shipped seam is never the one a test reaches,
    the reach is recorded so a verb that swallowed the error still fails its
    test, and the platform reads as one with no launchd unless a test says Mac."""
    with pytest.raises(AssertionError, match="launchctl"):
        schedule.launchctl("print", SERVICE)
    assert _no_live_launchd == [f"print {SERVICE}"]
    _no_live_launchd.clear()
    assert schedule.platform() != schedule.MACOS


#: Every module the schedule may import, at the top of the file. An allowlist,
#: so a launcher this list never thought of is still refused (review round one).
ALLOWED_IMPORTS = frozenset({
    "__future__", "argparse", "os", "plistlib", "sys", "collections.abc", "dataclasses",
    "pathlib", "typing", "cratekit.cli", "cratekit.cli.output", "cratekit.core",
    "cratekit.core.cause", "cratekit.core.exit_codes",
})

#: Attribute names that start a process, refused through any module.
LAUNCHER_ATTRS = frozenset({
    "system", "popen", "Popen", "fork", "forkpty", "startfile", "check_output",
    "check_call", "getoutput", "getstatusoutput", "create_subprocess_exec",
    "create_subprocess_shell", "subprocess", "execv", "execve", "execl", "execle",
    "execlp", "execlpe", "execvp", "execvpe", "spawnv", "spawnve", "spawnvp",
    "spawnvpe", "spawnl", "spawnle", "spawnlp", "spawnlpe", "posix_spawn",
    "posix_spawnp", "spawn",
})

#: Every attribute of ``os`` the schedule may name.
ALLOWED_OS = frozenset({"path", "environ", "access", "X_OK", "getuid", "pathsep", "abspath"})


def _imported(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Import):
            names.update(alias.name for alias in child.names)
        elif isinstance(child, ast.ImportFrom):
            names.add(child.module or "")
    return names


def test_only_the_one_seam_starts_a_process():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    seam = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "launchctl"
    )
    assert _imported(seam) == {"subprocess"}
    rest = [node for node in tree.body if node is not seam]
    imported = set().union(*(_imported(node) for node in rest))
    assert imported <= ALLOWED_IMPORTS, f"the schedule imports {sorted(imported - ALLOWED_IMPORTS)}"
    for node in rest:
        for child in ast.walk(node):
            # No name imported from os, and os under no other name (review
            # round two, finding 8): ``from os import system``, ``import os as
            # _os``.
            if isinstance(child, ast.ImportFrom):
                assert child.module != "os", "the schedule imports a name from os"
            if isinstance(child, ast.Import):
                for alias in child.names:
                    assert alias.asname is None, f"the schedule imports {alias.name} as {alias.asname}"
            # No launcher reached through any module, ``config.os.system``
            # included.
            if isinstance(child, ast.Attribute):
                assert child.attr not in LAUNCHER_ATTRS, f"the schedule names .{child.attr}"
            if isinstance(child, ast.Name):
                assert child.id not in {"__import__", "importlib", "getattr", "eval", "exec"}, child.id
            if (
                isinstance(child, ast.Attribute)
                and isinstance(child.value, ast.Name)
                and child.value.id == "os"
            ):
                assert child.attr in ALLOWED_OS, f"the schedule names os.{child.attr}"
    assert schedule.LAUNCHCTL == "/bin/launchctl"


def _shipped_seam(monkeypatch):
    """The module's own launchctl, from a fresh copy: the suite's guard has
    replaced the one on the imported module."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("schedule_shipped_copy", SOURCE)
    copy = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, copy)
    spec.loader.exec_module(copy)
    return copy


def test_the_seam_runs_launchctl_by_its_path_and_answers_its_words(tmp_path, monkeypatch):
    copy = _shipped_seam(monkeypatch)
    fake = tmp_path / "launchctl"
    fake.write_text("#!/bin/sh\necho \"said $*\"\necho oops >&2\nexit 7\n")
    fake.chmod(0o755)
    copy.LAUNCHCTL = str(fake)

    answer = copy.launchctl("print", SERVICE)

    assert answer.code == 7
    assert answer.words == f"oops said print {SERVICE}"


def test_the_seam_answers_a_launchctl_it_cannot_run_or_that_hangs(tmp_path, monkeypatch):
    copy = _shipped_seam(monkeypatch)
    copy.LAUNCHCTL = str(tmp_path / "absent")
    assert copy.launchctl("print", SERVICE).code == -1

    sleeper = tmp_path / "sleeper"
    sleeper.write_text("#!/bin/sh\nsleep 5\n")
    sleeper.chmod(0o755)
    copy.LAUNCHCTL, copy.LAUNCHCTL_TIMEOUT = str(sleeper), 1
    answer = copy.launchctl("print", SERVICE)
    assert answer.code == -1 and "could not be run" in answer.words


def test_the_module_names_no_system_domain_and_no_system_directory():
    text = SOURCE.read_text(encoding="utf-8")
    for spelled in ("LaunchDaemons", '"/Library', "'/Library", "system/", "sudo"):
        assert spelled not in text, f"the schedule module spells {spelled!r}"
    assert schedule.NIGHT_ARGV == ("sync", "night")
    assert schedule.LABEL == "cratekit.sync-night", "the guide names the agent by this label"


def test_the_default_directory_is_the_persons_own_launch_agents():
    assert schedule.launch_agents_dir() == Path.home() / "Library" / "LaunchAgents"


# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------


def test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it(mac, agents, crate):
    code, envelope = drive(["schedule", "install"])

    assert code == 0, envelope
    assert sorted(p.name for p in agents.iterdir()) == [schedule.PLIST_NAME]
    document = _plist(agents)
    log = config.state_path(schedule.LOG_KEY)
    # WRITTEN OUT BY HAND, never read off the module (review round one): a key
    # added to the template and its key set together is still caught here.
    assert document == {
        "Label": "cratekit.sync-night",
        "ProgramArguments": [str(crate), "sync", "night"],
        "StartCalendarInterval": {"Hour": 3, "Minute": 17},
        "StandardOutPath": str(log),
        "StandardErrorPath": str(log),
        "EnvironmentVariables": document["EnvironmentVariables"],
        "RunAtLoad": False,
    }
    assert (agents / schedule.PLIST_NAME).stat().st_mode & 0o777 == 0o600
    assert log.parent.is_dir(), "launchd cannot open a log in a directory that is not there"
    assert ("bootstrap", DOMAIN, str(agents / schedule.PLIST_NAME)) in mac.calls
    assert schedule.LABEL in mac.loaded
    summary = envelope["data"]["summary"]["schedule"]
    assert summary["at"] == "03:17" and summary["loaded"] is True and summary["replaced"] is False
    assert summary["argv"] == [str(crate), "sync", "night"]


def test_the_agent_names_an_absolute_crate(mac, agents):
    drive(["schedule", "install"])

    program = _plist(agents)["ProgramArguments"]
    assert Path(program[0]).is_absolute() and Path(program[0]).name == "crate"


@pytest.mark.parametrize("state", ["relative", "missing", "not executable", "a directory"])
def test_a_crate_that_cannot_run_is_refused_and_nothing_is_written(
    mac, agents, crate, monkeypatch, state
):
    if state == "relative":
        # A relative path that is there from here, so only absoluteness refuses it.
        monkeypatch.chdir(crate.parent.parent)
        found = Path("bin") / "crate"
    elif state == "a directory":
        found = crate.parent
    elif state == "missing":
        found = crate.parent / "gone" / "crate"
    else:
        crate.chmod(0o644)
        found = crate
    monkeypatch.setattr(schedule, "crate_path", lambda: found)

    code, envelope = drive(["schedule", "install"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-crate-unresolved"
    assert not agents.exists() or not any(agents.iterdir())
    assert "bootstrap" not in mac.verbs()


def test_the_crate_is_the_one_this_process_was_started_as(monkeypatch, tmp_path):
    started = tmp_path / "bin" / "crate"
    monkeypatch.setattr(sys, "argv", [str(started), "schedule", "install"])
    assert schedule.crate_path() == started

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [os.path.join("bin", "crate")])
    assert schedule.crate_path() == started, "a relative argv is made absolute"

    monkeypatch.setattr(sys, "argv", ["/somewhere/python", "-m", "cratekit"])
    assert schedule.crate_path() == Path(sys.executable).parent.absolute() / "crate"


def test_install_twice_replaces_the_agent_and_never_duplicates_it(mac, agents):
    drive(["schedule", "install"])
    code, envelope = drive(["schedule", "install", "--at", "22:05"])

    assert code == 0, envelope
    assert sorted(p.name for p in agents.iterdir()) == [schedule.PLIST_NAME]
    assert _plist(agents)["StartCalendarInterval"] == {"Hour": 22, "Minute": 5}
    assert mac.loaded[schedule.LABEL]["StartCalendarInterval"] == {"Hour": 22, "Minute": 5}
    assert mac.verbs().count("bootstrap") == 2
    assert mac.verbs().count("bootout") == 1
    assert envelope["data"]["summary"]["schedule"]["replaced"] is True


def test_a_plist_left_without_launchd_holding_it_is_replaced(mac, agents):
    agents.mkdir(parents=True)
    (agents / schedule.PLIST_NAME).write_bytes(b"left by hand")

    code, envelope = drive(["schedule", "install"])

    assert code == 0, envelope
    assert _plist(agents)["Label"] == schedule.LABEL
    assert "bootout" not in mac.verbs()
    assert envelope["data"]["summary"]["schedule"]["replaced"] is True


@pytest.mark.parametrize(
    ("text", "at"), [("4:05", (4, 5)), ("00:00", (0, 0)), ("23:59", (23, 59))]
)
def test_at_sets_the_time(mac, agents, text, at):
    code, envelope = drive(["schedule", "install", "--at", text])

    assert code == 0, envelope
    assert _plist(agents)["StartCalendarInterval"] == {"Hour": at[0], "Minute": at[1]}


@pytest.mark.parametrize(
    "text", ["24:00", "12:60", "3:7", "noon", "0300", "-1:30", "03:15:00", "", "003:15"]
)
def test_a_time_that_is_not_hh_mm_is_a_usage_error_and_writes_nothing(mac, agents, text):
    code, _envelope = drive(["schedule", "install", "--at", text])

    assert code == int(ExitCode.USAGE)
    assert not agents.exists()
    assert mac.calls == []


def test_the_agent_carries_a_fixed_path_the_resolved_directories_and_nothing_else(
    mac, agents, crate, monkeypatch
):
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_PROVIDER_TOKEN", "a-secret-value")
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", "/opt/tools/ffmpeg")
    monkeypatch.setenv("CRATEKIT_BIN_SH", "/bin/sh")
    monkeypatch.setenv("CRATEKIT_PROVIDER_CALLS", "99999")
    monkeypatch.setenv("A_PERSONAL_SETTING", "kept-at-home")
    monkeypatch.setenv("PATH", "/a/persons/own/path")
    monkeypatch.setenv(config.ENV_DOWNLOAD_STAGING, "")

    drive(["schedule", "install"])

    env = _plist(agents)["EnvironmentVariables"]
    set_here = {name for name in schedule.override_names() if os.environ.get(name)}
    assert set(env) == {
        "PATH", config.ENV_CONFIG_DIR, config.ENV_STATE_DIR, config.ENV_PROVIDER_GATE_DIR,
        "CRATEKIT_BIN_FFMPEG", *set_here,
    }
    assert set(env) <= schedule.allowed_names()
    assert env["CRATEKIT_BIN_FFMPEG"] == "/opt/tools/ffmpeg"
    assert "CRATEKIT_BIN_SH" not in env, "an override for a binary this build never runs"
    assert "CRATEKIT_PROVIDER_CALLS" not in env, "a raised limit is never carried"
    assert env[config.ENV_STATE_DIR] == str(config.installation_state_dir())
    assert env[config.ENV_CONFIG_DIR] == str(config.config_dir())
    assert env[config.ENV_PROVIDER_GATE_DIR] == str(config.provider_gate_dir())
    assert config.ENV_DOWNLOAD_STAGING not in env, "an empty override is not carried"
    assert "A_PERSONAL_SETTING" not in env
    assert not any("CREDENTIAL" in name for name in env)
    assert "a-secret-value" not in (agents / schedule.PLIST_NAME).read_text()
    path = env["PATH"].split(os.pathsep)
    assert path[0] == str(crate.parent)
    for fallback in binaries.fallback_dirs():
        assert str(fallback) in path, "the binaries' own directories are on the agent's PATH"
    assert "/a/persons/own/path" not in path
    assert path[-4:] == ["/usr/bin", "/bin", "/usr/sbin", "/sbin"]


def test_an_installation_found_through_xdg_alone_is_the_one_the_agent_reads(
    mac, agents, monkeypatch, tmp_path
):
    """Review round one, finding 1: with no Cratekit override set, the night
    must still resolve the configuration and state the install resolved."""
    for name in schedule.carried_names():
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg-state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg-config"))
    state, conf, gate = config.installation_state_dir(), config.config_dir(), config.provider_gate_dir()

    code, envelope = drive(["schedule", "install"])

    assert code == 0, envelope
    document = _plist(agents)
    env = document["EnvironmentVariables"]
    assert env[config.ENV_STATE_DIR] == str(state)
    assert env[config.ENV_CONFIG_DIR] == str(conf)
    assert env[config.ENV_PROVIDER_GATE_DIR] == str(gate)
    assert Path(document["StandardOutPath"]).is_relative_to(state)
    # The agent's own environment, with no XDG variable and another HOME,
    # resolves to the same directories.
    for name in ("XDG_STATE_HOME", "XDG_CONFIG_HOME"):
        monkeypatch.delenv(name)
    monkeypatch.setenv("HOME", str(tmp_path / "elsewhere"))
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    assert (config.installation_state_dir(), config.config_dir(), config.provider_gate_dir()) == (
        state, conf, gate,
    )


def test_a_relative_override_is_carried_absolute(mac, agents, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(config.ENV_STATE_DIR, os.path.join("scratch", "state"))
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, "library")
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", os.path.join("tools", "ffmpeg"))

    code, envelope = drive(["schedule", "install"])

    assert code == 0, envelope
    document = _plist(agents)
    env = document["EnvironmentVariables"]
    assert env[config.ENV_STATE_DIR] == str(tmp_path / "scratch" / "state")
    assert env[config.ENV_LIBRARY_ROOT] == str(tmp_path / "library")
    assert env["CRATEKIT_BIN_FFMPEG"] == str(tmp_path / "tools" / "ffmpeg")
    assert document["StandardOutPath"] == str(
        tmp_path / "scratch" / "state" / "schedule" / "sync-night.log"
    )


def test_a_bootstrap_that_fails_is_refused_in_its_words_and_leaves_nothing(mac, agents):
    mac.fail["bootstrap"] = schedule.Answer(5, "Bootstrap failed: 5: Input/output error")

    code, envelope = drive(["schedule", "install"])

    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "schedule-launchctl-failed"
    assert "Bootstrap failed: 5: Input/output error" in cause["message"]
    assert "nothing is installed" in cause["message"]
    assert not (agents / schedule.PLIST_NAME).exists()
    assert schedule.LABEL not in mac.loaded


def test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing(
    mac, agents, monkeypatch
):
    def forgetful(*args):
        answer = mac(*args)
        if args[0] == "bootstrap":
            mac.loaded.clear()
        return answer

    monkeypatch.setattr(schedule, "launchctl", forgetful)

    code, envelope = drive(["schedule", "install"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-launchctl-failed"
    assert not (agents / schedule.PLIST_NAME).exists()


def test_a_failed_replace_says_the_earlier_schedule_is_gone_too(mac, agents):
    drive(["schedule", "install"])
    mac.fail["bootstrap"] = schedule.Answer(5, "Bootstrap failed: 5: Input/output error")

    code, envelope = drive(["schedule", "install", "--at", "01:00"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "installed before it was removed too" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["replaced"] is True
    assert not (agents / schedule.PLIST_NAME).exists()
    assert schedule.LABEL not in mac.loaded


def test_an_agent_launchd_will_not_let_go_of_is_not_replaced(mac, agents):
    drive(["schedule", "install"])
    before = (agents / schedule.PLIST_NAME).read_bytes()
    mac.stuck = True

    code, envelope = drive(["schedule", "install", "--at", "01:00"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-launchctl-failed"
    assert (agents / schedule.PLIST_NAME).read_bytes() == before
    assert mac.verbs().count("bootstrap") == 1


def _roots(tmp_path: Path) -> tuple[Path, ...]:
    """Every root a verb could write under: the test's own directory, and the
    installation's state and configuration, which the suite puts beside it."""
    return (tmp_path, config.installation_state_dir(), config.config_dir())


def test_install_writes_only_the_plist_and_the_logs_directory(mac, agents, tmp_path):
    state = config.installation_state_dir()
    before = _tree(*_roots(tmp_path))

    drive(["schedule", "install"])

    after = _tree(*_roots(tmp_path))
    added = sorted(set(after) - set(before))
    plist = str(agents / schedule.PLIST_NAME)
    assert plist in added
    assert any(Path(path).is_relative_to(state) for path in added), "the walk saw the state"
    for path in added:
        if path == plist:
            continue
        relative = Path(path).relative_to(state)
        # The staging lock, held around the bootout, and the dispatcher's own
        # record of the run, which every verb leaves.
        assert relative == Path("staging.lock") or (
            relative.parent == Path("runs") and relative.suffix == ".json"
        ), path
    assert config.state_path(schedule.LOG_KEY).parent.is_dir()


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------


def _show(expect: int = 0) -> dict[str, Any]:
    code, envelope = drive(["schedule", "show"])
    assert code == expect, envelope
    return envelope


FAILED_SHOW = int(ExitCode.PRECONDITION)


def test_show_reads_an_installed_loaded_agent(mac, crate):
    drive(["schedule", "install", "--at", "02:45"])

    summary = _show()["data"]["summary"]["schedule"]

    assert summary["installed"] is True and summary["loaded"] == schedule.LOADED
    assert summary["at"] == "02:45" and summary["crate"] == str(crate)
    assert summary["runs_the_night"] is True
    assert "PATH" in summary["environment"]


def test_show_reads_an_installed_agent_launchd_does_not_hold(mac):
    drive(["schedule", "install"])
    mac.loaded.clear()

    envelope = _show()

    assert envelope["data"]["summary"]["schedule"]["loaded"] == schedule.NOT_LOADED
    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert rows["schedule.loaded"]["status"] == "warn"


def test_show_over_nothing_installed(mac, agents):
    summary = _show()["data"]["summary"]["schedule"]

    assert summary["installed"] is False and summary["loaded"] == schedule.NOT_LOADED
    assert summary["at"] is None and summary["crate"] is None
    assert not agents.exists()


def test_show_never_reads_launchd_it_cannot_read_as_not_loaded(mac):
    drive(["schedule", "install"])
    mac.fail["print"] = schedule.Answer(1, "launchctl: no such domain")

    envelope = _show()

    assert envelope["data"]["summary"]["schedule"]["loaded"] == schedule.UNKNOWN
    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert "no such domain" in rows["schedule.loaded"]["detail"]


def test_show_says_a_plist_it_cannot_read_never_reads_it_as_absent(mac, agents):
    agents.mkdir(parents=True)
    (agents / schedule.PLIST_NAME).write_bytes(b"\x00 not a plist")

    envelope = _show(FAILED_SHOW)

    assert envelope["cause"]["reason"] == "schedule-agent-unusable"
    summary = envelope["data"]["summary"]["schedule"]
    assert summary["installed"] is False and summary["unreadable"]
    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert rows["schedule.agent"]["status"] == "fail"


def test_show_says_an_agent_that_runs_anything_but_the_night(mac, agents, crate):
    agents.mkdir(parents=True)
    tampered = schedule.agent(crate, (3, 17), Path("/tmp/x.log"), {"PATH": "/usr/bin"})
    tampered["ProgramArguments"] = [str(crate), "sync", "land", "-d", "intake.land.apply=go"]
    (agents / schedule.PLIST_NAME).write_bytes(plistlib.dumps(tampered))

    envelope = _show(FAILED_SHOW)

    assert envelope["cause"]["reason"] == "schedule-agent-unusable"
    assert envelope["data"]["summary"]["schedule"]["runs_the_night"] is False
    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert rows["schedule.crate"]["status"] == "fail"


def test_show_says_an_agent_with_a_key_the_template_does_not_hold(mac, agents, crate):
    agents.mkdir(parents=True)
    widened = schedule.agent(crate, (3, 17), Path("/tmp/x.log"), {"PATH": "/usr/bin"})
    widened["KeepAlive"] = True
    (agents / schedule.PLIST_NAME).write_bytes(plistlib.dumps(widened))

    assert _show(FAILED_SHOW)["data"]["summary"]["schedule"]["runs_the_night"] is False


def test_show_carries_the_last_nights_line(mac):
    firing = sync_night._Firing(night="2026-11-21", started=sync_night._clock(), run_id="r1")
    assert sync_night._write_status(firing.record(sync_night.NOTHING, "nothing new tonight")) is None

    envelope = _show()

    assert envelope["data"]["summary"]["schedule"]["last"] == "nothing new tonight"


def test_show_says_a_night_record_it_cannot_read(mac):
    path = sync_night.status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")

    envelope = _show()

    rows = {row["key"]: row for row in envelope["data"]["checks"]}
    assert rows["schedule.last"]["status"] == "warn"
    assert "cannot be read" in rows["schedule.last"]["detail"]


def test_show_writes_nothing_and_asks_launchd_only_to_print(mac, tmp_path):
    drive(["schedule", "install"])
    lock = config.state_path("staging_lock")
    lock.unlink(missing_ok=True)
    before = {k: v for k, v in _tree(*_roots(tmp_path)).items() if "/runs/" not in k}
    mac.calls.clear()

    _show()

    after = {k: v for k, v in _tree(*_roots(tmp_path)).items() if "/runs/" not in k}
    assert after == before
    assert not lock.exists(), "show took the staging lock"
    assert set(mac.verbs()) == {"print"}


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------


def test_remove_boots_the_agent_out_and_deletes_its_plist(mac, agents):
    drive(["schedule", "install"])

    code, envelope = drive(["schedule", "remove"])

    assert code == 0, envelope
    assert envelope["outcome"] == "ok"
    assert not (agents / schedule.PLIST_NAME).exists()
    assert schedule.LABEL not in mac.loaded
    assert ("bootout", SERVICE) in mac.calls


def test_remove_over_nothing_installed_is_a_no_op(mac, agents):
    code, envelope = drive(["schedule", "remove"])

    assert code == 0, envelope
    assert envelope["outcome"] == "no_op"
    assert "bootout" not in mac.verbs()
    assert not agents.exists()


def test_remove_deletes_a_plist_launchd_does_not_hold(mac, agents):
    drive(["schedule", "install"])
    mac.loaded.clear()

    code, envelope = drive(["schedule", "remove"])

    assert code == 0 and envelope["outcome"] == "ok"
    assert not (agents / schedule.PLIST_NAME).exists()


def test_remove_boots_out_an_agent_whose_plist_is_gone(mac, agents):
    drive(["schedule", "install"])
    (agents / schedule.PLIST_NAME).unlink()

    code, envelope = drive(["schedule", "remove"])

    assert code == 0 and envelope["outcome"] == "ok"
    assert schedule.LABEL not in mac.loaded


@pytest.mark.parametrize("how", ["stuck", "bootout fails", "print unreadable"])
def test_a_remove_launchd_does_not_confirm_keeps_the_plist(mac, agents, how):
    drive(["schedule", "install"])
    if how == "stuck":
        mac.stuck = True
    elif how == "bootout fails":
        mac.fail["bootout"] = schedule.Answer(37, "Boot-out failed: 37: Operation already in progress")
    else:
        mac.fail["print"] = schedule.Answer(1, "launchctl: no such domain")

    code, envelope = drive(["schedule", "remove"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-launchctl-failed"
    assert (agents / schedule.PLIST_NAME).exists(), "the plist went while launchd may still hold it"


# ---------------------------------------------------------------------------
# Any platform but macOS
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("verb", ["install", "show", "remove"])
@pytest.mark.parametrize("running", ["linux", "win32"])
def test_any_platform_but_macos_refuses_naming_it(mac, agents, monkeypatch, verb, running):
    monkeypatch.setattr(schedule, "platform", lambda: running)

    code, envelope = drive(["schedule", verb])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-platform-unsupported"
    assert running in envelope["cause"]["message"]
    assert mac.calls == []
    assert not agents.exists()


# ---------------------------------------------------------------------------
# Review round one
# ---------------------------------------------------------------------------


def test_show_fails_over_an_agent_whose_crate_is_gone(mac, crate):
    """Finding 2: launchd cannot start a program that is not there."""
    drive(["schedule", "install"])
    crate.unlink()

    envelope = _show(FAILED_SHOW)

    assert envelope["cause"]["reason"] == "schedule-agent-unusable"
    assert "is not an executable file" in envelope["cause"]["message"]
    assert envelope["data"]["summary"]["schedule"]["runs_the_night"] is False


@pytest.mark.parametrize("verb", ["install", "show", "remove"])
def test_root_is_refused_and_launchd_is_never_asked(mac, agents, monkeypatch, verb):
    """Finding 5: ``gui/0`` is nobody's login."""
    monkeypatch.setattr(schedule, "uid", lambda: 0)

    code, envelope = drive(["schedule", verb])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert "never as root" in envelope["cause"]["message"]
    assert mac.calls == []
    assert not agents.exists()


@pytest.mark.parametrize("verb", ["install", "remove"])
def test_a_night_in_progress_is_never_booted_out(mac, agents, verb, tmp_path):
    """Finding 6: a night pass holds the staging lock for its whole run, and
    launchd's bootout would end it."""
    import subprocess

    drive(["schedule", "install"])
    mac.calls.clear()
    holder = subprocess.Popen(
        [sys.executable, "-c",
         "import sys, time\n"
         "from cratekit.core import staging_lock\n"
         "with staging_lock.held('crate sync night'):\n"
         "    print('held', flush=True); time.sleep(30)\n"],
        stdout=subprocess.PIPE, text=True, env=dict(os.environ),
    )
    try:
        assert holder.stdout.readline().strip() == "held"
        code, envelope = drive(["schedule", verb])
    finally:
        holder.kill()
        holder.wait()

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert envelope["cause"]["reason"] == "staging-held"
    assert "bootout" not in mac.verbs()
    assert schedule.LABEL in mac.loaded and (agents / schedule.PLIST_NAME).exists()


def test_a_replace_whose_write_fails_says_the_earlier_schedule_is_off(mac, agents, monkeypatch):
    """Finding 3: by the write, the earlier agent is booted out."""
    drive(["schedule", "install"])
    before = (agents / schedule.PLIST_NAME).read_bytes()

    def refused(payload, path, *, mode=0o600):
        raise PermissionError(13, "Permission denied", str(path))

    monkeypatch.setattr(config, "atomic_write_bytes", refused)

    code, envelope = drive(["schedule", "install", "--at", "01:00"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "schedule-agent-unwritten"
    assert "booted out and its plist kept" in envelope["cause"]["message"]
    assert (agents / schedule.PLIST_NAME).read_bytes() == before
    assert schedule.LABEL not in mac.loaded


def test_a_failed_load_launchd_may_still_hold_keeps_its_plist(mac, agents, monkeypatch):
    """Finding 4: the cleanup reads its own bootout before deleting."""
    def half(*args):
        if args[0] == "bootstrap":
            mac(*args)
            return schedule.Answer(5, "Bootstrap failed: 5: Input/output error")
        if args[0] == "bootout":
            mac.calls.append(args)
            return schedule.Answer(37, "Boot-out failed: 37: Operation already in progress")
        return mac(*args)

    monkeypatch.setattr(schedule, "launchctl", half)

    code, envelope = drive(["schedule", "install"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "launchd may still hold it, so its plist is kept" in envelope["cause"]["message"]
    assert (agents / schedule.PLIST_NAME).exists()
    assert schedule.LABEL in mac.loaded


def test_a_bootout_launchd_ignores_is_said_in_words_a_person_reads(mac):
    """Finding 8: never "launchctl answered 0" followed by the print dump."""
    drive(["schedule", "install"])
    mac.stuck = True

    code, envelope = drive(["schedule", "remove"])

    assert code == int(ExitCode.PRECONDITION), envelope
    message = envelope["cause"]["message"]
    assert "launchd still holds the agent after launchctl answered its bootout" in message
    assert "answered 0" not in message and "state =" not in message


def test_a_bootout_refused_over_an_agent_then_absent_boots_out_nothing(mac, agents, monkeypatch):
    """Finding 8: the first print unreadable, the bootout refused, the second
    print absent, with nothing installed: nothing was removed."""
    answers = iter([schedule.Answer(1, "launchctl: no such domain")])

    def flaky(*args):
        if args[0] == "print":
            nxt = next(answers, None)
            if nxt is not None:
                mac.calls.append(args)
                return nxt
        return mac(*args)

    monkeypatch.setattr(schedule, "launchctl", flaky)

    code, envelope = drive(["schedule", "remove"])

    assert code == 0, envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["schedule"]["removed"] is False


@pytest.mark.parametrize(
    "edit",
    [
        pytest.param(lambda d: d.update(RunAtLoad=True), id="run at load"),
        pytest.param(lambda d: d.pop("StartCalendarInterval"), id="no calendar"),
        pytest.param(lambda d: d.update(StartCalendarInterval={"Minute": 5}), id="every hour"),
        pytest.param(lambda d: d.update(StartCalendarInterval={"Hour": 99, "Minute": 0}), id="hour 99"),
        pytest.param(
            lambda d: d.update(StartCalendarInterval=[{"Hour": 3, "Minute": 0}, {"Hour": 4, "Minute": 0}]),
            id="two times",
        ),
        pytest.param(
            lambda d: d.update(StartCalendarInterval={"Hour": 3, "Minute": 0, "Weekday": 1}),
            id="one weekday",
        ),
        pytest.param(lambda d: d.update(Program="/bin/sh"), id="a program key"),
        pytest.param(
            lambda d: d.update(ProgramArguments=["/bin/sh", "sync", "night"]), id="another program"
        ),
        pytest.param(
            lambda d: d["EnvironmentVariables"].update(CRATEKIT_PROVIDER_CALLS="99999"),
            id="a raised limit",
        ),
        pytest.param(lambda d: d.update(StandardErrorPath="/tmp/elsewhere.log"), id="split log"),
    ],
)
def test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights(mac, agents, edit):
    """Finding 7: show judges what launchd will do, not only the arguments."""
    drive(["schedule", "install"])
    document = _plist(agents)
    edit(document)
    (agents / schedule.PLIST_NAME).write_bytes(plistlib.dumps(document))

    envelope = _show(FAILED_SHOW)

    assert envelope["cause"]["reason"] == "schedule-agent-unusable"
    assert envelope["data"]["summary"]["schedule"]["runs_the_night"] is False
    assert envelope["data"]["summary"]["schedule"]["problems"]


def test_show_reads_the_night_line_from_the_state_the_agent_carries(mac, monkeypatch, tmp_path):
    """Finding 7: a shell pointed at another state still reads the agent's night."""
    drive(["schedule", "install"])
    firing = sync_night._Firing(night="2026-11-21", started=sync_night._clock(), run_id="r1")
    assert sync_night._write_status(firing.record(sync_night.NOTHING, "the agent's own night")) is None
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "another-state"))

    envelope = _show()

    assert envelope["data"]["summary"]["schedule"]["last"] == "the agent's own night"


def test_show_fails_over_an_agent_launchd_holds_with_no_plist(mac, agents):
    drive(["schedule", "install"])
    (agents / schedule.PLIST_NAME).unlink()

    envelope = _show(FAILED_SHOW)

    assert "no plist is at" in envelope["cause"]["message"]
    assert envelope["data"]["summary"]["schedule"]["loaded"] == schedule.LOADED


# ---------------------------------------------------------------------------
# Review round two
# ---------------------------------------------------------------------------


def test_a_binary_the_install_finds_on_its_path_alone_is_on_the_agents_path(
    mac, agents, monkeypatch, tmp_path
):
    """Finding 3: the agent's PATH carries the directory the install found it in."""
    own = tmp_path / "own-tools"
    own.mkdir()
    tool = own / "keyfinder-cli"
    tool.write_text("#!/bin/sh\n")
    tool.chmod(0o755)
    monkeypatch.setenv("PATH", f"{own}{os.pathsep}/usr/bin{os.pathsep}/bin")
    monkeypatch.delenv(binaries.env_var("keyfinder-cli"), raising=False)

    drive(["schedule", "install"])

    path = _plist(agents)["EnvironmentVariables"]["PATH"].split(os.pathsep)
    assert str(own) in path


@pytest.mark.parametrize(
    "edit",
    [
        pytest.param(lambda d: d["ProgramArguments"].extend(["-d", "intake.land.native=go"]), id="an answer"),
        pytest.param(lambda d: d["ProgramArguments"].append(""), id="an empty word"),
        pytest.param(lambda d: d["EnvironmentVariables"].pop(config.ENV_STATE_DIR), id="no state"),
        pytest.param(lambda d: d["EnvironmentVariables"].pop(config.ENV_CONFIG_DIR), id="no config"),
        pytest.param(lambda d: d["EnvironmentVariables"].pop("PATH"), id="no path"),
        pytest.param(lambda d: d["EnvironmentVariables"].update({config.ENV_STATE_DIR: "state"}), id="relative state"),
        pytest.param(
            lambda d: d.update(StandardOutPath="/tmp/elsewhere.log", StandardErrorPath="/tmp/elsewhere.log"),
            id="log outside its state",
        ),
        pytest.param(lambda d: d.update(StandardOutPath="x.log", StandardErrorPath="x.log"), id="relative log"),
        pytest.param(lambda d: d.update(StartCalendarInterval={"Hour": 3, "Minute": 99}), id="minute 99"),
        pytest.param(lambda d: d.update(StartCalendarInterval={"Hour": True, "Minute": 0}), id="a true hour"),
    ],
)
def test_show_fails_over_an_agent_that_reads_another_installation_or_more_words(mac, agents, edit):
    drive(["schedule", "install"])
    document = _plist(agents)
    edit(document)
    (agents / schedule.PLIST_NAME).write_bytes(plistlib.dumps(document))

    envelope = _show(FAILED_SHOW)

    assert envelope["data"]["summary"]["schedule"]["problems"]


def test_show_never_prints_a_value_this_build_would_not_carry(mac, agents):
    """Finding 10: the name is a problem; its value is not echoed."""
    drive(["schedule", "install"])
    document = _plist(agents)
    document["EnvironmentVariables"]["CRATEKIT_CREDENTIAL_PROVIDER_SESSION"] = "a-session-secret"
    (agents / schedule.PLIST_NAME).write_bytes(plistlib.dumps(document))

    code, envelope = drive(["schedule", "show"])

    assert code == FAILED_SHOW
    assert "a-session-secret" not in str(envelope)
    assert any("CRATEKIT_CREDENTIAL_PROVIDER_SESSION" in p for p in envelope["data"]["summary"]["schedule"]["problems"])


def test_install_and_show_agree_on_the_environment_shape(mac):
    _code, installed = drive(["schedule", "install"])
    shown = _show()

    assert installed["data"]["summary"]["schedule"]["environment"] == (
        shown["data"]["summary"]["schedule"]["environment"]
    )
