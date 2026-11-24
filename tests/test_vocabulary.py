"""R-799: the general catalogue's words are filed by a table of their own.

The loader, the resolver asking the table first, the chooser and the tagger.
EVERY EXPECTED VALUE IS A LITERAL. Nothing here reaches a network.
"""

from __future__ import annotations

import copy
import tomllib
from importlib import resources

import pytest

from cratekit.core import routing, taxonomy
from cratekit.core.routing import Decline, Match
from cratekit.core.taxonomy import TaxonomyError, build_taxonomy, default_taxonomy
from cratekit.tagging import cyanite, published, searchers
from cratekit.tagging.searchers import Fetched
from cratekit.tagging.tag import SearchHit, SourceAnswer
from tests.test_catalogue_searcher import _all_three, _beatport_page, _beatport_track

TAXONOMY = default_taxonomy()

#: The name a file's record gives the general catalogue, typed. The table in
#: the template is keyed by it, and a rename of one without the other is the
#: failure this literal exists to catch.
CATALOGUE = "deezer"

#: The shipped rows: the catalogue's word, the genre written, and the place
#: that genre files in. Written out from the card's list.
SHIPPED = {
    "Pop": ("NonElectronic / Pop", "non_electronic", "pop"),
    "Alternative": ("Rock", "non_electronic", "rock"),
    "Rock": ("Rock", "non_electronic", "rock"),
    "Country": ("Folk", "non_electronic", "folk"),
    "Folk": ("Folk", "non_electronic", "folk"),
    "R&B": ("R&B", "rnb", None),
    "Soul & Funk": ("Soul", "soul", None),
    "Rap/Hip Hop": ("Hip-Hop", "hip_hop", None),
    "Jazz": ("Jazz", "jazz", None),
    "Classical": ("Classical", "non_electronic", "classical"),
    "Reggae": ("Caribbean", "non_electronic", "caribbean"),
}

#: The catalogue's other top level words, measured 2026-10-01. None has a row.
NO_ROW = [
    "Electro", "Dance", "Reggaeton", "Christian", "Salsa", "Traditional Mexicano",
    "Films/Games", "Metal", "African Music", "Asian Music", "Blues",
    "Brazilian Music", "Cumbia", "Indian Music", "Kids", "Latin Music",
]  # fmt: skip


@pytest.fixture(scope="module")
def default_raw() -> dict:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    return tomllib.loads(source.read_text(encoding="utf-8"))


def built(raw: dict, mutate):
    data = copy.deepcopy(raw)
    mutate(data)
    return build_taxonomy(data)


def problems_from(raw: dict, mutate) -> tuple[str, ...]:
    with pytest.raises(TaxonomyError) as caught:
        built(raw, mutate)
    return caught.value.problems


def named(raw: dict, mutate, *words: str) -> bool:
    """Whether one problem the mutated template loads with names every one of ``words``."""
    return any(all(word in p for word in words) for p in problems_from(raw, mutate))


def rows_of(data: dict) -> list:
    return data["vocabulary"][CATALOGUE]["words"]


def appended(*rows):
    """A mutation adding ``rows`` to the catalogue's table."""
    return lambda data: rows_of(data).extend(rows)


def vocabulary(value, source: str | None = None):
    """A mutation setting the vocabulary section, or one source's table in it, to ``value``."""

    def mutate(data):
        if source is None:
            data["vocabulary"] = value
        else:
            data["vocabulary"][source] = value

    return mutate


def emptied(data) -> None:
    """The catalogue's table declared with no rows."""
    data["vocabulary"][CATALOGUE]["words"] = []


def filed(taxonomy, genre: str) -> tuple[str, str | None, Match]:
    """Where routing files a file carrying this genre, with no energy reading."""
    landed = routing.resolve_bucket(taxonomy, genre)
    sub = routing.energy_sub(taxonomy, landed.bucket_id, None, source_genre=genre)
    return landed.bucket_id, sub.id if sub is not None else None, landed.match


# ── the shipped table ──────────────────────────────────────────────────────


def test_the_shipped_template_declares_the_catalogues_table_and_the_cards_rows():
    """Two tables since U244; Discogs' rows are ``tests/test_discogs_searcher.py``'s."""
    assert {one.source for one in TAXONOMY.vocabularies} == {CATALOGUE, searchers.DISCOGS}
    (table,) = [one for one in TAXONOMY.vocabularies if one.source == CATALOGUE]
    assert {row.word: (row.tag, row.bucket, row.sub) for row in table.words} == SHIPPED
    assert len(table.words) == len(SHIPPED)


@pytest.mark.parametrize("word", sorted(SHIPPED))
def test_every_shipped_tag_is_filed_where_its_row_says_by_an_exact_declaration(word):
    tag, bucket, sub = SHIPPED[word]
    landed_bucket, landed_sub, match = filed(TAXONOMY, tag)
    assert landed_bucket == bucket
    assert match in (Match.EXACT, Match.PASSTHROUGH)
    if sub is not None:
        assert landed_sub == sub
    else:
        # A bucket that splits by energy: the band is the reading's to choose,
        # and a file with a reading lands in one.
        band = routing.energy_sub(TAXONOMY, bucket, 5, source_genre=tag)
        assert band is not None and band.id in {b.id for b in TAXONOMY.energy.bands}


def test_no_shipped_tag_is_the_bare_name_of_a_bucket_that_files_by_source():
    by_source = {b.display for b in TAXONOMY.buckets if b.sub_by_source is not None}
    assert by_source == {"NonElectronic"}
    assert not by_source & {tag for tag, _bucket, _sub in SHIPPED.values()}


def test_the_word_for_the_pop_sub_is_not_the_subs_name_which_routes_to_the_dance_bucket():
    """The dance bucket's alias files Pop, so the sub's name files elsewhere."""
    assert filed(TAXONOMY, "Pop")[0] == "dance_pop"
    assert filed(TAXONOMY, "NonElectronic / Pop")[:2] == ("non_electronic", "pop")


# ── the resolver ───────────────────────────────────────────────────────────


@pytest.mark.parametrize("word", sorted(SHIPPED))
def test_a_word_of_the_catalogues_is_answered_from_its_own_table(word):
    tag, bucket, sub = SHIPPED[word]
    answer = routing.suggest_tag(TAXONOMY, word, source=CATALOGUE)
    assert (answer.tag, answer.bucket_id, answer.sub_id) == (tag, bucket, sub)
    assert not answer.declined and not answer.off_taxonomy and not answer.needs_review


@pytest.mark.parametrize("spelled", ["pop", "POP", "  Pop  ", "pOp"])
def test_a_word_is_matched_whole_whatever_its_case(spelled):
    assert routing.suggest_tag(TAXONOMY, spelled, source=CATALOGUE).tag == "NonElectronic / Pop"


@pytest.mark.parametrize("word", NO_ROW)
def test_a_top_level_word_with_no_row_is_declined_and_never_written(word):
    """Electro and Dance stay declined, and so does every word no folder names."""
    assert published.choose(TAXONOMY, [word]) is None


@pytest.mark.parametrize(
    ("word", "written"),
    [("Disco", "House / Funky House / Disco"), ("Trance", "Trance"), ("Deep House", "Deep House")],
)
def test_a_word_with_no_row_goes_on_to_the_aliases_and_is_written_when_it_names_a_folder(
    word, written
):
    """The table is asked first, and a word the aliases file correctly is still written."""
    assert TAXONOMY.vocabulary(CATALOGUE).get(word.lower()) is None
    answer = routing.suggest_tag(TAXONOMY, word, source=CATALOGUE)
    assert answer == routing.suggest_tag(TAXONOMY, word)
    assert published.choose(TAXONOMY, [word]) == (word, written)
    assert TAXONOMY.named_folder(written) is not None


def test_a_dance_word_the_aliases_file_is_not_passed_over_for_a_broad_word_with_a_row():
    """Declining every rowless word made an Electro, Disco and Pop album a pop record."""
    chosen = published.choose(TAXONOMY, ["Electro", "Disco", "Pop"])
    assert chosen == ("Disco", "House / Funky House / Disco")


@pytest.mark.parametrize("word", ["Indie Rock", "Punk", "Latin", "World Music", "Bollywood"])
def test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined(word, no_table):
    """R-799's second fault: a bare bucket name is never written once the table is declared."""
    assert routing.suggest_tag(TAXONOMY, word, source=CATALOGUE).tag == "NonElectronic"
    assert published.choose(no_table, [word]) == (word, "NonElectronic")
    assert published.choose(TAXONOMY, [word]) is None
    assert published.choose(TAXONOMY, [word, "Rock"]) == ("Rock", "Rock")


def test_the_guard_is_taken_with_the_table_and_not_with_its_rows(default_raw):
    """A table with no rows still says a written genre names a folder."""
    empty = built(default_raw, emptied)
    assert published.choose(empty, ["Indie Rock"]) is None
    assert published.choose(empty, ["Alternative"]) is None
    assert published.choose(empty, ["Rock"]) == ("Rock", "Rock")
    assert published.choose(empty, ["Pop"]) == ("Pop", "Dance / Pop")


def test_part_of_a_word_is_not_the_word():
    """A row is matched whole. Neither of these reaches the row for Pop or Rock."""
    pop_rock = routing.suggest_tag(TAXONOMY, "Pop Rock", source=CATALOGUE)
    assert pop_rock == routing.suggest_tag(TAXONOMY, "Pop Rock")
    assert pop_rock.tag == "Pop Rock"
    assert routing.suggest_tag(TAXONOMY, "Ro", source=CATALOGUE).tag == "Ro"


def test_an_empty_word_is_declined_before_any_table_is_read():
    assert routing.suggest_tag(TAXONOMY, "  ", source=CATALOGUE).decline is Decline.NOT_FOUND
    assert routing.suggest_tag(TAXONOMY, None, source=CATALOGUE).decline is Decline.NOT_FOUND


@pytest.mark.parametrize("source", [None, searchers.BEATPORT, searchers.TRAXSOURCE, "bandcamp"])
def test_a_record_shops_pop_goes_where_it_went_before(source):
    """The shops have no table, and a caller naming no source is theirs."""
    answer = routing.suggest_tag(TAXONOMY, "Pop", source=source)
    assert (answer.tag, answer.bucket_id, answer.sub_id) == ("Dance / Pop", "dance_pop", None)


def test_the_record_shops_searcher_names_no_source_to_the_resolver():
    """Driven: Beatport's Pop through the shipped searcher is the dance bucket's name."""
    page = _beatport_page([_beatport_track("an artist", "a title", "Pop")])
    refused = Fetched(note="HTTP 403", status=403)
    fetch = _all_three(beatport=page, traxsource=refused, bandcamp=refused)
    search = searchers.catalogue_searcher(TAXONOMY, fetch=fetch, sleep=lambda _seconds: None)
    hit = search("an artist", "a title")
    assert (hit.genre, hit.source, hit.source_genre) == ("Dance / Pop", searchers.BEATPORT, "Pop")


# ── the chooser and the tagger's seam ──────────────────────────────────────


def test_the_catalogues_pop_is_written_as_a_word_that_files_under_the_pop_sub():
    chosen = published.choose(TAXONOMY, ["Pop"])
    assert chosen == ("Pop", "NonElectronic / Pop")
    assert filed(TAXONOMY, chosen[1])[:2] == ("non_electronic", "pop")


def test_the_catalogues_alternative_files_under_rock_and_the_genre_written_names_rock():
    chosen = published.choose(TAXONOMY, ["Alternative"])
    assert chosen == ("Alternative", "Rock")
    assert filed(TAXONOMY, chosen[1])[:2] == ("non_electronic", "rock")


def test_the_first_word_with_a_row_is_chosen_in_the_catalogues_order():
    chosen = published.choose(TAXONOMY, ["Electro", "Christian", "Country", "Pop"])
    assert chosen == ("Country", "Folk")


MISSED = (
    SourceAnswer(searchers.BEATPORT, "miss"),
    SourceAnswer(searchers.TRAXSOURCE, "blocked"),
    SourceAnswer(searchers.BANDCAMP, "blocked"),
)
ISRC = "USRC17607839"


def said(*genres: str):
    def lookup(_isrc: object) -> published.Published:
        return published.Published(CATALOGUE, "matched", genres=tuple(genres))

    return lookup


def test_the_seam_hands_the_tagger_the_word_that_files_and_records_the_catalogues():
    hit = SearchHit(answers=MISSED, unread=(searchers.TRAXSOURCE, searchers.BANDCAMP))
    out = published.second_opinion(TAXONOMY, lookup=said("Pop"))(hit, ISRC)
    assert (out.genre, out.source, out.source_genre) == ("NonElectronic / Pop", CATALOGUE, "Pop")
    assert out.off_taxonomy is False
    assert out.answers[-1] == SourceAnswer(CATALOGUE, "matched", "Pop")


def test_a_word_with_no_row_is_declined_and_the_record_says_what_was_answered():
    hit = SearchHit(answers=MISSED, unread=(searchers.TRAXSOURCE, searchers.BANDCAMP))
    out = published.second_opinion(TAXONOMY, lookup=said("Christian"))(hit, ISRC)
    assert out.genre is None
    assert (out.source, out.source_genre) == (CATALOGUE, "Christian")
    assert out.answers[-1] == SourceAnswer(CATALOGUE, "matched", "Christian")


# ── a taxonomy with no table, and one with an empty one ────────────────────


#: What the shared resolver chose for the catalogue's words before this unit,
#: measured on the shipped template on 2026-10-02 and written out. A copy with
#: no table must go on answering exactly this, less the one word U118 moved:
#: "Soul & Funk" files under its first word, Soul, by the author's decision.
BEFORE = {
    "Pop": "Dance / Pop",
    "Alternative": "NonElectronic",
    "Country": "NonElectronic",
    "Rock": "Rock",
    "Folk": "Folk",
    "R&B": "R&B",
    "Soul & Funk": "Soul",
    "Rap/Hip Hop": "Hip-Hop",
    "Jazz": "Jazz",
    "Classical": "Classical",
    "Reggae": "Caribbean",
    "Electro": None,
    "Dance": None,
    "Christian": None,
}


@pytest.fixture(scope="module")
def no_table(default_raw):
    return built(default_raw, lambda data: data.pop("vocabulary"))


def test_a_taxonomy_with_no_table_declares_none(no_table):
    assert no_table.vocabularies == ()
    assert no_table.vocabulary(CATALOGUE) is None


@pytest.mark.parametrize("word", sorted(BEFORE))
def test_a_taxonomy_with_no_table_behaves_as_it_did(no_table, word):
    chosen = published.choose(no_table, [word])
    assert (chosen[1] if chosen else None) == BEFORE[word]
    with_source = routing.suggest_tag(no_table, word, source=CATALOGUE)
    assert with_source == routing.suggest_tag(no_table, word)


def test_a_table_is_read_only_for_the_source_it_names():
    assert routing.suggest_tag(TAXONOMY, "Pop", source="another_catalogue").tag == "Dance / Pop"


def test_a_table_with_no_rows_is_a_declaration_and_answers_for_no_word(default_raw):
    empty = built(default_raw, emptied)
    assert empty.vocabulary(CATALOGUE) == {}
    assert empty.vocabularies[0].words == ()


def test_an_empty_vocabulary_section_declares_no_table(default_raw):
    assert built(default_raw, vocabulary({})).vocabulary(CATALOGUE) is None


# ── the loader ─────────────────────────────────────────────────────────────


def test_a_vocabulary_that_is_not_a_table_of_sources_is_a_named_problem(default_raw):
    mutate = vocabulary([{"word": "Pop", "tag": "Rock"}])
    assert named(default_raw, mutate, "[vocabulary] must be a table of sources")


@pytest.mark.parametrize("table", [{}, {"words": {"word": "Pop", "tag": "Rock"}}, "Rock", []])
def test_a_source_whose_words_are_not_a_list_is_a_named_problem(default_raw, table):
    mutate = vocabulary(table, CATALOGUE)
    assert named(default_raw, mutate, f"[vocabulary.{CATALOGUE}]", "needs words, a list of rows")


@pytest.mark.parametrize("name", ["Deezer", "general catalogue", "9lives", ""])
def test_a_source_name_that_no_record_could_carry_is_refused(default_raw, name):
    assert named(default_raw, vocabulary({"words": []}, name), "the source name must match")


@pytest.mark.parametrize("name", ["dezer", "beatport", "traxsource", "bandcamp"])
def test_a_table_nothing_would_read_is_refused_and_not_ignored(default_raw, name):
    """A misspelled source and a shop's would each load clean and change nothing."""
    mutate = vocabulary({"words": [{"word": "Pop", "tag": "Rock"}]}, name)
    words = (f"[vocabulary.{name}]", "it would change nothing", "deezer")
    assert named(default_raw, mutate, *words)


def test_the_sources_the_loader_knows_are_the_ones_the_tagger_reads_a_table_for():
    """The loader cannot import tagging, so its tuple is pinned to the chooser's (U244, U245)."""
    assert taxonomy.VOCABULARY_SOURCES == (published.SOURCE, searchers.DISCOGS, cyanite.CYANITE)
    assert published.SOURCE == CATALOGUE
    assert not set(taxonomy.VOCABULARY_SOURCES) & set(searchers.SCRAPED_WALK)


# ── one rule for a folder's name, held to routing's own answer ─────────────


def _declared_strings() -> list[str]:
    """Every string the template declares anywhere a genre can be named."""
    found: set[str] = set(TAXONOMY.fallback.too_coarse_as_source)
    for bucket in TAXONOMY.buckets:
        found.add(bucket.display)
        found.update(bucket.aliases)
        found.update(bucket.tag_aliases)
        for sub in bucket.subs:
            found.add(sub.display)
            found.update(sub.tag_aliases)
        if bucket.sub_by_source is not None:
            found.update(bucket.sub_by_source.map)
    found.update(rule.keyword for rule in TAXONOMY.fuzzy)
    found.update(row.tag for table in TAXONOMY.vocabularies for row in table.words)
    return sorted(found | {"a word nothing declares", "Indie Pop"})


@pytest.mark.parametrize("genre", _declared_strings())
def test_a_named_folder_is_where_routing_files_the_genre(genre):
    """The loader's spelling of routing's two exact tiers, held to routing over every string."""
    place = TAXONOMY.named_folder(genre)
    landed_bucket, landed_sub, match = filed(TAXONOMY, genre)
    if place is None:
        bucket = TAXONOMY.bucket(landed_bucket)
        assert (
            match in (Match.FUZZY, Match.FALLBACK)
            or TAXONOMY.is_too_coarse_as_source(genre)
            or (bucket.sub_by_source is not None and genre not in bucket.sub_by_source.map)
        ), f"{genre!r} is filed exactly under {landed_bucket} and no folder is named"
        return
    assert match in (Match.EXACT, Match.PASSTHROUGH)
    assert place[0] == landed_bucket
    if place[1] is not None:
        assert place[1] == landed_sub
    else:
        assert TAXONOMY.bucket(landed_bucket).sub_by_source is None


def test_the_named_folder_population_is_not_empty_on_either_side():
    """Floors from 2026-10-02's 77 and 77, so the walk above cannot collapse to one side."""
    answers = [TAXONOMY.named_folder(genre) for genre in _declared_strings()]
    assert sum(place is not None for place in answers) >= 70
    assert sum(place is None for place in answers) >= 70


def test_a_row_that_is_not_a_table_is_refused(default_raw):
    assert named(default_raw, appended("Pop"), "is not a table")


@pytest.mark.parametrize("row", [{"tag": "Rock"}, {"word": "  ", "tag": "Rock"}, {"word": 7}])
def test_a_row_with_no_word_is_refused(default_raw, row):
    assert named(default_raw, appended(row), "needs a word")


@pytest.mark.parametrize("row", [{"word": "Metal"}, {"word": "Metal", "tag": ""}])
def test_a_row_with_no_tag_is_refused_and_names_its_word(default_raw, row):
    assert named(default_raw, appended(row), "'Metal'", "needs a tag")


@pytest.mark.parametrize("again", ["Pop", "pop", " POP "])
def test_a_word_declared_twice_is_refused_whatever_its_case(default_raw, again):
    assert named(default_raw, appended({"word": again, "tag": "Rock"}), "declared twice")


@pytest.mark.parametrize(
    "tag",
    [
        "Indie Pop",  # a keyword rule would catch it, and a keyword is a guess
        "Metal",  # nothing claims it, and it would fall to the fallback
        "rock",  # an alias in another case is not that alias
        "Hip-Hop ",  # checked as written to the file, which is stripped
    ],
)
def test_a_tag_nothing_files_by_an_exact_declaration_is_refused(default_raw, tag):
    mutate = appended({"word": "Metal", "tag": tag})
    if tag == "Hip-Hop ":
        assert built(default_raw, mutate).vocabulary(CATALOGUE)["metal"].tag == "Hip-Hop"
        return
    assert routing.resolve_bucket(TAXONOMY, tag).match in (Match.FUZZY, Match.FALLBACK)
    assert named(default_raw, mutate, "'Metal'", "is filed by no exact declaration")


@pytest.mark.parametrize("tag", ["Electronica", "Electronic", "Electronica / Other"])
def test_a_tag_the_taxonomy_calls_too_coarse_is_refused(default_raw, tag):
    assert TAXONOMY.is_too_coarse_as_source(tag)
    mutate = appended({"word": "Electro", "tag": tag})
    assert named(default_raw, mutate, "too coarse to be a final genre")


def test_the_bare_name_of_a_bucket_that_files_by_source_is_refused(default_raw):
    """R-799: Alternative as the bucket's name filed in the default sub, the word lost."""
    assert filed(TAXONOMY, "NonElectronic")[:2] == ("non_electronic", "rock")
    mutate = appended({"word": "Metal", "tag": "NonElectronic"})
    assert named(default_raw, mutate, "with no row of its own", "default sub 'rock'")


def test_an_alias_of_such_a_bucket_with_no_row_in_its_map_is_refused(default_raw):
    def mutate(data):
        bucket = next(b for b in data["bucket"] if b["id"] == "non_electronic")
        bucket["aliases"].append("Shoegaze")
        rows_of(data).append({"word": "Metal", "tag": "Shoegaze"})

    assert named(default_raw, mutate, "'Shoegaze'", "with no row of its own")


def test_the_same_alias_with_a_row_in_the_map_is_accepted(default_raw):
    def mutate(data):
        bucket = next(b for b in data["bucket"] if b["id"] == "non_electronic")
        bucket["aliases"].append("Shoegaze")
        bucket["sub_by_source"]["map"].append({"source": "Shoegaze", "sub": "rock"})
        rows_of(data).append({"word": "Metal", "tag": "Shoegaze"})

    row = built(default_raw, mutate).vocabulary(CATALOGUE)["metal"]
    assert (row.tag, row.bucket, row.sub) == ("Shoegaze", "non_electronic", "rock")


def test_every_problem_in_a_table_is_reported_at_once(default_raw):
    mutate = appended(
        {"word": "Metal", "tag": "NonElectronic"}, {"word": "Blues"}, {"word": "pop", "tag": "Rock"}
    )
    problems = problems_from(default_raw, mutate)
    assert sum("[vocabulary.deezer]" in p for p in problems) == 3


def test_a_template_at_schema_version_1_may_declare_a_vocabulary(default_raw):
    """No schema version moves; an older build ignores the table."""

    def mutate(data):
        data["schema_version"] = 1
        for bucket in data["bucket"]:
            bucket.pop("formerly", None)
            bucket.pop("split_from", None)
        # And the one class that needs version 4 (U119), for the same reason.
        data["sub_class"] = [c for c in data["sub_class"] if c.get("signal") != "playlist"]
        # And the genre sub, which needs version 5 (U155).
        for bucket in data["bucket"]:
            bucket.pop("genre_sub", None)

    assert built(default_raw, mutate).vocabulary(CATALOGUE)["pop"].tag == "NonElectronic / Pop"
