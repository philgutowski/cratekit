"""U212: a sync pass does not download again a track an unlanded pass staged.

Sitting 55 (A70) ran ``crate sync land`` while two Yours tracks a pass of
2026-10-31 had downloaded, tagged and named still sat in the staging folder,
that pass's landing gate never answered. The pass listed and downloaded them
again, and the copies stopped ``name apply`` on names already taken. Here the
first pass runs through the real dispatcher to its landing gate and stays
there, its downloads are tagged with the ISRC the real downloader writes (the
fake adapter writes none), and a second pass over a new playlist is read.

The stand ins are :mod:`tests.test_sync_land`'s: the pass, its intake jobs, the
missing list and the download are real; the tail and the landing stand in.
"""

# ruff: noqa: F811, the fixtures below are imported from the sync land suite by name
from __future__ import annotations

import json
from pathlib import Path

from cratekit.cli import sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core import tags
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.acquire_fakes import Landing
from tests.cli_drive import drive
from tests.intake.test_workers import Track
from tests.test_sync_all import _playlist, bind_playlists
from tests.test_sync_land import (  # noqa: F401 - fixtures by name
    _by_key,
    _check,
    _refused,
    _staged,
    _summary,
    machine,
    tail,
    vocal_model,
)

ISRC = {"101": "GBAAA2601101", "102": "GBAAA2601102", "103": "GBAAA2601103"}


def _rows(*ids: str) -> list[Track]:
    return [Track(n, f"Artist {n}", f"Title {n}", isrc=ISRC[n]) for n in ids]


def _first_pass(monkeypatch, script, cfg) -> dict:
    """Pass one to its landing gate, unanswered, its downloads tagged as the downloader tags."""
    for n in ISRC:
        script.landings.setdefault(n, Landing())
    bind_playlists(monkeypatch, (_playlist("pl-a", "Warmup"), _rows("101", "102")))
    code, first = drive(["sync", "land"])
    assert code == int(ExitCode.PENDING_HUMAN), first
    for n in ("101", "102"):
        path = _staged(cfg) / f"{n}.wav"
        assert tags.write_tags(
            path, {"artist": f"Artist {n}", "title": f"Title {n}", "isrc": ISRC[n]}
        ), path
    script.fetched.clear()
    return first


def _second_pass(monkeypatch, *ids: str) -> tuple[int, dict]:
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _rows("101", "102")),
        (_playlist("pl-b", "Peak"), _rows(*ids)),
    )
    return drive(["sync", "land"])


def test_a_second_pass_downloads_only_what_the_unlanded_first_did_not_stage(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _first_pass(monkeypatch, script, cfg)

    code, second = _second_pass(monkeypatch, "101", "103")

    assert code == int(ExitCode.PENDING_HUMAN), second
    assert [request.key for request in script.fetched] == ["103"]
    summary = _summary(second)
    assert summary["staged"] == 1
    body = json.loads(Path(summary["list"]).read_text())
    assert [track["id"] for track in body["tracks"]] == ["103"]
    said = _check(second, "missing")["detail"]
    assert said.startswith("1 missing track(s) listed as one at ")
    assert "; 1 more staged already by a download not landed yet" in said
    # THE LANDING STILL TAKES THE STAGED FILE: the tail and the landing ran
    # over the folder that holds it.
    staged = sorted(p.name for p in _staged(cfg).iterdir() if p.is_file())
    assert staged == ["101.wav", "102.wav", "103.wav"]
    land = tail.calls[-1]
    assert land[:3] == ["intake", "land", str(_staged(cfg))]
    assert summary["stopped_at"] == sync_land.LAND_GATE


def test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_still_lands(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _first_pass(monkeypatch, script, cfg)
    downloads = len(_by_key("acquire.download"))
    landings = sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"])

    code, second = _second_pass(monkeypatch, "102")

    assert code == int(ExitCode.PENDING_HUMAN), second
    assert script.fetched == []
    assert len(_by_key("acquire.download")) == downloads, "a download was queued"
    summary = _summary(second)
    assert summary["staged"] == 1
    assert "list" not in summary or summary["list"] is None
    assert _check(second, "missing")["detail"].startswith(
        "nothing to download: 1 missing track(s) are staged already by a download "
        "not landed yet"
    )
    assert _check(second, "download")["detail"] == (
        "nothing downloaded: every missing track is staged already"
    )
    assert sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"]) == landings + 1
    land = tail.calls[-1]
    assert land[land.index("--pass") + 1] == summary["land_name"]
    assert summary["land_name"].endswith("_synced")


def test_a_continued_pass_whose_own_downloads_are_staged_lists_them_again(
    machine, monkeypatch, tail
):
    """The pass's own downloads are in the staging folder, tagged, and its
    list names them, so continuing it rewrites the same list and reuses its
    own download job rather than refusing over the list or downloading again."""
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    listed = Path(_summary(first)["list"])
    before = listed.read_bytes()
    run_id = _summary(first)["pass_run"]

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PENDING_HUMAN), again
    assert listed.read_bytes() == before
    assert script.fetched == []
    assert len(_by_key("acquire.download")) == 1
    assert _summary(again)["staged"] == 0


def _rename_incomplete(isrc: str) -> Cause:
    return Cause(
        reason="rename-incomplete",
        message="0 file(s) were renamed, and 1 file(s) this plan named were not",
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT, steps=("read the files",)),
        retryable=True,
        origin=("write.naming_cli",),
        detail={
            "renamed": 0,
            "incomplete_count": 1,
            "incomplete": [
                {"from": "101.wav", "path": "/staged/101.wav", "why": "taken", "isrc": isrc}
            ],
        },
    )


def test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it(
    machine, monkeypatch, tail
):
    """The collision the listing cannot rule out, a copy downloaded anyway, is
    stood in for at the name step. The refusal's ISRC is read against the
    download jobs, and the step names the pass whose download it was."""
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    (download,) = _by_key("acquire.download")
    run_id = _summary(first)["pass_run"]
    monkeypatch.setattr(
        tail_chain, "dispatch", _refusing_name(tail, _rename_incomplete(ISRC["101"]))
    )

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PRECONDITION), again
    steps = again["cause"]["remediation"]["steps"]
    said = [step for step in steps if step.startswith(f"ISRC {ISRC['101']}")]
    assert said == [
        f"ISRC {ISRC['101']}, carried by 101.wav and by the file whose name it would "
        f"take, was downloaded by: {_summary(first)['land_name']} (job {download.job_id}); "
        f"keep one copy, move the other out of the folder, and continue the pass"
    ], steps
    assert _summary(again)["stopped_at"] == sync_land.NAME


def test_a_second_copy_no_download_job_records_is_said_so(machine, monkeypatch, tail):
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    run_id = _summary(first)["pass_run"]
    monkeypatch.setattr(
        tail_chain, "dispatch", _refusing_name(tail, _rename_incomplete("GBAAA2601999"))
    )

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PRECONDITION), again
    steps = again["cause"]["remediation"]["steps"]
    assert (
        "ISRC GBAAA2601999, carried by 101.wav and by the file whose name it would "
        "take, is in no download job of this library, so the copy in its way did "
        "not come from a download here: compare the two by hand"
    ) in steps, steps


def _refusing_name(tail, cause: Cause):
    def refusing(argv):
        if "name" in argv and "apply" in argv:
            tail.calls.append(list(argv))
            return _refused(cause)
        return tail(argv)

    return refusing
