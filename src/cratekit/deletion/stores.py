"""Declines and tombstones, on the revocable decision stores U11 shipped.

R35 and R36 both use the word REVOCABLE, and it is the word that decides the
shape of this file. "A declined file is remembered and never offered again UNTIL
THE DECLINE IS REVOKED" and "tombstones are listable AND revocable" are two
sentences that a private ledger beside the deletion pass would satisfy exactly
halfway: it would remember, and there would be no way back. A one-way door in the
one part of the product that removes music is the worst place in the system for
one.

So both stores are :class:`cratekit.core.review.DecisionStore`, which already
holds every property this needs and had them reviewed hard: a record is addressed
by a content-derived identifier rather than by a display name, re-recording is
idempotent, revoking KEEPS the record with its revocation stamped on it so a
person can tell "never suppressed" from "suppressed and lifted", the read
recognizes the document positively field by field and refuses anything it cannot
recognize rather than reading it as empty, and the whole read-then-write cycle
runs under a sibling lock because the alternative loses records while reporting
success. None of that is re-implemented here and none of it should be.

**WHY TWO STORES AND NOT ONE.** A decline and a tombstone answer different
questions about different things and have different lifetimes. A decline is about
one library ROW and one file on this disk: leave that file where it is. A
tombstone is about a RECORDING that outlives the row, the file, and the library:
never acquire this version again. Folding them into one store would make revoking
a decline un-suppress an acquisition, which is not what anybody who clicked
"keep this file" asked for. The state inventory already declares them as two
entries for the same reason, so this module spends the difference rather than
paying for it.

Layer note: MODULES. Every store key and every kind comes from
``cratekit.core.tombstone``, which sits below both this and the acquisition
passes that consult the same records, so a recorder and a consulter cannot drift
into two spellings of one identity.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any, Callable, Mapping

from cratekit.core import config, review, tombstone
from cratekit.deletion import library
from cratekit.deletion.library import (
    VERSION_IS_A_DESIGNATION,
    VERSION_IS_AN_ARTIST,
    RemovedRow,
)


def declines(cfg: config.Config) -> review.DecisionStore:
    """R35's store: files a person looked at and decided to keep."""
    return review.DecisionStore(tombstone.DECLINE_STORE_KEY, cfg)


def tombstones(cfg: config.Config) -> review.DecisionStore:
    """R36's store: versions this library has deliberately stopped holding."""
    return review.DecisionStore(tombstone.STORE_KEY, cfg)


def row_identity(row: RemovedRow) -> dict[str, str]:
    return tombstone.removed_file_identity(content_id=row.content_id, recorded=row.recorded)


def version_of(row: RemovedRow) -> dict[str, str]:
    """This row's version identity, with the mix name folded into the title.

    THE COMPOSITION IS WHY THE IDENTITY IS ACTUALLY UNIQUE. rekordbox files a
    mix name in ``RemixerName`` or ``Subtitle`` as readily as inside ``Title``,
    so two different remixes of one recording reach here as two rows carrying one
    title. Handing those straight to ``version_identity`` gave them ONE identity,
    and deleting either reported the other suppressed and never re-acquired it.
    ``core.tombstone`` is where the composition rules live, below both this and
    the acquisition side, so a recorder and a consulter cannot compose
    differently.

    **HOW THE RECORDER AND THE CONSULTER AGREE, WHICH IS NOT BY BOTH COMPOSING.**
    :func:`suppressed_version` composes nothing, and it cannot: a provider
    candidate arrives as one title with the mix name already inside it and no
    second field to offer. So the agreement runs the other way. The RECORDER is
    obliged to produce exactly the string the consulter will be handed.

    **AND THAT OBLIGATION IS PAID DIFFERENTLY PER COLUMN, WHICH IS THE CORRECTION
    THIS ROUND MAKES.** It used to be paid one way, by composing only from a
    field that really is a version designation, which is what
    ``library._version_of`` decides for the ``Subtitle``. That is the right
    guard for a free text column and it was the wrong guard for the other one:
    ``RemixerName`` is an association proxy into ``djmdArtist`` and therefore
    always holds an ARTIST NAME, so believing it and composing it verbatim wrote
    ``strobe (michael woods)`` while every provider spells ``Strobe (Michael
    Woods Remix)``. The value was true, the belief was correct, and the SPELLING
    was one no consulter would ever ask about, so every tombstone written from
    the commonest version column in a remix-heavy library suppressed nothing.
    ``tombstone.remixer_title`` spells it before composing.
    """
    if row.version_kind == VERSION_IS_AN_ARTIST:
        title = tombstone.remixer_title(row.title, row.version)
    else:
        title = tombstone.version_title(row.title, row.version)
    return tombstone.version_identity(artist=row.artist, title=title)


#: The payload field carrying the composition rules a tombstone's identity was
#: written under. Named once, because the writer and the reader are two functions
#: in this file and a field spelled twice is a stamp that stops being read.
IDENTITY_SCHEME_FIELD = "identity_scheme"

#: Prefix on the stamp, so a value read out of a payload is recognisable as one
#: of these rather than as an arbitrary string somebody put in the field.
_SCHEME_PREFIX = "is1_"

class _SchemeProbe:
    """A collection row, shaped exactly as far as the version reader touches one.

    The columns are spelled the way rekordbox spells them because
    ``library._version_of`` reads them by those names. A column the reader starts
    reading that this does not carry answers empty through ``library._text``, so
    the probe degrades to a narrower measurement rather than raising, and the
    suite is where that is caught.
    """

    __slots__ = ("RemixerName", "Subtitle")

    def __init__(self, remixer: str, subtitle: str) -> None:
        self.RemixerName = remixer
        self.Subtitle = subtitle


#: The collection rows :func:`identity_scheme` reads and composes, as raw column
#: values rather than as a version somebody has already decided.
#:
#: **THEY ARE FROZEN AND THEY ARE NOT A TEST FIXTURE.** Each one exists to make a
#: branch observable in the stamp. Through the READER: an absent version column,
#: a ``RemixerName`` believed on sight, a ``Subtitle`` the vocabulary believes,
#: one it does not, and both columns filled at once, which is the only thing that
#: pins their order. Through the COMPOSER: a version the title already carries
#: bare, one it carries in round brackets and one in square, a value needing the
#: whitespace tidy, a value carrying its own brackets, a value that tidies away
#: to nothing, a featured-credit group, a version word inside a longer word, a
#: remixer needing the designation appended, one that already ends in it, one
#: whose last word is a vocabulary word, one the title already names, and the
#: case, spacing and composition-form limbs of the fold. An empty artist and an
#: empty title appear singly, because the identity refuses only when BOTH are
#: empty and each single-empty branch is reachable.
#:
#: EDITING THIS TUPLE CHANGES THE STAMP, AND THAT IS THE SAFE DIRECTION. A build
#: whose stamp differs from the one in a record treats that record as written
#: under other rules and recognises it by the row it names, which is a lookup and
#: cannot be wrong. A build whose stamp wrongly MATCHES is the failure, so the
#: bias is toward moving the stamp too often rather than too rarely.
_SCHEME_PROBES: tuple[tuple[str, str, str, str], ...] = (
    # artist, title, RemixerName, Subtitle
    ("deadmau5", "Strobe", "", ""),
    ("deadmau5", "Strobe", "", "Extended Mix"),
    ("deadmau5", "Strobe Extended Mix", "", "Extended Mix"),
    ("deadmau5", "Strobe (Extended Mix)", "", "Extended Mix"),
    ("deadmau5", "Strobe [Extended Mix]", "", "Extended Mix"),
    ("deadmau5", "Strobe", "", " Extended  Mix "),
    ("deadmau5", "Strobe", "", "[Extended Mix]"),
    ("deadmau5", "Strobe", "", "(Mix)"),
    ("deadmau5", "Strobe", "", "Anjunadeep"),
    ("deadmau5", "Strobe", "Michael Woods", "Extended Mix"),
    ("Fisher", "Losing It (feat. Anna)", "Anna", ""),
    ("Fisher", "Losing It (Live with Strings)", "", "Live"),
    ("Bob Marley", "Lively Up", "", "Live"),
    ("deadmau5", "Strobe", "Michael Woods", ""),
    ("deadmau5", "Strobe", "Michael Woods Remix", ""),
    ("deadmau5", "Strobe", "The Cut", ""),
    ("deadmau5", "Strobe", " Michael Woods ", ""),
    ("deadmau5", "Strobe", "[Michael Woods]", ""),
    ("deadmau5", "Strobe (Michael Woods Remix)", "Michael Woods", ""),
    ("DEADMAU5", "  Strobe   Mix  ", "", ""),
    ("deadmau5", "Ströbe", "", ""),
    ("", "Strobe", "", "Extended Mix"),
    ("deadmau5", "", "", "Extended Mix"),
)


def identity_scheme() -> str:
    """What THIS build turns a collection row into, as one comparable value.

    **IT IS A MEASUREMENT OF THE RULES, NOT A NUMBER SOMEBODY REMEMBERS TO
    BUMP.** A hand-set version constant is the same instrument as the frozen
    composers this replaced: correct on the day it is written and silently wrong
    the first time a helper below it changes and nobody thinks to touch it. This
    runs the frozen probes through the whole path from a collection row to an
    identity and digests what comes out, so the value moves when the OUTPUT
    moves, wherever in the call tree the change was made.

    **THE READING IS INSIDE IT AND NOT ONLY THE COMPOSING, WHICH IS THE SAME
    DEFECT ONE FILE OVER.** ``library._version_of`` decides which column is
    believed, and ``tombstone.VERSION_WORDS`` decides whether a ``Subtitle`` is a
    version at all. Change either and one rekordbox row starts producing a
    different identity with every composition function untouched, so a stamp
    taken over the composer alone would still match and the recogniser would
    still trust an identity that had moved. What was NOT believed is digested
    too, so the vocabulary is observable even on a row whose composed identity it
    does not change.

    IT IS COMPUTED ON DEMAND RATHER THAN AT IMPORT, which is what makes any of
    that true: a constant frozen at import is a snapshot of one process, and the
    question this answers is whether the build that wrote a record reads and
    composes the way this one does.

    **WHAT IT IS NOT.** It is not part of any identity, so it never reaches a
    hash a suppression is addressed by, and a build whose stamp differs
    suppresses and consults exactly what it did before. It only tells the
    recogniser in :func:`tombstone_predicate` which question to ask of a stored
    record.
    """
    digest = hashlib.sha256()
    for artist, title, remixer, subtitle in _SCHEME_PROBES:
        version, kind, unbelieved = library._version_of(_SchemeProbe(remixer, subtitle))
        composed = version_of(
            RemovedRow(
                content_id="probe",
                recorded="",
                sequence=0,
                size=None,
                artist=artist,
                title=title,
                version=version,
                version_kind=kind or VERSION_IS_A_DESIGNATION,
                version_unbelieved=unbelieved,
            )
        )
        digest.update(
            json.dumps(
                [composed, version, kind, unbelieved], sort_keys=True, ensure_ascii=False
            ).encode("utf-8")
        )
        digest.update(b"\x1e")
    return f"{_SCHEME_PREFIX}{digest.hexdigest()[:16]}"


def _row_coordinates(content_id: Any, recorded: Any) -> tuple[str, str] | None:
    """Which ROW a record names, or None where it names none.

    The row rather than the version, and raw rather than composed: this is the
    pair of values a tombstone's payload has carried since the first commit of
    this pass, taken from the collection row and written down untouched. Nothing
    in the composition vocabulary is consulted, so nothing in it can move this.

    ``recorded`` is composed to NFC because
    :func:`tombstone.removed_file_identity` already fixes that as the rule for
    this exact field, and two rules for one field is how the two come to
    disagree. Both sides of every comparison here run through this one function
    in one build, which is the whole difference from the composition case: there,
    one side was a string frozen on a disk and the other was live.
    """
    if content_id is None or isinstance(content_id, bool):
        return None
    named = str(content_id)
    if not named.strip():
        return None
    return (named, unicodedata.normalize("NFC", str(recorded if recorded is not None else "")))


def ambiguous_versions(rows: Any) -> frozenset[str]:
    """The rows whose version identity is shared with a row that is a DIFFERENT recording.

    **THE RESIDUAL FINDING
    "The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence"
    SAID THIS NEEDED "A SIGNAL NEITHER THE ROW NOR THE LIBRARY CARRIES TODAY",
    AND THE ROW ALREADY CARRIES IT.** The claim was that two rows landing
    on one identity are indistinguishable: the LEGITIMATE convergence,
    ``Strobe`` with ``Michael Woods`` in the remixer column against ``Strobe
    (Michael Woods Remix)`` with it filled in as well, is the same shape as the
    feared COLLISION, two different recordings whose designations the ``Subtitle``
    vocabulary did not believe, both keeping a bare title. The identity IS the
    claim that two rows are one version, so no test of the identity can tell them
    apart.

    ``RemovedRow.isrc`` is read from the ``ISRC`` column and already rides in
    every tombstone's payload, and it settles it. The legitimate convergence is
    ONE recording filed twice, so it carries one code. The collision is TWO
    recordings, so it carries two. That finding's stated reason for not building
    this,
    that the same shape flags an ordinary duplicate import, is what the code
    resolves rather than a reason to skip it: a duplicate import is one recording
    imported twice and carries the SAME code.

    **THE CODES ARE FOLDED BEFORE THEY ARE COMPARED.** An ISRC is
    case-insensitive by specification, so ``gbaya1500001`` and ``GBAYA1500001``
    are one code, and comparing the raw strings answered "two recordings" for one
    recording whose two rows were typed in different cases. The direction was
    safe, since refusing leaves both rows deletable-by-nobody rather than
    suppressing something, but a discriminator that fires on a difference in
    spelling is not discriminating on the thing it names.

    **AND THE FOLDING IS ``tombstone.fold_code``, NOT ``tombstone.fold``, WHICH
    IS A CORRECTION TO WHAT THIS DOCSTRING USED TO ARGUE.** It used to say that
    ``fold`` is the folding both halves of every identity in this package already
    agree on, so it is the one to use here rather than a second one invented
    locally. That is a good rule for a TITLE and it is the wrong rule for a CODE.
    ``fold`` deliberately keeps punctuation, because punctuation is part of what a
    title says, and ISO 3901 defines an ISRC as twelve alphanumeric characters
    whose hyphenated ``GB-AYA-15-00001`` is the DISPLAY FORM of the same code
    ``GBAYA1500001``. Under ``fold`` those are two strings, so the display form
    and the raw form of ONE code read as two recordings and this function returned
    both content ids.

    That is worse than the case defect it replaced, because
    ``candidates.Category.AMBIGUOUS_VERSION`` is not in ``candidates.HANDLED``:
    the watermark does not pass over such a row, the pass never offers it, and so
    nothing can ever clear it. Still nothing deleted and nothing suppressed, so
    still the safe direction, but the cost is availability and it is permanent.
    Reusing the shared folding was the general rule applied to the one value in
    this module that is not free text.

    IT IS INCONCLUSIVE WHERE A CODE IS ABSENT, AND SILENCE IS READ AS AGREEMENT.
    A convergence where one row has no code, or neither has one, is left
    deletable, because the identity's own claim is the default and an absent code
    is not evidence against it. What is refused is a convergence carrying two
    codes that are both present and different, which is a positive statement that
    the two rows are two recordings.

    THIS IS THE ONLY THING BOUNDING THE VOCABULARY'S WORSE ERROR DIRECTION. A
    ``Subtitle`` designation the closed list does not know leaves the row with a
    bare title, so two versions of one recording collide and deleting either
    suppresses the other, which costs the user a track they did not delete.
    Nothing local could see that before, because it is not visible in one row. It
    is visible in the one collection walk ``run.plan`` already holds.
    """
    grouped: dict[tuple[tuple[str, str], ...], list[RemovedRow]] = {}
    for row in rows:
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity collides with nothing
            continue
        grouped.setdefault(tuple(sorted(identity.items())), []).append(row)
    ambiguous: set[str] = set()
    for sharing in grouped.values():
        codes = {tombstone.fold_code(row.isrc or "") for row in sharing}
        codes.discard("")
        if len(codes) > 1:
            ambiguous.update(row.content_id for row in sharing)
    return frozenset(ambiguous)


def identifiable(row: RemovedRow) -> bool:
    """Whether a tombstone COULD be written for this row, asked before anything moves.

    R36 makes the tombstone part of the deletion rather than a consequence of it,
    so a deletion whose tombstone cannot be written is a deletion that must not
    happen. Asking here, at review time, is what keeps that from being discovered
    between the move and the record, which is the one window in this whole pass
    where a failure has already destroyed something.

    **BOTH IDENTITIES ARE ASKED FOR, NOT JUST THE VERSION'S.** A row also has to
    be addressable as a ROW, because that is what the review item a person
    answers, the decline that remembers their answer, and the suppression
    identifier are all derived from. A row carrying no identifier of its own has
    no version identity problem at all and would sail past a check that only
    asked about the version, then refuse at the moment it was offered, which is
    a refusal in the middle of a pass rather than a category on one row.
    """
    try:
        version_of(row)
        row_identity(row)
    except Exception:  # noqa: BLE001 - the refusal is the answer, not the exception
        return False
    return True


def decline_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """A predicate over the declines, built from ONE read of the store.

    Built as a closure over a snapshot rather than asking the store per row, and
    that is not only about the file reads: a store consulted per row could change
    underneath a single categorisation pass, so two rows in one report would have
    been judged against two different sets of declines.
    """
    held = frozenset(
        record.suppression_id for record in declines(cfg).suppressions()
    )

    def declined(row: RemovedRow) -> bool:
        return (
            review.suppression_id_for(
                tombstone.DECLINE_STORE_KEY,
                tombstone.KIND_REMOVED_FILE,
                row_identity(row),
            )
            in held
        )

    return declined


def tombstone_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """Whether a run has already RECORDED the deletion of this row's version.

    **THE EVIDENCE THAT TELLS A RESUMED DELETION FROM A FILE SOMEBODY MOVED.**
    ``candidates.GONE`` means "the file the row named is not there", and that
    sentence carries two entirely different situations. One is a previous run of
    this pass that trashed the file and recorded it, which is finished business
    and is what makes an interrupted run resume rather than re-offer. The other
    is a person who renamed the file in the Finder, which is not finished at all:
    nothing moved, nothing was recorded, and retiring the row throws away a
    deletion they had confirmed. Absence cannot tell those apart. The TOMBSTONE
    can, because R36 makes it part of the deletion rather than a consequence of
    it, so a deletion this product completed has one and nothing else does.

    Built as a closure over ONE read, which is ``decline_predicate``'s own
    argument and holds here for the same reason: a store consulted per row could
    change underneath one pass, so two rows in one report would be judged against
    two different sets of records.

    REVOKED RECORDS COUNT. The question is "did a run record this deletion", not
    "is this version suppressed today". Revoking a tombstone makes the version
    acquirable again and says nothing about whether the file was moved, and
    reading a revocation as "no deletion happened" would re-open the very row the
    person had already dealt with.

    **AND A RECORD AN EARLIER BUILD WROTE COUNTS TOO, WHICH IS ANSWERED BY
    READING THE STORE RATHER THAN BY REBUILDING THE PAST.** This question is
    about history, and four rounds tried to answer it by recomputing what a
    former build would have composed for this row. Every one of them was correct
    on the day it was written: the reconstruction is made of live functions, so
    it moves with the build, and when it moves in step with the current composer
    the two agree and the caller reports that there is no history to worry about.
    A frozen composer does not fix that, because a frozen composer calls
    ``fold``, ``_already_carries`` and ``already_spelled_as_a_remix`` and those
    are live. Freezing one node of a call tree does not freeze the tree.

    **SO THE ERA IS A STAMP IN THE RECORD AND THE MATCH IS A LOOKUP.**
    :func:`record_tombstone` writes :data:`IDENTITY_SCHEME_FIELD` beside the
    identity, naming the rules that composed it. A record carrying THIS build's
    stamp is matched on its identity, exactly as before. A record carrying any
    other stamp, or none at all, was composed by rules this build does not have
    and must not guess at, so it is matched on the ROW IT NAMES: the
    ``content_id`` and ``recorded`` its payload has carried, raw, since the first
    commit of this pass. That comparison consults no composition rule, so no
    change to any composition rule can break it, and it stays right for a build
    that has not been written yet.

    **AN UNSTAMPED RECORD IS THE MIGRATION PATH AND IT NEEDS NO MIGRATION.** A
    record written before the stamp existed cannot be carrying this build's
    stamp, so it falls to the row lookup by the same rule that catches a future
    era, and nothing rewrites anybody's file to make that true. A read that
    repairs is a read that can fail while a person is only asking a question.

    WHAT THE STAMP BUYS OVER MATCHING EVERY RECORD ON ITS ROW, stated because it
    is the only thing it decides. This build's own records keep being recognised
    by their VERSION, so a row whose version column was edited after its deletion
    was recorded is not read as already recorded, and the tombstone naming the
    version the row now claims still gets written. Widening the question for
    every record would retire that row against a record naming a version it no
    longer has, and the listing would never gain the second spelling.
    """
    scheme = identity_scheme()
    records = tombstones(cfg).suppressions(include_revoked=True)
    held = frozenset(record.suppression_id for record in records)
    rows_recorded_under_other_rules = frozenset(
        coordinates
        for record in records
        if record.kind == tombstone.KIND_VERSION
        and str(record.payload.get(IDENTITY_SCHEME_FIELD) or "") != scheme
        for coordinates in (
            _row_coordinates(record.payload.get("content_id"), record.payload.get("recorded")),
        )
        if coordinates is not None
    )

    def recorded(row: RemovedRow) -> bool:
        if _row_coordinates(row.content_id, row.recorded) in rows_recorded_under_other_rules:
            return True
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity has no tombstone
            # FALSE RATHER THAN TRUE, and the direction is the whole of it. This
            # answer retires a confirmed removal without moving anything, so
            # True on a row nobody can identify would throw away a deletion
            # somebody confirmed for a file they had merely renamed. False
            # re-offers it, which costs one question.
            return False
        return (
            review.suppression_id_for(tombstone.STORE_KEY, tombstone.KIND_VERSION, identity)
            in held
        )

    return recorded


def record_decline(
    cfg: config.Config, row: RemovedRow, *, actor: str, resolved: str | None = None
) -> review.Suppression:
    """Remember that a person said to keep this file (R35)."""
    store = declines(cfg)
    return store.record(
        kind=tombstone.KIND_REMOVED_FILE,
        identity=row_identity(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            "recorded": row.recorded,
            "resolved": resolved or "",
        },
        actor=actor,
    )


def revoke_decline(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a decline, so the file is offered again on the next run (R35)."""
    store = declines(cfg)
    return store.revoke(suppression_id, actor=actor)


def record_tombstone(
    cfg: config.Config, row: RemovedRow, *, actor: str, trashed_to: str | None = None
) -> review.Suppression:
    """Suppress this exact version from future acquisition (R36).

    The ISRC rides in the PAYLOAD and not in the identity. See
    ``core.tombstone``: an identity may only contain fields both the recorder and
    the consulter always have, and a provider candidate frequently has no code at
    all, so a code in the identity would make the suppression silently miss the
    very sweeps it exists to stop.

    **AND THE RULES THAT COMPOSED THE IDENTITY RIDE WITH IT.** A record on a
    disk outlives the build that wrote it, and every attempt to work out
    afterwards which rules composed it has been a recomputation that drifts. The
    record says so itself instead. See :func:`identity_scheme` for what the value
    measures and :func:`tombstone_predicate` for the one question it decides.
    """
    store = tombstones(cfg)
    return store.record(
        kind=tombstone.KIND_VERSION,
        identity=version_of(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            # RIDES BESIDE THE TITLE RATHER THAN INSIDE IT. It keeps the row's
            # own spelling of the mix name, uncomposed and unfolded, so somebody
            # auditing a suppression can see WHICH COLUMN VALUE the identity was
            # built out of, which the composed title cannot show and which is the
            # first thing to look at when a tombstone missed. That sentence was
            # written twice for two fields while ``summarize`` emitted neither,
            # which made it a claim about a surface that did not exist;
            # ``summarize`` emits both now and the claim is true of the shipped
            # listing rather than of the payload alone.
            "version": row.version,
            # AND THE VALUE THAT WAS NOT BELIEVED RIDES BESIDE IT. An empty
            # ``version`` reads identically for a row that never carried one and
            # for a row whose designation the closed vocabulary did not
            # recognise, and only the second is a defect. That second case is the
            # measured failure direction of the vocabulary and the one that costs
            # the user a track, so the audit trail that exists to answer "why did
            # this tombstone miss" may not be the one place it is invisible.
            "version_unbelieved": row.version_unbelieved,
            "isrc": row.isrc or "",
            "content_id": row.content_id,
            "recorded": row.recorded,
            # THE ERA THIS IDENTITY WAS COMPOSED IN, so no later build has to
            # guess. Written beside the row coordinates deliberately: the two
            # are what a build with different composition rules reads, one to
            # know that it must not trust the identity and the other to know
            # which row the record is about.
            IDENTITY_SCHEME_FIELD: identity_scheme(),
            # EMPTY WHERE THIS PASS MOVED NOTHING, which is the settled-absence
            # case, and ``summarize`` emits it for exactly that reason: a person
            # listing suppressions has to be able to tell a deletion this tool
            # performed from one it recorded on somebody else's behalf.
            "trashed_to": trashed_to or "",
        },
        actor=actor,
    )


def revoke_tombstone(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a tombstone, making that version acquirable again (R36)."""
    store = tombstones(cfg)
    return store.revoke(suppression_id, actor=actor)


def list_tombstones(
    cfg: config.Config, *, include_revoked: bool = False
) -> tuple[review.Suppression, ...]:
    """Every tombstone, which is the LISTABLE half R36 asks for.

    Revoked records are available on request rather than by default, because the
    ordinary question is "what is suppressed" and the auditing question is "what
    was ever suppressed". Dropping the revoked ones entirely would leave a person
    unable to tell a version nobody ever deleted from one somebody deleted and
    then changed their mind about.
    """
    store = tombstones(cfg)
    return store.suppressions(include_revoked=include_revoked)


def suppressed_version(cfg: config.Config, *, artist: str, title: str) -> bool:
    """Whether this library has deliberately stopped holding that version.

    THE DELETION SIDE'S OWN CONSULT, and the wording matters because it used to
    claim to be the call an ACQUISITION pass makes. It cannot be: this module
    lives in the deletion package, and ``core.tombstone``'s own docstring says an
    acquisition module must never import from here, precisely because deletion
    and acquisition are two toggleable entries in ``core.profiles`` and either
    one can be switched off while the other runs. A consulter behind a toggle the
    consulting side does not control is a consulter that is absent exactly when
    it is needed. So an acquisition pass asks its own store through
    ``core.tombstone``'s shared kind and identity, and this is what the deletion
    pass and its tests ask when they want the same question answered from here.

    R36's requirement to REPORT a suppression rather than omitting the candidate
    silently belongs to whichever caller is filtering; what this owes is a
    truthful answer, including a refusal when the store cannot be read.
    """
    store = tombstones(cfg)
    return store.suppresses(
        tombstone.KIND_VERSION, tombstone.version_identity(artist=artist, title=title)
    )


def summarize(record: review.Suppression) -> Mapping[str, Any]:
    """One suppression projected for a listing or a structured payload.

    **IT COULD NOT TELL A DELETION THIS TOOL PERFORMED FROM ONE IT ASSERTED, AND
    IT IS THE ONLY SURFACE THERE IS.** ``run._settle_a_confirmed_absence`` writes
    a tombstone with ``trashed_to`` EMPTY, on purpose: the row was confirmed, the
    collection no longer holds it, and the file was not at the recorded path, so
    the deletion happened by somebody's hand rather than by this pass's. That is
    a materially different record from one written beside a real move into the
    Trash, and this projection omitted the one field that says which. The log
    line naming the identifier scrolls away; the listing is what a person has
    weeks later. So ``trashed_to`` is emitted, empty string and all, and an empty
    value is the statement that nothing was moved.

    **``version`` IS EMITTED FOR A DEFECT THIS ROUND MADE TWICE IN TWO LINES.**
    ``record_tombstone`` corrected a claim that the ISRC payload lets a person
    tell two same-titled versions apart in a listing, because this projection did
    not emit it, and then wrote the identical claim for ``version`` two lines
    later. Rather than correct the sentence again, the projection now emits what
    the sentences say it does: the row's own uncomposed spelling of the mix name,
    the value the vocabulary did NOT believe, and the code. Those four are the
    whole answer to "why did this tombstone miss", which is the only question
    anybody brings to this listing that the identity line cannot already answer.
    """
    return {
        "id": record.suppression_id,
        "kind": record.kind,
        "identity": tombstone.describe(record.identity or {}),
        "artist": record.payload.get("artist", ""),
        "title": record.payload.get("title", ""),
        "version": record.payload.get("version", ""),
        "version_unbelieved": record.payload.get("version_unbelieved", ""),
        "isrc": record.payload.get("isrc", ""),
        # EMPTY MEANS AN ERA BEFORE THE STAMP EXISTED, which is a fact about the
        # record and not a missing field. It is emitted because "why did this
        # tombstone miss" is the only question this listing exists to answer that
        # the identity line cannot, and "it was composed by rules this build does
        # not have" is one of the answers.
        IDENTITY_SCHEME_FIELD: record.payload.get(IDENTITY_SCHEME_FIELD, ""),
        # EMPTY MEANS THIS PASS MOVED NOTHING. Not absent, not omitted: a key
        # that disappears when the value is empty is a key a reader cannot tell
        # from one the build never wrote.
        "trashed_to": record.payload.get("trashed_to", ""),
        "recorded": record.recorded,
        "actor": record.actor,
        "revoked": record.revoked,
    }


__all__ = [
    "IDENTITY_SCHEME_FIELD",
    "ambiguous_versions",
    "decline_predicate",
    "declines",
    "identifiable",
    "identity_scheme",
    "list_tombstones",
    "record_decline",
    "record_tombstone",
    "revoke_decline",
    "revoke_tombstone",
    "row_identity",
    "summarize",
    "suppressed_version",
    "tombstone_predicate",
    "tombstones",
    "version_of",
]
