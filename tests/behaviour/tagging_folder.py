"""Tagging's folder scenarios: `crate tag folder` over a download folder (U306).

The shipped catalogue searcher, over a fetch answering per shop, decides three
files; a second sweep finds nothing, empty and missing folders say why, and a
Discogs token is asked first while a refusing Beatport stops after three. Self
contained, so the suites beside it can be trimmed without moving it.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from mutagen.flac import FLAC

from cratekit.core import config, tags, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import published, searchers
from tests._containers import synth_container
from tests.test_config import valid_data

TAXONOMY = taxonomy.default_taxonomy()
ARTIST = "Fixture Artist"
TOKEN = "fixture0discogs0value"


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path) -> Path:
    made = tmp_path / "silence"
    made.mkdir()
    return synth_container(made, ".flac")


def place(folder: Path, silence: Path, title: str, genre: str | None = None) -> Path:
    path = folder / f"{title}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    audio = FLAC(path)
    audio["artist"] = ARTIST
    audio["title"] = title
    audio.save()
    if genre is not None:
        assert tags.write_genre(path, genre)
    return path


def beatport_page(*tracks: tuple[str, str]) -> str:
    rows = [
        {
            "track_name": title,
            "mix_name": "",
            "artists": [{"artist_name": ARTIST}],
            "genre": [{"genre_name": genre}],
        }
        for title, genre in tracks
    ]
    state = {"queries": [{"state": {"data": {"tracks": {"data": rows}}}}]}
    payload = {"props": {"pageProps": {"dehydratedState": state}}}
    return (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(payload)
        + "</script></html>"
    )


def unasked_general(monkeypatch) -> None:
    """The general catalogue answers nothing, and no file carries an ISRC to ask it."""

    def fetch(url: str):
        raise AssertionError(f"the general catalogue was asked {url}")

    lookup = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)


def scraped(monkeypatch) -> list[str]:
    """Beatport names `sunrise`, misses the rest; Traxsource and Bandcamp refuse."""
    seen: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            found = ("sunrise", "Deep House") if "sunrise" in url else None
            page = beatport_page(found) if found else beatport_page()
            return searchers.Fetched(text=page, status=200)
        if url.startswith(searchers.TRAXSOURCE_SEARCH):
            return searchers.Fetched(note="HTTP 403", status=403)
        if url.startswith(searchers.BANDCAMP_SEARCH):
            return searchers.Fetched(
                text="<html><head><title>Client Challenge</title></head></html>", status=200
            )
        return searchers.Fetched(note=f"no route for {url}")

    def for_taxonomy(declared=None, refusals=None):
        return searchers.catalogue_searcher(
            TAXONOMY,
            fetch=fetch,
            sleep=lambda _s: None,
            walk=searchers.SCRAPED_WALK,
            refusals=refusals,
        )

    monkeypatch.setattr(searchers, "for_taxonomy", for_taxonomy)
    unasked_general(monkeypatch)
    return seen


def discogs_first(monkeypatch) -> list[str]:
    """Discogs is asked with a token and finds nothing; Beatport refuses every lookup."""
    seen: list[str] = []
    empty = json.dumps({"pagination": {"page": 1, "pages": 1, "items": 0}, "results": []})

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return searchers.Fetched(note="Cloudflare challenge, HTTP 403", status=403)
        if url.startswith(searchers.DISCOGS_SEARCH):
            return searchers.Fetched(text=empty, status=200)
        return searchers.Fetched(note=f"no route for {url}")

    asker = searchers.discogs_asker(token=TOKEN, fetch=fetch, sleep=lambda _s: None)

    def for_taxonomy(declared=None, refusals=None):
        return searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        )

    monkeypatch.setattr(searchers, "for_taxonomy", for_taxonomy)
    unasked_general(monkeypatch)
    return seen


def test_a_folder_swept_through_the_record_shops(stage, machine, silence, tmp_path, monkeypatch):
    folder = tmp_path / "downloads"
    place(folder, silence, "sunrise")
    place(folder, silence, "moonset")
    place(folder, silence, "noon", genre="Nu-Disco")
    scraped(monkeypatch)

    swept = stage.crate("tag", "folder", str(folder))
    assert swept.code == int(ExitCode.OK), swept.stdout
    assert tags.read_genre_from_file(folder / "sunrise.flac") == "Deep House"
    assert tags.read_genre_from_file(folder / "moonset.flac") is None
    assert tags.read_genre_from_file(folder / "noon.flac") == "Nu-Disco"

    # Again, as JSON: the one file still untagged is asked again.
    stage.json("tag", "folder", str(folder))

    empty = tmp_path / "empty"
    empty.mkdir()
    stage.crate("tag", "folder", str(empty))
    stage.json("tag", "folder", str(tmp_path / "absent"))
    stage.crate("tag", "folder", "")


def test_a_sweep_that_asks_discogs_first(stage, machine, silence, tmp_path, monkeypatch):
    folder = tmp_path / "downloads"
    for title in ("one", "two", "three", "four"):
        place(folder, silence, title)
    seen = discogs_first(monkeypatch)

    swept = stage.json("tag", "folder", str(folder))
    assert swept.code == int(ExitCode.OK), swept.stdout
    assert sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen) == 3
    assert any(url.startswith(searchers.DISCOGS_SEARCH) for url in seen)
