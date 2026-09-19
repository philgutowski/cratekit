"""U25: ``metadata.mytags-vocals`` writes My Tags, never a content column."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from cratekit.core import config, locations, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.write import metadata_cli
from tests._containers import synth_container
from tests.adopt_fixtures import BASELINE_CONTENT_IDS
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row


@pytest.fixture
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def ready(tmp_path, monkeypatch, silence):
    """A machine that can plan and, with --apply, write My Tags on a copy."""
    from pyrekordbox.db6 import database as binding

    from cratekit.core import preflight

    library = tmp_path / "library"
    music = library / "Music"
    music.mkdir(parents=True)
    db_path = library / "db" / "master.db"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
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
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer, "read_rekordbox_settings", lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0}
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )
    session.record_acknowledgment(cfg, terminal=lambda: True)

    _build_disposable_database(db_path, with_tag_category=True)
    audio = music / "voiced.flac"
    shutil.copy2(silence, audio)
    assert tags.write_tags(audio, {"voxlevel": 80, "voxgender": "M", "voxgenderconf": 90})

    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdContent,
                ID="3",
                Title="voiced.flac",
                rb_local_deleted=0,
                FolderPath=locations.location_url(audio),
            )
        )
        db_session.commit()
    engine.dispose()
    return cfg, audio, db_path


def test_vocal_tag_values_are_empty_below_the_cut():
    assert metadata_cli.vocal_tag_values(None, "M", 12.0) == []
    assert metadata_cli.vocal_tag_values(11, "M", 12.0) == []
    assert metadata_cli.vocal_tag_values(12, None, 12.0) == ["vox"]
    assert metadata_cli.vocal_tag_values(12, "M", 12.0) == ["vox", "male vox"]
    assert metadata_cli.vocal_tag_values(90, "F", 12.0) == ["vox", "female vox"]
    assert metadata_cli.vocal_tag_values(90, "U", 12.0) == ["vox"]


def _vocal_calibration(cfg, text: str) -> Path:
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_an_absent_vocal_calibration_is_the_default_cut(tmp_path):
    cfg = config.from_dict(valid_data(tmp_path / "library"))
    assert not config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg).exists()
    assert metadata_cli.vocal_cut(cfg) == 12.0


def test_a_present_vocal_calibration_is_its_own_threshold(tmp_path):
    cfg = config.from_dict(valid_data(tmp_path / "library"))
    _vocal_calibration(cfg, '{"threshold": 37.5, "method": "otsu"}')
    assert metadata_cli.vocal_cut(cfg) == 37.5


@pytest.mark.parametrize(
    "text",
    [
        '{"threshold": 37.',
        "",
        '["threshold", 37.5]',
        '{"method": "otsu"}',
        '{"threshold": "high"}',
        '{"threshold": null}',
        '{"threshold": NaN}',
        '{"threshold": Infinity}',
        '{"threshold": 1' + "0" * 400 + "}",
        '{"threshold": true}',
    ],
    ids=[
        "truncated",
        "empty",
        "list",
        "no-key",
        "text",
        "null",
        "nan",
        "infinity",
        "overflow",
        "boolean",
    ],
)
def test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting(tmp_path, text):
    """R-342: a corrupt calibration is not an absent one, so it is never the default cut."""
    from cratekit.core.cause import CratekitError

    cfg = config.from_dict(valid_data(tmp_path / "library"))
    path = _vocal_calibration(cfg, text)
    with pytest.raises(CratekitError) as caught:
        metadata_cli.vocal_cut(cfg)
    assert caught.value.cause.reason == "vocal-calibration-unreadable"
    assert caught.value.cause.detail["calibration"] == str(path)


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a file with no permissions")
def test_a_vocal_calibration_this_account_cannot_read_refuses(tmp_path):
    from cratekit.core.cause import CratekitError

    cfg = config.from_dict(valid_data(tmp_path / "library"))
    path = _vocal_calibration(cfg, '{"threshold": 37.5}')
    path.chmod(0)
    try:
        with pytest.raises(CratekitError) as caught:
            metadata_cli.vocal_cut(cfg)
    finally:
        path.chmod(0o600)
    assert caught.value.cause.reason == "vocal-calibration-unreadable"
    assert caught.value.cause.detail["kind"] == "PermissionError"


def test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing(ready):
    cfg, audio, db_path = ready
    del audio
    _vocal_calibration(cfg, '{"threshold": 37.')
    code, envelope = drive(["metadata", "mytags-vocals", "--apply"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "vocal-calibration-unreadable"

    db = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        assert metadata_cli.VALUE_VOX not in [tag.Name for tag in db.get_my_tag()]
    finally:
        rb_writer.close_db(db)


def test_the_plan_names_existing_rows_and_writes_nothing(ready):
    cfg, audio, db_path = ready
    del audio
    code, envelope = drive(["metadata", "mytags-vocals"])
    assert code == int(ExitCode.OK), envelope
    items = envelope["data"]["items"]
    assert [row["content_id"] for row in items] == ["3"]
    assert items[0]["values"] == [metadata_cli.VALUE_VOX, metadata_cli.VALUE_MALE]
    assert envelope["data"]["totals"]["written"] == 0
    assert envelope["data"]["chunk"] is None

    db = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        names = [tag.Name for tag in db.get_my_tag()]
        assert metadata_cli.VALUE_VOX not in names
        content = next(c for c in db.get_content() if str(c.ID) == "3")
        assert getattr(content, "GenreID", None) in (None, "")
    finally:
        rb_writer.close_db(db)


def test_apply_writes_my_tags_and_does_not_write_a_content_column(ready):
    cfg, audio, db_path = ready
    del audio
    before = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        row = next(c for c in before.get_content() if str(c.ID) == "3")
        title = row.Title
        genre = getattr(row, "GenreID", None)
        rating = getattr(row, "Rating", None)
        color = getattr(row, "ColorID", None)
    finally:
        rb_writer.close_db(before)

    code, envelope = drive(["metadata", "mytags-vocals", "--apply"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["written"] >= 1
    assert envelope["data"]["totals"]["written"] == 2, envelope["data"]["totals"]

    after = rb_writer.open_db(db_path, unlock=False, cfg=cfg)
    try:
        row = next(c for c in after.get_content() if str(c.ID) == "3")
        assert row.Title == title
        assert getattr(row, "GenreID", None) == genre
        assert getattr(row, "Rating", None) == rating
        assert getattr(row, "ColorID", None) == color
        vox = next(tag for tag in after.get_my_tag() if tag.Name == metadata_cli.VALUE_VOX)
        male = next(tag for tag in after.get_my_tag() if tag.Name == metadata_cli.VALUE_MALE)
        assert str(vox.ParentID) != "0"
        assert after.get_my_tag_songs(MyTagID=str(vox.ID), ContentID="3").first() is not None
        assert after.get_my_tag_songs(MyTagID=str(male.ID), ContentID="3").first() is not None
        for baseline in BASELINE_CONTENT_IDS:
            assert after.get_my_tag_songs(MyTagID=str(vox.ID), ContentID=baseline).first() is None
    finally:
        rb_writer.close_db(after)


def test_a_second_apply_is_idempotent(ready):
    cfg, audio, db_path = ready
    del cfg, audio
    drive(["metadata", "mytags-vocals", "--apply"])
    code, envelope = drive(["metadata", "mytags-vocals", "--apply"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["written"] == 0
    assert envelope["data"]["totals"]["already"] == 2
    del db_path


def test_a_library_with_no_tag_category_refuses_through_the_verb(ready, monkeypatch):
    """First caller of ensure_my_tag_value: the writer's refusal must reach the person."""
    cfg, audio, db_path = ready
    del audio
    db_path.unlink()
    _build_disposable_database(db_path, with_tag_category=False)
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdContent,
                ID="3",
                Title="voiced.flac",
                rb_local_deleted=0,
                FolderPath=locations.location_url(
                    Path(cfg.library.root) / "Music" / "voiced.flac"
                ),
            )
        )
        db_session.commit()
    engine.dispose()
    del monkeypatch
    code, envelope = drive(["metadata", "mytags-vocals", "--apply"])
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "mytag-category-template-missing"
