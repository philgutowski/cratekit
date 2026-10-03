"""U110: an INBOX batch is named by its date and source, never a run identifier.

Every landing test drives the real dispatcher, as ``tests/test_intake_land.py``
does, with its fixtures. What is pinned here is the naming: the batch folder
and its playlist take ``<date> <source>``, a second landing that day takes
`` 2``, ``--name`` still wins, and the intake file keeps the identifier the
marks read, so ``sync mark`` still finds its pass's jobs from it and ``export
archive`` still reads the same pass off it.

The date is the module's own seam, pinned here, so a run that crosses midnight
reads one date throughout.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, land_cli, missing_cli
from cratekit.intake import cli as intake_cli
from cratekit.label import go
from cratekit.sync import mark_cli, playlists
from tests.test_intake_land import (
    GATE,
    _drive,
    _land,
    _manifest,
    _music,
    _stage,
)
from tests.test_intake_land import cfg as cfg  # noqa: PLC0414 - the fixture, re-exported
from tests.test_intake_land import export as export  # noqa: PLC0414 - the fixture
from tests.test_intake_land import silence as silence  # noqa: PLC0414 - the fixture

DAY = date(2026, 10, 3)
#: A sync pass as ``intake missing --run`` names it.
RUN = "2026-10-03T101500Z-ab12"
PASS = missing_cli.synced_name(RUN)


@pytest.fixture(autouse=True)
def pinned_day(monkeypatch):
    monkeypatch.setattr(batch_name, "today", lambda: DAY)


def _queued(cfg: config.Config, reference: str, *, source_id: str, run_id: str = RUN) -> None:
    """One intake job of a pass, queued the way ``crate sync all`` queues it."""
    with jobs.open_store() as store:
        intake_cli.queue_playlist(
            store,
            cfg,
            handler_key="intake.playlist",
            reference=reference,
            tracks={"t1": {"artist": "A", "title": "T"}},
            run_id=run_id,
            source_id=source_id,
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
    return [
        line.split('Name="', 1)[1].split('"', 1)[0]
        for line in inbox.splitlines()
        if 'Type="1"' in line
    ]


# ---------------------------------------------------------------------------
# The scenarios the brief names
# ---------------------------------------------------------------------------


def test_a_tidal_playlist_sync_landing_is_named_for_the_date_and_tidal_playlists(
    cfg, silence, export
):
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "pl-b", source_id=playlists.SOURCE_ID)
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--pass", PASS)

    batch = "2026-10-03 Tidal playlists"
    assert (_music(cfg, batch) / "One.flac").is_file()
    intake = Path(envelope["pending_human_action"]["artifact"])
    assert intake == Path(cfg.library.root) / f"{PASS}_inboxed.xml"
    assert _playlist_names(intake) == [batch]
    assert "_inboxed" not in "".join(_playlist_names(intake))
    assert RUN.replace(":", "") not in batch


def test_sync_mark_and_export_archive_still_find_their_pass_from_the_intake_file(
    cfg, silence, export
):
    """The two readers of the file's name: ``sync mark`` matches the pass's own
    jobs to it, and ``export archive`` and ``label mark`` record under it."""
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "pl-other", source_id=playlists.SOURCE_ID, run_id="2026-10-02T090000Z-ffff")
    _stage(cfg, silence, "One.flac")

    intake = Path(_applied(export, "--pass", PASS)["pending_human_action"]["artifact"])

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


def test_a_second_landing_the_same_day_from_the_same_source_gets_a_distinct_name(
    cfg, silence, export
):
    later = "2026-10-03T180000Z-ef56"
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _queued(cfg, "pl-b", source_id=playlists.SOURCE_ID, run_id=later)
    _stage(cfg, silence, "One.flac")
    first = _applied(export, "--pass", PASS)
    _stage(cfg, silence, "Two.flac")

    second = _applied(export, "--pass", missing_cli.synced_name(later))

    assert (_music(cfg, "2026-10-03 Tidal playlists") / "One.flac").is_file()
    assert (_music(cfg, "2026-10-03 Tidal playlists 2") / "Two.flac").is_file()
    assert not (_music(cfg, "2026-10-03 Tidal playlists") / "Two.flac").exists()
    named = [_playlist_names(Path(one["pending_human_action"]["artifact"])) for one in (first, second)]
    assert named == [["2026-10-03 Tidal playlists"], ["2026-10-03 Tidal playlists 2"]]


def test_a_second_landing_under_the_same_pass_is_refused_and_not_merged(cfg, silence, export):
    """The intake file is the pass's, as it was before U110, so a second landing
    of one pass is refused before its gate, never landed beside the first."""
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _stage(cfg, silence, "One.flac")
    _applied(export, "--pass", PASS)
    _stage(cfg, silence, "Two.flac")

    code, refused = _drive(["-d", f"{GATE}=apply", *_land(export, "--pass", PASS)])

    assert code != int(ExitCode.PENDING_HUMAN), refused
    assert refused["cause"]["reason"] == "output-exists"
    assert not (_music(cfg, "2026-10-03 Tidal playlists 2")).exists()


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
    _stage(cfg, silence, "One.flac")

    envelope = _applied(export, "--name", "Friday warmup", "--pass", PASS)

    assert (_music(cfg, "Friday warmup") / "One.flac").is_file()
    assert Path(envelope["pending_human_action"]["artifact"]).name == f"{PASS}_inboxed.xml"


def test_the_gate_screen_names_the_playlist_before_anything_moves(cfg, silence, export):
    _queued(cfg, "pl-a", source_id=playlists.SOURCE_ID)
    _stage(cfg, silence, "One.flac")

    code, refused = _drive(_land(export, "--pass", PASS))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["playlist"] == "2026-10-03 Tidal playlists"
    assert shown["intake file"].endswith(f"{PASS}_inboxed.xml")


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


# ---------------------------------------------------------------------------
# The printers hand the pass and never a run as the batch name
# ---------------------------------------------------------------------------


def test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch():
    landed = go.tail(Path("/staging"), "/lists/m.manifest.json", "2026-10-03T12:00:00Z-cd34")[-1]

    assert landed == (
        "crate intake land /staging --manifest /lists/m.manifest.json "
        "--pass 2026-10-03T120000Z-cd34"
    )
    assert "--name" not in landed


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------


def _job(handler_key: str, **payload) -> jobs.Job:
    return jobs.Job(
        job_id="j",
        handler_key=handler_key,
        payload=payload,
        config_fingerprint="",
        config_toml="",
        library_id="lib",
        state=jobs.JobState.SUCCEEDED,
        created="",
        updated="",
    )


def test_each_kind_of_pass_job_says_its_own_word():
    assert batch_name.job_word(_job("intake.playlist", source_id="playlists")) == "Tidal playlists"
    assert batch_name.job_word(_job("intake.playlist")) == "Tidal playlists"
    assert batch_name.job_word(_job("intake.playlist", source_id="favorites")) == "Favorites"
    assert batch_name.job_word(_job("intake.set")) == "Set"
    assert batch_name.job_word(_job("sync.favorites")) is None


def test_several_words_are_joined_in_one_order_whatever_order_they_arrive_in():
    assert batch_name.joined(["Favorites", "Tidal playlists", "Favorites"]) == (
        "Tidal playlists and Favorites"
    )
    assert batch_name.joined(["Set", "Favorites", "Tidal playlists"]) == (
        "Tidal playlists, Favorites and Set"
    )
    assert batch_name.joined([]) is None


def test_label_rows_name_one_label_by_its_name_and_several_as_labels(tmp_path):
    from cratekit.intake import landing

    one = landing.read_label_manifest(
        _manifest(tmp_path / "a", [("1", "P", "One", "Sudbeat", 2025), ("2", "P", "Two", "sudbeat", 2024)])
    )
    several = landing.read_label_manifest(
        _manifest(tmp_path / "b", [("1", "P", "One", "Sudbeat", 2025), ("2", "P", "Two", "Kompakt", 2024)])
    )
    unsafe = landing.read_label_manifest(
        _manifest(tmp_path / "c", [("1", "P", "One", "AC/DC: Records", 2025)])
    )

    assert batch_name.label_words(one.rows) == "Sudbeat"
    assert batch_name.label_words(several.rows) == "Labels"
    assert batch_name.label_words(unsafe.rows) == "AC-DC- Records"
    assert batch_name.label_words(()) is None


def test_a_folder_that_holds_nothing_but_exists_still_takes_the_name(cfg):
    taken = Path(cfg.library.root) / cfg.library.music_dir / "2026-10-03 Downloads"
    taken.mkdir(parents=True)

    assert batch_name.readable(cfg) == "2026-10-03 Downloads 2"


def test_a_pass_with_jobs_on_another_library_says_nothing_about_this_one(cfg):
    with jobs.open_store() as store:
        intake_cli.queue_playlist(
            store,
            cfg,
            handler_key="intake.playlist",
            reference="pl-a",
            tracks={"t1": {"artist": "A", "title": "T"}},
            run_id=RUN,
            source_id=playlists.SOURCE_ID,
        )
    elsewhere = replace(cfg, library=replace(cfg.library, volume_id="another-volume"))

    assert batch_name.source_words(cfg, pass_name=PASS) == "Tidal playlists"
    assert batch_name.source_words(elsewhere, pass_name=PASS) == "Downloads"
