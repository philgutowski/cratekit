"""U250: a derivation reads each library file through one container open.

``read_truth`` used to ask three single field readers for the genre, the
energy and the vocal level, and each opened the file again, so every
``crate converge``, ``crate rebuild``, preview and resort derivation opened
every file three times, on a library that often sits on a USB drive. It now
reads the three fields through one :func:`cratekit.core.tags.read_tags` call.

WHAT THESE TESTS HOLD, and why the count is the assertion. The saving is an
open count, so the proof is the number of ``mutagen.File`` calls, which is
exact on any machine, rather than a wall clock threshold, which is not. The
readings must not move by a single value, because these derivations decide
what the library is written to: every case below compares ``read_truth``
against the three single field readers it replaced, which are still the
module's own answer to what each field reads as.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real
person, or a real track.
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


def _tagged(folder: Path, suffix: str, name: str, fields: dict[str, object]) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    probe = synth_container(folder, suffix)
    target = folder / f"{name}{suffix}"
    probe.rename(target)
    if fields:
        assert tags.write_tags(target, fields)
    return target


# The tag sets each container is read under. A numeric energy and level, a non
# numeric energy, a non numeric level, padded numbers, decimals, a genre alone,
# and no tags at all.
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
    path = _tagged(tmp_path / "lib", ".flac", "numeric", READINGS["numeric"])
    assert rebuild.read_truth(path) == rebuild.Truth(
        location=str(path), genre="Deep House", energy=7, voxlevel=55
    )
    word = _tagged(tmp_path / "lib", ".mp3", "word", READINGS["energy-word"])
    assert rebuild.read_truth(word) == rebuild.Truth(
        location=str(word), genre="Techno", energy=None, voxlevel=20
    )
    vox = _tagged(tmp_path / "lib", ".m4a", "vox", READINGS["vox-word"])
    assert rebuild.read_truth(vox) == rebuild.Truth(
        location=str(vox), genre="Disco", energy=4, voxlevel=None
    )
    padded = _tagged(tmp_path / "lib", ".aiff", "padded", READINGS["padded"])
    assert rebuild.read_truth(padded) == rebuild.Truth(
        location=str(padded), genre="Garage", energy=6, voxlevel=40
    )
    # A decimal is not a whole number, for the energy reader and read_truth
    # alike, so a conversion that learned decimals in one place shows here.
    decimal = _tagged(tmp_path / "lib", ".ogg", "decimal", READINGS["decimal"])
    assert tags.read_energy_from_file(decimal) is None
    assert rebuild.read_truth(decimal) == rebuild.Truth(
        location=str(decimal), genre="Electro", energy=None, voxlevel=None
    )


def test_an_undecodable_field_reads_none_and_its_neighbours_still_read(tmp_path, opens):
    """An MP4 freeform atom whose bytes are not text: that field alone reads None.

    The single energy reader goes through the strict body and folds the failure
    into None; the one open goes through the lenient body, which reads None for
    that field alone. The two must agree, and the genre beside it must survive.
    """
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
    """The derivation walk: one open per library file, and every reading unchanged.

    This is the card's equality check over a synthetic library: each ``Truth``
    the walk yields equals the one the three single field readers give.
    """
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

