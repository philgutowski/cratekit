"""The one rekordbox ``Location`` encoder, decoder, and comparison normalizer.

One module because intake, deletion and the XML bridge all join on Location,
and two implementations of one rule eventually disagree.

Both sides of any disk path versus Location comparison pass through
:func:`norm_for_compare`. macOS may hand back a decomposed (NFD) name where
rekordbox writes composed (NFC), so a raw ``==`` misses every accented file and
only those; that miss deleted 144 referenced files on 2026-07-10.

KTD27: an emitted ``Location`` must be byte-identical to rekordbox's own export,
or importing it creates a duplicate collection row. Measured against a live
export (2026-08-01): a space is ``%20`` while ``!`` stays literal, escapes use
lowercase hex, and ``#`` stays literal. :func:`location_url` normalizes to NFC
before encoding, so the encoder and decoder are symmetric.

:func:`norm_for_compare` does not case-fold. A case-only collision is caught by
the device-and-inode proof that gates a deletion, not here.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Sequence
from urllib.parse import quote, unquote

# rekordbox's own safe set: emitted literally, all else percent-encoded UTF-8.
# Editing it changes which rows match; a per-character test guards it. Every
# member but ``*`` and ``~`` was observed literal; those two are inherited,
# unconfirmed.
REKORDBOX_SAFE_CHARS = "/:@!#$*+,;=-._~()"

# quote() writes uppercase escapes and rekordbox lowercase, so the output is
# post-processed, keeping quote()'s UTF-8 handling. Safe because it runs on
# encoded text, where a literal "%" is already "%25".
_UPPERCASE_ESCAPE = re.compile(r"%[0-9A-F]{2}")

# The two URL spellings rekordbox has shipped; the decoder accepts both.
_LOCALHOST_PREFIX = "file://localhost"
_EMPTY_AUTHORITY_PREFIX = "file:///"
_FILE_SCHEME = "file://"


class LocationDecodeError(ValueError):
    """A ``Location`` that names a host this machine cannot resolve to a path.

    Refused rather than guessed, or it surfaces later as a misleading missing file.
    """


def norm_for_compare(path: str) -> str:
    """NFC-normalize a path string for equality and set-membership tests.

    Both sides of any comparison between an on-disk path and a decoded
    ``Location`` must pass through this, or every accented file is missed.
    """
    return unicodedata.normalize("NFC", path)


def _native_to_url_path(path: str, *, separator: str = os.sep) -> str:
    """Convert a native path to the ``/``-separated form a file URL uses.

    The R1 Windows seam: on POSIX a backslash is a filename character and must
    survive as ``%5C``, on Windows it is the separator. ``separator`` is a
    parameter so the Windows branch is testable on POSIX. Only that branch adds
    a leading slash (before a drive letter); doing it always would make a
    relative POSIX path look absolute.
    """
    if separator == "/":
        return path
    converted = path.replace(separator, "/")
    return converted if converted.startswith("/") else "/" + converted


def location_url(abs_path: Path | str, *, separator: str = os.sep) -> str:
    """Build the rekordbox ``Location`` attribute for an absolute path.

    NFC first, then percent-encode, then lowercase the escapes. The order is
    asserted: encoding first keeps the filesystem's composition form, and one
    differing byte duplicates the collection row (KTD27).
    """
    text = _native_to_url_path(str(abs_path), separator=separator)
    encoded = quote(norm_for_compare(text), safe=REKORDBOX_SAFE_CHARS)
    return _LOCALHOST_PREFIX + _UPPERCASE_ESCAPE.sub(lambda m: m.group(0).lower(), encoded)


def looks_like_location(value: str) -> bool:
    """True when ``value`` is a URL rather than a plain filesystem path.

    Decides whether percent-decoding is safe: a plain filename may contain the
    literal text ``%20``, and decoding it names a different file.
    """
    return "://" in value


def location_to_path(location: str) -> str:
    """Decode a rekordbox ``Location`` (or pass through a plain path) to a path.

    Always returns NFC. ``file://localhost/`` and ``file:///`` are decoded,
    another host raises :class:`LocationDecodeError`, and a plain path (or a
    streaming pseudo-location) is normalized but not percent-decoded.
    """
    if location.startswith(_LOCALHOST_PREFIX):
        return norm_for_compare(unquote(location[len(_LOCALHOST_PREFIX):]))
    if location.startswith(_EMPTY_AUTHORITY_PREFIX):
        return norm_for_compare(unquote(location[len(_FILE_SCHEME):]))
    if location.startswith(_FILE_SCHEME):
        authority = location[len(_FILE_SCHEME):].split("/", 1)[0]
        raise LocationDecodeError(
            f"location names the host {authority!r}, which is not this machine; "
            f"a remote location has no local path and must not be guessed into one"
        )
    if looks_like_location(location):
        return norm_for_compare(unquote(location))
    return norm_for_compare(location)


# Recorded-path resolution. rekordbox keeps a path's old volume name after the
# volume is renamed, so recorded paths are rewritten through a declared prefix
# map (S1), never guessed. Rules are ordered, first match wins, and anchored at
# a component boundary. Rule and path are both NFC, so the order of rewrite and
# normalization does not matter. Existence is not checked here, so an unmapped
# prefix stays distinct from a deleted file.


@dataclass(frozen=True)
class PrefixRule:
    """One anchored rewrite: paths under ``source`` are rewritten under ``target``.

    Both sides are NFC-normalized on construction, so either typed form matches.
    ``volume_id`` names the volume ``target`` sits on; resolution never reads it,
    but a destructive pass needs rule and volume proof as one value rather than
    two lists joined by position.
    """

    source: str
    target: str
    volume_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source", norm_for_compare(self.source).rstrip("/"))
        object.__setattr__(self, "target", norm_for_compare(self.target).rstrip("/"))


class Resolution(str, Enum):
    """Why a recorded path resolved the way it did.

    A token, not a message, so callers branch and the CLI renders. An
    ``UNMAPPED`` prefix is reported, never guessed at.
    """

    UNDER_ROOT = "under_root"
    REMAPPED = "remapped"
    UNMAPPED = "unmapped"
    NOT_A_PATH = "not_a_path"


@dataclass(frozen=True)
class ResolvedPath:
    """The outcome of resolving one recorded path.

    ``path`` is None for every status except ``UNDER_ROOT`` and ``REMAPPED``,
    so the deletion review cannot treat an unresolved row as resolved.
    """

    resolution: Resolution
    path: str | None = None
    rule_index: int | None = None
    prefix: str | None = None


def leading_prefix(path: str, *, components: int = 2) -> str | None:
    """The first ``components`` components of an absolute path, for reporting.

    Counts components rather than naming mount roots, which differ by platform.
    Doctor groups unresolved rows by it.
    """
    normalized = norm_for_compare(path)
    if not normalized.startswith("/"):
        return None
    parts = [p for p in normalized.split("/") if p]
    if not parts:
        return "/"
    return "/" + "/".join(parts[:components])


def _matches_anchored(path: str, prefix: str) -> bool:
    """True when ``path`` lies under ``prefix`` as a whole path component.

    ``/x/Old`` must not match ``/x/OldArchive/track.flac``.
    """
    if not prefix:
        return False
    return path == prefix or path.startswith(prefix + "/")


def prefix_rules(pairs: Sequence[tuple[str, str]]) -> tuple[PrefixRule, ...]:
    """The rules a resolved prefix map becomes, in declared order.

    ``pairs`` is what ``Config.resolved_prefix_map`` answers.
    """
    return tuple(PrefixRule(source, target) for source, target in pairs)


def resolve_recorded_path(
    recorded: str,
    *,
    root: Path | str,
    prefix_map: Sequence[PrefixRule] = (),
) -> ResolvedPath:
    """Resolve a path recorded by rekordbox into a path on this machine.

    Existence is not checked, so "no rule maps this prefix" and "the file is
    gone" stay distinguishable.
    """
    path = norm_for_compare(str(recorded))
    root_text = norm_for_compare(str(root)).rstrip("/")

    if not path.startswith("/"):
        # A streaming pseudo-location or device-relative path, not a failure.
        return ResolvedPath(Resolution.NOT_A_PATH, prefix=None)

    if _matches_anchored(path, root_text):
        return ResolvedPath(Resolution.UNDER_ROOT, path=path)

    for index, rule in enumerate(prefix_map):
        if _matches_anchored(path, rule.source):
            remainder = path[len(rule.source):]
            return ResolvedPath(
                Resolution.REMAPPED,
                path=rule.target + remainder,
                rule_index=index,
            )

    return ResolvedPath(Resolution.UNMAPPED, prefix=leading_prefix(path))
