"""U20: the automated precheck that must pass before a tree flips.

Four refusals and one happy path. The flip itself is ``record_cutover`` plus
this precheck, composed as ``tree_registry.flip``. Live rekordbox validation
is attended and is not in this file.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import output
from cratekit.core import config, session, snapshot, tree_registry
from cratekit.core.cause import CratekitError
from tests.test_config import valid_data

TREE_ID = "genre_energy"
CUTOVER_ON = date(2026, 8, 1)
DERIVATION = tree_registry.DerivationSource.TAXONOMY


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library):
    return config.from_dict(valid_data(library))


def _export(cfg: config.Config) -> Path:
    path = Path(cfg.library.root) / "fresh_export.xml"
    path.write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    return path


def _snapshot(cfg: config.Config) -> Path:
    store = snapshot.store_root(cfg)
    capture = store / "2026-08-01T000000Z-deadbeefcafebabe"
    capture.mkdir(parents=True)
    record = snapshot.Capture(
        stamp=capture.name,
        root=capture,
        database=capture / "master.db",
        integrity_verified=True,
    )
    (capture / snapshot.MANIFEST_NAME).write_text(
        json.dumps(record.to_json()) + "\n", encoding="utf-8"
    )
    return capture


def _ready(cfg: config.Config) -> Path:
    _snapshot(cfg)
    return _export(cfg)


def test_a_ready_library_flips_one_tree_and_leaves_the_rest_on_the_bridge(cfg):
    export = _ready(cfg)
    after = tree_registry.flip(
        cfg,
        TREE_ID,
        root_id="root-1",
        on=CUTOVER_ON,
        source=DERIVATION,
        export=export,
    )
    assert after.is_database_native(TREE_ID)
    assert after.is_on_the_bridge("inbox")
    record = after.record(TREE_ID)
    assert record is not None
    assert record.root_id == "root-1"
    assert record.cutover_on == CUTOVER_ON


def test_an_open_run_blocks_the_flip(cfg):
    export = _ready(cfg)
    session.write_record(
        session.SessionRecord(
            session_id="s-open",
            workflow="deferred-routing",
            started=output.timestamp(),
            state=session.SessionState.OPEN,
        ),
        cfg,
    )
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg, TREE_ID, root_id="root-1", on=CUTOVER_ON, source=DERIVATION, export=export
        )
    assert excinfo.value.cause.reason == "cutover-open-run"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_pending_intake_xml_blocks_the_flip(cfg):
    export = _ready(cfg)
    staging = Path(cfg.paths.download_staging)
    staging.mkdir(parents=True)
    (staging / "run-1_synced.xml").write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg, TREE_ID, root_id="root-1", on=CUTOVER_ON, source=DERIVATION, export=export
        )
    assert excinfo.value.cause.reason == "cutover-xml-pending"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_missing_export_blocks_the_flip(cfg):
    _snapshot(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg,
            TREE_ID,
            root_id="root-1",
            on=CUTOVER_ON,
            source=DERIVATION,
            export=Path(cfg.library.root) / "nope.xml",
        )
    assert excinfo.value.cause.reason == "cutover-export-missing"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_missing_snapshot_blocks_the_flip(cfg):
    export = _export(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg, TREE_ID, root_id="root-1", on=CUTOVER_ON, source=DERIVATION, export=export
        )
    assert excinfo.value.cause.reason == "cutover-snapshot-missing"
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_an_unverified_capture_does_not_count_as_a_snapshot(cfg):
    store = snapshot.store_root(cfg)
    fake = store / "2026-08-01T000000Z-unverified0001"
    fake.mkdir(parents=True)
    (fake / snapshot.MANIFEST_NAME).write_text("{}\n", encoding="utf-8")
    export = _export(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg, TREE_ID, root_id="root-1", on=CUTOVER_ON, source=DERIVATION, export=export
        )
    assert excinfo.value.cause.reason == "cutover-snapshot-missing"


def test_the_intake_tree_flips_on_a_rebuildable_source_like_any_other(cfg):
    """R-746. The intake tree's own refusal is gone: the landing chooses its
    medium by the tree's mode, so a native intake tree refuses no splice that
    anything still owes. The precheck and the rebuildability rule still hold."""
    export = _ready(cfg)
    tree_registry.flip(
        cfg,
        "inbox",
        root_id="root-inbox",
        on=CUTOVER_ON,
        source=DERIVATION,
        export=export,
    )
    recorded = tree_registry.read(cfg)
    assert recorded.is_database_native("inbox")
    assert recorded.record("inbox").root_id == "root-inbox"


def test_a_revert_puts_the_tree_back_on_the_bridge(cfg):
    export = _ready(cfg)
    tree_registry.flip(
        cfg,
        TREE_ID,
        root_id="root-1",
        on=CUTOVER_ON,
        source=DERIVATION,
        export=export,
    )
    after = tree_registry.revert_cutover(cfg, TREE_ID)
    assert after.is_on_the_bridge(TREE_ID)
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_hand_curated_tree_still_cannot_flip(cfg):
    export = _ready(cfg)
    with pytest.raises(tree_registry.TreeModeRefused):
        tree_registry.flip(
            cfg,
            "record_labels",
            root_id="root-2",
            on=CUTOVER_ON,
            source=tree_registry.DerivationSource.CURATED,
            export=export,
        )
    assert tree_registry.read(cfg).is_on_the_bridge("record_labels")


# ---------------------------------------------------------------------------
# R-235: the precheck as a report, and the guard on the way back
# ---------------------------------------------------------------------------


def test_the_report_names_every_check_in_the_order_the_assertion_refuses(cfg):
    export = _ready(cfg)
    results = tree_registry.cutover_precheck(cfg, export=export)
    assert [result.check for result in results] == [
        "no-open-run",
        "no-pending-intake-xml",
        "fresh-export",
        "verified-snapshot",
    ]
    assert all(result.passed for result in results)


def test_the_report_carries_each_refusal_and_does_not_stop_at_the_first(cfg):
    """Nothing is ready here, and the two checks that can fail both say so."""
    results = tree_registry.cutover_precheck(
        cfg, export=Path(cfg.library.root) / "nope.xml"
    )
    failed = {result.check: result.cause.reason for result in results if not result.passed}
    assert failed == {
        "fresh-export": "cutover-export-missing",
        "verified-snapshot": "cutover-snapshot-missing",
    }


def test_the_report_and_the_assertion_refuse_with_one_cause(cfg):
    export = _export(cfg)
    (failing,) = [
        result
        for result in tree_registry.cutover_precheck(cfg, export=export)
        if not result.passed
    ]
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.assert_cutover_ready(cfg, export=export)
    assert excinfo.value.cause == failing.cause


def _native_write(cfg: config.Config, *, tree: str = TREE_ID, created: int = 1) -> None:
    session.write_record(
        session.SessionRecord(
            session_id=f"s-write-{tree}-{created}",
            workflow="tree-membership",
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            change=session.ChangeSummary((session.TreeChange(tree=tree, created=created),)),
        ),
        cfg,
    )


def _flipped(cfg: config.Config) -> None:
    tree_registry.flip(
        cfg,
        TREE_ID,
        root_id="root-1",
        on=CUTOVER_ON,
        source=DERIVATION,
        export=_ready(cfg),
    )


def test_a_revert_after_a_native_write_is_refused_by_the_library_itself(cfg):
    _flipped(cfg)
    _native_write(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.revert_cutover(cfg, TREE_ID)
    assert excinfo.value.cause.reason == "cutover-native-write-taken"
    assert excinfo.value.cause.detail["sessions"] == [f"s-write-{TREE_ID}-1"]
    assert tree_registry.read(cfg).is_database_native(TREE_ID)


def test_an_update_counts_as_a_native_write_as_a_creation_does(cfg):
    _flipped(cfg)
    session.write_record(
        session.SessionRecord(
            session_id="s-update",
            workflow="tree-membership",
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            change=session.ChangeSummary((session.TreeChange(tree=TREE_ID, updated=3),)),
        ),
        cfg,
    )
    assert tree_registry.native_writes(cfg, TREE_ID) == ("s-update",)
    with pytest.raises(CratekitError):
        tree_registry.assert_revertible(cfg, TREE_ID)


def test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open(cfg):
    _flipped(cfg)
    _native_write(cfg, tree="record_labels", created=5)
    _native_write(cfg, created=0)
    assert tree_registry.native_writes(cfg, TREE_ID) == ()
    assert tree_registry.revert_cutover(cfg, TREE_ID).is_on_the_bridge(TREE_ID)


# ---------------------------------------------------------------------------
# What the review of R-235 found, closed
# ---------------------------------------------------------------------------


def _unreadable_record(cfg: config.Config) -> Path:
    directory = session.log_dir(cfg)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "s-torn.json"
    path.write_text("{ not a record\n", encoding="utf-8")
    return path


def test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write(cfg):
    """The gate's policy, not the report's: the torn record may be the write."""
    _flipped(cfg)
    torn = _unreadable_record(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.revert_cutover(cfg, TREE_ID)
    assert excinfo.value.cause.detail["unreadable"] == [str(torn)]
    assert tree_registry.read(cfg).is_database_native(TREE_ID)


def test_a_record_nobody_can_read_refuses_the_flip_rather_than_reading_as_no_open_run(cfg):
    export = _ready(cfg)
    torn = _unreadable_record(cfg)
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg, TREE_ID, root_id="root-1", on=CUTOVER_ON, source=DERIVATION, export=export
        )
    assert excinfo.value.cause.detail["unreadable"] == [str(torn)]
    assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_an_open_run_refuses_the_revert_because_it_may_have_written(cfg):
    _flipped(cfg)
    session.write_record(
        session.SessionRecord(
            session_id="s-killed",
            workflow="tree-membership",
            started=output.timestamp(),
            state=session.SessionState.OPEN,
        ),
        cfg,
    )
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.revert_cutover(cfg, TREE_ID)
    assert excinfo.value.cause.reason == "cutover-open-run"
    assert excinfo.value.cause.detail["sessions"] == ["s-killed"]
    assert tree_registry.read(cfg).is_database_native(TREE_ID)


def _write_started(cfg: config.Config, session_id: str, started: str) -> None:
    session.write_record(
        session.SessionRecord(
            session_id=session_id,
            workflow="tree-membership",
            started=started,
            state=session.SessionState.CLOSED,
            change=session.ChangeSummary((session.TreeChange(tree=TREE_ID, created=2),)),
        ),
        cfg,
    )


def test_a_write_under_an_earlier_cutover_does_not_close_this_ones_door(cfg):
    """Cut over, written, restored to before it, cut over again: one write, long ago."""
    _write_started(cfg, "s-last-month", "2026-07-01T10:00:00Z")
    _flipped(cfg)
    assert tree_registry.native_writes(cfg, TREE_ID) == ()
    assert tree_registry.revert_cutover(cfg, TREE_ID).is_on_the_bridge(TREE_ID)


@pytest.mark.parametrize(
    "started",
    [
        # The cutover day itself, and the day before it: a start is universal
        # time and the cutover day is the machine's own calendar date.
        "2026-08-01T00:05:00Z",
        "2026-07-31T23:50:00Z",
        # A start nothing can place counts, because it cannot be shown to predate.
        "not a timestamp",
    ],
)
def test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts(cfg, started):
    _write_started(cfg, "s-near", started)
    _flipped(cfg)
    assert tree_registry.native_writes(cfg, TREE_ID) == ("s-near",)


def test_the_day_before_the_margin_is_the_first_day_left_out(cfg):
    _write_started(cfg, "s-two-days", "2026-07-30T23:59:59Z")
    _flipped(cfg)
    assert tree_registry.native_writes(cfg, TREE_ID) == ()


def test_a_tree_already_recorded_is_not_recorded_again(cfg):
    """Under the lock, so two approved cutovers cannot replace one another."""
    _flipped(cfg)
    export = _export(cfg)
    before = tree_registry.path_for(cfg).read_bytes()
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.flip(
            cfg,
            TREE_ID,
            root_id="root-2",
            on=date(2026, 9, 1),
            source=DERIVATION,
            export=export,
        )
    assert excinfo.value.cause.reason == "cutover-already-recorded"
    assert excinfo.value.cause.detail["root_id"] == "root-1"
    assert tree_registry.path_for(cfg).read_bytes() == before


def test_a_reverted_tree_can_cut_over_again(cfg):
    _flipped(cfg)
    export = _export(cfg)
    tree_registry.revert_cutover(cfg, TREE_ID)
    after = tree_registry.flip(
        cfg, TREE_ID, root_id="root-2", on=CUTOVER_ON, source=DERIVATION, export=export
    )
    assert after.record(TREE_ID).root_id == "root-2"


def test_the_revert_holds_the_session_lock_while_it_asks_and_writes(cfg, monkeypatch):
    """No membership write is in flight between the question and the file."""
    _flipped(cfg)
    held_during: list[bool] = []
    real = tree_registry.assert_revertible

    def watching(config_in_hand, tree_id):
        held_during.append(bool(session._HELD))
        return real(config_in_hand, tree_id)

    monkeypatch.setattr(tree_registry, "assert_revertible", watching)
    tree_registry.revert_cutover(cfg, TREE_ID)
    assert held_during == [True]
    assert not session._HELD, "the revert left the session lock held"
