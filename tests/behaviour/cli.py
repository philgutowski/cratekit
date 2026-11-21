"""The command shell's scenarios: the help of every registered verb (U297).

Generated from the registry, so a verb added later is captured without an
edit here: the top level screen, every group's and every verb's, as an
unconfigured machine shows them, which is the full preset.
"""

from __future__ import annotations

from cratekit.cli import registry
from cratekit.core import profiles


def help_paths() -> list[tuple[str, ...]]:
    """The top level, then every group and every verb the full preset lists, in order."""
    membership = profiles.resolve("full")
    found: set[tuple[str, ...]] = {()}
    for entry in registry.landed_entries():
        if entry.available_to(membership):
            for depth in range(1, len(entry.path) + 1):
                found.add(entry.path[:depth])
    return sorted(found)


def test_help_of_every_verb(stage):
    paths = help_paths()
    assert len(paths) > 100, "the registry lists far fewer verbs than it holds"
    for path in paths:
        ran = stage.crate(*path, "--help")
        assert ran.code == 0, (path, ran.stderr)
        assert ran.stdout.startswith("usage: crate"), (path, ran.stdout[:80])
