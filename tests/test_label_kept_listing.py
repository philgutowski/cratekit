"""U217: a label's listing is kept, so a continue resumes it and a second ask is free.

Driven over the provider catalogue adapter with the stand in client of
``tests/test_label_tidal_catalogue.py``, counting every call the listing makes:
each search, each artist read and each page of a release listing. A ceiling
is the job engine's own park raised by that counter once it is spent, which is
what ``provider_gate`` raises at the line a person set.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from cratekit.core import jobs, provider_gate
from cratekit.core.cause import CratekitError, refuse
from cratekit.label import kept_listing, kept_reads, sweep, tidal_catalogue
from cratekit.label import registry as labels
from tests.test_label_tidal_catalogue import FakeClient, ProviderArtist, Release, cfg  # noqa: F401

NOW = datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc)
LABEL = "Kept Recordings"


class Budget:
    """Every provider call the listing makes, and the ceiling that stops it."""

    def __init__(self) -> None:
        self.calls = 0
        self.ceiling: int | None = None
        self.asked: list[str] = []

    def tick(self, what: str) -> None:
        if self.ceiling is not None and self.calls >= self.ceiling:
            raise jobs.Parked(
                refuse(provider_gate.CEILING, f"this command made {self.calls} calls").cause
            )
        self.calls += 1
        self.asked.append(what)


class CountedArtist(ProviderArtist):
    def __init__(self, budget: Budget, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.budget = budget

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        self.budget.tick(f"albums {self.id} {offset}")
        return super().get_albums(limit, offset)

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        self.budget.tick(f"singles {self.id} {offset}")
        return super().get_ep_singles(limit, offset)


class CountedClient(FakeClient):
    def __init__(self, budget: Budget, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.budget = budget

    def search(self, query: str, models=None, limit: int = 50, offset: int = 0) -> dict:
        self.budget.tick(f"search {query}")
        return super().search(query, models=models, limit=limit, offset=offset)

    def artist(self, artist_id: str | None = None) -> ProviderArtist:
        self.budget.tick(f"artist {artist_id}")
        return super().artist(artist_id)

    def album(self, album_id: str) -> Release:
        self.budget.tick(f"album {album_id}")
        return super().album(album_id)


class Credited:
    def __init__(self, identity: str) -> None:
        self.id = identity
        self.name = f"Act {identity}"


def label_release(release_id: str, *, by: str, year: str = "2025") -> Release:
    return Release(
        release_id, copyright=f"(P) {year} {LABEL}", year=year, artists=[Credited(by)]
    )


def roster_client(budget: Budget, *, acts: int = 4) -> CountedClient:
    """A label with no own page: ``acts`` artists, each found by one album search.

    Every act has one album and one single on the label, so its listing is two
    pages of answers and one empty page each, and the walk over its releases
    finds no artist it had not found.
    """
    artists = [
        CountedArtist(
            budget,
            f"Act {number}",
            [label_release(f"{number}01", by=str(number))],
            [label_release(f"{number}02", by=str(number))],
            artist_id=str(number),
        )
        for number in range(1, acts + 1)
    ]
    found = [label_release(f"{one.id}01", by=one.id) for one in artists]
    return CountedClient(
        budget,
        artists=artists,
        albums_by_query={LABEL: found},
    )


@pytest.fixture
def entry() -> labels.LabelEntry:
    return labels.LabelEntry(label_id="kept-recordings", name=LABEL)


@pytest.fixture
def clock(monkeypatch):
    now = [NOW]
    monkeypatch.setattr(kept_reads, "clock", lambda: now[0])
    return now


def adapter(client: CountedClient) -> tidal_catalogue.TidalCatalogue:
    return tidal_catalogue.TidalCatalogue(client)


def listed_ids(roster: Any) -> list[str]:
    return sorted(str(one.id) for one in tidal_catalogue.listing.artist_releases(roster))


def fresh_calls(entry) -> tuple[int, list[str]]:
    """What one listing of the label costs with nothing kept, measured."""
    budget = Budget()
    roster = adapter(roster_client(budget)).artist_for(entry)
    kept_listing.path_for(entry.label_id).unlink()
    return budget.calls, listed_ids(roster)


# ═══════════════════════════════════════════════════════════════════════════
# A second ask asks nothing
# ═══════════════════════════════════════════════════════════════════════════


def test_a_second_listing_of_the_same_label_asks_the_provider_nothing(entry, clock):
    budget = Budget()
    first = adapter(roster_client(budget)).artist_for(entry)
    spent = budget.calls
    assert spent > 0
    second = adapter(roster_client(budget)).artist_for(entry)
    assert budget.calls == spent, budget.asked[spent:]
    assert listed_ids(second) == listed_ids(first)
    assert second.kept.asked == 0 and second.kept.reused > 0
    assert "no provider call" in second.kept.said()


def test_a_kept_release_reads_as_the_provider_object_did(entry, clock):
    budget = Budget()
    first = tidal_catalogue.listing.artist_releases(adapter(roster_client(budget)).artist_for(entry))
    second = tidal_catalogue.listing.artist_releases(adapter(roster_client(budget)).artist_for(entry))
    by_id = {one.id: one for one in first}
    for kept in second:
        live = by_id[kept.id]
        assert sweep.year_of(kept) == sweep.year_of(live)
        assert sweep._title_of(kept) == sweep._title_of(live)
        assert tidal_catalogue._copyright_label(kept) == tidal_catalogue._copyright_label(live)
        assert tidal_catalogue._credited_ids(kept) == tidal_catalogue._credited_ids(live)
        assert tidal_catalogue.artist_name(kept) == tidal_catalogue.artist_name(live)


def test_a_kept_release_verifies_with_no_call(entry, clock):
    budget = Budget()
    client = roster_client(budget)
    adapter(client).artist_for(entry)
    roster = adapter(client).artist_for(entry)
    spent = budget.calls
    for release in tidal_catalogue.listing.artist_releases(roster):
        verdict = adapter(client).search_release(LABEL, release)
        assert verdict["resolved_label"] == LABEL
    assert budget.calls == spent


# ═══════════════════════════════════════════════════════════════════════════
# A continue after the ceiling asks only what was not read
# ═══════════════════════════════════════════════════════════════════════════


def test_a_listing_stopped_at_the_ceiling_continues_with_only_the_unread_part(entry, clock):
    whole, ids = fresh_calls(entry)
    budget = Budget()
    budget.ceiling = whole // 2 + 5
    with pytest.raises(jobs.Parked):
        adapter(roster_client(budget)).artist_for(entry)
    stopped_at = budget.calls
    # WRITTEN ON THE WAY OUT, though fewer answers than a flush's batch.
    assert kept_listing.path_for(entry.label_id).exists()

    budget.ceiling = None
    roster = adapter(roster_client(budget)).artist_for(entry)
    continued = budget.calls - stopped_at
    assert listed_ids(roster) == ids
    assert 0 < continued < whole
    # NOTHING ASKED TWICE: the two runs together asked exactly the fresh cost.
    assert stopped_at + continued == whole
    assert roster.kept.reused > 0 and 0 < roster.kept.asked <= continued
    assert "continued from an earlier run" in roster.kept.said()


def test_a_ceiling_stop_inside_discovery_keeps_every_search_it_finished(entry, clock):
    budget = Budget()
    budget.ceiling = 30
    with pytest.raises(jobs.Parked):
        adapter(roster_client(budget)).artist_for(entry)
    searched = [one for one in budget.asked if one.startswith("search ")]
    budget.asked.clear()
    budget.ceiling = None
    adapter(roster_client(budget)).artist_for(entry)
    again = [one for one in budget.asked if one.startswith("search ")]
    assert not set(searched) & set(again)


# ═══════════════════════════════════════════════════════════════════════════
# The first run lists each artist once
# ═══════════════════════════════════════════════════════════════════════════


def test_the_first_listing_pages_each_discovered_artist_once(entry, clock):
    budget = Budget()
    adapter(roster_client(budget)).artist_for(entry)
    pages = [one for one in budget.asked if one.startswith(("albums ", "singles "))]
    assert len(pages) == len(set(pages)), pages


def test_without_a_store_the_roster_still_lists_each_member_now():
    budget = Budget()
    act = CountedArtist(budget, "Act", [label_release("1", by="1")], artist_id="1")
    roster = tidal_catalogue.LabelRoster([act])
    assert [one.id for one in tidal_catalogue.listing.artist_releases(roster)] == ["1"]
    assert roster.kept is None


# ═══════════════════════════════════════════════════════════════════════════
# What makes it ask again
# ═══════════════════════════════════════════════════════════════════════════


def test_a_listing_older_than_the_kept_life_is_asked_again(entry, clock):
    budget = Budget()
    adapter(roster_client(budget)).artist_for(entry)
    whole = budget.calls
    clock[0] = NOW + kept_reads.KEPT_FOR
    roster = adapter(roster_client(budget)).artist_for(entry)
    assert budget.calls == 2 * whole
    assert roster.kept.reused == 0 and roster.kept.stale > 0
    assert "older than" in roster.kept.said()


def test_a_listing_just_inside_the_kept_life_is_still_answered(entry, clock):
    budget = Budget()
    adapter(roster_client(budget)).artist_for(entry)
    whole = budget.calls
    clock[0] = NOW + kept_reads.KEPT_FOR - timedelta(minutes=1)
    adapter(roster_client(budget)).artist_for(entry)
    assert budget.calls == whole


def test_a_listing_kept_in_the_future_is_not_fresh(entry, clock):
    budget = Budget()
    adapter(roster_client(budget)).artist_for(entry)
    whole = budget.calls
    clock[0] = NOW - timedelta(hours=1)
    adapter(roster_client(budget)).artist_for(entry)
    assert budget.calls == 2 * whole


@pytest.mark.parametrize(
    "changed",
    [
        {"match": "Kept Recordings Ltd"},
        {"seed_artists": ("id:1",)},
        {"name": "Kept Records"},
    ],
)
def test_a_label_entry_that_changed_reads_the_kept_listing_as_empty(entry, clock, changed):
    budget = Budget()
    adapter(roster_client(budget)).artist_for(entry)
    whole = budget.calls
    other = labels.LabelEntry(
        label_id=entry.label_id,
        name=changed.get("name", entry.name),
        match=changed.get("match"),
        seed_artists=changed.get("seed_artists", ()),
    )
    try:
        roster = adapter(roster_client(budget)).artist_for(other)
    except tidal_catalogue.LabelUnresolvable:
        roster = None
    assert budget.calls > whole
    if roster is not None:
        assert roster.kept.changed
        assert "changed after its listing was kept" in roster.kept.said()


def test_a_failed_listing_is_not_kept(entry, clock, monkeypatch):
    # THE RETRY LADDER WAITS THROUGH THE ADAPTER'S PAUSE, not for real.
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda seconds: None)
    budget = Budget()

    class Failing(CountedArtist):
        def get_ep_singles(self, limit=None, offset=0):
            raise RuntimeError("the provider failed")

    client = roster_client(budget)
    client.artists[0] = Failing(
        budget, "Act 1", [label_release("101", by="1")], artist_id="1"
    )
    roster = adapter(client).artist_for(entry)
    assert roster.unread  # the failure was recorded, not read as empty
    document = json.loads(kept_listing.path_for(entry.label_id).read_text())
    assert "1 get_albums" in document["listed"]
    assert "1 get_ep_singles" not in document["listed"]


def test_an_artist_with_no_identifier_is_listed_and_not_kept(entry, clock):
    budget = Budget()
    own = CountedArtist(budget, LABEL, [label_release("9", by="")])
    client = CountedClient(budget, artists=[own], albums_by_query={})
    adapter(client).artist_for(entry)
    whole = budget.calls
    roster = adapter(client).artist_for(entry)
    assert budget.calls > whole
    assert [one.id for one in tidal_catalogue.listing.artist_releases(roster)] == ["9"]


# ═══════════════════════════════════════════════════════════════════════════
# The store itself
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "written",
    [
        "{not json",
        "[]",
        json.dumps({"version": 2}),
        json.dumps({"version": 1, "label_id": "another"}),
        json.dumps({"version": 1, "label_id": "kept-recordings"}),
        json.dumps(
            {
                "version": 1,
                "label_id": "kept-recordings",
                "asked_for": {},
                "named": {},
                "identified": {},
                "searched": {"q": {"read_at": "yesterday", "value": []}},
                "listed": {},
            }
        ),
        json.dumps(
            {
                "version": 1,
                "label_id": "kept-recordings",
                "asked_for": {},
                "named": {},
                "identified": {},
                "searched": {},
                "listed": {"1 get_albums": {"read_at": NOW.isoformat(), "value": [{"id": 1}]}},
            }
        ),
    ],
)
def test_a_kept_listing_that_cannot_be_read_refuses_before_any_call(entry, clock, written):
    path = kept_listing.path_for(entry.label_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(written)
    budget = Budget()
    with pytest.raises(CratekitError) as refused:
        adapter(roster_client(budget)).artist_for(entry)
    assert refused.value.cause.reason == kept_listing.UNUSABLE
    assert str(path) in " ".join(refused.value.cause.remediation.steps)
    assert budget.calls == 0


def test_a_write_the_filesystem_refuses_is_said_and_the_listing_still_made(
    entry, clock, monkeypatch
):
    def refused(payload, path, **kwargs):
        raise OSError("read only volume")

    monkeypatch.setattr(kept_listing.config, "atomic_write_bytes", refused)
    budget = Budget()
    roster = adapter(roster_client(budget)).artist_for(entry)
    assert listed_ids(roster)
    assert "read only volume" in roster.kept.unkept
    assert "could not be kept" in roster.kept.said()


def test_the_store_writes_every_flush_batch_as_it_goes(entry, clock, monkeypatch):
    monkeypatch.setattr(kept_listing, "FLUSH_EVERY", 3)
    writes: list[int] = []
    real = kept_listing.config.atomic_write_bytes

    def counted(payload, path, **kwargs):
        writes.append(len(payload))
        return real(payload, path, **kwargs)

    monkeypatch.setattr(kept_listing.config, "atomic_write_bytes", counted)
    budget = Budget()
    roster = adapter(roster_client(budget)).artist_for(entry)
    assert len(writes) >= roster.kept.asked // 3


def test_the_first_listing_says_none_was_kept(entry, clock):
    roster = adapter(roster_client(Budget())).artist_for(entry)
    assert roster.kept.reused == 0
    assert "since none was kept" in roster.kept.said()


# ═══════════════════════════════════════════════════════════════════════════
# The verbs: label playlists after a listing, and the screen
# ═══════════════════════════════════════════════════════════════════════════


def test_label_playlists_after_a_sync_listing_asks_no_listing(entry, clock, cfg):  # noqa: F811
    budget = Budget()
    client = roster_client(budget)
    found = adapter(client)
    first = sweep.listed_releases(cfg, entry, found)
    spent = budget.calls
    again = sweep.listed_releases(cfg, entry, found)
    assert budget.calls == spent
    assert {one.id for one in again.releases} == {one.id for one in first.releases}
    assert again.kept is not None and again.kept.asked == 0
