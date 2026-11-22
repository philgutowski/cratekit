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

    The three payload values are spelled exactly as the ``match`` surface's
    field names, so the payload is DERIVED from this enum rather than written a
    second time. A fourth state added here without a payload decision fails
    ``PAYLOAD_STATES`` below rather than silently widening the envelope.
    """

    MATCHED = "matched"
    NEEDS_REVIEW = "needs_review"
    MISSING = "missing"
    #: Not one of R11's three. See the module docstring: this describes what
    #: acquisition may do, not how the match resolved.
    SUPPRESSED = "suppressed"


#: The three states the ``match`` payload carries, in the order it carries them.
#: A consumer of the payload derives its keys from here; nothing spells them
#: twice.
PAYLOAD_STATES: tuple[MatchState, ...] = (
    MatchState.MATCHED,
    MatchState.NEEDS_REVIEW,
    MatchState.MISSING,
)


class Why(StrEnum):
    """Why a track landed where it did. Stable slugs, never sentences.

    A reason is read by the next stage and by a person, so it is an identifier
    (R19). The sentence a person sees is rendered from it, and rewording that
    sentence must not change what a decision was recorded against.
    """

    #: The library holds this exact version.
    EXACT = "exact"
    #: The library holds a file carrying this row's ISRC. Identity by the one
    #: field both sides carry, and a slug of its own because "exact" would claim
    #: a text agreement that did not happen: the file's artist tag may list
    #: every credited artist where the row names one.
    ISRC_EXACT = "isrc-exact"
    #: The library holds this version under the credited list rule: the file's
    #: artist tag lists every credited artist and the row's primary artist is
    #: one of them. The same rationale as the slug above, applied the same way:
    #: the recording token never agreed, and "exact" would say it did.
    CREDITED_EXACT = "credited-exact"
    #: A person already said one of the owned versions is this record.
    VERDICT_ACCEPTED = "verdict-accepted"
    #: A person already said none of them is.
    VERDICT_REJECTED = "verdict-rejected"
    #: The recording is owned, the version is not. R11's whole point.
    VERSION_DIFFERS = "version-differs"
    #: Only a scored, approximate hit on the recording. Discovery, never identity.
    TITLE_APPROXIMATE = "title-approximate"
    #: The list spelled a title this module cannot parse one way, and the library
    #: holds the OTHER reading of it exactly. Evidence, and the strongest there
    #: is, but not a parse: "Sun Path - Live" and "Ziggy Stardust - Reprise" are
    #: one shape, so promoting the library's answer to a MATCH reports ownership
    #: of a record nobody checked. It costs one question instead.
    READING_AMBIGUOUS = "reading-ambiguous"
    #: Same Camelot number, different letter: the relative major or minor. It
    #: looks like agreement to anything comparing wheel positions, which is why
    #: it gets a slug of its own rather than folding into the one below.
    KEY_RELATIVE = "key-relative"
    #: The two keys disagree outright.
    KEY_DIFFERS = "key-differs"
    #: Nothing in the library resembles it.
    NOT_IN_LIBRARY = "not-in-library"
    #: A tombstone stands over this exact version (R36).
    TOMBSTONED = "tombstoned"
    #: A recorded verdict names a candidate the library no longer offers. The
    #: decision cannot be applied and this tool will not clear somebody's
    #: verdict for them, so the track is presented again with the item named.
    CANDIDATE_GONE = "candidate-gone"
    #: An acceptance that names no candidate while several are on offer. "One of
    #: these is the record" does not say which, and guessing is the silent join
    #: this whole unit exists to prevent.
    VERDICT_UNSPECIFIC = "verdict-unspecific"


#: The whys under which RESOLUTION owns a row on its own evidence, consulting no
#: queue and no person. A row matched under one of these retires any question an
#: earlier run filed about the same line, the residual titled "A review item
#: outlives its question: a later resolution that owns the row leaves the
#: version-match item open, and no verdict or predicate can retire it
#: honestly", and a matched row under any
#: OTHER why does not: ``VERDICT_ACCEPTED`` is a person's answer being applied,
#: and a person's answer retires nothing. Spelled as a set rather than read off
#: the state so the retiring side recognizes the rules positively, and a fourth
#: owning rule is added here on purpose or retires nothing.
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT, Why.CREDITED_EXACT})

#: The kind a version-match question is offered under. An identifier, normalized
#: by the queue on the way in, and the same one every producer of this question
#: must use or two spellings become two items for one candidate.
QUESTION_KIND = "version-match"

#: WHAT A QUESTION IS ABOUT, as stable identifiers that ride inside the review
#: item identity. Never display names (R19): a person's answer is recorded
#: against one of these, so rewording the sentence a person reads must not move
#: the item the answer lands in.
ASKS_ABOUT_KEY = "key"
ASKS_ABOUT_VERSION = "version"
ASKS_ABOUT_RECORDING = "recording"
ASKS_ABOUT_READING = "reading"

#: The whys whose question is ABOUT the key rather than about the version. Read
#: by the item identity, through :func:`question_shape`, so a key question and a
#: version question about one recording are two items and one answer never
#: settles the other.
#:
#: THAT SENTENCE WAS FALSE OF THE SHIPPED CODE FOR ONE ROUND and the set was
#: dead: repository-wide, only this definition and the ``__all__`` entry named
#: it. The round that removed the field this set used to gate left the set
#: standing with its docstring intact, so the file asserted a property it no
#: longer had, and one answer settled both questions again. See
#: :func:`question_shape`, which is the reader that makes the sentence true.
KEY_QUESTIONS: frozenset[Why] = frozenset({Why.KEY_RELATIVE, Why.KEY_DIFFERS})

#: Every OTHER why that is a question, and what it is about. Deliberately not a
#: default: a why that reaches :func:`question_shape` without an entry here is a
#: row that is not a question at all, and giving it a shape would file a
#: non-question in the queue under an identity somebody could answer.
_QUESTION_SHAPES: Mapping[Why, str] = {
    Why.VERSION_DIFFERS: ASKS_ABOUT_VERSION,
    Why.TITLE_APPROXIMATE: ASKS_ABOUT_RECORDING,
    Why.READING_AMBIGUOUS: ASKS_ABOUT_READING,
}


def question_shape(why: Why) -> str:
    """WHICH QUESTION this row is, as the identifier the item identity carries.

    THE IDENTITY OF A QUESTION IS A FUNCTION OF THE LIST LINE AND OF WHICH
    QUESTION IS BEING ASKED, and dropping the second half is what this exists to
    stop happening a third time. A round that made the item identity purely list
    derived collapsed the KEY question and the VERSION question about one
    recording onto ONE item, and the cost was measured end to end: a list line
    asking for ``Sun Path`` at 03A against a library holding only the extended
    mix is a VERSION question; somebody answers "yes, my extended mix is that
    record"; the library later gains the plain cut at 03B, the RELATIVE MINOR of
    the key the list asked for; and the next run reports MATCHED on the strength
    of the version answer, with the 03B file in ``paths``, the extended mix gone
    from them, exit zero, no warning and no question. ``Why.KEY_RELATIVE`` exists
    because 8A and 8B look like agreement to anything comparing wheel positions,
    and it had become reachable only while nobody had ever accepted anything
    about that line.

    WHAT THIS IS NOT is the defect the round before that one fixed. Nothing about
    the LIBRARY enters the identity: not a held file's key, not its version, not
    its path, not how many copies there are. ``question_identity``'s ``key`` is
    the LIST's key on every question, which is the property that lets one line
    open one item on two machines that hold different copies of it. What varies
    here is only WHICH QUESTION IS BEING ASKED, and two different questions are
    two items by definition, because an identity that covers both is an identity
    that is not unique to the thing it identifies.

    THE COST, taken deliberately and recorded. Two machines whose libraries make
    one list line ask two different questions open two items, so an answer
    exported from one does not settle the other. It should not: the second
    machine was never asked the first machine's question. See the residual titled
    "A question answered on one machine does not settle a different question
    about the same line".

    A why with no entry is REFUSED rather than given a default. A matched row and
    a missing row are not questions, so they have no question identity, and a
    default would hand one an identifier a person could answer. The two STALLED
    whys are refused for a narrower reason: they are written by
    :func:`apply_verdict` onto a row whose item was already found, so asking this
    about one means asking which question a rewritten answer was, which is a
    question with no answer.

    WHAT THIS DOES NOT DO, stated here because the round before this one wrote
    down the opposite and a measurement caught it. FOUR shapes, not five: both key
    whys map to :data:`ASKS_ABOUT_KEY`, so a key-differs question and a
    key-relative question about one line are ONE item, deliberately. Splitting
    them is not available, because which of the two fires is a function of what
    that machine's disk holds and an identity that reads the disk is the defect
    this function replaced. So an answer given while one of them was being asked
    IS read back while the other is being asked, and the identity cannot stop it.
    What stops it is :func:`apply_verdict`, which binds an unspecific acceptance
    to the candidate the item was offered with. See the residual titled "A
    question answered on one machine does not settle a different question about
    the same line", which records the measurement and the correction.
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
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("acquire.match",),
            detail={"why": str(why)},
        )
    return shape

#: The kind a tombstone is recorded under. NOT THIS MODULE'S TO CHOOSE, and the
#: correction is the most expensive thing this unit got wrong. R36's tombstone is
#: written by the deletion pass and consulted by an acquisition pass, and both of
#: those are toggleable feature modules, so an identity living inside either one
#: is absent exactly when the other needs it. It belongs in the DOMAIN layer,
#: which is where U24 puts it: ``cratekit.core.tombstone.KIND_VERSION``.
#:
#: This constant and :func:`version_identity` below are that module's algorithm
#: replicated byte for byte, because U24 is landing in its own worktree and this
#: unit cannot import a file that has not merged yet. THEY COLLAPSE INTO IMPORTS
#: the day it does::
#:
#:     from cratekit.core.tombstone import KIND_VERSION as TOMBSTONE_KIND
#:     from cratekit.core.tombstone import version_identity
#:
#: Until then ``test_the_tombstone_identity_is_u24s_algorithm_byte_for_byte``
#: pins the exact identifier, so the two cannot drift apart silently in the
#: window where two copies exist.
TOMBSTONE_KIND = "version"

#: The kind the COMPANION of a credited tombstone is recorded under, which is
#: ``cratekit.core.tombstone.KIND_VERSION_UNCREDITED`` replicated for the
#: reason :data:`TOMBSTONE_KIND` is, and compared against it by the same guard,
#: ``test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist``. The
#: deletion pass writes one beside the tombstone of a row whose title carried a
#: featured credit, addressed by that title with the credit groups taken out.
#: See :attr:`Wanted.uncredited_spellings` for who may ask under it.
UNCREDITED_KIND = "version-uncredited"


# ---------------------------------------------------------------------------
# Folding: one spelling per value, so one candidate is one decision
# ---------------------------------------------------------------------------

_MARKS = re.compile(r"[^\w\s]", re.UNICODE)
_RUNS = re.compile(r"\s+")

#: The FIRST WORDS that make a trailing bracketed group a PERFORMER credit rather
#: than a version. Credits come off the title because two listings of one record
#: disagree constantly about whether the guest is in the title or in the artist
#: field, and they are not folded into the version because a guest vocalist is
#: not an edit.
#:
#: WORDS AND NOT LETTERS (U262). This was a tuple of prefixes, ``"with "`` and
#: the rest, each ending on the space that made it a whole word, and the test
#: folded them before comparing, which took the space off. ``with`` then matched
#: the first letters of ``Without``, so ``Sun Path (Without You Remix)`` dropped
#: its remix as a credit, read as the plain record, and was reported owned and
#: never fetched; ``Withdrawn``, ``Within``, ``Feature`` and ``Featureless``
#: did the same. ``core.tombstone._CREDIT_MARKERS`` is this set, and
#: ``test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`` holds the
#: two equal. It is a copy rather than an import because the tombstone module's
#: set is inside the identity stamp ``deletion.stores.identity_scheme`` walks.
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})

#: Version qualifiers that mean "no qualifier at all". A record listed as the
#: original mix and the same record listed with nothing are one version, and
#: treating them as two asks a person to confirm a track against itself.
#: Deliberately short. "Album version" is NOT here: on plenty of releases it is
#: a genuinely different cut from the single, and folding it would silently join
#: two versions, which is the exact defect this unit exists to remove.
_NULL_VERSIONS: frozenset[str] = frozenset({"original", "original mix", "original version"})

#: A leading list ordinal in pasted text: "1. ", "12) ", "03 - " is NOT included
#: because a leading number followed by a dash is indistinguishable from an
#: artist whose name is a number.
_ORDINAL = re.compile(r"^\s*\d{1,3}\s*[.)]\s+")

#: One trailing bracketed group. Applied repeatedly, right to left, so
#: "Title (feat. X) (Someone Remix)" yields the remix as the version and drops
#: the credit.
_TRAILING_GROUP = re.compile(r"\s*[(\[]([^()\[\]]*)[)\]]\s*$")


def fold(text: object) -> str:
    """One canonical spelling of a value, for hashing and for comparison.

    Case, accents, and punctuation come off; word boundaries stay. That last
    part is the line: folding punctuation to NOTHING would make "Re Mix" and
    "Remix" the same token and would make two different titles collide, and a
    collision here silently merges two candidates onto one decision, which is
    the failure that cannot be noticed afterwards.
    """
    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _RUNS.sub(" ", _MARKS.sub(" ", stripped.casefold())).strip()


#: The code points a title's bare text leaves out: characters a
#: source adds or drops without changing what the title says. The variation
#: selectors, which pick text or emoji presentation of one symbol, and the
#: invisible format characters, the zero width space, joiner and non joiner,
#: the word joiner, the byte order mark, the soft hyphen and the directional
#: marks and controls. The tag characters, which spell a regional flag, are
#: format characters too and are KEPT, since two flags are two titles.
_TAG_CHARACTERS = range(0xE0000, 0xE0080)
_VARIATION_SELECTORS = (range(0xFE00, 0xFE10), range(0xE0100, 0xE01F0))


def _invisible(ch: str) -> bool:
    point = ord(ch)
    if any(point in selectors for selectors in _VARIATION_SELECTORS):
        return True
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS


def bare_title(title: object) -> str:
    """A title's own text, for the one case :func:`fold` cannot read.

    ``""`` for a title that folds to something, so the pair
    (``fold(title)``, ``bare_title(title)``) is exactly ``fold`` wherever
    ``fold`` says anything. For a title that folds to nothing, emoji or marks
    alone, the text itself: NFKC, which takes one title at another width or a
    compatibility form to one spelling (``！！！`` is ``!!!``, ``…`` is
    ``...``), then every space and every invisible character taken out (see
    :func:`_invisible`), so ``❤`` and ``❤️`` are one title and ``🔥`` and
    ``💧`` are two. NO CASEFOLD: such a title holds no letter, and over every
    code point folding to nothing case changes two Greek combining marks
    only, which compare equal either way, so a casefold here was dead code
    the mutation table could not kill.

    WHY NOT FOLD THEM IN. ``fold`` drops every mark on purpose, and the
    recording token the index is keyed by and the approximate pass scores
    stays the fold, so discovery is unchanged. What reads a title as one
    title, or hashes one into an identity, reads :func:`title_identity`.
    """
    if fold(title):
        return ""
    composed = unicodedata.normalize("NFKC", str(title))
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))


def title_identity(title: object) -> str:
    """What one title IS to the matcher: its fold, and for a title that folds
    to nothing, its bare text behind a unit separator.

    The fold, unchanged, for every title that folds to something, so every
    identity hashed from one is the identity it always was. A title that
    folds to nothing and has text is ``"\x1f"`` and its bare text: two
    titles of emoji or marks alone were ONE title to every comparison and
    every identity, so a wanted ``💧`` was called owned by a held ``🔥``,
    shared its review item, its match identifier and its search question
    with every other such title by the artist, and one answer or one
    dedupe settled them all. The separator is one :func:`fold` never
    leaves, so the value cannot equal any title's fold. A title with no
    text at all stays ``""``.
    """
    folded = fold(title)
    if folded:
        return folded
    bare = bare_title(title)
    return f"\x1f{bare}" if bare else ""


def same_title(one: object, other: object) -> bool:
    """Whether two titles are one title to the matcher. For every title that
    folds to something this is ``fold(one) == fold(other)``."""
    return title_identity(one) == title_identity(other)


def _is_a_credit(inside: str) -> bool:
    """Whether a bracketed group names a PERFORMER rather than an edit.

    ONE PLACE, because two callers ask it and a second copy would let them
    disagree about what a credit is. :func:`split_version` drops these from the
    version, and :func:`_credits_in` checks that a head this module composed from
    still carries every one the listing spelled, which is a check that means
    nothing if the two answer the question differently.

    THE GROUP'S FIRST WHOLE WORD, folded, and nothing else (U262), which is the
    rule ``core.tombstone._is_a_credit`` asks, over the same marker set but
    under this module's own :func:`fold`, so a group led by punctuation or
    spelled with an accent or in fullwidth letters can still answer differently
    there (a residual of U262's): ``(feat. Anna)``, ``(ft Anna)``
    and ``(with Anna)`` are credits, ``(Without You Remix)`` and ``(Feature
    Edit)`` are versions, and ``(Live with Strings)`` is a version because its
    marker is not first. The same answer as the letters test it replaced for
    every group whose first word IS a marker, so the only groups that moved are
    those whose first word merely begins with one. ``(Ft Worth Edit)`` reads as
    a credit under it, since ``Ft`` is the word ``ft``.
    """
    words = fold(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS


def _names_a_version(inside: str) -> bool:
    """Whether a bracketed group's last word is one the version vocabulary holds.

    The test :func:`split_version` asks of a group that stands first (U213),
    by the vocabulary the dash reader uses, so ``(Extended)`` stays a version
    and ``[Premade Sandwiches]`` is a title. Defined beside its one caller and
    read at call time, since the vocabulary is declared further down.
    """
    words = fold(inside).split()
    return bool(words) and words[-1] in _DASH_VERSIONS


def split_version(title: str) -> tuple[str, str]:
    """The BRACKETED half of the split, on its own. Not the reader's entry point.

    Only trailing bracketed groups are read here, and a dash is not looked at at
    all. That is a division of labour rather than a policy: :func:`split_title`
    is what the readers call and what reads both conventions, and this is the
    piece it starts with. The dash rule lives there, with the vocabulary that
    keeps it from splitting "Sun - Rise".

    Kept exported because it is the shape a caller wants when it already knows a
    string carries no dash convention, and because the two names differing by one
    word is a trap: if you want what a listing means by a title, call
    :func:`split_title`.

    A GROUP THAT IS ALL THE TITLE HAS LEFT IS THE TITLE (U213), its words kept
    and its brackets dropped. Glass Animals' ``[Premade Sandwiches]`` is a title
    written wholly in brackets, and walking it off like a qualifier left
    nothing: the provider row then read as naming no title and refused the
    whole ``crate sync twins`` run, and a library file tagged that way indexed
    under an empty title no row could reach. A qualifier needs a title to
    qualify, so the group that stands first is never one. NOT EVEN A CREDIT:
    the credit markers include ``with``, and ``[With You]`` or ``(With Or
    Without You)`` are titles, so excepting credits put the defect back for
    them (U213's review, round two). A row titled only ``(feat. Mira)`` reads
    as the title ``feat. Mira``, a residual. A GROUP THAT NAMES A VERSION
    STAYS ONE: ``(Extended)`` or ``[Original Mix]`` alone is a row that lost
    its title, refused as before, which U68's emitter pins (see
    :func:`_names_a_version`). Read here, in the one function every reader and
    the library index start from, so the two sides still fold one recording to
    one token.
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


#: What makes a word a VERSION DESIGNATION. NOT THIS MODULE'S TO CHOOSE either,
#: for exactly the reason :data:`TOMBSTONE_KIND` is not: the deletion pass decides
#: whether a rekordbox ``Subtitle`` names a version, this module decides whether a
#: dash tail names one, and those are two readers of ONE question. U24 puts the
#: answer in the domain layer as ``cratekit.core.tombstone.VERSION_WORDS`` and
#: this is that frozenset replicated element for element, because U24 is landing
#: in its own worktree and this unit cannot import a file that has not merged yet.
#: IT COLLAPSES INTO AN IMPORT the day it does::
#:
#:     from cratekit.core.tombstone import VERSION_WORDS
#:
#: TWO VOCABULARIES ANSWERING ONE QUESTION IS A DEFECT NO PASSING SUITE CAN SEE,
#: and it was live and measured. This module's own list held 17 words and U24's
#: held 27, so with the library holding ``Aurora Bloom - Sun Path (Unplugged)``
#: and a list spelling ``Aurora Bloom - Sun Path - Unplugged``, the run reported
#: MISSING with an acquisition option and went and fetched a file already on the
#: shelf, at exit zero, with nothing asked and nothing warned. That is verbatim
#: the failure :func:`_is_a_version` calls "the other half of the same mistake",
#: still live for eleven words. ``acapella``, ``alternate``, ``club``, ``cut``,
#: ``flip``, ``interlude``, ``mashup``, ``original``, ``radio``, ``session`` and
#: ``unplugged`` are those eleven.
#:
#: THE WIDENING IS SAFE IN THIS MODULE'S DIRECTION and it is worth saying which
#: direction that is, because it is not U24's. Over there a word believed wrongly
#: composes a parenthetical no provider spells, so a deletion fails to stick.
#: Here a word believed wrongly makes a one-word tail AMBIGUOUS rather than
#: split, and an ambiguous reading is only ever taken when the library holds
#: exactly that head at exactly that version: see :func:`split_ambiguous`. A word
#: this list should not hold therefore costs a question that the library already
#: had an answer for, and never a wrong join.
#:
#: ``test_the_version_vocabulary_is_u24s_element_for_element`` pins the exact
#: membership, so the two copies cannot drift in the window where two exist, and
#: the residual titled "One vocabulary lives in two files until the domain module
#: merges" carries the countdown.
VERSION_WORDS: frozenset[str] = frozenset(
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

#: Words that START a dash-introduced version tail, kept to the one convention
#: that needs it: the public playlist API ships "Remastered 2011" and "Remastered
#: Version", so the year is the last word and a trailing-word vocabulary cannot
#: see it. Deliberately tiny, since a leading-word rule is the loose one:
#: "Reprise Of Nothing" is a title.
#:
#: These are also the ONLY words allowed to make a one-word tail a version. See
#: :func:`_is_a_version`.
#:
#: ``rerecorded`` is here and is NOT in :data:`VERSION_WORDS`, which is a
#: difference between the two sides rather than a drift: U24 reads a free text
#: column and this reads a dash tail, and the leading-word convention is one this
#: side has and that side has no use for.
_DASH_VERSION_HEADS: frozenset[str] = frozenset({"remaster", "remastered", "rerecorded"})

#: Words that END a dash-introduced tail that is a VERSION rather than the rest
#: of a title. This is what separates "Sun Path - Nightwave Remix" from "Sun -
#: Rise". Deliberately a vocabulary rather than a shape: the shape is ambiguous,
#: so anything not recognized stays in the title, and the cost of a word this
#: list is missing is a question rather than a wrong join.
#:
#: DERIVED, never spelled a second time. The set is the domain vocabulary plus
#: the head words, so a word added to either one arrives here without anybody
#: remembering to add it twice, and the eleven-word divergence measured above
#: cannot reopen by an edit to one side.
_DASH_VERSIONS: frozenset[str] = VERSION_WORDS | _DASH_VERSION_HEADS

#: The separator the public playlist API puts before a version. The same three
#: characters ``read_text_lines`` splits an artist from a title on, which is why
#: the two readers apply it at different ends of the line.
_DASH = " - "


def _is_a_version(tail: str) -> bool:
    """Whether a dash-introduced tail names a version rather than ending a title.

    A ONE-WORD TAIL IS NOT ENOUGH TO DECIDE ON ITS OWN, and that is the whole of
    this rule. Matching on the last vocabulary word alone split every title whose
    final word happens to be one the vocabulary holds: "Ziggy Stardust -
    Reprise", "Hurt - Reprise", "Long - Live", "Studio 54 - Live", "Pump Up The
    Volume - Extended", "Nice Up - Dub", "Beat It - Demo", "Sunset - Acoustic".
    The reprise class is the sharpest, because an album reprise is a separate
    composition, so the mangle reframed it from "the library holds nothing like
    this" to "the library holds this record as a different version", and
    accepting that reports ownership of a track the library does not hold.

    REFUSING IT OUTRIGHT WAS THE OTHER HALF OF THE SAME MISTAKE, and it cost
    more. "Live", "Instrumental", "Acoustic", "Dub", "Demo", "Extended" and
    "Remix" are all real one-word tails the public playlist API ships, and a
    listing spelling one of them stopped converging with the provider row for the
    identical record: with the library holding "Sun Path (Instrumental)", the
    dash form scores 76.4 against a floor of 82 and reports MISSING with an
    acquisition option, so the run goes and fetches a file the library already
    holds, at exit zero, with nothing asked and nothing warned. The claim that a
    tail this misses "produces a question" is only true above the floor.

    AND THAT WAS THE MEASURED BEHAVIOUR OF ELEVEN WORDS UNTIL THIS ROUND, not a
    hazard argued in the past tense. This module kept a vocabulary of its own
    while the domain layer kept another, so ``Unplugged`` reported MISSING and
    re-acquired a held file while ``Live`` asked a question, for one library and
    one spelling convention. :data:`VERSION_WORDS` is now the domain layer's
    list and this module adds only its own head words to it.

    So the string alone does not decide it, and this function answers only the
    half a string CAN decide: a multi-word tail ending in the vocabulary, or one
    of the three head words the public playlist API uses on its own. The bare
    one-word case is genuinely ambiguous and is answered by the library instead,
    in :func:`split_ambiguous` and :func:`Wanted.readings`.

    WORDS ARE COUNTED RAW, not folded. Folding turns punctuation into spaces, so
    "Sun - Re-Mix" counted as two words and split; the tail is one word and the
    count has to be taken before anything rewrites it.
    """
    raw = str(tail).split()
    words = fold(tail).split()
    if not words:
        return False
    if words[0] in _DASH_VERSION_HEADS:
        return True
    return len(raw) > 1 and words[-1] in _DASH_VERSIONS


def split_ambiguous(title: str) -> tuple[str, str] | None:
    """The OTHER way a bare one-word dash tail reads, or None when there is none.

    "Sun Path - Live" is either a record called "Sun Path" in a live version or a
    record called "Sun Path - Live", and NO RULE OVER THE STRING CAN TELL THEM
    APART. Both of the previous attempts picked one and paid for it: splitting
    always mangled "Ziggy Stardust - Reprise", and refusing always reported a
    held track missing and re-acquired it.

    So neither is picked here. This returns the reading :func:`split_title`
    declined, and the library settles which one is true: see
    :attr:`Wanted.readings` and :func:`resolve_one`, where the split reading is
    taken ONLY when the library holds exactly that, the head at that version.
    Nothing weaker confirms it, because the library holding "Ziggy Stardust" says
    nothing at all about whether "Reprise" is a version or the end of a title.

    The tail is counted RAW and looked up FOLDED, for the reason
    :func:`_is_a_version` gives: "Re-Mix" is one word carrying a hyphen.
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
    """A listing's title, split into (title, version), reading BOTH conventions.

    The bracketed one first, then the dash. The dash pass exists because the
    public playlist API does not use brackets at all: it ships ``Sun Path -
    Nightwave Remix``, ``- Radio Edit``, ``- Remastered 2011``. Reading only the
    brackets made the same recording produce two different identities depending
    on which source the list came through, which is the three-reader convergence
    property failing at exactly the point it was written for, and the approximate
    pass did not rescue it: the dash spelling scores 72 against a floor of 82.

    The dash pass is GUARDED BY A VOCABULARY rather than by position, because a
    parser that split on any trailing dash would turn "Sun - Rise" into a record
    nobody released. Only a tail that names a version qualifier is read as one,
    and :func:`_is_a_version` says what that means.

    THIS FUNCTION IS THE CONSERVATIVE HALF AND NOT THE WHOLE ANSWER. A bare
    one-word tail is left in the title here, because from the string alone "Sun
    Path - Live" and "Ziggy Stardust - Reprise" are the same shape.
    :func:`split_ambiguous` returns the reading this one declined and the library
    settles it, so the one-word class converges when the library holds it and
    stays a whole title when it does not.

    THE VOCABULARY IS ENGLISH, so this convergence is English-only. A catalogue
    spelling its versions in another script converges through the bracketed
    reader and not through this one, which is recorded rather than hidden: see
    the residual titled "Four accepted findings from the second U16 review,
    recorded rather than fixed", item 2, in docs/residual-findings.md. CITED BY
    TITLE AND NOT BY NUMBER, because two branches have already given two
    different findings the same number and a citation by number cannot survive
    the merge that renumbers one of them.
    """
    remaining, bracketed = split_version(title)
    head, separator, tail = remaining.rpartition(_DASH)
    if not separator or not head.strip() or not _is_a_version(tail):
        return remaining, bracketed
    return head.strip(), " ".join(part for part in (tail.strip(), bracketed) if part)


def recording_token(artist: str, title: str) -> str:
    """The folded identity of a RECORDING, version excluded.

    Artist and title are joined through a separator that folding can never
    produce, so an artist whose name ends in the first word of a title cannot
    collide with a different split of the same characters.
    """
    return f"{fold(artist)}\x1f{fold(title)}"


def recording_identity(artist: str, title: str) -> str:
    """The identity of a RECORDING, version excluded: :func:`recording_token`
    with the title read by :func:`title_identity`.

    EQUAL TO THE TOKEN for every title that folds to something, so no
    recorded identity of one moves. The token stays what the index is keyed
    by and what the approximate pass scores; this is what tells two
    recordings apart, in every comparison and every identity hashed from one,
    so two titles of emoji alone by one artist are two recordings.
    """
    return f"{fold(artist)}\x1f{title_identity(title)}"


#: The whitespace ``rapidfuzz``'s token scorers split a NARROW string on, one
#: whose every character is below U+0100: everything Python calls whitespace
#: except NEL (U+0085) and the no-break space (U+00A0). A wider string, one
#: holding any character from U+0100 up, is split on exactly Python's
#: whitespace. Measured over every code point at all three of Python's string
#: widths, on rapidfuzz 3.14's compiled scorer, when U265 was built, and held
#: for every whitespace code point, every code point below U+3100 and both
#: sides of the U+00FF boundary by
#: ``test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on``.
#: :func:`fold` leaves neither character in a token, so this matters only for a
#: token that did not come through it, and then it is what keeps the score the
#: same.
_NARROW_SPACE = re.compile(r"[^\S\x85\xa0]+")


def _sorted_words(token: str) -> str:
    """A token's words sorted and joined by one space, which is the string
    ``fuzz.token_sort_ratio`` builds from it before it scores (U265).

    Split where the scorer splits, which depends on the string's width (see
    :data:`_NARROW_SPACE`), and sorted by code point, as the scorer sorts. The
    unit separator :func:`recording_token` joins artist and title with is
    whitespace to both this and the scorer at every width, so the artist's and
    the title's words sort together, exactly as they did inside the scorer.
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
        """The recording's identity, :func:`recording_identity`: the token for every
        title that folds to something, and what tells two titles of emoji or marks
        alone apart. Every identifier is hashed from this."""
        return recording_identity(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)


def key_token(key: str | None) -> str:
    """The canonical spelling of a Camelot code, or ``""`` for anything else.

    ``8A``, ``08A`` and ``08a`` are one key, and the library's own convention
    writes the padded form. An absent code and a code no parser recognizes both
    fold to the empty string, and that is not laziness: :func:`key_disagreement`
    reports nothing for either of them, so the two behave identically, and an
    identity that told them apart would open two questions with one answer.
    """
    parsed = naming.parse_camelot(str(key)) if key else None
    return "" if parsed is None else f"{parsed[0]:02d}{parsed[1]}"


# THE ONE FOLD AND THE ONE IDENTITY live with the tag reader since U212, so
# the write layer reads a file's ISRC through them too. Named here as well,
# because every caller above the tag reader has always asked this module.
fold_isrc = tags.fold_isrc
isrc_token = tags.isrc_token


def credited_members(artist: str) -> tuple[str, ...]:
    """The names a comma separated artist tag credits, each stripped, in order.

    A bare name with no comma is a list of one. THIS IS THE ONE PLACE A COMMA
    SPLITS AN ARTIST, and it is safe here for a reason :func:`_first_named`
    cannot claim: the split is used for MEMBERSHIP, never for identity. A row
    is held under this rule only when its primary artist is one whole member of
    the list AND the folded title agrees, so a comma inside a single artist's
    own name can lose a match and cannot invent one on its own.
    """
    return tuple(part for part in (piece.strip() for piece in str(artist).split(",")) if part)


def listed_title(title: str, version: str) -> str:
    """A title and a separate version qualifier, put back into one string.

    ONLY FOR A SOURCE THAT NEVER HAD ONE. A provider row carries the version in
    its own field, so there is no original spelling to preserve and something has
    to be composed; parentheses, because that is what a library row uses. Every
    other source hands over a title that already carries its version, and that
    ORIGINAL STRING is what gets hashed. See :attr:`Wanted.listed`.
    """
    return f"{title} ({version})" if str(version).strip() else str(title)


def _head_of(spelled: str, version: str) -> str:
    """``spelled`` with only its VERSION removed and everything else kept.

    NOT :attr:`Wanted.title`, and the gap between the two is a whole direction of
    failure. A featured credit is dropped from the matching title because it
    names a performer rather than an edit, but the library row a deletion
    recorded KEPT it, so composing a lookup from the stripped title asks the
    store about the plain no-qualifier record: a deletion of ``Sun Path`` then
    silently withholds ``Sun Path (feat. Mira)``. :func:`tombstone_fold` argues
    the whole cost asymmetry out loud, that a missed suppression re-acquires
    something and reports it while an over-eager one silently withholds music
    somebody wants, and a consult composed from the stripped title is the
    over-eager side of exactly that.

    Returns ``""`` when the version is not a bracketed suffix of the spelling,
    which is a spelling that carried its version in more than one group or put a
    credit AFTER it. The caller falls back to the matching title there, and that
    fallback is where the credit is lost, so it is a CHECKED fallback: see
    :attr:`Wanted.addresses`, which refuses to compose from a head that dropped a
    credit the listing spelled.

    TWO SHAPES, NOT THREE, and the dash was removed because nothing could ever
    observe it. A ``- version`` suffix is read that way only when
    :func:`split_title` or :func:`split_ambiguous` already read it that way, and
    both of those return the same head, so this branch and the caller's fallback
    produced the identical string for every input either could be given. A guard
    that no input can distinguish from its own fallback is not a guard, and
    leaving it in makes a mutation sweep report a hole where there is none.
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


#: A bracketed group ANYWHERE in a title, not only a trailing one. The trailing
#: walk cannot answer the question :func:`_credits_in` asks, because a listing
#: that spelled its version after a dash carries its credit in the middle: ``Sun
#: Path (feat. Mira) - Live`` has no trailing group at all.
_ANY_GROUP = re.compile(r"[(\[]([^()\[\]]*)[)\]]")


def _credits_in(text: str) -> tuple[str, ...]:
    """Every performer credit a spelling carries, folded, left to right.

    Used to compare a composed head against the listing it came from. Folded
    rather than verbatim, because ``(feat. Mira)`` and ``(Feat Mira)`` name the
    same performer and a comparison that told them apart would refuse to compose
    for a spelling that lost nothing.
    """
    return tuple(
        fold(found.group(1))
        for found in _ANY_GROUP.finditer(str(text))
        if _is_a_credit(found.group(1))
    )


def _equivalent_versions(version: str) -> tuple[str, ...]:
    """Every version TEXT that names the same version as this one.

    One entry for a real qualifier. For a version that folds to nothing, every
    spelling of "no qualifier at all" that :data:`_NULL_VERSIONS` already
    declares equal, in both directions: a list asking for ``Sun Path (Original
    Mix)`` has to reach a tombstone recorded from the row ``Sun Path``, and a
    list asking for ``Sun Path`` has to reach one recorded from ``Sun Path
    (Original Mix)``. Derived from that frozenset rather than spelled a second
    time, so the two cannot disagree about what a null qualifier is.
    """
    if version_token(version):
        return (str(version).strip(),)
    return ("", *sorted(_NULL_VERSIONS))


def _spellings_of(head: str, version: str) -> tuple[str, ...]:
    """Every title string a library row could carry for this head and version.

    THE BRACKETS ARE UNCONDITIONAL and the DASH IS CHECKED, because they are not
    equally ambiguous. A bracketed group at the end of a title is a qualifier by
    convention and is what a library row uses; a dash can be part of the title
    itself, which is the whole reason :func:`split_title` is vocabulary-guarded.
    So the dash form is composed only when this module's OWN reader reads it back
    as the same head and the same version, which means no lookup is ever
    composed under a name this module would itself read as somebody else's
    record.

    THE READ-BACK IS :func:`split_title` AND NOT :func:`split_ambiguous`, and
    accepting the second one was a widening in the direction this file rejects by
    name. ``split_ambiguous`` reads a string back only by declaring that this
    module CANNOT tell whose record it names, so composing ``Sun Path - Live`` on
    the strength of it addresses a row that may well be a composition called "Sun
    Path - Live", and a deletion of that composition would then silently withhold
    the live cut of "Sun Path". :func:`tombstone_fold` settles the direction: a
    missed suppression re-acquires something and reports it, an over-eager one
    withholds music somebody wants, and those costs are not comparable. Nothing
    could see it either way, because the listing that spells the dash form
    already addresses itself through :attr:`Wanted.listed`.

    THE MIRROR OF THAT RULE LIVES IN :attr:`Wanted.addresses`, which walked both
    readings of the same ambiguity and so composed the bracketed spellings from
    the dash-spelled listing this refuses to compose the dash spelling for. One
    ambiguity, two functions, opposite policies, and the docstring here defended
    the direction the other one was breaking. They now agree.

    The two-group forms are here for the spelling that puts one version in
    several brackets, ``Sun Path (Extended) (Remastered)``. A source carrying its
    version in one field cannot know where the groups were, so every cut is
    offered; every one of them folds back to the same version token, so none of
    them crosses a version boundary.
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
        # THE RECORDER'S OWN COMPOSITION ON TOP OF THE DASH FORM, and it is not a
        # doubled address by accident. U24 asks whether a title ALREADY CARRIES
        # its version by looking inside the title's BRACKETED groups and nowhere
        # else, deliberately, so a rekordbox row whose Title column holds
        # ``Sun Path - Nightwave Remix`` and whose version column repeats
        # ``Nightwave Remix`` is composed into
        # ``Sun Path - Nightwave Remix (Nightwave Remix)``. That string was
        # measured against U24's real module, not assumed, and this side reached
        # none of it from any of the three readers: the tombstone was invisible,
        # the version reported missing, acquisition fetched it back, and the
        # deletion was undone at exit zero with every suite green.
        #
        # It does not widen anything. The composition is gated on the SAME
        # conservative read-back as the dash form it is built from, and it names
        # the same recording at the same version, so it cannot cross a version
        # boundary any more than ``dashed`` itself can.
        built.append(f"{dashed} ({version})")
    return tuple(built)


#: Runs of any whitespace, collapsed to one space. A SECOND spacing pattern
#: beside ``_RUNS`` on purpose: that one folds a match token and this one folds a
#: tombstone identity, and the two are allowed to differ. Merging them would make
#: a change to either one silently change the other.
_TOMBSTONE_SPACING = re.compile(r"\s+")


def tombstone_fold(value: object) -> str:
    """U24's ``cratekit.core.tombstone.fold``, replicated exactly.

    NFC, then case, then spacing, in that order. NOT this module's own
    :func:`fold`, and the difference is the whole point of the correction: this
    one composes where the other decomposes, and this one KEEPS punctuation where
    the other folds it to spaces. ``Track (Live)`` and ``Track [Live]`` are two
    tombstones, deliberately, because a missed suppression re-acquires something
    and reports it while an over-eager one silently withholds music somebody
    wants, and those two costs are not comparable.
    """
    return _TOMBSTONE_SPACING.sub(
        " ", unicodedata.normalize("NFC", str(value)).casefold()
    ).strip()


def version_identity(*, artist: str, title: str) -> dict[str, str]:
    """What addresses one deleted version of one recording (R36, AE17).

    THE SAME MAPPING U24's ``core.tombstone.version_identity`` returns, for the
    same inputs, down to the bytes. A tombstone is recorded by the deletion pass
    and consulted here, the suppression identifier is a hash of the store key,
    the kind and this mapping, and a second spelling anywhere in that triple
    records a suppression this side can never find. Nothing raises when that
    happens: the version reports missing, acquisition fetches it back, and the
    deletion somebody made on purpose is undone with the whole suite green.

    Both fields are always present, even when empty, because an identity whose
    KEY SET varies with the input is two identities wearing one name. An identity
    with nothing in either field is REFUSED, because it would hash to one value
    and every unnamed candidate in the library would collide onto one
    suppression, which looks exactly like the feature working.

    The version rides INSIDE the title, which is why the argument list has no
    version in it. See :func:`listed_title`.
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
    """What addresses one REVIEW QUESTION about one recording.

    A DIFFERENT identity from the tombstone's, and telling them apart is the
    correction. A tombstone is a fact about a version that outlives every list;
    a review item is an answer to a question somebody was asked, and the key is
    part of two of the questions this module asks.

    ``key`` is the trap. ``key_disagreement`` can move a track from matched to
    needs review, so "the library holds this exact version at 03A and your list
    says 03B" is not the same question as "your list says 08A", and an identity
    that left the key out would let one answer settle both. It settled them in
    the permissive direction: accept once at 08A and every later key question
    about that recording came back matched, including 03B, the relative minor
    this module exists to catch.

    THE KEY THAT GOES IN IS THE LIST'S, ALWAYS, AND THE LIBRARY DOES NOT GET A
    VOTE, which is the second time this unit had to learn that an identity is a
    function of the thing it identifies. The caller used to pass the key only
    when the question turned out to be ABOUT the key, and which question gets
    asked is decided by what happens to be on that machine's disk. So one list
    line carrying a key opened item ``rv_5b77...`` on a machine holding that
    exact version at another key and ``rv_0efa...`` on a machine holding only
    another version, with one ``match_id`` across both: ``review export`` wrote
    the answer under the first, ``review import`` inserted it with no conflict,
    and the next run on the second machine asked the identical question again
    under the other identifier and ignored the answer. On ONE machine, deleting
    the copy that made it a key question stranded the verdict under an identity
    nothing looks up, which bypasses ``CANDIDATE_GONE`` because reaching that
    state needs the item to be FOUND first.

    THE KEY SET NEVER VARIES AND NEITHER DOES THE VALUE. A list line that names
    no key carries the empty token, which is what an unreadable code folds to as
    well, so a list that carries a key and one that does not are two lines and
    two items. That is the cost of the rule and it is the cheap side: the same
    line through all three readers is still one item, which is the promise R13
    actually makes, and no answer is ever applied to a question nobody was asked.

    ``asks`` IS THE HALF THE FIX ABOVE DELETED ALONG WITH THE DEFECT. Putting the
    LIST'S key on every question made the identity stop moving with the disk, and
    it also made "your list says 03A and I hold this at 03B" and "your list says
    03A and I hold another version entirely" one item, so an acceptance of the
    second silently settled the first: the run then reported ownership of the
    relative minor, in ``paths``, with the file the person had actually pointed
    at gone from them. :func:`question_shape` is what tells the two apart, and
    what it reads is :data:`KEY_QUESTIONS`, whose own docstring has claimed this
    property since before it was true.

    ``version`` IS IN IT FOR THE SAME REASON ONE FIELD OVER, and nothing was
    asserting it. ``Sun Path (Extended Mix)`` and ``Sun Path (Radio Edit)``
    against a library holding neither are two version questions about two
    versions, and an identity without this field makes them one item: answer
    about the extended mix and the radio edit comes back matched, carrying the
    paths of whatever the extended-mix answer named.
    """
    return _identity_asking(artist, title, version, key, question_shape(why))


def _identity_asking(
    artist: str, title: str, version: str, key: str | None, asks: str
) -> dict[str, str]:
    """The identity of one question, given its shape rather than its why.

    The one spelling of the mapping, so :func:`question_identity`, which has a
    why in hand, and :func:`every_question_identity`, which has none, cannot
    come to disagree about a key or a token and file one question under two
    identifiers.
    """
    return {
        # THE RECORDING'S IDENTITY, which is the token for every title that
        # folds to something, so no recorded item of one moves. Two titles of
        # emoji alone were one item, so one answer settled both, and a held
        # row's retirement superseded the other's question every run.
        "recording": recording_identity(artist, title),
        "version": version_token(version),
        "key": key_token(key),
        "asks": asks,
    }


#: Every shape a question can take, in the order they were declared. Read by
#: :func:`every_question_identity`, which has no why to hand because the row it
#: is asked about is not a question any more.
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

    Asked for a row that resolution now OWNS, which is a row with no why to
    derive a question from: ``question_shape`` refuses a matched why on purpose,
    because a matched row must never be filed as a question. But an earlier run
    over the same line may have filed one, under any of the four shapes, before
    the file carrying the row's ISRC arrived or before the rule that owns it now
    existed. The residual ``OWNING_RULES`` cites measured 85 such items on the
    live library. The retiring side cannot know which shape was asked, so it
    asks about all of them, and a shape nobody asked under is an identifier the
    queue simply does not hold.

    ONE PER SHAPE AND NOT ONE PER WHY. The two key whys share one shape by
    design, so enumerating whys would compute one identifier twice and count a
    retirement twice.
    """
    return tuple(
        _identity_asking(artist, title, version, key, asks) for asks in QUESTION_SHAPES
    )


#: How many hex characters of the digest an identifier carries. SIXTEEN, which is
#: 64 bits, and the width is a decision rather than a default.
#:
#: EVERY IDENTIFIER THIS MODULE GENERATES IS THIS WIDE: ``match_id``,
#: ``candidate_id`` and ``option_id``. ``TrackMatch.match_id``'s own docstring
#: says what a collision costs, that two rows carrying one id put the same
#: identifier in two arrays of one payload and "a consumer keying by id dropped
#: one of them with nothing to notice", and a candidate collision is worse: two
#: different owned versions become one thing a person can accept.
#:
#: SIXTY-FOUR BITS RATHER THAN THIRTY-TWO, because the birthday bound is what
#: decides this and not the length of any one list. At 32 bits two of roughly
#: 77,000 identifiers collide with even odds, and a library-scale run generates
#: identifiers per track per candidate across every list somebody ever matches;
#: at 64 bits the same even-odds point is around five billion. Main's own
#: residual "Two identity generators in one codebase, 16 bits and 64, and only
#: one of them was argued" records exactly this class of unargued width for a run
#: identifier, and this is a third generator that nobody had counted.
#:
#: Narrowing it is invisible to every behavioural test in this suite, because a
#: suite drives tens of identifiers and not tens of thousands.
#: ``test_every_identifier_this_module_generates_is_the_declared_width`` is what
#: makes the width a thing somebody has to change on purpose.
DIGEST_WIDTH = 16


def _digest(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:DIGEST_WIDTH]


def digest(*parts: str) -> str:
    """The one identifier digest, for a caller outside this module.

    Public so that a second generator elsewhere is this one and not a copy
    of it: the intake queue keys a recognised track by a digest of the same
    tokens this module's identifiers are built from, and a copy with its own
    width is the "two identity generators in one codebase" shape this module
    already records against itself.
    """
    return _digest(*parts)
