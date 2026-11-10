"""R-790: a label sweep offers a window of its newest releases, not its catalogue.

The first sweep of 32 favourite labels filed 2,832 releases at a cap of four
hundred each, back catalogue included, and nothing said which were new. These
tests drive the window through the real dispatcher, queue and worker where the
property is about what a person is handed, and through the sweep engine where
it is about which release takes a place.

NO DATE FLOOR, ANYWHERE (KTD11). A later sweep files only what is new because
the releases it already offered hold their places in the window, and the
watermark tests below advance every watermark past every release to prove
nothing reads one.

NOTHING HERE ACCEPTS A RELEASE. Every filed item is asserted undecided, because
a download follows only a decision the author makes in review.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.core import config, review, tombstone
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import catalogue, harvest, sweep
from cratekit.label import marks as label_marks
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, watermarks
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_config import valid_data
from tests.test_label_workers import queued_sweep

LABEL = "Anjunadeep"
SLUG = "anjunadeep"


@pytest.fixture
def installed(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    return resolved


def catalogue_of(count: int, *, newest: int = 2026) -> list[FakeRelease]:
    """``count`` releases, one a year, the newest first, ``r<year>`` each."""
    return [FakeRelease(f"r{year}", year=str(year)) for year in range(newest, newest - count, -1)]


def bind(monkeypatch, releases: list[FakeRelease]) -> FakeCatalogue:
    fake = FakeCatalogue(artists={SLUG: FakePagedArtist(releases)})
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def sweep_once() -> None:
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed


def filed(cfg: config.Config) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(
            review.list_items(store, queue=str(Queue.LABEL_RELEASE), limit=None)
        )


def grouped(by: str) -> list[dict]:
    code, envelope = drive(["review", "list", "--queue", "label-release", "--group-by", by])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["items"]


def register(*argv: str) -> None:
    code, envelope = drive(["label", "registry", "add", LABEL, *argv])
    assert code == int(ExitCode.OK), envelope


# ═══════════════════════════════════════════════════════════════════════════
# 1. Through the worker: what a person is handed
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty(installed, monkeypatch):
    register()
    bind(monkeypatch, catalogue_of(50))
    sweep_once()

    items = filed(installed)
    assert [item.payload["identity"] for item in items] == [f"r{y}" for y in range(2026, 2016, -1)]
    assert all(item.verdict is None for item in items)

    (row,) = grouped("label")
    assert row["label"] == SLUG
    assert row["label_name"] == LABEL
    assert row["items"] == 10
    assert row["beyond"] == 40


def test_a_second_sweep_files_only_the_new_release_and_refiles_nothing(installed, monkeypatch):
    register()
    releases = catalogue_of(50)
    bind(monkeypatch, releases)
    sweep_once()
    first = {item.payload["identity"]: item for item in filed(installed)}

    bind(monkeypatch, [FakeRelease("r2027", year="2027"), *releases])
    sweep_once()
    second = {item.payload["identity"]: item for item in filed(installed)}

    assert set(second) - set(first) == {"r2027"}
    assert len(second) == 11
    for identity, item in first.items():
        assert second[identity].payload[sweep.SWEEP_RUN] == item.payload[sweep.SWEEP_RUN]
    assert second["r2027"].payload[sweep.SWEEP_RUN] != first["r2026"].payload[sweep.SWEEP_RUN]
    assert all(item.verdict is None for item in second.values())

    runs = grouped("run")
    assert [row["items"] for row in runs] == [10, 1]
    assert [row["labels"] for row in runs] == [1, 1]
    assert [row["beyond"] for row in runs] == [40, 41]
    (label_row,) = grouped("label")
    assert label_row["items"] == 11
    assert label_row["beyond"] == 41
    assert label_row["swept"] == runs[1]["run"]


def test_a_label_whose_offer_is_raised_to_thirty_files_thirty(installed, monkeypatch):
    register("--offer", "30")
    bind(monkeypatch, catalogue_of(50))
    sweep_once()
    assert len(filed(installed)) == 30
    (row,) = grouped("label")
    assert row["beyond"] == 20


def test_raising_a_label_offer_after_a_sweep_files_the_difference(installed, monkeypatch):
    register()
    bind(monkeypatch, catalogue_of(50))
    sweep_once()
    code, envelope = drive(["label", "registry", "set", LABEL, "--offer", "30"])
    assert code == int(ExitCode.OK), envelope
    sweep_once()
    assert len(filed(installed)) == 30
    assert [row["items"] for row in grouped("run")] == [10, 20]


def test_the_configured_offer_is_the_default_for_every_label(installed, monkeypatch):
    config.save(replace(installed, labels=config.LabelsConfig(offer_per_sweep=4)))
    config.reset_cache()
    register()
    bind(monkeypatch, catalogue_of(50))
    sweep_once()
    assert len(filed(installed)) == 4
    (row,) = grouped("label")
    assert row["beyond"] == 46


def test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted(
    installed, monkeypatch
):
    """The increment slices to the track limit after the listing, so a window
    wider than that would file fewer than it said and count nothing for the rest.
    """
    register("--track-limit", "3")
    bind(monkeypatch, catalogue_of(50))
    sweep_once()
    assert len(filed(installed)) == 3
    (row,) = grouped("label")
    assert row["beyond"] == 47


def test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, catalogue_of(50))
    sweep_once()
    sweep_once()
    runs = grouped("run")
    assert [row["items"] for row in runs] == [10, 0]
    assert [row["beyond"] for row in runs] == [40, 40]


def test_an_item_filed_before_runs_were_recorded_groups_as_an_unrecorded_run(installed):
    with review.open_store(installed) as store:
        sweep.offer_release(
            store,
            run.Candidate(
                identity="old",
                recency="2020",
                payload={"label_id": SLUG, "label_name": LABEL, "identity": "old"},
            ),
        )
    (row,) = grouped("run")
    assert row == {"run": None, "items": 1, "labels": 1, "beyond": None, "held": 0}


# ═══════════════════════════════════════════════════════════════════════════
# 2. The engine: which release takes a place
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def entry(installed):
    del installed
    store = labels.RegistryStore()
    label_id = store.add(LABEL)
    return store.load().by_id(label_id)


def counting_confirm():
    asked: list[str] = []

    def search(claimed, release):
        asked.append(release.id)
        return {"verdict": "confirmed", "resolved_label": claimed, "source": "fixture", "notes": ""}

    return search, asked


def test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again(installed, entry):
    verify, asked = counting_confirm()
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(catalogue_of(20)),
        verify=verify,
        offered={"r2026", "r2025"},
        limit=5,
    )
    assert [c.identity for c in found.candidates] == ["r2024", "r2023", "r2022"]
    assert found.held == 2
    assert found.beyond == 15
    assert "r2026" not in asked and "r2025" not in asked


def test_an_owned_release_takes_no_place_in_the_window(installed, entry):
    verify, _ = counting_confirm()
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(catalogue_of(20)),
        verify=verify,
        owned={"r2026", "r2024"},
        limit=3,
    )
    assert [c.identity for c in found.candidates] == ["r2025", "r2023", "r2022"]
    assert found.beyond == 15


def test_a_tombstoned_release_takes_no_place_in_the_window(installed, entry):
    DecisionStore(tombstone.STORE_KEY, installed).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist="Label Act", title="Release r2026"),
        actor="test",
    )
    verify, _ = counting_confirm()
    found = sweep.list_for_label(
        installed, entry, artist=FakePagedArtist(catalogue_of(5)), verify=verify, limit=2
    )
    assert [c.identity for c in found.candidates] == ["r2025", "r2024"]
    assert [c.identity for c in found.suppressed] == ["r2026"]
    assert found.beyond == 2


def test_a_catalogue_shorter_than_the_window_has_nothing_beyond(installed, entry):
    verify, _ = counting_confirm()
    found = sweep.list_for_label(
        installed, entry, artist=FakePagedArtist(catalogue_of(3)), verify=verify, limit=10
    )
    assert len(found.candidates) == 3
    assert found.beyond == 0


def test_the_window_defaults_to_the_configuration_and_the_entry_overrides_it(installed, entry):
    verify, _ = counting_confirm()
    small = replace(installed, labels=config.LabelsConfig(offer_per_sweep=2))
    found = sweep.list_for_label(small, entry, artist=FakePagedArtist(catalogue_of(9)), verify=verify)
    assert len(found.candidates) == 2
    found = sweep.list_for_label(
        small, replace(entry, offer=6), artist=FakePagedArtist(catalogue_of(9)), verify=verify
    )
    assert len(found.candidates) == 6


def test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones(
    installed, entry
):
    """KTD11, at the window: no watermark decides scope, before or after a sweep."""
    label_marks.advance(installed, entry.label_id, year="2099")
    marks = watermarks.WatermarkStore(installed)
    marks.advance("labels", cursor="r2026", items=1, library_id=installed.library.volume_id)
    source = sweep.LabelSource(
        installed,
        registry=labels.Registry(labels={entry.label_id: entry}),
        artists={entry.label_id: FakePagedArtist(catalogue_of(12))},
        verify=counting_confirm()[0],
    )
    result = run.increment(
        source,
        owned=set(),
        limit=labels.effective_limit(entry),
        watermarks=marks,
        artifacts=artifacts.ArtifactRegistry(installed),
        run_id="run-past-the-mark",
        staging=Path(installed.paths.download_staging),
    )
    assert list(result.processed) == [f"r{y}" for y in range(2026, 2016, -1)]
    assert source.listings[0][1].beyond == 2


# ═══════════════════════════════════════════════════════════════════════════
# U238: what lies past the window is counted by the label's own copyright line
# ═══════════════════════════════════════════════════════════════════════════


def mixed_roster(label: str = LABEL) -> list[FakeRelease]:
    """Two artists on one roster, newest first, and two releases with no line.

    The label's act on the even years 2026 to 2008, each crediting the label;
    another act on the odd years 2025 to 2007, each crediting another label;
    then 2006 and 2005 by the label's act with no copyright line at all, the
    shape a listing that omitted the field leaves. Measured live (Atipic, 414
    counted past the window for about 27 of its own) this is the roster that
    used to be counted whole.
    """
    own = [
        FakeRelease(f"own{year}", year=str(year), copyright=f"(P) {year} {label}")
        for year in range(2026, 2007, -2)
    ]
    other = [
        FakeRelease(
            f"other{year}",
            year=str(year),
            artist="Elsewhere Act",
            copyright=f"(P) {year} Elsewhere Records",
        )
        for year in range(2025, 2006, -2)
    ]
    bare = [FakeRelease(f"bare{year}", year=str(year)) for year in (2006, 2005)]
    return [*own, *other, *bare]


def confirm_by_line(claimed, release):
    """The real verifier's judgement: the copyright line, else no credit."""
    del claimed
    names = harvest.labels_from_copyright(release)
    return {"resolved_label": names[0] if names else "", "source": "fixture"}


def test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked(
    installed, entry
):
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(mixed_roster()),
        verify=confirm_by_line,
        limit=3,
    )
    # The window itself is what it was: three of the label's, the two of
    # another label's it read on the way dropped as mismatches.
    assert [c.identity for c in found.candidates] == ["own2026", "own2024", "own2022"]
    assert [d.identity for d in found.dropped] == ["other2025", "other2023"]
    assert found.listed == 22
    # Past it: seven of the label's own (2020 to 2008), eight of another
    # label's left out, and two with no line counted as unchecked.
    assert found.beyond == 9
    assert found.beyond_unchecked == 2


def test_a_release_with_no_copyright_line_is_unchecked_never_dropped(installed, entry):
    verify, asked = counting_confirm()
    found = sweep.list_for_label(
        installed, entry, artist=FakePagedArtist(catalogue_of(20)), verify=verify, limit=5
    )
    assert found.beyond == 15
    assert found.beyond_unchecked == 15
    # Counting past the window asks the provider nothing.
    assert len(asked) == 5


def test_the_count_past_the_window_uses_the_labels_match_needle(installed, entry):
    found = sweep.list_for_label(
        installed,
        replace(entry, match="Deep Recordings"),
        artist=FakePagedArtist(mixed_roster("Deep Recordings Ltd")),
        verify=confirm_by_line,
        limit=3,
    )
    assert [c.identity for c in found.candidates] == ["own2026", "own2024", "own2022"]
    assert (found.beyond, found.beyond_unchecked) == (9, 2)


def test_a_round_records_the_most_the_label_could_still_offer(installed, monkeypatch):
    register("--offer", "3")
    fake = FakeCatalogue(
        artists={SLUG: FakePagedArtist(mixed_roster())},
        confirmed={f"own{year}" for year in range(2026, 2007, -2)} | {"bare2006", "bare2005"},
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    sweep_once()

    assert [item.payload["identity"] for item in filed(installed)] == [
        "own2026",
        "own2024",
        "own2022",
    ]
    (row,) = grouped("label")
    # Seven of the label's and two unchecked, never another label's eight.
    assert row["beyond"] == 9


def test_the_first_run_stays_the_filing_run_when_an_open_item_is_offered_again(installed):
    candidate = run.Candidate(identity="r1", recency="2026", payload={"label_id": SLUG})
    with review.open_store(installed) as store:
        sweep.offer_release(store, candidate, run_id="run-one")
        again = sweep.offer_release(store, candidate, run_id="run-two")
    assert again.payload[sweep.SWEEP_RUN] == "run-one"
    assert again.verdict is None


# ═══════════════════════════════════════════════════════════════════════════
# 3. The settings and the grouping refuse what they cannot mean
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("value", [0, -3, True, "10", 2.5])
def test_the_configured_offer_must_be_a_positive_whole_number(value):
    problems = config.validate({"labels": {"offer_per_sweep": value}})
    assert any("labels.offer_per_sweep" in problem for problem in problems)


def test_the_configured_offer_defaults_to_ten(installed):
    assert installed.labels.offer_per_sweep == config.DEFAULT_LABEL_OFFER == 10


def test_a_label_offer_survives_a_rename_and_an_unrelated_edit(installed):
    del installed
    store = labels.RegistryStore()
    label_id = store.add(LABEL, offer=25)
    store.edit(label_id, track_limit=100)
    store.rename(label_id, "Anjunadeep Recordings")
    held = store.load().by_id(label_id)
    assert held.offer == 25
    assert held.track_limit == 100


@pytest.mark.parametrize("value", ["0", "-1"])
def test_an_offer_below_one_refuses_at_the_parser_and_writes_nothing(installed, value):
    del installed
    code, _ = drive(["label", "registry", "add", LABEL, "--offer", value])
    assert code != int(ExitCode.OK)
    assert labels.RegistryStore().load().by_id(SLUG) is None


def test_an_offer_below_one_refuses_at_the_store(installed):
    del installed
    with pytest.raises(Exception) as caught:
        labels.RegistryStore().add(LABEL, offer=0)
    assert "offer" in str(caught.value)


def test_grouping_needs_a_queue_and_has_no_pages(installed):
    del installed
    code, envelope = drive(["review", "list", "--group-by", "label"])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    code, envelope = drive(
        ["review", "list", "--queue", "label-release", "--group-by", "run", "--after", "3"]
    )
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_a_queue_with_no_grouping_refuses_rather_than_listing_nothing(installed):
    del installed
    code, envelope = drive(["review", "list", "--queue", "path-repair", "--group-by", "label"])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "review-selection-invalid"


# ═══════════════════════════════════════════════════════════════════════════
# 4. What the review of this unit found
# ═══════════════════════════════════════════════════════════════════════════


def item_causes(job_id: str) -> dict[str, str | None]:
    from cratekit.core import jobs

    with jobs.open_store() as store:
        return {
            item.item_id: (item.cause.reason if item.cause is not None else None)
            for item in jobs.items(store, job_id)
        }


def sweep_expecting_refusal() -> str:
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), resumed
    return job_id


def test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new(
    installed, monkeypatch
):
    """Held releases are no longer re-verified, and they were what made a dead
    endpoint drop every release a sweep read. One is re-verified on this path.
    """
    register()
    releases = catalogue_of(5)
    bind(monkeypatch, releases)
    sweep_once()
    fake = FakeCatalogue(
        artists={SLUG: FakePagedArtist([FakeRelease("r2028", year="2028"), *releases])},
        confirmed=set(),
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    job_id = sweep_expecting_refusal()
    assert item_causes(job_id) == {SLUG: "label-sweep-incomplete"}
    assert len(filed(installed)) == 5
    # A refused sweep records no round, so the label's latest answer is still
    # the first sweep's rather than a count from a sweep that verified nothing.
    assert [row["items"] for row in grouped("run")] == [5]


def test_held_releases_that_still_confirm_let_a_label_of_unconfirmed_releases_succeed(
    installed, monkeypatch
):
    """The distributor credited shape: a few releases are the label's and the
    rest never confirm. Its later sweeps file nothing and must not refuse.
    """
    register()
    releases = catalogue_of(7)
    fake = FakeCatalogue(
        artists={SLUG: FakePagedArtist(releases)}, confirmed={"r2026", "r2025", "r2024"}
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    sweep_once()
    sweep_once()
    assert len(filed(installed)) == 3
    assert [row["items"] for row in grouped("run")] == [3, 0]


def test_a_held_release_since_downloaded_keeps_its_place(installed, entry):
    verify, _ = counting_confirm()
    found = sweep.list_for_label(
        installed,
        entry,
        artist=FakePagedArtist(catalogue_of(6)),
        verify=verify,
        offered={"r2026"},
        owned={"r2026"},
        limit=2,
    )
    assert found.held == 1
    assert [c.identity for c in found.candidates] == ["r2025"]


def test_a_harvested_label_name_is_not_counted_as_a_label_release(installed):
    with review.open_store(installed) as store:
        review.offer(
            store,
            queue=Queue.LABEL_RELEASE,
            kind="harvested-label",
            identity={"name": "Somebody"},
            payload={"name": "Somebody", "source": "harvest"},
        )
        sweep.offer_release(
            store,
            run.Candidate(identity="r1", recency="2026", payload={"label_id": SLUG}),
            run_id="run-one",
        )
    assert [row["items"] for row in grouped("label")] == [1]
    assert [row["run"] for row in grouped("run")] == ["run-one"]


def test_a_page_limit_with_a_grouping_refuses_rather_than_being_ignored(installed):
    del installed
    code, envelope = drive(
        ["review", "list", "--queue", "label-release", "--group-by", "label", "--limit", "5"]
    )
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_the_registry_says_when_the_track_limit_bounds_an_offer(installed):
    del installed
    register("--offer", "50", "--track-limit", "20")
    code, envelope = drive(["label", "registry", "list"])
    assert code == int(ExitCode.OK), envelope
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == f"labels.{SLUG}"]
    assert "offer 50, bounded by the track limit to 20" in check["detail"]


class CountingCatalogue(FakeCatalogue):
    """The fake catalogue, recording which releases verification was asked about."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verified: list[str] = []

    def search_release(self, claimed, release):
        self.verified.append(str(release.id))
        return super().search_release(claimed, release)


def test_a_later_sweep_asks_the_provider_nothing_about_releases_it_already_holds(
    installed, monkeypatch
):
    """Held releases are read off the queue the worker has open, not verified
    again. ``review.offer`` would quietly absorb a second filing of each, so the
    only place a sweep that forgot its queue shows is the provider calls it
    spends, one per held release per sweep, against a rate limited account.
    """
    register()
    releases = catalogue_of(50)
    bind(monkeypatch, releases)
    sweep_once()
    fake = CountingCatalogue(
        artists={SLUG: FakePagedArtist([FakeRelease("r2027", year="2027"), *releases])}
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    sweep_once()
    assert fake.verified == ["r2027"]


def test_a_run_over_two_labels_counts_what_both_left_beyond(installed, monkeypatch):
    """One ``sync labels`` job is one run with one item per label, so a run's
    row sums every label's count rather than reporting whichever came last.
    """
    register()
    code, envelope = drive(["label", "registry", "add", "Kompakt"])
    assert code == int(ExitCode.OK), envelope
    fake = FakeCatalogue(
        artists={
            SLUG: FakePagedArtist(catalogue_of(50)),
            "kompakt": FakePagedArtist(
                [FakeRelease(f"k{n}", year=str(2000 + n)) for n in range(15)]
            ),
        }
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    sweep_once()
    (row,) = grouped("run")
    assert row["items"] == 20
    assert row["labels"] == 2
    assert row["beyond"] == 45
    assert {r["label"]: r["beyond"] for r in grouped("label")} == {SLUG: 40, "kompakt": 5}
