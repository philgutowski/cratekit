"""The R25 sources, keyed by stable identifier, never by display name (D5).

A new source appends a spec here; ``enabled`` derives the queued set from the
active profile rather than a second list (P3).
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import profiles


@dataclass(frozen=True, slots=True)
class SourceSpec:
    """One increment source, the profile module that switches it, and its worker.

    ``module_id`` is None for a core source (playlists), so a slim profile
    enables only playlists.

    ``handler_key`` is the key the source's own verb queues under, which
    ``crate sync all`` reuses; None (no worker, or guided) is reported as not
    built rather than queued as work nothing runs (R-203). Keys are pinned
    against the registry in ``tests/test_sync_all.py``, which this layer may
    not import (KTD23).

    ``inbound_key`` is the key of a source's read only half (U74), queued
    whatever a write confirmation answers since a read needs no consent.

    ``no_cursor`` says why nothing records this source's watermark (R-263), so
    ``watermarks.status_rows`` reports "records none" rather than "never ran".

    ``guided_by`` names the verb that takes this source instead of
    ``crate sync all`` (U109). The composer plans, calls and queues nothing for
    it, its report names that verb, and it declares no ``handler_key``.
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
        # THE HEARTS LISTING (U74), resolved by the intake worker.
        inbound_key="intake.playlist",
        # NEITHER WORKER RECORDS A CURSOR, so a missing record says nothing
        # about whether a favorites sync ran.
        no_cursor="no favorites worker records a cursor, so a completed sync "
        "leaves nothing to report here",
    ),
    SourceSpec(
        "labels",
        module_id="labels",
        # GUIDED, NOT COMPOSED (U109). A routine sweep of every label flooded
        # the review queue, so labels are taken only by ``crate label sync``.
        guided_by="label.sync",
        # NO CURSOR HERE; ``crate label sync`` keeps its own per label marker.
        no_cursor="label releases are taken by crate label sync, which keeps "
        "its own marker per label of the releases it has asked about rather "
        "than a cursor here",
    ),
    # NO WORKER OF ITS OWN (U64); the intake worker runs each new playlist.
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
