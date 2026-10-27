"""R-1031: the mirror remembers what it could not match, and its gate's plan is the apply's.

Driven at the organize step, :func:`account_mirror.add_steps`, over the
recording fake account U147's suite uses, with an organize run handed in the
way ``crate organize`` hands one: a run that asks its gate records and freezes,
a report does neither, and the run whose account gate is decided rebuilds from
the record. The verb level drive of two acts with a library write between them
is in ``tests/test_organize.py``.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json
import os

import pytest

from cratekit.core import config
from cratekit.modules.outbound import ledger, mirror, service
from cratekit.organize import account_mirror, mirror_frozen
from cratekit.organize.steps import Area
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_organize_mirror import World, folder, row

RUN = "2026-10-27T10:00:00Z-ab12"


def _plan(world: World, run: account_mirror.Run | None) -> Area:
    area = Area(name="account")
    account_mirror.add_steps(world.cfg, area, lambda: world.account, run)
    return area


def _asked(world: World) -> list[str]:
    return [one["identity"] for one in world.account.matches]


def _frozen_path(cfg) -> str:
    return str(config.state_path("mirror_plans", cfg) / f"{RUN}.json")


def _shown(run: str = RUN) -> account_mirror.Run:
    """The run that shows the gate: it records and freezes."""
    return account_mirror.Run(run_id=run, record=True)


def _decided(run: str = RUN) -> account_mirror.Run:
    """The run that answers the gate: it rebuilds from the frozen plan."""
    return account_mirror.Run(run_id=run, record=True, decided=True)


# ═══════════════════════════════════════════════════════════════════════════
# 1. Remembered misses (R1, R2)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered(
    installed, monkeypatch
):
    """AE1. Three misses remembered, two rows landed: the provider is asked about two."""
    world = World(installed, monkeypatch, unmatched=(5, 6, 7))
    world.mirror(folder("Techno", Low=(1, 5, 6, 7)))
    world.run()
    assert set(ledger.mirror_misses(installed)) == {"c5", "c6", "c7"}
    before = len(_asked(world))

    world.mirror(folder("Techno", Low=(1, 5, 6, 7, 8, 9)))
    area = world.plan()

    assert _asked(world)[before:] == ["c8", "c9"]
    assert area.facts[account_mirror.MISSES_FACT].startswith("3 row(s) ")
    (item,) = area.steps[0].items[1:]
    # A remembered miss is still named under its playlist, with its reason.
    assert sorted(item["unmatched"]) == [
        f"Artist {n} - Title {n}: {mirror.NO_MATCH}" for n in (5, 6, 7)
    ]


def test_a_miss_is_recorded_by_the_run_that_shows_the_gate_with_nothing_applied(
    installed, monkeypatch
):
    world = World(installed, monkeypatch, unmatched=(2,))
    world.mirror(folder("Techno", Low=(1, 2)))

    _plan(world, _shown())

    assert ledger.mirror_misses(installed)["c2"][0] == mirror.NO_MATCH
    assert set(ledger.mirror_links(installed)) == {"c1"}
    before = len(_asked(world))
    world.plan()
    assert len(_asked(world)) == before


def test_a_report_records_no_link_no_miss_and_freezes_nothing(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(2,))
    world.mirror(folder("Techno", Low=(1, 2)))

    area = _plan(world, account_mirror.Run(run_id=RUN))

    assert ledger.mirror_misses(installed) == {} and ledger.mirror_links(installed) == {}
    assert not os.path.exists(_frozen_path(installed))
    assert account_mirror.FROZEN_FACT not in area.facts


def test_a_row_whose_database_code_changed_since_its_miss_is_asked_again(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(3,))
    world.mirror(folder("Techno", Low=(3,)))
    world.run()
    before = len(_asked(world))

    world.mirror(
        mirror.Folder(
            name="Techno",
            playlists=(mirror.Source(name="Techno Low", rows=(row(3, isrc="NEWCODE0003"),)),),
        )
    )
    world.plan()

    assert _asked(world)[before:] == ["c3"]


@pytest.mark.parametrize("changed", ["title", "artist", "path"])
def test_a_row_whose_title_artist_or_path_changed_since_its_miss_is_asked_again(
    installed, monkeypatch, changed
):
    world = World(installed, monkeypatch, unmatched=(3,))
    world.mirror(folder("Techno", Low=(3,)))
    world.run()
    before = len(_asked(world))

    moved = mirror.Row(**{**{f: getattr(row(3), f) for f in mirror.Row.__slots__}, changed: "else"})
    world.mirror(
        mirror.Folder(name="Techno", playlists=(mirror.Source(name="Techno Low", rows=(moved,)),))
    )
    world.plan()

    assert _asked(world)[before:] == ["c3"]


def test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not(
    installed, monkeypatch
):
    """AE2. A row with no database code, whose file is read only when it changed."""
    from cratekit.sync import pair_cli

    world = World(installed, monkeypatch)
    signatures = {"c2": "100:1", "c3": "100:1"}
    codes: dict[str, str] = {}
    monkeypatch.setattr(
        account_mirror, "file_signature", lambda _cfg: lambda one: signatures[one.content_id]
    )
    monkeypatch.setattr(pair_cli, "file_identity", lambda _cfg, path: (codes.get(path, ""), ""))
    untagged = tuple(
        mirror.Row(content_id=f"c{n}", title=f"Title {n}", artist=f"Artist {n}", path=f"f{n}")
        for n in (2, 3)
    )
    world.mirror(
        mirror.Folder(name="Techno", playlists=(mirror.Source(name="Techno Low", rows=untagged),))
    )
    world.run()
    assert {key: held[0] for key, held in ledger.mirror_misses(installed).items()} == {
        "c2": mirror.NO_ISRC,
        "c3": mirror.NO_ISRC,
    }
    read: list[str] = []
    monkeypatch.setattr(
        pair_cli, "file_identity", lambda _cfg, path: read.append(path) or (codes.get(path, ""), "")
    )

    # c2's file is retagged, which moves its mtime; c3's is untouched.
    signatures["c2"], codes["f2"] = "120:2", "FILECODE002"
    area = world.plan()

    assert read == ["f2"]
    assert _asked(world) == ["c2"]
    assert area.steps[0].counts["add"] == 1


def test_rematch_asks_every_remembered_miss_again(installed, monkeypatch):
    """AE2. ``--rematch``: every miss is asked, and a linked row is not."""
    world = World(installed, monkeypatch, unmatched=(5, 6))
    world.mirror(folder("Techno", Low=(1, 5, 6)))
    world.run()
    before = len(_asked(world))

    area = _plan(world, account_mirror.Run(run_id=RUN, rematch=True))

    assert sorted(_asked(world)[before:]) == ["c5", "c6"]
    assert account_mirror.MISSES_FACT not in area.facts


def test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered(
    installed, monkeypatch
):
    world = World(installed, monkeypatch, unmatched=(4, 5))
    # THE ADAPTER'S OWN WORDS, from the constant it formats its reason with.
    world.account.reasons["c4"] = (
        f"the ISRC X names 2 provider tracks, 1 {service.UNREADABLE_CANDIDATE} and none "
        f"of the rest agrees"
    )
    world.account.reasons["c5"] = "the ISRC Y names 2 provider tracks and none of them agrees"
    world.mirror(folder("Techno", Low=(4, 5)))
    world.run()

    assert set(ledger.mirror_misses(installed)) == {"c5"}
    before = len(_asked(world))
    world.plan()
    assert _asked(world)[before:] == ["c4"]


def test_a_row_matched_later_loses_its_miss(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(5,))
    world.mirror(folder("Techno", Low=(5,)))
    world.run()
    assert "c5" in ledger.mirror_misses(installed)

    world.account.catalog["c5"] = "r5"
    _plan(world, account_mirror.Run(run_id=RUN, record=True, rematch=True))

    assert "c5" not in ledger.mirror_misses(installed)
    assert ledger.mirror_links(installed)["c5"][0] == "r5"


def test_a_miss_is_never_recorded_over_a_link(installed, monkeypatch):
    ledger.record_mirror_links(installed, {"c1": ("r1", "ISRC00001")})

    ledger.record_mirror_misses(installed, {"c1": ("why", ("a",)), "c2": ("why", ("b",))})

    assert set(ledger.mirror_misses(installed)) == {"c2"}
    assert ledger.mirror_links(installed)["c1"] == ("r1", "ISRC00001")


def test_a_malformed_miss_is_dropped_and_asked_again_rather_than_refusing(installed):
    ledger.record_mirror_misses(installed, {"c2": ("why", ("b",))})
    path = config.state_path("outbound_writes", installed)
    document = json.loads(path.read_text())
    document["mirror_misses"]["c3"] = {"reason": "why", "under": "not a list"}
    path.write_text(json.dumps(document))

    assert set(ledger.mirror_misses(installed)) == {"c2"}


def test_a_ledger_whose_misses_are_not_a_map_refuses(installed):
    from cratekit.core.cause import CratekitError

    ledger.record_mirror_misses(installed, {"c2": ("why", ("b",))})
    path = config.state_path("outbound_writes", installed)
    document = json.loads(path.read_text())
    document["mirror_misses"] = ["c2"]
    path.write_text(json.dumps(document))

    with pytest.raises(CratekitError) as caught:
        ledger.mirror_misses(installed)
    assert caught.value.cause.reason == "outbound-ledger-unusable"


def test_a_write_elsewhere_in_the_ledger_carries_the_misses_through(installed):
    ledger.record_mirror_misses(installed, {"c2": ("why", ("b",))})

    ledger.record_mirror_links(installed, {"c9": ("r9", "ISRC00009")})

    assert ledger.mirror_misses(installed) == {"c2": ("why", ("b",))}


def test_the_file_signature_moves_when_the_file_is_rewritten(installed):
    from pathlib import Path

    music = Path(installed.library.root) / "Music"
    music.mkdir(parents=True, exist_ok=True)
    track = music / "one.flac"
    track.write_bytes(b"a" * 10)
    sign = account_mirror.file_signature(installed)
    one = mirror.Row(content_id="c1", path=str(track))

    first = sign(one)
    track.write_bytes(b"a" * 12)

    assert first and sign(one) != first
    assert sign(mirror.Row(content_id="c2", path=str(music / "gone.flac"))) == ""
    assert sign(mirror.Row(content_id="c3")) == ""


# ═══════════════════════════════════════════════════════════════════════════
# 2. The plan frozen on the run (R3)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_decided_run_rebuilds_the_frozen_plan_over_a_moved_library(installed, monkeypatch):
    """AE3 at the step. The library moved; the digest did not, and nothing was matched."""
    world = World(installed, monkeypatch, unmatched=(3,))
    world.mirror(folder("Techno", Low=(1, 2, 3)), folder("Soul", High=(4,)))
    shown = _plan(world, _shown())
    assert shown.facts[account_mirror.FROZEN_FACT].startswith("frozen on run ")
    asked = len(_asked(world))

    # A landing, a split and a refresh between the acts.
    world.mirror(folder("Techno", Low=(1, 2, 3, 9), Med=(8,)), folder("Jazz", Low=(7,)))
    applied = _plan(world, _decided())

    assert applied.digest() == shown.digest()
    assert len(_asked(world)) == asked
    assert applied.facts[account_mirror.FROZEN_FACT] == f"rebuilt from the plan frozen on run {RUN}"
    assert "read the account and rebuild 2 folder(s)" in applied.facts[account_mirror.PLAN_FACT]
    world.apply(applied)
    assert world.held("Techno Low") == ["r1", "r2"]
    assert world.held("Soul High") == ["r4"]
    assert not any(title.startswith("Jazz") for title in world.account.titles.values())


def test_the_rebuild_reads_the_account_listing_alone(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1, 2), Med=(3,)))
    world.run()
    world.mirror(folder("Techno", Low=(1, 2, 4), Med=(3,)))
    shown = _plan(world, _shown())
    world.account.matches.clear()

    applied = _plan(world, _decided())

    assert applied.digest() == shown.digest()
    assert world.account.matches == []
    # The root, the folder's playlists, and each recorded playlist's tracks.
    assert applied.facts[account_mirror.PLAN_FACT].startswith("4 account request(s) in ")


def test_an_account_that_moved_between_the_acts_moves_the_digest(installed, monkeypatch):
    """The frozen plan holds the library still, never the account."""
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1, 2)))
    world.run()
    shown = _plan(world, _shown())
    # A person adds a track to the mirrored playlist by hand on the account.
    world.account.playlists[world.playlist_id("Techno Low")].append("r99")
    world.account.names["r99"] = ("Someone", "By Hand")

    applied = _plan(world, _decided())

    assert applied.digest() != shown.digest()


def test_a_decided_run_with_no_frozen_plan_plans_afresh_and_says_so(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))

    area = _plan(world, _decided())

    assert _asked(world) == ["c1"]
    said = area.facts[account_mirror.FROZEN_FACT]
    assert said.startswith(f"run {RUN} holds no frozen mirror plan, so it was planned afresh; ")
    assert "frozen on run" in said
    assert os.path.exists(_frozen_path(installed))


def test_an_unreadable_frozen_plan_plans_afresh_rather_than_refusing(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    _plan(world, _shown())
    with open(_frozen_path(installed), "w", encoding="utf-8") as handle:
        handle.write('{"version": 1, "run_id": "%s", "library": {}}' % RUN)
    world.mirror(folder("Techno", Low=(1, 2)))
    world.account.matches.clear()

    area = _plan(world, _decided())

    # Planned afresh from the moved library: the new row is matched.
    assert _asked(world) == ["c2"]
    said = area.facts[account_mirror.FROZEN_FACT]
    assert "is not one this build reads" in said and "so it was planned afresh" in said


def test_a_frozen_plan_of_another_version_or_run_is_not_rebuilt(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    _plan(world, _shown())
    path = _frozen_path(installed)
    document = json.loads(open(path, encoding="utf-8").read())

    for changed in ({"version": 2}, {"run_id": "another"}):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({**document, **changed}, handle)
        frozen, said = mirror_frozen.load(installed, RUN)
        assert frozen is None and "is not one this build reads" in said, changed


def test_a_decision_on_another_run_never_reads_this_runs_frozen_plan(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    _plan(world, _shown())
    world.mirror(folder("Techno", Low=(1, 2)))
    world.account.matches.clear()

    area = _plan(world, _decided("2026-10-27T11:00:00Z-cd34"))

    assert _asked(world) == ["c2"]
    assert "holds no frozen mirror plan" in area.facts[account_mirror.FROZEN_FACT]


def test_the_frozen_plan_carries_the_librarys_refusals_and_its_favorites_reason(
    installed, monkeypatch
):
    world = World(installed, monkeypatch)
    cause = account_mirror._twice("Soul", "folders")
    world.mirror(folder("Techno", Low=(1,)), refused={"Soul": cause}, favorites="no folder")
    shown = _plan(world, _shown())
    world.mirror(folder("Techno", Low=(1,)))

    applied = _plan(world, _decided())

    assert applied.digest() == shown.digest()
    steps = {step.key: step for step in applied.steps}
    assert steps["mirror:Soul"].cause.reason == mirror.AMBIGUOUS_REASON
    assert steps["mirror:favorites"].detail == "not mirrored: no folder"


def test_a_run_identifier_that_cannot_name_a_file_is_not_frozen(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))

    area = _plan(world, _shown("../escape"))

    assert area.facts[account_mirror.FROZEN_FACT].startswith("not frozen: the run identifier ")
    assert not (config.state_path("mirror_plans", installed).parent / "escape.json").exists()
    assert mirror_frozen.load(installed, "../escape")[0] is None


def test_a_frozen_plan_older_than_a_week_is_pruned_when_another_is_written(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    _plan(world, _shown("2026-10-01T10:00:00Z-old1"))
    _plan(world, _shown("2026-10-26T10:00:00Z-new1"))
    directory = config.state_path("mirror_plans", installed)
    old = directory / "2026-10-01T10:00:00Z-old1.json"
    recent = directory / "2026-10-26T10:00:00Z-new1.json"
    stale = os.stat(old).st_mtime - (mirror_frozen.KEPT_DAYS + 1) * 86400
    os.utime(old, (stale, stale))

    _plan(world, _shown())

    assert not old.exists() and recent.exists()
    assert (directory / f"{RUN}.json").exists()


def test_a_ledger_that_cannot_take_the_links_leaves_the_plan_standing_and_says_so(
    installed, monkeypatch
):
    from cratekit.core.cause import refuse

    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))

    def unwritable(_cfg, _links):
        raise refuse("outbound-ledger-unusable", "the ledger is read only", origin=("test",))

    monkeypatch.setattr(ledger, "record_mirror_links", unwritable)
    area = _plan(world, _shown())

    assert area.steps[0].state == "planned"
    assert "not frozen: what the plan matched could not be recorded" in area.facts[
        account_mirror.FROZEN_FACT
    ]
    assert not os.path.exists(_frozen_path(installed))


# ═══════════════════════════════════════════════════════════════════════════
# 3. The review's round: each guard alone, and the frozen matches themselves
# ═══════════════════════════════════════════════════════════════════════════


def test_the_mirror_reads_the_words_the_seam_gives_an_unread_candidate():
    """The adapter's reason is pinned by its own suite, ``1 could not be read``."""
    assert mirror.UNREAD == service.UNREADABLE_CANDIDATE == "could not be read"


def test_the_frozen_matches_answer_a_row_the_ledger_could_not_remember(installed, monkeypatch):
    """A miss over an unread candidate is not in the ledger; the frozen plan still holds it."""
    world = World(installed, monkeypatch, unmatched=(4,))
    world.account.reasons["c4"] = f"the ISRC X names 2 provider tracks, 1 {service.UNREADABLE_CANDIDATE}"
    world.mirror(folder("Techno", Low=(1, 4)))
    shown = _plan(world, _shown())
    assert "c4" not in ledger.mirror_misses(installed)
    # The candidate reads now, so a plan asking again would add the track.
    world.account.catalog["c4"] = "r4"
    world.account.matches.clear()

    applied = _plan(world, _decided())

    assert world.account.matches == []
    assert applied.digest() == shown.digest()


def test_the_frozen_matches_stand_over_a_link_recorded_between_the_acts(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(5,))
    world.mirror(folder("Techno", Low=(1, 5)))
    shown = _plan(world, _shown())
    # Another run links the row between the two acts.
    ledger.record_mirror_links(installed, {"c5": ("r5", "ISRC00005")})

    applied = _plan(world, _decided())
    world.apply(applied)

    assert applied.digest() == shown.digest()
    assert world.held("Techno Low") == ["r1"]


def test_rematch_on_the_run_that_answers_asks_nothing_and_says_so(installed, monkeypatch):
    world = World(installed, monkeypatch, unmatched=(5,))
    world.mirror(folder("Techno", Low=(1, 5)))
    _plan(world, _shown())
    world.account.matches.clear()

    area = _plan(world, account_mirror.Run(run_id=RUN, record=True, decided=True, rematch=True))

    assert world.account.matches == []
    assert "--rematch on this run asked nothing" in area.facts[account_mirror.FROZEN_FACT]


def test_a_coded_rows_miss_is_kept_whatever_its_file_does(installed, monkeypatch):
    """The file is read only for a row with no code, so only then does it key the miss."""
    world = World(installed, monkeypatch, unmatched=(3,))
    signature = {"now": "100:1"}
    monkeypatch.setattr(account_mirror, "file_signature", lambda _cfg: lambda _one: signature["now"])
    world.mirror(folder("Techno", Low=(3,)))
    world.run()
    before = len(_asked(world))

    signature["now"] = "120:2"
    world.plan()

    assert len(_asked(world)) == before


def test_a_link_with_no_account_track_does_not_hide_a_miss(installed):
    ledger.record_mirror_misses(installed, {"c7": ("why", ("a",))})
    path = config.state_path("outbound_writes", installed)
    document = json.loads(path.read_text())
    document["mirror_links"]["c7"] = {"isrc": "X"}
    path.write_text(json.dumps(document))

    assert ledger.mirror_links(installed) == {}
    assert ledger.mirror_misses(installed) == {"c7": ("why", ("a",))}


def test_a_ledger_holding_a_link_and_a_miss_of_one_row_reads_the_link(installed):
    """A document an older build or a hand left in both maps: the miss gives way."""
    ledger.record_mirror_links(installed, {"c7": ("r7", "ISRC00007")})
    path = config.state_path("outbound_writes", installed)
    document = json.loads(path.read_text())
    document["mirror_misses"]["c7"] = {"reason": "why", "under": ["a"]}
    path.write_text(json.dumps(document))

    assert ledger.mirror_misses(installed) == {}


def test_linking_a_row_takes_its_miss_out_of_the_document(installed):
    ledger.record_mirror_misses(installed, {"c7": ("why", ("a",))})

    ledger.record_mirror_links(installed, {"c7": ("r7", "ISRC00007")})

    raw = json.loads(config.state_path("outbound_writes", installed).read_text())
    assert "c7" not in raw["mirror_misses"]


def test_a_miss_over_a_linked_row_is_never_written_to_the_document(installed):
    ledger.record_mirror_links(installed, {"c7": ("r7", "ISRC00007")})

    ledger.record_mirror_misses(installed, {"c7": ("why", ("a",)), "c8": ("why", ("b",))})

    raw = json.loads(config.state_path("outbound_writes", installed).read_text())
    assert set(raw["mirror_misses"]) == {"c8"}


def test_a_plan_that_cannot_be_frozen_stands_and_the_apply_plans_afresh(installed, monkeypatch):
    world = World(installed, monkeypatch)
    world.mirror(folder("Techno", Low=(1,)))
    blocked = config.state_path("mirror_plans", installed)
    blocked.parent.mkdir(parents=True, exist_ok=True)
    blocked.write_text("a file where the directory goes", encoding="utf-8")

    shown = _plan(world, _shown())
    applied = _plan(world, _decided())

    assert shown.steps[0].state == "planned"
    assert shown.facts[account_mirror.FROZEN_FACT].startswith("not frozen (")
    assert "so it was planned afresh" in applied.facts[account_mirror.FROZEN_FACT]
    assert applied.digest() == shown.digest()
