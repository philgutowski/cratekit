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

from typing import Any, Callable, Mapping

from cratekit.core import config, review, tombstone
from cratekit.deletion.library import RemovedRow


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
    ``tombstone.version_title`` is where the rule lives, below both this and the
    acquisition side, so a recorder and a consulter cannot compose differently.

    **HOW THE RECORDER AND THE CONSULTER AGREE, WHICH IS NOT BY BOTH COMPOSING.**
    :func:`suppressed_version` composes nothing, and it cannot: a provider
    candidate arrives as one title with the mix name already inside it and no
    second field to offer. So the agreement runs the other way. The RECORDER is
    obliged to produce exactly the string the consulter will be handed, and it
    keeps that obligation by composing only from a field that really is a version
    designation, which ``library._version_of`` is what decides. Composing from a
    ``Subtitle`` holding a label wrote the identity ``atlas (anjunadeep)`` for a
    track a provider spells ``Atlas``, so the tombstone was written, was
    listable, and answered NOT SUPPRESSED to the only question ever asked of it.
    """
    return tombstone.version_identity(
        artist=row.artist, title=tombstone.version_title(row.title, row.version)
    )


def identifiable(row: RemovedRow) -> bool:
    """Whether a tombstone COULD be written for this row, asked before anything moves.

    R36 makes the tombstone part of the deletion rather than a consequence of it,
    so a deletion whose tombstone cannot be written is a deletion that must not
    happen. Asking here, at review time, is what keeps that from being discovered
    between the move and the record, which is the one window in this whole pass
    where a failure has already destroyed something.
    """
    try:
        version_of(row)
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
    """
    store = tombstones(cfg)
    return store.record(
        kind=tombstone.KIND_VERSION,
        identity=version_of(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            # RIDES BESIDE THE TITLE RATHER THAN INSIDE IT, and the claim made
            # here used to be that a person reading a LISTING tells two
            # same-titled versions apart by it. They do not: ``summarize`` is the
            # only projection any surface renders and it does not emit this, and
            # what distinguishes the two rows there is the composed identity line.
            # What this is actually for is the record itself. It keeps the row's
            # own spelling of the mix name, uncomposed and unfolded, so somebody
            # auditing a suppression can see WHICH COLUMN VALUE the identity was
            # built out of, which is the one thing the composed title cannot show
            # and the first thing to look at when a tombstone missed.
            "version": row.version,
            "isrc": row.isrc or "",
            "content_id": row.content_id,
            "recorded": row.recorded,
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
    """One suppression projected for a listing or a structured payload."""
    return {
        "id": record.suppression_id,
        "kind": record.kind,
        "identity": tombstone.describe(record.identity or {}),
        "artist": record.payload.get("artist", ""),
        "title": record.payload.get("title", ""),
        "recorded": record.recorded,
        "actor": record.actor,
        "revoked": record.revoked,
    }


__all__ = [
    "decline_predicate",
    "declines",
    "identifiable",
    "list_tombstones",
    "record_decline",
    "record_tombstone",
    "revoke_decline",
    "revoke_tombstone",
    "row_identity",
    "summarize",
    "suppressed_version",
    "tombstones",
    "version_of",
]
