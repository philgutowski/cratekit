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
from cratekit.core import config
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

    def __call__(self, *args: str) -> schedule.Answer:
        self.calls.append(args)
        verb = args[0]
        if verb in self.fail:
            return self.fail[verb]
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


def _calls_in(node: ast.AST) -> set[str]:
    named: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute):
            named.add(child.attr)
        elif isinstance(child, ast.Name):
            named.add(child.id)
    return named


def test_only_the_one_seam_starts_a_process():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    launchers = {"subprocess", "Popen", "system", "popen", "execv", "execvp", "execl",
                 "spawnv", "spawnl", "posix_spawn", "startfile", "fork"}
    seam = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "launchctl"
    )
    assert "subprocess" in _calls_in(seam)
    for node in tree.body:
        if node is seam:
            continue
        reached = _calls_in(node) & launchers
        assert not reached, f"{getattr(node, 'name', type(node).__name__)} names {reached}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] + [getattr(node, "module", None) or ""]
            assert "subprocess" not in modules or node in list(ast.walk(seam)), (
                "subprocess is imported outside the launchctl seam"
            )
    assert schedule.LAUNCHCTL == "/bin/launchctl"


def test_the_module_names_no_system_domain_and_no_system_directory():
    text = SOURCE.read_text(encoding="utf-8")
    for spelled in ("LaunchDaemons", '"/Library', "'/Library", "system/", "sudo"):
        assert spelled not in text, f"the schedule module spells {spelled!r}"
    assert schedule.launch_agents_dir.__code__ is not None
    assert schedule.NIGHT_ARGV == ("sync", "night")


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
    assert set(document) == schedule.PLIST_KEYS
    assert document["Label"] == schedule.LABEL
    assert document["ProgramArguments"] == [str(crate), "sync", "night"]
    assert document["StartCalendarInterval"] == {"Hour": 3, "Minute": 17}
    assert document["RunAtLoad"] is False
    log = config.state_path(schedule.LOG_KEY)
    assert document["StandardOutPath"] == document["StandardErrorPath"] == str(log)
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


@pytest.mark.parametrize("state", ["relative", "missing", "not executable"])
def test_a_crate_that_cannot_run_is_refused_and_nothing_is_written(
    mac, agents, crate, monkeypatch, state
):
    if state == "relative":
        found = Path("bin") / "crate"
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


@pytest.mark.parametrize("text", ["24:00", "12:60", "3:7", "noon", "0300", "-1:30", "03:15:00", ""])
def test_a_time_that_is_not_hh_mm_is_a_usage_error_and_writes_nothing(mac, agents, text):
    code, _envelope = drive(["schedule", "install", "--at", text])

    assert code == int(ExitCode.USAGE)
    assert not agents.exists()
    assert mac.calls == []


def test_the_agent_carries_a_fixed_path_and_the_overrides_and_nothing_else(
    mac, agents, crate, monkeypatch
):
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_PROVIDER_TOKEN", "a-secret-value")
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", "/opt/tools/ffmpeg")
    monkeypatch.setenv("A_PERSONAL_SETTING", "kept-at-home")
    monkeypatch.setenv("PATH", "/a/persons/own/path")
    monkeypatch.setenv(config.ENV_DOWNLOAD_STAGING, "")

    drive(["schedule", "install"])

    env = _plist(agents)["EnvironmentVariables"]
    allowed = {"PATH", *schedule.carried_names()}
    assert {name for name in env if not name.startswith("CRATEKIT_BIN_")} <= allowed
    assert env["CRATEKIT_BIN_FFMPEG"] == "/opt/tools/ffmpeg"
    assert env[config.ENV_STATE_DIR] == os.environ[config.ENV_STATE_DIR]
    assert config.ENV_DOWNLOAD_STAGING not in env, "an empty override is not carried"
    assert "A_PERSONAL_SETTING" not in env
    assert not any("CREDENTIAL" in name for name in env)
    assert "a-secret-value" not in plistlib.dumps(_plist(agents)).decode()
    path = env["PATH"].split(os.pathsep)
    assert path[0] == str(crate.parent)
    assert "/a/persons/own/path" not in path
    assert path[-4:] == list(schedule.SYSTEM_PATH)


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


def test_install_writes_only_the_plist_and_the_logs_directory(mac, agents, tmp_path):
    state = config.installation_state_dir()
    before = _tree(tmp_path)

    drive(["schedule", "install"])

    after = _tree(tmp_path)
    added = sorted(set(after) - set(before))
    plist = str(agents / schedule.PLIST_NAME)
    assert plist in added
    for path in added:
        assert path == plist or Path(path).is_relative_to(state), path


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
    before = _tree(tmp_path)
    mac.calls.clear()

    _show()

    assert _tree(tmp_path) == before
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
