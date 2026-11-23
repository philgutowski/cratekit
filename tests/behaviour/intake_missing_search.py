"""Intake's missing scenarios over a text list: candidates searched, offered and accepted (U307).

A typed list's missing rows are searched and offered into review, an accepted
candidate is listed next run without a search, and a provider that cannot
search refuses. Its own file for its ``cfg`` and ``library``.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.label_fakes import UnreadableCatalogue
from tests.test_intake_missing_search import bind, near_miss, the_item, tracklist
from tests.test_intake_missing_search import cfg as cfg  # noqa: PLC0414
from tests.test_intake_missing_search import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_intake_missing_search import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_a_near_miss_is_offered_then_listed_once_accepted(
    stage, cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path")
    fake = bind(monkeypatch, near_miss())
    verb = ["intake", "missing", "--list", str(path)]

    offered = stage.json(*verb)
    assert offered.code == OK, offered.stdout
    assert offered.envelope["data"]["summary"]["candidates_offered"] == 1
    item_id = the_item(cfg).item_id
    accepted = stage.json("review", "resolve", item_id, "--verdict", "accepted", "--option", "7005")
    assert accepted.code == OK, accepted.stdout

    assert stage.crate(*verb).code == OK
    listed = stage.json(*verb)
    assert listed.code == OK, listed.stdout
    assert listed.envelope["data"]["summary"]["by_review"] == 1
    assert fake.searched_for == [("Aurora Bloom", "Sun Path")]


def test_a_provider_that_cannot_search_refuses_and_writes_nothing(
    stage, cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, "Aurora Bloom - Sun Path", "Nova Reef - Tide")
    bind(monkeypatch, UnreadableCatalogue())
    refused = stage.json("intake", "missing", "--list", str(path))
    assert refused.code != OK, refused.stdout
    assert refused.envelope["cause"]["reason"] == "unavailable-transient"
