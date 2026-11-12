"""U249: a library file's tags are read once per process, however many indexes ask.

A sync pass builds one index of the whole music folder per intake job and one
more for ``intake missing``, and before U249 each of those opened every file
again. The reader now remembers what each file said, keyed on the path, the
name template and the file's stat (size, modification and change times, inode
and device), and answers from memory only a file whose modification time is
at least two seconds older than the moment the entry was made. Every index is
still a fresh walk, so a file that is gone is absent and a new one is read.

Every library file here is set an hour into the past, because a file written
inside the window is never answered from memory, which is the rule a fresh
fixture would otherwise exercise on every line.
"""

from __future__ import annotations

import os
import shutil
import time
from collections import Counter
from pathlib import Path

import mutagen
import pytest

from cratekit import acquire
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import match
from cratekit.core import config, naming, tags
from cratekit.intake import cli as intake_cli
from tests._containers import synth_container
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.intake.test_workers import Track
from tests.test_config import valid_data
from tests.test_sync_all import _playlist, bind_playlists
from tests.test_sync_land import tail, vocal_model  # noqa: F401 - fixtures

FILES, PLAYLISTS, PER = 24, 3, 4
HOUR_NS = 3600 * 1_000_000_000


def _backdate(path: Path, *, ns: int | None = None) -> int:
    """Set ``path``'s times an hour back, or to ``ns``, and return the time set."""
    when = time.time_ns() - HOUR_NS if ns is None else ns
    os.utime(path, ns=(when, when))
    return when


@pytest.fixture
def template_flac(tmp_path) -> Path:
    (tmp_path / "template").mkdir()
    return synth_container(tmp_path / "template", ".flac")


def _tagged(template: Path, path: Path, artist: str, title: str, *, old: bool = True) -> Path:
    """A tagged copy of the template at ``path``, an hour old unless ``old`` is False."""
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template, path)
    assert tags.write_tags(path, {"artist": artist, "title": title})
    if old:
        _backdate(path)
    return path


class Opens:
    """Every container mutagen opened, by path."""

    def __init__(self, monkeypatch) -> None:
        self.paths: list[str] = []
        real = mutagen.File

        def counted(*args, **kwargs):
            self.paths.append(str(args[0]))
            return real(*args, **kwargs)

        monkeypatch.setattr(mutagen, "File", counted)

    def of(self, path: Path) -> int:
        return self.paths.count(str(path))


# ═══════════════════════════════════════════════════════════════════════════
# 1. Through the verb: a pass reads each library file once
# ═══════════════════════════════════════════════════════════════════════════


def _pass(tmp_path, monkeypatch, template: Path) -> tuple[Path, Script]:
    """The brief's reproduce: FILES tagged library files, PLAYLISTS account
    playlists of PER rows each that no library file holds."""
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    for i in range(FILES):
        _tagged(
            template, root / "Music" / f"Artist {i:03d} - Title {i:03d}.flac",
            f"Artist {i:03d}", f"Title {i:03d}",
        )
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.save(config.from_dict(valid_data(
        root, profile={"name": "slim"},
        acquisition={"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0},
        paths={"download_staging": str(tmp_path / "staging")},
    )))
    config.reset_cache()
    script = Script()
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", script)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)
    listed, serial = [], 0
    for p in range(PLAYLISTS):
        rows = []
        for _ in range(PER):
            serial += 1
            rows.append(Track(
                f"8{serial:06d}", f"Zebra Quux {serial}", f"Wholly Other Words {serial}",
                isrc=f"ZZ{serial:010d}",
            ))
            script.landings[f"8{serial:06d}"] = Landing(kind="lossless")
        listed.append((_playlist(f"pl-{p}", f"List {p}"), rows))
    bind_playlists(monkeypatch, *listed)
    return root / "Music", script


class Walks:
    """Every whole library walk ``index_library`` made, and a hook run after each."""

    def __init__(self, monkeypatch, after=None) -> None:
        self.sizes: list[int] = []
        real = match.index_library

        def walked(root, **kwargs):
            index = real(root, **kwargs)
            self.sizes.append(len(index))
            if after is not None:
                after(len(self.sizes))
            return index

        monkeypatch.setattr(match, "index_library", walked)


def test_a_pass_of_three_playlists_opens_each_library_file_once(
    tmp_path, monkeypatch, tail, template_flac  # noqa: F811
):
    music, _script = _pass(tmp_path, monkeypatch, template_flac)
    walks = Walks(monkeypatch)
    opens = Opens(monkeypatch)

    drive(["sync", "land"])

    whole = [size for size in walks.sizes if size >= FILES]
    assert len(whole) == PLAYLISTS + 1, (
        f"every job still walks the folder as it is now: {walks.sizes}"
    )
    library = sorted(music.glob("*.flac"))
    assert len(library) == FILES
    counted = Counter(opens.of(path) for path in library)
    assert counted == Counter({1: FILES}), (
        f"each library file opened once over {len(whole)} walks, not {dict(counted)}"
    )


def test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags(
    tmp_path, monkeypatch, tail, template_flac  # noqa: F811
):
    """Row 5 belongs to the second playlist. After the first job's walk, a
    library file is retagged as that row with a long album, so its size
    changes, and its old modification time is put back: the second job must
    read it again and resolve the row owned on the new tags."""
    music, _script = _pass(tmp_path, monkeypatch, template_flac)
    rewritten = music / "Artist 000 - Title 000.flac"
    before = rewritten.stat()

    def retag(walk: int) -> None:
        if walk != 1:
            return
        assert tags.write_tags(rewritten, {
            "artist": "Zebra Quux 5", "title": "Wholly Other Words 5", "album": "G" * 20000,
        })
        os.utime(rewritten, ns=(before.st_atime_ns, before.st_mtime_ns))
        after = rewritten.stat()
        assert after.st_size != before.st_size and after.st_mtime_ns == before.st_mtime_ns

    walks = Walks(monkeypatch, after=retag)
    opens = Opens(monkeypatch)
    resolved: dict[str, str] = {}
    real_resolve = intake_cli.resolve_track

    def recorded(wanted, job, cfg):
        settled = real_resolve(wanted, job, cfg)
        resolved[wanted.title] = str(settled.state)
        return settled

    monkeypatch.setattr(intake_cli, "resolve_track", recorded)

    drive(["sync", "land"])

    assert len([s for s in walks.sizes if s >= FILES]) == PLAYLISTS + 1
    assert opens.of(rewritten) == 2, "read once before the rewrite and once after"
    assert resolved["Wholly Other Words 5"] == str(match.MatchState.MATCHED), (
        f"the second job matched the file's old tags: {resolved}"
    )
    assert [title for title, state in resolved.items() if state == str(match.MatchState.MATCHED)] == [
        "Wholly Other Words 5"
    ], "only the rewritten file's row is held"
    assert len(resolved) == PLAYLISTS * PER


# ═══════════════════════════════════════════════════════════════════════════
# 2. The key and the window, against the index directly
# ═══════════════════════════════════════════════════════════════════════════


def _titles(index: match.LibraryIndex) -> set[str]:
    return {one.title for held in index.by_recording.values() for one in held}


def test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index(
    tmp_path, monkeypatch, template_flac
):
    music = tmp_path / "Music"
    one = _tagged(template_flac, music / "A - B.flac", "A", "B")
    opens = Opens(monkeypatch)

    first = match.index_library(music)
    second = match.index_library(music)

    assert opens.of(one) == 1
    assert _titles(first) == _titles(second) == {"B"}
    (held,) = second.versions(match.recording_token("A", "B"))
    assert held.path == one


def test_a_file_rewritten_to_the_same_size_inside_the_window_is_read_again(
    tmp_path, monkeypatch, template_flac
):
    """A FAT volume stamps in two second steps, so a rewrite inside one step
    keeps the size and the modification time. The change time and the inode
    are held still here, the way a volume with no change time reports them, so
    the window is the one rule left to decide."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B", old=False)
    held = path.stat()
    real = match._stamp_of

    def still(where: Path):
        stamp = real(where)
        if stamp is None or where != path:
            return stamp
        return stamp[:2] + (held.st_ctime_ns, held.st_ino, held.st_dev)

    monkeypatch.setattr(match, "_stamp_of", still)
    opens = Opens(monkeypatch)

    assert _titles(match.index_library(music)) == {"B"}
    assert tags.write_tags(path, {"title": "C"})
    os.utime(path, ns=(held.st_atime_ns, held.st_mtime_ns))
    assert path.stat().st_size == held.st_size, "the rewrite must keep the size"

    assert _titles(match.index_library(music)) == {"C"}
    assert opens.of(path) == 2


def test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time(
    tmp_path, monkeypatch, template_flac
):
    """``rsync -a``, ``cp -p`` and ``os.utime`` put the old modification time
    back over new bytes; the change time is the one stamp none of them sets."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    held = path.stat()
    opens = Opens(monkeypatch)

    assert _titles(match.index_library(music)) == {"B"}
    assert tags.write_tags(path, {"title": "C"})
    os.utime(path, ns=(held.st_atime_ns, held.st_mtime_ns))
    now = path.stat()
    assert (now.st_size, now.st_mtime_ns) == (held.st_size, held.st_mtime_ns)
    assert now.st_ctime_ns != held.st_ctime_ns

    assert _titles(match.index_library(music)) == {"C"}
    assert opens.of(path) == 2


def test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode(
    tmp_path, monkeypatch, template_flac
):
    """Two same size files whose times agree, one renamed over the other. The
    change time is held still, so the inode is the one stamp left to see it."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    other = _tagged(template_flac, tmp_path / "elsewhere" / "A - B.flac", "A", "C")
    when = path.stat().st_mtime_ns
    _backdate(other, ns=when)
    held = path.stat()
    assert other.stat().st_size == held.st_size
    real = match._stamp_of

    def still(where: Path):
        stamp = real(where)
        if stamp is None or where != path:
            return stamp
        return stamp[:2] + (held.st_ctime_ns,) + stamp[3:]

    monkeypatch.setattr(match, "_stamp_of", still)
    assert _titles(match.index_library(music)) == {"B"}
    os.replace(other, path)
    assert path.stat().st_ino != held.st_ino

    assert _titles(match.index_library(music)) == {"C"}


def test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again(
    tmp_path, monkeypatch, template_flac
):
    """A volume remounted with another in its place can hand the same inode
    number to another file; the device is the stamp that tells them apart."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    held = path.stat()
    device = [held.st_dev]
    real = match._stamp_of

    def still(where: Path):
        stamp = real(where)
        if stamp is None or where != path:
            return stamp
        return (held.st_size, held.st_mtime_ns, held.st_ctime_ns, held.st_ino, device[0])

    monkeypatch.setattr(match, "_stamp_of", still)
    opens = Opens(monkeypatch)
    match.index_library(music)
    match.index_library(music)
    assert opens.of(path) == 1, "an unchanged stamp is answered from memory"

    device[0] = held.st_dev + 1
    match.index_library(music)
    assert opens.of(path) == 2


def test_a_file_with_a_new_size_is_read_again(tmp_path, monkeypatch, template_flac):
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    held = path.stat()
    real = match._stamp_of

    def still(where: Path):
        stamp = real(where)
        if stamp is None or where != path:
            return stamp
        return (stamp[0], held.st_mtime_ns, held.st_ctime_ns, held.st_ino, held.st_dev)

    monkeypatch.setattr(match, "_stamp_of", still)
    assert _titles(match.index_library(music)) == {"B"}
    assert tags.write_tags(path, {"title": "C", "album": "G" * 20000})
    assert path.stat().st_size != held.st_size

    assert _titles(match.index_library(music)) == {"C"}


def test_a_file_with_a_new_modification_time_is_read_again(
    tmp_path, monkeypatch, template_flac
):
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    held = path.stat()
    when = held.st_mtime_ns
    real = match._stamp_of

    def still(where: Path):
        stamp = real(where)
        if stamp is None or where != path:
            return stamp
        return stamp[:2] + (held.st_ctime_ns, held.st_ino, held.st_dev)

    monkeypatch.setattr(match, "_stamp_of", still)
    assert _titles(match.index_library(music)) == {"B"}
    assert tags.write_tags(path, {"title": "C"})
    _backdate(path, ns=when + 1_000_000_000)
    assert path.stat().st_size == held.st_size

    assert _titles(match.index_library(music)) == {"C"}


def test_a_removed_file_is_absent_a_new_one_is_read_and_a_renamed_one_is_read_under_its_name(
    tmp_path, monkeypatch, template_flac
):
    music = tmp_path / "Music"
    gone = _tagged(template_flac, music / "A - Gone.flac", "A", "Gone")
    kept = _tagged(template_flac, music / "A - Kept.flac", "A", "Kept")
    moved = _tagged(template_flac, music / "A - Moved.flac", "A", "Moved")
    assert _titles(match.index_library(music)) == {"Gone", "Kept", "Moved"}

    gone.unlink()
    (music / "Sub").mkdir()
    renamed = moved.rename(music / "Sub" / "A - Moved.flac")
    new = _tagged(template_flac, music / "A - New.flac", "A", "New")
    opens = Opens(monkeypatch)

    index = match.index_library(music)

    assert _titles(index) == {"Kept", "Moved", "New"}
    assert {one.path for held in index.by_recording.values() for one in held} == {
        kept, renamed, new,
    }
    assert opens.of(kept) == 0 and opens.of(renamed) == 1 and opens.of(new) == 1


def test_the_name_template_is_part_of_the_key(tmp_path, template_flac):
    """A marker the template declares is stripped from the name; the same
    unchanged file read under a template without it keeps the marker in its
    artist, so an entry made under one template never answers the other."""
    music = tmp_path / "Music"
    music.mkdir()
    path = music / "[L] A - B.flac"
    shutil.copyfile(template_flac, path)
    _backdate(path)
    marked = naming.NameTemplate(markers=(naming.MarkerRule(field="lossy", literal="[L]"),))

    def artists(template: naming.NameTemplate) -> set[str]:
        index = match.index_library(music, template=template)
        return {one.artist for held in index.by_recording.values() for one in held}

    assert artists(marked) == {"A"}
    assert artists(naming.NameTemplate()) == {"[L] A"}
    assert artists(marked) == {"A"}


def test_a_read_that_failed_is_not_remembered(tmp_path, monkeypatch):
    """A container mutagen cannot open reads as an untagged file named for its
    stem, as it always has, and is read again by the next index, because a
    failed read on an external volume can be a moment's I/O error."""
    music = tmp_path / "Music"
    music.mkdir()
    path = music / "Named - Only.flac"
    path.write_bytes(b"not a flac stream at all")
    _backdate(path)
    opens = Opens(monkeypatch)

    first = match.index_library(music)
    assert opens.of(path) == 1, "one open per walk, as before U249"
    second = match.index_library(music)

    assert opens.of(path) == 2
    for index in (first, second):
        (held,) = index.versions(match.recording_token("Named", "Only"))
        assert held.path == path


def test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered(
    tmp_path, monkeypatch, template_flac
):
    """Whatever a partly failed read answered is what the file is indexed by,
    and the next walk asks the disk again rather than the memory."""
    music = tmp_path / "Music"
    _tagged(template_flac, music / "A - B.flac", "X", "Y")
    answers = iter(["Answer", "Again"])
    monkeypatch.setattr(tags, "read_tags_noting", lambda _p, _fields: ({
        "artist": "Lenient", "title": next(answers), "initialkey": None, "isrc": None,
    }, False))

    assert _titles(match.index_library(music)) == {"Answer"}
    assert match.remembered() == 0
    assert _titles(match.index_library(music)) == {"Again"}, "the failed read was remembered"


def test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left(
    tmp_path, monkeypatch, template_flac
):
    """Read whole at one stamp, then not whole at another (a copy half written),
    then the first stamp back over new bytes: the third walk reads the disk,
    because the file was seen changing in between."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    first = match._stamp_of(path)
    assert first is not None
    other = (first[0] + 1,) + first[1:]
    stamps = iter([first, other, first])
    monkeypatch.setattr(match, "_stamp_of", lambda _where: next(stamps))
    reads = iter([("First", True), ("Half", False), ("Restored", True)])

    def noting(_path, _fields):
        title, whole = next(reads)
        return {"artist": "A", "title": title, "initialkey": None, "isrc": None}, whole

    monkeypatch.setattr(tags, "read_tags_noting", noting)

    assert _titles(match.index_library(music)) == {"First"}
    assert _titles(match.index_library(music)) == {"Half"}
    assert match.remembered() == 0
    assert _titles(match.index_library(music)) == {"Restored"}


@pytest.mark.parametrize("name", ["empty.m4a", "empty.ogg", "zeros.opus", "short.aac"])
def test_a_container_the_reader_cannot_take_is_absent_and_not_whole(tmp_path, name):
    """A container mutagen does not recognise answers no handle, and one this
    module does not read is refused before any open; both read as absent, as
    :func:`tags.read_tags` answers them, and neither is whole."""
    fields = ("artist", "title", "initialkey", "isrc")
    path = tmp_path / name
    path.write_bytes(b"\0" * 4 if name.startswith("zeros") else b"")
    assert tags.read_tags(path, fields) == dict.fromkeys(fields)
    assert tags.read_tags_noting(path, fields) == (dict.fromkeys(fields), False)
    with pytest.raises(tags.TagReadFailed):
        tags.read_tags_checked(path, fields)


def test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed(
    tmp_path, monkeypatch, template_flac
):
    """One undecodable field reads as absent beside its neighbours, exactly as
    :func:`tags.read_tags` answers, and the read is marked as not whole, where
    the checked reader would have raised. A container mutagen cannot open is
    absent and not whole; a clean read is whole."""
    path = _tagged(template_flac, tmp_path / "A - B.flac", "A", "B")
    fields = ("artist", "title", "initialkey", "isrc")
    assert tags.read_tags_noting(path, fields) == (tags.read_tags(path, fields), True)

    real = tags._one_text

    def undecodable(handle, key, dialect):
        if "title" in str(key).lower():
            raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")
        return real(handle, key, dialect)

    monkeypatch.setattr(tags, "_one_text", undecodable)
    values, whole = tags.read_tags_noting(path, fields)
    assert values == tags.read_tags(path, fields)
    assert values["artist"] == "A" and values["title"] is None and not whole
    with pytest.raises(tags.TagReadFailed):
        tags.read_tags_checked(path, fields)

    garbage = tmp_path / "C - D.flac"
    garbage.write_bytes(b"not a flac stream at all")
    assert tags.read_tags_noting(garbage, fields) == (dict.fromkeys(fields), False)


def test_a_file_that_cannot_be_stated_is_read_as_before_and_never_remembered(
    tmp_path, monkeypatch, template_flac
):
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    monkeypatch.setattr(match, "_stamp_of", lambda _where: None)
    opens = Opens(monkeypatch)

    assert _titles(match.index_library(music)) == {"B"}
    assert _titles(match.index_library(music)) == {"B"}
    assert opens.of(path) == 2
    assert match.remembered() == 0


def test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone(tmp_path):
    path = tmp_path / "one.flac"
    path.write_bytes(b"x" * 7)
    seen = path.stat()
    assert match._stamp_of(path) == (
        seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev,
    )
    path.unlink()
    assert match._stamp_of(path) is None


def _held_clock(monkeypatch, at: int) -> list[int]:
    clock = [at]
    monkeypatch.setattr(match, "_now_ns", lambda: clock[0])
    return clock


@pytest.mark.parametrize(
    ("age_ns", "opened"),
    [(1_500_000_000, 2), (1_999_999_999, 2), (2_000_000_000, 1), (2_500_000_000, 1)],
    ids=["1.5s", "just-under-2s", "2s", "2.5s"],
)
def test_the_window_is_two_seconds_to_the_nanosecond(
    tmp_path, monkeypatch, template_flac, age_ns, opened
):
    """A file whose modification time is under two seconds older than the
    moment its entry was made is read again; two seconds or older is answered."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B", old=False)
    now = time.time_ns()
    _backdate(path, ns=now - age_ns)
    _held_clock(monkeypatch, now)
    opens = Opens(monkeypatch)

    match.index_library(music)
    match.index_library(music)

    assert opens.of(path) == opened


def test_the_entrys_moment_is_taken_before_the_read(tmp_path, monkeypatch, template_flac):
    """A write that lands while the file is being read falls inside the window
    only if the moment is the one before the read. The clock moves a second
    during each read here, and the file is a second and a half old."""
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B", old=False)
    now = time.time_ns()
    _backdate(path, ns=now - 1_500_000_000)
    clock = _held_clock(monkeypatch, now)
    real = mutagen.File
    opened: list[str] = []

    def slow(*args, **kwargs):
        opened.append(str(args[0]))
        clock[0] += 1_000_000_000
        return real(*args, **kwargs)

    monkeypatch.setattr(mutagen, "File", slow)
    match.index_library(music)
    match.index_library(music)

    assert opened.count(str(path)) == 2


# ═══════════════════════════════════════════════════════════════════════════
# 3. Nothing outlives its library
# ═══════════════════════════════════════════════════════════════════════════


def test_a_test_starts_with_nothing_remembered():
    assert match.remembered() == 0


@pytest.mark.parametrize("owner", [match, intake_cli], ids=["match", "intake"])
def test_a_reset_forgets_every_file(tmp_path, monkeypatch, template_flac, owner):
    music = tmp_path / "Music"
    path = _tagged(template_flac, music / "A - B.flac", "A", "B")
    match.index_library(music)
    assert match.remembered() == 1
    opens = Opens(monkeypatch)

    owner.reset_cache()

    assert match.remembered() == 0
    match.index_library(music)
    assert opens.of(path) == 1
