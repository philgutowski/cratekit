"""What a list line asks: the states, the reasons, and every fold and identity (U305).

Split from :mod:`cratekit.acquire.match`, which re-exports every public name.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Mapping
from enum import StrEnum

from cratekit.core import naming, tags
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

# ---------------------------------------------------------------------------
# The states, and the reasons
# ---------------------------------------------------------------------------


class MatchState(StrEnum):
    """R11's three states, plus what suppression is.

    The payload values are spelled as the ``match`` surface's field names, so the
    payload is derived from this enum; a fourth state fails ``PAYLOAD_STATES``.
    """

    MATCHED = "matched"
    NEEDS_REVIEW = "needs_review"
    MISSING = "missing"
    #: Not one of R11's three: what acquisition may do, not how the match resolved.
    SUPPRESSED = "suppressed"


#: The three states the ``match`` payload carries, in order. Consumers derive keys here.
PAYLOAD_STATES: tuple[MatchState, ...] = (
    MatchState.MATCHED, MatchState.NEEDS_REVIEW, MatchState.MISSING,
)


class Why(StrEnum):
    """Why a track landed where it did. Stable slugs, never sentences (R19).

    A decision is recorded against the slug, so rewording the rendered sentence
    must not move it.
    """

    #: The library holds this exact version.
    EXACT = "exact"
    #: A held file carries this row's ISRC. Not "exact", since the artist tag may
    #: list every credited artist where the row names one.
    ISRC_EXACT = "isrc-exact"
    #: Held under the credited list rule: the row's primary artist is one member of
    #: the file's artist tag. Not "exact", since the recording token never agreed.
    CREDITED_EXACT = "credited-exact"
    #: A person already said one of the owned versions is this record.
    VERDICT_ACCEPTED = "verdict-accepted"
    #: A person already said none of them is.
    VERDICT_REJECTED = "verdict-rejected"
    #: The recording is owned, the version is not. R11's whole point.
    VERSION_DIFFERS = "version-differs"
    #: Only a scored, approximate hit on the recording. Discovery, never identity.
    TITLE_APPROXIMATE = "title-approximate"
    #: The title parses two ways and the library holds the other reading exactly.
    #: Evidence, not a parse, so it costs one question rather than a match.
    READING_AMBIGUOUS = "reading-ambiguous"
    #: Same Camelot number, different letter. Its own slug because it looks like
    #: agreement to anything comparing wheel positions.
    KEY_RELATIVE = "key-relative"
    #: The two keys disagree outright.
    KEY_DIFFERS = "key-differs"
    #: Nothing in the library resembles it.
    NOT_IN_LIBRARY = "not-in-library"
    #: A tombstone stands over this exact version (R36).
    TOMBSTONED = "tombstoned"
    #: A verdict names a candidate the library no longer offers. Nobody's verdict is
    #: cleared for them, so the track is presented again with the item named.
    CANDIDATE_GONE = "candidate-gone"
    #: An acceptance naming no candidate while several are on offer. Guessing which
    #: is the silent join this unit exists to prevent.
    VERDICT_UNSPECIFIC = "verdict-unspecific"


#: The whys under which resolution owns a row on its own evidence. A row matched
#: under one retires any question an earlier run filed about the line; any other
#: why does not, since ``VERDICT_ACCEPTED`` applies a person's answer and that
#: retires nothing. A set, so a new owning rule retires only when added on purpose.
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT, Why.CREDITED_EXACT})

#: The kind a version-match question is offered under. Every producer uses this one
#: spelling, or two spellings become two items for one candidate.
QUESTION_KIND = "version-match"

#: What a question is about, as stable identifiers inside the review item identity.
#: Never display names (R19), since an answer is recorded against one.
ASKS_ABOUT_KEY = "key"
ASKS_ABOUT_VERSION = "version"
ASKS_ABOUT_RECORDING = "recording"
ASKS_ABOUT_READING = "reading"

#: The whys whose question is about the key. Read by :func:`question_shape`, so a
#: key question and a version question about one recording are two items.
KEY_QUESTIONS: frozenset[Why] = frozenset({Why.KEY_RELATIVE, Why.KEY_DIFFERS})

#: Every other why that is a question, and what it is about. No default: a why
#: missing here is not a question, and a shape would make it answerable.
_QUESTION_SHAPES: Mapping[Why, str] = {
    Why.VERSION_DIFFERS: ASKS_ABOUT_VERSION, Why.TITLE_APPROXIMATE: ASKS_ABOUT_RECORDING,
    Why.READING_AMBIGUOUS: ASKS_ABOUT_READING,
}


def question_shape(why: Why) -> str:
    """Which question this row is, as the identifier the item identity carries.

    A question's identity is the list line plus which question is asked; without
    the second half a version answer settled a later key question about the same
    line. Nothing about the library enters it, so one line opens one item on any
    machine. Both key whys share one shape, since which fires depends on the disk;
    :func:`apply_verdict` binds an unspecific acceptance to its offered candidate.
    See the residual titled "A question answered on one machine does not settle a
    different question about the same line".

    A why with no shape is refused: matched, missing and the two stalled whys are
    not questions, and a default would make them answerable.
    """
    if why in KEY_QUESTIONS:
        return ASKS_ABOUT_KEY
    shape = _QUESTION_SHAPES.get(why)
    if shape is None:
        raise refuse(
            "review-selection-invalid",
            f"{why} is not a question, so it has no review item identity; "
            f"giving it one would file a result in the queue under an "
            f"identifier somebody could answer",
            remedy=Remedy.REPORT_DEFECT, scope=Scope.ITEM, origin=("acquire.match",),
            detail={"why": str(why)},
        )
    return shape

#: The kind a tombstone is recorded under, U24's ``cratekit.core.tombstone.KIND_VERSION``
#: replicated byte for byte until it can be imported. The deletion and acquisition
#: passes are both toggleable, so the identity belongs in the domain layer.
#: ``test_the_tombstone_identity_is_u24s_algorithm_byte_for_byte`` pins it.
TOMBSTONE_KIND = "version"

#: The companion kind of a credited tombstone, ``KIND_VERSION_UNCREDITED`` replicated
#: as above: written beside the tombstone of a row whose title carried a featured
#: credit, addressed with the credit groups out. See :attr:`Wanted.uncredited_spellings`.
UNCREDITED_KIND = "version-uncredited"


# ---------------------------------------------------------------------------
# Folding: one spelling per value, so one candidate is one decision
# ---------------------------------------------------------------------------

_MARKS = re.compile(r"[^\w\s]", re.UNICODE)
_RUNS = re.compile(r"\s+")

#: The first words that make a trailing bracketed group a performer credit. Credits
#: come off the title because listings disagree about where the guest goes, and stay
#: out of the version because a guest is not an edit. Whole words (U262), so
#: ``Without`` is not ``with``. A copy of ``core.tombstone._CREDIT_MARKERS``, held
#: equal by a test, since that set sits inside the deletion identity stamp.
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})

#: Version qualifiers that mean no qualifier at all. Deliberately short: "album
#: version" is often a different cut, and folding it would join two versions.
_NULL_VERSIONS: frozenset[str] = frozenset({"original", "original mix", "original version"})

#: A leading list ordinal, "1. " or "12) ". Not "03 - ", which an artist named by a
#: number would also match.
_ORDINAL = re.compile(r"^\s*\d{1,3}\s*[.)]\s+")

#: One trailing bracketed group, applied right to left repeatedly.
_TRAILING_GROUP = re.compile(r"\s*[(\[]([^()\[\]]*)[)\]]\s*$")


def fold(text: object) -> str:
    """One canonical spelling of a value, for hashing and comparison.

    Case, accents and punctuation come off; word boundaries stay, so "Re Mix" and
    "Remix" do not collide and silently merge two candidates.
    """
    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _RUNS.sub(" ", _MARKS.sub(" ", stripped.casefold())).strip()


#: Code points a bare title leaves out, added or dropped without changing what it
#: says: variation selectors and invisible format characters. Tag characters, which
#: spell a regional flag, are kept, since two flags are two titles.
_TAG_CHARACTERS = range(0xE0000, 0xE0080)
_VARIATION_SELECTORS = (range(0xFE00, 0xFE10), range(0xE0100, 0xE01F0))


def _invisible(ch: str) -> bool:
    point = ord(ch)
    if any(point in selectors for selectors in _VARIATION_SELECTORS):
        return True
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS


def bare_title(title: object) -> str:
    """A title's own text, for a title :func:`fold` reduces to nothing.

    ``""`` when the title folds to something. Otherwise NFKC with spaces and
    invisible characters removed, so ``❤`` and ``❤️`` are one title and ``🔥`` and
    ``💧`` are two. No casefold, since such a title holds no letter.
    """
    if fold(title):
        return ""
    composed = unicodedata.normalize("NFKC", str(title))
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))


def title_identity(title: object) -> str:
    """What one title is to the matcher: its fold, or ``"\x1f"`` and its bare text.

    The fold is unchanged wherever it says anything, so no identity moves. Titles
    of emoji or marks alone get their bare text, so two of them are not one title.
    The separator is one :func:`fold` never leaves. No text at all stays ``""``.
    """
    folded = fold(title)
    if folded:
        return folded
    bare = bare_title(title)
    return f"\x1f{bare}" if bare else ""


def same_title(one: object, other: object) -> bool:
    """Whether two titles are one title to the matcher."""
    return title_identity(one) == title_identity(other)


def _is_a_credit(inside: str) -> bool:
    """Whether a bracketed group names a performer rather than an edit.

    One place, so :func:`split_version` and :func:`_credits_in` agree. The group's
    first whole folded word is a marker (U262), as ``core.tombstone._is_a_credit``
    asks: ``(feat. Anna)`` is a credit, ``(Without You Remix)`` and ``(Live with
    Strings)`` are versions.
    """
    words = fold(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS


def _names_a_version(inside: str) -> bool:
    """Whether a bracketed group's last word is in the version vocabulary (U213)."""
    words = fold(inside).split()
    return bool(words) and words[-1] in _DASH_VERSIONS


def split_version(title: str) -> tuple[str, str]:
    """The bracketed half of the split only; readers call :func:`split_title`.

    Trailing bracketed groups are walked off, credits dropped, the rest kept as the
    version. A group that is all the title has left is the title (U213), brackets
    dropped, since a qualifier needs a title to qualify, unless it names a version,
    which is a row that lost its title and stays refused.
    """
    remaining = str(title).strip()
    qualifiers: list[str] = []
    while True:
        found = _TRAILING_GROUP.search(remaining)
        if found is None:
            break
        inside = found.group(1).strip()
        if found.start() == 0 and not _names_a_version(inside):
            remaining = inside
            break
        remaining = remaining[: found.start()].strip()
        if _is_a_credit(inside):
            continue
        if inside:
            qualifiers.append(inside)
    return remaining, " ".join(reversed(qualifiers))


#: What makes a word a version designation: U24's ``cratekit.core.tombstone.VERSION_WORDS``
#: replicated until it can be imported, since the deletion pass and this dash reader
#: answer one question and two vocabularies let a held file read missing and be
#: fetched again. A word wrongly here costs only a question, because an ambiguous
#: reading is taken only when the library holds exactly it (:func:`split_ambiguous`).
#: ``test_the_version_vocabulary_is_u24s_element_for_element`` pins it; see the
#: residual titled "One vocabulary lives in two files until the domain module merges".
VERSION_WORDS: frozenset[str] = frozenset(
    {
        "acapella", "acoustic", "alternate", "bootleg", "club", "cut", "demo", "dub", "edit",
        "extended", "flip", "instrumental", "interlude", "live", "mashup", "mix", "original",
        "radio", "remaster", "remastered", "remix", "reprise", "rework", "session", "unplugged",
        "version", "vip",
    }
)

#: Words that start a dash version tail, for "Remastered 2011" where the year comes
#: last. Tiny, since a leading word rule is loose, and the only words that make a
#: one word tail a version. ``rerecorded`` is this side's alone, not drift.
_DASH_VERSION_HEADS: frozenset[str] = frozenset({"remaster", "remastered", "rerecorded"})

#: Words that end a dash tail naming a version, so "Sun Path - Nightwave Remix"
#: splits and "Sun - Rise" does not. Derived, so the two sources cannot diverge.
_DASH_VERSIONS: frozenset[str] = VERSION_WORDS | _DASH_VERSION_HEADS

#: The separator the public playlist API puts before a version, and the one
#: ``read_text_lines`` splits artist from title on, at the other end of the line.
_DASH = " - "


def _is_a_version(tail: str) -> bool:
    """Whether a dash tail names a version, as far as the string alone can say.

    True for a tail led by a head word, or a multi word tail ending in the
    vocabulary. A bare one word tail is ambiguous ("Sun Path - Live" against
    "Ziggy Stardust - Reprise") and the library settles it, in
    :func:`split_ambiguous`. Words are counted raw, so "Re-Mix" is one word.
    """
    raw = str(tail).split()
    words = fold(tail).split()
    if not words:
        return False
    if words[0] in _DASH_VERSION_HEADS:
        return True
    return len(raw) > 1 and words[-1] in _DASH_VERSIONS


def split_ambiguous(title: str) -> tuple[str, str] | None:
    """The other reading of a bare one word dash tail, or None when there is none.

    No rule over the string tells "Sun Path - Live" from a record of that name, so
    the library decides: the split reading is taken only when it holds exactly that
    head at that version (:attr:`Wanted.readings`, :func:`resolve_one`).
    """
    remaining, bracketed = split_version(title)
    head, separator, tail = remaining.rpartition(_DASH)
    if not separator or not head.strip() or _is_a_version(tail):
        return None
    if len(str(tail).split()) != 1:
        return None
    words = fold(tail).split()
    if not words or words[-1] not in _DASH_VERSIONS:
        return None
    return head.strip(), " ".join(part for part in (tail.strip(), bracketed) if part)


def split_title(title: str) -> tuple[str, str]:
    """A listing's title as (title, version), reading brackets then a dash.

    The dash pass exists because the public playlist API ships ``Sun Path -
    Nightwave Remix``, and one recording must fold to one identity whatever the
    source. It is guarded by a vocabulary, so "Sun - Rise" stays whole, and leaves
    a bare one word tail in the title for :func:`split_ambiguous`. The vocabulary
    is English: see the residual titled "Four accepted findings from the second
    U16 review, recorded rather than fixed", item 2.
    """
    remaining, bracketed = split_version(title)
    head, separator, tail = remaining.rpartition(_DASH)
    if not separator or not head.strip() or not _is_a_version(tail):
        return remaining, bracketed
    return head.strip(), " ".join(part for part in (tail.strip(), bracketed) if part)


def recording_token(artist: str, title: str) -> str:
    """The folded identity of a recording, version excluded.

    Joined by a separator folding never produces, so two splits of the same
    characters cannot collide.
    """
    return f"{fold(artist)}\x1f{fold(title)}"


def recording_identity(artist: str, title: str) -> str:
    """:func:`recording_token` with the title read by :func:`title_identity`.

    Equal to the token wherever the title folds to something. The token keys the
    index and the approximate pass; this tells recordings apart in every identity.
    """
    return f"{fold(artist)}\x1f{title_identity(title)}"


#: The whitespace ``rapidfuzz``'s token scorers split a string on when every
#: character is below U+0100: Python's whitespace except NEL and the no break
#: space. A wider string splits on exactly Python's whitespace (U265), held by
#: ``test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on``.
_NARROW_SPACE = re.compile(r"[^\S\x85\xa0]+")


def _sorted_words(token: str) -> str:
    """A token's words sorted and space joined, as ``fuzz.token_sort_ratio`` builds it (U265).

    Split where the scorer splits for the string's width, sorted by code point.
    """
    if token and max(token) > "\xff":
        words = token.split()
    else:
        words = [word for word in _NARROW_SPACE.split(token) if word]
    return " ".join(sorted(words))


def version_token(version: str) -> str:
    """The folded identity of a VERSION, with the no-op qualifiers folded away."""
    folded = fold(version)
    return "" if folded in _NULL_VERSIONS else folded


class Recorded:
    """The tokens of a row with an artist, a title and a version, list or library alike.

    :class:`~cratekit.acquire.match_list.Wanted` and
    :class:`~cratekit.acquire.match_library.Owned` both read these, so a list
    row and a held file fold through one definition and agree by construction.
    """

    __slots__ = ()

    @property
    def recording(self) -> str:
        return recording_token(self.artist, self.title)

    @property
    def distinct(self) -> str:
        """The recording's :func:`recording_identity`; every identifier hashes this."""
        return recording_identity(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)


def key_token(key: str | None) -> str:
    """The canonical spelling of a Camelot code, or ``""`` for anything else.

    ``8A``, ``08A`` and ``08a`` are one key. Absent and unparseable codes both fold
    to ``""``, since :func:`key_disagreement` treats them alike.
    """
    parsed = naming.parse_camelot(str(key)) if key else None
    return "" if parsed is None else f"{parsed[0]:02d}{parsed[1]}"


# The one ISRC fold and identity live with the tag reader since U212; named here
# for the callers that have always asked this module.
fold_isrc = tags.fold_isrc
isrc_token = tags.isrc_token


def credited_members(artist: str) -> tuple[str, ...]:
    """The names a comma separated artist tag credits, each stripped, in order.

    The one place a comma splits an artist, safe because it is used for
    membership, never identity: a comma inside one name can lose a match, not
    invent one.
    """
    return tuple(part for part in (piece.strip() for piece in str(artist).split(",")) if part)


def listed_title(title: str, version: str) -> str:
    """A title and a separate version put back into one string.

    Only for a source that carried the version in its own field; parentheses, as a
    library row uses. Any other source's original string is what gets hashed.
    """
    return f"{title} ({version})" if str(version).strip() else str(title)


def _head_of(spelled: str, version: str) -> str:
    """``spelled`` with only its bracketed version suffix removed.

    Not :attr:`Wanted.title`, which has lost its credits, so a lookup composed from
    it would let a deletion of the plain record withhold the credited one. ``""``
    when the version is not a bracketed suffix; the caller's fallback is checked by
    :attr:`Wanted.addresses`.
    """
    text = str(spelled).strip()
    qualifier = str(version).strip()
    if not qualifier:
        return text
    for shape in ("({})", "[{}]"):
        suffix = shape.format(qualifier)
        if text.casefold().endswith(suffix.casefold()):
            return text[: len(text) - len(suffix)].strip()
    return ""


#: A bracketed group anywhere in a title, since ``Sun Path (feat. Mira) - Live``
#: carries its credit in the middle.
_ANY_GROUP = re.compile(r"[(\[]([^()\[\]]*)[)\]]")


def _credits_in(text: str) -> tuple[str, ...]:
    """Every performer credit a spelling carries, folded, left to right.

    Folded, so ``(feat. Mira)`` and ``(Feat Mira)`` are one credit.
    """
    return tuple(
        fold(found.group(1))
        for found in _ANY_GROUP.finditer(str(text))
        if _is_a_credit(found.group(1))
    )


def _equivalent_versions(version: str) -> tuple[str, ...]:
    """Every version text naming the same version as this one.

    For a null version, every spelling :data:`_NULL_VERSIONS` declares equal, so
    ``Sun Path`` and ``Sun Path (Original Mix)`` reach each other's tombstones.
    """
    if version_token(version):
        return (str(version).strip(),)
    return ("", *sorted(_NULL_VERSIONS))


def _spellings_of(head: str, version: str) -> tuple[str, ...]:
    """Every title string a library row could carry for this head and version.

    Brackets always, including every split over two groups, since each folds back
    to the same version. The dash form only when :func:`split_title`, not
    :func:`split_ambiguous`, reads it back as this head and version, so no lookup
    is composed under a name that could be another record: an over eager
    suppression withholds music silently (see :func:`tombstone_fold`).
    """
    if not version:
        return (head,)
    built = [f"{head} ({version})", f"{head} [{version}]"]
    words = version.split()
    for cut in range(1, len(words)):
        built.append(f"{head} ({' '.join(words[:cut])}) ({' '.join(words[cut:])})")
    dashed = f"{head}{_DASH}{version}"
    if split_title(dashed) == (head, version):
        built.append(dashed)
        # U24 composes a row whose dash title repeats its version column into
        # ``Sun Path - Nightwave Remix (Nightwave Remix)``, so that is asked too.
        # Gated like the dash form, it names the same version.
        built.append(f"{dashed} ({version})")
    return tuple(built)


#: Whitespace runs for a tombstone identity. Separate from ``_RUNS`` so a change to
#: one fold cannot silently change the other.
_TOMBSTONE_SPACING = re.compile(r"\s+")


def tombstone_fold(value: object) -> str:
    """U24's ``cratekit.core.tombstone.fold``, replicated exactly.

    NFC, case, spacing; punctuation is kept, so ``Track (Live)`` and ``Track
    [Live]`` are two tombstones. A missed suppression re-acquires something and
    reports it, an over eager one silently withholds music somebody wants, and
    those costs are not comparable.
    """
    return _TOMBSTONE_SPACING.sub(
        " ", unicodedata.normalize("NFC", str(value)).casefold()
    ).strip()


def version_identity(*, artist: str, title: str) -> dict[str, str]:
    """What addresses one deleted version of one recording (R36, AE17).

    Byte for byte U24's ``core.tombstone.version_identity``, since any second
    spelling records a suppression this side never finds. Both fields always
    present; neither filled is refused, since every unnamed candidate would collide
    on one suppression. The version rides inside the title (:func:`listed_title`).
    """
    folded_artist = tombstone_fold(artist)
    folded_title = tombstone_fold(title)
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
            detail={"kind": TOMBSTONE_KIND},
        )
    return {"artist": folded_artist, "title": folded_title}


def question_identity(
    artist: str, title: str, version: str, key: str | None, why: Why
) -> dict[str, str]:
    """What addresses one review question about one recording.

    Not the tombstone's identity: a tombstone outlives every list, a question is
    one thing somebody was asked. Every value is the list line's own, the key
    included even when empty, never the library's, so one line is one item on
    every machine. The version and the shape (:func:`question_shape`) are in it so
    one answer cannot settle another version's or another kind's question.
    """
    return _identity_asking(artist, title, version, key, question_shape(why))


def _identity_asking(
    artist: str, title: str, version: str, key: str | None, asks: str
) -> dict[str, str]:
    """The identity of one question given its shape; the one spelling of the mapping."""
    return {
        # The recording's identity, so two emoji only titles are two items.
        "recording": recording_identity(artist, title),
        "version": version_token(version),
        "key": key_token(key),
        "asks": asks,
    }


#: Every shape a question can take, for :func:`every_question_identity`.
QUESTION_SHAPES: tuple[str, ...] = (
    ASKS_ABOUT_KEY,
    ASKS_ABOUT_VERSION,
    ASKS_ABOUT_RECORDING,
    ASKS_ABOUT_READING,
)


def every_question_identity(
    artist: str, title: str, version: str, key: str | None
) -> tuple[dict[str, str], ...]:
    """Every identity one list line can have been offered under, one per shape.

    For a row resolution now owns, which has no why: an earlier run may have filed
    a question under any shape, so the retiring side asks about all. One per shape,
    not per why, so the shared key shape is not counted twice.
    """
    return tuple(_identity_asking(artist, title, version, key, asks) for asks in QUESTION_SHAPES)


#: Hex characters of the digest every generated identifier carries (``match_id``,
#: ``candidate_id``, ``option_id``). Sixteen, 64 bits: a collision drops a row or
#: merges two candidates, and at 32 bits even odds arrive near 77,000 identifiers.
#: ``test_every_identifier_this_module_generates_is_the_declared_width`` pins it.
DIGEST_WIDTH = 16


def _digest(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:DIGEST_WIDTH]


def digest(*parts: str) -> str:
    """The one identifier digest, for a caller outside this module.

    Public so the intake queue's digest is this one rather than a copy with its
    own width.
    """
    return _digest(*parts)
