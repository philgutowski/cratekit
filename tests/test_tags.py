"""The container-correct tag writer, proved per container against real audio.

The claim under test is the strongest one this repository makes about user data:
a tag write changes the tags and changes nothing else. Not "should not", not
"was not observed to". The proof has four independent layers, because the failure
this guards against does not look like a failure. A corrupted AIFF is still a
file, still the right size, still in the right folder. It just does not decode
any more, and nothing said so at the time.

The four layers, and why one of them is not enough:

1. **The decoded audio stream hashes identically.** ffmpeg decodes the file to
   raw samples before and after the write and the two hashes must match. Hashing
   the FILE would be useless, because the file legitimately changes: that is the
   tag. Hashing the SAMPLES is the actual property.
2. **The container still parses as itself, with a sane duration.** A corrupted
   AIFF fails here before the hash is even reached, which turns an opaque hash
   mismatch into an obvious structural failure.
3. **The magic bytes are untouched.** The direct regression test for the actual
   incident: after a write, an AIFF still opens with ``FORM`` and a WAV with
   ``RIFF``, never ``ID3``. This is the assertion that would have caught it.
4. **The container's own embedded checksum.** FLAC carries an MD5 of its
   decoded audio in STREAMINFO, and for the chunk containers the audio payload
   chunk is hashed straight out of the file with no decoder involved. Both are
   second opinions that do not go through ffmpeg, so a bug in the ffmpeg
   invocation cannot make layer 1 vacuously pass.

Fixtures are SYNTHESIZED, one second of silence per container. Never sampled
from a real library: a test that needs the user's music is a test that only runs
on one machine.

ON ffmpeg BEING REQUIRED RATHER THAN OPTIONAL. The source suite skipped this
whole module when ffmpeg was absent. Cratekit's rule is that a skip is a
countdown registered in ``tests/_pending.py``, not something a test file decides
for itself, and an external binary does not fit that register. So a missing
ffmpeg FAILS here with a message naming the fix. The workflow installs it as an
explicit step, and the alternative is the one outcome the register exists to
prevent: the proof that audio is never damaged, silently not running.
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
    read_vox_from_file,
    read_voxgender_from_file,
    write_genre,
    write_tags,
)

# Every container the writer claims to handle. All six, not the four the plan's
# scenario names: dropping .m4a drops the only test that MP4 never receives an
# ID3 tag, and dropping .ogg drops the generic Vorbis branch entirely.
CONTAINERS = [".flac", ".aiff", ".wav", ".mp3", ".m4a", ".ogg"]

# Every writable field at once. Writing one field at a time would never catch a
# writer that clobbers a previously written frame.
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
}


def _require_ffmpeg() -> str:
    binary = shutil.which("ffmpeg")
    if binary is None:
        pytest.fail(
            "ffmpeg is required to prove that a tag write leaves audio bytes "
            "unchanged. Install it (the CI workflow does this in a dedicated "
            "step). This fails rather than skips because a skipped audio-safety "
            "proof is indistinguishable from a passing one in every summary "
            "anybody reads."
        )
    return binary


def _synth(tmp_path: Path, suffix: str) -> Path:
    """One second of silence in the given container."""
    _require_ffmpeg()
    out = tmp_path / f"probe{suffix}"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", "1", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), (
        f"ffmpeg could not encode {suffix}, so this container's audio-safety "
        f"proof cannot run: {proc.stderr[-400:]}"
    )
    return out


def _decoded_md5(path: Path) -> str:
    """MD5 of the DECODED sample stream, which is the thing that must not change."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-f", "md5", "-"],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _payload_chunk_digest(path: Path) -> str | None:
    """Hash the audio payload chunk of a RIFF or FORM container, with no decoder.

    A decoder-free second opinion aimed squarely at the corruption class: it can
    only produce a digest if the chunk table still parses AND the payload is
    where the table says it is. A bare ID3 stream written at offset 0 shifts
    everything, so this returns None or a different digest, whichever comes
    first. Returns None for containers that are not chunk-based.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The audio-safety proof, per container
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("suffix", CONTAINERS)
def test_a_tag_write_leaves_the_decoded_audio_unchanged(tmp_path, suffix):
    """The plan's scenario, run over every container rather than the named four."""
    import mutagen

    path = _synth(tmp_path, suffix)
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
def test_every_field_survives_the_round_trip(tmp_path, suffix):
    """Writer and reader closed against each other, in every container.

    Reading back through the production readers rather than through mutagen
    directly is the point. A reader that looked up its own keys would agree with
    a writer that used different ones, and the field would be silently absent in
    exactly one container.
    """
    path = _synth(tmp_path, suffix)
    assert write_tags(path, ALL_FIELDS) is True

    assert read_energy_from_file(path) == 7
    assert read_genre_from_file(path) == "Test Genre"
    assert read_vox_from_file(path) == 55
    assert read_voxgender_from_file(path) == "F"
    for field, value in ALL_FIELDS.items():
        assert read_tag(path, field) == str(value), f"{field} lost in {suffix}"


def test_aiff_never_receives_a_bare_id3_stream(tmp_path):
    """The incident, as a single assertion.

    An AIFF opens with ``FORM`` and its chunk table is byte-offset addressed from
    there. A bare ID3 writer puts an ID3 block at offset 0 and shifts everything,
    so the first bytes become ``ID3``, the FORM header moves, and the chunk sizes
    describe a layout that no longer exists. Stripping the tag afterwards does
    not recover the audio, because the offsets are gone.
    """
    path = _synth(tmp_path, ".aiff")
    assert write_tags(path, ALL_FIELDS) is True
    assert path.read_bytes()[:4] == b"FORM"


def test_wav_never_receives_a_bare_id3_stream(tmp_path):
    path = _synth(tmp_path, ".wav")
    assert write_tags(path, ALL_FIELDS) is True
    assert path.read_bytes()[:4] == b"RIFF"


def test_a_real_mp3_does_receive_a_bare_id3_stream(tmp_path):
    """The positive control, without which the two tests above pass vacuously.

    A writer that never wrote ID3 anywhere would satisfy both. ``.mp3`` is the
    one container whose ID3 genuinely is a stream prefix, so it must still get
    one.
    """
    path = _synth(tmp_path, ".mp3")
    assert write_genre(path, "Test Genre") is True
    assert read_genre_from_file(path) == "Test Genre"
    assert path.read_bytes()[:3] == b"ID3"


def test_mp4_never_receives_an_id3_header(tmp_path):
    """Same rule, different format. An ID3 header before the moov atom breaks it."""
    path = _synth(tmp_path, ".m4a")
    assert write_tags(path, ALL_FIELDS) is True
    assert path.read_bytes()[:3] != b"ID3"
    assert path.read_bytes()[4:8] == b"ftyp"


def test_the_flac_embedded_audio_checksum_is_unchanged(tmp_path):
    """FLAC's own opinion, which does not go through ffmpeg at all."""
    from mutagen.flac import FLAC

    path = _synth(tmp_path, ".flac")
    before = FLAC(path).info.md5_signature
    assert write_tags(path, ALL_FIELDS) is True
    assert FLAC(path).info.md5_signature == before


# ═══════════════════════════════════════════════════════════════════════════
# R17: there is no path from this module to a tempo frame
# ═══════════════════════════════════════════════════════════════════════════


def test_the_round_trip_probe_covers_every_declared_field():
    """``ALL_FIELDS`` says "every writable field", so it must be checked against
    the table rather than trusted.

    It is hand-written on purpose: each field needs a value of the right SHAPE,
    which cannot be derived. What can be derived is its COVERAGE, and without
    this the next field added to the table would round-trip in no container and
    the suite would stay green, which is the state this file was already in.
    """
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


def test_writing_a_tempo_field_raises_rather_than_returning_false(tmp_path):
    """It raises so a caller cannot treat it as an ordinary per-file failure.

    Returning False would put "this file was locked" and "you tried to write a
    beat grid" in the same bucket, and the second one is a bug in the caller that
    must be fixed rather than logged.
    """
    path = _synth(tmp_path, ".flac")
    with pytest.raises(ValueError, match="unknown tag fields"):
        write_tags(path, {"bpm": 124})


def test_the_writable_field_set_is_a_module_constant_not_configuration():
    """R19 makes taxonomy configurable. R17 makes this one table not.

    A user-definable field set would reopen the beat-grid hole through the
    config file, which is a longer road to the same wrong grid. Two structural
    assertions rather than a prose one: the table is a literal in the module
    body, and the module imports no configuration to build it from.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Dispatch, refusal, and the reader/writer agreement that S5 exists to force
# ═══════════════════════════════════════════════════════════════════════════


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
    """One classification, consulted by both the reader and the writer.

    This is the seam decision made testable: reader and writer cannot disagree
    about where a field lives, because they ask the same function.
    """
    assert dialect_of(suffix) is dialect


def test_an_unknown_container_is_refused_rather_than_guessed():
    """The ported writer treated anything unrecognized as a bare ID3 stream.

    That is the corruption path aimed at whichever container nobody had thought
    about yet. Refusing costs a failed write; guessing costs a file.
    """
    with pytest.raises(UnsupportedContainer):
        dialect_of(".wma")


def test_reading_an_unknown_container_returns_none_rather_than_raising(tmp_path):
    """Deliberately asymmetric with the writer, because the risks are asymmetric.

    Reading cannot damage anything, and a sweep across a directory holding one
    stray file should report no tags rather than abort the run.
    """
    stray = tmp_path / "notes.txt"
    stray.write_text("not audio")
    assert read_tag(stray, "genre") is None


def test_a_none_value_is_skipped_not_written_as_empty(tmp_path):
    """Callers pass everything they might have detected, including what they did not."""
    path = _synth(tmp_path, ".flac")
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
    """The degrade the mount precondition exists to make safe.

    Correct for one damaged file and catastrophic for a whole library at once,
    which is why this answer is only acceptable downstream of the volume check.
    """
    assert read_genre_from_file(tmp_path / "gone.flac") is None
