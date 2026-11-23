"""U46: the job handler registry, and the one site that drives a queued job.

A handler key resolves to a real function without importing a feature module,
a queued verb without a handler fails here, and a handler gets the frozen
configuration. Populations come from ``registry.ENTRIES`` (Part 5, P3).
"""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path

import pytest

from cratekit.cli import handlers, registry
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from tests import _import_probe

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


# The declaration tables


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


# Resolution refuses before it imports


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
    """KTD26: answering ``is_known`` imports no feature module, measured in a fresh
    interpreter."""
    measured = _import_probe.run_probe(
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
    _import_probe.assert_no_leak(measured, what="answering whether a handler key is known")


# The one call site


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
    """Exactly one ``drive`` call, counted as ``ast.Call`` nodes because the name
    also appears in tuples and prose a text search would count."""
    sites = {}
    for path in sorted((SRC_ROOT / "cratekit").rglob("*.py")):
        text = path.read_text()
        # A module that never spells ``drive`` holds no call to it, so it is not parsed.
        if "_vendor" in path.parts or "drive" not in text:
            continue
        count = _drive_calls(ast.parse(text))
        if count:
            sites[path.relative_to(SRC_ROOT).as_posix()] = count
    assert sites == {"cratekit/cli/handlers.py": 1}, sites


def test_a_job_whose_key_has_no_handler_refuses_rather_than_reporting_success(cfg, queue):
    """The subject is derived from the unbound table, since a fixed name silently
    stops testing this the day somebody binds it."""
    store, _ = queue
    unbound = sorted(handlers.HANDLERS_NOT_YET_BOUND)[0]
    job = jobs.enqueue(
        store, handler_key=unbound, payload={}, cfg=cfg, item_ids=("one",)
    )
    with pytest.raises(CratekitError) as caught:
        handlers.run_job(store, job)
    assert unbound in caught.value.cause.message
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


# A handler may not reload the configuration it was handed


#: Every spelling of "load the configuration fresh" this guard recognises. The
#: spellings it cannot see are named in the guard's docstring.
_RELOAD_ATTRS = frozenset({"load", "load_from_path"})


def _reload_calls(tree: ast.AST, *, aliases: frozenset[str]) -> list[str]:
    """Calls in ``tree`` that reload configuration: ``config.load()``, under an alias,
    or a bare imported ``load()``."""
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        if (
            isinstance(callee, ast.Attribute)
            and callee.attr in _RELOAD_ATTRS
            and isinstance(callee.value, ast.Name)
            and callee.value.id in aliases
        ):
            found.append(f"{callee.value.id}.{callee.attr}")
        elif isinstance(callee, ast.Name) and callee.id in aliases | _RELOAD_ATTRS:
            found.append(callee.id)
    return found


def _config_aliases(tree: ast.AST) -> frozenset[str]:
    """Every local name in ``tree`` bound to the configuration module, read from its
    imports, since an aliased import names the same module differently."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").endswith(
            "cratekit.core"
        ):
            names |= {a.asname or a.name for a in node.names if a.name == "config"}
        elif isinstance(node, ast.Import):
            names |= {
                a.asname or a.name.split(".")[0]
                for a in node.names
                if a.name == "cratekit.core.config"
            }
    return frozenset(names)


def test_no_declared_handler_loads_a_fresh_configuration():
    """No handler, or its batch form, reloads configuration (KTD9), by the spellings
    ``_reload_calls`` knows."""
    problems: list[str] = []
    for key, declaration in handlers.HANDLERS.items():
        dotted, _, attribute = declaration.partition(":")
        path = SRC_ROOT / (dotted.replace(".", "/") + ".py")
        assert path.is_file(), f"{key} declares {dotted}, which is not a module file"
        # A worker's batch form is a handler too (U270), so it is read by the same guard.
        names = {attribute}
        batched = handlers.batching_of(handlers.resolve(key))
        if batched is not None:
            assert batched[0].__module__ == dotted, f"{key}'s batch form lives elsewhere"
            names.add(batched[0].__name__)
        tree = ast.parse(path.read_text())
        aliases = _config_aliases(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or node.name not in names:
                continue
            for spelling in _reload_calls(node, aliases=aliases):
                problems.append(f"{key}: {declaration} calls {spelling}")
    assert not problems, (
        "a handler runs against the configuration frozen when its job was queued "
        f"(KTD9); reloading is the resume bug that closes: {problems}"
    )


@pytest.mark.parametrize(
    "body",
    [
        "from cratekit.core import config\n\ndef handle(job, item, cfg):\n    return config.load()\n",
        "import cratekit.core.config as cfg\n\ndef handle(job, item, c):\n    return cfg.load()\n",
        "from cratekit.core.config import load\n\ndef handle(job, item, cfg):\n    return load()\n",
        "from cratekit.core import config\n\ndef handle(job, item, cfg):\n    return config.load_from_path('x')\n",
    ],
    ids=["dotted", "aliased-module", "bare-name", "load-from-path"],
)
def test_the_fresh_configuration_guard_catches_every_spelling_it_claims(body):
    """The guard fires on a handler using each spelling it claims to recognise."""
    tree = ast.parse(textwrap.dedent(body))
    found = [
        spelling
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "handle"
        for spelling in _reload_calls(node, aliases=_config_aliases(tree))
    ]
    assert found, "the guard would not notice this handler reloading"


def test_the_fresh_configuration_guard_does_not_fire_on_a_handler_that_behaves():
    """P7: a guard that fires on correct code trains people to route around it."""
    body = textwrap.dedent(
        """
        from cratekit.core import config

        def handle(job, item, cfg):
            return cfg.paths.download_staging
        """
    )
    tree = ast.parse(body)
    assert not _reload_calls(tree, aliases=_config_aliases(tree))


# U270: a worker that names a batch form of itself is driven in batches


def _worker_with_batch(seen: list, size: int):
    def single(job_, item_, cfg_):
        raise AssertionError("a worker with a batch form is driven through it")

    def many(job_, items, handed, stop):
        seen.append((tuple(item.item_id for item in items), handed, stop()))
        return {item.item_id: None for item in items}

    single.batched = (many, size)
    return single


def test_a_worker_naming_a_batch_form_is_driven_in_batches_against_the_frozen_config(
    cfg, queue, monkeypatch, tmp_path
):
    store, root = queue
    job = jobs.enqueue(
        store, handler_key="master", payload={}, cfg=cfg, item_ids=("a", "b", "c")
    )
    moved = config.from_dict(
        {
            **json_roundtrip(cfg),
            "paths": {"download_staging": str(tmp_path / "somewhere-else")},
        }
    )
    config.save(moved)
    config.reset_cache()
    seen: list = []
    monkeypatch.setattr(handlers, "resolve", lambda key: _worker_with_batch(seen, 2))

    result = handlers.run_job(store, job, root=root)

    assert [ids for ids, _cfg, _stopped in seen] == [("a", "b"), ("c",)]
    assert all(
        handed.paths.download_staging == cfg.paths.download_staging
        for _ids, handed, _stopped in seen
    )
    assert not any(stopped for _ids, _cfg, stopped in seen)
    assert result.processed == 3


def test_a_worker_naming_no_batch_form_is_driven_one_item_at_a_time(cfg, queue, monkeypatch):
    store, root = queue
    job = jobs.enqueue(store, handler_key="master", payload={}, cfg=cfg, item_ids=("a", "b"))
    seen: list[str] = []

    def single(job_, item_, cfg_):
        seen.append(item_.item_id)

    monkeypatch.setattr(handlers, "resolve", lambda key: single)
    handlers.run_job(store, job, root=root)

    assert seen == ["a", "b"]
    assert handlers.batching_of(single) is None


@pytest.mark.parametrize(
    "named",
    [("not callable", 2), (lambda *a: {}, 0), (lambda *a: {}, True), (lambda *a: {},), "x"],
    ids=["not-callable", "size-zero", "size-bool", "one-element", "not-a-pair"],
)
def test_a_batch_form_that_is_not_a_callable_and_a_size_refuses(named):
    def single(job_, item_, cfg_):
        return None

    single.batched = named
    with pytest.raises(CratekitError) as caught:
        handlers.batching_of(single)
    assert caught.value.cause.reason == "internal-error"


def test_the_export_worker_names_its_batch_form_at_the_providers_add_limit():
    """The one worker bound to batches, and its size, the provider's limit on
    one add request, so a batch is one request (U270)."""
    from cratekit.export import cli as export_cli
    from cratekit.modules.outbound import export as outbound_export
    from cratekit.modules.outbound import tidal_account

    named = handlers.batching_of(handlers.resolve("export.playlist"))
    assert named == (export_cli.handle_batch, outbound_export.BATCH)
    assert outbound_export.BATCH == tidal_account.ADD_CHUNK == 100
    batched = {
        key
        for key in handlers.HANDLERS
        if handlers.batching_of(handlers.resolve(key)) is not None
    }
    assert batched == {"export.playlist"}
