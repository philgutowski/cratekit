"""The container-correct tag writer, proved per container against real audio.

A tag write changes the tags and nothing else, in four layers, since a corrupted
AIFF keeps its size: the decoded samples hash the same (ffmpeg); the container
parses with a sane duration; the magic bytes are untouched; and without ffmpeg,
FLAC's STREAMINFO MD5 and the chunk containers' payload hashed from the file.
Fixtures are synthesized silence. A missing ffmpeg fails rather than skips.
"""

from __future__ import annotations

import hashlib
import shutil
import struct
import subprocess
from pathlib import Path

import pytest

from cratekit.core.tags import (
    FIELDS,
    Dialect,
    UnsupportedContainer,
    dialect_of,
    read_energy_from_file,
    read_genre_from_file,
    read_tag,
    read_tags,
    read_vox_from_file,
    read_voxgender_from_file,
    write_genre,
    write_tags,
)
from tests._containers import require_ffmpeg, synth_container

# Every container the writer claims, .m4a and .ogg included.
CONTAINERS = [".flac", ".aiff", ".wav", ".mp3", ".m4a", ".ogg"]

# Every writable field at once, so a writer clobbering an earlier frame is caught.
ALL_FIELDS = {
    "title": "01A - 124 - Probe Title",
    "artist": "Probe Artist",
    "initialkey": "01A",
    "genre": "Test Genre",
    "energylevel": 7,
    "inizio": "1.234",
    "voxlevel": 55,
    "voxgender": "F",
    "voxgenderconf": 80,
    "isrc": "ZZ0000000001",
    "album": "Probe Album",
    "date": "2021-03-05",
    "albumartist": "Probe Album Artist",
    "label": "Probe Label",
    "copyright": "\u2117 2021 Probe Label",
    "driftlevel": "4.4",
    "drift": "variable",
    "secondgenre": "Probe Second Genre",
    "analyzed": "1",
}


# Moved to tests/_containers.py; re-bound here for the suites that import them.
_require_ffmpeg = require_ffmpeg
_synth = synth_container


@pytest.fixture(scope="module")
def _pristine(tmp_path_factory):
    """Each container synthesized once per module; every test writes on its own copy."""
    made: dict[str, Path] = {}

    def get(suffix: str) -> Path:
        if suffix not in made:
            made[suffix] = _synth(tmp_path_factory.mktemp("pristine"), suffix)
        return made[suffix]

    return get


@pytest.fixture
def container(tmp_path, _pristine):
    """A fresh real container in this test's own directory."""
    def make(suffix: str) -> Path:
        path = tmp_path / f"probe{suffix}"
        shutil.copyfile(_pristine(suffix), path)
        return path

    return make


def _decoded_md5(path: Path) -> str:
    """MD5 of the DECODED sample stream, which is the thing that must not change."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-f", "md5", "-"],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _payload_chunk_digest(path: Path) -> str | None:
    """A RIFF or FORM container's payload chunk hashed with no decoder, None if not chunk based."""
    data = path.read_bytes()
    if data[:4] == b"RIFF":
        wanted, big_endian = b"data", False
    elif data[:4] == b"FORM":
        wanted, big_endian = b"SSND", True
    else:
        return None

    offset = 12  # magic, size, form type
    order = ">I" if big_endian else "<I"
    while offset + 8 <= len(data):
        name = data[offset:offset + 4]
        (size,) = struct.unpack(order, data[offset + 4:offset + 8])
        body = data[offset + 8:offset + 8 + size]
        if name == wanted:
            return hashlib.md5(body).hexdigest()
        offset += 8 + size + (size % 2)  # chunk bodies are word-aligned
    return None


# The audio-safety proof, per container


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_tag_write_leaves_the_decoded_audio_unchanged(container, suffix):
    import mutagen

    path = container(suffix)
    before_stream = _decoded_md5(path)
    before_payload = _payload_chunk_digest(path)
    before_bytes = path.read_bytes()

    assert write_tags(path, ALL_FIELDS) is True

    handle = mutagen.File(path)
    assert handle is not None, "the file no longer parses as its own container"
    assert handle.info.length > 0.5, "the container's duration was damaged"
    assert _decoded_md5(path) == before_stream
    assert _payload_chunk_digest(path) == before_payload
    assert path.read_bytes() != before_bytes, (
        "the file did not change at all, so this test proved nothing about a write"
    )


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_every_field_survives_the_round_trip(container, suffix):
    """Writer and reader closed against each other through the production readers."""
    path = container(suffix)
    assert write_tags(path, ALL_FIELDS) is True
    assert read_energy_from_file(path) == 7
    assert read_genre_from_file(path) == "Test Genre"
    assert read_vox_from_file(path) == 55
    assert read_voxgender_from_file(path) == "F"
    for field, value in ALL_FIELDS.items():
        assert read_tag(path, field) == str(value), f"{field} lost in {suffix}"


@pytest.mark.parametrize("suffix,magic", [(".aiff", b"FORM"), (".wav", b"RIFF")])
def test_a_chunk_container_never_receives_a_bare_id3_stream(container, suffix, magic):
    """The incident: an ID3 block at offset 0 shifts a byte-addressed chunk table for good."""
    path = container(suffix)
    assert write_tags(path, ALL_FIELDS) is True
    assert path.read_bytes()[:4] == magic


def test_a_real_mp3_does_receive_a_bare_id3_stream(container):
    """The positive control: a writer that never wrote ID3 would pass the test above."""
    path = container(".mp3")
    assert write_genre(path, "Test Genre") is True
    assert read_genre_from_file(path) == "Test Genre"
    assert path.read_bytes()[:3] == b"ID3"


def test_mp4_never_receives_an_id3_header(container):
    """An ID3 header before the moov atom breaks it."""
    path = container(".m4a")
    assert write_tags(path, ALL_FIELDS) is True
    assert path.read_bytes()[:3] != b"ID3"
    assert path.read_bytes()[4:8] == b"ftyp"


def test_the_flac_embedded_audio_checksum_is_unchanged(container):
    """FLAC's own opinion, which does not go through ffmpeg at all."""
    from mutagen.flac import FLAC
    path = container(".flac")
    before = FLAC(path).info.md5_signature
    assert write_tags(path, ALL_FIELDS) is True
    assert FLAC(path).info.md5_signature == before


# R17: there is no path from this module to a tempo frame


def test_the_round_trip_probe_covers_every_declared_field():
    """``ALL_FIELDS`` is hand written for shape, so its coverage is checked against the table."""
    missing = set(FIELDS) - set(ALL_FIELDS)
    assert not missing, (
        f"fields declared in FIELDS but never round-tripped: {sorted(missing)}. "
        f"Add a value of the right shape to ALL_FIELDS; a field nobody writes in "
        f"the probe is a field whose container mapping is untested."
    )
    assert not set(ALL_FIELDS) - set(FIELDS)


def test_tempo_is_not_a_writable_field():
    """Structural, not conventional. There is no key and no frame to reach."""
    assert "bpm" not in FIELDS
    assert not any(spec.id3 == "TBPM" for spec in FIELDS.values())
    assert not any("bpm" in spec.vorbis.lower() for spec in FIELDS.values())
    assert not any("bpm" in spec.mp4.lower() for spec in FIELDS.values())


def test_writing_a_tempo_field_raises_rather_than_returning_false(container):
    """A raise, so a beat grid write is never filed as an ordinary per-file failure."""
    path = container(".flac")
    with pytest.raises(ValueError, match="unknown tag fields"):
        write_tags(path, {"bpm": 124})


def test_the_writable_field_set_is_a_module_constant_not_configuration():
    """R17: a configurable field set would reopen the beat grid hole, so it is a literal."""
    import ast

    import cratekit.core.tags as tags

    tree = ast.parse(Path(tags.__file__).read_text())
    assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "FIELDS"
    ]
    assert len(assignments) == 1, "FIELDS must be assigned exactly once, in the module body"
    assert isinstance(assignments[0].value, ast.Dict), "FIELDS must be a literal table"

    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not any("config" in name for name in imported), (
        f"the tag field set must not be derived from configuration; imports: {imported}"
    )


# Dispatch, refusal, and the reader/writer agreement that S5 exists to force


@pytest.mark.parametrize(
    "suffix, dialect",
    [
        (".flac", Dialect.VORBIS), (".ogg", Dialect.VORBIS), (".opus", Dialect.VORBIS),
        (".m4a", Dialect.MP4), (".mp4", Dialect.MP4), (".m4b", Dialect.MP4),
        (".wav", Dialect.ID3), (".aiff", Dialect.ID3), (".aif", Dialect.ID3),
        (".aifc", Dialect.ID3), (".mp3", Dialect.ID3),
    ],
)
def test_each_container_is_classified_once(suffix, dialect):
    """One classification, consulted by both the reader and the writer."""
    assert dialect_of(suffix) is dialect


def test_an_unknown_container_is_refused_rather_than_guessed():
    """Refusing costs a failed write; guessing a bare ID3 stream costs a file."""
    with pytest.raises(UnsupportedContainer):
        dialect_of(".wma")


def test_reading_an_unknown_container_returns_none_rather_than_raising(tmp_path):
    """Asymmetric with the writer: a read damages nothing, so a stray file reads as no tags."""
    stray = tmp_path / "notes.txt"
    stray.write_text("not audio")
    assert read_tag(stray, "genre") is None


def test_a_none_value_is_skipped_not_written_as_empty(container):
    """Callers pass everything they might have detected, including what they did not."""
    path = container(".flac")
    assert write_tags(path, {"energylevel": None, "genre": "Test Genre"}) is True
    assert read_energy_from_file(path) is None
    assert read_genre_from_file(path) == "Test Genre"


def test_a_write_to_a_missing_file_returns_false(tmp_path):
    """One bad file must not abort a batch of several thousand."""
    assert write_tags(tmp_path / "gone.flac", {"genre": "Test Genre"}) is False


def test_reading_an_unwritable_field_name_raises():
    """A typo in a field name is a bug, and a silent None would hide it."""
    with pytest.raises(ValueError, match="unknown tag field"):
        read_tag(Path("x.flac"), "bpm")


def test_reading_a_file_that_is_not_there_returns_none(tmp_path):
    """Safe only downstream of the mount precondition."""
    assert read_genre_from_file(tmp_path / "gone.flac") is None


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_one_open_reads_every_field_the_way_the_one_field_reader_does(container, suffix):
    """The index's one open reader answers what ``read_tag`` does, absent fields included."""
    path = container(suffix)
    assert write_tags(path, {"artist": "Probe Artist", "title": "01A - 124 - Probe Title",
                             "isrc": "ZZ0000000001"})
    fields = ("artist", "title", "initialkey", "isrc")
    # Against the values written: read_tag is now one field of the reader under test.
    assert read_tags(path, fields) == {
        "artist": "Probe Artist",
        "title": "01A - 124 - Probe Title",
        "initialkey": None,
        "isrc": "ZZ0000000001",
    }
    assert read_tag(path, "isrc") == "ZZ0000000001"


def test_one_open_over_an_unknown_field_raises_rather_than_answering_none():
    with pytest.raises(ValueError, match="unknown tag field"):
        read_tags(Path("probe.flac"), ("artist", "tempo"))


def test_one_open_over_a_missing_file_answers_every_field_absent(tmp_path):
    assert read_tags(tmp_path / "gone.flac", ("artist", "isrc")) == {"artist": None, "isrc": None}


@pytest.mark.parametrize("suffix", [".aiff", ".mp3"])
def test_an_isrc_another_tagger_wrote_is_read_from_the_standard_frame(container, suffix):
    """R-355: the round trip cannot pin the frame; another tagger writes ``TSRC``."""
    import mutagen
    import mutagen.id3 as id3
    path = container(suffix)
    handle = mutagen.File(path)
    if handle.tags is None:
        handle.add_tags()
    handle.tags.add(id3.TSRC(encoding=3, text=["ZZX9A2600042"]))
    handle.save()
    assert read_tag(path, "isrc") == "ZZX9A2600042"


@pytest.mark.parametrize("suffix", [".mp3", ".aiff", ".wav"])
def test_clearing_a_file_with_no_tag_block_writes_nothing(container, suffix):
    """U301. An ID3 container with nothing to remove is left byte for byte."""
    from cratekit.core.tags import clear_tags, strip_tags
    path = container(suffix)
    assert strip_tags(path) is True
    before = path.read_bytes()
    assert clear_tags(path, ["genre", "title"]) is True
    assert path.read_bytes() == before


def test_the_analysed_mark_is_spelled_as_files_already_carry_it():
    """U343: ``analyze run``'s resume mark is on files from its first run, so its
    spelling in each dialect is pinned; a respelling reads every one as unmeasured."""
    spec = FIELDS["analyzed"]
    assert (spec.vorbis, spec.id3, spec.mp4) == (
        "cratekitanalyzed",
        "TXXX:CratekitAnalyzed",
        "----:com.apple.iTunes:CratekitAnalyzed",
    )
