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
5. unplaced is a report and declares itself one, so nothing asks a person to
   close rekordbox before reading it (R-313)
   -> ``test_unplaced_declares_no_write_and_needs_only_what_a_read_needs``,
      ``test_doctor_does_not_ask_for_rekordbox_closed_for_the_unplaced_report``,
      ``test_unplaced_reports_with_rekordbox_open_and_writes_nothing`` and
      ``test_unplaced_still_refuses_on_a_drifted_binding_so_doctor_keeps_the_pins``.
   U91 gave the act back on the export medium, and the U91 section at the end
   of this file drives it, starting at
   ``test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created``

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
from types import SimpleNamespace

import pytest

from cratekit import cli
from cratekit.cli import doctor, output, registry
from cratekit.core import (
    active_taxonomy,
    config,
    jobs,
    preflight,
    profiles,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import rebuild, routing_cli, routing_pass, trees
from tests.test_active_taxonomy import shipped_without, write_active
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
    from cratekit.write import metadata_cli, routing_cli

    seen: list[tuple[str, str]] = []
    cuts: list[tuple[object, object]] = []
    frozen = object()
    measured = object()
    after = object()
    staged: list[tuple] = []

    def left_behind(report, declared):
        assert report is after
        del declared
        return (measured,)

    def produced(*handed):
        staged.append(handed)
        return "staged"

    def spy(cfg, *, tree_id, workflow, vocal_threshold, **rest):
        # NO DEFAULT ON ``workflow`` OR ``vocal_threshold``. A spy that supplied
        # one would answer the question for a worker that named nothing, which
        # is the half this test exists to tell apart.
        del cfg, rest
        seen.append((tree_id, workflow))
        cuts.append(vocal_threshold)
        # The one field of the engine's report a worker reads (R-312).
        return SimpleNamespace(after=after)

    def loader(cfg):
        # U89: the cut each worker hands the engine is the one loader's answer
        # over the configuration the worker was handed, and nothing else.
        assert cfg is frozen
        return 7.5

    def declared(cfg):
        # R-685: the taxonomy too, from the library that configuration names.
        assert cfg is frozen
        return taxonomy.default_taxonomy()

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", spy)
    monkeypatch.setattr(metadata_cli, "load_vocal_threshold", loader)
    monkeypatch.setattr(active_taxonomy, "load", declared)
    monkeypatch.setattr(rebuild, "left_behind", left_behind)
    monkeypatch.setattr(rebuild, "left_behind_record", lambda entry: {"kept": entry})
    monkeypatch.setattr(routing_cli.artifacts, "produced", produced)
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    assert rebuild_verb.handle(object(), item, frozen) is None
    # WHAT THE ENGINE MEASURED BECOMES THE RESORT ITEM'S REPORT (R-312), handed
    # to the one helper that stages it under the job and the ordinal. The
    # rebuild worker has no surface that reads one and still produces nothing.
    driven = SimpleNamespace(job_id="j")
    assert routing_cli.handle_resort(driven, item, frozen) == "staged"
    assert staged == [
        (routing_cli.RESORT_ARTIFACTS, frozen, driven, item,
         {"tree_id": TREE_ID, "left_behind": [{"kept": measured}]})
    ]

    assert cuts == [7.5, 7.5]
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
    assert envelope["data"]["totals"]["skipped_files"] == []
    assert not Path(stocked.library.db_path).exists(), (
        "the apply opened a database on a library that has flipped no tree"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Claim 3b: the apply names every file it skipped, and why (R-318)
# ═══════════════════════════════════════════════════════════════════════════

#: A file dropped into the intake folder and never imported, the case R-318
#: measured: a confirmed apply over it answered a count and no file.
UNIMPORTED = "Third Track.flac"


def _skipped_warnings(envelope: dict) -> list[str]:
    return [
        warning["message"]
        for warning in envelope["warnings"]
        if warning["code"] == routing_cli.SKIPPED_WARNING
    ]


def _set_row(cfg: config.Config, sql: str, *params: str) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why(acknowledged, native):
    """The measured cost in one test: twenty unimported files read as ``skipped: 20``.

    The totals carry the file and a reason from the deferred pass's own
    vocabulary, and the warning, which is what the human output prints, names the
    file and says what to do next. Asserted beside the database, so the report is
    checked against what the write actually did.
    """
    (_intake_dir(acknowledged) / UNIMPORTED).write_bytes(b"")

    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert _membership(acknowledged, native) == {"2"}
    totals = applied["data"]["totals"]
    assert totals["skipped"] == 1
    assert totals["skipped_files"] == [
        {
            "path": str(_intake_dir(acknowledged) / UNIMPORTED),
            "reason": str(routing_pass.Placement.NOT_IMPORTED),
            "trees": [TREE_ID],
            "content_ids": [],
        }
    ]
    (message,) = _skipped_warnings(applied)
    assert UNIMPORTED in message
    assert "import" in message.lower()
    assert ARRIVED not in message, "a file the apply DID file was named as skipped"


def test_the_human_output_names_the_skipped_file(acknowledged, native):
    """The surface R-318 is about: a person reading the default output.

    The human renderer prints no totals at all, so a reason carried only in the
    payload would reach a script and never a person.
    """
    (_intake_dir(acknowledged) / UNIMPORTED).write_bytes(b"")
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(
        ["--output", "human", "-d", "route.inbox.apply=apply", "route", "inbox"],
        stdout=out,
        stderr=err,
    )
    assert code == int(ExitCode.OK), err.getvalue()
    assert UNIMPORTED in out.getvalue(), out.getvalue()


def test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported(acknowledged, native):
    """``WITHDRAWN`` against ``NOT_IMPORTED`` is the pair the vocabulary exists for.

    The writer's own matcher sees both as absent, because it indexes live rows
    only. Telling a person to import a track they imported and then removed sends
    them round the same loop for ever.
    """
    _set_row(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", "2")

    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    (entry,) = applied["data"]["totals"]["skipped_files"]
    assert entry["reason"] == str(routing_pass.Placement.WITHDRAWN)
    assert entry["content_ids"] == ["2"]
    (message,) = _skipped_warnings(applied)
    assert ARRIVED in message
    assert "removed" in message


def test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows(acknowledged, native):
    """Both rows are named, because a person has to see both to pick the mistake."""
    _set_row(
        acknowledged,
        "UPDATE djmdContent SET FolderPath = ? WHERE ID = ?",
        str(_intake_dir(acknowledged) / ARRIVED),
        "1",
    )

    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    (entry,) = applied["data"]["totals"]["skipped_files"]
    assert entry["reason"] == str(routing_pass.Placement.AMBIGUOUS)
    assert sorted(entry["content_ids"]) == ["1", "2"]
    (message,) = _skipped_warnings(applied)
    assert ARRIVED in message


def test_a_clean_apply_names_no_skipped_file(acknowledged, native):
    """The negative half, so a warning emitted on every run cannot pass the above."""
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["skipped"] == 0
    assert applied["data"]["totals"]["skipped_files"] == []
    assert _skipped_warnings(applied) == []


def _match(outcome: str, *ids: str) -> trees.RowMatch:
    kind = trees.MatchOutcome(outcome)
    return trees.RowMatch(
        "x.flac",
        kind,
        content_id=ids[0] if kind is trees.MatchOutcome.MATCHED else None,
        content_ids=ids if kind is trees.MatchOutcome.AMBIGUOUS else (),
    )


@pytest.mark.parametrize(
    ("alive", "removed", "expected"),
    [
        (("matched", "1"), ("absent",), routing_pass.Placement.RESOLVED),
        (("ambiguous", "1", "2"), ("absent",), routing_pass.Placement.AMBIGUOUS),
        (("unresolved",), ("unresolved",), routing_pass.Placement.UNRESOLVED),
        (("absent",), ("matched", "3"), routing_pass.Placement.WITHDRAWN),
        (("absent",), ("ambiguous", "3", "4"), routing_pass.Placement.WITHDRAWN),
        (("absent",), ("absent",), routing_pass.Placement.NOT_IMPORTED),
    ],
    ids=["resolved", "ambiguous", "unresolved", "withdrawn", "withdrawn-twice", "not-imported"],
)
def test_the_placement_of_a_row_answer_is_one_rule(alive, removed, expected):
    """The one mapping both the deferred pass and the apply read."""
    assert routing_pass.row_placement(_match(*alive), _match(*removed)) is expected


def test_every_placement_a_skip_can_carry_has_its_own_next_act():
    """A reason with no sentence would reach a person as a bare token.

    Derived from the enum rather than listed, so a placement added later fails
    here until somebody writes what a person does about it. ``UNDECLARED`` is
    excluded because the apply never resolves a destination from a ledger.
    """
    owed = set(routing_pass.Placement) - routing_pass.WRITABLE - {
        routing_pass.Placement.UNDECLARED
    }
    assert set(routing_cli.SKIP_NEXT_ACT) == owed
    sentences = list(routing_cli.SKIP_NEXT_ACT.values())
    assert len(set(sentences)) == len(sentences), "two reasons share one next act"


def test_the_skip_warning_counts_every_file_and_caps_the_names():
    """A long list cannot read as a short one.

    Literal numbers throughout. Reading the cap back from the module made this
    test follow the constant wherever it went, so halving it stayed green.
    """
    many = [
        {"path": f"/in/{index:03d}.flac", "reason": "not-imported", "trees": [], "content_ids": []}
        for index in range(15)
    ]
    (warning,) = routing_cli.skipped_warnings(many)
    message = warning["message"]
    assert warning["code"] == routing_cli.SKIPPED_WARNING
    assert message.startswith("15 file(s)")
    assert "000.flac" in message
    assert "009.flac" in message
    assert "010.flac" not in message
    assert "and 5 more" in message


def test_a_file_skipped_twice_in_one_tree_names_that_tree_once():
    """An additive sub-class declares one file into two playlists of one tree,
    and the writer skips it once per playlist."""
    cfg = SimpleNamespace(
        library=SimpleNamespace(root="/library"), resolved_prefix_map=lambda: ()
    )
    absent = trees.RowMatch("/library/INBOX/a.flac", trees.MatchOutcome.ABSENT)
    (record,) = routing_cli._skipped_files(
        cfg, [], {absent.requested: (absent, ["one", "two", "one"])}
    )
    assert record["trees"] == ["one", "two"]
    assert record["reason"] == str(routing_pass.Placement.NOT_IMPORTED)


def test_the_skip_warnings_are_one_per_reason_in_a_stable_order():
    records = [
        {"path": "/in/b.flac", "reason": "withdrawn", "trees": [], "content_ids": ["9"]},
        {"path": "/in/a.flac", "reason": "not-imported", "trees": [], "content_ids": []},
        {"path": "/in/c.flac", "reason": "not-imported", "trees": [], "content_ids": []},
    ]
    first = routing_cli.skipped_warnings(records)
    assert len(first) == 2
    assert first == routing_cli.skipped_warnings(list(reversed(records)))


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
# Claim 5: unplaced is a report and says so (R-313)
# ═══════════════════════════════════════════════════════════════════════════


def test_unplaced_declares_no_write_and_needs_only_what_a_read_needs():
    """The declaration is what doctor and conformance read, so it is the surface.

    Until R-313 closed, the entry said ``writes={"db_tree"}`` and
    ``destructive=True`` and asked for rekordbox closed, for a verb that opens
    the database without write intent and takes no session. The volume stays,
    because the tree registry the report walks from is a state file on the
    library root. The pins stay, because the binding pin is checked on a read as
    well, which the drifted binding drive below proves.

    U91 added ``xml`` and nothing else: ``--export`` writes a new file beside an
    export, and no database surface is written on either path.

    The prefix map check joined for the residual finding "Setup wrote no
    location prefix rule for rekordbox's renamed drive, and the My Tags plan
    read clean over 9770 rows it could not resolve": the report resolves every
    recorded path through the map, and a report over a library most of whose
    rows it cannot resolve is the clean report over unread state that finding
    names. Still nothing about closing rekordbox.
    """
    entry = registry.entry("route.unplaced")
    assert entry.writes == frozenset({"xml"}), entry.writes
    assert entry.destructive is False
    assert entry.doctor_checks == (
        "library.mounted",
        "rekordbox.pins",
        "library.paths_resolved",
    ), entry.doctor_checks
    assert entry.gates == (), [spec.name for spec in entry.gates]


def test_doctor_does_not_ask_for_rekordbox_closed_for_the_unplaced_report(monkeypatch):
    """Doctor's per verb requirement, derived from this entry and nothing else.

    ``requires_check`` is taken over every entry a profile switches on, so over
    the real registry ``route.inbox`` would still require rekordbox closed and
    the assertion would say nothing about this verb. Narrowing the walk to the
    one entry is what makes the drive about ``route.unplaced``.
    """
    monkeypatch.setattr(registry, "entries", lambda: (registry.entry("route.unplaced"),))
    membership = profiles.resolve("full")
    assert doctor.requires_check("library.mounted", membership)
    assert doctor.requires_check("rekordbox.pins", membership)
    assert not doctor.requires_check("rekordbox.closed", membership)


def test_unplaced_reports_with_rekordbox_open_and_writes_nothing(
    configured, native, monkeypatch
):
    """The cost R-313 named, driven: a report that is safe with rekordbox open.

    No acknowledgment is recorded, so a destructive session could not open, and
    both rekordbox and its agent are reported running, which is the state a
    person is in when they want to look before they file. The report still has
    to name both rows, and the database file has to come back byte for byte.
    """
    del native
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    database = Path(configured.library.db_path)
    before = database.read_bytes()

    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["compared"] is True
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1", "2"}
    assert database.read_bytes() == before, "a report changed the database it read"
    assert not session.lock_path(configured).exists(), "a report took the session lock"


def test_unplaced_still_refuses_on_a_drifted_binding_so_doctor_keeps_the_pins(
    configured, native, monkeypatch
):
    """Why ``rekordbox.pins`` stays declared when ``rekordbox.closed`` goes.

    The binding pin is checked on EVERY open, read or write, so a read only
    report still refuses when the binding drifts. Dropping the check from the
    declaration would have doctor call the verb ready and the verb then refuse,
    which is the precondition the declaration exists to name in advance.
    """
    del native
    import pyrekordbox

    monkeypatch.setattr(pyrekordbox, "__version__", "0.0.0-drifted")
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.VERSION_PIN), envelope
    assert envelope["cause"]["reason"] == "pyrekordbox-pin-drift", envelope
    assert "rekordbox.pins" in registry.entry("route.unplaced").doctor_checks


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
# R-316: the dimension the engine said it did not compare reaches the envelope
# ═══════════════════════════════════════════════════════════════════════════
#
# The shipped taxonomy declares ``with_vox`` as an additive sub-playlist and no
# worker reads a vocal calibration, so the engine names ``vocal`` in its gaps.
# Before this, the inbox dropped that tuple and the rebuild worker dropped the
# whole report, and a person saw a clean job over a dimension nothing filed.


def _vocal_warnings(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.VOCAL_NOT_COMPARED]


@pytest.fixture
def no_vocal_dimension(monkeypatch):
    """The shipped taxonomy with its additive sub-playlists taken out.

    A declaration with nothing additive has no vocal dimension to leave
    uncompared, so a warning here would be the surface crying wolf, which
    teaches a person to skip the warning that is real.
    """
    import dataclasses

    shipped = taxonomy.default_taxonomy()
    assert any(entry.additive for entry in shipped.sub_classes), (
        "the shipped taxonomy no longer declares an additive sub-playlist, so the "
        "tests beside this fixture no longer exercise the gap they are about"
    )
    narrowed = dataclasses.replace(
        shipped,
        sub_classes=tuple(entry for entry in shipped.sub_classes if not entry.additive),
    )
    # THROUGH THE ONE LOADER, which is what every verb reads (R-685).
    monkeypatch.setattr(active_taxonomy, "load", lambda cfg: narrowed)


def test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared(
    acknowledged, native
):
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["applied"] is True
    assert _membership(acknowledged, native) == {"2"}
    warned = _vocal_warnings(applied)
    assert len(warned) == 1, applied["warnings"]
    assert set(warned[0]) == {"code", "message"}
    assert "vocal" in warned[0]["message"]
    assert "not_compared" not in applied["data"]["totals"], (
        "the gap leaked into the plan totals, which is the payload a person's "
        "decision is shown against, rather than riding as a warning"
    )


def test_a_declined_inbox_carries_no_vocal_warning(acknowledged, native):
    """Nothing was derived on the declined branch, so nothing went uncompared."""
    del acknowledged, native
    code, declined = _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])
    assert code == int(ExitCode.OK), declined
    assert _vocal_warnings(declined) == []


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift(
    acknowledged, native, argv
):
    """The rebuild's envelope carries the gap alongside the drift warning.

    Drift is induced for real, by moving a setting on disk after the job was
    queued, so the assertion is that the two warnings sit side by side rather
    than that one replaced the other.
    """
    code, queued = _drive(argv)
    assert code == int(ExitCode.OK), queued
    assert _vocal_warnings(queued) == [], (
        "the queue-only answer claimed a comparison nothing has run yet"
    )
    job_id = queued["data"]["job_id"]

    moved = config.from_dict(
        valid_data(
            Path(acknowledged.library.root),
            profile={"name": "full"},
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
            paths={"download_staging": str(Path(acknowledged.library.root).parent / "moved")},
        )
    )
    config.save(moved)
    config.reset_cache()

    code, done = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1"}
    codes = [w["code"] for w in done["warnings"]]
    assert "config-drift" in codes, done["warnings"]
    assert codes.count(rebuild.VOCAL_NOT_COMPARED) == 1, done["warnings"]


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_a_resume_that_drove_nothing_carries_no_vocal_warning(acknowledged, native, argv):
    """A job already finished on entry was compared by an earlier run, not this one."""
    del acknowledged, native
    job_id = _drive(argv)[1]["data"]["job_id"]
    code, first = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), first
    assert len(_vocal_warnings(first)) == 1, first["warnings"]
    code, again = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), again
    assert _vocal_warnings(again) == []


def test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface(
    acknowledged, native, no_vocal_dimension
):
    del no_vocal_dimension
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["applied"] is True
    assert _vocal_warnings(applied) == [], applied["warnings"]

    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    code, done = _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1", "2"}
    assert _vocal_warnings(done) == [], done["warnings"]


def test_the_rebuild_worker_still_returns_none(acknowledged, native):
    """``handle`` produces no artifact, and R-316 did not change that.

    Driven for real rather than through a spy, so the None is the worker's own
    answer after a rebuild that wrote, not a stand in's.
    """
    from cratekit.cli import rebuild as rebuild_verb

    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    assert rebuild_verb.handle(object(), item, acknowledged) is None
    assert _membership(acknowledged, native) == {"1"}


def test_the_gap_rule_is_the_derivations_own():
    """``governed_not_compared`` and the derivation answer from one rule.

    The warning on the rebuild's envelope is asked of the engine rather than read
    off the discarded report, so the two must agree by construction: the gaps the
    derivation returns over the shipped taxonomy with no threshold are exactly
    what the resume reports.
    """
    shipped = taxonomy.default_taxonomy()
    truth = [rebuild.Truth(location="/x/a.flac", genre=None, energy=None, voxlevel=None)]
    _placements, gaps = rebuild.derive_from_taxonomy(shipped, truth, vocal_threshold=None)
    assert gaps == (rebuild.VOCAL_DIMENSION,)
    assert rebuild.governed_not_compared(None, shipped) == gaps
    assert rebuild.derive_from_taxonomy(shipped, truth, vocal_threshold=0.5)[1] == ()
    assert rebuild.governed_not_compared(0.5, shipped) == ()


def test_the_warning_code_is_the_locked_spelling():
    """Every other assertion reads the constant, so this is the one that pins it.

    A code is a contract with whoever filters on it, and the brief locked this
    spelling. Renaming the constant's value would pass every test that compares
    against the constant.
    """
    assert rebuild.VOCAL_NOT_COMPARED == "vocal-dimension-not-compared"
    (warning,) = rebuild.not_compared_warnings((rebuild.VOCAL_DIMENSION,))
    assert warning["code"] == "vocal-dimension-not-compared"
    assert rebuild.not_compared_warnings(()) == ()


# ═══════════════════════════════════════════════════════════════════════════
# R-312: the resort is additive, and says what it left where it was
# ═══════════════════════════════════════════════════════════════════════════


def _left_behind(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.LEFT_BEHIND]


@pytest.fixture
def leftover(acknowledged, native) -> str:
    """A governed playlist holding a track the declaration does not place there.

    PRODUCED BY A SHIPPED VERB rather than planted: the confirmed inbox files
    the intake track, and the declaration a resort derives walks the music
    directory, which that file is not under. It is the state a genre change
    leaves behind seen from the side the engine reads it from, a membership in a
    declared destination that the declaration no longer asks for.
    """
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert _membership(acknowledged, native) == {"2"}
    return "2"


def test_a_resort_names_the_membership_it_left_where_it_was(acknowledged, native, leftover):
    """The cost R-312 records, then the answer to it.

    The resort adds the declared track and leaves the other one in place, and
    until this unit its envelope was a clean OK over a tree that held both. The
    warning names the playlist by its display and the track by its file, which
    are the two things a person needs to find the row in rekordbox and take it
    out, because nothing in this build removes it for them.
    """
    job_id = _drive(["route", "resort"])[1]["data"]["job_id"]
    code, done = _drive(["route", "resort", "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert _membership(acknowledged, native) == {"1", leftover}, (
        "the resort removed a membership, which this build has no governed path for"
    )
    (warning,) = _left_behind(done)
    assert "Electronica / Other/Unsorted" in warning["message"], warning
    assert ARRIVED in warning["message"], warning
    assert SHELVED not in warning["message"], (
        "the track the declaration places was named as a leftover"
    )
    assert "1 membership" in warning["message"], warning
    assert "adds and never removes" in warning["message"], warning


def test_a_resort_that_left_nothing_behind_says_nothing_about_it(acknowledged, native):
    """A converged tree carries no leftover warning, so the warning means something."""
    job_id = _drive(["route", "resort"])[1]["data"]["job_id"]
    code, done = _drive(["route", "resort", "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert _membership(acknowledged, native) == {"1"}
    assert _left_behind(done) == []


def test_a_resort_resume_that_drove_nothing_names_no_leftover(acknowledged, native, leftover):
    """A job finished on entry was measured by the run that drove it, not this one.

    The second resume holds no report, so naming a leftover there would be this
    run answering for a comparison it never made. The queue only answer is the
    same: nothing has been compared when a job is merely filed.
    """
    del acknowledged, native, leftover
    code, queued = _drive(["route", "resort"])
    assert _left_behind(queued) == []
    job_id = queued["data"]["job_id"]
    assert len(_left_behind(_drive(["route", "resort", "--job", job_id])[1])) == 1
    code, again = _drive(["route", "resort", "--job", job_id])
    assert code == int(ExitCode.OK), again
    assert _left_behind(again) == []


def test_one_jobs_leftovers_are_not_counted_under_another(acknowledged, native, leftover):
    """TWO jobs over one state each name the one leftover, never the pool of both.

    The reports are read back by job, and a read that ignored the job would
    count the first resort's report again under the second.
    """
    del acknowledged, native, leftover
    for _ in range(2):
        job_id = _drive(["route", "resort"])[1]["data"]["job_id"]
        (warning,) = _left_behind(_drive(["route", "resort", "--job", job_id])[1])
        assert "1 membership" in warning["message"], warning
        assert job_id in warning["message"], "the warning does not say where this job's list is"


def test_the_whole_list_is_written_where_the_warning_says_it_is(
    acknowledged, native, leftover
):
    """The names in a warning are capped, so the place it points at has to be real."""
    del acknowledged, native
    job_id = _drive(["route", "resort"])[1]["data"]["job_id"]
    (warning,) = _left_behind(_drive(["route", "resort", "--job", job_id])[1])
    listed_in = Path(warning["message"].rsplit("listed in ", 1)[1])
    (report,) = sorted(listed_in.glob("*.json"))
    written = json.loads(report.read_text(encoding="utf-8"))
    assert written["tree_id"] == TREE_ID
    assert [entry["content_id"] for entry in written["left_behind"]] == [leftover]
    assert written["left_behind"][0]["location"].endswith(ARRIVED)


def test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left(
    acknowledged, native, leftover, monkeypatch
):
    """THE OTHER EXIT, which is the one a resort over several trees usually takes.

    A job that closed carrying a cause leaves through that cause, and a refusal
    envelope has no warnings. The tree that finished was written to all the
    same, so the refusal carries the leftovers as one more thing left to do, on
    the cause the queue recorded rather than on a rebuilt one.
    """
    del acknowledged, native, leftover
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="route.resort",
            payload={},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )
    real = rebuild.rebuild_governed_tree

    def one_of_two(cfg, *, tree_id, workflow, **rest):
        if tree_id != TREE_ID:
            raise RuntimeError("this tree is not there")
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", one_of_two)
    code, refused = _drive(["route", "resort", "--job", job.job_id])
    assert code != int(ExitCode.OK), refused
    with jobs.open_store() as store:
        stored = jobs.get(store, job.job_id).cause
    steps = list(refused["cause"]["remediation"]["steps"])
    assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps)
    (added,) = steps[len(stored.remediation.steps) :]
    assert ARRIVED in added and "1 membership" in added, added
    assert tuple(refused["cause"]["origin"])[: len(stored.origin)] == stored.origin
    assert refused["cause"]["reason"] == stored.reason


def test_a_resort_that_failed_with_nothing_left_behind_adds_no_step(
    acknowledged, native, monkeypatch
):
    """Gated on what ran. A refusal over a converged tree names no leftover."""
    del acknowledged, native
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="route.resort",
            payload={},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )
    real = rebuild.rebuild_governed_tree

    def one_of_two(cfg, *, tree_id, workflow, **rest):
        if tree_id != TREE_ID:
            raise RuntimeError("this tree is not there")
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", one_of_two)
    code, refused = _drive(["route", "resort", "--job", job.job_id])
    assert code != int(ExitCode.OK), refused
    with jobs.open_store() as store:
        stored = jobs.get(store, job.job_id).cause
    assert list(refused["cause"]["remediation"]["steps"]) == list(stored.remediation.steps)


def _not_there_yet() -> Exception:
    """A tree rebuild that fails and will not fail the next time, recorded as such.

    ``jobs.retry`` re-arms only a job whose recorded failures are retryable
    (R-390). A ``RuntimeError`` reaches the item boundary as ``internal-error``,
    which is a defect and permanent, so a test that re-arms the job afterwards
    has to fail the item the way a transient failure fails it.
    """
    return refuse(
        "unavailable-transient",
        "this tree is not there yet",
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("test",),
    )


def test_a_second_process_names_what_the_first_ones_tree_left(
    acknowledged, native, leftover, monkeypatch
):
    """The driver that died is the run an in memory note loses.

    The first drive finishes this tree and fails the other, which is what a kill
    between two items leaves in the queue: one item done with its report
    committed, one not. A retry then drives only the second item, in what is a
    different process in life, and still names the first tree's leftover because
    it reads the reports back.
    """
    del acknowledged, native, leftover
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="route.resort",
            payload={},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )
    real = rebuild.rebuild_governed_tree
    calls: list[str] = []

    def second_tree_fails_once(cfg, *, tree_id, workflow, **rest):
        calls.append(tree_id)
        if tree_id != TREE_ID:
            if calls.count(tree_id) == 1:
                # A failure that clears on its own, and recorded as one: the
                # re-arm below reads the item's retryable flag (R-390), and a
                # bare RuntimeError is recorded as a permanent internal-error.
                raise _not_there_yet()
            return SimpleNamespace(after=rebuild.ConvergenceReport(tree_id, "root", derived=1))
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", second_tree_fails_once)
    assert _drive(["route", "resort", "--job", job.job_id])[0] != int(ExitCode.OK)
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    code, done = _drive(["route", "resort", "--job", job.job_id])
    assert code == int(ExitCode.OK), done
    assert calls == [TREE_ID, "second_tree", "second_tree"], calls
    (warning,) = _left_behind(done)
    assert ARRIVED in warning["message"], warning


def test_a_refusal_raised_before_the_drive_carries_no_leftover_step(
    acknowledged, native, leftover, monkeypatch
):
    """A run that drove nothing answers for no tree, whatever an earlier one wrote.

    The first resume finishes this tree, commits its report and fails the other.
    The retry then refuses on its calibration before any item is claimed. That
    refusal is about a file, and hanging the earlier run's leftovers on it would
    be this run reporting a comparison it never made. Found as a zero row in the
    unit's own mutation table and turned into a death.
    """
    from cratekit.write import metadata_cli

    del acknowledged, native, leftover
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="route.resort",
            payload={},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )
    real = rebuild.rebuild_governed_tree

    def one_of_two(cfg, *, tree_id, workflow, **rest):
        if tree_id != TREE_ID:
            raise _not_there_yet()
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", one_of_two)
    code, first = _drive(["route", "resort", "--job", job.job_id])
    assert ARRIVED in " ".join(first["cause"]["remediation"]["steps"]), first
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)

    def corrupt(cfg):
        del cfg
        raise refuse("config-unusable", "the calibration cannot be read")

    monkeypatch.setattr(metadata_cli, "load_vocal_threshold", corrupt)
    code, refused = _drive(["route", "resort", "--job", job.job_id])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "config-unusable", refused
    assert ARRIVED not in " ".join(refused["cause"]["remediation"]["steps"]), refused


def _difference(n: int, **fields) -> dict:
    return {
        "bucket": "b",
        "sub": "s",
        "folder": "Folder",
        "playlist": "Playlist",
        "content_id": str(n),
        "location": f"Music/track-{n:03}.flac",
        **fields,
    }


def test_the_leftover_warning_is_capped_and_still_counts_every_one():
    """A back catalogue can leave thousands, and the count must not be the cap."""
    # HANDED OVER BACKWARDS, so the names that survive the cap are the first in
    # order and not the first to arrive, which is what makes two runs agree.
    records = [_difference(n) for n in reversed(range(rebuild.LEFT_BEHIND_NAMED + 3))]
    (warning,) = rebuild.left_behind_warnings(records, listed_in="/queue/reports")
    assert f"{rebuild.LEFT_BEHIND_NAMED + 3} membership" in warning["message"]
    assert "track-000.flac" in warning["message"]
    assert f"track-{rebuild.LEFT_BEHIND_NAMED - 1:03}.flac" in warning["message"]
    assert f"track-{rebuild.LEFT_BEHIND_NAMED:03}.flac" not in warning["message"]
    assert "and 3 more" in warning["message"]
    assert warning["message"].endswith("listed in /queue/reports")


def test_a_leftover_with_no_readable_file_is_named_by_its_row():
    """The identifier is the fallback, never a blank."""
    (warning,) = rebuild.left_behind_warnings(
        [_difference(41, location=None)], listed_in="/queue/reports"
    )
    assert "Folder/Playlist: row 41." in warning["message"], warning
    assert " more" not in warning["message"], "one leftover was reported as a capped list"


def test_the_record_a_worker_writes_is_the_one_the_message_reads():
    """Two halves of one file format, pinned against each other rather than apart."""
    entry = rebuild.Difference(
        direction=rebuild.Direction.UNEXPECTED,
        bucket="b",
        sub="s",
        folder="Folder",
        playlist="Playlist",
        content_id="7",
        location="Music/seven.flac",
    )
    message = rebuild.left_behind_message(
        [rebuild.left_behind_record(entry)], listed_in="/queue/reports"
    )
    assert message is not None and "Folder/Playlist: Music/seven.flac" in message


def test_the_leftover_code_is_the_locked_spelling():
    assert rebuild.LEFT_BEHIND == "membership-left-behind"
    # The shipped skill says "the first twenty" in words, so the number is pinned.
    assert rebuild.LEFT_BEHIND_NAMED == 20
    assert rebuild.left_behind_warnings((), listed_in="/queue/reports") == ()


def test_the_resort_summary_says_the_verb_is_additive():
    """The registry line is what help prints, and it promised a re-place.

    Named by what it must say and what it must stop saying, so a reword that
    keeps the promise under new words still fails.
    """
    summary = registry.entry("route.resort").summary
    assert "add" in summary, summary
    assert "re-place" not in summary, summary
    assert "old" in summary, summary


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

    monkeypatch.setattr(routing_cli, "_apply_gate", lambda ctx, plan, shown: "later")
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
        f'    <TRACK TrackID="{tid}" Name="Track {tid}" Artist="Artist {tid}" Genre="Ignored"{length}',
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


#: The review warning an export sweep gives for nested membership no import
#: can land (R-694), spelled out rather than imported from the module under test.
ROUTING_NOT_LANDABLE = "routing-not-landable"


def _not_landable(envelope: dict) -> list[str]:
    """The messages of every review warning an envelope carries."""
    return [w["message"] for w in envelope["warnings"] if w["code"] == ROUTING_NOT_LANDABLE]


def _others(envelope: dict) -> list[dict]:
    """Every warning but the review warning, for a test reading the rest exactly."""
    return [w for w in envelope["warnings"] if w["code"] != ROUTING_NOT_LANDABLE]


def test_an_export_inbox_lands_each_track_in_its_declared_sub(configured, tagged, tmp_path):
    """Three tracks, three subs, and the file that comes out parses."""
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.OK)
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

    # R-694: every change in this file is nested membership, which the bridge
    # never lands (R-687), so it is a review and owes no import, and the
    # warning says why in the words the pending steps used to.
    assert envelope["pending_human_action"] is None
    assert _not_landable(envelope) == [
        f"3 membership(s) routed under the routing tree in {_routed(export).name} "
        "are a review that no import can land: a nested playlist imported from "
        "the file lands at the playlist root as a new playlist, and a folder "
        "imported from it keeps every playlist it held and adds a second copy of "
        "each; file the intake tracks into the subs this review names by hand in "
        "rekordbox; until they are filed, route inbox --export plans the same "
        "routing on every fresh export, and this build writes nested membership "
        "only to a tree that has cut over to the database",
    ]


def test_an_export_sub_that_does_not_exist_is_a_warning_and_nothing_is_created(
    configured, tagged, tmp_path
):
    """The non creating writer: a curated tree gains no playlist it never had."""
    export = _write_export(configured, tmp_path / "exports", subs=("Low", "Med"))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
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
    assert code == int(ExitCode.OK), envelope
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
    assert code == int(ExitCode.OK), envelope
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
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 3
    assert _others(envelope) == []


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
    _content, plan, *_rest = routing_cli.plan_export(configured, export)
    _cut_over_routing_tree(configured)
    with pytest.raises(tree_registry.TreeModeRefused):
        routing_cli.apply_export(configured, export, export.read_bytes(), plan)
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
# U87, reversed by R-688: the export sweep plans no star rating
# ═══════════════════════════════════════════════════════════════════════════
#
# Every source system sort set a rating from energy on a track whose rating was
# still zero, in the same pass as the filing, and U87 wrote it into the export.
# The tenth sitting imported four such ratings and read all four back as zero:
# every row of a collection export is one rekordbox already holds, and an import
# keeps the database's rating on such a row. So the sweep now writes none, and
# counts the ones it would have written into one warning. Every expected value
# below is a literal, never the taxonomy asked through the code that writes it,
# and every test reads the OUTPUT FILE with a real XML parser.

#: The warning code, spelled out rather than imported from the module under test.
RATING_NOT_LANDABLE = "rating-not-landable"


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


def _owed(envelope: dict) -> list[str]:
    """The messages of every owed rating warning an envelope carries."""
    return [w["message"] for w in envelope["warnings"] if w["code"] == RATING_NOT_LANDABLE]


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


def test_an_owed_star_rating_is_not_written_into_the_export(configured, tagged, tmp_path):
    """R-688. Every row keeps the export's own rating, the two owed ones are
    counted in a warning, and neither the totals nor the review warning claims
    a rating that the import would never land. No root playlist gained a track,
    so no import is owed at all (R-694)."""
    export = _rating_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    written = _ratings_of(_routed(export).read_bytes())
    assert written == {"21": "0", "22": "", "23": "102", "24": "0", "25": "0"}
    (message,) = _owed(envelope)
    assert message.startswith("2 intake row(s) are owed a star rating"), message
    assert "rated" not in envelope["data"]["totals"]
    assert envelope["pending_human_action"] is None
    (review,) = _not_landable(envelope)
    assert "rating" not in review, review


def _alone(cfg: config.Config, folder: Path, tid: str, rating: str) -> Path:
    """An export of one RATING_TRACKS row, so the owed count is that row's."""
    tracks = {tid: RATING_TRACKS[tid]}
    return _write_export(
        cfg, folder, tracks=tracks, ratings={tid: rating}, folders=RATING_FOLDERS
    )


def test_a_lone_unrated_track_with_energy_is_owed_one_rating(configured, tagged, tmp_path):
    """The positive the three rules below are measured against, on the same
    single row shape, so their empty answer is the rule's and not the shape's."""
    export = _alone(configured, tmp_path / "exports", "21", "0")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    (message,) = _owed(envelope)
    assert message.startswith("1 intake row(s) are owed a star rating"), message


def test_a_hand_rated_export_track_is_not_owed_a_rating(configured, tagged, tmp_path):
    export = _alone(configured, tmp_path / "exports", "23", "102")
    _code, envelope = _apply_export(export)
    assert _owed(envelope) == [], "a rating a person set was counted as owed"
    assert _ratings_of(_routed(export).read_bytes())["23"] == "102"


def test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed(
    configured, tagged, tmp_path
):
    """Filed, so the pass reached it, and not counted, so the flag held."""
    export = _alone(configured, tmp_path / "exports", "24", "0")
    _code, envelope = _apply_export(export)
    assert _sub_keys(_routed(export).read_bytes(), "NonElectronic", "Jazz") == ("24",)
    assert _owed(envelope) == [], "a rates = false bucket was counted as owed"


def test_a_track_with_no_energy_reading_is_filed_and_not_owed(configured, tagged, tmp_path):
    export = _alone(configured, tmp_path / "exports", "25", "0")
    _code, envelope = _apply_export(export)
    assert _sub_keys(_routed(export).read_bytes(), "Deep House", "Unsorted") == ("25",)
    assert _owed(envelope) == [], "a track with no energy was counted as owed"


def test_a_second_run_still_owing_ratings_is_nothing_to_route(configured, tagged, tmp_path):
    """Every track is filed and the two ratings are still owed. No run of this
    medium can land them, so they write no file and do not turn the answer the
    import check reads as done into route-blocked, and the warning still says
    they are owed."""
    export = _rating_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    before = sorted(path.name for path in first.parent.iterdir())

    code, envelope = _apply_export(first)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert totals["inserted"] == 0
    assert totals["reason"] == "nothing-to-route"
    assert [w["code"] for w in envelope["warnings"]] == [RATING_NOT_LANDABLE]
    assert sorted(path.name for path in first.parent.iterdir()) == before


def test_the_offered_plan_names_no_rating_and_says_which_are_owed(
    configured, tagged, tmp_path
):
    """The gate is where a person reads what the run will do, so the owed
    count is on it before the answer, and no item offers a rating."""
    export = _rating_export(configured, tmp_path / "exports")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    assert all("rating" not in item for item in shown["items"])
    assert "rated" not in shown
    (warning,) = shown["warnings"]
    assert warning.startswith("2 intake row(s) are owed a star rating"), warning
    assert not _routed(export).exists()


def test_a_declined_run_still_says_which_ratings_are_owed(configured, tagged, tmp_path):
    """The abort answer is how a person reads a plan without applying it, so
    its envelope carries the owed count the gate showed."""
    export = _rating_export(configured, tmp_path / "exports")
    code, envelope = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), envelope
    (message,) = _owed(envelope)
    assert message.startswith("2 intake row(s) are owed a star rating"), message
    assert not _routed(export).exists()


def test_a_row_with_no_rating_attribute_is_not_counted_as_owed(configured, tagged, tmp_path):
    """No ``Rating`` attribute is not "nobody rated this", so no warning."""
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert _owed(envelope) == []


def test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated(
    configured, tagged, tmp_path
):
    """With no routing tree nothing is filed, and an owed rating is no longer
    a change of its own, so no file is written and the skipped writes answer
    route-blocked rather than the answer the import check reads as done."""
    export = _rating_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().tree.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Other"'))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["applied"]) == (0, False)
    assert totals["reason"] == "route-blocked"
    codes = [w["code"] for w in envelope["warnings"]]
    assert "route-write-skipped" in codes and RATING_NOT_LANDABLE in codes
    assert not _routed(export).exists()


def test_an_analysed_track_keeps_its_rating_and_its_grid(configured, tagged, tmp_path):
    """R17 on the element U87 used to patch: track 21 is analysed and owed a
    rating, so the written file must carry its grid and its rating unchanged."""
    import xml.etree.ElementTree as ET

    export = _rating_export(configured, tmp_path / "exports", analyzed=("21",))
    before = ET.fromstring(export.read_bytes()).find("COLLECTION")
    _apply_export(export)
    written = _routed(export).read_bytes()
    after = ET.fromstring(written).find("COLLECTION")
    assert _ratings_of(written)["21"] == "0", "the analysed track was rated"

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


def test_two_rows_naming_one_file_are_both_counted_as_owed(configured, tagged, tmp_path):
    """rekordbox can hold one file under two ids, and the pass reads the file
    once; each row it files is a row a rating is owed on, and neither is
    written."""
    tracks = RATING_TRACKS | {"26": RATING_TRACKS["21"]}
    ratings = {tid: "0" for tid in tracks}
    export = _write_export(
        configured, tmp_path / "exports", tracks=tracks, ratings=ratings, folders=RATING_FOLDERS
    )
    _code, envelope = _apply_export(export)
    written = _routed(export).read_bytes()
    assert set(_sub_keys(written, "Tech House", "High")) == {"21", "23", "26"}
    rated = _ratings_of(written)
    assert (rated["21"], rated["26"]) == ("0", "0")
    (message,) = _owed(envelope)
    assert message.startswith("4 intake row(s) are owed a star rating"), message


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
    assert (totals["inserted"], totals["long_added"]) == (3, 2)
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
    assert (totals["inserted"], totals["long_added"]) == (0, 0)
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
    assert (totals["inserted"], totals["long_added"]) == (0, 2)
    assert _long_members(_routed(export).read_bytes()) == ("11", "31")
    # Nothing nested was written, so there is no review to warn about (R-694).
    assert _not_landable(envelope) == []


def test_an_export_run_owes_the_import_of_the_root_playlist_it_added_to_alone(
    configured, tagged, tmp_path
):
    """R-694. The long track playlist is the one root playlist the sweep writes
    and the one thing the bridge lands, so it is the whole of the import owed.
    The routing beside it is the review warning's, not the pending action's."""
    export = _long_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == str(Outcome.PENDING)
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "rekordbox_import"
    assert pending["artifact"] == str(_routed(export))
    assert pending["verify_verb"] == "route.inbox"
    assert pending["summary"] == (
        f"2 long track(s) were added to the root playlist '{LONG_PLAYLIST}' in "
        f"{_routed(export).name}, which rekordbox has not imported yet"
    )
    assert pending["steps"] == [
        f"import {_routed(export)} into rekordbox as a rekordbox xml library and "
        f"import from it the '{LONG_PLAYLIST}' playlist alone, and nothing else",
        "leave the routing tree's folders and playlists unimported: a nested "
        "playlist imported from the file lands at the playlist root as a new "
        "playlist, and a folder imported from it keeps every playlist it held and "
        "adds a second copy of each",
        "then export the collection again and run route inbox --export with that "
        "file, which owes no import once the playlist's import has landed, and "
        "whose routing is a review, since the bridge cannot land it",
    ]
    (review,) = _not_landable(envelope)
    assert review.startswith("3 membership(s) routed under the routing tree"), review


def test_the_check_run_after_the_playlist_import_owes_no_import(
    configured, tagged, tmp_path
):
    """R-694, the tenth sitting's shape: the long track playlist landed and the
    routing did not, so the check run plans the same routing again. Before, it
    ended pending on every run and its own check never answered. Now the
    routing is a review and no import is owed, which is the answer."""
    landed = (
        f'      <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="2">',
        '        <TRACK Key="11"/>',
        '        <TRACK Key="31"/>',
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=landed)
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.OK)
    assert envelope["pending_human_action"] is None
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_added"]) == (3, 0)
    assert totals["output"] == str(_routed(export))
    (review,) = _not_landable(envelope)
    assert review.startswith("3 membership(s) routed under the routing tree"), review


def test_no_long_track_builds_no_empty_playlist(configured, tagged, tmp_path):
    export = _long_export(configured, tmp_path / "exports", lengths={"31": "300"})
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["long_added"] == 0
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
    assert envelope["data"]["totals"]["long_added"] == 2
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
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["long_added"] == 0
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
    assert totals["long_added"] == 1
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


def test_a_template_declaring_no_long_track_playlist_builds_none(configured, tagged, tmp_path):
    """The library's active copy says so, on the volume where setup put it.

    The tenth sitting's shape exactly (R-685): an active copy made before the
    shipped template gained ``[long_tracks]``. The shipped template still
    declares the playlist, so a verb reading that instead builds one.
    """
    assert taxonomy.default_taxonomy().long_tracks is not None
    write_active(configured, shipped_without("long_tracks"))
    export = _long_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["long_added"] == 0
    assert _long_members(_routed(export).read_bytes()) is None
    assert all(item["long_track"] == "" for item in envelope["data"]["items"])


def test_an_edit_to_the_active_copy_is_the_playlist_the_routing_plan_names(
    configured, tagged, tmp_path
):
    """An EDIT, not only a removal: the display a person gave the long track
    playlist in their own declaration is the one the plan offers and the file
    holds, and the shipped name appears nowhere (R-685)."""
    from cratekit.write import routing_cli

    shipped = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    line = f'display = "{LONG_PLAYLIST}"'
    assert shipped.count(line) == 1
    write_active(configured, shipped.replace(line, 'display = "Long Sets By Hand"'))
    export = _long_export(configured, tmp_path / "exports")

    planned = routing_cli.plan_export(configured, export)
    long_plan, items = planned.long_plan, planned.items
    assert long_plan.keys
    assert {item["long_track"] for item in items} - {""} == {"Long Sets By Hand"}

    code, envelope = _apply_export(export)
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    offered = {item["long_track"] for item in envelope["data"]["items"]} - {""}
    assert offered == {"Long Sets By Hand"}
    written = _routed(export).read_bytes()
    assert _root_child(written, "Long Sets By Hand") is not None
    assert _long_members(written) is None


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


# ═══════════════════════════════════════════════════════════════════════════
# U89: the routing passes read the calibrated cut and fill "with vox"
# ═══════════════════════════════════════════════════════════════════════════
#
# Every routing caller passed ``vocal_threshold=None``, so the vocal rollout
# ended at tags: calibrate, file, and nothing landed under "with vox" (R-276,
# R-417). Every test below writes a calibration file where the one loader reads
# it, drives the shipped command line, and reads the database or the written
# file back. The cut of 5.0 is spelled here, not read from anywhere, and the
# readings either side of it, 6 and 4, are the brief's.

CUT = 5.0


def _calibrate(cfg: config.Config, text: str) -> Path:
    from cratekit.write import metadata_cli

    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _calibrated(cfg: config.Config) -> Path:
    return _calibrate(cfg, json.dumps({"threshold": CUT, "method": "otsu"}))


def _vox_display() -> str:
    from cratekit.write import trees

    return taxonomy.default_taxonomy().sub_class(trees.VOX_SUB_CLASS).display


def _vox_nodes(cfg: config.Config, root_id: str) -> list[rebuild.TreeNode]:
    """Every vocal sub-playlist under the governed root, read back from the file."""
    handle = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        return [
            node
            for node in rebuild.read_tree(handle, root_id)
            if node.playlist_display == _vox_display()
        ]
    finally:
        rb_writer.close_db(handle)


def _vox_members(cfg: config.Config, root_id: str) -> set[str]:
    return {cid for node in _vox_nodes(cfg, root_id) for cid in node.content_ids}


@pytest.fixture
def vox_levels(monkeypatch) -> dict[str, int]:
    """Voxlevel readings served from the file NAME, set by each test.

    Patched at the tag reader, as ``tagged`` patches genre and energy, so the
    reader the routing derivation calls is the one that runs.
    """
    from cratekit.core import tags

    levels: dict[str, int] = {}
    monkeypatch.setattr(tags, "read_vox_from_file", lambda path: levels.get(Path(path).name))
    return levels


def test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults(tmp_path):
    """One loader, two answers over it: routing needs None, My Tags the default."""
    from cratekit.write import metadata_cli

    cfg = config.from_dict(valid_data(tmp_path / "library"))
    assert metadata_cli.load_vocal_threshold(cfg) is None
    assert metadata_cli.vocal_cut(cfg) == metadata_cli.DEFAULT_VOCAL_THRESHOLD
    _calibrated(cfg)
    assert metadata_cli.load_vocal_threshold(cfg) == CUT
    assert metadata_cli.vocal_cut(cfg) == CUT


@pytest.mark.parametrize("level, filed", [(6, True), (4, False)], ids=["above", "below"])
def test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox(
    acknowledged, native, vox_levels, level, filed
):
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = level
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert _membership(acknowledged, native) == {"2"}
    assert _vox_members(acknowledged, native) == ({"2"} if filed else set())
    assert _vocal_warnings(applied) == [], (
        "the dimension was compared and the warning still says it was not"
    )


def test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox(
    acknowledged, native, vox_levels
):
    vox_levels[ARRIVED] = 60
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert _membership(acknowledged, native) == {"2"}
    assert _vox_members(acknowledged, native) == set()
    assert len(_vocal_warnings(applied)) == 1, applied["warnings"]


def test_a_corrupt_calibration_refuses_the_inbox_and_writes_nothing(
    acknowledged, native, vox_levels
):
    _calibrate(acknowledged, '{"threshold": 5.')
    vox_levels[ARRIVED] = 6
    code, refused = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "vocal-calibration-unreadable", refused
    assert _membership(acknowledged, native) == set()


def test_a_second_calibrated_inbox_creates_no_second_vocal_sub(acknowledged, native, vox_levels):
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    for _ in range(2):
        code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
        assert code == int(ExitCode.OK), applied
    nodes = _vox_nodes(acknowledged, native)
    assert len(nodes) == 1, [(node.folder_display, node.playlist_id) for node in nodes]
    assert nodes[0].content_ids == frozenset({"2"})


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
@pytest.mark.parametrize("level, filed", [(6, True), (4, False)], ids=["above", "below"])
def test_a_calibrated_resume_files_under_with_vox_and_does_not_warn(
    acknowledged, native, vox_levels, argv, level, filed
):
    job_id = _drive(argv)[1]["data"]["job_id"]
    _calibrated(acknowledged)
    vox_levels[SHELVED] = level
    code, done = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _vox_members(acknowledged, native) == ({"1"} if filed else set())
    assert _vocal_warnings(done) == [], (
        "the resume said the vocal dimension was not compared over a job that compared it"
    )


@pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)
def test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs(
    acknowledged, native, vox_levels, argv
):
    job_id = _drive(argv)[1]["data"]["job_id"]
    _calibrate(acknowledged, "")
    vox_levels[SHELVED] = 6
    code, refused = _drive([*argv, "--job", job_id])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "vocal-calibration-unreadable", refused
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.PENDING]
    assert _membership(acknowledged, native) == set()


def test_a_worker_driven_without_the_resume_refuses_a_corrupt_calibration(
    acknowledged, native, vox_levels
):
    """The worker reads the cut itself, so ``job resume`` cannot slip past it."""
    from cratekit.cli import rebuild as rebuild_verb
    from cratekit.core.cause import CratekitError

    _calibrate(acknowledged, '{"threshold": NaN}')
    vox_levels[SHELVED] = 6
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    with pytest.raises(CratekitError) as caught:
        rebuild_verb.handle(object(), item, acknowledged)
    assert caught.value.cause.reason == "vocal-calibration-unreadable"
    assert _membership(acknowledged, native) == set()


def test_converge_compares_the_vocal_sub_once_calibrated(acknowledged, native, vox_levels):
    from cratekit.cli import converge

    vox_levels[SHELVED] = 6
    code, before = _drive(["converge"])
    assert code == int(ExitCode.OK), before
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    _calibrated(acknowledged)
    _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert _vox_members(acknowledged, native) == {"1"}

    code, after = _drive(["converge"])
    assert code == int(ExitCode.OK), after
    (check,) = [c for c in after["data"]["checks"] if c["key"] == f"tree.{TREE_ID}"]
    assert check["status"] == converge.MATCHING, check
    assert "not compared" not in check["detail"], check


def test_a_corrupt_calibration_is_converge_not_comparing_rather_than_a_match(
    acknowledged, native
):
    from cratekit.cli import converge

    _calibrate(acknowledged, '{"method": "otsu"}')
    code, envelope = _drive(["converge"])
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == f"tree.{TREE_ID}"]
    assert check["status"] == converge.NOT_COMPARED, check
    assert "vocal calibration" in check["detail"], check


# The export medium. Track 11 is Deep House at energy 2, track 12 Deep House at
# energy 5, track 13 Tech House at energy 8 (EXPORT_TRACKS).


@pytest.fixture
def voiced(tagged, monkeypatch) -> dict[str, int]:
    """``tagged``, with voxlevel readings served from the file name as well."""
    from cratekit.core import tags

    del tagged
    levels: dict[str, int] = {}
    monkeypatch.setattr(tags, "read_vox_from_file", lambda path: levels.get(Path(path).name))
    return levels


def _export_vox(document: bytes, folder: str) -> tuple[str, ...] | None:
    """What one folder's vocal sub holds in a written file, None when it has none."""
    import xml.etree.ElementTree as ET

    declared = taxonomy.default_taxonomy()
    root = ET.fromstring(document)
    tree = next(
        node for node in root.find("PLAYLISTS")[0] if node.get("Name") == declared.tree.display
    )
    bucket = next(node for node in tree if node.get("Name") == folder)
    subs = [node for node in bucket if node.get("Name") == _vox_display()]
    if not subs:
        return None
    (playlist,) = subs
    return tuple(track.get("Key") for track in playlist.findall("TRACK"))


def test_a_calibrated_export_files_over_the_cut_and_not_under_it(configured, voiced, tmp_path):
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    voiced["Mid Track.flac"] = 4
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert totals["not_derived"] == []
    assert totals["vox_created"] == [f"Deep House/{_vox_display()}", f"Tech House/{_vox_display()}"]
    written = _routed(export).read_bytes()
    assert _export_vox(written, "Deep House") == ("11",)
    assert _export_vox(written, "Tech House") == ()
    # Still filed by energy as well: the vocal sub is additive.
    assert _sub_keys(written, "Deep House", "Low") == ("11",)
    assert _sub_keys(written, "Deep House", "Med") == ("12",)
    offered = {item["track_id"]: item["vocal"] for item in envelope["data"]["items"]}
    assert offered == {
        "11": f"Deep House/{_vox_display()}",
        "12": "",
        "13": "",
        "": "",
    }
    created = [item["destination"] for item in envelope["data"]["items"] if not item["track_id"]]
    assert created == totals["vox_created"]
    # R-694: the subs are nested, so the review names them and no import is owed.
    assert envelope["pending_human_action"] is None
    (review,) = _not_landable(envelope)
    assert "and 2 sub-playlist(s) created" in review, review


# ═══════════════════════════════════════════════════════════════════════════
# R-686: the apply gate shows the plan it asks about
# ═══════════════════════════════════════════════════════════════════════════


def _blocked_export(export: Path) -> dict:
    code, envelope = _drive(["route", "inbox", "--export", str(export)])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    return envelope


def _gate_export(configured, voiced, tmp_path) -> Path:
    """One export whose plan carries every column: a routed track, a vocal
    track, a long track in and out of the intake, and two new subs, plus one
    owed rating the plan does not carry (R-688)."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    return _long_export(configured, tmp_path / "exports", ratings={"12": "0"})


def test_the_export_gate_shows_every_item_the_digest_was_taken_over(
    configured, voiced, tmp_path
):
    """The gate carried the question and not one item. Its ``shown`` now holds
    the declined run's items, byte for byte once the names R-692 added are
    dropped, and the digest they were taken over, so what a person approves is
    what they read."""
    export = _gate_export(configured, voiced, tmp_path)
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    code, declined = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), declined
    assert _unnamed(shown["items"]) == declined["data"]["items"]
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["count"] == 6
    assert shown["export"] == str(export)
    counted = (shown["tracks"], shown["routed"], shown["vocal"], shown["long tracks"])
    assert counted == (4, 3, 1, 2)
    vox = _vox_display()
    assert shown["vocal subs created"] == [f"Deep House/{vox}", f"Tech House/{vox}"]
    assert shown["not derived"] == []
    (warning,) = shown["warnings"]
    assert warning.startswith("1 intake row(s) are owed a star rating"), warning
    assert not _routed(export).exists()


def test_the_export_gate_names_the_vocal_dimension_it_did_not_read(
    configured, voiced, tmp_path
):
    """Uncalibrated, the vocal column is empty because it was not read, and the
    screen says so rather than letting it read as no vocal tracks."""
    export = _write_export(configured, tmp_path / "exports")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    assert shown["not derived"] == [rebuild.VOCAL_DIMENSION]
    assert (shown["routed"], shown["vocal"]) == (3, 0)


def test_the_export_gate_screen_says_none_for_an_empty_warning_list(
    configured, voiced, tmp_path
):
    """An empty list says none, rather than a header with nothing under it. The
    rows here carry no rating attribute, so nothing is owed and nothing warns."""
    export = _write_export(configured, tmp_path / "exports")
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["route", "inbox", "--export", str(export)], stdout=out, stderr=err)
    assert code == int(ExitCode.DECISION_REQUIRED), err.getvalue()
    assert "  warnings: none" in out.getvalue() + err.getvalue()


def test_the_export_gate_says_why_an_intake_track_goes_nowhere(configured, voiced, tmp_path):
    """The case the screen matters most for: a track the planner could not
    read is listed with no destination, and its reason is on the screen before
    the answer rather than in the envelope after it."""
    export = _write_export(configured, tmp_path / "exports", missing_file="12")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    offered = {item["track_id"]: item["destination"] for item in shown["items"]}
    assert offered == {"11": "Deep House/Low", "12": "", "13": "Tech House/High"}
    assert (shown["tracks"], shown["routed"]) == (3, 2)
    (warning,) = shown["warnings"]
    assert "track 12" in warning and "not routed" in warning


def test_the_export_gate_prints_the_plan_in_the_default_mode(configured, voiced, tmp_path):
    """The human screen is the one a person answers from, so the plan has to
    reach it and not stop at the JSON envelope."""
    export = _gate_export(configured, voiced, tmp_path)
    digest = _blocked_export(export)["cause"]["detail"]["shown"]["digest"]
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["route", "inbox", "--export", str(export)], stdout=out, stderr=err)
    assert code == int(ExitCode.DECISION_REQUIRED), err.getvalue()
    screen = out.getvalue() + err.getvalue()
    assert "Apply this routing plan to the library?" in screen
    assert f"digest: {digest}" in screen
    assert "routed: 3" in screen and "long tracks: 2" in screen
    assert "  not derived: none" in screen
    assert "are owed a star rating" in screen, "the owed rating never reached the screen"
    vox = _vox_display()
    assert (
        f"artist=Artist 11, title=Track 11, track_id=11, destination=Deep House/Low, "
        f"vocal=Deep House/{vox}, long_track=" in screen
    )
    assert "rating=" not in screen
    assert f"long_track={LONG_PLAYLIST}" in screen
    assert f"artist=, title=, track_id=, destination=Tech House/{vox}," in screen


def _unnamed(items: list[dict]) -> list[dict]:
    """The shown items without the names the screen alone carries (R-692)."""
    return [
        {key: value for key, value in item.items() if key not in ("artist", "title")}
        for item in items
    ]


def test_the_export_gate_names_each_track_by_artist_and_title(configured, voiced, tmp_path):
    """R-692 in one test: a title and an artist are read off the gate's
    ``shown``, beside the export id the digest covers, while the declined
    envelope's items and the digest are the plan's, unnamed. A long track
    outside the intake is named too, and a created vocal sub, which is no
    track, gets empty names rather than a missing column. The JSON envelope
    sorts its keys, so the names leading each line is the default mode
    screen's test, not this one's."""
    export = _gate_export(configured, voiced, tmp_path)
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    named = [(item["track_id"], item["artist"], item["title"]) for item in shown["items"]]
    assert named == [
        ("11", "Artist 11", "Track 11"),
        ("12", "Artist 12", "Track 12"),
        ("13", "Artist 13", "Track 13"),
        ("31", "Artist 31", "Track 31"),
        ("", "", ""),
        ("", "", ""),
    ]
    code, declined = _drive(
        ["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)]
    )
    assert code == int(ExitCode.OK), declined
    assert all(
        "artist" not in item and "title" not in item for item in declined["data"]["items"]
    )
    assert _unnamed(shown["items"]) == declined["data"]["items"]
    assert shown["digest"] == declined["data"]["digest"]


def test_the_export_gate_leaves_an_unread_track_unnamed(configured, voiced, tmp_path):
    """An intake key with no collection row is still listed, with its reason
    in the warnings, and has no name to show rather than a borrowed one."""
    export = _write_export(configured, tmp_path / "exports", inbox=("11", "99"))
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    named = [(item["track_id"], item["artist"], item["title"]) for item in shown["items"]]
    assert named == [("11", "Artist 11", "Track 11"), ("99", "", "")]


def test_the_database_inbox_gate_shows_its_items(acknowledged, native, vox_levels):
    """The same gate on the database path was as blind, and one carry serves it."""
    code, blocked = _drive(["route", "inbox"])
    assert code == int(ExitCode.DECISION_REQUIRED), blocked
    shown = blocked["cause"]["detail"]["shown"]
    code, declined = _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])
    assert code == int(ExitCode.OK), declined
    assert shown["items"] == declined["data"]["items"] != []
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["count"] == len(declined["data"]["items"])


# ═══════════════════════════════════════════════════════════════════════════
# R-691: the database path plans its placements before the gate
# ═══════════════════════════════════════════════════════════════════════════
#
# The database path's plan was the file list, and the routing was decided in
# the apply after the answer, so R-686's carry showed the files and not one
# destination. The plan now carries where each file goes, the digest binds it,
# and the write consumes the plan the person read.

#: Where the shipped rules file an untagged intake file: the declared fallback
#: bucket and its sink, as display names, the way the export gate names them.
FALLBACK_DESTINATION = "Electronica / Other/Unsorted"


def _blocked_inbox() -> dict:
    code, blocked = _drive(["route", "inbox"])
    assert code == int(ExitCode.DECISION_REQUIRED), blocked
    return blocked["cause"]["detail"]["shown"]


def _filed_under(cfg: config.Config, root_id: str, content_id: str) -> set[str]:
    """Every ``folder/playlist`` under the governed root holding this row."""
    handle = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        return {
            f"{node.folder_display}/{node.playlist_display}"
            for node in rebuild.read_tree(handle, root_id)
            if content_id in node.content_ids
        }
    finally:
        rb_writer.close_db(handle)


def test_the_database_inbox_gate_shows_each_files_destination(acknowledged, native):
    """The residual in one test: a destination is read off the gate's ``shown``,
    the items are the declined run's byte for byte, and the totals are counted
    off them the way the export gate's are."""
    shown = _blocked_inbox()
    intake = _intake_dir(acknowledged)
    assert shown["items"] == [
        {
            "path": str(intake / ARRIVED),
            "name": ARRIVED,
            "destination": FALLBACK_DESTINATION,
            "vocal": "",
        }
    ]
    code, declined = _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])
    assert code == int(ExitCode.OK), declined
    assert shown["items"] == declined["data"]["items"]
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["intake"] == str(intake)
    assert (shown["count"], shown["tracks"], shown["routed"], shown["vocal"]) == (1, 1, 1, 0)
    assert shown["trees"] == [TREE_ID]
    assert shown["not derived"] == [rebuild.VOCAL_DIMENSION]
    assert shown["warnings"] == []


def test_the_database_apply_files_the_track_where_the_gate_said(acknowledged, native, vox_levels):
    """The plan the gate showed is the plan the write consumes, asserted where it
    can be seen: the row lands under the folder and playlist the screen named,
    and under the vocal sub the screen named once the library is calibrated."""
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    shown = _blocked_inbox()
    (item,) = shown["items"]
    vox = _vox_display()
    assert item["destination"] == FALLBACK_DESTINATION
    assert item["vocal"] == f"Electronica / Other/{vox}"
    assert (shown["routed"], shown["vocal"]) == (1, 1)
    assert shown["not derived"] == []

    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["digest"] == shown["digest"]
    assert _filed_under(acknowledged, native, "2") == {item["destination"], item["vocal"]}


def test_the_database_digest_binds_the_destinations_not_the_file_list(
    acknowledged, native, vox_levels
):
    """The defect's other half. The digest was taken over the file list, so a
    decision recorded against it stayed valid while the routing underneath it
    changed. Now a reading that moves a placement moves the digest, over one
    unchanged folder."""
    before = _blocked_inbox()
    assert [item["vocal"] for item in before["items"]] == [""]
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    after = _blocked_inbox()
    assert [item["name"] for item in after["items"]] == [item["name"] for item in before["items"]]
    assert [item["vocal"] for item in after["items"]] != [""]
    assert after["digest"] != before["digest"], (
        "the placement changed and the digest did not, so the digest binds the "
        "file list and not where the files go"
    )


def test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer(
    stocked, monkeypatch
):
    """Nothing native means nothing derived and nothing written, and the gate
    says so before the question rather than the envelope after it: every file
    is listed with no destination and the export remedy is on the screen.

    Nothing is read for it either. The review found the first draft loading
    the calibration and every file's tags on a library that can use neither,
    so a corrupt calibration refused a verb whose real answer is the export
    remedy. The reader is armed to raise, and the calibration is corrupt, and
    the gate still shows the plan; the declined envelope carries the same
    warning the screen did, so a reader of the JSON learns why every
    destination is empty."""
    _calibrate(stocked, '{"threshold": 5.')

    def unread(path):
        raise AssertionError(f"read {path} on a library with nothing native")

    monkeypatch.setattr(rebuild, "read_truth", unread)
    shown = _blocked_inbox()
    assert [item["destination"] for item in shown["items"]] == [""]
    assert (shown["tracks"], shown["routed"], shown["trees"]) == (1, 0, [])
    assert shown["warnings"] == [routing_cli.EXPORT_REMEDY]
    assert not Path(stocked.library.db_path).exists(), "the plan opened a database"

    code, declined = _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])
    assert code == int(ExitCode.OK), declined
    assert declined["data"]["totals"]["applied"] is False
    assert [w["message"] for w in declined["warnings"]] == [routing_cli.EXPORT_REMEDY]


def test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy(stocked):
    """Both facts are true of the state, and both surfaces now say both: the
    gate shows the remedy, and the confirmed answer is still inbox-empty and
    carries the same warning rather than dropping it."""
    for path in _intake_dir(stocked).iterdir():
        path.unlink()
    shown = _blocked_inbox()
    assert shown["items"] == [] and shown["warnings"] == [routing_cli.EXPORT_REMEDY]
    code, applied = _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["reason"] == "inbox-empty"
    assert [w["message"] for w in applied["warnings"]] == [routing_cli.EXPORT_REMEDY]


def test_an_empty_inbox_plan_names_every_native_tree(acknowledged, native):
    """The write indexes the plan by tree, so a plan over an empty folder still
    carries every tree that has cut over, with nothing to place in it, rather
    than a mapping the write would fail to index inside an open database."""
    for path in _intake_dir(acknowledged).iterdir():
        path.unlink()
    planned = routing_cli.plan_inbox(acknowledged, taxonomy.default_taxonomy())
    assert planned.items == []
    assert planned.placements == {TREE_ID: ()}
    assert planned.warnings == []


def test_the_database_gate_prints_the_destination_in_the_default_mode(acknowledged, native):
    """The human screen is the one a person answers from."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["route", "inbox"], stdout=out, stderr=err)
    assert code == int(ExitCode.DECISION_REQUIRED), err.getvalue()
    screen = out.getvalue() + err.getvalue()
    assert "Apply this routing plan to the library?" in screen
    assert f"name={ARRIVED}, destination={FALLBACK_DESTINATION}, vocal=" in screen
    assert "routed: 1" in screen
    assert f"trees:\n    {TREE_ID}" in screen, screen
    assert "  warnings: none" in screen


def test_an_uncalibrated_export_creates_no_vocal_sub_and_names_the_gap(
    configured, voiced, tmp_path
):
    voiced["Low Track.flac"] = 60
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert totals["not_derived"] == [rebuild.VOCAL_DIMENSION]
    assert totals["vox_created"] == []
    written = _routed(export).read_bytes()
    assert _export_vox(written, "Deep House") is None
    assert _export_vox(written, "Tech House") is None


def test_a_corrupt_calibration_refuses_the_export_before_the_plan(configured, voiced, tmp_path):
    _calibrate(configured, '{"threshold": true}')
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "vocal-calibration-unreadable", envelope
    assert not _routed(export).exists()


def test_the_export_vocal_subs_are_created_once(configured, voiced, tmp_path):
    """A second run over its own output creates none and has nothing to route."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    export = _write_export(configured, tmp_path / "exports")
    _apply_export(export)
    first = _routed(export)
    written = first.read_bytes()
    assert written.count(f'Name="{_vox_display()}"'.encode()) == 2

    code, again = _apply_export(first)
    assert code == int(ExitCode.OK), again
    totals = again["data"]["totals"]
    assert totals["vox_created"] == []
    assert totals["inserted"] == 0
    assert totals["reason"] == "nothing-to-route"
    assert [item for item in again["data"]["items"] if not item["track_id"]] == []


def test_vocal_subs_alone_are_a_change_and_write_a_file(configured, voiced, tmp_path):
    """Every track already filed, and the subs still missing: the file carries them."""
    _calibrated(configured)
    export = _write_export(configured, tmp_path / "exports")
    _apply_export(export)
    filed = _routed(export)
    without = filed.read_bytes().replace(
        f'Name="{_vox_display()}"'.encode(), b'Name="Removed Sub"'
    )
    bare = tmp_path / "again" / "library_FRESH.xml"
    bare.parent.mkdir()
    bare.write_bytes(without)
    code, envelope = _apply_export(bare)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 0
    assert len(envelope["data"]["totals"]["vox_created"]) == 2
    assert _routed(bare).is_file()
    # R-694: a created sub is nested too, so a file of subs alone is a review.
    assert envelope["pending_human_action"] is None
    (review,) = _not_landable(envelope)
    assert review.startswith("0 membership(s) routed and 2 sub-playlist(s) created"), review


def test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing(
    configured, voiced, tmp_path
):
    """The vocal writer raises on an unreachable tree, and the pass carries it as
    a skipped write beside the routing writer's own, not as a traceback."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    export = _write_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().tree.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Other"'))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    assert envelope["data"]["totals"]["vox_created"] == []
    messages = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any("no vocal sub-playlist was created" in m for m in messages), messages
    assert not _routed(export).exists()


def test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none(
    configured, voiced, no_vocal_dimension, tmp_path
):
    del no_vocal_dimension
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    export = _write_export(configured, tmp_path / "exports")
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["vox_created"] == []
    assert envelope["data"]["totals"]["not_derived"] == []
    # Spelled, because the narrowed taxonomy no longer declares the name.
    assert b'Name="with vox"' not in _routed(export).read_bytes()


def test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served(
    configured, voiced, tmp_path
):
    """A FOLDER of the vocal name where the playlist belongs is refused by the
    emitter, and that refusal reaches the envelope rather than reading as a
    folder that already had its sub (the zero row E6 of the U89 table)."""
    _calibrated(configured)
    vox = _vox_display()
    export = _write_export(
        configured,
        tmp_path / "exports",
        folders=(("Deep House", ("Low", "Med", "High", vox)), ("Tech House", ("Low", "Med", "High"))),
    )
    export.write_bytes(
        export.read_bytes().replace(f'Name="{vox}" Type="1"'.encode(), f'Name="{vox}" Type="0"'.encode())
    )
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["vox_created"] == [f"Tech House/{vox}"]
    messages = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any(vox in m for m in messages), messages


# ═══════════════════════════════════════════════════════════════════════════
# U91: route unplaced --export places what the routing tree does not hold
# ═══════════════════════════════════════════════════════════════════════════
#
# The source system's ``dj-sort-unplaced`` read a fresh export, routed every
# collection track no playlist under the routing tree held, created a sub where
# the bucket had none, and wrote a new file to import. Every test goes through
# the shipped command line and reads the OUTPUT FILE back.


def _placed_folder(
    name: str, subs: tuple[str, ...], held: dict[tuple[str, str], tuple[str, ...]]
) -> list[str]:
    """One genre folder whose subs hold the keys ``held`` names for them."""
    lines = [f'        <NODE Type="0" Name="{name}" Count="{len(subs)}">']
    for sub in subs:
        keys = held.get((name, sub), ())
        if not keys:
            lines.append(f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="0"/>')
            continue
        lines.append(
            f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="{len(keys)}">'
        )
        lines += [f'            <TRACK Key="{key}"/>' for key in keys]
        lines.append("          </NODE>")
    lines.append("        </NODE>")
    return lines


def _unplaced_export(
    cfg: config.Config,
    folder: Path,
    *,
    held: dict[tuple[str, str], tuple[str, ...]] | None = None,
    folders: tuple[tuple[str, tuple[str, ...]], ...] | None = None,
    intake: tuple[str, ...] = (),
    missing_file: str | None = None,
    root_extra: tuple[str, ...] = (),
) -> Path:
    """A fresh export whose routing tree already holds ``held`` and nothing else.

    Every track is a real file under the library, as in ``_write_export``, and
    track 11 is analysed, so its row carries an average tempo and a tempo
    element the sweep must leave byte for byte.
    """
    from cratekit.core import locations
    from tests.xml_fixtures import _xml_doc

    held = held or {}
    if folders is None:
        folders = (("Deep House", ("Low", "Med")), ("Tech House", ("Low", "Med")))
    music = Path(cfg.library.root) / "Music"
    rows: list[str] = []
    for tid, (name, *_rest) in EXPORT_TRACKS.items():
        path = music / name
        if tid != missing_file:
            path.write_bytes(b"")
        rows += _export_track(tid, locations.location_url(path), analyzed=tid == "11")
    declared = taxonomy.default_taxonomy()
    document = _xml_doc(
        collection=[
            f'  <COLLECTION Entries="{len(EXPORT_TRACKS)}">', *rows, "  </COLLECTION>"
        ],
        root_children=[
            f'      <NODE Type="0" Name="{declared.intake.display}" Count="1">',
            '        <NODE Name="2026-09-19 batch" Type="1" KeyType="0" '
            f'Entries="{len(intake)}">',
            *(f'          <TRACK Key="{key}"/>' for key in intake),
            "        </NODE>",
            "      </NODE>",
            f'      <NODE Type="0" Name="{declared.tree.display}" Count="{len(folders)}">',
            *(line for name, subs in folders for line in _placed_folder(name, subs, held)),
            "      </NODE>",
            *root_extra,
        ],
    )
    folder.mkdir(parents=True, exist_ok=True)
    export = folder / "library_FRESH.xml"
    export.write_bytes(document)
    return export


def _placed(export: Path) -> Path:
    return export.with_name(export.stem + "_placed.xml")


def _sweep(export: Path) -> tuple[int, dict]:
    return _drive(["route", "unplaced", "--export", str(export)])


def test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created(
    configured, tagged, tmp_path
):
    """The creating writer: Tech House has no High, so the sweep makes one."""
    export = _unplaced_export(configured, tmp_path / "exports")
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.OK)
    totals = envelope["data"]["totals"]
    assert totals["applied"] is True
    assert totals["inserted"] == 3
    assert totals["created"] == ["Tech House/High"]
    assert totals["output"] == str(_placed(export))

    written = _placed(export).read_bytes()
    for tid, (_name, _genre, _energy, (folder, sub)) in EXPORT_TRACKS.items():
        assert _sub_keys(written, folder, sub) == (tid,), (
            f"track {tid} did not land in {folder}/{sub} alone"
        )
    assert {
        item["track_id"]: item["destination"] for item in envelope["data"]["items"]
    } == {tid: f"{folder}/{sub}" for tid, (*_, (folder, sub)) in EXPORT_TRACKS.items()}

    # R-694: every placement is nested membership, which the bridge never
    # lands (R-687), so no import is owed and the review warning carries the
    # step a person takes instead.
    assert envelope["pending_human_action"] is None
    assert _not_landable(envelope) == [
        f"3 membership(s) routed and 1 sub-playlist(s) created under the routing "
        f"tree in {_placed(export).name} are a review that no import can land: a "
        "nested playlist imported from the file lands at the playlist root as a "
        "new playlist, and a folder imported from it keeps every playlist it held "
        "and adds a second copy of each; file the tracks this review names by "
        "hand in rekordbox, and route unplaced without --export only reports; "
        "until they are filed, route unplaced --export plans the same placements "
        "on every fresh export",
    ]
    assert export.read_bytes() != written, "the export itself was the file written"


def test_the_unplaced_check_run_owes_no_import_before_the_tracks_are_filed(
    configured, tagged, tmp_path
):
    """R-694. A fresh export taken after a person read the review and filed one
    of its three tracks by hand plans the other two again, since none of the
    placements could land from the file. The answer is the same review with no
    import owed, not a pending import whose own check could never answer."""
    code, first = _sweep(_unplaced_export(configured, tmp_path / "before"))
    assert code == int(ExitCode.OK), first
    assert first["pending_human_action"] is None
    later = _unplaced_export(
        configured, tmp_path / "after", held={("Deep House", "Low"): ("11",)}
    )
    code, again = _sweep(later)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == str(Outcome.OK)
    assert again["pending_human_action"] is None
    assert [item["track_id"] for item in again["data"]["items"]] == ["12", "13"]
    assert again["data"]["totals"]["inserted"] == 2
    (review,) = _not_landable(again)
    assert review.startswith("2 membership(s) routed and 1 sub-playlist(s) created"), review


def test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it(
    configured, tagged, tmp_path
):
    """Placed means held anywhere under the tree, not held where the rule says.

    Track 11 routes to Deep House/Low and a person filed it in Med by hand. The
    sweep leaves it there and does not add a second copy under Low.
    """
    export = _unplaced_export(
        configured, tmp_path / "exports", held={("Deep House", "Med"): ("11",)}
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    assert [item["track_id"] for item in envelope["data"]["items"]] == ["12", "13"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Deep House", "Low") == ()
    assert _sub_keys(written, "Deep House", "Med") == ("11", "12")


def test_a_track_held_only_in_a_vocal_sub_is_placed(configured, tagged, tmp_path):
    """Any sub under the tree places a track, the vocal sub included."""
    vox = _vox_display()
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        folders=(("Deep House", ("Low", "Med")), ("Tech House", ("Low", vox))),
        held={("Tech House", vox): ("13",)},
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert "13" not in {item["track_id"] for item in envelope["data"]["items"]}
    assert envelope["data"]["totals"]["created"] == []
    assert b'Name="High"' not in _placed(export).read_bytes()


def test_a_track_held_only_outside_the_tree_is_unplaced(configured, tagged, tmp_path):
    """The intake folder and a root playlist are not the routing tree."""
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        intake=("12",),
        root_extra=(
            '      <NODE Name="Warm up" Type="1" KeyType="0" Entries="1">',
            '        <TRACK Key="11"/>',
            "      </NODE>",
        ),
        held={("Tech House", "Low"): ("13",)},
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert [item["track_id"] for item in envelope["data"]["items"]] == ["11", "12"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Deep House", "Low") == ("11",)
    assert _sub_keys(written, "Deep House", "Med") == ("12",)


def test_without_the_flag_nothing_is_written_and_the_answer_names_the_flag(
    configured, tagged, tmp_path
):
    """The report R-313 made stays a report, and says which medium places."""
    export = _unplaced_export(configured, tmp_path / "exports")
    before = {path.name: path.read_bytes() for path in export.parent.iterdir()}
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["compared"] is False
    assert [w["code"] for w in envelope["warnings"]] == ["no-native-tree"]
    assert "route unplaced --export" in envelope["warnings"][0]["message"]
    assert {path.name: path.read_bytes() for path in export.parent.iterdir()} == before


def test_no_tempo_or_bpm_attribute_differs_after_the_sweep(configured, tagged, tmp_path):
    """Never write a beat grid: every grid token the export held comes back as it was."""
    import re

    export = _unplaced_export(configured, tmp_path / "exports")
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    grid = re.compile(rb'<TEMPO[^>]*>|\b(?:AverageBpm|Bpm|Inizio|Metro|Battito)="[^"]*"')
    before = grid.findall(export.read_bytes())
    assert before, "the fixture carries no grid, so this compares nothing"
    assert grid.findall(_placed(export).read_bytes()) == before


def test_a_second_sweep_over_its_own_output_places_nothing(configured, tagged, tmp_path):
    """Idempotent, and a sweep that placed nothing writes no file to import."""
    export = _unplaced_export(configured, tmp_path / "exports")
    _sweep(export)
    first = _placed(export)
    before = sorted(path.name for path in first.parent.iterdir())
    code, envelope = _sweep(first)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    totals = envelope["data"]["totals"]
    assert totals["inserted"] == 0
    assert totals["reason"] == "nothing-to-route"
    assert totals["output"] is None
    assert sorted(path.name for path in first.parent.iterdir()) == before


def test_an_unreadable_track_is_a_warning_and_the_rest_are_placed(
    configured, tagged, tmp_path
):
    export = _unplaced_export(configured, tmp_path / "exports", missing_file="13")
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    assert [w["code"] for w in _others(envelope)] == ["track-file-unreadable"]
    assert b'Name="High"' not in _placed(export).read_bytes()


def test_a_sweep_that_could_place_nothing_is_blocked_not_done(configured, tagged, tmp_path):
    """The one unplaced track cannot be read, so nothing is written, and the
    answer must not be the ``nothing-to-route`` the import check reads as done."""
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        held={("Deep House", "Low"): ("11",), ("Deep House", "Med"): ("12",)},
        missing_file="13",
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    assert not _placed(export).exists()


def test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented(
    configured, tagged, tmp_path
):
    """The creating writer makes a sub, never a genre folder."""
    export = _unplaced_export(
        configured, tmp_path / "exports", folders=(("Deep House", ("Low", "Med")),)
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    messages = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any("Tech House" in message for message in messages), messages
    assert b'Name="Tech House"' not in _placed(export).read_bytes()


def test_a_cut_over_tree_refuses_the_sweep_and_writes_nothing(configured, tagged, tmp_path):
    _cut_over_routing_tree(configured)
    export = _unplaced_export(configured, tmp_path / "exports")
    code, envelope = _sweep(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "tree-unconverged"
    assert "route unplaced without --export" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not _placed(export).exists()


@pytest.mark.parametrize(
    "replacement",
    [b'Type="0" Name="Elsewhere"', b'Type="1" Name="{tree}"'],
    ids=["absent", "a-playlist-of-that-name"],
)
def test_an_export_with_no_routing_tree_refuses(configured, tagged, tmp_path, replacement):
    """Every track would read as unplaced and every write be skipped."""
    display = taxonomy.default_taxonomy().tree.display
    export = _unplaced_export(configured, tmp_path / "exports")
    export.write_bytes(
        export.read_bytes().replace(
            f'Type="0" Name="{display}"'.encode(),
            replacement.replace(b"{tree}", display.encode()),
        )
    )
    code, envelope = _sweep(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "governed-tree-absent"
    assert not _placed(export).exists()


def test_an_unmounted_library_refuses_the_sweep(configured, tagged, tmp_path, monkeypatch):
    export = _unplaced_export(configured, tmp_path / "exports")
    real = Path.is_dir
    root = Path(configured.library.root)
    monkeypatch.setattr(Path, "is_dir", lambda self: False if self == root else real(self))
    code, envelope = _sweep(export)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert not _placed(export).exists()


def test_the_sweep_runs_with_rekordbox_open_and_opens_no_database(
    configured, tagged, tmp_path, monkeypatch
):
    """The export medium writes a new file, so rekordbox running costs nothing."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)

    def no_open(*args, **kwargs):
        raise AssertionError("the export sweep opened the database")

    monkeypatch.setattr(rb_writer, "open_db", no_open)
    export = _unplaced_export(configured, tmp_path / "exports")
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert not session.lock_path(configured).exists()


def test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates(
    configured, voiced, tmp_path
):
    """Over the cut, a track files under its energy sub and the vocal sub, and
    the creating writer makes the vocal sub where the folder has none."""
    _calibrated(configured)
    voiced["Top Track.flac"] = 6
    vox = _vox_display()
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        folders=(("Deep House", ("Low", "Med")), ("Tech House", ("Low", "Med", "High"))),
    )
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["created"] == [f"Tech House/{vox}"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert _sub_keys(written, "Tech House", vox) == ("13",)
    vocal = {item["track_id"]: item["vocal"] for item in envelope["data"]["items"]}
    assert vocal == {"11": "", "12": "", "13": f"Tech House/{vox}"}


def test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses(
    configured, tagged, tmp_path
):
    """Found by U91's hunt, driven before the fix: a line an old splicer ended
    with a bare LF, just above a genre folder's close, put the created sub one
    byte early, splitting a ``/>``, and the sweep wrote a file no parser reads."""
    import xml.etree.ElementTree as ET

    export = _unplaced_export(configured, tmp_path / "exports")
    last_sub = b'<NODE Name="Med" Type="1" KeyType="0" Entries="0"/>\r\n        </NODE>'
    document = export.read_bytes()
    assert document.count(last_sub) == 2, "the fixture no longer has the shape this bends"
    at = document.rindex(last_sub)
    export.write_bytes(document[:at] + last_sub.replace(b"\r\n", b"\n") + document[at + len(last_sub):])

    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["created"] == []
    messages = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any("Tech House" in m and "CRLF" in m for m in messages), messages
    written = _placed(export).read_bytes()
    ET.fromstring(written)
    assert _sub_keys(written, "Deep House", "Low") == ("11",)


def test_the_creating_writer_refuses_a_document_whose_lines_end_in_lf():
    """The engine alone, every line LF: nothing written rather than a corrupt file."""
    from cratekit.write import trees

    lines = [
        b'<?xml version="1.0" encoding="UTF-8"?>',
        b'<DJ_PLAYLISTS Version="1.0.0">',
        b'  <PLAYLISTS>',
        b'    <NODE Type="0" Name="ROOT" Count="1">',
        b'      <NODE Type="0" Name="Deep House" Count="1">',
        b'        <NODE Name="Low" Type="1" KeyType="0" Entries="0"/>',
        b"      </NODE>",
        b"    </NODE>",
        b"  </PLAYLISTS>",
        b"</DJ_PLAYLISTS>",
        b"",
    ]
    document = b"\n".join(lines)
    buffer = bytearray(document)
    report = trees.apply_unplaced_changes({("Deep House", "High"): ["1"]}, buffer)
    assert report.inserted == 0 and report.created == ()
    assert len(report.warnings) == 1 and "CRLF" in report.warnings[0]
    assert bytes(buffer) == document


def test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing(
    configured, tagged, tmp_path
):
    """The writer is told the tree, so it searches the tree alone (U91's U6 row).

    A folder named Tech House sits in the intake folder, BEFORE the routing tree
    in the document. Unscoped, the search finds it first and the created High
    lands there, outside every tree a person routes by.
    """
    export = _unplaced_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().intake.display
    opening = f'<NODE Type="0" Name="{display}" Count="1">\r\n'.encode()
    namesake = (
        b'        <NODE Type="0" Name="Tech House" Count="1">\r\n'
        b'          <NODE Name="Low" Type="1" KeyType="0" Entries="0"/>\r\n'
        b"        </NODE>\r\n"
    )
    document = export.read_bytes()
    assert document.count(opening) == 1, "the fixture no longer has the shape this bends"
    export.write_bytes(document.replace(opening, opening + namesake))

    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["created"] == ["Tech House/High"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert written.count(b'Name="High"') == 1, "a High was created outside the routing tree"


def test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent(
    configured, tagged, tmp_path
):
    """The inbox sweep hands _decide only rows it has, so a key with no row is
    one warning naming the row, not a second one about a file (U91's P1 row)."""
    export = _write_export(configured, tmp_path / "exports", inbox=("11", "99"))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert [w["code"] for w in _others(envelope)] == ["track-row-absent"]
