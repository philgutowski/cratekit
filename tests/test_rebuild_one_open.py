"""U250: a derivation reads each library file through one container open.

Proved by counting ``mutagen.File`` calls against the three single field readers. D1 applies.
"""

from __future__ import annotations

from pathlib import Path

import mutagen
import pytest

from cratekit.core import tags
from cratekit.write import rebuild
from tests._containers import synth_container

# The tag suites' own container matrix, every dialect the reader dispatches on.
CONTAINERS = [".flac", ".aiff", ".wav", ".mp3", ".m4a", ".ogg"]


def _field_wise(path: Path) -> rebuild.Truth:
    """The reading as the three single field readers give it, today's answer."""
    return rebuild.Truth(
        location=str(path),
        genre=tags.read_genre_from_file(path),
        energy=tags.read_energy_from_file(path),
        voxlevel=tags.read_vox_from_file(path),
    )


@pytest.fixture
def opens(monkeypatch) -> list[Path]:
    """Every ``mutagen.File`` call, by path, while the real reader still runs."""
    seen: list[Path] = []
    real = mutagen.File

    def counting(target, *args, **kwargs):
        seen.append(Path(target))
        return real(target, *args, **kwargs)

    monkeypatch.setattr(mutagen, "File", counting)
    return seen


#: One second of silence per container, encoded once per process and copied.
_SILENCE: dict[str, bytes] = {}


def _tagged(folder: Path, suffix: str, name: str, fields: dict[str, object]) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{name}{suffix}"
    if suffix in _SILENCE:
        target.write_bytes(_SILENCE[suffix])
    else:
        synth_container(folder, suffix).rename(target)
        _SILENCE[suffix] = target.read_bytes()
    if fields:
        assert tags.write_tags(target, fields)
    return target


# The tag sets each container is read under, from whole numbers to no tags at all.
READINGS = {
    "numeric": {"genre": "Deep House", "energylevel": 7, "voxlevel": 55},
    "energy-word": {"genre": "Techno", "energylevel": "high", "voxlevel": 20},
    "vox-word": {"genre": "Disco", "energylevel": 4, "voxlevel": "loud"},
    "padded": {"genre": " Garage ", "energylevel": " 6 ", "voxlevel": " 40 "},
    "decimal": {"genre": "Electro", "energylevel": "7.0", "voxlevel": "0.5"},
    "genre-only": {"genre": "Ambient"},
    "untagged": {},
}


@pytest.mark.parametrize("suffix", CONTAINERS)
@pytest.mark.parametrize("case", sorted(READINGS))
def test_one_open_reads_what_the_three_readers_read(tmp_path, opens, suffix, case):
    """Every container and every tag shape: one open, and today's exact reading."""
    path = _tagged(tmp_path / "lib", suffix, case, READINGS[case])
    expected = _field_wise(path)
    opens.clear()

    truth = rebuild.read_truth(path)

    assert opens == [path], f"{suffix} {case}: read_truth opened {opens!r}"
    assert truth == expected
    assert truth.location == str(path)


def test_a_numeric_reading_converts_the_way_the_single_readers_convert(tmp_path):
    """Guard against an equality that holds only because both sides read None."""
    for suffix, case, name, genre, energy, voxlevel in (
        (".flac", "numeric", "numeric", "Deep House", 7, 55),
        (".mp3", "energy-word", "word", "Techno", None, 20),
        (".m4a", "vox-word", "vox", "Disco", 4, None),
        (".aiff", "padded", "padded", "Garage", 6, 40),
        (".ogg", "decimal", "decimal", "Electro", None, None),
    ):
        path = _tagged(tmp_path / "lib", suffix, name, READINGS[case])
        if case == "decimal":
            # Not a whole number, for the energy reader and read_truth alike.
            assert tags.read_energy_from_file(path) is None
        assert rebuild.read_truth(path) == rebuild.Truth(
            location=str(path), genre=genre, energy=energy, voxlevel=voxlevel
        ), case


def test_an_undecodable_field_reads_none_and_its_neighbours_still_read(tmp_path, opens):
    """An undecodable MP4 freeform atom reads None alone; the genre beside it survives."""
    from mutagen.mp4 import MP4, MP4FreeForm

    path = _tagged(tmp_path / "lib", ".m4a", "broken", {"genre": "House", "voxlevel": 30})
    handle = MP4(path)
    handle[tags.FIELDS["energylevel"].mp4] = [MP4FreeForm(b"\xff\xfe\xfd")]
    handle.save()
    assert tags.read_tags(path, ("energylevel",))["energylevel"] is None
    expected = _field_wise(path)
    opens.clear()

    truth = rebuild.read_truth(path)

    assert opens == [path]
    assert truth == expected == rebuild.Truth(
        location=str(path), genre="House", energy=None, voxlevel=30
    )


@pytest.mark.parametrize(
    "name, content",
    [
        ("empty.flac", b""),
        ("garbage.mp3", b"this is not audio at all " * 40),
        ("garbage.aiff", b"FORM\x00\x00\x00\x04AIFX"),
        ("garbage.m4a", b"\x00\x00\x00\x08junk" * 10),
        ("truncated.wav", b"RIFF\x24\x00\x00\x00WAVEfmt "),
    ],
)
def test_a_file_no_open_can_read_reads_three_absent_values(tmp_path, opens, name, content):
    """An empty or unreadable file never raises and reads as nothing, as today."""
    path = tmp_path / name
    path.write_bytes(content)
    expected = _field_wise(path)
    opens.clear()

    truth = rebuild.read_truth(path)

    assert truth == expected == rebuild.Truth(location=str(path))
    assert opens == [path]


def test_an_unsupported_suffix_reads_absent_and_opens_nothing(tmp_path, opens):
    """A stray file the reader has no handling for is never opened at all."""
    path = tmp_path / "cover.jpg"
    path.write_bytes(b"\xff\xd8\xff\xe0 not a track")

    truth = rebuild.read_truth(path)

    assert truth == _field_wise(path) == rebuild.Truth(location=str(path))
    assert opens == []


def test_a_derivation_over_n_files_makes_n_opens(tmp_path, opens):
    """The derivation walk: one open per library file, and every reading unchanged."""
    music = tmp_path / "Music"
    made: list[Path] = []
    for index, suffix in enumerate(CONTAINERS):
        for case, fields in sorted(READINGS.items()):
            made.append(_tagged(music / f"folder{index}", suffix, f"{case}-{index}", fields))
    (music / "notes.txt").write_bytes(b"not a track")
    expected = [_field_wise(path) for path in sorted(made)]
    opens.clear()

    walked = list(rebuild.library_truth(music))

    assert len(opens) == len(made), f"{len(made)} files, {len(opens)} opens"
    assert sorted(opens) == sorted(made)
    assert walked == expected

