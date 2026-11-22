"""The routing and rebuild workers and the export medium, driven through the command line (U53).

Each test reads the DATABASE back rather than the envelope, since the engine
suites once passed while nothing in ``src`` called the engine. D1: no name here
is a real volume, person or track.
"""

from __future__ import annotations

import dataclasses
import difflib
import io
import json
import re
import shutil
import sqlite3
import tomllib
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

import cratekit
from cratekit import cli
from cratekit.cli import converge, doctor, output, registry
from cratekit.cli import rebuild as rebuild_verb
from cratekit.core import (
    active_taxonomy,
    config,
    jobs,
    locations,
    preflight,
    profiles,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import genre_favorites, metadata_cli, rebuild, routing_cli, routing_pass, trees
from tests._readings import serve_readings
from tests.test_active_taxonomy import shipped_without, write_active
from tests.test_config import valid_data
from tests.test_rb_writer_db import (
    RECORDED_APP_VERSION,
    _build_disposable_database,
    _encrypt_in_place,
)
from tests.xml_fixtures import _xml_doc

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"

#: One file under the music directory and one in the intake folder, so the two
#: derivations read disjoint sets.
SHELVED = "First Track.flac"
ARRIVED = "Second Track.flac"


def _exited(result: tuple[int, dict], expected: ExitCode = ExitCode.OK) -> dict:
    """The envelope of a drive that exited ``expected``, OK unless told otherwise."""
    code, envelope = result
    assert code == int(expected), envelope
    return envelope


def _fails(result: tuple[int, dict]) -> dict:
    """The envelope of a drive that did not exit OK."""
    code, envelope = result
    assert code != int(ExitCode.OK), envelope
    return envelope


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
    """A set-up machine whose configuration is on DISK, not monkeypatched in."""
    cfg = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """Everything about THIS machine a temporary library cannot speak for."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
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
    """Give the disposable database's rows the paths this run decided on."""
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
    """One file under the music directory and one in the intake folder."""
    (Path(configured.library.root) / "Music" / SHELVED).write_bytes(b"")
    intake = _intake_dir(configured)
    intake.mkdir(parents=True, exist_ok=True)
    (intake / ARRIVED).write_bytes(b"")
    return configured


#: The disposable database with the adopted root folder already made, by the
#: base file it was made from, so the open that makes it runs once a process.
_ADOPTED: dict[bytes, tuple[bytes, str]] = {}


def _adopted_database(path: Path, cfg: config.Config) -> str:
    """Build the disposable database with the tree's root folder, and say its identifier.

    Made through the guarded writer once per process for each base file, then
    copied, as the base itself is (U256). A build that leaves a sidecar beside
    the file is not copied."""
    _build_disposable_database(path)
    base = path.read_bytes()
    if base in _ADOPTED:
        adopted, root_id = _ADOPTED[base]
        path.write_bytes(adopted)
        return root_id
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        folder = rb_writer.ensure_folder(handle, TREE_DISPLAY)
        handle.session.commit()
        root_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    if not any(Path(f"{path}{suffix}").exists() for suffix in ("-wal", "-shm", "-journal")):
        _ADOPTED[base] = (path.read_bytes(), root_id)
    return root_id


@pytest.fixture
def native(stocked) -> str:
    """A database with a real adopted root, and a registry that has cut over.

    The root is a REAL row, since every walk goes down from its identifier."""
    path = Path(stocked.library.db_path)
    root_id = _adopted_database(path, stocked)
    _record_locations(
        path,
        {
            "1": str(Path(stocked.library.root) / "Music" / SHELVED),
            "2": str(_intake_dir(stocked) / ARRIVED),
        },
    )
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


def _drive_once(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    assert out.getvalue().strip(), f"the verb printed nothing: {err.getvalue()}"
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


#: The resort's plan gate (U219), answered by R34's separate recorded act, never inline.
RESORT_GATE = "route.resort.apply"


def _drive(argv: list[str]) -> tuple[int, dict]:
    """Drive one invocation; a resort's plan gate is approved the way a person does (U219, R34)."""
    code, document = _drive_once(argv)
    if (
        code == int(ExitCode.DECISION_REQUIRED)
        and document["cause"]["detail"].get("gate") == RESORT_GATE
        and "--run" not in argv
    ):
        run_id = document["run_id"]
        decided, envelope = _drive_once(
            ["run", "decide", run_id, RESORT_GATE, "apply", "--actor", "a-person"]
        )
        assert decided == int(ExitCode.OK), envelope
        code, document = _drive_once(["--run", run_id, *argv])
    return code, document


def _approved_adds() -> list[dict[str, str]]:
    """The adds a resort's gate would show for the governed tree, for a hand built job (U219)."""
    cfg = config.load()
    reports, _ = rebuild.preview_governed_trees(cfg, tree_ids=(TREE_ID,), vocal_threshold=None)
    return [row for report in reports for row in rebuild.additions(report)]


def _enqueue_resort(*item_ids: str) -> jobs.Job:
    """A resort queued by hand over ``item_ids``, frozen with the adds its gate would show."""
    with jobs.open_store() as store:
        return jobs.enqueue(
            store,
            handler_key="route.resort",
            payload={routing_cli.RESORT_ADDS_KEY: _approved_adds()},
            cfg=config.load(),
            item_ids=item_ids,
        )


def _fail_other_trees(monkeypatch, failure=lambda: RuntimeError("this tree is not there")):
    """Every tree but the governed one fails its rebuild with ``failure()``."""
    real = rebuild.rebuild_governed_tree

    def one_of_two(cfg, *, tree_id, workflow, **rest):
        if tree_id != TREE_ID:
            raise failure()
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", one_of_two)


def _apply_inbox() -> tuple[int, dict]:
    return _drive(["-d", "route.inbox.apply=apply", "route", "inbox"])


def _decline_inbox() -> tuple[int, dict]:
    return _drive(["-d", "route.inbox.apply=abort", "route", "inbox"])


def _queue_and_resume(argv=("rebuild", "--actor", "a-person")) -> tuple[str, int, dict]:
    """Queue ``argv``, then resume its job; say the job and the resume's answer."""
    job_id = _drive([*argv])[1]["data"]["job_id"]
    return (job_id, *_drive([*argv, "--job", job_id]))


def _items(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def _queued_jobs() -> tuple[jobs.Job, ...]:
    with jobs.open_store() as store:
        return jobs.list_jobs(store)


def _membership(cfg: config.Config, root_id: str) -> set[str]:
    """Every content identifier the governed tree holds, read back from the file."""
    handle = rb_writer.open_db(Path(cfg.library.db_path), cfg=cfg)
    try:
        held: set[str] = set()
        for node in rebuild.read_tree(handle, root_id):
            held |= set(node.content_ids)
        return held
    finally:
        rb_writer.close_db(handle)


#: The native library plain and encrypted, as a real one is (R-239); a test takes it by ``request``.
MEDIA = pytest.mark.parametrize("medium", ["native", "encrypted"])

#: The two queued verbs, which share the engine and not the shell.
QUEUED_VERBS = pytest.mark.parametrize(
    "argv", [["rebuild", "--actor", "a-person"], ["route", "resort"]], ids=["rebuild", "resort"]
)


@MEDIA
@QUEUED_VERBS
def test_a_queued_job_runs_its_item_and_the_tree_holds_the_track(
    acknowledged, argv, medium, request
):
    """Pending to done, and then the DATABASE is asked what happened (R-239: encrypted too)."""
    native = request.getfixturevalue(medium)
    queued = _exited(_drive(argv))
    job_id = queued["data"]["job_id"]
    assert [item.item_id for item in _items(job_id)] == [TREE_ID]
    assert all(item.state == jobs.ItemState.PENDING for item in _items(job_id))

    _exited(_drive([*argv, "--job", job_id]))
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1"}


def test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed(monkeypatch):
    """Two properties of the two workers, taken where they can be seen alone."""
    seen: list[tuple[str, str]] = []
    cuts: list[tuple[object, object]] = []
    frozen = object()
    measured = object()
    after = SimpleNamespace(missing=())
    staged: list[tuple] = []
    approvals: list[object] = []

    def left_behind(report, declared):
        assert report is after
        del declared
        return (measured,)

    def produced(*handed):
        staged.append(handed)
        return "staged"

    def spy(cfg, *, tree_id, workflow, vocal_threshold, **rest):
        # No default on ``workflow`` or ``vocal_threshold``: a spy that supplied
        # one would answer for a worker that named nothing.
        del cfg
        approvals.append(rest.get("approved"))
        seen.append((tree_id, workflow))
        cuts.append(vocal_threshold)
        return SimpleNamespace(after=after)

    def loader(cfg):
        # U89: the cut is the loader's answer over the worker's own configuration.
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
    monkeypatch.setattr(routing_cli.jobs.Artifacts, "produced", produced)
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    assert rebuild_verb.handle(object(), item, frozen) is None
    # What the engine measured becomes the resort item's staged report (R-312);
    # the resort hands the engine only its own tree's approved adds, the rebuild none (U219).
    mine = {"tree": TREE_ID, "folder": "f", "playlist": "p", "path": "a.flac"}
    other = {"tree": "another_tree", "folder": "f", "playlist": "p", "path": "b.flac"}
    driven = SimpleNamespace(job_id="j", payload={routing_cli.RESORT_ADDS_KEY: [mine, other]})
    assert routing_cli.handle_resort(driven, item, frozen) == "staged"
    assert approvals == [None, [mine]]
    assert staged == [
        (routing_cli.RESORT_ARTIFACTS, frozen, driven, item,
         {"tree_id": TREE_ID, "left_behind": [{"kept": measured}], "due_again": 0})
    ]

    assert cuts == [7.5, 7.5]
    assert [tree for tree, _ in seen] == [TREE_ID, TREE_ID]
    workflows = [workflow for _, workflow in seen]
    assert workflows == [rebuild.REBUILD_WORKFLOW, routing_cli.RESORT_WORKFLOW]
    assert len(set(workflows)) == 2, workflows
    assert routing_cli.INBOX_WORKFLOW not in workflows


@QUEUED_VERBS
def test_neither_queued_verb_files_a_job_with_no_items(acknowledged, native, argv):
    """A job with nothing to claim is walked once and reported as succeeded."""
    del acknowledged, native
    _exited(_drive(argv))
    filed = _queued_jobs()
    assert filed, "the verb reported OK and filed nothing at all"
    for job in filed:
        assert _items(job.job_id), f"{job.handler_key} filed a job with no items"


@QUEUED_VERBS
def test_neither_queued_verb_files_a_job_at_all_with_no_native_tree(configured, argv):
    """With no native tree there is nothing to queue, and it is not a refusal."""
    del configured
    envelope = _exited(_drive(argv))
    assert envelope["outcome"] == str(Outcome.NO_OP), envelope
    assert envelope["data"]["job_id"] == ""
    assert envelope["data"]["state"] == "no-native-tree"
    assert _queued_jobs() == ()


@MEDIA
def test_the_confirmed_inbox_applies_and_the_declined_one_does_not(acknowledged, medium, request):
    """The defect in one test: the two answers used to produce the same result."""
    native = request.getfixturevalue(medium)
    declined = _exited(_decline_inbox())
    assert declined["outcome"] == str(Outcome.NO_OP)
    assert declined["data"]["totals"]["applied"] is False
    assert _membership(acknowledged, native) == set(), "the declined branch wrote membership"

    applied = _exited(_apply_inbox())
    assert applied["outcome"] == str(Outcome.OK)
    assert applied["data"]["totals"]["applied"] is True
    assert applied["data"]["totals"]["added"] == 1
    assert _membership(acknowledged, native) == {"2"}, "the confirmed branch wrote nothing"
    assert declined["data"]["totals"] != applied["data"]["totals"], "the answers read the same"
    # A digest that moved over one unchanged folder would refuse the recorded decision as stale.
    assert declined["data"]["digest"] == applied["data"]["digest"]


def test_a_confirmed_inbox_over_an_empty_folder_opens_nothing(acknowledged, native):
    for path in _intake_dir(acknowledged).iterdir():
        path.unlink()
    before = len(session.records(acknowledged))

    envelope = _exited(_apply_inbox())
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "inbox-empty"
    assert len(session.records(acknowledged)) == before
    assert _membership(acknowledged, native) == set()


def test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so(stocked):
    """Membership written for a bridge tree is overwritten at the next import, so
    the apply says there is nowhere to put it rather than an empty success."""
    envelope = _exited(_apply_inbox())
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"
    assert envelope["data"]["totals"]["applied"] is False
    assert envelope["data"]["totals"]["skipped_files"] == []
    assert not Path(stocked.library.db_path).exists(), (
        "the apply opened a database on a library that has flipped no tree"
    )


#: A file dropped into the intake folder and never imported (R-318).
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
    """R-318: twenty unimported files once read as ``skipped: 20`` and no name."""
    (_intake_dir(acknowledged) / UNIMPORTED).write_bytes(b"")

    applied = _exited(_apply_inbox())
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
    """``WITHDRAWN`` against ``NOT_IMPORTED`` is the pair the vocabulary exists for."""
    _set_row(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", "2")

    applied = _exited(_apply_inbox())
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

    applied = _exited(_apply_inbox())
    (entry,) = applied["data"]["totals"]["skipped_files"]
    assert entry["reason"] == str(routing_pass.Placement.AMBIGUOUS)
    assert sorted(entry["content_ids"]) == ["1", "2"]
    (message,) = _skipped_warnings(applied)
    assert ARRIVED in message


def test_a_clean_apply_names_no_skipped_file(acknowledged, native):
    """So a warning emitted on every run cannot pass the tests above."""
    applied = _exited(_apply_inbox())
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
    """A reason with no sentence would reach a person as a bare token."""
    owed = set(routing_pass.Placement) - routing_pass.WRITABLE - {routing_pass.Placement.UNDECLARED}
    assert set(routing_cli.SKIP_NEXT_ACT) == owed
    sentences = list(routing_cli.SKIP_NEXT_ACT.values())
    assert len(set(sentences)) == len(sentences), "two reasons share one next act"


def test_the_skip_warning_counts_every_file_and_caps_the_names():
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
    """An additive sub-class puts one file in two playlists of a tree, skipped once per playlist."""
    cfg = SimpleNamespace(library=SimpleNamespace(root="/library"), resolved_prefix_map=lambda: ())
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


@MEDIA
def test_unplaced_reports_the_rows_no_governed_tree_holds(acknowledged, medium, request):
    """Two rows, neither filed, and the report has to name both."""
    request.getfixturevalue(medium)
    envelope = _exited(_drive(["route", "unplaced"]))
    assert envelope["data"]["totals"]["compared"] is True
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1", "2"}
    assert envelope["data"]["totals"]["count"] == 2
    assert envelope["data"]["totals"]["collection"] == 2
    paths = {item["path"] for item in envelope["data"]["items"]}
    assert str(Path(acknowledged.library.root) / "Music" / SHELVED) in paths


def test_unplaced_over_a_fully_placed_library_reports_none(acknowledged, native):
    """The other direction, so the report cannot be a constant."""
    del acknowledged
    _queue_and_resume()
    _apply_inbox()
    assert _membership(config.load(), native) == {"1", "2"}

    envelope = _exited(_drive(["route", "unplaced"]))
    assert envelope["data"]["totals"]["compared"] is True
    assert envelope["data"]["items"] == []
    assert envelope["data"]["totals"]["collection"] == 2


def test_unplaced_says_when_it_could_not_compare(configured):
    """An empty answer over a library nothing read is kept apart from an empty library."""
    del configured
    envelope = _exited(_drive(["route", "unplaced"]))
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["items"] == []
    assert envelope["data"]["totals"]["compared"] is False
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"


def test_unplaced_does_not_report_a_row_rekordbox_removed(acknowledged, native):
    """A tombstone is not a track waiting to be filed."""
    del native
    _set_row(acknowledged, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", "2")

    envelope = _exited(_drive(["route", "unplaced"]))
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1"}
    assert envelope["data"]["totals"]["collection"] == 1


def test_unplaced_declares_no_write_and_needs_only_what_a_read_needs():
    """The declaration is what doctor and conformance read, so it is the surface (R-313, U91)."""
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
    """Doctor's per verb requirement, derived from this entry and nothing else."""
    monkeypatch.setattr(registry, "entries", lambda: (registry.entry("route.unplaced"),))
    membership = profiles.resolve("full")
    assert doctor.requires_check("library.mounted", membership)
    assert doctor.requires_check("rekordbox.pins", membership)
    assert not doctor.requires_check("rekordbox.closed", membership)


def test_unplaced_reports_with_rekordbox_open_and_writes_nothing(configured, native, monkeypatch):
    """R-313: a report that is safe with rekordbox open."""
    del native
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    database = Path(configured.library.db_path)
    before = database.read_bytes()

    envelope = _exited(_drive(["route", "unplaced"]))
    assert envelope["data"]["totals"]["compared"] is True
    assert {item["content_id"] for item in envelope["data"]["items"]} == {"1", "2"}
    assert database.read_bytes() == before, "a report changed the database it read"
    assert not session.lock_path(configured).exists(), "a report took the session lock"


def test_unplaced_still_refuses_on_a_drifted_binding_so_doctor_keeps_the_pins(
    configured, native, monkeypatch
):
    """Why ``rekordbox.pins`` stays declared when ``rekordbox.closed`` goes."""
    del native
    import pyrekordbox

    monkeypatch.setattr(pyrekordbox, "__version__", "0.0.0-drifted")
    envelope = _exited(_drive(["route", "unplaced"]), ExitCode.VERSION_PIN)
    assert envelope["cause"]["reason"] == "pyrekordbox-pin-drift", envelope
    assert "rekordbox.pins" in registry.entry("route.unplaced").doctor_checks


def test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates(
    configured, native, monkeypatch
):
    """KTD24, reached from the queue rather than from a direct engine call."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: configured.library.volume_id),
    )
    job_id, code, envelope = _queue_and_resume()
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None
    assert str(item.cause.remediation.remedy) == "acknowledge-backup", item.cause.to_json()
    assert _membership(configured, native) == set()


def test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item(acknowledged, native):
    """The engine refuses rather than deriving nothing, and the worker carries it."""
    for path in (Path(acknowledged.library.root) / "Music").iterdir():
        path.unlink()
    (Path(acknowledged.library.root) / "Music").rmdir()
    job_id, code, envelope = _queue_and_resume()
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "rebuild-derivation-empty"
    assert _membership(acknowledged, native) == set()


def test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item(acknowledged, native):
    """A registry pointing at a root this library does not have."""
    del native
    record = tree_registry.read(acknowledged).record(TREE_ID)
    moved = dataclasses.replace(record, root_id="root-row-0000")
    tree_registry.write(acknowledged, tree_registry.Registry((moved,)))
    job_id, code, envelope = _queue_and_resume()
    assert code != int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None, item


@pytest.fixture
def planted_grid(configured) -> Path:
    """One analysis file where rekordbox actually keeps them (R-14)."""
    share = Path(configured.library.db_path).parent / "share"
    grid = share / "PIONEER" / "USBANLZ" / "8d2" / "one" / "ANLZ0000.DAT"
    grid.parent.mkdir(parents=True)
    grid.write_bytes(b"PMAI")
    return grid


def _watched_roots(monkeypatch) -> list[list[str]]:
    """Capture the roots each write arms its analysis watch over, without disarming it."""
    seen: list[list[str]] = []
    real = session.assert_gates

    def wrapper(cfg, *, analysis_roots=(), **rest):
        seen.append([str(root) for root in analysis_roots])
        return real(cfg, analysis_roots=analysis_roots, **rest)

    monkeypatch.setattr(session, "assert_gates", wrapper)
    return seen


@pytest.mark.parametrize(
    "drive", [lambda: _queue_and_resume()[1:], lambda: _apply_inbox()], ids=["rebuild", "inbox"]
)
def test_each_write_watches_the_grids_where_they_actually_live(
    acknowledged, native, planted_grid, monkeypatch, drive
):
    """R17's fifth surface, runtime half, measured at each call site rather than asserted."""
    del native, acknowledged
    seen = _watched_roots(monkeypatch)
    _exited(drive())
    assert seen, "the write opened no session at all, so there is nothing to measure"
    for roots in seen:
        assert planted_grid in session.analysis_files_under(roots), (
            f"the session watched {roots}, which holds no analysis file"
        )


@QUEUED_VERBS
def test_neither_resume_drives_another_verbs_job(acknowledged, native, argv):
    """``handlers.run_job`` reads the worker off the JOB ROW, not off this verb."""
    del acknowledged, native
    with jobs.open_store() as store:
        foreign = jobs.enqueue(
            store, handler_key="master", payload={}, cfg=config.load(), item_ids=("one",)
        )

    envelope = _fails(_drive([*argv, "--job", foreign.job_id]))
    assert envelope["cause"]["reason"] == "job-unknown", envelope
    assert [item.state for item in _items(foreign.job_id)] == [jobs.ItemState.PENDING]


#: Each queued verb with the handler key its jobs are filed under.
QUEUED_KEYS = pytest.mark.parametrize(
    "argv, key",
    [(["rebuild", "--actor", "a-person"], "rebuild"), (["route", "resort"], "route.resort")],
    ids=["rebuild", "resort"],
)


@QUEUED_KEYS
def test_neither_resume_drives_a_job_an_older_build_queued_with_no_items(
    acknowledged, native, argv, key
):
    """The zero item rule on the resume side, which is the door that predates the fix (U53)."""
    del acknowledged, native
    with jobs.open_store() as store:
        stale = jobs.enqueue(store, handler_key=key, payload={}, cfg=config.load())

    _fails(_drive([*argv, "--job", stale.job_id]))
    with jobs.open_store() as store:
        assert jobs.get(store, stale.job_id).state != jobs.JobState.SUCCEEDED


@QUEUED_KEYS
def test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit(
    acknowledged, native, argv, key, monkeypatch
):
    """R-225, which named this inheritance in advance."""
    del acknowledged
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=key,
            # The resort's worker writes only what its gate approved (U219).
            payload={"tree": None, "actor": "a-person", "adds": _approved_adds()},
            cfg=config.load(),
            item_ids=(TREE_ID, "second_tree"),
        )

    _fail_other_trees(monkeypatch)

    _fails(_drive([*argv, "--job", job.job_id]))
    states = {item.item_id: item.state for item in _items(job.job_id)}
    assert states[TREE_ID] == jobs.ItemState.DONE
    assert states["second_tree"] == jobs.ItemState.FAILED
    assert _membership(config.load(), native) == {"1"}, "a partial failure rolled back a success"


def test_a_resume_reads_no_registry_of_its_own(acknowledged, native):
    """Everything a queued job needs was frozen when it was queued."""
    del native
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    tree_registry.path_for(acknowledged).write_text("{ this is not a registry")

    _fails(_drive(["rebuild", "--actor", "a-person", "--job", job_id]))
    assert _items(job_id)[0].state == jobs.ItemState.FAILED, (
        "the unreadable registry blocked a job whose items were already frozen"
    )


def _vocal_warnings(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.VOCAL_NOT_COMPARED]


@pytest.fixture
def no_vocal_dimension(monkeypatch):
    """The shipped taxonomy with its additive sub-playlists taken out, through the one loader."""
    shipped = taxonomy.default_taxonomy()
    assert any(entry.additive for entry in shipped.sub_classes), "no additive sub-playlist left"
    narrowed = dataclasses.replace(
        shipped,
        sub_classes=tuple(entry for entry in shipped.sub_classes if not entry.additive),
    )
    monkeypatch.setattr(active_taxonomy, "load", lambda cfg: narrowed)


def test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared(
    acknowledged, native
):
    code, applied = _apply_inbox()
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["applied"] is True
    assert _membership(acknowledged, native) == {"2"}
    warned = _vocal_warnings(applied)
    assert len(warned) == 1, applied["warnings"]
    assert set(warned[0]) == {"code", "message"}
    assert "vocal" in warned[0]["message"]
    assert "not_compared" not in applied["data"]["totals"], "the gap leaked into the plan totals"


def test_a_declined_inbox_carries_no_vocal_warning(acknowledged, native):
    """Nothing was derived on the declined branch, so nothing went uncompared."""
    del acknowledged, native
    declined = _exited(_decline_inbox())
    assert _vocal_warnings(declined) == []


@QUEUED_VERBS
def test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift(
    acknowledged, native, argv
):
    """The rebuild's envelope carries the gap alongside the drift warning."""
    queued = _exited(_drive(argv))
    assert _vocal_warnings(queued) == [], "the queue-only answer claimed a comparison"
    job_id = queued["data"]["job_id"]

    moved = config.from_dict(
        valid_data(
            Path(acknowledged.library.root),
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
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


def _favorites_warnings(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == genre_favorites.CLASS_UNDECLARED]


@pytest.fixture
def no_favorites_class(monkeypatch):
    """This library's declaration without its playlist class, as the live library's copy was."""
    real = active_taxonomy.load

    def narrowed(cfg):
        declared = real(cfg)
        kept = tuple(e for e in declared.sub_classes if e.signal != taxonomy.SIGNAL_PLAYLIST)
        assert len(kept) == len(declared.sub_classes) - 1, "no playlist class to take out"
        tree = dataclasses.replace(declared.tree, id=TREE_ID)
        return dataclasses.replace(declared, sub_classes=kept, tree=tree)

    monkeypatch.setattr(active_taxonomy, "load", narrowed)


@QUEUED_VERBS
def test_a_driven_resume_over_no_favorites_class_names_the_skipped_step(
    acknowledged, native, no_favorites_class, argv
):
    del acknowledged, native, no_favorites_class
    queued = _exited(_drive(argv))
    assert _favorites_warnings(queued) == [], "the queue-only answer skipped nothing yet"
    job_id = queued["data"]["job_id"]
    code, done = _drive([*argv, "--job", job_id])
    assert code == int(ExitCode.OK), done
    (warned,) = _favorites_warnings(done)
    assert set(warned) == {"code", "message"}
    assert "genre Favorites step was skipped" in warned["message"]
    assert "schema_version 5" in warned["message"]
    assert "crate taxonomy upgrade" in warned["message"]
    again = _exited(_drive([*argv, "--job", job_id]))
    assert _favorites_warnings(again) == [], "a job finished on entry skipped nothing in this run"


@QUEUED_VERBS
def test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites(
    acknowledged, native, monkeypatch, argv
):
    """The class is declared under the routing tree alone, so a job over another tree skipped nothing."""
    del acknowledged, native
    real = active_taxonomy.load

    def narrowed(cfg):
        declared = real(cfg)
        assert declared.tree.id != TREE_ID
        kept = tuple(e for e in declared.sub_classes if e.signal != taxonomy.SIGNAL_PLAYLIST)
        return dataclasses.replace(declared, sub_classes=kept)

    monkeypatch.setattr(active_taxonomy, "load", narrowed)
    _, code, done = _queue_and_resume(argv)
    assert code == int(ExitCode.OK), done
    assert _favorites_warnings(done) == []


@QUEUED_VERBS
def test_a_driven_resume_over_the_declared_class_says_nothing_of_it(
    acknowledged, native, monkeypatch, argv
):
    del acknowledged, native
    real = active_taxonomy.load
    monkeypatch.setattr(
        active_taxonomy,
        "load",
        lambda cfg: dataclasses.replace(
            real(cfg), tree=dataclasses.replace(real(cfg).tree, id=TREE_ID)
        ),
    )
    _, code, done = _queue_and_resume(argv)
    assert code == int(ExitCode.OK), done
    assert _favorites_warnings(done) == []


@QUEUED_VERBS
def test_a_resume_that_drove_nothing_carries_no_vocal_warning(acknowledged, native, argv):
    """A job already finished on entry was compared by an earlier run, not this one."""
    del acknowledged, native
    job_id, code, first = _queue_and_resume(argv)
    assert code == int(ExitCode.OK), first
    assert len(_vocal_warnings(first)) == 1, first["warnings"]
    again = _exited(_drive([*argv, "--job", job_id]))
    assert _vocal_warnings(again) == []


def test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface(
    acknowledged, native, no_vocal_dimension
):
    del no_vocal_dimension
    code, applied = _apply_inbox()
    assert code == int(ExitCode.OK), applied
    assert applied["data"]["totals"]["applied"] is True
    assert _vocal_warnings(applied) == [], applied["warnings"]

    job_id, code, done = _queue_and_resume()
    assert code == int(ExitCode.OK), done
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _membership(acknowledged, native) == {"1", "2"}
    assert _vocal_warnings(done) == [], done["warnings"]


def test_the_rebuild_worker_still_returns_none(acknowledged, native):
    """``handle`` produces no artifact (R-316)."""
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    assert rebuild_verb.handle(object(), item, acknowledged) is None
    assert _membership(acknowledged, native) == {"1"}


def test_the_gap_rule_is_the_derivations_own():
    """``governed_not_compared`` and the derivation answer from one rule."""
    shipped = taxonomy.default_taxonomy()
    truth = [rebuild.Truth(location="/x/a.flac", genre=None, energy=None, voxlevel=None)]
    _placements, gaps = rebuild.derive_from_taxonomy(shipped, truth, vocal_threshold=None)
    assert gaps == (rebuild.VOCAL_DIMENSION,)
    assert rebuild.governed_not_compared(None, shipped) == gaps
    assert rebuild.derive_from_taxonomy(shipped, truth, vocal_threshold=0.5)[1] == ()
    assert rebuild.governed_not_compared(0.5, shipped) == ()


def test_the_warning_code_is_the_locked_spelling():
    """Every other assertion reads the constant, so this is the one that pins it."""
    assert rebuild.VOCAL_NOT_COMPARED == "vocal-dimension-not-compared"
    (warning,) = rebuild.not_compared_warnings((rebuild.VOCAL_DIMENSION,))
    assert warning["code"] == "vocal-dimension-not-compared"
    assert rebuild.not_compared_warnings(()) == ()


#: The resort's command line.
RESORT = ("route", "resort")


def _left_behind(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == rebuild.LEFT_BEHIND]


@pytest.fixture
def leftover(acknowledged, native) -> str:
    """A governed playlist holding a track the declaration does not place there."""
    _exited(_apply_inbox())
    assert _membership(acknowledged, native) == {"2"}
    return "2"


def test_a_resort_names_the_membership_it_left_where_it_was(acknowledged, native, leftover):
    """R-312: the resort is additive and says what it left where it was."""
    _, code, done = _queue_and_resume(RESORT)
    assert code == int(ExitCode.OK), done
    assert _membership(acknowledged, native) == {"1", leftover}, "the resort removed a membership"
    (warning,) = _left_behind(done)
    assert "Electronica / Other/Unsorted" in warning["message"], warning
    assert ARRIVED in warning["message"], warning
    assert SHELVED not in warning["message"], "a track the declaration places was named"
    assert "1 membership" in warning["message"], warning
    assert "adds and never removes" in warning["message"], warning


def test_a_resort_that_left_nothing_behind_says_nothing_about_it(acknowledged, native):
    """A converged tree carries no leftover warning, so the warning means something."""
    _, code, done = _queue_and_resume(RESORT)
    assert code == int(ExitCode.OK), done
    assert _membership(acknowledged, native) == {"1"}
    assert _left_behind(done) == []


def test_a_resort_resume_that_drove_nothing_names_no_leftover(acknowledged, native, leftover):
    """A job finished on entry was measured by the run that drove it, not this one."""
    del acknowledged, native, leftover
    code, queued = _drive(["route", "resort"])
    assert _left_behind(queued) == []
    job_id = queued["data"]["job_id"]
    assert len(_left_behind(_drive(["route", "resort", "--job", job_id])[1])) == 1
    again = _exited(_drive(["route", "resort", "--job", job_id]))
    assert _left_behind(again) == []


def test_one_jobs_leftovers_are_not_counted_under_another(acknowledged, native, leftover):
    """TWO jobs over one state each name the one leftover, never the pool of both."""
    del acknowledged, native, leftover
    for turn in range(2):
        # A resort with nothing to add queues no job (U219), so the second is enqueued by hand.
        job_id = _drive([*RESORT])[1]["data"]["job_id"] if turn == 0 else _enqueue_resort(TREE_ID).job_id
        (warning,) = _left_behind(_drive(["route", "resort", "--job", job_id])[1])
        assert "1 membership" in warning["message"], warning
        assert job_id in warning["message"], "the warning does not say where this job's list is"


def test_the_whole_list_is_written_where_the_warning_says_it_is(acknowledged, native, leftover):
    """The names in a warning are capped, so the place it points at has to be real."""
    del acknowledged, native
    (warning,) = _left_behind(_queue_and_resume(RESORT)[2])
    listed_in = Path(warning["message"].rsplit("listed in ", 1)[1])
    (report,) = sorted(listed_in.glob("*.json"))
    written = json.loads(report.read_text(encoding="utf-8"))
    assert written["tree_id"] == TREE_ID
    assert [entry["content_id"] for entry in written["left_behind"]] == [leftover]
    assert written["left_behind"][0]["location"].endswith(ARRIVED)


@pytest.mark.parametrize("left", [True, False], ids=["left-behind", "converged"])
def test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left(
    acknowledged, native, monkeypatch, request, left
):
    """The exit a resort over several trees usually takes; a converged tree adds no step."""
    del acknowledged, native
    if left:
        request.getfixturevalue("leftover")
    job = _enqueue_resort(TREE_ID, "second_tree")
    _fail_other_trees(monkeypatch)
    refused = _fails(_drive([*RESORT, "--job", job.job_id]))
    with jobs.open_store() as store:
        stored = jobs.get(store, job.job_id).cause
    steps = list(refused["cause"]["remediation"]["steps"])
    if not left:
        assert steps == list(stored.remediation.steps)
        return
    assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps)
    (added,) = steps[len(stored.remediation.steps) :]
    assert ARRIVED in added and "1 membership" in added, added
    assert tuple(refused["cause"]["origin"])[: len(stored.origin)] == stored.origin
    assert refused["cause"]["reason"] == stored.reason


def _not_there_yet() -> Exception:
    """A tree rebuild that fails and will not fail the next time, recorded as such (R-390)."""
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
    """The driver that died is the run an in memory note loses."""
    del acknowledged, native, leftover
    job = _enqueue_resort(TREE_ID, "second_tree")
    real = rebuild.rebuild_governed_tree
    calls: list[str] = []

    def second_tree_fails_once(cfg, *, tree_id, workflow, **rest):
        calls.append(tree_id)
        if tree_id != TREE_ID:
            if calls.count(tree_id) == 1:
                # Retryable (R-390): a bare RuntimeError would record a permanent failure.
                raise _not_there_yet()
            return SimpleNamespace(after=rebuild.ConvergenceReport(tree_id, "root", derived=1))
        return real(cfg, tree_id=tree_id, workflow=workflow, **rest)

    monkeypatch.setattr(rebuild, "rebuild_governed_tree", second_tree_fails_once)
    assert _drive(["route", "resort", "--job", job.job_id])[0] != int(ExitCode.OK)
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    done = _exited(_drive(["route", "resort", "--job", job.job_id]))
    assert calls == [TREE_ID, "second_tree", "second_tree"], calls
    (warning,) = _left_behind(done)
    assert ARRIVED in warning["message"], warning


def test_a_refusal_raised_before_the_drive_carries_no_leftover_step(
    acknowledged, native, leftover, monkeypatch
):
    """A run that drove nothing answers for no tree, whatever an earlier one wrote."""
    del acknowledged, native, leftover
    job = _enqueue_resort(TREE_ID, "second_tree")
    _fail_other_trees(monkeypatch, _not_there_yet)
    code, first = _drive(["route", "resort", "--job", job.job_id])
    assert ARRIVED in " ".join(first["cause"]["remediation"]["steps"]), first
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)

    def corrupt(cfg):
        del cfg
        raise refuse("config-unusable", "the calibration cannot be read")

    monkeypatch.setattr(metadata_cli, "load_vocal_threshold", corrupt)
    refused = _fails(_drive(["route", "resort", "--job", job.job_id]))
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
    # Handed over backwards, so the cap keeps the first in order, not the first to arrive.
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
    """The registry line is what help prints, and it promised a re-place."""
    summary = registry.entry("route.resort").summary
    assert "add" in summary, summary
    assert "re-place" not in summary, summary
    assert "old" in summary, summary


#: A second tree, still on the XML bridge, which no queued item may name.
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


@QUEUED_VERBS
def test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge(mixed, argv):
    """A rebuild of a bridge tree writes membership the next import overwrites."""
    del mixed
    _exited(_drive(argv))
    filed = _queued_jobs()
    assert len(filed) == 1, filed
    assert [item.item_id for item in _items(filed[0].job_id)] == [TREE_ID], (
        "a tree still on the XML bridge was queued for a database write"
    )


def test_a_rebuild_of_one_named_tree_queues_that_tree_alone(acknowledged, native):
    """The ``--tree`` flag scopes the work."""
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

    envelope = _exited(_drive(["rebuild", "--actor", "a-person", "--tree", TREE_ID]))
    assert [item.item_id for item in _items(envelope["data"]["job_id"])] == [TREE_ID]

    both = _exited(_drive(["rebuild", "--actor", "a-person"]))
    assert [item.item_id for item in _items(both["data"]["job_id"])] == [
        "second_shelf",
        TREE_ID,
    ], "the unscoped rebuild is what proves the scoped one was scoped"


def test_a_gate_answer_this_verb_does_not_recognise_writes_nothing(
    acknowledged, native, monkeypatch
):
    """The branch direction, which no drive through the shipped gate can reach."""
    del acknowledged
    monkeypatch.setattr(routing_cli, "_apply_gate", lambda ctx, plan, shown: "later")
    envelope = _exited(_drive(["route", "inbox"]))
    assert envelope["outcome"] == str(Outcome.NO_OP), envelope
    assert envelope["data"]["totals"]["applied"] is False
    assert _membership(config.load(), native) == set(), "the gate admitted by omission"


@pytest.fixture
def encrypted(acknowledged, native) -> str:
    """The native library encrypted with the binding's key, as a real one is (R-239)."""
    path = Path(acknowledged.library.db_path)
    _encrypt_in_place(path)
    assert rb_writer.unlock_needed(path)
    return native


def test_converge_compares_a_native_tree_on_an_encrypted_library(acknowledged, encrypted):
    """"Not compared" on a real library reads as "nothing to see", not "could not look"."""
    del acknowledged, encrypted
    envelope = _exited(_drive(["converge"]))
    statuses = {check["key"]: check["status"] for check in envelope["data"]["checks"]}
    assert statuses[f"tree.{TREE_ID}"] != converge.NOT_COMPARED, envelope


#: U86's three intake tracks, their tag readings, and where the declared rules put each.
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
    "24": ("Classical Track.flac", "Classical", 10, ("NonElectronic", "Classical")),
    "25": ("No Reading.flac", "Deep House", None, ("Deep House", "Unsorted")),
}

#: The folders RATING_TRACKS land in, so an unset rating is the rule's doing, not a skipped write's.
RATING_FOLDERS = (
    ("Deep House", ("Low", "Med", "High", "Unsorted")),
    ("Tech House", ("Low", "Med", "High")),
    ("NonElectronic", ("Classical",)),
)

#: The export scale's five and one star values, checked against the shipped template's raw TOML.
FIVE_STARS = "255"
ONE_STAR = "51"

#: Tokens only grid bearing XML carries, plus the tempo attribute itself.
GRID_TOKENS = ("<TEMPO", "Battito", "Metro=", "Inizio=", "AverageBpm=", "Bpm=")


def _export_track(
    tid: str,
    location: str,
    *,
    analyzed: bool = False,
    rating: str | None = None,
    seconds: str | None = None,
) -> list[str]:
    """One multi line collection row, the real export shape, optionally analysed."""
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
    return [
        f'        <NODE Type="0" Name="{name}" Count="{len(subs)}">',
        *(f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="0"/>' for sub in subs),
        "        </NODE>",
    ]


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
    """A fresh export: a collection, an INBOX batch, and the routing tree."""
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
    """The three tag readings, served from the file NAME (U250)."""
    by_name = {
        name: (genre, energy)
        for name, genre, energy, _ in (*EXPORT_TRACKS.values(), *RATING_TRACKS.values())
    }
    serve_readings(
        monkeypatch,
        genre=lambda path: by_name.get(path.name, (None, None))[0],
        energy=lambda path: by_name.get(path.name, (None, None))[1],
        vox=lambda path: None,
    )


def _hide_routing_tree(export: Path) -> str:
    """Rename the routing tree in ``export`` away, and say the display it had."""
    display = taxonomy.default_taxonomy().tree.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Other"'))
    return display


def _routed(export: Path) -> Path:
    return export.with_name(export.stem + "_routed.xml")


def _sub_keys(document: bytes, folder: str, sub: str) -> tuple[str, ...]:
    """What one sub playlist holds in a written file, read by a real XML parser."""
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


def _decline_export(export: Path) -> tuple[int, dict]:
    return _drive(["-d", "route.inbox.apply=abort", "route", "inbox", "--export", str(export)])


#: The review warning for nested membership no import can land (R-694), spelled out.
ROUTING_NOT_LANDABLE = "routing-not-landable"


def _not_landable(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope["warnings"] if w["code"] == ROUTING_NOT_LANDABLE]


def _others(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] != ROUTING_NOT_LANDABLE]


def test_an_export_inbox_lands_each_track_in_its_declared_sub(configured, tagged, tmp_path):
    """Three tracks, three subs, and the file that comes out parses."""
    export = _write_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export))
    assert envelope["outcome"] == str(Outcome.OK)
    totals = envelope["data"]["totals"]
    assert totals["applied"] is True
    assert totals["inserted"] == 3
    assert totals["created"] == []
    assert totals["output"] == str(_routed(export))

    written = _routed(export).read_bytes()
    for tid, (_name, _genre, _energy, (folder, sub)) in EXPORT_TRACKS.items():
        assert _sub_keys(written, folder, sub) == (tid,), f"{tid} is not alone in {folder}/{sub}"
    assert {
        item["track_id"]: item["destination"] for item in envelope["data"]["items"]
    } == {tid: f"{folder}/{sub}" for tid, (*_, (folder, sub)) in EXPORT_TRACKS.items()}

    # R-694: nested membership the bridge never lands (R-687) is a review and owes no import.
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
    envelope = _exited(_apply_export(export))
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

    envelope = _exited(_apply_export(first))
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["inserted"] == 0
    assert envelope["data"]["totals"]["reason"] == "nothing-to-route"
    assert envelope["pending_human_action"] is None
    assert sorted(path.name for path in first.parent.iterdir()) == before, "a no-op wrote a file"


def test_the_input_export_is_byte_identical_afterwards(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    before = export.read_bytes()
    _apply_export(export)
    assert export.read_bytes() == before, "the export was written in place"
    assert _routed(export).read_bytes() != before


def test_an_export_route_never_writes_a_tempo_bpm_or_grid(configured, tagged, tmp_path):
    """R17 over the diff: no added or removed line carries grid data."""
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
    """An unreadable file has no tags, and no tags would route it to the fallback."""
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


def test_an_export_with_no_routing_tree_is_blocked_not_already_filed(configured, tagged, tmp_path):
    """Every write skipped is not "nothing to route", the answer that proves an import landed."""
    export = _write_export(configured, tmp_path / "exports")
    display = _hide_routing_tree(export)
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
    envelope = _exited(_apply_export(export))
    assert envelope["data"]["totals"]["inserted"] == 0
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    assert not _routed(export).exists()


def test_an_export_route_on_an_unmounted_library_refuses(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    shutil.rmtree(configured.library.root)
    envelope = _fails(_apply_export(export))
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert not _routed(export).exists()


def test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map(
    configured, tagged, tmp_path
):
    """rekordbox keeps a volume name the drive stopped using; the prefix map finds the file."""
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

    envelope = _exited(_apply_export(export))
    assert envelope["data"]["totals"]["inserted"] == 3
    assert _others(envelope) == []


def test_a_native_routing_tree_refuses_before_the_plan_is_offered(configured, tagged, tmp_path):
    """Refused at the verb, so nobody approves a write the guard would stop; a decline refuses too."""
    export = _write_export(configured, tmp_path / "exports")
    _cut_over_routing_tree(configured)
    envelope = _fails(_decline_export(export))
    assert envelope["cause"]["reason"] == "tree-unconverged"


def test_the_export_writer_itself_refuses_a_routing_tree_that_has_cut_over(
    configured, tagged, tmp_path
):
    """The emitter alone, past the verb's own check, so neither layer relies on the other."""
    from cratekit.write import routing_export  # here: a capture on the base src imports this file
    export = _write_export(configured, tmp_path / "exports")
    _content, plan, *_rest = routing_export.plan_export(configured, export)
    _cut_over_routing_tree(configured)
    with pytest.raises(tree_registry.TreeModeRefused):
        routing_export.apply_export(configured, export, export.read_bytes(), plan)
    assert not _routed(export).exists()


def _cut_over_routing_tree(cfg: config.Config) -> None:
    record = tree_registry.TreeRecord(
        tree_id=taxonomy.default_taxonomy().tree.id,
        mode=tree_registry.Mode.DATABASE,
        cutover_on=date(2026, 8, 1),
        root_id="1",
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    tree_registry.write(cfg, tree_registry.Registry((record,)))


def test_a_declined_export_route_writes_nothing(configured, tagged, tmp_path):
    export = _write_export(configured, tmp_path / "exports")
    envelope = _exited(_decline_export(export))
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["applied"] is False
    assert not _routed(export).exists()


def test_an_export_without_an_intake_folder_refuses(configured, tagged, tmp_path):
    """An absent INBOX is not an empty one, and only one of them means done."""
    export = _write_export(configured, tmp_path / "exports")
    display = taxonomy.default_taxonomy().intake.display
    export.write_bytes(export.read_bytes().replace(f'Name="{display}"'.encode(), b'Name="Elsewhere"'))
    envelope = _fails(_apply_export(export))
    assert envelope["cause"]["reason"] == "intake-flow-absent"
    assert not _routed(export).exists()


def test_an_absent_export_refuses(configured, tmp_path):
    envelope = _fails(_apply_export(tmp_path / "no-such.xml"))
    assert envelope["cause"]["reason"] == "library-export-unusable"


def test_an_export_route_refuses_a_routing_tree_that_has_cut_over(configured, tagged, tmp_path):
    """A native tree is the database's; an export carrying its membership would replace it."""
    export = _write_export(configured, tmp_path / "exports")
    _cut_over_routing_tree(configured)
    envelope = _fails(_apply_export(export))
    assert envelope["cause"]["reason"] == "tree-unconverged"
    assert not _routed(export).exists()


def _remedies(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope["warnings"] if w["code"] == "no-native-tree"]


def test_without_export_a_library_with_no_native_tree_names_the_export_remedy(stocked):
    """The remedy names what the export medium delivers and no more (R-695): a
    review of the routing (R-687) and the long track root playlist an import lands."""
    envelope = _exited(_apply_inbox())
    assert envelope["data"]["totals"]["reason"] == "no-native-tree"
    assert _remedies(envelope) == [INBOX_REMEDY], envelope["warnings"]


def test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy(configured):
    """Without a declared long track playlist no import is owed for one, declined or applied (R-695)."""
    write_active(configured, shipped_without("long_tracks"))
    for option in ("abort", "apply"):
        envelope = _exited(_drive(["-d", f"route.inbox.apply={option}", "route", "inbox"]))
        assert _remedies(envelope) == [INBOX_REMEDY_REVIEW], (option, envelope["warnings"])


def test_the_remedy_names_the_long_track_playlist_the_active_copy_declares(configured):
    """The display a person gave the playlist is the one an import lands (R-685, R-695)."""
    shipped = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    line = f'display = "{LONG_PLAYLIST}"'
    assert shipped.count(line) == 1
    write_active(configured, shipped.replace(line, 'display = "Long Sets By Hand"'))
    envelope = _exited(_apply_inbox())
    assert _remedies(envelope) == [
        f"{INBOX_REMEDY_REVIEW}. It also adds long tracks to the root playlist "
        "'Long Sets By Hand', which one import can land"
    ], envelope["warnings"]


#: R-688: an import keeps the database's rating, so the sweep writes none and warns (spelled out).
RATING_NOT_LANDABLE = "rating-not-landable"


def _ratings_of(document: bytes) -> dict[str, str | None]:
    root = ET.fromstring(document)
    return {track.get("TrackID"): track.get("Rating") for track in root.find("COLLECTION")}


def _rating_export(cfg: config.Config, folder: Path, **overrides) -> Path:
    """An export of RATING_TRACKS, every one unrated but the hand rated one."""
    ratings = {tid: "0" for tid in RATING_TRACKS} | {"22": "", "23": "102"}
    options = {"tracks": RATING_TRACKS, "ratings": ratings, "folders": RATING_FOLDERS}
    return _write_export(cfg, folder, **(options | overrides))


def _owed(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope["warnings"] if w["code"] == RATING_NOT_LANDABLE]


def test_the_star_values_the_rating_tests_expect_are_the_shipped_curve():
    """The literals against the template's raw TOML, so the expectation is not the loader's."""
    template = Path(cratekit.__file__).parent / "templates" / "taxonomy.default.toml"
    cuts = tomllib.loads(template.read_text(encoding="utf-8"))["energy"]["rating"]["cuts"]
    assert str(cuts[-1]["rating"]) == FIVE_STARS and cuts[-1]["max"] == 10
    assert cuts[-2]["max"] < 10, "energy 10 is not alone in the top cut's reach"
    assert str(cuts[0]["rating"]) == ONE_STAR and cuts[0]["max"] >= 1


def test_an_owed_star_rating_is_not_written_into_the_export(configured, tagged, tmp_path):
    """R-688: every row keeps its rating and the owed ones are only counted; no import is owed (R-694)."""
    export = _rating_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export))
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
    return _write_export(cfg, folder, tracks=tracks, ratings={tid: rating}, folders=RATING_FOLDERS)


def test_a_lone_unrated_track_with_energy_is_owed_one_rating(configured, tagged, tmp_path):
    """The positive for the rules below on the same row shape, so their empty answer is the rule's."""
    export = _alone(configured, tmp_path / "exports", "21", "0")
    envelope = _exited(_apply_export(export))
    (message,) = _owed(envelope)
    assert message.startswith("1 intake row(s) are owed a star rating"), message


def test_a_hand_rated_export_track_is_not_owed_a_rating(configured, tagged, tmp_path):
    export = _alone(configured, tmp_path / "exports", "23", "102")
    _code, envelope = _apply_export(export)
    assert _owed(envelope) == [], "a rating a person set was counted as owed"
    assert _ratings_of(_routed(export).read_bytes())["23"] == "102"


@pytest.mark.parametrize(
    ("tid", "folder", "sub"),
    [("24", "NonElectronic", "Classical"), ("25", "Deep House", "Unsorted")],
    ids=["bucket-does-not-rate", "no-energy-reading"],
)
def test_a_track_the_rating_rule_skips_is_filed_and_not_owed(
    configured, tagged, tmp_path, tid, folder, sub
):
    """Filed, so the pass reached it, and not counted, so the rule held."""
    export = _alone(configured, tmp_path / "exports", tid, "0")
    _code, envelope = _apply_export(export)
    assert _sub_keys(_routed(export).read_bytes(), folder, sub) == (tid,)
    assert _owed(envelope) == [], f"track {tid} was counted as owed"


def test_a_second_run_still_owing_ratings_is_nothing_to_route(configured, tagged, tmp_path):
    """Ratings no run can land write no file and do not block the answer the import check reads."""
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


def test_the_offered_plan_names_no_rating_and_says_which_are_owed(configured, tagged, tmp_path):
    """The owed count is on the gate before the answer, and no item offers a rating."""
    export = _rating_export(configured, tmp_path / "exports")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    assert all("rating" not in item for item in shown["items"])
    assert "rated" not in shown
    (warning,) = shown["warnings"]
    assert warning.startswith("2 intake row(s) are owed a star rating"), warning
    assert not _routed(export).exists()


def test_a_declined_run_still_says_which_ratings_are_owed(configured, tagged, tmp_path):
    """The abort answer is how a person reads a plan, so it carries the owed count too."""
    export = _rating_export(configured, tmp_path / "exports")
    envelope = _exited(_decline_export(export))
    (message,) = _owed(envelope)
    assert message.startswith("2 intake row(s) are owed a star rating"), message
    assert not _routed(export).exists()


def test_a_row_with_no_rating_attribute_is_not_counted_as_owed(configured, tagged, tmp_path):
    """No ``Rating`` attribute is not "nobody rated this", so no warning."""
    export = _write_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export))
    assert _owed(envelope) == []


def test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated(
    configured, tagged, tmp_path
):
    """An owed rating is not a change of its own, so skipped writes answer route-blocked."""
    export = _rating_export(configured, tmp_path / "exports")
    _hide_routing_tree(export)
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["applied"]) == (0, False)
    assert totals["reason"] == "route-blocked"
    codes = [w["code"] for w in envelope["warnings"]]
    assert "route-write-skipped" in codes and RATING_NOT_LANDABLE in codes
    assert not _routed(export).exists()


def test_an_analysed_track_keeps_its_rating_and_its_grid(configured, tagged, tmp_path):
    """R17: track 21 is analysed and owed a rating, so its grid and rating stay unchanged."""
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
    """One file under two ids is read once, and each row filed is owed a rating, unwritten."""
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


#: U88's long track playlist and bounds, checked against the shipped template's TOML.
LONG_PLAYLIST = "Sets and Long Tracks"
TWENTY_FIVE_MINUTES = "1500"
NINETEEN_MINUTES = "1140"


def _root_child(document: bytes, name: str):
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
    """EXPORT_TRACKS at 25, 19 and 5 minutes, plus a one hour set outside the intake."""
    lengths = {"11": TWENTY_FIVE_MINUTES, "12": NINETEEN_MINUTES, "13": "300", "31": "3600"}
    options = {"lengths": lengths, "extra_rows": ("31",)}
    return _write_export(cfg, folder, **(options | overrides))


def test_the_long_track_values_the_tests_expect_are_the_shipped_declaration():
    template = Path(cratekit.__file__).parent / "templates" / "taxonomy.default.toml"
    raw = tomllib.loads(template.read_text(encoding="utf-8"))["long_tracks"]
    assert raw["display"] == LONG_PLAYLIST
    assert raw["over_seconds"] == 1200
    declared = taxonomy.default_taxonomy().long_tracks
    assert (declared.display, declared.over_seconds) == (LONG_PLAYLIST, 1200)


def test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not(configured, tagged, tmp_path):
    export = _long_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
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

    envelope = _exited(_apply_export(first))
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_added"]) == (0, 0)
    assert totals["reason"] == "nothing-to-route"
    assert envelope["warnings"] == []
    assert all(item["long_track"] == "" for item in envelope["data"]["items"]), "a member re-added"
    assert sorted(path.name for path in first.parent.iterdir()) == listing
    assert first.read_bytes() == before


def test_a_long_track_alone_is_a_change_and_writes_a_file(configured, tagged, tmp_path):
    """One set the playlist lacks is a file to import, even with an empty intake."""
    export = _long_export(configured, tmp_path / "exports", inbox=())
    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_added"]) == (0, 2)
    assert _long_members(_routed(export).read_bytes()) == ("11", "31")
    # Nothing nested was written, so there is no review to warn about (R-694).
    assert _not_landable(envelope) == []


def test_an_export_run_owes_the_import_of_the_root_playlist_it_added_to_alone(
    configured, tagged, tmp_path
):
    """R-694: the long track playlist is the one thing the bridge lands, so it is the whole import owed."""
    export = _long_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
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


def test_the_check_run_after_the_playlist_import_owes_no_import(configured, tagged, tmp_path):
    """R-694: the playlist landed and the routing did not, so the routing is a review, not owed."""
    landed = (
        f'      <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="2">',
        '        <TRACK Key="11"/>',
        '        <TRACK Key="31"/>',
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=landed)
    envelope = _exited(_apply_export(export))
    assert envelope["outcome"] == str(Outcome.OK)
    assert envelope["pending_human_action"] is None
    totals = envelope["data"]["totals"]
    assert (totals["inserted"], totals["long_added"]) == (3, 0)
    assert totals["output"] == str(_routed(export))
    (review,) = _not_landable(envelope)
    assert review.startswith("3 membership(s) routed under the routing tree"), review


def test_no_long_track_builds_no_empty_playlist(configured, tagged, tmp_path):
    export = _long_export(configured, tmp_path / "exports", lengths={"31": "300"})
    envelope = _exited(_apply_export(export))
    assert envelope["data"]["totals"]["long_added"] == 0
    assert _long_members(_routed(export).read_bytes()) is None


def test_a_track_is_never_removed_from_the_playlist(configured, tagged, tmp_path):
    """Add only: a member with no row and one now under the bound stay, and new ones follow."""
    existing = (
        f'      <NODE Name="{LONG_PLAYLIST}" Type="1" KeyType="0" Entries="2">',
        '        <TRACK Key="77"/>',
        '        <TRACK Key="12"/>',
        "      </NODE>",
    )
    export = _long_export(configured, tmp_path / "exports", root_extra=existing)
    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
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


def test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced(configured, tagged, tmp_path):
    """A folder of that name is refused, and a run left with nothing else is blocked, not filed."""
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
    assert all(item["long_track"] == "" for item in envelope["data"]["items"]), "refused adds offered"
    written = _routed(export).read_bytes()
    node = _root_child(written, LONG_PLAYLIST)
    assert node.get("Type") == "0"
    assert [t.get("Key") for t in node.find("NODE").findall("TRACK")] == ["99"]

    again = _exited(_apply_export(_routed(export)))
    assert again["data"]["totals"]["reason"] == "route-blocked"


def test_a_missing_duration_is_counted_not_guessed(configured, tagged, tmp_path):
    """Absent, empty, zero, a word and a fraction are all unreadable lengths."""
    lengths = {"12": "", "13": "0", "31": "abc", "32": "1500.5", "33": "3600"}
    export = _long_export(
        configured, tmp_path / "exports", lengths=lengths, extra_rows=("31", "32", "33")
    )
    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
    totals = envelope["data"]["totals"]
    assert totals["duration_unreadable"] == 5
    assert totals["long_added"] == 1
    assert _long_members(_routed(export).read_bytes()) == ("33",)


def test_the_offered_plan_names_each_long_track_before_anything_is_written(
    configured, tagged, tmp_path
):
    export = _long_export(configured, tmp_path / "exports")
    envelope = _exited(_decline_export(export))
    offered = {item["track_id"]: item["long_track"] for item in envelope["data"]["items"]}
    assert offered == {"11": LONG_PLAYLIST, "12": "", "13": "", "31": LONG_PLAYLIST}
    assert not _routed(export).exists()


def test_a_template_declaring_no_long_track_playlist_builds_none(configured, tagged, tmp_path):
    """The library's active copy says so, on the volume where setup put it (R-685)."""
    assert taxonomy.default_taxonomy().long_tracks is not None
    write_active(configured, shipped_without("long_tracks"))
    export = _long_export(configured, tmp_path / "exports")
    envelope = _exited(_apply_export(export))
    assert envelope["data"]["totals"]["long_added"] == 0
    assert _long_members(_routed(export).read_bytes()) is None
    assert all(item["long_track"] == "" for item in envelope["data"]["items"])


def test_an_edit_to_the_active_copy_is_the_playlist_the_routing_plan_names(
    configured, tagged, tmp_path
):
    """The display a person gave the playlist is the one planned and written (R-685)."""
    from cratekit.write import routing_export  # here: a capture on the base src imports this file
    shipped = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    line = f'display = "{LONG_PLAYLIST}"'
    assert shipped.count(line) == 1
    write_active(configured, shipped.replace(line, 'display = "Long Sets By Hand"'))
    export = _long_export(configured, tmp_path / "exports")

    planned = routing_export.plan_export(configured, export)
    long_plan, items = planned.long_plan, planned.items
    assert long_plan.keys
    assert {item["long_track"] for item in items} - {""} == {"Long Sets By Hand"}

    envelope = _exited(_apply_export(export), ExitCode.PENDING_HUMAN)
    offered = {item["long_track"] for item in envelope["data"]["items"]} - {""}
    assert offered == {"Long Sets By Hand"}
    written = _routed(export).read_bytes()
    assert _root_child(written, "Long Sets By Hand") is not None
    assert _long_members(written) is None


def test_the_add_only_writer_counts_each_new_track_once():
    """Directly on the writer: a repeated id and an existing member add nothing."""
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


#: U89's calibrated vocal cut (R-276, R-417); the tests read 6 and 4 either side of it.
CUT = 5.0


def _calibrate(cfg: config.Config, text: str) -> Path:
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _calibrated(cfg: config.Config) -> Path:
    return _calibrate(cfg, json.dumps({"threshold": CUT, "method": "otsu"}))


def _vox_display() -> str:
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
    """Voxlevel readings served from the file NAME, set by each test."""
    levels: dict[str, int] = {}
    serve_readings(monkeypatch, vox=lambda path: levels.get(path.name))
    return levels


def test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults(tmp_path):
    """One loader, two answers over it: routing needs None, My Tags the default."""
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
    applied = _exited(_apply_inbox())
    assert _membership(acknowledged, native) == {"2"}
    assert _vox_members(acknowledged, native) == ({"2"} if filed else set())
    assert _vocal_warnings(applied) == [], "a compared dimension was warned as not compared"


def test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox(
    acknowledged, native, vox_levels
):
    vox_levels[ARRIVED] = 60
    applied = _exited(_apply_inbox())
    assert _membership(acknowledged, native) == {"2"}
    assert _vox_members(acknowledged, native) == set()
    assert len(_vocal_warnings(applied)) == 1, applied["warnings"]


def test_a_corrupt_calibration_refuses_the_inbox_and_writes_nothing(
    acknowledged, native, vox_levels
):
    _calibrate(acknowledged, '{"threshold": 5.')
    vox_levels[ARRIVED] = 6
    refused = _fails(_apply_inbox())
    assert refused["cause"]["reason"] == "vocal-calibration-unreadable", refused
    assert _membership(acknowledged, native) == set()


def test_a_second_calibrated_inbox_creates_no_second_vocal_sub(acknowledged, native, vox_levels):
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    for _ in range(2):
        _exited(_apply_inbox())
    nodes = _vox_nodes(acknowledged, native)
    assert len(nodes) == 1, [(node.folder_display, node.playlist_id) for node in nodes]
    assert nodes[0].content_ids == frozenset({"2"})


@QUEUED_VERBS
@pytest.mark.parametrize("level, filed", [(6, True), (4, False)], ids=["above", "below"])
def test_a_calibrated_resume_files_under_with_vox_and_does_not_warn(
    acknowledged, native, vox_levels, argv, level, filed
):
    if argv[0] == "route":
        # U219: a resort's adds are approved at its gate; a rebuild reads at the drive.
        _calibrated(acknowledged)
        vox_levels[SHELVED] = level
    job_id = _drive(argv)[1]["data"]["job_id"]
    _calibrated(acknowledged)
    vox_levels[SHELVED] = level
    done = _exited(_drive([*argv, "--job", job_id]))
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.DONE]
    assert _vox_members(acknowledged, native) == ({"1"} if filed else set())
    assert _vocal_warnings(done) == [], "a compared dimension was warned as not compared"


@QUEUED_VERBS
def test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs(
    acknowledged, native, vox_levels, argv
):
    job_id = _drive(argv)[1]["data"]["job_id"]
    _calibrate(acknowledged, "")
    vox_levels[SHELVED] = 6
    refused = _fails(_drive([*argv, "--job", job_id]))
    assert refused["cause"]["reason"] == "vocal-calibration-unreadable", refused
    assert [item.state for item in _items(job_id)] == [jobs.ItemState.PENDING]
    assert _membership(acknowledged, native) == set()


def test_a_worker_driven_without_the_resume_refuses_a_corrupt_calibration(
    acknowledged, native, vox_levels
):
    """The worker reads the cut itself, so ``job resume`` cannot slip past it."""
    _calibrate(acknowledged, '{"threshold": NaN}')
    vox_levels[SHELVED] = 6
    item = jobs.Item(job_id="j", item_id=TREE_ID, ordinal=0, state=jobs.ItemState.PENDING)
    with pytest.raises(CratekitError) as caught:
        rebuild_verb.handle(object(), item, acknowledged)
    assert caught.value.cause.reason == "vocal-calibration-unreadable"
    assert _membership(acknowledged, native) == set()


def test_converge_compares_the_vocal_sub_once_calibrated(acknowledged, native, vox_levels):
    vox_levels[SHELVED] = 6
    _exited(_drive(["converge"]))
    job_id = _drive(["rebuild", "--actor", "a-person"])[1]["data"]["job_id"]
    _calibrated(acknowledged)
    _drive(["rebuild", "--actor", "a-person", "--job", job_id])
    assert _vox_members(acknowledged, native) == {"1"}

    after = _exited(_drive(["converge"]))
    (check,) = [c for c in after["data"]["checks"] if c["key"] == f"tree.{TREE_ID}"]
    assert check["status"] == converge.MATCHING, check
    assert "not compared" not in check["detail"], check


def test_a_corrupt_calibration_is_converge_not_comparing_rather_than_a_match(acknowledged, native):
    _calibrate(acknowledged, '{"method": "otsu"}')
    code, envelope = _drive(["converge"])
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == f"tree.{TREE_ID}"]
    assert check["status"] == converge.NOT_COMPARED, check
    assert "vocal calibration" in check["detail"], check


@pytest.fixture
def voiced(tagged, monkeypatch) -> dict[str, int]:
    """``tagged``, with voxlevel readings served from the file name as well."""
    del tagged
    levels: dict[str, int] = {}
    serve_readings(monkeypatch, vox=lambda path: levels.get(path.name))
    return levels


def _export_vox(document: bytes, folder: str) -> tuple[str, ...] | None:
    """What one folder's vocal sub holds in a written file, None when it has none."""
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
    envelope = _exited(_apply_export(export))
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
    assert offered == {"11": f"Deep House/{_vox_display()}", "12": "", "13": "", "": ""}
    created = [item["destination"] for item in envelope["data"]["items"] if not item["track_id"]]
    assert created == totals["vox_created"]
    # R-694: the subs are nested, so the review names them and no import is owed.
    assert envelope["pending_human_action"] is None
    (review,) = _not_landable(envelope)
    assert "and 2 sub-playlist(s) created" in review, review


def _blocked_export(export: Path) -> dict:
    """The envelope of an export run stopped at its apply gate (R-686)."""
    envelope = _exited(_drive(["route", "inbox", "--export", str(export)]), ExitCode.DECISION_REQUIRED)
    return envelope


def _gate_screen(argv: list[str]) -> str:
    """What a person reads at the apply gate in the default mode."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    assert code == int(ExitCode.DECISION_REQUIRED), err.getvalue()
    return out.getvalue() + err.getvalue()


def _gate_export(configured, voiced, tmp_path) -> Path:
    """An export whose plan carries every column, plus one owed rating it does not (R-688)."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    return _long_export(configured, tmp_path / "exports", ratings={"12": "0"})


def test_the_export_gate_shows_every_item_the_digest_was_taken_over(configured, voiced, tmp_path):
    """``shown`` holds the declined run's items (less R-692's names) and their digest."""
    export = _gate_export(configured, voiced, tmp_path)
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    declined = _exited(_decline_export(export))
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


def test_the_export_gate_names_the_vocal_dimension_it_did_not_read(configured, voiced, tmp_path):
    """Uncalibrated, the empty vocal column says it was not read, not that none are vocal."""
    export = _write_export(configured, tmp_path / "exports")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    assert shown["not derived"] == [rebuild.VOCAL_DIMENSION]
    assert (shown["routed"], shown["vocal"]) == (3, 0)


def test_the_export_gate_screen_says_none_for_an_empty_warning_list(configured, voiced, tmp_path):
    """An empty list says none, not a bare header; these rows carry no rating, so none warn."""
    export = _write_export(configured, tmp_path / "exports")
    assert "  warnings: none" in _gate_screen(["route", "inbox", "--export", str(export)])


def test_the_export_gate_says_why_an_intake_track_goes_nowhere(configured, voiced, tmp_path):
    """An unread track is listed with no destination and its reason before the answer."""
    export = _write_export(configured, tmp_path / "exports", missing_file="12")
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    offered = {item["track_id"]: item["destination"] for item in shown["items"]}
    assert offered == {"11": "Deep House/Low", "12": "", "13": "Tech House/High"}
    assert (shown["tracks"], shown["routed"]) == (3, 2)
    (warning,) = shown["warnings"]
    assert "track 12" in warning and "not routed" in warning


def test_the_export_gate_prints_the_plan_in_the_default_mode(configured, voiced, tmp_path):
    """A person answers from the human screen, so the plan has to reach it."""
    export = _gate_export(configured, voiced, tmp_path)
    digest = _blocked_export(export)["cause"]["detail"]["shown"]["digest"]
    screen = _gate_screen(["route", "inbox", "--export", str(export)])
    assert "Apply this routing plan to the library?" in screen
    assert f"digest: {digest}" in screen
    assert "routed: 3" in screen and "long tracks: 2" in screen
    assert "  not derived: none" in screen
    assert "are owed a star rating" in screen, "the owed rating never reached the screen"
    vox = _vox_display()
    assert (
        f"artist=Artist 11, title=Track 11, track_id=11, destination=Deep House/Low, "
        f"vocal=Deep House/{vox}, genre=, long_track=" in screen
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
    """R-692: the gate names each track, a created sub gets empty names, and the
    declined envelope's items and digest stay the plan's, unnamed."""
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
    declined = _exited(_decline_export(export))
    assert all("artist" not in item and "title" not in item for item in declined["data"]["items"])
    assert _unnamed(shown["items"]) == declined["data"]["items"]
    assert shown["digest"] == declined["data"]["digest"]


def test_the_export_gate_leaves_an_unread_track_unnamed(configured, voiced, tmp_path):
    """An intake key with no collection row is listed with no name rather than a borrowed one."""
    export = _write_export(configured, tmp_path / "exports", inbox=("11", "99"))
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    named = [(item["track_id"], item["artist"], item["title"]) for item in shown["items"]]
    assert named == [("11", "Artist 11", "Track 11"), ("99", "", "")]


def test_the_database_inbox_gate_shows_its_items(acknowledged, native, vox_levels):
    """The same gate on the database path was as blind, and one carry serves it."""
    blocked = _exited(_drive(["route", "inbox"]), ExitCode.DECISION_REQUIRED)
    shown = blocked["cause"]["detail"]["shown"]
    declined = _exited(_decline_inbox())
    assert shown["items"] == declined["data"]["items"] != []
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["count"] == len(declined["data"]["items"])


#: Where the shipped rules file an untagged intake file, as the gate names it (R-691).
FALLBACK_DESTINATION = "Electronica / Other/Unsorted"


def _blocked_inbox() -> dict:
    blocked = _exited(_drive(["route", "inbox"]), ExitCode.DECISION_REQUIRED)
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
    """R-691: the gate shows each destination, the declined run's items, and totals counted off them."""
    shown = _blocked_inbox()
    intake = _intake_dir(acknowledged)
    assert shown["items"] == [
        {
            "path": str(intake / ARRIVED),
            "name": ARRIVED,
            "destination": FALLBACK_DESTINATION,
            "vocal": "",
            "genre": "",
        }
    ]
    declined = _exited(_decline_inbox())
    assert shown["items"] == declined["data"]["items"]
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["intake"] == str(intake)
    assert (shown["count"], shown["tracks"], shown["routed"], shown["vocal"]) == (1, 1, 1, 0)
    assert shown["trees"] == [TREE_ID]
    assert shown["not derived"] == [rebuild.VOCAL_DIMENSION]
    assert shown["warnings"] == []


def test_the_database_apply_files_the_track_where_the_gate_said(acknowledged, native, vox_levels):
    """The plan the gate showed is the plan the write consumes, vocal sub included."""
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    shown = _blocked_inbox()
    (item,) = shown["items"]
    vox = _vox_display()
    assert item["destination"] == FALLBACK_DESTINATION
    assert item["vocal"] == f"Electronica / Other/{vox}"
    assert (shown["routed"], shown["vocal"]) == (1, 1)
    assert shown["not derived"] == []

    applied = _exited(_apply_inbox())
    assert applied["data"]["digest"] == shown["digest"]
    assert _filed_under(acknowledged, native, "2") == {item["destination"], item["vocal"]}


def test_the_database_digest_binds_the_destinations_not_the_file_list(
    acknowledged, native, vox_levels
):
    """A reading that moves a placement moves the digest, over one unchanged folder."""
    before = _blocked_inbox()
    assert [item["vocal"] for item in before["items"]] == [""]
    _calibrated(acknowledged)
    vox_levels[ARRIVED] = 6
    after = _blocked_inbox()
    assert [item["name"] for item in after["items"]] == [item["name"] for item in before["items"]]
    assert [item["vocal"] for item in after["items"]] != [""]
    assert after["digest"] != before["digest"], "the digest binds the file list, not the placements"


#: What the export medium delivers, spelled out (R-695).
INBOX_REMEDY_REVIEW = (
    "no tree has cut over, so nothing files this library into the routing tree. "
    "Export the collection from rekordbox and run route inbox --export with that "
    "file. It writes a review of the routing, and you file its tracks by hand, "
    "since no import can land a nested playlist"
)
INBOX_REMEDY = (
    f"{INBOX_REMEDY_REVIEW}. It also adds long tracks to the root playlist "
    f"{LONG_PLAYLIST!r}, which one import can land"
)


def test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer(
    stocked, monkeypatch
):
    """Nothing native means nothing derived or written, and the gate says so before the question."""
    _calibrate(stocked, '{"threshold": 5.')

    def unread(path):
        raise AssertionError(f"read {path} on a library with nothing native")

    monkeypatch.setattr(rebuild, "read_truth", unread)
    shown = _blocked_inbox()
    assert [item["destination"] for item in shown["items"]] == [""]
    assert (shown["tracks"], shown["routed"], shown["trees"]) == (1, 0, [])
    assert shown["warnings"] == [INBOX_REMEDY]
    assert not Path(stocked.library.db_path).exists(), "the plan opened a database"

    declined = _exited(_decline_inbox())
    assert declined["data"]["totals"]["applied"] is False
    assert [w["message"] for w in declined["warnings"]] == [INBOX_REMEDY]


def test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy(stocked):
    """The gate and the confirmed inbox-empty answer both carry the remedy."""
    for path in _intake_dir(stocked).iterdir():
        path.unlink()
    shown = _blocked_inbox()
    assert shown["items"] == [] and shown["warnings"] == [INBOX_REMEDY]
    applied = _exited(_apply_inbox())
    assert applied["data"]["totals"]["reason"] == "inbox-empty"
    assert [w["message"] for w in applied["warnings"]] == [INBOX_REMEDY]


def test_an_empty_inbox_plan_names_every_native_tree(acknowledged, native):
    """The write indexes the plan by tree, so an empty plan still carries every native tree."""
    for path in _intake_dir(acknowledged).iterdir():
        path.unlink()
    planned = routing_cli.plan_inbox(acknowledged, taxonomy.default_taxonomy())
    assert planned.items == []
    assert planned.placements == {TREE_ID: ()}
    assert planned.warnings == []


def test_the_database_gate_prints_the_destination_in_the_default_mode(acknowledged, native):
    screen = _gate_screen(["route", "inbox"])
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
    envelope = _exited(_apply_export(export))
    totals = envelope["data"]["totals"]
    assert totals["not_derived"] == [rebuild.VOCAL_DIMENSION]
    assert totals["vox_created"] == []
    written = _routed(export).read_bytes()
    assert _export_vox(written, "Deep House") is None
    assert _export_vox(written, "Tech House") is None


def test_a_corrupt_calibration_refuses_the_export_before_the_plan(configured, voiced, tmp_path):
    _calibrate(configured, '{"threshold": true}')
    export = _write_export(configured, tmp_path / "exports")
    envelope = _fails(_apply_export(export))
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

    again = _exited(_apply_export(first))
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
    without = filed.read_bytes().replace(f'Name="{_vox_display()}"'.encode(), b'Name="Removed Sub"')
    bare = tmp_path / "again" / "library_FRESH.xml"
    bare.parent.mkdir()
    bare.write_bytes(without)
    envelope = _exited(_apply_export(bare))
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
    """The vocal writer's raise on an unreachable tree is carried as a skipped write."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    export = _write_export(configured, tmp_path / "exports")
    _hide_routing_tree(export)
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
    envelope = _exited(_apply_export(export))
    assert envelope["data"]["totals"]["vox_created"] == []
    assert envelope["data"]["totals"]["not_derived"] == []
    # Spelled, because the narrowed taxonomy no longer declares the name.
    assert b'Name="with vox"' not in _routed(export).read_bytes()


def test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served(
    configured, voiced, tmp_path
):
    """A folder of the vocal name is refused, and the refusal reaches the envelope (U89 E6)."""
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
        lines.append(f'          <NODE Name="{sub}" Type="1" KeyType="0" Entries="{len(keys)}">')
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
    """A fresh export whose routing tree holds ``held`` and nothing else (U91)."""
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
        collection=[f'  <COLLECTION Entries="{len(EXPORT_TRACKS)}">', *rows, "  </COLLECTION>"],
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
    envelope = _exited(_sweep(export))
    assert envelope["outcome"] == str(Outcome.OK)
    totals = envelope["data"]["totals"]
    assert totals["applied"] is True
    assert totals["inserted"] == 3
    assert totals["created"] == ["Tech House/High"]
    assert totals["output"] == str(_placed(export))

    written = _placed(export).read_bytes()
    for tid, (_name, _genre, _energy, (folder, sub)) in EXPORT_TRACKS.items():
        assert _sub_keys(written, folder, sub) == (tid,), f"{tid} is not alone in {folder}/{sub}"
    assert {
        item["track_id"]: item["destination"] for item in envelope["data"]["items"]
    } == {tid: f"{folder}/{sub}" for tid, (*_, (folder, sub)) in EXPORT_TRACKS.items()}

    # R-694: nested membership the bridge never lands (R-687) owes no import, only a review.
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
    """R-694: after one of three tracks is filed by hand the other two are planned again, as a review."""
    first = _exited(_sweep(_unplaced_export(configured, tmp_path / "before")))
    assert first["pending_human_action"] is None
    later = _unplaced_export(configured, tmp_path / "after", held={("Deep House", "Low"): ("11",)})
    again = _exited(_sweep(later))
    assert again["outcome"] == str(Outcome.OK)
    assert again["pending_human_action"] is None
    assert [item["track_id"] for item in again["data"]["items"]] == ["12", "13"]
    assert again["data"]["totals"]["inserted"] == 2
    (review,) = _not_landable(again)
    assert review.startswith("2 membership(s) routed and 1 sub-playlist(s) created"), review


def test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it(
    configured, tagged, tmp_path
):
    """Placed means held anywhere under the tree, not held where the rule says."""
    export = _unplaced_export(configured, tmp_path / "exports", held={("Deep House", "Med"): ("11",)})
    envelope = _exited(_sweep(export))
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
    envelope = _exited(_sweep(export))
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
    envelope = _exited(_sweep(export))
    assert [item["track_id"] for item in envelope["data"]["items"]] == ["11", "12"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Deep House", "Low") == ("11",)
    assert _sub_keys(written, "Deep House", "Med") == ("12",)


def test_without_the_flag_nothing_is_written_and_the_answer_names_the_flag(
    configured, tagged, tmp_path
):
    """R-313's report stays a report and names what the export delivers: a review, no import (R-694, R-695)."""
    export = _unplaced_export(configured, tmp_path / "exports")
    before = {path.name: path.read_bytes() for path in export.parent.iterdir()}
    code, envelope = _drive(["route", "unplaced"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["compared"] is False
    assert [w["code"] for w in envelope["warnings"]] == ["no-native-tree"]
    assert envelope["warnings"][0]["message"] == (
        "no tree has cut over, so nothing places what the routing tree does not "
        "hold. Export the collection from rekordbox and run route unplaced "
        "--export with that file. It writes a review of where each unplaced "
        "track belongs, and you file those tracks by hand, since no import can "
        "land a nested playlist. It adds to no root playlist and owes no import"
    )
    assert {path.name: path.read_bytes() for path in export.parent.iterdir()} == before


def test_no_tempo_or_bpm_attribute_differs_after_the_sweep(configured, tagged, tmp_path):
    """Never write a beat grid: every grid token the export held comes back as it was."""
    export = _unplaced_export(configured, tmp_path / "exports")
    _exited(_sweep(export))
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
    envelope = _exited(_sweep(first))
    assert envelope["outcome"] == str(Outcome.NO_OP)
    totals = envelope["data"]["totals"]
    assert totals["inserted"] == 0
    assert totals["reason"] == "nothing-to-route"
    assert totals["output"] is None
    assert sorted(path.name for path in first.parent.iterdir()) == before


def test_an_unreadable_track_is_a_warning_and_the_rest_are_placed(configured, tagged, tmp_path):
    export = _unplaced_export(configured, tmp_path / "exports", missing_file="13")
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    assert [w["code"] for w in _others(envelope)] == ["track-file-unreadable"]
    assert b'Name="High"' not in _placed(export).read_bytes()


def test_a_sweep_that_could_place_nothing_is_blocked_not_done(configured, tagged, tmp_path):
    """An unreadable lone track writes nothing, and is not the ``nothing-to-route`` read as done."""
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        held={("Deep House", "Low"): ("11",), ("Deep House", "Med"): ("12",)},
        missing_file="13",
    )
    envelope = _exited(_sweep(export))
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["totals"]["reason"] == "route-blocked"
    assert not _placed(export).exists()


def test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented(
    configured, tagged, tmp_path
):
    """The creating writer makes a sub, never a genre folder."""
    export = _unplaced_export(configured, tmp_path / "exports", folders=(("Deep House", ("Low", "Med")),))
    code, envelope = _sweep(export)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["inserted"] == 2
    messages = [w["message"] for w in envelope["warnings"] if w["code"] == "route-write-skipped"]
    assert any("Tech House" in message for message in messages), messages
    assert b'Name="Tech House"' not in _placed(export).read_bytes()


def test_a_cut_over_tree_refuses_the_sweep_and_writes_nothing(configured, tagged, tmp_path):
    _cut_over_routing_tree(configured)
    export = _unplaced_export(configured, tmp_path / "exports")
    envelope = _fails(_sweep(export))
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
    envelope = _fails(_sweep(export))
    assert envelope["cause"]["reason"] == "governed-tree-absent"
    assert not _placed(export).exists()


def test_an_unmounted_library_refuses_the_sweep(configured, tagged, tmp_path, monkeypatch):
    export = _unplaced_export(configured, tmp_path / "exports")
    real = Path.is_dir
    root = Path(configured.library.root)
    monkeypatch.setattr(Path, "is_dir", lambda self: False if self == root else real(self))
    envelope = _fails(_sweep(export))
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
    _exited(_sweep(export))
    assert not session.lock_path(configured).exists()


def test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates(
    configured, voiced, tmp_path
):
    """Over the cut a track files under its energy sub and a vocal sub the writer creates."""
    _calibrated(configured)
    voiced["Top Track.flac"] = 6
    vox = _vox_display()
    export = _unplaced_export(
        configured,
        tmp_path / "exports",
        folders=(("Deep House", ("Low", "Med")), ("Tech House", ("Low", "Med", "High"))),
    )
    envelope = _exited(_sweep(export))
    assert envelope["data"]["totals"]["created"] == [f"Tech House/{vox}"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert _sub_keys(written, "Tech House", vox) == ("13",)
    vocal = {item["track_id"]: item["vocal"] for item in envelope["data"]["items"]}
    assert vocal == {"11": "", "12": "", "13": f"Tech House/{vox}"}


def test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses(
    configured, tagged, tmp_path
):
    """U91: a bare LF above a folder's close once put the created sub a byte early, splitting a ``/>``."""
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
    """The writer is told the tree, so it searches the tree alone (U91's U6 row)."""
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

    envelope = _exited(_sweep(export))
    assert envelope["data"]["totals"]["created"] == ["Tech House/High"]
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Tech House", "High") == ("13",)
    assert written.count(b'Name="High"') == 1, "a High was created outside the routing tree"


def test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent(configured, tagged, tmp_path):
    """A key with no row is one warning naming the row, not a second about a file (U91 P1)."""
    export = _write_export(configured, tmp_path / "exports", inbox=("11", "99"))
    code, envelope = _apply_export(export)
    assert code == int(ExitCode.OK), envelope
    assert [w["code"] for w in _others(envelope)] == ["track-row-absent"]


@pytest.fixture
def rominimal(monkeypatch):
    """The intake file reads as a Rominimal track at energy 3, with no vocal reading."""
    readings = {ARRIVED: ("Rominimal", 3)}
    serve_readings(
        monkeypatch,
        genre=lambda path: readings.get(path.name, (None, None))[0],
        energy=lambda path: readings.get(path.name, (None, None))[1],
        vox=lambda path: None,
    )


def test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both(
    acknowledged, native, rominimal
):
    """U155: the gate names the band and the genre sub the apply files into, and counts both."""
    del rominimal
    shown = _blocked_inbox()
    (item,) = shown["items"]
    assert item["destination"] == "Minimal / Deep Tech/Low Energy"
    assert item["genre"] == "Minimal / Deep Tech/Rominimal"
    assert item["vocal"] == ""
    assert (shown["routed"], shown["vocal"], shown["genre sub"]) == (1, 0, 1)
    applied = _exited(_apply_inbox())
    assert applied["data"]["items"] == shown["items"]
    assert _filed_under(acknowledged, native, "2") == {
        "Minimal / Deep Tech/Low Energy",
        "Minimal / Deep Tech/Rominimal",
    }


def test_the_gate_counts_tracks_filed_into_a_genre_sub():
    items = [
        {"destination": "A/Low", "vocal": "", "genre": "A/Rominimal"},
        {"destination": "A/Med", "vocal": "A/with vox", "genre": ""},
        {"destination": "", "vocal": "", "genre": ""},
    ]
    assert routing_cli._placed_counts(items) == {"routed": 2, "vocal": 1, "genre sub": 1}


def test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place(configured, voiced, tmp_path):
    """A vocal track files into two places and its row is still owed one rating (U155)."""
    _calibrated(configured)
    voiced["Low Track.flac"] = 6
    export = _write_export(configured, tmp_path / "exports", ratings={"11": "0"})
    envelope = _exited(_apply_export(export))
    (message,) = _owed(envelope)
    assert message.startswith("1 intake row(s) are owed a star rating"), message


#: The genre folder holding the Rominimal sub track 11 reads into on the export medium.
ROMINIMAL_FOLDER = ("Minimal / Deep Tech", ("Low Energy", "Med Energy", "High Energy", "Rominimal"))


@pytest.fixture
def rominimal_export(tagged, monkeypatch):
    """Track 11 reads as Rominimal at energy 2, the others as EXPORT_TRACKS has them."""
    del tagged
    readings = {name: (genre, energy) for name, genre, energy, _ in EXPORT_TRACKS.values()}
    readings["Low Track.flac"] = ("Rominimal", 2)
    serve_readings(
        monkeypatch,
        genre=lambda path: readings.get(path.name, (None, None))[0],
        energy=lambda path: readings.get(path.name, (None, None))[1],
    )


def test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both(
    configured, rominimal_export, tmp_path
):
    """The export gate names both places and counts the second; the file holds both."""
    del rominimal_export
    subs = ("Low", "Med", "High")
    folders = (("Deep House", subs), ("Tech House", subs), ROMINIMAL_FOLDER)
    export = _write_export(configured, tmp_path / "exports", folders=folders)
    shown = _blocked_export(export)["cause"]["detail"]["shown"]
    offered = {item["track_id"]: item for item in shown["items"]}
    assert offered["11"]["destination"] == "Minimal / Deep Tech/Low Energy"
    assert offered["11"]["genre"] == "Minimal / Deep Tech/Rominimal"
    assert offered["12"]["genre"] == "" and offered["13"]["genre"] == ""
    assert (shown["routed"], shown["genre sub"]) == (3, 1)
    _exited(_apply_export(export))
    written = _routed(export).read_bytes()
    assert _sub_keys(written, "Minimal / Deep Tech", "Low Energy") == ("11",)
    assert _sub_keys(written, "Minimal / Deep Tech", "Rominimal") == ("11",)


def test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both(
    configured, rominimal_export, tmp_path
):
    del rominimal_export
    folders = (("Deep House", ("Low", "Med")), ("Tech House", ("Low", "Med")), ROMINIMAL_FOLDER)
    export = _unplaced_export(configured, tmp_path / "exports", folders=folders)
    envelope = _exited(_sweep(export))
    offered = {item["track_id"]: item for item in envelope["data"]["items"]}
    assert offered["11"]["destination"] == "Minimal / Deep Tech/Low Energy"
    assert offered["11"]["genre"] == "Minimal / Deep Tech/Rominimal"
    written = _placed(export).read_bytes()
    assert _sub_keys(written, "Minimal / Deep Tech", "Rominimal") == ("11",)
    assert _sub_keys(written, "Minimal / Deep Tech", "Low Energy") == ("11",)
