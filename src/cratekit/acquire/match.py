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
until U24 merges, at which point they collapse into imports. The REVIEW ITEM
identity is a different thing and stays here: see ``question_identity``.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
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
    #: A person already said one of the owned versions is this record.
    VERDICT_ACCEPTED = "verdict-accepted"
    #: A person already said none of them is.
    VERDICT_REJECTED = "verdict-rejected"
    #: The recording is owned, the version is not. R11's whole point.
    VERSION_DIFFERS = "version-differs"
    #: Only a scored, approximate hit on the recording. Discovery, never identity.
    TITLE_APPROXIMATE = "title-approximate"
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


#: The kind a version-match question is offered under. An identifier, normalized
#: by the queue on the way in, and the same one every producer of this question
#: must use or two spellings become two items for one candidate.
QUESTION_KIND = "version-match"

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

#: The score at or above which an approximate recording hit is worth SHOWING a
#: person. Deliberately generous: everything above it becomes a question and
#: nothing above it becomes a match, so the cost of a low floor is noise in the
#: queue and the cost of a high one is a track reported missing that the library
#: already holds under a slightly different spelling.
APPROXIMATE_FLOOR = 82

#: How many approximate CANDIDATES are offered for one wanted track. A person
#: choosing between five candidates is choosing; a person choosing between forty
#: is scrolling. Spent twice on purpose: once as the recording limit the scorer
#: is given, and again as a truncation of the candidate list, because one
#: recording can be held as several versions at several keys and a limit on
#: recordings alone promises a number it does not deliver.
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
    """
    remaining = str(title).strip()
    qualifiers: list[str] = []
    while True:
        found = _TRAILING_GROUP.search(remaining)
        if found is None:
            break
        inside = found.group(1).strip()
        remaining = remaining[: found.start()].strip()
        folded = fold(inside)
        if any(folded.startswith(fold(prefix)) for prefix in _CREDIT_PREFIXES):
            continue
        if inside:
            qualifiers.append(inside)
    return remaining, " ".join(reversed(qualifiers))


#: Words that END a dash-introduced tail that is a VERSION rather than the rest
#: of a title. This is what separates "Sun Path - Nightwave Remix" from "Sun -
#: Rise". Deliberately a vocabulary rather than a shape: the shape is ambiguous,
#: so anything not recognized stays in the title, and the cost of a word this
#: list is missing is a question rather than a wrong join.
_DASH_VERSIONS: frozenset[str] = frozenset(
    {
        "acoustic",
        "bootleg",
        "demo",
        "dub",
        "edit",
        "extended",
        "instrumental",
        "live",
        "mix",
        "remaster",
        "remastered",
        "remix",
        "reprise",
        "rerecorded",
        "rework",
        "version",
        "vip",
    }
)

#: Words that START one, kept to the one convention that needs it: the public
#: playlist API ships "Remastered 2011" and "Remastered Version", so the year is
#: the last word and the vocabulary above cannot see it. Deliberately tiny, since
#: a leading-word rule is the loose one: "Reprise Of Nothing" is a title.
#:
#: These are also the ONLY words allowed to make a one-word tail a version. See
#: :func:`_is_a_version`.
_DASH_VERSION_HEADS: frozenset[str] = frozenset({"remaster", "remastered", "rerecorded"})

#: The separator the public playlist API puts before a version. The same three
#: characters ``read_text_lines`` splits an artist from a title on, which is why
#: the two readers apply it at different ends of the line.
_DASH = " - "


def _is_a_version(tail: str) -> bool:
    """Whether a dash-introduced tail names a version rather than ending a title.

    A ONE-WORD TAIL IS NOT ENOUGH, and that is the whole of the second version of
    this rule. Matching on the last vocabulary word alone split every title whose
    final word happens to be one of seventeen: "Ziggy Stardust - Reprise", "Hurt
    - Reprise", "Long - Live", "Studio 54 - Live", "Pump Up The Volume -
    Extended", "Nice Up - Dub", "Beat It - Demo", "Sunset - Acoustic". The
    reprise class is the sharpest, because an album reprise is a separate
    composition, so the mangle reframed it from "the library holds nothing like
    this" to "the library holds this record as a different version", and
    accepting that reports ownership of a track the library does not hold.

    The two costs are not comparable, which is what decides the rule. A tail this
    misses stays in the title and produces a QUESTION. A tail this takes wrongly
    produces a wrong join, which is the one thing this unit exists to remove. So
    a bare qualifier is left alone and only a multi-word tail, or one of the three
    head words the public playlist API actually uses on its own, is read.

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
    and :func:`_is_a_version` says what that means and why a bare one-word tail
    does not qualify.

    THE VOCABULARY IS ENGLISH, so this convergence is English-only. A catalogue
    spelling its versions in another script converges through the bracketed
    reader and not through this one, which is recorded rather than hidden: see
    R-19 in docs/residual-findings.md.
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


def listed_title(title: str, version: str) -> str:
    """A title and a separate version qualifier, put back into one string.

    ONLY FOR A SOURCE THAT NEVER HAD ONE. A provider row carries the version in
    its own field, so there is no original spelling to preserve and something has
    to be composed; parentheses, because that is what a library row uses. Every
    other source hands over a title that already carries its version, and that
    ORIGINAL STRING is what gets hashed. See :attr:`Wanted.listed`.
    """
    return f"{title} ({version})" if str(version).strip() else str(title)


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
    artist: str, title: str, version: str, key: str | None = None
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

    The key set never varies. The field is present and empty for the questions
    that are not about a key, so the version question a list asks with a key and
    the one it asks without are still one item and one answer.
    """
    return {
        "recording": recording_token(artist, title),
        "version": version_token(version),
        "key": key_token(key),
    }


def _digest(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


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
    #: THE TITLE EXACTLY AS THE SOURCE SPELLED IT, before the version came out of
    #: it. Carried rather than recomputed because the tombstone identity is a
    #: hash of a title, the other side of that hash reads a library row's Title
    #: column verbatim, and a title this module took apart and put back together
    #: is a different string. Empty for a source that never had one, which is a
    #: provider row carrying its version in a separate field.
    spelled: str = ""

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

        Composition is the fallback and not the rule. It is reached only by a
        source that hands over a version in its own field, where there is no
        original string to preserve and something has to be built.
        """
        return self.spelled or listed_title(self.title, self.version)

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36), which is U24's and not this module's."""
        return version_identity(artist=self.artist, title=self.listed)

    @property
    def suppression_spellings(self) -> tuple[dict[str, str], ...]:
        """Every identity one version of this recording could have been recorded under.

        CONSULTING IS NOT RECORDING, and the two get different rules. A recorder
        must write one identity, or one deletion becomes several records; a
        consulter that asks under one spelling and misses re-acquires a track
        somebody deleted on purpose, with nothing raised anywhere. So the store
        is asked under the spelling this list used AND under the composed one,
        which is what a provider-sourced list would have produced for the same
        version.

        This does NOT loosen KTD16. Every spelling here names the SAME version of
        the same recording, so no lookup can cross a version boundary and a
        tombstone over one remix can still never suppress another.
        """
        seen: list[dict[str, str]] = []
        for title in (self.listed, listed_title(self.title, self.version)):
            built = version_identity(artist=self.artist, title=title)
            if built not in seen:
                seen.append(built)
        return tuple(seen)

    def question(self, *, about_the_key: bool = False) -> dict[str, str]:
        """THE REVIEW ITEM identity, which is this module's.

        Separate from :attr:`identity` because they address different things: a
        tombstone outlives every list and a question is one thing somebody was
        asked. See :func:`question_identity` for why the key is in it.
        """
        return question_identity(
            self.artist, self.title, self.version, self.key if about_the_key else None
        )


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


def _first_named(entries: object) -> str:
    """The first non-empty name in a list of artists, whatever they are made of."""
    if not isinstance(entries, (list, tuple)):
        return ""
    for entry in entries:
        if isinstance(entry, str) and entry.strip():
            return entry.strip()
        name = _field(entry, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return ""


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

    A row that yields neither an artist nor a title is refused rather than read
    as an anonymous track, which is the same rule ``read_text_lines`` already
    stated in prose and the provider path did not apply. Three things went wrong
    without it, all of them quietly: two rows carrying nothing but an identifier
    folded to ONE match identifier and one of the two vanished from a payload a
    consumer keyed by id; an unreadable row matched any junk file in the library
    whose name folded to nothing and was reported owned; and a row whose artists
    arrived in a shape this reader did not know reported a held track missing.
    """
    raw_title = str(_field(row, "title", "") or _field(row, "name", "")).strip()
    declared = str(_field(row, "version", "")).strip()
    title, embedded = split_title(raw_title)
    external = _field(row, "external_ids", {})
    isrc = _field(row, "isrc") or (_field(external, "isrc") if external else None)
    artist = _artist_of(row)
    if not artist and not title:
        raise UnreadableList(
            f"track {position} names neither an artist nor a title, so nothing "
            f"can be looked up for it and it would match any file in the library "
            f"whose name folds to nothing",
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
        # KEPT ONLY WHEN THE VERSION CAME OUT OF IT. A row that declared its
        # version in its own field never spelled the two together, so there is no
        # original to preserve and the composed form is the honest answer. A row
        # that spelled them together is addressed by exactly what it said.
        spelled="" if declared else raw_title,
    )


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

    @property
    def recordings(self) -> tuple[str, ...]:
        return tuple(self.by_recording)

    def versions(self, recording: str) -> tuple[Owned, ...]:
        return self.by_recording.get(recording, ())

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
    """
    stem = path.stem
    head = naming.parse_head(stem, template=template) or {}
    body = naming.strip_heads(stem, template=template)
    artist_part, separator, title_part = body.partition(template.segment_sep)
    if not separator:
        artist_part, title_part = "", body

    tagged_artist = str(tags.read_tag(path, "artist") or "").strip()
    tagged_title = str(tags.read_tag(path, "title") or "").strip()
    named_artist, named_title = artist_part.strip(), str(title_part).strip()
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title
    title, version = split_title(spelled)

    written_key = head.get("key")
    key = written_key or tags.read_tag(path, "initialkey")
    return Owned(
        path=path,
        artist=artist,
        title=title,
        version=version,
        key=str(key).strip() if key else None,
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
    shape = template or naming.NameTemplate()
    suffixes = {suffix.lower() for suffix in naming.AUDIO_EXTS}
    grouped: dict[str, list[Owned]] = {}
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            held = reader(path, shape)
            grouped.setdefault(held.recording, []).append(held)
    return LibraryIndex(by_recording={key: tuple(rows) for key, rows in grouped.items()})


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
    that disagreement is a product decision recorded as R-17 and reserved for a
    person. What is settled either way is that the options have to EXIST: the
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


#: The whys whose question is ABOUT the key rather than about the version. Read
#: by the item identity, so a key question and a version question about one
#: recording are two items and one answer never settles the other.
KEY_QUESTIONS: frozenset[Why] = frozenset({Why.KEY_RELATIVE, Why.KEY_DIFFERS})

#: The whys that mean a STORED VERDICT COULD NOT BE APPLIED. The item is resolved
#: in the queue, so a listing of open items does not show it and resolving it
#: again is refused; the only way forward is to clear it. Named here so the verb
#: can name the remedy that actually works rather than the one that reads well.
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
    asks_about_key: bool = False
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
        """THE REVIEW ITEM identity. Frozen at resolution, never re-derived.

        ``asks_about_key`` is carried as a field rather than recomputed from
        ``why`` because ``apply_verdict`` rewrites ``why`` to say what happened
        to the answer, and an identity that changed when the answer arrived would
        write a verdict onto one item and read it back off another.
        """
        return self.wanted.question(about_the_key=self.asks_about_key)

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
        if recording != wanted.recording:
            difference = Why.TITLE_APPROXIMATE
        elif version_key != wanted.version_key:
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


def _suppressed(
    wanted: Wanted,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> str | None:
    """The identifier of the tombstone standing over this version, or None.

    Asked under every spelling one version could have been recorded under, for
    the reason :attr:`Wanted.suppression_spellings` gives: a consult that misses
    re-acquires something somebody deleted on purpose and nothing anywhere
    reports it, while an extra lookup costs one set membership test.
    """
    for identity in wanted.suppression_spellings:
        if suppresses(TOMBSTONE_KIND, identity):
            return suppression_id(TOMBSTONE_KIND, identity)
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
    """
    owned = index.versions(wanted.recording)
    exact = [held for held in owned if held.version_key == wanted.version_key]

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
                why=Why.EXACT,
                paths=tuple(str(held.path) for held in exact),
            )
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            # The relative case wins the reporting when both are present, because
            # it is the one that looks like agreement to everything downstream.
            why=Why.KEY_RELATIVE if Why.KEY_RELATIVE in disagreements else Why.KEY_DIFFERS,
            candidates=_candidates_for(wanted, exact),
            asks_about_key=True,
        )

    if owned:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,
            candidates=_candidates_for(wanted, owned),
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

    standing = _suppressed(wanted, suppresses=suppresses, suppression_id=suppression_id)
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
    one to name. The queue allows a verdict with no option, so with several
    candidates on offer "accepted" says the library has the record and does not
    say which version, and taking all of them would report the library holding
    three copies of one record on the strength of one unspecific yes.

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
            asks_about_key=found.asks_about_key,
            withheld=found.withheld,
        )
    if not accepted:
        standing = _suppressed(
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
                asks_about_key=found.asks_about_key,
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
            asks_about_key=found.asks_about_key,
            withheld=found.withheld,
        )
    if option is None:
        chosen = list(found.candidates) if len(found.candidates) == 1 else []
        unresolved = Why.VERDICT_UNSPECIFIC
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
            asks_about_key=found.asks_about_key,
            withheld=found.withheld,
        )
    return TrackMatch(
        wanted=found.wanted,
        state=MatchState.MATCHED,
        why=Why.VERDICT_ACCEPTED,
        candidates=tuple(chosen),
        paths=tuple(path for candidate in chosen for path in candidate.paths),
        item_id=item_id,
        asks_about_key=found.asks_about_key,
        withheld=found.withheld,
    )


__all__ = [
    "APPROXIMATE_FLOOR",
    "APPROXIMATE_LIMIT",
    "BY_ISRC",
    "BY_SEARCH",
    "KEY_QUESTIONS",
    "PAYLOAD_STATES",
    "QUESTION_KIND",
    "READERS",
    "SPOTIFY",
    "STALLED",
    "TEXT",
    "TIDAL",
    "TOMBSTONE_KIND",
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
    "fold",
    "index_library",
    "key_disagreement",
    "key_token",
    "listed_title",
    "question_identity",
    "read_spotify_items",
    "read_text_lines",
    "read_text_rows",
    "read_tidal_tracks",
    "recording_token",
    "resolve_all",
    "resolve_one",
    "split_title",
    "split_version",
    "tombstone_fold",
    "version_identity",
    "version_token",
]
