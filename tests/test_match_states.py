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
from tests import _pending
from tests._containers import synth_container

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
MATCH_SOURCE = SRC_ROOT / "cratekit" / "acquire" / "match.py"
MATCH_CLI_SOURCE = SRC_ROOT / "cratekit" / "acquire" / "match_cli.py"


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


@_pending.requires("cratekit.core.tombstone")
def test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist():
    """THE ONLY GUARD THAT CAN SEE THE COPIES DRIFT, armed when U24 lands.

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
    of the six it still cannot reach at all.

    So the second check is over the RECORDING PATH: for every rekordbox row shape,
    the identity U24's recorder would write, composed by its OWN
    ``version_title`` from the Title column AND the version column, is compared
    against the identities the three readers on this side actually produce, and
    the ones that cannot reconcile are named in ``UNRECONCILED`` rather than left
    to a silent miss. The version column is in it because that is where the two
    sides diverged: U24 reads a version out of ``RemixerName`` and ``Subtitle``
    and composes, this side composes from a provider's version field, and the
    property that matters is whether the two compositions produce one string.

    WHAT IT STILL CANNOT PROVE, and this is the residual R-21 records: U24's
    RECORDER is not imported here either, so the string it hands
    ``version_identity`` is taken from ``u24_records`` below, which is a
    hand-written imitation of ``deletion.stores.version_of`` that nothing checks
    against U24's real code. This guard compares one real function against one
    real function and one real derivation against an IMITATED one. The check that
    would close it is named in R-21.
    """
    from cratekit.core import tombstone

    assert match.TOMBSTONE_KIND == tombstone.KIND_VERSION
    assert match_cli.TOMBSTONE_STORE == tombstone.STORE_KEY
    for given, _expected in FOLD_PINS:
        assert match.tombstone_fold(given) == tombstone.fold(given)
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
    # THE DERIVATION, end to end.
    missed = tuple(
        (row[0], wanted.origin)
        for row in REKORDBOX_ROWS
        for wanted in every_reader_on(row)
        if tombstone.version_identity(
            artist="Aurora Bloom", title=tombstone.version_title(row[0], row[1])
        )
        not in wanted.suppression_spellings
    )
    assert missed == UNRECONCILED, (
        "a library row spelling this side cannot address changed, so either a "
        "tombstone became invisible or R-20 is now stale"
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
#: miss. A featured credit is dropped from the matching title because it names a
#: performer, so a source that never spelled it cannot put it back, and the
#: library row that kept it is unreachable from a provider row. Recorded as R-20
#: in docs/residual-findings.md. Every other pair reconciles, and this tuple
#: going empty or growing is a change somebody has to make on purpose.
UNRECONCILED: tuple[tuple[str, str], ...] = (
    ("Sun Path (feat. Mira) (Nightwave Remix)", match.TIDAL),
)


def u24_version_title(title: str, version: str) -> str:
    """U24's ``core.tombstone.version_title``, written out INDEPENDENTLY.

    THE COMPOSITION RULE, WHICH IS WHERE THE SEAM ACTUALLY IS. It composes with
    round parentheses, which is the shape this side composes with, so the plain
    case now meets. What it also does is SHORT CIRCUIT: when the folded version
    is already inside the folded title, the Title column is recorded exactly as
    it stands. So whatever shape a rekordbox Title happens to use survives into
    the identity, and a consulter cannot assume one shape, it has to enumerate
    them. It is idempotent for the same reason, so a title already carrying its
    version is never composed twice, and this side must not defeat that by
    composing over an already composed title.
    """
    folded = u24_fold(version)
    if not folded or folded in u24_fold(title):
        return title
    return f"{title} ({version})" if title else version


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
    the code here and both disagree with what actually gets written. R-21 records
    that and names the check that would close it.
    """
    return {
        "artist": u24_fold(artist),
        "title": u24_fold(u24_version_title(row_title, row_version)),
    }


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
    """A GAP STATED IS A GAP SOMEBODY CAN CLOSE, and R-20 states this one.

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
    became invisible, and one going away means R-20 is stale.

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
        if u24_records("Aurora Bloom", row[0], row[1]) not in wanted.suppression_spellings
    )
    assert missed == UNRECONCILED


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


def test_the_consulter_never_composes_over_an_already_composed_title():
    """IDEMPOTENCE, which the recorder has and this side must not defeat.

    ``version_title`` short circuits on containment, so it never appends a
    version a title already carries. This side composes from the SPELLING'S OWN
    HEAD, which is the spelling with its version taken off, so it cannot append a
    second copy either. Composing from the listing's full title instead would
    produce ``Sun Path (Nightwave Remix) (Nightwave Remix)``, an address nothing
    will ever record, and would quietly halve the useful spellings consulted.
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
        assert doubled == [], f"the version was composed twice: {doubled}"


#: A TITLE SHAPE THIS SIDE DOES NOT ENUMERATE. The recorder keeps whatever shape
#: the Title column used, so the consulter has to know the shapes; it knows round
#: parentheses, square brackets, the dash and the multi-group split. Anything
#: else misses, and that class is recorded as R-23 rather than guessed at.
UNENUMERATED_SHAPE = ("Sun Path {Nightwave Remix}", "Nightwave Remix")


def test_a_title_shape_outside_the_enumerated_ones_is_a_recorded_gap():
    """THE BOUNDARY OF THE ENUMERATION, asserted rather than assumed.

    A consulter that enumerates shapes has an edge, and an edge nobody wrote down
    is discovered by a track coming back after somebody deleted it. This pins
    where the edge is: a curly-brace Title short circuits ``version_title``, so
    the identity keeps that shape, and no spelling this side composes reaches it
    unless the list happened to spell it the same way. R-23 records the class.
    """
    title, version = UNENUMERATED_SHAPE
    recorded = u24_records("Aurora Bloom", title, version)
    listed = match.read_tidal_tracks([PROVIDER_ROW])[0]
    assert recorded not in listed.suppression_spellings
    # The list that spelled it the same way still reaches it, which is what makes
    # this a limit of the ENUMERATION rather than of the addressing rule.
    same = match.read_text_lines(f"Aurora Bloom - {title}\n")[0]
    assert recorded in same.suppression_spellings


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
    asked = one(version="Extended Mix", key="08A")
    assert set(asked.identity) == {"artist", "title"}
    assert set(asked.question()) == {"recording", "version", "key"}
    assert asked.question()["key"] == "08A"
    # THE KEY SET NEVER VARIES AND NEITHER DOES THE VALUE. ``question`` takes no
    # argument, because the one it used to take said whether the question was
    # about the key and the LIBRARY decided that. A list line naming no key
    # carries the empty token, which is what an unreadable code folds to too.
    assert one(version="Extended Mix").question()["key"] == ""
    assert one(version="Extended Mix", key="8A").question() == asked.question()
    assert one(version="Extended Mix", key="03B").question() != asked.question()


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
    probe = synth_container(tmp_path, ".flac")
    assert tags.write_tags(probe, {"artist": "Aurora Bloom", "title": "Sun Path (Live)"})
    target = music / "08A - 124 - Typo Artist - Wrong Title.flac"
    shutil.copy2(probe, target)

    index = index_of(music)
    held = index.versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert [(row.title, row.version) for row in held] == [("Sun Path", "Live")]
    assert index.versions(match.recording_token("Typo Artist", "Wrong Title")) == ()


def test_the_camelot_head_written_into_the_filename_is_the_librarys_key(music):
    hold(music, "03B - 120 - Aurora Bloom - Sun Path")
    held = index_of(music).versions(match.recording_token("Aurora Bloom", "Sun Path"))
    assert held[0].key == "03B"


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
    assert len(match._approximate(one(title="Sun Pathwayss"), index_of(music))) > (
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

    Whether a missing row belongs in the queue instead is R-17, a product
    decision reserved for a person. What is settled either way is that the
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
    assert empty.question_identity == confirmed.question_identity
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

    ``review export`` and ``review import`` move a decision between machines. One
    list line carrying a key resolves to a KEY question on a machine holding that
    exact version at another key, and to a VERSION question on a machine holding
    only another version. The identity used to be gated on which of those two the
    library chose, so the two machines opened two items under one ``match_id``:
    the import reported the row inserted with no conflict, the receiving machine
    looked its own question up under the other identifier, found nothing, and
    asked again. The answer was imported and ignored, and nothing anywhere said
    so.

    Driven at the seam rather than asserted on the object, because the object
    agreeing is what the last round already proved about ``match_id`` while this
    went on failing underneath it.
    """
    line = match.read_tidal_tracks(
        [{"id": "1", "title": "Sun Path", "version": "Nightwave Remix",
          "key": "08A", "artist": {"name": "Aurora Bloom"}}]
    )

    def library(*names: str) -> match.LibraryIndex:
        room = tmp_path / f"lib{len(names)}{names[0][:3]}"
        room.mkdir(parents=True, exist_ok=True)
        for name in names:
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

    # MACHINE A holds the exact version, at the wrong key.
    machine_a = library("03A - 124 - Aurora Bloom - Sun Path (Nightwave Remix)")
    # MACHINE B holds another version entirely.
    machine_b = library("08A - 124 - Aurora Bloom - Sun Path (Extended)")

    with review.open_store(cfg, path=tmp_path / "a.sqlite3") as store_a:
        asked = settled(machine_a, store_a)
        assert asked.why is match.Why.KEY_DIFFERS
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
