"""Intake's missing scenarios: a playlist job's missing rows written as a list (U307).

`crate intake playlist favorites` lists the account's hearts through the
faked catalogue and queues one item per row; the resume through the driver
reports each owned, offered or missing; `crate intake missing --job` writes
the missing rows as the list the download verb reads, with its manifest
beside it, and run again writes the same bytes. A track already staged in
the downloads folder under the ISRC the row carries is named staged and not
listed (U212). `crate intake missing --run` lists a sync pass's playlist
jobs once, a track two playlists share once with both provenances. A job
that has not finished is refused and nothing is written. On the missing
suite's own library, a folder of files the real index walks.

A file of its own, because the missing suite calls its configuration
``cfg`` and its library ``library`` as other intake suites call theirs.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from tests.label_fakes import StrictCatalogue, catalogue_factory
from tests.test_intake_missing import (
    RUN,
    Track,
    finished_in_run,
    hearts,
    mixed_library,
    resume_argv,
)
from tests.test_intake_missing import cfg as cfg  # noqa: PLC0414
from tests.test_intake_missing import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_intake_missing import library as library  # noqa: PLC0414
from tests.test_intake_missing_staged import SALT, rows, staged

OK = int(ExitCode.OK)


def test_a_playlist_job_and_the_list_of_what_it_found_missing(stage, cfg, library, monkeypatch):
    mixed_library(library)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(StrictCatalogue(hearts=hearts())))

    queued = stage.json("intake", "playlist", "favorites")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    resumed = stage.json(*resume_argv(job_id))
    assert resumed.code == OK, resumed.stdout
    assert resumed.envelope["data"]["state"] == "succeeded"

    assert stage.crate("intake", "missing", "--job", job_id).code == OK
    again = stage.json("intake", "missing", "--job", job_id)
    assert again.code == OK, again.stdout
    assert again.envelope["data"]["summary"]["written"] == 2


def test_a_track_already_staged_is_named_staged_and_not_listed(
    stage, cfg, library, tmp_path, monkeypatch
):
    staged(
        tmp_path,
        library,
        "Lumen Drift - Salt Road.flac",
        artist="Lumen Drift",
        title="Salt Road",
        isrc=SALT,
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(StrictCatalogue(hearts=rows())))
    queued = stage.json("intake", "playlist", "favorites")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    assert stage.json(*resume_argv(job_id)).code == OK

    listed = stage.json("intake", "missing", "--job", job_id)
    assert listed.code == OK, listed.stdout
    assert listed.envelope["data"]["summary"]["staged"] == 1


def test_a_pass_lists_its_playlists_once(stage, cfg, library):
    shared = Track("204", "Lumen Drift", "Salt Road")
    finished_in_run(cfg, "pl-a", [Track("205", "Kite Harbor", "Low Tide Signal"), shared])
    finished_in_run(cfg, "pl-b", [shared, Track("206", "Sable Cove", "Quiet Pier")])

    assert stage.crate("intake", "missing", "--run", RUN).code == OK
    listed = stage.json("intake", "missing", "--run", RUN)
    assert listed.code == OK, listed.stdout
    assert listed.envelope["data"]["summary"]["written"] == 3


def test_an_open_job_is_refused_and_nothing_is_written(stage, cfg, library, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(StrictCatalogue(hearts=hearts())))
    queued = stage.json("intake", "playlist", "favorites")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]

    refused = stage.json("intake", "missing", "--job", job_id)
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    assert refused.envelope["cause"]["reason"] == "intake-list-unusable"
    assert stage.crate("intake", "missing", "--job", job_id).code == refused.code
