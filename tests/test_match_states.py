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
import shutil
import sqlite3
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
# the one the tag reader is proven against.
from tests.test_tags import _synth

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


def test_the_version_identity_is_one_function_for_the_queue_and_the_tombstones():
    """Two spellings of this mapping is a suppression nobody can find.

    The queue item and the tombstone address the same thing, and a suppression
    identifier is a hash of the store, the kind, and the identity. A second
    spelling anywhere in that triple records a tombstone the match can never
    look up, and nothing raises: the version reports missing and acquisition
    goes and fetches back exactly what somebody deleted.
    """
    built = match.version_identity("Aurora Bloom", "Sun Path", "Original Mix")
    assert built == {"recording": match.recording_token("Aurora Bloom", "Sun Path"), "version": ""}
    assert one(version="Original Mix").identity == built


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
    probe = _synth(tmp_path, ".flac")
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


def reaches_an_export_reader(source: str) -> set[str]:
    """Which export reader this source binds to, in any import shape.

    BOUND THROUGH THE IMPORT GRAPH, not by attribute name. A guard matching a
    bare ``xml`` attribute passes for a module that imported the parser under
    another name, and fires on a correct module that happens to have a field
    called ``xml``. What is read here is what the source actually imported.
    """
    reached: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            reached.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            reached.add(node.module)
            reached.update(f"{node.module}.{alias.name}" for alias in node.names)
    return {
        name
        for name in reached
        for head in EXPORT_READERS
        if name == head or name.startswith(f"{head}.")
    }


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
    ],
)
def test_the_export_guard_bites_on_every_import_shape(source):
    """P7's other half, the one that keeps getting skipped.

    Running a guard against correct code proves it is quiet. Running it against
    the EVASION is what proves it is a guard. An alias switched an armed
    countdown in this repository off with one keyword, and a dotted submodule
    would do the same to an exact-name set.
    """
    assert reaches_an_export_reader(source)


@pytest.mark.parametrize(
    "source",
    [
        "from cratekit.core import naming, tags\n",
        "import hashlib\nimport unicodedata\n",
        "row = something.xml\n",
        '"""Prose about an xml export and about lxml, in a docstring."""\n',
        "from cratekit.write import trees\n",
    ],
)
def test_the_export_guard_stays_quiet_on_correct_code(source):
    """A guard that fires on correct code is a guard somebody routes around."""
    assert not reaches_an_export_reader(source)


def test_the_match_engine_never_reaches_a_rekordbox_export():
    """Approach point 1: ownership is the disk, never a document that can lag.

    A stale export once reported an owned track unowned, and the run then
    acquired a track the library already held. The guard is that this module
    cannot reach an export reader at all, in any import shape.
    """
    assert reaches_an_export_reader(MATCH_SOURCE.read_text()) == set()
    assert reaches_an_export_reader(MATCH_CLI_SOURCE.read_text()) == set()


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
    deleted = match.version_identity("Aurora Bloom", "Sun Path", "Someone Remix")

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
TEXT_LINES = "1. Aurora Bloom - Sun Path (Someone Remix)\n\n# a comment\nNova Reef - Tide Line\n"


def test_the_three_readers_produce_one_shape():
    from_tidal = match.read_tidal_tracks(TIDAL_ROWS)
    from_spotify = match.read_spotify_items(SPOTIFY_ROWS)
    from_text = match.read_text_lines(TEXT_LINES)
    for read in (from_tidal, from_spotify, from_text):
        assert [(w.artist, w.title, w.version_key) for w in read] == [
            ("Aurora Bloom", "Sun Path", match.version_token("Someone Remix")),
            ("Nova Reef", "Tide Line", ""),
        ]


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
    """A missing track is a fact, not something to adjudicate.

    Offering one would ask a person, once per run forever, to confirm that a
    track they put on a list should be acquired. When acquisition later cannot
    serve it from the configured provider, THAT is a question, and U11 declared
    a different queue for it.
    """
    path = write_list(tmp_path, "Nova Reef - Tide Line\n")
    _code, envelope = drive(["match", "run", path])
    row = envelope["data"]["missing"][0]
    assert row["why"] == str(match.Why.NOT_IN_LIBRARY)
    assert row["review_item"] is None
    assert queue_items(cfg) == []


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
        identity=match.version_identity("Aurora Bloom", "Sun Path", "Someone Remix"),
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
        identity=match.version_identity("Aurora Bloom", "Sun Path", "Someone Remix"),
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
        identity=match.version_identity("Aurora Bloom", "Sun Path", ""),
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


def test_a_web_address_is_refused_with_its_own_sentence(tmp_path):
    """Fetching a playlist needs a session and pagination; the intake verbs own both."""
    with pytest.raises(CratekitError) as excinfo:
        match_cli.read_list(Path("https://example.invalid/playlist/1"))
    assert "web address" in excinfo.value.cause.message


def test_a_list_that_is_not_there_refuses_with_a_code_from_the_vocabulary(cfg, tmp_path):
    code, envelope = drive(["match", "run", str(tmp_path / "nope.txt")])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "intake-list-unusable"


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
