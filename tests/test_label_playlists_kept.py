"""R-1091: a full label build keeps what it read, so a large label builds over several runs.

``crate label playlists LABEL`` reads every confirmed release's tracks. Each
read is now kept per label for :data:`cratekit.label.kept_reads.KEPT_FOR`, so
a build the provider's breaker parks part way resumes where it stopped, and
the run that carries out an approved plan reads none of the catalogue again.
Every scenario the brief names is here, driven through the real dispatcher with
the catalogue and the account faked, as ``tests/test_label_playlists.py``
drives the full build. The live build of a large label is owed to an attended
sitting and is not claimed here.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.core.jobs import Parked
from cratekit.label import kept_reads, playlists_cli
from tests.cli_drive import drive
from tests.label_fakes import FakeTrack
from tests.test_label_playlists import BUILD, LABEL, LABEL_ID, LISTED, _entry, _years
from tests.test_label_playlists import followed as followed  # noqa: PLC0414 - fixture
from tests.test_label_playlists_releases import (
    RELEASES,
    _decided,
    _took,
)
from tests.test_label_playlists_releases import (
    small_threshold as small_threshold,  # noqa: PLC0414 - fixture
)
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

CRAWL = playlists_cli.CRAWL_GATE
FULL = ["label", "playlists", LABEL]

#: The releases a full build reads, in the order it reads them: the listed ones
#: the fake confirms, newest year first, the undated one last. r6 is listed and
#: not confirmed, so it is never read.
READ = ["r3", "r4", "r2", "r1", "r7", "r5"]


def _parks_after(monkeypatch, fake, reads: int) -> dict:
    """The provider's breaker trips once ``reads`` releases have been read.

    Returns the switch: set ``after`` to ``None`` and the cooldown has lifted.
    """
    real = fake.release_tracks
    done: list[str] = []
    switch: dict = {"after": reads}

    def paced(release_id):
        if switch["after"] is not None and len(done) >= switch["after"]:
            fake.releases_asked_for.append(release_id)
            raise Parked(
                refuse(
                    "provider-cooldown",
                    "the provider answered rate limited too often and the gate is cooling",
                    retryable=True,
                ).cause
            )
        done.append(release_id)
        return real(release_id)

    monkeypatch.setattr(fake, "release_tracks", paced)
    return switch


def _stored() -> dict:
    return json.loads(kept_reads.path_for(LABEL_ID).read_text(encoding="utf-8"))


def _age_every_read(by: timedelta, only: set[str] | None = None) -> None:
    """Move kept reads back in time, as a store written ``by`` ago would be."""
    path = kept_reads.path_for(LABEL_ID)
    document = _stored()
    for release_id, read in document["reads"].items():
        if only is None or release_id in only:
            then = datetime.fromisoformat(read["read_at"]) - by
            read["read_at"] = then.isoformat()
    path.write_text(json.dumps(document), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════
# 1. A build the breaker stops part way resumes where it stopped
# ═══════════════════════════════════════════════════════════════════════════


def test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not(
    followed, monkeypatch
):
    _cfg, fake, account = followed
    switch = _parks_after(monkeypatch, fake, 3)
    code, refused = drive(FULL)
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "provider-cooldown"
    # WHAT WAS READ BEFORE THE TRIP IS KEPT, and nothing was written.
    assert sorted(_stored()["reads"]) == sorted(READ[:3])
    assert account._writes == 0

    switch["after"] = None
    fake.releases_asked_for.clear()
    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    # ONLY THE RELEASES THE STOPPED RUN NEVER READ are asked for.
    assert sorted(fake.releases_asked_for) == sorted(READ[3:])
    shown = refused["cause"]["detail"]["shown"]
    assert shown["release reads"].startswith(
        f"3 release read(s) reused from an earlier run, the oldest 0 minute(s) old, "
        f"and {len(READ) - 3} read by this run"
    )


def test_a_resumed_build_plans_what_a_build_in_one_go_plans(followed, monkeypatch):
    _cfg, fake, account = followed
    switch = _parks_after(monkeypatch, fake, 2)
    assert drive(FULL)[0] != int(ExitCode.OK)
    switch["after"] = None

    code, done = _decided(FULL, (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    (folder_id,) = account.folder_names
    assert _years(account, folder_id) == {
        "Kompakt 2021": ["t1", "t2"],
        "Kompakt 2022": ["t3"],
        "Kompakt 2023": ["t4", "t5", "t6", "t7"],
    }


def test_a_build_refused_part_way_by_a_failed_read_keeps_the_reads_before_it(
    followed, monkeypatch
):
    _cfg, fake, account = followed
    # r1 is read fourth and fails as an outage, not as a release that is gone.
    real = fake.release_tracks

    def failing(release_id):
        if release_id == "r1":
            fake.releases_asked_for.append(release_id)
            raise RuntimeError("the provider could not answer")
        return real(release_id)

    monkeypatch.setattr(fake, "release_tracks", failing)
    code, refused = drive(FULL)
    assert refused["cause"]["reason"] == "label-playlists-incomplete", refused
    kept = _stored()["reads"]
    # THE FAILED READ IS NOT AN ANSWER and is never kept.
    assert sorted(kept) == sorted(READ[:3])
    assert account._writes == 0


def test_a_park_whose_reads_cannot_be_written_is_still_told_as_the_park(
    followed, monkeypatch
):
    _cfg, fake, account = followed
    _parks_after(monkeypatch, fake, 3)

    _full_disk(monkeypatch)
    code, refused = drive(FULL)
    # THE STOP IS WHAT THE PERSON IS TOLD, never the failure to keep the reads.
    assert refused["cause"]["reason"] == "provider-cooldown", refused
    assert not kept_reads.path_for(LABEL_ID).exists()
    assert account._writes == 0


# ═══════════════════════════════════════════════════════════════════════════
# 2. The age
# ═══════════════════════════════════════════════════════════════════════════


def test_a_read_older_than_the_age_is_read_again(followed):
    _cfg, fake, _account = followed
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    _age_every_read(kept_reads.KEPT_FOR + timedelta(minutes=1), only={"r1", "r2"})
    fake.releases_asked_for.clear()

    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert sorted(fake.releases_asked_for) == ["r1", "r2"]
    # The read taken again replaces the old one, so a third run reads nothing.
    fake.releases_asked_for.clear()
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    assert fake.releases_asked_for == []


def test_a_read_just_inside_the_age_is_reused_and_named_as_old(followed):
    _cfg, fake, _account = followed
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    _age_every_read(kept_reads.KEPT_FOR - timedelta(hours=1))
    fake.releases_asked_for.clear()

    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert fake.releases_asked_for == []
    shown = refused["cause"]["detail"]["shown"]
    assert shown["release reads"].startswith(
        f"{len(READ)} release read(s) reused from an earlier run, the oldest 6 day(s) old, "
        f"and 0 read by this run"
    )


def test_a_read_dated_in_the_future_is_read_again(followed):
    _cfg, fake, _account = followed
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    _age_every_read(-timedelta(days=1), only={"r4"})
    fake.releases_asked_for.clear()
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    assert fake.releases_asked_for == ["r4"]


def test_the_age_is_seven_days():
    # The recommendation on the decisions page, 2026-11-01. A change to it is
    # Phillip's answer, and this pin is what moves with it.
    assert kept_reads.KEPT_FOR == timedelta(days=7)


# ═══════════════════════════════════════════════════════════════════════════
# 3. The gate run and the apply run read each release once between them
# ═══════════════════════════════════════════════════════════════════════════


def test_the_gate_run_and_the_apply_run_read_each_release_once(followed):
    _cfg, fake, account = followed
    code, done = _decided(FULL, (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    assert sorted(fake.releases_asked_for) == sorted(READ)
    assert account._writes > 0


def test_a_crawl_answered_build_reads_each_release_once_over_its_three_runs(
    followed, small_threshold
):
    _cfg, fake, account = followed
    code, done = _decided(FULL, (CRAWL, "crawl"), (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    assert sorted(fake.releases_asked_for) == sorted(READ)
    (folder_id,) = account.folder_names
    assert set(_years(account, folder_id)) == {"Kompakt 2021", "Kompakt 2022", "Kompakt 2023"}


def test_a_gone_release_is_kept_as_gone_and_counted_without_asking_again(followed):
    _cfg, fake, _account = followed
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    assert _stored()["reads"]["r7"]["gone"] is True
    fake.releases_asked_for.clear()
    code, refused = drive(FULL)
    assert fake.releases_asked_for == []
    assert "1 the provider no longer has" in refused["cause"]["detail"]["shown"]["catalogue"]


def test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year(followed):
    _cfg, fake, account = followed
    unplayable = FakeTrack("t2")
    unplayable.available = False
    fake.releases["r1"] = ([FakeTrack("t1"), unplayable], 2021)
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    assert _stored()["reads"]["r1"]["tracks"] == [
        {"id": "t1", "available": True},
        {"id": "t2", "available": False},
    ]
    code, done = _decided(FULL, (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    (folder_id,) = account.folder_names
    assert _years(account, folder_id)["Kompakt 2021"] == ["t1"]


def test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one(followed):
    _cfg, fake, account = followed
    # r2 is listed under 2022 and the provider dates it 2019.
    fake.releases["r2"] = ([FakeTrack("t3")], 2019)
    assert drive(FULL)[0] == int(ExitCode.DECISION_REQUIRED)
    assert _stored()["reads"]["r2"]["year"] == 2019
    code, done = _decided(FULL, (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    (folder_id,) = account.folder_names
    assert _years(account, folder_id)["Kompakt 2019"] == ["t3"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. The screens
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_build_says_its_reads_are_kept_for_the_apply_run(followed):
    _cfg, _fake, _account = followed
    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["release reads"] == (
        f"all {len(READ)} release read(s) made by this run, and kept for 7 day(s), so "
        f"the run that applies the plan reads none of them again"
    )


def test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest(
    followed, small_threshold, monkeypatch
):
    cfg, fake, _account = followed
    # A first run under a high threshold reads four releases and is parked.
    monkeypatch.setattr(playlists_cli, "FULL_BUILD_CALLS", 1000)
    switch = _parks_after(monkeypatch, fake, 4)
    assert drive(FULL)[0] != int(ExitCode.OK)
    monkeypatch.setattr(playlists_cli, "FULL_BUILD_CALLS", 4)
    switch["after"] = None

    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CRAWL
    shown = refused["cause"]["detail"]["shown"]
    rest = len(LISTED) - 4
    assert shown["estimate"].startswith(
        f"{len(LISTED)} release(s) listed and 4 of them read by an earlier run within "
        f"the last 7 day(s), so reading the other {rest} is at least {2 * rest} "
        f"provider call(s)"
    )
    assert shown["kept reads"] == (
        "4 release read(s) kept from an earlier run, the oldest 0 minute(s) old; a "
        "read is taken again once it is 7 day(s) old"
    )

    # THE GATE'S PLAN carries the kept count, and its digest is the listing's.
    reads = kept_reads.KeptReads.load(LABEL_ID)
    listed = playlists_cli.list_catalogue(cfg, _entry(), fake)
    counted = playlists_cli.estimate(cfg, _entry(), listed, reads)
    (item,) = counted.plan()["items"]
    assert (item["releases"], item["kept"], item["calls"]) == (len(LISTED), 4, 2 * rest)
    unkept = playlists_cli.estimate(cfg, _entry(), listed)
    assert unkept.kept == 0 and counted.plan()["digest"] == unkept.plan()["digest"]


def test_a_resume_under_the_same_crawl_answer_is_not_stale(
    followed, small_threshold, monkeypatch
):
    _cfg, fake, _account = followed
    code, refused = drive(FULL)
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, CRAWL, "crawl", "--actor", "a-person"])[0] == 0
    switch = _parks_after(monkeypatch, fake, 3)
    assert drive(["--run", run_id, *FULL])[0] != int(ExitCode.OK)
    switch["after"] = None
    fake.releases_asked_for.clear()

    # THE CRAWL DIGEST IS OVER THE LISTING, not over what is left to read, so
    # the answer given before the park still holds for the run that resumes.
    code, refused = drive(["--run", run_id, *FULL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    assert sorted(fake.releases_asked_for) == sorted(READ[3:])


# ═══════════════════════════════════════════════════════════════════════════
# 5. A store that cannot be read
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "written, problem",
    [
        ("{not json", "it is not JSON"),
        ("[]", "the document is a list, not a map"),
        ('{"version": 99, "label_id": "kompakt", "reads": {}}', "it says version 99"),
        ('{"version": 1, "label_id": "another", "reads": {}}', "it names the label"),
        ('{"version": 1, "label_id": "kompakt", "reads": []}', "its reads are not a map"),
        (
            '{"version": 1, "label_id": "kompakt", "reads": {"r1": {"year": 2021, '
            '"tracks": []}}}',
            "carries no instant",
        ),
        (
            '{"version": 1, "label_id": "kompakt", "reads": {"r1": {"read_at": '
            '"2026-11-01T00:00:00+00:00", "year": 2021, "tracks": [{"id": 5}]}}}',
            "is malformed",
        ),
        (
            '{"version": 1, "label_id": "kompakt", "reads": {"r1": {"read_at": '
            '"2026-11-01T00:00:00+00:00", "year": "2021", "tracks": []}}}',
            "carries the year",
        ),
        (
            '{"version": 1, "label_id": "kompakt", "reads": {"r1": {"read_at": '
            '"2026-11-01T00:00:00+00:00", "gone": "yes"}}}',
            "says gone",
        ),
        (
            '{"version": 1, "label_id": "kompakt", "reads": {"r1": {"read_at": '
            '"2026-11-01T00:00:00+00:00", "year": true, "tracks": []}}}',
            "carries the year",
        ),
    ],
)
def test_a_store_that_cannot_be_read_refuses_before_any_release_is_read(
    followed, written, problem
):
    _cfg, fake, account = followed
    path = kept_reads.path_for(LABEL_ID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(written, encoding="utf-8")

    code, refused = drive(FULL)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == kept_reads.UNUSABLE
    assert problem in refused["cause"]["detail"]["problem"]
    # BEFORE THE LISTING TOO: not a roster, a page or a release was asked for.
    assert fake.asked_for == [] and fake.releases_asked_for == []
    assert account._writes == 0
    # NEVER REWRITTEN: the refused document is left for the person to repair.
    assert path.read_text(encoding="utf-8") == written


def test_a_releases_build_neither_reads_nor_writes_the_store(followed):
    cfg, fake, _account = followed
    path = kept_reads.path_for(LABEL_ID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    _took(cfg, ("r3", "2023"))
    code, refused = drive(RELEASES)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert path.read_text(encoding="utf-8") == "{not json"


# ═══════════════════════════════════════════════════════════════════════════
# 6. The store on its own
# ═══════════════════════════════════════════════════════════════════════════


def test_reads_are_written_every_flush_and_not_only_at_the_end(installed, monkeypatch):
    del installed
    monkeypatch.setattr(kept_reads, "FLUSH_EVERY", 2)
    store = kept_reads.KeptReads.load(LABEL_ID)
    store.keep("a", [FakeTrack("t1")], 2020)
    assert not kept_reads.path_for(LABEL_ID).exists()
    store.keep_gone("b")
    assert sorted(_stored()["reads"]) == ["a", "b"]


def test_a_flush_with_nothing_new_writes_nothing(installed):
    del installed
    kept_reads.KeptReads.load(LABEL_ID).flush()
    assert not kept_reads.path_for(LABEL_ID).exists()


# ═══════════════════════════════════════════════════════════════════════════
# 7. A store that cannot be written, the review's round 1
# ═══════════════════════════════════════════════════════════════════════════


def _full_disk(monkeypatch) -> list[str]:
    """The kept reads' writes refused as a full disk; every other write goes through."""
    tried: list[str] = []
    real = kept_reads.config.atomic_write_bytes
    store = kept_reads.path_for(LABEL_ID)

    def refused(payload, path, **kwargs):
        if path != store:
            return real(payload, path, **kwargs)
        tried.append(str(path))
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(kept_reads.config, "atomic_write_bytes", refused)
    return tried


def test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so(
    followed, monkeypatch
):
    _cfg, fake, account = followed
    tried = _full_disk(monkeypatch)
    code, refused = drive(FULL)
    # THE PLAN, NOT A DEFECT: the store saves calls and holds nothing else.
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    assert tried
    said = refused["cause"]["detail"]["shown"]["release reads"]
    assert said == (
        f"all {len(READ)} release read(s) made by this run; the reads made by this "
        f"run could not be kept (OSError: [Errno 28] No space left on device), so a "
        f"later run reads them again"
    )

    code, done = _decided(FULL, (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-reads-unkept"]
    assert account._writes > 0
    assert not kept_reads.path_for(LABEL_ID).exists()


def test_a_periodic_write_that_fails_does_not_stop_the_read(followed, monkeypatch):
    _cfg, fake, _account = followed
    monkeypatch.setattr(kept_reads, "FLUSH_EVERY", 2)
    tried = _full_disk(monkeypatch)
    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert sorted(fake.releases_asked_for) == sorted(READ)
    # Tried after every second read, then once more on the way out.
    assert len(tried) == len(READ) // 2 + 1


def test_a_file_where_the_labels_directory_belongs_still_shows_the_plan(followed):
    _cfg, _fake, _account = followed
    directory = kept_reads.path_for(LABEL_ID).parent
    directory.parent.mkdir(parents=True, exist_ok=True)
    directory.write_text("not a directory", encoding="utf-8")
    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert "could not be kept" in refused["cause"]["detail"]["shown"]["release reads"]
    assert directory.read_text(encoding="utf-8") == "not a directory"


def test_a_write_that_succeeds_after_one_failed_clears_what_was_said(installed, monkeypatch):
    del installed
    store = kept_reads.KeptReads.load(LABEL_ID)
    store.keep("a", [FakeTrack("t1")], 2020)
    real = kept_reads.config.atomic_write_bytes
    _full_disk(monkeypatch)
    store.flush()
    assert store.unkept.startswith("OSError")
    monkeypatch.setattr(kept_reads.config, "atomic_write_bytes", real)
    store.flush()
    assert store.unkept == "" and sorted(_stored()["reads"]) == ["a"]


def test_the_build_gate_counts_the_calls_left_after_the_kept_reads(followed, monkeypatch):
    _cfg, fake, _account = followed
    switch = _parks_after(monkeypatch, fake, 4)
    assert drive(FULL)[0] != int(ExitCode.OK)
    switch["after"] = None
    code, refused = drive(FULL)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    rest = len(LISTED) - 4
    assert refused["cause"]["detail"]["shown"]["provider calls"] == (
        f"{len(LISTED)} release(s) listed, at least {2 * rest} provider call(s) to "
        f"read the tracks of the {rest} not kept from an earlier run"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 8. The store's numbers
# ═══════════════════════════════════════════════════════════════════════════


def test_the_store_is_written_every_fifty_reads():
    # A hundred seconds of calls at the default pace is what a kill can lose.
    assert kept_reads.FLUSH_EVERY == 50


def test_a_read_exactly_the_age_old_is_read_again(installed, monkeypatch):
    del installed
    start = datetime(2026, 11, 1, 12, 0, tzinfo=kept_reads.timezone.utc)
    monkeypatch.setattr(kept_reads, "clock", lambda: start)
    store = kept_reads.KeptReads.load(LABEL_ID)
    store.keep("a", [FakeTrack("t1")], 2020)
    store.flush()
    monkeypatch.setattr(kept_reads, "clock", lambda: start + kept_reads.KEPT_FOR)
    assert kept_reads.KeptReads.load(LABEL_ID).fresh("a") is None
    monkeypatch.setattr(
        kept_reads, "clock", lambda: start + kept_reads.KEPT_FOR - timedelta(seconds=1)
    )
    assert kept_reads.KeptReads.load(LABEL_ID).fresh("a") is not None


def test_a_year_given_as_a_bool_is_kept_as_no_year(installed):
    del installed
    store = kept_reads.KeptReads.load(LABEL_ID)
    store.keep("a", [FakeTrack("t1")], True)
    store.flush()
    assert _stored()["reads"]["a"]["year"] is None


def test_a_release_named_twice_is_counted_once_as_kept(installed):
    del installed
    store = kept_reads.KeptReads.load(LABEL_ID)
    store.keep("a", [FakeTrack("t1")], 2020)
    assert store.kept(["a", "a", "b"])[0] == 1
    assert store.reused == 0


@pytest.mark.parametrize(
    "age, said",
    [
        (timedelta(minutes=59), "59 minute(s)"),
        (timedelta(minutes=60), "1 hour(s)"),
        (timedelta(hours=47), "47 hour(s)"),
        (timedelta(hours=48), "2 day(s)"),
    ],
)
def test_an_age_reads_in_minutes_then_hours_then_days(age, said):
    assert kept_reads.age_text(age) == said
