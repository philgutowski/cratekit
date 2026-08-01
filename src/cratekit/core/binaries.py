"""Absolute-path resolution for the external binaries Cratekit shells out to.

WHY THIS EXISTS. A desktop app launched from a graphical file manager inherits a
minimal PATH: none of the directories a package manager installs into are on it.
So a bare-name subprocess call that works in a login shell fails inside the
packaged app, and it fails as "yt-dlp: command not found" deep inside a download,
naming nothing that would help. Every subprocess call site resolves its binary
through here instead.

TWO THINGS THE PORT CHANGES, both from a defect found in the source system.

**1. A missing binary is not a process exit.** The source system's exception
subclasses ``SystemExit``, so raising it terminates the process with the message
as the payload. That is one of three unrelated exit vocabularies KTD25 says to
unify: a foundation module that can end the process removes any chance for a
caller to catch, classify, and report the failure with its own remediation. Here
it is an ordinary exception.

**2. A platform binary is a different kind of missing.** The source system
resolves one binary that ships with the operating system and has no install
command at all. Its non-raising probe degrades gracefully, so no crash results,
but the raising path would have produced "install <it> and put it on PATH",
which is wrong and unactionable for something the platform owns. Platform
binaries are a separate category here, with a message that says the truth: this
should already be present, and its absence means something else.

THE CONTRACT ASYMMETRY IS DELIBERATE. ``find`` returns None for a broken
override; ``resolve`` raises for it. ``find`` is doctor's probe and must report
on every binary in one pass without aborting on the first one.

No filesystem side effects at import, same rule as the config module.
"""

from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from cratekit.core import secrets

#: Every platform the tables below answer for. Named so an audit can walk them
#: rather than checking only whichever one it happens to be running on.
SUPPORTED_PLATFORMS: tuple[str, ...] = ("darwin", "linux", "win32")

#: Directories a graphical launcher does not put on PATH, per platform. R1 keeps
#: the code portable, so this is a table lookup rather than a constant: the
#: source system's list is macOS-only, and hardcoding it makes the Windows
#: adapter a rewrite rather than a row.
_FALLBACK_DIRS_BY_PLATFORM: dict[str, tuple[str, ...]] = {
    "darwin": ("/opt/homebrew/bin", "/usr/local/bin", "~/.local/bin"),
    "linux": ("/usr/local/bin", "~/.local/bin", "~/bin"),
    "win32": (),
}


def fallback_dirs() -> tuple[Path, ...]:
    """The extra directories to probe, expanded, for the running platform."""
    raw = _FALLBACK_DIRS_BY_PLATFORM.get(sys.platform, ("/usr/local/bin", "~/.local/bin"))
    return tuple(Path(entry).expanduser() for entry in raw)


class PackageManager(StrEnum):
    """Where a binary comes from, as a TOKEN rather than a command line (D2).

    The module in the same unit that got this right says it verbatim:
    ``profiles.install_command`` returns the extras NAME, not a command, "because
    this layer must not contain the text a user types". The same argument holds
    here and the cost of ignoring it is concrete. A rendered command line baked in
    below the CLI takes three choices away from the layer that can actually make
    them: which package manager the user really has, whether the interface is a
    terminal at all, and whether to link to instructions instead.
    """

    HOMEBREW = "homebrew"
    APT = "apt"
    PIPX = "pipx"
    FROM_SOURCE = "from-source"


@dataclass(frozen=True, slots=True)
class InstallHint:
    """What to install and where from. Data, not a sentence.

    ``packages`` is a tuple because one binary can need two of them, and two
    package names is still data; "A && B" would be a shell fragment, which is the
    thing this type exists to stop.
    """

    manager: PackageManager
    packages: tuple[str, ...]


#: Where each user-installable binary comes from, per platform. A hint that names
#: the wrong package manager is worse than no hint: it sends the user to a
#: command that fails for a second, unrelated reason. Platforms with no answer are
#: absent rather than guessed.
_INSTALL_HINTS: dict[str, dict[str, InstallHint]] = {
    "yt-dlp": {
        "darwin": InstallHint(PackageManager.HOMEBREW, ("yt-dlp",)),
        "linux": InstallHint(PackageManager.PIPX, ("yt-dlp",)),
    },
    "ffmpeg": {
        "darwin": InstallHint(PackageManager.HOMEBREW, ("ffmpeg",)),
        "linux": InstallHint(PackageManager.APT, ("ffmpeg",)),
    },
    "ffprobe": {
        "darwin": InstallHint(PackageManager.HOMEBREW, ("ffmpeg",)),
        "linux": InstallHint(PackageManager.APT, ("ffmpeg",)),
    },
    "rclone": {
        "darwin": InstallHint(PackageManager.HOMEBREW, ("rclone",)),
        "linux": InstallHint(PackageManager.APT, ("rclone",)),
    },
    "keyfinder-cli": {
        "darwin": InstallHint(PackageManager.HOMEBREW, ("libkeyfinder", "keyfinder-cli")),
        "linux": InstallHint(PackageManager.FROM_SOURCE, ("keyfinder-cli",)),
    },
}

#: Every binary a user can install themselves. Derived from the table above so the
#: two cannot drift, and named so an audit can walk the whole table.
INSTALLABLE_BINARIES: tuple[str, ...] = tuple(_INSTALL_HINTS)

#: Binaries the operating system provides. They have no install command, and
#: telling a user to install one is a dead end. Their absence means the platform
#: is not the one we think it is, so the message says that instead.
PLATFORM_BINARIES: frozenset[str] = frozenset({"caffeinate"})

ENV_PREFIX = "CRATEKIT_BIN_"


class Remedy(StrEnum):
    """What to do about a missing binary, as a TOKEN rather than a command.

    D2 removed the shell command strings from this module, which was right, and
    left every failure here raising one undifferentiated signature. Four
    situations reach ``BinaryNotFound``, and each needs a different sentence from
    the CLI:

    * an override the user set points at something that is not executable, so
      the answer is to fix or unset that one variable and nothing else;
    * the operating system owns the binary, so there is nothing to install and
      its absence means this is not the platform it ships with;
    * the user installs it and this table knows where from, so the CLI renders
      the hint into a command line for the package manager they actually have;
    * the user installs it and this table has NO row for their platform, so the
      honest answer names the binary and stops, rather than guessing a package
      manager and sending them to a command that fails for a second reason.

    Without a token a caller separates those by matching on the message text,
    which is the KTD25 failure this vocabulary exists to prevent. ``config.py``
    and ``secrets.py`` grew the same enum in the same pass; these are this
    module's contribution to the reservation U5 owns (S4), not a rival scheme.
    """

    FIX_BINARY_OVERRIDE = "fix-binary-override"
    UNSUPPORTED_PLATFORM = "unsupported-platform"
    INSTALL_BINARY = "install-binary"
    INSTALL_BINARY_SOURCE_UNKNOWN = "install-binary-source-unknown"


class BinaryNotFound(Exception):
    """A required external binary is missing, or its override points at nothing.

    Ordinary exception, NOT a ``SystemExit``. See the module docstring: a
    foundation-layer failure that ends the process cannot be caught, classified,
    or reported by the layer that knows what the user was trying to do.

    Carries TWO structured pieces, and they answer different questions.
    ``remedy`` says which KIND of failure this is, so a caller can branch without
    reading the message. ``hint`` says what to install and where from, and is
    None whenever installing is not the remediation at all, which is an answer
    rather than a gap. The command line stays with the CLI (D2).
    """

    def __init__(
        self,
        message: str,
        *,
        binary: str,
        remedy: Remedy,
        hint: InstallHint | None = None,
    ) -> None:
        super().__init__(message)
        self.binary = binary
        self.remedy = remedy
        self.hint = hint


def env_var(name: str) -> str:
    """The per-binary override variable, for example ``CRATEKIT_BIN_YT_DLP``."""
    return ENV_PREFIX + name.upper().replace("-", "_")


def _executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def find(name: str) -> str | None:
    """Absolute path for ``name``, or None. NEVER raises.

    Resolution order, first hit wins: the per-binary override, then the caller's
    PATH, then the fallback directories. A set-but-broken override returns None
    here rather than falling through to PATH, because silently using a different
    binary than the one the user named is worse than finding none.
    """
    override = os.environ.get(env_var(name))
    if override:
        return override if _executable(Path(override)) else None
    hit = shutil.which(name)
    if hit:
        return hit
    for directory in fallback_dirs():
        candidate = directory / name
        if _executable(candidate):
            return str(candidate)
    return None


def resolve(name: str) -> str:
    """Absolute path for ``name``, or ``BinaryNotFound`` naming what to do."""
    override = os.environ.get(env_var(name))
    if override and not _executable(Path(override)):
        raise BinaryNotFound(
            f"{env_var(name)} is set to {override!r}, which is not an executable "
            f"file. Fix or unset the override; falling through to PATH would run "
            f"a different binary than the one you named.",
            binary=name,
            remedy=Remedy.FIX_BINARY_OVERRIDE,
        )
    hit = find(name)
    if hit:
        return hit

    checked = ", ".join([env_var(name), "PATH", *(str(d) for d in fallback_dirs())])
    if name in PLATFORM_BINARIES:
        raise BinaryNotFound(
            f"{name} is provided by the operating system and was not found "
            f"(checked {checked}). There is nothing to install; its absence means "
            f"this is not the platform it ships with.",
            binary=name,
            remedy=Remedy.UNSUPPORTED_PLATFORM,
        )
    # The message STATES what happened and where it looked. What to do about it
    # travels as `remedy` and `hint`, and the CLI renders those into whatever a
    # command looks like from where the user is standing (D2).
    #
    # No hint means this table has no row for this platform, which is a DIFFERENT
    # remediation from "install it, here is where from": the CLI can name the
    # binary and stop instead of guessing a package manager the user may not
    # have. Leaving both cases on one token would push that distinction back into
    # a None-check on a second attribute.
    hint = install_hint(name)
    raise BinaryNotFound(
        f"{name} was not found (checked {checked}).",
        binary=name,
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,
        hint=hint,
    )


def install_hint(name: str, *, platform: str | None = None) -> InstallHint | None:
    """Where ``name`` comes from on this platform, as data. None when there is none.

    None is an ANSWER, not a gap, and it covers two different cases the CLI
    renders differently: a binary the operating system provides, where "install
    it" is not the remediation at all, and a platform this table has no answer
    for, where guessing a package manager would send the user to a command that
    fails for an unrelated reason.

    ``platform`` is a parameter so an audit can walk every row rather than only
    the row for the machine it happens to be running on.
    """
    if name in PLATFORM_BINARIES:
        return None
    return _INSTALL_HINTS.get(name, {}).get(sys.platform if platform is None else platform)


def subprocess_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """The environment with the fallback directories prepended to PATH.

    Spawned jobs get this so their own children resolve too: a downloader that
    invokes an encoder by name is a second lookup, in a process this code never
    touches, and it fails the same way for the same reason.

    Opted-in environment credentials are STRIPPED. The secrets module names the
    risk it guards against as a credential the user discovers "after it leaks into
    a process listing", and this is the exact hop where that would happen: the
    binaries on the other side are third parties Cratekit does not control, and
    none of them has any use for a Cratekit credential. Opting the fallback in
    means Cratekit may read a credential from its own environment; it does not
    mean yt-dlp, ffmpeg, and rclone each get a copy.
    """
    env = {
        key: value
        for key, value in (os.environ if base is None else base).items()
        if not key.startswith(secrets.ENV_CREDENTIAL_PREFIX)
    }
    parts = [str(d) for d in fallback_dirs()]
    for piece in env.get("PATH", "").split(os.pathsep):
        if piece and piece not in parts:
            parts.append(piece)
    env["PATH"] = os.pathsep.join(parts)
    return env


__all__ = [
    "ENV_PREFIX",
    "INSTALLABLE_BINARIES",
    "PLATFORM_BINARIES",
    "SUPPORTED_PLATFORMS",
    "BinaryNotFound",
    "InstallHint",
    "PackageManager",
    "Remedy",
    "env_var",
    "fallback_dirs",
    "find",
    "install_hint",
    "resolve",
    "subprocess_env",
]
