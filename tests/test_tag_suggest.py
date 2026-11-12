"""U114: ``crate tag suggest`` offers a genre for a row with none, behind one gate.

Three layers, in the order they are trusted. The rules, pure: the band, the
weighing, what may be suggested. The plan, against a disposable database and
real tagged containers, one scenario per line of the brief. Then the verb
through the real dispatcher: the two acts R34 requires, the acknowledgment, the
stale digest, the declined row offered again, and the file and the row agreeing
after the write with no other column moved.

The genre words are the shipped taxonomy's. The library's lookup rows are
whatever this file seeds.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import hashlib
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.cli import gates
from cratekit.core import active_taxonomy, config, locations, rb_writer, session, tags, taxonomy
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import suggest, suggest_cli
from cratekit.tagging.tag import SearchHit
from tests import test_tag_rows as _rows_suite
from tests.cli_drive import drive
from tests.test_rb_writer_db import _build_disposable_database, _row

# The row verb's fixtures, shared rather than copied: the machine, its
# acknowledgment, the synthesized container, and the four autouse seams.
machine = _rows_suite.machine
acknowledged = _rows_suite.acknowledged
silence = _rows_suite.silence
_release_process_locks = _rows_suite._release_process_locks
_field_policies = _rows_suite._field_policies
_reader_cache = _rows_suite._reader_cache
_platform_seams = _rows_suite._platform_seams

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "suggest"]
GATE = suggest_cli.CONFIRM_GATE

MELODIC = "Melodic House"
DEEP = "Deep House"
PROGRESSIVE = "Progressive House"
#: Declared by the taxonomy and given no lookup row here.
AFRO = "Afro House"
#: A word adoption routes and the taxonomy does not name exactly.
LOOSE = "Dance"
#: A word the shipped taxonomy calls too coarse to be a final genre.
COARSE = next(word for word in DECLARED.fallback.too_coarse_as_source if word)

LOOKUPS = (MELODIC, DEEP, PROGRESSIVE, LOOSE, COARSE)

#: The two rows ``_build_disposable_database`` seeds. They record no path.
BASELINE = 2

ABSENT = object()


@dataclass(frozen=True)
class Track:
    """One row to seed and the file it names, under ``folder`` by ``artist``."""

    content_id: str
    row: str = ""
    file: object = ""
    artist: str = ""
    folder: str = "inbox"
    deleted: bool = False


def _genre_ids() -> dict[str, str]:
    return {name: str(ordinal) for ordinal, name in enumerate(LOOKUPS, start=100)}


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / "Music"


def _file(cfg: config.Config, track: Track) -> Path:
    return _music(cfg) / track.folder / f"track-{track.content_id}.flac"


def build(cfg: config.Config, silence: Path, *tracks: Track) -> dict[str, Path]:
    """A disposable database holding ``tracks``, each with the file it names."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    db_path = Path(cfg.library.db_path)
    _build_disposable_database(db_path, with_tag_category=False)
    ids = _genre_ids()
    artists: dict[str, str] = {}
    paths: dict[str, Path] = {}
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as db_session:
        for name, genre_id in ids.items():
            db_session.add(_row(tables.DjmdGenre, ID=genre_id, Name=name))
        for track in tracks:
            if track.artist and track.artist not in artists:
                artists[track.artist] = str(500 + len(artists))
                db_session.add(
                    _row(tables.DjmdArtist, ID=artists[track.artist], Name=track.artist)
                )
            path = _file(cfg, track)
            path.parent.mkdir(parents=True, exist_ok=True)
            if track.file is not ABSENT:
                shutil.copyfile(silence, path)
                if track.file:
                    assert tags.write_tags(path, {"genre": str(track.file)})
            paths[track.content_id] = path
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=track.content_id,
                    Title=f"track {track.content_id}",
                    ArtistID=artists.get(track.artist),
                    GenreID=ids.get(track.row),
                    BPM=12400,
                    Rating=3,
                    Commnt="a comment a person typed",
                    rb_local_deleted=1 if track.deleted else 0,
                    FolderPath=locations.location_url(path),
                )
            )
        db_session.commit()
    engine.dispose()
    collection.reset_cache()
    return paths


def _content(cfg: config.Config) -> dict[str, dict]:
    connection = sqlite3.connect(cfg.library.db_path)
    connection.row_factory = sqlite3.Row
    try:
        found = connection.execute("SELECT * FROM djmdContent").fetchall()
        return {str(row["ID"]): dict(row) for row in found}
    finally:
        connection.close()


def _genre_of(cfg: config.Config, content_id: str) -> str:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        ((name,),) = connection.execute(
            "SELECT g.Name FROM djmdContent c LEFT JOIN djmdGenre g ON g.ID = c.GenreID "
            "WHERE c.ID = ?",
            (content_id,),
        ).fetchall()
    finally:
        connection.close()
    return name or ""


def _bytes(paths: dict[str, Path]) -> dict[str, str]:
    return {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}


def _planned(cfg: config.Config, **kwargs) -> suggest.SuggestPlan:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return suggest.plan_suggestions(cfg, db, active_taxonomy.load(cfg), **kwargs)
    finally:
        rb_writer.close_db(db)


def _item(plan: suggest.SuggestPlan, content_id: str) -> suggest.Item:
    (found,) = [item for item in plan.items if item.content_id == content_id]
    return found


def _artist_of_eight(genre: str = MELODIC) -> list[Track]:
    """Eight tracks by one artist, all one genre, in a folder of their own."""
    return [Track(f"2{n}", genre, genre, artist="The Artist", folder="one") for n in range(8)]


class _Lookup:
    """A catalogue that answers from a table and counts what it was asked."""

    def __init__(self, answers: dict[str, suggest.Asked]):
        self.answers = answers
        self.asked: list[tuple[str, str, str]] = []

    def __call__(self, artist: str, title: str, isrc: str) -> suggest.Asked:
        self.asked.append((artist, title, isrc))
        return self.answers.get(title, suggest.Asked(suggest.DECLINED))


# ═══════════════════════════════════════════════════════════════════════════
# 1. The rules
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("weight", "total", "band"),
    [
        (16, 16, suggest.HIGH),
        (6, 6, suggest.HIGH),
        (5, 5, suggest.MEDIUM),
        (8, 10, suggest.HIGH),
        (7, 10, suggest.MEDIUM),
        (6, 10, suggest.MEDIUM),
        (5, 10, suggest.LOW),
        (2, 2, suggest.LOW),
        (3, 3, suggest.MEDIUM),
        (0, 4, suggest.NONE),
        (0, 0, suggest.NONE),
    ],
)
def test_the_band_is_the_share_over_enough_votes(weight, total, band):
    assert suggest.band_of(weight, total) == band


def test_only_a_genre_adoption_files_by_its_exact_name_is_suggestable():
    assert suggest.suggestable(DECLARED, MELODIC)
    assert suggest.suggestable(DECLARED, AFRO)
    assert not suggest.suggestable(DECLARED, LOOSE)
    assert not suggest.suggestable(DECLARED, COARSE)
    assert not suggest.suggestable(DECLARED, "")
    assert not suggest.suggestable(DECLARED, "Zydeco Polka Fusion")


def test_an_undeclared_word_lowers_the_agreement_and_is_never_suggested():
    genre, band, options = suggest.weigh(DECLARED, {LOOSE: 5, DEEP: 5})
    assert (genre, options) == (DEEP, (DEEP,))
    assert band == suggest.LOW
    assert suggest.weigh(DECLARED, {LOOSE: 9, COARSE: 3}) == ("", suggest.NONE, ())


def test_a_tie_between_declared_genres_is_a_split_with_no_default():
    assert suggest.weigh(DECLARED, {MELODIC: 2, DEEP: 2, LOOSE: 4}) == (
        "",
        suggest.SPLIT,
        (DEEP, MELODIC),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_an_artist_with_eight_tracks_all_melodic_house_suggests_it_high(machine, silence):
    build(machine, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    item = _item(_planned(machine), "10")
    assert (item.genre, item.band, item.action) == (MELODIC, suggest.HIGH, suggest.WRITE)
    assert item.votes == ((MELODIC, 8 * suggest.ARTIST_WEIGHT),)
    assert item.genre_id == _genre_ids()[MELODIC] and item.reason == ""


def test_a_folder_that_splits_evenly_offers_both_genres_and_no_default(machine, silence):
    build(
        machine,
        silence,
        Track("30", MELODIC, MELODIC, artist="a", folder="label"),
        Track("31", MELODIC, MELODIC, artist="b", folder="label"),
        Track("32", DEEP, DEEP, artist="c", folder="label"),
        Track("33", DEEP, DEEP, artist="d", folder="label"),
        Track("10", artist="e", folder="label"),
    )
    plan = _planned(machine)
    item = _item(plan, "10")
    assert (item.genre, item.band, item.options) == ("", suggest.SPLIT, (DEEP, MELODIC))
    assert (item.action, item.reason) == (suggest.LEAVE, suggest.TIED)
    assert plan.writes == ()


def test_a_neighbour_by_the_artist_in_the_same_folder_votes_once_at_the_artist_weight(
    machine, silence
):
    build(
        machine,
        silence,
        Track("30", DEEP, DEEP, artist="a", folder="label"),
        Track("10", artist="a", folder="label"),
    )
    assert _item(_planned(machine), "10").votes == ((DEEP, suggest.ARTIST_WEIGHT),)


def test_the_artist_outweighs_the_folder(machine, silence):
    build(
        machine,
        silence,
        Track("30", DEEP, DEEP, artist="a", folder="elsewhere"),
        Track("31", DEEP, DEEP, artist="a", folder="elsewhere"),
        Track("32", MELODIC, MELODIC, artist="b", folder="label"),
        Track("33", MELODIC, MELODIC, artist="c", folder="label"),
        Track("34", MELODIC, MELODIC, artist="d", folder="label"),
        Track("10", artist="A ", folder="label"),
    )
    item = _item(_planned(machine), "10")
    assert item.votes == ((DEEP, 4), (MELODIC, 3))
    assert (item.genre, item.band) == (DEEP, suggest.LOW)


def test_a_row_whose_file_carries_a_genre_its_row_lacks_votes_with_the_files_word(
    machine, silence
):
    build(
        machine,
        silence,
        *[Track(f"3{n}", "", DEEP, artist="a", folder="x") for n in range(3)],
        Track("10", artist="a", folder="y"),
    )
    plan = _planned(machine)
    assert plan.counts[suggest.FILE_HAS_GENRE] == 3
    item = _item(plan, "10")
    assert item.votes == ((DEEP, 3 * suggest.ARTIST_WEIGHT),)
    assert (item.genre, item.band) == (DEEP, suggest.HIGH)


def test_a_row_held_out_or_picked_is_not_looked_up(machine, silence):
    build(machine, silence, Track("10"), Track("11"), Track("12"))
    lookup = _Lookup({})
    with suggest.KeptCatalogue(machine, lookup) as kept:
        _planned(machine, catalogue=kept, leave=["10"], chosen={"11": DEEP})
    assert [title for _artist, title, _isrc in lookup.asked] == ["track 12"]


def test_a_catalogue_answer_outside_the_taxonomy_is_never_suggested(machine, silence):
    build(machine, silence, Track("10"), Track("11"), Track("12"))
    lookup = _Lookup(
        {
            "track 10": suggest.Asked(suggest.MATCHED, genre="Funky Groove", off_taxonomy=True),
            "track 11": suggest.Asked(suggest.MATCHED, genre=LOOSE),
            "track 12": suggest.Asked(suggest.MATCHED, genre=MELODIC, source="beatport"),
        }
    )
    with suggest.KeptCatalogue(machine, lookup) as kept:
        plan = _planned(machine, catalogue=kept)
    assert _item(plan, "10").votes == () and _item(plan, "10").reason == suggest.NO_VOTES
    assert _item(plan, "11").votes == () and _item(plan, "11").genre == ""
    twelve = _item(plan, "12")
    assert twelve.votes == ((MELODIC, suggest.CATALOGUE_WEIGHT),)
    assert (twelve.genre, twelve.band, twelve.action) == (MELODIC, suggest.HIGH, suggest.WRITE)
    assert twelve.catalogue.source == "beatport"


def test_a_row_with_a_genre_on_the_file_and_not_the_row_is_left_to_tag_rows(machine, silence):
    build(machine, silence, *_artist_of_eight(), Track("10", "", DEEP, artist="The Artist"))
    plan = _planned(machine)
    assert [item.content_id for item in plan.items] == []
    assert plan.counts[suggest.FILE_HAS_GENRE] == 1


def test_a_row_carrying_a_genre_is_counted_and_never_offered(machine, silence):
    build(machine, silence, Track("10", DEEP, ""), Track("11", DEEP, DEEP, deleted=True))
    plan = _planned(machine)
    assert plan.items == ()
    assert plan.counts[suggest.ROW_HAS_GENRE] == 1
    assert plan.rows == 1 + BASELINE


def test_every_live_row_lands_in_exactly_one_outcome(machine, silence):
    build(
        machine,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11", file=DEEP, folder="elsewhere"),
        Track("12", file=ABSENT),
        Track("13"),
    )
    plan = _planned(machine)
    wanted = dict.fromkeys(suggest.OUTCOMES, 0)
    wanted.update(
        {
            suggest.WRITE: 1,
            suggest.ROW_HAS_GENRE: 8,
            suggest.FILE_HAS_GENRE: 1,
            "file-missing": 1,
            suggest.NO_VOTES: 1,
            "no-path": BASELINE,
        }
    )
    assert dict(plan.counts) == wanted
    assert [item.content_id for item in plan.items] == ["10", "13"]


def test_a_suggestion_below_the_band_is_offered_and_written_only_when_widened(machine, silence):
    build(
        machine,
        silence,
        Track("30", MELODIC, MELODIC, artist="a", folder="label"),
        Track("31", MELODIC, MELODIC, artist="b", folder="label"),
        Track("32", MELODIC, MELODIC, artist="c", folder="label"),
        Track("33", DEEP, DEEP, artist="d", folder="label"),
        Track("10", artist="e", folder="label"),
    )
    held = _item(_planned(machine), "10")
    assert (held.genre, held.band, held.reason) == (MELODIC, suggest.MEDIUM, suggest.BELOW_BAND)
    widened = _item(_planned(machine, band=suggest.MEDIUM), "10")
    assert (widened.action, widened.genre) == (suggest.WRITE, MELODIC)
    assert _planned(machine).digest != _planned(machine, band=suggest.MEDIUM).digest


def test_a_person_picks_a_genre_for_a_split(machine, silence):
    build(
        machine,
        silence,
        Track("30", MELODIC, MELODIC, artist="a", folder="label"),
        Track("32", DEEP, DEEP, artist="c", folder="label"),
        Track("10", artist="e", folder="label"),
    )
    item = _item(_planned(machine, chosen={"10": PROGRESSIVE}), "10")
    assert (item.genre, item.action, item.chosen) == (PROGRESSIVE, suggest.WRITE, True)
    assert item.band == suggest.SPLIT and item.options == (DEEP, MELODIC)


def test_a_held_row_is_listed_and_left_and_a_stray_identifier_is_carried(machine, silence):
    build(machine, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    plan = _planned(machine, leave=["10", "99"], chosen={"98": DEEP})
    item = _item(plan, "10")
    assert (item.action, item.reason, item.genre) == (suggest.LEAVE, suggest.HELD_OUT, MELODIC)
    assert plan.unmatched == ("98", "99")
    assert plan.digest != _planned(machine, leave=["10"]).digest


def test_a_declared_genre_the_library_has_no_lookup_row_for_is_left(machine, silence):
    """A neighbour cannot carry such a genre, so it comes from a pick or a catalogue."""
    build(machine, silence, Track("10"))
    item = _item(_planned(machine, chosen={"10": AFRO}), "10")
    assert (item.genre, item.action, item.reason) == (AFRO, suggest.LEAVE, suggest.GENRE_UNKNOWN)


def test_the_plan_groups_by_genre_and_band(machine, silence):
    build(
        machine,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11", artist="The Artist"),
        Track("12"),
    )
    assert _planned(machine).groups() == [
        {"genre": MELODIC, "band": suggest.HIGH, "action": suggest.WRITE, "rows": 2},
        {"genre": "", "band": suggest.NONE, "action": suggest.LEAVE, "rows": 1},
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 3. The catalogue and its kept answers
# ═══════════════════════════════════════════════════════════════════════════


def _searcher(*hits):
    found = list(hits)
    calls: list[tuple[str, str]] = []

    def search(artist, title):
        calls.append((artist, title))
        hit = found.pop(0)
        if isinstance(hit, Exception):
            raise hit
        return hit

    return search, calls


def test_a_miss_is_asked_again_once_and_a_match_is_not():
    search, calls = _searcher(SearchHit(), SearchHit(genre=MELODIC, source="beatport"))
    answer = suggest.catalogue_lookup(search)("a", "t", "")
    assert (answer.said, answer.genre, len(calls)) == (suggest.MATCHED, MELODIC, 2)

    search, calls = _searcher(SearchHit(genre=DEEP, source="beatport"))
    assert suggest.catalogue_lookup(search)("a", "t", "").genre == DEEP and len(calls) == 1

    search, calls = _searcher(SearchHit(source="beatport", source_genre="Weird"))
    answer = suggest.catalogue_lookup(search)("a", "t", "")
    assert (answer.said, answer.source_genre, len(calls)) == (suggest.DECLINED, "Weird", 1)


def test_a_catalogue_that_cannot_be_read_is_this_rows_answer_and_is_not_asked_twice():
    unreachable = refuse("catalogue-unreachable", "no network")
    search, calls = _searcher(unreachable, unreachable)
    answer = suggest.catalogue_lookup(search)("a", "t", "")
    assert answer.said == suggest.UNREAD and "catalogue-unreachable" in answer.note
    assert len(calls) == 1

    search, calls = _searcher(SearchHit(unread=("beatport",)), SearchHit())
    assert suggest.catalogue_lookup(search)("a", "t", "").said == suggest.UNREAD
    assert len(calls) == 1


def test_three_rows_in_a_row_nobody_could_read_stop_the_walk_asking(machine):
    lookup = _Lookup({})
    lookup.answers = {f"t{n}": suggest.Asked(suggest.UNREAD, note="blocked") for n in range(9)}
    lookup.answers["t5"] = suggest.Asked(suggest.MATCHED, genre=DEEP)
    with suggest.KeptCatalogue(machine, lookup) as kept:
        answers = [kept.answer(str(n), "a", f"t{n}", "") for n in range(6)]
    assert [title for _artist, title, _isrc in lookup.asked] == ["t0", "t1", "t2"]
    assert kept.stopped and all(answer.said == suggest.UNREAD for answer in answers)
    assert "not asked" in answers[3].note


def test_an_unread_answer_between_two_reads_does_not_stop_the_walk(machine):
    lookup = _Lookup(
        {
            "t0": suggest.Asked(suggest.UNREAD),
            "t1": suggest.Asked(suggest.UNREAD),
            "t2": suggest.Asked(suggest.MATCHED, genre=DEEP),
            "t3": suggest.Asked(suggest.UNREAD),
            "t4": suggest.Asked(suggest.UNREAD),
        }
    )
    with suggest.KeptCatalogue(machine, lookup) as kept:
        for n in range(5):
            kept.answer(str(n), "a", f"t{n}", "")
    assert not kept.stopped and len(lookup.asked) == 5


def test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk(machine):
    """U244's review, round one, B2. With no Discogs token every row Beatport
    misses rides ``unread``, and three of them in a row stopped the walk asking
    Beatport too, telling the person the catalogues could not be read. A row
    left unread only by a catalogue nobody asked is not a refusal."""
    from urllib.parse import quote_plus

    from cratekit.tagging import searchers
    from tests.test_catalogue_searcher import _beatport_page, _beatport_track

    carried = {"Song Four", "Song Five"}
    titles = ["Song One", "Song Two", "Song Three", "Song Four", "Song Five"]
    searched: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        searched.append(url)
        hits = [
            _beatport_track("Bernard Badie", title, "Deep House")
            for title in carried
            if quote_plus(title) in url
        ]
        return searchers.Fetched(text=_beatport_page(hits), status=200)

    search = searchers.catalogue_searcher(DECLARED, fetch=fetch, sleep=lambda _s: None)
    with suggest.KeptCatalogue(machine, suggest.catalogue_lookup(search)) as kept:
        answers = [kept.answer(str(n), "Bernard Badie", t, "") for n, t in enumerate(titles)]

    assert not kept.stopped
    assert len({url for url in searched if url.startswith(searchers.BEATPORT_SEARCH)}) == 5
    assert [a.said for a in answers] == [suggest.UNREAD] * 3 + [suggest.MATCHED] * 2
    assert answers[0].passed_over == (searchers.DISCOGS,)
    assert searchers.DISCOGS_NO_TOKEN in answers[0].note
    assert "could not be read" not in answers[2].note


def test_a_row_a_catalogue_refused_beside_one_nobody_asked_still_counts():
    from cratekit.tagging import searchers
    from cratekit.tagging.tag import SourceAnswer

    hit = SearchHit(
        answers=(
            SourceAnswer("beatport", "blocked"),
            SourceAnswer("discogs", searchers.NOT_ASKED, note=searchers.DISCOGS_NO_TOKEN),
        ),
        unread=("beatport", "discogs"),
    )
    asked = suggest._asked_from(hit)
    assert asked.said == suggest.UNREAD and asked.passed_over == ()
    assert asked.note == "unread: beatport"


def test_a_kept_answer_keeps_what_it_passed_over(machine):
    today = date(2026, 11, 12)
    passed = suggest.Asked(suggest.UNREAD, note="unread: discogs", passed_over=("discogs",))
    lookup = _Lookup({"t": passed})
    with suggest.KeptCatalogue(machine, lookup, today=today) as kept:
        kept.answer("1", "a", "t", "")
    with suggest.KeptCatalogue(machine, lookup, today=today) as kept:
        again = kept.answer("1", "a", "t", "")
    assert again == passed and len(lookup.asked) == 1


def test_the_general_catalogue_is_asked_only_when_the_shops_gave_no_genre():
    asked: list[str | None] = []

    def published(hit, isrc):
        asked.append(isrc)
        return SearchHit(genre=PROGRESSIVE, source="deezer")

    search, _ = _searcher(SearchHit(), SearchHit())
    answer = suggest.catalogue_lookup(search, published)("a", "t", "ISRC1")
    assert (answer.genre, asked) == (PROGRESSIVE, ["ISRC1"])

    search, _ = _searcher(SearchHit(genre=DEEP))
    suggest.catalogue_lookup(search, published)("a", "t", "ISRC2")
    assert asked == ["ISRC1"]


def test_a_kept_answer_is_reused_and_one_a_week_old_is_asked_again(machine):
    today = date(2026, 10, 9)
    lookup = _Lookup({"t": suggest.Asked(suggest.MATCHED, genre=DEEP)})
    with suggest.KeptCatalogue(machine, lookup, today=today) as kept:
        assert kept.answer("1", "a", "t", "").genre == DEEP
    assert suggest.catalogue_path(machine).is_file()

    with suggest.KeptCatalogue(machine, lookup, today=today + timedelta(days=6)) as kept:
        assert kept.answer("1", "a", "t", "").genre == DEEP and kept.asked == 0
        # Asked for another title, the row is asked again.
        kept.answer("1", "a", "other", "")
        assert kept.asked == 1
    with suggest.KeptCatalogue(machine, lookup, today=today + timedelta(days=30)) as kept:
        kept.answer("1", "a", "other", "")
        assert kept.asked == 1


def test_an_answer_nobody_could_read_is_kept_for_the_day_only(machine):
    today = date(2026, 10, 9)
    lookup = _Lookup({"t": suggest.Asked(suggest.UNREAD, note="blocked")})
    with suggest.KeptCatalogue(machine, lookup, today=today) as kept:
        kept.answer("1", "a", "t", "")
    with suggest.KeptCatalogue(machine, lookup, today=today) as kept:
        assert kept.answer("1", "a", "t", "").note == "blocked" and kept.asked == 0
    with suggest.KeptCatalogue(machine, lookup, today=today + timedelta(days=1)) as kept:
        kept.answer("1", "a", "t", "")
        assert kept.asked == 1
    assert len(lookup.asked) == 2


def test_a_kept_file_that_cannot_be_read_is_asked_again(machine):
    path = suggest.catalogue_path(machine)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    lookup = _Lookup({"t": suggest.Asked(suggest.MATCHED, genre=DEEP)})
    with suggest.KeptCatalogue(machine, lookup) as kept:
        assert kept.answer("1", "a", "t", "").genre == DEEP and kept.asked == 1


# ═══════════════════════════════════════════════════════════════════════════
# 4. The verb
# ═══════════════════════════════════════════════════════════════════════════


def _first_act(verb: list[str] = VERB) -> tuple[str, dict]:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    return refused["run_id"], refused


def _decide(run_id: str, answer: str = "apply") -> None:
    decided, envelope = drive(["run", "decide", run_id, GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope


def _two_acts(verb: list[str] = VERB) -> tuple[int, dict, dict]:
    run_id, refused = _first_act(verb)
    _decide(run_id)
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def test_the_file_and_the_row_carry_the_genre_and_nothing_else_moved(acknowledged, silence):
    cfg = acknowledged
    paths = build(
        cfg,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11"),
    )
    before = _content(cfg)
    untouched = _bytes({key: path for key, path in paths.items() if key != "10"})

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == acted["data"]["digest"]
    assert {
        "genre": MELODIC,
        "band": suggest.HIGH,
        "action": suggest.WRITE,
        "rows": 1,
    } in shown["groups"]
    assert tags.read_genre_from_file(paths["10"]) == MELODIC
    assert _genre_of(cfg, "10") == MELODIC and _genre_of(cfg, "11") == ""
    assert _bytes({key: path for key, path in paths.items() if key != "10"}) == untouched
    after = _content(cfg)
    for content_id, was in before.items():
        moved = {
            column
            for column, value in after[content_id].items()
            if value != was[column] and column not in rb_writer.BOOKKEEPING_COLUMNS
        }
        assert moved == ({"GenreID"} if content_id == "10" else set()), content_id
    totals = acted["data"]["totals"]
    assert (totals["written"], totals["read_back"]) == (1, 1)
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes[0] == suggest_cli.GENRES_WRITTEN and suggest_cli.ROWS_LEFT in codes
    (record,) = session.records(cfg)
    assert record.workflow == suggest.WORKFLOW


def test_a_declined_plan_writes_nothing_and_the_row_is_offered_again(acknowledged, silence):
    cfg = acknowledged
    paths = build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    before, files = _content(cfg), _bytes(paths)

    run_id, refused = _first_act()
    _decide(run_id, "abort")
    code, declined = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK) and declined["outcome"] == "no_op", declined
    assert _content(cfg) == before and _bytes(paths) == files and session.records(cfg) == ()

    _again, shown = _first_act()
    assert shown["cause"]["detail"]["shown"]["digest"] == refused["cause"]["detail"]["shown"][
        "digest"
    ]


def test_a_row_left_out_stays_as_it_is_and_is_offered_next_run(acknowledged, silence):
    cfg = acknowledged
    build(
        cfg,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11", artist="The Artist"),
    )
    code, acted, _ = _two_acts([*VERB, "--leave", "11"])
    assert code == int(ExitCode.OK), acted
    assert (_genre_of(cfg, "10"), _genre_of(cfg, "11")) == (MELODIC, "")
    plan = _planned(cfg)
    assert [(item.content_id, item.action) for item in plan.items] == [("11", suggest.WRITE)]


def test_the_gate_refuses_a_plan_that_changed(acknowledged, silence):
    cfg = acknowledged
    paths = build(
        cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"), Track("11")
    )
    run_id, _ = _first_act()
    _decide(run_id)
    assert tags.write_tags(paths["11"], {"genre": DEEP})
    before, files = _content(cfg), _bytes(paths)

    code, stale = drive(["--run", run_id, *VERB])
    assert stale["cause"]["reason"] == "decision-stale", stale
    assert code != int(ExitCode.OK)
    assert _content(cfg) == before and _bytes(paths) == files and session.records(cfg) == ()


def test_the_gate_takes_no_inline_answer(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    code, refused = drive(["-d", f"{GATE}=apply", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _genre_of(cfg, "10") == ""


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine, silence):
    build(machine, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    code, envelope = drive(VERB)
    assert envelope["cause"]["reason"] == "backup-acknowledgment-missing", envelope
    assert code != int(ExitCode.OK)
    assert not gates.run_path(envelope["run_id"]).exists()
    assert _genre_of(machine, "10") == ""


def test_with_rekordbox_open_the_plan_is_read_and_no_file_is_written(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    paths = build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    files = _bytes(paths)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, running, _ = _two_acts()
    assert code != int(ExitCode.OK) and running["cause"]["reason"] == "rekordbox-running"
    assert _bytes(paths) == files and _genre_of(cfg, "10") == ""


def test_a_file_that_will_not_take_its_genre_leaves_its_row_and_the_rest_land(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    paths = build(
        cfg,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11", artist="The Artist"),
    )
    real = tags.write_genre
    monkeypatch.setattr(
        tags, "write_genre", lambda path, genre: False if path == paths["11"] else real(path, genre)
    )
    code, refused, _ = _two_acts()
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "tag-suggest-unwritten"
    assert refused["cause"]["detail"]["failed"] == ["11"]
    assert (_genre_of(cfg, "10"), _genre_of(cfg, "11")) == (MELODIC, "")
    assert tags.read_genre_from_file(paths["11"]) in (None, "")


def test_a_session_gate_that_refuses_leaves_every_file_as_it_was(
    acknowledged, silence, monkeypatch
):
    """The files are written inside the row session, behind its lock."""
    from cratekit.tagging import rows

    cfg = acknowledged
    paths = build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    files = _bytes(paths)
    run_id, _ = _first_act()
    _decide(run_id)

    def busy(*args, **kwargs):
        raise refuse("library-volume-mismatch", "the volume is not the recorded one")

    monkeypatch.setattr(rows.session, "assert_gates", busy)
    code, refused = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "library-volume-mismatch"
    assert _bytes(paths) == files and _genre_of(cfg, "10") == ""


def test_a_row_that_reads_back_wrong_also_names_the_files_that_did_not_take_it(
    acknowledged, silence, monkeypatch
):
    from cratekit.tagging import rows

    cfg = acknowledged
    paths = build(
        cfg,
        silence,
        *_artist_of_eight(),
        Track("10", artist="The Artist"),
        Track("11", artist="The Artist"),
    )
    real = tags.write_genre
    monkeypatch.setattr(
        tags, "write_genre", lambda path, genre: False if path == paths["11"] else real(path, genre)
    )
    monkeypatch.setattr(rows, "judge", lambda writes, *rest: (("10: reads wrong",), ()))
    code, refused, _ = _two_acts()
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "internal-error"
    assert "could not be written: 11" in refused["cause"]["message"]
    assert refused["cause"]["detail"]["files"]["failed"] == ["11"]


def test_a_file_given_a_genre_after_the_gate_is_left_and_named(
    acknowledged, silence, monkeypatch
):
    """Approved blank, carrying a genre by the time the write reaches it."""
    from cratekit.tagging import rows

    cfg = acknowledged
    paths = build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    real = rows.apply_rows

    def a_person_got_there_first(*args, **kwargs):
        assert tags.write_tags(paths["10"], {"genre": DEEP})
        return real(*args, **kwargs)

    monkeypatch.setattr(rows, "apply_rows", a_person_got_there_first)
    code, refused, _ = _two_acts()
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "tag-suggest-unwritten"
    assert refused["cause"]["detail"]["moved"] == ["10"]
    assert tags.read_genre_from_file(paths["10"]) == DEEP and _genre_of(cfg, "10") == ""


def test_a_file_the_writer_says_it_wrote_and_that_does_not_read_back_leaves_its_row(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    paths = build(cfg, silence, *_artist_of_eight(), Track("10", artist="The Artist"))
    monkeypatch.setattr(tags, "write_genre", lambda path, genre: True)
    code, refused, _ = _two_acts()
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "tag-suggest-unwritten"
    assert refused["cause"]["detail"]["wrong"] == ["10"]
    assert _genre_of(cfg, "10") == "" and not tags.read_genre_from_file(paths["10"])


def test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read(acknowledged, silence):
    build(acknowledged, silence, Track("10"))
    for value in (f"10={LOOSE}", "10", "=Deep House", f"10={DEEP}"):
        argv = [*VERB, "--set", value]
        if value == f"10={DEEP}":
            argv += ["--set", f"10={MELODIC}"]
        code, refused = drive(argv)
        assert refused["cause"]["reason"] == "review-selection-invalid", (value, refused)
        assert code != int(ExitCode.OK)


def test_an_empty_plan_still_asks_and_opens_nothing_to_write(acknowledged, silence, monkeypatch):
    cfg = acknowledged
    build(cfg, silence, Track("10", DEEP, DEEP))
    real_open = rb_writer.open_db

    def read_only(path, *args, require_closed=False, **kwargs):
        assert not require_closed, "an empty plan opened the database to write"
        return real_open(path, *args, require_closed=require_closed, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", read_only)
    code, acted, refused = _two_acts()
    assert refused["cause"]["detail"]["shown"]["count"] == 0
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert acted["warnings"][0]["code"] == suggest_cli.NOTHING_TO_WRITE


def test_the_catalogue_is_asked_once_across_the_two_acts(acknowledged, silence, monkeypatch):
    from cratekit.tagging import published, searchers

    cfg = acknowledged
    paths = build(cfg, silence, Track("10"))
    calls: list[tuple[str, str]] = []

    def search(artist, title):
        calls.append((artist, title))
        return SearchHit(genre=DEEP, source="beatport")

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_taxonomy", lambda declared: lambda hit, isrc: hit)
    code, acted, _ = _two_acts([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), acted
    assert calls == [("", "track 10")]
    assert tags.read_genre_from_file(paths["10"]) == DEEP and _genre_of(cfg, "10") == DEEP


def test_the_verb_declares_the_file_and_the_row():
    from cratekit.cli import registry

    entry = registry.find("tag.suggest") if hasattr(registry, "find") else None
    if entry is None:
        (entry,) = [one for one in registry.ENTRIES if one.name == "tag.suggest"]
    assert entry.writes == frozenset({"files", "db_metadata"}) and entry.destructive
    assert [gate.name for gate in entry.gates][0] == GATE
    assert entry.gates[0].explicit
