"""U344: the tail's restamp no longer measures energy on files ``analyze run`` just scored.

``analyze run`` measures energy through the restamp's own measure, so a file
it scored carries the level a restamp would give it. ``analyze restamp
--scored-by RUN_JOB`` leaves out exactly those files, and only while the run's
calibration is still the active one and the file's tag still reads its level;
every other file is restamped as it always was. The tail passes the flag from
its own pass state and says what was left out. A hand run is unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.analysis import artifacts, energy
from cratekit.analysis import cli as analysis_cli
from cratekit.cli import registry
from cratekit.cli import tail as tail_chain
from cratekit.core import jobs, tags
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive
from tests.test_analysis_workers import (  # noqa: F401 - fixtures, used by name
    analysis_job,
    bind_scoring,
    calibration_over,
    cfg,
    detector,
    features,
    folder,
    item_states,
    place,
    resume_argv,
    silence,
    unbound,
)

RUN = ("analyze", "run")
#: The shipped reading, kept before the autouse stand in replaces it.
SHIPPED_SLICE_LENGTH = analysis_cli.slice_length
RESTAMP = ("analyze", "restamp")


class Measuring:
    """The restamp's extractor, answering one seed for every file and keeping each path asked."""

    def __init__(self, seed: int = 11) -> None:
        self.seed = seed
        self.asked: list[str] = []

    def __call__(self, path: Path) -> dict[str, float]:
        self.asked.append(Path(path).name)
        return features(self.seed)


@pytest.fixture
def measuring(monkeypatch) -> Measuring:
    extractor = Measuring()
    monkeypatch.setattr(energy, "_EXTRACTOR", extractor)
    return extractor


class Lengths:
    """The length the energy's slice is centred on, by call: steady unless told to move."""

    def __init__(self) -> None:
        self.answers: list[float | str | None] = []
        self.asked: list[str] = []

    def __call__(self, path: Path) -> float | str | None:
        self.asked.append(Path(path).name)
        return self.answers.pop(0) if self.answers else 185.25


@pytest.fixture(autouse=True)
def lengths(monkeypatch) -> Lengths:
    """No soundfile on this machine, so the header's length stands in, holding by default."""
    stand_in = Lengths()
    monkeypatch.setattr(analysis_cli, "slice_length", stand_in)
    return stand_in


@pytest.fixture
def calibrated(cfg) -> energy.Calibration:  # noqa: F811 - the imported fixture
    calibration = calibration_over(count=20)
    energy.save_calibration(cfg, calibration)
    return calibration


def run_over(folder: Path) -> jobs.Job:  # noqa: F811 - the imported fixture's name
    """``analyze run`` over ``folder``, queued and driven to done; the job."""
    code, queued = drive([*RUN, "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    code, resumed = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def restamp_jobs() -> list[jobs.Job]:
    key = registry.entry("analyze.restamp").handler_key
    with jobs.open_store() as store:
        return [job for job in jobs.list_jobs(store) if job.handler_key == key]


def queue_restamp(folder: Path, *flags: str) -> dict:  # noqa: F811
    code, envelope = drive([*RESTAMP, *flags, "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), envelope
    return envelope


def energy_of(path: Path) -> str | None:
    return tags.read_tag(path, "energylevel")


# The run's report


def test_the_run_report_names_the_calibration_its_level_was_scored_under(
    cfg, folder, silence, monkeypatch, calibrated  # noqa: F811
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    (report,) = artifacts.committed(cfg, run.job_id)
    assert report["status"] == "analyzed" and report["energy"] == 6
    assert report[analysis_cli.SCORED_UNDER] == energy.fingerprint(calibrated)


def test_the_shipped_detector_records_the_calibration_its_settings_carry(
    cfg, calibrated  # noqa: F811
):
    """The production branch: the settings the head was bound under, not the file now."""
    from cratekit.analysis import ahead

    bound = ahead.Settings.of(calibrated, cfg)
    energy.save_calibration(cfg, calibration_over(count=21))
    assert analysis_cli._scored_under(cfg, bound) == energy.fingerprint(calibrated)
    unscored = ahead.Settings.of(None, cfg)
    assert analysis_cli._scored_under(cfg, unscored) is None


def test_the_run_reads_the_slices_length_before_and_after_its_own_write(
    cfg, folder, silence, monkeypatch, calibrated, lengths  # noqa: F811
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    (report,) = artifacts.committed(cfg, run.job_id)
    assert report[analysis_cli.SLICE_HELD] is True
    assert lengths.asked == ["a.flac", "a.flac"]


def test_a_run_that_scored_no_energy_reads_no_length(
    cfg, folder, silence, monkeypatch, calibrated, lengths  # noqa: F811
):
    place(folder, silence, "a")
    bind_scoring(
        monkeypatch, detect_=detector(level=None, status=energy.STATUS_FEATURES_UNAVAILABLE)
    )
    run = run_over(folder)
    (report,) = artifacts.committed(cfg, run.job_id)
    assert report[analysis_cli.SLICE_HELD] is False and lengths.asked == []


@pytest.mark.parametrize(
    "answers",
    [[185.329, 185.567], [None, None], [185.25, None], [None, 185.25]],
    ids=["moved", "unread", "unread-after", "unread-before"],
)
def test_a_file_whose_slice_moved_or_went_unread_with_the_runs_write_is_restamped(
    cfg, folder, silence, monkeypatch, calibrated, measuring, lengths, answers  # noqa: F811
):
    """The review's MP3 with no Xing header: its length is read off its size, which the
    run's tag write grows, so the restamp's slice is not the one the run measured."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    lengths.answers = list(answers)
    run = run_over(folder)
    (report,) = artifacts.committed(cfg, run.job_id)
    assert report[analysis_cli.SLICE_HELD] is False

    queue_restamp(folder, "--scored-by", run.job_id)

    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == ["a.flac"]
    assert job.payload["left_out"] == []


def test_the_slices_length_is_the_headers_or_says_the_file_is_decoded_whole(
    monkeypatch, tmp_path
):
    from cratekit.analysis import decode

    shipped = SHIPPED_SLICE_LENGTH
    track = tmp_path / "track.mp3"
    monkeypatch.setattr(decode, "libsndfile_opens", lambda _path: True)
    monkeypatch.setattr(decode, "duration", lambda _path: 185.329)
    assert shipped(track) == 185.329
    monkeypatch.setattr(decode, "libsndfile_opens", lambda _path: False)
    assert shipped(track) == analysis_cli.DECODED_WHOLE

    def unreadable(_path):
        raise RuntimeError("no header")

    monkeypatch.setattr(decode, "libsndfile_opens", unreadable)
    assert shipped(track) is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "skipped-prefixed"),
        ("energy_status", energy.STATUS_FEATURES_UNAVAILABLE),
        ("energy", "6"),
        ("energy", True),
        ("path", None),
        (analysis_cli.SLICE_HELD, None),
    ],
)
def test_a_run_report_short_of_a_scored_level_leaves_its_file_to_the_restamp(
    cfg, folder, silence, monkeypatch, calibrated, measuring, field, value  # noqa: F811
):
    """Each condition of a left out file, broken alone on the run's own committed report."""
    import json

    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=1 if value is True else 6))
    run = run_over(folder)
    scored = folder / "a.flac"
    if value is True:
        # True reads as 1, so the tag carries 1, and only the type tells them apart.
        assert energy_of(scored) == "1"
    with jobs.open_store() as store:
        (item,) = jobs.items(store, run.job_id)
    report_path = artifacts.final_path(cfg, run.job_id, item.ordinal)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report[field] = value
    report_path.write_text(json.dumps(report), encoding="utf-8")

    queue_restamp(folder, "--scored-by", run.job_id)

    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == [scored.name]


def test_a_calibration_fingerprint_is_one_per_calibration_and_moves_with_a_refit(
    cfg, calibrated  # noqa: F811
):
    read_back = energy.load_calibration(cfg)
    assert energy.fingerprint(read_back) == energy.fingerprint(calibrated)
    assert energy.fingerprint(calibrated.to_json()) == energy.fingerprint(calibrated)
    refit = calibration_over(count=21)
    assert energy.fingerprint(refit) != energy.fingerprint(calibrated)
    import dataclasses

    cuts_alone = dataclasses.replace(
        calibrated, thresholds=tuple(cut + 0.01 for cut in calibrated.thresholds)
    )
    assert energy.fingerprint(cuts_alone) != energy.fingerprint(calibrated), (
        "the cuts decide the level, so they are part of which calibration it is"
    )
    floor_alone = dataclasses.replace(calibrated, onset_floor=(calibrated.onset_floor or 0) + 1)
    assert energy.fingerprint(floor_alone) != energy.fingerprint(calibrated)


def test_a_run_with_no_calibration_records_none_and_the_restamp_still_refuses(
    cfg, folder, silence, monkeypatch  # noqa: F811
):
    """Nothing scored, nothing left out: the refusal at the queue is today's."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=None, status=energy.STATUS_UNCALIBRATED))
    run = run_over(folder)
    (report,) = artifacts.committed(cfg, run.job_id)
    assert report[analysis_cli.SCORED_UNDER] is None
    code, envelope = drive([*RESTAMP, "--scored-by", run.job_id, "--queue-only", str(folder)])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "energy-calibration-missing"


# The restamp told the run's job


def test_a_restamp_told_the_run_measures_none_of_the_files_it_scored(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    before = {path.name: energy_of(path) for path in folder.iterdir()}

    envelope = queue_restamp(folder, "--scored-by", run.job_id)

    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["state"] == analysis_cli.ALL_SCORED
    assert envelope["data"]["progress"] == {"left_out": 2, "scored_by": run.job_id}
    assert restamp_jobs() == [], "nothing was left to restamp, so nothing was queued"
    assert measuring.asked == [], "no file the run scored is measured again"
    assert {path.name: energy_of(path) for path in folder.iterdir()} == before
    assert energy.read_undo_log(cfg) == {}


def test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """A name already carrying the head is skipped by the run (its marker before U343),
    so the restamp takes it."""
    place(folder, silence, "a")
    headed = place(folder, silence, "05B - 120 - headed", energylevel=2)
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    scored = folder / "a.flac"
    assert scored.is_file()

    envelope = queue_restamp(folder, "--scored-by", run.job_id)

    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == [headed.name]
    assert envelope["data"]["progress"]["left_out"] == 1
    assert job.payload["scored_by"] == run.job_id
    assert job.payload["left_out"] == [scored.name]
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    analysis = resumed["data"]["progress"]["analysis"]
    assert analysis["left_out"] == 1 and analysis["scored_by"] == run.job_id
    assert analysis["by_status"] == {"restamped": 1}
    assert measuring.asked == [headed.name]
    assert energy_of(headed) == str(energy.level_for(features(measuring.seed), calibrated))
    assert energy_of(headed) != "2"
    assert energy_of(scored) == "6"


def test_a_file_whose_tag_moved_since_the_run_is_restamped(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    moved = folder / "a.flac"
    assert tags.write_tags(moved, {"energylevel": 3})

    queue_restamp(folder, "--scored-by", run.job_id)

    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == [moved.name]
    assert job.payload["left_out"] == ["b.flac"]


def test_every_file_is_restamped_once_the_calibration_changed_since_the_run(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    energy.save_calibration(cfg, calibration_over(count=21))

    envelope = queue_restamp(folder, "--scored-by", run.job_id)

    (job,) = restamp_jobs()
    assert sorted(item_states(job.job_id)) == ["a.flac", "b.flac"]
    assert envelope["data"]["progress"]["left_out"] == 0
    assert job.payload["left_out"] == []


def test_a_file_the_run_could_not_score_is_restamped(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """A level the features could not give is no level, so the restamp tries again."""
    place(folder, silence, "a")
    bind_scoring(
        monkeypatch,
        detect_=detector(level=None, status=energy.STATUS_FEATURES_UNAVAILABLE),
    )
    run = run_over(folder)
    queue_restamp(folder, "--scored-by", run.job_id)
    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == ["a.flac"]


@pytest.mark.parametrize("which", ["unknown", "another-verb", "another-folder", "unfinished"])
def test_a_job_that_is_not_this_folders_finished_run_leaves_nothing_out_and_says_so(
    cfg, folder, silence, monkeypatch, calibrated, measuring, tmp_path, which  # noqa: F811
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run = run_over(folder)
    named = run.job_id
    if which == "unknown":
        named = "no-such-job"
    elif which == "another-verb":
        # A restamp that finished, so only the verb tells it from a run.
        queue_restamp(folder)
        (other,) = restamp_jobs()
        code, _resumed = drive(resume_argv(other.job_id))
        assert code == int(ExitCode.OK)
        named = other.job_id
    elif which == "another-folder":
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        place(elsewhere, silence, "c")
        with jobs.open_store() as store:
            jobs.cancel(store, run.job_id)
        named = run_over(elsewhere).job_id
        assert named != run.job_id
    else:
        code, _queued = drive([*RUN, "--queue-only", str(folder)])
        assert code == int(ExitCode.OK)
        key = registry.entry("analyze.run").handler_key
        with jobs.open_store() as store:
            (fresh,) = [
                job
                for job in jobs.list_jobs(store, states=[jobs.JobState.QUEUED])
                if job.handler_key == key
            ]
        named = fresh.job_id

    envelope = queue_restamp(folder, "--scored-by", named)

    open_jobs = [job for job in restamp_jobs() if job.job_id != named and job.is_open()]
    (job,) = open_jobs
    assert list(item_states(job.job_id)) == ["a.flac"]
    assert envelope["data"]["progress"]["left_out"] == 0
    (said,) = [w for w in envelope["warnings"] if w["code"] == "restamp-left-out-nothing"]
    assert named in said["message"] and "every file is restamped" in said["message"]


def test_a_restamp_driven_in_the_foreground_still_says_it_left_nothing_out(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """The review's mistyped job: the foreground answer is the resume's, so it reads the payload."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run_over(folder)
    code, envelope = drive([*RESTAMP, "--scored-by", "no-such-job", str(folder)])
    assert code == int(ExitCode.OK), envelope
    (said,) = [w for w in envelope["warnings"] if w["code"] == "restamp-left-out-nothing"]
    assert "no-such-job" in said["message"]
    assert envelope["data"]["progress"]["analysis"]["left_out"] == 0


def test_a_hand_run_of_restamp_is_what_it_always_was(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """No flag, no new key anywhere: every file queued, the payload and answer unchanged."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    run_over(folder)

    envelope = queue_restamp(folder)

    (job,) = restamp_jobs()
    assert list(item_states(job.job_id)) == ["a.flac"]
    assert "scored_by" not in job.payload and "left_out" not in job.payload
    assert "left_out" not in envelope["data"]["progress"]
    assert not [w for w in envelope["warnings"] if w["code"] == "restamp-left-out-nothing"]
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    analysis = resumed["data"]["progress"]["analysis"]
    assert "left_out" not in analysis and "scored_by" not in analysis
    assert measuring.asked == ["a.flac"]


def test_the_tail_spells_the_restamps_words_as_the_verb_does():
    assert tail_chain.SCORED_BY_FLAG == analysis_cli.SCORED_BY_FLAG
    assert tail_chain.ALL_SCORED == analysis_cli.ALL_SCORED
    assert tail_chain.LEFT_OUT == analysis_cli.PAYLOAD_LEFT_OUT


# The tail, over the real verbs


def chain() -> tail_chain.Chain:
    return tail_chain.Chain(
        progress=None,
        namespace="test.tail",
        title="the test tail",
        steps=tail_chain.STEPS,
        origin=("test",),
        again="run it again",
    )


def through_restamp(held: tail_chain.Chain, folder: Path, cfg) -> None:  # noqa: F811
    """The tail's run and restamp steps, as the chain runs them, over the real verbs."""
    for step, verb, words in tail_chain.TAIL:
        if step != tail_chain.TAG:
            tail_chain.tail_step(held, step, verb, words, folder, cfg)


def row(held: tail_chain.Chain, step: str) -> dict:
    (found,) = [check for check in held.checks if check["key"] == f"test.tail.{step}"]
    return found


def test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    held = chain()

    through_restamp(held, folder, cfg)

    run = analysis_job("analyze.run")
    assert held.analyzed == run.job_id
    restamped = row(held, tail_chain.RESTAMP)
    assert restamped["status"] == "ok"
    assert "queued nothing" in restamped["detail"]
    assert f"analyze run job {run.job_id} scored all 2 staged file(s)" in restamped["detail"]
    assert held.summary["restamp_left_out"] == 2
    assert tail_chain.RESTAMP in held.summary["steps"]
    (asked,) = [argv for argv in held.summary["commands"] if tuple(argv[1:3]) == RESTAMP]
    assert asked[3:5] == ["--scored-by", run.job_id]
    assert restamp_jobs() == [] and measuring.asked == []


def test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    place(folder, silence, "a")
    headed = place(folder, silence, "05B - 120 - headed", energylevel=2)
    bind_scoring(monkeypatch, detect_=detector(level=6))
    held = chain()

    through_restamp(held, folder, cfg)

    run = analysis_job("analyze.run")
    (job,) = restamp_jobs()
    assert job.state is jobs.JobState.SUCCEEDED
    detail = row(held, tail_chain.RESTAMP)["detail"]
    assert f"job {job.job_id} succeeded" in detail
    assert f"leaving out 1 staged file(s) analyze run job {run.job_id} scored" in detail
    assert held.summary["restamp_left_out"] == 1
    assert measuring.asked == [headed.name]


def test_a_resumed_tail_restamps_every_file_since_its_run_scored_none(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """Run again over files the first pass named, the run skips them all, so the restamp
    takes them all, and the row says none was left out."""
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    through_restamp(chain(), folder, cfg)

    again = chain()
    through_restamp(again, folder, cfg)

    (job,) = restamp_jobs()
    assert sorted(item_states(job.job_id)) == ["a.flac", "b.flac"]
    detail = row(again, tail_chain.RESTAMP)["detail"]
    assert "leaving out no staged file" in detail
    assert again.summary["restamp_left_out"] == 0
    assert sorted(measuring.asked) == ["a.flac", "b.flac"]


def test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing(
    cfg, folder, silence, monkeypatch, calibrated, measuring  # noqa: F811
):
    """U343, the tail end to end on fixtures: run, rescore, restamp and name apply leave
    each file under its own name with its measures and its mark, no head, no title
    head and no key, and the landing plans each title as its title tag gives it."""
    from cratekit.intake import ingest
    from cratekit.write import naming_cli

    first = place(folder, silence, "Ada - Alpha", artist="Ada", title="Alpha")
    second = place(folder, silence, "Ada - Bravo", artist="Ada", title="Bravo")
    bind_scoring(monkeypatch, detect_=detector(level=6))
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg_: ())
    held = chain()

    for step, verb, words in tail_chain.TAIL:
        if step == tail_chain.TAG:
            continue
        tail_chain.tail_step(held, step, verb, words, folder, cfg)
        if step == tail_chain.ANALYZE:
            tail_chain.rescore(held, folder, cfg, unable=None)
    tail_chain.name(held, folder, cfg)

    assert [step for step in held.summary["steps"]] == [
        tail_chain.ANALYZE, tail_chain.RESTAMP, tail_chain.NAME
    ], held.summary
    assert sorted(path.name for path in folder.iterdir()) == [first.name, second.name]
    for path, title in ((first, "Alpha"), (second, "Bravo")):
        read = tags.read_tags(path, ("title", "initialkey", "analyzed", "energylevel"))
        assert read == {
            "title": title, "initialkey": None, "analyzed": "1", "energylevel": "6",
        }, path.name
        meta = ingest.file_meta(path, cfg=cfg)
        assert (meta["name"], meta["tonality"]) == (title, ""), path.name
