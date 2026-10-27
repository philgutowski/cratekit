#!/usr/bin/env python3
"""Repository-wide portability and secret scan. Runs as a test, a hook, and a CI gate.

R1 says Cratekit installs on a clean machine with no reference to the author's
paths, volumes, accounts, or machine. The source system had a guard for that, and
the guard had three holes wide enough to walk through:

1. **It only looked at package Python.** ``grep -rn ... src/dj_tools --include="*.py"``.
   Tests, docs, shipped skills, shell scripts, HTML templates, and workflow files
   were all invisible to it. Two live violations sit in exactly those blind spots:
   a shipped skill telling the reader to work in the author's home directory, and
   another naming the author's volume. Both pass the source guard today.
2. **Its exclusion was a filename substring.** ``grep -v "DJ_common/config.py"``
   exempts any path that CONTAINS that text, so a new file could inherit the
   exemption by accident of naming. Exclusions here are exact repo-relative paths.
3. **Its literal set was two hardcoded strings.** One home directory, one volume.
   A second volume, a second account, or the same volume named without its
   ``/Volumes/`` prefix all sailed through. The patterns here are derived shapes,
   not fixed strings.

This module also carries the secret scan, because it is the same question asked
about a different literal: does a tracked file contain something that belongs to
one person rather than to the project. It runs over EVERY tracked path, vendored
trees included. That scope is deliberate. In the source system the artifact that
gets vendored sits in the same directory as a live OAuth session file holding an
access token and a refresh token, a credentials env file, and a service token. A
scan bounded to package source would not look at any of them.

A NOTE ON THIS FILE'S OWN CLEANLINESS. The guard must not be its own violation.
Nothing here spells the author's home directory, volume, or account. Every
pattern is a shape. Where a test needs a concrete example of a bad literal, the
example is assembled from fragments at runtime so this source stays clean. The
one place real identifiers enter is ``machine_identity_tokens``, which reads them
from the running machine rather than from this file.

Usage::

    python scripts/scan_repo.py            # scan the tracked tree, exit 1 on any finding
    python scripts/scan_repo.py FILE ...   # scan only these paths (pre-commit passes them)
"""

from __future__ import annotations

import getpass
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Exclusions. EXACT repo-relative POSIX paths, never substrings, never globs.
#
# A substring exclusion is how the source guard quietly stopped covering files
# that had never been reviewed: anything whose path happened to contain the
# excluded fragment inherited the exemption. An exact path can only ever exempt
# the one file somebody decided to exempt.
#
# Empty on purpose. If an entry is ever needed, it belongs here with a comment
# saying who decided and why, not spread across the callers.
# ---------------------------------------------------------------------------
ALLOWED_EXACT: frozenset[str] = frozenset()

# Compressed and packed containers. The content scan cannot read inside one, so
# a tracked archive is REFUSED rather than skipped: skipping it reported a clean
# tree over bytes nobody read (R-3). Third-party code is committed unpacked with
# its provenance recorded, which is what vendor/README.md does.
ARCHIVE_SUFFIXES = frozenset(
    {
        ".zip", ".tar", ".gz", ".tgz", ".bz2", ".tbz", ".tbz2", ".xz", ".txz",
        ".7z", ".rar", ".zst", ".lz", ".lzma", ".lz4", ".z", ".whl", ".jar",
        ".egg", ".deb", ".rpm", ".cpio", ".cab", ".ar",
    }
)

# Extensions with no text to scan. Read as bytes and skipped early, both to save
# work and because a binary blob produces meaningless "violations" otherwise.
# Archives are in this set for the read, and refused separately above it.
BINARY_SUFFIXES = ARCHIVE_SUFFIXES | frozenset(
    {
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns",
        ".pdf",
        ".db", ".sqlite", ".sqlite3", ".pyc", ".so", ".dylib", ".dll",
        ".flac", ".wav", ".aiff", ".aif", ".mp3", ".m4a", ".mp4", ".mov",
        ".woff", ".woff2", ".ttf", ".otf",
    }
)

# An archive carried under a name that does not say so is still an archive. The
# leading bytes are what every extractor reads, so they are what this reads.
# Offsets, then the bytes expected there.
_ARCHIVE_MAGIC: tuple[tuple[int, bytes], ...] = (
    (0, b"PK\x03\x04"),  # zip, and every format built on it (wheel, jar)
    (0, b"PK\x05\x06"),  # an empty zip
    (0, b"\x1f\x8b"),  # gzip
    (0, b"\xfd7zXZ\x00"),  # xz
    (0, b"7z\xbc\xaf\x27\x1c"),  # 7z
    (0, b"Rar!\x1a\x07"),  # rar
    (0, b"\x28\xb5\x2f\xfd"),  # zstd
    (0, b"\x04\x22\x4d\x18"),  # lz4 frame
    (0, b"\x02\x21\x4c\x18"),  # lz4 legacy frame
    (0, b"\x1f\x9d"),  # Unix compress, ``.Z``
    (0, b"LZIP\x01"),  # lzip
    (0, b"!<arch>\n"),  # ar, which is also every ``.deb``
    (0, b"\xed\xab\xee\xdb"),  # rpm
    (0, b"MSCF\x00\x00\x00\x00"),  # cab
    (257, b"ustar"),  # tar, whose marker sits after the first header's name field
)
# Two markers are ASCII, so each is matched with the structure that follows it
# rather than on its letters alone, which ordinary prose could start with:
# bzip2's ``BZh`` with its block size digit and block magic, and cpio's
# ``07070`` with its variant digit and the hex field after it.
_ASCII_ARCHIVE_MAGIC: tuple[re.Pattern[bytes], ...] = (
    re.compile(rb"\ABZh[1-9]1AY&SY"),
    re.compile(rb"\A07070[127][0-9A-Fa-f]{8}"),
)

# ---------------------------------------------------------------------------
# Portability: path and account SHAPES, not fixed strings.
# ---------------------------------------------------------------------------

# A home directory on any platform, capturing the account segment that follows.
# The character class stops at anything that would end a path inside prose, a
# string literal, or a shell command.
_HOME_DIR = re.compile(r"(?:/Users|/home|/root|\\Users)/([^/\\\s\"'`,)\]}:;*]+)")

# A mounted volume on any platform, capturing the volume name.
_MOUNT = re.compile(r"(?:/Volumes|/mnt|/media)/([^/\\\s\"'`,)\]}:;*]+)")

# A drive-letter path is a machine assumption even without an account name.
_WINDOWS_DRIVE = re.compile(r"\b[A-Z]:\\\\?(?:Users|Documents)\b")

# An email address is an account identifier.
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Segments that are obviously stand-ins rather than a real account or volume.
# A doc SHOULD be able to write out a path shape; what it must not do is write
# out one particular person's path.
PLACEHOLDER_SEGMENTS = frozenset(
    {
        "you", "your", "youruser", "yourname", "user", "username", "USERNAME",
        "USER", "me", "someone", "somebody", "name", "NAME", "account",
        "example", "EXAMPLE", "placeholder", "changeme", "CHANGEME",
        "alice", "bob", "jane", "john", "dj",
        "LIBRARY", "library", "Library", "VOLUME", "volume", "Volume",
        "MyLibrary", "MusicLibrary", "MUSIC", "music", "Music",
        "runner", "root", "ubuntu", "docker", "vscode", "ci", "build", "tmp",
    }
)

# Domains that mean "this is an illustration", per RFC 2606.
PLACEHOLDER_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "invalid", "test")

# Account-shaped tokens too generic to be anyone's identifier. Applied only to
# the RUNTIME-DERIVED identity set below, never to the shape patterns.
_IDENTITY_STOPWORDS = frozenset(
    {
        "root", "runner", "user", "admin", "ubuntu", "build", "ci", "test",
        "docker", "vscode", "home", "none", "null", "data", "temp", "tmp",
        "macos", "linux", "windows", "python", "github", "local", "system",
    }
)


def _is_placeholder_segment(segment: str) -> bool:
    """True when a captured path segment stands in for a real one.

    Anything opening with a templating marker counts, so ``<name>``, ``{user}``,
    ``$HOME``, and ``%USERPROFILE%`` all read as shapes rather than identities.
    """
    if not segment:
        return True
    if segment[0] in "<{$%(":
        return True
    return segment in PLACEHOLDER_SEGMENTS


# A gitignored, per-clone list of identifiers a contributor knows are theirs:
# volume names, account handles, machine names. One per line, "#" comments.
#
# It exists because the runtime tier below can only see a volume that is MOUNTED
# RIGHT NOW. Unplug the drive and a bare volume name in a document stops being
# detectable, which makes the guard depend on what happens to be connected. That
# is not a guard, it is a coincidence. Declaring the names makes it deterministic.
#
# Gitignored on purpose: the file names one person's identifiers, so it is the
# one thing in the repository that must never ship. `.scan-identity.example`
# documents the format.
IDENTITY_FILE = ".scan-identity"


def identity_file_tokens(root: Path) -> set[str]:
    """Read declared identifiers from the gitignored per-clone identity file."""
    path = root / IDENTITY_FILE
    if not path.is_file():
        return set()
    tokens = set()
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            tokens.add(line)
    return tokens


def machine_identity_tokens(root: Path | None = None) -> set[str]:
    """Identifiers belonging to this machine and this contributor.

    This is the tier that catches a bare volume name, an account name written
    without its path prefix, or a hostname. Three sources, in order of
    reliability:

    1. the declared identity file, which is deterministic;
    2. the ``CRATEKIT_SCAN_IDENTITY`` environment variable, comma separated, for
       a runner that has no checkout-local file;
    3. the running system: the login account, the home directory name, the short
       hostname, and the names of currently mounted volumes.

    Source 3 is a bonus, not the foundation. It reads those values from the
    machine rather than listing them here, which is the only way to check for the
    author's own identifiers without this file containing them, but it can only
    see a volume while it is plugged in.

    On a clean CI machine the whole set is nearly empty and the path SHAPES above
    do the work, which is correct: a clean machine has no personal identity to
    leak.

    Short and generic tokens are dropped, because a four-letter account name that
    is also an English word would flag half the prose in the repository.
    """
    tokens: set[str] = set()

    def _add(value: str | None) -> None:
        if not value:
            return
        value = value.strip()
        if len(value) < 4 or value.lower() in _IDENTITY_STOPWORDS:
            return
        tokens.add(value)

    for declared in identity_file_tokens(root if root is not None else REPO_ROOT):
        _add(declared)
    for declared in os.environ.get("CRATEKIT_SCAN_IDENTITY", "").split(","):
        _add(declared)

    # A Claude Code cloud session runs in a container whose account, hostname
    # and mounts are the platform's, not a person's: its mount root holds
    # directories named for the harness's own fixtures, and one of those names
    # is an ordinary English word that appears in file names across this tree.
    # Reading them as identity flagged every such file. The declared tiers
    # above still apply there; only the detected tier is the machine's.
    if os.environ.get("CLAUDE_CODE_REMOTE"):
        return tokens

    try:
        _add(getpass.getuser())
    except Exception:  # pragma: no cover - getuser can fail with no passwd entry
        pass
    _add(Path.home().name)
    _add(socket.gethostname().split(".")[0])

    # Names of currently mounted volumes, read from the platform's mount root.
    for mount_root in ("/Volumes", "/media", "/mnt"):
        root = Path(mount_root)
        try:
            entries = list(root.iterdir()) if root.is_dir() else []
        except OSError:  # pragma: no cover - permission-denied mount roots
            entries = []
        for entry in entries:
            if not _is_placeholder_segment(entry.name):
                _add(entry.name)

    return tokens


def portability_violations(text: str, *, identity_tokens: set[str] | None = None) -> list[str]:
    """Return one message per portability violation found in ``text``.

    Pure: it takes a string and returns strings. That is what lets the fixture
    tests prove each rule bites without planting a file in the repository, and it
    is the same shape the skills lint uses, so rule (d) there can simply call
    this rather than keeping a second, drifting copy of the literal set.
    """
    problems: list[str] = []

    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        problems.append(
            f"hardcoded home directory {match.group(0)!r}; resolve the user "
            f"directory through the platform library, or write a placeholder"
        )

    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        problems.append(
            f"hardcoded volume path {match.group(0)!r}; the library root is "
            f"configuration, not a literal"
        )

    for match in _WINDOWS_DRIVE.finditer(text):
        problems.append(f"hardcoded drive-letter path {match.group(0)!r}")

    for match in _EMAIL.finditer(text):
        address = match.group(0)
        if address.lower().endswith(PLACEHOLDER_EMAIL_DOMAINS):
            continue
        problems.append(f"account identifier (email address) {address!r}")

    # Matched case INSENSITIVELY. A volume declared as ``EP_Style_Name`` and
    # written as ``EP_STYLE_NAME`` is the same drive to the person reading it and
    # to the case insensitive filesystem it is mounted on, and it was a silent
    # miss here until 2026-08-27: a test fixture carried the author's real drive
    # name in upper case through a green suite and a passing scan.
    #
    # This is the opposite risk direction from ``PLACEHOLDER_SEGMENTS`` above,
    # which enumerates its case variants by hand and should stay that way. That
    # set PERMITS, so a variant it misses becomes a noisy false positive. This
    # check DENIES, so a variant it misses becomes a silent pass, and a guard
    # that fails silently is the one shape this module exists to not be.
    for token in sorted(identity_tokens or ()):
        if re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", text, re.IGNORECASE
        ):
            problems.append(
                f"personal identifier {token!r} (a declared or detected account, "
                f"machine, or volume name); shipped artifacts name no person, "
                f"machine, or volume"
            )

    return problems


# ---------------------------------------------------------------------------
# Secrets. Credential SHAPES over every tracked path.
# ---------------------------------------------------------------------------

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "OAuth token field",
        # The shape the source system's session cache uses: a JSON or TOML field
        # named for a token, carrying a long opaque value.
        # The separator between words is optional, so client_secret,
        # clientSecret, client-secret and clientsecret are one rule rather than
        # four. A real vendored file used the camelCase spelling and this scan
        # walked straight past five live credential pairs, because the keyword
        # list had been written in the one casing the author happened to think
        # of. Naming conventions are not a security boundary.
        re.compile(
            r"""["']?(?:access[_-]?token|refresh[_-]?token|id[_-]?token"""
            r"""|client[_-]?secret|client[_-]?id|session[_-]?id"""
            r"""|consumer[_-]?(?:key|secret))["']?"""
            r"""\s*[:=]\s*["'][^"'\s]{16,}["']""",
            re.IGNORECASE,
        ),
    ),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{24,}={0,2}")),
    ("JSON web token", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("provider secret key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----")),
    (
        "credential assignment",
        # The optional closing quote after the keyword is load-bearing, not
        # tidiness. Without it this rule matches `secret = "..."` but NOT
        # `"secret": "..."`, because in the quoted form a quote character sits
        # between the keyword and the colon where the pattern expects only
        # whitespace. Every credential in a JSON or JSON-shaped literal takes
        # the quoted form, which is most of them.
        re.compile(
            r"""(?:api[_-]?key|apikey|secret|password|passwd|passphrase"""
            r"""|auth[_-]?token|access[_-]?secret|access[_-]?key)["']?"""
            r"""\s*[:=]\s*["'][^"'\s]{12,}["']""",
            re.IGNORECASE,
        ),
    ),
)

# Values that are obviously illustrative. Checked against the whole matched span
# so a documented example is never mistaken for a live credential.
_PLACEHOLDER_VALUE = re.compile(
    r"(?:<[^>]*>|\$\{[^}]*\}|\{\{[^}]*\}\}|xxx+|\*{3,}|\.\.\.|"
    r"YOUR[_-]|CHANGE[_-]?ME|REPLACE[_-]?ME|PLACEHOLDER|EXAMPLE|DUMMY|FAKE[_-]|"
    r"REDACTED|NOT[_-]?A[_-]?REAL|SAMPLE)",
    re.IGNORECASE,
)

# Filenames that ARE a credential store regardless of what is inside them. This
# rule exists because of the concrete adjacency the plan calls out: the artifact
# that gets vendored sits beside a live OAuth session file. A content scan cannot
# see inside a compressed archive, but it can always see a name.
CREDENTIAL_FILENAMES: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|[._-])session\.json$", re.IGNORECASE),
    re.compile(r"session[._-]?(?:cache|token|state)\.json$", re.IGNORECASE),
    re.compile(r"^secrets?\.(?:env|json|toml|ya?ml)$", re.IGNORECASE),
    re.compile(r"^\.env$", re.IGNORECASE),
    re.compile(r"credentials?(?:\.[a-z0-9]+)?$", re.IGNORECASE),
    re.compile(r"^id_(?:rsa|dsa|ecdsa|ed25519)$"),
    re.compile(r"\.(?:pem|p12|pfx|keystore|jks)$", re.IGNORECASE),
    re.compile(r"^[a-z0-9_-]*token$", re.IGNORECASE),
)

# Names that clearly ship a TEMPLATE rather than a filled-in credential.
_TEMPLATE_NAME = re.compile(r"(?:\.example$|\.sample$|\.template$|^example[._-]|^sample[._-])")


def secret_violations(text: str) -> list[str]:
    """Return one message per credential-shaped literal in ``text``."""
    problems: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            span = match.group(0)
            if _PLACEHOLDER_VALUE.search(span):
                continue
            problems.append(f"{label}: {_elide(span)}")
    return problems


def credential_filename_violations(relative_path: str) -> list[str]:
    """Return a message when the PATH itself names a credential store."""
    name = Path(relative_path).name
    if _TEMPLATE_NAME.search(name):
        return []
    for pattern in CREDENTIAL_FILENAMES:
        if pattern.search(name):
            return [
                f"tracked file name looks like a credential store: {relative_path!r}; "
                f"credentials belong in the OS keychain, never in the repository"
            ]
    return []


def archive_violations(path: Path, relative_path: str) -> list[str]:
    """Return a message when a tracked file is a compressed or packed archive.

    Judged by name first and by leading bytes second, so an archive renamed to
    something neutral is still refused. A symlink is left to the symlink rule,
    which owns it, rather than followed here to whatever it points at.
    """
    message = (
        f"tracked file is an archive the scan cannot read inside: {relative_path!r}; "
        f"commit the tree unpacked with its provenance recorded instead"
    )
    name = Path(relative_path).name.lower()
    if any(name.endswith(suffix) for suffix in ARCHIVE_SUFFIXES):
        return [message]
    if path.is_symlink():
        return []
    try:
        with path.open("rb") as handle:
            head = handle.read(512)
    except OSError:
        return []
    for offset, magic in _ARCHIVE_MAGIC:
        if head[offset : offset + len(magic)] == magic:
            return [message]
    if any(pattern.match(head) for pattern in _ASCII_ARCHIVE_MAGIC):
        return [message]
    return []


def _elide(span: str, keep: int = 12) -> str:
    """Show enough of a finding to locate it, never enough to leak it.

    A guard that prints the secret it found has copied the secret into CI logs,
    the terminal scrollback, and any transcript of the run.
    """
    span = span.replace("\n", " ")
    if len(span) <= keep:
        return span
    return f"{span[:keep]}... ({len(span)} chars, elided)"


# ---------------------------------------------------------------------------
# Walking the tree
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# The restart state has no per unit area any more (U124). Every unit used to
# append its paragraph to the head of RESTART-cratekit.md, so every two
# branches cut from one base conflicted there and a lane landing waited a
# merge round per unit. A unit's paragraph is now its own file under
# docs/restart/, and this file keeps only the sections no unit owns. A
# paragraph written back into it is refused here, because the hook runs this
# on every commit that stages the file and CI runs it over the tree.
# ---------------------------------------------------------------------------
RESTART_FILE = "RESTART-cratekit.md"

#: Everything above the first section, exactly. Editing the reader's line is
#: editing this constant too, which is the point: a unit cannot slip a
#: paragraph in above the sections without this guard saying so.
RESTART_HEAD = (
    "# Restart: Cratekit\n"
    "\n"
    "Verified state only. How to work is `docs/METHOD.md`. Why the rules are what\n"
    "they are is `docs/history/`. **No hash is written here on purpose**, since this\n"
    "file is part of the commit it would be naming.\n"
    "\n"
    "**Each unit's own record is a file in `docs/restart/`**, named for what it\n"
    "records, `u114.md` for U114, `r572.md` for R-572, `sitting35.md` for an\n"
    "attended sitting. A unit writes its paragraph there and never here, so two\n"
    "units built in parallel land in either order. This lists the ones added since\n"
    "U124, newest first:\n"
    "\n"
    "    git log --diff-filter=A --name-only --format= -- docs/restart\n"
    "\n"
    "U124 moved every earlier record in one commit, so those list together after\n"
    "them; the newest of those are `u118.md`, `u114.md` and `r925.md`.\n"
    "\n"
    "This file keeps only the sections no unit owns, and `scripts/scan_repo.py`\n"
    "refuses a unit's paragraph anywhere in it.\n"
    "\n"
)

#: The sections no unit owns. A new one is a decision about the restart state
#: itself, made here, not a place a unit's record can open.
RESTART_SECTIONS = frozenset(
    {
        "## Main, verify before trusting it",
        "## What is open",
        "## Do this first",
        "## The branches",
        "## When a relay run is cut off mid unit",
        "## Standing decisions",
    }
)

#: The openers a record carried, "**U118 built, ...", "**R-857 done, ...",
#: "**Sitting 35, ...", "**A5 ...": a paragraph that opens on a unit, a
#: residual, a chore or a sitting is that one's record. Refused anywhere in
#: the file, inside a kept section too.
_UNIT_RECORD = re.compile(r"^\*\*(?:U\d+|R-\d+|A\d+|Sitting \d+)\b", re.M)


def restart_violations(relative_path: str, text: str) -> list[str]:
    """A unit's record written into the restart state instead of its own file."""
    if relative_path != RESTART_FILE:
        return []
    remedy = "a unit's paragraph goes in docs/restart/<unit>.md (U124)"
    problems: list[str] = []
    first = re.search(r"^## ", text, re.M)
    head = text[: first.start()] if first else text
    if head != RESTART_HEAD:
        problems.append(f"the head above the first section is not the fixed reader's line; {remedy}")
    for heading in re.findall(r"^## .*$", text, re.M):
        if heading not in RESTART_SECTIONS:
            problems.append(f"section {heading[3:]!r} is not one no unit owns; {remedy}")
    for match in _UNIT_RECORD.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        problems.append(f"line {line} opens a unit's record; {remedy}")
    return problems


def tracked_paths(root: Path) -> list[Path]:
    """Every tracked file under ``root``, vendored trees included.

    Git is asked first because "would this ship" is the definition that matters.
    Untracked-but-not-ignored files are included alongside tracked ones on
    purpose: a violation that has been written but not yet committed is still a
    violation, and catching it before the commit is the whole value of a guard.
    Ignored files are excluded, since by definition they never ship.

    Outside a git checkout, and in the fixture tests, this falls back to a
    filesystem walk so the same checkers can be driven against a synthetic tree.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
             "--exclude-standard"],
            capture_output=True,
            check=True,
        )
        names = [n for n in result.stdout.decode().split("\0") if n]
        return [root / name for name in names]
    except (OSError, subprocess.CalledProcessError):
        return [
            path
            for path in sorted(root.rglob("*"))
            if path.is_file() and ".git" not in path.parts
        ]


def _read_text(path: Path) -> str | None:
    """Decode a file as text, or return None when it is binary or unreadable."""
    if path.suffix.lower() in BINARY_SUFFIXES:
        return None
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def symlink_violations(path: Path, root: Path) -> list[str]:
    """Return one message per portability problem in a symlink's TARGET.

    THE HOLE THIS CLOSES. Every other checker here reads a file's CONTENT, and a
    symlink has none: following one to a directory raises, the reader returns
    None, and the entry is skipped before any rule sees it. So a link whose
    target is an absolute path on the author's machine sailed through a scan that
    reported clean, and got committed. That happened, with a ``.venv`` symlink
    pointing at an absolute home directory, on a tree where this scan exited 0.

    A symlink is a portability violation in exactly two shapes: an ABSOLUTE
    target, which cannot resolve on anyone else's machine, and a relative target
    that ESCAPES the repository, which resolves to whatever happens to sit beside
    the clone. A relative link inside the tree is fine and stays fine.
    """
    try:
        if not path.is_symlink():
            return []
        target = os.readlink(path)
    except OSError:  # pragma: no cover - unreadable link
        return []

    if os.path.isabs(target):
        return [f"is a symlink to the absolute path {target!r}, which exists only on one machine"]

    resolved = (path.parent / target).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return [f"is a symlink escaping the repository, to {target!r}"]
    return []


def scan_tree(
    root: Path,
    paths: list[Path] | None = None,
    *,
    check_identity: bool = True,
) -> list[str]:
    """Scan a tree and return every finding as ``"<relative path>: <problem>"``.

    ``check_identity`` exists so the fixture tests can turn off the
    runtime-derived tier and assert the shape patterns on their own, which keeps
    those tests deterministic across machines.
    """
    identity = machine_identity_tokens(root) if check_identity else set()
    findings: list[str] = []

    for path in paths if paths is not None else tracked_paths(root):
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = path.as_posix()
        if relative in ALLOWED_EXACT:
            continue

        findings += [f"{relative}: {p}" for p in credential_filename_violations(relative)]
        # Before the content read, because a symlink has no content to read and
        # is otherwise skipped entirely.
        findings += [f"{relative}: {p}" for p in symlink_violations(path, root)]
        # Also before the content read, because the reader returns None for an
        # archive and the loop would otherwise move on as though it were clean.
        findings += [f"{relative}: {p}" for p in archive_violations(path, relative)]

        text = _read_text(path)
        if text is None:
            continue
        findings += [f"{relative}: {p}" for p in portability_violations(text, identity_tokens=identity)]
        findings += [f"{relative}: {p}" for p in secret_violations(text)]
        findings += [f"{relative}: {p}" for p in restart_violations(relative, text)]

    return findings


def main(argv: list[str]) -> int:
    root = Path(os.environ.get("CRATEKIT_SCAN_ROOT", REPO_ROOT)).resolve()
    # absolute(), never resolve(): resolve() FOLLOWS a symlink, so the path the
    # checkers receive is the target rather than the link, and the symlink rule
    # below then sees nothing to judge. This is the path pre-commit uses, because
    # it passes filenames, so getting it wrong disarms the rule exactly where it
    # is meant to fire.
    explicit = [Path(a).absolute() for a in argv[1:]] or None
    findings = scan_tree(root, explicit)
    if not findings:
        return 0
    print("repository scan found content that must not ship:", file=sys.stderr)
    for finding in findings:
        print(f"  {finding}", file=sys.stderr)
    print(
        "\nR1: no shipped artifact names a person, machine, path, volume, or "
        "account. Credentials belong in the OS keychain.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
