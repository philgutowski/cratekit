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
from tests.test_rb_writer_db import (
    RECORDED_APP_VERSION,
    _build_disposable_database,
    _encrypt_in_place,
)

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
    # The capture check is NOT patched here. It asks the file whether it needs
    # the key, and the encrypted drives below depend on it asking (R-239).
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
    handle = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
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

    IN THE SHARE BESIDE THE DATABASE, which is the analysis store (R-14). The
    ``PIONEER/USBANLZ/P0xx`` tree at the volume root is the USB export cache, and
    no row's analysis resolves into it.
    """
    share = Path(configured.library.db_path).parent / "share"
    grid = share / "PIONEER" / "USBANLZ" / "8d2" / "one" / "ANLZ0000.DAT"
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


# ═══════════════════════════════════════════════════════════════════════════
# The zero rows the first table found, turned into deaths
# ═══════════════════════════════════════════════════════════════════════════

#: A second tree, still on the XML bridge. Membership written into the database
#: for one of these is membership the next import overwrites, so no queued item
#: may name it. Every fixture above holds ONE tree and it is native, which is why
#: the first mutation table could not kill the filter that excludes this one.
BRIDGE_TREE = "loose_shelf"


@pytest.fixture
def mixed(native, acknowledged) -> str:
    """One tree that has cut over and one that has not, in one registry."""
    entries = tree_registry.read(acknowledged)
    tree_registry.write(
        acknowledged,
        tree_registry.Registry(
            (
                *entries.trees,
                tree_registry.TreeRecord(tree_id=BRIDGE_TREE, mode=tree_registry.Mode.XML),
            )
        ),
    )
    return native


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge(mixed, argv):
    """A rebuild of a bridge tree writes membership the next import overwrites.

    The filter that excludes it survived the unit's first mutation table with
    zero deaths, and the reason was the fixtures rather than the guard: every one
    of them held a single tree and that tree had cut over, so a run that ignored
    the medium produced the same item list as one that respected it.
    """
    del mixed
    code, envelope = _drive(argv)
    assert code == int(ExitCode.OK), envelope
    filed = _queued_jobs()
    assert len(filed) == 1, filed
    assert [item.item_id for item in _items(filed[0].job_id)] == [TREE_ID], (
        "a tree still on the XML bridge was queued for a database write"
    )


def test_a_rebuild_of_one_named_tree_queues_that_tree_alone(acknowledged, native):
    """The ``--tree`` flag scopes the work, and nothing drove it until now.

    A rebuild that ignored the name would sweep every governed tree in the
    library while reporting the one the person asked for, which on a library with
    several trees is a great deal of writing nobody requested.
    """
    del native
    entries = tree_registry.read(acknowledged)
    second = tree_registry.TreeRecord(
        tree_id="second_shelf",
        mode=tree_registry.Mode.DATABASE,
        cutover_on=date(2026, 8, 1),
        root_id=entries.record(TREE_ID).root_id,
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    tree_registry.write(acknowledged, tree_registry.Registry((*entries.trees, second)))

    code, envelope = _drive(["rebuild", "--actor", "a-person", "--tree", TREE_ID])
    assert code == int(ExitCode.OK), envelope
    assert [item.item_id for item in _items(envelope["data"]["job_id"])] == [TREE_ID]

    code, both = _drive(["rebuild", "--actor", "a-person"])
    assert code == int(ExitCode.OK), both
    assert [item.item_id for item in _items(both["data"]["job_id"])] == [
        "second_shelf",
        TREE_ID,
    ], "the unscoped rebuild is what proves the scoped one was scoped"


def test_a_gate_answer_this_verb_does_not_recognise_writes_nothing(
    acknowledged, native, monkeypatch
):
    """The branch direction, which no drive through the shipped gate can reach.

    The gate declares two options, so the command line can produce ``apply`` and
    ``abort`` and nothing else, and a branch written as "is abort" is therefore
    indistinguishable from one written as "not apply" for as long as that stays
    true. It will not stay true: an option added to this gate later would acquire
    the writing behaviour purely by nobody having classified it, which is the
    fail-open direction. Driven at the seam because the seam is where the third
    answer can exist at all.
    """
    del acknowledged
    from cratekit.write import routing_cli

    monkeypatch.setattr(routing_cli, "_apply_gate", lambda ctx, plan: "later")
    code, envelope = _drive(["route", "inbox"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP), envelope
    assert envelope["data"]["totals"]["applied"] is False
    assert _membership(config.load(), native) == set(), (
        "an answer this verb does not recognise wrote membership, so the gate "
        "admits by omission rather than by decision"
    )


# ═══════════════════════════════════════════════════════════════════════════
# R-239: every verb here opens an ENCRYPTED library, which is what a real one is
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def encrypted(acknowledged, native) -> str:
    """The native library above, encrypted with the key the binding supplies.

    Every other database in this file is plain, and these verbs used to pass
    ``unlock=False`` to the opener, which a plain file accepts and a real library
    refuses. Encrypted AFTER the rows are recorded, because recording them goes
    straight through ``sqlite3``, which cannot read an encrypted file.
    """
    path = Path(acknowledged.library.db_path)
    _encrypt_in_place(path)
    assert rb_writer.unlock_needed(path)
    return native


def test_a_confirmed_inbox_applies_on_an_encrypted_library(acknowledged, encrypted):
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["applied"] is True
    assert _membership(acknowledged, encrypted) == {"2"}


@pytest.mark.parametrize(
    "argv",
    [["rebuild", "--actor", "a-person"], ["route", "resort"]],
    ids=["rebuild", "resort"],
)
def test_a_queued_rebuild_and_resort_run_on_an_encrypted_library(
    acknowledged, encrypted, argv
):
    code, queued = _drive(argv)
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]

    code, done = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, encrypted) == {"1"}


def test_unplaced_compares_on_an_encrypted_library(acknowledged, encrypted):
    del acknowledged, encrypted
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["compared"] is True
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1", "2"}


def test_converge_compares_a_native_tree_on_an_encrypted_library(acknowledged, encrypted):
    """``converge`` answered "not compared" on every real library, which a person
    reads as "nothing to see" rather than as "could not look"."""
    del acknowledged, encrypted
    from cratekit.cli import converge

    code, envelope = _drive(["converge"])
    assert code == int(ExitCode.OK), envelope
    statuses = {
        check["key"]: check["status"] for check in envelope["data"]["checks"]
    }
    assert statuses[f"tree.{TREE_ID}"] != converge.NOT_COMPARED, envelope


# ═══════════════════════════════════════════════════════════════════════════
# U86: the export medium, for a library whose tree has not cut over
# ═══════════════════════════════════════════════════════════════════════════
#
# The source system sorted the INBOX playlist of a fresh export and wrote a new
# file to import. That needs no database write, so it works on a library that
# has cut nothing over, which is every library until U29. Every test below goes
# through the shipped command line and then reads the OUTPUT FILE back, because
# the envelope is what a hollow write would still produce.

#: Three intake tracks, their tag readings, and where the declared rules put
#: each one. The destination is spelled out here rather than derived, so the
#: expectation cannot be the code under test asked twice.
EXPORT_TRACKS = {
    "11": ("Low Track.flac", "Deep House", 2, ("Deep House", "Low")),
    "12": ("Mid Track.flac", "Deep House", 5, ("Deep House", "Med")),
    "13": ("Top Track.flac", "Tech House", 8, ("Tech House", "High")),
}

#: U87's tracks: one per rating rule. Energy 10 is the top of the star curve
#: and energy 1 the bottom; track 23 was rated by a person; track 24 files into
#: a bucket declared ``rates = false``; track 25 has no energy reading.
RATING_TRACKS = {
    "21": ("Floor Filler.flac", "Tech House", 10, ("Tech House", "High")),
    "22": ("Warm Up.flac", "Deep House", 1, ("Deep House", "Low")),
    "23": ("Hand Rated.flac", "Tech House", 10, ("Tech House", "High")),
    "24": ("Jazz Track.flac", "Jazz", 10, ("NonElectronic", "Jazz")),
    "25": ("No Reading.flac", "Deep House", None, ("Deep House", "Unsorted")),
}

#: The folders RATING_TRACKS land in, so every one of them is filed and a
#: rating left unset is the rating rule's doing and not a skipped write's.
RATING_FOLDERS = (
    ("Deep House", ("Low", "Med", "High", "Unsorted")),
    ("Tech House", ("Low", "Med", "High")),
    ("NonElectronic", ("Jazz",)),
)

#: The export scale's five and one star values, spelled out rather than asked
#: of the taxonomy, and checked against the shipped template's raw TOML by
#: ``test_the_star_values_the_rating_tests_expect_are_the_shipped_curve``.
FIVE_STARS = "255"
ONE_STAR = "51"

#: Tokens that only ever appear in grid bearing XML, the set the beat grid
#: suite forbids an emitter to produce, plus the tempo attribute itself.
GRID_TOKENS = ("<TEMPO", "Battito", "Metro=", "Inizio=", "AverageBpm=", "Bpm=")


def _export_track(
    tid: str,
    location: str,
    *,
    analyzed: bool = False,
    rating: str | None = None,
    seconds: str | None = None,
) -> list[str]:
    """One multi line collection row, the real export shape, optionally analysed.

    ``rating`` None leaves the ``Rating`` attribute out, which U86's tests were
    written against and which the rating pass does not plan for (U87). A real
    export always carries one, so every U87 test passes it. ``seconds`` None
    leaves ``TotalTime`` out the same way (U88).
    """
    bpm = "124.00" if analyzed else "0.00"
    rated = "" if rating is None else f' Rating="{rating}"'
    length = "" if seconds is None else f' TotalTime="{seconds}"'
    lines = [
        f'    <TRACK TrackID="{tid}" Name="Track {tid}" Artist="A" Genre="Ignored"{length}',
        f'           AverageBpm="{bpm}"{rated} Location="{location}">',
    ]
    if analyzed:
        lines.append('      <TEMPO Inizio="0.512" Bpm="124.00" Metro="4/4" Battito="1"/>')
    lines.append("    </TRACK>")
    return lines


def _routing_folder(name: str, subs: tuple[str, ...]) -> list[str]:
    lines = [f'        <NODE Type="0" Name="{name}" Count="{len(subs)}">']
    lines += [
        f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="0"/>' for sub in subs
    ]
    lines.append("        </NODE>")
    return lines


def _write_export(
    cfg: config.Config,
    folder: Path,
    *,
    subs: tuple[str, ...] = ("Low", "Med", "High"),
    inbox: tuple[str, ...] | None = None,
    extra_rows: tuple[str, ...] = (),
    missing_file: str | None = None,
    tracks: dict[str, tuple] = EXPORT_TRACKS,
    ratings: dict[str, str] | None = None,
    folders: tuple[tuple[str, tuple[str, ...]], ...] | None = None,
    analyzed: tuple[str, ...] = ("11",),
    lengths: dict[str, str] | None = None,
    root_extra: tuple[str, ...] = (),
) -> Path:
    """A fresh export: a collection, an INBOX batch, and the routing tree.

    Every intake file is a real file under the library, because the reader is
    handed the path the export records and a Location naming nothing is refused
    as unreadable rather than routed to a fallback.

    ``ratings`` maps a track id to the ``Rating`` its row carries; a track it
    does not name carries none. ``lengths`` does the same for ``TotalTime``,
    over extra rows as well. ``folders`` replaces the two genre folders.
    ``root_extra`` is more children of the playlist root, after the two trees.
    """
    from cratekit.core import locations
    from tests.xml_fixtures import _xml_doc

    inbox = tuple(tracks) if inbox is None else inbox
    ratings = ratings or {}
    lengths = lengths or {}
    if folders is None:
        folders = (("Deep House", subs), ("Tech House", subs))
    music = Path(cfg.library.root) / "Music"
    rows: list[str] = []
    for tid, (name, *_rest) in tracks.items():
        path = music / name
        if tid != missing_file:
            path.write_bytes(b"")
        rows += _export_track(
            tid,
            locations.location_url(path),
            analyzed=tid in analyzed,
            rating=ratings.get(tid),
            seconds=lengths.get(tid),
        )
    for tid in extra_rows:
        rows += _export_track(
            tid, locations.location_url(music / f"{tid}.flac"), seconds=lengths.get(tid)
        )
    count = len(tracks) + len(extra_rows)
    declared = taxonomy.default_taxonomy()
    batch = [
        '          <NODE Name="2026-09-18 batch" Type="1" KeyType="0" '
        f'Entries="{len(inbox)}">',
        *(f'            <TRACK Key="{key}"/>' for key in inbox),
        "          </NODE>",
    ]
    document = _xml_doc(
        collection=[f'  <COLLECTION Entries="{count}">', *rows, "  </COLLECTION>"],
        root_children=[
            f'      <NODE Type="0" Name="{declared.intake.display}" Count="1">',
            *batch,
            "      </NODE>",
            f'      <NODE Type="0" Name="{declared.tree.display}" Count="{len(folders)}">',
            *(line for name, held in folders for line in _routing_folder(name, held)),
            "      </NODE>",
            *root_extra,
        ],
    )
    folder.mkdir(parents=True, exist_ok=True)
    export = folder / "library_FRESH.xml"
    export.write_bytes(document)
    return export


@pytest.fixture
def tagged(monkeypatch):
    """The three tag readings, served from the file NAME.

    Patched at the tag reader rather than at ``read_truth``, so the reader the
    native path uses is the one that runs. An empty file has no tags, and a
    tag writer here would be a second thing under test.
    """
    from cratekit.core import tags

    by_name = {
        name: (genre, energy)
        for name, genre, energy, _ in (*EXPORT_TRACKS.values(), *RATING_TRACKS.values())
    }
    monkeypatch.setattr(
        tags, "read_genre_from_file", lambda path: by_name.get(Path(path).name, (None, None))[0]
    )
    monkeypatch.setattr(
        tags, "read_energy_from_file", lambda path: by_name.get(Path(path).name, (None, None))[1]
    )
    monkeypatch.setattr(tags, "read_vox_from_file", lambda path: None)


def _routed(export: Path) -> Path:
    return export.with_name(export.stem + "_routed.xml")


def _sub_keys(document: bytes, folder: str, sub: str) -> tuple[str, ...]:
    """What one sub playlist holds in a written file, read by a real XML parser.

    A parser rather than the byte locates, so a file the locates can read and
    rekordbox could not is a failure here rather than a pass.
    """
    import xml.etree.ElementTree as ET

    declared = taxonomy.default_taxonomy()
    root = ET.fromstring(document)
    tree = next(
        node for node in root.find("PLAYLISTS")[0] if node.get("Name") == declared.tree.display
    )
    bucket = next(node for node in tree if node.get("Name") == folder)
    playlist = next(node for node in bucket if node.get("Name") == sub)
    keys = tuple(track.get("Key") for track in playlist.findall("TRACK"))
    assert int(playlist.get("Entries")) == len(keys), "the entry count disagrees"
    return keys


def _apply_export(export: Path) -> tuple[int, dict]:
    return _drive(["-d", "route.inbox.apply=apply", "route", "inbox", "--export", str(export)])


def test_an_export_inbox_lands_each_track_in_its_declared_sub(configured, tagged, tmp_path):
    """Three tracks, three subs, and the file that comes out parses."""
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == str(Outcome.PENDING)
    totals = envelope["data"]["totals"]
    assert totals["applied"] is True
    assert totals["inserted"] == 3
    assert totals["created"] == []
    assert totals["output"] == str(_routed(export))

    written = _routed(export).read_bytes()
    for tid, (_name, _genre, _energy, (folder, sub)) in EXPORT_TRACKS.items():
        assert _sub_keys(written, folder, sub) == (tid,), (
            f"track {tid} did not land in {folder}/{sub} alone"
        )
    assert {
        item["track_id"]: item["destination"] for item in envelope["data"]["items"]
    } == {tid: f"{folder}/{sub}" for tid, (*_, (folder, sub)) in EXPORT_TRACKS.items()}

    pending = envelope["pending_human_action"]
    assert pending["kind"] == "rekordbox_import"
    assert pending["artifact"] == str(_routed(export))
    assert pending["verify_verb"] == "route.inbox", (
        "the import check is not the verb that proves it by inserting nothing"
    )


def test_an_export_sub_that_does_not_exist_is_a_warning_and_nothing_is_created(
    configured, tagged, tmp_path
):
    """The non creating writer: a curated tree gains no playlist it never had."""
    export = _write_export(configured, tmp_path / "exports", subs=("Low", "Med"))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert totals["created"] == []
    assert totals["inserted"] == 2
    messages = [warning["message"] for warning in envelope["warnings"]]
    assert any("Tech House/High" in message for message in messages), messages
    written = _routed(export).read_bytes()
    assert b'Name="High"' not in written, "a sub the tree never had was created"


def test_a_second_export_run_over_its_own_output_inserts_nothing(configured, tagged, tmp_path):
    """Idempotent, and a run that inserted nothing writes no file to import."""
    export = _write_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    before = sorted(path.name for path in first.parent.iterdir())

    code, envelope = _apply_export(first)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["inserted"] == 0
    assert envelope["data"]["totals"]["reason"] == "nothing-to-route"
    assert envelope["pending_human_action"] is None
    assert sorted(path.name for path in first.parent.iterdir()) == before, (
        "a run that routed nothing still wrote a file somebody would import"
    )


def test_the_input_export_is_byte_identical_afterwards(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    before = export.read_bytes()
    _apply_export(export)
    assert export.read_bytes() == before, "the export was written in place"
    assert _routed(export).read_bytes() != before


def test_an_export_route_never_writes_a_tempo_bpm_or_grid(configured, tagged, tmp_path):
    """R17 over the diff: no added or removed line carries grid data.

    Track 11 is analysed, so the input HAS a grid, and the rekordbox authored
    one must survive verbatim while nothing new of the kind appears.
    """
    import difflib

    export = _write_export(configured, tmp_path / "exports")
    before = export.read_bytes().decode("utf-8").splitlines()
    _apply_export(export)
    after = _routed(export).read_bytes().decode("utf-8").splitlines()
    changed = [
        line
        for line in difflib.unified_diff(before, after, lineterm="", n=0)
        if line[:1] in "+-" and not line.startswith(("+++", "---"))
    ]
    assert changed, "the diff is empty, so this proves nothing"
    offenders = [line for line in changed if any(token in line for token in GRID_TOKENS)]
    assert offenders == [], offenders
    assert sum("<TEMPO" in line for line in after) == sum("<TEMPO" in line for line in before) == 1


def test_an_export_track_whose_file_is_not_there_is_a_warning_and_not_routed(
    configured, tagged, tmp_path
):
    """An unreadable file has no tags, and no tags route to the fallback, which
    would file a track by the one fact nobody measured."""
    export = _write_export(configured, tmp_path / "exports", missing_file="12")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    codes = [warning["code"] for warning in envelope["warnings"]]
    assert "track-file-unreadable" in codes, envelope["warnings"]
    items = {item["track_id"]: item["destination"] for item in envelope["data"]["items"]}
    assert items["12"] == ""
    written = _routed(export).read_bytes()
    routed = {
        key
        for folder in ("Deep House", "Tech House")
        for sub in ("Low", "Med", "High")
        for key in _sub_keys(written, folder, sub)
    }
    assert routed == {"11", "13"}, "the unreadable track was routed anyway"


def test_an_export_intake_key_with_no_collection_row_is_a_warning(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports", inbox=("11", "99"))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["inserted"] == 1
    assert "track-row-absent" in [warning["code"] for warning in envelope["warnings"]]


def test_an_export_with_no_routing_tree_is_blocked_not_already_filed(
    configured, tagged, tmp_path
):
    """Every write skipped is not "nothing to route", which is the answer the
    pending action names as proof that an import landed."""
    export = _write_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().tree.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Other"'))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["inserted"] == 0
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    skipped = [w for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert skipped and all(display in w["message"] for w in skipped), envelope["warnings"]
    assert not _routed(export).exists()


def test_an_export_whose_every_file_is_unreadable_is_blocked_not_already_filed(
    configured, tagged, tmp_path
):
    """Every track left behind at the read is the same shape one step earlier."""
    export = _write_export(configured, tmp_path / "exports", inbox=("11",), missing_file="11")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 0
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    assert not _routed(export).exists()


def test_an_export_route_on_an_unmounted_library_refuses(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    import shutil

    shutil.rmtree(configured.library.root)
    code, envelope = _apply_export(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert not _routed(export).exists()


def test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map(
    configured, tagged, tmp_path
):
    """rekordbox keeps recording a volume name after the drive stopped using it,
    and the declared prefix map is what finds the file again. Without it all
    three tracks are unreadable and nothing is routed."""
    from cratekit.core import locations

    data = valid_data(
        Path(configured.library.root),
        profile={"name": "full"},
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    data["library"]["location_prefix_map"] = [
        {"from": "/retired-volume/lib", "to": "{library.root}"}
    ]
    config.save(config.from_dict(data))
    config.reset_cache()
    export = _write_export(configured, tmp_path / "exports")
    live = locations.location_url(Path(configured.library.root)).encode()
    old = locations.location_url("/retired-volume/lib").encode()
    export.write_bytes(export.read_bytes().replace(live, old))
    assert live not in export.read_bytes()

    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["inserted"] == 3
    assert envelope["warnings"] == []


def test_a_native_routing_tree_refuses_before_the_plan_is_offered(
    configured, tagged, tmp_path
):
    """Refused at the verb, not only at the emitter, so a person is never asked
    to approve a write the guard would stop. A declined answer still refuses."""
    export = _write_export(configured, tmp_path / "exports")
    _cut_over_routing_tree(configured)
    code, envelope = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "tree-unconverged"


def test_the_export_writer_itself_refuses_a_routing_tree_that_has_cut_over(
    configured, tagged, tmp_path
):
    """The emitter layer alone, reached past the verb's own check, so neither
    layer is a guard only the other one covers."""
    from cratekit.write import routing_cli

    export = _write_export(configured, tmp_path / "exports")
    _content, plan, ratings, *_rest = routing_cli.plan_export(configured, export)
    _cut_over_routing_tree(configured)
    with pytest.raises(tree_registry.TreeModeRefused):
        routing_cli.apply_export(configured, export, export.read_bytes(), plan, ratings)
    assert not _routed(export).exists()


def _cut_over_routing_tree(cfg: config.Config) -> None:
    tree_registry.write(
        cfg,
        tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=taxonomy.default_taxonomy().tree.id,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 8, 1),
                    root_id="1",
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        ),
    )


def test_a_declined_export_route_writes_nothing(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["applied"] is False
    assert not _routed(export).exists()


def test_an_export_without_an_intake_folder_refuses(configured, tagged, tmp_path):
    """An absent INBOX is not an empty one, and only one of them means done."""
    export = _write_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().intake.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Elsewhere"'))
    code, envelope = _apply_export(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "intake-flow-absent"
    assert not _routed(export).exists()


def test_an_absent_export_refuses(configured, tmp_path):
    code, envelope = _apply_export(tmp_path / "no-such.xml")
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "library-export-unusable"


def test_an_export_route_refuses_a_routing_tree_that_has_cut_over(
    configured, tagged, tmp_path
):
    """The medium follows the registry. A native tree is the database's, and
    an export carrying membership for it replaces that tree on import."""
    export = _write_export(configured, tmp_path / "exports")
    declared = taxonomy.default_taxonomy()
    tree_registry.write(
        configured,
        tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=declared.tree.id,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 8, 1),
                    root_id="1",
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        ),
    )
    code, envelope = _apply_export(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "tree-unconverged"
    assert not _routed(export).exists()


def test_without_export_a_library_with_no_native_tree_names_the_export_remedy(stocked):
    """Still no-native-tree, and now the answer names the medium that works."""
    code, envelope = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"
    remedies = [
        warning["message"]
        for warning in envelope["warnings"]
        if warning["code"] == "no-native-tree"
    ]
    assert remedies and "--export" in remedies[0], envelope["warnings"]


# ═══════════════════════════════════════════════════════════════════════════
# U87: the export filing pass fills an empty star rating from energy
# ═══════════════════════════════════════════════════════════════════════════
#
# Every source system sort set a rating from energy on a track whose rating was
# still zero, in the same pass as the filing. Every expected value below is a
# literal, never the taxonomy asked through the code that writes it, and every
# test reads the OUTPUT FILE with a real XML parser.


def _ratings_of(document: bytes) -> dict[str, str | None]:
    """Each collection track's ``Rating`` in a written file, by a real parser."""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(document)
    return {track.get("TrackID"): track.get("Rating") for track in root.find("COLLECTION")}


def _rating_export(cfg: config.Config, folder: Path, **overrides) -> Path:
    """An export of RATING_TRACKS, every one unrated but the hand rated one.

    Track 22 carries an EMPTY rating rather than a zero, the other shape of
    "nobody rated this", so both are driven.
    """
    ratings = {tid: "0" for tid in RATING_TRACKS} | {"22": "", "23": "102"}
    options = {"tracks": RATING_TRACKS, "ratings": ratings, "folders": RATING_FOLDERS}
    return _write_export(cfg, folder, **(options | overrides))


def test_the_star_values_the_rating_tests_expect_are_the_shipped_curve():
    """The literals above against the template's own TOML, read raw, so the
    expectation is the fixture and not the loader or the planner."""
    import tomllib

    import cratekit

    template = Path(cratekit.__file__).parent / "templates" / "taxonomy.default.toml"
    cuts = tomllib.loads(template.read_text(encoding="utf-8"))["energy"]["rating"]["cuts"]
    assert str(cuts[-1]["rating"]) == FIVE_STARS and cuts[-1]["max"] == 10
    assert cuts[-2]["max"] < 10, "energy 10 is not alone in the top cut's reach"
    assert str(cuts[0]["rating"]) == ONE_STAR and cuts[0]["max"] >= 1


def test_an_unrated_export_track_takes_its_star_rating_from_energy(
    configured, tagged, tmp_path
):
    """Top of the curve five stars, bottom one star, zero and empty both filled."""
    export = _rating_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    written = _ratings_of(_routed(export).read_bytes())
    assert written["21"] == FIVE_STARS, "a zero rated top energy track was not five stars"
    assert written["22"] == ONE_STAR, "an empty rated bottom energy track was not one star"
    assert envelope["data"]["totals"]["rated"] == 2
    assert "2 unrated track(s)" in envelope["pending_human_action"]["summary"]


def test_a_hand_rated_export_track_is_never_overwritten(configured, tagged, tmp_path):
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    assert _ratings_of(_routed(export).read_bytes())["23"] == "102", (
        "a rating a person set was replaced by the energy curve"
    )


def test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_left_unrated(
    configured, tagged, tmp_path
):
    """Filed, so the pass reached it, and still unrated, so the flag held."""
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    written = _routed(export).read_bytes()
    assert _sub_keys(written, "NonElectronic", "Jazz") == ("24",)
    assert _ratings_of(written)["24"] == "0", "a rates = false bucket was rated"


def test_a_track_with_no_energy_reading_is_filed_and_left_unrated(
    configured, tagged, tmp_path
):
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    written = _routed(export).read_bytes()
    assert _sub_keys(written, "Deep House", "Unsorted") == ("25",)
    assert _ratings_of(written)["25"] == "0", "a track with no energy was rated"


def test_a_second_export_run_over_its_own_rated_output_changes_nothing(
    configured, tagged, tmp_path
):
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    before = sorted(path.name for path in first.parent.iterdir())

    code, envelope = _apply_export(first)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["rated"]) == (0, 0)
    assert totals["reason"] == "nothing-to-route"
    assert all(item["rating"] == "" for item in envelope["data"]["items"])
    assert sorted(path.name for path in first.parent.iterdir()) == before


def test_a_filed_track_still_unrated_is_rated_in_a_file_of_its_own(
    configured, tagged, tmp_path
):
    """Nothing to insert is not nothing to write while a rating is owed, and a
    re-run that answered nothing-to-route here would pass the import check
    over a track the pass never rated."""
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    first.write_bytes(first.read_bytes().replace(f'Rating="{FIVE_STARS}"'.encode(), b'Rating="0"'))

    code, envelope = _apply_export(first)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["rated"]) == (0, 1)
    assert _ratings_of(_routed(first).read_bytes())["21"] == FIVE_STARS


def test_the_offered_plan_names_each_rating_before_anything_is_written(
    configured, tagged, tmp_path
):
    """The rating rides the items, so it is inside the digest a person approves."""
    export = _rating_export(configured, tmp_path / "exports")
    code, envelope = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), envelope
    offered = {item["track_id"]: item["rating"] for item in envelope["data"]["items"]}
    assert offered == {"21": FIVE_STARS, "22": ONE_STAR, "23": "", "24": "", "25": ""}
    assert not _routed(export).exists()


def test_a_row_with_no_rating_attribute_is_not_planned(configured, tagged, tmp_path):
    """The writer patches a value in place and cannot add one, so planning a
    rating there would declare a write the run never performs."""
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["rated"] == 0
    assert all(item["rating"] == "" for item in envelope["data"]["items"])


def test_a_run_whose_every_filing_was_skipped_still_rates_and_is_not_already_filed(
    configured, tagged, tmp_path
):
    """A rating is an attribute of a track, so a missing routing tree does not
    un-rate it, and the skipped writes still ride as warnings rather than the
    answer the import check reads as done."""
    export = _rating_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().tree.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Other"'))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["rated"]) == (0, 2)
    assert totals["reason"] != "nothing-to-route"
    assert "route-write-skipped" in [w["code"] for w in envelope["warnings"]]


def test_a_rating_pass_never_changes_a_tempo_or_bpm(configured, tagged, tmp_path):
    """R17 on the rated element itself: track 21 is analysed AND rated, so the
    patch lands in the one open tag whose track carries a tempo child."""
    import xml.etree.ElementTree as ET

    export = _rating_export(configured, tmp_path / "exports", analyzed=("21",))
    before = ET.fromstring(export.read_bytes()).find("COLLECTION")
    _apply_export(export)
    written = _routed(export).read_bytes()
    after = ET.fromstring(written).find("COLLECTION")
    assert _ratings_of(written)["21"] == FIVE_STARS, "the analysed track was not rated"

    def tempo(collection):
        return {
            track.get("TrackID"): (
                track.get("AverageBpm"),
                [sorted(t.attrib.items()) for t in track.findall("TEMPO")],
            )
            for track in collection
        }

    assert tempo(after) == tempo(before)
    assert tempo(before)["21"][1], "the analysed track has no tempo child, so this proves nothing"


def test_two_rows_naming_one_file_are_both_rated(configured, tagged, tmp_path):
    """rekordbox can hold one file under two ids, and the pass reads the file
    once; each row it files is a row the rating is owed on."""
    tracks = RATING_TRACKS | {"26": RATING_TRACKS["21"]}
    ratings = {tid: "0" for tid in tracks}
    export = _write_export(
        configured, tmp_path / "exports", tracks=tracks, ratings=ratings, folders=RATING_FOLDERS
    )
    _apply_export(export)
    written = _routed(export).read_bytes()
    assert set(_sub_keys(written, "Tech House", "High")) == {"21", "23", "26"}
    rated = _ratings_of(written)
    assert (rated["21"], rated["26"]) == (FIVE_STARS, FIVE_STARS)


# ═══════════════════════════════════════════════════════════════════════════
# U88: the export filing pass builds the long track playlist
# ═══════════════════════════════════════════════════════════════════════════
#
# The source system put every collection track over twenty minutes into one
# root playlist on every sort. The name and the bound are literals here, checked
# against the shipped template's raw TOML, so the expectation is not the loader
# asked twice. Every test reads the OUTPUT FILE with a real XML parser.

LONG_PLAYLIST = "Sets and Long Tracks"
TWENTY_FIVE_MINUTES = "1500"
NINETEEN_MINUTES = "1140"


def _root_child(document: bytes, name: str):
    """The direct child of the playlist root named ``name``, or None."""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(document).find("PLAYLISTS")[0]
    found = [node for node in root if node.get("Name") == name]
    assert len(found) <= 1, f"{len(found)} root children are named {name!r}"
    return found[0] if found else None


def _long_members(document: bytes) -> tuple[str, ...] | None:
    """What the root long track playlist holds, or None when there is none."""
    node = _root_child(document, LONG_PLAYLIST)
    if node is None:
        return None
    assert node.get("Type") == "1", "the long track node is not a playlist"
    keys = tuple(track.get("Key") for track in node.findall("TRACK"))
    assert int(node.get("Entries")) == len(keys), "the entry count disagrees"
    return keys


def _long_export(cfg: config.Config, folder: Path, **overrides) -> Path:
    """EXPORT_TRACKS at 25, 19 and 5 minutes, plus a one hour set outside the
    intake, which the playlist takes because it reads the whole collection."""
    lengths = {"11": TWENTY_FIVE_MINUTES, "12": NINETEEN_MINUTES, "13": "300", "31": "3600"}
    options = {"lengths": lengths, "extra_rows": ("31",)}
    return _write_export(cfg, folder, **(options | overrides))


def test_the_long_track_values_the_tests_expect_are_the_shipped_declaration():
    import tomllib

    import cratekit

    template = Path(cratekit.__file__).parent / "templates" / "taxonomy.default.toml"
    raw = tomllib.loads(template.read_text(encoding="utf-8"))["long_tracks"]
    assert raw["display"] == LONG_PLAYLIST
    assert raw["over_seconds"] == 1200
    declared = taxonomy.default_taxonomy().long_tracks
    assert (declared.display, declared.over_seconds) == (LONG_PLAYLIST, 1200)


def test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not(
    configured, tagged, tmp_path
):
    export = _long_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_tracks"]) == (3, 2)
    assert _long_members(_routed(export).read_bytes()) == ("11", "31")
    assert LONG_PLAYLIST in envelope["pending_human_action"]["summary"]


def test_a_track_of_exactly_the_bound_is_not_a_member(configured, tagged, tmp_path):
    """The source system's bound is strict: over twenty minutes, not twenty."""
    export = _long_export(
        configured, tmp_path / "exports", lengths={"11": "1200", "12": "1201"}, extra_rows=()
    )
    _apply_export(export)
    assert _long_members(_routed(export).read_bytes()) == ("12",)


def test_a_second_run_over_its_own_output_adds_nothing(configured, tagged, tmp_path):
    """Idempotent, and it is still the answer the import check reads as done."""
    export = _long_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    before = first.read_bytes()
    listing = sorted(path.name for path in first.parent.iterdir())

    code, envelope = _apply_export(first)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_tracks"]) == (0, 0)
    assert totals["reason"] == "nothing-to-route"
    assert envelope["warnings"] == []
    assert all(item["long_track"] == "" for item in envelope["data"]["items"]), (
        "the offered plan names a member the playlist already holds as an addition"
    )
    assert sorted(path.name for path in first.parent.iterdir()) == listing
    assert first.read_bytes() == before


def test_a_long_track_alone_is_a_change_and_writes_a_file(configured, tagged, tmp_path):
    """An empty intake and one set the playlist lacks is still a file to import,
    or a set imported before this pass existed is never separated."""
    export = _long_export(configured, tmp_path / "exports", inbox=())
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_tracks"]) == (0, 2)
    assert _long_members(_routed(export).read_bytes()) == ("11", "31")


def test_no_long_track_builds_no_empty_playlist(configured, tagged, tmp_path):
    export = _long_export(configured, tmp_path / "exports", lengths={"31": "300"})
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["long_tracks"] == 0
    assert _long_members(_routed(export).read_bytes()) is None


def test_a_track_is_never_removed_from_the_playlist(configured, tagged, tmp_path):
    """Add only. A member with no collection row and a member now under the
    bound are both kept, and the new member goes after them."""
    existing = (
        f'      <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="2">',
        '        <TRACK Key="77"/>',
        '        <TRACK Key="12"/>',
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=existing)
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["long_tracks"] == 2
    assert _long_members(_routed(export).read_bytes()) == ("77", "12", "11", "31")


def test_a_same_named_playlist_inside_a_folder_is_not_hijacked(configured, tagged, tmp_path):
    nested = (
        '      <NODE Type="0" Name="Archive" Count="1">',
        f'        <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="1">',
        '          <TRACK Key="99"/>',
        "        </NODE>",
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=nested)
    _apply_export(export)
    written = _routed(export).read_bytes()
    assert _long_members(written) == ("11", "31")
    archive = _root_child(written, "Archive")
    inner = [node for node in archive if node.get("Name") == LONG_PLAYLIST]
    assert len(inner) == 1
    assert [track.get("Key") for track in inner[0].findall("TRACK")] == ["99"]
    assert inner[0].get("Entries") == "1"


def test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced(
    configured, tagged, tmp_path
):
    """The writer replaces by name, so a folder standing there is refused, and a
    run left with nothing else to do is blocked, never already filed."""
    folder = (
        f'      <NODE Type="0" Name="{LONG_PLAYLIST}" Count="1">',
        '        <NODE Name="Kept" Type="1" KeyType="0" Entries="1">',
        '          <TRACK Key="99"/>',
        "        </NODE>",
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=folder)
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["long_tracks"] == 0
    skipped = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any(LONG_PLAYLIST in message for message in skipped), envelope["warnings"]
    assert all(item["long_track"] == "" for item in envelope["data"]["items"]), (
        "the offered plan names additions the writer will refuse"
    )
    written = _routed(export).read_bytes()
    node = _root_child(written, LONG_PLAYLIST)
    assert node.get("Type") == "0"
    assert [t.get("Key") for t in node.find("NODE").findall("TRACK")] == ["99"]

    code, again = _apply_export(_routed(export))
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["reason"] == "route-blocked"


def test_a_missing_duration_is_counted_not_guessed(configured, tagged, tmp_path):
    """Absent, empty, zero, a word and a fraction are all unreadable lengths."""
    lengths = {"12": "", "13": "0", "31": "abc", "32": "1500.5", "33": "3600"}
    export = _long_export(
        configured, tmp_path / "exports", lengths=lengths, extra_rows=("31", "32", "33")
    )
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    totals = envelope["data"]["totals"]
    assert totals["duration_unreadable"] == 5
    assert totals["long_tracks"] == 1
    assert _long_members(_routed(export).read_bytes()) == ("33",)


def test_the_offered_plan_names_each_long_track_before_anything_is_written(
    configured, tagged, tmp_path
):
    export = _long_export(configured, tmp_path / "exports")
    code, envelope = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), envelope
    offered = {item["track_id"]: item["long_track"] for item in envelope["data"]["items"]}
    assert offered == {"11": LONG_PLAYLIST, "12": "", "13": "", "31": LONG_PLAYLIST}
    assert not _routed(export).exists()


def test_a_template_declaring_no_long_track_playlist_builds_none(
    configured, tagged, tmp_path, monkeypatch
):
    import dataclasses

    shipped = taxonomy.default_taxonomy()
    monkeypatch.setattr(
        taxonomy, "default_taxonomy", lambda: dataclasses.replace(shipped, long_tracks=None)
    )
    export = _long_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"]["long_tracks"] == 0
    assert _long_members(_routed(export).read_bytes()) is None
    assert all(item["long_track"] == "" for item in envelope["data"]["items"])


def test_the_add_only_writer_counts_each_new_track_once():
    """Directly on the writer: a repeated id and an existing member add nothing."""
    from cratekit.write import trees
    from tests.xml_fixtures import _xml_doc

    content = bytearray(
        _xml_doc(
            collection=['  <COLLECTION Entries="0">', "  </COLLECTION>"],
            root_children=[
                f'      <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="1">',
                '        <TRACK Key="5"/>',
                "      </NODE>",
            ],
        )
    )
    assert trees.add_to_root_playlist(LONG_PLAYLIST, ["5", "6", "6", "7"], content) == (2, None)
    assert _long_members(bytes(content)) == ("5", "6", "7")
    before = bytes(content)
    assert trees.add_to_root_playlist(LONG_PLAYLIST, ["7", "5"], content) == (0, None)
    assert bytes(content) == before
