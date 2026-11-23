"""What a tombstone and a decline are ADDRESSED BY. One vocabulary, two readers.

R36: a completed deletion writes a tombstone for that exact version, and an
acquisition skips it and reports the suppression. The deletion pass RECORDS and
an acquisition pass CONSULTS, and deletion is a toggleable module, so the
identity lives here, below both.

**KTD16: a tombstone identifies a VERSION, not a recording.** The identity is the
artist and the title, and THE TITLE IS REQUIRED TO CARRY THE VERSION (AE17).
rekordbox files a mix name in ``RemixerName`` or ``Subtitle``, so a producer
holding it apart COMPOSES IT INTO THE TITLE through :func:`version_title`, and a
remixer, which is an artist name, is first spelled as a provider spells it by
:func:`remixer_title`. Composition is safe only because of what is fed to it,
since ``("Sun", "Sun Path")`` and ``("Sun (Sun Path)", "")`` land on one identity;
``Subtitle`` is believed only when it reads as a version (:data:`VERSION_WORDS`).

The collision that survives is bounded by the ISRC, in
``deletion.stores.ambiguous_versions``: one recording carries one code, a
collision two. THE ISRC IS NOT IN THE IDENTITY, since a provider candidate often
lacks one and an identity may hold only fields both sides always have.

Folding covers case, spacing and Unicode form and nothing else, so
``Track (Live)`` and ``Track [Live]`` differ. A missed suppression re-acquires
and REPORTS it; an over-eager one silently withholds music, the worse direction.

Layer note: DOMAIN. The stores live in ``cratekit.core.review``, opened on the
keys below, so a consult and a record cannot drift apart.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The tombstone state entry, spelled ONCE so the recorder and the consulter open
#: one store, with ``review.DecisionStore(tombstone.STORE_KEY, cfg)``.
STORE_KEY = "tombstones"

#: R35's other half, the files a person decided to keep, consulted in the same walk.
DECLINE_STORE_KEY = "declines"

#: The kind a tombstone carries: one deleted version of one recording.
KIND_VERSION = "version"

#: The kind the COMPANION of a credited tombstone carries, the same version with
#: its featured credits taken out (R-431). A SECOND KIND AND NOT A SECOND SPELLING,
#: so only a consulter asking for it by name reaches it, and the acquisition side
#: asks only for a listing that spelled no credit at all.
KIND_VERSION_UNCREDITED = "version-uncredited"

#: The kind a decline carries, a ROW's file rather than a version, so revoking a
#: decline never un-suppresses an acquisition.
KIND_REMOVED_FILE = "removed-file"

#: Runs of any whitespace collapse to one space, the only structural folding.
_SPACING = re.compile(r"\s+")

#: Every parenthesised or bracketed group, where a title keeps its mix name.
_BRACKETED = re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]")

#: Every non-alphanumeric, for :func:`fold_code`. ``[\W_]`` so a non-ASCII
#: alphanumeric survives, since merging two codes over-suppresses.
_NOT_A_CODE_CHARACTER = re.compile(r"[\W_]+", re.UNICODE)

#: Brackets inside a value about to be bracketed, replaced by a space.
_BRACKET_CHARACTERS = re.compile(r"[()\[\]]+")

#: The words that make a ``Subtitle`` a VERSION DESIGNATION, a closed list since
#: ``Extended Mix`` and ``Anjunadeep`` share a shape. Both error directions are
#: measured (U24): a missed designation collides two versions, over-suppression,
#: and a false one composes a tombstone no provider spelling matches. THE
#: MEMBERSHIP IS PINNED EXACTLY, since a list that can be narrowed silently is
#: pinned by nothing; flipping the default is recorded rather than done.
VERSION_WORDS = frozenset(
    {
        "acapella",
        "acoustic",
        "alternate",
        "bootleg",
        "club",
        "cut",
        "demo",
        "dub",
        "edit",
        "extended",
        "flip",
        "instrumental",
        "interlude",
        "live",
        "mashup",
        "mix",
        "original",
        "radio",
        "remaster",
        "remastered",
        "remix",
        "reprise",
        "rework",
        "session",
        "unplugged",
        "version",
        "vip",
    }
)

#: A NON-WORD split, so a vocabulary hit is a WORD and ``Re-Edit`` reads as two.
_WORD_SPLIT = re.compile(r"\W+", re.UNICODE)

#: The designation a provider appends to a remixer's name, named so it can be found.
REMIX_DESIGNATION = "Remix"


def already_spelled_as_a_remix(value: str) -> bool:
    """Whether appending :data:`REMIX_DESIGNATION` would write that word twice.

    **NO VOCABULARY IS CONSULTED.** ``RemixerName`` holds an ARTIST NAME, and an
    artist misread as a designation collides with a ``Subtitle``, over-suppression,
    so this rule never errs on an artist. It dominates appending unconditionally
    POINTWISE; the measurement over 65 values is U24's.
    """
    words = [word for word in _WORD_SPLIT.split(fold(value)) if word]
    return bool(words) and words[-1] == fold(REMIX_DESIGNATION)

#: Words opening a FEATURED CREDIT group, which names a guest and never a version.
_CREDIT_MARKERS = frozenset({"feat", "ft", "featuring", "with"})


def reads_as_version(value: str) -> bool:
    """Whether free text names a VERSION; its measured errors are on :data:`VERSION_WORDS`."""
    return bool(VERSION_WORDS.intersection(_WORD_SPLIT.split(fold(value))))


def fold(value: str) -> str:
    """One spelling of a free-text field, for identity purposes only.

    NFC, then case, then spacing, in a fixed order. Punctuation stays; a structured
    code wants :func:`fold_code`.
    """
    return _SPACING.sub(" ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


def fold_code(value: str) -> str:
    """One spelling of a STRUCTURED IDENTIFIER, for comparison only.

    ``GB-AYA-15-00001`` is the display form of ``GBAYA1500001`` (ISO 3901), and the
    free text fold read them as two recordings and wedged the queue. So NFKC, and
    every non-alphanumeric REMOVED. It never transliterates, since merging two
    codes is over-suppression.
    """
    return _NOT_A_CODE_CHARACTER.sub(
        "", unicodedata.normalize("NFKC", str(value)).casefold()
    )


def _already_carries(title: str, folded_version: str) -> bool:
    """Whether the title already names this version, AS A VERSION.

    DELIMITED by bracket and then by word boundary, so ``Live`` is not carried by
    ``Lively Up`` and ``Michael Woods`` is carried by ``(Michael Woods Remix)``.
    Lookarounds rather than ``\\b``, which means nothing beside a non-word character.
    A featured credit group is skipped, since a guest is never a version.
    """
    folded_title = fold(title)
    delimited = re.compile(rf"(?<!\w){re.escape(folded_version)}(?!\w)")
    return any(
        delimited.search(group)
        for match in _BRACKETED.finditer(folded_title)
        for group in match.groups()
        if group is not None and not _is_a_credit(group)
    )


def _is_a_credit(group: str) -> bool:
    """Whether a bracketed group names GUEST PERFORMERS, tested on its first word only."""
    words = _WORD_SPLIT.split(fold(group).strip())
    return bool(words) and words[0] in _CREDIT_MARKERS


def uncredited_title(title: str) -> str:
    """``title`` with every bracketed credit group taken out, or ``""``.

    EMPTY MEANS THERE IS NO COMPANION TO RECORD, for a title with no credit or one
    that is nothing but a credit. NOT REACHABLE FROM ``deletion.stores.version_of``
    AND IT MUST STAY THAT WAY, or the identity stamp moves.
    """
    dropped = False

    def keep_or_drop(found: re.Match[str]) -> str:
        nonlocal dropped
        group = found.group(1) if found.group(1) is not None else found.group(2)
        if _is_a_credit(group):
            dropped = True
            return " "
        return found.group(0)

    stripped = _SPACING.sub(" ", _BRACKETED.sub(keep_or_drop, str(title))).strip()
    return stripped if dropped else ""


def remixer_title(title: str, remixer: str) -> str:
    """The title a PROVIDER spells, for a producer holding a bare REMIXER name.

    ``RemixerName`` holds an ARTIST NAME, so ``Michael Woods`` is spelled ``Michael
    Woods Remix`` before composing, or every tombstone from that column misses.
    The append is skipped where it would say ``Remix`` twice
    (:func:`already_spelled_as_a_remix`), and a remixer the title already names,
    tested on the BARE name, is not composed at all.
    """
    folded = fold(remixer)
    if not folded or _already_carries(title, folded):
        return title
    spelled = remixer if already_spelled_as_a_remix(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    return version_title(title, spelled)


def _as_a_bracketed_value(version: str) -> str:
    """A column's value as it may appear inside a bracket, see :func:`version_title`."""
    return _SPACING.sub(" ", _BRACKET_CHARACTERS.sub(" ", str(version))).strip()


def version_title(title: str, version: str) -> str:
    """The title with the version in it, for a producer that holds the two apart.

    An empty version changes nothing, and one the title already carries, compared
    FOLDED, is not added twice. The value is TIDIED first, ends and brackets only,
    or a stray space or bracket in a column makes a second, unmatchable identity.
    """
    tidied = _as_a_bracketed_value(version)
    folded_version = fold(tidied)
    if not folded_version or _already_carries(title, folded_version):
        return title
    return f"{title} ({tidied})" if title else tidied


# HISTORY IS NOT RECOMPUTED HERE. A frozen composer calling live helpers drifts
# silently, so the recogniser asks the STORE what it holds, and
# ``deletion.stores.identity_scheme`` tells one era from another.


def version_identity(*, artist: str, title: str) -> dict[str, str]:
    """The identity of one version of one recording.

    Both fields are always present, so the key set never varies, and an identity
    empty in both is REFUSED, since it would suppress everything.
    """
    folded_artist = fold(artist)
    folded_title = fold(title)
    if not folded_artist and not folded_title:
        raise refuse(
            "review-selection-invalid",
            "a tombstone needs an artist or a title to identify the version it "
            "suppresses; an identity with neither collapses every version in the "
            "library onto one record, and afterwards nothing can tell that apart "
            "from the suppression working",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("tombstone",),
            detail={"kind": KIND_VERSION},
        )
    return {"artist": folded_artist, "title": folded_title}


def removed_file_identity(*, content_id: str, recorded: str) -> dict[str, str]:
    """The identity of one removed row's file, for a decline and a review item.

    ADDRESSED BY THE ROW AND THE PATH IT RECORDS, not the resolved path, so a
    re-pointed row is asked again and a remount changes no answer. ``None``, a
    boolean or a blank identifier is refused rather than read as ``'None'``,
    ``'False'`` or spaces, while ``0`` stays addressable.
    """
    if content_id is None or isinstance(content_id, bool) or not str(content_id).strip():
        raise refuse(
            "review-selection-invalid",
            "a removed row has to be identified by its collection row; without "
            "one, every removed file in the library addresses the same decision",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("tombstone",),
            detail={"kind": KIND_REMOVED_FILE},
        )
    return {"content_id": str(content_id), "recorded": unicodedata.normalize("NFC", str(recorded))}


def describe(identity: Mapping[str, Any]) -> str:
    """A one-line rendering of an identity, rewritable without orphaning a decision."""
    artist = str(identity.get("artist") or "")
    title = str(identity.get("title") or "")
    if artist or title:
        return f"{artist} - {title}" if artist and title else (artist or title)
    return str(identity.get("recorded") or identity.get("content_id") or "")

