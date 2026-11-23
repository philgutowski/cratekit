"""Tagging's retag scenarios: `crate tag retag` over a folder of coarse genres (U306).

A download folder holds three files: two carrying the catch all the shipped
taxonomy calls too coarse to be a final tag and one carrying a specific
genre. The verb stops at its explicit gate, the decision is recorded, the
sweep is queued and then driven, with a searcher bound at the worker's seam
that names one file and has no answer for the other, which goes to the review
queue. A second look at the finished job drives nothing. A second sweep over
the same folder offers the one file still coarse and is aborted. A folder with
nothing coarse is asked about and queues nothing, an absent folder says so,
an unnamed folder is refused, and a file deleted between the queue and the
drive fails its item by name. Self contained, so the suites it stands beside
can be trimmed without moving it.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.core import config, tags, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import published, searchers
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container
from tests.test_config import valid_data

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)
GATE = "tag.retag.confirm"
TAXONOMY = taxonomy.default_taxonomy()
CATCH_ALL = TAXONOMY.fallback.too_coarse_as_source[1]
SPECIFIC = "Deep House"


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A configured machine with ``repair`` on, the module that gates the verb."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library, modules={"repair": True}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path) -> Path:
    made = tmp_path / "silence"
    made.mkdir()
    return synth_container(made, ".flac")


@pytest.fixture
def searcher(monkeypatch):
    """A searcher answering by title, bound where the worker looks one up.

    The general catalogue is bound too, to a lookup that fails on any ask, so
    no file reaches the network through it.
    """
    answers = {"coarse-named": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT)}
    asked: list[tuple[str, str]] = []

    def search(artist: str, title: str):
        asked.append((artist, title))
        return answers.get(title)

    def fetch(url: str):
        raise AssertionError(f"the general catalogue was asked {url}")

    lookup = published.genre_lookup(fetch=fetch, sleep=lambda _seconds: None)
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared=None, refusals=None: search)
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)
    return asked


def place(folder: Path, silence: Path, name: str, genre: str) -> Path:
    path = folder / f"{name}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    assert tags.write_genre(path, genre), f"the fixture could not tag {name}"
    return path


def approve(stage, verb: list[str]) -> str:
    """The two acts the explicit gate takes: the refusal, then the recorded decision."""
    refused = stage.json(*verb)
    assert refused.code == DECISION, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    return run_id


def test_a_folder_retagged_behind_its_gate(stage, machine, silence, searcher, tmp_path):
    folder = tmp_path / "downloads"
    named = place(folder, silence, "coarse-named", CATCH_ALL)
    unanswered = place(folder, silence, "coarse-unanswered", CATCH_ALL)
    curated = place(folder, silence, "curated", SPECIFIC)
    verb = ["tag", "retag", str(folder)]

    assert stage.crate(*verb).code == DECISION
    run_id = approve(stage, verb)
    queued = stage.json("--run", run_id, *verb)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    driven = stage.crate("--run", run_id, *verb, "--job", job_id)
    assert driven.code == OK, driven.stderr
    assert tags.read_genre_from_file(named) == SPECIFIC
    assert tags.read_genre_from_file(unanswered) == CATCH_ALL
    assert tags.read_genre_from_file(curated) == SPECIFIC
    # The finished job read again, as JSON: it is reported, not driven.
    assert stage.json("--run", run_id, *verb, "--job", job_id).code == OK

    # A second sweep offers the one file still coarse, and is aborted.
    again = stage.json(*verb)
    assert again.code == DECISION, again.stdout
    second = again.envelope["run_id"]
    assert stage.decide(second, GATE, "abort").code == OK
    assert stage.crate("--run", second, *verb).code == OK
    assert tags.read_genre_from_file(unanswered) == CATCH_ALL


def test_the_zeroes_and_the_refusals(stage, machine, silence, searcher, tmp_path):
    done = tmp_path / "done"
    place(done, silence, "curated", SPECIFIC)
    run_id = approve(stage, ["tag", "retag", str(done)])
    nothing = stage.json("--run", run_id, "tag", "retag", str(done))
    assert nothing.code == OK, nothing.stdout

    absent = ["tag", "retag", str(tmp_path / "absent")]
    run_id = approve(stage, absent)
    assert stage.crate("--run", run_id, *absent).code == OK

    assert stage.json("tag", "retag", "").code != OK

    # A file deleted between the queue and the drive fails its item by name,
    # and the file before it is still corrected.
    folder = tmp_path / "downloads"
    named = place(folder, silence, "coarse-named", CATCH_ALL)
    place(folder, silence, "coarse-vanished", CATCH_ALL)
    verb = ["tag", "retag", str(folder)]
    run_id = approve(stage, verb)
    queued = stage.json("--run", run_id, *verb)
    assert queued.code == OK, queued.stdout
    (folder / "coarse-vanished.flac").unlink()
    failed = stage.json("--run", run_id, *verb, "--job", queued.envelope["data"]["job_id"])
    assert failed.code != OK, failed.stdout
    assert tags.read_genre_from_file(named) == SPECIFIC
