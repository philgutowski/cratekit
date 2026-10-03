"""The three R25 sources, keyed by stable identifier, never by display name.

D5 forbids a persisted record keyed on a playlist title. The same rule applies
to the source list itself: ``labels``, ``favorites``, and ``playlists`` are
identifiers. A later unit that adds a source appends a spec here, and
``enabled`` derives the queued set from the active profile rather than from a
second hand list (P3).
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import profiles


@dataclass(frozen=True, slots=True)
class SourceSpec:
    """One increment source, the profile module that switches it, and its worker.

    ``module_id`` is None when the source is core. Playlists are core (feature
    row 3). Labels and favorites are modules, so a slim profile enables only
    playlists.

    ``handler_key`` is the key the source's OWN verb queues under, and None when
    no worker exists for the source yet or when the source is guided (below).
    ``crate sync all`` queues each source
    under this key and never under its own, so a source with None is reported as
    not built rather than queued as work nothing runs (R-203). The keys are
    pinned against the registry in ``tests/test_sync_all.py``, since this layer
    may not import it (KTD23).

    ``inbound_key`` is the key a source's READ ONLY half queues under, when the
    source has one (U74). Favourites writes hearts to the account behind a
    confirmation and also reads the account's hearts into the library; the read
    needs no consent, so ``crate sync all`` queues it whatever the confirmation's
    answer. It is a field of the source rather than a source of its own, because
    it is switched by the same module and ``PLANNERS`` is pinned to ``SPECS``.

    ``no_cursor`` is why nothing records this source's watermark, and None when
    something does (R-263). A missing record then means two different facts:
    "never completed cleanly" for a source that records one, and "records none"
    for a source that does not. ``watermarks.status_rows`` reports the second
    as its own state rather than telling a person a clean sweep never ran.

    ``guided_by`` is the registry name of the verb that takes this source
    INSTEAD of ``crate sync all``, and None for a source the composer runs
    (U109). Such a source is still declared, so ``crate sync status`` still
    reports it, but the composer plans nothing for it, calls no provider for
    it and queues nothing, and its report names that verb as the way in. A
    guided source declares no ``handler_key``, because nothing ``sync all``
    queues is its work. The name is pinned against the registry in
    ``tests/test_sync_all.py`` beside the handler keys.
    """

    source_id: str
    module_id: str | None = None
    handler_key: str | None = None
    inbound_key: str | None = None
    no_cursor: str | None = None
    guided_by: str | None = None

    def command(self) -> str | None:
        """The command that takes a guided source, as a person types it."""
        if self.guided_by is None:
            return None
        return "crate " + self.guided_by.replace(".", " ")


SPECS: tuple[SourceSpec, ...] = (
    SourceSpec(
        "favorites",
        module_id="favorites",
        handler_key="sync.favorites",
        # THE HEARTS LISTING (U74), queued as ``crate intake playlist favorites``
        # queues it, so the intake worker resolves each heart.
        inbound_key="intake.playlist",
        # NEITHER WORKER RECORDS A CURSOR, measured by grep 2026-09-20: the
        # only writers of this document are ``run.increment``, which no
        # favorites path calls, and the playlists sweep. A missing record is
        # therefore no evidence about whether a favorites sync ran.
        no_cursor="no favorites worker records a cursor, so a completed sync "
        "leaves nothing to report here",
    ),
    SourceSpec(
        "labels",
        module_id="labels",
        # GUIDED, NOT COMPOSED (U109). A routine sync swept every favourite
        # label whether the author wanted that today or not, and the sweep's
        # offers grew the review queue to thousands of back catalogue releases.
        # Label releases are now taken only when ``crate label sync`` asks,
        # label by label, so ``sync all`` names that verb and touches nothing.
        guided_by="label.sync",
        # NO CURSOR HERE, still. ``crate label sync`` keeps its own per label
        # marker of the releases it has asked about, and this document is not
        # it.
        no_cursor="label releases are taken by crate label sync, which keeps "
        "its own marker per label of the releases it has asked about rather "
        "than a cursor here",
    ),
    # NO WORKER OF ITS OWN (U64). Each new account playlist is queued as the
    # job ``crate intake playlist`` queues, so the intake worker runs it.
    SourceSpec("playlists", handler_key="intake.playlist"),
)

#: Derived from SPECS, never listed again (P3).
DECLARED: tuple[str, ...] = tuple(spec.source_id for spec in SPECS)


def enabled_specs(membership: profiles.Membership) -> tuple[SourceSpec, ...]:
    """The sources this profile switches on, in declared order."""
    return tuple(
        spec
        for spec in SPECS
        if spec.module_id is None or spec.module_id in membership.available
    )


def enabled(membership: profiles.Membership) -> tuple[str, ...]:
    """The identifiers of the sources this profile switches on, in declared order."""
    return tuple(spec.source_id for spec in enabled_specs(membership))
