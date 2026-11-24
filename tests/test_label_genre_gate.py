"""R-798: the label genre gate judges a release by kind, at sweep time."""

from __future__ import annotations

import copy
import json
import tomllib
from importlib import resources

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
from tests.test_label_approved import listed_ids
from tests.test_label_genre import registry
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture
from tests.test_label_workers import queued_sweep

LABEL = "Tide Works"
SLUG = "tide-works"

#: The general catalogue's 27 top level words and their kinds, written out so a drift fails.
MEASURED = {
    "Pop": "pop", "Rap/Hip Hop": "hip_hop", "Reggaeton": "latin", "Rock": "rock", "Dance": "dance",
    "R&B": "rnb", "Alternative": "rock", "Christian": "christian", "Electro": "dance",
    "Folk": "folk_country", "Reggae": "reggae", "Jazz": "jazz", "Country": "folk_country",
    "Salsa": "latin", "Traditional Mexicano": "latin", "Classical": "classical",
    "Films/Games": "soundtrack", "Metal": "rock", "Soul & Funk": "rnb", "African Music": "world",
    "Asian Music": "world", "Blues": "jazz", "Brazilian Music": "latin", "Cumbia": "latin",
    "Indian Music": "world", "Kids": "kids", "Latin Music": "latin",
}

TAXONOMY = default_taxonomy()
#: What a held release is reported by, and a sweep's counts in ``label held``.
HELD_KEYS = ("release_id", "genres", "kind")
SWEEP_COUNTS = ("filed", "asked", "not_judged", "unread", "held")


def isrc(n: int) -> str:
    """A well formed ISRC nobody was issued."""
    return f"ZZTST26{n:05d}"


class Track:
    def __init__(self, track_id: str, artist: str, name: str, code: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = code


class Lookup:
    """The general catalogue as a table: ISRC to published words, or to an answer."""

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


def serve(monkeypatch, fake, lookup=None):
    """``fake`` as the provider, and ``lookup`` as the general catalogue when one is given."""
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    if lookup is not None:
        bind_lookup(monkeypatch, lookup)
    return fake


class Provider(FakeCatalogue):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verified: list[str] = []

    def search_release(self, claimed, release):
        self.verified.append(str(release.id))
        return super().search_release(claimed, release)


def bind(monkeypatch, releases: dict[str, tuple[str, str]], **kwargs) -> Provider:
    """One label whose releases are ``{id: (year, isrc)}``, one track each."""
    listed = [FakeRelease(rid, year=year) for rid, (year, _) in releases.items()]
    rows = {rid: ([Track(f"t-{rid}", "Label Act", f"Release {rid}", code)], int(year))
            for rid, (year, code) in releases.items()}
    return serve(monkeypatch, Provider(artists={SLUG: FakePagedArtist(listed)}, releases=rows,
                                       **kwargs))


def register(*argv: str, name: str = LABEL) -> None:
    registry("add", name, *argv)


def swept(monkeypatch, releases=None, lookup=None, *, argv=(), **kwargs) -> Provider:
    """Register with ``argv``, bind ``releases`` and ``lookup`` (one Christian), sweep once."""
    register(*argv)
    fake = bind(monkeypatch, releases or {"r-christian": ("2025", isrc(2))}, **kwargs)
    bind_lookup(monkeypatch, lookup or Lookup({isrc(2): ("Christian",)}))
    sweep_once()
    return fake


def held_ok(*argv: str) -> dict:
    code, envelope = held_verb(*argv)
    assert code == int(ExitCode.OK), envelope
    return envelope


def approved_ok() -> dict:
    code, envelope = drive(["label", "approved"])
    assert code == int(ExitCode.OK), envelope
    return envelope


def standing_gate(store) -> genre_gate.SweepGate:
    """A gate over the store's standing holds that reads and asks nothing."""
    return genre_gate.SweepGate(
        TAXONOMY, tracks=FailingReader(set()), standing=genre_gate.StandingHolds(store),
        lookup=never_asked,
    )


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


def returns(**said: list[str]) -> dict:
    """The summary of ``label held return``, each list empty but those given."""
    return {"returned": [], "marked": [], "already_returned": [], **said}


def check(envelope: dict, key: str) -> dict:
    found = [one for one in envelope["data"]["checks"] if one["key"] == key]
    assert len(found) == 1, (key, [one["key"] for one in envelope["data"]["checks"]])
    return found[0]


def tracks(*numbers: int) -> list[Track]:
    """One track per number, each with that number's ISRC."""
    return [Track(str(n), "A", f"T{n}", isrc(n)) for n in numbers]


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


@pytest.mark.parametrize(
    ("words", "kinds"),
    [
        pytest.param(("CHRISTIAN", "  christian "), ("christian",) * 2, id="whatever-its-case"),
        pytest.param(("", None), (None, None), id="empty-is-no-kind"),
        # Both words contain a needle of a later rule: "dance" and "reggae".
        pytest.param(("Dancehall/Ragga", "Reggaeton"), ("reggae", "latin"), id="first-rule-wins"),
        pytest.param(
            ("Rhythm & Blues", "Rhythm and Blues", "Blues"), ("rnb", "rnb", "jazz"),
            id="long-rnb-is-not-the-blues-it-contains",
        ),
    ],
)
def test_a_published_word_is_matched_to_its_kind(words, kinds):
    assert tuple(routing.published_kind(TAXONOMY, word) for word in words) == kinds


PASS, HOLD, NOT_JUDGED = KindVerdict.PASS, KindVerdict.HOLD, KindVerdict.NOT_JUDGED


@pytest.mark.parametrize(
    ("kind", "words", "verdict", "placed", "says"),
    [
        pytest.param(None, ["Pop", "Dance"], PASS, (("Pop", "pop"), ("Dance", "dance")), (),
                     id="one-word-of-the-labels-kind-passes-a-release-listing-another-too"),
        pytest.param(None, ["Zydeco"], NOT_JUDGED, None, ("no rule of the gate knows", "Zydeco"),
                     id="a-word-no-rule-knows-is-not-judged-and-never-held"),
        pytest.param(None, ["Zydeco", "Christian"], HOLD, (("Christian", "christian"),),
                     ("which is christian and not dance",),
                     id="an-unknown-word-does-not-save-a-release-a-known-word-places-elsewhere"),
        pytest.param(None, [], NOT_JUDGED, None, "the general catalogue publishes no genre for it",
                     id="a-release-with-no-published-word-is-not-judged"),
        pytest.param("rnb", ["R&B"], PASS, None, (), id="an-rnb-label-passes-rnb"),
        pytest.param(None, ["R&B"], HOLD, None, (), id="the-default-kind-holds-rnb"),
        pytest.param("rnb", ["Dance"], HOLD, None, (), id="an-rnb-label-holds-dance"),
        pytest.param("polka", ["Christian"], NOT_JUDGED, None, ("'polka'", "does not name"),
                     id="a-kind-the-taxonomy-does-not-name-is-not-judged-and-says-which"),
    ],
)
def test_the_labels_kind_decides_what_its_releases_words_do(kind, words, verdict, placed, says):
    """``says`` is the reason's fragments, or as a string the whole reason."""
    judged = routing.kind_verdict(TAXONOMY, kind, words)
    assert judged.verdict is verdict
    if placed is not None:
        assert judged.placed == placed
    if isinstance(says, str):
        assert judged.reason == says
    for said in () if isinstance(says, str) else says:
        assert said in judged.reason


def test_a_label_followed_for_any_kind_passes_without_a_word():
    for genres in ([], ["Christian"], ["Zydeco"]):
        judged = routing.kind_verdict(TAXONOMY, "any", genres)
        assert judged.verdict is KindVerdict.PASS
        assert judged.kind == "any"
    assert routing.kind_settled(TAXONOMY, "any").verdict is KindVerdict.PASS


def test_a_label_with_no_kind_is_the_declared_default():
    assert routing.label_kind(TAXONOMY, None) == "dance"
    assert routing.label_kind(TAXONOMY, "") == "dance"
    assert routing.label_kind(TAXONOMY, " RNB ") == "rnb"
    assert routing.kind_settled(TAXONOMY, None) is None


@pytest.fixture(scope="module")
def default_raw() -> dict:
    source = resources.files("cratekit") / "templates" / "taxonomy.default.toml"
    return tomllib.loads(source.read_text(encoding="utf-8"))


def built_from(raw: dict, change):
    """The taxonomy built from a copy of ``raw`` with ``change`` made to its label gate."""
    data = copy.deepcopy(raw)
    change(data["label_gate"])
    return build_taxonomy(data)


def test_the_shipped_template_declares_the_default_kind_and_its_kinds():
    gate = TAXONOMY.label_gate
    assert gate.default_kind == "dance"
    assert set(gate.kinds) == set(MEASURED.values())
    assert "any" not in gate.kinds


def _published(rule):
    return lambda gate: gate["published"].append(rule)


def _gate(key, value):
    return lambda gate: gate.__setitem__(key, value)


def _says(default_raw, change, said):
    """Whether the gate with ``change`` made is refused by one problem saying all of ``said``."""
    with pytest.raises(TaxonomyError) as caught:
        built_from(default_raw, change)
    parts = (said,) if isinstance(said, str) else said
    return any(all(part in p for part in parts) for p in caught.value.problems)


@pytest.mark.parametrize(
    ("change", "said"),
    [
        pytest.param(
            _published({"kind": "polka"}),
            ("[[label_gate.published]]", "needs all_of, any_of, or equals"), id="rule-no-matcher",
        ),
        pytest.param(_published({"any_of": ["polka"]}), "needs a kind", id="rule-no-kind"),
        pytest.param(
            _published({"any_of": ["polka"], "kind": "any"}), "cannot be the kind of a word",
            id="rule-reserved-kind",
        ),
        pytest.param(
            _published({"any_of": "polka", "kind": "polka"}), "any_of must be a list of words",
            id="matcher-not-a-list",
        ),
        pytest.param(
            _gate("published", {"any_of": ["polka"], "kind": "polka"}), "two pairs of brackets",
            id="rules-in-one-pair-of-brackets",
        ),
        pytest.param(
            _gate("default_kind", "polka"), "default_kind 'polka' is not a kind",
            id="default-kind-no-rule-names",
        ),
        pytest.param(_gate("default_kind", 7), "default_kind must be", id="default-not-a-word"),
        pytest.param(
            _published({"any_of": ["polka"], "kind": "default"}), "clears a label's kind",
            id="rule-kind-is-the-clearing-word",
        ),
        # The registry stores a kind as one word, so a rule may name no other shape.
        pytest.param(
            _published({"any_of": ["polka"], "kind": "hip hop"}), "kind 'hip hop' is not one word",
            id="rule-kind-of-two-words",
        ),
        pytest.param(
            _gate("default_kind", "hip hop"), "default_kind must be", id="default-of-two-words"
        ),
    ],
)
def test_a_malformed_label_gate_is_refused_by_what_it_lacks(default_raw, change, said):
    assert _says(default_raw, change, said)


def test_a_share_rule_needle_typed_with_a_capital_matches_too(default_raw):
    """Both rule tables are folded when loaded and matched by one function."""
    rules = [{"any_of": ["Gqom"], "family": "gqom"}, {"equals": ["Kwaito"], "family": "kwaito"}]
    built = built_from(default_raw, lambda gate: gate["rule"].extend(rules))
    assert routing.gate_family(built, "gqom") == "gqom"
    assert routing.gate_family(built, "KWAITO") == "kwaito"


def test_every_shipped_kind_is_one_the_registry_will_store():
    for kind in (*TAXONOMY.label_gate.kinds, "any"):
        assert labels.check_kind(kind) == kind


def test_a_default_of_any_is_allowed(default_raw):
    assert built_from(default_raw, _gate("default_kind", "any")).label_gate.default_kind == "any"


def test_a_needle_typed_with_a_capital_still_matches(default_raw):
    built = built_from(default_raw, _published({"equals": ["Zydeco"], "kind": "Folk_Country"}))
    assert routing.published_kind(built, "zydeco") == "folk_country"


def test_a_copy_written_before_the_gate_had_published_rules_loads_and_judges_nothing(default_raw):
    built = built_from(default_raw, lambda gate: (gate.pop("published"), gate.pop("default_kind")))
    assert built.label_gate.published == ()
    assert built.label_gate.default_kind == "dance"
    judged = routing.kind_verdict(built, None, ["Christian"])
    assert judged.verdict is KindVerdict.NOT_JUDGED
    assert "declares no rule" in judged.reason
    assert routing.kind_settled(built, None) is not None


KNOWN_NO_GENRE = "the general catalogue knows it and publishes no genre for it"


@pytest.mark.parametrize(
    ("table", "rows", "words", "asked"),
    [
        pytest.param({2: ("Christian",), 3: ("Dance",)}, tracks(1, 2, 3),
                     {"genres": ("Christian",), "answer": "matched"}, [1, 2],
                     id="the-first-track-that-answers-with-a-genre-is-the-releases-answer"),
        pytest.param({4: ("Dance",)}, tracks(1, 2, 3, 4, 5),
                     {"genres": (), "answer": "miss",
                      "why_none": "the general catalogue does not know its tracks"}, [1, 2, 3],
                     id="no-more-than-three-tracks-are-asked-about"),
        pytest.param({}, [{"isrc": isrc(1)}, Track("2", "A", "Two", isrc(1)), {"isrc": isrc(2)}],
                     {}, [1, 2], id="a-row-is-a-mapping-or-an-object-and-an-isrc-is-asked-once"),
        pytest.param({1: ()}, tracks(1), {"answer": "matched", "why_none": KNOWN_NO_GENRE}, None,
                     id="a-match-that-publishes-no-genre-says-that-and-not-a-miss"),
        pytest.param({1: ()}, tracks(1, 2), {"answer": "matched", "why_none": KNOWN_NO_GENRE}, None,
                     id="a-track-the-catalogue-knows-outranks-one-it-does-not"),
        pytest.param({1: ("Dance",)}, [{"external_ids": {"isrc": isrc(1)}}], {"genres": ("Dance",)},
                     [1], id="an-isrc-under-external-ids-is-asked-about"),
    ],
)
def test_a_releases_words_are_what_the_tracks_asked_about_publish(table, rows, words, asked):
    assert genre_gate.TRACKS_ASKED == 3
    lookup = Lookup({isrc(n): said for n, said in table.items()})
    got = genre_gate.published_words(rows, lookup)
    assert {name: getattr(got, name) for name in words} == words
    if asked is not None:
        assert lookup.asked == [isrc(n) for n in asked]


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


def test_a_track_the_catalogue_knows_outranks_one_it_does_not_whatever_the_order():
    rows = [Track("1", "A", "One", isrc(1)), Track("2", "A", "Two", "not an isrc")]
    words = genre_gate.published_words(
        rows,
        lambda value: published.Published(
            published.SOURCE, "no-isrc" if "not" in str(value) else "miss"
        ),
    )
    assert words.answer == "miss"


@pytest.mark.parametrize(
    ("table", "count", "verdict", "judged", "asked"),
    [
        # One track's ISRC can sit on a compilation of another kind.
        pytest.param({1: ("Pop",), 2: ("Dance",), 3: ("Christian",)}, 3, PASS,
                     {"genres": ("Pop", "Dance")}, [1, 2],
                     id="a-release-that-would-be-held-is-asked-about-again-before-it-is"),
        pytest.param({1: ("Dance",), 2: ("Christian",)}, 2, PASS, {}, [1],
                     id="a-release-whose-first-track-passes-asks-about-no-other"),
        pytest.param({n: ("Christian",) for n in (1, 2, 3, 4)}, 4, HOLD,
                     {"genres": ("Christian",)}, [1, 2, 3],
                     id="a-release-is-held-only-when-every-track-asked-agrees"),
        pytest.param({1: ("Christian",), 2: "blocked"}, 3, NOT_JUDGED,
                     {"answer": "blocked", "genres": ()}, [1, 2],
                     id="a-catalogue-that-refuses-after-a-would-be-hold-holds-nothing"),
    ],
)
def test_a_release_is_judged_on_as_many_tracks_as_settle_it(table, count, verdict, judged, asked):
    lookup = Lookup({isrc(n): said for n, said in table.items()})
    rows = tracks(*range(1, count + 1))
    got = genre_gate.judge_rows(TAXONOMY, None, rows, genre_gate.Asking(lookup))
    assert got.verdict is verdict
    assert {name: getattr(got, name) for name in judged} == judged
    assert lookup.asked == [isrc(n) for n in asked]


def test_three_releases_unread_in_a_row_end_the_asking_and_an_answer_resets_it():
    """Unread answers are not remembered by the lookup, so three in a row end the asking."""
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
    # The literal: the two names are one object, so X equals X would hold for any word.
    assert sweep.KIND == "label-release"
    assert genre_gate.RELEASE_KIND == "label-release"
    assert genre_gate.release_item_id("r1") == review.item_id_for(
        "label-release", "label-release", {"release_id": "r1"}
    )


class FailingReader:
    """A release reader that fails for the releases named, has lost the ``gone``, counts reads."""

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
        return (Track("1", "A", "One", isrc(1)),), 2026, None


ENTRY = labels.LabelEntry(label_id=SLUG, name=LABEL)


class Flaky(FakeCatalogue):
    """The provider over a ``FailingReader``, recording each release asked for."""

    def __init__(self, failing: set[str], gone: set[str] = frozenset()) -> None:
        super().__init__()
        self.reader = FailingReader(failing, gone)

    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        return self.reader(release_id)


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
    """A read for the ownership question, which the gate never sees, still ends a run."""
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


def hold_one(store, release_id: str, *, run_id: str = "run-1", reason: str = "held", **kwargs):
    """A hold on ``release_id``, a Christian release of a dance label unless ``kwargs`` say."""
    fields = {"payload": {"identity": release_id, "title": f"Release {release_id}"}, "group": SLUG,
              "name": LABEL, "detail": {"genres": ["Christian"], "kind": "dance"}, **kwargs}
    return review.hold(store, queue=Queue.LABEL_RELEASE, kind=sweep.KIND,
                       identity={"release_id": release_id}, reason=reason, run_id=run_id, **fields)


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
        every = review.holds(store, queue=Queue.LABEL_RELEASE, states=review.HOLD_STATES)
        assert [one.state for one in every] == [review.HOLD_RETURNED]


def test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one(installed):
    with review.open_store(installed) as store:
        one, two = hold_one(store, "r1"), hold_one(store, "r2")
        review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id)
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id=one.item_id) is True
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id) is False
        assert review.release_hold(store, queue=Queue.LABEL_RELEASE, item_id="rv_none") is False
        assert review.find_hold(store, queue=Queue.LABEL_RELEASE, item_id=one.item_id) is None
        kept = review.find_hold(store, queue=Queue.LABEL_RELEASE, item_id=two.item_id)
        assert kept.state == review.HOLD_RETURNED


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


def test_a_release_of_another_kind_is_held_and_counted_for_its_label(installed, monkeypatch):
    """AE5. A dance label, a release the general catalogue calls Christian."""
    releases = {"r-dance": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))}
    swept(monkeypatch, releases, Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)}))
    assert list(filed(installed)) == ["r-dance"]
    assert held_ids(installed) == ["r-christian"]
    [row] = grouped("label")
    assert (row["label"], row["items"], row["held"]) == (SLUG, 1, 1)
    [by_run] = grouped("run")
    assert (by_run["items"], by_run["held"]) == (1, 1)
    envelope = held_ok()
    said = check(envelope, "label.held.held")["detail"]
    assert "1 release(s) held by the genre gate across 1 label(s)" in said
    assert check(envelope, f"label.held.label.{SLUG}")["detail"] == (
        "Tide Works: 1 held, 1 the general catalogue calls Christian"
    )
    line = check(envelope, "label.held.release.r-christian")["detail"]
    assert "release r-christian ('Release r-christian' by Label Act) on Tide Works is held" in line
    assert "which is christian and not dance, the kind its label is followed as" in line
    assert "crate label held return r-christian" in line
    [release] = envelope["data"]["summary"]["releases"]
    assert [release[key] for key in HELD_KEYS] == ["r-christian", ["Christian"], "dance"]
    # Not rejected: no tombstone of any kind was written.
    assert DecisionStore(tombstone.STORE_KEY, installed).suppressions(include_revoked=True) == ()


ABSENT = object()


@pytest.mark.parametrize(
    ("releases", "lookup", "argv", "stamped", "note"),
    [
        pytest.param({"r-dance": ("2026", isrc(1))}, Lookup({isrc(1): ("Electro", "Pop")}), (),
                     {"genre_gate": "passed", "genre_gate_answer": "matched",
                      "published_genres": ["Electro", "Pop"]}, "Electro, Pop",
                     id="the-gate-passed-it-and-on-which-words"),
        pytest.param({"r-unknown": ("2026", isrc(1))}, Lookup({}), (),
                     {"genre_gate": "not-judged", "genre_gate_answer": "miss",
                      "genre_gate_note": "the general catalogue does not know its tracks",
                      "published_genres": ABSENT}, "",
                     id="the-catalogue-does-not-know-it-so-it-is-marked-not-judged"),
        pytest.param(None, never_asked, ("--kind", "any"),
                     {"genre_gate": "passed", "genre_gate_answer": "not-asked",
                      "genre_gate_note": "its label is followed for any kind of music"}, "",
                     id="a-label-followed-for-any-kind-files-everything-and-asks-nothing"),
    ],
)
def test_a_filed_release_says_what_the_gate_made_of_it(
    installed, monkeypatch, releases, lookup, argv, stamped, note
):
    swept(monkeypatch, releases, lookup, argv=argv)
    [item] = filed(installed).values()
    assert {key: item.payload.get(key, ABSENT) for key in stamped} == stamped
    assert note in item.payload["genre_gate_note"]
    assert item.verdict is None
    assert held_ids(installed) == []


def test_the_labels_kind_decides_what_is_filed(installed, monkeypatch):
    """AE6. An R&B release is filed from an R&B label and held from a dance one."""
    register("--kind", "rnb")
    register(name="Salt Flats")
    fake = Provider(
        artists={SLUG: FakePagedArtist([FakeRelease("r-a")]),
                 "salt-flats": FakePagedArtist([FakeRelease("r-b")])},
        releases={"r-a": ([Track("1", "A", "One", isrc(1))], 2026),
                  "r-b": ([Track("2", "A", "One", isrc(1))], 2026)},
    )
    serve(monkeypatch, fake, Lookup({isrc(1): ("R&B",)}))
    sweep_once()
    assert list(filed(installed)) == ["r-a"]
    assert held_ids(installed) == ["r-b"]
    assert {row["label"]: row["held"] for row in grouped("label")} == {SLUG: 0, "salt-flats": 1}


def test_a_held_release_returned_to_review_is_filed_and_not_held_again(installed, monkeypatch):
    lookup = Lookup({isrc(1): ("Dance",), isrc(2): ("Christian",)})
    releases = {"r-dance": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))}
    fake = swept(monkeypatch, releases, lookup)
    [first] = [row["run"] for row in grouped("run")]
    envelope = held_ok("return", "r-christian")
    assert envelope["data"]["summary"] == returns(returned=["r-christian"])
    item = filed(installed)["r-christian"]
    assert item.verdict is None
    assert item.payload["genre_gate"] == "returned"
    assert (item.payload["title"], item.payload["label_id"]) == ("Release r-christian", SLUG)
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
    swept(monkeypatch)
    held_verb("return", "r-christian")
    before = filed(installed)["r-christian"]
    envelope = held_ok("return", "r-christian")
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"] == returns(already_returned=["r-christian"])
    assert filed(installed)["r-christian"].payload == before.payload


def test_returning_a_release_nothing_holds_refuses_and_files_none_of_the_others(
    installed, monkeypatch
):
    swept(monkeypatch)
    code, envelope = held_verb("return", "r-christian", "r-typo")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "review-item-unknown"
    assert envelope["cause"]["detail"]["unknown"] == ["r-typo"]
    assert filed(installed) == {}
    assert held_ids(installed) == ["r-christian"]


def test_return_needs_a_release_and_a_listing_takes_none(installed):
    for argv in (("return",), ("list", "r-1")):
        code, envelope = held_verb(*argv)
        assert code == int(ExitCode.PRECONDITION), envelope
        assert envelope["cause"]["reason"] == "review-selection-invalid"


def test_a_labels_kind_changed_after_a_hold_releases_what_now_fits(installed, monkeypatch):
    releases = {"r-rnb": ("2026", isrc(1)), "r-christian": ("2025", isrc(2))}
    fake = swept(monkeypatch, releases, Lookup({isrc(1): ("R&B",), isrc(2): ("Christian",)}))
    assert filed(installed) == {}
    assert sorted(held_ids(installed)) == ["r-christian", "r-rnb"]
    registry("set", LABEL, "--kind", "rnb")
    # NO REQUEST: the second sweep judges the holds on the words they recorded.
    bind_lookup(monkeypatch, never_asked)
    verified, read = list(fake.verified), list(fake.releases_asked_for)
    sweep_once()
    assert list(filed(installed)) == ["r-rnb"]
    assert held_ids(installed) == ["r-christian"]
    # Nothing verified again; the one read asks whether the library came to own it.
    assert fake.verified == verified
    assert fake.releases_asked_for == [*read, "r-rnb"]
    payload = filed(installed)["r-rnb"].payload
    assert (payload["genre_gate"], payload["published_genres"]) == ("passed", ["R&B"])
    # Filed under the releasing sweep; the standing hold counts under its first sweep.
    by_run = {row["run"]: (row["items"], row["held"]) for row in grouped("run")}
    assert sorted(by_run.values()) == [(0, 1), (1, 0)]
    assert by_run[payload[sweep.SWEEP_RUN]] == (1, 0)
    # The hold that stands says the kind it is now held against.
    with review.open_store(installed) as store:
        [standing] = review.holds(store, queue=Queue.LABEL_RELEASE)
    assert "not rnb" in standing.reason
    assert standing.detail["kind"] == "rnb"


def test_a_catalogue_unread_on_every_release_holds_nothing_and_says_so(installed, monkeypatch):
    lookup = Lookup({isrc(1): "blocked", isrc(2): "blocked"})
    swept(monkeypatch, {"r-1": ("2026", isrc(1)), "r-2": ("2025", isrc(2))}, lookup)
    assert sorted(filed(installed)) == ["r-1", "r-2"]
    assert held_ids(installed) == []
    for item in filed(installed).values():
        assert item.payload["genre_gate"] == "not-judged"
        assert item.payload["genre_gate_answer"] == "blocked"
        assert "could not be read (blocked)" in item.payload["genre_gate_note"]
    envelope = held_ok()
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "fail"
    assert (
        "the general catalogue could not be read for any of the 2 release(s) the newest "
        "sweep of Tide Works asked it about"
    ) in line["detail"]
    assert "HELD NOTHING" in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert [row[key] for key in SWEEP_COUNTS] == [2, 2, 2, 2, 0]


def test_a_sweep_that_judged_some_and_not_others_says_how_many(installed, monkeypatch):
    releases = {"r-1": ("2026", isrc(1)), "r-2": ("2025", isrc(2)), "r-3": ("2024", isrc(3))}
    swept(monkeypatch, releases, Lookup({isrc(1): ("Dance",), isrc(3): ("Christian",)}))
    envelope = held_ok()
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "info"
    assert "filed 2 release(s) and the genre gate could not judge 1 of them" in line["detail"]
    assert "could not be read" not in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert [row[key] for key in SWEEP_COUNTS] == [2, 3, 1, 0, 1]


def test_a_sweep_the_gate_judged_in_full_has_no_sweep_line(installed, monkeypatch):
    swept(monkeypatch, {"r-1": ("2026", isrc(1))}, Lookup({isrc(1): ("Dance",)}))
    _code, envelope = held_verb()
    assert [one["key"] for one in envelope["data"]["checks"]] == ["label.held.held"]


def test_a_sweep_that_holds_some_releases_files_no_more_than_the_window(installed, monkeypatch):
    """R-790's window: a held release takes a place, so nothing is read past it."""
    releases = {f"r-{n}": (str(2020 + n), isrc(n)) for n in (6, 5, 4, 3, 2, 1)}
    lookup = Lookup({isrc(n): ("Christian",) if n > 4 else ("Dance",) for n in range(1, 7)})
    fake = swept(monkeypatch, releases, lookup, argv=("--offer", "3"))
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
    lookup = Lookup({isrc(1): ("Dance",), isrc(2): ("Dance",)})
    releases = {"r-2": ("2026", isrc(2)), "r-1": ("2025", isrc(1))}
    fake = swept(monkeypatch, releases, lookup, confirmed={"r-1"})
    assert list(filed(installed)) == ["r-1"]
    assert lookup.asked == [isrc(1)]
    assert fake.releases_asked_for == ["r-1"]
    sweep_once()
    assert lookup.asked == [isrc(1)]


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
    active_copy_without_published_rules(installed)
    swept(monkeypatch, lookup=never_asked)
    payload = filed(installed)["r-christian"].payload
    assert payload["genre_gate"] == "not-judged"
    assert "declares no rule" in payload["genre_gate_note"]
    assert held_ids(installed) == []
    envelope = registry("set", LABEL, "--kind", "rnb", code=ExitCode.PRECONDITION)
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
    releases = {"r-2": ("2025", isrc(2)), "r-1": ("2024", isrc(1))}
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Christian",)})
    swept(monkeypatch, releases, lookup, argv=("--offer", "3"))
    assert sorted(held_ids(installed)) == ["r-1", "r-2"]
    bind(monkeypatch, {"r-3": ("2026", isrc(3)), **releases}, confirmed=set())
    job_id = queued_sweep()
    code, resumed = drive(["sync", "labels", "--job", job_id])
    assert code != int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        [item] = jobs.items(store, job_id)
    assert item.cause.reason == "label-sweep-incomplete"
    assert sorted(held_ids(installed)) == ["r-1", "r-2"]


def test_an_unreachable_catalogue_is_given_up_on_once_for_the_whole_sweep(installed, monkeypatch):
    """One job, two labels. The outage is counted across them, not per label."""
    register()
    register(name="Salt Flats")
    fake = Provider(
        artists={
            slug: FakePagedArtist([FakeRelease(f"{p}-{n}", year=f"{2027 - n}") for n in (1, 2)])
            for slug, p in ((SLUG, "a"), ("salt-flats", "b"))
        },
        releases={
            rid: ([Track(f"t-{rid}", "Label Act", f"Release {rid}", isrc(n))], 2026)
            for n, rid in enumerate(("a-1", "a-2", "b-1", "b-2"), start=1)
        },
    )
    lookup = Lookup({isrc(n): "unreachable" for n in (1, 2, 3, 4)})
    serve(monkeypatch, fake, lookup)
    sweep_once()
    assert lookup.asked == [isrc(1), isrc(2), isrc(3)]
    assert sorted(filed(installed)) == ["a-1", "a-2", "b-1", "b-2"]
    last = filed(installed)["b-2"].payload
    assert (last["genre_gate"], last["genre_gate_answer"]) == ("not-judged", "not-asked")
    assert "3 releases in a row" in last["genre_gate_note"]
    assert held_ids(installed) == []


def test_a_release_with_no_isrc_does_not_hide_a_sweep_the_catalogue_refused_throughout(
    installed, monkeypatch
):
    """It was never asked about, so it is not one of the questions that went unread."""
    swept(
        monkeypatch, {"r-1": ("2026", isrc(1)), "r-2": ("2025", "")}, Lookup({isrc(1): "blocked"}),
    )
    _code, envelope = held_verb()
    line = check(envelope, f"label.held.sweep.{SLUG}")
    assert line["status"] == "fail"
    assert "any of the 1 release(s)" in line["detail"]
    [row] = envelope["data"]["summary"]["sweeps"]
    assert (row["filed"], row["asked"], row["not_judged"], row["unread"]) == (2, 1, 2, 1)


def test_a_hold_the_window_no_longer_reaches_is_dropped_when_it_stops_holding(
    installed, monkeypatch
):
    """Newer releases push a held one past the window."""
    older = {"r-1": ("2025", isrc(1))}
    lookup = Lookup({isrc(1): ("R&B",), isrc(2): ("Dance",)})
    swept(monkeypatch, older, lookup, argv=("--offer", "1"))
    assert held_ids(installed) == ["r-1"]
    bind(monkeypatch, {"r-2": ("2026", isrc(2)), **older})
    sweep_once()
    # Still a dance label: the newer release is filed and the hold stands past the window.
    assert list(filed(installed)) == ["r-2"]
    assert held_ids(installed) == ["r-1"]
    drive(["label", "registry", "set", LABEL, "--kind", "rnb"])
    bind_lookup(monkeypatch, never_asked)
    sweep_once()
    assert held_ids(installed) == []
    # Not filed either: past the window, counted there like any unexamined release.
    assert list(filed(installed)) == ["r-2"]
    [row] = grouped("label")
    assert (row["items"], row["held"], row["beyond"]) == (1, 0, 1)


def test_a_held_release_deleted_on_purpose_since_is_held_no_longer(installed, monkeypatch):
    swept(monkeypatch)
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
    swept(monkeypatch)
    _code, envelope = held_verb()
    assert "no longer followed" not in check(envelope, "label.held.release.r-christian")["detail"]
    drive(["label", "registry", "remove", LABEL])
    _code, envelope = held_verb()
    assert (
        "its label is no longer followed, so no sweep will judge it again"
        in check(envelope, "label.held.release.r-christian")["detail"]
    )


def listing(cfg, entry, releases, *, gate, offered=None, limit=None, owned=None):
    return sweep.list_for_label(
        cfg, entry, artist=FakePagedArtist(releases),
        verify=lambda claimed, release: {"verdict": "confirmed"}, offered=offered, owned=owned,
        limit=limit, gate=gate,
    )


def test_a_hold_in_force_on_a_release_already_in_the_queue_is_dropped(installed):
    """A process that dies between filing a release and dropping its hold leaves both."""
    with review.open_store(installed) as store:
        hold_one(store, "r1")
        gate = standing_gate(store)
        found = listing(installed, ENTRY, [FakeRelease("r1")], gate=gate, offered={"r1"})
    assert found.held == 1
    assert (found.candidates, found.gated) == ((), ())
    assert found.stale == ("r1",)


def test_a_released_hold_the_library_came_to_own_is_dropped_and_not_filed(installed):
    rnb = labels.LabelEntry(label_id=SLUG, name=LABEL, kind="rnb")
    with review.open_store(installed) as store:
        hold_one(store, "r1", reason="held while the label was a dance label",
                 payload={"identity": "r1"}, detail={"genres": ["R&B"], "kind": "dance"})
        gate = standing_gate(store)
        found = listing(installed, rnb, [FakeRelease("r1")], gate=gate, owned={"r1"})
        assert (found.candidates, found.gated, found.released) == ((), (), ())
        assert found.stale == ("r1",)
        # And the source that made the listing drops the hold it names.
        source = sweep.LabelSource(
            installed, registry=labels.Registry(labels={SLUG: rnb}),
            artists={SLUG: FakePagedArtist([FakeRelease("r1")])},
            verify=lambda claimed, release: {"verdict": "confirmed"}, store=store, owned={"r1"},
            gate=gate,
        )
        assert source.list_recent(10) == []
        assert review.holds(store, queue=Queue.LABEL_RELEASE) == ()


def test_a_returned_hold_the_queue_does_not_hold_is_filed_and_never_judged(installed):
    with review.open_store(installed) as store:
        held = hold_one(store, "r1")
        review.return_hold(store, queue=Queue.LABEL_RELEASE, item_id=held.item_id)
        gate = standing_gate(store)
        found = listing(installed, ENTRY, [FakeRelease("r1")], gate=gate)
    assert [one.identity for one in found.candidates] == ["r1"]
    assert found.candidates[0].payload["genre_gate"] == "returned"
    assert found.gated == () and found.released == ()


def test_a_hold_whose_words_cannot_be_read_back_stays_held(installed):
    with review.open_store(installed) as store:
        hold_one(store, "r1", reason="held on words nobody can read now",
                 payload={"identity": "r1"}, detail={})
        gate = standing_gate(store)
        found = listing(
            installed, labels.LabelEntry(label_id=SLUG, name=LABEL, kind="christian"),
            [FakeRelease("r1")], gate=gate,
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
        TAXONOMY, tracks=lambda rid: ((Track("1", "A", "One", isrc(int(rid[1:]))),), 2026, None),
        lookup=Lookup({isrc(4): ("Christian",), isrc(2): ("Dance",), isrc(1): ("Dance",)}),
    )
    releases = [FakeRelease(f"r{n}", year=str(2020 + n)) for n in (4, 3, 2, 1)]
    found = listing(installed, ENTRY, releases, gate=gate, offered={"r3"}, limit=3)
    assert [one.candidate.identity for one in found.gated] == ["r4"]
    assert found.held == 1
    assert [one.identity for one in found.candidates] == ["r2"]
    assert found.beyond == 1


def test_a_kind_is_stored_folded_listed_and_survives_a_rename_and_an_unrelated_edit(installed):
    register("--kind", "RnB")
    assert labels.RegistryStore().load().by_id(SLUG).kind == "rnb"
    labels.RegistryStore().rename(SLUG, "Tide Works Recordings")
    labels.RegistryStore().edit(SLUG, track_limit=25)
    labels.RegistryStore().edit(SLUG, match="tide")
    entry = labels.RegistryStore().load().by_id(SLUG)
    assert (entry.kind, entry.track_limit, entry.match) == ("rnb", 25, "tide")
    envelope = registry("list")
    assert "kind rnb" in envelope["data"]["checks"][0]["detail"]
    assert envelope["data"]["summary"]["labels"][0]["kind"] == "rnb"


def test_a_label_with_no_kind_says_none_and_lists_none(installed):
    register()
    assert labels.RegistryStore().load().by_id(SLUG).kind is None
    envelope = registry("list")
    assert "kind" not in envelope["data"]["checks"][0]["detail"]
    assert envelope["data"]["summary"]["labels"][0]["kind"] is None


def test_a_kind_the_taxonomy_does_not_name_is_refused_and_nothing_is_written(installed):
    register()
    before = labels.RegistryStore().path.read_bytes()
    envelope = registry("set", LABEL, "--kind", "polka", code=ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "label-name-invalid"
    assert "'polka' is not a kind the library's taxonomy names" in envelope["cause"]["message"]
    assert "rnb" in envelope["cause"]["detail"]["kinds"]
    assert "any" in envelope["cause"]["detail"]["kinds"]
    assert labels.RegistryStore().path.read_bytes() == before
    registry("add", "New Label", "--kind", "polka", code=ExitCode.PRECONDITION)
    assert labels.RegistryStore().load().by_name("New Label") is None


def test_the_word_default_clears_a_kind_back_to_none(installed):
    """So the label follows the taxonomy's default again, whatever that becomes."""
    register("--kind", "rnb")
    registry("set", LABEL, "--kind", "default")
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
    registry("set", LABEL, "--kind", "any")
    assert labels.RegistryStore().load().by_id(SLUG).kind == "any"


def test_a_verb_that_sets_no_field_refuses_a_kind(installed):
    register()
    envelope = registry("remove", LABEL, "--kind", "rnb", code=ExitCode.PRECONDITION)
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


def accept(cfg: config.Config, *release_ids: str, label_id: str = SLUG, **stamp) -> str:
    """Each release offered as the sweep files it, then accepted. The last item id."""
    with review.open_store(cfg) as store:
        for release_id in release_ids:
            payload = {
                "artist": "Label Act", "title": f"Release {release_id}", "label_id": label_id,
                "label_name": LABEL, "identity": release_id, **stamp,
            }
            candidate = run.Candidate(identity=release_id, recency="2026", payload=payload)
            item_id = sweep.offer_release(store, candidate).item_id
            review.resolve(store, item_id, review.Verdict.ACCEPTED, actor="suite")
    return item_id


def approved_check(envelope: dict, key: str) -> dict:
    return check(envelope, f"label.approved.{key}")


def provider_of(monkeypatch, releases: dict[str, str], lookup=None) -> FakeCatalogue:
    """The provider's ``{id: isrc}`` releases bound, and ``lookup`` when given."""
    return serve(monkeypatch, FakeCatalogue(releases={
        rid: ([Track(f"t-{rid}", f"Artist {rid}", f"Song {rid}", code)], 2026)
        for rid, code in releases.items()
    }), lookup)


def test_an_accepted_release_of_another_kind_is_held_at_approval_on_the_recorded_words(
    installed, monkeypatch
):
    """R18. Judged on the words the sweep recorded, with nobody asked again."""
    register()
    accept(installed, "r-dance", published_genres=["Dance"])
    accept(installed, "r-christian", published_genres=["Christian"])
    provider_of(monkeypatch, {"r-dance": isrc(1), "r-christian": isrc(2)}, never_asked)
    envelope = approved_ok()
    assert listed_ids(envelope) == ["t-r-dance"]
    line = approved_check(envelope, "held.r-christian")["detail"]
    said = "release r-christian ('Release r-christian' on Tide Works) is HELD by the genre gate"
    assert said in line
    assert "which is christian and not dance" in line
    assert "crate label registry set LABEL --kind KIND" in line
    [held] = envelope["data"]["summary"]["held"]
    assert [held[key] for key in HELD_KEYS] == ["r-christian", ["Christian"], "dance"]
    held_line = approved_check(envelope, "held")["detail"]
    assert "1 accepted release(s) held by the genre gate" in held_line
    # The dance release was judged, so only the share rule's line would fail it.
    assert approved_check(envelope, "ungated")["status"] == "ok"


def test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval(
    installed, monkeypatch
):
    register()
    accept(installed, "r-old")
    lookup = Lookup({isrc(9): ("Christian",)})
    fake = provider_of(monkeypatch, {"r-old": isrc(9)}, lookup)
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
    provider_of(monkeypatch, {"r-unknown": isrc(9)}, Lookup({}))
    envelope = approved_ok()
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
    provider_of(monkeypatch, {"r-dance": isrc(1)}, Lookup({isrc(1): ("Electro",)}))
    envelope = approved_ok()
    assert listed_ids(envelope) == ["t-r-dance"]
    assert approved_check(envelope, "ungated")["status"] == "ok"
    assert envelope["data"]["summary"]["ungated"] == []


def test_a_returned_release_is_listed_at_approval_and_not_judged_again(installed, monkeypatch):
    swept(monkeypatch)
    held_verb("return", "r-christian")
    item = filed(installed)["r-christian"]
    with review.open_store(installed) as store:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="suite")
    bind_lookup(monkeypatch, never_asked)
    envelope = approved_ok()
    assert listed_ids(envelope) == ["t-r-christian"]
    assert (envelope["data"]["summary"]["held"], envelope["data"]["summary"]["ungated"]) == ([], [])


def test_a_returned_mark_on_the_payload_alone_is_believed(installed, monkeypatch):
    """A queue moved to another machine carries the payload and not the hold."""
    register()
    accept(installed, "r-christian", published_genres=["Christian"], genre_gate="returned")
    provider_of(monkeypatch, {"r-christian": isrc(2)}, never_asked)
    _code, envelope = drive(["label", "approved"])
    assert listed_ids(envelope) == ["t-r-christian"]
    assert envelope["data"]["summary"]["held"] == []


def test_approval_judges_by_the_kind_the_label_has_now(installed, monkeypatch):
    register("--kind", "christian")
    accept(installed, "r-christian", published_genres=["Christian"])
    accept(installed, "r-dance", published_genres=["Dance"])
    provider_of(monkeypatch, {"r-christian": isrc(2), "r-dance": isrc(1)}, never_asked)
    _code, envelope = drive(["label", "approved"])
    assert listed_ids(envelope) == ["t-r-christian"]
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-dance"]


def test_a_release_on_a_label_the_registry_no_longer_holds_is_the_default_kind(
    installed, monkeypatch
):
    accept(installed, "r-christian", label_id="gone-label", published_genres=["Christian"])
    provider_of(monkeypatch, {"r-christian": isrc(2)}, never_asked)
    _code, envelope = drive(["label", "approved"])
    [held] = envelope["data"]["summary"]["held"]
    assert (held["release_id"], held["kind"]) == ("r-christian", "dance")


def test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time(
    installed, monkeypatch
):
    register()
    item_id = accept(installed, "r-old")
    provider_of(monkeypatch, {"r-old": isrc(9)}, Lookup({isrc(9): ("Christian",)}))
    _code, envelope = drive(["label", "approved"])
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-old"]
    assert "crate label held return r-old" in approved_check(envelope, "held.r-old")["detail"]
    envelope = held_ok("return", "r-old")
    assert envelope["data"]["summary"] == returns(marked=["r-old"])
    assert "is already in review" in check(envelope, "label.held.release.r-old")["detail"]
    # Nothing was filed a second time and the acceptance stands.
    assert [(one.item_id, one.verdict) for one in filed(installed).values()] == [
        (item_id, review.Verdict.ACCEPTED)
    ]
    assert held_ids(installed) == []
    assert held_ids(installed, states=(review.HOLD_RETURNED,)) == ["r-old"]
    bind_lookup(monkeypatch, never_asked)
    envelope = approved_ok()
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
    accept(installed, "r-kept", "r-missing")
    lookup = Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)})
    provider_of(monkeypatch, {"r-kept": isrc(1), "r-missing": isrc(2)}, lookup)
    (installed.library.root / "Music" / "Artist r-kept - Song r-kept.flac").write_bytes(b"")
    envelope = approved_ok()
    assert lookup.asked == [isrc(2)]
    assert listed_ids(envelope) == ["t-r-missing"]
    assert (envelope["data"]["summary"]["held"], envelope["data"]["summary"]["owned"]) == ([], 1)
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
    provider_of(monkeypatch, {"r-1": isrc(1)}, Lookup({isrc(1): "blocked"}))
    envelope = approved_ok()
    assert listed_ids(envelope) == ["t-r-1"]
    assert envelope["data"]["summary"]["held"] == []
    assert "could not be read (blocked)" in approved_check(envelope, "ungated")["detail"]
