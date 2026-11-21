"""U292: ``crate tag backlog`` sorts the needs genre backlog by cause, writing nothing.

Three layers, in the order they are trusted. The rules, pure: the cause of a
row, a proposal's evidence, a word's question and its recommendation. The
plan, against a disposable database and real tagged containers built by the
``tag suggest`` suite's fixtures, so each verb's own plan is what is counted.
Then the verb through the real dispatcher, its envelope validated, with a
recorded catalogue and never the network.

The genre words are the shipped taxonomy's. ``Indie Tech`` and ``Grime`` are
words no folder takes; ``amapiano`` is one tagging writes as a genre and
routing files nowhere, so neither ``taxonomy alias`` nor ``taxonomy folder``
takes it.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.adopt import genres as genres_report
from cratekit.adopt import scan as adopt_scan
from cratekit.core import active_taxonomy, config, locations, rb_writer, taxonomy
from cratekit.core import taxonomy_word as word_edit
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import backlog, rows, suggest
from cratekit.tagging.tag import SearchHit
from tests import test_tag_suggest as _suggest_suite
from tests.cli_drive import drive, drive_human

machine = _suggest_suite.machine
silence = _suggest_suite.silence
_release_process_locks = _suggest_suite._release_process_locks
_field_policies = _suggest_suite._field_policies
_reader_cache = _suggest_suite._reader_cache
_platform_seams = _suggest_suite._platform_seams

Track = _suggest_suite.Track
ABSENT = _suggest_suite.ABSENT

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "backlog"]

MELODIC = _suggest_suite.MELODIC
DEEP = _suggest_suite.DEEP
AFRO = _suggest_suite.AFRO
COARSE = _suggest_suite.COARSE
INDIE = "Indie Tech"
GRIME = "Grime"
#: Tagging writes it as a genre; routing files it nowhere.
AMAPIANO = "amapiano"


@pytest.fixture(autouse=True)
def _lookups(monkeypatch):
    """The off taxonomy words get lookup rows too, so a row can carry one."""
    monkeypatch.setattr(
        _suggest_suite, "LOOKUPS", (*_suggest_suite.LOOKUPS, INDIE, GRIME, AMAPIANO)
    )


def build(cfg, silence, *tracks):
    return _suggest_suite.build(cfg, silence, *tracks)


def _planned(cfg: config.Config, **kwargs) -> backlog.Backlog:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return backlog.plan_backlog(cfg, db, active_taxonomy.load(cfg), **kwargs)
    finally:
        rb_writer.close_db(db)


def _row(plan: backlog.Backlog, content_id: str) -> backlog.Row:
    (found,) = [row for row in plan.rows if row.content_id == content_id]
    return found


def _word(plan: backlog.Backlog, spelling: str) -> backlog.Word:
    (found,) = [word for word in plan.words if word.spelling.casefold() == spelling.casefold()]
    return found


def _census_needing(cfg: config.Config) -> set[str]:
    """Adoption's own census, asked directly: the rows it reads as needs genre."""
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        census = adopt_scan.scan_rows(
            collection.collection_rows(list(db.get_content())),
            active_taxonomy.load(cfg),
            root=Path(cfg.library.root),
            prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
            energy_reader=rows._no_energy,
        )
        return {
            track.content_id
            for track in census
            if track.disposition is adopt_scan.Disposition.NEEDS_GENRE
        }
    finally:
        rb_writer.close_db(db)


def _eight(genre: str = MELODIC, artist: str = "The Artist", folder: str = "one", first: int = 20):
    return [
        Track(str(first + n), genre, genre, artist=artist, folder=folder) for n in range(8)
    ]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree(cfg: config.Config) -> dict[str, str]:
    root = Path(cfg.library.root)
    found = {str(path): _sha(path) for path in root.rglob("*") if path.is_file()}
    found["db"] = _sha(Path(cfg.library.db_path))
    return found


# ═══════════════════════════════════════════════════════════════════════════
# 1. The rules
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("row", "file", "cause", "word"),
    [
        ("", "", backlog.NO_GENRE, ""),
        ("", MELODIC, backlog.ROW_LAGS_FILE, MELODIC),
        (INDIE, MELODIC, backlog.ROW_LAGS_FILE, MELODIC),
        (COARSE, "", backlog.TOO_COARSE, COARSE),
        ("", COARSE, backlog.TOO_COARSE, COARSE),
        (INDIE, "", backlog.OFF_TAXONOMY, INDIE),
        ("", INDIE, backlog.OFF_TAXONOMY, INDIE),
        (COARSE, INDIE, backlog.OFF_TAXONOMY, INDIE),
        (INDIE, COARSE, backlog.OFF_TAXONOMY, INDIE),
        (GRIME, INDIE, backlog.OFF_TAXONOMY, INDIE),
        ("  ", "  ", backlog.NO_GENRE, ""),
    ],
)
def test_the_cause_of_a_row_is_tested_in_order(row, file, cause, word):
    assert backlog.cause_of(DECLARED, row, file) == (cause, word)


def _item(votes, genre=MELODIC, band=suggest.HIGH, catalogue=None):
    return suggest.Item(
        content_id="1",
        path="p",
        artist="a",
        title="t",
        genre=genre,
        band=band,
        options=(genre,),
        votes=tuple(votes),
        catalogue=catalogue,
        action=suggest.WRITE,
    )


def test_a_proposal_from_a_catalogue_names_the_catalogue_and_its_word():
    asked = suggest.Asked(suggest.MATCHED, genre=MELODIC, source="discogs", source_genre="Melodic House")
    proposal = backlog.proposal_of(_item([(MELODIC, 6)], catalogue=asked))
    assert (proposal.source, proposal.source_genre) == ("discogs", "Melodic House")
    assert proposal.share == 1.0 and proposal.band == suggest.HIGH


def test_a_proposal_the_library_alone_voted_for_names_the_neighbours():
    declined = suggest.Asked(suggest.MATCHED, genre=DEEP, source="discogs", source_genre="Deep House")
    proposal = backlog.proposal_of(_item([(MELODIC, 16), (INDIE, 4)], catalogue=declined))
    assert proposal.source == backlog.NEIGHBOURS and proposal.source_genre == ""
    assert proposal.share == 0.8


def test_an_off_taxonomy_catalogue_match_is_not_the_source():
    asked = suggest.Asked(
        suggest.MATCHED, genre=MELODIC, source="beatport", source_genre="x", off_taxonomy=True
    )
    assert backlog.proposal_of(_item([(MELODIC, 8)], catalogue=asked)).source == backlog.NEIGHBOURS


def _members(count, spelling=INDIE, file=None, start=0):
    return [
        backlog.Row(
            content_id=str(start + n),
            path=f"p{n}",
            artist="",
            title="",
            row_word="",
            file_word=spelling if file is None else file,
            cause=backlog.OFF_TAXONOMY,
            word=spelling,
            status=backlog.ASKED,
        )
        for n in range(count)
    ]


def test_a_word_whose_neighbours_agree_recommends_their_genre_as_its_alias():
    word = backlog.word_of(DECLARED, _members(3), {MELODIC: 8}, 0)
    first = word.options[0]
    assert first.answer == backlog.ALIAS and first.command == f"{word_edit.ALIAS_VERB} 'Indie Tech' 'Melodic House'"
    assert [option.answer for option in word.options] == [backlog.ALIAS, backlog.FOLDER, backlog.LEAVE]
    assert first.rows == 3 and word.neighbour_band == suggest.HIGH


def test_a_word_at_the_folder_threshold_recommends_its_own_folder():
    word = backlog.word_of(DECLARED, _members(genres_report.FOLDER_WORTH), {MELODIC: 8}, 0)
    assert [option.answer for option in word.options] == [backlog.FOLDER, backlog.ALIAS, backlog.LEAVE]
    assert word.options[0].command == f"{word_edit.FOLDER_VERB} 'Indie Tech'"


def test_a_word_one_short_of_the_threshold_with_no_agreement_is_left_first():
    word = backlog.word_of(DECLARED, _members(genres_report.FOLDER_WORTH - 1), {MELODIC: 2, DEEP: 2}, 0)
    assert [option.answer for option in word.options] == [backlog.LEAVE, backlog.FOLDER]


def test_neighbours_agreeing_only_at_low_do_not_recommend_an_alias():
    word = backlog.word_of(DECLARED, _members(2), {MELODIC: 2}, 0)
    assert word.neighbour_band == suggest.LOW
    assert backlog.ALIAS not in [option.answer for option in word.options]


def test_a_word_counts_its_spellings_files_and_rows_apart():
    members = [
        *_members(3, INDIE),
        *_members(1, "indie tech", start=10),
        *_members(2, INDIE, file="", start=20),
    ]
    members = [replace(row, row_word=INDIE) if not row.file_word else row for row in members]
    word = backlog.word_of(DECLARED, members, {}, 1)
    assert word.spelling == INDIE and word.rows == 6
    assert word.spellings == ((INDIE, 5), ("indie tech", 1))
    assert (word.files_carry, word.several, word.row_only, word.exact) == (3, 1, 2, 5)
    folder = next(option for option in word.options if option.answer == backlog.FOLDER)
    assert folder.rows == 5


def test_a_word_neither_answer_takes_asks_nothing_and_says_why():
    word = backlog.word_of(DECLARED, _members(2, AMAPIANO), {MELODIC: 8}, 0)
    assert word.options == ()
    why, message, step = word.unanswerable
    assert why == word_edit.ALREADY_FILED and "already has a place" in message and step
    assert word.to_json()["question"] is None


def test_a_neighbour_votes_once_for_a_whole_word_at_its_higher_weight():
    live = {
        "1": backlog._Live("1", "A", "f", INDIE, "t"),
        "2": backlog._Live("2", "A", "f", INDIE, "t"),
        "3": backlog._Live("3", "A", "f", MELODIC, "t"),
        "4": backlog._Live("4", "B", "f", DEEP, "t"),
        "5": backlog._Live("5", "A", "g", GRIME, "t"),
    }
    assert backlog.neighbour_votes(["1", "2"], live, DECLARED) == {
        MELODIC: suggest.ARTIST_WEIGHT,
        DEEP: suggest.FOLDER_WEIGHT,
    }


def test_the_digest_names_no_copy():
    row = backlog.Row("1", "/a/one.flac", "x", "y", "", "", backlog.NO_GENRE, "", backlog.LEFT)
    one = backlog.Backlog(rows=(row,), words=(), tracks=1, catalogue=False)
    other = backlog.Backlog(
        rows=(replace(row, path="/b/elsewhere.flac", artist="z", title="w"),),
        words=(),
        tracks=1,
        catalogue=False,
    )
    assert one.digest == other.digest
    moved = backlog.Backlog(rows=(replace(row, reason="x"),), words=(), tracks=1, catalogue=False)
    assert moved.digest != one.digest


# ═══════════════════════════════════════════════════════════════════════════
# 2. The plan
# ═══════════════════════════════════════════════════════════════════════════


def _library():
    return [
        # Routed, so never in the backlog.
        *_eight(MELODIC, "The Artist", "one", 20),
        # A row lagging its file, which tag rows writes.
        Track("10", "", MELODIC, artist="Someone", folder="two"),
        # A row lagging a file whose genre the library has no lookup row for.
        Track("11", "", AFRO, artist="Someone", folder="two"),
        # No genre anywhere, beside eight agreeing tracks by the artist.
        Track("12", "", "", artist="The Artist", folder="one"),
        # No genre anywhere and nothing beside it.
        Track("13", "", "", artist="Nobody", folder="three"),
        # A catch all.
        Track("14", COARSE, "", artist="Nobody", folder="three"),
        # A word no folder takes, on two files, one in another case, and on a
        # row alone.
        Track("15", "", INDIE, artist="The Artist", folder="four"),
        Track("16", "", "indie tech", artist="The Artist", folder="four"),
        Track("17", INDIE, "", artist="The Artist", folder="four"),
        # A word neither answer takes.
        Track("18", "", AMAPIANO, artist="Nobody", folder="three"),
        # A tombstone carrying no genre, which nobody reads.
        Track("19", "", "", deleted=True),
    ]


def test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    ids = [row.content_id for row in plan.rows]
    assert len(ids) == len(set(ids))
    assert set(ids) == _census_needing(machine)
    assert not {str(20 + n) for n in range(8)} & set(ids) and "19" not in ids
    assert sum(plan.counts.values()) == len(plan.rows) == sum(plan.statuses.values())
    assert plan.counts == {
        backlog.FILE_UNREAD: 0,
        backlog.ROW_LAGS_FILE: 2,
        backlog.NO_GENRE: 2,
        backlog.TOO_COARSE: 1,
        backlog.OFF_TAXONOMY: 4,
    }


def test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    served, unknown = _row(plan, "10"), _row(plan, "11")
    assert (served.cause, served.status, served.verb, served.word) == (
        backlog.ROW_LAGS_FILE,
        backlog.SERVED,
        backlog.ROWS_VERB,
        MELODIC,
    )
    assert (unknown.status, unknown.reason) == (backlog.LEFT, rows.GENRE_UNKNOWN)
    db = rb_writer.open_db(machine.library.db_path, unlock=False, cfg=machine)
    try:
        written = {item.content_id for item in rows.plan_rows(machine, db, DECLARED).writes}
    finally:
        rb_writer.close_db(db)
    assert {row.content_id for row in plan.rows if row.status == backlog.SERVED} == written & {
        row.content_id for row in plan.rows
    }


def test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours(machine, silence):
    build(machine, silence, *_library())
    row = _row(_planned(machine), "12")
    assert (row.status, row.verb) == (backlog.PROPOSED, backlog.SUGGEST_VERB)
    assert row.proposal.genre == MELODIC and row.proposal.band == suggest.HIGH
    assert row.proposal.source == backlog.NEIGHBOURS and row.proposal.share == 1.0


def test_a_row_below_the_floor_is_never_proposed_and_is_left_with_its_band(machine, silence):
    build(
        machine,
        silence,
        Track("30", MELODIC, MELODIC, artist="Pair", folder="x"),
        Track("31", MELODIC, MELODIC, artist="Pair", folder="y"),
        Track("32", "", "", artist="Pair", folder="z"),
    )
    plan = _planned(machine)
    row = _row(plan, "32")
    assert (row.status, row.reason, row.proposal) == (backlog.LEFT, suggest.BELOW_BAND, None)
    assert plan.proposals == ()
    assert any(entry["reason"] == suggest.BELOW_BAND for entry in plan.remainder())


def test_a_row_with_nothing_beside_it_is_left_with_no_votes(machine, silence):
    build(machine, silence, *_library())
    row = _row(_planned(machine), "13")
    assert (row.cause, row.status, row.reason) == (backlog.NO_GENRE, backlog.LEFT, suggest.NO_VOTES)


def test_a_catch_all_is_left_to_tag_retag(machine, silence):
    build(machine, silence, *_library())
    row = _row(_planned(machine), "14")
    assert (row.cause, row.status, row.verb, row.word) == (
        backlog.TOO_COARSE,
        backlog.LEFT,
        backlog.RETAG_VERB,
        COARSE,
    )


def test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows(machine, silence):
    build(machine, silence, *_library(), Track("40", "", GRIME, artist="Nobody", folder="five"))
    plan = _planned(machine)
    assert [word.spelling.casefold() for word in plan.words] == ["indie tech", AMAPIANO, "grime"]
    indie = _word(plan, INDIE)
    assert indie.rows == 3 and indie.files_carry == 2 and indie.row_only == 1
    assert {_row(plan, cid).status for cid in ("15", "16", "17")} == {backlog.ASKED}
    # The artist's eight Melodic House tracks vote, so the alias is recommended.
    assert indie.options[0].answer == backlog.ALIAS and indie.neighbour_genre == MELODIC


def test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    row = _row(plan, "18")
    assert row.status == backlog.LEFT
    assert row.reason == f"{backlog.UNANSWERABLE}:{word_edit.ALREADY_FILED}"
    assert _word(plan, AMAPIANO).options == ()


def test_a_file_whose_genre_cannot_be_read_is_its_own_cause(machine, silence):
    paths = build(machine, silence, Track("50", "", ""), Track("51", COARSE, ""))
    paths["50"].write_bytes(b"\x00" * 64)
    plan = _planned(machine)
    row = _row(plan, "50")
    assert (row.cause, row.status, row.reason) == (backlog.FILE_UNREAD, backlog.LEFT, rows.FILE_UNREADABLE)


def test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    commands = [step["command"] for step in plan.campaign()]
    assert commands == [
        backlog.ROWS_VERB,
        backlog.SUGGEST_VERB,
        f"{word_edit.ALIAS_VERB} WORD GENRE or {word_edit.FOLDER_VERB} WORD",
        backlog.ROWS_VERB,
        backlog.RESORT_VERB,
    ]
    rows_moved = [step["rows"] for step in plan.campaign()]
    assert rows_moved == [1, 1, 3, 2, 2]
    assert plan.projected() == {"now": 9, "no_word_answered": 7, "every_word_answered": 5}


def test_an_empty_backlog_plans_no_campaign(machine, silence):
    build(machine, silence, *_eight())
    plan = _planned(machine)
    assert plan.rows == () and plan.campaign() == [] and plan.words == ()


def test_the_plan_writes_nothing(machine, silence):
    build(machine, silence, *_library())
    before = _tree(machine)
    _planned(machine)
    assert _tree(machine) == before


# ═══════════════════════════════════════════════════════════════════════════
# 3. The catalogue
# ═══════════════════════════════════════════════════════════════════════════


class _Recorded:
    """A catalogue answering from recorded hits by title, counting what it was asked."""

    def __init__(self, hits):
        self.hits = hits
        self.asked: list[tuple[str, str]] = []

    def __call__(self, artist, title):
        self.asked.append((artist, title))
        return self.hits.get(title)


def test_a_lone_discogs_match_is_proposed_from_discogs_with_its_word(machine, silence):
    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))
    search = _Recorded(
        {"track 60": SearchHit(genre=DEEP, source="discogs", source_genre="Deep House")}
    )
    with suggest.KeptCatalogue(machine, suggest.catalogue_lookup(search)) as kept:
        plan = _planned(machine, catalogue=kept)
    row = _row(plan, "60")
    assert row.status == backlog.PROPOSED
    assert (row.proposal.genre, row.proposal.source, row.proposal.source_genre) == (
        DEEP,
        "discogs",
        "Deep House",
    )
    assert row.proposal.band == suggest.HIGH and plan.catalogue
    assert plan.campaign()[0]["command"] == f"{backlog.SUGGEST_VERB} --catalogue"


def test_only_a_row_with_no_genre_is_asked_of_the_catalogue(machine, silence):
    build(machine, silence, *_library())
    search = _Recorded({})
    with suggest.KeptCatalogue(machine, suggest.catalogue_lookup(search)) as kept:
        _planned(machine, catalogue=kept)
    assert {title for _artist, title in search.asked} == {"track 12", "track 13"}


# ═══════════════════════════════════════════════════════════════════════════
# 4. The verb
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_reports_the_backlog_and_asks_no_gate(machine, silence):
    build(machine, silence, *_library())
    before = _tree(machine)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    assert _tree(machine) == before
    data = envelope["data"]
    assert len(data["items"]) == 9 and data["chunk"] is None
    totals = data["totals"]
    assert totals["causes"][backlog.OFF_TAXONOMY] == 4 and totals["floor"] == backlog.FLOOR
    assert totals["projected"]["now"] == 9 and not totals["catalogue"]
    words = {word["word"]: word for word in totals["words"]}
    assert words[INDIE]["question"].startswith("Indie Tech: 3 track(s)")
    assert words[INDIE]["recommended"] == 0 and words[INDIE]["options"][0]["answer"] == backlog.ALIAS
    codes = {warning["code"] for warning in envelope["warnings"]}
    assert {"backlog-words-asked", "backlog-library-alone", "backlog-remainder"} <= codes
    assert all("path" in item for item in data["items"])


def test_the_verb_with_catalogue_asks_the_recorded_catalogue_and_keeps_its_answers(
    machine, silence, monkeypatch
):
    from cratekit.tagging import published, searchers

    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))
    search = _Recorded(
        {"track 60": SearchHit(genre=DEEP, source="discogs", source_genre="Deep House")}
    )
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_taxonomy", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["proposal"]["source"] == "discogs" and item["status"] == backlog.PROPOSED
    assert search.asked == [("Nobody", "track 60")]
    # Kept for tag suggest, which reads the answer rather than asking again.
    assert suggest.catalogue_path(machine).exists()
    code, _again = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK) and len(search.asked) == 1


def test_a_catalogue_nobody_could_read_is_named(machine, silence, monkeypatch):
    from cratekit.core.cause import refuse
    from cratekit.tagging import published, searchers

    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))

    def blocked(artist, title):
        raise refuse("catalogue-unreachable", "blocked", origin=("test",))

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: blocked)
    monkeypatch.setattr(published, "for_taxonomy", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-catalogue-unread"]
    assert "could not be read for 1 row(s), 60" in warning["message"]


def test_an_empty_backlog_is_a_no_op(machine, silence):
    build(machine, silence, *_eight())
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK) and envelope["outcome"] == "no-op", envelope
    assert envelope["data"]["totals"]["campaign"] == []


def test_a_person_reads_the_backlog(machine, silence):
    build(machine, silence, *_library())
    code, text = drive_human(VERB)
    assert code == int(ExitCode.OK), text
    assert text.strip()


def test_the_verb_declares_no_write_and_no_gate():
    from cratekit.cli import registry

    entry = registry.entry("tag.backlog")
    assert entry.writes == frozenset() and not entry.destructive and entry.gates == ()
    assert entry.output_schema == "plan/1"
