"""R-235: the two verbs over the tree registry, driven through the real dispatcher.

WHAT THIS FILE IS FOR THAT ``test_cutover_precheck.py`` CANNOT BE. That file
drives ``tree_registry.flip`` as a library, with a root identifier the test
makes up. Nothing there finds a root, asks a gate, or is reachable by a person.
Here every scenario goes through ``cli.run``, the root is a row in a real
database file, and the approval is R34's two acts.

THE LIBRARY IS A TEMPORARY ONE IN EVERY PART, the library root included. The
registry is library state, beside the library root, so a fixture that redirected
the configuration and the database and left the root alone would record its
cutovers somewhere a real run reads.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.cli import cutover, doctor
from cratekit.core import config, preflight, rb_writer, session, snapshot, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests import adopt_fixtures, cutover_fixtures
from tests.cli_drive import approve_and_queue, drive
from tests.test_adoption import _bucket_and_genre
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION

DECLARED = taxonomy.default_taxonomy()
TREE = DECLARED.tree.id
DISPLAY = DECLARED.tree.display
CUTOVER_GATE = "tree.cutover.approve"
REVERT_GATE = "tree.revert.approve"
TODAY = date(2026, 9, 27)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reader_cache():
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as ``test_adopt_workers`` patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )
    monkeypatch.setattr(cutover, "_today", lambda: TODAY)


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def _tracks() -> tuple[adopt_fixtures.Track, ...]:
    _bucket, genre = _bucket_and_genre(DECLARED)
    return (
        adopt_fixtures.Track("r-one", "one.flac", genre),
        adopt_fixtures.Track("r-two", "two.flac", genre),
    )


@pytest.fixture
def machine(library, monkeypatch):
    """A set-up machine whose library holds tracks and no tree root yet."""
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
    adopt_fixtures.build(resolved, _tracks())
    collection.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


def _add_folder(cfg: config.Config, name: str, *, under: str | None = None) -> str:
    return cutover_fixtures.add_folder(cfg, name, under=under)


def _snapshot(cfg: config.Config) -> Path:
    return cutover_fixtures.verified_snapshot(cfg)


def _export(cfg: config.Config) -> Path:
    return cutover_fixtures.fresh_export(cfg)


@pytest.fixture
def ready(machine):
    """A library the precheck passes, holding exactly one root for the tree."""
    _snapshot(machine)
    export = _export(machine)
    root_id = _add_folder(machine, DISPLAY)
    return machine, export, root_id


def _cutover(export: Path, tree: str = TREE) -> list[str]:
    return ["tree", "cutover", tree, "--export", str(export)]


def _revert(tree: str = TREE) -> list[str]:
    return ["tree", "revert", tree]


def _two_acts(verb: list[str], gate: str, option: str) -> tuple[int, dict, dict]:
    """R34's two acts, then the acting drive. Answers its code, envelope and the offer."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _cut_over(export: Path) -> dict:
    code, acted, _refused = _two_acts(_cutover(export), CUTOVER_GATE, "approve")
    assert code == int(ExitCode.OK), acted
    return acted


# ---------------------------------------------------------------------------
# The cutover
# ---------------------------------------------------------------------------


def test_the_plan_names_the_root_and_approval_records_that_tree_alone(ready):
    cfg, export, root_id = ready
    code, acted, refused = _two_acts(_cutover(export), CUTOVER_GATE, "approve")

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    (item,) = shown["items"]
    assert item == {
        "tree": "genre_energy",
        "display": "BY GENRE + ENERGY",
        "root_id": root_id,
        "root_name": "BY GENRE + ENERGY",
        "source": "taxonomy",
        "export": str(export.resolve()),
        "registry": str(Path(cfg.library.root) / ".cratekit" / "coupled" / "tree_registry.json"),
        "database": str(Path(cfg.library.root) / "db" / "master.db"),
        "precheck_passed": "no-open-run no-pending-intake-xml fresh-export verified-snapshot",
    }
    assert shown["precheck"] == {
        "no-open-run": "passed",
        "no-pending-intake-xml": "passed",
        "fresh-export": "passed",
        "verified-snapshot": "passed",
    }
    assert shown["anchors_to"] == f"BY GENRE + ENERGY, row {root_id}"
    assert shown["writes"] == item["registry"]
    assert shown["reads"] == item["database"]

    after = tree_registry.read(cfg)
    record = after.record(TREE)
    assert record is not None
    assert record.mode == tree_registry.Mode.DATABASE
    assert record.root_id == root_id
    assert record.cutover_on == TODAY
    assert record.source is tree_registry.DerivationSource.TAXONOMY
    assert after.tree_ids() == (TREE,), "a tree nobody named was recorded beside it"
    assert after.is_on_the_bridge(DECLARED.intake.id)
    assert acted["data"]["totals"] == {"recorded": True, "cutover_on": TODAY.isoformat()}
    assert acted["data"]["digest"] == shown["digest"]


def test_nothing_is_recorded_until_the_person_approves(ready):
    cfg, export, _root_id = ready
    code, refused = drive(_cutover(export))
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert refused["cause"]["detail"]["explicit"] is True
    assert not tree_registry.path_for(cfg).exists()

    decided, _ = drive(
        ["run", "decide", refused["run_id"], CUTOVER_GATE, "approve", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)
    assert not tree_registry.path_for(cfg).exists(), (
        "recording the decision recorded the cutover, so the answer and the act "
        "are one step and a person who only answered has already gone through "
        "the one way door"
    )


def test_an_abort_records_nothing(ready):
    cfg, export, _root_id = ready
    code, acted, _refused = _two_acts(_cutover(export), CUTOVER_GATE, "abort")
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE)


def test_a_library_with_no_root_is_refused_and_no_root_is_created(machine):
    _snapshot(machine)
    export = _export(machine)
    code, refused = drive(_cutover(export))

    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "cutover-root-unresolved"
    assert refused["cause"]["detail"]["found"] == 0
    assert tree_registry.read(machine).is_on_the_bridge(TREE)
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        assert list(handle.get_playlist(Name=DISPLAY)) == [], (
            "the verb created the root it could not find, which is the silent "
            "parallel tree"
        )
    finally:
        rb_writer.close_db(handle)


def test_two_roots_of_one_name_are_refused(ready):
    cfg, export, root_id = ready
    twin = _add_folder(cfg, DISPLAY)
    code, refused = drive(_cutover(export))

    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "cutover-root-unresolved"
    assert refused["cause"]["detail"]["found"] == 2
    assert sorted(refused["cause"]["detail"]["roots"]) == sorted([root_id, twin])
    assert tree_registry.read(cfg).is_on_the_bridge(TREE)


def test_a_namesake_nested_under_another_folder_is_not_a_root(ready):
    cfg, export, root_id = ready
    elsewhere = _add_folder(cfg, "somewhere else")
    _add_folder(cfg, DISPLAY, under=elsewhere)

    _cut_over(export)
    assert tree_registry.read(cfg).record(TREE).root_id == root_id


def test_a_nested_namesake_alone_is_no_root_at_all(machine):
    _snapshot(machine)
    export = _export(machine)
    elsewhere = _add_folder(machine, "somewhere else")
    _add_folder(machine, DISPLAY, under=elsewhere)

    code, refused = drive(_cutover(export))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["detail"]["found"] == 0


def test_a_playlist_of_the_trees_name_is_not_a_root(machine):
    _snapshot(machine)
    export = _export(machine)
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        handle.create_playlist(DISPLAY)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, refused = drive(_cutover(export))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["detail"]["found"] == 0


def _open_a_run(cfg: config.Config, export: Path) -> None:
    from cratekit.cli import output

    session.write_record(
        session.SessionRecord(
            session_id="s-open",
            workflow="deferred-routing",
            started=output.timestamp(),
            state=session.SessionState.OPEN,
        ),
        cfg,
    )


def _leave_intake_xml(cfg: config.Config, export: Path) -> None:
    staging = Path(cfg.paths.download_staging)
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "run-1_synced.xml").write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")


def _remove_the_export(cfg: config.Config, export: Path) -> None:
    export.unlink()


def _remove_the_snapshot(cfg: config.Config, export: Path) -> None:
    import shutil

    shutil.rmtree(snapshot.store_root(cfg))


@pytest.mark.parametrize(
    ("spoil", "reason", "check"),
    [
        (_open_a_run, "cutover-open-run", "no-open-run"),
        (_leave_intake_xml, "cutover-xml-pending", "no-pending-intake-xml"),
        (_remove_the_export, "cutover-export-missing", "fresh-export"),
        (_remove_the_snapshot, "cutover-snapshot-missing", "verified-snapshot"),
    ],
)
def test_each_precheck_failure_refuses_before_anything_is_recorded(ready, spoil, reason, check):
    cfg, export, _root_id = ready
    spoil(cfg, export)
    code, refused = drive(_cutover(export))

    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == reason
    failed = [row["check"] for row in refused["cause"]["detail"]["precheck"] if not row["passed"]]
    assert failed == [check], "the refusal did not carry each precheck's own result"
    assert len(refused["cause"]["detail"]["precheck"]) == 4
    assert "gate" not in refused["cause"]["detail"], (
        "a library that cannot cut over was asked to approve a cutover"
    )
    assert not tree_registry.path_for(cfg).exists()


def test_two_failing_prechecks_are_both_named_on_one_run(ready):
    cfg, export, _root_id = ready
    _leave_intake_xml(cfg, export)
    _remove_the_snapshot(cfg, export)
    _code, refused = drive(_cutover(export))

    assert refused["cause"]["reason"] == "cutover-xml-pending"
    failed = [row["check"] for row in refused["cause"]["detail"]["precheck"] if not row["passed"]]
    assert failed == ["no-pending-intake-xml", "verified-snapshot"]


def test_a_precheck_that_fails_after_the_approval_still_refuses(ready):
    """The approving invocation is held to the precheck too, not only the offer."""
    cfg, export, _root_id = ready
    code, refused = drive(_cutover(export))
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, CUTOVER_GATE, "approve", "--actor", "a-person"])

    _leave_intake_xml(cfg, export)
    code, acted = drive(["--run", run_id, *_cutover(export)])
    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["reason"] == "cutover-xml-pending"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE)


def test_a_root_that_changed_after_the_offer_makes_the_approval_stale(ready):
    cfg, export, root_id = ready
    code, refused = drive(_cutover(export))
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, CUTOVER_GATE, "approve", "--actor", "a-person"])

    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        handle.delete_playlist(handle.get_playlist(ID=root_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    replacement = _add_folder(cfg, DISPLAY)
    assert replacement != root_id

    code, acted = drive(["--run", run_id, *_cutover(export)])
    assert code != int(ExitCode.OK), acted
    assert tree_registry.read(cfg).is_on_the_bridge(TREE), (
        "an approval given for one root recorded a cutover anchored to another"
    )


def test_a_tree_the_taxonomy_does_not_declare_is_refused(ready):
    cfg, export, _root_id = ready
    code, refused = drive(_cutover(export, tree="no_such_tree"))
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "cutover-tree-undeclared"
    assert refused["cause"]["detail"]["routing_tree"] == TREE
    named = sorted({TREE, DECLARED.intake.id})
    assert refused["cause"]["detail"]["cutover_trees"] == named
    (step,) = refused["cause"]["remediation"]["steps"]
    assert all(repr(tree_id) in step for tree_id in named), step
    assert not tree_registry.path_for(cfg).exists()


def test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree(ready):
    """R-746. The intake tree stayed on the bridge because flipping it would
    have refused the splice that landed new rows. The landing now chooses its
    medium by the tree's mode, so the refusal expired with the reason for it,
    and the intake tree anchors to its own root the way the routing tree does."""
    cfg, export, routing_root = ready
    intake_root = _add_folder(cfg, DECLARED.intake.display)
    code, acted, _refused = _two_acts(
        _cutover(export, tree=DECLARED.intake.id), CUTOVER_GATE, "approve"
    )
    assert code == int(ExitCode.OK), acted
    recorded = tree_registry.read(cfg)
    assert recorded.is_database_native(DECLARED.intake.id)
    assert recorded.record(DECLARED.intake.id).root_id == intake_root
    assert intake_root != routing_root
    assert recorded.is_on_the_bridge(TREE), "the routing tree was not asked about"


def test_a_tree_already_native_records_nothing_and_asks_nothing(ready):
    cfg, export, root_id = ready
    _cut_over(export)
    before = tree_registry.path_for(cfg).read_bytes()
    _add_folder(cfg, DISPLAY)

    code, again = drive(_cutover(export))
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert [w["code"] for w in again["warnings"]] == ["cutover-already-recorded"]
    assert root_id in again["warnings"][0]["message"]
    assert tree_registry.path_for(cfg).read_bytes() == before


def test_the_source_comes_off_the_taxonomy():
    assert cutover.derivation_source(DECLARED, TREE) is tree_registry.DerivationSource.TAXONOMY
    if DECLARED.catalog is not None:
        assert (
            cutover.derivation_source(DECLARED, DECLARED.catalog.id)
            is tree_registry.DerivationSource.CATALOGUE_CRAWL
        )


# ---------------------------------------------------------------------------
# Adoption, which is what the cutover was for
# ---------------------------------------------------------------------------


def _resume(job_id: str) -> list[str]:
    from cratekit.cli import jobs as cli_jobs
    from cratekit.core import jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def _memberships(cfg: config.Config) -> dict[str, list[str]]:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        found: dict[str, list[str]] = {}
        for row in handle.get_playlist():
            members = [
                str(entry.ContentID)
                for entry in handle.get_playlist_songs(PlaylistID=str(row.ID))
            ]
            if members:
                found[str(row.ID)] = sorted(members)
        return found
    finally:
        rb_writer.close_db(handle)


def _under(cfg: config.Config, root_id: str) -> set[str]:
    """Every playlist identifier two levels under ``root_id``."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        folders = [str(row.ID) for row in handle.get_playlist(ParentID=root_id)]
        return {
            str(row.ID)
            for folder in folders
            for row in list(handle.get_playlist(ParentID=folder))
        }
    finally:
        rb_writer.close_db(handle)


def _adopt() -> tuple[int, dict]:
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    return drive(_resume(job_id))


def test_an_uncut_library_refuses_adoption_and_names_the_cutover_verb(ready):
    cfg, _export_path, _root_id = ready
    code, resumed = _adopt()

    assert code != int(ExitCode.OK)
    inner = resumed["cause"]["inner"]
    assert inner["reason"] == "tree-unconverged"
    steps = " ".join(inner["remediation"]["steps"])
    assert f"crate tree cutover {TREE} --export" in steps, (
        "the refusal names no act a person can perform, which is R-235"
    )
    assert _memberships(cfg) == {}


def test_after_the_cutover_adoption_writes_membership_under_the_adopted_root(ready):
    cfg, export, root_id = ready
    _cut_over(export)
    code, resumed = _adopt()

    assert code == int(ExitCode.OK), resumed
    held = _memberships(cfg)
    assert held, "the apply reported success and the database holds no membership"
    assert sorted(member for members in held.values() for member in members) == [
        "r-one",
        "r-two",
    ]
    assert set(held) <= _under(cfg, root_id), (
        "the membership landed in a playlist that is not under the root the "
        "cutover adopted"
    )


# ---------------------------------------------------------------------------
# The revert
# ---------------------------------------------------------------------------


def test_a_revert_before_any_native_write_puts_the_tree_back_on_the_bridge(ready):
    cfg, export, root_id = ready
    _cut_over(export)
    code, acted, refused = _two_acts(_revert(), REVERT_GATE, "revert")

    assert code == int(ExitCode.OK), acted
    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert item["tree"] == TREE
    assert item["root"] == root_id
    assert item["cutover_on"] == TODAY.isoformat()
    assert acted["data"]["totals"] == {"reverted": True}
    assert tree_registry.read(cfg).is_on_the_bridge(TREE)
    assert tree_registry.read(cfg).record(TREE) is None


def test_a_revert_is_not_performed_until_it_is_approved(ready):
    cfg, export, _root_id = ready
    _cut_over(export)
    code, _refused = drive(_revert())
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert tree_registry.read(cfg).is_database_native(TREE)

    code, acted, _ = _two_acts(_revert(), REVERT_GATE, "abort")
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert tree_registry.read(cfg).is_database_native(TREE)


def test_a_revert_after_a_native_write_refuses_and_the_tree_stays_native(ready):
    cfg, export, root_id = ready
    _cut_over(export)
    code, resumed = _adopt()
    assert code == int(ExitCode.OK), resumed

    code, refused = drive(_revert())
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "cutover-native-write-taken"
    assert refused["cause"]["detail"]["tree_id"] == TREE
    assert len(refused["cause"]["detail"]["sessions"]) == 1
    assert "gate" not in refused["cause"]["detail"]
    record = tree_registry.read(cfg).record(TREE)
    assert record is not None and record.root_id == root_id


def test_a_native_write_taken_after_the_approval_still_refuses_the_revert(ready):
    """The guard under the registry lock is the one that holds, not the verb's."""
    cfg, export, _root_id = ready
    _cut_over(export)
    code, refused = drive(_revert())
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, REVERT_GATE, "revert", "--actor", "a-person"])

    code, resumed = _adopt()
    assert code == int(ExitCode.OK), resumed

    code, acted = drive(["--run", run_id, *_revert()])
    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["reason"] == "cutover-native-write-taken"
    assert tree_registry.read(cfg).is_database_native(TREE)


def test_a_revert_of_a_tree_on_the_bridge_writes_nothing_and_asks_nothing(machine):
    code, acted = drive(_revert())
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert [w["code"] for w in acted["warnings"]] == ["revert-nothing-recorded"]
    assert not tree_registry.path_for(machine).exists()


def test_a_write_to_another_tree_does_not_close_this_trees_door(ready):
    cfg, export, _root_id = ready
    _cut_over(export)
    from cratekit.cli import output

    session.write_record(
        session.SessionRecord(
            session_id="s-other",
            workflow="tree-membership",
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            change=session.ChangeSummary(
                (
                    session.TreeChange(tree="some_other_tree", created=4),
                    session.TreeChange(tree=TREE, created=0, updated=0),
                )
            ),
        ),
        cfg,
    )
    assert tree_registry.native_writes(cfg, TREE) == ()
    code, acted, _ = _two_acts(_revert(), REVERT_GATE, "revert")
    assert code == int(ExitCode.OK), acted
    assert tree_registry.read(cfg).is_on_the_bridge(TREE)


# ---------------------------------------------------------------------------
# Doctor
# ---------------------------------------------------------------------------


def _tree_finding(cfg: config.Config) -> doctor.Finding:
    report = doctor.run(cfg)
    (finding,) = [f for f in report.findings if f.key == "tree.registry"]
    return finding


def test_doctor_lists_every_declared_tree_on_a_library_nobody_has_cut_over(machine):
    finding = _tree_finding(machine)
    assert finding.status is doctor.Status.OK
    assert f"{TREE} is on the XML bridge" in finding.detail
    assert f"{DECLARED.intake.id} is on the XML bridge" in finding.detail


def test_doctor_shows_the_mode_and_the_anchored_root_after_a_cutover(ready):
    cfg, export, root_id = ready
    _cut_over(export)
    finding = _tree_finding(cfg)

    assert finding.status is doctor.Status.OK
    assert f"{TREE} is database native, anchored to root {root_id}" in finding.detail
    assert TODAY.isoformat() in finding.detail
    assert f"{DECLARED.intake.id} is on the XML bridge" in finding.detail
    assert str(tree_registry.path_for(cfg)) in finding.detail


def test_doctor_lists_and_fails_a_recorded_tree_the_taxonomy_does_not_declare(machine):
    registry = tree_registry.EMPTY.with_record(
        tree_registry.TreeRecord(
            tree_id="a_dropped_tree",
            mode=tree_registry.Mode.DATABASE,
            cutover_on=TODAY,
            root_id="root-9",
            source=tree_registry.DerivationSource.TAXONOMY,
        )
    )
    tree_registry.write(machine, registry)
    finding = _tree_finding(machine)
    assert "a_dropped_tree is database native, anchored to root root-9" in finding.detail
    assert finding.status is doctor.Status.FAIL


def test_doctor_fails_on_a_registry_it_cannot_read_rather_than_listing_the_bridge(machine):
    path = tree_registry.path_for(machine)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json\n", encoding="utf-8")
    finding = _tree_finding(machine)

    assert finding.status is doctor.Status.FAIL
    assert "XML bridge" not in finding.detail, (
        "an unreadable registry was reported as every tree being on the bridge"
    )


# ---------------------------------------------------------------------------
# What the review found, closed
# ---------------------------------------------------------------------------


def test_the_steps_the_refused_adoption_names_are_the_steps_that_work(ready):
    """The remedy as a person follows it: refused, cut over, apply again.

    DRIVEN BECAUSE THE FIRST DRAFT OF THE STEP WAS FALSE. It named a resume of
    the refused job, and the engine refuses one: the job ended on a cause that
    is not retryable. A step nobody drove is the defect this unit closes.
    """
    cfg, export, root_id = ready
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, refused = drive(_resume(job_id))
    assert code != int(ExitCode.OK)
    steps = refused["cause"]["inner"]["remediation"]["steps"]
    assert "crate tree cutover" in steps[0]
    assert "crate adopt apply" in steps[1]
    assert "job resume" not in " ".join(steps)

    code, resumed = drive(["job", "resume", job_id])
    assert code != int(ExitCode.OK), "a resume retried a job the step says it cannot"
    assert resumed["cause"]["reason"] == "job-not-retryable"

    _cut_over(export)
    code, applied = _adopt()
    assert code == int(ExitCode.OK), applied
    held = _memberships(cfg)
    assert sorted(member for members in held.values() for member in members) == [
        "r-one",
        "r-two",
    ]
    assert set(held) <= _under(cfg, root_id)


def test_two_cutovers_offered_before_either_was_approved_record_one(ready):
    cfg, export, root_id = ready
    code, first = drive(_cutover(export))
    assert code == int(ExitCode.DECISION_REQUIRED)
    code, second = drive(_cutover(export))
    assert code == int(ExitCode.DECISION_REQUIRED)
    for offered in (first, second):
        decided, _ = drive(
            ["run", "decide", offered["run_id"], CUTOVER_GATE, "approve", "--actor", "a-person"]
        )
        assert decided == int(ExitCode.OK)

    code, acted = drive(["--run", first["run_id"], *_cutover(export)])
    assert code == int(ExitCode.OK), acted
    recorded = tree_registry.path_for(cfg).read_bytes()

    code, again = drive(["--run", second["run_id"], *_cutover(export)])
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert tree_registry.path_for(cfg).read_bytes() == recorded
    assert tree_registry.read(cfg).record(TREE).root_id == root_id


def _native(cfg: config.Config, tree_id: str, root_id: str, source) -> None:
    """Write one database native record, the way a hand edit or the verb would."""
    tree_registry.write(
        cfg,
        tree_registry.EMPTY.with_record(
            tree_registry.TreeRecord(
                tree_id=tree_id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=TODAY,
                root_id=root_id,
                source=source,
            )
        ),
    )


def test_doctor_reads_a_native_inbox_record_as_ok(machine):
    """R-787. The verb records the intake tree since #224, so doctor failing it
    sent the person to a revert that refuses once a native landing exists."""
    _native(machine, DECLARED.intake.id, "root-7", tree_registry.DerivationSource.TAXONOMY)
    finding = _tree_finding(machine)

    assert finding.status is doctor.Status.OK, finding.detail
    assert (
        f"{DECLARED.intake.id} is database native, anchored to root root-7 "
        f"since {TODAY.isoformat()}, rebuilt from taxonomy"
    ) in finding.detail
    assert "crate tree revert" not in finding.detail
    assert f"{TREE} is on the XML bridge" in finding.detail


def test_doctor_reads_an_inbox_the_verb_cut_over_as_ok(ready):
    """The record the verb itself writes, not one authored beside the fix."""
    cfg, export, _routing_root = ready
    intake_root = _add_folder(cfg, DECLARED.intake.display)
    code, acted, _refused = _two_acts(
        _cutover(export, tree=DECLARED.intake.id), CUTOVER_GATE, "approve"
    )
    assert code == int(ExitCode.OK), acted
    finding = _tree_finding(cfg)

    assert finding.status is doctor.Status.OK, finding.detail
    assert (
        f"{DECLARED.intake.id} is database native, anchored to root {intake_root}"
    ) in finding.detail


def test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create(machine):
    """The catalogue tree is declared and no verb records it (R39)."""
    assert DECLARED.catalog is not None
    _native(
        machine, DECLARED.catalog.id, "root-7", tree_registry.DerivationSource.CATALOGUE_CRAWL
    )
    finding = _tree_finding(machine)

    assert finding.status is doctor.Status.FAIL
    assert f"{DECLARED.catalog.id} is recorded database native" in finding.detail
    assert "crate tree revert" in finding.detail
    assert f"only {', '.join(sorted({TREE, DECLARED.intake.id}))} are" in finding.detail
    assert f"{TREE} is on the XML bridge" in finding.detail


def test_doctor_and_the_verb_read_one_set_of_cutover_trees(machine, monkeypatch):
    """R-787. One function names the trees a cutover may record and both ask it.

    Unpatched, the two answers are the one function's answer. Patched to a
    sentinel, doctor hands back the sentinel itself and the verb's acceptance
    moves with it, so neither can be holding a list of its own.
    """
    assert DECLARED.catalog is not None
    expected = frozenset({TREE, DECLARED.intake.id})
    _declared, may_cut_over, _reason = doctor._declared_trees(machine)
    assert may_cut_over == tree_registry.cutover_trees(DECLARED) == expected

    sentinel = frozenset({DECLARED.catalog.id})
    monkeypatch.setattr(tree_registry, "cutover_trees", lambda declared: sentinel)
    _declared, may_cut_over, _reason = doctor._declared_trees(machine)
    assert may_cut_over is sentinel
    assert (
        cutover.derivation_source(DECLARED, DECLARED.catalog.id)
        is tree_registry.DerivationSource.TAXONOMY
    )
    with pytest.raises(CratekitError) as refused:
        cutover.derivation_source(DECLARED, DECLARED.intake.id)
    assert refused.value.cause.reason == "cutover-tree-undeclared"


def test_the_catalogue_tree_is_refused_as_not_rebuildable(ready):
    """Declared, and named with its real source, so the registry's rule refuses it."""
    cfg, export, _root_id = ready
    assert DECLARED.catalog is not None
    _add_folder(cfg, DECLARED.catalog.display)
    code, refused = drive(_cutover(export, tree=DECLARED.catalog.id))

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "tree-unconverged"
    assert refused["cause"]["detail"]["tree_id"] == DECLARED.catalog.id
    assert refused["cause"]["detail"]["cutover_trees"] == sorted({TREE, DECLARED.intake.id})
    assert not tree_registry.path_for(cfg).exists()


def test_an_empty_export_is_no_export(ready):
    cfg, export, _root_id = ready
    export.write_bytes(b"")
    code, refused = drive(_cutover(export))

    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "cutover-export-missing"
    assert not tree_registry.path_for(cfg).exists()
