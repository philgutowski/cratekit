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
from tests.test_cli_contract import configured as configured  # noqa: PLC0414
from tests.test_cli_contract import library as library  # noqa: PLC0414

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


# U303's scenarios: what the shell's split and trim must leave as it found it.


def _plain(value):
    """A value as a dump can print it the same way in any process.

    A frozenset's order follows the string hash, which is seeded per process,
    so sets are sorted; a dataclass becomes its fields in declared order.
    """
    import dataclasses

    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: _plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(one) for one in value)
    if isinstance(value, (list, tuple)):
        return [_plain(one) for one in value]
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


def _keep(stage, label: str, text: str) -> None:
    """A reading made in this process, kept in the capture as a command would be."""
    stage.commands.append({"argv": [label], "exit": 0, "stdout": text, "stderr": ""})


def test_the_registry_value_for_value(stage):
    import json as json_module

    dump = {
        "entries": [_plain(entry) for entry in registry.entries()],
        "landed": [entry.name for entry in registry.landed_entries()],
        "verb_names": sorted(registry.VERB_NAMES),
        "features": _plain(registry.FEATURES),
        "policy_rows": _plain(registry.POLICY_ROWS),
        "write_surfaces": sorted(registry.WRITE_SURFACES),
        "emit_surfaces": sorted(registry.EMIT_SURFACES),
        "deferred": sorted(registry.DEFERRED_MODULES),
        "distribution": registry.DISTRIBUTION,
    }
    assert len(dump["entries"]) > 100
    _keep(stage, "(the registry)", json_module.dumps(dump, indent=1, default=repr))


def test_doctor_and_status_on_each_machine(stage, configured, monkeypatch):
    from cratekit.cli import doctor
    from tests import doctor_machines

    for name in ("green", "hostile"):
        machine = getattr(doctor_machines, name)
        monkeypatch.setattr(doctor, "Probes", lambda machine=machine: machine())
        stage.crate("doctor")
        told = stage.json("doctor")
        assert told.envelope["data"]["checks"], name
        stage.crate("status")
        stage.json("status")


def test_setup_answered_by_flags_and_refused(stage, library, monkeypatch):
    from cratekit.cli import doctor
    from tests import doctor_machines

    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    told = stage.json(
        "setup",
        "--library-root", str(library),
        "--db-path", str(library / "db" / "master.db"),
        "--volume-id", doctor_machines.VOLUME,
        "--staging", str(library.parent / "staging"),
        "--profile", "slim",
        "--taxonomy", "default",
    )
    assert told.envelope["data"]["checks"], told.stdout
    assert config.config_path().is_file()
    # Asked again over a configuration that exists, and with a root that does not.
    stage.crate("setup", "--library-root", str(library), "--profile", "full")
    stage.crate("setup", "--library-root", str(library / "nowhere"))


def test_a_gate_shown_answered_stale_and_not_reached(stage, configured):
    ok, asked = int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)

    # Shown, on the screen and in the envelope.
    assert stage.crate("profile", "set", "slim").code == asked
    shown = stage.json("profile", "set", "slim")
    assert shown.code == asked, shown.stdout
    run_id = shown.envelope["run_id"]
    stage.crate("run", "show", run_id)

    # Answered in a second act, but the profile moved before the run went on,
    # so the digest it was answered over no longer holds.
    assert stage.decide(run_id, "profile.set.apply", "apply").code == ok
    assert stage.crate("-d", "profile.set.apply=apply", "profile", "set", "slim").code == ok
    stage.crate("--run", run_id, "profile", "set", "slim")
    stage.json("--run", run_id, "profile", "set", "slim")

    # Answered and continued in one command.
    again = stage.json("profile", "set", "full")
    assert again.code == asked, again.stdout
    stage.crate("run", "decide", again.envelope["run_id"], "profile.set.apply", "apply", "--continue")

    # Answered inline, declined inline, and not reached when there is nothing to change.
    stage.crate("-d", "profile.set.apply=abort", "profile", "set", "slim")
    stage.crate("profile", "set", "full")
    stage.json("-d", "profile.set.apply=nonsense", "profile", "set", "slim")
    stage.crate("run", "decide", run_id, "no.such.gate", "apply", "--actor", "a-person")
    stage.crate("status")


def test_every_toggle_off_and_a_missing_extra(stage):
    import argparse
    import contextlib
    import io
    import json as json_module

    from cratekit import cli
    from cratekit.modules import extras

    def verb_paths(parser) -> list[str]:
        found: list[str] = []

        def walk(node, prefix):
            for action in node._actions:
                if isinstance(action, argparse._SubParsersAction):
                    for name, child in action.choices.items():
                        walk(child, (*prefix, name))
            if prefix:
                found.append(" ".join(prefix))

        walk(parser, ())
        return sorted(found)

    reading = {"full": verb_paths(cli.build_parser(membership=profiles.resolve("full")))}
    for module in profiles.MODULES:
        parser = cli.build_parser(membership=profiles.resolve("full", {module: False}))
        reading[f"full without {module}"] = verb_paths(parser)
        reading[f"slim with {module}"] = verb_paths(
            cli.build_parser(membership=profiles.resolve("slim", {module: True}))
        )

    blocked = registry.Entry(
        name="analyze.demo",
        summary="the analyze.demo verb",
        module="tests.cli_fixtures.needs_extra",
        builder="build",
        handler_key="analyze.demo",
        module_id="analysis",
        extras="analysis",
        extras_modules=("a_third_party_analysis_library",),
    )
    parser = cli.build_parser([blocked], membership=profiles.resolve("full"))
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        parser.parse_args(["analyze", "--help"])
    args = cli.build_parser([blocked], membership=profiles.resolve("full")).parse_args(
        ["analyze", "demo"]
    )
    cause = cli._stub_cause(args._entry, args._stub)
    reading["stub help"] = out.getvalue()
    reading["stub cause"] = [cause.reason, _plain(cause.detail), cause.message]
    reading["install analysis"] = extras.install_command("analysis")
    _keep(stage, "(toggles and the stub)", json_module.dumps(reading, indent=1, default=repr))

    for module in ("analysis", "deletion", "reports", "labels", "duplicates"):
        stage.crate("--help")
        for entry in registry.landed_entries():
            if entry.module_id == module:
                stage.crate(*entry.path)
                break
