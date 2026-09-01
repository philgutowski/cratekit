"""U46: the job handler registry, and the one site that drives a queued job.

WHAT THIS FILE GUARDS THAT THE ENGINE'S OWN SUITE CANNOT. ``tests/test_jobs.py``
proves ``jobs.drive`` keeps its promises when called directly. It has always
passed, and until this unit nothing in ``src`` called ``drive`` at all, so a green
run of that file said nothing about whether the product ever ran a queued item.
This file is about the binding: that a handler key resolves to a real function,
that resolving one does not drag a feature module into a process that is only
supervising, that a verb added later without a handler fails HERE rather than at
somebody's queue, and that the configuration reaching a handler is the frozen one.

THE POPULATION IS DERIVED, NEVER LISTED (Part 5, P3). Every quantified assertion
below walks ``registry.ENTRIES`` or the tables themselves, so the verb somebody
adds next month is inside the assertion the day it lands.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from cratekit.cli import handlers, registry
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"


def queued_entries() -> tuple[registry.Entry, ...]:
    """Every verb whose work this build queues, derived from the registry."""
    return tuple(e for e in registry.ENTRIES if e.landed and e.long_running)


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine. ``enqueue`` freezes exactly this."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def queue(tmp_path):
    root = tmp_path / "queue"
    root.mkdir()
    with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
        yield store, root


# ---------------------------------------------------------------------------
# The declaration tables
# ---------------------------------------------------------------------------


def test_the_declared_population_is_not_empty():
    """The vacuity guard. Every assertion below quantifies over these."""
    assert queued_entries()
    assert handlers.HANDLERS


def test_every_declared_handler_resolves_to_a_callable():
    for key in handlers.HANDLERS:
        assert callable(handlers.resolve(key)), key


def test_every_queued_verb_is_either_bound_or_named_as_unbound():
    """A verb added later without a handler fails HERE, not at a user's queue."""
    missing = [
        entry.handler_key
        for entry in queued_entries()
        if entry.handler_key not in handlers.HANDLERS
        and entry.handler_key not in handlers.HANDLERS_NOT_YET_BOUND
    ]
    assert not missing, (
        "these queued verbs declare no handler and are not recorded as unbound, "
        f"so their jobs would report cleanly and run nothing: {sorted(missing)}"
    )


def test_no_key_is_both_bound_and_recorded_as_unbound():
    """The exemption expires on its own, which is what keeps it from rotting."""
    overlap = set(handlers.HANDLERS) & set(handlers.HANDLERS_NOT_YET_BOUND)
    assert not overlap, sorted(overlap)


def test_neither_table_names_a_verb_this_build_does_not_queue():
    """A declaration cannot outlive the verb it describes."""
    queued = {entry.handler_key for entry in queued_entries()}
    stale = (set(handlers.HANDLERS) | set(handlers.HANDLERS_NOT_YET_BOUND)) - queued
    assert not stale, sorted(stale)


def test_every_unbound_verb_says_why_and_every_bound_one_says_nothing():
    for key in handlers.HANDLERS_NOT_YET_BOUND:
        assert (handlers.unbound_reason(key) or "").strip(), key
    for key in handlers.HANDLERS:
        assert handlers.unbound_reason(key) is None, key


def test_is_known_answers_for_a_declared_key_and_an_invented_one():
    assert handlers.is_known(next(iter(handlers.HANDLERS)))
    assert not handlers.is_known("no.such.handler")


# ---------------------------------------------------------------------------
# Resolution refuses before it imports
# ---------------------------------------------------------------------------


def test_an_undeclared_key_refuses_by_name():
    with pytest.raises(CratekitError) as caught:
        handlers.resolve("no.such.handler")
    cause = caught.value.cause
    assert "no.such.handler" in cause.message
    assert str(cause.remediation.remedy) == "report-defect"


@pytest.mark.parametrize(
    "declaration, expected",
    [
        ("cratekit.master.cli", "declaration"),
        ("cratekit.master.cli:nope", "no such member"),
        ("cratekit.master.cli:SOURCE", "not callable"),
    ],
)
def test_a_broken_declaration_refuses_rather_than_returning_something(
    monkeypatch, declaration, expected
):
    monkeypatch.setattr(handlers, "HANDLERS", {**handlers.HANDLERS, "broken": declaration})
    with pytest.raises(CratekitError) as caught:
        handlers.resolve("broken")
    assert expected in caught.value.cause.message


def test_resolving_a_handler_key_imports_nothing_a_supervisor_does_not_need():
    """KTD26's property, measured where it can differ.

    A FRESH INTERPRETER and a PER-CALL DELTA, both load bearing. In this process
    every feature module is already in ``sys.modules`` by the time the suite gets
    here, so an in-process before-and-after difference is empty whatever the code
    does; ``tests/test_cli_contract.py`` records a mutation table proving exactly
    that about the same property one seam over. A total-set assertion would fail
    for an unrelated reason too, because importing ``cratekit.cli.handlers`` runs
    the package ``__init__``. So: one clean process, and the only thing measured is
    what each individual ``is_known`` call pulled in.
    """
    probe = textwrap.dedent(
        """
        import json, sys
        from cratekit.cli import handlers, registry

        walked, leaked = 0, {}
        for entry in registry.ENTRIES:
            if not (entry.landed and entry.long_running):
                continue
            before = set(sys.modules)
            handlers.is_known(entry.handler_key)
            handlers.unbound_reason(entry.handler_key)
            added = sorted(
                name for name in set(sys.modules) - before
                if name.startswith("cratekit")
            )
            walked += 1
            if added:
                leaked[entry.handler_key] = added
        print(json.dumps({"walked": walked, "leaked": leaked}))
        """
    )
    done = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, cwd=REPO_ROOT
    )
    assert done.returncode == 0, done.stderr
    measured = json.loads(done.stdout)
    assert measured["walked"] > 0, "the probe walked no keys, so it measured nothing"
    assert measured["leaked"] == {}, measured["leaked"]


# ---------------------------------------------------------------------------
# The one call site
# ---------------------------------------------------------------------------


def _drive_calls(tree: ast.AST) -> int:
    found = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        if isinstance(callee, ast.Attribute) and callee.attr == "drive":
            found += 1
        elif isinstance(callee, ast.Name) and callee.id == "drive":
            found += 1
    return found


def test_exactly_one_place_in_the_package_calls_the_job_driver():
    """One driver, and it is found by parsing rather than by searching for text.

    A text search cannot answer this: ``core/jobs.py`` names ``jobs.drive`` in two
    ``origin`` tuples and ``backup/cli.py`` names it in prose, so a grep returns
    four lines that are not calls. Counting ``ast.Call`` nodes is the difference
    between measuring the code and measuring the comments.
    """
    sites = {}
    for path in sorted((SRC_ROOT / "cratekit").rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        count = _drive_calls(ast.parse(path.read_text()))
        if count:
            sites[path.relative_to(SRC_ROOT).as_posix()] = count
    assert sites == {"cratekit/cli/handlers.py": 1}, sites


def test_a_job_whose_key_has_no_handler_refuses_rather_than_reporting_success(cfg, queue):
    store, _ = queue
    job = jobs.enqueue(
        store, handler_key="rebuild", payload={}, cfg=cfg, item_ids=("one",)
    )
    with pytest.raises(CratekitError) as caught:
        handlers.run_job(store, job)
    assert "rebuild" in caught.value.cause.message
    assert jobs.items(store, job.job_id)[0].state == jobs.ItemState.PENDING


def test_the_handler_receives_the_frozen_configuration_and_not_the_current_one(
    cfg, queue, monkeypatch, tmp_path
):
    """KTD9, driven. The setting is changed on disk between enqueue and drive."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="master", payload={}, cfg=cfg, item_ids=("one",)
    )

    moved = config.from_dict(
        {
            **json_roundtrip(cfg),
            "paths": {"download_staging": str(tmp_path / "somewhere-else")},
        }
    )
    config.save(moved)
    config.reset_cache()

    seen: list[config.Config] = []

    def spy(job_, item_, handed):
        seen.append(handed)
        return None

    monkeypatch.setattr(handlers, "resolve", lambda key: spy)
    result = handlers.run_job(store, job, root=root)

    assert len(seen) == 1
    assert seen[0].paths.download_staging == cfg.paths.download_staging
    assert seen[0].paths.download_staging != moved.paths.download_staging
    assert result.processed == 1


def test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between(
    cfg, queue, monkeypatch, tmp_path
):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="master", payload={}, cfg=cfg, item_ids=("one",)
    )
    moved = config.from_dict(
        {
            **json_roundtrip(cfg),
            "paths": {"download_staging": str(tmp_path / "somewhere-else")},
        }
    )
    config.save(moved)
    config.reset_cache()

    monkeypatch.setattr(handlers, "resolve", lambda key: (lambda j, i, c: None))
    result = handlers.run_job(store, job, root=root)

    assert result.drifted
    warnings = handlers.drift_warnings(result.drifted)
    assert warnings and warnings[0]["code"] == "config-drift"
    assert "paths.download_staging" in warnings[0]["message"]


def test_no_drift_means_no_warning():
    assert handlers.drift_warnings(()) == ()


def test_a_handler_that_produces_a_file_has_it_committed_and_recorded(cfg, queue, monkeypatch):
    """The artifact half of the driver's contract, exercised from the shipped site."""
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="master", payload={}, cfg=cfg, item_ids=("one",)
    )
    final = root / "out" / "one.txt"

    def produce(job_, item_, cfg_):
        staged = root / "staged-one"
        staged.write_text("mastered")
        return jobs.Produced(staged=staged, final=final)

    monkeypatch.setattr(handlers, "resolve", lambda key: produce)
    handlers.run_job(store, job, root=root)

    item = jobs.items(store, job.job_id)[0]
    assert item.state == jobs.ItemState.DONE
    assert item.artifact == str(final)
    assert final.read_text() == "mastered"


def json_roundtrip(cfg: config.Config) -> dict:
    """The configuration as the plain mapping ``from_dict`` accepts."""
    import tomllib

    return tomllib.loads(cfg.to_toml_bytes().decode("utf-8"))


# ---------------------------------------------------------------------------
# A handler may not reload the configuration it was handed
# ---------------------------------------------------------------------------


def test_no_declared_handler_loads_a_fresh_configuration():
    """The guard that makes the frozen-config parameter more than a convention.

    A three-argument handler can still call ``config.load()`` in its body; the
    signature removes the NEED, not the ability. This is what removes the ability,
    and it is derived from the table rather than from a list of modules.
    """
    problems: list[str] = []
    for key, declaration in handlers.HANDLERS.items():
        dotted, _, attribute = declaration.partition(":")
        path = SRC_ROOT / (dotted.replace(".", "/") + ".py")
        assert path.is_file(), f"{key} declares {dotted}, which is not a module file"
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.FunctionDef) or node.name != attribute:
                continue
            for inner in ast.walk(node):
                if (
                    isinstance(inner, ast.Call)
                    and isinstance(inner.func, ast.Attribute)
                    and inner.func.attr == "load"
                    and isinstance(inner.func.value, ast.Name)
                    and inner.func.value.id == "config"
                ):
                    problems.append(f"{key}: {declaration} calls config.load")
    assert not problems, (
        "a handler runs against the configuration frozen when its job was queued "
        f"(KTD9); reloading is the resume bug that closes: {problems}"
    )


def test_the_fresh_configuration_guard_catches_a_handler_that_reloads(tmp_path):
    """The guard proved against a handler that does the thing, not just asserted."""
    source = textwrap.dedent(
        """
        from cratekit.core import config

        def handle(job, item, cfg):
            return config.load()
        """
    )
    found = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name != "handle":
            continue
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and inner.func.attr == "load"
                and isinstance(inner.func.value, ast.Name)
                and inner.func.value.id == "config"
            ):
                found.append(inner)
    assert found, "the guard above would not notice a handler that reloads"
