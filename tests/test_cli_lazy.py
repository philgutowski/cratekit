"""Every ``crate`` command imports only the verb it runs (U248).

Before U248 the parser imported all of the registry's verb modules before it
read a word, so ``crate --version`` waited most of a second on modules it never
used. Now a verb's module is imported when argparse selects that verb, and a
help listing asks a module only when its line could read differently for it.

What these tests hold, and the reason for each:

1. **The saving, as modules loaded, never as a wall clock.** Measured in a
   fresh interpreter, because by the time the suite reaches this file every
   verb module is cached and an in-process difference is empty whatever the
   code does (``tests/_import_probe.py`` says why at length).
2. **Nothing a person reads changed.** Every help screen, at the top level, for
   every group and for every verb, on both presets, is the same text from the
   lazy parser as from the eager one, which is the construction loop as it
   stood before U248, kept verbatim for the tree walkers. And the parser's own
   refusals, an unknown verb, a group with no verb, an abbreviated option and a
   bad value, carry the same status and the same words.
3. **The stub still works**: a verb whose extra is missing is listed with what
   it needs and refuses ``module-extras-missing`` when run.
4. **One broken module no longer takes every command down**, the change U248
   makes on purpose: it fails loudly for its own verb and nowhere else.
5. **Every landed entry still imports and resolves its builder**, which the
   parser used to prove on every run and now proves only for the verb it runs.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib
import io

import pytest

from cratekit import cli
from cratekit.cli import registry
from cratekit.core import profiles
from cratekit.core.exit_codes import ExitCode
from cratekit.modules import extras
from tests import _import_probe

#: The ceiling on Cratekit's own modules after ``crate doctor --help`` in a fresh
#: interpreter. Measured at U248: 74 against 298 before it (the card's survey
#: counted 298 after a whole parser). The margin is for the doctor's own closure
#: growing; a return of the eager parser lands far above it.
DOCTOR_HELP_CEILING = 110

#: Two verb modules the card names, which ``doctor --help`` must not load.
#: Each has a large closure of its own (163 and about 128 modules), so loading
#: either is the regression this file exists to catch.
NOT_DOCTORS = ("cratekit.organize.cli", "cratekit.intake.land_cli")


def _verb_modules() -> set[str]:
    return {entry.module for entry in registry.landed_entries()}


def _probe(argv: list[str]) -> dict:
    """Run ``crate ARGV`` in a fresh interpreter and say what it loaded.

    On the full preset so every verb is in the tree and could have been loaded.
    The membership is set rather than read from the isolated home, so the
    measurement does not depend on which preset an unconfigured machine falls
    back to.
    """
    return _import_probe.run_probe(
        f"""
        import contextlib, io, json, sys
        from cratekit import cli
        from cratekit.cli import registry
        from cratekit.core import profiles

        cli._membership = lambda: profiles.resolve("full")
        verbs = {{entry.module for entry in registry.landed_entries()}}
        before = set(sys.modules)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.run({argv!r}, stdout=out, stderr=err)
        loaded = set(sys.modules)
        print(json.dumps({{
            "code": code,
            "printed": out.getvalue(),
            "verbs": sorted(verbs & loaded),
            "cratekit": sum(name.startswith("cratekit") for name in loaded),
            "walked": len(verbs),
            "leaked": sorted(verbs & (loaded - before)),
        }}))
        """
    )


def _closure(module: str) -> dict:
    """The verb modules one module's own import loads, in a fresh interpreter."""
    return _import_probe.run_probe(
        f"""
        import importlib, json, sys
        from cratekit.cli import registry

        verbs = {{entry.module for entry in registry.landed_entries()}}
        importlib.import_module({module!r})
        print(json.dumps({{"verbs": sorted(verbs & set(sys.modules))}}))
        """
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1. The saving, counted in modules
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("argv", [["--version"], ["--help"], []], ids=["version", "help", "bare"])
def test_the_version_and_the_top_level_help_load_no_verb_module(argv):
    result = _probe(argv)
    assert result["code"] == 0
    assert result["walked"] > 50, "the registry walked too few verbs to measure anything"
    assert result["verbs"] == [], f"crate {' '.join(argv)} loaded {result['verbs']}"


def test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports():
    """The card's scenario, against the doctor module's own closure.

    The closure is measured, not listed, so a doctor that grows an import of
    another verb module is not this test's failure, while a parser that loads a
    verb nobody asked for is.
    """
    result = _probe(["doctor", "--help"])
    assert result["code"] == 0
    assert "usage: crate doctor" in result["printed"]
    own = _closure(registry.entry("doctor").module)["verbs"]
    assert registry.entry("doctor").module in result["verbs"]
    assert result["verbs"] == own, f"loaded beyond the doctor's own imports: {result['verbs']}"
    for name in NOT_DOCTORS:
        assert name not in result["verbs"], f"crate doctor --help loaded {name}"
    assert result["cratekit"] < DOCTOR_HELP_CEILING, result["cratekit"]


def test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra():
    """``crate intake --help`` lists five verbs from registry data alone."""
    group = "intake"
    members = [e for e in registry.landed_entries() if e.path[0] == group and len(e.path) > 1]
    assert members and not any(e.extras_modules for e in members)
    result = _probe([group, "--help"])
    assert result["code"] == 0
    for entry in members:
        assert entry.path[1] in result["printed"]
    assert result["verbs"] == [], result["verbs"]


# ═══════════════════════════════════════════════════════════════════════════
# 2. Nothing a person reads changed: lazy against eager
# ═══════════════════════════════════════════════════════════════════════════


def _paths(membership: profiles.Membership) -> list[tuple[str, ...]]:
    """The top level, every group and every verb the preset lists."""
    found = {()}
    for entry in registry.landed_entries():
        if entry.available_to(membership):
            for depth in range(1, len(entry.path) + 1):
                found.add(entry.path[:depth])
    return sorted(found)


def _said(parser: argparse.ArgumentParser, argv: list[str]) -> tuple[object, str, str]:
    """What argparse prints for ARGV and the status it exits with."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            return exc.code, out.getvalue(), err.getvalue()
    entry = getattr(args, "_entry", None)
    return ("parsed", entry.name if entry else None), out.getvalue(), err.getvalue()


@pytest.mark.parametrize("preset", ["full", "slim"])
def test_every_help_screen_reads_the_same_as_the_eager_parsers(preset, monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")
    membership = profiles.resolve(preset)
    paths = _paths(membership)
    assert len(paths) > 40
    for path in paths:
        argv = [*path, "--help"]
        lazy = _said(cli.build_parser(membership=membership), argv)
        eager = _said(cli.build_parser(membership=membership, eager=True), argv)
        assert lazy == eager, f"crate {' '.join(argv)} reads differently"
        assert lazy[0] == 0 and lazy[1].startswith("usage: crate")


@pytest.mark.parametrize(
    "argv",
    [
        ["bogus"],
        ["analyze", "bogus"],
        ["doctor", "--bogus"],
        ["--output", "xml", "status"],
        ["--calls", "0", "status"],
        ["--out", "json", "status"],
        ["--outp=json", "--calls=3", "job", "list"],
        ["-d", "a=b", "--run", "R", "status"],
        ["status", "--he"],
        ["--", "doctor"],
        ["-d"],
        ["job", "list", "extra"],
        ["intake", "land"],
        ["analyze", "run", "--bogus"],
    ],
)
def test_the_parsers_answers_are_the_eager_parsers(argv):
    """Same status, same words, same verb selected, for what argparse decides."""
    membership = profiles.resolve("full")
    lazy = _said(cli.build_parser(membership=membership), argv)
    eager = _said(cli.build_parser(membership=membership, eager=True), argv)
    assert lazy == eager


def test_a_group_named_with_no_verb_prints_the_same_screen(monkeypatch):
    """``crate intake`` with no verb: the dispatcher's own help, unchanged."""
    monkeypatch.setenv("COLUMNS", "80")
    monkeypatch.setattr(cli, "_membership", lambda: profiles.resolve("full"))
    lazy = io.StringIO()
    assert cli.run(["intake"], stdout=lazy, stderr=io.StringIO()) == int(ExitCode.OK)
    real = cli.build_parser
    monkeypatch.setattr(cli, "build_parser", lambda: real(eager=True))
    eager = io.StringIO()
    assert cli.run(["intake"], stdout=eager, stderr=io.StringIO()) == int(ExitCode.OK)
    assert lazy.getvalue() == eager.getvalue()
    assert lazy.getvalue().startswith("usage: crate")


# ═══════════════════════════════════════════════════════════════════════════
# 3 and 4. The stub, and a broken module
# ═══════════════════════════════════════════════════════════════════════════


def _fake(name: str, module: str, **kwargs) -> registry.Entry:
    return registry.Entry(
        name=name,
        summary=f"the {name} verb",
        module=module,
        builder="build",
        handler_key=name,
        **kwargs,
    )


def _with_extra(name: str, module: str) -> registry.Entry:
    return _fake(
        name,
        module,
        module_id="analysis",
        extras="analysis",
        extras_modules=("a_third_party_analysis_library",),
    )


def _help(parser: argparse.ArgumentParser, argv: list[str]) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), pytest.raises(SystemExit):
        parser.parse_args(argv)
    return " ".join(out.getvalue().split())


def test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command():
    entries = [_with_extra("analyze.demo", "tests.cli_fixtures.needs_extra")]
    parser = cli.build_parser(entries, membership=profiles.resolve("full"))
    listed = _help(parser, ["analyze", "--help"])
    assert "the analyze.demo verb (requires the 'analysis' extra)" in listed

    args = cli.build_parser(entries, membership=profiles.resolve("full")).parse_args(
        ["analyze", "demo"]
    )
    assert args._stub is not None and args._handler is None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.reason == "module-extras-missing"
    assert cause.detail["install"] == extras.install_command("analysis")


def test_a_verb_that_imports_its_extra_lazily_is_listed_plainly_as_it_was():
    """The five real entries that declare extras import them inside functions."""
    entries = [_with_extra("analyze.demo", "tests.cli_fixtures.plain")]
    listed = _help(cli.build_parser(entries, membership=profiles.resolve("full")), ["analyze", "--help"])
    assert "the analyze.demo verb" in listed
    assert "requires" not in listed


def test_a_listing_asks_only_the_verbs_whose_line_could_differ():
    asked: list[str] = []

    def importer(name):
        asked.append(name)
        return importlib.import_module(name)

    entries = [
        _fake("analyze.plain", "tests.cli_fixtures.plain"),
        _with_extra("analyze.heavy", "tests.cli_fixtures.plain"),
    ]
    parser = cli.build_parser(entries, membership=profiles.resolve("full"), importer=importer)
    assert asked == []
    _help(parser, ["analyze", "--help"])
    assert asked == ["tests.cli_fixtures.plain"]


def test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working():
    """The deliberate change of U248.

    Before it, an import error of our own in any verb module escaped
    ``build_parser`` on every command, ``crate --help`` included. Now it escapes
    only when its own verb is selected, still as itself and never as a missing
    extra, and a listing that would have asked it shows its plain summary.
    """
    entries = [
        _with_extra("analyze.broken", "tests.cli_fixtures.broken_module"),
        _fake("status", "tests.cli_fixtures.plain"),
    ]
    membership = profiles.resolve("full")
    parser = cli.build_parser(entries, membership=membership)

    assert parser.parse_args(["status"])._entry.name == "status"
    assert "usage: crate status" in _help(cli.build_parser(entries, membership=membership), ["status", "--help"])
    listed = _help(cli.build_parser(entries, membership=membership), ["analyze", "--help"])
    assert "the analyze.broken verb" in listed and "requires" not in listed

    with pytest.raises(ImportError) as raised:
        cli.build_parser(entries, membership=membership).parse_args(["analyze", "broken"])
    assert raised.value.name == "cratekit.this_module_does_not_exist"


def test_the_eager_parser_still_raises_a_broken_module_at_construction():
    entries = [_with_extra("analyze.broken", "tests.cli_fixtures.broken_module")]
    with pytest.raises(ImportError):
        cli.build_parser(entries, membership=profiles.resolve("full"), eager=True)


def test_a_verb_is_built_once_however_often_it_is_asked():
    calls: list[str] = []

    def importer(name):
        calls.append(name)
        return importlib.import_module(name)

    entries = [_with_extra("analyze.demo", "tests.cli_fixtures.plain")]
    parser = cli.build_parser(entries, membership=profiles.resolve("full"), importer=importer)
    _help(parser, ["analyze", "--help"])
    assert parser.parse_args(["analyze", "demo"])._entry.name == "analyze.demo"
    assert parser.parse_args(["analyze", "demo"])._entry.name == "analyze.demo"
    assert len(calls) <= 2


# ═══════════════════════════════════════════════════════════════════════════
# 5. Every landed entry imports and resolves its builder
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("entry", registry.landed_entries(), ids=lambda e: e.name)
def test_every_landed_entry_imports_and_resolves_its_builder(entry):
    module = importlib.import_module(entry.module)
    assert callable(getattr(module, entry.builder, None)), f"{entry.module}.{entry.builder}"
    if entry.argv_builder:
        assert callable(getattr(module, entry.argv_builder, None)), entry.argv_builder


def test_dispatch_in_process_still_builds_and_runs_the_verb_it_names(monkeypatch):
    """``run decide --continue`` and the tail call this with their own words."""
    entries = [_fake("status", "tests.cli_fixtures.plain")]
    real = cli.build_parser
    monkeypatch.setattr(
        cli, "build_parser", lambda: real(entries, membership=profiles.resolve("full"))
    )
    envelope = cli.dispatch(["status"], stderr=io.StringIO())
    assert envelope.verb == "status"
    assert envelope.exit_code is ExitCode.OK

