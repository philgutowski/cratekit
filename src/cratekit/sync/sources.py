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
    no worker exists for the source yet. ``crate sync all`` queues each source
    under this key and never under its own, so a source with None is reported as
    not built rather than queued as work nothing runs (R-203). The keys are
    pinned against the registry in ``tests/test_sync_all.py``, since this layer
    may not import it (KTD23).
    """

    source_id: str
    module_id: str | None = None
    handler_key: str | None = None


SPECS: tuple[SourceSpec, ...] = (
    SourceSpec("favorites", module_id="favorites", handler_key="sync.favorites"),
    SourceSpec("labels", module_id="labels", handler_key="sync.labels"),
    # NO WORKER AND NO LISTING. Playlists ride the increment engine once a
    # listing exists, and until then ``sync all`` names them as not built.
    SourceSpec("playlists"),
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
