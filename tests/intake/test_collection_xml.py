"""U37: the COLLECTION TRACK emitter, KTD27 Locations, U22 stub refusal."""

from __future__ import annotations

import pytest

from cratekit.core import locations, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.intake.collection_xml import (
    GRIDLESS_AVERAGE_BPM,
    build_track_xml,
    is_stub_listing,
    splice_tracks,
)
from tests.test_no_beatgrid_ever import FORBIDDEN_TOKENS
from tests.xml_fixtures import _fresh_xml, _no_bare_lf

META = dict(
    bpm=124.0,
    energy=7,
    name="04A - 124 - Test Title",
    artist="Test Artist",
    album="Test Album",
    genre="Deep House",
    size_bytes=12345678,
    duration_s=321,
    bitrate_kbps=1000,
    sample_rate=44100,
    location="file://localhost/x.flac",
    tonality="4A",
    inizio=0.512,
)


def _xml(tid: int, added: str = "2026-01-01", **over) -> str:
    """One TRACK element for the probe metadata, ``over`` replacing its fields."""
    return build_track_xml(tid, {**META, **over}, added, declared=taxonomy.default_taxonomy())


def test_emitted_location_matches_rekordbox_encoding_for_space_and_bang(tmp_path):
    """KTD27: space becomes %20, ! stays literal, hex is lowercase."""
    path = tmp_path / "New Year with Trevor!" / "It's A Track.flac"
    path.parent.mkdir()
    path.write_bytes(b"x")
    synthesized = locations.location_url(path)
    xml = _xml(9, location=str(path))
    assert f'Location="{synthesized}"' in xml
    assert "%20" in xml
    assert "Trevor!" in xml
    assert "%21" not in xml
    assert "%c3" not in xml or "%C3" not in xml
    # A Fresh Export Location is carried through unmodified.
    inherited = "file://localhost/library/stale-volume/Already%20Here!.flac"
    assert f'Location="{inherited}"' in _xml(3, location=inherited)


def test_average_bpm_is_gridless_inizio_no_tempo_child_and_the_bytes_crlf():
    """The gridless constant even when a BPM is present; no bare LF."""
    xml = _xml(1, bpm=174.0, added="2026-08-17", energy=None, inizio=3.25)
    assert f'AverageBpm="{GRIDLESS_AVERAGE_BPM}"' in xml
    assert 'AverageBpm="174' not in xml
    for token in FORBIDDEN_TOKENS:
        assert token not in xml
    assert _no_bare_lf(xml.encode("utf-8"))


def test_a_u22_stub_listing_is_not_a_splice_target():
    stub = (
        b'<?xml version="1.0" encoding="UTF-8"?>\r\n<DJ_PLAYLISTS>\r\n  <COLLECTION>\r\n'
        b'    <TRACK Name="some-identity"/>\r\n</COLLECTION>\r\n</DJ_PLAYLISTS>\r\n'
    )
    assert is_stub_listing(stub)
    assert not is_stub_listing(_fresh_xml())
    with pytest.raises(CratekitError) as excinfo:
        splice_tracks(bytearray(stub), [_xml(1)])
    assert excinfo.value.cause.reason == "intake-export-is-stub"


def test_splice_into_a_fresh_export_bumps_entries_and_inserts_the_track():
    buf = bytearray(_fresh_xml())
    xml = _xml(900000001)
    splice_tracks(buf, [xml])
    out = bytes(buf)
    assert b'Entries="1"' in out
    assert b'TrackID="900000001"' in out
    assert b"<TEMPO" not in out
    assert _no_bare_lf(out)
