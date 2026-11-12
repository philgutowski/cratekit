"""U279: ``crate setbuild`` indexes only the library itself.

Filed from attended sitting 96. The index walked the whole library root, so the
copies a rehearsal keeps under ``<root>/.cratekit/local/rehearsals/<id>/staging``
sorted ahead of ``<root>/Music/...`` and took each real file's place when
``build_index`` collapsed one work to its first file. A person anchoring on the
real file by path was told it is not in the library, and a set could name a
companion by a path a cleanup removes.

Two folders are left out of the walk: the library state folder
(``config.library_state_dir``, whatever ``library.state_dirname`` says) and
``paths.download_staging`` when it sits under the root, which is setup's own
default (``<root>/Downloads``). They are matched BY LOCATION, the directory they
are, never by a name a library folder could share.

The engine half drives ``iter_audio`` and ``build_index`` over plain files with
a fake reader. The verb half drives ``crate setbuild`` over real tagged FLAC in
a disposable library, configured the way setup configures one.
"""

from __future__ import annotations

import io
import json
import os
import shutil
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output
from cratekit.core import config, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.modules.tools import setbuilder
from cratekit.setbuilder import cli as setbuild_cli
from tests._containers import synth_container

TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[LQ]"),))
GENRE = "Deep House"
STAGING = Path(".cratekit") / "local" / "rehearsals" / "X" / "staging"


def touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def same_work(path: Path) -> dict[str, str | None]:
    """Every file reads as one work, so the collapse keeps exactly one of them."""
    return {"title": "08A - 124 - Same Work", "artist": "Alder", "initialkey": "8A"}


def under(path: Path, folder: Path) -> bool:
    return path == folder or folder in path.parents


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------


def test_a_staging_copy_never_takes_the_library_files_place(tmp_path):
    """The sitting's shape: a rehearsal copy sorts first and won the collapse."""
    root = tmp_path / "library"
    staged = touch(root / STAGING / "A.flac")
    real = touch(root / "Music" / "A.flac")
    state = root / ".cratekit"

    before = setbuilder.build_index(root, template=TEMPLATE, reader=same_work)
    assert [t.path for t in before] == [str(staged)], (
        "the fixture no longer reproduces the defect: the staging copy must sort "
        "ahead of the library's own file for this test to mean anything"
    )

    index = setbuilder.build_index(root, template=TEMPLATE, reader=same_work, exclude=(state,))
    assert [t.path for t in index] == [str(real)]


def test_the_excluded_walk_is_todays_walk_less_the_excluded_folders(tmp_path):
    """Every library file indexed exactly as before, in exactly the same order.

    Today's answer is ``iter_audio`` with nothing left out, which is
    ``sorted(root.rglob("*"))`` filtered by suffix. The tree carries what a
    hand written walk gets wrong: dot folders that are the library's, a folder
    named like the state folder deeper down, a symlinked folder (not walked
    today), nested folders on both sides of an excluded one, and files whose
    names sort between the excluded folder and its siblings.
    """
    root = tmp_path / "library"
    state = root / ".cratekit"
    staging = root / "Downloads" / "incoming"
    names = [
        ".cratekit/local/rehearsals/X/staging/A.flac",
        ".cratekit/local/cache.json",
        ".cratekit-old/kept.flac",
        ".cratekit.flac",
        ".hidden/B.mp3",
        "Downloads/incoming/C.flac",
        "Downloads/incoming/deeper/D.aiff",
        "Downloads/incoming-other/E.flac",
        "Downloads/F.flac",
        "Music/.cratekit/G.flac",
        "Music/Downloads/incoming/H.flac",
        "Music/Album/I.FLAC",
        "Music/Album/notes.txt",
        "Music/Z/J.m4a",
        "K.wav",
    ]
    for name in names:
        touch(root / name)
    elsewhere = touch(tmp_path / "outside" / "L.flac").parent
    (root / "Music" / "linked").symlink_to(elsewhere, target_is_directory=True)

    today = list(setbuilder.iter_audio(root))
    expected = [p for p in today if not (under(p, state) or under(p, staging))]
    walked = list(setbuilder.iter_audio(root, (state, staging)))

    assert walked == expected
    assert len(walked) == len(today) - 3, "the fixture lost a file it means to exclude"
    # The library's own folders that merely share a name are walked.
    assert root / "Music" / ".cratekit" / "G.flac" in walked
    assert root / "Music" / "Downloads" / "incoming" / "H.flac" in walked
    assert root / ".cratekit-old" / "kept.flac" in walked
    assert root / "Downloads" / "incoming-other" / "E.flac" in walked


def test_an_excluded_folder_is_matched_by_location_whatever_its_spelling(tmp_path):
    """A path is not an identity. The configured value is spelled through a link."""
    root = tmp_path / "library"
    staged = touch(root / "Downloads" / "A.flac")
    real = touch(root / "Music" / "A.flac")
    alias = tmp_path / "alias"
    alias.symlink_to(root, target_is_directory=True)

    for spelling in (
        alias / "Downloads",
        root / "Music" / ".." / "Downloads",
        Path(str(root / "Downloads") + os.sep),
    ):
        walked = list(setbuilder.iter_audio(root, (spelling,)))
        assert walked == [real], f"{spelling} did not exclude {staged}"


def test_a_folder_that_excludes_nothing_changes_nothing(tmp_path):
    """Missing, outside the root, the root itself, or holding the root."""
    root = tmp_path / "library"
    touch(root / "Music" / "A.flac")
    touch(root / "Downloads" / "B.flac")
    outside = tmp_path / "staging"
    touch(outside / "C.flac")
    today = list(setbuilder.iter_audio(root))

    for folder in (root / "absent", outside, root, tmp_path, root / "Music" / "A.flac"):
        assert list(setbuilder.iter_audio(root, (folder,))) == today, folder


def test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served(tmp_path):
    """A cache from before the change holds the staging copy, current identity and all."""
    root = tmp_path / "library"
    staged = touch(root / STAGING / "A.flac")
    real = touch(root / "Music" / "A.flac")
    state = root / ".cratekit"
    cache = tmp_path / "cache.json"

    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=same_work)
    entries = json.loads(cache.read_text(encoding="utf-8"))["entries"]
    assert str(staged) in entries, "the earlier build did not cache the staging copy"

    reads: list[Path] = []

    def reader(path):
        reads.append(path)
        return same_work(path)

    index = setbuilder.build_index(
        root, template=TEMPLATE, cache_path=cache, reader=reader, exclude=(state,)
    )
    assert [t.path for t in index] == [str(real)]
    assert reads == [], "the library file was cached and should not be read again"
    kept = json.loads(cache.read_text(encoding="utf-8"))["entries"]
    assert sorted(kept) == [str(real)], "the excluded entry survived the write back"


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configure(library):
    """Save a configuration; setup's default puts staging at ``<root>/Downloads``."""

    def save(*, state_dirname: str | None = None, staging: Path | None = None) -> config.Config:
        section = {
            "root": str(library),
            "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        }
        if state_dirname is not None:
            section["state_dirname"] = state_dirname
        cfg = config.from_dict(
            {
                "schema_version": config.CURRENT_SCHEMA_VERSION,
                "library": section,
                "paths": {"download_staging": str(staging or library / "Downloads")},
                "profile": {"name": "full"},
            }
        )
        config.save(cfg)
        config.reset_cache()
        return cfg

    return save


@pytest.fixture
def place(library, silence):
    """One tagged FLAC at ``folder/<artist> - <head>.flac`` under the library."""

    def put(folder: Path, artist: str, title: str, key: str, bpm: float, energy=5) -> Path:
        head = f"{key} - {bpm:g} - {title}"
        path = library / folder / f"{artist} - {head}.flac"
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(silence, path)
        assert tags.write_tags(
            path,
            {
                "title": head,
                "artist": artist,
                "initialkey": key,
                "genre": GENRE,
                "energylevel": energy,
            },
        ), f"the fixture could not tag {path.name}"
        return path

    return put


def envelope_of(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    assert out.getvalue().strip(), f"the verb printed nothing: {err.getvalue()}"
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def named_paths(document: dict) -> list[str]:
    return [item["path"] for item in document["data"]["items"]]


def a_library_with_staging_copies(place, staging_folder: Path) -> dict[str, Path]:
    """The sitting's shape: every work also copied into a staging folder.

    ``Only Staged`` exists only as a staging copy, so a set that names it has
    named a path a cleanup removes.
    """
    music = Path("Music") / "Labels"
    works = {
        "anchor": ("Alder", "Anchor Work", "08A", 124, 6),
        "low": ("Birch", "Same Key Lower", "08A", 124, 4),
        "up": ("Cedar", "Neighbour Up", "09A", 125, 8),
    }
    held = {}
    for name, (artist, title, key, bpm, energy) in works.items():
        place(staging_folder, artist, title, key, bpm, energy)
        held[name] = place(music, artist, title, key, bpm, energy)
    held["staged"] = place(staging_folder, "Deodar", "Only Staged", "08A", 124, 5)
    return held


def assert_nothing_from(document: dict, folder: Path) -> None:
    for path in named_paths(document):
        assert not under(Path(path), folder), f"the set named {path}, inside {folder}"


@pytest.mark.parametrize(
    ("state_dirname", "where"),
    [
        (None, "state"),
        ("Cratekit State", "state"),
        (None, "staging"),
    ],
    ids=["state-folder", "renamed-state-folder", "download-staging"],
)
def test_setbuild_ranks_around_the_library_file_and_names_no_copy(
    configure, library, place, state_dirname, where
):
    cfg = configure(state_dirname=state_dirname)
    folder = (
        config.library_state_dir(cfg) / "local" / "rehearsals" / "X" / "staging"
        if where == "state"
        else Path(cfg.paths.download_staging)
    )
    excluded = config.library_state_dir(cfg) if where == "state" else folder
    held = a_library_with_staging_copies(place, folder.relative_to(library))

    code, document = envelope_of(["setbuild", str(held["anchor"])])
    assert code == int(ExitCode.OK), document
    paths = [item["path"] for item in document["data"]["items"]]
    assert sorted(paths) == sorted([str(held["low"]), str(held["up"])])
    assert_nothing_from(document, excluded)

    # The anchor payload carries no path, so the name is resolved through the
    # verb's own index and resolver, then driven through the verb as well.
    index = setbuild_cli._index(config.load(), library)
    assert setbuild_cli.named_anchor("Alder - Anchor Work", index).path == str(held["anchor"])
    assert not [t.path for t in index if under(Path(t.path), excluded)]
    code, document = envelope_of(["setbuild", "--named", "Alder - Anchor Work"])
    assert code == int(ExitCode.OK), document
    assert sorted(named_paths(document)) == sorted(paths)
    assert_nothing_from(document, excluded)


def test_a_companion_held_only_in_staging_is_left_out_of_the_set(configure, library, place):
    cfg = configure()
    state = config.library_state_dir(cfg)
    folder = state / "local" / "rehearsals" / "X" / "staging"
    held = a_library_with_staging_copies(place, folder.relative_to(library))

    code, document = envelope_of(["setbuild", str(held["anchor"])])
    assert code == int(ExitCode.OK), document
    titles = {item["title"] for item in document["data"]["items"]}
    assert "Only Staged" not in titles
    assert titles == {"Same Key Lower", "Neighbour Up"}


@pytest.mark.parametrize("where", ["state", "staging"])
def test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder(
    configure, library, place, where
):
    cfg = configure()
    state = config.library_state_dir(cfg)
    folder = (
        state / "local" / "rehearsals" / "X" / "staging"
        if where == "state"
        else Path(cfg.paths.download_staging)
    )
    held = a_library_with_staging_copies(place, folder.relative_to(library))

    code, document = envelope_of(["setbuild", str(held["staged"])])
    assert code == int(ExitCode.PRECONDITION)
    cause = document["cause"]
    assert cause["reason"] == "setbuild-anchor-not-indexed"
    named = str(state) if where == "state" else str(folder)
    assert cause["detail"]["excluded_by"] == named
    words = "Cratekit's own state folder" if where == "state" else "download staging folder"
    assert words in cause["message"], cause["message"]
    assert named in cause["message"]
    assert "is not in the library index" not in cause["message"]


def test_an_unindexed_anchor_outside_every_excluded_folder_keeps_its_wording(
    configure, library, place
):
    configure()
    place(Path("Music"), "Alder", "Anchor Work", "08A", 124)
    code, document = envelope_of(["setbuild", str(library / "Music" / "no-such.flac")])
    assert code == int(ExitCode.PRECONDITION)
    cause = document["cause"]
    assert cause["reason"] == "setbuild-anchor-not-indexed"
    assert "is not in the library index" in cause["message"]
    assert "excluded_by" not in cause["detail"]
