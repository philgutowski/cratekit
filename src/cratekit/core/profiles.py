"""Profiles: named presets of module membership, and nothing else.

A profile is the answer to one question, asked once at setup: which feature
modules should be on. It is not a bundle of settings, not a personality, and not
a place to hide a default that belongs in the config schema. Every time a
"profile" in a piece of software starts carrying unrelated values, changing the
profile starts changing things the user did not ask about, and the only safe
move becomes never changing it.

So the contract here is narrow on purpose (D6):

1. A profile is a named preset of module membership.
2. An explicit per-module toggle OVERRIDES the profile. The precedence is stated
   here, in one function, not left to emerge from whichever code path ran last.
3. Changing a profile touches module membership and nothing else. That is this
   unit's own test scenario, and the module is shaped so that it is true by
   construction: ``apply`` returns a copy with two keys replaced and every other
   key carried through untouched.
4. Library adoption stays available in EVERY profile, including the slimmest
   one (R5). It is not a module and has no toggle, because a user who installed
   the slim profile is exactly the user most likely to need to adopt an existing
   library, and a toggle they have to find first is a toggle that blocks them.

This module reads no configuration and imports nothing from Cratekit. It takes
values and returns values, which is what lets one process resolve two different
profiles without reloading anything.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from dataclasses import dataclass

#: Every toggleable feature module, named one-to-one with the extras groups that
#: carry its heavy dependencies (KTD7). A module with no heavy dependency has no
#: extras group, which is why this list is longer than the extras table; the
#: reverse must never be true, and ``tests/test_config.py`` asserts it.
#:
#: The list tracks the Feature Inventory's Module rows. A row that ships as a
#: module and is MISSING here is not merely undocumented: ``resolve`` raises
#: ``UnknownModule`` for any toggle it does not recognise, so the user cannot
#: turn that feature off, and ``PROFILES["full"]`` is derived from this tuple, so
#: the slim profile cannot exclude it either. In other words an omission here
#: makes a module row behave like a core row, silently.
MODULES: tuple[str, ...] = (
    "analysis",
    "vocals",
    "favorites",
    "labels",
    "deletion",
    "web",
    "desktop",
    # The three standalone utility rows. They carry no heavy dependency of their
    # own, so none of them appears in EXTRAS_BACKED: what they need is an
    # external BINARY, which pip cannot install and an extras group therefore
    # cannot promise. That gap is doctor's to report, not packaging's.
    "setbuilder",
    "mastering",
    "backup",
)

#: Modules whose dependencies are heavy enough to live behind an extras group.
#: Kept beside ``MODULES`` rather than derived from packaging metadata at runtime,
#: because resolving installed metadata is I/O and this layer does none.
#: ``tests/test_config.py`` asserts this set matches the extras actually declared,
#: so the two cannot drift apart the way a hand-mirrored list normally does.
EXTRAS_BACKED: frozenset[str] = frozenset({"analysis", "vocals", "web", "desktop"})

#: Capabilities no profile may switch off. R5 names library adoption explicitly:
#: "Module rows are opt-in, except library adoption, which stays available on
#: demand in every profile."
ALWAYS_AVAILABLE: frozenset[str] = frozenset({"adoption"})

#: The presets. ``custom`` is the empty preset rather than a special case in the
#: resolver: under ``custom`` every module's state comes from its explicit
#: toggle, which is exactly what "the empty preset plus overrides" already means.
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
    """The resolved answer, with the reasoning kept rather than discarded.

    ``overridden`` exists so the CLI can tell a user "analysis is on because you
    turned it on, not because your profile says so". Without it, a user who
    switches profiles and sees no change has no way to discover that their own
    old toggle is the reason.
    """

    profile: str
    modules: frozenset[str]
    overridden: frozenset[str]

    @property
    def available(self) -> frozenset[str]:
        """Everything this install can do: enabled modules plus what is always on."""
        return self.modules | ALWAYS_AVAILABLE


def resolve(profile: str, explicit: Mapping[str, bool] | None = None) -> Membership:
    """Apply the profile preset, then the explicit toggles. Pure.

    Precedence, stated once: **the explicit toggle wins.** A module absent from
    ``explicit`` takes the profile's answer. A module present takes its own,
    whether that is on or off, so a user can subtract from ``full`` as well as
    add to ``slim``.

    This is why ``explicit`` must carry only what the config file actually set.
    A fully defaulted mapping would make every module "explicitly off", the
    profile would never apply to anything, and choosing a profile would silently
    do nothing.
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
    """Return a copy of raw config data with the profile changed and nothing else.

    "Nothing else" is the point, and it is why this works on the RAW mapping
    rather than on a typed config: rebuilding a typed object would re-serialize
    every field, and any default that had drifted between versions would be
    silently rewritten into the user's file as though they had chosen it.

    Explicit module toggles are DELIBERATELY preserved. Switching profiles is a
    change to the preset, not a reset of the user's own decisions; a user who
    turned one module off and then moved from slim to full still means it off.
    Clearing overrides is a separate, explicitly named action.

    The copy is DEEP. A shallow one hands back the caller's own nested tables, so
    "changing a profile touches module membership and nothing else" would be true
    of the returned document and false of the object the caller then edits: a
    later write to ``result["library"]`` would silently rewrite the input too.
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

    Returns the extras NAME, not a command line. R5 requires that a module
    enabled without its extras fails with the exact command that fixes it, and
    rendering that command is the CLI's job: this layer must not contain the text
    a user types (D2). Modules with no heavy dependency return None, which is not
    a failure, it is the answer.
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
