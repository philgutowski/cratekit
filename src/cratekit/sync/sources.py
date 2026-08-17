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
    """One increment source, and the profile module that switches it.

    ``module_id`` is None when the source is core. Playlists are core (feature
    row 3). Labels and favorites are modules, so a slim profile queues only
    playlists.
    """

    source_id: str
    module_id: str | None = None


SPECS: tuple[SourceSpec, ...] = (
    SourceSpec("favorites", module_id="favorites"),
    SourceSpec("labels", module_id="labels"),
    SourceSpec("playlists"),
)

#: Derived from SPECS, never listed again (P3).
DECLARED: tuple[str, ...] = tuple(spec.source_id for spec in SPECS)


def enabled(membership: profiles.Membership) -> tuple[str, ...]:
    """The sources this profile actually queues, in declared order."""
    return tuple(
        spec.source_id
        for spec in SPECS
        if spec.module_id is None or spec.module_id in membership.available
    )
