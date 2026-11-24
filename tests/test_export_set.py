"""R-837: a set becomes a private playlist on the account, and is archived.

Through the real dispatcher with catalogue and account faked; a real account is attended.
"""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.acquire import match
from cratekit.cli import registry
from cratekit.core import review, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.export import set_cli
from cratekit.intake import candidates
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import ledger, sets
from cratekit.sync import mark_record
from cratekit.sync import playlists as sync_playlists
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_intake_missing_search import Hit
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import _asked
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_outbound_workers import bind as bind_account

BUILD = "export.set.confirm"
ARCHIVE = "export.archive.confirm"
NAME = "Warehouse Night"

#: Five rows. The provider's search names four exactly and nothing for the fifth.
ROWS = tuple((f"Artist {n}", f"Title {n}") for n in ("One", "Two", "Three", "Four", "Five"))
FIVE = ROWS[4]
SEARCHES = {
    (artist, title): [Hit(f"tid-{index}", artist, title)]
    for index, (artist, title) in enumerate(ROWS[:4], start=1)
}


@pytest.fixture
def account(installed, monkeypatch):
    """A catalogue that can search, and an account that records every call."""
    fake = FakeCatalogue(searches=dict(SEARCHES))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    return installed, fake, held


def _listed(cfg, name: str, text: str) -> Path:
    folder = cfg.library.root.parent / "lists"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(text, encoding="utf-8")
    return folder / name


def _tracklist(cfg, rows=ROWS, name: str = f"{NAME}.txt") -> Path:
    return _listed(cfg, name, "".join(f"{a} - {t}\n" for a, t in rows))


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on an explicit gate, then the run that carries them out."""
    refused = _asked(argv)
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _build(path: Path, option: str = "apply", *extra: str) -> tuple[int, dict]:
    return _two_acts(["export", "set", str(path), *extra], BUILD, option)


def _built(path: Path, option: str = "apply", *extra: str) -> dict:
    code, done = _build(path, option, *extra)
    assert code == int(ExitCode.OK), done
    return done


def _seventh(cfg, name: str) -> dict:
    """The one row of a tracklist of ``SEVEN``, planned and declined."""
    (row,) = _tracks(_built(_tracklist(cfg, rows=(SEVEN,), name=name), "abort"))
    return row


def _landed(cfg, name: str = "set-batch") -> Path:
    folder = cfg.library.root / "landed"
    folder.mkdir(parents=True, exist_ok=True)
    xml = folder / f"{name}_inboxed.xml"
    xml.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")
    return xml


def _archive(xml: Path, option: str = "apply", name: str = NAME) -> tuple[int, dict]:
    return _two_acts(["export", "archive", name, "--xml", str(xml)], ARCHIVE, option)


def _archived(xml: Path, option: str = "apply", name: str = NAME) -> dict:
    code, done = _archive(xml, option, name)
    assert code == int(ExitCode.OK), done
    return done


@pytest.fixture
def built(account):
    """``account`` with the five row set built on it and approved."""
    _built(_tracklist(account[0]))
    return account


def _tracks(done: dict) -> list[dict]:
    return [item for item in done["data"]["items"] if item["kind"] == "track"]


def _accepted(cfg, line: str, hits, option: str) -> None:
    """A person accepts ``option`` in review for the tracklist row ``line``."""
    (wanted,) = match.read_text_lines(f"{line}\n")
    answer = candidates.read_answer(wanted, tuple(hits))
    with review.open_store(cfg) as items:
        offered = candidates.propose(items, wanted, answer, handler_key="intake.missing")
    argv = ["review", "resolve", offered.item_id, "--verdict", "accepted", "--option", option]
    code, resolved = drive(argv)
    assert code == int(ExitCode.OK), resolved


# 1. The declaration
def test_both_verbs_write_only_the_account_behind_an_explicit_gate():
    for name, gate in (("export.set", BUILD), ("export.archive", ARCHIVE)):
        entry = registry.entry(name)
        assert entry.writes == frozenset({"remote"}), name
        assert entry.module_id == "export" and entry.feature_rows == (36,)
        # The set's second gate is the rename's (U140), held in its own suite.
        spec = entry.gates[0]
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"
        assert [one.name for one in entry.gates[1:]] == (
            ["export.set.rename"] if name == "export.set" else []
        )
    assert registry.entry("export.archive").destructive
    assert not registry.entry("export.set").destructive


def test_a_tracklist_name_keeps_the_digest_that_tells_two_recordings_apart():
    # Two recordings sharing a stem are two sets, each keyed by its name.
    named = {
        "REC001-aaaaaaaaaaaa.tracklist.txt": "REC001-aaaaaaaaaaaa",
        "REC001-bbbbbbbbbbbb.tracklist.txt": "REC001-bbbbbbbbbbbb",
        "typed set.txt": "typed set", "found.list.json": "found",
    }
    assert {name: set_cli.name_of(Path(name)) for name in named} == named
    assert set_cli.set_name(" Live / Boiler Room ") == "Live - Boiler Room"


# 2. The set playlist
def test_five_rows_with_one_unmatched_plan_four_and_name_the_fifth(account):
    cfg, _fake, held = account
    done = _built(_tracklist(cfg), "abort")
    assert done["outcome"] == "no_op" and held.created == [] and held.added == []
    rows = _tracks(done)
    assert [row["action"] for row in rows] == ["add"] * 4 + ["unmatched"]
    fifth = rows[4]
    assert (fifth["artist"], fifth["title"]) == ("Artist Five", "Title Five")
    assert fifth["why"] == "the provider's search returned nothing for it"
    assert done["data"]["totals"]["add"] == 4 and done["data"]["totals"]["unmatched"] == 1
    (warning,) = [w for w in done["warnings"] if w["code"] == "export-tracks-unmatched"]
    assert "Artist Five - Title Five: the provider's search returned nothing" in warning["message"]


def test_approved_the_account_holds_a_private_playlist_of_four_in_order(account):
    cfg, _fake, held = account
    done = _built(_tracklist(cfg))
    assert done["outcome"] == "ok"
    assert held.created == [NAME]
    (playlist,) = held.playlists
    assert playlist in held.private
    assert held.playlists[playlist] == ["tid-1", "tid-2", "tid-3", "tid-4"]
    recorded = ledger.set_playlist(cfg, NAME)
    assert recorded is not None and recorded.remote_id == playlist
    assert recorded.added == frozenset({"tid-1", "tid-2", "tid-3", "tid-4"})
    # The answer names the fifth on the run that wrote, too (R-850).
    assert any(w["code"] == "export-tracks-unmatched" for w in done["warnings"])


def test_a_second_run_onto_the_same_set_plans_nothing(account):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    _built(path)
    held.chunks.clear()
    done = _built(path)
    assert done["outcome"] == "no_op"
    assert done["data"]["totals"]["writes"] is False
    assert held.created == [NAME] and held.chunks == []
    assert [row["action"] for row in _tracks(done)] == ["already"] * 4 + ["unmatched"]


def test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist(built):
    cfg, fake, held = built
    fake.searches[FIVE] = [Hit("tid-5", *FIVE)]
    _built(_tracklist(cfg))
    assert held.created == [NAME]
    (playlist,) = held.playlists
    assert held.playlists[playlist][-1] == "tid-5"


def test_a_set_with_nothing_matched_makes_no_empty_playlist(account):
    cfg, _fake, held = account
    done = _built(_tracklist(cfg, rows=(("Nobody", "Nothing"),), name="empty.txt"))
    assert done["outcome"] == "no_op" and held.created == []
    assert ledger.set_playlist(cfg, "empty") is None


def test_a_search_the_provider_cannot_answer_refuses_before_the_gate(installed, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(UnreadableCatalogue()))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    code, refused = drive(["export", "set", str(_tracklist(installed))])
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "unavailable-transient"
    assert held.created == []


def test_two_exact_candidates_are_not_chosen_between(account):
    cfg, fake, held = account
    fake.searches[FIVE] = [Hit("tid-5a", *FIVE), Hit("tid-5b", *FIVE)]
    done = _built(_tracklist(cfg), "abort")
    fifth = _tracks(done)[4]
    assert fifth["action"] == "unmatched" and "several match it exactly" in fifth["why"]


def test_the_sweep_never_reads_a_set_playlist_as_intake(account, monkeypatch):
    from cratekit.sync import cli as sync_cli
    cfg, _fake, _held = account
    _built(_tracklist(cfg))
    built = ledger.set_playlist_ids(cfg)
    assert len(built) == 1
    (playlist_id,) = built
    listed = AccountPlaylist(playlist_id=playlist_id, name=NAME, tracks=4)
    excluded = sync_playlists.exclusion(listed, recorded=set(), in_flight=set(), set_built=built)
    assert excluded is sync_playlists.Excluded.SET_PLAYLIST
    handed: list[frozenset[str]] = []
    class Stop(Exception):
        pass
    def plan(store, cfg_, found, *, handler_key, label_built=frozenset(), set_built=frozenset(),
             paired=frozenset(), mirrored=frozenset()):
        handed.append(set_built)
        raise Stop
    monkeypatch.setattr(sync_playlists, "plan", plan)
    with pytest.raises(Stop):
        sync_cli._plan_playlists(SimpleNamespace(handler_key="intake.playlist"), None)
    assert handed == [built]


def _document(cfg, name: str, origin: str, rows: list[dict]) -> Path:
    return _listed(cfg, name, json.dumps({"list": 1, "origin": origin, "tracks": rows}))


def test_a_tidal_list_documents_own_identifiers_are_used_without_a_search(account):
    cfg, fake, held = account
    rows = [{"id": "tid-9", "title": "Title Nine", "artist": {"name": "Artist Nine"}}]
    _built(_document(cfg, "doc.list.json", "tidal", rows))
    assert fake.searched_for == []
    (playlist,) = held.playlists
    assert held.playlists[playlist] == ["tid-9"]


def test_another_sources_identifier_is_never_handed_to_the_account(account):
    cfg, fake, held = account
    rows = [{"id": "sp-1", "name": "Title One", "artists": [{"name": "Artist One"}]}]
    done = _built(_document(cfg, "spot.list.json", "spotify", rows), "abort")
    (row,) = _tracks(done)
    assert row["id"] != "sp-1"
    assert fake.searched_for, "the row was searched for rather than read off its source id"


def test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist(account):
    cfg, _fake, held = account
    held.unaddable.add("tid-2")
    done = _built(_tracklist(cfg))
    assert any(w["code"] == "export-set-tracks-refused" for w in done["warnings"])
    done = _built(_tracklist(cfg))
    actions = [row["action"] for row in _tracks(done)]
    assert actions == ["already", "refused", "already", "already", "unmatched"]
    assert "would not add it" in _tracks(done)[1]["why"]


def test_a_track_taken_off_by_a_person_is_said_and_not_put_back(built):
    cfg, _fake, held = built
    (playlist,) = held.playlists
    held.playlists[playlist].remove("tid-3")
    fake_rows = (*ROWS, ("Artist One", "Title One"))
    done = _built(_tracklist(cfg, rows=fake_rows))
    actions = [row["action"] for row in _tracks(done)]
    assert actions == ["already", "already", "taken-off", "already", "unmatched", "repeat"]
    assert "tid-3" not in held.playlists[playlist]


def test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for(built):
    cfg, fake, held = built
    (playlist,) = held.playlists
    # The fifth row's track was added by hand: on the playlist, never written here.
    held.playlists[playlist].append("tid-5")
    fake.searches[FIVE] = [Hit("tid-5", *FIVE)]
    held.chunks.clear()
    done = _built(_tracklist(cfg))
    assert done["outcome"] == "no_op" and held.chunks == []
    assert _tracks(done)[4]["action"] == "already"


def test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match(account):
    cfg, fake, held = account
    held.catalog["set-row-1"] = "tid-by-isrc"
    rows = [{"title": "Title Six", "artist": {"name": "Artist Six"}, "isrc": "QZABC2600001"}]
    done = _built(_document(cfg, "isrc.list.json", "tidal", rows))
    (row,) = _tracks(done)
    assert (row["id"], row["how"]) == ("tid-by-isrc", "isrc")
    assert held.matches[0]["isrc"] == "QZABC2600001" and fake.searched_for == []


def test_a_candidate_accepted_in_review_is_used_and_not_searched_for_again(account):
    cfg, fake, _held = account
    fake.searches[FIVE] = [Hit("tid-5a", *FIVE), Hit("tid-5b", *FIVE)]
    _accepted(cfg, "Artist Five - Title Five", fake.searches[FIVE], "tid-5b")
    fake.searched_for.clear()
    done = _built(_tracklist(cfg), "abort")
    fifth = _tracks(done)[4]
    assert (fifth["id"], fifth["how"], fifth["action"]) == ("tid-5b", "accepted", "add")
    assert FIVE not in fake.searched_for


# 2b. R-879: a set the library holds, and a search that fills its page
SEVEN = ("Artist Seven", "Title Seven")


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC, encoded once and copied per file, because ffmpeg is slow."""
    return synth_container(tmp_path_factory.mktemp("synth"), ".flac")


def _tagged(silence: Path, target: Path, **fields: str) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, target)
    assert tags.write_tags(target, fields)
    return target


def _held(silence, cfg, isrc: str = "", name: str = "Title Seven", album: str = "") -> Path:
    """A real file the library holds for ``SEVEN``, carrying ``isrc`` and ``album`` when given."""
    fields = {"artist": SEVEN[0], "title": f"04A - 126 - {name}", "isrc": isrc, "album": album}
    target = cfg.library.root / cfg.library.music_dir / f"04A - 126 - {SEVEN[0]} - {name}.flac"
    return _tagged(silence, target, **{key: value for key, value in fields.items() if value})


def _isrc_asked(album: str = "") -> dict:
    """What the account is asked for ``SEVEN`` by its held file's ISRC."""
    return {"identity": "set-row-1", "isrc": "QZABC2600007", "title": SEVEN[1], "artist": SEVEN[0],
            "album": album}


def _paged(account, hits: list) -> tuple[dict, FakeCatalogue]:
    """``SEVEN``'s row planned over a search serving ``hits``, and the catalogue that served it."""
    cfg, fake, _held = account
    fake.searches[SEVEN] = hits
    return _seventh(cfg, "paged.txt"), fake


def _filler(count: int, start: int = 0) -> list[Hit]:
    """Hits that resemble nothing the row says, to fill a page."""
    return [Hit(f"fill-{n}", "Other Act", f"Unrelated {n}") for n in range(start, start + count)]


@pytest.mark.parametrize(
    ("album", "handed", "listed"),
    # R-572: the set path reads the album beside the ISRC the way file_identity does.
    [("", "", "held.txt"), ("  Tidal Lines ", "Tidal Lines", "held-album.txt")],
    ids=["no-album-tag", "its-album-tag-handed-over"],
)
def test_a_row_the_library_holds_is_listed_by_its_files_isrc_with_no_search(
    account, silence, album, handed, listed
):
    cfg, fake, held = account
    _held(silence, cfg, isrc="QZABC2600007", album=album)
    held.catalog["set-row-1"] = "tid-by-file"
    row = _seventh(cfg, listed)
    assert (row["id"], row["how"], row["action"]) == ("tid-by-file", "library-isrc", "add")
    # Twice, once at the gate's refusal and once on the run that carries it out.
    asked = _isrc_asked(album=handed)
    assert held.matches == [asked, asked]
    assert held.agreeing == ["set-row-1", "set-row-1"], "a file's tag was trusted alone"
    assert fake.searched_for == []


def test_a_persons_answer_in_review_wins_over_the_librarys_file(account, silence):
    cfg, fake, held = account
    _held(silence, cfg, isrc="QZABC2600007")
    held.catalog["set-row-1"] = "tid-by-file"
    fake.searches[SEVEN] = [Hit("tid-7a", *SEVEN), Hit("tid-7b", *SEVEN)]
    _accepted(cfg, "Artist Seven - Title Seven", fake.searches[SEVEN], "tid-7b")
    row = _seventh(cfg, "held.txt")
    assert (row["id"], row["how"]) == ("tid-7b", "accepted")
    assert held.matches == []


def test_a_held_file_whose_isrc_the_account_cannot_name_is_searched_and_said(account, silence):
    cfg, fake, held = account
    _held(silence, cfg, isrc="QZABC2600007")
    row = _seventh(cfg, "held.txt")
    assert row["action"] == "unmatched"
    assert row["why"].startswith(
        "the provider names no single track under its library file's ISRC QZABC2600007; "
    )
    assert fake.searched_for == [SEVEN, SEVEN]


def test_held_copies_carrying_different_isrcs_ask_the_account_nothing(account, silence):
    cfg, fake, held = account
    _held(silence, cfg, isrc="QZABC2600007")
    music = cfg.library.root / cfg.library.music_dir
    copy = music / "copy" / f"04A - 126 - {SEVEN[0]} - {SEVEN[1]}.flac"
    _tagged(silence, copy, artist=SEVEN[0], title=f"04A - 126 - {SEVEN[1]}", isrc="QZABC2600009")
    row = _seventh(cfg, "held.txt")
    assert held.matches == []
    assert row["why"].startswith(
        "the library holds it in 2 file(s) carrying 2 different ISRCs, so none was asked about; "
    )


def test_another_versions_isrc_is_not_the_rows(account, silence):
    cfg, _fake, held = account
    _held(silence, cfg, isrc="QZABC2600007")
    _held(silence, cfg, isrc="QZABC2600010", name="Title Seven (Extended Mix)")
    held.catalog["set-row-1"] = "tid-by-file"
    row = _seventh(cfg, "held.txt")
    assert (row["id"], row["how"]) == ("tid-by-file", "library-isrc")
    assert {one["isrc"] for one in held.matches} == {"QZABC2600007"}


@pytest.mark.parametrize(
    "isrc, name",
    [("QZABC2600010", "Title Seven (Extended Mix)"), ("QZABC2600008", "Another Title")],
    ids=["held-only-at-another-version", "not-held"],
)
def test_a_row_the_library_does_not_hold_asks_the_account_nothing(account, silence, isrc, name):
    """A file of another version, or another title, is not the row's."""
    cfg, _fake, held = account
    _held(silence, cfg, isrc=isrc, name=name)
    row = _seventh(cfg, "held.txt")
    assert held.matches == []
    assert row["why"] == "the provider's search returned nothing for it"


def test_a_held_file_with_no_isrc_is_searched_and_says_so(account, silence):
    cfg, fake, held = account
    _held(silence, cfg)
    row = _seventh(cfg, "held.txt")
    assert row["why"].startswith("the library holds it and its file carries no ISRC; ")
    assert held.matches == [] and fake.searched_for == [SEVEN, SEVEN]


def test_an_absent_music_folder_is_said_and_never_read_as_holding_nothing(account):
    cfg, _fake, held = account
    (cfg.library.root / cfg.library.music_dir).rmdir()
    row = _seventh(cfg, "held.txt")
    assert "music folder" in row["why"] and "is not there" in row["why"]
    assert held.matches == []


def test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it(account):
    row, fake = _paged(account, [Hit("tid-7", *SEVEN), *_filler(49), *_filler(10, start=49)])
    assert (row["id"], row["how"], row["action"]) == ("tid-7", "search", "add")
    assert fake.pages_asked == [(*SEVEN, 0), (*SEVEN, catalogue.TRACK_SEARCH_PAGE)] * 2


@pytest.mark.parametrize(
    "hits",
    [[*_filler(50), Hit("tid-7", *SEVEN)],
     [Hit("tid-7", *SEVEN), *_filler(49), Hit("tid-7", *SEVEN)]],
    ids=["on-the-second-page-alone", "served-again-on-the-next-page"],
)
def test_one_exact_track_over_two_pages_is_listed(account, hits):
    row, _fake = _paged(account, hits)
    assert (row["id"], row["how"]) == ("tid-7", "search")


def test_a_second_distinct_exact_match_on_the_next_page_leaves_it_out_as_several(account):
    row, _fake = _paged(account, [Hit("tid-7a", *SEVEN), *_filler(49), Hit("tid-7b", *SEVEN)])
    assert row["action"] == "unmatched"
    assert "several match it exactly, 2 distinct tracks" in row["why"]


def test_no_exact_match_on_any_page_leaves_it_out_as_none(account):
    near = Hit("tid-near", SEVEN[0], "Title Sevens")
    row, _fake = _paged(account, [*_filler(50), *_filler(5, start=50), near])
    assert row["action"] == "unmatched"
    assert row["why"].startswith(
        "the provider's search returned 56 hit(s) over 2 page(s) and none matches it exactly"
    )


def test_the_page_bound_reached_leaves_it_out_and_says_so(account):
    pages, page = candidates.SEARCH_PAGES, catalogue.TRACK_SEARCH_PAGE
    row, fake = _paged(account, [Hit("tid-7", *SEVEN), *_filler(pages * page + 20 - 1)])
    assert row["action"] == "unmatched"
    assert "the page bound was reached with one exact match" in row["why"]
    assert [offset for *_row, offset in fake.pages_asked] == [n * page for n in range(pages)] * 2


def test_the_walk_never_asks_past_the_providers_ceiling_of_300():
    """Past the client's documented 300 rows a page comes back empty, read as the end."""
    hits = [Hit("tid-7", *SEVEN), *_filler(399)]
    answer, asked = _walk("Artist Seven - Title Seven", hits)
    assert max(asked) + catalogue.TRACK_SEARCH_PAGE <= 300
    assert answer.full and candidates.sole_exact(answer) is None


def test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound(account):
    cfg, fake, _held_account = account
    row = ("Artist Seven", "Sun Path - Live")
    (wanted,) = match.read_text_lines("Artist Seven - Sun Path - Live\n")
    assert wanted.other_reading is not None, "the fixture's title no longer reads two ways"
    fake.searches[(wanted.artist, candidates.query_title(wanted))] = _filler(60)
    done = _built(_tracklist(cfg, rows=(row,), name="paged.txt"), "abort")
    (said,) = _tracks(done)
    assert "its title reads two ways" in said["why"], said["why"]
    assert "page bound" not in said["why"]


def test_an_exact_match_with_no_identifier_is_not_said_to_resemble_nothing(account):
    row, _fake = _paged(account, [Hit("", *SEVEN)])
    assert "carries no identifier" in row["why"]
    assert "none resembles it" not in row["why"]


def _walk(line: str, hits: list) -> tuple[candidates.Answer, list[int]]:
    """``search_pages`` over ``hits`` served a page at a time, and the offsets asked."""
    (wanted,) = match.read_text_lines(f"{line}\n")
    asked: list[int] = []
    def search(offset: int):
        asked.append(offset)
        return hits[offset : offset + catalogue.TRACK_SEARCH_PAGE]
    return candidates.search_pages(search, wanted), asked


def test_a_short_first_page_is_read_once():
    answer, asked = _walk("Artist Seven - Title Seven", [Hit("tid-7", *SEVEN)])
    assert asked == [0] and answer.pages == 1 and not answer.full
    assert candidates.sole_exact(answer).track.ref == "tid-7"


class _Unreadable:
    id = "tid-x"


@pytest.mark.parametrize(
    ("line", "hits", "said"),
    [
        ("Artist Seven - Title Seven", [Hit("tid-7a", *SEVEN), Hit("tid-7b", *SEVEN)], None),
        ("Artist Seven - Sun Path - Live",
         [Hit("tid-7", "Artist Seven", "Sun Path", version="Live")], lambda read: read.ambiguous),
        ("Artist Seven - Title Seven", [Hit("tid-7", *SEVEN), _Unreadable()],
         lambda answer: answer.unreadable == 1),
        ("Artist Seven - Title Seven", [Hit("", *SEVEN)], None),
    ],
    ids=["two-exact-matches", "a-title-that-reads-two-ways", "an-unreadable-row",
         "an-exact-match-with-no-identifier"],
)
def test_a_full_first_page_that_can_list_nothing_reads_no_second_page(line, hits, said):
    answer, asked = _walk(line, [*hits, *_filler(60)])
    if said is not None:
        assert said(answer), "the fixture no longer reads as its case says"
    assert asked == [0] and candidates.sole_exact(answer) is None


def test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists():
    hits = [Hit("tid-7", *SEVEN), *_filler(2 * catalogue.TRACK_SEARCH_PAGE - 1)]
    answer, asked = _walk("Artist Seven - Title Seven", hits)
    assert asked == [0, 50, 100], "the third page, empty, is the end of the listing"
    assert candidates.sole_exact(answer).track.ref == "tid-7"
    (wanted,) = match.read_text_lines("Artist Seven - Title Seven\n")
    two = candidates.read_pages(wanted, [tuple(hits[:50]), tuple(hits[50:100])])
    assert two.hits == 100 and two.full and candidates.sole_exact(two) is None


# 3. The archive
def test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once(built):
    cfg, _fake, held = built
    other = "Second Night"
    _built(_tracklist(cfg, name=f"{other}.txt"))
    year = ledger.set_playlist(cfg, NAME).year
    xml = _landed(cfg)
    done = _archived(xml)
    assert done["outcome"] == "ok"
    first = ledger.set_playlist(cfg, NAME).remote_id
    # U142: the set's folder is Downloaded Sets <year>, never the plain year.
    assert held.folders_created == [f"Downloaded Sets {year}"]
    (folder_item,) = [item for item in done["data"]["items"] if item["kind"] == "folder"]
    assert folder_item["name"] == f"Downloaded Sets {year}"
    (folder_id,) = held.folder_names
    assert held.placed[first] == folder_id
    # U242: NO TITLE CHANGES, the set is held as taken under the pass.
    assert held.titles[first] == NAME and held.renamed == []
    taken = mark_record.MarkRecord(cfg).taken()
    assert [(t.playlist_id, t.name, t.by, t.how) for t in taken.values()] == [
        (first, NAME, "set-batch", mark_record.BY_SET)
    ]
    done = _archived(xml, name=other)
    second = ledger.set_playlist(cfg, other).remote_id
    assert held.folders_created == [f"Downloaded Sets {year}"]
    assert held.placed[second] == folder_id


def test_a_playlist_already_in_its_folder_is_left(built):
    cfg, _fake, held = built
    xml = _landed(cfg)
    _archived(xml)
    held.moves.clear()
    held.renamed.clear()
    done = _archived(xml)
    assert done["outcome"] == "no_op"
    assert held.moves == [] and held.renamed == [] and len(held.folders_created) == 1


def test_a_year_folder_deleted_on_the_account_is_made_again(built):
    cfg, _fake, held = built
    _built(_tracklist(cfg, name="Second Night.txt"))
    xml = _landed(cfg)
    _archived(xml)
    (gone,) = held.folder_names
    del held.folder_names[gone]
    _archived(xml, name="Second Night")
    assert len(held.folders_created) == 2
    (fresh,) = held.folder_names
    assert fresh != gone
    assert held.placed[ledger.set_playlist(cfg, "Second Night").remote_id] == fresh
    year = ledger.set_playlist(cfg, "Second Night").year
    assert ledger.set_folder(cfg, f"Downloaded Sets {year}") == fresh
    assert ledger.set_folder(cfg, year) == ""


def test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled(built):
    cfg, _fake, held = built
    year = ledger.set_playlist(cfg, NAME).year
    held.folder_names["by-hand"] = f"Downloaded Sets {year}"
    _archived(_landed(cfg))
    assert held.folders_created == []
    assert held.placed[ledger.set_playlist(cfg, NAME).remote_id] == "by-hand"


def test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so(built):
    """U142: an adoption alone is no write, so no record is said to be replaced."""
    cfg, _fake, held = built
    recorded = ledger.set_playlist(cfg, NAME)
    folder_name = f"Downloaded Sets {recorded.year}"
    ledger.reserve_set_folder(cfg, folder_name, lambda: "gone-from-the-account")
    folder = held.create_folder(folder_name)
    made_by_hand = len(held.folders_created)
    held.placed[recorded.remote_id] = folder
    # A SET MARKED BY HAND BEFORE U242, its old prefix still on it.
    held.titles[recorded.remote_id] = f"DOWNLOADED {NAME}"
    argv = ["export", "archive", NAME, "--xml", str(_landed(cfg))]
    asked = _asked(argv)
    shown = asked["cause"]["detail"]["shown"]
    assert "recorded folder" not in shown
    assert shown["nothing to write"] == "the playlist is already in its folder and held as taken"
    done = _archived(_landed(cfg))
    assert done["outcome"] == "no_op"
    assert held.moves == [] and held.renamed == []
    assert len(held.folders_created) == made_by_hand
    assert ledger.set_folder(cfg, folder_name) == "gone-from-the-account"
    held.titles[recorded.remote_id] = "My Own Title"
    asked = _asked(argv)
    assert "as a person set it" in asked["cause"]["detail"]["shown"]["nothing to write"]


def test_two_folders_named_as_the_year_refuse_and_write_nothing(built):
    cfg, _fake, held = built
    year = ledger.set_playlist(cfg, NAME).year
    held.folder_names.update({"one": f"Downloaded Sets {year}", "two": f"Downloaded Sets {year}"})
    code, refused = drive(["export", "archive", NAME, "--xml", str(_landed(cfg))])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-set-ambiguous"
    assert f"Downloaded Sets {year}" in refused["cause"]["message"]
    assert held.moves == [] and held.renamed == []


def test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left(built):
    cfg, _fake, held = built
    playlist = ledger.set_playlist(cfg, NAME).remote_id
    held.titles[playlist] = "My Own Title"
    done = _archived(_landed(cfg))
    assert held.placed.get(playlist) and held.renamed == []
    assert any(w["code"] == "export-archive-changed-since-plan" for w in done["warnings"])
    assert mark_record.MarkRecord(cfg).taken() == {}


def test_a_name_with_a_slash_finds_the_set_it_named_at_build(account):
    cfg, _fake, held = account
    _built(_tracklist(cfg), "apply", "--name", "Live / Boiler Room")
    assert held.created == ["Live - Boiler Room"]
    done = _archived(_landed(cfg), name="Live / Boiler Room")
    assert done["outcome"] == "ok" and held.renamed == []
    assert ledger.set_playlist(cfg, "Live - Boiler Room").remote_id in (
        mark_record.MarkRecord(cfg).taken_ids()
    )


def test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed(built, monkeypatch):
    cfg, _fake, held = built
    lagging = {"on": True}
    listed = held.folder_playlists
    def folder_playlists(folder_id):
        return {} if lagging["on"] else listed(folder_id)
    monkeypatch.setattr(held, "folder_playlists", folder_playlists)
    done = _archived(_landed(cfg))
    assert held.moves and held.renamed == []
    (warning,) = [w for w in done["warnings"] if w["code"] == "export-archive-changed-since-plan"]
    assert "not yet listed" in warning["message"] and "retitled" not in warning["message"]
    lagging["on"] = False
    held.moves.clear()
    done = _archived(_landed(cfg))
    assert held.moves == [] and held.renamed == []
    assert ledger.set_playlist(cfg, NAME).remote_id in mark_record.MarkRecord(cfg).taken_ids()


def test_an_archive_with_no_landed_file_refuses_before_anything(built):
    cfg, _fake, held = built
    missing = cfg.library.root / "landed" / "never_inboxed.xml"
    code, refused = drive(["export", "archive", NAME, "--xml", str(missing)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert held.moves == [] and held.folders_created == []


def test_an_archive_of_a_set_never_made_says_so(account):
    cfg, _fake, held = account
    done = _archived(_landed(cfg), name="Never Made")
    assert done["outcome"] == "no_op"
    assert [w["code"] for w in done["warnings"]] == ["export-archive-nothing-built"]


def test_sync_unmark_takes_the_archive_mark_off_again(built):
    cfg, fake, held = built
    _archived(_landed(cfg))
    listed = held.titles.items()
    fake.account = [AccountPlaylist(playlist_id=p, name=t, tracks=None) for p, t in listed]
    held.renamed.clear()
    code, done = _two_acts(["sync", "unmark", "--pass", "set-batch"], "sync.unmark.confirm")
    assert code == int(ExitCode.OK), done
    assert held.renamed == [], "a release writes nothing on the account (U242)"
    assert mark_record.MarkRecord(cfg).taken_ids() == frozenset()


# 3b. The one gated loop both backfills share (U309)
def _loop(option: str, apply, *plans: tuple[str, bool]) -> dict:
    """The shared loop over ``plans`` (name, writes), its gate answered ``option``."""
    ctx = SimpleNamespace(
        gate=SimpleNamespace(require=lambda *_a, **_k: option),
        entry=SimpleNamespace(gates=(BUILD,)),
        envelope=lambda **shown: shown,
    )
    planned = [SimpleNamespace(name=name, writes=writes) for name, writes in plans]
    payload = {"totals": {"writes": True}}
    backfill = set_cli._SET_BACKFILL
    return set_cli._gate_then_apply_each(ctx, None, payload, {}, [], planned, apply, backfill)


def test_a_backfill_whose_gate_was_aborted_applies_nothing():
    """A backfill gate answered abort applies nothing and is a no op."""
    asked = []
    done = _loop("abort", lambda _cfg, one: (asked.append(one), [], True), ("a", True))
    assert (asked, done["outcome"]) == ([], set_cli.Outcome.NO_OP)


def test_a_backfill_skips_the_planless_and_names_only_what_wrote():
    """A plan writing nothing is never applied, and a set is named done only if it wrote."""
    asked = []

    def apply(_cfg, one):
        asked.append(one.name)
        return None, [], one.name == "wrote"

    done = _loop("apply", apply, ("planless", False), ("wrote", True), ("unchanged", True))
    assert asked == ["wrote", "unchanged"]
    assert done["data"]["totals"]["applied"] == {"playlists": ["wrote"]}


def test_a_backfill_failing_before_anything_landed_raises_it_as_is():
    """A failure before any set landed is raised as it was, not as a part way failure."""
    boom = RuntimeError("the account dropped the first write")

    def apply(_cfg, _one):
        raise boom

    with pytest.raises(RuntimeError) as raised:
        _loop("apply", apply, ("first", True))
    assert raised.value is boom


# 4. Add only, by the suite's own scan
@pytest.mark.parametrize(
    "source", [Path(sets.__file__), *sorted(Path(set_cli.__file__).parent.glob("set_*.py"))]
)
def test_no_removal_shape_appears_in_the_set_path(source):
    called = {
        node.func.attr
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8")))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    words = ("remove", "delete", "unheart", "clear")
    assert not {name for name in called if any(word in name for word in words)}
