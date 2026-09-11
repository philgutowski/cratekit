"""U61: ``crate sync all`` composes the source increments that already have workers.

WHAT THIS FILE GUARDS. Before U61 the verb queued one job per enabled source
under its own handler key, ``sync.all``, with no items, and nothing ran a job
under that key. Every assertion the old test made held, the jobs existed and
shared a run id, and the verb that replaces ``dj-sync`` did nothing at all. So
the properties here are the ones that make a pass real: each source is queued
under the key its OWN worker serves, with items; the jobs are then driven to
done through the argv the job engine would spawn; and no path leaves a job
under ``sync.all`` behind.

THE PROVIDERS ARE STAND INS and are the only substitution. The catalogue and
the streaming account are put in front of their seams on the module attribute,
exactly as the two worker suites do, and everything else is the real
dispatcher, the real gate flow, the real queue and the real workers.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.cli import gates, handlers, registry
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import cli as favorites_cli
from cratekit.modules.outbound import source as outbound_source
from cratekit.sync import cli as sync_cli
from cratekit.sync import sources
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.test_cli_contract import _enqueue_calls
from tests.test_config import valid_data
from tests.test_label_workers import LABELS, SLUGS, readable, register
from tests.test_label_workers import bind as bind_catalogue
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import catalog

SYNC_ALL = registry.entry("sync.all")
CONFIRM = sync_cli.CONFIRM
SRC = Path(sync_cli.__file__)


def _install(tmp_path, monkeypatch, profile: str) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": profile}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    outbound_source.forget_libraries()
    return resolved


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine with every module switched on, so both built sources are enabled."""
    yield _install(tmp_path, monkeypatch, "full")
    outbound_source.forget_libraries()


@pytest.fixture
def slim(tmp_path, monkeypatch):
    """The slim profile, which switches on playlists alone."""
    yield _install(tmp_path, monkeypatch, "slim")
    outbound_source.forget_libraries()


@pytest.fixture
def exported(installed) -> Path:
    return outbound_fakes.write_export(installed.library.root / "outbound")


def _jobs() -> list[jobs.Job]:
    with jobs.open_store() as store:
        return list(jobs.list_jobs(store))


def _items(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return [item.item_id for item in jobs.items(store, job_id)]


def _verb(exported: Path) -> list[str]:
    return ["sync", "all", "--export", str(exported)]


def _confirmed(exported: Path, option: str = "sync") -> tuple[str, int, dict]:
    """R34's two acts on the composer's own gate, then the pass. Returns (run, code, envelope)."""
    code, refused = drive(_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, passed = drive(["--run", run_id, *_verb(exported)])
    return run_id, code, passed


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declarations the composition rests on
# ═══════════════════════════════════════════════════════════════════════════


def test_every_source_with_a_worker_names_a_key_the_registry_binds():
    """The keys ``sources`` holds as strings, pinned where the registry is visible."""
    built = [spec for spec in sources.SPECS if spec.handler_key is not None]
    assert built, "no source declares a worker, so every drive below is vacuous"
    for spec in built:
        owner = registry.by_handler_key(spec.handler_key)
        assert owner.landed and owner.long_running, owner.name
        assert spec.handler_key in handlers.HANDLERS, spec.handler_key
        assert owner.module_id == spec.module_id, (
            f"{spec.source_id} is switched by {spec.module_id!r} but its worker's "
            f"verb is switched by {owner.module_id!r}, so a profile could enable "
            f"one without the other"
        )


def test_every_source_with_a_worker_has_a_planner_and_no_other_does():
    assert set(sync_cli.PLANNERS) == {
        spec.source_id for spec in sources.SPECS if spec.handler_key is not None
    }


def test_no_path_creates_a_job_under_sync_all():
    """The registry derived population, and the composer's own module, both say no.

    The queueing guard in ``tests/test_cli_contract.py`` parses a long-running
    verb's module for an ``enqueue`` call. This is its converse for the one verb
    that must never have one: a call here would be a job under a key nothing
    runs, which is the whole of R-203 for this verb.
    """
    queued = {e.handler_key for e in registry.ENTRIES if e.landed and e.long_running}
    assert SYNC_ALL.handler_key not in queued
    assert SYNC_ALL.argv_builder is None
    assert SYNC_ALL.handler_key not in handlers.HANDLERS
    assert SYNC_ALL.handler_key not in handlers.HANDLERS_NOT_YET_BOUND
    assert _enqueue_calls(ast.parse(SRC.read_text())) == 0


def test_the_composer_declares_one_explicit_gate_compared_against_a_digest():
    (gate,) = SYNC_ALL.gates
    assert gate.name == CONFIRM
    assert gate.explicit and gate.digest_source is not None
    favourites = next(
        g for g in registry.entry(sync_cli.FAVORITES_VERB).gates
        if g.name == sync_cli.FAVORITES_CONFIRM
    )
    assert gate.options == favourites.options
    assert gate.prompt == favourites.prompt


# ═══════════════════════════════════════════════════════════════════════════
# 2. A full pass
# ═══════════════════════════════════════════════════════════════════════════


def test_a_full_pass_queues_each_source_under_its_own_key_with_one_run(
    installed, exported
):
    del installed
    register(*LABELS[:2])
    run_id, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "ok"

    queued = {job.handler_key: job for job in _jobs()}
    assert set(queued) == {"sync.favorites", "sync.labels"}
    assert {job.payload["run_id"] for job in queued.values()} == {run_id}, (
        "every source in one pass must share one intake run, or each worker "
        "writes its own intake file and R29 is broken"
    )
    assert _items(queued["sync.labels"].job_id) == list(SLUGS[:2])
    _, resolved = favorites_cli.resolve_sweep(str(exported), None)
    assert _items(queued["sync.favorites"].job_id) == list(resolved.track_ids)
    assert resolved.track_ids, "the fixture's favourites playlist is empty"

    summary = passed["data"]["summary"]
    assert summary["queued"] == 2
    assert {(j["source"], j["job_id"], j["handler_key"]) for j in summary["jobs"]} == {
        (job.payload["source_id"], job.job_id, key) for key, job in queued.items()
    }
    # PLAYLISTS IS CORE, so every profile enables it and every pass names it.
    assert summary["not_queued"] == {"playlists": sync_cli.NOT_BUILT}


def test_the_gate_refusal_has_queued_nothing_and_says_what_would_be(
    installed, exported
):
    """PLAN, ASK, QUEUE. A labels sweep queued before the question would be queued
    again by the run that answers it."""
    del installed
    register(LABELS[0])
    code, refused = drive(_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _jobs() == []
    shown = refused["cause"]["detail"]["shown"]
    assert shown["queued"] == []
    assert shown["would_queue"] == ["favorites", "labels"]


def test_the_gate_asks_over_the_digest_sync_favorites_itself_offers(
    installed, exported
):
    """Read off the two verbs' own run records, not recomputed here, so the
    comparison is between what each verb offered rather than a function and
    itself."""
    del installed
    register(LABELS[0])
    _, composed = drive(_verb(exported))
    _, alone = drive(["sync", "favorites", "--export", str(exported)])
    offered = gates.load(composed["run_id"]).offers[CONFIRM]
    assert offered == gates.load(alone["run_id"]).offers[sync_cli.FAVORITES_CONFIRM]


def test_aborting_the_confirmation_queues_no_favourites_job_and_says_so(
    installed, exported
):
    del installed
    register(LABELS[0])
    _, code, passed = _confirmed(exported, option="abort")
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.labels"]
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": sync_cli.DECLINED,
        "playlists": sync_cli.NOT_BUILT,
    }
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "favorites"]
    assert check["status"] == "info" and "abort" in check["detail"]


def test_a_source_that_refuses_does_not_stop_the_other(installed):
    """No export: favourites refuses for itself and labels is still swept, with
    no question asked, because the only question was favourites'."""
    del installed
    register(LABELS[0])
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.labels"]
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
        "playlists": sync_cli.NOT_BUILT,
    }
    assert "sync-source-not-queued" in {w["code"] for w in passed["warnings"]}
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "favorites"]
    assert check["status"] == "fail"


def test_nothing_queued_because_every_source_refused_is_a_refusal(installed):
    """Not a no-op. A pass that did nothing for a reason the person can fix says so."""
    del installed
    code, refused = drive(["sync", "all"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "outbound-export-required"
    assert refused["cause"]["detail"]["sources"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
        "labels": "label-registry-empty",
        "playlists": sync_cli.NOT_BUILT,
    }
    assert _jobs() == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. The slim profile, the honest zero
# ═══════════════════════════════════════════════════════════════════════════


def test_a_slim_pass_queues_nothing_and_reports_playlists_as_not_built(slim):
    del slim
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "no_op", (
        "nothing was queued, so an ok would be a clean report over nothing"
    )
    assert passed["data"]["summary"]["queued"] == 0
    assert passed["data"]["summary"]["not_queued"] == {"playlists": sync_cli.NOT_BUILT}
    (check,) = passed["data"]["checks"]
    assert check["title"] == "playlists" and "not built" in check["detail"]
    assert _jobs() == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. What the pass queued, run by the workers that already exist
# ═══════════════════════════════════════════════════════════════════════════


def test_the_jobs_a_pass_queues_run_to_done_through_the_existing_workers(
    installed, exported, monkeypatch
):
    """Driven through ``argv_for``, the argv the job engine spawns, so the
    favourites resume loads the run ``hand_off`` minted and the dispatcher's own
    rule that a run belongs to one verb is what is under test."""
    del installed
    register(*LABELS[:2])
    bind_catalogue(monkeypatch, readable(*SLUGS[:2]))
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind_account(monkeypatch, account)
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed

    for job in _jobs():
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), (job.handler_key, resumed)
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), job.handler_key
    assert sorted(account.hearted) == ["tid-1", "tid-2"]
    assert {job.handler_key for job in _jobs()} == {"sync.favorites", "sync.labels"}


def test_the_favourites_job_carries_a_gate_run_its_own_verb_owns(installed, exported):
    del installed
    register(LABELS[0])
    run_id, _, _ = _confirmed(exported)
    (job,) = [j for j in _jobs() if j.handler_key == "sync.favorites"]
    handed = gates.load(job.payload[jobs.GATE_RUN_KEY])
    assert handed.run_id != run_id
    assert handed.verb == sync_cli.FAVORITES_VERB
    decision = handed.decisions[sync_cli.FAVORITES_CONFIRM]
    original = gates.load(run_id).decisions[CONFIRM]
    assert (decision.option, decision.actor, decision.digest) == (
        original.option,
        "a-person",
        original.digest,
    )


# ═══════════════════════════════════════════════════════════════════════════
# 5. The hand off copies an answer and never supplies one
# ═══════════════════════════════════════════════════════════════════════════


def _gates() -> gates.Gates:
    return gates.Gates(state=gates.new_run(SYNC_ALL))


def test_a_hand_off_with_nothing_recorded_refuses(installed):
    del installed
    (spec,) = SYNC_ALL.gates
    with pytest.raises(CratekitError) as caught:
        _gates().hand_off(spec, verb="sync.favorites", gate="sync.favorites.confirm")
    assert caught.value.cause.reason == "internal-error"


def test_a_hand_off_of_a_decision_with_no_digest_refuses(installed):
    del installed
    (spec,) = SYNC_ALL.gates
    asked = _gates()
    asked.state.decisions[spec.name] = gates.Decision("sync", "a-person", "now")
    with pytest.raises(CratekitError):
        asked.hand_off(spec, verb="sync.favorites", gate="sync.favorites.confirm")


@pytest.mark.parametrize(
    "verb, gate",
    [
        ("sync.favorites", "sync.favorites.nothing"),
        ("sync.favorites", "write.cloudsync.unreadable"),
        ("export.playlist", "export.playlist.confirm"),
    ],
    ids=["undeclared", "option-not-offered", "another-verb"],
)
def test_a_hand_off_to_a_gate_that_could_not_mean_the_same_refuses(installed, verb, gate):
    del installed
    (spec,) = SYNC_ALL.gates
    asked = _gates()
    asked.state.decisions[spec.name] = gates.Decision("sync", "a-person", "now", "d1")
    with pytest.raises(CratekitError):
        asked.hand_off(spec, verb=verb, gate=gate)


def test_a_source_refused_at_queue_time_leaves_the_queued_ones_named(
    installed, exported, monkeypatch
):
    """The review's finding, driven. Favourites queues first and each enqueue is
    its own transaction, so a labels refusal at that moment leaves a favourites
    job filed. The pass must say so, or rerunning it queues favourites twice."""
    del installed
    from cratekit.core.cause import refuse
    from cratekit.label import cli as label_cli

    def refusing(*args, **kwargs):
        raise refuse("internal-error", "the queue refused this source")

    monkeypatch.setattr(label_cli, "queue_sweep", refusing)
    register(LABELS[0])
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    (job,) = _jobs()
    assert job.handler_key == "sync.favorites"
    summary = passed["data"]["summary"]
    assert [j["job_id"] for j in summary["jobs"]] == [job.job_id]
    assert summary["not_queued"]["labels"] == "internal-error"
    assert "sync-source-not-queued" in {w["code"] for w in passed["warnings"]}
