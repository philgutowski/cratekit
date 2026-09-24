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


def _meta(**over):
    meta = dict(
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
    meta.update(over)
    return meta


def test_emitted_location_matches_rekordbox_encoding_for_space_and_bang(tmp_path):
    """KTD27: space becomes %20, ! stays literal, hex is lowercase."""
    path = tmp_path / "New Year with Trevor!" / "It's A Track.flac"
    path.parent.mkdir()
    path.write_bytes(b"x")
    synthesized = locations.location_url(path)
    xml = build_track_xml(9, _meta(location=str(path)), "2026-01-01", declared=taxonomy.default_taxonomy())
    assert f'Location="{synthesized}"' in xml
    assert "%20" in xml
    assert "Trevor!" in xml
    assert "%21" not in xml
    assert "%c3" not in xml or "%C3" not in xml


def test_an_inherited_location_is_not_reencoded():
    """A Fresh Export Location is carried through unmodified."""
    inherited = "file://localhost/library/stale-volume/Already%20Here!.flac"
    xml = build_track_xml(3, _meta(location=inherited), "2026-01-01", declared=taxonomy.default_taxonomy())
    assert f'Location="{inherited}"' in xml


def test_average_bpm_is_the_gridless_constant_even_when_bpm_is_present():
    xml = build_track_xml(1, _meta(bpm=174.0), "2026-08-17", declared=taxonomy.default_taxonomy())
    assert f'AverageBpm="{GRIDLESS_AVERAGE_BPM}"' in xml
    assert "174" not in xml.split("Name=")[0] or 'AverageBpm="174' not in xml
    assert 'AverageBpm="174' not in xml


def test_inizio_does_not_become_a_tempo_child():
    xml = build_track_xml(2, _meta(energy=None, inizio=3.25), "2026-01-01", declared=taxonomy.default_taxonomy())
    for token in FORBIDDEN_TOKENS:
        assert token not in xml


def test_emitted_bytes_use_crlf_and_no_bare_lf():
    xml = build_track_xml(4, _meta(), "2026-01-01", declared=taxonomy.default_taxonomy())
    assert _no_bare_lf(xml.encode("utf-8"))


def test_a_u22_stub_listing_is_not_a_splice_target():
    stub = (
        b'<?xml version="1.0" encoding="UTF-8"?>\r\n'
        b"<DJ_PLAYLISTS>\r\n"
        b"  <COLLECTION>\r\n"
        b'    <TRACK Name="some-identity"/>\r\n'
        b"</COLLECTION>\r\n"
        b"</DJ_PLAYLISTS>\r\n"
    )
    assert is_stub_listing(stub)
    assert not is_stub_listing(_fresh_xml())
    with pytest.raises(CratekitError) as excinfo:
        splice_tracks(bytearray(stub), [build_track_xml(1, _meta(), "2026-01-01", declared=taxonomy.default_taxonomy())])
    assert excinfo.value.cause.reason == "intake-export-is-stub"


def test_splice_into_a_fresh_export_bumps_entries_and_inserts_the_track():
    buf = bytearray(_fresh_xml())
    xml = build_track_xml(900000001, _meta(), "2026-01-01", declared=taxonomy.default_taxonomy())
    splice_tracks(buf, [xml])
    out = bytes(buf)
    assert b'Entries="1"' in out
    assert b'TrackID="900000001"' in out
    assert b"<TEMPO" not in out
    assert _no_bare_lf(out)
