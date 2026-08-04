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

#: The words that make a value a VERSION DESIGNATION rather than a note about the
#: track. A closed, explicit list rather than a shape test, because "does this
#: read as a mix name" has no syntax to test: ``Extended Mix`` and ``Anjunadeep``
#: are the same shape and only the vocabulary tells them apart.
#:
#: **IT LIVES HERE, BELOW BOTH READERS, FOR THE REASON THE STORE KEY DOES.** It
#: was private to ``deletion.library``, where it answered one question: is this
#: ``Subtitle`` a version. It answers a second one now, in :func:`remixer_title`,
#: which is about SPELLING rather than belief, and a vocabulary with two callers
#: in two packages is the shape this module exists to prevent.
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
    """
    return _SPACING.sub(" ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


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

    A VALUE THAT ALREADY READS AS A DESIGNATION IS LEFT ALONE. Some libraries and
    some importers put a whole mix name in the column, and appending to that
    gives ``(Michael Woods Remix Remix)``, which is a second unmatchable spelling
    replacing the first. That is the one place :func:`reads_as_version` is asked
    about this column, and it is asked about SPELLING rather than about belief: a
    non-empty remixer is a version either way, and all this decides is how it is
    written down.

    A REMIXER THE TITLE ALREADY NAMES IS NOT COMPOSED AT ALL, and that test is on
    the BARE name rather than on the spelled one. ``Strobe (Michael Woods
    Extended Remix)`` carries ``Michael Woods`` and does not carry ``Michael
    Woods Remix``, so testing the spelled form would compose a second bracket
    onto a title that already says everything it needs to.
    """
    folded = fold(remixer)
    if not folded or _already_carries(title, folded):
        return title
    spelled = remixer if reads_as_version(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    return version_title(title, spelled)


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
    """
    folded_version = fold(version)
    if not folded_version or _already_carries(title, folded_version):
        return title
    return f"{title} ({version})" if title else version


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
    """
    if not str(content_id):
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
    "describe",
    "fold",
    "reads_as_version",
    "remixer_title",
    "removed_file_identity",
    "version_identity",
    "version_title",
]
