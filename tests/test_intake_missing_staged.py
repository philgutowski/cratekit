"""U212: ``intake missing`` never lists a track already staged in the downloads folder.

Sitting 55 (A70) ran ``crate sync land`` over an account that still had two
tracks an earlier pass had downloaded, tagged and named in the staging folder,
that pass's landing gate never answered. The pass downloaded them again, the
copies took placeholder names, and ``name apply`` refused ``rename-incomplete``
because their names were taken. The listing now reads the ISRC the downloader
writes on every file it delivers from each staged file, through the reader the
landing uses, and a missing track a staged file carries is counted as staged
and not listed.

Every expected value is a literal from the fixture rows. A staged file is a
real container carrying real tags, since the identity is read from the file.
"""

# ruff: noqa: F811, the fixtures below are imported from the missing list suite by name
from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.core.exit_codes import ExitCode
from cratekit.intake import landing
from tests._containers import tagged_container
from tests.test_intake_missing import (  # noqa: F401 - the fixtures are used by name
    Track,
    cfg,
    finished,
    fresh_cache,
    library,
    lists_dir,
    missing,
)

SALT = "GBAAA2600001"
SIGNAL = "GBAAA2600002"


def staging(library: Path) -> Path:
    return library.parent / "staging"


def rows() -> list[Track]:
    salt = Track("204", "Lumen Drift", "Salt Road")
    salt.isrc = SALT
    signal = Track("205", "Kite Harbor", "Low Tide Signal")
    signal.isrc = SIGNAL
    return [salt, signal]


def staged(tmp_path: Path, library: Path, name: str, **fields: str) -> Path:
    return tagged_container(tmp_path, staging(library) / name, **fields)


def listed_ids(summary: dict) -> list[str]:
    body = json.loads(Path(summary["list"]).read_text())
    return [track["id"] for track in body["tracks"]]


def check(envelope: dict, key: str) -> dict:
    (found,) = [c for c in envelope["data"]["checks"] if c["key"] == f"intake.missing.{key}"]
    return found


def test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed(
    cfg, library, tmp_path, monkeypatch
):
    staged(
        tmp_path, library, "Lumen Drift - Salt Road.flac",
        artist="Lumen Drift", title="Salt Road", isrc=SALT,
    )
    job_id = finished(monkeypatch, rows())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert listed_ids(summary) == ["205"]
    assert (summary["written"], summary["missing"], summary["staged"]) == (1, 1, 1)
    (row,) = summary["staged_tracks"]
    assert (row["artist"], row["title"], row["isrc"]) == ("Lumen Drift", "Salt Road", SALT)
    assert Path(row["file"]).name == "Lumen Drift - Salt Road.flac"
    said = check(envelope, "staged")
    assert said["status"] == "info"
    assert said["detail"].startswith("1 missing track(s) are staged already in ")
    assert "Lumen Drift - Salt Road as Lumen Drift - Salt Road.flac" in said["detail"]


def test_a_staged_file_carrying_another_isrc_changes_nothing(cfg, library, tmp_path, monkeypatch):
    staged(
        tmp_path, library, "Other - Song.flac", artist="Other", title="Song", isrc="GBAAA2600009"
    )
    job_id = finished(monkeypatch, rows())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert listed_ids(summary) == ["204", "205"]
    assert (summary["staged"], summary["staged_tracks"]) == (0, [])
    assert check(envelope, "staged")["detail"] == (
        "no missing track is staged already in the download staging folder"
    )


def test_a_staged_file_with_no_readable_isrc_leaves_the_track_listed(
    cfg, library, tmp_path, monkeypatch
):
    """Absence of a read is not a match: the same artist and title with no ISRC
    tag, and a container no reader opens under the provider id's name, are
    both not the track."""
    staged(
        tmp_path, library, "Lumen Drift - Salt Road.flac", artist="Lumen Drift", title="Salt Road"
    )
    staging(library).joinpath("205.flac").write_bytes(b"not a container")
    job_id = finished(monkeypatch, rows())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert listed_ids(summary) == ["204", "205"]
    assert summary["staged"] == 0


def test_a_track_with_no_isrc_is_never_matched_to_a_staged_file_with_none(
    cfg, library, tmp_path, monkeypatch
):
    staged(tmp_path, library, "Kite Harbor - Low Tide Signal.flac", artist="Kite Harbor")
    job_id = finished(monkeypatch, [Track("205", "Kite Harbor", "Low Tide Signal")])

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope["data"]["summary"]) == ["205"]
    assert envelope["data"]["summary"]["staged"] == 0


def test_every_missing_track_staged_is_something_to_land_not_a_no_op(
    cfg, library, tmp_path, monkeypatch
):
    staged(tmp_path, library, "a.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)
    staged(tmp_path, library, "b.flac", artist="Kite Harbor", title="Low Tide Signal",
           isrc="gb-aaa-26-00002")
    job_id = finished(monkeypatch, rows())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    summary = envelope["data"]["summary"]
    assert (summary["list"], summary["written"], summary["staged"]) == (None, 0, 2)
    assert not (lists_dir(library) / f"intake-{job_id}.list.json").exists()
    written = check(envelope, "written")
    assert written["status"] == "info"
    assert written["detail"].startswith("nothing listed for download: the 2 missing track(s)")
    assert "staged already" in written["detail"]


def test_a_track_this_lists_own_earlier_copy_names_stays_listed_once_staged(
    cfg, library, tmp_path, monkeypatch
):
    """A continued pass reads its own downloads in the staging folder. They
    are this list's, so the list is written again byte for byte rather than
    shortened and refused over its earlier copy."""
    job_id = finished(monkeypatch, rows())
    code, first = missing(job_id)
    assert code == int(ExitCode.OK), first
    path = Path(first["data"]["summary"]["list"])
    before = path.read_bytes()
    staged(tmp_path, library, "204.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)

    code, again = missing(job_id)

    assert code == int(ExitCode.OK), again
    assert path.read_bytes() == before
    assert again["data"]["summary"]["staged"] == 0
    assert listed_ids(again["data"]["summary"]) == ["204", "205"]


def test_a_staging_folder_that_cannot_be_read_is_said_never_read_as_nothing_staged(
    cfg, library, tmp_path, monkeypatch
):
    staged(tmp_path, library, "a.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)
    job_id = finished(monkeypatch, rows())

    def refused(folder: Path):
        raise PermissionError(13, "Permission denied", str(folder))

    monkeypatch.setattr(landing, "listing", refused)

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope["data"]["summary"]) == ["204", "205"]
    said = check(envelope, "staged")
    assert said["status"] == "fail"
    assert "could not be read (Permission denied)" in said["detail"]


@pytest.mark.parametrize("named", ["204.flac", "Lumen Drift - Salt Road.flac"])
def test_a_staged_file_counts_under_its_provider_name_or_its_given_name(
    cfg, library, tmp_path, monkeypatch, named
):
    staged(tmp_path, library, named, artist="Lumen Drift", title="Salt Road", isrc=SALT)
    job_id = finished(monkeypatch, rows())

    _code, envelope = missing(job_id)

    assert envelope["data"]["summary"]["staged"] == 1
