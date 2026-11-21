"""U318: a remix takes a Discogs release and its genre only when that release carries its version.

Measured at sitting 101's tag sweep for A181: two remixes took a Discogs
release that does not carry their version, and with it a genre their
recording was never given. "Two Months Off (Tim Green Remix)" took release
8532080, which holds four other mixes and no Tim Green mix, and "As You Fly
(Mita Gami Extended Mix)" took the 16BL remix single, release 28513768. The
Discogs match read a title past its version: a file's title is known by its
core, the words before the bracket groups it ends with, so any track or
release title of the same core met it, whatever its mix.

WHAT THIS SUITE GUARDS, the card's merge blockers first:

* A FILE WHOSE TITLE NAMES A VERSION TAKES ONLY A RELEASE THAT WRITES IT,
  on a track or, for a single, on the release's own title or a track that
  is the version alone. The two sitting releases, hand built here in the
  shape Discogs serves them, refuse their files.
* A FILE THAT MATCHED BEFORE STILL MATCHES unless it names a version the
  release does not write: a title with no version, and one whose version is
  version words alone ("Extended Mix", "Original Mix"), the noise the shared
  reader already sheds, are matched exactly as before.
* THE MISS SAYS WHY in the file's record, in words a person reads, and the
  file goes on to the next source as any miss does.
* NOTHING BUT DISCOGS CHANGES. Beatport, Traxsource and Bandcamp read the
  same rows the same way.

Nothing here touches the network, and the token is a fixture word. The
artist is a fixture name; the titles are the sitting's.
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

#: The sitting's two releases, as hand built payloads at the producer's
#: boundary: the release read Discogs serves, its tracklist the mixes the
#: sitting's record named, none of them the file's.
TWO_MONTHS_OFF = 8532080
TWO_MONTHS_OFF_TRACKS = (
    "Two Months Off",
    "Two Months Off (Radio Edit)",
    "Two Months Off (Dark Lane Remix)",
    "Two Months Off (Sunfold Dub)",
)
AS_YOU_FLY = 28513768
AS_YOU_FLY_TRACKS = ("As You Fly (16BL Remix)", "As You Fly (16BL Dub)")


def listed(*titles_: str) -> list[dict]:
    return [
        {"position": f"A{index}", "type_": "track", "title": title}
        for index, title in enumerate(titles_, 1)
    ]


def asked(title: str, number: int, *, release_title: str = "An EP", tracks: tuple[str, ...]):
    """Discogs' answer for a file titled ``title`` by :data:`ARTIST`, whose
    search names one release, ``number``, holding ``tracks``."""
    fetch = routed(
        search=results(number),
        releases={
            number: release(number, artist=ARTIST, title=release_title, tracks=listed(*tracks))
        },
    )
    return discogs_answer(searcher(fetch)(ARTIST, title))


def matched(title: str, *, release_title: str = "An EP", tracks: tuple[str, ...]) -> bool:
    return asked(title, 5, release_title=release_title, tracks=tracks).answer == "matched"


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


# ---------------------------------------------------------------------------
# A. The sitting's two files
# ---------------------------------------------------------------------------


def test_the_tim_green_remix_refuses_a_release_of_four_other_mixes():
    said = asked(
        "Two Months Off (Tim Green Remix)",
        TWO_MONTHS_OFF,
        release_title="Two Months Off",
        tracks=TWO_MONTHS_OFF_TRACKS,
    )
    assert said.answer == "miss"
    assert said.note == "Discogs release 8532080 holds no track with this version (tim green)"


def test_the_mita_gami_extended_mix_refuses_the_16bl_remix_single():
    said = asked(
        "As You Fly (Mita Gami Extended Mix)",
        AS_YOU_FLY,
        release_title="As You Fly",
        tracks=AS_YOU_FLY_TRACKS,
    )
    assert said.answer == "miss"
    assert said.note == "Discogs release 28513768 holds no track with this version (mita gami)"


def test_the_sitting_files_headed_as_the_library_writes_them_refuse_too():
    for title, number, release_title, tracks in (
        (
            "04A - 126 - Two Months Off (Tim Green Remix)",
            TWO_MONTHS_OFF,
            "Two Months Off",
            TWO_MONTHS_OFF_TRACKS,
        ),
        (
            "09B - 122 - [MP3] As You Fly (Mita Gami Extended Mix)",
            AS_YOU_FLY,
            "As You Fly",
            AS_YOU_FLY_TRACKS,
        ),
    ):
        assert asked(title, number, release_title=release_title, tracks=tracks).answer == "miss"


def test_each_sitting_file_still_takes_a_release_that_carries_its_mix():
    assert matched(
        "Two Months Off (Tim Green Remix)",
        release_title="Two Months Off",
        tracks=(*TWO_MONTHS_OFF_TRACKS, "Two Months Off (Tim Green Remix)"),
    )
    assert matched(
        "As You Fly (Mita Gami Extended Mix)",
        release_title="As You Fly",
        tracks=("As You Fly (Mita Gami Remix)",),
    ), "the extended form of a remix is that remix, as the reader sheds Extended"


def test_the_refused_file_is_left_untagged_with_the_reason_in_its_record(tmp_path, silence):
    path = tmp_path / "two months off.flac"
    shutil.copy2(silence, path)
    assert tags.write_tags(
        path, {"artist": ARTIST, "title": "04A - 126 - Two Months Off (Tim Green Remix)"}
    )
    fetch = routed(
        search=results(TWO_MONTHS_OFF),
        releases={
            TWO_MONTHS_OFF: release(
                TWO_MONTHS_OFF,
                artist=ARTIST,
                title="Two Months Off",
                tracks=listed(*TWO_MONTHS_OFF_TRACKS),
            )
        },
    )
    result = tag.tag_one(path, searcher=searcher(fetch))
    assert result.genre_written is None
    assert tags.read_genre_from_file(path) in (None, "")
    (discogs,) = [said for said in result.answers if said.source == searchers.DISCOGS]
    assert (discogs.answer, discogs.note) == (
        "miss",
        "Discogs release 8532080 holds no track with this version (tim green)",
    )
    # The walk goes on to Beatport, as after any Discogs miss.
    (beatport,) = [said for said in result.answers if said.source == searchers.BEATPORT]
    assert beatport.answer == "miss"


def test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix():
    fetch = routed(
        search=results(1, 2),
        releases={
            1: release(
                1, artist=ARTIST, title="Two Months Off", tracks=listed(*TWO_MONTHS_OFF_TRACKS)
            ),
            2: release(
                2,
                artist=ARTIST,
                title="Remixes",
                tracks=listed("Two Months Off (Tim Green Remix)"),
                styles=("Techno",),
            ),
        },
    )
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert said.answer == "matched"
    assert "release 2" in said.note


def test_the_miss_names_every_release_refused_for_its_version_and_no_other():
    fetch = routed(
        search=results(1, 2, 3),
        releases={
            1: release(1, artist=ARTIST, title="Two Months Off", tracks=listed("Two Months Off")),
            2: release(2, artist=ARTIST, title="Other", tracks=listed("Another Song")),
            3: release(
                3, artist=ARTIST, title="Two Months Off", tracks=listed("Two Months Off (B Remix)")
            ),
        },
    )
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
        },
    )
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert said.answer not in ("miss", "matched")


# ---------------------------------------------------------------------------
# B. The brief's scenarios
# ---------------------------------------------------------------------------


def test_a_remix_takes_nothing_from_a_release_of_the_plain_title_and_another_remix():
    assert not matched("X (A Remix)", tracks=("X", "X (B Remix)"))


def test_a_remix_takes_a_release_whose_track_writes_it():
    assert matched("X (A Remix)", tracks=("X", "X (A Remix)"))


def test_a_title_with_no_version_still_matches_the_plain_recording():
    assert matched("X", tracks=("X",))
    assert matched("X", tracks=("X (Original Mix)",))


def test_a_title_with_no_version_matches_a_release_of_remixes_only_as_before():
    """Out of scope (R-1637 is Beatport's side of it): unchanged from main."""
    assert matched("X", tracks=("X (A Remix)",))


def test_the_extended_and_original_noise_follows_the_reader():
    """The reader sheds a version of version words alone, "Extended Mix" and
    "Original Mix", as it always did, so such a file names no other mix and
    matches the release of "X (Original Mix)" and of "X" as before."""
    assert matched("X (Extended Mix)", tracks=("X (Original Mix)",))
    assert matched("X (Extended Mix)", tracks=("X",))
    assert matched("X (Original Mix)", tracks=("X (Extended Mix)",))
    assert matched("X (Radio Edit)", tracks=("X",))
    assert matched("X (2014 Remaster)", tracks=("X",))


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
    ],
)
def test_a_mix_that_names_no_one_still_takes_the_plain_title(title):
    """A description of a mix, "Main", "Vocal", "Album", "12 Inch", names no
    other mix (``titles.MIX_DESCRIPTIONS``), so it matches as it did."""
    assert matched(title, tracks=("X",))


def test_a_named_mix_after_a_description_still_names_its_maker():
    assert not matched("X (Tim Green Vocal Mix)", tracks=("X",))
    assert matched("X (Tim Green Vocal Mix)", tracks=("X (Tim Green Remix)",))
    assert not matched("X (Main Tim Green Mix)", tracks=("X (Dark Lane Mix)",))


def test_the_single_fallback_refuses_a_remix_on_a_one_track_release_of_the_title():
    assert not matched("X (A Remix)", release_title="X", tracks=("X",))
    assert not matched("X (A Remix)", release_title="X", tracks=("Original Mix",))


def test_the_single_fallback_takes_a_release_whose_track_is_the_version_alone():
    assert matched("X (A Remix)", release_title="X", tracks=("Original Mix", "A Remix"))
    assert not matched("X (A Remix)", release_title="X", tracks=("Original Mix", "B Remix"))


def test_the_single_fallback_takes_a_release_whose_own_title_writes_the_version():
    assert matched("X (A Remix)", release_title="X (A Remix)", tracks=("Side One",))
    assert not matched("X (A Remix)", release_title="X (B Remix)", tracks=("Side One",))


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
    ],
)
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
    ],
)
def test_another_version_or_none_takes_nothing(title, track):
    assert not matched(title, tracks=(track,))


def test_an_artist_that_does_not_match_still_refuses_a_track_that_writes_the_version():
    fetch = routed(
        search=results(4),
        releases={4: release(4, artist="Someone Else", title="X", tracks=listed("X (A Remix)"))},
    )
    assert discogs_answer(searcher(fetch)(ARTIST, "X (A Remix)")).answer == "miss"


# ---------------------------------------------------------------------------
# C. Nothing but Discogs changes
# ---------------------------------------------------------------------------


def test_the_shared_matcher_still_reads_a_remix_as_its_title():
    """The seam is Discogs': ``titles.matches`` is unchanged for every caller,
    so Beatport, Traxsource and Bandcamp read the row as they did."""
    assert searchers._title_matches(
        "Two Months Off (Tim Green Remix)", "Two Months Off", artist=ARTIST
    )


def test_beatport_is_unchanged_for_a_remix_against_the_plain_row():
    fetch = routed(
        search=results(),
        beatport=searchers.Fetched(
            text=_beatport_page(
                [_beatport_track(ARTIST, "Two Months Off", BUCKET_GENRE, mix="Original Mix")]
            ),
            status=200,
        ),
    )
    hit = searcher(fetch, token=None)(ARTIST, "Two Months Off (Tim Green Remix)")
    assert hit.genre == BUCKET_GENRE


# ---------------------------------------------------------------------------
# D. The two readers
# ---------------------------------------------------------------------------


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
        # A title of brackets alone is its own title, never its version, and
        # a title part that names nothing is no title for one to follow.
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
    ],
)
def test_a_files_named_versions(title, named):
    assert titles.named_versions(titles.read_file(title, ARTIST)) == frozenset(named)


@pytest.mark.parametrize(
    ("row", "titled", "alone"),
    [
        # A row whose title is the file's writes the mix wherever its
        # structure puts it; read alone, only a row that is the mix does.
        ("Two Months Off (Tim Green Remix)", True, False),
        ("Two Months Off [Tim Green Remix]", True, False),
        ("Two Months Off - Tim Green Remix", True, False),
        ("Two Months Off - Tim Green Remix - Part 2", True, False),
        ("Two Months Off (Tim Green Remix) - 2014 Remaster", True, False),
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
    ],
)
def test_a_catalogue_title_writes_a_version(row, titled, alone):
    named = frozenset({("tim", "green")})
    assert titles.writes_version(row, named, titled=True) is titled
    assert titles.writes_version(row, named, titled=False) is alone


def test_no_named_version_is_written_by_any_row():
    assert not titles.writes_version("Two Months Off (Tim Green Remix)", frozenset(), titled=True)


# ---------------------------------------------------------------------------
# E. Review round one: what names no one, folding, and the guards
# ---------------------------------------------------------------------------


def test_the_mix_descriptions_are_exactly_these():
    """Pinned word for word, as the domain's version words are: a word taken
    out reads as a maker's name and loses the plain release (round one's
    BLOCKING finding), and a word put in can fold a maker away."""
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


#: Mixes of the plain title's own recording, the 147 labels round one drove,
#: each matched against the album's plain track on main.
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
    """The recorded cost (a residual): a style word both lists lack reads as a
    maker's name, so such a file misses the plain track rather than guess."""
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
    ],
)
def test_a_maker_is_folded_as_a_name_is(title, row):
    assert matched(title, tracks=(row,))


def test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix():
    """Round one's finding 6: "Sun Path (Tide Remix)" is Tide's remix of
    another title, never evidence that a single of "Sunrise Mood" holds one."""
    assert not matched(
        "Sunrise Mood (Tide Remix)",
        release_title="Sunrise Mood",
        tracks=("Sunrise Mood", "Sun Path (Tide Remix)"),
    )
    assert matched(
        "Sunrise Mood (Tide Remix)",
        release_title="Sunrise Mood",
        tracks=("Sunrise Mood", "(Tide Remix)"),
    )


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
    ],
)
def test_what_a_title_names_as_its_mix(title, artist, named):
    assert titles.named_versions(titles.read_file(title, artist)) == frozenset(named)


def test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone():
    fetch = routed(
        search=results(1, 2),
        releases={
            # Refused on its tracks alone: the release's title is not the file's.
            1: release(1, artist=ARTIST, title="Other", tracks=listed("Two Months Off")),
            # Refused on its title alone: no track is the file's title.
            2: release(2, artist=ARTIST, title="Two Months Off", tracks=listed("Side One")),
        },
    )
    said = discogs_answer(searcher(fetch)(ARTIST, "Two Months Off (Tim Green Remix)"))
    assert (said.answer, said.note) == (
        "miss",
        "Discogs release 1 holds no track with this version (tim green); "
        "Discogs release 2 holds no track with this version (tim green)",
    )


def test_a_title_naming_two_mixes_lists_them_in_order_in_the_note():
    said = asked("X (Tide Remix) (Bloom Edit)", 6, tracks=("X",))
    assert (said.answer, said.note) == (
        "miss",
        "Discogs release 6 holds no track with this version (bloom or tide)",
    )
