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
import io
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
from tests.cli_drive import drive
from tests.intake.test_workers import Track
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
from tests.test_cli_contract import _enqueue_calls
from tests.test_config import valid_data
from tests.test_label_workers import LABELS, SLUGS, readable, register
from tests.test_label_workers import bind as bind_catalogue
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
    # No provider session is stored here, so it refuses for itself.
    assert summary["not_queued"] == {"playlists": "credential-missing"}
    # A LABELS AND A FAVOURITES JOB ARE NOT INTAKE JOBS, so the pass names no
    # ``intake missing --run``, which would find nothing of theirs to list.
    assert summary["next"] is None
    assert "sync.next" not in {c["key"] for c in passed["data"]["checks"]}


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
        "playlists": "credential-missing",
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
        "playlists": "credential-missing",
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
        "playlists": "credential-missing",
    }
    assert _jobs() == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. The slim profile, and the playlists source it runs alone (U64)
# ═══════════════════════════════════════════════════════════════════════════


def _playlist(playlist_id: str, name: str, tracks: int | None = None) -> AccountPlaylist:
    return AccountPlaylist(playlist_id=playlist_id, name=name, tracks=tracks)


def bind_playlists(
    monkeypatch, *listed: tuple[AccountPlaylist, list[Track] | None]
) -> FakeCatalogue:
    """An account whose own playlists are ``listed``, each with its tracks.

    A playlist given ``None`` for its tracks is listed on the account and cannot
    be resolved, which is the shape of a playlist deleted between the two reads.
    """
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
    code, refused = drive(["sync", "all"])
    assert code != int(ExitCode.OK), refused
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
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
    """Both ways a playlist can be empty: the listing's count says so, or the
    count is unknown and the tracks come back empty. Neither is a silent success."""
    del slim
    fake = bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Counted Empty", tracks=0), _tracks()),
        (_playlist("pl-b", "Listed Empty"), _tracks()),
    )
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "no_op"
    assert passed["data"]["summary"]["playlists"]["listed"] == 0
    assert _swept(config.load()) is None


def test_the_favourites_placeholders_are_left_to_the_favourites_source(slim, monkeypatch):
    """By the favourites source's own pattern, never a copied literal. The two near
    names are playlists a person made and are swept."""
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert {job.payload[intake_cli.SOURCE] for job in _playlist_jobs()} == {
        "pl-all",
        "pl-copy",
        "pl-old",
    }
    excluded = passed["data"]["summary"]["playlists"]["excluded"]
    assert {excluded[k]["reason"] for k in ("pl-q", "pl-backlog")} == {"favorites-placeholder"}


def test_the_cursor_records_ids_only_once_a_job_succeeds(slim, monkeypatch):
    """Queued is not swept, an open job is not queued twice, and a succeeded job
    records its playlist's identifier and never its title."""
    cfg = slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup Title"), _tracks("101")),
        (_playlist("pl-b", "Peak Title"), _tracks("201")),
    )
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
    assert _swept(cfg) is None, "queueing a playlist recorded it as swept"

    code, again = drive(["sync", "all"])
    assert code == int(ExitCode.OK), again
    assert len(_playlist_jobs()) == 2, "an open job's playlist was queued a second time"
    assert {k: v["reason"] for k, v in again["data"]["summary"]["playlists"]["excluded"].items()} == {
        "pl-a": "in-flight",
        "pl-b": "in-flight",
    }

    (job_a,) = [j for j in _playlist_jobs() if j.payload[intake_cli.SOURCE] == "pl-a"]
    code, resumed = drive(cli_jobs.argv_for(job_a))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)

    code, third = drive(["sync", "all"])
    assert code == int(ExitCode.OK), third
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["data"]["summary"]["playlists"]["recorded_now"] == []
    assert _swept(cfg) is None
    assert len(_playlist_jobs()) == 2


def test_a_playlist_queued_by_hand_is_not_this_sources_to_record(slim, monkeypatch):
    """``crate intake playlist`` shares the handler key. Its job is not in flight
    for this source and its success is not a sweep this source made."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    code, by_hand = drive(["intake", "playlist", "pl-a"])
    assert code == int(ExitCode.OK), by_hand
    code, resumed = drive(cli_jobs.argv_for(_playlist_jobs()[0]))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert [row["playlist_id"] for row in passed["data"]["summary"]["playlists"]["queued"]] == ["pl-a"]
    assert _swept(cfg) is None


def test_another_librarys_finished_job_is_not_this_librarys_sweep(slim, monkeypatch):
    """The queue is installation scoped and the cursor is per library. A playlist
    another library's pass swept is still new to this one."""
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    block = passed["data"]["summary"]["playlists"]
    assert block["excluded"]["pl-gone"]["reason"] == "unreadable"
    assert "pl-gone" in block["unreadable"]
    assert "sync-playlists-unreadable" in {w["code"] for w in passed["warnings"]}


def test_an_account_listing_that_fails_is_a_refusal_not_an_empty_account(slim, monkeypatch):
    """R-135's class for this source. The slim pass has nothing else, so it refuses."""
    del slim

    class Unlistable(FakeCatalogue):
        def account_playlists(self):
            raise RuntimeError("the provider stopped answering")

    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Unlistable()))
    code, refused = drive(["sync", "all"])
    assert code != int(ExitCode.OK), refused
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    (job,) = _playlist_jobs()
    summary = passed["data"]["summary"]
    assert [j["job_id"] for j in summary["jobs"]] == [job.job_id]
    assert summary["not_queued"]["playlists"] == "internal-error"
    assert [row["job_id"] for row in summary["playlists"]["queued"]] == [job.job_id]
    (check,) = [c for c in passed["data"]["checks"] if c["title"] == "playlists"]
    assert check["status"] == "fail" and job.job_id in check["detail"]


# ═══════════════════════════════════════════════════════════════════════════
# 3b. The deferred mark, R-358 code half
#
# THE PRODUCER IS THE PASS AND NOT A HAND BUILT DATACLASS. ``recorded_now`` is
# only ever non empty because a pass queued a playlist and that playlist's
# intake job then SUCCEEDED, so every mark test below drives that sequence for
# real before it asks anything about a rename.
# ═══════════════════════════════════════════════════════════════════════════


def _recording_pass(cfg, fake) -> playlists.Sweep:
    """Queue ``pl-a``, finish its job, and return the pass that records it.

    :func:`playlists.plan` reconciles, so it is called EXACTLY ONCE here: a
    second call records nothing fresh and would hand back a sweep whose
    ``recorded_now`` is empty for a reason that has nothing to do with marks.
    """
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    with jobs.open_store() as store:
        sweep = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sweep.recorded_now == ("pl-a",), sweep.recorded_now
    return sweep


def test_a_mark_without_a_real_importable_file_renames_nothing(slim, monkeypatch, tmp_path):
    """Both halves of the file rule, and neither reaches the account at all.

    The listing count is asserted because the ORDER is the property: the file is
    checked before the recheck's second read, so a caller with no file spends no
    provider call finding that out.
    """
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    listings = fake.account_listings

    with pytest.raises(CratekitError) as absent:
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert absent.value.cause.reason == "sync-marks-blocked"

    output.write_text("", encoding="utf-8")
    with pytest.raises(CratekitError) as empty:
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert empty.value.cause.reason == "sync-marks-blocked"

    assert account.renamed == []
    assert fake.account_listings == listings, "the recheck read ran before the file check"


def test_a_mark_after_a_real_importable_file_prefixes_the_recorded_playlist(
    slim, monkeypatch, tmp_path
):
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")
    listings = fake.account_listings

    marked = playlists.mark_swept(sweep, fake, account, local_output=output)

    assert marked == ("pl-a",)
    assert account.renamed == [("pl-a", playlists.SWEPT_PREFIX + "Warmup")]
    assert playlists.is_swept_name(account.titles["pl-a"])
    assert fake.account_listings == listings + 1, "the recheck was not a second read"


def test_a_playlist_renamed_on_the_account_since_the_plan_is_left_alone(
    slim, monkeypatch, tmp_path
):
    """What the recheck is for. The prefix would land on a playlist that is no
    longer the thing the pass swept, and the title it would build names a
    playlist that no longer exists under that name."""
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    fake.account = [_playlist("pl-a", "Warmup Rework")]
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")

    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ()
    assert account.renamed == []


def test_a_playlist_gone_from_the_account_since_the_plan_is_not_marked(
    slim, monkeypatch, tmp_path
):
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(slim, fake)
    fake.account = []
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")

    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ()
    assert account.renamed == []


def test_a_recorded_playlist_the_pass_never_listed_is_not_pending_at_all(
    slim, monkeypatch
):
    """ASSERTED ON ``pending_marks`` AND NOT THROUGH ``mark_swept``, because the
    recheck would hide it. A playlist in the cursor that this pass did not list
    has no name to prefix, and a mark with no name reaches the recheck, fails it
    for the wrong reason, and reports the same nothing. Two guards over one case
    is one guard nothing covers."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    _recording_pass(cfg, fake)

    fake.account = []
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert later.listed == ()
    assert later.recorded == frozenset({"pl-a"})
    assert playlists.pending_marks(later) == ()


def test_a_playlist_the_source_system_already_prefixed_is_not_prefixed_twice(
    slim, monkeypatch, tmp_path
):
    """Reachable while both systems run, which is the state R-358 is about: the
    job finishes here and DJ_tools sweeps the same playlist before this pass
    records it. Marking again would build ``DOWNLOADED DOWNLOADED Warmup``."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    fake.account = [_playlist("pl-a", playlists.SWEPT_PREFIX + "Warmup")]
    with jobs.open_store() as store:
        sweep = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert sweep.recorded_now == ("pl-a",)

    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")

    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ()
    assert account.renamed == []


def test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass(
    slim, monkeypatch, tmp_path
):
    """The cursor moves before anything is marked, so the mark set cannot be what
    the cursor ADDED. A refused mark here would otherwise leave a playlist
    recorded, excluded as recorded for life, and never prefixed."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(cfg, fake)
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"

    with pytest.raises(CratekitError):
        playlists.mark_swept(sweep, fake, account, local_output=output)
    assert account.renamed == []

    # The next pass records nothing new and still owes the mark.
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert later.recorded_now == ()
    assert later.excluded["pl-a"] == playlists.Excluded.RECORDED
    assert [mark.target_id for mark in playlists.pending_marks(later)] == ["pl-a"]

    output.write_text("<COLLECTION/>", encoding="utf-8")
    assert playlists.mark_swept(later, fake, account, local_output=output) == ("pl-a",)
    assert account.renamed == [("pl-a", playlists.SWEPT_PREFIX + "Warmup")]


def test_a_mark_that_landed_is_not_owed_a_second_time(slim, monkeypatch, tmp_path):
    """What ends the retrying is the prefix itself, read back off the account."""
    cfg = slim
    fake = bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    sweep = _recording_pass(cfg, fake)
    account = outbound_fakes.FakeAccount()
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")
    assert playlists.mark_swept(sweep, fake, account, local_output=output) == ("pl-a",)

    # PINNED BEFORE IT IS FED BACK. Handing the account's own title straight to
    # the next listing without asserting it first would make the whole test an
    # expected value taken from the code under test.
    assert account.titles["pl-a"] == playlists.SWEPT_PREFIX + "Warmup"
    fake.account = [_playlist("pl-a", account.titles["pl-a"])]
    with jobs.open_store() as store:
        later = playlists.plan(store, cfg, fake, handler_key=INTAKE_PLAYLIST)
    assert playlists.pending_marks(later) == ()
    assert playlists.mark_swept(later, fake, account, local_output=output) == ()
    assert len(account.renamed) == 1


def test_a_rename_that_fails_mid_batch_still_names_the_ones_that_landed(
    slim, monkeypatch, tmp_path
):
    """Each rename is its own remote write. The return value is gone when this
    raises, so a caller that has to name what reached the account passes a list,
    on ``queue``'s pattern."""
    cfg = slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
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

    account = outbound_fakes.FakeAccount(fail_on={"pl-b"})
    output = tmp_path / "run-1_synced.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")
    landed: list[str] = []

    with pytest.raises(RuntimeError):
        playlists.mark_swept(
            sweep, fake, account, local_output=output, applied=landed
        )

    assert landed == ["pl-a"]
    assert account.renamed == [("pl-a", playlists.SWEPT_PREFIX + "Warmup")]


def test_the_current_intake_path_marks_nothing_and_still_reports_unbound(slim, monkeypatch):
    """The brief's second scenario. A pass that RECORDED a playlist still reports
    the mark unbound, because the intake worker resolves tracks and acquires
    none, so no importable file exists for the mark step to wait on."""
    cfg = slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    drive(["sync", "all"])
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    code, third = drive(["sync", "all"])
    assert code == int(ExitCode.OK), third
    block = third["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert block["mark"] == playlists.MARK_UNBOUND
    assert block["marked"] == []
    assert _swept(cfg) == ("pl-a",)


# R-359. SWEPT MEANS RESOLVED, NOT ACQUIRED, AND BOTH SURFACES SAY SO. The
# producer is the real pass over a playlist the library owns none of: its
# intake job SUCCEEDS with every track reported missing and none acquired, and
# the next pass records it. ``reconcile`` is deliberately unchanged; what this
# guards is that a person is not left to read "recorded" as "the library holds
# the files". The literal is spelled out rather than read off the module, so a
# changed token fails here instead of agreeing with itself.


def _recorded_over_missing(monkeypatch) -> None:
    """Drive the producer to the point the next pass records a playlist whose
    every track the library does not own."""
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101", "102")))
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
    (job,) = _playlist_jobs()
    code, resumed = drive(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    progress = resumed["data"]["progress"]
    assert (progress["missing"], progress["acquired"]) == (2, 0), progress


def _run_human(argv: list[str]) -> tuple[int, str]:
    """The default human mode, through the real dispatcher. ``drive`` always asks
    for json, so a test through it stays green over a blank human answer."""
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    block = passed["data"]["summary"]["playlists"]
    assert block["recorded_now"] == ["pl-a"]
    assert _swept(cfg) == ("pl-a",)
    assert block["swept_means"] == "resolved-not-acquired"


def test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired(
    slim, monkeypatch
):
    del slim
    _recorded_over_missing(monkeypatch)
    code, text = _run_human(["sync", "all"])
    assert code == int(ExitCode.OK), text
    line = _playlists_line(text)
    assert "1 recorded" in line, text
    assert "resolved" in line and "not acquired" in line, text
    lowered = text.lower()
    for claim in ("downloaded", "library holds", "in your library", "acquired the"):
        assert claim not in lowered, text


# ═══════════════════════════════════════════════════════════════════════════
# 3d. The pass names its next step, U73
#
# A pass ends in one list, one download and one landed file (R29). The pass
# itself queues and stops, so what it owes a person is the command that turns
# its intake jobs into that one list, in the output a person reads by default.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb(
    slim, monkeypatch
):
    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    code, text = _run_human(["sync", "all"])
    assert code == int(ExitCode.OK), text
    (run_id,) = {job.payload["run_id"] for job in _playlist_jobs()}
    (line,) = [row for row in text.splitlines() if "sync.next:" in row]
    assert f"crate intake missing --run {run_id}" in line, text
    assert "2 intake job(s)" in line, text


def test_the_json_summary_carries_the_same_command(slim, monkeypatch):
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101")))
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["data"]["summary"]["next"] == f"crate intake missing --run {passed['run_id']}"


def test_a_pass_that_queued_no_intake_job_names_no_run_verb(slim, monkeypatch):
    """``intake missing --run`` refuses a run with no intake job, so naming it
    here would send a person to a refusal."""
    del slim
    bind_playlists(monkeypatch, (_playlist("pl-a", "Counted Empty", tracks=0), _tracks()))
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["data"]["summary"]["next"] is None
    assert "sync.next" not in {c["key"] for c in passed["data"]["checks"]}


def test_a_pass_through_to_one_list_holds_a_shared_track_once_with_both_playlists(
    slim, monkeypatch
):
    """The producer is the pass: two playlists sharing a track, both jobs run
    by the real worker, then the verb the pass named. One list, one row for the
    shared track, both playlists in its provenance."""
    import json

    del slim
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101", "102")),
        (_playlist("pl-b", "Peak"), _tracks("102", "201")),
    )
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    for job in _playlist_jobs():
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed

    command = passed["data"]["summary"]["next"].split()
    assert command[:3] == ["crate", "intake", "missing"]
    code, listed = drive(command[1:])
    assert code == int(ExitCode.OK), listed
    summary = listed["data"]["summary"]
    body = json.loads(Path(summary["list"]).read_text())
    assert sorted(track["id"] for track in body["tracks"]) == ["101", "102", "201"]
    rows = json.loads(Path(summary["manifest"]).read_text())["rows"]
    assert sorted(rows["102"]["source_refs"]) == ["pl-a", "pl-b"]
    assert (rows["101"]["source_ref"], rows["201"]["source_ref"]) == ("pl-a", "pl-b")


def test_the_block_says_what_swept_means_whatever_the_pass_found():
    """On the pure path too, so an account with nothing recorded is not a block
    that leaves the word undefined."""
    block = playlists.report(playlists.Sweep(), [])
    assert block["swept_means"] == "resolved-not-acquired"
    assert "not acquired" in (playlists.said(block) or "")
    assert playlists.said({}) is None, "a block carrying no token was given words"


def test_the_pass_composes_no_mark_step_while_no_sweep_writes_an_importable_file():
    """DELETE THIS GUARD WHEN THE LIVE HALF OF R-358 IS DONE, and not before.

    ``mark_swept`` exists and ``sync.cli`` deliberately does not call it. That is
    the whole of the code half: the seam is built and the first live rename is an
    attended act, so a session that wires the mark step into the production pass
    unattended trips this rather than renaming somebody's playlists.
    """
    banned = {"mark_swept", "rename_playlist"}
    named: set[str] = set()
    for node in ast.walk(ast.parse(SRC.read_text(encoding="utf-8"))):
        # EVERY WAY THE NAME CAN ARRIVE, not only ``playlists.mark_swept(...)``.
        # An attribute scan alone is walked straight past by a plain
        # ``from cratekit.sync.playlists import mark_swept`` and a bare call,
        # which is the shape a session wiring this up is most likely to write.
        if isinstance(node, ast.Attribute):
            named.add(node.attr)
        elif isinstance(node, ast.Name):
            named.add(node.id)
        elif isinstance(node, ast.ImportFrom):
            named.update(alias.asname or alias.name for alias in node.names)
    assert named, "the scan read no names at all"
    assert sorted(named & banned) == []


def test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran():
    """Two different facts, and an empty list is not what separates them."""
    sweep = playlists.Sweep()
    never = playlists.report(sweep, [])
    ran = playlists.report(sweep, [], marked=())
    assert (never["mark"], never["marked"]) == (playlists.MARK_UNBOUND, [])
    assert (ran["mark"], ran["marked"]) == (playlists.MARK_APPLIED, [])
    assert playlists.report(sweep, [], marked=("pl-a",))["marked"] == ["pl-a"]


def test_the_sync_package_defines_no_remove_write():
    """The brief's fourth scenario, over the package that gained the mark caller.

    ``tests/modules/test_outbound.py`` makes this assertion over the outbound,
    export and favourites roots. R-358 gave ``sync`` its first reason to name an
    account write, so the same names are banned here too. The SET is imported
    from there rather than copied: a copy means extending one arms three roots
    and leaves this one unarmed, which is the drift ``outbound_fakes`` exists to
    stop one layer down.
    """
    from tests.modules.test_outbound import FORBIDDEN_WRITE_NAMES

    defined: set[str] = set()
    for path in SRC.parent.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined.add(node.name)
    assert defined, "the scan read no functions at all"
    assert sorted(defined & FORBIDDEN_WRITE_NAMES) == []


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
    # WHICH GUARD EACH CASE REACHES. The cloud sync gate offers neither the
    # option nor a digest, so both layers refuse it. The export gate compares a
    # digest and does not offer "sync", so only the option layer refuses it.
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


def test_a_hand_off_to_a_gate_that_compares_no_digest_refuses(installed, monkeypatch):
    """The digest layer alone. No declared gate offers "sync" without comparing a
    digest, so one is made here: the real favourites entry with its confirm's
    digest source removed. Without that layer the resumed child would never
    meet ``DecisionStale``, whatever the plan became after the answer."""
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


# ═══════════════════════════════════════════════════════════════════════════
# 6. The hearts listing, favourites' read only half (U74)
# ═══════════════════════════════════════════════════════════════════════════


def _hearts(*ids: str) -> list[Track]:
    return [Track(track_id, f"Heart Artist {track_id}", f"Heart {track_id}") for track_id in ids]


def bind_hearts(monkeypatch, fake: FakeCatalogue | None = None) -> FakeCatalogue:
    """An account with three hearts and no playlists of its own, unless given one."""
    fake = fake if fake is not None else FakeCatalogue(hearts=_hearts("301", "302", "303"))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


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
    """The inbound key is a string at this layer, pinned where the registry is
    visible. It must be an intake key, or ``intake missing --run`` would not list
    what it found and the pass would name no next step for it."""
    declared = {spec.source_id: spec.inbound_key for spec in sources.SPECS if spec.inbound_key}
    assert declared == {"favorites": INTAKE_PLAYLIST}
    owner = registry.by_handler_key(INTAKE_PLAYLIST)
    assert owner.landed and owner.long_running
    assert INTAKE_PLAYLIST in handlers.HANDLERS
    assert INTAKE_PLAYLIST in intake_cli.INTAKE_KEYS


def test_the_gate_refusal_queues_no_hearts_listing_either(installed, exported, monkeypatch):
    """PLAN, ASK, QUEUE still holds. The read is queued by the run that answers."""
    del installed
    bind_hearts(monkeypatch)
    code, refused = drive(_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _jobs() == []
    # THE GATE SAYS the hearts go whatever the answer, which is what a person
    # deciding the write needs to know about the read.
    assert refused["cause"]["detail"]["shown"]["inbound"] == {
        "favorites": {"queued_whatever_the_answer": True, "not_queued": None}
    }


def test_the_gate_says_when_the_hearts_could_not_be_listed(installed, exported):
    del installed
    code, refused = drive(_verb(exported))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["inbound"] == {
        "favorites": {"queued_whatever_the_answer": False, "not_queued": "credential-missing"}
    }


def test_an_abort_still_queues_the_hearts_listing_under_the_shared_run(
    installed, exported, monkeypatch
):
    """The unit's whole point. Declining the write no longer drops the read."""
    del installed
    register(LABELS[0])
    fake = bind_hearts(monkeypatch)
    run_id, code, passed = _confirmed(exported, option="abort")
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "ok"

    assert sorted(job.handler_key for job in _jobs()) == [INTAKE_PLAYLIST, "sync.labels"]
    (job,) = _hearts_jobs()
    assert job.payload["run_id"] == run_id
    assert job.payload[intake_cli.SOURCE] == intake_cli.FAVORITES
    # EXACTLY WHAT ``crate intake playlist favorites`` QUEUES, read through the
    # same listing path, so the worker cannot tell the two apart.
    assert job.payload[intake_cli.TRACKS] == intake_cli.list_playlist(fake, intake_cli.FAVORITES)
    assert len(_items(job.job_id)) == 3

    summary = passed["data"]["summary"]
    assert summary["not_queued"]["favorites"] == sync_cli.DECLINED
    assert _inbound(passed) == {
        "handler_key": INTAKE_PLAYLIST,
        "hearts": 3,
        "job_ids": [job.job_id],
        "not_queued": None,
        "open_jobs": [],
    }
    assert ("favorites", job.job_id, INTAKE_PLAYLIST) in {
        (j["source"], j["job_id"], j["handler_key"]) for j in summary["jobs"]
    }
    assert summary["queued"] == 2
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
    """The write half's own precondition used to refuse the whole source. With
    the labels registry empty too, the hearts are the only work, and the pass is
    OK rather than a refusal naming the export."""
    del installed
    bind_hearts(monkeypatch)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert passed["outcome"] == "ok"
    assert len(_hearts_jobs()) == 1
    assert passed["data"]["summary"]["not_queued"] == {
        "favorites": "outbound-export-required",
        "labels": "label-registry-empty",
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert _hearts_jobs() == []
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    assert fake.heart_listings == 0
    assert "favorites" not in passed["data"]["summary"]
    assert "sync.favorites.inbound" not in {c["key"] for c in passed["data"]["checks"]}


def test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run(installed):
    """No provider session: the hearts are reported not listed, with the
    catalogue's own remedy, and the labels sweep is queued regardless."""
    del installed
    register(LABELS[0])
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.labels"]
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
    register(LABELS[0])

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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert _hearts_jobs() == []
    assert [job.payload[intake_cli.SOURCE] for job in _playlist_jobs()] == ["pl-a"]
    assert "sync.labels" in {job.handler_key for job in _jobs()}
    assert _inbound(passed)["not_queued"] == "label-playlist-unreadable"
    assert _inbound_check(passed)["status"] == "fail"


def test_nothing_queued_because_every_half_refused_is_still_a_refusal(installed, monkeypatch):
    """The hearts refusal joins the refusal list after the write half's, so the
    pass still leads with the export a person can supply."""
    del installed

    class NoHearts(FakeCatalogue):
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing failed")

    bind_hearts(monkeypatch, NoHearts())
    code, refused = drive(["sync", "all"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "outbound-export-required"
    sources_data = refused["cause"]["detail"]["sources"]
    assert sources_data["summary"]["favorites"]["inbound"]["not_queued"] == (
        "label-playlist-unreadable"
    )
    assert _jobs() == []


def test_an_account_with_no_hearts_queues_nothing_for_them(installed, monkeypatch):
    del installed
    register(LABELS[0])
    bind_hearts(monkeypatch, FakeCatalogue())
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert _hearts_jobs() == []
    block = _inbound(passed)
    assert block["hearts"] == 0 and block["not_queued"] == "empty"
    check = _inbound_check(passed)
    assert check["status"] == "info" and "no hearts" in check["detail"]


def test_an_open_hearts_job_is_not_queued_twice(installed, monkeypatch):
    del installed
    fake = bind_hearts(monkeypatch)
    code, first = drive(["sync", "all"])
    assert code == int(ExitCode.OK), first
    (job,) = _hearts_jobs()

    # NOTHING NEW AND TWO SOURCES REFUSED, so the second pass is the refusal that
    # names the export, carrying the whole pass. Not an OK over an open job.
    code, again = drive(["sync", "all"])
    assert code != int(ExitCode.OK), again
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
    code, by_hand = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), by_hand
    (job,) = _hearts_jobs()
    code, passed = drive(["sync", "all"])
    assert code != int(ExitCode.OK), passed
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
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
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert len(_hearts_jobs()) == 2


def test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone(
    installed, monkeypatch
):
    del installed
    from cratekit.core.cause import refuse

    register(LABELS[0])
    bind_hearts(monkeypatch)
    real = intake_cli.queue_playlist

    def refusing(store, cfg, **kwargs):
        if kwargs.get("source_id") == intake_cli.FAVORITES_SOURCE_ID:
            raise refuse("internal-error", "the queue refused the hearts")
        return real(store, cfg, **kwargs)

    monkeypatch.setattr(intake_cli, "queue_playlist", refusing)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    assert [job.handler_key for job in _jobs()] == ["sync.labels"]
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
    """The outbound job carries ``source_id`` favorites too, under its own key.
    It is a write to the account, not a listing of the hearts."""
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
    """Labels switched off and no playlist new: the unreadable hearts are the
    only thing between this pass and work, so the pass says so with that
    refusal rather than reading as the honest zero a declined write is."""
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
