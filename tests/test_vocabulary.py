"""R-799: the general catalogue's words are filed by a table of their own.

The alias lists on the buckets were written against the record shops' words,
where Pop is a dance genre. Read through them the general catalogue's Pop was
written as the dance bucket's name on 10 of the author's tracks, and its
Alternative as a bucket's bare name on 6. These tests drive the table the
taxonomy now declares per source: the loader that refuses a row whose tag
names no folder, the resolver that asks the table first, the chooser that
writes a word of the buckets' aliases only when it names a folder, and the
tagger writing the word that files.

EVERY EXPECTED VALUE IS A LITERAL. The shipped rows are written out here and
never read off the template under test, and the places are pinned by
identifier and then driven through routing, so a row that drifts fails.

NOTHING HERE REACHES A NETWORK. The general catalogue is a callable over a
literal answer.
"""

from __future__ import annotations

import copy
import tomllib
from importlib import resources

import pytest

from cratekit.core import routing, taxonomy
from cratekit.core.routing import Decline, Match
from cratekit.core.taxonomy import TaxonomyError, build_taxonomy, default_taxonomy
from cratekit.tagging import published, searchers
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


def rows_of(data: dict) -> list:
    return data["vocabulary"][CATALOGUE]["words"]


def filed(taxonomy, genre: str) -> tuple[str, str | None, Match]:
    """Where routing files a file carrying this genre, with no energy reading."""
    landed = routing.resolve_bucket(taxonomy, genre)
    sub = routing.energy_sub(taxonomy, landed.bucket_id, None, source_genre=genre)
    return landed.bucket_id, sub.id if sub is not None else None, landed.match


# ── the shipped table ──────────────────────────────────────────────────────


def test_the_shipped_template_declares_one_table_and_the_cards_rows():
    (table,) = TAXONOMY.vocabularies
    assert table.source == CATALOGUE
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
    """Why the row writes a word of its own. A file whose genre is Pop is
    filed in the dance bucket by that bucket's alias, so the sub's name is not
    a word that files under it."""
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
    [
        ("Disco", "House / Funky House / Disco"),
        ("Trance", "Trance"),
        ("Deep House", "Deep House"),
    ],
)
def test_a_word_with_no_row_goes_on_to_the_aliases_and_is_written_when_it_names_a_folder(
    word, written
):
    """The table is asked first and is not the whole answer. A specific word
    the aliases already file correctly is still written."""
    assert TAXONOMY.vocabulary(CATALOGUE).get(word.lower()) is None
    assert routing.suggest_tag(TAXONOMY, word, source=CATALOGUE) == routing.suggest_tag(
        TAXONOMY, word
    )
    assert published.choose(TAXONOMY, [word]) == (word, written)
    assert TAXONOMY.named_folder(written) is not None


def test_a_dance_word_the_aliases_file_is_not_passed_over_for_a_broad_word_with_a_row():
    """What the review drove. Declining every word with no row made an album
    listing Electro, Disco and Pop a pop record, where the aliases had filed
    it under the disco bucket."""
    assert published.choose(TAXONOMY, ["Electro", "Disco", "Pop"]) == (
        "Disco",
        "House / Funky House / Disco",
    )


@pytest.mark.parametrize("word", ["Indie Rock", "Punk", "Latin", "World Music", "Bollywood"])
def test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined(word, no_table):
    """R-799's second fault, for the words with no row. The aliases answer each
    with the non electronic bucket's own name, which a copy with no table
    wrote, and a copy that declares the table never does."""
    assert routing.suggest_tag(TAXONOMY, word, source=CATALOGUE).tag == "NonElectronic"
    assert published.choose(no_table, [word]) == (word, "NonElectronic")
    assert published.choose(TAXONOMY, [word]) is None
    assert published.choose(TAXONOMY, [word, "Rock"]) == ("Rock", "Rock")


def test_the_guard_is_taken_with_the_table_and_not_with_its_rows(default_raw):
    """A table with no rows still says a written genre names a folder."""

    def mutate(data):
        data["vocabulary"][CATALOGUE]["words"] = []

    empty = built(default_raw, mutate)
    assert published.choose(empty, ["Indie Rock"]) is None
    assert published.choose(empty, ["Alternative"]) is None
    assert published.choose(empty, ["Rock"]) == ("Rock", "Rock")
    assert published.choose(empty, ["Pop"]) == ("Pop", "Dance / Pop")


def test_part_of_a_word_is_not_the_word():
    """A row is matched whole. Neither of these reaches the row for Pop or Rock."""
    assert routing.suggest_tag(TAXONOMY, "Pop Rock", source=CATALOGUE) == routing.suggest_tag(
        TAXONOMY, "Pop Rock"
    )
    assert routing.suggest_tag(TAXONOMY, "Pop Rock", source=CATALOGUE).tag == "Pop Rock"
    assert routing.suggest_tag(TAXONOMY, "Ro", source=CATALOGUE).tag == "Ro"


def test_an_empty_word_is_declined_before_any_table_is_read():
    assert routing.suggest_tag(TAXONOMY, "  ", source=CATALOGUE).decline is Decline.NOT_FOUND
    assert routing.suggest_tag(TAXONOMY, None, source=CATALOGUE).decline is Decline.NOT_FOUND


@pytest.mark.parametrize("source", [None, searchers.BEATPORT, searchers.TRAXSOURCE, "bandcamp"])
def test_a_record_shops_pop_goes_where_it_went_before(source):
    """The pin the card asks for. The record shops have no table, and a caller
    that names no source is the shops' own caller."""
    answer = routing.suggest_tag(TAXONOMY, "Pop", source=source)
    assert (answer.tag, answer.bucket_id, answer.sub_id) == ("Dance / Pop", "dance_pop", None)


def test_the_record_shops_searcher_names_no_source_to_the_resolver():
    """Driven, not read: Beatport's Pop through the shipped searcher is the
    dance bucket's name, on the template that declares the catalogue's table."""
    page = _beatport_page([_beatport_track("an artist", "a title", "Pop")])
    refused = Fetched(note="HTTP 403", status=403)
    search = searchers.catalogue_searcher(
        TAXONOMY,
        fetch=_all_three(beatport=page, traxsource=refused, bandcamp=refused),
        sleep=lambda _seconds: None,
    )
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
    assert published.choose(TAXONOMY, ["Electro", "Christian", "Country", "Pop"]) == (
        "Country",
        "Folk",
    )


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
    def mutate(data):
        data["vocabulary"][CATALOGUE]["words"] = []

    empty = built(default_raw, mutate)
    assert empty.vocabulary(CATALOGUE) == {}
    assert empty.vocabularies[0].words == ()


def test_an_empty_vocabulary_section_declares_no_table(default_raw):
    def mutate(data):
        data["vocabulary"] = {}

    assert built(default_raw, mutate).vocabulary(CATALOGUE) is None


# ── the loader ─────────────────────────────────────────────────────────────


def test_a_vocabulary_that_is_not_a_table_of_sources_is_a_named_problem(default_raw):
    def mutate(data):
        data["vocabulary"] = [{"word": "Pop", "tag": "Rock"}]

    assert any(
        "[vocabulary] must be a table of sources" in p for p in problems_from(default_raw, mutate)
    )


@pytest.mark.parametrize("table", [{}, {"words": {"word": "Pop", "tag": "Rock"}}, "Rock", []])
def test_a_source_whose_words_are_not_a_list_is_a_named_problem(default_raw, table):
    def mutate(data):
        data["vocabulary"][CATALOGUE] = table

    assert any(
        f"[vocabulary.{CATALOGUE}]" in p and "needs words, a list of rows" in p
        for p in problems_from(default_raw, mutate)
    )


@pytest.mark.parametrize("name", ["Deezer", "general catalogue", "9lives", ""])
def test_a_source_name_that_no_record_could_carry_is_refused(default_raw, name):
    def mutate(data):
        data["vocabulary"][name] = {"words": []}

    assert any("the source name must match" in p for p in problems_from(default_raw, mutate))


@pytest.mark.parametrize("name", ["dezer", "beatport", "traxsource", "bandcamp"])
def test_a_table_nothing_would_read_is_refused_and_not_ignored(default_raw, name):
    """A misspelled name and a record shop's. Each would load clean and change
    nothing, and the review found nothing said so."""

    def mutate(data):
        data["vocabulary"][name] = {"words": [{"word": "Pop", "tag": "Rock"}]}

    assert any(
        f"[vocabulary.{name}]" in p and "it would change nothing" in p and "deezer" in p
        for p in problems_from(default_raw, mutate)
    )


def test_the_sources_the_loader_knows_are_the_ones_the_tagger_reads_a_table_for():
    """The loader cannot import the tagging package, so its tuple is pinned to
    the name the chooser passes the resolver."""
    assert taxonomy.VOCABULARY_SOURCES == (published.SOURCE,)
    assert published.SOURCE == CATALOGUE
    assert not set(taxonomy.VOCABULARY_SOURCES) & set(searchers.SOURCES)


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
    """The loader spells routing's two exact tiers for itself. This holds the
    spelling to routing over every string the template declares: whenever a
    folder is named, routing files the genre there by an exact declaration."""
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
    """Measured on the shipped template on 2026-10-02: 154 strings, 77 naming a
    folder and 77 not. Floors, so the test above cannot pass over a walk that
    collapsed to one side."""
    answers = [TAXONOMY.named_folder(genre) for genre in _declared_strings()]
    assert sum(place is not None for place in answers) >= 70
    assert sum(place is None for place in answers) >= 70


def test_a_row_that_is_not_a_table_is_refused(default_raw):
    def mutate(data):
        rows_of(data).append("Pop")

    assert any("is not a table" in p for p in problems_from(default_raw, mutate))


@pytest.mark.parametrize("row", [{"tag": "Rock"}, {"word": "  ", "tag": "Rock"}, {"word": 7}])
def test_a_row_with_no_word_is_refused(default_raw, row):
    def mutate(data):
        rows_of(data).append(row)

    assert any("needs a word" in p for p in problems_from(default_raw, mutate))


@pytest.mark.parametrize("row", [{"word": "Metal"}, {"word": "Metal", "tag": ""}])
def test_a_row_with_no_tag_is_refused_and_names_its_word(default_raw, row):
    def mutate(data):
        rows_of(data).append(row)

    assert any("'Metal'" in p and "needs a tag" in p for p in problems_from(default_raw, mutate))


@pytest.mark.parametrize("again", ["Pop", "pop", " POP "])
def test_a_word_declared_twice_is_refused_whatever_its_case(default_raw, again):
    def mutate(data):
        rows_of(data).append({"word": again, "tag": "Rock"})

    assert any("declared twice" in p for p in problems_from(default_raw, mutate))


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
    def mutate(data):
        rows_of(data).append({"word": "Metal", "tag": tag})

    if tag == "Hip-Hop ":
        assert built(default_raw, mutate).vocabulary(CATALOGUE)["metal"].tag == "Hip-Hop"
        return
    assert routing.resolve_bucket(TAXONOMY, tag).match in (Match.FUZZY, Match.FALLBACK)
    assert any(
        "'Metal'" in p and "is filed by no exact declaration" in p
        for p in problems_from(default_raw, mutate)
    )


@pytest.mark.parametrize("tag", ["Electronica", "Electronic", "Electronica / Other"])
def test_a_tag_the_taxonomy_calls_too_coarse_is_refused(default_raw, tag):
    def mutate(data):
        rows_of(data).append({"word": "Electro", "tag": tag})

    assert TAXONOMY.is_too_coarse_as_source(tag)
    assert any("too coarse to be a final genre" in p for p in problems_from(default_raw, mutate))


def test_the_bare_name_of_a_bucket_that_files_by_source_is_refused(default_raw):
    """R-799's second measured fault: Alternative written as the bucket's name,
    filed in the default sub with the word lost."""

    def mutate(data):
        rows_of(data).append({"word": "Metal", "tag": "NonElectronic"})

    assert filed(TAXONOMY, "NonElectronic")[:2] == ("non_electronic", "rock")
    assert any(
        "with no row of its own" in p and "default sub 'rock'" in p
        for p in problems_from(default_raw, mutate)
    )


def test_an_alias_of_such_a_bucket_with_no_row_in_its_map_is_refused(default_raw):
    def mutate(data):
        bucket = next(b for b in data["bucket"] if b["id"] == "non_electronic")
        bucket["aliases"].append("Shoegaze")
        rows_of(data).append({"word": "Metal", "tag": "Shoegaze"})

    assert any(
        "'Shoegaze'" in p and "with no row of its own" in p
        for p in problems_from(default_raw, mutate)
    )


def test_the_same_alias_with_a_row_in_the_map_is_accepted(default_raw):
    def mutate(data):
        bucket = next(b for b in data["bucket"] if b["id"] == "non_electronic")
        bucket["aliases"].append("Shoegaze")
        bucket["sub_by_source"]["map"].append({"source": "Shoegaze", "sub": "rock"})
        rows_of(data).append({"word": "Metal", "tag": "Shoegaze"})

    row = built(default_raw, mutate).vocabulary(CATALOGUE)["metal"]
    assert (row.tag, row.bucket, row.sub) == ("Shoegaze", "non_electronic", "rock")


def test_every_problem_in_a_table_is_reported_at_once(default_raw):
    def mutate(data):
        rows_of(data).extend(
            [
                {"word": "Metal", "tag": "NonElectronic"},
                {"word": "Blues"},
                {"word": "pop", "tag": "Rock"},
            ]
        )

    problems = problems_from(default_raw, mutate)
    assert sum("[vocabulary.deezer]" in p for p in problems) == 3


def test_a_template_at_schema_version_1_may_declare_a_vocabulary(default_raw):
    """No schema version moves for this table. A build older than this unit
    ignores it and files the catalogue's words as it did before."""

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
