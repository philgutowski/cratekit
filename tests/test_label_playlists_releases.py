"""U191: a label sync's taken releases reach the year playlists without the catalogue.

``crate label playlists LABEL --releases`` reads the releases a label sync go
took for the label, and only those, and adds their tracks to the label's year
playlists through the same plan a full build uses. A full build reads the
listing first and, over an estimate of provider calls, stops at its own gate
before any release is read. Every scenario the brief names is here, driven
through the real dispatcher with the catalogue and the account faked, as
``tests/test_label_playlists.py`` drives the full build. The live read back of
the account is owed to an attended sitting and is not claimed here.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cratekit.cli.output import digest_of, timestamp
from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from cratekit.label import playlists_cli, sync_cli
from cratekit.modules.outbound import folders, ledger
from tests.cli_drive import drive
from tests.label_fakes import FakePagedArtist, FakeRelease, FakeTrack
from tests.test_label_playlists import BUILD, LABEL, LABEL_ID, LISTED, _entry, _years
from tests.test_label_playlists import followed as followed  # noqa: PLC0414 - fixture
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

CRAWL = playlists_cli.CRAWL_GATE
RELEASES = ["label", "playlists", LABEL, "--releases"]


def _took(cfg, *releases: tuple[str, str], settled: bool = True) -> None:
    """Record one ``pick`` answer that took ``releases``, settled by a go or not."""
    document = sync_cli.load_record(cfg)
    entry = {
        "label_id": LABEL_ID,
        "label_name": LABEL,
        "answer": sync_cli.PICK,
        "taken": [identity for identity, _year in releases],
        "answered_at": timestamp(),
        "releases": [
            {
                "identity": identity,
                "artist": "Some Artist",
                "title": f"Title {identity}",
                "year": year,
                "tracks": 1,
                "size": 1,
                "item_id": None,
                "payload": {},
            }
            for identity, year in releases
        ],
    }
    if settled:
        entry[sync_cli.SETTLED] = {"run": "a-go", "job": None, "at": timestamp()}
    document["answers"].append(entry)
    sync_cli.write_record(cfg, document)


def _decided(argv: list[str], *answers: tuple[str, str]) -> tuple[int, dict]:
    """Each gate answered on its own, in turn, then the run that carries them out."""
    code, refused = drive(argv)
    run_id = refused.get("run_id")
    for gate, option in answers:
        assert code == int(ExitCode.DECISION_REQUIRED), refused
        assert refused["cause"]["detail"]["gate"] == gate
        assert drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])[0] == 0
        code, refused = drive(["--run", run_id, *argv])
    return code, refused


def _releases(option: str = "apply") -> tuple[int, dict]:
    return _decided(RELEASES, (BUILD, option))


def _reads(monkeypatch, account) -> list[str]:
    """Every playlist whose tracks the plan reads off the account."""
    read: list[str] = []
    real = account.playlist_tracks

    def recorded(playlist_id):
        read.append(playlist_id)
        return real(playlist_id)

    monkeypatch.setattr(account, "playlist_tracks", recorded)
    return read


def _hand_made(account, title: str, folder_id: str, tracks: list[str]) -> str:
    made = account.create_playlist(title)
    account.move_to_folder(made, folder_id)
    account.playlists[made] = list(tracks)
    return made


# ═══════════════════════════════════════════════════════════════════════════
# 1. The releases a sync took, and nothing else
# ═══════════════════════════════════════════════════════════════════════════


def test_two_taken_releases_in_one_year_add_to_that_year_only(followed, monkeypatch):
    cfg, fake, account = followed
    account.folder_names = {"f-hand": LABEL}
    other = _hand_made(account, "Kompakt 2021", "f-hand", ["t1"])
    year = _hand_made(account, "Kompakt 2023", "f-hand", ["t4"])
    account.created.clear()
    writes = account._writes
    read = _reads(monkeypatch, account)
    _took(cfg, ("r3", "2023"), ("r4", "2023"))

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    # THE TAKEN RELEASES AND NOTHING ELSE: no roster, no listing, no verifier,
    # and no other release's tracks.
    assert fake.asked_for == []
    # Once by the run that asked the gate and once by the run that applied.
    assert sorted(fake.releases_asked_for) == ["r3", "r3", "r4", "r4"]
    assert account.playlists[year] == ["t4", "t5", "t6", "t7"]
    # A YEAR NO TAKEN RELEASE NAMES is neither read nor written.
    assert account.playlists[other] == ["t1"]
    assert other not in read
    assert account.created == [] and account.folders_created == []
    assert account._writes > writes
    (step,) = done["data"]["items"][1:]
    assert (step["year"], step["action"], step["add"]) == ("2023", folders.ADOPT, 3)


def test_a_missing_year_playlist_is_created_in_the_folder(followed):
    cfg, fake, account = followed
    account.folder_names = {"f-hand": LABEL}
    fake.releases["r8"] = ([FakeTrack("t10"), FakeTrack("t11")], 2026)
    _took(cfg, ("r8", "2026"))

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert account.folders_created == [] and account.created == ["Kompakt 2026"]
    assert _years(account, "f-hand") == {"Kompakt 2026": ["t10", "t11"]}
    assert sorted(ledger.label_shape(cfg, LABEL_ID).years["2026"].added) == ["t10", "t11"]


def test_a_missing_folder_is_created_with_only_the_taken_years(followed):
    cfg, _fake, account = followed
    _took(cfg, ("r1", "2021"))

    code, refused = drive(RELEASES)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["year playlists"] == [
        "Kompakt 2021: create it private, put it in the folder, add 2 of 2 track(s)"
    ]
    assert shown["releases read"] == ["Some Artist - Title r1 (2021)"]
    assert account._writes == 0

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert account.folders_created == [LABEL]
    (folder_id,) = account.folder_names
    assert _years(account, folder_id) == {"Kompakt 2021": ["t1", "t2"]}
    assert ledger.label_shape(cfg, LABEL_ID).folder_id == folder_id


def test_a_release_the_provider_no_longer_lists_is_counted_not_refused(followed):
    cfg, fake, account = followed
    # r7 is listed in the fake catalogue and the provider has nothing for it.
    _took(cfg, ("r7", "2020"), ("r2", "2022"))

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert sorted(fake.releases_asked_for) == ["r2", "r2", "r7", "r7"]
    (folder_id,) = account.folder_names
    assert _years(account, folder_id) == {"Kompakt 2022": ["t3"]}
    code, refused = drive(RELEASES)
    assert "1 the provider no longer has" in refused["cause"]["detail"]["shown"]["catalogue"]


def test_a_second_run_plans_nothing(followed):
    cfg, _fake, account = followed
    _took(cfg, ("r3", "2023"), ("r4", "2023"))
    assert _releases()[0] == int(ExitCode.OK)
    writes = account._writes

    code, refused = drive(RELEASES)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert "nothing to write" in shown
    assert refused["cause"]["detail"]["shown"]["year playlists"] == [
        "Kompakt 2023: use the one already built, add 0 of 4 track(s)"
    ]
    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert account._writes == writes


def test_an_answer_no_go_has_taken_is_not_read(followed):
    cfg, fake, account = followed
    _took(cfg, ("r3", "2023"), settled=False)

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-nothing-taken"]
    # NOT EVEN THE FOLDER is made for a sync that took nothing.
    assert fake.releases_asked_for == [] and fake.asked_for == []
    assert account._writes == 0 and account.folders_created == []


def test_another_labels_answers_are_not_read(followed):
    cfg, fake, account = followed
    _took(cfg, ("r3", "2023"))
    document = sync_cli.load_record(cfg)
    document["answers"][0]["label_id"] = "another-label"
    sync_cli.write_record(cfg, document)

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-nothing-taken"]
    assert fake.releases_asked_for == [] and account._writes == 0


def test_a_label_nobody_follows_is_still_a_plan_of_nothing(followed):
    _cfg, fake, account = followed
    code, done = _decided(["label", "playlists", "Nobody Follows This", "--releases"], (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-not-followed"]
    assert fake.asked_for == [] and account._writes == 0


def test_an_answer_given_to_a_full_build_is_not_taken_for_a_releases_build(followed):
    cfg, _fake, account = followed
    # Every confirmed, dated release taken, so both builds plan the same writes.
    _took(cfg, ("r1", "2021"), ("r2", "2022"), ("r3", "2023"), ("r4", "2023"))
    full = ["label", "playlists", LABEL]
    code, refused = drive(full)
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, BUILD, "apply", "--actor", "a-person"])[0] == 0

    code, refused = drive(["--run", run_id, *RELEASES])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    assert account._writes == 0


# ═══════════════════════════════════════════════════════════════════════════
# 2. A full build is counted before it is read
# ═══════════════════════════════════════════════════════════════════════════


def test_the_estimate_is_two_calls_a_release_at_the_configured_pace():
    under = playlists_cli.Estimate("x", "X", releases=250, pace_s=1.0)
    over = playlists_cli.Estimate("x", "X", releases=251, pace_s=1.5)
    assert (under.calls, under.seconds, under.over) == (500, 500, False)
    assert (over.calls, over.seconds, over.over) == (502, 753, True)
    assert playlists_cli.FULL_BUILD_CALLS == 500


def test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line():
    """U193. A ceiling below the build's line would stop the crawl part way, so
    the gate says so before any release is read, with the one run figure."""
    under_line = playlists_cli.Estimate("x", "X", releases=100, pace_s=1.0, ceiling=150, spent=3)
    assert under_line.calls == 200 < playlists_cli.FULL_BUILD_CALLS
    assert under_line.over_ceiling and under_line.over
    assert under_line.one_run == 400
    said = under_line.shown()["call ceiling"]
    assert "more than the 150 provider calls one command may make" in said
    assert "3 of them spent on the listing already" in said
    assert "--calls 400" in said
    # ONLY THE CEILING ASKS HERE, so the reason names it and not the build's line.
    assert "ceiling of 150" in under_line.shown()["why this asks"]

    roomy = playlists_cli.Estimate("x", "X", releases=251, pace_s=1.0, ceiling=5000)
    assert roomy.over and not roomy.over_ceiling
    assert "call ceiling" not in roomy.shown()
    assert "a full build over 500" in roomy.shown()["why this asks"]

    at_default = playlists_cli.Estimate("x", "X", releases=250, pace_s=1.0)
    assert at_default.ceiling == config.DEFAULT_PROVIDER_CALLS_PER_COMMAND
    assert not at_default.over, "exactly the ceiling is a crawl that finishes"


def test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate(followed, monkeypatch):
    """Driven: no threshold patched, the seven release catalogue is fourteen
    calls, and ``--calls 5`` puts that over this run's ceiling."""
    _cfg, fake, account = followed
    verified = _verifier_calls(monkeypatch, fake)
    code, refused = drive(["--calls", "5", "label", "playlists", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CRAWL
    shown = refused["cause"]["detail"]["shown"]
    assert "more than the 5 provider calls one command may make" in shown["call ceiling"]
    assert fake.releases_asked_for == [] and verified == []
    assert account._writes == 0


@pytest.fixture
def small_threshold(monkeypatch):
    """A threshold the seven release fake catalogue is over, at fourteen calls."""
    monkeypatch.setattr(playlists_cli, "FULL_BUILD_CALLS", 4)


def _verifier_calls(monkeypatch, fake) -> list[str]:
    asked: list[str] = []
    real = fake.search_release

    def recorded(claimed, release):
        asked.append(str(getattr(release, "id", "")))
        return real(claimed, release)

    monkeypatch.setattr(fake, "search_release", recorded)
    return asked


def test_a_full_build_over_the_threshold_stops_at_its_gate_after_the_count(
    followed, small_threshold, monkeypatch
):
    _cfg, fake, account = followed
    verified = _verifier_calls(monkeypatch, fake)
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CRAWL
    shown = refused["cause"]["detail"]["shown"]
    assert shown["estimate"].startswith(
        f"{len(LISTED)} release(s) listed, so reading their tracks is at least "
        f"{2 * len(LISTED)} provider call(s)"
    )
    assert "--releases" in shown["instead"]
    # THE COUNT AND NOTHING MORE: the listing was read, no release was.
    assert fake.asked_for == [LABEL_ID]
    assert fake.releases_asked_for == [] and verified == []
    assert account._writes == 0


def test_a_full_build_declined_at_its_crawl_gate_reads_and_writes_nothing(
    followed, small_threshold
):
    _cfg, fake, account = followed
    code, done = _decided(["label", "playlists", LABEL], (CRAWL, "abort"))
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert fake.releases_asked_for == [] and account._writes == 0


def test_a_full_build_answered_crawl_reads_the_catalogue_and_asks_the_build_gate(
    followed, small_threshold
):
    _cfg, fake, account = followed
    code, done = _decided(["label", "playlists", LABEL], (CRAWL, "crawl"), (BUILD, "apply"))
    assert code == int(ExitCode.OK), done
    (folder_id,) = account.folder_names
    assert set(_years(account, folder_id)) == {"Kompakt 2021", "Kompakt 2022", "Kompakt 2023"}
    assert "r1" in fake.releases_asked_for


def test_a_full_build_under_the_threshold_asks_only_the_build_gate(followed):
    _cfg, fake, _account = followed
    code, refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    assert refused["cause"]["detail"]["shown"]["provider calls"] == (
        f"{len(LISTED)} release(s) listed, at least {2 * len(LISTED)} provider call(s) "
        f"to read their tracks"
    )


def test_the_crawl_gate_is_asked_again_when_the_listing_grows(
    followed, small_threshold, monkeypatch
):
    _cfg, fake, account = followed
    argv = ["label", "playlists", LABEL]
    code, refused = drive(argv)
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, CRAWL, "crawl", "--actor", "a-person"])[0] == 0
    fake.artists[LABEL_ID] = FakePagedArtist([*LISTED, FakeRelease("r9", year="2024")])

    code, refused = drive(["--run", run_id, *argv])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["gate"] == CRAWL
    assert fake.releases_asked_for == [] and account._writes == 0


# ═══════════════════════════════════════════════════════════════════════════
# 3. What the review of round 1 drove
# ═══════════════════════════════════════════════════════════════════════════


def test_a_go_whose_every_release_is_gone_says_so_and_not_that_nothing_was_taken(followed):
    cfg, fake, account = followed
    _took(cfg, ("r7", "2020"))

    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-nothing-left"]
    assert "1 gone from the provider" in done["warnings"][0]["message"]
    assert account._writes == 0 and account.folders_created == []


def test_a_release_named_only_by_its_review_item_is_never_asked_for_or_shown_as_read(followed):
    cfg, fake, _account = followed
    _took(cfg, ("item:abc123", "2023"), ("r3", "2023"))

    code, refused = drive(RELEASES)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["releases read"] == ["Some Artist - Title r3 (2023)"]
    assert "0 the provider no longer has, 1 named by no release" in shown["catalogue"]
    assert fake.releases_asked_for == ["r3"]


def test_a_release_the_provider_dates_by_nothing_takes_the_year_its_answer_recorded(followed):
    cfg, _fake, account = followed
    # r5 carries no year at the provider. Its answer recorded 2019 for one and
    # nothing usable for the other, which is left out as undated.
    _took(cfg, ("r5", "2019"))
    assert _releases()[0] == int(ExitCode.OK)
    (folder_id,) = account.folder_names
    assert _years(account, folder_id) == {"Kompakt 2019": ["t8"]}


def test_a_recorded_year_that_is_not_four_digits_is_undated(followed):
    cfg, _fake, account = followed
    _took(cfg, ("r5", "19"))
    code, done = _releases()
    assert code == int(ExitCode.OK), done
    assert [w["code"] for w in done["warnings"]] == ["label-playlists-nothing-left"]
    assert "1 with no year" in done["warnings"][0]["message"]
    assert account._writes == 0


def test_a_full_builds_digest_is_the_plan_identity_alone(followed):
    cfg, fake, account = followed
    planned = folders.plan(
        cfg, playlists_cli.read_catalogue(cfg, _entry(), fake), account
    )
    assert playlists_cli.plan_payload(planned, name=LABEL)["digest"] == digest_of(
        planned.identity()
    )


def test_the_estimate_reads_the_configured_pace(followed):
    cfg, fake, _account = followed
    listed = playlists_cli.list_catalogue(cfg, _entry(), fake)
    paced = SimpleNamespace(provider=config.ProviderConfig(min_interval_s=3.0))
    counted = playlists_cli.estimate(paced, _entry(), listed)
    assert (counted.releases, counted.pace_s, counted.seconds) == (len(LISTED), 3.0, 42)


def test_a_full_build_lists_the_label_once_per_run(followed):
    _cfg, fake, _account = followed
    code, _refused = drive(["label", "playlists", LABEL])
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert fake.asked_for == [LABEL_ID]
