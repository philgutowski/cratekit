"""U16: the three states, and the middle one that the source system has no name for.

Every test here is written against a specific way the system this replaces got
it wrong:

* it resolves a wanted track to whatever a text search returned first, so a
  remix, an extended cut and a clean edit all read as owned;
* it decides ownership from an exported document, so a library that moved since
  the export reads as a library that never held the track;
* it writes what a person has to decide into a comma separated file, so the
  decision lives for exactly as long as the directory it was written in;
* it has no concept of a version that was deliberately deleted, so a deletion
  is undone by the next sweep and nobody is told.

The file is in five parts: folding and versions, the on-disk index, resolution,
the three shapes an intake list arrives in, and the verb.
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
from cratekit.acquire import match, match_cli
from cratekit.cli import output, registry
from cratekit.core import config, naming, review, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode

# The ONE container synthesizer, borrowed rather than copied. A second one would
# be a second opinion about what a valid file is, and the tag suite's opinion is
# the one the tag reader is proven against. It lives in a helper module rather
# than in that suite, so importing it does not run another suite's top level.
from tests._containers import synth_container, tagged_container

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
MATCH_SOURCE = SRC_ROOT / "cratekit" / "acquire" / "match.py"
MATCH_CLI_SOURCE = SRC_ROOT / "cratekit" / "acquire" / "match_cli.py"
RESIDUALS_DOC = REPO_ROOT / "docs" / "residual-findings.md"


# ═══════════════════════════════════════════════════════════════════════════
# Residual citations, by title
# ═══════════════════════════════════════════════════════════════════════════
#
# A RESIDUAL NUMBER IS NOT A STABLE NAME AND THIS UNIT LEARNED IT THE EXPENSIVE
# WAY. Six numbers in the middle of the range are claimed by this branch and by
# main at once, with DIFFERENT CONTENT on each side, because two units appended
# to the same file in parallel. Every citation by number in this unit's tests
# therefore pointed at a different subject the moment either side renumbered, and
# that is a break nothing can see: the sentence still reads perfectly and cites
# the wrong finding.
#
# So every citation here names a TITLE. Titles are what the entries are about,
# they survive a renumber, and a citation that stops resolving is caught by
# ``test_every_residual_this_unit_cites_is_a_heading_that_exists`` rather than
# read past. ``test_no_residual_is_cited_by_number_anywhere_in_this_unit`` keeps
# the other spelling from coming back.
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, saved, so the real verb resolves the real paths.

    The environment variable is set as well as the file for the reason the
    review suite gives: the autouse isolation already points the library root
    somewhere, and ``from_dict`` relocates a configured root onto whatever the
    environment says, so writing only the file would leave the value under test
    and the value in force as two different directories.
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def music(cfg):
    return cfg.library.root / cfg.library.music_dir


def hold(music: Path, name: str) -> Path:
    """Put a file in the library under the naming convention, with no tags.

    An empty container is deliberate for most fixtures: the tag reader returns
    None for a file it cannot parse, so these exercise the FILENAME half of
    on-disk truth. The tag half gets a real container of its own below.
    """
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
    return match.resolve_all(
        wanted, index, suppresses=suppresses, suppression_id=no_identifier
    )


def one(*, artist="Aurora Bloom", title="Sun Path", version="", key=None, origin=match.TEXT):
    return match.Wanted(
        artist=artist, title=title, version=version, key=key, origin=origin
    )


def drive(argv: list[str]) -> tuple[int, dict]:
    """Run the real dispatcher and return (status, envelope)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue())


def write_list(tmp_path: Path, body: str, name: str = "list.txt") -> str:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return str(path)


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: folding, and what counts as a version
# ═══════════════════════════════════════════════════════════════════════════


def test_folding_keeps_word_boundaries_rather_than_deleting_punctuation():
    """A collision here merges two candidates onto one decision, silently.

    Folding punctuation away entirely would make "Re Mix" and "Remix" one token,
    and the person would be asked once about two different records. Folding it
    to a space keeps them apart while still letting a hyphen and a space agree.
    """
    assert match.fold("Re-Mix") == match.fold("Re Mix")
    assert match.fold("ReMix") != match.fold("Re Mix")
    assert match.fold("  Café  DEL  Mar ") == "cafe del mar"


def test_the_artist_and_title_cannot_be_resplit_into_a_colliding_pair():
    """The join uses a separator folding can never produce.

    Without it, artist "Sun" title "Path" and artist "Sun Path" title "" are one
    token, and two different records become one decision.
    """
    assert match.recording_token("Sun", "Path") != match.recording_token("Sun Path", "")


def test_the_original_mix_and_no_qualifier_at_all_are_one_version():
    """Otherwise a person is asked to confirm a track against itself."""
    assert match.version_token("Original Mix") == match.version_token("")
    assert match.version_token("original") == ""


def test_an_album_version_is_not_folded_away():
    """It is a real, different cut on plenty of releases.

    Folding it would silently join two versions, which is the one thing this
    unit exists to stop.
    """
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
        ("Song (Remix)", ("Song", "Remix")),
        ("Song [Remix] (Edit)", ("Song", "Remix Edit")),
        ("[]", ("", "")),
        ("[With You]", ("With You", "")),
        ("(With Or Without You)", ("With Or Without You", "")),
        ("(Without You)", ("Without You", "")),
        ("(Without You Remix)", ("", "Without You Remix")),
        ("(With Love) (Remix)", ("With Love", "Remix")),
        ("(feat. Mira)", ("feat. Mira", "")),
        ("(Extended)", ("", "Extended")),
        ("[Original Mix] (Remastered)", ("", "Original Mix Remastered")),
        ("[Premade Sandwiches Live]", ("", "Premade Sandwiches Live")),
    ],
)
def test_a_title_written_wholly_in_brackets_keeps_its_words(spelled, expected):
    """U213. A group that is all the title has left is the title, brackets dropped.

    Glass Animals' ``[Premade Sandwiches]`` walked off whole like a qualifier,
    so the row named no title and refused every playlist ``crate sync twins``
    planned. An empty group is still nothing, and a group after a title is
    still the version it always was. A first group is the title even when it
    reads like a credit, since ``with`` is a credit marker and ``[With You]``
    is a title.
    """
    assert match.split_version(spelled) == expected
    assert match.split_title(spelled) == expected


# ═══════════════════════════════════════════════════════════════════════════
# U262: a credit is a first WORD, not the first letters of a group
# ═══════════════════════════════════════════════════════════════════════════

#: Groups whose first word only BEGINS with a credit marker's letters. Each is a
#: mix name, so each is a version. The letters rule read all five as credits and
#: dropped them, so the remix resolved as the plain record, matched exact.
U262_VERSION_GROUPS: tuple[str, ...] = (
    "Without You Remix",
    "Withdrawn Mix",
    "Within Mix",
    "Feature Edit",
    "Featureless Dub",
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

    The credit test folded its prefixes, which took off the space that made
    each one a whole word, so ``with`` matched the first letters of
    ``Without`` and the whole group came off the title. The row then resolved
    matched, exact, against a library holding only the plain record: the remix
    was reported owned and never downloaded, and nobody was asked.
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
    """``(Ft Worth Edit)`` reads as a credit, because ``Ft`` IS the word ``ft``.

    The brief listed it among the versions, beside a rule (the group's first
    whole word is a marker) under which it is a credit, and the rule is the one
    ``core.tombstone`` records deletions by. A Fort Worth edit and a guest
    called Worth Edit are one spelling, and telling them apart would need a
    rule both modules share, which moves the tombstone identity stamp. Pinned
    so the choice is visible; the card asks Phillip about it.
    """
    from cratekit.core import tombstone

    spelled = "Sun Path (Ft Worth Edit)"
    assert match.split_title(spelled) == ("Sun Path", "")
    assert match._is_a_credit("Ft Worth Edit") and tombstone._is_a_credit("Ft Worth Edit")
    (found,) = resolve([u262_wanted(spelled)], u262_plain_record(tmp_path)).matches
    assert (found.state, found.why) == (match.MatchState.MATCHED, match.Why.EXACT)


def test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version(tmp_path):
    """The index reads a held title through the same split, so the fix reaches both sides.

    Held only as ``Sun Path (Without You Remix)``, a list asking for the plain
    record was matched exact against the remix, because the index had walked
    the group off the held title as a credit.
    """
    held = tagged_container(
        tmp_path,
        tmp_path / "library" / "Sun Path (Without You Remix).flac",
        artist="Nova Reef",
        title="Sun Path (Without You Remix)",
    )
    index = match.index_paths([held])
    (found,) = resolve([u262_wanted("Sun Path")], index).matches
    assert (found.state, found.why) == (match.MatchState.NEEDS_REVIEW, match.Why.VERSION_DIFFERS)
    (same,) = resolve([u262_wanted("Sun Path (Without You Remix)")], index).matches
    assert (same.state, same.why) == (match.MatchState.MATCHED, match.Why.EXACT)


#: One list of groups both credit predicates are asked about: the brief's ten,
#: a marker that is a later word, the bare markers, and spellings of the marker
#: that differ in case and punctuation.
U262_EVERY_GROUP: tuple[str, ...] = (
    *U262_VERSION_GROUPS,
    *U262_CREDIT_GROUPS,
    "Live with Strings",
    "Nightwave Remix",
    "feat",
    "With",
    "FT. Anna",
    "Feat.Anna",
    "ft.anna",
    "featuring",
    "Featurette",
    "Ftw Edit",
    "Ft Worth Edit",
    "With You",
    "",
)


@pytest.mark.parametrize("group", U262_EVERY_GROUP)
def test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is(group):
    """U262. Two modules ask whether a group is a credit, and they now answer alike.

    ``core.tombstone._is_a_credit`` read the first whole word and the matcher
    read the first letters, so ``(Without You Remix)`` was a credit to one and
    a mix name to the other. The tombstone module's rule is inside the
    identity stamp, so the matcher keeps its own copy, and this holds the two
    equal over one list of groups.
    """
    from cratekit.core import tombstone

    assert match._is_a_credit(group) == tombstone._is_a_credit(group)


def test_the_matcher_and_the_tombstone_share_one_credit_vocabulary():
    from cratekit.core import tombstone

    assert match._CREDIT_MARKERS == tombstone._CREDIT_MARKERS


def test_a_defect_title_keeps_the_tombstone_identity_its_spelling_always_had():
    """A tombstone recorded from such a row is still met.

    The identity is the listing's verbatim spelling and the deletion pass
    records a row's Title column composed by ``core.tombstone``, which this
    unit does not touch, so the consult reaches the same record before and
    after. What changes is only which other spellings it composes: the
    remix's bracket and dash forms, where the letters rule composed the null
    qualifier forms of a record it had read as plain.
    """
    from cratekit.core import tombstone

    spelled = "Sun Path (Without You Remix)"
    wanted = u262_wanted(spelled)
    recorded = tombstone.version_identity(
        artist="Nova Reef", title=tombstone.version_title(spelled, "")
    )
    assert wanted.identity == {"artist": "nova reef", "title": "sun path (without you remix)"}
    assert recorded in wanted.suppression_spellings
    assert wanted.addresses == (
        "Sun Path (Without You Remix)",
        "Sun Path [Without You Remix]",
        "Sun Path (Without) (You Remix)",
        "Sun Path (Without You) (Remix)",
        "Sun Path - Without You Remix",
        "Sun Path - Without You Remix (Without You Remix)",
    )
    plain = tombstone.version_identity(artist="Nova Reef", title="Sun Path")
    assert plain not in wanted.suppression_spellings


#: The addresses three credited listings composed before U262, run and recorded
#: on the base. A credited row's spellings must not move.
U262_CREDITED_ADDRESSES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Sun Path (feat. Mira) (Nightwave Remix)",
        (
            "Sun Path (feat. Mira) (Nightwave Remix)",
            "Sun Path (feat. Mira) [Nightwave Remix]",
            "Sun Path (feat. Mira) (Nightwave) (Remix)",
            "Sun Path (feat. Mira) - Nightwave Remix",
            "Sun Path (feat. Mira) - Nightwave Remix (Nightwave Remix)",
        ),
    ),
    ("Sun Path (Nightwave Remix) (ft Mira)", ("Sun Path (Nightwave Remix) (ft Mira)",)),
    (
        "Sun Path (with Mira)",
        (
            "Sun Path (with Mira)",
            "Sun Path (with Mira) (original)",
            "Sun Path (with Mira) [original]",
            "Sun Path (with Mira) (original mix)",
            "Sun Path (with Mira) [original mix]",
            "Sun Path (with Mira) (original) (mix)",
            "Sun Path (with Mira) - original mix",
            "Sun Path (with Mira) - original mix (original mix)",
            "Sun Path (with Mira) (original version)",
            "Sun Path (with Mira) [original version]",
            "Sun Path (with Mira) (original) (version)",
            "Sun Path (with Mira) - original version",
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
        "8",
        "",
        "[X]",
    )


def test_a_dash_inside_a_title_is_never_read_as_a_version():
    """The parser that guessed would invent a record nobody released."""
    assert match.split_version("Sun - Rise") == ("Sun - Rise", "")


def u24_fold(value: str) -> str:
    """U24's ``core.tombstone.fold``, written out INDEPENDENTLY.

    A second implementation on purpose. Calling the function under test to build
    the expected value proves only that it equals itself, and the whole point of
    this pair of tests is that two implementations written in two worktrees agree
    on the bytes.
    """
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


#: INPUTS CHOSEN FOR WHAT A FOLD CHANGE BITES ON, not for readability. Every row
#: is a string where two plausible normalizations disagree, so a copy of this
#: algorithm that drifts from NFC to NFKC, or acquires a leading-article strip, or
#: stops case-folding, produces a different answer HERE rather than passing.
#:
#: A pin over ASCII cannot see any of that: "Aurora Bloom" is NFC-stable, so NFC
#: and NFKC give identical bytes and a drift between them is invisible. The
#: verifier proved that by injecting exactly that change and watching the whole
#: suite stay green.
FOLD_PINS: tuple[tuple[str, str], ...] = (
    # NFC composes; NFD would leave the combining acute on its own.
    ("Café del Mar", "café del mar"),
    ("Café del Mar", "café del mar"),
    # THE TWO ROWS THAT SEE AN NFC TO NFKC DRIFT. Under NFKC the fullwidth run
    # becomes "sun path" and the circled digit becomes "1 track"; under NFC both
    # survive. These are what a pin over ASCII cannot do.
    ("Ｓｕｎ Ｐａｔｈ", "ｓｕｎ ｐａｔｈ"),
    ("① Track", "① track"),
    # Full case folding expands this ligature on its own, with no compatibility
    # normalization involved. Pinned because it is a real property both copies
    # must share, and because it is easy to mistake for an NFKC effect.
    ("Suﬁx", "sufix"),
    # A leading-article strip is a plausible "improvement" and would break both
    # sides silently. The article stays.
    ("The Sun Path", "the sun path"),
    # Case folding is deeper than lowercasing for these two.
    ("STRASSE", "strasse"),
    ("İstanbul", "i̇stanbul"),
    # Spacing folds, punctuation does not, and the two are the axis U24 chose.
    ("  Sun   Path  (Live)  ", "sun path (live)"),
    ("Sun Path [Live]", "sun path [live]"),
    # Non-Latin passes through untouched apart from spacing.
    ("曲  (リミックス)", "曲 (リミックス)"),
)


@pytest.mark.parametrize("given,expected", FOLD_PINS, ids=lambda v: repr(v)[:40])
def test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree(given, expected):
    """PIN THE FOLD, NOT ONE HASH, because a hash pins one input.

    Two copies of this algorithm exist until U24 merges, and the risk is not that
    somebody renames a key: it is that one copy's NORMALIZATION drifts, which
    only shows up on the inputs the normalization exists for. Every row here is
    such an input, and the independently written reference below has to agree
    with the module on all of them.
    """
    assert match.tombstone_fold(given) == expected
    assert match.tombstone_fold(given) == u24_fold(given)


def test_the_fold_pins_actually_discriminate_between_normalizations():
    """A pin nobody proved discriminates is a pin over ASCII wearing a costume.

    Asserts that the table contains at least one row where NFC and NFKC differ,
    one where a leading article would be stripped, and one where composition
    matters, so the table cannot rot into a list of strings that agree under
    every normalization anybody might drift to.
    """
    import unicodedata as u

    inputs = [given for given, _ in FOLD_PINS]
    assert any(
        u.normalize("NFC", given).casefold() != u.normalize("NFKC", given).casefold()
        for given in inputs
    ), "no row here can see an NFC to NFKC drift"
    assert any(given.lower().startswith("the ") for given in inputs)
    assert any(
        u.normalize("NFC", given) != u.normalize("NFD", given) for given in inputs
    )


def test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist():
    """THE ONLY GUARD THAT CAN SEE THE COPIES DRIFT, and it is now armed.

    ARMED AT THE U16 MERGE, 2026-08-13. U24 landed ``cratekit.core.tombstone``
    on main, so the gate this test carried was discharged the way the register
    says one is discharged: the entry was deleted and the decorator came off
    together, because deleting the entry alone makes ``requires`` raise at
    import and takes this whole file out of COLLECTION, which reads as a calm
    green run over 330 tests that never executed.

    Until then two implementations of one algorithm live in two worktrees and
    nothing in either tree can compare them, so this file pins the fold against
    an independently written reference. That catches a drift on THIS side. It
    cannot catch one on the other, and a drift on either side has the same cost:
    a tombstone recorded under one spelling is invisible to the other, the
    version reports missing, acquisition fetches it back, and the deletion is
    undone with the suite green.

    TWO CHECKS, AND THE FIRST ONE IS THE ONE THAT PROVES LEAST. Handing both
    sides the same string proves the FUNCTIONS agree, and this unit's own second
    commit message already says that was never the risk: U24 hashes a collection
    row's Title column verbatim while this side may COMPOSE a title when the
    source spelled the version separately, so the two can agree as functions and
    still be handed different strings for one record. That is not hypothetical.
    It is what a provider row does for six of the seven spellings below, and one
    of the six it reaches only through the companion the recorder writes for a
    credited row, never under the tombstone's own kind.

    So the second check is over the RECORDING PATH: for every rekordbox row shape,
    the identity U24's recorder would write, composed by its OWN
    ``version_title`` from the Title column AND the version column, is compared
    against the identities the three readers on this side actually produce, and
    the ones that cannot reconcile are named in ``UNRECONCILED`` rather than left
    to a silent miss. The version column is in it because that is where the two
    sides diverged: U24 reads a version out of ``RemixerName`` and ``Subtitle``
    and composes, this side composes from a provider's version field, and the
    property that matters is whether the two compositions produce one string.

    WHAT IT STILL CANNOT PROVE, and this is what the residual titled "The two
    tombstone derivations are reconciled only at merge" records: U24's
    RECORDER is not imported here either, so the string it hands
    ``version_identity`` is taken from ``u24_records`` below, which is a
    hand-written imitation of ``deletion.stores.version_of`` that nothing checks
    against U24's real code. This guard compares one real function against one
    real function and one real derivation against an IMITATED one. The check that
    would close it is named in that entry.
    """
    from cratekit.core import tombstone

    assert match.TOMBSTONE_KIND == tombstone.KIND_VERSION
    assert match.UNCREDITED_KIND == tombstone.KIND_VERSION_UNCREDITED
    assert match_cli.TOMBSTONE_STORE == tombstone.STORE_KEY
    for given, _expected in FOLD_PINS:
        assert match.tombstone_fold(given) == tombstone.fold(given)
    # THE VOCABULARY, which is the third thing that exists twice and the one that
    # was never compared. This module reads a dash tail and the domain module
    # reads a free text column, and those are two readers of one question: is
    # this word a version designation. Two answers to it were live and measured,
    # 17 words here against 27 there, and the eleven-word gap reported MISSING
    # and re-acquired a held file for every one of the missing words.
    assert match.VERSION_WORDS == tombstone.VERSION_WORDS
    for row_title in ROW_SPELLINGS:
        assert match.version_identity(
            artist="Aurora Bloom", title=row_title
        ) == tombstone.version_identity(artist="Aurora Bloom", title=row_title)
    # THE COMPOSITION, against the domain module's own rule rather than against
    # this file's imitation of it. Every row is composed the way the recorder
    # composes, then hashed the way the recorder hashes.
    for row_title, row_version, _listed, _title, _version in REKORDBOX_ROWS:
        assert tombstone.version_title(row_title, row_version) == u24_version_title(
            row_title, row_version
        ), "the imitation of version_title in this file has drifted from the real one"
    # THE SHAPES THE BRACKETED TEST DECIDES, which REKORDBOX_ROWS does not cover
    # and which is where the imitation went stale. The literals are what the real
    # module returned when they were recorded, so this fails whichever copy moved.
    for title, version, expected in U24_COMPOSITIONS:
        assert tombstone.version_title(title, version) == expected, (
            f"U24's version_title moved on {title!r} with {version!r}; this "
            f"file's imitation and its recorded literals both need re-measuring"
        )
    # THE DERIVATION, end to end, over BOTH records the recorder writes: the
    # tombstone under its verbatim identity, and the companion a credited row
    # gains with its credit groups out. A listing reaches a deletion when either
    # consult does, which is what ``standing_tombstone`` asks.
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
    """THE MOST EXPENSIVE DEFECT THIS UNIT SHIPPED, pinned so it cannot return.

    Two units addressed the same ``tombstones`` store under the same ``version``
    kind with two different mappings and two different foldings. U24 folds to
    NFC, keeps punctuation, and keys on artist and title with the version inside
    the title; this unit folded to NFKD, stripped punctuation to spaces, and
    keyed on a joined recording token and a separate version. The two hashed to
    ``dc_ddf982896f62fde4317a4fdd`` and ``dc_9ce08a8c650a73894e480868`` for one
    record. Nothing raises when that happens: a version somebody deleted on
    purpose reports missing on the next run and acquisition fetches it back.

    The literal identifier is pinned rather than derived, so a change to the
    folding, the key names, the kind or the store key fails HERE, in the window
    where two copies of this algorithm exist in two worktrees. When U24 merges,
    ``match.TOMBSTONE_KIND`` and ``match.version_identity`` collapse into imports
    from ``cratekit.core.tombstone`` and this test keeps guarding the value.
    """
    identity = match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)")
    assert identity == {"artist": "aurora bloom", "title": "sun path (someone remix)"}
    assert identity == {
        "artist": u24_fold("Aurora Bloom"),
        "title": u24_fold("Sun Path (Someone Remix)"),
    }
    assert match.TOMBSTONE_KIND == "version"
    assert (
        review.suppression_id_for(match_cli.TOMBSTONE_STORE, match.TOMBSTONE_KIND, identity)
        == "dc_ddf982896f62fde4317a4fdd"
    )


#: THE SPELLINGS A REKORDBOX Title COLUMN ACTUALLY HOLDS for one version of one
#: recording. U24 hashes this string verbatim, so this is the input to the other
#: side of the seam, and the question this table asks is whether a LIST naming
#: the same record arrives at the same identity.
ROW_SPELLINGS = [
    "Sun Path (Nightwave Remix)",
    "Sun Path - Nightwave Remix",
    "Sun Path [Nightwave Remix]",
    "Sun Path (feat. Mira) (Nightwave Remix)",
    "Sun Path (Extended) (Remastered)",
    "Sun Path",
    "Sun Path (Original Mix)",
]


#: ONE REKORDBOX COLLECTION ROW PER ENTRY, plus what a list naming the same
#: record spells, plus the provider row a source with a separate version field
#: ships for it. Every column a literal, because an input built by the code under
#: test cannot show that code reading a row wrongly.
#:
#: THE VERSION COLUMN IS WHY THIS TABLE REPLACED A LIST OF TITLES. U24's recorder
#: no longer hashes the Title column on its own: it reads a version out of
#: ``RemixerName`` and then ``Subtitle`` and passes both through
#: ``version_title``, because two different remixes of one recording collide
#: whenever the mix name sits in those columns rather than inside the Title.
#: Fields: title column, version column, what a list spells, provider title,
#: provider version.
REKORDBOX_ROWS: tuple[tuple[str, str, str, str, str], ...] = (
    ("Sun Path (Nightwave Remix)", "Nightwave Remix",
     "Sun Path (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
    ("Sun Path - Nightwave Remix", "Nightwave Remix",
     "Sun Path - Nightwave Remix", "Sun Path", "Nightwave Remix"),
    ("Sun Path [Nightwave Remix]", "Nightwave Remix",
     "Sun Path [Nightwave Remix]", "Sun Path", "Nightwave Remix"),
    ("Sun Path (feat. Mira) (Nightwave Remix)", "Nightwave Remix",
     "Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
    # THE ROW U24'S OWN FIX IS ABOUT. The mix name is in the version column and
    # nowhere in the Title, so the recorder COMPOSES rather than short
    # circuiting, and what it composes is the parenthesised form this side
    # composes for the same record.
    ("Sun Path", "Nightwave Remix",
     "Sun Path (Nightwave Remix)", "Sun Path", "Nightwave Remix"),
    ("Sun Path (Extended) (Remastered)", "",
     "Sun Path (Extended) (Remastered)", "Sun Path", "Extended Remastered"),
    ("Sun Path", "", "Sun Path", "Sun Path", ""),
    ("Sun Path (Original Mix)", "",
     "Sun Path (Original Mix)", "Sun Path", "Original Mix"),
)

#: THE DERIVATIONS THAT DO NOT RECONCILE, named rather than left to a silent
#: miss, AND EMPTY ON PURPOSE. It held one entry, ``("Sun Path (feat. Mira)
#: (Nightwave Remix)", match.TIDAL)``: a featured credit is dropped from the
#: matching title because it names a performer, so a source that never spelled it
#: cannot put it back, and the library row that kept it was unreachable from a
#: provider row. Recorded in docs/residual-findings.md under "A provider row
#: cannot address a library row that kept a featured credit". It went empty when
#: the recorder began writing a companion with the credit groups out, which the
#: residual titled "A deleted track the tombstone consult cannot reach is listed
#: for download" records. The verbatim consult STILL cannot reach that row, and
#: ``test_the_verbatim_consult_alone_still_misses_the_credited_row`` pins that,
#: so this tuple being empty says the companion is doing the work and not that
#: the verbatim consult widened. Growing it is a change somebody has to make on
#: purpose.
UNRECONCILED: tuple[tuple[str, str], ...] = ()


#: U24's ``core.tombstone`` bracket and credit vocabulary, written out
#: INDEPENDENTLY at ``81d575c`` and unchanged at that branch's current tip.
#: Second implementations on purpose, for the reason :func:`u24_fold` gives.
U24_BRACKETED = re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]")
U24_CREDIT_MARKERS = frozenset({"feat", "ft", "featuring", "with"})
U24_WORD_SPLIT = re.compile(r"\W+", re.UNICODE)


def u24_is_a_credit(group: str) -> bool:
    """U24's ``core.tombstone._is_a_credit``, written out INDEPENDENTLY.

    The FIRST WORD of the group and nothing else, because that is where the
    convention puts the marker: ``(feat. Anna)``, ``(with Anna)``. A containment
    test would read ``(Live with Strings)`` as a credit and stop composing for a
    real mix name.
    """
    words = U24_WORD_SPLIT.split(u24_fold(group).strip())
    return bool(words) and words[0] in U24_CREDIT_MARKERS


def u24_already_carries(title: str, folded_version: str) -> bool:
    """U24's ``core.tombstone._already_carries``, written out INDEPENDENTLY.

    **A PLAIN SUBSTRING TEST IS WHAT THIS FILE USED TO IMITATE, AND IT WAS THREE
    ROUNDS STALE.** U24 replaced ``folded_version in fold(title)`` with a
    DELIMITED question and recorded why in its own docstring: a substring test
    reads ``Live`` as already carried by ``Lively Up``, so two rows of one
    recording collapse onto one identity and deleting either suppresses both.

    So the test is bracketed. A title carries its own mix name inside ``(...)``
    or ``[...]`` and nowhere else, which is the convention providers and
    rekordbox libraries actually spell. The match INSIDE the group is delimited
    on word boundaries too, because ``RemixerName`` holds an artist name and
    requiring the group to equal the version would compose ``Strobe (Michael
    Woods Remix) (Michael Woods)``. A group opening with a credit marker is
    skipped entirely, because what is inside it is a performer either way.

    WHAT THE STALE IMITATION COST, measured against U24's real module rather
    than argued: for the row ``Sun Path - Nightwave Remix`` with ``Nightwave
    Remix`` in the version column, U24 composes ``Sun Path - Nightwave Remix
    (Nightwave Remix)`` and the substring imitation returned the title unchanged.
    The armed derivation guard below therefore computed ONE unreconciled entry
    and passed, while the same computation against U24's real module yields FOUR:
    a tombstone U24 records that none of this side's three readers could address,
    so the version reported missing, acquisition re-fetched it, the deletion was
    undone, and the suite stayed green. The three that were hidden are closed in
    ``_spellings_of`` rather than named as a gap.
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

    THE COMPOSITION RULE, WHICH IS WHERE THE SEAM ACTUALLY IS. It composes with
    round parentheses, which is the shape this side composes with, so the plain
    case meets. What it also does is SHORT CIRCUIT, on the bracketed question
    :func:`u24_already_carries` asks: when a bracketed group of the title already
    names the version, the Title column is recorded exactly as it stands. So
    whatever shape a rekordbox Title happens to use survives into the identity,
    and a consulter cannot assume one shape, it has to enumerate them.

    THE EMPTY CHECK IS LOAD BEARING NOW and was decorative before. ``fold("")``
    is ``""`` and ``"" in anything`` is true, so under a substring test the first
    clause could be deleted with nothing noticing; under a bracketed test an
    empty version answers no, and deleting the check would compose ``Sun Path ()``
    for every ordinary library row.
    """
    folded = u24_fold(version)
    if not folded or u24_already_carries(title, folded):
        return title
    return f"{title} ({version})" if title else version


#: WHAT U24'S REAL ``version_title`` RETURNS, RUN AND RECORDED, at ``81d575c``
#: and unchanged at that branch's current tip. Literals rather than a comparison,
#: because a comparison against the real module can only run once it merges and
#: an imitation nothing pins today is how the last one went three rounds stale.
#:
#: EVERY ROW IS A SHAPE THE BRACKETED TEST DECIDES DIFFERENTLY FROM A SUBSTRING
#: TEST, which is the whole point: a table of ordinary titles would agree under
#: both and pin nothing. ``Lively Up`` and ``Extended Play Track`` are the two
#: over-suppressions U24's own docstring names; ``Strobe (Michael Woods Remix)``
#: is the word-boundary case, where the group CONTAINS the version rather than
#: equalling it; ``Losing It (feat. Anna)`` is the credit group, which is skipped
#: so a remix and its original stay apart; the dash and curly rows are the two
#: shapes where the recorder composes and this file used to think it did not.
#: Fields: Title column, version column, the identity title U24 writes.
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
    ("Sun Path", "", "Sun Path"),
    ("", "Nightwave Remix", "Nightwave Remix"),
)


@pytest.mark.parametrize("title,version,expected", U24_COMPOSITIONS, ids=lambda v: str(v)[:32])
def test_this_files_imitation_of_the_recorder_still_composes_what_u24_composes(
    title, version, expected
):
    """THE GUARD THAT RUNS TODAY, and its absence is what let the imitation rot.

    An imitation of another branch's code is a CLAIM ABOUT THAT BRANCH, and a
    claim nothing checks is a claim that drifts. This file's copy of
    ``version_title`` used a plain substring test for three rounds after U24
    replaced it with a bracketed one, and the only comparison against the real
    module was gated behind the merge. The armed derivation guard therefore
    computed one unreconciled entry and passed while the real answer was four,
    hiding a tombstone U24 records that none of this side's readers could reach.

    So the expected strings are LITERALS taken by running U24's module, and this
    fails the moment either copy moves. The gated guard below asserts the same
    table against the real function once it can import it, which closes the loop
    from the other end.
    """
    assert u24_version_title(title, version) == expected


def u24_records(artist: str, row_title: str, row_version: str = "") -> dict[str, str]:
    """What U24's recorder writes, DERIVED the way it derives it.

    ``deletion.stores.version_of`` hands ``row.artist`` and
    ``tombstone.version_title(row.title, row.version)`` to ``version_identity``,
    where ``row.title`` is the collection row's Title column and ``row.version``
    is read from ``RemixerName`` and then ``Subtitle``. Written out here rather
    than imported, because the deletion package is landing in its own worktree
    and the whole point of this helper is to be a SECOND implementation.

    AN IMITATION, AND NOTHING HERE CHECKS IT AGAINST U24'S REAL RECORDER. The
    fold and the composition below are second implementations of algorithms
    stated to this unit; the READER that fills ``row.version`` is a file in
    another worktree. If it maps a column this does not, this helper agrees with
    the code here and both disagree with what actually gets written. The residual
    titled "The two tombstone derivations are reconciled only at merge" records
    that and names the check that would close it.
    """
    return {
        "artist": u24_fold(artist),
        "title": u24_fold(u24_version_title(row_title, row_version)),
    }


def u24_uncredited(artist: str, row_title: str, row_version: str = "") -> dict[str, str] | None:
    """The COMPANION the recorder writes beside a credited tombstone, or None.

    ``deletion.stores.uncredited_version_of`` written out INDEPENDENTLY, for the
    reason :func:`u24_fold` gives. The composed title with every bracketed group
    whose first word is a credit marker taken out, folded. None when nothing was
    taken out, and None when nothing was left.
    """
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
    """THE SEAM, and it is what a literal-fed parity test cannot see.

    Round one proved the FUNCTION agreed, by handing both sides the same string.
    The entire risk is that the two sides DERIVE different strings from one
    record, and they did: this side split the title, pulled the version out and
    put it back in round parentheses, so it agreed only where the row happened to
    use that one spelling. Four of the seven below missed, including the dash
    form this unit had just learned to parse, and a miss is silent on both sides
    because nothing knows a tombstone exists.

    Driven from the ROW SPELLING through the real readers, which is the only way
    to see it. A pasted list and a public playlist both hand over the title as
    the row spells it, so the address is that string, unaltered.
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


#: EVERY IDENTITY TITLE the provider row for the Nightwave remix has to reach,
#: as LITERALS. The test this replaces derived its expected value by calling
#: ``match.listed_title``, the function under test, so the assertion reduced to
#: ``X in (X,)``: rewriting ``listed_title`` to compose with square brackets left
#: it green, and rewriting it to compose with a dash left it green too. A test
#: that builds its expectation by calling the code under test asserts nothing.
PROVIDER_REACHES: tuple[str, ...] = (
    "sun path (nightwave remix)",
    "sun path [nightwave remix]",
    "sun path - nightwave remix",
)

#: The provider row those literals belong to.
PROVIDER_ROW = {"title": "Sun Path", "version": "Nightwave Remix",
                "artist": {"name": "Aurora Bloom"}}


@pytest.mark.parametrize("spelling", PROVIDER_REACHES)
def test_a_provider_row_reaches_every_spelling_of_the_version_it_names(spelling):
    """The one source that never spelled the two together, held to the same seam.

    A provider carries the version beside the title, so ``spelled`` is empty and
    the address had to be composed, and the composition produced exactly ONE
    identity: the parenthesised one. Of the seven spellings a rekordbox Title
    column really holds, a provider-sourced list could address that one, so a
    tombstone U24 wrote from ``Sun Path - Nightwave Remix`` or ``Sun Path
    [Nightwave Remix]`` was invisible and the version was re-acquired at exit
    zero, which is the headline this unit's second round claimed to have fixed
    and had not.
    """
    wanted = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert {"artist": "aurora bloom", "title": spelling} in wanted.suppression_spellings


def test_the_one_spelling_a_provider_row_cannot_reach_is_named_rather_than_assumed():
    """A GAP STATED IS A GAP SOMEBODY CAN CLOSE, and one residual states this one.

    "A provider row cannot address a library row that kept a featured credit".

    A featured credit is dropped from the matching title because it names a
    performer rather than an edit, so a row that never spelled it has nothing to
    put back and cannot address the library row that kept it. The list that DID
    spell it reaches it, which is what makes this a limit of the provider shape
    and not of the addressing rule.
    """
    credited = {"artist": "aurora bloom", "title": "sun path (feat. mira) (nightwave remix)"}
    provider = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert credited not in provider.suppression_spellings
    spelled = match.read_text_lines(
        "Aurora Bloom - Sun Path (feat. Mira) (Nightwave Remix)\n"
    )[0]
    assert credited in spelled.suppression_spellings


#: LISTINGS WHOSE CREDIT IS NOT WHERE ``_head_of`` LOOKS FOR IT, ACROSS ALL
#: THREE READERS, and the exact set of addresses each one may produce. A literal
#: everywhere: deriving the expectation from ``Wanted.addresses`` would assert
#: that the code agrees with itself, which is the shape that let this defect
#: through three rounds.
#:
#: THE THIRD COLUMN IS WHY THIS TABLE GREW. The first three rounds of this fix
#: were verified on ``read_text_lines`` alone, and the provider reader is the one
#: shape where the credit is DISCARDED BEFORE the precondition can look at it: a
#: row that carries its version in its own field had its ``spelled`` string
#: composed from the MATCHING title, which has had its credits taken off, so
#: ``_credits_in(head) == _credits_in(spelled)`` was vacuously true on both sides
#: and every address composed was the plain record's. A fix verified on one
#: reader out of three is how this came back after being fixed once already.
#: Fields: the title a list spells, the provider's own two fields, the addresses
#: the two spelled-title readers produce, the addresses the provider produces.
CREDIT_OUTSIDE_THE_SUFFIX: tuple[
    tuple[str, tuple[str, str], tuple[str, ...], tuple[str, ...]], ...
] = (
    # The credit is printed AFTER the version group.
    (
        "Sun Path (Live) (feat. Mira)",
        ("Sun Path (feat. Mira)", "Live"),
        ("Sun Path (Live) (feat. Mira)",),
        ("Sun Path (feat. Mira) (Live)", "Sun Path (feat. Mira) [Live]"),
    ),
    # And the same shape with square brackets, which is a different branch.
    (
        "Sun Path [Live] (feat. Mira)",
        ("Sun Path (feat. Mira)", "Live"),
        ("Sun Path [Live] (feat. Mira)",),
        ("Sun Path (feat. Mira) (Live)", "Sun Path (feat. Mira) [Live]"),
    ),
    # The version arrives in more than one group, so there is no single suffix
    # to take off. This is the one the third round made WORSE for the spelled
    # readers and the fourth left live for the provider: it composed FOUR
    # credit-free addresses, one of them ``Sun Path (Extended) (Remastered)``, a
    # literal row in this file's own REKORDBOX_ROWS.
    (
        "Sun Path (feat. Mira) (Extended) (Remastered)",
        ("Sun Path (feat. Mira)", "Extended Remastered"),
        ("Sun Path (feat. Mira) (Extended) (Remastered)",),
        (
            "Sun Path (feat. Mira) (Extended Remastered)",
            "Sun Path (feat. Mira) [Extended Remastered]",
            "Sun Path (feat. Mira) (Extended) (Remastered)",
            "Sun Path (feat. Mira) - Extended Remastered",
            # THE RECORDER'S COMPOSITION ON TOP OF THE DASH FORM. U24 skips a
            # credit group when it asks whether a title already carries its
            # version, so a Title column holding the dash spelling with the
            # version repeated in its own column is composed rather than kept,
            # and this is the string it composes. Measured against U24's real
            # module. It keeps the credit, which is what the assertion below is
            # about.
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
    """THE OVER-EAGER DIRECTION, WHICH THE DESIGN REJECTS AND THE CODE WAS DOING.

    ``_head_of`` takes the version off the END of the spelling, and a featured
    credit is not always last. Where it could not be located the composition fell
    back to the MATCHING title, which has had its credits taken off, so every
    address composed was the PLAIN record's, and deleting the plain row resolved
    a list line naming the credited recording to SUPPRESSED: in none of the three
    arrays, at exit zero, with acquisition skipping a track nobody had deleted.

    DRIVEN THROUGH ALL THREE READERS, because closing it on one is what happened
    twice. The provider row is the shape that stayed open: its credit was thrown
    away while the two fields were being put back together, before the credit
    precondition could compare anything, so the comparison was empty against
    empty and passed.

    THE SET IS ASSERTED WHOLE rather than by absence, because "the plain address
    is gone" is also true of a composition that produces some other wrong string.
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
    """The same thing DRIVEN, because the cost is a track that never arrives.

    ``test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`` pins
    the shape where the credit is the whole trailing group. These are the shapes
    where ``_head_of`` cannot find the version at the end, one of which composed
    the literal ``Sun Path (Extended) (Remastered)`` row this deletes.

    ONE LIST LINE PER READER, in the shape that reader really ships, so the
    tombstone this deletes is either reached by all three or by none, and a fix
    that lands on one of them is visible here rather than three rounds later.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Extended) (Remastered)"),
        actor="deletion",
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
        rows: list[dict] = [{"id": "sp1", "name": listed,
                             "artists": [{"name": "Aurora Bloom"}]}]
    else:
        rows = [{"id": "1", "title": provider[0], "version": provider[1],
                 "artist": {"name": "Aurora Bloom"}}]
    return write_list(
        tmp_path,
        json.dumps({"list": 1, "origin": origin, "tracks": rows}),
        f"{name}-{origin}.json",
    )


def test_the_plain_record_is_still_suppressed_for_the_list_that_names_it(
    cfg, music, tmp_path
):
    """THE OTHER HALF, because "nothing is suppressed" is also a way to pass.

    Every assertion above is a negative one, and a composition that produced no
    address at all would satisfy all of them while quietly switching the
    tombstone consult off. The list that names the record the deletion actually
    took still reaches it.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Extended) (Remastered)"),
        actor="deletion",
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
    """WHAT ``_head_of`` IS ACTUALLY FOR, and the only thing that needs it.

    For a listing with no credit, the head this composes from and the matching
    title are the same string, so the whole function is indistinguishable from
    its own fallback. It earns its keep on exactly one input: a credited listing
    whose version IS a bracketed suffix, where it keeps the credit that
    ``split_version`` took off and the fallback cannot. Lose either bracket shape
    and the credited row spelled the other way becomes unreachable, and a
    deletion of it is undone at exit zero.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", recorded_row),
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
    """THE READ-BACK GATE IS THE CONSERVATIVE READER, and it had been widened.

    ``_spellings_of`` composes the dash form only when this module's own reader
    reads it back as the same record. The third round let ``split_ambiguous``
    satisfy that, and ``split_ambiguous`` reads a string back by DECLARING that
    this module cannot tell whose record it names. So ``Sun Path - Live`` became
    an address of the live cut of "Sun Path", and a deletion of a composition
    genuinely called "Sun Path - Live" would have silently withheld it. Nothing
    could observe the widening, because the listing that spells the dash form
    already addresses itself.
    """
    assert (("artist", "aurora bloom"), ("title", dashed)) not in spellings_of(listed)


def test_every_row_spelling_is_addressed_from_every_reader_or_is_a_named_gap():
    """THE DERIVATION CHECK THAT RUNS TODAY, while U24 is in another worktree.

    The gated guard above compares this side against the real domain module and
    cannot run yet. This one compares it against ``u24_records``, an
    independently written second implementation, over all three readers and every
    rekordbox row shape, so the seam is checked every run rather than only after
    a merge. The gaps are a literal tuple: one going missing means a tombstone
    became invisible, and one going away means the featured-credit residual is
    stale.

    DRIVEN FROM THE ROW AND ITS VERSION COLUMN, not from a title alone, because
    that is what the recorder is handed. The row whose mix name sits only in the
    version column is the one U24's own fix exists for, and it is the one that
    proves the two sides now COMPOSE the same string rather than merely agreeing
    when neither of them composes anything.
    """
    missed = tuple(
        (row[0], wanted.origin)
        for row in REKORDBOX_ROWS
        for wanted in every_reader_on(row)
        if not reaches(
            wanted,
            u24_records("Aurora Bloom", row[0], row[1]),
            u24_uncredited("Aurora Bloom", row[0], row[1]),
        )
    )
    assert missed == UNRECONCILED


def test_the_verbatim_consult_alone_still_misses_the_credited_row():
    """WHAT ``UNRECONCILED`` GOING EMPTY DOES NOT MEAN.

    The provider row still cannot address the credited library row under the
    tombstone's own kind, because it was never handed the credit. That miss is
    the conservative direction and it is kept: what closed the residual titled
    "A deleted track the tombstone consult cannot reach is listed for download"
    is a second record on the recorder's side, not a wider consult on this one.
    A literal on every side, so a verbatim consult that started composing from
    the stripped title fails here by name.
    """
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
        "Sun Path (feat. Zed) (Nightwave Remix)",
        "Sun Path (Nightwave Remix) (feat. Zed)",
        "Sun Path [ft. Zed] [Nightwave Remix]",
        "Sun Path (with Zed) - Nightwave Remix",
    ],
)
def test_a_listing_that_spelled_a_credit_never_asks_for_a_companion(listed):
    """THE GUARD ON THE CONSULTING SIDE, in every reader that can spell a credit.

    A companion is a credited deletion with the guest taken out, so it cannot
    say WHICH guest. A listing crediting Zed that asked under it would be
    withheld by a deletion of the recording crediting Mira, which is the over
    eager direction. So a listing that spelled any credit asks nothing.
    """
    for wanted in (
        match.read_text_lines(f"Aurora Bloom - {listed}\n")[0],
        match.read_spotify_items([{"name": listed, "artists": [{"name": "Aurora Bloom"}]}])[0],
        match.read_tidal_tracks(
            [{"title": listed, "version": "", "artist": {"name": "Aurora Bloom"}}]
        )[0],
    ):
        assert wanted.uncredited_spellings == ()


def test_the_recorder_and_the_consulter_compose_the_same_string():
    """THE PROPERTY, rather than two functions handed one string.

    The round before this proved the identity FUNCTIONS agreed by giving both
    sides the same input, which cannot see the risk: the recorder DERIVES its
    string from a collection row and this side derives one from a listing. Now
    that the recorder composes too, the property is sharp and can be stated. For
    a row whose version lives only in the version column, the string the recorder
    hands ``version_identity`` must be one of the strings this side consults
    under, and the parenthesised composition is where they meet.

    The expected string is a LITERAL. Deriving it from either composition would
    make this agree with whichever one changed.
    """
    recorded = u24_version_title("Sun Path", "Nightwave Remix")
    assert recorded == "Sun Path (Nightwave Remix)"
    wanted = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert "Sun Path (Nightwave Remix)" in wanted.addresses


def test_the_only_doubled_address_is_the_one_the_recorder_actually_writes():
    """IDEMPOTENCE WHERE THE RECORDER HAS IT, AND A DOUBLE WHERE IT DOES NOT.

    THE SENTENCE THIS TEST USED TO ASSERT WAS MEASURABLY FALSE. It forbade every
    doubled address on the argument that ``Sun Path (Nightwave Remix) (Nightwave
    Remix)`` is "an address nothing will ever record", and that argument was a
    written explanation with no measurement behind it. ``version_title`` short
    circuits on a BRACKETED question, not on containment, so a rekordbox Title
    column holding ``Sun Path - Nightwave Remix`` beside a version column
    repeating ``Nightwave Remix`` is composed into ``Sun Path - Nightwave Remix
    (Nightwave Remix)``. U24's real module was run to get that string. The blanket
    ban is what kept this side from ever consulting under it, and the cost was a
    deletion undone in silence.

    SO THE PROPERTY IS SHARPER, not weaker. A doubled address is allowed for
    exactly the spelling whose double the recorder writes, the DASH form, and for
    no other. The bracketed spellings still compose once, because a bracketed
    group is what makes the recorder short circuit, and composing over one of
    those would produce a string nothing records. That distinction is the whole
    of ``_already_carries``, so it is the thing worth asserting.
    """
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
            [],
            ["Sun Path - Nightwave Remix (Nightwave Remix)"],
        ), f"a version was composed twice under a spelling nothing records: {doubled}"
        # AND NEVER ONTO A BRACKETED SPELLING, which is where the recorder short
        # circuits and where a double would address nothing.
        assert not [
            address for address in doubled
            if "(nightwave remix) (nightwave remix)" in address.casefold()
            or "[nightwave remix] (nightwave remix)" in address.casefold()
        ]
    # THE DASH DOUBLE IS ACTUALLY REACHED, so this is not two negative clauses
    # agreeing that nothing happens.
    assert "Sun Path - Nightwave Remix (Nightwave Remix)" in (
        match.read_tidal_tracks([PROVIDER_ROW])[0].addresses
    )


#: A TITLE SHAPE THIS SIDE DOES NOT ENUMERATE. The recorder keeps whatever shape
#: the Title column used, so the consulter has to know the shapes; it knows round
#: parentheses, square brackets, the dash and the multi-group split. Anything
#: else misses, and that class is recorded under "The recorder keeps the Title
#: column's own shape, so the consulter enumerates shapes" rather than guessed at.
UNENUMERATED_SHAPE = ("Sun Path {Nightwave Remix}", "Nightwave Remix")


def test_a_title_shape_outside_the_enumerated_ones_is_a_recorded_gap():
    """THE BOUNDARY OF THE ENUMERATION, asserted rather than assumed, AND IT MOVED.

    A consulter that enumerates shapes has an edge, and an edge nobody wrote down
    is discovered by a track coming back after somebody deleted it. The edge was
    written down wrongly here for three rounds, because this file's imitation of
    ``version_title`` used a plain substring test while the real one asks a
    BRACKETED question. Under the substring test a curly-brace Title short
    circuited and the identity kept that exact shape, so a list spelling it the
    same way reached it. It does not: a curly brace is not a bracket U24 reads,
    so the recorder COMPOSES, and what it writes is ``sun path {nightwave remix}
    (nightwave remix)``.

    WHAT REACHES IT NOW IS THE OTHER READER, which is the useful half of the
    boundary. A source carrying its version in its OWN FIELD hands this side a
    title and a version, and this side composes the parenthesised form onto the
    title it was handed, curly braces and all, so it meets the recorder exactly.
    A pasted line spelling the curly form carries no version this side can read,
    so it composes the null-qualifier equivalents instead and misses. That is the
    class the residual titled "The recorder keeps the Title column's own shape,
    so the consulter enumerates shapes" records, and it is a limit of what this
    side can PARSE rather than of what it composes.
    """
    title, version = UNENUMERATED_SHAPE
    recorded = u24_records("Aurora Bloom", title, version)
    assert recorded["title"] == "sun path {nightwave remix} (nightwave remix)"
    # The plain provider row names a different title and cannot reach it.
    listed = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert recorded not in listed.suppression_spellings
    # NOR DOES THE LIST THAT SPELLED IT THE SAME WAY, because the curly brace
    # carries no version this side reads, so there is nothing to compose.
    same = match.read_text_lines(f"Aurora Bloom - {title}\n")[0]
    assert recorded not in same.suppression_spellings
    # A source that keeps its version in a field DOES reach it, which is what
    # makes this a parsing edge rather than a composition edge.
    fielded = match.read_tidal_tracks(
        [{"title": title, "version": version, "artist": {"name": "Aurora Bloom"}}]
    )[0]
    assert recorded in fielded.suppression_spellings


@pytest.mark.parametrize(
    "recorded_title",
    ["sun path - nightwave remix", "sun path [nightwave remix]"],
)
def test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found(
    recorded_title,
):
    """DRIVEN THROUGH RESOLUTION, which is where the multi-spelling consult lived.

    Narrowing ``resolve_one`` back to a single-spelling lookup killed no test in
    this file. The one that died when ``suppression_spellings`` was narrowed
    asserted a set intersection on the object and never went through resolution,
    so the consult was unobservable at its most important call site: the branch
    that decides whether a version is re-acquired.

    The recorded identity is a literal, so nothing here can agree with a
    composition that changed underneath it.
    """
    standing = {"artist": "aurora bloom", "title": recorded_title}

    def suppresses(kind, identity):
        return kind == match.TOMBSTONE_KIND and dict(identity) == standing

    found = match.resolve_one(
        match.read_tidal_tracks([PROVIDER_ROW])[0],
        match.LibraryIndex(by_recording={}),
        suppresses=suppresses,
        suppression_id=no_identifier,
    )
    assert found.state is match.MatchState.SUPPRESSED
    assert found.why is match.Why.TOMBSTONED


@pytest.mark.parametrize(
    "recorded_title,reachable",
    [
        # This module reads "Sun Path - Original Mix" back as the plain record,
        # because a two-word tail ending in the vocabulary is a version. So a
        # tombstone written from that row names the same version and is reached.
        ("sun path - original mix", True),
        ("sun path - original version", True),
        # It reads "Sun Path - Original" as a TITLE, because a bare one-word tail
        # outside the vocabulary is not a qualifier. Composing that spelling
        # anyway would let a deletion of somebody else's record withhold this
        # one, which is the over-eager direction the design rejects by name.
        ("sun path - original", False),
    ],
)
def test_a_dash_spelling_is_composed_only_when_this_module_reads_it_back(
    recorded_title, reachable
):
    """THE GATE ON THE ONE AMBIGUOUS CONVENTION, asserted in both directions.

    Brackets at the end of a title are a qualifier by convention, so they are
    composed unconditionally. A dash can be part of the title itself, which is
    the whole reason ``split_title`` is vocabulary-guarded, so a dash spelling is
    composed only when this module's own reader reads it back as the same record.
    Without the gate the consult addresses rows it would itself call somebody
    else's; with the gate applied to brackets too, the canonical composition for
    a credited head disappears.
    """
    spellings = frozen(match.read_text_lines("Aurora Bloom - Sun Path\n")[0].suppression_spellings)
    composed = (("artist", "aurora bloom"), ("title", recorded_title))
    assert (composed in spellings) is reachable


@pytest.mark.parametrize(
    "line,suppressed",
    [
        # The listing spells the version the way the tombstone was recorded, so
        # it addresses it and the deletion stands.
        ("Aurora Bloom - Sun Path (Live)", True),
        ("Aurora Bloom - Sun Path [Live]", True),
        # And the one this round REFUSED to address, on purpose. See below.
        ("Aurora Bloom - Sun Path - Live", False),
    ],
    ids=["round", "square", "ambiguous-dash"],
)
def test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one(
    cfg, music, tmp_path, line, suppressed
):
    """ONE AMBIGUITY, ONE POLICY, AND IT USED TO HAVE TWO, driven at resolution.

    ``_spellings_of`` refuses to compose ``Sun Path - Live`` from a head and a
    version, and says why: a deletion of a composition genuinely called "Sun Path
    - Live" would then silently withhold the live cut of "Sun Path". The mirror
    of that was wide open in ``Wanted.addresses``, which walked BOTH readings, so
    the list line ``Aurora Bloom - Sun Path - Live`` composed ``Sun Path (Live)``
    and a deletion of the live cut silently withheld a listing that may well mean
    the composition. Same cost, opposite direction, defended in one docstring
    while being rejected by name two functions away.

    THE POLICY THAT WON IS THE CONSERVATIVE ONE, because ``tombstone_fold``
    settles it and has for three rounds: a missed suppression re-acquires
    something and REPORTS it, an over-eager one withholds music somebody wants
    and says nothing. So the dash-spelled listing is reported MISSING with
    something to go and get, which is the cost, and it is the cost that shows up
    in a run rather than the one that never does.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
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
    """THE SAME RULE ON THE OBJECT, in both directions, as literals.

    The driven test above proves one direction costs a re-acquisition. This
    proves the rule is symmetric: the dash-spelled listing composes no bracketed
    address, and the bracket-spelled listing composes no dash address. An
    asymmetry here is the shape the last three rounds kept producing, where one
    of the two functions was fixed and the other went on doing the opposite.
    """
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
    """The loosening this must not be. KTD16 says a tombstone identifies a VERSION.

    REBUILT ON INPUTS THAT ACTUALLY HAVE SEVERAL SPELLINGS. The version this
    replaces built every input with ``one()``, which constructs ``Wanted``
    directly with ``spelled=""``, so each input carried exactly one identity and
    the assertion was that four singletons did not intersect. It would have
    passed against a consult that never widened at all, which is the shape it
    exists to bound.

    The strangers are chosen one axis apart each: no qualifier, a different
    qualifier, a different recording, and the one-word dash form whose second
    reading is the case the readings rule added.
    """
    remix = spellings_of("Sun Path (Nightwave Remix)")
    assert len(remix) > 1, "the input carries one spelling, so this bounds nothing"
    for stranger in (
        "Sun Path",
        "Sun Path (Someone Remix)",
        "Sun Pathway (Nightwave Remix)",
        "Sun Path - Live",
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
        ("Aurora Bloom", "Sun Path", "Someone Remix"),
        ("Aurora Bloom", "Sun Path", ""),
        ("Aurora Bloom", "Sun Path", "Original Mix"),
        ("  Nova   Reef ", " Tide  Line ", "Extended Mix"),
        ("Caf\u00e9 del Mar", "Track", "Live"),
    ],
)
def test_a_composed_address_still_matches_a_row_spelled_that_way(artist, title, version):
    """The composition path, held to the row it is modelled on.

    ``Original Mix`` is in the table on purpose: this module folds that qualifier
    away for MATCHING, because a record listed as the original mix and the same
    record listed with nothing are one version. It must NOT fold it away for the
    tombstone, because U24 does not, and a suppression that disagrees about one
    qualifier is a suppression that misses.
    """
    composed = match.listed_title(title.strip(), version)
    assert match.version_identity(artist=artist, title=composed) == u24_records(
        artist, composed
    )


def test_an_identity_with_neither_an_artist_nor_a_title_is_refused():
    """It would hash to one value and collapse the whole library onto it.

    U24 refuses this, so this side refuses it identically, or the collapse
    arrives from whichever producer did not.
    """
    with pytest.raises(CratekitError) as excinfo:
        match.version_identity(artist="  ", title="")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_review_item_identity_is_not_the_tombstone_identity():
    """Two questions, two addresses, and the key is in one of them.

    A tombstone is a fact about a version that outlives every list. A review item
    is an answer to something somebody was asked, and ``key_disagreement`` can
    move a track from matched to needs review, so a key question is its own
    question. Sharing one identity let one answer settle three: accept at 08A and
    every later key question on that recording came back matched, including 03B,
    the relative minor this module names as the trap.
    """
    version = match.Why.VERSION_DIFFERS
    asked = one(version="Extended Mix", key="08A")
    assert set(asked.identity) == {"artist", "title"}
    assert set(asked.question(version)) == {"recording", "version", "key", "asks"}
    assert asked.question(version)["key"] == "08A"
    # THE KEY SET NEVER VARIES AND NEITHER DOES THE VALUE. Every value is read
    # off the LIST LINE. The argument ``question`` takes is which question is
    # being asked, not what the library holds, and the one it used to take was
    # the second of those. A list line naming no key carries the empty token,
    # which is what an unreadable code folds to too.
    assert one(version="Extended Mix").question(version)["key"] == ""
    assert one(version="Extended Mix", key="8A").question(version) == asked.question(
        version
    )
    assert one(version="Extended Mix", key="03B").question(version) != asked.question(
        version
    )


def test_a_key_question_and_a_version_question_are_two_items_on_one_line():
    """THE HALF THE LAST ROUND DELETED ALONG WITH THE DEFECT, on the object.

    Putting the list's key on every question stopped the identity moving with the
    disk, and it also made "your list says 08A and I hold this exact version at
    another key" and "your list says 08A and I hold a different version" ONE
    item. Both carry the same recording, the same version token and the same key,
    so the only thing that can tell them apart is which question is being asked,
    which is what ``asks`` carries and what :data:`match.KEY_QUESTIONS` decides.

    THE APPROXIMATE AND READING QUESTIONS ARE TWO MORE, for the same reason and
    with the same cost if they collapse: an approximate offer is candidates from
    a DIFFERENT recording and a reading offer is a different parse of the line,
    so an answer to either of them settling a version question would report
    ownership of something nobody was asked about.
    """
    asked = one(version="Extended Mix", key="08A")
    shapes = {
        why: asked.question(why)["asks"]
        for why in (
            match.Why.VERSION_DIFFERS,
            match.Why.KEY_RELATIVE,
            match.Why.KEY_DIFFERS,
            match.Why.TITLE_APPROXIMATE,
            match.Why.READING_AMBIGUOUS,
        )
    }
    assert shapes == {
        match.Why.VERSION_DIFFERS: match.ASKS_ABOUT_VERSION,
        match.Why.KEY_RELATIVE: match.ASKS_ABOUT_KEY,
        match.Why.KEY_DIFFERS: match.ASKS_ABOUT_KEY,
        match.Why.TITLE_APPROXIMATE: match.ASKS_ABOUT_RECORDING,
        match.Why.READING_AMBIGUOUS: match.ASKS_ABOUT_READING,
    }
    # FOUR IDENTITIES, not five: the two key whys are one question wearing two
    # reasons, which is the one place two whys may share an item.
    identities = [asked.question(why) for why in shapes]
    assert len({tuple(sorted(found.items())) for found in identities}) == 4
    assert asked.question(match.Why.KEY_RELATIVE) == asked.question(
        match.Why.KEY_DIFFERS
    )
    # AND THE VERSION IS STILL IN IT, one field over, for the same reason. Two
    # versions of one recording at one key are two questions, and an identity
    # without this field makes them one item and one answer.
    version = match.Why.VERSION_DIFFERS
    assert asked.question(version)["version"] == "extended mix"
    assert one(version="Radio Edit", key="08A").question(version) != asked.question(
        version
    )


@pytest.mark.parametrize(
    "why",
    [
        match.Why.EXACT,
        match.Why.NOT_IN_LIBRARY,
        match.Why.VERDICT_ACCEPTED,
        match.Why.VERDICT_REJECTED,
        match.Why.TOMBSTONED,
        match.Why.CANDIDATE_GONE,
        match.Why.VERDICT_UNSPECIFIC,
    ],
)
def test_a_row_that_is_not_a_question_has_no_review_item_identity(why):
    """A DEFAULT HERE IS AN IDENTIFIER SOMEBODY COULD ANSWER.

    Matched and missing are results and never reach the queue, and the two
    stalled whys are written onto a row whose item was already found, so asking
    which question they are is a question with no answer. A shape mapping with a
    fallback would hand every one of them an item identity, and an item identity
    is the thing ``review resolve`` takes.
    """
    with pytest.raises(CratekitError) as excinfo:
        one(version="Extended Mix", key="08A").question(why)
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_key_folds_to_the_padded_form_and_an_unreadable_one_folds_to_nothing():
    """An absent key and an unparseable one behave identically, so they address alike."""
    assert match.key_token("8a") == match.key_token("08A") == "08A"
    assert match.key_token(None) == match.key_token("not a key") == ""


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: ownership is what the disk says
# ═══════════════════════════════════════════════════════════════════════════


def test_the_index_reads_the_filename_when_a_file_carries_no_tags(music):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.artist, row.title, row.version, row.key) for row in held] == [
        ("Aurora Bloom", "Sun Path", "Extended Mix", "08A")
    ]


def test_the_index_prefers_the_files_own_tags_over_a_misleading_filename(music, tmp_path):
    """The tag half of on-disk truth, against a real container.

    A file whose name was typed by hand and whose tags were written by the
    tagger disagree constantly, and the tags are what the file itself says. This
    uses a synthesized container rather than an empty one, because the reader
    that matters is the production reader and an empty file never reaches it.
    """
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


# ---------------------------------------------------------------------------
# The headed title tag: the head inside the TITLE TAG comes off the way the stem's does
# ---------------------------------------------------------------------------


def headed_tag(music: Path, tmp_path: Path, name: str, *, artist: str, title: str) -> Path:
    """A real container in the library carrying the given tags under ``name``.

    The live library writes the ``KEY - BPM - `` head into the title tag as well
    as the filename, the live system's convention, so a fixture that puts the
    head only in the name proves nothing about the reader this section is
    written against. The finding is the residual titled "The index takes the
    title tag with its head on, so no processed file resolves owned and every
    heart is offered or missing", cited by title for the reason ``split_title``
    gives.
    """
    return tagged_container(tmp_path, music / f"{name}.flac", artist=artist, title=title)


def test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches(
    music, tmp_path
):
    """The headed tag, first scenario. 9767 of 9868 files on the live volume carry
    the head inside the tag, and every one of them resolved offered or missing
    against a provider row spelling the plain title, because the tag was taken
    verbatim and only the stem was stripped."""
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
    """U213. Both sides read the bracketed title through one function, so they converge.

    Before, the provider row refused and the file indexed under an empty
    title, so the library's own copy could never be found by its title.
    """
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
    """The headed tag, third scenario. The head is exactly a key, a tempo and the
    terminator, so ``50`` after the terminator is the title's own first word."""
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
    """The collision the filename side already accepts, named rather than hidden.

    A release titled ``8A - 124 - Sun Path`` cannot be told from a head, on the
    tag any more than on the stem. ``strip_heads`` is not widened to guess, so the
    tag reads the way the stem has always read."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - 8A - 124 - Sun Path",
        artist="Aurora Bloom", title="8A - 124 - Sun Path",
    )
    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert index.versions(match.recording_token("Aurora Bloom", "8A - 124 - Sun Path")) == ()


def test_a_tag_that_is_only_a_head_falls_to_the_filename_the_way_an_empty_tag_does(
    music, tmp_path
):
    """The headed tag, fourth scenario: the head only tag, on the read side.

    A title tag of ``06A - 126 -`` says nothing about the title once the head is
    off, so it is treated as the absent tag it amounts to and the pair rule falls
    to the filename, which is what the reader does today for a file with no
    title tag at all. Before this unit the head itself became the title and the
    file was reachable by nothing."""
    headed_tag(
        music, tmp_path, "06A - 126 - Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title="06A - 126 -",
    )
    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.artist, row.title, row.key) for row in held] == [("Aurora Bloom", "Sun Path", "06A")]
    assert len(index) == 1


def test_a_plain_title_tag_is_untouched_by_the_head_strip(music, tmp_path):
    """The headed tag, the fourth scenario's other half. A title with no head reads as
    it always has, dash version included."""
    headed_tag(
        music, tmp_path, "08A - 124 - Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title="Sun Path - Radio Edit",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.version) for row in held] == [("Sun Path", "Radio Edit")]


def test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem(
    music, tmp_path
):
    """Some catalogue and scraper paths write the key and tempo at the END of a
    name, and the stem stripper removes that shape. The tag strips under the
    same rule, both ends, so the two surfaces cannot disagree about one file."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - Sun Path - 08A - 124",
        artist="Aurora Bloom", title="Sun Path - 08A - 124",
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [row.title for row in held] == ["Sun Path"]


def test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none(music, tmp_path):
    """The same bytes give the same key whether or not ``naming apply`` has run.

    The first draft of this unit stripped the tag's head and read nothing off
    it, and the review drove the cost: the file below indexed with no key, so a
    row wanting 07A matched cleanly, and after a rename padded the same head
    into the filename the index reported 06A and the same row disagreed. The
    naming verb already reads the head off either surface, so this reader now
    holds the same opinion. The stem still outranks the tag, and both outrank
    the ``initialkey`` tag."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - Sun Path", artist="Aurora Bloom", title="06A - 126 - Sun Path"
    )
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.key) for row in held] == [("Sun Path", "06A")]


def test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag(
    music, tmp_path
):
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
    """The trailing collision, named the way the leading one is.

    The stem stripper has always removed a head written as a suffix, because
    some catalogue paths write it there, and the tag now strips under the same
    rule. A release genuinely titled ``Room - 12B - 100`` indexes as ``Room``
    from either surface, and a provider row spelling the whole title reaches it
    through the approximate pass or not at all. Accepted for the tag as it was
    for the stem: one rule on both surfaces, so the two cannot disagree about
    one file."""
    headed_tag(
        music, tmp_path, "Aurora Bloom - Room - 12B - 100",
        artist="Aurora Bloom", title="Room - 12B - 100",
    )
    index = index_of(music)
    assert [row.title for row in index.versions(match.recording_token("Aurora Bloom", "Room"))] == ["Room"]
    assert index.versions(match.recording_token("Aurora Bloom", "Room - 12B - 100")) == ()


def test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template(
    music, tmp_path, cfg
):
    """The template the verbs hand the index is the library's, marker included,
    and the tag strips under the same one the stem does."""
    marker = cfg.naming.lossy_marker
    headed_tag(
        music, tmp_path, f"08A - 124 - {marker} Aurora Bloom - Sun Path",
        artist="Aurora Bloom", title=f"08A - 124 - {marker} Sun Path",
    )
    aware = match.index_library(music, template=match_cli.library_template(cfg))
    held = aware.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [row.title for row in held] == ["Sun Path"]


# ---------------------------------------------------------------------------
# The ISRC and the credited list: a held file resolves owned by the identity
# both sides carry, and by the primary artist's membership in the file's list
# ---------------------------------------------------------------------------


ISRC_RESIDUAL = (
    "The match engine never consults the ISRC, and a processed file's artist tag "
    "lists every credited artist, so a quarter of the hearts the library holds "
    "read missing or offered"
)


def credited(
    music: Path, tmp_path: Path, name: str, *, artist: str, title: str, isrc: str | None
) -> Path:
    """A real container the way the live library holds a processed file.

    The artist tag lists every credited artist, the title tag carries the head,
    and the ISRC is there when the provider delivered one. 1691 of 9868 files
    on the volume carry no ISRC tag, so ``isrc=None`` is a real population and
    not an edge. The finding is the residual titled in :data:`ISRC_RESIDUAL`,
    cited by title for the reason ``split_title`` gives.
    """
    fields = {"artist": artist, "title": title}
    if isrc is not None:
        fields["isrc"] = isrc
    return tagged_container(tmp_path, music / f"{name}.flac", **fields)


def burning(music: Path, tmp_path: Path, *, isrc: str | None = "USNRS2644532") -> Path:
    """The brief's file: ``Malive, Tito Azevedo, MRQZ`` against a row naming ``Malive``."""
    return credited(
        music, tmp_path, "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix)",
        artist="Malive, Tito Azevedo, MRQZ", title="04A - 126 - Burning (Extended Mix)",
        isrc=isrc,
    )


def row(*, artist: str, title: str, isrc: str | None, key=None) -> match.Wanted:
    """A provider row through the REAL reader, so the title is split the way a
    listing's is and the row carries what a provider row carries."""
    shaped = {"id": "301", "artist": {"name": artist}, "title": title, "isrc": isrc, "key": key}
    return match.read_row(shaped, origin=match.TIDAL, position=1)


def test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says(
    music, tmp_path
):
    """The first scenario. The credited list makes the recording token
    ``malive tito azevedo mrqz / burning`` against a wanted ``malive / burning``,
    so no text comparison can match, and both sides carry the ISRC."""
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
    """The second scenario. The same container with its ISRC removed is one of
    the 1691 files the ISRC rule cannot reach, and the credited list rule holds
    it: ``Malive`` is a member of ``Malive, Tito Azevedo, MRQZ`` and the folded
    title is the same."""
    burning(music, tmp_path, isrc=None)

    index = index_of(music)
    assert index.held_by_isrc("USNRS2644532") == ()
    # THE UNTAGGED FILE IS NOT INDEXED UNDER AN EMPTY KEY, or a row with no
    # ISRC would be held by every file with no tag.
    assert "" not in index.by_isrc
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")], index
    )
    (one_match,) = found.matches
    assert one_match.state is match.MatchState.MATCHED
    assert one_match.why is match.Why.CREDITED_EXACT
    assert len(one_match.paths) == 1


def test_the_primary_artist_need_not_be_first_in_the_credited_list(music, tmp_path):
    """The third scenario, ``Traumer, antraum, Anton :: Hyaku`` against a row
    naming ``antraum``, measured on the live library among the 26 held rows the
    product listed for download."""
    credited(
        music, tmp_path, "07A - 128 - Traumer, antraum, Anton - Hyaku",
        artist="Traumer, antraum, Anton", title="07A - 128 - Hyaku", isrc=None,
    )
    found = resolve([row(artist="antraum", title="Hyaku", isrc=None)], index_of(music))
    assert found.matches[0].state is match.MatchState.MATCHED


def test_a_different_recording_sharing_the_title_under_another_isrc_is_not_owned(
    music, tmp_path
):
    """The fourth scenario. Neither rule reaches it: the ISRC differs, and the
    row's artist is not a member of the file's list."""
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
    """The ISRC settles the recording and the version. It says nothing about the
    key, which is the library's own statement, so a row at the relative minor of
    the file's key is still a KEY_RELATIVE question and not a silent match."""
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
    """A hyphenated, lower case ISRC on the row is the same identity. The tag
    reader and the missing verb already fold this way, and a third spelling of
    the fold would be a third place for the two sides to disagree."""
    burning(music, tmp_path)
    found = resolve(
        [row(artist="Malive", title="Burning (Extended Mix)", isrc="us-nrs-26-44532")],
        index_of(music),
    )
    assert found.matches[0].why is match.Why.ISRC_EXACT


def test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone(
    music, tmp_path
):
    """The ISRC clause of the candidate labeller on its own. A compilation
    copy tagged ``Various Artists`` carries the row's ISRC and the row's title,
    and names no member the row names, so only the ISRC says it is the
    recording. The match asks about the key, and the candidate has to say the
    same rather than call the file a scored resemblance."""
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
    """The file side of the fold. A tag another tagger wrote hyphenated and
    lower case is the same identity as the provider's bare upper case one, and
    the index has to key it that way or the row never finds it."""
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
    """A catalogue number in the ISRC tag is a value that is not a recording's
    identity, and it is dropped the way ``source.isrc_for`` drops it, so a row
    carrying the same junk string does not match a file through it."""
    credited(
        music, tmp_path, "09A - 124 - Nova Reef - Tide",
        artist="Nova Reef", title="09A - 124 - Tide", isrc="CAT-001",
    )
    index = index_of(music)
    assert index.held_by_isrc(match.isrc_token("CAT-001")) == ()
    assert match.isrc_token("CAT-001") == ""
    # NOT IN THE MAP UNDER ANY SPELLING. A junk key nothing asks for is still a
    # key the next reader of this map would trust.
    assert index.by_isrc == {}
    found = resolve([row(artist="Someone Else", title="Tide", isrc="CAT-001")], index)
    assert found.matches[0].state is not match.MatchState.MATCHED


def test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one(
    music, tmp_path
):
    """The credited list rule finds the RECORDING. A file held at a different
    version is then the version question R11 asks, and its candidate says so,
    rather than the discovery class a scored hit would have been reported under."""
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
    """``Tito`` is not a member of ``Malive, Tito Azevedo, MRQZ``. A rule that
    matched on a substring would hand a solo artist every collaboration whose
    list contains their first name."""
    burning(music, tmp_path, isrc=None)
    found = resolve(
        [row(artist="Tito", title="Burning (Extended Mix)", isrc=None)], index_of(music)
    )
    assert found.matches[0].state is not match.MatchState.MATCHED


def test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing(music, tmp_path):
    """A file whose artist tag names one artist has a list of one, so the
    credited rule and the recording token agree, and the index counts one file."""
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
    """The review's shape, driven on a fixture and not seen on the live volume:
    a bootleg ingested with the original's tags, or one ISRC written across a
    release, carries the row's ISRC under another title. Called owned it would
    point the paths at the wrong recording and the heart would never be
    acquired, so it is asked about instead, with the file named."""
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
    """The ISRC settles the version however the file spells it, so the one
    question left is the key, and the candidate says the same thing the match
    says rather than a version question the engine already settled."""
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
    """Two copies, one tagged with the ISRC and one untagged that the recording
    token matches. The reason says the identity was carried, so the paths are
    the files that carry it, and the untagged copy's key does not join the
    disagreement over a row the ISRC settled."""
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
    """A hand built index carrying an empty key, which the walk never writes,
    still answers nothing to an empty token: the guard on the lookup side
    stands on its own and not only on the guard at the walk."""
    held = match.Owned(path=music / "x.flac", artist="A", title="T", version="", key=None)
    index = match.LibraryIndex(by_recording={}, by_isrc={"": (held,)})
    assert index.held_by_isrc("") == ()
    assert index.held_by_isrc(match.isrc_token(None)) == ()


def test_the_reader_opens_the_container_once_for_all_four_fields(music, tmp_path, monkeypatch):
    """The shape of the residual titled "The index reader opens every container
    three times, and the walk is the library". Four fields read through four
    opens is four parses per file over 9868 files on an external volume, and
    the ISRC read must not be a fourth one."""
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
    """The shape the source repo got right, asserted directly.

    A caller that forgets a FILTER gets a plausible answer. A caller that
    forgets a LOOKUP gets nothing and notices immediately.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert index.versions(match.recording_token("Nobody", "Nothing")) == ()


#: Everything that can read a rekordbox export. The package's own byte engine,
#: the standard library parser, and the third-party one. Matched as PREFIXES,
#: because ``xml`` and ``xml.etree.ElementTree`` are the same dependency and a
#: set of exact names is one dotted segment away from being switched off.
EXPORT_READERS = ("cratekit.write.rbxml", "xml", "lxml")


#: The calls that import a module from a STRING at run time. A guard reading only
#: import statements is one line away from being switched off by either of them.
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

    ``package`` is the dotted package the source lives in, which is what a
    relative import is relative TO. Without it ``from ..write import rbxml`` is a
    node with ``level=2`` and a module name of ``write``, matching nothing, and
    the guard returns an empty set for the one import shape a module inside the
    package is most likely to use.
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
    """Which export reader this source binds to, IN ANY SHAPE AND AT ANY DEPTH.

    BOUND THROUGH THE IMPORT GRAPH, not by attribute name. A guard matching a
    bare ``xml`` attribute passes for a module that imported the parser under
    another name, and fires on a correct module that happens to have a field
    called ``xml``. What is read here is what the source actually imported.

    THREE HOLES THE FIRST VERSION HAD, all of them proved by running the parser
    through them while the guard returned the empty set. It skipped every
    ``ImportFrom`` with a truthy ``level``, so ``from ..write import rbxml``
    passed. It read one file, so ``from cratekit.write import trees`` passed and
    ``trees`` imports ``rbxml`` at module scope; the old suite went further and
    asserted that shape was QUIET, which enshrined a live route as correct code.
    And it read import STATEMENTS, so ``importlib.import_module("lxml.etree")``
    passed.

    THE ROUTE THIS STILL CANNOT SEE, stated rather than pretended away: reading
    an export with ``open`` and a regular expression imports nothing at all. The
    rule is "do not read an export" and this function can only see "do not import
    a parser", so the last route is covered by a SECOND guard below, over string
    literals, and by the shape of the engine itself, which reads the disk only
    through ``index_library`` and only for suffixes in ``naming.AUDIO_EXTS``.
    Two partial guards that between them cover the rule beat one that claims to.
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


#: What an export looks like as TEXT, for the route no import guard can see. A
#: module that opens a collection file and picks it apart with a regular
#: expression has to name it or name its markup somewhere.
_EXPORT_TEXT = re.compile(r"\.xml\b|rekordbox|DJ_PLAYLISTS|<COLLECTION|<TRACK\b", re.IGNORECASE)


def _docstrings(tree: ast.AST) -> set[int]:
    """Every docstring node's id, so prose about an export is not a defect."""
    found: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
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
    """Lines where this source names an export file or its markup, docstrings aside.

    The complement of the import guard, and it exists because the rule is about
    READING an export rather than about importing a parser. ``open("Collection
    .xml")`` plus a hand-rolled regular expression reaches no parser at all and
    is the same defect: a derived document, believed over the disk.
    """
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
        # RELATIVE, at both depths a module in this package could write.
        "from ..write import rbxml\n",
        "from ..write.rbxml import root_node\n",
        "from . import rbxml\n",
        # TRANSITIVE. trees imports rbxml at module scope, so a module that
        # imports trees reaches the byte engine without naming it.
        "from cratekit.write import trees\n",
        "import cratekit.write.trees\n",
        # DYNAMIC, where the module name is a string and no import statement
        # mentions it at all.
        'importlib.import_module("lxml.etree")\n',
        '__import__("xml.etree.ElementTree")\n',
    ],
)
def test_the_export_guard_bites_on_every_import_shape(source):
    """P7's other half, the one that keeps getting skipped.

    Running a guard against correct code proves it is quiet. Running it against
    the EVASION is what proves it is a guard. An alias switched an armed
    countdown in this repository off with one keyword, and a dotted submodule
    would do the same to an exact-name set.

    The relative shapes are anchored at ``cratekit.write`` rather than at this
    unit's own package, because the point is the resolution, and a guard that
    resolved them to nothing returned the empty set for all three.
    """
    assert reaches_an_export_reader(source, package="cratekit.write")


@pytest.mark.parametrize(
    "source",
    [
        "from cratekit.core import naming, tags\n",
        "import hashlib\nimport unicodedata\n",
        "row = something.xml\n",
        '"""Prose about an xml export and about lxml, in a docstring."""\n',
        "from cratekit.core.review import DecisionStore\n",
        "from . import match\n",
    ],
)
def test_the_export_guard_stays_quiet_on_correct_code(source):
    """A guard that fires on correct code is a guard somebody routes around."""
    assert not reaches_an_export_reader(source)


@pytest.mark.parametrize(
    "source",
    [
        'raw = open("Collection.xml").read()\n',
        'path = root / "rekordbox.xml"\n',
        're.findall(r"<TRACK Location=", raw)\n',
    ],
)
def test_the_text_guard_bites_on_an_export_read_with_no_parser_at_all(source):
    """The route the import guard cannot see, guarded on its own terms.

    ``open`` plus a regular expression imports nothing. The rule is "do not read
    an export", so what is checked here is whether the module names one.
    """
    assert names_an_export_in_text(source)


@pytest.mark.parametrize(
    "source",
    [
        '"""Prose about a rekordbox.xml export, in a docstring."""\n',
        'suffix = ".flac"\n',
        'origin = "tidal"\n',
    ],
)
def test_the_text_guard_leaves_prose_and_ordinary_literals_alone(source):
    assert not names_an_export_in_text(source)


def test_the_match_engine_never_reaches_a_rekordbox_export():
    """Approach point 1: ownership is the disk, never a document that can lag.

    A stale export once reported an owned track unowned, and the run then
    acquired a track the library already held. The guard is that this module
    cannot reach an export reader at all, in any import shape, at any depth, and
    that it does not name an export as text either.
    """
    assert reaches_an_export_reader(MATCH_SOURCE.read_text()) == set()
    assert reaches_an_export_reader(MATCH_CLI_SOURCE.read_text()) == set()
    assert names_an_export_in_text(MATCH_SOURCE.read_text()) == []
    assert names_an_export_in_text(MATCH_CLI_SOURCE.read_text()) == []


def test_the_transitive_walk_actually_walks():
    """The hole that mattered most, proved against the REAL package.

    ``cratekit.write.trees`` imports the byte engine at module scope. A guard
    that reads one file returns the empty set for a module importing it, and the
    old suite asserted exactly that shape was quiet, which is a live route
    written down as correct code. Both halves are asserted here: that the second
    hop really does reach the engine today, so the fixture cannot rot into a
    tautology, and that the walk finds it.
    """
    assert "cratekit.write.rbxml" in _imports_of(
        _source_of("cratekit.write.trees"), package="cratekit.write"
    )
    assert reaches_an_export_reader("from cratekit.write import trees\n")


# ---------------------------------------------------------------------------
# A resolution that owns a row retires the question an earlier run asked about
# it. The residual titled "A review item outlives its question: a later
# resolution that owns the row leaves the version-match item open, and no
# verdict or predicate can retire it honestly".
# ---------------------------------------------------------------------------


def _adjudicated(store, wanted, index) -> match.TrackMatch:
    return match_cli.adjudicate(
        store,
        resolve([wanted], index),
        handler_key="acquire.match.run",
        suppresses=nothing_suppressed,
        suppression_id=no_identifier,
    ).matches[0]


def _ask_about_burning(store, music) -> match.TrackMatch:
    """Put the brief's row in front of a person: the library holds the radio
    edit and the row asks for the extended mix, so the row is a VERSION question
    and the queue gains one open item about it."""
    hold(music, "04A - 126 - Malive - Burning (Radio Edit)")
    asked = _adjudicated(
        store,
        row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
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
    """The brief's first scenario, under both rules the live measurement found:
    81 items under the ISRC rule and 4 under the credited one."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        burning(music, tmp_path, isrc=isrc_on_the_file)
        owned = _adjudicated(
            store,
            row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
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


def test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated(
    cfg, music, tmp_path
):
    """The brief's second scenario, at the seam. The same row resolved twice
    more against the owning library leaves one item, still retired."""
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
    """The brief's fourth scenario, at the seam. A rejection recorded before the
    ISRC file arrived stands, with its actor, after the rule owns the row."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        review.resolve(store, asked.item_id, review.Verdict.REJECTED, actor="phillip")
        burning(music, tmp_path)
        owned = _adjudicated(
            store,
            row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
            index_of(music),
        )
        assert owned.why is match.Why.ISRC_EXACT
        kept = review.get(store, asked.item_id)
        assert kept.verdict is review.Verdict.REJECTED
        assert kept.actor == "phillip"


def test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection(
    cfg, music, tmp_path
):
    """THE REVERSE DIRECTION, which the brief does not name and the third
    verdict makes reachable. The file carrying the ISRC is deleted, so the row
    is a version question again. Left standing, the machine's verdict reaches
    ``apply_verdict`` as "not accepted", which is a rejection nobody made: the
    row would report MISSING under ``verdict-rejected`` and acquisition would go
    and fetch a record the library may hold. So the machine revokes its own
    verdict and the question is asked again, open, with the fresh description."""
    with review.open_store(cfg) as store:
        asked = _ask_about_burning(store, music)
        carrying = burning(music, tmp_path)
        line = row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532")
        assert _adjudicated(store, line, index_of(music)).why is match.Why.ISRC_EXACT
        assert review.get(store, asked.item_id).verdict is review.Verdict.SUPERSEDED

        carrying.unlink()
        again = _adjudicated(store, line, index_of(music))
        assert (again.state, again.why) == (
            match.MatchState.NEEDS_REVIEW,
            match.Why.VERSION_DIFFERS,
        )
        assert again.item_id == asked.item_id
        reopened = review.get(store, asked.item_id)
        assert reopened.verdict is None
        assert reopened.actor == "acquire.match.run"
        assert [one.item_id for one in review.list_items(store)] == [asked.item_id]


def test_a_retired_question_whose_row_goes_missing_keeps_the_verdict(cfg, music, tmp_path):
    """THE COST RECORDED, not the feature. The residual titled "A superseded
    verdict outlives its rule when the row goes missing rather than back to a
    question": the reopen path revokes the machine's verdict only when there
    is something to ask, and a missing row passes through, so the item keeps
    a rule that no longer holds. Clearing it here would put an open question
    about a missing row in front of a person. Pinned so the choice is made on
    purpose when the residual is picked up, and the assertion flips with it."""
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
    """``OWNING_RULES`` is a positive set. A row matched because a PERSON
    accepted it is a matched row under ``verdict-accepted``, and that path must
    not walk the retiring side: the item it would find is the very one carrying
    the acceptance, which ``supersede`` leaves alone anyway, but the guard is
    the recognition and not the second layer."""
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
            store,
            row(artist="Malive", title="Burning (Extended Mix)", isrc="USNRS2644532"),
            index_of(music),
        )
        assert (applied.state, applied.why) == (
            match.MatchState.MATCHED,
            match.Why.VERDICT_ACCEPTED,
        )
        kept = review.get(store, asked.item_id)
        assert kept.verdict is review.Verdict.ACCEPTED
        assert kept.actor == "phillip"


def test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue():
    """THE FIX THAT LANDS ON THE CHECKING PATH. The retirement lives inside
    ``adjudicate``, and four of its five callers opened the review store only
    for a question, so an owned row reached it from ``match run`` alone and
    from none of the verbs that filed the live items. Every module that calls
    ``adjudicate`` now names the shared predicate, and a new caller that gates
    on the needs-review state alone fails here."""
    callers = [
        path
        for path in (REPO_ROOT / "src" / "cratekit").rglob("*.py")
        if "match_cli.adjudicate(" in path.read_text(encoding="utf-8")
    ]
    assert len(callers) >= 4, [path.name for path in callers]
    for path in callers:
        text = path.read_text(encoding="utf-8")
        # AS MANY GATES AS CALLS. The missing pass calls ``adjudicate`` twice,
        # and a module that names the predicate once could still gate its
        # other call on the needs-review state alone.
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
    """The retiring side enumerates shapes, and each must be the identity the
    asking side would have filed under, or a retirement looks for an item
    under an identifier nothing ever wrote to."""
    line = one(artist="Aurora Bloom", title="Sun Path", version="Extended Mix", key="08A")
    identities = line.questions()
    assert [identity["asks"] for identity in identities] == list(match.QUESTION_SHAPES)
    assert len({json.dumps(identity, sort_keys=True) for identity in identities}) == 4
    for why in (
        match.Why.KEY_DIFFERS,
        match.Why.KEY_RELATIVE,
        match.Why.VERSION_DIFFERS,
        match.Why.TITLE_APPROXIMATE,
        match.Why.READING_AMBIGUOUS,
    ):
        assert line.question(why) in identities


def test_the_verb_lists_a_retired_question_only_when_asked_for_everything(
    cfg, music, tmp_path
):
    """End to end through ``match run`` and ``review list``: the item a first
    run filed leaves the open list when a second run owns the row, and reads
    the third verdict with its rule under ``--all``."""
    hold(music, "04A - 126 - Malive - Burning (Radio Edit)")
    listing = write_list(
        tmp_path,
        json.dumps({
            "list": 1,
            "origin": match.TIDAL,
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


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: the three states
# ═══════════════════════════════════════════════════════════════════════════


def test_an_exact_version_is_matched_and_asks_nobody(music):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.why is match.Why.EXACT
    assert found.candidates == ()


def test_a_track_owned_only_as_a_different_remix_needs_review_and_names_the_difference(music):
    """AE8, and the whole reason this unit exists.

    The source system treats this as owned, so the user finds out at the gig
    that the file on the drive is not the record they queued.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.VERSION_DIFFERS
    assert [c.version for c in found.candidates] == ["Someone Remix"]
    assert found.candidates[0].difference is match.Why.VERSION_DIFFERS


def test_a_relative_key_disagreement_surfaces_rather_than_picking_one(music):
    """The trap: 8A and 8B share a wheel position and share every note.

    Anything comparing wheel numbers calls them the same key, and they are the
    minor and the major recording of the same material.
    """
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
    """THE STATE DEPENDED ON THE SORT ORDER OF THE MUSIC TREE.

    ``exact[0]`` read one file out of a list the Candidate docstring itself says
    holds several. With an untagged copy and a keyed copy of the same version
    both present, the answer was whichever the directory walk returned first:
    matched when the unkeyed one sorted first, needs-review when the keyed one
    did, for identical content. Renaming a folder changed the answer.

    Parametrized over both orders so this cannot pass by luck the way the old
    behaviour did.
    """
    (music / first_folder).mkdir()
    (music / "B sorted").mkdir()
    (music / first_folder / "Aurora Bloom - Sun Path.flac").write_bytes(b"")
    (music / "B sorted" / "03A - 124 - Aurora Bloom - Sun Path.flac").write_bytes(b"")
    found = resolve([one(key="08A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.KEY_DIFFERS


def test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present(music):
    """8A and 8B look like agreement to everything comparing wheel positions.

    So when one held copy is the relative and another disagrees outright, the
    slug that names the trap is the one reported. It was reachable only by luck
    before, because it lost to whichever file sorted first.
    """
    hold(music, "08B - 124 - Aurora Bloom - Sun Path")
    (music / "03A - 124 - Aurora Bloom - Sun Path.mp3").write_bytes(b"")
    found = resolve([one(key="08A")], index_of(music)).matches[0]
    assert found.why is match.Why.KEY_RELATIVE


def test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries(music):
    """The other half of the same root, and the one a person sees.

    Grouping by version alone built one candidate per version showing the FIRST
    file's key while carrying every file's path, so a person shown 08A accepted a
    set including 03A. A candidate is one version at one key.
    """
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
    """Grouping by version alone would collapse them onto one.

    A person accepting one would then be accepting the other, because both sets
    of paths would ride on a single option identifier.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Pathway")
    hold(music, "08A - 124 - Aurora Blooms - Sun Path")
    found = resolve([one(title="Sun Path Way")], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert len({c.candidate_id for c in found.candidates}) == len(found.candidates) >= 2


def test_two_files_of_one_version_are_one_candidate_carrying_two_paths(music):
    """A lossless copy and its lossy twin are one answer to one question.

    Asking twice would be the smaller cost. The larger one is that a person
    accepting one of them settles nothing about the other, so the same record
    comes back as a question on the next run.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    (music / "08A - 124 - Aurora Bloom - Sun Path (Someone Remix).mp3").write_bytes(b"")
    found = resolve([one(version="Extended Mix")], index_of(music)).matches[0]
    assert len(found.candidates) == 1
    assert len(found.candidates[0].paths) == 2


def test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording(music, cfg):
    """R21's marker is part of the NAME, never part of the record.

    A template that cannot strip it makes the marked copy a different recording
    from its lossless twin, which is how the source system put a pair of
    duplicates in one playlist. The marker text is config's (S3), so the verb
    hands the engine a template built from it.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    marked = music / f"08A - 124 - {cfg.naming.lossy_marker} Aurora Bloom - Sun Path.mp3"
    marked.write_bytes(b"")

    plain = match.index_library(music)
    assert len(plain.versions(match.recording_token("Aurora Bloom", "Sun Path"))) == 1

    aware = match.index_library(music, template=match_cli.library_template(cfg))
    assert len(aware.versions(match.recording_token("Aurora Bloom", "Sun Path"))) == 2


def test_a_tombstoned_version_is_suppressed_while_another_remix_resolves_normally(music):
    """AE17. R36 in one test.

    The suppressed one is reported rather than counted missing, and it is not
    silently dropped. The other remix of the same recording is unaffected,
    because a tombstone is about one exact version.
    """
    deleted = match.version_identity(artist="Aurora Bloom", title="Sun Path (Someone Remix)")

    def suppresses(kind, identity):
        return kind == match.TOMBSTONE_KIND and dict(identity) == deleted

    result = resolve(
        [one(version="Someone Remix"), one(version="Другой Mix")],
        index_of(music),
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

    The library holds the original mix, a tombstone stands over the extended mix,
    the list asks for the extended mix. Consulting the store before the version
    question made all three arrays come back empty with one warning and exit
    zero: the person was never asked whether the cut they own is the record, and
    the track was invisible to any consumer reading matched or missing.
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
    """Ownership is on-disk truth, so a tombstone standing over a held file is stale.

    Reporting suppressed here would tell a person the library does not hold a
    record it plainly does. The verb reports the disagreement instead.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    found = resolve([one()], index_of(music), suppresses=lambda _k, _i: True).matches[0]
    assert found.state is match.MatchState.MATCHED


def test_the_tombstone_lookup_has_no_default(music):
    """The permissive default this repository has already shipped once.

    A caller that forgot the tombstone store would re-acquire exactly what
    somebody deleted on purpose, with every test green. There is no default to
    forget: leaving it out is a TypeError.
    """
    with pytest.raises(TypeError):
        match.resolve_all([one()], index_of(music))  # type: ignore[call-arg]


def test_one_match_identifier_never_appears_in_two_arrays_of_one_payload(music):
    """A consumer keying by id silently dropped one of them.

    The identifier excluded the key and the STATE includes it, so a list carrying
    one row with a key and one without emitted the same id under ``matched`` and
    under ``needs_review``.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    payload = resolve([one(), one(key="03B")], index_of(music)).payload()
    rows = [row for state in payload.values() for row in state]
    assert len(rows) == 2
    assert len({row["id"] for row in rows}) == 2
    assert len(payload["matched"]) == len(payload["needs_review"]) == 1


def test_at_most_the_declared_number_of_approximate_candidates_is_offered(music):
    """The constant caps CANDIDATES, which is what its comment promises.

    It was spent only as the scorer's recording limit, and one recording can be
    held as several versions at several keys, so a person could be handed far
    more options than the number the comment names.
    """
    # THREE recordings, each held as three versions at three keys. The scorer
    # returns three recordings, well inside its own limit, and they expand to
    # nine candidates: the number a person is handed had nothing capping it.
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
    """IT TRUNCATED AN ALPHABETICALLY SORTED LIST, so it dropped the best answer.

    ``_candidates_for`` re-sorted on the folded tokens, destroying the score
    order the approximate pass had just produced, and the cap then took the first
    five. With "Sun Path Alt" scoring 91.3 as five versions and "Sun Pathx"
    scoring 97.7 as one, the person was shown five wrong answers and the right
    one was withheld. Rejecting then re-acquires a track the library already
    holds, which is what the approximate pass exists to prevent.

    And a silent truncation looks exactly like an offer of everything the library
    resembles, so the count that was kept back is reported.
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


def test_the_withheld_warning_survives_onto_the_run_that_actually_acquires(
    cfg, music, tmp_path
):
    """IT WAS SILENT ON THE ONE RUN ITS OWN SENTENCE IS ABOUT.

    The warning's reason for existing is that a person who rejects a truncated
    offer "has rejected answers they were never shown, and the run then acquires
    a track the library already holds". It was emitted only for NEEDS_REVIEW,
    which is the run where nothing is acquired. ``apply_verdict`` carries the
    withheld count onto the rejected MISSING row, and the warning never looked at
    that state, so run one exited 12 saying candidates were kept back, the person
    rejected, and run two exited 0 with an acquisition option, no pending action
    and an empty warnings array.
    """
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
    """A REJECTION REACHES MISSING BY A ROAD RESOLUTION NEVER WALKS.

    Consulting the store last is right, but the rejection branch built its
    acquisition options without consulting it at all, so a question about a
    version standing under a tombstone came back as a missing row telling the
    next verb to go and get it, at exit zero. The step text says in as many
    words "reject to acquire the version the list asked for", and a warning is
    not a declared input to that verb.
    """
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


def test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source(
    music, tmp_path
):
    """Artist and title fall back AS A PAIR, or the identity is from nowhere.

    Falling back field by field gave a file with a title tag and no artist tag an
    identity assembled from two sources, matching neither its tags nor its name,
    and the identity is what ownership is looked up by.
    """
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"title": "Sun Path"})
    target = music / "08A - 124 - Aurora Bloom - Wrong Title.flac"
    shutil.copy2(probe, target)

    index = index_of(music)
    assert index.versions(match.recording_token("Aurora Bloom", "Wrong Title"))
    assert index.versions(match.recording_token("Aurora Bloom", "Sun Path")) == ()


def test_a_present_artist_tag_is_never_thrown_away_by_the_pair_fallback(music, tmp_path):
    """THE PAIR RULE'S OWN FAILURE, which round one introduced and did not test.

    A file with an artist tag, no title tag, and a name carrying no separator has
    no filename artist to fall back to, so falling back as a pair set the artist
    to nothing. The file is then found by no list naming its artist: a held track
    reports missing and is acquired again, which is the same cost the field-wise
    rule had, arriving from the other side.
    """
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"artist": "Aurora Bloom"})
    shutil.copy2(probe, music / "SunPath.flac")

    held = index_of(music).versions(match.recording_token("Aurora Bloom", "SunPath"))
    assert [row.artist for row in held] == ["Aurora Bloom"]


def test_the_payload_carries_exactly_the_fields_the_declared_surface_requires():
    """DERIVED from the schema, so the two cannot drift apart.

    The payload keys come from ``PAYLOAD_STATES`` and the surface's required
    fields come from U5's declaration. Writing the three names a second time in
    this test would prove only that somebody typed them consistently twice.
    """
    declared = set(output.schema_document("match")["required"])
    assert set(match.MatchResult(()).payload()) == declared
    assert {str(state) for state in match.PAYLOAD_STATES} == declared
    assert str(match.MatchState.SUPPRESSED) not in declared


@pytest.mark.parametrize("source", [MATCH_SOURCE, MATCH_CLI_SOURCE], ids=lambda p: p.name)
def test_no_set_or_mapping_literal_in_this_unit_has_a_duplicate_element(source):
    """The shape a green suite cannot see, hunted by parsing rather than running.

    Every other test iterates the RUNTIME object, where a duplicate collapsed at
    parse time is already gone. This repository has shipped that defect once
    with the whole suite passing. A frozenset literal is covered too, because the
    walk reaches the set inside the call.
    """
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.Set, ast.Dict)):
            keys = node.elts if isinstance(node, ast.Set) else node.keys
            constants = [k.value for k in keys if isinstance(k, ast.Constant)]
            duplicates = sorted({k for k in constants if constants.count(k) > 1})
            assert not duplicates, f"line {node.lineno}: duplicate elements {duplicates}"


def test_the_duplicate_literal_hunt_can_actually_see_one():
    """A guard nobody proved bites is a comment (P7, other direction).

    Both literal shapes, including the frozenset call the real module uses, so
    a walk that stopped reaching inside the call would fail here rather than
    passing quietly over the module it is pointed at.
    """
    for shape in ('X = {"a", "b", "a"}', 'X = frozenset({"a", "a"})', 'X = {"a": 1, "a": 2}'):
        node = next(
            n for n in ast.walk(ast.parse(shape)) if isinstance(n, (ast.Set, ast.Dict))
        )
        keys = node.elts if isinstance(node, ast.Set) else node.keys
        values = [k.value for k in keys if isinstance(k, ast.Constant)]
        assert len(values) != len(set(values))


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: one internal shape, three sources (R13)
# ═══════════════════════════════════════════════════════════════════════════

#: One playlist expressed three ways. The provider carries the version in its
#: own field; the public playlist API carries it inside the title; pasted text
#: carries it inside the title too and has no identifier at all.
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
#: THE SPELLING THE PUBLIC PLAYLIST API ACTUALLY USES. Its ``name`` carries the
#: version after a dash and not in brackets, which is the one shape the readers
#: did NOT agree on, and the old parity test used the bracketed spelling, the one
#: shape where they already did.
SPOTIFY_DASH_ROWS = [
    {"track": {"id": "sp1", "name": "Sun Path - Someone Remix",
               "artists": [{"name": "Aurora Bloom"}]}},
    {"track": {"id": "sp2", "name": "Tide Line", "artists": [{"name": "Nova Reef"}]}},
]
TEXT_LINES = "1. Aurora Bloom - Sun Path (Someone Remix)\n\n# a comment\nNova Reef - Tide Line\n"


@pytest.mark.parametrize("spotify", [SPOTIFY_ROWS, SPOTIFY_DASH_ROWS], ids=["bracketed", "dashed"])
def test_the_three_readers_produce_one_shape(spotify):
    """BOTH spellings of the public playlist API, not only the easy one.

    ``Sun Path - Someone Remix`` is what that API ships, the module's own
    docstring says so, and only the bracketed groups were read. The row resolved
    missing against a library holding the exact file, the approximate pass did
    not rescue it (72.4 against a floor of 82), and the identical row through the
    provider reader resolved matched. That is the three-reader convergence
    property, which is the reason this test exists, failing at the point it was
    written for.
    """
    from_tidal = match.read_tidal_tracks(TIDAL_ROWS)
    from_spotify = match.read_spotify_items(spotify)
    from_text = match.read_text_lines(TEXT_LINES)
    for read in (from_tidal, from_spotify, from_text):
        assert [(w.artist, w.title, w.version_key) for w in read] == [
            ("Aurora Bloom", "Sun Path", match.version_token("Someone Remix")),
            ("Nova Reef", "Tide Line", ""),
        ]
    # THE MATCH CONVERGES AND THE ADDRESS DELIBERATELY DOES NOT. A listing is
    # addressed by the title it actually spelled, because the other side of that
    # hash reads a library row verbatim, so a dash-spelled list and a provider row
    # are two addresses for one version. The consult covers both, which is what
    # makes a tombstone recorded from either spelling findable from the other.
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
        # A HEAD WORD carries a one-word tail, because the public playlist API
        # ships exactly these three on their own and a year is not a vocabulary
        # word.
        ("Sun Path - Remastered 2011", ("Sun Path", "Remastered 2011")),
        ("Sun Path - Remastered", ("Sun Path", "Remastered")),
        ("Sun Path - Nightwave Remix (Radio Edit)", ("Sun Path", "Nightwave Remix Radio Edit")),
        # NOT a version. A parser that split on any trailing dash would invent a
        # record nobody released, which is why the split is vocabulary-guarded.
        ("Sun - Rise", ("Sun - Rise", "")),
        ("Tide Line - Reprise Of Nothing", ("Tide Line - Reprise Of Nothing", "")),
        ("- Remix", ("- Remix", "")),
    ],
)
def test_a_dash_qualifier_is_read_only_when_it_names_a_version(name, expected):
    assert match.split_title(name) == expected
    # The bracket-only splitter is unchanged, so the hazard it was written
    # against stays written down where somebody will find it.
    assert match.split_version("Sun - Rise") == ("Sun - Rise", "")


@pytest.mark.parametrize(
    "name",
    [
        # THE REPRISE CLASS, which is the sharpest of these. An album reprise is a
        # separate composition, so splitting it reframes "the library holds
        # nothing like this" into "the library holds this record as a different
        # version", and accepting that reports ownership of a track the library
        # does not hold.
        "Sgt. Pepper's Lonely Hearts Club Band - Reprise",
        "Ziggy Stardust - Reprise",
        "Hurt - Reprise",
        # Every other one-word vocabulary tail that is really the end of a title.
        "Long - Live",
        "Studio 54 - Live",
        "Pump Up The Volume - Extended",
        "Nice Up - Dub",
        "Beat It - Demo",
        "Sunset - Acoustic",
        # FOLDING INFLATED THE WORD COUNT: the inner hyphen became a space, so a
        # one-word tail counted as two and split. The count is taken raw now.
        "Sun - Re-Mix",
        # A Latin tail on a non-Latin title is the same exposure.
        "曲 - Live",
    ],
)
def test_a_legitimate_title_ending_in_a_vocabulary_word_is_not_split(name):
    """THE ENTIRE EXPOSURE OF A VOCABULARY RULE, and round one had no case for it.

    The negatives before this all used a tail OUTSIDE the vocabulary, which tests
    that a word not on the list is not on the list. What matters is a real title
    whose final word IS on it. A bare one-word qualifier is genuinely ambiguous,
    so the string reader leaves it alone and the LIBRARY settles it instead: see
    ``test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it``,
    which is where "left alone" stops meaning "reported missing".
    """
    assert match.split_title(name) == (name, "")


#: THE ONE-WORD TAILS THE PUBLIC PLAYLIST API REALLY SHIPS. Every one of them is
#: a whole class rather than an example, and refusing the class outright was the
#: second round's regression: with the library holding "Sun Path (Instrumental)"
#: the dash form scored 76.4 against a floor of 82 and reported MISSING with an
#: acquisition option, which is verbatim the defect the first round closed.
ONE_WORD_TAILS = ("Live", "Instrumental", "Acoustic", "Dub", "Demo", "Extended", "Remix")


@pytest.mark.parametrize("tail", ONE_WORD_TAILS)
def test_a_bare_one_word_tail_offers_the_reading_the_string_rule_declined(tail):
    """BOTH READINGS EXIST, and neither is picked by the string.

    ``split_title`` keeps the conservative one, because "Ziggy Stardust -
    Reprise" and "Sun Path - Live" are the same shape and no rule over the
    characters can tell a version from the end of a title. What must not happen
    is the reading being thrown away, which is what left the whole class
    unreachable.
    """
    assert match.split_title(f"Sun Path - {tail}") == (f"Sun Path - {tail}", "")
    assert match.split_ambiguous(f"Sun Path - {tail}") == ("Sun Path", tail)


@pytest.mark.parametrize(
    "name",
    [
        "Sun - Rise",
        "Tide Line - Reprise Of Nothing",
        "Sun Path (Nightwave Remix)",
        "Sun Path - Nightwave Remix",
        "Sun Path - Remastered",
        "- Remix",
    ],
)
def test_a_title_with_only_one_reading_offers_no_second_one(name):
    """The ambiguity is narrow on purpose.

    A tail outside the vocabulary is not a version in either reading; a tail
    ``split_title`` already reads is not ambiguous; and a head that is empty is
    not a title. Offering a second reading for any of those would widen the
    library-confirmed rule into a general licence to re-split a title.
    """
    assert match.split_ambiguous(name) is None


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Sun - Rise", ("Sun - Rise", "")),
        ("Sing - Sing - Sing", ("Sing - Sing - Sing", "")),
        ("The Man - Machine", ("The Man - Machine", "")),
        ("Come - Alive", ("Come - Alive", "")),
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
    """Everything except provenance is derived from the recording.

    The assertion is two-sided on purpose: the rows agree once ``source`` is
    dropped, AND ``source`` is the only key that differs. Comparing a projection
    alone would pass for a row that had quietly stopped carrying anything.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    index = index_of(music)
    payloads = [
        resolve(read, index).payload()
        for read in (
            match.read_tidal_tracks(TIDAL_ROWS),
            match.read_spotify_items(SPOTIFY_ROWS),
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
        {"artist": ["Two Names"], "title": "Listy"},
        {"artists": ["Two Names"], "title": "Listy"},
        {"artist": [{"name": "Two Names"}], "title": "Listy"},
        {"artists": "Two Names", "title": "Listy"},
    ],
    ids=[
        "list-under-artist",
        "list-under-artists",
        "objects-under-artist",
        "string-under-artists",
    ],
)
def test_every_shape_a_row_spells_its_artists_in_reads_the_same(row):
    """A list under ``artist`` read as NO ARTIST AT ALL, and nothing said so.

    The object branch excluded lists and there was no fallback, so the row hashed
    to an identity matching nothing and a track the library plainly held was
    reported missing at score 50, beside the ``artists`` spelling of the same
    track landing matched. Two spellings of one shape must not be two answers.

    The BARE STRING under ``artists`` is the same defect one shape further out,
    and it cost more, because refusing an unreadable row is at least a refusal
    while failing to read an artist that is present is silent.
    """
    assert match.read_tidal_tracks([row])[0].artist == "Two Names"


def test_a_row_that_names_neither_an_artist_nor_a_title_is_refused(music):
    """POSITIVE RECOGNITION, which the text reader had and the provider path did not.

    Three things went wrong without it, all of them quietly. Two rows carrying
    nothing but an identifier folded to one match identifier, so two list entries
    became one row and a consumer keying by id lost one. An anonymous row
    resolved matched against any junk file whose name folds to nothing, so an
    unreadable row was reported owned. And nothing warned about either.
    """
    with pytest.raises(match.UnreadableList) as excinfo:
        match.read_tidal_tracks([{"id": "a"}, {"id": "b"}])
    assert excinfo.value.line == 1


@pytest.mark.parametrize(
    "row",
    [
        {"id": "sp1", "name": "Sun Path"},
        {"id": "sp1", "name": "Sun Path", "artists": []},
        {"id": "sp1", "artists": [{"name": "Aurora Bloom"}]},
    ],
    ids=["no-artist-key", "empty-artists", "no-title"],
)
def test_a_row_naming_only_one_half_of_a_record_is_refused_too(row):
    """BOTH HALVES, and demanding only one of them was the same hole re-opened.

    The guard refused a row only when artist AND title were both absent, so an
    artist-less row was accepted and given an identity that is not unique to the
    thing it identifies. ``read_text_lines`` already refuses a line with no
    artist by name and says why in prose, so the provider path was applying a
    weaker rule than the one this module's own docstring cites.
    """
    with pytest.raises(match.UnreadableList) as excinfo:
        match.read_spotify_items([row])
    assert excinfo.value.line == 1


def test_two_rows_sharing_a_title_and_naming_two_artists_are_two_records(
    cfg, music, tmp_path
):
    """THE IDENTITY THAT WAS NOT UNIQUE TO THE THING IT IDENTIFIED.

    Two public playlist rows spelling their artists as a bare string, ``Aurora
    Bloom`` and ``Nova Reef``, both read as no artist at all, both hashed to the
    identity of a title with nothing beside it, and both resolved MATCHED against
    one unrelated file carrying a title tag and no artist tag. Two different
    recordings were reported owned, pointing at a file that is neither, under one
    identifier, so one of the two vanished from any payload keyed by id, at exit
    zero, with no warning and no question.

    Both halves are asserted: the artists now READ, and the two rows are two
    records rather than one.
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
    """Driven through the verb, where the collapse was invisible.

    A junk file is present too, because with one there the anonymous rows did not
    merely collapse, they resolved matched against it.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: the verb, and the split U11 settled
# ═══════════════════════════════════════════════════════════════════════════


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
    """U11's split, driven rather than read.

    A matched track and a missing one both run through the verb and the queue
    stays empty. The static half of this lives in tests/test_review_queue.py and
    cannot see what the verb does at run time.
    """
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
    """THE NAME QUANTIFIES OVER THE OPTIONS, so the options are what it asserts.

    It used to assert a why, a null review item and an empty queue, and nothing
    at all about options, because there were none: the row carried an empty
    candidate list, an empty path list and nothing else, while the verb's
    docstring said it carried its acquisition options as data. The name was false
    the day it was written.

    Whether a missing row belongs in the queue instead is the residual titled
    "Two briefs disagree about whether a missing track is a review item", a
    product decision reserved for a person. What is settled either way is that the
    sentence has to be true.
    """
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
    # Every other row's options are its own, so a consumer cannot read one row's
    # option identifier and acquire another row's record.
    assert options[0]["id"] != match.acquisition_options(one())[0].option_id


def test_an_acquisition_option_names_the_exact_version_and_never_a_looser_one():
    """An option meaning "some other cut will do" is the silent substitution.

    The version travels in the query and in its own field, so a source is asked
    for the record the list asked for. A code, when the list carried one, comes
    first because a provider that has it does not have to guess.
    """
    wanted = match.Wanted(
        artist="Aurora Bloom", title="Sun Path", version="Someone Remix", isrc="GBAAA0000001"
    )
    options = match.acquisition_options(wanted)
    assert [option.how for option in options] == [match.BY_ISRC, match.BY_SEARCH]
    assert options[0].query == "GBAAA0000001"
    assert options[1].query == "Aurora Bloom Sun Path (Someone Remix)"
    assert all(option.version == "Someone Remix" for option in options)


def test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get(
    cfg, music, tmp_path
):
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
    """Driven through the verb, which is where the divergence actually cost.

    With the remix owned, the row ``{"origin": "spotify", "name": "Sun Path -
    Nightwave Remix"}`` resolved MISSING against a library holding the file, and
    the identical row through the provider reader resolved matched. The
    approximate pass did not rescue it: 72.4 against a floor of 82.
    """
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
    assert (
        envelope["data"]["matched"][0]["id"] == through_provider["data"]["matched"][0]["id"]
    )


@pytest.mark.parametrize("tail", ONE_WORD_TAILS)
def test_a_one_word_version_tail_is_asked_about_and_never_re_acquired(
    cfg, music, tail
):
    """THE WHOLE ONE-WORD CLASS, PINNED, and not one example of it.

    The second round refused to split a bare one-word tail, and the parity test
    that was supposed to catch that only ever exercised "Someone Remix", two
    words, so it stayed green while seven real qualifiers stopped converging.
    With the library holding the file EXACTLY, the public playlist row resolved
    MISSING with an acquisition option for a track already on the shelf, at exit
    zero. That is the failure this asserts is gone, and it is asserted as what it
    is: the row is not missing and carries nothing to go and fetch.

    WHAT IT NO LONGER ASSERTS IS THAT THE STATE CONVERGES, because the third
    round bought that convergence by letting the library decide a parse and then
    reporting the result as a MATCH. "Long - Live" is in this file's own list of
    legitimate titles ending in a vocabulary word, so a library holding "Long
    (Live)" made the run report ownership of a record nobody had checked. A
    source that carries its version in a field of its own has said where the
    boundary is; a source that spelled one string has not. So the provider row
    matches and the two dash rows ask, once, and everything the STRING can settle
    still converges: the two rows that spelled the same characters agree on the
    state, the reason, the identifier and the item.
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
    # NOT ACQUIRED, for any of the three, which is the whole point of the class.
    for found in (provider, spotify, text):
        assert found.state is not match.MatchState.MISSING
        assert found.acquisitions == ()
    assert (provider.state, provider.why) == (match.MatchState.MATCHED, match.Why.EXACT)
    for found in (spotify, text):
        assert (found.state, found.why) == (
            match.MatchState.NEEDS_REVIEW,
            match.Why.READING_AMBIGUOUS,
        )
        assert [candidate.version for candidate in found.candidates] == [tail]
    assert spotify.match_id == text.match_id
    assert spotify.question_identity == text.question_identity


@pytest.mark.parametrize(
    "held",
    [
        # The library holds the other reading, so there is something to ask about.
        "08A - 124 - Aurora Bloom - Sun Path (Live)",
        # And at a different key, so the CANDIDATE changes while the question
        # does not. An identity that moved with the library would make these two
        # runs two different questions.
        "03A - 124 - Aurora Bloom - Sun Path (Live)",
    ],
    ids=["held", "held-at-another-key"],
)
def test_the_identifier_of_an_ambiguous_row_never_moves_with_the_library(
    cfg, music, tmp_path, held
):
    """A MATCH IDENTIFIER IS A FUNCTION OF THE LIST, and it had become one of the disk.

    ``_reading_the_library_confirms`` rewrote the wanted track, and every
    identifier downstream is derived from what resolution carries, so one list
    line produced ``mt_477c70a711c8071a`` on a machine holding "Sun Path (Live)"
    and ``mt_dd324b5ffa6b8362`` on a machine holding nothing. ``review export``
    and ``review import`` exist to move a decision BETWEEN machines and that
    class could not travel: the importing machine looked up an identifier the
    exporting one never wrote, found nothing, and asked again.

    Worse on ONE machine, because renaming the confirming file flipped the
    reading back, so the answer somebody had already given was looked up under an
    identity nobody had ever been asked. It was not found, a fresh question was
    offered, and the resolved item stayed in the store listed by nothing and
    warned about by nothing. ``CANDIDATE_GONE`` is the state built for exactly
    "the library changed under a recorded verdict" and it was unreachable,
    because reaching it needs the item to be FOUND first.
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
    # THE ITEM IDENTITY IS ASSERTED ACROSS THE TWO LIBRARIES THAT ASK THE SAME
    # QUESTION, which is the property, rather than across a library that asks
    # nothing. The empty library produces a MISSING row, and a result has no
    # review item to compare: see
    # ``test_a_row_that_is_not_a_question_has_no_review_item_identity``. Held at
    # 08A and held at 03A are one question with two candidates, and the two
    # parameters of this test are exactly those two libraries.
    assert confirmed.question_identity == match.question_identity(
        "Aurora Bloom", "Sun Path - Live", "", None, match.Why.READING_AMBIGUOUS
    )
    # The reported title is the one the LIST spelled, in both, because the
    # identifier and the payload have to agree about which record this is.
    assert (confirmed.wanted.title, confirmed.wanted.version) == ("Sun Path - Live", "")


def test_a_verdict_survives_the_rename_that_flips_the_reading(
    cfg, music, tmp_path
):
    """THE STRANDING, DRIVEN, and the state that was being bypassed.

    A person answers the question, then the confirming file is re-tagged or
    renamed so the library no longer holds that reading. With the identity
    derived from the library, the second run asked a NEW question and the
    answered item sat resolved and unreachable. With it derived from the list,
    the same item is found, the candidate it named is no longer on offer, and the
    run says so: CANDIDATE_GONE, under the original item identifier, which is a
    row a person can act on.
    """
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


def test_the_dashed_one_word_spelling_is_asked_about_rather_than_acquired(
    cfg, music, tmp_path
):
    """Driven through the verb, where the regression actually cost.

    "Instrumental" is the sharpest of the class because it scores 76.4, below the
    approximate floor, so nothing rescued it: the run reported the track missing,
    carried an acquisition option, warned about nothing and exited zero. The row
    is a QUESTION now rather than a match, and the assertions that matter are the
    negative ones: nothing is missing and nothing is offered to acquire.

    THE RUN EXITS ZERO AND SAYS SO, which is a decision rather than the old
    silence. Gating on this class costs a measured 14 of 68 cells in the
    library-state table, all in the same direction, and ``- Edit``, ``- Mix`` and
    ``- Live`` are three of the commonest spellings a public playlist ships, so a
    real library run against real playlists would exit 12 on almost every run and
    fill a queue faster than a person empties it. What R11 forbids is a question
    nobody is TOLD about, so the price of not gating is paid on the warning
    channel and in the needs-review array, and both are asserted here.
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
    # NOT SILENT. The question is named on the warning channel, carries the item
    # a person answers it under, and names the verb that shows it to them.
    warned = [w for w in envelope["warnings"] if w["code"] == match_cli.READING_UNSETTLED]
    assert [(w["item"], w["remedy"]) for w in warned] == [
        (row["review_item"], match_cli.REVIEW_VERB)
    ]
    assert queue_items(cfg)[0].item_id == row["review_item"]


def test_an_ungated_question_still_gates_once_its_verdict_cannot_be_applied(
    cfg, music, tmp_path
):
    """THE ESCAPE FROM THE UNGATED CLASS, which is the half that could go wrong.

    A reading question does not stop the run. A reading question somebody
    ANSWERED, whose candidate the library has since stopped offering, is a
    different fact: the item is RESOLVED, so ``review list`` does not show it and
    ``review resolve`` refuses it, and the only way forward is an act nobody
    performs unless told. ``apply_verdict`` rewrites the why into one of
    ``STALLED``, which is not in ``UNGATED``, so the run blocks and names the verb
    that can act. Without that, not gating this class would have hidden the one
    state that genuinely needs a person.
    """
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
    """PROPERTY 2, APPLIED TO THE PARSE, which is where it was not being applied.

    "Long - Live" is in this file's own list of legitimate titles whose last word
    is a version word, and a library holding "Long (Live)" resolved it MATCHED,
    why EXACT, pathing that file, at exit zero. If the list meant a composition
    called "Long - Live" and the library holds a live cut of a different record
    called "Long", the run reports ownership of a track the library does not
    hold, which is the failure the whole unit exists to remove and the one a
    person finds out about at the gig.

    There is no evidence separating "Long - Live" from "Sun Path - Live", so this
    is a rule about the class and not about one title, and the rule is the one
    property 2 already states: a generous read costs one question, never one
    wrong join.
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
        # THE REPRISE CLASS, which is what refusing the split was defending. An
        # album reprise is a separate composition, so the library holding the
        # record it is a reprise OF is not evidence that the tail is a version.
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
    """WHAT THE SECOND ROUND WAS DEFENDING, kept, at the level that decides it.

    The bar for reading a bare tail as a version is the highest evidence there
    is: the library holds the head AT THAT VERSION. Holding the head at some
    other version is not evidence about this question at all, so it must not
    reframe "the library holds nothing like this" into "the library holds this
    record as a different version" and offer the base recording as a candidate.
    A person accepting that reports ownership of a track the library does not
    hold, which is the wrong join this unit exists to remove.

    The title stays whole, which is what a later reader and the acquisition query
    both read.

    IT MUST NOT EVEN BECOME THE AMBIGUITY QUESTION, and asserting only that it is
    not matched missed that. Weakening the bar from "holds the head at that
    version" to "holds the head at all" left the reprise class resolving to
    READING_AMBIGUOUS with an empty offer: not a match, not a version difference,
    and so invisible to both of the assertions below it. A question with nothing
    on it is a person being asked to choose from no answers about a record the
    library plainly says nothing about.
    """
    hold(music, f"08A - 124 - {held}")
    found = resolve(match.read_text_lines(f"{line}\n"), index_of(music)).matches[0]
    assert found.wanted.title == expected_title
    assert found.wanted.version == ""
    assert found.why is not match.Why.VERSION_DIFFERS
    assert found.why is not match.Why.READING_AMBIGUOUS
    assert found.state is not match.MatchState.MATCHED


def test_the_ambiguity_offer_names_the_version_the_other_reading_means(cfg, music):
    """THE OFFER IS AS NARROW AS THE EVIDENCE, and it was as wide as the head.

    The evidence for reading "Sun Path - Live" as a version is that the library
    holds "Sun Path" at exactly "Live". Offering the head's OTHER versions
    alongside asks a person to accept a cut this list never mentioned, on the
    strength of a parse they are being asked about in the same breath, and an
    acceptance is what puts a file in the matched array with its path. Every
    other test in this class holds the head at one version, where a candidate
    list filtered to the confirming version and one that is not are the same
    list.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]
    assert found.why is match.Why.READING_AMBIGUOUS
    assert [candidate.version for candidate in found.candidates] == ["Live"]


def test_the_reading_the_list_actually_spelled_wins_when_the_library_holds_both(
    cfg, music
):
    """A TIE GOES TO WHAT THE LIST SAID, and the tie is reachable.

    A library can hold a record called "Sun Path - Live" AND a live version of a
    record called "Sun Path". Both readings are then confirmed, and the one that
    must win is the conservative one, because it is the string the list actually
    spelled and the other is this module's guess about it. Without that order the
    guess wins whenever the library happens to hold both, and the person is told
    they own a file they were not asking about.
    """
    whole = hold(music, "08A - 124 - Aurora Bloom - Sun Path - Live")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    found = resolve(
        match.read_text_lines("Aurora Bloom - Sun Path - Live\n"), index_of(music)
    ).matches[0]
    assert found.state is match.MatchState.MATCHED
    assert found.wanted.title == "Sun Path - Live"
    assert found.paths == (str(whole),)


def test_a_version_question_becomes_an_addressable_item_with_its_candidates(
    cfg, music, tmp_path
):
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
    """R12's negative half, asserted against the FILESYSTEM.

    Derived by walking the library root rather than by naming the files this
    verb happens to write today, so a spreadsheet added beside them later is
    covered on the day it appears.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\nNova Reef - Tide\n")
    drive(["match", "run", path])
    written = [p for p in cfg.library.root.rglob("*") if p.is_file()]
    assert not [p for p in written if p.suffix.lower() in {".csv", ".tsv"}]


def test_a_run_over_an_answered_question_reports_matched_and_writes_nothing(
    cfg, music, tmp_path
):
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


def test_a_rejected_question_makes_the_track_missing_rather_than_matched(
    cfg, music, tmp_path
):
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


def test_an_accepted_candidate_that_has_since_gone_is_not_reported_matched(
    cfg, music, tmp_path
):
    """Ownership is on-disk truth, and a verdict does not put a file back.

    The track returns as a question naming the item, because clearing somebody's
    verdict is their act. What must never happen is a matched row pointing at a
    file that is not there.
    """
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


def test_an_acceptance_naming_no_candidate_is_applied_only_when_there_is_one(
    cfg, music, tmp_path
):
    """The queue allows a verdict with no option, so this state is reachable.

    With one candidate on offer, "accepted" can only mean that one. With
    several, it says the library has the record and does not say which version,
    and taking all of them reports three copies on the strength of one
    unspecific yes, which is the silent join in a different costume.
    """
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
    """ONE ANSWER SILENTLY DECIDED TWO MORE, in the permissive direction.

    The key decides the state but was not in the item identity, so every key
    question about one recording plus version was the same stored item. Accept a
    candidate at 08A and the next run asking 03B, the relative minor of the owned
    03A and the exact trap this module names, came back matched with no question
    at all. So did an unrelated 11B.
    """
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
        ("03B", "k03b.json", match.Why.KEY_RELATIVE),
        ("11B", "k11b.json", match.Why.KEY_DIFFERS),
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
    """THE COST OF THE RULE, RECORDED RATHER THAN DISCOVERED, and it is the cheap side.

    The identity of a question is a function of the LIST LINE. The key is in it,
    for the reason ``question_identity`` gives, so a line that names a key and a
    line that does not are two lines and two items. That is a real loss: this
    used to be one item, because the key was put in only when the question turned
    out to be about the key.

    IT WAS BOUGHT WITH SOMETHING WORSE. Which question gets asked is decided by
    what is on that machine's disk, so the old rule let the LIBRARY decide the
    identity: one line opened two different items on two machines under one
    ``match_id``, and an exported answer imported cleanly into an identifier the
    receiving machine never looks up. What R13 actually promises is that the same
    line through the three readers is one question, and that is asserted here
    beside the cost.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    plain = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n", "plain.txt")

    def keyed(code: str | None, name: str) -> str:
        row = {"id": "1", "title": "Sun Path", "version": "Extended Mix",
               "artist": {"name": "Aurora Bloom"}}
        if code is not None:
            row["key"] = code
        return write_list(
            tmp_path,
            json.dumps({"list": 1, "origin": match.TIDAL, "tracks": [row]}),
            name,
        )

    _code, first = drive(["match", "run", plain])
    item_id = first["data"]["needs_review"][0]["review_item"]
    _code, with_key = drive(["match", "run", keyed("08A", "keyed.json")])
    assert with_key["data"]["needs_review"][0]["review_item"] != item_id
    assert len(queue_items(cfg)) == 2

    # THE PROMISE THAT SURVIVES: the same line, through a different reader, is
    # the same question. Nothing here carries a key, so nothing here splits.
    _code, unkeyed = drive(["match", "run", keyed(None, "unkeyed.json")])
    assert unkeyed["data"]["needs_review"][0]["review_item"] == item_id
    assert len(queue_items(cfg)) == 2


def test_a_verdict_travels_between_two_machines_that_hold_different_versions(
    cfg, music, tmp_path
):
    """THE PAIR OF VERBS THIS IDENTITY EXISTS FOR, driven across two libraries.

    ``review export`` and ``review import`` move a decision between machines, and
    the property that makes them work is that ONE QUESTION about one list line
    has one identity wherever it is asked. The identity used to be gated on
    values the library supplied, so two machines holding different COPIES of the
    same version opened two items under one ``match_id``: the import reported the
    row inserted with no conflict, the receiving machine looked its own question
    up under the other identifier, found nothing, and asked again. The answer was
    imported and ignored, and nothing anywhere said so.

    THE TWO LIBRARIES HERE HOLD DIFFERENT FILES AND ASK THE SAME QUESTION, which
    is the case the property is about. Both hold another version of the record,
    so both put a VERSION question; one holds a different other version from the
    other, at a different key, under a different name. Nothing about any of that
    reaches the identity.

    Driven at the seam rather than asserted on the object, because the object
    agreeing is what an earlier round proved about ``match_id`` while this went
    on failing underneath it.
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
            store,
            resolve(line, index),
            handler_key="acquire.match.run",
            suppresses=nothing_suppressed,
            suppression_id=no_identifier,
        ).matches[0]

    # MACHINE A holds the extended cut, at 03A.
    machine_a = library("03A - 124 - Aurora Bloom - Sun Path (Extended)", "a")
    # MACHINE B holds the instrumental, at 08A. A different file, a different
    # version, a different key, and the same question.
    machine_b = library("08A - 124 - Aurora Bloom - Sun Path (Instrumental)", "b")

    with review.open_store(cfg, path=tmp_path / "a.sqlite3") as store_a:
        asked = settled(machine_a, store_a)
        assert asked.why is match.Why.VERSION_DIFFERS
        review.resolve(
            store_a, asked.item_id, review.Verdict.REJECTED, actor="phillip"
        )
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

    assert (answered.state, answered.why) == (
        match.MatchState.MISSING,
        match.Why.VERDICT_REJECTED,
    )
    assert answered.item_id == asked.item_id
    assert asked.match_id == answered.match_id


def test_a_key_question_answered_elsewhere_does_not_settle_a_version_question(
    cfg, music, tmp_path
):
    """THE COST OF TELLING THE TWO QUESTIONS APART, DRIVEN AND RECORDED.

    One list line resolves to a KEY question on a machine holding that exact
    version at another key, and to a VERSION question on a machine holding only
    another version. Those are two questions: the first asks "is your 03A copy of
    this remix the record", the second asks "is your extended cut the record",
    and the answers are not interchangeable. So they are two items, an answer
    exported from the first does not settle the second, and the second machine
    asks its own question.

    THE ROUND THAT MADE THEM ONE ITEM PAID FOR IT IMMEDIATELY, which is why this
    is the direction chosen: an acceptance of the version question came back
    MATCHED against the relative minor the moment the library gained one, with
    the accepted file gone from ``paths``. The residual titled "A question
    answered on one machine does not settle a different question about the same
    line" records what is given up.
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
            store,
            resolve(line, index),
            handler_key="acquire.match.run",
            suppresses=nothing_suppressed,
            suppression_id=no_identifier,
        ).matches[0]

    keyed = library("03A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)", "k")
    versioned = library("08A - 124 - Aurora Bloom - Sun Path (Extended)", "v")

    with review.open_store(cfg, path=tmp_path / "k.sqlite3") as store_k:
        asked = settled(keyed, store_k)
        assert asked.why is match.Why.KEY_DIFFERS
        review.resolve(
            store_k, asked.item_id, review.Verdict.REJECTED, actor="phillip"
        )
        document = review.export_document(store_k)

    with review.open_store(cfg, path=tmp_path / "v.sqlite3") as store_v:
        fresh = settled(versioned, store_v)
        assert fresh.why is match.Why.VERSION_DIFFERS
        assert fresh.item_id != asked.item_id
        review.import_document(store_v, document, actor="importer")
        after = settled(versioned, store_v)

    # THE IMPORTED ANSWER IS NOT APPLIED, and the row stays a question rather
    # than being decided by something nobody asked here.
    assert (after.state, after.why) == (
        match.MatchState.NEEDS_REVIEW,
        match.Why.VERSION_DIFFERS,
    )
    assert after.item_id == fresh.item_id
    # ONE ``match_id`` ACROSS BOTH, which is the property that did not change:
    # the two machines agree about which RECORD this row is, and disagree only
    # about which question they were able to put.
    assert asked.match_id == after.match_id


def test_a_run_blocked_by_an_unapplicable_verdict_names_the_verb_that_can_act(
    cfg, music, tmp_path
):
    """IT PARKED AT PENDING_HUMAN FOREVER NAMING A REMEDY NOBODY COULD RUN.

    The item stays RESOLVED, so ``review list`` returns nothing and ``review
    resolve`` refuses with review-already-resolved, while the run keeps exiting
    12 and pointing at ``review.list``. A caller reading the exit code and then
    the named verify verb is told "blocked" and "nothing to do" at once, and the
    only escape, ``review clear``, was never named. Reachable by deleting or
    retagging one file.
    """
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
    # And the item identifier reaches a consumer on the channel built for codes,
    # rather than only in a sentence.
    stalled = [w for w in second["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]
    assert [w["item"] for w in stalled] == [item_id]
    assert stalled[0]["remedy"] == match_cli.CLEAR_VERB

    # THE ESCAPE ACTUALLY WORKS, which is what makes naming it worth anything.
    code, _ = drive(["review", "clear", item_id])
    assert code == int(ExitCode.OK)
    code, third = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert third["data"]["needs_review"][0]["why"] == str(match.Why.VERSION_DIFFERS)
    assert third["pending_human_action"]["verify_verb"] == match_cli.REVIEW_VERB


def stall(cfg, music, tmp_path, how_many: int) -> tuple[list[str], dict]:
    """Leave ``how_many`` questions carrying a verdict that cannot be applied.

    Accept a candidate for each, then take the accepted file away and put a
    different remix in its place, which is the shape a retag or a move produces.
    """
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
    return [
        step.split()[1:] for step in pending["steps"] if step.startswith("crate ")
    ]


@pytest.mark.parametrize("how_many", [1, 2, 5])
def test_every_printed_remedy_is_a_command_that_actually_runs(
    cfg, music, tmp_path, how_many
):
    """WITH TWO OR MORE STALLED ITEMS THE PRINTED REMEDY WAS NOT A COMMAND.

    The identifiers were joined into one line, and the verb takes a single
    positional, so the shell answered "unrecognized arguments" and exit 2. That
    is the exact defect class this unit says it removes: a pending action naming
    a remedy nobody can execute is the printed instruction the field replaces.
    Reachable whenever a person accepted candidates for two or more tracks and
    then retagged or moved files.

    Parametrized over one, two and five, because the old shape passed at one.
    Each step is DRIVEN, not pattern-matched, so "it looks like a command" is not
    what is being asserted.
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
    # And the run is genuinely unblocked afterwards, which is what makes the
    # remedy worth printing.
    code, after = drive(["match", "run", str(tmp_path / f"stall{how_many}.txt")])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert not [
        row for row in after["data"]["needs_review"]
        if row["why"] in {str(match.Why.CANDIDATE_GONE), str(match.Why.VERDICT_UNSPECIFIC)}
    ]


def test_the_pending_action_counts_questions_rather_than_rows_in_both_halves(
    cfg, music, tmp_path
):
    """One sentence counted two ways is arithmetic nobody can follow.

    Round one applied "counted by question" to the total and left the stalled
    part a row count, so one line pasted twice reported "1 tracks ... need a
    person; 2 of them carry a verdict that could not be applied", and then
    printed one identifier for the two.
    """
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
    assert len(
        [w for w in stalled["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE]
    ) == 1


def test_a_verdict_this_build_cannot_read_leaves_the_item_answerable(
    cfg, music, tmp_path
):
    """The hazard of a stored value that freezes an item out of every route.

    An item carrying a verdict from a newer build must still be presented as a
    question, because the way out of a wrong decision is to clear it, and an
    item nobody can reach cannot be cleared.
    """
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
    """R13 and R12 in one assertion, and the reason identity excludes the ref.

    The same playlist arrives as provider rows and then as pasted text. If the
    item identity carried the provider's own identifier, the second run would
    open a second question and a person would answer the same thing twice.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    hold(music, "08A - 124 - Nova Reef - Tide Line")
    provider = write_list(
        tmp_path,
        json.dumps({"list": 1, "origin": match.TIDAL, "tracks": TIDAL_ROWS}),
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
    """R36: skipped by acquisition, and never omitted silently.

    The tombstone is recorded through the decision store U11 shipped, under the
    kind and identity this module declares, which is the pairing the register
    holds the deletion unit to.
    """
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
    """THE SEAM, DRIVEN, which is where round one's parity proof was worth nothing.

    The tombstone is recorded exactly as the deletion pass records it: the row's
    artist and its Title column verbatim, through the real decision store. Then
    a list naming the same record runs through the real dispatcher.

    Round one recomposed the title into round parentheses before hashing, so this
    reported ``missing=1``, ``warnings=[]``, exit 0, and an acquisition option
    telling the next verb to go and fetch the exact version somebody had deleted,
    for five of these seven spellings. That is verbatim the failure the module's
    own docstring describes.
    """
    store = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    recorded = store.record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", row_title),
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


def test_a_tombstone_over_a_held_version_is_reported_rather_than_hidden(
    cfg, music, tmp_path
):
    hold(music, "08A - 124 - Aurora Bloom - Sun Path")
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=match.version_identity(artist="Aurora Bloom", title="Sun Path"),
        actor="test",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path\n")
    _code, envelope = drive(["match", "run", path])
    assert len(envelope["data"]["matched"]) == 1
    assert [w["code"] for w in envelope["warnings"]] == [match_cli.TOMBSTONE_OVER_OWNED]


def test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults(
    cfg, music, tmp_path
):
    """THE REPORT WAS NARROWER THAN THE RULE IT REPORTS ON.

    Suppression asks the store under every spelling of one version; this warning
    asked under ``track.identity``, a single spelling. So a tombstone recorded
    from the row ``Sun Path (Live)``, standing over a file the library still
    holds, left NO trace at all when the list spelled the version ``Sun Path
    [Live]``: the row reported matched, the warnings array was empty, and the
    stale record stayed invisible until somebody hit it during a deletion.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    path = write_list(tmp_path, "Aurora Bloom - Sun Path [Live]\n", "stale.txt")
    _code, envelope = drive(["match", "run", path])

    assert len(envelope["data"]["matched"]) == 1
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


def test_a_deletion_of_the_plain_record_never_withholds_the_credited_one(
    cfg, music, tmp_path
):
    """THE DIRECTION THE DESIGN REJECTS, and the consult was widening into it.

    A featured credit is dropped from the MATCHING title because it names a
    performer, and the composed fallback then asked the store under ``sun path``,
    the identity of the plain no-qualifier record, which is a spelling the
    recorder never writes for the credited row. ``tombstone_fold`` argues the
    cost asymmetry out loud: a missed suppression re-acquires something and
    reports it, while an over-eager one silently withholds music somebody wants,
    and those two costs are not comparable.

    Both directions are asserted, because a fix that simply stopped consulting
    would have re-broken the case the widening was for.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path"),
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
        ("Sun Path [ft. Mira] [Nightwave Remix]", ""),
        ("Sun Path (feat. Mira)", "Nightwave Remix"),
    ],
)
def test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit(
    cfg, music, tmp_path, row_title, row_version
):
    """THE SHAPE THE VERBATIM CONSULT CANNOT REACH, driven from the real recorder.

    The residual titled "A deleted track the tombstone consult cannot reach is
    listed for download" measured this reporting MISSING, which the list verb
    then handed to a download. The listing names the version and no guest, the
    way a provider with a version field spells it.
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
        "Sun Path (feat. Zed) (Nightwave Remix)",
        "Sun Path (Daybreak Remix)",
        "Sun Path",
    ],
)
def test_a_credited_deletion_withholds_nothing_but_its_own_version(
    cfg, music, tmp_path, listed
):
    """THE OVER EAGER DIRECTION, asserted against the real recorder.

    Another guest, another remix, and the bare recording are three things nobody
    deleted. Each stays missing, with no warning, under a standing companion.
    """
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
    """The plain cut and the credited cut were both deleted, so the listing that
    spelled no credit is answered by a tombstone AND by a companion. It is
    reported under the tombstone, the record a person wrote for that row."""
    plain = deleted(cfg, "Sun Path (Nightwave Remix)", content_id="9002")
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Nightwave Remix)\n", "both.txt")
    _code, envelope = drive(["match", "run", path])
    assert [w["suppression"] for w in envelope["warnings"]] == [plain.suppression_id]


def test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion():
    """A CREDIT WITH NOTHING IN THE TITLE TO SHOW IT. The reader keeps the first
    artist and drops the rest, so a row billing Zed beside the main artist reads
    exactly like the row that credits nobody, and would be withheld by a deletion
    of the recording that credits Mira. Under ``artists`` and under ``artist``,
    as mappings and as strings, because those are one shape spelled four ways."""
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
    """BUILT BY HAND MEANS NOBODY LOOKED. The verb builds one from a held file,
    whose title the index has already taken the credits off, so "no credit in
    it" is an absence of looking and not an absence of credits."""
    by_hand = match.Wanted(artist="Aurora Bloom", title="Sun Path", version="Nightwave Remix")
    assert by_hand.suppression_spellings
    assert by_hand.uncredited_spellings == ()


def test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale(
    cfg, music, tmp_path
):
    """THE REPORT THAT WOULD TELL A PERSON TO LIFT A DELETION THE DISK SAYS
    NOTHING ABOUT. The Mira cut was deleted and the Zed cut is held. A companion
    has had its guest taken out, so it cannot say which of the two it stands
    for, and neither the matched row nor the offered file may report it as a
    stale record over a held file."""
    deleted(cfg, "Sun Path (feat. Mira) (Nightwave Remix)")
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (feat. Zed) (Nightwave Remix)")
    body = "Aurora Bloom - Sun Path (Nightwave Remix)\nAurora Bloom - Sun Path (Daybreak Remix)\n"
    _code, envelope = drive(["match", "run", write_list(tmp_path, body, "zed.txt")])

    assert [one["version"] for one in envelope["data"]["matched"]] == ["Nightwave Remix"]
    assert [one["version"] for one in envelope["data"]["needs_review"]] == ["Daybreak Remix"]
    assert [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED] == []


def test_a_deletion_of_the_plain_record_writes_no_companion(cfg, music, tmp_path):
    """THE GUARD ON THE RECORDING SIDE. One deletion of a row with no credit is
    one record, so there is nothing under the companion kind for anything to
    reach, and the credited listing stays missing as it always did."""
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
    """THE CLAIM THAT THIS WIDENS NOTHING, measured rather than argued.

    While the credited row is HELD, the listing that never spelled the guest
    resolves matched, because a credit names a performer and comes off the
    matching title. So the engine already calls the two one version, and the
    companion makes the deleted state agree with the held one. A different remix
    is a question while held, never a match, and plain missing once deleted.
    """
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
        ("Sun Path", "Sun Path (Original Mix)"),
        ("Sun Path (Original Mix)", "Sun Path"),
        ("Sun Path (Original Mix)", "Sun Path [Original Version]"),
    ],
)
def test_the_two_spellings_of_no_qualifier_at_all_reach_each_other(
    cfg, music, tmp_path, recorded_row, listed
):
    """BOTH DIRECTIONS, because ``_NULL_VERSIONS`` already calls them one version.

    ``version_token`` folds "Original Mix" to nothing, so the match treats the
    two as one version and would have asked a person to confirm a track against
    itself otherwise. The tombstone consult did not: a list spelling ``Sun Path
    (Original Mix)`` never reached a tombstone recorded from the row ``Sun
    Path``, so the version was re-acquired at exit zero. It was recorded in no
    residual either.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", recorded_row),
        actor="deletion",
    )
    path = write_list(tmp_path, f"Aurora Bloom - {listed}\n", "null.txt")
    code, envelope = drive(["match", "run", path])

    assert code == int(ExitCode.OK)
    assert envelope["data"]["missing"] == []
    warnings = [w for w in envelope["warnings"] if w["code"] == match_cli.SUPPRESSED_WARNING]
    assert [w["suppression"] for w in warnings] == [recorded.suppression_id]


def test_a_tombstone_store_that_cannot_be_read_refuses_rather_than_matching(
    cfg, music, tmp_path
):
    """Fail CLOSED, and this verb takes its snapshot before it does any work.

    Treating an unreadable store as empty would re-acquire exactly what somebody
    removed on purpose, which is the sentence the store's own refusal carries.
    The snapshot being taken up front is what makes the refusal arrive before a
    single track has been resolved rather than partway through a list.
    """
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


# ── the list document, recognized positively ─────────────────────────────────


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
    """A leading bracket counts as JSON, not only a leading brace.

    Otherwise this falls through to the line reader, ``["Artist - Title"]``
    splits on the separator perfectly happily, and a document of the wrong shape
    becomes one track with punctuation in its name. Same defect as reading a
    wrong document as an empty one, wearing a different hat.
    """
    with pytest.raises(CratekitError):
        match_cli.read_list(
            Path(write_list(tmp_path, '["Aurora Bloom - Sun Path"]', "arr2.json"))
        )


def test_a_null_tracks_field_is_refused_rather_than_read_as_an_empty_list(tmp_path):
    """An absent array and an empty one are different facts."""
    assert _refusal(tmp_path, json.dumps({"list": 1, "origin": "text", "tracks": None}))


def test_a_key_this_build_does_not_read_is_refused_rather_than_ignored(tmp_path):
    """A misspelled 'tracks' otherwise parses as a valid document holding none."""
    cause = _refusal(
        tmp_path, json.dumps({"list": 1, "origin": "text", "trakcs": ["A - B"]})
    ).cause
    assert cause.detail["unknown"] == ["trakcs"]


def test_an_origin_this_build_cannot_read_is_refused(tmp_path):
    assert _refusal(tmp_path, json.dumps({"list": 1, "origin": "vinyl", "tracks": []}))


def test_a_track_of_the_wrong_shape_is_refused_with_its_position(tmp_path):
    cause = _refusal(
        tmp_path, json.dumps({"list": 1, "origin": match.TIDAL, "tracks": ["A - B"]})
    ).cause
    assert cause.detail["position"] == 1


@pytest.mark.parametrize(
    "given",
    ["https://example.invalid/playlist/1", " https://example.invalid/playlist/1"],
    ids=["plain", "leading-space"],
)
def test_a_web_address_is_refused_with_its_own_sentence(tmp_path, given):
    """Fetching a playlist needs a session and pagination; the intake verbs own both.

    The leading space is not hypothetical: it survives a copy and paste, it is
    legal in a filename so it cannot be refused on its own, and anchoring the
    scheme at the first character sent the address back out as "no such file or
    directory", which is the exact failure the check exists to stop.
    """
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
    """The document reader refuses this in three ways and the text path did not.

    "Every track on your list is owned" and "your list was empty" are the same
    three empty arrays and the same exit zero. The document reader already says
    so twice, once about a null ``tracks`` and once about a newer format, in the
    words "reading it anyway would report a clean match over tracks it could not
    see". The plain-text path made exactly that report.
    """
    path = write_list(tmp_path, body, "blank.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_a_document_that_declares_an_empty_track_array_is_still_a_list(cfg, tmp_path):
    """A positive declaration of zero tracks HAS said something.

    That is the distinction the null-tracks refusal already draws in its own
    words, so the refusal above is about a file with nothing readable in it
    rather than about the number zero.
    """
    path = write_list(
        tmp_path, json.dumps({"list": 1, "origin": match.TEXT, "tracks": []}), "empty.json"
    )
    assert match_cli.read_list(Path(path)) == ()


def test_a_document_row_carrying_a_line_break_is_refused_with_its_array_position(tmp_path):
    """The rows were joined with newlines and re-split, so three things went wrong.

    A refusal cited a line number in a string nobody has, a row that happened to
    carry a newline silently became two tracks, and the array's length stopped
    being the number of tracks read.
    """
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
        tmp_path,
        json.dumps({"list": 1, "origin": match.TEXT, "tracks": TEXT_LINES.splitlines()}),
        "lines.json",
    )
    plain = write_list(tmp_path, TEXT_LINES, "plain.txt")
    assert match_cli.read_list(Path(document)) == match_cli.read_list(Path(plain))


def test_the_naming_template_the_index_uses_is_the_declared_one():
    """A second template here would read the library by a convention nobody writes."""
    assert naming.NameTemplate().head_fields == ("key", "bpm")


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: the identity of a QUESTION, and the coefficients nothing was reading
# ═══════════════════════════════════════════════════════════════════════════


def keyed_list(tmp_path, name: str, **fields) -> str:
    """One provider row as a list document, so the key travels in its own field."""
    row = {"id": "1", "title": "Sun Path", "artist": {"name": "Aurora Bloom"}}
    row.update(fields)
    return write_list(
        tmp_path,
        json.dumps({"list": 1, "origin": match.TIDAL, "tracks": [row]}),
        name,
    )


def test_a_version_answer_never_settles_a_key_question_about_the_same_line(
    cfg, music, tmp_path
):
    """THE DEFECT THE LAST ROUND INTRODUCED, DRIVEN THROUGH THE REAL VERBS.

    Putting the LIST's key on every question stopped the identity moving with the
    disk and collapsed two questions onto one item. The whole sequence, in one
    library, with one list line:

    The list asks for ``Sun Path`` at 03A. The library holds only the extended
    mix, so the run asks a VERSION question. Somebody answers it: yes, my
    extended mix is that record. The run reports MATCHED with the extended mix in
    ``paths``, which is right.

    Then the library gains the plain cut at 03B, the RELATIVE MINOR of the key
    the list asked for and the exact trap ``Why.KEY_RELATIVE`` exists to catch.
    With one item for both questions, the next run applied the version answer to
    a key question nobody had asked: MATCHED, exit zero, no warning, ``paths``
    carrying the 03B file, and the extended mix the person had actually pointed
    at gone from them.

    So the third run has to be a QUESTION, under a DIFFERENT item, and the file
    the person accepted must not be reported as this record at a key nobody
    checked.
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
    # BOTH ITEMS ARE IN THE STORE, one answered and one open, which is what two
    # questions look like.
    assert len(queue_items(cfg)) == 2


def test_two_versions_of_one_recording_are_two_questions_and_two_answers(
    cfg, music, tmp_path
):
    """THE SAME COLLAPSE ONE FIELD OVER, and nothing was asserting this either.

    ``Sun Path (Extended Mix)`` and ``Sun Path (Radio Edit)`` are two records. The
    library holds neither and holds a third version, so each line is its own
    version question. With the version out of the item identity they are one
    item: answer about the extended mix and the radio edit comes back MATCHED,
    carrying the paths of whatever the first answer named.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    both = write_list(
        tmp_path,
        "Aurora Bloom - Sun Path (Extended Mix)\nAurora Bloom - Sun Path (Radio Edit)\n",
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
    """THE TWO KEY WHYS ARE ONE ITEM BY DESIGN, so the ANSWER carries the binding.

    ``KEY_DIFFERS`` and ``KEY_RELATIVE`` both ask about the key, so
    ``question_shape`` gives them one ``asks`` value and one item on purpose:
    FOUR identities, not five. Splitting them is not the fix and would undo the
    round before this one, because WHICH of the two fires is a function of what
    that machine's disk holds, and an identity that moves with the disk is the
    defect this unit removed.

    WHAT WAS ACTUALLY BROKEN, measured through the real verbs in both
    directions. A list line asking for ``Sun Path`` at 03A against a library
    holding it at 08A is a ``KEY_DIFFERS`` question. Accept it WITHOUT naming the
    copy. Replace the 08A file with an 03B one, the relative minor that
    ``Why.KEY_RELATIVE`` exists to catch because 3A and 3B look like agreement to
    anything comparing wheel positions. The next run found the same item, read
    the same yes, and reported ``matched`` at exit zero with the 03B path in
    ``paths``, no question and no warning. The reverse ran the same way.

    An unspecific yes is a claim about THE CANDIDATE THAT WAS ON THE SCREEN, so
    ``apply_verdict`` now binds it to the option the item was offered with. A yes
    read back against a different candidate is a candidate that is gone, and it
    stalls exactly the way a verdict naming a gone candidate stalls. Naming the
    copy with ``--option`` was always safe, because ``candidate_id`` digests the
    owned key; this gives the answer that names nothing the same protection.

    THE POSITIVE LEG IS IN HERE ON PURPOSE. A binding that refused everything
    would pass the negative half and break the feature, so the same unspecific
    yes is first driven back against the UNCHANGED library and has to apply.
    """
    listed = keyed_list(tmp_path, "asked.json", key="03A")
    held = hold(music, f"{answered_at} - 124 - Aurora Bloom - Sun Path")

    _code, first = drive(["match", "run", listed])
    asked = first["data"]["needs_review"][0]
    assert asked["why"] == str(answered_why)
    item_id = asked["review_item"]
    drive(["review", "resolve", item_id, "--verdict", "accepted"])

    # THE ANSWER APPLIES to the copy it was given about.
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
    # AND THE RUN SAYS SO, on the channel that carries a verdict it cannot apply,
    # with the remedy that actually works.
    warned = [
        w for w in after["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE
    ]
    assert [(w["item"], w["remedy"]) for w in warned] == [(item_id, match_cli.CLEAR_VERB)]
    # THE QUESTION UNDERNEATH IS STILL THE OTHER ONE, which is what makes this a
    # binding on the answer rather than a split of the identity: the same item is
    # asked again, and it is asked about a why the first answer never saw.
    assert match.question_shape(later_why) == match.question_shape(answered_why)


def test_the_set_that_names_the_key_questions_is_what_the_identity_reads():
    """IT WAS DEAD AND ITS DOCSTRING CLAIMED A PROPERTY THE CODE HAD LOST.

    Repository-wide, ``KEY_QUESTIONS`` was named by its own definition and by the
    ``__all__`` entry and by nothing else, while its comment said it was read by
    the item identity so that a key question and a version question are two
    items. Both clauses were false. It is read by ``question_shape`` now, and a
    why leaving it stops being a key question, which is what this asserts.
    """
    assert match.KEY_QUESTIONS == {match.Why.KEY_RELATIVE, match.Why.KEY_DIFFERS}
    for why in match.KEY_QUESTIONS:
        assert match.question_shape(why) == match.ASKS_ABOUT_KEY
    # AND NOTHING ELSE IS A KEY QUESTION, so the set is a boundary rather than a
    # list of examples.
    for why in (match.Why.VERSION_DIFFERS, match.Why.TITLE_APPROXIMATE,
                match.Why.READING_AMBIGUOUS):
        assert match.question_shape(why) != match.ASKS_ABOUT_KEY


#: HOW MANY IDENTIFIERS THE WIDTH HAS TO SURVIVE before a collision is as likely
#: as not. A billion, and it is a requirement rather than an observation: one run
#: generates an identifier per track and one per candidate, and a library-scale
#: user matches lists for years, so the number that matters is a lifetime total
#: and not the size of any one list.
REQUIRED_EVEN_ODDS_POPULATION = 1_000_000_000


def even_odds_population(width: int) -> float:
    """How many identifiers of this hex width before a collision is even money.

    The birthday bound, ``sqrt(2 ln2 . 2^bits)``, computed rather than quoted.
    Four bits per hex character.
    """
    import math

    return math.sqrt(2 * math.log(2) * 2 ** (4 * width))


def smallest_sufficient_width() -> int:
    """The narrowest WHOLE-BYTE hex width that clears the requirement.

    WHOLE BYTES, which is the half of this nobody had written down. An odd hex
    width is half a byte, so the last character carries a nibble that no storage,
    no wire format and no reader treats as a unit, and a width nobody can state
    in bytes is a width nobody chose. So the search steps by two, and the answer
    is the smallest even width whose birthday bound is past the requirement.
    """
    return next(
        width
        for width in range(2, 65, 2)
        if even_odds_population(width) >= REQUIRED_EVEN_ODDS_POPULATION
    )


def test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement():
    """A TEST THAT DEFINES ITS EXPECTATION BY ASKING THE THING IT VERIFIES.

    THIS IS THE SELF REFERENTIAL SHAPE, and it was here in both halves. The only
    dying assertion was the literal ``DIGEST_WIDTH == 16``, and the behavioural
    half asserted ``len(digest) == match.DIGEST_WIDTH``, which is derived from the
    constant and therefore passes at EVERY width. Changing 16 to 15 or 17 killed
    exactly one assertion, and it was the one that just restates the value.

    SO THE EXPECTATION IS COMPUTED. The requirement is a population and a
    birthday bound; the constraint is that a width is a whole number of bytes;
    the answer is the narrowest width satisfying both, and the number 16 appears
    nowhere in the derivation. Narrower fails the requirement, wider is not the
    narrowest, and an odd width is not a byte count.

    THE ARITHMETIC IS CHECKED AGAINST THE VALUES THE MODULE'S OWN COMMENT CLAIMS,
    because a formula that agrees with itself proves nothing either: 32 bits gives
    roughly 77,000 and 64 bits around five billion, which is what that comment
    says out loud.
    """
    assert round(even_odds_population(8)) == 77163
    assert 5.0e9 < even_odds_population(16) < 5.1e9
    assert match.DIGEST_WIDTH == smallest_sufficient_width()
    assert match.DIGEST_WIDTH % 2 == 0
    assert even_odds_population(match.DIGEST_WIDTH) >= REQUIRED_EVEN_ODDS_POPULATION
    assert even_odds_population(match.DIGEST_WIDTH - 2) < REQUIRED_EVEN_ODDS_POPULATION


def test_the_declared_width_survives_a_population_a_narrower_one_does_not():
    """THE BIRTHDAY ARGUMENT, DRIVEN, because an arithmetic pin is still arithmetic.

    Identifiers are synthesized the way the module synthesizes them, from a
    library-shaped population of artists, titles, versions and keys, and counted
    for real collisions. At half the declared width the collisions are there to
    see; at the declared width there are none. The inputs are fixed, so both
    counts are deterministic rather than a sample somebody got lucky with.
    """
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


def test_every_identifier_this_module_generates_is_the_declared_width(
    cfg, music, tmp_path
):
    """SIXTY-FOUR BITS, ASSERTED AGAINST A COMPUTED EXPECTATION, not against itself.

    ``match_id``, ``candidate_id`` and ``option_id`` all come out of one digest.
    Halving the width to 32 bits left the whole suite green, because a suite
    drives tens of identifiers and a collision needs tens of thousands. Main's
    own residual about two identity generators, 16 bits and 64, records exactly
    this class of unargued width for a run identifier; this is a third generator
    nobody had counted.

    THE WIDTH THE REAL VERB EMITS is compared against
    :func:`smallest_sufficient_width`, which is derived from the requirement.
    Comparing it against ``match.DIGEST_WIDTH`` is what this used to do, and that
    is the constant verifying itself: every identifier the module builds is
    exactly as wide as the constant says at any value the constant takes.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    path = write_list(
        tmp_path,
        "Aurora Bloom - Sun Path (Extended Mix)\nNova Reef - Tide Line\n",
        "widths.txt",
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


def test_a_resemblance_below_the_floor_is_missing_rather_than_a_question(
    cfg, music, tmp_path
):
    """THE FLOOR IS A PRODUCT DIAL AND NOTHING WAS PINNING IT.

    Lowering it from 82 to 41 left the whole suite green, and the floor decides
    which rows become questions at all. Its own comment says the cost of a low
    one is "noise in the queue", which is the very thing the residual titled "The
    ambiguous reading class is queued as a question and does not gate the run"
    has just taken a product decision about.

    The pinned example is the one measured by the residual titled "The index
    reads a file's title one way, so the disk side of the one-word dash stays
    narrow": ``Sun Path`` against a library holding only ``Sun Path
    Instrumental`` scores 76.4.
    The score is computed here rather than asserted from memory, so this row
    stays a discriminator if the scorer ever changes.
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


#: THE TWO LIBRARY TITLES THAT SIT EITHER SIDE OF THE FLOOR WITH NOTHING BETWEEN
#: THEM, and the scores are measured rather than remembered. Against the folded
#: recording token for ``Aurora Bloom / Sun Path``, ``Sun Pat Reprise`` scores
#: 81.63 and ``Sun Path Meridian`` scores 82.35, so 82 is the only integer floor
#: that puts one below and the other above.
FLOOR_NEIGHBOURS = ("Sun Pat Reprise", "Sun Path Meridian")


def test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way(
    cfg, music, tmp_path
):
    """A CONSTANT PINNED ONLY FROM THE EXTREMES IS A CONSTANT WITH A FREE BAND.

    The row above this one separates 41 from 82 and nothing separates 82 from its
    neighbours: measured, moving the floor to 77, to 81 or to 83 killed NOT ONE
    test in the suite, so at least [77, 83] was free and the value was pinned only
    by the distant ends. A dial with a seven-wide free band is a dial nobody has
    actually chosen, which is the same shape as the coefficient the round before
    this one found multiplied by four with the suite green.

    SO THE PIN IS THE NEAREST SCORE ON EACH SIDE. One library holds two
    resembling recordings, one scoring just under the floor and one just over it,
    and one list line asks about the record neither of them is. At 82 exactly one
    of them becomes a candidate. Lower the floor by one and the other joins the
    offer; raise it by one and there is no question at all and the track reports
    missing. Every integer floor except this one changes what a person is shown.

    The scores are COMPUTED here, not asserted from memory, so the pair stays a
    discriminator if the scorer ever changes and says so loudly if it does not.
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
    """THE CONSTANT IS SPENT TWICE AND ONLY THE SECOND SPEND WAS MEASURED.

    Its comment argues at length that the limit is given to the scorer AND used
    to truncate the candidate list, because one recording can be held as several
    versions. Multiplying the scorer's limit by four left the suite green, so the
    first spend was a written justification with nothing behind it.

    The two spends are told apart by the WITHHELD COUNT. Eight resembling
    recordings held as one version each: capped at the scorer, five candidates
    are built and nothing is kept back; uncapped, eight are built, five shown and
    three reported withheld. A run that says three were kept back over a library
    of one-version recordings is a run whose scorer limit is not this constant.
    """
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
    """BOTH MEMBERS OF ``STALLED`` EARN THEIR PLACE AND ONLY ONE WAS PINNED.

    Dropping ``VERDICT_UNSPECIFIC`` from that set left the whole suite green
    while the row it names lost everything the set buys: no
    ``verdict-unapplicable`` warning, no ``review clear`` remedy, and a place in
    the ANSWERABLE half of the pending action, which tells a caller to list the
    queue and record a verdict on an item that is RESOLVED in the store,
    invisible to ``review list`` and refused by ``review resolve``. That dead end
    is the one ``_pending``'s own docstring says it exists to prevent.
    """
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
    warned = [
        w for w in after["warnings"] if w["code"] == match_cli.VERDICT_UNAPPLICABLE
    ]
    assert [(w["item"], w["remedy"]) for w in warned] == [
        (item_id, match_cli.CLEAR_VERB)
    ]
    pending = after["pending_human_action"]
    assert pending["verify_verb"] == match_cli.CLEAR_VERB
    assert f"crate review clear {item_id}" in pending["steps"]
    # NOT FILED AS ANSWERABLE. ``review resolve`` refuses it, so a step telling
    # somebody to record a verdict on it is a printed instruction that fails.
    assert not any(step.startswith("list the version-match queue") for step in pending["steps"])


def test_an_unanswered_item_is_re_offered_so_its_candidates_follow_the_library(
    cfg, music, tmp_path
):
    """AN OPEN ITEM WHOSE OPTIONS ARE FROZEN AT THE FIRST RUN OFFERS FICTION.

    ``adjudicate`` re-offers an item that exists but carries no verdict. Dropping
    that condition left the suite green and left the stored payload and options
    at whatever the library held the first time the line was seen, so ``review
    show`` offered a person candidates that no longer exist while the library
    moved underneath them. ``review.offer`` is the thing that refreshes an open
    item, and it only gets the chance if it is called.
    """
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


def test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported(
    cfg, music, tmp_path
):
    """THE SILENCE THE LAST ROUND CREATED, in both states it survives into.

    The warning loop asks under ``Wanted.addresses``, which since the round that
    narrowed it walks only the reading the LIST spelled. A candidate is by
    construction a version the list did NOT spell, which is what makes it a
    question, so a tombstone standing over the file being OFFERED as the answer
    was reported in no state at all.

    Driven: a tombstone under ``Sun Path (Live)``, the library still holding that
    file, and the list line ``Aurora Bloom - Sun Path - Live``. The first run
    offered that exact file and said nothing about the tombstone. Accepting it
    produced a matched row with an EMPTY warning array. This file's own docstring
    promises the opposite in as many words: a tombstone over a version the
    library actually holds is a stale record, and saying so is cheaper than
    letting somebody discover it during a deletion.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
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


def test_one_tombstone_over_one_row_is_one_warning_however_it_is_reached(
    cfg, music, tmp_path
):
    """The row's own address and the offered file can be the same tombstone.

    A list spelling ``Sun Path (Live)`` addresses that string itself AND is
    offered the file held under it, so both loops find one suppression for one
    row. Two warnings about one stale record is one thing to fix wearing two
    hats.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
        actor="deletion",
    )
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Live)")
    path = write_list(tmp_path, "Aurora Bloom - Sun Path (Live)\n", "once.txt")
    _code, envelope = drive(["match", "run", path])
    stale = [w for w in envelope["warnings"] if w["code"] == match_cli.TOMBSTONE_OVER_OWNED]
    assert [w["suppression"] for w in stale] == [recorded.suppression_id]


#: U24's ``cratekit.core.tombstone.VERSION_WORDS``, WRITTEN OUT INDEPENDENTLY.
#: Not derived from ``match.VERSION_WORDS``, because a pin computed from the
#: thing it pins asserts that the code agrees with itself, which is the shape
#: that let three defects through in this unit already. The gated drift guard
#: compares this side against the real module the day it merges; until then this
#: literal is the only thing standing between the two copies.
U24_VERSION_WORDS: frozenset[str] = frozenset(
    {
        "acapella", "acoustic", "alternate", "bootleg", "club", "cut", "demo",
        "dub", "edit", "extended", "flip", "instrumental", "interlude", "live",
        "mashup", "mix", "original", "radio", "remaster", "remastered", "remix",
        "reprise", "rework", "session", "unplugged", "version", "vip",
    }
)

#: The words that were in this module's list and in nobody else's, and the ones
#: that were in the domain module's and not here. The second column is the one
#: that cost: every word in it reported MISSING for a file the library held.
VOCABULARY_GAP: tuple[str, ...] = (
    "acapella", "alternate", "club", "cut", "flip", "interlude", "mashup",
    "original", "radio", "session", "unplugged",
)


def test_the_version_vocabulary_is_u24s_element_for_element():
    """ONE QUESTION, ONE VOCABULARY, and there were two of them.

    "Is this word a version designation" is asked by the deletion pass about a
    rekordbox ``Subtitle`` and by this module about a dash tail. Two lists
    answering it is the same defect as two spellings of the tombstone identity,
    one level down, and it is invisible to any suite that drives one side.

    ``rerecorded`` is the one deliberate difference and it is a HEAD word rather
    than a tail word: this module has a leading-word convention because the
    public playlist API ships "Remastered 2011", and the domain module has no use
    for one.
    """
    assert match.VERSION_WORDS == U24_VERSION_WORDS
    assert set(VOCABULARY_GAP) < match.VERSION_WORDS
    # DERIVED, so a word cannot be added to one and forgotten in the other.
    assert match._DASH_VERSIONS == match.VERSION_WORDS | match._DASH_VERSION_HEADS
    assert match._DASH_VERSIONS - match.VERSION_WORDS == {"rerecorded"}


@pytest.mark.parametrize("word", VOCABULARY_GAP)
def test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file(
    cfg, music, tmp_path, word
):
    """THE MEASURED COST OF THE SECOND VOCABULARY, one row per missing word.

    With the library holding ``Aurora Bloom - Sun Path (Unplugged)`` and a list
    spelling ``Aurora Bloom - Sun Path - Unplugged``, the run reported MISSING
    with an acquisition option and went and fetched a file already on the shelf,
    at exit zero, with nothing asked and nothing warned. That is verbatim what
    ``_is_a_version``'s docstring calls "the other half of the same mistake", and
    it was live for eleven words while ``Live`` asked a question.

    Four of the eleven landed on ``title-approximate`` instead, which is not the
    same failure but is the same wrong question: an approximate hit offers
    candidates from a DIFFERENT recording, so a person was asked whether some
    other record is theirs rather than whether their unplugged cut is this one.
    """
    hold(music, f"08A - 124 - Aurora Bloom - Sun Path ({word.title()})")
    path = write_list(
        tmp_path, f"Aurora Bloom - Sun Path - {word.title()}\n", f"{word}.txt"
    )
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
    """THE SENTENCE A CALLER READS UNDERCOUNTED THE QUEUE SIX FOLD.

    The ungated class is filtered out of the GATE on purpose. It was filtered out
    of the SENTENCE too, so a run whose ``needs_review`` array held 24 rows
    printed "4 tracks ... need a person" and the other 20 existed only on the
    warning channel. The caller who reads a summary is exactly the caller who
    does not read every warning, so that is R11's silence wearing this unit's own
    fix as a costume.

    What must NOT change is the exit status: the ungated rows still do not gate,
    which is the decision the ambiguous-reading residual records.
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


def test_an_ungated_question_on_its_own_still_leaves_the_run_at_exit_zero(
    cfg, music, tmp_path
):
    """The count is in the sentence and not in the gate, which is the whole point."""
    for tail in ("Live", "Edit"):
        hold(music, f"08A - 124 - Nova Reef - Tide Line ({tail})")
    path = write_list(
        tmp_path,
        "Nova Reef - Tide Line - Live\nNova Reef - Tide Line - Edit\n",
        "onlyungated.txt",
    )
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.OK)
    assert envelope["pending_human_action"] is None
    assert len(envelope["data"]["needs_review"]) == 2
    assert len(
        [w for w in envelope["warnings"] if w["code"] == match_cli.READING_UNSETTLED]
    ) == 2


def test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire(
    cfg, music, tmp_path
):
    """THE COUNTEREXAMPLE TO A REASON THAT WAS WRITTEN AS IF MEASURED.

    The ambiguous-reading residual rejected a proposed narrowing on the ground
    that the two readings "ALWAYS differ in acquisition": the question is asked
    exactly when the library holds the confirming file, so accepting means the
    library has it and rejecting means going and getting it.

    That is false whenever a tombstone stands over the reading the LIST spelled.
    Accepting holds; rejecting reaches ``apply_verdict``'s tombstone consult and
    produces SUPPRESSED with nothing to acquire. So for this class the two
    answers are hold versus SKIP, and a narrowing on "genuinely different
    acquisitions" would drop it outright rather than leaving it untouched. The
    control below is the same pair with no tombstone, which is where the reason
    does hold.
    """
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path - Live"),
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
    """WHAT THE ENUMERATION RESIDUAL COSTS, MEASURED RATHER THAN ASSERTED.

    That entry says the cost is taken "because the run says what it is about to
    get". Driven with the file actually gone from the disk, the run says what it
    is about to GET and says nothing about the DELETION: the dash-spelled list
    exits 0 with a missing row, an acquisition query, and ZERO warnings, so the
    row is indistinguishable from any other missing track in a 200 row list.

    The bracket-spelled list is the control and is the shape the enumeration does
    reach: same tombstone, same absent file, all three arrays empty and a warning
    naming the suppression. The difference between the two is the whole residual.
    """
    recorded = review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Aurora Bloom", "Sun Path (Live)"),
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
    assert [option["query"] for option in row["acquisition"]] == [
        "Aurora Bloom Sun Path - Live"
    ]
    assert missed["warnings"] == [], (
        "the run that undoes a deliberate deletion now says so, and this entry's "
        "cost has changed"
    )


#: A residual cited the old way, built from pieces so this pattern does not match
#: its own source line. Two branches have already given two different findings one
#: number, so a citation by number is a citation that stops resolving silently.
_BY_NUMBER = re.compile(r"\bR" + "-" + r"[0-9]+")

#: The files this unit owns. Other units cite their own residuals by number and
#: that is their business; what this guard is about is the three files whose
#: citations were measured to be pointing at six colliding numbers.
UNIT_FILES = (MATCH_SOURCE, MATCH_CLI_SOURCE, Path(__file__).resolve())


def test_every_residual_this_unit_cites_is_a_heading_that_exists():
    """A CITATION BY TITLE IS ONLY BETTER THAN A NUMBER IF SOMETHING CHECKS IT.

    Every title in ``RESIDUALS`` is matched against the headings in
    ``docs/residual-findings.md``, so a renumber leaves the citations working and
    a RETITLE fails a test rather than leaving a sentence pointing at nothing.
    """
    headings = {
        line.split(". ", 1)[1].strip()
        for line in RESIDUALS_DOC.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ") and ". " in line
    }
    missing = [title for title in RESIDUALS if title not in headings]
    assert missing == [], f"cited titles that are not headings: {missing}"


def test_every_residual_title_this_unit_names_is_actually_cited_somewhere():
    """A REGISTER THAT OUTLIVES ITS CITATIONS IS A LIST NOBODY MAINTAINS."""
    prose = "\n".join(path.read_text(encoding="utf-8") for path in UNIT_FILES)
    # The register itself is prose in this file, so a title is cited when it
    # appears somewhere OTHER than the tuple that declares it.
    # COMMENT MARKERS AND QUOTES COME OFF FIRST. A title is written across two
    # adjacent string literals in the register above and across several ``#:``
    # comment lines in the source, so a raw whitespace collapse finds neither.
    flattened = re.sub(r"\s+", " ", re.sub(r"#:?", " ", prose).replace('"', " "))
    for title in RESIDUALS:
        assert flattened.count(re.sub(r"\s+", " ", title)) >= 2, title


def test_no_residual_is_cited_by_number_anywhere_in_this_unit():
    """THE MECHANISM THAT ALREADY BROKE ONCE ON THIS WAVE, closed.

    A trial merge against main reports six residual numbers colliding with
    different content on each side, and this unit's source and tests cited four
    of them a total of eleven times. After the merge every one of those points at
    a different subject, and nothing anywhere fails.
    """
    for path in UNIT_FILES:
        found = _BY_NUMBER.findall(path.read_text(encoding="utf-8"))
        assert found == [], f"{path.name} cites a residual by number: {found}"


# ═══════════════════════════════════════════════════════════════════════════
# U265: the approximate pass sorts each name's words once, and answers as before
# ═══════════════════════════════════════════════════════════════════════════
#
# ``_approximate`` handed ``rapidfuzz`` the scorer ``token_sort_ratio``, which
# splits and sorts both strings' words again for every pair, so each library
# name was sorted once per wanted row. It now sorts each name once for the life
# of the index and scores the sorted forms with ``fuzz.ratio``, which is what
# ``token_sort_ratio`` computes after its own sort. The matcher decides what is
# acquired and what is a duplicate, so the shipped call is kept below as the
# reference and the new pass is held EQUAL to it, every candidate, score and
# order, rather than close to it.


def _shipped_approximate(wanted, index, *, limit=match.APPROXIMATE_LIMIT):
    """THE SCORER AS SHIPPED BEFORE U265, kept as the reference it is held to.

    ``limit`` is the shipped call's, the offer limit, unless a caller asks for
    every recording over the floor, which is how the resolver has called
    discovery since U286 filters the hits by title before it caps them.
    """
    from rapidfuzz import fuzz, process

    if not index.by_recording:
        return ()
    found = process.extract(
        wanted.recording,
        tuple(index.by_recording),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=match.APPROXIMATE_FLOOR,
        limit=limit,
    )
    return tuple(held for token, _score, _position in found for held in index.versions(token))


#: Words for generated names: plain, accented, fullwidth, ligatures, other
#: scripts, a repeated word, and the halves that fold to nothing.
_U265_WORDS = (
    "sun", "path", "aurora", "bloom", "night", "drive", "deep", "echo", "you", "me",
    "Beyoncé", "Sigur Rós", "Röyksopp", "Ｓｕｎ", "Ｐａｔｈ", "naïve", "straße", "ﬁne",
    "東京", "Привет", "écho", "dup dup dup", "Ⅻ", "", "!!!", "01",
)


def _u265_library(seed: int) -> tuple[match.LibraryIndex, list[match.Wanted]]:
    """A generated library and list, tie dense on purpose.

    Three families: names drawn from the word pool above, including empty
    halves; the fixtures' own ``Sun Path`` naming with one and two letter edits,
    which puts many recordings over the floor for one row and many equal scores
    inside the five returned; and every artist and title swapped, which the
    word sort scores as one string.
    """
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
    """Every row's candidates, in their order, equal the shipped scorer's.

    The comparison is on the whole ``Owned`` tuple, so a different candidate, a
    different order among equal scores, or a different cut at the floor or the
    limit all fail it. And the fixture is asserted to carry the cases that make
    equality mean something: rows with more than five recordings over the floor,
    equal scores inside a returned five, and rows with nothing over the floor.
    """
    from rapidfuzz import fuzz, process

    index, rows = _u265_library(seed)
    over_the_limit = tied_inside = nothing = 0
    for wanted in rows:
        assert match._approximate(wanted, index, limit=limit) == _shipped_approximate(
            wanted, index, limit=limit
        ), wanted.recording
        every = process.extract(
            wanted.recording,
            tuple(index.by_recording),
            scorer=fuzz.token_sort_ratio,
            score_cutoff=match.APPROXIMATE_FLOOR,
            limit=None,
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
    """THE WHOLE MATRIX, no cutoff: ``ratio`` over the sorted forms equals
    ``token_sort_ratio`` over the tokens for every pair, as a float, with ``==``.

    The candidate test above sees only what clears the floor; this sees every
    score, so a pair the sort disagreed about under the floor cannot hide.
    """
    from rapidfuzz import fuzz

    index, rows = _u265_library(7)
    # Raw tokens too, never folded, at every width and with the two characters
    # the scorer splits on in a wide string and not in a narrow one.
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
    """Python's whitespace is not always ``rapidfuzz``'s, and which it is
    depends on the string's WIDTH, measured over every code point when U265 was
    built: in a string whose characters are all below U+0100 the scorer does not
    split on U+0085 or U+00A0, and in any wider string it splits on exactly
    Python's whitespace.

    ``fold`` leaves neither in a token, but the sort is held to the scorer on
    any text, so a token from anywhere scores as it did. Every code point Python
    calls whitespace, both exceptions, and every code point below U+3100, in
    three shapes (inside a word, alone, and doubled between two words) at each
    of Python's three string widths, the wide ones made by a word beside it.
    """
    from rapidfuzz import fuzz

    points = {cp for cp in range(0x110000) if chr(cp).isspace()}
    points |= {0x85, 0xA0, 0x1F} | set(range(0x3100))
    points -= set(range(0xD800, 0xE000))
    for widen in ("", " \xe9", " Ā", " \U0001f600"):
        for cp in sorted(points):
            c = chr(cp)
            for token, other in (
                (f"zz{c}aa{widen}", f"aa zz{widen}"),
                (f"{c}{widen}", ""),
                (f"b{c}{c}a{widen}", f"a b{widen}"),
                (f"b{c}a{widen}", "a b"),
            ):
                assert fuzz.ratio(match._sorted_words(token), match._sorted_words(other)) == (
                    fuzz.token_sort_ratio(token, other)
                ), (hex(cp), widen)
    assert match._sorted_words("b\xa0a") == "b\xa0a", "a narrow string keeps its no-break space"
    assert match._sorted_words("b\xa0a Ā") == "a b Ā", "a wide one splits on it"
    # THE BOUNDARY: U+00FF is the widest narrow character and U+0100 the
    # narrowest wide one, so a width test one off either way is caught here.
    for edge in ("\xff", "Ā"):
        for c in ("\x85", "\xa0"):
            token, other = f"z{c}a{edge}", f"a{edge} z"
            assert fuzz.ratio(match._sorted_words(token), match._sorted_words(other)) == (
                fuzz.token_sort_ratio(token, other)
            ), (hex(ord(edge)), hex(ord(c)))


def test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call(monkeypatch):
    """R recordings and W rows cost R + W sorts, and a new index pays its own R.

    The sort was paid once per PAIR, inside the scorer, so a library name was
    sorted again for every wanted row; the count is the proof the saving is
    there, since no wall clock threshold is asserted.
    """
    calls: list[str] = []
    real = match._sorted_words

    def counted(token: str) -> str:
        calls.append(token)
        return real(token)

    monkeypatch.setattr(match, "_sorted_words", counted)
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


# ═══════════════════════════════════════════════════════════════════════════
# U286: the artist agreeing is necessary for an approximate offer, never
# sufficient. The discovery score above reads artist and title together, so
# with a short title the shared artist carried an unrelated song over the
# floor: Monkey Safari, Joy scored 84.2 against the library's Monkey Safari,
# Goodbye and was held for review rather than downloaded. Four more of the
# five open title-approximate items at sitting 99 had the same shape.
# ═══════════════════════════════════════════════════════════════════════════

#: The card's five pairs, each a short wanted title against an unrelated held
#: one by the same artist, every one of them over the discovery floor.
U286_UNRELATED = (
    ("Monkey Safari", "Joy", "Goodbye"),
    ("Paul Deep (AR)", "Rea", "Tique"),
    ("Hot Since 82", "Wow", "Wild"),
    ("Alex Kaminski", "Mana", "Nebula"),
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
    """Each pair clears the discovery floor, so it reaches the title test, and
    the title test drops it: the row reads missing and the pass downloads it."""
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
    # THE WORDS SPLIT OR JOINED, review round one's finding: ``fold`` turns a
    # dot into a space, so these share no word and score on their letters
    # alone, under the floor, and were read missing and downloaded again.
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
    """FILTERED BEFORE THE CANDIDATES ARE BUILT. The failing recording is held
    as five versions, so a filter applied to the candidates, or to nothing,
    would build six and report one withheld beside an offer of five."""
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
    """FILTERED BEFORE THE CAP, NOT AFTER IT. Six unrelated three letter titles
    by the same artist each outscore the real near match, so the best five
    recordings hold none it would offer: filtered after the cap, the row
    would read missing and download a record the library holds."""
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
    """The word sort reads a swapped listing as one string at 100, and it is
    the same record, so the title test lets each half stand for the other."""
    hold(music, "08A - 124 - Sun Path - Aurora Bloom")
    found = resolve([one()], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [(c.artist, c.title) for c in found.candidates] == [("Sun Path", "Aurora Bloom")]


def test_a_swap_is_offered_only_when_both_halves_cross():
    """One half crossing is not a swap: the title has to resemble the held
    artist AND the artist the held title."""
    held = match.Owned(path=Path("x.flac"), artist="Sun Path", title="Tide Line", version="", key=None)
    assert not match._title_resembles(one(), held)
    held = match.Owned(path=Path("x.flac"), artist="Nova Reef", title="Aurora Bloom", version="", key=None)
    assert not match._title_resembles(one(), held)


def _index_of_owned(*held: match.Owned) -> match.LibraryIndex:
    grouped: dict[str, list[match.Owned]] = {}
    for owned in held:
        grouped.setdefault(owned.recording, []).append(owned)
    return match.LibraryIndex(by_recording={k: tuple(v) for k, v in grouped.items()})


#: An artist long enough that a title of one short word, or of none, still
#: clears the discovery floor, so a title that folds to nothing reaches the
#: title test at all.
LONG_ARTIST = "Aurora Bloom and the Harbour Lights Orchestra"


@pytest.mark.parametrize(("wanted", "held"), [("!!!", "Sun"), ("Sun", "!!!")])
def test_a_title_that_folds_to_nothing_is_offered_as_before(wanted, held):
    """A title with no letter or digit cannot be read, so the title test says
    nothing about it and the discovery score decides, as it did before U286.
    Read as sharing nothing it would download a record the library may hold."""
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
    """No special case offers everything by the artist to a one letter title:
    A against B shares nothing and settles missing, A against A is owned."""
    assert _discovery_score("Aurora Bloom", "A", "Aurora Bloom", "B") >= match.APPROXIMATE_FLOOR
    hold(music, "08A - 124 - Aurora Bloom - B")
    found = resolve([one(title="A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MISSING
    hold(music, "08A - 124 - Aurora Bloom - A")
    found = resolve([one(title="A")], index_of(music)).matches[0]
    assert found.state is match.MatchState.MATCHED


def test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about(music, tmp_path):
    """Sitting 9's Stefan Ringer ``SO``, the library's ``Sexual Obsession``: an
    approximate hold that was right. It scores far under the discovery floor,
    so it never came from the scored pass, and the ISRC branch that asks it is
    untouched by the title test."""
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


#: THE TWO TITLE PAIRS EITHER SIDE OF THE TITLE FLOOR, scores computed below:
#: ``Burning Sunlight`` against ``Morning Starlight Rising`` scores 65.0, and
#: ``Joy`` against ``Jay``, one letter changed in a three letter title, 66.67,
#: the lowest score a single changed letter can give a title of three letters
#: or more. 66 is the one integer floor between them.
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
    """THE REFERENCE, WRITTEN APART FROM THE CODE: the shipped scorer's every
    hit over the floor, in its order, each recording kept when its folded
    title, or both halves crossed, is one string with the spaces gone or
    reaches the title floor by ``token_set_ratio``, or when either title folds
    to nothing, then the first five. And U265's identity where nothing is dropped: a row whose shipped
    five all pass is offered exactly the shipped five, every candidate and
    order unchanged. The generated libraries are asserted to carry rows of
    both kinds, and rows where a dropped hit makes room for a sixth."""
    from rapidfuzz import fuzz

    def agree(one_name, other_name):
        joined = "".join(one_name.split())
        if joined and joined == "".join(other_name.split()):
            return True
        return fuzz.token_set_ratio(one_name, other_name) >= match.APPROXIMATE_TITLE_FLOOR

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
    # THE CARD'S SHAPE BESIDE U265'S: short titles by one artist, related and
    # not, so rows drop hits and a drop makes room for a hit past the five.
    short = ("Joy", "Jay", "Joys", "Box", "Cox", "Fox", "Lox", "Pox", "Sox",
             "Wow", "Wild", "Rea", "Tique", "Mana", "Nebula", "Goodbye", "O.K.")
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
        for title in ("Joy", "Wow", "Mana", "Rea", "Get Out", "A", "OK", "Good Bye")
    ]
    unchanged = dropped = refilled = joined = 0
    for wanted in rows:
        every = by_recording(_shipped_approximate(wanted, index, limit=None))
        kept = [group for group in every if passes(wanted, group[0])][: match.APPROXIMATE_LIMIT]
        expected = tuple(held for group in kept for held in group)
        assert match._resembling(wanted, index) == expected, wanted.recording
        joined += any(
            "".join(match.fold(wanted.title).split()) == "".join(match.fold(g[0].title).split())
            and match.fold(wanted.title) != match.fold(g[0].title)
            for g in kept
        )

        shipped = by_recording(_shipped_approximate(wanted, index))
        if all(passes(wanted, group[0]) for group in shipped):
            assert match._resembling(wanted, index) == _shipped_approximate(wanted, index)
            unchanged += bool(shipped)
        else:
            dropped += 1
            refilled += len(kept) > len([g for g in shipped if passes(wanted, g[0])])
    assert unchanged and dropped and refilled and joined, (unchanged, dropped, refilled, joined)


def test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio():
    """``Get Out`` against ``Agenou`` with the spaces taken out scores 66.67,
    over the title floor, so the joined form is compared for equality only:
    a ratio would let the card's own unrelated pair back in."""
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
    """Review round two's finding: the swap allowance compared each crossed
    half by its score alone, so a title first listing whose title or artist
    is split or dotted differently from the file's read missing and was
    downloaded again. Each half now gets the same equality the titles do."""
    hold(music, f"08A - 124 - {held}")
    path = write_list(tmp_path, f"{listed}\n", "swapped.txt")
    code, envelope = drive(["match", "run", path])
    assert code == int(ExitCode.PENDING_HUMAN)
    (row,) = envelope["data"]["needs_review"]
    assert row["why"] == str(match.Why.TITLE_APPROXIMATE)


# ═══════════════════════════════════════════════════════════════════════════
# A title that folds to nothing is told apart by its own text (card 834)
# ═══════════════════════════════════════════════════════════════════════════


#: Two titles of emoji alone by one artist, which ``fold`` takes to nothing.
FIRE, DROP, SNOW = "\U0001f525", "\U0001f4a7", "❄"


def test_two_different_emoji_titles_by_one_artist_are_not_one_recording(music):
    """The card's own pair. ``fold`` takes both titles to nothing, so the
    recording token was one, the exact branch called the wanted ``💧`` owned
    by the held ``🔥``, and the track was never downloaded. It is now asked,
    by U286's allowance for a title that folds to nothing, never matched."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert found.state is not match.MatchState.MATCHED
    assert found.paths == ()
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert found.why is match.Why.TITLE_APPROXIMATE
    assert [c.title for c in found.candidates] == [FIRE]


def test_two_different_emoji_titles_through_the_real_verb_are_not_owned(cfg, music, tmp_path):
    """The residual's own drive, a text list through ``match run``: not
    matched, so the row reaches a person and is never silently skipped."""
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
    """Both files sit under one recording token. Only the one the row names is
    the match, and its path alone is reported."""
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
    """One title written two ways by two sources is one recording, so the
    bare text drops width, case, spacing and the invisible characters a
    source adds or leaves out. A real duplicate must not download again."""
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
    """Grouped by the recording token alone they were one candidate titled
    by whichever file came first and carrying both paths, so accepting it
    accepted a file the person was never shown, under one identifier."""
    hold(music, f"08A - 124 - Aurora Bloom - {FIRE}")
    hold(music, f"08A - 124 - Aurora Bloom - {SNOW}")
    found = resolve([one(title=DROP)], index_of(music)).matches[0]
    assert found.state is match.MatchState.NEEDS_REVIEW
    assert sorted(c.title for c in found.candidates) == sorted([FIRE, SNOW])
    assert all(len(c.paths) == 1 for c in found.candidates)
    assert len({c.candidate_id for c in found.candidates}) == 2


def test_a_candidate_whose_title_folds_to_something_keeps_its_identifier(music):
    """The identifier a recorded answer names is unchanged for every title
    that folds to something: the bare title joins the digest only when it is
    not empty."""
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Extended Mix)")
    found = resolve([one()], index_of(music)).matches[0]
    (candidate,) = found.candidates
    expected = match._digest(
        match.recording_token("Aurora Bloom", "Sun Path"), "extended mix", "08A"
    )
    assert candidate.candidate_id == f"cd_{expected}"


def test_an_emoji_titles_identities_are_unchanged():
    """No recorded tombstone, review item or match identifier moves: they hash
    through ``fold`` and ``tombstone_fold``, which this change leaves alone."""
    wanted = one(title=DROP)
    assert wanted.recording == "aurora bloom\x1f"
    assert wanted.recording == match.recording_token("Aurora Bloom", FIRE)
    assert wanted.identity == {"artist": "aurora bloom", "title": DROP}
    asked = match.question_identity("Aurora Bloom", DROP, "", None, match.Why.TITLE_APPROXIMATE)
    assert asked["recording"] == "aurora bloom\x1f"
    found = match.TrackMatch(wanted=wanted, state=match.MatchState.MISSING, why=match.Why.NOT_IN_LIBRARY)
    assert found.match_id == f"mt_{match._digest('aurora bloom\x1f', '', '')}"


def test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled(music, tmp_path):
    """An ISRC agrees only with the title, and two emoji titles are two
    titles, so the file is offered as the question a differing title is."""
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


#: Titles that fold to something, for the differential below: the fixtures'
#: own, U265's generated words, and the shapes ``fold`` exists for.
_FOLDED_TITLES = (
    "Sun Path", "sun path", "SUN PATH", "Sun  Path", "Sun-Path", "Sun.Path", "Sun Path!",
    "Sun Pathx", "Re Mix", "Remix", "O.K.", "OK", "Good Bye", "Goodbye", "Beyoncé",
    "Beyonce", "Ｓｕｎ", "Sun", "naïve", "naive", "straße", "STRASSE", "ﬁne", "fine",
    "東京", "Привет", "Ⅻ", "XII", "01", "1", "_", "A", "a", "Joy", "Jay", "\U0001f525 Sun",
    "Sun \U0001f525", "Sun \U0001f4a7", "1️⃣", "Ⓐ",
)


def test_a_title_that_folds_to_something_compares_exactly_as_it_did():
    """Every pair whose folds are not empty: ``same_title`` is ``fold``
    equality, so no title that matched before stops matching and none starts."""
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
