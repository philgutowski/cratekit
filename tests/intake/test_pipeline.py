"""U37: normalize, identify, single-file ingest, lossy policy, recognition gate."""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.acquire.adapter import LosslessPolicy
from cratekit.acquire.match import Wanted
from cratekit.core import config, naming, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.naming import MarkerRule, NameSpec, NameTemplate
from cratekit.intake import normalize, pipeline, recognize
from cratekit.intake.ingest import decide_placement, read_meta
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml


def _cfg(tmp_path: Path) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    staging = tmp_path / "staging"
    staging.mkdir()
    data = valid_data(root)
    data["paths"] = {"download_staging": str(staging)}
    cfg = config.from_dict(data)
    config.save(cfg)
    config.reset_cache()
    return cfg


def test_a_tracklist_and_a_file_become_the_same_wanted_shape(tmp_path):
    rows = normalize.from_tracklist("Artist One - Title One\nArtist Two - Title Two\n")
    assert len(rows) == 2
    assert rows[0].artist == "Artist One"
    assert rows[0].title == "Title One"
    audio = tmp_path / "song.flac"
    audio.write_bytes(b"fLaC")
    file_rows = normalize.from_audio_file(audio)
    assert len(file_rows) == 1
    assert file_rows[0].ref == str(audio.resolve())


def test_identification_only_downloads_nothing_and_writes_a_tracklist(
    tmp_path, monkeypatch
):
    source = tmp_path / "set.mp3"
    source.write_bytes(b"ID3")

    def fake_identifier(path: Path) -> tuple[Wanted, ...]:
        assert path == source
        return (Wanted(artist="A", title="One"), Wanted(artist="B", title="Two"))

    with pytest.raises(CratekitError) as excinfo:
        pipeline.identify_only(source, identifier=fake_identifier)
    assert excinfo.value.cause.reason == "intake-recognition-unready"

    monkeypatch.setattr(recognize.secrets, "exists", lambda name: True)
    # BOTH binaries, because the gate names both: ffmpeg carves and ffprobe
    # measures, and a build that could carve but not measure would spend
    # before it knew how much.
    monkeypatch.setattr(
        recognize.binaries,
        "find",
        lambda name: f"/usr/bin/{name}" if name in recognize.BINARIES else None,
    )
    result = pipeline.identify_only(source, identifier=fake_identifier)
    assert "A - One" in result.tracklist
    assert "B - Two" in result.tracklist
    assert result.rows[0].artist == "A"


def test_a_missing_recognition_key_is_reported_before_any_spend(tmp_path):
    called = {"n": 0}

    def identifier(_path: Path) -> tuple[Wanted, ...]:
        called["n"] += 1
        return ()

    with pytest.raises(CratekitError) as excinfo:
        recognize.identify(tmp_path / "x.mp3", identifier=identifier)
    assert excinfo.value.cause.reason == "intake-recognition-unready"
    assert called["n"] == 0


def test_single_file_ingest_uses_no_network(tmp_path):
    cfg = _cfg(tmp_path)
    audio = Path(cfg.library.root) / "track.flac"
    audio.write_bytes(b"fLaC")
    export = tmp_path / "fresh.xml"
    export.write_bytes(_fresh_xml())
    destination = Path(cfg.library.root) / "batch_inboxed.xml"
    result = pipeline.ingest_file(
        audio, cfg=cfg, export=export, destination=destination
    )
    assert result.networked is False
    assert destination.is_file()
    body = destination.read_bytes()
    assert b"<TEMPO" not in body
    assert b'AverageBpm="0.00"' in body
    assert result.placed[0].location.startswith("file://localhost")


def test_slim_analysis_off_omits_key_and_bpm_from_the_name():
    template = NameTemplate(
        markers=(MarkerRule(field="lossy", literal="[MP3]"),),
    )
    rendered = naming.render_all(
        NameSpec(stem="Night Drive", suffix=".flac", title="Night Drive"),
        template=template,
    )
    assert rendered.filename == "Night Drive.flac"
    assert " - " not in rendered.filename
    assert rendered.title_tag == "Night Drive"
    assert rendered.library_name == rendered.title_tag


def test_strict_lossy_is_reported_unacquired():
    with pytest.raises(CratekitError) as excinfo:
        pipeline.acquire_lossy_or_refuse(
            policy=LosslessPolicy.STRICT, source_is_lossless=False
        )
    assert excinfo.value.cause.reason == "lossy-refused"


def test_lossy_allowed_requires_the_marker_on_all_three_surfaces():
    marked = pipeline.acquire_lossy_or_refuse(
        policy=LosslessPolicy.ALLOW_LOSSY_MARKED, source_is_lossless=False
    )
    assert marked is True
    template = NameTemplate(
        markers=(MarkerRule(field="lossy", literal="[MP3]"),),
    )
    rendered = naming.render_all(
        NameSpec(stem="Title", suffix=".mp3", title="Title", lossy=True),
        template=template,
    )
    assert "[MP3]" in rendered.filename
    assert "[MP3]" in rendered.title_tag
    assert "[MP3]" in rendered.library_name


def test_a_stub_export_is_refused(tmp_path):
    cfg = _cfg(tmp_path)
    audio = Path(cfg.library.root) / "track.flac"
    audio.write_bytes(b"fLaC")
    stub = tmp_path / "run_synced.xml"
    stub.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        "<DJ_PLAYLISTS>\r\n"
        "  <COLLECTION>\r\n"
        '    <TRACK Name="identity"/>\r\n'
        "</COLLECTION>\r\n"
        "</DJ_PLAYLISTS>\r\n",
        encoding="utf-8",
    )
    with pytest.raises(CratekitError) as excinfo:
        pipeline.ingest_file(
            audio,
            cfg=cfg,
            export=stub,
            destination=tmp_path / "out.xml",
        )
    assert excinfo.value.cause.reason == "intake-export-is-stub"


def test_staging_files_are_refused(tmp_path):
    cfg = _cfg(tmp_path)
    trapped = Path(cfg.paths.download_staging) / "still-here.flac"
    trapped.write_bytes(b"fLaC")
    with pytest.raises(CratekitError) as excinfo:
        read_meta(trapped, cfg=cfg)
    assert excinfo.value.cause.reason == "intake-staging-refused"


def test_placement_uses_taxonomy_ids_not_display_names():
    placement = decide_placement({"genre": "", "energy": None}, taxonomy.default_taxonomy())
    assert placement is not None
    tree, bucket, sub = placement
    assert tree == "genre_energy"
    assert bucket
    assert sub
    assert " " not in tree
    assert "INBOX" not in (tree, bucket, sub)
