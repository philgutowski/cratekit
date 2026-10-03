"""R-798: the label genre gate judges a release by kind, at sweep time.

36 of the 186 tracks downloaded in the label test of 2026-10-01 were not dance
music, among them Christian music from another label with the same name as a
followed one. The gate in ``label approved`` had no genre to read and ran only
after acceptance. These tests drive the gate where a person meets it, through
the real dispatcher, queue and worker, with a fake provider and a fake general
catalogue, and through the rule and the stores where the property is theirs.

NOTHING HERE REACHES A NETWORK. The general catalogue is a callable over a
table in this file, bound where the worker looks its lookup up, and a root
fixture fails any test that reaches the live one.

NOTHING HERE ACCEPTS A RELEASE ON ITS OWN. A sweep files and holds. A download
follows only a decision the author makes in review.

Every expected value is a literal from the fixtures. D1 applies: no real label,
artist or track is named. The genre words are the general catalogue's own
published vocabulary, which is the thing under test.
"""

from __future__ import annotations

import copy
import json
import tomllib
from importlib import resources
from pathlib import Path

import pytest

from cratekit.core import config, jobs, review, routing, tombstone
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import DecisionStore, Queue
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import TaxonomyError, build_taxonomy, default_taxonomy
from cratekit.label import catalogue, sweep
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.label.catalogue import ReleasesUnasked, ReleaseTracks, ReleaseUnresolvable
from cratekit.sync import run
from cratekit.tagging import published
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedArtist, FakeRelease, catalogue_factory
from tests.test_config import valid_data
from tests.test_label_workers import queued_sweep

LABEL = "Tide Works"
SLUG = "tide-works"

#: The general catalogue's 27 top level words, measured 2026-10-01, each with
#: the kind the shipped rules must give it. Written out, never derived from the
#: template, so a rule that drifts fails here.
MEASURED = {
    "Pop": "pop",
    "Rap/Hip Hop": "hip_hop",
    "Reggaeton": "latin",
    "Rock": "rock",
    "Dance": "dance",
    "R&B": "rnb",
    "Alternative": "rock",
    "Christian": "christian",
    "Electro": "dance",
    "Folk": "folk_country",
    "Reggae": "reggae",
    "Jazz": "jazz",
    "Country": "folk_country",
    "Salsa": "latin",
    "Traditional Mexicano": "latin",
    "Classical": "classical",
    "Films/Games": "soundtrack",
    "Metal": "rock",
    "Soul & Funk": "rnb",
    "African Music": "world",
    "Asian Music": "world",
    "Blues": "jazz",
    "Brazilian Music": "latin",
    "Cumbia": "latin",
    "Indian Music": "world",
    "Kids": "kids",
    "Latin Music": "latin",
}

TAXONOMY = default_taxonomy()


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures and fakes
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def installed(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(root)
    data["profile"] = {"name": "full"}
    resolved = config.from_dict(data)
    config.save(resolved)
    config.reset_cache()
    return resolved


def isrc(n: int) -> str:
    """A well formed ISRC nobody was issued."""
    return f"ZZTST26{n:05d}"


class Track:
    """A provider row in the shape the provider reader reads, with an ISRC."""

    def __init__(self, track_id: str, artist: str, name: str, code: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = code


class Lookup:
    """The general catalogue as a table: ISRC to published words, or to an answer.

    A tuple is a match that published those words. A string is the answer
    itself, ``blocked`` or ``unreachable``. An ISRC absent from the table is a
    track the catalogue does not know.
    """

    def __init__(self, table: dict[str, tuple[str, ...] | str]) -> None:
        self.table = dict(table)
        self.asked: list[str] = []

    def __call__(self, value: object) -> published.Published:
        self.asked.append(str(value))
        said = self.table.get(str(value))
        if said is None:
            return published.Published(published.SOURCE, "miss")
        if isinstance(said, str):
            return published.Published(published.SOURCE, said, note=f"the catalogue said {said}")
        return published.Published(published.SOURCE, "matched", genres=said)


def never_asked(value: object) -> published.Published:
    raise AssertionError(f"the general catalogue was asked about {value!r}")


def bind_lookup(monkeypatch, lookup) -> None:
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)


class Provider(FakeCatalogue):
    """A provider that counts how often each release was verified."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verified: list[str] = []

    def search_release(self, claimed, release):
        self.verified.append(str(release.id))
        return super().search_release(claimed, release)


def bind(monkeypatch, releases: dict[str, tuple[str, str]], **kwargs) -> Provider:
    """One label whose releases are ``{id: (year, isrc)}``, one track each."""
    fake = Provider(
        artists={SLUG: FakePagedArtist([FakeRelease(rid, year=year) for rid, (year, _) in releases.items()])},
        releases={
            rid: ([Track(f"t-{rid}", "Label Act", f"Release {rid}", code)], int(year))
            for rid, (year, code) in releases.items()
        },
        **kwargs,
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def register(*argv: str, name: str = LABEL) -> None:
    code, envelope = drive(["label", "registry", "add", name, *argv])
    assert code == int(ExitCode.OK), envelope


def sweep_once() -> str:
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code == int(ExitCode.OK), resumed
    return job_id


def filed(cfg: config.Config) -> dict[str, review.Item]:
    with review.open_store(cfg) as store:
        page = review.list_items(
            store, queue=str(Queue.LABEL_RELEASE), include_resolved=True, limit=None
        )
    return {str(item.payload["identity"]): item for item in page.items}


def held_ids(cfg: config.Config, *, states=(review.HOLD_HELD,)) -> list[str]:
    with review.open_store(cfg) as store:
        found = review.holds(store, queue=str(Queue.LABEL_RELEASE), states=states)
    return [str(one.identity["release_id"]) for one in found]


def grouped(by: str) -> list[dict]:
    code, envelope = drive(["review", "list", "--queue", "label-release", "--group-by", by])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["items"]


def held_verb(*argv: str) -> tuple[int, dict]:
    return drive(["label", "held", *argv])


def check(envelope: dict, key: str) -> dict:
    found = [one for one in envelope["data"]["checks"] if one["key"] == key]
    assert len(found) == 1, (key, [one["key"] for one in envelope["data"]["checks"]])
    return found[0]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The rule: what kind a word is, and what that does to a release
# ═══════════════════════════════════════════════════════════════════════════


def test_every_measured_word_of_the_general_catalogue_is_a_kind():
    assert len(MEASURED) == 27
    assert {word: routing.published_kind(TAXONOMY, word) for word in MEASURED} == MEASURED


@pytest.mark.parametrize("word", sorted(MEASURED))
def test_a_dance_label_passes_the_dance_words_and_holds_every_other(word):
    judged = routing.kind_verdict(TAXONOMY, None, [word])
    expected = KindVerdict.PASS if MEASURED[word] == "dance" else KindVerdict.HOLD
    assert judged.verdict is expected
    assert judged.kind == "dance"
    assert word in judged.reason


def test_a_word_is_matched_whatever_its_case():
    assert routing.published_kind(TAXONOMY, "CHRISTIAN") == "christian"
    assert routing.published_kind(TAXONOMY, "  christian ") == "christian"


def test_an_empty_word_is_no_kind():
    assert routing.published_kind(TAXONOMY, "") is None
    assert routing.published_kind(TAXONOMY, None) is None


def test_the_first_rule_that_matches_wins():
    # Both words contain a needle of a later rule: "dance" and "reggae".
    assert routing.published_kind(TAXONOMY, "Dancehall/Ragga") == "reggae"
    assert routing.published_kind(TAXONOMY, "Reggaeton") == "latin"


def test_the_long_spelling_of_rnb_is_rnb_and_not_the_blues_it_contains():
    assert routing.published_kind(TAXONOMY, "Rhythm & Blues") == "rnb"
    assert routing.published_kind(TAXONOMY, "Rhythm and Blues") == "rnb"
    assert routing.published_kind(TAXONOMY, "Blues") == "jazz"


def test_one_word_of_the_labels_kind_passes_a_release_listing_another_kind_too():
    judged = routing.kind_verdict(TAXONOMY, None, ["Pop", "Dance"])
    assert judged.verdict is KindVerdict.PASS
    assert judged.placed == (("Pop", "pop"), ("Dance", "dance"))


def test_a_word_no_rule_knows_is_not_judged_and_never_held():
    judged = routing.kind_verdict(TAXONOMY, None, ["Zydeco"])
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert "no rule of the gate knows" in judged.reason
    assert "Zydeco" in judged.reason


def test_an_unknown_word_does_not_save_a_release_a_known_word_places_elsewhere():
    judged = routing.kind_verdict(TAXONOMY, None, ["Zydeco", "Christian"])
    assert judged.verdict is KindVerdict.HOLD
    assert judged.placed == (("Christian", "christian"),)
    assert "which is christian and not dance" in judged.reason


def test_a_release_with_no_published_word_is_not_judged():
    judged = routing.kind_verdict(TAXONOMY, None, [])
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert judged.reason == "the general catalogue publishes no genre for it"


def test_the_labels_kind_decides_which_words_pass():
    assert routing.kind_verdict(TAXONOMY, "rnb", ["R&B"]).verdict is KindVerdict.PASS
    assert routing.kind_verdict(TAXONOMY, None, ["R&B"]).verdict is KindVerdict.HOLD
    assert routing.kind_verdict(TAXONOMY, "rnb", ["Dance"]).verdict is KindVerdict.HOLD


def test_a_label_followed_for_any_kind_passes_without_a_word():
    for genres in ([], ["Christian"], ["Zydeco"]):
        judged = routing.kind_verdict(TAXONOMY, "any", genres)
        assert judged.verdict is KindVerdict.PASS
        assert judged.kind == "any"
    assert routing.kind_settled(TAXONOMY, "any").verdict is KindVerdict.PASS


def test_a_kind_the_taxonomy_does_not_name_is_not_judged_and_says_which():
    judged = routing.kind_verdict(TAXONOMY, "polka", ["Christian"])
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert "'polka'" in judged.reason
    assert "does not name" in judged.reason


def test_a_label_with_no_kind_is_the_declared_default():
    assert routing.label_kind(TAXONOMY, None) == "dance"
    assert routing.label_kind(TAXONOMY, "") == "dance"
    assert routing.label_kind(TAXONOMY, " RNB ") == "rnb"
    assert routing.kind_settled(TAXONOMY, None) is None


# ── the loader ─────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def default_raw() -> dict:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    return tomllib.loads(source.read_text(encoding="utf-8"))


def problems_from(raw: dict, mutate) -> tuple[str, ...]:
    data = copy.deepcopy(raw)
    mutate(data)
    with pytest.raises(TaxonomyError) as caught:
        build_taxonomy(data)
    return caught.value.problems


def test_the_shipped_template_declares_the_default_kind_and_its_kinds():
    gate = TAXONOMY.label_gate
    assert gate.default_kind == "dance"
    assert set(gate.kinds) == set(MEASURED.values())
    assert "any" not in gate.kinds


def test_a_published_rule_with_no_matcher_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["published"].append({"kind": "polka"})

    assert any(
        "[[label_gate.published]]" in p and "needs all_of, any_of, or equals" in p
        for p in problems_from(default_raw, mutate)
    )


def test_a_published_rule_with_no_kind_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["published"].append({"any_of": ["polka"]})

    assert any("needs a kind" in p for p in problems_from(default_raw, mutate))


def test_a_published_rule_naming_the_reserved_kind_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["published"].append({"any_of": ["polka"], "kind": "any"})

    assert any(
        "cannot be the kind of a word" in p for p in problems_from(default_raw, mutate)
    )


def test_a_matcher_that_is_not_a_list_of_words_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["published"].append({"any_of": "polka", "kind": "polka"})

    assert any(
        "any_of must be a list of words" in p for p in problems_from(default_raw, mutate)
    )


def test_published_rules_in_one_pair_of_brackets_are_refused(default_raw):
    def mutate(data):
        data["label_gate"]["published"] = {"any_of": ["polka"], "kind": "polka"}

    assert any("two pairs of brackets" in p for p in problems_from(default_raw, mutate))


def test_a_default_kind_no_rule_names_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["default_kind"] = "polka"

    assert any(
        "default_kind 'polka' is not a kind" in p for p in problems_from(default_raw, mutate)
    )


def test_a_default_kind_that_is_not_a_word_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["default_kind"] = 7

    assert any("default_kind must be" in p for p in problems_from(default_raw, mutate))


def test_the_word_that_clears_a_kind_cannot_be_the_kind_of_a_word(default_raw):
    def mutate(data):
        data["label_gate"]["published"].append({"any_of": ["polka"], "kind": "default"})

    assert any("clears a label's kind" in p for p in problems_from(default_raw, mutate))


def test_a_share_rule_needle_typed_with_a_capital_matches_too(default_raw):
    """Both rule tables are folded when loaded and matched by one function."""
    data = copy.deepcopy(default_raw)
    data["label_gate"]["rule"].append({"any_of": ["Gqom"], "family": "gqom"})
    data["label_gate"]["rule"].append({"equals": ["Kwaito"], "family": "kwaito"})
    built = build_taxonomy(data)
    assert routing.gate_family(built, "gqom") == "gqom"
    assert routing.gate_family(built, "KWAITO") == "kwaito"


def test_a_kind_no_label_could_be_marked_with_is_refused(default_raw):
    """The registry stores a kind as one word, so a rule may name no other shape."""

    def mutate(data):
        data["label_gate"]["published"].append({"any_of": ["polka"], "kind": "hip hop"})

    assert any(
        "kind 'hip hop' is not one word" in p for p in problems_from(default_raw, mutate)
    )


def test_a_default_kind_of_two_words_is_refused(default_raw):
    def mutate(data):
        data["label_gate"]["default_kind"] = "hip hop"

    assert any("default_kind must be" in p for p in problems_from(default_raw, mutate))


def test_every_shipped_kind_is_one_the_registry_will_store():
    for kind in (*TAXONOMY.label_gate.kinds, "any"):
        assert labels.check_kind(kind) == kind


def test_a_default_of_any_is_allowed(default_raw):
    data = copy.deepcopy(default_raw)
    data["label_gate"]["default_kind"] = "any"
    assert build_taxonomy(data).label_gate.default_kind == "any"


def test_a_needle_typed_with_a_capital_still_matches(default_raw):
    data = copy.deepcopy(default_raw)
    data["label_gate"]["published"].append({"equals": ["Zydeco"], "kind": "Folk_Country"})
    built = build_taxonomy(data)
    assert routing.published_kind(built, "zydeco") == "folk_country"


def test_a_copy_written_before_the_gate_had_published_rules_loads_and_judges_nothing(
    default_raw,
):
    data = copy.deepcopy(default_raw)
    del data["label_gate"]["published"]
    del data["label_gate"]["default_kind"]
    built = build_taxonomy(data)
    assert built.label_gate.published == ()
    assert built.label_gate.default_kind == "dance"
    judged = routing.kind_verdict(built, None, ["Christian"])
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert "declares no rule" in judged.reason
    assert routing.kind_settled(built, None) is not None


# ═══════════════════════════════════════════════════════════════════════════
# 2. Asking the general catalogue about one release
# ═══════════════════════════════════════════════════════════════════════════


def test_the_first_track_that_answers_with_a_genre_is_the_releases_answer():
    lookup = Lookup({isrc(2): ("Christian",), isrc(3): ("Dance",)})
    rows = [Track("1", "A", "One", isrc(1)), Track("2", "A", "Two", isrc(2)), Track("3", "A", "Three", isrc(3))]
    words = genre_gate.published_words(rows, lookup)
    assert words.genres == ("Christian",)
    assert words.answer == "matched"
    assert lookup.asked == [isrc(1), isrc(2)]


def test_no_more_than_three_tracks_are_asked_about():
    lookup = Lookup({isrc(4): ("Dance",)})
    rows = [Track(str(n), "A", f"T{n}", isrc(n)) for n in range(1, 6)]
    words = genre_gate.published_words(rows, lookup)
    assert genre_gate.TRACKS_ASKED == 3
    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]
    assert words.genres == ()
    assert words.answer == "miss"
    assert words.why_none == "the general catalogue does not know its tracks"


@pytest.mark.parametrize("answer", ["blocked", "unreachable", "parse-break"])
def test_an_answer_that_could_not_be_read_stops_the_asking(answer):
    lookup = Lookup({isrc(1): answer, isrc(2): ("Dance",)})
    rows = [Track("1", "A", "One", isrc(1)), Track("2", "A", "Two", isrc(2))]
    words = genre_gate.published_words(rows, lookup)
    assert lookup.asked == [isrc(1)]
    assert words.unread
    assert words.answer == answer
    assert f"could not be read ({answer})" in words.why_none


def test_a_release_with_no_isrc_asks_nothing_and_says_so():
    words = genre_gate.published_words(
        [Track("1", "A", "One"), {"title": "Two", "isrc": "  "}], never_asked
    )
    assert words.answer == "no-isrc"
    assert not words.unread
    assert "carries an ISRC" in words.why_none


def test_a_row_is_read_as_a_mapping_or_an_object_and_an_isrc_is_asked_once():
    lookup = Lookup({})
    rows = [{"isrc": isrc(1)}, Track("2", "A", "Two", isrc(1)), {"isrc": isrc(2)}]
    genre_gate.published_words(rows, lookup)
    assert lookup.asked == [isrc(1), isrc(2)]


def test_a_match_that_publishes_no_genre_says_that_and_not_a_miss():
    lookup = Lookup({isrc(1): ()})
    words = genre_gate.published_words([Track("1", "A", "One", isrc(1))], lookup)
    assert words.answer == "matched"
    assert words.why_none == "the general catalogue knows it and publishes no genre for it"


def test_a_track_the_catalogue_knows_outranks_one_it_does_not_whatever_the_order():
    rows = [Track("1", "A", "One", isrc(1)), Track("2", "A", "Two", isrc(2))]
    words = genre_gate.published_words(rows, Lookup({isrc(1): ()}))
    assert words.answer == "matched"
    assert words.why_none == "the general catalogue knows it and publishes no genre for it"
    rows = [Track("1", "A", "One", isrc(1)), Track("2", "A", "Two", "not an isrc")]
    words = genre_gate.published_words(
        rows,
        lambda value: published.Published(
            published.SOURCE, "no-isrc" if "not" in str(value) else "miss"
        ),
    )
    assert words.answer == "miss"


def test_an_isrc_under_external_ids_is_asked_about():
    lookup = Lookup({isrc(1): ("Dance",)})
    words = genre_gate.published_words([{"external_ids": {"isrc": isrc(1)}}], lookup)
    assert lookup.asked == [isrc(1)]
    assert words.genres == ("Dance",)


def test_a_release_that_would_be_held_is_asked_about_again_before_it_is():
    """One track's ISRC can sit on a compilation of another kind."""
    lookup = Lookup({isrc(1): ("Pop",), isrc(2): ("Dance",), isrc(3): ("Christian",)})
    rows = [Track(str(n), "A", f"T{n}", isrc(n)) for n in (1, 2, 3)]
    judged = genre_gate.judge_rows(TAXONOMY, None, rows, genre_gate.Asking(lookup))
    assert judged.verdict is KindVerdict.PASS
    assert judged.genres == ("Pop", "Dance")
    assert lookup.asked == [isrc(1), isrc(2)]


def test_a_release_whose_first_track_passes_asks_about_no_other():
    lookup = Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)})
    rows = [Track(str(n), "A", f"T{n}", isrc(n)) for n in (1, 2)]
    judged = genre_gate.judge_rows(TAXONOMY, None, rows, genre_gate.Asking(lookup))
    assert judged.verdict is KindVerdict.PASS
    assert lookup.asked == [isrc(1)]


def test_a_release_is_held_only_when_every_track_asked_agrees():
    lookup = Lookup({isrc(n): ("Christian",) for n in (1, 2, 3, 4)})
    rows = [Track(str(n), "A", f"T{n}", isrc(n)) for n in (1, 2, 3, 4)]
    judged = genre_gate.judge_rows(TAXONOMY, None, rows, genre_gate.Asking(lookup))
    assert judged.verdict is KindVerdict.HOLD
    assert judged.genres == ("Christian",)
    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]


def test_a_catalogue_that_refuses_after_a_would_be_hold_holds_nothing():
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): "blocked"})
    rows = [Track(str(n), "A", f"T{n}", isrc(n)) for n in (1, 2, 3)]
    judged = genre_gate.judge_rows(TAXONOMY, None, rows, genre_gate.Asking(lookup))
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert judged.answer == "blocked"
    assert judged.genres == ()
    assert lookup.asked == [isrc(1), isrc(2)]


def test_three_releases_unread_in_a_row_end_the_asking_and_an_answer_resets_it():
    """An unreachable catalogue is not remembered by the lookup, so without this
    every release of every label pays a transport timeout."""
    table = {isrc(n): "unreachable" for n in (1, 2, 4, 5, 6)}
    table[isrc(3)] = ("Dance",)
    lookup = Lookup(table)
    asking = genre_gate.Asking(lookup)

    def ask(n: int | None) -> genre_gate.Words:
        return asking.words([Track("t", "A", "T", isrc(n) if n else "")])

    assert [ask(n).answer for n in (1, 2)] == ["unreachable", "unreachable"]
    assert ask(None).answer == "no-isrc"  # asked nothing: neither ends the run nor extends it
    assert ask(3).genres == ("Dance",)  # an answer ends the run of two
    assert [ask(n).answer for n in (4, 5, 6)] == ["unreachable"] * 3
    asked = list(lookup.asked)
    unasked = ask(7)
    assert lookup.asked == asked
    assert unasked.answer == "not-asked"
    assert not unasked.unread
    assert unasked.why_none == (
        "the general catalogue could not be read for 3 releases in a row, so the "
        "rest were not asked about"
    )
    assert genre_gate.UNREAD_IN_A_ROW == 3


def test_the_gate_names_the_review_kind_the_sweep_files_under():
    # The literal, not one module's name for it against the other's: the two
    # are one object since the review, and X equals X would hold for any word.
    assert sweep.KIND == "label-release"
    assert genre_gate.RELEASE_KIND == "label-release"
    assert genre_gate.release_item_id("r1") == review.item_id_for(
        "label-release", "label-release", {"release_id": "r1"}
    )


class FailingReader:
    """A release reader that fails for the releases named, and counts every read."""

    def __init__(self, failing: set[str], gone: set[str] = frozenset()) -> None:
        self.failing = failing
        self.gone = gone
        self.read: list[str] = []

    def __call__(self, release_id: str):
        self.read.append(release_id)
        if release_id in self.gone:
            raise ReleaseUnresolvable(release_id)
        if release_id in self.failing:
            raise RuntimeError("the provider timed out")
        return (Track("1", "A", "One", isrc(1)),), 2026


ENTRY = labels.LabelEntry(label_id=SLUG, name=LABEL)


class Flaky(FakeCatalogue):
    """A provider that fails for the releases named and has lost some others."""

    def __init__(self, failing: set[str], gone: set[str] = frozenset()) -> None:
        super().__init__()
        self.failing = failing
        self.gone = gone

    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        if release_id in self.gone:
            raise ReleaseUnresolvable(release_id)
        if release_id in self.failing:
            raise RuntimeError("the provider timed out")
        return (Track("1", "A", "One", isrc(1)),), 2026


def test_three_failed_reads_in_a_row_end_the_asking_and_a_gone_release_resets_it():
    fake = Flaky({"a", "b", "e", "f", "g"}, gone={"d"})
    gate = genre_gate.SweepGate(
        TAXONOMY, tracks=ReleaseTracks(fake).release_tracks, lookup=Lookup({})
    )
    reasons = [gate.judge(ENTRY, rid).reason for rid in "abdefgh"]
    # a and b fail, d is the provider answering, e f g fail, h is not asked.
    assert fake.releases_asked_for == ["a", "b", "d", "e", "f", "g"]
    assert "could not be read from the provider (RuntimeError" in reasons[0]
    assert "the provider no longer has the release" in reasons[2]
    assert reasons[6] == (
        "its tracks were not read: the provider failed 3 releases in a row, so the "
        "rest were not asked for"
    )
    assert gate.judge(ENTRY, "h").verdict is KindVerdict.NOT_JUDGED


def test_a_read_the_gate_never_saw_still_ends_a_run_of_failures():
    """The review's case: the ownership question reads a release the gate is
    never asked about, and its success must break the gate's run too."""
    fake = Flaky({"a", "b", "d"})
    reader = ReleaseTracks(fake)
    gate = genre_gate.SweepGate(TAXONOMY, tracks=reader.release_tracks, lookup=Lookup({}))
    for rid in "ab":
        gate.judge(ENTRY, rid)
    reader.release_tracks("c")  # the ownership question, alone
    gate.judge(ENTRY, "d")
    judged = gate.judge(ENTRY, "e")
    assert fake.releases_asked_for == ["a", "b", "c", "d", "e"]
    assert "not read" not in judged.reason


def test_the_reader_does_not_ask_the_provider_once_it_is_failing():
    fake = Flaky({"a", "b", "c"})
    reader = ReleaseTracks(fake)
    for rid in "abc":
        with pytest.raises(RuntimeError):
            reader.release_tracks(rid)
    with pytest.raises(ReleasesUnasked):
        reader.release_tracks("d")
    assert fake.releases_asked_for == ["a", "b", "c"]
    # A release already read keeps its remembered answer, whatever it was.
    with pytest.raises(RuntimeError):
        reader.release_tracks("a")


def test_a_label_of_any_kind_reads_no_track_and_asks_nothing():
    reader = FailingReader(set())
    gate = genre_gate.SweepGate(TAXONOMY, tracks=reader, lookup=never_asked)
    judged = gate.judge(labels.LabelEntry(label_id=SLUG, name=LABEL, kind="any"), "r1")
    assert judged.verdict is KindVerdict.PASS
    assert judged.answer == "not-asked"
    assert reader.read == []


# ── one release read once, for both questions ──────────────────────────────


def test_a_release_is_read_from_the_provider_once_however_often_it_is_asked_for():
    fake = FakeCatalogue(releases={"r1": ([Track("1", "A", "One", isrc(1))], 2026)})
    reader = ReleaseTracks(fake)
    first = reader.release_tracks("r1")
    assert reader.release_tracks("r1") is first
    assert fake.releases_asked_for == ["r1"]


def test_a_failed_read_is_remembered_and_raised_again_as_it_was():
    class Down(FakeCatalogue):
        def release_tracks(self, release_id):
            self.releases_asked_for.append(release_id)
            raise RuntimeError("the provider timed out")

    fake = Down()
    reader = ReleaseTracks(fake)
    with pytest.raises(RuntimeError) as first:
        reader.release_tracks("r1")
    with pytest.raises(RuntimeError) as second:
        reader.release_tracks("r1")
    assert second.value is first.value
    assert fake.releases_asked_for == ["r1"]


# ═══════════════════════════════════════════════════════════════════════════
# 3. The hold record
# ═══════════════════════════════════════════════════════════════════════════


def hold_one(store, release_id: str, *, run_id: str = "run-1", reason: str = "held", group=SLUG):
    return review.hold(
        store,
        queue=Queue.LABEL_RELEASE,
        kind=sweep.KIND,
        identity={"release_id": release_id},
        payload={"identity": release_id, "title": f"Release {release_id}"},
        group=group,
        name=LABEL,
        reason=reason,
        detail={"genres": ["Christian"], "kind": "dance"},
        run_id=run_id,
    )


def test_a_hold_is_not_a_review_item_and_not_a_tombstone(installed):
    with review.open_store(installed) as store:
        held = hold_one(store, "r1")
        assert held.state == review.HOLD_HELD
        assert held.item_id == genre_gate.release_item_id("r1")
        assert review.find(store, held.item_id) is None
        assert review.list_items(store, queue=None, include_resolved=True, limit=None).items == ()
    assert DecisionStore(tombstone.STORE_KEY, installed).suppressions(include_revoked=True) == ()


def test_holding_again_refreshes_the_reason_and_keeps_the_first_run(installed):
    with review.open_store(installed) as store:
        first = hold_one(store, "r1", run_id="run-1", reason="first")
        again = hold_one(store, "r1", run_id="run-2", reason="second")
        assert (again.run_id, again.reason, again.created) == ("run-1", "second", first.created)
        assert len(review.holds(store, queue=Queue.LABEL_RELEASE)) == 1


def test_a_returned_hold_is_never_held_again(installed):
    with review.open_store(installed) as store:
        held = hold_one(store, "r1")
        returned = review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=held.item_id)
        assert returned.state == review.HOLD_RETURNED
        again = hold_one(store, "r1", reason="held a second time")
        assert again.state == review.HOLD_RETURNED
        assert again.reason == "held"
        assert review.holds(store, queue=Queue.LABEL_RELEASE) == ()
        assert [
            one.state
            for one in review.holds(store, queue=Queue.LABEL_RELEASE, states=review.HOLD_STATES)
        ] == [review.HOLD_RETURNED]


def test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one(installed):
    with review.open_store(installed) as store:
        one, two = hold_one(store, "r1"), hold_one(store, "r2")
        review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id)
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id=one.item_id) is True
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id) is False
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id="rv_none") is False
        assert review.find_hold(store, queue=Queue.LABEL_RELEASE, item_id=one.item_id) is None
        assert (
            review.find_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id).state
            == review.HOLD_RETURNED
        )


def test_returning_a_hold_nothing_made_answers_none(installed):
    with review.open_store(installed) as store:
        assert review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id="rv_none") is None


def test_a_label_with_holds_and_no_items_still_has_its_row(installed):
    with review.open_store(installed) as store:
        hold_one(store, "r1", run_id="run-1")
        hold_one(store, "r2", run_id="run-1")
        hold_one(store, "r3", run_id="run-2")
        returned = hold_one(store, "r4", run_id="run-2")
        review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=returned.item_id)
        by_label = review.grouped(store, queue=Queue.LABEL_RELEASE, by="label")
        by_run = review.grouped(store, queue=Queue.LABEL_RELEASE, by="run")
    assert by_label == [
        {"label": SLUG, "label_name": LABEL, "items": 0, "beyond": None, "swept": None, "held": 3}
    ]
    assert by_run == [
        {"run": "run-1", "items": 0, "labels": 1, "beyond": None, "held": 2},
        {"run": "run-2", "items": 0, "labels": 1, "beyond": None, "held": 1},
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 4. Through the worker: what a sweep files and what it holds
# ═══════════════════════════════════════════════════════════════════════════


def test_a_release_of_another_kind_is_held_and_counted_for_its_label(installed, monkeypatch):
    """AE5. A dance label, a release the general catalogue calls Christian."""
    register()
    bind(monkeypatch, {"r-dance": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)}))

    sweep_once()

    assert list(filed(installed)) == ["r-dance"]
    assert held_ids(installed) == ["r-christian"]
    [row] = grouped("label")
    assert (row["label"], row["items"], row["held"]) == (SLUG, 1, 1)
    [by_run] = grouped("run")
    assert (by_run["items"], by_run["held"]) == (1, 1)

    code, envelope = held_verb()
    assert code == int(ExitCode.OK), envelope
    assert "1 release(s) held by the genre gate across 1 label(s)" in (
        check(envelope, "label.held.held")["detail"]
    )
    assert check(envelope, f"label.held.label.{SLUG}")["detail"] == (
        "Tide Works: 1 held, 1 the general catalogue calls Christian"
    )
    line = check(envelope, "label.held.release.r-christian")["detail"]
    assert "release r-christian ('Release r-christian' by Label Act) on Tide Works is held" in line
    assert "which is christian and not dance, the kind its label is followed as" in line
    assert "crate label held return r-christian" in line
    [release] = envelope["data"]["summary"]["releases"]
    assert (release["release_id"], release["genres"], release["kind"]) == (
        "r-christian",
        ["Christian"],
        "dance",
    )
    # Not rejected: no tombstone of any kind was written.
    assert DecisionStore(tombstone.STORE_KEY, installed).suppressions(include_revoked=True) == ()


def test_a_filed_release_says_the_gate_passed_it_and_on_which_words(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-dance": ("2026", isrc(1))})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Electro", "Pop")}))
    sweep_once()
    payload = filed(installed)["r-dance"].payload
    assert payload["genre_gate"] == "passed"
    assert payload["genre_gate_answer"] == "matched"
    assert payload["published_genres"] == ["Electro", "Pop"]
    assert "Electro, Pop" in payload["genre_gate_note"]
    assert filed(installed)["r-dance"].verdict is None


def test_the_labels_kind_decides_what_is_filed(installed, monkeypatch):
    """AE6. An R&B release is filed from an R&B label and held from a dance one."""
    register("--kind", "rnb")
    register(name="Salt Flats")
    fake = Provider(
        artists={
            SLUG: FakePagedArtist([FakeRelease("r-a")]),
            "salt-flats": FakePagedArtist([FakeRelease("r-b")]),
        },
        releases={
            "r-a": ([Track("1", "A", "One", isrc(1))], 2026),
            "r-b": ([Track("2", "A", "One", isrc(1))], 2026),
        },
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    bind_lookup(monkeypatch, Lookup({isrc(1): ("R&B",)}))

    sweep_once()

    assert list(filed(installed)) == ["r-a"]
    assert held_ids(installed) == ["r-b"]
    assert {row["label"]: row["held"] for row in grouped("label")} == {SLUG: 0, "salt-flats": 1}


def test_a_release_the_catalogue_does_not_know_is_filed_and_marked_not_judged(
    installed, monkeypatch
):
    """AE7."""
    register()
    bind(monkeypatch, {"r-unknown": ("2026", isrc(1))})
    bind_lookup(monkeypatch, Lookup({}))

    sweep_once()

    payload = filed(installed)["r-unknown"].payload
    assert payload["genre_gate"] == "not-judged"
    assert payload["genre_gate_answer"] == "miss"
    assert payload["genre_gate_note"] == "the general catalogue does not know its tracks"
    assert "published_genres" not in payload
    assert held_ids(installed) == []


def test_a_held_release_returned_to_review_is_filed_and_not_held_again(installed, monkeypatch):
    register()
    fake = bind(monkeypatch, {"r-dance": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))})
    lookup = Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)})
    bind_lookup(monkeypatch, lookup)
    sweep_once()
    [first] = [row["run"] for row in grouped("run")]

    code, envelope = held_verb("return", "r-christian")

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"] == {
        "returned": ["r-christian"],
        "marked": [],
        "already_returned": [],
    }
    item = filed(installed)["r-christian"]
    assert item.verdict is None
    assert item.payload["genre_gate"] == "returned"
    assert item.payload["title"] == "Release r-christian"
    assert item.payload["label_id"] == SLUG
    assert item.payload[sweep.SWEEP_RUN] == first
    assert item.handler_key == sweep.HANDLER_KEY
    assert held_ids(installed) == []
    assert held_ids(installed, states=(review.HOLD_RETURNED,)) == ["r-christian"]

    asked, verified = list(lookup.asked), list(fake.verified)
    sweep_once()

    assert sorted(filed(installed)) == ["r-christian", "r-dance"]
    assert held_ids(installed) == []
    # Both are in the queue now, so the second sweep asked nobody anything.
    assert (lookup.asked, fake.verified) == (asked, verified)
    code, envelope = held_verb()
    assert code == int(ExitCode.OK)
    assert envelope["outcome"] == "no_op"
    assert check(envelope, "label.held.held")["detail"] == "no release is held by the genre gate"


def test_returning_twice_changes_nothing_the_second_time(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(2): ("Christian",)}))
    sweep_once()
    held_verb("return", "r-christian")
    before = filed(installed)["r-christian"]

    code, envelope = held_verb("return", "r-christian")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"] == {
        "returned": [],
        "marked": [],
        "already_returned": ["r-christian"],
    }
    assert filed(installed)["r-christian"].payload == before.payload


def test_returning_a_release_nothing_holds_refuses_and_files_none_of_the_others(
    installed, monkeypatch
):
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(2): ("Christian",)}))
    sweep_once()

    code, envelope = held_verb("return", "r-christian", "r-typo")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-item-unknown"
    assert envelope["cause"]["detail"]["unknown"] == ["r-typo"]
    assert filed(installed) == {}
    assert held_ids(installed) == ["r-christian"]


def test_return_needs_a_release_and_a_listing_takes_none(installed):
    code, envelope = held_verb("return")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-selection-invalid"
    code, envelope = held_verb("list", "r-1")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_a_labels_kind_changed_after_a_hold_releases_what_now_fits(installed, monkeypatch):
    register()
    fake = bind(monkeypatch, {"r-rnb": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("R&B",), isrc(2): ("Christian",)}))
    sweep_once()
    assert filed(installed) == {}
    assert sorted(held_ids(installed)) == ["r-christian", "r-rnb"]

    code, envelope = drive(["label", "registry", "set", LABEL, "--kind", "rnb"])
    assert code == int(ExitCode.OK), envelope
    # NO REQUEST: the second sweep judges the holds on the words they recorded.
    bind_lookup(monkeypatch, never_asked)
    verified, read = list(fake.verified), list(fake.releases_asked_for)
    sweep_once()

    assert list(filed(installed)) == ["r-rnb"]
    assert held_ids(installed) == ["r-christian"]
    # Nothing is verified again. The one provider read is the increment asking
    # whether the library came to own the released release in the meantime.
    assert fake.verified == verified
    assert fake.releases_asked_for == [*read, "r-rnb"]
    payload = filed(installed)["r-rnb"].payload
    assert payload["genre_gate"] == "passed"
    assert payload["published_genres"] == ["R&B"]
    # Filed under the sweep that released it, and still counted held under
    # the sweep that first held the one that stands.
    by_run = {row["run"]: (row["items"], row["held"]) for row in grouped("run")}
    assert sorted(by_run.values()) == [(0, 1), (1, 0)]
    assert by_run[payload[sweep.SWEEP_RUN]] == (1, 0)
    # The hold that stands says the kind it is now held against.
    with review.open_store(installed) as store:
        [standing] = review.holds(store, queue=Queue.LABEL_RELEASE)
    assert "not rnb" in standing.reason
    assert standing.detail["kind"] == "rnb"


def test_a_catalogue_unread_on_every_release_holds_nothing_and_says_so(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-1": ("2026", isrc(1)), "r-2": ("2025", isrc(2))})
    lookup = Lookup({isrc(1): "blocked", isrc(2): "blocked"})
    bind_lookup(monkeypatch, lookup)

    sweep_once()

    assert sorted(filed(installed)) == ["r-1", "r-2"]
    assert held_ids(installed) == []
    for item in filed(installed).values():
        assert item.payload["genre_gate"] == "not-judged"
        assert item.payload["genre_gate_answer"] == "blocked"
        assert "could not be read (blocked)" in item.payload["genre_gate_note"]
    code, envelope = held_verb()
    assert code == int(ExitCode.OK), envelope
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "fail"
    assert (
        "the general catalogue could not be read for any of the 2 release(s) the newest "
        "sweep of Tide Works asked it about"
    ) in line["detail"]
    assert "HELD NOTHING" in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert (row["filed"], row["asked"], row["not_judged"], row["unread"], row["held"]) == (
        2, 2, 2, 2, 0,
    )


def test_a_sweep_that_judged_some_and_not_others_says_how_many(installed, monkeypatch):
    register()
    bind(
        monkeypatch,
        {"r-1": ("2026", isrc(1)), "r-2": ("2025", isrc(2)), "r-3": ("2024", isrc(3))},
    )
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Dance",), isrc(3): ("Christian",)}))

    sweep_once()

    code, envelope = held_verb()
    assert code == int(ExitCode.OK), envelope
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "info"
    assert "filed 2 release(s) and the genre gate could not judge 1 of them" in line["detail"]
    assert "could not be read" not in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert (row["filed"], row["asked"], row["not_judged"], row["unread"], row["held"]) == (
        2, 3, 1, 0, 1,
    )


def test_a_sweep_the_gate_judged_in_full_has_no_sweep_line(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-1": ("2026", isrc(1))})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Dance",)}))
    sweep_once()
    _code, envelope = held_verb()
    assert [one["key"] for one in envelope["data"]["checks"]] == ["label.held.held"]


def test_a_sweep_that_holds_some_releases_files_no_more_than_the_window(
    installed, monkeypatch
):
    """R-790's window: a held release takes a place, so nothing is read past it."""
    register("--offer", "3")
    fake = bind(
        monkeypatch,
        {
            "r-6": ("2026", isrc(6)),
            "r-5": ("2025", isrc(5)),
            "r-4": ("2024", isrc(4)),
            "r-3": ("2023", isrc(3)),
            "r-2": ("2022", isrc(2)),
            "r-1": ("2021", isrc(1)),
        },
    )
    lookup = Lookup(
        {isrc(6): ("Christian",), isrc(5): ("Christian",), **{isrc(n): ("Dance",) for n in (1, 2, 3, 4)}}
    )
    bind_lookup(monkeypatch, lookup)

    sweep_once()

    assert list(filed(installed)) == ["r-4"]
    assert sorted(held_ids(installed)) == ["r-5", "r-6"]
    [row] = grouped("label")
    assert (row["items"], row["held"], row["beyond"]) == (1, 2, 3)
    assert lookup.asked == [isrc(6), isrc(5), isrc(4)]
    assert fake.verified == ["r-6", "r-5", "r-4"]

    # A second sweep files nothing more, and asks nobody about what it holds.
    sweep_once()
    assert list(filed(installed)) == ["r-4"]
    assert sorted(held_ids(installed)) == ["r-5", "r-6"]
    assert lookup.asked == [isrc(6), isrc(5), isrc(4)]
    assert fake.verified == ["r-6", "r-5", "r-4"]
    # Each release was read from the provider once, for ownership and the gate.
    assert sorted(fake.releases_asked_for) == ["r-4", "r-5", "r-6"]


def test_the_catalogue_is_asked_only_about_a_release_that_would_be_filed(installed, monkeypatch):
    """Not about one the provider would not confirm, and not about one already queued."""
    register()
    fake = bind(
        monkeypatch,
        {"r-2": ("2026", isrc(2)), "r-1": ("2025", isrc(1))},
        confirmed={"r-1"},
    )
    lookup = Lookup({isrc(1): ("Dance",), isrc(2): ("Dance",)})
    bind_lookup(monkeypatch, lookup)
    sweep_once()
    assert list(filed(installed)) == ["r-1"]
    assert lookup.asked == [isrc(1)]
    assert fake.releases_asked_for == ["r-1"]
    sweep_once()
    assert lookup.asked == [isrc(1)]


def test_a_label_followed_for_any_kind_files_everything_and_asks_nothing(installed, monkeypatch):
    register("--kind", "any")
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, never_asked)
    sweep_once()
    payload = filed(installed)["r-christian"].payload
    assert payload["genre_gate"] == "passed"
    assert payload["genre_gate_answer"] == "not-asked"
    assert payload["genre_gate_note"] == "its label is followed for any kind of music"


def active_copy_without_published_rules(cfg: config.Config) -> None:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    text = source.read_text(encoding="utf-8")
    cut = text.index("# The same gate asked about KIND")
    body = text[:cut].replace('default_kind = "dance"\n', "")
    assert "label_gate.published" not in body and "default_kind" not in body
    path = config.state_path("taxonomy_active", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_a_library_whose_taxonomy_has_no_published_rules_files_as_before_and_asks_nothing(
    installed, monkeypatch
):
    """The live copy, until it takes the new section by hand at a sitting."""
    active_copy_without_published_rules(installed)
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, never_asked)

    sweep_once()

    payload = filed(installed)["r-christian"].payload
    assert payload["genre_gate"] == "not-judged"
    assert "declares no rule" in payload["genre_gate_note"]
    assert held_ids(installed) == []
    code, envelope = drive(["label", "registry", "set", LABEL, "--kind", "rnb"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "declares no kinds at all" in envelope["cause"]["message"]


def test_a_taxonomy_that_cannot_be_read_refuses_the_sweep_before_the_provider_is_resolved(
    installed, monkeypatch
):
    register()
    path = config.state_path("taxonomy_active", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("this is not a taxonomy = = =", encoding="utf-8")

    def never(_cfg):
        raise AssertionError("the provider was resolved")

    monkeypatch.setattr(catalogue, "resolve", never)
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), resumed
    assert filed(installed) == {}


def test_a_dead_verifier_over_a_window_of_standing_holds_refuses(installed, monkeypatch):
    """A standing hold is not verified again, so it must not hide a dead verifier."""
    register("--offer", "3")
    releases = {"r-2": ("2025", isrc(2)), "r-1": ("2024", isrc(1))}
    bind(monkeypatch, releases)
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Christian",), isrc(2): ("Christian",)}))
    sweep_once()
    assert sorted(held_ids(installed)) == ["r-1", "r-2"]

    bind(monkeypatch, {"r-3": ("2026", isrc(3)), **releases}, confirmed=set())
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])

    assert code != int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        [item] = jobs.items(store, job_id)
    assert item.cause.reason == "label-sweep-incomplete"
    assert sorted(held_ids(installed)) == ["r-1", "r-2"]


def test_an_unreachable_catalogue_is_given_up_on_once_for_the_whole_sweep(
    installed, monkeypatch
):
    """One job, two labels. The outage is counted across them, not per label."""
    register()
    register(name="Salt Flats")
    fake = Provider(
        artists={
            SLUG: FakePagedArtist([FakeRelease("a-1", year="2026"), FakeRelease("a-2", year="2025")]),
            "salt-flats": FakePagedArtist(
                [FakeRelease("b-1", year="2026"), FakeRelease("b-2", year="2025")]
            ),
        },
        releases={
            rid: ([Track(f"t-{rid}", "Label Act", f"Release {rid}", isrc(n))], 2026)
            for n, rid in enumerate(("a-1", "a-2", "b-1", "b-2"), start=1)
        },
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    lookup = Lookup({isrc(n): "unreachable" for n in (1, 2, 3, 4)})
    bind_lookup(monkeypatch, lookup)

    sweep_once()

    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]
    assert sorted(filed(installed)) == ["a-1", "a-2", "b-1", "b-2"]
    last = filed(installed)["b-2"].payload
    assert last["genre_gate"] == "not-judged"
    assert last["genre_gate_answer"] == "not-asked"
    assert "3 releases in a row" in last["genre_gate_note"]
    assert held_ids(installed) == []


def test_a_release_with_no_isrc_does_not_hide_a_sweep_the_catalogue_refused_throughout(
    installed, monkeypatch
):
    """It was never asked about, so it is not one of the questions that went unread."""
    register()
    bind(monkeypatch, {"r-1": ("2026", isrc(1)), "r-2": ("2025", "")})
    bind_lookup(monkeypatch, Lookup({isrc(1): "blocked"}))

    sweep_once()

    _code, envelope = held_verb()
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "fail"
    assert "any of the 1 release(s)" in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert (row["filed"], row["asked"], row["not_judged"], row["unread"]) == (2, 1, 2, 1)


def test_a_hold_the_window_no_longer_reaches_is_dropped_when_it_stops_holding(
    installed, monkeypatch
):
    """Newer releases push a held one past the window. It must not stay counted
    as held under a reason the label's new kind made untrue."""
    register("--offer", "1")
    older = {"r-1": ("2025", isrc(1))}
    bind(monkeypatch, older)
    bind_lookup(monkeypatch, Lookup({isrc(1): ("R&B",), isrc(2): ("Dance",)}))
    sweep_once()
    assert held_ids(installed) == ["r-1"]

    bind(monkeypatch, {"r-2": ("2026", isrc(2)), **older})
    sweep_once()
    # Still a dance label: the newer release is filed and the hold stands,
    # though the window of one never reached it.
    assert list(filed(installed)) == ["r-2"]
    assert held_ids(installed) == ["r-1"]

    drive(["label", "registry", "set", LABEL, "--kind", "rnb"])
    bind_lookup(monkeypatch, never_asked)
    sweep_once()

    assert held_ids(installed) == []
    # Not filed either: it is past the window, like any release the sweep
    # has not examined, and is counted there.
    assert list(filed(installed)) == ["r-2"]
    [row] = grouped("label")
    assert (row["items"], row["held"], row["beyond"]) == (1, 0, 1)


def test_a_held_release_deleted_on_purpose_since_is_held_no_longer(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(2): ("Christian",)}))
    sweep_once()
    assert held_ids(installed) == ["r-christian"]
    DecisionStore(tombstone.STORE_KEY, installed).record(
        kind=tombstone.KIND_VERSION,
        identity=tombstone.version_identity(artist="Label Act", title="Release r-christian"),
        actor="test",
    )
    sweep_once()
    assert held_ids(installed) == []
    assert filed(installed) == {}


def test_a_hold_on_a_label_nobody_follows_any_more_says_so(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(2): ("Christian",)}))
    sweep_once()
    _code, envelope = held_verb()
    assert "no longer followed" not in check(envelope, "label.held.release.r-christian")["detail"]
    drive(["label", "registry", "remove", LABEL])
    _code, envelope = held_verb()
    assert (
        "its label is no longer followed, so no sweep will judge it again"
        in check(envelope, "label.held.release.r-christian")["detail"]
    )


# ── the engine, where the property is about one listing ────────────────────


def listing(cfg, entry, releases, *, gate, offered=None, limit=None, owned=None):
    return sweep.list_for_label(
        cfg,
        entry,
        artist=FakePagedArtist(releases),
        verify=lambda claimed, release: {"verdict": "confirmed"},
        offered=offered,
        owned=owned,
        limit=limit,
        gate=gate,
    )


def test_a_hold_in_force_on_a_release_already_in_the_queue_is_dropped(installed):
    """A process that dies between filing a release and dropping its hold leaves both."""
    with review.open_store(installed) as store:
        hold_one(store, "r1")
        gate = genre_gate.SweepGate(
            TAXONOMY,
            tracks=FailingReader(set()),
            standing=genre_gate.StandingHolds(store),
            lookup=never_asked,
        )
        found = listing(installed, ENTRY, [FakeRelease("r1")], gate=gate, offered={"r1"})
    assert found.held == 1
    assert (found.candidates, found.gated) == ((), ())
    assert found.stale == ("r1",)


def test_a_released_hold_the_library_came_to_own_is_dropped_and_not_filed(installed):
    rnb = labels.LabelEntry(label_id=SLUG, name=LABEL, kind="rnb")
    with review.open_store(installed) as store:
        review.hold(
            store,
            queue=Queue.LABEL_RELEASE,
            kind=sweep.KIND,
            identity={"release_id": "r1"},
            payload={"identity": "r1"},
            group=SLUG,
            name=LABEL,
            reason="held while the label was a dance label",
            detail={"genres": ["R&B"], "kind": "dance"},
            run_id="run-1",
        )
        gate = genre_gate.SweepGate(
            TAXONOMY,
            tracks=FailingReader(set()),
            standing=genre_gate.StandingHolds(store),
            lookup=never_asked,
        )
        found = listing(installed, rnb, [FakeRelease("r1")], gate=gate, owned={"r1"})
        assert (found.candidates, found.gated, found.released) == ((), (), ())
        assert found.stale == ("r1",)
        # And the source that made the listing drops the hold it names.
        source = sweep.LabelSource(
            installed,
            registry=labels.Registry(labels={SLUG: rnb}),
            artists={SLUG: FakePagedArtist([FakeRelease("r1")])},
            verify=lambda claimed, release: {"verdict": "confirmed"},
            store=store,
            owned={"r1"},
            gate=gate,
        )
        assert source.list_recent(10) == []
        assert review.holds(store, queue=Queue.LABEL_RELEASE) == ()


def test_a_returned_hold_the_queue_does_not_hold_is_filed_and_never_judged(installed):
    with review.open_store(installed) as store:
        held = hold_one(store, "r1")
        review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=held.item_id)
        gate = genre_gate.SweepGate(
            TAXONOMY,
            tracks=FailingReader(set()),
            standing=genre_gate.StandingHolds(store),
            lookup=never_asked,
        )
        found = listing(installed, ENTRY, [FakeRelease("r1")], gate=gate)
    assert [one.identity for one in found.candidates] == ["r1"]
    assert found.candidates[0].payload["genre_gate"] == "returned"
    assert found.gated == () and found.released == ()


def test_a_hold_whose_words_cannot_be_read_back_stays_held(installed):
    with review.open_store(installed) as store:
        review.hold(
            store,
            queue=Queue.LABEL_RELEASE,
            kind=sweep.KIND,
            identity={"release_id": "r1"},
            payload={"identity": "r1"},
            group=SLUG,
            name=LABEL,
            reason="held on words nobody can read now",
            detail={},
            run_id="run-1",
        )
        gate = genre_gate.SweepGate(
            TAXONOMY,
            tracks=FailingReader(set()),
            standing=genre_gate.StandingHolds(store),
            lookup=never_asked,
        )
        found = listing(
            installed,
            labels.LabelEntry(label_id=SLUG, name=LABEL, kind="christian"),
            [FakeRelease("r1")],
            gate=gate,
        )
    assert found.candidates == ()
    [one] = found.gated
    assert one.standing is True
    assert one.judged.reason == "held on words nobody can read now"


def test_a_listing_with_no_gate_files_every_candidate_unstamped(installed):
    found = listing(installed, ENTRY, [FakeRelease("r1")], gate=None)
    assert [one.identity for one in found.candidates] == ["r1"]
    assert "genre_gate" not in found.candidates[0].payload
    assert found.gated == ()


def test_a_held_release_and_a_queued_one_both_take_a_place(installed):
    gate = genre_gate.SweepGate(
        TAXONOMY,
        tracks=lambda rid: ((Track("1", "A", "One", isrc(int(rid[1:]))),), 2026),
        lookup=Lookup({isrc(4): ("Christian",), isrc(2): ("Dance",), isrc(1): ("Dance",)}),
    )
    releases = [FakeRelease(f"r{n}", year=str(2020 + n)) for n in (4, 3, 2, 1)]
    found = listing(installed, ENTRY, releases, gate=gate, offered={"r3"}, limit=3)
    assert [one.candidate.identity for one in found.gated] == ["r4"]
    assert found.held == 1
    assert [one.identity for one in found.candidates] == ["r2"]
    assert found.beyond == 1


# ═══════════════════════════════════════════════════════════════════════════
# 5. The registry carries a label's kind
# ═══════════════════════════════════════════════════════════════════════════


def test_a_kind_is_stored_folded_listed_and_survives_a_rename_and_an_unrelated_edit(installed):
    register("--kind", "RnB")
    assert labels.RegistryStore().load().by_id(SLUG).kind == "rnb"
    labels.RegistryStore().rename(SLUG, "Tide Works Recordings")
    labels.RegistryStore().edit(SLUG, track_limit=25)
    labels.RegistryStore().edit(SLUG, match="tide")
    entry = labels.RegistryStore().load().by_id(SLUG)
    assert (entry.kind, entry.track_limit, entry.match) == ("rnb", 25, "tide")
    code, envelope = drive(["label", "registry", "list"])
    assert code == int(ExitCode.OK), envelope
    assert "kind rnb" in envelope["data"]["checks"][0]["detail"]
    assert envelope["data"]["summary"]["labels"][0]["kind"] == "rnb"


def test_a_label_with_no_kind_says_none_and_lists_none(installed):
    register()
    assert labels.RegistryStore().load().by_id(SLUG).kind is None
    _code, envelope = drive(["label", "registry", "list"])
    assert "kind" not in envelope["data"]["checks"][0]["detail"]
    assert envelope["data"]["summary"]["labels"][0]["kind"] is None


def test_a_kind_the_taxonomy_does_not_name_is_refused_and_nothing_is_written(installed):
    register()
    before = labels.RegistryStore().path.read_bytes()
    code, envelope = drive(["label", "registry", "set", LABEL, "--kind", "polka"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-name-invalid"
    assert "'polka' is not a kind the library's taxonomy names" in envelope["cause"]["message"]
    assert "rnb" in envelope["cause"]["detail"]["kinds"]
    assert "any" in envelope["cause"]["detail"]["kinds"]
    assert labels.RegistryStore().path.read_bytes() == before
    code, envelope = drive(["label", "registry", "add", "New Label", "--kind", "polka"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert labels.RegistryStore().load().by_name("New Label") is None


def test_the_word_default_clears_a_kind_back_to_none(installed):
    """So the label follows the taxonomy's default again, whatever that becomes."""
    register("--kind", "rnb")
    code, envelope = drive(["label", "registry", "set", LABEL, "--kind", "default"])
    assert code == int(ExitCode.OK), envelope
    assert labels.RegistryStore().load().by_id(SLUG).kind is None
    register("--kind", "rnb")
    register("--kind", "default")
    assert labels.RegistryStore().load().by_id(SLUG).kind is None
    # A kind of None still means "keep what is held", as for every field.
    register("--kind", "rnb")
    labels.RegistryStore().edit(SLUG, track_limit=5)
    assert labels.RegistryStore().load().by_id(SLUG).kind == "rnb"


def test_a_kind_alone_is_a_field_set_can_change(installed):
    register()
    code, envelope = drive(["label", "registry", "set", LABEL, "--kind", "any"])
    assert code == int(ExitCode.OK), envelope
    assert labels.RegistryStore().load().by_id(SLUG).kind == "any"


def test_a_verb_that_sets_no_field_refuses_a_kind(installed):
    register()
    code, envelope = drive(["label", "registry", "remove", LABEL, "--kind", "rnb"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "--kind" in envelope["cause"]["message"]
    assert labels.RegistryStore().load().by_id(SLUG) is not None


@pytest.mark.parametrize("value", ["", "  ", "two words", "r&b", "-dance"])
def test_a_kind_that_is_not_one_word_refuses_at_the_store(installed, value):
    register()
    with pytest.raises(Exception) as caught:
        labels.RegistryStore().edit(SLUG, kind=value)
    assert "kind" in str(caught.value)
    assert labels.RegistryStore().load().by_id(SLUG).kind is None


def test_a_registry_written_before_kinds_existed_reads_with_none(installed):
    register()
    path = labels.RegistryStore().path
    raw = json.loads(path.read_text(encoding="utf-8"))
    del raw["labels"][SLUG]["kind"]
    path.write_text(json.dumps(raw), encoding="utf-8")
    assert labels.RegistryStore().load().by_id(SLUG).kind is None


# ═══════════════════════════════════════════════════════════════════════════
# 6. ``label approved`` judges kind with the same words
# ═══════════════════════════════════════════════════════════════════════════


def accept(cfg: config.Config, release_id: str, *, label_id: str = SLUG, **stamp) -> str:
    with review.open_store(cfg) as store:
        item = sweep.offer_release(
            store,
            run.Candidate(
                identity=release_id,
                recency="2026",
                payload={
                    "artist": "Label Act",
                    "title": f"Release {release_id}",
                    "label_id": label_id,
                    "label_name": LABEL,
                    "identity": release_id,
                    **stamp,
                },
            ),
        )
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="suite")
    return item.item_id


def approved_check(envelope: dict, key: str) -> dict:
    return check(envelope, f"label.approved.{key}")


def listed_ids(envelope: dict) -> list[str]:
    path = envelope["data"]["summary"]["list"]
    return [t["id"] for t in json.loads(Path(path).read_text())["tracks"]] if path else []


def provider_of(monkeypatch, releases: dict[str, str]) -> FakeCatalogue:
    fake = FakeCatalogue(
        releases={
            rid: ([Track(f"t-{rid}", f"Artist {rid}", f"Song {rid}", code)], 2026)
            for rid, code in releases.items()
        }
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    return fake


def test_an_accepted_release_of_another_kind_is_held_at_approval_on_the_recorded_words(
    installed, monkeypatch
):
    """R18. Judged on the words the sweep recorded, with nobody asked again."""
    register()
    accept(installed, "r-dance", published_genres=["Dance"])
    accept(installed, "r-christian", published_genres=["Christian"])
    provider_of(monkeypatch, {"r-dance": isrc(1), "r-christian": isrc(2)})
    bind_lookup(monkeypatch, never_asked)

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-dance"]
    line = approved_check(envelope, "held.r-christian")["detail"]
    assert "release r-christian ('Release r-christian' on Tide Works) is HELD by the genre gate" in line
    assert "which is christian and not dance" in line
    assert "crate label registry set LABEL --kind KIND" in line
    [held] = envelope["data"]["summary"]["held"]
    assert (held["release_id"], held["genres"], held["kind"]) == (
        "r-christian",
        ["Christian"],
        "dance",
    )
    assert "1 accepted release(s) held by the genre gate" in approved_check(envelope, "held")["detail"]
    # The dance release was judged, so only the share rule's line would fail it.
    assert approved_check(envelope, "ungated")["status"] == "ok"


def test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval(
    installed, monkeypatch
):
    register()
    accept(installed, "r-old")
    fake = provider_of(monkeypatch, {"r-old": isrc(9)})
    lookup = Lookup({isrc(9): ("Christian",)})
    bind_lookup(monkeypatch, lookup)

    code, envelope = drive(["label", "approved"])

    assert lookup.asked == [isrc(9)]
    # One provider read: the rows the verb already had are what the gate used.
    assert fake.releases_asked_for == ["r-old"]
    assert listed_ids(envelope) == []
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-old"]
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"


def test_a_release_neither_rule_could_judge_is_listed_and_says_what_each_lacked(
    installed, monkeypatch
):
    register()
    accept(installed, "r-unknown")
    provider_of(monkeypatch, {"r-unknown": isrc(9)})
    bind_lookup(monkeypatch, Lookup({}))

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-unknown"]
    ungated = approved_check(envelope, "ungated")
    assert ungated["status"] == "fail"
    assert (
        "the catalogue reports no genre for it, and the general catalogue does not know "
        "its tracks"
    ) in ungated["detail"]
    assert envelope["data"]["summary"]["ungated"] == ["r-unknown"]


def test_a_release_the_kind_rule_passed_is_judged_though_its_rows_report_no_genre(
    installed, monkeypatch
):
    register()
    accept(installed, "r-dance")
    provider_of(monkeypatch, {"r-dance": isrc(1)})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Electro",)}))

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-dance"]
    assert approved_check(envelope, "ungated")["status"] == "ok"
    assert envelope["data"]["summary"]["ungated"] == []


def test_a_returned_release_is_listed_at_approval_and_not_judged_again(installed, monkeypatch):
    register()
    bind(monkeypatch, {"r-christian": ("2025", isrc(2))})
    bind_lookup(monkeypatch, Lookup({isrc(2): ("Christian",)}))
    sweep_once()
    held_verb("return", "r-christian")
    item = filed(installed)["r-christian"]
    with review.open_store(installed) as store:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="suite")
    bind_lookup(monkeypatch, never_asked)

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-christian"]
    assert envelope["data"]["summary"]["held"] == []
    assert envelope["data"]["summary"]["ungated"] == []


def test_a_returned_mark_on_the_payload_alone_is_believed(installed, monkeypatch):
    """A queue moved to another machine carries the payload and not the hold."""
    register()
    accept(installed, "r-christian", published_genres=["Christian"], genre_gate="returned")
    provider_of(monkeypatch, {"r-christian": isrc(2)})
    bind_lookup(monkeypatch, never_asked)
    _code, envelope = drive(["label", "approved"])
    assert listed_ids(envelope) == ["t-r-christian"]
    assert envelope["data"]["summary"]["held"] == []


def test_approval_judges_by_the_kind_the_label_has_now(installed, monkeypatch):
    register("--kind", "christian")
    accept(installed, "r-christian", published_genres=["Christian"])
    accept(installed, "r-dance", published_genres=["Dance"])
    provider_of(monkeypatch, {"r-christian": isrc(2), "r-dance": isrc(1)})
    bind_lookup(monkeypatch, never_asked)
    _code, envelope = drive(["label", "approved"])
    assert listed_ids(envelope) == ["t-r-christian"]
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-dance"]


def test_a_release_on_a_label_the_registry_no_longer_holds_is_the_default_kind(
    installed, monkeypatch
):
    accept(installed, "r-christian", label_id="gone-label", published_genres=["Christian"])
    provider_of(monkeypatch, {"r-christian": isrc(2)})
    bind_lookup(monkeypatch, never_asked)
    _code, envelope = drive(["label", "approved"])
    [held] = envelope["data"]["summary"]["held"]
    assert (held["release_id"], held["kind"]) == ("r-christian", "dance")


def test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time(
    installed, monkeypatch
):
    """The review's case. A release filed before the gate existed is accepted,
    held at approval, and was never held by a sweep, so no hold names it."""
    register()
    item_id = accept(installed, "r-old")
    provider_of(monkeypatch, {"r-old": isrc(9)})
    bind_lookup(monkeypatch, Lookup({isrc(9): ("Christian",)}))
    _code, envelope = drive(["label", "approved"])
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-old"]
    assert "crate label held return r-old" in approved_check(envelope, "held.r-old")["detail"]

    code, envelope = held_verb("return", "r-old")

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"] == {
        "returned": [],
        "marked": ["r-old"],
        "already_returned": [],
    }
    assert "is already in review" in check(envelope, "label.held.release.r-old")["detail"]
    # Nothing was filed a second time and the acceptance stands.
    assert [(one.item_id, one.verdict) for one in filed(installed).values()] == [
        (item_id, review.Verdict.ACCEPTED)
    ]
    assert held_ids(installed) == []
    assert held_ids(installed, states=(review.HOLD_RETURNED,)) == ["r-old"]

    bind_lookup(monkeypatch, never_asked)
    code, envelope = drive(["label", "approved"])
    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-old"]
    assert envelope["data"]["summary"]["held"] == []

    code, envelope = held_verb("return", "r-old")
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["already_returned"] == ["r-old"]


def test_the_catalogue_is_not_asked_about_a_release_the_library_already_holds(
    installed, monkeypatch
):
    """Every accepted release is read on every run, the downloaded ones too."""
    register()
    accept(installed, "r-kept")
    accept(installed, "r-missing")
    provider_of(monkeypatch, {"r-kept": isrc(1), "r-missing": isrc(2)})
    (installed.library.root / "Music" / "Artist r-kept - Song r-kept.flac").write_bytes(b"")
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)})
    bind_lookup(monkeypatch, lookup)

    code, envelope = drive(["label", "approved"])

    assert code == int(ExitCode.OK), envelope
    assert lookup.asked == [isrc(2)]
    assert listed_ids(envelope) == ["t-r-missing"]
    assert envelope["data"]["summary"]["held"] == []
    assert envelope["data"]["summary"]["owned"] == 1
    assert (
        "every track of it is already in the library, so the general catalogue was "
        "not asked about it"
    ) in approved_check(envelope, "ungated")["detail"]


def test_an_owned_release_is_still_judged_on_words_the_sweep_recorded(installed, monkeypatch):
    """That costs no request, and its line says held and not unjudged."""
    register()
    accept(installed, "r-own", published_genres=["Christian"])
    provider_of(monkeypatch, {"r-own": isrc(1)})
    (installed.library.root / "Music" / "Artist r-own - Song r-own.flac").write_bytes(b"")
    bind_lookup(monkeypatch, never_asked)
    _code, envelope = drive(["label", "approved"])
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-own"]


def test_an_unreadable_registry_refuses_approval_before_the_provider_is_resolved(
    installed, monkeypatch
):
    """A label's kind decides what is held, so the registry is read first."""
    register()
    accept(installed, "r-1")
    labels.RegistryStore().path.write_text("{ not json", encoding="utf-8")

    def never(_cfg):
        raise AssertionError("the provider was resolved")

    monkeypatch.setattr(catalogue, "resolve", never)
    code, envelope = drive(["label", "approved"])
    assert code != int(ExitCode.OK), envelope
    assert "label" in envelope["cause"]["reason"]


def test_a_catalogue_that_refuses_at_approval_holds_nothing_and_lists_the_release(
    installed, monkeypatch
):
    register()
    accept(installed, "r-1")
    provider_of(monkeypatch, {"r-1": isrc(1)})
    bind_lookup(monkeypatch, Lookup({isrc(1): "blocked"}))
    code, envelope = drive(["label", "approved"])
    assert code == int(ExitCode.OK), envelope
    assert listed_ids(envelope) == ["t-r-1"]
    assert envelope["data"]["summary"]["held"] == []
    assert "could not be read (blocked)" in approved_check(envelope, "ungated")["detail"]
