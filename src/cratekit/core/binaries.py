"""Absolute-path resolution for the external binaries Cratekit shells out to.

A desktop app launched from a graphical file manager inherits a minimal PATH,
so every subprocess call site resolves its binary through here rather than by
bare name.

A missing binary raises an ordinary exception, never ``SystemExit``, so the
caller can classify and report it (KTD25). A platform binary has no install
command, so its absence gets its own message and remedy.

``find`` returns None for a broken override and ``resolve`` raises for it:
``find`` is doctor's probe and must report every binary in one pass.

No filesystem side effects at import.
"""

from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from cratekit.core import secrets

#: Every platform the tables below answer for, so an audit can walk them all.
SUPPORTED_PLATFORMS: tuple[str, ...] = ("darwin", "linux", "win32")

#: Directories a graphical launcher does not put on PATH, per platform (R1).
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
    """Where a binary comes from, as a token rather than a command line (D2).

    The text a user types belongs to the CLI, which knows their package
    manager and whether there is a terminal at all.
    """

    HOMEBREW = "homebrew"
    APT = "apt"
    PIPX = "pipx"
    FROM_SOURCE = "from-source"


@dataclass(frozen=True, slots=True)
class InstallHint:
    """What to install and where from. Data, not a sentence or shell fragment."""

    manager: PackageManager
    packages: tuple[str, ...]


#: Where each user-installable binary comes from, per platform. Platforms with
#: no answer are absent rather than guessed: a wrong package manager is worse
#: than no hint.
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

#: Every binary a user can install, derived from the table so the two cannot drift.
INSTALLABLE_BINARIES: tuple[str, ...] = tuple(_INSTALL_HINTS)

#: Binaries the operating system provides; their absence means the wrong platform.
PLATFORM_BINARIES: frozenset[str] = frozenset({"caffeinate"})

ENV_PREFIX = "CRATEKIT_BIN_"


class Remedy(StrEnum):
    """What to do about a missing binary, as a token so callers never match text.

    Fix the override, nothing to install (platform binary), install from the
    known source, or install from a source this table does not know (KTD25, S4).
    """

    FIX_BINARY_OVERRIDE = "fix-binary-override"
    UNSUPPORTED_PLATFORM = "unsupported-platform"
    INSTALL_BINARY = "install-binary"
    INSTALL_BINARY_SOURCE_UNKNOWN = "install-binary-source-unknown"


class BinaryNotFound(Exception):
    """A required external binary is missing, or its override points at nothing.

    ``remedy`` says which kind of failure; ``hint`` says what to install, and
    is None whenever installing is not the remediation (D2).
    """

    def __init__(
        self, message: str, *, binary: str, remedy: Remedy, hint: InstallHint | None = None
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
    """Absolute path for ``name``, or None. Never raises.

    Order: the override, then PATH, then the fallback directories. A broken
    override returns None rather than silently using a different binary.
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


def override_problem(name: str) -> str | None:
    """The override that is set and is not an executable file, or None.

    ``find`` cannot tell this from "not installed", and the two need opposite
    instructions.
    """
    override = os.environ.get(env_var(name))
    return override if override and not _executable(Path(override)) else None


def resolve(name: str) -> str:
    """Absolute path for ``name``, or ``BinaryNotFound`` naming what to do."""
    override = override_problem(name)
    if override:
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
    # The message states what happened; what to do travels as remedy and hint
    # (D2). No hint is its own remedy, not a None-check on a second attribute.
    hint = install_hint(name)
    raise BinaryNotFound(
        f"{name} was not found (checked {checked}).",
        binary=name,
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,
        hint=hint,
    )


def install_hint(name: str, *, platform: str | None = None) -> InstallHint | None:
    """Where ``name`` comes from on ``platform``, this one by default, or None.

    None covers a platform binary and a platform this table has no row for.
    """
    if name in PLATFORM_BINARIES:
        return None
    return _INSTALL_HINTS.get(name, {}).get(sys.platform if platform is None else platform)


def subprocess_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """The environment with the fallback directories prepended to PATH.

    Spawned jobs get this so their own children resolve too. Opted-in Cratekit
    credentials are stripped: third-party binaries have no use for them, and a
    credential in a child environment can leak into a process listing.
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
    "ENV_PREFIX", "INSTALLABLE_BINARIES", "PLATFORM_BINARIES", "SUPPORTED_PLATFORMS",
    "BinaryNotFound", "InstallHint", "PackageManager", "Remedy", "env_var", "fallback_dirs",
    "find", "install_hint", "override_problem", "resolve", "subprocess_env",
]
