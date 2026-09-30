"""The one rekordbox ``Location`` encoder, decoder, and comparison normalizer.

Three primitives, one module, because they are one rule seen from three sides.
A ``Location`` is the exact-match evidence every later unit joins on: intake
matches new tracks against the collection by Location, deletion proves a file is
unreferenced by Location, and the XML bridge inherits Locations rather than
inventing them. Two implementations of the same rule that agree today will
disagree eventually, and the disagreement is invisible until it has already
destroyed something.

WHY THIS MODULE EXISTS AT ALL, in two incidents.

**The 144-file loss (2026-07-10).** macOS filesystems hand back a filename in
whatever composition form it was created with, and historically HFS+ stored
DECOMPOSED (NFD): ``e`` U+0065 followed by COMBINING ACUTE ACCENT U+0301.
rekordbox exports the same filename COMPOSED (NFC): LATIN SMALL LETTER E WITH
ACUTE U+00E9. Those are different codepoint sequences, so::

    "Grigore\\u0301.flac" == "Grigor\\u00e9.flac"   ->  False

A raw ``==`` or a set-membership test between a walked disk path and a decoded
Location therefore MISSES every accented file, and only accented files: ASCII
names compare byte-identically and never enter the miss set. An ad-hoc orphan
sweep did exactly that, concluded 144 still-referenced files had no Location
pointing at them, and deleted them. Every single deleted file was non-ASCII.
That is the whole mechanism: not an exotic Unicode edge case, just two spellings
of one name and one comparison that did not know it.

The rule that falls out: BOTH sides of any disk-path-versus-Location comparison
pass through :func:`norm_for_compare` first. Not one side. Both.

**KTD27, the emitter invariant.** An emitted ``Location`` must be byte-identical
to what rekordbox itself exports, or rekordbox's import creates a second
collection row instead of matching the existing one. The user then has a
duplicate they did not ask for, pointing at the same file, with the cue points
and grid on the wrong one. Two consequences for this module:

1. The safe set and the escape spelling below are not style choices. They
   reproduce rekordbox's own encoding, measured character class by character
   class against a live export of 10,070 collection rows on 2026-08-01. Three
   things that measurement settled, two of which the ported encoder got wrong:

   * a space becomes ``%20`` while ``!`` stays literal. This is the pair KTD27
     names, it is the pair that distinguishes rekordbox's rule from both
     ``quote()``'s default and ``quote_plus()``, and the ported encoder had it
     right;
   * every one of the 144,350 percent escapes in that export uses LOWERCASE hex
     digits. Python's ``quote()`` emits uppercase. 711 of 10,070 real rows
     therefore failed a byte-identity check against the ported encoder, every
     one of them a row with a non-ASCII character in its path;
   * ``#`` is emitted LITERAL, not as ``%23``. Another 19 rows failed on that
     alone. It is not a URI fragment delimiter as far as rekordbox is concerned,
     because a ``Location`` is an attribute value rather than a link.

   With both corrected, all 10,070 rows round-trip byte-identically.
2. :func:`location_url` NFC-normalizes BEFORE it encodes. The source system's
   encoder did not, so a decomposed on-disk name emitted ``Grigore%cc%81.flac``
   while rekordbox's own export of that same file said ``Grigor%c3%a9.flac``.
   One file, two Location strings, and by KTD27 that is precisely the byte
   mismatch that duplicates a row. The decoder always normalized; the encoder
   never did. Making the pair symmetric is the fix.

WHAT :func:`norm_for_compare` DOES NOT DO. It does not case-fold. Two names
differing only in case are a real collision on a case-insensitive volume and
this function will not report them equal. That case is covered where it belongs,
by the device-and-inode proof that gates a deletion, not by a string normalizer.
An implementer who assumes otherwise gets a guard that silently passes.
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

# rekordbox's own safe set, reproduced exactly. Every character here is emitted
# literally; everything else becomes percent-encoded UTF-8 bytes. Editing this
# string changes what rekordbox considers a matching row, so the per-character
# table test exists to make an edit fail loudly rather than quietly.
#
# Every member except ``*`` and ``~`` was observed literal in the measured
# export. Those two appear nowhere in that corpus, so they are inherited from the
# encoder this ports rather than confirmed, and they are flagged here so nobody
# reads the whole set as equally evidenced.
REKORDBOX_SAFE_CHARS = "/:@!#$*+,;=-._~()"

# rekordbox writes percent escapes in lowercase hex; Python's quote() writes them
# in uppercase. Post-processing rather than hand-rolling the encoder keeps
# quote()'s UTF-8 handling, which is the part that is easy to get subtly wrong.
#
# The substitution is unambiguous BECAUSE it runs on already-encoded text: a
# literal "%" in a filename has itself become "%25" by this point, so every "%"
# here starts an escape and a filename containing the text "%C3" cannot be
# corrupted into a different one.
_UPPERCASE_ESCAPE = re.compile(r"%[0-9A-F]{2}")

# The two URL spellings rekordbox has shipped. Both appear in real exports, so
# the decoder handles both rather than assuming the current one.
_LOCALHOST_PREFIX = "file://localhost"
_EMPTY_AUTHORITY_PREFIX = "file:///"
_FILE_SCHEME = "file://"


class LocationDecodeError(ValueError):
    """A ``Location`` that names a host this machine cannot resolve to a path.

    Refusing beats guessing. The source system's decoder fell through to a bare
    ``unquote`` for a non-localhost authority and returned ``file://host/x.flac``
    as if it were a filesystem path, which then failed an existence check and was
    reported as a missing file. The cause and the symptom had nothing to do with
    each other, and the real cause was invisible.
    """


def norm_for_compare(path: str) -> str:
    """NFC-normalize a path string for equality and set-membership tests.

    Both sides of any comparison between an on-disk path and a decoded
    ``Location`` must pass through this. See the module docstring for the
    incident that establishes the rule; the short version is that skipping it
    silently loses every accented file and nothing else.
    """
    return unicodedata.normalize("NFC", path)


def _native_to_url_path(path: str, *, separator: str = os.sep) -> str:
    """Convert a native path to the ``/``-separated form a file URL uses.

    The R1 seam for a Windows adapter, and it has to be a seam rather than a
    literal because the two platforms disagree about what a backslash MEANS. On
    POSIX a backslash is an ordinary filename character and must survive as
    ``%5C``; on Windows it is the separator and must become ``/``. A single
    implementation that picked either answer would be wrong on one platform, and
    wrong in the direction that corrupts a path rather than raising.

    The separator is a parameter so the Windows behaviour is testable from a
    POSIX machine, which is the only way this branch gets exercised before
    somebody actually runs Cratekit on Windows.

    The leading slash is added only on the non-POSIX branch. A Windows absolute
    path opens with a drive letter rather than a separator, so the URL path needs
    one prepended; a POSIX absolute path already has it, and prepending
    unconditionally would quietly turn a relative path into an absolute-looking
    one instead of leaving it visibly wrong.
    """
    if separator == "/":
        return path
    converted = path.replace(separator, "/")
    return converted if converted.startswith("/") else "/" + converted


def location_url(abs_path: Path | str, *, separator: str = os.sep) -> str:
    """Build the rekordbox ``Location`` attribute for an absolute path.

    NFC first, then percent-encode, then lowercase the escapes. The order
    matters and is asserted: encoding first would preserve whichever composition
    form the filesystem happened to hand back, and KTD27 says a Location that
    differs from rekordbox's own by one byte duplicates the collection row
    rather than matching it.
    """
    text = _native_to_url_path(str(abs_path), separator=separator)
    encoded = quote(norm_for_compare(text), safe=REKORDBOX_SAFE_CHARS)
    return _LOCALHOST_PREFIX + _UPPERCASE_ESCAPE.sub(lambda m: m.group(0).lower(), encoded)


def looks_like_location(value: str) -> bool:
    """True when ``value`` is a URL rather than a plain filesystem path.

    Used to decide whether percent-decoding is safe. It is not always safe: a
    real filename may contain the literal text ``%20``, and decoding it turns
    that file into a different, non-existent file. The source system worked
    around this in one caller with an inline ``'://' not in fp`` test; the guard
    belongs in the primitive, because the caller that forgets it is the one that
    reports a present file as missing.
    """
    return "://" in value


def location_to_path(location: str) -> str:
    """Decode a rekordbox ``Location`` (or pass through a plain path) to a path.

    Always returns NFC, so the result is directly comparable to any other value
    that went through :func:`norm_for_compare`.

    Four inputs, deliberately distinguished:

    * ``file://localhost/...`` and ``file:///...``, the two spellings rekordbox
      has used, both decoded;
    * ``file://<other host>/...``, refused rather than mangled into a path;
    * anything else, treated as a value that is already a path. It is normalized
      but NOT percent-decoded, so a filename containing a literal ``%20`` is
      preserved. Streaming pseudo-locations, which are not paths at all, take
      this branch untouched.
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


# ---------------------------------------------------------------------------
# Recorded-path resolution: the volume prefix map
# ---------------------------------------------------------------------------
#
# rekordbox records a path once, at import, and keeps recording it after the
# volume is renamed or remounted somewhere else. In the library this was measured
# against, most active rows still carry a volume name the drive has not used for
# a long time. A resolver that does not know that resolves none of them, and a
# resolver that "helpfully" swaps in the current root without being told to would
# be inventing a fact.
#
# So the map is DECLARED configuration (S1, owned by the config schema) and this
# module CONSUMES it as a parameter. Two properties are load-bearing:
#
#   * Ordered, first match wins. One prefix can be another prefix's prefix, and
#     an unordered mapping resolves that pair differently depending on iteration
#     order, which is a bug that appears and disappears between runs.
#   * Anchored. The source system used ``str.replace``, which is unanchored and
#     rewrites EVERY occurrence: a path that happens to contain the old volume
#     name deeper down comes back corrupted rather than unresolved.
#
# One ordering question this answers rather than sidesteps: does the prefix
# rewrite happen before or after NFC normalization? Neither, because BOTH sides
# are normalized. Normalizing only the path would leave a rule whose configured
# prefix was typed in the other composition form unmatchable, and a volume named
# with an accent is entirely ordinary. Normalizing both makes the order stop
# mattering, which is a better answer than picking one and documenting it.
#
# Resolution and existence are also kept apart. The source fused them into one
# function returning None for both "no rule matched" and "the file is gone",
# which makes an unmapped prefix indistinguishable from a deleted file. Deletion
# needs those to be different categories: one is a bug in configuration, the
# other is a file the user may be asked to move to the Trash.


@dataclass(frozen=True)
class PrefixRule:
    """One anchored rewrite: paths under ``source`` are rewritten under ``target``.

    Both sides are NFC-normalized on construction. A user may type a configured
    prefix in either composition form, and a rule that only matches the form it
    was typed in is a rule that silently stops matching.

    ``volume_id`` is the recorded identity of the volume ``target`` sits on, and
    resolution never reads it. It rides here because a destructive pass needs the
    rule and the proof of where the rule points to be ONE value: carried beside
    the rules in a second list, the two are joined by position, and a list that
    is filtered or reordered on one side asserts the wrong disk for every rule
    after the change.
    """

    source: str
    target: str
    volume_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source", norm_for_compare(self.source).rstrip("/"))
        object.__setattr__(self, "target", norm_for_compare(self.target).rstrip("/"))


class Resolution(str, Enum):
    """Why a recorded path resolved the way it did.

    A structured token rather than a message, so a caller can branch on it and
    the CLI layer can render it. The one that matters most is ``UNMAPPED``: the
    plan requires an unmapped prefix to be REPORTED, never guessed at.
    """

    UNDER_ROOT = "under_root"
    REMAPPED = "remapped"
    UNMAPPED = "unmapped"
    NOT_A_PATH = "not_a_path"


@dataclass(frozen=True)
class ResolvedPath:
    """The outcome of resolving one recorded path.

    ``path`` is None for every status except ``UNDER_ROOT`` and ``REMAPPED``.
    That is not defensiveness, it is the split the deletion review depends on: a
    caller cannot accidentally treat an unresolved row as a resolved one, because
    there is no path there to treat.
    """

    resolution: Resolution
    path: str | None = None
    rule_index: int | None = None
    prefix: str | None = None


def leading_prefix(path: str, *, components: int = 2) -> str | None:
    """The first ``components`` components of an absolute path, for reporting.

    Mount roots are spelled differently on every platform, so this counts
    components instead of naming any of them. It is what the doctor check groups
    unresolved rows by, so the user is shown "these 8554 rows record this prefix"
    rather than 8554 individual failures.
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

    The component boundary is the whole point. ``/x/Old`` must not match
    ``/x/OldArchive/track.flac``: they are different directories that happen to
    share a string prefix, and rewriting the second one produces a path that
    points at nothing while claiming to be resolved.
    """
    if not prefix:
        return False
    return path == prefix or path.startswith(prefix + "/")


def prefix_rules(pairs: Sequence[tuple[str, str]]) -> tuple[PrefixRule, ...]:
    """The rules a resolved prefix map becomes, in declared order.

    ``pairs`` is what ``Config.resolved_prefix_map`` answers. Named once here so
    a caller that resolves recorded paths does not rebuild the same three lines
    and drift from the rest when the rule's construction changes.
    """
    return tuple(PrefixRule(source, target) for source, target in pairs)


def resolve_recorded_path(
    recorded: str,
    *,
    root: Path | str,
    prefix_map: Sequence[PrefixRule] = (),
) -> ResolvedPath:
    """Resolve a path recorded by rekordbox into a path on this machine.

    Existence is deliberately NOT checked here. The caller asserts that
    separately, so "no rule maps this prefix" and "the file is gone" stay
    distinguishable; fusing them is how a configuration error gets reported as a
    missing file.
    """
    path = norm_for_compare(str(recorded))
    root_text = norm_for_compare(str(root)).rstrip("/")

    if not path.startswith("/"):
        # A streaming pseudo-location or a device-relative path. Not something
        # this machine can resolve, and not a failure either.
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
