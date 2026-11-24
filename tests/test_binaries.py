"""U2: external binary resolution, and the lint that keeps every call site honest.

An app launched from a file manager inherits a minimal PATH, so a bare-name call
fails there. ``BinaryNotFound`` is an ordinary exception, not ``SystemExit``
(KTD25), and the bare-name lint covers every binary the package runs.
"""

from __future__ import annotations

import os
import re
import stat
import sys
from pathlib import Path

import pytest

from cratekit.core import binaries

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"


def _make_executable(directory: Path, name: str) -> Path:
    path = directory / name
    path.write_text("#!/bin/sh\nexit 0\n")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _resolve_missing(monkeypatch, tmp_path, name: str):
    """Drive ``resolve`` to its raising path for ``name`` and return the exception."""
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var(name), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve(name)
    return excinfo.value


def _unplaceable(monkeypatch, tmp_path, name: str = "ffmpeg"):
    """A user-installable binary with its hint row emptied, rather than a patched
    ``sys.platform`` that tests the standard library."""
    monkeypatch.setitem(binaries._INSTALL_HINTS, name, {})
    return _resolve_missing(monkeypatch, tmp_path, name)


def test_a_binary_on_the_path_resolves(monkeypatch, tmp_path):
    exe = _make_executable(tmp_path, "yt-dlp")
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.delenv(binaries.env_var("yt-dlp"), raising=False)
    assert binaries.resolve("yt-dlp") == str(exe)


def test_a_binary_off_the_path_is_found_in_the_fallback_directories(monkeypatch, tmp_path):
    """The whole reason this module exists, in one test."""
    exe = _make_executable(tmp_path, "ffmpeg")
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var("ffmpeg"), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    assert binaries.resolve("ffmpeg") == str(exe)


def test_an_override_wins_over_the_path(monkeypatch, tmp_path):
    _make_executable(tmp_path, "ffmpeg")
    override = _make_executable(tmp_path, "ffmpeg-custom")
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(override))
    assert binaries.resolve("ffmpeg") == str(override)


def test_a_broken_override_is_an_explicit_error_not_a_fallthrough(monkeypatch, tmp_path):
    """Falling through would silently run a different binary than the one named."""
    _make_executable(tmp_path, "ffmpeg")
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(tmp_path / "missing"))
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve("ffmpeg")
    assert binaries.env_var("ffmpeg") in str(excinfo.value)


def test_find_never_raises_because_doctor_reports_on_all_of_them(monkeypatch, tmp_path):
    """``find`` is doctor's probe, reporting every binary in one pass."""
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var("keyfinder-cli"), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    assert binaries.find("keyfinder-cli") is None
    monkeypatch.setenv(binaries.env_var("keyfinder-cli"), str(tmp_path / "missing"))
    assert binaries.find("keyfinder-cli") is None


def test_a_missing_binary_does_not_end_the_process():
    """KTD25: a foundation failure that exits cannot be caught or classified."""
    assert not issubclass(binaries.BinaryNotFound, SystemExit)
    assert issubclass(binaries.BinaryNotFound, Exception)


def test_a_missing_user_installable_binary_carries_a_structured_remedy(
    monkeypatch, tmp_path
):
    """D2: the remedy travels as data, and the CLI, which knows the platform, renders it."""
    monkeypatch.setattr(sys, "platform", "darwin")
    error = _resolve_missing(monkeypatch, tmp_path, "ffmpeg")
    assert "ffmpeg" in str(error)
    assert error.hint == binaries.InstallHint(
        manager=binaries.PackageManager.HOMEBREW, packages=("ffmpeg",)
    )


def test_no_install_hint_spells_out_a_command_line():
    """Every platform of every binary: one rendered command is one the CLI cannot override."""
    for name in binaries.INSTALLABLE_BINARIES:
        for platform in binaries.SUPPORTED_PLATFORMS:
            hint = binaries.install_hint(name, platform=platform)
            if hint is None:
                continue
            assert isinstance(hint, binaries.InstallHint)
            for package in hint.packages:
                assert " " not in package, (
                    f"{name} on {platform} carries {package!r}, which is a command "
                    f"line rather than a package name"
                )


def test_a_missing_platform_binary_does_not_tell_the_user_to_install_it(
    monkeypatch, tmp_path
):
    """The defect the port fixes: no advice to install what the user cannot."""
    name = sorted(binaries.PLATFORM_BINARIES)[0]
    error = _resolve_missing(monkeypatch, tmp_path, name)
    assert "provided by the operating system" in str(error)
    assert error.hint is None
    assert binaries.install_hint(name) is None


def test_the_binary_failures_carry_four_different_remedies(monkeypatch, tmp_path):
    """KTD25: a broken override, a platform binary, a placeable and an unplaceable
    install need four sentences from the CLI, separable by more than message text.
    The platform binary and the unplaceable one carry no hint, so the remedy alone
    tells them apart."""
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(tmp_path / "missing"))
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve("ffmpeg")
    broken_override = excinfo.value
    monkeypatch.delenv(binaries.env_var("ffmpeg"), raising=False)

    platform_owned = _resolve_missing(
        monkeypatch, tmp_path, sorted(binaries.PLATFORM_BINARIES)[0]
    )
    monkeypatch.setattr(sys, "platform", "darwin")
    installable = _resolve_missing(monkeypatch, tmp_path, "ffmpeg")
    # Installable, but with no row for this platform: nothing honest to say about where from.
    unplaceable = _unplaceable(monkeypatch, tmp_path)

    assert broken_override.remedy is binaries.Remedy.FIX_BINARY_OVERRIDE
    assert platform_owned.remedy is binaries.Remedy.UNSUPPORTED_PLATFORM
    assert installable.remedy is binaries.Remedy.INSTALL_BINARY
    assert unplaceable.remedy is binaries.Remedy.INSTALL_BINARY_SOURCE_UNKNOWN
    assert platform_owned.hint is None and unplaceable.hint is None

    remedies = {
        broken_override.remedy,
        platform_owned.remedy,
        installable.remedy,
        unplaceable.remedy,
    }
    assert len(remedies) == 4, "collapsed remedies force callers back to string matching"


def test_a_binary_remedy_is_a_token_and_not_the_command_a_user_types():
    """D2: the token names the kind of answer; the CLI writes the sentence."""
    for remedy in binaries.Remedy:
        assert " " not in remedy.value
        assert "crate " not in remedy.value
        assert not re.search(r"\b(?:brew|apt|pipx|pip|sudo)\b", remedy.value)


def test_a_spawned_process_does_not_inherit_an_opted_in_credential(monkeypatch):
    """Opting in lets Cratekit read a credential, not hand it to every child it spawns."""
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_IDENTIFY_KEY", "value-from-the-env")
    monkeypatch.setenv("PATH", "/usr/bin")
    env = binaries.subprocess_env()
    assert "CRATEKIT_CREDENTIAL_IDENTIFY_KEY" not in env
    assert "value-from-the-env" not in "".join(env.values())


def test_the_fallback_directories_are_a_platform_table_not_a_constant():
    """R1: a new platform's adapter is a row, not a rewrite."""
    assert isinstance(binaries.fallback_dirs(), tuple)
    if sys.platform == "win32":
        assert binaries.fallback_dirs() == ()
    else:
        assert binaries.fallback_dirs()


def test_spawned_processes_inherit_the_widened_path(monkeypatch):
    """A downloader invoking an encoder by name is a second lookup, in a child process."""
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (Path("/opt/example/bin"),))
    parts = binaries.subprocess_env()["PATH"].split(os.pathsep)
    assert parts.index("/opt/example/bin") < parts.index("/usr/bin")
    assert parts.count("/usr/bin") == 1, "an existing PATH entry must not be duplicated"


# The ported lint, widened

#: Every binary the package shells out to; a partial list certifies what it never checks.
_LINTED_BINARIES = ("yt-dlp", "ffmpeg", "ffprobe", "tdn", "keyfinder-cli", "rclone", "caffeinate")

_BARE_ARGV = re.compile(r"""\[\s*["'](%s)["']""" % "|".join(map(re.escape, _LINTED_BINARIES)))


def bare_binary_argv(source: str) -> list[str]:
    """Return every line that starts an argv list with a bare binary name."""
    return [
        f"{number}: {line.strip()}"
        for number, line in enumerate(source.splitlines(), 1)
        if _BARE_ARGV.search(line)
    ]


def test_the_bare_argv_lint_catches_a_bare_name():
    assert bare_binary_argv('subprocess.run(["ffmpeg", "-i", path])\n')


def test_the_bare_argv_lint_allows_a_resolved_name():
    assert bare_binary_argv('subprocess.run([binaries.resolve("ffmpeg"), "-i", path])\n') == []


def test_no_module_invokes_an_external_binary_by_bare_name():
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.name == "binaries.py":
            continue  # the module that DEFINES the names
        for hit in bare_binary_argv(path.read_text()):
            offenders.append(f"{path.relative_to(SRC_ROOT)}:{hit}")
    assert not offenders, (
        "external binaries invoked by bare name:\n"
        + "\n".join(offenders)
        + "\nResolve them through cratekit.core.binaries; a bare name works in a "
        "login shell and fails inside a packaged app."
    )
