"""U16: the three states, and the middle one that the source system has no name for.

Each test guards a way the system this replaces got it wrong: it resolved a wanted track to the
first text hit, decided ownership from an export that can lag, kept a person's decision in a
file that dies with its directory, and had no concept of a deliberately deleted version.
Parts: folding and versions, the on-disk index, resolution, the intake shapes, and the verb.
"""

from __future__ import annotations

import ast
import io
import json
import re
import shutil
import sqlite3
import unicodedata
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import match, match_cli, match_identity, match_library
from cratekit.cli import output, registry
from cratekit.core import config, naming, review, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode

# The ONE container synthesizer, borrowed from a helper module rather than copied, so
# there is one opinion of what a valid file is and importing it runs no other suite.
from tests._containers import synth_container, tagged_container

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
MATCH_SOURCES = tuple(
    SRC_ROOT / "cratekit" / "acquire" / f"{name}.py"
    for name in ("match", "match_identity", "match_list", "match_library")
)
MATCH_CLI_SOURCE = SRC_ROOT / "cratekit" / "acquire" / "match_cli.py"
RESIDUALS_DOC = REPO_ROOT / "docs" / "residual-findings.md"


# ── Residual citations, by title ─────────────────────────────────────────────
# A residual number is not a stable name, so every citation here names a TITLE.
# ``test_every_residual_this_unit_cites_is_a_heading_that_exists`` catches a retitle and
# ``test_no_residual_is_cited_by_number_anywhere_in_this_unit`` keeps numbers out.
RESIDUALS: tuple[str, ...] = (
    "Two briefs disagree about whether a missing track is a review item",
    "Four accepted findings from the second U16 review, recorded rather than fixed",
    "A provider row cannot address a library row that kept a featured credit",
    "The two tombstone derivations are reconciled only at merge",
    "The index reads a file's title one way, so the disk side of the one-word "
    "dash stays narrow",
    "The recorder keeps the Title column's own shape, so the consulter "
    "enumerates shapes",
    "The one-word dash class cannot converge on state across the three readers",
    "The ambiguous reading class is queued as a question and does not gate the run",
    "A question answered on one machine does not settle a different question "
    "about the same line",
    "One vocabulary lives in two files until the domain module merges",
    "A deleted track the tombstone consult cannot reach is listed for download",
    "The match engine never consults the ISRC, and a processed file's artist tag "
    "lists every credited artist, so a quarter of the hearts the library holds "
    "read missing or offered",
    "A review item outlives its question: a later resolution that owns the row "
    "leaves the version-match item open, and no verdict or predicate can retire "
    "it honestly",
    "A superseded verdict outlives its rule when the row goes missing rather than "
    "back to a question",
)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, saved, so the real verb resolves the real paths."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root), "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")}, "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def music(cfg):
    return cfg.library.root / cfg.library.music_dir


def hold(music: Path, name: str) -> Path:
    """Put a file in the library under the naming convention, with no tags, so these exercise the
    FILENAME half of on-disk truth."""
    path = music / f"{name}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def index_of(music: Path) -> match.LibraryIndex:
    return match.index_library(music)


def nothing_suppressed(_kind, _identity) -> bool:
    return False


def no_identifier(kind, identity) -> str:
    return f"dc_{kind}_{sorted(identity.items())}"


def resolve(wanted, index, *, suppresses=nothing_suppressed) -> match.MatchResult:
    return match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=no_identifier)


def one(*, artist="Aurora Bloom", title="Sun Path", version="", key=None, origin=match.TEXT):
    return match.Wanted(artist=artist, title=title, version=version, key=key, origin=origin)


def drive(argv: list[str]) -> tuple[int, dict]:
    """Run the real dispatcher and return (status, envelope)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def write_list(tmp_path: Path, body: str, name: str = "list.txt") -> str:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return str(path)


# ── Part 1: folding, and what counts as a version ─────────────────────────


def test_folding_keeps_word_boundaries_rather_than_deleting_punctuation():
    """A collision here merges two candidates onto one decision, silently.

    Folding punctuation to a space keeps "Re Mix" and "Remix" apart while a hyphen and a space
    agree.
    """
    assert match.fold("Re-Mix") == match.fold("Re Mix")
    assert match.fold("ReMix") != match.fold("Re Mix")
    assert match.fold("  Café  DEL  Mar ") == "cafe del mar"


def test_the_artist_and_title_cannot_be_resplit_into_a_colliding_pair():
    """The join uses a separator folding can never produce, so two records stay two."""
    assert match.recording_token("Sun", "Path") != match.recording_token("Sun Path", "")


def test_the_original_mix_and_no_qualifier_at_all_are_one_version():
    """Otherwise a person is asked to confirm a track against itself."""
    assert match.version_token("Original Mix") == match.version_token("")
    assert match.version_token("original") == ""


def test_an_album_version_is_not_folded_away():
    """It is a real, different cut on plenty of releases, so folding it would join versions."""
    assert match.version_token("Album Version") != ""


def test_a_trailing_bracketed_qualifier_becomes_the_version():
    assert match.split_version("Sun Path (Extended Mix)") == ("Sun Path", "Extended Mix")
    assert match.split_version("Sun Path [Radio Edit]") == ("Sun Path", "Radio Edit")


def test_a_featured_credit_is_a_performer_and_never_a_version():
    """Two listings of one record disagree constantly about where the guest goes."""
    title, version = match.split_version("Sun Path (feat. Mira) (Someone Remix)")
    assert (title, version) == ("Sun Path", "Someone Remix")
    assert match.split_version("Sun Path (feat. Mira)") == ("Sun Path", "")


@pytest.mark.parametrize(
    ("spelled", "expected"),
    [
        ("[Premade Sandwiches]", ("Premade Sandwiches", "")),
        ("(Premade Sandwiches)", ("Premade Sandwiches", "")),
        ("  [Premade Sandwiches]  ", ("Premade Sandwiches", "")),
        ("[Premade Sandwiches] (Live)", ("Premade Sandwiches", "Live")),
        ("[Premade Sandwiches] (feat. Mira)", ("Premade Sandwiches", "")),
        ("Song (Remix)", ("Song", "Remix")), ("Song [Remix] (Edit)", ("Song", "Remix Edit")),
        ("[]", ("", "")), ("[With You]", ("With You", "")),
        ("(With Or Without You)", ("With Or Without You", "")),
        ("(Without You)", ("Without You", "")), ("(Without You Remix)", ("", "Without You Remix")),
        ("(With Love) (Remix)", ("With Love", "Remix")), ("(feat. Mira)", ("feat. Mira", "")),
        ("(Extended)", ("", "Extended")),
        ("[Original Mix] (Remastered)", ("", "Original Mix Remastered")),
        ("[Premade Sandwiches Live]", ("", "Premade Sandwiches Live")),
    ],
)
def test_a_title_written_wholly_in_brackets_keeps_its_words(spelled, expected):
    """U213. A group that is all the title has left is the title, brackets dropped.

    ``[Premade Sandwiches]`` left no title; an empty group is still nothing, a group after a
    title still a version, and a first group a title even when it reads like a credit.
    """
    assert match.split_version(spelled) == expected
    assert match.split_title(spelled) == expected


# ── U262: a credit is a first WORD, not the first letters of a group ─────────

#: Groups whose first word only BEGINS with a credit marker's letters, so each is a version.
U262_VERSION_GROUPS: tuple[str, ...] = (
    "Without You Remix", "Withdrawn Mix", "Within Mix", "Feature Edit", "Featureless Dub",
)

#: Groups whose first word IS a credit marker, in the spellings a listing uses.
U262_CREDIT_GROUPS: tuple[str, ...] = ("feat. Anna", "ft Anna", "Featuring Anna", "with Anna")


def u262_plain_record(tmp_path: Path) -> match.LibraryIndex:
    """A library holding only the plain ``Nova Reef - Sun Path``, tagged."""
    path = tagged_container(
        tmp_path, tmp_path / "library" / "Sun Path.flac", artist="Nova Reef", title="Sun Path"
    )
    return match.index_paths([path])


def u262_wanted(spelled: str) -> match.Wanted:
    title, version = match.split_title(spelled)
    return match.Wanted(artist="Nova Reef", title=title, version=version, spelled=spelled)


@pytest.mark.parametrize("group", U262_VERSION_GROUPS)
def test_a_group_that_only_begins_with_a_credits_letters_is_a_version(tmp_path, group):
    """U262. ``Sun Path (Without You Remix)`` is a remix, not the plain record.

    The letters rule read ``Without`` as ``with`` and dropped the group, so the remix matched
    exact against the plain record and was never fetched.
    """
    spelled = f"Sun Path ({group})"
    assert match.split_title(spelled) == ("Sun Path", group)
    assert match.split_version(spelled) == ("Sun Path", group)
    (found,) = resolve([u262_wanted(spelled)], u262_plain_record(tmp_path)).matches
    assert (found.state, found.why) == (match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)


@pytest.mark.parametrize("group", U262_CREDIT_GROUPS)
def test_a_group_whose_first_word_is_a_credit_still_comes_off(tmp_path, group):
    """The other half: a real featured credit is still a performer and no version."""
    spelled = f"Sun Path ({group})"
    assert match.split_title(spelled) == ("Sun Path", "")
    (found,) = resolve([u262_wanted(spelled)], u262_plain_record(tmp_path)).matches
    assert (found.state, found.why) == (match.MatchState.MATCHED, match.Why.EXACT)


def test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit(tmp_path):
    """``(Ft Worth Edit)`` reads as a credit, because ``Ft`` IS the word ``ft``, the rule
    ``core.tombstone`` records deletions by. Pinned so the choice is visible."""
    from cratekit.core import tombstone

    spelled = "Sun Path (Ft Worth Edit)"
    assert match.split_title(spelled) == ("Sun Path", "")
    assert match_identity._is_a_credit("Ft Worth Edit") and tombstone._is_a_credit("Ft Worth Edit")
    (found,) = resolve([u262_wanted(spelled)], u262_plain_record(tmp_path)).matches
    assert (found.state, found.why) == (match.MatchState.MATCHED, match.Why.EXACT)


def test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version(tmp_path):
    """The index reads a held title through the same split, so the fix reaches both sides."""
    held = tagged_container(
        tmp_path, tmp_path / "library" / "Sun Path (Without You Remix).flac", artist="Nova Reef",
        title="Sun Path (Without You Remix)",
    )
    index = match.index_paths([held])
    (found,) = resolve([u262_wanted("Sun Path")], index).matches
    assert (found.state, found.why) == (match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)
    (same,) = resolve([u262_wanted("Sun Path (Without You Remix)")], index).matches
    assert (same.state, same.why) == (match.MatchState.MATCHED, match.Why.EXACT)


#: One list of groups both credit predicates are asked about.
U262_EVERY_GROUP: tuple[str, ...] = (
    *U262_VERSION_GROUPS, *U262_CREDIT_GROUPS, "Live with Strings", "Nightwave Remix", "feat",
    "With", "FT. Anna", "Feat.Anna", "ft.anna", "featuring", "Featurette", "Ftw Edit",
    "Ft Worth Edit", "With You", "",
)


@pytest.mark.parametrize("group", U262_EVERY_GROUP)
def test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is(group):
    """U262. The matcher keeps its own copy of ``core.tombstone._is_a_credit`` because the rule sits
    inside the identity stamp, so this holds the two equal over one list of groups."""
    from cratekit.core import tombstone

    assert match_identity._is_a_credit(group) == tombstone._is_a_credit(group)


def test_the_matcher_and_the_tombstone_share_one_credit_vocabulary():
    from cratekit.core import tombstone

    assert match_identity._CREDIT_MARKERS == tombstone._CREDIT_MARKERS


def test_a_defect_title_keeps_the_tombstone_identity_its_spelling_always_had():
    """A tombstone recorded from such a row is still met: the identity is the listing's verbatim
    spelling, and only the other spellings the consult composes change."""
    from cratekit.core import tombstone

    spelled = "Sun Path (Without You Remix)"
    wanted = u262_wanted(spelled)
    recorded = tombstone.version_identity(
        artist="Nova Reef", title=tombstone.version_title(spelled, "")
    )
    assert wanted.identity == {"artist": "nova reef", "title": "sun path (without you remix)"}
    assert recorded in wanted.suppression_spellings
    assert wanted.addresses == (
        "Sun Path (Without You Remix)", "Sun Path [Without You Remix]",
        "Sun Path (Without) (You Remix)", "Sun Path (Without You) (Remix)",
        "Sun Path - Without You Remix", "Sun Path - Without You Remix (Without You Remix)",
    )
    plain = tombstone.version_identity(artist="Nova Reef", title="Sun Path")
    assert plain not in wanted.suppression_spellings


#: The addresses three credited listings composed before U262. A credited row's spellings must not
#: move.
U262_CREDITED_ADDRESSES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Sun Path (feat. Mira) (Nightwave Remix)",
        (
            "Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path (feat. Mira) [Nightwave Remix]",
            "Sun Path (feat. Mira) (Nightwave) (Remix)", "Sun Path (feat. Mira) - Nightwave Remix",
            "Sun Path (feat. Mira) - Nightwave Remix (Nightwave Remix)",
        ),
    ),
    ("Sun Path (Nightwave Remix) (ft Mira)", ("Sun Path (Nightwave Remix) (ft Mira)",)),
    (
        "Sun Path (with Mira)",
        (
            "Sun Path (with Mira)", "Sun Path (with Mira) (original)",
            "Sun Path (with Mira) [original]", "Sun Path (with Mira) (original mix)",
            "Sun Path (with Mira) [original mix]", "Sun Path (with Mira) (original) (mix)",
            "Sun Path (with Mira) - original mix",
            "Sun Path (with Mira) - original mix (original mix)",
            "Sun Path (with Mira) (original version)", "Sun Path (with Mira) [original version]",
            "Sun Path (with Mira) (original) (version)", "Sun Path (with Mira) - original version",
            "Sun Path (with Mira) - original version (original version)",
        ),
    ),
)


@pytest.mark.parametrize(("spelled", "addresses"), U262_CREDITED_ADDRESSES)
def test_a_credited_rows_suppression_spellings_are_unchanged(spelled, addresses):
    wanted = u262_wanted(spelled)
    assert wanted.addresses == addresses
    assert wanted.uncredited_spellings == ()


def test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses():
    (read,) = match.read_tidal_tracks(
        [{"id": "5", "name": "[Premade Sandwiches]", "artist": {"name": "Glass Animals"}}]
    )
    assert (read.artist, read.title, read.version) == ("Glass Animals", "Premade Sandwiches", "")
    assert read.spelled == "[Premade Sandwiches]"
    for nothing in ("[]", "( )", "(Extended)", "[Radio Edit]"):
        with pytest.raises(match.UnreadableList, match="names no title"):
            match.read_tidal_tracks(
                [{"id": "6", "name": nothing, "artist": {"name": "Glass Animals"}}]
            )


def test_listed_names_reads_a_row_the_reader_refuses():
    row = {"id": " 7 ", "name": "", "artist": {"name": "Glass Animals"}}
    assert match.listed_names(row) == ("7", "Glass Animals", "")
    assert match.listed_names({"id": "8", "title": "[X]", "name": "Y", "artists": []}) == (
        "8", "", "[X]",
    )


def test_a_dash_inside_a_title_is_never_read_as_a_version():
    """The parser that guessed would invent a record nobody released."""
    assert match.split_version("Sun - Rise") == ("Sun - Rise", "")


def u24_fold(value: str) -> str:
    """U24's ``core.tombstone.fold``, written out INDEPENDENTLY, since building the expected value
    with the function under test proves only that it equals itself."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


#: Inputs chosen for what a fold change bites on: a copy that drifts from NFC to NFKC, gains
#: an article strip or stops case-folding fails HERE, which an ASCII pin cannot see.
FOLD_PINS: tuple[tuple[str, str], ...] = (
        # NFC composes; NFD would leave the combining acute on its own.
    ("Café del Mar", "café del mar"),
    ("Café del Mar", "café del mar"),
        # The two rows that see an NFC to NFKC drift: the fullwidth run and the circled digit.
    ("Ｓｕｎ Ｐａｔｈ", "ｓｕｎ ｐａｔｈ"),
    ("① Track", "① track"),
        # Full case folding expands this ligature with no compatibility normalization.
    ("Suﬁx", "sufix"),
        # A leading-article strip would break both sides silently. The article stays.
    ("The Sun Path", "the sun path"),
    ("STRASSE", "strasse"),
    ("İstanbul", "i̇stanbul"),
        # Spacing folds, punctuation does not.
    ("  Sun   Path  (Live)  ", "sun path (live)"),
    ("Sun Path [Live]", "sun path [live]"),
    ("曲  (リミックス)", "曲 (リミックス)"),
)


@pytest.mark.parametrize("given,expected", FOLD_PINS, ids=lambda v: repr(v)[:40])
def test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree(given, expected):
    """Pin the fold, not one hash: a copy's NORMALIZATION drifts only on its own inputs."""
    assert match.tombstone_fold(given) == expected
    assert match.tombstone_fold(given) == u24_fold(given)


def test_the_fold_pins_actually_discriminate_between_normalizations():
    """The table holds rows where NFC and NFKC differ, an article would be stripped and composition
    matters, so it cannot rot into strings that agree under every normalization."""
    import unicodedata as u

    inputs = [given for given, _ in FOLD_PINS]
    assert any(
        u.normalize("NFC", given).casefold() != u.normalize("NFKC", given).casefold()
        for given in inputs
    ), "no row here can see an NFC to NFKC drift"
    assert any(given.lower().startswith("the ") for given in inputs)
    assert any(u.normalize("NFC", given) != u.normalize("NFD", given) for given in inputs)


def test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist():
    """The two copies of the tombstone identity agree over the recording path.

    A tombstone recorded under one spelling is invisible to the other, so the version is fetched
    back and the deletion undone. For each rekordbox row shape this compares U24's recorder
    identity, composed by its own ``version_title``, with those the three readers produce, and
    what cannot reconcile is named in ``UNRECONCILED``. Still unproved, per the residual titled "The
    two
    tombstone derivations are reconciled only at merge": ``u24_records`` imitates the recorder.
    """
    from cratekit.core import tombstone

    assert match.TOMBSTONE_KIND == tombstone.KIND_VERSION
    assert match.UNCREDITED_KIND == tombstone.KIND_VERSION_UNCREDITED
    assert match_cli.TOMBSTONE_STORE == tombstone.STORE_KEY
    for given, _expected in FOLD_PINS:
        assert match.tombstone_fold(given) == tombstone.fold(given)
        # The vocabulary, the third thing that exists twice: a gap between this module's dash tail
        # list and the domain module's reported MISSING and re-acquired held files.
    assert match.VERSION_WORDS == tombstone.VERSION_WORDS
    for row_title in ROW_SPELLINGS:
        assert match.version_identity(
            artist="Aurora Bloom", title=row_title
        ) == tombstone.version_identity(artist="Aurora Bloom", title=row_title)
        # The composition, against the domain module's own rule rather than this file's imitation.
    for row_title, row_version, _listed, _title, _version in REKORDBOX_ROWS:
        assert tombstone.version_title(row_title, row_version) == u24_version_title(
            row_title, row_version
        ), "the imitation of version_title in this file has drifted from the real one"
        # The shapes the bracketed test decides, as literals the real module returned.
    for title, version, expected in U24_COMPOSITIONS:
        assert tombstone.version_title(title, version) == expected, (
            f"U24's version_title moved on {title!r} with {version!r}; this "
            f"file's imitation and its recorded literals both need re-measuring"
        )
        # The derivation over BOTH records the recorder writes: the verbatim tombstone and the
        # companion a credited row gains with its credits out.
    for row in REKORDBOX_ROWS:
        composed = tombstone.version_title(row[0], row[1])
        assert u24_uncredited("Aurora Bloom", row[0], row[1]) == (
            tombstone.version_identity(
                artist="Aurora Bloom", title=tombstone.uncredited_title(composed)
            )
            if tombstone.uncredited_title(composed)
            else None
        ), "the imitation of the companion in this file has drifted from the real one"
    missed = tuple(
        (row[0], wanted.origin)
        for row in REKORDBOX_ROWS
        for wanted in every_reader_on(row)
        if not reaches(
            wanted,
            tombstone.version_identity(
                artist="Aurora Bloom", title=tombstone.version_title(row[0], row[1])
            ),
            u24_uncredited("Aurora Bloom", row[0], row[1]),
        )
    )
    assert missed == UNRECONCILED, (
        "a library row spelling this side cannot address changed, so a tombstone "
        "became invisible"
    )


def test_the_tombstone_identity_is_u24s_algorithm_byte_for_byte():
    """The tombstone identity is U24's algorithm byte for byte: two units once hashed one record to
    two identifiers and a deleted version was fetched back. The identifier is a literal, so a
    change to folding, key names, kind or store key fails HERE."""
    identity = match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)")
    assert identity == {"artist": "aurora bloom", "title": "sun path (someone remix)"}
    assert identity == {
        "artist": u24_fold("Aurora Bloom"), "title": u24_fold("Sun Path (Someone Remix)"),
    }
    assert match.TOMBSTONE_KIND == "version"
    assert (
        review.suppression_id_for(match_cli.TOMBSTONE_STORE, match.TOMBSTONE_KIND, identity)
        == "dc_ddf982896f62fde4317a4fdd"
    )


#: The spellings a rekordbox Title column holds for one version of one recording; U24 hashes
#: the string verbatim, so a LIST naming the same record must reach the same identity.
ROW_SPELLINGS = [
    "Sun Path (Nightwave Remix)", "Sun Path - Nightwave Remix", "Sun Path [Nightwave Remix]",
    "Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path (Extended) (Remastered)", "Sun Path",
    "Sun Path (Original Mix)",
]


#: One rekordbox collection row per entry, plus what a list naming the record spells and the
#: provider row a source with a separate version field ships. Every column is a literal.
#: Fields: title column, version column, what a list spells, provider title, provider version.
REKORDBOX_ROWS: tuple[tuple[str, str, str, str, str], ...] = (
    ("Sun Path (Nightwave Remix)", "Nightwave Remix",
     "Sun Path (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
    ("Sun Path - Nightwave Remix", "Nightwave Remix",
     "Sun Path - Nightwave Remix", "Sun Path", "Nightwave Remix"),
    ("Sun Path [Nightwave Remix]", "Nightwave Remix",
     "Sun Path [Nightwave Remix]", "Sun Path", "Nightwave Remix"),
    ("Sun Path (feat. Mira) (Nightwave Remix)", "Nightwave Remix",
     "Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
        # The row U24's own fix is about: the mix name is only in the version column.
    ("Sun Path", "Nightwave Remix",
     "Sun Path (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
    ("Sun Path (Extended) (Remastered)", "",
     "Sun Path (Extended) (Remastered)", "Sun Path", "Extended Remastered"),
    ("Sun Path", "", "Sun Path", "Sun Path", ""),
    ("Sun Path (Original Mix)", "",
     "Sun Path (Original Mix)", "Sun Path", "Original Mix"),
)

#: The derivations that do not reconcile, EMPTY ON PURPOSE. It once held a credited row a
#: provider row could not address ("A provider row cannot address a library row that kept a
#: featured credit") and emptied when the recorder began writing a companion, per the residual
#: titled "A deleted track the tombstone consult cannot reach is listed for download". The verbatim
#: consult STILL cannot reach it, pinned by
#: ``test_the_verbatim_consult_alone_still_misses_the_credited_row``.
UNRECONCILED: tuple[tuple[str, str], ...] = ()


#: U24's ``core.tombstone`` bracket and credit vocabulary, written out INDEPENDENTLY.
U24_BRACKETED = re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]")
U24_CREDIT_MARKERS = frozenset({"feat", "ft", "featuring", "with"})
U24_WORD_SPLIT = re.compile(r"\W+", re.UNICODE)


def u24_is_a_credit(group: str) -> bool:
    """U24's ``core.tombstone._is_a_credit``, written out INDEPENDENTLY: the FIRST WORD only, so
    ``(Live with Strings)`` stays a mix name."""
    words = U24_WORD_SPLIT.split(u24_fold(group).strip())
    return bool(words) and words[0] in U24_CREDIT_MARKERS


def u24_already_carries(title: str, folded_version: str) -> bool:
    """U24's ``core.tombstone._already_carries``, written out INDEPENDENTLY.

    A title carries its mix name inside brackets only, on word boundaries, skipping a credit
    group; a substring test reads ``Live`` as carried by ``Lively Up`` and merges two rows.
    """
    delimited = re.compile(rf"(?<!\w){re.escape(folded_version)}(?!\w)")
    return any(
        delimited.search(group)
        for found in U24_BRACKETED.finditer(u24_fold(title))
        for group in found.groups()
        if group is not None and not u24_is_a_credit(group)
    )


def u24_version_title(title: str, version: str) -> str:
    """U24's ``core.tombstone.version_title``, written out INDEPENDENTLY.

    It composes with round parentheses but SHORT CIRCUITS when a bracketed group already names the
    version, so a consulter must enumerate shapes; the empty check stops ``Sun Path ()``.
    """
    folded = u24_fold(version)
    if not folded or u24_already_carries(title, folded):
        return title
    return f"{title} ({version})" if title else version


#: What U24's real ``version_title`` returns, as literals, for shapes a bracketed test decides
#: differently from a substring test. Fields: Title column, version column, identity title.
U24_COMPOSITIONS: tuple[tuple[str, str, str], ...] = (
    ("Lively Up", "Live", "Lively Up (Live)"),
    ("Extended Play Track", "Extended", "Extended Play Track (Extended)"),
    ("Strobe (Michael Woods Remix)", "Michael Woods", "Strobe (Michael Woods Remix)"),
    ("Losing It (feat. Anna)", "Anna", "Losing It (feat. Anna) (Anna)"),
    ("Sun Path (Lively)", "Live", "Sun Path (Lively) (Live)"),
    ("Sun Path (Live with Strings)", "Live with Strings", "Sun Path (Live with Strings)"),
    ("Sun Path [Nightwave Remix]", "Nightwave Remix", "Sun Path [Nightwave Remix]"),
    ("Sun Path - Nightwave Remix", "Nightwave Remix",
     "Sun Path - Nightwave Remix (Nightwave Remix)"),
    ("Sun Path {Nightwave Remix}", "Nightwave Remix",
     "Sun Path {Nightwave Remix} (Nightwave Remix)"),
    ("Sun Path", "", "Sun Path"), ("", "Nightwave Remix", "Nightwave Remix"),
)


@pytest.mark.parametrize("title,version,expected", U24_COMPOSITIONS, ids=lambda v: str(v)[:32])
def test_this_files_imitation_of_the_recorder_still_composes_what_u24_composes(
    title, version, expected
):
    """This file's imitation of the recorder still composes what U24 composes, as literals from
    running U24's module, so it fails when either copy moves."""
    assert u24_version_title(title, version) == expected


def u24_records(artist: str, row_title: str, row_version: str = "") -> dict[str, str]:
    """What U24's recorder writes, derived the way it derives it. A SECOND implementation, not
    checked against the real recorder (the residual titled "The two tombstone derivations are
    reconciled
    only at merge")."""
    return {
        "artist": u24_fold(artist), "title": u24_fold(u24_version_title(row_title, row_version)),
    }


def u24_uncredited(artist: str, row_title: str, row_version: str = "") -> dict[str, str] | None:
    """The companion the recorder writes beside a credited tombstone: the composed title with every
    credit group taken out, folded, or None when nothing was taken out or left."""
    dropped: list[str] = []

    def keep_or_drop(found: re.Match[str]) -> str:
        group = found.group(1) if found.group(1) is not None else found.group(2)
        if u24_is_a_credit(group):
            dropped.append(group)
            return " "
        return found.group(0)

    stripped = u24_fold(U24_BRACKETED.sub(keep_or_drop, u24_version_title(row_title, row_version)))
    if not dropped or not stripped:
        return None
    return {"artist": u24_fold(artist), "title": stripped}


def reaches(
    wanted: match.Wanted, verbatim: dict[str, str], companion: dict[str, str] | None
) -> bool:
    """Whether either consult ``standing_tombstone`` makes lands on this deletion."""
    return verbatim in wanted.suppression_spellings or (
        companion is not None and companion in wanted.uncredited_spellings
    )


def every_reader_on(row: tuple[str, str, str, str, str]) -> tuple[match.Wanted, ...]:
    """One rekordbox row, named by a list arriving through all three readers."""
    _title, _version, listed, provider_title, provider_version = row
    return (
        match.read_text_lines(f"Aurora Bloom - {listed}\n")[0],
        match.read_spotify_items(
            [{"name": listed, "artists": [{"name": "Aurora Bloom"}]}]
        )[0],
        match.read_tidal_tracks(
            [{"title": provider_title, "version": provider_version,
              "artist": {"name": "Aurora Bloom"}}]
        )[0],
    )


@pytest.mark.parametrize("row_title", ROW_SPELLINGS)
def test_a_list_addresses_a_tombstone_the_way_a_deleted_row_actually_recorded_it(row_title):
    """A list addresses a tombstone the way a deleted row actually recorded it.

    The two sides can DERIVE different strings from one record, which misses silently, so this is
    driven from the row spelling through the real readers.
    """
    recorded = u24_records("Aurora Bloom", row_title)
    for wanted in (
        match.read_text_lines(f"Aurora Bloom - {row_title}\n")[0],
        match.read_spotify_items(
            [{"name": row_title, "artists": [{"name": "Aurora Bloom"}]}]
        )[0],
    ):
        assert recorded in wanted.suppression_spellings, (
            f"a tombstone recorded from the row {row_title!r} is addressed by "
            f"nothing this list produces: {wanted.suppression_spellings}"
        )


#: Every identity title the provider row for the Nightwave remix has to reach, as
#: LITERALS: building the expectation with the function under test asserts nothing.
PROVIDER_REACHES: tuple[str, ...] = (
    "sun path (nightwave remix)", "sun path [nightwave remix]", "sun path - nightwave remix",
)

#: The provider row those literals belong to.
PROVIDER_ROW = {"title": "Sun Path", "version": "Nightwave Remix",
                "artist": {"name": "Aurora Bloom"}}


@pytest.mark.parametrize("spelling", PROVIDER_REACHES)
def test_a_provider_row_reaches_every_spelling_of_the_version_it_names(spelling):
    """A provider row, which carries the version beside the title, reaches every spelling too; the
    composition once produced only the parenthesised identity and the version came back."""
    wanted = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert {"artist": "aurora bloom", "title": spelling} in wanted.suppression_spellings


def test_the_one_spelling_a_provider_row_cannot_reach_is_named_rather_than_assumed():
    """A gap stated is a gap somebody can close.

    The residual titled "A provider row cannot address a library row that kept a featured credit": a
    row that never spelled the credit has nothing to put back, a limit of the provider shape.
    """
    credited = {"artist": "aurora bloom", "title": "sun path (feat. mira) (nightwave remix)"}
    provider = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert credited not in provider.suppression_spellings
    spelled = match.read_text_lines("Aurora Bloom - Sun Path (feat. Mira) (Nightwave Remix)\n")[0]
    assert credited in spelled.suppression_spellings


#: Listings whose credit is not where ``_head_of`` looks, across all three readers, with the
#: exact addresses each may produce, as literals. The third column is the provider reader,
#: where the credit is discarded before the precondition can look at it.
CREDIT_OUTSIDE_THE_SUFFIX: tuple[
    tuple[str, tuple[str, str], tuple[str, ...], tuple[str, ...]], ...
] = (
    (
        "Sun Path (Live) (feat. Mira)", ("Sun Path (feat. Mira)", "Live"),
        ("Sun Path (Live) (feat. Mira)",),
        ("Sun Path (feat. Mira) (Live)", "Sun Path (feat. Mira) [Live]"),
    ),
    (
        "Sun Path [Live] (feat. Mira)", ("Sun Path (feat. Mira)", "Live"),
        ("Sun Path [Live] (feat. Mira)",),
        ("Sun Path (feat. Mira) (Live)", "Sun Path (feat. Mira) [Live]"),
    ),
        # The version arrives in more than one group, so there is no single suffix to take off.
    (
        "Sun Path (feat. Mira) (Extended) (Remastered)",
        ("Sun Path (feat. Mira)", "Extended Remastered"),
        ("Sun Path (feat. Mira) (Extended) (Remastered)",),
        (
            "Sun Path (feat. Mira) (Extended Remastered)",
            "Sun Path (feat. Mira) [Extended Remastered]",
            "Sun Path (feat. Mira) (Extended) (Remastered)",
            "Sun Path (feat. Mira) - Extended Remastered",
                        # The recorder's composition on the dash form keeps the credit.
            "Sun Path (feat. Mira) - Extended Remastered (Extended Remastered)",
        ),
    ),
)


@pytest.mark.parametrize(
    "listed,provider,spelled_addresses,provider_addresses", CREDIT_OUTSIDE_THE_SUFFIX
)
@pytest.mark.parametrize("origin", [match.TEXT, match.SPOTIFY, match.TIDAL])
def test_a_credited_listing_is_never_addressed_as_the_plain_record(
    origin, listed, provider, spelled_addresses, provider_addresses
):
    """A credited listing is never addressed as the plain record.

    ``_head_of`` takes the version off the END and a credit is not always last, so deleting the
    plain row suppressed a credited recording. Driven through all three readers, set asserted whole.
    """
    title, version = provider
    if origin == match.TIDAL:
        wanted = match.read_tidal_tracks(
            [{"title": title, "version": version, "artist": {"name": "Aurora Bloom"}}]
        )[0]
        expected = provider_addresses
    elif origin == match.SPOTIFY:
        wanted = match.read_spotify_items(
            [{"name": listed, "artists": [{"name": "Aurora Bloom"}]}]
        )[0]
        expected = spelled_addresses
    else:
        wanted = match.read_text_lines(f"Aurora Bloom - {listed}\n")[0]
        expected = spelled_addresses
    assert wanted.addresses == expected
    plain = {match.tombstone_fold(one) for one in ("Sun Path", "Sun Path (Live)",
                                                   "Sun Path (Extended) (Remastered)",
                                                   "Sun Path (Extended Remastered)")}
    assert not plain & {found["title"] for found in wanted.suppression_spellings}


@pytest.mark.parametrize(
    "listed,provider,spelled_addresses,provider_addresses", CREDIT_OUTSIDE_THE_SUFFIX
)
@pytest.mark.parametrize("origin", [match.TEXT, match.SPOTIFY, match.TIDAL])
def test_a_deletion_of_the_plain_record_never_withholds_a_credit_spelled_late(
    cfg, music, tmp_path, origin, listed, provider, spelled_addresses, provider_addresses
):
    """Deleting the plain record never withholds a credit spelled late, one list line per reader."""
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Extended) (Remastered)"), actor="deletion",
    )
    path = list_document(tmp_path, origin, listed, provider, "credited")
    _code, envelope = drive(["match", "run", path])
    assert len(envelope["data"]["missing"]) == 1, (
        "a deletion of the plain record silently withheld the credited one"
    )
    assert envelope["warnings"] == []


def list_document(
    tmp_path: Path, origin: str, listed: str, provider: tuple[str, str], name: str
) -> str:
    """One listing, written as the file the named reader actually reads."""
    if origin == match.TEXT:
        return write_list(tmp_path, f"Aurora Bloom - {listed}\n", f"{name}.txt")
    if origin == match.SPOTIFY:
        rows: list[dict] = [{"id": "sp1", "name": listed, "artists": [{"name": "Aurora Bloom"}]}]
    else:
        rows = [{"id": "1", "title": provider[0], "version": provider[1],
                 "artist": {"name": "Aurora Bloom"}}]
    return write_list(
        tmp_path, json.dumps({"list": 1, "origin": origin, "tracks": rows}),
        f"{name}-{origin}.json",
    )


def test_the_plain_record_is_still_suppressed_for_the_list_that_names_it(cfg, music, tmp_path):
    """The other half: a composition producing no address at all would pass every negative
    assertion above, so the list naming the deleted record must still reach it."""
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Extended) (Remastered)"), actor="deletion",
    )
    plain = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended) (Remastered)\n", "p.txt")
    _code, still = drive(["match", "run", plain])
    assert still["data"]["missing"] == []
    assert [w["code"] for w in still["warnings"]] == [match_cli.SUPPRESSED_WARNING]


@pytest.mark.parametrize(
    "listed,recorded_row",
    [
        ("Sun Path (feat. Mira) [Nightwave Remix]", "Sun Path (feat. Mira) (Nightwave Remix)"),
        ("Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path (feat. Mira) [Nightwave Remix]"),
    ],
    ids=["square-listed", "round-listed"],
)
def test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version(
    cfg, music, tmp_path, listed, recorded_row
):
    """What ``_head_of`` is for: a credited listing whose version IS a bracketed suffix, keeping the
    credit ``split_version`` took off. Losing either bracket shape makes the credited row
    unreachable."""
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", recorded_row),
        actor="deletion",
    )
    path = write_list(tmp_path, f"Aurora Bloom - {listed}\n", "credited.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


@pytest.mark.parametrize(
    "listed,dashed",
    [
        ("Sun Path (Live)", "sun path - live"),
        ("Sun Path [Instrumental]", "sun path - instrumental"),
    ],
)
def test_the_dash_spelling_of_a_bare_one_word_version_is_not_composed(listed, dashed):
    """The dash spelling of a bare one word version is not composed: ``split_ambiguous`` reads back
    by DECLARING it cannot tell, so it must not satisfy the gate and make ``Sun Path - Live``
    an address of the live cut."""
    assert (("artist", "aurora bloom"), ("title", dashed)) not in spellings_of(listed)


def test_every_row_spelling_is_addressed_from_every_reader_or_is_a_named_gap():
    """The derivation check that runs today: this side against ``u24_records`` over all three
    readers and every rekordbox row shape, driven from the row and its version column. The gaps
    are a literal tuple, so one going missing means a tombstone became invisible."""
    missed = tuple(
        (row[0], wanted.origin)
        for row in REKORDBOX_ROWS
        for wanted in every_reader_on(row)
        if not reaches(
            wanted, u24_records("Aurora Bloom", row[0], row[1]),
            u24_uncredited("Aurora Bloom", row[0], row[1]),
        )
    )
    assert missed == UNRECONCILED


def test_the_verbatim_consult_alone_still_misses_the_credited_row():
    """``UNRECONCILED`` going empty does not mean the verbatim consult widened: what closed the
    residual titled "A deleted track the tombstone consult cannot reach is listed for download" is a
    second record on the recorder's side, so a verbatim consult composing from the stripped title
    must fail here."""
    provider = match.read_tidal_tracks(
        [{"title": "Sun Path", "version": "Nightwave Remix", "artist": {"name": "Aurora Bloom"}}]
    )[0]
    credited = {"artist": "aurora bloom", "title": "sun path (feat. mira) (nightwave remix)"}
    assert credited not in provider.suppression_spellings
    assert {"artist": "aurora bloom", "title": "sun path (nightwave remix)"} in (
        provider.uncredited_spellings
    )


@pytest.mark.parametrize(
    "listed",
    [
        "Sun Path (feat. Zed) (Nightwave Remix)", "Sun Path (Nightwave Remix) (feat. Zed)",
        "Sun Path [ft. Zed] [Nightwave Remix]", "Sun Path (with Zed) - Nightwave Remix",
    ],
)
def test_a_listing_that_spelled_a_credit_never_asks_for_a_companion(listed):
    """A listing that spelled any credit never asks for a companion, which names no guest."""
    for wanted in (
        match.read_text_lines(f"Aurora Bloom - {listed}\n")[0],
        match.read_spotify_items([{"name": listed, "artists": [{"name": "Aurora Bloom"}]}])[0],
        match.read_tidal_tracks(
            [{"title": listed, "version": "", "artist": {"name": "Aurora Bloom"}}]
        )[0],
    ):
        assert wanted.uncredited_spellings == ()


def test_the_recorder_and_the_consulter_compose_the_same_string():
    """The recorder and the consulter compose the same string, as a LITERAL, for a row whose version
    lives only in the version column."""
    recorded = u24_version_title("Sun Path", "Nightwave Remix")
    assert recorded == "Sun Path (Nightwave Remix)"
    wanted = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert "Sun Path (Nightwave Remix)" in wanted.addresses


def test_the_only_doubled_address_is_the_one_the_recorder_actually_writes():
    """A doubled address is allowed for the dash form only: ``version_title`` short circuits on a
    BRACKETED question, so ``Sun Path - Nightwave Remix`` with a repeated version column composes
    the doubled string, while composing over a bracketed spelling would address nothing."""
    for wanted in (
        match.read_tidal_tracks([PROVIDER_ROW])[0],
        match.read_text_lines("Aurora Bloom - Sun Path (Nightwave Remix)\n")[0],
        match.read_text_lines("Aurora Bloom - Sun Path - Nightwave Remix\n")[0],
    ):
        doubled = [
            address for address in wanted.addresses
            if address.casefold().count("nightwave remix") > 1
        ]
        assert doubled in (
            [], ["Sun Path - Nightwave Remix (Nightwave Remix)"],
        ), f"a version was composed twice under a spelling nothing records: {doubled}"
                # Never onto a bracketed spelling, where the recorder short circuits.
        assert not [
            address for address in doubled
            if "(nightwave remix) (nightwave remix)" in address.casefold()
            or "[nightwave remix] (nightwave remix)" in address.casefold()
        ]
        # The dash double is actually reached, so this is not two negative clauses agreeing.
    assert "Sun Path - Nightwave Remix (Nightwave Remix)" in (
        match.read_tidal_tracks([PROVIDER_ROW])[0].addresses
    )


#: A title shape this side does not enumerate misses, recorded under "The recorder keeps the
#: Title column's own shape, so the consulter enumerates shapes".
UNENUMERATED_SHAPE = ("Sun Path {Nightwave Remix}", "Nightwave Remix")


def test_a_title_shape_outside_the_enumerated_ones_is_a_recorded_gap():
    """The boundary of the enumeration, asserted rather than assumed.

    A curly brace is not a bracket U24 reads, so the recorder COMPOSES; a source with a version
    field reaches it, a pasted line does not. That is the residual titled "The recorder keeps the
    Title
    column's own shape, so the consulter enumerates shapes", a limit of what this side can PARSE.
    """
    title, version = UNENUMERATED_SHAPE
    recorded = u24_records("Aurora Bloom", title, version)
    assert recorded["title"] == "sun path {nightwave remix} (nightwave remix)"
    listed = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert recorded not in listed.suppression_spellings
        # Nor does the list that spelled it the same way: no version this side reads.
    same = match.read_text_lines(f"Aurora Bloom - {title}\n")[0]
    assert recorded not in same.suppression_spellings
        # A source keeping its version in a field DOES reach it: a parsing edge, not a
        # composition edge.
    fielded = match.read_tidal_tracks(
        [{"title": title, "version": version, "artist": {"name": "Aurora Bloom"}}]
    )[0]
    assert recorded in fielded.suppression_spellings


@pytest.mark.parametrize(
    "recorded_title", ["sun path - nightwave remix", "sun path [nightwave remix]"],
)
def test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found(recorded_title):
    """A tombstone under a spelling the composition never produces is found, through resolution,
    where narrowing ``resolve_one`` to one spelling killed no test. The identity is a literal."""
    standing = {"artist": "aurora bloom", "title": recorded_title}

    def suppresses(kind, identity):
        return kind == match.TOMBSTONE_KIND and dict(identity) == standing

    found = match.resolve_one(
        match.read_tidal_tracks([PROVIDER_ROW])[0], match.LibraryIndex(by_recording={}),
        suppresses=suppresses, suppression_id=no_identifier,
    )
    assert found.state is match.MatchState.SUPPRESSED
    assert found.why is match.Why.TOMBSTONED


@pytest.mark.parametrize(
    "recorded_title,reachable",
    [
                # A two word tail ending in the vocabulary reads back as the plain record, so a
                # tombstone written from that row is reached.
        ("sun path - original mix", True),
        ("sun path - original version", True),
                # A bare one word tail outside the vocabulary reads as a TITLE. Composing it
                # anyway would let a deletion of somebody else's record withhold this one.
        ("sun path - original", False),
    ],
)
def test_a_dash_spelling_is_composed_only_when_this_module_reads_it_back(recorded_title, reachable):
    """A dash spelling is composed only when this module reads it back; brackets at the end of a
    title are a qualifier by convention and compose unconditionally."""
    spellings = frozen(match.read_text_lines("Aurora Bloom - Sun Path\n")[0].suppression_spellings)
    composed = (("artist", "aurora bloom"), ("title", recorded_title))
    assert (composed in spellings) is reachable


@pytest.mark.parametrize(
    "line,suppressed",
    [
                # The listing spells the version the way the tombstone was recorded, so it
                # addresses it and the deletion stands.
        ("Aurora Bloom - Sun Path (Live)", True),
        ("Aurora Bloom - Sun Path [Live]", True),
                # And the one refused on purpose. See below.
        ("Aurora Bloom - Sun Path - Live", False),
    ],
    ids=["round", "square", "ambiguous-dash"],
)
def test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one(
    cfg, music, tmp_path, line, suppressed
):
    """One ambiguity, one policy, driven at resolution: ``Sun Path - Live`` must not compose ``Sun
    Path (Live)``. A missed suppression re-acquires and REPORTS; an over eager one withholds
    silently."""
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    path = write_list(tmp_path, f"{line}\n", "gone.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    if suppressed:
        assert envelope["data"]["missing"] == []
        assert [w["suppression"] for w in warnings] == [recorded.suppression_id]
    else:
        assert warnings == []
        assert [row["why"] for row in envelope["data"]["missing"]] == [
            str(match.Why.NOT_IN_LIBRARY)
        ]
        assert envelope["data"]["missing"][0]["acquisition"], (
            "a missed suppression is the cheap side only because the run says "
            "what it is about to go and get"
        )


def test_neither_reading_of_an_ambiguous_title_composes_the_other_ones_address():
    """The same rule on the object, in both directions, as literals, so one function cannot be fixed
    while the other does the opposite."""
    dashed = spellings_of("Sun Path - Live")
    bracketed = spellings_of("Sun Path (Live)")
    assert (("artist", "aurora bloom"), ("title", "sun path (live)")) not in dashed
    assert (("artist", "aurora bloom"), ("title", "sun path [live]")) not in dashed
    assert (("artist", "aurora bloom"), ("title", "sun path - live")) not in bracketed
    assert not dashed & bracketed


def frozen(identities):
    return {tuple(sorted(identity.items())) for identity in identities}


def spellings_of(line: str) -> set:
    return frozen(match.read_text_lines(f"Aurora Bloom - {line}\n")[0].suppression_spellings)


def test_consulting_several_spellings_never_crosses_a_version_boundary():
    """Consulting several spellings never crosses a version boundary (KTD16).

    Inputs that actually HAVE several spellings, one axis apart: no qualifier, another qualifier,
    another recording, and the one word dash form.
    """
    remix = spellings_of("Sun Path (Nightwave Remix)")
    assert len(remix) > 1, "the input carries one spelling, so this bounds nothing"
    for stranger in (
        "Sun Path", "Sun Path (Someone Remix)", "Sun Pathway (Nightwave Remix)", "Sun Path - Live",
    ):
        other = spellings_of(stranger)
        assert len(other) > 1, f"{stranger!r} carries one spelling, so this bounds nothing"
        assert not remix & other, (
            f"a listing for the Nightwave remix addresses the same identity as "
            f"{stranger!r}, so one tombstone would suppress two versions"
        )


@pytest.mark.parametrize(
    "artist,title,version",
    [
        ("Aurora Bloom", "Sun Path", "Someone Remix"), ("Aurora Bloom", "Sun Path", ""),
        ("Aurora Bloom", "Sun Path", "Original Mix"),
        ("  Nova   Reef ", " Tide  Line ", "Extended Mix"), ("Caf\u00e9 del Mar", "Track", "Live"),
    ],
)
def test_a_composed_address_still_matches_a_row_spelled_that_way(artist, title, version):
    """``Original Mix`` is folded away for MATCHING but not for the tombstone, as in U24."""
    composed = match.listed_title(title.strip(), version)
    assert match.version_identity(artist=artist, title=composed) == u24_records(artist, composed)


def test_an_identity_with_neither_an_artist_nor_a_title_is_refused():
    """It would hash to one value and collapse the whole library onto it.

    U24 refuses this, so this side refuses it identically.
    """
    with pytest.raises(CratekitError) as excinfo:
        match.version_identity(artist="  ", title="")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_review_item_identity_is_not_the_tombstone_identity():
    """A review item answers a question and ``key_disagreement`` can move a track to needs review,
    so a key question is its own; sharing one identity let an answer at 08A settle a later 03B."""
    version = match.Why.VERSION_DIFFERS
    asked = one(version="Extended Mix", key="08A")
    assert set(asked.identity) == {"artist", "title"}
    assert set(asked.question(version)) == {"recording", "version", "key", "asks"}
    assert asked.question(version)["key"] == "08A"
        # The key set never varies and neither does the value: every value is read off the
        # LIST LINE, and a line naming no key carries the empty token, like an unreadable code.
    assert one(version="Extended Mix").question(version)["key"] == ""
    assert one(version="Extended Mix", key="8A").question(version) == asked.question(version)
    assert one(version="Extended Mix", key="03B").question(version) != asked.question(version)


def test_a_key_question_and_a_version_question_are_two_items_on_one_line():
    """Both carry the same recording, version token and key, so only ``asks`` tells them apart, as
    :data:`match.KEY_QUESTIONS` decides; the approximate and reading questions are two more."""
    asked = one(version="Extended Mix", key="08A")
    shapes = {
        why: asked.question(why)["asks"]
        for why in (
            match.Why.VERSION_DIFFERS, match.Why.KEY_RELATIVE, match.Why.KEY_DIFFERS,
            match.Why.TITLE_APPROXIMATE, match.Why.READING_AMBIGUOUS,
        )
    }
    assert shapes == {
        match.Why.VERSION_DIFFERS: match.ASKS_ABOUT_VERSION,
        match.Why.KEY_RELATIVE: match.ASKS_ABOUT_KEY, match.Why.KEY_DIFFERS: match.ASKS_ABOUT_KEY,
        match.Why.TITLE_APPROXIMATE: match.ASKS_ABOUT_RECORDING,
        match.Why.READING_AMBIGUOUS: match.ASKS_ABOUT_READING,
    }
        # Four identities, not five: the two key whys are one question wearing two reasons.
    identities = [asked.question(why) for why in shapes]
    assert len({tuple(sorted(found.items())) for found in identities}) == 4
    assert asked.question(match.Why.KEY_RELATIVE) == asked.question(match.Why.KEY_DIFFERS)
        # The version is still in it: two versions at one key are two questions.
    version = match.Why.VERSION_DIFFERS
    assert asked.question(version)["version"] == "extended mix"
    assert one(version="Radio Edit", key="08A").question(version) != asked.question(version)


@pytest.mark.parametrize(
    "why",
    [
        match.Why.EXACT, match.Why.NOT_IN_LIBRARY, match.Why.VERDICT_ACCEPTED,
        match.Why.VERDICT_REJECTED, match.Why.TOMBSTONED, match.Why.CANDIDATE_GONE,
        match.Why.VERDICT_UNSPECIFIC,
    ],
)
def test_a_row_that_is_not_a_question_has_no_review_item_identity(why):
    """A default here is an identifier somebody could answer.

    Matched and missing never reach the queue, so a fallback would hand each an identity that
    ``review resolve`` takes.
    """
    with pytest.raises(CratekitError) as excinfo:
        one(version="Extended Mix", key="08A").question(why)
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_key_folds_to_the_padded_form_and_an_unreadable_one_folds_to_nothing():
    """An absent key and an unparseable one behave identically, so they address alike."""
    assert match.key_token("8a") == match.key_token("08A") == "08A"
    assert match.key_token(None) == match.key_token("not a key") == ""


# ── Part 2: ownership is what the disk says ───────────────────────────────


def test_the_index_reads_the_filename_when_a_file_carries_no_tags(music):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.artist, row.title, row.version, row.key) for row in held] == [
        ("Aurora Bloom", "Sun Path", "Extended Mix", "08A")
    ]


def test_the_index_prefers_the_files_own_tags_over_a_misleading_filename(music, tmp_path):
    """The tag half of on-disk truth, against a real container: the tags are what the file says, and
    an empty file never reaches the production reader."""
    tagged_container(
        tmp_path, music / "08A - 124 - Typo Artist - Wrong Title.flac",
        artist="Aurora Bloom", title="Sun Path (Live)",
    )

    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.version) for row in held] == [("Sun Path", "Live")]
    assert index.versions(match.recording_token("Typo Artist", "Wrong Title")) == ()


def test_the_camelot_head_written_into_the_filename_is_the_librarys_key(music):
    hold(music, "03B - 120 - Aurora Bloom - Sun Path")
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert held[0].key == "03B"


# The headed title tag: the head inside the TITLE TAG comes off the way the stem's does


def headed_tag(music: Path, tmp_path: Path, name: str, *, artist: str, title: str) -> Path:
    """A real container carrying the given tags under ``name``. The live library writes the
    ``KEY - BPM - `` head into the title tag too, so a name only fixture proves nothing."""
    return tagged_container(tmp_path, music / f"{name}.flac", artist=artist, title=title)


def test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches(music, tmp_path):
    """The headed tag, first scenario: a head inside the tag is stripped, so a plain provider row
    matches instead of resolving offered or missing."""
    headed_tag(
        music, tmp_path, "06A - 126 - Felixcw - Dr. Beat",
        artist="Felixcw", title="06A - 126 - Dr. Beat",
    )

    index = index_of(music)
    held = index.versions(match.recording_token("Felixcw", "Dr. Beat"))
    assert [(row.artist, row.title, row.version, row.key) for row in held] == [
        ("Felixcw", "Dr. Beat", "", "06A")
    ]
    assert index.versions(match.recording_token("Felixcw", "06A - 126 - Dr. Beat")) == ()
    found = resolve([one(artist="Felixcw", title="Dr. Beat", origin=match.TIDAL)], index)
    assert found.matches[0].state is match.MatchState.MATCHED


def test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row(music, tmp_path):
    """U213. Both sides read the bracketed title through one function, so they converge."""
    headed_tag(
        music, tmp_path, "06A - 126 - Glass Animals - [Premade Sandwiches]",
        artist="Glass Animals", title="06A - 126 - [Premade Sandwiches]",
    )
    index = index_of(music)
    held = index.versions(match.recording_token("Glass Animals", "Premade Sandwiches"))
    assert [(row.title, row.version) for row in held] == [("Premade Sandwiches", "")]
    rows = match.read_tidal_tracks(
        [{"id": "5", "name": "[Premade Sandwiches]", "artist": {"name": "Glass Animals"}}]
    )
    assert resolve(rows, index).matches[0].state is match.MatchState.MATCHED


def test_a_head_only_in_the_filename_with_a_plain_tag_indexes_as_it_did(music, tmp_path):
    """The headed tag, second scenario: the change moves nothing that already worked."""
    headed_tag(
        music, tmp_path, "06A - 126 - Felixcw - Dr. Beat", artist="Felixcw", title="Dr. Beat"
    )
    held = index_of(music).versions(match.recording_token("Felixcw", "Dr. Beat"))
    assert [(row.artist, row.title, row.version, row.key) for row in held] == [
        ("Felixcw", "Dr. Beat", "", "06A")
    ]


def test_the_tempo_goes_with_the_head_and_a_number_opening_the_title_stays(music, tmp_path):
    """The headed tag, third scenario: ``50`` after the terminator is the title's own first word."""
    headed_tag(
        music, tmp_path, "10A - 100 - Mira Vale - 50 BPM Metronome",
        artist="Mira Vale", title="10A - 100 - 50 BPM Metronome",
    )
    index = index_of(music)
    held = index.versions(match.recording_token("Mira Vale", "50 BPM Metronome"))
    assert [row.title for row in held] == ["50 BPM Metronome"]
    found = resolve([one(artist="Mira Vale", title="50 BPM Metronome")], index)
    assert found.matches[0].state is match.MatchState.MATCHED


def test_a_title_that_genuinely_opens_with_a_camelot_code_and_a_number_is_read_as_a_head(
    music, tmp_path
):
    """A title genuinely opening with a Camelot code and a number reads as a head, a collision the
    filename side already accepts, named rather than hidden."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - 8A - 124 - Sun Path",
        artist="Aurora Bloom", title="8A - 124 - Sun Path",
    )
    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert index.versions(match.recording_token("Aurora Bloom", "8A - 124 - Sun Path")) == ()


def test_a_tag_that_is_only_a_head_falls_to_the_filename_the_way_an_empty_tag_does(music, tmp_path):
    """The headed tag, fourth scenario: a head only tag is treated as absent and falls to the
    filename."""
    headed_tag(
        music, tmp_path, "06A - 126 - Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title="06A - 126 -",
    )
    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.artist, row.title, row.key) for row in held] == [("Aurora Bloom", "Sun Path", "06A")]
    assert len(index) == 1


def test_a_plain_title_tag_is_untouched_by_the_head_strip(music, tmp_path):
    """The headed tag, fourth scenario's other half: a title with no head reads as it always has."""
    headed_tag(
        music, tmp_path, "08A - 124 - Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title="Sun Path - Radio Edit",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.version) for row in held] == [("Sun Path", "Radio Edit")]


def test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem(
    music, tmp_path
):
    """A head written as a suffix inside the tag comes off as it does from the stem.

    Both ends strip under the same rule, so the two surfaces cannot disagree about one file.
    """
    headed_tag(
        music, tmp_path, "Aurora Bloom - Sun Path - 08A - 124",
        artist="Aurora Bloom", title="Sun Path - 08A - 124",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [row.title for row in held] == ["Sun Path"]


def test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none(music, tmp_path):
    """The same bytes give the same key whether or not ``naming apply`` has run. The stem outranks
    the tag, and both outrank ``initialkey``."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - Sun Path", artist="Aurora Bloom", title="06A - 126 - Sun Path"
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.key) for row in held] == [("Sun Path", "06A")]


def test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag(music, tmp_path):
    tagged_container(
        tmp_path, music / "03B - 120 - Aurora Bloom - Sun Path.flac",
        artist="Aurora Bloom", title="06A - 126 - Sun Path", initialkey="09A",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [row.key for row in held] == ["03B"]
    tagged_container(
        tmp_path, music / "Aurora Bloom - Sun Path (Live).flac",
        artist="Aurora Bloom", title="06A - 126 - Sun Path (Live)", initialkey="09A",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert sorted(row.key for row in held) == ["03B", "06A"]


def test_a_title_that_genuinely_ends_with_a_camelot_code_and_a_number_loses_that_tail(
    music, tmp_path
):
    """A title genuinely ending with a Camelot code and a number loses that tail.

    Accepted for the tag as for the stem: one rule on both surfaces, so they cannot disagree.
    """
    headed_tag(
        music, tmp_path, "Aurora Bloom - Room - 12B - 100",
        artist="Aurora Bloom", title="Room - 12B - 100",
    )
    index = index_of(music)
    assert [row.title for row in index.versions(match.recording_token("Aurora Bloom", "Room"))] == ["Room"]
    assert index.versions(match.recording_token("Aurora Bloom", "Room - 12B - 100")) == ()


def test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template(music, tmp_path, cfg):
    """The template the verbs hand the index is the library's, marker included, for tag and stem."""
    marker = cfg.naming.lossy_marker
    headed_tag(
        music, tmp_path, f"08A - 124 - {marker} Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title=f"08A - 124 - {marker} Sun Path",
    )
    aware = match.index_library(music, template=match_cli.library_template(cfg))
    held = aware.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [row.title for row in held] == ["Sun Path"]


# The ISRC and the credited list: a held file resolves owned by the identity both sides
# carry, and by the primary artist's membership in the file's list


ISRC_RESIDUAL = (
    "The match engine never consults the ISRC, and a processed file's artist tag "
    "lists every credited artist, so a quarter of the hearts the library holds "
    "read missing or offered"
)


def credited(
    music: Path, tmp_path: Path, name: str, *, artist: str, title: str, isrc: str | None
) -> Path:
    """A real container the way the live library holds a processed file: the artist tag lists every
    credit, the title tag carries the head, and ``isrc=None`` is a real population."""
    fields = {"artist": artist, "title": title}
    if isrc is not None:
        fields["isrc"] = isrc
    return tagged_container(tmp_path, music / f"{name}.flac", **fields)


def burning(music: Path, tmp_path: Path, *, isrc: str | None = "USNRS2644532") -> Path:
    """The brief's file: ``Malive, Tito Azevedo, MRQZ`` against a row naming ``Malive``."""
    return credited(
        music, tmp_path, "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix)",
        artist="Malive, Tito Azevedo, MRQZ", title="04A - 126 - Burning (Extended Mix)", isrc=isrc,
    )


def row(*, artist: str, title: str, isrc: str | None, key=None) -> match.Wanted:
    """A provider row through the REAL reader, so it carries what a provider row carries."""
    shaped = {"id": "301", "artist": {"name": artist}, "title": title, "isrc": isrc, "key": key}
    return match.read_row(shaped, origin=match.TIDAL, position=1)


def test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says(music, tmp_path):
    """First scenario: the credited list defeats text comparison, and both sides carry the ISRC."""
    burning(music, tmp_path)

    index = index_of(music)
    assert [held.isrc for held in index.held_by_isrc("USNRS2644532")] == ["USNRS2644532"]
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")], index
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.MATCHED
    assert one_match.why is match.Why.ISRC_EXACT
    assert [Path(p).name for p in one_match.paths] == [
        "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac"
    ]


def test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member(
    music, tmp_path
):
    """Second scenario: with no ISRC tag the credited list rule holds the file by membership."""
    burning(music, tmp_path, isrc=None)

    index = index_of(music)
    assert index.held_by_isrc("USNRS2644532") == ()
        # The untagged file is not indexed under an empty key, or a row with no ISRC would be
        # held by every file with no tag.
    assert "" not in index.by_isrc
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")], index
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.MATCHED
    assert one_match.why is match.Why.CREDITED_EXACT
    assert len(one_match.paths) == 1


def test_the_primary_artist_need_not_be_first_in_the_credited_list(music, tmp_path):
    """Third scenario: the primary artist need not be first in the credited list."""
    credited(
        music, tmp_path, "07A - 128 - Traumer, antraum, Anton - Hyaku",
        artist="Traumer, antraum, Anton", title="07A - 128 - Hyaku", isrc=None,
    )
    found = resolve([row(artist="antraum", title="Hyaku", isrc=None)], index_of(music))
    assert found.matches[0].state is match.MatchState.MATCHED


def test_a_different_recording_sharing_the_title_under_another_isrc_is_not_owned(music, tmp_path):
    """Fourth scenario: another ISRC and an artist outside the file's list is not owned."""
    credited(
        music, tmp_path, "09A - 124 - Nova Reef - Burning (Extended Mix)",
        artist="Nova Reef", title="09A - 124 - Burning (Extended Mix)", isrc="GBAYE0000001",
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is not match.MatchState.MATCHED
    assert one_match.paths == ()


def test_an_isrc_hit_still_asks_about_the_key(music, tmp_path):
    """The ISRC settles the recording and version but not the key, which is the library's own
    statement, so a relative minor row is still a KEY_RELATIVE question."""
    burning(music, tmp_path)
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532", key="04B")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.NEEDS_REVIEW
    assert one_match.why is match.Why.KEY_RELATIVE
    assert [c.difference for c in one_match.candidates] == [match.Why.KEY_RELATIVE]


def test_a_rows_isrc_is_folded_before_it_is_asked(music, tmp_path):
    """A hyphenated, lower case ISRC on the row is the same identity.

    The tag reader and the missing verb fold this way, and a third spelling would be a third
    place to disagree.
    """
    burning(music, tmp_path)
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="us-nrs-26-44532")],
        index_of(music),
    )
    assert found.matches[0].why is match.Why.ISRC_EXACT


def test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone(
    music, tmp_path
):
    """The ISRC clause of the candidate labeller on its own: a ``Various Artists`` copy with the
    row's ISRC and title names no member, so only the ISRC says it is the recording."""
    credited(
        music, tmp_path, "07B - 126 - Various Artists - Burning (Extended Mix)",
        artist="Various Artists", title="07B - 126 - Burning (Extended Mix)", isrc="USNRS2644532",
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532", key="07A")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.NEEDS_REVIEW
    assert one_match.why is match.Why.KEY_RELATIVE
    assert [c.difference for c in one_match.candidates] == [match.Why.KEY_RELATIVE]


def test_a_files_isrc_tag_is_folded_before_it_is_indexed(music, tmp_path):
    """The file side of the fold: a hyphenated, lower case ISRC tag keys as the bare one."""
    credited(
        music, tmp_path, "04A - 126 - Malive - Burning (Extended Mix)",
        artist="Malive, Tito Azevedo, MRQZ", title="04A - 126 - Burning (Extended Mix)",
        isrc="us-nrs-26-44532",
    )
    index = index_of(music)
    assert list(index.by_isrc) == ["USNRS2644532"]
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")], index
    )
    assert found.matches[0].why is match.Why.ISRC_EXACT


def test_a_malformed_isrc_tag_is_not_an_identity(music, tmp_path):
    """A catalogue number in the ISRC tag is not a recording's identity and is dropped, as
    ``source.isrc_for`` drops it, so junk on a row does not match a file through it."""
    credited(
        music, tmp_path, "09A - 124 - Nova Reef - Tide",
        artist="Nova Reef", title="09A - 124 - Tide", isrc="CAT-001",
    )
    index = index_of(music)
    assert index.held_by_isrc(match.isrc_token("CAT-001")) == ()
    assert match.isrc_token("CAT-001") == ""
        # Not in the map under any spelling: a junk key nothing asks for is still trusted later.
    assert index.by_isrc == {}
    found = resolve([row(artist="Someone Else", title="Tide", isrc="CAT-001")], index)
    assert found.matches[0].state is not match.MatchState.MATCHED


def test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one(
    music, tmp_path
):
    """The credited list rule finds the RECORDING, so a file at another version is the version
    question R11 asks, and its candidate says so rather than reporting a scored hit."""
    credited(
        music, tmp_path, "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Radio Edit)",
        artist="Malive, Tito Azevedo, MRQZ", title="04A - 126 - Burning (Radio Edit)", isrc=None,
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.NEEDS_REVIEW
    assert one_match.why is match.Why.VERSION_DIFFERS
    assert [c.difference for c in one_match.candidates] == [match.Why.VERSION_DIFFERS]


def test_membership_is_whole_names_not_substrings(music, tmp_path):
    """``Tito`` is not a member of ``Malive, Tito Azevedo, MRQZ``: membership is whole names, not
    substrings, or a solo artist would be handed every collaboration naming them."""
    burning(music, tmp_path, isrc=None)
    found = resolve(
        [row(artist="Tito", title="Burning (Extended Mix)", isrc=None)], index_of(music)
    )
    assert found.matches[0].state is not match.MatchState.MATCHED


def test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing(music, tmp_path):
    """A single artist file has a list of one, so the credited rule moves nothing."""
    credited(
        music, tmp_path, "08A - 124 - Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title="08A - 124 - Sun Path", isrc="ZZ0000000001",
    )
    index = index_of(music)
    assert len(index) == 1
    (held,) = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert match.credited_members(held.artist) == ("Aurora Bloom",)
    assert held.members == frozenset({"aurora bloom"})
    assert held.isrc == "ZZ0000000001"
    assert index.held("Aurora Bloom", "Sun Path") == (held,)


def test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match(music, tmp_path):
    """An ISRC hit whose title disagrees is a question, with the file named.

    A bootleg ingested with the original's tags would otherwise point the paths at the wrong
    recording and the heart would never be acquired.
    """
    credited(
        music, tmp_path, "09A - 124 - Nova Reef - Tide",
        artist="Nova Reef", title="09A - 124 - Tide", isrc="USNRS2644532",
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.NEEDS_REVIEW
    assert one_match.why is match.Why.TITLE_APPROXIMATE
    assert [Path(p).name for c in one_match.candidates for p in c.paths] == [
        "09A - 124 - Nova Reef - Tide.flac"
    ]
    assert [c.difference for c in one_match.candidates] == [match.Why.TITLE_APPROXIMATE]


def test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone(music, tmp_path):
    """The ISRC settles the version however the file spells it, so only the key is left to ask,
    and the candidate says what the match says."""
    credited(
        music, tmp_path, "04A - 126 - Malive - Burning (Original Mix)",
        artist="Malive", title="04A - 126 - Burning (Original Mix)", isrc="USNRS2644532",
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532", key="04B")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.NEEDS_REVIEW
    assert one_match.why is match.Why.KEY_RELATIVE
    assert [c.difference for c in one_match.candidates] == [match.Why.KEY_RELATIVE]


def test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other(music, tmp_path):
    """An ISRC settled row lists the files carrying the ISRC and no other.

    The untagged copy's key does not join the disagreement over a row the ISRC settled.
    """
    burning(music, tmp_path)
    credited(
        music, tmp_path, "archive/07B - 126 - Malive - Burning (Extended Mix)",
        artist="Malive", title="07B - 126 - Burning (Extended Mix)", isrc=None,
    )
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532", key="04A")],
        index_of(music),
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.MATCHED
    assert one_match.why is match.Why.ISRC_EXACT
    assert [Path(p).name for p in one_match.paths] == [
        "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac"
    ]


def test_an_empty_isrc_token_asks_the_index_nothing(music):
    """A hand built index with an empty key still answers nothing to an empty token: the lookup
    guard stands on its own."""
    held = match.Owned(path=music / "x.flac", artist="A", title="T", version="", key=None)
    index = match.LibraryIndex(by_recording={}, by_isrc={"": (held,)})
    assert index.held_by_isrc("") == ()
    assert index.held_by_isrc(match.isrc_token(None)) == ()


def test_the_reader_opens_the_container_once_for_all_four_fields(music, tmp_path, monkeypatch):
    """The reader opens the container once for all four fields (the residual titled "The index reader opens
    every container three times, and the walk is the library"); the ISRC must not be a fourth
    open."""
    burning(music, tmp_path)
    import mutagen

    opened: list[Path] = []
    real = mutagen.File

    def counting(path, *args, **kwargs):
        opened.append(Path(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(mutagen, "File", counting)
    index_of(music)
    assert len(opened) == 1


def test_a_file_the_containers_table_does_not_name_is_not_in_the_library(music):
    (music / "notes.txt").write_text("not audio")
    assert len(index_of(music)) == 0


def test_ownership_is_membership_rather_than_a_filter_somebody_applies(music):
    """Ownership is membership rather than a filter: a caller that forgets a FILTER gets a plausible
    answer, one that forgets a LOOKUP gets nothing and notices."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert index.versions(match.recording_token("Nobody", "Nothing")) == ()


#: Everything that can read a rekordbox export: the package's byte engine, the standard
#: library parser and the third party one. Matched as PREFIXES, since ``xml`` and
#: ``xml.etree.ElementTree`` are one dependency.
EXPORT_READERS = ("cratekit.write.rbxml", "xml", "lxml")


#: The calls that import a module from a STRING at run time, which a guard reading only
#: import statements would miss.
_DYNAMIC_IMPORTS = ("import_module", "__import__")


def _source_of(dotted: str) -> str | None:
    """The source of a first-party module, so the walk can follow it."""
    base = SRC_ROOT.joinpath(*dotted.split("."))
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.is_file():
            return candidate.read_text()
    return None


def _imports_of(source: str, *, package: str) -> set[str]:
    """Every module this source binds, with relative imports resolved.

    ``package`` is what a relative import is relative TO; without it ``from ..write import
    rbxml`` matches nothing.
    """
    reached: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            reached.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split(".")
                anchor = ".".join(parts[: len(parts) - node.level + 1])
                module = f"{anchor}.{node.module}" if node.module else anchor
            else:
                module = node.module or ""
            if not module:
                continue
            reached.add(module)
            reached.update(f"{module}.{alias.name}" for alias in node.names)
        elif isinstance(node, ast.Call):
            named = node.func.attr if isinstance(node.func, ast.Attribute) else (
                node.func.id if isinstance(node.func, ast.Name) else ""
            )
            if named in _DYNAMIC_IMPORTS:
                reached.update(
                    argument.value
                    for argument in node.args
                    if isinstance(argument, ast.Constant) and isinstance(argument.value, str)
                )
    return reached


def reaches_an_export_reader(source: str, *, package: str = "cratekit.acquire") -> set[str]:
    """Which export reader this source binds to, in any shape and at any depth.

    Bound through the import graph, not attribute names: relative imports resolved, the walk
    transitive, ``importlib.import_module`` caught. ``open`` imports nothing, so a second guard
    covers string literals.
    """
    reached: set[str] = set()
    pending = [(source, package)]
    seen: set[str] = set()
    while pending:
        text, where = pending.pop()
        for name in _imports_of(text, package=where):
            if name in reached:
                continue
            reached.add(name)
            if not name.startswith("cratekit.") or name in seen:
                continue
            seen.add(name)
            followed = _source_of(name)
            if followed is not None:
                pending.append((followed, name.rpartition(".")[0] or name))
    return {
        name
        for name in reached
        for head in EXPORT_READERS
        if name == head or name.startswith(f"{head}.")
    }


#: What an export looks like as TEXT, for the route no import guard can see: a module
#: opening a collection file and picking it apart with a regular expression must name it.
_EXPORT_TEXT = re.compile(r"\.xml\b|rekordbox|DJ_PLAYLISTS|<COLLECTION|<TRACK\b", re.IGNORECASE)


def _docstrings(tree: ast.AST) -> set[int]:
    """Every docstring node's id, so prose about an export is not a defect."""
    found: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = getattr(node, "body", None) or []
        first = body[0] if body else None
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            found.add(id(first.value))
    return found


def names_an_export_in_text(source: str) -> list[int]:
    """Lines where this source names an export file or its markup, docstrings aside: ``open``
    plus a regular expression reaches no parser and is the same defect."""
    tree = ast.parse(source)
    prose = _docstrings(tree)
    return sorted(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in prose
        and _EXPORT_TEXT.search(node.value)
    )


@pytest.mark.parametrize(
    "source",
    [
        "import xml.etree.ElementTree as ET\nET.parse(p)\n",
        "import lxml.etree\n",
        "from lxml import etree as ET\n",
        "from xml.etree import ElementTree\n",
        "import cratekit.write.rbxml as bridge\n",
        "from cratekit.write import rbxml\n",
        "from cratekit.write.rbxml import root_node\n",
        "from ..write import rbxml\n",
        "from ..write.rbxml import root_node\n",
        "from . import rbxml\n",
                # Transitive: trees imports rbxml at module scope.
        "from cratekit.write import trees\n",
        "import cratekit.write.trees\n",
                # Dynamic, where the module name is a string.
        'importlib.import_module("lxml.etree")\n',
        '__import__("xml.etree.ElementTree")\n',
    ],
)
def test_the_export_guard_bites_on_every_import_shape(source):
    """The export guard bites on every import shape, not only on correct code: running it against
    the evasion is what proves it a guard."""
    assert reaches_an_export_reader(source, package="cratekit.write")


@pytest.mark.parametrize(
    "source",
    [
        "from cratekit.core import naming, tags\n", "import hashlib\nimport unicodedata\n",
        "row = something.xml\n",
        '"""Prose about an xml export and about lxml, in a docstring."""\n',
        "from cratekit.core.review import DecisionStore\n", "from . import match\n",
    ],
)
def test_the_export_guard_stays_quiet_on_correct_code(source):
    """A guard that fires on correct code is a guard somebody routes around."""
    assert not reaches_an_export_reader(source)


@pytest.mark.parametrize(
    "source",
    [
        'raw = open("Collection.xml").read()\n', 'path = root / "rekordbox.xml"\n',
        're.findall(r"<TRACK Location=", raw)\n',
    ],
)
def test_the_text_guard_bites_on_an_export_read_with_no_parser_at_all(source):
    """The route the import guard cannot see, guarded on its own terms: ``open`` plus a regular
    expression imports nothing, so what is checked is whether the module names an export."""
    assert names_an_export_in_text(source)


@pytest.mark.parametrize(
    "source",
    [
        '"""Prose about a rekordbox.xml export, in a docstring."""\n', 'suffix = ".flac"\n',
        'origin = "tidal"\n',
    ],
)
def test_the_text_guard_leaves_prose_and_ordinary_literals_alone(source):
    assert not names_an_export_in_text(source)


def test_the_match_engine_never_reaches_a_rekordbox_export():
    """Approach point 1: ownership is the disk, never a document that can lag. This module cannot
    reach an export reader in any import shape or depth, nor name one as text."""
    for source in (*MATCH_SOURCES, MATCH_CLI_SOURCE):
        assert reaches_an_export_reader(source.read_text()) == set(), source.name
        assert names_an_export_in_text(source.read_text()) == [], source.name


def test_the_transitive_walk_actually_walks():
    """The transitive walk is proved against the REAL package: ``cratekit.write.trees`` imports the
    byte engine, so a guard reading one file would call a module importing it quiet."""
    assert "cratekit.write.rbxml" in _imports_of(
        _source_of("cratekit.write.trees"), package="cratekit.write"
    )
    assert reaches_an_export_reader("from cratekit.write import trees\n")


# A resolution that owns a row retires the question an earlier run asked about it (the
# residual titled "A review item outlives its question: a later resolution that owns the row leaves
# the version-match item open, and no verdict or predicate can retire it honestly").


def _adjudicated(store, wanted, index) -> match.TrackMatch:
    return match_cli.adjudicate(
        store, resolve([wanted], index), handler_key="acquire.match.run",
        suppresses=nothing_suppressed, suppression_id=no_identifier,
    ).matches[0]


def _ask_about_burning(store, music) -> match.TrackMatch:
    """Put the brief's row in front of a person: the library holds the radio edit and the row
    asks for the extended mix, a VERSION question with one open item."""
    hold(music, "04A - 126 - Malive - Burning (Radio Edit)")
    asked = _adjudicated(
        store, row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
        index_of(music),
    )
    assert asked.state is match.MatchState.NEEDS_REVIEW
    assert asked.why is match.Why.VERSION_DIFFERS
    assert [one.item_id for one in review.list_items(store)] == [asked.item_id]
    return asked


@pytest.mark.parametrize(
    ("isrc_on_the_file", "rule"),
    [("USNRS2644532", match.Why.ISRC_EXACT), (None, match.Why.CREDITED_EXACT)],
    ids=["isrc-exact", "credited-exact"],
)
def test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule(
    cfg, music, tmp_path, isrc_on_the_file, rule
):
    """The brief's first scenario, under both rules the live measurement found: the ISRC rule
    and the credited one."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        burning(music, tmp_path, isrc=isrc_on_the_file)
        owned = _adjudicated(
            store, row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
            index_of(music),
        )
        assert (owned.state, owned.why) == (match.MatchState.MATCHED, rule)
        assert owned.item_id is None, "an owned row is not a question and names no item"

        assert [one.item_id for one in review.list_items(store)] == []
        assert [one.item_id for one in review.list_items(store, include_suppressed=True)] == []
        retired = review.get(store, asked.item_id)
        assert retired.verdict is review.Verdict.SUPERSEDED
        assert retired.actor == str(rule)
        assert retired.option is None


def test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated(cfg, music, tmp_path):
    """The brief's second scenario, at the seam: the row resolved twice more leaves one item,
    still retired."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        burning(music, tmp_path)
        line = row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")
        for _ in range(2):
            owned = _adjudicated(store, line, index_of(music))
            assert owned.why is match.Why.ISRC_EXACT
        everything = review.list_items(store, include_resolved=True, limit=None).items
        assert [one.item_id for one in everything] == [asked.item_id]
        assert everything[0].verdict is review.Verdict.SUPERSEDED


def test_a_persons_answer_is_never_overwritten_by_a_later_resolution(cfg, music, tmp_path):
    """The brief's fourth scenario, at the seam: a rejection recorded before the ISRC file
    arrived stands, with its actor, after the rule owns the row."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        review.resolve(store, asked.item_id, review.Verdict.REJECTED, actor="phillip")
        burning(music, tmp_path)
        owned = _adjudicated(
            store, row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
            index_of(music),
        )
        assert owned.why is match.Why.ISRC_EXACT
        kept = review.get(store, asked.item_id)
        assert kept.verdict is review.Verdict.REJECTED
        assert kept.actor == "phillip"


def test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection(
    cfg, music, tmp_path
):
    """A retired question the row asks again is reopened, not read as a rejection.

    Left standing, the machine's verdict would reach ``apply_verdict`` as a rejection nobody made.
    """
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        carrying = burning(music, tmp_path)
        line = row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")
        assert _adjudicated(store, line, index_of(music)).why is match.Why.ISRC_EXACT
        assert review.get(store, asked.item_id).verdict is review.Verdict.SUPERSEDED

        carrying.unlink()
        again = _adjudicated(store, line, index_of(music))
        assert (again.state, again.why) == (
            match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS,
        )
        assert again.item_id == asked.item_id
        reopened = review.get(store, asked.item_id)
        assert reopened.verdict is None
        assert reopened.actor == "acquire.match.run"
        assert [one.item_id for one in review.list_items(store)] == [asked.item_id]


def test_a_retired_question_whose_row_goes_missing_keeps_the_verdict(cfg, music, tmp_path):
    """The cost recorded, not the feature: the residual titled "A superseded verdict outlives its rule when
    the row goes missing rather than back to a question". The assertion flips with it."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        carrying = burning(music, tmp_path)
        line = row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")
        assert _adjudicated(store, line, index_of(music)).why is match.Why.ISRC_EXACT
        carrying.unlink()
        (music / "04A - 126 - Malive - Burning (Radio Edit).flac").unlink()
        gone = _adjudicated(store, line, index_of(music))
        assert (gone.state, gone.why) == (match.MatchState.MISSING, match.Why.NOT_IN_LIBRARY)
        kept = review.get(store, asked.item_id)
        assert kept.verdict is review.Verdict.SUPERSEDED
        assert kept.actor == "isrc-exact"
        assert [one.item_id for one in review.list_items(store)] == []


def test_a_persons_acceptance_being_applied_retires_nothing(cfg, music, tmp_path):
    """A person's acceptance being applied retires nothing: ``OWNING_RULES`` is a positive set, so
    the guard is the recognition and not the second layer."""
    assert match.Why.VERDICT_ACCEPTED not in match.OWNING_RULES
    assert match.OWNING_RULES == frozenset(
        {match.Why.EXACT, match.Why.ISRC_EXACT, match.Why.CREDITED_EXACT}
    )
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        (candidate,) = asked.candidates
        review.resolve(
            store, asked.item_id, review.Verdict.ACCEPTED,
            option=candidate.candidate_id, actor="phillip",
        )
        applied = _adjudicated(
            store, row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
            index_of(music),
        )
        assert (applied.state, applied.why) == (
            match.MatchState.MATCHED, match.Why.VERDICT_ACCEPTED,
        )
        kept = review.get(store, asked.item_id)
        assert kept.verdict is review.Verdict.ACCEPTED
        assert kept.actor == "phillip"


def test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue():
    """Every caller of ``adjudicate`` gates on the rows that touch the queue, or an owned row
    reaches the retirement from ``match run`` alone."""
    callers = [
        path
        for path in (REPO_ROOT / "src" / "cratekit").rglob("*.py")
        if "match_cli.adjudicate(" in path.read_text(encoding="utf-8")
    ]
    assert len(callers) >= 4, [path.name for path in callers]
    for path in callers:
        text = path.read_text(encoding="utf-8")
                # As many gates as calls: the missing pass calls ``adjudicate`` twice.
        assert text.count("match_cli.touches_the_queue(") >= text.count(
            "match_cli.adjudicate("
        ), path
        assert "resolved.of(match.MatchState.NEEDS_REVIEW):" not in text, path


def test_the_gate_predicate_admits_a_question_and_a_rule_owned_row_and_nothing_else():
    line = one()
    def shaped(state, why):
        return match.TrackMatch(wanted=line, state=state, why=why)
    assert match_cli.touches_the_queue(
        shaped(match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)
    )
    for why in match.OWNING_RULES:
        assert match_cli.owned_by_a_rule(shaped(match.MatchState.MATCHED, why))
        assert match_cli.touches_the_queue(shaped(match.MatchState.MATCHED, why))
    assert not match_cli.owned_by_a_rule(
        shaped(match.MatchState.MATCHED, match.Why.VERDICT_ACCEPTED)
    )
    assert not match_cli.touches_the_queue(
        shaped(match.MatchState.MATCHED, match.Why.VERDICT_ACCEPTED)
    )
    assert not match_cli.touches_the_queue(
        shaped(match.MatchState.MISSING, match.Why.NOT_IN_LIBRARY)
    )
    assert not match_cli.touches_the_queue(
        shaped(match.MatchState.SUPPRESSED, match.Why.TOMBSTONED)
    )


def test_every_question_identity_is_one_per_shape_and_agrees_with_the_asked_one():
    """Every question identity is one per shape and agrees with the asked one, or a retirement
    looks under an identifier nothing wrote."""
    line = one(artist="Aurora Bloom", title="Sun Path", version="Extended Mix", key="08A")
    identities = line.questions()
    assert [identity["asks"] for identity in identities] == list(match.QUESTION_SHAPES)
    assert len({json.dumps(identity, sort_keys=True) for identity in identities}) == 4
    for why in (
        match.Why.KEY_DIFFERS, match.Why.KEY_RELATIVE, match.Why.VERSION_DIFFERS,
        match.Why.TITLE_APPROXIMATE, match.Why.READING_AMBIGUOUS,
    ):
        assert line.question(why) in identities


def test_the_verb_lists_a_retired_question_only_when_asked_for_everything(cfg, music, tmp_path):
    """End to end through ``match run`` and ``review list``: the item a first run filed leaves
    the open list when a second run owns the row, and reads the third verdict under ``--all``."""
    hold(music, "04A - 126 - Malive - Burning (Radio Edit)")
    listing = write_list(
        tmp_path,
        json.dumps({
            "list": 1, "origin": match.TIDAL,
            "tracks": [{
                "id": "301", "artist": {"name": "Malive"},
                "title": "Burning (Extended Mix)", "isrc": "USNRS2644532",
            }],
        }),
        "burning.json",
    )
    code, first = drive(["match", "run", listing])
    assert code == int(ExitCode.PENDING_HUMAN)
    item_id = first["data"]["needs_review"][0]["review_item"]
    _code, listed = drive(["review", "list"])
    assert [one["id"] for one in listed["data"]["items"]] == [item_id]

    burning(music, tmp_path)
    code, second = drive(["match", "run", listing])
    assert code == int(ExitCode.OK)
    assert second["data"]["matched"][0]["why"] == "isrc-exact"
    assert second["data"]["needs_review"] == []

    _code, listed = drive(["review", "list"])
    assert listed["data"]["items"] == []
    _code, suppressed = drive(["review", "list", "--suppressed"])
    assert suppressed["data"]["items"] == []
    _code, everything = drive(["review", "list", "--all"])
    (retired,) = everything["data"]["items"]
    assert retired["id"] == item_id
    assert retired["verdict"] == "superseded"
    assert retired["actor"] == "isrc-exact"


# ── Part 3: the three states ─────────────────────────────────────────────────


def test_an_exact_version_is_matched_and_asks_nobody(music):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.why is match.Why.EXACT
    assert found.candidates == ()


def test_a_track_owned_only_as_a_different_remix_needs_review_and_names_the_difference(music):
    """AE8, and the whole reason this unit exists: the source system treats this as owned, so the
    user finds out at the gig that the file is not the record they queued."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.VERSION_DIFFERS
    assert [c.version for c in found.candidates] == ["Someone Remix"]
    assert found.candidates[0].difference is match.Why.VERSION_DIFFERS


def test_a_relative_key_disagreement_surfaces_rather_than_picking_one(music):
    """The trap: 8A and 8B share a wheel position and every note, but are the minor and the
    major recording, so comparing wheel numbers would call them the same key."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    found = resolve([one(key="8B")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.KEY_RELATIVE


def test_a_key_that_disagrees_outright_is_a_different_answer(music):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    found = resolve([one(key="3B")], index_of(music)).matches[0]
    assert found.why is match.Why.KEY_DIFFERS


@pytest.mark.parametrize("first_folder", ["A archive", "C archive"], ids=["sorts-first", "sorts-last"])
def test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first(
    music, first_folder
):
    """The key check reads every held copy rather than whichever sorted first, over both orders."""
    (music / first_folder).mkdir()
    (music / "B sorted").mkdir()
    (music / first_folder / "Aurora Bloom - Sun Path.flac").write_bytes(b"")
    (music / "B sorted" / "03A - 124 - Aurora Bloom - Sun Path.flac").write_bytes(b"")
    found = resolve([one(key="08A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.KEY_DIFFERS


def test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present(music):
    """The relative key wins the reporting when both disagreements are present, not by sort luck."""
    hold(music, "08B - 124 - Aurora Bloom - Sun Path")
    (music / "03A - 124 - Aurora Bloom - Sun Path.mp3").write_bytes(b"")
    found = resolve([one(key="08A")], index_of(music)).matches[0]
    assert found.why is match.Why.KEY_RELATIVE


def test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries(music):
    """A candidate shows a key true of every path it carries: grouping by version alone showed the
    first file's key over every path. A candidate is one version at one key."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    (music / "03A - 124 - Aurora Bloom - Sun Path (Someone Remix).mp3").write_bytes(b"")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert sorted(c.key for c in found.candidates) == ["03A", "08A"]
    for candidate in found.candidates:
        assert all(Path(p).name.startswith(candidate.key) for p in candidate.paths)
    assert len({c.candidate_id for c in found.candidates}) == 2


def test_an_absent_key_on_either_side_is_not_a_disagreement(music):
    """Otherwise most of a real playlist lands in the queue."""
    hold(music, "Aurora Bloom - Sun Path")
    assert resolve([one(key="8B")], index_of(music)).matches[0].state is match.MatchState.MATCHED
    hold(music, "08A - 124 - Nova Reef - Tide Line")
    same = resolve([one(artist="Nova Reef", title="Tide Line")], index_of(music))
    assert same.matches[0].state is match.MatchState.MATCHED


def test_key_disagreement_is_silent_about_a_code_it_cannot_parse():
    assert match.key_disagreement("8A", "not a key") is None
    assert match.key_disagreement("", "8A") is None
    assert match.key_disagreement("08a", "8A") is None


def test_an_approximate_hit_is_a_question_and_never_a_match(music):
    """A fuzzy or substring hit is discovery. It is never an identity."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Pathway")
    found = resolve([one(title="Sun Path")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert found.candidates[0].difference is match.Why.TITLE_APPROXIMATE
    assert found.candidates[0].title == "Sun Pathway"


def test_nothing_resembling_it_at_all_is_missing(music):
    hold(music, "08A - 124 - Nova Reef - Tide Line")
    found = resolve([one()], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING
    assert found.why is match.Why.NOT_IN_LIBRARY
    assert found.candidates == ()


def test_two_approximate_recordings_with_no_qualifier_stay_two_candidates(music):
    """Two approximate recordings with no qualifier stay two candidates, or accepting one would
    accept the other."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Pathway")
    hold(music, "08A - 124 - Aurora Blooms - Sun Path")
    found = resolve([one(title="Sun Path Way")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert len({c.candidate_id for c in found.candidates}) == len(found.candidates) >= 2


def test_two_files_of_one_version_are_one_candidate_carrying_two_paths(music):
    """A lossless copy and its lossy twin are one answer to one question, or the record would
    return."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    (music / "08A - 124 - Aurora Bloom - Sun Path (Someone Remix).mp3").write_bytes(b"")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert len(found.candidates) == 1
    assert len(found.candidates[0].paths) == 2


def test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording(music, cfg):
    """R21's marker is part of the NAME, never the record. The marker text is config's (S3), so the
    verb hands the engine a template built from it."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    marked = music / f"08A - 124 - {cfg.naming.lossy_marker} Aurora Bloom - Sun Path.mp3"
    marked.write_bytes(b"")

    plain = match.index_library(music)
    assert len(plain.versions(match.recording_token("Aurora Bloom", "Sun Path"))) == 1

    aware = match.index_library(music, template=match_cli.library_template(cfg))
    assert len(aware.versions(match.recording_token("Aurora Bloom", "Sun Path"))) == 2


def test_a_tombstoned_version_is_suppressed_while_another_remix_resolves_normally(music):
    """AE17. R36 in one test: the suppressed one is reported, not counted missing or dropped, and
    another remix of the recording is unaffected, since a tombstone is about one exact version."""
    deleted = match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)")

    def suppresses(kind, identity):
        return kind == match.TOMBSTONE_KIND and dict(identity) == deleted

    result = resolve(
        [one(version="Someone Remix"), one(version="Другой Mix")], index_of(music),
        suppresses=suppresses,
    )
    first, second = result.matches
    assert first.state is match.MatchState.SUPPRESSED
    assert first.why is match.Why.TOMBSTONED
    assert first.suppression_id
    assert second.state is match.MatchState.MISSING


def test_a_suppressed_track_is_in_none_of_the_three_arrays(music):
    """It must not be counted missing, and it must not vanish."""
    result = resolve([one()], index_of(music), suppresses=lambda _k, _i: True)
    payload = result.payload()
    assert [] == payload["matched"] == payload["needs_review"] == payload["missing"]
    assert len(result.suppressed) == 1


def test_a_tombstone_does_not_pre_empt_a_question_about_a_version_the_library_holds(music):
    """R36 governs what acquisition may fetch, not what a person may be asked.

    Consulting the store before the version question left all three arrays empty at exit zero.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    found = resolve(
        [one(version="Extended Mix")], index_of(music), suppresses=lambda _k, _i: True
    ).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.VERSION_DIFFERS
    assert [c.version for c in found.candidates] == [""]


def test_a_tombstone_still_suppresses_when_the_library_can_say_nothing(music):
    """The case R36 is actually about: something is about to be acquired."""
    found = resolve([one()], index_of(music), suppresses=lambda _k, _i: True).matches[0]
    assert found.state is match.MatchState.SUPPRESSED


def test_a_tombstone_over_a_version_the_disk_actually_holds_does_not_beat_the_disk(music):
    """Ownership is on-disk truth, so a tombstone standing over a held file is stale, and
    reporting suppressed would say the library lacks a record it holds."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    found = resolve([one()], index_of(music), suppresses=lambda _k, _i: True).matches[0]
    assert found.state is match.MatchState.MATCHED


def test_the_tombstone_lookup_has_no_default(music):
    """The tombstone lookup has no default: a caller forgetting the store would re-acquire what
    somebody deleted on purpose, so leaving it out is a TypeError."""
    with pytest.raises(TypeError):
        match.resolve_all([one()], index_of(music))  # type: ignore[call-arg]


def test_one_match_identifier_never_appears_in_two_arrays_of_one_payload(music):
    """One match identifier never appears in two arrays of one payload; the identifier excluded the
    key and the STATE includes it."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    payload = resolve([one(), one(key="03B")], index_of(music)).payload()
    rows = [row for state in payload.values() for row in state]
    assert len(rows) == 2
    assert len({row["id"] for row in rows}) == 2
    assert len(payload["matched"]) == len(payload["needs_review"]) == 1


def test_at_most_the_declared_number_of_approximate_candidates_is_offered(music):
    """The constant caps CANDIDATES, not only the scorer's recording limit, which one recording held
    as several versions would exceed."""
        # THREE recordings, each held as three versions at three keys, expand to nine candidates.
    for recording in ("Sun Pathway", "Sun Pathways", "Sun Path Ways"):
        for number, version in enumerate(("Someone Remix", "Extended Mix", "Radio Edit")):
            hold(music, f"0{number + 1}A - 124 - Aurora Bloom - {recording} ({version})")
    found = resolve([one(title="Sun Pathwayss")], index_of(music)).matches[0]
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert len(match._resembling(one(title="Sun Pathwayss"), index_of(music))) > (
        match.APPROXIMATE_LIMIT
    ), "the fixture no longer over-produces, so the cap is not being tested"
    assert 0 < len(found.candidates) <= match.APPROXIMATE_LIMIT


def test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back(
    cfg, music, tmp_path
):
    """The offer limit keeps the best scoring answers and says what it kept back.

    ``_candidates_for`` once re-sorted on folded tokens and the cap kept five wrong answers; a
    silent truncation looks like an offer of everything, so the count kept back is reported.
    """
    for number in range(5):
        hold(music, f"0{number + 1}A - 124 - Aurora Bloom - Sun Path Alt (Mix {number})")
    hold(music, "08A - 124 - Aurora Bloom - Sun Pathx")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "near.txt")
    _code, envelope = drive(["match", "run", path])

    row = envelope["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)
    titles = [candidate["title"] for candidate in row["candidates"]]
    assert "Sun Pathx" in titles, (
        "the best-scoring recording was dropped by an alphabetical truncation"
    )
    assert titles[0] == "Sun Pathx", "the offer is no longer in score order"
    assert len(row["candidates"]) == match.APPROXIMATE_LIMIT
    assert row["candidates_withheld"] == 1
    assert [w["code"] for w in envelope["warnings"]] == [match_cli.CANDIDATES_WITHHELD]


def test_the_withheld_warning_survives_onto_the_run_that_actually_acquires(cfg, music, tmp_path):
    """The withheld warning survives onto the run that actually acquires: it was emitted only for
    NEEDS_REVIEW, so after a rejection run two exited 0 with an option and no warning."""
    for number in range(5):
        hold(music, f"0{number + 1}A - 124 - Aurora Bloom - Sun Path Alt (Mix {number})")
    hold(music, "08A - 124 - Aurora Bloom - Sun Pathx")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "near.txt")

    first_code, first = drive(["match", "run", path])
    assert first_code == int(ExitCode.PENDING_HUMAN)
    drive(["review", "resolve", first["data"]["needs_review"][0]["review_item"],
           "--verdict", "rejected"])

    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    row = envelope["data"]["missing"][0]
    assert row["candidates_withheld"] == 1
    assert row["acquisition"], "this is the run that goes and gets it"
    assert match_cli.CANDIDATES_WITHHELD in {w["code"] for w in envelope["warnings"]}


def test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition(
    cfg, music, tmp_path
):
    """A rejection reaches MISSING by a road resolution never walks, and must still consult the
    store, since a warning is not a declared input to the next verb."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=match.version_identity(
            artist="Aurora Bloom", title="Sun Path (Extended Mix)"
        ),
        actor="test",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    assert first["data"]["needs_review"][0]["why"] == str(match.Why.VERSION_DIFFERS)
    drive(["review", "resolve", first["data"]["needs_review"][0]["review_item"],
           "--verdict", "rejected"])

    code, second = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert second["data"]["missing"] == [], (
        "a tombstoned version was handed to acquisition by a rejection"
    )
    assert second["data"]["matched"] == second["data"]["needs_review"] == []
    warnings = [w for w in second["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert len(warnings) == 1 and warnings[0]["suppression"]


def test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source(music, tmp_path):
    """Artist and title fall back AS A PAIR, or the identity is assembled from two sources and
    matches neither the tags nor the name."""
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"title": "Sun Path"})
    target = music / "08A - 124 - Aurora Bloom - Wrong Title.flac"
    shutil.copy2(probe, target)

    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Wrong Title"))
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path")) == ()


def test_a_present_artist_tag_is_never_thrown_away_by_the_pair_fallback(music, tmp_path):
    """A present artist tag is never thrown away by the pair fallback when the name has no
    separator."""
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"artist": "Aurora Bloom"})
    shutil.copy2(probe, music / "SunPath.flac")

    held = index_of(music).versions(match.recording_token("Aurora Bloom", "SunPath"))
    assert [row.artist for row in held] == ["Aurora Bloom"]


def test_the_payload_carries_exactly_the_fields_the_declared_surface_requires():
    """Derived from the schema, so the two cannot drift apart."""
    declared = set(output.schema_document("match")["required"])
    assert set(match.MatchResult(()).payload()) == declared
    assert {str(state) for state in match.PAYLOAD_STATES} == declared
    assert str(match.MatchState.SUPPRESSED) not in declared


@pytest.mark.parametrize("source", [*MATCH_SOURCES, MATCH_CLI_SOURCE], ids=lambda p: p.name)
def test_no_set_or_mapping_literal_in_this_unit_has_a_duplicate_element(source):
    """The shape a green suite cannot see, hunted by parsing: a duplicate collapsed at parse time is
    already gone from the RUNTIME object. The walk reaches a frozenset inside the call."""
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.Set, ast.Dict)):
            keys = node.elts if isinstance(node, ast.Set) else node.keys
            constants = [k.value for k in keys if isinstance(k, ast.Constant)]
            duplicates = sorted({k for k in constants if constants.count(k) > 1})
            assert not duplicates, f"line {node.lineno}: duplicate elements {duplicates}"


def test_the_duplicate_literal_hunt_can_actually_see_one():
    """A guard nobody proved bites is a comment (P7, other direction): both literal shapes,
    including the frozenset call the real module uses."""
    for shape in ('X = {"a", "b", "a"}', 'X = frozenset({"a", "a"})', 'X = {"a": 1, "a": 2}'):
        node = next(n for n in ast.walk(ast.parse(shape)) if isinstance(n, (ast.Set, ast.Dict)))
        keys = node.elts if isinstance(node, ast.Set) else node.keys
        values = [k.value for k in keys if isinstance(k, ast.Constant)]
        assert len(values) != len(set(values))


# ── Part 4: one internal shape, three sources (R13) ───────────────────────

#: One playlist expressed three ways: the provider carries the version in its own field,
#: the public playlist API and pasted text carry it inside the title, and text has no id.
TIDAL_ROWS = [
    {"id": "1001", "title": "Sun Path", "version": "Someone Remix",
     "artist": {"name": "Aurora Bloom"}},
    {"id": "1002", "title": "Tide Line", "version": "", "artist": {"name": "Nova Reef"}},
]
SPOTIFY_ROWS = [
    {"track": {"id": "sp1", "name": "Sun Path (Someone Remix)",
               "artists": [{"name": "Aurora Bloom"}]}},
    {"track": {"id": "sp2", "name": "Tide Line", "artists": [{"name": "Nova Reef"}]}},
]
#: The spelling the public playlist API actually uses: ``name`` carries the version after a
#: dash, the one shape the readers did NOT agree on.
SPOTIFY_DASH_ROWS = [
    {"track": {"id": "sp1", "name": "Sun Path - Someone Remix",
               "artists": [{"name": "Aurora Bloom"}]}},
    {"track": {"id": "sp2", "name": "Tide Line", "artists": [{"name": "Nova Reef"}]}},
]
TEXT_LINES = "1. Aurora Bloom - Sun Path (Someone Remix)\n\n# a comment\nNova Reef - Tide Line\n"


@pytest.mark.parametrize("spotify", [SPOTIFY_ROWS, SPOTIFY_DASH_ROWS], ids=["bracketed", "dashed"])
def test_the_three_readers_produce_one_shape(spotify):
    """Both spellings of the public playlist API, not only the easy one.

    ``Sun Path - Someone Remix`` is what that API ships and only bracketed groups were read, so the
    row resolved missing while the provider row matched.
    """
    from_tidal = match.read_tidal_tracks(TIDAL_ROWS)
    from_spotify = match.read_spotify_items(spotify)
    from_text = match.read_text_lines(TEXT_LINES)
    for read in (from_tidal, from_spotify, from_text):
        assert [(w.artist, w.title, w.version_key) for w in read] == [
            ("Aurora Bloom", "Sun Path", match.version_token("Someone Remix")),
            ("Nova Reef", "Tide Line", ""),
        ]
        # The match converges and the address deliberately does not: a listing is addressed by the
        # title it spelled, and the consult covers both spellings.
    composed = {w.identity["title"] for w in from_tidal}
    for wanted in from_spotify:
        assert composed & {
            spelling["title"] for spelling in wanted.suppression_spellings
        }, "a version this list can name is addressed by nothing the other side writes"


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Sun Path - Nightwave Remix", ("Sun Path", "Nightwave Remix")),
        ("Sun Path - Radio Edit", ("Sun Path", "Radio Edit")),
        ("Sun Path - Extended Mix", ("Sun Path", "Extended Mix")),
                # A head word carries a one word tail, as the public playlist API ships these three,
                # and a year is not a vocabulary word.
        ("Sun Path - Remastered 2011", ("Sun Path", "Remastered 2011")),
        ("Sun Path - Remastered", ("Sun Path", "Remastered")),
        ("Sun Path - Nightwave Remix (Radio Edit)", ("Sun Path", "Nightwave Remix Radio Edit")),
                # Not a version: splitting on any trailing dash would invent an unreleased record.
        ("Sun - Rise", ("Sun - Rise", "")),
        ("Tide Line - Reprise Of Nothing", ("Tide Line - Reprise Of Nothing", "")),
        ("- Remix", ("- Remix", "")),
    ],
)
def test_a_dash_qualifier_is_read_only_when_it_names_a_version(name, expected):
    assert match.split_title(name) == expected
        # The bracket only splitter is unchanged, so its hazard stays written down.
    assert match.split_version("Sun - Rise") == ("Sun - Rise", "")


@pytest.mark.parametrize(
    "name",
    [
                # The reprise class, the sharpest: an album reprise is a separate composition, and
                # accepting a split would report ownership of a track the library does not hold.
        "Sgt. Pepper's Lonely Hearts Club Band - Reprise",
        "Ziggy Stardust - Reprise",
        "Hurt - Reprise",
                # Every other one word vocabulary tail that is really the end of a title.
        "Long - Live",
        "Studio 54 - Live",
        "Pump Up The Volume - Extended",
        "Nice Up - Dub",
        "Beat It - Demo",
        "Sunset - Acoustic",
                # Folding inflated the word count: the inner hyphen became a space. Counted raw now.
        "Sun - Re-Mix",
        "曲 - Live",
    ],
)
def test_a_legitimate_title_ending_in_a_vocabulary_word_is_not_split(name):
    """A legitimate title ending in a vocabulary word is not split.

    A bare one word qualifier is ambiguous, so the string reader leaves it alone and the LIBRARY
    settles it: see ``test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it``.
    """
    assert match.split_title(name) == (name, "")


#: The one word tails the public playlist API really ships, each a whole class.
ONE_WORD_TAILS = ("Live", "Instrumental", "Acoustic", "Dub", "Demo", "Extended", "Remix")


@pytest.mark.parametrize("tail", ONE_WORD_TAILS)
def test_a_bare_one_word_tail_offers_the_reading_the_string_rule_declined(tail):
    """Both readings exist, and neither is picked by the string: ``split_title`` keeps the
    conservative one, and the other must not be thrown away."""
    assert match.split_title(f"Sun Path - {tail}") == (f"Sun Path - {tail}", "")
    assert match.split_ambiguous(f"Sun Path - {tail}") == ("Sun Path", tail)


@pytest.mark.parametrize(
    "name",
    [
        "Sun - Rise", "Tide Line - Reprise Of Nothing", "Sun Path (Nightwave Remix)",
        "Sun Path - Nightwave Remix", "Sun Path - Remastered", "- Remix",
    ],
)
def test_a_title_with_only_one_reading_offers_no_second_one(name):
    """The ambiguity is narrow on purpose: a tail outside the vocabulary, one ``split_title``
    already reads, or an empty head must not license re-splitting any title."""
    assert match.split_ambiguous(name) is None


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Sun - Rise", ("Sun - Rise", "")), ("Sing - Sing - Sing", ("Sing - Sing - Sing", "")),
        ("The Man - Machine", ("The Man - Machine", "")), ("Come - Alive", ("Come - Alive", "")),
        ("Sun - Rise!", ("Sun - Rise!", "")),
    ],
)
def test_the_titles_that_were_already_safe_stay_safe(name, expected):
    assert match.split_title(name) == expected


def test_a_bare_track_record_is_read_as_readily_as_a_playlist_item():
    """The playlist endpoint wraps its track and the tracks endpoint does not."""
    wrapped = match.read_spotify_items(SPOTIFY_ROWS)
    bare = match.read_spotify_items([row["track"] for row in SPOTIFY_ROWS])
    assert wrapped == bare


def test_a_pasted_line_with_no_separator_is_refused_rather_than_read_as_a_title():
    """Reading it as an anonymous title puts a track in the queue nothing can match."""
    with pytest.raises(match.UnreadableList) as excinfo:
        match.read_text_lines("Aurora Bloom - Sun Path\njust some words\n")
    assert excinfo.value.line == 2


def test_the_same_list_from_three_sources_produces_identical_rows(music):
    """Everything except provenance is derived from the recording: the rows agree once ``source`` is
    dropped, AND ``source`` is the only key that differs."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    index = index_of(music)
    payloads = [
        resolve(read, index).payload()
        for read in (
            match.read_tidal_tracks(TIDAL_ROWS), match.read_spotify_items(SPOTIFY_ROWS),
            match.read_text_lines(TEXT_LINES),
        )
    ]

    def without_source(payload):
        return {
            state: [{k: v for k, v in row.items() if k != "source"} for row in rows]
            for state, rows in payload.items()
        }

    assert without_source(payloads[0]) == without_source(payloads[1]) == without_source(payloads[2])
    origins = {
        row["source"]["origin"] for payload in payloads for rows in payload.values() for row in rows
    }
    assert origins == {match.TIDAL, match.SPOTIFY, match.TEXT}


def test_the_provider_reference_never_reaches_the_identity():
    """Two services holding one record must be one question, not two."""
    tidal = match.read_tidal_tracks(TIDAL_ROWS)[0]
    spotify = match.read_spotify_items(SPOTIFY_ROWS)[0]
    assert tidal.ref != spotify.ref
    assert tidal.identity == spotify.identity


@pytest.mark.parametrize(
    "row",
    [
        {"artist": ["Two Names"], "title": "Listy"}, {"artists": ["Two Names"], "title": "Listy"},
        {"artist": [{"name": "Two Names"}], "title": "Listy"},
        {"artists": "Two Names", "title": "Listy"},
    ],
    ids=[
        "list-under-artist", "list-under-artists", "objects-under-artist", "string-under-artists",
    ],
)
def test_every_shape_a_row_spells_its_artists_in_reads_the_same(row):
    """Every shape a row spells its artists in reads the same: a list under ``artist`` read as NO
    ARTIST, and a bare string under ``artists`` is the same defect one shape out."""
    assert match.read_tidal_tracks([row])[0].artist == "Two Names"


def test_a_row_that_names_neither_an_artist_nor_a_title_is_refused(music):
    """Positive recognition: a row naming neither an artist nor a title is refused, or identifier
    only rows fold to one match identifier and an anonymous row matches junk files."""
    with pytest.raises(match.UnreadableList) as excinfo:
        match.read_tidal_tracks([{"id": "a"}, {"id": "b"}])
    assert excinfo.value.line == 1


@pytest.mark.parametrize(
    "row",
    [
        {"id": "sp1", "name": "Sun Path"}, {"id": "sp1", "name": "Sun Path", "artists": []},
        {"id": "sp1", "artists": [{"name": "Aurora Bloom"}]},
    ],
    ids=["no-artist-key", "empty-artists", "no-title"],
)
def test_a_row_naming_only_one_half_of_a_record_is_refused_too(row):
    """A row naming only one half of a record is refused too, a rule as strong as
    ``read_text_lines``."""
    with pytest.raises(match.UnreadableList) as excinfo:
        match.read_spotify_items([row])
    assert excinfo.value.line == 1


def test_two_rows_sharing_a_title_and_naming_two_artists_are_two_records(cfg, music, tmp_path):
    """Two rows sharing a title and naming two artists are two records.

    Bare string artists once read as no artist, hashed to one identity and matched one unrelated
    file, so one row vanished from any payload keyed by id.
    """
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"title": "Sun Path"})
    shutil.copy2(probe, music / "SunPath.flac")
    rows = [
        {"id": "sp1", "name": "Sun Path", "artists": "Aurora Bloom"},
        {"id": "sp2", "name": "Sun Path", "artists": "Nova Reef"},
    ]
    read = match.read_spotify_items(rows)
    assert [wanted.artist for wanted in read] == ["Aurora Bloom", "Nova Reef"]
    resolved = resolve(read, index_of(music))
    assert len({found.match_id for found in resolved.matches}) == 2
    assert resolved.of(match.MatchState.MATCHED) == ()


def test_two_anonymous_rows_can_no_longer_collapse_onto_one_row(cfg, music, tmp_path):
    """Driven through the verb, where the collapse was invisible, with a junk file present."""
    (music / "-.flac").write_bytes(b"")
    path = write_list(
        tmp_path,
        json.dumps({"list": 1, "origin": match.TIDAL, "tracks": [{"id": "a"}, {"id": "b"}]}),
        "anon.json",
    )
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["detail"]["position"] == 1


# ── Part 5: the verb, and the split U11 settled ──────────────────────────────


def queue_items(cfg) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(review.list_items(store, include_resolved=True, limit=None).items)


def test_the_verb_emits_one_match_envelope_with_the_status_agreeing(cfg, music, tmp_path):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert output.envelope_problems(envelope) == []
    assert envelope["schema"] == output.current_schema("match")
    assert envelope["exit_code"] == code
    assert [row["title"] for row in envelope["data"]["matched"]] == ["Sun Path"]


def test_only_the_needs_review_state_reaches_the_queue(cfg, music, tmp_path):
    """U11's split, driven rather than read: matched and missing tracks leave the queue empty. The
    static half lives in tests/test_review_queue.py."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\nNova Reef - Tide Line\n")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert len(envelope["data"]["matched"]) == 1
    assert len(envelope["data"]["missing"]) == 1
    assert queue_items(cfg) == []


def test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question(
    cfg, music, tmp_path
):
    """The name quantifies over the options, so the options are what it asserts. Whether a missing
    row belongs in the queue is the residual titled "Two briefs disagree about whether a missing
    track
    is a review item", a decision reserved for a person."""
    path = write_list(tmp_path, "Nova Reef - Tide Line\n")
    _code, envelope = drive(["match", "run", path])
    row = envelope["data"]["missing"][0]
    assert row["why"] == str(match.Why.NOT_IN_LIBRARY)
    assert row["review_item"] is None
    assert queue_items(cfg) == []

    options = row["acquisition"]
    assert options, "a missing row carries no acquisition options at all"
    assert [option["how"] for option in options] == [match.BY_SEARCH]
    assert options[0]["query"] == "Nova Reef Tide Line"
    assert options[0]["artist"] == "Nova Reef"
    assert len({option["id"] for option in options}) == len(options)
        # Every other row's options are its own, so one row's option id cannot acquire another's.
    assert options[0]["id"] != match.acquisition_options(one())[0].option_id


def test_an_acquisition_option_names_the_exact_version_and_never_a_looser_one():
    """An option meaning "some other cut will do" is the silent substitution: the version travels in
    the query and its own field, and a code, when the list carried one, comes first."""
    wanted = match.Wanted(
        artist="Aurora Bloom", title="Sun Path", version="Someone Remix", isrc="GBAAA0000001"
    )
    options = match.acquisition_options(wanted)
    assert [option.how for option in options] == [match.BY_ISRC, match.BY_SEARCH]
    assert options[0].query == "GBAAA0000001"
    assert options[1].query == "Aurora Bloom Sun Path (Someone Remix)"
    assert all(option.version == "Someone Remix" for option in options)


def test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get(cfg, music, tmp_path):
    """"None of these is the record" is the sentence that hands it to acquisition."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    drive(["review", "resolve", first["data"]["needs_review"][0]["review_item"],
           "--verdict", "rejected"])
    _code, second = drive(["match", "run", path])
    row = second["data"]["missing"][0]
    assert row["why"] == str(match.Why.VERDICT_REJECTED)
    assert [option["how"] for option in row["acquisition"]] == [match.BY_SEARCH]
    assert row["acquisition"][0]["version"] == "Extended Mix"


def test_the_dash_spelling_of_a_public_playlist_resolves_the_same_as_the_provider(
    cfg, music, tmp_path
):
    """The dash spelling of a public playlist resolves the same as the provider, through the verb;
    the approximate pass did not rescue it (72.4 against a floor of 82)."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    dashed = write_list(
        tmp_path,
        json.dumps(
            {"list": 1, "origin": match.SPOTIFY,
             "tracks": [{"id": "sp1", "name": "Sun Path - Nightwave Remix",
                         "artists": [{"name": "Aurora Bloom"}]}]}
        ),
        "dashed.json",
    )
    provider = write_list(
        tmp_path,
        json.dumps(
            {"list": 1, "origin": match.TIDAL,
             "tracks": [{"id": "1", "title": "Sun Path", "version": "Nightwave Remix",
                         "artist": {"name": "Aurora Bloom"}}]}
        ),
        "provider.json",
    )
    code, envelope = drive(["match", "run", dashed])
    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    assert envelope["data"]["matched"][0]["why"] == str(match.Why.EXACT)
    _code, through_provider = drive(["match", "run", provider])
    assert (envelope["data"]["matched"][0]["id"] == through_provider["data"]["matched"][0]["id"])


@pytest.mark.parametrize("tail", ONE_WORD_TAILS)
def test_a_one_word_version_tail_is_asked_about_and_never_re_acquired(cfg, music, tail):
    """The whole one word class is asked about and never re-acquired.

    The dash row resolved MISSING with an option for a held track at exit zero. The STATE no longer
    converges, since letting the library decide a parse made "Long - Live" claim "Long (Live)": a
    provider row matches and the dash rows ask once.
    """
    hold(music, f"08A - 124 - Aurora Bloom - Sun Path ({tail})")
    index = index_of(music)
    provider, spotify, text = (
        resolve(read, index).matches[0]
        for read in (
            match.read_tidal_tracks(
                [{"title": "Sun Path", "version": tail, "artist": {"name": "Aurora Bloom"}}]
            ),
            match.read_spotify_items(
                [{"name": f"Sun Path - {tail}", "artists": [{"name": "Aurora Bloom"}]}]
            ),
            match.read_text_lines(f"Aurora Bloom - Sun Path - {tail}\n"),
        )
    )
        # Not acquired, for any of the three, which is the point of the class.
    for found in (provider, spotify, text):
        assert found.state is not match.MatchState.MISSING
        assert found.acquisitions == ()
    assert (provider.state, provider.why) == (match.MatchState.MATCHED, match.Why.EXACT)
    for found in (spotify, text):
        assert (found.state, found.why) == (
            match.MatchState.NEEDS_REVIEW, match.Why.READING_AMBIGUOUS,
        )
        assert [candidate.version for candidate in found.candidates] == [tail]
    assert spotify.match_id == text.match_id
    assert spotify.question_identity == text.question_identity


@pytest.mark.parametrize(
    "held",
    [
                # The library holds the other reading, so there is something to ask about.
        "08A - 124 - Aurora Bloom - Sun Path (Live)",
                # And at a different key, so the CANDIDATE changes while the question does not.
        "03A - 124 - Aurora Bloom - Sun Path (Live)",
    ],
    ids=["held", "held-at-another-key"],
)
def test_the_identifier_of_an_ambiguous_row_never_moves_with_the_library(
    cfg, music, tmp_path, held
):
    """A match identifier is a function of the list, not the disk.

    ``_reading_the_library_confirms`` rewrote the wanted track, so one line gave two identifiers on
    two machines and an answered item was looked up under an identity nobody was asked.
    """
    empty = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]
    hold(music, held)
    confirmed = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]

    assert empty.state is match.MatchState.MISSING
    assert confirmed.state is match.MatchState.NEEDS_REVIEW
    assert empty.match_id == confirmed.match_id
        # The item identity is asserted across the two libraries that ask the same question, held
        # at 08A and at 03A, rather than across one that asks nothing (a MISSING row has no item:
        # see ``test_a_row_that_is_not_a_question_has_no_review_item_identity``).
    assert confirmed.question_identity == match.question_identity(
        "Aurora Bloom", "Sun Path - Live", "", None, match.Why.READING_AMBIGUOUS
    )
        # The title is the one the LIST spelled, so the identifier and payload agree.
    assert (confirmed.wanted.title, confirmed.wanted.version) == ("Sun Path - Live", "")


def test_a_verdict_survives_the_rename_that_flips_the_reading(cfg, music, tmp_path):
    """The stranding, driven: after the confirming file is renamed, the item is found by its list
    derived identity and the run says CANDIDATE_GONE, a row a person can act on."""
    first = hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path - Live\n", "flip.txt")
    _code, asked = drive(["match", "run", path])
    row = asked["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.READING_AMBIGUOUS)
    item_id = row["review_item"]
    drive(
        ["review", "resolve", item_id, "--verdict", "accepted",
         "--option", row["candidates"][0]["id"]]
    )
    _code, settled = drive(["match", "run", path])
    assert settled["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)

    first.rename(music / "11B - 124 - Aurora Bloom - Sun Path (Live).flac")
    code, after = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    stalled = after["data"]["needs_review"][0]
    assert stalled["why"] == str(match.Why.CANDIDATE_GONE)
    assert stalled["review_item"] == item_id


def test_the_dashed_one_word_spelling_is_asked_about_rather_than_acquired(cfg, music, tmp_path):
    """Driven through the verb: "Instrumental" scores below the approximate floor, so the run once
    reported it missing at exit zero.

    The row is a QUESTION now, exiting zero because gating would exit 12 on almost every real run.
    What R11 forbids is a question nobody is TOLD about, so it is named on the warning channel.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Instrumental)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path - Instrumental\n", "oneword.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["pending_human_action"] is None
    assert envelope["data"]["missing"] == []
    assert envelope["data"]["matched"] == []
    row = envelope["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.READING_AMBIGUOUS)
    assert row["acquisition"] == []
    assert [candidate["version"] for candidate in row["candidates"]] == ["Instrumental"]
        # Not silent: the question is named on the warning channel, carries the item a person
        # answers it under, and names the verb that shows it.
    warned = [w for w in envelope["warnings"] if w["code"] == match_cli.READING_UNSETTLED]
    assert [(w["item"], w["remedy"]) for w in warned] == [
        (row["review_item"], match_cli.REVIEW_VERB)
    ]
    assert queue_items(cfg)[0].item_id == row["review_item"]


def test_an_ungated_question_still_gates_once_its_verdict_cannot_be_applied(cfg, music, tmp_path):
    """The escape from the ungated class: an ANSWERED reading question whose candidate went is
    RESOLVED and hidden from ``review list``, so ``apply_verdict`` rewrites it into ``STALLED``,
    which is not in ``UNGATED``, and the run blocks and names the verb that can act."""
    held = hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path - Live\n", "oneword.txt")
    code, asked = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    row = asked["data"]["needs_review"][0]
    drive(
        ["review", "resolve", row["review_item"], "--verdict", "accepted",
         "--option", row["candidates"][0]["id"]]
    )
    held.rename(music / "11B - 124 - Aurora Bloom - Sun Path (Live).flac")

    code, after = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert after["data"]["needs_review"][0]["why"] == str(match.Why.CANDIDATE_GONE)
    assert after["pending_human_action"]["verify_verb"] == match_cli.CLEAR_VERB


def test_an_undecidable_parse_is_never_promoted_to_a_match(cfg, music):
    """Property 2 applied to the parse: an undecidable parse is never promoted to a match.

    "Long - Live" against a held "Long (Live)" resolved MATCHED, reporting ownership of a track the
    library does not hold. A generous read costs one question, never one wrong join.
    """
    hold(music, "08A - 124 - Long Player - Long (Live)")
    found = resolve(
        match.read_text_lines("Long Player - Long - Live\n"), index_of(music)
    ).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.READING_AMBIGUOUS
    assert found.paths == ()
    assert found.wanted.title == "Long - Live"


@pytest.mark.parametrize(
    "line,held,expected_title",
    [
                # The reprise class, which is what refusing the split defends: an album reprise is a
                # separate composition, so holding the record it reprises is not evidence of a
                # version.
        ("David Bowie - Ziggy Stardust - Reprise", "David Bowie - Ziggy Stardust",
         "Ziggy Stardust - Reprise"),
        ("The Beatles - Sgt Peppers - Reprise", "The Beatles - Sgt Peppers",
         "Sgt Peppers - Reprise"),
        ("Nova Reef - Sunset - Acoustic", "Nova Reef - Sunset", "Sunset - Acoustic"),
        ("Nova Reef - Nice Up - Dub", "Nova Reef - Nice Up", "Nice Up - Dub"),
    ],
)
def test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it(
    cfg, music, line, held, expected_title
):
    """An ambiguous reading is taken only when the library holds the head AT THAT VERSION.

    Holding the head at another version is no evidence, so it must not reframe "nothing like this"
    into "this record as a different version", nor become a question with an empty offer.
    """
    hold(music, f"08A - 124 - {held}")
    found = resolve(match.read_text_lines(f"{line}\n"), index_of(music)).matches[0]
    assert found.wanted.title == expected_title
    assert found.wanted.version == ""
    assert found.why is not match.Why.VERSION_DIFFERS
    assert found.why is not match.Why.READING_AMBIGUOUS
    assert found.state is not match.MatchState.MATCHED


def test_the_ambiguity_offer_names_the_version_the_other_reading_means(cfg, music):
    """The offer is as narrow as the evidence: the head's other versions would ask a person to
    accept a cut the list never mentioned."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]
    assert found.why is match.Why.READING_AMBIGUOUS
    assert [candidate.version for candidate in found.candidates] == ["Live"]


def test_the_reading_the_list_actually_spelled_wins_when_the_library_holds_both(cfg, music):
    """A tie goes to what the list said: when the library holds both readings, the conservative one,
    the string the list spelled, must win over this module's guess."""
    whole = hold(music, "08A - 124 - Aurora Bloom - Sun Path - Live")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    found = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.wanted.title == "Sun Path - Live"
    assert found.paths == (str(whole),)


def test_a_version_question_becomes_an_addressable_item_with_its_candidates(cfg, music, tmp_path):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.PENDING_HUMAN)
    assert envelope["outcome"] == "pending"
    assert envelope["pending_human_action"]["verify_verb"] == match_cli.REVIEW_VERB
    row = envelope["data"]["needs_review"][0]
    items = queue_items(cfg)
    assert [item.item_id for item in items] == [row["review_item"]]
    assert items[0].queue == review.Queue.VERSION_MATCH
    assert [option.option_id for option in items[0].options] == [
        candidate["id"] for candidate in row["candidates"]
    ]


def test_no_file_is_written_for_a_person_to_edit(cfg, music, tmp_path):
    """R12's negative half, asserted against the FILESYSTEM by walking the library root, so a
    spreadsheet added later is covered the day it appears."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\nNova Reef - Tide\n")
    drive(["match", "run", path])
    written = [p for p in cfg.library.root.rglob("*") if p.is_file()]
    assert not [p for p in written if p.suffix.lower() in {".csv", ".tsv"}]


def test_a_run_over_an_answered_question_reports_matched_and_writes_nothing(cfg, music, tmp_path):
    """The property the source system cannot have: the decision outlives the run."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]
    option = first["data"]["needs_review"][0]["candidates"][0]["id"]

    code, _ = drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])
    assert code == int(ExitCode.OK)
    before = queue_items(cfg)[0].updated

    code, second = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    row = second["data"]["matched"][0]
    assert row["why"] == str(match.Why.VERDICT_ACCEPTED)
    assert row["paths"]
    assert queue_items(cfg)[0].updated == before, (
        "an answered question was written to again, so 'a decision is never "
        "re-asked' is true only until somebody looks at the timestamps"
    )


def test_a_rejected_question_makes_the_track_missing_rather_than_matched(cfg, music, tmp_path):
    """Rejected means none of the owned versions is this record."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]

    drive(["review", "resolve", item_id, "--verdict", "rejected"])
    code, second = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert second["data"]["needs_review"] == []
    assert second["data"]["missing"][0]["why"] == str(match.Why.VERDICT_REJECTED)


def test_an_accepted_candidate_that_has_since_gone_is_not_reported_matched(cfg, music, tmp_path):
    """Ownership is on-disk truth, and a verdict does not put a file back: the track returns as a
    question naming the item, never a matched row pointing at a missing file."""
    remix = hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]
    option = first["data"]["needs_review"][0]["candidates"][0]["id"]
    drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])

    remix.unlink()
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Another Remix)")
    _code, second = drive(["match", "run", path])
    assert second["data"]["matched"] == []
    row = second["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.CANDIDATE_GONE)
    assert row["review_item"] == item_id


def test_an_acceptance_naming_no_candidate_is_applied_only_when_there_is_one(cfg, music, tmp_path):
    """An acceptance naming no candidate is applied only when there is exactly one; with several it
    does not say which version."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    single = first["data"]["needs_review"][0]["review_item"]
    drive(["review", "resolve", single, "--verdict", "accepted"])
    _code, settled = drive(["match", "run", path])
    assert settled["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)

    hold(music, "08A - 124 - Nova Reef - Tide Line (Someone Remix)")
    hold(music, "08A - 124 - Nova Reef - Tide Line (Another Remix)")
    many = write_list(tmp_path, "Nova Reef - Tide Line (Extended Mix)\n", "many.txt")
    _code, offered = drive(["match", "run", many])
    item_id = offered["data"]["needs_review"][0]["review_item"]
    assert len(offered["data"]["needs_review"][0]["candidates"]) == 2

    drive(["review", "resolve", item_id, "--verdict", "accepted"])
    _code, after = drive(["match", "run", many])
    row = next(r for r in after["data"]["needs_review"] if r["review_item"] == item_id)
    assert row["why"] == str(match.Why.VERDICT_UNSPECIFIC)
    assert not [r for r in after["data"]["matched"] if r["title"] == "Tide Line"]


def test_one_answered_key_question_never_settles_another_one(cfg, music, tmp_path):
    """One answered key question never settles another: the key decides the state but was not in the
    identity, so accepting 08A let a later 03B come back matched."""
    hold(music, "03A - 124 - Aurora Bloom - Sun Path")
    asked = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "plain.txt")

    def with_key(code: str, name: str) -> str:
        return write_list(
            tmp_path,
            json.dumps(
                {"list": 1, "origin": match.TIDAL,
                 "tracks": [{"id": "1", "title": "Sun Path", "key": code,
                             "artist": {"name": "Aurora Bloom"}}]}
            ),
            name,
        )

    _code, first = drive(["match", "run", with_key("08A", "k08a.json")])
    item_id = first["data"]["needs_review"][0]["review_item"]
    option = first["data"]["needs_review"][0]["candidates"][0]["id"]
    drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])

    _code, settled = drive(["match", "run", with_key("08A", "k08a.json")])
    assert settled["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)

    for code, name, expected in (
        ("03B", "k03b.json", match.Why.KEY_RELATIVE), ("11B", "k11b.json", match.Why.KEY_DIFFERS),
    ):
        _code, other = drive(["match", "run", with_key(code, name)])
        assert other["data"]["matched"] == [], f"{code} was decided by the answer to 08A"
        assert other["data"]["needs_review"][0]["why"] == str(expected)
        assert other["data"]["needs_review"][0]["review_item"] != item_id

        # A REJECTION propagates identically, so it is asserted from the same fixture.
    _code, plain = drive(["match", "run", asked])
    assert plain["data"]["matched"][0]["why"] == str(match.Why.EXACT)


def test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not(
    cfg, music, tmp_path
):
    """A list line that names a key is a different question from one that does not.

    The cost of the rule, recorded: the identity is a function of the LIST LINE and includes the
    key. It was bought with something worse, the library deciding the identity so an exported
    answer could not be found. R13 promises one line through three readers is one question.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    plain = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n", "plain.txt")

    def keyed(code: str | None, name: str) -> str:
        row = {"id": "1", "title": "Sun Path", "version": "Extended Mix",
               "artist": {"name": "Aurora Bloom"}}
        if code is not None:
            row["key"] = code
        return write_list(
            tmp_path, json.dumps({"list": 1, "origin": match.TIDAL, "tracks": [row]}), name,
        )

    _code, first = drive(["match", "run", plain])
    item_id = first["data"]["needs_review"][0]["review_item"]
    _code, with_key = drive(["match", "run", keyed("08A", "keyed.json")])
    assert with_key["data"]["needs_review"][0]["review_item"] != item_id
    assert len(queue_items(cfg)) == 2

        # The promise that survives: the same line through a different reader is the same question.
    _code, unkeyed = drive(["match", "run", keyed(None, "unkeyed.json")])
    assert unkeyed["data"]["needs_review"][0]["review_item"] == item_id
    assert len(queue_items(cfg)) == 2


def test_a_verdict_travels_between_two_machines_that_hold_different_versions(cfg, music, tmp_path):
    """A verdict travels between two machines that hold different versions.

    ``review export`` and ``import`` need ONE QUESTION about one list line to have one identity
    wherever it is asked; it once depended on library values, so the import applied to nothing.
    """
    line = match.read_tidal_tracks(
        [{"id": "1", "title": "Sun Path", "version": "Nightwave Remix",
          "key": "08A", "artist": {"name": "Aurora Bloom"}}]
    )

    def library(name: str, room_id: str) -> match.LibraryIndex:
        room = tmp_path / f"lib{room_id}"
        room.mkdir(parents=True, exist_ok=True)
        hold(room, name)
        return index_of(room)

    def settled(index, store) -> match.TrackMatch:
        return match_cli.adjudicate(
            store, resolve(line, index), handler_key="acquire.match.run",
            suppresses=nothing_suppressed, suppression_id=no_identifier,
        ).matches[0]

        # MACHINE A holds the extended cut, at 03A.
    machine_a = library("03A - 124 - Aurora Bloom - Sun Path (Extended)", "a")
        # MACHINE B holds the instrumental, at 08A: another file, version and key, same question.
    machine_b = library("08A - 124 - Aurora Bloom - Sun Path (Instrumental)", "b")

    with review.open_store(cfg, path=tmp_path / "a.sqlite3") as store_a:
        asked = settled(machine_a, store_a)
        assert asked.why is match.Why.VERSION_DIFFERS
        review.resolve(store_a, asked.item_id, review.Verdict.REJECTED, actor="phillip")
        document = review.export_document(store_a)

    with review.open_store(cfg, path=tmp_path / "b.sqlite3") as store_b:
        fresh = settled(machine_b, store_b)
        assert fresh.why is match.Why.VERSION_DIFFERS
        assert fresh.item_id == asked.item_id, (
            "the two machines opened two items for one list line, so the export "
            "lands under an identifier this one never looks up"
        )
        taken = review.import_document(store_b, document, actor="importer")
        assert taken.conflicts == ()
        answered = settled(machine_b, store_b)

    assert (answered.state, answered.why) == (match.MatchState.MISSING, match.Why.VERDICT_REJECTED)
    assert answered.item_id == asked.item_id
    assert asked.match_id == answered.match_id


def test_a_key_question_answered_elsewhere_does_not_settle_a_version_question(cfg, music, tmp_path):
    """A key question answered elsewhere does not settle a version question.

    They are two items, since the answers are not interchangeable. The residual titled "A question
    answered
    on one machine does not settle a different question about the same line" records what is given
    up.
    """
    line = match.read_tidal_tracks(
        [{"id": "1", "title": "Sun Path", "version": "Nightwave Remix",
          "key": "08A", "artist": {"name": "Aurora Bloom"}}]
    )

    def library(name: str, room_id: str) -> match.LibraryIndex:
        room = tmp_path / f"cost{room_id}"
        room.mkdir(parents=True, exist_ok=True)
        hold(room, name)
        return index_of(room)

    def settled(index, store) -> match.TrackMatch:
        return match_cli.adjudicate(
            store, resolve(line, index), handler_key="acquire.match.run",
            suppresses=nothing_suppressed, suppression_id=no_identifier,
        ).matches[0]

    keyed = library("03A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)", "k")
    versioned = library("08A - 124 - Aurora Bloom - Sun Path (Extended)", "v")

    with review.open_store(cfg, path=tmp_path / "k.sqlite3") as store_k:
        asked = settled(keyed, store_k)
        assert asked.why is match.Why.KEY_DIFFERS
        review.resolve(store_k, asked.item_id, review.Verdict.REJECTED, actor="phillip")
        document = review.export_document(store_k)

    with review.open_store(cfg, path=tmp_path / "v.sqlite3") as store_v:
        fresh = settled(versioned, store_v)
        assert fresh.why is match.Why.VERSION_DIFFERS
        assert fresh.item_id != asked.item_id
        review.import_document(store_v, document, actor="importer")
        after = settled(versioned, store_v)

        # The imported answer is not applied, and the row stays a question.
    assert (after.state, after.why) == (match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)
    assert after.item_id == fresh.item_id
        # One ``match_id`` across both: the machines agree about the RECORD, not the question.
    assert asked.match_id == after.match_id


def test_a_run_blocked_by_an_unapplicable_verdict_names_the_verb_that_can_act(cfg, music, tmp_path):
    """A run blocked by an unapplicable verdict names the verb that can act: the item stays RESOLVED
    so ``review resolve`` refuses, and the only escape, ``review clear``, was never named."""
    remix = hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]
    option = first["data"]["needs_review"][0]["candidates"][0]["id"]
    drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])

    remix.unlink()
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Another Remix)")
    code, second = drive(["match", "run", path])

    assert code == int(ExitCode.PENDING_HUMAN)
    assert second["data"]["needs_review"][0]["why"] == str(match.Why.CANDIDATE_GONE)
    pending = second["pending_human_action"]
    assert pending["verify_verb"] == match_cli.CLEAR_VERB
    assert any(item_id in step for step in pending["steps"])
        # And the item identifier reaches a consumer on the channel built for codes.
    stalled = [w for w in second["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]
    assert [w["item"] for w in stalled] == [item_id]
    assert stalled[0]["remedy"] == match_cli.CLEAR_VERB

        # The escape actually works, which is what makes naming it worth anything.
    code, _ = drive(["review", "clear", item_id])
    assert code == int(ExitCode.OK)
    code, third = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert third["data"]["needs_review"][0]["why"] == str(match.Why.VERSION_DIFFERS)
    assert third["pending_human_action"]["verify_verb"] == match_cli.REVIEW_VERB


def stall(cfg, music, tmp_path, how_many: int) -> tuple[list[str], dict]:
    """Leave ``how_many`` questions carrying a verdict that cannot be applied, by accepting a
    candidate then replacing the file with a different remix, as a retag or move does."""
    lines = []
    for number in range(how_many):
        hold(music, f"08A - 124 - Artist{number} - Track{number} (Someone Remix)")
        lines.append(f"Artist{number} - Track{number} (Extended Mix)")
    path = write_list(tmp_path, "\n".join(lines) + "\n", f"stall{how_many}.txt")
    _code, first = drive(["match", "run", path])
    for row in first["data"]["needs_review"]:
        drive(
            ["review", "resolve", row["review_item"], "--verdict", "accepted",
             "--option", row["candidates"][0]["id"]]
        )
    for number in range(how_many):
        (music / f"08A - 124 - Artist{number} - Track{number} (Someone Remix).flac").unlink()
        hold(music, f"08A - 124 - Artist{number} - Track{number} (Another Remix)")
    _code, second = drive(["match", "run", path])
    return lines, second


def runnable_steps(pending: dict) -> list[list[str]]:
    return [step.split()[1:] for step in pending["steps"] if step.startswith("crate ")]


@pytest.mark.parametrize("how_many", [1, 2, 5])
def test_every_printed_remedy_is_a_command_that_actually_runs(cfg, music, tmp_path, how_many):
    """Every printed remedy is a command that actually runs.

    With two or more stalled items the identifiers were joined into one argument and the verb takes
    one positional, so the printed remedy exited 2. Each step is DRIVEN.
    """
    _lines, envelope = stall(cfg, music, tmp_path, how_many)
    assert envelope["exit_code"] == int(ExitCode.PENDING_HUMAN)
    pending = envelope["pending_human_action"]
    commands = runnable_steps(pending)
    assert len(commands) == how_many
    assert len({tuple(command) for command in commands}) == how_many
    for command in commands:
        assert command[:2] == ["review", "clear"]
        assert len(command) == 3, f"not a single-item invocation: {command}"
        code, _ = drive(command)
        assert code == int(ExitCode.OK), f"the printed remedy failed: {command}"
        # And the run is genuinely unblocked afterwards, which is what makes the remedy worth
        # printing.
    code, after = drive(["match", "run", str(tmp_path / f"stall{how_many}.txt")])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert not [
        row for row in after["data"]["needs_review"]
        if row["why"] in {str(match.Why.CANDIDATE_GONE), str(match.Why.VERDICT_UNSPECIFIC)}
    ]


def test_the_pending_action_counts_questions_rather_than_rows_in_both_halves(cfg, music, tmp_path):
    """The pending action counts questions rather than rows in both halves, so one line pasted twice
    does not print "1 tracks ... 2 of them"."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(
        tmp_path,
        "Aurora Bloom - Sun Path (Extended Mix)\nAurora Bloom - Sun Path (Extended Mix)\n",
        "twice.txt",
    )
    _code, envelope = drive(["match", "run", path])
    assert len(envelope["data"]["needs_review"]) == 2
    assert envelope["pending_human_action"]["summary"].startswith("1 tracks")
    assert len(queue_items(cfg)) == 1

    row = envelope["data"]["needs_review"][0]
    drive(["review", "resolve", row["review_item"], "--verdict", "accepted",
           "--option", row["candidates"][0]["id"]])
    (music / "08A - 124 - Aurora Bloom - Sun Path (Someone Remix).flac").unlink()
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Another Remix)")
    _code, stalled = drive(["match", "run", path])

    summary = stalled["pending_human_action"]["summary"]
    assert summary.startswith("1 tracks")
    assert "1 of them carry a verdict" in summary
    assert len(runnable_steps(stalled["pending_human_action"])) == 1
        # And the warning channel says it once, not once per row.
    assert len([w for w in stalled["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]) == 1


def test_a_verdict_this_build_cannot_read_leaves_the_item_answerable(cfg, music, tmp_path):
    """A verdict this build cannot read leaves the item answerable, since the way out of a wrong
    decision is to clear it and an unreachable item cannot be."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]

    with sqlite3.connect(review.queue_path(cfg)) as conn:
        conn.execute(
            "UPDATE review_items SET verdict = ? WHERE item_id = ?",
            ("deferred-until-tuesday", item_id),
        )

    code, second = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert second["data"]["needs_review"][0]["review_item"] == item_id
    assert second["data"]["needs_review"][0]["why"] == str(match.Why.VERSION_DIFFERS)


def test_a_question_answered_from_one_source_is_never_asked_again_from_another(
    cfg, music, tmp_path
):
    """R13 and R12 in one assertion: an identity carrying the provider's identifier would open a
    second question when the same playlist arrives as pasted text."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    hold(music, "08A - 124 - Nova Reef - Tide Line")
    provider = write_list(
        tmp_path, json.dumps({"list": 1, "origin": match.TIDAL, "tracks": TIDAL_ROWS}),
        "provider.json",
    )
    _code, first = drive(["match", "run", provider])
    item_id = first["data"]["needs_review"][0]["review_item"]
    option = first["data"]["needs_review"][0]["candidates"][0]["id"]
    drive(["review", "resolve", item_id, "--verdict", "accepted", "--option", option])

    pasted = write_list(tmp_path, TEXT_LINES, "pasted.txt")
    code, second = drive(["match", "run", pasted])
    assert code == int(ExitCode.OK)
    assert second["data"]["needs_review"] == []
    assert len(queue_items(cfg)) == 1


def test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier(
    cfg, music, tmp_path
):
    """R36: skipped by acquisition, and never omitted silently. The tombstone is recorded through
    the decision store U11 shipped, under the kind and identity this module declares."""
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    recorded = store.record(
        kind=match.TOMBSTONE_KIND,
        identity=match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)"),
        actor="test",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Someone Remix)\n")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]
    assert queue_items(cfg) == []


@pytest.mark.parametrize("row_title", ROW_SPELLINGS)
def test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it(
    cfg, music, tmp_path, row_title
):
    """A tombstone recorded from any row spelling suppresses the list that names it.

    Recorded as the deletion pass records it, artist and Title column verbatim, through the real
    store. Recomposing before hashing missed five of the seven spellings.
    """
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    recorded = store.record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", row_title),
        actor="deletion",
    )
    path = write_list(tmp_path, f"Aurora Bloom - {row_title}\n", "seam.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == [], (
        "a version standing under a tombstone was reported missing, so the next "
        "verb fetches back exactly what somebody deleted"
    )
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


def test_a_revoked_tombstone_stops_suppressing(cfg, music, tmp_path):
    """R36 says listable AND revocable, and revocable means the next run acquires."""
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    recorded = store.record(
        kind=match.TOMBSTONE_KIND,
        identity=match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)"),
        actor="test",
    )
    store.revoke(recorded.suppression_id, actor="test")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Someone Remix)\n")
    _code, envelope = drive(["match", "run", path])
    assert len(envelope["data"]["missing"]) == 1
    assert envelope["warnings"] == []


def test_a_tombstone_over_a_held_version_is_reported_rather_than_hidden(cfg, music, tmp_path):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=match.version_identity(artist="Aurora Bloom", title="Sun Path"), actor="test",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n")
    _code, envelope = drive(["match", "run", path])
    assert len(envelope["data"]["matched"]) == 1
    assert [w["code"] for w in envelope["warnings"]] == [match_cli.TOMBSTONE_OVER_OWNED]


def test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults(
    cfg, music, tmp_path
):
    """A stale tombstone is reported under every spelling the match consults, not only
    ``track.identity``, so ``Sun Path [Live]`` still reports a tombstone from ``Sun Path
    (Live)``."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path [Live]\n", "stale.txt")
    _code, envelope = drive(["match", "run", path])

    assert len(envelope["data"]["matched"]) == 1
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


def test_a_deletion_of_the_plain_record_never_withholds_the_credited_one(cfg, music, tmp_path):
    """A deletion of the plain record never withholds the credited one.

    The composed fallback asked under ``sun path``, which the recorder never writes for the credited
    row; an over eager suppression withholds wanted music silently. Both directions are asserted.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path"),
        actor="deletion",
    )
    credited = write_list(tmp_path, "Aurora Bloom - Sun Path (feat. Mira)\n", "credited.txt")
    _code, envelope = drive(["match", "run", credited])
    assert len(envelope["data"]["missing"]) == 1, (
        "a deletion of the plain record silently withheld the credited one"
    )

    plain = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "plain.txt")
    _code, still = drive(["match", "run", plain])
    assert still["data"]["missing"] == []
    assert [w["code"] for w in still["warnings"]] == [match_cli.SUPPRESSED_WARNING]


def deleted(cfg, title: str, *, version: str = "", content_id: str = "9001"):
    """A deletion recorded by the REAL recorder, companion and all."""
    from cratekit.deletion import stores
    from cratekit.deletion.library import RemovedRow

    return stores.record_tombstone(
        cfg,
        RemovedRow(
            content_id=content_id, recorded="2026-09-19", sequence=1, size=None,
            artist="Aurora Bloom", title=title, version=version,
        ),
        actor="deletion",
    )


@pytest.mark.parametrize(
    "row_title,row_version",
    [
        ("Sun Path (feat. Mira) (Nightwave Remix)", ""),
        ("Sun Path (Nightwave Remix) (feat. Mira)", ""),
        ("Sun Path [ft. Mira] [Nightwave Remix]", ""), ("Sun Path (feat. Mira)", "Nightwave Remix"),
    ],
)
def test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit(
    cfg, music, tmp_path, row_title, row_version
):
    """The shape the verbatim consult cannot reach, driven from the real recorder.

    The residual titled "A deleted track the tombstone consult cannot reach is listed for download"
    measured it MISSING and handed to a download; the listing names the version and no guest.
    """
    from cratekit.core import tombstone

    written = deleted(cfg, row_title, version=row_version)
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Nightwave Remix)\n", "provider.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert len(warnings) == 1
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    by_id = {record.suppression_id: record for record in store.suppressions()}
    standing = by_id[warnings[0]["suppression"]]
    assert standing.kind == tombstone.KIND_VERSION_UNCREDITED
    assert standing.payload["credited_id"] == written.suppression_id


@pytest.mark.parametrize(
    "listed",
    [
        "Sun Path (feat. Zed) (Nightwave Remix)", "Sun Path (Daybreak Remix)", "Sun Path",
    ],
)
def test_a_credited_deletion_withholds_nothing_but_its_own_version(cfg, music, tmp_path, listed):
    """The over eager direction: another guest, another remix and the bare recording are three
    things nobody deleted, each still missing with no warning."""
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    path = write_list(tmp_path, f"Aurora Bloom - {listed}\n", "other.txt")
    _code, envelope = drive(["match", "run", path])

    assert len(envelope["data"]["missing"]) == 1
    assert envelope["warnings"] == []


def test_a_provider_row_crediting_somebody_else_is_not_withheld(cfg):
    """The same guard through the reader that carries its version in a field."""
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    suppresses, identify = match_cli.suppression_view(
        review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    )
    other, same = match.read_tidal_tracks(
        [
            {"title": "Sun Path (feat. Zed)", "version": "Nightwave Remix",
             "artist": {"name": "Aurora Bloom"}},
            {"title": "Sun Path", "version": "Nightwave Remix",
             "artist": {"name": "Aurora Bloom"}},
        ]
    )
    assert match.standing_tombstone(other, suppresses=suppresses, suppression_id=identify) is None
    assert match.standing_tombstone(same, suppresses=suppresses, suppression_id=identify)


def test_a_listing_both_records_answer_is_reported_under_the_tombstone(cfg, music, tmp_path):
    """A listing both records answer is reported under the tombstone, the record a person wrote
    for that row, rather than the companion."""
    plain = deleted(cfg, "Sun Path (Nightwave Remix)", content_id="9002")
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Nightwave Remix)\n", "both.txt")
    _code, envelope = drive(["match", "run", path])
    assert [w["suppression"] for w in envelope["warnings"]] == [plain.suppression_id]


def test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion():
    """A credit with nothing in the title to show it never asks for a companion: a row billing Zed
    reads like one crediting nobody and would be withheld by a deletion crediting Mira."""
    solo, *billed = match.read_tidal_tracks(
        [
            {"title": "Sun Path", "version": "Nightwave Remix",
             "artists": [{"name": "Aurora Bloom"}]},
            {"title": "Sun Path", "version": "Nightwave Remix",
             "artists": [{"name": "Aurora Bloom"}, {"name": "Zed"}]},
            {"title": "Sun Path", "version": "Nightwave Remix",
             "artists": ["Aurora Bloom", "Zed"]},
            {"title": "Sun Path", "version": "Nightwave Remix",
             "artist": ["Aurora Bloom", "Zed"]},
        ]
    )
    assert {"artist": "aurora bloom", "title": "sun path (nightwave remix)"} in (
        solo.uncredited_spellings
    )
    assert [one.uncredited_spellings for one in billed] == [(), (), ()]
        # A blank entry is not a second artist, and a bare string is a list of one.
    padded, bare = match.read_tidal_tracks(
        [
            {"title": "Sun Path", "version": "", "artists": [{"name": "Aurora Bloom"}, {"name": " "}]},
            {"title": "Sun Path", "version": "", "artists": "Aurora Bloom, Zed"},
        ]
    )
    assert padded.uncredited_spellings and bare.uncredited_spellings


def test_a_wanted_nobody_read_from_a_listing_never_asks_for_a_companion():
    """Built by hand means nobody looked: the verb builds one from a held file whose title the
    index already took the credits off, so "no credit in it" is an absence of looking."""
    by_hand = match.Wanted(artist="Aurora Bloom", title="Sun Path", version="Nightwave Remix")
    assert by_hand.suppression_spellings
    assert by_hand.uncredited_spellings == ()


def test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale(cfg, music, tmp_path):
    """A held file crediting somebody else never calls the companion stale: it cannot say which
    guest it stands for."""
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (feat. Zed) (Nightwave Remix)")
    body = "Aurora Bloom - Sun Path (Nightwave Remix)\nAurora Bloom - Sun Path (Daybreak Remix)\n"
    _code, envelope = drive(["match", "run", write_list(tmp_path, body, "zed.txt")])

    assert [one["version"] for one in envelope["data"]["matched"]] == ["Nightwave Remix"]
    assert [one["version"] for one in envelope["data"]["needs_review"]] == ["Daybreak Remix"]
    assert [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED] == []


def test_a_deletion_of_the_plain_record_writes_no_companion(cfg, music, tmp_path):
    """The guard on the recording side: a row with no credit is one record, with nothing under
    the companion kind for anything to reach."""
    deleted(cfg, "Sun Path (Nightwave Remix)")
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    assert [record.kind for record in store.suppressions()] == [match.TOMBSTONE_KIND]

    credited = write_list(
        tmp_path, "Aurora Bloom - Sun Path (feat. Mira) (Nightwave Remix)\n", "credited.txt"
    )
    _code, envelope = drive(["match", "run", credited])
    assert len(envelope["data"]["missing"]) == 1
    assert envelope["warnings"] == []


def test_the_companion_reaches_exactly_what_ownership_reached(cfg, music, tmp_path):
    """The companion reaches exactly what ownership reached: while the credited row is HELD the
    listing without the guest resolves matched, so the deleted state agrees with it."""
    body = "Aurora Bloom - Sun Path (Nightwave Remix)\nAurora Bloom - Sun Path (Daybreak Remix)\n"
    held = hold(music, "08A - 124 - Aurora Bloom - Sun Path (feat. Mira) (Nightwave Remix)")
    _code, while_held = drive(["match", "run", write_list(tmp_path, body, "held.txt")])
    assert [(one["version"], one["why"]) for one in while_held["data"]["matched"]] == [
        ("Nightwave Remix", "exact")
    ]
    assert [one["version"] for one in while_held["data"]["needs_review"]] == ["Daybreak Remix"]

    held.unlink()
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    _code, once_deleted = drive(["match", "run", write_list(tmp_path, body, "deleted.txt")])
    assert [one["version"] for one in once_deleted["data"]["missing"]] == ["Daybreak Remix"]
    assert once_deleted["data"]["matched"] == []
    assert [w["code"] for w in once_deleted["warnings"]] == [match_cli.SUPPRESSED_WARNING]


@pytest.mark.parametrize(
    "recorded_row,listed",
    [
        ("Sun Path", "Sun Path (Original Mix)"), ("Sun Path (Original Mix)", "Sun Path"),
        ("Sun Path (Original Mix)", "Sun Path [Original Version]"),
    ],
)
def test_the_two_spellings_of_no_qualifier_at_all_reach_each_other(
    cfg, music, tmp_path, recorded_row, listed
):
    """The two spellings of no qualifier at all reach each other: ``version_token`` folds "Original
    Mix" to nothing, but the tombstone consult did not, so the version was re-acquired."""
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", recorded_row),
        actor="deletion",
    )
    path = write_list(tmp_path, f"Aurora Bloom - {listed}\n", "null.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


def test_a_tombstone_store_that_cannot_be_read_refuses_rather_than_matching(cfg, music, tmp_path):
    """Fail CLOSED: an unreadable tombstone store refuses, since treating it as empty would
    re-acquire what somebody removed. The snapshot is up front, before any track resolves."""
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    store.path.parent.mkdir(parents=True, exist_ok=True)
    store.path.write_text("[]")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n")
    code, envelope = drive(["match", "run", path])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "review-file-unusable"


def test_the_tombstone_store_is_a_declared_decision_store():
    """A store nobody declared is a file nobody chose a root for."""
    assert match_cli.TOMBSTONE_STORE in review.DECISION_STORE_KEYS


def test_the_handler_is_not_called_run():
    """``cli.run`` is the dispatcher, one frame away in every traceback."""
    assert not hasattr(match_cli, "run")
    assert callable(match_cli.match_list)


def test_the_verb_declares_the_queue_it_offers_into():
    """The one surface, assigned once, so a call site cannot invent a second."""
    assert match_cli.QUEUE is review.Queue.VERSION_MATCH
    assert registry.entry("match.run").adjudicates


# ── the list document, recognized positively ──────────────────────────────────


def _refusal(tmp_path, body, name="doc.json") -> CratekitError:
    with pytest.raises(CratekitError) as excinfo:
        match_cli.read_list(Path(write_list(tmp_path, body, name)))
    return excinfo.value


def test_a_document_from_a_newer_format_refuses_rather_than_reading_as_empty(tmp_path):
    """Reading it anyway reports a clean match over tracks it could not see."""
    cause = _refusal(tmp_path, json.dumps({"list": 2, "origin": "text", "tracks": []})).cause
    assert cause.reason == "intake-list-unusable"
    assert cause.code is ExitCode.PRECONDITION


def test_a_document_with_no_format_declaration_refuses(tmp_path):
    assert _refusal(tmp_path, json.dumps({"origin": "text", "tracks": []})).cause.detail


def test_a_boolean_is_not_a_format_number(tmp_path):
    """A bool is an int in this language, and one is not a document version."""
    assert _refusal(tmp_path, json.dumps({"list": True, "tracks": []}))


def test_a_top_level_array_is_refused_rather_than_read_as_no_tracks(tmp_path):
    with pytest.raises(CratekitError):
        match_cli.read_list(Path(write_list(tmp_path, "  [1, 2, 3]  ", "arr.json")))


def test_a_json_array_of_strings_is_not_quietly_read_as_a_tracklist(tmp_path):
    """A leading bracket counts as JSON, or ``["Artist - Title"]`` becomes one track with
    punctuation."""
    with pytest.raises(CratekitError):
        match_cli.read_list(Path(write_list(tmp_path, '["Aurora Bloom - Sun Path"]', "arr2.json")))


def test_a_null_tracks_field_is_refused_rather_than_read_as_an_empty_list(tmp_path):
    """An absent array and an empty one are different facts."""
    assert _refusal(tmp_path, json.dumps({"list": 1, "origin": "text", "tracks": None}))


def test_a_key_this_build_does_not_read_is_refused_rather_than_ignored(tmp_path):
    """A misspelled 'tracks' otherwise parses as a valid document holding none."""
    cause = _refusal(tmp_path, json.dumps({"list": 1, "origin": "text", "trakcs": ["A - B"]})).cause
    assert cause.detail["unknown"] == ["trakcs"]


def test_an_origin_this_build_cannot_read_is_refused(tmp_path):
    assert _refusal(tmp_path, json.dumps({"list": 1, "origin": "vinyl", "tracks": []}))


def test_a_track_of_the_wrong_shape_is_refused_with_its_position(tmp_path):
    cause = _refusal(
        tmp_path, json.dumps({"list": 1, "origin": match.TIDAL, "tracks": ["A - B"]})
    ).cause
    assert cause.detail["position"] == 1


@pytest.mark.parametrize(
    "given", ["https://example.invalid/playlist/1", " https://example.invalid/playlist/1"],
    ids=["plain", "leading-space"],
)
def test_a_web_address_is_refused_with_its_own_sentence(tmp_path, given):
    """Fetching a playlist needs a session and pagination; the intake verbs own both. A leading
    space survives a paste, so anchoring the scheme at the first character missed it."""
    with pytest.raises(CratekitError) as excinfo:
        match_cli.read_list(Path(given))
    assert "web address" in excinfo.value.cause.message


def test_a_list_that_is_not_there_refuses_with_a_code_from_the_vocabulary(cfg, tmp_path):
    code, envelope = drive(["match", "run", str(tmp_path / "nope.txt")])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "intake-list-unusable"


@pytest.mark.parametrize(
    "body", ["", "   \n\n  \n", "# only a comment\n# and another\n"],
    ids=["empty", "blank", "comments"],
)
def test_a_tracklist_with_no_track_lines_refuses_rather_than_matching_over_nothing(
    cfg, music, tmp_path, body
):
    """A tracklist with no track lines refuses rather than matching over nothing: "every track is
    owned" and "your list was empty" are the same three empty arrays."""
    path = write_list(tmp_path, body, "blank.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_a_document_that_declares_an_empty_track_array_is_still_a_list(cfg, tmp_path):
    """A positive declaration of zero tracks HAS said something, unlike a file with nothing
    readable in it, which is what the null tracks refusal above draws."""
    path = write_list(
        tmp_path, json.dumps({"list": 1, "origin": match.TEXT, "tracks": []}), "empty.json"
    )
    assert match_cli.read_list(Path(path)) == ()


def test_a_document_row_carrying_a_line_break_is_refused_with_its_array_position(tmp_path):
    """A row carrying a line break is refused with its array position; rows joined with newlines
    and re-split cited a nonexistent line and turned one row into two tracks."""
    cause = _refusal(
        tmp_path,
        json.dumps(
            {"list": 1, "origin": match.TEXT,
             "tracks": ["Aurora Bloom - Sun Path", "Nova Reef - Tide\nMore - Tracks"]}
        ),
        "rows.json",
    ).cause
    assert cause.detail["position"] == 2


def test_a_malformed_document_row_is_refused_at_its_own_position(tmp_path):
    """The position is the array index, not a line in a string the caller never had."""
    cause = _refusal(
        tmp_path,
        json.dumps(
            {"list": 1, "origin": match.TEXT,
             "tracks": ["", "# comment", "Aurora Bloom - Sun Path", "just some words"]}
        ),
        "positions.json",
    ).cause
    assert cause.detail["position"] == 4


def test_a_text_document_and_a_plain_text_file_read_the_same(tmp_path):
    document = write_list(
        tmp_path, json.dumps({"list": 1, "origin": match.TEXT, "tracks": TEXT_LINES.splitlines()}),
        "lines.json",
    )
    plain = write_list(tmp_path, TEXT_LINES, "plain.txt")
    assert match_cli.read_list(Path(document)) == match_cli.read_list(Path(plain))


def test_the_naming_template_the_index_uses_is_the_declared_one():
    """A second template here would read the library by a convention nobody writes."""
    assert naming.NameTemplate().head_fields == ("key", "bpm")


# ── Part 6: the identity of a QUESTION, and the coefficients nothing was reading ──


def keyed_list(tmp_path, name: str, **fields) -> str:
    """One provider row as a list document, so the key travels in its own field."""
    row = {"id": "1", "title": "Sun Path", "artist": {"name": "Aurora Bloom"}}
    row.update(fields)
    return write_list(
        tmp_path, json.dumps({"list": 1, "origin": match.TIDAL, "tracks": [row]}), name,
    )


def test_a_version_answer_never_settles_a_key_question_about_the_same_line(cfg, music, tmp_path):
    """A version answer never settles a key question about the same line, through the real verbs.

    One item for both questions applied an answer about the extended mix to a key question about
    03B, the RELATIVE MINOR ``Why.KEY_RELATIVE`` exists to catch; it must be a QUESTION again.
    """
    hold(music, "05B - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    path = keyed_list(tmp_path, "relative.json", key="03A")

    code, asked = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    version_row = asked["data"]["needs_review"][0]
    assert version_row["why"] == str(match.Why.VERSION_DIFFERS)
    version_item = version_row["review_item"]
    drive(["review", "resolve", version_item, "--verdict", "accepted"])

    _code, settled = drive(["match", "run", path])
    accepted = settled["data"]["matched"][0]
    assert accepted["why"] == str(match.Why.VERDICT_ACCEPTED)
    assert [Path(p).name for p in accepted["paths"]] == [
        "05B - 124 - Aurora Bloom - Sun Path (Extended Mix).flac"
    ]

    hold(music, "03B - 124 - Aurora Bloom - Sun Path")
    code, after = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN), (
        "the version answer settled a key question nobody asked"
    )
    assert after["data"]["matched"] == []
    key_row = after["data"]["needs_review"][0]
    assert key_row["why"] == str(match.Why.KEY_RELATIVE)
    assert key_row["review_item"] != version_item
    assert key_row["paths"] == []
        # Both items are in the store, one answered and one open.
    assert len(queue_items(cfg)) == 2


def test_two_versions_of_one_recording_are_two_questions_and_two_answers(cfg, music, tmp_path):
    """Two versions of one recording are two questions and two answers, not one item."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    both = write_list(
        tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\nAurora Bloom - Sun Path (Radio Edit)\n",
        "versions.txt",
    )
    _code, asked = drive(["match", "run", both])
    rows = {row["version"]: row for row in asked["data"]["needs_review"]}
    assert set(rows) == {"Extended Mix", "Radio Edit"}
    assert rows["Extended Mix"]["review_item"] != rows["Radio Edit"]["review_item"]

    drive(
        ["review", "resolve", rows["Extended Mix"]["review_item"],
         "--verdict", "accepted",
         "--option", rows["Extended Mix"]["candidates"][0]["id"]]
    )
    code, after = drive(["match", "run", both])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert [row["version"] for row in after["data"]["matched"]] == ["Extended Mix"]
    assert [row["version"] for row in after["data"]["needs_review"]] == ["Radio Edit"]


@pytest.mark.parametrize(
    "answered_at,then_held,answered_why,later_why",
    [
        ("08A", "03B", match.Why.KEY_DIFFERS, match.Why.KEY_RELATIVE),
        ("03B", "08A", match.Why.KEY_RELATIVE, match.Why.KEY_DIFFERS),
    ],
    ids=["differs-then-relative", "relative-then-differs"],
)
def test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another(
    cfg, music, tmp_path, answered_at, then_held, answered_why, later_why
):
    """An unspecific yes about one copy does not settle a question about another.

    ``KEY_DIFFERS`` and ``KEY_RELATIVE`` are one item by design, so ``apply_verdict`` binds an
    unspecific yes to the offered option and a different candidate stalls as a gone one. The same
    yes against the UNCHANGED library must still apply.
    """
    listed = keyed_list(tmp_path, "asked.json", key="03A")
    held = hold(music, f"{answered_at} - 124 - Aurora Bloom - Sun Path")

    _code, first = drive(["match", "run", listed])
    asked = first["data"]["needs_review"][0]
    assert asked["why"] == str(answered_why)
    item_id = asked["review_item"]
    drive(["review", "resolve", item_id, "--verdict", "accepted"])

        # The answer applies to the copy it was given about.
    code, settled = drive(["match", "run", listed])
    assert code == int(ExitCode.OK)
    assert settled["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)
    assert [Path(p).name for p in settled["data"]["matched"][0]["paths"]] == [held.name]

    held.unlink()
    swapped = hold(music, f"{then_held} - 124 - Aurora Bloom - Sun Path")

    code, after = drive(["match", "run", listed])
    assert code == int(ExitCode.PENDING_HUMAN), (
        f"an unspecific yes about the {answered_at} copy was applied to the "
        f"{then_held} copy"
    )
    assert after["data"]["matched"] == []
    row = after["data"]["needs_review"][0]
    assert row["review_item"] == item_id
    assert row["why"] == str(match.Why.CANDIDATE_GONE)
    assert swapped.name not in [
        path for state in after["data"].values() for r in state for path in r["paths"]
    ]
        # And the run says so, on the channel that carries a verdict it cannot apply.
    warned = [w for w in after["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]
    assert [(w["item"], w["remedy"]) for w in warned] == [(item_id, match_cli.CLEAR_VERB)]
        # The question underneath is still the other one: a binding on the answer, not a split of
        # the identity.
    assert match.question_shape(later_why) == match.question_shape(answered_why)


def test_the_set_that_names_the_key_questions_is_what_the_identity_reads():
    """The set that names the key questions is what the identity reads: ``KEY_QUESTIONS`` was named
    by nothing else, and a why leaving it stops being a key question."""
    assert match.KEY_QUESTIONS == {match.Why.KEY_RELATIVE, match.Why.KEY_DIFFERS}
    for why in match.KEY_QUESTIONS:
        assert match.question_shape(why) == match.ASKS_ABOUT_KEY
        # And nothing else is a key question, so the set is a boundary and not a list of examples.
    for why in (match.Why.VERSION_DIFFERS, match.Why.TITLE_APPROXIMATE,
                match.Why.READING_AMBIGUOUS):
        assert match.question_shape(why) != match.ASKS_ABOUT_KEY


#: How many identifiers the width has to survive before a collision is as likely as not: a
#: billion, a lifetime total for a library scale user.
REQUIRED_EVEN_ODDS_POPULATION = 1_000_000_000


def even_odds_population(width: int) -> float:
    """How many identifiers of this hex width before a collision is even money: the birthday bound,
    ``sqrt(2 ln2 . 2^bits)``, four bits per hex character."""
    import math

    return math.sqrt(2 * math.log(2) * 2 ** (4 * width))


def smallest_sufficient_width() -> int:
    """The narrowest WHOLE-BYTE hex width that clears the requirement; an odd width is half a byte,
    so the search steps by two."""
    return next(
        width
        for width in range(2, 65, 2)
        if even_odds_population(width) >= REQUIRED_EVEN_ODDS_POPULATION
    )


def test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement():
    """The expectation is computed, not asked of the thing it verifies.

    ``len(digest) == match.DIGEST_WIDTH`` passes at EVERY width, so the answer is the narrowest
    whole byte width meeting a population and a birthday bound, checked against the module's own
    comment.
    """
    assert round(even_odds_population(8)) == 77163
    assert 5.0e9 < even_odds_population(16) < 5.1e9
    assert match.DIGEST_WIDTH == smallest_sufficient_width()
    assert match.DIGEST_WIDTH % 2 == 0
    assert even_odds_population(match.DIGEST_WIDTH) >= REQUIRED_EVEN_ODDS_POPULATION
    assert even_odds_population(match.DIGEST_WIDTH - 2) < REQUIRED_EVEN_ODDS_POPULATION


def test_the_declared_width_survives_a_population_a_narrower_one_does_not():
    """The birthday argument, driven: identifiers synthesized from a library shaped population
    collide at half the declared width and not at the declared one. The inputs are fixed."""
    import hashlib

    def digest_at(width: int, parts: tuple[str, ...]) -> str:
        return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:width]

    population = [
        (f"Artist {a:03d}", f"Title {t:03d}", f"Version {v:02d}", f"{k:02d}A")
        for a in range(40)
        for t in range(50)
        for v in range(10)
        for k in range(5)
    ]
    assert len(population) == 100_000
    narrow = {digest_at(8, parts) for parts in population}
    declared = {digest_at(match.DIGEST_WIDTH, parts) for parts in population}
    assert len(population) - len(narrow) > 0, (
        "the narrow width stopped colliding, so this no longer discriminates"
    )
    assert len(declared) == len(population), (
        f"{len(population) - len(declared)} collisions at the declared width"
    )


def test_every_identifier_this_module_generates_is_the_declared_width(cfg, music, tmp_path):
    """Every identifier this module generates is the declared width, against a computed expectation.

    Halving the width left the suite green, since a suite drives tens of identifiers. Comparing with
    ``match.DIGEST_WIDTH`` would be the constant verifying itself.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    path = write_list(
        tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\nNova Reef - Tide Line\n", "widths.txt",
    )
    _code, envelope = drive(["match", "run", path])
    seen: list[str] = []
    for state in ("matched", "needs_review", "missing"):
        for row in envelope["data"][state]:
            seen.append(row["id"])
            seen.extend(candidate["id"] for candidate in row["candidates"])
            seen.extend(option["id"] for option in row["acquisition"])
    assert len(seen) >= 4
    expected = smallest_sufficient_width()
    for identifier in seen:
        prefix, _, digest = identifier.partition("_")
        assert prefix in {"mt", "cd", "aq"}
        assert len(digest) == expected, identifier
        assert set(digest) <= set("0123456789abcdef")


def test_a_resemblance_below_the_floor_is_missing_rather_than_a_question(cfg, music, tmp_path):
    """The floor is a product dial and nothing was pinning it.

    Its cost is "noise in the queue", the residual titled "The ambiguous reading class is queued as
    a
    question and does not gate the run". The example is measured by the residual titled "The index
    reads a
    file's title one way, so the disk side of the one-word dash stays narrow": ``Sun Path`` against
    only ``Sun Path Instrumental`` scores 76.4.
    """
    from rapidfuzz import fuzz

    score = fuzz.token_sort_ratio(
        match.recording_token("Aurora Bloom", "Sun Path"),
        match.recording_token("Aurora Bloom", "Sun Path Instrumental"),
    )
    assert 41 <= score < match.APPROXIMATE_FLOOR, (
        "this row no longer sits between the two floors it is meant to separate"
    )

    hold(music, "08A - 124 - Aurora Bloom - Sun Path Instrumental")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "floor.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["data"]["needs_review"] == []
    assert envelope["data"]["missing"][0]["why"] == str(match.Why.NOT_IN_LIBRARY)


#: The two library titles either side of the floor with nothing between them, scores measured
#: (81.63 and 82.35), so 82 is the only integer floor between them.
FLOOR_NEIGHBOURS = ("Sun Pat Reprise", "Sun Path Meridian")


def test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way(cfg, music, tmp_path):
    """The floor is pinned from both sides by the nearest score either way.

    A constant pinned only from the extremes has a free band. At 82 exactly one of two resembling
    recordings is a candidate, one lower and both are, one higher and none. Scores are COMPUTED.
    """
    from rapidfuzz import fuzz

    asked = match.recording_token("Aurora Bloom", "Sun Path")
    below, above = (
        fuzz.token_sort_ratio(asked, match.recording_token("Aurora Bloom", title))
        for title in FLOOR_NEIGHBOURS
    )
    assert below < match.APPROXIMATE_FLOOR <= above, (
        f"{FLOOR_NEIGHBOURS} no longer straddle the floor: {below} and {above}"
    )
    assert int(above) - int(below) <= 1, (
        "the two neighbours drifted apart, so they no longer pin the floor to one value"
    )

    for title in FLOOR_NEIGHBOURS:
        hold(music, f"08A - 124 - Aurora Bloom - {title}")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "band.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.PENDING_HUMAN), (
        "raising the floor past the nearer neighbour removed the question entirely"
    )
    row = envelope["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)
    assert [candidate["title"] for candidate in row["candidates"]] == [
        FLOOR_NEIGHBOURS[1]
    ], "the offer no longer holds exactly the recordings the floor admits"


def test_the_scorer_is_capped_at_the_same_number_the_offer_is(cfg, music, tmp_path):
    """The scorer is capped at the same number the offer is. The two spends are told apart by the
    WITHHELD COUNT: eight one version recordings build five candidates, nothing kept back, when
    capped, and eight built, five shown, three withheld when uncapped."""
    for suffix in "ABCDEFGH":
        hold(music, f"08A - 124 - Aurora Bloom - Sun Path {suffix}")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n", "cap.txt")
    _code, envelope = drive(["match", "run", path])
    row = envelope["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)
    assert len(row["candidates"]) == match.APPROXIMATE_LIMIT
    assert row["candidates_withheld"] == 0, (
        "more recordings reached the candidate builder than the recording cap allows"
    )
    assert [
        warning for warning in envelope["warnings"]
        if warning["code"] == match_cli.CANDIDATES_WITHHELD
    ] == []


def test_an_unspecific_acceptance_stalls_the_run_the_same_way_a_gone_candidate_does(
    cfg, music, tmp_path
):
    """Both members of ``STALLED`` earn their place: dropping ``VERDICT_UNSPECIFIC`` left the suite
    green but lost its warning, the ``review clear`` remedy and its place in the pending action."""
    hold(music, "08A - 124 - Aurora Bloom - Tide Line (Someone Remix)")
    hold(music, "03A - 124 - Aurora Bloom - Tide Line (Another Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Tide Line (Extended Mix)\n", "vague.txt")
    _code, first = drive(["match", "run", path])
    item_id = first["data"]["needs_review"][0]["review_item"]
    assert len(first["data"]["needs_review"][0]["candidates"]) == 2
    drive(["review", "resolve", item_id, "--verdict", "accepted"])

    code, after = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    row = after["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.VERDICT_UNSPECIFIC)
    warned = [w for w in after["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]
    assert [(w["item"], w["remedy"]) for w in warned] == [(item_id, match_cli.CLEAR_VERB)]
    pending = after["pending_human_action"]
    assert pending["verify_verb"] == match_cli.CLEAR_VERB
    assert f"crate review clear {item_id}" in pending["steps"]
        # Not filed as answerable: ``review resolve`` refuses it, so a step telling somebody to
        # record a verdict on it is a printed instruction that fails.
    assert not any(step.startswith("list the version-match queue") for step in pending["steps"])


def test_an_unanswered_item_is_re_offered_so_its_candidates_follow_the_library(
    cfg, music, tmp_path
):
    """An unanswered item is re-offered so its candidates follow the library, or ``review show``
    offers candidates that no longer exist."""
    first_file = hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n", "moving.txt")
    _code, asked = drive(["match", "run", path])
    item_id = asked["data"]["needs_review"][0]["review_item"]
    stored = {option.option_id for option in queue_items(cfg)[0].options}
    assert stored == {
        candidate["id"] for candidate in asked["data"]["needs_review"][0]["candidates"]
    }

    first_file.unlink()
    hold(music, "03A - 124 - Aurora Bloom - Sun Path (Another Remix)")
    _code, again = drive(["match", "run", path])
    offered = again["data"]["needs_review"][0]
    assert offered["review_item"] == item_id
    refreshed = queue_items(cfg)[0]
    assert {option.option_id for option in refreshed.options} == {
        candidate["id"] for candidate in offered["candidates"]
    }
    assert {option.option_id for option in refreshed.options} != stored, (
        "the item kept offering a candidate the library no longer holds"
    )
    assert refreshed.payload["candidates"] == offered["candidates"]


def test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported(cfg, music, tmp_path):
    """A tombstone over the file being offered as the answer is reported, in both states.

    A candidate is a version the list did NOT spell, so the warning loop, asking under
    ``Wanted.addresses``, missed a tombstone over the file OFFERED.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path - Live\n", "stale.txt")

    code, asked = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    row = asked["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.READING_AMBIGUOUS)
    stale = [w for w in asked["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in stale] == [recorded.suppression_id]

    drive(
        ["review", "resolve", row["review_item"], "--verdict", "accepted",
         "--option", row["candidates"][0]["id"]]
    )
    _code, settled = drive(["match", "run", path])
    assert settled["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)
    still = [w for w in settled["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in still] == [recorded.suppression_id], (
        "the row that reports ownership of a tombstoned file says nothing about it"
    )


def test_one_tombstone_over_one_row_is_one_warning_however_it_is_reached(cfg, music, tmp_path):
    """One tombstone over one row is one warning however it is reached: the row's own address and
    the offered file are one suppression."""
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Live)\n", "once.txt")
    _code, envelope = drive(["match", "run", path])
    stale = [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in stale] == [recorded.suppression_id]


#: U24's ``cratekit.core.tombstone.VERSION_WORDS``, WRITTEN OUT INDEPENDENTLY, since a pin
#: computed from the thing it pins asserts the code agrees with itself.
U24_VERSION_WORDS: frozenset[str] = frozenset(
    {
        "acapella", "acoustic", "alternate", "bootleg", "club", "cut", "demo",
        "dub", "edit", "extended", "flip", "instrumental", "interlude", "live",
        "mashup", "mix", "original", "radio", "remaster", "remastered", "remix",
        "reprise", "rework", "session", "unplugged", "version", "vip",
    }
)

#: Words in this module's list and nobody else's, and the reverse; the second column cost, each
#: reported MISSING for a held file.
VOCABULARY_GAP: tuple[str, ...] = (
    "acapella", "alternate", "club", "cut", "flip", "interlude", "mashup",
    "original", "radio", "session", "unplugged",
)


def test_the_version_vocabulary_is_u24s_element_for_element():
    """One question, one vocabulary, and there were two: the deletion pass and this module both ask
    "is this word a version designation". ``rerecorded`` is the one deliberate difference, a HEAD
    word."""
    assert match.VERSION_WORDS == U24_VERSION_WORDS
    assert set(VOCABULARY_GAP) < match.VERSION_WORDS
        # Derived, so a word cannot be added to one and forgotten in the other.
    assert match_identity._DASH_VERSIONS == match.VERSION_WORDS | match_identity._DASH_VERSION_HEADS
    assert match_identity._DASH_VERSIONS - match.VERSION_WORDS == {"rerecorded"}


@pytest.mark.parametrize("word", VOCABULARY_GAP)
def test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file(
    cfg, music, tmp_path, word
):
    """The measured cost of the second vocabulary, one row per missing word: a held ``(Unplugged)``
    file reported MISSING for the dash spelling and was fetched, at exit zero, for eleven words."""
    hold(music, f"08A - 124 - Aurora Bloom - Sun Path ({word.title()})")
    path = write_list(tmp_path, f"Aurora Bloom - Sun Path - {word.title()}\n", f"{word}.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == [], f"{word} re-acquires a file on the shelf"
    row = envelope["data"]["needs_review"][0]
    assert row["why"] == str(match.Why.READING_AMBIGUOUS)
    assert row["acquisition"] == []
    assert [candidate["version"] for candidate in row["candidates"]] == [word.title()]


def test_the_pending_summary_counts_every_outstanding_question_not_only_the_gating_ones(
    cfg, music, tmp_path
):
    """The pending summary counts every outstanding question, not only the gating ones.

    The ungated class was filtered from the SENTENCE as well as the gate, so 24 rows printed "4
    tracks ... need a person". The exit status must not change.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    for tail in ("Live", "Edit", "Dub"):
        hold(music, f"08A - 124 - Nova Reef - Tide Line ({tail})")
    path = write_list(
        tmp_path,
        "Aurora Bloom - Sun Path (Extended Mix)\n"
        "Nova Reef - Tide Line - Live\n"
        "Nova Reef - Tide Line - Edit\n"
        "Nova Reef - Tide Line - Dub\n",
        "counts.txt",
    )
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert len(envelope["data"]["needs_review"]) == 4
    summary = envelope["pending_human_action"]["summary"]
    assert summary.startswith("1 tracks")
    assert "3 further questions are queued and did not block this run" in summary
    assert "4 outstanding in all" in summary
    assert any("3 further questions" in step for step in envelope["pending_human_action"]["steps"])


def test_an_ungated_question_on_its_own_still_leaves_the_run_at_exit_zero(cfg, music, tmp_path):
    """The count is in the sentence and not in the gate, which is the whole point."""
    for tail in ("Live", "Edit"):
        hold(music, f"08A - 124 - Nova Reef - Tide Line ({tail})")
    path = write_list(
        tmp_path, "Nova Reef - Tide Line - Live\nNova Reef - Tide Line - Edit\n", "onlyungated.txt",
    )
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["pending_human_action"] is None
    assert len(envelope["data"]["needs_review"]) == 2
    assert len([w for w in envelope["warnings"] if w["code"] == match_cli.READING_UNSETTLED]) == 2


def test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire(cfg, music, tmp_path):
    """Rejecting an ambiguous reading can skip rather than acquire.

    The ambiguous reading residual claimed the readings "ALWAYS differ in acquisition", false when
    a tombstone stands over the reading the LIST spelled: accepting holds, rejecting is SUPPRESSED.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path - Live"),
        actor="deletion",
    )
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    hold(music, "08A - 124 - Nova Reef - Tide Line (Live)")
    tombstoned = write_list(tmp_path, "Aurora Bloom - Sun Path - Live\n", "skip.txt")
    control = write_list(tmp_path, "Nova Reef - Tide Line - Live\n", "fetch.txt")

    for path, verdict in ((tombstoned, "accepted"), (control, "accepted")):
        _code, asked = drive(["match", "run", path])
        row = asked["data"]["needs_review"][0]
        drive(
            ["review", "resolve", row["review_item"], "--verdict", verdict,
             "--option", row["candidates"][0]["id"]]
        )
    _code, held = drive(["match", "run", tombstoned])
    assert held["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)
    assert len(held["data"]["matched"][0]["paths"]) == 1

        # Now the other answer to the same question, on both lists.
    for path in (tombstoned, control):
        item_id = drive(["match", "run", path])[1]["data"]["matched"][0]["review_item"]
        drive(["review", "clear", item_id])
        _code, asked = drive(["match", "run", path])
        row = asked["data"]["needs_review"][0]
        drive(["review", "resolve", row["review_item"], "--verdict", "rejected"])

    _code, skipped = drive(["match", "run", tombstoned])
    assert skipped["data"]["matched"] == []
    assert skipped["data"]["missing"] == []
    assert skipped["data"]["needs_review"] == []
    assert [w["code"] for w in skipped["warnings"]] == [match_cli.SUPPRESSED_WARNING]

    _code, fetched = drive(["match", "run", control])
    row = fetched["data"]["missing"][0]
    assert row["why"] == str(match.Why.VERDICT_REJECTED)
    assert len(row["acquisition"]) == 1


def test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it(
    cfg, music, tmp_path
):
    """What the enumeration residual costs, measured: with the file gone, the dash spelled list
    exits 0 with a missing row and ZERO warnings, where the bracket spelled control warns of the
    suppression."""
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND, identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    bracketed = write_list(tmp_path, "Aurora Bloom - Sun Path (Live)\n", "bracket.txt")
    dashed = write_list(tmp_path, "Aurora Bloom - Sun Path - Live\n", "dash.txt")

    code, reached = drive(["match", "run", bracketed])
    assert code == int(ExitCode.OK)
    assert reached["data"] == {"matched": [], "needs_review": [], "missing": []}
    assert [(w["code"], w["suppression"]) for w in reached["warnings"]] == [
        (match_cli.SUPPRESSED_WARNING, recorded.suppression_id)
    ]

    code, missed = drive(["match", "run", dashed])
    assert code == int(ExitCode.OK)
    row = missed["data"]["missing"][0]
    assert row["why"] == str(match.Why.NOT_IN_LIBRARY)
    assert [option["query"] for option in row["acquisition"]] == ["Aurora Bloom Sun Path - Live"]
    assert missed["warnings"] == [], (
        "the run that undoes a deliberate deletion now says so, and this entry's "
        "cost has changed"
    )


#: A residual cited the old way, built from pieces so this pattern does not match its own
#: source line.
_BY_NUMBER = re.compile(r"\bR" + "-" + r"[0-9]+")

#: The files this unit owns. Other units cite their own residuals by number.
UNIT_FILES = (*MATCH_SOURCES, MATCH_CLI_SOURCE, Path(__file__).resolve())


def test_every_residual_this_unit_cites_is_a_heading_that_exists():
    """Every title in ``RESIDUALS`` is a heading in ``docs/residual-findings.md``, so a RETITLE
    fails a test."""
    headings = {
        line.split(". ", 1)[1].strip()
        for line in RESIDUALS_DOC.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ") and ". " in line
    }
    missing = [title for title in RESIDUALS if title not in headings]
    assert missing == [], f"cited titles that are not headings: {missing}"


def test_every_residual_title_this_unit_names_is_actually_cited_somewhere():
    """A register that outlives its citations is a list nobody maintains."""
    prose = "\n".join(path.read_text(encoding="utf-8") for path in UNIT_FILES)
        # A title is cited when it appears somewhere other than the tuple that declares it.
        # Comment markers and quotes come off first, because a title is written across adjacent
        # string literals in the register and across several ``#:`` lines in the source.
    flattened = re.sub(r"\s+", " ", re.sub(r"#:?", " ", prose).replace('"', " "))
    for title in RESIDUALS:
        assert flattened.count(re.sub(r"\s+", " ", title)) >= 2, title


def test_no_residual_is_cited_by_number_anywhere_in_this_unit():
    """A residual cited by number stops resolving silently when branches renumber, so every
    citation here names a title."""
    for path in UNIT_FILES:
        found = _BY_NUMBER.findall(path.read_text(encoding="utf-8"))
        assert found == [], f"{path.name} cites a residual by number: {found}"


# ── U265: the approximate pass sorts each name's words once, and answers as before ──
# ``_approximate`` handed ``rapidfuzz`` ``token_sort_ratio``, which re-sorts both strings for
# every pair. It now sorts each name once per index and scores the sorted forms with
# ``fuzz.ratio``. The matcher decides what is acquired, so the shipped call is kept below as
# the reference and the new pass is held EQUAL to it.


def _shipped_approximate(wanted, index, *, limit=match.APPROXIMATE_LIMIT):
    """The scorer as shipped before U265, kept as the reference it is held to. ``limit`` is the
    offer limit unless a caller asks for every recording over the floor."""
    from rapidfuzz import fuzz, process

    if not index.by_recording:
        return ()
    found = process.extract(
        wanted.recording, tuple(index.by_recording), scorer=fuzz.token_sort_ratio,
        score_cutoff=match.APPROXIMATE_FLOOR, limit=limit,
    )
    return tuple(held for token, _score, _position in found for held in index.versions(token))


#: Words for generated names: plain, accented, fullwidth, ligatures, other scripts, a
#: repeated word, and the halves that fold to nothing.
_U265_WORDS = (
    "sun", "path", "aurora", "bloom", "night", "drive", "deep", "echo", "you", "me",
    "Beyoncé", "Sigur Rós", "Röyksopp", "Ｓｕｎ", "Ｐａｔｈ", "naïve", "straße", "ﬁne",
    "東京", "Привет", "écho", "dup dup dup", "Ⅻ", "", "!!!", "01",
)


def _u265_library(seed: int) -> tuple[match.LibraryIndex, list[match.Wanted]]:
    """A generated library and list, tie dense on purpose: words including empty halves, the
    fixtures' ``Sun Path`` naming with edits, and artist and title swapped."""
    import random

    rng = random.Random(seed)

    def name(most: int) -> str:
        return " ".join(rng.choice(_U265_WORDS) for _ in range(rng.randint(0, most)))

    pairs: set[tuple[str, str]] = set()
    for _ in range(140):
        pairs.add((name(3), name(4)))
    for stem in ("Sun Path", "Sun Pathway", "Night Drive", "Deep Echo"):
        for tail in ("", "x", "s", "y", " Alt", " Mix", " 2", " Ways", "ss"):
            for artist in ("Aurora Bloom", "Aurora Blooms", "Bloom Aurora"):
                pairs.add((artist, stem + tail))
    pairs |= {(title, artist) for artist, title in list(pairs)[:40]}
    held = [
        match.Owned(path=Path(f"{n:04d}.flac"), artist=a, title=t, version=v, key=None)
        for n, (a, t) in enumerate(sorted(pairs))
        for v in ("",) * (1 + n % 2)
    ]
    grouped: dict[str, list[match.Owned]] = {}
    for owned in held:
        grouped.setdefault(owned.recording, []).append(owned)
    index = match.LibraryIndex(by_recording={k: tuple(v) for k, v in grouped.items()})

    rows = [one(artist=name(3), title=name(4)) for _ in range(60)]
    rows += [
        one(artist=artist, title=stem + tail)
        for stem in ("Sun Path", "Night Drive", "Sun Pathwayss")
        for tail in ("", "x", "ss", " Alt")
        for artist in ("Aurora Bloom", "Aurora Bloomz", "")
    ]
    rows += [one(artist="", title=""), one(artist="Path Sun", title="Bloom Aurora")]
    return index, rows


@pytest.mark.parametrize("limit", [match.APPROXIMATE_LIMIT, None])
@pytest.mark.parametrize("seed", [265, 2650, 26500])
def test_the_approximate_pass_answers_exactly_as_the_shipped_scorer(seed, limit):
    """Every row's candidates, in their order, equal the shipped scorer's, over a fixture asserted
    to carry rows over five recordings, equal scores and nothing over the floor."""
    from rapidfuzz import fuzz, process

    index, rows = _u265_library(seed)
    over_the_limit = tied_inside = nothing = 0
    for wanted in rows:
        assert match._approximate(wanted, index, limit=limit) == _shipped_approximate(
            wanted, index, limit=limit
        ), wanted.recording
        every = process.extract(
            wanted.recording, tuple(index.by_recording), scorer=fuzz.token_sort_ratio,
            score_cutoff=match.APPROXIMATE_FLOOR, limit=None,
        )
        over_the_limit += len(every) > match.APPROXIMATE_LIMIT
        kept = [score for _token, score, _position in every[: match.APPROXIMATE_LIMIT]]
        tied_inside += len(kept) != len(set(kept))
        nothing += not every
    assert over_the_limit and tied_inside and nothing, (
        "the generated library no longer carries more than five hits, ties inside "
        "the five and empty answers, so equality is not being tested where it can fail"
    )


def test_every_pair_scores_the_same_through_the_sorted_form():
    """The whole matrix, no cutoff: ``ratio`` over the sorted forms equals ``token_sort_ratio``
    for every pair, as a float, so a pair the sort disagreed about under the floor cannot hide."""
    from rapidfuzz import fuzz

    index, rows = _u265_library(7)
        # Raw tokens too, never folded, at every width and with the two characters the scorer
        # splits on in a wide string and not in a narrow one.
    raw = [
        "a\x85b\x1fc", "a\xa0b\x1fc d", "x\xa0y\x1fПривет", "a\x85b body\x1fﬁne",
        "\x1f", "", " ", "\x1f\x1f", "tab\there\x1f  spaced  ", "😀\x1fz a\xa0b",
    ]
    choices = list(index.by_recording) + raw
    asked = [wanted.recording for wanted in rows] + choices[:50] + raw
    for query in asked:
        sorted_query = match._sorted_words(query)
        for choice in choices:
            assert fuzz.ratio(sorted_query, match._sorted_words(choice)) == (
                fuzz.token_sort_ratio(query, choice)
            ), (query, choice)


def test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on():
    """The word sort splits on exactly the whitespace the scorer splits on.

    The scorer's whitespace depends on the string's WIDTH: below U+0100 it does not split on
    U+0085 or U+00A0. Covered across Python's three string widths and every code point below U+3100.
    """
    from rapidfuzz import fuzz

    points = {cp for cp in range(0x110000) if chr(cp).isspace()}
    points |= {0x85, 0xA0, 0x1F} | set(range(0x3100))
    points -= set(range(0xD800, 0xE000))
    for widen in ("", " \xe9", " Ā", " \U0001f600"):
        for cp in sorted(points):
            c = chr(cp)
            for token, other in (
                (f"zz{c}aa{widen}", f"aa zz{widen}"), (f"{c}{widen}", ""),
                (f"b{c}{c}a{widen}", f"a b{widen}"), (f"b{c}a{widen}", "a b"),
            ):
                assert fuzz.ratio(match._sorted_words(token), match._sorted_words(other)) == (
                    fuzz.token_sort_ratio(token, other)
                ), (hex(cp), widen)
    assert match._sorted_words("b\xa0a") == "b\xa0a", "a narrow string keeps its no-break space"
    assert match._sorted_words("b\xa0a Ā") == "a b Ā", "a wide one splits on it"
        # The boundary: U+00FF is the widest narrow character and U+0100 the narrowest wide
        # one, so a width test one off either way is caught.
    for edge in ("\xff", "Ā"):
        for c in ("\x85", "\xa0"):
            token, other = f"z{c}a{edge}", f"a{edge} z"
            assert fuzz.ratio(match._sorted_words(token), match._sorted_words(other)) == (
                fuzz.token_sort_ratio(token, other)
            ), (hex(ord(edge)), hex(ord(c)))


def test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call(monkeypatch):
    """R recordings and W rows cost R + W sorts, and a new index pays its own R.

    The sort was paid once per PAIR inside the scorer; the count proves the saving, since no
    wall clock threshold is asserted.
    """
    calls: list[str] = []
    real = match._sorted_words

    def counted(token: str) -> str:
        calls.append(token)
        return real(token)

    monkeypatch.setattr(match, "_sorted_words", counted)
    monkeypatch.setattr(match_library, "_sorted_words", counted)
    index, rows = _u265_library(11)
    recordings = len(index.by_recording)
    for wanted in rows:
        match._approximate(wanted, index, limit=match.APPROXIMATE_LIMIT)
    assert len(calls) == recordings + len(rows)

    calls.clear()
    again, _rows = _u265_library(12)
    match._approximate(rows[0], again, limit=match.APPROXIMATE_LIMIT)
    assert len(calls) == len(again.by_recording) + 1

    calls.clear()
    assert match._approximate(rows[0], match.LibraryIndex(by_recording={}), limit=None) == ()
    assert calls == [], "an empty index sorts nothing and asks the scorer nothing"


# ── U286: the artist agreeing is necessary for an approximate offer, never sufficient ──
# With a short title a shared artist carried an unrelated song over the discovery floor
# (Monkey Safari, Joy against Monkey Safari, Goodbye scored 84.2 and was held for review).

#: The card's five pairs, each a short wanted title against an unrelated held one by the
#: same artist, every one over the discovery floor.
U286_UNRELATED = (
    ("Monkey Safari", "Joy", "Goodbye"), ("Paul Deep (AR)", "Rea", "Tique"),
    ("Hot Since 82", "Wow", "Wild"), ("Alex Kaminski", "Mana", "Nebula"),
    ("Traumer", "Get Out", "Agenou"),
)


def _discovery_score(wanted_artist, wanted_title, held_artist, held_title):
    """The shipped discovery score, computed rather than remembered."""
    from rapidfuzz import fuzz

    return fuzz.token_sort_ratio(
        match.recording_token(wanted_artist, wanted_title),
        match.recording_token(held_artist, held_title),
    )


@pytest.mark.parametrize(("artist", "wanted", "held"), U286_UNRELATED)
def test_a_short_title_sharing_nothing_with_the_held_one_settles_missing(
    music, artist, wanted, held
):
    """Each pair clears the discovery floor, so it reaches the title test, which drops it: the
    row reads missing and the pass downloads it."""
    assert _discovery_score(artist, wanted, artist, held) >= match.APPROXIMATE_FLOOR, (
        "the pair no longer clears the discovery floor, so it no longer tests the title"
    )
    hold(music, f"08A - 124 - {artist} - {held}")
    found = resolve([one(artist=artist, title=wanted)], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING
    assert found.why is match.Why.NOT_IN_LIBRARY
    assert found.candidates == ()
    assert found.acquisitions, "a missing row with nothing to acquire downloads nothing"


def test_joy_against_goodbye_is_downloaded_through_the_real_verb(cfg, music, tmp_path):
    """The sitting's own row, through ``match run``: missing, not offered."""
    hold(music, "07A - 124 - Monkey Safari - Goodbye")
    path = write_list(tmp_path, "Monkey Safari - Joy\n", "joy.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["data"]["needs_review"] == []
    (missing,) = envelope["data"]["missing"]
    assert missing["why"] == str(match.Why.NOT_IN_LIBRARY)


#: Real near matches, each still offered: (wanted title, held title).
U286_NEAR = (
    ("Midnight Harbour Lights", "Midnight Harbor Lights"),  # one letter dropped
    ("Midnight Harbour Lights", "Midnight Harbour Light"),  # one letter at the end
    ("Midnight Harbour Lights", "Midnight Harbour Lighte"),  # one letter changed
    ("Midnight Harbour Lights", "Midnight Lights"),  # a word dropped
    ("Lights Midnight", "Midnight Lights"),  # the words reordered
    ("Sun Path", "Sun Pathx"),  # the module's own near miss
    ("Sun Path", "Sun Path Alt"),  # the module's own near miss
    ("Joy", "Jay"),  # one letter changed in a three letter title
    ("Joy", "Joys"),  # one letter added to a three letter title
        # The words split or joined: ``fold`` turns a dot into a space, so these share no word,
        # score on letters alone under the floor, and were read missing.
    ("OK", "O.K."),
    ("DNA", "D.N.A."),
    ("Good Bye", "Goodbye"),
    ("Every Day", "Everyday"),
    ("Hi Fi", "HiFi"),
)


@pytest.mark.parametrize(("wanted", "held"), U286_NEAR)
def test_a_real_near_match_is_still_offered(music, wanted, held):
    assert _discovery_score("Aurora Bloom", wanted, "Aurora Bloom", held) >= (
        match.APPROXIMATE_FLOOR
    ), "the pair no longer clears the discovery floor, so it tests nothing here"
    hold(music, f"08A - 124 - Aurora Bloom - {held}")
    found = resolve([one(title=wanted)], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [candidate.title for candidate in found.candidates] == [held]


def test_an_unrelated_title_by_another_artist_is_still_not_offered(music):
    hold(music, "08A - 124 - Nova Reef - Goodbye")
    hold(music, "08A - 124 - Nova Reef - Joy")
    found = resolve([one(artist="Monkey Safari", title="Joy")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING


def test_of_two_near_hits_only_the_one_whose_title_resembles_is_offered(music):
    """Filtered before the candidates are built: the failing recording is held as five versions,
    so a filter applied after would build six and report one withheld beside an offer of five."""
    hold(music, "08A - 124 - Aurora Bloom - Joys")
    for number, version in enumerate(("A", "B", "C", "D", "E"), start=1):
        hold(music, f"0{number}A - 124 - Aurora Bloom - Goodbye (Mix {version})")
    near = match._approximate(one(title="Joy"), index_of(music), limit=None)
    assert {held.title for held in near} == {"Joys", "Goodbye"}, (
        "discovery no longer returns both, so the filter is not being tested"
    )
    found = resolve([one(title="Joy")], index_of(music)).matches[0]
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [candidate.title for candidate in found.candidates] == ["Joys"]
    assert found.withheld == 0


def test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out(music):
    """Filtered before the cap, not after it.

    Six unrelated three letter titles by the same artist each outscore the real near match, so
    filtered after the cap the row would read missing and download a record the library holds.
    """
    unrelated = ("Box", "Cox", "Fox", "Lox", "Pox", "Sox")
    for title in unrelated:
        hold(music, f"08A - 124 - Aurora Bloom - {title}")
    hold(music, "08A - 124 - Aurora Bloom Band - Joy")
    near_score = _discovery_score("Aurora Bloom", "Joy", "Aurora Bloom Band", "Joy")
    assert all(
        _discovery_score("Aurora Bloom", "Joy", "Aurora Bloom", title) > near_score
        for title in unrelated
    ), "the unrelated titles no longer outscore the near match"
    assert len(unrelated) > match.APPROXIMATE_LIMIT
    found = resolve([one(title="Joy")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert [(c.artist, c.title) for c in found.candidates] == [("Aurora Bloom Band", "Joy")]


def test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered(music):
    """The word sort reads a swapped listing as one string at 100 and it is the same record, so
    the title test lets each half stand for the other."""
    hold(music, "08A - 124 - Sun Path - Aurora Bloom")
    found = resolve([one()], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [(c.artist, c.title) for c in found.candidates] == [("Sun Path", "Aurora Bloom")]


def test_a_swap_is_offered_only_when_both_halves_cross():
    """One half crossing is not a swap: the title has to resemble the held artist AND the artist
    the held title."""
    held = match.Owned(path=Path("x.flac"), artist="Sun Path", title="Tide Line", version="", key=None)
    assert not match._title_resembles(one(), held)
    held = match.Owned(path=Path("x.flac"), artist="Nova Reef", title="Aurora Bloom", version="", key=None)
    assert not match._title_resembles(one(), held)


def _index_of_owned(*held: match.Owned) -> match.LibraryIndex:
    grouped: dict[str, list[match.Owned]] = {}
    for owned in held:
        grouped.setdefault(owned.recording, []).append(owned)
    return match.LibraryIndex(by_recording={k: tuple(v) for k, v in grouped.items()})


#: An artist long enough that a title of one short word, or none, still clears the discovery
#: floor, so a title that folds to nothing reaches the title test.
LONG_ARTIST = "Aurora Bloom and the Harbour Lights Orchestra"


@pytest.mark.parametrize(("wanted", "held"), [("!!!", "Sun"), ("Sun", "!!!")])
def test_a_title_that_folds_to_nothing_is_offered_as_before(wanted, held):
    """A title with no letter or digit cannot be read, so the discovery score decides as before
    U286; read as sharing nothing it would download a record the library may hold."""
    owned = match.Owned(path=Path("x.flac"), artist=LONG_ARTIST, title=held, version="", key=None)
    index = _index_of_owned(owned)
    asked = one(artist=LONG_ARTIST, title=wanted)
    assert match._approximate(asked, index, limit=None) == (owned,), (
        "the pair no longer clears the discovery floor, so it tests nothing here"
    )
    found = resolve([asked], index).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [c.title for c in found.candidates] == [held]


def test_a_one_letter_title_is_judged_by_the_same_rule(music):
    """No special case offers everything by the artist to a one letter title: A against B settles
    missing, A against A is owned."""
    assert _discovery_score("Aurora Bloom", "A", "Aurora Bloom", "B") >= match.APPROXIMATE_FLOOR
    hold(music, "08A - 124 - Aurora Bloom - B")
    found = resolve([one(title="A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING
    hold(music, "08A - 124 - Aurora Bloom - A")
    found = resolve([one(title="A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED


def test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about(music, tmp_path):
    """An ISRC hit on an abbreviated title (``SO`` against ``Sexual Obsession``) is still asked.

    It scores far under the discovery floor, so it never came from the scored pass, and the ISRC
    branch that asks it is untouched by the title test.
    """
    assert _discovery_score("Stefan Ringer", "SO", "Stefan Ringer", "Sexual Obsession") < (
        match.APPROXIMATE_FLOOR
    )
    credited(
        music, tmp_path, "05A - 122 - Stefan Ringer - Sexual Obsession",
        artist="Stefan Ringer", title="05A - 122 - Sexual Obsession", isrc="USNRS2644599",
    )
    found = resolve(
        [row(artist="Stefan Ringer", title="SO", isrc="USNRS2644599")], index_of(music)
    ).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE


#: The two title pairs either side of the title floor, scores computed below: ``Burning
#: Sunlight`` against ``Morning Starlight Rising`` scores 65.0 and ``Joy`` against ``Jay`` 66.67,
#: the lowest a single changed letter gives a title of three letters or more. 66 is the one
#: integer floor between them.
TITLE_FLOOR_NEIGHBOURS = (("Burning Sunlight", "Morning Starlight Rising"), ("Joy", "Jay"))


def test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way():
    from rapidfuzz import fuzz

    below, above = (
        fuzz.token_set_ratio(match.fold(asked), match.fold(held))
        for asked, held in TITLE_FLOOR_NEIGHBOURS
    )
    assert below < match.APPROXIMATE_TITLE_FLOOR <= above, (below, above)
    assert int(above) - int(below) <= 1
    (low_asked, low_held), (high_asked, high_held) = TITLE_FLOOR_NEIGHBOURS

    def owned(title: str) -> match.Owned:
        return match.Owned(path=Path("x.flac"), artist="Aurora Bloom", title=title, version="", key=None)

    assert not match._title_resembles(one(title=low_asked), owned(low_held))
    assert match._title_resembles(one(title=high_asked), owned(high_held))
        # And the highest of the card's live pairs sits under it.
    assert fuzz.token_set_ratio("get out", "agenou") < match.APPROXIMATE_TITLE_FLOOR


@pytest.mark.parametrize("seed", [265, 2650, 26500])
def test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped(seed):
    """The reference, written apart from the code: the shipped scorer's hits over the floor, each
    kept when its title agrees (joined, ``token_set_ratio``, spelled out per card 833, or empty),
    then the first five, led by what the card 833 lookup finds that the score did not."""
    from rapidfuzz import fuzz

    listed = match_library._SPELLED_OUT

    def spelled(name):
        return "".join(listed.get(word, word) for word in name.split())

    def agree(one_name, other_name):
        joined = "".join(one_name.split())
        if joined and joined == "".join(other_name.split()):
            return True
                # Card 833: a third way to agree, the two spelled out, by equality.
        if joined and spelled(one_name) == spelled(other_name):
            return True
        return fuzz.token_set_ratio(one_name, other_name) >= match.APPROXIMATE_TITLE_FLOOR

    def looked_up(wanted, groups, offered):
        """Card 833's lookup, written apart: every recording by the row's folded artist whose title
        spelled out is the row's, one title holding a listed word, that the five do not hold, in
        token order."""
        artist, title = match.fold(wanted.artist), match.fold(wanted.title)
        asks = any(word in listed for word in title.split())
        return [
            group
            for group in sorted(groups, key=lambda g: g[0].recording)
            if match.fold(group[0].artist) == artist
            and spelled(match.fold(group[0].title)) == spelled(title)
            and (asks or any(word in listed for word in match.fold(group[0].title).split()))
            and group[0].recording not in offered
        ]

    def passes(wanted, held):
        asked, found = match.fold(wanted.title), match.fold(held.title)
        if not asked or not found:
            return True
        if agree(asked, found):
            return True
        crossed = agree(asked, match.fold(held.artist))
        return crossed and agree(match.fold(wanted.artist), found)

    def by_recording(rows):
        grouped: dict[str, list[match.Owned]] = {}
        for held in rows:
            grouped.setdefault(held.recording, []).append(held)
        return list(grouped.values())

    generated, rows = _u265_library(seed)
        # The card's shape beside U265's: short titles by one artist, related and not, so rows
        # drop hits and a drop makes room for a hit past the five.
    short = ("Joy", "Jay", "Joys", "Box", "Cox", "Fox", "Lox", "Pox", "Sox",
             "Wow", "Wild", "Rea", "Tique", "Mana", "Nebula", "Goodbye", "O.K.",
             "Love You", "For You", "Luv Us", "Tonight", "2 Nite", "Luv U",
             "I Love You", "Love You More", "Love You Babe", "Love You Down", "Love You So")
    held = [owned for versions in generated.by_recording.values() for owned in versions]
    held += [
        match.Owned(path=Path(f"s{n:03d}.flac"), artist=artist, title=title, version="", key=None)
        for n, (artist, title) in enumerate(
            [(a, t) for a in ("Aurora Bloom", "Nova Reef") for t in short]
            + [("Aurora Bloom Band", "Joy"), ("Nova Reef Band", "Wow")]
        )
    ]
    index = _index_of_owned(*held)
    rows = rows + [
        one(artist=artist, title=title)
        for artist in ("Aurora Bloom", "Nova Reef")
        for title in (
            "Joy", "Wow", "Mana", "Rea", "Get Out", "A", "OK", "Good Bye",
            "Luv U", "4 U", "Love You", "Tonite",
        )
    ]
    every_recording = by_recording(held)
    unchanged = dropped = refilled = joined = led = outranked = 0
    for wanted in rows:
        every = by_recording(_shipped_approximate(wanted, index, limit=None))
        five = [group for group in every if passes(wanted, group[0])][: match.APPROXIMATE_LIMIT]
        first = looked_up(wanted, every_recording, {group[0].recording for group in five})
        led += bool(first)
        outranked += any(group in every for group in first)
        kept = first + five
        expected = tuple(held for group in kept for held in group)
        assert match._resembling(wanted, index) == expected, wanted.recording
        joined += any(
            "".join(match.fold(wanted.title).split()) == "".join(match.fold(g[0].title).split())
            and match.fold(wanted.title) != match.fold(g[0].title)
            for g in kept
        )

        shipped = by_recording(_shipped_approximate(wanted, index))
        if not first and all(passes(wanted, group[0]) for group in shipped):
            assert match._resembling(wanted, index) == _shipped_approximate(wanted, index)
            unchanged += bool(shipped)
        else:
            dropped += 1
            refilled += len(kept) > len([g for g in shipped if passes(wanted, g[0])])
    assert unchanged and dropped and refilled and joined and led and outranked, (
        unchanged, dropped, refilled, joined, led, outranked
    )


def test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio():
    """``Get Out`` against ``Agenou`` with the spaces taken out scores 66.67, over the title floor,
    so the joined form is compared for equality only: a ratio would let the card's unrelated
    pair back in."""
    from rapidfuzz import fuzz

    assert fuzz.ratio("getout", "agenou") >= match.APPROXIMATE_TITLE_FLOOR
    agenou = match.Owned(path=Path("x.flac"), artist="Traumer", title="Agenou", version="", key=None)
    assert not match._title_resembles(one(artist="Traumer", title="Get Out"), agenou)
    goodbye = match.Owned(path=Path("x.flac"), artist="Traumer", title="Goodbye", version="", key=None)
    assert match._title_resembles(one(artist="Traumer", title="Good Bye"), goodbye)


@pytest.mark.parametrize(
    ("held", "listed"),
    [
        ("Aurora Bloom - OK", "O.K. - Aurora Bloom"),
        ("Aurora Bloom - Goodbye", "Good Bye - Aurora Bloom"),
        ("Aurora Bloom - Every Day", "Everyday - Aurora Bloom"),
        ("M.I.A. - Paper Planes", "Paper Planes - MIA"),
    ],
)
def test_a_swapped_listing_split_differently_is_still_offered(cfg, music, tmp_path, held, listed):
    """A swapped listing split differently is still offered: each crossed half gets the same
    equality the titles do."""
    hold(music, f"08A - 124 - {held}")
    path = write_list(tmp_path, f"{listed}\n", "swapped.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    (row,) = envelope["data"]["needs_review"]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)


# ── Card 833: a title spelled in slang or numerals is offered as the possible copy it is ──
# ``Luv U`` against a held ``Love You``, by one artist, is never read missing and never called
# owned. A short curated word list is read only when two titles are compared (2026-11-15).

#: (artist, slang spelling, spelled out), each the same title by one artist. Monkey Safari
#: clears the discovery floor with ``Luv U`` and ``4 U``; Prince and Aurora Bloom do not, so
#: they reach the offer through the spelled out lookup alone.
SPELLED_PAIRS = (
    ("Monkey Safari", "Luv U", "Love You"), ("Monkey Safari", "4 U", "For You"),
    ("Prince", "Luv U", "Love You"), ("Prince", "4 U", "For You"),
    ("Aurora Bloom", "4 U", "For You"), ("Prince", "I Would Die 4 U", "I Would Die For You"),
    ("Aurora Bloom", "I Would Die 4 U", "I Would Die For You"),
    ("Aurora Bloom", "2 Nite", "Tonight"), ("Monkey Safari", "2 Nite", "Tonight"),
    ("Aurora Bloom", "4Ever", "Forever"), ("Aurora Bloom", "B4 U Go", "Before You Go"),
    ("Aurora Bloom", "Luv U 2", "Love You Too"), ("Aurora Bloom", "U", "You"),
)


@pytest.mark.parametrize("reverse", [False, True], ids=["slang-wanted", "slang-held"])
@pytest.mark.parametrize(("artist", "slang", "spelled"), SPELLED_PAIRS)
def test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy(
    music, artist, slang, spelled, reverse
):
    """The card's goal, both ways round: offered for review as a resemblance, with the held file
    as the one candidate, never matched and never missing."""
    asked, held = (spelled, slang) if reverse else (slang, spelled)
    hold(music, f"08A - 124 - {artist} - {held}")
    found = resolve([one(artist=artist, title=asked)], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [(c.artist, c.title) for c in found.candidates] == [(artist, held)]
    assert found.paths == (), "a spelled out reading is a question, never ownership"
    assert found.acquisitions == ()


def test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score():
    """Two of the card's pairs score under the discovery floor for a short artist, so the spelled
    out lookup beside the score is what offers them. Scores computed, not remembered."""
    for artist, slang, spelled in (("Prince", "4 U", "For You"), ("Prince", "Luv U", "Love You")):
        assert _discovery_score(artist, slang, artist, spelled) < match.APPROXIMATE_FLOOR
        held = match.Owned(path=Path("x.flac"), artist=artist, title=spelled, version="", key=None)
        index = _index_of_owned(held)
        asked = one(artist=artist, title=slang)
        assert match._approximate(asked, index, limit=None) == ()
        assert match._resembling(asked, index) == (held,)


def test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded(cfg, music, tmp_path):
    hold(music, "08A - 124 - Prince - For You")
    path = write_list(tmp_path, "Prince - 4 U\n", "slang.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert envelope["data"]["missing"] == []
    (asked,) = envelope["data"]["needs_review"]
    assert asked["why"] == str(match.Why.TITLE_APPROXIMATE)


def test_the_slang_title_itself_held_is_owned_and_the_spelled_out_one_is_not_offered(music):
    """Nothing new is owned, and the exact branch still comes first: holding both spellings, the
    row is matched to its own spelling only."""
    own = hold(music, "08A - 124 - Prince - 4 U")
    hold(music, "08A - 124 - Prince - For You")
    found = resolve([one(artist="Prince", title="4 U")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.paths == (str(own),)


def test_a_spelled_out_copy_by_another_artist_is_not_offered(music):
    hold(music, "08A - 124 - Nova Reef - For You")
    found = resolve([one(artist="Prince", title="4 U")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING


#: Pairs that must still read missing, each over the discovery floor for :data:`LONG_ARTIST`
#: so the title test decides: a word the list lacks (``Wot``, ``Cos``), and a listed word
#: whose spelled out form is merely CLOSE to an unrelated title, which is why the reading is
#: compared by equality (``2`` against ``Tom`` would score 80 by ratio).
STILL_MISSING = (
    ("Wot", "What"), ("Cos", "Because"), ("2", "Tom"), ("4", "Fort"), ("N", "Ant"), ("B", "Bee"),
    ("U", "Yo"), ("Luv", "Lover"),
)


@pytest.mark.parametrize(("wanted", "held"), STILL_MISSING)
def test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing(wanted, held):
    owned = match.Owned(path=Path("x.flac"), artist=LONG_ARTIST, title=held, version="", key=None)
    index = _index_of_owned(owned)
    asked = one(artist=LONG_ARTIST, title=wanted)
    assert match._approximate(asked, index, limit=None) == (owned,), (
        "the pair no longer clears the discovery floor, so it tests nothing here"
    )
    found = resolve([asked], index).matches[0]
    assert found.state is match.MatchState.MISSING


def test_a_title_split_differently_is_still_kept_when_its_spelled_out_reading_is_not():
    """Monotone: the reading is a third way to agree, never a replacement. ``U Turn`` spelled out
    is no longer one string with ``UTurn``, but they still agree by U286's equality."""
    assert match._agree("u turn", "uturn")
    assert match._agree("n joy", "njoy")


def test_the_lookup_does_not_widen_a_title_split_differently():
    """The lookup reads a pair only when one title holds a listed word, so ``OK`` against ``O.K.``,
    U286's class, is offered by the score exactly where it was and never by the lookup."""
    held = match.Owned(path=Path("x.flac"), artist="Prince", title="O.K.", version="", key=None)
    index = _index_of_owned(held)
    assert index.spelled_alike(match.recording_token("Prince", "OK")) == ()
    assert index.spelled_alike(match.recording_token("Prince", "K.O.")) == ()


def test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads(music):
    """Order: a recording discovery scored and the lookup also finds keeps its scored place, and one
    only the lookup finds is put first, as the same title under the reading."""
    hold(music, "08A - 124 - Monkey Safari - Love You")
    hold(music, "08A - 124 - Monkey Safari - Luv Us")
    found = resolve([one(artist="Monkey Safari", title="Luv U")], index_of(music)).matches[0]
    near = match._approximate(one(artist="Monkey Safari", title="Luv U"), index_of(music), limit=None)
    assert [held.title for held in near][0] == "Luv Us"
    assert [c.title for c in found.candidates] == [held.title for held in near]

    hold(music, "08A - 124 - Prince - Luv Us")
    hold(music, "08A - 124 - Prince - Love You")
    found = resolve([one(artist="Prince", title="Luv U")], index_of(music)).matches[0]
    assert [c.title for c in found.candidates] == ["Love You", "Luv Us"]


def test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so(music):
    """A lookup hit pushing a scored one out of the offer says so: the offer shows five and the one
    it drops is counted as withheld."""
    for title in ("Luv Ua", "Luv Ub", "Luv Uc", "Luv Ud", "Luv Ue", "Luv Uf"):
        hold(music, f"08A - 124 - Prince - {title}")
    hold(music, "08A - 124 - Prince - Love You")
    asked = one(artist="Prince", title="Luv U")
    assert len(match._approximate(asked, index_of(music), limit=None)) == 6, (
        "the six near titles no longer clear the discovery floor"
    )
    found = resolve([asked], index_of(music)).matches[0]
    assert len(found.candidates) == match.APPROXIMATE_LIMIT
    assert found.withheld == 1, "five scored plus one looked up, five shown"
    assert found.candidates[0].title == "Love You"


#: The curated list as the card's decision names it, written here and not read from the code,
#: so an entry dropped there fails a case here.
SPELLINGS = (
    ("u", "you"), ("ur", "your"), ("luv", "love"), ("4", "for"), ("2", "to"), ("too", "to"),
    ("n", "and"), ("r", "are"), ("b", "be"), ("c", "see"), ("y", "why"), ("thru", "through"),
    ("tho", "though"), ("nite", "night"), ("tonite", "tonight"), ("2nite", "tonight"),
    ("2day", "today"), ("2morrow", "tomorrow"), ("4ever", "forever"), ("b4", "before"),
    ("cuz", "because"), ("coz", "because"), ("lil", "little"), ("gr8", "great"), ("l8r", "later"),
)


@pytest.mark.parametrize(("word", "spelled"), SPELLINGS)
def test_every_listed_spelling_offers_its_spelled_out_title(word, spelled):
    """Each entry driven on its own, both ways round, for an artist short enough that the discovery
    score cannot reach the pair, so a dropped entry fails here."""
    artist = "Moby"
    for asked, held_title in ((word, spelled), (spelled, word)):
        held = match.Owned(path=Path("x.flac"), artist=artist, title=held_title, version="", key=None)
        found = resolve([one(artist=artist, title=asked)], _index_of_owned(held)).matches[0]
        assert found.state is match.MatchState.NEEDS_REVIEW, (asked, held_title)
        assert [c.title for c in found.candidates] == [held_title]


def test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out():
    """``Lil Kid`` and ``Little Kid`` are two artists: only the title is read spelled out."""
    held = match.Owned(path=Path("x.flac"), artist="Little Kid", title="For You", version="", key=None)
    found = resolve([one(artist="Lil Kid", title="4 U")], _index_of_owned(held)).matches[0]
    assert found.state is match.MatchState.MISSING


@pytest.mark.parametrize(("wanted", "held"), [("Two Day", "Today"), ("Four Tune", "Fortune")])
def test_a_spelled_number_is_not_read_as_a_numeral(wanted, held):
    """With ``two`` and ``four`` read as ``to`` and ``for`` and the spaces gone, two unrelated
    titles became one. Neither is listed."""
    owned = match.Owned(path=Path("x.flac"), artist="Moby", title=held, version="", key=None)
    found = resolve([one(artist="Moby", title=wanted)], _index_of_owned(owned)).matches[0]
    assert found.state is match.MatchState.MISSING


def test_a_lookup_hit_discovery_ranked_past_the_five_still_leads(cfg, music, tmp_path):
    """A lookup hit discovery ranked past the five still leads: ``Luv U`` discovered sixth would be
    cut by the cap and never offered or counted."""
    for title in ("I Love You", "Love You More", "Love You Babe", "Love You Down", "Love You So"):
        hold(music, f"08A - 124 - Aurora Bloom - {title}")
    hold(music, "08A - 124 - Aurora Bloom - Luv U")
    asked = one(title="Love You")
    near = [held.title for held in match._approximate(asked, index_of(music), limit=None)]
    assert near.index("Luv U") >= match.APPROXIMATE_LIMIT, near
    found = resolve([asked], index_of(music)).matches[0]
    assert found.candidates[0].title == "Luv U"
    assert len(found.candidates) == match.APPROXIMATE_LIMIT
    assert found.withheld == 1
    path = write_list(tmp_path, "Aurora Bloom - Love You\n", "ranked.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    (row,) = envelope["data"]["needs_review"]
    assert row["candidates"][0]["title"] == "Luv U"


def test_the_word_list_is_the_curated_one():
    assert dict(SPELLINGS) == dict(match_library._SPELLED_OUT)


def test_the_word_list_maps_no_word_to_itself_and_only_folded_words():
    """A key is one folded word, so the lookup finds it after :func:`fold`; a value is what the key
    stands for, folded, and never the key itself."""
    for word, spelled in match_library._SPELLED_OUT.items():
        assert word == match.fold(word) and " " not in word, word
        assert spelled == match.fold(spelled) and spelled != word, word


def _old_agree(one_name: str, other_name: str) -> bool:
    """U286's ``_agree`` as it shipped, written apart from the code."""
    from rapidfuzz import fuzz

    if one_name and one_name.replace(" ", "") == other_name.replace(" ", ""):
        return True
    return fuzz.token_set_ratio(one_name, other_name) >= match.APPROXIMATE_TITLE_FLOOR


def test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair():
    """The differential: over every pair of a corpus of titles, whatever agreed still agrees, a pair
    holding no listed word agrees exactly as before, and every pair that newly agrees is one
    string with the spaces gone once each listed word is spelled out."""
    listed = match_library._SPELLED_OUT

    def spelled(name: str) -> str:
        return "".join(listed.get(word, word) for word in name.split())

    corpus = {match.fold(t) for pair in U286_NEAR for t in pair}
    corpus |= {match.fold(t) for _a, *titles in U286_UNRELATED for t in titles}
    corpus |= {match.fold(t) for _a, *titles in SPELLED_PAIRS for t in titles}
    corpus |= {match.fold(t) for pair in STILL_MISSING for t in pair}
    corpus |= {match.fold(t) for pair in TITLE_FLOOR_NEIGHBOURS for t in pair}
    corpus |= {match.fold(w) for w in _U265_WORDS}
    corpus |= {match.fold(w) for w in list(listed) + list(listed.values())}
    corpus.discard("")
    added = 0
    for one_name in sorted(corpus):
        for other_name in sorted(corpus):
            before, now = _old_agree(one_name, other_name), match._agree(one_name, other_name)
            if before:
                assert now, (one_name, other_name)
            holds = any(w in listed for w in (one_name + " " + other_name).split())
            if not holds:
                assert now == before, (one_name, other_name)
            if now and not before:
                assert holds and spelled(one_name) == spelled(other_name), (one_name, other_name)
                added += 1
    assert added, "no pair in the corpus exercises the reading"


# ── A title that folds to nothing is told apart by its own text (card 834) ───────


#: Two titles of emoji alone by one artist, which ``fold`` takes to nothing.
FIRE, DROP, SNOW = "\U0001f525", "\U0001f4a7", "❄"


def test_two_different_emoji_titles_by_one_artist_are_not_one_recording(music):
    """The card's own pair: ``fold`` takes both titles to nothing, so the exact branch called the
    wanted ``💧`` owned by the held ``🔥``. It is now asked, never matched."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert found.state is not match.MatchState.MATCHED
    assert found.paths == ()
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [c.title for c in found.candidates] == [FIRE]


def test_two_different_emoji_titles_through_the_real_verb_are_not_owned(cfg, music, tmp_path):
    """The residual's own drive, a text list through ``match run``: not matched, so the row
    reaches a person and is never silently skipped."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    path = write_list(tmp_path, f"Aurora Bloom - {DROP}\n", "emoji.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert envelope["data"]["matched"] == []
    (row,) = envelope["data"]["needs_review"]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)


def test_the_same_emoji_title_by_one_artist_is_still_owned(music):
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    found = resolve([one(title=FIRE)], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.why is match.Why.EXACT
    assert [Path(p).name for p in found.paths] == [f"08A - 124 - Aurora Bloom - {FIRE}.flac"]


def test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds(music):
    """Both files sit under one recording token. Only the one the row names is the match, and its
    path alone is reported."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    hold(music, f"08A - 124 - Aurora Bloom - {DROP}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert [Path(p).name for p in found.paths] == [f"08A - 124 - Aurora Bloom - {DROP}.flac"]


@pytest.mark.parametrize(
    ("wanted", "held"),
    [
        ("!!!", "!!!"),
        ("!!!", "！！！"),  # fullwidth marks, one title at another width
        ("❤", "❤️"),  # the emoji presentation selector
        ("❤︎", "❤️"),  # text and emoji presentation
        ("? ?", "??"),  # spacing
        ("...", "…"),  # an ellipsis, one character or three
        ("\U0001f468‍\U0001f467", "\U0001f468\U0001f467"),  # a zero width joiner
        ("​" + FIRE, FIRE),  # a zero width space
        ("", ""),
    ],
    ids=["marks", "width", "selector", "text-and-emoji", "spacing", "ellipsis", "joiner",
         "zero-width-space", "empty"],
)
def test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned(wanted, held):
    """One title written two ways by two sources is one recording, so the bare text drops width,
    case, spacing and invisible characters. A real duplicate must not download again."""
    owned = match.Owned(path=Path("x.flac"), artist="Aurora Bloom", title=held, version="", key=None)
    assert match.same_title(wanted, held)
    found = resolve([one(title=wanted)], _index_of_owned(owned)).matches[0]
    assert found.state is match.MatchState.MATCHED, found.why


@pytest.mark.parametrize(
    ("wanted", "held"),
    [
        (DROP, FIRE),
        ("!!!", "???"),
        ("!!!", "!!"),
        ("\U0001f44d", "\U0001f44d\U0001f3fd"),  # a skin tone is a visible difference
        (FIRE, ""),
        ("❤", "♥"),  # two hearts, two code points
    ],
)
def test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title(wanted, held):
    owned = match.Owned(path=Path("x.flac"), artist="Aurora Bloom", title=held, version="", key=None)
    assert not match.same_title(wanted, held)
    found = resolve([one(title=wanted)], _index_of_owned(owned)).matches[0]
    assert found.state is not match.MatchState.MATCHED
    assert found.paths == ()


def test_two_held_emoji_titles_are_offered_as_two_candidates(music):
    """Grouped by the recording token alone they were one candidate titled by whichever file came
    first and carrying both paths, so accepting it accepted a file never shown."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    hold(music, f"08A - 124 - Aurora Bloom - {SNOW}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert sorted(c.title for c in found.candidates) == sorted([FIRE, SNOW])
    assert all(len(c.paths) == 1 for c in found.candidates)
    assert len({c.candidate_id for c in found.candidates}) == 2


def test_a_candidate_whose_title_folds_to_something_keeps_its_identifier(music):
    """The identifier a recorded answer names is unchanged for every title that folds to something:
    the bare title joins the digest only when it is not empty."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve([one()], index_of(music)).matches[0]
    (candidate,) = found.candidates
    expected = match._digest(
        match.recording_token("Aurora Bloom", "Sun Path"), "extended mix", "08A"
    )
    assert candidate.candidate_id == f"cd_{expected}"


def test_an_emoji_titles_identities_are_its_own():
    """Two titles of emoji alone by one artist are two recordings to every identity hashed from one:
    the review item, the match identifier and the search option. The token the index is keyed by
    and the tombstone identity are unchanged."""
    drop, fire = one(title=DROP), one(title=FIRE)
    assert drop.recording == fire.recording == "aurora bloom\x1f"
    assert drop.distinct == f"aurora bloom\x1f\x1f{DROP}"
    assert drop.distinct != fire.distinct
    assert drop.identity == {"artist": "aurora bloom", "title": DROP}

    def ids(wanted):
        found = match.TrackMatch(
            wanted=wanted, state=match.MatchState.MISSING, why=match.Why.NOT_IN_LIBRARY,
            acquisitions=match.acquisition_options(wanted),
        )
        asked = match.question_identity(
            wanted.artist, wanted.title, "", None, match.Why.TITLE_APPROXIMATE
        )
        return found.match_id, sorted(asked.items()), [a.option_id for a in found.acquisitions]

    for left, right in zip(ids(drop), ids(fire), strict=True):
        assert left != right


#: Titles that fold to something, with the identities they had before this card, computed
#: from the token so a change to any of them fails here.
@pytest.mark.parametrize("title", ["Sun Path", "O.K.", "Sun \U0001f525", "Beyoncé", ""])
def test_a_title_that_folds_to_something_keeps_every_identity(title):
    wanted = one(title=title)
    token = match.recording_token("Aurora Bloom", title)
    assert wanted.distinct == token
    found = match.TrackMatch(
        wanted=wanted, state=match.MatchState.MISSING, why=match.Why.NOT_IN_LIBRARY,
        acquisitions=match.acquisition_options(wanted),
    )
    assert found.match_id == f"mt_{match._digest(token, '', '')}"
    assert [a.option_id for a in found.acquisitions] == [
        f"aq_{match._digest(match.BY_SEARCH, token, '')}"
    ]
    asked = match.question_identity("Aurora Bloom", title, "", None, match.Why.TITLE_APPROXIMATE)
    assert asked["recording"] == token


def test_a_held_emoji_row_does_not_retire_another_emoji_rows_question(cfg, music, tmp_path):
    """A held emoji row does not retire another emoji row's question: they shared an identity, so
    the ``💧`` question was superseded every run and could not be answered."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    path = write_list(tmp_path, f"Aurora Bloom - {DROP}\nAurora Bloom - {FIRE}\n", "both.txt")
    for _run in range(2):
        code, envelope = drive(["match", "run", path])
        assert code == int(ExitCode.PENDING_HUMAN)
        (asked,) = envelope["data"]["needs_review"]
        assert asked["title"] == DROP
    _code, listed = drive(["review", "list"])
    assert [item["id"] for item in listed["data"]["items"]] == [asked["review_item"]]
    code, _ = drive(["review", "resolve", asked["review_item"], "--verdict", "rejected"])
    assert code == int(ExitCode.OK)
    _code, after = drive(["match", "run", path])
    assert [row["title"] for row in after["data"]["missing"]] == [DROP]


def test_an_answer_about_one_emoji_title_does_not_settle_another(cfg, music, tmp_path):
    """The item was keyed on the token, so accepting ``❤`` for a listed ``♥`` called a later ``💔``
    owned."""
    hold(music, "08A - 124 - Aurora Bloom - \u2764")
    first = write_list(tmp_path, "Aurora Bloom - \u2665\n", "heart.txt")
    _code, asked = drive(["match", "run", first])
    (row,) = asked["data"]["needs_review"]
    option = row["candidates"][0]["id"]
    code, _ = drive(["review", "resolve", row["review_item"], "--verdict", "accepted", "--option", option])
    assert code == int(ExitCode.OK)
    _code, again = drive(["match", "run", first])
    assert again["data"]["matched"][0]["why"] == str(match.Why.VERDICT_ACCEPTED)
    later = write_list(tmp_path, "Aurora Bloom - \U0001f494\n", "broken.txt")
    _code, other = drive(["match", "run", later])
    assert other["data"]["matched"] == []
    (open_row,) = other["data"]["needs_review"]
    assert open_row["review_item"] != row["review_item"]


def test_two_emoji_rows_in_one_list_carry_two_match_identifiers(cfg, music, tmp_path):
    """A consumer keying by the match identifier, ``intake missing``'s dedupe among them, read the
    second row as the first one listed twice."""
    path = write_list(tmp_path, f"Aurora Bloom - {FIRE}\nAurora Bloom - {DROP}\n", "two.txt")
    _code, envelope = drive(["match", "run", path])
    ids = [row["id"] for row in envelope["data"]["missing"]]
    assert len(ids) == len(set(ids)) == 2


def test_an_emoji_candidate_offered_for_another_is_named_a_resemblance(music):
    """``_same_recording`` reads the title by its identity, so the held ``🔥`` offered for a wanted
    ``💧`` says what it is, not ``exact``."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert [c.difference for c in found.candidates] == [match.Why.TITLE_APPROXIMATE]


def test_two_flags_are_two_titles():
    """The tag characters spelling a regional flag are format characters the bare text keeps, so
    England and Scotland are two titles."""
    england = "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f"
    scotland = "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f"
    assert not match.same_title(england, scotland)
    assert match.same_title(england, england)


def test_an_isrc_under_another_artist_and_another_emoji_title_is_asked(music, tmp_path):
    """The ISRC branch is the only rule that reaches a file under another artist, so a title it read
    as one would settle the row outright."""
    credited(
        music, tmp_path, "08A - 124 - Nova Reef - fire",
        artist="Nova Reef", title=f"08A - 124 - {FIRE}", isrc="USNRS2644532",
    )
    found = resolve(
        [row(artist="Aurora Bloom", title=DROP, isrc="USNRS2644532")], index_of(music)
    ).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert found.paths == ()


def test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled(music, tmp_path):
    """An ISRC agrees only with the title, and two emoji titles are two titles, so the file is
    offered as the question a differing title is."""
    credited(
        music, tmp_path, "08A - 124 - Aurora Bloom - fire",
        artist="Aurora Bloom", title=f"08A - 124 - {FIRE}", isrc="USNRS2644532",
    )
    index = index_of(music)
    asked = resolve([row(artist="Aurora Bloom", title=DROP, isrc="USNRS2644532")], index)
    (found,) = asked.matches
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    owned = resolve([row(artist="Aurora Bloom", title=FIRE, isrc="USNRS2644532")], index)
    assert owned.matches[0].why is match.Why.ISRC_EXACT


def test_the_credited_list_rule_tells_two_emoji_titles_apart(music, tmp_path):
    credited(
        music, tmp_path, "08A - 124 - Nova Reef, Aurora Bloom - fire",
        artist="Nova Reef, Aurora Bloom", title=f"08A - 124 - {FIRE}", isrc=None,
    )
    index = index_of(music)
    found = resolve([row(artist="Aurora Bloom", title=DROP, isrc=None)], index).matches[0]
    assert found.state is not match.MatchState.MATCHED
    assert found.paths == ()
    owned = resolve([row(artist="Aurora Bloom", title=FIRE, isrc=None)], index).matches[0]
    assert owned.why is match.Why.CREDITED_EXACT


#: Titles that fold to something, for the differential below: the fixtures' own, U265's
#: generated words, and the shapes ``fold`` exists for.
_FOLDED_TITLES = (
    "Sun Path", "sun path", "SUN PATH", "Sun  Path", "Sun-Path", "Sun.Path", "Sun Path!",
    "Sun Pathx", "Re Mix", "Remix", "O.K.", "OK", "Good Bye", "Goodbye", "Beyoncé",
    "Beyonce", "Ｓｕｎ", "Sun", "naïve", "naive", "straße", "STRASSE", "ﬁne", "fine",
    "東京", "Привет", "Ⅻ", "XII", "01", "1", "_", "A", "a", "Joy", "Jay", "\U0001f525 Sun",
    "Sun \U0001f525", "Sun \U0001f4a7", "1️⃣", "Ⓐ",
)


def test_a_title_that_folds_to_something_compares_exactly_as_it_did():
    """Every pair whose folds are not empty: ``same_title`` is ``fold`` equality, so no title that
    matched before stops matching and none starts."""
    for left in _FOLDED_TITLES:
        assert match.fold(left), left
        assert match.bare_title(left) == ""
        for right in _FOLDED_TITLES:
            assert match.same_title(left, right) == (match.fold(left) == match.fold(right)), (
                left, right,
            )


def test_a_title_that_folds_to_nothing_never_equals_one_that_folds_to_something():
    for left in ("", "!!!", FIRE, "❤️"):
        for right in _FOLDED_TITLES:
            assert not match.same_title(left, right)
            assert not match.same_title(right, left)


def _answer_recorded_before(cfg, music, listed: str, held: str, *, named: bool = True) -> str:
    """An acceptance as the build before this card recorded it: the emoji titled candidate under its
    former identifier, the digest of the token."""
    index = index_of(music)
    found = resolve([one(title=listed)], index).matches[0]
    (offered,) = found.candidates
    former = match._former_candidate_id(offered)
    assert former != offered.candidate_id
    detail = {**offered.to_json(), "id": former, "title": held}
    with review.open_store(cfg) as items:
        item = review.offer(
            items, queue=match_cli.QUEUE, kind=match.QUESTION_KIND,
            identity=found.question_identity, payload=found.to_json(),
            options=(review.Option(option_id=former, summary=held, detail=detail),),
        )
        review.resolve(
            items, item.item_id, review.Verdict.ACCEPTED,
            option=former if named else None, actor="test",
        )
    return former


def test_an_answer_recorded_before_naming_an_emoji_file_still_applies(cfg, music, tmp_path):
    """A file whose title folds to nothing was offered under an identifier hashed from the artist's
    empty fold, which moved, so an acceptance read as a gone candidate. It is carried over."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    _answer_recorded_before(cfg, music, "Fire", FIRE)
    path = write_list(tmp_path, "Aurora Bloom - Fire\n", "fire.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK), envelope["data"]["needs_review"]
    (row,) = envelope["data"]["matched"]
    assert row["why"] == str(match.Why.VERDICT_ACCEPTED)
    assert [Path(p).name for p in row["paths"]] == [f"08A - 124 - Aurora Bloom - {FIRE}.flac"]


def test_a_yes_recorded_before_naming_no_option_still_applies(cfg, music, tmp_path):
    """An unspecific yes is bound to the one option the item offered, which the store keeps under
    its former identifier, so that is carried too."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    _answer_recorded_before(cfg, music, "Fire", FIRE, named=False)
    path = write_list(tmp_path, "Aurora Bloom - Fire\n", "fire.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK), envelope["data"]["needs_review"]
    (row,) = envelope["data"]["matched"]
    assert row["why"] == str(match.Why.VERDICT_ACCEPTED)


def test_an_answer_recorded_before_is_not_carried_to_another_emoji_file(cfg, music, tmp_path):
    """The former identifier was every such file by the artist, so an answer
    about ``🔥`` is not carried to a ``❄`` now held in its place."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    _answer_recorded_before(cfg, music, "Fire", FIRE)
    (music / f"08A - 124 - Aurora Bloom - {FIRE}.flac").unlink()
    hold(music, f"08A - 124 - Aurora Bloom - {SNOW}")
    path = write_list(tmp_path, "Aurora Bloom - Fire\n", "fire.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert envelope["data"]["matched"] == []
    (row,) = envelope["data"]["needs_review"]
    assert row["why"] == str(match.Why.CANDIDATE_GONE)


def test_a_former_identifier_is_carried_only_with_one_fit_and_its_title():
    owned = (
        match.Owned(path=Path("a.flac"), artist="Aurora Bloom", title=FIRE, version="", key=None),
        match.Owned(path=Path("b.flac"), artist="Aurora Bloom", title=SNOW, version="", key=None),
    )
    found = resolve([one(title="Fire")], _index_of_owned(*owned)).matches[0]
    by_title = {c.title: c for c in found.candidates}
    former = match._former_candidate_id(by_title[FIRE])
    assert former == match._former_candidate_id(by_title[SNOW])
    assert match.current_option(found, former, FIRE) == by_title[FIRE].candidate_id
    assert match.current_option(found, former, SNOW) == by_title[SNOW].candidate_id
    assert match.current_option(found, former, DROP) == former
    assert match.current_option(found, former, None) == former
    current = by_title[FIRE].candidate_id
    assert match.current_option(found, current, SNOW) == current


def test_a_candidate_titled_with_letters_has_the_identifier_it_had():
    sun = match.Candidate(
        candidate_id="x", artist="Aurora Bloom", title="Sun Path", version="Extended Mix",
        key="08A", difference=match.Why.VERSION_DIFFERS, paths=("a",),
    )
    token = match.recording_token("Aurora Bloom", "Sun Path")
    assert match._former_candidate_id(sun) == f"cd_{match._digest(token, 'extended mix', '08A')}"
