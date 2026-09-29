"""R-740: a landed track's library Name carries the head its file carries.

Every landing used to write the bare title as the Name, because the head was
stripped from the title tag and rendered again from a key and no tempo, and the
tempo lives nowhere but that head. These land real FLAC files through
``landing.apply`` and read the Name the intake file wrote.
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import pytest

from cratekit.core import config, tags
from cratekit.intake import landing, pipeline
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml

HEADED = "01A - 112 - Ain't Gonna Hurt Nobody"


@pytest.fixture
def cfg(tmp_path: Path) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    staging = tmp_path / "staging"
    staging.mkdir()
    data = valid_data(root)
    data["paths"] = {"download_staging": str(staging)}
    built = config.from_dict(data)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path: Path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


def _land(
    cfg: config.Config,
    silence: Path,
    tmp_path: Path,
    filename: str,
    *,
    batch: str = "2026-09-29_acquired",
    **fields: object,
) -> tuple[str, bytes, Path]:
    """Land one file, return its Name as written, the intake file, the target."""
    staged = Path(cfg.paths.download_staging) / filename
    shutil.copyfile(silence, staged)
    if fields:
        written: dict[str, object] = {
            "artist": "Probe",
            "genre": "Deep House",
            "energylevel": 7,
        }
        written.update(fields)
        assert tags.write_tags(staged, written) is True
    export = tmp_path / f"{batch}_fresh.xml"
    export.write_bytes(_fresh_xml())
    destination = Path(cfg.library.root) / f"{batch}_inboxed.xml"
    result = landing.apply(
        landing.plan(Path(cfg.paths.download_staging), cfg, batch),
        cfg=cfg,
        export=export,
        destination=destination,
    )
    assert len(result.placed) == 1
    body = destination.read_bytes()
    names = re.findall(rb'<TRACK TrackID="\d+" Name="([^"]*)"', body)
    assert len(names) == 1
    return html.unescape(names[0].decode()), body, result.moved[0].target


def _no_tempo(body: bytes) -> None:
    assert b"<TEMPO" not in body
    rows = re.findall(rb"<TRACK TrackID=[^>]*>", body)
    assert rows
    for row in rows:
        assert b'AverageBpm="0.00"' in row


def test_a_title_headed_file_with_no_tempo_elsewhere_lands_named_as_its_title(
    cfg, silence, tmp_path
):
    name, body, target = _land(
        cfg, silence, tmp_path, f"{HEADED}.flac", title=HEADED, initialkey="01A"
    )
    assert name == HEADED
    _no_tempo(body)
    # The file is not touched: the head was read as text, never written back.
    assert tags.read_tag(target, "title") == HEADED


def test_a_title_head_with_no_key_tag_still_lands_whole(cfg, silence, tmp_path):
    name, _, _ = _land(cfg, silence, tmp_path, "Body.flac", title="08A - 124 - Body")
    assert name == "08A - 124 - Body"


def test_the_title_head_wins_over_a_disagreeing_key_tag(cfg, silence, tmp_path):
    """The Name is what Reload Tags would read, so it is the title tag's head."""
    name, body, _ = _land(
        cfg, silence, tmp_path, "Body.flac", title="08A - 124 - Body", initialkey="3B"
    )
    assert name == "08A - 124 - Body"
    assert b'Tonality="3B"' in body


def test_a_file_headed_in_its_filename_only_carries_that_head(cfg, silence, tmp_path):
    name, body, _ = _land(
        cfg, silence, tmp_path, "05B - 98 - Probe - Body.flac", title="Body"
    )
    assert name == "05B - 98 - Body"
    _no_tempo(body)


def test_a_file_headed_nowhere_lands_bare_and_nothing_invents_a_tempo(
    cfg, silence, tmp_path
):
    name, body, _ = _land(
        cfg, silence, tmp_path, "Body.flac", title="Body", initialkey="08A"
    )
    assert name == "Body"
    _no_tempo(body)


def test_a_lossy_file_keeps_its_marker_on_all_three_surfaces(cfg, silence, tmp_path):
    headed = "08A - 124 - [MP3] Body"
    name, body, target = _land(cfg, silence, tmp_path, f"{headed}.flac", title=headed)
    assert target.stem == headed
    assert tags.read_tag(target, "title") == headed
    assert name == headed
    _no_tempo(body)


def test_a_second_landing_of_the_same_file_renders_the_same_name(
    cfg, silence, tmp_path
):
    """The landed file already carries its head on every surface, so landing it
    again must neither double the head nor lose it."""
    first, _, target = _land(
        cfg, silence, tmp_path, "Body.flac", title="08A - 124 - Body", initialkey="08A"
    )
    second, body, _ = _land(
        cfg, target, tmp_path, "08A - 124 - Body.flac", batch="2026-09-30_acquired"
    )
    assert second == first == "08A - 124 - Body"
    _no_tempo(body)


def test_intake_file_names_its_track_from_the_same_head(cfg, silence, tmp_path):
    """``intake file`` reaches the same ``read_meta`` through ``ingest_file``, so
    it carries the head the same way and writes no tempo either."""
    audio = Path(cfg.library.root) / f"{HEADED}.flac"
    shutil.copyfile(silence, audio)
    assert tags.write_tags(audio, {"title": HEADED, "genre": "Deep House"}) is True
    export = tmp_path / "fresh.xml"
    export.write_bytes(_fresh_xml())
    destination = Path(cfg.library.root) / "one_inboxed.xml"
    pipeline.ingest_file(audio, cfg=cfg, export=export, destination=destination)
    body = destination.read_bytes()
    names = re.findall(rb'<TRACK TrackID="\d+" Name="([^"]*)"', body)
    assert [html.unescape(n.decode()) for n in names] == [HEADED]
    _no_tempo(body)
