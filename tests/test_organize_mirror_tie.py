"""R-1032: the mirror takes one of several agreeing releases where a heart would refuse.

Driven at the organize step, :func:`account_mirror.add_steps`, with every write
through the recording fake account U147's suite uses and every MATCH through
the real adapter over the fake provider client, so the choice between releases
is the one ``match_track`` makes and not one a fake was told to make. The heart
side of the same tie, which must still refuse (AE5), is driven end to end in
``tests/test_outbound_tidal_account.py`` by the favourites sweep over
``_releases_for_three_rows``, whose row 2 is this tie.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.modules.outbound import ledger, mirror, service, tidal_account
from tests import outbound_fakes
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_organize_mirror import World
from tests.test_outbound_tidal_account import CODE, FakeClient, Track, no_sleep

OTHER = "AA0000000002"


class Matched(outbound_fakes.StrictAccount):
    """The recording fake for every write, the real adapter for every match."""

    def __init__(self, client: FakeClient) -> None:
        super().__init__(catalog={})
        self.client = client
        self.adapter = tidal_account.TidalAccount(client, sleep=no_sleep)

    def match_track(self, **asked):
        self.matches.append(asked)
        return self.adapter.match_track(**asked)

    def unmatched_reason(self, identity: str) -> str:
        return self.adapter.unmatched_reason(identity)


def _alike(*ids: str) -> list[Track]:
    """Releases of one recording spelled alike, a single and its album cuts."""
    return [Track(one, "Sun Path", None, ("Nova Reef",)) for one in ids]


def _world(installed, monkeypatch, isrcs: dict[str, list], hearts=()) -> World:
    world = World(installed, monkeypatch)
    world.account = Matched(FakeClient(isrcs=isrcs, hearts=list(hearts)))
    return world


def _row(content_id: str = "c1", isrc: str = CODE) -> mirror.Row:
    return mirror.Row(content_id=content_id, title="Sun Path", artist="Nova Reef", isrc=isrc)


def _soul_high(*rows: mirror.Row) -> mirror.Folder:
    return mirror.Folder(name="Soul", playlists=(mirror.Source(name="Soul High", rows=rows),))


def test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded(installed, monkeypatch):
    """AE4. Two releases agree, neither hearted, no album: one is added and recorded."""
    world = _world(installed, monkeypatch, {CODE: _alike("202", "101")})
    world.mirror(_soul_high(_row()))

    area = world.run()

    assert world.held("Soul High") == ["101"]
    assert ledger.mirror_links(installed)["c1"] == ("101", CODE)
    assert "c1" not in ledger.mirror_misses(installed)
    assert area.steps[0].counts["unmatched"] == 0
    assert area.steps[0].counts["add"] == 1


def test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing(
    installed, monkeypatch
):
    """AE4's second half, and a heart placed later does not move the copy."""
    world = _world(installed, monkeypatch, {CODE: _alike("101", "202")})
    world.mirror(_soul_high(_row()))
    world.run()
    asked = list(world.account.client.isrc_asked)
    writes = (list(world.account.chunks), list(world.account.taken))
    world.account.client.user.favorites.hearts.append("202")

    area = world.run()

    assert world.account.client.isrc_asked == asked
    assert (list(world.account.chunks), list(world.account.taken)) == writes
    assert world.held("Soul High") == ["101"]
    assert all(step.apply is None for step in area.steps)


def test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again(
    installed, monkeypatch
):
    """The live ledger holds thousands of tie misses R-1031 remembered; each is asked once."""
    tied, absent = _row("c1"), _row("c2", isrc=OTHER)
    world = _world(installed, monkeypatch, {CODE: _alike("101", "202")})
    matcher = mirror.Matcher(world.account, {}, lambda _row: mirror.Identity())
    ledger.record_mirror_misses(
        installed,
        {
            "c1": (
                f"the ISRC {CODE} names 2 provider tracks, 2 {service.AGREEING_RELEASES} "
                "and the account hearts 0 of those, and the file carries no album tag, "
                "so none was chosen",
                matcher.under(tied),
            ),
            "c2": (mirror.NO_MATCH, matcher.under(absent)),
        },
    )
    world.mirror(_soul_high(tied, absent))

    world.run()

    assert world.account.client.isrc_asked == [CODE]
    assert world.held("Soul High") == ["101"]
    assert ledger.mirror_links(installed)["c1"] == ("101", CODE)
    assert set(ledger.mirror_misses(installed)) == {"c2"}


def test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again(
    installed, monkeypatch
):
    """Not only the tie refuses here, so the rule stands and the miss is not remembered."""
    world = _world(
        installed, monkeypatch, {CODE: [*_alike("101", "202"), Track("303", "", None, ())]}
    )
    world.mirror(_soul_high(_row()))

    area = world.run()

    (item,) = area.steps[0].items[1:]
    (said,) = item["unmatched"]
    assert service.UNREADABLE_CANDIDATE in said and service.AGREEING_RELEASES in said
    assert "c1" not in ledger.mirror_misses(installed)
    assert "c1" not in ledger.mirror_links(installed)
    world.plan()
    assert world.account.client.isrc_asked == [CODE, CODE]


def test_a_release_that_does_not_agree_is_never_the_one_taken(installed, monkeypatch):
    """The lowest identifier is a radio edit; the row is the plain record."""
    world = _world(
        installed,
        monkeypatch,
        {CODE: [Track("101", "Sun Path", "Radio Edit", ("Nova Reef",)), *_alike("303", "202")]},
    )
    world.mirror(_soul_high(_row()))

    world.run()

    assert world.held("Soul High") == ["202"]
