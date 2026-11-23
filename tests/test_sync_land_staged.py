"""A sync pass does not download, or land, a track an unlanded pass staged (U212, R-1499).

Those tracks are another pass's download, so a second pass leaves them off its
list and refuses before its download, naming the first pass and the command
that lands it (:mod:`tests.test_sync_land_beside`). The first pass runs through
the real dispatcher to its landing gate and stays there, its downloads tagged
with the ISRC the real downloader writes. The stand ins are
:mod:`tests.test_sync_land`'s: the tail and the landing stand in.
"""

# ruff: noqa: F811, the fixtures below are imported from the sync land suite by name
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from cratekit.cli import sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core import tags
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from tests._sync_builders import exited
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
    first = exited(drive(["sync", "land"]), ExitCode.PENDING_HUMAN)
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


def _refused_beside_the_first(first: dict, second: dict) -> dict:
    """The second pass's refusal before its download, naming the first (R-1499)."""
    cause = second["cause"]
    assert cause["reason"] == "refused-by-policy", cause
    assert _summary(second)["stopped_at"] == sync_land.DOWNLOAD
    (waiting,) = cause["detail"]["waiting"]
    assert waiting["pass"] == _summary(first)["land_name"]
    assert waiting["pass_run"] == _summary(first)["pass_run"]
    assert (
        f"crate sync land --pass-run {_summary(first)['pass_run']}"
        in " ".join(cause["remediation"]["steps"])
    )
    return cause


def test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses(
    machine, monkeypatch, tail
):
    """The listing leaves out what the first pass staged, and the second pass
    refuses before it downloads anything, naming the first and its command."""
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    landings = sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"])

    second = exited(_second_pass(monkeypatch, "101", "103"), ExitCode.REFUSED_BY_POLICY)
    assert script.fetched == []
    summary = _summary(second)
    assert summary["staged"] == 1
    body = json.loads(Path(summary["list"]).read_text())
    assert [track["id"] for track in body["tracks"]] == ["103"]
    said = _check(second, "missing")["detail"]
    assert said.startswith("1 missing track(s) listed as one at ")
    assert "; 1 more staged already by a download not landed yet" in said
    cause = _refused_beside_the_first(first, second)
    assert cause["detail"]["waiting"][0]["tracks"] == 2
    staged = sorted(p.name for p in _staged(cfg).iterdir() if p.is_file())
    assert staged == ["101.wav", "102.wav"]
    assert sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"]) == landings


def test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses(
    machine, monkeypatch, tail
):
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    downloads = len(_by_key("acquire.download"))
    landings = sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"])

    second = exited(_second_pass(monkeypatch, "102"), ExitCode.REFUSED_BY_POLICY)
    assert script.fetched == []
    assert len(_by_key("acquire.download")) == downloads, "a download was queued"
    summary = _summary(second)
    assert summary["staged"] == 1
    assert "list" not in summary or summary["list"] is None
    assert _check(second, "missing")["detail"].startswith(
        "nothing to download: 1 missing track(s) are staged already by a download "
        "not landed yet"
    )
    _refused_beside_the_first(first, second)
    assert sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"]) == landings


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

    again = exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PENDING_HUMAN)
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
    """A copy downloaded anyway, stood in for at the name step, is traced by its
    ISRC to the pass whose download it was."""
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    (download,) = _by_key("acquire.download")
    run_id = _summary(first)["pass_run"]
    monkeypatch.setattr(
        tail_chain, "dispatch", _refusing_name(tail, _rename_incomplete(ISRC["101"]))
    )

    again = exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PRECONDITION)
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

    again = exited(drive(["sync", "land", "--pass-run", run_id]), ExitCode.PRECONDITION)
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


def test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused(
    machine, monkeypatch, tail
):
    """With the listed track a lossy only offer and the rest staged by the first
    pass, the second refuses before its download, so nothing is refused for
    good and the first pass's tracks wait for their own landing."""
    cfg, script = machine
    first = _first_pass(monkeypatch, script, cfg)
    script.landings["103"] = Landing(kind="lossy")
    landings = sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"])

    second = exited(_second_pass(monkeypatch, "101", "103"), ExitCode.REFUSED_BY_POLICY)
    summary = _summary(second)
    assert summary["staged"] == 1
    assert not summary.get("download_refused")
    assert not summary.get("download_job")
    assert script.fetched == []
    _refused_beside_the_first(first, second)
    assert sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"]) == landings


def _download_job(cfg, list_name: str, isrc: str, *, finish: bool) -> str:
    """A download job over ``<list_name>.list.json`` freezing one track of ``isrc``."""
    from cratekit.acquire import cli as acquire_cli
    from cratekit.cli import registry
    from cratekit.core import jobs

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=registry.entry(tail_chain.DOWNLOAD_VERB).handler_key,
            payload={
                acquire_cli.LIST: f"/lists/{list_name}.list.json",
                acquire_cli.TRACKS: {"7": {"artist": "a", "title": "t", "isrc": isrc}},
            },
            cfg=cfg,
            item_ids=("7",),
        )

        def work(_job, _item):
            if not finish:
                raise RuntimeError("never acquired")

        try:
            jobs.drive(store, job.job_id, work)
        except Exception:  # noqa: BLE001 - the queue records the failed item
            pass
    return job.job_id


def test_the_passes_named_are_this_librarys_finished_downloads_earliest_first(machine):
    """Only this library's finished downloads are named, earliest first; a job
    that froze the track and never acquired it, or another library's, is not."""
    from tests.test_sync_land import dataclasses_replace_library

    cfg, _script = machine
    earliest = _download_job(cfg, "pass-a", ISRC["101"], finish=True)
    _download_job(cfg, "pass-unfinished", ISRC["101"], finish=False)
    _download_job(dataclasses_replace_library(cfg), "pass-elsewhere", ISRC["101"], finish=True)
    _download_job(cfg, "pass-other-recording", ISRC["102"], finish=True)
    latest = _download_job(cfg, "pass-b", ISRC["101"], finish=True)

    said = tail_chain._downloaded_by(ISRC["101"], "101.wav", cfg)

    assert said == (
        f"ISRC {ISRC['101']}, carried by 101.wav and by the file whose name it would "
        f"take, was downloaded by: pass-a (job {earliest}), pass-b (job {latest}); keep "
        f"one copy, move the other out of the folder, and continue the pass"
    )


def test_a_stop_that_is_not_rename_incomplete_or_cannot_read_the_queue_is_unchanged(
    machine, monkeypatch
):
    """Only the naming verb's own answer is read, and a queue that cannot be
    read leaves the refusal as it was."""
    from cratekit.core import jobs
    from cratekit.core.cause import CratekitError

    cfg, _script = machine
    _download_job(cfg, "pass-a", ISRC["101"], finish=True)
    other = dataclasses.replace(_rename_incomplete(ISRC["101"]), reason="internal-error")
    stop = tail_chain.Stop.of(sync_land.NAME, other)
    assert tail_chain.second_copies(stop, cfg) is stop

    def unreadable():
        raise CratekitError(_rename_incomplete(ISRC["101"]))

    monkeypatch.setattr(jobs, "open_store", unreadable)
    held = tail_chain.Stop.of(sync_land.NAME, _rename_incomplete(ISRC["101"]))
    assert tail_chain.second_copies(held, cfg) is held
