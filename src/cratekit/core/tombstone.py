"""What a tombstone and a decline are ADDRESSED BY. One vocabulary, two readers.

R36 says every completed deletion writes a tombstone identifying that exact
version of that recording, that acquisition sources skip a tombstoned version and
report the suppression rather than omitting it silently, and that tombstones are
listable and revocable. Two entirely different parts of the product therefore
have to agree about what "that exact version" means:

* the deletion pass RECORDS a suppression, from a row rekordbox soft-deleted;
* an acquisition pass CONSULTS it, from a candidate a provider returned.

Neither knows the other exists, and neither may. Deletion is a toggleable feature
module; a slim install with deletion switched off still has to be able to ask
whether a candidate is suppressed, so an acquisition module reaching into the
deletion package for the answer would be an import that is absent exactly when it
is needed. So the identity lives here, below both of them, and both spell it the
same way because there is only one way to spell it.

**KTD16: a tombstone identifies a VERSION, not a recording**, chosen over
recording-level and fuzzy matching because the library is remix-heavy and fuzzy
identity is the precise defect the three-state match exists to prevent. The
identity is therefore the artist and the title, and THE TITLE IS REQUIRED TO
CARRY THE VERSION: ``Something (Someone's Remix)`` and ``Something`` are two
identities, so deleting one never suppresses the other. That is AE17 stated as a
data structure rather than as a policy somebody has to remember.

**AND "REQUIRED TO" IS THE CORRECTION. IT USED TO READ "IS", WHICH REKORDBOX'S
OWN SCHEMA CONTRADICTS.** ``djmdContent`` has a dedicated ``RemixerName`` column
and a ``Subtitle`` beside it, so a remix-heavy library routinely holds two
different versions of one recording whose ``Title`` is the same bare string and
whose mix name sits in a column of its own. Asserting that the title carries the
version made the identity of "deadmau5 / Strobe (Michael Woods Remix)" collapse
onto the identity of the original whenever rekordbox had filed the mix name
where it belongs, and the consequence runs in the direction this module calls the
worse one: deleting the remix reports the ORIGINAL suppressed and never
re-acquires it. Over-suppression silently withholds music the user wants.

So a producer that holds the version in a separate field COMPOSES IT INTO THE
TITLE before asking for an identity, through :func:`version_title`, and the rule
lives here rather than at each producer for the same reason the store key does.
It keeps the two-field identity intact, which the ISRC paragraph below is the
argument for: a provider candidate arrives with the mix name already inside its
title and no separate field to offer, so a THIRD key would be a key one side
never has.

**WHAT COMPOSITION GUARANTEES, NARROWED TO WHAT IS TRUE.** It used to be written
here that composition "can only ever split one identity into two, never merge two
into one", so it moved strictly away from over-suppression. That is true WHEN THE
SECOND FIELD REALLY IS A MIX NAME, which is the case it was written for, and it
is false in general. Composing produces a title, and a title is a string another
row may already hold, so two identities that were distinct MERGE whenever one
row's composed title equals another row's plain one::

    ("Everything", "I Do")  and  ("Everything (I Do)", "")
    ("Sun", "Sun Path")     and  ("Sun (Sun Path)", "")

Both pairs land on one identity, and deleting either member suppresses the other,
which is the over-suppression direction.

**AND THE PARAGRAPH THAT USED TO FOLLOW CALLED THOSE UNREACHABLE, WHICH WAS
FALSE FOR THE COLUMN IT NAMED AS THE SAFE ONE.** It argued that they need a
version field holding something that is not a mix name, and that ``RemixerName``
cannot be one because rekordbox's schema dedicates it to a remixer. That is the
error: a remixer is an ARTIST, so ``RemixerName`` holds an artist NAME, and an
artist name is exactly "something that is not a mix name". ``("Sun", "Sun Path")``
against ``("Sun (Sun Path)", "")`` is reachable the moment a row credits a
remixer called Sun Path, and the column was believed on sight with no test of any
kind applied to it. The safety argument was resting on the one column it did not
hold for.

Composing a bare artist name was also unmatchable in its own right, which is the
same defect :func:`_already_carries` names below and closes only for the branch
where the title already carries the bracket: a row spelled ``Strobe`` with
``Michael Woods`` in the column composed ``strobe (michael woods)``, and no
provider spells that. So a producer holding a REMIXER passes it through
:func:`remixer_title`, which spells it the way a provider does before composing,
and the two shapes close together: ``Strobe (Michael Woods Remix)`` is a string a
provider produces AND is not a title another row is likely to hold bare.

So the honest statement is that composition is safe because of what is fed to it,
not because of what it does, the producer is where that is guarded, and what
guards it is different per column. ``RemixerName`` is spelled before it is
composed. ``Subtitle`` is ID3 ``TIT3``, holds anything at all, and is believed
only when it reads as a version, which is :data:`VERSION_WORDS` and is a closed
list with both its error directions measured and written down there.

**AND THE COLLISION THAT SURVIVES BOTH OF THOSE IS BOUNDED FROM OUTSIDE THIS
MODULE, BY THE ISRC.** Two rows of one recording whose designations the
vocabulary did not believe both keep a bare title, so they land on one identity
and deleting either suppresses the other, which is the over-suppression
direction. Nothing here can tell that from the legitimate convergence
composition is REQUIRED to produce, ``Strobe`` with a remixer against ``Strobe
(Michael Woods Remix)`` with none, because both are two rows landing on one
identity and the identity IS the claim that they are one version. The row
carries the discriminator anyway: the legitimate convergence is one recording
and carries ONE code, the collision is two recordings and carries TWO. The check
belongs to the recorder, which sees a whole collection at once, and lives in
``deletion.stores.ambiguous_versions``. It is stated here because this module is
where the collision is argued and an argument whose answer lives elsewhere has
to say so.

**WHY THE ISRC IS NOT IN THE IDENTITY, recorded because it is the obvious
suggestion and it is wrong.** An ISRC does identify a specific recording, and a
database row often carries one. A provider candidate often does not. If the
identity carried the code, a tombstone written from a row that had one would fail
to suppress the same version arriving from a source that had none: the two
mappings differ, so the two hashes differ, and the suppression silently misses.
An identity is only useful when two producers who have never met agree on it
without coordinating, which means it may only contain fields BOTH sides always
have. The code is recorded in the suppression's payload instead, where a person
reading the listing can see it and nothing joins on it.

**Folding, and its one limit.** Case, surrounding space, internal runs of space,
and Unicode composition form are all folded, because those four differ routinely
between a database row and a search result and none of them is a different
version. Nothing else is folded: punctuation stays, so ``Track (Live)`` and
``Track [Live]`` are two identities. That is deliberately conservative. A missed
suppression re-acquires something and REPORTS it; an over-eager one silently
withholds music the user wants, and the two costs are not comparable.

Layer note: DOMAIN. It names a state entry key and no verb, it reads no file, and
it imports nothing above the foundation. The stores themselves live in
``cratekit.core.review``, which is infrastructure, so a caller that wants to
record or consult a suppression builds a ``DecisionStore`` on the key below and
asks it. Two names from one module, so a consult and a record cannot drift apart.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The declared state entry holding tombstones, spelled ONCE. A caller opens it
#: with ``review.DecisionStore(tombstone.STORE_KEY, cfg)``. Naming it here rather
#: than at each call site is what stops the recorder and the consulter opening
#: two different stores, which would be a suppression that suppresses nothing and
#: nothing to notice it.
STORE_KEY = "tombstones"

#: R35's other half: the files a person looked at and decided to keep. Same
#: module for the same reason, since the deletion pass consults one and records
#: the other in the same walk.
DECLINE_STORE_KEY = "declines"

#: The kind a tombstone carries: one deleted version of one recording.
KIND_VERSION = "version"

#: The kind a decline carries. It is a ROW's file rather than a version, and that
#: difference is the point. Declining is "leave this file where it is", which is a
#: decision about one library row; tombstoning is "never acquire this again",
#: which is a decision about a recording that outlives the row. Recording both
#: under one kind would make revoking a decline un-suppress an acquisition.
KIND_REMOVED_FILE = "removed-file"

#: Runs of any whitespace collapse to one space. Written as a pattern rather than
#: as ``" ".join(value.split())`` so the intent survives: this folds SPACING, and
#: it is the only structural thing here that is folded.
_SPACING = re.compile(r"\s+")

#: Every parenthesised or bracketed group in a title, which is where a title that
#: already carries its own mix name keeps it. Non-nesting on purpose: a title with
#: nested brackets is not a shape any provider spells, and the inner group is
#: matched on its own anyway.
_BRACKETED = re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]")

#: Everything that is not a letter or a digit, for :func:`fold_code`. ``[\W_]``
#: rather than ``[^0-9a-z]`` so that a non-ASCII alphanumeric survives as itself:
#: dropping it would merge two values that are genuinely different, and merging
#: two codes is the over-suppression direction.
_NOT_A_CODE_CHARACTER = re.compile(r"[\W_]+", re.UNICODE)

#: The bracket characters, for the value that is about to be put INSIDE a bracket.
#: A delimiter appearing in its own content is not a delimiter, so they are
#: replaced with a space rather than deleted, and the whitespace collapse behind
#: them closes the gap.
_BRACKET_CHARACTERS = re.compile(r"[()\[\]]+")

#: The words that make a value a VERSION DESIGNATION rather than a note about the
#: track. A closed, explicit list rather than a shape test, because "does this
#: read as a mix name" has no syntax to test: ``Extended Mix`` and ``Anjunadeep``
#: are the same shape and only the vocabulary tells them apart.
#:
#: **IT LIVES HERE, BELOW BOTH READERS, FOR THE REASON THE STORE KEY DOES.** It
#: was private to ``deletion.library``, where it answered one question: is this
#: ``Subtitle`` a version. It moved here when a second question was routed
#: through it, and a vocabulary with two callers in two packages is the shape
#: this module exists to prevent.
#:
#: **IT HAS ONE CALLER AGAIN, AND THE SECOND QUESTION WAS NOT A QUESTION FOR A
#: VOCABULARY.** :func:`reads_as_version` asks whether a version word appears
#: ANYWHERE, which is the only thing that can be asked of a free text column, and
#: the false positives measured below are exactly the values where that is wrong:
#: artist and label names carrying a version word. Round five asked that same
#: test about a ``RemixerName`` and round six asked a positional variant of it,
#: and both were asking a word list to classify a column whose schema already
#: says it holds an artist name. :func:`already_spelled_as_a_remix` replaces both
#: and consults nothing here; the measurement that decided it is on that
#: function. This list now answers the belief question for ``Subtitle`` and
#: nothing else.
#:
#: **BOTH ERROR DIRECTIONS ARE MEASURED, AND THEY ARE NOT SYMMETRIC.** Against 75
#: genuine version designations a real library holds, 56 read as NOT a version:
#: ``Acappella``, ``Vocal``, ``Refix``, ``Redux``, ``Rmx``, ``Dubplate``,
#: ``Nightcore``, ``Slowed``, ``12 Inch``, ``Ao Vivo``, ``Versión`` and the rest
#: of a long tail, including every non-English spelling. Against 42 ordinary ID3
#: ``TIT3`` values, 15 read AS a version: ``Original Motion Picture Soundtrack``,
#: ``Extended Play``, the labels ``Club Sweat`` and ``Toolroom Club``, and the
#: artists ``Radio Slave``, ``Dub Pistols``, ``Cut Chemist`` and ``Mix Master
#: Mike``.
#:
#: A FALSE NEGATIVE leaves the row with a bare title, so two versions of one
#: recording collide onto one identity and deleting either suppresses the other:
#: the user loses a track they did not delete, which is the direction this module
#: calls the worse one. A FALSE POSITIVE composes an extra parenthetical, so the
#: tombstone is written and listable and matches no provider spelling: the
#: deletion fails to stick and the version becomes re-acquirable. Under those
#: costs "believe the column unless there is a reason not to" is the cheaper
#: default and this list has it backwards.
#:
#: **IT IS NOT REPAIRED BY ADDING WORDS AND THE MEMBERSHIP IS PINNED EXACTLY.**
#: Adding the 56 spellings would move the rate and not the shape: a closed list
#: cannot be complete over a free text column, and the previous round's list
#: could be NARROWED word by word with the suite staying green, which is the
#: property that lets a defect walk back in. An exact membership assertion is
#: what catches that, and it catches widening too. Flipping the default is the
#: real repair and it is not this round's: it regresses an accepted finding, the
#: label written into an identity, and it introduces its own collision, the one
#: the module docstring above spells ``("Sun", "Sun Path")``, which nothing local
#: can tell from a legitimate convergence. That is recorded rather than done.
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

#: Splits a folded value into its words, so a vocabulary hit is a WORD and not a
#: substring. Without it ``Remixed Records``, a label, would read as a version and
#: ``Anjunadeep`` would too, on the ``dee``-shaped accidents a substring test
#: makes. It is a NON-WORD split rather than a whitespace one, so ``Re-Edit`` and
#: ``Extended/Club Mix`` are read as the several words they are.
_WORD_SPLIT = re.compile(r"\W+", re.UNICODE)

#: The designation a provider appends to a remixer's name. Named rather than
#: written inline because it is the one string that makes a composed remix title
#: match a provider's spelling, and a literal buried in a format string is not a
#: decision anybody can find.
REMIX_DESIGNATION = "Remix"


def already_spelled_as_a_remix(value: str) -> bool:
    """Whether appending :data:`REMIX_DESIGNATION` would write that word twice.

    **NO VOCABULARY IS CONSULTED, AND THAT IS THE WHOLE OF THE CHANGE.** Two
    rounds asked a version-word list whether a ``RemixerName`` "reads like a
    designation": round five asked whether a version word appeared ANYWHERE,
    round six asked whether it appeared LAST. Both are classifiers over a column
    whose own schema settles the question, since ``RemixerName`` is an
    association proxy over ``RemixerID`` into ``djmdArtist`` and therefore holds
    an ARTIST NAME. Asking whether an artist name reads like a designation is the
    wrong question of the wrong column, and the two rounds got two different
    wrong answers to it.

    **MEASURED, OVER 65 VALUES IN THREE CLASSES.** 40 genuine mix-name
    designations, 15 artist names whose last word is in the vocabulary
    (``The Cut``, ``Todd Terry Live``, ``Defected Radio``), and 10 artist names
    carrying a vocabulary word anywhere but last (``Radio Slave``, ``Cut
    Chemist``, ``Cut Copy``). Misses, meaning a composed title that is not what a
    provider spells for that version:

    ======================================  ===========  ===========  =========
    rule                                    designation  artist name  total
    ======================================  ===========  ===========  =========
    round five ``reads_as_version``          8 of 40     25 of 25     33 of 65
    round six ``ends_as_a_designation``     20 of 40     15 of 25     35 of 65
    unconditional append, no test at all    40 of 40      0 of 25     40 of 65
    this rule                               38 of 40      0 of 25     38 of 65
    ======================================  ===========  ===========  =========

    **THE TOTAL COLUMN IS REPORTED AND IS NOT THE CRITERION, deliberately.** It
    is a weighted average whose weights are how often this column holds a
    designation rather than an artist name, and nothing in this repository
    samples a real ``RemixerName``, so that weight is exactly the unmeasurable
    frequency the residual findings deleted a claim about. The class columns are
    the measurement, and on the class the schema says the column holds, this
    rule and the no-test rule miss NOTHING and both vocabulary rules miss most of
    it.

    **THE TWO CLASSES OF ERROR ARE NOT EQUALLY BAD, AND THIS IS STRUCTURAL RATHER
    THAN FREQUENTIAL.** Getting a DESIGNATION wrong appends, giving
    ``(Extended Mix Remix)``, which no provider spells: the tombstone misses, so
    the deletion fails to stick and the version is re-acquirable, which is the
    under-suppression direction this module calls the milder one. Getting an
    ARTIST wrong leaves the name verbatim, giving ``(the cut)``, and that has
    BOTH directions: it misses the provider spelling, AND it is the same string
    ``Subtitle`` composes for a designation reading ``The Cut``, so one identity
    now stands for two versions and deleting either suppresses the other. Under
    that asymmetry the right rule is the one that never errs on an artist name,
    whatever it costs on designations.

    **WHY A TEST AT ALL RATHER THAN APPENDING UNCONDITIONALLY.** The two rules
    differ on exactly the values whose last word is already ``Remix`` and agree
    everywhere else, which is structural rather than sampled: the test IS "is the
    last word ``Remix``", so where it answers no both rules append the same word to
    the same value. Where it answers yes the unconditional rule writes ``(Michael
    Woods Remix Remix)`` and this writes ``(Michael Woods Remix)``, which is what a
    provider spells when Michael Woods is the remixer. So this dominates the
    unconditional rule POINTWISE, is never worse on any value whatsoever, and
    needs no claim about how often anything happens.

    **A COUNT OF THE DIFFERING VALUES IS NOT EVIDENCE FOR THAT AND IS NOT GIVEN.**
    An earlier draft cited "two of the 65", which is simply how many ``Remix``
    tailed values the set happens to contain, so it measures the set rather than
    the rule and would move if a value were added. The pointwise claim above holds
    at any size of set, and it is the claim.

    **AND IT CANNOT MANUFACTURE THE CONVERGENCE THE VOCABULARY RULE DID.** The
    verbatim branch fires only on a value that already ENDS in ``Remix``. A
    ``Subtitle`` holding that identical string names that identical version, so
    two rows landing on one identity through this branch are one version filed
    twice, which is the convergence the identity is supposed to find. That is not
    true of a branch firing on ``The Cut``, where the artist reading and the
    designation reading are two different versions wearing one string.

    **ITS OWN ERROR DIRECTION, STATED.** An artist whose name's last word is
    literally ``Remix`` is left verbatim and composes an unmatchable identity.
    None is known and none is in the value set; the direction is
    under-suppression, so the cost is a deletion that does not stick.
    """
    words = [word for word in _WORD_SPLIT.split(fold(value)) if word]
    return bool(words) and words[-1] == fold(REMIX_DESIGNATION)

#: The words that open a FEATURED CREDIT. A bracketed group starting with one of
#: these names a guest performer rather than a version of the recording, and the
#: difference decides an identity: ``Losing It (feat. Anna)`` with the remixer
#: column empty and the same title with ``Anna`` in it are two different records,
#: and treating the credit group as though it named the remix collapsed them onto
#: one identity, so deleting the remix suppressed the original.
_CREDIT_MARKERS = frozenset({"feat", "ft", "featuring", "with"})


def reads_as_version(value: str) -> bool:
    """Whether a free text value names a VERSION of the recording.

    Folded through :func:`fold`, which is the same folding the identity itself
    uses, so this asks its question in the one spelling both sides of the
    identity already agree on rather than inventing a second one.

    WHICH WAY IT FAILS IS MEASURED AND IS RECORDED ON :data:`VERSION_WORDS`. The
    short version: a designation using none of these words is not believed, so
    the row keeps its bare title and two versions of one recording can share one
    identity, which is over-suppression and the worse direction; a note that
    happens to contain one of these words IS believed, so the identity carries a
    parenthetical no provider spells and the tombstone suppresses nothing.
    """
    return bool(VERSION_WORDS.intersection(_WORD_SPLIT.split(fold(value))))


def fold(value: str) -> str:
    """One spelling of a free-text field, for identity purposes only.

    NFC first, then case, then spacing. The order does not change the result for
    any input this has been run against, and it is fixed anyway so that two
    implementations cannot produce two answers for one of the inputs where it
    would: composing after case-folding is not the same operation as case-folding
    after composing for every script.

    It is NOT a display transformation and nothing renders its output. A person
    is shown the payload, which keeps the original spelling.

    **IT IS FOR FREE TEXT AND IT IS NOT THE FOLDING FOR A STRUCTURED CODE.** It
    keeps punctuation, because punctuation is part of what a title says, and a
    caller comparing two spellings of an identifier whose punctuation is
    presentational wants :func:`fold_code` instead.
    """
    return _SPACING.sub(" ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


def fold_code(value: str) -> str:
    """One spelling of a STRUCTURED IDENTIFIER, for comparison only.

    **A FREE-TEXT FOLD READ ONE ISO 3901 CODE AS TWO RECORDINGS, AND THAT WEDGED
    THE QUEUE.** :func:`fold` is NFC, then case, then whitespace runs, and it
    keeps punctuation. An ISRC's punctuation is presentational: ISO 3901 defines
    the code as twelve alphanumeric characters and the hyphenated
    ``GB-AYA-15-00001`` is the DISPLAY FORM of the same code ``GBAYA1500001``.
    Compared under the free-text fold those are two strings, so two rows of ONE
    recording read as two recordings, ``stores.ambiguous_versions`` returned both
    content ids, and ``candidates.Category.AMBIGUOUS_VERSION`` is not in
    ``candidates.HANDLED``, so the watermark held at those rows forever with the
    pass never offering them and therefore never able to clear them. Nothing was
    deleted and nothing was suppressed, so the direction was safe; the cost was
    availability, which is the same "one row wedges the whole queue" failure
    ``run._settle_a_confirmed_absence`` exists to prevent.

    THREE DIFFERENCES FROM :func:`fold`, EACH FOR A MEASURED SPELLING.

    * Non-alphanumerics are REMOVED rather than collapsed, so the display form's
      hyphens, a typed space, and a non-breaking space all disappear instead of
      surviving as a separator the raw code does not have.
    * NFKC rather than NFC, so a fullwidth ``ＧBAYA1500001`` pasted out of a web
      page is the same code as its ASCII spelling. NFC leaves fullwidth forms
      alone and read that as a second recording.
    * Nothing is collapsed to empty and then compared as equal by accident: a
      value that folds to nothing is an ABSENT code to every caller here, and an
      absent code is read as agreement rather than as a collision.

    **WHAT IT DELIBERATELY DOES NOT DO IS TRANSLITERATE.** Characters outside
    ASCII that ARE alphanumeric survive as themselves, so a Cyrillic ``А`` typed
    for a Latin ``A`` stays a different code. Dropping it would silently merge two
    values that are genuinely different, and merging is the OVER-suppression
    direction: the collision guard would stop firing and a deletion would take out
    a version the person never deleted. Removing punctuation cannot do that,
    because no two well-formed codes differ only in punctuation.
    """
    return _NOT_A_CODE_CHARACTER.sub(
        "", unicodedata.normalize("NFKC", str(value)).casefold()
    )


def _already_carries(title: str, folded_version: str) -> bool:
    """Whether the title already names this version, AS A VERSION.

    **A PLAIN SUBSTRING TEST IS WHAT THIS REPLACES, AND IT WAS SILENTLY DROPPING
    VERSIONS OUT OF IDENTITIES.** ``folded_version in fold(title)`` is true
    whenever the version appears anywhere at all, so ``Live`` counted as already
    carried by ``Lively Up`` and ``Extended`` by ``Extended Play Track``. Two rows
    of one recording, one with the column empty and one with it filled in, then
    produced ONE identity, deleting either suppressed both, and that is the
    over-suppression direction this module's docstring calls the worse one.

    So the test is DELIMITED, and the delimiter is a bracket. A title carries its
    own mix name inside ``(...)`` or ``[...]`` and nowhere else, because that is
    the convention every provider and every rekordbox library actually spells, so
    a version is already carried when a bracketed group of the title NAMES it.
    ``Lively Up`` has no groups at all and ``Extended Play Track`` has none
    either, so both compose and both stay distinct from the bare title.

    THE MATCH INSIDE THE GROUP IS ITSELF DELIMITED, on word boundaries rather
    than on the whole group, and that is not fussiness. rekordbox's
    ``RemixerName`` is an association proxy into ``djmdArtist``, so it holds an
    ARTIST NAME: the row is ``Strobe (Michael Woods Remix)`` with ``Michael
    Woods`` in the column. Requiring the group to equal the version would compose
    that into ``Strobe (Michael Woods Remix) (Michael Woods)``, a spelling no
    provider will ever produce and therefore a tombstone that suppresses nothing.
    Requiring the group to CONTAIN the version at word boundaries answers yes,
    and still answers no for ``Live`` against a group reading ``Lively``.

    Lookarounds rather than ``\\b`` because a mix name may begin or end with a
    character that is not a word character, and ``\\b`` is defined against the
    character next to it in the PATTERN, so it silently means nothing there.

    **A FEATURED CREDIT GROUP IS NOT A VERSION GROUP, and reading it as one gave
    two different tracks one identity.** ``Fisher / Losing It (feat. Anna)`` with
    the remixer column empty and the same title with ``Anna`` in that column are
    the original and a remix of it. The bracket that carries the guest credit
    contains the remixer's name at word boundaries, so the version was judged
    already carried, nothing was composed, and both rows produced ``losing it
    (feat. anna)``: deleting the remix suppressed the original, which is the
    over-suppression direction. A group opening with a credit marker is skipped,
    so the remix composes and the two stay apart. It is skipped rather than
    stripped, because what is inside it is a performer either way and none of it
    names a version.
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
    """Whether a bracketed group names GUEST PERFORMERS rather than a version.

    Tested on the group's first word, because that is where the convention puts
    the marker and nowhere else: ``(feat. Anna)``, ``(ft. Anna)``,
    ``(with Anna)``. A marker anywhere else in the group is a word in a mix name,
    ``(Live with Strings)`` being the shape that would break under a containment
    test, so the head is the whole rule.
    """
    words = _WORD_SPLIT.split(fold(group).strip())
    return bool(words) and words[0] in _CREDIT_MARKERS


def remixer_title(title: str, remixer: str) -> str:
    """The title a PROVIDER spells, for a producer holding a bare REMIXER name.

    **THE RECORDER OWES THE CONSULTER THE EXACT STRING IT WILL BE HANDED, AND FOR
    THIS COLUMN IT WAS NEVER PAYING.** ``RemixerName`` is an association proxy
    over ``RemixerID`` into ``djmdArtist``, so it always holds an ARTIST NAME
    rather than a mix name: the row is ``Strobe`` by ``deadmau5`` with ``Michael
    Woods`` in the column. Composed as it stood, that produced the identity
    ``strobe (michael woods)``, and a provider spells the same version ``Strobe
    (Michael Woods Remix)``, so the consulter asked for ``strobe (michael woods
    remix)`` and missed. Every tombstone written from that column was
    unmatchable, which means every remix the user deleted was re-acquirable, and
    the remixer column is the normal case in a remix-heavy library rather than an
    edge. :func:`_already_carries` names this defect in its own docstring and
    closes it only for the branch where the title already carries the bracket.

    So the artist name is SPELLED as a designation before it is composed, and the
    two conventions one collection routinely holds then agree: ``Strobe`` with
    ``Michael Woods`` in the column and ``Strobe (Michael Woods Remix)`` with it
    filled in as well now produce ONE identity, where before they produced two.

    THE APPEND IS SKIPPED ONLY WHERE IT WOULD SAY ``Remix`` TWICE. Some libraries
    and some importers put a whole mix name in the column, and appending to
    ``Michael Woods Remix`` gives ``(Michael Woods Remix Remix)``, which is a
    second unmatchable spelling replacing the first.

    **TWO ROUNDS DECIDED THAT SKIP WITH A WORD LIST AND BOTH WERE WRONG,
    MEASURED.** Round five asked :func:`reads_as_version`, which answers "does a
    version word appear anywhere", so ``Radio Slave``, ``Dub Pistols``, ``Cut
    Chemist``, ``Mix Master Mike``, ``Club Sweat`` and ``Original Gee`` were all
    composed verbatim and every one of them missed. Round six asked whether the
    version word came LAST, which fixed those six and broke ``The Cut``, ``Da
    Dub``, ``Todd Terry Live`` and every other artist with a vocabulary word at
    the tail, while also missing every designation that does not put its version
    word last: ``Versión Extendida``, ``Live at Wembley``, ``Mixed by Someone``.
    Both were asking a vocabulary to classify a column that is an association
    proxy into ``djmdArtist``, which is to say a column the schema has already
    classified.

    :func:`already_spelled_as_a_remix` is asked instead. It consults no
    vocabulary: it asks whether the value's last word is the very word about to
    be appended, which is the only thing the skip ever existed to prevent. Its
    measurement over 65 values, the two error classes and why they are not
    equally bad are all on that function.

    **WHY THE VERBATIM BRANCH IS SAFE HERE AND WAS NOT BEFORE.** A branch that
    fires on ``The Cut`` composes ``(the cut)``, and ``Subtitle`` holding the
    designation ``The Cut`` composes ``(the cut)`` as well, so one identity
    stands for two versions and deleting either suppresses the other. That is
    over-suppression, reached through a rule meant to avoid the milder error.
    This branch fires only on a value already ending in ``Remix``, and a
    ``Subtitle`` holding that same string names that same version, so the rows it
    can converge are one version filed twice.

    A REMIXER THE TITLE ALREADY NAMES IS NOT COMPOSED AT ALL, and that test is on
    the BARE name rather than on the spelled one. ``Strobe (Michael Woods
    Extended Remix)`` carries ``Michael Woods`` and does not carry ``Michael
    Woods Remix``, so testing the spelled form would compose a second bracket
    onto a title that already says everything it needs to.
    """
    folded = fold(remixer)
    if not folded or _already_carries(title, folded):
        return title
    spelled = remixer if already_spelled_as_a_remix(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    return version_title(title, spelled)


def _as_a_bracketed_value(version: str) -> str:
    """A column's value as it may appear inside a bracket a provider would spell.

    Surrounding whitespace goes, interior whitespace runs collapse, and bracket
    characters become spaces. See :func:`version_title` for what each one closes.
    """
    return _SPACING.sub(" ", _BRACKET_CHARACTERS.sub(" ", str(version))).strip()


def version_title(title: str, version: str) -> str:
    """The title with the version in it, for a producer that holds the two apart.

    Both halves of the guard matter and each closes a real shape. The first half
    is load-bearing rather than decorative, which it was NOT while the second one
    was a plain substring test: ``fold("")`` is ``""`` and ``"" in anything`` is
    true, so the empty check could be deleted with nothing noticing. It cannot be
    now, because :func:`_already_carries` asks a bracketed question that an empty
    version answers no to, and deleting the check would compose ``Strobe ()``
    for every ordinary row in the library.

    AN EMPTY VERSION CHANGES NOTHING, so the ordinary row, which is most of them,
    produces exactly the identity it produced before this function existed.

    A VERSION ALREADY INSIDE THE TITLE IS NOT ADDED TWICE. rekordbox libraries
    are inconsistent about this: the same collection holds ``Strobe`` with
    ``Michael Woods`` in ``RemixerName`` and ``Strobe (Michael Woods Remix)``
    with the column filled in as well. Appending unconditionally would give those
    two rows two identities, so re-importing a track under the other convention
    would walk straight past its own tombstone. The containment test is done on
    the FOLDED forms, because that is the only spelling either side agrees on.

    The bracket shape is the one a provider uses, which is the whole point: the
    consulter never calls this, it simply passes the title it was handed, and the
    two meet only if the composed string is spelled the way titles are spelled in
    the wild.

    **THE VALUE IS TIDIED BEFORE IT GOES INSIDE THE BRACKET, AND UNTIL IT WAS,
    THE COLUMN'S OWN TYPING SURVIVED INTO THE IDENTITY.** :func:`fold` strips the
    ends of the WHOLE composed string and the closing bracket sits outside the
    value, so ``'Michael Woods Remix   '`` composed ``strobe (michael woods
    remix )`` and ``' Michael Woods Remix'`` composed ``strobe ( michael woods
    remix)``. Both match no provider spelling and neither matches the identity the
    same value produces without the spaces, so one trailing space in one rekordbox
    column is a version that cannot be suppressed and, worse, a second identity
    for a version that already has one. A value carrying its own brackets was the
    same defect with a different character: ``'Michael Woods (Remix)'`` composed
    ``Strobe (Michael Woods (Remix))``, and ``_BRACKETED`` is non-nesting by
    design, so nothing reads that as a version group either.

    Tidying is the ends and the brackets and NOTHING ELSE. The interior is the
    person's own text and this module does not get to rewrite it; the whitespace
    collapse that runs with it is the same collapse :func:`fold` already applies
    one step later, so it changes no identity that was not already broken.
    """
    tidied = _as_a_bracketed_value(version)
    folded_version = fold(tidied)
    if not folded_version or _already_carries(title, folded_version):
        return title
    return f"{title} ({tidied})" if title else tidied


def version_identity(*, artist: str, title: str) -> dict[str, str]:
    """The identity of one version of one recording.

    Both fields are always present, even when empty, because an identity whose
    KEY SET varies with the input is two identities wearing one name: a producer
    that omitted an empty artist would hash differently from one that supplied
    it, and the two would never match.

    An identity with nothing in either field is REFUSED. It would hash to a single
    value, so every unnamed candidate in the library would collide onto one
    suppression, and the collision would look exactly like the feature working:
    one deletion would suppress everything.
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

    ADDRESSED BY THE ROW AND THE PATH IT RECORDS, not by the resolved path. Two
    reasons, and both are about what must happen when something changes.

    The recorded path is part of the identity, so a row later re-pointed at a
    different file is a different candidate and is offered again. A decline says
    "leave THAT file alone", and inheriting it onto whatever the row points at
    next would be a decision nobody made.

    The RESOLVED path is not part of it, because resolution depends on the volume
    prefix map, which is configuration. A decline recorded before a remount would
    stop matching after one, and a person would be asked again about a file they
    had already answered for.

    **THE GUARD BELOW USED TO BE THE ``str(None)`` SHAPE THIS MODULE FIXED ONE
    FUNCTION AWAY.** It read ``if not str(content_id)``, and ``str(None)`` is
    ``'None'``, which is truthy, so a row with no identifier of its own did not
    refuse: it produced the identity ``{'content_id': 'None', ...}`` and that
    string went on to address the review item, the decline, and the membership
    test that decides whether a playlist still points at the file. Two such rows
    do not fully collide, because ``recorded`` disambiguates them, so what it
    produced was a WRONG key rather than a collapse; the guard existed to make
    the wrong key unreachable and did not.

    ``None`` is tested for BEFORE the string conversion, which is the whole
    correction, and the emptiness test then runs on the converted value so that
    ``0`` stays addressable: a numeric identifier is a legitimate identifier and
    ``not 0`` would refuse it.

    **AND THE EMPTINESS TEST IS ON THE STRIPPED VALUE, WHICH IS THE SAME DEFECT
    ONE STEP ALONG.** ``'   '`` is truthy, so a row whose identifier is nothing
    but spaces produced ``{'content_id': '   '}`` and that string went on to
    address the review item, the decline and the playlist membership test, in the
    same way ``'None'`` did. It is the wrong-key shape rather than a collapse,
    because ``recorded`` still separates two such rows, and a key nobody can type
    is a decision nobody can revoke. Stripping is only for the TEST: what is
    returned is the value as given, because the identifier belongs to the
    collection row and this module does not get to rewrite it.

    **AND ``False`` IS THE SAME DEFECT A THIRD TIME.** ``str(False)`` is
    ``'False'``, which is truthy and strips to itself, so a boolean in the
    identifier column addressed the review item, the decline and the playlist
    membership test as the literal string ``'False'``, exactly as ``None``
    addressed them as ``'None'``. It is tested for by TYPE rather than by
    truthiness, because ``not False`` is true and ``not True`` is not, so a
    falsiness test would refuse one boolean and accept the other. ``0`` and
    ``'0'`` are unaffected and stay addressable, which is why the type test is
    ``isinstance`` and not a comparison: ``0 == False`` in Python and comparing
    would take the legitimate numeric identifier down with the boolean.
    ``library._sequence_of`` already refuses booleans in its own column for the
    same reason. Reachability through the real collection reader is near zero,
    since ``_text`` returns strings; this is the guard being true rather than
    nearly true.
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
    """A one-line rendering of an identity, for a listing or a refusal message.

    Rendering is separate from the identity itself, and the separation is the
    same one a review item makes between its summary and its key: the text below
    may be rewritten freely, and rewriting it must never orphan a decision
    somebody already made.
    """
    artist = str(identity.get("artist") or "")
    title = str(identity.get("title") or "")
    if artist or title:
        return f"{artist} - {title}" if artist and title else (artist or title)
    return str(identity.get("recorded") or identity.get("content_id") or "")


__all__ = [
    "DECLINE_STORE_KEY",
    "KIND_REMOVED_FILE",
    "KIND_VERSION",
    "REMIX_DESIGNATION",
    "STORE_KEY",
    "VERSION_WORDS",
    "already_spelled_as_a_remix",
    "describe",
    "fold",
    "reads_as_version",
    "remixer_title",
    "removed_file_identity",
    "version_identity",
    "version_title",
]
