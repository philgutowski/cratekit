"""U2: external binary resolution, and the lint that keeps every call site honest.

The failure this module exists for is specific: an app launched from a graphical
file manager inherits a minimal PATH with none of the directories a package
manager installs into. A bare-name subprocess call that works in a login shell
fails inside the packaged app, deep inside a download, naming nothing useful.

Two of the tests here are about the PORT rather than the port's source, and both
come from a defect found in the original:

* ``BinaryNotFound`` is an ordinary exception, not a ``SystemExit``. The source
  system's version terminates the process, so no caller ever gets to classify the
  failure or attach what the user was actually doing (KTD25).
* A binary the operating system provides is a different kind of missing from one
  the user installs. The source system resolves one such binary with no install
  hint at all; asking a user to install it would be unactionable advice about
  something they cannot install.

The last test is the ported lint, widened. The original covered four binary names
and missed two, and the two it missed are the ones nobody thinks about, which is
exactly why they drift back to bare names.
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
    """Falling through would run a DIFFERENT binary than the one the user named.

    Silently using something else is worse than finding nothing, because the run
    appears to work and produces output nobody can account for.
    """
    _make_executable(tmp_path, "ffmpeg")
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(tmp_path / "missing"))
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve("ffmpeg")
    assert binaries.env_var("ffmpeg") in str(excinfo.value)


def test_find_never_raises_because_doctor_reports_on_all_of_them(monkeypatch, tmp_path):
    """The contract asymmetry, and why it is deliberate.

    ``find`` is doctor's probe. It has to report every binary in one pass, so
    aborting on the first missing one would hide the rest.
    """
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var("keyfinder-cli"), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    assert binaries.find("keyfinder-cli") is None
    monkeypatch.setenv(binaries.env_var("keyfinder-cli"), str(tmp_path / "missing"))
    assert binaries.find("keyfinder-cli") is None


def test_a_missing_binary_does_not_end_the_process():
    """KTD25: a foundation failure that exits cannot be caught or classified.

    The source system's exception subclasses ``SystemExit``, so raising it ends
    the process with the message as the payload and the layer that knows what the
    user was trying to do never sees it.
    """
    assert not issubclass(binaries.BinaryNotFound, SystemExit)
    assert issubclass(binaries.BinaryNotFound, Exception)


def test_a_missing_user_installable_binary_carries_a_structured_remedy(
    monkeypatch, tmp_path
):
    """D2: the remedy travels as data, and the CLI renders the command line.

    The module next to this one in the same unit already models this correctly and
    says so verbatim: ``profiles.install_command`` returns the extras NAME rather
    than a command line, "because this layer must not contain the text a user
    types". A hint baked into a string here takes that choice away from the CLI,
    which is the layer that knows the platform, the package manager the user
    actually has, and whether it is even talking to a terminal.
    """
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var("ffmpeg"), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    monkeypatch.setattr(sys, "platform", "darwin")

    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve("ffmpeg")

    assert "ffmpeg" in str(excinfo.value)
    hint = excinfo.value.hint
    assert hint == binaries.InstallHint(
        manager=binaries.PackageManager.HOMEBREW, packages=("ffmpeg",)
    )


def test_no_install_hint_spells_out_a_command_line():
    """The whole table, not just the one the resolver happened to reach.

    A single rendered command that survives anywhere in the table is a command
    the CLI cannot override, so the audit walks every platform of every binary.
    """
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
    """The defect the port fixes.

    The source system resolves a binary the operating system provides, and its
    raising path would produce "install <it> and put it on PATH". That is advice
    about something the user cannot install, for a problem that means something
    else entirely.
    """
    name = sorted(binaries.PLATFORM_BINARIES)[0]
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var(name), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))

    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve(name)
    message = str(excinfo.value)
    assert "provided by the operating system" in message
    assert excinfo.value.hint is None
    assert binaries.install_hint(name) is None


# ── KTD25: the three failures here are three failures, not one ───────────────


def _resolve_missing(monkeypatch, tmp_path, name: str):
    """Drive ``resolve`` to its raising path for ``name`` and return the exception."""
    monkeypatch.setenv("PATH", "/nonexistent")
    monkeypatch.delenv(binaries.env_var(name), raising=False)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (tmp_path,))
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve(name)
    return excinfo.value


def _unplaceable(monkeypatch, tmp_path, name: str = "ffmpeg"):
    """A user-installable binary the hint table has no row for on this platform.

    The row is emptied rather than ``sys.platform`` being patched to one that has
    no row. Patching the platform name reaches into ``shutil.which``, which takes
    a Windows-only branch on the string alone and then fails on the missing
    Windows API: the test would be asserting something about the standard
    library rather than about this module.
    """
    monkeypatch.setitem(binaries._INSTALL_HINTS, name, {})
    return _resolve_missing(monkeypatch, tmp_path, name)


def test_the_binary_failures_carry_four_different_remedies(monkeypatch, tmp_path):
    """One signature for four situations forces the caller back to string matching.

    D2 removed the shell command strings from this module, which was right, and
    left every raise here indistinguishable. A broken override, a binary the
    operating system owns, a binary this table can place, and a binary it cannot
    place on this platform need four different sentences from the CLI, and the
    only thing that made them separable was the message text. That is exactly the
    failure KTD25 exists to prevent, and the two sibling modules in this unit
    already grew a remedy enum for it.
    """
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(tmp_path / "missing"))
    broken_override = None
    with pytest.raises(binaries.BinaryNotFound) as excinfo:
        binaries.resolve("ffmpeg")
    broken_override = excinfo.value
    monkeypatch.delenv(binaries.env_var("ffmpeg"), raising=False)

    platform_owned = _resolve_missing(
        monkeypatch, tmp_path, sorted(binaries.PLATFORM_BINARIES)[0]
    )
    monkeypatch.setattr(sys, "platform", "darwin")
    installable = _resolve_missing(monkeypatch, tmp_path, "ffmpeg")
    # Installable, but the table has no row for this platform: there is nothing
    # honest to say about where from.
    unplaceable = _unplaceable(monkeypatch, tmp_path)

    assert broken_override.remedy is binaries.Remedy.FIX_BINARY_OVERRIDE
    assert platform_owned.remedy is binaries.Remedy.UNSUPPORTED_PLATFORM
    assert installable.remedy is binaries.Remedy.INSTALL_BINARY
    assert unplaceable.remedy is binaries.Remedy.INSTALL_BINARY_SOURCE_UNKNOWN

    remedies = {
        broken_override.remedy,
        platform_owned.remedy,
        installable.remedy,
        unplaceable.remedy,
    }
    assert len(remedies) == 4, "collapsed remedies force callers back to string matching"


def test_a_binary_remedy_is_a_token_and_not_the_command_a_user_types():
    """D2 again. The token names the KIND of answer; the CLI writes the sentence."""
    for remedy in binaries.Remedy:
        assert " " not in remedy.value
        assert "crate " not in remedy.value
        assert not re.search(r"\b(?:brew|apt|pipx|pip|sudo)\b", remedy.value)


def test_a_missing_binary_carries_a_remedy_even_when_it_carries_no_hint(
    monkeypatch, tmp_path
):
    """None for ``hint`` is an answer, and it must not be the ONLY answer.

    Two different failures produce no hint: a binary the platform owns, where
    installing is not the remediation at all, and a binary the user installs that
    this table cannot place on their platform. Leaving them to share one signature
    means the caller decides between "your platform is wrong" and "install this
    yourself" by re-deriving what the resolver already knew.
    """
    platform_owned = _resolve_missing(
        monkeypatch, tmp_path, sorted(binaries.PLATFORM_BINARIES)[0]
    )
    unplaceable = _unplaceable(monkeypatch, tmp_path)

    assert platform_owned.hint is None and unplaceable.hint is None
    assert platform_owned.remedy is not unplaceable.remedy


def test_a_spawned_process_does_not_inherit_an_opted_in_credential(monkeypatch):
    """``subprocess_env`` is the hop where a credential meets third-party binaries.

    The environment fallback is opt-in, and opting in means Cratekit may read a
    credential from its own environment. It does not mean yt-dlp, ffmpeg, and
    rclone should each receive a copy in a process listing, which is the exposure
    the secrets module names as the reason the fallback is opt-in at all.
    """
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_IDENTIFY_KEY", "value-from-the-env")
    monkeypatch.setenv("PATH", "/usr/bin")

    env = binaries.subprocess_env()

    assert "CRATEKIT_CREDENTIAL_IDENTIFY_KEY" not in env
    assert "value-from-the-env" not in "".join(env.values())


def test_the_fallback_directories_are_a_platform_table_not_a_constant():
    """R1: the code stays portable, so a Windows adapter is a row, not a rewrite.

    The source system's list is macOS-only and hardcoded, which is the shape that
    makes "add a platform" mean "rewrite the module".
    """
    assert isinstance(binaries.fallback_dirs(), tuple)
    if sys.platform == "win32":
        assert binaries.fallback_dirs() == ()
    else:
        assert binaries.fallback_dirs()


def test_spawned_processes_inherit_the_widened_path(monkeypatch):
    """A downloader invoking an encoder by name is a second lookup, in a process
    this code never touches. It fails the same way for the same reason."""
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: (Path("/opt/example/bin"),))

    parts = binaries.subprocess_env()["PATH"].split(os.pathsep)

    assert parts.index("/opt/example/bin") < parts.index("/usr/bin")
    assert parts.count("/usr/bin") == 1, "an existing PATH entry must not be duplicated"


# ═══════════════════════════════════════════════════════════════════════════
# The ported lint, widened
# ═══════════════════════════════════════════════════════════════════════════

#: Every binary the package shells out to. The source system's version of this
#: lint covered four names and silently missed two others that it also invokes.
#: A lint with a partial list is a lint that certifies the files it does not
#: check, so this list is the full set and grows with any new binary.
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
