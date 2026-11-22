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

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from typing import Any

from cratekit.acquire.match_identity import (
    ASKS_ABOUT_KEY,
    ASKS_ABOUT_READING,
    ASKS_ABOUT_RECORDING,
    ASKS_ABOUT_VERSION,
    DIGEST_WIDTH,
    KEY_QUESTIONS,
    OWNING_RULES,
    PAYLOAD_STATES,
    QUESTION_KIND,
    QUESTION_SHAPES,
    TOMBSTONE_KIND,
    UNCREDITED_KIND,
    VERSION_WORDS,
    MatchState,
    Why,
    _digest,
    _sorted_words,
    bare_title,
    credited_members,
    digest,
    every_question_identity,
    fold,
    fold_isrc,
    isrc_token,
    key_token,
    listed_title,
    question_identity,
    question_shape,
    recording_identity,
    recording_token,
    same_title,
    split_ambiguous,
    split_title,
    split_version,
    title_identity,
    tombstone_fold,
    version_identity,
    version_token,
)
from cratekit.acquire.match_library import (
    LibraryIndex,
    Owned,
    _spelled_out,
    index_library,
    index_paths,
    remembered,
    reset_cache,
)
from cratekit.acquire.match_list import (
    READERS,
    SPOTIFY,
    TEXT,
    TIDAL,
    UnreadableList,
    Wanted,
    listed_names,
    read_row,
    read_spotify_items,
    read_text_lines,
    read_text_rows,
    read_tidal_tracks,
    row_isrc,
)
from cratekit.core import naming

#: The score at or above which an approximate recording hit is worth SHOWING a
#: person. Deliberately generous: nothing above it becomes a match, and
#: everything above it becomes a question unless its title alone falls under
#: :data:`APPROXIMATE_TITLE_FLOOR` (U286), so the cost of a low floor is noise in the
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
#: is scrolling. Spent twice on purpose: once as the number of recordings
#: :func:`_resembling` keeps, after the title test and never before it (U286),
#: and again as a truncation of the candidate list, because one
#: recording can be held as several versions at several keys and a limit on
#: recordings alone promises a number it does not deliver.
#:
#: ONLY THE SECOND SPEND WAS MEASURED, which made the first a written
#: justification with nothing behind it: multiplying the scorer's limit by four
#: left the whole suite green. The two spends are observable apart, and the thing
#: that separates them is the WITHHELD COUNT. Eight resembling recordings held as
#: one version each: with the recordings capped here, five candidates are built and
#: nothing is withheld; with the cap raised, eight are built, five are shown and
#: three are reported kept back. So a run that says "3 further candidates were
#: never shown" over a library of one-version recordings is a run whose
#: recording cap is not this constant, or one where card 833's spelled out
#: lookup found recordings outside the five, which ride on top of them (see
#: :func:`_resembling`), and
#: ``test_the_scorer_is_capped_at_the_same_number_the_offer_is`` asserts the
#: number is spent in both places.
APPROXIMATE_LIMIT = 5

#: The score the TITLE ALONE must reach for a recording the discovery score
#: found to be offered as a resemblance (U286). The discovery score reads the
#: artist and the title together, so with a short title the shared artist
#: carries an unrelated song over :data:`APPROXIMATE_FLOOR`: ``Monkey Safari,
#: Joy`` scored 84.2 against the library's ``Monkey Safari, Goodbye`` and was
#: held for review rather than downloaded. The artist agreeing is necessary for
#: an offer and never sufficient, so each hit's folded title is scored against
#: the wanted one with ``token_set_ratio`` and must reach this floor too.
#:
#: MEASURED, NOT CHOSEN. The five pairs sitting 99 found in the review queue
#: score 25.0 to 61.5 (``Get Out`` against ``Agenou`` the highest). One letter
#: changed in a title of three letters scores 66.67, the lowest a single
#: changed letter can give a title of three letters or more, and a dropped
#: word, an added word or the words reordered score 100. 66 is the highest
#: integer floor that keeps every one letter change of a three letter title.
#: A two letter title with one letter changed scores 50 and a one letter title
#: against another 0, so both settle missing by the same rule, as U286 asks.
#: ``test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way``
#: holds the value between its nearest neighbours.
APPROXIMATE_TITLE_FLOOR = 66



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
            option_id=f"aq_{_digest(BY_SEARCH, wanted.distinct, wanted.version_key)}",
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
            f"mt_{_digest(self.wanted.distinct, self.wanted.version_key, self.wanted.key_key)}"
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
    #
    # BY THE RECORDING'S IDENTITY and not its token, so two files whose titles
    # fold to nothing, ``🔥`` and ``❄`` by one artist, are two candidates and
    # not one titled by whichever came first and carrying the other's path.
    # The identity is the token for every title that folds to something, so
    # every such candidate keeps the identifier a recorded answer names.
    grouped: dict[tuple[str, str, str], list[Owned]] = {}
    for held in owned:
        grouped.setdefault((held.distinct, held.version_key, held.key_key), []).append(held)
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
    caller. An ISRC agrees only WITH the title, see :func:`resolve_one`, and
    the title is read by :func:`same_title`, so two titles that fold to nothing
    are one recording only when their bare text agrees.
    """
    if not same_title(held.title, wanted.title):
        return False
    if held.distinct == wanted.distinct:
        return True
    return fold(wanted.artist) in held.members or _carries(held, token)


def _approximate(
    wanted: Wanted, index: LibraryIndex, *, limit: int | None
) -> tuple[Owned, ...]:
    """Recordings that merely RESEMBLE the wanted one. Discovery, never identity.

    Scored on the folded recording token, so the artist and the title are both
    in the comparison: a title alone matches every cover version and every
    unrelated record that happens to share a common word.

    The scorer is imported here rather than at module scope because the parser
    imports every landed verb's module on every invocation, ``crate --help``
    included, and this is the only function in the unit that needs it. A cheap
    help screen is a property U5 states about the dispatcher, and paying for a
    scoring library to print one would take it away.

    THE SCORE IS ``token_sort_ratio``, computed as ``ratio`` over words sorted
    once (U265). The shipped call handed ``token_sort_ratio`` the raw tokens,
    and it split and sorted both strings again for every pair, so each library
    name was sorted once per wanted row. ``token_sort_ratio`` is ``ratio`` over
    the two sorted strings, so sorting each library name once for the index,
    and the wanted token once here, gives the same float for every pair, and
    the same ``extract`` over the same positions gives the same candidates in
    the same order with the same ties, floor and limit. The suite keeps the
    shipped call as the reference and holds this one equal to it, at the
    offer limit and with none.

    ``limit`` caps the RECORDINGS returned, ``None`` returning every one over
    the floor. The resolver asks for every one through :func:`_resembling`,
    which drops the hits whose title does not resemble before it caps them
    (U286), so an unrelated song cannot take a place a real one needed.
    """
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    recordings, sorted_choices = index.sorted_recordings()
    found = process.extract(
        _sorted_words(wanted.recording),
        sorted_choices,
        scorer=fuzz.ratio,
        score_cutoff=APPROXIMATE_FLOOR,
        limit=limit,
    )
    # BEST SCORE FIRST, and the order is load-bearing from here on. ``extract``
    # returns descending, ties in position order, and everything downstream
    # preserves it so that the offer limit drops the worst answers rather than
    # whichever sorted last. The position names the unsorted recording.
    return tuple(
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
    )


def _title_resembles(wanted: Wanted, held: Owned) -> bool:
    """Whether ``held``'s TITLE resembles the wanted one on its own (U286).

    ``token_set_ratio`` of the two folded titles against
    :data:`APPROXIMATE_TITLE_FLOOR`: a set measure, so a dropped or added word
    and reordered words score 100 and a typo scores as a typo, while two
    titles sharing no word score on their letters alone.

    THREE ALLOWANCES, each keeping the offer U286 found, and each because the
    cost of a wrong drop is a duplicate downloaded where the cost of a wrong
    offer is one question. A title that folds to nothing on either side holds
    no letter or digit to read, so this says nothing about it and the
    discovery score decides, as it always did. Two titles that are one string
    once their spaces are gone, ``O.K.`` and ``OK``, ``Good Bye`` and
    ``Goodbye``, are one title split differently: :func:`fold` turns a dot
    into a space, so they share no word and score on their letters alone,
    under the floor (review round one's finding). EQUALITY AND NOT A RATIO:
    ``getout`` against ``agenou`` scores 66.67, which would let one of the
    card's unrelated pairs back in. And a file whose artist and
    title are the row's swapped, a listing pasted title first or a file named
    the wrong way round, is the same record, which the word sort scores as one
    string at 100: each half then has to agree with the other side's other
    half by the same test, the equality included, so a dotted artist,
    ``M.I.A.`` against ``MIA``, crosses as a dotted title does (review round
    two's finding).
    """
    asked, found = fold(wanted.title), fold(held.title)
    if not asked or not found:
        return True
    if _agree(asked, found):
        return True
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)


def _agree(one: str, other: str) -> bool:
    """Whether two folded names agree for :func:`_title_resembles`: one string
    once their spaces are gone, as written or with each word of
    :data:`_SPELLED_OUT` spelled out, or ``token_set_ratio`` at or over
    :data:`APPROXIMATE_TITLE_FLOOR`. An empty side agrees with nothing here;
    the caller decides what a title that folds to nothing means.

    THE SPELLED OUT READING IS A THIRD WAY TO AGREE, NEVER A REPLACEMENT
    (card 833), so every pair that agreed still agrees: ``U Turn`` spelled out
    is ``youturn`` and no longer ``UTurn``, which still agrees as written.
    And it is compared by EQUALITY, NOT A RATIO: spelled out, ``2`` is ``to``,
    which scores 80 against an unrelated ``Tom``, and ``N`` is ``and``, 66.67
    against ``Ant``, the short title class U286 stopped offering."""
    from rapidfuzz import fuzz

    if one and (
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)
    ):
        return True
    return fuzz.token_set_ratio(one, other) >= APPROXIMATE_TITLE_FLOOR






def _resembling(wanted: Wanted, index: LibraryIndex) -> tuple[Owned, ...]:
    """What the approximate pass offers: the recordings discovery finds whose
    title resembles too, best score first, at most :data:`APPROXIMATE_LIMIT`
    of them, led by any the spelled out lookup finds outside those five.

    FILTERED BEFORE THE CAP, NOT AFTER IT (U286). Discovery returns every
    recording over the floor and the title test runs on each in score order,
    so a prolific artist's unrelated short titles, each outscoring a real near
    match through the shared artist, cannot fill the five and push it out:
    filtered after the cap, that row would read missing and download a record
    the library holds. And filtered before :func:`_candidates_for`, so a
    dropped hit never reaches the offer or the withheld count.

    One recording's versions are adjacent in discovery's answer and share one
    folded artist and title, so the first version answers for them all.

    THE SPELLED OUT LOOKUP FIRST, FOR WHAT THE FIVE LEFT OUT (card 833). A
    recording :meth:`LibraryIndex.spelled_alike` finds that is not among the
    five scored recordings, never scored or scored too low, is the same
    title under the reading, so it leads. One the five hold keeps its scored
    place, so a row the score already offered everything to is offered
    exactly as before. The five are the SCORED recordings, as before, and a
    lookup hit rides on top of them: spent once over both, a lookup hit
    pushed a scored recording out of the offer with nothing saying so
    (review round one). Now the offer's truncation drops it and the withheld
    count reports it.
    """
    scored: list[Owned] = []
    recordings = 0
    for _recording, versions in groupby(
        _approximate(wanted, index, limit=None), key=attrgetter("recording")
    ):
        held = tuple(versions)
        if not _title_resembles(wanted, held[0]):
            continue
        scored.extend(held)
        recordings += 1
        if recordings == APPROXIMATE_LIMIT:
            break
    # NOT AMONG THE FIVE, NOT MERELY NOT SCORED (review round two): a lookup
    # hit discovery ranked sixth or lower was skipped as scored and then cut
    # by the cap, never offered and never counted. No title test here: a
    # lookup hit is the row's title spelled out, which ``_agree`` always
    # takes.
    offered = {held.recording for held in scored}
    looked_up = [
        held
        for recording in index.spelled_alike(wanted.recording)
        if recording not in offered
        for held in index.versions(recording)
    ]
    return tuple(looked_up + scored)


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
    #
    # THE TITLE IS READ BY :func:`same_title`: two titles that fold
    # to nothing agree only when their bare text does, so a file carrying the
    # row's ISRC under another emoji title is doubtful, as another title is.
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
    settled = [held for held in carrying if same_title(held.title, wanted.title)]
    doubtful = [held for held in carrying if not same_title(held.title, wanted.title)]
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

    near = _resembling(wanted, index)
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


def _former_candidate_id(candidate: Candidate) -> str:
    """The identifier ``candidate`` had before a title's identity was read
    (card 834): the digest of the recording TOKEN rather than its identity.
    Equal to :attr:`Candidate.candidate_id` for every title that folds to
    something."""
    token = recording_token(candidate.artist, candidate.title)
    return f"cd_{_digest(token, version_token(candidate.version), candidate.key or '')}"


def current_option(found: TrackMatch, option: str, title: object) -> str:
    """The candidate a recorded answer names today, by the identifier and the
    title it was given about.

    ``option`` unchanged unless it names no candidate on offer and a
    candidate's FORMER identifier is ``option`` and that candidate's title is
    ``title`` by :func:`same_title`; then that candidate's identifier. A file
    whose title folds to nothing was offered under an identifier hashed from
    the artist's empty fold, and reading titles by their identity moved it, so
    a person's acceptance of that file, recorded before, read as a candidate
    gone while the file was on disk (review round two). The title is what
    keeps the old identifier from answering for ANOTHER such file now under
    it: the old identifier was every such file by the artist at that version
    and key, so a held ``🔥`` replaced by a ``❄`` stays a candidate gone. A
    caller with no stored title passes ``None`` and the answer is not carried.
    """
    if title is None or any(one.candidate_id == option for one in found.candidates):
        return option
    carried = [
        one for one in found.candidates
        if _former_candidate_id(one) == option and same_title(one.title, title)
    ]
    # AT MOST ONE FITS: the former identifier fixes the token, the version
    # and the key, the title fixes the title's identity, and together those
    # are the group :func:`_candidates_for` makes one candidate of.
    return carried[0].candidate_id if carried else option


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
    "APPROXIMATE_FLOOR", "APPROXIMATE_LIMIT", "APPROXIMATE_TITLE_FLOOR", "ASKS_ABOUT_KEY",
    "ASKS_ABOUT_READING", "ASKS_ABOUT_RECORDING", "ASKS_ABOUT_VERSION", "BY_ISRC", "BY_SEARCH",
    "DIGEST_WIDTH", "KEY_QUESTIONS", "PAYLOAD_STATES", "OWNING_RULES", "QUESTION_KIND",
    "QUESTION_SHAPES", "READERS", "SPOTIFY", "STALLED", "TEXT", "TIDAL", "TOMBSTONE_KIND",
    "UNCREDITED_KIND", "VERSION_WORDS", "Acquisition", "Candidate", "LibraryIndex", "MatchResult",
    "MatchState", "Owned", "TrackMatch", "UnreadableList", "Wanted", "Why", "acquisition_options",
    "apply_verdict", "bare_title", "credited_members", "current_option", "digest", "fold",
    "fold_isrc", "index_library", "index_paths", "isrc_token", "key_disagreement", "key_token",
    "listed_names", "listed_title", "every_question_identity", "question_identity",
    "question_shape", "read_row", "read_spotify_items", "read_text_lines", "read_text_rows",
    "read_tidal_tracks", "remembered", "reset_cache", "row_isrc", "recording_identity",
    "recording_token", "resolve_all", "resolve_one", "same_title", "split_ambiguous", "split_title",
    "split_version", "standing_tombstone", "title_identity", "tombstone_fold", "version_identity",
    "version_token",
]
