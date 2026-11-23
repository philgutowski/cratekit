"""U61: ``crate sync all`` composes the source increments that already have workers.

A pass is real only when each source is queued under its own worker's key,
with items, the jobs run to done through the engine's argv, and no job is left
under ``sync.all``, which nothing runs. Only the providers are stand ins.
"""

from __future__ import annotations

import ast
import io
import os
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import gates, handlers, registry
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import cli as favorites_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import source as outbound_source
from cratekit.sync import cli as sync_cli
from cratekit.sync import playlists, sources, watermarks
from tests import outbound_fakes
from tests._sync_builders import exited, failed
from tests.cli_drive import drive
from tests.intake.test_workers import Track
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
from tests.test_cli_contract import _enqueue_calls
from tests.test_config import valid_data
from tests.test_label_workers import LABELS, register
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import catalog

SYNC_ALL = registry.entry("sync.all")
INTAKE_PLAYLIST = registry.entry("intake.playlist").handler_key
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
    resolved = _install(tmp_path, monkeypatch, "slim")
    (resolved.library.root / "db").mkdir(parents=True, exist_ok=True)
    yield resolved
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
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, passed = drive(["--run", run_id, *_verb(exported)])
    return run_id, code, passed


# 1. The declarations the composition rests on


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


def test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing():
    """U109: a source ``sync all`` leaves to another verb names one the registry agrees with.

    The verb shares the source's module and is the command printed; it holds no handler key.
    """
    guided = [spec for spec in sources.SPECS if spec.guided_by is not None]
    assert [spec.source_id for spec in guided] == ["labels"]
    for spec in guided:
        owner = registry.entry(spec.guided_by)
        assert owner.landed, owner.name
        assert owner.module_id == spec.module_id, owner.name
        assert spec.handler_key is None and spec.inbound_key is None, spec.source_id
        assert spec.source_id not in sync_cli.PLANNERS
        assert spec.command() == "crate " + " ".join(owner.name.split(".")), spec.command()
    assert dict((s.source_id, s.command()) for s in guided) == {"labels": "crate label sync"}


def test_no_path_creates_a_job_under_sync_all():
    """The registry and the composer's own module both say no ``enqueue`` (R-203)."""
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


# 2. A full pass


def test_a_full_pass_queues_each_source_under_its_own_key_with_one_run(
    installed, exported
):
    del installed
    # LABELS ARE REGISTERED AND STILL NOT SWEPT (U109), so favourites queues alone.
    register(*LABELS[:2])
    run_id, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "ok"

    queued = {job.handler_key: job for job in _jobs()}
    assert set(queued) == {"sync.favorites"}
    assert {job.payload["run_id"] for job in queued.values()} == {run_id}, (
        "every source in one pass must share one intake run, or each worker "
        "writes its own intake file and R29 is broken"
    )
    _, resolved = favorites_cli.resolve_sweep(str(exported), None)
    assert _items(queued["sync.favorites"].job_id) == list(resolved.track_ids)
    assert resolved.track_ids, "the fixture's favourites playlist is empty"

    summary = passed["data"]["summary"]
    assert summary["queued"] == 1
    assert {(j["source"], j["job_id"], j["handler_key"]) for j in summary["jobs"]} == {
        (job.payload["source_id"], job.job_id, key) for key, job in queued.items()
    }
    # PLAYLISTS IS CORE, so every pass names it, and with no provider session
    # stored it refuses for itself.
    assert summary["not_queued"] == {"playlists": "credential-missing"}
    # A FAVOURITES JOB IS NOT AN INTAKE JOB, so the pass names no
    # ``intake missing --run``, which would find nothing to list.
    assert summary["next"] is None
    assert "sync.next" not in {c["key"] for c in passed["data"]["checks"]}


def test_the_gate_refusal_has_queued_nothing_and_says_what_would_be(
    installed, exported
):
    """PLAN, ASK, QUEUE: a source queued before the question would be queued again by the answer."""
    del installed
    register(LABELS[0])
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    assert _jobs() == []
    shown = refused["cause"]["detail"]["shown"]
    assert shown["queued"] == []
    assert shown["would_queue"] == ["favorites"]


def test_the_gate_asks_over_the_digest_sync_favorites_itself_offers(
    installed, exported
):
    """Read off both verbs' run records, so what each verb offered is compared, not a function with itself."""
    del installed
    _, composed = drive(_verb(exported))
    _, alone = drive(["sync", "favorites", "--export", str(exported)])
    offered = gates.load(composed["run_id"]).offers[CONFIRM]
    assert offered == gates.load(alone["run_id"]).offers[sync_cli.FAVORITES_CONFIRM]


def _written_days_ago(exported: Path, days: float) -> datetime:
    moment = datetime.now(timezone.utc).timestamp() - days * 86_400
    os.utime(exported, (moment, moment))
    return datetime.fromtimestamp(exported.stat().st_mtime, tz=timezone.utc)


def test_the_composed_gate_names_the_exports_date_beside_what_would_queue(
    installed, exported
):
    """R-227: the pass builds its own favourites plan, so the export's date must still show beside its block."""
    del installed
    written = _written_days_ago(exported, 30)
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["would_queue"] == ["favorites"]
    assert shown["export"]["written"] == (
        written.astimezone().replace(microsecond=0).isoformat()
    )
    assert "Export the collection again" in shown["export"]["warning"]
    assert shown["export"]["age_days"] == 30
    assert shown["export"]["freshness"] == "stale"


def test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers(installed, exported):
    """R-693: the composed gate lists the favourites the sweep would heart back, as the favourites gate does."""
    del installed
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    shown = refused["cause"]["detail"]["shown"]
    _exported, resolved = favorites_cli.resolve_sweep(str(exported), None)
    assert shown["items"] == list(resolved.track_ids)
    assert shown["items"]
    assert shown["count"] == len(resolved.track_ids)
    assert shown["playlist"] == resolved.key
    assert shown["export path"] == str(exported)
    assert shown["digest"] == favorites_cli.sweep_digest(exported, resolved)
    assert shown["would_queue"] == ["favorites"]


def test_a_pass_that_queued_over_an_old_export_warns_and_still_queues(
    installed, exported
):
    """The confirmed favourites job carries each pass to the report, not the warningless refusal."""
    del installed
    written = _written_days_ago(exported, 30)
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    stale = [w for w in passed["warnings"] if w["code"] == "outbound-export-stale"]
    assert len(stale) == 1, passed["warnings"]
    assert written.astimezone().date().isoformat() in stale[0]["message"]
    assert "sync.favorites" in {job.handler_key for job in _jobs()}, (
        "a stale export refuses nothing"
    )


def test_the_composed_gate_judges_against_the_configured_limit(installed, exported):
    """A month old export is within a sixty day limit, and the block says whose number that was."""
    del installed
    _written_days_ago(exported, 30)
    current = config.load()
    config.save(
        replace(current, outbound=replace(current.outbound, export_stale_days=60))
    )
    config.reset_cache()
    _, refused = drive(_verb(exported))
    block = refused["cause"]["detail"]["shown"]["export"]
    assert (block["freshness"], block["stale_after_days"]) == ("within-limit", 60)
    assert "warning" not in block


def test_a_pass_over_a_recent_export_carries_no_age_warning(installed, exported):
    del installed
    _written_days_ago(exported, 2)
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert "sync.favorites" in {job.handler_key for job in _jobs()}
    codes = {w["code"] for w in passed["warnings"]}
    assert not codes & {"outbound-export-stale", "outbound-export-age-unknown"}
    assert codes, "the favourites standing warning proves the loop ran"


def test_aborting_the_confirmation_queues_no_favourites_job_and_says_so(
    installed, exported, monkeypatch
):
    """The account's hearts are what queue, so the pass reaches its report."""
    del installed
    bind_hearts(monkeypatch)
    _, code, passed = _confirmed(exported, option="abort")
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == [INTAKE_PLAYLIST]
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": sync_cli.DECLINED,
        "playlists": sync_cli.NOTHING_NEW,
    }
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "favorites"]
    assert check["status"] == "info" and "abort" in check["detail"]


def test_a_source_that_refuses_does_not_stop_the_other(installed, monkeypatch):
    """No export: favourites refuses and the new playlist still queues with no question, the only one being favourites'."""
    del installed
    bind_hearts(
        monkeypatch,
        FakeCatalogue(
            playlists={"pl-a": FakePagedPlaylist(_tracks("101"))},
            account=[_playlist("pl-a", "Warmup")],
        ),
    )
    passed = exited(drive(["sync", "all"]))
    assert [job.payload[intake_cli.SOURCE] for job in _jobs()] == ["pl-a"]
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
    }
    assert "sync-source-not-queued" in {w["code"] for w in passed["warnings"]}
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "favorites"]
    assert check["status"] == "fail"


def test_nothing_queued_because_every_source_refused_is_a_refusal(installed):
    """A pass that did nothing for a reason the person can fix says so."""
    del installed
    refused = failed(drive(["sync", "all"]))
    assert refused["cause"]["reason"] == "outbound-export-required"
    assert refused["cause"]["detail"]["sources"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
        "playlists": "credential-missing",
    }
    # THE GUIDED LINE RIDES THE REFUSAL TOO, as its LAST step since a refusal
    # prints no check rows; the first stays the refusing source's own fix.
    assert refused["cause"]["detail"]["sources"]["summary"]["guided"] == {
        "labels": "crate label sync"
    }
    steps = refused["cause"]["remediation"]["steps"]
    assert steps[-1] == (
        "labels are not swept by sync all; take them with: crate label sync"
    ), steps
    assert len(steps) >= 2, "the refusing source's own step was lost"
    assert _jobs() == []


# 2b. Labels are not swept here, and the pass says where they went (U109)


class NoLabelCalls(FakeCatalogue):
    """An account whose label catalogue (``artist_for``) must never be asked anything."""

    def artist_for(self, entry):
        raise AssertionError(f"sync all asked the label catalogue for {entry!r}")


def test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider(
    installed, exported, monkeypatch
):
    """Every label registered and a catalogue bound, still no labels job or listing.

    ``LabelSource`` is fenced too, so reaching the sweep's engine by any door fails.
    """
    del installed
    from cratekit.label import sweep

    def fenced(*args, **kwargs):
        raise AssertionError("sync all built a label sweep")

    register(*LABELS)
    monkeypatch.setattr(sweep, "LabelSource", fenced)
    bind_hearts(monkeypatch, NoLabelCalls(hearts=_hearts("301"), **_A_NEW_PLAYLIST))
    run_id, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    keys = sorted(job.handler_key for job in _jobs())
    assert keys == sorted([INTAKE_PLAYLIST, INTAKE_PLAYLIST, "sync.favorites"]), keys
    assert "sync.labels" not in keys
    summary = passed["data"]["summary"]
    assert "labels" not in summary["sources"]
    assert "labels" not in summary["not_queued"]
    assert summary["guided"] == {"labels": "crate label sync"}


def test_the_pass_names_the_guided_verb_in_one_check_row(installed, exported):
    del installed
    register(LABELS[0])
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    rows = [c for c in passed["data"]["checks"] if c["title"] == "labels"]
    assert len(rows) == 1, rows
    (row,) = rows
    assert row["key"] == "sync.labels" and row["status"] == "info"
    assert "crate label sync" in row["detail"]
    assert "not swept by sync all" in row["detail"]


def test_the_human_output_names_the_guided_verb(installed, monkeypatch):
    """The default output prints only the checks, so the row is where a routine sync is told."""
    del installed
    bind_hearts(monkeypatch)
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["sync", "all"], stdout=out, stderr=err)
    text = out.getvalue() + err.getvalue()
    assert code == int(ExitCode.OK), text
    (line,) = [one for one in text.splitlines() if "sync.labels" in one]
    assert "crate label sync" in line, line


def test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue(
    installed, exported
):
    """The gate shows labels in neither list and names their verb, since every favourites pass stops there first."""
    del installed
    register(LABELS[0])
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    shown = refused["cause"]["detail"]["shown"]
    assert "labels" not in shown["would_queue"]
    assert "labels" not in shown["not_queued"]
    assert shown["guided"] == {"labels": "crate label sync"}


def test_the_human_refusal_names_the_guided_verb(installed):
    """No export and no credential: nothing queues and the refusal says where label releases went."""
    del installed
    register(LABELS[0])
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["sync", "all"], stdout=out, stderr=err)
    text = out.getvalue() + err.getvalue()
    assert code != int(ExitCode.OK), text
    assert "take them with: crate label sync" in text, text


def test_a_profile_without_the_labels_module_names_no_guided_verb(slim, monkeypatch):
    """Slim does not switch the labels verb on, so it is not pointed at it."""
    del slim
    bind_hearts(monkeypatch, FakeCatalogue(**_A_NEW_PLAYLIST))
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["guided"] == {}
    assert "sync.labels" not in {c["key"] for c in passed["data"]["checks"]}


# 3. The slim profile, and the playlists source it runs alone (U64)


def _playlist(playlist_id: str, name: str, tracks: int | None = None) -> AccountPlaylist:
    return AccountPlaylist(playlist_id=playlist_id, name=name, tracks=tracks)


def bind_playlists(
    monkeypatch, *listed: tuple[AccountPlaylist, list[Track] | None]
) -> FakeCatalogue:
    """An account whose own playlists are ``listed``; ``None`` tracks cannot be resolved."""
    fake = FakeCatalogue(
        playlists={
            playlist.playlist_id: FakePagedPlaylist(tracks)
            for playlist, tracks in listed
            if tracks is not None
        },
        account=[playlist for playlist, _ in listed],
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def _tracks(*ids: str) -> list[Track]:
    return [Track(track_id, f"Artist {track_id}", f"Title {track_id}") for track_id in ids]


def _playlist_jobs() -> list[jobs.Job]:
    return [job for job in _jobs() if job.handler_key == INTAKE_PLAYLIST]


def _swept(installed_cfg: config.Config) -> tuple[str, ...] | None:
    mark = watermarks.WatermarkStore(installed_cfg).read(playlists.SOURCE_ID)
    return None if mark is None else mark.swept


def test_the_playlists_source_names_the_intake_worker_it_composes():
    (spec,) = [spec for spec in sources.SPECS if spec.source_id == playlists.SOURCE_ID]
    assert spec.handler_key == registry.entry("intake.playlist").handler_key
    assert spec.module_id is None, "playlists are core, so the slim profile runs them"


def test_a_slim_pass_with_no_provider_session_refuses_and_queues_nothing(slim):
    del slim
    refused = failed(drive(["sync", "all"]))
    assert refused["cause"]["reason"] == "credential-missing"
    assert _jobs() == []


def test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run(
    slim, monkeypatch
):
    """The brief's first scenario: three playlists, one carrying the swept prefix."""
    del slim
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101", "102")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
        (_playlist("pl-c", playlists.SWEPT_PREFIX + "Closing"), _tracks("301")),
    )
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "ok"

    queued = {job.payload[intake_cli.SOURCE]: job for job in _playlist_jobs()}
    assert set(queued) == {"pl-a", "pl-b"}
    assert {job.payload["run_id"] for job in queued.values()} == {passed["run_id"]}
    assert {job.payload["source_id"] for job in queued.values()} == {playlists.SOURCE_ID}
    assert _items(queued["pl-a"].job_id) == ["101", "102"]
    assert "pl-c" not in fake.playlists_asked_for, "a swept playlist was listed anyway"

    summary = passed["data"]["summary"]
    assert summary["queued"] == 2
    assert "playlists" not in summary["not_queued"]
    block = summary["playlists"]
    assert block["excluded"] == {
        "pl-c": {"reason": "already-swept", "name": playlists.SWEPT_PREFIX + "Closing"}
    }
    assert {row["playlist_id"] for row in block["queued"]} == {"pl-a", "pl-b"}
    assert block["mark"] == playlists.MARK_UNBOUND
    # STILL NO JOB UNDER ``sync.all``, read off the queue this pass filled.
    assert SYNC_ALL.handler_key not in {job.handler_key for job in _jobs()}


def test_a_playlist_with_no_tracks_queues_nothing_and_is_reported(slim, monkeypatch):
    """An empty playlist, by its count or by empty tracks under an unknown count, is never a silent success."""
    del slim
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Counted Empty", tracks=0), _tracks()),
        (_playlist("pl-b", "Listed Empty"), _tracks()),
    )
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "no_op"
    assert _jobs() == []
    summary = passed["data"]["summary"]
    assert summary["not_queued"] == {"playlists": sync_cli.NOTHING_NEW}
    assert {k: v["reason"] for k, v in summary["playlists"]["excluded"].items()} == {
        "pl-a": "empty",
        "pl-b": "empty",
    }
    assert fake.playlists_asked_for == ["pl-b"]
    (check,) = passed["data"]["checks"]
    assert check["status"] == "info"
    assert "nothing new" in check["detail"] and "2 empty" in check["detail"]
    assert _swept(config.load()) is None, "an empty sweep recorded a clean completion"


def test_an_account_with_no_playlists_is_reported_not_recorded(slim, monkeypatch):
    del slim
    bind_playlists(monkeypatch)
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "no_op"
    assert passed["data"]["summary"]["playlists"]["listed"] == 0
    assert _swept(config.load()) is None


def test_the_favourites_placeholders_are_left_to_the_favourites_source(slim, monkeypatch):
    """By the favourites source's own pattern, never a copied literal; the near names are swept."""
    del slim
    placeholder = favorites_cli.placeholder_name("2026-Q2")
    backlog = favorites_cli.placeholder_name(favorites_cli.BACKLOG)
    assert favorites_cli.PLACEHOLDER_NAME.fullmatch(placeholder)
    assert favorites_cli.PLACEHOLDER_NAME.fullmatch(backlog)
    near = [f"All {placeholder.split()[0]}", f"{placeholder} copy", f"{backlog} old"]
    assert not any(favorites_cli.PLACEHOLDER_NAME.fullmatch(name) for name in near)
    bind_playlists(
        monkeypatch,
        (_playlist("pl-q", placeholder), _tracks("101")),
        (_playlist("pl-backlog", backlog), _tracks("102")),
        (_playlist("pl-all", near[0]), _tracks("201")),
        (_playlist("pl-copy", near[1]), _tracks("301")),
        (_playlist("pl-old", near[2]), _tracks("401")),
    )
    passed = exited(drive(["sync", "all"]))
    assert {job.payload[intake_cli.SOURCE] for job in _playlist_jobs()} == {
        "pl-all",
        "pl-copy",
        "pl-old",
    }
    excluded = passed["data"]["summary"]["playlists"]["excluded"]
    assert {excluded[k]["reason"] for k in ("pl-q", "pl-backlog")} == {"favorites-placeholder"}


def test_the_label_batch_debris_is_not_queued_as_intake(slim, monkeypatch):
    """R-361: two label batch playlists and a person's of that ending are not listed or queued."""
    del slim
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-sol-1", "Sol Selectas LIBRARY"), _tracks("101", "102")),
        (_playlist("pl-sol-2", "Sol Selectas LIBRARY"), _tracks("103")),
        (_playlist("pl-night", "My Night LIBRARY"), _tracks("201")),
        (_playlist("pl-swept", playlists.SWEPT_PREFIX + "Colorize LIBRARY"), _tracks("301")),
        (_playlist("pl-2026", "Colorize 2026"), _tracks("401")),
        (_playlist("pl-title", "Colorize Library"), _tracks("501")),
    )
    passed = exited(drive(["sync", "all"]))
    assert {job.payload[intake_cli.SOURCE] for job in _playlist_jobs()} == {"pl-2026", "pl-title"}
    assert set(fake.playlists_asked_for) == {"pl-2026", "pl-title"}, (
        "a debris playlist was listed track by track anyway"
    )
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"] == {
        "pl-sol-1": {"reason": "label-debris", "name": "Sol Selectas LIBRARY"},
        "pl-sol-2": {"reason": "label-debris", "name": "Sol Selectas LIBRARY"},
        "pl-night": {"reason": "label-debris", "name": "My Night LIBRARY"},
        "pl-swept": {
            "reason": "already-swept",
            "name": playlists.SWEPT_PREFIX + "Colorize LIBRARY",
        },
    }
    assert _swept(config.load()) is None, "excluding debris recorded a clean completion"


def test_a_pass_that_finds_only_debris_says_so_on_the_check(slim, monkeypatch):
    """The nothing new tally names the reason, so label batch leavings read as counted, not skipped."""
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Rebellion LIBRARY"), _tracks("101")),
        (_playlist("pl-b", "Do Not Sit On The Furniture LIBRARY"), _tracks("102")),
    )
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "no_op"
    assert _jobs() == []
    summary = passed["data"]["summary"]
    assert summary["not_queued"] == {"playlists": sync_cli.NOTHING_NEW}
    (check,) = passed["data"]["checks"]
    assert check["status"] == "info"
    assert "2 label-debris" in check["detail"], check["detail"]


def test_the_cursor_records_ids_only_once_a_job_succeeds(slim, monkeypatch):
    """Queued is not swept, an open job is not queued twice, and a succeeded job records the identifier, never the title."""
    cfg = slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup Title"), _tracks("101")),
        (_playlist("pl-b", "Peak Title"), _tracks("201")),
    )
    exited(drive(["sync", "all"]))
    assert _swept(cfg) is None, "queueing a playlist recorded it as swept"

    again = exited(drive(["sync", "all"]))
    assert len(_playlist_jobs()) == 2, "an open job's playlist was queued a second time"
    assert {k: v["reason"] for k, v in again["data"]["summary"]["playlists"]["excluded"].items()} == {
        "pl-a": "in-flight",
        "pl-b": "in-flight",
    }

    (job_a,) = [j for j in _playlist_jobs() if j.payload[intake_cli.SOURCE] == "pl-a"]
    resumed = exited(drive(cli_jobs.argv_for(job_a)))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)

    third = exited(drive(["sync", "all"]))
    block = third["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert {k: v["reason"] for k, v in block["excluded"].items()} == {
        "pl-a": "recorded",
        "pl-b": "in-flight",
    }
    assert _swept(cfg) == ("pl-a",)
    document = watermarks.WatermarkStore(cfg).path.read_text(encoding="utf-8")
    assert "Warmup Title" not in document and "Peak Title" not in document


def test_a_failed_job_is_not_recorded_and_its_playlist_is_offered_again(slim, monkeypatch):
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    drive(["sync", "all"])
    (job,) = _playlist_jobs()
    with jobs.open_store() as store:
        jobs.transition(store, job.job_id, jobs.JobState.FAILED)
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["recorded_now"] == []
    assert _swept(cfg) is None
    assert len(_playlist_jobs()) == 2


def _by_hand(store, cfg, reference: str, *, handler_key: str = INTAKE_PLAYLIST) -> jobs.Job:
    """A job queued the way ``crate intake playlist`` queues one: no run, no source."""
    return intake_cli.queue_playlist(
        store,
        cfg,
        handler_key=handler_key,
        reference=reference,
        tracks={"101": {"title": "Title 101"}},
    )


def test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass(slim, monkeypatch):
    """R-382: after ``crate intake playlist`` runs to done, ``crate sync all`` records the playlist, not queuing it again."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    exited(drive(["intake", "playlist", "pl-a"]))
    (job,) = _playlist_jobs()
    assert "source_id" not in job.payload, "the producer is a job with no source id"
    code, resumed = drive(cli_jobs.argv_for(job))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["queued"] == []
    assert block["recorded_now"] == ["pl-a"]
    assert block["excluded"]["pl-a"]["reason"] == "recorded"
    assert _swept(cfg) == ("pl-a",)
    assert len(_playlist_jobs()) == 1


def test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued(slim, monkeypatch):
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    exited(drive(["intake", "playlist", "pl-a"]))
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["queued"] == []
    assert block["excluded"]["pl-a"]["reason"] == "in-flight"
    assert len(_playlist_jobs()) == 1, "an open hand queued job's playlist was queued again"
    assert _swept(cfg) is None


@pytest.mark.parametrize("ended", [jobs.JobState.FAILED, jobs.JobState.CANCELLED])
def test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded(
    slim, monkeypatch, ended
):
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        job = _by_hand(store, cfg, "pl-a")
        jobs.transition(store, job.job_id, ended)
    passed = exited(drive(["sync", "all"]))
    assert [row["playlist_id"] for row in passed["data"]["summary"]["playlists"]["queued"]] == ["pl-a"]
    assert _swept(cfg) is None


def test_a_set_intake_naming_the_playlist_is_not_a_playlist_intake(slim, monkeypatch):
    """``intake.set`` carries a source too, and is not what the cursor records."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    set_key = registry.entry("intake.set").handler_key
    assert set_key != INTAKE_PLAYLIST
    with jobs.open_store() as store:
        finished = _by_hand(store, cfg, "pl-a", handler_key=set_key)
        jobs.transition(store, finished.job_id, jobs.JobState.SUCCEEDED)
        _by_hand(store, cfg, "pl-a", handler_key=set_key)  # and one still open
    passed = exited(drive(["sync", "all"]))
    assert [row["playlist_id"] for row in passed["data"]["summary"]["playlists"]["queued"]] == ["pl-a"]
    assert _swept(cfg) is None


def test_two_succeeded_jobs_for_one_playlist_record_it_once(slim, monkeypatch):
    """One by hand, one a pass queued, both done, one identifier in the cursor."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        hand = _by_hand(store, cfg, "pl-a")
        swept = intake_cli.queue_playlist(
            store,
            cfg,
            handler_key=INTAKE_PLAYLIST,
            reference="pl-a",
            tracks={"101": {"title": "Title 101"}},
            run_id="an-earlier-run",
            source_id=playlists.SOURCE_ID,
        )
        for job in (hand, swept):
            jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["recorded_now"] == ["pl-a"]
    assert _swept(cfg) == ("pl-a",)


PLAYLIST_UUID = "0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1"


@pytest.mark.parametrize(
    "typed",
    [
        f"https://tidal.com/browse/playlist/{PLAYLIST_UUID}",
        f"https://listen.tidal.com/playlist/{PLAYLIST_UUID}?u",
        PLAYLIST_UUID.upper(),
    ],
)
def test_a_playlist_typed_as_a_url_by_hand_records_its_identifier(slim, monkeypatch, typed):
    """The standalone verb stores what was TYPED, so a verbatim URL in the cursor would be offered again."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist(PLAYLIST_UUID, "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        job = _by_hand(store, cfg, typed)
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["queued"] == []
    assert block["excluded"][PLAYLIST_UUID]["reason"] == "recorded"
    assert _swept(cfg) == (PLAYLIST_UUID,)


def test_a_playlist_typed_as_a_url_and_still_open_is_in_flight(slim, monkeypatch):
    cfg = slim
    bind_playlists(monkeypatch, (_playlist(PLAYLIST_UUID, "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        _by_hand(store, cfg, f"https://tidal.com/playlist/{PLAYLIST_UUID}")
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["queued"] == []
    assert block["excluded"][PLAYLIST_UUID]["reason"] == "in-flight"


def test_a_pass_queued_job_records_the_listing_identifier_verbatim(slim, monkeypatch):
    """The parser lowercases input, so a pass's job is recorded exactly as listed, as the next listing compares."""
    cfg = slim
    listed = PLAYLIST_UUID.upper()
    bind_playlists(monkeypatch, (_playlist(listed, "Warmup"), _tracks("101")))
    drive(["sync", "all"])
    (job,) = _playlist_jobs()
    with jobs.open_store() as store:
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["excluded"][listed]["reason"] == "recorded"
    assert _swept(cfg) == (listed,)


def test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded(slim, monkeypatch):
    """``marking_sweep`` reads :func:`playlists.reconcile`'s policy, so a playlist is recorded to a mark taken before it."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        job = _by_hand(store, cfg, "pl-a")
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
        sweep = playlists.marking_sweep(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sweep.recorded == frozenset({"pl-a"})
    assert _swept(cfg) is None, "a mark moved the cursor"


def test_a_hearts_intake_is_not_recorded_as_a_playlist(slim, monkeypatch):
    """Both producers of a hearts job: the reserved reference, and the favourites source's with its source id."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    with jobs.open_store() as store:
        by_verb = _by_hand(store, cfg, "FAVORITES")
        by_source = intake_cli.queue_playlist(
            store,
            cfg,
            handler_key=INTAKE_PLAYLIST,
            reference=intake_cli.FAVORITES,
            tracks={"101": {"title": "Title 101"}},
            run_id="an-earlier-run",
            source_id=intake_cli.FAVORITES_SOURCE_ID,
        )
        for job in (by_verb, by_source):
            jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["recorded_now"] == []
    assert _swept(cfg) is None


def test_another_librarys_finished_job_is_not_this_librarys_sweep(slim, monkeypatch):
    """The queue is per installation and the cursor per library, so another library's swept playlist is new here."""
    import dataclasses

    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="0000-0000")
    )
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store,
            elsewhere,
            handler_key=INTAKE_PLAYLIST,
            reference="pl-a",
            tracks={"101": {"title": "Title 101"}},
            run_id="another-run",
            source_id=playlists.SOURCE_ID,
        )
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["recorded_now"] == []
    assert _swept(cfg) is None
    assert [row["playlist_id"] for row in passed["data"]["summary"]["playlists"]["queued"]] == ["pl-a"]


def test_an_unreadable_playlist_is_reported_and_the_rest_still_queue(slim, monkeypatch):
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-gone", "Deleted Meanwhile"), None),
        (_playlist("pl-a", "Warmup"), _tracks("101")),
    )
    passed = exited(drive(["sync", "all"]))
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"]["pl-gone"]["reason"] == "unreadable"
    assert "pl-gone" in block["unreadable"]
    assert "sync-playlists-unreadable" in {w["code"] for w in passed["warnings"]}


def test_an_account_listing_that_fails_is_a_refusal_not_an_empty_account(slim, monkeypatch):
    """R-135 for this source: the slim pass has nothing else, so it refuses."""
    del slim

    class Unlistable(FakeCatalogue):
        def account_playlists(self):
            raise RuntimeError("the provider stopped answering")

    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Unlistable()))
    refused = failed(drive(["sync", "all"]))
    assert refused["cause"]["reason"] == "sync-source-lookups-failed"
    assert _jobs() == []


def test_a_refusal_part_way_through_the_playlists_keeps_the_filed_ones_named(
    slim, monkeypatch
):
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    real = intake_cli.queue_playlist

    def second_refuses(store, cfg, **kwargs):
        if kwargs["reference"] == "pl-b":
            from cratekit.core.cause import refuse

            raise refuse("internal-error", "the queue refused the second playlist")
        return real(store, cfg, **kwargs)

    monkeypatch.setattr(intake_cli, "queue_playlist", second_refuses)
    passed = exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    summary = passed["data"]["summary"]
    assert [j["job_id"] for j in summary["jobs"]] == [job.job_id]
    assert summary["not_queued"]["playlists"] == "internal-error"
    assert [row["job_id"] for row in summary["playlists"]["queued"]] == [job.job_id]
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "playlists"]
    assert check["status"] == "fail" and job.job_id in check["detail"]


# 3b. The deferred mark, R-358 code half, each driven through a real pass


def _recording_pass(cfg, fake) -> playlists.Sweep:
    """Queue ``pl-a``, finish its job, and plan the pass ONCE: a second plan records nothing."""
    exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    resumed = exited(drive(cli_jobs.argv_for(job)))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    with jobs.open_store() as store:
        sweep = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sweep.recorded_now == ("pl-a",), sweep.recorded_now
    return sweep


class _Taker:
    """The record ``mark_swept`` hands each mark to (U242); ``fail_on`` names takes that raise."""

    def __init__(self, cfg: config.Config, *, fail_on=()) -> None:
        self.cfg = cfg
        self.fail_on = frozenset(fail_on)
        self.taken: list[tuple[str, str]] = []

    def __call__(self, identity: str, name: str) -> None:
        from cratekit.sync import mark_record

        if identity in self.fail_on:
            raise RuntimeError(f"interrupted take for {identity}")
        mark_record.MarkRecord(self.cfg).take(
            [mark_record.Taken(identity, name, "a-pass", mark_record.BY_PASS, "2026-11-12T00:00:00Z")]
        )
        self.taken.append((identity, name))


def _written(tmp_path: Path) -> Path:
    """The pass's local output, written as an importable file."""
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")
    return output


def test_a_mark_without_a_real_importable_file_renames_nothing(slim, monkeypatch, tmp_path):
    """Both halves of the file rule; the file is checked before the recheck reads the account."""
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    account = _Taker(slim)
    output = tmp_path / "run-1_synced.xml"
    listings = fake.account_listings

    with pytest.raises(CratekitError) as absent:
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert absent.value.cause.reason == "sync-marks-blocked"

    output.write_text("", encoding="utf-8")
    with pytest.raises(CratekitError) as empty:
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert empty.value.cause.reason == "sync-marks-blocked"

    assert account.taken == []
    assert fake.account_listings == listings, "the recheck read ran before the file check"


def test_a_mark_after_a_real_importable_file_takes_the_recorded_playlist(
    slim, monkeypatch, tmp_path
):
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    account = _Taker(slim)
    output = _written(tmp_path)
    listings = fake.account_listings

    marked = playlists.mark_swept(sweep, fake, account, local_output=output)

    assert marked == ("pl-a",)
    assert account.taken == [("pl-a", "Warmup")]
    assert "pl-a" in playlists.taken_ids(slim), "held as taken, no title written (U242)"
    assert fake.account_listings == listings + 1, "the recheck was not a second read"


@pytest.mark.parametrize(
    "now", [[_playlist("pl-a", "Warmup Rework")], []], ids=["renamed", "gone"]
)
def test_a_playlist_renamed_or_gone_on_the_account_since_the_plan_is_left_alone(
    slim, monkeypatch, tmp_path, now
):
    """The recheck stops a prefix landing on a playlist renamed or gone since the pass swept it."""
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    fake.account = now
    account = _Taker(slim)
    output = _written(tmp_path)

    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ()
    assert account.taken == []


def test_a_recorded_playlist_the_pass_never_listed_is_not_pending_at_all(
    slim, monkeypatch
):
    """On ``pending_marks``, since ``mark_swept``'s recheck would refuse a nameless mark anyway."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    _recording_pass(cfg, fake)

    fake.account = []
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert later.listed == ()
    assert later.recorded == frozenset({"pl-a"})
    assert playlists.pending_marks(later) == ()


def test_a_recorded_debris_playlist_is_not_pending_at_all():
    """R-361 on ``pending_marks``: a ` LIBRARY` name in the cursor is never prefixed."""
    sweep = playlists.Sweep(
        listed=(
            _playlist("pl-sol", "Sol Selectas LIBRARY"),
            _playlist("pl-swept", playlists.SWEPT_PREFIX + "Colorize LIBRARY"),
            _playlist("pl-title", "Colorize Library"),
            _playlist("pl-2026", "Colorize 2026"),
        ),
        recorded=frozenset({"pl-sol", "pl-swept", "pl-title", "pl-2026"}),
    )
    assert [mark.target_id for mark in playlists.pending_marks(sweep)] == ["pl-2026", "pl-title"]
    # ``only`` narrows and never widens: naming the debris does not mark it.
    assert playlists.pending_marks(sweep, only=frozenset({"pl-sol"})) == ()


def test_a_playlist_the_source_system_already_prefixed_is_not_prefixed_twice(
    slim, monkeypatch, tmp_path
):
    """DJ_tools may sweep the playlist before this pass records it; marking again would double the prefix."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    fake.account = [_playlist("pl-a", playlists.SWEPT_PREFIX + "Warmup")]
    with jobs.open_store() as store:
        sweep = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sweep.recorded_now == ("pl-a",)

    account = _Taker(slim)
    output = _written(tmp_path)

    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ()
    assert account.taken == []


def test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass(
    slim, monkeypatch, tmp_path
):
    """The cursor moves before marking, so a refused mark must not leave a recorded playlist never prefixed."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(cfg, fake)
    account = _Taker(slim)
    output = tmp_path / "run-1_synced.xml"

    with pytest.raises(CratekitError):
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert account.taken == []

    # The next pass records nothing new and still owes the mark.
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert later.recorded_now == ()
    assert later.excluded["pl-a"] == playlists.Excluded.RECORDED
    assert [mark.target_id for mark in playlists.pending_marks(later)] == ["pl-a"]

    output.write_text("<COLLECTION/>", encoding="utf-8")
    assert playlists.mark_swept(later, fake, account, local_output=output) == ("pl-a",)
    assert account.taken == [("pl-a", "Warmup")]


def test_a_mark_that_landed_is_not_owed_a_second_time(slim, monkeypatch, tmp_path):
    """What ends the retrying is the taken entry, read back off the record."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(cfg, fake)
    account = _Taker(slim)
    output = _written(tmp_path)
    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ("pl-a",)

    # THE RECORD, NOT THE TITLE (U242): the account still lists it unprefixed.
    assert playlists.taken_ids(cfg) == frozenset({"pl-a"})
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert later.listed[0].name == "Warmup"
    assert playlists.pending_marks(later) == ()
    assert playlists.mark_swept(later, fake, account, local_output=output) == ()
    assert len(account.taken) == 1


def test_a_rename_that_fails_mid_batch_still_names_the_ones_that_landed(
    slim, monkeypatch, tmp_path
):
    """Each rename is its own remote write; a caller naming what reached the account passes a list, as ``queue`` does."""
    cfg = slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    exited(drive(["sync", "all"]))
    for job in _playlist_jobs():
        code, resumed = drive(cli_jobs.argv_for(job))
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    with jobs.open_store() as store:
        sweep = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sorted(sweep.recorded) == ["pl-a", "pl-b"]

    account = _Taker(cfg, fail_on={"pl-b"})
    output = _written(tmp_path)
    landed: list[str] = []

    with pytest.raises(RuntimeError):
        playlists.mark_swept(
            sweep, fake, account, local_output=output, applied=landed
        )
    assert playlists.taken_ids(cfg) == frozenset({"pl-a"})

    assert landed == ["pl-a"]
    assert account.taken == [("pl-a", "Warmup")]


def test_the_current_intake_path_marks_nothing_and_still_reports_unbound(slim, monkeypatch):
    """A recorded playlist still reports the mark unbound, since the worker acquires nothing to wait on."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    drive(["sync", "all"])
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    third = exited(drive(["sync", "all"]))
    block = third["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert block["mark"] == playlists.MARK_UNBOUND
    assert block["marked"] == []
    assert _swept(cfg) == ("pl-a",)


# R-359: swept means resolved, not acquired, and both surfaces say so. The
# literal is spelled out so a changed token fails rather than agreeing with itself.


def _recorded_over_missing(monkeypatch) -> None:
    """Drive the producer until the next pass records a playlist the library owns none of."""
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101", "102")))
    exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    resumed = exited(drive(cli_jobs.argv_for(job)))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    progress = resumed["data"]["progress"]
    assert (progress["missing"], progress["acquired"]) == (2, 0), progress


def _run_human(argv: list[str]) -> tuple[int, str]:
    """The default human mode through the real dispatcher; ``drive`` always asks for json."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue()


def _playlists_line(text: str) -> str:
    (line,) = [row for row in text.splitlines() if "sync.playlists:" in row]
    return line


def test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired(
    slim, monkeypatch
):
    cfg = slim
    _recorded_over_missing(monkeypatch)
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert _swept(cfg) == ("pl-a",)
    assert block["swept_means"] == "resolved-not-acquired"


def test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired(
    slim, monkeypatch
):
    del slim
    _recorded_over_missing(monkeypatch)
    text = exited(_run_human(["sync", "all"]))
    line = _playlists_line(text)
    assert "1 recorded" in line, text
    assert "resolved" in line and "not acquired" in line, text
    lowered = text.lower()
    for claim in ("downloaded", "library holds", "in your library", "acquired the"):
        assert claim not in lowered, text


# 3d. The pass names its next step, the command that lists its intake jobs (U73)


def test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb(
    slim, monkeypatch
):
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    text = exited(_run_human(["sync", "all"]))
    (run_id,) = {job.payload["run_id"] for job in _playlist_jobs()}
    (line,) = [row for row in text.splitlines() if "sync.next:" in row]
    assert f"crate intake missing --run {run_id}" in line, text
    assert "2 intake job(s)" in line, text


def test_the_json_summary_carries_the_same_command(slim, monkeypatch):
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["next"] == f"crate intake missing --run {passed['run_id']}"


def test_a_pass_that_queued_no_intake_job_names_no_run_verb(slim, monkeypatch):
    """``intake missing --run`` refuses a run with no intake job, so it is not named."""
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Counted Empty", tracks=0), _tracks()))
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["next"] is None
    assert "sync.next" not in {c["key"] for c in passed["data"]["checks"]}


def test_a_pass_through_to_one_list_holds_a_shared_track_once_with_both_playlists(
    slim, monkeypatch
):
    """Two playlists sharing a track, both jobs run, then the named verb: one list, one shared row, both in its provenance."""
    import json

    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101", "102")),
        (_playlist("pl-b", "Peak"), _tracks("102", "201")),
    )
    passed = exited(drive(["sync", "all"]))
    for job in _playlist_jobs():
        resumed = exited(drive(cli_jobs.argv_for(job)))
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    command = passed["data"]["summary"]["next"].split()
    assert command[:3] == ["crate", "intake", "missing"]
    listed = exited(drive(command[1:]))
    summary = listed["data"]["summary"]
    body = json.loads(Path(summary["list"]).read_text())
    assert sorted(track["id"] for track in body["tracks"]) == ["101", "102", "201"]
    rows = json.loads(Path(summary["manifest"]).read_text())["rows"]
    assert sorted(rows["102"]["source_refs"]) == ["pl-a", "pl-b"]
    assert (rows["101"]["source_ref"], rows["201"]["source_ref"]) == ("pl-a", "pl-b")


def test_the_block_says_what_swept_means_whatever_the_pass_found():
    """On the pure path too, so an account with nothing recorded leaves no word undefined."""
    block = playlists.report(playlists.Sweep(), [])
    assert block["swept_means"] == "resolved-not-acquired"
    assert "not acquired" in (playlists.said(block) or "")
    assert playlists.said({}) is None, "a block carrying no token was given words"


def test_a_pass_renames_nothing_even_over_a_recorded_playlist_with_its_file_landed(
    slim, monkeypatch
):
    """R-397: an ungated pass whose marks are all due renames nothing on the account."""
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    _recording_pass(slim, fake)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    (Path(slim.library.root) / "pass_synced_inboxed.xml").write_text(
        "<COLLECTION/>", encoding="utf-8"
    )
    passed = exited(drive(["sync", "all"]))
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"]["pl-a"]["reason"] == "recorded"
    assert (block["mark"], block["marked"]) == (playlists.MARK_UNBOUND, [])
    assert account.renamed == []


def test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran():
    """Two different facts, and an empty list is not what separates them."""
    sweep = playlists.Sweep()
    never = playlists.report(sweep, [])
    ran = playlists.report(sweep, [], marked=())
    assert (never["mark"], never["marked"]) == (playlists.MARK_UNBOUND, [])
    assert (ran["mark"], ran["marked"]) == (playlists.MARK_APPLIED, [])
    assert playlists.report(sweep, [], marked=("pl-a",))["marked"] == ["pl-a"]


def test_the_sync_package_defines_no_remove_write():
    """The outbound suite's banned account writes, imported not copied, banned over ``sync``."""
    from tests.modules.test_outbound import FORBIDDEN_WRITE_NAMES

    defined: set[str] = set()
    for path in SRC.parent.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined.add(node.name)
    assert defined, "the scan read no functions at all"
    assert sorted(defined & FORBIDDEN_WRITE_NAMES) == []


# 4. What the pass queued, run by the workers that already exist


def test_the_jobs_a_pass_queues_run_to_done_through_the_existing_workers(
    installed, exported, monkeypatch
):
    """Driven through ``argv_for``, so the favourites resume loads ``hand_off``'s run and one run per verb is under test."""
    del installed
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2))
    bind_account(monkeypatch, account)
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed

    for job in _jobs():
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), (job.handler_key, resumed)
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), job.handler_key
    assert sorted(account.hearted) == ["tid-1", "tid-2"]
    assert {job.handler_key for job in _jobs()} == {"sync.favorites"}


def test_the_favourites_job_carries_a_gate_run_its_own_verb_owns(installed, exported):
    del installed
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


# 5. The hand off copies an answer and never supplies one


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
    # The cloud gate offers neither option nor digest, so both layers refuse;
    # the export gate has a digest but no "sync", so only the option layer does.
    ids=["undeclared", "offers-neither", "option-not-offered"],
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
    """Favourites queues first in its own transaction, so a later playlists refusal must say it filed."""
    del installed
    from cratekit.core.cause import refuse

    def refusing(*args, **kwargs):
        raise refuse("internal-error", "the queue refused this source")

    bind_hearts(
        monkeypatch,
        FakeCatalogue(
            playlists={"pl-a": FakePagedPlaylist(_tracks("101"))},
            account=[_playlist("pl-a", "Warmup")],
        ),
    )
    monkeypatch.setattr(playlists, "queue", refusing)
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    (job,) = _jobs()
    assert job.handler_key == "sync.favorites"
    summary = passed["data"]["summary"]
    assert [j["job_id"] for j in summary["jobs"]] == [job.job_id]
    assert summary["not_queued"]["playlists"] == "internal-error"
    assert "sync-source-not-queued" in {w["code"] for w in passed["warnings"]}


def test_the_composed_pass_carries_the_favourites_verb_standing_warning(
    installed, exported
):
    """R-424 survives the composition; the message is read off the verb's module, not typed."""
    del installed
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.favorites"]
    warning = next(
        w
        for w in passed["warnings"]
        if w["code"] == favorites_cli.LOCAL_WRITE_WARNING["code"]
    )
    assert warning["message"] == favorites_cli.LOCAL_WRITE_WARNING["message"]


def test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached(
    installed, exported, monkeypatch
):
    """A declined source's standing warning stays out of the envelope.

    The hearts are listed so the pass reaches the warnings loop (mutation row ``D2_filed_filter``).
    """
    del installed
    bind_hearts(monkeypatch)
    _, code, passed = _confirmed(exported, option="abort")
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == [INTAKE_PLAYLIST]
    assert passed["data"]["summary"]["not_queued"]["favorites"] == sync_cli.DECLINED
    codes = {w["code"] for w in passed["warnings"]}
    assert favorites_cli.LOCAL_WRITE_WARNING["code"] not in codes, passed["warnings"]


def test_a_hand_off_to_a_gate_that_compares_no_digest_refuses(installed, monkeypatch):
    """The digest layer alone: the real favourites entry, its confirm's digest source removed."""
    import dataclasses

    del installed
    owner = registry.entry("sync.favorites")
    blind = tuple(
        dataclasses.replace(g, digest_source=None)
        if g.name == "sync.favorites.confirm"
        else g
        for g in owner.gates
    )
    monkeypatch.setattr(
        registry,
        "_BY_NAME",
        {**dict(registry._BY_NAME), owner.name: dataclasses.replace(owner, gates=blind)},
    )
    (spec,) = SYNC_ALL.gates
    asked = _gates()
    asked.state.decisions[spec.name] = gates.Decision("sync", "a-person", "now", "d1")
    with pytest.raises(CratekitError):
        asked.hand_off(spec, verb="sync.favorites", gate="sync.favorites.confirm")


# 6. The hearts listing, favourites' read only half (U74)


def _hearts(*ids: str) -> list[Track]:
    return [Track(track_id, f"Heart Artist {track_id}", f"Heart {track_id}") for track_id in ids]


def bind_hearts(monkeypatch, fake: FakeCatalogue | None = None) -> FakeCatalogue:
    """An account with three hearts and no playlists of its own, unless given one."""
    fake = fake if fake is not None else FakeCatalogue(hearts=_hearts("301", "302", "303"))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


#: An account playlist the pass has never seen, so the playlists source queues
#: one job and carries the pass to its report when the hearts queue nothing.
_A_NEW_PLAYLIST = {
    "playlists": {"pl-a": FakePagedPlaylist([Track("101", "Artist 101", "Title 101")])},
    "account": [AccountPlaylist(playlist_id="pl-a", name="Warmup", tracks=None)],
}


def _hearts_jobs() -> list[jobs.Job]:
    return [
        job
        for job in _playlist_jobs()
        if job.payload.get("source_id") == intake_cli.FAVORITES_SOURCE_ID
    ]


def _pass(envelope: dict) -> dict:
    """The pass's report, whether it ended OK or as the refusal that carries it."""
    if envelope.get("cause"):
        return envelope["cause"]["detail"]["sources"]
    return envelope["data"]


def _inbound(envelope: dict) -> dict:
    return _pass(envelope)["summary"]["favorites"]["inbound"]


def _inbound_check(envelope: dict) -> dict:
    (check,) = [c for c in _pass(envelope)["checks"] if c["key"] == "sync.favorites.inbound"]
    return check


def test_only_favourites_declares_a_read_half_and_its_key_is_a_bound_intake_key():
    """The inbound key must be an intake key, or ``intake missing --run`` would not list what it found."""
    declared = {spec.source_id: spec.inbound_key for spec in sources.SPECS if spec.inbound_key}
    assert declared == {"favorites": INTAKE_PLAYLIST}
    owner = registry.by_handler_key(INTAKE_PLAYLIST)
    assert owner.landed and owner.long_running
    assert INTAKE_PLAYLIST in handlers.HANDLERS
    assert INTAKE_PLAYLIST in intake_cli.INTAKE_KEYS


def test_the_gate_refusal_queues_no_hearts_listing_either(installed, exported, monkeypatch):
    """PLAN, ASK, QUEUE: the read is queued by the run that answers."""
    del installed
    bind_hearts(monkeypatch)
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    assert _jobs() == []
    # THE GATE SAYS the hearts go whatever the answer.
    assert refused["cause"]["detail"]["shown"]["inbound"] == {
        "favorites": {"queued_whatever_the_answer": True, "not_queued": None}
    }


def test_the_gate_says_when_the_hearts_could_not_be_listed(installed, exported):
    del installed
    refused = exited(drive(_verb(exported)), ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["shown"]["inbound"] == {
        "favorites": {"queued_whatever_the_answer": False, "not_queued": "credential-missing"}
    }


def test_an_abort_still_queues_the_hearts_listing_under_the_shared_run(
    installed, exported, monkeypatch
):
    """Declining the write does not drop the read."""
    del installed
    fake = bind_hearts(monkeypatch)
    run_id, code, passed = _confirmed(exported, option="abort")
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "ok"

    assert [job.handler_key for job in _jobs()] == [INTAKE_PLAYLIST]
    (job,) = _hearts_jobs()
    assert job.payload["run_id"] == run_id
    assert job.payload[intake_cli.SOURCE] == intake_cli.FAVORITES
    # EXACTLY WHAT ``crate intake playlist favorites`` QUEUES, through the
    # same listing path, so the worker cannot tell them apart.
    assert job.payload[intake_cli.TRACKS] == intake_cli.list_favorites(fake)[0]
    assert len(_items(job.job_id)) == 3

    summary = passed["data"]["summary"]
    assert summary["not_queued"]["favorites"] == sync_cli.DECLINED
    assert _inbound(passed) == {
        "handler_key": INTAKE_PLAYLIST,
        "hearts": 3,
        "job_ids": [job.job_id],
        "not_queued": None,
        "open_jobs": [],
        "shortfall": None,
    }
    assert ("favorites", job.job_id, INTAKE_PLAYLIST) in {
        (j["source"], j["job_id"], j["handler_key"]) for j in summary["jobs"]
    }
    assert summary["queued"] == 1
    # AN INTAKE JOB, so the pass names the verb that lists what it found missing.
    assert summary["next"] == f"crate intake missing --run {run_id}"
    check = _inbound_check(passed)
    assert check["status"] == "ok" and job.job_id in check["detail"]
    (outbound,) = [c for c in passed["data"]["checks"] if c["key"] == "sync.favorites"]
    assert "abort" in outbound["detail"]


def test_a_confirmed_pass_queues_both_halves(installed, exported, monkeypatch):
    del installed
    bind_hearts(monkeypatch)
    run_id, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert sorted(job.handler_key for job in _jobs()) == [INTAKE_PLAYLIST, "sync.favorites"]
    assert {job.payload["run_id"] for job in _jobs()} == {run_id}
    assert passed["data"]["summary"]["sources"] == ["favorites"]


def test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal(
    installed, monkeypatch
):
    """The write half's precondition no longer refuses the source: the hearts alone make the pass OK."""
    del installed
    bind_hearts(monkeypatch)
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "ok"
    assert len(_hearts_jobs()) == 1
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
        "playlists": sync_cli.NOTHING_NEW,
    }
    (outbound,) = [c for c in passed["data"]["checks"] if c["key"] == "sync.favorites"]
    assert outbound["status"] == "fail"


def test_a_slim_pass_lists_no_hearts_and_queues_none(slim, monkeypatch):
    """The read is the favourites module's, and slim does not switch it on."""
    del slim
    fake = FakeCatalogue(
        hearts=_hearts("301"),
        playlists={"pl-a": FakePagedPlaylist(_tracks("101"))},
        account=[_playlist("pl-a", "Warmup")],
    )
    bind_hearts(monkeypatch, fake)
    passed = exited(drive(["sync", "all"]))
    assert _hearts_jobs() == []
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    assert fake.heart_listings == 0
    assert "favorites" not in passed["data"]["summary"]
    assert "sync.favorites.inbound" not in {c["key"] for c in passed["data"]["checks"]}


def test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run(
    installed, exported
):
    """No provider session: hearts reported unlisted with the catalogue's remedy, the write still queued."""
    del installed
    _, code, passed = _confirmed(exported)
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.favorites"]
    block = _inbound(passed)
    assert block["not_queued"] == "credential-missing"
    assert block["hearts"] is None and block["job_ids"] == []
    check = _inbound_check(passed)
    assert check["status"] == "fail" and check["remedy"]
    assert "hearts were not listed" in check["detail"]
    assert any(
        w["code"] == "sync-source-not-queued" and w["message"].startswith("favorites inbound:")
        for w in passed["warnings"]
    )


def test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue(
    installed, monkeypatch
):
    del installed

    class NoHearts(FakeCatalogue):
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing spent its whole budget")

    bind_hearts(
        monkeypatch,
        NoHearts(
            playlists={"pl-a": FakePagedPlaylist(_tracks("101"))},
            account=[_playlist("pl-a", "Warmup")],
        ),
    )
    passed = exited(drive(["sync", "all"]))
    assert _hearts_jobs() == []
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    assert _inbound(passed)["not_queued"] == "label-playlist-unreadable"
    assert _inbound_check(passed)["status"] == "fail"


def test_nothing_queued_because_every_half_refused_is_still_a_refusal(installed, monkeypatch):
    """The hearts refusal follows the write half's, so the pass leads with the export a person can supply."""
    del installed

    class NoHearts(FakeCatalogue):
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing failed")

    bind_hearts(monkeypatch, NoHearts())
    refused = failed(drive(["sync", "all"]))
    assert refused["cause"]["reason"] == "outbound-export-required"
    sources_data = refused["cause"]["detail"]["sources"]
    assert sources_data["summary"]["favorites"]["inbound"]["not_queued"] == (
        "label-playlist-unreadable"
    )
    assert _jobs() == []


def test_an_account_with_no_hearts_queues_nothing_for_them(installed, monkeypatch):
    del installed
    bind_hearts(monkeypatch, FakeCatalogue(**_A_NEW_PLAYLIST))
    passed = exited(drive(["sync", "all"]))
    assert _hearts_jobs() == []
    block = _inbound(passed)
    assert block["hearts"] == 0 and block["not_queued"] == "empty"
    check = _inbound_check(passed)
    assert check["status"] == "info" and "no hearts" in check["detail"]


class ShortHearts(FakeCatalogue):
    """The seam as the adapter answers when the provider counted hearts it did not serve (R-504)."""

    def __init__(self, rows: list[Track], *, declared: int, **kwargs) -> None:
        super().__init__(hearts=rows, **kwargs)
        self.declared = declared

    def favourite_tracks(self):
        self.heart_listings += 1
        raise catalogue.HeartsShortfall(self.hearts, self.declared)


def test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count(
    installed, monkeypatch
):
    del installed
    bind_hearts(monkeypatch, ShortHearts(_hearts("301", "302", "303"), declared=5))
    passed = exited(drive(["sync", "all"]))
    (job,) = _hearts_jobs()
    assert len(_items(job.job_id)) == 3
    block = _inbound(passed)
    assert block["hearts"] == 3 and block["not_queued"] is None
    assert block["shortfall"] == {"declared": 5, "listed": 3, "withheld": 2}
    check = _inbound_check(passed)
    assert check["status"] == "fail"
    assert job.job_id in check["detail"]
    assert "5 declared, 3 listed, 2 withheld by the provider" in check["detail"]


def test_hearts_all_withheld_are_not_reported_as_an_account_with_none(installed, monkeypatch):
    del installed
    bind_hearts(monkeypatch, ShortHearts([], declared=4, **_A_NEW_PLAYLIST))
    passed = exited(drive(["sync", "all"]))
    assert _hearts_jobs() == []
    block = _inbound(passed)
    assert block["not_queued"] == "empty"
    assert block["shortfall"] == {"declared": 4, "listed": 0, "withheld": 4}
    check = _inbound_check(passed)
    assert check["status"] == "fail"
    assert "no hearts" not in check["detail"]
    assert "4 declared, 0 listed, 4 withheld by the provider" in check["detail"]


def test_a_complete_hearts_listing_carries_no_shortfall(installed, monkeypatch):
    del installed
    bind_hearts(monkeypatch)
    passed = exited(drive(["sync", "all"]))
    assert _inbound(passed)["shortfall"] is None
    check = _inbound_check(passed)
    assert check["status"] == "ok" and "withheld" not in check["detail"]


def test_the_human_output_prints_the_inbound_shortfall(installed, monkeypatch):
    del installed
    bind_hearts(monkeypatch, ShortHearts(_hearts("301", "302", "303"), declared=5))
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["sync", "all"], stdout=out, stderr=err)
    text = out.getvalue() + err.getvalue()
    assert code == int(ExitCode.OK), text
    assert "[FAIL] sync.favorites.inbound:" in text
    assert "5 declared, 3 listed, 2 withheld by the provider" in text


def test_an_open_hearts_job_is_not_queued_twice(installed, monkeypatch):
    del installed
    fake = bind_hearts(monkeypatch)
    exited(drive(["sync", "all"]))
    (job,) = _hearts_jobs()

    # NOTHING NEW AND TWO SOURCES REFUSED, so the second pass is the refusal
    # naming the export, not an OK over an open job.
    again = failed(drive(["sync", "all"]))
    assert again["cause"]["reason"] == "outbound-export-required"
    assert _hearts_jobs() == [job], "an open hearts job was queued a second time"
    block = _inbound(again)
    assert block["not_queued"] == "in-flight"
    assert block["open_jobs"] == [job.job_id]
    assert fake.heart_listings == 1, "the hearts were listed again beside an open job"
    check = _inbound_check(again)
    assert check["status"] == "info" and job.job_id in check["detail"]


def test_a_hearts_job_queued_by_hand_is_not_queued_beside(installed, monkeypatch):
    """``crate intake playlist favorites`` lists the same hearts under the same key."""
    del installed
    bind_hearts(monkeypatch)
    exited(drive(["intake", "playlist", "favorites"]))
    (job,) = _hearts_jobs()
    passed = failed(drive(["sync", "all"]))
    assert _hearts_jobs() == [job]
    assert _inbound(passed)["open_jobs"] == [job.job_id]


def test_a_finished_hearts_job_does_not_hold_the_next_pass(installed, monkeypatch):
    """No cursor: a heart acquired since resolves owned, so the next pass lists again."""
    del installed
    bind_hearts(monkeypatch)
    drive(["sync", "all"])
    (job,) = _hearts_jobs()
    with jobs.open_store() as store:
        jobs.transition(store, job.job_id, jobs.JobState.FAILED)
    passed = exited(drive(["sync", "all"]))
    assert len(_hearts_jobs()) == 2
    assert _inbound(passed)["not_queued"] is None


def test_another_librarys_open_hearts_job_does_not_hold_this_one(installed, monkeypatch):
    import dataclasses

    cfg = installed
    bind_hearts(monkeypatch)
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="0000-0000")
    )
    with jobs.open_store() as store:
        intake_cli.queue_playlist(
            store,
            elsewhere,
            handler_key=INTAKE_PLAYLIST,
            reference=intake_cli.FAVORITES,
            tracks={"301": {"title": "Heart 301"}},
            source_id=intake_cli.FAVORITES_SOURCE_ID,
        )
    passed = exited(drive(["sync", "all"]))
    assert len(_hearts_jobs()) == 2
    assert _inbound(passed)["open_jobs"] == []


def test_an_open_playlists_job_does_not_hold_the_hearts(installed, monkeypatch):
    """Same key, another source: only a hearts job is the same work."""
    del installed
    bind_hearts(
        monkeypatch,
        FakeCatalogue(
            hearts=_hearts("301"),
            playlists={"pl-a": FakePagedPlaylist(_tracks("101"))},
            account=[_playlist("pl-a", "Warmup")],
        ),
    )
    drive(["sync", "all"])
    assert len(_hearts_jobs()) == 1
    (hearts_job,) = _hearts_jobs()
    with jobs.open_store() as store:
        jobs.transition(store, hearts_job.job_id, jobs.JobState.FAILED)
    exited(drive(["sync", "all"]))
    assert len(_hearts_jobs()) == 2


def test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone(
    installed, monkeypatch
):
    del installed
    from cratekit.core.cause import refuse

    bind_hearts(
        monkeypatch, FakeCatalogue(hearts=_hearts("301", "302", "303"), **_A_NEW_PLAYLIST)
    )
    real = intake_cli.queue_playlist

    def refusing(store, cfg, **kwargs):
        if kwargs.get("source_id") == intake_cli.FAVORITES_SOURCE_ID:
            raise refuse("internal-error", "the queue refused the hearts")
        return real(store, cfg, **kwargs)

    monkeypatch.setattr(intake_cli, "queue_playlist", refusing)
    passed = exited(drive(["sync", "all"]))
    assert [job.payload[intake_cli.SOURCE] for job in _jobs()] == ["pl-a"]
    assert _inbound(passed)["not_queued"] == "internal-error"
    assert passed["data"]["summary"]["not_queued"]["favorites"] == "outbound-export-required"
    check = _inbound_check(passed)
    assert check["status"] == "fail"
    # LISTED, THEN REFUSED AT THE QUEUE. Not the words a failed listing gets.
    assert "3 heart(s) were listed and not queued" in check["detail"]
    assert "were not listed" not in check["detail"]


def test_an_open_outbound_favourites_job_does_not_hold_the_hearts(
    installed, exported, monkeypatch
):
    """The outbound job carries ``source_id`` favorites under its own key, a write and not a listing."""
    del installed
    bind_hearts(monkeypatch)
    _confirmed(exported)
    (hearts_job,) = _hearts_jobs()
    assert any(job.handler_key == "sync.favorites" and job.is_open() for job in _jobs())
    with jobs.open_store() as store:
        jobs.transition(store, hearts_job.job_id, jobs.JobState.FAILED)
    _confirmed(exported)
    assert len(_hearts_jobs()) == 2


def test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op(
    tmp_path, monkeypatch
):
    """With labels off and no new playlist, unreadable hearts make the pass a refusal, not an honest zero."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    data["modules"] = {"labels": False}
    config.save(config.from_dict(data))
    config.reset_cache()
    outbound_source.forget_libraries()
    exported = outbound_fakes.write_export(root / "outbound")

    class NoHearts(FakeCatalogue):
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing failed")

    bind_hearts(monkeypatch, NoHearts())
    try:
        _, code, refused = _confirmed(exported, option="abort")
    finally:
        outbound_source.forget_libraries()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"
    assert _jobs() == []


# R-515: the sweep carries a short playlist listing per playlist


def test_the_sweep_summary_carries_the_shortfall_per_playlist(slim, monkeypatch):
    del slim
    fake = FakeCatalogue(
        playlists={
            "pl-a": FakePagedPlaylist(_tracks("101", "102"), declared=5),
            "pl-b": FakePagedPlaylist(_tracks("201"), declared=1),
        },
        account=[_playlist("pl-a", "Warmup"), _playlist("pl-b", "Peak")],
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    passed = exited(drive(["sync", "all"]))

    queued = {job.payload[intake_cli.SOURCE]: job for job in _playlist_jobs()}
    assert set(queued) == {"pl-a", "pl-b"}, "a short playlist is queued, never refused"
    assert _items(queued["pl-a"].job_id) == ["101", "102"]
    block = passed["data"]["summary"]["playlists"]
    assert block["withheld"] == {
        "pl-a": {"declared": 5, "listed": 2, "withheld": 3, "name": "Warmup"},
    }
    (warning,) = [w for w in passed["warnings"] if w["code"] == "sync-playlists-withheld"]
    assert "Warmup: 5 declared, 2 listed, 3 withheld by the provider" in warning["message"]
    assert "Peak" not in warning["message"]


def test_a_sweep_of_full_playlists_carries_no_shortfall(slim, monkeypatch):
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    passed = exited(drive(["sync", "all"]))
    assert passed["data"]["summary"]["playlists"]["withheld"] == {}
    assert "sync-playlists-withheld" not in {w["code"] for w in passed["warnings"]}


# R-1289: the sweep reads each playlist row by row, so one track the account
# lists with no title or no artist never leaves the whole playlist out


def _unread_warning(passed) -> str:
    (warning,) = [w for w in passed["warnings"] if w["code"] == "sync-playlists-unread"]
    return warning["message"]


@pytest.mark.parametrize(
    ("untitled", "absent"),
    [
        (Track("103", "Artist 103", ""), "title"),
        (Track("103", "", "Title 103"), "artist"),
    ],
)
def test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues(
    slim, monkeypatch, untitled, absent
):
    """The brief's first two scenarios: two readable tracks queue, the third is named."""
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), [*_tracks("101", "102"), untitled]),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    passed = exited(drive(["sync", "all"]))

    queued = {job.payload[intake_cli.SOURCE]: job for job in _playlist_jobs()}
    assert set(queued) == {"pl-a", "pl-b"}
    assert _items(queued["pl-a"].job_id) == ["101", "102"]
    block = passed["data"]["summary"]["playlists"]
    assert "pl-a" not in block["excluded"] and block["unreadable"] == {}
    assert block["unread"] == {
        "pl-a": {
            "name": "Warmup",
            "tracks": {
                "103": {
                    "artist": untitled.artist["name"],
                    "title": untitled.name,
                    "isrc": "",
                    "why": f"the account lists it with no {absent}",
                }
            },
        }
    }
    message = _unread_warning(passed)
    assert f"Warmup: 103 (the account lists it with no {absent})" in message
    assert "Peak" not in message
    # TRUE OF WHAT HAPPENS NEXT: the playlist is recorded once its job
    # succeeds, so no later sync offers it again.
    assert "no later sync offers" in message
    assert "sync-playlists-unreadable" not in {w["code"] for w in passed["warnings"]}


def test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds(
    slim, monkeypatch
):
    """The warning's promise, driven: the job succeeds, the next pass records it."""
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), [*_tracks("101"), Track("103", "Artist 103", "")]),
    )
    exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    resumed = exited(drive(cli_jobs.argv_for(job)))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    code, second = drive(["sync", "all"])
    block = second["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert block["excluded"]["pl-a"]["reason"] == "recorded"
    assert block["unread"] == {}
    assert len(_playlist_jobs()) == 1


def test_a_row_with_no_provider_id_still_leaves_its_playlist_out_by_name(slim, monkeypatch):
    """The brief's third scenario: a track with no id cannot be named or set aside."""
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), [*_tracks("101"), Track("", "Artist", "Title")]),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    passed = exited(drive(["sync", "all"]))
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-b"]
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"]["pl-a"] == {"reason": "unreadable", "name": "Warmup"}
    assert "pl-a" in block["unreadable"]
    assert block["unread"] == {}
    assert "sync-playlists-unreadable" in {w["code"] for w in passed["warnings"]}


def test_a_refusal_not_about_one_playlist_still_stops_the_sweep(slim, monkeypatch):
    """The brief's fourth scenario: an expired session is the source's, not a playlist's."""
    del slim
    from cratekit.core.cause import refuse

    class Expired(FakeCatalogue):
        def playlist_for(self, reference):
            if reference == "pl-b":
                raise refuse(
                    "credential-missing", "the provider session expired", origin=("test",)
                )
            return super().playlist_for(reference)

    fake = Expired(
        playlists={
            "pl-a": FakePagedPlaylist([*_tracks("101"), Track("103", "Artist 103", "")]),
            "pl-b": FakePagedPlaylist(_tracks("201")),
        },
        account=[_playlist("pl-a", "Warmup"), _playlist("pl-b", "Peak")],
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    refused = failed(drive(["sync", "all"]))
    assert refused["cause"]["reason"] == "credential-missing"
    assert _jobs() == []


def test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty(slim, monkeypatch):
    del slim
    bind_playlists(
        monkeypatch,
        (
            _playlist("pl-a", "Warmup"),
            [Track("103", "Artist 103", ""), Track("104", "", "Title 104")],
        ),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    passed = exited(drive(["sync", "all"]))
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-b"]
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"]["pl-a"] == {"reason": "unreadable", "name": "Warmup"}
    assert block["unreadable"]["pl-a"] == (
        "no track on it could be queued: 103 (the account lists it with no title), "
        "104 (the account lists it with no artist)"
    )
    assert set(block["unread"]["pl-a"]["tracks"]) == {"103", "104"}
    codes = {w["code"] for w in passed["warnings"]}
    # OFFERED AGAIN, as any unreadable playlist is, so the unread warning's
    # words about a recorded playlist are not said of it.
    assert "sync-playlists-unreadable" in codes
    assert "sync-playlists-unread" not in codes
    assert _swept(config.load()) is None


def test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check(
    slim, monkeypatch
):
    del slim
    bind_playlists(
        monkeypatch, (_playlist("pl-a", "Warmup"), [Track("103", "Artist 103", "")])
    )
    passed = exited(drive(["sync", "all"]))
    assert passed["outcome"] == "no_op"
    (check,) = passed["data"]["checks"]
    assert "1 unreadable" in check["detail"]


def test_a_fully_readable_sweep_names_nothing_unread(slim, monkeypatch):
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101", "102")))
    passed = exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    assert _items(job.job_id) == ["101", "102"]
    assert passed["data"]["summary"]["playlists"]["unread"] == {}
    assert "sync-playlists-unread" not in {w["code"] for w in passed["warnings"]}


def test_a_short_listing_with_an_unread_track_carries_both(slim, monkeypatch):
    """The declared count check the sweep had stays: the shortfall rides beside."""
    del slim
    fake = FakeCatalogue(
        playlists={
            "pl-a": FakePagedPlaylist(
                [*_tracks("101"), Track("103", "Artist 103", "")], declared=4
            ),
        },
        account=[_playlist("pl-a", "Warmup")],
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    passed = exited(drive(["sync", "all"]))
    (job,) = _playlist_jobs()
    assert _items(job.job_id) == ["101"]
    block = passed["data"]["summary"]["playlists"]
    assert block["withheld"]["pl-a"] == {
        "declared": 4, "listed": 2, "withheld": 2, "name": "Warmup"
    }
    assert set(block["unread"]["pl-a"]["tracks"]) == {"103"}
