"""U16: three-state matching, and the one internal shape every intake becomes.

R11 in one sentence: an external list resolves each track to matched, needs
review, or missing, and a version difference is never silently treated as
matched. The system this replaces has two comma separated files, owned and
missing, and no representation for the middle state at all, so a remix, an
extended cut, a live take, and a clean edit all landed in "owned" and the user
found out at the gig.

FOUR PROPERTIES, and each one answers a specific way that failed.

1. **Ownership is on-disk truth.** The index is built by walking the library's
   own music tree, reading each file's tags and falling back to its filename.
   Never an export. An export is a snapshot of what rekordbox believed at the
   moment somebody pressed a button, and the source system read a stale one and
   reported an owned track unowned, then went and acquired it again.

2. **A fuzzy or substring hit is a DISCOVERY heuristic and never an identity.**
   Every approximate hit resolves to needs review with the difference named. The
   scoring here can be as generous as it likes precisely because a generous
   score costs one question rather than one wrong join.

3. **A version is part of the identity.** ``recording_token`` folds the artist
   and title; ``version_token`` folds the qualifier separately. Two records that
   agree on the recording and disagree on the version are a QUESTION, and the
   question carries what differs, so a person answers "is your extended mix the
   record this list means" rather than "here are two strings".

4. **One internal shape.** Three readers, one ``Wanted``. A list that arrived as
   a provider playlist, as a public Spotify playlist, or as pasted text produces
   the same match result and, more importantly, the same review item identity,
   so a question answered against one source is not asked again when the same
   list arrives through another. Acquisition is source-agnostic once matched
   (R13), and this module is where "once matched" is made true.

   ONE PLACE THE STRING CANNOT DELIVER THIS ON ITS OWN, and both previous
   attempts picked a side and paid for it. A dash tail that is a bare one-word
   qualifier is either a version or the end of a title, and "Sun Path - Live"
   and "Ziggy Stardust - Reprise" are the same shape. Splitting always mangles
   the second; refusing always reports the first missing and re-acquires a file
   the library holds. So both readings are carried and the library is asked
   which one it holds: see :func:`split_ambiguous`.

   WHAT THE LIBRARY'S ANSWER IS ALLOWED TO DECIDE IS THE QUESTION, NOT THE
   IDENTITY, and reading it as deciding both cost two defects at once. The
   library used to REWRITE the wanted track, so the identifier a row carried was
   a function of what happened to be on that machine's disk: one list produced
   two different ``match_id`` values on two machines, which is exactly the pair
   of verbs ``review export`` and ``review import`` exist to serve, and on one
   machine renaming the confirming file flipped the reading, looked a resolved
   item up under an identity nobody had ever been asked, and left the answer
   somebody gave unreachable in the store with nothing reported.
   :attr:`TrackMatch.match_id` and :meth:`Wanted.question` are now derived from
   the reading the STRING yields and from nothing else, so they are the same on
   every machine.

   THAT SENTENCE WAS TRUE OF THE IDENTIFIER AND FALSE OF THE ITEM for one round,
   and the item is the thing the two verbs actually move. ``question`` took an
   argument saying whether the question was about the key, resolution passed it
   whichever branch the LIBRARY chose, so one list line opened two different
   review items on two machines under one ``match_id``: an answer exported from
   the first imported into the second with no conflict, was filed under an
   identifier the second never looks up, and the same question was asked again
   beside it. A fix that lands on the identifier and leaves the item is a fix on
   the wrong object. The key in the item identity is now the LIST'S key, on every
   question, and the library chooses only what is offered and how the question
   reads.

   AND DELETING THAT ARGUMENT TOOK A SECOND THING WITH IT, which is the same
   defect from the other side and cost a round of its own. With the key on every
   question and nothing saying WHICH question, "your list says 03A and I hold
   this exact version at 03B" and "your list says 03A and I hold another version
   entirely" became one item, so one answer settled both. Driven: the library
   holds only the extended mix, the row is a version question, somebody accepts
   it, the library later gains the plain cut at 03B, and the run reports MATCHED
   with the 03B file in ``paths`` and the extended mix gone from them, at exit
   zero, with no warning and no question. ``Why.KEY_RELATIVE`` exists because 8A
   and 8B look like agreement to anything comparing wheel positions, and it had
   become reachable only while nobody had ever accepted anything about that line.

   SO THE IDENTITY IS A FUNCTION OF THE LIST LINE AND OF WHICH QUESTION IS BEING
   ASKED, AND OF NOTHING ABOUT THE LIBRARY. Every VALUE in it comes off the list
   line; what varies with the disk is only which of the four questions is put,
   and two different questions are two items because an identity covering both is
   an identity that is not unique to the thing it identifies. See
   :func:`question_shape`, which is where :data:`KEY_QUESTIONS` is read, and the
   residual titled "A question answered on one machine does not settle a
   different question about the same line" for what that costs.

   THE ONE CLASS WHERE THE THREE READERS CANNOT CONVERGE ON THE STATE, stated
   rather than papered over in the residual titled "The one-word dash class
   cannot converge on state across the three readers". A source that carries its version in its own field
   has told us where the boundary is; a source that spells "Sun Path - Live"
   has not, and no rule over that string can. Converging the two anyway needs
   either an identity that moves with the library, which is the defect above, or
   one identifier standing for two different records, a composition called "Sun
   Path - Live" and a live cut of "Sun Path". So the ambiguous class resolves to
   NEEDS REVIEW with the held file offered, and property 2 governs: an
   undecidable parse costs one question rather than one wrong join. What still
   converges is everything the string CAN settle, and the practical promise
   nobody is asked twice, because the provider row for the same record matches
   exactly and asks nothing.

**WHERE THE FETCH IS NOT.** Nothing here opens a socket. The readers take rows
that somebody already has: a provider client's track objects, a public playlist
API's items, or lines a person pasted. R13's URL fetching belongs to the intake
verbs, which own provider sessions and pagination; putting it here would make
this module untestable without an account and would give the product two places
that page a playlist.

**THE SUPPRESSED STATE, and why it is not a fourth array.** R36 says an
acquisition source skips a tombstoned version and REPORTS the suppression rather
than omitting it silently. R11 says the match is exactly three states, and the
``match`` payload surface has been closed at three arrays since U5 reserved it.
Those are not in conflict once the two questions are told apart: matched, needs
review, and missing describe the MATCH, and suppression describes what
acquisition may do with the result. A suppressed version is therefore reported
on its own channel by the verb, is in none of the three arrays, and so is
skipped by anything that reads ``missing`` to decide what to go and get. Putting
it in ``missing`` would count it missing, which is what the brief forbids by
name; dropping it would be the silent omission R36 forbids by name.

**ORDER: every question first, then suppression.** A version the library actually
holds is matched even if a tombstone stands over it, because property 1 says the
disk wins and a tombstone over a held file is a stale record rather than a fact
about the library. The verb reports that disagreement instead of hiding it. The
same argument runs one step further and it took a review to see it: a tombstone
must not pre-empt a QUESTION either. R36 governs what acquisition may fetch, not
what a person may be asked, so the store is consulted last, on the one case it is
about, a version nothing in the library resembles and something is therefore
about to go and get.

**WHERE THE IDENTITY LIVES, and the correction that cost the most.** A tombstone
is recorded by a deletion pass and consulted by an acquisition pass, and both of
those are toggleable modules, so an identity spelled inside either one is absent
exactly when the other needs it. It belongs below both, in the domain layer, and
that is where U24 puts it as ``cratekit.core.tombstone``. ``TOMBSTONE_KIND`` and
``version_identity`` here are that module's algorithm replicated byte for byte
until U24 merges, at which point they collapse into imports OF THAT MODULE'S OWN
NAMES, which are ``KIND_VERSION`` and ``version_identity``: the local constant is
called ``TOMBSTONE_KIND`` and nothing upstream is, so a merge instruction that
names this side's spelling sends whoever follows it literally to a symbol that
does not exist. The exact two import lines are written out at ``TOMBSTONE_KIND``
below. The REVIEW ITEM identity is a different thing and stays here: see
``question_identity``.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path
from typing import Any

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

#: The score at or above which an approximate recording hit is worth SHOWING a
#: person. Deliberately generous: everything above it becomes a question and
#: nothing above it becomes a match, so the cost of a low floor is noise in the
#: queue and the cost of a high one is a track reported missing that the library
#: already holds under a slightly different spelling.
#:
#: "NOISE IN THE QUEUE" IS NOT A FREE COST AND THE RESIDUAL TITLED "The ambiguous
#: reading class is queued as a question and does not gate the run" IS THE PRICE
#: OF IT. That entry accepts a class of question that does not stop the run
#: precisely because a queue filling faster than a person empties it stops
#: carrying information, and this constant is the dial that decides how many rows
#: become questions at all. Lowering it is therefore a product change and not a
#: tuning: at 41 a list line and a library file sharing barely half their folded
#: characters open a question, and ``Aurora Bloom - Sun Path`` against a library
#: holding only ``Sun Path Instrumental`` scores 76.4, which is the pinned
#: example either side of this number.
#: ``test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`` is
#: what makes the value a decision somebody has to take on purpose.
APPROXIMATE_FLOOR = 82

#: How many approximate CANDIDATES are offered for one wanted track. A person
#: choosing between five candidates is choosing; a person choosing between forty
#: is scrolling. Spent twice on purpose: once as the recording limit the scorer
#: is given, and again as a truncation of the candidate list, because one
#: recording can be held as several versions at several keys and a limit on
#: recordings alone promises a number it does not deliver.
#:
#: ONLY THE SECOND SPEND WAS MEASURED, which made the first a written
#: justification with nothing behind it: multiplying the scorer's limit by four
#: left the whole suite green. The two spends are observable apart, and the thing
#: that separates them is the WITHHELD COUNT. Eight resembling recordings held as
#: one version each: with the scorer capped here, five candidates are built and
#: nothing is withheld; with the cap raised, eight are built, five are shown and
#: three are reported kept back. So a run that says "3 further candidates were
#: never shown" over a library of one-version recordings is a run whose scorer
#: limit is not this constant, and
#: ``test_the_scorer_is_capped_at_the_same_number_the_offer_is`` asserts the
#: number is spent in both places.
APPROXIMATE_LIMIT = 5


# ---------------------------------------------------------------------------
# Folding: one spelling per value, so one candidate is one decision
# ---------------------------------------------------------------------------

_MARKS = re.compile(r"[^\w\s]", re.UNICODE)
_RUNS = re.compile(r"\s+")

#: Trailing bracketed groups that name a PERFORMER rather than a version. They
#: come off the title because two listings of one record disagree constantly
#: about whether the guest is in the title or in the artist field, and they are
#: not folded into the version because a guest vocalist is not an edit.
_CREDIT_PREFIXES: tuple[str, ...] = ("feat ", "feat. ", "ft ", "ft. ", "featuring ", "with ")

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


def _is_a_credit(inside: str) -> bool:
    """Whether a bracketed group names a PERFORMER rather than an edit.

    ONE PLACE, because two callers ask it and a second copy would let them
    disagree about what a credit is. :func:`split_version` drops these from the
    version, and :func:`_credits_in` checks that a head this module composed from
    still carries every one the listing spelled, which is a check that means
    nothing if the two answer the question differently.
    """
    folded = fold(inside)
    return any(folded.startswith(fold(prefix)) for prefix in _CREDIT_PREFIXES)


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
    qualify, so the group that stands first is never one. A CREDIT STILL
    COMES OFF, so a row titled only ``(feat. Mira)`` reads as naming no title
    and is refused as before: a credit names a performer, never the record.
    Read here, in the one function every reader and the library index start
    from, so the two sides still fold one recording to one token.
    """
    remaining = str(title).strip()
    qualifiers: list[str] = []
    while True:
        found = _TRAILING_GROUP.search(remaining)
        if found is None:
            break
        inside = found.group(1).strip()
        if found.start() == 0 and not _is_a_credit(inside):
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


def version_token(version: str) -> str:
    """The folded identity of a VERSION, with the no-op qualifiers folded away."""
    folded = fold(version)
    return "" if folded in _NULL_VERSIONS else folded


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


_ISRC = re.compile(r"[A-Z]{2}[A-Z0-9]{3}[0-9]{7}")


def fold_isrc(value: object) -> str:
    """An ISRC spelling with its whitespace and hyphens dropped, upper cased.

    THE ONE FOLD, called by the outbound source, the missing verb and the index,
    so a hyphenated spelling on one side and a bare one on the other are one
    string. Not validated: a verb that has to say a value was malformed rather
    than absent reads this and then asks :func:`isrc_token`.
    """
    return re.sub(r"[\s-]", "", str(value or "")).upper()


def isrc_token(value: object) -> str:
    """The folded ISRC as an identity, or ``""`` when the value is not one.

    A value that does not read as an ISRC once folded, a catalogue number or a
    stray label, is NOT an identity and folds to empty rather than to a key
    nothing else could share by accident.
    """
    folded = fold_isrc(value)
    return folded if _ISRC.fullmatch(folded) else ""


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
        "recording": recording_token(artist, title),
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


# ---------------------------------------------------------------------------
# The one internal shape (R13)
# ---------------------------------------------------------------------------

#: The three list origins this unit reads. Values are stable identifiers that
#: travel in a list document, so they are never display names (R19).
TIDAL = "tidal"
SPOTIFY = "spotify"
TEXT = "text"


@dataclass(frozen=True, slots=True)
class Wanted:
    """One track an external list asks for, in the shape everything downstream reads.

    ``ref`` is the source's own identifier and is PROVENANCE, never identity.
    Keying anything on it would make the same record from two services two
    different questions, and a person would answer both.
    """

    artist: str
    title: str
    version: str = ""
    key: str | None = None
    isrc: str | None = None
    origin: str = TEXT
    ref: str = ""
    #: THE TITLE AS THE SOURCE SPELLED IT, VERSION AND ALL. Carried rather than
    #: recomputed because the tombstone identity is a hash of a title, the other
    #: side of that hash reads a library row's Title column verbatim, and a title
    #: this module took apart and put back together is a different string. A
    #: source that split the title from the version has the two put back together
    #: by the reader, from the row's OWN title, so a featured credit the row
    #: spelled survives into every address composed from it. Empty only for a
    #: ``Wanted`` built by hand, where :attr:`listed` composes the fallback.
    spelled: str = ""
    #: THE OTHER WAY THIS LISTING'S TITLE READS, as (title, version), when its
    #: dash tail is a bare one-word qualifier and the string alone cannot say
    #: whether that is a version or the end of a title. ``None`` when the title
    #: has only one reading, which is almost every title. See
    #: :func:`split_ambiguous` and :attr:`readings`.
    other_reading: tuple[str, str] | None = None
    #: WHETHER THE ROW BILLED MORE THAN ONE ARTIST. :attr:`artist` keeps the
    #: first and drops the rest, and a provider that lists a guest beside the
    #: main artist has credited them without a word of it reaching the title.
    #: Read only by :attr:`uncredited_spellings`, which must not take a title
    #: with no bracketed credit as a listing that credited nobody.
    several_artists: bool = False

    @property
    def recording(self) -> str:
        return recording_token(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)

    @property
    def key_key(self) -> str:
        return key_token(self.key)

    @property
    def listed(self) -> str:
        """The title this track is ADDRESSED BY, which is the one it arrived as.

        THE SEAM, and getting it wrong is invisible from either side alone. The
        deletion pass hashes a library row's Title column verbatim. Round one of
        this file hashed a title that had been split and recomposed into round
        parentheses, so the two sides agreed only when the row happened to use
        that one spelling out of the several a row really uses. Four other
        spellings of one version missed, including the dash form this module
        learned to parse, and a miss is silent on both sides: nothing knows a
        tombstone exists, so nothing reports one.

        Composition is the fallback and not the rule, and where it happens moved.
        A reader that is handed a version in its own field composes at the point
        it still has the row's own title, credits included; this fallback is what
        is left for a ``Wanted`` somebody built by hand, and it composes from
        :attr:`title`, which has had its credits taken off. See :func:`_from_row`
        for what that costs when it is the only composition there is.
        """
        return self.spelled or listed_title(self.title, self.version)

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36), which is U24's and not this module's."""
        return version_identity(artist=self.artist, title=self.listed)

    @property
    def readings(self) -> tuple[Wanted, ...]:
        """This listing, and the other way its title reads. Conservative first.

        One entry for a title with one reading. Two when the dash tail is a bare
        one-word qualifier, which no rule over the string can resolve: see
        :func:`split_ambiguous`. The second entry carries the SAME spelled
        string, because the address a deletion recorded is what the row said and
        does not change with how this module reads it.

        ONE CONSUMER, :func:`_other_reading_the_library_holds`, and it uses the
        second entry to decide what to OFFER with a question. Nothing identifying
        is derived from it: not the match identifier, not the review item, and
        since this round not an address either. See :attr:`addresses` for why the
        last of those had to go.
        """
        if self.other_reading is None:
            return (self,)
        title, version = self.other_reading
        return (
            self,
            replace(self, title=title, version=version, other_reading=None),
        )

    @property
    def addresses(self) -> tuple[str, ...]:
        """Every TITLE STRING a library row could carry for this exact version.

        Built from the spelling's own head rather than from the matching title,
        for the reason :func:`_head_of` gives.

        THE READING THE LIST SPELLED, AND NOT THE OTHER ONE, which is the same
        policy :func:`_spellings_of` applies to the same ambiguity and the two
        were pointing in opposite directions. That function refuses to compose
        ``Sun Path - Live`` from a head and a version, argued out loud, because a
        deletion of a composition genuinely called "Sun Path - Live" would then
        silently withhold the live cut. This walked both readings, so a list line
        spelling ``Aurora Bloom - Sun Path - Live`` composed ``Sun Path (Live)``
        and ``Sun Path [Live]`` and a deletion of the live cut silently withheld
        a listing that may well mean the composition. Same cost, opposite
        direction, one ambiguity. :func:`tombstone_fold` settles which way both go:
        a missed suppression re-acquires something and REPORTS it, an over-eager
        one withholds music somebody wants and says nothing, and those two costs
        are not comparable. So an undecidable reading never crosses into an
        address, in either direction, and the residual is a dash-spelled listing
        re-acquiring a version deleted under its bracketed spelling.

        THE CREDIT IS A PRECONDITION OF COMPOSING AT ALL, and until this round it
        was a sentence in a docstring while the code did the opposite for three
        real shapes. ``_head_of`` locates the version as a bracketed SUFFIX, so a
        listing that put its credit after the version, ``Sun Path (Live) (feat.
        Mira)``, or split the version over several groups, ``Sun Path (feat.
        Mira) (Extended) (Remastered)``, fell back to the matching title, which
        has had its credits taken off. Every address then composed was the PLAIN
        record's, so deleting the plain ``Sun Path (Live)`` silently withheld the
        credited recording somebody had asked for, in none of the three arrays,
        at exit zero. That is the over-eager suppression :func:`tombstone_fold`
        rejects by name, and it is the more expensive of the two costs.

        So the fallback is checked rather than trusted: composition happens only
        when the head still carries every credit the listing spelled. When it
        does not, the listing is addressed by exactly what it said and by nothing
        else, which costs a missed suppression that gets reported.
        """
        found: list[str] = []
        spelled = self.listed
        head = _head_of(spelled, self.version) or self.title
        composed: tuple[str, ...] = ()
        if _credits_in(head) == _credits_in(spelled):
            composed = tuple(
                built
                for text in _equivalent_versions(self.version)
                for built in _spellings_of(head, text)
            )
        for spelling in (spelled, *composed):
            if spelling not in found:
                found.append(spelling)
        return tuple(found)

    @property
    def suppression_spellings(self) -> tuple[dict[str, str], ...]:
        """Every identity one version of this recording could have been recorded under.

        CONSULTING IS NOT RECORDING, and the two get different rules. A recorder
        must write one identity, or one deletion becomes several records; a
        consulter that asks under one spelling and misses re-acquires a track
        somebody deleted on purpose, with nothing raised anywhere. So the store
        is asked under the spelling this list used AND under every other spelling
        a library row carries for the same version: the three bracket and dash
        conventions, the multi-group form, and the null qualifiers
        :data:`_NULL_VERSIONS` already declares equal to no qualifier at all.

        A PROVIDER ROW USED TO REACH EXACTLY ONE OF THEM. Its version arrives in
        its own field, so ``spelled`` is empty, and the set collapsed to the
        single parenthesised composition; a tombstone written from ``Sun Path -
        Nightwave Remix`` or ``Sun Path [Nightwave Remix]`` was invisible to it
        and the track was re-acquired at exit zero.

        This does NOT loosen KTD16. Every spelling here names the SAME version of
        the same recording, so no lookup can cross a version boundary and a
        tombstone over one remix can still never suppress another. What it will
        not do is widen INWARDS: nothing composed here drops a featured credit
        the listing spelled, because that would let a deletion of the plain
        record withhold the credited one. That sentence was an assertion for
        three rounds and is a checked precondition now: see :attr:`addresses`.
        """
        seen: list[dict[str, str]] = []
        for title in self.addresses:
            built = version_identity(artist=self.artist, title=title)
            if built not in seen:
                seen.append(built)
        return tuple(seen)

    @property
    def uncredited_spellings(self) -> tuple[dict[str, str], ...]:
        """The identities to ask the COMPANION kind under, which is often none.

        THE SHAPE :attr:`suppression_spellings` CANNOT REACH, CLOSED FROM THE
        OTHER SIDE. The residual titled "A deleted track the tombstone consult
        cannot reach is listed for download" is the record of what it cost while
        it was open. A provider carrying its version in its own field
        spells ``Sun Path`` and ``Nightwave Remix``. The library row somebody
        deleted read ``Sun Path (feat. Mira) (Nightwave Remix)``, the tombstone
        is addressed by that string, and nothing here can compose a guest it was
        never handed. It reported missing, ``intake missing`` listed it, and the
        next download fetched back a file a person had removed. So the deletion
        pass records a companion with the credit groups out, under
        :data:`UNCREDITED_KIND`, and this is what asks for it.

        ONLY A LISTING THAT SPELLED NO CREDIT ASKS AT ALL, and that is the guard
        rather than a saving. A listing crediting Zed that asked here would be
        withheld by a deletion of the recording that credits Mira, which is the
        over eager direction :func:`tombstone_fold` rejects by name. A listing
        that spelled its credit reaches its own tombstone verbatim through
        :attr:`suppression_spellings` and needs nothing from this.

        "SPELLED NO CREDIT" HAS TO BE SOMETHING THIS OBJECT SAW, and there are
        two ways it can fail to have seen one. A ``Wanted`` built by hand carries
        no :attr:`spelled` at all: the verb builds one from a HELD FILE, whose
        title the index has already taken the credits off, so an empty answer
        there means nobody looked and not that nobody was credited. And a
        provider row that bills a guest in its ARTISTS list has credited them
        with nothing in the title to show it, which :attr:`several_artists`
        carries. Neither asks. Each costs a missed suppression that is reported.

        IT WIDENS NOTHING THE ENGINE DID NOT ALREADY CALL ONE VERSION. A credit
        names a performer and comes off the matching title, so this listing
        resolves OWNED against that credited row while the row is held.
        ``test_the_companion_reaches_exactly_what_ownership_reached`` drives
        both halves, so the sentence is a measurement. And a deletion of the
        PLAIN record writes no companion, so it can never withhold the credited
        one from here.

        The same spellings, because the companion kept whatever bracket shape
        the row used and only lost its credits.
        """
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
            return ()
        return self.suppression_spellings

    def question(self, why: Why) -> dict[str, str]:
        """THE REVIEW ITEM identity, which is this module's.

        Separate from :attr:`identity` because they address different things: a
        tombstone outlives every list and a question is one thing somebody was
        asked. See :func:`question_identity` for why the key is in it.

        ONE ARGUMENT, AND IT IS WHICH QUESTION THIS IS, not what the library
        holds. The argument it used to take was ``about_the_key``, a boolean the
        LIBRARY set on a field of the resolved row, and an identity a machine's
        disk gets a vote in is not an identity. Deleting it took the question
        with it and collapsed the key question onto the version question, so the
        replacement is the WHY, which names the question rather than the disk:
        every VALUE here is still read off ``self``, which is the list line and
        nothing else. :func:`question_shape` argues both halves.
        """
        return question_identity(self.artist, self.title, self.version, self.key, why)

    def questions(self) -> tuple[dict[str, str], ...]:
        """Every identity this line can have been asked under, one per shape.

        For the row that is no longer a question: resolution owned it, and the
        items an earlier run filed about it are retired through these. See
        :func:`every_question_identity`.
        """
        return every_question_identity(self.artist, self.title, self.version, self.key)


def _field(row: object, name: str, default: Any = None) -> Any:
    """Read ``name`` from a mapping or from an object attribute.

    Both, because the same reader has to serve a list document that was written
    to disk and a provider client's live track objects. Supporting only the
    first would make the intake verbs convert every object before calling this,
    which is a second normalization step and therefore a second place for the
    shapes to disagree.
    """
    if isinstance(row, Mapping):
        value = row.get(name, default)
    else:
        value = getattr(row, name, default)
    return default if value is None else value


def row_isrc(row: object) -> Any:
    """The ISRC a provider row carries, as the row spelled it, or None.

    From the row itself, else from its ``external_ids``, which is where a
    public playlist row keeps it. PUBLIC, because the label genre gate asks a
    general catalogue by this value and must find it wherever this module's
    own reader would: a second reader that knew one of the two places
    would call a release unaskable while its rows carried the identifier.
    """
    external = _field(row, "external_ids", {})
    return _field(row, "isrc") or (_field(external, "isrc") if external else None)


def _first_named(entries: object) -> str:
    """The first non-empty name in a list of artists, whatever they are made of.

    A BARE STRING IS A LIST OF ONE. Two rows spelling their artists
    ``{"artists": "Aurora Bloom"}`` and ``{"artists": "Nova Reef"}`` both read as
    no artist at all, so both hashed to an identity carrying only the title and
    both landed on the same identifier for two different recordings. It is not
    split on a comma: a comma is legal inside an artist's own name, and guessing
    where one artist ends is the wrong-join risk this module exists to remove.
    """
    if isinstance(entries, str):
        return entries.strip()
    if not isinstance(entries, (list, tuple)):
        return ""
    for entry in entries:
        if isinstance(entry, str) and entry.strip():
            return entry.strip()
        name = _field(entry, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return ""


def _bills_several(row: object) -> bool:
    """Whether a provider row names more than one artist, under either field.

    Counted the way :func:`_first_named` reads, a string or a mapping or an
    object with a name, so the two cannot disagree about what an entry is. A
    bare string is a list of one and is never split, for the reason given there.
    """
    for field_name in ("artist", "artists"):
        entries = _field(row, field_name)
        if not isinstance(entries, (list, tuple)):
            continue
        named = [entry for entry in entries if _first_named([entry])]
        if len(named) > 1:
            return True
    return False


def _artist_of(row: object) -> str:
    """The primary artist, from whichever of the four shapes a provider used.

    THE LIST UNDER ``artist`` IS THE ONE THAT WAS MISSING, and it read as no
    artist at all rather than as a shape this reader does not know. A row
    spelling its artists ``{"artist": ["Two", "Names"]}`` produced an empty
    artist, hashed to an identity matching nothing, and reported a track the
    library plainly held as missing with no warning and exit zero, right beside
    the ``{"artists": [...]}`` spelling of the same track landing matched. A
    list is read here exactly as a list under ``artists`` is read, first entry
    first, because two spellings of one shape must not be two answers.

    THE BARE STRING UNDER ``artists`` WAS MISSING FOR THE SAME REASON and cost
    more, because it silently failed to read an artist that was RIGHT THERE. Two
    rows carrying ``{"name": "Sun Path", "artists": "Aurora Bloom"}`` and
    ``{"name": "Sun Path", "artists": "Nova Reef"}`` both produced an empty
    artist and therefore one identity for two different recordings. See
    :func:`_first_named`.
    """
    single = _field(row, "artist")
    if isinstance(single, str) and single.strip():
        return single.strip()
    if isinstance(single, (list, tuple)):
        return _first_named(single) or _first_named(_field(row, "artists", ()))
    if single is not None:
        name = _field(single, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return _first_named(_field(row, "artists", ()))


def read_tidal_tracks(rows: Iterable[object]) -> tuple[Wanted, ...]:
    """Provider playlist rows, where the version is its OWN field.

    This is the shape that makes the three readers worth having. The provider
    carries "Someone Remix" beside the title; the public playlist API below
    carries it inside the title; pasted text carries it inside the title too.
    All three fold to one version token, so all three ask one question.
    """
    return tuple(
        _from_row(row, origin=TIDAL, position=position)
        for position, row in enumerate(rows, start=1)
    )


def read_spotify_items(items: Iterable[object]) -> tuple[Wanted, ...]:
    """Public playlist items, each of which wraps the track it holds.

    A row that is already a track is accepted too. The wrapper is what the
    playlist endpoint returns and the bare track is what the tracks endpoint
    returns, and refusing one of them would put the choice of endpoint into this
    module's contract.
    """
    found: list[Wanted] = []
    for position, item in enumerate(items, start=1):
        inner = _field(item, "track")
        found.append(
            _from_row(
                inner if inner is not None else item, origin=SPOTIFY, position=position
            )
        )
    return tuple(found)


def read_text_lines(text: str, *, allow_empty: bool = False) -> tuple[Wanted, ...]:
    """Pasted "Artist - Title" lines. Blank lines and ``#`` comments are skipped.

    A line that carries no separator is REFUSED rather than read as a title with
    no artist. A tracklist with one malformed line is far more often a tracklist
    somebody pasted wrong than a record by nobody, and reading it as anonymous
    would put a track in the queue that no source can ever match.

    A file with NO readable line in it at all is refused for the same reason the
    document reader refuses a newer format: reading it anyway reports a clean
    match over nothing, and "every track on your list is owned" and "your list
    was empty" are the same three empty arrays and the same exit zero.
    ``allow_empty`` is for the one caller that has a positive declaration to go
    on, a list document whose ``tracks`` array is present and empty.
    """
    found: list[Wanted] = []
    for number, raw in enumerate(str(text).splitlines(), start=1):
        line = _ORDINAL.sub("", raw).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=raw, number=number))
    if not found and not allow_empty:
        raise UnreadableList(
            "this list holds no track lines at all; a blank list and a list whose "
            "every track is owned produce the same empty result and the same "
            "exit status, so it is refused rather than reported clean"
        )
    return tuple(found)


def read_text_rows(rows: Iterable[object], *, allow_empty: bool = True) -> tuple[Wanted, ...]:
    """A list document's ``tracks`` array, where each entry is ONE line.

    Read entry by entry rather than joined into one blob and re-split. The join
    put three defects in one line of code: a refusal named a line number in a
    string nobody has, a row that happened to carry a newline silently became two
    tracks, and the array's length stopped being the number of tracks read.

    Blank and ``#`` rows are still skipped, and that is deliberate rather than
    an oversight: a document written from a pasted tracklist carries the pasted
    lines verbatim, comments included, and the two spellings of one list have to
    read the same. What is NOT allowed is a row hiding a second track inside it.
    """
    found: list[Wanted] = []
    for position, raw in enumerate(rows, start=1):
        text = str(raw)
        if "\n" in text or "\r" in text:
            raise UnreadableList(
                f"track {position} carries a line break, so one entry in the "
                f"array would become two tracks and the list would be longer "
                f"than it declares",
                line=position,
            )
        line = _ORDINAL.sub("", text).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=text, number=position))
    if not found and not allow_empty:
        raise UnreadableList("this list holds no track lines at all")
    return tuple(found)


def _line(line: str, *, raw: str, number: int) -> Wanted:
    artist, separator, title = line.partition(_DASH)
    if not separator or not artist.strip() or not title.strip():
        raise UnreadableList(
            f"line {number} is not an 'Artist - Title' line: {raw.strip()!r}",
            line=number,
        )
    return _from_row(
        {"artist": artist, "title": title}, origin=TEXT, position=number
    )


#: Origin to the reader that speaks it. A list document names its origin and the
#: reader is looked up here, so adding a fourth source is one entry plus one
#: reader rather than a branch somebody has to find.
READERS: Mapping[str, Callable[[Iterable[object]], tuple[Wanted, ...]]] = {
    TIDAL: read_tidal_tracks,
    SPOTIFY: read_spotify_items,
}


def _from_row(row: object, *, origin: str, position: int) -> Wanted:
    """One row, POSITIVELY recognized or refused.

    BOTH HALVES ARE REQUIRED, and demanding only one of them was the same defect
    wearing a weaker rule. ``read_text_lines`` refuses a line with no artist by
    name, and this path accepted one: an artist-less row keeps its title, and a
    title alone is not unique to the recording it names. Two rows reading "Sun
    Path" by two different artists then carried ONE match identifier, both
    resolved matched against one unrelated file whose own artist tag was absent,
    and one of the two vanished from any payload a consumer keys by id, at exit
    zero, with no warning and no question.

    Three more things went wrong with no guard at all: two rows carrying nothing
    but an identifier folded to one match identifier; an unreadable row matched
    any junk file in the library whose name folded to nothing and was reported
    owned; and a row whose artists arrived in a shape this reader did not know
    reported a held track missing.
    """
    raw_title = _raw_title(row)
    declared = str(_field(row, "version", "")).strip()
    title, embedded = split_title(raw_title)
    isrc = row_isrc(row)
    artist = _artist_of(row)
    if not artist or not title:
        absent = "artist" if title else "title"
        raise UnreadableList(
            f"track {position} names no {absent}, and the half that is left is "
            f"not unique to the recording it means: it matches any file in the "
            f"library agreeing on that half, and two rows differing only in the "
            f"missing one are a single identifier",
            line=position,
        )
    return Wanted(
        artist=artist,
        title=title,
        version=declared or embedded,
        key=(str(_field(row, "key", "")).strip() or None),
        isrc=(str(isrc).strip() or None) if isrc else None,
        origin=origin,
        ref=str(_field(row, "id", "")).strip(),
        # THE ROW'S OWN TITLE, WITH ITS VERSION IN IT. A row that spelled the two
        # together is addressed by exactly what it said. A row that declared its
        # version in a separate field never spelled them together, so the two are
        # composed HERE, FROM THE ROW'S TITLE rather than from the matching one,
        # and that word is the whole of the correction. The matching title has
        # had its featured credits taken off, because a guest vocalist names a
        # performer rather than an edit, so composing the address from it turned
        # a provider row for ``Sun Path (feat. Mira)`` into every address of the
        # PLAIN record: a tombstone over the literal library row ``Sun Path
        # (Extended) (Remastered)`` then suppressed a listing for the credited
        # recording, in none of the three arrays, at exit zero, with acquisition
        # skipping a track nobody had deleted. ``Wanted.addresses`` cannot catch
        # that, because by the time it compares the credits the composition has
        # already dropped it and the comparison is vacuous on both sides.
        spelled=listed_title(raw_title, declared) if declared else raw_title,
        # ONLY WHEN THE ROW SPELLED THE TWO TOGETHER. A declared version leaves
        # nothing ambiguous, because the source already said which part is the
        # version.
        other_reading=None if declared else split_ambiguous(raw_title),
        several_artists=_bills_several(row),
    )


def _raw_title(row: object) -> str:
    """The title one provider row spells, its version and brackets still in it."""
    return str(_field(row, "title", "") or _field(row, "name", "")).strip()


def listed_names(row: object) -> tuple[str, str, str]:
    """The provider id, the artist and the title as one row lists them (U213).

    Read the way :func:`read_row` reads them, for naming a row it REFUSED: a
    caller that plans many playlists sets that one track aside by its id and
    says which it was, rather than refusing every playlist over it. The title
    is the row's own spelling, unsplit, since a refused row has no reading.
    """
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)


def read_row(row: object, *, origin: str, position: int) -> Wanted:
    """ONE provider shaped row as a ``Wanted``, for a reader outside this module.

    The recognition identifier receives a hit in exactly the shape a provider
    row has, a mapping with a title, a list of artists and an ISRC under
    ``external_ids``, and reading it here rather than in a second reader is
    what keeps a recognised track and the same track pasted in a tracklist
    folding to one identity: every rule the readers learned about artists,
    versions, spellings and ambiguous titles applies to both or to neither.
    Raises :class:`UnreadableList` for a row naming no artist or no title.
    """
    return _from_row(row, origin=origin, position=position)


class UnreadableList(ValueError):
    """A pasted tracklist carries a line this reader will not guess at.

    A plain exception rather than a structured cause, because this module sits
    below the layer that owns the failure vocabulary. The verb converts it, in
    the one place that is allowed to know what a remediation looks like.
    """

    def __init__(self, message: str, *, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


# ---------------------------------------------------------------------------
# The library, indexed from what is on the disk
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Owned:
    """One audio file the library holds, and what the disk says it is."""

    path: Path
    artist: str
    title: str
    version: str
    key: str | None
    #: THE FILE'S ISRC, FOLDED, or empty when the tag is absent or malformed.
    #: 1691 of 9868 files on the live volume carry none, and those are held by
    #: the credited list rule or by the recording token alone.
    isrc: str = ""
    #: THE FOLDED NAMES THE ARTIST TAG CREDITS, for the credited list rule.
    #: Computed once when the file is read, not on every lookup, because the
    #: index answers one membership question per row over every file under a
    #: title and the inputs never change between rows.
    members: frozenset[str] = field(init=False, default=frozenset())

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "members", frozenset(fold(name) for name in credited_members(self.artist))
        )

    @property
    def recording(self) -> str:
        return recording_token(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)

    @property
    def key_key(self) -> str:
        return key_token(self.key)


@dataclass(frozen=True, slots=True)
class LibraryIndex:
    """Ownership as MEMBERSHIP, which is the shape the source repo got right.

    Ownership being a lookup in this index, rather than a filter somebody
    applies at each call site, is what stops a caller forgetting it. A caller
    that forgets a filter gets a plausible answer; a caller that forgets a
    lookup gets nothing and notices.
    """

    by_recording: Mapping[str, tuple[Owned, ...]]
    #: Every file under the folded ISRC it carries. A file with no ISRC tag is
    #: in :attr:`by_recording` and not here.
    by_isrc: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)
    #: Every file under its folded title alone, the lookup the credited list
    #: rule reads. Membership is decided at the lookup, not here, so one file
    #: is indexed once however many artists its tag credits and ``__len__``
    #: still counts files.
    by_title: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)

    @property
    def recordings(self) -> tuple[str, ...]:
        return tuple(self.by_recording)

    def versions(self, recording: str) -> tuple[Owned, ...]:
        return self.by_recording.get(recording, ())

    def held_by_isrc(self, isrc: str) -> tuple[Owned, ...]:
        """Every file carrying this folded ISRC. Empty for an empty token, so a
        row with no ISRC, or a malformed one, asks nothing here."""
        return self.by_isrc.get(isrc, ()) if isrc else ()

    def held(self, artist: str, title: str) -> tuple[Owned, ...]:
        """Every file that IS this recording, under two rules in order.

        The recording token first, the exact text rule every caller had. Then
        THE CREDITED LIST RULE: a file whose folded title is this title and
        whose artist tag credits this artist as one whole member. In this
        library the artist tag of a processed file lists every credited
        artist, ``Malive, Tito Azevedo, MRQZ``, where the provider row names
        the primary one, ``Malive``, so the token can never agree and the
        approximate pass either offered the file or scored it under the floor.
        The finding is the residual titled "The match engine never consults the
        ISRC, and a processed file's artist tag lists every credited artist, so
        a quarter of the hearts the library holds read missing or offered",
        cited by title for the reason given under :func:`split_title`.

        Whole names, never substrings: ``Tito`` is not a member of that list.
        The two rules are unioned, token hits first, because a file tagged with
        the one artist and a file tagged with the list are both copies the
        library holds.

        A COMMA IS THE ONLY JOINER, and that is a measured limit rather than an
        oversight. Walked on the live volume on 2026-09-23, 3041 of 9868 artist
        tags carry a comma, and of the tags with no comma 105 carry an
        ampersand, 25 a feat or ft, and 12 an x or an and. The ampersand is a
        band's own name far more often than a join, ``Above & Beyond``, so
        splitting on it would invent members, and the other two are a
        population of 37 a person can answer from the review queue.
        """
        exact = self.versions(recording_token(artist, title))
        member = fold(artist)
        counted = {one.path for one in exact}
        credited = tuple(
            one for one in self.by_title.get(fold(title), ())
            if member in one.members and one.path not in counted
        )
        return exact + credited

    def __len__(self) -> int:
        return sum(len(held) for held in self.by_recording.values())


def _read_from_disk(path: Path, template: naming.NameTemplate) -> Owned:
    """What this file is, from its tags first and its filename second.

    Tags first because a tag is what the file itself says; the filename second
    because the library's own naming convention carries the Camelot head and,
    for anything acquired before it was tagged, the artist and title too.
    Neither alone is enough, and an export is neither.

    THE ARTIST AND THE TITLE FALL BACK AS A PAIR, AND A PRESENT VALUE IS NEVER
    DISCARDED. Three rules in precedence order, because two of them alone each
    lose a file. Field by field, a title tag with no artist tag gave an identity
    assembled from two sources matching neither the tags nor the name. As a
    plain pair, an artist tag with no title tag and a filename carrying no
    separator threw the artist away entirely, so the file was found by no list
    naming its artist and a held track reported missing. So: both tags win when
    both are there; otherwise the NAME wins when the name carries both halves;
    otherwise each field takes whatever it has, which is the only case where the
    two sources mix and the only case where mixing beats losing a value.

    THE KEY'S PRECEDENCE RUNS THE OTHER WAY, on purpose. The Camelot head is
    written into the filename by this product, following the library's own
    convention, so for the key the NAME is the library's own statement and the
    tag is whatever some other tool last wrote. For the artist and the title
    there is no such convention and the tag is the file speaking.

    THE TITLE TAG IS STRIPPED OF ITS HEAD THE WAY THE STEM IS. The live library
    writes ``KEY - BPM - `` into the title tag as well as the filename, the live
    system's convention, and 9767 of 9868 files on the volume carry it there. A
    tag taken verbatim put the head inside every recording token, so no
    processed file could match a provider row exactly and the first live
    favourites job resolved 206 hearts as 0 owned over a library holding at
    least 96 of them. The finding is the residual titled "The index takes the
    title tag with its head on, so no processed file resolves owned and every
    heart is offered or missing", cited by title for the reason given under
    :func:`split_title`. A tag that is nothing but a head strips to empty and
    takes the branch an absent tag takes, which is the filename. The head found
    inside the tag carries the key when the stem has none, below the stem's
    head and above the ``initialkey`` tag, which is the opinion
    ``write/naming_cli.py`` already holds about the same bytes: the first draft
    read nothing off the tag's head, and the review drove a file that indexed
    with no key until a rename padded the same head into its filename, so one
    file gave two answers depending on whether ``naming apply`` had run.
    """
    stem = path.stem
    head = naming.parse_head(stem, template=template) or {}
    body = naming.strip_heads(stem, template=template)
    artist_part, separator, title_part = body.partition(template.segment_sep)
    if not separator:
        artist_part, title_part = "", body

    # ONE CONTAINER OPEN FOR THE FOUR FIELDS. Three opens per file was the shape
    # the residual titled "The index reader opens every container three times,
    # and the walk is the library" recorded, and the ISRC is not a fourth.
    read = tags.read_tags(path, ("artist", "title", "initialkey", "isrc"))
    tagged_artist = str(read["artist"] or "").strip()
    spelled_tag = read["title"] or ""
    tagged_title = naming.strip_heads(spelled_tag, template=template)
    named_artist, named_title = artist_part.strip(), str(title_part).strip()
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title
    title, version = split_title(spelled)

    tag_head = naming.parse_head(spelled_tag, template=template) or {}
    written_key = head.get("key") or tag_head.get("key")
    key = written_key or read["initialkey"]
    return Owned(
        path=path,
        artist=artist,
        title=title,
        version=version,
        key=str(key).strip() if key else None,
        isrc=isrc_token(read["isrc"]),
    )


def index_library(
    root: Path,
    *,
    template: naming.NameTemplate | None = None,
    reader: Callable[[Path, naming.NameTemplate], Owned] = _read_from_disk,
) -> LibraryIndex:
    """Walk the library's music tree and index what it holds.

    ``reader`` is injected so a test can drive the grouping without synthesizing
    a valid container for every fixture. Its default is the real disk reader, so
    the production path is the one that runs unless somebody deliberately
    replaces it; a default that read nothing would make an empty library and a
    forgotten argument look identical.
    """
    return index_paths(
        sorted(root.rglob("*")) if root.is_dir() else (), template=template, reader=reader
    )


def index_paths(
    paths: Iterable[Path],
    *,
    template: naming.NameTemplate | None = None,
    reader: Callable[[Path, naming.NameTemplate], Owned] = _read_from_disk,
) -> LibraryIndex:
    """Index exactly the files named, the way :func:`index_library` indexes a tree.

    For a caller that knows which files it means and must not be answered from
    anything else beside them: a landing ties its planned files to the rows that
    asked for them before they move (U113), and download staging also holds the
    partial downloads of attempts that never finished. A name that is not an
    audio file, or not a file, is passed over exactly as the walk passes it.
    """
    shape = template or naming.NameTemplate()
    suffixes = {suffix.lower() for suffix in naming.AUDIO_EXTS}
    grouped: dict[str, list[Owned]] = {}
    by_isrc: dict[str, list[Owned]] = {}
    by_title: dict[str, list[Owned]] = {}
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        held = reader(path, shape)
        grouped.setdefault(held.recording, []).append(held)
        by_title.setdefault(fold(held.title), []).append(held)
        if held.isrc:
            by_isrc.setdefault(held.isrc, []).append(held)
    return LibraryIndex(
        by_recording={key: tuple(rows) for key, rows in grouped.items()},
        by_isrc={key: tuple(rows) for key, rows in by_isrc.items()},
        by_title={key: tuple(rows) for key, rows in by_title.items()},
    )


# ---------------------------------------------------------------------------
# Keys: the relative major and minor trap
# ---------------------------------------------------------------------------


def key_disagreement(wanted: str | None, owned: str | None) -> Why | None:
    """How two Camelot codes disagree, or None when there is nothing to say.

    ABSENCE IS NOT DISAGREEMENT. A listing with no key and a library file with
    one agree about everything they both have an opinion on, and reporting that
    as a conflict would put most of a real playlist in the queue.

    The relative case gets its own answer because it is the one that looks like
    agreement: 8A and 8B share a wheel position and share every note, so a check
    comparing wheel numbers calls them the same key, and the two are a minor and
    a major recording of the same material. Picking one silently is what the
    plan's own scenario forbids.
    """
    if not wanted or not owned:
        return None
    left = naming.parse_camelot(wanted)
    right = naming.parse_camelot(owned)
    if left is None or right is None:
        return None
    if left == right:
        return None
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS


# ---------------------------------------------------------------------------
# One resolved track
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Candidate:
    """One owned VERSION offered as the answer to a version question.

    ADDRESSED BY THE VERSION AND THE KEY, NOT BY THE FILE. Two files that are the
    same version at the same key, a lossless copy and a marked lossy one, are one
    answer to "is the record you want the one I hold as this version", so they
    are one candidate carrying two paths. Addressing by path instead would ask
    the same question twice and would orphan the decision the first time somebody
    renames a file.

    THE KEY IS IN THE GROUPING because it is shown. Grouping by version alone
    built a candidate that displayed one file's key while carrying every file's
    path, so a person shown 08A accepted a set that included 03A, and the
    difference this unit exists to surface was surfaced on a value that was true
    of one of the answers.

    The artist and title travel with it because an approximate hit offers
    candidates from a DIFFERENT recording, and a person shown only a version
    qualifier cannot tell which record they are being asked about.
    """

    candidate_id: str
    artist: str
    title: str
    version: str
    key: str | None
    difference: Why
    paths: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.candidate_id,
            "artist": self.artist,
            "title": self.title,
            "version": self.version,
            "key": self.key,
            "difference": str(self.difference),
            "paths": list(self.paths),
        }


#: How a source is asked for a version this library does not hold. Identifiers,
#: because the next verb switches on them.
BY_ISRC = "isrc"
BY_SEARCH = "search"


@dataclass(frozen=True, slots=True)
class Acquisition:
    """One way to go and get a missing version. DATA on the row, not a question.

    R11's brief says a missing track "becomes a review item with acquisition
    options" and U11 declared missing as an OUTPUT rather than a question, and
    that disagreement is a product decision recorded as the residual titled "Two
    briefs disagree about whether a missing track is a review item" and reserved
    for a person. What is settled either way is that the options have to EXIST: the
    verb's own docstring claimed a missing row carried them and the row carried
    an empty candidate list, an empty path list and nothing else.

    Two shapes rather than one, because a provider that has the code does not
    have to guess and a provider that does not has to be handed text. Neither
    one loosens the version: both name the exact version the list asked for,
    since an option meaning "some other cut will do" is the silent substitution
    this whole unit exists to remove.
    """

    option_id: str
    how: str
    query: str
    artist: str
    title: str
    version: str
    isrc: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.option_id,
            "how": self.how,
            "query": self.query,
            "artist": self.artist,
            "title": self.title,
            "version": self.version,
            "isrc": self.isrc,
        }


def acquisition_options(wanted: Wanted) -> tuple[Acquisition, ...]:
    """What a source can be asked for, most precise first."""
    built: list[Acquisition] = []
    if wanted.isrc:
        built.append(
            Acquisition(
                option_id=f"aq_{_digest(BY_ISRC, wanted.isrc)}",
                how=BY_ISRC,
                query=wanted.isrc,
                artist=wanted.artist,
                title=wanted.title,
                version=wanted.version,
                isrc=wanted.isrc,
            )
        )
    built.append(
        Acquisition(
            option_id=f"aq_{_digest(BY_SEARCH, wanted.recording, wanted.version_key)}",
            how=BY_SEARCH,
            query=f"{wanted.artist} {wanted.listed}".strip(),
            artist=wanted.artist,
            title=wanted.title,
            version=wanted.version,
        )
    )
    return tuple(built)


#: The whys that mean a STORED VERDICT COULD NOT BE APPLIED. The item is resolved
#: in the queue, so a listing of open items does not show it and resolving it
#: again is refused; the only way forward is to clear it. Named here so the verb
#: can name the remedy that actually works rather than the one that reads well.
#:
#: BOTH MEMBERS EARN THEIR PLACE and only one of them was pinned. Dropping
#: ``VERDICT_UNSPECIFIC`` left the whole suite green while the row it names got
#: no ``verdict-unapplicable`` warning, no ``review clear`` remedy, and a place
#: in ``_pending``'s answerable half, which files a RESOLVED item, invisible to
#: ``review list`` and refused by ``review resolve``, under the sentence "list
#: the queue and record a verdict on each item". That dead end is the one
#: ``_pending``'s own docstring says it exists to prevent.
#: ``test_an_unspecific_acceptance_stalls_the_run_the_same_way_a_gone_candidate_does``
#: drives it through the real store.
#:
#: :data:`KEY_QUESTIONS` used to sit here beside it and now sits with :data:`Why`,
#: because the identity reads it and the identity is defined further up the file.
STALLED: frozenset[Why] = frozenset({Why.CANDIDATE_GONE, Why.VERDICT_UNSPECIFIC})


@dataclass(frozen=True, slots=True)
class TrackMatch:
    """One wanted track, the state it resolved to, and why.

    ``match_id`` is derived from the recording, the version and the key and from
    nothing else, which is what makes the same list from three sources produce
    the same rows. The provider's own reference travels under ``wanted`` as
    provenance.

    THE KEY IS IN THE IDENTIFIER because it is in the state. Without it a list
    carrying one row with a key and one without emitted the SAME id in two
    different arrays of one payload, and a consumer keying by id dropped one of
    them with nothing to notice.
    """

    wanted: Wanted
    state: MatchState
    why: Why
    candidates: tuple[Candidate, ...] = ()
    paths: tuple[str, ...] = ()
    item_id: str | None = None
    suppression_id: str | None = None
    acquisitions: tuple[Acquisition, ...] = ()
    #: Candidates the offer limit kept back. Reported rather than dropped, so a
    #: rejection is a rejection of what was shown and everybody knows it.
    withheld: int = 0

    @property
    def match_id(self) -> str:
        return (
            f"mt_{_digest(self.wanted.recording, self.wanted.version_key, self.wanted.key_key)}"
        )

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36). See :func:`version_identity`."""
        return self.wanted.identity

    @property
    def question_identity(self) -> dict[str, str]:
        """THE REVIEW ITEM identity: the list line, and WHICH QUESTION was asked.

        Every VALUE in it is read off ``wanted``, which is the list line. Nothing
        about this machine's library reaches it, which is what makes one line
        open one item on two machines that hold different copies of it, and it is
        the property ``review export`` and ``review import`` are useless without.
        This used to be gated on an ``asks_about_key`` field that resolution set
        from whichever branch the library took, so the identity a verdict was
        written under was a function of that machine's disk and an answer landed
        under an identifier the receiving machine never looks up.

        ``why`` IS NOT THAT FIELD BACK, and the difference is the whole of
        :func:`question_shape`. It names which question this row IS, and two
        different questions must be two items or one answer settles both, which
        is what happened for a round: a version acceptance came back matched
        against the relative minor at a key nobody was asked about.

        FOUR SHAPES AND NOT FIVE, so this separates a key question from a version
        question and never separates the two KEY whys from each other. That is on
        purpose and :func:`question_shape` argues it. The protection against an
        answer crossing between them lives on the ANSWER, in
        :func:`apply_verdict`, and not here.

        REFUSES on a row that is not a question. A matched or missing row has no
        review item, and the identifier it would compute is one somebody could
        answer.
        """
        return self.wanted.question(self.why)

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.match_id,
            "state": str(self.state),
            "why": str(self.why),
            "artist": self.wanted.artist,
            "title": self.wanted.title,
            "version": self.wanted.version,
            "key": self.wanted.key,
            "isrc": self.wanted.isrc,
            "candidates": [candidate.to_json() for candidate in self.candidates],
            "candidates_withheld": self.withheld,
            "acquisition": [option.to_json() for option in self.acquisitions],
            "paths": list(self.paths),
            "review_item": self.item_id,
            "suppression": self.suppression_id,
            # PROVENANCE, and the only key that may differ between the same list
            # read from two services. Everything above it is derived from the
            # recording, which is what "identical match results" means.
            "source": {"origin": self.wanted.origin, "ref": self.wanted.ref},
        }


@dataclass(frozen=True, slots=True)
class MatchResult:
    """Every track in one list, resolved.

    The payload is DERIVED from ``PAYLOAD_STATES`` rather than assembled by
    hand, so the three arrays cannot fall out of step with the states, and a
    fourth state cannot arrive in the envelope without a decision.
    """

    matches: tuple[TrackMatch, ...]

    def __len__(self) -> int:
        return len(self.matches)

    def of(self, state: MatchState) -> tuple[TrackMatch, ...]:
        return tuple(found for found in self.matches if found.state is state)

    @property
    def suppressed(self) -> tuple[TrackMatch, ...]:
        return self.of(MatchState.SUPPRESSED)

    def payload(self) -> dict[str, list[dict[str, Any]]]:
        return {
            str(state): [found.to_json() for found in self.of(state)]
            for state in PAYLOAD_STATES
        }


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def _candidates_for(wanted: Wanted, owned: Sequence[Owned]) -> tuple[Candidate, ...]:
    """Group owned files into one candidate per version, naming what differs.

    GROUPED BY RECORDING, VERSION AND KEY, not by version alone. An approximate
    pass offers files from several different recordings, and two of them with no
    version qualifier would collapse onto one candidate carrying both sets of
    paths, so a person accepting one of them would be accepting the other too.
    The key joins the grouping for the same reason one level down: a candidate
    shows ONE key, so every path under it has to be at that key or the value on
    screen is true of some of what the person is accepting.
    """
    grouped: dict[tuple[str, str, str], list[Owned]] = {}
    for held in owned:
        grouped.setdefault((held.recording, held.version_key, held.key_key), []).append(held)
    built: list[Candidate] = []
    token = isrc_token(wanted.isrc)
    # INSERTION ORDER, NOT SORTED. Sorting looked harmless and threw away the one
    # ordering that carries information: the approximate pass hands its rows over
    # best score first, and re-sorting them alphabetically then truncating to the
    # offer limit dropped the BEST match and kept five worse ones. A library
    # holding "Sun Path Alt" at 91.3 as five versions and "Sun Pathx" at 97.7 as
    # one showed the person five wrong answers and withheld the right one. Every
    # other caller passes rows straight out of the index, whose order is a sorted
    # directory walk, so this is deterministic there too.
    for recording, version_key, key in grouped:
        rows = grouped[(recording, version_key, key)]
        first = rows[0]
        if not _same_recording(wanted, first, token):
            difference = Why.TITLE_APPROXIMATE
        elif version_key != wanted.version_key and not _carries(first, token):
            # AN ISRC SETTLES THE VERSION TOO. A file carrying the row's ISRC
            # under another version spelling is that version however it is
            # spelled, so the only question left about it is the key, and a
            # candidate that said "version" beside a match that said "key"
            # would ask a person a question the engine had already settled.
            difference = Why.VERSION_DIFFERS
        else:
            difference = key_disagreement(wanted.key, key) or Why.EXACT
        built.append(
            Candidate(
                candidate_id=f"cd_{_digest(recording, version_key, key)}",
                artist=first.artist,
                title=first.title,
                version=first.version,
                # The FOLDED key, not the first file's spelling of it, because
                # this one value stands for every path in the group.
                key=key or None,
                difference=difference,
                paths=tuple(str(row.path) for row in rows),
            )
        )
    return tuple(built)


def _carries(held: Owned, token: str) -> bool:
    """Whether ``held`` carries this ISRC. Empty carries nothing."""
    return bool(token) and held.isrc == token


def _same_recording(wanted: Wanted, held: Owned, token: str) -> bool:
    """Whether ``held`` is the recording ``wanted`` names, under any rule
    :func:`resolve_one` applies, so a credited hit or an ISRC hit at another
    version is reported as the version question it is and not as a scored
    resemblance. ``token`` is the row's folded ISRC, computed once by the
    caller. An ISRC agrees only WITH the folded title, see :func:`resolve_one`.
    """
    if held.recording == wanted.recording:
        return True
    if fold(held.title) != fold(wanted.title):
        return False
    return fold(wanted.artist) in held.members or _carries(held, token)


def _approximate(wanted: Wanted, index: LibraryIndex) -> tuple[Owned, ...]:
    """Recordings that merely RESEMBLE the wanted one. Discovery, never identity.

    Scored on the folded recording token, so the artist and the title are both
    in the comparison: a title alone matches every cover version and every
    unrelated record that happens to share a common word.

    The scorer is imported here rather than at module scope because the parser
    imports every landed verb's module on every invocation, ``crate --help``
    included, and this is the only function in the unit that needs it. A cheap
    help screen is a property U5 states about the dispatcher, and paying for a
    scoring library to print one would take it away.
    """
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    found = process.extract(
        wanted.recording,
        index.recordings,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=APPROXIMATE_FLOOR,
        limit=APPROXIMATE_LIMIT,
    )
    # BEST SCORE FIRST, and the order is load-bearing from here on. ``extract``
    # returns descending, and everything downstream preserves it so that the
    # offer limit drops the worst answers rather than whichever sorted last.
    return tuple(held for token, _score, _position in found for held in index.versions(token))


def standing_tombstone(
    wanted: Wanted,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
    companions: bool = True,
) -> str | None:
    """The identifier of the tombstone standing over this version, or None.

    Asked under every spelling one version could have been recorded under, for
    the reason :attr:`Wanted.suppression_spellings` gives: a consult that misses
    re-acquires something somebody deleted on purpose and nothing anywhere
    reports it, while an extra lookup costs one set membership test.

    PUBLIC because the verb reports a tombstone that did NOT suppress, and a
    report that asks under one spelling while the suppression asks under several
    says nothing about the cases the extra spellings exist for.
    """
    for identity in wanted.suppression_spellings:
        if suppresses(TOMBSTONE_KIND, identity):
            return suppression_id(TOMBSTONE_KIND, identity)
    # THE COMPANION IS ASKED SECOND, so a listing both records could answer is
    # reported under the tombstone a person actually wrote, whose revocation
    # lifts both. A listing only the companion answers is handed the companion's
    # identifier, and lifting that lifts the companion alone: the shape that was
    # suppressed becomes acquirable and the credited spelling stays deleted.
    #
    # ``companions=False`` IS FOR A CALLER ABOUT TO CALL THE RECORD STALE. A
    # companion has had its guest taken out, so it cannot say which credited row
    # it stands for, and a held file is evidence against it only if it is that
    # row. The verb's report over a MATCHED row cannot know that, so it does not
    # ask, and stays silent rather than telling a person to lift a deletion the
    # disk says nothing about.
    if not companions:
        return None
    for identity in wanted.uncredited_spellings:
        if suppresses(UNCREDITED_KIND, identity):
            return suppression_id(UNCREDITED_KIND, identity)
    return None


def _held_exactly(wanted: Wanted, index: LibraryIndex) -> bool:
    """Whether the library holds this recording AT THIS VERSION.

    The one piece of evidence that settles an ambiguous reading. See
    :func:`split_ambiguous`.
    """
    return any(
        held.version_key == wanted.version_key
        for held in index.held(wanted.artist, wanted.title)
    )


def _other_reading_the_library_holds(
    wanted: Wanted, index: LibraryIndex
) -> Wanted | None:
    """The reading :func:`split_title` declined that the library holds EXACTLY.

    THE BAR IS DELIBERATELY THE HIGHEST ONE THERE IS: the library holds the head
    at exactly that version. Anything weaker is not evidence about this question
    at all. The library holding "Ziggy Stardust" says nothing about whether
    "Reprise" is a version or the end of a title, so a rule that accepted a
    near-hit would reframe "the library holds nothing like this" into "the
    library holds this record as a different version", and a person accepting
    that reports ownership of a track the library does not hold.

    WHAT THE ANSWER SETTLES IS THE QUESTION, NOT THE PARSE, and the difference is
    the whole correction. This used to RETURN a rewritten ``Wanted`` that the
    rest of resolution then treated as the truth, which promoted an undecidable
    parse straight to MATCHED on the strength of a coincidence: "Long - Live" is
    in this module's own list of legitimate titles ending in a vocabulary word,
    and a library holding "Long (Live)" made the run report ownership of a record
    nobody had checked. It also made the identifier a function of the disk, so
    one list produced two ``match_id`` values on two machines and renaming one
    file stranded an answer somebody had already given.

    So the caller keeps the reading the LIST spelled, and what this returns is
    used for one thing: the candidate offered with the question. See
    :func:`resolve_one`.
    """
    for reading in wanted.readings[1:]:
        if _held_exactly(reading, index):
            return reading
    return None


def resolve_one(
    wanted: Wanted,
    index: LibraryIndex,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> TrackMatch:
    """Resolve one wanted track against the library and the tombstones.

    ``suppresses`` HAS NO DEFAULT, deliberately. A default of "nothing is
    suppressed" is the permissive answer, and a caller that forgot to pass the
    tombstone store would re-acquire exactly what somebody deleted on purpose
    while every test stayed green. The same argument the soft-delete marker
    already lost once in this repository.

    THE ORDER: every question about what the library holds is asked FIRST, and
    the tombstones are consulted last, immediately before a track is called
    missing. R36 governs what acquisition may fetch, not whether a match question
    may be asked. Consulting the store earlier pre-empted a real question with a
    warning: the library held the original mix, a tombstone stood over the
    extended mix, the list asked for the extended mix, and all three arrays came
    back empty. The person was never asked whether the cut they own is the
    record, and the track was invisible to any consumer reading matched or
    missing.

    THE READING THE LIST SPELLED IS THE ONE THAT TRAVELS. Everything identifying
    on the way out, the match identifier, the review item identity and the
    acquisition option, is derived from ``wanted`` exactly as the reader built
    it, so it is a function of the LIST and not of this machine's disk. A title
    the string cannot read one way is not re-read into something else: the other
    reading is offered as a QUESTION, below, once nothing the list actually said
    has matched. See :func:`_other_reading_the_library_holds`.
    """
    # THE ISRC FIRST, because it is the one identity both sides carry and it
    # is exact and cheap. A hit settles the recording and the version, whatever
    # the artist tag says, and it says nothing about the key, which is the
    # library's own statement and is still checked below. The text rules come
    # second, for the rows with no ISRC and the 1691 files with no tag.
    #
    # AN ISRC AGREES ONLY WITH THE FOLDED TITLE. A file carrying the row's ISRC
    # under a different title is not called owned on the strength of one tag:
    # a bootleg ingested with the original's tags, or a tagger that wrote one
    # ISRC across a release, would otherwise mark the heart owned, point its
    # paths at the wrong recording, and the row would never be acquired and
    # nothing would say so. Such a file is offered as a question instead, below,
    # under the discovery reason, with its paths, and the review drove the
    # shape rather than the live volume, whose 49 held rows agreed on the title.
    #
    # WHEN THE ISRC SETTLES A ROW, THE PATHS ARE THE FILES CARRYING IT and the
    # key is checked over those. A copy matched on text alone at the same
    # version is not appended: the reason says the identity was carried, and it
    # has to be true of every path it stands beside.
    title = fold(wanted.title)
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
    settled = [held for held in carrying if fold(held.title) == title]
    doubtful = [held for held in carrying if fold(held.title) != title]
    owned = index.held(wanted.artist, wanted.title)
    if settled:
        exact, agreed = settled, Why.ISRC_EXACT
    else:
        exact = [held for held in owned if held.version_key == wanted.version_key]
        agreed = (
            Why.EXACT
            if any(held.recording == wanted.recording for held in exact)
            else Why.CREDITED_EXACT
        )

    if exact:
        # EVERY held copy, not the first one the directory walk returned. Reading
        # only ``exact[0]`` made the state depend on the sort order of the music
        # tree: an untagged copy filed under "A archive" answered "no
        # disagreement" for a keyed copy filed under "B sorted", and renaming the
        # folder to "C archive" changed the same content from matched to
        # needs-review. The permissive branch won whenever an unkeyed copy sorted
        # first, so KEY_RELATIVE, the slug that exists because 8A and 8B look
        # like agreement, was reachable only by luck.
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None}:
            return TrackMatch(
                wanted=wanted,
                state=MatchState.MATCHED,
                why=agreed,
                paths=tuple(str(held.path) for held in exact),
            )
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            # The relative case wins the reporting when both are present, because
            # it is the one that looks like agreement to everything downstream.
            why=Why.KEY_RELATIVE if Why.KEY_RELATIVE in disagreements else Why.KEY_DIFFERS,
            candidates=_candidates_for(wanted, exact),
        )

    if owned:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,
            candidates=_candidates_for(wanted, owned),
        )

    if doubtful:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,
            candidates=_candidates_for(wanted, doubtful),
        )

    # THE OTHER READING, ASKED ABOUT RATHER THAN ASSUMED, and placed here for two
    # reasons. It comes AFTER the two branches above so that a tie goes to the
    # string the list actually spelled: a library holding a record called "Sun
    # Path - Live" answers the row before anything is guessed about it. It comes
    # BEFORE the approximate pass so the question is a precise one, naming the
    # file and the reading, rather than a fuzzy hit whose score decides whether
    # the class is a question at all; "Instrumental" scores 76.4 against a floor
    # of 82 and "Live" scores 89.4, and the difference between them is not a
    # difference in what the person needs to be asked.
    confirming = _other_reading_the_library_holds(wanted, index)
    if confirming is not None:
        # ONLY THE FILES HELD AT THAT VERSION, not every version of the head. The
        # evidence is that the library holds the head at exactly the version the
        # other reading names, and offering the head's OTHER versions alongside
        # would ask a person to accept a cut this list never mentioned, on the
        # strength of a parse they are being asked about in the same breath.
        held = [
            row
            for row in index.held(confirming.artist, confirming.title)
            if row.version_key == confirming.version_key
        ]
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,
            # SCORED AGAINST WHAT THE LIST SAID, which is what makes the offer
            # honest: relative to the title this row spelled, the held file is a
            # different recording, and that is precisely the thing being asked.
            candidates=_candidates_for(wanted, held),
        )

    near = _approximate(wanted, index)
    if near:
        offered = _candidates_for(wanted, near)
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,
            candidates=offered[:APPROXIMATE_LIMIT],
            # SAID OUT LOUD. A truncated offer that says nothing looks exactly
            # like an offer of everything the library resembles, so a person who
            # rejects it has rejected answers they were never shown.
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),
        )

    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )
    if standing is not None:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.SUPPRESSED,
            why=Why.TOMBSTONED,
            suppression_id=standing,
        )

    return TrackMatch(
        wanted=wanted,
        state=MatchState.MISSING,
        why=Why.NOT_IN_LIBRARY,
        acquisitions=acquisition_options(wanted),
    )


def resolve_all(
    wanted: Sequence[Wanted],
    index: LibraryIndex,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> MatchResult:
    """Resolve a whole list, preserving its order inside each state."""
    return MatchResult(
        matches=tuple(
            resolve_one(
                one, index, suppresses=suppresses, suppression_id=suppression_id
            )
            for one in wanted
        )
    )


def apply_verdict(
    found: TrackMatch,
    *,
    accepted: bool | None,
    option: str | None,
    offered: Sequence[str],
    item_id: str,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> TrackMatch:
    """Fold a recorded decision into a track that would otherwise need review.

    THREE ANSWERS, NOT TWO. ``accepted`` is None for an item nobody has decided
    AND for an item carrying a verdict this build cannot read, and both of those
    leave the track where it is: still a question, still answerable. A verdict
    the reader does not recognize must never freeze an item out of every route,
    because the route out of a wrong decision is to clear it and a frozen item
    cannot be reached to clear.

    A decision naming a candidate the library no longer offers is NOT applied.
    Ownership is on-disk truth, so reporting a track matched on the strength of
    a verdict about a file that is gone would be reporting ownership of nothing.
    The track comes back as a question naming the item, because clearing
    somebody's verdict is their act and not this tool's.

    AN ACCEPTANCE THAT NAMES NO CANDIDATE is applied only when there is exactly
    one to name AND it is the one that was on offer when the answer was given.
    The queue allows a verdict with no option, so with several candidates on
    offer "accepted" says the library has the record and does not say which
    version, and taking all of them would report the library holding three copies
    of one record on the strength of one unspecific yes.

    ``offered`` IS WHAT THE ANSWER WAS ABOUT, and passing it is what closes the
    last hole in this unit's identity story. An unspecific yes is a claim about
    THE CANDIDATE THAT WAS ON THE SCREEN, not a claim about the question in the
    abstract, and the two come apart whenever the library changes under a settled
    item. Measured end to end and not hypothetical: a list line asking for ``Sun
    Path`` at 03A against a library holding it at 08A is a ``KEY_DIFFERS``
    question; somebody accepts it without naming the copy; the 08A file is
    replaced by an 03B copy, the RELATIVE MINOR that ``Why.KEY_RELATIVE`` exists
    to catch; and because both key whys are one ``asks`` value by design, the run
    finds the same item, reads the same yes, and reported MATCHED with the 03B
    path in ``paths``, exit zero, no question and no warning. It works the same
    way in reverse. Splitting the two whys would not fix it, because WHICH of
    them fires is a function of what the disk happens to hold, so the identity
    would move with the library again, which is the defect the round before this
    one removed. The identity is right; what was missing is that the answer was
    never bound to the thing it was an answer about.

    So an unspecific yes recorded against one candidate and read back against a
    different one is NOT APPLIED, and it stalls exactly the way a verdict naming
    a gone candidate stalls, with the same why, the same warning and the same
    ``review clear`` remedy. Naming the candidate with ``--option`` was always
    safe, because ``candidate_id`` digests the owned key; this gives the answer
    that names nothing the same protection by binding it to what it saw.

    An item whose stored options are EMPTY, or that offered several while the
    answer named none, has no single candidate to bind to, so the answer is
    unspecific and stays unspecific. That is the conservative direction: the
    remedy is to clear the item and answer the question that is actually being
    asked now.

    A REJECTION CONSULTS THE TOMBSTONES, which is why this takes the store at
    all. Resolution asks the store only on the path that ends in "missing", and
    a rejection reaches "missing" by another road: the question was asked because
    the library held something, the person said none of it is the record, and the
    row that comes out says go and get the version the list asked for. The step
    text says exactly that. Without the second consult a rejected question
    produced a missing row carrying acquisition options for a version standing
    under a tombstone, at exit zero, and a warning is not a declared input to the
    verb that reads them.
    """
    if accepted is None:
        return TrackMatch(
            wanted=found.wanted,
            state=found.state,
            why=found.why,
            candidates=found.candidates,
            paths=found.paths,
            item_id=item_id,
            withheld=found.withheld,
        )
    if not accepted:
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )
        if standing is not None:
            return TrackMatch(
                wanted=found.wanted,
                state=MatchState.SUPPRESSED,
                why=Why.TOMBSTONED,
                candidates=found.candidates,
                item_id=item_id,
                suppression_id=standing,
                withheld=found.withheld,
            )
        return TrackMatch(
            wanted=found.wanted,
            state=MatchState.MISSING,
            why=Why.VERDICT_REJECTED,
            candidates=found.candidates,
            item_id=item_id,
            # A REJECTION IS A MISSING ROW and carries what a missing row
            # carries. "None of the versions I hold is this record" is the
            # sentence that hands the track to acquisition, so the row that says
            # it has to say what to go and get.
            acquisitions=acquisition_options(found.wanted),
            withheld=found.withheld,
        )
    if option is None:
        # THE CANDIDATE THE ANSWER WAS ABOUT, when there was exactly one of them
        # to be about. An item that offered several and was answered without
        # naming one is unspecific whatever the library holds now, and an item
        # with no stored options is an answer about nothing nameable.
        about = offered[0] if len(offered) == 1 else None
        if about is None or len(found.candidates) != 1:
            chosen = []
            unresolved = Why.VERDICT_UNSPECIFIC
        else:
            # BOUND, so the yes is read back against the candidate it was given
            # about. A different one on offer today is a candidate that is gone,
            # which is the state that already stalls the run and names the way out.
            chosen = [c for c in found.candidates if c.candidate_id == about]
            unresolved = Why.CANDIDATE_GONE
    else:
        chosen = [c for c in found.candidates if c.candidate_id == option]
        unresolved = Why.CANDIDATE_GONE
    if not chosen:
        return TrackMatch(
            wanted=found.wanted,
            state=MatchState.NEEDS_REVIEW,
            why=unresolved,
            candidates=found.candidates,
            item_id=item_id,
            withheld=found.withheld,
        )
    return TrackMatch(
        wanted=found.wanted,
        state=MatchState.MATCHED,
        why=Why.VERDICT_ACCEPTED,
        candidates=tuple(chosen),
        paths=tuple(path for candidate in chosen for path in candidate.paths),
        item_id=item_id,
        withheld=found.withheld,
    )


__all__ = [
    "APPROXIMATE_FLOOR",
    "APPROXIMATE_LIMIT",
    "ASKS_ABOUT_KEY",
    "ASKS_ABOUT_READING",
    "ASKS_ABOUT_RECORDING",
    "ASKS_ABOUT_VERSION",
    "BY_ISRC",
    "BY_SEARCH",
    "DIGEST_WIDTH",
    "KEY_QUESTIONS",
    "PAYLOAD_STATES",
    "OWNING_RULES",
    "QUESTION_KIND",
    "QUESTION_SHAPES",
    "READERS",
    "SPOTIFY",
    "STALLED",
    "TEXT",
    "TIDAL",
    "TOMBSTONE_KIND",
    "UNCREDITED_KIND",
    "VERSION_WORDS",
    "Acquisition",
    "Candidate",
    "LibraryIndex",
    "MatchResult",
    "MatchState",
    "Owned",
    "TrackMatch",
    "UnreadableList",
    "Wanted",
    "Why",
    "acquisition_options",
    "apply_verdict",
    "credited_members",
    "digest",
    "fold",
    "fold_isrc",
    "index_library",
    "index_paths",
    "isrc_token",
    "key_disagreement",
    "key_token",
    "listed_names",
    "listed_title",
    "every_question_identity",
    "question_identity",
    "question_shape",
    "read_row",
    "read_spotify_items",
    "read_text_lines",
    "read_text_rows",
    "read_tidal_tracks",
    "row_isrc",
    "recording_token",
    "resolve_all",
    "resolve_one",
    "split_ambiguous",
    "split_title",
    "split_version",
    "standing_tombstone",
    "tombstone_fold",
    "version_identity",
    "version_token",
]
