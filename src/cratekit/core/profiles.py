"""Profiles: named presets of module membership, and nothing else (D6).

A profile carries no other setting, so changing it never changes what the user
did not ask about. An explicit per-module toggle overrides the profile, decided
in ``resolve`` alone. Changing a profile touches membership and nothing else,
which ``apply`` makes true by construction. Library adoption is not a module and
stays available in every profile (R5).

Pure: reads no configuration and imports nothing from Cratekit.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from dataclasses import dataclass

#: Every toggleable feature module, one per Feature Inventory Module row, named
#: like its extras group where it has one (KTD7). A module missing here cannot
#: be toggled or left out of slim, so it silently behaves as core.
MODULES: tuple[str, ...] = (
    "analysis",
    "vocals",
    "favorites",
    "labels",
    "deletion",
    "web",
    "desktop",
    # U5: each name below gates one or more Module rows (R5);
    # tests/test_cli_contract.py asserts the correspondence both ways.
    "identify",  # rows 1, 2, 5: recognition and tracklist intake
    "repair",  # row 17: filename and path repair
    "duplicates",  # row 15: the review-gated duplicate audit
    "reports",  # row 20 and the read-only library reports
    "export",  # row 36: playlist export to a streaming service
    "setbuilder",  # row 29
    "mastering",  # row 30: set recording mastering
    "backup",  # row 31: library backup, which feeds the backup-age warning
    "skills",  # row 33: the operator skill layer

    # setbuilder, mastering and backup need an external binary, not a Python
    # dependency, so they have no extras group; doctor reports the binary (U35).
)

#: Modules whose heavy dependencies live behind an extras group. Hand kept,
#: since reading packaging metadata is I/O; ``tests/test_config.py`` asserts it
#: matches the declared extras.
EXTRAS_BACKED: frozenset[str] = frozenset({"analysis", "vocals", "web", "desktop"})

#: Capabilities no profile may switch off (R5).
ALWAYS_AVAILABLE: frozenset[str] = frozenset({"adoption"})

#: The presets. ``custom`` is the empty preset, so every module's state comes
#: from its explicit toggle with no special case in the resolver.
PROFILES: Mapping[str, frozenset[str]] = {
    "slim": frozenset(),
    "full": frozenset(MODULES),
    "custom": frozenset(),
}

PROFILE_NAMES: tuple[str, ...] = tuple(PROFILES)


class UnknownProfile(ValueError):
    """A profile name that is not one of the presets."""


class UnknownModule(ValueError):
    """A toggle naming something that is not a module."""


@dataclass(frozen=True, slots=True)
class Membership:
    """The resolved membership, keeping which modules a toggle overrode.

    ``overridden`` lets the CLI explain why switching profiles changed nothing.
    """

    profile: str
    modules: frozenset[str]
    overridden: frozenset[str]

    @property
    def available(self) -> frozenset[str]:
        """Everything this install can do: enabled modules plus what is always on."""
        return self.modules | ALWAYS_AVAILABLE


def resolve(profile: str, explicit: Mapping[str, bool] | None = None) -> Membership:
    """Apply the profile preset, then the explicit toggles, which win. Pure.

    ``explicit`` must carry only what the config file actually set: a fully
    defaulted mapping would turn every module explicitly off and the profile
    would never apply.
    """
    if profile not in PROFILES:
        raise UnknownProfile(
            f"{profile!r} is not a profile. Known profiles: "
            f"{', '.join(PROFILE_NAMES)}."
        )
    toggles = dict(explicit or {})
    unknown = sorted(set(toggles) - set(MODULES))
    if unknown:
        raise UnknownModule(
            f"not modules: {', '.join(unknown)}. Known modules: "
            f"{', '.join(MODULES)}."
        )

    enabled = set(PROFILES[profile])
    overridden: set[str] = set()
    for name, wanted in toggles.items():
        if wanted != (name in enabled):
            overridden.add(name)
        if wanted:
            enabled.add(name)
        else:
            enabled.discard(name)

    return Membership(
        profile=profile,
        modules=frozenset(enabled),
        overridden=frozenset(overridden),
    )


def apply(data: Mapping, profile: str) -> dict:
    """Return a deep copy of raw config data with the profile changed and nothing else.

    Works on the raw mapping because a typed config would re-serialize every
    field and write drifted defaults into the user's file. Explicit toggles are
    kept, since switching a preset does not reset the user's own decisions. The
    copy is deep so a later edit to a nested table cannot rewrite the input.
    """
    if profile not in PROFILES:
        raise UnknownProfile(
            f"{profile!r} is not a profile. Known profiles: "
            f"{', '.join(PROFILE_NAMES)}."
        )
    out = copy.deepcopy(dict(data))
    out["profile"] = {**dict(out.get("profile") or {}), "name": profile}
    return out


def install_command(module: str) -> str | None:
    """The extras group that carries ``module``'s heavy dependencies, or None.

    Returns the extras name, not a command line: the CLI renders the command
    (R5, D2). None means the module has no heavy dependency, not a failure.
    """
    if module not in MODULES:
        raise UnknownModule(f"{module!r} is not a module. Known: {', '.join(MODULES)}.")
    return module if module in EXTRAS_BACKED else None


__all__ = [
    "ALWAYS_AVAILABLE",
    "EXTRAS_BACKED",
    "MODULES",
    "PROFILES",
    "PROFILE_NAMES",
    "Membership",
    "UnknownModule",
    "UnknownProfile",
    "apply",
    "install_command",
    "resolve",
]
