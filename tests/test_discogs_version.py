"""U318: a remix takes a Discogs release and its genre only when that release carries
its version.

At sitting 101 "Two Months Off (Tim Green Remix)" took release 8532080 and "As You Fly
(Mita Gami Extended Mix)" the 16BL remix single, 28513768, since the match read a title
by its core alone. Guarded: a file naming a version takes only a release that writes it,
on a track or, for a single, its own title or a track that is the version alone; a file
that matched before still does unless it names an unwritten version ("Extended Mix" and
"Original Mix" are noise); the miss says why; Beatport, Traxsource and Bandcamp are
unchanged. Offline; the titles are the sitting's, the artist a fixture.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.core import tags
from cratekit.tagging import searchers, tag, titles
from tests._containers import synth_container
from tests.test_catalogue_searcher import BUCKET_GENRE, _beatport_page, _beatport_track
from tests.test_discogs_searcher import discogs_answer, release, results, routed, searcher

#: The fixture artist every release and file here is credited to.
ARTIST = "Fixture Artist"

#: The sitting's two releases as hand built payloads, none holding the file's mix.
TWO_MONTHS_OFF = 8532080
TWO_MONTHS_OFF_TRACKS = (
    "Two Months Off", "Two Months Off (Radio Edit)", "Two Months Off (Dark Lane Remix)",
    "Two Months Off (Sunfold Dub)",
)
AS_YOU_FLY = 28513768
AS_YOU_FLY_TRACKS = ("As You Fly (16BL Remix)", "As You Fly (16BL Dub)")


def listed(*titles_: str) -> list[dict]:
    return [
        {"position": f"A{index}", "type_": "track", "title": title}
        for index, title in enumerate(titles_, 1)
    ]


def pressings(titled: dict[int, tuple[str, ...]], *, artist: str = ARTIST, styles=None):
    """A fetch whose search names each release, ``titled`` by its title then its tracks."""
    releases = {}
    for number, (title, *tracks) in titled.items():
        more = {"styles": styles[number]} if styles and number in styles else {}
        listing = listed(*tracks)
        releases[number] = release(number, artist=artist, title=title, tracks=listing, **more)
    return routed(search=results(*titled), releases=releases)


def asked(title: str, number: int, *, release_title: str = "An EP", tracks: tuple[str, ...]):
    """Discogs' answer for ``title`` by :data:`ARTIST`, naming release ``number`` of ``tracks``."""
    fetch = pressings({number: (release_title, *tracks)})
    return discogs_answer(searcher(fetch)(ARTIST, title))


def matched(title: str, *, release_title: str = "An EP", tracks: tuple[str, ...]) -> bool:
    return asked(title, 5, release_title=release_title, tracks=tracks).answer == "matched"


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


# ═══ A. The sitting's two files ════════════════════════════════════════════


TIM_GREEN = ("Two Months Off (Tim Green Remix)", TWO_MONTHS_OFF, "Two Months Off")
MITA_GAMI = ("As You Fly (Mita Gami Extended Mix)", AS_YOU_FLY, "As You Fly")


@pytest.mark.parametrize(
    ("head", "sitting", "tracks", "note"),
    [
        pytest.param(
            "", TIM_GREEN, TWO_MONTHS_OFF_TRACKS,
            "Discogs release 8532080 holds no track with this version (tim green)",
            id="the-tim-green-remix-refuses-a-release-of-four-other-mixes"),
        pytest.param(
            "", MITA_GAMI, AS_YOU_FLY_TRACKS,
            "Discogs release 28513768 holds no track with this version (mita gami)",
            id="the-mita-gami-extended-mix-refuses-the-16bl-remix-single"),
        # Headed as the library writes them, they refuse too.
        pytest.param("04A - 126 - ", TIM_GREEN, TWO_MONTHS_OFF_TRACKS, None, id="headed-tim-green"),
        pytest.param(
            "09B - 122 - [MP3] ", MITA_GAMI, AS_YOU_FLY_TRACKS, None, id="headed-mita-gami"),
    ])
def test_the_sitting_files_refuse_a_release_that_lacks_their_mix(head, sitting, tracks, note):
    title, number, release_title = sitting
    said = asked(head + title, number, release_title=release_title, tracks=tracks)
    assert said.answer == "miss"
    if note is not None:
        assert said.note == note


def test_each_sitting_file_still_takes_a_release_that_carries_its_mix():
    assert matched(
        "Two Months Off (Tim Green Remix)", release_title="Two Months Off",
        tracks=(*TWO_MONTHS_OFF_TRACKS, "Two Months Off (Tim Green Remix)"))
    assert matched(
        "As You Fly (Mita Gami Extended Mix)", release_title="As You Fly",
        tracks=("As You Fly (Mita Gami Remix)",),
    ), "the extended form of a remix is that remix, as the reader sheds Extended"


def test_the_refused_file_is_left_untagged_with_the_reason_in_its_record(tmp_path, silence):
    path = tmp_path / "two months off.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(
        path, {"artist": ARTIST, "title": "04A - 126 - Two Months Off (Tim Green Remix)"})
    fetch = pressings({TWO_MONTHS_OFF: ("Two Months Off", *TWO_MONTHS_OFF_TRACKS)})
    result = tag.tag_one(path, searcher=searcher(fetch))
    assert result.genre_written is None
    assert tags.read_genre_from_file(path) in (None, "")
    (discogs,) = [said for said in result.answers if said.source == searchers.DISCOGS]
    assert (discogs.answer, discogs.note) == (
        "miss", "Discogs release 8532080 holds no track with this version (tim green)")
    # The walk goes on to Beatport, as after any Discogs miss.
    (beatport,) = [said for said in result.answers if said.source == searchers.BEATPORT]
    assert beatport.answer == "miss"


def test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix():
    fetch = pressings(
        {1: ("Two Months Off", *TWO_MONTHS_OFF_TRACKS), 2: ("Remixes", TIM_GREEN[0])},
        styles={2: ("Techno",)})
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert said.answer == "matched"
    assert "release 2" in said.note


def test_the_miss_names_every_release_refused_for_its_version_and_no_other():
    fetch = pressings({
        1: ("Two Months Off", "Two Months Off"), 2: ("Other", "Another Song"),
        3: ("Two Months Off", "Two Months Off (B Remix)"),
    })
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert (said.answer, said.note) == (
        "miss",
        "Discogs release 1 holds no track with this version (tim green); "
        "Discogs release 3 holds no track with this version (tim green)",
    )


def test_a_plain_miss_still_carries_no_note():
    said = asked("Two Months Off (Tim Green Remix)", 9, tracks=("Another Song",))
    assert (said.answer, said.note) == ("miss", "")


def test_an_unread_release_beside_a_version_refusal_is_unread_not_a_miss():
    fetch = routed(
        search=results(1, 2),
        releases={
            1: release(1, artist=ARTIST, title="Two Months Off", tracks=listed("Two Months Off")),
            2: searchers.Fetched(text="<html>", status=200),
        })
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert said.answer not in ("miss", "matched")


# ═══ B. The brief's scenarios ══════════════════════════════════════════════


@pytest.mark.parametrize(
    ("title", "tracks", "taken"),
    [
        pytest.param("X (A Remix)", ("X", "X (B Remix)"), False, id="remix-of-plain-and-other"),
        pytest.param("X (A Remix)", ("X", "X (A Remix)"), True, id="remix-a-track-writes"),
        pytest.param("X", ("X",), True, id="no-version-takes-the-plain-recording"),
        pytest.param("X", ("X (Original Mix)",), True, id="no-version-takes-the-original-mix"),
        # Out of scope (R-1637 is Beatport's side of it): unchanged from main.
        pytest.param("X", ("X (A Remix)",), True, id="no-version-takes-remixes-only-as-before"),
        # A version of version words alone names no other mix and matches as before.
        pytest.param("X (Extended Mix)", ("X (Original Mix)",), True, id="extended-takes-original"),
        pytest.param("X (Extended Mix)", ("X",), True, id="extended-takes-plain"),
        pytest.param("X (Original Mix)", ("X (Extended Mix)",), True, id="original-takes-extended"),
        pytest.param("X (Radio Edit)", ("X",), True, id="radio-edit-takes-plain"),
        pytest.param("X (2014 Remaster)", ("X",), True, id="remaster-takes-plain"),
        # A named mix after a description still names its maker.
        pytest.param("X (Tim Green Vocal Mix)", ("X",), False, id="named-vocal-mix-plain"),
        pytest.param("X (Tim Green Vocal Mix)", ("X (Tim Green Remix)",), True, id="named-vocal"),
        pytest.param("X (Main Tim Green Mix)", ("X (Dark Lane Mix)",), False, id="main-named-mix"),
    ])
def test_a_release_is_taken_only_for_the_version_it_writes(title, tracks, taken):
    assert matched(title, tracks=tracks) is taken


@pytest.mark.parametrize(
    ("release_title", "tracks", "taken"),
    [
        pytest.param("X", ("X",), False, id="refuses-a-one-track-release-of-the-title"),
        pytest.param("X", ("Original Mix",), False, id="refuses-a-one-track-original"),
        pytest.param("X", ("Original Mix", "A Remix"), True, id="takes-a-track-of-the-version"),
        pytest.param("X", ("Original Mix", "B Remix"), False, id="refuses-another-version-alone"),
        pytest.param("X (A Remix)", ("Side One",), True, id="takes-its-own-title-writing-it"),
        pytest.param("X (B Remix)", ("Side One",), False, id="refuses-its-own-title-writing-other"),
    ])
def test_the_single_fallback_takes_only_a_release_that_writes_the_version(
        release_title, tracks, taken):
    assert matched("X (A Remix)", release_title=release_title, tracks=tracks) is taken


@pytest.mark.parametrize(
    "title",
    [
        "X (Main Mix)",
        "X (Vocal Mix)",
        "X - Vocal Mix",
        "X (Album Version)",
        'X (12" Version)',
        "X (12 Inch Mix)",
        "X (Short Edit)",
        "X (Clean Edit)",
        "X (Extended Vocal Mix)",
    ])
def test_a_mix_that_names_no_one_still_takes_the_plain_title(title):
    """A mix description (``titles.MIX_DESCRIPTIONS``) names no other mix."""
    assert matched(title, tracks=("X",))


@pytest.mark.parametrize(
    ("title", "track"),
    [
        ("X (A Remix)", "X - A Remix"),
        ("X - A Remix", "X (A Remix)"),
        ("X (A Remix)", "X [A Remix]"),
        ("X (A Remix)", "X (A Remix) (Extended)"),
        ("X (A Remix)", "X (A Remix) [feat. Someone]"),
        ("X (A Extended Remix)", "X (A Remix)"),
        ("X (feat. Someone) (A Remix)", "X (A Remix)"),
        ("X (A Remix) - 08A - 124", "X (A Remix)"),
        ("08A - 124 - X (A Remix)", "X (A Remix)"),
        ("X (a remix)", "X (A REMIX)"),
        ("X (A Remix)", "X A Remix"),
    ])
def test_a_version_is_read_as_the_reader_reads_it_wherever_it_is_written(title, track):
    assert matched(title, tracks=(track,))


@pytest.mark.parametrize(
    ("title", "track"),
    [
        ("X (A Remix)", "X"),
        ("X (A Remix)", "X (B Remix)"),
        ("X (A Remix)", "X (Extended Mix)"),
        ("X (A Remix)", "X (AB Remix)"),
        ("X (A B Remix)", "X (B Remix)"),
        ("X (A 2020 Remix)", "X (A Remix)"),
        ("X - A Remix", "X"),
        ("08A - 124 - X (A Remix)", "X (Original Mix)"),
        ("X (A Remix) (Extended)", "X (B Remix)"),
    ])
def test_another_version_or_none_takes_nothing(title, track):
    assert not matched(title, tracks=(track,))


def test_an_artist_that_does_not_match_still_refuses_a_track_that_writes_the_version():
    fetch = pressings({4: ("X", "X (A Remix)")}, artist="Someone Else")
    assert discogs_answer(searcher(fetch)(ARTIST, "X (A Remix)")).answer == "miss"


# ═══ C. Nothing but Discogs changes ════════════════════════════════════════


def test_the_shared_matcher_still_reads_a_remix_as_its_title():
    """``titles.matches`` is unchanged, so the other sources read the row as they did."""
    assert searchers._title_matches(
        "Two Months Off (Tim Green Remix)", "Two Months Off", artist=ARTIST)


def test_beatport_is_unchanged_for_a_remix_against_the_plain_row():
    fetch = routed(
        search=results(),
        beatport=searchers.Fetched(
            text=_beatport_page(
                [_beatport_track(ARTIST, "Two Months Off", BUCKET_GENRE, mix="Original Mix")]),
            status=200,
        ))
    hit = searcher(fetch, token=None)(ARTIST, "Two Months Off (Tim Green Remix)")
    assert hit.genre == BUCKET_GENRE


# ═══ D. The two readers ════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("title", "named"),
    [
        ("Two Months Off (Tim Green Remix)", {("tim", "green")}),
        ("As You Fly (Mita Gami Extended Mix)", {("mita", "gami")}),
        ("04A - 126 - Two Months Off (Tim Green Remix)", {("tim", "green")}),
        ("Two Months Off - Tim Green Remix", {("tim", "green")}),
        ("Two Months Off - Tim Green Remix (Extended)", {("tim", "green")}),
        ("Two Months Off (Tim Green Remix) (Extended Mix)", {("tim", "green")}),
        ("Two Months Off (feat. Someone) (Tim Green Remix)", {("tim", "green")}),
        ("Two Months Off (Extended Tim Green Remix)", {("tim", "green")}),
        ("Two Months Off (Tim Green 2020 Remix)", {("tim", "green", "2020")}),
        (f"{ARTIST} - Album - 01 Two Months Off (Tim Green Remix)", {("tim", "green")}),
        # Version words alone, and what is no version at all, name nothing.
        ("Two Months Off", set()),
        ("Two Months Off (Extended Mix)", set()),
        ("Two Months Off (Original Mix)", set()),
        ("Two Months Off (Radio Edit)", set()),
        ("Two Months Off (Main Mix)", set()),
        ("Two Months Off (Vocal Mix)", set()),
        ("Two Months Off (Album Version)", set()),
        ("Two Months Off (Tim Green Vocal Mix)", {("tim", "green")}),
        ("Two Months Off (Mike's (Dub) Mix)", {("mike",)}),
        ("Two Months Off (2014 Remaster)", set()),
        ("Two Months Off (Remix)", set()),
        ("Two Months Off (Part 1)", set()),
        ("Two Months Off (feat. Someone)", set()),
        ("Two Months Off - Original Mix", set()),
        # Brackets alone are a title, never a version; a title naming nothing has none.
        ("(Sunrise Mood Extended Mix)", set()),
        ("(Kerri Chandler Remix) - Original Mix", set()),
        ("(Intro) (Tide Remix)", {("tide",)}),
        ("02 (Sunrise Mood Extended Mix)", set()),
        ("[MP3] (Sunrise Mood Extended Mix)", set()),
        (f"{ARTIST} - Sun Path - 02 (Sunrise Mood Extended Mix)", set()),
        ("007 (Tide Remix)", {("tide",)}),
        ("[MP3] Sunrise Mood (Tide Remix)", {("tide",)}),
        ("08A - 124 -  - Sunrise Mood Extended Mix", set()),
        # Only a list could cut an unbracketed version from its title.
        ("Two Months Off Tim Green Remix", set()),
        # An album after the artist's credit is no version of the title.
        (f"Two Months Off - {ARTIST} - Some Album Remix", set()),
        # An ambiguous name's splits carry its version already.
        (f"{ARTIST} - Sunrise Mood Tim Green Remix", set()),
        ("", set()),
    ])
def test_a_files_named_versions(title, named):
    assert titles.named_versions(titles.read_file(title, ARTIST)) == frozenset(named)


@pytest.mark.parametrize(
    ("row", "titled", "alone"),
    [
        # A row titled as the file writes the mix anywhere; alone, only the mix row does.
        ("Two Months Off (Tim Green Remix)", True, False),
        ("Two Months Off [Tim Green Remix]", True, False),
        ("Two Months Off - Tim Green Remix", True, False),
        ("Two Months Off - Tim Green Remix - Part 2", True, False),
        ("Two Months Off (Tim Green Remix) - 2014 Remaster", True, False),
        # A group ending a dash part before a non-version tail (the table's T19).
        ("Two Months Off (Tim Green Remix) - Part 2", True, False),
        ("Two Months Off (Tim Green Remix) (Extended)", True, False),
        ("Two Months Off (Tim Green Dub)", True, False),
        ("Two Months Off (Tim Green's Remix)", True, False),
        ("Two Months Off (TIM GREEN REMIX)", True, False),
        ("Two Months Off (Tim Green Rmx)", True, False),
        ("Two Months Off Tim Green Remix", True, False),
        ("Tim Green Remix", True, True),
        ("Tim Green Extended Mix", True, True),
        ("Tim Green Remix (Extended)", True, True),
        ("(Tim Green Remix)", True, True),
        ("Two Months Off", False, False),
        ("Two Months Off (Dark Lane Remix)", False, False),
        ("Two Months Off (Green Remix)", False, False),
        ("Two Months Off (Tim Green)", False, False),
        ("Two Months Off (Remixes)", False, False),
        ("Sun Path (Tim Green Remix)", True, False),
        ("Lost And Found Tim Green", False, False),
        ("Lost And Found Tim Green Dub", True, False),
        ("", False, False),
    ])
def test_a_catalogue_title_writes_a_version(row, titled, alone):
    named = frozenset({("tim", "green")})
    assert titles.writes_version(row, named, titled=True) is titled
    assert titles.writes_version(row, named, titled=False) is alone


def test_no_named_version_is_written_by_any_row():
    assert not titles.writes_version("Two Months Off (Tim Green Remix)", frozenset(), titled=True)


# ═══ E. Review round one: what names no one, folding, and the guards ═══════


def test_the_mix_descriptions_are_exactly_these():
    """Pinned word for word: a word out reads as a maker's name, a word in folds one away."""
    assert titles.MIX_DESCRIPTIONS == frozenset(
        {
            "album", "bonus", "beats", "beatless", "full", "length", "long", "main",
            "short", "single", "track", "intro", "outro", "part", "pt", "maxi", "ep",
            "lp", "inch", "7", "12", "1", "2", "3",
            "alternative", "clean", "dirty", "explicit", "censored", "digital",
            "digitally", "hi", "res", "mono", "stereo", "master", "mixed", "unmixed",
            "continuous", "new", "early", "first", "second", "final", "rough",
            "special", "unreleased", "promo", "re", "video", "tv", "film", "movie",
            "soundtrack", "dj", "tool", "uk", "us", "english", "spanish", "german",
            "french", "italian", "japanese",
            "vocal", "piano", "orchestral", "stripped", "ambient", "classic", "deep",
            "disco", "dance", "house",
        }
    )  # fmt: skip


#: Mixes of the plain title's own recording, the 147 labels round one drove.
SAME_RECORDING = (
    "LP Version|Album Version|Album Mix|Digital Remaster|2009 Digital Remaster|"
    "2009 Remastered Version|Remastered Version|Remastered 2009|2009 Remaster|"
    "2009 - Remaster|UK Radio Edit|US Radio Edit|Video Edit|Video Version|Video Mix|"
    "Re-Edit|Alternative Mix|Alternative Version|Alternate Version|Bonus Beats|Beats|"
    "Dub Version|Instrumental Version|Acapella Version|Edit|Short Version|Long Version|"
    "Full Version|Full Length Version|Extended Version|Extended Club Mix|"
    "Extended Vocal Mix|Club Vocal Mix|Classic Mix|Classic Vocal Mix|Deep Mix|Disco Mix|"
    "Dance Mix|House Mix|Special Version|Special Edit|Promo Edit|DJ Edit|DJ Mix|"
    "DJ Version|Unreleased Mix|Unreleased Version|Original Version|Original Extended Mix|"
    'Original Club Mix|Original 12" Mix|12" Version|7" Version|7 Inch Edit|12 Inch Mix|'
    "Single Version|Single Edit|Radio Mix|Radio Version|Original Radio Edit|"
    "Explicit Version|Clean Version|Clean Edit|Stereo Mix|Mono Version|Live Version|"
    "Live Edit|Acoustic Version|Piano Version|Orchestral Version|Stripped Version|"
    "Demo Version|Remix|Rework|VIP Mix|Beatless Mix|Ambient Mix|DJ Tool|Reprise|"
    "Vocal Edit|Vocal Version|Vocal Dub|Instrumental Edit|Instrumental Dub|"
    "Main Vocal Mix|Mixed|Bonus Track|Original|Extended|Instrumental|Dub|Club Mix|"
    "Radio Edit|Original Mix|Extended Mix|New Mix|New Version|Remix Edit|Remix Version|"
    "Remix Radio Edit|Extended Remix|Original Instrumental Mix|TV Mix|TV Version|"
    "Soundtrack Version|Film Version|Movie Version|Promo Mix|Promo Version|Master Mix|"
    "Final Mix|Rough Mix|Early Version|Early Mix|First Version|Second Version|"
    "Version 2|Mix 1|Mix 2|Pt. 2 Mix|Part 2 Mix|Japanese Version|English Version|"
    "Spanish Version|German Version|Maxi Version|Maxi Mix|Maxi Edit|EP Version|"
    "12'' Extended Mix|Extended 12\" Mix|Original 7\" Version|Remastered Album Version|"
    "Remastered LP Version|2011 Remastered Version|2011 - Remastered|Digitally Remastered|"
    "Digital Remastered Version|Mixed Version|Continuous Mix|Unmixed Version|"
    "Hi-Res Version|Stereo Version|Mono Mix|Mono Single Version|Original Mono Version"
).split("|")


@pytest.mark.parametrize("label", SAME_RECORDING)
def test_a_mix_of_the_same_recording_still_takes_the_album_track(label):
    assert matched(f"04A - 126 - Sunrise Mood ({label})", tracks=("Opener", "Sunrise Mood"))


def test_a_mix_named_by_a_word_no_list_holds_is_read_as_its_makers():
    """The recorded cost: a style word both lists lack reads as a maker, so the file misses."""
    assert not matched("Sunrise Mood (Juno Mix)", tracks=("Sunrise Mood",))


@pytest.mark.parametrize(
    ("title", "row"),
    [
        ("Sunrise Mood (Ame Remix)", "Sunrise Mood (Âme Remix)"),
        ("Sunrise Mood (Âme Remix)", "Sunrise Mood (Ame Remix)"),
        ("Sunrise Mood (Tide & Sun Remix)", "Sunrise Mood (Tide And Sun Remix)"),
        ("Sunrise Mood (Tim Green's Remix)", "Sunrise Mood (Tim Green Remix)"),
        ("Sunrise Mood (Tim Green Remix)", "Sunrise Mood (Tim Green Rmx)"),
        ("Sunrise Mood (Tim Green Rmx)", "Sunrise Mood (Tim Green Remix)"),
        ("Sunrise Mood (Main Tim Green Mix)", "Sunrise Mood (Tim Green Remix)"),
    ])
def test_a_maker_is_folded_as_a_name_is(title, row):
    assert matched(title, tracks=(row,))


def test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix():
    """Round one's finding 6: another title's remix is no evidence the single holds one."""
    assert not matched(
        "Sunrise Mood (Tide Remix)", release_title="Sunrise Mood",
        tracks=("Sunrise Mood", "Sun Path (Tide Remix)"))
    assert matched(
        "Sunrise Mood (Tide Remix)", release_title="Sunrise Mood",
        tracks=("Sunrise Mood", "(Tide Remix)"))


def test_a_row_written_as_the_file_is_written_matches_whatever_its_dash_parts():
    """Round one's finding 9: a version in a middle dash part is written."""
    for title in (
        "Two Months Off - Tim Green Remix - Part 2",
        "Two Months Off (Tim Green Remix) - Live",
        "Two Months Off - Tim Green Remix (Extended) - 2014 Remaster",
    ):
        assert matched(title, tracks=(title,)), title


@pytest.mark.parametrize(
    ("title", "artist", "named"),
    [
        # A part that credits the artist is no version of the title.
        ("Two Months Off - Culture Club - Album", "Culture Club", set()),
        # A later part's own groups are its version.
        ("Two Months Off - Extended Mix (Tim Green Remix)", ARTIST, {("tim", "green")}),
        # An ambiguous name's splits carry its version, so it names none here.
        (f"{ARTIST} - Vocal Mix (Tide Remix)", ARTIST, set()),
        # A stretch that ends in no version word is no version.
        ("Two Months Off (Tim Green Vocal)", ARTIST, set()),
        ("Two Months Off (Main Tim Green Mix)", ARTIST, {("tim", "green")}),
        ("Two Months Off (Tim Green's Remix)", ARTIST, {("tim", "green")}),
        ("Two Months Off (2009 Digital Remaster)", ARTIST, set()),
    ])
def test_what_a_title_names_as_its_mix(title, artist, named):
    assert titles.named_versions(titles.read_file(title, artist)) == frozenset(named)


def test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone():
    # Refused on its tracks alone (1: the title is not the file's), or its title alone (2: no
    # track is the file's title).
    fetch = pressings({1: ("Other", "Two Months Off"), 2: ("Two Months Off", "Side One")})
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert (said.answer, said.note) == (
        "miss",
        "Discogs release 1 holds no track with this version (tim green); "
        "Discogs release 2 holds no track with this version (tim green)",
    )


def test_a_title_naming_two_mixes_lists_them_in_order_in_the_note():
    said = asked("X (Tide Remix) (Bloom Edit)", 6, tracks=("X",))
    assert (said.answer, said.note) == (
        "miss", "Discogs release 6 holds no track with this version (bloom or tide)")


@pytest.mark.parametrize(
    "group",
    ["feat. Tom Tom Club", "feat. Culture Club", "ft. Amp Live", "with Bombay Bicycle Club"])
def test_a_credit_group_ending_in_a_version_word_is_no_version(group):
    """Round two's row 7: a feature credit is never a mix, so the plain track matches."""
    assert titles.named_versions(titles.read_file(f"Song ({group})", ARTIST)) == frozenset()
    assert matched(f"Song ({group})", tracks=("Opener", "Song"))


@pytest.mark.parametrize("label", ["The Original Mix", "The Remix", "The Radio Edit"])
def test_an_article_names_no_maker(label):
    assert matched(f"Sunrise Mood ({label})", tracks=("Sunrise Mood",))


def test_an_article_is_folded_out_of_a_makers_name_on_both_sides():
    assert matched("Sunrise Mood (The Black Madonna Remix)", tracks=("Sunrise Mood (Black Madonna Remix)",))
    assert not matched("Sunrise Mood (The Black Madonna Remix)", tracks=("Sunrise Mood",))


# ═══ U324. A maker spelled with a letter accent stripping leaves alone ═════

#: Sitting 102's file and the three releases its sweep named, each mix spelled with ø.
ROYKSOPP = "Röyksopp"
WHAT_ELSE = "What Else Is There? (Trentemoller Remix)"
WHAT_ELSE_RELEASES = (2667673, 589586, 641256)

#: Each letter the fold takes and its plain reading: one maker spelled two ways.
ONE_MAKER = (
    ("Trentemøller", "Trentemoller"), ("TRENTEMØLLER", "Trentemoller"), ("Straße", "Strasse"),
    ("Łukasz", "Lukasz"), ("łukasz", "Lukasz"), ("Æther", "Aether"), ("æther", "Aether"),
    ("Œuvre", "Oeuvre"), ("œuvre", "Oeuvre"), ("Đorđe", "Dorde"), ("ĐORĐE", "Dorde"),
    ("Þór", "Thor"), ("þór", "Thor"),
)


def _carrying(number: int, mix: str):
    """A fetch naming release ``number`` of the plain title and the title's ``mix``."""
    titled = ("What Else Is There?", "What Else Is There?", f"What Else Is There? ({mix})")
    return pressings({number: titled}, artist=ROYKSOPP)


@pytest.mark.parametrize("number", WHAT_ELSE_RELEASES)
def test_the_trentemoller_remix_takes_each_release_the_sweep_named(number):
    said = discogs_answer(searcher(_carrying(number, "Trentemøller Remix"))(ROYKSOPP, WHAT_ELSE))
    assert said.answer == "matched", said.note


def test_the_mix_spelled_with_its_letter_takes_a_release_writing_it_plain():
    fetch = _carrying(7, "Trentemoller Remix")
    said = discogs_answer(searcher(fetch)(ROYKSOPP, "What Else Is There? (Trentemøller Remix)"))
    assert said.answer == "matched", said.note


def test_the_sitting_file_takes_its_genre_through_tag_one(tmp_path, silence):
    path = tmp_path / "what else is there.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(path, {"artist": ROYKSOPP, "title": f"04A - 126 - {WHAT_ELSE}"})
    number = WHAT_ELSE_RELEASES[0]
    titled = {number: ("What Else Is There?", "What Else Is There? (Trentemøller Remix)")}
    fetch = pressings(titled, artist=ROYKSOPP, styles={number: ("Techno",)})
    result = tag.tag_one(path, searcher=searcher(fetch))
    (discogs,) = [said for said in result.answers if said.source == searchers.DISCOGS]
    assert discogs.answer == "matched", discogs.note
    assert result.genre_written is not None
    assert tags.read_genre_from_file(path) == result.genre_written


@pytest.mark.parametrize(("written", "plain"), ONE_MAKER)
def test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker(written, plain):
    assert matched(f"Sunrise Mood ({plain} Remix)", tracks=(f"Sunrise Mood ({written} Remix)",))
    assert matched(f"Sunrise Mood ({written} Remix)", tracks=(f"Sunrise Mood ({plain} Remix)",))
    named = titles.named_versions(titles.read_file(f"Sunrise Mood ({written} Remix)", ARTIST))
    assert named == titles.named_versions(titles.read_file(f"Sunrise Mood ({plain} Remix)", ARTIST))


@pytest.mark.parametrize(("written", "plain"), ONE_MAKER)
def test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words(written, plain):
    assert matched(f"Sunrise Mood ({plain} Remix)", tracks=(f"Sunrise Mood - {written} Remix",))
    assert matched(f"Sunrise Mood - {written} Remix", tracks=(f"Sunrise Mood ({plain} Remix)",))


def test_another_maker_is_still_a_version_miss_with_the_note():
    for title in ("What Else Is There? (Trentemøller Remix)", WHAT_ELSE):
        said = asked(title, 9, tracks=("What Else Is There? (Vitalic Remix)",))
        assert (said.answer, said.note) == (
            "miss", "Discogs release 9 holds no track with this version (trentemoller)")


@pytest.mark.parametrize(
    ("mine", "theirs"),
    [
        # The fold reads a letter as its plain spelling, never another letter's.
        ("Trentemøller", "Trentemoeller"),
        ("Æther", "Ather"),
        ("Straße", "Strase"),
        ("Þór", "Tor"),
        ("Đorđe", "Dorje"),
    ])
def test_a_different_spelling_is_still_another_maker(mine, theirs):
    assert not matched(f"Sunrise Mood ({mine} Remix)", tracks=(f"Sunrise Mood ({theirs} Remix)",))
    assert not matched(f"Sunrise Mood ({theirs} Remix)", tracks=(f"Sunrise Mood ({mine} Remix)",))


def test_a_plain_title_naming_no_mix_matches_as_before():
    assert matched("What Else Is There?", tracks=("What Else Is There?",))
    assert matched("What Else Is There? (Extended Mix)", tracks=("What Else Is There?",))
    assert matched("Straße", tracks=("Straße",))


def test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone():
    """Each table entry read alone: deleting one makes its letter a different maker."""
    assert {letter: titles._folded(letter) for letter in "øØæÆœŒßđĐłŁþÞ"} == {
        "ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe", "ß": "ss",
        "đ": "d", "Đ": "d", "ł": "l", "Ł": "l", "þ": "th", "Þ": "th",
    }


def test_a_letter_that_also_carries_an_accent_is_read_plain():
    """The table is read after accents come off, so "ǿ" and "ǽ" are "o" and "ae"."""
    assert (titles._folded("ǿ"), titles._folded("ǽ")) == ("o", "ae")
    assert matched("Sunrise Mood (Trentemoller Remix)", tracks=("Sunrise Mood (Trentemǿller Remix)",))
