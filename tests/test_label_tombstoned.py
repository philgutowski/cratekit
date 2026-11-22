"""U243: a track the library removed leaves its label year playlists and stays off."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from cratekit.core import tombstone
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import library, stores
from cratekit.label import catalogue, kept_reads, tombstoned
from cratekit.modules.outbound import ledger
from tests import outbound_fakes
from tests import test_label_dated as dated_suite
from tests import test_label_heard as heard_suite
from tests import test_label_playlists as playlists_suite
from tests import test_prune as prune_suite
from tests.cli_drive import drive
from tests.label_fakes import (
    FakeCatalogue,
    FakePagedArtist,
    FakeRelease,
    FakeTrack,
    catalogue_factory,
)
from tests.test_label_playlists import LABEL, LABEL_ID, LISTED
from tests.test_label_playlists_releases import _took
from tests.test_label_workers import register
from tests.test_outbound_workers import bind as bind_account
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

BUILD = "label.playlists.confirm"
DAY = "2026-10-09"
PRUNE = "label.prune.confirm"
ACT = "Label Act"


def _named(track_id: str, *, artists=(ACT,), version: str = "") -> FakeTrack:
    """A provider track carrying the words the downloader tags a file with."""
    track = FakeTrack(track_id)
    track.artists = [SimpleNamespace(name=name) for name in artists]
    track.name = f"Track {track_id}"
    track.full_name = f"Track {track_id} ({version})" if version else track.name
    return track


def _releases() -> dict:
    return {
        "r1": ([_named("t1"), _named("t2")], 2021), "r2": ([_named("t3")], 2022),
        "r3": ([_named("t4"), _named("t5", version="Dub")], 2023),
        "r4": ([_named("t6"), _named("t7", artists=(ACT, "A Guest"))], 2023),
        "r5": ([_named("t8")], None), "r6": ([_named("t9")], 2023),
    }


def _catalogue() -> FakeCatalogue:
    return FakeCatalogue(artists={LABEL_ID: FakePagedArtist(list(LISTED))}, releases=_releases(),
                         confirmed={"r1", "r2", "r3", "r4", "r5", "r7"})


def _tombstone(cfg, artist: str, title: str, content_id: str = "41") -> None:
    """A removal recorded by the deletion pass's own recorder, as a trash records it."""
    row = library.RemovedRow(content_id=content_id, recorded=f"/a/library/Music/{content_id}.flac",
                             sequence=50, size=11, artist=artist, title=title)
    stores.record_tombstone(cfg, row, actor="a-person", trashed_to="/a/trash")


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    refused = _gated(argv)
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _applied(argv: list[str], gate: str) -> dict:
    code, done = _two_acts(argv, gate)
    assert code == int(ExitCode.OK), done
    return done


def _prune() -> dict:
    return _applied(["label", "prune", LABEL], PRUNE)


def _build(*argv: str) -> dict:
    return _applied(["label", "playlists", LABEL, *argv], BUILD)


def _heard() -> None:
    """The heard verb's two acts, through the heard suite's own explicit gate check."""
    code, envelope = heard_suite._two_acts(heard_suite.VERB)
    assert code == int(ExitCode.OK), envelope


def _gated(argv: list[str]) -> dict:
    """The refusal ``argv`` stops at, its decision gate still to answer."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused


def _kept(tracks: list[dict], read_at: str | None = None) -> None:
    """A kept read of r3 holding ``tracks``, as an earlier run left it."""
    path = kept_reads.path_for(LABEL_ID)
    path.parent.mkdir(parents=True, exist_ok=True)
    read = {"read_at": read_at or datetime.now(timezone.utc).isoformat(), "year": 2023,
            "tracks": tracks}
    document = {"version": kept_reads.VERSION, "label_id": LABEL_ID, "reads": {"r3": read}}
    path.write_text(json.dumps(document), encoding="utf-8")


def _world(monkeypatch, fake: FakeCatalogue) -> outbound_fakes.StrictAccount:
    """Kompakt followed over ``fake``, and the strict account the verbs write."""
    register(LABEL)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    account = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, account)
    return account


@pytest.fixture
def followed(installed, monkeypatch):
    fake = _catalogue()
    account = _world(monkeypatch, fake)
    return SimpleNamespace(cfg=installed, fake=fake, account=account, monkeypatch=monkeypatch)


@pytest.fixture
def built(followed):
    _build()
    assert followed.account.playlists == {"pl-1": ["t1", "t2"], "pl-2": ["t3"],
                                          "pl-3": ["t4", "t5", "t6", "t7"]}
    return followed


def _taken(envelope: dict) -> list[tuple[str, str]]:
    return [(item["playlist"], item["id"]) for item in envelope["data"]["items"]
            if item["action"] == "take-off"]


# 1. The prune takes a removed track off


def test_a_tombstoned_track_on_a_year_playlist_is_pruned(built):
    """The card's live case: a removed track stayed on its label year playlist."""
    _tombstone(built.cfg, ACT, "Track t4")
    refused = _gated(["label", "prune", LABEL])
    assert "1 track(s)" in refused["cause"]["detail"]["shown"]["removed from the library"]
    done = _prune()
    assert _taken(done) == [("pl-3", "t4")]
    assert built.account.playlists["pl-3"] == ["t5", "t6", "t7"]
    year = ledger.label_shape(built.cfg, LABEL_ID).years["2023"]
    assert year.pruned == frozenset({"t4"})


def test_a_tombstone_matches_the_version_and_every_billed_artist(built):
    """The title with its version, and the artists joined as the downloader tags them."""
    _tombstone(built.cfg, ACT, "Track t5 (Dub)", content_id="42")
    _tombstone(built.cfg, f"{ACT}, A Guest", "Track t7", content_id="43")
    done = _prune()
    assert sorted(_taken(done)) == [("pl-3", "t5"), ("pl-3", "t7")]


# The version is part of the recording's identity.
@pytest.mark.parametrize(
    ("artist", "title"), [(ACT, "Track t5"), ("Another Act", "Track t4"), (ACT, "Track t44")]
)
def test_a_tombstone_of_another_version_takes_nothing_off(built, artist, title):
    _tombstone(built.cfg, artist, title)
    done = _prune()
    assert _taken(done) == []
    assert built.account.taken == []


def test_a_revoked_tombstone_takes_nothing_off(built):
    """Lifting the tombstone is the person taking the deletion back."""
    _tombstone(built.cfg, ACT, "Track t4")
    (record,) = stores.list_tombstones(built.cfg)
    stores.revoke_tombstone(built.cfg, record.suppression_id, actor="a-person")
    done = _prune()
    assert _taken(done) == []


def test_a_year_playlist_the_prune_empties_is_named_and_kept(built):
    _tombstone(built.cfg, ACT, "Track t3")
    refused = _gated(["label", "prune", LABEL])
    shown = refused["cause"]["detail"]["shown"]
    assert any("left empty" in line for line in shown["take off"]["Kompakt 2022"])
    done = _prune()
    assert done["data"]["totals"]["emptied"] == ["Kompakt 2022"]
    assert built.account.playlists["pl-2"] == []
    assert "pl-2" in built.account.titles, "an emptied year playlist was deleted"


def test_a_removed_track_stays_off_after_a_full_build(built):
    _tombstone(built.cfg, ACT, "Track t4")
    _prune()
    _build()
    assert built.account.playlists["pl-3"] == ["t5", "t6", "t7"]


# 2. A build never adds a removed track


def test_a_full_build_never_adds_a_tombstoned_track(followed):
    """A year built afresh, which is the build that used to put one back."""
    _tombstone(followed.cfg, ACT, "Track t4")
    refused = _gated(["label", "playlists", LABEL])
    said = refused["cause"]["detail"]["shown"]["removed from the library"]
    assert said.startswith("1 track(s)")
    _build()
    assert followed.account.playlists["pl-3"] == ["t5", "t6", "t7"]


def test_a_year_every_track_of_which_was_removed_is_not_made(followed):
    _tombstone(followed.cfg, ACT, "Track t3")
    _build()
    assert "Kompakt 2022" not in followed.account.titles.values()


def test_a_build_onto_an_adopted_year_does_not_add_a_removed_track(followed):
    """An adopted year is planned from its tracks on the account, not the ledger."""
    account = followed.account
    account.folder_names = {"f-hand": LABEL}
    made = account.create_playlist("Kompakt 2023")
    account.move_to_folder(made, "f-hand")
    account.playlists[made] = ["t5"]
    _tombstone(followed.cfg, ACT, "Track t4")
    _build()
    assert account.playlists[made] == ["t5", "t6", "t7"]


def test_a_releases_build_never_adds_a_tombstoned_track(followed):
    _took(followed.cfg, ("r3", "2023"))
    _tombstone(followed.cfg, ACT, "Track t4")
    _build("--releases")
    (made,) = [pid for pid, title in followed.account.titles.items() if title == "Kompakt 2023"]
    assert followed.account.playlists[made] == ["t5"]


# 3. The kept reads carry the words the question is asked under


def test_a_kept_read_judges_a_track_by_the_words_it_kept(followed):
    """The run that applies reads no release again, and still leaves the track out."""
    _gated(["label", "playlists", LABEL])
    stored = json.loads(kept_reads.path_for(LABEL_ID).read_text(encoding="utf-8"))
    assert stored["reads"]["r3"]["tracks"][1] == {
        "id": "t5", "available": True, "artist": ACT, "title": "Track t5 (Dub)"
    }
    _tombstone(followed.cfg, ACT, "Track t4")
    followed.fake.releases_asked_for.clear()
    _build()
    assert followed.fake.releases_asked_for == []
    assert followed.account.playlists["pl-3"] == ["t5", "t6", "t7"]


def test_a_kept_read_written_without_the_words_is_read_again(followed):
    """A read kept before this unit cannot be judged, so it is not judged blind."""
    _kept([{"id": "t4", "available": True}, {"id": "t5", "available": True}])
    _tombstone(followed.cfg, ACT, "Track t4")
    refused = _gated(["label", "playlists", LABEL])
    assert "r3" in followed.fake.releases_asked_for
    assert refused["cause"]["detail"]["shown"]["removed from the library"].startswith("1 ")


def test_a_kept_track_whose_words_are_not_text_is_refused(followed):
    _kept([{"id": "t4", "available": True, "artist": 5, "title": "x"}])
    code, refused = drive(["label", "playlists", LABEL])
    assert code != int(ExitCode.OK)
    assert refused["cause"]["reason"] == kept_reads.UNUSABLE


# 4. The question itself


def test_the_question_is_asked_of_one_read_of_the_store(installed, monkeypatch):
    _tombstone(installed, ACT, "Track t4")
    reads = []
    real = tombstoned.DecisionStore.suppressions
    def counted(self, *args, **kwargs):
        reads.append(1)
        return real(self, *args, **kwargs)
    monkeypatch.setattr(tombstoned.DecisionStore, "suppressions", counted)
    asked = tombstoned.Tombstoned(installed)
    assert asked(ACT, "Track t4") and not asked(ACT, "Track t5") and asked(ACT, "track t4")
    assert reads == [1]


def test_a_track_with_no_words_is_never_removed_and_reads_nothing(installed, monkeypatch):
    def unread(self, *args, **kwargs):
        raise AssertionError("the store was read for a track with nothing to ask under")
    monkeypatch.setattr(tombstoned.DecisionStore, "suppressions", unread)
    assert tombstoned.Tombstoned(installed)("", "") is False
    assert tombstoned.Tombstoned(installed)(" ", " ") is False


def test_the_companion_of_a_credited_deletion_answers_for_the_provider_spelling(installed):
    """A deletion of a credited title also writes the uncredited spelling, asked second."""
    _tombstone(installed, ACT, "Track t4 (feat. A Guest)")
    kinds = {record.kind for record in stores.list_tombstones(installed)}
    assert tombstone.KIND_VERSION_UNCREDITED in kinds
    assert tombstoned.Tombstoned(installed)(ACT, "Track t4")


def test_the_track_words_are_read_as_the_downloader_tags_them():
    track = _named("t1", artists=(ACT, "A Guest"), version="Dub")
    assert tombstoned.track_artist(track) == f"{ACT}, A Guest"
    assert tombstoned.track_title(track) == "Track t1 (Dub)"
    assert tombstoned.track_artist(SimpleNamespace(artist=SimpleNamespace(name="Lead"))) == "Lead"
    assert tombstoned.track_artist(SimpleNamespace(artist="Lead ")) == "Lead"
    assert tombstoned.track_artist(SimpleNamespace()) == ""
    assert tombstoned.track_title(SimpleNamespace(title="Plain")) == "Plain"
    assert tombstoned.track_title(SimpleNamespace(full_name="", name="Bare")) == "Bare"


# 5. Round one's findings: heard, the releases screen, a year of nothing


@pytest.fixture
def plain(installed, monkeypatch):
    """The heard suite's world: Kompakt followed over the shared unnamed tracks."""
    fake = playlists_suite._catalogue()
    return installed, fake, _world(monkeypatch, fake)


def test_hearing_a_dated_playlist_never_puts_a_removed_track_back(plain):
    """R1 B1: the prune took the track off the year and hearing merged it back."""
    cfg, fake, account = plain
    folder_id = heard_suite._made(cfg, fake, account, [dated_suite._answer(["r3", "r4"], DAY)])
    dated_id = heard_suite._ids(account, folder_id)[heard_suite.DATED]
    _tombstone(cfg, "", "Track t4")
    _prune()
    assert playlists_suite._years(account, folder_id)[heard_suite.YEAR] == ["t5", "t6", "t7"]
    refused = _gated(heard_suite.VERB)
    assert "1 left out as removed" in refused["cause"]["detail"]["shown"]["year playlist"]
    _heard()
    assert playlists_suite._years(account, folder_id)[heard_suite.YEAR] == ["t5", "t6", "t7"]
    # THE DATED PLAYLIST STILL GOES, with the removed track on it.
    assert heard_suite.DATED not in heard_suite._ids(account, folder_id)
    assert account.deleted == [(dated_id, ("t4", "t5", "t6", "t7"))]


def test_hearing_a_playlist_of_only_removed_tracks_needs_no_year(plain):
    cfg, fake, account = plain
    folder_id = heard_suite._made(cfg, fake, account, [dated_suite._answer(["r3"], DAY)])
    _tombstone(cfg, "", "Track t4", content_id="44")
    _tombstone(cfg, "", "Track t5", content_id="45")
    year_id = heard_suite._ids(account, folder_id)[heard_suite.YEAR]
    del account.placed[year_id]
    _heard()
    assert heard_suite.DATED not in heard_suite._ids(account, folder_id)


def test_a_releases_build_of_a_wholly_removed_release_says_why(followed):
    """R1 D1: the screen said the provider no longer lists a track it lists."""
    _took(followed.cfg, ("r2", "2022"))
    _tombstone(followed.cfg, ACT, "Track t3")
    refused = _gated(["label", "playlists", LABEL, "--releases"])
    said = refused["cause"]["detail"]["shown"]["nothing to build"]
    assert "1 track(s) of them were removed from the library" in said


def test_a_year_the_provider_plays_nothing_of_is_planned_as_before(followed):
    """R1 R6: only a year emptied by removals is left unmade."""
    followed.fake.releases["r2"][0][0].available = False
    _build()
    assert "Kompakt 2022" in followed.account.titles.values()


@pytest.mark.parametrize(
    "tracks",
    [
        [{"id": "t4", "available": True, "artist": ACT}],
        [{"id": "t4", "available": True, "title": "Track t4"}],
        [{"id": "t4", "available": True, "artist": ACT, "title": "Track t4"},
         {"id": "t5", "available": True}],
    ],
    ids=["no-title", "no-artist", "one-track-unnamed"],
)
def test_a_kept_read_missing_any_track_word_is_read_again(followed, tracks):
    _kept(tracks)
    _gated(["label", "playlists", LABEL])
    assert "r3" in followed.fake.releases_asked_for


# 6. Round two's findings: a single named for its track, a prune heard undid


def _with_a_single() -> FakeCatalogue:
    """The catalogue plus r8, a single whose title is its one track's."""
    releases = _releases()
    single = _named("t10")
    single.name = single.full_name = "Solo Cut"
    releases["r8"] = ([single], 2023)
    listed = [*LISTED, FakeRelease("r8", year="2023", title="Solo Cut")]
    return FakeCatalogue(artists={LABEL_ID: FakePagedArtist(listed)}, releases=releases,
                         confirmed={"r1", "r2", "r3", "r4", "r5", "r7", "r8"})


def test_a_removed_single_is_taken_off_though_its_release_is_suppressed(followed):
    """R2 B1: the tombstone suppressed the single's release, so its track went unjudged."""
    fake = _with_a_single()
    followed.monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    done = _build()
    assert followed.account.playlists["pl-3"][-1] == "t10"
    _tombstone(followed.cfg, ACT, "Solo Cut")
    refused = _gated(["label", "prune", LABEL])
    assert "removed from the library" in refused["cause"]["detail"]["shown"]
    done = _prune()
    assert _taken(done) == [("pl-3", "t10")]
    assert "t10" not in followed.account.playlists["pl-3"]


def test_hearing_never_merges_back_a_removed_single(installed, monkeypatch):
    """R2 B1's heard face: the dated playlist held the single from before the removal."""
    fake = _with_a_single()
    account = _world(monkeypatch, fake)
    answer = dated_suite._answer(["r3", "r8"], DAY)
    folder_id = heard_suite._made(installed, fake, account, [answer])
    year_id = heard_suite._ids(account, folder_id)[heard_suite.YEAR]
    # TAKEN OFF THE YEAR BY HAND, as the card's live session did.
    account.playlists[year_id] = [one for one in account.playlists[year_id] if one != "t10"]
    _tombstone(installed, ACT, "Solo Cut")
    _heard()
    assert "t10" not in account.playlists[year_id]


def test_hearing_never_undoes_a_prune_of_a_held_release(plain):
    """The class one step over: a track the prune took off the year stays off it."""
    cfg, fake, account = plain
    folder_id = heard_suite._made(cfg, fake, account, [dated_suite._answer(["r3", "r4"], DAY)])
    prune_suite._hold(cfg, "r3")
    _prune()
    assert playlists_suite._years(account, folder_id)[heard_suite.YEAR] == ["t6", "t7"]
    _heard()
    assert playlists_suite._years(account, folder_id)[heard_suite.YEAR] == ["t6", "t7"]
    assert heard_suite.DATED not in heard_suite._ids(account, folder_id)


def test_hearing_a_playlist_of_only_removed_tracks_says_nothing_goes_in_the_year(plain):
    cfg, fake, account = plain
    heard_suite._made(cfg, fake, account, [dated_suite._answer(["r3"], DAY)])
    _tombstone(cfg, "", "Track t4", content_id="44")
    _tombstone(cfg, "", "Track t5", content_id="45")
    refused = _gated(heard_suite.VERB)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["year playlist"].startswith("nothing goes in the year: all 2 track(s)")
    assert not [one for one in shown.get("items", []) if one.get("action") == "add"]
