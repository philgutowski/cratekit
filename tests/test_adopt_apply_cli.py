"""U27: the ``adopt apply`` command line, and the one session it opens.

The conformance suite drives only this verb's QUEUEING path, over a plan that is
empty, so the session would ship undriven without this file. The residual it
closes said ``apply_plan`` rewrote a user's file with nothing asserting the
volume identity, the backup acknowledgment or the whole-run lock.
:func:`apply_outstanding` opens ONE session around the loop, and the session
tests below measure it from inside the loop and against the file's own bytes.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import shutil
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import apply_cli, collection
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, preflight, rb_writer, session, tags, taxonomy
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode
from tests import adopt_fixtures
from tests.cli_drive import approve_and_queue, drive
from tests.test_adoption import TREE_ID, _bucket_and_genre, _plan_of, _readable, _row
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION

#: A volume identity that is not the configured one.
FOREIGN_VOLUME = "0000-0000"
APPLY = ["adopt", "apply"]
GATE = "adopt.apply.approve"


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture(autouse=True)
def _reader_cache():
    """No test may inherit another test's library: the reader memoizes per process
    on the resolved database path, which every test here shares."""
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What this machine cannot speak for on behalf of a temporary library; that
    the canary refuses a tripped marker is proved in ``tests/test_rb_writer_db.py``."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


@pytest.fixture
def cfg(library, monkeypatch):
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    return resolved


#: One readable routable track, one row whose file is not on disk, and one
#: tombstone, so a census exercises three outcomes of the derivation.
def _tracks(declared_taxonomy) -> tuple[adopt_fixtures.Track, ...]:
    _bucket, genre = _bucket_and_genre(declared_taxonomy)
    return (
        adopt_fixtures.Track("r-ok", "present.flac", genre),
        adopt_fixtures.Track("r-missing", "absent.flac", genre, on_disk=False),
        adopt_fixtures.Track("r-gone", "removed.flac", genre, deleted=True),
    )


@pytest.fixture
def seeded(cfg, declared):
    """Configuration pointing at a disposable database holding those three rows."""
    adopt_fixtures.build(cfg, _tracks(declared))
    collection.reset_cache()
    return cfg


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


@pytest.fixture
def acknowledged(cfg):
    """A machine that has answered the backup question, through the real
    ``record_acknowledgment`` so a change to its shape fails here."""
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC, encoded once and copied per plan, because ffmpeg is slow."""
    from tests._containers import synth_container

    return synth_container(tmp_path_factory.mktemp("synth"), ".flac")


def _synthesized(music: Path, silence: Path) -> Path:
    """A real file in the library's music folder, where ``_synth`` would put one."""
    return Path(shutil.copyfile(silence, music / silence.name))


def _matching(cfg_value):
    """An identity provider that answers with the configured volume."""
    return lambda _path: cfg_value.library.volume_id


def _one_track_plan(cfg_value, declared_taxonomy, silence) -> tuple[adopt_plan.AdoptionPlan, Path]:
    """A plan with exactly one applicable entry, over a REAL file on disk, since
    what is under test is what reaches a user's file."""
    _bucket, genre = _bucket_and_genre(declared_taxonomy)
    path = _synthesized(Path(cfg_value.library.root) / "Music", silence)
    tags.write_genre(path, "Original Genre")
    plan = _plan_of(cfg_value, declared_taxonomy, [_row(cfg_value, path.name, genre, "c-1")])
    assert plan.applicable(), "the fixture built a plan with nothing to apply"
    return plan, path


def _apply(cfg_value, plan, declared_taxonomy, **overrides):
    """``apply_outstanding`` with a tag write and the configured volume, by default."""
    arguments = {
        "actor": "a-person",
        "tag_value": lambda *_: "Adopted Genre",
        "identity_provider": _matching(cfg_value),
        "mount_enumerator": lambda: (),
        **overrides,
    }
    return apply_cli.apply_outstanding(cfg_value, plan, declared_taxonomy, **arguments)


# ═══════════════════════════════════════════════════════════════════════════
# The session. This is the unit.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_whole_loop_runs_with_the_library_lock_actually_held(acknowledged, declared, silence):
    """The lock is observed FROM INSIDE the loop, in ``tag_value``, the middle of
    the pass: a measurement of the disk, not a claim about the call order.

    On the same pass: the lock is RELEASED afterwards, measured by taking it
    again; the memberships come back as the mapping the tree writer takes, for
    the entries PLACED, valued with locations and never content identifiers
    (U55); the collector writes nothing to the database, since sessions do not
    nest; and the ledger records whoever answered the gate (R34).
    """
    plan, path = _one_track_plan(acknowledged, declared, silence)
    db = Path(acknowledged.library.db_path)
    db_before = db.stat().st_mtime_ns if db.exists() else None
    holders: list[object] = []

    def tag_value(_entry, _declared):
        holders.append(session.read_lock_holder(session.lock_path(acknowledged)))
        return "Adopted Genre"

    report, memberships = _apply(
        acknowledged, plan, declared, actor="the-approver", tag_value=tag_value
    )

    assert len(holders) == 1, "the loop did not reach the one entry the plan holds"
    assert holders[0] is not None, (
        "the tag write happened with no holder recorded against the library lock, "
        "which is the residual's condition unchanged"
    )
    assert len(report.applied) == 1
    assert tags.read_genre_from_file(path) == "Adopted Genre"
    with session.session_lock(acknowledged):
        pass

    landed = [entry for entry in plan.applicable() if entry.entry_id in set(report.applied)]
    assert dict(memberships) == apply_cli.membership_locations(landed, declared)
    assert memberships, "the loop placed an entry and reported no membership for it"
    placed = [value for values in memberships.values() for value in values]
    assert placed and all(str(path) == value for value in placed), (
        "the collector grouped something that is not a location, so handing it to "
        "write_tree_membership would match nothing and report a clean session"
    )
    assert not set(placed) & {entry.content_id for entry in plan.applicable()}, (
        "the collector is back to grouping content identifiers, which is the defect"
    )

    db_after = db.stat().st_mtime_ns if db.exists() else None
    assert db_after == db_before, "the collector reached the database it is written not to touch"
    assert {entry.actor for entry in adopt_apply.read(acknowledged).applied} == {"the-approver"}


def test_the_analysis_watch_is_armed_on_the_library_root(acknowledged, declared, silence):
    """R17's fifth surface, runtime half: a watch over no roots reports a clean
    session whatever happened, so a real analysis file is moved from inside
    ``tag_value`` and the session must refuse.

    The file sits BESIDE the music folder, not in it: narrowing the root to
    ``Music`` killed no test until it moved up one level.
    """
    plan, _path = _one_track_plan(acknowledged, declared, silence)
    grid = Path(acknowledged.library.root) / "ANLZ0001.DAT"
    grid.write_bytes(b"not a real grid, and never written by this product")

    def tag_value(_entry, _declared):
        grid.rename(grid.with_name("ANLZ0002.DAT"))
        return "Adopted Genre"

    with pytest.raises(CratekitError):
        _apply(acknowledged, plan, declared, tag_value=tag_value)


def test_the_analysis_watch_reaches_a_share_outside_the_library_root(
    acknowledged, declared, tmp_path, silence
):
    """R-14: a database acknowledged outside the library root takes its analysis
    share with it, so the root alone holds no grid. A grid there rewritten inside
    the pass has to be seen."""
    share = tmp_path / "home" / "rekordbox" / "share"
    outside = replace(
        acknowledged,
        library=replace(
            acknowledged.library,
            db_path=share.parent / "master.db",
            db_outside_root_acknowledged_on="2026-09-11",
        ),
    )
    plan, _path = _one_track_plan(outside, declared, silence)
    grid = share / "PIONEER" / "USBANLZ" / "8d2" / "one" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True)
    grid.write_bytes(b"not a real grid, and never written by this product")
    assert grid not in session.analysis_files_under([outside.library.root]), (
        "the grid sits under the library root, so this cannot show the root alone misses it"
    )

    def tag_value(_entry, _declared):
        grid.write_bytes(b"a rewritten grid, longer than the one that was there")
        return "Adopted Genre"

    with pytest.raises(CratekitError) as excinfo:
        _apply(outside, plan, declared, tag_value=tag_value)
    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified", cause
    assert any(str(grid) in line for line in cause.detail["changed"]), cause.detail


def test_the_workflow_name_and_the_registry_verb_name_cannot_drift():
    """``WORKFLOW`` is what the session log records this run under; nothing reads
    that log in a fixture, so only a comparison can see the two drift apart."""
    assert apply_cli.WORKFLOW == registry.entry("adopt.apply").name


def _refused_and_untouched(cfg_value, plan, declared, path, code, **overrides) -> None:
    """The apply refuses with ``code``, and neither the file nor the ledger moved."""
    before = path.read_bytes()
    with pytest.raises(CratekitError) as excinfo:
        _apply(cfg_value, plan, declared, **overrides)
    assert excinfo.value.cause.code == code
    assert path.read_bytes() == before, (
        "a refused apply rewrote the file anyway, which is a refusal that has "
        "already done the thing it refused"
    )
    assert adopt_apply.read(cfg_value).entry_ids() == frozenset()


def test_an_unacknowledged_machine_rewrites_no_file(cfg, declared, silence):
    """Refusal two of three, on the state every library is in before a person
    answers the backup question, which is the state adoption most often meets."""
    plan, path = _one_track_plan(cfg, declared, silence)
    _refused_and_untouched(cfg, plan, declared, path, ExitCode.ACK_REQUIRED)


def test_a_volume_whose_identity_moved_rewrites_no_file(acknowledged, declared, silence):
    """Refusal three of three, which must happen before any path is resolved; the
    file is the only witness that tells "refused first" from "refused after"."""
    plan, path = _one_track_plan(acknowledged, declared, silence)
    _refused_and_untouched(
        acknowledged,
        plan,
        declared,
        path,
        ExitCode.LIBRARY_UNAVAILABLE,
        identity_provider=lambda _path: FOREIGN_VOLUME,
    )


def test_a_second_run_holding_the_lock_rewrites_no_file(acknowledged, declared, silence):
    """Refusal one of three, the one the residual measured as absent. The lock is
    taken on a separate handle, as another run would hold it (conformance 6)."""
    plan, path = _one_track_plan(acknowledged, declared, silence)
    lock = session.lock_path(acknowledged)
    lock.parent.mkdir(parents=True, exist_ok=True)
    contender = open(lock, "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        _refused_and_untouched(acknowledged, plan, declared, path, ExitCode.LIBRARY_BUSY)
    finally:
        contender.close()


def test_a_nested_session_is_refused_rather_than_deadlocking(acknowledged, declared, silence):
    """The composition the collector avoids, driven once so the module docstring's
    argument is a measured fact rather than a reading of ``session_lock``."""
    plan, _path = _one_track_plan(acknowledged, declared, silence)

    def nesting(_entry, _folder, _sub):
        with session.session_lock(acknowledged):
            pass

    with pytest.raises(session.SessionComposition):
        with session.assert_gates(
            acknowledged,
            workflow=apply_cli.WORKFLOW,
            analysis_roots=(acknowledged.library.root,),
            identity_provider=_matching(acknowledged),
            mount_enumerator=lambda: (),
        ):
            nesting(plan.applicable()[0], "folder", "sub")


# ═══════════════════════════════════════════════════════════════════════════
# The approval, the gate, and the shell
# ═══════════════════════════════════════════════════════════════════════════


def test_the_approval_gate_is_found_by_digest_source_not_by_position():
    """Reordering the declared gates must not change which question is asked, or
    the verb would ask about cloud sync and take the answer as an approval. An
    absent question is not a granted answer."""
    entry = registry.entry("adopt.apply")
    assert apply_cli._approval_gate(entry).name == GATE

    reversed_entry = replace(entry, gates=tuple(reversed(entry.gates)))
    assert apply_cli._approval_gate(reversed_entry).name == GATE

    with pytest.raises(CratekitError) as excinfo:
        apply_cli._approval_gate(replace(entry, gates=()))
    assert excinfo.value.cause.reason == "internal-error"


def test_the_resume_names_the_job_and_carries_the_run_that_holds_the_approval():
    """A job frozen by this build carries its run, so the resume continues the run
    holding the approval; one frozen by an older build carries none, and still
    resumes to a valid command line that refuses at the gate."""

    class _Job:
        job_id = "job-7"
        payload = {jobs.GATE_RUN_KEY: "run-3"}

    class _Older:
        job_id = "job-7"
        payload = {}

    assert apply_cli.adopt_apply_argv(_Job()) == [
        "--run",
        "run-3",
        "adopt",
        "apply",
        "--job",
        "job-7",
    ]
    assert apply_cli.adopt_apply_argv(_Older()) == ["adopt", "apply", "--job", "job-7"]


# ═══════════════════════════════════════════════════════════════════════════
# The census over the person's own collection
# ═══════════════════════════════════════════════════════════════════════════


def test_the_census_is_the_library_and_every_row_of_it_is_carried(seeded, declared):
    """Every live row comes back classified, the tombstone is skipped, and the one
    row on disk with a routable genre is the only one the plan can act on. Two
    builds of the unchanged library give one digest, across a cleared cache, or
    every approval would be stale on its first resume."""
    scanned = apply_cli.census(seeded, declared)
    by_id = {track.content_id: track for track in scanned}

    assert set(by_id) == {"r-ok", "r-missing", *adopt_fixtures.BASELINE_CONTENT_IDS}, (
        "the census dropped a row, or invented one; a tombstone must be skipped "
        "and every other row must be carried"
    )
    assert by_id["r-ok"].readability is adopt_scan.Readability.READABLE
    assert by_id["r-ok"].disposition is adopt_scan.Disposition.ROUTE
    assert by_id["r-missing"].readability is adopt_scan.Readability.MISSING
    assert by_id["r-missing"].disposition is adopt_scan.Disposition.EXCLUDED

    plan = apply_cli.current_plan(seeded, declared)
    assert plan.content_ids() == set(by_id)
    assert [entry.content_id for entry in plan.applicable()] == ["r-ok"]
    assert plan.tree == declared.tree.id

    collection.reset_cache()
    assert apply_cli.current_plan(seeded, declared).digest() == plan.digest()
    assert plan.digest()


def test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing(cfg, declared):
    """The LIMIT of what the census can say: ``scan_rows`` skips a deleted row, so
    only the COLLECTION tells the two zeroes apart."""
    adopt_fixtures.build(
        cfg, (adopt_fixtures.Track("r-gone", "gone.flac", "Techno", deleted=True),)
    )
    collection.reset_cache()
    tombstoned = apply_cli.census(cfg, declared)
    live_rows = [row for row in collection.read_collection(cfg) if not row.deleted]

    adopt_fixtures.build(cfg, ())
    collection.reset_cache()
    empty = apply_cli.census(cfg, declared)

    assert adopt_scan.categories(tombstoned) == adopt_scan.categories(empty)
    assert len(tombstoned) == len(empty) == len(adopt_fixtures.BASELINE_CONTENT_IDS)
    assert len(live_rows) == len(adopt_fixtures.BASELINE_CONTENT_IDS), (
        "the collection is what tells the two zeroes apart, and it must be able to"
    )


def test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag(seeded):
    """R19, driven against a MODIFIED taxonomy so the value is resolved and not
    merely equal to the shipped constant."""
    declared = taxonomy.default_taxonomy()
    moved = replace(declared, tree=replace(declared.tree, id=TREE_ID))
    assert apply_cli.current_plan(seeded, moved).tree == TREE_ID


def test_the_census_classifies_against_the_taxonomy_its_caller_resolved(seeded):
    """``declared`` is a PARAMETER: handed a taxonomy that calls the fixture's genre
    too coarse, the census must stop routing it, or one plan entry could be built
    from two taxonomies at once."""
    declared = taxonomy.default_taxonomy()
    routed = apply_cli.census(seeded, declared)
    assert any(track.disposition is adopt_scan.Disposition.ROUTE for track in routed)

    _bucket, genre = _bucket_and_genre(declared)
    narrowed = replace(
        declared,
        fallback=replace(
            declared.fallback,
            too_coarse_as_source=(*declared.fallback.too_coarse_as_source, genre),
        ),
    )
    collection.reset_cache()
    starved = apply_cli.census(seeded, narrowed)
    assert not any(track.disposition is adopt_scan.Disposition.ROUTE for track in starved), (
        "the census routed against a taxonomy its caller did not pass, so an "
        "entry can be built from two taxonomies at once"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The shell, driven through the real dispatcher
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def installed(library, monkeypatch):
    """A machine the real ``cli.run`` can load, set up rather than half set up.

    The dispatcher loads configuration for itself, so the file is saved. The
    library has something applicable, or every test would take the no-op path,
    and the volume and acknowledgment are answered, or every resume would stop
    on the gate rather than on the thing it asks about.
    """
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, _tracks(taxonomy.default_taxonomy()))
    collection.reset_cache()
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: resolved.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


def _queued() -> list:
    with jobs.open_store() as store:
        return [
            held
            for held in jobs.list_jobs(store)
            if held.handler_key == registry.entry("adopt.apply").handler_key
        ]


def _decided(answer: str) -> tuple[str, dict]:
    """The gate met, then answered as a separate recorded act: the run and the refusal."""
    code, refused = drive(APPLY)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    return run_id, refused


def test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest(installed):
    """R34's two acts, driven, then what the frozen payload holds: the digest the
    approval was recorded against has to travel with the job.

    THE RESUME THE DRIVER SPAWNS CAN ACTUALLY PROCEED. The gate is explicit, so a
    resume argv naming only the job minted a fresh run and refused for ever
    (driven 2026-08-23). The real ``argv_for`` output is driven here, and what it
    reaches is the membership write's refusal on an uncut tree, proof it got past
    the gate.
    """
    verb = registry.entry("adopt.apply")
    expected = apply_cli.current_plan(installed, taxonomy.default_taxonomy())

    run_id, refused = _decided("approve")
    assert refused["cause"]["detail"]["gate"] == GATE
    code, envelope = drive(["--run", run_id, *APPLY])
    assert code == int(ExitCode.OK), envelope

    held = _queued()
    assert len(held) == 1, "an approved run queued something other than exactly one job"
    assert held[0].payload["tree"] == expected.tree
    assert held[0].payload["digest"] == expected.digest(), (
        "the queued job does not carry the digest its approval was recorded "
        "against, so a resume cannot tell this plan from one that has moved"
    )
    assert envelope["data"]["job_id"] == held[0].job_id
    assert envelope["verb"] == verb.name

    argv = cli_jobs.argv_for(held[0])
    assert "--job" in argv and held[0].job_id in argv
    code, resumed = drive(argv)
    assert code != int(ExitCode.DECISION_REQUIRED), (
        f"the resume the driver spawns refuses its own gate: {resumed.get('cause')}. "
        f"A job whose own resume cannot answer its gate is a job nothing can advance"
    )
    assert len(_queued()) == 1, "the resume queued a second record"
    assert resumed["cause"]["reason"] == "no-evidence", resumed
    assert resumed["cause"]["inner"]["reason"] == "tree-unconverged", resumed
    with jobs.open_store() as store:
        assert jobs.get(store, held[0].job_id).state is jobs.JobState.FAILED
    assert adopt_apply.read(installed).entry_ids() == frozenset(), (
        "the applied ledger marked entries over an adoption that placed nothing"
    )


def test_a_declined_run_queues_nothing_at_all(installed):
    """Abort is a real answer, measured on the queue rather than the word."""
    run_id, _refused = _decided("abort")
    code, envelope = drive(["--run", run_id, *APPLY])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["job_id"] == "", (
        "R-234: cli.output requires job_id to be a string, so a null here failed "
        "the declared job_state/1 schema this verb emits"
    )
    assert _queued() == [], "a declined adoption was queued anyway"


def test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused(
    installed, monkeypatch, silence
):
    """The gate is OFFERED the digest, which is what makes a stale answer visible;
    dropping it once killed no test. The plan is moved by giving the census a
    row, as a real library moves."""
    plan_before = apply_cli.current_plan(installed, taxonomy.default_taxonomy())
    run_id, _refused = _decided("approve")

    path = _synthesized(Path(installed.library.root) / "Music", silence)
    _bucket, genre = _bucket_and_genre(taxonomy.default_taxonomy())
    scanned = tuple(
        adopt_scan.scan_rows(
            [_row(installed, path.name, genre, "c-moved")],
            taxonomy.default_taxonomy(),
            root=installed.library.root,
            probe=_readable,
        )
    )
    monkeypatch.setattr(apply_cli, "census", lambda _cfg, _declared, **_scope: scanned)
    assert apply_cli.current_plan(installed, taxonomy.default_taxonomy()).digest() != (
        plan_before.digest()
    ), "the fixture did not actually move the plan, so the assertion below is empty"

    code, envelope = drive(["--run", run_id, *APPLY])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert _queued() == [], "a plan that moved after approval was queued anyway"


def test_a_resume_reconciles_a_claim_a_dead_driver_left_behind(installed):
    """Reconcile, not get: a row saying running while no driver holds the lock is
    the state a killed driver leaves. Swapping ``reconcile`` for ``get`` once
    killed no test. The job reaches a terminal state, which it can only do if the
    row was re-derived and the item then attempted."""
    run_id, job_id = approve_and_queue(APPLY, GATE)

    with jobs.open_store() as store:
        jobs.transition(store, job_id, jobs.JobState.RUNNING)
        assert jobs.get(store, job_id).state is jobs.JobState.RUNNING

    code, resumed = drive(["--run", run_id, *APPLY, "--job", job_id])
    assert code != int(ExitCode.OK)
    assert resumed["cause"]["reason"] == "no-evidence", resumed

    with jobs.open_store() as store:
        reconciled = jobs.get(store, job_id)
        assert reconciled.state is jobs.JobState.FAILED
        assert [item.state for item in jobs.items(store, job_id)] == [jobs.ItemState.FAILED]


# ═══════════════════════════════════════════════════════════════════════════
# R-693: the approval gate shows the plan it asks about
# ═══════════════════════════════════════════════════════════════════════════


def _shown_matches(shown: dict, document: dict) -> None:
    assert shown["items"] == document["listed"]
    assert shown["digest"] == document["digest"]
    assert shown["count"] == len(document["listed"])
    assert shown["tree"] == document["tree"]
    assert shown["counts"] == document["counts"]
    assert shown["collisions"] == document["collisions"]


def test_the_approval_gate_shows_every_entry_the_digest_was_taken_over(installed):
    """The gate's ``shown`` holds the entries the digest lists, the applicable
    ones, with the digest, the tree, the counts per disposition and the
    collisions; what the plan will not touch is a count (R-693). A resume on a
    run holding no answer meets the same gate over the rebuilt plan and shows it
    the same way."""
    plan = apply_cli.current_plan(installed, taxonomy.default_taxonomy())
    document = adopt_plan.to_json(plan)
    listed = {entry.entry_id for entry in plan.applicable()}
    document["listed"] = [entry for entry in document["entries"] if entry["id"] in listed]
    assert 0 < len(document["listed"]) < len(document["entries"]), (
        "the fixture needs an applicable entry and one the plan will not touch, "
        "or the screen's choice between them cannot be seen"
    )

    run_id, refused = _decided("approve")
    _shown_matches(refused["cause"]["detail"]["shown"], document)
    assert _queued() == []
    _approved, envelope = drive(["--run", run_id, *APPLY])
    job_id = envelope["data"]["job_id"]

    code, refused = drive([*APPLY, "--job", job_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    _shown_matches(refused["cause"]["detail"]["shown"], document)
