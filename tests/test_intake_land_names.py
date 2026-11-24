"""U110: an INBOX batch is named by its date and source, never a run identifier.

A second landing that day takes `` 2``, ``--name`` wins, and the intake file keeps the
identifier the marks read. The date is pinned so one run reads one date."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, land_cli, landing, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import go
from cratekit.sync import mark_cli, playlists
from tests.test_intake_land import GATE, _drive, _land, _manifest, _music, _stage
from tests.test_intake_land import cfg as cfg
from tests.test_intake_land import export as export
from tests.test_intake_land import silence as silence

DAY = date(2026, 10, 3)
#: A sync pass as ``intake missing --run`` names it.
RUN = "2026-10-03T101500Z-ab12"
PASS = missing_cli.synced_name(RUN)


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _queued(
    cfg: config.Config, reference: str, *, source_id: str, run_id: str = RUN,
    ended: jobs.JobState = jobs.JobState.SUCCEEDED,
) -> None:
    """One intake job of a pass, queued as ``crate sync all`` does and ended as its worker does."""
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store, cfg, handler_key="intake.playlist", reference=reference,
            tracks={"t1": {"artist": "A", "title": "T"}}, run_id=run_id, source_id=source_id,
        )
        stopped = Cause(
            reason="internal-error", message="stopped for the test",
            remediation=Remediation(steps=("nothing",)), origin=("test",),
        )
        jobs.transition(
            store, job.job_id, ended, cause=None if ended is jobs.JobState.SUCCEEDED else stopped
        )


def _applied(export: Path, *extra: str) -> dict:
    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, *extra)])
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    return envelope


def _playlist_names(intake: Path) -> list[str]:
    """Every playlist the intake file's INBOX holds, read off its bytes."""
    body = intake.read_text(encoding="utf-8")
    inbox = body[body.index('<NODE Name="INBOX"') :]
    inbox = inbox[: inbox.index("\n      </NODE>")] if "\n      </NODE>" in inbox else inbox
    lines = [line for line in inbox.splitlines() if 'Type="1"' in line]
    return [line.split('Name="', 1)[1].split('"', 1)[0] for line in lines]


def test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass(
    cfg, silence, export
):
    """``sync mark`` matches the pass's jobs to its intake file's name, as the marks record."""
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "pl-other", source_id=playlists.SOURCE_ID, run_id="2026-10-02T090000Z-ffff")
    _stage(cfg, silence, "One.flac")
    batch = "2026-10-03 Tidal playlists"
    # The gate screen names the playlist before anything moves.
    code, refused = _drive(_land(export, "--pass", PASS))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["playlist"] == batch
    assert refused["cause"]["detail"]["shown"]["intake file"].endswith(f"{PASS}_inboxed.xml")
    envelope = _applied(export, "--pass", PASS)
    assert (_music(cfg, batch) / "One.flac").is_file()
    intake = Path(envelope["pending_human_action"]["artifact"])
    assert intake == Path(cfg.library.root) / f"{PASS}_inboxed.xml"
    assert _playlist_names(intake) == [batch]
    assert "_inboxed" not in "".join(_playlist_names(intake))
    assert RUN.replace(":", "") not in batch
    assert mark_cli.pass_name_of(intake) == PASS
    with jobs.open_store() as store:
        found = mark_cli._pass_jobs(store, cfg, mark_cli.pass_name_of(intake), "intake.playlist")
    assert [playlists.playlist_of(job) for job in found] == ["pl-a"]
    # Retired by ``intake imported``, the same pass is read off the new name.
    retired = intake.with_name(intake.name + land_cli.RETIRED_SUFFIX)
    assert mark_cli.pass_name_of(retired) == PASS


def test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label(
    cfg, silence, export, tmp_path
):
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Sudbeat", 2025)])
    envelope = _applied(export, "--manifest", str(manifest), "--pass", "2026-10-03T120000Z-cd34")
    assert (_music(cfg, "2026-10-03 Sudbeat") / "One.flac").is_file()
    intake = Path(envelope["pending_human_action"]["artifact"])
    assert intake.name == "2026-10-03T120000Z-cd34_inboxed.xml"
    assert _playlist_names(intake) == ["2026-10-03 Sudbeat"]


def test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged(
    cfg, silence, export
):
    """A second landing of one pass is refused before its gate; another pass takes `` 2``."""
    later = "2026-10-03T180000Z-ef56"
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "pl-b", source_id=playlists.SOURCE_ID, run_id=later)
    _stage(cfg, silence, "One.flac")
    first = _applied(export, "--pass", PASS)
    _stage(cfg, silence, "Two.flac")
    code, refused = _drive(["-d", f"{GATE}=apply", *_land(export, "--pass", PASS)])
    assert code != int(ExitCode.PENDING_HUMAN), refused
    assert refused["cause"]["reason"] == "output-exists"
    assert not (_music(cfg, "2026-10-03 Tidal playlists 2")).exists()
    second = _applied(export, "--pass", missing_cli.synced_name(later))
    assert (_music(cfg, "2026-10-03 Tidal playlists") / "One.flac").is_file()
    assert (_music(cfg, "2026-10-03 Tidal playlists 2") / "Two.flac").is_file()
    assert not (_music(cfg, "2026-10-03 Tidal playlists") / "Two.flac").exists()
    named = [_playlist_names(Path(one["pending_human_action"]["artifact"])) for one in (first, second)]
    assert named == [["2026-10-03 Tidal playlists"], ["2026-10-03 Tidal playlists 2"]]


def test_a_job_the_pass_lost_does_not_name_the_batch(cfg, silence, export):
    """A failed job's tracks are left out of the download, so its word is too."""
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "favorites", source_id="favorites", ended=jobs.JobState.FAILED)
    assert batch_name.source_words(cfg, pass_name=PASS) == "Tidal playlists"
    _queued(cfg, "favorites", source_id="favorites")
    assert batch_name.source_words(cfg, pass_name=PASS) == "Tidal playlists and Favorites"


def test_a_default_name_taken_after_the_gate_is_refused_under_the_lock(
    cfg, silence, export, monkeypatch
):
    """A name taken between the gate and the lock refuses stale; run again, the next is free."""
    _stage(cfg, silence, "One.flac")
    real_apply = landing.apply

    def taken_meanwhile(planned, **kwargs):
        raise AssertionError("the engine was reached over a taken name")

    def take_then_lock(batch):
        _music(cfg, batch).mkdir(parents=True)
        return real_lock(batch)

    real_lock = landing.batch_lock
    monkeypatch.setattr(landing, "batch_lock", take_then_lock)
    monkeypatch.setattr(landing, "apply", taken_meanwhile)
    code, refused = _drive(["-d", f"{GATE}=apply", *_land(export)])
    assert refused["cause"]["reason"] == "decision-stale", refused
    assert "2026-10-03 Downloads" in refused["cause"]["message"]
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    monkeypatch.setattr(landing, "batch_lock", real_lock)
    monkeypatch.setattr(landing, "apply", real_apply)
    _applied(export)
    assert (_music(cfg, "2026-10-03 Downloads 2") / "One.flac").is_file()


def test_a_landing_whose_intake_file_another_landing_is_writing_is_refused(cfg, silence, export):
    """The intake file is keyed on the pass, so its own lock holds one pass under another name."""
    _stage(cfg, silence, "One.flac")
    with landing.intake_lock(PASS):
        code, refused = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", "Other", "--pass", PASS)])
        with pytest.raises(CratekitError) as caught:
            with landing.intake_lock(PASS):
                pass
    assert refused["cause"]["reason"] == "job-driver-held", refused
    assert refused["cause"]["detail"]["intake"] == PASS
    assert (Path(cfg.paths.download_staging) / "One.flac").is_file()
    assert not (Path(cfg.library.root) / f"{PASS}_inboxed.xml").exists()
    assert caught.value.cause.reason == "job-driver-held"
    assert caught.value.cause.detail["intake"] == PASS
    # A batch named exactly as a pass is a different lock.
    with landing.intake_lock(PASS), landing.batch_lock(PASS):
        pass


def test_a_pass_with_no_jobs_here_lands_as_downloads(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    _applied(export, "--pass", PASS)
    assert (_music(cfg, "2026-10-03 Downloads") / "One.flac").is_file()


def test_name_overrides_and_names_the_intake_file_when_no_pass_is_given(cfg, silence, export):
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _stage(cfg, silence, "One.flac")
    envelope = _applied(export, "--name", "Friday warmup")
    assert (_music(cfg, "Friday warmup") / "One.flac").is_file()
    intake = Path(envelope["pending_human_action"]["artifact"])
    assert intake.name == "Friday warmup_inboxed.xml"
    assert _playlist_names(intake) == ["Friday warmup"]


def test_name_and_pass_together_name_the_batch_and_the_file_apart(cfg, silence, export):
    """The recheck is for a name this run chose; a person's ``--name`` may be landed into again."""
    _music(cfg, "Friday warmup").mkdir(parents=True)
    _stage(cfg, silence, "One.flac")
    envelope = _applied(export, "--name", "Friday warmup", "--pass", PASS)
    assert (_music(cfg, "Friday warmup") / "One.flac").is_file()
    assert Path(envelope["pending_human_action"]["artifact"]).name == f"{PASS}_inboxed.xml"


@pytest.mark.parametrize("given", ["", " padded", ".hidden", "a/b", "a\\b"])
def test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate(
    cfg, silence, export, given
):
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(_land(export, "--pass", given))
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "intake-list-unusable"
    assert refused["cause"]["detail"] == {"pass": given}
    assert list(Path(cfg.library.root).glob("*_inboxed.xml")) == []


def test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch():
    landed = go.tail(Path("/staging"), "/lists/m.manifest.json", "2026-10-03T12:00:00Z-cd34")[-1]
    assert landed == (
        "crate intake land /staging --manifest /lists/m.manifest.json "
        "--pass 2026-10-03T120000Z-cd34"
    )
    assert "--name" not in landed


def _job(handler_key: str, **payload) -> jobs.Job:
    return jobs.Job(
        "j", handler_key, payload, "", "", "lib", jobs.JobState.SUCCEEDED, created="", updated=""
    )


def test_each_kind_of_pass_job_says_its_own_word():
    assert batch_name.job_word(_job("intake.playlist", source_id="playlists")) == "Tidal playlists"
    assert batch_name.job_word(_job("intake.playlist")) == "Tidal playlists"
    assert batch_name.job_word(_job("intake.playlist", source_id="favorites")) == "Favorites"
    assert batch_name.job_word(_job("intake.set")) == "Set"
    assert batch_name.job_word(_job("sync.favorites")) is None


def test_several_words_are_joined_in_one_order_whatever_order_they_arrive_in():
    joined = batch_name.joined
    assert joined(["Favorites", "Tidal playlists", "Favorites"]) == "Tidal playlists and Favorites"
    assert joined(["Set", "Favorites", "Tidal playlists"]) == "Tidal playlists, Favorites and Set"
    assert batch_name.joined([]) is None


def test_label_rows_name_one_label_by_its_name_and_several_as_labels(tmp_path):
    def read(folder: str, *rows: tuple) -> landing.LabelManifest:
        return landing.read_label_manifest(_manifest(tmp_path / folder, list(rows)))

    one = read("a", ("1", "P", "One", "Sudbeat", 2025), ("2", "P", "Two", "sudbeat", 2024))
    several = read("b", ("1", "P", "One", "Sudbeat", 2025), ("2", "P", "Two", "Kompakt", 2024))
    unsafe = read("c", ("1", "P", "One", "AC/DC: Records", 2025))
    assert batch_name.label_words(one.rows) == "Sudbeat"
    assert batch_name.label_words(several.rows) == "Labels"
    assert batch_name.label_words(unsafe.rows) == "AC-DC- Records"
    assert batch_name.label_words(()) is None


def test_a_folder_that_holds_nothing_but_exists_still_takes_the_name(cfg):
    taken = Path(cfg.library.root) / cfg.library.music_dir / "2026-10-03 Downloads"
    taken.mkdir(parents=True)
    assert batch_name.readable(cfg) == "2026-10-03 Downloads 2"


def test_a_pass_with_jobs_on_another_library_says_nothing_about_this_one(cfg):
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    elsewhere = replace(cfg, library=replace(cfg.library, volume_id="another-volume"))
    assert batch_name.source_words(cfg, pass_name=PASS) == "Tidal playlists"
    assert batch_name.source_words(elsewhere, pass_name=PASS) == "Downloads"
