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


@pytest.mark.parametrize(
    "artist,title,version",
    [
        ("Aurora Bloom", "Sun Path", "Someone Remix"),
        ("Aurora Bloom", "Sun Path", ""),
        ("Aurora Bloom", "Sun Path", "Original Mix"),
        ("  Nova   Reef ", " Tide  Line ", "Extended Mix"),
        ("Café del Mar", "Track", "Live"),
    ],
)
def test_a_wanted_track_addresses_a_tombstone_the_way_a_deleted_row_records_it(
    artist, title, version
):
    """The two producers, driven from the two shapes they actually have.

    The deletion pass reads a library row, which carries ONE title with the
    version inside it. This unit reads a listing, which carries a title and a
    version as separate values, and three readers disagree about which. Both have
    to arrive at one mapping, so the listing's pair is recombined into the row's
    spelling rather than hashed as a pair.

    ``Original Mix`` is in the table on purpose: this module folds that qualifier
    away for MATCHING, because a record listed as the original mix and the same
    record listed with nothing are one version. It must NOT fold it away for the
    tombstone, because U24 does not, and a suppression that disagrees about one
    qualifier is a suppression that misses.
    """
    from_a_row = {"artist": u24_fold(artist), "title": u24_fold(f"{title} ({version})".strip())}
    if not version:
        from_a_row = {"artist": u24_fold(artist), "title": u24_fold(title)}
    assert one(artist=artist, title=title.strip(), version=version).identity == from_a_row


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
    assert set(asked.question(about_the_key=True)) == {"recording", "version", "key"}
    assert asked.question(about_the_key=True)["key"] == "08A"
    # The KEY SET never varies, only the value, so a version question asked with
    # a key and one asked without are still one item.
    assert set(asked.question()) == set(asked.question(about_the_key=True))
    assert asked.question()["key"] == ""
    assert one(version="Extended Mix", key="8A").question(about_the_key=True) == asked.question(
        about_the_key=True
    )
    assert one(version="Extended Mix", key="03B").question(
        about_the_key=True
    ) != asked.question(about_the_key=True)


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
    assert {w.identity["title"] for w in from_spotify} == {
        w.identity["title"] for w in from_tidal
    }


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Sun Path - Nightwave Remix", ("Sun Path", "Nightwave Remix")),
        ("Sun Path - Radio Edit", ("Sun Path", "Radio Edit")),
        ("Sun Path - Remastered 2011", ("Sun Path", "Remastered 2011")),
        ("Sun Path - Live", ("Sun Path", "Live")),
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
    ],
    ids=["list-under-artist", "list-under-artists", "objects-under-artist"],
)
def test_every_shape_a_row_spells_its_artists_in_reads_the_same(row):
    """A list under ``artist`` read as NO ARTIST AT ALL, and nothing said so.

    The object branch excluded lists and there was no fallback, so the row hashed
    to an identity matching nothing and a track the library plainly held was
    reported missing at score 50, beside the ``artists`` spelling of the same
    track landing matched. Two spellings of one shape must not be two answers.
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


def test_a_version_question_asked_with_a_key_and_without_one_is_still_one_item(
    cfg, music, tmp_path
):
    """The key set never varies, only the value, so the split is not over-eager.

    A version question is not about the key, so a list that carries one and a
    list that does not ask the same thing and share the answer.
    """
    hold(music, "08A - 124 - Aurora Bloom - Sun Path (Someone Remix)")
    plain = write_list(tmp_path, "Aurora Bloom - Sun Path (Extended Mix)\n", "plain.txt")
    keyed = write_list(
        tmp_path,
        json.dumps(
            {"list": 1, "origin": match.TIDAL,
             "tracks": [{"id": "1", "title": "Sun Path", "version": "Extended Mix",
                         "key": "08A", "artist": {"name": "Aurora Bloom"}}]}
        ),
        "keyed.json",
    )
    _code, first = drive(["match", "run", plain])
    item_id = first["data"]["needs_review"][0]["review_item"]
    _code, second = drive(["match", "run", keyed])
    assert second["data"]["needs_review"][0]["review_item"] == item_id
    assert len(queue_items(cfg)) == 1


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


def test_the_pending_action_counts_questions_rather_than_rows(cfg, music, tmp_path):
    """Two rows of one list that resolve to one item are one thing to answer."""
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
