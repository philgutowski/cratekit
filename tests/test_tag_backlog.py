"""U292: ``crate tag backlog`` sorts the needs genre backlog by cause, writing nothing.

The rules pure, the plan on a disposable database with the ``tag suggest``
suite's containers, and the verb through the dispatcher on a recorded catalogue.

The words are the shipped taxonomy's: ``Indie Tech`` and ``Grime`` no folder
takes; ``amapiano`` and ``mpb`` alias a saved genre folder, answered by
``taxonomy alias``; ``alternative`` aliases a style sub, which neither verb
takes. Every answer is planned on the shipped template. D1 applies.
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
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

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
#: Tagging aliases of a genre folder; routing files them nowhere.
AMAPIANO = "amapiano"
MPB = "mpb"
RNB = "R&B"
#: A tagging alias of a style sub, which neither verb takes.
ALTERNATIVE = "alternative"
#: A genre adoption files by that ``taxonomy alias`` refuses as a GENRE.
SUB_GENRE = "House"

SHIPPED = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)


@pytest.fixture(autouse=True)
def _lookups(monkeypatch):
    """Off taxonomy words get lookup rows too, R&B among them, for ``tag rows`` to follow."""
    monkeypatch.setattr(
        _suggest_suite,
        "LOOKUPS",
        (*_suggest_suite.LOOKUPS, INDIE, GRIME, AMAPIANO, MPB, ALTERNATIVE, RNB, SUB_GENRE),
    )


@pytest.fixture(autouse=True)
def _active_copy(request):
    """A machine's library holds the shipped template as its active copy."""
    if "machine" not in request.fixturenames:
        return
    cfg = request.getfixturevalue("machine")
    path = config.state_path("taxonomy_active", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SHIPPED, encoding="utf-8")


def build(cfg, silence, *tracks):
    return _suggest_suite.build(cfg, silence, *tracks)


def _planned(cfg: config.Config, **kwargs) -> backlog.Backlog:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        _path, text = active_taxonomy.read_text(cfg)
        return backlog.plan_backlog(cfg, db, active_taxonomy.load(cfg), text=text, **kwargs)
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


# 1. The rules


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


def _word_of(members, votes, **kwargs):
    return backlog.word_of(DECLARED, SHIPPED, members, votes, **kwargs)


def test_a_word_whose_neighbours_agree_recommends_their_genre_as_its_alias():
    word = _word_of(_members(3), {MELODIC: 8})
    first = word.options[0]
    assert first.answer == backlog.ALIAS and first.command == f"{word_edit.ALIAS_VERB} 'Indie Tech' 'Melodic House'"
    assert [option.answer for option in word.options] == [backlog.ALIAS, backlog.FOLDER, backlog.LEAVE]
    assert first.rows == 3 and word.neighbours == ((MELODIC, 8),)


def _on_row(members, spelling=INDIE):
    """What tag rows would write onto each member: its file's word."""
    return {row.content_id: spelling for row in members}


def test_a_folder_that_would_file_the_threshold_is_recommended_first():
    members = _members(genres_report.FOLDER_WORTH)
    word = _word_of(members, {MELODIC: 8}, rows_write=_on_row(members))
    assert [option.answer for option in word.options] == [backlog.FOLDER, backlog.ALIAS, backlog.LEAVE]
    assert word.options[0].command == f"{word_edit.FOLDER_VERB} 'Indie Tech'"
    assert word.options[0].rows == genres_report.FOLDER_WORTH


def test_the_threshold_is_what_the_folder_files_not_every_spelling():
    """Round one: 30 rows of the spelling and 25 of another case recommended the folder on 55."""
    members = [*_members(30), *_members(25, "indie tech", start=100)]
    word = _word_of(members, {MELODIC: 8}, rows_write=_on_row(members[:30]))
    assert word.options[0].answer == backlog.ALIAS
    folder = next(option for option in word.options if option.answer == backlog.FOLDER)
    assert folder.rows == 30


def test_a_word_one_short_of_the_threshold_with_no_agreement_is_left_first():
    members = _members(genres_report.FOLDER_WORTH - 1)
    word = _word_of(members, {MELODIC: 2, DEEP: 2}, rows_write=_on_row(members))
    assert [option.answer for option in word.options] == [backlog.LEAVE, backlog.FOLDER]


def test_neighbours_agreeing_only_at_low_do_not_recommend_an_alias():
    word = _word_of(_members(2), {MELODIC: 2})
    assert backlog.ALIAS not in [option.answer for option in word.options]


def test_neighbours_agreeing_at_medium_recommend_their_alias():
    word = _word_of(_members(2), {MELODIC: 4, DEEP: 2})
    assert word.options[0].answer == backlog.ALIAS


def test_an_alias_the_verb_refuses_is_never_offered():
    """Round one: taxonomy alias refuses House as a genre, so recommending it was refused."""
    with pytest.raises(word_edit.Refused):
        word_edit.alias(SHIPPED, INDIE, SUB_GENRE)
    refused = _word_of(_members(3), {SUB_GENRE: 16})
    assert backlog.ALIAS not in [option.answer for option in refused.options]
    assert refused.options[0].answer == backlog.LEAVE
    taken = _word_of(_members(3), {MELODIC: 16, SUB_GENRE: 2})
    assert taken.options[0].label == f"An alias of {MELODIC}"


def test_an_alias_to_a_genre_the_library_has_no_entry_for_moves_nothing():
    word = _word_of(_members(3), {MELODIC: 8}, known=lambda genre: False)
    alias = next(option for option in word.options if option.answer == backlog.ALIAS)
    assert alias.rows == 0 and "no genre entry for Melodic House" in alias.detail
    # Round two: the files are retagged whatever the rows do, and said so.
    assert "3 file(s) holding the word alone are retagged Melodic House" in alias.detail
    assert "0 row(s) follow" in alias.detail
    # An alias moving no row is not recommended.
    assert word.options[0].answer == backlog.LEAVE


def test_a_word_the_copy_cannot_hold_is_refused_and_the_report_goes_on():
    """Round two: a control character the TOML parser refuses failed the verb."""
    word = _word_of(_members(2, "Odd\x7fWord"), {})
    assert word.options == () and word.unanswerable[0] == word_edit.WOULD_NOT_LOAD


def test_with_no_active_copy_no_word_is_answered():
    word = backlog.word_of(DECLARED, None, _members(3), {MELODIC: 8})
    assert word.options == () and word.unanswerable[0] == backlog.NO_COPY


def test_a_word_counts_its_spellings_files_and_rows_apart():
    members = [
        *_members(3, INDIE),
        *_members(1, "indie tech", start=10),
        *_members(2, INDIE, file="", start=20),
    ]
    members = [replace(row, row_word=INDIE) if not row.file_word else row for row in members]
    word = _word_of(members, {}, several=frozenset({"0"}), rows_write={"1": INDIE})
    assert word.spelling == INDIE and word.rows == 6
    assert word.spellings == ((INDIE, 5), ("indie tech", 1))
    assert (word.files_carry, word.several, word.elsewhere, word.on_row) == (3, 1, 2, 3)
    folder = next(option for option in word.options if option.answer == backlog.FOLDER)
    assert folder.rows == 3


def test_a_row_whose_file_holds_another_word_is_counted_elsewhere():
    """Round one: a word row over a catch-all file was in none of the three counts."""
    members = [replace(row, row_word=INDIE, file_word=COARSE) for row in _members(1)]
    word = _word_of(members, {})
    assert (word.files_carry, word.several, word.elsewhere) == (0, 0, 1)


def test_a_word_neither_answer_takes_asks_nothing_and_says_why():
    for answer in (lambda: word_edit.folder(SHIPPED, ALTERNATIVE), lambda: word_edit.alias(SHIPPED, ALTERNATIVE, MELODIC)):
        with pytest.raises(word_edit.Refused):
            answer()
    word = _word_of(_members(2, ALTERNATIVE), {MELODIC: 8})
    assert word.options == () and not word.settled
    why, message, step = word.unanswerable
    assert why == word_edit.ALREADY_FILED and "already has a place" in message and step
    assert word.to_json()["question"] is None


def test_a_word_already_saved_as_an_alias_has_one_answer_the_verb_takes():
    """Round one: called unanswerable, though taxonomy alias reaches its gate with it."""
    edit = word_edit.alias(SHIPPED, AMAPIANO, AFRO)
    assert not edit.writes
    word = _word_of(_members(2, AMAPIANO), {MELODIC: 8})
    assert word.settled == f"{word_edit.ALIAS_VERB} amapiano 'Afro House'"
    assert word.options == () and word.unanswerable is None and word.reached == {"0", "1"}


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


# 2. The plan


def _library():
    return [
        # Routed, so never in the backlog.
        *_eight(MELODIC, "The Artist", "one", 20),
        # A row lagging its file, which tag rows writes.
        Track("10", "", MELODIC, artist="Someone", folder="two"),
        # A row lagging a file whose genre the library has no lookup row for.
        Track("11", "", AFRO, artist="Someone", folder="two"),
        # No genre anywhere, in the folder of eight agreeing tracks.
        Track("12", "", "", artist="Solo", folder="one"),
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
        Track("18", "", ALTERNATIVE, artist="Nobody", folder="three"),
        # Two words with one answer each, an alias already saved: R&B has a
        # genre entry, so its row follows; Afro House has none.
        Track("41", "", MPB, artist="Nobody", folder="three"),
        Track("42", "", AMAPIANO, artist="Nobody", folder="three"),
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
        backlog.OFF_TAXONOMY: 6,
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
    lagging = {row.content_id for row in plan.rows if row.cause == backlog.ROW_LAGS_FILE}
    assert {row.content_id for row in plan.rows if row.status == backlog.SERVED} == written & lagging
    # TAG ROWS ALSO WRITES A WORD NO FOLDER TAKES onto a blank row, which moves
    # nothing out of needs genre, so those rows stay their word's.
    assert {"15", "18"} <= written and _row(plan, "15").cause == backlog.OFF_TAXONOMY


def test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours(machine, silence):
    build(machine, silence, *_library())
    row = _row(_planned(machine), "12")
    assert (row.status, row.verb) == (backlog.PROPOSED, backlog.SUGGEST_VERB)
    assert row.proposal.genre == MELODIC and row.proposal.band == suggest.HIGH
    assert row.proposal.source == backlog.NEIGHBOURS and row.proposal.share == 1.0
    assert row.proposal.votes == ((MELODIC, 8 * suggest.FOLDER_WEIGHT),)


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
    assert [word.spelling.casefold() for word in plan.words] == [
        "indie tech",
        ALTERNATIVE,
        AMAPIANO,
        "grime",
        MPB,
    ]
    indie = _word(plan, INDIE)
    assert (indie.rows, indie.files_carry, indie.elsewhere, indie.on_row) == (3, 2, 1, 2)
    assert {_row(plan, cid).status for cid in ("15", "16", "17")} == {backlog.ASKED}
    # The artist's eight Melodic House tracks vote, so the alias is recommended.
    assert indie.options[0].answer == backlog.ALIAS and indie.neighbours[0][0] == MELODIC
    assert [option.rows for option in indie.options] == [2, 2, 0]


def test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    row = _row(plan, "18")
    assert row.status == backlog.LEFT
    assert row.reason == f"{backlog.UNANSWERABLE}:{word_edit.ALREADY_FILED}"
    assert _word(plan, ALTERNATIVE).options == ()


def test_a_word_with_one_answer_moves_only_the_rows_it_reaches(machine, silence):
    build(machine, silence, *_library())
    plan = _planned(machine)
    mpb, amapiano = _row(plan, "41"), _row(plan, "42")
    assert (mpb.status, mpb.verb) == (backlog.SETTLED, f"{word_edit.ALIAS_VERB} mpb 'R&B'")
    assert (amapiano.status, amapiano.reason) == (backlog.LEFT, backlog.NOT_REACHED)
    assert _word(plan, AMAPIANO).settled and not _word(plan, AMAPIANO).reached


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
        f"{word_edit.ALIAS_VERB} mpb 'R&B'",
        f"{word_edit.ALIAS_VERB} WORD GENRE or {word_edit.FOLDER_VERB} WORD",
        backlog.ROWS_VERB,
        backlog.RESORT_VERB,
    ]
    rows_moved = [step["rows"] for step in plan.campaign()]
    assert rows_moved == [1, 1, 1, 2, 3, 3]
    assert plan.projected() == {"now": 11, "no_word_answered": 8, "every_word_answered": 6}


def test_an_empty_backlog_plans_no_campaign(machine, silence):
    build(machine, silence, *_eight())
    plan = _planned(machine)
    assert plan.rows == () and plan.campaign() == [] and plan.words == ()


def test_the_plan_writes_nothing(machine, silence):
    build(machine, silence, *_library())
    before = _tree(machine)
    _planned(machine)
    assert _tree(machine) == before


# 3. The catalogue


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


# 4. The verb


def test_the_verb_reports_the_backlog_and_asks_no_gate(machine, silence):
    build(machine, silence, *_library())
    before = _tree(machine)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    assert _tree(machine) == before
    totals = envelope["data"]["summary"]
    assert totals["causes"][backlog.OFF_TAXONOMY] == 6 and totals["floor"] == backlog.FLOOR
    assert totals["projected"]["now"] == 11 and not totals["catalogue"]
    words = {word["word"]: word for word in totals["words"]}
    assert words[INDIE]["question"].startswith("Indie Tech: 3 track(s)")
    assert words[INDIE]["recommended"] == 0 and words[INDIE]["options"][0]["answer"] == backlog.ALIAS
    codes = {warning["code"] for warning in envelope["warnings"]}
    assert {"backlog-words-asked", "backlog-library-alone", "backlog-remainder"} <= codes
    assert len(totals["items"]) == 11 and all("path" in item for item in totals["items"])
    keys = [check["key"] for check in envelope["data"]["checks"]]
    assert keys[0] == f"backlog.cause.{backlog.ROW_LAGS_FILE}" and keys[-1] == "backlog.projected"
    assert "backlog.word.Indie Tech" in keys and "backlog.step.1" in keys


def test_the_verb_with_catalogue_asks_the_recorded_catalogue_and_keeps_its_answers(
    machine, silence, monkeypatch
):
    from cratekit.tagging import published, searchers

    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))
    search = _Recorded(
        {"track 60": SearchHit(genre=DEEP, source="discogs", source_genre="Deep House")}
    )
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["summary"]["items"]
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
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-catalogue-unread"]
    assert "could not be read for 1 row(s), 60" in warning["message"]


def test_an_empty_backlog_is_a_no_op(machine, silence):
    build(machine, silence, *_eight())
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["summary"]["campaign"] == []


def test_a_person_reads_the_backlog(machine, silence):
    build(machine, silence, *_library())
    code, text = drive_human(VERB)
    assert code == int(ExitCode.OK), text
    assert "Indie Tech: 3 track(s) carry this genre word" in text
    assert "1) An alias of Melodic House (recommended)" in text
    assert "crate tag rows: 1 row(s)" in text and "11 row(s) need a genre now" in text
    assert "one answer, asking nothing: crate taxonomy alias mpb 'R&B'" in text


def test_the_verb_declares_no_write_and_no_gate():
    from cratekit.cli import registry

    entry = registry.entry("tag.backlog")
    assert entry.writes == frozenset() and not entry.destructive and entry.gates == ()
    assert entry.output_schema == "diagnostic/1"


# 5. What round one of the review drove


def test_rows_whose_file_is_not_here_are_counted_and_said(machine, silence):
    """Round one: three files unlinked read as a clean no op over 13 rows."""
    paths = build(machine, silence, *_eight(), Track("70", "", ""), Track("71", "", INDIE))
    paths["70"].unlink()
    paths["71"].unlink()
    paths["20"].unlink()
    plan = _planned(machine)
    assert plan.rows == () and plan.unread == {rows.FILE_MISSING: 3}
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK) and envelope["outcome"] == "ok", envelope
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-files-unread"]
    assert "3 row(s) are in no cause" in warning["message"]
    assert envelope["data"]["summary"]["unread"] == {rows.FILE_MISSING: 3}


def test_a_row_tag_rows_would_move_into_needs_genre_is_counted_back(machine, silence):
    """Round one: tag rows, the campaign's first step, writes a routed row that word."""
    build(machine, silence, Track("70", MELODIC, INDIE), Track("71", "", MELODIC))
    plan = _planned(machine)
    assert plan.joining == ("70",)
    assert plan.projected() == {"now": 1, "no_word_answered": 1, "every_word_answered": 1}
    code, envelope = drive(VERB)
    assert "backlog-rows-joining" in {w["code"] for w in envelope["warnings"]}


def test_a_neighbour_votes_with_its_files_word_as_tag_suggest_votes_it(machine, silence):
    """Round one: blank neighbour rows over Melodic House files said nothing until tag rows."""
    build(
        machine,
        silence,
        *[Track(str(20 + n), "", MELODIC, artist="The Artist", folder="one") for n in range(8)],
        Track("15", "", INDIE, artist="The Artist", folder="four"),
    )
    indie = _word(_planned(machine), INDIE)
    assert indie.neighbours == ((MELODIC, 8 * suggest.ARTIST_WEIGHT),)
    assert indie.options[0].answer == backlog.ALIAS


def test_a_folder_counts_a_row_only_where_tag_rows_would_write_its_word(machine, silence):
    """Round one: a file holding the word beside another genre is left by tag rows."""
    paths = build(machine, silence, Track("15", "", INDIE), Track("16", "", INDIE))
    from cratekit.core import tags

    assert tags.write_tag_values(paths["16"], "genre", [INDIE, DEEP])
    assert tags.read_tag_values(paths["16"], "genre") == (INDIE, DEEP)
    indie = _word(_planned(machine), INDIE)
    folder = next(option for option in indie.options if option.answer == backlog.FOLDER)
    assert folder.rows == 1 and indie.several == 1 and indie.files_carry == 1


def test_the_digest_covers_the_words_the_unread_and_the_joining():
    row = backlog.Row("1", "p", "", "", "", "", backlog.NO_GENRE, "", backlog.LEFT)
    base = backlog.Backlog(rows=(row,), words=(), tracks=1, catalogue=False)
    word = backlog.word_of(DECLARED, SHIPPED, _members(1), {})
    for other in (
        replace(base, words=(word,)),
        replace(base, catalogue=True),
        replace(base, unread={rows.FILE_MISSING: 1}),
        replace(base, joining=("9",)),
    ):
        assert other.digest != base.digest


def test_a_library_most_of_whose_rows_are_under_no_prefix_rule_refuses(machine, silence, monkeypatch):
    from cratekit.write import metadata_cli

    build(machine, silence, Track("70", "", ""))
    monkeypatch.setattr(
        metadata_cli,
        "resolution_totals",
        lambda cfg, db: metadata_cli.ResolutionTotals(
            active=10, unresolved=9, unmapped=9, prefixes={"/Elsewhere": 9}
        ),
    )
    code, envelope = drive(VERB)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "library-paths-majority-unresolved"


def test_discogs_passed_over_is_said_with_how_to_record_a_token(machine, silence, monkeypatch):
    from cratekit.tagging import searchers

    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))
    passed = suggest.Asked(
        suggest.UNREAD, note="unread: discogs, no token", passed_over=(searchers.DISCOGS,)
    )
    monkeypatch.setattr(suggest, "catalogue_lookup", lambda *_searchers: lambda *_row: passed)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-catalogue-unread"]
    assert "Discogs was not asked about 1 row(s), 60" in warning["message"]
    assert "could not be read" not in warning["message"]


def test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them(
    machine, silence, monkeypatch
):
    """U322, sitting 102: Beatport refusing every row is fetched three times and counted."""
    from cratekit.core import tags
    from cratekit.tagging import published, searchers
    from tests.test_beatport_refusal import (
        REFUSED,
        _beatport_requests,
        _discogs_searches,
        _over_the_wire,
    )
    from tests.test_discogs_searcher import SENT

    paths = build(
        machine,
        silence,
        *(Track(str(60 + n), "", "", artist="Nobody", folder="x") for n in range(6)),
    )
    for n, path in enumerate(sorted(paths.values())):
        assert tags.write_tags(path, {"isrc": f"GBAYE00000{n:02d}"})
    general: list[object] = []

    def deezer(isrc):
        general.append(isrc)
        return published.Published(published.SOURCE, "miss")

    monkeypatch.setattr(published, "for_lookup", lambda: deezer)
    seen: list[str] = []
    fetch = _over_the_wire(REFUSED, seen=seen)
    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    search = searchers.catalogue_searcher(
        DECLARED, fetch=fetch, sleep=lambda _s: None, discogs=asker
    )
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope

    assert _discogs_searches(seen) == 6
    assert _beatport_requests(seen) == searchers.REFUSALS_BEFORE_STOP
    counted = envelope["data"]["summary"]["catalogue_answers"]
    assert counted["rows"] == 6 and counted["stopped"] == 0
    assert counted["catalogues"][searchers.DISCOGS] == {
        "asked": 6, "matched": 0, "missed": 6, "unread": 0, "not_asked": 0, "not_sent": 0,
    }  # fmt: skip
    assert counted["catalogues"][searchers.BEATPORT] == {
        "asked": 3, "matched": 0, "missed": 0, "unread": 3, "not_asked": 3, "not_sent": 3,
    }  # fmt: skip
    # The verb asks the general catalogue through the suggest binder, past the
    # refusing Beatport, by each file's ISRC (round one of the review, 5).
    assert sorted(general) == [f"GBAYE00000{n:02d}" for n in range(6)]
    assert counted["catalogues"][published.SOURCE] == {
        "asked": 6, "matched": 0, "missed": 6, "unread": 0, "not_asked": 0, "not_sent": 0,
    }  # fmt: skip
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == "backlog.catalogue"]
    assert check["detail"].startswith(
        "6 row(s) with no genre were weighed with the catalogues: discogs asked about 6, "
        "matched 0, missed 6, could not be read for 0, not asked about 0; beatport asked "
        "about 3, matched 0, missed 0, could not be read for 3, not asked about 3 (3 of "
        "them once it had refused this client)"
    )
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-catalogue-unread"]
    assert "beatport could not be read for 6 row(s) another catalogue answered" in warning["message"]
    assert "the catalogues could not be read" not in warning["message"]


def test_the_catalogue_line_is_absent_without_the_catalogue(machine, silence):
    build(machine, silence, Track("60", "", "", artist="Nobody", folder="x"))
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["catalogue_answers"] is None
    assert "backlog.catalogue" not in [c["key"] for c in envelope["data"]["checks"]]


def test_the_catalogue_line_names_the_rows_the_walk_stopped_before(machine, silence, monkeypatch):
    from cratekit.core.cause import refuse
    from cratekit.tagging import published, searchers

    build(
        machine,
        silence,
        *(Track(str(60 + n), "", "", artist="Nobody", folder="x") for n in range(5)),
    )

    def blocked(artist, title):
        raise refuse("catalogue-unreachable", "blocked", origin=("test",))

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: blocked)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["catalogue_answers"]["stopped"] == 2
    (check,) = [c for c in envelope["data"]["checks"] if c["key"] == "backlog.catalogue"]
    assert check["detail"] == (
        "5 row(s) with no genre were weighed with the catalogues, and no catalogue's "
        "answer is recorded; the walk asked nothing about 2 row(s) once no catalogue "
        "could be read for 3 rows in a row"
    )


def test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row(
    machine, silence, monkeypatch
):
    """U322 review: a refused token no longer stops the walk, and the warning says so."""
    from cratekit.tagging import published, searchers
    from tests.test_beatport_refusal import MISSED, _beatport_requests, _over_the_wire, _Response
    from tests.test_discogs_searcher import SENT

    build(
        machine,
        silence,
        *(Track(str(60 + n), "", "", artist="Nobody", folder="x") for n in range(5)),
    )
    seen: list[str] = []
    fetch = _over_the_wire(MISSED, discogs=_Response(401, "{}", {}), seen=seen)
    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    search = searchers.catalogue_searcher(
        DECLARED, fetch=fetch, sleep=lambda _s: None, discogs=asker
    )
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    code, envelope = drive([*VERB, "--catalogue"])
    assert code == int(ExitCode.OK), envelope
    assert _beatport_requests(seen) == 5
    assert envelope["data"]["summary"]["catalogue_answers"]["stopped"] == 0
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "backlog-catalogue-unread"]
    assert warning["message"].startswith(
        "Discogs was not read for 5 row(s), 60, 61, 62, 63, 64, because the recorded "
        "Discogs token could not be used, so those were weighed without it"
    )
