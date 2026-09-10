"""U53: the routing and rebuild workers, and the two verbs that reported work nobody did.

WHAT THIS FILE GUARDS THAT THE ENGINE SUITES CANNOT. ``tests/test_rebuild.py``
drives ``rebuild_tree`` directly and has always passed, and until this unit
NOTHING IN ``src`` CALLED IT, so a green run of that file said nothing about
whether the product ever rebuilt anything. The same is true one verb over:
``route.inbox`` asked its apply gate and returned the plan on both branches, and
``route.unplaced`` was the literal ``_plan([], ...)``. Neither defect is visible
to any assertion about the engine, because neither is about the engine.

SO EVERY TEST BELOW GOES THROUGH THE SHIPPED COMMAND LINE, on a disposable
database in a temporary directory, and then reads the DATABASE back rather than
the envelope. An envelope is what the defect produced; the membership rows are
what it did not.

THE FOUR CLAIMS, and where each is proved:

1. a queued rebuild and a queued resort run their items from pending to done and
   the tree they wrote holds the tracks
   -> ``test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track``
      and ``test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track``
2. neither queued verb can file a job with nothing to claim
   -> ``test_neither_queued_verb_files_a_job_with_no_items``
      and ``test_neither_queued_verb_files_a_job_at_all_with_no_native_tree``
3. the inbox applies when confirmed and does not when declined, and the two
   envelopes differ where a caller can see
   -> ``test_the_confirmed_inbox_applies_and_the_declined_one_does_not``
4. unplaced reports the library rather than a constant
   -> ``test_unplaced_reports_the_rows_no_governed_tree_holds``,
      ``test_unplaced_over_a_fully_placed_library_reports_none`` and
      ``test_unplaced_says_when_it_could_not_compare``

WHAT IS SUPPLEMENTED. Binding the first caller in ``src`` to an engine makes
this unit the owner of that engine's unreviewed failure paths, which is the
lesson filed at
``docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md``.
Three of those paths are driven here through the worker rather than through the
engine: the missing acknowledgment, the absent music directory, and a registry
naming a root the database does not have.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import io
import json
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output
from cratekit.core import config, jobs, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"

#: One file under the music directory and one in the intake folder, so the two
#: derivations under test read disjoint sets and a test cannot pass because the
#: other verb happened to have placed the same track.
SHELVED = "First Track.flac"
ARRIVED = "Second Track.flac"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library) -> config.Config:
    """A set-up machine whose configuration is on DISK, not monkeypatched in.

    The verbs here run through ``cli.run``, which loads configuration for itself,
    so a substituted ``config.load`` would prove that the substitute works. The
    application pin is recorded because an unset one refuses at the database
    gate, which is a refusal about the fixture rather than about the verb.
    """
    cfg = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """Everything about THIS machine a temporary library cannot speak for.

    The same seams the sibling write suites patch, for the same reason: that
    these guards refuse is proved in ``tests/test_rb_writer_db.py``, and proving
    it again here would only prove the fixture.
    """
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION
    )
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture
def acknowledged(configured, monkeypatch):
    """The volume identity agrees and a recovery point has been acknowledged."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: configured.library.volume_id),
    )
    session.record_acknowledgment(configured, terminal=lambda: True)
    return configured


def _record_locations(db_path: Path, recorded: dict[str, str]) -> None:
    """Give the disposable database's rows the paths this run decided on.

    Written straight into the file BEFORE the guarded writer opens it, because
    creating a collection row is exactly what the additive whitelist forbids:
    intake makes those rows and these verbs only ever place rows that exist.
    """
    conn = sqlite3.connect(db_path)
    try:
        for content_id, path in recorded.items():
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = 0 WHERE ID = ?",
                (path, content_id),
            )
        conn.commit()
    finally:
        conn.close()


def _intake_dir(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / taxonomy.default_taxonomy().intake.display


@pytest.fixture
def stocked(configured) -> config.Config:
    """One file under the music directory and one in the intake folder.

    Both are real files with the right suffix and no tags at all, which is a
    state a library is genuinely in: the shipped rules route an untagged file to
    a declared fallback bucket, so nothing here depends on a tag writer.
    """
    (Path(configured.library.root) / "Music" / SHELVED).write_bytes(b"")
    intake = _intake_dir(configured)
    intake.mkdir(parents=True, exist_ok=True)
    (intake / ARRIVED).write_bytes(b"")
    return configured


@pytest.fixture
def native(stocked) -> str:
    """A database with a real adopted root, and a registry that has cut over.

    The root is a REAL row with a real identifier rather than a literal, because
    every walk in these engines goes down from that identifier and a made-up one
    would be refused by ``anchored_root`` before anything under test ran.
    """
    path = Path(stocked.library.db_path)
    _build_disposable_database(path)
    _record_locations(
        path,
        {
            "1": str(Path(stocked.library.root) / "Music" / SHELVED),
            "2": str(_intake_dir(stocked) / ARRIVED),
        },
    )
    handle = rb_writer.open_db(path, unlock=False, cfg=stocked)
    try:
        folder = rb_writer.ensure_folder(handle, TREE_DISPLAY)
        handle.session.commit()
        root_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    tree_registry.write(
        stocked,
        tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE_ID,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 8, 1),
                    root_id=root_id,
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        ),
    )
    return root_id


# ═══════════════════════════════════════════════════════════════════════════
# Driving
# ═══════════════════════════════════════════════════════════════════════════


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    assert out.getvalue().strip(), f"the verb printed nothing: {err.getvalue()}"
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def _items(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def _queued_jobs() -> tuple[jobs.Job, ...]:
    with jobs.open_store() as store:
        return jobs.list_jobs(store)


def _membership(cfg: config.Config, root_id: str) -> set[str]:
    """Every content identifier the governed tree holds, read back from the file.

    Read by walking DOWN from the adopted root identifier, which is the same walk
    the engine's own check makes and the only one that cannot be fooled by a
    namesake elsewhere in the library.
    """
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        held: set[str] = set()
        for node in rebuild.read_tree(handle, root_id):
            held |= set(node.content_ids)
        return held
    finally:
        rb_writer.close_db(handle)


# ═══════════════════════════════════════════════════════════════════════════
# Claim 1: the queued work actually runs
# ═══════════════════════════════════════════════════════════════════════════


def test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track(
    acknowledged, native
):
    """Pending to done, and then the DATABASE is asked what happened.

    The item state alone would not do it. ``jobs.drive`` transitions an item to
    done when its handler returns without raising, so a handler that returned
    immediately would satisfy every assertion about the queue while writing
    nothing, which is the shape of the defect this unit exists to close.
    """
    code, queued = _drive(["rebuild", "--actor", "a-person"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    assert [item.item_id for item in _items(job_id)] == [TREE_ID]
    assert all(item.state == jobs.ItemState.PENDING for item in _items(job_id))

    code, done = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1"}


def test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track(
    acknowledged, native
):
    """The same claim for the sibling verb, which shares the engine and not the shell."""
    code, queued = _drive(["route", "resort"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    assert [item.item_id for item in _items(job_id)] == [TREE_ID]

    code, done = _drive(["route", "resort", "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1"}


def test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed(monkeypatch):
    """Two properties of the two workers, taken where they can be seen alone.

    THE ITEM IS THE TREE. A worker that rebuilt every tree per item would do the
    whole sweep once per tree and report each pass as one item's work, and no
    assertion over a one-tree library could tell the two apart.

    EACH VERB WRITES UNDER ITS OWN WORKFLOW NAME, which is what the session log
    answers with when somebody asks which act touched their library. Two verbs
    sharing one name is a log that cannot answer the only question it is for.
    """
    from cratekit.cli import rebuild as rebuild_verb
    from cratekit.write import routing_cli

    seen: list[tuple[str, str]] = []

    def spy(cfg, *, tree_id, workflow, **rest):
        # NO DEFAULT ON ``workflow``. A spy that supplied one would answer the
        # question for a worker that named nothing, which is the half this test
        # exists to tell apart.
        del cfg, rest
        seen.append((tree_id, workflow))

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", spy)
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    assert rebuild_verb.handle(object(), item, None) is None
    assert routing_cli.handle_resort(object(), item, None) is None

    assert [tree for tree, _ in seen] == [TREE_ID, TREE_ID]
    workflows = [workflow for _, workflow in seen]
    assert workflows == [rebuild.REBUILD_WORKFLOW, routing_cli.RESORT_WORKFLOW]
    assert len(set(workflows)) == 2, workflows
    assert routing_cli.INBOX_WORKFLOW not in workflows


# ═══════════════════════════════════════════════════════════════════════════
# Claim 2: the zero item rule, in both directions
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_neither_queued_verb_files_a_job_with_no_items(acknowledged, native, argv):
    """A job with nothing to claim is walked once and reported as succeeded.

    ``jobs.drive`` has no way to tell an empty job from a finished one, so the
    queue reported a rebuild that happened over a library nothing had read. The
    property is asserted over the STORE rather than over the envelope, because
    the envelope is what the defect already produced.
    """
    del acknowledged, native
    code, envelope = _drive(argv)
    assert code == int(ExitCode.OK), envelope
    filed = _queued_jobs()
    assert filed, "the verb reported OK and filed nothing at all"
    for job in filed:
        assert _items(job.job_id), f"{job.handler_key} filed a job with no items"


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_neither_queued_verb_files_a_job_at_all_with_no_native_tree(configured, argv):
    """The other half, and it is not a refusal.

    A library that has never flipped a tree is the state every library is in
    until its first cutover, and nothing about it is wrong. What would be wrong
    is filing the empty job, so the verb says there was nothing to queue and
    exits OK, and the store is asked whether it believed it.
    """
    del configured
    code, envelope = _drive(argv)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP), envelope
    assert envelope["data"]["job_id"] == ""
    assert envelope["data"]["state"] == "no-native-tree"
    assert _queued_jobs() == ()


# ═══════════════════════════════════════════════════════════════════════════
# Claim 3: the inbox applies only when somebody said so
# ═══════════════════════════════════════════════════════════════════════════


def test_the_confirmed_inbox_applies_and_the_declined_one_does_not(acknowledged, native):
    """The defect in one test: the two answers used to produce the same result.

    The plan was returned on BOTH branches, so somebody who confirmed saw a plan
    and believed it had happened. Both halves are asserted against the DATABASE,
    and the envelopes are then compared so a caller reading the payload rather
    than the library can tell the two apart as well.
    """
    code, declined = _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])
    assert code == int(ExitCode.OK), declined
    assert declined["outcome"] == str(Outcome.NO_OP)
    assert declined["data"]["totals"]["applied"] is False
    assert _membership(acknowledged, native) == set(), (
        "the declined branch wrote membership, so the gate decided nothing"
    )

    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["outcome"] == str(Outcome.OK)
    assert applied["data"]["totals"]["applied"] is True
    assert applied["data"]["totals"]["added"] == 1
    assert _membership(acknowledged, native) == {"2"}, (
        "the confirmed branch reported a plan and wrote nothing, which is the "
        "hollow verb this unit closed"
    )

    assert declined["data"]["totals"] != applied["data"]["totals"], (
        "the two answers are indistinguishable in the payload, so a caller that "
        "reads the envelope cannot tell whether anything happened"
    )
    assert declined["data"]["digest"] == applied["data"]["digest"], (
        "the digest moved between two runs over one unchanged folder, so the "
        "decision a person records against it would be refused as stale"
    )


def test_a_confirmed_inbox_over_an_empty_folder_opens_nothing(acknowledged, native):
    """An empty folder is not a write, asserted where it can be seen.

    Nothing is derived, no database is opened and no session is taken, which is
    what lets this verb exit OK on a machine that has never acknowledged a
    backup. Asserted through the session log rather than through the return
    value, because a path that took a session and then decided it had nothing to
    do would satisfy every assertion about the envelope.
    """
    for path in _intake_dir(acknowledged).iterdir():
        path.unlink()
    before = len(session.records(acknowledged))

    code, envelope = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "inbox-empty"
    assert len(session.records(acknowledged)) == before
    assert _membership(acknowledged, native) == set()


def test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so(stocked):
    """Membership written for a tree still on the bridge is overwritten at the
    next import, so the apply reports that there is nowhere to put this yet
    rather than reporting an empty success."""
    code, envelope = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"
    assert envelope["data"]["totals"]["applied"] is False
    assert not Path(stocked.library.db_path).exists(), (
        "the apply opened a database on a library that has flipped no tree"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Claim 4: unplaced reports the library
# ═══════════════════════════════════════════════════════════════════════════


def test_unplaced_reports_the_rows_no_governed_tree_holds(acknowledged, native):
    """Two rows, neither filed, and the report has to name both.

    This is the assertion the constant could never fail: ``_plan([], ...)``
    reported an empty answer whatever the library held, and an empty answer reads
    as "your library is fully filed".
    """
    del native
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["compared"] is True
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1", "2"}
    assert envelope["data"]["totals"]["count"] == 2
    assert envelope["data"]["totals"]["collection"] == 2
    paths = {item["path"] for item in envelope["data"]["items"]}
    assert str(Path(acknowledged.library.root) / "Music" / SHELVED) in paths


def test_unplaced_over_a_fully_placed_library_reports_none(acknowledged, native):
    """The other direction, and it is what stops the fix being a constant of its own.

    A report that could only ever say "everything is unplaced" is the same defect
    with the sign flipped, so the library is FILLED first, by the shipped verbs,
    and then the same report has to come back empty.
    """
    del acknowledged
    _drive(["rebuild", "--actor", "a-person", "--job",
            _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]])
    _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert _membership(config.load(), native) == {"1", "2"}

    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["compared"] is True
    assert envelope["data"]["items"] == []
    assert envelope["data"]["totals"]["collection"] == 2


def test_unplaced_says_when_it_could_not_compare(configured):
    """An empty answer over a library nothing read is the constant defect arriving
    by another route, so the two are kept apart in the payload."""
    del configured
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["items"] == []
    assert envelope["data"]["totals"]["compared"] is False
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"


def test_unplaced_does_not_report_a_row_rekordbox_removed(acknowledged, native):
    """A tombstone is not a track waiting to be filed.

    Reporting one sends somebody to place something they deleted on purpose,
    which is the ``WITHDRAWN`` against ``NOT_IMPORTED`` distinction the routing
    pass already draws, said here about the report rather than about the pass.
    """
    del native
    conn = sqlite3.connect(acknowledged.library.db_path)
    try:
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '2'")
        conn.commit()
    finally:
        conn.close()

    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1"}
    assert envelope["data"]["totals"]["collection"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# The engine's failure paths, now that this unit owns them
# ═══════════════════════════════════════════════════════════════════════════


def test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates(
    configured, native, monkeypatch
):
    """KTD24, reached from the queue rather than from a direct engine call.

    ``acknowledged`` is deliberately not requested, so no recovery point exists.
    The refusal has to arrive on the ITEM: a worker that swallowed it would
    report the job done over a library it never wrote, which is the failure this
    whole unit is about.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: configured.library.volume_id),
    )
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]

    code, envelope = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None
    assert str(item.cause.remediation.remedy) == "acknowledge-backup", item.cause.to_json()
    assert _membership(configured, native) == set()


def test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item(
    acknowledged, native
):
    """The engine refuses rather than deriving nothing, and the worker carries it.

    An empty read is not evidence that a tree is right, and this is the path that
    would otherwise clear a tree's unconverged flag having read nothing at all.
    """
    for path in (Path(acknowledged.library.root) / "Music").iterdir():
        path.unlink()
    (Path(acknowledged.library.root) / "Music").rmdir()
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]

    code, envelope = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "rebuild-derivation-empty"
    assert _membership(acknowledged, native) == set()


def test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item(
    acknowledged, native
):
    """A registry pointing at a root this library does not have.

    That is the restored pre-cutover database, and ``anchored_root`` is what
    refuses it. It is reached here through the worker because the worker is what
    supplies ``root_exists``, and a worker that answered True for every
    identifier would walk down from a row that is not there.
    """
    del native
    entries = tree_registry.read(acknowledged)
    record = entries.record(TREE_ID)
    tree_registry.write(
        acknowledged,
        tree_registry.Registry((tree_registry.replace_root(record, "root-row-0000"),))
        if hasattr(tree_registry, "replace_root")
        else tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE_ID,
                    mode=record.mode,
                    cutover_on=record.cutover_on,
                    root_id="root-row-0000",
                    source=record.source,
                ),
            )
        ),
    )
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]

    code, envelope = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None, item


# ═══════════════════════════════════════════════════════════════════════════
# The review's round, driven so each finding has a guard that would bite again
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def planted_grid(configured) -> Path:
    """One analysis file where rekordbox actually keeps them.

    NOT beside the audio. The watch walks for ANLZ files by NAME, and a caller
    that names the music directory fingerprints an empty set, which reports a
    clean session whatever happened to the grids. That is a barren watch rather
    than an absent one, so the empty-list refusal one layer down cannot see it.
    """
    grid = Path(configured.library.root) / "PIONEER" / "USBANLZ" / "P001" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True)
    grid.write_bytes(b"PMAI")
    return grid


def _watched_roots(monkeypatch) -> list[list[str]]:
    """Capture the roots each write arms its analysis watch over, without disarming it.

    A WRAPPER RATHER THAN A STUB. The real gates still run, so this measures the
    shipped path instead of replacing it, and the assertion that follows is taken
    over the TREE: which files the captured roots actually cover.
    """
    from cratekit.core import session as session_module

    seen: list[list[str]] = []
    real = session_module.assert_gates

    def wrapper(cfg, *, analysis_roots=(), **rest):
        seen.append([str(root) for root in analysis_roots])
        return real(cfg, analysis_roots=analysis_roots, **rest)

    monkeypatch.setattr(session_module, "assert_gates", wrapper)
    return seen


def test_a_driven_rebuild_watches_the_grids_where_they_actually_live(
    acknowledged, native, planted_grid, monkeypatch
):
    """R17's fifth surface, runtime half, measured over the tree rather than asserted.

    The claim is not that some path was passed. It is that the files the watch
    covers include this library's real analysis files, which is the only version
    of the claim a narrower root fails.
    """
    del native
    seen = _watched_roots(monkeypatch)
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    code, envelope = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code == int(ExitCode.OK), envelope

    assert seen, "the write opened no session at all, so there is nothing to measure"
    for roots in seen:
        assert planted_grid in session.analysis_files_under(roots), (
            f"the session armed its analysis watch over {roots}, which holds no "
            f"analysis file at all, so it would report a clean session whatever "
            f"happened to this library's grids"
        )
    del acknowledged


def test_a_confirmed_inbox_watches_the_grids_where_they_actually_live(
    acknowledged, native, planted_grid, monkeypatch
):
    """The same claim for the apply, which is a separate call site."""
    del acknowledged, native
    seen = _watched_roots(monkeypatch)
    code, envelope = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), envelope

    assert seen, "the apply opened no session at all, so there is nothing to measure"
    for roots in seen:
        assert planted_grid in session.analysis_files_under(roots), roots


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_neither_resume_drives_another_verbs_job(acknowledged, native, argv):
    """``handlers.run_job`` reads the worker off the JOB ROW, not off this verb.

    So without a check here, naming somebody else's job identifier drives that
    verb's work in process, under this verb's envelope and without that verb's
    own resume time checks.
    """
    del acknowledged, native
    with jobs.open_store() as store:
        foreign = jobs.enqueue(
            store,
            handler_key="master",
            payload={},
            cfg=config.load(),
            item_ids=("one",),
        )

    code, envelope = _drive([*argv, "--job", foreign.job_id])
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert [item.state for item in _items(foreign.job_id)] == [jobs.ItemState.PENDING]


@pytest.mark.parametrize(
    "argv, key",
    [(["rebuild", "--actor", "a-person"], "rebuild"), (["route", "resort"], "route.resort")],
    ids=["rebuild", "resort"],
)
def test_neither_resume_drives_a_job_an_older_build_queued_with_no_items(
    acknowledged, native, argv, key
):
    """The zero item rule on the resume side, which is the door that predates the fix.

    Every rebuild and every resort queued before U53 carries no items, and
    ``jobs.drive`` walks an itemless job in one empty pass and records it
    SUCCEEDED. So the verb that refuses to FILE one has to refuse to DRIVE one
    as well, or the defect simply arrives from the queue instead.
    """
    del acknowledged, native
    with jobs.open_store() as store:
        stale = jobs.enqueue(store, handler_key=key, payload={}, cfg=config.load())

    code, envelope = _drive([*argv, "--job", stale.job_id])
    assert code != int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        assert jobs.get(store, stale.job_id).state != jobs.JobState.SUCCEEDED


@pytest.mark.parametrize(
    "argv, key",
    [(["rebuild", "--actor", "a-person"], "rebuild"), (["route", "resort"], "route.resort")],
    ids=["rebuild", "resort"],
)
def test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit(
    acknowledged, native, argv, key, monkeypatch
):
    """R-225, which named this inheritance in advance.

    ``jobs.drive`` raises only when EVERY attempted item failed, so a job over
    two trees where one failed returns normally with the job recorded failed. An
    unconditional OK on the resume exits 0 over half a library, and the person
    reading the exit status is the one who then believes the sweep finished.
    """
    del acknowledged
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=key,
            payload={"tree": None, "actor": "a-person"},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )

    real = rebuild.rebuild_governed_tree

    def one_of_two(cfg, *, tree_id, workflow, **rest):
        if tree_id != TREE_ID:
            raise RuntimeError("this tree is not there")
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", one_of_two)

    code, envelope = _drive([*argv, "--job", job.job_id])
    assert code != int(ExitCode.OK), envelope
    states = {item.item_id: item.state for item in _items(job.job_id)}
    assert states[TREE_ID] == jobs.ItemState.DONE
    assert states["second_tree"] == jobs.ItemState.FAILED
    assert _membership(config.load(), native) == {"1"}, (
        "the item that did succeed was rolled back, which is not what a partial "
        "failure means: the successes are durable and the exit says so"
    )


def test_a_resume_reads_no_registry_of_its_own(acknowledged, native):
    """Everything a queued job needs was frozen when it was queued.

    Reading the registry on the resume path would let an unreadable one
    permanently block work whose items are already decided, and the difference is
    visible in the ITEM: the driver either ran and recorded a cause, or it never
    ran at all.
    """
    del native
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    tree_registry.path_for(acknowledged).write_text("{ this is not a registry")

    code, envelope = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code != int(ExitCode.OK), envelope
    assert _items(job_id)[0].state == jobs.ItemState.FAILED, (
        "the verb refused before it drove anything, so the item is still pending "
        "and the unreadable registry blocked a job whose items were already frozen"
    )
