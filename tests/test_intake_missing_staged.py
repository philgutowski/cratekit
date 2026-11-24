"""U212: ``intake missing`` never lists a track already staged in the downloads folder.

A staged file is a real container, since the identity is read from its tags."""

# ruff: noqa: F811, the fixtures below are imported from the missing list suite by name
from __future__ import annotations

import json
from pathlib import Path

import pytest

from cratekit.core.exit_codes import ExitCode
from cratekit.intake import landing
from tests import test_intake_missing as miss
from tests._containers import tagged_container
from tests.test_intake_missing import cfg, fresh_cache, library  # noqa: F401 - used by name

SALT = "GBAAA2600001"
SIGNAL = "GBAAA2600002"


def staging(library: Path) -> Path:
    return library.parent / "staging"


def rows() -> list[miss.Track]:
    return [_salt(), _carrying(miss.Track("205", "Kite Harbor", "Low Tide Signal"), SIGNAL)]


def _carrying(track: miss.Track, isrc: str) -> miss.Track:
    track.isrc = isrc
    return track


def _salt() -> miss.Track:
    return _carrying(miss.Track("204", "Lumen Drift", "Salt Road"), SALT)


def staged(tmp_path: Path, library: Path, name: str, **fields: str) -> Path:
    return tagged_container(tmp_path, staging(library) / name, **fields)


def listed_ids(summary: dict) -> list[str]:
    body = json.loads(Path(summary["list"]).read_text())
    return [track["id"] for track in body["tracks"]]


def check(envelope: dict, key: str) -> dict:
    (found,) = [c for c in envelope["data"]["checks"] if c["key"] == f"intake.missing.{key}"]
    return found


def test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed(
        cfg, library, tmp_path, monkeypatch):
    """One job asked of a staging folder as it fills, from absent to every missing track staged."""
    job_id = miss.finished(monkeypatch, rows())
    first = miss.ok(job_id)[0]
    # REVIEW ROUND ONE, F4: no staging folder yet is nothing staged, said.
    assert check(first, "staged") == {
        **check(first, "staged"),
        "status": "info",
        "detail": f"the download staging folder {staging(library)} is not there, so "
        f"nothing is staged",
    }
    path = Path(first["data"]["summary"]["list"])
    before = path.read_bytes()
    # ANOTHER ISRC changes nothing.
    staged(tmp_path, library, "Other - Song.flac", artist="Other", title="Song", isrc="GBAAA2600009")
    envelope, summary = miss.ok(job_id, "--out", str(tmp_path / "other"))
    assert listed_ids(summary) == ["204", "205"]
    assert (summary["staged"], summary["staged_tracks"]) == (0, [])
    said = f"no missing track is staged already in {staging(library)}"
    assert check(envelope, "staged")["detail"] == said
    # ABSENCE OF A READ IS NOT A MATCH: no ISRC tag, or a container no reader opens, is not it.
    staged(tmp_path, library, "Lumen Drift - Salt Road (1).flac", artist="Lumen Drift",
           title="Salt Road")
    staging(library).joinpath("205.flac").write_bytes(b"not a container")
    envelope, summary = miss.ok(job_id, "--out", str(tmp_path / "unread"))
    assert listed_ids(summary) == ["204", "205"]
    assert summary["staged"] == 0
    # A CONTINUED PASS reads its own downloads: a row this list's earlier copy names stays.
    staged(tmp_path, library, "Lumen Drift - Salt Road.flac", artist="Lumen Drift",
           title="Salt Road", isrc=SALT)
    again, summary = miss.ok(job_id)
    assert path.read_bytes() == before
    assert summary["staged"] == 0
    assert listed_ids(summary) == ["204", "205"]
    # ANOTHER LIST of the same job finds the wanted track staged and does not list it.
    envelope, summary = miss.ok(job_id, "--out", str(tmp_path / "wanted"))
    assert listed_ids(summary) == ["205"]
    assert (summary["written"], summary["missing"], summary["staged"]) == (1, 1, 1)
    (row,) = summary["staged_tracks"]
    assert (row["artist"], row["title"], row["isrc"]) == ("Lumen Drift", "Salt Road", SALT)
    assert Path(row["file"]).name == "Lumen Drift - Salt Road.flac"
    said = check(envelope, "staged")
    assert said["status"] == "info"
    assert said["detail"].startswith("1 missing track(s) are staged already in ")
    assert "Lumen Drift - Salt Road as Lumen Drift - Salt Road.flac" in said["detail"]
    # A FOLDER THAT CANNOT BE READ is said, never read as nothing staged.
    def refused(folder: Path):
        raise PermissionError(13, "Permission denied", str(folder))
    with monkeypatch.context() as patched:
        patched.setattr(landing, "listing", refused)
        envelope, summary = miss.ok(job_id, "--out", str(tmp_path / "sealed"))
    assert listed_ids(summary) == ["204", "205"]
    said = check(envelope, "staged")
    assert said["status"] == "fail"
    assert "could not be read (Permission denied)" in said["detail"]
    # EVERY MISSING TRACK STAGED is something to land, not a no-op.
    staged(tmp_path, library, "b.flac", artist="Kite Harbor", title="Low Tide Signal",
           isrc="gb-aaa-26-00002")
    out = tmp_path / "all"
    envelope, summary = miss.ok(job_id, "--out", str(out))
    assert envelope["outcome"] == "ok"
    assert (summary["list"], summary["written"], summary["staged"]) == (None, 0, 2)
    assert not (out / f"intake-{job_id}.list.json").exists()
    written = check(envelope, "written")
    assert written["status"] == "info"
    assert written["detail"].startswith("nothing listed for download: the 2 missing track(s)")
    assert "staged already" in written["detail"]


def test_a_track_with_no_isrc_is_never_matched_to_a_staged_file_with_none(
        cfg, library, tmp_path, monkeypatch):
    staged(tmp_path, library, "Kite Harbor - Low Tide Signal.flac", artist="Kite Harbor")
    job_id = miss.finished(monkeypatch, [miss.Track("205", "Kite Harbor", "Low Tide Signal")])
    envelope = miss.ok(job_id)[0]
    assert listed_ids(envelope["data"]["summary"]) == ["205"]
    assert envelope["data"]["summary"]["staged"] == 0
    # REVIEW ROUND ONE, F2: the folder was not compared, and the row says so.
    assert check(envelope, "staged")["detail"] == (
        "no missing track carries an ISRC, so none was compared with the download staging folder"
    )


@pytest.mark.parametrize("named", ["204.flac", "Lumen Drift - Salt Road.flac"])
def test_a_staged_file_counts_under_its_provider_name_or_its_given_name(
        cfg, library, tmp_path, monkeypatch, named):
    staged(tmp_path, library, named, artist="Lumen Drift", title="Salt Road", isrc=SALT)
    job_id = miss.finished(monkeypatch, rows())
    _code, envelope = miss.missing(job_id)
    assert envelope["data"]["summary"]["staged"] == 1


def _wanted(ref: str, isrc: str):
    from cratekit.acquire import match
    row = {"id": ref, "artist": "Lumen Drift", "title": "Salt Road", "isrc": isrc}
    return match.read_row(row, origin=match.TIDAL, position=1)


def _earlier(out: Path, name: str, track: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)
    body = {"list": 1, "origin": "tidal", "tracks": [track]}
    (out / f"{name}.list.json").write_text(json.dumps(body), encoding="utf-8")


@pytest.mark.parametrize(
    ("earlier", "kept"),
    [
        ({"id": "204", "artist": "a", "title": "t"}, True),
        ({"id": "999", "artist": "a", "title": "t", "isrc": SALT}, True),
        ({"id": "999", "artist": "a", "title": "t"}, False),
    ], ids=["by-provider-id", "by-isrc", "neither"])
def test_each_half_of_the_own_rows_rule_keeps_a_row_alone(cfg, library, tmp_path, earlier, kept):
    """The earlier copy claims a row by provider id, or by ISRC when the ids differ."""
    from cratekit.intake import missing_cli
    staged(tmp_path, library, "a.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)
    out = miss.lists_dir(library)
    _earlier(out, "own", earlier)
    found = missing_cli._staged([_wanted("204", SALT)], out=out, name="own")
    assert (found.found == ()) is kept, found


def test_a_track_held_since_the_job_is_never_said_to_carry_no_isrc(
        cfg, library, tmp_path, monkeypatch):
    """Nothing missing asks the staging folder nothing, and the row says so (review round two)."""
    job_id = miss.finished(monkeypatch, [_salt()])
    (library / "Music" / "Lumen Drift - Salt Road.flac").write_bytes(b"")
    staged(tmp_path, library, "a.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)
    envelope, summary = miss.ok(job_id)
    assert (summary["missing"], summary["owned_since"], summary["staged"]) == (0, 1, 0)
    said = "no track is missing, so none was asked whether it is staged"
    assert check(envelope, "staged")["detail"] == said


def test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok(cfg, library, tmp_path):
    """The left out refusal stands aside when the finished rows are staged; the skip still fails."""
    kept = miss.finished_in_run(cfg, "pl-a", [_salt()])
    broken = miss.in_run(cfg, "pl-b", [miss.Track("205", "Kite Harbor", "Low Tide Signal")])
    miss.fail(broken)
    staged(tmp_path, library, "a.flac", artist="Lumen Drift", title="Salt Road", isrc=SALT)
    code, envelope = miss.run_missing("--skip-failed")
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["jobs"], summary["skipped"]) == ([kept], [broken])
    assert (summary["list"], summary["staged"]) == (None, 1)
    (skipped,) = [c for c in envelope["data"]["checks"] if c["title"] == "skipped"]
    assert skipped["status"] == "fail" and broken in skipped["detail"]
