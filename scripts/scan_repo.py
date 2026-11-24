#!/usr/bin/env python3
"""Repository-wide portability and secret scan. Runs as a test, a hook, and a CI gate.

R1: Cratekit installs on a clean machine with no reference to the author's
paths, volumes, accounts, or machine. This scans EVERY tracked path, vendored
trees included, for path and account shapes and for credential shapes.
Exclusions are exact repo-relative paths, never substrings, and every pattern
is a shape rather than a fixed string.

The guard must not be its own violation: nothing here spells the author's home
directory, volume, or account. A test's example of a bad literal is assembled
from fragments at runtime, and ``machine_identity_tokens`` reads real
identifiers from the running machine rather than from this file.

Usage::

    python scripts/scan_repo.py            # scan the tracked tree, exit 1 on any finding
    python scripts/scan_repo.py FILE ...   # scan only these paths (pre-commit passes them)
"""

from __future__ import annotations

import functools
import getpass
import os
import re
import socket
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# Exclusions: EXACT repo-relative POSIX paths, never substrings or globs, so an
# entry exempts only the one file somebody decided to exempt. Empty on purpose.
ALLOWED_EXACT: frozenset[str] = frozenset()

# Archives are REFUSED rather than skipped, since the content scan cannot read
# inside one (R-3); third-party code is committed unpacked with its provenance.
ARCHIVE_SUFFIXES = frozenset({
    ".zip", ".tar", ".gz", ".tgz", ".bz2", ".tbz", ".tbz2", ".xz", ".txz",
    ".7z", ".rar", ".zst", ".lz", ".lzma", ".lz4", ".z", ".whl", ".jar",
    ".egg", ".deb", ".rpm", ".cpio", ".cab", ".ar",
})

# Extensions with no text to scan; archives are in it for the read and refused separately.
BINARY_SUFFIXES = ARCHIVE_SUFFIXES | frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns",
    ".pdf",
    ".db", ".sqlite", ".sqlite3", ".pyc", ".so", ".dylib", ".dll",
    ".flac", ".wav", ".aiff", ".aif", ".mp3", ".m4a", ".mp4", ".mov",
    ".woff", ".woff2", ".ttf", ".otf",
})

# An archive under a neutral name is caught by its leading bytes: offset, then bytes.
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
# bzip2 and cpio markers are ASCII, so each is matched with the structure after
# it rather than on letters ordinary prose could start with.
_ASCII_ARCHIVE_MAGIC: tuple[re.Pattern[bytes], ...] = (
    re.compile(rb"\ABZh[1-9]1AY&SY"),
    re.compile(rb"\A07070[127][0-9A-Fa-f]{8}"),
)

# Portability: path and account SHAPES, not fixed strings. Each class stops at
# anything that would end a path inside prose, a string literal, or a command.
_HOME_DIR = re.compile(r"(?:/Users|/home|/root|\\Users)/([^/\\\s\"'`,)\]}:;*]+)")
_MOUNT = re.compile(r"(?:/Volumes|/mnt|/media)/([^/\\\s\"'`,)\]}:;*]+)")
_WINDOWS_DRIVE = re.compile(r"\b[A-Z]:\\\\?(?:Users|Documents)\b")
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Stand-in segments: a doc may write a path shape, never one person's path.
PLACEHOLDER_SEGMENTS = frozenset({
    "you", "your", "youruser", "yourname", "user", "username", "USERNAME",
    "USER", "me", "someone", "somebody", "name", "NAME", "account",
    "example", "EXAMPLE", "placeholder", "changeme", "CHANGEME",
    "alice", "bob", "jane", "john", "dj",
    "LIBRARY", "library", "Library", "VOLUME", "volume", "Volume",
    "MyLibrary", "MusicLibrary", "MUSIC", "music", "Music",
    "runner", "root", "ubuntu", "docker", "vscode", "ci", "build", "tmp",
})

# RFC 2606 illustration domains.
PLACEHOLDER_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "invalid", "test")

# Tokens too generic to be anyone's identifier, dropped from every identity tier.
_IDENTITY_STOPWORDS = frozenset({
    "root", "runner", "user", "admin", "ubuntu", "build", "ci", "test",
    "docker", "vscode", "home", "none", "null", "data", "temp", "tmp",
    "macos", "linux", "windows", "python", "github", "local", "system",
})


# A DETECTED token that is an ordinary English word (U957) matches only where it
# names the machine or volume: a home or mount path segment, or a host name. A
# machine called by a plain word would otherwise fail every file that uses the
# word. A DECLARED token matches bare whatever the list says, so a person who
# wants the bare word caught declares it. The list ships beside this file, so
# macOS and the Linux runner decide alike, with no system dictionary.
ORDINARY_WORDS_FILE = Path(__file__).resolve().parent / "scan_ordinary_words.txt"
# The list's own path in the tree: every ordinary word is on it by definition,
# so a DECLARED ordinary word is not looked for there (U957). Every other
# token, and every other class of the scan, still reads it.
ORDINARY_WORDS_PATH = "scripts/scan_ordinary_words.txt"

# The local network suffixes a machine answers on, for ``<token>.<suffix>``.
_HOST_SUFFIXES = r"(?:local|lan|localdomain|home\.arpa)"
# Where a host name ends: not inside a longer name, nor before a further label.
_HOST_END = r"(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])"


@functools.lru_cache(maxsize=1)
def ordinary_words() -> frozenset[str]:
    """The shipped list of ordinary words, lower case; a missing list raises rather than relaxes."""
    lines = ORDINARY_WORDS_FILE.read_text(encoding="utf-8").splitlines()
    return frozenset(line.strip() for line in lines if line.strip() and not line.startswith("#"))


def is_ordinary_word(token: str) -> bool:
    """True when ``token`` is on the shipped list of ordinary words.

    Any case of the word as a whole counts (``Garden``, ``GARDEN``), but a
    capital inside a mixed case token (``AirPort``) marks a name, never a word.
    """
    if token[1:] != token[1:].lower() and not token.isupper():
        return False
    return token.lower() in ordinary_words()


class IdentityTokens(frozenset):
    """Every identity token, carrying the detected ordinary words that match only by shape.

    ``shape_only`` names which of the tokens match only by shape; a name in it
    that is not a token is never looked for. A plain set passed to
    ``portability_violations`` has none, so every token in it matches bare: a
    caller that loses this type over reports, it never passes silently.
    """

    shape_only: frozenset[str]

    def __new__(cls, tokens=(), shape_only=()):
        self = super().__new__(cls, tokens)
        self.shape_only = frozenset(shape_only)
        return self


def _is_placeholder_segment(segment: str) -> bool:
    """True when a captured path segment is a stand-in or opens with a template marker."""
    return not segment or segment[0] in "<{$%(" or segment in PLACEHOLDER_SEGMENTS


# A gitignored, per-clone list of a contributor's own identifiers, one per line,
# "#" comments. The runtime tier sees only a volume mounted now; declaring the
# names makes the guard deterministic. `.scan-identity.example` has the format.
IDENTITY_FILE = ".scan-identity"


def identity_file_tokens(root: Path) -> set[str]:
    """Read declared identifiers from the gitignored per-clone identity file."""
    path = root / IDENTITY_FILE
    if not path.is_file():
        return set()
    lines = (line.split("#", 1)[0].strip() for line in path.read_text().splitlines())
    return {line for line in lines if line}


# Where mounted volumes are listed; a module constant so a test can point it at a fixture.
MOUNT_ROOTS: tuple[str, ...] = ("/Volumes", "/media", "/mnt")


def machine_identity_tokens(root: Path | None = None) -> IdentityTokens:
    """Identifiers belonging to this machine and this contributor.

    From the declared identity file, the comma separated
    ``CRATEKIT_SCAN_IDENTITY`` variable, and the running system (login account,
    home directory name, short hostname, mounted volume names). Short and
    generic tokens are dropped, since they would flag ordinary prose. A
    detected token that is an ordinary word, and not also declared, is in
    ``shape_only``: it matches only in a path or host shape (U957).
    """
    declared: set[str] = set()
    detected: set[str] = set()

    def _add(into: set[str], value: str | None) -> None:
        if not value:
            return
        value = value.strip()
        if len(value) < 4 or value.lower() in _IDENTITY_STOPWORDS:
            return
        into.add(value)

    for value in identity_file_tokens(root if root is not None else REPO_ROOT):
        _add(declared, value)
    for value in os.environ.get("CRATEKIT_SCAN_IDENTITY", "").split(","):
        _add(declared, value)

    # A cloud session's account, hostname and mounts are the platform's, not a
    # person's, so only the declared tiers apply there.
    if os.environ.get("CLAUDE_CODE_REMOTE"):
        return IdentityTokens(declared)

    try:
        _add(detected, getpass.getuser())
    except Exception:  # pragma: no cover - getuser can fail with no passwd entry
        pass
    _add(detected, Path.home().name)
    _add(detected, socket.gethostname().split(".")[0])

    for mount_root in MOUNT_ROOTS:
        mounts = Path(mount_root)
        try:
            entries = list(mounts.iterdir()) if mounts.is_dir() else []
        except OSError:  # pragma: no cover - permission-denied mount roots
            entries = []
        for entry in entries:
            if not _is_placeholder_segment(entry.name):
                _add(detected, entry.name)

    declared_folded = {token.lower() for token in declared}
    shape_only = {
        token
        for token in detected
        if is_ordinary_word(token) and token.lower() not in declared_folded
    }
    return IdentityTokens(declared | detected, shape_only)


@functools.lru_cache(maxsize=64)
def _host_forms(token: str) -> re.Pattern[str]:
    """Where a token is a host: ``<t>.local`` and the like, ``user@<t>``,
    ``scheme://<t>`` or ``//<t>`` after a space, quote or bracket, ``\\\\<t>\\`` in a UNC path, and
    ``<t>:/path`` or ``<t>:~/path`` as scp and rsync write it. Never a method call
    (``<t>.local()``), a URL scheme (``<t>://``), a ``file:///`` path or an
    escaped drive path (``C:\\\\<t>\\\\``). Every form opens at the token, so
    ``_names_the_machine`` tries it only where the token is written."""
    name = re.escape(token)
    return re.compile(
        "|".join((
            rf"(?<![A-Za-z0-9_-]){name}\.{_HOST_SUFFIXES}(?![A-Za-z0-9_(-])",
            rf"(?<=[A-Za-z0-9._%+-]@){name}(?![A-Za-z0-9_-])(?!\.[A-Za-z])",
            rf"(?:(?<=[A-Za-z]://)|(?<=[\s\"'`(<\[]//)|(?<=^//)){name}{_HOST_END}",
            rf"(?:(?<=[^:A-Za-z0-9\\]\\\\)|(?<=^\\\\)){name}{_HOST_END}",
            rf"(?<![^\s\"'`(\[]){name}:(?:~|/(?!/))",
        )),
        re.IGNORECASE,
    )


def _names_the_machine(token: str, text: str, segments: set[str]) -> bool:
    """True when ``token`` is a home or mount path segment in ``text``, or a host."""
    if token.lower() in segments:
        return True
    host = _host_forms(token)
    # Each place the token is written, under the host forms' own case rule.
    return any(
        host.match(text, written.start())
        for written in re.finditer(re.escape(token), text, re.IGNORECASE)
    )


def portability_violations(text: str, *, identity_tokens: set[str] | None = None) -> list[str]:
    """One message per portability violation in ``text``; pure, and the skills lint calls it."""
    problems: list[str] = []
    # Every home and mount segment that is not a stand in, for the shape only tokens below.
    segments: set[str] = set()

    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        segments.add(segment.lower())
        problems.append(
            f"hardcoded home directory {match.group(0)!r}; resolve the user "
            f"directory through the platform library, or write a placeholder"
        )

    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        segments.add(segment.lower())
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

    # Case INSENSITIVE: an upper cased volume name is the same drive. This check
    # denies, so a missed case variant would be a silent pass. A detected
    # ordinary word matches only where it names the machine (U957).
    shape_only = identity_tokens.shape_only if isinstance(identity_tokens, IdentityTokens) else ()
    for token in sorted(identity_tokens or ()):
        if token in shape_only:
            found = _names_the_machine(token, text, segments)
        else:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])"
            found = re.search(pattern, text, re.IGNORECASE) is not None
        if found:
            problems.append(
                f"personal identifier {token!r} (a declared or detected account, "
                f"machine, or volume name); shipped artifacts name no person, "
                f"machine, or volume"
            )

    return problems


# Secrets: credential SHAPES over every tracked path.

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "OAuth token field",
        # A field named for a token with a long opaque value; the word separator
        # is optional so every casing convention is one rule.
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
        # The optional quote after the keyword is what matches the JSON form `"secret": "..."`.
        re.compile(
            r"""(?:api[_-]?key|apikey|secret|password|passwd|passphrase"""
            r"""|auth[_-]?token|access[_-]?secret|access[_-]?key)["']?"""
            r"""\s*[:=]\s*["'][^"'\s]{12,}["']""",
            re.IGNORECASE,
        ),
    ),
)

# Illustrative values, checked against the whole matched span.
_PLACEHOLDER_VALUE = re.compile(
    r"(?:<[^>]*>|\$\{[^}]*\}|\{\{[^}]*\}\}|xxx+|\*{3,}|\.\.\.|"
    r"YOUR[_-]|CHANGE[_-]?ME|REPLACE[_-]?ME|PLACEHOLDER|EXAMPLE|DUMMY|FAKE[_-]|"
    r"REDACTED|NOT[_-]?A[_-]?REAL|SAMPLE)",
    re.IGNORECASE,
)

# Filenames that ARE a credential store regardless of what is inside them.
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

# Names that ship a TEMPLATE rather than a filled-in credential.
_TEMPLATE_NAME = re.compile(r"(?:\.example$|\.sample$|\.template$|^example[._-]|^sample[._-])")


# Where each secret pattern is run (U257). Every match is still made by the
# pattern itself; a shortcut only leaves out positions and texts where a match
# is impossible. ``tests/test_scan_secret_equality.py`` pins equality with the plain loop.


class _LiteralLead(NamedTuple):
    """A pattern every match of which starts with ``literal``, case sensitively."""

    literal: str


class _KeywordGate(NamedTuple):
    """A keyword alternation, which may match only behind a separator its ``value`` matches at."""

    keyword_end: re.Pattern[str]
    width: int
    value: re.Pattern[str]


# The two case insensitive alternations in the pieces their sources are written
# in. A source that is not exactly these pieces gets no gate: time, never a finding.
_KEY_CLOSE = r"""["']?\s*"""
_SEPARATOR_AND_VALUE = r"""[:=]\s*["'][^"'\s]{%d,}["']"""
_KEYWORD_PATTERNS: dict[str, tuple[str, str, int]] = {
    "OAuth token field": (
        r"""["']?""",
        r"""(?:access[_-]?token|refresh[_-]?token|id[_-]?token"""
        r"""|client[_-]?secret|client[_-]?id|session[_-]?id"""
        r"""|consumer[_-]?(?:key|secret))""",
        16,
    ),
    "credential assignment": (
        "",
        r"""(?:api[_-]?key|apikey|secret|password|passwd|passphrase"""
        r"""|auth[_-]?token|access[_-]?secret|access[_-]?key)""",
        12,
    ),
}

# Python's own pattern parser, so a shortcut is read off the pattern. Private
# modules: their absence costs the shortcuts, never a finding.
try:
    from re import _constants as _re_constants
    from re import _parser as _re_parser
except ImportError:  # pragma: no cover - the supported Pythons have them
    _re_constants = _re_parser = None

# Every candidate separator for either alternation; a run holds one separator,
# so no run hides the start of another.
_SEPARATOR_RUN = re.compile(r"""[:=]\s*["']""")
_SPACE = re.compile(r"\s")
_QUOTES = "\"'"


def _parsed(pattern: re.Pattern[str]):
    """Python's own parse of ``pattern``, or None where this Python has no parser to read."""
    if _re_parser is None:  # pragma: no cover - every supported Python has it
        return None
    try:
        return _re_parser.parse(pattern.pattern, pattern.flags)
    except Exception:  # pragma: no cover - the pattern compiled, so it parses
        return None


def _literal_lead(pattern: re.Pattern[str]) -> _LiteralLead | None:
    """The literal every match of a case sensitive ``pattern`` starts with, or None."""
    parsed = _parsed(pattern)
    if parsed is None or (pattern.flags | parsed.state.flags) & re.IGNORECASE:
        return None
    items = list(parsed)
    if items and items[0] == (_re_constants.AT, _re_constants.AT_BOUNDARY):
        items = items[1:]
    literal = ""
    for op, value in items:
        if op is not _re_constants.LITERAL:
            break
        literal += chr(value)
    return _LiteralLead(literal) if literal else None


def _keyword_gate(label: str, pattern: re.Pattern[str]) -> _KeywordGate | None:
    """The gate for one of the two alternations, or None when its source is not the declared one."""
    declared = _KEYWORD_PATTERNS.get(label)
    if declared is None:
        return None
    opening, keywords, shortest = declared
    value = _SEPARATOR_AND_VALUE % shortest
    if pattern.pattern != opening + keywords + _KEY_CLOSE + value:
        return None
    keyword_end = re.compile(keywords + r"\Z", pattern.flags)
    parsed = _parsed(keyword_end)
    if parsed is None:
        return None
    _, high = parsed.getwidth()
    if high > 256:  # an unbounded keyword has no window to look back over
        return None
    return _KeywordGate(keyword_end, high, re.compile(value, pattern.flags))


def _shortcut_for(label: str, pattern: re.Pattern[str]) -> _LiteralLead | _KeywordGate | None:
    return _keyword_gate(label, pattern) or _literal_lead(pattern)


def _keyword_gate_passes(gate: _KeywordGate, text: str) -> bool:
    """False only when the gated pattern has no match anywhere in ``text``.

    A match's separator opens a ``_SEPARATOR_RUN`` where the value matches, and
    walking back over whitespace (none folds to a keyword letter, pinned by a
    test) and at most one quote lands where the engine finds a keyword ending.
    """
    for run in _SEPARATOR_RUN.finditer(text):
        separator = run.start()
        if gate.value.match(text, separator) is None:
            continue
        end = separator
        while end > 0 and _SPACE.match(text, end - 1):
            end -= 1
        ends = (end, end - 1) if end > 0 and text[end - 1] in _QUOTES else (end,)
        for keyword_end in ends:
            if gate.keyword_end.search(text, max(0, keyword_end - gate.width), keyword_end):
                return True
    return False


def _matches(pattern: re.Pattern[str], shortcut, text: str):
    """The matches ``pattern.finditer(text)`` yields, in its order, found with ``shortcut``."""
    if isinstance(shortcut, _KeywordGate):
        return pattern.finditer(text) if _keyword_gate_passes(shortcut, text) else ()
    if isinstance(shortcut, _LiteralLead):
        return _matches_at_literal(pattern, shortcut.literal, text)
    return pattern.finditer(text)


def _matches_at_literal(pattern: re.Pattern[str], literal: str, text: str):
    """``finditer`` with only the start positions it would have rejected left out.

    Every match starts with ``literal``, so only the positions ``str.find``
    reports are tried, in order, resuming from each match's end as ``finditer``
    does; ``match(text, pos)`` reads the word boundary before ``pos`` the same way.
    """
    position = text.find(literal)
    while position != -1:
        match = pattern.match(text, position)
        if match is None:
            position = text.find(literal, position + 1)
        else:
            yield match
            position = text.find(literal, match.end())


# Paired with the table by position, never by label.
_SECRET_SHORTCUTS: tuple[_LiteralLead | _KeywordGate | None, ...] = tuple(
    _shortcut_for(label, pattern) for label, pattern in SECRET_PATTERNS
)


def _secret_violations_over(text: str, patterns, shortcuts) -> list[str]:
    problems: list[str] = []
    for (label, pattern), shortcut in zip(patterns, shortcuts, strict=True):
        for match in _matches(pattern, shortcut, text):
            span = match.group(0)
            if _PLACEHOLDER_VALUE.search(span):
                continue
            problems.append(f"{label}: {_elide(span)}")
    return problems


def secret_violations(text: str) -> list[str]:
    """Return one message per credential-shaped literal in ``text``."""
    return _secret_violations_over(text, SECRET_PATTERNS, _SECRET_SHORTCUTS)


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
    """Return a message when a tracked file is an archive, by name then leading bytes.

    A symlink is left to the symlink rule rather than followed.
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
    """Show enough of a finding to locate it, never enough to leak it into a log."""
    span = span.replace("\n", " ")
    if len(span) <= keep:
        return span
    return f"{span[:keep]}... ({len(span)} chars, elided)"


# The restart state keeps only the sections no unit owns (U124); a unit's
# paragraph is its own file under docs/restart/ and is refused here.
RESTART_FILE = "RESTART-cratekit.md"

#: Everything above the first section, exactly.
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

#: The sections no unit owns.
RESTART_SECTIONS = frozenset({
    "## Main, verify before trusting it",
    "## What is open",
    "## Do this first",
    "## The branches",
    "## When a relay run is cut off mid unit",
    "## Standing decisions",
})

#: A paragraph opening on a unit, residual, chore or sitting is its record; refused anywhere.
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
        problems.append(
            f"the head above the first section is not the fixed reader's line; {remedy}"
        )
    for heading in re.findall(r"^## .*$", text, re.M):
        if heading not in RESTART_SECTIONS:
            problems.append(f"section {heading[3:]!r} is not one no unit owns; {remedy}")
    for match in _UNIT_RECORD.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        problems.append(f"line {line} opens a unit's record; {remedy}")
    return problems


def tracked_paths(root: Path) -> list[Path]:
    """Every tracked or untracked-but-not-ignored file under ``root``, vendored trees included.

    Outside a git checkout this falls back to a filesystem walk.
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
    """Return a message when a symlink's TARGET is absolute or escapes the repository.

    A symlink has no content for the other checkers to read.
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

    ``check_identity=False`` turns off the runtime-derived tier for deterministic tests.
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
        # Symlinks and archives before the content read, which returns None for both.
        findings += [f"{relative}: {p}" for p in symlink_violations(path, root)]
        findings += [f"{relative}: {p}" for p in archive_violations(path, relative)]
        text = _read_text(path)
        if text is None:
            continue
        tokens = identity
        if relative == ORDINARY_WORDS_PATH:
            listed = ordinary_words()
            tokens = IdentityTokens(
                (token for token in identity if token.lower() not in listed),
                getattr(identity, "shape_only", ()),
            )
        portable = portability_violations(text, identity_tokens=tokens)
        findings += [f"{relative}: {p}" for p in portable]
        findings += [f"{relative}: {p}" for p in secret_violations(text)]
        findings += [f"{relative}: {p}" for p in restart_violations(relative, text)]

    return findings


def main(argv: list[str]) -> int:
    root = Path(os.environ.get("CRATEKIT_SCAN_ROOT", REPO_ROOT)).resolve()
    # absolute(), never resolve(), which would follow a symlink past the symlink rule.
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
