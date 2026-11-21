"""The command shell's scenarios: every verb's help, and a config no verb can use.

The help is generated from the registry, so a verb added later is captured
without an edit here: the top level screen, every group's and every verb's, as
an unconfigured machine shows them, which is the full preset (U297).

The second scenario runs one verb after another on a machine with no
configuration, and then on one whose configuration file is not a
configuration. Each of these verbs loads the configuration before anything
else and takes no argument to reach that load, so what a person is told, and
the origin the envelope names, is each verb's own (U298).
"""

from __future__ import annotations

from cratekit.cli import registry
from cratekit.core import config, profiles
from cratekit.core.exit_codes import ExitCode

#: The verbs that reach their configuration load with nothing on the command
#: line, a verb or more of every package whose shell loads one.
LOADS_A_CONFIG_BARE = (
    ("acquire", "audit"),
    ("adopt", "apply"),
    ("adopt", "move"),
    ("adopt", "scan"),
    ("analyze", "check"),
    ("backup", "run"),
    ("converge",),
    ("delete", "review"),
    ("export", "set"),
    ("favorites", "backfill"),
    ("favorites", "order"),
    ("favorites", "refresh"),
    ("favorites", "split"),
    ("inbox", "analyzed"),
    ("inbox", "rotate"),
    ("intake", "imported"),
    ("intake", "land"),
    ("intake", "shelve"),
    ("label", "approved"),
    ("label", "artists"),
    ("label", "held"),
    ("label", "judge"),
    ("label", "sync"),
    ("organize",),
    ("profile", "show"),
    ("repair", "paths"),
    ("repair", "rows"),
    ("report", "genres"),
    ("restore", "list"),
    ("review", "list"),
    ("route", "inbox"),
    ("route", "unplaced"),
    ("setbuild",),
    ("status",),
    ("sync", "all"),
    ("sync", "favorites"),
    ("sync", "land"),
    ("sync", "pair"),
    ("sync", "release"),
    ("sync", "removed"),
    ("sync", "strip"),
    ("sync", "taken"),
    ("sync", "twins"),
    ("tag", "backlog"),
    ("tag", "campaign"),
    ("tag", "remap"),
    ("tag", "rows"),
    ("tag", "suggest"),
    ("taxonomy", "upgrade"),
    ("tombstone", "list"),
)


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



def test_a_config_no_verb_can_use(stage):
    refused = int(ExitCode.PRECONDITION)

    def every_verb_refuses(kind: str) -> None:
        for verb in LOADS_A_CONFIG_BARE:
            told = stage.json(*verb)
            assert told.code == refused, (verb, told.stdout)
            cause = told.envelope["cause"]
            assert (cause["reason"], cause["detail"]) == ("config-unusable", {"kind": kind}), verb
            assert stage.crate(*verb).code == refused, verb

    every_verb_refuses("ConfigMissing")

    written = config.config_path()
    written.parent.mkdir(parents=True, exist_ok=True)
    written.write_text("schema_version = [this is not a configuration\n", encoding="utf-8")
    every_verb_refuses("ConfigCorrupt")
