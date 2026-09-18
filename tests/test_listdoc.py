"""U68: the shared emitter's list document, read back by the product's own reader.

Every expected value here is a LITERAL taken from the fixture rows, never a value
``listdoc.document`` produced. A round trip checked against the emitter's own
output is X equals X: it passes whatever the emitter writes, as long as the
reader reads it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.acquire import listdoc, match
from cratekit.acquire.cli import frozen_tracks
from cratekit.acquire.listdoc import Provenance, Row
from cratekit.acquire.match_cli import read_list
from cratekit.core.cause import CratekitError

SOURCE = Provenance(source="playlists", source_ref="pl-9", year=2024)

#: Three provider rows, the second embedding its version in the title and the
#: third declaring it in its own field.
ROWS = (
    Row(ref="101", artist="Aurora Bloom", title="Sun Path", isrc="GBAAA2400001", key="8A"),
    Row(ref="202", artist="Nova Reef", title="Tide Line - Nightwave Remix"),
    Row(ref="303", artist="Mira Vale", title="Low Orbit", version="Extended Mix"),
)


def _write(tmp_path: Path, rows=ROWS, provenance=SOURCE, name="set") -> listdoc.Written:
    return listdoc.write(tmp_path, name, rows, provenance)


def test_the_list_round_trips_through_the_real_reader_and_the_download_freeze(tmp_path):
    written = _write(tmp_path)
    assert written.list_path == tmp_path / "set.list.json"
    assert written.listed == ("101", "202", "303")
    wanted = read_list(written.list_path)
    assert [w.ref for w in wanted] == ["101", "202", "303"]
    assert [(w.artist, w.title) for w in wanted] == [
        ("Aurora Bloom", "Sun Path"),
        ("Nova Reef", "Tide Line"),
        ("Mira Vale", "Low Orbit"),
    ]
    assert [w.key for w in wanted] == ["8A", None, None]
    assert [w.version_key for w in wanted] == ["", "nightwave remix", "extended mix"]
    assert frozen_tracks(wanted) == {
        "101": {"artist": "Aurora Bloom", "title": "Sun Path", "isrc": "GBAAA2400001"},
        "202": {"artist": "Nova Reef", "title": "Tide Line", "isrc": None},
        "303": {"artist": "Mira Vale", "title": "Low Orbit", "isrc": None},
    }


def test_the_document_carries_only_the_keys_the_reader_reads(tmp_path):
    written = _write(tmp_path)
    body = json.loads(written.list_path.read_text(encoding="utf-8"))
    assert set(body) == {"list", "origin", "tracks"}
    assert body["list"] == 1
    assert body["origin"] == "tidal"


def test_a_row_with_no_provider_id_is_unlisted_and_the_document_still_reads(tmp_path):
    orphan = Row(ref="  ", artist="Kite Shore", title="Unlisted")
    written = _write(tmp_path, rows=(ROWS[0], orphan, ROWS[1]))
    assert written.listed == ("101", "202")
    assert written.unlisted == (orphan,)
    assert [w.ref for w in read_list(written.list_path)] == ["101", "202"]


def test_a_duplicate_id_is_written_once_and_the_first_occurrence_wins(tmp_path):
    repeat = Row(ref="101", artist="Someone Else", title="Other Record")
    written = _write(tmp_path, rows=(ROWS[0], ROWS[1], repeat))
    assert written.listed == ("101", "202")
    wanted = read_list(written.list_path)
    assert [(w.ref, w.artist) for w in wanted] == [("101", "Aurora Bloom"), ("202", "Nova Reef")]
    rows = json.loads(written.manifest_path.read_text(encoding="utf-8"))["rows"]
    assert rows["101"]["artist"] == "Aurora Bloom"


def test_an_id_is_compared_stripped_because_the_reader_strips_it(tmp_path):
    padded = Row(ref=" 101 ", artist="Someone Else", title="Other Record")
    written = _write(tmp_path, rows=(ROWS[0], padded))
    assert written.listed == ("101",)


@pytest.mark.parametrize(
    ("title", "version", "token"),
    [
        ("Tide Line - Nightwave Remix", "", "nightwave remix"),
        ("Tide Line (Extended Mix)", "", "extended mix"),
        ("Tide Line", "Dub", "dub"),
    ],
)
def test_a_version_re_reads_to_the_same_token(tmp_path, title, version, token):
    row = Row(ref="202", artist="Nova Reef", title=title, version=version)
    (wanted,) = read_list(_write(tmp_path, rows=(row,)).list_path)
    assert wanted.title == "Tide Line"
    assert wanted.version_key == token


def test_an_existing_different_list_is_refused_and_left_alone(tmp_path):
    target = tmp_path / "set.list.json"
    target.write_text('{"list": 1, "origin": "tidal", "tracks": []}\n', encoding="utf-8")
    with pytest.raises(listdoc.ListDocRefused, match="already exists"):
        _write(tmp_path)
    assert target.read_text(encoding="utf-8") == '{"list": 1, "origin": "tidal", "tracks": []}\n'
    assert not (tmp_path / "set.manifest.json").exists()


def test_an_existing_different_manifest_is_refused_before_the_list_is_written(tmp_path):
    (tmp_path / "set.manifest.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(listdoc.ListDocRefused, match="already exists"):
        _write(tmp_path)
    assert not (tmp_path / "set.list.json").exists()


def test_writing_the_same_list_again_is_a_no_op(tmp_path):
    first = _write(tmp_path)
    before = (first.list_path.stat().st_mtime_ns, first.manifest_path.stat().st_mtime_ns)
    second = _write(tmp_path)
    assert second == first
    after = (first.list_path.stat().st_mtime_ns, first.manifest_path.stat().st_mtime_ns)
    assert after == before


def test_a_missing_half_of_the_pair_is_completed(tmp_path):
    first = _write(tmp_path)
    first.list_path.unlink()
    _write(tmp_path)
    assert [w.ref for w in read_list(first.list_path)] == ["101", "202", "303"]


def test_no_listable_row_writes_nothing_and_says_so(tmp_path):
    orphan = Row(ref="", artist="Kite Shore", title="Unlisted")
    written = _write(tmp_path, rows=(orphan,))
    assert written.list_path is None
    assert written.manifest_path is None
    assert written.listed == ()
    assert written.unlisted == (orphan,)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "broken",
    [
        Row(ref="404", artist="", title="Sun Path"),
        Row(ref="404", artist="Aurora Bloom", title="   "),
        Row(ref="404", artist="Aurora Bloom", title="(Extended)"),
    ],
    ids=["no-artist", "no-title", "only-a-version"],
)
def test_a_row_the_reader_would_refuse_is_refused_by_the_emitter(tmp_path, broken):
    with pytest.raises(listdoc.ListDocRefused) as refused:
        _write(tmp_path, rows=(ROWS[0], broken))
    assert refused.value.position == 2
    assert list(tmp_path.iterdir()) == []


def test_the_reader_does_refuse_the_whole_list_over_that_row(tmp_path):
    # What the emitter guard is FOR, measured on the reader rather than asserted.
    path = tmp_path / "hand.list.json"
    path.write_text(
        json.dumps(
            {
                "list": 1,
                "origin": "tidal",
                "tracks": [
                    {"id": "101", "title": "Sun Path", "artist": "Aurora Bloom"},
                    {"id": "404", "title": "Sun Path", "artist": ""},
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CratekitError):
        read_list(path)


@pytest.mark.parametrize("name", ["", " set", "a/b", "..", ".", "a\\b", "a\x00b"])
def test_a_name_that_is_not_one_plain_file_name_is_refused(tmp_path, name):
    with pytest.raises(listdoc.ListDocRefused):
        _write(tmp_path, name=name)
    assert list(tmp_path.iterdir()) == []


def test_the_manifest_records_each_ids_provenance(tmp_path):
    per_id = {
        "101": Provenance(source="labels", label_id="L1", label_name="Tidewater", year=2023, release_id="R7"),
        "202": Provenance(source="playlists", source_ref="pl-9"),
        "303": Provenance(source="favorites"),
    }
    written = _write(tmp_path, provenance=per_id)
    doc = json.loads(written.manifest_path.read_text(encoding="utf-8"))
    assert doc["manifest"] == 1
    assert doc["list"] == "set.list.json"
    assert list(doc["rows"]) == ["101", "202", "303"]
    assert doc["rows"]["101"] == {
        "source": "labels",
        "source_ref": None,
        "label_id": "L1",
        "label_name": "Tidewater",
        "year": 2023,
        "release_id": "R7",
        "artist": "Aurora Bloom",
        "title": "Sun Path",
        "version": "",
        "isrc": "GBAAA2400001",
    }
    assert doc["rows"]["303"]["version"] == "Extended Mix"


def test_a_listed_id_with_no_provenance_refuses_and_writes_nothing(tmp_path):
    with pytest.raises(listdoc.ListDocRefused, match="303"):
        _write(tmp_path, provenance={"101": SOURCE, "202": SOURCE})
    assert list(tmp_path.iterdir()) == []


def test_a_provenance_naming_no_source_refuses(tmp_path):
    with pytest.raises(listdoc.ListDocRefused, match="no source"):
        _write(tmp_path, provenance=Provenance(source=" "))


# ---------------------------------------------------------------------------
# rows_of
# ---------------------------------------------------------------------------


def _tidal(**row) -> match.Wanted:
    return match.read_row(row, origin=match.TIDAL, position=1)


def test_frozen_tracks_become_rows_that_freeze_back_identically(tmp_path):
    frozen = {
        "101": {"artist": "Aurora Bloom", "title": "Sun Path", "isrc": "GBAAA2400001"},
        "202": {"artist": "Nova Reef", "title": "Tide Line", "isrc": None},
    }
    written = _write(tmp_path, rows=listdoc.rows_of(frozen))
    assert frozen_tracks(read_list(written.list_path)) == {
        "101": {"artist": "Aurora Bloom", "title": "Sun Path", "isrc": "GBAAA2400001"},
        "202": {"artist": "Nova Reef", "title": "Tide Line", "isrc": None},
    }


def test_a_read_track_keeps_its_featured_credit_through_the_round_trip(tmp_path):
    wanted = _tidal(id="505", title="Sun Path (feat. Mira) (Extended Mix)", artist="Aurora Bloom")
    (again,) = read_list(_write(tmp_path, rows=listdoc.rows_of([wanted])).list_path)
    assert again.spelled == "Sun Path (feat. Mira) (Extended Mix)"
    assert again.title == "Sun Path"
    assert again.version_key == "extended mix"


@pytest.mark.parametrize(
    "raw",
    ["Sun Path (Extended)", "Sun Path (feat. Mira) (Extended)"],
)
def test_a_declared_version_beside_an_embedded_one_round_trips_whole(tmp_path, raw):
    # Spelled together, this re-reads as "extended dub", so the source's own
    # spelling is not written. The split title is not written either, because it
    # has lost "(Extended)" and the credit: the raw title and the declared
    # version are, which re-read to the same addressed title.
    wanted = _tidal(id="606", title=raw, version="Dub", artist="Aurora Bloom")
    (row,) = listdoc.rows_of([wanted])
    assert (row.title, row.version) == (raw, "Dub")
    (again,) = read_list(_write(tmp_path, rows=(row,)).list_path)
    assert again.version_key == "dub"
    assert again.listed == f"{raw} (Dub)"


def test_a_hand_built_track_with_no_spelling_writes_its_title_and_version(tmp_path):
    wanted = match.Wanted(artist="Aurora Bloom", title="Sun Path", version="Dub", origin=match.TIDAL, ref="707")
    (row,) = listdoc.rows_of([wanted])
    assert (row.title, row.version) == ("Sun Path", "Dub")


def test_a_frozen_mapping_carries_no_version_so_none_is_written(tmp_path):
    # Recorded, not endorsed: the freeze dropped it. See rows_of's docstring.
    (row,) = listdoc.rows_of({"808": {"artist": "Aurora Bloom", "title": "Sun Path", "isrc": None}})
    (again,) = read_list(_write(tmp_path, rows=(row,)).list_path)
    assert again.version == ""


def test_a_track_from_another_service_is_unlisted_not_written_as_a_provider_id(tmp_path):
    other = match.read_row(
        {"id": "sp-77", "name": "Sun Path", "artists": [{"name": "Aurora Bloom"}]},
        origin=match.SPOTIFY,
        position=1,
    )
    written = _write(tmp_path, rows=listdoc.rows_of([_tidal(id="101", title="Sun Path", artist="A"), other]))
    assert written.listed == ("101",)
    assert [row.ref for row in written.unlisted] == [""]
    assert written.unlisted[0].artist == "Aurora Bloom"
