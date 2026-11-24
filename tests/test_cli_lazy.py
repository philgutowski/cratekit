"""Every ``crate`` command imports only the verb it runs (U248): a verb's module loads when
argparse selects it, a help listing asks one only when its line could differ. Held here: the
saving in modules, never a clock; help and refusals as the eager parsers'; the stub; one broken
module failing only its verb; every landed entry resolving its builder."""

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

#: Ceiling on Cratekit's own modules after ``crate doctor --help`` on the full preset:
#: 58 at U248 against 301 before; the margin is for the doctor's own closure growing.
#: 2026-11-23, U328: the registry's table went into five parts, which load with it at every
#: start, so the ceiling rose by those five (86 to 91 on the base it was measured on, 4d1ff8b9).
DOCTOR_HELP_CEILING = 95

#: Two verb modules with large closures of their own, which ``doctor --help`` must not load.
NOT_DOCTORS = ("cratekit.organize.cli", "cratekit.intake.land_cli")


def _verb_modules() -> set[str]:
    return {entry.module for entry in registry.landed_entries()}


def _probe(argv: list[str]) -> dict:
    """Run ``crate ARGV`` in a fresh interpreter on the full preset and say what it loaded."""
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
            "code": code, "printed": out.getvalue(), "verbs": sorted(verbs & loaded),
            "cratekit": sum(name.startswith("cratekit") for name in loaded), "walked": len(verbs),
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


# ═══ 1. The saving, counted in modules ═════════════════════════════════════
@pytest.mark.parametrize("argv", [["--version"], ["--help"], []], ids=["version", "help", "bare"])
def test_the_version_and_the_top_level_help_load_no_verb_module(argv):
    result = _probe(argv)
    assert result["code"] == 0
    assert result["walked"] > 50, "the registry walked too few verbs to measure anything"
    assert result["verbs"] == [], f"crate {' '.join(argv)} loaded {result['verbs']}"
    assert result["leaked"] == [], result["leaked"]


def test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports():
    """The doctor loads its own measured closure, and the parser loads no verb nobody asked for."""
    result = _probe(["doctor", "--help"])
    assert result["code"] == 0
    assert "usage: crate doctor" in result["printed"]
    own = _closure(registry.entry("doctor").module)["verbs"]
    assert registry.entry("doctor").module in result["verbs"]
    assert result["verbs"] == own, f"loaded beyond the doctor's own imports: {result['verbs']}"
    assert result["leaked"] == own, "the run itself, not the probe's setup, loaded the doctor"
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


# ═══ 2. Nothing a person reads changed: lazy against eager ═════════════════
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
    # Each lazy parser is fresh; the eager one is plain argparse, which parsing leaves as built.
    eager = cli.build_parser(membership=membership, eager=True)
    for path in paths:
        argv = [*path, "--help"]
        lazy = _said(cli.build_parser(membership=membership), argv)
        assert lazy == _said(eager, argv), f"crate {' '.join(argv)} reads differently"
        assert lazy[0] == 0 and lazy[1].startswith("usage: crate")


@pytest.mark.parametrize(
    "argv",
    [
        ["bogus"], ["analyze", "bogus"], ["doctor", "--bogus"], ["--output", "xml", "status"],
        ["--calls", "0", "status"], ["--out", "json", "status"],
        ["--outp=json", "--calls=3", "job", "list"], ["-d", "a=b", "--run", "R", "status"],
        ["status", "--he"], ["--", "doctor"], ["-d"], ["job", "list", "extra"], ["intake", "land"],
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


# ═══ 3 and 4. The stub, and a broken module ════════════════════════════════
def _fake(name: str, module: str, **kwargs) -> registry.Entry:
    return registry.Entry(
        name=name, summary=f"the {name} verb", module=f"tests.cli_fixtures.{module}",
        builder="build", handler_key=name, **kwargs,
    )


def _with_extra(name: str, module: str) -> registry.Entry:
    extra = {"extras": "analysis", "extras_modules": ("a_third_party_analysis_library",)}
    return _fake(name, module, module_id="analysis", **extra)


_BUILD_PARSER = cli.build_parser


def _full(entries: list[registry.Entry], **kwargs) -> argparse.ArgumentParser:
    """A fresh parser over ``entries`` on the full preset, by the real builder."""
    return _BUILD_PARSER(entries, membership=profiles.resolve("full"), **kwargs)


def _recording(asked: list[str]):
    """An importer that records each module it is asked for, then imports it."""

    def importer(name):
        asked.append(name)
        return importlib.import_module(name)

    return importer


def _help(parser: argparse.ArgumentParser, argv: list[str]) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), pytest.raises(SystemExit):
        parser.parse_args(argv)
    return " ".join(out.getvalue().split())


def test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command():
    entries = [_with_extra("analyze.demo", "needs_extra")]
    listed = _help(_full(entries), ["analyze", "--help"])
    assert "the analyze.demo verb (requires the 'analysis' extra)" in listed
    args = _full(entries).parse_args(["analyze", "demo"])
    assert args._stub is not None and args._handler is None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.reason == "module-extras-missing"
    assert cause.detail["install"] == extras.install_command("analysis")


def test_a_verb_that_imports_its_extra_lazily_is_listed_plainly_as_it_was():
    """The five real entries that declare extras import them inside functions."""
    listed = _help(_full([_with_extra("analyze.demo", "plain")]), ["analyze", "--help"])
    assert "the analyze.demo verb" in listed
    assert "requires" not in listed


def test_a_listing_asks_only_the_verbs_whose_line_could_differ():
    asked: list[str] = []
    entries = [_fake("analyze.plain", "plain"), _with_extra("analyze.heavy", "plain")]
    parser = _full(entries, importer=_recording(asked))
    assert asked == []
    _help(parser, ["analyze", "--help"])
    assert asked == ["tests.cli_fixtures.plain"]


def test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working():
    """U248's deliberate change: an import error escapes as itself, for its own verb alone."""
    entries = [_with_extra("analyze.broken", "broken_module"), _fake("status", "plain")]
    assert _full(entries).parse_args(["status"])._entry.name == "status"
    assert "usage: crate status" in _help(_full(entries), ["status", "--help"])
    listed = _help(_full(entries), ["analyze", "--help"])
    assert "the analyze.broken verb" in listed and "requires" not in listed
    with pytest.raises(ImportError) as raised:
        _full(entries).parse_args(["analyze", "broken"])
    assert raised.value.name == "cratekit.this_module_does_not_exist"


def test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb():
    """The listing's swallow is not only for ImportError: any failure keeps the plain line."""
    entries = [_with_extra("analyze.odd", "raises_at_import"), _fake("analyze.fine", "plain")]
    listed = _help(_full(entries), ["analyze", "--help"])
    assert "the analyze.odd verb" in listed and "requires" not in listed
    assert "the analyze.fine verb" in listed
    with pytest.raises(ValueError, match="a defect of our own"):
        _full(entries).parse_args(["analyze", "odd"])


def test_a_defective_builder_is_a_defect_and_never_a_usage_error():
    """A builder's own ArgumentError is a traceback, never exit 2 blaming the person."""
    entries = [_fake("status", "conflicting_builder")]
    parser = _full(entries)
    with pytest.raises(RuntimeError, match="building status from") as raised:
        parser.parse_args(["status"])
    assert isinstance(raised.value.__cause__, argparse.ArgumentError)
    # Built only once the builder returned, so asking again is still a defect.
    with pytest.raises(RuntimeError, match="building status from"):
        parser.parse_args(["status"])
    with pytest.raises(argparse.ArgumentError):
        _full(entries, eager=True)


def test_an_argument_error_raised_by_the_import_is_a_defect_too():
    """The same class one step earlier, from review round two."""
    with pytest.raises(RuntimeError, match="building status from") as raised:
        _full([_fake("status", "argument_error_at_import")]).parse_args(["status"])
    assert isinstance(raised.value.__cause__, argparse.ArgumentError)


def test_the_eager_parser_still_raises_a_broken_module_at_construction():
    with pytest.raises(ImportError):
        _full([_with_extra("analyze.broken", "broken_module")], eager=True)


def test_a_verb_is_built_once_however_often_it_is_asked():
    calls: list[str] = []
    parser = _full([_with_extra("analyze.demo", "plain")], importer=_recording(calls))
    _help(parser, ["analyze", "--help"])
    assert parser.parse_args(["analyze", "demo"])._entry.name == "analyze.demo"
    assert parser.parse_args(["analyze", "demo"])._entry.name == "analyze.demo"
    assert calls == ["tests.cli_fixtures.plain"] * 2, "one for the listing, one to build"


# ═══ 5. Every landed entry imports and resolves its builder ═════════════════
@pytest.mark.parametrize("entry", registry.landed_entries(), ids=lambda e: e.name)
def test_every_landed_entry_imports_and_resolves_its_builder(entry):
    module = importlib.import_module(entry.module)
    assert callable(getattr(module, entry.builder, None)), f"{entry.module}.{entry.builder}"
    if entry.argv_builder:
        assert callable(getattr(module, entry.argv_builder, None)), entry.argv_builder


def test_dispatch_in_process_still_builds_and_runs_the_verb_it_names(monkeypatch):
    """``run decide --continue`` and the tail call this with their own words."""
    monkeypatch.setattr(cli, "build_parser", lambda: _full([_fake("status", "plain")]))
    envelope = cli.dispatch(["status"], stderr=io.StringIO())
    assert envelope.verb == "status"
    assert envelope.exit_code is ExitCode.OK
