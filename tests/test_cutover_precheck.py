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


def test_the_intake_tree_cannot_flip_even_on_a_rebuildable_source(cfg):
    export = _ready(cfg)
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        tree_registry.flip(
            cfg,
            "inbox",
            root_id="root-inbox",
            on=CUTOVER_ON,
            source=DERIVATION,
            export=export,
        )
    assert excinfo.value.tree_id == "inbox"
    assert tree_registry.read(cfg).is_on_the_bridge("inbox")


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
