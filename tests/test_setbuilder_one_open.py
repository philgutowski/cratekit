"""U266: the set builder's index reads each file through one container open.

The ``mutagen.File`` call count is asserted exactly, and every reading equals
the seven single field reads it replaced and literal expectations. D1 applies.
"""

from __future__ import annotations

import json
from pathlib import Path

import mutagen
import pytest

from cratekit.core import tags
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameTemplate
from cratekit.modules.tools import setbuilder
from tests._containers import synth_container

# Every suffix ``iter_audio`` offers that the tag module reads, so every
# dialect and every opening class the reader dispatches on.
CONTAINERS = [".flac", ".aiff", ".aif", ".wav", ".mp3", ".m4a", ".ogg", ".opus"]

# The suffixes ``iter_audio`` offers and the tag module refuses unopened.
REFUSED = [suffix for suffix in AUDIO_EXTS if suffix not in CONTAINERS]

TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))


def _field_wise(path: Path) -> dict[str, str | None]:
    """The reading as seven single field reads give it: the reader before U266."""
    return {name: tags.read_tag(path, name) for name in setbuilder.INDEX_FIELDS}


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


@pytest.fixture(scope="module")
def probes(tmp_path_factory) -> dict[str, Path]:
    """One second of silence per container, synthesised once for the module."""
    folder = tmp_path_factory.mktemp("probes")
    made: dict[str, Path] = {}
    for suffix in CONTAINERS:
        out = folder / suffix.lstrip(".")
        out.mkdir()
        made[suffix] = synth_container(out, suffix)
    return made


def _tagged(probes, folder: Path, suffix: str, name: str, fields: dict[str, object]) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{name}{suffix}"
    target.write_bytes(probes[suffix].read_bytes())
    if fields:
        assert tags.write_tags(target, fields), f"the fixture could not tag {target.name}"
    return target


# The tag sets each container is read under; the title carries the name head,
# where the live library keeps it.
READINGS: dict[str, dict[str, object]] = {
    "every-field": {
        "title": "08A - 124 - Sun Path", "artist": "Nova Reef", "genre": "Deep House",
        "initialkey": "08A", "energylevel": 6, "voxlevel": 40, "voxgender": "female",
    },
    "lossy-marked": {
        "title": "11B - 122 - [MP3] Low Tide", "artist": "Alder", "genre": "Garage",
        "initialkey": "11B",
    },
    "two-fields": {"title": "Unheaded Work", "artist": "Birch"},
    "padded": {"title": " 03A - 120 - Spaced ", "genre": " Disco ", "energylevel": " 7 "},
    "beyond-ascii": {"title": "05A - 118 - Électrique Nuit", "artist": "Øre Väst"},
    "untagged": {},
}


#: What the every field shape reads back as, on every container.
EVERY_FIELD_READ = {
    "title": "08A - 124 - Sun Path", "artist": "Nova Reef", "genre": "Deep House",
    "initialkey": "08A", "energylevel": "6", "voxlevel": "40", "voxgender": "female",
}


#: The shapes whose title carries a key head, so a set can place them.
KEYED_SHAPES = {"every-field", "lossy-marked", "padded", "beyond-ascii"}


@pytest.mark.parametrize("suffix", CONTAINERS)
@pytest.mark.parametrize("case", sorted(READINGS))
def test_one_open_reads_what_the_seven_reads_read(tmp_path, probes, opens, suffix, case):
    """Every container and every tag shape: one open, and today's exact mapping."""
    path = _tagged(probes, tmp_path / "lib", suffix, case, READINGS[case])
    opens.clear()
    expected = _field_wise(path)
    assert len(opens) == len(setbuilder.INDEX_FIELDS), "the oracle is the seven open reader"
    opens.clear()

    read = setbuilder.read_index_tags(path)

    assert opens == [path], f"{suffix} {case}: read_index_tags opened {opens!r}"
    assert read == expected
    assert list(read) == list(setbuilder.INDEX_FIELDS), "the mapping's keys moved"
    if case == "every-field":
        # Pinned literally too, since the seven reads share the one reader's body.
        assert read == EVERY_FIELD_READ, f"{suffix}: the values written are not read"


def test_the_values_read_are_the_values_written(tmp_path, probes):
    """Guard against an equality that holds only because both sides read None."""
    path = _tagged(probes, tmp_path / "lib", ".flac", "every", READINGS["every-field"])
    assert setbuilder.read_index_tags(path) == EVERY_FIELD_READ
    padded = _tagged(probes, tmp_path / "lib", ".mp3", "padded", READINGS["padded"])
    assert setbuilder.read_index_tags(padded) == {
        "title": "03A - 120 - Spaced", "artist": None, "genre": "Disco", "initialkey": None,
        "energylevel": "7", "voxlevel": None, "voxgender": None,
    }


def test_an_undecodable_field_reads_none_and_its_neighbours_still_read(tmp_path, probes, opens):
    """An MP4 freeform atom whose bytes are not text: that field alone reads None."""
    from mutagen.mp4 import MP4, MP4FreeForm

    path = _tagged(
        probes, tmp_path / "lib", ".m4a", "broken",
        {"title": "08A - 124 - Sun Path", "artist": "Nova Reef", "voxlevel": 30},
    )
    handle = MP4(path)
    handle[tags.FIELDS["energylevel"].mp4] = [MP4FreeForm(b"\xff\xfe\xfd")]
    handle.save()
    expected = _field_wise(path)
    opens.clear()

    read = setbuilder.read_index_tags(path)

    assert opens == [path]
    assert read == expected
    assert read["energylevel"] is None
    assert read["title"] == "08A - 124 - Sun Path"
    assert read["voxlevel"] == "30"


def _unreadable(folder: Path) -> list[Path]:
    """Files no reader can take a tag from, each for a different reason."""
    folder.mkdir(parents=True, exist_ok=True)
    garbage = folder / "garbage.flac"
    garbage.write_bytes(b"this is not a flac stream at all" * 8)
    empty = folder / "empty.mp3"
    empty.write_bytes(b"")
    noise = folder / "noise.ogg"
    noise.write_bytes(b"\x00\x01" * 32)
    vanished = folder / "vanished.wav"
    return [garbage, empty, noise, vanished]


def test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises(tmp_path, opens):
    """Unopenable, empty, unrecognised and vanished files: one open, all absent."""
    absent = dict.fromkeys(setbuilder.INDEX_FIELDS)
    for path in _unreadable(tmp_path / "lib"):
        assert _field_wise(path) == absent, f"{path.name} is not unreadable today"
        opens.clear()
        assert setbuilder.read_index_tags(path) == absent, path.name
        assert opens == [path], f"{path.name}: opened {opens!r}"


def test_the_refused_suffixes_are_the_ones_the_tag_module_refuses():
    """The two lists above split ``AUDIO_EXTS`` the way the tag module does."""
    assert REFUSED, "every suffix iter_audio offers is read, so nothing is refused"
    for suffix in CONTAINERS:
        tags.dialect_of(suffix)
    for suffix in REFUSED:
        with pytest.raises(tags.UnsupportedContainer):
            tags.dialect_of(suffix)


@pytest.mark.parametrize("suffix", REFUSED)
def test_a_listed_container_no_tag_reader_handles_opens_nothing(tmp_path, opens, suffix):
    """``iter_audio`` lists these suffixes and the tag reader refuses them unopened."""
    path = tmp_path / f"stray{suffix}"
    path.write_bytes(b"\x00" * 64)

    assert setbuilder.read_index_tags(path) == dict.fromkeys(setbuilder.INDEX_FIELDS)
    assert opens == []


def _mixed_library(probes, root: Path) -> list[Path]:
    """A folder of every container under several tag shapes, plus the unreadable."""
    made: list[Path] = []
    shapes = sorted(READINGS)
    for number, suffix in enumerate(CONTAINERS):
        for offset in range(3):
            case = shapes[(number + offset) % len(shapes)]
            fields = dict(READINGS[case])
            if "title" in fields:
                # Its own work, so the duplicate collapse keeps every keyed file
                # and the comparison below is over the whole walk.
                fields["title"] = f"{fields['title']} {suffix.lstrip('.')} {offset}"
            folder = root / suffix.lstrip(".")
            made.append(_tagged(probes, folder, suffix, f"{case}-{offset}", fields))
    stray = root / "stray.aac"
    stray.write_bytes(b"\x00" * 64)
    made.append(stray)
    made.extend(p for p in _unreadable(root / "broken") if p.exists())
    return made


def test_the_index_is_what_the_seven_open_reader_built_one_open_a_file(tmp_path, probes, opens):
    """A cold walk over mixed containers: one open a file, the same index and cache."""
    root = tmp_path / "lib"
    made = _mixed_library(probes, root)
    walked = list(setbuilder.iter_audio(root))
    assert sorted(walked) == sorted(made)

    today_cache = tmp_path / "today.json"
    today = setbuilder.build_index(
        root, template=TEMPLATE, cache_path=today_cache, reader=_field_wise
    )
    opens.clear()

    cache = tmp_path / "cache.json"
    cold = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache)

    openable = [p for p in walked if p.suffix != ".aac"]
    assert sorted(opens) == sorted(openable), "a cold walk opens each file once"
    assert cold == today
    # Four of the six shapes carry a key in the title head, and every fixture
    # title is its own work, so the index keeps exactly the files of those shapes.
    keyed = [p for p in made if p.stem.rsplit("-", 1)[0] in KEYED_SHAPES]
    assert len(keyed) >= 2 * len(CONTAINERS), "the fixture holds too few works"
    assert sorted(t.path for t in cold) == sorted(str(p) for p in keyed)
    stored = json.loads(cache.read_text(encoding="utf-8"))
    assert stored == json.loads(today_cache.read_text(encoding="utf-8")), "the cache differs"

    never_cached = sorted(p for p in openable if all(v is None for v in _field_wise(p).values()))
    assert never_cached, "the fixture has no wholly empty read to keep uncached"
    opens.clear()

    warm = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache)

    assert warm == today
    assert sorted(opens) == never_cached, "a warm walk reopened a cached file"
